#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2013  Francisco José Rodríguez Bogado                    #
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
## superfacturaventa.py - Clase base para todas las facturas de venta. ##
#########################################################################

from . import VERBOSE, VencimientoCobro, DocumentoDePago
import mx.DateTime
from formularios import utils
import re

# "Macros/constantes" de tipos de facturas:
FRA_NO_DOCUMENTADA,FRA_NO_VENCIDA,FRA_IMPAGADA,FRA_COBRADA,FRA_ABONO = range(5)

class SuperFacturaVenta:
    """
    Superclase para las facturas de venta y prefacturas.
    """

    def calcular_vencido(self, fecha_base = mx.DateTime.today()):
        """
        Devuelve el importe vencido[1] de la factura en la fecha recibida.
        Por defecto se usa la fecha del sistema.

        [1] Cobrado o no, da igual.
        """
        from facturadeabono import FacturaDeAbono
        if isinstance(self, FacturaDeAbono):
            # Las facturas de abono no tienen vencimientos, solo "cobros" que 
            # se relacionan con otros efectos de cobro. "So", el importe habrá 
            # vencido si la fecha es superior a la del abono.
            if self.fecha <= fecha_base:
                vencido = self.importeTotal
            else:
                vencido = 0.0
        else:
            vencido = sum([vto.importe for vto in self.vencimientosCobro 
                            if vto.fecha <= fecha_base])
        # ¿OPTIMIZACIÓN?: 
        #try:
        #    _vencido = FacturaVenta._connection.queryOne("""
        #        SELECT SUM(importe)
        #          FROM vencimiento_cobro
        #          WHERE fecha <= '%s' AND factura_venta_id = %d;
        #        """ % (fecha_base.strftime("%Y-%m-%d"), self.id))[0];
        #    if _vencido == None:
        #        raise TypeError
        #except (IndexError, TypeError):
        #    _vencido = 0.0
        #assert vencido == _vencido, "%s %s" % (vencido, _vencido)
        return vencido
        #return _vencido

    def esta_vencida(self):
        """
        Devuelve True si _todos_ los vencimientos de la factura se han pasado.
        """
        vencida = True
        for vto in self.vencimientosCobro:
            if vto.fecha > mx.DateTime.localtime():
                vencida = False
                break 
                # Tiene un vto. que no ha llegado. Me la salto.
        return vencida

    def get_albaranes(self, incluir_nones = False, incluir_servicios = False):
        """
        Devuelve los objetos albarán que están relacionados 
        con la factura a través de sus líneas de venta.
        """
        albaranes = []
        for ldv in self.lineasDeVenta:
            if not incluir_nones:
                if ldv.albaranSalidaID and ldv.albaranSalida not in albaranes:
                    albaranes.append(ldv.albaranSalida)
            else:
                if ldv.albaranSalida not in albaranes:
                    albaranes.append(ldv.albaranSalida)
        if incluir_servicios:
            for srv in self.servicios:
                if not incluir_nones:
                    if srv.albaranSalidaID and srv.albaranSalida not in albaranes:
                        albaranes.append(srv.albaranSalida)
                else:
                    if srv.albaranSalida not in albaranes:
                        albaranes.append(srv.albaranSalida)
        return albaranes

    def get_pedidos(self, incluir_nones = False):
        """
        Devuelve los objetos PedidoVenta que están relacionados 
        con la factura a través de sus líneas de venta.
        """
        pedidos = []
        for ldv in self.lineasDeVenta:
            if not incluir_nones:
                if ldv.pedidoVentaID and ldv.pedidoVenta not in pedidos:
                    pedidos.append(ldv.pedidoVenta)
            else:
                if ldv.pedidoVenta not in pedidos:
                    pedidos.append(ldv.pedidoVenta)
        for srv in self.servicios:
            pedido = srv.pedidoVenta
            if not incluir_nones:
                if pedido and pedido not in pedidos:
                    pedidos.append(pedido)
            else:
                if pedido not in pedidos:
                    pedidos.append(pedido)
        return pedidos

    def calcular_total(self, iva = True):
        """
        Calcula el total de la factura, con descuentos, IVA y demás incluido.
        Devuelve un FixedPoint (a casi todos los efectos, se comporta como 
        un FLOAT. De todas formas, pasa bien por el utils.float2str).
        """
        subtotal = self.calcular_subtotal() 
        tot_dto = self.calcular_total_descuento(subtotal) 
        abonos = sum([pa.importe for pa in self.pagosDeAbono])
        if iva:
            tot_iva = self.calcular_total_iva(subtotal, tot_dto, self.cargo, abonos)
        else:
            tot_iva = 0.0
        irpf = self.irpf * subtotal
        total = subtotal+float(self.cargo)+tot_dto+tot_iva+abonos+irpf
        return total
    
    def calcular_importe_total(self, iva = True):
        """
        Calcula y devuelve el importe total, incluyendo IVA (por defecto), 
        de la factura.
        """
        return self.calcular_total()
        # NOTA: Método "duplicado" por error. Funciona mejor el «calcular_total» porque no comete "errores" de redondeo.
        #total = 0
        #for ldv in self.lineasDeVenta:
        #    total += ldv.get_subtotal(iva = False)
        #for s in self.servicios:
        #    total += s.get_subtotal(iva = False)
        #for pda in self.pagosDeAbono:
        #    total += pda.importe 
        #total += self.cargo
        #total *= (1 - self.descuento)
        #total *= (1 + self.iva)
        #return total

    importeTotal = property(calcular_importe_total, 
                            doc = calcular_importe_total.__doc__)

    def calcular_total_descuento(self, subtotal = None):
        """
        Calcula el total del descuento global.
        """
        if subtotal == None:
            subtotal = self.calcular_subtotal()
        tot_dto = utils.ffloat(-1 * (subtotal + float(self.cargo)) 
                               * self.descuento)
        return tot_dto

    def calcular_total_iva(self, subtotal = None, tot_dto = None, 
                           cargo = None, abonos = None):
        """
        Calcula el importe total de IVA de la factura.
        """
        if subtotal == None:
            subtotal = self.calcular_subtotal()
        if tot_dto == None: 
            tot_dto = self.calcular_total_descuento(subtotal)
        if cargo == None:
            cargo = self.cargo
        if abonos == None:
            abonos = sum([pa.importe for pa in self.pagosDeAbono])
        total_iva = utils.ffloat(subtotal + tot_dto + self.cargo + abonos) * self.iva 
        return total_iva
    
    def emparejar_vencimientos(self):
        """
        Devuelve un diccionario con los vencimientos y cobros de la factura 
        emparejados.
        El diccionario es de la forma:
        {vencimiento1: [cobro1], 
         vencimiento2: [cobro2], 
         vencimiento3: [], 
         'vtos': [vencimiento1, vencimiento2, vencimiento3...], 
         'cbrs': [cobro1, cobro2]}
        Si tuviese más cobros que vencimientos, entonces se devolvería un diccionario tal que:
        {vencimiento1: [cobro1], 
         vencimiento2: [cobro2],
         None: [cobro3, cobro4...], 
         'vtos': [vencimiento1, vencimiento2], 
         'cbrs': [cobro1, cobro2, cobro3, cobro4...]}
        'vtos' y 'cbrs' son copias ordenadas de las listas de vencimientos y cobros.
        El algoritmo para hacerlo es:
        1.- Construyo el diccionario con todos los vencimientos.
        2.- Construyo una lista auxiliar con los cobros ordenados por fecha.
        3.- Recorro el diccionario de vencimientos por orden de fecha.
            3.1.- Saco y asigno el primer cobro de la lista al vencimiento tratado en la iteración.
            3.2.- Si no quedan vencimientos por asignar, creo una clave None y agrego los cobros restantes.
        """
        res = {}
        cbrs = self.cobros[:]
        cbrs.sort(utils.cmp_fecha_id)
        vtos = self.vencimientosCobro[:]
        vtos.sort(utils.cmp_fecha_id)
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

    def calcular_beneficio(self):
        """
        Devuelve la suma de los beneficios por línea de venta.
        El beneficio de un servicio es el precio total del servicio.
        El beneficio de una LDV es el (PVP - IVA) * porcentaje_tarifa * cantidad.
        """
        tot = 0.0
        for srv in self.servicios:
            tot += srv.calcular_beneficio()
        for ldv in self.lineasDeVenta:
            ben = ldv.calcular_beneficio()
            tot += ben
        return tot

    def calcular_pendiente_cobro(self):
        """
        Devuelve el importe pendiente de cobro de la factura.
        Se considera pendiente de cobro a la diferencia entre 
        el total cobrado y el total de los vencimientos, *independientemente
        del importe total de la factura*. Es indispensable, por tanto, 
        que el importe total de la factura coincida con el total 
        de vencimientos.
        Aunque si no fuera así -por un cambio en las LDVs 
        involuntario, error o borrado- no afectaría a la 
        parte financiera si los vencimientos están correctamente 
        creados.
        """
        totvtos = sum([v.importe for v in self.vencimientosCobro])
        totcbrs = self.calcular_cobrado()
        return totvtos - totcbrs

    def calcular_cobrado(self, fecha_base = None):
        """
        Devueve el importe total cobrado de la factura hasta la fecha recibida.
        Si no se pasa una fecha, se devuelve el total cobrado (sumatorio de 
        los importes de todos los cobros relacionados).
        """
        if fecha_base is None:
            # Un cobro cobrado, valga la redundancia, es un cobro que se ha 
            # hecho efectivo, es decir, un pagaré/cheque con fecha no 
            # vencida(*) o con fecha vencida pero marcado como cobrado, 
            # un confirming(*), un pago en efectivo o por transferencia, etc...
            # (*) Una promesa de pago cuenta para mí como un cobro aunque 
            # todavía no tenga las pelas en el bolsillo.
            cobros_cobrados = [c for c in self.cobros 
                                if c.esta_cobrado()]
                                #if not c.sync() and c.esta_cobrado()]
            # UGLY HACK: sync() siempre devuelve None, por eso le pongo el 
            # not. Así fuerzo a sincronizar los valores antes de comprobar 
            # si está cobrado. 
            # UPDATE: [20130627] Ya no es necesario el sync. Con la 
            # optimización de esta_cobrado ejecuto una stored en el SGBD.
        else:
            cobros_cobrados = [c for c in self.cobros 
                                if c.fecha <= fecha_base and 
                                   c.esta_cobrado(fecha_base)]
        res = sum([c.importe for c in cobros_cobrados])
        return res

    def calcular_pendiente_de_documento_de_pago(self):
        """
        Devuelve la cantidad de la factura pendiente de cubrir por un 
        documento de pago, vencido o no, o por un cobro.
        OJO: Calcula la diferencia en base al total de los vencimientos, 
        independientemente del total de la factura. Una factura sin 
        vencimientos no sabemos cómo se cobra, por tanto nos da igual si 
        tiene o no documentos de pago, y por tanto aquí devolverá un cero 
        como un castillo como en el que vivo con tu madre.
        Cartón de leche, pijama de lino.
        """
        cobros = sum([c.importe for c in self.cobros])
        total_vencimientos = sum([v.importe for v in self.vencimientosCobro])
        res = total_vencimientos - cobros
        return res

    def __dividir_por_comercial(self, func_a_evaluar_en_lineas_as_str, 
                                *args, **kw):
        """
        Divide el resultado que devuelva la función «func_a_evaluar_en_lineas» 
        aplicada a las líneas de venta, servicio, de abono, etc.
        """
        from facturaventa import FacturaVenta
        from facturadeabono import FacturaDeAbono
        from prefactura import Prefactura
        comerciales = {None: 0.0}   # Al menos siempre debe quedar None con 0
                                    # aunque no tenga eledeuves ni servicios.
        totalregladetres = 0.0
        if isinstance(self, (FacturaVenta, Prefactura)):
            lineas = self.lineasDeVenta + self.servicios
        elif isinstance(self, FacturaDeAbono):
            try:
                lineas=self.abono.lineasDeAbono+self.abono.lineasDeDevolucion
            except AttributeError:
                # ¿Factura de abono sin abono? Puede ser... Raro, pero posible.
                lineas = []
        else:
            raise TypeError
        for srv_o_ldv in lineas:
            subtotal = getattr(srv_o_ldv, 
                               func_a_evaluar_en_lineas_as_str)(*args, **kw)
            totalregladetres += subtotal    # Alias cuenta de la vieja.
            try:
                comerciales[srv_o_ldv.comercial] += subtotal 
            except KeyError:
                comerciales[srv_o_ldv.comercial] = subtotal
        totalfactura = self.calcular_total()  # Con IVA, descuentos y de todo.
        res = {}
        for comercial in comerciales:
            try:
                res[comercial] = (comerciales[comercial] / totalregladetres
                                  * totalfactura)
            except ZeroDivisionError:
                res[comercial] = 0.0
        return res

    def __dividir_por_proveedor(self, func_a_evaluar_en_lineas_as_str, 
                                *args, **kw):
        """
        Divide el resultado que devuelva la función «func_a_evaluar_en_lineas» 
        aplicada a las líneas de venta, servicio, de abono, etc.
        """
        from facturaventa import FacturaVenta
        from facturadeabono import FacturaDeAbono
        from prefactura import Prefactura
        proveedores = {None: 0.0}   # Al menos siempre debe quedar None con 0
                                    # aunque no tenga eledeuves ni servicios.
        totalregladetres = 0.0
        if isinstance(self, (FacturaVenta, Prefactura)):
            lineas = self.lineasDeVenta + self.servicios
        elif isinstance(self, FacturaDeAbono):
            try:
                lineas=self.abono.lineasDeAbono+self.abono.lineasDeDevolucion
            except AttributeError:
                # ¿Factura de abono sin abono? Puede ser... Raro, pero posible.
                lineas = []
        else:
            raise TypeError
        for srv_o_ldv in lineas:
            subtotal = getattr(srv_o_ldv, 
                               func_a_evaluar_en_lineas_as_str)(*args, **kw)
            totalregladetres += subtotal    # Alias cuenta de la vieja.
            try:
                proveedores[srv_o_ldv.proveedor] += subtotal 
            except KeyError:
                proveedores[srv_o_ldv.proveedor] = subtotal
        totalfactura = self.calcular_total()  # Con IVA, descuentos y de todo.
        res = {}
        for proveedor in proveedores:
            try:
                res[proveedor] = (proveedores[proveedor] / totalregladetres
                                  * totalfactura)
            except ZeroDivisionError:
                res[proveedor] = 0.0
        return res
 
    def dividir_total_por_comercial(self):
        """
        Devuelve el total de la factura en euros dividido por comercial en 
        función de los importes de las líneas de venta que componen la factura 
        pertenecientes a cada comercial (relacionados a través del pedido, 
        pero esos detalles van en otra clase. Máxima cohesión, mínima 
        dependencia).
        """
        res = self.__dividir_por_comercial("calcular_subtotal", iva = False)
        return res
   
    def dividir_beneficio_por_comercial(self):
        """
        Hace lo mismo que el método de dividir el total de la factura por 
        comercial, solo que en este caso calcula el beneficio aportado por 
        las ventas del comercial.
        """
        # Esto es un as que me guardo en la manga.
        res = self.__dividir_por_comercial("calcular_beneficio")
        return res

    def dividir_total_por_proveedor(self):
        """
        Devuelve el total de la factura en euros dividido por comercial en 
        función de los importes de las líneas de venta que componen la factura 
        pertenecientes a cada comercial (relacionados a través del pedido, 
        pero esos detalles van en otra clase. Máxima cohesión, mínima 
        dependencia).
        """
        res = self.__dividir_por_proveedor("calcular_subtotal", iva = False)
        return res
   
    def dividir_beneficio_por_proveedor(self):
        """
        Hace lo mismo que el método de dividir el total de la factura por 
        comercial, solo que en este caso calcula el beneficio aportado por 
        las ventas del comercial.
        """
        # Esto es un as que me guardo en la manga.
        res = self.__dividir_por_proveedor("calcular_beneficio")
        return res

    def get_comerciales(self):
        """
        Devuelve los comerciales de la factura relacionados a través de 
        los pedidos.
        """
        comerciales = []
        for p in self.get_pedidos():
            comercial = p.comercial
            if comercial != None and comercial not in comerciales:
                comerciales.append(comercial)
        return tuple(comerciales)

    def get_proveedores(self):
        """
        Devuelve los comerciales de la factura relacionados a través de 
        los productos.
        """
        proveedores = []
        try:
            for ldv in self.lineasDeVenta:
                proveedor = ldv.producto.proveedor
                if proveedor != None and proveedor not in proveedores:
                    proveedores.append(proveedor)
        except AttributeError:
            pass    # No es factura de venta ni prefactura.
        try:
            for ldc in self.lineasDeCompra:
                proveedor = ldc.producto.proveedor
                if proveedor != None and proveedor not in proveedores:
                    proveedores.append(proveedor)
        except AttributeError:
            pass    # No es factura de compra.
        try:
            for ldd in self.lineasDeDevolucion:
                proveedor = ldd.producto.proveedor
                if proveedor != None and proveedor not in proveedores:
                    proveedores.append(proveedor)
            for lda in self.lineasDeAbono:
                proveedor = lda.producto.proveedor
                if proveedor != None and proveedor not in proveedores:
                    proveedores.append(proveedor)
        except AttributeError:
            pass    # No es factura de abono.
        return tuple(proveedores)

    def get_str_estado(self, cache = {}, fecha = mx.DateTime.today()):
        """
        Si la factura está en el diccionario de caché recibido (por su puid) 
        entonces no consulta el estado en la BD.
        """
        ESTADOS = ("No documentada", 
                   "Documentada no vencida", 
                   "Impagada", 
                   "Cobrada", 
                   "Pendiente de abonar")
        try:
            estado = cache[self.puid]
            if VERBOSE: 
                print "pclases.py::SuperFacturaVenta.get_str_estado -> HIT!"
        except KeyError:
            estado = self.get_estado(fecha)
        str_estado = ESTADOS[estado]
        return str_estado

    def UNOPTIMIZED_get_str_estado(self, 
                                   cache = {}, 
                                   fecha = mx.DateTime.today()):
        """
        Si la factura está en el diccionario de caché recibido (por su puid) 
        entonces no consulta el estado en la BD.
        """
        ESTADOS = ("No documentada", 
                   "Documentada no vencida", 
                   "Impagada", 
                   "Cobrada", 
                   "Pendiente de abonar")
        try:
            estado = cache[self.puid]
            if VERBOSE: 
                print "pclases.py::SuperFacturaVenta.get_str_estado -> HIT!"
        except KeyError:
            estado = self.UNOPTIMIZED_get_estado(fecha)
        str_estado = ESTADOS[estado]
        return str_estado

    # 20100927: Nueva clasificación de facturas:
    def UNOPTIMIZED_get_estado(self, fecha = mx.DateTime.today()):
        """
        Devuelve el estado de la factura:
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
        #cobrado = self.DEPRECATED_calcular_cobrado(fecha)      # 0.013 según cProfile
        cobrado = self.calcular_cobrado(fecha)     # 0.005 según cProfile
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
            return FRA_IMPAGADA

    def get_estado(self, fecha = mx.DateTime.today()):
        """
        Devuelve el estado de la factura:
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
        from facturaventa import FacturaVenta
        from facturadeabono import FacturaDeAbono
        from prefactura import Prefactura
        if isinstance(self, (Prefactura, FacturaDeAbono)):
            return self.UNOPTIMIZED_get_estado(fecha = fecha)
        else:
            sqlfuncs = (("fra_impagada", FRA_IMPAGADA), 
                        ("fra_no_documentada", FRA_NO_DOCUMENTADA), 
                        ("fra_cobrada", FRA_COBRADA), 
                        ("fra_no_vencida", FRA_NO_VENCIDA), 
                        #("fra_impagada", FRA_IMPAGADA), 
                        ("fra_abono", FRA_ABONO)) 
            for sqlfunc, estado in sqlfuncs:
                if FacturaVenta._connection.queryOne("SELECT %s(%d, '%s');" 
                            % (sqlfunc, self.id, fecha.strftime("%Y-%m-%d")) 
                        )[0]:
                    return estado
        # FIXME: Hasta ahora prefería que se me enviase un correo de error 
        #        para los casos extremos (factura con un vencimiento 
        #        compensado y otro documentado pendiente de vencer, como en 
        #        el caso de la factura X130787 --FacturaVenta:10463--, por 
        #        ejemplo). Pero como se va a acabar llamando al UNOPTIMIZED...
        #        para lanzar la excepción y pierdo la optimización, para eso 
        #        devuelvo el resultado y vuelco a log o me mando el correo 
        #        igualmente para enterarme y estudiar el caso concreto. 
        #        Arf. Arf. Arf. **Y eso es justamente lo que me queda por 
        #        hacer aquí: enviarme una notificación de alguna manera.  
        estado = self.UNOPTIMIZED_get_estado(fecha = fecha)
        #str_estado = self.UNOPTIMIZED_get_str_estado(fecha = fecha)
        # raise ValueError, "La factura «%s» no tiene estado. La función sin optimizar dice que es «%s»." % (self.get_puid(), str_estado)
        return estado

    def calcular_importe_no_documentado(self, fecha = mx.DateTime.today()):
        """
        Devuelve el importe de los vencimientos no documentados.
        Vencimiento no documentado = vencimiento que no tiene asociado ningún 
        cobro en la fecha indicada.
        """
        total = 0.0
        dic_vtos = self.emparejar_vencimientos()
        for vto in dic_vtos:
            if (isinstance(vto, VencimientoCobro)
                or (hasattr(vto, "id") and vto.id==0)): # FakeVto.id=0 siempre.
                importe_cobrado_en_fecha = 0.0
                for cobro in dic_vtos[vto]:
                    if cobro.fecha <= fecha:
                        importe_cobrado_en_fecha += cobro.importe
                total += vto.importe - importe_cobrado_en_fecha
        return total

    def calcular_importe_documentado(self, fecha = mx.DateTime.today()):
        """
        Devuelve el importe de los vencimientos documentados.
        Vencimiento documentado = vencimiento que tiene asociado un  
        cobro de tipo Pagaré/Cheque/Confirming con fecha de recepción anterior 
        a la fecha indicada.
        """
        total = 0.0
        dic_vtos = self.emparejar_vencimientos()
        for vto in dic_vtos:
            if (isinstance(vto, VencimientoCobro) 
                or (hasattr(vto, "id") and vto.id==0)): # FakeVto.id=0 siempre.
                for cobro in dic_vtos[vto]:
                    if ((cobro.pagareCobro 
                         and cobro.pagareCobro.fechaRecepcion <= fecha) 
                        or (cobro.confirming 
                            and cobro.confirming.fechaRecepcion <= fecha)):
                        total += cobro.importe
        return total

    def calcular_importe_vencido(self, fecha = mx.DateTime.today()):
        """
        Devuelve el total del importe vencido en la fecha indicada.
        """
        importes_vencidos = [vto.importe for vto in self.vencimientosCobro 
                             if vto.fecha <= fecha]
        total = sum(importes_vencidos)
        return total

    def calcular_importe_vencido_no_cobrado_ni_documentado(self, 
                                                fecha = mx.DateTime.today()):
        """
        Devuelve el total del importe vencido Y NO COBRADO O DOCUMENTADO en 
        la fecha indicada.
        """
        total = 0.0
        dic_vtos = self.emparejar_vencimientos()
        for vto in dic_vtos:
            if (isinstance(vto, VencimientoCobro)
                or (hasattr(vto, "id") and vto.id==0)): # FakeVto.id=0 siempre.
                importe_vencido = vto.importe
                if vto.fecha <= fecha:  # Vencimiento vencido. ¿Estará cobrado
                                        # o documentado?
                    for cobro in dic_vtos[vto]:
                        if (cobro.confirmingID 
                            and cobro.confirming.fechaRecepcion <= fecha):
                                # Me da igual si está pendiente o no. Está 
                                # documentado y me basta.
                                importe_vencido -= cobro.importe
                        elif (cobro.pagareCobroID 
                            and cobro.pagareCobro.fechaRecepcion <= fecha):
                                # Me da igual si está pendiente o no. Está 
                                # documentado y me basta.
                                importe_vencido -= cobro.importe
                        elif cobro.fecha <= fecha:  # Transferencia, efectivo...
                            importe_vencido -= cobro.importe
        return total

    def calcular_importe_cobrado(self, fecha = mx.DateTime.today()):
        """
        Devuelve el total del importe cobrado en la fecha indicada. Importe 
        cobrado = importe de los cobros anteriores a esa fecha o de los 
        pagarés/confirming/cheques marcados como cobrados.
        """
        total = 0.0
        dic_vtos = self.emparejar_vencimientos()
        for vto in dic_vtos:
            if (isinstance(vto, VencimientoCobro)
                or (hasattr(vto, "id") and vto.id==0)): # FakeVto.id=0 siempre.
                for cobro in dic_vtos[vto]:
                    if cobro.confirmingID:
                        if (cobro.confirming.fechaRecepcion <= fecha 
                            and not cobro.confirming.pendiente):
                            total += cobro.importe
                    elif cobro.pagareCobroID:
                        if (cobro.pagareCobro.fechaRecepcion <= fecha 
                            and not cobro.pagareCobro.pendiente):
                            total += cobro.importe
                    else:
                        if cobro.fecha <= fecha:
                            total += cobro.importe
        return total

    def get_plazo_pago(self, default = None):
        """
        Calcula el número de días de la forma de pago de la factura. Si no 
        tiene vencimientos, se lo trae del pedido. Si tampoco tiene, del 
        cliente y si no, devuelve None o el valor especificado en "default".
        :returns: Entero o lista de enteros con el número de días de la 
                  forma de pago. O valor indicado en "default".
        """
        res = []
        regexpr = re.compile("\d+")
        # De los vencimientos de la propia factura.
        for vto in self.vencimientosCobro:
            forma_de_pago_en_observaciones = vto.observaciones
            if ("CONTADO" in forma_de_pago_en_observaciones.upper() 
                or "EFECTIVO" in forma_de_pago_en_observaciones.upper()):
                forma_de_pago_en_observaciones += " 0"
            for v in regexpr.findall(forma_de_pago_en_observaciones):
                try:
                    v = int(v)
                    if not ((v % 15 == 0) and (0 <= v <= 365)):
                        continue #No es un plazo. Es número de cuenta o algo.
                except (ValueError, TypeError):     # Are you kidding me? 
                    continue
                if v not in res:
                    res.append(v)
        # No hay vencimientos. Del pedido.
        if not res:
            for p in self.get_pedidos():
                if p.formaDePago and p.formaDePago.plazo not in res:
                    res.append(p.formaDePago.plazo)
        # No hay pedidos. Del cliente.
        if not res:
            for v in self.cliente.get_dias_de_pago():
                if v not in res:
                    res.append(v)
        # Me quedo con lo que haya o devuelvo por defecto:
        if res:
            if len(res) == 1:
                plazo = res[0]
            else:
                res.sort()
                plazo = res
        else:
            plazo = default
        return plazo

    def get_plazo_pagado(self):
        """
        Devuelve el número de días transcurrido entre la fecha de la factura 
        y el día en que se hizo realmente el pago (o se hará, si es un 
        vencimiento futuro).
        Si el pago no se ha hecho, devuelve None
        """
        plazos = utils.unificar([c.calc_plazo_pago_real() 
                                 for c in self.cobros])
        # Devuelvo el mayor de los plazos porque esta función va a servir 
        # para medir la desviación respecto a la forma de pago original y 
        # queremos saber el peor de los casos.
        try:
            plazo = max(plazos)
        except ValueError:
            plazo = None
        return plazo

    def get_documento_pagado(self):
        """
        :returns: Devuelve una cadena con el documento de cobro entregado 
                  por el cliente. None si no se ha llegado a documentar.
        """
        strings_cobros = []
        for c in self.cobros:
            doc = c.documentoDePago
            if isinstance(doc, DocumentoDePago):
                strings_cobros.append(doc.documento)
            else:
                if doc:     # Puede ser None
                    strings_cobros.append(doc)  # que ya es una cadena
        if not strings_cobros:
            documento = None
        else:
            documento = ", ".join(strings_cobros)
        return documento

    def get_str_cobro_real(self, default = ""):
        """
        :returns: Devuelve una cadena con el número de días reales 
                  transcurridos hasta el vencimiento del cobro y el 
                  documento de cobro real entregado por el cliente.
                  Si la factura/prefactura/abono no ha sido cobrada
                  todavía, devuelve la cadena recibida en "default".
        """
        plazo = self.get_plazo_pagado()
        if plazo is not None:
            documento = self.get_documento_pagado()
            if documento is None:  # Viene de una factura sin vencimientos.
                pass
            else:
                default = "%s, %d D. F. F." % (documento, plazo)
        return default


