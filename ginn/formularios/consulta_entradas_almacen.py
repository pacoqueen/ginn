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
## consulta_entradas_almacen.py - Valoración de entradas.
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 19 de julio de 2006 -> Inicio
## 
###################################################################
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sqlobject
import sys
from framework import pclases
import mx.DateTime
import geninformes
import re
import ventana_progreso
from utils import _float as float


class ConsultaEntradasAlmacen(Ventana):
    inicio = None
    fin = None
    resultados = []
        
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        global fin
        Ventana.__init__(self, 'consulta_entradas_almacen.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_producto/clicked': self.buscar_producto,
                       'b_fecha_fin/clicked': self.set_fin}
        self.add_connections(connections)
        utils.rellenar_lista(self.wids['cmbe_proveedor'], [(c.id, c.nombre) for c in pclases.Proveedor.select(orderBy='nombre')])

        cols = (('Proveedor', 'gobject.TYPE_STRING', False, True, False, None),
                ('Albarán', 'gobject.TYPE_STRING', False, True, True, None),
                ('Fecha', 'gobject.TYPE_STRING', False, True, False, None),
                ('Producto', 'gobject.TYPE_STRING', False, True, True, None),
                ('Cantidad', 'gobject.TYPE_FLOAT', False, True, False, None),
                ('Precio', 'gobject.TYPE_FLOAT', False, True, False, None),
                ('Subtotal', 'gobject.TYPE_FLOAT', False, True, False, None),
                ('idldc','gobject.TYPE_STRING',False,False,False,None))
        utils.preparar_listview(self.wids['tv_datos'], cols)
        for ncol in (4, 5, 6):
            col = self.wids['tv_datos'].get_column(ncol)
            for cell in col.get_cell_renderers():
                cell.set_property("xalign", 1)
        temp = time.localtime()
        self.fin = mx.DateTime.DateTimeFrom(day = temp[2], month = temp[1], year = temp[0])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.producto = None
        gtk.main()

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, items):
    	"""
        Rellena el model con los items de la consulta (objetos LDC).
        """        
    	model = self.wids['tv_datos'].get_model()
    	model.clear()
        self.wids['tv_datos'].freeze_child_notify()
        self.wids['tv_datos'].set_model(None)
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        i = 0.0
        try:
            tot = len(items)
        except TypeError:   # len() of unsized object. Es un SelectResults
            tot = items.count()
        total = 0
        # Albarán tienen todas las LDC porque las LDC se han obtenido a partir de albaranes.
    	for ldc in items:
            i+=1
            vpro.set_valor(i/tot, 'Mostrando %d...' % (ldc.id))
            subtotal = ldc.cantidad * ldc.precio
            model.append((ldc.nombre_proveedor,
                          ldc.albaranEntrada.numalbaran,
                          utils.str_fecha(ldc.albaranEntrada.fecha),
                          ldc.descripcion_productoCompra,
                          ldc.cantidad,
                          ldc.precio,
                          subtotal,
                          ldc.id))
            total += subtotal
        self.wids['tv_datos'].set_model(model)
        self.wids['tv_datos'].thaw_child_notify()
        vpro.ocultar()
        self.wids['e_total'].set_text("%s €" % utils.float2str(total))
        self.wids['e_entradas'].set_text("%d" % tot)
        
    def set_inicio(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
        self.inicio = mx.DateTime.DateTimeFrom(year = int(temp[2]), month = int(temp[1]), day = (temp[0]))


    def set_fin(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.fin = mx.DateTime.DateTimeFrom(year = int(temp[2]), month = int(temp[1]), day = (temp[0]))

    def buscar(self,boton):
        """
        Dadas fecha de inicio y de fin, lista todos los albaranes
        pendientes de facturar.
        """
        # Filtro por fecha y proveedor:
        idproveedor = utils.combo_get_value(self.wids['cmbe_proveedor'])
        AE = pclases.AlbaranEntrada
        if not self.inicio:
            if idproveedor == None: 
                albaranes = AE.select(AE.q.fecha <= self.fin, orderBy = 'fecha')
            else:
                albaranes = AE.select(pclases.AND(AE.q.fecha <= self.fin, AE.q.proveedorID == idproveedor), 
                                      orderBy = 'fecha')
        else:
            if idproveedor == None: 
                albaranes = AE.select(pclases.AND(AE.q.fecha >= self.inicio, AE.q.fecha <= self.fin), 
                                      orderBy='fecha')
            else:
                albaranes = AE.select(pclases.AND(AE.q.fecha >= self.inicio, 
                                                  AE.q.fecha <= self.fin, 
                                                  AE.q.proveedorID == idproveedor), 
                                      orderBy='fecha')
        # Filtro por producto:
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        i = 0.0
        tot = albaranes.count()
        self.resultados = []
        for a in albaranes:
            i+=1
            vpro.set_valor(i/tot, "Analizando entradas%s..." \
                % (a.numalbaran != None and a.numalbaran != "" and " [%s]" % (a.numalbaran) or ""))
            for ldc in a.lineasDeCompra:
                if self.producto == None or ldc.productoCompra == self.producto:
                    self.resultados.append(ldc)
        vpro.ocultar()
        self.rellenar_tabla(self.resultados)

    def refinar_busqueda_productos(self, resultados):
        filas_res = []
        for r in resultados:
            filas_res.append((r.id, r.codigo, r.descripcion))
        idproducto = utils.dialogo_resultado(filas_res,
                                             titulo = 'Seleccione producto',
                                             cabeceras = ('ID Interno', 'Código', 'Descripción')) 
        if idproducto < 0:
            return None
        else:
            return idproducto
 
    def pedir_producto(self):
        """
        Solicita una descripción de producto, muestra una
        ventana de resultados coincidentes con la 
        búsqueda de ese código y devuelve un 
        objeto producto seleccionado de entre
        los resultados o None si se cancela o 
        no se encuentra.
        """
        producto = None
        codigo = utils.dialogo_entrada(titulo = 'PRODUCTO', 
                            texto = 'Introduzca descripción del producto.',
                            padre = self.wids['ventana'])
        if codigo == None:  # Ha cancelado
            producto = self.producto
        if codigo != None:
            prods = pclases.ProductoCompra.select(pclases.AND(
                pclases.ProductoCompra.q.descripcion.contains(codigo), 
                pclases.ProductoCompra.q.obsoleto == False))
            prods = [p for p in prods]
            mens_error = 'No se encontró ningún producto con esa descripción.'
            if len(prods) > 1:
                idproducto = self.refinar_busqueda_productos(prods)
                if idproducto != None:
                    prods = [p for p in prods if p.id == idproducto]
                else:
                    return None
            elif len(prods) < 1:
                utils.dialogo_info('CÓDIGO NO ENCONTRADO', mens_error)
                return None
            producto = prods[0]
        return producto

    def buscar_producto(self, boton): 
        self.producto = self.pedir_producto()
        self.wids['e_producto'].set_text(self.producto and self.producto.descripcion or "")

    def por_fecha_ldc(self,e1,e2):
        """
        Función para ordenar líneas de compra por fecha.
        """
        fecha1 = e1.albaranEntrada.fecha
        fecha2 = e2.albaranEntrada.fecha
        if fecha1 < fecha2:
            return -1
        elif fecha1 > fecha2:
            return 1
        else:
            return 0

    def imprimir(self,boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        from ginn.formularios import reports as informes
        datos = []
        total = 0
        self.resultados.sort(self.por_fecha_ldc)
        for ldc in self.resultados:
            subtotal = ldc.cantidad * ldc.precio
            datos.append((ldc.nombre_proveedor,
                          ldc.albaranEntrada.numalbaran,
                          utils.str_fecha(ldc.albaranEntrada.fecha),
                          ldc.descripcion_productoCompra,
                          utils.float2str(ldc.cantidad),
                          utils.float2str(ldc.precio),
                          utils.float2str(subtotal)
                        ))
            total += subtotal
        if len(self.resultados) > 0:
            datos.append(("", "", "", "", "", "", "-"*20))
            datos.append(("", "", "", "", "", "", utils.float2str(total)))
        if (self.inicio) == None:            
            fechaInforme = 'Hasta '+utils.str_fecha(self.fin)
        else:
            fechaInforme = utils.str_fecha(self.inicio)+' - '+utils.str_fecha(self.fin)
        if datos != []:
            informes.abrir_pdf(geninformes.entradasAlmacen(datos,fechaInforme, cols_a_derecha=(4, 5, 6)))


if __name__ == '__main__':
    t = ConsultaEntradasAlmacen()


