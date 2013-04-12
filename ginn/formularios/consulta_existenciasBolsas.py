#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado,                   #
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
## listado_productosBolsas.py - Listado de Geocem embolsado. 
###################################################################
## 
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk
import sys, os
from framework import pclases
import mx.DateTime
from formularios.ventana_progreso import VentanaProgreso

class ConsultaExistenciasBolsas(Ventana):

    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self.inicio = None
        self.fin = None
        Ventana.__init__(self, 'consulta_existenciasBolsas.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_fecha/clicked': self.set_fecha, 
                       'b_actualizar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_exportar/clicked': self.exportar, 
                       'e_fecha/focus-out-event': act_fecha}
        self.add_connections(connections)
        cols = (('Código', 'gobject.TYPE_STRING', False, True, False, None),
                ('Descripción', 'gobject.TYPE_STRING', False,True,False,None),
                ('Existencias\ntotales', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Bultos\ntotales', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Existencias (A)', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Bultos (A)', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Existencias (B)', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Bultos (B)', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Existencias (C)', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Bultos (C)', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
        self.tvs = [(self.wids["tv_datos"], self.wids['e_total_kilos'], 
                     self.wids['e_total_bultos'], None)]
        nb = self.wids['nb_almacenes']
        for a in pclases.Almacen.select(
                pclases.Almacen.q.activo == True, orderBy = "id"):
            tv, e_kg, e_bultos, box = build_tv(a)
            self.tvs.append((tv, e_kg, e_bultos, a))
            nb.append_page(box, gtk.Label(a.nombre))
        nb.show_all()
        for tv, e_kg, e_bultos, box in self.tvs:
            utils.preparar_listview(tv, cols)
            for ncol in range(2, 10):
                col = self.wids['tv_datos'].get_column(ncol)
                for cell in col.get_cell_renderers():
                    cell.set_property("xalign", 1)
            tv.connect("row-activated", self.abrir_producto)
        self.wids['b_actualizar'].grab_focus()
        gtk.main()

    def set_fecha(self, boton):
        """
        Cambia la fecha de los filtros.
        """
        w = self.wids[boton.name.replace("b_", "e_")]
        try:
            fechaentry = utils.parse_fecha(w.get_text())
        except (TypeError, ValueError):
            fechaentry = mx.DateTime.today()
        w.set_text(utils.str_fecha(utils.mostrar_calendario(
                                                fecha_defecto = fechaentry, 
                                                padre = self.wids['ventana'])))

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        npag = self.wids['nb_almacenes'].get_current_page()
        tv = self.tvs[npag][0]
        abrir_csv(treeview2csv(tv))

    def abrir_producto(self, tv, path, column):
        """
        Abre el producto al que se le ha hecho doble clic en una ventana nueva.
        """
        model = tv.get_model()
        puid = model[path][-1]
        producto = pclases.getObjetoPUID(puid)
        if producto.es_rollo():
            import productos_de_venta_rollos
            V = productos_de_venta_rollos.ProductosDeVentaRollos
            ventana_producto = V(producto, usuario = self.usuario)  # @UnusedVariable
        elif producto.es_bala() or producto.es_bigbag() or producto.es_bolsa():
            import productos_de_venta_balas
            V = productos_de_venta_balas.ProductosDeVentaBalas
            ventana_producto = V(producto, usuario = self.usuario)  # @UnusedVariable

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, items):
        """
        Rellena el model con los items de la consulta
        """
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        vpro.set_valor(0.0, "Contando existencias...")
        act = 0.0
        tot = len(items) * len(self.tvs)
        try:
            fecha = utils.parse_fecha(self.wids['e_fecha'].get_text())
        except (TypeError, ValueError, AttributeError):
            fecha = mx.DateTime.today()
            self.wids['e_fecha'].set_text(utils.str_fecha(fecha))
        # XXX: Optimización (cosas de cómo están hechas las funciones de get_*
        #      por dentro en pclases):
        if fecha >= mx.DateTime.today():
            fecha = None
        for tv, kg, bultos, a in self.tvs:
            model = tv.get_model()
            model.clear()
            totalkgs = 0.0
            totalbultos = 0
            for pv in items:
                vpro.set_valor(act/tot, 
                               "Contando existencias...\t[%s]" % pv.get_puid())
                stock = pv.get_stock(hasta = fecha, almacen = a)
                totalkgs += stock
                existencias = pv.get_existencias(hasta=fecha, almacen = a)
                totalbultos += existencias
                stock_A = pv.get_stock_A(hasta = fecha, almacen = a)
                existencias_A = pv.get_existencias_A(hasta=fecha, almacen = a)
                stock_B = pv.get_stock_B(hasta = fecha, almacen = a)
                existencias_B = pv.get_existencias_B(hasta=fecha, almacen = a)
                stock_C = pv.get_stock_C(hasta = fecha, almacen = a)
                existencias_C = pv.get_existencias_C(hasta=fecha, almacen = a)
                model.append((pv.codigo,
                              pv.descripcion,
                              utils.float2str(stock),
                              utils.float2str(existencias, autodec = True),
                              utils.float2str(stock_A!=None and stock_A or 0),
                              utils.float2str(existencias_A != None and 
                                              existencias_A or 0, 
                                              autodec = True),
                              utils.float2str(stock_B!=None and stock_B or 0),
                              utils.float2str(existencias_B != None and 
                                              existencias_B or 0, 
                                              autodec = True),
                              utils.float2str(stock_C!=None and stock_C or 0),
                              utils.float2str(existencias_C != None and 
                                              existencias_C or 0, 
                                              autodec = True),
                              pv.get_puid()))
                act += 1
            kg.set_text(utils.float2str(totalkgs))
            bultos.set_text(utils.float2str(totalbultos, autodec = True))
        vpro.ocultar()

    def buscar(self, boton):
        productos = []
        for pv in pclases.ProductoVenta.select():
            if pv.es_bolsa():
                productos.append(pv)
        self.rellenar_tabla(productos)

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        from informes.treeview2pdf import treeview2pdf
        from formularios.reports import abrir_pdf
        npag = self.wids['nb_almacenes'].get_current_page()
        tv, ekg, ebultos = self.tvs[npag][0:3]
        kg = ekg.get_text()
        bultos = ebultos.get_text()
        strfecha = utils.str_fecha(mx.DateTime.localtime())
        iter1 = tv.get_model().append(("---", )*11)
        iter2 = tv.get_model().append(
            ("", "", kg, bultos, "", "", "", "", "", "", ""))
        informe = treeview2pdf(tv, 
                        titulo="Listado de existencias de fibra embolsada: %s"
                            % self.wids['nb_almacenes'].get_tab_label_text(
                                tv.parent.parent), 
                        fecha = strfecha) 
        tv.get_model().remove(iter1)
        tv.get_model().remove(iter2)
        if informe:
            abrir_pdf(informe)

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

def build_tv(almacen):
    """
    Construye un TreeView dentro de un ScrolledWindow y lo devuelve, 
    junto con los 2 entries de totales.
    """
    tv = gtk.TreeView()
    tv.set_name("tv_%s" % almacen.get_puid())
    sc = gtk.ScrolledWindow()
    sc.add(tv)
    vbox = gtk.VBox()
    vbox.pack_start(sc, expand = True)
    hbox = gtk.HBox()
    hbox.pack_start(gtk.Label("Total kg: "))
    kg = gtk.Entry()
    kg.set_has_frame(False)
    kg.set_property("editable", False)
    hbox.pack_start(kg)
    hbox.pack_start(gtk.Label("Total bultos: "))
    bultos = gtk.Entry()
    bultos.set_has_frame(False)
    bultos.set_property("editable", False)
    hbox.pack_start(bultos)
    vbox.pack_start(hbox, expand = False)
    return tv, kg, bultos, vbox


if __name__ == '__main__':
    t = ConsultaExistenciasBolsas()

