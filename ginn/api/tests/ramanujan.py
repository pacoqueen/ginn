#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
El enfermizo hindú era un hacha calculando mentalmente. Me conformo con que
este script sea capaz de cuadrar los números de existencias, producciones,
ventas y consumos de cada producto para la detección temprana de desviaciones.
"""

# pylint: disable=too-many-lines

from __future__ import print_function
import time
import datetime
import sys
import os
import re
import subprocess
import logging
import argparse
try:
    import tablib
except ImportError:
    sys.stderr.write("Es necesario instalar tablib para leer las existencias"
                     " inciales: pip install tablib")
    sys.exit(1)
LOGFILENAME = "%s.log" % (".".join(os.path.basename(__file__).split(".")[:-1]))
logging.basicConfig(filename=LOGFILENAME,
                    format="%(asctime)s %(levelname)-8s : %(message)s",
                    level=logging.DEBUG)
# Desde el framework se hacen algunas cosas sucias con los argumentos,
# así que tengo que hacer una importación limpia a posteriori.
# pylint: disable=invalid-name
_argv, sys.argv = sys.argv, []
ruta_ginn = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "ginn"))
sys.path.append(ruta_ginn)
# pylint: disable=import-error,wrong-import-position
from framework import pclases                                   # noqa
from framework.memoize import memoized                          # noqa
from api import murano                                          # noqa
from api.murano.connection import CODEMPRESA                    # noqa
from api.murano import connection                               # noqa
from api.murano.extra import get_peso_neto, get_superficie      # noqa
from lib.tqdm.tqdm import tqdm  # Barra de progreso modo texto. # noqa
sys.argv = _argv


# TODO: Hacer un parámetro para demonio o algo que saque la consulta de
# inventario a lo cron y lo vuelque a un Excel.
# DONE: Hacer un chequeo por A, B y C antes de los totales para detectar
# errores al importar un bulto como A siendo B y cosas así.

# Pestañas: Desviaciones, Totales, Desglose, A, B, C, Resumen, Valoración
# y Agrupación, que agrupa por fecha de fabricación y proyecto para valoración.
# Los primeros ficheros tenían solo 2 pestañas.
MINTABS = 2
MAXTABS = 9


# pylint: disable=too-many-arguments
def calcular_desviacion(existencias_ini, produccion, ventas, consumos, ajustes,
                        existencias_fin):
    """
    Hace y devuelve el cálculo en sí:
    existencias_fin - (existencias_ini + produccion - ventas - consumos)
    """
    # Las salidas vienen en positivo. Si quiero restar, hay que multiplicar
    # por -1 **una vez sumadas**.
    salidas = [-sum(x) for x in zip(ventas, consumos)]
    # Los ajustes van en positivo si son entradas y en negativo si son salidas.
    # Los sumo sin cambio de signo
    entradas = [sum(x) for x in zip(produccion, ajustes)]
    # Salidas ya van en negativo, entradas y existencias en positivo.
    # El resultado (total) lo paso a negativo para restarlo a las existencias_0
    total = [-sum(x) for x in zip(existencias_ini, entradas, salidas)]
    desviacion = [round(sum(x), 2) for x in zip(existencias_fin, total)]
    return desviacion


# pylint: disable=too-many-locals, too-many-statements, too-many-arguments
def cuentalavieja(producto_ginn, data_inventario, data_pendiente,
                  fini, ffin, report,
                  data_res, dev=False, calidad=None):
    """
    Recibe un producto de ginn y comprueba que entre las fechas fini y ffin
    (recibidas como `datetimes`) es correcto el cálculo
    existencias_1 = existencias_0 + entradas_0->1 - salidas_0->1
    Donde:
    entradas_0->1 = producción_0->1 + ajustes_0->1
    salidas_0->1 = ventas_albaranes_0->1 + consumos_0->1

    Los datos de existencias los obtiene de Murano, los actuales, y del
    fichero excel recibido para las iniciales.
    Los de producción los obtiene de ginn.
    Las de ajustes, aunque procedan de ginn, se obtienen de Murano filtrando
    por la serie del documento.
    Los de ventas se sacan de los albaranes de salida **desde** el almacén
    principal. Estén o no facturados.
    Los consumos se obtienen también de ginn.

    Se realiza un chequeo adicional para comprobar que la producción coincide
    con las entradas en Murano (consulta de MovimientosSerie filtrados por
    fecha contra el SQLServer).

    El parámetro «dev» es solo para depurar el script ("modo desarrollo"),
    no los cálculos. Únicamente sirve para ejecutarlo sin conexión a SQLServer.

    Si calidad es None, no tiene en cuenta calidad. Si es 'A', 'B' o 'C' solo
    realiza los cálculos para los bultos de esa calidad.

    data_pendiente trae los valores de producción y consumos no volcados
    del mes pasado que ha entrado este mes en Murano sin proceder de la
    producción y consumos del mes corriente. Viene un diccionario con **todos**
    los productos y dentro de cada uno las calidades y None para los totales.

    Devuelve True si todo cuadra.
    """
    try:
        calidad = calidad.upper()
    except AttributeError:   # Calidad es None.
        pass
    assert calidad in (None, 'A', 'B', 'C'), "Calidad debe ser None o A/B/C."
    # TODO: Productos sin trazabilidad no deberían analizarse. O bien hacerlo
    # de otra forma, porque las existencias finales son 0 si se consulta por
    # serie.
    # Habría que conectar a otra tabla para ver las existencias e incluso para
    # contar los ajustes (que es como se agrega stock a estos productos).
    res = False
    # 0.- Localizo el producto y todos los datos que solo puedo sacar de Murano
    (producto_murano, existencias_ini, existencias_fin,
     produccion_ginn, ventas, consumos_ginn,
     volcados_murano, consumos_murano, ajustes) = calcular_movimientos(
         producto_ginn, data_inventario, fini, ffin, dev, calidad=calidad)
    # 1.- La "cuenta" en sí.
    desviacion = calcular_desviacion(existencias_ini, produccion_ginn, ventas,
                                     consumos_ginn, ajustes, existencias_fin)
    res = desviacion == [.0, .0, .0]
    # ¿Esa desviación corresponde con algún albarán hecho justo el día del
    # inventario?
    if not res and not dev:
        nventas = get_ventas(producto_murano,
                             fini + datetime.timedelta(days=1), ffin,
                             calidad=calidad)
        ndesviacion = calcular_desviacion(existencias_ini, produccion_ginn,
                                          nventas, consumos_ginn, ajustes,
                                          existencias_fin)
        nres = ndesviacion == [.0, .0, .0]
        if nres:
            res = nres
            desviacion = ndesviacion
            ventas = nventas
        # ¿Quizás con un ajuste positivo que ya se ha contado como parte de
        # la producción de ginn? (Cambio de producto con update_producto en
        # Murano a través de la API pero también cambiado en el parte en ginn)
        najustes = [.0, .0, .0]
        ndesviacion = calcular_desviacion(existencias_ini, produccion_ginn,
                                          ventas, consumos_ginn, najustes,
                                          existencias_fin)
        nres = ndesviacion == [.0, .0, .0]
        if nres:
            res = nres
            desviacion = ndesviacion
            ajustes = najustes
            volcados_murano = [sum(t) for t in zip(produccion_ginn, ajustes)]
    # 2.- Cabecera del informe de resultados:
    if not dev:
        # pylint: disable=no-member
        if calidad is None:
            strcalidad = ""
        else:
            strcalidad = " ({})".format(calidad)
        try:
            report.write("{}: {}{}\n".format(producto_murano.CodigoArticulo,
                                             producto_ginn.descripcion,
                                             strcalidad))
        except AttributeError:
            report.write("{}: _({}) {}_\n".format(
                "***¡Producto no encontrado en Murano!***",
                producto_ginn.puid, producto_ginn.descripcion))
    else:
        report.write("PV{}: {}\n".format(producto_ginn.id,
                                         producto_ginn.descripcion))
    # 3.- Compruebo que los datos del ERP y Murano son iguales:
    if ([round(i, 2) for i in produccion_ginn]
            != [round(i, 2) for i in volcados_murano]):
        report.write("> Producción ginn: {}; entradas Murano: {}\n".format(
            ["{:n}".format(round(i, 2)) for i in produccion_ginn],
            ["{:n}".format(round(i, 2)) for i in volcados_murano]))
    if consumos_ginn != consumos_murano:
        report.write("> Consumos ginn: {}; consumos Murano: {}\n".format(
            ["{:n}".format(round(i, 2)) for i in consumos_ginn],
            ["{:n}".format(round(i, 2)) for i in consumos_murano]))
    # 4.- Escribo los resultados al report.
    report.write("Existencias iniciales: \t{}\n".format(
        ["{:n}".format(round(i, 2)) for i in existencias_ini]))
    report.write("Producción: \t\t{}\n".format(
        ["{:n}".format(round(i, 2)) for i in produccion_ginn]))
    report.write("Ventas: \t\t{}\n".format(
        ["{:n}".format(i) for i in ventas]))
    report.write("Consumos: \t\t{}\n".format(
        ["{:n}".format(round(i, 2)) for i in consumos_ginn]))
    report.write("Ajustes: \t\t{}\n".format(
        ["{:n}".format(round(i, 2)) for i in ajustes]))
    report.write("Existencias finales: \t{}\n".format(
        ["{:n}".format(round(i, 2)) for i in existencias_fin]))
    if not res:
        report.write("**")
    report.write("Desviación")
    if not res:
        report.write("**")
    report.write(": \t\t{}\n".format(
        ["{:n}".format(round(i, 2)) for i in desviacion]))
    report.write("-"*70)
    if res:
        report.write(" _[OK]_ \n")
    else:
        report.write(" **[KO]**\n")
    report.write("\n")
    # 5.- Guardo los resultados en el Dataset para exportarlos después.
    if not dev:
        try:
            familia = producto_murano['CodigoFamilia']
        except TypeError:   # Producto no encontrado en Murano.
            familia = "N/A"
    else:
        familia = "TEST"
    cuadra = res and "OK" or "KO"
    pendiente = find_pendiente_mes_pasado(data_pendiente, producto_ginn,
                                          dev, calidad)
    en_curso = find_produccion_en_curso(producto_ginn, dev, calidad)
    suma = ("=", "=", "=")      # =D2+G2-J2-M2+P2+Y2-AB2
    delta = ("=", "=", "=")     # =S2-AH2
    data_res.append([familia,                           # A
                     'PV{}'.format(producto_ginn.id),   # B
                     producto_ginn.descripcion,         # C
                     existencias_ini[0],                # D
                     existencias_ini[1],                # E
                     existencias_ini[2],                # F
                     produccion_ginn[0],                # G
                     produccion_ginn[1],                # H
                     produccion_ginn[2],                # I
                     ventas[0],                         # J
                     ventas[1],                         # K
                     ventas[2],                         # L
                     consumos_ginn[0],                  # M
                     consumos_ginn[1],                  # N
                     consumos_ginn[2],                  # O
                     ajustes[0],                        # P
                     ajustes[1],                        # Q
                     ajustes[2],                        # R
                     existencias_fin[0],                # S
                     existencias_fin[1],                # T
                     existencias_fin[2],                # U
                     desviacion[0],                     # V
                     desviacion[1],                     # W
                     desviacion[2],                     # X
                     pendiente[0],                      # Y
                     pendiente[1],                      # Z
                     pendiente[2],                      # AA
                     en_curso[0],                       # AB
                     en_curso[1],                       # AC
                     en_curso[2],                       # AD
                     suma[0],                           # AE
                     suma[1],                           # AF
                     suma[2],                           # AG
                     delta[0],                          # AH
                     delta[1],                          # AI
                     delta[2],                          # AJ
                     '',                                # AK
                     cuadra                             # AL
                     ])
    # 6.- Y devuelvo si todo cuadra (True) o hay alguna desviación (False)
    return res


def find_pendiente_mes_pasado(data_pendiente, producto_ginn, dev=False,
                              calidad=None):
    """
    De la hoja de cálculo del mes pasado extrae lo que estaba pendiente
    de volcar entonces para agregarlo a la producción de este mes.
    """
    try:
        calidad = calidad.upper()
    except AttributeError:   # Calidad es None.
        pass
    assert calidad in (None, 'A', 'B', 'C'), "Calidad debe ser None o A/B/C."
    codigo = "PV{}".format(producto_ginn.id)
    try:
        bultos = data_pendiente[codigo][calidad]['#']
        metros = data_pendiente[codigo][calidad]['m2']
        kilos = data_pendiente[codigo][calidad]['kg']
    except KeyError:    # Producto nuevo. No hay nada pendiente del mes pasado.
        bultos, metros, kilos = 0, 0.0, 0.0
    return bultos, metros, kilos


def find_produccion_en_curso(producto_ginn, dev=False, calidad=None):
    """
    A través de ginn devuelve la producción pendiente de validar en el
    momento de la ejecución.
    """
    en_curso = get_produccion_en_curso(producto_ginn, dev)
    if calidad:
        res = (en_curso[calidad]['#'],
               en_curso[calidad]['m2'],
               en_curso[calidad]['kg'])
    else:
        res = (sum([en_curso[calidad]['#'] for calidad in en_curso.keys()]),
               sum([en_curso[calidad]['m2'] for calidad in en_curso.keys()]),
               sum([en_curso[calidad]['kg'] for calidad in en_curso.keys()]))
    return res


@memoized
def _buscar_partes_no_bloqueados():
    """
    Busca los partes pendientes de validar en el momento de ejecutar el script.
    """
    res = []
    no_bloqueados = pclases.ParteDeProduccion.selectBy(bloqueado=False)
    for pdp in no_bloqueados:
        res.append(pdp)
    return res


@memoized
def _buscar_partidas_carga_no_volcadas():
    """
    Devuelve las partidas de carga con consumos pendientes de volcar en el
    momento de lanzar el script.
    """
    pcargas = set()     # Porque una misma partida de carga ha podido ser
    # consumida en varios partes de producción tengo que quedarme con un
    # conjunto donde no se repitan para no contarlos varias veces.
    no_bloqueados = _buscar_partes_no_bloqueados()
    for pdp in no_bloqueados:
        if pdp.es_de_geotextiles():
            pcarga = pdp.partidaCarga
            if pcarga and not pcarga.api:
                pcargas.add(pcarga)
    return pcargas


@memoized
def _buscar_bigbags_pendientes_consumir():
    """
    Devuelve los bigbags asociados a los consumos de los partes de embolsado
    que no han sido todavía volcados como consumo a Murano.
    """
    bigbags = []
    no_bloqueados = _buscar_partes_no_bloqueados()
    for pdp in no_bloqueados:
        if pdp.es_de_bolsas():
            for bigbag in pdp.bigbags:
                if not bigbag.api:
                    bigbags.append(bigbag)
    return bigbags


@memoized
def get_produccion_en_curso(producto_ginn, dev=False):
    """
    Devuelve la producción y los consumos pendientes de volcar a Murano
    en el momento actual. El resultado es un diccionario con los bultos, m² y
    kg por calidad.
    """
    res = {'A': {'#': 0,
                 'kg': 0.0,
                 'm2': 0.0},
           'B': {'#': 0,
                 'kg': 0.0,
                 'm2': 0.0},
           'C': {'#': 0,
                 'kg': 0.0,
                 'm2': 0.0}}
    no_bloqueados = _buscar_partes_no_bloqueados()
    pcargas = _buscar_partidas_carga_no_volcadas()
    bigbags = _buscar_bigbags_pendientes_consumir()
    # PRODUCCIÓN
    for pdp in no_bloqueados:
        for a in pdp.articulos:
            if a.productoVenta == producto_ginn:
                calidad = a.get_str_calidad()
                res[calidad]['#'] += 1
                try:
                    res[calidad]['m2'] += a.superficie
                except TypeError:
                    pass        # No tiene superficie. Sumo 0.
                res[calidad]['kg'] += a.peso_neto
    # CONSUMOS
    # Suma de bigbags del producto no volcados como consumo todavía.
    for bigbag in bigbags:
        pv = bigbag.productoVenta
        if pv == producto_ginn:
            calidad = a.get_str_calidad()
            res[calidad]['#'] -= 1  # Consumos entran en negativo
            # Es bigbag. No tiene superficie
            res[calidad]['kg'] -= a.peso_neto
    # Suma de los consumos de fibra en partidas de carga no validadas.
    for pcarga in pcargas:
        for bala in pcarga.balas:
            pv = bala.productoVenta
            if pv == producto_ginn:
                calidad = a.get_str_calidad()
                res[calidad]['#'] -= 1
                # Es bala. No tiene superficie
                res[calidad]['kg'] -= a.peso_neto
    return res


def calcular_movimientos(producto_ginn, data_inventario, fini, ffin,
                         dev=False, calidad=None):
    """
    Lanza las consultas, hace los cálculos y devuelve:
    - La representación del registro del producto en Murano
    - existencias iniciales
    - existencias actuales
    - producción entre [fini..ffin)
    - ventas entre [fini..ffin)
    - consumos entre [fini..ffin)
    - volcados de producción desde API ginn entre [fini..ffin)
    - consumos desde API ginn entre [fini..ffin)
    - ajustes manuales hechos en Murano para regularizaciones, etc. (serie MAN)
    - ajustes manuales hechos desde API ginn en Murano (serie API)
    """
    try:
        calidad = calidad.upper()
    except AttributeError:   # Calidad es None.
        pass
    assert calidad in (None, 'A', 'B', 'C'), "Calidad debe ser None o A/B/C."
    # Datos de Murano. Si estoy en el equipo de desarrollo, uso 0 para todos.
    if not dev:
        producto_murano = murano.ops.get_producto_murano(producto_ginn)
        existencias_fin = get_existencias_murano(producto_murano, calidad)
        ventas = get_ventas(producto_murano, fini, ffin, calidad)
        volcados_murano = get_volcados_fab(producto_murano, fini, ffin,
                                           calidad)
        consumos_murano = get_bajas_consumo(producto_murano, fini, ffin,
                                            calidad)
        ajustes_murano = get_ajustes_murano(producto_murano, fini, ffin,
                                            calidad)
        ajustes_ginn = get_volcados_api(producto_murano, fini, ffin, calidad)
    else:
        producto_murano = None
        existencias_fin = 0, 0, 0
        ventas = 0, 0, 0
        volcados_murano = 0, 0, 0
        consumos_murano = 0, 0, 0
        ajustes_murano = 0, 0, 0
        ajustes_ginn = 0, 0, 0
    existencias_ini = get_existencias_inventario(data_inventario,
                                                 producto_ginn,
                                                 calidad=calidad)
    # Obtengo los datos de producción y consumos del ERP.
    produccion_ginn = get_produccion(producto_ginn, fini, ffin,
                                     calidad=calidad)
    consumos_ginn = get_consumos_ginn(producto_ginn, fini, ffin,
                                      calidad=calidad)
    # Si hay procesos de importación pendientes de pasar a Murano, contarán
    # como ajustes negativos. Hay que asegurarse de ejecutar el Sr. Lobo antes.
    # Los ajustes de ginn y los de Murano siguen la misma norma: positivos para
    # alta en Murano y negativo para bajas. Da igual si son API o MAN.
    ajustes = [sum(t) for t in zip(ajustes_ginn, ajustes_murano)]
    #  Los volcados los devuelvo para chequear los volcados de la API.
    return (producto_murano, existencias_ini, existencias_fin,
            produccion_ginn, ventas, consumos_ginn,
            volcados_murano, consumos_murano,
            ajustes)


def get_existencias_inventario(data_inventario, producto_ginn, calidad=None):
    """
    Devuelve las existencias que se registraron en el fichero de inventario.
    """
    # No me queda más remedio que obtener este dato únicamente del fichero y
    # no mediante consulta SQL por 2 motivos:
    # - Las subconsultas y anidaciones que tendría que hacer al SQL me
    #   llevarían días.
    # - Nicky siempre va a tomar como base los Excel de los inventarios y
    #   cualquier otra cosa que salga de aquí no valdrá. De todos modos, si
    #   alguien hace cambios y nuestros cálculos se basan en movimientos
    #   donde **ya** están esos cambios, el resultado no será fiable.
    try:
        calidad = calidad.upper()
    except AttributeError:   # Calidad es None.
        pass
    assert calidad in (None, 'A', 'B', 'C'), "Calidad debe ser None o A/B/C."
    almacen = 'GTX'
    codigo = 'PV{}'.format(producto_ginn.id)
    bultos = {'A': 0, 'B': 0, 'C': 0, '': 0}
    metros = {'A': 0.0, 'B': 0.0, 'C': 0.0, '': 0.0}
    kilos = {'A': 0.0, 'B': 0.0, 'C': 0.0, '': 0.0}
    for fila in data_inventario.dict:
        try:
            codigo_sheet = fila[u'Código producto']
        except KeyError:  # El orden siempre es el mismo...
            codigo_sheet = fila[fila.keys()[2]]
        try:
            almacen_sheet = fila[u'Almacén']
        except KeyError:  # aunque haya cambiado el nombre de las columnas.
            almacen_sheet = fila[fila.keys()[0]]
        try:
            calidad_sheet = fila[u'Calidad']
        except KeyError:
            calidad_sheet = fila[fila.keys()[5]]
        if codigo_sheet == codigo and almacen_sheet == almacen:
            bultos[calidad_sheet] += int(fila['Bultos'])
            metros[calidad_sheet] += float(fila['Metros cuadrados'])
            kilos[calidad_sheet] += float(fila['Peso neto'])
    if calidad is None:
        sumbultos = sum([bultos[i] for i in bultos])
        summetros = sum([metros[i] for i in metros])
        sumkilos = sum([kilos[i] for i in kilos])
    else:
        sumbultos = bultos[calidad]
        summetros = metros[calidad]
        sumkilos = kilos[calidad]
    return (round(sumbultos, 2), round(summetros, 2), round(sumkilos, 2))


def get_existencias_murano(producto_murano, calidad=None):
    """
    Devuelve las existencias que Murano tiene en este momento.
    Devuelve una tupla (bultos, m², kg).
    Obtiene todos los datos de la tabla ArticulosSerie.
    **Solo se consulta sobre el almacén GTX.**
    """
    try:
        calidad = calidad.upper()
    except AttributeError:   # Calidad es None.
        pass
    assert calidad in (None, 'A', 'B', 'C'), "Calidad debe ser None o A/B/C."
    # TODO: También podría recibir un fichero de inventario para calcular
    # desviaciones entre dos .xls.
    try:
        codigo = producto_murano.CodigoArticulo
    except AttributeError:
        codigo = None   # Producto no existe en Murano.
    totales = _get_existencias_murano(codigo)
    #  No debería haber series sin calidad (''), pero por si acaso las cuento:
    bultos = {'A': 0, 'B': 0, 'C': 0, '': 0}
    metros = {'A': 0.0, 'B': 0.0, 'C': 0.0, '': 0.0}
    kilos = {'A': 0.0, 'B': 0.0, 'C': 0.0, '': 0.0}
    for total in totales:
        quality = total['calidad']
        bultos[quality] += total['bultos']
        metros[quality] += float(total['metros_cuadrados'])
        kilos[quality] += float(total['peso_neto'])
    if calidad is None:
        sumbultos = sum([bultos[qlty] for qlty in bultos])
        summetros = sum([metros[qlty] for qlty in metros])
        sumkilos = sum([kilos[qlty] for qlty in kilos])
    else:
        sumbultos = bultos[calidad]
        summetros = metros[calidad]
        sumkilos = kilos[calidad]
    return (round(sumbultos, 2), round(summetros, 2), round(sumkilos, 2))


@memoized
def _get_existencias_murano(codigo):
    """
    Lanza la consulta para obtener las existencias del producto recibido
    devolviendo la lista de series en Murano de todas las calidades.
    """
    if codigo:
        almacen = "GTX"
        sql = """USE GEOTEXAN;
            SELECT
               ArticulosSeries.CodigoAlmacen,
               Articulos.CodigoFamilia as familia,
               ArticulosSeries.CodigoArticulo,
               Articulos.DescripcionArticulo,
               ArticulosSeries.Partida,
               ArticulosSeries.CodigoTalla01_ AS calidad,
               COUNT(ArticulosSeries.UnidadesSerie) AS bultos,
               CAST(SUM(ArticulosSeries.PesoNeto_)
                                        AS NUMERIC(36,2)) AS peso_neto,
               CAST(SUM(ArticulosSeries.PesoBruto_)
                                        AS NUMERIC(36,2)) AS peso_bruto,
               CAST(SUM(ArticulosSeries.MetrosCuadrados)
                                        AS NUMERIC(36,2)) AS metros_cuadrados
            FROM ArticulosSeries LEFT OUTER JOIN Articulos
                ON ArticulosSeries.CodigoArticulo = Articulos.CodigoArticulo
                    AND Articulos.CodigoEmpresa = '10200'
            WHERE ArticulosSeries.CodigoEmpresa = '10200'
              AND ArticulosSeries.CodigoArticulo = '{}'
              AND ArticulosSeries.CodigoAlmacen = '{}'
              AND ArticulosSeries.UnidadesSerie > 0
            GROUP BY ArticulosSeries.CodigoArticulo,
              Articulos.DescripcionArticulo,
              ArticulosSeries.CodigoAlmacen,
              ArticulosSeries.CodigoTalla01_,
              ArticulosSeries.Partida,
              Articulos.CodigoFamilia
            ORDER BY Articulos.CodigoFamilia,
              Articulos.DescripcionArticulo,
              ArticulosSeries.Partida,
              ArticulosSeries.CodigoTalla01_;""".format(codigo, almacen)
        conn = connection.Connection()
        totales = conn.run_sql(sql)
    else:
        totales = []
    return totales


def get_ventas(producto_murano, fini, ffin, calidad=None):
    """
    Devuelve las salidas de albarán en Murano del producto recibido entre
    las fechas de inicio y de fin. Ojo, **no las ventas facturadas** sino las
    salidas de albarán. Y solo desde GTX.
    Obtiene los datos de las tablas:
    - LineasAlbaranCliente (Se saca todo de aquí. Ojo con el _bug_ de Murano
      donde la suma de los bultos del packing list no coincide con las
      cantidades de la línea)
    - MovimientoStock (candidata para cotejar, pero al final no se usa)
        OrigenMovimiento = A
    - MovimientoArticuloSerie (tampoco se usa)
        OrigenDocumento = 1
    """
    try:
        calidad = calidad.upper()
    except AttributeError:   # Calidad es None.
        pass
    assert calidad in (None, 'A', 'B', 'C'), "Calidad debe ser None o A/B/C."
    fini = fini.strftime("%Y-%m-%d")
    ffin = ffin.strftime("%Y-%m-%d")
    try:
        codigo = producto_murano.CodigoArticulo
    except AttributeError:  # Ya no existe en Murano
        codigo = None
    bultos = {'A': 0, 'B': 0, 'C': 0, '': 0}
    metros = {'A': 0.0, 'B': 0.0, 'C': 0.0, '': 0.0}
    kilos = {'A': 0.0, 'B': 0.0, 'C': 0.0, '': 0.0}
    totales = _get_ventas(codigo, fini, ffin)
    for total in totales:
        quality = total['CodigoTalla01_']
        unidad = total['UnidadMedida1_']
        # Este assert no es cierto para producto sin tratamiento de series como
        # el PV185 (Restos de geotextiles) que se vende por KG.
        # assert float(total['Unidades2_']) % 1.0 == 0.0, \
        #     "Bultos debe ser un entero."
        bultos[quality] += int(total['Unidades2_'])
        if unidad == 'M2':
            totalmetros = float(total['Unidades'])
            totalkilos = float(total['PesoNeto_'])
        else:
            totalkilos = float(total['Unidades'])
            totalmetros = float(total['MetrosCuadrados'])
        metros[quality] += totalmetros
        kilos[quality] += totalkilos
    if calidad is None:
        sumbultos = sum([bultos[i] for i in bultos])
        summetros = sum([metros[i] for i in metros])
        sumkilos = sum([kilos[i] for i in kilos])
    else:
        sumbultos = bultos[calidad]
        summetros = metros[calidad]
        sumkilos = kilos[calidad]
    return (round(sumbultos, 2), round(summetros, 2), round(sumkilos, 2))


@memoized
def _get_ventas(codigo, fini, ffin):
    """
    Devuelve las ventas del almacén principal en todas las calidades del
    producto correspondiente al código de Murano recibido.
    """
    res = []
    if codigo:
        almacen = "GTX"
        sql = """USE GEOTEXAN;
             SELECT SerieAlbaran, NumeroAlbaran, FechaAlbaran, FechaRegistro,
                    CodigoArticulo, DescripcionArticulo, UnidadMedida1_,
                    UnidadMedida2_, CodigoTalla01_, UnidadesServidas,
                    Unidades, Unidades2_, Bultos, MetrosCuadrados,
                    PesoNeto_, PesoBruto_
               FROM LineasAlbaranCliente
              WHERE CodigoEmpresa = {}
                AND FechaAlbaran >= '{}'
                AND FechaAlbaran < '{}'
                AND CodigoArticulo = '{}'
                AND CodigoAlmacen = '{}'
              ORDER BY FechaRegistro;""".format(CODEMPRESA, fini, ffin, codigo,
                                                almacen)
        conn = connection.Connection()
        res = conn.run_sql(sql)
    return res


@memoized
def get_registros_movimientostock(fini, ffin, codigo, almacen, tipo_movimiento,
                                  origen_movimiento, codigo_canal, serie):
    """
    Devuelve los registros de la tabla MovimientoStock de Murano
    correspondientes al tipo de movimiento y origen de movimiento recibidos.
    Serán 1/2 (entrada/salida) o F/S/A (fabricación/salida/albarán)
    respectivamente para determinar si es un consumo, una venta, un borrado o
    un alta.
    """
    sql = """USE GEOTEXAN;
             SELECT *
               FROM MovimientoStock
              WHERE CodigoEmpresa = '10200'
                AND Fecha >= '{}'
                AND Fecha < '{}'
                AND CodigoArticulo = '{}'
                AND CodigoAlmacen = '{}'
                AND TipoMovimiento = {}
                AND OrigenMovimiento = '{}' """.format(fini, ffin, codigo,
                                                       almacen,
                                                       tipo_movimiento,
                                                       origen_movimiento)
    if codigo_canal is not None:
        sql += "AND CodigoCanal = '{}' ".format(codigo_canal)
    if serie is not None:
        if serie[0] == '!':
            sql += " AND Serie <> '{}' ".format(serie[1:])
        else:
            sql += " AND Serie = '{}' ".format(serie)
    sql += "ORDER BY FechaRegistro;"
    conn = connection.Connection()
    res = conn.run_sql(sql)
    return res


def get_registros_movimientoarticuloserie(fini, ffin, codigo, almacen,
                                          origen_documento, comentario=None,
                                          serie=None):
    """
    Devuelve los registros de Murano correspondientes a los movimientos de
    series del producto, fechas y tipos recibidos.
    OrigenDocumento puede ser 11 (salida) o 2 (entrada).
    Comentario puede ser "Consumo %" o nada.
    Serie puede ser MAN/FAB/API/CONSFIB/CONSBB y admite «!» como primer
    carácter para indicar la condición contraria (NOT).
    """
    sql = """USE GEOTEXAN;
             SELECT *
               FROM MovimientoArticuloSerie
              WHERE CodigoEmpresa = {}
                AND Fecha >= '{}'
                AND Fecha < '{}'
                AND CodigoArticulo = '{}'
                AND CodigoAlmacen = '{}'
                AND OrigenDocumento = {}
              """.format(CODEMPRESA, fini, ffin, codigo, almacen,
                         origen_documento)
    if comentario is not None:
        if comentario[0] == '!':
            sql += "AND Comentario NOT LIKE '{}' ".format(comentario[1:])
        else:
            sql += "AND Comentario LIKE '{}' ".format(comentario)
    if serie is not None:
        if serie[0] == '!':
            sql += "AND SerieDocumento <> '{}' ".format(serie[1:])
        else:
            sql += "AND SerieDocumento = '{}' ".format(serie)
    sql += "ORDER BY FechaRegistro;"
    conn = connection.Connection()
    res = conn.run_sql(sql)
    return res


# pylint: disable=too-many-arguments, too-many-branches
def get_volcados(producto_murano, fini, ffin, tipo_movimiento,
                 origen_movimiento, codigo_canal,
                 origen_documento, comentario=None, serie=None, calidad=None):
    """
    Devuelve los volcados realizados de cada tipo, que viene determinado por
    los parámetros a pasar a la consulta SQL.
    El parámetro «Comentario» se tratará con LIKE y debe incluir los comodines.
    No se agregan aquí. Si la primera letra es `!`, entonces se hará un
    NOT LIKE.
    El parámetro «serie» se utiliza tanto en movimientos de stock como en
    los movimientos de serie para los ajustes manuales desde el propio Murano.
    Si serie es None, no se aplica. Si, por ejemplo, es '!MAN' se hace un
    <> 'MAN' y si es 'MAN' se hace un Serie[Documento] = 'MAN';
    """
    try:
        calidad = calidad.upper()
    except AttributeError:   # Calidad es None.
        pass
    assert calidad in (None, 'A', 'B', 'C'), "Calidad debe ser None o A/B/C."
    fini = fini.strftime("%Y-%m-%d")
    ffin = ffin.strftime("%Y-%m-%d")
    try:
        codigo = producto_murano.CodigoArticulo
    except AttributeError:
        codigo = None
    bultos = {'A': 0, 'B': 0, 'C': 0, '': 0}
    metros = {'A': 0.0, 'B': 0.0, 'C': 0.0, '': 0.0}
    kilos = {'A': 0.0, 'B': 0.0, 'C': 0.0, '': 0.0}
    # Primero se obtiene la dimensión principal de una tabla (MovimientoStock):
    almacen = "GTX"
    totales = get_registros_movimientostock(fini, ffin, codigo, almacen,
                                            tipo_movimiento, origen_movimiento,
                                            codigo_canal, serie)
    for total in totales:
        quality = total['CodigoTalla01_']
        unidad = total['UnidadMedida1_']
        if unidad == 'M2':
            totalmetros = float(total['Unidades'])
            metros[quality] += totalmetros
        else:
            totalkilos = float(total['Unidades'])
            kilos[quality] += totalkilos
    # Bultos y la dimensión adicional (metros cuadrados o kilos) de otra:
    # (Aunque también se podría haber obtenido todo de aquí, pero así me
    # aseguro --double-check-- de que es coherente entre las 2 tablas)
    totales = get_registros_movimientoarticuloserie(fini, ffin, codigo,
                                                    almacen, origen_documento,
                                                    comentario, serie)
    for total in totales:
        quality = total['CodigoTalla01_']
        unidad = total['UnidadMedida1_']
        bultos[quality] += total['UnidadesSerie']
        if unidad == 'ROLLO' and total['MetrosCuadrados']:  # No C, va por kg
            totalkilos = float(total['PesoNeto_'])
            kilos[quality] += totalkilos
        else:   # Será cero para BALAS, BIGBAG y CAJAS, pero por... belleza.
            totalmetros = float(total['MetrosCuadrados'])
            metros[quality] += totalmetros
    if calidad is None:
        sumbultos = sum([bultos[i] for i in bultos])
        summetros = sum([metros[i] for i in metros])
        sumkilos = sum([kilos[i] for i in kilos])
    else:
        sumbultos = bultos[calidad]
        summetros = metros[calidad]
        sumkilos = kilos[calidad]
    return (round(sumbultos, 2), round(summetros, 2), round(sumkilos, 2))


def get_volcados_fab(producto_murano, fini, ffin, calidad=None):
    """
    Devuelve los movimientos de series de tipo FAB (las que proceden del API
    de ginn)  en Murano con fecha de registro entre las recibidas para contar
    los bultos. No cuenta los movimientos 'API' hechos desde el API de ginn
    pero no procedentes de fabricación, sino de ajustes manuales (ipython).
    Busca los movimientos de stock para las unidades: m² o kg.
    Las altas a contar para producción son las entradas **menos** las salidas
    (eliminaciones de artículos) procedentes de fabricación.
    La serie 'FAB' también se podría usar para filtrar, pero con
    el OrigenDocumento 'F' nos vale.
    Lo que sí nos va a valer para identificar los movimientos manuales
    por regularizaciones de inventario, principalmente, es usar la serie 'MAN'.
    Altas:
        MovimientoStock:
            tipoMovimiento = 1 (entrada)
            OrigenMovimiento = 'F' (Fabricación)
            CodigoCanal = ''
        MovimientoArticuloSerie:
            OrigenDocumento = 2 (Fabricación)
            Comentario NOT LIKE 'Consumo%'
            SerieDocumento = 'FAB'
    Bajas:
        MovimientoStock:
            TipoMovimiento = 2 (salida)
            OrigenMovimiento = 'F' (Fabricación)
            CodigoCcanal = ''
        MovimientoArticuloSerie:
            OrigenDocumento = 11 (Salida de stock)
            Comentario NOT LIKE 'Consumo%'
            SerieDocumento = 'FAB'
    """
    # Lo primero son las altas:
    altas = get_volcados(producto_murano, fini, ffin, 1, 'F', '', 2,
                         serie="FAB", calidad=calidad)
    # Ahora las bajas por eliminación desde partes, no por consumo.
    bajas = get_volcados(producto_murano, fini, ffin, 2, 'F', '', 11,
                         '!Consumo%', serie="FAB", calidad=calidad)
    # Y ahora las sumo (los movimientos de salida vienen en positivo de Murano
    # y viene todo sumado, sin desglose por calidades).
    sumbultos = altas[0] - bajas[0]
    summetros = altas[1] - bajas[1]
    sumkilos = altas[2] - bajas[2]
    return (round(sumbultos, 2), round(summetros, 2), round(sumkilos, 2))


def get_bajas_consumo(producto_murano, fini, ffin, calidad=None):
    """
    Devuelve los movimientos de series de tipo FAB (las que proceden del API
    de ginn) con fecha de registro entre las recibidas y que sean de consumos.
    Tanto de balas en las partidas de carga como de bigbags en los partes de
    embolsado. Son:
    MovimientoStock:
        TipoMovimiento = 2 (salida)
        OrigenMovimiento = 'F' (Fabricación)
        CodigoCanal: CONSFIB|CONSBB
    MovimientoArticuloSerie:
        OrigenDocumento = 11 (Salida de stock)
        Comentario LIKE 'Consumo %'
        SerieDocumento <> 'MAN'
    """
    consumos_balas = get_volcados(producto_murano, fini, ffin, 2, 'F',
                                  'CONSFIB', 11, 'Consumo bala%', '!MAN',
                                  calidad=calidad)
    consumos_bigbags = get_volcados(producto_murano, fini, ffin, 2, 'F',
                                    'CONSBB', 11, 'Consumo bigbag%', '!MAN',
                                    calidad=calidad)
    sumbultos = consumos_balas[0] + consumos_bigbags[0]
    summetros = consumos_balas[1] + consumos_bigbags[1]
    sumkilos = consumos_balas[2] + consumos_bigbags[2]
    return (round(sumbultos, 2), round(summetros, 2), round(sumkilos, 2))


def get_ajustes_murano(producto_murano, fini, ffin, calidad=None):
    """
    Ajustes manuales:
        Altas:
            MovimientoStock:
                TipoMovimiento = 1 (entrada)
                OrigenMovimiento = 'E' (Movimiento de entrada)
                Serie = 'MAN'
            MovimientoArticuloSerie:
                OrigenDocumento = 10 (Entrada de stock)
                SerieDocumento = 'MAN'
        Bajas:
            MovimientoStock:
                TipoMovimiento = 2 (salida)
                OrigenMovimiento = 'S' (Movimiento de salida)
                Serie = 'MAN'
            MovimientoArticuloSerie:
                OrigenDocumento = 11 (Salida de stock)
                SerieDocumento = 'MAN'
    Los ajustes son movimientos de salida, así que los devuelvo en negativo.
    """
    # Eliminaciones manuales, movimientos manuales de salida por ajustes...
    # El código canal a None hará que no se use ese parámetro en el SQL
    ajustes_positivos = get_volcados(producto_murano, fini, ffin, 1, 'E', None,
                                     10, serie='MAN', calidad=calidad)
    ajustes_negativos = get_volcados(producto_murano, fini, ffin, 2, 'S', None,
                                     11, serie='MAN', calidad=calidad)
    sumbultos = ajustes_positivos[0] - ajustes_negativos[0]
    summetros = ajustes_positivos[1] - ajustes_negativos[1]
    sumkilos = ajustes_positivos[2] - ajustes_negativos[2]
    res = round(sumbultos, 2), round(summetros, 2), round(sumkilos, 2)
    return res


def get_volcados_api(producto_murano, fini, ffin, calidad=None):
    """
    Devuelve los movimientos de series de tipo API (las que proceden del API
    de ginn) en Murano con fecha de registro entre las recibidas para contar
    los bultos. No cuenta los movimientos 'FAB' hechos desde el API de ginn
    pero procedentes de fabricación, no de ajustes manuales desde consola.
    Busca los movimientos de stock para las unidades: m² o kg.
    Las altas a contar para estos ajustes son las entradas **menos** las
    salidas (eliminaciones de artículos) procedentes directamente de la API.
    Altas:
        MovimientoStock:
            tipoMovimiento = 1 (entrada)
            OrigenMovimiento = 'F' (Fabricación)
            CodigoCanal = ''
            Serie = 'API'
        MovimientoArticuloSerie:
            OrigenDocumento = 2 (Fabricación)
            SerieDocumento = 'API'
    Bajas:
        MovimientoStock:
            TipoMovimiento = 2 (salida)
            OrigenMovimiento = 'F' (Fabricación)
            CodigoCanal = ''
        MovimientoArticuloSerie:
            OrigenDocumento = 11 (Salida de stock)
            Comentario NOT LIKE 'Consumo%'
            SerieDocumento = 'API'
    """
    # Lo primero son las altas:
    altas = get_volcados(producto_murano, fini, ffin, 1, 'F', '', 2,
                         serie="API", calidad=calidad)
    # Ahora las bajas por eliminación desde partes, no por consumo.
    bajas = get_volcados(producto_murano, fini, ffin, 2, 'F', '', 11,
                         '!Consumo%', serie="API", calidad=calidad)
    # Y ahora las sumo (los movimientos de salida vienen en positivo de Murano
    # y viene todo sumado, sin desglose por calidades).
    sumbultos = altas[0] - bajas[0]
    summetros = altas[1] - bajas[1]
    sumkilos = altas[2] - bajas[2]
    return (round(sumbultos, 2), round(summetros, 2), round(sumkilos, 2))


# pylint: disable=too-many-branches
def get_produccion(producto_ginn, fini, ffin, strict=False, calidad=None):
    """
    Devuelve todos la producción del producto entre las fechas. Se obtiene de
    ginn.
    En función del parámetro strict, si es False solo tiene en cuenta la hora
    de comienzo del parte. Da igual si está verificado o no.
    Un rollo fabricado a las 00:15 del 14 de enero no se contará como
    producción del día 14, sino del 13 siempre que el parte haya comenzado
    antes de las 12 de la noche.
    **Es la opción recomendada si se va a comparar con las cifras de
    consulta_producido.py de ginn.** (En ginn la "unidad de búsqueda" son los
    partes de producción porque se calculan rendimientos en base a turnos
    de producción de ocho horas o partes completos)
    Si es True cuenta como fecha para la comparación con fini y ffin la
    fecha **real** de alta del artículo en la base de datos. Da igual si un
    rollo se dio de alta el día 15 del mes con fecha del parte 10 para
    corregir un error del día 10. Ese rollo contará como producido el 15.
    **Es la opción recomendada para comparar con las cifras de Murano, ya que
    en la API de ginn cada rollo entra en Murano unos segundos después de
    crearse en ginn. No se espera a que se verifique el parte. Ni siquiera a
    que acabe el turno. Rollo fabricado, rollo que está disponible en Murano.**
    Toda la producción se hacen sobre el almacén GTX. No es necesario filtrar
    por almacén.
    ___
    ~~Ojo porque los cambios de producto se ven como producción en Murano, pero
    la fecha de alta será la del cambio en Murano, no la de la producción
    original. Eso puede provocar descuadres si ha pasado mucho tiempo entre
    que se fabricó y se corrigió el producto.~~ Ya no es así. Van en canal API.
    """
    try:
        calidad = calidad.upper()
    except AttributeError:   # Calidad es None.
        pass
    assert calidad in (None, 'A', 'B', 'C'), "Calidad debe ser None o A/B/C."
    # A todos los efectos el día comienza en el turno de las 6:
    fhoraini = datetime.datetime(fini.year, fini.month, fini.day, 6)
    bultos = {'A': 0, 'B': 0, 'C': 0}
    metros = {'A': 0.0, 'B': 0.0, 'C': 0.0}
    kilos = {'A': 0.0, 'B': 0.0, 'C': 0.0}
    if producto_ginn.es_clase_c():  # Los productos C se pesan. No van en parte
        strict = True
    if not strict:
        articulos = query_articulos_from_partes(producto_ginn, fhoraini, ffin)
    else:   # En vez de por partes, filtro por fecha de registro **real** en
        # la base de datos de cada artículo.
        articulos = query_articulos(producto_ginn, fhoraini, ffin)
    for a in articulos:
        if a.es_clase_a():
            bultos['A'] += 1
            metros['A'] += get_superficie(a) or 0
            kilos['A'] += get_peso_neto(a)
        elif a.es_clase_b():
            bultos['B'] += 1
            metros['B'] += get_superficie(a) or 0
            kilos['B'] += get_peso_neto(a)
        elif a.es_clase_c():
            bultos['C'] += 1
            metros['C'] += get_superficie(a) or 0
            kilos['C'] += get_peso_neto(a)
    if calidad is None:
        sumbultos = sum([bultos[i] for i in bultos])
        summetros = sum([metros[i] for i in metros])
        sumkilos = sum([kilos[i] for i in kilos])
    else:
        sumbultos = bultos[calidad]
        summetros = metros[calidad]
        sumkilos = kilos[calidad]
    return (round(sumbultos, 2), round(summetros, 2), round(sumkilos, 2))


def query_articulos_from_partes(producto, fini, ffin):
    """
    Devuelve los artículos de ginn comprendidos en los partes de producción
    del producto recibido entre las fechas recibidas. Intervalo abierto en la
    fecha de fin.
    """
    # A todos los efectos el día comienza en el turno de las 6:
    fhoraini = datetime.datetime(fini.year, fini.month, fini.day, 6)
    fhorafin = datetime.datetime(ffin.year, ffin.month, ffin.day, 6)
    PDP = pclases.ParteDeProduccion
    A = pclases.Articulo
    # pylint: disable=no-member
    pdps = PDP.select(pclases.AND(PDP.q.fechahorainicio >= fhoraini,
                                  PDP.q.fechahorainicio < fhorafin,
                                  A.q.parteDeProduccionID == PDP.q.id,
                                  A.q.productoVentaID == producto.id))
    tratados = []
    res = []
    for pdp in tqdm(pdps, desc="Producción {}".format(producto.puid),
                    leave=False):
        if pdp in tratados:
            continue    # Ya contado, me lo salto.
        tratados.append(pdp)
        for a in tqdm(pdp.articulos, desc=pdp.puid, leave=False):
            res.append(a)
    return res


def query_articulos(producto, fini, ffin):
    """
    Devuelve los registros Articulo de ginn comprendidos entre las fechas
    recibidas. Los artículos en sí no guardan la fecha y hora de fabricación.
    Son los rollo/bala/bala_cable/rollo_c/etc. los que lo hacen.
    """
    todos_los_articulos = _query_articulos(fini, ffin)
    try:
        articulos = todos_los_articulos[producto][:]
    except KeyError:
        articulos = []
    return articulos


@memoized
def _query_articulos(fini, ffin):
    """
    Devuelve una lista de todos los artículos de _ginn_ cuya fecha de
    fabricación (que se guarda en la tabla relacionada a `articulo`)
    está entre las fechas recibidas.
    Organiza los artículos en un diccionario cuyas claves son el producto
    de venta al que pertenecen.
    """
    articulos = {}
    # A todos los efectos el día comienza en el turno de las 6:
    fhoraini = datetime.datetime(fini.year, fini.month, fini.day, 6)
    fhorafin = datetime.datetime(ffin.year, ffin.month, ffin.day, 6)
    tablas = (pclases.Bala, pclases.BalaCable, pclases.Caja, pclases.Bigbag,
              pclases.Rollo, pclases.RolloC)
    # PLAN: Esto se podría optimizar. Es tontería recorrer todos los artículos
    # entre las dos fechas por cada producto que el script va a comprobar
    # cuando después se va a filtrar para quedarnos con los que coincidan.
    for tabla in tablas:
        # pylint: disable=no-member
        rs = tabla.select(pclases.AND(tabla.q.fechahora >= fhoraini,
                                      tabla.q.fechahora < fhorafin))
        for item in tqdm(rs, desc="Artículos (strict)", total=rs.count()):
            try:
                articulo = item.articulo
            except IndexError:
                print("Ítem sin artículo {}.".format(item.get_info()))
                sys.exit(4)
            try:
                producto_articulo = articulo.productoVenta
            except IndexError:
                print("Artículo sin producto venta {})".format(
                    articulo.get_info()))
                sys.exit(5)
            try:
                articulos[producto_articulo].append(item.articulo)
            except KeyError:
                articulos[producto_articulo] = [item.articulo]
    return articulos


# pylint:disable=too-many-branches
def get_consumos_ginn(producto_ginn, fini, ffin, calidad=None):
    """
    Devuelve los consumos del producto entre las fechas. Los consumos se toman
    de ginn y la fecha usada para determinar si entra en el filtro es la
    fecha de la partida de carga.
    Las partidas de carga, a diferencia de las producciones, no se vuelcan a
    Murano instantáneamente. Para permitir al operario irlas metiendo poco a
    poco en sus ratos "libres" lo que se hace es ejecutar cada cierto tiempo
    un script que busca las pendientes de volcar y da de baja las balas/bigbag
    en Murano en forma de movimiento de serie FAB en el canal CONS*. Este
    script solo da por buenos los consumos de los partes que estén ya
    verificados; por lo que los más recientes es posible que no hayan entrado
    en Murano, pero se contarán aquí. Para eso está el chequeo que se hace
    en otra función entre los consumos de ginn y los volcados de consumos
    en Murano.
    Para el caso del consumo de bigbag, se mira la fecha del parte (sin horas,
    solo la fecha de inicio) que es por donde se filtra en la consulta de ginn.
    Todos los consumos se hacen sobre el almacén GTX. No es necesario filtrar
    por almacén.
    """
    try:
        calidad = calidad.upper()
    except AttributeError:   # Calidad es None.
        pass
    assert calidad in (None, 'A', 'B', 'C'), "Calidad debe ser None o A/B/C."
    bultos = {'A': 0, 'B': 0, 'C': 0}
    metros = {'A': 0.0, 'B': 0.0, 'C': 0.0}
    kilos = {'A': 0.0, 'B': 0.0, 'C': 0.0}
    articulos_consumidos = get_articulos_consumidos_ginn(producto_ginn, fini,
                                                         ffin)
    for articulo in articulos_consumidos:
        if articulo.es_clase_a():
            bultos['A'] += 1
            metros['A'] += get_superficie(articulo) or 0
            kilos['A'] += get_peso_neto(articulo)
        elif articulo.es_clase_b():
            bultos['B'] += 1
            metros['B'] += get_superficie(articulo) or 0
            kilos['B'] += get_peso_neto(articulo)
        elif articulo.es_clase_c():
            bultos['C'] += 1
            metros['C'] += get_superficie(articulo) or 0
            kilos['C'] += get_peso_neto(articulo)
    if calidad is None:
        sumbultos = sum([bultos[i] for i in bultos])
        summetros = sum([metros[i] for i in metros])
        sumkilos = sum([kilos[i] for i in kilos])
    else:
        sumbultos = bultos[calidad]
        summetros = metros[calidad]
        sumkilos = kilos[calidad]
    return (round(sumbultos, 2), round(summetros, 2), round(sumkilos, 2))


def get_articulos_consumidos_ginn(producto, fini, ffin):
    """
    Devuelve una lista de artículos del producto de ginn recibido consumido en
    los partes de producción entre las fechas fini (incluida) y ffin (no incl.)
    """
    todos_los_articulos_consumidos = _get_articulos_consumidos_ginn(fini, ffin)
    try:
        articulos = todos_los_articulos_consumidos[producto][:]
    except KeyError:    # No se ha consumido nada de ese producto
        articulos = []
    return articulos


@memoized
def _get_articulos_consumidos_ginn(fini, ffin):
    """
    Analiza todos los partes de producción entre las fechas recibidas
    (verificados o no, ya que la producción siempre la medimos completa —han
    corrido ríos de tinta y saliva con esto—, la producción en curso es
    producción) y devuelve un diccionario organizado por producto de venta con
    todos los artículos consumidos de cada uno de ellos.
    Para los productos no consumidos hoy hay entrada en el diccionario.
    """
    res = {}
    # A todos los efectos el día comienza en el turno de las 6:
    fhoraini = datetime.datetime(fini.year, fini.month, fini.day, 6)
    fhorafin = datetime.datetime(ffin.year, ffin.month, ffin.day, 6)
    PDP = pclases.ParteDeProduccion
    # pylint: disable=no-member
    pdps = PDP.select(pclases.AND(PDP.q.fechahorainicio >= fhoraini,
                                  PDP.q.fechahorafin < fhorafin))
    # pylint: disable=too-many-nested-blocks
    pcs_tratadas = []
    for pdp in tqdm(pdps, desc="Analizando consumos"):
        # Si estamos buscando consumos de bigbags miro directamente en los
        # partes los bigbags asociados.
        for bb in pdp.bigbags:
            articulo = bb.articulo
            producto = articulo.productoVenta
            try:
                res[producto].append(articulo)
            except KeyError:
                res[producto] = [articulo]
        # Pero si lo que estamos buscando son consumos de fibra, miro las
        # partidas de carga. Como dos partes pueden estar asociados a la
        # misma partida de carga, llevo el control de los ya tratados.
        try:
            pc = pdp.partidaCarga
            if not pc:  # Es parte de geotextiles pero no ha consumido nada.
                continue
            if pc in pcs_tratadas:  # La partida de carga ya la he contado.
                continue
        except ValueError:
            # No es un parte de geotextiles.
            pass
        else:
            pcs_tratadas.append(pc)
            for bala in pc.balas:
                articulo = bala.articulo
                producto = articulo.productoVenta
                try:
                    res[producto].append(articulo)
                except KeyError:
                    res[producto] = [articulo]
    return res


def parse_fecha(cadfecha):
    """
    Devuelve un datetime con la fecha recibida como cadena en `cadfecha`.
    Admite:
    31/12/2016
    31/12 (se asume año actual)
    31/12/16
    31-12-2016 (y todas las variantes anteriores con guión)
    311217 = 31122017 => 31/12/2017
    3101 => 31/01/2017 (si estamos en 2017)
    01 => 01/01/2017 (si estamos en enero de 2017)
    20170115 => 15/01/2017
    """
    hoy = datetime.date.today()
    if "-" in cadfecha:
        cadfecha = cadfecha.replace("-", "/")
    if "/" not in cadfecha:
        if len(cadfecha) <= 2:
            cadfecha += "/{}/{}".format(hoy.month, hoy.year)
        elif len(cadfecha) <= 4:
            cadfecha = cadfecha[:2] + "/" + cadfecha[2:4] + str(hoy.year)
        else:
            cadfecha = cadfecha[:2] + "/" + cadfecha[2:4] + "/" + cadfecha[4:]
    if cadfecha.count("/") == 0:
        dia = int(cadfecha)
    elif cadfecha.count("/") == 1:
        anno = datetime.date.today().year
        dia, mes = [int(c) for c in cadfecha.split("/")]
    else:
        dia, mes, anno = [int(c) for c in cadfecha.split("/")]
    # Año con 2 cifras
    if anno < 100:
        anno += 2000
    res = datetime.date(anno, mes, dia)
    return res


def parse_fecha_xls(ruta):
    """
    Devuelve la fecha correspondiente a la ruta del fichero recibido.
    Si el fichero se llama, por ejemplo: 20161223*.xls, la fecha se
    correspondería a 23/12/2016.
    Si no se puede encontrar una cadena de números equivalente, entonces
    devolverá la fecha de creación del fichero.
    Devuelve un datetime.
    """
    regex = re.compile("[0-9]{8}")
    try:
        cadfecha = regex.findall(ruta)[-1]
    except IndexError:
        fecha_ultima_modificacion = datetime.datetime.utcfromtimestamp(
            os.path.getmtime(ruta))
        res = fecha_ultima_modificacion
    else:
        try:
            res = parse_fecha(cadfecha)
            if res.year < 2000:     # Ha cogido mes+dia como año.
                raise ValueError
        except ValueError:  # El orden es al contrario, ceporro.
            cadfecha = cadfecha[6:] + cadfecha[4:6] + cadfecha[:4]
            res = parse_fecha(cadfecha)
    return res


def buscar_ultimo_fichero_inventario(ruta="."):
    """
    Busca el último fichero acabado en .xls del directorio y devuelve su ruta.
    None si no se encontró ninguno **acabado en `.xls`**.
    """
    try:
        res = max([os.path.join(ruta, f) for f in os.listdir(ruta)
                   if f.endswith('ramanujan.xls')], key=os.path.getctime)
    except ValueError:
        print("Fichero YYYYMMDD_HH_ramanujan.xls no encontrado en "
              "`{}`.".format(ruta))
        sys.exit(2)
    return res


def find_fich_inventario(ruta):
    """
    Si ruta es un directorio, devuelve el último .xls del directorio.
    Si es una ruta a un fichero, comprueba que sea .xls, .ods o .csv y devuelve
    la ruta completa al mismo.
    """
    if os.path.isdir(ruta):
        res = buscar_ultimo_fichero_inventario(ruta)
    else:
        res = ruta
    res = os.path.abspath(res)
    return res


def load_inventario(fich_inventario, hoja="Totales"):
    """
    Devuelve los datos del excel/ods del inventario como un Dataset de tablib.
    Por defecto devuelve los datos de la hoja "Totales", pero puede devolver
    también los de "Desglose" o "Desviaciones".
    """
    book = tablib.Databook().load(None, open(fich_inventario, "r+b").read())
    sheets = book.sheets()
    assert MINTABS <= len(sheets) <= MAXTABS, "El fichero '{}' no parece ser "\
                                              "válido.".format(fich_inventario)
    found = False
    data = None
    for data in sheets:
        if "<"+hoja.lower()+" " in data.__repr__().lower():
            found = True
            break
    if not found:
        sys.stderr.write("Hoja de inventario no encontrada en {}.".format(
            fich_inventario))
        sys.exit(3)
    return data


def load_pendiente_mes_pasado(fich_inventario):
    """
    Abre el fichero de inventario y extrae los datos de las columnas de
    pendiente de volcar **del mes anterior** en bultos, m² y kg.
    Devuelve un diccionario de códigos de producto con las calidades
    None (todos), A, B y C y a su vez con diccionarios con '#', 'm2' y 'kg'.
     {None: {'#': 0, 'm2': 0.0, 'kg': 0.0},
      'A':  {'#': 0, 'm2': 0.0, 'kg': 0.0},
      'B':  {'#': 0, 'm2': 0.0, 'kg': 0.0},
      'C':  {'#': 0, 'm2': 0.0, 'kg': 0.0}}
    """
    res = {}
    book = tablib.Databook().load(None, open(fich_inventario, "r+b").read())
    sheets = book.sheets()
    assert MINTABS <= len(sheets) <= MAXTABS, "El fichero '{}' no parece ser "\
                                              "válido.".format(fich_inventario)
    for hoja in ("Desviaciones",    # Pendiente volcar totales
                 "A",               # Pendiente volcar calidad A
                 "B",               # Pendiente volcar calidad B
                 "C"):              # Pendiente volcar calidad c
        if hoja == "Desviaciones":
            calidad = None
        else:
            calidad = hoja  # A, B o C
        found = False
        data = None
        for data in sheets:
            if "<"+hoja.lower()+" " in data.__repr__().lower():
                found = True
                break
        if not found:
            sys.stderr.write("Hoja de inventario no encontrada en {}.".format(
                fich_inventario))
            sys.exit(3)
        else:
            # almacen = 'GTX'
            # Las producciones solo pueden ser en el almacén principal.
            bultos = {'A': 0, 'B': 0, 'C': 0, '': 0}
            metros = {'A': 0.0, 'B': 0.0, 'C': 0.0, '': 0.0}
            kilos = {'A': 0.0, 'B': 0.0, 'C': 0.0, '': 0.0}
            for fila in data.dict:
                try:
                    codigo_sheet = fila[u'Código']
                except KeyError:  # El orden siempre es el mismo...
                    codigo_sheet = fila[fila.keys()[1]]
                codigo = codigo_sheet
                try:
                    bultos = int(fila[u'En curso n\u2192n+1 (bultos)'])
                    metros = float(fila[u'En curso n\u2192n+1 (m²)'])
                    kilos = float(fila[u'En curso n\u2192n+1 (kg)'])
                except KeyError:
                    if (fila.keys()[29].startswith("En curso n") and
                            fila.keys()[29].split("(")[0].endswith("n+1 ")):
                        bultos = int(fila[fila.keys()[27]])
                        metros = float(fila[fila.keys()[28]])
                        kilos = float(fila[fila.keys()[29]])
                    else:       # No existe la columna. Inventario antiguo.
                        # Uso ceros y ya completaré a mano.
                        bultos, metros, kilos = 0, 0.0, 0.0
                if codigo not in res:
                    res[codigo] = {}
                res[codigo][calidad] = {'#': bultos,
                                        'm2': round(metros, 2),
                                        'kg': round(kilos, 2)}
    return res


def do_inventario(producto, totales, desglose, dev=False):
    """
    Agrega a los datasets de tablib las existencias actuales del producto y
    el desglose por bultos del mismo.
    """
    codarticulo = 'PV{}'.format(producto.id)
    codalmacen = 'GTX'
    sql_totales = """USE GEOTEXAN;
    SELECT ArticulosSeries.CodigoAlmacen,
       Articulos.CodigoFamilia as familia,
       ArticulosSeries.CodigoArticulo,
       Articulos.DescripcionArticulo,
       ArticulosSeries.Partida,
       ArticulosSeries.CodigoTalla01_ AS calidad,
       COUNT(ArticulosSeries.UnidadesSerie) AS bultos,
       CAST(SUM(ArticulosSeries.PesoNeto_) AS NUMERIC(36,2)) AS peso_neto,
       CAST(SUM(ArticulosSeries.PesoBruto_) AS NUMERIC(36,2)) AS peso_bruto,
       CAST(SUM(ArticulosSeries.MetrosCuadrados) AS NUMERIC(36,2))
                                                        AS metros_cuadrados
    FROM ArticulosSeries LEFT OUTER JOIN Articulos
      ON ArticulosSeries.CodigoArticulo = Articulos.CodigoArticulo
         AND Articulos.CodigoEmpresa = '10200'
    WHERE ArticulosSeries.CodigoEmpresa = '10200'
      AND ArticulosSeries.CodigoArticulo = '{}'
      AND ArticulosSeries.CodigoAlmacen = '{}'
      -- AND ArticulosSeries.FechaInicial >= @fecha_ini
      -- AND ArticulosSeries.FechaInicial < @fecha_fin
      AND ArticulosSeries.UnidadesSerie > 0
    GROUP BY ArticulosSeries.CodigoArticulo,
             Articulos.DescripcionArticulo,
             ArticulosSeries.CodigoAlmacen,
             ArticulosSeries.CodigoTalla01_,
             ArticulosSeries.Partida,
             Articulos.CodigoFamilia
    ORDER BY Articulos.CodigoFamilia,
             Articulos.DescripcionArticulo,
             ArticulosSeries.Partida,
             ArticulosSeries.CodigoTalla01_;
    """.format(codarticulo, codalmacen)
    sql_desglose = """USE GEOTEXAN;
    SELECT ArticulosSeries.CodigoAlmacen,
           Articulos.CodigoFamilia as familia,
           ArticulosSeries.CodigoArticulo,
           Articulos.DescripcionArticulo,
           ArticulosSeries.NumeroSerieLc,
           ArticulosSeries.Partida,
           ArticulosSeries.CodigoTalla01_ AS calidad,
           ArticulosSeries.UnidadesSerie AS bultos,
           CAST(ArticulosSeries.PesoNeto_ AS NUMERIC(36,2)) AS peso_neto,
           CAST(ArticulosSeries.PesoBruto_ AS NUMERIC(36,2)) AS peso_bruto,
           CAST(ArticulosSeries.MetrosCuadrados AS NUMERIC(36,2))
                                                        AS metros_cuadrados,
           ArticulosSeries.FechaInicial AS fecha_fabricacion,
           ArticulosSeries.CodigoPale
    FROM ArticulosSeries LEFT OUTER JOIN Articulos
        ON ArticulosSeries.CodigoArticulo = Articulos.CodigoArticulo
            AND Articulos.CodigoEmpresa = '10200'
    WHERE ArticulosSeries.CodigoEmpresa = '10200'
      AND ArticulosSeries.CodigoArticulo = '{}'
      AND ArticulosSeries.CodigoAlmacen = '{}'
      AND ArticulosSeries.UnidadesSerie > 0
    ORDER BY Articulos.CodigoFamilia,
             Articulos.DescripcionArticulo,
             ArticulosSeries.Partida,
             ArticulosSeries.CodigoTalla01_,
             ArticulosSeries.CodigoPale;
    """.format(codarticulo, codalmacen)
    if not dev:
        conn = connection.Connection()
        rs_totales = conn.run_sql(sql_totales)
        rs_desgloses = conn.run_sql(sql_desglose)
        for rs_total in rs_totales:
            fila_total = [rs_total['CodigoAlmacen'],
                          rs_total['familia'],
                          rs_total['CodigoArticulo'],
                          rs_total['DescripcionArticulo'],
                          rs_total['Partida'],
                          rs_total['calidad'],
                          rs_total['bultos'],
                          rs_total['peso_neto'],
                          rs_total['peso_bruto'],
                          rs_total['metros_cuadrados']]
            totales.append(fila_total)
        for rs_desglose in rs_desgloses:
            fila_desglose = [rs_desglose['CodigoAlmacen'],
                             rs_desglose['familia'],
                             rs_desglose['CodigoArticulo'],
                             rs_desglose['DescripcionArticulo'],
                             rs_desglose['NumeroSerieLc'],
                             rs_desglose['Partida'],
                             rs_desglose['calidad'],
                             rs_desglose['bultos'],
                             rs_desglose['peso_neto'],
                             rs_desglose['peso_bruto'],
                             rs_desglose['metros_cuadrados'],
                             rs_desglose['fecha_fabricacion'],
                             rs_desglose['CodigoPale']]
            desglose.append(fila_desglose)
    else:
        totales.append(['ALMACÉN', 'FAMILIA', 'PV000', 'Descripción',
                        'P-000', 'A', 0, 0.0, 0.0, 0.0])
        desglose.append(['ALMACÉN', 'FAMILIA', 'PV000', 'Descripción',
                         'Q000000', 'P-000', 'A', 0, 0.0, 0.0, 0.0,
                         datetime.datetime.now(), 'P-000'])


def determine_linea(producto, dev=False):
    """
    Recibe un producto de ginn y a partir de su familia en Murano devuelve
    la línea de producción a la que pertenece.
    """
    # HARCODED
    lineas = {'Fibra': ('VTA FIB', 'VTA RESFIB', 'VTA CEMFIB'),
              'Geotextiles': ('VTA GTX', 'VTA RESGTX'),
              'Geocem': ('VTA GEOCEM', ),
              'Comercializado': ('VTA COMER', 'EMBA')}
    if dev:
        linea = "Test"
    else:
        pvmurano = murano.ops.get_producto_murano(producto)
        try:
            familia = pvmurano['CodigoFamilia']
        except TypeError:
            # pvmurano es None. El producto de ginn no existe en Murano.
            linea = "N/A"
        else:
            for linea in lineas:
                if familia in lineas[linea]:
                    break
    return linea


def do_resumen(producto, resumen,
               desviaciones_a, desviaciones_b, desviaciones_c,
               dev=False):
    """
    Monta la pestaña resumen por línea de producción y calidad.
    """
    linea = determine_linea(producto, dev)
    for qlty, desviaciones in (("A", desviaciones_a),
                               ("B", desviaciones_b),
                               ("C", desviaciones_c)):
        calidad = "Calidad {}".format(qlty)
        for fila in desviaciones.dict:
            try:
                codigo = fila['Código']     # Errores unicode en Windows.
            except KeyError:
                codigo = fila[u'Código']
            if codigo == 'PV{}'.format(producto.id):
                iniciales = (fila['Ini. (bultos)'],
                             fila['Ini. (m²)'],
                             fila['Ini. (kg)'])
                producidos = (fila['Prod. (bultos)'],
                              fila['Prod. (m²)'],
                              fila['Prod. (kg)'])
                vendidos = (fila['Ventas (bultos)'],
                            fila['Ventas (m²)'],
                            fila['Ventas (kg)'])
                consumidos = (fila['Cons. (bultos)'],
                              fila['Cons. (m²)'],
                              fila['Cons. (kg)'])
                ajustes = (fila['Ajustes (bultos)'],
                           fila['Ajustes (m²)'],
                           fila['Ajustes (kg)'])
                try:
                    en_curso = (fila['No volcado n-1→n (bultos)']
                                - fila['No volcado n→n+1 (bultos)'],
                                fila['No volcado n-1→n (m²)']
                                - fila['No volcado n→n+1 (m²)'],
                                fila['No volcado n-1→n (kg)']
                                - fila['No volcado n→n+1 (kg'])
                except KeyError:
                    # Versión antigua. No tenemos lo pendiente por A, B y C.
                    en_curso = (0, 0.0, 0.0)    # Habrá que hacerlo a mano.
                # TODO: ¿Funciona la producción en curso en la pestaña resumen? En el cierre de marzo he tenido que escribirlo a mano.
                total = (iniciales[0] + producidos[0]
                         - vendidos[0] - consumidos[0]
                         + ajustes[0] + en_curso[0],
                         iniciales[1] + producidos[1]
                         - vendidos[1] - consumidos[1]
                         + ajustes[1] + en_curso[1],
                         iniciales[2] + producidos[2]
                         - vendidos[2] - consumidos[2]
                         + ajustes[2] + en_curso[2])
                en_murano = (fila['Fin. (bultos)'],
                             fila['Fin. (m²)'],
                             fila['Fin. (kg)'])
                delta = (en_murano[0] - total[0],
                         en_murano[1] - total[1],
                         en_murano[2] - total[2])
                filaresumen = [linea, calidad,                          # 0, 1
                               iniciales[0],  iniciales[1],  iniciales[2],
                               producidos[0], producidos[1], producidos[2],
                               vendidos[0],   vendidos[1],
                               vendidos[2],      # 8..10
                               consumidos[0], consumidos[1], consumidos[2],
                               ajustes[0],    ajustes[1],    ajustes[2],
                               en_curso[0],   en_curso[1],   en_curso[2],
                               total[0],      total[1],      total[2],  # ..22
                               en_murano[0],  en_murano[1],  en_murano[2],
                               delta[0],      delta[1],      delta[2],
                               '']     # ..29
                # Busco la fila de la línea que acabo de calcular.
                found = False
                for i in range(len(resumen)):
                    if (resumen[i][0] == linea              # 'Familia'
                            and resumen[i][1] == calidad):  # 'Calidad'
                        # Y agrego las cifras
                        resumen[i] = [linea, calidad] + map(
                                lambda x, y: x+y,
                                resumen[i][2:-1],
                                filaresumen[2:-1]) + ['']
                        found = True
                        break
                if not found:
                    # O la creo nueva
                    resumen.append(filaresumen)


def do_valoracion(valoracion, agrupado, desglose, dev=False):
    """
    Rellena la pestaña de la hoja de cálculo conteniendo el listado de
    existencias con las columnas:
    Almacén, Familia, Proyecto, Código producto, Descripción, Código de
    trazabilidad, calidad, peso_neto, fecha de fabricación, palé, precio
    de coste de fabricación por kg de esa unidad y coste total de la unidad.
    La fecha de fabricación se obtiene del parte de producción (ginn).
    El precio de valoración y el proyecto se extrae de Murano.
    El resto de datos se aprovecha de data_inventario.
    Rellena también la pestaña de totales (`agrupado`) con la valoración
    total agrupada por almacén, familia, calidad, fecha de fabricación y
    proyecto. En la fecha de fabricación agrupa por mes en el año corriente
    y anterior. En los anteriores, por año únicamente.
    """
    agrupacion = {}
    if dev:
        valoracion.apppend(('GTX', 'VTA GTX', '      ', 'PV0000',
                            'Descripción', 'R000000', 'A', 100.0,
                            datetime.datetime.now(), None, 0.5,
                            100.0*0.5))
        agrupado.append(('GTX', 'VTA GTX', 'A', '2020/01', '      ',
                         100.0, 0.5, 100*0.5))
    else:
        for fila in tqdm(desglose.dict, desc="Valorando existencias",
                         total=len(desglose)):
            fila_valoracion = build_fila_valoracion(fila, agrupacion)
            valoracion.append(fila_valoracion)
        for almacen in agrupacion:
            for familia in agrupacion[almacen]:
                for calidad in agrupacion[almacen][familia]:
                    for fecha in agrupacion[almacen][familia][calidad]:
                        for proyecto in agrupacion[almacen][familia][calidad][fecha]:
                            kg = agrupacion[almacen][familia][calidad][fecha]['kg']
                            valor_total = agrupacion[almacen][familia][calidad][fecha]['valor']
                            try:
                                precio_medio = valor_total / kg
                            except ZeroDivisionError:
                                precio_medio = 0.0
                            agrupado.append(
                                    (almacen, familia, calidad, fecha,
                                     proyecto, kg, precio_medio, valor_total))


def build_fila_valoracion(fila, agrupacion):
    """
    Consulta de Murano y de ginn los datos no encontrados en la fila del
    datalib de desglose recibido.
    """
    try:
        almacen = fila[u'Almacén']
    except KeyError:  # El orden siempre es el mismo...
        almacen = fila[fila.keys()[0]]
    try:
        familia = fila[u'Familia']
    except KeyError:  # ... hasta que deje de serlo
        familia = fila[fila.keys()[1]]
    try:
        codigo_producto = fila[u'Código producto']
    except KeyError:
        codigo_producto = fila[fila.keys()[2]]
    try:
        descripcion = fila[u'Descripción']
    except KeyError:
        descripcion = fila[fila.keys()[3]]
    try:
        codigo_trazabilidad = fila[u'Código trazabilidad']
    except KeyError:
        codigo_trazabilidad = fila[fila.keys()[4]]
    try:
        calidad = fila[u'Calidad']
    except KeyError:
        calidad = fila[fila.keys()[6]]
    try:
        pale = fila[u'Palé']
    except KeyError:
        pale = fila[fila.keys()[12]]
    pv = murano.ops.get_producto_ginn(codigo_producto)
    articulo = pclases.Articulo.get_articulo(codigo_trazabilidad)
    proyecto = murano.ops.get_proyecto(pv)
    precio = murano.ops.get_precio_coste(articulo)
    # Malo sería que cambie el peso entre que genero el datalib de
    # desglose y monto este. Así me evito el error float*Decimal:
    peso_neto = articulo.peso_neto
    coste = precio * peso_neto
    # Asumimos la fecha del parte como fecha de fabricación de todos
    # los artículos. Se toma la fecha lógica del parte (si antes de las
    # 6:00, es del día anterior) no la fecha natural. Es con intención
    # de que cuadre con las producciones y demás, que también toman
    # las 6:00 como pivote de cambio de día.
    # Si por lo que sea no tiene parte, se devuelve la fecha y hora
    # de creación del artículo, que no tiene por qué coincidir si
    # se ha dado de alta más tarde por problemas en la línea.
    try:
        fhora_fabricacion = articulo.parteDeProduccion.fechahorainicio
    except AttributeError:
        fhora_fabricacion = articulo.fechahora
    fecha_fabricacion = datetime.date.fromordinal(
        fhora_fabricacion.toordinal())
    if fhora_fabricacion.hour < 6:
        fecha_fabricacion -= datetime.timedelta(days=1)
    res = (almacen, familia, proyecto, codigo_producto,
           descripcion, codigo_trazabilidad, calidad,
           peso_neto, fecha_fabricacion, pale, precio,
           coste)
    # Antes de devolver la fila, actualizo las agrupaciones
    if almacen not in agrupacion:
        agrupacion[almacen] = {}
    else:
        if familia not in agrupacion[almacen]:
            agrupacion[almacen][familia] = {}
        else:
            if calidad not in agrupacion[almacen][familia]:
                agrupacion[almacen][familia][calidad] = {}
            else:
                anno = fecha_fabricacion.year
                anno_corriente = datetime.date.today().year
                # Se agrupa el año completo si es anterior a dos años atrás.
                if anno <= anno_corriente-2:
                    mes = fecha_fabricacion.month
                    fecha = "{}/{}".format(anno, mes)
                else:
                    fecha = "{}".format(anno)
                if fecha not in agrupacion[almacen][familia][calidad]:
                    agrupacion[almacen][familia][calidad][fecha] = {}
                else:
                    if proyecto not in agrupacion[almacen][familia][calidad][fecha]:
                        agrupacion[almacen][familia][calidad][fecha][proyecto] = {'kg': 0.0, 'valor': 0.0}
                    else:
                        agrupacion[almacen][familia][calidad][fecha][proyecto]['kg'] += peso_neto
                        agrupacion[almacen][familia][calidad][fecha][proyecto]['valor'] += peso_neto * precio
    return res


def main():
    """
    Rutina principal.
    """
    # # Parámetros
    tini = time.time()
    parser = argparse.ArgumentParser(
        description="Soy Srinivasa Iyengar Ramanujan.\n"
                    "Calculo entradas y salidas por producto para detectar "
                    "desviaciones en las existencias desde la fecha inicial.\n"
                    "Todavía no me ha encontrado Hardy, así que de momento"
                    "solo sé hacer los cálculos para productos de venta y "
                    "el almacén principal.")
    def_fich_ini = '.'
    parser.add_argument("--fichero_stock_inicial", dest="fich_inventario",
                        default=def_fich_ini)
    parser.add_argument("-p", "--productos", dest="codigos_productos",
                        help="Códigos de productos a comprobar.",
                        nargs="+", default=[])
    ahora = datetime.datetime.today().strftime("%Y%m%d_%H")
    parser.add_argument("-o", dest="fsalida",
                        help="Guardar resultados en fichero de salida.",
                        default="%s_ramanujan.md" % (ahora))
    parser.add_argument("-v", "--view", dest="ver_salida",
                        help="Abre el fichero de salida en un editor externo.",
                        default=False, action='store_true')
    parser.add_argument("-d", "--debug", dest="debug", help="Modo depuración.",
                        default=False, action="store_true")
    args = parser.parse_args()
    if args.debug:
        connection.DEBUG = True
    if args.ver_salida:
        if not os.path.exists(args.fsalida):
            open(args.fsalida, 'a').close()
        subprocess.Popen(["gvim", args.fsalida])
    # # Pruebas
    productos = []
    results = []    # Resultados de las comprobaciones para cada `productos`.
    if args.codigos_productos:
        for codigo in tqdm(args.codigos_productos,
                           desc="Buscando productos ginn"):
            producto = murano.ops.get_producto_ginn(codigo)
            productos.append(producto)
    else:
        for pv in tqdm(pclases.ProductoVenta.select(
                            pclases.ProductoVenta.q.obsoleto == False,  # noqa
                            orderBy="id"),
                       desc="Buscando productos ginn"):
            productos.append(pv)
    fich_inventario = find_fich_inventario(args.fich_inventario)
    fini = parse_fecha_xls(fich_inventario)
    today = datetime.datetime.today()
    # Para evitar problemas con las fechas que incluyen horas, y para que
    # éstas entren en el intervalo, agrego un día a la fecha final y hago
    # el filtro con menor estricto: una producción del 02/01/17 23:00
    # la consideramos como que entra en el día 2, y entraría en el filtro
    # [01/01/17..02/01/17] porque en realidad sería [01/01/17..03/01/17).
    ffin = today + datetime.timedelta(days=1)
    report = open(args.fsalida, "a", 0)
    report.write("Analizando desde {} a {}, fin no incluido.\n".format(
        fini.strftime("%d/%m/%Y"), ffin.strftime("%d/%m/%Y")))
    report.write("=========================================================="
                 "\n")
    report.write("## Todas las cantidades son en (bultos, m², kg).\n")
    data_inventario = load_inventario(fich_inventario)
    data_pendiente = load_pendiente_mes_pasado(fich_inventario)
    data_res = tablib.Dataset(title="Desviaciones")
    inventario = tablib.Dataset(title="Totales")
    desglose = tablib.Dataset(title="Desglose")
    resumen = tablib.Dataset(title="Resumen")
    valoracion = tablib.Dataset(title="Valoración")
    agrupado = tablib.Dataset(title="Agrupado")
    desviaciones_a = tablib.Dataset(title="A")
    desviaciones_b = tablib.Dataset(title="B")
    desviaciones_c = tablib.Dataset(title="C")
    data_res.headers = ['Familia',          'Código',       'Producto',
                        'Ini. (bultos)',    'Ini. (m²)',    'Ini. (kg)',
                        'Prod. (bultos)',   'Prod. (m²)',   'Prod. (kg)',
                        'Ventas (bultos)',  'Ventas (m²)',  'Ventas (kg)',
                        'Cons. (bultos)',   'Cons. (m²)',   'Cons. (kg)',
                        'Ajustes (bultos)', 'Ajustes (m²)', 'Ajustes (kg)',
                        'Fin. (bultos)',    'Fin. (m²)',    'Fin. (kg)',
                        'Dif. (bultos)',    'Dif. (m²)',    'Dif. (kg)',
                        'En curso n-1→n (bultos)',
                        'En curso n-1→n (m²)',
                        'En curso n-1→n (kg)',
                        'En curso n→n+1 (bultos)',
                        'En curso n→n+1 (m²)',
                        'En curso n→n+1 (kg)',
                        '∑ (bultos)',       '∑ (m²)',       '∑ (kg)',
                        'Δ (bultos)',       'Δ (m²)',       'Δ (kg)',
                        'Notas', 'ℹ'
                        ]
    desviaciones_a.headers = data_res.headers[:]
    desviaciones_b.headers = desviaciones_a.headers[:]
    desviaciones_c.headers = desviaciones_b.headers[:]
    inventario.headers = ['Almacén', 'Familia', 'Código producto',
                          'Descripción', 'Partida', 'Calidad', 'Bultos',
                          'Peso neto', 'Peso bruto', 'Metros cuadrados']
    desglose.headers = ['Almacén', 'Familia', 'Código producto',
                        'Descripción', 'Código trazabilidad', 'Partida',
                        'Calidad', 'Bultos', 'Peso neto', 'Peso bruto',
                        'Metros cuadrados', 'Fecha importación a Murano',
                        'Palé']
    resumen.headers = ['Familia', 'Calidad',
                       'Ini. (bultos)',     'Ini. (m²)',    'Ini. (kg)',
                       'Prod. (bultos)',    'Prod. (m²)',   'Prod. (kg)',
                       'Ventas (bultos)',   'Ventas (m²)',  'Ventas (kg)',
                       'Cons. (bultos)',    'Cons. (m²)',   'Cons. (kg)',
                       'Ajustes (bultos)',  'Ajustes (m²)', 'Ajustes (kg)',
                       'En curso (bultos)', 'En curso (m²)', 'En curso (kg)',
                       '∑ (bultos)',        '∑ (m²)',       '∑ (kg)',
                       'Murano (#)',        'Murano (m²)',  'Murano (kg)',
                       'Δ (bultos)',        'Δ (m²)',       'Δ (kg)',
                       'ℹ']
    valoracion.headers = ['Almacén', 'Familia', 'Proyecto', 'Código producto',
                          'Descripción', 'Código trazabilidad', 'Calidad',
                          'Peso neto', 'Fecha fabricación', 'Palé',
                          'Precio valoración', 'Coste fabricación']
    agrupado.headers = ['Almacén', 'Familia', 'Calidad', 'Fecha fabricación',
                        'Proyecto', '∑ peso neto', 'Precio kg', 'Valoración']
    for producto in tqdm(productos, desc="Productos"):
        res = cuentalavieja(producto, data_inventario, data_pendiente,
                            fini, ffin, report,
                            data_res, args.debug)
        cuentalavieja(producto, data_inventario, data_pendiente,
                      fini, ffin, report,
                      desviaciones_a, args.debug, calidad="A")
        cuentalavieja(producto, data_inventario, data_pendiente,
                      fini, ffin, report,
                      desviaciones_b, args.debug, calidad="B")
        cuentalavieja(producto, data_inventario, data_pendiente,
                      fini, ffin, report,
                      desviaciones_c, args.debug, calidad="C")
        results.append((producto, res))
        do_inventario(producto, inventario, desglose, args.debug)
        do_resumen(producto, resumen,
                   desviaciones_a, desviaciones_b, desviaciones_c,
                   args.debug)
    do_valoracion(valoracion, agrupado, desglose, args.debug)
    fallos = [p for p in results if not p[1]]
    report.write("Encontradas {} desviaciones: {}".format(
        len(fallos), "; ".join(['PV{}'.format(p[0].id) for p in fallos])))
    report.write("\n\nFecha y hora de generación del informe: {}\n".format(
        datetime.datetime.now().strftime("%d/%m/%Y %H:%M")))
    tfin = time.time()
    hours, rem = divmod(tfin - tini, 3600)
    minutes, seconds = divmod(rem, 60)
    report.write("Tiempo transcurrido: {:0>2}:{:0>2}:{:05.2f}\n".format(
        int(hours), int(minutes), seconds))
    report.write("\n\n___\n\n")
    report.close()
    fout = args.fsalida.replace(".md", ".xls")
    book = tablib.Databook((data_res, inventario, desglose,
                            desviaciones_a, desviaciones_b, desviaciones_c,
                            resumen, valoracion, agrupado))
    with open(fout, 'wb') as f:
        # pylint: disable=no-member
        f.write(book.xls)


if __name__ == "__main__":
    main()
