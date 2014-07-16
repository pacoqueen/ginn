#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Por el cambio de producto de varios rollos hay que crear los partes
correspondientes y partidas sin alterar las productividades.
UPDATE [16/07/2014] Hay que pasar una serie de rollos pero ahora de
Danofelt a NT 12 normal (rparra). Se cambia el load_rollos por
_load_rollos y se crea un nuevo load_rollos con los códigos nuevos.
"""

import sys
import os
import datetime

#import mx.DateTime
# Determino dónde estoy para importar pclases y utils
DIRACTUAL = os.path.split(os.path.abspath(os.path.curdir))[-1]
try:
    FULLDIRPADRE = os.path.split(os.path.abspath(os.path.curdir))[0]
    DIRPADRE = os.path.split(FULLDIRPADRE)[-1]
except IndexError:
    sys.exit(2)  # Where The Fuck am I?
assert DIRACTUAL == "scripts" or DIRPADRE == "tests", \
                    "Debe ejecutar el script desde el directorio donde reside"\
                    " o bien desde un subdirectorio de `tests`."
sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "ginn")))
from framework import pclases
#from framework import tests_coherencia
from formularios import utils
from lib.textprogressbar.progress.bar import IncrementalBar

add_horas = lambda h, d: (
        datetime.datetime.combine(datetime.date(1, 1, 1), h) + d).time()

def _load_rollos(productividades):
    """
    Devuelve un diccionario con los productos a los que hay que pasar cada
    rollo que está en la lista de cada clave.
    Guarda en el diccionario de productividades los rendimientos de los partes
    antes de tocarlos más adelante.
    """
    nt15 = (350516, 350518, 350523, 350524, 350527)                         # 5
    nt23 = (341302, 341303, 341304, 341305, 341306, 341307, 349848, 349849,
            349850, 349851, 349854, 349855, 349859, 349862, 349866, 349867) #16
    nt30 = (349894, 349898, 349904, 349905, 349906, 349909)                 # 6
    pvnt15 = pclases.ProductoVenta.select(pclases.AND(
                pclases.ProductoVenta.q.descripcion.contains("NT 15 "),
                pclases.NOT(
                    pclases.ProductoVenta.q.descripcion.contains("NT 155")),
                pclases.ProductoVenta.q.camposEspecificosRolloID ==
                    pclases.CamposEspecificosRollo.q.id,
                pclases.CamposEspecificosRollo.q.metrosLineales == 100,
                pclases.CamposEspecificosRollo.q.ancho == 5.5),
            orderBy="id")[0]
    pvnt23 = pclases.ProductoVenta.select(pclases.AND(
                pclases.ProductoVenta.q.descripcion.contains("NT 23 "),
                pclases.NOT(
                    pclases.ProductoVenta.q.descripcion.contains("NT 235")),
                pclases.ProductoVenta.q.camposEspecificosRolloID ==
                    pclases.CamposEspecificosRollo.q.id,
                pclases.CamposEspecificosRollo.q.metrosLineales == 100,
                pclases.CamposEspecificosRollo.q.ancho == 5.5),
            orderBy="id")[0]
    pvnt30 = pclases.ProductoVenta.select(pclases.AND(
                pclases.ProductoVenta.q.descripcion.contains("NT 30"),
                pclases.NOT(
                    pclases.ProductoVenta.q.descripcion.contains("NT 305")),
                pclases.ProductoVenta.q.camposEspecificosRolloID ==
                    pclases.CamposEspecificosRollo.q.id,
                pclases.CamposEspecificosRollo.q.metrosLineales == 90,
                pclases.CamposEspecificosRollo.q.ancho == 5.5),
            orderBy="id")[0]
    res = {pvnt15: [],
           pvnt23: [],
           pvnt30: []}
    for codigo in nt15:
        rollo = pclases.Rollo.selectBy(numrollo=codigo)[0]
        res[pvnt15].append(rollo)
        pdp = rollo.parteDeProduccion
        if pdp not in productividades:
            productividades[pdp] = pdp.calcular_rendimiento()
    for codigo in nt23:
        rollo = pclases.Rollo.selectBy(numrollo=codigo)[0]
        res[pvnt23].append(rollo)
        pdp = rollo.parteDeProduccion
        if pdp not in productividades:
            productividades[pdp] = pdp.calcular_rendimiento()
    for codigo in nt30:
        rollo = pclases.Rollo.selectBy(numrollo=codigo)[0]
        res[pvnt30].append(rollo)
        pdp = rollo.parteDeProduccion
        if pdp not in productividades:
            productividades[pdp] = pdp.calcular_rendimiento()
    return res


def load_rollos(productividades):
    """
    Devuelve un diccionario con los productos a los que hay que pasar cada
    rollo que está en la lista de cada clave.
    Guarda en el diccionario de productividades los rendimientos de los partes
    antes de tocarlos más adelante.
    """
    nt12 = (354096, 354097, 354098, 354099, 354100,  # 5
            354101, 354102, 354103, 354104, 354105,  # 10
            354106, 354107)                          # 12
    pvnt12 = pclases.ProductoVenta.select(pclases.AND(
                pclases.ProductoVenta.q.descripcion.contains("NT 12 "),
                pclases.NOT(
                    pclases.ProductoVenta.q.descripcion.contains("NT 125")),
                pclases.ProductoVenta.q.camposEspecificosRolloID ==
                    pclases.CamposEspecificosRollo.q.id,
                pclases.CamposEspecificosRollo.q.metrosLineales == 100,
                pclases.CamposEspecificosRollo.q.ancho == 1.83),
            orderBy="id")[0]
    res = {pvnt12: []}
    for codigo in nt12:
        rollo = pclases.Rollo.selectBy(numrollo=codigo)[0]
        res[pvnt12].append(rollo)
        pdp = rollo.parteDeProduccion
        if pdp not in productividades:
            productividades[pdp] = pdp.calcular_rendimiento()
    return res


def crear_partida():
    """
    Crea y devuelve una partida vacía donde meter los rollos del producto.
    """
    ultima_partida = pclases.Partida.select(orderBy="-id")[0]
    numpartida = ultima_partida.numpartida
    while pclases.Partida.selectBy(numpartida=numpartida).count() > 0:
        numpartida += 1
    partida = pclases.Partida(numpartida=numpartida,
                              codigo="P-%d" % numpartida,
                              gramaje=0.0,
                              longitudinal=0.0,
                              alongitudinal=0.0,
                              transversal=0.0,
                              atransversal=0.0,
                              compresion=0.0,
                              perforacion=0.0,
                              espesor=0.0,
                              permeabilidad=0.0,
                              poros=0.0,
                              partidaCarga=None,
                              observaciones="Creada automáticamente el %s"
                                            " por cambio de producto." % (
                                                utils.str_fecha(
                                                    datetime.date.today())),
                              piramidal=0.0)
    return partida


def determinar_pdp(rollo):
    """
    A partir del parte actual del rollo, busca (y si no, crea) el parte de
    producción en el que debe estar para no mezclarlo con los rollos del
    producto anterior en el parte en el que se encuentra actualmente.
    """
    pdp_actual = rollo.articulo.parteDeProduccion
    pdp = pdp_actual.siguiente()
    if pdp.productoVenta != rollo.productoVenta:
        pdp = crear_pdp_siguiente(pdp_actual)
    return pdp


def crear_pdp_siguiente(pdp):
    """
    Crea un parte de producción de duración, inicialmente, cero justo a
    continuación de pdp. Le asigna los mismos empleados PERO NO LOS
    CONSUMOS. Eso se hará más tarde.
    El parte recibido se recorta un minuto para dejar hueco para el nuevo.
    """
    horainicio = add_horas(pdp.horafin, -datetime.timedelta(minutes=1))
    horafin = pdp.horafin
    fechahorainicio = pdp.fechahorafin - datetime.timedelta(minutes=1)
    fechahorafin = pdp.fechahorafin
    pdp.horafin = horainicio
    pdp.fechahorafin = fechahorainicio
    pdp.sync()
    nuevo = pdp.clone(horainicio=horainicio,
                      horafin=horafin,
                      bloqueado=True,
                      observaciones="[admin] Creado por cambio de producto"
                                    " y partida en algunos rollos del parte "
                                    "anterior.",
                      fechahorainicio=fechahorainicio,
                      fechahorafin=fechahorafin)
    for horastrabajadas in pdp.horasTrabajadas:
        horastrabajadas.clone(parteDeProduccion=nuevo,
                              horas=datetime.time(minute=1))
        horastrabajadas.horas = add_horas(horastrabajadas.horas, 
                                          -datetime.timedelta(minutes=1))
        horastrabajadas.sync()
    return nuevo


def asignar(rollo, pdp, partida, productividades):
    """
    Asigna el rollo al parte y a la partida recibida. Ajusta la duración del
    parte actual del rollo y del parte al que va antes de reasignarlo.
    El nuevo parte tendrá el rendimiento que salga. Solo ajusto el original.
    En teoría la producción conjunta debería ser la misma que antes de
    crear el parte.
    """
    pdp_anterior = rollo.parteDeProduccion
    rendimiento_objetivo = productividades[pdp_anterior]
    ajustar_consumos(pdp_anterior, pdp, partida)
    rollo.parteDeProduccion = pdp
    rollo.partida = partida
    rollo.sync()
    # Ajusto el rendimiento después de haberle quitado el rollo al que tenía
    # antes de quitarlo.
    ajustar_rendimiento(pdp_anterior, rendimiento_objetivo, pdp)
    # De los partes nuevos, guardo la productividad final tras actualizarla.
    productividades[pdp] = pdp.calcular_rendimiento()


def ajustar_consumos(pdp_orig, pdp_dest, partida_dest):
    """
    Del parte pdp_orig calcula la parte de consumos que corresponde al
    rollo que hemos sacado considerando que cada rollo consume una
    parte proporcional del total.
    En el pdp_dest crea, si no existe ya, un consumo similar al que
    asigna o aumenta la cantidad calculada.
    Asigna también, si no lo estaba ya, la partida del nuevo parte a la
    de carga del parte anterior. Como pdp_dest al menos tendrá ya un
    rollo y, por tanto, una partida; no hay posibilidad de AttributeError.
    """
    total_rollos = len(pdp_orig.articulos)
    for cons in pdp_orig.consumos:
        parte_proporcional = cons.cantidad / total_rollos
        cons.cantidad -= parte_proporcional
        consumo_dest = buscar_consumo(pdp_dest, cons)
        consumo_dest.cantidad += parte_proporcional
        cons.sync()
        consumo_dest.sync()
    partida_orig = pdp_orig.partida
    partidaCarga_orig = partida_orig.partidaCarga
    partida_dest.partidaCarga = partidaCarga_orig
    partida_dest.sync()


def buscar_consumo(pdp, consumo):
    """
    Busca, y si no, crea a partir del consumo «consumo» un consumo
    perteneciente al parte «pdp» con el mismo producto consumido que «consumo».
    Si se tiene que crear, se hará con cantidad 0. Después se ajustará con
    la cantidad correcta.
    """
    res = None
    for cons in pdp.consumos:
        if cons.productoCompra == consumo.productoCompra:
            res = cons
    if not res:
        res = consumo.clone(parteDeProduccion=pdp)
    return res


def ajustar_rendimiento(pdp, objetivo, pdp_siguiente):
    """
    Recorta las horas de pdp hasta llegar al rendimiento (productividad)
    objetivo. Una vez alcanzado, amplía el siguiente ajustando la hora de
    inicio a la del final de pdp.
    PRECONDICIÓN: El rendimiento actual de pdp es MAYOR que el objetivo, de
    modo que recortando horas suba hasta alcanzarlo.
    El ajuste se hará con precisión de 1 decimal.
    """
    if not pdp.articulos:   # El parte se ha quedado vacío. ¡No puedo ajustar!
        print "¡Parte %s vacío!" % pdp.get_info()
        sys.exit(1)
    # Ajustes de un minuto. Me da igual que tarde una eternidad.
    delta = datetime.timedelta(minutes=1)
    precision = 2
    while (round(pdp.calcular_rendimiento(), precision)
           < round(objetivo, precision)):
        pdp.fechahorafin -= delta
        pdp.horafin = pdp.fechahorafin.time()
        for horastrabajadas in pdp.horasTrabajadas:
            add_horas(horastrabajadas.horas, -delta)
        for horastrabajadas in pdp_siguiente.horasTrabajadas:
            add_horas(horastrabajadas.horas, delta)
    pdp.sync()
    pdp_siguiente.fechahorainicio = pdp.fechahorafin
    pdp_siguiente.horainicio = pdp.horafin
    pdp_siguiente.sync()

def main():
    """
    Carga la lista de rollos y cambia el producto de venta de cada uno de ellos
    """
    productividades = {}
    rollos = load_rollos(productividades)
    total_rollos = sum([len(rollos[p]) for p in rollos])
    barra = IncrementalBar('Creando partes...', max=total_rollos)
    for producto in rollos:
        partida = crear_partida()
        for rollo in rollos[producto]:
            parte = determinar_pdp(rollo)
            asignar(rollo, parte, partida, productividades)
            barra.next()
    barra.finish()
    # Resumen de productividades:
    partes = productividades.keys()
    partes.sort(key=lambda p: p.productoVenta.descripcion)
    for pdp in partes:
        print pdp.get_info()
        print "\tAntes: %.2f\tDespués: %.2f\tDuración:%s" % (
            productividades[pdp], pdp.calcular_rendimiento(),
            utils.str_hora_corta(pdp.get_duracion()))


if __name__ == "__main__":
    main()
