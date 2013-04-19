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
## productos_compra.py - Catálogo de Materias prima (compra).      
###################################################################
## NOTAS:
##  
##  
###################################################################
## Changelog:
## 9 de octubre de 2005 -> Inicio 
## 9 de octubre de 2005 -> 90% funcional (faltan fichas de prod.)
## 9 de enero de 2006 -> Separación de tipos de productos en 
##                       diferentes ventanas.
## 29 de enero de 2005 -> Portado a versión 02.
## 27 de noviembre de 2005 -> Añadido TreeViews de historiales.
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
from framework.seeker import VentanaGenerica
from utils import _float as float

class ProductosCompra(Ventana, VentanaGenerica):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self._objetoreciencreado = None
        Ventana.__init__(self, 'productos_compra.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_articulos/clicked': self.ver_articulos,
                       'b_tarifas/clicked': self.ver_tarifas,
                       'b_nuevo/clicked': self.crear_nuevo_producto,
                       'b_borrar/clicked': self.borrar_producto,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_anterior/clicked': self.ir_a_anterior,
                       'b_siguiente/clicked': self.ir_a_siguiente,
                       'b_buscar/clicked': self.buscar_producto, 
                       'b_tabla/clicked': self.abrir_productos_en_tabla, 
                       'ch_obsoleto/toggled': self.actualizar_estado_controles}
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        gtk.main()


    # --------------- Funciones auxiliares ------------------------------
    def es_diferente(self):
        """
        Devuelve True si la información en pantalla es distinta a la
        del objeto en memoria.
        """
        producto = self.objeto
        if producto == None: return False    # Si no hay producto activo, 
        # devuelvo que no hay cambio respecto a la ventana
        # Datos a comparar:
        # - código <-> e_codigo
        # - descripción <-> e_descripcion
        # - idtipodematerial <-> cb_tipo
        # - nombre <-> e_nombre
        # - preciopordefecto <-> e_precio
        # - minimo <-> e_minimo
        # - unidad <-> e_unidad
        condicion = producto.codigo == self.wids['e_codigo'].get_text()
        if pclases.DEBUG and not condicion:
            print "productos_compra::es_diferente -> %s ha cambiado" % (
                "e_codigo")
        condicion = condicion and (
            producto.descripcion == self.wids['e_descripcion'].get_text())
        if pclases.DEBUG and not condicion:
            print "productos_compra::es_diferente -> %s ha cambiado" % (
                "e_descripcion")
        condicion = condicion and (
            producto.tipoDeMaterialID == utils.combo_get_value(
                self.wids['cb_tipo']))
        condicion = condicion and (
            producto.proveedorID == utils.combo_get_value(
                self.wids['cb_proveedor']))
        if pclases.DEBUG and not condicion:
            print "productos_compra::es_diferente -> %s ha cambiado" % (
                "cb_tipo")
        condicion = condicion and (
            self.wids['ch_control_existencias'].get_active() 
                == producto.controlExistencias)
        if pclases.DEBUG and not condicion:
            print "productos_compra::es_diferente -> %s ha cambiado" % (
                "ch_control_existencias")
        condicion = condicion and (
            self.wids['e_precio_defecto'].get_text() 
                == "%s €" % (utils.float2str(producto.precioDefecto)))
        if pclases.DEBUG and not condicion:
            print "productos_compra::es_diferente -> %s ha cambiado" % (
                "e_precio_defecto")
        if producto.controlExistencias:
            condicion = condicion and (
                utils.float2str(producto.minimo) 
                    == self.wids['e_minimo'].get_text())
            if pclases.DEBUG and not condicion:
                print "productos_compra::es_diferente -> %s ha cambiado" % (
                    "e_minimo")
            condicion = condicion and (
                utils.float2str(producto.existencias) 
                    == self.wids['e_stock'].get_text())
            if pclases.DEBUG and not condicion:
                print "productos_compra::es_diferente -> %s ha cambiado" % (
                    "e_stock")
            condicion = condicion and (
                producto.unidad == self.wids['e_unidad'].get_text())
            if pclases.DEBUG and not condicion:
                print "productos_compra::es_diferente -> %s ha cambiado" % (
                    "e_unidad")
        condicion = (condicion and self.objeto.observaciones==self.leer_valor(
            pclases.ProductoCompra._SO_columnDict["observaciones"], 
            'txt_observaciones'))
        if pclases.DEBUG and not condicion:
            print "productos_compra::es_diferente -> %s ha cambiado" % (
                "txt_observaciones")
        # Obsoleto se actualiza automáticamente. No hace falta comparar.
        return not condicion    # Concición verifica que sea igual

    def aviso_actualizacion(self):
        """
        Muestra una ventana modal con el mensaje de objeto 
        actualizado.
        """
        if (self.objeto.existencias != self.objeto.swap['existencias'] 
            and (not self.usuario or self.usuario.nivel > 1)):
            # No dejo decidir al usuario, actualizo las existencias para 
            # ajustarlas a la cantidad de la BD y evitar que machaque el 
            # cambio de stock remoto con un valor local obsoleto.
            self.wids['e_stock'].set_text(
                utils.float2str(self.objeto.existencias))
            self.objeto.make_swap()
            color=self.wids['e_stock'].get_colormap().alloc_color("IndianRed1")
            self.wids['e_stock'].modify_bg(gtk.STATE_NORMAL, color)
            self.rellenar_existencias_almacen(self.objeto)
        else:
            utils.dialogo_info('ACTUALIZAR',
                           'El producto ha sido modificado remotamente.\nDeb'\
                           'e actualizar la información mostrada en pantalla'\
                           '.\nPulse el botón «Actualizar»', 
                           padre = self.wids['ventana'])
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
        # Inicialización del resto de widgets:
        utils.rellenar_lista(self.wids['cb_tipo'], 
                             [(t.id, t.descripcion) 
                              for t in pclases.TipoDeMaterial.select()])
        utils.rellenar_lista(self.wids['cbe_valoracion'], 
                             ((0, "Función por defecto"), 
                              (1, "Precio medio"), 
                              (2, "Precio último pedido"), 
                              (3, "Precio última entrada en almacén"), 
                              (4, "Usar precio por defecto especificado")))   
        # FIXME: Qué poco me gustan los valores HARCODED. Si no fuera 
        # porque voy justito de tiempo...
        self.wids['cbe_valoracion'].connect("changed", 
                                            self.rellenar_info_valoracion)
        cols = (('Fecha', 'gobject.TYPE_STRING', False, True, True, None), 
                ('Existencias', 'gobject.TYPE_FLOAT', True, True, False, 
                    self.cambiar_cant_historial), 
                ('Observaciones', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_obs_historial), 
                ('Almacén', 'gobject.TYPE_STRING', False, True, False, None), 
                ('id', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_hist'], cols)
        self.wids['tv_hist'].connect("row-activated", 
                                     self.actualizar_historico)
        cols = (('Nº Albarán', 'gobject.TYPE_STRING', False,True,True,None), 
                ('Fecha', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Cantidad', 'gobject.TYPE_STRING', False, True, False, None),
                ('Precio', 'gobject.TYPE_STRING', False, True, False, None),
                ('Silo', 'gobject.TYPE_STRING', False, True, False, None),
                ('Proveedor', 'gobject.TYPE_STRING', False,True,False,None), 
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_entradas'], cols)
        self.wids['tv_entradas'].connect("row-activated", self.abrir_albaran)
        cols = (('Fecha', 'gobject.TYPE_STRING', False, True, True, None), 
                ('Cantidad', 'gobject.TYPE_FLOAT', False, True, False, None), 
                ('Silo', 'gobject.TYPE_STRING', False, True, False, None), 
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_consumos'], cols)
        cols = (('Nº Albarán', 'gobject.TYPE_STRING', False,True,True,None), 
                ('Fecha', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Cantidad', 'gobject.TYPE_FLOAT', False, True, False, None),
                ('Cliente', 'gobject.TYPE_STRING', False, True, False, None),  
                ('Servido desde', 'gobject.TYPE_STRING',False,True,False,None),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_salidas'], cols)
        cols = (('Tarifa', 'gobject.TYPE_STRING', False, True, True, None), 
                ('Precio costo', 'gobject.TYPE_STRING',False,True,False,None), 
                ('Precio tarifa', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_precio_tarifa), 
                ('Porcentaje', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_porcentaje_tarifa), 
                ('Precio +21% IVA', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_pvp_tarifa), 
                ('Vigente', 'gobject.TYPE_BOOLEAN', False, True, False, None), 
                ('Hasta', 'gobject.TYPE_STRING', False, True, False, None), 
                ('ID_Tarifa', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_tarifas'], cols)
        cols = (('Almacén', 'gobject.TYPE_STRING', False, True, True, None), 
                ('Existencias', 'gobject.TYPE_STRING',False,True,False,None),
                ('IDAlmacen', 'gobject.TYPE_INT64',False,False,False,None))
        utils.preparar_listview(self.wids['tv_existencias'], cols)
        # context-menu
        menu = gtk.Menu()
        def insertar_texto_en_entry(menuentry, 
                                    texto, 
                                    w = self.wids['e_descripcion']):
            pos = w.get_position()
            w.insert_text(texto, pos)
            w.set_position(pos + len(texto.decode("utf-8")))
        menu_item = gtk.MenuItem("Insertar «ø»")
        menu.append(menu_item)
        menu_item.connect("activate", insertar_texto_en_entry, "ø")
        menu_item.show()
        menu_item = gtk.MenuItem("Insertar «½»")
        menu.append(menu_item)
        menu_item.connect("activate", insertar_texto_en_entry, "½")
        menu_item.show()
        menu_item = gtk.MenuItem("Insertar «²»")
        menu.append(menu_item)
        menu_item.connect("activate", insertar_texto_en_entry, "²")
        menu_item.show()
        menu_item = gtk.MenuItem("Insertar «³»")
        menu.append(menu_item)
        menu_item.connect("activate", insertar_texto_en_entry, "³")
        menu_item.show()
        self.wids['e_descripcion'].connect_object("event", 
                                                  self.e_descripcion_menu, 
                                                  menu)
        # XXX: No dejo cambiar manualmente las existencias a no ser que 
        # tenga nivel 0 (admin) o 1 (alto). Al crear un producto nuevo las 
        # existencias por defecto siempre son 0, así que para cambiarlas se 
        # tendrán que seguir los procedimientos lógicos de añadir por albarán 
        # de entrada o sacar por albaranes de salida o TPV.
        self.wids['e_stock'].set_property("editable", 
            (not self.usuario) or (self.usuario.nivel <= 1))
        # XXX: Me ha pillado el toro de la migración de libglade a GtkBuilder.
        self.wids['lproveedor_defecto'] = gtk.Label("Por defecto:")
        self.wids['cb_proveedor'] = gtk.ComboBox()
        utils.rellenar_lista(self.wids['cb_proveedor'], 
                             [(t.id, 
                                len(t.nombre) < 40 
                                and t.nombre 
                                or t.nombre[:40] + "...") 
                              for t in pclases.Proveedor.select(
                                  orderBy = "nombre")])
        self.wids['table2'].attach(self.wids['lproveedor_defecto'], 2, 3, 7, 8)
        self.wids['table2'].attach(self.wids['cb_proveedor'], 3, 4, 7, 8, 
            yoptions = gtk.EXPAND)
        self.wids['lproveedor_defecto'].show()
        self.wids['cb_proveedor'].show()
        #self.wids['table2'].remove(self.wids['e_proveedores'])
        self.wids['table2'].attach(self.wids['e_proveedores'], 1, 2, 7, 8)

    def e_descripcion_menu(self, widget, event):
        """
        Muestra el menú contextual de símbolos.
        """
        if event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
            widget.popup(None, None, None, event.button, event.time)
            return True
        return False

    def abrir_albaran(self, tv, path, vc):
        """
        Abre el albarán de entrada seleccionado.
        """
        if self.usuario != None and self.usuario.nivel >= 1:
            return
        idldc = tv.get_model()[path][-1]
        ldc = pclases.LineaDeCompra.get(idldc)
        albaran = ldc.albaranEntrada
        if albaran != None:
            from formularios import albaranes_de_entrada
            ventana = albaranes_de_entrada.AlbaranesDeEntrada(albaran)  # @UnusedVariable

    def actualizar_historico(self, tv, path, view_col):
        """
        Fuerza a actualizar el registro histórico seleccionado.
        """
        if self.usuario != None and self.usuario.nivel > 0:
            return
        ide = tv.get_model()[path][-1]
        h = pclases.HistorialExistenciasCompra.get(ide)
        fecha = h.fecha
        producto = h.productoCompra
        almacen = h.almacen
        # print "Recontando..."
        tal = producto.get_existencias_historico(fecha, forzar = True,  # @UnusedVariable
            actualizar = True, almacen = almacen)
        # print tal
        self.rellenar_historial(producto)

    def cambiar_cant_historial(self, cell, path, texto):
        """
        Cambia la cantidad del registro historial si el nivel 
        del usuario lo permite.
        """
        # NOTA: El único usuario que lo va a poder hacer es el administrador. 
        #       Que ya está bien la cosa.
        model = self.wids['tv_hist'].get_model()
        ide = model[path][-1]
        try:
            cantidad = float(texto)
        except ValueError:
            return
        if self.usuario == None or self.usuario.nivel == 0:
            h = pclases.HistorialExistenciasCompra.get(ide)
            h.cantidad = cantidad
            model[path][1] = h.cantidad

    def cambiar_obs_historial(self, cell, path, texto):
        """
        Cambia las observaciones del registro historial.
        """
        model = self.wids['tv_hist'].get_model()
        ide = model[path][-1]
        h = pclases.HistorialExistenciasCompra.get(ide)
        h.observaciones = texto
        model[path][2] = h.observaciones

    def activar_widgets(self, s, chequear_permisos = True):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        ws = ('e_idproducto', 'e_codigo', 'e_descripcion',
              'e_minimo', 'e_stock',  
              'e_unidad', 'b_borrar', 'b_articulos',
              'b_tarifas', 'e_precio_defecto', 
              'tv_hist', 'tv_entradas', 'tv_consumos', 'tv_salidas', 
              'table3', 'vbox2', 'cb_tipo', 'ch_control_existencias', 
              'txt_observaciones') 
        for w in ws:
            self.wids[w].set_sensitive(s)
        if chequear_permisos:
            self.check_permisos(nombre_fichero_ventana = "productos_compra.py")
        # Como la restricción de productos obsoletos es preferente respecto a 
        # los permisos...
        self.actualizar_estado_controles(self.wids['ch_obsoleto'])

    def ir_a_primero(self):
        """
        Hace que el primer registro -si lo hay- de la tabla implicada
        en el objeto del formulario sea el objeto activo.
        """
        producto = self.objeto
        try:
            # Anulo el aviso de actualización del envío que deja de ser activo.
            if producto != None: 
                producto.notificador.set_func(lambda : None)
            # Selecciono todos y me quedo con el primero de la lista
            producto = pclases.ProductoCompra.select(orderBy = "-id")[0]
            # Activo la notificación
            producto.notificador.activar(self.aviso_actualizacion) 
        except:
            producto = None     
        self.objeto = producto
        self.actualizar_ventana()

    def ir_a_anterior(self,widget):
        """
        Hace que el registro anterior (ordenados por ID interno)
        sea el objeto activo
        """
        producto = self.objeto
        if producto!=None:
            producto.notificador.desactivar()
        try:
            anterior = pclases.ProductoCompra.select(
                pclases.AND(pclases.ProductoCompra.q.id < producto.id), 
                orderBy='-id')[0]
        except IndexError:
            utils.dialogo_info(texto = "El elemento seleccionado es el primero"
                                       " registrado en el sistema",
                               titulo="ERROR")
            return
        self.objeto = anterior
        self.objeto.notificador.activar(self.aviso_actualizacion)
        self.actualizar_ventana()
        
    def ir_a_siguiente(self,widget):
        """
        Hace que el siguiente registro (ordenados por ID interno)
        sea el objeto activo
        """
        producto = self.objeto
        if producto!=None:
            producto.notificador.desactivar()
        try:
            siguiente = pclases.ProductoCompra.select(pclases.AND(
                            pclases.ProductoCompra.q.id > producto.id), 
                            orderBy='id')[0]
        except IndexError:
            utils.dialogo_info(texto = "El elemento seleccionado es el último"
                                       " registrado en el sistema",
                               titulo="ERROR")
            return
        self.objeto = siguiente
        self.objeto.notificador.activar(self.aviso_actualizacion)
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
            filas_res.append(
                (r.id, 
                 r.codigo, 
                 r.descripcion, 
                 r.controlExistencias and r.existencias or "-", 
                 r.precioDefecto, 
                 r.tipoDeMaterial and r.tipoDeMaterial.descripcion or "", 
                 r.proveedor and r.proveedor.nombre or "", 
                 r.obsoleto))
        idproducto = utils.dialogo_resultado(filas_res,
                                             titulo = 'Seleccione producto',
                                             cabeceras = ('ID Interno', 
                                                    'Código', 
                                                    'Descripción', 
                                                    'Existencias', 
                                                    'Precio defecto', 
                                                    'Tipo de material',
                                                    'Proveedor por defecto',
                                                    'Obsoleto'), 
                                             padre = self.wids['ventana'])
        if idproducto < 0:
            return None
        else:
            return idproducto

    def rellenar_info_valoracion(self, combo):
        """
        Guarda el valor elegido en el registro del producto de compra y 
        muestra el cálculo de la valoración en función del valor seleccionado.
        """
        self.objeto.fvaloracion = combo.child.get_text()
        self.objeto.sync()
        self.rellenar_calculo_valoracion()

    def rellenar_calculo_valoracion(self):
        """
        Introduce los valores calculados de la valoración del producto.
        """
        precio = self.objeto.get_precio_valoracion()
        self.wids['e_valoracion_precio'].set_text(
                    "%s €" % (utils.float2str(precio, 3)))
        self.wids['e_valoracion_total'].set_text(
                    "%s €" % (utils.float2str(self.objeto.existencias*precio)))
        self.wids['e_valoracion_existencias'].set_text(
                    "%s %s" % (utils.float2str(self.objeto.existencias), 
                               self.objeto.unidad))

    def rellenar_widgets(self):
        """
        Introduce la información del producto actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        producto = self.objeto
        self.wids['ventana'].set_title(
            "Productos de compra - %s" % (producto.descripcion))
        self.wids['ch_obsoleto'].set_active(producto.obsoleto)
        self.wids['e_codigo'].set_text(producto.codigo)
        self.wids['e_descripcion'].set_text(producto.descripcion)
        utils.combo_set_from_db(self.wids['cb_tipo'], 
                                producto.tipoDeMaterialID)
        utils.combo_set_from_db(self.wids['cb_proveedor'], 
                                producto.proveedorID)
        # Datos no modificables:
        self.wids['e_idproducto'].set_text(`producto.id`)
        self.wids['ch_control_existencias'].set_active(
            producto.controlExistencias)
        self.wids['e_precio_defecto'].set_text(
            "%s €" % (utils.float2str(producto.precioDefecto)))
        if producto.controlExistencias:
            self.wids['e_minimo'].set_text(utils.float2str(producto.minimo))
            try:
                self.wids['e_unidad'].set_text(producto.unidad)
            except TypeError:
                if producto.unidad == None:
                    producto.unidad = ''
                else:
                    producto.unidad = `producto.unidad`
                self.wids['e_unidad'].set_text(producto.unidad)
            self.wids['e_stock'].set_text(
                utils.float2str(producto.existencias))
            self.rellenar_historial(producto)
            self.rellenar_entradas(producto)
            self.rellenar_consumos(producto)
            self.rellenar_salidas(producto)
            self.rellenar_existencias_almacen(producto)
        for w in ("e_unidad", "e_stock", "e_minimo", "label117", "label15", 
                  "label14", "scrolledwindow1", "scrolledwindow2", 
                  "scrolledwindow3", "scrolledwindow4", 'table3'):
            self.wids[w].set_property("visible", producto.controlExistencias)
        funcs = {"Función por defecto": 0, 
                 "Precio medio": 1, 
                 "Precio último pedido": 2, 
                 "Precio última entrada en almacén": 3, 
                 "Usar precio por defecto especificado": 4, 
                 "": -1}
            # FIXME: Pero qué poco me gusta que esté HARCODED.
        utils.combo_set_from_db(self.wids['cbe_valoracion'], 
                                funcs[self.objeto.fvaloracion])
        self.rellenar_calculo_valoracion()  # Por si no ha cambiado el texto, 
                                            # fuerzo a mostrar la valoración.
        self.rellenar_tarifas()
        txt_proveedores = ", ".join([p.nombre for p in producto.proveedores])
        self.wids['e_proveedores'].set_text(txt_proveedores)
        self.escribir_valor(self.objeto._SO_columnDict["observaciones"], 
                            self.objeto.observaciones, 
                            'txt_observaciones')
        self.objeto.make_swap()
        self.wids['e_stock'].modify_bg(gtk.STATE_NORMAL, None)  # Por si se 
            # ha cambiado desde el aviso de actualización.
        self.actualizar_estado_controles(self.wids['ch_obsoleto'])

    def rellenar_existencias_almacen(self, producto):
        """
        Rellena las existencias de cada almacén para el producto.
        Relación inyectiva, muestra todos los almacenes y la cantidad para 
        cada uno o "-" si no hay registro.
        """
        model = self.wids['tv_existencias'].get_model()
        self.wids['tv_existencias'].set_model(None)
        model.clear()
        for a in pclases.Almacen.select(pclases.Almacen.q.activo == True, 
                                        orderBy = "id"):
            existencias = a.get_existencias(self.objeto)
            try:
                strexistencias = utils.float2str(existencias)
            except (TypeError, ValueError):
                strexistencias = "-"
            model.append((a.nombre, 
                          strexistencias, 
                          a.id))
        self.wids['tv_existencias'].set_model(model)

    def rellenar_tarifas(self):
        """
        Introduce el precio del producto para todas 
        las tarifas encontradas en la base de datos.
        """
        tarifas = pclases.Tarifa.select(orderBy = "nombre")
        model = self.wids['tv_tarifas'].get_model()
        model.clear()
        for tarifa in tarifas:
            preciotarifa = tarifa.obtener_precio(self.objeto)
            try:
                porcentaje = 100*((preciotarifa/self.objeto.precioDefecto)-1)
            except ZeroDivisionError:
                porcentaje = 0
            model.append((tarifa.nombre, 
                          utils.float2str(self.objeto.precioDefecto, 3, 
                                          autodec = True), 
                          utils.float2str(preciotarifa, 3, autodec = True), 
                          "%s %%" % (utils.float2str(porcentaje, 1)), 
                          utils.float2str(preciotarifa * 1.21, 2, 
                                          autodec = True), 
                          tarifa.esta_vigente(), 
                          not tarifa.periodoValidezFin 
                            and utils.str_fecha(tarifa.periodoValidezFin) 
                            or "", 
                          tarifa.id))

    def cambiar_precio_tarifa(self, cell, path, texto):
        model = self.wids['tv_tarifas'].get_model()
        idtarifa = model[path][-1]
        tarifa = pclases.Tarifa.get(idtarifa)
        try:
            nuevoprecio = utils.parse_euro(texto)
        except ValueError:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", 
                               texto = "El texto %s no es válido." % (texto), 
                               padre = self.wids['ventana'])
        else:
            if tarifa.obtener_precio(self.objeto) != nuevoprecio:
                tarifa.asignarTarifa(self.objeto, nuevoprecio)
                self.rellenar_tarifas()

    def cambiar_porcentaje_tarifa(self, cell, path, texto):
        model = self.wids['tv_tarifas'].get_model()
        idtarifa = model[path][-1]
        tarifa = pclases.Tarifa.get(idtarifa)
        try:
            porcentaje = utils.parse_porcentaje(texto, True)
        except ValueError:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", 
                               texto = "El texto %s no es válido." % (texto), 
                               padre = self.wids['ventana'])
        else:
            nuevoprecio = (1.0 + porcentaje) * self.objeto.precioDefecto
            if tarifa.obtener_precio(self.objeto) != nuevoprecio:
                tarifa.asignarTarifa(self.objeto, nuevoprecio)
                self.rellenar_tarifas()

    def cambiar_pvp_tarifa(self, cell, path, texto):
        model = self.wids['tv_tarifas'].get_model()
        idtarifa = model[path][-1]
        tarifa = pclases.Tarifa.get(idtarifa)
        try:
            nuevoprecio = utils.parse_euro(texto)
        except ValueError:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", 
                               texto = "El texto %s no es válido." % (texto), 
                               padre = self.wids['ventana'])
        else:
            nuevoprecio /= 1.21
            if tarifa.obtener_precio(self.objeto) != nuevoprecio:
                tarifa.asignarTarifa(self.objeto, nuevoprecio)
                self.rellenar_tarifas()

    def rellenar_entradas(self, producto):
        """
        Rellena la tabla de entradas del producto 
        en albaranes.
        """
        model = self.wids['tv_entradas'].get_model()
        self.wids['tv_entradas'].set_model(None)
        model.clear()
        total_entradas = total_precio = 0
        for ldc in producto.lineasDeCompra:
            if ldc.albaranEntrada != None:
                total_entradas += ldc.cantidad
                total_precio += ldc.get_subtotal()
                model.append((ldc.albaranEntrada.numalbaran, 
                              utils.str_fecha(ldc.albaranEntrada.fecha), 
                              utils.float2str(ldc.cantidad), 
                              utils.float2str(ldc.precio, 3), 
                              ldc.cargaSiloID 
                                and ldc.cargaSilo.silo.nombre or "-", 
                              ldc.albaranEntrada.proveedor 
                                and ldc.albaranEntrada.proveedor.nombre 
                                or "-", 
                              ldc.id))
        model.append(("", "   >>> TOTAL: ", utils.float2str(total_entradas), 
                      utils.float2str(total_precio), "", "", -1))
        self.wids['tv_entradas'].set_model(model)

    def rellenar_consumos(self, producto):
        """
        Rellena la tabla de consumos del producto.
        """
        model = self.wids['tv_consumos'].get_model()
        self.wids['tv_consumos'].set_model(None)
        model.clear()
        total_consumos = 0
        iters = {}
        for c in producto.consumos:
            fecha = (c.parteDeProduccion 
                     and utils.str_fecha(c.parteDeProduccion.fecha) or "-")
            if fecha not in iters:
                iters[fecha] = model.append(None, (fecha, c.cantidad, "", 0))
            else:
                model[iters[fecha]][1] += c.cantidad
            if fecha == "-":
                fechahoras = fecha
            else:
                fechahoras = "%s [%s-%s]" % (fecha, 
                    utils.str_hora_corta(c.parteDeProduccion.horainicio), 
                    utils.str_hora_corta(c.parteDeProduccion.horafin))
            model.append(iters[fecha], (fechahoras, c.cantidad, 
                                        c.siloID and c.silo.nombre or "", 
                                        c.id))
            total_consumos += c.cantidad
        model.append(None, ("   >>> TOTAL: ", total_consumos, "", -1))
        self.wids['tv_consumos'].set_model(model)


    def rellenar_salidas(self, producto):
        """
        Rellena la tabla de salidas del producto de 
        compra en líneas de venta.
        """
        model = self.wids['tv_salidas'].get_model()
        self.wids['tv_salidas'].set_model(None)
        model.clear()
        total_salidas = 0
        for ldv in producto.lineasDeVenta:
            if ldv.albaranSalida or ldv.ticket:
                docsalida = ""
                if ldv.albaranSalida:
                    docsalida = ldv.albaranSalida.numalbaran 
                elif ldv.ticket:
                    docsalida = "Ticket %s" % ldv.ticket.numticket
                try:
                    nombrealmacen = ldv.albaranSalida.almacenOrigen.nombre
                except AttributeError:
                    if ldv.ticket:
                        # Las ventas de TPV siempre son desde el almacén 
                        # principal. Ver tpv.py.
                        try:
                            nombrealmacen = ("TPV: " 
                              + pclases.Almacen.get_almacen_principal().nombre)
                        except Exception, e:
                            print e
                            self.logger.error("productos_compra.py"
                                "::rellenar_salidas -> %s" % e)
                            nombrealmacen = "ERROR"
                    else:
                        nombrealmacen = "N/D"
                model.append((docsalida, 
                              utils.str_fecha(ldv.albaranSalida 
                                              and ldv.albaranSalida.fecha 
                                              or ldv.ticket.fechahora), 
                              ldv.cantidad, 
                              ldv.albaranSalida 
                                and ldv.albaranSalida.clienteID 
                                and ldv.albaranSalida.cliente.nombre or "-", 
                              nombrealmacen, 
                              ldv.id))
            total_salidas += ldv.cantidad
        model.append(("", "    >>> TOTAL: ", total_salidas, "", "", -1))
        self.wids['tv_salidas'].set_model(model)

    def rellenar_historial(self, producto):
        """
        Rellena la tabla de la ventana con los registros 
        de historiales de existencias del producto.
        """
        model = self.wids['tv_hist'].get_model()
        self.wids['tv_hist'].set_model(None)
        model.clear()
        for h in producto.historialesExistenciasCompra:
            model.append((utils.str_fecha(h.fecha), 
                          h.cantidad != None and h.cantidad or 0.0, 
                          h.observaciones, 
                          h.almacen and h.almacen.nombre or "", 
                          h.id))
        self.wids['tv_hist'].set_model(model)

    # --------------- Manejadores de eventos ----------------------------
    
    def actualizar_estado_controles(self, ch):
        """
        Actualiza el estado (habilitado/deshabilitado) de los controles del 
        producto en función de si está marcado como obsoleto o no.
        """
        if not self.objeto:
            return
        self.objeto.sync()
        self.objeto.obsoleto = ch.get_active()
        self.objeto.syncUpdate()
        self.objeto.make_swap()
        nombrescontroles = ("e_codigo", "e_descripcion", "e_precio_defecto", 
                            "e_minimo", "e_stock", "e_unidad", "cb_tipo", 
                            "ch_control_existencias", "expander1")
        for nombrecontrol in nombrescontroles:
            control = self.wids[nombrecontrol]
            control.set_sensitive(not self.objeto.obsoleto)
        notebook = self.wids['notebook1']
        for npag in range(1, notebook.get_n_pages()):
            childcontainer = notebook.get_nth_page(npag)
            childcontainer.set_sensitive(not self.objeto.obsoleto)

    def crear_nuevo_producto(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        producto = self.objeto
        # Datos a pedir: Elementos con restriccion 'not null' en la tabla, 
        # idproducto y idtipodematerial.
        if producto != None:
            producto.notificador.set_func(lambda : None)
        tdmid = utils.combo_get_value(self.wids['cb_tipo'])
        producto = pclases.ProductoCompra(tipoDeMaterialID = tdmid,
                                          descripcion = '', 
                                          codigo = '', 
                                          unidad = 'ud.', 
                                          minimo = 0,
                                          existencias = 0, 
                                          obsoleto = False, 
                                          proveedor = None)
        pclases.Auditoria.nuevo(producto, self.usuario, __file__)
        self._objetoreciencreado = producto
        utils.dialogo_info('PRODUCTO CREADO',  
                           'Se ha creado un producto nuevo.\nA continuación '\
                           'complete la información del producto y guarde lo'\
                           's cambios.', 
                           padre = self.wids['ventana'])
        producto.notificador.set_func(self.aviso_actualizacion)
        self.objeto = producto
        self.actualizar_ventana()

    def abrir_productos_en_tabla(self, boton):
        """
        Abre la ventana "productos.py" donde se muestran todos los 
        productos y tarifas en tabla.
        """
        from formularios import productos
        ventana_tabla = productos.Productos(usuario = self.usuario)  # @UnusedVariable

    def buscar_producto(self, widget, a_buscar = ""):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        producto = self.objeto
        if not a_buscar:
            opciones = {'Ignorar productos obsoletos': True}
            a_buscar = utils.dialogo_entrada(titulo="BUSCAR PRODUCTO COMPRA", 
                        texto="Introduzca código o descripción de producto:", 
                        padre=self.wids['ventana'], 
                        opciones = opciones) 
        if a_buscar != None:
            resultados = utils.buscar_productos_compra(a_buscar, 
                incluir_obsoletos=not opciones['Ignorar productos obsoletos'])
            if resultados.count() == 0:
                try:
                    resultados = self.intentar_corregir_busqueda(a_buscar)
                    if (not resultados 
                        or (hasattr(resultados, "count") 
                            and resultados.count() == 0)):
                        raise ImportError   # Me vale aunque no sea verdad.
                except ImportError:
                    utils.dialogo_info('SIN RESULTADOS', 
                                   'La búsqueda no produjo resultados.\nPrue'\
                                   'be a cambiar el texto buscado o déjelo e'\
                                   'n blanco para ver una lista completa.\n('\
                                   'Atención: Ver la lista completa puede re'\
                                   'sultar lento si el número de elementos e'\
                                   's muy alto)', 
                                   padre = self.wids['ventana'])
                    return
            if resultados.count() > 1:
                ## Refinar los resultados
                idproducto = self.refinar_resultados_busqueda(resultados)
                if idproducto == None:
                    return
                resultados = [pclases.ProductoCompra.get(idproducto)]
            ## Un único resultado
            # Primero anulo la función de actualización
            if producto != None:
                producto.notificador.desactivar()
            # Pongo el objeto como actual
            self.objeto = resultados[0]
            # Y activo la función de notificación:
            self.objeto.notificador.set_func(self.aviso_actualizacion)
            self.actualizar_ventana()

    def intentar_corregir_busqueda(self, texto):
        """
        Por cada palabra recibida intenta sugerir una equivalente 
        encontrada en los códigos y descripciones de los productos.
        Aún está verde y en pruebas. No se debería recargar el corrector 
        en cada búsqueda fallida, entre otras cosas.
        Lanzará un ImportError si no se puede cargar el módulo corrector.
        Devuelve False si no se 
        """
        from lib import spelling    # Antes de hacer nada más, para no 
                                    # perder tiempo en caso de error.
        txtbase = []
        for pc in pclases.ProductoCompra.select():
            txtbase.append(pc.codigo.lower())
            txtbase.append(pc.descripcion.lower())
        txtbase = " ".join(txtbase)
        corrector = spelling.SpellCorrector(txtbase)
        sugerencia_completa = []
        texto = " ".join(texto.split()).lower()
        for palabra in texto.split():
            sugerencia = corrector.correct(palabra)
            sugerencia_completa.append(sugerencia)
        sugerencia_completa = " ".join(sugerencia_completa)
        if (sugerencia_completa != texto and 
            utils.buscar_productos_compra(sugerencia_completa).count() > 0 and 
            # ¿Para qué sugerir nada si sabemos que no se va a encontrar? 
            utils.dialogo(titulo = "SUGERENCIA DE BÚSQUEDA", 
                          texto = "No se encontraron coincidencias.\n"
                                  "¿Tal vez quiso decir «%s»?" 
                                        % sugerencia_completa, 
                          padre = self.wids['ventana'])):
            res = utils.buscar_productos_compra(sugerencia_completa)
        else:
            res = []
        return res

    def guardar(self, widget):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        producto = self.objeto
        codigo = self.wids['e_codigo'].get_text()
        producto.observaciones = self.leer_valor(
            pclases.ProductoCompra._SO_columnDict["observaciones"], 
            'txt_observaciones')
        # Control de código duplicado.
        if codigo.strip():
            dupe = pclases.ProductoCompra.select(pclases.AND(
                pclases.ProductoCompra.q.codigo == codigo, 
                pclases.ProductoCompra.q.id != producto.id))
            if dupe.count():
                producto.observaciones += "\nCódigo duplicado: %s" % codigo
                codigo = ""
        ## EOControl de código duplicado.
        descripcion = self.wids['e_descripcion'].get_text()
        idtipo = utils.combo_get_value(self.wids['cb_tipo'])
        producto.controlExistencias \
            = self.wids['ch_control_existencias'].get_active()
        try:
            minimo = float(self.wids['e_minimo'].get_text())
        except ValueError:
            minimo = producto.minimo
        try:
            unidad = self.wids['e_unidad'].get_text()
        except ValueError:
            unidad = producto.unidad
        try:
            existencias = float(self.wids['e_stock'].get_text())
        except:
            existencias = producto.existencias
        try:
            precio = utils.parse_euro(self.wids['e_precio_defecto'].get_text())
        except ValueError:
            precio = 0
        if precio != self.objeto.precioDefecto:
            self.logger.warning("productos_compra::guardar -> El precio del "\
                "producto %s ha cambiado, cambiando precio de tarifas vigent"\
                "es para conservar porcentajes. Precio antiguo: %f. Precio n"\
                "uevo: %f" % (self.objeto.descripcion, 
                              self.objeto.precioDefecto, 
                              precio))
            for tarifa in pclases.Tarifa.select():
                if tarifa.vigente:
                    porcentaje = tarifa.get_porcentaje(self.objeto, 
                                                       fraccion = True)
                    nuevoprecio = precio * (1.0 + porcentaje)
                    tarifa.asignarTarifa(self.objeto, nuevoprecio)
        # Desactivo el notificador momentáneamente
        producto.notificador.set_func(lambda: None)
        # Actualizo los datos del objeto
        self.objeto.precioDefecto = precio
        producto.codigo = codigo
        producto.descripcion = descripcion
        producto.idtipodematerialID = idtipo
        producto.minimo = minimo
        producto.unidad = unidad
        producto.existencias = existencias
        producto.tipoDeMaterialID = utils.combo_get_value(self.wids['cb_tipo'])
        producto.proveedorID = utils.combo_get_value(self.wids['cb_proveedor'])
        # Fuerzo la actualización de la BD y no espero a SQLObject:
        producto.syncUpdate()
        # Vuelvo a activar el notificador
        producto.notificador.set_func(self.aviso_actualizacion)
        self.objeto = producto
        self.actualizar_ventana()
        # No hace falta guardar «obsoleto» se autoguarda en el evento toggled.
        self.wids['b_guardar'].set_sensitive(False)

    def borrar_producto(self, widget):
        """
        Elimina el producto de la tabla pero NO
        intenta eliminar ninguna de sus relaciones,
        de forma que si se incumple alguna 
        restricción de la BD, cancelará la eliminación
        y avisará al usuario.
        """
        producto = self.objeto
        if not utils.dialogo("""
            Si borra un producto no podrá volver a recuperarlo y               
            se eliminará también de aquellos pedidos, albaranes y              
            facturas donde aparezca, pudiendo causar incoherencias.            
                                                                               
            ¿Está absolutamente seguro de querer eliminar el producto?""", 
            'BORRAR', 
            padre = self.wids['ventana']):
            return
        try:
            numlineas = len(producto.lineasDeCompra) \
                        + len(producto.lineasDePedido) \
                        + len(producto.lineasDePedidoDeCompra) \
                        + len(producto.lineasDeVenta)
            if (numlineas > 0 \
                and utils.dialogo("""
               El producto está implicado en %d operaciones de compra-venta.  
               Si lo borra del sistema se perderá la información relativa a   
               estas operaciones. Si no está seguro de lo que hace, cancele   
               este diálogo respondiendo «NO» y marque el producto como 
               obsoleto.                                
                                                                              
               ¿Desea continuar con la eliminación del producto?""" % (
                numlineas), 
                        titulo = "¿ESTÁ COMPLETAMENTE SEGURO DE ELIMINARLO?", 
                        padre = self.wids['ventana'])) or numlineas == 0:
                producto.notificador.set_func(lambda : None)
                # producto.destroy(ventana = __file__)
                producto.destroy_en_cascada(ventana = __file__)   # CWT
                self.objeto = None
                self.ir_a_primero()
        except: 
            utils.dialogo_info('PRODUCTO NO ELIMINADO', 
                               'El producto está implicado en operaciones '\
                               'que impiden su borrado.', 
                               padre = self.wids['ventana'])


    def ver_articulos(self, w):
        producto = self.objeto
        articulos = producto.articulos
        def ver_id(self, ldv):
            if ldv == None:
                return '-'
            else:
                return ldv.id
        ars = [(a.id, ver_id(a.idlineadeventa), ver_id(a.idlineadecompra), 
                             a.cantidad, a.unidad) for a in articulos]
        utils.dialogo_resultado(ars, 'ARTÍCULOS RELACIONADOS', 
            cabeceras=['ID', 'LDV', 'LDC', 'Cantidad', 'Unidad'])

    def ver_tarifas(self, w):
        producto = self.objeto
        tarifas = producto.tarifas
        tars = [(t.id, t.nombretarifa, t.descripcion, 
                 t.obtenerTarifa(producto)) for t in tarifas]
        utils.dialogo_resultado(tars, 'TARIFAS RELACIONADAS', 
            cabeceras=['ID', 'Nombre', 'Descripción', 'Precio'])


if __name__=='__main__':
    pclases.DEBUG = True
    v = ProductosCompra()
    
