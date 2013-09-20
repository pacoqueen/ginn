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
## productos_venta.py - Catálogo de productos de venta.
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 9 de octubre de 2005 -> Inicio 
## 9 de octubre de 2005 -> 90% funcional (faltan fichas de prod.)
## 9 de enero de 2006 -> Separo productos de venta del resto.
## 23 de enero de 2006 -> Portado a clase.
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
from informes.barcode.EANBarCode import EanBarCode
try:
    from psycopg import ProgrammingError as psycopg_ProgrammingError
except ImportError:
    from psycopg2 import ProgrammingError as psycopg_ProgrammingError


class ProductosDeVentaBalas(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self._objetoreciencreado = None
        Ventana.__init__(self, 'productos_de_venta_balas.glade', objeto, 
                         usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_anterior/clicked': self.ir_a_anterior,
                       'b_siguiente/clicked':self.ir_a_siguiente,
                       'b_contar/clicked' : self.muestra_stock,
                       'b_fichas/clicked': self.ver_ficha,
                       'b_articulos/clicked': self.ver_articulos,
                       'b_tarifas/clicked': self.ver_tarifas,
                       'b_nuevo/clicked': self.crear_nuevo_producto,
                       'b_borrar/clicked': self.borrar_producto,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_add_campoesp/clicked': self.add_campoesp,
                       'b_drop_campoesp/clicked': self.drop_campoesp,
                       'b_change_campoesp/clicked': self.change_campoesp,
                       'b_buscar/clicked': self.buscar_producto, 
                       'ch_no_anno_cert/toggled': self.change_anno_cert, 
                       'sp_anno_certificacion/output': utils.show_leading_zeros
                      }
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        self.wids['b_contar'].set_property("visible", False)
        gtk.main()

    # --------------- Funciones auxiliares ------------------------------
    def es_diferente(self):
        """
        Devuelve True si la información en pantalla es distinta a la
        del objeto en memoria.
        """
        producto = self.objeto
        if producto == None: return False   # Si no hay producto activo, 
                    # devuelvo que no hay cambio respecto a la ventana. 
        # Datos a comparar:
        # - código <-> e_codigo
        # - descripción <-> e_descripcion
        # - nombre <-> e_nombre
        # - preciopordefecto <-> e_precio
        # - minimo <-> e_minimo
        condicion = producto.codigo == self.wids['e_codigo'].get_text()
        # print condicion
        condicion = condicion and (producto.descripcion == self.wids['e_descripcion'].get_text())
        condicion = condicion and (producto.nombre == self.wids['e_nombre'].get_text())
        condicion = condicion and (str(producto.preciopordefecto) == self.wids['e_precio'].get_text())
        condicion = condicion and (str(producto.minimo) == self.wids['e_minimo'].get_text())
        condicion = condicion and (str(producto.arancel) == self.wids['e_arancel'].get_text())
        condicion = condicion and (utils.float2str(producto.prodestandar) == self.wids['e_prodestandar'].get_text())
        condicion = condicion and (str(producto.camposEspecificosBala.dtex) == self.wids['e_dtex'].get_text())
        condicion = condicion and (str(producto.camposEspecificosBala.corte) == self.wids['e_corte'].get_text())
        condicion = condicion and (str(producto.camposEspecificosBala.color) == self.wids['e_color'].get_text())
        condicion = condicion and (producto.camposEspecificosBala.antiuv == self.wids['chk_antiuv'].get_active())
        condicion = condicion and (producto.camposEspecificosBala.reciclada == self.wids['ch_reciclada'].get_active())
        condicion = condicion and (producto.camposEspecificosBala.tipoMaterialBalaID == utils.combo_get_value(self.wids['cb_material']))
        if producto.camposEspecificosBala.gramosBolsa != None:
            gramosBolsa_compara = str(
                producto.camposEspecificosBala.gramosBolsa)
        else:
            gramosBolsa_compara = "N/A"
        condicion = condicion and (
            gramosBolsa_compara == self.wids['e_gramosBolsa'].get_text())
        if producto.camposEspecificosBala.bolsasCaja != None:
            bolsasCaja_compara = str(
                producto.camposEspecificosBala.bolsasCaja)
        else:
            bolsasCaja_compara = "N/A"
        condicion = condicion and (
            bolsasCaja_compara == self.wids['e_bolsasCaja'].get_text())
        if producto.camposEspecificosBala.cajasPale != None:
            cajasPale_compara = str(
                producto.camposEspecificosBala.cajasPale)
        else:
            cajasPale_compara = "N/A"
        condicion = condicion and (
            cajasPale_compara == self.wids['e_cajasPale'].get_text())
        condicion = (condicion and 
            producto.dni == self.wids['e_dni'].get_text())
        condicion = (condicion and 
            producto.uso == self.wids['e_uso'].get_text())
        if self.wids['ch_no_anno_cert'].get_active():
            condicion = (condicion and producto.annoCertificacion == None)
        else:
            condicion = (condicion and
                producto.annoCertificacion 
                    == self.wids['sp_anno_certificacion'].get_value_as_int())
        cliente = utils.combo_get_value(self.wids['cbe_cliente'])
        if cliente == 0:
            cliente = None
        try:
            cliente_objeto = self.objeto.camposEspecificosBala.cliente.id
        except AttributeError:
            cliente_objeto = None
        condicion = (condicion and cliente_objeto == cliente)
        return not condicion    # Concición verifica que sea igual

    def aviso_actualizacion(self):
        """
        Muestra una ventana modal con el mensaje de objeto 
        actualizado.
        """
        utils.dialogo_info('ACTUALIZAR',
                           'El producto ha sido modificado remotamente.\nDebe actualizar la información mostrada en pantalla.\nPulse el botón «Actualizar»', 
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
        utils.rellenar_lista(self.wids['cb_material'],[(t.id, t.descripcion) for t in pclases.TipoMaterialBala.select()])
        cols = (('Tarifa', 'gobject.TYPE_STRING', False, True, True, None),
                ('Precio', 'gobject.TYPE_FLOAT', False, True, False, None),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_tarifas'], cols)
        try:
            dde_nombre = pclases.DatosDeLaEmpresa.select()[0].nombre
        except IndexError:
            dde_nombre = ""
        clientes = ((0, dde_nombre), )
        for cliente in pclases.Cliente.select(
                pclases.Cliente.q.inhabilitado == False, 
                orderBy = "nombre"):
            clientes += ((cliente.id, "%s (%s)" % (cliente.nombre, 
                                                   cliente.cif)), )
        utils.rellenar_lista(self.wids['cbe_cliente'], clientes)

    def activar_widgets(self, s, chequear_permisos = True):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        ws = ('e_idproducto', 'e_codigo', 'e_descripcion', 'e_nombre', 
              'e_precio', 'e_minimo', 'e_stock', 'b_contar', 'e_dtex', 
              'e_corte', 'e_color','chk_antiuv','b_borrar', 'b_fichas', 
              'b_articulos','b_tarifas','e_arancel', 'e_prodestandar', 
              'cb_material', 'expander2', 'ch_reciclada', 'cbe_cliente') 
        for w in ws:
            self.wids[w].set_sensitive(s)
        if chequear_permisos:
            self.check_permisos(nombre_fichero_ventana = "productos_de_venta_balas.py")
        if self.objeto and len(self.objeto.articulos) > 0:
            self.wids['ch_reciclada'].set_sensitive(False)  
            # Una vez se ha fabricado algo no puedo dejar que cambie la fibra a reciclada y viceversa, puesto que entonces me
            # alteraría el cálculo de stock, la forma de dar de alta más balas, etiquetas etc...
        if self.objeto and not self.objeto.es_bolsa():
            self.wids['cbe_cliente'].set_sensitive(False)
    

    def ir_a_primero(self):
        """
        Hace que el primer registro -si lo hay- de la tabla implicada
        en el objeto del formulario sea el objeto activo.
        """
        producto = self.objeto
        try:
            # Anulo el aviso de actualización del envío que deja de ser activo.
            if producto != None: producto.notificador.desactivar()
            producto = pclases.ProductoVenta.select(pclases.ProductoVenta.q.camposEspecificosBalaID != None)[0]  # Selecciono todos y me quedo con el primero de la lista
            producto.notificador.activar(self.aviso_actualizacion)      # Activo la notificación
        except:
            producto = None     
        self.objeto = producto
        self.actualizar_ventana()

    def ir_a_anterior(self,widget):
        """
        Hace que el registro anterior (ordenados por ID interno)
        sea el objeto activo
        """
        if self.wids['b_guardar'] != None and self.wids['b_guardar'].get_property('sensitive'):
            # Hay cambios pendientes de guardar.
            if utils.dialogo('Hay cambios pendientes de guardar.\n¿Desea hacerlo ahora?', '¿GUARDAR CAMBIOS?'):
                try:
                    self.guardar(None)
                except:
                    utils.dialogo_info(titulo = 'NO SE PUDO GUARDAR', 
                        texto = 'Los cambios no se pudieron guardar '
                            'automáticamente.\nDebe hacerlo de forma manual', 
                        padre = self.wids['ventana'])
                    return 
        producto = self.objeto
        linea = pclases.LineaDeProduccion.select(
            pclases.LineaDeProduccion.q.nombre.contains('fibra'))[0]
        lineaembol = pclases.LineaDeProduccion.select(
            pclases.LineaDeProduccion.q.nombre.contains('bolsa'))[0]
        try:
            anterior = pclases.ProductoVenta.select(pclases.AND(
                pclases.ProductoVenta.q.camposEspecificosBalaID != None, 
                pclases.OR(
                  pclases.ProductoVenta.q.lineaDeProduccionID == linea.id, 
                  pclases.ProductoVenta.q.lineaDeProduccionID == lineaembol.id
                ),
                pclases.ProductoVenta.q.id < producto.id),orderBy='-id')[0]
        except IndexError:
            utils.dialogo_info(texto = "El elemento seleccionado es el primero registrado en el sistema", 
                               titulo="ERROR", 
                               padre = self.wids['ventana'])
            return
        self.objeto = anterior
        self.actualizar_ventana()
        
    def ir_a_siguiente(self,widget):
        """
        Hace que el siguiente registro (ordenados por ID interno)
        sea el objeto activo
        """
        if self.wids['b_guardar'] != None and self.wids['b_guardar'].get_property('sensitive'):
            # Hay cambios pendientes de guardar.
            if utils.dialogo('Hay cambios pendientes de guardar.\n¿Desea hacerlo ahora?', '¿GUARDAR CAMBIOS?'):
                try:
                    self.guardar(None)
                except:
                    utils.dialogo_info(titulo = 'NO SE PUDO GUARDAR', 
                                       texto = 'Los cambios no se pudieron guardar automáticamente.\nDebe hacerlo de forma manual', 
                                       padre = self.wids['ventana'])
                    return 
        producto = self.objeto
        linea = pclases.LineaDeProduccion.select(pclases.LineaDeProduccion.q.nombre.contains('fibra'))[0]
        lineaembol = pclases.LineaDeProduccion.select(
            pclases.LineaDeProduccion.q.nombre.contains('bolsa'))[0]
        try:
            siguiente = pclases.ProductoVenta.select(pclases.AND(
                pclases.ProductoVenta.q.camposEspecificosBalaID != None, 
                pclases.OR(
                  pclases.ProductoVenta.q.lineaDeProduccionID == linea.id, 
                  pclases.ProductoVenta.q.lineaDeProduccionID == lineaembol.id
                ),
                pclases.ProductoVenta.q.id > producto.id),orderBy='id')[0]
        except IndexError:
            utils.dialogo_info(texto = "El elemento seleccionado es el último"
                                       " registrado en el sistema", 
                               titulo = "ERROR", 
                               padre = self.wids['ventana'])
            return
        self.objeto = siguiente
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
            filas_res.append((r.id, r.codigo, r.nombre, r.descripcion))
        idproducto = utils.dialogo_resultado(filas_res,
                        titulo = 'Seleccione producto',
                        cabeceras = ('ID Interno', 
                                     'Código', 
                                     'Nombre', 
                                     'Descripción'), 
                        padre = self.wids['ventana'], 
                        abrir_en_ventana_nueva = 
                            (ProductosDeVentaBalas, 
                             pclases.ProductoVenta, 
                             self.usuario))
        if idproducto < 0:
            return None
        else:
            return idproducto

    def rellenar_widgets(self):
        """
        Introduce la información del producto actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        self.wids['b_guardar'].set_sensitive(False)
        producto = self.objeto
        linea = pclases.LineaDeProduccion.select(
            pclases.LineaDeProduccion.q.nombre.contains('fibra'))[0]
        lineaembol = pclases.LineaDeProduccion.select(
            pclases.LineaDeProduccion.q.nombre.contains('bolsa'))[0]
        productos = pclases.ProductoVenta.select(pclases.AND(
            pclases.ProductoVenta.q.camposEspecificosBalaID != None, 
            pclases.OR(
                pclases.ProductoVenta.q.lineaDeProduccionID == linea.id, 
                pclases.ProductoVenta.q.lineaDeProduccionID == lineaembol.id
            )), orderBy = 'id')
        productos_count = productos.count()
        yo_index = pclases.SQLlist(productos).index(producto) + 1
        self.wids['ventana'].set_title(
            "Productos de venta: FIBRA - %s (%d de %d)" % (
                producto.descripcion, 
                yo_index, 
                productos_count))
        if len(producto.articulos) > 0:
            self.wids['ch_reciclada'].set_sensitive(False)  
            # Una vez se ha fabricado algo no puedo dejar que cambie la fibra a reciclada y viceversa, puesto que entonces me
            # alteraría el cálculo de stock, la forma de dar de alta más balas, etiquetas etc...
        self.wids['i_barcode'].set_from_file(EanBarCode().getImage(producto.codigo))
        self.wids['e_codigo'].set_text(producto.codigo)
        self.wids['e_descripcion'].set_text(producto.descripcion)
        self.wids['e_nombre'].set_text(producto.nombre)
        self.wids['e_precio'].set_text(str(producto.preciopordefecto))
        self.wids['e_minimo'].set_text(str(producto.minimo))
        self.wids['e_arancel'].set_text(str(producto.arancel))
        self.wids['e_prodestandar'].set_text(utils.float2str(producto.prodestandar))
        campos = producto.camposEspecificosBala
        self.wids['ch_reciclada'].set_active(campos.reciclada)
        self.wids['e_dtex'].set_text(str(campos.dtex))
        self.wids['e_corte'].set_text(str(campos.corte))
        self.wids['e_color'].set_text(str(campos.color))
        self.wids['chk_antiuv'].set_active(campos.antiuv)
        utils.combo_set_from_db(self.wids['cb_material'], 
                                campos.tipoMaterialBalaID)
        # Campos para bolsas de fibra de cemento:
        if campos.gramosBolsa != None:
            self.wids['e_gramosBolsa'].set_text(str(campos.gramosBolsa))
        else:
            self.wids['e_gramosBolsa'].set_text("N/A")
        if campos.bolsasCaja != None:
            self.wids['e_bolsasCaja'].set_text(str(campos.bolsasCaja))
        else:
            self.wids['e_bolsasCaja'].set_text("N/A")
        if campos.cajasPale != None:
            self.wids['e_cajasPale'].set_text(str(campos.cajasPale))
        else:
            self.wids['e_cajasPale'].set_text("N/A")
        # Datos no modificables:
        self.wids['e_idproducto'].set_text(`producto.id`)
        self.muestra_stock()
        # self.wids['e_stock'].set_text('Pulsar botón "Contar stock"')
        self.mostrar_especificos()
        self.rellenar_tabla_tarifas()
        self.wids['e_cajasPale'].set_sensitive(not self.objeto.articulos)
        try:
            cliente = campos.cliente.id
        except AttributeError:
            cliente = 0
        utils.combo_set_from_db(self.wids['cbe_cliente'], cliente)
        # Nuevos campos de etiquetas norma13:
        if self.objeto.annoCertificacion is None:
            self.wids['sp_anno_certificacion'].set_text("")
            self.wids['ch_no_anno_cert'].set_active(True)
        else:
            self.wids['sp_anno_certificacion'].set_value(
                    self.objeto.annoCertificacion)
            utils.show_leading_zeros(self.wids['sp_anno_certificacion'])
            self.wids['ch_no_anno_cert'].set_active(False)
        self.wids['e_dni'].set_text(producto.dni)
        self.wids['e_uso'].set_text(producto.uso)
        ### Botones anterior/siguiente
        producto = self.objeto
        try:
            linea = pclases.LineaDeProduccion.select(
                pclases.LineaDeProduccion.q.nombre.contains('fibra'))[0]
            lineaembol = pclases.LineaDeProduccion.select(
                pclases.LineaDeProduccion.q.nombre.contains('bolsa'))[0]
            anteriores = pclases.ProductoVenta.select(pclases.AND(
                pclases.ProductoVenta.q.camposEspecificosBalaID != None, 
                pclases.OR(
                  pclases.ProductoVenta.q.lineaDeProduccionID == linea.id, 
                  pclases.ProductoVenta.q.lineaDeProduccionID == lineaembol.id
                ),
                pclases.ProductoVenta.q.id < producto.id)).count()
            siguientes = pclases.ProductoVenta.select(pclases.AND(
                pclases.ProductoVenta.q.camposEspecificosBalaID != None, 
                pclases.OR(
                  pclases.ProductoVenta.q.lineaDeProduccionID == linea.id, 
                  pclases.ProductoVenta.q.lineaDeProduccionID == lineaembol.id
                ),
                pclases.ProductoVenta.q.id > producto.id)).count()
        except:
            pass
        else:
            self.wids['b_anterior'].set_sensitive(anteriores)
            self.wids['b_siguiente'].set_sensitive(siguientes)
        self.wids['b_guardar'].set_sensitive(False)
        self.objeto.make_swap()

    def change_anno_cert(self, ch_no_anno):
        self.wids['sp_anno_certificacion'].set_sensitive(
                not ch_no_anno.get_active())

    def rellenar_tabla_tarifas(self):
        model = self.wids['tv_tarifas'].get_model()
        model.clear()
        for t in pclases.Tarifa.select():
            model.append((t.nombre, t.obtener_precio(self.objeto), t.id))
 
    def mostrar_especificos(self):
        """
        Muestra los datos específicos del producto.
        Elimina los hijos que componen la tabla 
        antes de insertar los nuevos.
        """
        hijos = self.wids['tabla'].get_children()
        for hijo in hijos:
            hijo.destroy()
        producto = self.objeto
        filas = len(producto.camposEspecificos)
        if filas == 0: 
            filas = 1   # Para evitar el "assert". De todas formas aunque sea de 1x2, si no hay datos específicos no se va a mostrar nada.
        self.wids['tabla'].resize(filas, 2)
        y = 0   # Fila donde insertar el campo.
        for campo in producto.camposEspecificos:
            label = gtk.Label("%s: " % campo.nombre)
            entry = gtk.Entry()
            entry.set_text(campo.valor)
            entry.set_has_frame(False)
            entry.set_editable(False)
            self.wids['tabla'].attach(label, 0, 1, y, y+1)
            self.wids['tabla'].attach(entry, 1, 2, y, y+1)
            label.show()
            entry.show()
            y += 1

    # --------------- Manejadores de eventos ----------------------------
    def muestra_stock(self, boton = None):
        """
        Escribe el stock del producto en el widget.
        """
        producto = self.objeto
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        vpro.set_valor(0.9, 'Contando existencias en almacén...')
        while gtk.events_pending(): gtk.main_iteration(False)
        self.wids['e_stock'].set_text("%s Kg" 
            % utils.float2str(round(producto.get_stock(),2)))
        vpro.ocultar()

    def calcular_digitoc(self, cod):
        pesos = [1, 3]*6
        magic = 10
        suma = 0
        for i in range(12):
            suma = suma + int(cod[i]) * pesos[i]
        z = (magic - (suma % magic)) % magic
        if z < 0 or z >= magic:
            return None
        return str(z)

    def buscar_cod_libre(self):
        """
        Devuelve un código de tres cifras como 
        cadena que no esté ya en la tabla de 
        productos como producto terminado.
        Siempre devolverá el primer código
        libre más cercano a 000.
        Si no quedan más mostrará un mensaje
        de error por pantalla y devolverá
        999.
        """
        prods = pclases.ProductoVenta.select(pclases.AND(
            pclases.OR(
                pclases.ProductoVenta.q.camposEspecificosBalaID !=None, 
                pclases.ProductoVenta.q.camposEspecificosRolloID !=None, 
                pclases.ProductoVenta.q.camposEspecificosEspecialID !=None), 
            pclases.ProductoVenta.q.codigo.startswith('843603219')))
        # Incluyo todo tipo de productos porque aunque la fibra esté limitada 
        # al rango 300~400, el resto no, y al crearlos ha podido pillar uno 
        # de esos números.
        codsproducto = [int(p.codigo[-4:-1]) for p in prods]
        codsproducto.sort()
        #for i in xrange(300, 400):  # OJO: Códigos hardcoded. Para balas se 
                                    # han asignado los códigos 300 a 399.
        for i in xrange(1000):  # Ya no hay división entre fibra y geotextiles 
            # a la hora de asignar códigos EAN. Se han agotado los de fibra y 
            # "liberamos" el resto de los 500 (o así) que nos quedan.
            try:
                if not i in codsproducto:
                    return "%03d" % i
            except IndexError:  # No hay o me pasé de rango
                return "%03d" % i
        utils.dialogo_info('NO QUEDAN CÓDIGOS DISPONIBLES', 
                           'Todos los códigos EAN13 fueron asignados.', 
                           padre = self.wids['ventana'])
        return '999'

    def generar_codigo_ean(self):
        """
        Genera un código EAN-13 completo, dígito control
        incluido, dentro del rango asignado a Geotexan.
        """
        codpais = '84'
        codempresa = '3603219'
        codproducto = self.buscar_cod_libre()
        codtemp = codpais + codempresa + codproducto 
        digitoc = self.calcular_digitoc(codtemp)
        return codtemp + digitoc
        
    def crear_nuevo_producto(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        producto = self.objeto
        if producto != None:
            producto.notificador.desactivar()
        try:
            tipoDefecto = pclases.TipoMaterialBala.select(
              pclases.TipoMaterialBala.q.descripcion.contains('POLIPROPILENO')
              )[0]
        except IndexError:
            tipoDefecto = None
        campos = pclases.CamposEspecificosBala(dtex = 0,
                                            corte = 0,
                                            color = '',
                                            antiuv = False,
                                            tipoMaterialBala = tipoDefecto, 
                                            reciclada = False, 
                                            gramosBolsa = None,
                                            bolsasCaja = None,
                                            cajasPale = None)
        pclases.Auditoria.nuevo(campos, self.usuario, __file__)
        linea = pclases.LineaDeProduccion.select(
            pclases.LineaDeProduccion.q.nombre.contains('fibra'))[0]
            # Por defecto se va a crear como producto de la línea de fibras. 
            # Al guardar se cambiará a la línea de embolsado si fuera el caso.
        producto = pclases.ProductoVenta(lineaDeProduccion = linea,
                                    camposEspecificosRollo = None,
                                    camposEspecificosBala = campos, 
                                    codigo = self.generar_codigo_ean(), 
                                    nombre = '',
                                    descripcion = '', 
                                    preciopordefecto = 0, 
                                    minimo = 0,
                                    arancel = '')
        pclases.Auditoria.nuevo(producto, self.usuario, __file__)
        self._objetoreciencreado = producto
        utils.dialogo_info('PRODUCTO CREADO', 
                           'Se ha creado un producto nuevo.\nA continuación '
                           'complete la información del producto y guarde '
                           'los cambios.\n\nNO OLVIDE INTRODUCIR LA '
                           'FORMULACIÓN PARA EL CONSUMO AUTOMÁTICO DE '
                           'MATERIALES EN LA VENTANA CORRESPONDIENTE.', 
                           padre = self.wids['ventana'])
        producto.notificador.activar(self.aviso_actualizacion)
        self.objeto = producto
        self.activar_widgets(True)
        self.actualizar_ventana()

    def buscar_producto(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        producto = self.objeto
        a_buscar = utils.dialogo_entrada(
                "Introduzca código, nombre o descripción de producto:", 
                padre = self.wids['ventana']) 
        if a_buscar != None:
            a_buscar = a_buscar.strip()
            try:
                ida_buscar = int(a_buscar)
            except ValueError:
                ida_buscar = -1
            criterio = pclases.OR(
                    pclases.ProductoVenta.q.codigo.contains(a_buscar),
                    pclases.ProductoVenta.q.nombre.contains(a_buscar),
                    pclases.ProductoVenta.q.descripcion.contains(a_buscar),
                    pclases.ProductoVenta.q.id == ida_buscar)
            criterio = pclases.AND(criterio, 
                    pclases.ProductoVenta.q.camposEspecificosBalaID != None)
            resultados = pclases.ProductoVenta.select(criterio)
            if resultados.count() > 1:
                    ## Refinar los resultados
                    idproducto = self.refinar_resultados_busqueda(resultados)
                    if idproducto == None:
                        return
                    resultados = [pclases.ProductoVenta.get(idproducto)]
                    # Se supone que la comprensión de listas es más rápida que hacer un nuevo get a SQLObject.
                    # Me quedo con una lista de resultados de un único objeto ocupando la primera posición.
                    # (Más abajo será cuando se cambie realmente el objeto actual por este resultado.)
            elif resultados.count() < 1:
                    ## Sin resultados de búsqueda
                    utils.dialogo_info('SIN RESULTADOS', 'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.\n(Atención: Ver la lista completa puede resultar lento si el número de elementos es muy alto)', 
                                       padre = self.wids['ventana'])
                    return
            ## Un único resultado
            # Primero anulo la función de actualización
            if producto != None:
                producto.notificador.desactivar()
            # Pongo el objeto como actual
            producto = resultados[0]
            # Y activo la función de notificación:
            producto.notificador.activar(self.aviso_actualizacion)
            self.activar_widgets(True)
        self.objeto = producto
        self.actualizar_ventana()

    def guardar(self, widget):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        producto = self.objeto
        codigo = self.wids['e_codigo'].get_text()
        if len(codigo) < 12:
            utils.dialogo_info(titulo = "CÓDIGO DEMASIADO CORTO", 
                               texto = "El código debe tener 13 dígitos para ajustarse al formato EAN-13.\nSe va a completar con ceros.", 
                               padre = self.wids['ventana'])
            codigo += "0" * (12 - len(codigo))  # Completo hasta 12 para que después se le haga la suma de control.
        if len(codigo) == 12:
            codigo = codigo + self.calcular_digitoc(codigo)
        if len(codigo) > 13:
            utils.dialogo_info(titulo = "CÓDIGO INCORRECTO", 
                               texto = "Código EAN-13 incorrecto. Debe tener exactamente 13 dígitos.\nPuede introducir 12 y dejar que se calcule atomáticamente el dígito de control, si le es más cómodo.\n\nA continuación se va a recortar el código a 13 dígitos y se intentará comprobar la suma de control.", 
                               padre = self.wids['ventana'])
            codigo = codigo[:13]
        if len(codigo) == 13:
            digitocontrol = self.calcular_digitoc(codigo[:12])
            if codigo[12] != digitocontrol:
                utils.dialogo_info(titulo = "FALLÓ SUMA DE COMPROBACIÓN", 
                                   texto = "El dígito de control no es correct"
                                           "o. Se corregirá automáticamente.", 
                                   padre = self.wids['ventana'])
                codigo = codigo[:12] + digitocontrol
        descripcion = self.wids['e_descripcion'].get_text()
        linea = pclases.LineaDeProduccion.select(
            pclases.LineaDeProduccion.q.nombre.contains('fibra'))[0]
        lineaembol = pclases.LineaDeProduccion.select(
            pclases.LineaDeProduccion.q.nombre.contains('bolsa'))[0]
        nombre = self.wids['e_nombre'].get_text()
        arancel = self.wids['e_arancel'].get_text()
        try:
            precio = utils.parse_float(self.wids['e_precio'].get_text().replace(',','.'))
        except ValueError:
            precio = producto.preciopordefecto
        try:
            minimo = utils.parse_float(self.wids['e_minimo'].get_text())
        except ValueError:
            minimo = producto.minimo
        try:
            dtex = utils.parse_float(self.wids['e_dtex'].get_text())
        except ValueError:
            dtex = producto.camposEspecificosBala.dtex
        try:
            corte = int(self.wids['e_corte'].get_text())
        except ValueError:
            dtex = producto.camposEspecificosBala.dtex
        gramosBolsa = utils.parse_numero(self.wids['e_gramosBolsa'].get_text())
        producto.camposEspecificosBala.gramosBolsa = gramosBolsa
        bolsasCaja = utils.parse_numero(self.wids['e_bolsasCaja'].get_text())
        producto.camposEspecificosBala.bolsasCaja = bolsasCaja
        cajasPale = utils.parse_numero(self.wids['e_cajasPale'].get_text())
        producto.camposEspecificosBala.cajasPale = cajasPale
        color = self.wids['e_color'].get_text()
        antiuv = self.wids['chk_antiuv'].get_active()
        reciclada = self.wids['ch_reciclada'].get_active()
        idtipoMaterialBala = utils.combo_get_value(self.wids['cb_material']) 
        prodestandar = self.wids['e_prodestandar'].get_text()
        try:
            prodestandar = utils.parse_float(prodestandar)
        except ValueError:
            prodestandar = 0.0
        # Desactivo el notificador momentáneamente
        producto.notificador.activar(lambda: None)
        # Actualizo los datos del objeto
        producto.prodestandar = prodestandar
        try:
            producto.codigo = codigo
        except psycopg_ProgrammingError:
            try:
                producto_asignado = pclases.ProductoVenta.select(
                    pclases.ProductoVenta.q.codigo == codigo)[0]
                producto_asignado = producto_asignado.descripcion
            except IndexError:
                producto_asignado = "?"
            utils.dialogo_info(titulo = "CÓDIGO DUPLICADO", 
                               texto = "El código EAN %s no se encuentra "
                               "disponible.\nActualmente está asignado a:"
                               " %s" % (codigo, producto_asignado), 
                               padre = self.wids['ventana'])
        producto.descripcion = descripcion
        if producto.camposEspecificosBala.gramosBolsa:
            producto.lineaDeProduccionID = lineaembol.id
        else:
            producto.lineaDeProduccionID = linea.id
        producto.nombre = nombre
        producto.preciopordefecto = precio
        producto.minimo = minimo
        producto.arancel = arancel
        producto.camposEspecificosBala.dtex = dtex
        producto.camposEspecificosBala.corte = corte
        producto.camposEspecificosBala.color = color
        producto.camposEspecificosBala.antiuv = antiuv
        producto.camposEspecificosBala.reciclada = reciclada
        producto.camposEspecificosBala.tipoMaterialBalaID = idtipoMaterialBala
        producto.dni = self.wids['e_dni'].get_text()
        producto.uso = self.wids['e_uso'].get_text()
        if self.wids['ch_no_anno_cert'].get_active():
            producto.annoCertificacion = None
        else:
            producto.annoCertificacion \
                    = self.wids['sp_anno_certificacion'].get_value_as_int()
        cliente = utils.combo_get_value(self.wids['cbe_cliente'])
        if cliente == 0:
            cliente = None
        producto.camposEspecificosBala.clienteID = cliente
        # Fuerzo la actualización de la BD y no espero a que SQLObject lo 
        # haga por mí:
        producto.syncUpdate()
        # Vuelvo a activar el notificador
        producto.notificador.activar(self.aviso_actualizacion)
        self.wids['b_guardar'].set_sensitive(False)
        self.actualizar_ventana()

    def borrar_producto(self, widget):
        """
        Elimina el producto de la tabla pero NO
        intenta eliminar ninguna de sus relaciones,
        de forma que si se incumple alguna 
        restricción de la BD, cancelará la eliminación
        y avisará al usuario.
        """
        producto = self.objeto
        if not utils.dialogo('¿Eliminar el producto?', 'BORRAR'):
            return
        if producto.articulos != [] or producto.precios != []:
            utils.dialogo_info('PRODUCTO NO ELIMINADO', 'El producto está implicado en operaciones que impiden su borrado.', padre = self.wids['ventana'])
        else:
            producto.notificador.desactivar()
            campos = producto.camposEspecificosBala
            try:
                producto.destroy(ventana = __file__)
                campos.destroy(ventana = __file__)
            except:
                utils.dialogo_info(titulo = "NO SE PUEDE ELIMINAR",
                                   texto = "El producto no se puede eliminar. Verifique que no\ntiene ventas o producción relacionada.", 
                                   padre = self.wids['ventana'])
            else:
                self.objeto = None
                self.ir_a_primero()

    def ver_ficha(self, w):
        producto = self.objeto
        from formularios import formulacion_fibra
        formulacion_fibra.FormulacionFibra(producto)
        return

    def ver_articulos(self, w):
        """
        Muestra las existencias del artículo en el almacén
        """
        producto = self.objeto
        elementos = pclases.Articulo.select(pclases.AND(pclases.Articulo.q.albaranSalidaID == None, 
                                                        pclases.Articulo.q.productoVentaID == producto.id, 
                                                        pclases.Bala.q.partidaCargaID == None, 
                                                        pclases.Bala.q.id == pclases.Articulo.q.balaID))
        utils.dialogo_info(titulo = 'EXISTENCIAS', texto = 'Hay %d balas de %s en el almacén.\nEl mínimo es %d.' % (elementos.count(),producto.descripcion,producto.minimo), padre = self.wids['ventana'])

    def ver_tarifas(self, w):
        from formularios import tarifas_de_precios
        tarifas_de_precios.TarifasDePrecios()
        return
        
    def add_campoesp(self, w):
        campo = utils.dialogo_entrada('Introduzca nombre del campo:', 'NOMBRE')
        if not campo:
            return
        valor = utils.dialogo_entrada('Introduzca valor del campo:', 'VALOR')
        if not valor:
            return
        producto = self.objeto
        ce = pclases.CamposEspecificos(productoVenta = producto,
                                       nombre = campo,
                                       valor = valor)
        pclases.Auditoria.nuevo(ce, self.usuario, __file__)
        self.mostrar_especificos()

    def seleccionar_campoesp(self, campos):
        ops = [(c.id, c.nombre) for c in campos]
        return utils.dialogo_combo('SELECCIONE CAMPO', 
                                   'Seleccione un campo al que camiar el valor o eliminar.\nSi desea cambiar el nombre del campo debe eliminarlo\ny crear uno nuevo con el nuevo nombre.\n',
                                   ops)

    def drop_campoesp(self, w):
        producto = self.objeto
        idce = self.seleccionar_campoesp(producto.camposEspecificos)
        if idce == None:
            return
        ce = pclases.CamposEspecificos.get(idce)
        ce.destroy(ventana = __file__)
        self.mostrar_especificos()

    def change_campoesp(self, w):
        producto = self.objeto
        idce = self.seleccionar_campoesp(producto.camposEspecificos)
        if idce == None:
            return
        valor = utils.dialogo_entrada('Introduzca valor del campo:', 'VALOR')
        if valor == None:
            return
        ce = pclases.CamposEspecificos.get(idce)
        ce.valor = valor
        self.mostrar_especificos()

if __name__ == "__main__":
    p = ProductosDeVentaBalas()

