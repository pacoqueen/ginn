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
## ----------------------------------------------------------------
##  
###################################################################
## Changelog:
## 9 de octubre de 2005 -> Inicio 
## 9 de octubre de 2005 -> 90% funcional (faltan fichas de prod.)
## 9 de enero de 2006 -> Separo productos de venta del resto.
## 23 de enero de 2006 -> Portado a clase.
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
from informes.barcode.EANBarCode import EanBarCode
import mx.DateTime
try:
    from psycopg import ProgrammingError as psycopg_ProgrammingError
except ImportError:
    from psycopg2 import ProgrammingError as psycopg_ProgrammingError


class ProductosDeVentaRollos(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self._objetoreciencreado = None
        Ventana.__init__(self, 'productos_de_venta_rollos.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_anterior/clicked': self.ir_a_anterior,
                       'b_siguiente/clicked': self.ir_a_siguiente,
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
                       'b_copyFrom/clicked': self.copy_from, 
                       'b_copyTo/clicked': self.copy_to, 
                       'b_copyDefecto/clicked': self.copy_defecto, 
                       'b_add_marcado/clicked': self.add_marcado, 
                       'b_drop_marcado/clicked': self.borrar_marcado, 
                       'b_historial/clicked': self.mostrar_historial, 
                       'b_fechaInicio/clicked': self.fecha_inicio_marcado, 
                       'b_fechaFin/clicked': self.fecha_fin_marcado, 
                       'cb_marcado/changed': self.cambiar_marcado_mostrado}  
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        self.mostrar_ultimo_marcado()
        self.wids['b_contar'].set_property("visible", False)
        gtk.main()

    def fecha_inicio_marcado(self, boton):
        """
        Cambia la fecha de inicio del marcado CE seleccionado.
        """
        mid = utils.combo_get_value(self.wids['cb_marcado'])
        if mid:
            marcado = pclases.MarcadoCe.get(mid)
            txt = """
            Introduzca la fecha de inicio de aplicación del marcado.
            Cancele este diálogo para indicar que no se debe restringir el 
            inicio de aplicación de estos valores.
            """
            fecha = utils.dialogo_entrada(titulo = "FECHA DE INICIO", 
                                          texto = txt, 
                                          padre = self.wids['ventana'])
            if not fecha or not fecha.strip():
                marcado.fechaInicio = None
            else:
                try:
                    marcado.fechaInicio = utils.parse_fecha(fecha)
                except:
                    utils.dialogo_info(titulo = "ERROR", 
                                       texto = "El texto %s no es una fecha válida." % fecha, 
                                       padre = self.wids['ventana'])
            marcado.sync()
            self.rellenar_marcado_ce(marcado)

    def fecha_fin_marcado(self, boton):
        """
        Cambia la fecha de fin del marcado CE seleccionado.
        """
        mid = utils.combo_get_value(self.wids['cb_marcado'])
        if mid:
            marcado = pclases.MarcadoCe.get(mid)
            txt = """
            Introduzca la fecha de fin de aplicación del marcado.
            Cancele este diálogo para indicar que no se debe restringir el 
            fin de aplicación de estos valores.
            """
            fecha = utils.dialogo_entrada(titulo = "FECHA DE FIN", 
                                          texto = txt, 
                                          padre = self.wids['ventana'])
            if not fecha or not fecha.strip():
                marcado.fechaFin = None
            else:
                try:
                    marcado.fechaFin = utils.parse_fecha(fecha)
                except:
                    utils.dialogo_info(titulo = "ERROR", 
                                       texto = "El texto %s no es una fecha válida." % fecha, 
                                       padre = self.wids['ventana'])
            marcado.sync()
            self.rellenar_marcado_ce(marcado)

    def mostrar_ultimo_marcado(self):
        """
        Muestra el marcado CE del producto coincidente con la fecha actual o 
        los valores por defecto si no los hay.
        """
        if self.objeto:
            hoy = utils.abs_mxfecha(mx.DateTime.localtime())
            marcado = self.objeto.camposEspecificosRollo.buscar_marcado(hoy)
            if marcado:
                utils.combo_set_from_db(self.wids['cb_marcado'], marcado.id)
            else:
                marcado = self.objeto.camposEspecificosRollo
                self.mostrar_marcado(marcado)

    def borrar_marcado(self, boton):
        """
        Elimina la ficha de marcado CE mostrada en pantalla, si la hay.
        No "elimina" los valores por defecto.
        """
        marcado_activo_id = utils.combo_get_value(self.wids['cb_marcado'])
        if marcado_activo_id:
            marcado = pclases.MarcadoCe.get(marcado_activo_id)
            marcado.destroy(ventana = __file__)
            self.actualizar_ventana()

    def cambiar_marcado_mostrado(self, cb):
        """
        Obtiene el ID del marcado CE seleccionado en el combo y lo 
        muestra en pantalla.
        """
        if self.objeto:
            id = utils.combo_get_value(cb)
            if id:
                marcado = pclases.MarcadoCe.get(id)
            else:
                marcado = self.objeto.camposEspecificosRollo
            self.mostrar_marcado(marcado)

    def add_marcado(self, boton):
        """
        Crea una nueva ficha de marcado CE a cero.
        """
        # TODO: PLAN: USABILIDAD: En el marcado actual establecer como fecha 
        # de fin un día antes de la fecha de inicio del que se crea aquí:
        if self.objeto:
            nce = pclases.MarcadoCe(camposEspecificosRollo 
                                        = self.objeto.camposEspecificosRollo, 
                                    fechaInicio = mx.DateTime.localtime(), 
                                    fechaFin = None)
            pclases.Auditoria.nuevo(nce, self.usuario, __file__)
            utils.combo_set_from_db(self.wids['cb_marcado'], nce.id)
            self.rellenar_marcado_ce(nce)

    # --------------- Funciones auxiliares ------------------------------
    def es_diferente(self):
        """
        Devuelve True si la información en pantalla es distinta a la
        del objeto en memoria.
        """
        producto = self.objeto
        if producto == None: return False   # Si no hay producto activo, devuelvo que no hay cambio respecto a la ventana
        # Datos a comparar:
        # - código <-> e_codigo
        # - descripción <-> e_descripcion
        # - nombre <-> e_nombre
        # - preciopordefecto <-> e_precio
        # - minimo <-> e_minimo
        condicion = producto.codigo == self.wids['e_codigo'].get_text()
        # print condicion
        condicion = condicion and (
            producto.descripcion == self.wids['e_descripcion'].get_text())
        condicion = condicion and (
            producto.nombre == self.wids['e_nombre'].get_text())
        condicion = condicion and (
            str(producto.preciopordefecto) == self.wids['e_precio'].get_text())
        condicion = condicion and (
            str(producto.minimo) == self.wids['e_minimo'].get_text())
        condicion = condicion and (
            str(producto.arancel) == self.wids['e_arancel'].get_text())
        condicion = condicion and (
            utils.float2str(producto.prodestandar) 
            == self.wids['e_prodestandar'].get_text())
        cer = producto.camposEspecificosRollo
        condicion = condicion and (
            str(cer.gramos) == self.wids['e_gramos'].get_text())
        condicion = condicion and (
            str(cer.codigoComposan) == self.wids['e_composan'].get_text())
        condicion = condicion and (str(cer.metrosLineales) 
            == self.wids['e_metros_lineales'].get_text())
        condicion = condicion and (utils.float2str(cer.ancho, 
                                                   precision = 3, autodec = 2) 
            == self.wids['e_ancho'].get_text())
        condicion = condicion and (
            str(cer.diametro) == self.wids['e_diametro'].get_text())
        condicion = condicion and (
            str(cer.rollosPorCamion) == self.wids['e_rollo_camion'].get_text())
        condicion = condicion and (
            utils.float2str(cer.pesoEmbalaje) 
            == self.wids['e_peso_embalaje'].get_text())
        condicion = condicion and (cer.fichaFabricacion 
            == self.wids['e_ficha_fabricacion'].get_text())
        condicion = condicion and self.comparar_marcado_ce()
        condicion = condicion and (self.objeto.camposEspecificosRollo.c 
            == self.wids['ch_gtxc'].get_active())
        modelo_etiqueta = utils.combo_get_value(self.wids['cb_etiqueta'])
        if modelo_etiqueta == 0:
            modelo_etiqueta = None
        try:
            modelo_etiqueta_objeto = cer.modeloEtiqueta.id
        except AttributeError:
            modelo_etiqueta_objeto = None
        condicion = (condicion and modelo_etiqueta_objeto == modelo_etiqueta)
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
        cols = (('Tarifa', 'gobject.TYPE_STRING', False, True, True, None),
                ('Precio', 'gobject.TYPE_FLOAT', False, True, False, None),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_tarifas'], cols)
        etiquetas = ((0, "Estándar Geotexan"), )
        for modelo in pclases.ModeloEtiqueta.select():
            etiquetas += ((modelo.id, modelo.nombre), )
        utils.rellenar_lista(self.wids['cb_etiqueta'], etiquetas)

    def activar_widgets(self, s, chequear_permisos = True):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        ws = ('e_idproducto', 'e_codigo', 'e_descripcion', 'e_nombre', 
              'e_precio', 'e_minimo', 'e_stock', 'b_contar', 'e_gramos' , 
              'e_composan', 'e_diametro' , 'e_ancho' , 'e_rollo_camion',
              'e_peso_embalaje', 'e_metros_lineales', 'b_borrar', 'b_fichas', 
              'b_articulos','b_tarifas','e_arancel', 'e_prodestandar', 
              'frame2', 'table3', "ch_gtxc", "e_ficha_fabricacion", 
              "cb_etiqueta")
        for w in ws:
            self.wids[w].set_sensitive(s)
        if chequear_permisos:
            self.check_permisos(
                nombre_fichero_ventana = "productos_de_venta_rollos.py")
        if self.objeto and len(self.objeto.articulos) > 0:
            self.wids['ch_gtxc'].set_sensitive(False)
            # Una vez fabricado algo, no dejo que cambie el tipo de producto 
            # a geotextil C o viceversa porque si no me forma una trapatiesta 
            # en la BD de aúpa.
        activar_campos_esp = bool(self.objeto 
                                  and not self.objeto.camposEspecificosRollo.c)
        for w in ("e_gramos", "e_ancho", "e_composan", "e_diametro", 
                  "e_rollo_camion", "e_metros_lineales", "e_ficha_fabricacion", 
                  "table3", "hbox7", "hbox6", "hbox5"):
            self.wids[w].set_sensitive(s and activar_campos_esp)

    def ir_a_primero(self):
        """
        Hace que el primer registro -si lo hay- de la tabla implicada
        en el objeto del formulario sea el objeto activo.
        """
        producto = self.objeto
        try:
            # Anulo el aviso de actualización del envío que deja de ser activo.
            linea = pclases.LineaDeProduccion.select(pclases.LineaDeProduccion.q.nombre.contains('geotextiles'))[0]
            if producto != None: producto.notificador.desactivar()
            producto = pclases.ProductoVenta.select(pclases.AND(pclases.ProductoVenta.q.camposEspecificosRolloID != None, 
                                                                  pclases.ProductoVenta.q.lineaDeProduccionID == linea.id), 
                                                    orderBy = "-id")[0]  
                # Selecciono todos y me quedo con el ÚLTIMO de la lista
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
                                       texto = 'Los cambios no se pudieron guardar automáticamente.\nDebe hacerlo de forma manual', 
                                       padre = self.wids['ventana'])
                    return 
        producto = self.objeto
        linea = pclases.LineaDeProduccion.select(pclases.LineaDeProduccion.q.nombre.contains('geotextiles'))[0]
        try:
            anterior = pclases.ProductoVenta.select(pclases.AND(pclases.ProductoVenta.q.camposEspecificosRolloID != None, pclases.ProductoVenta.q.lineaDeProduccionID == linea.id, pclases.ProductoVenta.q.id < producto.id),orderBy='-id')[0]
        except IndexError:
            utils.dialogo_info(texto = "El elemento seleccionado es el primero registrado en el sistema",
                               titulo="ERROR", 
                               padre = self.wids['ventana'])
            return
        self.objeto = anterior
        self.actualizar_ventana()
        self.mostrar_ultimo_marcado()
        
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
        linea = pclases.LineaDeProduccion.select(pclases.LineaDeProduccion.q.nombre.contains('geotextiles'))[0]
        try:
            siguiente = pclases.ProductoVenta.select(pclases.AND(pclases.ProductoVenta.q.camposEspecificosRolloID != None, pclases.ProductoVenta.q.lineaDeProduccionID == linea.id, pclases.ProductoVenta.q.id > producto.id),orderBy='id')[0]
        except IndexError:
            utils.dialogo_info(texto = "El elemento seleccionado es el último registrado en el sistema",
                               titulo="ERROR",
                               padre = self.wids['ventana'])
            return
        self.objeto = siguiente
        self.actualizar_ventana()
        self.mostrar_ultimo_marcado()
   
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
                                             padre = self.wids['ventana'])
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
        producto = self.objeto
        if len(producto.articulos) > 0:
            self.wids['ch_gtxc'].set_sensitive(False)
            # No puede cambiar el tipo de producto una vez fabricado algo.
        self.wids['i_barcode'].set_from_file(EanBarCode().getImage(producto.codigo))
        self.wids['e_codigo'].set_text(producto.codigo)
        self.wids['e_descripcion'].set_text(producto.descripcion)
        self.wids['e_nombre'].set_text(producto.nombre)
        self.wids['e_precio'].set_text(str(producto.preciopordefecto))
        self.wids['e_minimo'].set_text(str(producto.minimo))
        self.wids['e_arancel'].set_text(str(producto.arancel))
        self.wids['e_prodestandar'].set_text(utils.float2str(producto.prodestandar))
        campos = producto.camposEspecificosRollo
        self.wids['ch_gtxc'].set_active(campos.c)
        self.wids['e_ancho'].set_text(utils.float2str(campos.ancho, 
                                                      precision = 3, 
                                                      autodec = 2))
        self.wids['e_gramos'].set_text(str(campos.gramos))
        self.wids['e_metros_lineales'].set_text(str(campos.metrosLineales))
        if campos.ancho <= 0:
            self.wids['e_ancho'].modify_base(gtk.STATE_NORMAL, 
                self.wids['e_ancho'].get_colormap().alloc_color("red"))
        else:
            self.wids['e_ancho'].modify_base(gtk.STATE_NORMAL, 
                self.wids['e_ancho'].get_colormap().alloc_color("white"))
        if campos.gramos <= 0:
            self.wids['e_gramos'].modify_base(gtk.STATE_NORMAL, 
                self.wids['e_gramos'].get_colormap().alloc_color("red"))
        else:
            self.wids['e_gramos'].modify_base(gtk.STATE_NORMAL, 
                self.wids['e_gramos'].get_colormap().alloc_color("white"))
        colormap = self.wids['e_metros_lineales'].get_colormap()
        if campos.metrosLineales <= 0:
            self.wids['e_metros_lineales'].modify_base(gtk.STATE_NORMAL, 
                colormap.alloc_color("red"))
        else:
            self.wids['e_metros_lineales'].modify_base(gtk.STATE_NORMAL, 
                colormap.alloc_color("white"))
        self.wids['e_composan'].set_text(str(campos.codigoComposan))
        self.wids['e_diametro'].set_text(str(campos.diametro))
        self.wids['e_rollo_camion'].set_text(str(campos.rollosPorCamion))
        self.wids['e_peso_embalaje'].set_text(utils.float2str(campos.pesoEmbalaje))
        self.wids['e_ficha_fabricacion'].set_text(campos.fichaFabricacion)
        try:
            modelo_etiqueta = campos.modeloEtiqueta.id
        except AttributeError:
            modelo_etiqueta = 0
        utils.combo_set_from_db(self.wids['cb_etiqueta'], 
                                modelo_etiqueta)
        # Datos no modificables:
        self.wids['e_idproducto'].set_text(`producto.id`)
        self.muestra_stock()
        # self.wids['e_stock'].set_text("Pulse para consultar almacén.")
        self.mostrar_especificos()
        self.rellenar_tabla_tarifas()
        self.rellenar_marcado_ce()
        self.objeto.make_swap()
        linea = pclases.LineaDeProduccion.select(
            pclases.LineaDeProduccion.q.nombre.contains('geotextiles'))[0]
        anteriores = pclases.ProductoVenta.select(pclases.AND(
                pclases.ProductoVenta.q.camposEspecificosRolloID != None, 
                pclases.ProductoVenta.q.lineaDeProduccionID == linea.id, 
                pclases.ProductoVenta.q.id < producto.id))
        siguientes = pclases.ProductoVenta.select(pclases.AND(
                pclases.ProductoVenta.q.camposEspecificosRolloID != None, 
                pclases.ProductoVenta.q.lineaDeProduccionID == linea.id, 
                pclases.ProductoVenta.q.id > producto.id))
        self.wids['b_anterior'].set_sensitive(anteriores.count())
        self.wids['b_siguiente'].set_sensitive(siguientes.count())

    def rellenar_marcado_ce(self, marcado_activo = None):
        """
        Introduce los valores del marcado CE en los entries.
        Tambien reconstruye el combo de marcados y selecciona el activo.
        Si no hay marcado activo o se quiere mostrar el marcado por defecto, 
        se debe pasar None.
        """
        if self.objeto != None:
            marcados = [(0, "Valores por defecto")]
            marcados += [(m.id, "%s - %s" % (
                     m.fechaInicio and utils.str_fecha(m.fechaInicio) or "N/A", 
                     m.fechaFin and utils.str_fecha(m.fechaFin) or "N/A"))
                     for m in self.objeto.camposEspecificosRollo.marcadosCe]
            utils.rellenar_lista(self.wids['cb_marcado'], marcados)
            if not marcado_activo:
                utils.combo_set_from_db(self.wids['cb_marcado'], 0)
                cer = self.objeto.camposEspecificosRollo
            else:
                try:
                    assert isinstance(marcado_activo, pclases.MarcadoCe)
                    utils.combo_set_from_db(self.wids['cb_marcado'], 
                                            marcado_activo.id)
                    cer = marcado_activo
                except (AttributeError, AssertionError):
                    utils.combo_set_from_db(self.wids['cb_marcado'], 0)
                    cer = self.objeto.camposEspecificosRollo
            self.mostrar_marcado(cer)

    def mostrar_marcado(self, cer):
        # "Atributos"
        for nombre_campo in [k for k in cer._SO_columnDict.keys() if "Prueba" in k]:
            valor_campo = getattr(cer, nombre_campo)
            valor_texto = utils.float2str(valor_campo, 3, autodec = True)
            self.wids["e_%s" % (nombre_campo)].set_text(valor_texto)
        # "Propiedades"
        for nombre_property in [k for k in dir(cer) if "valorPrueba" in k]:
            valor_campo = getattr(cer, nombre_property)
            valor_texto = utils.float2str(valor_campo, 3, autodec = True)
            self.wids["e_%s" % (nombre_property)].set_text(valor_texto)

    def comparar_marcado_ce(self):
        """
        Compara los valores con los de la ventana y devuelve True 
        si son iguales.
        """
        if self.objeto != None:
            try:
                id = utils.combo_get_value(self.wids['cb_marcado'])
            except AttributeError:  # Demasiado tiempo contando stock, aún 
                                    # no se ha rellenado la tabla:
                id = None
            if id:
                cer = pclases.MarcadoCe.get(id)
            else:
                cer = self.objeto.camposEspecificosRollo
            # "Atributos"
            for nombre_campo in [k for k in cer._SO_columnDict.keys() if "Prueba" in k]:
                valor_campo = getattr(cer, nombre_campo)
                valor_texto = utils.float2str(valor_campo, 3, autodec = True)
                valor_ventana = self.wids["e_%s" % (nombre_campo)].get_text()
                if valor_ventana != valor_texto:
                    return False
            # "Propiedades"
            for nombre_property in [k for k in dir(cer) if "valorPrueba" in k]:
                valor_campo = getattr(cer, nombre_property)
                valor_texto = utils.float2str(valor_campo, 3, autodec = True)
                valor_ventana = self.wids["e_%s" % (nombre_property)].get_text()
                if valor_ventana != valor_texto:
                    return False
        return True

    def guardar_marcado_ce(self):
        """
        Guarda los valores del marcado CE en los entries.
        """
        if self.objeto != None:
            valores_malos = []
            id = utils.combo_get_value(self.wids['cb_marcado'])
            if id == 0:
                cer = self.objeto.camposEspecificosRollo
            else:
                cer = pclases.MarcadoCe.get(id)
            # "Atributos"
            for nombre_campo in [k for k in cer._SO_columnDict.keys() if "Prueba" in k]:
                valor_ventana = self.wids["e_%s" % (nombre_campo)].get_text()
                try:
                    valor_campo = utils._float(valor_ventana)
                except ValueError:
                    valores_malos.append((valor_ventana, nombre_campo))
                else:
                    setattr(cer, nombre_campo, valor_campo)
            #self.rellenar_marcado_ce()
            if valores_malos != []:
                txt_valores_malos = "\n".join(["%s: %s" % (nombre, valor) for valor, nombre in valores_malos])
                utils.dialogo_info(titulo = "VALORES ERRÓNEOS", 
                                   texto = "Los siguientes valores no son correctos:\n%s.\nSe ignorarán y se usarán en su lugar los valores originales." % (txt_valores_malos), 
                                   padre = self.wids['ventana'])

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
            filas = 1   # Para evitar el "assert". De todas formas aunque sea 
                # de 1x2, si no hay datos específicos no se va a mostrar nada.
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
        self.wids['e_stock'].set_text("%s m²" % utils.float2str(round(producto.get_stock())))
        vpro.ocultar()

    def calcular_digitoc(self, cod):
        #def sup(n):
        #    return ((n+9)/10)*10
        #peso = 1
        #sum = 0
        #for d in cod:
        #    sum += int(d) * peso
        #    if peso == 1:
        #        peso = 3
        #    else:
        #        peso = 1
        #return str(sup(sum) - sum)
        pesos = [1, 3]*6
        magic = 10
        sum = 0
        for i in range(12):
            sum = sum + int(cod[i]) * pesos[i]
        z = (magic - (sum % magic)) % magic
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
        #prods = pclases.ProductoVenta.select(pclases.AND(pclases.ProductoVenta.q.camposEspecificosRolloID !=None, 
        #                                                   pclases.ProductoVenta.q.codigo.startswith('843603219')))
        prods = pclases.ProductoVenta.select(
            pclases.ProductoVenta.q.codigo.startswith('843603219'))
        codsproducto = [p.codigo[-4:-1] for p in prods]
        codsproducto.sort()
        for i in xrange(1000):  # Si el subcódigo de producto del EAN-13 está duplicado esto no funcionará.
                                # Añadida restricción UNIQUE en la BD para evitarlo.
            # print i, int(codsproducto[i])
            try:
                if i != int(codsproducto[i]):
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
        codtemp = codpais+codempresa+codproducto 
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
        campos = pclases.CamposEspecificosRollo(gramos = 0,
                                                metrosLineales = 0,
                                                codigoComposan = '',
                                                ancho = 0,
                                                diametro = 0,
                                                rollosPorCamion = 0, 
                                                c = False, 
                                                modeloEtiqueta = None)
        linea = pclases.LineaDeProduccion.select(pclases.LineaDeProduccion.q.nombre.contains('geotextiles'))[0] 
        producto = pclases.ProductoVenta(lineaDeProduccion = linea,
                                         camposEspecificosBala = None,
                                         camposEspecificosRollo = campos, 
                                         codigo = self.generar_codigo_ean(), 
                                         nombre = '',
                                         descripcion = '', 
                                         preciopordefecto = 0, 
                                         minimo = 0,
                                         arancel = '')
        self._objetoreciencreado = producto
        utils.dialogo_info('PRODUCTO CREADO', 
                           'Se ha creado un producto nuevo.\nA continuación complete la información del producto y guarde los cambios.\n\nNO OLVIDE INTRODUCIR LOS METROS LINEALES Y ANCHO, \nASÍ COMO INTRODUCIR LA FORMULACIÓN PARA EL CONSUMO AUTOMÁTICO EN LA VENTANA CORRESPONDIENTE.', 
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
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR PRODUCTO", 
                                         texto = "Introduzca código, nombre o descripción de producto:", 
                                         padre = self.wids['ventana']) 
        if a_buscar != None:
            try:
                ida_buscar = int(a_buscar)
            except ValueError:
                ida_buscar = -1
            criterio = pclases.OR(pclases.ProductoVenta.q.codigo.contains(a_buscar),
                                    pclases.ProductoVenta.q.descripcion.contains(a_buscar),
                                    pclases.ProductoVenta.q.nombre.contains(a_buscar),
                                    pclases.ProductoVenta.q.id == ida_buscar)
            linea = pclases.LineaDeProduccion.select(pclases.LineaDeProduccion.q.nombre.contains('geotextiles'))[0]
            criterio = pclases.AND(criterio, pclases.ProductoVenta.q.camposEspecificosRolloID != None, pclases.ProductoVenta.q.lineaDeProduccionID == linea.id)
            resultados = pclases.ProductoVenta.select(criterio)
            if resultados.count() > 1:
                    ## Refinar los resultados
                    idproducto = self.refinar_resultados_busqueda(resultados)
                    if idproducto == None:
                        return
                    resultados = [pclases.ProductoVenta.get(idproducto)]
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
            try:
                producto = resultados[0]
                # Al borrar alguien desde otro ordenador un producto, me ha saltado a mí esta excepción al buscar en mi ventana 
                # otro producto que ni siquiera tenía nada que ver. Creo que es porque la consulta de la búsqueda anterior al 
                # borrado no se refresca al volver a buscar. Sospecho. Si se cierra y vuelve a abrir la ventana, no hay problemas.
                # Traceback (most recent call last):
                #   File "./productos_de_venta_rollos.py", line 473, in buscar_producto
                #     producto = resultados[0]
                # IndexError: list index out of range
            except IndexError:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "Se produjo un error al recuperar la información.\nCierre y vuelva a abrir la ventana antes de volver a intentarlo.", 
                                   padre = self.wids['texto'])
                return
            # Y activo la función de notificación:
            producto.notificador.activar(self.aviso_actualizacion)
            self.activar_widgets(True)
        self.objeto = producto
        self.actualizar_ventana()
        self.mostrar_ultimo_marcado()

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
                                   texto = "El dígito de control no es correcto. Se corregirá automáticamente.", 
                                   padre = self.wids['ventana'])
                codigo = codigo[:12] + digitocontrol
        descripcion = self.wids['e_descripcion'].get_text()
        # idlinea Un producto pertenece a una línea, no se puede cambiar
        nombre = self.wids['e_nombre'].get_text()
        arancel = self.wids['e_arancel'].get_text()
        try:
            precio = float(self.wids['e_precio'].get_text())
        except ValueError:
            precio = producto.preciopordefecto
        try:
            minimo = float(self.wids['e_minimo'].get_text())
        except ValueError:
            minimo = producto.minimo
        try:
            gramos = int(self.wids['e_gramos'].get_text())
        except ValueError:
            gramos = producto.camposEspecificosRollo.gramos
        try:
            ancho = float(self.wids['e_ancho'].get_text())
        except ValueError:
            ancho = producto.camposEspecificosRollo.ancho
        try:
            diametro = int(self.wids['e_diametro'].get_text())
        except ValueError:
            diametro = producto.camposEspecificosRollo.diametro
        try:
            metrosLineales = int(self.wids['e_metros_lineales'].get_text())
        except:
            metrosLineales = producto.camposEspecificosRollo.metrosLineales
        try:
            rolloCamion = int(self.wids['e_rollo_camion'].get_text())
        except ValueError:
            rolloCamion = producto.camposEspecificosRollo.rollosPorCamion
        try:
            pesoEmbalaje = float(self.wids['e_peso_embalaje'].get_text())
        except ValueError:
            pesoEmbalaje = producto.camposEspecificosRollo.pesoEmbalaje
        prodestandar = self.wids['e_prodestandar'].get_text()
        try:
            prodestandar = float(prodestandar)
        except ValueError:
            prodestandar = 0.0
        producto.camposEspecificosRollo.fichaFabricacion \
            = self.wids['e_ficha_fabricacion'].get_text()

        composan = self.wids['e_composan'].get_text()
 
        # Desactivo el notificador momentáneamente
        producto.notificador.activar(lambda: None)
        # Actualizo los datos del objeto
        try:
            producto.codigo = codigo
        except psycopg_ProgrammingError:
            try:
                producto_asignado = pclases.ProductoVenta.select(pclases.ProductoVenta.q.codigo == codigo)[0]
                producto_asignado = producto_asignado.descripcion
            except IndexError:
                producto_asignado = "?"
            utils.dialogo_info(titulo = "CÓDIGO DUPLICADO", 
                               texto = "El código EAN %s no se encuentra disponible.\nActualmente está asignado a: %s" % (codigo, producto_asignado), 
                               padre = self.wids['ventana'])
        producto.descripcion = descripcion
        producto.nombre = nombre
        producto.preciopordefecto = precio
        producto.minimo = minimo
        producto.arancel = arancel
        producto.prodestandar = prodestandar
        producto.camposEspecificosRollo.gramos = gramos
        producto.camposEspecificosRollo.ancho = ancho
        producto.camposEspecificosRollo.diametro = diametro
        producto.camposEspecificosRollo.codigoComposan = composan
        producto.camposEspecificosRollo.rollosPorCamion = rolloCamion
        producto.camposEspecificosRollo.pesoEmbalaje = pesoEmbalaje
        producto.camposEspecificosRollo.metrosLineales = metrosLineales
        marcado_activo_id = utils.combo_get_value(self.wids["cb_marcado"])
        producto.camposEspecificosRollo.c = self.wids['ch_gtxc'].get_active()
        modelo_etiqueta = utils.combo_get_value(self.wids['cb_etiqueta'])
        if modelo_etiqueta == 0:
            modelo_etiqueta = None
        producto.camposEspecificosRollo.modeloEtiquetaID = modelo_etiqueta
        self.guardar_marcado_ce()
        # Fuerzo la actualización de la BD y no espero a que SQLObject 
        # lo haga por mí:
        producto.syncUpdate()
        producto.camposEspecificosRollo.syncUpdate()
        # Vuelvo a activar el notificador
        producto.notificador.activar(self.aviso_actualizacion)
        self.actualizar_ventana()
        if marcado_activo_id:
            marcado_activo = pclases.MarcadoCe.get(marcado_activo_id)
            self.rellenar_marcado_ce(marcado_activo = marcado_activo)
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
        if not utils.dialogo('¿Eliminar el producto?', 'BORRAR', padre = self.wids['ventana']):
            return
        if producto.articulos != [] or producto.precios != []:
            utils.dialogo_info('PRODUCTO NO ELIMINADO', 
                               'El producto está implicado en operaciones que impiden su borrado.', 
                               padre = self.wids['ventana'])
        else:
            producto.notificador.desactivar()
            cer = producto.camposEspecificosRollo
            producto.camposEspecificosRollo = None
            try:
                producto.destroy(ventana = __file__)
            except:
                producto.camposEspecificosRollo = cer
                utils.dialogo_info(titulo = "PRODUCTO NO BORRADO", 
                                   texto = "El producto no se pudo eliminar",
                                   padre = self.wids['ventana'])
                self.actualizar_ventana()
                return
            cer.destroy(ventana = __file__)
            self.objeto = None
            self.ir_a_primero()
        # self.actualizar_ventana()

    def ver_ficha(self, w):
        producto = self.objeto
        import formulacion_geotextiles
        formulacion_geotextiles.FormulacionGeotextiles(producto)
        return

    def ver_articulos(self, w):
        """
        Muestra las existencias del artículo en el almacén
        """
        producto = self.objeto
        elementos = pclases.Articulo.select(pclases.AND(pclases.Articulo.q.albaranSalidaID == None,pclases.Articulo.q.productoVentaID == producto.id))
        utils.dialogo_info(titulo = 'EXISTENCIAS', 
                           texto = 'Hay %d unidades de %s en el almacén.\nEl mínimo es %d' \
                            % (elementos.count(),producto.descripcion,producto.minimo),
                           padre = self.wids['ventana'])
        return
        
    def ver_tarifas(self, w):
        producto = self.objeto
        import tarifas_de_precios
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

    def get_filas_marcado(self):
        """
        Devuelve las filas para la ventana de búsqueda de copia de valores de 
        marcado.
        """
        cers = pclases.CamposEspecificosRollo.select(
            pclases.CamposEspecificosRollo.q.gramos 
                == self.objeto.camposEspecificosRollo.gramos)
        pvs = [cer.productosVenta[0] 
               for cer in cers if len(cer.productosVenta) == 1]
        filas = [(
            pv.id, 
            pv.descripcion, 
            pv.camposEspecificosRollo.gramos, 
            pv.camposEspecificosRollo.estandarPruebaGramaje, 
            pv.camposEspecificosRollo.estandarPruebaAlargamientoLongitudinal, 
            pv.camposEspecificosRollo.estandarPruebaLongitudinal, 
            pv.camposEspecificosRollo.estandarPruebaTransversal, 
            pv.camposEspecificosRollo.estandarPruebaAlargamientoTransversal, 
            pv.camposEspecificosRollo.estandarPruebaCompresion, 
            pv.camposEspecificosRollo.estandarPruebaPerforacion, 
            pv.camposEspecificosRollo.estandarPruebaEspesor, 
            pv.camposEspecificosRollo.estandarPruebaPermeabilidad, 
            pv.camposEspecificosRollo.estandarPruebaPoros, 
            pv.camposEspecificosRollo.estandarPruebaPiramidal 
            ) for pv in pvs]
        filas.append((0, "Búsqueda manual") + (0.0, ) * 12)
        return filas
    
    def buscar_producto_para_marcado(self):
        """
        Devuelve un producto resultado de una búsqueda.
        """
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR PRODUCTO", 
                                         texto = "Introduzca código, nombre o descripción de producto:", 
                                         padre = self.wids['ventana']) 
        if a_buscar == None:
            return None
        else:
            try:
                ida_buscar = int(a_buscar)
            except ValueError:
                ida_buscar = -1
            criterio = pclases.OR(pclases.ProductoVenta.q.codigo.contains(a_buscar),
                                  pclases.ProductoVenta.q.descripcion.contains(a_buscar),
                                  pclases.ProductoVenta.q.nombre.contains(a_buscar),
                                  pclases.ProductoVenta.q.id == ida_buscar)
            linea = pclases.LineaDeProduccion.select(pclases.LineaDeProduccion.q.nombre.contains('geotextiles'))[0]
            criterio = pclases.AND(criterio, pclases.ProductoVenta.q.camposEspecificosRolloID != None, 
                                   pclases.ProductoVenta.q.lineaDeProduccionID == linea.id)
            resultados = pclases.ProductoVenta.select(criterio)
            if resultados.count() > 1:
                    ## Refinar los resultados
                    idproducto = self.refinar_resultados_busqueda(resultados)
                    if idproducto == None:
                        return
                    resultados = [pclases.ProductoVenta.get(idproducto)]
                    # Me quedo con una lista de resultados de un único objeto ocupando la primera posición.
                    # (Más abajo será cuando se cambie realmente el objeto actual por este resultado.)
            elif resultados.count() < 1:
                    ## Sin resultados de búsqueda
                    utils.dialogo_info('SIN RESULTADOS', 'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.\n(Atención: Ver la lista completa puede resultar lento si el número de elementos es muy alto)',
                                       padre = self.wids['ventana'])
                    return None
            ## Un único resultado
            # Primero anulo la función de actualización
            try:
                producto = resultados[0]
                # Al borrar alguien desde otro ordenador un producto, me ha saltado a mí esta excepción al buscar en mi ventana 
                # otro producto que ni siquiera tenía nada que ver. Creo que es porque la consulta de la búsqueda anterior al 
                # borrado no se refresca al volver a buscar. Sospecho. Si se cierra y vuelve a abrir la ventana, no hay problemas.
                # Traceback (most recent call last):
                #   File "./productos_de_venta_rollos.py", line 473, in buscar_producto
                #     producto = resultados[0]
                # IndexError: list index out of range
            except IndexError:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "Se produjo un error al recuperar la información.\nCierre y vuelva a abrir la ventana antes de volver a intentarlo.", 
                                   padre = self.wids['texto'])
                return None
            else:
                return producto

    def copy_from(self, boton = None):
        """
        Copia los valores de marcado de otro producto al actual.
        Muestra una ventana de resultados con los marcados de los productos 
        que tienen el mismo gramaje que el actual y una opción para búsqueda 
        manual.
        Del producto seleccionado copia los valores de marcado de su 
        CamposEspecificosRollo al objeto actual si es distinto de None.
        """
        if self.objeto != None:
            filas = self.get_filas_marcado()
            idproducto = utils.dialogo_resultado(
                            filas, 
                            titulo = "Seleccione producto", 
                            cabeceras = ("ID", 
                                         "Descripción", 
                                         "gr", 
                                         "Gramaje", 
                                         "A. long.", 
                                         "R. long.", 
                                         "R. trans.", 
                                         "A. trans.", 
                                         "Compr.", 
                                         "Perf.", 
                                         "Espesor", 
                                         "Perm.", 
                                         "Porom.", 
                                         "P.Piram."), 
                            padre = self.wids['ventana'], 
                            multi = False)
            if not isinstance(idproducto, int):
                try:
                    idproducto = int(idproducto)
                except Exception, msg:
                    txt = "%sproductos_de_venta_rollos::Error en búsqueda al "\
                          "convertir a entero. Mensaje de la excepción: %s"%(
                            self.usuario and self.usuario.usuario or "", msg)
                    self.logger.error(txt)
                    print txt
                    self.utils.dialogo_info(titulo = "ERROR", 
                                            texto = txt, 
                                            padre = self.wids['ventana'])
            if idproducto > 0:
                pv = pclases.ProductoVenta.get(idproducto)
                cer = pv.camposEspecificosRollo # TODO: Aquí habría que coger
                # el marcado vigente o dejar elegir desde cual traerse los 
                # valores.
                mid = utils.combo_get_value(self.wids['cb_marcado'])
                if not mid:
                    dst = self.objeto.camposEspecificosRollo
                else:
                    dst = pclases.MarcadoCe.get(mid)
                cer._copyMarcadoTo(dst)
                self.actualizar_ventana()
            elif idproducto == 0:
                producto = self.buscar_producto_para_marcado()
                if producto != None:
                    cer = producto.camposEspecificosRollo
                    mid = utils.combo_get_value(self.wids['cb_marcado'])
                    if not mid:
                        dst = self.objeto.camposEspecificosRollo
                    else:
                        dst = pclases.MarcadoCe.get(mid)
                    cer._copyMarcadoTo(dst)
                    #self.actualizar_ventana()
                    self.rellenar_marcado_ce(cer)

    def copy_to(self, boton = None):
        """
        Copia los valores del producto actual a uno o varios seleccionados 
        por el usuario.
        Muestra una ventana de resultados con los productos del mismo 
        gramaje y una opción especial para búsqueda manual. En todos los 
        productos seleccionados se copian los valores del marcado del 
        objeto en pantalla.
        """
        if self.objeto != None:
            filas = self.get_filas_marcado()
            idsproducto = utils.dialogo_resultado(
                            filas, 
                            titulo = "Seleccione productos", 
                            cabeceras = ("ID", 
                                         "Descripción", 
                                         "gr", 
                                         "Gramaje", 
                                         "A. long.", 
                                         "R. long.", 
                                         "R. trans.", 
                                         "A. trans.", 
                                         "Compr.", 
                                         "Perf.", 
                                         "Espesor", 
                                         "Perm.", 
                                         "Porom.", 
                                         "P.Piram."), 
                            padre = self.wids['ventana'], 
                            multi = True)
            for idproducto in idsproducto:
                if not isinstance(idproducto, int):
                    try:
                        idproducto = int(idproducto)
                    except Exception, msg:
                        txt = "%sproductos_de_venta_rollos::Error en búsqueda al convertir a entero. Mensaje de la excepción: %s" % (
                            self.usuario and self.usuario.usuario or "", msg)
                        self.logger.error(txt)
                        print txt
                        self.utils.dialogo_info(titulo = "ERROR", 
                                                texto = txt, 
                                                padre = self.wids['ventana'])
                if idproducto > 0:
                    pv = pclases.ProductoVenta.get(idproducto)
                    cer = pv.camposEspecificosRollo
                    mid = utils.combo_get_value(self.wids['cb_marcado'])
                    if not mid:
                        org = self.objeto.camposEspecificosRollo
                    else:
                        org = pclases.MarcadoCe.get(mid)
                    org._copyMarcadoTo(cer) # TODO: Permitir seleccionar si 
                    # copiar a los valores por defecto (cer) o algún marcado 
                    # adicional, el marcado vigente para el producto, etc.
                elif idproducto == 0:
                    producto = self.buscar_producto_para_marcado()
                    if producto != None:
                        cer = producto.camposEspecificosRollo
                        mid = utils.combo_get_value(self.wids['cb_marcado'])
                        if not mid:
                            org = self.objeto.camposEspecificosRollo
                        else:
                            org = pclases.MarcadoCe.get(mid)
                        org._copyMarcadoTo(cer)

    def copy_defecto(self, boton = None):
        """
        Inserta los valores por defecto en la ventana para el producto
        actual, pero no los guarda.
        """
        if self.objeto != None:
            valores = get_valores_defecto_marcado()
            mid = utils.combo_get_value(self.wids['cb_marcado'])
            if not mid:
                cer = self.objeto.camposEspecificosRollo
                producto = cer.productosVenta[0]
            else:
                cer = pclases.MarcadoCe.get(mid)
                producto = cer.camposEspecificosRollo.productosVenta[0]
            for campo in valores:
                for nt in valores[campo]:
                    if "%s " % (nt) in producto.descripcion:
                        setattr(cer, campo, valores[campo][nt]) 
            #self.actualizar_ventana()
            self.rellenar_marcado_ce(cer)

    def mostrar_historial(self, boton):
        hs = self.objeto.historialesExistencias[:]
        hs.sort(lambda h1, h2: utils.cmp_abs_mxfecha(h1.fecha, h2.fecha))
        hs = [(h.id, 
               utils.str_fecha(h.fecha), 
               utils.float2str(h.cantidad), 
               `h.bultos`) for h in hs]
        utils.dialogo_resultado(titulo = "HISTORIAL DE EXISTENCIAS", 
                                filas = hs, 
                                padre = self.wids['ventana'], 
                                cabeceras = ("ID", "Fecha", "m²", "Rollos"))


