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
import sys, os
#print os.path.abspath(os.path.curdir)
from framework import pclases

def get_puid(prod_o_servicio):
    """
    Devuelve el ID encabezado por un texto relacionado con el tipo de objeto 
    recibido.
    Si recibe None, devuelve la cadena vacía.
    """
    res = ""
    if prod_o_servicio:
        if isinstance(prod_o_servicio, pclases.Servicio):  # @UndefinedVariable
            res = "SP:%d" % prod_o_servicio.id
        elif isinstance(prod_o_servicio, pclases.ServicioTomado):  # @UndefinedVariable
            res = "ST:%d" % prod_o_servicio.id
        else:
            res = prod_o_servicio.get_puid()
    return res

def exportar_a(lineasdeventa, dest):
    """
    «lineasdeventa» es una lista de lineasdeventa a exportar. 
    «dest» es un fichero destino donde se guardará la información de los 
    lineasdeventa en formato CSV.
    """
    if not dest.endswith(".csv"):
        dest += ".csv"
    archivo = open(dest, "a")
    # No capturo IOError porque no sé cómo corregir el error. Que lo decida 
    # el usuario cuando avise de la excepción en la capa superior.
    escritor = csv.writer(archivo, 
                          delimiter = ";", 
                          lineterminator = "\n")
    for ldv in lineasdeventa:
        puid = get_puid(ldv.producto)
        if not puid:
            puid = get_puid(ldv.servicio)
        fila = (ldv.id, 
                ldv.albaranSalidaID, 
                ldv.facturaVentaID, 
                puid, 
                ldv.producto and ldv.producto.codigo or "", 
                ldv.producto and ldv.producto.descripcion or ldv.servicio.concepto, 
                ldv.get_subtotal(iva = False), 
                )
        escritor.writerow(fila)
    archivo.close()
    # TODO: Aquí faltaría marcar como exportado.


