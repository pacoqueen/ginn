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
## formulacion_fibra.py - Formulación HARCODED de la línea de fibra
###################################################################
## NOTAS:
## Ventana hecha a volapié para crear los descuentos predefinidos.
## No permite definir más material para el descuento automático ni 
## cambiar las formulaciones, solo cantidades y productos de compra
## empleados en cada "categoría". 
## ----------------------------------------------------------------
## 
###################################################################
## Changelog:
## 
## 
###################################################################
# 
###################################################################
from ventana import Ventana
from formularios import utils
import re
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
from utils import _float as float
try:
    from psycopg import ProgrammingError as psycopg_ProgrammingError
except ImportError:
    from psycopg2 import ProgrammingError as psycopg_ProgrammingError



class FormulacionFibra(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        Ventana.__init__(self, 'formulacion_fibra.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       '_b_guardar/clicked': self.guardar,
                       'b_ensimaje/clicked': self.buscar_mp,
                       'b_antiuvi/clicked': self.buscar_mp,
                       'b_negro/clicked': self.buscar_mp,
                       'b_titanio/clicked': self.buscar_mp,
                       'b_plasticog/clicked': self.buscar_mp,
                       'b_plasticoe/clicked': self.buscar_mp,
                       'b_flejes/clicked': self.buscar_mp,
                       'b_add_consumo/clicked': self.add_consumo_por_producto, 
                       'b_drop_consumo/clicked': self.drop_consumo_por_producto,
                       'b_cambiar_producto_compra/clicked': 
                            self.cambiar_producto_compra, 
                       'b_add_producto_a_consumo/clicked': 
                            self.add_producto_a_consumo
                      }
        self.add_connections(connections)
        cols = (("Descripción (opcional)", "gobject.TYPE_STRING", 
                    True, True, True, None),
                ("Material", "gobject.TYPE_STRING", False, True, False, None), 
                ("Cantidad", "gobject.TYPE_STRING", 
                    True, True, True, self.cambiar_cantidad), 
                ("Unidad", "gobject.TYPE_STRING", 
                    True, True, True, self.cambiar_unidad), 
                ("ID", "gobject.TYPE_STRING", False, False, False, None))
            # Unidad: Deberá ser algo así como:
            # % para porcentaje del peso.
            # algo/u para descontar m, k o en lo que quiera que se mida el 
            # producto de compra por cada unidad fabricada.
            # algo/kg para descontar m, k o en lo que quiera que se mida el 
            # producto de compra por cada kg (m² en rollos) fabricado.
            # algo/x m para descontar m, k o en lo que quiera que se mida el 
            # producto de compra por cada x metros de ancho de cada 
            # rollo fabricado (sólo para geotextiles y geocompuestos)
        utils.preparar_treeview(self.wids['tv_consumos'], cols, multi = True)
            # En el treeview cada nodo padre será una materia prima con su 
            # descuento y tal. Los nodos hijos contendrán el producto
            # de venta al que se aplica ese descuento automático.
        self.wids['tv_consumos'].connect("row-activated", self.abrir_producto)
        self.comprobar_registro()
        self.rellenar_widgets()
        gtk.main()
    
    def add_producto_a_consumo(self, boton):
        """
        Añade un producto de venta a un consumo existente.
        """
        model, paths = self.wids['tv_consumos'].get_selection().get_selected_rows()
        if paths != []:
            productos = self.pedir_productos_venta()
            if productos:
                for path in paths:
                    if model[path].parent == None:
                        id_consumo = model[path][-1]
                    else:
                        id_consumo = model[path].parent[-1]
                    consumo_adicional_por_producto = pclases.ConsumoAdicional.get(id_consumo)
                    for producto in productos:
                        if producto not in consumo_adicional_por_producto.productosVenta:
                            consumo_adicional_por_producto.addProductoVenta(producto)
                        else:
                            utils.dialogo_info(titulo = "YA EXISTE", 
                                               texto = "El producto %s ya consume según la fórmula de %s.\n\nPulse «Aceptar» para continuar." % (producto.descripcion, consumo_adicional_por_producto.nombre), 
                                               padre = self.wids['ventana'])
                self.rellenar_consumos_adicionales_por_producto()
        else:
            utils.dialogo_info(titulo = "SELECCIONE UN CONSUMO", 
                               texto = "Debe seleccionar un consumo existente.", 
                               padre = self.wids['ventana'])

    def abrir_producto(self, tv, path, view_column):
        """
        Abre el producto de compra si la línea marcada es de 
        consumo y el de venta si es un "contenido" de consumo.
        """
        model = tv.get_model()
        ide = model[path][-1]
        if model[path].parent == None:
            from formularios import productos_compra
            consumo = pclases.ConsumoAdicional.get(ide)
            producto_compra = consumo.productoCompra
            v = productos_compra.ProductosCompra(producto_compra)  # @UnusedVariable
        else:
            from formularios import productos_de_venta_balas
            v = productos_de_venta_balas.ProductosDeVentaBalas(  # @UnusedVariable
                    pclases.ProductoVenta.get(ide))

    def guardar(self, b):
        """
        Guarda los valores para la cantidad en los campos de los registros correspondientes.
        """
        try:
            self.cas['ensimaje'].cantidad = float(self.wids['e_censimaje'].get_text())
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", texto = "Corrija el formato numérico usado y vuelva a intentarlo.")
        try:
            self.cas['antiuvi'].cantidad = float(self.wids['e_cantiuvi'].get_text())
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", texto = "Corrija el formato numérico usado y vuelva a intentarlo.")
        try:
            self.cas['negro'].cantidad = float(self.wids['e_cnegro'].get_text())
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", texto = "Corrija el formato numérico usado y vuelva a intentarlo.")
        try:
            self.cas['titanio'].cantidad = float(self.wids['e_ctitanio'].get_text())
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", texto = "Corrija el formato numérico usado y vuelva a intentarlo.")
        try:
            self.cas['plástico grueso'].cantidad = float(self.wids['e_cplasticog'].get_text())
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", texto = "Corrija el formato numérico usado y vuelva a intentarlo.")
        try:
            self.cas['plástico estirable'].cantidad = float(self.wids['e_cplasticoe'].get_text())
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", texto = "Corrija el formato numérico usado y vuelva a intentarlo.")
        try:
            self.cas['flejes'].cantidad = float(self.wids['e_cflejes'].get_text())
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", texto = "Corrija el formato numérico usado y vuelva a intentarlo.")
        self.rellenar_widgets()

    def rellenar_widgets(self):
        """
        Introduce los valores actuales de la formulación.
        """
        #self.wids['e_censimaje'].set_text('%.5f' % self.cas['ensimaje'].cantidad)
        #self.wids['e_ensimaje'].set_text(self.cas['ensimaje'].productoCompra and self.cas['ensimaje'].productoCompra.descripcion or '')
        #self.wids['e_cantiuvi'].set_text('%.5f' % self.cas['antiuvi'].cantidad)
        #self.wids['e_antiuvi'].set_text(self.cas['antiuvi'].productoCompra and self.cas['antiuvi'].productoCompra.descripcion or '')
        #self.wids['e_cnegro'].set_text('%.5f' % self.cas['negro'].cantidad)
        #self.wids['e_negro'].set_text(self.cas['negro'].productoCompra and self.cas['negro'].productoCompra.descripcion or '')
        #self.wids['e_ctitanio'].set_text('%.5f' % self.cas['titanio'].cantidad)
        #self.wids['e_titanio'].set_text(self.cas['titanio'].productoCompra and self.cas['titanio'].productoCompra.descripcion or '')
        #self.wids['e_cplasticog'].set_text('%.5f' % self.cas['plástico grueso'].cantidad)
        #self.wids['e_plasticog'].set_text(self.cas['plástico grueso'].productoCompra and self.cas['plástico grueso'].productoCompra.descripcion or '')
        #self.wids['e_cplasticoe'].set_text('%.5f' % self.cas['plástico estirable'].cantidad)
        #self.wids['e_plasticoe'].set_text(self.cas['plástico estirable'].productoCompra and self.cas['plástico estirable'].productoCompra.descripcion or '')
        #self.wids['e_cflejes'].set_text('%.5f' % self.cas['flejes'].cantidad)
        #self.wids['e_flejes'].set_text(self.cas['flejes'].productoCompra and self.cas['flejes'].productoCompra.descripcion or '')
        self.rellenar_consumos_adicionales_por_producto()

    def rellenar_consumos_adicionales_por_producto(self):
        """
        Rellena los consumos adicionales específicos por 
        producto fabricado.
        """
        model = self.wids['tv_consumos'].get_model()
        model.clear()
        self.wids['tv_consumos'].freeze_child_notify()
        self.wids['tv_consumos'].set_model(None)
        
        consumos = pclases.ConsumoAdicional.select("""
            id IN (
                SELECT consumo_adicional__producto_venta.consumo_adicional_id 
                  FROM consumo_adicional__producto_venta
                 WHERE producto_venta_id IN (
                                SELECT id 
                                  FROM producto_venta 
                                 WHERE campos_especificos_bala_id IS NOT NULL))
            """, orderBy = "id")
        for consumo in consumos:
            if ((consumo.productoCompra and consumo.productoCompra.obsoleto) 
                or (self.objeto and consumo.formulacion != self.objeto)):
                continue
            padre = model.append(None, 
                                 (consumo.nombre,
                                  consumo.productoCompra 
                                    and consumo.productoCompra.descripcion 
                                    or "-", 
                                  utils.float2str(consumo.cantidad, 5), 
                                  consumo.unidad,
                                  consumo.id))
            for producto in consumo.productosVenta:
                model.append(padre, ("",
                                     producto.descripcion,
                                     "",
                                     "",
                                     producto.id))
        self.wids['tv_consumos'].set_model(model)
        self.wids['tv_consumos'].thaw_child_notify()
        
    def comprobar_registro(self):
        """
        Comprueba si existe el registro de la formulación de la línea
        de fibra y los registros de descuento automático relacionados.
        Si no existen, los crea con valores por defecto.
        """
        try:
            linea = pclases.LineaDeProduccion.select(
                pclases.LineaDeProduccion.q.nombre.contains("de fibra"))[0]
        except:
            utils.dialogo_info(titulo = "ERROR GRAVE", texto = "No se encontró la línea de fibra en la BD.\nCierre la ventana y contacte con el administrador de la aplicación.", padre = self.wids['ventana'])
            return
        self.objeto = linea.formulacion
        if self.objeto == None:
            self.objeto = pclases.Formulacion(nombre = "FIBRA", 
                            observaciones = "Generado automáticamente.")
            pclases.Auditoria.nuevo(self.objeto, self.usuario, __file__)
            linea.formulacion = self.objeto
        nombres_ca_existentes = [ca.nombre for ca 
                                    in self.objeto.consumosAdicionales]
        nombres_ca = {'ensimaje': (0.4, ' %'), 
                      'antiuvi': (0.2, ' %'), 
                      'negro': (2.3, ' %'), 
                      # 'titanio': (0.0, ' %'), 
                      'plástico grueso': (0.355, ' kg / ud'), 
                      'plástico estirable': (0.200, ' kg / ud'), 
                      'flejes': (26.096, ' m / ud'), 
                      'filtro ø 200': (1, ' ud / 200 kg'), 
                      'filtro corona circular': (1, ' ud / 35000 kg'), 
                     }
        self.cas = {}
        for nombre in nombres_ca:
            if nombre not in nombres_ca_existentes:
                ca = pclases.ConsumoAdicional(nombre = nombre,
                                              cantidad = nombres_ca[nombre][0],
                                              unidad = nombres_ca[nombre][1],
                                              formulacionID = self.objeto.id,
                                              productoCompraID = None)
                pclases.Auditoria.nuevo(ca, self.usuario, __file__)
                for productoVenta in pclases.ProductoVenta.select(pclases.ProductoVenta.q.camposEspecificosBalaID != None):
                    if not productoVenta.es_bolsa():
                        # Las bolsas son fibra pero llevan su propia 
                        # formulación, así que me las salto.
                        ca.addProductoVenta(productoVenta)
                self.cas[nombre] = ca
            else:
                self.cas[nombre] = [ca for ca in 
                    self.objeto.consumosAdicionales if ca.nombre == nombre][0]

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
            filas_res.append((r.id, r.codigo, r.descripcion))
        idproducto = utils.dialogo_resultado(filas_res,
                                             titulo = 'Seleccione producto',
                                             cabeceras = ('ID Interno', 'Código', 'Descripción'))
        if idproducto < 0:
            return None
        else:
            return idproducto

    def buscar_producto(self):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se devolverá
        a no ser que se pulse en Cancelar en
        la ventana de resultados, en cuyo caso se deveulve
        None.
        """
        a_buscar = utils.dialogo_entrada("Introduzca código o descripción de producto:") 
        if a_buscar != None:
            try:
                ida_buscar = int(a_buscar)
            except ValueError:
                ida_buscar = -1
            criterio = pclases.OR(
                pclases.ProductoCompra.q.codigo.contains(a_buscar),
                pclases.ProductoCompra.q.descripcion.contains(a_buscar),
                pclases.ProductoCompra.q.id == ida_buscar)
            resultados = pclases.ProductoCompra.select(pclases.AND(
                criterio, 
                pclases.ProductoCompra.q.obsoleto == False, 
                pclases.ProductoCompra.q.controlExistencias == True))
            if resultados.count() > 1:
                ## Refinar los resultados
                idproducto = self.refinar_resultados_busqueda(resultados)
                if idproducto == None:
                    return None
                resultados = [pclases.ProductoCompra.get(idproducto)]
            elif resultados.count() < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info('SIN RESULTADOS', 
                                   'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.\n(Atención: Ver la lista completa puede resultar lento si el número de elementos es muy alto)')
                return None
            ## Un único resultado
            return resultados[0]
        else:
            return "CANCELAR"

    def buscar_mp(self, b):
        """
        Muestra un cuadro de búsqueda de productos de compra.
        Relaciona el seleccionado con el registro correspondiente 
        en función del botón pulsado.
        """
        producto = self.buscar_producto()
        if producto == "CANCELAR":      # Si cancela ANTES del resultado de búsqueda, devuelve la cadena "CANCELAR" y considero
                                        # que es que ha cancelado de verdad. El segundo cancelar, el de resultados de búsqueda 
                                        # (si llega) lo considero como "sin producto en la formulación" (None).
            return
        nombreb = b.name.replace('b_', '')
        trans = {'ensimaje': 'ensimaje',
                 'antiuvi': 'antiuvi',
                 'negro': 'negro',
                 'titanio': 'titanio',
                 'plasticoe': 'plástico estirable',
                 'plasticog': 'plástico grueso',
                 'flejes': 'flejes'}
        nombre = trans[nombreb]
        self.cas[nombre].productoCompra = producto
        self.rellenar_widgets()

    def add_consumo_por_producto(self, boton):
        """
        Añade un consumo automático por producto.
        """
        productos = self.pedir_productos_venta()
        if productos:
            producto_compra = self.pedir_producto_compra()
            if (productos != None and len(productos) > 0 
                and producto_compra != None):
                nombre = self.pedir_nombre()
                if nombre == None:
                    return
                cantidad = self.pedir_cantidad()
                if cantidad == None:
                    return
                unidad = self.pedir_unidad(producto_compra)
                if unidad == None:
                    return
                nuevo_consumo_adicional = pclases.ConsumoAdicional(
                                        formulacionID = self.objeto.id, 
                                        productoCompraID = producto_compra.id, 
                                        nombre = nombre, 
                                        cantidad = cantidad, 
                                        unidad = unidad)
                pclases.Auditoria.nuevo(nuevo_consumo_adicional, self.usuario, 
                                        __file__)
                for producto in productos:
                    nuevo_consumo_adicional.addProductoVenta(producto)
                self.rellenar_consumos_adicionales_por_producto()
    
    def drop_consumo_por_producto(self, boton):
        """
        Elimina el consumo o consumos seleccionados en el TreeView.
        """
        texto = """
        Si ha seleccionado un consumo se eliminará el consumo completo.             
        Si seleccionó uno o varios productos, se eliminarán del consumo al          
        que pertenece, por lo que ya no empleará el material relacionado            
        cuando se fabriquen artículos del mismo.                                    
                                                                                    
        ¿Está seguro de querer continuar?                                           
                                                                                    
        """
        model, paths = self.wids['tv_consumos'].get_selection().get_selected_rows()
        if paths and utils.dialogo(titulo = "¿ELIMINAR?", texto = texto, padre = self.wids['ventana']):
            for path in paths:
                if model[path].parent == None:
                    id_consumo = model[path][-1]
                    consumo_adicional_por_producto = pclases.ConsumoAdicional.get(id_consumo)
                    try:
                        for p in consumo_adicional_por_producto.productosVenta:
                            consumo_adicional_por_producto.removeProductoVenta(p)
                        consumo_adicional_por_producto.destroy(ventana = __file__)
                    except psycopg_ProgrammingError, msg:
                        utils.dialogo_info(titulo = "ERROR: INFORME A LOS DESARROLLADORES", 
                                           texto = "Ocurrió un error al eliminar el consumo.\nDEBUG: Traza de la excepción:\n%s" % (msg), 
                                           padre = self.wids['ventana'])
                else:
                    id_consumo = model[path].parent[-1]
                    idproductov = model[path][-1]
                    consumo_adicional_por_producto = pclases.ConsumoAdicional.get(id_consumo)
                    productov = pclases.ProductoVenta.get(idproductov)
                    consumo_adicional_por_producto.removeProductoVenta(productov)
            self.rellenar_consumos_adicionales_por_producto()

    def cambiar_cantidad(self, cell, path, texto):
        """
        Cambia la cantidad del descuento adicional por producto.
        """
        try:
            cantidad = utils._float(texto)
        except ValueError:
            utils.dialogo_info(titulo = "FORMATO INCORRECTO", 
                               texto = "El texto %s no es válido." % (texto), 
                               padre = self.wids['ventana'])
            return
        model = self.wids['tv_consumos'].get_model()
        if model[path].parent == None:
            idconsumo = model[path][-1]
            consumo = pclases.ConsumoAdicional.get(idconsumo)
            consumo.cantidad = cantidad
        self.rellenar_consumos_adicionales_por_producto()

    def cambiar_unidad(self, cell, path, texto):
        """
        Cambia la unidad de descuento para el descuento adicional por producto
        """
        model = self.wids['tv_consumos'].get_model()
        if model[path].parent == None:
            idconsumo = model[path][-1]
            consumo = pclases.ConsumoAdicional.get(idconsumo)
            if comprobar_unidad(texto, consumo.cantidad):
                consumo.unidad = texto
        self.rellenar_consumos_adicionales_por_producto()
    
    def pedir_producto(self):
        """
        Solicita un código, nombre o descripcicón 
        de producto, muestra una ventana de resultados 
        coincidentes con la búsqueda y devuelve una 
        lista de ids de productos o [] si se cancela o 
        no se encuentra.
        """
        productos = None
        txt = utils.dialogo_entrada(texto = 'Introduzca código, nombre o descripción de producto.', 
                                    titulo = 'BUSCAR PRODUCTO', 
                                    padre = self.wids['ventana'])
        if txt != None:
            criterio = pclases.OR(pclases.ProductoVenta.q.codigo.contains(txt),
                                    pclases.ProductoVenta.q.nombre.contains(txt),
                                    pclases.ProductoVenta.q.descripcion.contains(txt))
            criterio = pclases.AND(criterio, pclases.ProductoVenta.q.camposEspecificosBalaID != None)
            prods = pclases.ProductoVenta.select(criterio)
            productos = [p for p in prods]
        return productos

    def pedir_productos_venta(self):
        """
        Muestra una ventana de búsqueda de un producto y 
        devuelve uno o varios objetos productos dentro de 
        una tupla o None si se cancela.
        """
        productos = self.pedir_producto()
        if productos == None:
            return
        if productos == []:
            utils.dialogo_info(titulo = "NO ENCONTRADO", 
                               texto = "Producto no encontrado", 
                               padre = self.wids['ventana'])
            return
        filas = [(p.id, p.codigo, p.descripcion) for p in productos]
        idsproducto = utils.dialogo_resultado(filas,
                                              titulo = "SELECCIONE UNO O VARIOS PRODUCTOS", 
                                              padre = self.wids['ventana'], 
                                              cabeceras = ("ID", "Código", "Descripción"), 
                                              multi = True)
        if idsproducto and idsproducto!= [-1]:
            return [pclases.ProductoVenta.get(ide) for ide in idsproducto]
        
    def pedir_producto_compra(self):
        """
        Devuelve UN producto de compra obtenido a partir 
        de una búsqueda, etc.
        """
        producto = None
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR MATERIAL", 
                texto = "Introduzca texto a buscar en productos de compra:", 
                padre = self.wids['ventana'])
        if a_buscar != None:
            criterio = pclases.OR(
                pclases.ProductoCompra.q.id.contains(a_buscar),
                pclases.ProductoCompra.q.codigo.contains(a_buscar),
                pclases.ProductoCompra.q.descripcion.contains(a_buscar))
            resultados = pclases.ProductoCompra.select(pclases.AND(
                criterio, 
                pclases.ProductoCompra.q.obsoleto == False))
            if resultados.count() > 1:
                ## Refinar los resultados:
                filas_res = []
                for r in resultados:
                    filas_res.append((r.id, r.codigo, r.descripcion))
                idproducto = utils.dialogo_resultado(filas_res, 
                        titulo = 'Seleccione producto', 
                        cabeceras = ('ID Interno', 'Código', 'Descripción'), 
                        padre = self.wids['ventana'])
                if idproducto < 0:
                    return
                producto = pclases.ProductoCompra.get(idproducto)
                    # id es clave primaria, esta comprensión debería devolver 
                    # un único producto
            elif resultados.count() < 1:
                ## La búsqueda no produjo resultados.
                utils.dialogo_info('SIN RESULTADOS', 
                    'La búsqueda no produjo ningún resultado.\nIntente una '
                    'búsqueda menos restrictiva usando un texto más corto.', 
                    padre = self.wids['ventana'])
                return None
            else:
                producto = resultados[0]
        return producto

    def pedir_nombre(self):
        """
        Pide un texto y lo devuelve. Sin más.
        """
        return utils.dialogo_entrada(titulo = "NOMBRE CONSUMO", 
                                     texto = "Introduzca un nombre identificativo si lo desea:", 
                                     padre = self.wids['ventana'])

    def pedir_cantidad(self):
        """
        Pide una cantidad que debe ser un número float.
        """
        res = utils.dialogo_entrada(titulo = "CANTIDAD", 
                                    texto = "Introduzca la cantidad a consumir del producto de compra (sin unidades):", 
                                    padre = self.wids['ventana'])
        try:
            res = utils._float(res)
        except ValueError:
            utils.dialogo_info(titulo = "CANTIDAD INCORRECTA", 
                               texto = "El texto introducido %s no es correcto." % (res), 
                               padre = self.wids['ventana'])
            res = None
        return res

    def pedir_unidad(self, productoCompra):
        """
        Pide la unidad del descuento y comprueba que sea correcta.
        Recibe el producto de compra para mostrar el valor por defecto.
        """
        txt = """
                                                                                
        Introduzca las unidades para el descuento de materiales.                
                                                                                
        Por ejemplo:                                                            
            %  (porcentaje en las unidades del material                         
                     por peso de producto terminado).                           
            ud / 5 ud   (unidad del material por cada 5 unidades                
                         de producto terminado).                                
            m / kg  (metro de material por kilo de producto).                   
            kg / 5.5 m (kg de material por cada 5.5 metros de producto).        
                                                                                
        NOTA: La unidad del materal que se descuenta debe ser la misma          
              que consta en catálogo, pedidos de compra, etc.                   
                                                                                
        """ 
        defecto = "%s / ud" % (productoCompra.unidad)
        res = utils.dialogo_entrada(titulo = "INTRODUZCA UNIDAD", 
                                    texto = txt, 
                                    padre = self.wids['ventana'], 
                                    valor_por_defecto = defecto)
        if not comprobar_unidad(res):
            utils.dialogo(titulo = "FORMATO INCORRECTO", 
                          texto = "El texto introducido %s no tiene el formato correcto." % (res), 
                          padre = self.wids['ventana'])
            res = None
        return res

    def cambiar_producto_compra(self, boton):
        """
        Cambia el producto que se consume en el registro de 
        consumo adicional seleccionado por otro.
        """
        producto_compra = self.buscar_producto()
        if producto_compra == "CANCELAR":
            return
        sel = self.wids['tv_consumos'].get_selection()
        model, paths = sel.get_selected_rows()
        for path in paths:
            if model[path].parent == None:
                id_consumo = model[path][-1]
            else:
                id_consumo = model[path].parent[-1]
            consumo_adicional_por_producto = pclases.ConsumoAdicional.get(
                id_consumo)
            consumo_adicional_por_producto.productoCompra = producto_compra
        self.rellenar_consumos_adicionales_por_producto()


def comprobar_unidad(txt, cantidadpc = 1.0):
    """
    Comprueba si la unidad de descuento "txt" cumple con 
    alguna de las unidades interpretables por el programa.
    cantidadpc se usa para agregarlo a la parte "unidad" y 
    chequear todo el conjunto en el proceso.
    """
    res = False
    txt = "%s %s" % (utils.float2str(cantidadpc, 5), txt)
    txt = txt.strip()
    # TODO: De momento lo hago así porque no sé de qué modo ni dónde guardarlo:
    regexp_porcentaje = re.compile("^-?\d+[\.,]?\d*\s*%$")
    regexp_fraccion = re.compile("-?\d+[\.,]?\d*\s*\w*\s*/\s*-?\d*[\.,]?\d*\s*\w+")
    if regexp_porcentaje.findall(txt) != []:
        cantidad = parsear_porcentaje(txt)  # @UnusedVariable
        res = True
    elif regexp_fraccion.findall(txt) != []:
        cantidad, unidad, cantidad_pv, unidad_pv = parsear_fraccion(txt)  # @UnusedVariable
        res = True
    return res

def parsear_porcentaje(txt):
    """
    Devuelve la cantidad del porcentaje como fracción de 1.
    """
    regexp_float = re.compile("^-?\d+[\.,]?\d*")
    num = regexp_float.findall(txt)[0]
    return utils._float(num) / 100

def parsear_fraccion(txt):
    """
    Devuelve la cantidad de producto compra y unidad que hay que descontar 
    por cada cantidad de producto venta y unidad (que también se devuelven).
    Es necesario que venga la cantidadpc aunque en el registro, en el campo 
    "unidad" no aparece.
    """
    regexp_float = re.compile("-?\d+[\.,]?\d*")
    regexp_unidad = re.compile("\w+")
    cantidades = regexp_float.findall(txt)
    if len(cantidades) == 1:
        cantidadpc = cantidades[0]
        cantidadpv = '1'
        txt = txt.replace(cantidadpc, "")
    elif len(cantidades) == 2:
        cantidadpc, cantidadpv = cantidades[0:2]
        txt = txt.replace(cantidadpc, "")
        txt = txt.replace(cantidadpv, "")
    else:
        cantidadpc = '1'
        cantidadpv = '1'
    txt = txt.replace("/", "")
    unidadpc, unidadpv = regexp_unidad.findall(txt)[0:2]
    cantidadpc = utils._float(cantidadpc)
    cantidadpv = utils._float(cantidadpv)
    return cantidadpc, unidadpc, cantidadpv, unidadpv



if __name__ == '__main__':
    f = FormulacionFibra()
      
