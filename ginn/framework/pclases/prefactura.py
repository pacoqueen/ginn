#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2020  Francisco José Rodríguez Bogado                    #
#                          <frbogado@geotexan.com>                            #
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

#########################################################################
## prefactura.py - Clase para las facturas pro-forma.                  ##
#########################################################################

'''
Created on 03/07/2013

@author: bogado
'''

from . import PRPCTOO, starter
from sqlobject import SQLObject, MultipleJoin
from .superfacturaventa import SuperFacturaVenta
from formularios import utils
import datetime

class Prefactura(SQLObject, PRPCTOO, SuperFacturaVenta):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- clienteID = ForeignKey('Cliente')
    servicios = MultipleJoin('Servicio')
    lineasDeVenta = MultipleJoin('LineaDeVenta')
    vencimientosCobro = MultipleJoin('VencimientoCobro')
    cobros = MultipleJoin('Cobro')
    estimacionesCobro = MultipleJoin('EstimacionCobro')
    pagosDeAbono = MultipleJoin('PagoDeAbono')
    comisiones = MultipleJoin('Comision')
    documentos = MultipleJoin('Documento')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        res = "%s - %s; %s" % (self.numfactura,
                self.cliente and self.cliente.nombre or "",
                utils.str_fecha(self.fecha))
        return res

    def DEPRECATED_get_str_estado(self):
        """
        Devuelve el estado de la prefactura como cadena:
        Vacía: No tiene líneas de venta ni servicios.
        Sin vencimientos: No tiene vencimientos creados.
        No vencida: Si alguna fecha de vencimiento < actual.
        Vencida: Si todas las fechas de vencimiento >= actual.
        Cobrada: Si cobros == importe total.
        """
        ESTADOS = ("Vacía", "Sin vencimientos", "No vencida", "Vencida",
                   "Cobrada")
        if len(self.lineasDeVenta) + len(self.servicios) == 0:
            return ESTADOS[0]
        if len(self.vencimientosCobro) == 0:
            return ESTADOS[1]
        ultima_fecha_vto = self.vencimientosCobro[0].fecha
        for v in self.vencimientosCobro:
            if v.fecha > ultima_fecha_vto:
                ultima_fecha_vto = v.fecha
        vencido = sum([v.importe for v in self.vencimientosCobro])
        cobrado = sum([c.importe for c in self.cobros
                    if c.pagareCobro == None or not c.pagareCobro.pendiente])
        if cobrado and cobrado >= vencido:
            return ESTADOS[4]
        else:
            if ultima_fecha_vto < datetime.date.today():
                return ESTADOS[3]
            else:
                return ESTADOS[2]
    def get_next_numfactura(anno = datetime.date.today().year):
        """
        Devuelve el siguiente número de factura del año recibido.
        """
        fras = Prefactura.select(Prefactura.q.fecha >= datetime.date(day=1,
                                                                     month=1,
                                                                     year=anno))
        numfacturas = [fra.get_numero_numfactura() for fra in fras]
        try:
            sig = max(numfacturas) + 1
        except ValueError:
            sig = 1
        return "%s/%s" % (anno, sig)

    get_next_numfactura = staticmethod(get_next_numfactura)

    def get_numero_numfactura_y_anno_from(numfactura):
        partyear, partnum = numfactura.split("/")
        n = int(partnum)
        a = int(partyear)
        assert n > 0
        assert len(str(a)) == 4
        return n, a

    get_numero_numfactura_y_anno_from = staticmethod(get_numero_numfactura_y_anno_from)

    def get_numero_numfactura_from(numfactura):
        return Prefactura.get_numero_numfactura_y_anno_from(numfactura)[0]

    get_numero_numfactura_from = staticmethod(get_numero_numfactura_from)

    def get_numero_numfactura(self):
        """
        Devuelve el número de factura sin prefijo ni
        sufijo y como entero.
        Salta una excepción si no se pudo determinar
        la parte numérica del número de factura.
        Comprueba también la aserción
        año de la fecha de factura = año de numfactura
        """
        numfactura, partyear = Prefactura.get_numero_numfactura_y_anno_from(self.numfactura)
        assert partyear == self.fecha.year
        return numfactura

    def calcular_total_irpf(self, subtotal = None, tot_dto = None, cargo = None, abonos = None):
        """
        Calcula el importe total de retención de IRPF (se resta al total)
        de la factura.
        """
        if subtotal == None:
            subtotal = self.calcular_subtotal()
        if tot_dto == None:
            tot_dto = self.calcular_total_descuento(subtotal)
        if cargo == None:
            cargo = self.cargo
        if abonos == None:
            abonos = sum([pa.importe for pa in self.pagosDeAbono])
        total_irpf = utils.ffloat(subtotal + tot_dto + self.cargo + abonos) * self.irpf
        return total_irpf

    def calcular_subtotal(self):
        """
        Devuelve el subtotal de la factura: líneas de venta + servicios.
        No cuenta abonos, descuento global ni IVA.
        """
        total_ldvs = sum([utils.ffloat((l.cantidad * l.precio) * (1 - l.descuento)) for l in self.lineasDeVenta])
        total_srvs = sum([utils.ffloat((s.precio * s.cantidad) * (1 - s.descuento)) for s in self.servicios])
        subtotal = total_ldvs + total_srvs
        return subtotal
