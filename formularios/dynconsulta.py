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
        self.fecha_mes_actual = mx.DateTime.DateTimeFrom(
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
        self.fecha_mes_final = mx.DateTime.DateTimeFrom(anno_final, 
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
            fechacol = mx.DateTime.DateTimeFrom(month = mescol, 
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
            if old_valor != None and valor != old_valor:
                cell.set_property("foreground", "red")
            else:
                cell.set_property("foreground", None)
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
        self.rellenar_widgets()
        self.wids['tv_datos'].expand_all()

    def rellenar_widgets(self):
        """
        Introduce la información del objeto actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
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
        # Vuelvo a volcar todos los valores precalculados. Se calculan al 
        # cargar los conceptos de segundo nivel. Se muestran en primera 
        # instancia estos datos reales en `montar_filas` en lugar de tirar de 
        # las estimaciones de ValorPresupuestoAnual.
        self.mostrar_valores_reales_precalculados(nodos_conceptos, 
                                                  padres, 
                                                  vpro)
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
        penultimo_mes_en_tabla = mx.DateTime.DateFrom(anno, mes, 1)
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
            anno_pasado = mx.DateTime.DateTimeFrom(
                    ultimo_mes_en_tabla.year - 1,
                    ultimo_mes_en_tabla.month, 
                    1)
            if anno_pasado.month == 12:
                anno_pasado_month = 1
                anno_pasado_year = anno_pasado.year + 1
            else:
                anno_pasado_month = anno_pasado.month + 1
                anno_pasado_year = anno_pasado.year
            anno_pasado_mas_1_mes = mx.DateTime.DateTimeFrom(
                    anno_pasado_year,
                    anno_pasado_month, 
                    1)
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
                    nv = v.clone(mes = mx.DateTime.DateTimeFrom(
                        year = v.mes.year + 1, 
                        month = v.mes.month, 
                        day = 1))
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
        model = self.wids['tv_datos'].get_model()
        i = 0.0
        for c in self.precalc[self.fecha_mes_actual]:
            vpro.set_valor(i / len(self.precalc[self.fecha_mes_actual].keys()),
                    "Aplicando sustitución por valores reales...")
            pa = c.presupuestoAnual
            nodo_padre = padres[pa]
            nodo_concepto = nodos_conceptos[c]
            model[nodo_concepto][1] = utils.float2str(
                    self.precalc[self.fecha_mes_actual][c])
            try:
                model[nodo_padre][1] = (utils.float2str(
                    utils.parse_float(model[nodo_padre][1]) 
                    + self.precalc[self.fecha_mes_actual][c]))
            except (TypeError, ValueError):
                model[nodo_padre][1] = utils.float2str(
                                        self.precalc[self.fecha_mes_actual][c])
            i += 1

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
            if (v.mes.month == self.fecha_mes_actual.month 
                    and c.presupuestoAnual.descripcion 
                            == "Proveedores granza"): # OJO: HARCODED
                # Este valor no lo muestro. Tengo que tirar de datos reales.
                try:
                    filas[c][mes_offset]=self.precalc[self.fecha_mes_actual][c]
                except KeyError: # Se ha metido a mano. No hay datos reales.
                    filas[c][mes_offset] = v.importe
            else:
                filas[c][mes_offset] = v.importe
            vpro.set_valor(i / valores_count, 
                           "Cargando valores de dynconsulta...") 
            i += 1
        return filas

    def cargar_conceptos_segundo_nivel(self, vpro):
        i = 0.0
        self.precalc[self.fecha_mes_actual] = precalcular(
                                                        self.fecha_mes_actual, 
                                                        self.wids['ventana'])
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

def precalcular(fecha, ventana_padre = None, usuario = None):
    """
    Devuelve un diccionario de conceptos del mes especificado con los valores
    que se puedan calcular a partir de datos reales.
    Si el concepto no existe, lo crea en la base de datos
    """
    vpro = VentanaActividad(ventana_padre, 
            "Precalculando datos reales del mes en curso...")
    vpro.mostrar()
    # Valores que puedo conocer del ERP (de momento):
    # 1.- IVA (soportado - repercutido)
    # TODO: PORASQUI
    # 2.- Entradas de granza
    vpro.mover()
    primes = fecha
    finmes = mx.DateTime.DateTimeFrom(primes.year, primes.month, -1)
    vpro.mover()
    # Primero: productos granza:
    granzas = pclases.ProductoCompra.select(pclases.AND(
        pclases.ProductoCompra.q.descripcion.contains("granza"), 
        pclases.ProductoCompra.q.obsoleto == False, 
        pclases.ProductoCompra.q.tipoDeMaterialID 
            == pclases.TipoDeMaterial.select(
                 pclases.TipoDeMaterial.q.descripcion.contains("prima")
                )[0].id))
    # Saco datos de facturas:
    fras = pclases.FacturaCompra.select(pclases.AND(
        pclases.FacturaCompra.q.fecha >= primes, 
        pclases.FacturaCompra.q.fecha <= finmes))
    if pclases.DEBUG:
        print __file__, fras.count(), "facturas encontradas."
    # Filtro para quedarme con las de granza:
    vpro.mover()
    res = {}
    for f in fras:
        for ldc in f.lineasDeCompra:
            if ldc.productoCompra in granzas:
                if pclases.DEBUG:
                    print __file__, f.get_info(), ldc.get_info()
                concepto = buscar_concepto_proveedor_granza(ldc.proveedor, 
                                                            usuario)
                try:
                    res[concepto] += ldc.get_subtotal()
                except KeyError:
                    res[concepto] = ldc.get_subtotal()
            vpro.mover()
    # Y ahora de los albaranes no facturados.
    albs = pclases.AlbaranEntrada.select(pclases.AND(
        pclases.AlbaranEntrada.q.fecha >= primes, 
        pclases.AlbaranEntrada.q.fecha <= finmes))
    if pclases.DEBUG:
        print __file__, albs.count(), "albaranes encontrados."
    # Filtro para quedarme con los de granza:
    vpro.mover()
    for a in albs:
        for ldc in a.lineasDeCompra:
            # Solo quiero lo no facturado.
            if not ldc.facturaCompraID and ldc.productoCompra in granzas:
                if pclases.DEBUG:
                    print __file__, a.get_info(), ldc.get_info()
                concepto = buscar_concepto_proveedor_granza(ldc.proveedor, 
                                                            usuario)
                try:
                    res[concepto] += ldc.get_subtotal()
                except KeyError:
                    res[concepto] = ldc.get_subtotal()
            vpro.mover()
    vpro.ocultar()
    if pclases.DEBUG:
        print __file__, res
    return res

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

