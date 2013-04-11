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

def exportar_a(albaranes, dest):
    """
    «albaranes» es una lista de albaranes de entrada a exportar. 
    «dest» es un fichero destino donde se guardará la información de los 
    albaranes en formato CSV.
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
    for a in albaranes:
        fila = (a.id, 
                a.numalbaran, 
                a.proveedor and a.proveedor.nombre or "", 
                a.proveedor and a.proveedor.cif or "", 
                a.proveedor and a.proveedor.direccion or "", 
                a.proveedor and a.proveedor.cp or "", 
                a.proveedor and a.proveedor.ciudad or "", 
                a.proveedor and a.proveedor.provincia or "", 
                a.proveedor and a.proveedor.pais or "", 
                a.fecha.strftime("%d/%m/%Y"), 
                a.bloqueado and 1 or 0, # Albarán bloqueado
                # No vuelvo transportista ni destino_id
                a.repuestos and 1 or 0)
        escritor.writerow(fila)
    archivo.close()
    # TODO: Aquí faltaría marcar el albarán como exportado.


