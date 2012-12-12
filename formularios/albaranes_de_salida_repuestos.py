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
## albaranes_salida_repuestos.py - Albaranes internos de gasto de repuestos.
###################################################################
## 
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sqlobject
import sys, os
try:
    import pclases
except ImportError:
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    import pclases
try:
    import geninformes
except ImportError:
    sys.path.append('../informes')
    import geninformes
from utils import ffloat, _float as float
import mx, mx.DateTime

class AlbaranesDeSalidaRepuestos(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self.modificado = False # Para detectar si el albarán en pantalla se ha modificado
                                # en la sesión actual. 
        self.nuevo = False      # Para detectar si un albarán es nuevo.
        Ventana.__init__(self, 'albaranes_de_salida_repuestos.glade', objeto, usuario = self.usuario)
        connections = {'b_salir/clicked': self.pre_salir,
                       'b_fecha/clicked': self.buscar_fecha,
                       'b_drop_ldv/clicked': self.drop_ldv,
                       'b_add_producto/clicked': self.add_producto,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_borrar/clicked': self.borrar_albaran,
                       'b_nuevo/clicked': self.crear_nuevo_albaran,
                       'b_buscar/clicked': self.buscar_albaran,
                       # 'b_imprimir/clicked': self.imprimir,
                       'cbe_almacen/changed': self.guardar
                      }
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        gtk.main()

    def es_diferente(self):
        """
        Devuelve True si la información en pantalla es distinta a la
        del objeto en memoria.
        """
        albaran = self.objeto
        if albaran == None: return False    # Si no hay albaran activo, 
                    # devuelvo que no hay cambio respecto a la ventana. 
        condicion = albaran.numalbaran == self.wids['e_numalbaran'].get_text()
        condicion = condicion and (utils.str_fecha(albaran.fecha) == self.wids['e_fecha'].get_text())
        condicion = condicion and self.wids['ch_bloqueado'].get_active() == albaran.bloqueado
        condicion = condicion and (
            utils.combo_get_value(self.wids['cbe_almacen']) 
                == self.objeto.almacenOrigenID)
        return not condicion    # "condicion" verifica que sea igual

    def aviso_actualizacion(self):
        """
        Muestra una ventana modal con el mensaje de objeto 
        actualizado.
        """
        utils.dialogo_info('ACTUALIZAR',
                           'El albarán ha sido modificado remotamente.\nDebe actualizar la información mostrada en pantalla.\nPulse el botón «Actualizar»')
        self.wids['b_actualizar'].set_sensitive(True)

    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        # Inicialmente no se muestra NADA. Sólo se le deja al
        # usuario la opción de buscar o crear nuevo.
        self.wids['b_actualizar'].set_sensitive(False)
        self.wids['b_guardar'].set_sensitive(False)
        self.wids['b_nuevo'].set_sensitive(True)
        self.wids['b_buscar'].set_sensitive(True)
        self.activar_widgets(False)
        # Inicialización del resto de widgets:
        cols = (('Código', 'gobject.TYPE_STRING', False, True, False, None),
                ('Descripción', 'gobject.TYPE_STRING', False, True, True, None),
                ('Cantidad', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_cantidad_ldv),
                ('IDLDV', 'gobject.TYPE_INT64', False, False, False, None)
               )
        utils.preparar_treeview(self.wids['tv_ldvs'], cols)
        self.wids['tv_ldvs'].get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        almacenes = [(a.id, a.nombre) 
                     for a in pclases.Almacen.select(
                         pclases.Almacen.q.activo == True, 
                         orderBy = "id")]
        utils.rellenar_lista(self.wids['cbe_almacen'], 
                             almacenes)

    def activar_widgets(self, s):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        if self.objeto and self.objeto.bloqueado and self.usuario and self.usuario.nivel >= 2:
            s = False
        ws = ('b_add_producto', 'b_drop_ldv', 'b_borrar', 'e_numalbaran', 
              'ch_bloqueado', 'b_fecha', 'tv_ldvs', 'e_fecha', "cbe_almacen") 
        for w in ws:
            try:
                self.wids[w].set_sensitive(s)
            except:
                print "Borra %s de la lista" % w
        if self.objeto:
            self.wids['cbe_almacen'].set_sensitive(
                not len(self.objeto.lineasDeVenta))

    def ir_a_primero(self):
        """
        Hace que el primer registro -si lo hay- de la tabla implicada
        en el objeto del formulario sea el objeto activo.
        """
        albaran = self.objeto
        try:
            # Anulo el aviso de actualización del envío que deja de ser activo.
            if albaran != None: albaran.notificador.desactivar()
            albaranes = pclases.AlbaranSalida.select(
                pclases.AlbaranSalida.q.observaciones.contains("repuesto"), 
                orderBy = '-id')
                # Selecciono todos los albaranes de venta de repuestos y me 
                # quedo con el primero de la lista.
            try:
                albaran = [a for a in albaranes if a.es_de_repuestos()][0]
            except IndexError:
                albaran = None
            else:
                self.modificado = False
                self.nuevo = False
                # Activo la notificación:
                albaran.notificador.activar(self.aviso_actualizacion) 
        except Exception, msg:
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
                              r.fecha and r.fecha.strftime('%d/%m/%Y') or '', 
                              r.clienteID and r.cliente.nombre or ""))
        idalbaran = utils.dialogo_resultado(filas_res,
                                            titulo = 'Seleccione albarán',
                                            cabeceras = ('ID', 
                                                         'Número de albarán', 
                                                         'Fecha', 
                                                         'Cliente'), 
                                            padre = self.wids['ventana']) 
        if idalbaran < 0:
            return None
        else:
            return idalbaran

    def rellenar_ldvs(self):
        model = self.wids['tv_ldvs'].get_model()
        model.clear()
        for ldv in self.objeto.lineasDeVenta:
            cantidad = ldv.cantidad 
            iterpadre = model.append(None, (ldv.producto.codigo, 
                                            ldv.producto.descripcion, 
                                            utils.float2str(cantidad),
                                            ldv.id))
 
    def rellenar_widgets(self):
        """
        Introduce la información del albaran actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        self.wids['b_guardar'].set_sensitive(False) 
            # Deshabilito el guardar antes de actualizar para 
            # evitar "falsos positivos".
        albaran = self.objeto
        if albaran == None: 
            return
        self.wids['e_numalbaran'].set_text(albaran.numalbaran)
        self.wids['e_fecha'].set_text(utils.str_fecha(albaran.fecha))
        self.wids['ch_bloqueado'].set_active(self.objeto.bloqueado)
        self.suspender(self.wids['cbe_almacen'])
        utils.combo_set_from_db(self.wids['cbe_almacen'], 
                                self.objeto.almacenOrigenID, 
                                forced_value = self.objeto.almacenOrigen 
                                    and self.objeto.almacenOrigen.nombre 
                                    or None)
        self.revivir(self.wids['cbe_almacen'])
        self.rellenar_ldvs()
        self.wids['b_guardar'].set_sensitive(False) 
            # Deshabilito el guardar antes de actualizar para 
            # evitar "falsos positivos".
        self.objeto.make_swap()

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
        nuevo_numalbaran = \
            pclases.AlbaranSalida.get_siguiente_numero_numalbaran_str()
            # Datos a pedir:
        numalbaran = utils.dialogo_entrada(
                        titulo = "NÚMERO DE ALBARÁN", 
                        texto = 'Introduzca un número para el albarán.\nDeje'
                                ' el número de albarán por defecto si no est'
                                'á seguro.', 
                        valor_por_defecto = nuevo_numalbaran, 
                        padre = self.wids['ventana'])
        if numalbaran == None: 
            return
        # numero_numalbaran = utils.parse_numero(numalbaran)
        numero_numalbaran_usuario = utils.parse_numero(numalbaran, invertir = True)
        numero_numalbaran_sugerido = utils.parse_numero(nuevo_numalbaran, invertir = True)
        #if self.usuario != None and self.usuario.nivel > 1 and numero_numalbaran != None and numero_numalbaran > nuevo_numalbaran:
        if (self.usuario 
            and self.usuario.nivel > 1 
            and numero_numalbaran_usuario != None 
            and numero_numalbaran_usuario > numero_numalbaran_sugerido):
            utils.dialogo_info(titulo = "NÚMERO DE ALBARÁN INCORRECTO", 
                               texto = "No es estrictamente necesario que todos los albaranes sean consecutivos.\n\nSin embargo, no se aconseja crear albaranes con número superior al sugerido.\n\nSi considera que debe hacerlo, contacte con un usuario con mayor nivel de privilegios.", 
                               padre = self.wids['ventana'])
            return
        if albaran != None: albaran.notificador.desactivar()
        propia_empresa = Cliente.id_propia_empresa_cliente()
        almacenes = [(a.id, a.nombre) 
                     for a in pclases.Almacen.select(
                         pclases.Almacen.q.activo == True, 
                         orderBy = "id")]
        almacenppal = pclases.Almacen.get_almacen_principal_id_or_none()
        almo = utils.dialogo_combo(titulo = "ALMACÉN ORIGEN", 
                    texto = "Seleccione el almacén origen de la mercancía",  
                    ops = almacenes, 
                    padre = self.wids['ventana'], 
                    valor_por_defecto = almacenppal)
        if not almo:    # Cancelar
            return
        try:
            albaran = pclases.AlbaranSalida(numalbaran = numalbaran,
                                    transportista = None,
                                    clienteID = propia_empresa, 
                                    bloqueado = False, 
                                    facturable = False, 
                                    motivo = "Es de consumo de repuestos", 
                                    observaciones = "repuestos", 
                                    destino = None, 
                                    fecha = mx.DateTime.localtime(), 
                                    almacenOrigenID = almo, 
                                    almacenDestino = None)
            pclases.Auditoria.nuevo(albaran, self.usuario, __file__)
            utils.dialogo_info('ALBARÁN CREADO', 
                               'El albarán %s ha sido creado.\nNo olvide asociar las salidas.' % albaran.numalbaran, 
                               padre = self.wids['ventana'])
            self.nuevo = True
            self.modificado = False
        except Exception, e:
            texto = "%salbaranes_de_salida::crear_nuevo_albaran -> Error al crear nuevo albarán. Excepción capturada: %s" % (self.usuario and self.usuario.usuario+": " or "", e)
            print texto
            self.logger.error(texto)
            utils.dialogo_info('ERROR: ALBARÁN NO CREADO', 
                               'El albarán %s no ha sido creado.\nCompruebe que el número no esté siendo usado y vuelva a intentarlo.\n\n\n' % (numalbaran), 
                               padre = self.wids['ventana']) 
        albaran.notificador.activar(self.aviso_actualizacion)
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
        a_buscar=utils.dialogo_entrada(titulo = "BUSCAR ALBARÁN", 
                                       texto = "Introduzca número de albarán:",
                                       padre = self.wids['ventana'])
        if a_buscar != None:
            resultados = pclases.AlbaranSalida.select(pclases.AND(
                pclases.AlbaranSalida.q.numalbaran.contains(a_buscar), 
                pclases.AlbaranSalida.q.observaciones.contains("repuestos")))
            if resultados.count() > 1:
                ## Refinar los resultados
                idalbaran = self.refinar_resultados_busqueda(resultados)
                if idalbaran == None:
                    return
                resultados = [pclases.AlbaranSalida.get(idalbaran)]
            elif resultados.count() < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info('SIN RESULTADOS', 'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.\n(Atención: Ver la lista completa puede resultar lento si el número de elementos es muy alto)', padre = self.wids['ventana'])
                return
            ## Un único resultado
            # Primero anulo la función de actualización
            if albaran != None:
                albaran.notificador.desactivar()
            # Pongo el objeto como actual
            albaran = resultados[0]
            self.nuevo = False
            self.modificado = False
            # Y activo la función de notificación:
            albaran.notificador.activar(self.aviso_actualizacion)
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
        albaran.notificador.desactivar()
        # Actualizo los datos del objeto
        albaran.numalbaran = numalbaran
        albaran.bloqueado = self.wids['ch_bloqueado'].get_active()
        try:
            albaran.fecha = utils.parse_fecha(fecha)
        except:
            albaran.fecha = time.localtime()
        albaran.almacenOrigenID=utils.combo_get_value(self.wids['cbe_almacen'])
        # Fuerzo la actualización de la BD y no espero a que SQLObject lo 
        # haga por mí:
        albaran.sync()
        # Vuelvo a activar el notificador
        albaran.notificador.activar(self.aviso_actualizacion)
        self.objeto = albaran
        self.modificado = True
        self.actualizar_ventana()
        self.wids['b_guardar'].set_sensitive(False)

    def buscar_fecha(self, boton):
        self.wids['e_fecha'].set_text(utils.str_fecha(utils.mostrar_calendario(fecha_defecto = self.objeto and self.objeto.fecha or None, padre = self.wids['ventana'])))

    def add_producto(self, boton):
        """
        OJO: Los repuestos deben tener como tipo de material uno que tenga en 
        su descripción "aceite", "lubricante" o "repuesto".
        """
        tipos = pclases.TipoDeMaterial.select(pclases.OR(
            pclases.TipoDeMaterial.q.descripcion.contains("repuesto"), 
            pclases.TipoDeMaterial.q.descripcion.contains("aceite"), 
            pclases.TipoDeMaterial.q.descripcion.contains("lubricante")))
        if tipos.count() == 0:
            utils.dialogo_info(titulo = "SIN DATOS", 
                               texto = "No hay repuestos dados de alta en los"
                                       " tipos de material.", 
                               padre = self.wids['ventana'])
        else:
            tipos = [(t.id, t.descripcion) for t in tipos]
            idtipo = utils.dialogo_combo(titulo = "SELECCIONE TIPO", 
                                    texto = "Seleccione un tipo de material", 
                                    padre = self.wids['ventana'], 
                                    ops = tipos)
            if idtipo != None:
                prods = pclases.ProductoCompra.select(pclases.AND(
                    pclases.ProductoCompra.q.tipoDeMaterialID == idtipo, 
                    pclases.ProductoCompra.q.obsoleto == False))
                if prods.count() == 0:
                    utils.dialogo_info(titulo = "SIN DATOS", 
                        texto = "No hay repuestos dados de alta con el tipo "
                                "de material «%s»." % (
                            pclases.TipoDeMaterial.get(idtipo).descripcion), 
                        padre = self.wids['ventana'])
                else:
                    prods = [(p.id, p.descripcion) for p in prods]
                    idprod = utils.dialogo_combo(
                                        titulo = "SELECCIONE PRODUCTO", 
                                        texto = "Seleccione un respuesto:", 
                                        padre = self.wids['ventana'], 
                                        ops = prods)
                    if idprod != None:
                        prod = pclases.ProductoCompra.get(idprod)
                        ldv = pclases.LineaDeVenta(facturaVenta = None, 
                                                   pedidoVenta = None, 
                                                   albaranSalida=self.objeto, 
                                                   productoVenta = None, 
                                                   productoCompra = prod, 
                                                   cantidad = 0)
                        pclases.Auditoria.nuevo(ldv, self.usuario, __file__)
                        self.actualizar_ventana()

    def cambiar_cantidad_ldv(self, cell, path, text):
        try:
            nueva = utils._float(text)
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", 
                               texto = "El texto %s no es un número." % text, 
                               padre = self.wids['ventana'])
        else:
            model = self.wids['tv_ldvs'].get_model()
            idldv = model[path][-1]
            ldv = pclases.LineaDeVenta.get(idldv)
            vieja = ldv.cantidad
            diferencia = nueva - vieja
            producto = ldv.productoCompra
            producto.sync()
            #bak = producto.existencias
            #producto.existencias -= diferencia
            if (producto.get_existencias(self.objeto.almacenOrigen) 
                    - diferencia) < 0:
                utils.dialogo_info(titulo = "ERROR EXISTENCIAS", 
                                   texto = "No hay existencias suficientes.", 
                                   padre = self.wids['ventana'])
                #producto.existencias = bak
            else:
                producto.add_existencias(-diferencia, 
                                         self.objeto.almacenOrigen, 
                                         actualizar_global = True)
                #producto.syncUpdate()
                ldv.cantidad = nueva
                ldv.syncUpdate()
                model[path][2] = utils.float2str(ldv.cantidad)

    def drop_ldv(self, boton):
        """
        Pone a None el idalbaran de la 
        línea de venta seleccionada y 
        a False la confirmación (aumentando
        la cantidad del artículo).
        """
        if (self.wids['tv_ldvs'].get_selection().count_selected_rows() and
           utils.dialogo(titulo = "¿BORRAR LÍNEA?", 
                         texto = "¿Está seguro de borra las líneas seleccion"
                                 "adas?\n\nHacerlo cancelará el gasto de rep"
                                 "uestos, así como otras operaciones que pud"
                                 "ieran estar relacionadas con el mismo.", 
                         padre = self.wids['ventana'])):
            model, paths = self.wids['tv_ldvs'].get_selection().get_selected_rows()
            for path in paths:
                iter = model.get_iter(path)
                if model[iter].parent == None:  # Es una LDV
                    idldv = model[iter][-1]
                    try:
                        ldv = pclases.LineaDeVenta.get(idldv)
                    except pclases.SQLObjectNotFound:   # Ya se ha borrado.
                        pass
                    else:
                        self.desvincular_ldv_del_albaran(ldv)
                self.modificado = True
            self.actualizar_ventana()
    
    def desvincular_ldv_del_albaran(self, ldv):
        """ Elimina si no tiene relaciones y aumenta existencias."""
        producto = ldv.productoCompra
        #producto.sync()
        #producto.existencias += ldv.cantidad
        #producto.syncUpdate()
        producto.add_existencias(ldv.cantidad, self.objeto.almacenOrigen, 
                                 actualizar_global = True)
        ldv.destroy_en_cascada()

    def borrar_albaran(self, boton):
        """
        Elimina el albarán de la BD y anula la relación entre
        él y sus LDVs.
        """
        if not utils.dialogo('Se eliminará el albarán actual.\n¿Está seguro?', 'BORRAR ALBARÁN'): return
        albaran = self.objeto
        albaran.notificador.desactivar()
        for ldv in albaran.lineasDeVenta:
            self.desvincular_ldv_del_albaran(ldv)
        try:
            albaran.destroy(ventana = __file__)
        except:
            utils.dialogo_info('ERROR', 'No se pudo eliminar.\nIntente eliminar primero los productos, servicios, transportes y comisiones del albarán.', padre = self.wids['ventana'])
            return
        self.ir_a_primero()

    def pre_salir(self, w):
        """
        Bueno, se ejecuta antes de salir de la ventana, ¿qué nombre esperabas?
        """
        self.salir(w)


if __name__=='__main__':
    try:
        a = AlbaranesDeSalida(usuario = pclases.Usuario.select(pclases.Usuario.q.usuario.contains("rafa"))[0])
    except:
        a = AlbaranesDeSalidaRepuestos()
    #a = AlbaranesDeSalida()

