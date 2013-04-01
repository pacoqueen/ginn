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
## albaranes_de_entrada_repuestos.py - Solo para albaranes de repuestos.
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 12 de diciembre de 2008 -> Proviene de albaranes_de_entrada.py
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, time
try:
    import pclases
except ImportError:
    import sys
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    import pclases
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes
from utils import _float as float


class AlbaranesDeEntradaRepuestos(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'albaranes_de_entrada_repuestos.glade', objeto, usuario = self.usuario)
        connections = {'b_nuevo/clicked': self.crear_nuevo_albaran,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_buscar/clicked': self.buscar_albaran,
                       'b_fecha/clicked': self.buscar_fecha,
                       'b_add_ldv/clicked': self.add_repuesto,
                       'b_drop_ldv/clicked': self.drop_producto,
                       'b_add_pedido/clicked': self.add_pedido,
                       'b_borrar/clicked': self.borrar_albaran,
                       'b_imprimir/clicked': self.imprimir,
                       'b_salir/clicked': self.salir, 
                       'cbe_almacen/changed': self.guardar
                      }
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        gtk.main()

    # --------------- Funciones auxiliares ------------------------------
    def pedir_cantidad(self):
        cant = utils.dialogo_entrada(titulo = '¿CANTIDAD?',
                                     texto = 'Introduzca cantidad', 
                                     valor_por_defecto = '1', 
                                     padre = self.wids['ventana'])
        try:
            cant = float(cant)
        except:
            utils.dialogo_info(titulo = 'ERROR EN CANTIDAD', 
                               texto = 'Cantidad incorrecta.\nAsegúrese de escribirla con punto (.) como separador decimal.\nSe añadirá el producto al albarán, modifique la cantidad directamente ahí.', 
                               padre = self.wids['ventana'])
            cant = 1
        return cant


    def pedir_producto(self):
        """
        Solicita un código de producto, muestra una
        ventana de resultados coincidentes con la 
        búsqueda de ese código y devuelve un 
        objeto producto seleccionado de entre
        los resultados o None si se cancela o 
        no se encuentra.
        """
        producto = None
        codigo = utils.dialogo_entrada(texto = 'Introduzca código o descripción del producto.', 
                                       titulo = 'PRODUCTO', 
                                       padre = self.wids['ventana'])
        if codigo != None:
            prods = pclases.ProductoCompra.select(pclases.AND(pclases.OR(pclases.ProductoCompra.q.descripcion.contains(codigo), 
                                                                         pclases.ProductoCompra.q.codigo.contains(codigo)), 
                                                              pclases.ProductoCompra.q.controlExistencias == True))
            prods = tuple(prods)
            mens_error = 'No se encontró ningún producto con ese código o descripción.'
            if len(prods) > 1:
                idproducto = self.refinar_busqueda_productos(prods)
                if idproducto != None:
                    prods = [pclases.ProductoCompra.get(idproducto)]
                else:
                    return None
            elif len(prods) < 1:
                utils.dialogo_info(titulo = 'CÓDIGO NO ENCONTRADO', 
                                   texto = mens_error, 
                                   padre = self.wids['ventana'])
                return None
            producto = prods[0]
        return producto

    def pedir_pedido(self):
        """
        Solicita un número de pedido, muestra una
        ventana de resultados coincidentes con la 
        búsqueda de ese número y devuelve un 
        objeto pedido seleccionado de entre
        los resultados o None si se cancela o 
        no se encuentra.
        """
        pedido = None
        codigo = utils.dialogo_entrada(texto = 'Introduzca número de pedido.', 
                                       titulo = 'NÚMERO DE PEDIDO', 
                                       padre = self.wids['ventana'])
        if codigo != None:
            if self.objeto.proveedorID == None:
                pedidos = pclases.PedidoCompra.select(pclases.PedidoCompra.q.numpedido.contains(codigo))
            else:
                pedidos = pclases.PedidoCompra.select(pclases.AND(pclases.PedidoCompra.q.numpedido.contains(codigo), 
                                                                  pclases.PedidoCompra.q.proveedorID == self.objeto.proveedorID))
            pedidos = [p for p in pedidos if len(p.get_lineas_sin_albaranear()) > 0] 
            if len(pedidos) > 1:
                idpedido = self.refinar_busqueda_pedidos(pedidos)
                if idpedido != None:
                    # pedidos = [p for p in pedidos if p.id == idpedido]
                    pedidos = [pclases.PedidoCompra.get(idpedido)]
                else:
                    return None
            elif len(pedidos) < 1:
                mens_error = 'No se encontró ningún pedido.'
                utils.dialogo_info(titulo = 'PEDIDO NO ENCONTRADO', 
                                   texto = mens_error, 
                                   padre = self.wids['ventana'])
                return None
            try:
                pedido = pedidos[0]
            except IndexError:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "Ocurrió un error al recuperar la información del pedido.\nCierre y vuelva a abrir la ventana.", 
                                   padre = self.wids['ventana'])
                pedido = None
        return pedido
        
    def refinar_busqueda_productos(self, resultados):
        filas_res = []
        for r in resultados:
            filas_res.append((r.id, r.codigo, r.descripcion))
        idproducto = utils.dialogo_resultado(filas_res,
                                             titulo = 'Seleccione producto',
                                             cabeceras = ('ID Interno', 'Código', 'Descripción'),
                                             padre = self.wids['ventana']) 
        if idproducto < 0:
            return None
        else:
            return idproducto
            
    def refinar_busqueda_pedidos(self, resultados):
        filas_res = []
        for r in resultados:
            if r.proveedor != None:
                proveedor = r.proveedor.nombre
            else:
                proveedor = ''
            filas_res.append((r.id, r.numpedido, utils.str_fecha(r.fecha), proveedor, ))
        idpedido = utils.dialogo_resultado(filas_res,
                                             titulo = 'Seleccione pedido',
                                             cabeceras = ('ID Interno', 'Num. Pedido', 'Fecha', 'Proveedor'),
                                             padre = self.wids['ventana']) 
        if idpedido < 0:
            return None
        else:
            return idpedido
            
    def es_diferente(self):
        """
        Devuelve True si la información en pantalla es distinta a la
        del objeto en memoria.
        """
        # NOTA: No hay que preocuparse por el exceso de cómputo. Estas comparaciones
        # son bastante rápidas al tener python -como los lenguajes de verdad y no
        # los jueguetes tipo VB- las operaciones lógicas cortocircuitadas, de forma
        # que si condición pasa a False no se evalúa lo que esté detrás del and en
        # las instrucciones posteriores.
        albaran = self.objeto
        if albaran == None: return False    # Si no hay albaran activo, devuelvo que no hay cambio respecto a la ventana
        condicion = (str(albaran.numalbaran) == self.wids['e_numalbaran'].get_text())
        condicion = condicion and (utils.str_fecha(albaran.fecha) == self.wids['e_fecha'].get_text())
        condicion = condicion and (utils.combo_get_value(self.wids['cmbe_proveedor']) == albaran.proveedorID) 
        condicion = condicion and (
            utils.combo_get_value(self.wids['cbe_almacen']) 
                == self.objeto.almacenID)
        return not condicion    # "condicion" verifica que sea igual

    def aviso_actualizacion(self):
        """
        Muestra una ventana modal con el mensaje de objeto 
        actualizado.
        """
