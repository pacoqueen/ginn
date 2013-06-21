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

import sys
from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk, mx.DateTime
from framework import pclases
from framework.seeker import VentanaGenerica 
old_float = float
from ventana_progreso import VentanaProgreso, VentanaActividad
from widgets import replace_widget
import pprint
from collections import defaultdict
try:
    from collections import MutableMapping as transformedDictBase
except ImportError:
    transformedDictBase = object
from informes.treeview2pdf import treeview2pdf
from informes.treeview2csv import treeview2csv
from formularios.reports import abrir_pdf, abrir_csv
import pango
import datetime

class TransformedDict(transformedDictBase):
    """
    A dictionary which applies an arbitrary key-altering function before 
    accessing the keys"""
    # From: http://stackoverflow.com/questions/3387691/
    #                                   python-how-to-perfectly-override-a-dict

    def __init__(self, *args, **kwargs):
        self.store = dict()
        try:
            self.update(dict(*args, **kwargs)) #use the free update to set keys
        except AttributeError:
            self.store.update(*args, **kwargs)

    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key

    def __str__(self):
        return pprint.pformat(self.store)

    def __repr__(self):
        return pprint.pformat(self.store)


class MyMonthsDict(TransformedDict):
    def __keytransform__(self, key):
        try:
            assert isinstance(key, (type(mx.DateTime.today()), datetime.date))
            key = primero_de_mes(key)
        except AssertionError:
            anno = mx.DateTime.today().year
            mes = mx.DateTime.today().month
            if key < mes:
                anno += 1
            return mx.DateTime.DateFrom(anno, key, 1)
        else:
            return key

