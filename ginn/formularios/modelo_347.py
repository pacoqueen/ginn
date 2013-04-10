#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado                    #
#                          (pacoqueen@users.sourceforge.net)                  #
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
## modelo_347.py - Listado de clientes y proveedores con 
##                 facturación >= 3.000 €
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 
###################################################################
## 
###################################################################
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sqlobject
import sys, os
try:
    import pclases
except ImportError:
    sys.path.append(os.path.join('..', 'framework'))
    import pclases
import mx.DateTime
try:
    import geninformes
except ImportError:
    sys.path.append(os.path.join('..', 'informes'))
    import geninformes
try:
    from treeview2pdf import treeview2pdf
except ImportError:
    sys.path.append(os.path.join("..", "informes"))
    from treeview2pdf import treeview2pdf
try:
    from treeview2csv import treeview2csv
except ImportError:
    sys.path.append(os.path.join("..", "informes"))
    from treeview2pdf import treeview2pdf
from informes import abrir_pdf, abrir_csv
import ventana_progreso

class Modelo347(Ventana):
    def __init__(self, objeto = None, usuario = None):
        self.usuario = usuario
        Ventana.__init__(self, 'modelo_347.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_exportar/clicked': self.exportar}
        self.add_connections(connections)
        try:
            primer_anno_compra = pclases.FacturaCompra._connection.queryOne(
                "SELECT MIN(date_part('year', fecha)) "
                "FROM factura_compra;")[0]
            primer_anno_venta = pclases.FacturaVenta._connection.queryOne(
                "SELECT MIN(date_part('year', fecha)) "
                "FROM factura_venta;")[0]
            ultimo_anno_compra = pclases.FacturaCompra._connection.queryOne(
                "SELECT MAX(date_part('year', fecha)) "
                "FROM factura_compra;")[0]
            ultimo_anno_venta = pclases.FacturaVenta._connection.queryOne(
                "SELECT MAX(date_part('year', fecha)) "
                "FROM factura_venta;")[0]
            primer_anno = min(primer_anno_compra, primer_anno_venta)
            ultimo_anno = max(ultimo_anno_compra, ultimo_anno_venta)
        except IndexError:
            primer_anno = ultimo_anno = actual = 0
        actual = mx.DateTime.localtime().year - 1
        self.wids['sp_anno'].set_value(actual)
        if not primer_anno <= actual <= ultimo_anno:
            actual = ultimo_anno
        for tv in ("tv_clientes", "tv_proveedores"):
            cols = (('Cliente','gobject.TYPE_STRING', False, True, True, None),
                    ('NIF','gobject.TYPE_STRING', False, True, False, None),
                    ('Facturado','gobject.TYPE_STRING',False,True,False,None),
                    ('IdCliente','gobject.TYPE_INT64',False,False,False,None))
            utils.preparar_listview(self.wids[tv], cols)
            col = self.wids[tv].get_columns()[2]
            for cell in col.get_cell_renderers():
                cell.set_property("xalign", 1.0)
            col.set_alignment(0.5)
        self.wids['tv_clientes'].connect("row-activated", 
                                         self.abrir_facturado_clientes)
        gtk.main()

    def abrir_facturado_clientes(self, tv, path, vc):
        """
        Abre la consulta de facturación por cliente con el cliente marcado 
        y las fechas correspondientes al año de la ventana.
        """
        model = tv.get_model()
        id = model[path][-1]
        cliente = pclases.Cliente.get(id) 
        anno = self.wids['sp_anno'].get_value_as_int()
        fini = mx.DateTime.DateTimeFrom(day = 1, 
                                        month = 1, 
                                        year = anno)
        fin = mx.DateTime.DateTimeFrom(day = 31, 
                                       month = 12, 
                                       year = anno)
        import facturacion_por_cliente_y_fechas
        ventana = facturacion_por_cliente_y_fechas.FacturacionPorClienteYFechas(
            objeto = cliente, 
            fini = fini, 
            ffin = fin, 
            usuario = self.usuario)

    def chequear_cambios(self):
        pass

    def rellenar_tablas(self, clientes, proveedores):
        """
        Rellena el model con los items de la consulta
        """
        for tv, datos, total in (("tv_clientes", clientes, "e_total_c"), 
                                 ("tv_proveedores", proveedores, "e_total_p")):
            model = self.wids[tv].get_model()
            model.clear()
            self.wids[tv].freeze_child_notify()
            self.wids[tv].set_model(None)
            for nombre, cif, facturado, id in datos:
                model.append((nombre, 
                              cif, 
                              utils.float2str(facturado), 
                              id))
            sumatotal = sum([i[2] for i in datos])
            self.wids[total].set_text(utils.float2str(sumatotal))
            self.wids[tv].set_model(model)
            self.wids[tv].thaw_child_notify()

    def buscar(self, boton):
        """
        Dadas fecha de inicio y de fin, lista todos los albaranes
        pendientes de facturar.
        """
        umbral = 3005.06   # Hacienda dixit. 
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        anno = self.wids['sp_anno'].get_value_as_int()
        finicio = mx.DateTime.DateTimeFrom(day = 1, 
                                           month = 1, 
                                           year = anno)
        ffin = mx.DateTime.DateTimeFrom(day = 31, 
                                        month = 12, 
                                        year = anno)
        facturasventa = pclases.FacturaVenta.select(pclases.AND(
                            pclases.FacturaVenta.q.fecha >= finicio, 
                            pclases.FacturaVenta.q.fecha <= ffin))
        facturascompra = pclases.FacturaCompra.select(pclases.AND(
                            pclases.FacturaCompra.q.fecha >= finicio, 
                            pclases.FacturaCompra.q.fecha <= ffin))
        act = 0.0; tot = facturasventa.count() + facturascompra.count()
        clientes = {}
        for f in facturasventa:
            vpro.set_valor(act/tot, "Analizando facturas de venta...")
            cliente = f.cliente
            if cliente not in clientes:
                clientes[cliente] = f.calcular_importe_total()
            else:
                clientes[cliente] += f.calcular_importe_total()
            act += 1
        proveedores = {}
        for f in facturascompra:
            vpro.set_valor(act/tot, "Analizando facturas de compra...")
            proveedor = f.proveedor
            if proveedor not in proveedores:
                proveedores[proveedor] = f.calcular_importe_total()
            else:
                proveedores[proveedor] += f.calcular_importe_total()
            act += 1
        lista_clientes = []
        for c in clientes:
            if c != None and clientes[c] > umbral:
                lista_clientes.append((c.nombre, 
                                       c.cif, 
                                       clientes[c], 
                                       c.id))
        lista_proveedores = []
        for p in proveedores:
            if p != None and proveedores[p] > umbral:
                lista_proveedores.append((p.nombre, 
                                          p.cif, 
                                          proveedores[p], 
                                          p.id))
        self.rellenar_tablas(lista_clientes, lista_proveedores)
        vpro.ocultar()

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe.
        """
        # TODO: Esto debe imprimir además una carta por cliente y proveedor 
        #       para enviársela y corroborar los datos.
        utils.dialogo_info(titulo = "NO DISPONIBLE", 
                           texto = "Funcionalidad no disponible.", 
                           padre = self.wids['ventana'])


    def exportar(self, boton):
        """
        Exporta el TreeView a CSV.
        """
        abrir_csv(treeview2csv(self.wids['tv_clientes']))
        abrir_csv(treeview2csv(self.wids['tv_proveedores']))

if __name__ == '__main__':
    t = Modelo347()

