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


# DONE: Meter licencia GPL en ficheros.
# DONE: Meter CIF, dirección, etc. en proveedores y clientes.
# DONE: Subir al CVS

__all__ = ['albaransalida', 
           'facturaventa', 
           'lineadeventa', 
           'servicioprestado', 
           'abonoventa', 
           'lineadeabono', 
           'lineadedevolucion', 
           'albaranentrada', 
           'facturacompra', 
           'lineadecompra', 
           'serviciotomado']

import albaransalida, facturaventa, lineadeventa, servicioprestado, \
       abonoventa, lineadeabono, lineadedevolucion, albaranentrada, \
       facturacompra, lineadecompra, serviciotomado
       
def test():
    import sys, os
    os.system("rm /tmp/*.csv")
    if os.path.exists("framework"):
        sys.path.insert(0, os.path.join('SQLObject', 'SQLObject-0.6.1'))
        sys.path.insert(0, os.path.join("framework"))
        sys.path.insert(0, os.path.join("formularios"))
    elif os.path.exists(os.path.join("..", "framework")):
        sys.path.insert(0, os.path.join('..', 'SQLObject', 'SQLObject-0.6.1'))
        sys.path.insert(0, os.path.join("..", "framework"))
        sys.path.insert(0, os.path.join("..", "formularios"))
    import pclases
    albss = pclases.AlbaranSalida.select()[-5:-1]  # @UndefinedVariable
    albss.append(pclases.AlbaranSalida.get(3862))  # @UndefinedVariable
    albaransalida.exportar_a(albss, "/tmp/albaranes_salida.csv")
    for a in albss:
        lineadeventa.exportar_a(a.lineasDeVenta, "/tmp/ldvs_albaranes_salida.csv")
        servicioprestado.exportar_a(a.servicios, "/tmp/ldvs_albaranes_salida.csv")
    frasv = pclases.FacturaVenta.select()[-5:-1]  # @UndefinedVariable
    frasv.append(pclases.FacturaVenta.get(1660))  # @UndefinedVariable
    facturaventa.exportar_a(frasv, "/tmp/facturas_venta.csv")
    for f in frasv:
        lineadeventa.exportar_a(f.lineasDeVenta, "/tmp/ldvs_facturas_venta.csv")
        servicioprestado.exportar_a(f.servicios, "/tmp/ldvs_facturas_venta.csv")
    abonos = pclases.Abono.select()[-6:-1]  # @UndefinedVariable
    abonoventa.exportar_a(abonos, "/tmp/abonos.csv")
    for a in abonos:
        lineadedevolucion.exportar_a(a.lineasDeDevolucion, "/tmp/lineas_abono.csv")
        lineadeabono.exportar_a(a.lineasDeAbono, "/tmp/lineas_abono.csv")
    albse = pclases.AlbaranEntrada.select()[-6:-1]  # @UndefinedVariable
    albaranentrada.exportar_a(albse, "/tmp/albaranes_entrada.csv")
    for a in albse:
        lineadecompra.exportar_a(a.lineasDeCompra, "/tmp/ldcs_albaranes_entrada.csv")
    frasc = pclases.FacturaCompra.select()[-6:-1]  # @UndefinedVariable
    facturacompra.exportar_a(frasc, "/tmp/facturas_compra.csv")
    for f in frasc:
        lineadecompra.exportar_a(f.lineasDeCompra, "/tmp/ldcs_facturas_compra.csv")
        serviciotomado.exportar_a(f.serviciosTomados, "/tmp/ldcs_facturas_compra.csv")