def activate(ch, ch_destino):
    ch_destino.set_sensitive(ch.get_active())

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
        self.precalc = MyMonthsDict()
        self.dic_campos = {}
        self.old_model = {}
        Ventana.__init__(self, 'dynconsulta.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_nuevo/clicked': self.nuevo,
                       'b_borrar/clicked': self.borrar,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       # 'b_guardar/clicked': self.guardar,
                       'b_buscar/clicked': self.buscar,
                       'sp_mes_actual/value-changed': self.update_mes_actual, 
                       'sp_num_meses/value-changed': self.update_mes_final, 
                       'tv_datos/query-tooltip': self.tooltip_query, 
                       'b_exportar/clicked': self.exportar,  
                       'b_imprimir/clicked': self.imprimir
                      }  
        self.wids['ch_presupuesto'].set_active(True) 
        self.wids['ch_datos_reales'].set_active(True) 
        self.wids['ch_reales_mes0'].set_active(True) 
        self.wids['ch_datos_pdtes'].set_active(False) 
        self.wids['ch_datos_reales'].connect("toggled", 
                lambda ch, chdest: chdest.set_sensitive(ch.get_active()),
                self.wids['ch_datos_pdtes'])
        self.inicializar_ventana()
        self.actualizar_ventana(None)
        self.wids['ventana'].resize(800, 600)
        self.add_connections(connections)
        gtk.main()

    def tooltip_query(self, treeview, x, y, mode, tooltip):
        path = treeview.get_path_at_pos(x, y)
        if path:
            treepath, column = path[:2]  # @UnusedVariable
            model = treeview.get_model()
            itr = model.get_iter(treepath)
            texto = model[itr][0].replace("&", "&amp;")
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
        return False    # GtkEntry - did not receive focus-out-event. If you connect a handler to this signal, it must return FALSE so the entry gets the event as well
    
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
        if self.fecha_mes_final < self.fecha_mes_actual:
            self.fecha_mes_final = mx.DateTime.DateFrom(
                    self.fecha_mes_final.year + 1, 
                    self.fecha_mes_final.month, 
                    self.fecha_mes_final.day)
        if glade_loaded:
            self.inicializar_ventana()
            self.actualizar_ventana(None)
        return False    # GtkEntry - did not receive focus-out-event. If you connect a handler to this signal, it must return FALSE so the entry gets the event as well

    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        self.wids['e_costes'].modify_text(gtk.STATE_NORMAL, 
                self.wids['e_costes'].get_colormap().alloc_color("red"))
        self.wids['e_ingresos'].modify_text(gtk.STATE_NORMAL, 
                self.wids['e_ingresos'].get_colormap().alloc_color("blue"))
        self.wids['e_costes'].set_property("xalign", 0.9)
        self.wids['e_ingresos'].set_property("xalign", 0.9)
        self.wids['e_total'].set_property("xalign", 0.9)
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
            self.wids['tv_datos'].get_column(n).get_cell_renderers()[0]\
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
            # Extraigo valor numérico
            valor = model[itr][numcol]
            try:
                valor_numerico = utils._float(valor)
            except (TypeError, ValueError):
                valor_numerico = None
            # Color gradual en función de datos reales / datos precalculados
            puid = model[itr][-1]
            try:
                real = self.cave[puid][numcol]
            except KeyError:    # Es defaultdict, pero por si acaso.
                real = 0   # Puro presupuesto. Nada de valor real.
            if valor_numerico and real:
                try:
                    proporcion = 1.0 - (abs(real) / abs(valor_numerico))
                    grade = int(proporcion * 65535)
                except ZeroDivisionError: # Por si acaso. XD
                    grade = 0
                bg_color = gtk.gdk.Color(red = int(65535*0.9 + grade*0.1), 
                                         green = int(65535*0.7 + grade * 0.3), 
                                         blue = int(65535*0.1 + grade*0.9))
            else:
                bg_color = None    # No hay valor o es otra cosa
            # Extraigo valor anterior:
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
            # Color de cambio de valores respecto a "iteración" anterior
            if self.old_model and old_valor != valor: 
                # Valor puede ser None porque es la primera vez que se muestran
                # todos los datos y en ese caso no debe colorear.
                cell.set_property("foreground", "dark green")
                if not model.iter_parent(itr):
                    cell.set_property("weight", 4000)
                    cell.set_property("background", "gray")
                else:
                    cell.set_property("weight", 400)
                    cell.set_property("background", "yellow")
            else: # Coloreado de valores +/-
                if not model.iter_parent(itr):
                    if valor_numerico != None:
                        if valor_numerico == 0:
                            color_valor = "white"
                        elif valor_numerico < 0:
                            color_valor = "red"
                        else:
                            color_valor = "blue"
                    else:
                        color_valor = "white"
                    cell.set_property("foreground", color_valor)
                    cell.set_property("weight", 4000)
                    cell.set_property("background", "gray")
                else:
                    if valor_numerico != None:
                        if valor_numerico == 0:
                            color_valor = None
                        elif valor_numerico < 0:
                            color_valor = "red"
                        else:
                            color_valor = "blue"
                    else:
                        color_valor = "white"
                    cell.set_property("foreground", color_valor)
                    cell.set_property("weight", 400)
                    # Si no ha cambiado y no es una fila "cabecera", entonces 
                    # coloreo el fondo según la gradación de datos reales.
                    cell.set_property("background", bg_color)
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
            mes = (self.mes_actual + indexcol - 1) % 12 #self.num_meses
            model = tv.get_model()
            valor = model[path][indexcol]
            if utils._float(valor) == 0:
                return
            concepto = pclases.getObjetoPUID(model[path][-1])
            if not isinstance(concepto, pclases.PresupuestoAnual):
                # Los resúmenes no los muestro, que vayan al detalle. 
                concepto_desc = concepto.descripcion
                txt_inspect = "%s (%s): %s = \n" % (
                            concepto_desc, col.get_property("title"), valor)
                resultados = []
                for o, importe, tm in self.tracking[mes][concepto]:
                    resultados.append((o.puid, o.get_info(), importe, tm))
                to_open = utils.dialogo_resultado(resultados, 
                        titulo = "INSPECCIONAR VALOR «%s»" % valor, 
                        padre = self.wids['ventana'], 
                        cabeceras = ['Cód. interno', 'Descripción', 
                                     'Importe', 'Toneladas'], 
                        texto = txt_inspect)
                if to_open > 0:
                    objeto = pclases.getObjetoPUID(to_open)
                    if isinstance(objeto, (pclases.ServicioTomado, 
                                          pclases.LineaDeCompra)):
                        if objeto.facturaCompra:
                            from formularios import facturas_compra
                            v = facturas_compra.FacturasDeEntrada(  # @UnusedVariable
                                    objeto = objeto.facturaCompra, 
                                    usuario = self.usuario)
                        elif objeto.albaranEntrada:
                            from formularios import albaranes_de_entrada
                            v = albaranes_de_entrada.AlbaranesDeEntrada(  # @UnusedVariable
                                    objeto = objeto.albaranEntrada, 
                                    usuario = self.usuario)
                    elif isinstance(objeto, (pclases.Servicio, 
                                             pclases.LineaDeVenta)): 
                        if objeto.facturaVenta:
                            from formularios import facturas_venta
                            v = facturas_venta.FacturasVenta(  # @UnusedVariable
                                    objeto = objeto.facturaVenta, 
                                    usuario = self.usuario)
                        elif objeto.prefactura:
                            from formularios import prefacturas
                            v = prefacturas.Prefacturas(  # @UnusedVariable
                                    objeto = objeto.prefactura, 
                                    usuario = self.usuario)
                        elif objeto.albaranSalida:
                            from formularios import albaranes_de_salida
                            v = albaranes_de_salida.AlbaranesDeSalida(  # @UnusedVariable
                                    objeto = objeto.albaranSalida, 
                                    usuario = self.usuario)
                    elif isinstance(objeto, pclases.FacturaVenta):
                        from formularios import facturas_venta  # @Reimport
                        v = facturas_venta.FacturasVenta(  # @UnusedVariable
                                objeto = objeto, 
                                usuario = self.usuario)
                    elif isinstance(objeto, pclases.FacturaCompra):
                        from formularios import facturas_compra  # @Reimport
                        v = facturas_compra.FacturasDeEntrada(  # @UnusedVariable
                                objeto = objeto, 
                                usuario = self.usuario)
                    elif isinstance(objeto, 
                            pclases.VencimientoValorPresupuestoAnual):
                        from formularios import presupuestos
                        v = presupuestos.Presupuestos(  # @UnusedVariable
                                objeto = objeto, 
                                usuario = self.usuario)
                # PORASQUI: El get_info() no es buena idea. Demasiado "técnico"

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
        if self.wids['ch_datos_reales'].get_active():
            self.precalc = precalcular(self.fecha_mes_actual, 
                                       self.fecha_mes_final, 
                                       self.wids['ventana'])
        else:
            self.precalc = MyMonthsDict()
        self.rellenar_widgets()
        self.wids['tv_datos'].expand_all()

    def rellenar_widgets(self):
        # Los únicos otros dos widgets son los de mes de inicio y ancho de 
        # tabla en meses, que ya se rellenan ellos solos.
        self.costes = 0.0
        self.ingresos = 0.0
        padres = self.rellenar_tabla()
        self.actualizar_totales(padres)
        self.wids['e_costes'].set_text(utils.float2str(self.costes))
        self.wids['e_ingresos'].set_text(utils.float2str(self.ingresos))
        total = self.ingresos + self.costes
        self.wids['e_total'].set_text(utils.float2str(total))
        self.wids['e_total'].modify_text(gtk.STATE_NORMAL, 
                self.wids['e_total'].get_colormap().alloc_color(
                    total > 0 and "blue" 
                    or total < 0 and "red" 
                    or "green"))
        self.wids['e_total'].modify_font(pango.FontDescription("bold"))

    def actualizar_totales(self, padres):
        """
        Recorre los nodos de primer nivel y actualiza los totales en 
        función del tipo de importe: gasto o ingreso.
        """
        # Solo hay un (concepto de) presupuesto anual de tipo ingreso: ventas.
        for concepto in padres:
            fila = self.wids['tv_datos'].get_model()[padres[concepto]]
            for valor in fila:
                try:
                    valor_float = utils._float(valor)
                except (ValueError, TypeError):     # Es el PUID o descripción.
                    continue
                if concepto.es_gasto():
                    self.costes += valor_float
                else:
                    self.ingresos += valor_float

    def rellenar_tabla(self):
        self.tracking = {} # Aquí guardaré los objetos que componen cada valor.
        self.cave = {}
        # Por si acaso, algo de mantenimiento por aquí. Al turrón: 
        if pclases.DEBUG:
            print __file__, "Eliminando posibles vencimientos de presupuesto"\
                            " duplicados...", 
            deleted = pclases.VencimientoValorPresupuestoAnual._remove_dupes()
        if pclases.DEBUG:
            print deleted
        # Y ahora sí que sí. Al lío:  
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        model = self.wids['tv_datos'].get_model()
        self.old_model = bak_model(model)
        model.clear()
        padres = self.cargar_conceptos_primer_nivel(vpro)
        filas = self.cargar_conceptos_segundo_nivel(vpro)
        if self.wids['ch_presupuesto'].get_active():
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
        vpro.ocultar()
        return padres

    def mostrar_valores_reales_precalculados(self, 
                                             nodos_conceptos, 
                                             padres, 
                                             vpro):
        for mescol in range(self.num_meses):
            fechacol = restar_mes(self.fecha_mes_actual, -mescol)
            i = 0.0
            try:
                datos_reales = self.precalc[fechacol]
            except KeyError:    # Lo no nay ;)
                datos_reales = []
            for concepto in datos_reales:
                vpro.set_valor(
                        i / len(datos_reales.keys()),
                        "Aplicando sustitución por valores reales en %s..." 
                            % fechacol.strftime("%B"))
                # Si había un valor previo, tengo que retirar la estimación 
                # y sumar lo real. En caso de granza, entonces la parte 
                # proporcional de las Tm.
                valor_real_importe = datos_reales[concepto]['importe']
                objetos = datos_reales[concepto]['objetos']
                if self.wids['ch_presupuesto'].get_active():
                    vto_presupuestado = buscar_vencimiento_presupuestado(
                                                        fechacol, 
                                                        concepto,
                                                        self.fecha_mes_actual)
                else:
                    vto_presupuestado = None
                if criterio_sustitucion(vto_presupuestado, 
                                        valor_real_importe, 
                                        self.fecha_mes_actual, 
                                        fechacol):
                    # Y si no, dejo lo que estaba.
                    if pclases.DEBUG:
                        print __file__, "Cambio presupuesto por real:", \
                                concepto.descripcion,\
                                vto_presupuestado, valor_real_importe
                    diff = self.cambiar_valor_presupuestado(valor_real_importe, 
                                                            vto_presupuestado,
                                                            concepto, 
                                                            fechacol, 
                                                            mescol, 
                                                            nodos_conceptos, 
                                                            objetos)
                    try:
                        self.cave[concepto.puid][mescol+1]+=valor_real_importe
                    except AttributeError:  # No valor real
                        # self.cave[concepto.puid][mescol + 1] = 0
                        pass
                    self.actualizar_sumatorio_padre(mescol, concepto, padres, 
                                                    diff)
                i += 1

    def cambiar_valor_presupuestado(self, valor_real_importe, 
                                    valor_presupuestado, concepto, fechacol, 
                                    mescol, nodos_conceptos, objetos):
        """
        Si el valor presupuestado es de granza, quita el importe 
        correspondiente a las toneladas del valor real y suma este valor 
        real a lo que quede. Deja en el cell la cantidad final.
        Devuelve la diferencia entre el nuevo valor y el que había antes 
        para que se actualice el nodo padre únicamente sumando esa cantidad y 
        así evitar recalcular toda la "subcolumna".
        «objetos» es una lista de objetos de los que procede el valor real.
        """
        (valor_presupuestado_restante, 
         valor_presupuestado_importe) = self.calcular_presupuestado_restante(
                                                        valor_presupuestado, 
                                                        fechacol, 
                                                        concepto)
        model = self.wids['tv_datos'].get_model()
        nodo_concepto = nodos_conceptos[concepto]
        if self.wids['ch_datos_pdtes'].get_active():
            # Si los valores confirmados los ignoro, simplemente no incremento 
            # el valor total de la celda, pero sí que decremento el 
            # presupuesto. El IVA no cuenta. Eso se paga estén o no las 
            # facturas pendientes.
            for objeto in objetos[:]:
                if (not esta_pendiente(objeto) 
                        and (valor_presupuestado 
                             and not valor_presupuestado.es_de_iva())):
                    try:
                        importe_confirmado = objeto.get_subtotal(iva = True, 
                                                            prorrateado = True)
                    except AttributeError:  # Es factura o algo asín
                        importe_confirmado = objeto.calcular_importe_total()
                    if concepto.es_gasto:
                        importe_confirmado *= -1
                    valor_real_importe -= importe_confirmado
                    objetos.remove(objeto)
        model[nodo_concepto][mescol + 1] = utils.float2str(
                                                valor_presupuestado_restante 
                                                + valor_real_importe)
        self.actualizar_traza(objetos, concepto, fechacol, valor_presupuestado)
        delta = ((valor_presupuestado_restante + valor_real_importe) 
                 - valor_presupuestado_importe)
        if pclases.DEBUG:
            print __file__, ">>> cambiar_valor_presupuestado >>> ð =", delta
        return delta

    def actualizar_traza(self, objetos, concepto, fechacol, 
                         valor_presupuestado):
        if not fechacol.month in self.tracking:
            self.tracking[fechacol.month] = defaultdict(list) 
        for o in objetos:
            if (isinstance(o, pclases.LineaDeCompra) 
                    and o.productoCompra in buscar_productos_granza()):
                importe_objeto = o.get_subtotal(iva = True, prorrateado=True)
                try:
                    numvtos = len(o.facturaCompra.vencimientosPago)
                except AttributeError:
                    numvtos = max(
                        len(o.albaranEntrada.proveedor.get_vencimientos()), 1)
                tm = o.cantidad / numvtos
                if concepto.es_gasto():
                    trinfo = (o, -importe_objeto, -tm)
                else:
                    trinfo = (o, importe_objeto, tm)
                restar_en_traza_presupuesto(self.tracking, 
                                            fechacol.month, 
                                            self.mes_actual, 
                                            concepto, 
                                            valor_presupuestado, 
                                            importe_objeto,
                                            tm)
            else:
                try:
                    importe_objeto = o.get_subtotal(iva = True, 
                                                    prorrateado = True)
                    if isinstance(o, (pclases.LineaDeCompra, 
                                      pclases.ServicioTomado)):
                        importe_objeto = -importe_objeto
                except AttributeError: # Es factura o algo así.
                    importe_objeto = o.calcular_importe_total(iva = True)
                    if isinstance(o, pclases.FacturaCompra):
                    # IVA es gasto, pero tiene fras de venta que deben ir en 
                    # positivo. No puedo usar el criterio concepto.es_gasto().
                        importe_objeto = -importe_objeto
                trinfo = (o, importe_objeto, None)
                restar_en_traza_presupuesto(self.tracking, 
                                            fechacol.month, 
                                            self.mes_actual, 
                                            concepto, 
                                            valor_presupuestado, 
                                            importe_objeto)
            self.tracking[fechacol.month][concepto].append(trinfo)

    def calcular_presupuestado_restante(self, valor_presupuestado, fechacol, 
                                        concepto):
        valor_real_toneladas = None
        if valor_presupuestado:
            valor_presupuestado_importe = valor_presupuestado.importe
            if valor_presupuestado.es_de_granza():
                precalc_concepto = self.precalc[fechacol][concepto]
                valor_real_toneladas = precalc_concepto['toneladas']
                valor_presupuestado_restante = (valor_presupuestado.precio 
                    #* (valor_presupuestado.toneladas - valor_real_toneladas))
                    # Sumo porque las tm presupuestadas ya vienen en negativo. 
                    * (valor_presupuestado.toneladas + valor_real_toneladas))
                # Si "me como" todo lo presupuestado, parto de cero para 
                # mostrar el valor real completo. (Si no, acabará restando
                # ese delta y falseará el resultado)
                # Uso min porque las toneladas vienen en negativo al ser gasto.
                valor_presupuestado_restante = min(0, 
                                                valor_presupuestado_restante)
            else:
                # Como voy a sustituirlo entero, el valor restante es 0.0 para 
                # que solo se vea el valor real que le voy a sumar.
                valor_presupuestado_restante = 0.0
        else:
            valor_presupuestado_restante = 0.0
            valor_presupuestado_importe = 0.0
        return valor_presupuestado_restante, valor_presupuestado_importe

    def actualizar_sumatorio_padre(self, mescol, concepto, padres, diff):
        # Thanks bicycle repair man!
        model = self.wids['tv_datos'].get_model()
        pa = concepto.presupuestoAnual
        nodo_padre = padres[pa]
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
                    ] + [utils.float2str(w) for w in filas[c]] + [c.puid]
            nodos_conceptos[c] = model.append(nodo_padre, fila)
            for mes_matriz in range(1, self.num_meses + 1):
                # Actualizo totales de fila padre
                try:
                    model[nodo_padre][mes_matriz] = utils.float2str(
                            utils.parse_float(model[nodo_padre][mes_matriz]) 
                            + utils.parse_float(fila[mes_matriz]))
                except (TypeError, ValueError):
                    model[nodo_padre][mes_matriz] = utils.float2str(
                            fila[mes_matriz])
            i += 1
        return nodos_conceptos 

    def montar_filas(self, filas, vpro):
        i = 0.0
        # Estos valores se metieron en la fecha y concepto que fueran, pero 
        # aquí tienen que moverse a la fecha de la FDP que corresponda al 
        # concepto. 
        valores = pclases.VencimientoValorPresupuestoAnual.select(pclases.AND(
            pclases.VencimientoValorPresupuestoAnual.q.fecha
                >= self.fecha_mes_actual, 
            pclases.VencimientoValorPresupuestoAnual.q.fecha
                < self.fecha_mes_final)) 
        valores_count = valores.count()
        for v in valores:
            v.sync()
            # CWT: En mes actual no valen valores presupuestados. Solo reales. 
            if (self.wids['ch_reales_mes0'].get_active() and 
                self.fecha_mes_actual 
                    <= v.fecha <= final_de_mes(self.fecha_mes_actual)):
                continue
            # Hay valores de meses anteriores al primero de la tabla cuyos 
            # vencimientos caen ahora. Esos los quito. Si el mes en que se 
            # presupuestaron ya se ha ido, sus vencimientos no valen.
            vp = v.valorPresupuestoAnual
            if vp.fecha < self.fecha_mes_actual:
                continue
            c = v.conceptoPresupuestoAnual
            mes_offset = (v.fecha.month - self.fecha_mes_actual.month) % (
                                                                self.num_meses)
            try:
                filas[c][mes_offset] += v.importe
            except KeyError:    # Que será lo normal. No debería haber dos vtos. 
                                # en la misma fecha para un mismo concepto.
                filas[c][mes_offset] = v.importe
            if not v.fecha.month in self.tracking:
                self.tracking[v.fecha.month] = defaultdict(list) 
            try:
                tm = v.toneladas
            except ValueError:
                tm = None
            self.tracking[v.fecha.month][c].append(
                    (v, v.importe, tm))
            vpro.set_valor(i / valores_count, 
                           "Cargando valores de dynconsulta...") 
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
            self.cave[pa.puid] = defaultdict(old_float)
            fila = [pa.descripcion] #FIXME: .replace("&", "&amp;")]
            for m in range(self.num_meses):  # @UnusedVariable
                fila.append("")
            fila.append(pa.puid)
            nodo = model.append(None, fila) 
            padres[pa] = nodo 
            vpro.set_valor(i / pas_count, 
                           "Cargando conceptos de primer nivel...") 
            i += 1
        return padres

    def cargar_conceptos_segundo_nivel(self, vpro):
        """
        Solo carga los conceptos. Con todos los valores a cero.
        """
        i = 0.0
        conceptos = pclases.ConceptoPresupuestoAnual.select()
        conceptos_count = conceptos.count()
        filas = {}
        for c in conceptos:
            self.cave[c.puid] = defaultdict(old_float)
            filas[c] = []
            for m in range(self.num_meses):  # @UnusedVariable
                filas[c].append(0)
            vpro.set_valor(i / conceptos_count, 
                           "Cargando conceptos de dynconsulta...") 
            i += 1
        return filas

    def buscar(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        # TODO: Buscar dentro de todas las filas y tracking un texto tecleado 
        #       y pasarle el foco o algo.
        pass

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe.
        """
        resp = utils.dialogo(titulo = "¿IMPRIMIR DESGLOSE?", 
                texto = "Puede imprimir un resumen o todo el contenido de "
                        "la consulta\n¿Desea imprimir toda la información "
                        "desglosada?", 
                padre = self.wids['ventana'])
        if resp:
            tv = self.wids['tv_datos']
            tv.expand_all()
            while gtk.events_pending(): gtk.main_iteration(False)
            cols_a_totalizar = []
        else:
            tv = self.wids['tv_datos']
            tv.collapse_all()
            while gtk.events_pending(): gtk.main_iteration(False)
            from consulta_ventas_por_producto import convertir_a_listview
            tv = convertir_a_listview(tv)
            cols_a_totalizar = range(1, self.num_meses + 1)
        strfecha = "De %s a %s" % (utils.str_fecha(self.fecha_mes_actual), 
                utils.str_fecha(self.fecha_mes_final - mx.DateTime.oneDay))
        abrir_pdf(
                treeview2pdf(tv, titulo = "Informe resumen financiero", 
                             fecha = strfecha, apaisado = True, 
                             numcols_a_totalizar = cols_a_totalizar))

    def exportar(self, boton):
        """
        Exporta el TreeView a CSV.
        """
        abrir_csv(treeview2csv(self.wids['tv_datos']))


def precalcular(fecha_ini, fecha_fin, ventana_padre = None, usuario = None):
    """
    Devuelve un diccionario de conceptos del mes especificado con los valores
    que se puedan calcular a partir de datos reales.
    Si el concepto no existe, lo crea en la base de datos
    cobrados / pagados).
    """
    vpro = VentanaActividad(ventana_padre, "Precalculando datos reales...")
    vpro.mostrar()
    # Valores que puedo conocer del ERP (de momento):
    # 1.- Entradas de granza
    res = calcular_entradas_de_granza(vpro, fecha_ini, fecha_fin, usuario)
    # 2.- IVA (soportado - repercutido)
    calcular_iva_real(res, vpro, fecha_ini, fecha_fin)
    # 3.- Ventas por tipo (internacionales, geotextiles, geocompuestos...)
    calcular_ventas(res, vpro, fecha_ini, fecha_fin)
    # 4.- Compras que no son de granza
    calcular_compras_no_granza(res, vpro, fecha_ini, fecha_fin)
    if pclases.DEBUG and pclases.VERBOSE:
        print __file__, res
    vpro.ocultar()
    return res

def calcular_iva_real(res, vpro, fechaini, fechafin):
    """
    Calcula el IVA del mes de la fecha y lo almacena en el concepto 
    «Impuestos» de los valores precalculados.
    """
    vpro.mover()
    concepto = buscar_concepto_iva()
    fecha = fechaini
    while fecha <= fechafin:
        vpro.mover()
        soportado, fras_soportadas = calcular_soportado(vpro, fecha)
        vpro.mover()
        repercutido, fras_repercutidas = calcular_repercutido(vpro, fecha)
        vpro.mover()
        importe_iva = soportado - repercutido
        if importe_iva:
            # Paso de guardar valores nulos. La RAM es un bien escaso!
            if fecha not in res:
                res[fecha] = {}
            try:
                res[fecha][concepto]['importe'] += importe_iva 
                res[fecha][concepto]['objetos'] += fras_soportadas 
                res[fecha][concepto]['objetos'] += fras_repercutidas
            except KeyError:
                res[fecha][concepto] = {'importe': importe_iva, 
                        'objetos': fras_soportadas + fras_repercutidas}
        # IVA a devolver se compensa el mes siguiente.
        try:
            importe_este_mes = res[fecha][concepto]['importe']
        except KeyError:
            importe_este_mes = None
        if importe_este_mes > 0 and restar_mes(fecha, -1) < fechafin: 
            # El último mes ya no arrastro, no me quedan celdas donde acumular. 
            fechanext = restar_mes(fecha, -1)
            if fechanext not in res:
                res[fechanext] = {}
            try:
                res[fechanext][concepto]['importe'] += importe_este_mes
                res[fechanext][concepto]['objetos'] \
                        = res[fecha][concepto]['objetos']
            except KeyError:
                res[fechanext][concepto] = {'importe': importe_este_mes, 
                        'objetos': res[fecha][concepto]['objetos']} 
            res[fecha][concepto]['importe'] -= importe_este_mes # = 0.0
            res[fecha][concepto]['objetos'] = []
        fecha = restar_mes(fecha, -1)
    # FIXME: Devuelvo en negativo o positivo, pero el resto de cifras (ventas, 
    # compras, salarios, etc.) va en positivo aunque sean gastos. Convertir a  
    # negativo automáticamente aquí y en presupuesto si es de tipo gasto.

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
    return iva, pclases.SQLlist(frascompra)

def calcular_repercutido(vpro, fecha):
    # Pago este mes el IVA del mes pasado. Ojo.
    fini = restar_mes(fecha)
    fini = mx.DateTime.DateTimeFrom(fini.year, fini.month, 1)
    ffin = mx.DateTime.DateTimeFrom(fini.year, fini.month, -1)
    frasventa = pclases.FacturaVenta.select(pclases.AND(
        pclases.FacturaVenta.q.fecha >= fini, 
        pclases.FacturaVenta.q.fecha <= ffin))
    iva = sum([f.calcular_total_iva() for f in frasventa])
    return iva, pclases.SQLlist(frasventa)

def calcular_ventas(res, vpro, fechaini, fechafin):
    """
    Calcula y clasifica las ventas realizadas entre las fechas de inicio y 
    fin.
    """
    vpro.mover()
    fecha = fechaini
    while fecha <= fechafin:
        vpro.mover()
        ldv_vencimientos_ventas, srv_vencimientos_ventas \
                = buscar_vencimientos_ventas(vpro, fecha)
        vpro.mover()
        lineas_no_facturadas, servicios_no_facturados \
                = buscar_lineas_albaranes_venta(vpro, fecha)
        vpro.mover()
        clasificar_ventas(res, ldv_vencimientos_ventas, 
                          srv_vencimientos_ventas, lineas_no_facturadas, 
                          servicios_no_facturados, fecha, vpro)
        fecha = restar_mes(fecha, -1)

def buscar_vencimientos_ventas(vpro, fecha):
    """
    Devuelve líneas de venta y servicios correspondientes a vencimientos de 
    facturas en el mes indicado por «fecha».
    """
    fini = primero_de_mes(fecha)
    ffin = final_de_mes(fecha)
    vtos_venta = pclases.VencimientoCobro.select(pclases.AND(
        pclases.VencimientoCobro.q.fecha >= fini, 
        pclases.VencimientoCobro.q.fecha <= ffin))
    ldvs = []
    srvs = []
    for v in vtos_venta:
        vpro.mover()
        f = v.factura
        for ldv in f.lineasDeVenta:
            if ldv not in ldvs:
                ldvs.append(ldv)
            vpro.mover()
        for srv in f.servicios:
            if srv not in srvs:
                srvs.append(srv)
            vpro.mover()
    return ldvs, srvs

def buscar_lineas_albaranes_venta(vpro, fecha):
    """
    Devuelve las líneas de venta correspondientes a albaranes no facturados 
    del mes indicado por la fecha «fecha».
    """
    fini = primero_de_mes(fecha)
    ffin = final_de_mes(fecha)
    albs = pclases.AlbaranSalida.select(pclases.AND(
        pclases.AlbaranSalida.q.fecha >= fini, 
        pclases.AlbaranSalida.q.fecha <= ffin))
    # Filtro y me quedo con las líneas no facturadas
    ldvs = []
    srvs = []
    for a in albs:
        vpro.mover()
        for ldv in a.lineasDeVenta:
            vpro.mover()
            if not ldv.factura:
                ldvs.append(ldv)
        for srv in a.servicios:
            vpro.mover()
            if not srv.factura:
                srvs.append(srv)
    return ldvs, srvs

def clasificar_ventas(res, ldv_facturadas, srv_facturados, ldv_no_facturadas, 
                      srv_no_facturados, fecha, vpro):
    """
    De los dos grupos de líneas de venta recibidos determina su importe, fecha 
    de vencimiento y concepto donde clasificarlas. Incrementa la celda* de la 
    columna de fecha de vencimiento y fila del concepto en la cantidad del 
    importe de la línea de venta. Si tiene varios vencimientos, prorratea la 
    cantidad.
    * En realidad el importe real en el diccionario de la celda que ocupará si 
    supera el criterio de sustitución.
    """
    for ldv in ldv_facturadas:
        vpro.mover()
        importe_prorrateado_ldv = ldv.get_subtotal(iva = True, 
                                                   prorrateado = True)
        concepto = buscar_concepto_ldv(ldv.factura.cliente, ldv.producto)
        if not fecha in res:
            res[fecha] = {}
        try:
            res[fecha][concepto]['importe'] += importe_prorrateado_ldv
            res[fecha][concepto]['objetos'].append(ldv)
        except KeyError:
            res[fecha][concepto] = {'importe': importe_prorrateado_ldv, 
                                    'objetos': [ldv]}
    for srv in srv_facturados:
        vpro.mover()
        importe_prorrateado_srv = srv.get_subtotal(iva = True, 
                                                   prorrateado = True)
        concepto = buscar_concepto_ldv(srv.factura.cliente, None)
        if not fecha in res:
            res[fecha] = {}
        try:
            res[fecha][concepto]['importe'] += importe_prorrateado_srv
            res[fecha][concepto]['objetos'].append(srv)
        except KeyError:
            res[fecha][concepto] = {'importe': importe_prorrateado_srv, 
                                    'objetos': [srv]}
    for ldv in ldv_no_facturadas:
        # En este caso la fecha no es la fecha de vencimiento, sino la del 
        # albarán. Así que necesito determinar cuándo vence según el 
        # cliente.
        vpro.mover()
        importe_prorrateado_ldv = ldv.get_subtotal(iva = True, 
                                                   prorrateado = True)
        concepto = buscar_concepto_ldv(ldv.albaranSalida.cliente, ldv.producto)
        fechas = ldv.albaranSalida.cliente.get_fechas_vtos_por_defecto(
                                                    ldv.albaranSalida.fecha)
        if not fechas:
            fechas = [fecha]    # Uso la del albarán porque el cliente no 
                                # tiene información suficiente.
        for fecha in fechas:
            if not fecha in res:
                res[fecha] = {}
            try:
                res[fecha][concepto]['importe'] += importe_prorrateado_ldv
                res[fecha][concepto]['objetos'].append(ldv)
            except KeyError:
                res[fecha][concepto] = {'importe': importe_prorrateado_ldv, 
                                        'objetos': [ldv]}
    for srv in srv_no_facturados:
        # En este caso la fecha no es la fecha de vencimiento, sino la del 
        # albarán. Así que necesito determinar cuándo vence según el 
        # cliente.
        vpro.mover()
        importe_prorrateado_srv = srv.get_subtotal(iva = True, 
                                                   prorrateado = True)
        concepto = buscar_concepto_ldv(srv.albaranSalida.cliente, None)
        fechas = srv.albaranSalida.cliente.get_fechas_vtos_por_defecto(
                                                    srv.albaranSalida.fecha)
        if not fechas:
            fechas = [fecha]    # Uso la del albarán porque el cliente no 
                                # tiene información suficiente.
        for fecha in fechas:
            if not fecha in res:
                res[fecha] = {}
            try:
                res[fecha][concepto]['importe'] += importe_prorrateado_srv
                res[fecha][concepto]['objetos'].append(srv)
            except KeyError:
                res[fecha][concepto] = {'importe': importe_prorrateado_srv, 
                                        'objetos': [srv]}

def buscar_concepto_ldv(cliente, producto = None):
    """
    Devuelve el concepto de presupuesto que corresponde al cliente y 
    producto recibido. Si no se recibe producto se considera que es un 
    servicio y devuelve el tipo de concepto "General".
    """
    # Concepto por defecto, el del cliente.
    if cliente.es_extranjero():
        nac = "Internacionales"
    else:
        nac = "Nacionales"
    try:
        tdp = cliente.tipoDeCliente.descripcion
    except AttributeError: # No está clasificado por los usuarios. Uso general.
        tdp = "General"
    # Ahora afino en función del tipo de producto de la línea de venta. 
    try:
        if producto.es_fibra():
            tdp = "Fibra"
        elif producto.es_bigbag() or producto.es_bolsa() or producto.es_caja():
            tdp = "Geocem"
        elif isinstance(producto, pclases.ProductoCompra):
            tdp = "Comercializado"
    except AttributeError:
        pass
    try:
        concepto = pclases.ConceptoPresupuestoAnual.selectBy(
                descripcion = "%s - %s" % (nac, tdp))[0]
    except IndexError:
        # No existe el concepto. DEBERÍA. Lo creo.
        concepto = pclases.ConceptoPresupuestoAnual(
                descripcion = "%s - %s" % (nac, tdp), 
                presupuestoAnual = pclases.PresupuestoAnual.selectBy(
                    descripcion = "Clientes")[0], 
                proveedor = None)
    return concepto

def calcular_compras_no_granza(res, vpro, fechaini, fechafin):
    """
    Calcula y clasifica las compras realizadas entre las fechas de inicio y 
    fin.
    """
    vpro.mover()
    fecha = fechaini
    granzas = buscar_productos_granza()
    while fecha <= fechafin:
        vpro.mover()
        ldc_vencimientos_compras, srv_vencimientos_compras \
            = buscar_vencimientos_compras_no_granza(vpro, fecha, granzas)
        vpro.mover()
        lineas_no_facturadas, servicios_no_facturados \
            = buscar_lineas_albaranes_compra_no_granza(vpro, fecha, granzas)
        vpro.mover()
        clasificar_compras(res, ldc_vencimientos_compras, 
                          srv_vencimientos_compras, lineas_no_facturadas, 
                          servicios_no_facturados, fecha, vpro)
        fecha = restar_mes(fecha, -1)

def buscar_vencimientos_compras_no_granza(vpro, fecha, granzas):
    """
    Devuelve líneas de compra y servicios correspondientes a vencimientos de 
    facturas en el mes indicado por «fecha» que no sean de granza.
    """
    fini = primero_de_mes(fecha)
    ffin = final_de_mes(fecha)
    vtos_compra = pclases.VencimientoPago.select(pclases.AND(
        pclases.VencimientoPago.q.fecha >= fini, 
        pclases.VencimientoPago.q.fecha <= ffin))
    ldcs = []
    srvs = []
    for v in vtos_compra:
        vpro.mover()
        f = v.facturaCompra
        for ldc in f.lineasDeCompra:
            if ldc.productoCompra not in granzas and ldc not in ldcs:
                ldcs.append(ldc)
            vpro.mover()
        for srv in f.serviciosTomados:
            if srv not in srvs:
                srvs.append(srv)
            vpro.mover()
    return ldcs, srvs

def buscar_lineas_albaranes_compra_no_granza(vpro, fecha, granzas):
    """
    Devuelve las líneas de compra correspondientes a albaranes no facturados 
    del mes indicado por la fecha «fecha» que no sean de granza.
    """
    fini = primero_de_mes(fecha)
    ffin = final_de_mes(fecha)
    albs = pclases.AlbaranEntrada.select(pclases.AND(
        pclases.AlbaranEntrada.q.fecha >= fini, 
        pclases.AlbaranEntrada.q.fecha <= ffin))
    # Filtro y me quedo con las líneas no facturadas y que no sean de granza.
    ldcs = []
    srvs = []
    for a in albs:
        vpro.mover()
        for ldc in a.lineasDeCompra:
            vpro.mover()
            if not ldc.facturaCompra and ldc.productoCompra not in granzas:
                ldcs.append(ldc)
        #for srv in a.serviciosTomados:
        #    vpro.mover()
        #    if not srv.factura:
        #        srvs.append(srv)
        # Los albaranes de entrada no tienen servicios. Los servicios se 
        # facturan directamente.
    return ldcs, srvs

def clasificar_compras(res, ldc_facturadas, srv_facturados, ldc_no_facturadas, 
                      srv_no_facturados, fecha, vpro):
    """
    De los dos grupos de líneas de compra recibidos determina su importe, fecha 
    de vencimiento y concepto donde clasificarlas. Incrementa la celda* de la 
    columna de fecha de vencimiento y fila del concepto en la cantidad del 
    importe de la línea de venta. Si tiene varios vencimientos, prorratea la 
    cantidad.
    * En realidad el importe real en el diccionario de la celda que ocupará si 
    supera el criterio de sustitución.
    """
    for ldc in ldc_facturadas:
        vpro.mover()
        # Gasto. En negativo.
        importe_prorrateado_ldc = -ldc.get_subtotal(iva = True, 
                                                    prorrateado = True)
        concepto = buscar_concepto_ldc(ldc.facturaCompra.proveedor, 
                                       ldc.productoCompra)
        if not fecha in res:
            res[fecha] = {}
        try:
            res[fecha][concepto]['importe'] += importe_prorrateado_ldc
            res[fecha][concepto]['objetos'].append(ldc)
        except KeyError:
            res[fecha][concepto] = {'importe': importe_prorrateado_ldc, 
                                    'objetos': [ldc]}
    for srv in srv_facturados:
        vpro.mover()
        # Gasto. Negativo
        importe_prorrateado_srv = -srv.get_subtotal(iva = True, 
                                                    prorrateado = True)
        concepto = buscar_concepto_ldc(srv.facturaCompra.proveedor, None)
        if not fecha in res:
            res[fecha] = {}
        try:
            res[fecha][concepto]['importe'] += importe_prorrateado_srv
            res[fecha][concepto]['objetos'].append(srv)
        except KeyError:
            res[fecha][concepto] = {'importe': importe_prorrateado_srv, 
                                    'objetos': [srv]}
    for ldc in ldc_no_facturadas:
        # En este caso la fecha no es la fecha de vencimiento, sino la del 
        # albarán. Así que necesito determinar cuándo vence según el 
        # proveedor.
        vpro.mover()
        # Gasto. En negativo
        importe_prorrateado_ldc = -ldc.get_subtotal(iva = True, 
                                                    prorrateado = True)
        concepto = buscar_concepto_ldc(ldc.albaranEntrada.proveedor, 
                                       ldc.productoCompra)
        try:
            fechas = ldc.albaranEntrada.proveedor.get_fechas_vtos_por_defecto(
                                                    ldc.albaranEntrada.fecha)
        except AttributeError:  # No proveedor. Sí albarán. El objeto viene 
                                # de una búsqueda de albaranes no facturados.
            fechas = [] # fecha es similar a ldc.albaranEntrada.fecha
        if not fechas:
            fechas = [fecha]    # Uso la del albarán porque el proveedor no 
                                # tiene información suficiente.
        for fecha in fechas:
            if not fecha in res:
                res[fecha] = {}
            try:
                res[fecha][concepto]['importe'] += importe_prorrateado_ldc
                res[fecha][concepto]['objetos'].append(ldc)
            except KeyError:
                res[fecha][concepto] = {'importe': importe_prorrateado_ldc, 
                                        'objetos': [ldc]}
    for srv in srv_no_facturados:
        # En este caso la fecha no es la fecha de vencimiento, sino la del 
        # albarán. Así que necesito determinar cuándo vence según el 
        # proveedor.
        vpro.mover()
        # Gasto. En negativo
        importe_prorrateado_srv = -srv.get_subtotal(iva = True, 
                                                    prorrateado = True)
        concepto = buscar_concepto_ldc(srv.albaranEntrada.proveedor, None)
        fechas = srv.albaranEntrada.proveedor.get_fechas_vtos_por_defecto(
                                                    srv.albaranEntrada.fecha)
        if not fechas:
            fechas = [fecha]    # Uso la del albarán porque el proveedor no 
                                # tiene información suficiente.
        for fecha in fechas:
            if not fecha in res:
                res[fecha] = {}
            try:
                res[fecha][concepto]['importe'] += importe_prorrateado_srv
                res[fecha][concepto]['objetos'].append(srv)
            except KeyError:
                res[fecha][concepto] = {'importe': importe_prorrateado_srv, 
                                        'objetos': [srv]}

def buscar_concepto_ldc(proveedor, producto = None):
    """
    Devuelve el concepto de presupuesto que corresponde al proveedor y 
    producto recibido. Si no se recibe producto se considera que es un 
    servicio y devuelve el tipo de concepto "General".
    """
    # Concepto por defecto, el del proveedor.
    try:
        proveedor.sync()
        tdp = proveedor.tipoDeProveedor.descripcion
    except AttributeError: # No está clasificado por los usuarios. Uso resto.
        tdp = "Resto"
    if tdp == "Granza":     # Si por la ldc no puedo sacar el tipo, entonces 
        tdp = "Resto"       # lo clasifico como general. Porque todas las 
                            # compras de granza ya se tratan en otro sitio. 
    # Ahora afino en función del tipo de producto de la línea de venta. 
    if producto:
        producto.sync()
        tdm = producto.tipoDeMaterial
        # OJO: HARCODED. Tipos de material conocidos. Si se crearan nuevos, 
        # caería en el tipo del proveedor.
        iny = {'Materia Prima': None,   # Usaré el del proveedor. 
               'Material adicional': 'Materiales', 
               'Mantenimiento': 'Materiales', 
               'Repuestos geotextiles': 'Repuestos', 
               'Repuestos fibra': 'Repuestos', 
               'Aceites y lubricantes': 'Materiales', 
               'Mercancía inicial Valdemoro': 'Comercializados', 
               'Productos comercializados': 'Comercializados', 
               'Comercializados': 'Comercializados'}
        try:
            tdpiny = iny[tdm]
        except KeyError:
            pass    # Si no está o no tiene, uso el del proveedor.
        else:
            if tdpiny != None:
                tdp = tdpiny
    try:
        concepto = pclases.ConceptoPresupuestoAnual.selectBy(
                                                        descripcion = tdp)[0]
    except IndexError:
        # No existe el concepto. DEBERÍA. Lo creo.
        if proveedor.es_extranjero():
            nac = "Internacionales"
        else:
            nac = "Nacionales"        
        concepto = pclases.ConceptoPresupuestoAnual(
                descripcion = "%s - %s" % (nac, tdp), 
                presupuestoAnual = pclases.PresupuestoAnual.selectBy(
                    descripcion = "Proveedores")[0], 
                proveedor = None)
    return concepto

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
    res = MyMonthsDict()
    clasificar_vencimientos_compra(vtos, granzas, usuario, res, vpro)
    vpro.mover()
    # Y ahora de los albaranes no facturados.
    albs = buscar_albaranes_de_entrada(primes, finmes)
    vpro.mover()
    # Filtro para quedarme con los de granza:
    clasificar_albaranes_de_entrada(albs, granzas, usuario, res, vpro)
    vpro.mover()
    return res

def clasificar_albaranes_de_entrada(albs, granzas, usuario, res, vpro):
    for a in albs:
        for ldc in a.lineasDeCompra:
            ldc.sync()
            # Solo quiero lo no facturado.
            if (not ldc.facturaCompraID and ldc.productoCompra in granzas
                    and ldc.cantidad):
                # Si la línea no tiene cantidad de nada, paso. No quiero 
                # guardar valores nulos que me coman tiempo de proceso o RAM.
                # Piensa como si siguieras programando con 640 K, old boy.
                if pclases.DEBUG: # and pclases.VERBOSE:
                    print __file__, a.get_info(), ldc.get_info()
                concepto = buscar_concepto_proveedor_granza(ldc.proveedor, 
                                                            usuario)
                proveedor = ldc.albaranEntrada.proveedor
                fechas_vto = proveedor.get_fechas_vtos_por_defecto(
                                                    ldc.albaranEntrada.fecha)
                if not fechas_vto:
                    fechas_vto = [ldc.albaranEntrada.fecha]
                numvtos = len(fechas_vto)
                for fecha_vto in fechas_vto:
                    fecha = primero_de_mes(fecha_vto)
                    if fecha not in res:
                        res[fecha] = {}
                    cantidad_prorrateada = ldc.cantidad / numvtos
                    try:
                        # Gasto. En negativo
                        res[fecha][concepto]['importe'] += -ldc.get_subtotal(
                                                            iva = True,
                                                            prorrateado = True)
                        res[fecha][concepto]['toneladas']+=cantidad_prorrateada
                        res[fecha][concepto]['objetos'].append(ldc)
                    except KeyError:
                        # Gasto. En negativo
                        res[fecha][concepto] = {
                            'importe': -ldc.get_subtotal(iva = True, 
                                                         prorrateado = True), 
                            'toneladas': cantidad_prorrateada, 
                            'objetos': [ldc]}
                vpro.mover()

def buscar_albaranes_de_entrada(primes, finmes):
    # ¡OJO! Si el albarán es de otra fecha anterior a «primes», aunque entren 
    # sus "teóricos" vencimientos en los meses del TreeView, se va a ignorar. 
    # La consulta no lo encontrará.
    albs = pclases.AlbaranEntrada.select(pclases.AND(
        pclases.AlbaranEntrada.q.fecha >= primes, 
        pclases.AlbaranEntrada.q.fecha <= finmes))
    if pclases.DEBUG:
        print __file__, albs.count(), "albaranes encontrados."
    return albs

def clasificar_vencimientos_compra(vtos, granzas, usuario, res, vpro):
    # Me quedo solo con los vencimientos de fras. de compra de granza.
    for v in vtos:
        if pclases.DEBUG and pclases.VERBOSE:
            print __file__, v.get_info(), v.fecha
        fra = v.facturaCompra
        for ldc in fra.lineasDeCompra:
            ldc.sync
            ldc.sync()
            ldc.facturaCompra and ldc.facturaCompra.sync()
            ldc.albaranEntrada and ldc.albaranEntrada.sync()
            if ldc.productoCompra in granzas:
                if pclases.DEBUG and pclases.VERBOSE:
                    print __file__, fra.get_info(), ldc.get_info()
                concepto = buscar_concepto_proveedor_granza(ldc.proveedor, 
                                                            usuario)
                fechas_mes_vto = buscar_mes_vto(ldc.facturaCompra)
                # Gasto. En negativo
                importe = -ldc.get_subtotal(iva = True, prorrateado = True) 
                cantidad = ldc.cantidad / len(fechas_mes_vto)
                #for fecha_mes_vto in fechas_mes_vto:
                fecha_mes_vto = v.fecha
                if fecha_mes_vto not in res:
                    res[fecha_mes_vto] = {}
                try:
                    res[fecha_mes_vto][concepto]['importe'] += importe
                    res[fecha_mes_vto][concepto]['toneladas'] += cantidad
                    res[fecha_mes_vto][concepto]['objetos'].append(ldc)
                except KeyError:
                    res[fecha_mes_vto][concepto] = {'importe': importe, 
                                                    'toneladas': cantidad, 
                                                    'objetos': [ldc]}
            vpro.mover()

def buscar_mes_vto(fra_compra):
    """Devuelve las fechas de vencimiento de la factura. Si no tiene 
    vencimientos (algún usuario se está haciendo el remolón con su trabajo) 
    entonces devuelve la fecha de la factura.
    Las fechas las devuelve a primero del mes que sea, ignorando el día real
    de pago.

    :fra_compra: pclases.FacturaCompra
    :returns: mx.DateTime.Date(Time)

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
                        == "Proveedores granza")[0],  # EXISTE. Hay un check al 
                                            # principio que se asegura de eso.
                proveedor = proveedor)
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

