#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2013  Francisco José Rodríguez Bogado                    #
#                          <frbogado@geotexan.com>                            #
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
## mail_sender.py - Ventana para enviar correos electrónicos.
###################################################################
## NOTAS:
##  
## ----------------------------------------------------------------
##  
###################################################################
## Changelog:
## 24 de septiembre de 2013 -> Inicio 
## 
###################################################################

import os
import pygtk
pygtk.require('2.0')
import gtk
from formularios.utils import enviar_correoe
from widgets import Widgets

class MailSender:
    def __init__(self):
        self.resultado_envio = False    # Inicialmente es así.
        fich_glade = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                  "mail_sender.glade")
        self.wids = Widgets(fich_glade)
        self.wids['ventana'].connect("destroy", gtk.main_quit)
        self.wids['ventana'].connect("delete-event", self.salir)
        self.wids['b_cancelar'].connect("clicked", self.salir, None)
        self.wids['b_aceptar'].connect("clicked", self.enviar)
        # PLAN: No estaría mal que se chequeara si están los campos rellenos 
        # y activar el Aceptar únicamente si los obligatorios lo están.
        self.wids['b_aceptar'].set_sensitive(True)

    def salir(self, boton, evento):
        try:
            self.wids['ventana'].destroy()
        except KeyError:    # La ventana ya se ha destruido. Me olvido ya.
            pass

    def run(self):
        self.wids['ventana'].show_all()
        self.wids['spinner'].stop()
        self.wids['spinner'].set_property("visible", False)
        gtk.main()
        return self.resultado_envio

    def cerrar(self):
        self.resultado_envio = True     # Porque ha cancelado la ventana. 
            # Me da igual si se ha enviado realmente o no; pero no ha fallado.
        self.salir(None, None)

    def set_servidor(self, servidor):
        self.smtpserver = servidor

    def set_usuario(self, smtpusuario):
        self.smtpuser = smtpusuario

    def set_password(self, smtppassword):
        self.smtppwd = smtppassword

    def set_from(self, direccion):
        self.remitente = direccion

    def set_to(self, direccion):
        self.wids['e_para'].set_text(direccion)

    def set_copia(self, copia):
        self.wids['ch_copia'].set_active(copia)
    
    def set_asunto(self, asunto):
        self.wids['e_asunto'].set_text(asunto)

    def set_texto(self, texto):
        self.wids['txt_texto'].get_buffer().set_text(texto)

    def set_adjunto(self, adjunto):
        ruta_adjunto = os.path.abspath(adjunto)
        self.wids['e_adjunto'].set_text(ruta_adjunto)

    def _cargar_remitente(self):
        # TODO: Check y tal...
        return self.remitente

    def _cargar_destinatarios(self):
        para = self.wids['e_para'].get_text()
        paras = para.replace(";", " ").replace(",", " ").split()
        # TODO: Check y tal...
        return paras

    def _cargar_asunto(self):
        asunto = self.wids['e_asunto'].get_text()
        # TODO: Check y tal...
        return asunto

    def _cargar_texto(self):
        buf = self.wids['txt_texto'].get_buffer()
        texto = buf.get_slice(*buf.get_bounds())
        # TODO: Check y tal...
        return texto

    def _cargar_adjuntos(self):
        f = self.wids['e_adjunto'].get_text()
        # TODO: Check y tal...
        return f

    def _get_asunto(self):
        asunto = self.wids['e_asunto'].get_text()
        return asunto

    def _get_texto(self):
        buf = self.wids['txt_texto'].get_buffer()
        texto = buf.get_text(*buf.get_bounds())
        return texto

    def _get_adjuntos(self):
        """
        Devuelve una lista de nombres de fichero para adjuntar.
        """
        txt_adjuntos = self.wids['e_adjunto'].get_text()
        adjuntos = txt_adjuntos.replace(",", " ").replace(";", " ").split()
        return adjuntos
    
    def set_smtpconf(self, servidor, puerto, usuario, contrasenna, ssl = True):
        """
        De momento el puerto y SSL se ignora. Ya se encarga el enviar_correoe 
        de chequear todo eso.
        """
        self.set_servidor(servidor)
        self.set_usuario(usuario)
        self.set_password(contrasenna)

    def enviar(self, boton):
        self.wids['spinner'].start()
        self.wids['spinner'].set_property("visible", True)
        while gtk.events_pending(): gtk.main_iteration(False)
        rte = self._cargar_remitente()
        tos = self._cargar_destinatarios()
        asunto = self._get_asunto()
        texto = self._get_texto()
        adjuntos = self._get_adjuntos()
        servidor = self.smtpserver
        usuario = self.smtpuser
        password = self.smtppwd
        if self.wids['ch_copia'].get_active():
            tos.append(rte)
        # TODO: Esto debería ir en un hilo aparte.
        res = enviar_correoe(rte, tos, asunto, texto, adjuntos, servidor,  
                             usuario, password)
        if res:
            # TODO: PORASQUI: Mostrar ventana de diálogo de OK y devolver True.
            self.resultado_envio = True
            self.wids['b_aceptar'].set_sensitive(False)
            self.wids['b_cancelar'].set_label("Cerrar")
        else:
            # TODO: PORASQUI: Mostrar ventana de diálogo de "lacagaste" y seguir en la ventana.
            self.resultado_envio = False
        self.wids['spinner'].stop()
        self.wids['spinner'].set_property("visible", False)

def main():
    ventana_mail_sender = MailSender()
    ventana_mail_sender.set_from("frbogado@geotexan.com")
    ventana_mail_sender.set_to("informatica@geotexan.com")
    ventana_mail_sender.set_copia(True)
    ventana_mail_sender.set_asunto("Test")
    ventana_mail_sender.set_texto("""She comes in colors ev'rywhere;
She combs her hair
She's like a rainbow
Coming, colors in the air
Oh, everywhere
She comes in colors """)
    ventana_mail_sender.set_adjunto(__file__)
    ventana_mail_sender.set_smtpconf("smtp.googlemail.com", 465, 
                                     "practicas.geotexan@gmail.com", 
                                     "")
    resultado = ventana_mail_sender.run()
    if resultado:
        print "El correo fue enviado correctamente."
    else:
        print "El correo no pudo ser enviado."

if __name__ == "__main__":
    main()

