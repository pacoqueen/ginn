#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2014  Francisco José Rodríguez Bogado,                   #
#                          Diego Muñoz Escalante.                             #
# (pacoqueen@users.sourceforge.net, escalant3@users.sourceforge.net)          #
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
## consulta_ventas_por_producto.py --
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 26 de julio de 2007 -> Inicio
## 7 de marzo de 2014 -> Rediseño.
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
import mx.DateTime

class ConsultaVentasPorProducto(Ventana):

    def __init__(self, objeto = None, usuario = None):
        self.usuario = usuario
        Ventana.__init__(self, 'consulta_ventas_por_producto.glade', 
                         objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       'b_exportar/clicked': self.exportar, 
                       'e_fechainicio/focus-out-event': act_fecha, 
                       'e_fechafin/focus-out-event': act_fecha}
        self.add_connections(connections)
        # TreeViews de fibra y cemento
        cols = [
            ('Producto', 'gobject.TYPE_STRING', False, True, True, None),
            ('kg A', 'gobject.TYPE_STRING', False, True, False, None),
            ('# A', 'gobject.TYPE_STRING', False, True, False, None),
            ('kg B', 'gobject.TYPE_STRING', False, True, False, None),
            ('# B', 'gobject.TYPE_STRING', False, True, False, None),
            ('kg C', 'gobject.TYPE_STRING', False, True, False, None),
            ('# C', 'gobject.TYPE_STRING', False, True, False, None),
            ('Total kg', 'gobject.TYPE_STRING', False, True, False, None),
            ('Total #', 'gobject.TYPE_STRING', False, True, False, None),
            ('PUID', 'gobject.TYPE_STRING', False, False, False, None)]
        for tv in (self.wids['tv_fibra'], self.wids['tv_cem']):
            utils.preparar_treeview(tv, cols)
            tv.connect("row-activated", self.abrir_producto_albaran_o_abono)
            for n in range(1, 9): 
                tv.get_column(n).get_cell_renderers()[0].set_property(
                        'xalign', 1) 
        # TreeView de geotextiles
        cols.insert(1, 
            ('m² A', 'gobject.TYPE_STRING', False, True, False, None))
        cols.insert(4, 
            ('m² B', 'gobject.TYPE_STRING', False, True, False, None))
        cols.insert(7, 
            ('m² C', 'gobject.TYPE_STRING', False, True, False, None))
        cols.insert(10, 
            ('Total m²', 'gobject.TYPE_STRING', False, True, False, None))
        utils.preparar_treeview(self.wids['tv_gtx'], cols)
        self.wids['tv_gtx'].connect("row-activated", 
                                      self.abrir_producto_albaran_o_abono)
        tv = self.wids['tv_gtx']
        for n in range(1, 13): 
            tv.get_column(n).get_cell_renderers()[0].set_property('xalign', 1) 
        # TreeView de otros
        cols = [
            ('Producto', 'gobject.TYPE_STRING', False, True, True, None),
            ('Cantidad', 'gobject.TYPE_STRING', False, True, False, None),
            ('PUID', 'gobject.TYPE_STRING', False, False, False, None)]
        utils.preparar_treeview(self.wids['tv_otros'], cols)
        self.wids['tv_otros'].connect("row-activated", 
                                      self.abrir_producto_albaran_o_abono)
        tv = self.wids['tv_otros']
        tv.get_column(1).get_cell_renderers()[0].set_property('xalign', 1) 
        fin = mx.DateTime.localtime()
        inicio = mx.DateTime.localtime() - mx.DateTime.oneWeek
        self.wids['e_fechainicio'].set_text(utils.str_fecha(inicio))
        self.wids['e_fechafin'].set_text(utils.str_fecha(fin))
        gtk.main()
    
    def chequear_cambios(self):
        pass

    def set_inicio(self, boton):
        temp = utils.mostrar_calendario(fecha_defecto = utils.parse_fecha(self.wids['e_fechainicio'].get_text()), 
                                        padre = self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))

    def set_fin(self, boton):
        temp = utils.mostrar_calendario(fecha_defecto = utils.parse_fecha(self.wids['e_fechafin'].get_text()), 
                                        padre = self.wids['ventana'])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))

    def buscar(self, boton):
        """
        A partir de las fechas de inicio y fin de la ventana busca los 
        artículos con trazabilidad y los clasifica por A, B y C en metros, 
        kilos reales CON embalaje y bultos. También busca los productos de 
        compra con las cantidades que salieron o entraron.
        """
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        fini = utils.parse_fecha(self.wids['e_fechainicio'].get_text())
        ffin = utils.parse_fecha(self.wids['e_fechafin'].get_text())
        vpro.set_valor(0.0, "Buscando albaranes de salida...")
        albs = pclases.AlbaranSalida.select(pclases.AND(
                                    pclases.AlbaranSalida.q.fecha >= fini, 
                                    pclases.AlbaranSalida.q.fecha < ffin), 
                                            orderBy = "fecha")
        fib = {}
        gtx = {}
        cem = {}
        otros = {}
        i = 0.0
        tot = albs.count()
        for a in albs:
            i += 1
            vpro.set_valor(i/tot, "Analizando albarán %s..." % a.numalbaran)
            # TODO: XXX
        # Abonos
        vpro.set_valor(0.0, "Buscando abonos...")
        adedas = pclases.AlbaranDeEntradaDeAbono.select(pclases.AND(
                            pclases.AlbaranDeEntradaDeAbono.q.fecha >= fini, 
                            pclases.AlbaranDeEntradaDeAbono.q.fecha < ffin), 
                        orderBy = "fecha")
        i = 0.0
        tot = adedas.count()
        for a in adedas:
            i += 1
            vpro.set_valor(i/tot, "Analizando abono %s..." % a.numalbaran)
            # TODO: XXX
        vpro.ocultar()
        self.rellenar_tabla(fib, gtx, cem, otros)

    def rellenar_tabla(self, fib, gtx, cem, otros):
        """
        Rellena el model con los items de la consulta.
        Recibe cuatro diccionarios dependiendo del tipo de producto que habrá 
        que introducir en los cuatro treeviews correspondientes.
        Los diccionarios se organizan:
        {'producto1': {'albarán1': {'m2': 0.0, 
                                    'kg': 0.0, 
                                    '#': 0}, 
         'producto2': {'albarán1': {'cantidad': 0.0}, 
         'producto3': {'albarán2': {'kg': 0.0, 
                                    '#': 0}, 
        ...}
        """ 
        tot_fibra = {'kg': 0.0, 
                     '#': 0}
        tot_gtx = {'kg': 0.0, 
                   '#': 0, 
                   'm2': 0.0}
        tot_cem = {'kg': 0.0, 
                   '#': 0}
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        i = 0.0
        tot = len(fib) + len(gtx) + len(cem) + len(otros)
        try:
            vpro.set_valor(i / tot, "Mostrando %s..." % ("")) 
        except ZeroDivisionError: 
            pass    # It's Easier to Ask Forgiveness than Permission (EAFP)
        for tv, dic, tot in ((self.wids['tv_fibra'], fib, tot_fibra), 
                             (self.wids['tv_gtx'], gtx, tot_gtx), 
                             (self.wids['tv_cem'], cem, tot_cem), 
                             (self.wids['tv_otros'], otros, None)):
            model = tv.get_model()
            model.clear()
            for producto in dic:
                i += 1
                vpro.set_valor(i / tot, "Mostrando %s..." % (producto)) 
                # TODO: PORASQUI
        vpro.ocultar()
        return tot_fibra, tot_gtx, tot_cem

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        tv = self.wids['tv_datos']
        abrir_csv(treeview2csv(tv))

    def abrir_producto_albaran_o_abono(self, tv, path, view_column):
        """
        Si la fila seleccionada es una tarifa, abre la tarifa. Si es 
        un producto, abre el producto.
        """
        model = tv.get_model()
        puid = model[path][-1]
        objeto = pclases.getObjetoPUID(puid)
        if isinstance(objeto, pclases.ProductoVenta):        # ProductoVenta 
            pv = objeto
            if pv.es_rollo() or pv.es_rollo_c():
                from formularios import productos_de_venta_rollos
                v = productos_de_venta_rollos.ProductosDeVentaRollos(pv, usuario = self.usuario)  # @UnusedVariable
            elif (pv.es_bala() or pv.es_bala_cable() or pv.es_bigbag() 
                    or pv.es_bolsa() or pv.es_caja()):
                from formularios import productos_de_venta_balas
                v = productos_de_venta_balas.ProductosDeVentaBalas(pv, usuario = self.usuario)  # @UnusedVariable
            elif pv.es_especial():
                from formularios import productos_de_venta_especial
                v = productos_de_venta_especial.ProductosDeVentaEspecial(pv, usuario = self.usuario)  # @UnusedVariable
        elif isinstance(objeto, pclases.ProductoCompra):
            pc = objeto
            from formularios import productos_compra
            v = productos_compra.ProductosCompra(pc, usuario = self.usuario)  # @UnusedVariable
        elif isinstance(objeto, pclases.AlbaranSalida):
            alb = objeto
            from formularios import albaranes_de_salida
            v = albaranes_de_salida.AlbaranesDeSalida(alb, usuario = self.usuario)  # @UnusedVariable
        elif isinstance(objeto, pclases.AlbaranDeEntradaDeAbono):
            abono = objeto
            from formularios import abonos_venta
            v = abonos_venta.AbonosVenta(abono, usuario = self.usuario)  # @UnusedVariable

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe.
        """
        from informes.treeview2pdf import treeview2pdf
        from formularios.reports import abrir_pdf
        strfecha = "%s - %s" % (self.wids['e_fechainicio'].get_text(), 
                                self.wids['e_fechafin'].get_text())
        resp = utils.dialogo(titulo = "¿IMPRIMIR DESGLOSE?", 
                             texto = "Puede imprimir únicamente los productos"
                                     " o toda la información de la ventana.\n"
                                     "¿Desea imprimir toda la información "
                                     "desglosada?", 
                             padre = self.wids['ventana'])
        tv = clone_treeview(self.wids['tv_datos'])  # Para respetar el orden 
        # del treeview original y que no afecte a las filas de totales que 
        # añado después. Si las añado al original directamente se mostrarán 
        # en el orden que correspondería en lugar de al final.
        model = tv.get_model()
        fila_sep = model.append(None, ("===",) * 9)
        fila_total_gtx = model.append(None, ("Total m² geotextiles", self.wids['e_total_metros'].get_text(), "", "", "", "", "", "", ""))
        fila_total_fibra = model.append(None, ("Total kg fibra", self.wids['e_total_kilos'].get_text(), "", "", "", "", "", "", ""))
        fila_total_otros = model.append(None, ("Total € otros", self.wids['e_total_otros'].get_text(), "", "", "", "", "", "", ""))
        if resp:
            tv.expand_all()
            while gtk.events_pending(): gtk.main_iteration(False)
        else:
            tv.collapse_all()
            while gtk.events_pending(): gtk.main_iteration(False)
            tv = convertir_a_listview(tv)
            # Para este caso particular me sobran las columnas de albarán y eso
            tv.remove_column(tv.get_columns()[-4])
            tv.remove_column(tv.get_columns()[-4])
            tv.remove_column(tv.get_columns()[-4])
        abrir_pdf(treeview2pdf(tv, 
            titulo = "Salidas de almacén agrupadas por producto", 
            fecha = strfecha))
        model.remove(fila_sep)
        model.remove(fila_total_gtx)
        model.remove(fila_total_fibra)
        model.remove(fila_total_otros)

def clone_treeview(otv):
    """
    Clona un treeview en uno nuevo.
    """
    ntv = gtk.TreeView()
    ntv.set_name(otv.get_name())
    omodel = otv.get_model()
    tipos = [omodel.get_column_type(i) for i in range(omodel.get_n_columns())]
    nmodel = gtk.TreeStore(*tipos)
    ntv.set_model(nmodel)
    for fila_nivel_1 in omodel:
        def agregar_fila(model, padre, fila):
            iterpadre = model.append(padre, fila)
            if hasattr(fila, 'iterchildren'):
                for hijo in fila.iterchildren():
                    agregar_fila(model, iterpadre, hijo)
        agregar_fila(nmodel, None, fila_nivel_1)
    for ocol in otv.get_columns():
        title = ocol.get_title()
        ocell = ocol.get_cell_renderers()[0]
        ncell = type(ocell)()
        ncol = gtk.TreeViewColumn(title, ncell)
        ncol.set_data("q_ncol", ocol.get_data("q_ncol"))
        ncol.get_cell_renderers()[0].set_property('xalign', 
                ocol.get_cell_renderers()[0].get_property('xalign')) 
        ntv.append_column(ncol)
    return ntv

def convertir_a_listview(otv):
    """
    Convierte el TreeView en un ListView con los mismos datos que el original y 
    lo devuelve.
    """
    ntv = gtk.TreeView()
    ntv.set_name(otv.get_name())
    omodel = otv.get_model()
    tipos = [omodel.get_column_type(i) for i in range(omodel.get_n_columns())]
    nmodel = gtk.ListStore(*tipos)
    ntv.set_model(nmodel)
    for fila in omodel:
        nmodel.append([e for e in fila])
    for ocol in otv.get_columns():
        title = ocol.get_title()
        ocell = ocol.get_cell_renderers()[0]
        ncell = type(ocell)()
        ncol = gtk.TreeViewColumn(title, ncell)
        ncol.set_data("q_ncol", ocol.get_data("q_ncol"))
        ncol.get_cell_renderers()[0].set_property('xalign', 
                ocol.get_cell_renderers()[0].get_property('xalign')) 
        ntv.append_column(ncol)
    return ntv

def act_fecha(entry, event):                                                    
    """
    Cambia los mnemotécnicos de fecha por la fecha debidamente formateada 
    o la cadena vacía para indicar que no hay límite de fecha.
    """
    txtfecha = entry.get_text()
    try:
        txtfecha = utils.str_fecha(utils.parse_fecha(txtfecha))
    except (ValueError, TypeError):
        txtfecha = ""
    entry.set_text(txtfecha)


if __name__ == '__main__':
    t = ConsultaVentasPorProducto()