################################################################################
def get_valores_defecto_marcado():
    """
    Devuelve un diccionario con los valores por defecto del marcado CE.
    """
    valores = {"estandarPruebaGramaje" : 
                {"NT 11": 90, "NT 12": 100, "NT 13": 110, "NT 15": 125, 
                 "NT 17": 140, "NT 18": 160, "NT 21": 180, "NT 23": 200, 
                 "NT 30": 260, "NT 35": 300, "NT 40": 350, "NT 46": 400, 
                 "NT 58": 500}, 
               "toleranciaPruebaGramaje" : 
                {"NT 11": -2, "NT 12": -2, "NT 13": -2, "NT 15": -2, 
                 "NT 17": -2, "NT 18": -2, "NT 21": -2, "NT 23": -2, 
                 "NT 30": -2, "NT 35": -2, "NT 40": -2, "NT 46": -2, 
                 "NT 58": -2},
               "toleranciaPruebaGramajeSup" : 
                {"NT 11": 2, "NT 12": 2, "NT 13": 2, "NT 15": 2, 
                 "NT 17": 2, "NT 18": 2, "NT 21": 2, "NT 23": 2, 
                 "NT 30": 2, "NT 35": 2, "NT 40": 2, "NT 46": 2, 
                 "NT 58": 2}, 
               "estandarPruebaAlargamientoLongitudinal" : 
                {"NT 11": 52.75, "NT 12": 61.88, "NT 13": 44.78, 
                 "NT 15": 62.76, "NT 17": 54.87, "NT 18": 58.50, 
                 "NT 21": 52.92, "NT 23": 54.97, "NT 30": 60.86, 
                 "NT 35": 62.06, "NT 40": 57.02, "NT 46": 65.87, 
                 "NT 58": 59.34},
               "toleranciaPruebaAlargamientoLongitudinal" : 
                {"NT 11": -9.61, "NT 12": -8.41, "NT 13": -4.83, 
                 "NT 15": -6.96, "NT 17": -5.46, "NT 18": -3.53, 
                 "NT 21": -3.89, "NT 23": -3.47, "NT 30": -2.96, 
                 "NT 35": -2.97, "NT 40": -1.78, "NT 46": -4.77, 
                 "NT 58": -1.11},
               "toleranciaPruebaAlargamientoLongitudinalSup" : 
                {"NT 11": 9.61, "NT 12": 8.41, "NT 13": 4.83, "NT 15": 6.96, 
                 "NT 17": 5.46, "NT 18": 3.53, "NT 21": 3.89, "NT 23": 3.47, 
                 "NT 30": 2.96, "NT 35": 2.97, "NT 40": 1.78, "NT 46": 4.77, 
                 "NT 58": 1.11},
               "estandarPruebaLongitudinal" : 
                {"NT 11": 6.46, "NT 12": 7.20, "NT 13": 7.63, "NT 15": 7.72, 
                 "NT 17": 9.16, "NT 18": 11.78, "NT 21": 13.49, "NT 23": 15.64, 
                 "NT 30": 20.41, "NT 35": 21.13, "NT 40": 25.20, 
                 "NT 46": 27.91, "NT 58": 33.53},
               "toleranciaPruebaLongitudinal" : 
                {"NT 11": -1.24*1.5, "NT 12": -0.78*1.5, "NT 13": -0.71*1.5, 
                 "NT 15": -0.91*1.5, "NT 17": -0.66*1.5, "NT 18": -1.27*1.5, 
                 "NT 21": -2.11*1.5, "NT 23": -1.37*1.5, "NT 30": -2.14*1.5, 
                 "NT 35": -1.33*1.5, "NT 40": -1.66*1.5, "NT 46": -1.17*1.5, 
                 "NT 58": -2.41*1.5},
               "toleranciaPruebaLongitudinalSup" : 
                {"NT 11": -1.24, "NT 12": -0.78, "NT 13": -0.71, 
                 "NT 15": -0.91, "NT 17": -0.66, "NT 18": -1.27, 
                 "NT 21": -2.11, "NT 23": -1.37, "NT 30": -2.14, 
                 "NT 35": -1.33, "NT 40": -1.66, "NT 46": -1.17, 
                 "NT 58": -2.41},
               "estandarPruebaTransversal" : 
                {"NT 11": 6.48, "NT 12": 6.97, "NT 13": 9.03, "NT 15": 10.08, 
                 "NT 17": 9.67, "NT 18": 12.02, "NT 21": 12.48, "NT 23": 14.47, 
                 "NT 30": 19.55, "NT 35": 24.82, "NT 40": 25.60, 
                 "NT 46": 31.60, "NT 58": 38.98},
               "toleranciaPruebaTransversal" : 
                {"NT 11": -1.12 * 1.5, "NT 12": -0.51 * 1.5, 
                 "NT 13": -1.39 * 1.5, "NT 15": -1.28 * 1.5, 
                 "NT 17": -1.33 * 1.5, "NT 18": -1.59 * 1.5, 
                 "NT 21": -1.25 * 1.5, "NT 23": -1.44 * 1.5, 
                 "NT 30": -3.66 * 1.5, "NT 35": -3.15 * 1.5, 
                 "NT 40": -1.73 * 1.5, "NT 46": -4.51 * 1.5, 
                 "NT 58": -1.93 * 1.5},
               "toleranciaPruebaTransversalSup" : 
                {"NT 11": -1.12, "NT 12": -0.51, "NT 13": -1.39, 
                 "NT 15": -1.28, "NT 17": -1.33, "NT 18": -1.59, 
                 "NT 21": -1.25, "NT 23": -1.44, "NT 30": -3.66, 
                 "NT 35": -3.15, "NT 40": -1.73, "NT 46": -4.51, 
                 "NT 58": -1.93},
               "estandarPruebaAlargamientoTransversal" : 
                {"NT 11": 62.44, "NT 12": 65.69, "NT 13": 54.78, 
                 "NT 15": 68.16, "NT 17": 61.70, "NT 18": 64.35, 
                 "NT 21": 62.30, "NT 23": 62.65, "NT 30": 66.15, 
                 "NT 35": 62.53, "NT 40": 64.19, "NT 46": 69.63, 
                 "NT 58": 66.85},
               "toleranciaPruebaAlargamientoTransversal" : 
                {"NT 11": -7.50, "NT 12": -9.64, "NT 13": -3.35, 
                 "NT 15": -2.10, "NT 17": -1.24, "NT 18": -4.87, 
                 "NT 21": -2.46, "NT 23": -1.85, "NT 30": -4.43, 
                 "NT 35": -5.13, "NT 40": -2.30, "NT 46": -4.71, 
                 "NT 58": -4.71},
               "toleranciaPruebaAlargamientoTransversalSup" : 
                {"NT 11": 7.50, "NT 12": 9.64, "NT 13": 3.35, "NT 15": 2.10, 
                 "NT 17": 1.24, "NT 18": 4.87, "NT 21": 2.46, "NT 23": 1.85, 
                 "NT 30": 4.43, "NT 35": 5.13, "NT 40": 2.30, "NT 46": 4.71, 
                 "NT 58": 4.71},
               "estandarPruebaCompresion" : 
                {"NT 11": 1.11, "NT 12": 1.23, "NT 13": 1.36, "NT 15": 1.56, 
                 "NT 17": 1.72, "NT 18": 1.96, "NT 21": 2.26, "NT 23": 2.57, 
                 "NT 30": 3.31, "NT 35": 3.93, "NT 40": 4.49, "NT 46": 5.26, 
                 "NT 58": 6.49},
               "toleranciaPruebaCompresion" : 
                {"NT 11": -0.05 * 1.5, "NT 12": -0.09 * 1.5, 
                 "NT 13": -0.17 * 1.5, "NT 15": -0.15 * 1.5, 
                 "NT 17": -0.11 * 1.5, "NT 18": -0.12 * 1.5, 
                 "NT 21": -0.11 * 1.5, "NT 23": -0.05 * 1.5, 
                 "NT 30": -0.11 * 1.5, "NT 35": -0.30 * 1.5, 
                 "NT 40": -0.36 * 1.5, "NT 46": -0.60 * 1.5, 
                 "NT 58": -0.43 * 1.5},
               "toleranciaPruebaCompresionSup" : 
                {"NT 11": -0.05, "NT 12": -0.09, "NT 13": -0.17, 
                 "NT 15": -0.15, "NT 17": -0.11, "NT 18": -0.12, 
                 "NT 21": -0.11, "NT 23": -0.05, "NT 30": -0.11, 
                 "NT 35": -0.30, "NT 40": -0.36, "NT 46": -0.60, 
                 "NT 58": -0.43},
               "estandarPruebaPerforacion" : 
                {"NT 11": 33.07, "NT 12": 28.80, "NT 13": 31.00, 
                 "NT 15": 23.90, "NT 17": 22.27, "NT 18": 19.20, 
                 "NT 21": 17.47, "NT 23": 15.73, "NT 30": 11.80, 
                 "NT 35": 9.80, "NT 40": 7.87, "NT 46": 6.40, 
                 "NT 58": 6.20},
               "toleranciaPruebaPerforacion" : 
                {"NT 11": 1.90, "NT 12": 2.58, "NT 13": 1.30, "NT 15": 2.48, 
                 "NT 17": 1.35, "NT 18": 2.57, "NT 21": 0.37, "NT 23": 0.94, 
                 "NT 30": 1.12, "NT 35": 0.99, "NT 40": 0.76, "NT 46": 1.42, 
                 "NT 58": 0.94},
               "toleranciaPruebaPerforacionSup" : 
                {"NT 11": 1.90 * 1.5, "NT 12": 2.58 * 1.5, "NT 13": 1.30 * 1.5, 
                 "NT 15": 2.48 * 1.5, "NT 17": 1.35 * 1.5, "NT 18": 2.57 * 1.5, 
                 "NT 21": 0.37 * 1.5, "NT 23": 0.94 * 1.5, "NT 30": 1.12 * 1.5, 
                 "NT 35": 0.99 * 1.5, "NT 40": 0.76 * 1.5, "NT 46": 1.42 * 1.5, 
                 "NT 58": 0.94 * 1.5},
               "estandarPruebaEspesor" : 
                {"NT 11": 0.9, "NT 12": 0.9, "NT 13": 1.0, "NT 15": 1.1, 
                 "NT 17": 1.2, "NT 18": 1.4, "NT 21": 1.4, "NT 23": 1.4, 
                 "NT 30": 1.8, "NT 35": 2.0, "NT 40": 2.7, "NT 46": 3.0, 
                 "NT 58": 3.4},
               "toleranciaPruebaEspesor" : 
                {"NT 11": 0.0, "NT 12": 0.0, "NT 13": 0.0, "NT 15": 0.0, 
                 "NT 17": 0.0, "NT 18": 0.0, "NT 21": 0.0, "NT 23": 0.0, 
                 "NT 30": 0.0, "NT 35": 0.0, "NT 40": 0.0, "NT 46": 0.0, 
                 "NT 58": 0.0},
               "toleranciaPruebaEspesorSup" : 
                {"NT 11": 0.0, "NT 12": 0.0, "NT 13": 0.0, "NT 15": 0.0, 
                 "NT 17": 0.0, "NT 18": 0.0, "NT 21": 0.0, "NT 23": 0.0, 
                 "NT 30": 0.0, "NT 35": 0.0, "NT 40": 0.0, "NT 46": 0.0, 
                 "NT 58": 0.0},
               "estandarPruebaPermeabilidad" : 
                {"NT 11": 64.00, "NT 12": 75.78, "NT 13": 61.40, 
                 "NT 15": 60.80, "NT 17": 56.10, "NT 18": 56.00, 
                 "NT 21": 44.62, "NT 23": 31.20, "NT 30": 32.10, 
                 "NT 35": 33.66, "NT 40": 26.72, "NT 46": 20.14, 
                 "NT 58": 18.96},
               "toleranciaPruebaPermeabilidad" : 
                {"NT 11": -9.60 * 1.5, "NT 12": -11.37 * 1.5, 
                 "NT 13": -9.21 * 1.5, "NT 15": -9.12 * 1.5, 
                 "NT 17": -8.42 * 1.5, "NT 18": -8.40 * 1.5, 
                 "NT 21": -6.69 * 1.5, "NT 23": -4.68 * 1.5, 
                 "NT 30": -4.81 * 1.5, "NT 35": -5.05 * 1.5, 
                 "NT 40": -4.01 * 1.5, "NT 46": -3.02 * 1.5, 
                 "NT 58": -2.84 * 1.5},
               "toleranciaPruebaPermeabilidadSup" : 
                {"NT 11": -9.60, "NT 12": -11.37, "NT 13": -9.21, 
                 "NT 15": -9.12, "NT 17": -8.42, "NT 18": -8.40, 
                 "NT 21": -6.69, "NT 23": -4.68, "NT 30": -4.81, 
                 "NT 35": -5.05, "NT 40": -4.01, "NT 46": -3.02, 
                 "NT 58": -2.84},
               "estandarPruebaPoros" : 
                {"NT 11": 0.210, "NT 12": 0.198, "NT 13": 0.160, 
                 "NT 15": 0.198, "NT 17": 0.171, "NT 18": 0.134, 
                 "NT 21": 0.098, "NT 23": 0.062, "NT 30": 0.059, 
                 "NT 35": 0.057, "NT 40": 0.056, "NT 46": 0.055, 
                 "NT 58": 0.054},
               "toleranciaPruebaPoros" : 
                {"NT 11": -0.03, "NT 12": -0.03, "NT 13": -0.02, 
                 "NT 15": -0.03, "NT 17": -0.03, "NT 18": -0.02, 
                 "NT 21": -0.02, "NT 23": -0.01, "NT 30": -0.01, 
                 "NT 35": -0.01, "NT 40": -0.01, "NT 46": -0.01, 
                 "NT 58": -0.01},
               "toleranciaPruebaPorosSup" : 
                {"NT 11": 0.03, "NT 12": 0.03, "NT 13": 0.02, "NT 15": 0.03, 
                 "NT 17": 0.03, "NT 18": 0.02, "NT 21": 0.02, "NT 23": 0.01, 
                 "NT 30": 0.01, "NT 35": 0.01, "NT 40": 0.01, "NT 46": 0.01, 
                 "NT 58": 0.01},
               # TODO: NT 155, NT 235 y NT 305 también tienen valores por 
               # defecto para las pruebas anteriores. METER.
               "estandarPruebaPiramidal" : 
                {"NT 155": 0.66, "NT 235": 1.14, "NT 305": 1.38},
               "toleranciaPruebaPiramidal" : 
                {"NT 155": -0.198 * 1.5, 
                 "NT 235": -0.342 * 1.5, 
                 "NT 305": -0.414 * 1.5},
               "toleranciaPruebaPiramidalSup" : 
                {"NT 155": -0.198, "NT 235": -0.342, "NT 305": -0.414},
              }
    return valores

