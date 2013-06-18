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
## abonos_venta.py - Ventana de abonos sobre ventas facturadas.
###################################################################
## NOTAS:
## 
###################################################################
## Changelog:
## 14 de marzo de 2006 -> Inicio
## 16 de marzo de 2006 -> En pruebas
##
###################################################################
## TODO:
## Bloquear albarán si se genera factura de abono o algo así para 
## evitar que se descuente en una factura y después se machaque 
## con otra factura de abono nueva al regenerarla después de 
## haber modificado el albarán original que ya ha sido facturado.
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk, time
from framework import pclases
from formularios import reports
from informes import geninformes
import mx.DateTime 
from formularios.utils import _float as float

class AbonosVenta(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'abonos_venta.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_nuevo/clicked': self.crear_nuevo_abono,
                       'b_guardar/clicked': self.guardar,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_borrar/clicked': self.borrar_abono,
                       'b_buscar/clicked': self.buscar_abono,
                       'b_imprimir/clicked': self.imprimir,
                       'b_albaran_abono/clicked': self.generar_albaran,
                       'b_add_ajuste/clicked': self.add_ajuste,
                       'b_drop_ajuste/clicked': self.drop_ajuste,
                       'b_add_devolucion/clicked': self.add_devolucion,
                       'b_drop_devolucion/clicked': self.drop_devolucion,
                       'b_cliente/clicked': self.cambiar_cliente,
                       'b_fra_abono/clicked': self.generar_fra_abono,
                       'b_fecha/clicked': self.buscar_fecha 
                      }  
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
        abono = self.objeto
        if abono == None: return False    # Si no hay abono activo, devuelvo que 
                                        # no hay cambio respecto a la ventana
        condicion = self.wids['e_numabono'].get_text() == abono.numabono
        condicion = (condicion 
         and (utils.str_fecha(abono.fecha) == self.wids['e_fecha'].get_text()))
        condicion = (condicion 
         and abono.observaciones == self.wids['e_observaciones'].get_text())
        condicion = (condicion 
         and abono.almacenID==utils.combo_get_value(self.wids['cbe_almacen']))
        return not condicion    # Condición verifica que sea igual

    def aviso_actualizacion(self):
        """
        Muestra una ventana modal con el mensaje de objeto 
        actualizado.
        """
        utils.dialogo_info('ACTUALIZAR',
            'El abono ha sido modificado remotamente.\nDebe actualizar la inf'
            'ormación mostrada en pantalla.\nPulse el botón «Actualizar»', 
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
        # self.wids['b_fra_abono'].set_sensitive(False)
        # Inicialización del resto de widgets:
        cols = (('Código', 'gobject.TYPE_STRING', False, True, False, None),
                ('Descripción', 'gobject.TYPE_STRING', False,True,False,None),
                ('Cantidad facturada', 'gobject.TYPE_FLOAT', 
                    False, True, False, None),
                ('Precio factura', 'gobject.TYPE_FLOAT', 
                    False, False, False, None),
                ('Cantidad a ajustar', 'gobject.TYPE_FLOAT', 
                    True, False, False, self.cambiar_cantidad),
                ('Nuevo precio', 'gobject.TYPE_FLOAT', 
                    True, False, False, self.cambiar_nuevo_precio),
                ('Diferencia', 'gobject.TYPE_STRING', 
                    True, False, False, self.cambiar_diferencia),
                ('Total', 'gobject.TYPE_FLOAT', False, False, False, None),
                ('IDLDA', 'gobject.TYPE_INT64', False, False, False, None)
               )
        utils.preparar_listview(self.wids['tv_precios'], cols)
        cols = (('Código', 'gobject.TYPE_STRING', False, True, False, None),
                ('Código interno', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Descripción', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Albarán de procedencia', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Albarán abono', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Importe', 'gobject.TYPE_FLOAT', 
                    True, False, False, self.cambiar_importe_devolucion),
                ('Observaciones', 'gobject.TYPE_STRING', 
                    True, False, False, self.cambiar_observaciones_devolucion),
                ('IDLDD', 'gobject.TYPE_INT64', False, False, False, None)
               )
        utils.preparar_treeview(self.wids['tv_devoluciones'], cols)
        self.wids['e_total'].set_alignment(1.0)
        self.wids['e_bultos'].set_alignment(1.0)
        self.wids['e_cantidad'].set_alignment(1.0)
        utils.rellenar_lista(self.wids['cbe_almacen'], 
                        [(a.id, a.nombre) 
                         for a in pclases.Almacen.select(
                             pclases.Almacen.q.activo == True, 
                             orderBy = "nombre")])

    def activar_widgets(self, s):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        se_puede_imprimir = (self.wids['b_imprimir'].get_property("sensitive") 
                             or (self.objeto != None 
                             and self.objeto.facturaDeAbono != None))
        se_puede_generar_albaran_entrada \
            = self.wids['b_albaran_abono'].get_property("sensitive")
        try:
            permisos = self.usuario.get_permiso(__file__)
            self.wids['b_nuevo'].set_sensitive(permisos.nuevo)
            s = s and permisos.permiso
        except AttributeError:
            s = s and (self.usuario == None or self.usuario.nivel <= 2)
            if self.usuario and self.usuario.nivel > 2:
                self.wids['b_nuevo'].set_sensitive(False)
        ws = ('hbox1', 'hbox5', 'vbox2', 'hbox6', 'b_albaran_abono', 
              'b_fra_abono', 'b_add_ajuste', 'b_drop_ajuste', 
              'b_add_devolucion', 'b_drop_devolucion', 'b_borrar', 
              'cbe_almacen')
        for w in ws:
            self.wids[w].set_sensitive(s)
        self.wids['b_imprimir'].set_sensitive(se_puede_imprimir)
            # Imprimir se puede siempre, qué más da quién sea el usuario. Lo 
            # dejo como estaba antes de entrar aquí.
        self.wids['b_albaran_abono'].set_sensitive(
            se_puede_generar_albaran_entrada and s)
            # Debe quedar habilitado únicamente si ya lo estaba antes y se ha 
            # recibido que sensitive = True.
        if self.objeto:
            self.wids['cbe_almacen'].set_sensitive(
                not len(self.objeto.lineasDeDevolucion))

    def ir_a_primero(self):
        """
        Hace que el primer registro -si lo hay- de la tabla implicada
        en el objeto del formulario sea el objeto activo.
        """
        abono = self.objeto
        try:
            # Anulo el aviso de actualización del envío que deja de ser activo.
            if abono != None: abono.notificador.set_func(lambda : None)
            abono = pclases.Abono.select(orderBy = "-id")[0]    # Selecciono 
                                # todos y me quedo con el primero de la lista
            abono.notificador.set_func(self.aviso_actualizacion)    # Activo 
                                                            # la notificación
        except:
            abono = None     
        self.objeto = abono
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
            nombrecliente = [r.cliente and r.cliente.nombre or ''][0]
            tienefactura = r.facturaDeAbono == None and "No" or "Sí"
            filas_res.append((r.id, r.numabono, utils.str_fecha(r.fecha), 
                              nombrecliente, tienefactura))
        idabono = utils.dialogo_resultado(filas_res,
                                          titulo = 'Seleccione abono',
                                          cabeceras = ('ID', 
                                                       'Número de abono', 
                                                       'Fecha', 
                                                       'Cliente', 
                                                       'Factura de abono'), 
                                          padre = self.wids['ventana'])
        if idabono < 0:
            return None
        else:
            of_the_jedi = idabono
            return of_the_jedi  # Je

    def rellenar_widgets(self):
        """
        Introduce la información del abono actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        abono = self.objeto
        self.wids['e_numabono'].set_text(abono.numabono)
        self.wids['e_fecha'].set_text(utils.str_fecha(abono.fecha))
        self.wids['e_observaciones'].set_text(abono.observaciones)
        cliente = abono.cliente
        self.wids['hbox5'].set_sensitive(cliente != None)
        self.wids['vbox2'].set_sensitive(cliente != None)
        self.wids['hbox6'].set_sensitive(cliente != None)
        self.wids['hbuttonbox2'].set_sensitive(cliente != None)
        self.wids['e_cliente'].set_text(cliente and cliente.nombre or '')
        total = self.rellenar_ajustes()
        total += self.rellenar_devoluciones()   ## Rellena también los entry 
                            ## de bultos de entrada y cantidad (en m² o kg.)
        self.wids['e_total'].set_text("%s €" % (utils.float2str(total)))
        if total < 0:
            self.wids['e_total'].modify_text(gtk.STATE_NORMAL,
                self.wids['e_total'].get_colormap().alloc_color("red"))
        else:
            self.wids['e_total'].modify_text(gtk.STATE_NORMAL,
                self.wids['e_total'].get_colormap().alloc_color("black"))
        # Si no quedan artículos sin albarán de entrada, deshabilito el botón
        self.wids['b_albaran_abono'].set_sensitive(len([l for l 
            in self.objeto.lineasDeDevolucion 
            if l.albaranDeEntradaDeAbono == None]) >= 1)
        if abono.facturaDeAbono:
            self.wids['e_fra_abono'].set_text(abono.numabono)
            hijos = self.wids['b_fra_abono'].child.child.get_children()
            try:
                hijos[1].set_label("Eliminar\n factura \nde abono")
            except AttributeError:      # Si no es el 1 será el 0. Más no hay 
                                        # en el botón.
                hijos[0].set_label("Eliminar\n factura \nde abono")
            self.wids['b_imprimir'].set_sensitive(True)
        else:
            self.wids['e_fra_abono'].set_text("NO GENERADA")
            hijos = self.wids['b_fra_abono'].child.child.get_children()
            try:
                hijos[1].set_label("Generar\n factura \nde abono")
            except AttributeError:
                hijos[0].set_label("Generar\n factura \nde abono")
            self.wids['b_imprimir'].set_sensitive(False)
        self.wids['e_facturas'].set_text(", ".join([f.numfactura 
            for f in abono.facturasVenta]))
        self.wids['e_albaranes'].set_text(", ".join([a.numalbaran 
            for a in abono.albaranesSalida]))
        utils.combo_set_from_db(self.wids['cbe_almacen'], 
                                abono.almacenID, 
                                forced_value = abono.almacen 
                                                and abono.almacen.nombre
                                                or None)
        self.wids['e_cobro'].set_text(self.objeto.get_str_cobro())
        self.objeto.make_swap()

    def rellenar_ajustes(self):
        """
        Introduce las líneas de ajuste de precios del abono en el 
        listview y devuelve la suma de las diferencias de precios.
        """
        abono = self.objeto
        model = self.wids['tv_precios'].get_model()
        model.clear()
        total = 0
        ldas = abono.lineasDeAbono[:]
        try:
            ldas.sort(lambda x, y: int(x.id - y.id))
        except:     # ¿No tiene ID? Bua, pues no lo ordeno y punto.
            pass
        for lda in ldas:
            total += self.agregar_lda(lda, model)
        return total

    def agregar_lda(self, lda, model):
        try:
            # total = (lda.diferencia * lda.lineaDeVenta.cantidad)
            total = (lda.diferencia * lda.cantidad)
            model.append((lda.lineaDeVenta.producto.codigo,
                          lda.lineaDeVenta.producto.descripcion,
                          lda.lineaDeVenta.cantidad,
                          lda.lineaDeVenta.precio,
                          lda.cantidad,
                          lda.diferencia + lda.lineaDeVenta.precio,
                          utils.float2str(lda.diferencia, 
                                          precision = 10, autodec = True),
                          total,
                          lda.id))
            difcant = lda.lineaDeVenta.cantidad - lda.cantidad
            if difcant < 0:
                utils.dialogo_info(titulo = 'ABONO INCOHERENTE', texto = \
                """
                En el abono consta que se facturó %.2f de %s. Sin 
                embargo intenta abonar %.2f, que es superior a lo 
                facturado. Tal vez quiera crear una nueva factura           
                a cargar al con la diferencia (%.2f) en 
                lugar de un abono.                                          
                """ % (lda.lineaDeVenta.cantidad, 
                       lda.lineaDeVenta.producto.descripcion, 
                       lda.cantidad, abs(difcant)))
            elif difcant > 0:
                if len(self.objeto.lineasDeDevolucion) == 0:
                    utils.dialogo_info(titulo = 'ABONO INCOHERENTE', texto = \
                    """
                    Si la cantidad de producto facturado difiere de la del     
                    abono significa que se ha producido también una devolución 
                    de mercancía. Debe, por tanto, incluir en el abono las     
                    líneas de devolución correspondientes a esta diferencia    
                    entre material facturado y abonado por ajuste de precio.   
                    ¡Cree la devolución del material en el abono actual para   
                    no volver a ver este mensaje de error!                     
                    """)
        except AttributeError:  # No tiene LDV sino Servicio
#            total = (lda.diferencia * lda.servicio.cantidad)
            total = (lda.diferencia * lda.cantidad)
            model.append(("SERVICIO",
                          lda.servicio.concepto,
                          lda.servicio.cantidad,
                          lda.servicio.precio,
                          lda.cantidad,
                          lda.diferencia + lda.servicio.precio,
                          lda.diferencia,
                          total,
                          lda.id))
            difcant = lda.servicio.cantidad - lda.cantidad
            if difcant < 0:
                utils.dialogo_info(titulo = 'ABONO INCOHERENTE', texto = \
                """
                En el abono consta que se facturó %.2f de %s. Sin 
                embargo intenta abonar %.2f, que es superior a lo 
                facturado. Tal vez quiera crear una nueva factura           
                a cargar al con la diferencia (%.2f) en 
                lugar de un abono.                                          
                """ % (lda.servicio.cantidad, lda.servicio.concepto, 
                       lda.cantidad, difcant))
            elif difcant > 0:
                if len(self.objeto.lineasDeDevolucion) == 0:
                    utils.dialogo_info(titulo = 'ABONO INCOHERENTE', texto = \
                    """
                    Si la cantidad de producto facturado difiere de la del     
                    abono significa que se ha producido también una devolución 
                    de mercancía. Debe, por tanto, incluir en el abono las     
                    líneas de devolución correspondientes a esta diferencia    
                    entre material facturado y abonado por ajuste de precio.   
                    ¡Cree la devolución del material en el abono actual para   
                    no volver a ver este mensaje de error!                     
                    """)
        return total

    def rellenar_devoluciones(self):
        """
        Introduce las devoluciones del abono en el treeview y 
        devuelve el total de los importes de los artículos 
        devueltos según el precio de la factura/abono del que 
        procedan
        """
        abono = self.objeto
        model = self.wids['tv_devoluciones'].get_model()
        model.clear()
        total = 0
        metros = 0
        kilos = 0
        bultos = 0
        padres = {}
        for ldd in abono.lineasDeDevolucion:
            if ldd.articulo.productoVenta.id not in padres:
                padres[ldd.articulo.productoVenta.id] = []
            padres[ldd.articulo.productoVenta.id].append(ldd)
        for productoid in padres:
            iterpadre = self.agregar_producto_ldd(
                pclases.ProductoVenta.get(productoid), 
                model, 
                padres[productoid])
            for ldd in padres[productoid]:
                stotal, smetros, skilos, sbultos = self.agregar_ldd(ldd, 
                                                                    model, 
                                                                    iterpadre)
                total += stotal
                metros += smetros
                kilos += skilos
                bultos += sbultos
        self.wids['e_cantidad'].set_text("%s m² + %s kg" % (
            utils.float2str(metros), utils.float2str(kilos)))
        self.wids['e_bultos'].set_text(`bultos`)
        return -1 * total

    def agregar_producto_ldd(self, producto, model, listaldds):
        padre = model.append(None, (producto.codigo,
                                    '-',
                                    producto.descripcion,
                                    '-',
                                    '-',
                                    -sum([l.precio for l in listaldds]), 
                                        # Devolución de pelas: negativo
                                    "%d bultos" % len(listaldds),
                                    0))
        return padre

    def agregar_ldd(self, ldd, model, iterpadre):
        model.append(iterpadre, (ldd.articulo.productoVenta.codigo,
                                 ldd.articulo.codigo_interno,
                                 ldd.articulo.productoVenta.descripcion,
                                 ldd.albaranSalida 
                                    and ldd.albaranSalida.numalbaran or '-',
                                 ldd.albaranDeEntradaDeAbono 
                                    and ldd.albaranDeEntradaDeAbono.numalbaran 
                                    or '-',
                                 -ldd.precio,   # Devolución de pelas: 
                                                # negativo (solo en pantalla).
                                 ldd.observaciones,
                                 ldd.id))
        producto = ldd.articulo.productoVenta
        if producto.es_rollo():
            metros = (producto.camposEspecificosRollo.ancho 
                      * producto.camposEspecificosRollo.metrosLineales)
            kilos = 0
        elif producto.es_bala():
            metros = 0
            kilos = ldd.articulo.bala.pesobala
        elif producto.es_bigbag():
            metros = 0
            kilos = ldd.articulo.bigbag.pesobigbag
        elif producto.es_rolloC() or producto.es_bala_cable():
            metros = 0
            kilos = ldd.articulo.peso
        elif producto.es_caja():
            metros = 0
            kilos = ldd.articulo.peso
        else:
            if ldd.articulo.es_rollo_defectuoso():
                metros = ldd.articulo.superficie
                kilos = 0
            else:
                print "WARNING: ¡El artículo ID %d (LDD ID %d) no es bala, ni"\
                      " rollo [defectuoso] ni bigbag!" % (ldd.articulo.id, 
                                                          ldd.id)
            metros = 0
            kilos = 0
        bultos = 1      # Son artículos de la BD individuales, así que siempre 
                        # constituyen un único bulto.
        return ldd.precio, metros, kilos, bultos
                            # El precio de la LDD se toma de la LDV de la 
                            # factura a la hora de agregarla. El artículo se 
                            # selecciona a continuación de entre los artículos 
                            # del producto_venta de la LDV que estén
                            # contenidos en el albarán al que pertenece 
                            # también la LDV.

    def cambiar_cantidad(self, cell, path, nuevo_texto):
        model = self.wids['tv_precios'].get_model()
        idlda = model[path][-1]
        lda = pclases.LineaDeAbono.get(idlda)
        try:
            nuevacant = float(nuevo_texto)
            lda.cantidad = nuevacant
        except ValueError:
            utils.dialogo_info(titulo = 'NÚMERO INCORRECTO', 
                texto = 'El texto %s no es correcto. Introduzca un número.' %(
                     nuevo_texto), 
                padre = self.wids['ventana'])
        self.actualizar_ventana()

    def cambiar_nuevo_precio(self, cell, path, nuevo_texto):
        model = self.wids['tv_precios'].get_model()
        idlda = model[path][-1]
        lda = pclases.LineaDeAbono.get(idlda)
        try:
            nuevoprecio = float(nuevo_texto)
            if lda.lineaDeVenta != None:
                lda.diferencia = nuevoprecio - lda.lineaDeVenta.precio
            elif lda.servicio != None:
                lda.diferencia = nuevoprecio - lda.servicio.precio
        except ValueError:
            utils.dialogo_info(titulo = 'NÚMERO INCORRECTO', 
                texto = 'El texto %s no es correcto. Introduzca un número.' % (
                    nuevo_texto), 
                padre = self.wids['ventana'])
        self.actualizar_ventana()

    def cambiar_diferencia(self, cell, path, nuevo_texto):
        model = self.wids['tv_precios'].get_model()
        idlda = model[path][-1]
        lda = pclases.LineaDeAbono.get(idlda)
        try:
            nuevadiferencia = float(nuevo_texto)
            lda.diferencia = nuevadiferencia        
        except ValueError:
            utils.dialogo_info(titulo = 'NÚMERO INCORRECTO', 
                texto = 'El texto %s no es correcto. Introduzca un número.' %(
                    nuevo_texto), 
                padre = self.wids['ventana'])
        self.actualizar_ventana()

    def cambiar_importe_devolucion(self, cell, path, nuevo_texto):
        model = self.wids['tv_devoluciones'].get_model()
        if model[path].parent == None:
            return
        idldd = model[path][-1]
        ldd = pclases.LineaDeDevolucion.get(idldd)
        try:
            nuevoprecio = float(nuevo_texto)
            ldd.precio = nuevoprecio
        except ValueError:
            utils.dialogo_info(titulo = 'NÚMERO INCORRECTO', 
                texto = 'El texto %s no es correcto. Introduzca un número.' %(
                    nuevo_texto), 
                padre = self.wids['ventana'])
        self.actualizar_ventana()

    def cambiar_observaciones_devolucion(self, cell, path, nuevo_texto):
        model = self.wids['tv_devoluciones'].get_model()
        if model[path].parent == None:
            return
        idldd = model[path][-1]
        ldd = pclases.LineaDeDevolucion.get(idldd)
        ldd.observaciones = nuevo_texto
        self.actualizar_ventana()

#XXX

    # --------------- Manejadores de eventos ----------------------------
    def generar_albaran(self, w):
        """
        Desvincula los artículos* de sus albaranes de salida originales.
        A su vez, relaciona esos albaranes con la LDD y crea un nuevo
        albarán de entrada de abono que contiene todos esos artículos.
        * Los que no estén ya relacionados con albaranes de abono, se entiende.
        """
        numalbaran = utils.dialogo_entrada(
            'Introduzca un número para el albarán de abono de entrada.\nPued'
            'e dejarlo en blanco si lo desea.',
            'NÚMERO DE ALBARÁN DE ENTRADA POR ABONO', 
            padre = self.wids['ventana'], 
            valor_por_defecto = self.objeto.numabono)
        if numalbaran == None:
            return
        # El usuario ha acabado ignorando siempre las observaciones del 
        # albarán de entrada. Le da a Aceptar sin meter nunca nada.
        # En pro de la usabilidad, y como mártir de ella que me considero ya 
        # a estas alturas... paso de pedir observaciones ya.
        observaciones = "Generado el %s." % (
            utils.str_fecha(mx.DateTime.localtime()))
        adeda = pclases.AlbaranDeEntradaDeAbono(numalbaran = numalbaran, 
                                                observaciones = observaciones, 
                                                fecha = mx.DateTime.localtime()
                                               )
        pclases.Auditoria.nuevo(adeda, self.usuario, __file__)
        for ldd in [l for l in self.objeto.lineasDeDevolucion 
                    if l.albaranDeEntradaDeAbono == None]:
            ldd.albaranSalida = ldd.articulo.albaranSalida
            ldd.articulo.albaranSalida = None
            ldd.albaranDeEntradaDeAbono = adeda
            # Y el paso final, devolverlo al almacén del abono:
            # OJO: Hasta que no se genera el albarán de entrada, el artículo 
            # no pasa al almacén.
            ldd.articulo.almacen = self.objeto.almacen
        self.actualizar_ventana()
        
    def add_devolucion(self, w):
        """
        Solicita una factura. Dentro de esa factura se selecciona una 
        línea de venta. A continuación muestra los artículos relacionados
        con el albarán de salida que contiene la LDV y cuyo producto de
        venta sea el de esa LDV. De entre esos artículos se seleccionan
        todos los que se vayan a descontar, se crean las LDD.
        """
        cliente = self.objeto.cliente
        facturas = pclases.FacturaVenta.select(
            pclases.FacturaVenta.q.clienteID == cliente.id)
        prefacturas = pclases.Prefactura.select(
            pclases.Prefactura.q.clienteID == cliente.id)
        if facturas.count() + prefacturas.count() == 0:
            utils.dialogo_info(titulo = 'NO HAY FACTURAS', 
                texto = 'No se han facturado ventas al cliente del abono.', 
                padre = self.wids['ventana'])
        else:
            fra = utils.buscar_factura(self.wids['ventana'], cliente = cliente)
            if fra != None:
                idldv = self.seleccionar_ldv_de_factura(fra)
                if idldv != None:
                    ldv = pclases.LineaDeVenta.get(idldv)
                    articulos = self.seleccionar_articulos(ldv)
                    for articulo in articulos:
                        self.crear_ldd(self.objeto, articulo, ldv)
                    self.actualizar_ventana()
    
    def crear_ldd(self, abono, articulo, ldv):
        """
        Crea una LDD.
        """
        # elimina del albarán de salida el artículo y asocia la
        # LDD con ese albarán de salida. --> Aún no, eso se hace al generar el 
        # albarán de entrada de abono.
        articulo = pclases.Articulo.get(articulo)
        if articulo.es_rollo():
            precio = (ldv.precio 
              * articulo.productoVenta.camposEspecificosRollo.metros_cuadrados)
        elif articulo.es_bala():
            precio = ldv.precio * articulo.bala.pesobala
        elif (articulo.es_bigbag() or articulo.es_bala_cable() 
              or articulo.es_rolloC()):
            precio = ldv.precio * articulo.peso
        elif articulo.es_rollo_defectuoso():
            precio = ldv.precio * articulo.superficie
        elif articulo.es_caja():
            precio = ldv.precio * articulo.peso
        ldd = pclases.LineaDeDevolucion(articulo = articulo, 
                                        abono = abono, 
                                        albaranDeEntradaDeAbono = None, 
                                        albaranSalida = None,
                                        precio = precio)
        pclases.Auditoria.nuevo(ldd, self.usuario, __file__)

    def seleccionar_articulos(self, ldv):
        """
        Muestra los artículos relacionados con el producto de venta
        y el abono relacionados a su vez con la LDV.
        Devuelve una lista de LDVs seleccionadas.
        """
        albaran = ldv.albaranSalida
        if albaran == None:
            utils.dialogo_info(titulo = "NO SE PUEDE ABONAR",
                               texto = """
            No puede abonar mercancía que no ha salido del almacén.            
            Asegúrese de que existe un albarán de salida relacionado           
            con la venta de la factura que ha elegido.                         
            """, 
                               padre = self.wids['ventana'])
            return []
        articulos_ya_incluidos = [ldd.articulo 
                                  for ldd in self.objeto.lineasDeDevolucion]
        articulos = [a for a in albaran.articulos 
                     if a.productoVenta == ldv.productoVenta and 
                        a not in articulos_ya_incluidos] 
            # De esta forma puedo volver a abonar un artículo que ya se abonó 
            # anteriormente y se volvió a vender en otro (este) albarán.
        filas = [(a.id, a.codigo_interno) for a in articulos]
        idsa = utils.dialogo_resultado(filas,
                                       titulo = 'SELECCIONE UN ARTÍCULO',
                                       cabeceras = ['ID', 'Código interno'],
                                       multi = True, 
                                       padre = self.wids['ventana'])
        if idsa[0] == -1:
            return []
        else:
            return idsa

    def drop_devolucion(self, w):
        model,itr=self.wids['tv_devoluciones'].get_selection().get_selected()
        if itr == None:
            utils.dialogo_info(titulo = 'ERROR', 
                               texto = 'No ha seleccionado ninguna línea', 
                               padre = self.wids['ventana'])
            return

        if model[itr].parent == None:
            return
        idldd = model[itr][-1]
        ldd = pclases.LineaDeDevolucion.get(idldd)
        try:
            if ldd.albaranSalida:
                ldd.articulo.albaranSalida = ldd.albaranSalida.id
            ldd.destroy(usuario = self.usuario, ventana = __file__)
            # Y el artículo vuelve al limbo de los almacenes (al cliente, 
            # quicir).
            ldd.articulo.almacen = None
            self.actualizar_ventana()
        except:
            utils.dialogo_info(titulo = 'ERROR',
                texto = 'Ocurrió un error al eliminar la línea de devolución.'
                        '\nEnvíe un informe a los desarrolladores.', 
                padre = self.wids['ventana'])
     
    def cambiar_cliente(self, w):
        abono = self.objeto
        if abono.lineasDeAbono or abono.lineasDeDevolucion:
            txt = """
            No puede cambiar el cliente si el abono ya          
            contiene devoluciones o ajustes de precio.          
            Elimine primero el contenido del abono si           
            quiere cambiar el cliente o cree un nuevo           
            abono.                                              
            """
            utils.dialogo_info(titulo = 'NO PUEDE CAMBIAR EL CLIENTE',
                               texto = txt)
        else:
            clientes = [(c.id, c.nombre) 
                        for c in pclases.Cliente.select(orderBy='nombre')]
            idcliente = utils.dialogo_combo('SELECCIONE CLIENTE',
                'Seleccione un cliente. Si no encuentra el cliente buscado'
                ', verifique\nque existe en la aplicación mediante la vent'
                'ana de clientes.',
                clientes, 
                padre = self.wids['ventana'])
            try:
                cliente = pclases.Cliente.get(idcliente)
            except:
                return  # El cliente no existe o canceló.
            abono.cliente = cliente
            self.actualizar_ventana()
    
    def add_ajuste(self, w):
        """
        El usuario busca entre las facturas del cliente una 
        línea de venta sobre la que realizar la corrección
        de precio.
        Una vez seleccionada se crea una línea de abono
        relacionada con la LDV y el abono actual con los
        datos por defecto.
        Posteriormente el usuario podrá cambiar el precio
        final o la diferencia en el abono.
        """
        cliente = self.objeto.cliente
        libre = utils.dialogo(titulo = "¿AÑADIR CONCEPTO LIBRE?", 
            texto = "Pulse «sí» para añadir un concepto no facturado;\no "
                    "«no» para buscar entre las facturas del cliente.", 
            padre = self.wids['ventana'], 
            cancelar = True)
        if libre:
            concepto = utils.dialogo_entrada(titulo = "CONCEPTO", 
                        texto = "Introduzca el concepto a abonar:", 
                        padre = self.wids['ventana'])
            if concepto != None:
                precio = utils.dialogo_entrada(titulo = "PRECIO", 
                            texto = "Introduzca el importe a abonar:", 
                            padre = self.wids['ventana'])
                if precio != None:
                    try:
                        precio = utils.parse_euro(precio)
                    except ValueError:
                        utils.dialogo_info(titulo = "ERROR", 
                            texto = "El texto %s no es correcto." % (precio), 
                            padre = self.wids['ventana'])
                    else:
                        srv = pclases.Servicio(pedidoVenta = None,
                                               facturaVenta = None,
                                               albaranSalida = None,
                                               concepto = concepto, 
                                               cantidad = 1.0, 
                                               precio = precio, 
                                               descuento = 0.0)
                        pclases.Auditoria.nuevo(srv, self.usuario, __file__)
                        lda = pclases.LineaDeAbono(lineaDeVenta = None, 
                                abono = self.objeto, 
                                servicio = srv, 
                                diferencia = -precio, 
                                cantidad = 1.0, 
                                observaciones = 'Línea sin correspondencia en'
                                                ' facturas.')
                        pclases.Auditoria.nuevo(lda, self.usuario, __file__)
                        self.actualizar_ventana()
        else:
            fras = pclases.FacturaVenta.select(
                    pclases.FacturaVenta.q.clienteID == cliente.id)
            prefras = pclases.Prefactura.select(
                        pclases.Prefactura.q.clienteID == cliente.id)
            facturas = (fras.count() + prefras.count())
            if facturas == 0:
                utils.dialogo_info(titulo = 'NO HAY FACTURAS', 
                  texto = 'No se han facturado ventas al cliente del abono.', 
                  padre = self.wids['ventana'])
            else:
                fra = utils.buscar_factura(self.wids['ventana'], 
                                           cliente = cliente)
                if fra != None:
                    idsldv, idsserv = self.seleccionar_ldvs_de_factura(fra)
                    for idldv in idsldv:
                        ldv = pclases.LineaDeVenta.get(idldv)
                        self.crear_lda(self.objeto, ldv, None)
                    for idserv in idsserv:
                        serv = pclases.Servicio.get(idserv)
                        self.crear_lda(self.objeto, None, serv)
                    self.actualizar_ventana()
    
    def crear_lda(self, abono, ldv = None, serv = None):
        if ldv != None:
            lda = pclases.LineaDeAbono(abono = abono, 
                                       lineaDeVenta = ldv, 
                                       cantidad = ldv.cantidad, 
                                       servicio = None)
            pclases.Auditoria.nuevo(lda, self.usuario, __file__)
        if serv != None:
            lda = pclases.LineaDeAbono(abono = abono, 
                                       lineaDeVenta = None,
                                       cantidad = serv.cantidad,
                                       servicio = serv)
            pclases.Auditoria.nuevo(lda, self.usuario, __file__)

    def seleccionar_ldvs_de_factura(self, factura):
        """
        Devuelve una lista de identificadores de LDV seleccionadas
        de la factura recibida y otra de servicios.
        Si no se elige ninguna o se cancela la operación, devuelve
        las dos lista vacías.
        """
        filas = [("LDV_%d" % (l.id), l.producto.codigo, 
                  l.producto.descripcion, l.cantidad, 
                  l.precio *(1.0-l.descuento)) 
                 for l in factura.lineasDeVenta if len(l.lineasDeAbono) == 0]
        servicios = [("S_%d" % (s.id), "", s.concepto, s.cantidad, 
                      s.precio * (1.0 - s.descuento)) 
                     for s in factura.servicios 
                     if len(s.lineasDeAbono) == 0]
        filas += servicios
        titulo = 'SELECCIONE VENTA FACTURADA'
        ids = utils.dialogo_resultado(filas,
                                      titulo,
                                      cabeceras = ['ID', 'Código', 
                                                   'Descripción', 'Cantidad', 
                                                   'Precio (dto. incluido)'],
                                      multi = True)
        if ids[0] == -1:
            return [], []
        else:
            idldvs=[int(ide.replace("LDV_", "")) for ide in ids if "LDV_" in ide]
            idservs = [int(ide.replace("S_", "")) for ide in ids if "S_" in ide]
            return idldvs, idservs
    
    def seleccionar_ldv_de_factura(self, factura):
        """
        Devuelve un identificador de LDV seleccionada
        de la factura recibida.
        Si no se elige ninguna o se cancela la operación, devuelve
        None.
        Solo se muestran aquellas LDVs con artículos que no hayan 
        sido ya abonados.
        """
        ldvs = []
        for ldv in factura.lineasDeVenta:
            if ldv.albaranSalidaID != None:
                producto = ldv.productoVenta
                # Selecciono artículos con albarán de salida y sin 
                # devoluciones de ese albarán:
                articulos = [a for a in ldv.albaranSalida.articulos 
                             if a.productoVenta == producto 
                             and ldv.albaranSalida not in [ldd.albaranSalida 
                                    for ldd in a.lineasDeDevolucion]
                            ]
                if articulos != []:
                    ldvs.append(ldv)
        filas = [(l.id, l.productoVenta.codigo, l.productoVenta.descripcion, 
                  l.cantidad, l.precio *(1.0-l.descuento)) 
                 for l in ldvs]
        titulo = 'SELECCIONE VENTA FACTURADA'
        idsldv = utils.dialogo_resultado(filas,
                                         titulo,
                                         cabeceras=['ID', 'Código', 
                                                    'Descripción', 
                                                    'Cantidad', 
                                                    'Precio (dto. incluido)'],
                                         multi = False)
        if idsldv == -1:
            return None
        else:
            return idsldv
            
    def drop_ajuste(self, w):
        model, itr = self.wids['tv_precios'].get_selection().get_selected()
        if itr == None:
            utils.dialogo_info(titulo = 'ERROR', 
                               texto = 'No ha seleccionado ninguna línea', 
                               padre = self.wids['ventana'])
            return
        idlda = model[itr][-1]
        lda = pclases.LineaDeAbono.get(idlda)
        try:
            lda.destroy(usuario = self.usuario, ventana = __file__)
            self.actualizar_ventana()
        except:
            utils.dialogo_info(titulo = 'ERROR',
                texto = 'Ocurrió un error al eliminar la línea de ajuste.\nEn'
                        'víe un informe a los desarrolladores.', 
                padre = self.wids['ventana'])
    
    def crear_nuevo_abono(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        abono = self.objeto
            # Datos a pedir: Cliente y número de abono.
        numdefecto = pclases.Abono.get_nuevo_numabono()
        txt = """
                                                                
        Introduzca un número de abono.                          
                                                                
        Si no está seguro, use el número sugerido: %s           
                                                                
        """ % (numdefecto)
        numabono = utils.dialogo_entrada(txt, 'NÚMERO DE ABONO', numdefecto, 
                                         padre = self.wids['ventana'])
        if numabono == None: return
        clientes = [(c.id, c.nombre) for c in 
                    pclases.Cliente.select(orderBy='nombre')]
        idcliente = utils.dialogo_combo('SELECCIONE CLIENTE',
                        'Seleccione un cliente. Si no encuentra el cliente bu'
                        'scado, verifique\nque existe en la aplicación median'
                        'te la ventana de clientes.',
                        clientes, 
                        padre = self.wids['ventana'])
        try:
            cliente = pclases.Cliente.get(idcliente)
        except:
            return  # El cliente no existe o canceló.
        if abono != None:
            abono.notificador.desactivar()
        abono = pclases.Abono(fecha = time.localtime(), 
                            facturaDeAbono = None,
                            numabono = numabono,
                            cliente = cliente, 
                            almacen = pclases.Almacen.get_almacen_principal())
        pclases.Auditoria.nuevo(abono, self.usuario, __file__)
        self.objeto = abono
        self.actualizar_ventana()
        abono.notificador.set_func(self.aviso_actualizacion)

    def buscar_abono(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        abono = self.objeto
        a_buscar = utils.dialogo_entrada(
                    "Introduzca número de abono o nombre del cliente:", 
                    padre = self.wids['ventana']) 
        if a_buscar != None:
            criterio = pclases.Abono.q.numabono.contains(a_buscar)
            resultados = pclases.Abono.select(criterio)
            if resultados.count() == 0:
                # No hay abonos con número que contengan lo que se busca, 
                # intento buscar por cliente.
                clientes = pclases.Cliente.select(
                            pclases.Cliente.q.nombre.contains(a_buscar))
                if clientes.count() > 1:
                    filas = [(c.id, c.nombre) for c in clientes]
                    idcliente = utils.dialogo_resultado(filas, 
                        'SELECCIONE UN CLIENTE CONCRETO', 
                        cabeceras = ['ID', 'Cliente'])
                    if idcliente == None:
                        return
                elif clientes.count() == 1:
                    idcliente = clientes[0].id
                else:
                    # Tampoco se ha encontrado el cliente.
                    utils.dialogo_info('SIN RESULTADOS', 
                        'La búsqueda no produjo resultados.\nPruebe a cambiar'
                        ' el texto buscado o déjelo en blanco para ver una li'
                        'sta completa.\n(Atención: Ver la lista completa pued'
                        'e resultar lento si el número de elementos es muy al'
                        'to)', 
                        padre = self.wids['ventana'])
                    return
                criterio = pclases.Abono.q.clienteID == idcliente
                resultados = pclases.Abono.select(criterio)
            if resultados.count() > 1:
                ## Refinar los resultados
                idabono = self.refinar_resultados_busqueda(resultados)
                if idabono == None:
                    return
                resultados = [pclases.Abono.get(idabono)]
            elif resultados.count() < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info('SIN RESULTADOS', 
                    'La búsqueda no produjo resultados.\nPruebe a cambiar el '
                    'texto buscado o déjelo en blanco para ver una lista comp'
                    'leta.\n(Atención: Ver la lista completa puede resultar l'
                    'ento si el número de elementos es muy alto)', 
                    padre = self.wids['ventana'])
                return
            ## Un único resultado
            # Primero anulo la función de actualización
            if abono != None:
                abono.notificador.set_func(lambda : None)
            # Pongo el objeto como actual
            abono = resultados[0]
            # Y activo la función de notificación:
            abono.notificador.set_func(self.aviso_actualizacion)
            self.objeto = abono
            self.actualizar_ventana()

    def guardar(self, widget):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        abono = self.objeto
        # Desactivo el notificador momentáneamente
        abono.notificador.set_func(lambda: None)
        # Campos del objeto que hay que guardar: Fecha y numabono.
        fecha_anterior = abono.fecha
        numabono_anterior = abono.numabono
        fecha = utils.parse_fecha(self.wids['e_fecha'].get_text())
        numabono = self.wids['e_numabono'].get_text()
        # Actualizo los datos del objeto
        abono.observaciones = self.wids['e_observaciones'].get_text()
        abono.fecha = fecha
        abono.numabono = numabono
        if not abono.numabono_correcto():
            abono.fecha = fecha_anterior
            abono.numabono = numabono_anterior
            utils.dialogo_info(titulo = "ERROR SECUENCIALIDAD", 
                texto = "La fecha y número de abono no cumplen criterios de "
                        "secuencialidad.", 
                padre = self.wids['ventana'])
        # Fuerzo la actualización de la BD y no espero a que SQLObject lo haga 
        # por mí:
        abono.syncUpdate()
        # Vuelvo a activar el notificador
        abono.notificador.set_func(self.aviso_actualizacion)
        self.actualizar_ventana()
        self.wids['b_guardar'].set_sensitive(False)

    def buscar_fecha(self, w):
        fecha = utils.str_fecha(
                  utils.mostrar_calendario(
                    self.objeto.fecha.tuple()[:3][::-1], 
                    padre = self.wids['ventana'])
                  )
        self.wids['e_fecha'].set_text(fecha)

    def borrar_abono(self, boton):
        """
        Elimina el abono de la BD y anula la relación entre
        él y sus LDVs.
        """
        if not utils.dialogo('Se eliminará el abono actual y todo su contenid'
                             'o.\n¿Está seguro?', 'BORRAR ABONO'): return
        abono = self.objeto
        abono.notificador.set_func(lambda : None)
        for ldd in abono.lineasDeDevolucion + abono.lineasDeAbono:
            ldd.abono = None
            ldd.destroy(usuario = self.usuario, ventana = __file__)
        abono.destroy(usuario = self.usuario, ventana = __file__)
        self.ir_a_primero()
        
    def imprimir(self,boton):
        """
        Prepara los datos para llamar al generador de informes
        """
        self.guardar(None)  # Si se ha olvidado guardar, guardo yo.
        abono = self.objeto
        if abono == None:
            return
        # Se debe abonar con el IVA de la fecha de la factura abonada. Si hay 
        # varias, me quedo con la más reciente.
        try:
            fecha_fra = max([f.fecha for f in abono.get_facturas()])
            iva = abono.cliente.get_iva_norm(fecha = fecha_fra)
        except ValueError:
            iva = abono.cliente.get_iva_norm(fecha = abono.fecha)
        cliente = {'numcli': str(abono.cliente.id),
                   'nombre': abono.cliente.nombre,
                   'nombref': abono.cliente.nombref,
                   'cif': abono.cliente.cif,
                   'direccion': abono.cliente.direccion,
                   'cp': abono.cliente.cp,
                   'localidad': abono.cliente.ciudad,
                   'provincia': abono.cliente.provincia,
                   'pais': abono.cliente.pais,
                   'telf': abono.cliente.telefono,
                   'fax': '',
                   'direccionf': abono.cliente.direccionfacturacion,
                   'cpf': abono.cliente.cpfacturacion,
                   'localidadf': abono.cliente.ciudadfacturacion,
                   'provinciaf': abono.cliente.provinciafacturacion,
                   'paisf': abono.cliente.paisfacturacion} 
        lineasAbono = []
        model = self.wids['tv_precios'].get_model()
        for i in range(len(model)):
            linea = {'codigo': model[i][0] != "SERVICIO" and model[i][0] or "",
                     'descripcion': model[i][1],
                     'importe': utils.float2str(model[i][6] ), #/ (1 + iva)),
                     #'precio': utils.float2str(model[i][6] ), #/ (1 + iva)),
                     'precio': model[i][6],
                     'descuento': "0",      # No hay descuento en abonos
                     'cantidad': model[i][4],
                     'total': (utils.float2str(float(model[i][6]) 
                                               * float(model[i][4])))
                    }
            lineasAbono.append(linea)
        lineasDevolucion = []
        model = self.wids['tv_devoluciones'].get_model()
        total_bultos = 0
        for i in range(len(model)):
            if model[i].parent != None:
                continue    # Salto las líneas de los artículos. Las trataré 
                        # recorriendo los hijos de las líneas de los totales.
            cantidad = 0
            bultos = 0
            for devolucion in model[i].iterchildren():
                bultos += 1
                ldd = pclases.LineaDeDevolucion.get(devolucion[-1])
                if ldd.articulo.es_rollo():
                    cantidad_linea = ldd.articulo.superficie
                elif ldd.articulo.es_rollo_defectuoso():
                    cantidad_linea = ldd.articulo.superficie
                elif (ldd.articulo.es_bigbag() 
                      or ldd.articulo.es_bala() 
                      or ldd.articulo.es_rolloC() 
                      or ldd.articulo.es_bala_cable()):
                    cantidad_linea = ldd.articulo.peso
                else:
                    self.logger.error("abonos_venta::imprimir -> El artículo "
                                      "%s de la LDD %s no es bala, rollo [def"
                                      "ectuoso] ni bigbag" % (
                                        ldd.articuloID, ldd.id))
                    cantidad_linea = 0
                cantidad += cantidad_linea
            total_bultos += bultos
            try:
                preciolinea = model[i][5] / cantidad
            except ZeroDivisionError:
                preciolinea = 0.0
            linea = {'codigo': model[i][0], 
                     'descripcion': model[i][2],
                     'precio': utils.float2str(preciolinea), #/ (1 + iva)),
                     # Precio unitario = (importe total _sin_ IVA / cantidad).
                     'descuento': "0",      # No hay descuentos en las 
                                            # devoluciones de mercancía.
                     'importe': utils.float2str(model[i][5] ), # / (1 + iva)), 
                        # Importe total de las devoluciones del mismo artículo
                     'cantidad': utils.float2str(cantidad),
                     'total': utils.float2str(model[i][5] ) #/ (1 + iva))
                    }
            lineasDevolucion.append(linea)
        if total_bultos > 0:    # Si hay devoluciones, pongo los bultos en las 
                                # observaciones:
            observaciones_abono = "%d bultos devueltos en total." % (
                total_bultos)
        else:
            observaciones_abono = ""
        if (self.objeto.observaciones != None 
            and self.objeto.observaciones.strip() != ""):
            observaciones_abono += "\n%s" % (self.objeto.observaciones)
        facdata = {'facnum':abono.numabono,
                   'fecha':utils.str_fecha(abono.fecha), 
                   'observaciones': observaciones_abono
                  }
        try:
            total = utils.parse_euro(self.wids['e_total'].get_text())
        except ValueError:
            total = 0
        totales = {'subtotal': utils.float2str(total), # / (1 + iva)), 
                   'cargo': None,       # Los abonos nunca llevan cargo
                   'descuento': None,   # Tampoco descuentos
                   'totaliva': utils.float2str(total * iva), 
                   'iva': utils.float2str(iva * 100, 0), 
                   'total': utils.float2str(total * (1 + iva)), 
                  }
        from numerals import numerals as convertir_numero_a_texto
        texto = convertir_numero_a_texto(totales['total'], moneda = "euros", 
                                         fraccion = "céntimos").upper()
        vencimiento = {'fecha': utils.str_fecha(  # @UnusedVariable
                            mx.DateTime.DateFrom(abono.fecha) + mx.DateTime.oneDay * 90),
                       'pago': "vencimiento['pago']", 
                       'documento': "vencimiento['documento']" 
                      }
        vencimiento = None  # TODO: De momento se queda así porque me parece 
                            # que el importe se descuenta del siguiente pagaré 
                            # o fra. y por tanto no hay vencimiento en el que 
                            # la empresa llegue a pagar realmente nada. 
                            # REPITO: De momento, ya se sabe, hasta que surja 
                            # un nuevo... ¡CWT!
        if abono.cliente.extranjero:
            arancel = ""    # Si arancel != None, esto se escribirá delante 
                            # del texto legal.
        else:
            arancel = None  # La interfaz de los abonos en geninformes es así: 
                            # None para "no arancel".
        facturas_abonadas = self.wids['e_facturas'].get_text()
        reports.abrir_pdf(geninformes.abono(cliente, 
                                            facdata, 
                                            lineasAbono, 
                                            lineasDevolucion, 
                                            arancel, 
                                            vencimiento, 
                                            texto, 
                                            totales, 
                                            1 + iva, 
                                            facturas_abonadas))
        self.packinglist()

    def packinglist(self, abrir_pdf = True):
        """
        Prepara e imprime (genera un PDF) los datos del Packing List de los
        artículos del albarán. Idealmente se usará solo para fibra, aunque
        también soporta geotextiles, geocompuestos y fibra de cemento.
        """
        pl = []
        abono = self.objeto
        model = self.wids['tv_devoluciones'].get_model()
        for i in range(len(model)):
            producto = model[i][2]
            fecha = utils.str_fecha(abono.fecha)
            try:
                datos_empresa = pclases.DatosDeLaEmpresa.select()[0]
                linea0 = datos_empresa.nombre.upper()
                linea1 = datos_empresa.direccion
                linea2 = "%s %s (%s)" % (datos_empresa.cp, 
                                         datos_empresa.ciudad, 
                                         datos_empresa.provincia)
                if datos_empresa.fax:
                    linea3 = "TEL %s - FAX %s" % (datos_empresa.telefono, 
                                                  datos_empresa.fax)
                else:
                    linea3 = "TEL %s" % (datos_empresa.telefono)
            except Exception, msg:
                utils.dialogo_info(titulo="ERROR BUSCANDO DATOS DE LA EMPRESA", 
                                texto = "Los datos de la cabecera "
                                        "(información de la propia empresa) "
                                        "no se encontraron.\n\nContacte con "
                                        "el administrador para solventar "
                                        "este error.\n\n\nInformación de "
                                        "depuración:\n%s" % msg, 
                                padre = self.wids['ventana'])
                return
            nombre = abono.cliente.nombre
            direccion = abono.cliente.direccion
            ciudad = abono.cliente.ciudad
            cp = abono.cliente.cp
            pais = abono.cliente.pais
            lotes = []
            balas = []
            tipo = ""
            for ldd_row in model[i].iterchildren():
                ldd = pclases.LineaDeDevolucion.get(ldd_row[-1])
                codigoproducto = ldd.productoVenta.codigo
                if ldd.articulo.es_rollo():
                    if ldd.articulo.partida not in lotes:
                        lotes.append(ldd.articulo.partida)
                    if tipo == "":
                        prod = ldd.articulo.productoVenta
                        anchoart = prod.camposEspecificosRollo.ancho
                        mlinart = prod.camposEspecificosRollo.metrosLineales
                        tipo = "%.2fx%d" % (anchoart, 
                                            mlinart)
                    balas.append((ldd.articulo.codigo, 
                                  "%.2f m2" % (ldd.articulo.superficie), 
                                  ldd.articulo.superficie, 
                                  ldd.articulo.rollo.numrollo, 
                                  ldd.articulo.codigo))
                elif ldd.articulo.es_rollo_defectuoso():
                    if ldd.articulo.partida not in lotes:
                        lotes.append(ldd.articulo.partida)
                    if tipo == "":
                        tipo = "%.2fx%.2f" % (ldd.articulo.ancho, 
                                              ldd.articulo.largo)
                    balas.append((ldd.articulo.codigo, 
                                  "%.2f m2" % (ldd.articulo.superficie), 
                                  ldd.articulo.superficie, 
                                  ldd.articulo.rolloDefectuoso.numrollo, 
                                  ldd.articulo.codigo))
                elif ldd.articulo.es_bala():
                    if ldd.articulo.lote not in lotes:
                        lotes.append(ldd.articulo.lote)
                    if tipo == "":
                        prod = ldd.articulo.productoVenta
                        tipo = prod.camposEspecificosBala.color
                    balas.append((ldd.articulo.codigo,
                                  "%.2f kg" % (ldd.articulo.peso), 
                                  ldd.articulo.peso, 
                                  ldd.articulo.bala.numbala, 
                                  ldd.articulo.codigo))
                elif ldd.articulo.es_bigbag():
                    if ldd.articulo.loteCem not in lotes:
                        lotes.append(ldd.articulo.loteCem)
                    if tipo == "":
                        prod = ldd.articulo.productoVenta
                        tipo = prod.camposEspecificosBala.color
                    balas.append((ldd.articulo.codigo,
                                  "%.2f kg" % (ldd.articulo.peso), 
                                  ldd.articulo.peso, 
                                  ldd.articulo.bigbag.numbigbag, 
                                  ldd.articulo.codigo))
                elif ldd.articulo.es_bala_cable():
                    balas.append((ldd.articulo.codigo,
                                  "%s kg" % utils.float2str(ldd.articulo.peso),
                                  ldd.articulo.peso, 
                                  ldd.articulo.balaCable.numbala, 
                                  ldd.articulo.codigo))
                elif ldd.articulo.es_rolloC():
                    balas.append((ldd.articulo.codigo, 
                                  "%s kg" % utils.float2str(ldd.articulo.peso),
                                  ldd.articulo.peso, 
                                  ldd.articulo.rolloC.numrollo, 
                                  ldd.articulo.codigo))
            total = "%d" % (len(balas))
            peso = utils.float2str(sum([b[2] for b in balas]))
                # balas es una tupla de tuplas con 4 elementos: código, peso 
                # como cadena, peso  y número de rollo, bala o bigbag.
            pl.append({'producto': producto,
                       'codigo_producto': codigoproducto, 
                       'fecha': fecha,
                       'lote': ", ".join([l.codigo for l in lotes]),
                       'tipo': tipo, 
                       'balas': balas,
                       'total': total,
                       'peso': peso,
                       'envio': {'nombre': nombre,
                                 'direccion': direccion, 
                                 'ciudad': ciudad,
                                 'cp': cp,
                                 'pais': pais}, 
                       'empresa': {'linea0': linea0,
                                   'linea1': linea1,
                                   'linea2': linea2,
                                   'linea3': linea3}
                       })
        return self.imprimir_packing_list(tuple(pl), abrir_pdf)
    
    def imprimir_packing_list(self, packing_lists, abrir_pdf = True):
        from formularios.reports import abrir_pdf as abrir_archivo_pdf
        self.guardar(None)  # Si se ha olvidado guardar, guardo yo.
        packings_generados = []
        func_packinglist = geninformes._packingListBalas
        for i in xrange(len(packing_lists)):
            nomarchivo = func_packinglist(packing_lists[i], i+1, 
                            titulo = "Packing list de abono %s" % (
                                self.objeto.numabono))
            if abrir_pdf:
                abrir_archivo_pdf(nomarchivo)
            packings_generados.append(nomarchivo)
        return packings_generados
        
    def generar_fra_abono(self, w):
        if self.objeto.facturaDeAbono == None:
            if self.objeto.fecha:
                fa = pclases.FacturaDeAbono(fecha = self.objeto.fecha)
                pclases.Auditoria.nuevo(fa, self.usuario, __file__)
            else: 
                fa = pclases.FacturaDeAbono(fecha = mx.DateTime.localtime())
                pclases.Auditoria.nuevo(fa, self.usuario, __file__)
            self.objeto.facturaDeAbono = fa
            self.objeto.make_swap()
            utils.dialogo_info(titulo = 'FACTURA GENERADA',
                               padre = self.wids['ventana'], 
                               texto = """
            Factura de abono generada.                                         
            Puede descontar el abono de la siguiente factura de venta del 
            cliente o imprimirla junto con el albarán mediante el botón 
            correspondiente. 
            """)
        else:
            if self.objeto.facturaDeAbono.pagosDeAbono != []:
                utils.dialogo_info(titulo = 'ABONO CON FACTURA',
                                   texto = """
                El abono ya ha generado una factura de abono                  
                que cuenta con pagos realizados.
                No es posible relacionar el mismo abono con 
                una nueva factura si este ya tiene importes 
                abonados.
                Cree un nuevo abono o anule los pagos.
                """, 
                                   padre = self.wids['ventana'])
            else:
                if utils.dialogo(titulo = '¿BORRAR FACTURA EXISTENTE?',
                                 texto = "El albarán ya tiene una factura, ¿de"
                                        "sea eliminarla?", 
                                 padre = self.wids['ventana']):
                    fa = self.objeto.facturaDeAbono
                    self.objeto.facturaDeAbono = None
                    self.objeto.make_swap()
                    for c in fa.cobros:
                        c.destroy(usuario = self.usuario, ventana = __file__)
                    fa.destroy(usuario = self.usuario, ventana = __file__)
                    utils.dialogo_info(titulo = 'CREAR NUEVA FACTURA',
                                       texto = "Ahora puede crear una nueva f"
                                               "actura con el abono", 
                                       padre = self.wids['ventana'])
        self.actualizar_ventana()


if __name__ == '__main__':
    v = AbonosVenta(usuario = pclases.Usuario.selectBy(usuario = "enrique")[0])