def criterio_sustitucion(vto_presupuesto, valor_real_importe, 
                         fecha_primera_col, fecha = None):
    if not fecha:
        fecha = primero_de_mes(mx.DateTime.today())
    # Si ni siquiera hay valor presupuestado, está claro, ¿no? Mostrar el real:
    sustituir_por_reales = True
    if vto_presupuesto:
        # Para el mes actual SIEMPRE valores reales.
        if primero_de_mes(fecha) <= fecha_primera_col <= final_de_mes(fecha):
            sustituir_por_reales = True
        else:
            sustituir_por_reales = False
            ### Caso granza
            if vto_presupuesto.es_de_granza():
                # DONE: Principio de realidad: Siempre que 
                # haya datos reales, se sustituyen las estimaciones por datos 
                # reales. En granza además se puede hacer de forma 
                # proporcional complementando al presupuesto.
                # Esto significa que si han entrado 15 toneladas de granza, 
                # en el mes de su vencimiento se retiran 15 toneladas al 
                # precio estimado y se pone el importe real de esas 15 
                # toneladas sumadas al resto de estimado. 
                sustituir_por_reales = True
            ### Caso IVA
            if (vto_presupuesto.es_de_iva() 
                    and abs(valor_real_importe)>abs(vto_presupuesto.importe)):
                # En el caso del IVA se muestra el importe calculado a partir 
                # de datos reales cuando sea el mes corriente (primer "if" de 
                # arriba) o cuando se supere la estimación.
                sustituir_por_reales = True
            ### Caso ventas.
            if (vto_presupuesto.es_de_ventas()
                    and valor_real_importe > vto_presupuesto.importe):
                # Solo sustituyo cuando supere lo previsto.
                sustituir_por_reales = True
            ### Caso resto proveedores.
            if (vto_presupuesto.es_de_compras() 
                    and abs(valor_real_importe)>abs(vto_presupuesto.importe)):
                # Solo sustituyo cuando supere lo previsto.
                sustituir_por_reales = True
            if pclases.DEBUG:
                print __file__, "-------->>>>", \
                    vto_presupuesto.conceptoPresupuestoAnual.descripcion, \
                    "; mes presup.:", \
                        vto_presupuesto.valorPresupuestoAnual.fecha.month, \
                    "; mes vto.:", vto_presupuesto.fecha.month, \
                    "; presup. en mes vto.:", vto_presupuesto.importe, \
                    "; real:", valor_real_importe, 
    if pclases.DEBUG:
        print __file__, valor_real_importe, "sustituir_por_reales [", \
                sustituir_por_reales, "]"
    return sustituir_por_reales