def get_valores_nuevo_marcado():
    """
    Devuelve un diccionario con los valores por defecto del marcado CE.
    """
    valores = {"estandarPruebaGramaje" : 
                {"NT 10": 80, 
                 "NT 11": 90, 
                 "NT 12": 100, 
                 "NT 13": 110, 
                 "NT 14": 115, 
                 "NT 15": 125, 
                 "NT 17": 140, 
                 "NT 175": 150, 
                 "NT 18": 160, 
                 "NT 21": 180, 
                 "NT 23": 200, 
                 "NT 25": 250, 
                 "NT 30": 260, 
                 "NT 35": 300, 
                 "NT 40": 350, 
                 "NT 46": 400, 
                 "NT 58": 500, 
                 "NT 69": 600, 
                 "PP 200": 200}, 
               "toleranciaPruebaGramaje" : 
                {"NT 10": -1.744, 
                 "NT 11": -1.773, 
                 "NT 12": -1.81, 
                 "NT 13": -1.001, 
                 "NT 14": -2.0125, 
                 "NT 15": -2.225, 
                 "NT 17": -2.366, 
                 "NT 175": -2.4, 
                 "NT 18": -2.528, 
                 "NT 21": -2.754, 
                 "NT 23": -3.02, 
                 "NT 25": -3.3, 
                 "NT 30": -3.406, 
                 "NT 35": -3.63, 
                 "NT 40": -3.71, 
                 "NT 46": -3.84, 
                 "NT 58": -4.0, 
                 "NT 69": -4.26, 
                 "PP 200": -3.08},
               "toleranciaPruebaGramajeSup" : 
                {"NT 10": 1.744, 
                 "NT 11": 1.773, 
                 "NT 12": 1.81, 
                 "NT 13": 1.001, 
                 "NT 14": 2.0125, 
                 "NT 15": 2.225, 
                 "NT 17": 2.366, 
                 "NT 175": 2.4, 
                 "NT 18": 2.528, 
                 "NT 21": 2.754, 
                 "NT 23": 3.02, 
                 "NT 25": 3.3, 
                 "NT 30": 3.406, 
                 "NT 35": 3.63, 
                 "NT 40": 3.71, 
                 "NT 46": 3.84, 
                 "NT 58": 4.0, 
                 "NT 69": 4.26, 
                 "PP 200": 3.08}, 
               "estandarPruebaAlargamientoLongitudinal" : 
                {"NT 10": 48.80, 
                 "NT 11": 51.67, 
                 "NT 12": 53.39, 
                 "NT 13": 52.58, 
                 "NT 14": 51.06, 
                 "NT 15": 49.48, 
                 "NT 17": 52.86, 
                 "NT 175": 55.40, 
                 "NT 18": 53.72, 
                 "NT 21": 54.83, 
                 "NT 23": 55.76, 
                 "NT 25": 58.92, 
                 "NT 30": 57.74, 
                 "NT 35": 57.91, 
                 "NT 40": 58.17, 
                 "NT 46": 57.82, 
                 "NT 58": 63.11, 
                 "NT 69": 68.10, 
                 "PP 200": 62.05},
               "toleranciaPruebaAlargamientoLongitudinal" : 
                {"NT 10": -6.89, 
                 "NT 11": -7.32, 
                 "NT 12": -6.07, 
                 "NT 13": -6.69, 
                 "NT 14": -6.90, 
                 "NT 15": -6.41, 
                 "NT 17": -6.44, 
                 "NT 175": -7.32, 
                 "NT 18": -6.63, 
                 "NT 21": -6.64, 
                 "NT 25": -6.53, 
                 "NT 23": -6.99, 
                 "NT 30": -7.05, 
                 "NT 35": -6.65, 
                 "NT 40": -6.96, 
                 "NT 46": -6.72, 
                 "NT 58": -6.48, 
                 "NT 69": -6.63, 
                 "PP 200": -8.45},
               "toleranciaPruebaAlargamientoLongitudinalSup" : 
                {"NT 10": 6.89, 
                 "NT 11": 7.32, 
                 "NT 12": 6.07, 
                 "NT 13": 6.69, 
                 "NT 14": 6.90, 
                 "NT 15": 6.41, 
                 "NT 17": 6.44, 
                 "NT 175": 7.32, 
                 "NT 18": 6.63, 
                 "NT 21": 6.64, 
                 "NT 25": 6.53, 
                 "NT 23": 6.99, 
                 "NT 30": 7.05, 
                 "NT 35": 6.65, 
                 "NT 40": 6.96, 
                 "NT 46": 6.72, 
                 "NT 58": 6.48, 
                 "NT 69": 6.63, 
                 "PP 200": 8.45},
               "estandarPruebaLongitudinal" : 
                {"NT 10": 5.36, 
                 "NT 11": 6.46, 
                 "NT 12": 7.20, 
                 "NT 13": 7.63, 
                 "NT 14": 7.70, 
                 "NT 15": 8.00, 
                 "NT 17": 9.16, 
                 "NT 175": 10.92, 
                 "NT 18": 11.78, 
                 "NT 21": 12.40, 
                 "NT 23": 15.00, 
                 "NT 25": 18.53, 
                 "NT 30": 19.50, 
                 "NT 35": 21.13, 
                 "NT 40": 25.20, 
                 "NT 46": 27.91, 
                 "NT 58": 31.52, 
                 "NT 69": 34.90, 
                 "PP 200": 9.97},
               "toleranciaPruebaLongitudinal" : 
                {"NT 10": -0.25 * 1.5, 
                 "NT 11": -1.24 * 1.5, 
                 "NT 12": -0.78 * 1.5, 
                 "NT 13": -0.71 * 1.5, 
                 "NT 14": -0.80 * 1.5, 
                 "NT 15": -1.19 * 1.5, 
                 "NT 17": -0.66 * 1.5, 
                 "NT 175": -1.13 * 1.5, 
                 "NT 18": -1.27 * 1.5, 
                 "NT 21": -0.86 * 1.5, 
                 "NT 23": -1.50 * 1.5, 
                 "NT 25": -3.27 * 1.5, 
                 "NT 30": -1.46 * 1.5, 
                 "NT 35": -1.33 * 1.5, 
                 "NT 40": -1.66 * 1.5, 
                 "NT 46": -1.17 * 1.5, 
                 "NT 58": -1.72 * 1.5, 
                 "NT 69": -1.82 * 1.5, 
                 "PP 200": -3.02 * 1.5},
               "toleranciaPruebaLongitudinalSup" : 
                {"NT 10": -0.25, 
                 "NT 11": -1.24, 
                 "NT 12": -0.78, 
                 "NT 13": -0.71, 
                 "NT 14": -0.80, 
                 "NT 15": -1.19, 
                 "NT 17": -0.66, 
                 "NT 175": -1.13, 
                 "NT 18": -1.27, 
                 "NT 21": -0.86, 
                 "NT 23": -1.50, 
                 "NT 25": -3.27, 
                 "NT 30": -1.46, 
                 "NT 35": -1.33, 
                 "NT 40": -1.66, 
                 "NT 46": -1.17, 
                 "NT 58": -1.72, 
                 "NT 69": -1.82, 
                 "PP 200": -3.02},
               "estandarPruebaTransversal" : 
                {"NT 10": 5.89, 
                 "NT 11": 6.48, 
                 "NT 12": 7.30, 
                 "NT 13": 9.03, 
                 "NT 14": 9.20, 
                 "NT 15": 10.08, 
                 "NT 17": 10.10, 
                 "NT 175": 11.61, 
                 "NT 18": 12.02, 
                 "NT 21": 12.48, 
                 "NT 23": 15.00, 
                 "NT 25": 17.70, 
                 "NT 30": 19.55, 
                 "NT 35": 24.82, 
                 "NT 40": 25.60, 
                 "NT 46": 31.60, 
                 "NT 58": 36.80, 
                 "NT 69": 43.70, 
                 "PP 200": 13.82},
               "toleranciaPruebaTransversal" : 
                {"NT 10": -0.11 * 1.5, 
                 "NT 11": -1.12 * 1.5, 
                 "NT 12": -0.64 * 1.5, 
                 "NT 13": -1.39 * 1.5, 
                 "NT 14": -0.60 * 1.5, 
                 "NT 15": -1.28 * 1.5, 
                 "NT 17": -0.76 * 1.5, 
                 "NT 175": -1.08 * 1.5, 
                 "NT 18": -1.59 * 1.5, 
                 "NT 21": -1.25 * 1.5, 
                 "NT 23": -1.97 * 1.5, 
                 "NT 25": -3.02 * 1.5, 
                 "NT 30": -3.66 * 1.5, 
                 "NT 35": -3.15 * 1.5,
                 "NT 40": -1.73 * 1.5, 
                 "NT 46": -4.51 * 1.5, 
                 "NT 58": -2.46 * 1.5, 
                 "NT 69": -1.99 * 1.5, 
                 "PP 200": -0.37 * 1.5},
               "toleranciaPruebaTransversalSup" : 
                {"NT 10": -0.11, 
                 "NT 11": -1.12, 
                 "NT 12": -0.64, 
                 "NT 13": -1.39, 
                 "NT 14": -0.60, 
                 "NT 15": -1.28, 
                 "NT 17": -0.76, 
                 "NT 175": -1.08, 
                 "NT 18": -1.59, 
                 "NT 21": -1.25, 
                 "NT 23": -1.97, 
                 "NT 25": -3.02, 
                 "NT 30": -3.66, 
                 "NT 35": -3.15,
                 "NT 40": -1.73, 
                 "NT 46": -4.51, 
                 "NT 58": -2.46, 
                 "NT 69": -1.99, 
                 "PP 200": -0.37}, 
               "estandarPruebaAlargamientoTransversal" : 
                {"NT 10": 61.65, 
                 "NT 11": 56.14, 
                 "NT 12": 59.17, 
                 "NT 13": 58.83, 
                 "NT 14": 57.72, 
                 "NT 15": 55.00, 
                 "NT 17": 61.16, 
                 "NT 175": 61.91, 
                 "NT 18": 58.35, 
                 "NT 21": 60.98, 
                 "NT 23": 60.94, 
                 "NT 25": 61.57, 
                 "NT 30": 63.57, 
                 "NT 35": 60.73, 
                 "NT 40": 63.50, 
                 "NT 46": 61.08, 
                 "NT 58": 64.72, 
                 "NT 69": 73.77, 
                 "PP 200": 68.18},
               "toleranciaPruebaAlargamientoTransversal" : 
                {"NT 10": -6.40, 
                 "NT 11": -6.36, 
                 "NT 12": -6.62, 
                 "NT 13": -6.62, 
                 "NT 14": -6.72, 
                 "NT 15": -6.04, 
                 "NT 17": -6.87, 
                 "NT 175": -7.50, 
                 "NT 18": -6.73, 
                 "NT 21": -6.77, 
                 "NT 23": -6.71, 
                 "NT 25": -6.72, 
                 "NT 30": -7.22, 
                 "NT 35": -7.36, 
                 "NT 40": -7.16, 
                 "NT 46": -6.57, 
                 "NT 58": -7.32, 
                 "NT 69": -6.46, 
                 "PP 200": -8.77},
               "toleranciaPruebaAlargamientoTransversalSup" : 
                {"NT 10": 6.40, 
                 "NT 11": 6.36, 
                 "NT 12": 6.62, 
                 "NT 13": 6.62, 
                 "NT 14": 6.72, 
                 "NT 15": 6.04, 
                 "NT 17": 6.87, 
                 "NT 175": 7.50, 
                 "NT 18": 6.73, 
                 "NT 21": 6.77, 
                 "NT 23": 6.71, 
                 "NT 25": 6.72, 
                 "NT 30": 7.22, 
                 "NT 35": 7.36, 
                 "NT 40": 7.16, 
                 "NT 46": 6.57, 
                 "NT 58": 7.32, 
                 "NT 69": 6.46, 
                 "PP 200": 8.77},
               "estandarPruebaCompresion" : 
                {"NT 10": 1.04, 
                 "NT 11": 1.11, 
                 "NT 12": 1.23, 
                 "NT 13": 1.36, 
                 "NT 14": 1.52, 
                 "NT 15": 1.56, 
                 "NT 17": 1.72, 
                 "NT 175": 1.95, 
                 "NT 18": 1.96, 
                 "NT 21": 2.26, 
                 "NT 23": 2.57, 
                 "NT 25": 3.02, 
                 "NT 30": 3.31, 
                 "NT 35": 3.93, 
                 "NT 40": 4.49, 
                 "NT 46": 5.26, 
                 "NT 58": 6.49, 
                 "NT 69": 6.91, 
                 "PP 200": 2.13},
               "toleranciaPruebaCompresion" : 
                {"NT 10": -0.02 * 1.5, 
                 "NT 11": -0.05 * 1.5, 
                 "NT 12": -0.09 * 1.5, 
                 "NT 13": -0.17 * 1.5, 
                 "NT 14": -0.12 * 1.5, 
                 "NT 15": -0.15 * 1.5, 
                 "NT 17": -0.11 * 1.5, 
                 "NT 175": -0.20 * 1.5, 
                 "NT 18": -0.12 * 1.5, 
                 "NT 21": -0.11 * 1.5, 
                 "NT 23": -0.05 * 1.5, 
                 "NT 25": -0.13 * 1.5, 
                 "NT 30": -0.11 * 1.5, 
                 "NT 35": -0.30 * 1.5, 
                 "NT 40": -0.36 * 1.5, 
                 "NT 46": -0.60 * 1.5, 
                 "NT 58": -0.43 * 1.5, 
                 "NT 69": -0.53 * 1.5, 
                 "PP 200": -0.14 * 1.5},
               "toleranciaPruebaCompresionSup" : 
                {"NT 10": -0.02, 
                 "NT 11": -0.05, 
                 "NT 12": -0.09, 
                 "NT 13": -0.17, 
                 "NT 14": -0.12, 
                 "NT 15": -0.15, 
                 "NT 17": -0.11, 
                 "NT 175": 0.20, 
                 "NT 18": -0.12, 
                 "NT 21": -0.11, 
                 "NT 23": -0.05, 
                 "NT 25": -0.13, 
                 "NT 30": -0.11, 
                 "NT 35": -0.30, 
                 "NT 40": -0.36, 
                 "NT 46": -0.60, 
                 "NT 58": -0.43, 
                 "NT 69": -0.53, 
                 "PP 200": -0.14},
               "estandarPruebaPerforacion" : 
                {"NT 10": 35.40, 
                 "NT 11": 33.07, 
                 "NT 12": 28.80, 
                 "NT 13": 31.00, 
                 "NT 14": 28.72, 
                 "NT 15": 23.90, 
                 "NT 17": 22.27, 
                 "NT 175": 21.10, 
                 "NT 18": 19.20, 
                 "NT 21": 17.47, 
                 "NT 23": 15.73, 
                 "NT 25": 13.05, 
                 "NT 30": 11.80, 
                 "NT 35": 9.80, 
                 "NT 40": 7.87, 
                 "NT 46": 6.40, 
                 "NT 58": 6.20, 
                 "NT 69": 5.50, 
                 "PP 200": 6.40},
               "toleranciaPruebaPerforacion" : 
                {"NT 10": 1.41, 
                 "NT 11": 1.90, 
                 "NT 12": 2.58, 
                 "NT 13": 1.30, 
                 "NT 14": 1.86, 
                 "NT 15": 2.48, 
                 "NT 17": 1.35, 
                 "NT 175": 2.00, 
                 "NT 18": 2.57, 
                 "NT 21": 0.37, 
                 "NT 23": 0.94, 
                 "NT 25": 0.21, 
                 "NT 30": 1.12, 
                 "NT 35": 0.99, 
                 "NT 40": 0.76, 
                 "NT 46": 1.42, 
                 "NT 58": 0.94, 
                 "NT 69": 0.42, 
                 "PP 200": 3.74},
               "toleranciaPruebaPerforacionSup" : 
                {"NT 10": 1.41 * 1.5, 
                 "NT 11": 1.90 * 1.5, 
                 "NT 12": 2.58 * 1.5, 
                 "NT 13": 1.30 * 1.5, 
                 "NT 14": 1.86 * 1.5, 
                 "NT 15": 2.48 * 1.5, 
                 "NT 17": 1.35 * 1.5, 
                 "NT 175": 2.00 * 1.5, 
                 "NT 18": 2.57 * 1.5, 
                 "NT 21": 0.37 * 1.5, 
                 "NT 23": 0.94 * 1.5, 
                 "NT 25": 0.21 * 1.5, 
                 "NT 30": 1.12 * 1.5, 
                 "NT 35": 0.99 * 1.5, 
                 "NT 40": 0.76 * 1.5, 
                 "NT 46": 1.42 * 1.5, 
                 "NT 58": 0.94 * 1.5, 
                 "NT 69": 0.42 * 1.5, 
                 "PP 200": 3.74 * 1.5},
               "estandarPruebaEspesor" : 
                {"NT 10": 0.9, 
                 "NT 11": 1.05, 
                 "NT 12": 1.11, 
                 "NT 13": 1.16, 
                 "NT 14": 1.17, 
                 "NT 15": 1.26, 
                 "NT 17": 1.39, 
                 "NT 175": 1.48, 
                 "NT 18": 1.51, 
                 "NT 21": 1.63, 
                 "NT 23": 1.74, 
                 "NT 25": 2.20, 
                 "NT 30": 2.21, 
                 "NT 35": 2.40, 
                 "NT 40": 2.73, 
                 "NT 46": 3.06, 
                 "NT 58": 3.98, 
                 "NT 69": 4.93, 
                 "PP 200": 3.00},
               "toleranciaPruebaEspesor" : 
                {"NT 10": -36.7, 
                 "NT 11": -23.8, 
                 "NT 12": -21.6, 
                 "NT 13": -21.6, 
                 "NT 14": -21.4, 
                 "NT 15": -21.4, 
                 "NT 17": -19.4, 
                 "NT 175": -21.6, 
                 "NT 18": -17.9, 
                 "NT 21": -19.6, 
                 "NT 23": -19.5, 
                 "NT 25": -17.3, 
                 "NT 30": -16.3, 
                 "NT 35": -14.2, 
                 "NT 40": -13.9, 
                 "NT 46": -11.8, 
                 "NT 58": -10.6, 
                 "NT 69": -11.2, 
                 "PP 200": -18.7},
               "toleranciaPruebaEspesorSup" : 
                {"NT 10": 36.7, 
                 "NT 11": 23.8, 
                 "NT 12": 21.6, 
                 "NT 13": 21.6, 
                 "NT 14": 21.4, 
                 "NT 15": 21.4, 
                 "NT 17": 19.4, 
                 "NT 175": 21.6, 
                 "NT 18": 17.9, 
                 "NT 21": 19.6, 
                 "NT 23": 19.5, 
                 "NT 25": 17.3, 
                 "NT 30": 16.3, 
                 "NT 35": 14.2, 
                 "NT 40": 13.9, 
                 "NT 46": 11.8, 
                 "NT 58": 10.6, 
                 "NT 69": 11.2, 
                 "PP 200": 18.7},
               "estandarPruebaPermeabilidad" : 
                {"NT 10": 71.20, 
                 "NT 11": 64.00, 
                 "NT 12": 63.78, 
                 "NT 13": 61.40, 
                 "NT 14": 61.00, 
                 "NT 15": 60.80, 
                 "NT 17": 56.10, 
                 "NT 175": 56.05, 
                 "NT 18": 56.00, 
                 "NT 21": 44.62, 
                 "NT 23": 31.20, 
                 "NT 25": 31.15, 
                 "NT 30": 31.05, 
                 "NT 35": 30.95, 
                 "NT 40": 26.72, 
                 "NT 46": 20.14, 
                 "NT 58": 18.96, 
                 "NT 69": 17.50, 
                 "PP 200": 90.10},
               "toleranciaPruebaPermeabilidad" : 
                {"NT 10": -9.80 * 1.5, 
                 "NT 11": -9.60 * 1.5, 
                 "NT 12": -9.43 * 1.5, 
                 "NT 13": -9.21 * 1.5, 
                 "NT 14": -9.09 * 1.5, 
                 "NT 15": -9.12 * 1.5, 
                 "NT 17": -8.42 * 1.5, 
                 "NT 175": -8.00 * 1.5, 
                 "NT 18": -8.40 * 1.5, 
                 "NT 21": -6.69 * 1.5, 
                 "NT 23": -4.68 * 1.5, 
                 "NT 25": -4.61 * 1.5, 
                 "NT 30": -4.81 * 1.5, 
                 "NT 35": -5.05 * 1.5, 
                 "NT 40": -4.01 * 1.5, 
                 "NT 46": -3.02 * 1.5, 
                 "NT 58": -2.84 * 1.5, 
                 "NT 69": -2.77 * 1.5, 
                 "PP 200": -9.12 * 1.5},
               "toleranciaPruebaPermeabilidadSup" : 
                {"NT 10": -9.80, 
                 "NT 11": -9.60, 
                 "NT 12": -9.43, 
                 "NT 13": -9.21, 
                 "NT 14": -9.09, 
                 "NT 15": -9.12, 
                 "NT 17": -8.42, 
                 "NT 175": -8.00, 
                 "NT 18": -8.40, 
                 "NT 21": -6.69, 
                 "NT 23": -4.68, 
                 "NT 25": -4.61, 
                 "NT 30": -4.81, 
                 "NT 35": -5.05, 
                 "NT 40": -4.01, 
                 "NT 46": -3.02, 
                 "NT 58": -2.84, 
                 "NT 69": -2.77, 
                 "PP 200": -9.12},
               "estandarPruebaPoros" : 
                {"NT 10": 0.220, 
                 "NT 11": 0.210, 
                 "NT 12": 0.198, 
                 "NT 13": 0.180, 
                 "NT 14": 0.175, 
                 "NT 15": 0.175, 
                 "NT 17": 0.171, 
                 "NT 175": 0.157, 
                 "NT 18": 0.134, 
                 "NT 21": 0.098, 
                 "NT 23": 0.062, 
                 "NT 25": 0.061, 
                 "NT 30": 0.059, 
                 "NT 35": 0.057, 
                 "NT 40": 0.056, 
                 "NT 46": 0.055, 
                 "NT 58": 0.054, 
                 "NT 69": 0.051, 
                 "PP 200": 0.290},
               "toleranciaPruebaPoros" : 
                {"NT 10": -0.03, 
                 "NT 11": -0.03, 
                 "NT 12": -0.03, 
                 "NT 13": -0.03, 
                 "NT 14": -0.03, 
                 "NT 15": -0.03, 
                 "NT 17": -0.03, 
                 "NT 175": -0.03, 
                 "NT 18": -0.02, 
                 "NT 21": -0.02, 
                 "NT 23": -0.01, 
                 "NT 25": -0.01, 
                 "NT 30": -0.01, 
                 "NT 35": -0.01, 
                 "NT 40": -0.01, 
                 "NT 46": -0.01, 
                 "NT 58": -0.01, 
                 "NT 69": -0.01, 
                 "PP 200": -0.03},
               "toleranciaPruebaPorosSup" : 
                {"NT 10": 0.03, 
                 "NT 11": 0.03, 
                 "NT 12": 0.03, 
                 "NT 13": 0.03, 
                 "NT 14": 0.03, 
                 "NT 15": 0.03, 
                 "NT 17": 0.03, 
                 "NT 175": 0.03, 
                 "NT 18": 0.02, 
                 "NT 21": 0.02, 
                 "NT 23": 0.01, 
                 "NT 25": 0.01, 
                 "NT 30": 0.01, 
                 "NT 35": 0.01, 
                 "NT 40": 0.01, 
                 "NT 46": 0.01, 
                 "NT 58": 0.01, 
                 "NT 69": 0.01, 
                 "PP 200": 0.03}, 
               # TODO: NT 155, NT 235 y NT 305 también tienen valores por 
               # defecto para las pruebas anteriores. METER.
               "estandarPruebaPiramidal" : 
                {"NT 155": 0.66, "NT 235": 1.14, "NT 305": 1.38},
               "toleranciaPruebaPiramidal" : 
                {"NT 155": -0.198 * 1.5, 
                 "NT 235": -0.342 * 1.5, 
                 "NT 305": -0.414 * 1.5},
               "toleranciaPruebaPiramidalSup" : 
                {"NT 155": -0.198, "NT 235": -0.342, "NT 305": -0.414}
              }
    return valores

