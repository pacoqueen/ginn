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
## consulta_ventas.py -- 
###################################################################
## NOTAS:
##  No cuenta servicios.
##  Cuenta prefacturas.
##  Al exportar exporta solo la página activa, pero al imprimir 
##  genera los 3 PDFs. It's not a bug. It's a feature!
###################################################################
## Changelog:
## 27 de marzo de 2006 -> Inicio
## 3 de agosto de 2006 -> Arreglado cálculo de totales.
## 20 de noviembre de 2006 -> ¡Felicidades mamá!
## 
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk, time
from framework import pclases
import mx.DateTime
from informes import geninformes
import pango 
from lib import charting


class ConsultaVentas(Ventana):
    inicio = None
    fin = None
    resultado = []
        
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        global fin
        Ventana.__init__(self, 'consulta_ventas.glade', objeto, self.usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       'b_exportar/clicked': self.exportar, 
                       'notebook1/switch-page': self.cambiar_grafica}
        self.add_connections(connections)
        cols = (('Fecha', 'gobject.TYPE_STRING', False, True, False, None),
                ('Producto', 'gobject.TYPE_STRING', False, True, False, None),
                ('Cantidad', 'gobject.TYPE_STRING', False, True, False, None),
                ('Precio', 'gobject.TYPE_STRING', False, True, False, None),
                ('Total (sin IVA)', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Cliente', 'gobject.TYPE_STRING', False, True, False, None),
                ('Pedido', 'gobject.TYPE_STRING', False, True, False, None),
                ("Comercial", 'gobject.TYPE_STRING', False, True, False, None),
                ('Albarán', 'gobject.TYPE_STRING', False, True, False, None),
                ("Transporte\n-alb.completo-", 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Destino', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Factura', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Forma de cobro', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Cobro real', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Idlineadecompra', 'gobject.TYPE_INT64', 
                    False, False, False, None))
        tv = self.wids['tv_datos']
        utils.preparar_treeview(tv, cols)
        tv.connect("row-activated", self.abrir_producto_o_tarifa)
        tv.get_column(2).get_cell_renderers()[0].set_property('xalign', 0.5) 
        tv.get_column(3).get_cell_renderers()[0].set_property('xalign', 1) 
        tv.get_column(4).get_cell_renderers()[0].set_property('xalign', 1) 
        tv.get_column(9).get_cell_renderers()[0].set_property('xalign', 1) 
        self.colorear(tv)
        cols = (('Producto', 'gobject.TYPE_STRING', False, True, True, None),
                ('Cantidad', 'gobject.TYPE_STRING', False, True, False, None),
                ('Total (sin IVA)', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Id', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_producto'], cols)
        getcoltvpro = self.wids['tv_producto'].get_column
        getcoltvpro(1).get_cell_renderers()[0].set_property('xalign', 1) 
        getcoltvpro(2).get_cell_renderers()[0].set_property('xalign', 1) 
        cols = (('Cliente', 'gobject.TYPE_STRING', False, True, True, None),
                ('CIF', 'gobject.TYPE_STRING', False, True, False, None),
                ('Fecha', 'gobject.TYPE_STRING', False, True, False, None),
                ('Importe c/IVA', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Nº. factura', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Forma de cobro', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Cobro real', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Id', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_cliente'], cols)
        cell = self.wids['tv_cliente'].get_column(3).get_cell_renderers()[0]
        cell.set_property('xalign', 1) 
        self.wids['tv_cliente'].connect("row-activated", 
                                        self.abrir_factura_o_cliente)
        inicio = mx.DateTime.DateTimeFrom(day = 1, 
                                        month = mx.DateTime.localtime().month, 
                                        year = mx.DateTime.localtime().year)
        self.inicio = inicio.strftime("%Y/%m/%d")
        self.wids['e_fechainicio'].set_text(utils.str_fecha(inicio))
        # TODO: Hacer que sea editable y que recuerde la fecha.
        temp = time.localtime()
        self.fin = str(temp[0])+'/'+str(temp[1])+'/'+str(temp[2])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.metros_totales = 0.0
        self.kilos_totales = 0.0
        opciones = [(c.id, c.nombre) 
                    for c in pclases.Cliente.select(orderBy = "nombre")]
        opciones.insert(0, (-1, "Todos"))
        utils.rellenar_lista(self.wids['cbe_cliente'], opciones)
        utils.combo_set_from_db(self.wids['cbe_cliente'], -1)
        opciones = [(c.id, c.nombre) 
                    for c in pclases.Almacen.select(
                        pclases.Almacen.q.activo == True, 
                        orderBy = "id")]
        opciones.insert(0, (-1, "Todos"))
        utils.rellenar_lista(self.wids['cbe_almacen'], opciones)
        utils.combo_set_from_db(self.wids['cbe_almacen'], -1)
        # CWT: Filtro por producto
        opciones = [(pv.id, pv.descripcion)
                    for pv in pclases.ProductoVenta.select(
                        pclases.ProductoVenta.q.obsoleto == False,
                        orderBy = "descripcion")]
        for pc in pclases.ProductoCompra.select(
                        pclases.ProductoCompra.q.obsoleto == False,
                        orderBy = "descripcion"):
            opciones.append((-pc.id, pc.descripcion)) # En negativo los PCompra
        opciones.insert(0, (0, "Todos"))
        self.wids['cbe_producto'] = gtk.ComboBoxEntry()
        utils.rellenar_lista(self.wids['cbe_producto'], opciones)
        utils.combo_set_from_db(self.wids['cbe_producto'], 0)
        box = gtk.HBox()
        box.pack_start(gtk.Label("Producto:"), expand = False)
        box.pack_start(self.wids['cbe_producto'], expand = True)
        box.set_homogeneous(False)
        self.wids['cbe_almacen'].parent.parent.add(box)
        self.wids['cbe_almacen'].parent.parent.reorder_child(box, 2)
        self.wids['cbe_almacen'].parent.parent.show_all()
        # Esta vez dejo el 0 como "Todos"
        hay_fibra = pclases.CamposEspecificosBala.select().count() > 0
        self.wids['label7'].set_property("visible", hay_fibra)
        self.wids['e_total_kilos'].set_property("visible", hay_fibra)
        hay_gtx = pclases.CamposEspecificosRollo.select().count() > 0
        self.wids['label8'].set_property("visible", hay_gtx)
        self.wids['e_total_metros'].set_property("visible", hay_gtx)
        self.por_tarifa = {}
        self.por_cliente = {}
        self.por_comercial = {}
        self.por_proveedor = {}
        cols = (('Comercial', 'gobject.TYPE_STRING', False, True, True, None),
                ('Forma de pago', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Facturación del comercial\n(IVA incl.)', 
                    'gobject.TYPE_STRING', False, True, False, None),
                ('Beneficio', 'gobject.TYPE_STRING', False, True, False, None),
                ('Total facturado\n(IVA incl.)', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Cobro real', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Id', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_comercial'], cols)
        tv = self.wids['tv_comercial']
        tv.get_column(2).get_cell_renderers()[0].set_property('xalign', 1) 
        tv.get_column(3).get_cell_renderers()[0].set_property('xalign', 1) 
        tv.get_column(4).get_cell_renderers()[0].set_property('xalign', 1) 
        tv.connect("row-activated", self.abrir_factura_o_comercial)
        self.wids['ch_servicios'].set_active(True)  # Por defecto lo voy a 
            # activar para que se vean las ventas totales en la nueva pestaña
            # por cliente.
        cols = (('Proveedor', 'gobject.TYPE_STRING', False, True, True, None),
                ('Forma de pago', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Asignable al proveedor\n(IVA incl.)', 
                    'gobject.TYPE_STRING', False, True, False, None),
                ('Beneficio', 'gobject.TYPE_STRING', False, True, False, None),
                ('Total facturado\n(IVA incl.)', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Cobro real', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Id', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_proveedor'], cols)
        tv = self.wids['tv_proveedor']
        tv.get_column(2).get_cell_renderers()[0].set_property('xalign', 1) 
        tv.get_column(3).get_cell_renderers()[0].set_property('xalign', 1) 
        tv.get_column(4).get_cell_renderers()[0].set_property('xalign', 1) 
        tv.connect("row-activated", self.abrir_factura_o_proveedor)
        gtk.main()
    
    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        if self.wids['notebook1'].get_current_page() == 0:
            tv = self.wids['tv_datos']
            desglosar = True
        elif self.wids['notebook1'].get_current_page() == 1:
            tv = self.wids['tv_cliente']
            desglosar = False
        elif self.wids['notebook1'].get_current_page() == 2:
            tv = self.wids['tv_producto']
            desglosar = None    # No se aplica. No es TreeView, sino ListView.
        elif self.wids['notebook1'].get_current_page() == 3:
            tv = self.wids['tv_comercial']
            desglosar = True
        elif self.wids['notebook1'].get_current_page() == 4:
            tv = self.wids['tv_proveedor']
            desglosar = True
        else:
            return
        abrir_csv(treeview2csv(tv, desglosar = desglosar))

    def colorear(self, tv):
        def cell_func(column, cell, model, itr, numcol):
            if (((model[itr][2] and model[itr][2].startswith("-")) 
                 or (model[itr][3] and model[itr][3].startswith("-"))) 
                and (model[itr][4] and model[itr][4].startswith("-"))):
                cell.set_property("foreground", "red")
            else:
                cell.set_property("foreground", None)
            if (model[itr][2] and model[itr][2].startswith('[') 
                    and model[itr][2].endswith(']')):
                cell.set_property("style-set", True)
                cell.set_property("style", pango.STYLE_ITALIC)
            else:
                cell.set_property("style-set", False)
        cols = tv.get_columns()
        for i in xrange(len(cols)):
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell, cell_func, i)

    def abrir_factura_o_cliente(self, tv, path, view_column):
        """
        Abre la factura o el cliente según corresponda.
        """
        model = tv.get_model()
        ide = model[path][-1]
        if ide > 0 and model[path].parent == None:   # Es cliente.
            from formularios import clientes
            cliente = pclases.Cliente.get(ide)
            v = clientes.Clientes(cliente)  # @UnusedVariable
        elif ide > 0 and model[path].parent != None: # Es factura.
            factura = pclases.FacturaVenta.get(ide)
            from formularios import facturas_venta
            v = facturas_venta.FacturasVenta(factura)  # @UnusedVariable
    
    def abrir_factura_o_comercial(self, tv, path, view_column):
        """
        Abre la factura o la ficha del comercial, según corresponda.
        """
        model = tv.get_model()
        ide = model[path][-1]
        if ide > 0 and ide != '0' and model[path].parent == None: # Es comercial.
            comercial = pclases.Comercial.get(ide)
            empleado = comercial.empleado
            from formularios import empleados
            v = empleados.Empleados(empleado)  # @UnusedVariable
        elif ide != "" and model[path].parent != None: # Es factura.
            factura = pclases.getObjetoPUID(ide)
            if isinstance(factura, pclases.FacturaVenta):
                from formularios import facturas_venta
                v = facturas_venta.FacturasVenta(factura,  # @UnusedVariable
                                                 usuario = self.usuario)
            elif isinstance(factura, pclases.FacturaDeAbono):
                from formularios import abonos_venta
                v = abonos_venta.AbonosVenta(factura, usuario = self.usuario)  # @UnusedVariable

    def abrir_factura_o_proveedor(self, tv, path, view_column):
        """
        Abre la factura o la ficha del proveedor, según corresponda.
        """
        model = tv.get_model()
        ide = model[path][-1]
        if ide > 0 and ide != '0' and model[path].parent == None: # Es proveedor.
            proveedor = pclases.Proveedor.get(ide)
            from formularios import proveedores
            v = proveedores.Proveedores(proveedor)  # @UnusedVariable
        elif ide != "" and model[path].parent != None: # Es factura.
            factura = pclases.getObjetoPUID(ide)
            if isinstance(factura, pclases.FacturaVenta):
                from formularios import facturas_venta
                v = facturas_venta.FacturasVenta(factura,  # @UnusedVariable
                                                 usuario = self.usuario)
            elif isinstance(factura, pclases.FacturaDeAbono):
                from formularios import abonos_venta
                v = abonos_venta.AbonosVenta(factura, usuario = self.usuario)  # @UnusedVariable

    def abrir_producto_o_tarifa(self, tv, path, view_column):
        """
        Si la fila seleccionada es una tarifa, abre la tarifa. Si es 
        un producto, abre el producto.
        """
        model = tv.get_model()
        ide = model[path][-1]
        if ide > 0 and model[path].parent == None:   # Es tarifa.
            from formularios import tarifas_de_precios
            tarifa = pclases.Tarifa.get(ide)
            v = tarifas_de_precios.TarifasDePrecios(tarifa)  # @UnusedVariable
        elif ide > 0 and model[path].parent != None: # Es producto
            ldv = pclases.LineaDeVenta.get(ide)
            producto = ldv.producto
            if isinstance(producto, pclases.ProductoVenta):
                if producto.es_rollo():
                    from formularios import productos_de_venta_rollos
                    v = productos_de_venta_rollos.ProductosDeVentaRollos(  # @UnusedVariable
                            producto)
                elif producto.es_bala() or producto.es_bigbag():
                    from formularios import productos_de_venta_balas
                    v = productos_de_venta_balas.ProductosDeVentaBalas(  # @UnusedVariable
                            producto)

    def get_producto_filtro(self):
        """
        Si se ha seleccionado un producto del filtro, devuelve su objeto
        de la BD. En otro caso, None.
        """
        idproducto = utils.combo_get_value(self.wids['cbe_producto'])
        if idproducto > 0:
            producto = pclases.ProductoVenta.get(idproducto)
        elif idproducto < 0:
            producto = pclases.ProductoCompra.get(-idproducto)
        else:
            producto = None
        return producto

    def chequear_cambios(self):
        pass

    def rellenar_tabla_por_tarifa(self, items, items_abono, servicios):
        """
        Rellena el model con los items de la consulta
        """ 
        model = self.wids['tv_datos'].get_model()
        model.clear()
        total = 0.0
        self.metros_totales = 0.0
        self.kilos_totales = 0.0
        self.por_tarifa = {}
        idalmacen = utils.combo_get_value(self.wids['cbe_almacen'])
        if idalmacen == -1:
            almacen = None
        else:
            almacen = pclases.Almacen.get(idalmacen)
        for i in items_abono['lineasDeDevolucion']:
            if not almacen or i.get_almacen() == almacen:
                tarifa, total = self.procesar_ldd(i, self.por_tarifa, model, 
                                                  total)
        for i in items_abono['lineasDeAbono']:
            if not almacen or i.get_almacen() == almacen:
                tarifa, total = self.procesar_lda(i, self.por_tarifa, model, 
                                                  total)
        for i in items:
            if not almacen or i.get_almacen() == almacen:
                tarifa, total = self.procesar_ldv(i, self.por_tarifa, model, 
                                                  total)
        for srv in servicios:
            if not almacen or i.get_almacen() == almacen:
                tarifa, total = self.procesar_srv(srv, self.por_tarifa, model, 
                                                  total)
        for tarifa in self.por_tarifa:
            model[self.por_tarifa[tarifa]['nodo']][4] = \
                "%s €" % (utils.float2str(self.por_tarifa[tarifa]['total'], 3))
            if self.por_tarifa[tarifa]['metros'] != 0:
                total_gtx = "GTX.: %s m² (%d rollos), %s kg" % (
                    utils.float2str(self.por_tarifa[tarifa]['metros'], 2), 
                    self.por_tarifa[tarifa]['rollos'], 
                    utils.float2str(self.por_tarifa[tarifa]['kilos_gtx'], 2))
            else:
                total_gtx = ""
            if self.por_tarifa[tarifa]['kilos'] != 0:
                kilos_fibra = utils.float2str(
                                self.por_tarifa[tarifa]['kilos'], 2)
                total_fib = "FIBRA: %s kg" % (kilos_fibra)
            else:
                total_fib = ""
            if self.por_tarifa[tarifa]['kilos_cable'] != 0:
                kilos_cable = self.por_tarifa[tarifa]['kilos_cable']
                kilos_cable = utils.float2str(kilos_cable, 2)
                total_cab = "FIBRA C: %s kg" % (kilos_cable)
            else:
                total_cab = ""
            txt_totales = "; ".join(
                [i for i in (total_gtx, total_fib, total_cab) if i])
            model[self.por_tarifa[tarifa]['nodo']][5] = txt_totales 
        self.wids['e_total'].set_text("%s € " % (utils.float2str(total)))
        total_kilos = "%s kg" % (utils.float2str(self.kilos_totales))
        total_fibra_c = sum([self.por_tarifa[t]['kilos_cable'] 
                             for t in self.por_tarifa])
        if total_fibra_c:
            total_kilos += " + %s kg C" % (
                utils.float2str(total_fibra_c, 2))
        self.wids['e_total_kilos'].set_text(total_kilos)
        total_metros = "%s m²" % (utils.float2str(self.metros_totales))
        self.wids['e_total_metros'].set_text(total_metros)
        # Y ahora la gráfica.
        datachart = []
        for t in self.por_tarifa:
            datachart.append([t and t.nombre or "Sin tarifa", 
                              self.por_tarifa[t]['total'], 
                              t and 3 or 7])
        try:
            oldchart = self.wids['eventbox_chart'].get_child()
            if oldchart != None:
                #self.wids['eventbox_chart'].remove(oldchart)
                chart = oldchart
            else:
                chart = charting.Chart(orient = "horizontal")
                self.wids['eventbox_chart'].add(chart)
            datachart.sort(lambda fila1, fila2: (fila1[0] < fila2[0] and -1) 
                                                 or (fila1[0] > fila2[0] and 1)
                                                 or 0)
            chart.plot(datachart)
            self.wids['eventbox_chart'].show_all()
        except Exception, msg:
            txt = "consulta_ventas.py::rellenar_tabla_por_tarifa -> "\
                  "Error al dibujar gráfica (charting): %s" % msg
            print txt
            self.logger.error(txt)

    def cambiar_grafica(self, nb, page, page_num):
        if page_num == 0:
            # Y ahora la gráfica.
            datachart = []
            for t in self.por_tarifa:
                datachart.append([t and t.nombre or "Sin tarifa", 
                                  self.por_tarifa[t]['total'], 
                                  t and 3 or 7])
            try:
                oldchart = self.wids['eventbox_chart'].get_child()
                if oldchart != None:
                    self.wids['eventbox_chart'].remove(oldchart)
                    #chart = oldchart
                #else:
                chart = charting.Chart(orient = "horizontal")
                self.wids['eventbox_chart'].add(chart)
                datachart.sort(
                    lambda fila1, fila2: (fila1[0] < fila2[0] and -1) 
                                         or (fila1[0] > fila2[0] and 1) 
                                         or 0)
                chart.plot(datachart)
                self.wids['eventbox_chart'].show_all()
            except Exception, msg:
                txt = "consulta_ventas.py::cambiar_grafica -> "\
                      "Error al dibujar gráfica (charting): %s" % msg
                print txt
                self.logger.error(txt)
        elif page_num == 1:
            # Y ahora la gráfica.
            datachart = []
            for t in self.por_cliente:
                datachart.append([t and t.nombre or "Sin cliente", 
                                  sum([f.calcular_importe_total() for f 
                                       in self.por_cliente[t]]), 
                                  t and 3 or 8])
            # Filtro y me quedo con el TOP5:
            datachart.sort(lambda c1, c2: int(c2[1] - c1[1]))
            _datachart = datachart[:5]
            _datachart.append(("Resto", sum([c[1] for c in datachart[5:]]), 7))
            datachart = _datachart
            try:
                oldchart = self.wids['eventbox_chart'].get_child()
                if oldchart != None:
                    self.wids['eventbox_chart'].remove(oldchart)
                    #chart = oldchart
                #else:
                chart = charting.Chart(orient = "horizontal", 
                                           values_on_bars = True)
                self.wids['eventbox_chart'].add(chart)
                chart.plot(datachart)
                self.wids['eventbox_chart'].show_all()
            except Exception, msg:
                txt = "consulta_ventas.py::cambiar_gragica -> "\
                      "Error al dibujar gráfica (charting): %s" % msg
                print txt
                self.logger.error(txt)
        elif page_num == 3:
            # Y ahora la gráfica.
            datachart = []
            model = self.wids['tv_comercial'].get_model()
            try:
                maximo_ventas = max([utils._float(f[1]) 
                                     for f in model if f[0]!="Sin comercial"])
            except ValueError:  # empty sequence
                maximo_ventas = 0
            for fila in model:
                if fila[0] == "Sin comercial":
                    color = 7
                elif utils._float(fila[2]) == maximo_ventas:
                    color = 0
                else:
                    color = 3
                datachart.append([fila[0], utils._float(fila[2]), color])
            # Filtro y me quedo con el TOP5:
            datachart.sort(lambda c1, c2: int(c2[2] - c1[2]))
            #_datachart = datachart[:5]
            #_datachart.append(("Resto", sum([c[1] for c in datachart[5:]])))
            #datachart = _datachart
            try:
                oldchart = self.wids['eventbox_chart'].get_child()
                if oldchart != None:
                    self.wids['eventbox_chart'].remove(oldchart)
                    #chart = oldchart
                #else:
                chart = charting.Chart(orient = "horizontal", 
                                           values_on_bars = True)
                self.wids['eventbox_chart'].add(chart)
                chart.plot(datachart)
                self.wids['eventbox_chart'].show_all()
            except Exception, msg:
                txt = "consulta_ventas.py::cambiar_gragica -> "\
                      "Error al dibujar gráfica (charting): %s" % msg
                print txt
                self.logger.error(txt)
        elif page_num == 4:
            # Y ahora la gráfica.
            datachart = []
            model = self.wids['tv_proveedor'].get_model()
            try:
                maximo_ventas = max([utils._float(f[1]) 
                                     for f in model if f[0]!="Sin proveedor"])
            except ValueError:  # empty sequence
                maximo_ventas = 0
            for fila in model:
                if fila[0] == "Sin proveedor":
                    color = 7
                elif utils._float(fila[2]) == maximo_ventas:
                    color = 0
                else:
                    color = 3
                datachart.append([fila[0], utils._float(fila[2]), color])
            # Filtro y me quedo con el TOP5:
            datachart.sort(lambda c1, c2: int(c2[2] - c1[2]))
            #_datachart = datachart[:5]
            #_datachart.append(("Resto", sum([c[1] for c in datachart[5:]])))
            #datachart = _datachart
            try:
                oldchart = self.wids['eventbox_chart'].get_child()
                if oldchart != None:
                    self.wids['eventbox_chart'].remove(oldchart)
                    #chart = oldchart
                #else:
                chart = charting.Chart(orient = "horizontal", 
                                           values_on_bars = True)
                self.wids['eventbox_chart'].add(chart)
                chart.plot(datachart)
                self.wids['eventbox_chart'].show_all()
            except Exception, msg:
                txt = "consulta_ventas.py::cambiar_gragica -> "\
                      "Error al dibujar gráfica (charting): %s" % msg
                print txt
                self.logger.error(txt)
 
    def procesar_lda(self, lda, por_tarifa, model, total):
        producto = self.get_producto_filtro()
        if producto and lda.producto != producto:
            return None, total
        # XXX: Filtro por producto
        precio = lda.precio * (1 - lda.descuento)
            # Lo pongo en negativo porque es dinero que se ha devuelto/pagado.
        total_ldv = lda.cantidad * precio 
        tarifa = lda.get_tarifa()
        kilos = kilos_gtx = kilos_cable = metros = rollos = 0  # @UnusedVariable
        if lda.productoVenta and lda.productoVenta.es_rollo():
            metros = lda.cantidad
            try:
                rollos = int(lda.cantidad /  # @UnusedVariable
                    lda.productoVenta.camposEspecificosRollo.metros_cuadrados)
            except ZeroDivisionError:
                rollos = 0  # @UnusedVariable
            kilos_gtx = ((metros *  # @UnusedVariable
                lda.productoVenta.camposEspecificosRollo.gramos) / 1000.0)
        elif lda.productoVenta and (lda.productoVenta.es_bala() 
                                    or lda.productoVenta.es_bigbag()):
            kilos = lda.cantidad  # @UnusedVariable
        elif lda.productoVenta and (lda.productoVenta.es_bala_cable()):
            kilos_cable = lda.cantidad  # @UnusedVariable
        else:       # ldv.producto es un pclases.ProductoCompra. No puedo 
                    # medir sus metros, kilos ni bultos
            pass
        if tarifa not in self.por_tarifa:
            padre = model.append(None,
                                    ("", 
                                     tarifa and tarifa.nombre or "Sin tarifa",
                                     "",
                                     "", 
                                     "%s €" % (utils.float2str(0, 3)),
                                     "", 
                                     "", 
                                     "", 
                                     "",
                                     "",
                                     "", 
                                     "",
                                     "",
                                     "",
                                     tarifa and tarifa.id or 0))
            self.por_tarifa[tarifa] = {'nodo': padre, 
                                  'ldvs': [lda, ], 
                                  'total': total_ldv, 
                                  'metros': 0, 
                                  'kilos': 0, 
                                  'rollos': 0, 
                                  'kilos_gtx': 0, 
                                  'kilos_cable': 0}
                # Los kg y metros no deben computar para el total, ya se 
                # cuentan en la factura correspondiente. El importe en 
                # euros, sin embargo, sí que hay que contarlo.
        else:
            self.por_tarifa[tarifa]['ldvs'].append(lda)
            self.por_tarifa[tarifa]['total'] += total_ldv
            padre = self.por_tarifa[tarifa]['nodo']
        if lda.pedidoVentaID == None:
            pedido = ''
        else:
            pedido = lda.pedidoVenta.numpedido
        fra = lda.facturaVenta or lda.prefactura
        if fra == None:
            factura = ""
            fdp = ""
            fdpreal = ""
        #    if pedido != "":
        #        fdp = pedido.formaDePago and pedido.formaDePago.toString() or ""
        #    else:
        #        fdp = ""
        else:
            factura = fra.numfactura
            try:
                fdp = fra.vencimientosCobro[0].observaciones
            except (AttributeError, IndexError):
                fdp = ""
            fdpreal = fra.get_str_cobro_real()
        if lda.albaranSalida != None and lda.albaranSalida.cliente != None:
            cliente = lda.albaranSalida.cliente.nombre
        elif fra != None and fra.cliente != None:
            cliente = fra.cliente.nombre
        elif lda.pedidoVenta != None and lda.pedidoVenta.cliente != None:
            cliente = lda.pedidoVenta.cliente.nombre
        else:
            cliente = ""
        destino = lda.albaranSalida and lda.albaranSalida.nombre or cliente
        total = total + (precio * lda.cantidad)
        if lda.productoVenta and lda.productoVenta.es_rollo():
            metros_o_kilos = "m²"
            try:
                bultos = "(%s rollos)" % (int(lda.cantidad / 
                    lda.productoVenta.camposEspecificosRollo.metros_cuadrados))
            except ZeroDivisionError:
                bultos = ""
        elif lda.productoVenta and (lda.productoVenta.es_bala() 
                                    or lda.productoVenta.es_bigbag()):
            metros_o_kilos = "kg"
            bultos = "(N/A)"
        else:
            metros_o_kilos = ""
            bultos = ""
        cantidad = "%s %s" % (utils.float2str(lda.cantidad, 1), metros_o_kilos)
        transporte = ""     # En abonos nole.
        comerciales = (lda.facturaVenta 
            and lda.facturaVenta.dividir_total_por_comercial().keys() or [])
        comerciales = [c.get_nombre_completo() for c in comerciales if c]
        comercial = "; ".join(comerciales)
        model.append(padre, 
            (utils.str_fecha((lda.facturaVentaID and lda.facturaVenta.fecha) 
                              or (lda.prefacturaID and lda.prefactura.fecha)
                        or (lda.albaranSalidaID and lda.albaranSalida.fecha) 
                            or (lda.pedidoVentaID and lda.pedidoVenta.fecha)),
             (lda.producto and lda.producto.descripcion)
                or (lda.servicio and lda.servicio.descripcion)
                or "Línea de abono vacía",
             "[%s %s]" % (cantidad, bultos),
             "%s €" % (utils.float2str(precio, 3)),
             "%s €" % (utils.float2str(total_ldv, 3)),
             cliente, 
             pedido,
             comercial, 
             lda.albaranSalidaID and lda.albaranSalida.numalbaran or "",
             transporte, 
             destino, 
             factura,
             fdp, 
             fdpreal, 
             lda.id))
        return tarifa, total

    def procesar_ldd(self, ldd, por_tarifa, model, total):
        producto = self.get_producto_filtro()
        if producto and ldd.producto != producto:
            return None, total
        # XXX: Filtro por producto
        precio = -ldd.precio * (1 - ldd.descuento)
            # Lo pongo en negativo porque es dinero que se ha devuelto/pagado.
        total_ldv = precio # ldd.cantidad * precio  
            # En las LDD el precio es el precio del artículo completo (la 
            # unidad), no por m² ni kg.
        tarifa = ldd.get_tarifa()
        kilos = kilos_gtx = kilos_cable = metros = rollos = 0
        if ldd.productoVenta and ldd.productoVenta.es_rollo():
            metros = ldd.cantidad
            try:
                rollos = int(ldd.cantidad / 
                    ldd.productoVenta.camposEspecificosRollo.metros_cuadrados)
            except ZeroDivisionError:
                rollos = 0
            kilos_gtx = ((metros * 
                          ldd.productoVenta.camposEspecificosRollo.gramos) 
                         / 1000.0)
        elif ldd.productoVenta and (ldd.productoVenta.es_bala() 
                                    or ldd.productoVenta.es_bigbag()):
            kilos = ldd.cantidad
        elif ldd.productoVenta and (ldd.productoVenta.es_bala_cable()):
            kilos_cable += ldd.cantidad
        else:       # ldv.producto es un pclases.ProductoCompra. No puedo 
                    # medir sus metros, kilos ni bultos
            pass
        if tarifa not in self.por_tarifa:
            padre = model.append(None, 
                                    ("", 
                                     tarifa and tarifa.nombre or "Sin tarifa",
                                     "",
                                     "", 
                                     "%s €" % (utils.float2str(0, 3)),
                                     "", 
                                     "", 
                                     "", 
                                     "",
                                     "",
                                     "", 
                                     "",
                                     "", 
                                     "",
                                     tarifa and tarifa.id or 0))
            self.por_tarifa[tarifa] = {'nodo': padre, 
                                  'ldvs': [ldd, ], 
                                  'total': total_ldv, 
                                  'metros': metros, 
                                  'kilos': kilos, 
                                  'rollos': rollos, 
                                  'kilos_gtx': kilos_gtx, 
                                  'kilos_cable': kilos_cable}
        else:
            self.por_tarifa[tarifa]['ldvs'].append(ldd)
            self.por_tarifa[tarifa]['total'] += total_ldv
            self.por_tarifa[tarifa]['metros'] += metros
            self.por_tarifa[tarifa]['kilos'] += kilos
            self.por_tarifa[tarifa]['rollos'] += rollos
            self.por_tarifa[tarifa]['kilos_gtx'] += kilos_gtx
            self.por_tarifa[tarifa]['kilos_cable'] += kilos_cable
            padre = self.por_tarifa[tarifa]['nodo']
        if ldd.pedidoVentaID == None:
            pedido = ''
        else:
            pedido = ldd.pedidoVenta.numpedido
        fra = ldd.facturaVenta or ldd.prefactura
        if fra == None:
            factura = ""
            fdp = ""
            fdpreal = ""
            #if pedido != "":
            #    fdp = pedido.formaDePago and pedido.formaDePago.toString() or ""
            #else:
            #    fdp = ""
        else:
            factura = fra.numfactura
            try:
                fdp = fra.vencimientosCobro[0].observaciones
            except (IndexError, AttributeError):
                fdp = ""
            fdpreal = fra.get_str_cobro_real()
        if ldd.albaranSalida != None and ldd.albaranSalida.cliente != None:
            cliente = ldd.albaranSalida.cliente.nombre
        elif fra != None and fra.cliente != None:
            cliente = fra.cliente.nombre
        elif ldd.pedidoVenta != None and ldd.pedidoVenta.cliente != None:
            cliente = ldd.pedidoVenta.cliente.nombre
        else:
            cliente = ""
        destino = ldd.albaranSalida and ldd.albaranSalida.nombre or cliente
        total = total + precio # * ldd.cantidad)  # El precio en la LDD ya es 
        # el subtotal. Es el precio de la unidad completa, no en m² ni kg.
        if ldd.productoVenta and ldd.productoVenta.es_rollo():
            metros_o_kilos = "m²"
            try:
                bultos = "(%s rollos)" % (int(ldd.cantidad / 
                    ldd.productoVenta.camposEspecificosRollo.metros_cuadrados))
            except ZeroDivisionError:
                bultos = ""
            self.metros_totales += ldd.cantidad
        elif ldd.productoVenta and (ldd.productoVenta.es_bala() 
                                    or ldd.productoVenta.es_bigbag()):
            metros_o_kilos = "kg"
            bultos = "(N/A)"
            self.kilos_totales += ldd.cantidad
        else:
            metros_o_kilos = ""
            bultos = ""
        cantidad = "%s %s" % (utils.float2str(ldd.cantidad, 1), metros_o_kilos)
        transporte = ""     # En abonos nole.
        comerciales = (ldd.facturaVenta 
            and ldd.facturaVenta.dividir_total_por_comercial().keys() or [])
        comerciales = [c.get_nombre_completo() for c in comerciales if c]
        comercial = "; ".join(comerciales)
        model.append(padre, 
            (utils.str_fecha((ldd.facturaVentaID and ldd.facturaVenta.fecha) 
                        or (ldd.prefacturaID and ldd.prefactura.fecha)
                        or (ldd.albaranSalidaID and ldd.albaranSalida.fecha) 
                        or (ldd.pedidoVentaID and ldd.pedidoVenta.fecha)),
             ldd.producto.descripcion,
             "%s %s" % (cantidad, bultos),
             "%s €" % (utils.float2str(precio, 3)),
             "%s €" % (utils.float2str(total_ldv, 3)),
             cliente, 
             pedido,
             comercial, 
             ldd.albaranSalidaID and ldd.albaranSalida.numalbaran or "",
             transporte, 
             destino, 
             factura,
             fdp, 
             fdpreal, 
             ldd.id))
        return tarifa, total

    def procesar_ldv(self, i, por_tarifa, model, total):
        producto = self.get_producto_filtro()
        if producto and i.producto != producto:
            return None, total
        # XXX: Filtro por producto
        precio = i.precio * (1 - i.descuento)
        total_ldv = i.cantidad * precio
        tarifa = i.get_tarifa()
        kilos_cable = kilos = metros = rollos = kilos_gtx = 0
        if i.productoVenta and i.productoVenta.es_rollo():
            metros = i.cantidad
            try:
                rollos = int(i.cantidad / 
                    i.productoVenta.camposEspecificosRollo.metros_cuadrados)
            except ZeroDivisionError:
                rollos = 0
            kilos_gtx = (metros 
                * i.productoVenta.camposEspecificosRollo.gramos) / 1000.0
        elif i.productoVenta and (i.productoVenta.es_bala() 
                                  or i.productoVenta.es_bigbag()):
            kilos = i.cantidad
        elif i.productoVenta and i.productoVenta.es_bala_cable():
            kilos_cable = i.cantidad
        else:       # ldv.producto es un pclases.ProductoCompra. 
                    # No puedo medir sus metros, kilos ni bultos
            pass
        if tarifa not in self.por_tarifa:
            padre = model.append(None, 
                                    ("", 
                                     tarifa and tarifa.nombre or "Sin tarifa",
                                     "",
                                     "", 
                                     "%s €" % (utils.float2str(0, 3)),
                                     "", 
                                     "",
                                     "",
                                     "", 
                                     "", 
                                     "", 
                                     "", 
                                     "",
                                     "",
                                     tarifa and tarifa.id or 0))
            self.por_tarifa[tarifa] = {'nodo': padre, 
                                  'ldvs': [i, ], 
                                  'total': total_ldv, 
                                  'metros': metros, 
                                  'kilos': kilos, 
                                  'rollos': rollos, 
                                  'kilos_gtx': kilos_gtx, 
                                  'kilos_cable': kilos_cable}
        else:
            self.por_tarifa[tarifa]['ldvs'].append(i)
            self.por_tarifa[tarifa]['total'] += total_ldv
            self.por_tarifa[tarifa]['metros'] += metros
            self.por_tarifa[tarifa]['kilos'] += kilos
            self.por_tarifa[tarifa]['rollos'] += rollos
            self.por_tarifa[tarifa]['kilos_gtx'] += kilos_gtx
            self.por_tarifa[tarifa]['kilos_cable'] += kilos_cable
            padre = self.por_tarifa[tarifa]['nodo']
        if i.pedidoVentaID == None:
            pedido = ''
        else:
            pedido = i.pedidoVenta.numpedido
        fra = i.facturaVenta or i.prefactura
        if fra == None:
            factura = ""
            fdp = fdpreal = ""
            #if pedido != "":
            #    fdp = pedido.formaDePago and pedido.formaDePago.toString() or ""
            #else:
            #    fdp = ""
        else:
            factura = fra.numfactura
            try:
                fdp = fra.vencimientosCobro[0].observaciones
            except (IndexError, AttributeError):
                fdp = ""
            fdpreal = fra.get_str_cobro_real()
        if i.albaranSalida != None and i.albaranSalida.cliente != None:
            cliente = i.albaranSalida.cliente.nombre
        elif fra != None and fra.cliente != None:
            cliente = fra.cliente.nombre
        elif i.pedidoVenta != None and i.pedidoVenta.cliente != None:
            cliente = i.pedidoVenta.cliente.nombre
        else:
            cliente = ""
        destino = (i.albaranSalida and i.albaranSalida.nombre 
                   and i.albaranSalida.nombre or cliente)
        total = total + (precio * i.cantidad)
        if i.productoVenta and i.productoVenta.es_rollo():
            metros_o_kilos = "m²"
            try:
                bultos = "(%s rollos)" % (int(i.cantidad 
                    / i.productoVenta.camposEspecificosRollo.metros_cuadrados))
            except ZeroDivisionError:
                bultos = ""
            self.metros_totales += i.cantidad
        elif i.productoVenta and (i.productoVenta.es_bala() 
                                  or i.productoVenta.es_bigbag()):
            metros_o_kilos = "kg"
            bultos = "(N/A)"
            self.kilos_totales += i.cantidad
        else:
            metros_o_kilos = ""
            bultos = ""
        cantidad = "%s %s" % (utils.float2str(i.cantidad, 1), metros_o_kilos)
        sumtransportes = (i.albaranSalida and 
                          sum([transp.precio 
                               for transp 
                               in i.albaranSalida.transportesACuenta])
                          or None)
        transporte = (sumtransportes 
                      and "%s €" % utils.float2str(sumtransportes) 
                      or "")
        comerciales = (i.facturaVenta 
            and i.facturaVenta.dividir_total_por_comercial().keys() or [])
        comerciales = [c.get_nombre_completo() for c in comerciales if c]
        comercial = "; ".join(comerciales)
        model.append(padre, 
            (utils.str_fecha((i.facturaVentaID and i.facturaVenta.fecha) 
                            or (i.prefacturaID and i.prefactura.fecha)
                            or (i.albaranSalidaID and i.albaranSalida.fecha) 
                            or (i.pedidoVentaID and i.pedidoVenta.fecha)),
             i.producto.descripcion,
             "%s %s" % (cantidad, bultos),
             "%s €" % (utils.float2str(precio, 3)),
             "%s €" % (utils.float2str(total_ldv, 3)),
             cliente, 
             pedido,
             comercial, 
             i.albaranSalidaID and i.albaranSalida.numalbaran or "",
             transporte, 
             destino, 
             factura,
             fdp, 
             fdpreal, 
             i.id))
        return tarifa, total
        
    def procesar_srv(self, i, por_tarifa, model, total):
        producto = self.get_producto_filtro()
        if producto:
            return None, total
        # XXX: Filtro por producto. Los servicios no tienen producto.
        precio = i.precio * (1 - i.descuento)
        total_ldv = i.cantidad * precio
        tarifa = None
        kilos_cable = kilos = metros = rollos = kilos_gtx = 0
        if tarifa not in self.por_tarifa:
            padre = model.append(None, 
                                    ("", 
                                     tarifa and tarifa.nombre or "Sin tarifa",
                                     "",
                                     "", 
                                     "%s €" % (utils.float2str(0, 3)),
                                     "", 
                                     "",
                                     "",
                                     "",
                                     "",
                                     "", 
                                     "",
                                     "", 
                                     "",
                                     tarifa and tarifa.id or 0))
            self.por_tarifa[tarifa] = {'nodo': padre, 
                                  'ldvs': [i, ], 
                                  'total': total_ldv, 
                                  'metros': metros, 
                                  'kilos': kilos, 
                                  'rollos': rollos, 
                                  'kilos_gtx': kilos_gtx, 
                                  'kilos_cable': kilos_cable}
        else:
            self.por_tarifa[tarifa]['ldvs'].append(i)
            self.por_tarifa[tarifa]['total'] += total_ldv
            self.por_tarifa[tarifa]['metros'] += metros
            self.por_tarifa[tarifa]['kilos'] += kilos
            self.por_tarifa[tarifa]['rollos'] += rollos
            self.por_tarifa[tarifa]['kilos_gtx'] += kilos_gtx
            self.por_tarifa[tarifa]['kilos_cable'] += kilos_cable
            padre = self.por_tarifa[tarifa]['nodo']
        if i.pedidoVentaID == None:
            pedido = ''
        else:
            pedido = i.pedidoVenta.numpedido
        fra = i.facturaVenta or i.prefactura
        if fra == None:
            fdp = factura = fdpreal = ""
            #if pedido != "":
            #    fdp = pedido.formaDePago and pedido.formaDePago.toString() or ""
            #else:
            #    fdp = ""
        else:
            factura = fra.numfactura
            try:
                fdp = fra.vencimientosCobro[0].observaciones
            except (IndexError, AttributeError):
                fdp = ""
            fdpreal = fra.get_str_cobro_real()
        if i.albaranSalida != None and i.albaranSalida.cliente != None:
            cliente = i.albaranSalida.cliente.nombre
        elif fra != None and fra.cliente != None:
            cliente = fra.cliente.nombre
        elif i.pedidoVenta != None and i.pedidoVenta.cliente != None:
            cliente = i.pedidoVenta.cliente.nombre
        else:
            cliente = ""
        destino = i.albaranSalida and i.albaranSalida.nombre or cliente
        total = total + (precio * i.cantidad)
        cantidad = utils.float2str(i.cantidad, autodec = True)
        sumtransportes = (i.albaranSalida and 
                          sum([t.precio 
                               for t in i.albaranSalida.transportesACuenta])
                          or None)
        transporte = (sumtransportes 
                      and "%s €" % utils.float2str(sumtransportes) 
                      or "")
        comerciales = (i.facturaVenta 
            and i.facturaVenta.dividir_total_por_comercial().keys() or [])
        comerciales = [c.get_nombre_completo() for c in comerciales if c]
        comercial = "; ".join(comerciales)
        model.append(padre, 
            (utils.str_fecha((i.facturaVentaID and i.facturaVenta.fecha) 
                            or (i.prefacturaID and i.prefactura.fecha)
                            or (i.albaranSalidaID and i.albaranSalida.fecha) 
                            or (i.pedidoVentaID and i.pedidoVenta.fecha)),
             i.concepto,
             cantidad,
             "%s €" % (utils.float2str(precio, 3)),
             "%s €" % (utils.float2str(total_ldv, 3)),
             cliente, 
             pedido,
             comercial, 
             i.albaranSalidaID and i.albaranSalida.numalbaran or "",
             transporte, 
             destino, 
             factura,
             fdp, 
             fdpreal, 
             -i.id))
        return tarifa, total
        
    def set_inicio(self, boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
        self.inicio = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])

    def set_fin(self, boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.fin = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])

    def por_fecha(self, e1, e2):
        """
        Permite ordenar una lista de objetos por fecha (deben tener un 
        atributo fecha).
        """
        if e1.fecha < e2.fecha:
            return -1
        elif e1.fecha > e2.fecha:
            return 1
        else:
            return 0
        
    def buscar(self, boton):
        """
        Dadas fecha de inicio y de fin, busca todas las ventas 
        (facturadas) entre esas dos fechas.
        """
        producto = self.get_producto_filtro()
        # XXX: Filtro por producto
        # TODO: PORASQUI: Deshabilito las pestañas que no pueden computar
        # por producto hasta que pueda corregirlo:
        self.wids['notebook1'].get_nth_page(1).set_property("visible",
                                                            not producto)
        self.wids['notebook1'].get_nth_page(3).set_property("visible",
                                                            not producto)
        self.wids['notebook1'].get_nth_page(4).set_property("visible",
                                                            not producto)
        self.wids['notebook1'].set_current_page(2)
        # TODO: PORASQUI: Probar si se ve todo el desplegable de productos en el servidor. En local se corta al ancho y no se ve.
        # XXX
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        # print self.fin, self.inicio
        vpro.set_valor(0.0, "Analizando facturas y abonos...")
        idcliente = utils.combo_get_value(self.wids['cbe_cliente'])
        if idcliente == -1:
            idcliente = None
        # El listado de ventas se hace a partir de facturas. Para hacerlo con 
        # albaranes, bueno, you know, cambiar la consulta y tal.
        self.resultado = []
        self.resultado_abonos = {'lineasDeAbono': [], 'lineasDeDevolucion': []}
        servicios = []
        if not self.inicio:
            if idcliente != None:
                facturas = pclases.FacturaVenta.select(
                    pclases.AND(pclases.FacturaVenta.q.fecha <= self.fin, 
                                pclases.FacturaVenta.q.clienteID == idcliente),
                    orderBy = 'fecha')
                prefacturas = pclases.Prefactura.select(
                    pclases.AND(pclases.Prefactura.q.fecha <= self.fin, 
                                pclases.Prefactura.q.clienteID == idcliente), 
                    orderBy = 'fecha')
                facturasDeAbono = pclases.FacturaDeAbono.select(
                    pclases.AND(pclases.FacturaDeAbono.q.fecha <= self.fin,
                            pclases.FacturaDeAbono.q.clienteID == idcliente),
                    orderBy = 'fecha')
                vpro.set_valor(0.1, "Analizando facturas y abonos...")
                facturasDeAbono = [f for f in facturasDeAbono 
                                    if f.abono 
                                       and f.abono.clienteID == idcliente]
            else:
                facturas = pclases.FacturaVenta.select(
                    pclases.FacturaVenta.q.fecha <= self.fin, 
                    orderBy = 'fecha')
                prefacturas = pclases.Prefactura.select(
                    pclases.Prefactura.q.fecha <= self.fin, 
                    orderBy = 'fecha')
                facturasDeAbono = pclases.FacturaDeAbono.select(
                    pclases.FacturaDeAbono.q.fecha <= self.fin, 
                    orderBy = 'fecha')
                vpro.set_valor(0.1, "Analizando facturas y abonos...")
                facturasDeAbono = [f for f in facturasDeAbono if f.abono]
        else:
            if idcliente != None:
                facturas = pclases.FacturaVenta.select(
                    pclases.AND(pclases.FacturaVenta.q.fecha >= self.inicio,
                                pclases.FacturaVenta.q.fecha <= self.fin, 
                                pclases.FacturaVenta.q.clienteID == idcliente),
                    orderBy='fecha')
                prefacturas = pclases.Prefactura.select(
                    pclases.AND(pclases.Prefactura.q.fecha >= self.inicio,
                                pclases.Prefactura.q.fecha <= self.fin, 
                                pclases.Prefactura.q.clienteID == idcliente), 
                    orderBy='fecha')
                facturasDeAbono = pclases.FacturaDeAbono.select(
                    pclases.AND(pclases.FacturaDeAbono.q.fecha <= self.fin, 
                                pclases.FacturaDeAbono.q.fecha >= self.inicio),
                    orderBy = 'fecha')
                vpro.set_valor(0.1, "Analizando facturas y abonos...")
                facturasDeAbono = [f for f in facturasDeAbono 
                                    if f.abono 
                                       and f.abono.clienteID == idcliente]
            else:
                facturas = pclases.FacturaVenta.select(
                    pclases.AND(pclases.FacturaVenta.q.fecha >= self.inicio,
                                pclases.FacturaVenta.q.fecha <= self.fin), 
                    orderBy='fecha')
                prefacturas = pclases.Prefactura.select(
                    pclases.AND(pclases.Prefactura.q.fecha >= self.inicio,
                                pclases.Prefactura.q.fecha <= self.fin), 
                    orderBy='fecha')
                facturasDeAbono = pclases.FacturaDeAbono.select(
                    pclases.AND(pclases.FacturaDeAbono.q.fecha <= self.fin, 
                                pclases.FacturaDeAbono.q.fecha >= self.inicio),
                    orderBy = 'fecha')
                vpro.set_valor(0.1, "Analizando facturas y abonos...")
                facturasDeAbono = [f for f in facturasDeAbono if f.abono]
        vpro.set_valor(0.2, "Analizando facturas y abonos...")
        facturas = list(facturas) + list(prefacturas)
        facturas.sort(self.por_fecha)
        vpro.set_valor(0.3, "Analizando facturas y abonos...")
        for f in facturas:
            for linea in f.lineasDeVenta:
                self.resultado.append(linea)
            if self.wids['ch_servicios'].get_active():
                for srv in f.servicios:
                    servicios.append(srv)
        facturasDeAbono.sort(self.por_fecha)
        vpro.set_valor(0.4, "Analizando facturas y abonos...")
        for f in facturasDeAbono:
            abono = f.abono
            for lda in abono.lineasDeAbono:
                if (lda.lineaDeVenta != None 
                    and not self.wids['ch_servicios'].get_active()):
                    # Filtro las que son ajuste de precio de servicios.
                    self.resultado_abonos['lineasDeAbono'].append(lda)
            for ldd in abono.lineasDeDevolucion:
                self.resultado_abonos['lineasDeDevolucion'].append(ldd)
        vpro.set_valor(0.5, "Mostrando datos por tarifa...")
        self.rellenar_tabla_por_tarifa(self.resultado, 
                                       self.resultado_abonos, 
                                       servicios)
        vpro.set_valor(0.6, "Mostrando datos por producto...")
        self.rellenar_tabla_por_producto(self.resultado, 
                                         self.resultado_abonos, 
                                         servicios)
        vpro.set_valor(0.7, "Mostrando datos por cliente...")
        self.rellenar_tabla_clientes(self.resultado, 
                                     self.resultado_abonos, 
                                     servicios)
        vpro.set_valor(0.8, "Mostrando datos por comercial...")
        self.rellenar_tabla_comerciales(self.resultado, 
                                        self.resultado_abonos, 
                                        servicios)
        vpro.set_valor(0.9, "Mostrando datos por proveedor...")
        self.rellenar_tabla_proveedores(self.resultado, 
                                        self.resultado_abonos, 
                                        servicios)
        vpro.set_valor(1.0, "")
        vpro.ocultar()

    def rellenar_tabla_clientes(self, resultado, resultado_abonos, servicios):
        producto = self.get_producto_filtro()
        # XXX: Filtro por producto
        idalmacen = utils.combo_get_value(self.wids['cbe_almacen'])
        if idalmacen == -1:
            almacen = None
        else:
            almacen = pclases.Almacen.get(idalmacen)
        self.por_cliente = {}
        for linea in resultado:
            if not almacen or linea.get_almacen() == almacen:
                if not producto or linea.producto == producto:
                    cliente = linea.get_cliente()
                    factura = linea.get_factura_o_prefactura()
                    if cliente not in self.por_cliente:
                        self.por_cliente[cliente] = [factura]
                    else:
                        if factura not in self.por_cliente[cliente]:
                            self.por_cliente[cliente] += [factura]
        for ldabono in (resultado_abonos['lineasDeAbono'] 
                        + resultado_abonos['lineasDeDevolucion']):
            if not almacen or linea.get_almacen() == almacen:
                if not producto or linea.producto == producto:
                    cliente = ldabono.abono.cliente
                    factura = ldabono.abono.facturaDeAbono
                    if cliente not in self.por_cliente:
                        self.por_cliente[cliente] = [factura]
                    else:
                        if factura not in self.por_cliente[cliente]:
                            self.por_cliente[cliente] += [factura]
        for srv in servicios:
            if not almacen or srv.get_almacen() == almacen:
                if not producto:
                    cliente = srv.get_cliente()
                    factura = srv.get_factura_o_prefactura()
                    if cliente not in self.por_cliente:
                        self.por_cliente[cliente] = [factura]
                    else:
                        if factura not in self.por_cliente[cliente]:
                            self.por_cliente[cliente] += [factura]
        model = self.wids['tv_cliente'].get_model()
        model.clear()
        for cliente in self.por_cliente:
            # TODO: BUG: PORASQUI: ¿Y ahora qué hago con el total de la factura
            # si he seleccionado un producto y solo quiero el importe de esa
            # línea? Mientras tanto, deshabilito las pestañas conflictivas si 
            # hay filtro de producto.
            padre = model.append(None, 
                                 (cliente and cliente.nombre or "SIN CLIENTE", 
                                  "", 
                                  "", 
                                  utils.float2str(
                                    sum([f.calcular_importe_total() 
                                       for f in self.por_cliente[cliente]
                                       if not f is None])), 
                                  "",
                                  "", 
                                  "",
                                  cliente and cliente.id or 0))
            for factura in self.por_cliente[cliente]:
                # TODO: Si tiene varios vencimientos, combinar textos. 
                try:
                    fdp = factura.vencimientosCobro[0].observaciones
                except (IndexError, AttributeError):
                    fdp = ""    # Solo fdp confirmada en la factura.
                    #try:
                    #    fdp = factura.get_pedidos()[0].formaDePago.toString()
                    #except (IndexError, AttributeError):
                        #try:
                        #    fdp = factura.cliente.get_texto_forma_cobro()
                        #except (IndexError, AttributeError):
                        #    ftp = ""
                try:
                    fdpreal = factura.get_str_cobro_real()
                    model.append(padre, 
                            ("", 
                             factura.cliente.cif, 
                             utils.str_fecha(factura.fecha), 
                             utils.float2str(factura.calcular_importe_total()), 
                             factura.numfactura, 
                             fdp, 
                             fdpreal, 
                             factura.id))
                except AttributeError:  # ¿Factura es None?
                    txt = "El cliente %s tiene servicios o ventas "\
                          "sin factura. Sin embargo se ha intentado mostrar"\
                          " información de una factura en la consulta, "\
                          "obteniendo 'None' desde un servicio o una ldv. "\
                          "No debería ser una línea de abono. Se tratan "\
                          "en otra función diferente."\
                          "Contenido del diccionario 'self.por_cliente': %s"\
                            % (cliente.nombre, self.por_cliente)
                    self.logger.warning(txt)
                    print txt

    def rellenar_tabla_comerciales(self, resultado, resultado_abonos, 
                                   servicios):
        producto = self.get_producto_filtro()
        # XXX: Filtro por producto
        idalmacen = utils.combo_get_value(self.wids['cbe_almacen'])
        if idalmacen == -1:
            almacen = None
        else:
            almacen = pclases.Almacen.get(idalmacen)
        self.por_comercial = {}
        for linea in resultado:
            if not almacen or linea.get_almacen() == almacen:
                if not producto or linea.producto == producto:
                    comercial = linea.get_comercial()
                    factura = linea.get_factura_o_prefactura()
                    if comercial not in self.por_comercial:
                        self.por_comercial[comercial] = [factura]
                    else:
                        if factura not in self.por_comercial[comercial]:
                            self.por_comercial[comercial] += [factura]
        for srv in servicios:
            if not almacen or srv.get_almacen() == almacen:
                if producto:
                    comercial = srv.get_comercial()
                    factura = srv.get_factura_o_prefactura()
                    if comercial not in self.por_comercial:
                        self.por_comercial[comercial] = [factura]
                    else:
                        if factura not in self.por_comercial[comercial]:
                            self.por_comercial[comercial] += [factura]
        for lda in resultado_abonos['lineasDeAbono']:
            if not almacen or lda.get_almacen() == almacen:
                if not producto or lda.producto == producto:
                    comercial = lda.get_comercial()
                    factura = lda.facturaVenta    # De abono, en realidad
                    if comercial not in self.por_comercial:
                        self.por_comercial[comercial] = [factura]
                    else:
                        if factura not in self.por_comercial[comercial]:
                            self.por_comercial[comercial] += [factura]
        for ldd in resultado_abonos['lineasDeDevolucion']:
            if not almacen or ldd.get_almacen() == almacen:
                if not producto or ldd.producto == producto:
                    comercial = ldd.get_comercial()
                    factura = ldd.facturaVenta  # De abono, en realidad
                    if comercial not in self.por_comercial:
                        self.por_comercial[comercial] = [factura]
                    else:
                        if factura not in self.por_comercial[comercial]:
                            self.por_comercial[comercial] += [factura]
        model = self.wids['tv_comercial'].get_model()
        model.clear()
        for comercial in self.por_comercial:
            if comercial:
                nombre_comercial = "%s %s" % (comercial.empleado.nombre, 
                                              comercial.empleado.apellidos)
            else:
                nombre_comercial = "Sin comercial"
            padre = model.append(None, 
                                 (nombre_comercial, 
                                  "", 
                                  "0.0", 
                                  "0.0", 
                                  "0.0", 
                                  "",
                                  comercial and comercial.id or 0))
            for factura in self.por_comercial[comercial]:
                # Porque una factura puede tener varios comerciales, es 
                # necesario volver a dividir para obtener de nuevo el 
                # diccionario. Doble de CPU, pero es lo que hay de momento.
                facturado = factura.dividir_total_por_comercial()[comercial]
                beneficio=factura.dividir_beneficio_por_comercial()[comercial]
                totfactura = factura.calcular_importe_total()
                fdpreal = factura.get_str_cobro_real()
                model.append(padre, 
                             (factura.numfactura, 
                              factura.vencimientosCobro 
                                and factura.vencimientosCobro[0].observaciones 
                                or "", 
                              utils.float2str(facturado), 
                              utils.float2str(beneficio), 
                              utils.float2str(totfactura), 
                              fdpreal, 
                              factura.get_puid()))
                model[padre][2] = utils.float2str(
                                    utils._float(model[padre][2]) + facturado)
                model[padre][3] = utils.float2str(
                                    utils._float(model[padre][3]) + beneficio)
                model[padre][4] = utils.float2str(
                                    utils._float(model[padre][4]) + totfactura)

    def rellenar_tabla_proveedores(self, resultado, resultado_abonos, 
                                   servicios):
        producto = self.get_producto_filtro()
        # XXX: Filtro por producto
        idalmacen = utils.combo_get_value(self.wids['cbe_almacen'])
        if idalmacen == -1:
            almacen = None
        else:
            almacen = pclases.Almacen.get(idalmacen)
        self.por_proveedor = {}
        for linea in resultado:
            if not almacen or linea.get_almacen() == almacen:
                if not producto or linea.producto == producto:
                    proveedor = linea.get_proveedor()
                    factura = linea.get_factura_o_prefactura()
                    if proveedor not in self.por_proveedor:
                        self.por_proveedor[proveedor] = [factura]
                    else:
                        if factura not in self.por_proveedor[proveedor]:
                            self.por_proveedor[proveedor] += [factura]
        for srv in servicios:
            if not almacen or srv.get_almacen() == almacen:
                if not producto:
                    proveedor = srv.get_proveedor()
                    factura = srv.get_factura_o_prefactura()
                    if proveedor not in self.por_proveedor:
                        self.por_proveedor[proveedor] = [factura]
                    else:
                        if factura not in self.por_proveedor[proveedor]:
                            self.por_proveedor[proveedor] += [factura]
        for lda in resultado_abonos['lineasDeAbono']:
            if not almacen or lda.get_almacen() == almacen:
                if not producto or lda.producto == producto:
                    proveedor = lda.get_proveedor()
                    factura = lda.facturaVenta    # De abono, en realidad
                    if proveedor not in self.por_proveedor:
                        self.por_proveedor[proveedor] = [factura]
                    else:
                        if factura not in self.por_proveedor[proveedor]:
                            self.por_proveedor[proveedor] += [factura]
        for ldd in resultado_abonos['lineasDeDevolucion']:
            if not almacen or ldd.get_almacen() == almacen:
                if not producto or ldd.producto == producto:
                    proveedor = ldd.proveedor
                    factura = ldd.facturaVenta  # De abono, en realidad
                    if proveedor not in self.por_proveedor:
                        self.por_proveedor[proveedor] = [factura]
                    else:
                        if factura not in self.por_proveedor[proveedor]:
                            self.por_proveedor[proveedor] += [factura]
        model = self.wids['tv_proveedor'].get_model()
        model.clear()
        for proveedor in self.por_proveedor:
            if proveedor:
                nombre_proveedor = proveedor.nombre
            else:
                nombre_proveedor = "Sin proveedor"
            padre = model.append(None, 
                                 (nombre_proveedor, 
                                  "", 
                                  "0.0", 
                                  "0.0", 
                                  "0.0", 
                                  "",
                                  proveedor and proveedor.id or 0))
            for factura in self.por_proveedor[proveedor]:
                # Porque una factura puede tener varios proveedores, es 
                # necesario volver a dividir para obtener de nuevo el 
                # diccionario. Doble de CPU, pero es lo que hay de momento.
                facturado = factura.dividir_total_por_proveedor()[proveedor]
                beneficio=factura.dividir_beneficio_por_proveedor()[proveedor]
                totfactura = factura.calcular_importe_total()
                fdpreal = factura.get_str_cobro_real()
                model.append(padre, 
                             (factura.numfactura, 
                              factura.vencimientosCobro 
                                and factura.vencimientosCobro[0].observaciones 
                                or "", 
                              utils.float2str(facturado), 
                              utils.float2str(beneficio), 
                              utils.float2str(totfactura), 
                              fdpreal, 
                              factura.get_puid()))
                model[padre][2] = utils.float2str(
                                    utils._float(model[padre][2]) + facturado)
                model[padre][3] = utils.float2str(
                                    utils._float(model[padre][3]) + beneficio)
                model[padre][4] = utils.float2str(
                                    utils._float(model[padre][4]) + totfactura)

    def rellenar_tabla_por_producto(self, 
                                    resultado, 
                                    resultado_abonos, 
                                    servicios):
        productofiltro = self.get_producto_filtro()
        # XXX: Filtro por producto
        idalmacen = utils.combo_get_value(self.wids['cbe_almacen'])
        if idalmacen == -1:
            almacen = None
        else:
            almacen = pclases.Almacen.get(idalmacen)
        por_producto = {}
        for linea in resultado:
            if not almacen or linea.get_almacen() == almacen:
                if not productofiltro or linea.producto == productofiltro:
                    producto = linea.producto.descripcion
                    subtotal = linea.get_subtotal(iva = False)
                    cantidad = linea.cantidad
                    if producto not in por_producto:
                        por_producto[producto] = [cantidad, subtotal]
                    else:
                        por_producto[producto][0] += cantidad
                        por_producto[producto][1] += subtotal
        for srv in servicios:
            if not almacen or srv.get_almacen() == almacen:
                if not productofiltro:
                    producto = srv.concepto
                    subtotal = srv.get_subtotal(iva = False)
                    cantidad = srv.cantidad
                    if producto not in por_producto:
                        por_producto[producto] = [cantidad, subtotal]
                    else:
                        por_producto[producto][0] += cantidad
                        por_producto[producto][1] += subtotal
        model = self.wids['tv_producto'].get_model()
        model.clear()
        for desc in por_producto:
            model.append((desc, 
                          utils.float2str(por_producto[desc][0], autodec=True),
                          utils.float2str(por_producto[desc][1]), 
                          0))

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        from formularios import reports
        datos = []
        model = self.wids['tv_datos'].get_model()
        for itr in model:
            datos.append((itr[0],  itr[1],  itr[2],  itr[3],  itr[4], 
                          itr[5],  itr[6],  itr[7],  itr[8],  itr[9], 
                          itr[10], itr[11], itr[12], itr[13]))
            hijos = itr.iterchildren()
            if hijos != None:
                for hijo in hijos:
                    datos.append((hijo[0], hijo[1], hijo[2], hijo[3], hijo[4], 
                                  hijo[5], hijo[6], hijo[7], hijo[8], hijo[9], 
                                  hijo[10], hijo[11], hijo[12], hijo[13]))
            datos.append(("---", "---", "---", "---", "---", "---", "---", 
                          "---", "---", "---", "---", "---", "---", "---"))
        datos.append(("", "", "", "", "", "", "", "", "", "", "", "", "", ""))
        if self.metros_totales != 0:
            metros_totales = "TOTAL m² de geotextiles: %s " % (
                                utils.float2str(self.metros_totales))
        else:
            metros_totales = ""
        if self.kilos_totales != 0:
            kilos_totales = "TOTAL kg de fibra: %s " % (
                                utils.float2str(self.kilos_totales))
        else:
            kilos_totales = ""
        total_importe = self.wids['e_total'].get_text()
        datos.append(("" , "IMPORTE TOTAL: %s " % (total_importe), 
                      "", "", "", "%s" % (metros_totales), "", "", 
                      "%s" % (kilos_totales), "", "", "", ""))
        if not self.inicio:            
            fechaInforme = 'Hasta ' + utils.str_fecha(
                                        time.strptime(self.fin, "%Y/%m/%d"))
        else:
            fechaInforme = (utils.str_fecha(
                time.strptime(self.inicio, "%Y/%m/%d")) + ' - ' 
                + utils.str_fecha(time.strptime(self.fin, "%Y/%m/%d")))
        if datos != []:
            reports.abrir_pdf(geninformes.ventas(datos, fechaInforme))
        from informes.treeview2pdf import treeview2pdf
        if self.wids['notebook1'].get_current_page() == 0:
            self.wids['notebook1'].next_page()
            self.wids['notebook1'].realize()
            while gtk.events_pending(): gtk.main_iteration(False)
            self.wids['notebook1'].prev_page()
        reports.abrir_pdf(treeview2pdf(self.wids['tv_producto'], 
                                        titulo = "Ventas por producto", 
                                        fecha = fechaInforme))
        reports.abrir_pdf(treeview2pdf(self.wids['tv_cliente'], 
                                        titulo = "Facturas por cliente", 
                                        fecha = fechaInforme))
        reports.abrir_pdf(treeview2pdf(self.wids['tv_comercial'], 
                                    titulo = "Ventas facturadas por comercial",
                                    fecha = fechaInforme))
        reports.abrir_pdf(treeview2pdf(self.wids['tv_proveedor'], 
                        titulo = "Ventas facturadas según proveedor de origen",
                        fecha = fechaInforme))


if __name__ == '__main__':
    t = ConsultaVentas()

