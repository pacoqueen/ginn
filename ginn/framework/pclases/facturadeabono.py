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

import datetime
from . import PRPCTOO, starter
from sqlobject import SQLObject, MultipleJoin
from .superfacturaventa import SuperFacturaVenta, FRA_COBRADA, \
                              FRA_NO_DOCUMENTADA, FRA_NO_VENCIDA, FRA_ABONO
from formularios import utils

class FacturaDeAbono(SQLObject, PRPCTOO, SuperFacturaVenta):
    class sqlmeta:
        fromDatabase = True
    abonos = MultipleJoin('Abono')
    cobros = MultipleJoin('Cobro')      # Por un lado se puede descontar de un
        # pagaré en forma de cobro con cantidad negativa.
        # En realidad esta relación es 1 a 1.
    pagosDeAbono = MultipleJoin('PagoDeAbono')  # Por otro, si no se ha
        # descontado de un pagaré; es decir, si la factura original
        # ya se cobró; se puede devolver la cantidad del abono mediante
        # pagos de abono.
        # Habrá que tener un método que controle que no se pueda pagar un
        # abono ya descontado.

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_albaranes(self, incluir_nones = False, *args, **kw):
        # El resto de argumentos (*args, **kw) no me importa un carajo, pero
        # los tomo para cumplir la interfaz.
        """
        Devuelve los albaranes DE ENTRADA de abono relacionados con la
        factura de abono.
        """
        albaranes = []
        abono = self.abono
        for ldd in abono.lineasDeDevolucion:
            if not incluir_nones:
                if (ldd.albaranDeEntradaDeAbonoID
                    and ldd.albaranDeEntradaDeAbono not in albaranes):
                    albaranes.append(ldd.albaranDeEntradaDeAbono)
            else:
                if ldd.albaranDeEntradaDeAbonoID not in albaranes:
                    albaranes.append(ldd.albaranDeEntradaDeAbono)

    def get_pedidos(self, incluir_nones = False):
        """
        Devuelve una lista vacía. No hay pedidos para abonos.
        """
        # Pero he de implementarlo para respetar la "interfaz" de la clase.
        return []

    def get_abono(self):
        """
        Devuelve el primero de los abonos relacionados con la
        factura de abono o None si no tiene.
        La relación en realidad es 1 a 1, por lo que se ignorará
        el resto de los abonos si hubiera más de 1.
        """
        if len(self.abonos) == 0:
            return None
        return self.abonos[0]

    def get_abono_id(self):
        """
        Devuelve el ID del abono relacionado o None
        si no tiene abono relacionado.
        Al contrario que con los atributos (o propiedades) de los
        "legacy" SQLObjects, aquí es más lento -un poco solo-
        acceder al «otrocampoID» en lugar de a «otrocampo» directamente.
        """
        abono = self.abono
        if abono != None:
            return abono.id
        return None

    abono = property(get_abono, doc = get_abono.__doc__)
    abonoID = property(get_abono_id, doc = get_abono_id.__doc__)

    def get_obra(self):
        """
        Devuelve la obra relacionada con la factura de abono a través del
        abono en sí.
        """
        return self.abono.obra

    def get_obra_id(self):
        """
        Devuelve la obra relacionada con la factura de abono a través del
        abono en sí.
        """
        return self.abono.obraID

    obra = property(get_obra, doc = get_obra.__doc__)
    obraID = property(get_obra_id, doc = get_obra_id.__doc__)

    def get_numfactura(self):
        """
        Devuelve el número de factura que le correspondería
        a esta factura de abono. Es el mismo que el número
        del abono al que está relacionado.
        Devuelve la cadena vacía si no tiene relación con
        ningún abono.
        """
        if self.abono != None:
            return self.abono.numabono
        return ""

    numfactura = property(get_numfactura, doc = get_numfactura.__doc__)

    def get_iva(self):
        """
        Devuelve el IVA de la factura de abono.
        Siempre será el IVA del cliente.
        En caso de error devuelve 0.21.
        """
        try:
            iva = self.cliente.get_iva_norm(fecha = self.fecha)
        except:
            iva = 0.21
        #for abono in self.abonos:
        #    if abono.clienteID != None:
        #        # OJO: La fecha para ver el IVA que le corresponde es la de
        #        # la factura de abono, no la de los abonos en sí. Es el mismo
        #        # criterio que con pedidos, albaranes y facturas.
        #        iva = abono.cliente.get_iva_norm(fecha = self.fecha)
        #        break
        return iva

    def set_iva(self, iva):
        """
        Hace que el IVA de la factura de abono sea el
        recibido como parámetro.
        OJO: Para ello cambia el IVA del cliente al que
        pertenecen los abonos de la factura de abono.
        """
        iva = float(iva)
            # La excepción ValueError si el parámetro no se puede convertir a
            # float dejo que la atienda el invocador.
        if iva > 1:
            iva /= 100.0
        if iva < 0:
            iva *= -1
        for abono in self.abonos:
            if abono.clienteID != None:
                abono.cliente.iva = iva # * 100.0
                    # DONE: OJO: Esto es solo hasta que estandarice los
                    # IVA y se guarden todos como fracción de la unidad.
                break

    iva = property(get_iva, set_iva, "IVA aplicado a la factura de abono")

    def calcular_importe_total(self, iva_incluido = True):
        """
        Calcula y devuelve el importe total de la factura de abono.
        Incluye el IVA por defecto del cliente.
        """
        total = 0
        for abono in self.abonos:
            total += abono.importeSinIva
        if iva_incluido:
            total *= (1 + self.iva)
        return total

    importeTotal = property(calcular_importe_total,
                            doc = calcular_importe_total.__doc__)

    def calcular_total(self):
        return self.calcular_importe_total(iva_incluido = True)

    def calcular_base_imponible(self):
        return self.calcular_importe_total(iva_incluido = False)

    def calcular_total_descuento(self, *args, **kw):
        """
        No hay descuentos en abonos.
        """
        return 0.0

    def calcular_total_iva(self, *args, **kw):
        return sum([abono.importeSinIva for abono in self.abonos]) * self.iva

    def emparejar_vencimientos(self):
        """
        Por compatibilidad con facturas de venta.
        Devuelve los cobros en un diccionario con el formato
        del emparejar_vencimientos de FacturaVenta (ver __doc__
        de éste).
        Como las facturas de abono no tienen vencimiento, se usará
        la fecha de la factura como fecha de vencimiento.
        """
        res = {}
        cbrs = self.cobros[:]
        cbrs.sort(utils.cmp_fecha_id)
        class FakeVto:
            ide = 0; facturaVentaID = self.id; facturaVenta = self; prefacturaID = None; prefactura = None; fecha = self.fecha; importe = self.importeTotal; observaciones = "Vencimiento ficticio de la factura de abono."
            def get_factura_o_prefactura(self):
                return self.facturaVenta
        vtos = [FakeVto()]
        res['vtos'] = vtos[:]
        res['cbrs'] = cbrs[:]
        for vto in vtos:
            try:
                cbr = cbrs.pop()
            except IndexError:
                res[vto] = []
            else:
                res[vto] = [cbr]
        if cbrs != []:
            res[None] = cbrs
        return res

    vencimientosCobro = property(
        lambda yomismo: yomismo.emparejar_vencimientos()['vtos'])

    def calcular_beneficio(self):
        """
        Devuelve una cantidad en negativo que representa el beneficio que se
        ha anulado con esta devolución o ajuste de precio.
        """
        res = 0.0
        for ldd in self.abono.lineasDeDevolucion:
            res += ldd.calcular_beneficio()
        for lda in self.abono.lineasDeAbono:
            res += lda.calcular_beneficio()
        return res

    def get_cliente(self):
        """
        Devuelve el cliente de la factura de abono, que lo
        extrae del abono al que pertenece.
        """
        return self.abono and self.abono.cliente or None

    def get_clienteID(self):
        cliente = self.get_cliente()
        return cliente and cliente.id or None

    cliente = property(get_cliente, doc = get_cliente.__doc__)
    clienteID = property(get_clienteID)

    # 20100927: Nueva clasificación de facturas:
    def get_estado(self, fecha = datetime.date.today()):
        """
        Devuelve el estado de la factura de abono:
        0: No documentada ni vencida: Ningún documento de pago relacionado.
           FRA_NO_DOCUMENTADA
        1: Documentada no vencida: Tiene documento de pago y éste todavía
                                   no ha vencido. Se toma en cuenta la fecha
                                   de vencimiento del doc. de pago, no la de
                                   la factura.
           FRA_NO_VENCIDA
        2: Impagada: Los vencimientos de la factura han cumplido y no se ha
                     cobrado, con o sin documento de pago de por medio.
           FRA_IMPAGADA
        3: Cobrada: Toda la factura está cobrada.
           FRA_COBRADA
        4: Pendiente de abonar: Así estarán todos los abonos antes de
                                descontarlos en un cobro o en un nuevo pedido.
                                No contarán para el cálculo del crédito.
           FRA_ABONO
        Para que una factura esté en un estado, todos los vencimientos de la
        misma deben estar en ese estado.
        """
        # Cobrada por completo:
        # Todos los vencimientos tienen un cobro y ese cobro:
        #  - No es pagaré ni confirming.
        #  - O bien, es pagaré o confirming y no están pendientes.
        cobrado = 0.0
        for c in self.cobros:
            if c.confirmingID:
                if not c.confirming.pendiente:
                    cobrado += c.importe
            elif c.pagareCobroID:
                if not c.pagareCobro.pendiente:
                    cobrado += c.importe
            else:
                cobrado += c.importe
        if round(cobrado, 2) == round(self.calcular_total(), 2):
            return FRA_COBRADA
        # No documentada (ni pagarés, ni confirmings; o bien ningún cobro en
        # absoluto).
        docs_pago = [c for c in self.cobros
                     if c.pagareCobroID or c.confirmingID]
        if (not docs_pago or not self.cobros) and not self.esta_vencida():
            return FRA_NO_DOCUMENTADA
        # Documentada con ningún vencimiento cumplido.
        # Solo miro si los vencimientos no han cumplido. Da igual que tengan
        # documento de cobro o no; porque si no ha entrado en NO_DOCUMENTADA
        # ni en COBRADA es que está documentada, aunque solo tenga uno para
        # over nine thousands de vencimientos.
        cumplidos = []
        for v in self.vencimientosCobro:
            try:    # Última fecha de vencimiento (si hubiera varias) del
                    # pagaré o confirmig relacionado con el vencimiento.
                cobro = v.facturaVenta.emparejar_vencimientos()[v][-1]
                try:
                    fecha_vto = cobro.pagareCobro.fechaVencimiento
                except AttributeError:
                    fecha_vto = cobro.confirming.fechaVencimiento
            except (IndexError, KeyError, AttributeError):
                fecha_vto = v.fecha
            if fecha_vto <= fecha:
                cumplidos.append(v)
        if not cumplidos:
            return FRA_NO_VENCIDA
        # Impagada.
        # Si no es nada de lo anterior, está impagada.
        else:
            #return FRA_IMPAGADA
            return FRA_ABONO

    def calcular_importe_pendiente_de_abonar(self):
        """
        Devuelve el importe (c/IVA) pendiente de abonar de la factura de abono.
        El importe abonado es la suma de los cobros relacionados con la
        factura de abono (viene en negativo por ser un "pago" en forma de
        descuento de un cobro) y de los pagos de abono asociados a nuevas
        facturas del cliente. En cuyo caso el importe ya se ha descontado de
        una venta, que puede o no haber sido cobrada ya, pero que en todo
        caso no puedo permitir que vuelva a descontarse de otro cobro.
        """
        abonado = 0.0
        for c in self.cobros:
            abonado += c.importe
        for p in self.pagosDeAbono:
            abonado += p.importe    # Esté o no pendiente (p.pendiente) de
                                    # cobrarse la facturaVenta asociada.
        pdte = round(self.importeTotal - abonado, 2)
        return pdte

