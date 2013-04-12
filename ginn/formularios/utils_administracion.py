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
## utils_administracion.py - Algunas utilidades para el módulo de 
##                           administración.
###################################################################
## NOTAS:
##  DEPRECATED
## 
###################################################################
## Changelog:
##  14 de octubre de 2005 -> Inicio
## 
###################################################################

raise ImportError, "Este módulo está obsoleto."

import sys


def id_propia_empresa_proveedor():
    """
    Devuelve el id de la propia empresa en la tabla proveedores.
    """
    from pclases import DatosDeLaEmpresa, Proveedor
    try:
        empresa = DatosDeLaEmpresa.select()[0]
    except:
        print "ERROR: No hay datos de la empresa."
        return 0
    try:
        empresa = Proveedor.select(Proveedor.q.nombre == empresa.nombre)[0]
    except:  #IndexError? SQLObjectNotFound?
        print "ERROR: La empresa no está en la tabla de de proveedores."
        return 0
    return empresa.id

def ultimo_pedido_de_venta():
    """
    Devuelve el último número de pedido de venta válido 
    para el año en curso o 0 si no hay pedidos de venta. 
    """
    from framework import pclases
    # Los pedidos de compra son aquellos que tienen como proveedor a 
    # la propia empresa:
    idcliente = id_propia_empresa_cliente()
    try:
        ultimopedido = pclases.PedidoVenta.select(
                pclases.PedidoVenta.q.clienteID == idcliente,
                orderBy="-numpedido")[0]
        ultimonumpedido = ultimopedido.numpedido
    except IndexError:
        # No hay pedidos de venta, así que ultimonumpedido es 0:
        ultimonumpedido = 0
    return ultimonumpedido

def ultimo_numfactura():
    """
    Devuelve el mayor número de factura.
    """
    from framework import pclases
    try:
        fact = pclases.FacturaVenta.select(orderBy = "-numfactura")[0]
    except IndexError:
        return 0
    return fact.numfactura
    
def id_propia_empresa_cliente():
    """
    Devuelve el id de la propia empresa en la tabla clientes.
    """
    from pclases import DatosDeLaEmpresa, Cliente, Auditoria
    try:
        empresa = DatosDeLaEmpresa.select()[0]
    except:
        print "ERROR: No hay datos de la empresa."
        return 0
    try:
        empresa = Cliente.select(Cliente.q.nombre == empresa.nombre)[0]
    except IndexError:  # Pues la creo.
        try:
            empresa = Cliente(nombre = empresa.nombre, 
                              tarifa = None, 
                              contador = None,
                              cliente = None)
            Auditoria.nuevo(empresa, None, __file__)
        except TypeError:   # Me falta algún campo.
            print "utils_administracion.py::id_propia_empresa_cliente -> "\
                  "ERROR: TypeError al crear empresa como cliente."
            return 0
    except:  # ¿SQLObjectNotFound?
        print "utils_administracion.py::id_propia_empresa_cliente -> "\
              "ERROR: La empresa no está en la tabla de clientes."
        return 0
    return empresa.id

def get_albaranes_from_pedido(pedido):
    """
    Devuelve una lista de objetos Albaran que estén
    relacionados con el Pedido "pedido" a través de
    sus LineaDeVenta.
    OJO: Pedidos de venta y albaranes de salida.
    """
    albs = []
    for ldv in pedido.lineasDeVenta:
        if (ldv.albaranSalida != None) and (not ldv.albaranSalida in albs):
            albs.append(ldv.albaran)
    return albs

