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
## usuarios.py - Panel de control de usuarios y módulos. 
###################################################################
## NOTAS:
## Si una ventana no pertenece a ningún módulo no aparecerá en los
## permisos ni en el menú. A efectos prácticos, no existirá para 
## los usuarios aunque esté en la BD y tenga relación con alguno 
## a través de la tabla "permisos".
## Ver cómo hago lo de actualizar el treeview en los permisos, 
## porque haciéndolo así no hay que destruir el model y volver a 
## llenarlo, con lo que tampoco se redibuja el treeview entero, no
## se cierran las ramas expandidas, etc.  
## ----------------------------------------------------------------
##  
###################################################################
## Changelog:
## 27 de abril de 2006 -> Inicio.
## 
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import sys, os 
from framework import pclases
import gtk, gtk.glade, time
import mx.DateTime
import gobject
try:
    from hashlib import md5
except ImportError:
    import md5 

class Usuarios(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'usuarios.glade', objeto, usuario=self.usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_actualizar/clicked': self.actualizar_ventana, 
                       'b_guardar/clicked': self.guardar, 
                       'b_nuevo/clicked': self.crear_nuevo_usuario, 
                       'b_borrar/clicked': self.borrar_usuario, 
                       'b_buscar/clicked': self.buscar_usuario,
                       'b_enviar/clicked': self.enviar_mensaje,
                       'b_passw/clicked': self.nueva_contrasenna,
                       'b_drop/clicked': self.borrar_mensaje,
                       'b_modulo_clean/clicked': self.limpiar_modulo,
                       'b_ventana_clean/clicked': self.limpiar_ventana,
                       'b_add_vm/clicked': self.add_ventana_a_modulo,
                       'b_add_modulo/clicked': self.add_modulo,
                       'b_drop_modulo/clicked': self.drop_modulo,
                       'b_add_ventana/clicked': self.add_ventana,
                       'b_drop_ventana/clicked': self.drop_ventana
                      }
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        # self.wids['ventana'].maximize()
        self.wids['ventana'].resize(800, 600)
        self.rellenar_tab_modulos()     # Esto siempre debe hacerse al menos 1 vez aunque no haya usuarios.
        gtk.main()

    # --------------- Funciones auxiliares ------------------------------
    def es_diferente(self):
        """
        Devuelve True si la información en pantalla es distinta a la
        del objeto en memoria.
        """
        usuario = self.objeto
        if usuario == None: return False    # Si no hay usuario activo, 
                    # devuelvo que no hay cambio respecto a la ventana.
        condicion = usuario.usuario == self.wids['e_user'].get_text()
        if not condicion and pclases.DEBUG:
            print "usuaruos.py::es_diferente", "e_user"
        condicion = (condicion and 
                     (usuario.nombre == self.wids['e_nombre'].get_text()))
        if not condicion and pclases.DEBUG:
            print "usuaruos.py::es_diferente", "e_nombre"
        condicion = (condicion and 
                     self.wids['e_cuenta'].get_text() == usuario.cuenta)
        if not condicion and pclases.DEBUG:
            print "usuaruos.py::es_diferente", "e_cuenta"
        condicion = (condicion and 
                     self.wids['e_cpass'].get_text() == usuario.cpass)
        if not condicion and pclases.DEBUG:
            print "usuaruos.py::es_diferente", "e_cpass"
        nivel_ventana = self.wids['sp_nivel'].get_value_as_int()
        nivel_usuario = usuario.nivel
        condicion = (condicion and 
                     nivel_ventana == nivel_usuario)
        if not condicion and pclases.DEBUG:
            print "usuaruos.py::es_diferente", "sp_nivel", nivel_ventana, nivel_usuario
        condicion = (condicion and 
                     self.wids['e_smtpserver'].get_text()==usuario.smtpserver)
        if not condicion and pclases.DEBUG:
            print "usuaruos.py::es_diferente", "e_smtpserver"
        condicion = (condicion and 
            self.wids['e_smtppassword'].get_text() == usuario.smtppassword)
        if not condicion and pclases.DEBUG:
            print "usuaruos.py::es_diferente", "e_smtppassword"
        condicion = (condicion and 
                     self.wids['e_smtpuser'].get_text() == usuario.smtpuser)
        if not condicion and pclases.DEBUG:
            print "usuaruos.py::es_diferente", "e_smtpuser"
        condicion = (condicion and 
                     self.wids['e_email'].get_text() == usuario.email)
        if not condicion and pclases.DEBUG:
            print "usuaruos.py::es_diferente", "e_email"
        condicion = (condicion and 
            self.wids['ch_firmaTotal'].get_active() == usuario.firmaTotal)
        if not condicion and pclases.DEBUG:
            print "usuaruos.py::es_diferente", "ch_firmaTotal"
        condicion = (condicion and 
          self.wids['ch_firmaComercial'].get_active()==usuario.firmaComercial)
        if not condicion and pclases.DEBUG:
            print "usuaruos.py::es_diferente", "ch_firmaComercial"
        condicion = (condicion and 
          self.wids['ch_firmaDirector'].get_active() == usuario.firmaDirector)
        if not condicion and pclases.DEBUG:
            print "usuaruos.py::es_diferente", "ch_firmaDirector"
        condicion = (condicion and 
            self.wids['ch_firmaTecnico'].get_active() == usuario.firmaTecnico)
        if not condicion and pclases.DEBUG:
            print "usuaruos.py::es_diferente", "ch_firmaTecnico"
        condicion = (condicion and 
            self.wids['ch_firmaUsuario'].get_active() == usuario.firmaUsuario)
        buffer = self.wids['txt_observaciones'].get_buffer()
        condicion = (condicion and 
            usuario.observaciones == buffer.get_text(buffer.get_start_iter(), 
                                                        buffer.get_end_iter()))
        if not condicion and pclases.DEBUG:
            print "usuaruos.py::es_diferente","txt_observaciones"
        return not condicion    # "condicion" verifica que sea igual

    def aviso_actualizacion(self):
        """
        Muestra una ventana modal con el mensaje de objeto 
        actualizado.
        """
        utils.dialogo_info('ACTUALIZAR',
                           'El usuario ha sido modificado remotamente.\nDebe actualizar la información mostrada en pantalla.\nPulse el botón «Actualizar»')
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
        cols = (('Módulo/Ventana', 'gobject.TYPE_STRING',False,True,True,None),
                ('Permiso', 'gobject.TYPE_BOOLEAN', True, True, False, 
                    self.cambiar_permiso),
                ('Lectura', 'gobject.TYPE_BOOLEAN', True, True, False, 
                    self.cambiar_lectura),
                ('Modificación', 'gobject.TYPE_BOOLEAN', True, True, False, 
                    self.cambiar_escritura),
                ('Nuevo', 'gobject.TYPE_BOOLEAN', True, True, False, 
                    self.cambiar_ejecucion),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None)
               )
        utils.preparar_treeview(self.wids['tv_permisos'], cols)
        cols = (('Fecha', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_fechahora),
                ('Mensaje', 'gobject.TYPE_STRING', True, True, True, 
                    self.cambiar_mensaje),
                ('Leído', 'gobject.TYPE_BOOLEAN', True, True, False, 
                    self.cambiar_leido),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None)
               )
        utils.preparar_listview(self.wids['tv_mensajes'], cols)
        self.wids['tv_mensajes'].get_selection().set_mode(
            gtk.SELECTION_MULTIPLE)
        self.preparar_tab_modulos()

    def preparar_tab_modulos(self):
        cols = (('Módulo/Ventanas', 'gobject.TYPE_STRING', True, True, True, self.cambiar_nombre_modulo),
                ('Descripción', 'gobject.TYPE_STRING', True, True, False, self.cambiar_descripcion_modulo),
                ('Icono', 'gobject.TYPE_STRING', True, True, False, self.cambiar_icono_modulo),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_modulos'], cols)
        model = gtk.TreeStore(gobject.TYPE_STRING,
                              gobject.TYPE_STRING,
                              gobject.TYPE_STRING,
                              gtk.gdk.Pixbuf,
                              gobject.TYPE_INT64)
        self.wids['tv_modulos'].set_model(model)
        cell = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn('', cell, pixbuf = 3)
        self.wids['tv_modulos'].insert_column(column, 3)
        cols = (('Descripción', 'gobject.TYPE_STRING', True, True, True, self.cambiar_descripcion_ventana),
                ('Fichero', 'gobject.TYPE_STRING', True, True, False, self.cambiar_fichero_ventana),
                ('Clase', 'gobject.TYPE_STRING', True, True, False, self.cambiar_clase_ventana),
                ('Icono', 'gobject.TYPE_STRING', True, True, False, self.cambiar_icono_ventana),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_ventanas'], cols)
        model = gtk.ListStore(gobject.TYPE_STRING,
                              gobject.TYPE_STRING,
                              gobject.TYPE_STRING,
                              gobject.TYPE_STRING,
                              gtk.gdk.Pixbuf,
                              gobject.TYPE_INT64)
        self.wids['tv_ventanas'].set_model(model)
        cell = gtk.CellRendererPixbuf()
        column = gtk.TreeViewColumn('', cell, pixbuf = 4)
        self.wids['tv_ventanas'].insert_column(column, 4)

    def rellenar_tab_modulos(self):
        ventanas = [(v.id, v.descripcion) for v in pclases.Ventana.select(orderBy = "descripcion")]
        utils.rellenar_lista(self.wids['cb_add_ventana'], ventanas)
        self.rellenar_modulos()
        self.rellenar_ventanas()

    def rellenar_modulos(self):
        model = self.wids['tv_modulos'].get_model()
        model.clear()
        for m in pclases.Modulo.select():
            try:
                pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join('..', 'imagenes', m.icono))
            except (gobject.GError, AttributeError):
                pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join('..', 'imagenes', 'dorsia.png'))
            iterpadre = model.append(None, (m.nombre, 
                                            m.descripcion, 
                                            m.icono,
                                            pixbuf, 
                                            m.id))
            for v in m.ventanas:
                try:
                    pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join('..', 'imagenes', v.icono))
                except (gobject.GError, AttributeError):
                    pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join('..', 'imagenes', 'dorsia.png'))
                model.append(iterpadre, (v.fichero,
                                         v.descripcion, 
                                         v.icono,
                                         pixbuf, 
                                         v.id))
        
    def rellenar_ventanas(self):
        model = self.wids['tv_ventanas'].get_model()
        model.clear()
        for v in pclases.Ventana.select():
            try:
                pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join('..', 'imagenes', v.icono))
            except (gobject.GError, AttributeError):
                pixbuf = gtk.gdk.pixbuf_new_from_file(os.path.join('..', 'imagenes', 'dorsia.png'))
            model.append((v.descripcion, 
                          v.fichero, 
                          v.clase, 
                          v.icono,
                          pixbuf, 
                          v.id))

    def activar_widgets(self, s):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        ws = ('table1', 'scrolledwindow1', 'hbox2')
        for w in ws:
            self.wids[w].set_sensitive(s)

    def ir_a_primero(self):
        """
        Hace que el primer registro -si lo hay- de la tabla implicada
        en el objeto del formulario sea el objeto activo.
        """
        usuario = self.objeto
        try:
            # Anulo el aviso de actualización del envío que deja de ser activo.
            if usuario != None: usuario.desactivar()
            usuario = pclases.Usuario.select(orderBy = 'id')[0] 
                # Selecciono todos los usuarioes de venta y me quedo con el primero de la lista.
            usuario.notificador.activar(self.aviso_actualizacion)       # Activo la notificación
        except:
            usuario = None  
        self.objeto = usuario
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
            filas_res.append((r.id, r.usuario, r.nombre, r.cuenta, r.nivel))
        idusuario = utils.dialogo_resultado(filas_res,
                                            titulo = 'Seleccione usuario',
                                            cabeceras = ('ID', 'Usuario', "Nombre", "Cuenta soporte", "Nivel de privilegios"), 
                                            padre = self.wids['ventana']) 
        if idusuario < 0:
            return None
        else:
            return idusuario

    def rellenar_widgets(self):
        """
        Introduce la información del usuario actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        usuario = self.objeto
        if usuario == None: 
            return
        self.wids['ventana'].set_title("Gestión de usuarios - %s" % (usuario.usuario))
        self.wids['e_user'].set_text(usuario.usuario)
        self.wids['e_nombre'].set_text(usuario.nombre)
        self.wids['e_cuenta'].set_text(usuario.cuenta)
        self.wids['e_cpass'].set_text(usuario.cpass)
        self.wids['sp_nivel'].set_value(usuario.nivel)
        self.wids['ch_firmaTotal'].set_active(usuario.firmaTotal)
        self.wids['ch_firmaComercial'].set_active(usuario.firmaComercial)
        self.wids['ch_firmaDirector'].set_active(usuario.firmaDirector)
        self.wids['ch_firmaTecnico'].set_active(usuario.firmaTecnico)
        self.wids['ch_firmaUsuario'].set_active(usuario.firmaUsuario)
        self.wids['txt_observaciones'].get_buffer().set_text(usuario.observaciones)
        usuario.notificador.desactivar()
        if usuario.email == None:
            usuario.email = ""
        self.wids['e_email'].set_text(usuario.email)
        if usuario.smtpserver == None:
            usuario.smtpserver = ""
        self.wids['e_smtpserver'].set_text(usuario.smtpserver)
        if usuario.smtpuser == None:
            usuario.smtpuser = ""
        self.wids['e_smtpuser'].set_text(usuario.smtpuser)
        if usuario.smtppassword == None:
            usuario.smtppassword = ""
        self.wids['e_smtppassword'].set_text(usuario.smtppassword)
        usuario.notificador.activar(self.aviso_actualizacion)
        self.rellenar_permisos()
        self.rellenar_alertas()
        self.rellenar_tab_modulos()
        self.objeto.make_swap()

    def rellenar_permisos(self):
        usuario = self.objeto
        model = self.wids['tv_permisos'].get_model()
        model.clear()
        for m in pclases.Modulo.select():
            ventanasconpermiso = [p.ventana for p in usuario.permisos if p.permiso and p.ventana.modulo == m]
            if len(ventanasconpermiso) == len(m.ventanas) and len(m.ventanas) > 0:
                permisomodulo = True
            else:
                permisomodulo = False
            if len([p.ventana for p in usuario.permisos if p.lectura and p.ventana.modulo == m]) == len(m.ventanas) and len(m.ventanas) > 0:
                rmodulo = True
            else:
                rmodulo = False
            if len([p.ventana for p in usuario.permisos if p.escritura and p.ventana.modulo == m]) == len(m.ventanas) and len(m.ventanas) > 0:
                wmodulo = True
            else:
                wmodulo = False
            if len([p.ventana for p in usuario.permisos if p.nuevo and p.ventana.modulo == m]) == len(m.ventanas) and len(m.ventanas) > 0:
                xmodulo = True
            else:
                xmodulo = False
            iterpadre = model.append(None, (m.nombre, 
                                            permisomodulo, 
                                            rmodulo, 
                                            wmodulo, 
                                            xmodulo,
                                            m.id))
            # PLAN: El CellRendererToggle tiene una propiedad "inconsistent". Se podría usar para indicar
            # si tiene permisos sobre algunas de las ventanas del módulo.
            for v in m.ventanas:
                model.append(iterpadre, (v.descripcion,
                                         v.id in [p.ventana.id for p in usuario.permisos if p.permiso],
                                         v.id in [p.ventana.id for p in usuario.permisos if p.lectura],
                                         v.id in [p.ventana.id for p in usuario.permisos if p.escritura],
                                         v.id in [p.ventana.id for p in usuario.permisos if p.nuevo],
                                         v.id))
    
    def wraplines(self, texto, MAX):
        """
        Hace básicamente lo mismo que el cutmaster de menu.py, 
        pero con otro tamaño. Voy con prisas y no me quiero parar
        ahora a modificarlo para que acepte el máximo por 
        parámetro, importarlo o meterlo en utils.
        """
        if len(texto) > MAX:
            palabras = texto.split(' ')
            t = ''
            l = ''
            for p in palabras:
                if len(l) + len(p) + 1 < MAX:
                    l += "%s " % p
                else:
                    t += "%s\n" % l
                    l = "%s " % p
                if len(l) > MAX:    # Se ha colado una palabra de más del MAX
                    tmp = l
                    while len(tmp) > MAX:
                        t += "%s-\n" % tmp[:MAX]
                        tmp = tmp[MAX:]
                    l = tmp
                # print t.replace("\n", "|"), "--", l, "--", p
            t += l
            res = t
        else:
            res = texto
        return res
    
    def rellenar_alertas(self):
        model = self.wids['tv_mensajes'].get_model()
        model.clear()
        for a in self.objeto.alertas:
            model.append((a.fechahora.strftime('%d/%m/%Y %H:%M'),
                          self.wraplines(a.mensaje, 60),
                          a.entregado,
                          a.id))

    def set_permiso(self, ventana, permitir, r = None, w = None, x = None):
        """
        Busca un registro permiso entre la ventana y el usuario.
        Si no existe lo crea.
        Establece el permiso a lo que indique permitir.
        Si r, w o x son None no se tocan esos permisos. Si son True o False 
        se le pone el permiso a ese valor booleano.
        """
        usuario = self.objeto
        if ventana not in [p.ventana for p in usuario.permisos]:
            p = pclases.Permiso(usuario = usuario, ventana = ventana, permiso = permitir)
            pclases.Auditoria.nuevo(p, self.usuario, __file__)
        else:
            p = [p for p in usuario.permisos if p.ventana == ventana][0]
            p.permiso = permitir
        if r != None:
            p.lectura = r or permitir # Si se le permite abrir lo lógico es que pueda leer registros ya existentes al menos.
        if w != None:
            p.escritura = w
        if x != None:
            p.nuevo = x
        

    # --------------- Manejadores de eventos ----------------------------
    def cambiar_nombre_modulo(self, cell, path, text):
        model = self.wids['tv_modulos'].get_model()
        idm = model[path][-1]
        modulo = pclases.Modulo.get(idm)
        modulo.nombre = text
        self.rellenar_tab_modulos()
        
    def cambiar_descripcion_modulo(self, cell, path, text):
        model = self.wids['tv_modulos'].get_model()
        idm = model[path][-1]
        modulo = pclases.Modulo.get(idm)
        modulo.descripcion = text
        self.rellenar_tab_modulos()

    def cambiar_icono_modulo(self, cell, path, text):
        model = self.wids['tv_modulos'].get_model()
        idm = model[path][-1]
        modulo = pclases.Modulo.get(idm)
        modulo.icono = text
        self.rellenar_tab_modulos()

    def cambiar_descripcion_ventana(self, cell, path, text):
        model = self.wids['tv_ventanas'].get_model()
        idv = model[path][-1]
        ventana = pclases.Ventana.get(idv)
        ventana.descripcion = text
        self.rellenar_tab_modulos()
        
    def cambiar_fichero_ventana(self, cell, path, text):
        model = self.wids['tv_ventanas'].get_model()
        idv = model[path][-1]
        ventana = pclases.Ventana.get(idv)
        ventana.fichero = text
        self.rellenar_tab_modulos()

    def cambiar_clase_ventana(self, cell, path, text):
        model = self.wids['tv_ventanas'].get_model()
        idv = model[path][-1]
        ventana = pclases.Ventana.get(idv)
        ventana.clase = text
        self.rellenar_tab_modulos()

    def cambiar_icono_ventana(self, cell, path, text):
        model = self.wids['tv_ventanas'].get_model()
        idv = model[path][-1]
        ventana = pclases.Ventana.get(idv)
        ventana.icono = text
        self.rellenar_tab_modulos()
        
    def enviar_mensaje(self, b):
        usuario = self.objeto
        texto = utils.dialogo_entrada(titulo = 'NUEVO MENSAJE', texto = 'Introduzca mensaje de la alerta:')
        if texto != None:
            usuario.enviar_mensaje(texto)
        self.rellenar_alertas()
    
    def borrar_mensaje(self, b):
        model, paths = self.wids['tv_mensajes'].get_selection().get_selected_rows()
        for path in paths:
            aid = model[path][-1]
            alerta = pclases.Alerta.get(aid)
            if not alerta.entregado:
                utils.dialogo_info(titulo = "ALERTA PENDIENTE", texto = "La alerta seleccionada aún no ha sido leída por el usuario.\nMárquela como leída si realmente quiere borrarla.")
            else:
                try:
                    alerta.destroy(ventana = __file__)
                except:
                    utils.dialogo_info(titulo = "ERROR", texto = "El mensaje no se pudo borrar")
        self.rellenar_alertas()
    
    def cambiar_permiso(self, cell, path):
        model = self.wids['tv_permisos'].get_model()
        permitir = not cell.get_active()
        if not model[path].parent:  # Permitir acceso a todo el módulo
            idm = model[path][-1]
            modulo = pclases.Modulo.get(idm)
            for ventana in modulo.ventanas:
                self.set_permiso(ventana, permitir)
            # Actualizo el model para reflejar los cambios en el treeview:
            model[path][1] = permitir
            for hijo in model[path].iterchildren():
                hijo[1] = permitir
        else:
            idv = model[path][-1]
            ventana = pclases.Ventana.get(idv)
            self.set_permiso(ventana, permitir)
            # Actualizo el model para reflejar los cambios en el treeview:
            model[path][1] = permitir
#        self.rellenar_permisos()
        
    def cambiar_lectura(self, cell, path):
        model = self.wids['tv_permisos'].get_model()
        permiso_lectura = not cell.get_active()
        if not model[path].parent:  # Permitir acceso a todo el módulo
            idm = model[path][-1]
            modulo = pclases.Modulo.get(idm)
            for ventana in modulo.ventanas:
                self.set_permiso(ventana, True, r = permiso_lectura)
            # Actualizo el model para reflejar los cambios en el treeview:
            model[path][2] = permiso_lectura
            model[path][1] = model[path][1] or permiso_lectura
            for hijo in model[path].iterchildren():
                hijo[2] = permiso_lectura
                hijo[1] = hijo[1] or permiso_lectura
        else:
            idv = model[path][-1]
            ventana = pclases.Ventana.get(idv)
            self.set_permiso(ventana, True, r = permiso_lectura)
            # Actualizo el model para reflejar los cambios en el treeview:
            model[path][2] = permiso_lectura
            model[path][1] = model[path][1] or permiso_lectura

    def cambiar_escritura(self, cell, path):
        model = self.wids['tv_permisos'].get_model()
        permiso_escritura = not cell.get_active()
        if not model[path].parent:  # Permitir acceso a todo el módulo
            idm = model[path][-1]
            modulo = pclases.Modulo.get(idm)
            for ventana in modulo.ventanas:
                self.set_permiso(ventana, True, w = permiso_escritura)
            # Actualizo el model para reflejar los cambios en el treeview:
            model[path][3] = permiso_escritura
            model[path][1] = model[path][1] or permiso_escritura
            for hijo in model[path].iterchildren():
                hijo[3] = permiso_escritura
                hijo[1] = hijo[1] or permiso_escritura
        else:
            idv = model[path][-1]
            ventana = pclases.Ventana.get(idv)
            self.set_permiso(ventana, True, w = permiso_escritura)
            # Actualizo el model para reflejar los cambios en el treeview:
            model[path][3] = permiso_escritura
            model[path][1] = model[path][1] or permiso_escritura

    def cambiar_ejecucion(self, cell, path):
        model = self.wids['tv_permisos'].get_model()
        permiso_nuevo = not cell.get_active()
        if not model[path].parent:  # Permitir acceso a todo el módulo
            idm = model[path][-1]
            modulo = pclases.Modulo.get(idm)
            for ventana in modulo.ventanas:
                self.set_permiso(ventana, True, x = permiso_nuevo)
            # Actualizo el model para reflejar los cambios en el treeview:
            model[path][4] = permiso_nuevo
            model[path][1] = model[path][1] or permiso_nuevo
            for hijo in model[path].iterchildren():
                hijo[4] = permiso_nuevo
                hijo[1] = hijo[1] or permiso_nuevo
        else:
            idv = model[path][-1]
            ventana = pclases.Ventana.get(idv)
            self.set_permiso(ventana, True, x = permiso_nuevo)
            # Actualizo el model para reflejar los cambios en el treeview:
            model[path][4] = permiso_nuevo
            model[path][1] = model[path][1] or permiso_nuevo

    def cambiar_fechahora(self, cell, path, text):
        model = self.wids['tv_mensajes'].get_model()
        ida = model[path][-1]
        alerta = pclases.Alerta.get(ida)
        try:
            fecha, hora = text.split(' ')
            dia, mes, anno = map(int, fecha.split('/'))
            horas, minutos = map(int, hora.split(':'))
            alerta.fechahora = mx.DateTime.DateTimeFrom(day = dia, month = mes, year = anno, hour = horas, minute = minutos)
        except:
            utils.dialogo_info(titulo = 'HORA INCORRECTA', texto = 'El formato debe ser "dia/mes/año horas:minutos"')
        self.rellenar_alertas()
        
    def cambiar_mensaje(self, cell, path, text):
        model = self.wids['tv_mensajes'].get_model()
        ida = model[path][-1]
        alerta = pclases.Alerta.get(ida)
        alerta.mensaje = text
        self.rellenar_alertas()
        
    def cambiar_leido(self, cell, path):
        model = self.wids['tv_mensajes'].get_model()
        ida = model[path][-1]
        alerta = pclases.Alerta.get(ida)
        alerta.entregado = not cell.get_active()
        self.rellenar_alertas()

    def crear_nuevo_usuario(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        usuario = self.objeto
        txt = """
        Introduzca nombre de usuario.                               
        Tenga en cuenta que inicialmente la contraseña será         
        la misma que el nombre de usuario. Aunque por defecto       
        el usuario no tendrá permisos, considere cambiar la         
        contraseña por una más segura.                              
        Tenga en cuenta también que el nombre de usuario            
        (distinto al nombre real) no debe superar los 16            
        caracteres.                                                 
        """
        try:
            nomusuario = utils.dialogo_entrada(txt, 
                                               'NOMBRE DE USUARIO', '')
        except:
            # Seguramente haya introducido un nombre repetido o en blanco (valor por defecto del diálogo).
            utils.dialogo_info()
            return
        if nomusuario == None: return
        if usuario != None: 
            usuario.notificador.desactivar()
        try:
            passwd = md5.new(nomusuario).hexdigest()
        except AttributeError:  # Es el md5 de hashlib
            passwd = md5(nomusuario).hexdigest()
        usuario = pclases.Usuario(usuario = nomusuario,
                                        passwd = passwd,
                                        nombre = '',
                                        cuenta = '',
                                        cpass = '')
        pclases.Auditoria.nuevo(usuario, self.usuario, __file__)
        utils.dialogo_info('USUARIO CREADO', 'El usuario %s ha sido creado.\nNo olvide completar el resto de información relativa al mismo.' % usuario.usuario)
        usuario.notificador.activar(self.aviso_actualizacion)
        self.objeto = usuario
        self.actualizar_ventana()

    def buscar_usuario(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        usuario = self.objeto
        a_buscar = utils.dialogo_entrada("Introduzca nombre de usuario o nombre real:") 
        if a_buscar != None:
            resultados = pclases.Usuario.select(pclases.OR(pclases.Usuario.q.usuario.contains(a_buscar),
                                                             pclases.Usuario.q.nombre.contains(a_buscar)))
            if resultados.count() > 1:
                ## Refinar los resultados
                idusuario = self.refinar_resultados_busqueda(resultados)
                if idusuario == None:
                    return
                resultados = [pclases.Usuario.get(idusuario)]
            elif resultados.count() < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info('SIN RESULTADOS', 'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.\n(Atención: Ver la lista completa puede resultar lento si el número de elementos es muy alto)')
                return
            ## Un único resultado
            # Primero anulo la función de actualización
            if usuario != None:
                usuario.notificador.desactivar()
            # Pongo el objeto como actual
            usuario = resultados[0]
            # Y activo la función de notificación:
            usuario.notificador.activar(self.aviso_actualizacion)
        self.objeto = usuario
        self.actualizar_ventana()

    def guardar(self, widget):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        usuario = self.objeto
        # Campos del objeto que hay que guardar:
        nusuario = self.wids['e_user'].get_text()
        nombre = self.wids['e_nombre'].get_text()
        cuenta = self.wids['e_cuenta'].get_text()
        cpass = self.wids['e_cpass'].get_text()
        nivel = self.wids['sp_nivel'].get_value_as_int()
        email = self.wids['e_email'].get_text()
        smtpserver = self.wids['e_smtpserver'].get_text()
        smtpuser = self.wids['e_smtpuser'].get_text()
        smtppassword = self.wids['e_smtppassword'].get_text()
        # Desactivo el notificador momentáneamente
        usuario.notificador.desactivar()
        # Actualizo los datos del objeto
        usuario.firmaTotal = self.wids['ch_firmaTotal'].get_active()
        usuario.firmaComercial = self.wids['ch_firmaComercial'].get_active()
        usuario.firmaDirector = self.wids['ch_firmaDirector'].get_active()
        usuario.firmaTecnico = self.wids['ch_firmaTecnico'].get_active()
        usuario.firmaUsuario = self.wids['ch_firmaUsuario'].get_active()
        if usuario.firmaTotal:
            usuario.firmaComercial = usuario.firmaDirector = usuario.firmaTecnico = usuario.firmaUsuario = True
        buffer = self.wids['txt_observaciones'].get_buffer()
        usuario.observaciones = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter())
        usuario.usuario = nusuario
        usuario.nombre = nombre 
        usuario.cuenta = cuenta
        usuario.cpass = cpass
        usuario.nivel = nivel
        usuario.email = email
        usuario.smtpserver = smtpserver
        usuario.smtppassword = smtppassword
        usuario.smtpuser = smtpuser
        # Fuerzo la actualización de la BD y no espero a que SQLObject lo haga por mí:
        usuario.sync()
        # Vuelvo a activar el notificador
        usuario.notificador.activar(self.aviso_actualizacion)
        self.objeto = usuario
        self.actualizar_ventana()
        self.wids['b_guardar'].set_sensitive(False)

    def limpiar_modulo(self, b = None):
        self.wids['e_nombre_modulo'].set_text('')
        self.wids['e_icono_modulo'].set_text('')
        self.wids['e_descripcion_modulo'].set_text('')
        
    def limpiar_ventana(self, b = None):
        self.wids['e_icono_ventana'].set_text('')
        self.wids['e_descripcion_ventana'].set_text('')
        self.wids['e_archivo_ventana'].set_text('')
        self.wids['e_clase_ventana'].set_text('')

    def nueva_contrasenna(self, b):
        passw = utils.dialogo_entrada(titulo = 'NUEVA CONTRASEÑA',
                                      texto = 'Introduzca la nueva contraseña', 
                                      padre = self.wids['ventana'])
        try:
            self.objeto.notificador.desactivar() 
            try:
                self.objeto.passwd = md5.new(passw).hexdigest()
            except AttributeError:  # Es el md5 de hashlib
                self.objeto.passwd = md5(passw).hexdigest()
            utils.dialogo_info(titulo = 'CONTRASEÑA CAMBIADA', 
                               texto = 'Contraseña cambiada con éxito.', 
                               padre = self.wids['ventana'])
            self.objeto.sync()
            self.objeto.notificador.activar(self.aviso_actualizacion)
                # Activo la notificación
            self.actualizar_ventana()
        except Exception, msg:
            utils.dialogo_info(titulo = 'ERROR', 
                texto = 'Contraseña no cambiada. Contacte con el administrador'
                        ' de la base de datos para que la restrablezca '
                        'manualmente.\n\n\n'
                        'Información de depuración: %s' % msg, 
                padre = self.wids['ventana'])

    def add_ventana_a_modulo(self, b):
        model, itr = self.wids['tv_modulos'].get_selection().get_selected()
        if itr == None or model[itr].parent != None:
            utils.dialogo_info(titulo = 'SELECCIONE MÓDULO', texto = 'Debe seleccionar un módulo al que añadir la ventana.')
            return
        idventana = utils.combo_get_value(self.wids['cb_add_ventana'])
        if idventana == None:
            utils.dialogo_info(titulo = 'SELECCIONE VENTANA', texto = 'Debe seleccionar una ventana para añadir al módulo.')
        idmodulo = model[itr][-1]
        modulo = pclases.Modulo.get(idmodulo)
        ventana = pclases.Ventana.get(idventana)
        ventana.modulo = modulo
        self.rellenar_tab_modulos()
        
    def add_modulo(self, b):
        nombre = self.wids['e_nombre_modulo'].get_text()
        icono = self.wids['e_icono_modulo'].get_text()
        descripcion = self.wids['e_descripcion_modulo'].get_text()
        if nombre:
            m = pclases.Modulo(nombre = nombre, icono = icono, descripcion = descripcion)
            pclases.Auditoria.nuevo(m, self.usuario, __file__)
            self.limpiar_modulo()
            self.rellenar_tab_modulos()
        
    def drop_modulo(self, b):
        model, itr = self.wids['tv_modulos'].get_selection().get_selected()
        if itr != None:
            if model[itr].parent == None:
                idmodulo = model[itr][-1]
                modulo = pclases.Modulo.get(idmodulo)
                for v in modulo.ventanas:
                    v.modulo = None
                modulo.destroy(ventana = __file__)
            else:
                idventana = model[itr][-1]
                ventana = pclases.Ventana.get(idventana)
                ventana.modulo = None
            self.rellenar_tab_modulos()
        
    def add_ventana(self, b):
        icono = self.wids['e_icono_ventana'].get_text()
        descripcion = self.wids['e_descripcion_ventana'].get_text()
        fichero = self.wids['e_archivo_ventana'].get_text()
        clase = self.wids['e_clase_ventana'].get_text()
        if fichero and descripcion and clase:
            v = pclases.Ventana(descripcion = descripcion, icono = icono, clase = clase, fichero = fichero, modulo = None)
            pclases.Auditoria.nuevo(v, self.usuario, __file__)
            self.limpiar_ventana()
            self.rellenar_tab_modulos()
        
    def drop_ventana(self, b):
        model, itr = self.wids['tv_ventanas'].get_selection().get_selected()
        if itr != None:
            idventana = model[itr][-1]
            ventana = pclases.Ventana.get(idventana)
            ventana.modulo = None
            for p in ventana.permisos:
                p.ventana = None
                p.usuario = None
                p.destroy(ventana = __file__)
            ventana.destroy(ventana = __file__)
            self.rellenar_tab_modulos()

    def borrar_usuario(self, boton):
        """
        Elimina el albarán de la BD y anula la relación entre
        él y sus LDVs.
        """
        if not utils.dialogo('Se intentará eliminar el usuario actual y todos sus permisos y datos relacionados.\n¿Está seguro?', 'BORRAR USUARIO'): return
        usuario = self.objeto
        usuario.notificador.desactivar()
        for permiso in usuario.permisos:
            permiso.usuario = None
            permiso.destroy(ventana = __file__)
        for alerta in usuario.alerta:
            alerta.usuario = None
            alerta.destroy(ventana = __file__)
        try:
            usuario.destroy(ventana = __file__)
        except:
            utils.dialogo_info('ERROR', 'No se pudo eliminar.\nIntente borrar primero sus mensajes pendientes, etc.')
            return
        self.ir_a_primero()


if __name__=='__main__':
    u = Usuarios()

