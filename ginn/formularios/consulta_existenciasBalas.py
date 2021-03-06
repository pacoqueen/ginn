#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2020  Francisco José Rodríguez Bogado,                   #
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

"""
consulta_existenciasBalas.py - Imprime existencias de fibra.
----------------------------------------------------------------
NOTAS:

"""
###################################################################
# Changelog:
# 16 de marzo de 2006 -> Inicio
###################################################################

import pygtk
pygtk.require('2.0')
import time
import tempfile
from ventana import Ventana
from formularios import utils
from framework import pclases
from informes import geninformes
from formularios import reports

class ConsultaExistenciasBalas(Ventana):

    def __init__(self, objeto=None, usuario=None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        # En vez de marear al usuario, directamente intento atacar Murano.
        # Si no puedo, busco solo en ginn. Si los resultados no coinciden
        # con lo que esperaba el usuario, que le faquen. Debería haber ido
        # a Murano desde el principio.
        try:
            from api import murano
            conexion = murano.connection.Connection()
            info = ".".join(conexion.__repr__().split(".")[:2])
            info += "> "
            reports.abrir_pdf(
                geninformes.existencias_fibra_por_lote(
                    "{} - {}, {}".format(info,
                                         utils.str_fecha(time.localtime()),
                                         time.strftime("%H:%M")),
                    external_api=conexion))
        except:
            # Si tengo conexión a Murano, me olvido de los informes obsoletos.
            # Si no, recurro a ellos. Nunca se sabe si volveremos al viejo ginn
            if utils.dialogo(titulo="¿EXPORTAR A CSV?",
                             texto="¿Quiere generar también un archivo CSV por"
                                   " cada almacén?",
                             defecto=False,
                             tiempo=15):
                csv = True
                ruta_csv = tempfile.NamedTemporaryFile(suffix=".csv").name
            else:
                csv = False
                ruta_csv = None
            reports.abrir_pdf(geninformes.existencias_productos(
                'balas',
                "%s, %s" % (utils.str_fecha(time.localtime()),
                            time.strftime("%H:%M")),
                ruta_csv=ruta_csv))
            if pclases.Almacen.select(pclases.Almacen.q.activo==True).count() > 1:
                for a in pclases.Almacen.select(pclases.Almacen.q.activo==True):
                    if csv:
                        ruta_csv = tempfile.NamedTemporaryFile(
                            suffix="_%s.csv" % a.nombre,
                            delete=False).name
                    reports.abrir_pdf(
                        geninformes.existencias_productos(
                            'balas',
                            "%s, %s" % (
                                utils.str_fecha(time.localtime()),
                                time.strftime("%H:%M")),
                            almacen=a,
                            ruta_csv=ruta_csv))
            if utils.dialogo(titulo="¿IMPRIMIR DESGLOSE?",
                             texto="¿Desea imprimir un desglose por lote de la"
                                   " fibra en almacén?      \n\nNOTA: Puede "
                                   "tardar algún tiempo.",
                             defecto="No"):
                reports.abrir_pdf(
                    geninformes.existencias_fibra_por_lote("%s, %s" % (
                        utils.str_fecha(time.localtime()),
                        time.strftime("%H:%M"))))


if __name__ == '__main__':
    t = ConsultaExistenciasBalas()
