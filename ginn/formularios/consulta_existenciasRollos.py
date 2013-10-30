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
## consulta_existenciasRollos.py  
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import time
from framework import pclases
from informes import geninformes
import tempfile
import sys

class ConsultaExistenciasRollos(Ventana):
    
    def __init__(self, objeto = None, usuario = None, gui = True):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        Si `gui` es True, tira de Gtk para preguntar, exportar y abrir los 
        PDF. En otro caso devuelve los nombres de fichero por salida estándar.
        """
        if gui:
            if utils.dialogo(titulo = "¿EXPORTAR A CSV?", 
                        texto = "¿Quiere generar también un archivo CSV por "
                                "cada PDF que se cree a continuación?", 
                        defecto = False, 
                        tiempo = 15):
                csv = True 
                ruta_csv = tempfile.NamedTemporaryFile(suffix = ".csv").name
            else:
                csv = False
        else:
            csv = False
            ruta_csv = None
        ruta_pdf = geninformes.existencias_productos(
            'rollos', 
            "%s, %s" % (utils.str_fecha(time.localtime()), 
                        time.strftime("%H:%M")), 
            ruta_csv = ruta_csv)
        self.fich_generados = [ruta_pdf]
        if gui:
            from formularios import reports
            reports.abrir_pdf(ruta_pdf)
        if pclases.Almacen.select(pclases.Almacen.q.activo==True).count() > 1:
            for a in pclases.Almacen.select(pclases.Almacen.q.activo == True):
                if csv:
                    ruta_csv = tempfile.NamedTemporaryFile(
                        suffix = "_%s.csv" % a.nombre, 
                        delete = False).name
                ruta_pdf = geninformes.existencias_productos('rollos', 
                        "%s, %s" % (
                            utils.str_fecha(time.localtime()), 
                            time.strftime("%H:%M")), 
                        almacen = a, 
                        ruta_csv = ruta_csv)
                self.fich_generados.append(ruta_pdf)
                if gui: 
                    reports.abrir_pdf(ruta_pdf)
        if not gui:
            try:
                sys.stdout.write("\n".join(self.fich_generados))
                sys.stdout.write("\n")
            except IOError:
                pass    # No tengo salida estándar.


if __name__ == '__main__':
    t = ConsultaExistenciasRollos()
    
