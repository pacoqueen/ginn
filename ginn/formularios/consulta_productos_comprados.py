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
## consulta_productos_clientes.py --
###################################################################
## NOTAS:
##
###################################################################
## Changelog:
## 4 de abril de 2006 -> Inicio
##
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sqlobject
try:
    import pclases
except ImportError:
    import sys
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    import pclases
import mx.DateTime
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes


class ConsultaProductosComprados(Ventana):
    inicio = None
    fin = None
    cliente = None
    resultado = []

    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        global fin
        Ventana.__init__(self, 'consulta_pedidos_clientes.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin,
                       'b_exportar/clicked': self.exportar}
        self.add_connections(connections)
        utils.rellenar_lista(self.wids['cmbe_cliente'], [(c.id, c.nombre) for c in pclases.Cliente.select(orderBy='nombre')])
        cols = (('Código', 'gobject.TYPE_STRING', False, True, False, None),
                ('Descripción', 'gobject.TYPE_STRING', False,True,False,None),
                ('Precio s/IVA', 'gobject.TYPE_STRING', False,True,False,None),
                ('ID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(self.wids['tv_datos'], cols)
        col = self.wids['tv_datos'].get_column(2)
        for cell in col.get_cell_renderers():
            cell.set_property("xalign", 1)
        self.wids['tv_datos'].connect("row-activated", self.abrir_producto)
        temp = time.localtime()
        self.fin = str(temp[0])+'/'+str(temp[1])+'/'+str(temp[2])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        if objeto != None:
            utils.combo_set_from_db(self.wids["cmbe_cliente"], objeto.id)
            self.wids["b_buscar"].clicked()
        self.wids['hbox4'].set_property("visible", False)
        self.wids['ventana'].set_title("Productos facturados al cliente")
        gtk.main()

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        import sys, os
        sys.path.append(os.path.join("..", "informes"))
        from treeview2csv import treeview2csv
        from informes import abrir_csv
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
                    import productos_de_venta_rollos
                    ventana_producto = productos_de_venta_rollos.ProductosDeVentaRollos(producto, usuario = self.usuario)
                elif producto.es_bala() or producto.es_bigbag():
                    import productos_de_venta_balas
                    ventana_producto = productos_de_venta_balas.ProductosDeVentaBalas(producto, usuario = self.usuario)
            elif "PC" in idproducto:
                producto = pclases.ProductoCompra.get(idproducto.split(":")[1])
                import productos_compra
                ventana_producto = productos_compra.ProductosCompra(producto, usuario = self.usuario)
        except Exception, e:
            utils.dialogo_info(titulo = "ERROR RECUPERANDO PRODUCTO",
                               texto = "El producto ID %d no se ha encontrado."
                               "\n\n"
                               "Compruebe que no haya sido eliminado recargando"
                               " la consulta y vuelva a intentarlo."
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
        idcliente = utils.combo_get_value(self.wids['cmbe_cliente'])
        if idcliente != None:
            cliente = pclases.Cliente.get(idcliente)
            tarifa = cliente.tarifa
            for i in items:
                if tarifa:
                    precio_tarifa = tarifa.obtener_precio(i, 
                                                          sincronizar = True)
                else:
                    precio_tarifa = i.precioDefecto
                model.append((i.codigo,
                              i.descripcion,
                              utils.float2str(precio_tarifa),
                              i.get_puid()))

    def set_inicio(self, boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
        self.inicio = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])

    def set_fin(self, boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.fin = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])

    def buscar(self, boton):
        """
        Dadas fecha de inicio y de fin, lista todos los albaranes
        pendientes de facturar.
        """
        idcliente = utils.combo_get_value(self.wids['cmbe_cliente'])
        if idcliente == None:
            utils.dialogo_info(titulo = 'ERROR',
                               texto = 'Seleccione un cliente',
                               padre = self.wids['ventana'])
        else:
            idcliente = utils.combo_get_value(self.wids['cmbe_cliente'])
            self.cliente = pclases.Cliente.get(idcliente)
            cliente = self.cliente
            if not self.inicio:
                facturas = pclases.FacturaVenta.select(pclases.AND(
                                pclases.FacturaVenta.q.clienteID == cliente.id, 
                                pclases.FacturaVenta.q.fecha <= self.fin), 
                            orderBy = 'fecha')
            else:
                facturas = pclases.FacturaVenta.select(pclases.AND(
                                pclases.FacturaVenta.q.fecha >= self.inicio,
                                pclases.FacturaVenta.q.fecha <= self.fin,
                                pclases.FacturaVenta.q.clienteID == cliente.id),
                            orderBy='fecha')
            productos = []
            for f in facturas:
                for ldv in f.lineasDeVenta:
                    producto = ldv.producto
                    if producto not in productos:
                        productos.append(producto)
            self.rellenar_tabla(productos)

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        import sys, os
        sys.path.append(os.path.join("..", "informes"))
        from treeview2pdf import treeview2pdf
        from informes import abrir_pdf
        idcliente = utils.combo_get_value(self.wids['cmbe_cliente'])
        if idcliente == None:
            utils.dialogo_info(titulo = 'ERROR',
                               texto = 'Seleccione un cliente',
                               padre = self.wids['ventana'])
        else:
            idcliente = utils.combo_get_value(self.wids['cmbe_cliente'])
            self.cliente = pclases.Cliente.get(idcliente)
            cliente = self.cliente
            if not self.inicio:            
                fechaInforme = 'Hasta ' + utils.str_fecha(time.strptime(self.fin, "%Y/%m/%d"))
            else:
                fechaInforme = utils.str_fecha(time.strptime(self.inicio, "%Y/%m/%d")) + ' - ' + utils.str_fecha(time.strptime(self.fin, "%Y/%m/%d"))
        
            strfecha = fechaInforme
            informe = treeview2pdf(self.wids['tv_datos'], 
                        titulo = "Productos comprados por " + cliente.nombre, 
                        fecha = strfecha) 
            if informe:
                abrir_pdf(informe)

if __name__ == '__main__':
    t = ConsultaProductosComprados()

