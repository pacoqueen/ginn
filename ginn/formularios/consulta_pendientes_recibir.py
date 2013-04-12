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
## consulta_pendientes_recibir.py - 
##      Pedidos y restos pendientes de recibir
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, os
import geninformes


class PendientesRecibir(Ventana):
    
    
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        from tempfile import gettempdir
        import os
        import mx, mx.DateTime

        if utils.dialogo(titulo = "EXPORTAR A CSV", 
                         texto="¿Desea exportar una versión CSV del informe?",
                         defecto = "No", 
                         tiempo = 10):
            ruta_csv = os.path.join(gettempdir(), "csv_pdte_recibir_%s.csv" 
                                % mx.DateTime.localtime().strftime("%Y%m%d"))
        else:
            ruta_csv = None

        from formularios import reports as informes
        informes.abrir_pdf(
            geninformes.pendiente_recibir(exportar_a_csv_a = ruta_csv))


if __name__ == '__main__':
    t = PendientesRecibir()    