def buscar_vencimiento_presupuestado(fecha, concepto, fecha_mes_actual):
    """
    Devuelve el objeto VencimientoValorPresupuesto del presupuesto para la 
    fecha DE VENCIMIENTO y concepto especificados.
    """
    try:
        vtos = pclases.VencimientoValorPresupuestoAnual.select(pclases.AND(
          pclases.VencimientoValorPresupuestoAnual.q.fecha 
                >= primero_de_mes(fecha),
          pclases.VencimientoValorPresupuestoAnual.q.fecha 
                <= final_de_mes(fecha)))
        vto = [v for v in vtos if v.conceptoPresupuestoAnual == concepto][0]
        vp = vto.valorPresupuestoAnual
        # No interesan los vencimientos de valores presupuestados en el pasado.
        if vp.fecha < fecha_mes_actual:
            return None
        return vto
    except IndexError:
        return None

def restar_en_traza_presupuesto(dict_tracking, 
                                mes, 
                                mes_actual, 
                                concepto, 
                                valor_presupuestado, 
                                valor_real_importe, 
                                valor_real_toneladas = None):
    """
    Del diccionario de trazabilidad, extrae el objeto del valor presupuestado 
    y lo sustituye de nuevo por él mismo pero con la cantidad que aporta al 
    valor final decrementada en «valor_real_importe» y toneladas si es el caso.
    """
    for obj, importe, tm in dict_tracking[mes][concepto]:
        if obj == valor_presupuestado:
            dict_tracking[mes][concepto].remove((obj, importe, tm))
            # Para el mes actual nunca hay valores presupuestados. No lo 
            # vuelvo a agregar y santas pascuas.
            if mes != mes_actual:
                if valor_real_toneladas != None:
                    tm -= -valor_real_toneladas # Real: +. En presup.: -
                    importe = obj.precio * tm
                else:
                    importe -= valor_real_importe
                # Quito también valores negativos. Ya no influyen. Se ha 
                # sustituido por completo el valor presupuestado.
                if ((not concepto.es_gasto() and importe > 0) or (
                     concepto.es_gasto() and importe < 0)):
                    dict_tracking[mes][concepto].append((obj, 
                                                         importe, 
                                                         tm))
            break

def esta_pendiente(o):
    """
    Devuelve True si el objeto recibido está pendiente de cobro/pago. Ya sea 
    factura, línea de factura o servicio.
    Si no puede determinar la naturaleza, devuelve False por defecto.
    En el caso de las líneas de venta/compra y servicios mira si están 
    pendientes o no basándose en su factura **completa**.
    """
    o.sync()
    try:
        o = o.factura
        o.sync()
    except AttributeError:
        pass
    try:
        o = o.facturaCompra
        o.sync()
    except AttributeError:
        pass
    try:
        res = o.calcular_pendiente_cobro()
    except AttributeError:
        try:
            res = o.get_importe_primer_vencimiento_pendiente()
        except AttributeError:
            res = False
    return res


if __name__ == "__main__":
    p = DynConsulta()
