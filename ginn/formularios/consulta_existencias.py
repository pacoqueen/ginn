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
## consulta_existencias.py -- 
###################################################################
## NOTAS:
##  
## ----------------------------------------------------------------
##  
###################################################################
## Changelog:
## 16 de marzo de 2006 -> Inicio
###################################################################

import pygtk
pygtk.require('2.0')
import gtk, time, os
from informes import geninformes
import mx.DateTime
from ventana import Ventana
from formularios import utils

class ConsultaExistencias(Ventana):
    
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        from formularios import reports
        import tempfile

        ventana = gtk.Window()  # Es solo para poder mostrar el diálogo de 
                                # progreso.
        res = utils.dialogo(titulo = "FILTRAR EXISTENCIAS NULAS", 
                         texto = "¿Desea filtrar ignorando los productos con"
                                 " existencias a cero?", 
                         cancelar = True, 
                         padre = ventana)
        if res in (gtk.RESPONSE_YES, True):
            func_informe = geninformes.existencias_no_nulas
        elif res in (gtk.RESPONSE_NO, False):
            func_informe = geninformes.existencias
        else:   # res == gtk.RESPONSE_CANCEL:
            return      # Canceló
        res = utils.dialogo(titulo = "EXPORTAR A CSV", 
                texto = "A continuación se generará el informe en PDF.\n"
                        "¿Desa también que se exporte a CSV?", 
                defecto = "No", 
                tiempo = 10, 
                cancelar = True)
        if res in (gtk.RESPONSE_YES, True):
            exportar_a_csv_a = os.path.join(tempfile.gettempdir(), 
                                            "csv_existencias_%s" % (
                                   mx.DateTime.localtime().strftime("%Y%m%d")))
        elif res in (gtk.RESPONSE_NO, False):
            exportar_a_csv_a = None
        else: 
            return      # Canceló
        pdfgenerado = func_informe(exportar_a_csv_a = exportar_a_csv_a, 
                                   ventana_padre = ventana)
        ventana.destroy()
        reports.abrir_pdf(pdfgenerado)

if __name__ == '__main__':
    t = ConsultaExistencias()
 
