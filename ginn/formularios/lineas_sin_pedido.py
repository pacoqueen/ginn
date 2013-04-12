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
## lineas_sin_pedido.py -- 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 14 de septiembre de 2005 -> Inicio
## 20 de septiembre de 2005 -> Funciones genéricas comunes.
## 23 de septiembre de 2005 -> Cambios menores
## 14 de octubre de 2005 -> Añadida confirmación al salir.
## 18 de octubre de 2005 -> Importo el módulo "time".
## 18 de octubre de 2005 -> Vuelvo a conectar "ventana/destroy" a 
##   gtk.main_quit. No termina de funcionar con el callback salir.
## 24 de octubre de 2005 -> Minor bugfix con un resultados.count en
##   vez de resultados.count() que llevaba tiempo arrastrando.
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, time
from framework import pclases
import mx.DateTime

class LineasDeVentaSinPedido(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'lineas_sin_pedido.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_agregar/clicked': self.crear_nuevo_pedido,
                       'b_borrar/clicked': self.eliminar_linea_sin_pedido,
                       'b_modificar/clicked': self.agregar_a_pedido}
        self.add_connections(connections)
        cols = [('Nombre','gobject.TYPE_STRING',False,True,False,None),
                ('Descripción','gobject.TYPE_STRING',False,True,False,None),
                ('Cantidad','gobject.TYPE_DOUBLE',False,True,False,None),
                ('Fecha Hora','gobject.TYPE_STRING',False,True,False,None),
                ('Albarán', 'gobject.TYPE_STRING', False, True, False, None),
                ('Factura', 'gobject.TYPE_STRING', False, True, False, None),
                ('Idlinea_sin_pedido','gobject.TYPE_INT64',False,False,False,None)]
        if pclases.Ticket.select().count():
            cols.insert(-2, ('Ticket', 'gobject.TYPE_STRING', False, True, False, None))
        utils.preparar_listview(self.wids['tv_tipos'], cols)
        self.rellenar_tabla()
        gtk.main()


    def chequear_cambios(self):
        pass

    def rellenar_tabla(self):
    	"""
        Rellena el model con los linea_sin_pedidoes existentes
        """        
        tipos = pclases.LineaDeVenta.select(pclases.LineaDeVenta.q.pedidoVentaID == None)
    	model = self.wids['tv_tipos'].get_model()
    	model.clear()
    	for t in tipos:
            row = [hasattr(t.producto, "nombre") and t.producto.nombre or t.producto.descripcion,
                   t.producto.descripcion,
                   t.cantidad,
                   utils.str_fecha(t.fechahora),
                   t.albaranSalida and t.albaranSalida.numalbaran or '-',
                   (t.facturaVenta and t.facturaVenta.numfactura) or (t.prefactura and t.prefactura.numfactura) or '-',
                   t.id]
            if pclases.Ticket.select().count():
                row.insert(-2, t.ticket and t.ticket.numticket or "-")
            model.append(row)
    
    
    def eliminar_linea_sin_pedido(self,widget):
        model, itr = self.wids['tv_tipos'].get_selection().get_selected()
        if itr != None:
            idtipo = model[itr][-1]
            linea_sin_pedido = pclases.LineaDeVenta.get(idtipo)
        else:        
            utils.dialogo_info('ERROR','Seleccione linea a eliminar')
            return
        ok = linea_sin_pedido.eliminar()
        if (ok > 0):
            utils.dialogo_info('ERROR','No se ha podido eliminar. Existen '+ok+' operaciones con esta linea.')
        self.rellenar_tabla()
    
    def agregar_a_pedido(self, widget):
        """
        Asigna la linea sin pedido a un pedido ya creado
        """
        model, itr = self.wids['tv_tipos'].get_selection().get_selected()
        if itr != None:
            idtipo = model[itr][-1]
            linea_sin_pedido = pclases.LineaDeVenta.get(idtipo)
        else:
            utils.dialogo_info('ERROR','Seleccione una línea para asignarla al pedido')
            return

        numpedido = utils.dialogo_entrada(titulo = 'NÚMERO DE PEDIDO', texto = 'Introduzca el número del pedido al que desea añadir la línea seleccionada')
        pedido = self.buscar_pedido(numpedido)
        if pedido == None:
            utils.dialogo_info(texto = 'No se encontró ningún pedido con ese número', titulo = 'ERROR')
            return
        linea_sin_pedido.pedidoVenta = pedido
        ldc = pclases.LineaDePedido(presupuesto = None, 
                                    pedidoVenta = pedido,
                                    productoVenta = linea_sin_pedido.productoVenta,
                                    productoCompra = linea_sin_pedido.productoCompra, 
                                    fechahora = mx.DateTime.localtime(), 
                                    cantidad = linea_sin_pedido.cantidad, 
                                    precio = linea_sin_pedido.precio, 
                                    descuento = linea_sin_pedido.descuento, 
                                    fechaEntrega = None, 
                                    textoEntrega='')
        pclases.Auditoria.nuevo(ldc, self.usuario, __file__)
        self.rellenar_tabla()
        import pedidos_de_venta
        pedidos_de_venta.PedidosDeVenta(objeto = pedido, usuario = self.usuario)
    
    
    def crear_nuevo_pedido(self, widget):
        """
        Asigna la linea sin pedido a un pedido a crear
        """
        model, itr = self.wids['tv_tipos'].get_selection().get_selected()
        if itr != None:
            idtipo = model[itr][-1]
            linea_sin_pedido = pclases.LineaDeVenta.get(idtipo)
        else:
            utils.dialogo_info('ERROR','Seleccione una línea para asignarla al pedido', padre = self.wids['ventana'])
            return
        numpedido = utils.dialogo_entrada(titulo = 'NÚMERO DE PEDIDO', texto = 'Introduzca el número del pedido que desea crear', padre = self.wids['ventana'])
        if numpedido != None:
            try:
                pclases.PedidoVenta.select(pclases.PedidoVenta.q.numpedido == numpedido)[0]
                utils.dialogo_info(titulo = 'ERROR', texto = 'No se pudo crear el nuevo pedido. Ya existe un pedido con ese número.', padre = self.wids['ventana'])
                return
            except:
                if linea_sin_pedido.facturaVenta != None:
                    pedido = pclases.PedidoVenta(cliente = linea_sin_pedido.facturaVenta.cliente, numpedido = numpedido, fecha = mx.DateTime.localtime())
                    pclases.Auditoria.nuevo(pedido, self.usuario, __file__)
                elif linea_sin_pedido.prefactura != None:
                    pedido = pclases.PedidoVenta(cliente = linea_sin_pedido.prefactura.cliente, numpedido = numpedido, fecha = mx.DateTime.localtime())
                    pclases.Auditoria.nuevo(pedido, self.usuario, __file__)
                elif linea_sin_pedido.albaranSalida != None:
                    pedido = pclases.PedidoVenta(cliente = linea_sin_pedido.albaranSalida.cliente, numpedido = numpedido, fecha = mx.DateTime.localtime())
                    pclases.Auditoria.nuevo(pedido, self.usuario, __file__)
                else:
                    utils.dialogo_info(titulo='INFO',texto='La línea seleccionada no tiene ni albarán ni factura asociada.\nPor lo que para crear el pedido deber introducir un cliente', padre = self.wids['ventana'])
                    clientes = []
                    for c in pclases.Cliente.select(orderBy = "nombre"):
                        clientes.append((c.id,c.nombre))
                    cliente = utils.dialogo_combo(titulo = 'Seleccione cliente',texto = 'Seleccione el cliente para el pedido creado para la línea', ops = clientes)
                    if cliente != None:
                        pedido = pclases.PedidoVenta(cliente = cliente, numpedido = numpedido)
                        pclases.Auditoria.nuevo(pedido, self.usuario, __file__)
                    else:
                        utils.dialogo_info(titulo = 'ERROR', texto= 'No se creó el pedido', padre = self.wids['ventana'])
                        return
            linea_sin_pedido.pedidoVenta = pedido
            ldc = pclases.LineaDePedido(presupuesto = None, 
                                        pedidoVenta = pedido,
                                        productoVenta = linea_sin_pedido.productoVenta,
                                        productoCompra = linea_sin_pedido.productoCompra, 
                                        fechahora = mx.DateTime.localtime(), 
                                        cantidad = linea_sin_pedido.cantidad, 
                                        precio = linea_sin_pedido.precio, 
                                        descuento = linea_sin_pedido.descuento, 
                                        fechaEntrega = None, 
                                        textoEntrega='')
            pclases.Auditoria.nuevo(ldc, self.usuario, __file__)
            self.rellenar_tabla()
            import pedidos_de_venta
            pedidos_de_venta.PedidosDeVenta(objeto = pedido, usuario = self.usuario)
 
    def buscar_pedido(self, numero):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        if numero != None:
            resultados = pclases.PedidoVenta.select(pclases.PedidoVenta.q.numpedido.contains(numero))
            if resultados.count() > 1:
                    ## Refinar los resultados
                    idpedido = self.refinar_resultados_busqueda(resultados)
                    if idpedido == None:
                        return
                    resultados = [pclases.PedidoVenta.get(idpedido)]
                    # Se supone que la comprensión de listas es más rápida que hacer un nuevo get a SQLObject.
                    # Me quedo con una lista de resultados de un único objeto ocupando la primera posición.
                    # (Más abajo será cuando se cambie realmente el objeto actual por este resultado.)
            elif resultados.count() < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info('SIN RESULTADOS', 'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.\n(Atención: Ver la lista completa puede resultar lento si el número de elementos es muy alto)', padre = self.wids['ventana'])
                return
            ## Un único resultado
            return resultados[0]
        else:
            return None

    def refinar_resultados_busqueda(self, resultados):
        """
        Muestra en una ventana de resultados todos los
        registros de "resultados".
        Devuelve el id (primera columna de la ventana
        de resultados) de la fila seleccionada o None
        si se canceló.
        """
        filas_res = []
        for r in resultados:
            filas_res.append((r.id, r.numpedido, utils.str_fecha(r.fecha), r.get_nombre_cliente()))
        idpedido = utils.dialogo_resultado(filas_res,
                                           titulo = 'Seleccione pedido',
                                           cabeceras = ('ID', 'Número de pedido', 'Fecha', 'Cliente'))
        if idpedido < 0:
            return None
        else:
            return idpedido

  
    
if __name__ == '__main__':
    t = LineasDeVentaSinPedido()    
