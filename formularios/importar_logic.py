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
## importar_logic.py - Ventana para importar MDB de logic.
###################################################################
## Changelog:
## 22 de mayo de 2006 -> Inicio
###################################################################
## NOTAS:
## En el directorio utils hay algunos binarios mdb-*, pero están 
## enlazados dinámicamente. Por el momento usaré los instalados 
## del repositorio de Debian/Guadalinex en el servidor. Para las
## máquinas cliente tendré que buscar la forma de lanzar los 
## binarios para MS-Windows o GNU/Linux dependiendo de la 
## plataforma. O bien usar el servidor a modo de cgi o algo 
## parecido que procese el archivo y devuelva el resultado.
## [...]
## Finalmente he usado XMLRPC. Una maravilla, señora.
##
## La barra de actividad no se mueve dado que el intérprete espera
## a que el proceso remoto acabe, congelando incluso Gtk. Por eso,
## puede parecer que se ha colgado, pero NO ES ASÍ.
##
## NOTA: ¡¡¡ IMPORTANTE !!! ¡¡¡ IMPORTANTE !!! ¡¡¡ IMPORTANTE !!!
## Debe haber un usuario logic con la contraseña indicada en 
## el servidor.
## DONE: Con el metaf de menu.py no va el scp (da error por no 
## poder abrir fileno o algo así).
###################################################################
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sqlobject
import sys
try:
    import pclases
    from configuracion import ConfigConexion
except ImportError:
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    import pclases
    from configuracion import ConfigConexion
import mx
import mx.DateTime
import os, time, tempfile
sys.path.append('.')
from sshsession import SshSession
import socket
from ventana_progreso import VentanaActividad
import gobject

class ImportarLogic(Ventana):
    # pexpect necesita una salida de erorres "de verdad"
    sys.stderr = sys.__stderr__
    def __init__(self, objeto = None, usuario = None):
        config = ConfigConexion()
        self.CONFIG = {'host': config.get_host(), 'port': 22222, # Parámetros XMLRPC
                       'user': 'logic', 'password': 'svabk3', 'dir_destino': '/tmp'}  #Parámetros SCP
#        self.CONFIG = {'host': '192.168.1.100', 'port': 22222, # Parámetros XMLRPC
#                       'user': 'logic', 'password': 'svabk3', 'dir_destino': '/tmp'}  #Parámetros SCP

