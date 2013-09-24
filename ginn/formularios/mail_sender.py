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

import pygtk
pygtk.require('2.0')
import gtk
from formularios.utils import enviar_correoe

class MailSender:
    def __init__(self):
        pass

    def run(self):
        return False

def main():
    ventana_mail_sender = MailSender()
    resultado = ventana_mail_sender.run()
    if resultado:
        print "El correo fue enviado correctamente."
    else:
        print "El correo no pudo ser enviado."

if __name__ == "__main__":
    main()