#        utils.dialogo_info('ACTUALIZAR',
#                           'El albarán ha sido modificado remotamente.\nDebe actualizar la información mostrada en pantalla.\nPulse el botón «Actualizar»', 
#                           padre = self.wids['ventana'])
        self.wids['b_actualizar'].set_sensitive(True)

    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        # Inicialmente no se muestra NADA. Sólo se le deja al
        # usuario la opción de buscar o crear nuevo.
        self.activar_widgets(False)
        self.wids['b_actualizar'].set_sensitive(False)
        self.wids['b_guardar'].set_sensitive(False)
        self.wids['b_nuevo'].set_sensitive(True)
        self.wids['b_buscar'].set_sensitive(True)
        provs = pclases.Proveedor.select(orderBy = 'nombre')
        lista_provs = [(p.id, p.nombre) for p in provs if not p.inhabilitado]
        utils.rellenar_lista(self.wids['cmbe_proveedor'],lista_provs)
        # Inicialización del resto de widgets:
        cols = (('Código', 'gobject.TYPE_STRING', False, True, False, None),
                ('Descripción', 'gobject.TYPE_STRING', False, True, False, None),
                ('Cantidad recibida', 'gobject.TYPE_STRING', True, True, False, self.cambiar_cantidad),
                ('Precio s/IVA', 'gobject.TYPE_STRING', True, True, False, self.cambiar_precio),
                ('IVA', 'gobject.TYPE_STRING', True, True, False, self.cambiar_iva), 
                ('Descuento', 'gobject.TYPE_STRING', True, True, False, self.cambiar_descuento_ldc), 
                ('Total línea', 'gobject.TYPE_STRING', False, True, False, None),
                ('IDProducto', 'gobject.TYPE_INT64', False, False, False, None)
               )
        utils.preparar_listview(self.wids['tv_ldvs'], cols)
        for n in (2, 3):
            for cell in self.wids['tv_ldvs'].get_column(n).get_cell_renderers():
                cell.set_property('xalign', 1.0)
        almacenes = [(a.id, a.nombre) 
                     for a in pclases.Almacen.select(
                         pclases.Almacen.q.activo == True, 
                         orderBy = "id")]
        utils.rellenar_lista(self.wids['cbe_almacen'], 
                             almacenes)

    def cambiar_precio(self, cell, path, texto):
        try:
            precio = float(texto)
        except:
            return
        model = self.wids['tv_ldvs'].get_model()
        ldc = pclases.LineaDeCompra.get(model[path][-1])
        ldc.precio = precio
        self.actualizar_ventana()
    
    def cambiar_iva(self, cell, path, texto):
        try:
            iva = utils.parse_porcentaje(texto, True)
        except:
            utils.dialogo_info(titulo = "ERROR", 
                               texto = "La cantidad %s no es un número válido." % (texto), 
                               padre = self.wids['ventana'])
            return
        model = self.wids['tv_ldvs'].get_model()
        idldc = model[path][-1]
        ldc = pclases.LineaDeCompra.get(idldc)
        ldc.iva = iva
        self.rellenar_widgets()
    
    def cambiar_descuento_ldc(self, cell, path, texto):
        try:
            descuento = utils.parse_porcentaje(texto, True)
        except:
            utils.dialogo_info(titulo = "ERROR", 
                               texto = "La cantidad %s no es un número válido." % (texto), 
                               padre = self.wids['ventana'])
            return
        model = self.wids['tv_ldvs'].get_model()
        idldc = model[path][-1]
        ldc = pclases.LineaDeCompra.get(idldc)
        ldc.descuento = descuento
        self.rellenar_widgets()

    def cambiar_cantidad(self, cell, path, texto):
        """
        Cambia la cantidad de una linea de venta de un albarán de entrada,
        en el caso de que se escriba una cantidad menor de la que estaba en
        el pedido de compra (si es que tenía uno asociado), se desdobla la
        línea de venta original en dos líneas: una con el albarán asociado
        (por lo que deja de estar pendiente) y otra con la cantidad pendiente
        que no queda asociada al albarán. Si en el pedido quedara alguna LDV 
        sin "albaranear" del mismo producto, al mismo precio, etc... esta 
        segunda línea con la cantidad excedente se suma a la del pedido y se 
        elimina, para evitar líneas sueltas de cantidades pequeñas.
        En el caso de que se escriba una cantidad mayor a la que estaba
        originalmente en el pedido se darán dos opciones:
        - Crear una nueva linea de compra sin pedido asociado, con la cantidad
          incrementada.
        - Incrementar la cantidad en la línea de compra del pedido original.
        
        ...

        Bla, bla, bla, bla.
        ¡Hola! Soy Troy McLure. Tal vez me recuerden de otros cambios de requisitos en caliente como
        «cambiemos "en albarán" por "albaraneada"», «vendamos productos de compra sin manufacturar» o 
        «tal vez necesitemos un histórico de existencias»...
        Todo lo de arriba YA NO SIRVE. Ahora, con las nuevas líneas de pedido de compra, la cantidad se 
        aumenta directamente en la línea de compra y santas pascuas.
        """
        try:
            cantidad = float(texto)
        except:
            return
        model = self.wids['tv_ldvs'].get_model()
        try:
            ldc = pclases.LineaDeCompra.get(model[path][-1])
        except pclases.SQLObjectNotFound:
            utils.dialogo_info(titulo = "LÍNEA BORRADA", 
                               texto = "La línea seleccionada fue eliminada desde otro puesto.", 
                               padre = self.wids['ventana'])
        else:
            antigua = ldc.cantidad
            ldc.cantidad = cantidad
            if ldc.productoCompra.controlExistencias:
                # XXX DEBUG
                #print ldc.productoCompra.existencias
                # XXX EODEBUG
                diferencia = cantidad - antigua
                ldc.productoCompra.sync() 
                ldc.productoCompra.existencias += diferencia 
                ldc.productoCompra.add_existencias(diferencia, 
                                                   almacen=self.objeto.almacen)
                ldc.productoCompra.syncUpdate() 
                ldc.productoCompra.sync() 
                # XXX DEBUG
                #print ldc.productoCompra.existencias
                # XXX EODEBUG
            if ldc.cargaSilo:
                ldc.cargaSilo.cantidad = cantidad
        self.actualizar_ventana()

    def rellenar_tabla(self, tabla):
        """
        Rellena el model con las ldc existentes
        """
        albaran = self.objeto
        if albaran != None:
            lineas = albaran.lineasDeCompra
            try:
                lineas.sort(lambda l1, l2: l1.id - l2.id)
            except:
                pass
            model = self.wids['tv_ldvs'].get_model()
            model.clear()
            for l in lineas:
                model.append((l.productoCompra.codigo,
                              l.productoCompra.descripcion,
                              utils.float2str(l.cantidad, 2),
                              utils.float2str(l.precio, 4, autodec = True),
                              "%s %%" % (utils.float2str(l.iva * 100, 0)),
                              "%s %%" % (utils.float2str(l.descuento * 100, 0)),
                              utils.float2str(l.get_subtotal(iva = True)),
                              l.id))


    def activar_widgets(self, s):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        ws = ('b_add_ldv', 'b_add_pedido', 'b_drop_ldv', 'b_borrar', 
              'e_numalbaran', 'b_fecha', 'tv_ldvs', 'e_fecha', 'cbe_almacen') 
        for w in ws:
            self.wids[w].set_sensitive(s)
        if self.objeto:
            self.wids['cbe_almacen'].set_sensitive(
                not len(self.objeto.lineasDeCompra))

    def ir_a_primero(self):
        """
        Hace que el primer registro -si lo hay- de la tabla implicada
        en el objeto del formulario sea el objeto activo.
        """
        albaran = self.objeto
        try:
            # Anulo el aviso de actualización del envío que deja de ser activo.
            if albaran != None: 
                albaran.notificador.desactivar()
            albaran = pclases.AlbaranEntrada.select(
                pclases.AlbaranEntrada.q.repuestos == True, 
                orderBy = "-id")[0]
                # Selecciono todos los albaranes de compra y me quedo con el primero de la lista.
            albaran.notificador.activar(self.aviso_actualizacion)       # Activo la notificación
        except IndexError:
            albaran = None
        self.objeto = albaran
        self.actualizar_ventana()

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
            filas_res.append((r.id, 
                              r.numalbaran, 
                              utils.str_fecha(r.fecha), 
                              r.proveedor != None and r.proveedor.nombre or ""
                             ))
        idalbaran = utils.dialogo_resultado(filas_res, 
                                            titulo = 'SELECCIONE ALBARÁN', 
                                            cabeceras = ('ID Interno', 'Número de albarán', 'Fecha', 'Proveedor'), 
                                            padre = self.wids['ventana'])
        if idalbaran < 0:
            return None
        else:
            return idalbaran

    def rellenar_widgets(self):
        """
        Introduce la información del albaran actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        albaran = self.objeto
        self.wids['e_numalbaran'].set_text(albaran.numalbaran)
        self.wids['e_fecha'].set_text(utils.str_fecha(albaran.fecha))
        self.rellenar_tabla(self.wids['tv_ldvs'])
        if albaran.proveedorID == None:
            self.wids['cmbe_proveedor'].set_active(-1)
            self.wids['cmbe_proveedor'].child.set_text("")
        else:
            utils.combo_set_from_db(self.wids['cmbe_proveedor'], albaran.proveedorID)
        self.wids['e_facturas'].set_text(", ".join([f.numfactura for f in albaran.facturasCompra]))
        self.wids['e_pedidos'].set_text(", ".join([p.numpedido for p in albaran.pedidosCompra]))
        self.suspender(self.wids['cbe_almacen'])
        utils.combo_set_from_db(self.wids['cbe_almacen'], 
                                self.objeto.almacenID, 
                                forced_value = self.objeto.almacen 
                                    and self.objeto.almacen.nombre or None)
        self.revivir(self.wids['cbe_almacen'])
        self.objeto.make_swap()

    def add_repuesto(self, widget):
        """
        Añade un producto al pedido pero a través de dos diálogos que filtran 
        los productos para elegir únicamente repuestos.
        Si en el segundo diálogo se introduce un texto que no es un producto 
        de los filtrados, se pregunta si crearlo nuevo o no.
        """
        albaran = self.objeto
        producto = utils.pedir_repuesto(self.wids['ventana'], 
            proveedor_defecto = self.objeto.proveedor, 
            usuario = self.usuario)
        if producto == None:
            return
        cantidad = self.pedir_cantidad()
        try:
            iva = producto.proveedores[0].iva
        except (IndexError, AttributeError):
            iva = 0.21
        linea = pclases.LineaDeCompra(productoCompra = producto,
                                      cantidad = cantidad,
                                      albaranEntrada = albaran,
                                      pedidoCompra = None,
                                      facturaCompra = None, 
                                      iva = iva, 
                                      precio = producto.preciopordefecto)
        pclases.Auditoria.nuevo(linea, self.usuario, __file__)
        if linea.productoCompra.controlExistencias: 
            # XXX DEBUG
            #print linea.productoCompra.existencias
            # XXX EODEBUG
            linea.productoCompra.sync() 
            linea.productoCompra.existencias += cantidad
            linea.productoCompra.add_existencias(cantidad, 
                                                 almacen=self.objeto.almacen)
            linea.productoCompra.syncUpdate() 
            linea.productoCompra.sync() 
            # XXX DEBUG
            #print linea.productoCompra.existencias
            # XXX EODEBUG
        self.actualizar_ventana()

    def drop_producto(self, widget):
        if self.wids['tv_ldvs'].get_selection().count_selected_rows() != 1: return
        model, itr = self.wids['tv_ldvs'].get_selection().get_selected()
        idlinea = model[itr][-1]
        try:
            linea = pclases.LineaDeCompra.get(idlinea)
        except pclases.SQLObjectNotFound:
            utils.dialogo_info(titulo = "LÍNEA BORRADA", 
                               texto = "La línea seleccionada ya fue eliminada desde otro puesto.", 
                               padre = self.wids['ventana'])
        else:
            if linea.siloID != None:
                utils.dialogo_info(titulo = "LÍNEA CON CARGA EN SILO", 
                    texto = 'Cancele primero la carga del silo (seleccionando'
                            ' "Sin carga" en\nla columna correspondiente) y v'
                            'uelva a intentar eliminar la línea.', 
                    padre = self.wids['ventana'])
                return
            producto = linea.productoCompra
            if linea.productoCompra.controlExistencias: 
                # XXX DEBUG
                #print linea.productoCompra.existencias
                # XXX EODEBUG
                producto.sync() 
                producto.existencias -= linea.cantidad
                producto.add_existencias(-linea.cantidad, 
                                                   almacen=self.objeto.almacen)
                if producto.existencias < 0:
                    producto.existencias = 0
                    # En este caso, si la cantidad absoluta de existencias es 
                    # cero, como debería ser un campo calculado pongo a cero 
                    # las existencias de todos los almacenes para ese producto 
                    # (pues ese debería ser el origen del cálculo).
                    for sa in producto.stocksAlmacen:
                        sa.existencias = 0
                        sa.syncUpdate()
                producto.syncUpdate() 
                producto.sync() 
                # XXX DEBUG
                #print linea.productoCompra.existencias
                # XXX EODEBUG
            if linea.facturaCompraID == None:
                linea.destroy(ventana = __file__)
            else:
                linea.albaranEntrada = None
        self.actualizar_ventana()

    def add_pedido(self, widget):
        albaran = self.objeto
        if albaran != None:
            pedido = self.pedir_pedido()
            if pedido == None:
                return
            if albaran.proveedor == None:
                albaran.proveedor = pedido.proveedor
            elif albaran.proveedor != pedido.proveedor:
                utils.dialogo_info(titulo = "ERROR EN PROVEEDOR", 
                                   texto = "El proveedor del pedido no coincide con el del albarán.", 
                                   padre = self.wids['ventana'])
                return
            if pedido.cerrado:
                utils.dialogo_info(titulo = "PEDIDO CERRADO", 
                                   texto = "El pedido ha sido cerrado. No puede efectuar entradas sobre el mismo.", 
                                   padre = self.wids['ventana'])
                return
            lineas = [ldpc for ldpc in pedido.lineasDePedidoDeCompra if ldpc.cantidadPendiente > 0]
            for l in lineas:
                iva = l.pedidoCompra.iva
                ldc = pclases.LineaDeCompra(pedidoCompra = l.pedidoCompra,
                                            productoCompra = l.productoCompra,
                                            albaranEntrada = self.objeto,
                                            cantidad = l.cantidadPendiente,
                                            precio = l.precio,
                                            descuento = l.descuento,
                                            facturaCompra = None, 
                                            iva = iva)
                pclases.Auditoria.nuevo(ldc, self.usuario, __file__)
                if ldc.productoCompra.controlExistencias: 
                    # XXX DEBUG
                    #print ldc.productoCompra.existencias
                    # XXX EODEBUG
                    ldc.productoCompra.sync()
                    #print ldc.cantidad
                    ldc.productoCompra.existencias += ldc.cantidad
                    ldc.productoCompra.add_existencias(ldc.cantidad, 
                                                   almacen=self.objeto.almacen)
                    ldc.productoCompra.syncUpdate() 
                    ldc.productoCompra.sync()
                    # XXX DEBUG
                    #print ldc.productoCompra.existencias
                    # XXX EODEBUG
            self.actualizar_ventana()

    # --------------- Manejadores de eventos ----------------------------
    def crear_nuevo_albaran(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        albaran = self.objeto
        global transportista
        transportista = None
            # Datos a pedir:
        numalbaran = utils.dialogo_entrada(texto = 'Introduzca un número para el albarán.', 
                                           titulo = 'NÚMERO DE ALBARÁN', 
                                           padre = self.wids['ventana'])
        if not numalbaran: 
            if numalbaran != None:
                utils.dialogo_info(titulo = "ATENCIÓN", 
                                   texto = "No se permiten albaranes de entrada de repuestos sin número.", 
                                   padre = self.wids['ventana'])
            return
        provs = pclases.Proveedor.select(orderBy = 'nombre')
        lista_provs = [(p.id, p.nombre) for p in provs if not p.inhabilitado]
        idproveedor = utils.dialogo_combo(titulo = "SELECCIONAR PROVEEDOR", 
                                          texto = "Seleccione el proveedor de la factura:", 
                                          ops = lista_provs, 
                                          padre = self.wids['ventana'])
        if idproveedor is None:
            return
        if albaran != None: albaran.notificador.set_func(lambda : None)
        almacenes = [(a.id, a.nombre) 
                     for a in pclases.Almacen.select(
                         pclases.Almacen.q.activo == True, 
                         orderBy = "id")]
        almacenppal = pclases.Almacen.get_almacen_principal_id_or_none()
        almo = utils.dialogo_combo(titulo = "ALMACÉN DESTINO", 
                    texto = "Seleccione el almacén destino de la mercancía",  
                    ops = almacenes, 
                    padre = self.wids['ventana'], 
                    valor_por_defecto = almacenppal)
        if not almo:    # Cancelar
            return
        albaran = pclases.AlbaranEntrada(fecha = time.localtime(),
                                         numalbaran = numalbaran,
                                         proveedorID = idproveedor, 
                                         repuestos = True, 
                                         almacenID = almo)
        pclases.Auditoria.nuevo(albaran, self.usuario, __file__)
        utils.dialogo_info('ALBARÁN CREADO', 
                           'El albarán %s ha sido creado.\nComplete la información asociando entradas al mismo.' % str(albaran.numalbaran),
                           padre = self.wids['ventana'])
        albaran.notificador.set_func(self.aviso_actualizacion)
        self.objeto = albaran
        self.actualizar_ventana()

    def buscar_albaran(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        albaran = self.objeto
        a_buscar = utils.dialogo_entrada(texto = "Introduzca número de albarán", titulo = 'BUSCAR ALBARÁN', padre = self.wids['ventana']) 
        if a_buscar != None:
            resultados = pclases.AlbaranEntrada.select(pclases.AND(
                pclases.AlbaranEntrada.q.numalbaran.contains(a_buscar), 
                pclases.AlbaranEntrada.q.repuestos == True))
            if resultados.count() > 1:
                ## Refinar los resultados
                idalbaran = self.refinar_resultados_busqueda(resultados)
                if idalbaran == None:
                    return
                resultados = [pclases.AlbaranEntrada.get(idalbaran)]
                # Me quedo con una lista de resultados de un único objeto ocupando la primera posición.
                # (Más abajo será cuando se cambie realmente el objeto actual por este resultado.)
            elif resultados.count() < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info('SIN RESULTADOS', 
                                   'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.\n(Atención: Ver la lista completa puede resultar lento si el número de elementos es muy alto)',
                                   padre = self.wids['ventana'])
                return
            ## Un único resultado
            # Primero anulo la función de actualización
            if albaran != None:
                albaran.notificador.set_func(lambda : None)
            # Pongo el objeto como actual
            try:
                albaran = resultados[0]
            except IndexError:
                utils.dialogo_info(titulo = "ERROR: ALBARÁN NO ENCONTRADO", 
                                   texto = "Ocurrió un error y no se pudo recuperar el albarán.\nTal vez se haya eliminado en otro equipo o ha intentado cerrar la ventana con una búsqueda pendiente de completar.",
                                   padre = self.wids['ventana'])
                return
            # Y activo la función de notificación:
            albaran.notificador.set_func(self.aviso_actualizacion)
        self.objeto = albaran
        self.actualizar_ventana()

    def guardar(self, widget):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        albaran = self.objeto
            # Campos del objeto que hay que guardar:
        numalbaran = self.wids['e_numalbaran'].get_text()
        fecha = self.wids['e_fecha'].get_text()
        # Desactivo el notificador momentáneamente
        albaran.notificador.set_func(lambda: None)
        # Actualizo los datos del objeto
        albaran.numalbaran = numalbaran
        prov_anterior = albaran.proveedor
        albaran.proveedor = utils.combo_get_value(self.wids['cmbe_proveedor'])
        if not albaran.proveedor:
            utils.dialogo_info(titulo = "ATENCIÓN", 
                               texto = "No se permiten albaranes de entrada sin proveedor.", 
                               padre = self.wids['ventana'])
            if prov_anterior == None:
                try:
                    import utils_almacen
                    idpropiaempresa=utils_almacen.id_propia_empresa_proveedor()
                    prov_anterior = pclases.Proveedor.get(idpropiaempresa)
                except:
                    try:
                        prov_anterior = pclases.Proveedor.select(
                            orderBy="nombre")[0]
                    except IndexError:
                        prov_anterior = None
            albaran.proveedor = prov_anterior
        try:
            albaran.fecha = utils.parse_fecha(fecha)
        except:
            albaran.fecha = time.localtime()
            utils.dialogo_info(titulo = "ERROR GUARDANDO FECHA", 
                               texto = "La fecha %s no es correcta." % (fecha), 
                               padre = self.wids['ventana'])
        albaran.almacenID = utils.combo_get_value(self.wids['cbe_almacen'])
        # Fuerzo la actualización de la BD y no espero a que SQLObject lo haga por mí:
        albaran.syncUpdate()
        # Vuelvo a activar el notificador
        albaran.notificador.set_func(self.aviso_actualizacion)
        self.actualizar_ventana()
        self.wids['b_guardar'].set_sensitive(False)

    def buscar_fecha(self, boton):
        self.wids['e_fecha'].set_text(utils.str_fecha(utils.mostrar_calendario(fecha_defecto = self.objeto and self.objeto.fecha or None, padre = self.wids['ventana'])))
        
    def borrar_albaran(self, boton):
        """
        Elimina el albarán de la BD
        """
        if utils.dialogo('Se eliminará el albarán actual y todas sus relaciones con ventas, pedidos, etc.\n¿Está seguro?', 
                         'BORRAR ALBARÁN', 
                         padre = self.wids['ventana']): 
            albaran = self.objeto
            if len([ldc for ldc in albaran.lineasDeCompra if ldc.silo != None]) > 0:
                res = utils.dialogo(titulo = "DESCARGAR SILOS", 
                                    texto = "¿Anular también las cargas en silo implicados en el albarán?", 
                                    cancelar = True, 
                                    icono = gtk.STOCK_DIALOG_WARNING, 
                                    defecto = False)
            else:
                res = False
            if res != gtk.RESPONSE_CANCEL:
                if res:
                    for ldc in albaran.lineasDeCompra:
                        if ldc.silo != None:
                            cs = ldc.cargaSilo 
                            ldc.cargaSilo = None
                            cs.destroy(ventana = __file__)
                for linea in albaran.lineasDeCompra:
                    producto = linea.productoCompra
                    if linea.productoCompra.controlExistencias: 
                        # XXX DEBUG
                        #print linea.productoCompra.existencias
                        # XXX EODEBUG
                        producto.sync() 
                        producto.existencias -= linea.cantidad
                        if producto.existencias < 0:
                            producto.existencias = 0
                            # En este caso, si la cantidad absoluta de 
                            # existencias es cero, como debería ser un campo 
                            # calculado pongo a cero las existencias de todos 
                            # los almacenes para ese producto (pues ese 
                            # debería ser el origen del cálculo).
                            for sa in producto.stocksAlmacen:
                                sa.existencias = 0
                                sa.syncUpdate()
                        producto.syncUpdate() 
                        producto.sync() 
                        # XXX DEBUG
                        #print linea.productoCompra.existencias
                        # XXX EODEBUG
                albaran.notificador.set_func(lambda : None)
                albaran.destroy_en_cascada(ventana = __file__)
                self.ir_a_primero()
    
    def imprimir(self, boton):
        """
        Crea un impreso del albarán
        """
        self.guardar(None)  # Si se ha olvidado guardar, guardo yo.
        import informes
        albaran = self.objeto
        if albaran.proveedor != None:
            proveedor = albaran.proveedor.nombre
        else:
            proveedor = ''
        pedidos = []
        lineas = []
        for l in albaran.lineasDeCompra:
            if l.pedidoCompra != None:
                numpedido = l.pedidoCompra.numpedido
            else:
                numpedido = '-'
            lineas.append({'codigo': l.productoCompra.codigo, 'descripcion': l.productoCompra.descripcion, 'cantidad': l.cantidad, 'numped': numpedido })
            if l.pedidoCompra != None and l.pedidoCompra.numpedido not in pedidos:
                pedidos.append(l.pedidoCompra.numpedido)
        cadenaPedidos = ','.join(pedidos)
        general = {'albnum':albaran.numalbaran, 
                   'fecha':utils.str_fecha(albaran.fecha), 
                   'proveedor':proveedor, 
                   'pednum':cadenaPedidos}
        observaciones = utils.dialogo_entrada(titulo = 'OBSERVACIONES', 
                                              texto = '¿Desea incluir alguna observación en el albarán?', 
                                              padre = self.wids['ventana'])
        if observaciones == None:
            return
        informes.abrir_pdf(geninformes.albaranEntrada(general, lineas, observaciones))


if __name__=='__main__':
    a = AlbaranesDeEntradaRepuestos()

