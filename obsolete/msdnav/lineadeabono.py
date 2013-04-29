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
from lineadeventa import get_puid

def exportar_a(lineasdeajuste, dest):
    """
    «lineasdeajuste» es una lista de lineasdeajuste a exportar. 
    «dest» es un fichero destino donde se guardará la información de los 
    lineasdeajuste en formato CSV.
    """
    if not dest.endswith(".csv"):
        dest += ".csv"
    archivo = open(dest, "a")
    # No capturo IOError porque no sé cómo corregir el error. Que lo decida 
    # el usuario cuando avise de la excepción en la capa superior.
    escritor = csv.writer(archivo, 
                          delimiter = ";", 
                          lineterminator = "\n")
    for lda in lineasdeajuste:
        puid = get_puid(lda.producto)
        if not puid:
            puid = get_puid(lda.servicio)
        subtotal = lda.diferencia * lda.cantidad
        fila = (lda.id,
                lda.abonoID, 
                puid, 
                lda.producto and lda.producto.codigo or "", 
                lda.producto and lda.producto.descripcion or lda.servicio.concepto, 
                subtotal, 
                )
        escritor.writerow(fila)
    archivo.close()
    # TODO: Aquí faltaría marcar el albarán como exportado.


