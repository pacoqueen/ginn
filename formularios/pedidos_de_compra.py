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
## pedidos_a_terceros.py - Pedidos de compra a proveedores. 
###################################################################
## NOTAS:
##  Aquí el IVA por defecto sigue siendo 16 porque no depende 
## del cliente (que siempre es Geotexan).
## ----------------------------------------------------------------
## 
###################################################################
## Changelog:
##  1 de septiembre de 2005 -> Inicio
##  6 de septiembre de 2005 -> Ya se crean y muestran pedidos.
##  9 de septiembre de 2005 -> Funcional al ~90%.
## 14 de septiembre de 2005 -> Funcional al 99%
## 25 de octubre de 2005 -> Arreglado cálculo del total LDC.
## 26 de octubre de 2005 -> Chapuceado el mostrar ldc (ver XXX).
## 26 de octubre de 2005 -> ir_a_primero después de borrar.
## 19 de enero de 2006 -> Fork a versión 0.2.
## 23 de enero de 2006 -> Cambio a clase.
## 28 de noviembre de 2006 -> Añadidas líneas de pedido de compra.
###################################################################
## DONE:
## + Hay un problema con la actualización. Cuando modifico el 
##   objeto en pantalla NO debo notificarlo. Ahora mismo notifica
##   y, lo que es peor, se queda colgado en el diálogo de aviso.
##   DONE. (Lo he arreglado desactivando el notificador 
##          momentáneamente mientras guardo los cambios).
## + Todos los ver_algo (botones de más opciones) guardan el 
##   elemento que se seleccione para abrirlo en una ventana nueva.
##   Cuando los formularios estén hechos hay que "empalmarlo".
##   DONE
## + En buscar pedido, cuando antes paso por un diálogo de 
##   resultados, no hago el "truqui" de desactivar el notificador.
##   Tengo que comprobar que funcione igual de bien que cuando sólo
##   hay un resultado de búsqueda y sí se hace. (Vamos, que no dé
##   falsos positivos de actualización como me pasaba antes).DONE.
## + Me falta controlar los cambios en IVA.
##   Guardar el IVA es más complicado, hay que cambiar todas las 
##   LDCs, no se guarda como atributo del objeto. DONE.
###################################################################

from ventana import Ventana
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sqlobject, gobject
import utils, utils_almacen
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
import re, mx, mx.DateTime
import postomatic