##############################################################################################################
##### You, lamer. This is for you. Read carefully:                                                       #####
##### Don't try to crack this login. See? 192.168.1.100 It's a LAN! Behind a firewall and                #####
##### without extern connections. Don't waste your time. Neither my bandwidth. IT ISN'T MY HOME MACHINE! #####
##############################################################################################################

        self.seguir = True
        Ventana.__init__(self, 'importar_logic.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_abrir/clicked': self.abrir,
                       'b_abrir_cuentas/clicked': self.abrir_cuentas,
                       'ch_mismo/toggled': self.usar_mismo,
                       'b_procesar/clicked': self.procesar}
        self.add_connections(connections)
        gtk.main()

    def chequear_cambios(self):
        pass

    def mostrar_dialogo_abrir(self):
        dialog = gtk.FileChooserDialog("Abrir",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        try:
            home = os.environ['HOME']
        except KeyError:
            try:
                home = os.environ['HOMEPATH']
            except KeyError:
                home = "."
                print "WARNING: No se pudo obtener el «home» del usuario"
        if os.path.exists(os.path.join(home, 'bin', 'geomdb')):
            dialog.set_current_folder(os.path.join(home, 'bin', 'geomdb'))
        else:
            dialog.set_current_folder(home)
        filter = gtk.FileFilter()
        filter.set_name("Archivos exportados de LOGIC")
        filter.add_pattern("*.mdb")
        filter.add_pattern("*.MDB")
        filter.add_pattern("*.Mdb")

        dialog.add_filter(filter)
        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        dialog.add_filter(filter)


        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            archivo = dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            archivo = None
        dialog.destroy()
        return archivo

    def abrir(self, b):
        nomarchivo = self.mostrar_dialogo_abrir()
        if nomarchivo == None:
            return
        self.add_salida('Esta operación puede tardar mucho.\nDeje que se complete aunque la ventana parezca congelada.\nPulse "Procesar" para comenzar.\n\n')
        self.wids['e_mdb'].set_text(nomarchivo)

    def abrir_cuentas(self, b):
        nomarchivo = self.mostrar_dialogo_abrir()
        if nomarchivo == None:
            return
        self.wids['e_cuentas'].set_text(nomarchivo)

    def usar_mismo(self, ch):
        act = ch.get_active()
        self.wids['e_cuentas'].set_text(self.wids['e_mdb'].get_text())
        self.wids['e_cuentas'].set_sensitive(not act)
        self.wids['b_abrir_cuentas'].set_sensitive(not act)

    def add_salida(self, texto):
        self.wids['txt_out'].get_buffer().insert_at_cursor(texto)

    def importar_en_remoto(self, host, puerto, nomarchivo, nomarchivo_cuentas):
        """
        host: nombre canónico del host remoto o IP.
        puerto: puerto XMLRCP.
        nomarchivo: Nombre del fichero a tratar. Sólo el nombre, sin ruta, y tal y 
                    como se espera encontrar en el servidor (respetando mayúsculas, etc.).
        """
        import xmlrpclib
        server_url = 'http://%s:%s' % (host, puerto)
        server = xmlrpclib.Server(server_url)
        return server.parse(nomarchivo, nomarchivo_cuentas)

    def _actualizar(self, vprogreso):
        vprogreso.mover()
        time.sleep(0.03)
        if not self.seguir:
            vprogreso.ocultar()
        return self.seguir   # Poner a False cuando acabe el proceso y haya que cerrar la ventana de actividad

    def copia_remota(self, rutacompleta):
        # Copia del .mdb a un directorio temporal en el servidor GNU/Linux.
        self.add_salida('Copiando fichero %s...\n' % (rutacompleta))
        # Ventana de actividad: ---8<---
        self.seguir = True
        vprogreso = VentanaActividad(texto = 'Creando copia remota...\n(Esta operación puede tomar algún tiempo.)', padre = self.wids['ventana'])
        self.wids['ventana'].window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        while gtk.events_pending(): gtk.main_iteration(False)
        vprogreso.mostrar()
        vprogreso.mover()
#        gobject.idle_add(self._actualizar, vprogreso, priority = gobject.PRIORITY_LOW)
#        self._actualizar(vprogreso)
#        while gtk.events_pending(): gtk.main_iteration(False)
        # ------------------------->8---
        sesion = SshSession(host = self.CONFIG['host'], user = self.CONFIG['user'], password = self.CONFIG['password'])
        sesion.scp(src = rutacompleta, dest = self.CONFIG['dir_destino'])
        # -------------------------8<---
        vprogreso.mover()
        self.seguir = False
        vprogreso.ocultar()
        # ------------------------->8---
        self.wids['ventana'].window.set_cursor(None)

    def metodo_remoto(self, rutacompleta, rutacompleta_cuentas):
        # Llamada RPC para importar: 
        nomarchivo = os.path.basename(rutacompleta)
        nomarchivo_cuentas = os.path.basename(rutacompleta_cuentas)
        self.add_salida('Importando datos...\n')
        # Ventana de actividad: ---8<---
        self.seguir = True
        self.wids['ventana'].window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        while gtk.events_pending(): gtk.main_iteration(False)
        vprogreso = VentanaActividad(texto = 'Invocando procedimiento remoto...\n(Esta operación puede tomar algún tiempo.)', padre = self.wids['ventana'])
        vprogreso.mostrar()
        vprogreso.mover()
#        gobject.idle_add(self._actualizar, vprogreso, priority = gobject.PRIORITY_LOW)#, priority = gobject.PRIORITY_HIGH_IDLE)
#        self._actualizar(vprogreso)
#        while gtk.events_pending(): gtk.main_iteration(False)
        # ------------------------->8---
        try:
            res = self.importar_en_remoto(self.CONFIG['host'], self.CONFIG['port'], nomarchivo, nomarchivo_cuentas)
        except socket.error, msg:
            self.add_salida('La llamada a procedimiento remoto falló:\n%s\n' % msg)
            res = 1
        # -------------------------8<---
        vprogreso.mover()
        self.seguir = False
        vprogreso.ocultar()
        # ------------------------->8---
        self.wids['ventana'].window.set_cursor(None)
        if res != 0:
            self.add_salida('El comando remoto devolvió el código de error %d.\n' % res)
        else:
            self.add_salida("Importación satisfactoria.\n\nPuede cerrar la ventana ahora.")

    def procesar(self, b):
        rutacompleta = self.wids['e_mdb'].get_text()
        rutacompleta_cuentas = self.wids['e_cuentas'].get_text()
        if os.path.exists(rutacompleta) and os.path.exists(rutacompleta_cuentas):
            self.copia_remota(rutacompleta)
            self.copia_remota(rutacompleta_cuentas)
            self.metodo_remoto(rutacompleta, rutacompleta_cuentas)
        else:
            utils.dialogo_info(titulo = "NO ENCONTRADO", texto = "Archivo(s) no encontrado(s).", padre = self.wids['ventana'])


if __name__ == '__main__':
    t = ImportarLogic()    
