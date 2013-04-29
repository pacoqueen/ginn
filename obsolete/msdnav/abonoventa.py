#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado                    #
#                          (pacoqueen@users.sourceforge.net)                  #
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


import csv

def exportar_a(abonos, dest):
    """
    «abonos» es una lista de abonos a exportar. 
    «dest» es un fichero destino donde se guardará la información de los 
    abonos en formato CSV.
    Solo guarda los datos del albarán, no el contenido.
    """
    if not dest.endswith(".csv"):
        dest += ".csv"
    archivo = open(dest, "a")
    # No capturo IOError porque no sé cómo corregir el error. Que lo decida 
    # el usuario cuando avise de la excepción en la capa superior.
    escritor = csv.writer(archivo, 
                          delimiter = ";", 
                          lineterminator = "\n")
    for a in abonos:
        fila = (a.id, 
                a.numabono, 
                a.cliente and a.cliente.nombre or "", 
                a.cliente and a.cliente.cif or "", 
                a.cliente and a.cliente.direccion or "", 
                a.cliente and a.cliente.cp or "", 
                a.cliente and a.cliente.ciudad or "", 
                a.cliente and a.cliente.provincia or "", 
                a.cliente and a.cliente.pais or "", 
                a.fecha.strftime("%d/%m/%Y"), 
               )
        escritor.writerow(fila)
    archivo.close()
    # TODO: Aquí faltaría marcarlo como exportado.


