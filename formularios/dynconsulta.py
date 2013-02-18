#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2013  Francisco José Rodríguez Bogado                    #
#                          <pacoqueen@users.sourceforge.net>                  #
#                                                                             #
# This file is part of GeotexInn.                                             #
#                                                                             #
# GeotexInn is free software; you can redistribute it and/or modify           #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation; either version 2 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# GeotexInn is distributed in the hope that it will be useful,                #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with GeotexInn; if not, write to the Free Software                    #
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA  #
###############################################################################


###################################################################
## dynconsulta.py - Consulta dinámica resumen de análisis financiero
###################################################################
## Changelog:
## 8 de febrero de 2012 -> Inicio
###################################################################

import sys, os
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, mx, mx.DateTime
try:
    import pclases
    from seeker import VentanaGenerica 
except ImportError:
    sys.path.append(os.path.join('..', 'framework'))
    import pclases
    from seeker import VentanaGenerica 
from utils import _float as float
from ventana_progreso import VentanaProgreso, VentanaActividad
from albaranes_de_salida import buscar_proveedor
from widgets import replace_widget


class DynConsulta(Ventana, VentanaGenerica):
    def __init__(self, objeto = None, usuario = None, mes_actual = None, 
                 num_meses = 12):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.mes_actual = (mes_actual != None and mes_actual 
                                            or mx.DateTime.localtime().month)
        self.update_mes_actual()
        self.num_meses = num_meses != None and num_meses or 12
        self.update_mes_final()
        self.usuario = usuario
        self.clase = None
        self.precalc = {}
        self.dic_campos = {}
        self.old_model = {}
        Ventana.__init__(self, 'dynconsulta.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_nuevo/clicked': self.nuevo,
                       'b_borrar/clicked': self.borrar,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       # 'b_guardar/clicked': self.guardar,
                       'b_buscar/clicked': self.buscar,
                       'sp_mes_actual/value-changed': self.update_mes_actual, 
                       'sp_num_meses/value-changed': self.update_mes_final, 
                       'tv_datos/query-tooltip': self.tooltip_query
                      }  
        self.wids['ch_datos_reales'].set_active(True)
        self.inicializar_ventana()
        self.actualizar_ventana(None)
        self.wids['ventana'].resize(800, 600)
        self.add_connections(connections)
        gtk.main()

    def tooltip_query(self, treeview, x, y, mode, tooltip):
        path = treeview.get_path_at_pos(x, y)
        if path:
            treepath, column = path[:2]
            model = treeview.get_model()
            iter = model.get_iter(treepath)
            texto = model[iter][0].replace("&", "&amp;")
            tooltip.set_text(texto)
        return False

    def es_diferente(self):
        """
        Devuelve True si algún valor en ventana difiere de 
        los del objeto.
        """
        return False

    def update_mes_actual(self, spinbutton_mes = None):
        try:
            self.mes_actual = spinbutton_mes.get_value_as_int()
        except AttributeError: # ¿No se ha creado el glade todavía?
            glade_loaded = False
        else:
            glade_loaded = True
        self.fecha_mes_actual = mx.DateTime.DateFrom(
                                                mx.DateTime.localtime().year, 
                                                self.mes_actual,
                                                1)
        if glade_loaded:
            self.inicializar_ventana()
            self.actualizar_ventana(None)
    
    def update_mes_final(self, sp = None):
        try:
            self.num_meses = sp.get_value_as_int()
        except AttributeError: # ¿No se ha cargado el glade todavía?
            glade_loaded = False
        else:
            glade_loaded = True
        mes_final = ((self.fecha_mes_actual.month-1 + self.num_meses) % 12) + 1
        anno_final = self.fecha_mes_actual.year + (self.num_meses / 12)
        while mes_final > 12:
            anno_final += 1
            mes_final -= 12
        self.fecha_mes_final = mx.DateTime.DateFrom(anno_final, 
                                                    mes_final, 
                                                    1)
        if glade_loaded:
            self.inicializar_ventana()
            self.actualizar_ventana(None)

    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        antiguo_tv_datos = self.wids['tv_datos']
        nuevo_tv_datos = gtk.TreeView()
        nuevo_tv_datos.show()
        replace_widget(antiguo_tv_datos,nuevo_tv_datos)
        self.wids['tv_datos'] = nuevo_tv_datos
        self.wids['sp_mes_actual'].set_value(self.mes_actual)
        self.wids['sp_num_meses'].set_value(self.num_meses)
        self.activar_widgets(False)
        self.wids['b_actualizar'].set_sensitive(True)
        self.wids['b_guardar'].set_sensitive(False)
        self.wids['b_buscar'].set_sensitive(True)
        for b in ("b_nuevo", "b_guardar", "b_borrar"):
            self.wids[b].set_property("visible", False)
        # Inicialización del resto de widgets:
        cols = [('Concepto', 'gobject.TYPE_STRING', False, True, True, None)]
        if not self.mes_actual:
            mes = mx.DateTime.localtime().month
        else:
            mes = self.mes_actual
        for m in range(self.num_meses):
            mescol = ((mes - 1 + m) % 12) + 1 
            fechacol = mx.DateTime.DateFrom(month = mescol, 
                    year = mx.DateTime.localtime().year + (m > 0 and 1 or 0))
            if mescol == 1:
                strmes = fechacol.strftime("%B'%y")
            else:
                strmes = fechacol.strftime("%B")
            cols.append((strmes,'gobject.TYPE_STRING',False,True,True,None))
        cols += [('PUID', 'gobject.TYPE_STRING', False, False, False, None)]
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        for n in range(1, self.num_meses + 1):
            col = self.wids['tv_datos'].get_column(n).get_cell_renderers()[0]\
                    .set_property("xalign", 1)
        col = self.wids['tv_datos'].get_column(0)
        col.set_expand(True)
        self.wids['tv_datos'].connect("row-activated", self.inspect)
        self.wids['tv_datos'].set_tooltip_column(0)
        self.wids['tv_datos'].connect("query-tooltip", self.tooltip_query)
        self.colorear(self.wids['tv_datos'])

    def colorear(self, tv):
        """
        Pone en rojo los valores que han cambiado respecto a la última vez 
        que se actualizó el model.
        """
        def cell_func(col, cell, model, itr, numcol):
            valor = model[itr][numcol]
            if not model.iter_parent(itr):  # Es concepto de primer nivel
                padre = model[itr][0]
                try:
                    old_valor = self.old_model[padre]['valores'][numcol-1]
                except (KeyError, IndexError):
                    old_valor = None
            else:
                padre = model[model.iter_parent(itr)][0]
                hijo = model[itr][0]
                try:
                    old_valor = self.old_model[padre]['hijos'][hijo][numcol-1]
                except (KeyError, IndexError):
                    old_valor = None
            if self.old_model and old_valor != valor: 
                # Valor puede ser None porque es la primera vez que se muestran
                # toodos los datos y en ese caso no debe colorear.
                cell.set_property("foreground", "dark green")
                if not model.iter_parent(itr):
                    cell.set_property("weight", 4000)
                    cell.set_property("background", "gray")
                else:
                    cell.set_property("weight", 400)
                    cell.set_property("background", "yellow")
            else:
                if not model.iter_parent(itr):
                    cell.set_property("foreground", "white")
                    cell.set_property("weight", 4000)
                    cell.set_property("background", "gray")
                else:
                    cell.set_property("foreground", None)
                    cell.set_property("weight", 400)
                    cell.set_property("background", None)
        cols = tv.get_columns()
        for i in xrange(1, len(cols)):
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell, cell_func, i)

    def inspect(self, tv, path, col):
        """
        Muestra de dónde vienen los datos precalculados.
        """
        indexcol = get_col_pos(tv, col)
        if indexcol > 0:
            mes = self.mes_actual + indexcol - 1
            model = tv.get_model()
            valor = model[path][indexcol]
            concepto = pclases.getObjetoPUID(model[path][-1]).descripcion
            txt_inspect = "Aquí va una traza del valor %s (%s)"\
                          " para el mes %s (%d)." % (
                            valor, concepto, col.get_property("title"), mes)
            utils.dialogo_info(
                    titulo = "INSPECCIONAR VALOR «%s»" % valor, 
                    texto = txt_inspect, 
                    padre = self.wids['ventana'])

    def activar_widgets(self, s, chequear_permisos = True):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        if self.objeto == None:
            s = False
        ws = []
        for w in ws:
            try:
                self.wids[w].set_sensitive(s)
            except Exception, msg:
                print "Widget problemático:", w, "Excepción:", msg
                import traceback
                traceback.print_last()
        if chequear_permisos:
            self.check_permisos(nombre_fichero_ventana = "dynconsulta.py")

    def actualizar_ventana(self, boton = None):
        self.precalc = precalcular(self.fecha_mes_actual, 
                                   self.fecha_mes_final, 
                                   self.wids['ventana'])
        self.rellenar_widgets()
        self.wids['tv_datos'].expand_all()

    def rellenar_widgets(self):
        # Los únicos otros dos widgets son los de mes de inicio y ancho de 
        # tabla en meses, que ya se rellenan ellos solos.
        self.rellenar_tabla()

    def rellenar_tabla(self):
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        model = self.wids['tv_datos'].get_model()
        self.old_model = bak_model(model)
        model.clear()
        padres = self.cargar_conceptos_primer_nivel(vpro)
        filas = self.cargar_conceptos_segundo_nivel(vpro)
        filas = self.montar_filas(filas, vpro)
        nodos_conceptos = self.mostrar_matriz_en_treeview(filas, padres, vpro)
        if self.wids['ch_datos_reales'].get_active():
            self.mostrar_valores_reales_precalculados(nodos_conceptos, 
                                                      padres, vpro)
        # Ahora toca pasar el mes que se ha ido al final del año actual. Ciclo 
        # el mes si el último mes mostrado en la cuadrícula está completamente 
        # a cero. Uso como datos de referencia el del mismo mes pero del 
        # año anterior. Si también está a cero (nunca se ha presupuestado ese
        # mes en la historia del programa), desisto.
        self.ciclar_mes(vpro)
        vpro.ocultar()

    def ciclar_mes(self, vpro):
        model = self.wids['tv_datos'].get_model()
        pasar_mes = True
        # Primero busco valores que ya existen en la BD. Porque puede ser que 
        # los valores a cero en el TreeView provengan de datos "reales" (esto 
        # es, no estimados) que se almacenan en precalc y tienen preferencia 
        # sobre los datos del presupuesto a la hora de mostrarse. En ese caso 
        # siempre se van a mostrar los valores 0 y siempre va a intentar 
        # pasar el mes de año pasado al actual, duplicando los valores en la 
        # BD.
        ultimo_mes_en_tabla = self.fecha_mes_final
        mes = ultimo_mes_en_tabla.month
        if mes == 1:
            anno = ultimo_mes_en_tabla.year - 1
            mes = 12
        else:
            mes -= 1
            anno = ultimo_mes_en_tabla.year
        penultimo_mes_en_tabla = restar_mes(ultimo_mes_en_tabla)
        valores = pclases.ValorPresupuestoAnual.select(pclases.AND(
            pclases.ValorPresupuestoAnual.q.mes <= ultimo_mes_en_tabla, 
            pclases.ValorPresupuestoAnual.q.mes > penultimo_mes_en_tabla))
        if pclases.DEBUG:
            print __file__, "ultimo_mes_en_tabla", ultimo_mes_en_tabla
            print __file__, "penultimo_mes_en_tabla", penultimo_mes_en_tabla
            print __file__, "valores.count()", valores.count()
        if not valores.count():     # Nunca se ha hecho el presupuesto para 
            # ese mes/año. Hora de crearlo a partir del año pasado (si es que 
            # no hay valores precalculados o algo y realmente está todo a 0).
            # Ahora compruebo entonces los valores actuales en el TreeView 
            # para ver si está todo a cero.
            for fila in model:
                if pclases.DEBUG:
                    print fila[0], fila[-2] and utils._float(fila[-2])
                if fila[-2] and utils._float(fila[-2]) != 0:
                    pasar_mes = False
                    break
            if pclases.DEBUG: print "(1) >>> pasar_mes", pasar_mes
            # Valores antiguos los busco en el año pasado.
            anno_pasado = restar_mes(ultimo_mes_en_tabla, 12)
            anno_pasado_mas_1_mes = restar_mes(anno_pasado, -1)
            valores_clonar = pclases.ValorPresupuestoAnual.select(pclases.AND(
                    pclases.ValorPresupuestoAnual.q.mes >= anno_pasado, 
                    pclases.ValorPresupuestoAnual.q.mes < anno_pasado_mas_1_mes
                    ))
            valores_count = valores_clonar.count()
            if (not valores_count 
                    or sum([v.importe for v in valores_clonar]) == 0):
                # No hay nada que copiar. Bucle infinito a cero.
                pasar_mes = False
            if pclases.DEBUG:
                print __file__, valores_count
                for v in valores_clonar:
                    print v.get_info(), v.importe
            if pclases.DEBUG: print "(2) >>> pasar_mes", pasar_mes
            if pasar_mes:
                # Copio a valores nuevos
                i = 0.0
                for v in valores_clonar:
                    vpro.set_valor(i / valores_count, 
                                   "Trasladando valores antiguos...") 
                    nv = v.clone(mes = restar_mes(v.mes, -12))
                    if pclases.DEBUG:
                        print __file__, "Nuevo valor:", nv.get_info(), \
                                nv.importe, utils.str_fecha(nv.mes)
                    pclases.Auditoria.nuevo(nv, self.usuario, __file__)
                    i += 1
                # Y refresco (una tónica, por favor. ¡CHISTACO!)
                self.actualizar_ventana()

    def mostrar_valores_reales_precalculados(self, 
                                             nodos_conceptos, 
                                             padres, 
                                             vpro):
            # PORASQUI: Aquí es donde debería comprobar el criterio de 
            #           sustitición en cada caso: forma de pago en compras, 
            #           mes siguiente (¿o era trimestral?) en IVA, etc.
            # TODO: Hay otro problema: Supongamos un valor precalculado que es 
            # de un concepto que no existe en los valores presupuestados, por 
            # lo tanto no puede sustituir a nadie y se va a ignorar.
        #    if criterio_sustitucion(v, self.fecha_mes_actual):
            #if (v.mes.month == self.fecha_mes_actual.month 
            #        and c.presupuestoAnual.descripcion 
            #                == "Proveedores granza"): # OJO: HARCODED
                # Tengo que tirar de datos reales. Este valor no lo muestro, o 
                # muestro solo la parte proporcional que resta de los datos 
                # reales (mirar specs para asegurarme).
        #        filas[c][mes_offset] = ""
                # Los datos reales los volcaré después.
                #try:
                #    filas[c][mes_offset]=self.precalc[self.fecha_mes_actual][c]
                #except KeyError: # Se ha metido a mano. No hay datos reales.
                #    filas[c][mes_offset] = v.importe
            # TODO: Si me muevo a mayo el total es 2000 reales + 275 estimados, pero solo veo en el cell 2000 de reales. Eso es porque todavía no estoy sustituyendo realmente los datos, sino machacando.
        model = self.wids['tv_datos'].get_model()
        for mescol in range(self.num_meses):
            fechacol = restar_mes(self.fecha_mes_actual, -mescol)
            i = 0.0
            try:
                datos_reales = self.precalc[fechacol]
            except KeyError:    # Lo no nay ;)
                datos_reales = []
            for concepto in datos_reales:
                vpro.set_valor(
                        i / len(self.precalc[fechacol].keys()),
                        "Aplicando sustitución por valores reales en %s..." 
                            % fechacol.strftime("%B"))
                # Si había un valor previo, tengo que retirar la estimación 
                # y sumar lo real. En caso de granza, entonces la parte 
                # proporcional de las Tm.
                importe_valor_real = self.precalc[fechacol][concepto]
                valor_presupuestado = buscar_valor_presupuestado(fechacol, 
                                                                 concepto)
                if criterio_sustitucion(valor_presupuestado, 
                                        importe_valor_real):
                    # Y si no, dejo lo que estaba.
                    if pclases.DEBUG:
                        print __file__, "Cambio presupuesto por real:", \
                                valor_presupuestado, importe_valor_real
                    diff = self.cambiar_valor_presupuestado(importe_valor_real, 
                                                            valor_presupuestado,
                                                            concepto, 
                                                            fechacol, 
                                                            )
                    # PORASQUI: ¿De dónde salía nodo_padre y qué era?
                    self.actualizar_sumatorio_padre(model, nodo_padre, mescol, 
                                                    fechacol, diff)
                i += 1

    def cambiar_valor_presupuestado(self, valor_real, valor_presupuestado, 
                                    concepto, fechacol):
        """
        Si el valor presupuestado es de granza, quita el importe 
        correspondiente a las toneladas del valor real y suma este valor 
        real a lo que quede. Deja en el cell la cantidad final.
        Devuelve la diferencia entre el nuevo valor y el que había antes 
        para que se actualice el nodo padre únicamente sumando esa cantidad y 
        así evitar recalcular toda la "subcolumna".
        """
        if valor_presupuestado:
            valor_presupuestado_importe = valor_presupuestado.importe
            if valor_presupuestado.es_de_granza():
                valor_real_toneladas=self.precalc[fechacol][concepto]['toneladas']
                valor_presup_restante = (valor_presupuestado.precio 
                    * (valor_presupuestado.toneladas - valor_real_toneladas))
            else:
                # Como voy a sustituirlo entero, el valor restante es 0.0 para que 
                # solo se vea el valor real que le voy a sumar.
                valor_presup_restante = 0.0
            pa = concepto.presupuestoAnual
            nodo_padre = padres[pa]
            nodo_concepto = nodos_conceptos[concepto]
            model[nodo_concepto][mescol + 1] = utils.float2str(
                    valor_presup_restante + valor_real)
        else:
            valor_presup_restante = 0.0
            valor_presupuestado_importe = 0.0
        return (valor_presup_restante + valor_real)-valor_presupuestado_importe

    def actualizar_sumatorio_padre(self, model, nodo_padre, mescol, fechacol, 
                                   diff):
        # Thanks bicycle repair man!
        try:
            model[nodo_padre][mescol + 1] = (utils.float2str(
                utils.parse_float(model[nodo_padre][mescol + 1]) 
                + diff))
        except (TypeError, ValueError):
            model[nodo_padre][mescol + 1] = utils.float2str(diff)

    def mostrar_matriz_en_treeview(self, filas, padres, vpro):
        model = self.wids['tv_datos'].get_model()
        i = 0.0
        nodos_conceptos = {}
        for c in filas:
            vpro.set_valor(i / len(filas.keys()), 
                           "Montando matriz...")
            pa = c.presupuestoAnual
            nodo_padre = padres[pa]
            fila = [c.descripcion # FIXME: .replace("&", "&amp;") # 
                                  #        Problemas con el tooltip.
                    ] + filas[c] + [c.puid]
            nodos_conceptos[c] = model.append(nodo_padre, fila)
            for mes_matriz in range(1, self.num_meses + 1):
                # Actualizo totales de fila padre
                try:
                    model[nodo_padre][mes_matriz] = utils.float2str(
                            utils.parse_float(model[nodo_padre][mes_matriz]) 
                            + fila[mes_matriz])
                except (TypeError, ValueError):
                    model[nodo_padre][mes_matriz] = utils.float2str(
                            fila[mes_matriz])
            i += 1
        return nodos_conceptos 

    def montar_filas(self, filas, vpro):
        i = 0.0
        valores = pclases.ValorPresupuestoAnual.select(pclases.AND(
            pclases.ValorPresupuestoAnual.q.mes >= self.fecha_mes_actual, 
            pclases.ValorPresupuestoAnual.q.mes < self.fecha_mes_final)) 
        valores_count = valores.count()
        for v in valores:
            v.sync()
            c = v.conceptoPresupuestoAnual
            mes_offset = (v.mes.month - self.fecha_mes_actual.month) % (
                                                                self.num_meses)
            filas[c][mes_offset] = v.importe
            vpro.set_valor(i / valores_count, 
                           "Cargando valores de dynconsulta...") 
            i += 1
        return filas

    def cargar_conceptos_segundo_nivel(self, vpro):
        i = 0.0
        conceptos = pclases.ConceptoPresupuestoAnual.select()
        conceptos_count = conceptos.count()
        filas = {}
        for c in conceptos:
            filas[c] = []
            for m in range(self.num_meses):
                filas[c].append(0)
            vpro.set_valor(i / conceptos_count, 
                           "Cargando conceptos de dynconsulta...") 
            i += 1
        return filas

    def cargar_conceptos_primer_nivel(self, vpro):
        vpro.set_valor(0, "Cargando conceptos de primer nivel...") 
        model = self.wids['tv_datos'].get_model()
        padres = {}
        pas = pclases.PresupuestoAnual.select()
        pas_count = pas.count()
        i = 0.0
        for pa in pas:
            fila = [pa.descripcion] #FIXME: .replace("&", "&amp;")]
            for m in range(self.num_meses):
                fila.append("")
            fila.append(pa.puid)
            nodo = model.append(None, fila) 
            padres[pa] = nodo 
            vpro.set_valor(i / pas_count, 
                           "Cargando conceptos de primer nivel...") 
            i += 1
        return padres
            
    def buscar(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        # TODO: Buscar dentro de todas las filas un texto tecleado y 
        #       pasarle el foco o algo.
        pass

def precalcular(fecha_ini, fecha_fin, ventana_padre = None, usuario = None):
    """
    Devuelve un diccionario de conceptos del mes especificado con los valores
    que se puedan calcular a partir de datos reales.
    Si el concepto no existe, lo crea en la base de datos
    """
    vpro = VentanaActividad(ventana_padre, "Precalculando datos reales...")
    vpro.mostrar()
    # Valores que puedo conocer del ERP (de momento):
    # 1.- Entradas de granza
    res = calcular_entradas_de_granza(vpro, fecha_ini, fecha_fin, usuario)
    # 2.- IVA (soportado - repercutido)
    calcular_iva_real(res, vpro, fecha_ini)
    # 3.- Ventas por tipo (internacionales, geotextiles, geocompuestos...)
    #calcular_ventas(res, vpro, fecha_ini, fecha_fin)
    if pclases.DEBUG:
        print __file__, res
    return res

def calcular_iva_real(res, vpro, fecha):
    """
    Calcula el IVA del mes de la fecha y lo almacena en el concepto 
    «Impuestos» de los valores precalculados.
    """
    vpro.mover()
    concepto = buscar_concepto_iva()
    vpro.mover()
    soportado = calcular_soportado(vpro, fecha)
    vpro.mover()
    repercutido = calcular_repercutido(vpro, fecha)
    vpro.mover()
    try:
        res[fecha][concepto]['importe'] = soportado - repercutido 
    except KeyError:
        res[fecha] = {concepto: soportado - repercutido}
    # FIXME: Devuelvo en negativo o positivo, pero el resto de cifras (ventas, 
    # compras, salarios, etc.) va en positivo aunque sean gastos. Preguntar en 
    # la siguiente reunión.

def buscar_concepto_iva():
    # OJO: Harcoded
    try:
        c = pclases.ConceptoPresupuestoAnual.selectBy(descripcion = "IVA")[0]
    except IndexError:
        try:
            padre=pclases.PresupuestoAnual.selectBy(descripcion="Impuestos")[0]
        except IndexError:
            padre = pclases.PresupuestoAnual(descripcion = "Impuestos")
        c = pclases.ConceptoPresupuestoAnual(descripcion = "IVA", 
                                             presupuestoAnual = padre)
    return c

def calcular_soportado(vpro, fecha):
    # Pago este mes el IVA del mes pasado. Ojo.
    fini = restar_mes(fecha)
    fini = mx.DateTime.DateTimeFrom(fini.year, fini.month, 1)
    ffin = mx.DateTime.DateTimeFrom(fini.year, fini.month, -1)
    frascompra = pclases.FacturaCompra.select(pclases.AND(
        pclases.FacturaCompra.q.fecha >= fini, 
        pclases.FacturaCompra.q.fecha <= ffin))
    iva = sum([f.calcular_importe_iva() for f in frascompra])
    return iva

def calcular_repercutido(vpro, fecha):
    # Pago este mes el IVA del mes pasado. Ojo.
    fini = restar_mes(fecha)
    fini = mx.DateTime.DateTimeFrom(fini.year, fini.month, 1)
    ffin = mx.DateTime.DateTimeFrom(fini.year, fini.month, -1)
    frasventa = pclases.FacturaVenta.select(pclases.AND(
        pclases.FacturaVenta.q.fecha >= fini, 
        pclases.FacturaVenta.q.fecha <= ffin))
    iva = sum([f.calcular_total_iva() for f in frasventa])
    return iva

def restar_mes(fecha = mx.DateTime.today(), meses = 1):
    if meses > 0:
        try:
            return restar_mes(
                    mx.DateTime.DateFrom(fecha.year, 
                                         fecha.month - 1, 
                                         fecha.day), 
                    meses - 1)
        except mx.DateTime.RangeError:
            return restar_mes(
                    mx.DateTime.DateFrom(fecha.year - 1, 
                                         12, 
                                         fecha.day), 
                    meses - 1)
    elif meses < 0:
        try:
            return restar_mes(
                    mx.DateTime.DateFrom(fecha.year, 
                                         fecha.month + 1, 
                                         fecha.day), 
                    meses + 1)
        except mx.DateTime.RangeError:
            return restar_mes(
                    mx.DateTime.DateFrom(fecha.year + 1, 
                                         1, 
                                         fecha.day), 
                    meses + 1)
    else:
        return fecha

def calcular_entradas_de_granza(vpro, fecha_ini, fecha_fin, usuario):
    vpro.mover()
    primes = fecha_ini
    finmes = mx.DateTime.DateFrom(fecha_fin.year, fecha_fin.month, -1)
    vpro.mover()
    # Primero: productos granza:
    granzas = buscar_productos_granza()
    # Saco datos de facturas:
    vtos = buscar_vencimientos_compra(primes, finmes)
    # Filtro para quedarme con las de granza:
    vpro.mover()
    res = {}
    clasificar_vencimientos_compra(vtos, granzas, usuario, res, vpro)
    vpro.mover()
    # Y ahora de los albaranes no facturados.
    albs = buscar_albaranes_de_entrada(primes, finmes)
    vpro.mover()
    # Filtro para quedarme con los de granza:
    clasificar_albaranes_de_entrada(albs, granzas, usuario, res, vpro)
    vpro.ocultar()
    return res

def clasificar_albaranes_de_entrada(albs, granzas, usuario, res, vpro):
    for a in albs:
        for ldc in a.lineasDeCompra:
            # Solo quiero lo no facturado.
            if not ldc.facturaCompraID and ldc.productoCompra in granzas:
                if pclases.DEBUG:
                    print __file__, a.get_info(), ldc.get_info()
                concepto = buscar_concepto_proveedor_granza(ldc.proveedor, 
                                                            usuario)
                fecha = primero_de_mes(ldc.albaranEntrada.fecha)
                if fecha not in res:
                    res[fecha] = {}
                try:
                    res[fecha][concepto]['importe'] += ldc.get_subtotal()
                    res[fecha][concepto]['toneladas'] += ldc.cantidad
                except KeyError:
                    res[fecha][concepto] = {'importe': ldc.get_subtotal(), 
                                            'toneladas': ldc.cantidad}
            vpro.mover()

def buscar_albaranes_de_entrada(primes, finmes):
    albs = pclases.AlbaranEntrada.select(pclases.AND(
        pclases.AlbaranEntrada.q.fecha >= primes, 
        pclases.AlbaranEntrada.q.fecha <= finmes))
    if pclases.DEBUG:
        print __file__, albs.count(), "albaranes encontrados."
    return albs

def clasificar_vencimientos_compra(vtos, granzas, usuario, res, vpro):
    # Me quedo solo con los vencimientos de fras. de compra de granza.
    fras = []
    for v in vtos:
        if pclases.DEBUG:
            print __file__, v.get_info(), v.fecha
        fra = v.facturaCompra
        for ldc in fra.lineasDeCompra:
            ldc.sync
            ldc.sync()
            ldc.facturaCompra and ldc.facturaCompra.sync()
            ldc.albaranEntrada and ldc.albaranEntrada.sync()
            if ldc.productoCompra in granzas:
                if pclases.DEBUG:
                    print __file__, fra.get_info(), ldc.get_info()
                concepto = buscar_concepto_proveedor_granza(ldc.proveedor, 
                                                            usuario)
                fechas_mes_vto = buscar_mes_vto(ldc.facturaCompra)
                importe = ldc.get_subtotal() / len(fechas_mes_vto)
                cantidad = ldc.cantidad / len(fechas_mes_vto)
                for fecha_mes_vto in fechas_mes_vto:
                    if fecha_mes_vto not in res:
                        res[fecha_mes_vto] = {}
                    try:
                        res[fecha_mes_vto][concepto]['importe'] += importe
                        res[fecha_mes_vto][concepto]['toneladas'] += cantidad
                    except KeyError:
                        res[fecha_mes_vto][concepto] = {'importe': importe, 
                                                        'toneladas': cantidad}
            vpro.mover()

def buscar_mes_vto(fra_compra):
    """Devuelve las fechas de vencimiento de la factura. Si no tiene 
    vencimientos (algún usuario se está haciendo el remolón con su trabajo) 
    entonces devuelve la fecha de la factura.
    Las fechas las devuelve a primero del mes que sea, ignorando el día real
    de pago.

    :fra_compra: pclases.FacturaCompra
    :returns: mx.DateTime.Date

    """
    fechas = []
    for v in fra_compra.vencimientosPago:
        fechas.append(primero_de_mes(v.fecha))
    if not fechas:
        fechas = [primero_de_mes(fra_compra.fecha)]
    return fechas

def primero_de_mes(f):
    return mx.DateTime.DateFrom(f.year, f.month, 1)

def final_de_mes(f):
    return mx.DateTime.DateFrom(f.year, f.month, -1)

def buscar_vencimientos_compra(primes, finmes):
    vtos = pclases.VencimientoPago.select(pclases.AND(
        pclases.VencimientoPago.q.fecha >= primes, 
        pclases.VencimientoPago.q.fecha <= finmes))
    # Filtro y saco los que ya están pagados (ver doc. requisitos)
    vtos_pdtes = [v for v in vtos if v.calcular_importe_pdte() > 0]
    if pclases.DEBUG:
        print __file__, len(vtos_pdtes), "de", vtos.count(), \
              "vencimientos encontrados."
    return vtos

def buscar_productos_granza():
    granzas = pclases.ProductoCompra.select(pclases.AND(
        pclases.ProductoCompra.q.descripcion.contains("granza"), 
        pclases.ProductoCompra.q.obsoleto == False, 
        pclases.ProductoCompra.q.tipoDeMaterialID 
            == pclases.TipoDeMaterial.select(
                 pclases.TipoDeMaterial.q.descripcion.contains("prima")
                )[0].id))
    return granzas

def buscar_concepto_proveedor_granza(proveedor, usuario = None):
    """
    Busca el concepto del dynconsulta anual correspondiente al proveedor. Si 
    no lo encuentra, lo crea.
    """
    try:
        concepto = pclases.ConceptoPresupuestoAnual.select(
          pclases.ConceptoPresupuestoAnual.q.descripcion==proveedor.nombre)[0]
    except IndexError:
        concepto = pclases.ConceptoPresupuestoAnual(
                descripcion = proveedor.nombre, 
                presupuestoAnual = pclases.PresupuestoAnual.select(
                    pclases.PresupuestoAnual.q.descripcion 
                        == "Proveedores granza")[0] # EXISTE. Hay un check al 
                                            # principio que se asegura de eso.
                )
        pclases.Auditoria.nuevo(concepto, usuario, __file__)
    return concepto

def get_col_pos(tv, col):
    """
    Devuelve la posición (índice entero comenzando por 0) de la columna en 
    el TreeView.
    """
    return tv.get_columns().index(col)


def bak_model(model):
    res = {}
    for fila in model:
        res[fila[0]] = {'valores': [], 'hijos': {}}
        for i in range(1, len(fila)):
            res[fila[0]]['valores'].append(fila[i])
        for sub_fila in fila.iterchildren():
            res[fila[0]]['hijos'][sub_fila[0]] = []
            for j in range(1, len(sub_fila)):
                res[fila[0]]['hijos'][sub_fila[0]].append(sub_fila[j])
    return res

def criterio_sustitucion(valor_presupuesto, fecha = None):
    # TODO: PORASQUI: Falta el criterio del IVA, comprobar que este es correcto...
    sustituir_por_reales = True
    if valor_presupuesto:
        sustituir_por_reales = False
        if fecha == None:
            fecha = primero_de_mes(mx.DateTime.today())
        if (valor_presupuesto.es_de_granza() 
                and valor_presupuesto.mes.month == fecha.month):
            # PORASQUI: (también) TODO: Principio de realidad: Siempre que haya 
            # datos reales, se sustituyen las estimaciones por datos reales. 
            # Esto significa que si han entrado 15 toneladas de granza, en el mes 
            # de su vencimiento se retiran 15 toneladas al precio estimado y se 
            # pone el importe real de esas 15 toneladas sumadas al resto de 
            # estimado. ¿Seguro? Revisa las specs, anda.
            sustituir_por_reales = True
        if (valor_presupuesto.es_de_iva() 
                and valor_presupuesto.mes.month == fecha.month):
            sustituir_por_reales = True
        if pclases.DEBUG:
            print __file__, "-------->>>>", \
                    valor_presupuesto.conceptoPresupuestoAnual.descripcion, \
                    valor_presupuesto.mes.month, "sustituir_por_reales [", \
                    sustituir_por_reales, "]"
    return sustituir_por_reales

def buscar_valor_presupuestado(fecha, concepto):
    """
    Devuelve el objeto valor del presupuesto para la fecha y concepto 
    especificados.
    """
    try:
        return pclases.ValorPresupuestoAnual.select(pclases.AND(
            pclases.ValorPresupuestoAnual.q.mes == fecha, 
            pclases.ValorPresupuestoAnual.q.conceptoPresupuestoAnualID 
                == concepto.id))[0]
    except IndexError:
        return None

if __name__ == "__main__":
    """
    Primer parámetro: número de meses a mostrar.
    Segundo parámetro: primer mes a mostrar (1 = enero).
    """
    pclases.DEBUG = True
    try:
        num_meses = int(sys.argv[1])
    except (TypeError, ValueError, IndexError):
        num_meses = None
    try:    # Para testeo. 1 = Enero
        mes = int(sys.argv[2])
    except (TypeError, ValueError, IndexError):
        mes = None
    p = DynConsulta(mes_actual = mes, num_meses = num_meses)