def insertar_valores_defecto_marcado():
    """
    Inserta en la BD, para cada producto, los valores del marcado CE 
    por defecto.
    """
    valores = get_valores_defecto_marcado()
    for cer in pclases.CamposEspecificosRollo.select():
        producto = cer.productosVenta[0]
        for campo in valores:
            for nt in valores[campo]:
                if "%s " % (nt) in producto.descripcion:
                    print producto.descripcion, campo, valores[campo][nt]
                    setattr(cer, campo, valores[campo][nt]) 

def insertar_nuevos_valores_marcado():
    """
    Inserta en la BD, para cada producto, una nueva ficha de marcado CE.
    OJO: ¡Ejecutar solo una vez!
    """
    valores = get_valores_nuevo_marcado()
    for cer in pclases.CamposEspecificosRollo.select():
        try:
            producto = cer.productosVenta[0]
        except IndexError:
            cer.destroy(ventana = __file__)
            continue
        for campo in valores:
            for nt in valores[campo]:
                if "%s " % (nt) in producto.descripcion:
                    try:
                        marcado = cer.marcadosCe[0]
                    except IndexError:
                        marcado = pclases.MarcadoCe(
                            fechaInicio = mx.DateTime.DateTimeFrom(day = 20, 
                                                                   month = 5, 
                                                                   year = 2008),
                            fechaFin = None, 
                            camposEspecificosRollo = cer)
                    print producto.descripcion, campo, valores[campo][nt]
                    setattr(marcado, campo, valores[campo][nt]) 

################################################################################


if __name__ == "__main__":
    p = ProductosDeVentaRollos()