class PedidosDeCompra(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self._objetoreciencreado = None
        Ventana.__init__(self, 'pedidos_de_compra.glade', 
                         objeto, 
                         usuario = self.usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_nuevo/clicked': self.crear_nuevo_pedido,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_buscarfecha/clicked': self.mostrar_calendario,
                       'b_anadir_producto/clicked': self.anadir_ldc,
                       'b_eliminar_producto/clicked': self.borrar_ldc,
                       'b_borrar/clicked': self.borrar_pedido,
                       'b_ver_envios/clicked': self.ver_envios,
                       'b_ver_vencimientos/clicked': self.ver_vencimientos,
                       'b_ver_pagos/clicked': self.ver_pagos,
                       'b_ver_facturas/clicked': self.ver_facturas,
                       'b_ver_abonos/clicked': self.ver_abonos,
                       'b_imprimir/clicked': self.imprimir,
                       'b_buscar/clicked': self.buscar_pedido, 
                       'b_unificar/clicked': self.unificar, 
                      }
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        gtk.main()

    def unificar(self, boton):
        """
        Unifica las líneas de pedido de compra y las líneas de pedido 
        albaraneadas agrupando las que tengan mismo precio, entregas, 
        etc...
        """
        pedido = self.objeto
        if pedido != None:
            pedido.unificar_ldcs()
            pedido.unificar_ldpcs()
            self.actualizar_ventana()

    def es_diferente(self):
        """
        Devuelve True si la información en pantalla es distinta a la del
        objeto en memoria.
        """
        pedido = self.objeto
        # PLAN: Debería hacer esta función genérica y recibir los campos
        #       a comparar. Así lo podría reutilizar.
        # Datos a comprobar:
        # - idproveedor
        # - fecha
        # - numpedido
        # - descuento
        # - IVA
        if pedido==None: 
            return False  
        condicion = (self.wids['e_numpedido'].get_text() == pedido.numpedido)
        try:
            condicion = condicion and (
                self.wids['e_fecha'].get_text() 
                == utils.str_fecha(pedido.fecha))
        except AttributeError:  # No tiene fecha, es None:
            condicion = condicion and (
                self.parse_fecha(self.wids['e_fecha'].get_text()) 
                == pedido.fecha)
        try:
            condicion = condicion and (
                utils.combo_get_value(self.wids['cb_proveedor']) 
                == pedido.proveedor.id)
        except AttributeError:  # No tiene proveedor y no puedo acceder a su id
            condicion = condicion and (utils.combo_get_value(
                self.wids['cb_proveedor']) == pedido.proveedor) 
            # Si no hay model, devuelve None. Como tampoco pedido tiene 
            # proveedor, ambos deberían ser None.
        condicion = condicion and (self.wids['e_descuento'].get_text() 
            == "%s %%" % (utils.float2str(pedido.descuento * 100)))
        condicion = condicion and (self.wids['e_iva'].get_text() 
            == "%s %%" % (utils.float2str(pedido.iva * 100)))
        bounds = self.wids['txt_entregas'].get_buffer().get_bounds()
        condicion = condicion and (
            self.wids['txt_entregas'].get_buffer().get_text(bounds[0], 
                bounds[1]) == pedido.entregas)
        bounds = self.wids['txt_observaciones'].get_buffer().get_bounds()
        condicion = condicion and (
            self.wids['txt_observaciones'].get_buffer().get_text(bounds[0], 
                bounds[1]) == pedido.observaciones)
        condicion = condicion and (
            self.wids['e_forma_de_pago'].get_text() == pedido.formaDePago)
        condicion = condicion and (
            self.wids['ch_bloqueado'].get_active() == pedido.bloqueado)
        condicion = condicion and (
            self.wids['ch_cerrado'].get_active() == pedido.cerrado)
        condicion = condicion and (
            self.wids['e_direntrega0'].get_text() == pedido.direccionEntrega0)
        condicion = condicion and (
            self.wids['e_direntrega1'].get_text() == pedido.direccionEntrega1)
        condicion = condicion and (
            self.wids['e_direntrega2'].get_text() == pedido.direccionEntrega2)
        condicion = condicion and (
            self.wids['e_responsable0'].get_text() == pedido.responsable0)
        condicion = condicion and (
            self.wids['e_responsable1'].get_text() == pedido.responsable1)
        condicion = condicion and (
            self.wids['e_portes0'].get_text() == pedido.portes0)
        condicion = condicion and (
            self.wids['e_portes1'].get_text() == pedido.portes1)
        condicion = condicion and (
            self.wids['e_observaciones0'].get_text() == pedido.observaciones0)
        condicion = condicion and (
            self.wids['e_observaciones1'].get_text() == pedido.observaciones1)
        condicion = condicion and (
            self.wids['e_observaciones2'].get_text() == pedido.observaciones2)
        return not condicion	# condicon verifica que todo sea igual.

    def parse_porcentaje(self, strfloat):
      """
      Recibe un porcentaje como cadena. Puede incluir el un espacio,
      el signo menos (-) y el porciento (%).
      La función procesa la cadena y devuelve un flotante que se 
      corresponde con el valor completo del porcentaje, es decir, 
      no en la forma 0. sino xx. (10 % = 10 != 0.1)
      """
      return utils.parse_porcentaje(strfloat)

    def parse_fecha(self, strfecha):
        """
        Recibe una fecha en formato dd/mm/aaaa y devuelve
        una tupla con la fecha en formato (d, m, aaaa).
        Si la fecha no se puede procesar devuelve None 
        (por compatibilidad con pedido.fecha=None).
        """
        # PLAN: Mejorar para que pueda aceptar más formatos de fecha.
        #       Probablemente algo así esté ya hecho en el módulo time.
        #try:
        #  d, m, a = map(int, strfecha.split('/')) 
        #  return (d,m,a)
        #except ValueError:
        #  return None
        return utils.parse_fecha(strfecha)
      
    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo
        sus valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el treeview, etc.
        """
        self.wids['ch_imprimir_precios'].set_active(True)
        # Inicialmente no se muestra NADA. Sólo se le deja al usuario la 
        # opción de buscar.
        self.activar_widgets(False)
        self.wids['b_actualizar'].set_sensitive(False)
        self.wids['b_guardar'].set_sensitive(False)
        # Alineación de los ENTRY de totales:
        self.wids['e_bruto'].set_alignment(1.0)
        self.wids['e_neto'].set_alignment(1.0)
        self.wids['e_total'].set_alignment(1.0)
        self.wids['e_totaliva'].set_alignment(1.0)
        # Inserto los proveedores en el combo:
        provs = pclases.Proveedor.select(orderBy = 'nombre')
        lista_provs = [(p.id, p.nombre) for p in provs if not p.inhabilitado]
        utils.rellenar_lista(self.wids['cb_proveedor'], lista_provs)
        self.wids['cb_proveedor'].connect("changed", 
                                          self.combo_proveedor_cambiado)
        # Preparo las columnas de la tabla.
        # Llevará:
        #   - Código de producto (de la relación con productos)
        #   - Descripción        (de la relación con productos)
        #   - Precio/unidad      (de la propia LDC -valor por defecto de 
        #                         productos-)
        #   - Cantidad           (de la propia LDC)
        #   - Total de línea     (de la propia LDC -valor por defecto 
        #                         calculado-)
        #   - Confirmación       (de la propia LDC)
        #   - Identificador de LDC (INT64~integer de Postgre) -No se mostrará-
        cols = (('Código', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Descripción', 'gobject.TYPE_STRING', False, True, True, None),
                ('Cantidad', 'gobject.TYPE_DOUBLE', True, True, False, 
                    self.actualizar_cantidad_ldc), 
                ('Precio/u', 'gobject.TYPE_DOUBLE', True, True, False, 
                    self.actualizar_precio_ldc), 
                ('Total', 'gobject.TYPE_DOUBLE', False, True, False, None), 
                ('Entrega', 'gobject.TYPE_STRING', True, True, False, 
                    self.actualizar_entrega_ldc), 
                ('Recibida', 'gobject.TYPE_BOOLEAN', False, True, False, None), 
                ('en albarán', 'gobject.TYPE_STRING', False, True, False, None),
                ('con fecha', 'gobject.TYPE_STRING', False, True, False, None), 
                ('IDLDV', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_lineasdeventa'], cols)
        cols = (('Descripción', 'gobject.TYPE_STRING', False, True, True, None),
                ('Cantidad', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_cantidad_ldpc),  
                ('Precio/u', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_precio_ldpc), 
                ('Dto.', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_descuento_ldpc), 
                ('Subtotal', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Fecha entrega', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_fecha_entrega_ldpc), 
                ('Texto entrega', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_texto_entrega_ldpc), 
                ('IDLDPC', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_ldpc'], cols)
        postomatic.attach_menu_notas(self.wids['tv_ldpc'], 
                                     pclases.LineaDePedidoDeCompra, 
                                     self.usuario, 
                                     0)
        cols = (('Producto', 'gobject.TYPE_STRING', False, True, True, None), 
                ('Cantidad', 'gobject.TYPE_STRING', False, True, False, None), 
                ('IDProducto', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_pendiente'], cols)

    def cambiar_cantidad_ldpc(self, cell, path, texto):
        """
        Cambia la cantidad de la línea de pedido de compra.
        """
        regexp = re.compile("[\d.,]+")  
        # El "-" lo he obviado queriendo. ¡It's not a bug! ¡It's a feature!
        pedido = self.objeto
        if pedido != None:
            model = self.wids['tv_ldpc'].get_model()
            idldpc = model[path][-1]
            try:
                ldpc = pclases.LineaDePedidoDeCompra.get(idldpc)
            except ZeroDivisionError:
                return
            cantidad = regexp.findall(texto)
            if len(cantidad) > 0:
                cantidad = cantidad[0]
                ldpc.cantidad = float(cantidad)
                subtotal = self.rellenar_lineas_de_pedido_de_compra()
                self.rellenar_totales(subtotal)

    def cambiar_precio_ldpc(self, cell, path, texto):
        """
        Cambia el precio de la línea de pedido de compra.
        """
        pedido = self.objeto
        if pedido != None:
            model = self.wids['tv_ldpc'].get_model()
            idldpc = model[path][-1]
            try:
                ldpc = pclases.LineaDePedidoDeCompra.get(idldpc)
            except:
                return
            try:
                precio = utils.parse_euro(texto)
            except ValueError:
                precio = 0
            ldpc.precio = precio
            subtotal = self.rellenar_lineas_de_pedido_de_compra()
            self.rellenar_totales(subtotal)

    def cambiar_descuento_ldpc(self, cell, path, texto):
        """
        Cambia el descuento de la línea de pedido de compra.
        El descuento se parsea para que vaya en fracción de la unidad.
        """
        pedido = self.objeto
        if pedido != None:
            model = self.wids['tv_ldpc'].get_model()
            idldpc = model[path][-1]
            try:
                ldpc = pclases.LineaDePedidoDeCompra.get(idldpc)
            except:
                return
            try:
                dto = utils.parse_porcentaje(texto)
            except ValueError:
                dto = 0
            ldpc.descuento = dto / 100.0
            subtotal = self.rellenar_lineas_de_pedido_de_compra()
            self.rellenar_totales(subtotal)

    def cambiar_fecha_entrega_ldpc(self, cell, path, texto):
        """
        Cambia la fecha de entrega de la línea de pedido de compra.
        Si texto.strip() == "" se asigna la fecha a None.
        """
        pedido = self.objeto
        if pedido != None:
            model = self.wids['tv_ldpc'].get_model()
            idldpc = model[path][-1]
            try:
                ldpc = pclases.LineaDePedidoDeCompra.get(idldpc)
            except:
                return
            texto = texto.strip()
            if texto == "":
                ldpc.fechaEntrega = None
            else:
                try:
                    fecha = utils.parse_fecha(texto)
                except (mx.DateTime.RangeError, ValueError):
                    utils.dialogo_info(titulo = "VALOR INCORRECTO", 
                                       texto = "La fecha introducida no es correcta. Use el formato «dd/mm/aa» o «dd/mm/aaaa».", 
                                       padre = self.wids['ventana'])
                else:
                    ldpc.fechaEntrega = fecha
            subtotal = self.rellenar_lineas_de_pedido_de_compra()
            self.rellenar_totales(subtotal)

    def cambiar_texto_entrega_ldpc(self, cell, path, texto):
        """
        Cambia el texto de la entrega de la línea de pedido de compra.
        """
        pedido = self.objeto
        if pedido != None:
            model = self.wids['tv_ldpc'].get_model()
            idldpc = model[path][-1]
            try:
                ldpc = pclases.LineaDePedidoDeCompra.get(idldpc)
            except:
                return
            ldpc.textoEntrega = texto
            subtotal = self.rellenar_lineas_de_pedido_de_compra()
            self.rellenar_totales(subtotal)

    def combo_proveedor_cambiado(self, c):
        idprov = utils.combo_get_value(c)
        if idprov != None:
            proveedor = pclases.Proveedor.get(idprov)
            if proveedor.inhabilitado:
                self.objeto.proveedorID = idprov = None
                self.actualizar_ventana()
                c.child.set_text("")
                c.set_active(-1)
                utils.dialogo_info(titulo = "PROVEEDOR INHABILITADO", 
                                   texto = "El proveedor %s ha sido inhabilitado. Seleccione otro proveedor.\nMotivo: %s.\nNo pueden hacérsele pedidos hasta que vuelva a habilitarse en la ventana correspondiente." % (proveedor.nombre, proveedor.motivo), 
                                   padre = self.wids['ventana'])
                c.grab_focus()
            else:
                if self.wids['e_forma_de_pago'].get_text() == "":
                    self.wids['e_forma_de_pago'].set_text(proveedor.formadepago)
                self.wids['e_iva'].set_text("%s %%" % (
                    utils.float2str(proveedor.iva * 100)))
                self.objeto.iva = proveedor.iva
                subtotal = self.rellenar_lineas_de_pedido_de_compra()
                self.rellenar_totales(subtotal)
        if self.objeto.proveedorID != idprov:
            pedido = self.objeto
            pedido.notificador.desactivar()
            pedido.proveedorID = idprov
            pedido.syncUpdate()
            pedido.make_swap()
            pedido.notificador.activar(self.aviso_actualizacion)
    
    def check_permisos(self):
        """
        Activa o desactiva los controles dependiendo de los 
        permisos del usuario.
        """
        VENTANA = "pedidos_de_compra.py"
        if self.usuario != None and self.usuario.nivel > 0:
            ventanas=pclases.Ventana.select(pclases.Ventana.q.fichero==VENTANA)
            if ventanas.count() == 1:   # Siempre debería ser 1.
                permiso = self.usuario.get_permiso(ventanas[0])
                if permiso.escritura:
                    if self.usuario.nivel <= 1:
                        # print "Activo widgets para usuario con nivel de 
                        # privilegios <= 1."
                        self.activar_widgets(True, chequear_permisos = False)
                    else:
                        # print "Activo widgets porque permiso de lectura y 
                        # objeto no bloqueado."
                        self.activar_widgets(self.objeto != None and (
                            not self.objeto.bloqueado 
                            or self._objetoreciencreado == self.objeto), 
                                             chequear_permisos = False)
                else:   # No tiene permiso de escritura. Sólo puede modificar 
                        # el objeto que acaba de crear.
                    if self._objetoreciencreado == self.objeto: 
                        # print "Activo widgets porque objeto recién creado 
                        # aunque no tiene permiso de escritura."
                        self.activar_widgets(True, chequear_permisos = False)
                    else:
                        # print "Desactivo widgets porque no permiso de 
                        # escritura."
                        self.activar_widgets(False, chequear_permisos = False)
                self.wids['b_buscar'].set_sensitive(permiso.lectura)
                self.wids['b_nuevo'].set_sensitive(permiso.nuevo)
        else:
            self.activar_widgets(True, chequear_permisos = False)

    def activar_widgets(self, s, chequear_permisos = True):
        """ 
        Activa o desactiva (sensitive=True/False) todos
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso se 
        evaluará como boolean.
        Si chequear_permisos se debe poner a False para 
        evitar recursión infinita.
        """
        ws = ('b_ver_envios', 'b_ver_vencimientos', 'b_ver_pagos', 
              'b_ver_facturas', 'b_ver_abonos', 'e_numpedido', 'cb_proveedor',
              'e_fecha', 'b_buscarfecha', 'e_iva', 'e_descuento',
              'e_bruto', 'e_totaliva', 'e_total', 'e_neto', 'b_anadir_producto',
              'b_eliminar_producto', 'b_borrar', 'txt_entregas', 
              'e_forma_de_pago', 'txt_observaciones', 'tv_pendiente', 
              'tv_lineasdeventa', 'tv_ldpc', 'hbuttonbox1', 
              'e_direntrega0', 'e_direntrega1', 'e_direntrega2', 
              'e_responsable0', 'e_responsable1', 'e_portes0', 'e_portes1', 
              'e_observaciones0', 'e_observaciones1', 'e_observaciones2')
        for w in ws:
            self.wids[w].set_sensitive(s)
        if chequear_permisos:
            self.check_permisos()
        # Casos especiales: observaciones2 
        # (dde.pedCompraTextoEditableConNivel1) y observaciones0 
        # (dde.pedCompraTextoFijo)
        if self.usuario and self.usuario.nivel > 0:
            self.wids['e_observaciones0'].set_sensitive(False)
        if self.usuario and self.usuario.nivel > 1:
            self.wids['e_observaciones2'].set_sensitive(False)
        # El texto de la forma de pago de observaciones 2 tiene preferencia 
        # sobre el de toda la vida. Si está relleno, oculto el otro para no 
        # liar al usuario porque de todas formas en el geninformes se va a 
        # ignorar.
        self.wids['e_forma_de_pago'].set_sensitive(
            not self.wids['e_observaciones2'].get_text()) 

    def ir_a_primero(self):
      """
      Hace que el primer registro -si lo hay- de la tabla
      pedidos con la propia empresa como cliente (pedido 
      de compra) sea el pedido activo.
      """
      pedido = self.objeto
      try:
          # Anulo el aviso de actualización del pedido que deja de ser activo 
          if pedido != None: pedido.notificador.desactivar()
          pedido = pclases.PedidoCompra.select(orderBy = "-id")[0]
          pedido.notificador.activar(self.aviso_actualizacion)
      except:
          pedido = None
      self.objeto = pedido
      self.actualizar_ventana()

    def pedir_producto(self, filtrar = True, txt = ''):
      """
      Pide un producto mediante una ventana de búsqueda.
      Devuelve un objeto producto o None si canceló/no se encontró.
      """
      producto = None
      a_buscar = utils.dialogo_entrada(titulo = "BUSCAR PRODUCTO", 
                                       texto = "Introduzca texto a buscar: ", 
                                       valor_por_defecto = txt)
      if a_buscar != None:
        try:
            id_a_buscar = utils.parse_numero(a_buscar)
        except:
            id_a_buscar = 0
        criterio = sqlobject.OR(pclases.ProductoCompra.q.id == id_a_buscar,
                        pclases.ProductoCompra.q.codigo.contains(a_buscar),
                        pclases.ProductoCompra.q.descripcion.contains(a_buscar))
        if filtrar:
            resultados = pclases.ProductoCompra.select(pclases.AND(
                pclases.ProductoCompra.q.controlExistencias == True, 
                pclases.ProductoCompra.q.obsoleto == False, 
                criterio))
        else:
            resultados = pclases.ProductoCompra.select(criterio)
        if resultados.count() > 1:
            ## Refinar los resultados:
            filas_res = []
            for r in resultados:
                filas_res.append((r.id, r.codigo, r.descripcion))
            idproducto = utils.dialogo_resultado(filas_res, 
                                            titulo = 'Seleccione producto', 
                                            cabeceras = ('ID Interno', 
                                                         'Código', 
                                                         'Descripción'), 
                                            padre = self.wids['ventana'])
            if idproducto < 0:
                return None, a_buscar
            producto = pclases.ProductoCompra.get(idproducto)
        elif resultados.count() < 1:
            ## La búsqueda no produjo resultados.
            utils.dialogo_info('SIN RESULTADOS', 
                               'La búsqueda no produjo ningún resultado.\n'
                               'Intente una búsqueda menos restrictiva usando'
                               ' un texto más corto.', 
                               padre = self.wids['ventana'])
            return None, a_buscar
        else:
            producto = resultados[0]
      return producto, a_buscar
     
    # --------------- Manejadores de eventos ----------------------------
    def actualizar_precio_ldc(self, cell, path, nuevotexto):
      """
      Actualiza el precio en la LDC del "path" -última
      columna del Row del Model - según el texto que 
      contielle la delda "cell".
      """
      idldc = self.wids['tv_lineasdeventa'].get_model()[path][-1]
      pedido = self.objeto
      try:
        ldc = [l for l in pedido.lineasDeCompra if l.id == idldc][0]
        ldc.precio = utils._float(nuevotexto)
        self.actualizar_ventana()
      except IndexError:
        utils.dialogo("La LDC no existe.")
      except ValueError:
        utils.dialogo("Debe ser un número.")

    def actualizar_entrega_ldc(self, cell, path, nuevotexto):
        """
        Actualiza el campo entrega en la LDC del "path" -última
        columna del Row del Model - según el texto que 
        contiene la celda "cell".
        """
        pedido = self.objeto
        model = self.wids['tv_lineasdeventa'].get_model()
        idldc = model[path][-1]
        try:
            ldc = pclases.LineaDeCompra.get(idldc)
            ldc.entrega = nuevotexto
            ldc.syncUpdate()
            model[path][5] = ldc.entrega
        except:
            utils.dialogo(titulo = "ERROR", 
                          texto = "La línea de compra (%d) no existe o no se pudo actualizar." % (idldc), 
                          padre = self.wids['ventana'])

    def actualizar_cantidad_ldc(self, cell, path, nuevotexto):
      """
      Actualiza la cantidad en la LDC del "path" -última
      columna del Row del Model - según el texto que 
      contielle la delda "cell".
      """
      pedido = self.objeto
      idldc = self.wids['tv_lineasdeventa'].get_model()[path][-1]
      try:
        ldc = [l for l in pedido.lineasDeCompra if l.id == idldc][0]
        ldc.cantidad = utils._float(nuevotexto)
        self.actualizar_ventana()
      except IndexError:
        utils.dialogo("La LDC no existe.")
      except ValueError:
        utils.dialogo("Debe ser un número.")

    def crear_nuevo_pedido(self, event):
        """ 
        Pide los datos básicos para crear un nuevo pedido.
        Una vez insertado en la BD hay que hacer ese pedido
        activo en la ventana para que pueda ser editado.
        """
        # Datos a pedir: Número de pedido (que por defecto será el último -MAX- más 1
        #                de todos aquellos pedidos que sean de compra)
        ultimonumpedido = utils_almacen.ultimo_pedido_de_compra_mas_uno()
        numpedido = utils.dialogo_entrada(titulo = 'NÚMERO DE PEDIDO', 
                                          texto = 'Número de pedido: Introduzca el número de pedido.\nPor defecto será %d.' % (ultimonumpedido),
                                          valor_por_defecto = str(ultimonumpedido), 
                                          padre = self.wids['ventana'])
        if numpedido == None:
            #Ha cancelado
            return 
        else:
            if numpedido == '':
                #Número por defecto
                numpedido = ultimonumpedido 
            # Verifico que numpedido no esté repetido:
            peds = pclases.PedidoCompra.select()
            if numpedido in [p.numpedido for p in peds if p.fecha and p.fecha.year == time.localtime().tm_year]:
                utils.dialogo_info(titulo = 'NÚMERO DUPLICADO', 
                                   texto = "El número de pedido ya existe. No se pudo crear un pedido nuevo.", 
                                   padre = self.wids['ventana'])
            else:
                try:
                    dde = pclases.DatosDeLaEmpresa.select()[0]
                    de0 = dde.nombre
                    de1 = dde.direccion
                    de2 = "%s %s (%s), %s" % (dde.cp,
                                              dde.ciudad,
                                              dde.provincia,
                                              dde.pais)
                    r0 = dde.nombreResponsableCompras + " " + dde.telefonoResponsableCompras
                    r1 = dde.emailResponsableCompras
                    p0 = "PORTES PAGADOS"
                    if dde.esSociedad:
                        fabortienda = "FÁBRICA"
                    else:
                        fabortienda = "TIENDA"
                    p1 = "ENTREGA EN NUESTRA %s DE %s" % (fabortienda, 
                                                          dde.ciudad.upper())
                    o0 = dde.pedCompraTextoFijo
                    o1 = dde.pedCompraTextoEditable
                    o2 = dde.pedCompraTextoEditableConNivel1
                except IndexError:
                    de0 = de1 = de2 = r0 = r1 = p0 = p1 = o0 = o1 = o2
                # Aquí ya debo tener un número de pedido y de cliente correcto.
                self._objetoreciencreado = pedido = pclases.PedidoCompra(
                    proveedor = None, 
                    fecha = time.localtime(), 
                    numpedido = numpedido, 
                    descuento = 0,
                    iva = 0.21, 
                    cerrado = False, 
                    bloqueado = True, 
                    direccionEntrega0 = de0, 
                    direccionEntrega1 = de1, 
                    direccionEntrega2 = de2, 
                    responsable0 = r0, 
                    responsable1 = r1, 
                    portes0 = p0, 
                    portes1 = p1, 
                    observaciones = "",     # Observaciones del usuario.
                    observaciones0 = o0,    # Observaciones casi obligatorias. 
                    observaciones1 = o1,    # Necesarios permisos para 
                    observaciones2 = o2,    # modificarlas.
                    formaDePago = o2)
            self.objeto = pedido
        self.actualizar_ventana()

    def actualizar_ventana(self, widget=None, objeto_anterior = None):
        """
        Actualiza el contenido de los controles de la
        ventana para que muestren todos los datos 
        del pedido actual.
        """
        pedido = self.objeto
        self.activar_widgets(pedido!=None)
        if pedido != None:
            try:
                pedido.sync()  
                # Por si acaso hay cambios remotos que no están en el objeto.
            except: # HA SIDO BORRADO
                utils.dialogo_info(titulo = 'BORRADO', 
                                   texto = 'Pedido borrado remotamente.', 
                                   padre = self.wids['ventana'])
                self.ir_a_primero()
            else:
                self.wids['e_numpedido'].set_text(pedido.numpedido)
                utils.combo_set_from_db(self.wids['cb_proveedor'], 
                                        pedido.proveedorID)
                try:
                    self.wids['e_fecha'].set_text(
                        utils.str_fecha(pedido.fecha))
                except AttributeError:  # No tiene fecha
                    self.wids['e_fecha'].set_text('')
                model_ldc = self.wids['tv_lineasdeventa'].get_model()
                model_ldc.clear()	# Por si ya había algo
                for ldc in pedido.lineasDeCompra:
                    total = ldc.precio * ldc.cantidad
                    confirmada = ldc.albaranEntrada != None     # TODO: Este campo creo que ya sobra. Una vez comprobado que todas las líneas que aparezcan aquí lo tienen a True (porque no deberían existir LDCs con pedido pero sin albarán), quitar el campo.
                    model_ldc.append(
                        [ldc.productoCompra.codigo,
                         ldc.productoCompra.descripcion,
                         ldc.cantidad,
                         ldc.precio,
                         total,
                         ldc.entrega,
                         confirmada,
                         ldc.albaranEntrada 
                            and ldc.albaranEntrada.numalbaran 
                            or "", 
                         ldc.albaranEntrada 
                            and utils.str_fecha(ldc.albaranEntrada.fecha) 
                            or "", 
                         ldc.id])
                subtotal = self.rellenar_lineas_de_pedido_de_compra()
                self.rellenar_totales(subtotal)
                self.wids['txt_entregas'].get_buffer().set_text(pedido.entregas)
                self.wids['txt_observaciones'].get_buffer().set_text(pedido.observaciones)
                self.wids['e_forma_de_pago'].set_text(pedido.formaDePago)
                self.wids['ch_cerrado'].set_active(pedido.cerrado)
                self.wids['ch_bloqueado'].set_active(pedido.bloqueado)
                self.wids['tv_pendiente'].set_sensitive(not self.objeto.cerrado)
                self.wids['e_direntrega0'].set_text(pedido.direccionEntrega0)
                self.wids['e_direntrega1'].set_text(pedido.direccionEntrega1)
                self.wids['e_direntrega2'].set_text(pedido.direccionEntrega2)
                self.wids['e_responsable0'].set_text(pedido.responsable0)
                self.wids['e_responsable1'].set_text(pedido.responsable1)
                self.wids['e_portes0'].set_text(pedido.portes0)
                self.wids['e_portes1'].set_text(pedido.portes1)
                self.wids['e_observaciones0'].set_text(pedido.observaciones0)
                self.wids['e_observaciones1'].set_text(pedido.observaciones1)
                self.wids['e_observaciones2'].set_text(pedido.observaciones2)
                self.objeto.make_swap()
        else:
            self.activar_widgets(False, False)
            self.wids['e_numpedido'].set_text("")
            self.wids['e_fecha'].set_text('')
            model_ldc = self.wids['tv_lineasdeventa'].get_model()
            model_ldc.clear()	# Por si ya había algo
            self.wids['txt_entregas'].get_buffer().set_text("")
            self.wids['txt_observaciones'].get_buffer().set_text("")
            self.wids['e_forma_de_pago'].set_text("")
            self.wids['ch_cerrado'].set_active(False)
            self.wids['ch_bloqueado'].set_active(False)
            self.wids['tv_pendiente'].set_sensitive(False)
        self.wids['b_actualizar'].set_sensitive(False)

    def rellenar_totales(self, subtotal):
        """
        Rellena los totales del pedido.
        """
        pedido = self.objeto
        self.wids['e_iva'].set_text("%s %%" % (utils.float2str(pedido.iva * 100)))
        if pedido.descuento == None: 
            pedido.descuento = 0
            # Esto sólo es para prevenir. No se debería tocar al mostrar los datos.
        self.wids['e_descuento'].set_text("%s %%" % (utils.float2str(pedido.descuento * 100)))
        total_iva = subtotal * pedido.iva
        total_descuento = -1 * subtotal * pedido.descuento
        total = subtotal + total_iva + total_descuento
        self.wids['e_bruto'].set_text('%s €' % utils.float2str(subtotal))
        self.wids['e_totaliva'].set_text('%s €' % utils.float2str(total_iva))
        self.wids['e_neto'].set_text('%s €' % utils.float2str(total_descuento))	
        #OJO: El nombre está mal, no es el NETO (BRUTO+DESC.) es el TOTAL DESC.
        self.wids['e_total'].set_text('%s €' % utils.float2str(total))
 

    def rellenar_pendiente(self):
        """
        Rellena el cuadro de pendiente de recibir.
        Si el pedido está cerrado, lo deshabilita después 
        de introducir la información.
        """
        pedido = self.objeto
        if pedido != None:
            model = self.wids['tv_pendiente'].get_model()
            self.wids['tv_pendiente'].set_model(None)
            model.clear()
            productos_pendientes_servir = pedido.get_productos_pendientes_servir()
            if len(productos_pendientes_servir) == 0 and len(self.objeto.lineasDePedidoDeCompra) > 0:
                self.objeto.cerrado = True      # Cierre automático del pedido si ya no queda nada por servir.
                self.wids['ch_cerrado'].set_active(self.objeto.cerrado)
            for producto, cantidad in productos_pendientes_servir:
                model.append((producto.descripcion, 
                              "%s %s" % (utils.float2str(cantidad), producto.unidad), 
                              producto.id))
            self.wids['tv_pendiente'].set_model(model)

    def rellenar_lineas_de_pedido_de_compra(self):
        """
        Rellena el TreeView de líneas de pedido de compra.
        """
        pedido = self.objeto
        subtotal = 0
        if pedido != None:
            model = self.wids['tv_ldpc'].get_model()
            self.wids['tv_ldpc'].set_model(None)
            model.clear()
            for ldpc in pedido.lineasDePedidoDeCompra:
                model.append((ldpc.productoCompra.descripcion, 
                              "%s %s" % (utils.float2str(ldpc.cantidad, 1), ldpc.productoCompra.unidad), 
                              "%s €" % (utils.float2str(ldpc.precio, 4, autodec = True)), 
                              "%s %%" % (utils.float2str(ldpc.descuento * 100)),
                              "%s €" % (utils.float2str(ldpc.get_subtotal(), 3)),  
                              ldpc.fechaEntrega and utils.str_fecha(ldpc.fechaEntrega) or "", 
                              ldpc.textoEntrega,  
                              ldpc.id
                            ))
                subtotal += ldpc.get_subtotal()
            self.wids['tv_ldpc'].set_model(model)
            self.rellenar_pendiente()
        return subtotal

    def mostrar_calendario(self, widget):
      """
      Muestra un Gtk.Calendar y escribe la fecha seleccionada
      en el widget e_fecha.
      """
      self.wids['e_fecha'].set_text(utils.str_fecha(utils.mostrar_calendario(fecha_defecto = self.objeto and self.objeto.fecha or None, padre = self.wids['ventana'])))

    def buscar_pedido(self, widget):
      """
      Muestra una ventana de búsqueda de pedidos de compra  
      y a continuación los resultados. El pedido
      seleccionado se hará activo en la
      ventana.
      """
      pedido = self.objeto
      a_buscar = utils.dialogo_entrada(titulo = "BUSCAR PEDIDO", 
                                       texto = "Introduzca número de pedido:", 
                                       padre = self.wids['ventana'])
      # PLAN: En adelante sería interesante poder buscar por más criterios.
      if a_buscar != None:
        criterio = pclases.PedidoCompra.q.numpedido.contains(a_buscar)
        resultados = pclases.PedidoCompra.select(criterio)
        if resultados.count() > 1:
          ## Refinar los resultados:
          filas_res = []
          for r in resultados:
            try:
              nombreproveedor = r.proveedor.nombre
            except AttributeError: # No tiene proveedor. Es None y eso da un warning muy feo al representarlo en un TView.
              nombreproveedor = ''
            filas_res.append((r.id, r.numpedido, nombreproveedor, 
                            [r.fecha and r.fecha.strftime('%d/%m/%Y') or ''][0]))
          idpedido = utils.dialogo_resultado(filas_res, 
                                             titulo = 'Seleccione pedido',
                                        cabeceras = ('ID Interno', 'Número de pedido', 'Proveedor', 'Fecha'))
          if idpedido < 0:
            return
          resultados = [pclases.PedidoCompra.get(idpedido)]
            # Se supone que la comprensión es más rápida que PedidoCompra.get(id)
        elif resultados.count() < 1:
          ## Sin resultados de búsqueda
          utils.dialogo_info('SIN RESULTADOS', 'La búsqueda no produjo resultados.\nAsegúrese de haber introducido un número de pedido.')
          return
        # Primero anulo la función de actualización:
        if pedido != None: pedido.notificador.desactivar()
        # Pongo el pedido como actual:
        pedido = resultados[0]
        # Y activo la función de notificación:
        pedido.notificador.activar(self.aviso_actualizacion)
        self.objeto = pedido
        self.actualizar_ventana()

    def anadir_ldc(self, widget):
        """
        Pide datos, crea una LDPC y la añade al pedido.
        """
        pedido = self.objeto
        producto, a_buscar = self.pedir_producto()
        if a_buscar == None:
            return
        if producto == None: 
            if utils.dialogo(titulo = "BUSCAR EN MÁS PRODUCTOS", 
                             texto = "No se encontraron productos con gestión"
                                     " de existencias por software.\n\n¿Desea"
                                     " buscar entre todos los productos de "
                                     "compra?", 
                             padre = self.wids['ventana']):
                producto, a_buscar = self.pedir_producto(filtrar = False, 
                                                         txt = a_buscar)
                if producto == None:
                    return
            else:
                return
        cantidad = utils.dialogo_entrada(texto = 'Introduzca cantidad:', 
                                         titulo = 'CANTIDAD', 
                                         valor_por_defecto = '1', 
                                         padre = self.wids['ventana'])
        if cantidad == None: 
            return  
        precio = utils.dialogo_entrada(titulo = "IVA", 
                                       texto = 'Introduzca precio SIN IVA:', 
                                       valor_por_defecto = utils.float2str(producto.precioDefecto), 
                                       padre = self.wids['ventana'])
        if precio == None: 
            return
        try:
            cantidad = utils._float(cantidad)
            precio = utils._float(precio)
        except TypeError:
            utils.dialogo(titulo = "ERROR EN FORMATO NUMÉRICO", 
                          texto = 'El precio y cantidad deben ser números.', 
                          padre = self.wids['ventana'])
            return
        except ValueError:
            utils.dialogo(titulo = "ERROR EN FORMATO NUMÉRICO", 
                          texto = 'Inténtelo de nuevo usando punto (.) como símbolo decimal.', 
                          padre = self.wids['ventana'])
            return
        fechahora = time.localtime()
        ldpc = pclases.LineaDePedidoDeCompra(pedidoCompra = pedido,
                                             cantidad = cantidad,
                                             precio = precio,
                                             productoCompra = producto,
                                             descuento = 0, 
                                             fechaEntrega = None) 
        self.actualizar_ventana()

    def borrar_ldc(self, widget):
        """
        Elimina la LDPC actualmente marcada del pedido.
        Si la LDPC está implicada en albaranes, artículos, etc. la
        propia BD impedirá el borrado (that's I hope).
        En todo caso, _se eliminará del pedido_.
        """
        pedido = self.objeto
        model, paths = self.wids['tv_ldpc'].get_selection().get_selected_rows()
        for path in paths:
            idldpc = model[path][-1]
            ldpc = pclases.LineaDePedidoDeCompra.get(idldpc)
            try:
                ldpc.destroySelf()
            except:
                utils.dialogo_info('NO SE PUDO ELIMINAR COMPLETAMENTE', 
                                   "El producto no se pudo eliminar completamente.\nVerifique que no esté implicado en otras operaciones, \nque no se ha confirmado ya la recepción, etc.",
                                    padre = self.wids['ventana'])
        self.actualizar_ventana()
  
    def borrar_pedido(self, widget):
        """
        Borra el pedido completo.
        """
        pedido = self.objeto
        if utils.dialogo(titulo = "BORRAR PEDIDO", 
                         texto = 'Eliminar un pedido implica interacciones complejas. ¿Está seguro?', 
                         padre = self.wids['ventana']):
            borrar_entradas = utils.dialogo(titulo = "¿BORRAR ENTRADAS?", 
                                            texto = "¿Desea también eliminar las entradas en almacén relacionadas con el pedido?", 
                                            padre = self.wids['ventana'])
            # Primero elimino las líneas de compra:
            fallidas = 0
            for ldc in pedido.lineasDeCompra:
                if borrar_entradas:
                    producto = ldc.productoCompra
                    cantidad = ldc.cantidad
                    try:
                        ldc.destroySelf()
                    except:
                        fallidas += 1
                    else: 
                    # Actualizo existencias que fueron incrementadas cuando se creó la LDC. Y si no se hizo... no haber borrado el pedido.
                        producto.sync()
                        producto.existencias -= cantidad
                else:
                    ldc.pedidoCompra = None
            for ldpc in pedido.lineasDePedidoDeCompra:
                try:
                    ldpc.destroySelf()
                except:
                    fallidas += 1
            # Si aquí quedan líneas de venta es porque el impacto de 
            # borrarlas sería demasiado grande (implica envíos relacionados,
            # facturas e incluso alteraciones en el stock).
            if fallidas > 0:
                utils.dialogo_info('PEDIDO NO BORRADO.', 
                                   'El pedido no pudo ser completamente eliminado.\nExisten enlaces con albaranes, facturas, etc. que impiden el borrado.',
                                   padre = self.wids['ventana'])
            else:
                if pedido != None:
                    pedido.notificador.desactivar()
                try:
                    pedido.destroySelf()
                    self.ir_a_primero()
                except:
                    utils.dialogo_info('ERROR EN LA ELIMINACIÓN',
                                       'El pedido no fue eliminado.\nEs posible que esté implicado en otras operaciones.',
                                       padre = self.wids['ventana'])
            self.actualizar_ventana()

    def guardar(self, widget):
        """
        Guarda el contenido de los entry y demás en el objeto y 
        lo sincroniza con la BD.
        """
        pedido = self.objeto
        # Campos del objeto que hay que guardar: 
        # (el resto se actualizan al instante al tener edición directa -precios, etc.-)
        # - idproveedor (el idcliente no cambia porque en un pedido de compra siempre debe ser la empresa)
        # - fecha
        # - numpedido
        # - descuento
        # - iva
        idproveedor = utils.combo_get_value(self.wids['cb_proveedor'])
        if idproveedor != None:
            idproveedor = pclases.Proveedor.get(idproveedor)
            # Si no, idproveedor ya vale None, que es el valor que tendrá en pedido.idproveedor.
        try:
            fecha = time.strptime(self.wids['e_fecha'].get_text(), "%d/%m/%Y")
            # OJO: Sólo acepta fechas en ese formato. No valen guiones. Sólo «/».
        except ValueError:  #La fecha no es correcta
            fecha = None
        numpedido = self.wids['e_numpedido'].get_text()
        if self.wids['e_observaciones2'].get_text():
            self.wids['e_forma_de_pago'].set_text(
                self.wids['e_observaciones2'].get_text())
        forma_de_pago = self.wids['e_forma_de_pago'].get_text()
        try:
            descuento = utils.parse_porcentaje(self.wids['e_descuento'].get_text()) / 100.0
        except ValueError:
            descuento = 0
        try:
            iva = utils.parse_porcentaje(self.wids['e_iva'].get_text()) / 100.0
        except ValueError:
            iva = 0.21
        # Verifico que numpedido no esté repetido:
        peds = pclases.PedidoCompra.select(pclases.PedidoCompra.q.numpedido!=pedido.numpedido)
        nums = [p.numpedido for p in peds]
        if numpedido in nums:
            utils.dialogo_info("NÚMERO DE PEDIDO REPETIDO.", "El numero de pedido es incorrecto.\nIntroduzca otro.", padre = self.wids['ventana'])
            self.wids['e_numpedido'].set_text(pedido.numpedido)
            return
        # Desactivo momentáneamente el notificador:
        # Esto es necesario para que no avise del cambio que voy a 
        # hacer a continuación, ya que el usuario SABE que lo ha 
        # actualizado y además los cambios los va a ver inmediatamente.
        pedido.notificador.desactivar()
        # Actualizo los atributos del objeto:
        pedido.numpedido = numpedido
        pedido.descuento = descuento
        try:
            pedido.fecha = fecha
        except:
            print 'ERROR: Pedidos de compra: No se pudo "parsear" la fecha. Se usará la fecha actual.'
            pedido.fecha = time.localtime()
        pedido.proveedor = idproveedor
        pedido.iva=iva
        bounds = self.wids['txt_entregas'].get_buffer().get_bounds()
        pedido.entregas = self.wids['txt_entregas'].get_buffer().get_text(bounds[0], bounds[1])
        bounds = self.wids['txt_observaciones'].get_buffer().get_bounds()
        pedido.observaciones = self.wids['txt_observaciones'].get_buffer().get_text(bounds[0], bounds[1])
        pedido.formaDePago = forma_de_pago
        pedido.cerrado = self.wids['ch_cerrado'].get_active()
        pedido.bloqueado = self.wids['ch_bloqueado'].get_active()
        pedido.direccionEntrega0 = self.wids['e_direntrega0'].get_text()
        pedido.direccionEntrega1 = self.wids['e_direntrega1'].get_text()
        pedido.direccionEntrega2 = self.wids['e_direntrega2'].get_text()
        pedido.responsable0 = self.wids['e_responsable0'].get_text()
        pedido.responsable1 = self.wids['e_responsable1'].get_text()
        pedido.portes0 = self.wids['e_portes0'].get_text()
        pedido.portes1 = self.wids['e_portes1'].get_text()
        pedido.observaciones0 = self.wids['e_observaciones0'].get_text()
        pedido.observaciones1 = self.wids['e_observaciones1'].get_text()
        pedido.observaciones2 = self.wids['e_observaciones2'].get_text()
        # Fuerzo la actualización la BD y no espero a que SQLObject lo haga 
        # por mí:
        pedido.sync()
        # Vuelvo a activar el notificador:
        pedido.notificador.activar(self.aviso_actualizacion)
        self.actualizar_ventana()
        self.wids['b_guardar'].set_sensitive(False)

    def ver_envios(self, widget):
      """
      Busca y muestra, en una ventana aparte, los envíos
      relacionados con el pedido actual a través de los
      albaranes que contienen uno y otro siguiendo las
      líneas de venta del pedido.
      """
      utils.dialogo_info('FUNCIÓN DESHABILITADA', 
                         'Función deshabilitada temporalmente.', 
                         padre = self.wids['ventana'])

    def ver_vencimientos(self, widget):
      """
      Muestra los vencimientos del pedido actual
      en un diálogo de resultados de búsqueda.
      """
      utils.dialogo_info('FUNCIÓN DESHABILITADA', 'Función deshabilitada temporalmente.', padre = self.wids['ventana'])
      
    def ver_pagos(self, widget):
      """
      Muestra los pagos del pedido actual en una ventana de 
      resultados.
      """
      utils.dialogo_info('FUNCIÓN DESHABILITADA', 'Función deshabilitada temporalmente.', padre = self.wids['ventana'])

    def ver_facturas(self, widget):
      """
      Muestra las facturas relacionadas con el pedido
      a través de las líneas de venta en una ventana
      de resultados de búsqueda.
      """
      utils.dialogo_info('FUNCIÓN DESHABILITADA', 'Función deshabilitada temporalmente.', padre = self.wids['ventana'])

    def ver_abonos(self, widget):
      """
      Muestra los abonos relacionados con las líneas
      de venta que contiene el pedido actual en una
      ventana de resultados.
      """
      utils.dialogo_info('FUNCIÓN DESHABILITADA', 'Función deshabilitada temporalmente.', padre = self.wids['ventana'])

    def imprimir(self,boton):
        """
        Crea un impreso del pedido.
        OJO: Sólo imprime aquellas líneas pendientes de recibir.
        """
        self.guardar(None)  # Si se ha olvidado guardar, guardo yo.
        import informes
        pedido = self.objeto
        pednum = pedido.numpedido
        if pedido.proveedor == None:
            utils.dialogo_info(titulo = 'ERROR', 
                               texto = 'El pedido no tiene un proveedor asociado', 
                               padre = self.wids['ventana'])
        else:
            proveedor = {}
            proveedor['nombre'] = pedido.proveedor.nombre
            proveedor['direccion'] = pedido.proveedor.direccion
            proveedor['direccion2'] = "%s %s %s %s" % (pedido.proveedor.cp and "%s, " % (pedido.proveedor.cp) or "", 
                                                       pedido.proveedor.ciudad, 
                                                       pedido.proveedor.ciudad and "(%s)" % (pedido.proveedor.provincia) or pedido.proveedor.provincia, 
                                                       pedido.proveedor.pais and "; %s" % (pedido.proveedor.pais) or "")
            proveedor['telefono'] = pedido.proveedor.telefono
            proveedor['fax'] = pedido.proveedor.fax
            proveedor['cif'] = pedido.proveedor.cif
            proveedor['contacto'] = pedido.proveedor.contacto
            proveedor['formadepago'] = pedido.proveedor.formadepago
            proveedor['correoe'] = pedido.proveedor.correoe
            fecha = utils.str_fecha(pedido.fecha)
            descuento = self.wids['e_descuento'].get_text()
            iva = self.wids['e_iva'].get_text()
            subtotal =  self.wids['e_bruto'].get_text()
            totalIVA =  self.wids['e_totaliva'].get_text()
            totalDescuento = self.wids['e_neto'].get_text()
            total =  self.wids['e_total'].get_text()
            general = {'pednum': pednum, 
                       'proveedor': proveedor, 
                       'fecha':fecha, 
                       'iva': iva, 
                       'descuento': descuento, 
                       'subtotal':subtotal, 
                       'totalIVA': totalIVA, 
                       'totalDescuento': totalDescuento, 
                       'total': total}        
            lineas = []
            for l in pedido.lineasDePedidoDeCompra:
                # if l.albaranEntrada != None:
                #    continue    # Me salto las líneas que ya hayan sido "albaraneadas" (je).
                cantidad = '%s %s' % (utils.float2str(l.cantidad), l.productoCompra.unidad)
                if l.descuento != 0:
                    precio = "%s (dto:%s %%)" % (utils.float2str(l.precio, 4, autodec = True), utils.float2str(l.descuento * 100, 0))
                else:
                    precio = utils.float2str(l.precio, 4, autodec = True)
                textoEntrega = l.textoEntrega != None and l.textoEntrega or ""
                lineas.append({'codigo': l.productoCompra.codigo, 
                               'descripcion': l.productoCompra.descripcion, 
                               'cantidad': cantidad, 
                               'precio': precio,
                               'entrega': "%s %s" % (utils.str_fecha(l.fechaEntrega), textoEntrega)})
            bounds = self.wids['txt_entregas'].get_buffer().get_bounds()
            txtEntregas = self.wids['txt_entregas'].get_buffer().get_text(bounds[0], bounds[1])
            entregas = txtEntregas.split('\n')
            observaciones = pedido.observaciones
            forma_pago = pedido.formaDePago
            #informes.abrir_pdf(geninformes.pedidoCompra(general, proveedor, lineas, entregas, observaciones, forma_pago))
            informes.abrir_pdf(geninformes.pedidoCompra(general, 
              proveedor, 
              lineas, 
              entregas, 
              observaciones, 
              forma_pago, 
              pedido.direccionEntrega0, 
              pedido.direccionEntrega1, 
              pedido.direccionEntrega2, 
              pedido.responsable0, 
              pedido.responsable1, 
              pedido.portes0, 
              pedido.portes1, 
              mostrar_precios = self.wids['ch_imprimir_precios'].get_active(),
              observaciones0 = pedido.observaciones0, 
              observaciones1 = pedido.observaciones1))
              #observaciones2 = pedido.observaciones2)) <- Ya no hace falta, 
              # se pasa directamente en forma_pago. Contienen lo mismo a no 
              # ser que se deje en blanco observaciones2 en esta ventana y se 
              # rellene la forma de pago teniendo nivel 0 ó 1.
        
if __name__=='__main__':
    p = PedidosDeCompra()


