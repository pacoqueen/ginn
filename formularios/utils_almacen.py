#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco Jos� Rodr�guez Bogado,                   #
#                          Diego Mu�oz Escalante.                             #
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
## utils_almacen.py - Utilidades del m�dulo almac�n. 
###################################################################
## NOTAS:
## 
## ----------------------------------------------------------------
## 
###################################################################
## Changelog:
##  4 de octubre de 2005 -> Inicio
## 19 de enero de 2006 -> Fork a v02.
###################################################################

import sys
import time
sys.path.append('../framework')


import pclases, sqlobject, time

def id_propia_empresa_proveedor():
    """
    Devuelve el id de la propia empresa en la tabla proveedores.
    """
    try:
        empresa = pclases.DatosDeLaEmpresa.select()[0]
    except IndexError:
        print "ERROR: No hay datos de la empresa."
        return 0
    try:
        empresa = pclases.Proveedor.select(pclases.Proveedor.q.nombre==empresa.nombre)[0]
    except:  #IndexError? SQLObjectNotFound?
        print "ERROR: La empresa no est� en la tabla de de proveedores."
        return 0
    return empresa.id
  
def id_propia_empresa():
    """
    Devuelve el id de la propia empresa en la tabla clientes.
    """
    try:
        empresa = pclases.DatosDeLaEmpresa.select()[0]
    except IndexError:
        print "ERROR: No hay datos de la empresa."
        return 0
    try:
        empresa = pclases.Cliente.select(pclases.Cliente.q.nombre==empresa.nombre)[0]
    except:  #IndexError? SQLObjectNotFound?
        print "ERROR: La empresa no est� en la tabla de clientes."
        return 0
    return empresa.id

def ultimo_pedido_de_compra_mas_uno():
    """
    Devuelve el �ltimo n�mero de pedido de compra v�lido 
    0 si no hay pedidos de compra. 
    Devuelve el n�mero de pedido como num�rico (aunque en
    realidad sea un str en la BD). 
    No tiene en cuenta aquellos pedidos cuyo n�mero de 
    pedido no se puede interpretar como n�mero y solo 
    tiene en cuenta los pedidos del a�o corriente. 
    El criterio para averiguar el �ltimo n�mero de 
    pedido es la fecha.
    Si el n�mero siguiente al del �ltimo pedido por fecha 
    est� ocupado (no deber�a), sigue sumando 1 hasta que 
    llegue a un n�mero de pedido libre.
    """
    import mx
    from mx.DateTime import localtime as ahora
    strnumspedido = pclases.PedidoCompra._connection.queryAll("SELECT numpedido FROM pedido_compra  WHERE date_part('year', fecha) = %d ORDER BY fecha, numpedido;" % (ahora().year))
    intnumspedido = []
    for numpedido in strnumspedido:
        try:
            intnumspedido.append(int(numpedido[0]))
        except (ValueError, IndexError):
            pass
    if len(intnumspedido) == 0:
        ultimo = 0
    else:
        ultimo = intnumspedido[-1]
    while pclases.PedidoCompra.select(pclases.PedidoCompra.q.numpedido == str(ultimo)).count() != 0:
        ultimo += 1
    return ultimo

def ultimo_numalbaran(venta, interno):
    """
    Devuelve el �ltimo n�mero de albar�n que cumpla
    las condiciones venta==True/False e interno==True/False
    o 0 si no hay ninguno.
    """
    albs = pclases.Albaran.select(sqlobject.AND(pclases.Albaran.q.venta == venta, 
                            pclases.Albaran.q.interno == interno),
                      orderBy="-numalbaran")
    if albs.count() == 0:
        return 0
    return albs[0].numalbaran

def productosConFicha():
    """
    Devuelve una lista de identificadores de productos que tienen ficha de
    producci�n.
    """
    fichas = pclases.FichaDeProduccion.select()
    return [f.idproducto.id for f in fichas]

  
