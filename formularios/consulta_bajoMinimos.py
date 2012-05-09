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
## consulta_bajoMinimos.py 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 16 de marzo de 2006 -> Inicio
## 3 de agosto de 2006 -> Optimizada consulta para productos de 
##                        venta.
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
    from os.path import join as pathjoin
    sys.path.append(pathjoin("..", "framework"))
    import pclases
import mx
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes
import utils_almacen

class ConsultaBajoMinimos(Ventana):
    
    resultado = []
    
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        global fin
        Ventana.__init__(self, 'consulta_bajoMinimos.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_crear_pedido/clicked': self.crear_pedido, 
                       'b_exportar/clicked': self.exportar}
        self.add_connections(connections)
        cols = (('Código','gobject.TYPE_STRING', False, True, False, None),
                ('Descripción','gobject.TYPE_STRING', False,True,False,None),
                ('Mínimo','gobject.TYPE_FLOAT', False, True, False, None),
                ('Stock','gobject.TYPE_FLOAT', False, True, False, None),
                ('Unidad','gobject.TYPE_STRING', False, True, False, None),
                ('Proveedores habituales', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('idproducto','gobject.TYPE_INT64',False,False,False,None))
        utils.preparar_listview(self.wids['tv_datos'], cols)
        self.wids['tv_datos'].get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        i = 0
        for col in self.wids['tv_datos'].get_columns():
            cells = col.get_cell_renderers()
            for cell in cells:
                col.set_attributes(cell, markup = i)
            i += 1
        if pclases.ProductoVenta.select().count() == 0:
            self.wids['r_venta'].set_sensitive(False)
        proveedores = pclases.Proveedor.select(
                                pclases.Proveedor.q.inhabilitado == False, 
                                orderBy = "nombre")
        proveedores = [(p.id, p.nombre) for p in proveedores]
        proveedores.insert(0, (0, "Todos los proveedores"))
        utils.rellenar_lista(self.wids['cbe_proveedor'], proveedores)
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

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, items, venta):
        """
        Rellena el model con los items de la consulta
        """
        model = self.wids['tv_datos'].get_model()
        model.clear()
        if venta == True:
            for i in items:           
                model.append((i[0].codigo, 
                              i[0].descripcion, 
                              i[0].minimo, 
                              i[1], 
                              "", 
                              "", 
                              i[0].id))
        else:
            for i in items:
                proveedores = []
                for ldc in i.lineasDeCompra:    
                    # Obtengo los proveedores de los albaranes, 
                    # no de los pedidos.
                    if ldc.proveedor != None:
                        nombreproveedor = ldc.proveedor.nombre.replace("&", 
                                                                       "&amp;")
                        if nombreproveedor not in proveedores:
                            proveedores.append(nombreproveedor)
                if not proveedores:
                    # Si aún no hay albaranes, pruebo con los pedidos.
                    for ldpc in i.lineasDePedidoDeCompra:
                        pedido = ldpc.pedidoCompra
                        if pedido:
                            proveedor = pedido.proveedor
                            if proveedor:
                                nombreproveedor = proveedor.nombre.replace(
                                    "&", "&amp;")
                                if nombreproveedor not in proveedores:
                                    proveedores.append(nombreproveedor)
                codigo = i.codigo
                descripcion = i.descripcion
                if i.get_pendientes():
                    codigo='<span background="SpringGreen"><i>%s</i></span>'%(
                        codigo)
                    descripcion = '<span background="SpringGreen"><i>'\
                                  '%s</i></span>' % (descripcion)
                model.append((codigo,
                              descripcion,
                              i.minimo,
                              i.existencias, 
                              i.unidad,
                              ", ".join(proveedores), 
                              i.id))

    def buscar(self,boton):
        """
        Lista los productos bajo mínimos
        """
        self.resultado = []
        if self.wids['r_compra'].get_active():
            proveedorid = utils.combo_get_value(self.wids['cbe_proveedor'])
            if proveedorid == 0 or proveedorid is None:
                proveedor = None
            else:
                proveedor = pclases.Proveedor.get(proveedorid)
            self.wids['b_crear_pedido'].set_sensitive(True)
            if not proveedor:
                self.resultado = pclases.ProductoCompra.select(
                    pclases.AND(
                        pclases.ProductoCompra.q.existencias 
                            < pclases.ProductoCompra.q.minimo, 
                        pclases.ProductoCompra.q.controlExistencias == True, 
                        pclases.ProductoCompra.q.obsoleto == False), 
                        orderBy = 'descripcion')
            else:
                PC = pclases.ProductoCompra
                PDC = pclases.PedidoCompra
                LDPDC = pclases.LineaDePedidoDeCompra
                ADE = pclases.AlbaranEntrada
                FDC = pclases.FacturaCompra
                LDC = pclases.LineaDeCompra
                tiene_pedidos_del_proveedor = pclases.AND(
                    PC.q.id == LDPDC.q.productoCompraID, 
                    LDPDC.q.pedidoCompraID == PDC.q.id, 
                    PDC.q.proveedorID == proveedor.id)
                tiene_albaranes_del_proveedor = pclases.AND(
                    PC.q.id == LDC.q.productoCompraID, 
                    LDC.q.albaranEntradaID == ADE.q.id, 
                    ADE.q.proveedorID == proveedor.id)
                tiene_facturas_del_proveedor = pclases.AND(
                    PC.q.id == LDC.q.productoCompraID, 
                    LDC.q.facturaCompraID == FDC.q.id, 
                    FDC.q.proveedorID == proveedor.id)
                self.resultado0 = PC.select(pclases.AND(
                    PC.q.existencias < PC.q.minimo, 
                    PC.q.controlExistencias == True, 
                    PC.q.obsoleto == False, 
                    tiene_pedidos_del_proveedor, 
                    ))
                self.resultado1 = PC.select(pclases.AND(
                    PC.q.existencias < PC.q.minimo, 
                    PC.q.controlExistencias == True, 
                    PC.q.obsoleto == False, 
                    tiene_albaranes_del_proveedor, 
                    ))
                self.resultado2 = PC.select(pclases.AND(
                    PC.q.existencias < PC.q.minimo, 
                    PC.q.controlExistencias == True, 
                    PC.q.obsoleto == False, 
                    tiene_facturas_del_proveedor
                    ))
                self.resultado = list(self.resultado0)
                self.resultado += [r for r in self.resultado1 
                                   if r not in self.resultado]
                self.resultado += [r for r in self.resultado2 
                                   if r not in self.resultado]
                self.resultado = utils.unificar(self.resultado)
            self.rellenar_tabla(self.resultado, False)
        else:
            self.wids['b_crear_pedido'].set_sensitive(False)
            # NOTA: Se cuenta el mínimo como UNIDADES (bala completa o 
            #       rollo completo), no en kilos ni m².
            productos = pclases.ProductoVenta.select("""
                producto_venta.minimo > (
                    SELECT COUNT(*) 
                    FROM articulo 
                    WHERE articulo.producto_venta_id = producto_venta.id 
                          AND articulo.albaran_salida_id = NULL)""")
            for p in productos:
                articulos_en_almacen = pclases.Articulo.select(
                    pclases.AND(pclases.Articulo.q.productoVentaID == p.id,
                                pclases.Articulo.q.albaranSalidaID == None))
                self.resultado.append((p, articulos_en_almacen.count()))
            self.rellenar_tabla(self.resultado,True)


    def imprimir(self,boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        import informes
        if self.resultado != []:
            datos = []
            if isinstance(self.resultado[0],tuple):
            # Listado de productos de venta
                titulo = 'Productos bajo mínimos'
                for item in self.resultado:
                    datos.append((item[0].codigo,
                                    item[0].descripcion,
                                    item[0].minimo,
                                    item[1]))

            else:
            # Listado de productos de compra (materiales)
                titulo = 'Materiales bajo mínimos'
                for item in self.resultado:
                    datos.append((item.codigo,
                                 item.descripcion,
                                 item.minimo,
                                 item.existencias))
            informes.abrir_pdf(geninformes.bajoMinimos(
                                titulo, 
                                datos, 
                                utils.str_fecha(time.localtime()), 
                                self.wids['cbe_proveedor'].child.get_text()))

    def crear_pedido(self, boton):
        """
        Crea un pedido de faltas con los productos de compra seleccionados.
        """
        model, paths=self.wids['tv_datos'].get_selection().get_selected_rows()
        if paths == None or paths == []:
            utils.dialogo_info(titulo = "SIN SELECCIÓN", 
                               texto="Debe seleccionar al menos un producto.", 
                               padre = self.wids['ventana'])
        else:
            ultimonumpedido = utils_almacen.ultimo_pedido_de_compra_mas_uno()
            numpedido = utils.dialogo_entrada(titulo = 'NÚMERO DE PEDIDO', 
                            texto = 'Número de pedido: Introduzca el número '
                                    'de pedido.\nPor defecto será %d.' % (
                                        ultimonumpedido),
                            valor_por_defecto = str(ultimonumpedido),
                                              padre = self.wids['ventana'])
            if numpedido != None:
                peds = pclases.PedidoCompra.select(
                    """date_part('year', fecha) = %d AND numpedido = '%s'""" 
                        % (mx.DateTime.localtime().year, numpedido))
                if peds.count() > 0:
                    utils.dialogo_info(titulo = "DUPLICADO", 
                        texto = "Número de pedido duplicado. Use otro.", 
                        padre = self.wids['ventana'])
                else:
                    proveedor = get_proveedor_productos(
                        [pclases.ProductoCompra.get(model[path][-1]) 
                         for path in paths])
                    pedido=pclases.PedidoCompra(proveedor = proveedor, 
                                                fecha = time.localtime(), 
                                                numpedido = numpedido, 
                                                descuento = 0,
                                                iva = 0.18, 
                                                cerrado = False) 
                    for path in paths:
                        id = model[path][-1]
                        ldp=pclases.LineaDePedidoDeCompra(pedidoCompra=pedido,
                                cantidad = model[path][2] - model[path][3],
                                precio = 0,
                                productoCompraID = id,
                                descuento = 0,
                                fechaEntrega = None, 
                                textoEntrega = None, 
                                notas = "Creado a partir de la consulta de "
                                        "faltas.")
                    import pedidos_de_compra
                    ventana_pedido = pedidos_de_compra.PedidosDeCompra(pedido)


def get_proveedor_productos(productos):
    """
    Intenta encontrar un proveedor común para todos los 
    productos recibidos.
    Si no puede, devuelve None.
    """
    proveedores = {}
    for p in productos:
        for proveedor in p.proveedores:
            if proveedor not in proveedores:
                proveedores[proveedor] = 1
            else:
                proveedores[proveedor] += 1
    maximo = 0
    mas_repetido = None
    for p in proveedores:
        if proveedores[p] > maximo:
            maximo, mas_repetido = proveedores[p], proveedor
    return mas_repetido

if __name__ == '__main__':
    t = ConsultaBajoMinimos()

