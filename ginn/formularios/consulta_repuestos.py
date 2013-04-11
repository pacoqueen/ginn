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

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sqlobject, os
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append(os.path.join('..','informes'))
    import geninformes
import mx, mx.DateTime

class ConsultaRepuestos(Ventana):
    
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        import informes, tempfile

        exportar_a_csv_a = None

        if utils.dialogo(titulo = "FILTRAR EXISTENCIAS NULAS", 
                         texto = "¿Desea filtrar ignorando los productos con"
                                 " existencias a cero?"):
            func_informe = geninformes.repuestos_no_nulos
        else:
            func_informe = geninformes.repuestos
        if utils.dialogo(titulo = "EXPORTAR A CSV", 
                         texto = "A continuación se generará el informe en "
                                 "PDF.\n¿Desa también que se exporte a CSV?", 
                         defecto = "No", 
                         tiempo = 10): 
            exportar_a_csv_a = os.path.join(tempfile.gettempdir(), 
                                            "csv_repuestos_%s" % (
                                    mx.DateTime.localtime().strftime("%Y%m%d")))
        pdfs = func_informe(exportar_a_csv_a = exportar_a_csv_a)
        for pdf in pdfs:
            informes.abrir_pdf(pdf)

if __name__ == '__main__':
    t = ConsultaRepuestos()
 
