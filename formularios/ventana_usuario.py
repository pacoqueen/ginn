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
## ventana_usuario.py 
###################################################################
## NOTAS:
## 
###################################################################
## Changelog:
## 27 de abril de 2006 -> Inicio.
## 
###################################################################
## 
## 
###################################################################
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import sys, os 
try:
    import pclases
except ImportError:
    sys.path.append(os.path.join('..', 'framework'))
    import pclases
import gtk, gtk.glade, time, sqlobject, mx
import mx.DateTime
import gobject
import md5

class Usuarios(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        Ventana.__init__(self, 'ventana_usuario.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_actualizar/clicked': self.actualizar_ventana, 
                       'b_guardar/clicked': self.guardar, 
                       'b_nuevo/clicked': self.crear_nuevo_usuario, 
                       'b_borrar/clicked': self.borrar_usuario, 
                       'b_buscar/clicked': self.buscar_usuario,
                       'b_enviar/clicked': self.enviar_mensaje,
                       'b_passw/clicked': self.nueva_contrasenna,
                       'b_drop/clicked': self.borrar_mensaje
                      }
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
            utils.dialogo_info(titulo = "NO SE PUDO DETERMINAR SU USUARIO",
                               texto = "No se pudo determinar su nombre de usuario.\nAsegúrese de haber iniciado sesión correctamente y vuelva a intentarlo.",
                               padre = self.wids['ventana'])
            self.logger.error("ventana_usuario::__init__:No se pudo determinar nombre de usuario.")
        else:
            self.ir_a(objeto)
            self.wids['ventana'].maximize()
            gtk.main()

    # --------------- Funciones auxiliares ------------------------------
    def es_diferente(self):
        """
        Devuelve True si la información en pantalla es distinta a la
        del objeto en memoria.
        """
        usuario = self.objeto
        if usuario == None: return False    # Si no hay usuario activo, devuelvo que no hay cambio respecto a la ventana
        condicion = usuario.usuario == self.wids['e_user'].get_text()
        condicion = condicion and (usuario.nombre == self.wids['e_nombre'].get_text())
        condicion = condicion and self.wids['e_cuenta'].get_text() == usuario.cuenta
        condicion = condicion and self.wids['e_cpass'].get_text() == usuario.cpass 
        condicion = condicion and self.wids['e_smtpserver'].get_text() == usuario.smtpserver
        condicion = condicion and self.wids['e_smtppassword'].get_text() == usuario.smtppassword
        condicion = condicion and self.wids['e_smtpuser'].get_text() == usuario.smtpuser
        condicion = condicion and self.wids['e_email'].get_text() == usuario.email
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
#   self.wids['ch_interno'].set_sensible(False)
        cols = (('Fecha', 'gobject.TYPE_STRING', True, True, False, self.cambiar_fechahora),
                ('Mensaje', 'gobject.TYPE_STRING', True, True, True, self.cambiar_mensaje),
                ('Leído', 'gobject.TYPE_BOOLEAN', True, True, False, self.cambiar_leido),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None)
               )
        utils.preparar_listview(self.wids['tv_mensajes'], cols)

    def activar_widgets(self, s):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        #ws = ('table1')
        ws = []
        for w in ws:
            self.wids[w].set_sensitive(s)

    def ir_a_primero(self):
        """
        Hace que el primer registro -si lo hay- de la tabla implicada
        en el objeto del formulario sea el objeto activo.
        """
        self.objeto = None
        self.rellenar_widgets()

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
            filas_res.append((r.id, r.usuario))
        idusuario = utils.dialogo_resultado(filas_res,
                                            titulo = 'Seleccione usuario',
                                            cabeceras = ('ID Interno', 'Nombre de usuario')) 
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
        if usuario != None:
            self.wids['e_user'].set_text(usuario.usuario)
            self.wids['e_nombre'].set_text(usuario.nombre)
            self.wids['e_cuenta'].set_text(usuario.cuenta)
            self.wids['e_cpass'].set_text(usuario.cpass)
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
            self.rellenar_alertas()
            self.objeto.make_swap()
    
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
#                print t.replace("\n", "|"), "--", l, "--", p
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

        
    def enviar_mensaje(self, b):
        usuario = self.objeto
        texto = utils.dialogo_entrada(titulo = 'NUEVO MENSAJE', texto = 'Introduzca mensaje de la alerta:')
        if texto != None:
            usuario.enviar_mensaje(texto)
        self.rellenar_alertas()
    
    def borrar_mensaje(self, b):
        model, iter = self.wids['tv_mensajes'].get_selection().get_selected()
        if iter != None:
            aid = model[iter][-1]
            alerta = pclases.Alerta.get(aid)
            if not alerta.entregado:
                utils.dialogo_info(titulo = "ALERTA PENDIENTE", texto = "La alerta seleccionada aún no ha sido leída por el usuario.\nMárquela como leída si realmente quiere borrarla.")
            else:
                try:
                    alerta.destroySelf()
                except:
                    utils.dialogo_info(titulo = "ERROR", texto = "El mensaje no se pudo borrar", padre = self.wids['ventana'])
                self.rellenar_alertas()
    
        
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
        if usuario != None: usuario.notificador.desactivar()
        usuario = pclases.Usuario(usuario = nomusuario,
                                        passwd = md5.new(nomusuario).hexdigest(),
                                        nombre = '',
                                        cuenta = '',
                                        cpass = '')
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
            resultados = pclases.Usuario.select(sqlobject.OR(pclases.Usuario.q.usuario.contains(a_buscar),
                                                             pclases.Usuario.q.nombre.contains(a_buscar)))
            if resultados.count() > 1:
                ## Refinar los resultados
                idusuario = self.refinar_resultados_busqueda(resultados)
                if idusuario == None:
                    return
                resultados = [pclases.Uduario.get(idusuario)]
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
        email = self.wids['e_email'].get_text()
        smtpserver = self.wids['e_smtpserver'].get_text()
        smtpuser = self.wids['e_smtpuser'].get_text()
        smtppassword = self.wids['e_smtppassword'].get_text()
        # Desactivo el notificador momentáneamente
        usuario.notificador.desactivar()
        # Actualizo los datos del objeto
        usuario.usuario = nusuario
        usuario.nombre = nombre 
        usuario.cuenta = cuenta
        usuario.cpass = cpass
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

    def nueva_contrasenna(self, b):
        passw = utils.dialogo_entrada(titulo = 'NUEVA CONTRASEÑA',
                                      texto = 'Introduzca la nueva contraseña')
        try:
            self.objeto.notificador.desactivar() 
            self.objeto.passwd = md5.new(passw).hexdigest()
            utils.dialogo_info(titulo = 'CONTRASEÑA CAMBIADA', texto = 'Contraseña cambiada con éxito.')
            self.objeto.sync()
            self.objeto.notificador.activar(self.aviso_actualizacion)       # Activo la notificación
            self.actualizar_ventana()
        except:
            utils.dialogo_info(titulo = 'ERROR', texto = 'Contraseña no cambiada. Contacte con el administrador de la base de datos para que la restrablezca manualmente.', padre = self.wids['ventana'])


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
            permiso.destroySelf()
        for alerta in usuario.alerta:
            alerta.usuario = None
            alerta.destroySelf()
        try:
            usuario.destroySelf()
        except:
            utils.dialogo_info('ERROR', 'No se pudo eliminar.\nIntente borrar primero sus mensajes pendientes, etc.', padre = self.wids['ventana'])
            return
        self.ir_a_primero()


if __name__=='__main__':
    u = Usuarios()

