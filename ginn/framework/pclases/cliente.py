#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2014  Francisco José Rodríguez Bogado                    #
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
## cliente.py - Clase ORM para los clientes.                           ##
#########################################################################

'''
Created on 03/07/2013

@author: bogado
'''

from . import PRPCTOO, starter, Cobro, Auditoria, DatosDeLaEmpresa, AND, \
              DEBUG, VERBOSE, Obra
from sqlobject import SQLObject, MultipleJoin, RelatedJoin
from superfacturaventa import FRA_NO_DOCUMENTADA, FRA_NO_VENCIDA,\
                              FRA_IMPAGADA, FRA_COBRADA, FRA_ABONO
from facturaventa import FacturaVenta
from prefactura import Prefactura
import mx.DateTime
import datetime
import sys
import re
import time
from formularios import utils

# Tiempo de expiración de la cutrecaché de crédito de clientes
T_CACHE_EXPIRED = 60    # Segundos.

class Cliente(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    pedidosVenta = MultipleJoin('PedidoVenta')
    albaranesSalida = MultipleJoin('AlbaranSalida')
    facturasVenta = MultipleJoin('FacturaVenta')
    #------------------------------------------- tarifaID = ForeignKey('Tarifa')
    #--------------------------------------- contadorID = ForeignKey('Contador')
    abonos = MultipleJoin('Abono')
    clientes = MultipleJoin('Cliente')
    #----------------------- clienteID = ForeignKey('Cliente')       # Comercial
    comisiones = MultipleJoin('Comision')
    #--------------------- proveedorID = ForeignKey('Proveedor', default = None)
    #--------------- cuentaOrigenID = ForeignKey('CuentaOrigen', default = None)
    presupuestos = MultipleJoin('Presupuesto')
    cuentasBancariasCliente = MultipleJoin('CuentaBancariaCliente')
    documentos = MultipleJoin('Documento')
    prefacturas = MultipleJoin('Prefactura')
    obras = RelatedJoin('Obra', 
                        joinColumn='cliente_id', 
                        otherColumn='obra_id', 
                        intermediateTable='obra__cliente')
    cobros = MultipleJoin("Cobro")
    concentracionesRemesa = MultipleJoin("ConcentracionRemesa")
    #------------- tipoDeClienteID = ForeignKey("TipoDeCliente", default = None)
    camposEspecificosRollos = MultipleJoin("CamposEspecificosRollo")
    camposEspecificosBalas = MultipleJoin("CamposEspecificosBala")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        cad = "%s (CIF %s)" % (self.nombre, self.cif)
        return cad

    def get_documentoDePago(self, strict_mode = False):
        """
        Devuelve un objeto DocumentoDePago que se relaciona unívocamente con 
        el texto que tiene el cliente en el documento de pago.
        None si no lo puede determinar.
        """
        return Cobro._parse_docpago(self.documentodepago, strict_mode)

    def get_texto_forma_cobro(self):
        """
        Devuelve un texto que representa la forma de cobro del cliente. 
        Por ejemplo:  efectivo, pagaré 90 D.F.F., transferencia banco 
        1234-23-...
        """
        formapago = ""
        if (self.documentodepago != None 
                and self.documentodepago.strip() != "" 
                and self.documentodepago.strip() != "0"):
            formapago = "%s, " % (self.documentodepago)
        if (self.vencimientos != None 
                and self.vencimientos.strip() != "" 
                and self.vencimientos.strip() != "0"):
            formapago += "%s " % (self.vencimientos)
        if (self.diadepago != None 
                and self.diadepago.strip() != "" 
                and self.diadepago.strip() != "-"):
            formapago += "los días %s" % (self.diadepago)
        if len(formapago) > 0:
            formapago += ". "
        try:
            txtcompl = self.textoComplementarioFormaDePago
        except AttributeError:
            txtcompl = ""
        if formapago and txtcompl:
            formapago += " " + txtcompl
        return formapago

    textoformacobro = property(get_texto_forma_cobro)

    def get_iva_norm(self, fecha = None):
        """
        Devuelve el iva normalizado (i.e. como fracción de 1) 
        del cliente.
        NOTAS: Temporal hasta que el IVA de la BD se guarde correctamente 
        y corrija las funciones donde se usa.
        Si se especifica fecha y el cliente tiene el IVA estándar, se compara 
        la fecha con el 1 de julio de 2.010 que fue cuando entró en vigor la 
        ley del nuevo IVA al 18%, o con el 1 de septiembre de 2012 que se 
        volvió a cambiar al 21%. Se hace así para el cálculo de los abonos, 
        donde no se guarda el IVA, sino que se determina a partir del cliente.
        """
        if self.iva == None:
            # Aprovecho para quitar los Nones del IVA de los clientes.
            self.iva = 0.21 
        iva = self.iva
        if iva > 1:
            iva /= 100.0
        if (iva == 0.21 and fecha 
            and fecha < mx.DateTime.DateTimeFrom(2010, 7, 1)):
            iva = 0.16  # IVA estándar oficial antes del 1 de julio de 2.010
        elif (iva == 0.21 and fecha 
            and fecha >= mx.DateTime.DateTimeFrom(2010, 7, 1)
            and fecha < mx.DateTime.DateTimeFrom(2012, 9, 1)):
            iva = 0.18  # IVA estándar oficial antes del 1 de sept. de 2.012
        return iva

    def get_fechas_vtos_por_defecto(self, fecha):
        """
        Devuelve una lista ordenada de fechas de vencimientos a 
        partir de los vencimientos, día de pago y tomando la 
        fecha recibida como base.
        En caso de que el proveedor no tenga la información necesaria 
        devuelve una lista vacía.
        """
        res = []
        vtos = self.get_vencimientos()
        try:
            diacobro = int(self.diadepago)
        except (TypeError, ValueError):
            diacobro = None
        for incr in vtos:
            try:
                nfecha = fecha + incr
            except TypeError:
                nfecha = fecha + datetime.timedelta(incr)
            res.append(nfecha)
            if diacobro != None:
                while True:
                    try:
                        res[-1] = mx.DateTime.DateTimeFrom(
                                    day = diacobro, 
                                    month = res[-1].month, 
                                    year = res[-1].year)
                        break
                    except:
                        diacobro -= 1
                        if diacobro <= 0:
                            diacobro = 31
                try:
                    nfecha = fecha + incr
                except TypeError: # No se pueden sumar fechas datetime con enteros.
                    nfecha = fecha + datetime.timedelta(incr)
                if res[-1] < nfecha:
                    mes = res[-1].month + 1; anno = res[-1].year
                    if mes > 12:
                        mes = 1; anno += 1
                    res[-1] = mx.DateTime.DateTimeFrom(day = diacobro, 
                                                       month = mes, 
                                                       year = anno)
                while res[-1].day_of_week >= 5:
                    res[-1] += mx.DateTime.oneDay
        res.sort()
        return res
 
    def get_vencimientos(self, fecha_base = mx.DateTime.localtime()):
        """
        Devuelve una lista con los días naturales de los vencimientos
        del cliente. P. ej.:
        - Si el cliente tiene "30", devuelve [30].
        - Si no tiene, devuelve [].
        - Si tiene "30-60", devuelve [30, 60].
        - Si tiene "90 D.F.F." (90 días a partir de fecha factura), 
          devuelve [90].
        - Si tiene "30-120 D.R.F." (30 y 120 días a partir de fecha de 
          recepción de factura) devuelve [30, 120]. etc.
        - ¡NUEVO! Si tiene "120 D.U.D.M.F.F." (120 días a contar a partir del 
          último día del mes de la fecha de factura) devuelve 120 + los días 
          que haya entre la fecha «fecha_base» y el fin de mes, con objeto de 
          que sean sumados a la fecha de factura desde la ventana que me 
          invoca.
        En definitiva, filtra todo el texto y devuelve los números que 
        encuentre en cliente.vencimientos (por norma general).
        """
        res = []
        if self.vencimientos != None:
            if "contado" in self.vencimientos.lower():
                res = [0]
            else:
                regexpcars = re.compile("\w")
                cadena = "".join(regexpcars.findall(self.vencimientos)).upper()
                regexpr = re.compile("\d*")
                lista_vtos = regexpr.findall(self.vencimientos)
                if "UDM" in cadena:
                    try:
                        findemes = mx.DateTime.DateTimeFrom(
                            day = -1, 
                            month = fecha_base.month, 
                            year = fecha_base.year)
                    except Exception, msg:
                        print "ERROR: pclases::Cliente::get_vencimientos() -> "\
                              "Exception: %s" % (msg)
                        difafindemes = 0
                    else:
                        difafindemes = findemes.day - fecha_base.day
                else:
                    difafindemes = 0
                try:
                    res = [int(i) + difafindemes for i in lista_vtos if i != '']
                except TypeError, msg:
                    print "ERROR: pclases::Cliente::get_vencimientos() -> "\
                          "TypeError: %s" % (msg)
        return res

    def get_dias_de_pago(self):
        """
        Devuelve UNA TUPLA con los días de pago del cliente (vacía si no tiene).
        """
        res = []
        if self.diadepago != None:
            regexpr = re.compile("\d*")
            lista_dias = regexpr.findall(self.diadepago)
            try:
                res = tuple([int(i) for i in lista_dias if i != ''])
            except TypeError, msg:
                print "ERROR: pclases: cliente.get_dias_de_pago(): %s" % (msg)
        return res

    def es_extranjero(self):
        """
        Devuelve True si el cliente es extranjero.
        Para ello mira si el país del cliente es diferente al 
        de la empresa. Si no se encuentran datos de la empresa
        devuelve True si el país no es España.
        """
        cpf = unicode(self.paisfacturacion.strip())
        try:
            de = DatosDeLaEmpresa.select()[0]
            depf = unicode(de.paisfacturacion.strip())
            res = cpf != "" and depf.lower() != cpf.lower()
        except IndexError:
            res = cpf != "" and cpf.lower() != unicode("españa")
        return res

    extranjero = property(es_extranjero)
    
    def get_facturas(self, fechaini = None, fechafin = None):
        """
        Devuelve las facturas del cliente entre las dos 
        fechas recibidas (incluidas). Si ambas son None no 
        aplicará rango de fecha en la búsqueda.
        """
        criterio = (FacturaVenta.q.clienteID == self.id)
        criteriopre = (Prefactura.q.clienteID == self.id)
        if fechaini:
            criterio = AND(criterio, FacturaVenta.q.fecha >= fechaini)
            criteriopre = AND(criteriopre, Prefactura.q.fecha >= fechaini)
        if fechafin:
            criterio = AND(criterio, FacturaVenta.q.fecha <= fechafin)
            criteriopre = AND(criteriopre, Prefactura.q.fecha >= fechaini)
        return ([f for f in FacturaVenta.select(criterio)] 
                + [f for f in Prefactura.select(criterio)])

    def calcular_comprado(self, fechaini = None, fechafin = None):
        """
        Devuelve el importe total de ventas al cliente
        entre las fechas indicadas. Si las fechas son None no 
        impondrá rangos en la búsqueda. No se consideran 
        pedidos ni albaranes, solo compras ya facturadas.
        """
        total = 0
        facturas = self.get_facturas(fechaini, fechafin)
        for f in facturas:
            total += f.calcular_importe_total()
        return total

    def calcular_cobrado(self, fechaini = None, fechafin = None):
        """
        Devuelve el importe total de compras cobradas al cliente  
        entre las fechas indicadas. Si las fechas son None no 
        impondrá rangos en la búsqueda. No se consideran 
        pedidos ni albaranes, solo compras ya facturadas.
        De todas esas facturas, suma el importe de los pagos
        relacionadas con las mismas. _No tiene en cuenta_ las 
        fechas de los cobros, solo las fechas de las facturas 
        a las que corresponden esos cobros (ya que la consulta 
        base es de facturas, lo lógico es saber cuánto de esas 
        facturas está pagado, sea en las fechas que sea).
        Si no hay facturas o no hay cobros, devuelve 0.0.
        """
        #import time
        #antes = time.time()
        facturas = self.get_facturas(fechaini, fechafin)
        #total = 0
        #for f in facturas:
        #    for cobro in f.cobros:
        #        total += cobro.importe
        #_total = total
        #print "1.-", time.time() - antes
        #antes = time.time()
        # OPTIMIZACIÓN:
        if facturas:
            csql = """
                SELECT SUM(cobro.importe) 
                  FROM cobro 
                  WHERE factura_venta_id IN (%s);
            """ % (", ".join([str(f.id) for f in facturas]))
            try:
                total = Cliente._connection.queryOne(csql)[0]
            except IndexError:
                total = 0.0
            if total == None:
                total = 0.0
        else:
            total = 0.0
        #print "2.-", time.time() - antes
        #print _total, total
        #assert round(_total, 2) == round(total, 2)
        return total

    def calcular_pendiente_cobro(self, fechaini = None, fechafin = None):
        """
        Devuelve el importe total pendiente de cobro del cliente. Para ello 
        _ignora los vencimientos_ y simplemente devuelve la diferencia
        entre el importe total facturado y el importe total de los
        cobros relacionados con esas facturas.
        """
        total = self.calcular_comprado(fechaini, fechafin)
        cobrado = self.calcular_cobrado(fechaini, fechafin)
        pendiente = total - cobrado
        return pendiente

    def calcular_pendiente_cobro_vencido(self, 
                                         fechaini = None, 
                                         fechafin = None, 
                                         fecha_base = mx.DateTime.today()):
        """
        Calcula el pendiente de cobro[1] de los vencimientos vencidos en 
        fecha_base de las facturas entre fechaini y fechafin.
        [1] Los cobros también se filtran por fecha_base. Si son posteriores, 
        no se tienen en cuenta.
        Devuelve el pendiente de cobro y un diccionario de facturas, pendiente 
        vencido y cobrado (por ese orden en cada clave del diccionario).
        """
        vencido = 0.0
        cobrado = 0.0
        dicfacturas = {}
        facturas = self.get_facturas(fechaini, fechafin)
        for f in facturas:
            vencf = f.calcular_vencido(fecha_base)
            vencido += vencf
            cobrf = f.calcular_cobrado(fecha_base)
            cobrado += cobrf
            #if vencf - cobrf > 0:
            tot_vtos = sum([v.importe for v in f.vencimientosCobro])
            if (round(tot_vtos - cobrf) != 0):  # No me intersan las 
                                                # diferencias de céntimos
                dicfacturas[f] = (vencf, cobrf)
        return vencido - cobrado, dicfacturas

    def DEPRECATED_calcular_credito_disponible(self, 
                                               cache_pdte_cobro = None, 
                                               base = 0.0):
        """
        Riesgo concedido - pendiente de cobro.
        OJO: No usar cache_pdte_cobro si no se está completamente seguro de 
        la certeza de los datos, en cuyo caso es preferible dejar que 
        se calcule dentro de la rutina aunque tarde más.
        El valor "base" se sumará al pendiente de cobro y sirve para contar 
        la cantidad que se está a punto de facturar, ya que si el límite es, 
        por ejemplo, 11k € y se va a sacar una factura de 11.5k €, SOBREPASA 
        el límite y no debería dejar sacarla.
        """
        if self.riesgoConcedido==-1: # Ignorar. Devuelvo un máximo arbitrario.
            return sys.maxint
        else:
            if cache_pdte_cobro is None:    # Recalculo (agüita, suele tardar)
                pdte_cobro = self.calcular_pendiente_cobro()
            else:
                pdte_cobro = cache_pdte_cobro
            res = self.riesgoConcedido - (pdte_cobro + base)
        return res

    def __actualizar_cache_credito(self, valor_credito, *args):
        self.tiempocache = time.time()
        self.valorcache = valor_credito
        self.cachedargs = args

    def __cutrecache_caducada(self, *args):
        """
        De momento vamos a hacer suposiciones de tiempo.
        Queridos profesores de la facultad. En estos 10 años no me he olvidado 
        de vuestros consejos. PERO.
        """
        try:
            expired = time.time() - self.tiempocache > T_CACHE_EXPIRED
        except AttributeError:  # No hay caché. Por tanto... sí.
            expired = True
        if not expired:
            # Puede que sea una llamada con otros parámetros:
            if args != self.cachedargs:
                expired = True
            else:
                expired = False
        return expired

    def UNOPTIMIZED_calcular_credito_disponible(self, 
                                     impagado = None, 
                                     sin_documentar = None, 
                                     sin_vencer = None, 
                                     base = 0.0):
        """
        Devuelve el máximo del importe que puede servirse a un cliente.
        sin_documentar y sin_vencer se pueden instanciar a una cantidad si 
        ya se ha calculado anteriormente, para ahorrar tiempo aquí.
        Si el cliente no tiene riesgo concedido, no se tiene en cuenta el 
        crédito.
        Si no,
            si el cliente tiene facturas impagadas, es CERO.
            si no, riesgo = (S(fras. sin documentar) + S(pdtes. vencimiento))
        El valor "base" se sumará al pendiente de cobro y sirve para contar 
        la cantidad que se está a punto de facturar, ya que si el límite es, 
        por ejemplo, 11k € y se va a sacar una factura de 11.5k €, SOBREPASA 
        el límite y no debería dejar sacarla.
        """
        if DEBUG and VERBOSE:
            print "SOY EL PUTO CALCULAR_CREDITO SIN CACHÉ"
        if DEBUG:
            bacall = antes = time.time()                        # XXX
        if self.riesgoConcedido==-1: # Ignorar. Devuelvo un máximo arbitrario.
            credito = sys.maxint
        else:
            tempcache = {} # Intentémoslo. Deberían hacerse 1/4 menos de 
                            # llamadas a get_estado **contra** la BD.
            if impagado is None:
                if DEBUG and VERBOSE:
                    print "[0] >>>", time.time() - antes        # XXX
                    antes = time.time()                         # XXX
                impagado = self.calcular_impagado(cache = tempcache)
                if DEBUG and VERBOSE:
                    print "[1] >>>", time.time() - antes        # XXX
                    antes = time.time()                         # XXX
            if impagado > 0:
                credito = 0
            else:
                if sin_documentar is None:
                    if DEBUG and VERBOSE:
                        print "[2] >>>", time.time() - antes    # XXX
                        antes = time.time()                     # XXX
                    sin_documentar = self.calcular_sin_documentar(
                                                            cache = tempcache)
                    if DEBUG and VERBOSE:
                        print "[3] >>>", time.time() - antes    # XXX
                        antes = time.time()                     # XXX
                if sin_vencer is None:
                    if DEBUG and VERBOSE:
                        print "[4] >>>", time.time() - antes    # XXX
                        antes = time.time()                     # XXX
                    sin_vencer = self.calcular_sin_vencer(cache = tempcache)
                    if DEBUG and VERBOSE:
                        print "[5] >>>", time.time() - antes    # XXX
                        antes = time.time()                     # XXX
                credito = self.riesgoConcedido - (sin_documentar + sin_vencer)
                credito -= base
        if DEBUG:
            clara = time.time() - bacall                        # XXX
            print "[Cliente.calcular_credito_disponible]"\
                  " Tiempo transcurrido: %.2f segundos" % clara # XXX
        # Pruebas ANTES de optimización: 
        # >>> from framework import pclases
        # >>> for c in pclases.Cliente.select(pclases.Cliente.q.nombre.contains("CETCO")):
        # >>>     print c.nombre, c.calcular_credito_disponible()
        # CETCO IBERIA, S.L.U. Tiempo transcurrido: 25.51 segundos (etc.) 
        # XXX 
        return credito

    def _calcular_credito_disponible(self, 
                                     base = 0.0, 
                                     fecha = None):
        if not fecha:
            fecha = mx.DateTime.today()
        credito = Cliente._connection.queryOne(
            "SELECT calcular_credito_disponible(%d, '%s', %f)" % (
                self.id, fecha.strftime("%Y-%m-%d"), base))[0]
        # if credito == 'Infinity':     # float('inf')
        if credito > sys.maxint:
            credito = sys.maxint
        return credito

    def calcular_credito_disponible(self, 
                                    impagado = None, 
                                    sin_documentar = None, 
                                    sin_vencer = None, 
                                    base = 0.0):
        ########## La Chapucaché:
        """
        < ¿caché? >---sí-->< ¿caducada? >---no-->[Devolver caché] 
             |no                 |sí                    ^
             |-------------------·                      |
             v                                          |
         [calcular]------->[actualizar caché]-----------·
        """
        if ((not hasattr(self, "tiempocache"))    # Primera vez. O bien 
            or self.__cutrecache_caducada(impagado, 
                                          sin_documentar, 
                                          sin_vencer, 
                                          base)): # (sort of) fallo de caché
            if (impagado != None or sin_documentar != None 
                    or sin_vencer != None):     # Aprovecho los precálculos
                credito = self.UNOPTIMIZED_calcular_credito_disponible(
                                                        impagado, 
                                                        sin_documentar, 
                                                        sin_vencer, 
                                                        base)
            else:
                credito = self._calcular_credito_disponible(base)
            self.__actualizar_cache_credito(credito, impagado, sin_documentar, 
                                            sin_vencer, base)
        return self.valorcache

    def calcular_impagado(self, cache = {}):
        impagadas = self.get_facturas_impagadas(cache = cache)
        total = sum([f.calcular_importe_total() for f in impagadas])
        return total

    def calcular_sin_documentar(self, cache = {}):
        sin_documentar = self.get_facturas_sin_doc_pago(cache = cache)
        # total = sum([f.calcular_importe_total() for f in sin_documentar])
        total = sum([f.calcular_importe_no_documentado() 
                        for f in sin_documentar])
        return total

    def calcular_sin_vencer(self, cache = {}):
        sin_vencer = self.get_facturas_doc_no_vencidas(cache = cache)
        total = sum([f.calcular_importe_total() for f in sin_vencer])
        return total

    def get_facturas_vencidas_impagadas(self):
        """
        Devuelve las facturas vencidas e impagadas (con documento de cobro 
        vencido o directamente sin documento de cobro y sin pagos 
        relacionados).
        """
        if DEBUG:
            print " --> Soy get_facturas_vencidas_impagadas. Toc-toc. Entrando..."
        impagadas = []
        for fra in self.facturasVenta:
            if round(fra.calcular_cobrado(), 2) < round(fra.importeTotal, 2):
                impagadas.append(fra)   # Aunque sea por un céntimo
        if DEBUG:
            print " <-- Soy get_facturas_vencidas_impagadas. Saliendo."
        return impagadas

    def get_facturas_vencidas_sin_documento_de_cobro(self):
        """
        Devuelve las facturas vencidas y sin documento de cobro 
        ni sin pagos relacionados.
        """
        if DEBUG:
            print " --> Soy get_facturas_vencidas_sin_documento_de_cobro."\
                  " Toc-toc. Entrando..."
        impagadas = []
        # El criterio es muy fácil. El importe cubierto por los documentos de 
        # cobro o cobros en general (registros cobro) es menor al de los 
        # vencimientos totales.
        # Si la factura no ha vencido (ninguna fecha de vencimiento supera a 
        # la actual) no se tiene en cuenta. Para considerarla vencida, todos 
        # los vencimientos deben haber expirado -esto es para evitar el caso 
        # en que se ha cumplido el primer vencimiento y el segundo cobro 
        # aún no está cubierto por un doc. de pago-.
        for fra in self.facturasVenta:
            if fra.esta_vencida():
                totvencs = sum([v.importe for v in fra.vencimientosCobro])
                totcobrs = sum([c.importe for c in fra.cobros])
                if round(totcobrs, 2) < round(totvencs, 2):
                    impagadas.append(fra)   # Aunque sea por un céntimo
        if DEBUG:
            print " <-- Soy get_facturas_vencidas_sin_documento_de_cobro."\
                  " Saliendo."
        return impagadas

    def get_direccion_completa(self):
        """
        Devuelve una cadena con la dirección completa del cliente:
        dirección, código postal, ciudad, provincia y país.
        """
        res = "%s;" % self.direccion
        if self.cp:
            res += "%s -" % self.cp
        res += " %s" % self.ciudad
        if self.provincia and self.ciudad != self.provincia:
            res += ", %s" % self.provincia
        if self.pais:
            res += " (%s)" % self.pais
        if res.strip() == ";":
            res = ""
        return res.strip()

    def buscar_comerciales(self):
        """
        Devuelve un diccionario con los comerciales que han trabajado con el 
        cliente y el listado de pedidos que los relaciona.
        """
        res = {}
        for p in self.pedidosVenta:
            comercial = p.comercial
            try:
                res[comercial].append(p)
            except KeyError:
                res[comercial] = [p]
        return res

    def crear_obra_generica(self):
        """
        Crea la obra genérica con los datos del cliente.
        Si ya tiene (alg)una creada y el nombre es el mismo, usa esa como 
        genérica y completa la información de la misma.
        """
        if self.obras:
            for o in self.obras:
                if o.nombre.strip() == self.nombre.strip():
                    o.generica = True
                    break
        obra_generica = [o for o in self.obras 
                         if o.nombre == self.nombre and o.generica]
        try:
            obra_generica = obra_generica[0]
        except:
            obra_generica = Obra(nombre = self.nombre, 
                                direccion = self.direccion, 
                                cp = self.cp,  
                                ciudad = self.ciudad, 
                                provincia = self.provincia, 
                                fechainicio = mx.DateTime.localtime(), 
                                fechafin = None, 
                                observaciones = "Obra genérica del cliente %s."
                                    % (self.get_puid()), 
                                pais = self.pais, 
                                generica = True)
            self.addObra(obra_generica)
        else:
            obra_generica.direccion = self.direccion 
            obra_generica.cp = self.cp  
            obra_generica.ciudad = self.ciudad 
            obra_generica.provincia = self.provincia 
            obra_generica.pais = self.pais
            obra_generica.fechainicio = mx.DateTime.localtime() 
            obra_generica.fechafin = None 
            obra_generica.observaciones = "Obra genérica del cliente %s."% (
                                            self.get_puid()) 
        return obra_generica

    def _get_obras_genericas(self):
        """
        Devuelve un listado de obras genéricas relacionadas con el cliente 
        ordenado por ID.
        """
        obras = [o for o in self.obras if o.generica]
        obras.sort(lambda o1, o2: int(o1.id - o2.id))
        return obras

    def get_obra_generica(self):
        """
        Devuelve la obra genérica relacionada con el cliente. Si no hay 
        ninguna, la crea. Si hay varias devuelve la de ID más bajo.
        OJO: Esto puede permitir -si así lo fuerza el usuario- que varios 
        clientes tengan la misma obra genérica, o que un cliente tenga 
        relación con una obra genérica de otro cliente. Pero en el fondo da 
        igual porque lo importante es que al menos haya una obra por cliente.
        POSTCONDICIÓN: Siempre devuelve una obra.
        """
        obras = self._get_obras_genericas()
        try:
            obra = obras[0]
        except IndexError:
            obra = self.crear_obra_generica()
        return obra
    
    def get_contactos_obras(self):
        """
        Devuelve todos los contactos del cliente relacionados a través de 
        sus obras.
        """
        contactos = []
        for o in self.obras:
            for c in o.contactos:
                if c not in contactos:
                    contactos.append(c)
        return contactos

    # 20100927: Nueva clasificación de facturas:
    def get_facturas_sin_doc_pago(self, cache = {}):
        """
        Facturas sin documento de pago Y NO VENCIDAS.
        Siempre se inentará primero buscar en el diccionario recibido. Si ahí 
        no está la factura (por si PUID), entonces se consulta a la BD.
        """
        res = []
        for f in self.get_facturas_y_abonos():
            try:
                estado_factura = cache[f.puid]
                if VERBOSE: 
                    print "pclases.py::Cliente.get_facturas_sin_doc_pago -> Hit!"
            except KeyError:
                estado_factura = f.get_estado()
            if estado_factura == FRA_NO_DOCUMENTADA:
                res.append(f)
        return res

    def get_facturas_doc_no_vencidas(self, cache = {}):
        res = []
        for f in self.get_facturas_y_abonos():
            try:
                estado_factura = cache[f.puid]
            except KeyError:
                estado_factura = f.get_estado()
            if estado_factura == FRA_NO_VENCIDA:
                res.append(f)
        return res

    def get_facturas_impagadas(self, cache = {}):
        res = []
        for f in self.get_facturas_y_abonos():
            try:
                estado_factura = cache[f.puid]
            except KeyError:
                estado_factura = f.get_estado()
            if estado_factura == FRA_IMPAGADA:
                res.append(f)
        return res

    def get_facturas_no_abonadas(self, cache = {}):
        """
        Devielve las facturas de abono no pagadas ni descontadas en pedidos.
        """
        res = []
        for f in self.get_facturas_y_abonos():
            try:
                estado_factura = cache[f.puid]
            except KeyError:
                estado_factura = f.get_estado()
            if estado_factura == FRA_ABONO:
                res.append(f)
        return res

    def get_facturas_cobradas(self, cache = {}):
        res = []
        for f in self.get_facturas_y_abonos():
            try:
                estado_factura = cache[f.puid]
                if VERBOSE: 
                    print "pclases.py::Cliente.get_facturas_cobradas -> Hit!"
            except KeyError:
                estado_factura = f.get_estado()
            if estado_factura == FRA_COBRADA:
                res.append(f)
        return res

    def get_facturas_y_abonos(self):
        """
        Iterador que devuelve cada vez una factura, prefactura o factura de 
        abono hasta agotar todas las del cliente.
        """
        for fra in self.facturasVenta:
            yield fra
        for pre in self.prefacturas:
            yield pre
        for a in self.abonos:
            if a.facturaDeAbono:
                yield a.facturaDeAbono
        # raise StopIteration  # PAMIQUENOHACEFALTAMIARMITA

    @classmethod
    def id_propia_empresa_cliente(clase_cliente):
        """
        Devuelve el id de la propia empresa en la tabla clientes.
        """
        try:
            empresa = DatosDeLaEmpresa.select()[0]
        except:
            print "ERROR: No hay datos de la empresa."
            return 0
        try:
            empresa = clase_cliente.select(
                    clase_cliente.q.nombre == empresa.nombre)[0]
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

    def calcular_rating(self):
        """
        Calificación del cliente en una escala de 1 a 5.
        0 = Cliente no evaluado: Es nuevo o no hay datos suficientes todavía.
        1 = Cliente con riesgo concedido cero por parte de la empresa.
        2 = Cliente con impagos en la actualidad.
        3 = El cliente suele pagar con retraso.
        4 = El cliente paga a tiempo los vencimientos.
        5 = Cliente que cumple con los vencimientos y su facturación en
            lo que va de año es superior a la media.
        """
        try:
            rating = self.rating
        except AttributeError:
            rating = None
        if rating != None:
            return rating
        # ^^^ Por si algún día decido que se pueda almacenar en la BD y editar 
        # por el usuario, en cuyo caso su opinión prevalecerá sobre el cálculo.
        # Ya meteré algún botoncico para "resetearlo" a None y que se vuelva a 
        # recalcular a partir de sus datos de facturación.
        quality = 0
        if self.riesgoConcedido == 0.0:
            quality = 1
        elif self.get_facturas_impagadas():
            quality = 2
        else:
            if self.facturasVenta:
                exceso_plazo = self.calcular_exceso_medio_plazo_cobro()
                if exceso_plazo > 0:
                    quality = 3
                elif exceso_plazo == None:
                    quality = 0
                else: 
                    quality = 4
                    # Si además de pagar bien, su facturación es superior a la 
                    # media, entonces es un cinco estrellas.
                    pda = mx.DateTime.DateFrom(day = 1, month = 1, 
                            year = mx.DateTime.today().year)
                    if (self.calcular_facturado(fini = pda) >= 
                            (Cliente.calcular_facturacion(fini = pda) 
                                / Cliente.selectBy(
                                    inhabilitado = False).count())):
                        quality = 5
        return quality

    def calcular_exceso_medio_plazo_cobro(self):
        """
        Calcula el exceso medio de los cobros sobre los vencimientos de las
        facturas del cliente.
        Devuelve None si no hay datos suficientes para calcular.
        """
        plazos = []
        for f in self.facturasVenta:
            plazo = f.get_plazo_pagado() 
            if plazo != None:
                plazo_ini = f.get_plazo_pago(default = 0)
                try:
                    plazo -= plazo_ini
                except TypeError:   # plazo_ini es una lista de días.
                    plazo_ini.sort()
                    plazo -= plazo_ini[-1]  # Me quedo con el día más lejano
                        # porque seguramente lo demás sea el día de pago, no 
                        # el plazo entre vencimientos.
                plazos.append(plazo)
        if plazos:
            res = utils.media(plazos)
        else:
            res = None
        return res

    def calcular_facturado(self, fini = None, ffin = None):
        """
        Calcula la facturación bruta del cliente entre las fechas recibidas.
        """
        res = 0.0
        if fini and not ffin:
            fras = FacturaVenta.select(AND(FacturaVenta.q.fecha >= fini, 
                FacturaVenta.q.clienteID == self.id))
        elif not fini and ffin:
            fras = FacturaVenta.select(AND(FacturaVenta.q.fecha < ffin, 
                FacturaVenta.q.clienteID == self.id))
        elif fini and ffin:
            fras = FacturaVenta.select(AND(FacturaVenta.q.fecha >= fini, 
                FacturaVenta.q.fecha < ffin, 
                FacturaVenta.q.clienteID == self.id))
        else:   # not fini and not ffin
            fras = FacturaVenta.select(AND(
                FacturaVenta.q.clienteID == self.id))
        res = sum([f.calcular_importe_total() for f in fras])
        return res
        
    @staticmethod
    def calcular_facturacion(fini = None, ffin = None):
        """
        Calcula la facturación bruta de todos los clientes entre las fechas 
        recibidas.
        """
        res = 0.0
        if fini and not ffin:
            fras = FacturaVenta.select(AND(FacturaVenta.q.fecha >= fini, 
                FacturaVenta.q.clienteID == Cliente.q.id, 
                Cliente.q.inhabilitado == False))
        elif not fini and ffin:
            fras = FacturaVenta.select(AND(FacturaVenta.q.fecha < ffin, 
                FacturaVenta.q.clienteID == Cliente.q.id, 
                Cliente.q.inhabilitado == False))
        elif fini and ffin:
            fras = FacturaVenta.select(AND(FacturaVenta.q.fecha >= fini, 
                FacturaVenta.q.fecha < ffin, 
                FacturaVenta.q.clienteID == Cliente.q.id, 
                Cliente.q.inhabilitado == False))
        else:   # not fini and not ffin
            fras = FacturaVenta.select(AND(
                FacturaVenta.q.clienteID == Cliente.q.id, 
                Cliente.q.inhabilitado == False))
        res = sum([f.calcular_importe_total() for f in fras])
        return res

