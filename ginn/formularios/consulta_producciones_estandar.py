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
## consulta_producciones_estandar.py                               
###################################################################
## Listado de productos de venta (rollos) con sus velocidades. 
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
import mx.DateTime

class ProduccionesEstandar(Ventana):

    def __init__(self, objeto = None, usuario = None):
        self.usuario = usuario
        Ventana.__init__(self, 'listado_productos.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_limpiar/clicked': self.limpiar_tv, 
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_exportar/clicked': self.exportar}
        self.wids['b_limpiar'].set_property("visible", False)
        self.add_connections(connections)
        cols = (('Código', 'gobject.TYPE_STRING', False, True, False, None),
                ('Descripción', 'gobject.TYPE_STRING', False,True,False,None),
                ('Gramos', 'gobject.TYPE_STRING', False,True,False,None),
                ('Producción estándar', 
                    'gobject.TYPE_STRING', False,True,False,None),
                ('ID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(self.wids['tv_datos'], cols)
        for ncol in (2, 3):
            col = self.wids['tv_datos'].get_column(ncol)
            for cell in col.get_cell_renderers():
                cell.set_property("xalign", 1)
        self.wids['tv_datos'].connect("row-activated", self.abrir_producto)
        #self.wids['e_buscar'].grab_focus()
        self.wids['e_buscar'].set_property("visible", False)
        self.wids['label1'].set_property("visible", False)
        self.wids['ventana'].set_title("Velocidades de la línea de geotextiles según producto")
        gtk.main()

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        tv = self.wids['tv_datos']
        abrir_csv(treeview2csv(tv))

    def abrir_producto(self, tv, path, column):
        """
        Abre el producto al que se le ha hecho doble clic en una ventana nueva.
        """
        model = tv.get_model()
        idproducto = model[path][-1]
        try:
            if "PV" in idproducto:
                producto = pclases.ProductoVenta.get(idproducto.split(":")[1])
                if producto.es_rollo():
                    from formularios import productos_de_venta_rollos
                    V = productos_de_venta_rollos.ProductosDeVentaRollos
                    ventana_producto = V(producto, usuario = self.usuario)  # @UnusedVariable
                elif producto.es_bala() or producto.es_bigbag():
                    from formularios import productos_de_venta_balas
                    V = productos_de_venta_balas.ProductosDeVentaBalas
                    ventana_producto = V(producto, usuario = self.usuario)  # @UnusedVariable
            elif "PC" in idproducto:
                producto = pclases.ProductoCompra.get(idproducto.split(":")[1])
                from formularios import productos_compra
                V = productos_compra.ProductosCompra
                ventana_producto = V(producto, usuario = self.usuario)  # @UnusedVariable
        except Exception, e:
            utils.dialogo_info(titulo = "ERROR RECUPERANDO PRODUCTO",
                               texto = "El producto ID %d no se ha encontrado."
                               "\n\n"
                               "Compruebe que no haya sido eliminado recargand"
                               "o la consulta y vuelva a intentarlo."
                               "\n\n\n"
                               "Información de depuración:"
                               "\n%s" % (idproducto, e),
                               padre = self.wids['ventana'])

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, items):
        """
        Rellena el model con los items de la consulta
        """
        model = self.wids['tv_datos'].get_model()
        model.clear()
        for i in items:
            model.append((i.codigo,
                          i.descripcion,
                          i.camposEspecificosRollo.gramos, 
                          utils.float2str(i.prodestandar),
                          i.get_puid()))

    def buscar(self, boton):
        productos = pclases.ProductoVenta.select(
                pclases.ProductoVenta.q.camposEspecificosRolloID != None)
        self.rellenar_tabla(productos)

    def limpiar_tv(self, boton):
        """
        Limpia el TreeView.
        """
        model = self.wids['tv_datos'].get_model()
        model.clear()

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        from informes.treeview2pdf import treeview2pdf
        from formularios.reports import abrir_pdf
        strfecha = utils.str_fecha(mx.DateTime.localtime())
        informe = treeview2pdf(self.wids['tv_datos'], 
                        titulo="Listado de productos con velocidades", 
                        fecha = strfecha, 
                        apaisado = False) 
        if informe:
            abrir_pdf(informe)

if __name__ == '__main__':
    t = ProduccionesEstandar()

