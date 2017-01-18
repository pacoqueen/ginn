#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
El enfermizo hindú era un hacha calculando mentalmente. Me conformo con que
este script sea capaz de cuadrar los números de existencias, producciones,
ventas y consumos de cada producto para la detección temprana de desviaciones.
"""

# pylint: disable=too-many-lines

from __future__ import print_function
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
from framework import pclases
from api import murano
from api.murano import connection
from api.murano.extra import get_peso_neto, get_superficie
from lib.tqdm.tqdm import tqdm  # Barra de progreso modo texto.
sys.argv = _argv


# TODO: Hacer un parámetro para demonio o algo que saque la consulta de
# inventario a lo cron y lo vuelque a un Excel.


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
def cuentalavieja(producto_ginn, data_inventario, fini, ffin, report,
                  data_res, dev=False):
    """
    Recibe un producto de ginn y comprueba que entre las fechas fini y ffin
    (recibidas como `datetimes`) es correcto el cálculo
    existencias_1 = existencias_0 + entradas_0->1 - salidas_0->1
    Donde:
    entradas_0->1 = producción_0->1
    salidas_0->1 = ventas_albaranes_0->1 + consumos_0->1

    Los datos de existencias los obtiene de Murano, los actuales, y del
    fichero excel recibido para las iniciales.
    Los de producción los obtiene de ginn.
    Los de ventas se sacan de los albaranes de salida **desde** el almacén
    principal. Estén o no facturados.
    Los consumos se obtienen también de ginn.

    Se realiza un chequeo adicional para comprobar que la producción coincide
    con las entradas en Murano (consulta de MovimientosSerie filtrados por
    fecha contra el SQLServer).

    El parámetro «dev» es solo para depurar el script ("modo desarrollo"),
    no los cálculos. Únicamente sirve para ejecutarlo sin conexión a SQLServer.

    Devuelve True si todo cuadra.
    """
    res = False
    # 0.- Localizo el producto todos los datos que solo puedo sacar de Murano.
    (producto_murano, existencias_ini, existencias_fin,
     produccion_ginn, ventas, consumos_ginn,
     volcados_murano, consumos_murano, ajustes) = calcular_movimientos(
         producto_ginn, data_inventario, fini, ffin, dev)
    # 1,- La "cuenta" en sí.
    desviacion = calcular_desviacion(existencias_ini, produccion_ginn, ventas,
                                     consumos_ginn, ajustes, existencias_fin)
    res = desviacion == [.0, .0, .0]
    # ¿Esa desviación corresponde con algún albarán hecho justo el día del
    # inventario?
    if not res and not dev:
        nventas = get_ventas(producto_murano,
                             fini + datetime.timedelta(days=1), ffin)
        ndesviacion = calcular_desviacion(existencias_ini, produccion_ginn,
                                          nventas, consumos_ginn, ajustes,
                                          existencias_fin)
        nres = ndesviacion == [.0, .0, .0]
        if nres:
            res = nres
            desviacion = ndesviacion
            ventas = nventas
    # 2.- Cabecera del informe de resultados:
    if not dev:
        # pylint: disable=no-member
        try:
            report.write("{}: {}\n".format(producto_murano.CodigoArticulo,
                                           producto_ginn.descripcion))
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
    report.write("Existencias iniciales: {}\n".format(
        ["{:n}".format(round(i, 2)) for i in existencias_ini]))
    report.write("Producción: {}\n".format(
        ["{:n}".format(round(i, 2)) for i in produccion_ginn]))
    report.write("Ventas: {}\n".format(
        ["{:n}".format(i) for i in ventas]))
    report.write("Consumos: {}\n".format(
        ["{:n}".format(round(i, 2)) for i in consumos_ginn]))
    report.write("Ajustes: {}\n".format(
        ["{:n}".format(round(i, 2)) for i in ajustes]))
    report.write("Existencias finales: {}\n".format(
        ["{:n}".format(round(i, 2)) for i in existencias_fin]))
    if not res:
        report.write("**")
    report.write("Desviación")
    if not res:
        report.write("**")
    report.write(": {}\n".format(
        ["{:n}".format(round(i, 2)) for i in desviacion]))
    report.write("-"*70)
    if res:
        report.write(" _[OK]_ \n")
    else:
        report.write(" **[KO]**\n")
    report.write("\n")
    # 5.- Guardo los resultados en el Dataset para exportarlos después.
    data_res.append(['PV{}'.format(producto_ginn.id),
                     producto_ginn.descripcion,
                     existencias_ini[0],   # A
                     existencias_ini[1],   # B
                     existencias_ini[2],   # C
                     produccion_ginn[0],
                     produccion_ginn[1],
                     produccion_ginn[2],
                     ventas[0],
                     ventas[1],
                     ventas[2],
                     consumos_ginn[0],
                     consumos_ginn[1],
                     consumos_ginn[2],
                     ajustes[0],
                     ajustes[1],
                     ajustes[2],
                     existencias_fin[0],
                     existencias_fin[1],
                     existencias_fin[2],
                     desviacion[0],
                     desviacion[1],
                     desviacion[2]])
    # 6.- Y devuelvo si todo cuadra (True) o hay alguna desviación (False)
    return res


def calcular_movimientos(producto_ginn, data_inventario, fini, ffin, dev=False):
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
    - ajustes manuales hechos desde ginn (produccion - volcados)
    """
    # Datos de Murano. Si estoy en el equipo de desarrollo, uso 0 para todos.
    if not dev:
        producto_murano = murano.ops.get_producto_murano(producto_ginn)
        existencias_fin = get_existencias_murano(producto_murano)
        ventas = get_ventas(producto_murano, fini, ffin)
        volcados_murano = get_volcados_api(producto_murano, fini, ffin)
        consumos_murano = get_bajas_consumo(producto_murano, fini, ffin)
        ajustes_murano = get_ajustes_murano(producto_murano, fini, ffin)
    else:
        producto_murano = None
        existencias_fin = 0, 0, 0
        ventas = 0, 0, 0
        volcados_murano = 0, 0, 0
        consumos_murano = 0, 0, 0
        ajustes_murano = 0, 0, 0
    existencias_ini = get_existencias_inventario(data_inventario,
                                                 producto_ginn)
    # Obtengo los datos de producción y consumos del ERP.
    produccion_ginn = get_produccion(producto_ginn, fini, ffin)
    consumos_ginn = get_consumos_ginn(producto_ginn, fini, ffin)
    # Si hay procesos de importación pendientes de pasar a Murano, contarán
    # como ajustes negativos. Hay que asegurarse de ejecutar el Sr. Lobo antes.
    ## ajustes_ginn = [x-y for x, y in zip(volcados_murano, produccion_ginn)]
    # Si calculo así los ajuste desde ginn, siempre balanceará la diferencia
    # entre la producción y las entradas efectivas en Murano. ¿Por qué? Porque
    # esos ajustes hechos a través de la API se hacen como borrado+creación
    # del artículo en el nuevo producto desde un terminal; y, por tanto, son
    # indistinguibles de las creaciones y borrados hechos desde el parte. Usan
    # las musmas funciones de ops.py. Es decir, que si lo calculo así,
    # entrarían dos veces en el cálculo de la desviación: como parte del total
    # de producción, y como supuestos ajustes manuales con signo contrario.
    ajustes_ginn = [0, 0, 0]
    ajustes = [sum(t) for t in zip(ajustes_ginn, ajustes_murano)]
    #  Los volcados los devuelvo para chequear los volcados de la API.
    return (producto_murano, existencias_ini, existencias_fin,
            produccion_ginn, ventas, consumos_ginn,
            volcados_murano, consumos_murano,
            ajustes)


def get_existencias_inventario(data_inventario, producto_ginn):
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
    almacen = 'GTX'
    codigo = 'PV{}'.format(producto_ginn.id)
    res = [0, .0, .0]   # Bultos, metros, kilos
    for fila in data_inventario.dict:
        try:
            codigo_sheet = fila[u'Código producto']
        except KeyError:    # El orden siempre es el mismo...
            codigo_sheet = fila[fila.keys()[2]]
        try:
            almacen_sheet = fila[u'Almacén']
        except KeyError:    # aunque haya cambiado el nombre de las columnas.
            almacen_sheet = fila[fila.keys()[0]]
        if codigo_sheet == codigo and almacen_sheet == almacen:
            # No distinguimos A, B y C.
            res[0] += int(fila['Bultos'])
            res[1] += float(fila['Metros cuadrados'])
            res[2] += float(fila['Peso neto'])
    return res


def get_existencias_murano(producto_murano):
    """
    Devuelve las existencias que Murano tiene en este momento.
    Devuelve una tupla (bultos, m², kg).
    Obtiene todos los datos de la tabla ArticulosSerie.
    **Solo se consulta sobre el almacén GTX.**
    """
    # TODO: También podría recibir un fichero de inventario para calcular
    # desviaciones entre dos .xls.
    almacen = "GTX"
    try:
        codigo = producto_murano.CodigoArticulo
    except AttributeError:
        codigo = None   # Producto no existe en Murano.
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
    #  No debería haber series sin calidad (''), pero por si acaso las cuento:
    bultos = {'A': 0, 'B': 0, 'C': 0, '': 0}
    metros = {'A': 0.0, 'B': 0.0, 'C': 0.0, '': 0.0}
    kilos = {'A': 0.0, 'B': 0.0, 'C': 0.0, '': 0.0}
    for total in totales:
        calidad = total['calidad']
        bultos[calidad] += total['bultos']
        metros[calidad] += float(total['metros_cuadrados'])
        kilos[calidad] += float(total['peso_neto'])
    sumbultos = sum([bultos[i] for i in bultos])
    summetros = sum([metros[i] for i in metros])
    sumkilos = sum([kilos[i] for i in kilos])
    return (round(sumbultos, 2), round(summetros, 2), round(sumkilos, 2))


def get_ventas(producto_murano, fini, ffin):
    """
    Devuelve las salidas de albarán en Murano del producto recibido entre
    las fechas de inicio y de fin. Ojo, **no las ventas facturadas** sino las
    salidas de albarán. Y solo desde GTX.
    Obtiene los datos de las tablas:
    - LineasAlbaranCliente
    - MovimientoStock (candidata para cotejar, pero al final no se usa)
        OrigenMovimiento = A
    - MovimientoArticuloSerie
        OrigenDocumento = 1
    """
    almacen = "GTX"
    fini = fini.strftime("%Y-%m-%d")
    ffin = ffin.strftime("%Y-%m-%d")
    try:
        codigo = producto_murano.CodigoArticulo
    except AttributeError:  # Ya no existe en Murano
        codigo = None
    bultos = {'A': 0, 'B': 0, 'C': 0, '': 0}
    metros = {'A': 0.0, 'B': 0.0, 'C': 0.0, '': 0.0}
    kilos = {'A': 0.0, 'B': 0.0, 'C': 0.0, '': 0.0}
    sql = """USE GEOTEXAN;
             SELECT SerieAlbaran, NumeroAlbaran, FechaAlbaran, FechaRegistro,
                    CodigoArticulo, DescripcionArticulo, UnidadMedida1_,
                    UnidadMedida2_, CodigoTalla01_, UnidadesServidas,
                    Unidades, Unidades2_, Bultos, MetrosCuadrados,
                    PesoNeto_, PesoBruto_
               FROM LineasAlbaranCliente
              WHERE CodigoEmpresa = '10200'
                AND FechaAlbaran >= '{}'
                AND FechaAlbaran < '{}'
                AND CodigoArticulo = '{}'
                AND CodigoAlmacen = '{}'
              ORDER BY FechaRegistro;""".format(fini, ffin, codigo, almacen)
    conn = connection.Connection()
    totales = conn.run_sql(sql)
    for total in totales:
        calidad = total['CodigoTalla01_']
        unidad = total['UnidadMedida1_']
        assert float(total['Unidades2_']) % 1.0 == 0.0, "Bultos debe ser un entero."
        bultos[calidad] += int(total['Unidades2_'])
        if unidad == 'M2':
            totalmetros = float(total['Unidades'])
            totalkilos = float(total['PesoNeto_'])
        else:
            totalkilos = float(total['Unidades'])
            totalmetros = float(total['MetrosCuadrados'])
        metros[calidad] += totalmetros
        kilos[calidad] += totalkilos
    sumbultos = sum([bultos[i] for i in bultos])
    summetros = sum([metros[i] for i in metros])
    sumkilos = sum([kilos[i] for i in kilos])
    return (round(sumbultos, 2), round(summetros, 2), round(sumkilos, 2))


# pylint: disable=too-many-arguments, too-many-branches
def get_volcados(producto_murano, fini, ffin, tipo_movimiento,
                 origen_movimiento, codigo_canal,
                 origen_documento, comentario=None, serie=None):
    """
    Devuelve los volcados realizados de cada tipo, que viene determinado por
    los parámetros a pasar a la consulta SQL.
    El parámetro «Comentario» se tratará con LIKE y debe incluir los comodines.
    No se agregan aquí. Si la primera letra es `!`, entonces se hará un
    NOT LIKE.
    El parámetro «serie» se utiliza tanto en movimientos de stock como en
    los movimientos de serie para los ajustes manuales desde el propio Murano.
    Si serie es None, no se aplica. Si es '!MAN' se hace un <> 'MAN' y si es
    'MAN' se hace un Serie[Documento] = 'MAN';
    """
    almacen = "GTX"
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
    totales = conn.run_sql(sql)
    for total in totales:
        calidad = total['CodigoTalla01_']
        unidad = total['UnidadMedida1_']
        if unidad == 'M2':
            totalmetros = float(total['Unidades'])
            metros[calidad] += totalmetros
        else:
            totalkilos = float(total['Unidades'])
            kilos[calidad] += totalkilos
    # Bultos y la dimensión adicional (metros cuadrados o kilos) de otra:
    # (Aunque también se podría haber obtenido todo de aquí, pero así me
    # aseguro --double-check-- de que es coherente entre las 2 tablas)
    sql = """USE GEOTEXAN;
             SELECT *
               FROM MovimientoArticuloSerie
              WHERE CodigoEmpresa = '10200'
                AND Fecha >= '{}'
                AND Fecha < '{}'
                AND CodigoArticulo = '{}'
                AND CodigoAlmacen = '{}'
                AND OrigenDocumento = {}
              """.format(fini, ffin, codigo, almacen, origen_documento)
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
    totales = conn.run_sql(sql)
    for total in totales:
        calidad = total['CodigoTalla01_']
        unidad = total['UnidadMedida1_']
        bultos[calidad] += total['UnidadesSerie']
        if unidad == 'ROLLO' and total['MetrosCuadrados']: #No C que, va por kg
            totalkilos = float(total['PesoNeto_'])
            kilos[calidad] += totalkilos
        else:   # Será cero para BALAS, BIGBAG y CAJAS, pero por... belleza.
            totalmetros = float(total['MetrosCuadrados'])
            metros[calidad] += totalmetros
    sumbultos = sum([bultos[i] for i in bultos])
    summetros = sum([metros[i] for i in metros])
    sumkilos = sum([kilos[i] for i in kilos])
    return (round(sumbultos, 2), round(summetros, 2), round(sumkilos, 2))


def get_volcados_api(producto_murano, fini, ffin):
    """
    Devuelve los movimientos de series de tipo FAB (las que proceden del API
    de ginn)  en Murano con fecha de registro entre las recibidas para contar
    los bultos.
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
            SerieDocumento <> 'MAN'
    Bajas:
        MovimientoStock:
            TipoMovimiento = 2 (salida)
            OrigenMovimiento = 'F' (Fabricación)
            CodigoCcanal = ''
        MovimientoArticuloSerie:
            OrigenDocumento = 11 (Salida de stock)
            Comentario NOT LIKE 'Consumo%'
            SerieDocumento <> 'MAN'
    """
    # Lo primero son las altas:
    altas = get_volcados(producto_murano, fini, ffin, 1, 'F', '', 2,
                         serie="!MAN")
    # Ahora las bajas por eliminación desde partes, no por consumo.
    bajas = get_volcados(producto_murano, fini, ffin, 2, 'F', '', 11,
                         '!Consumo%', serie="!MAN")
    # Y ahora las sumo (los movimientos de salida vienen en positivo de Murano
    # y viene todo sumado, sin desglose por calidades).
    sumbultos = altas[0] - bajas[0]
    summetros = altas[1] - bajas[1]
    sumkilos = altas[2] - bajas[2]
    return (round(sumbultos, 2), round(summetros, 2), round(sumkilos, 2))


def get_bajas_consumo(producto_murano, fini, ffin):
    """
    Devuelve los movimientos de series de tipo FAB (las que proceden del API
    de ginn) con fecha de registro entre las recibidas y que sean de consumos.
    Tanto de balas en las partidas de carga como de bigbags en los partes de
    embolsado. Son:
    MovimientoArticuloSerie:
        OrigenDocumento = 11 (Salida de stock)
        Comentario LIKE 'Consumo%'
        SerieDocumento <> 'MAN'
    MovimientoStock:
        TipoMovimiento = 2 (salida)
        OrigenMovimiento = 'F' (Fabricación)
        CodigoCanal: CONSFIB|CONSBB
    """
    consumos_balas = get_volcados(producto_murano, fini, ffin, 2, 'F',
                                  'CONSFIB', 11, 'Consumo bala%', '!MAN')
    consumos_bigbags = get_volcados(producto_murano, fini, ffin, 2, 'F',
                                    'CONSBB', 11, 'Consumo bigbag%', '!MAN')
    sumbultos = consumos_balas[0] + consumos_bigbags[0]
    summetros = consumos_balas[1] + consumos_bigbags[1]
    sumkilos = consumos_balas[2] + consumos_bigbags[2]
    return (round(sumbultos, 2), round(summetros, 2), round(sumkilos, 2))


def get_ajustes_murano(producto_murano, fini, ffin):
    """
    Ajustes manuales:
        MovimientoStock:
            TipoMovimiento = 2 (salida)
            OrigenMovimiento = 'S' (Movimiento de salida)
            Serie = 'MAN'
        MovimientoArticuloSerie:
            OrigenDocumento = 11 (Salida de stock)
            SerieDocumento = 'MAN'
    """
    # Eliminaciones manuales, movimientos manuales de salida por ajustes...
    # El código canal a None hará que no se use ese parámetro en el SQL
    ajustes = get_volcados(producto_murano, fini, ffin, 2, 'S', None,
                           11, serie='MAN')
    sumbultos, summetros, sumkilos = ajustes
    return (round(sumbultos, 2), round(summetros, 2), round(sumkilos, 2))


# pylint: disable=too-many-branches
def get_produccion(producto_ginn, fini, ffin, strict=False):
    """
    Devuelve todos la producción del producto entre las fechas. Se obtiene de
    ginn.
    En función del parámetro strict, si es True solo tiene en cuenta la hora
    de finalización del parte. Da igual si está verificado o no.
    Un rollo fabricado a las 22:15 del 12 de enero no se contará como
    producción del día 12, sino del 13.
    **Es la opción recomendada si se va a comparar con las cifras de
    consulta_producido.py de ginn.** (En ginn la "unidad de búsqueda" son los
    partes de producción porque se calculan rendimientos en base a turnos
    de producción de ocho horas o partes completos)
    Si es False cuenta como fecha para la comparación con fini y ffin la
    fecha **real** de alta del artículo en la base de datos. Da igual si un
    rollo se dio de alta el día 15 del mes con fecha del parte 10 para
    corregir un error del día 10. Ese rollo contará como producido el 15.
    **Es la opción recomendada para comparar con las cifras de Murano, ya que
    en la API de ginn cada rollo entra en Murano unos segundos después de
    crearse en ginn. No se espera a que se verifique el parte. Ni siquiera a
    que acabe el turno. Rollo fabricado, rollo que está disponible en Murano.**
    Toda la producción se hacen sobre el almacén GTX. No es necesario filtrar
    por almacén.
    """
    bultos = {'A': 0, 'B': 0, 'C': 0}
    metros = {'A': 0.0, 'B': 0.0, 'C': 0.0}
    kilos = {'A': 0.0, 'B': 0.0, 'C': 0.0}
    # pylint: disable=no-member
    if producto_ginn.es_clase_c():  # Los productos C se pesan. No van en parte
        strict = True
    if not strict:
        PDP = pclases.ParteDeProduccion
        A = pclases.Articulo
        pdps = PDP.select(pclases.AND(PDP.q.fechahorafin >= fini,
                                      PDP.q.fechahorafin < ffin,
                                      A.q.parteDeProduccionID == PDP.q.id,
                                      A.q.productoVentaID == producto_ginn.id))
        # Porque el groupBy necesitaría un poco de low-level en el SQLObject:
        tratados = []
        for pdp in tqdm(pdps, desc="Producción {}".format(producto_ginn.puid),
                        leave=False):
            if pdp in tratados:
                continue    # Ya contado, me lo salto.
            tratados.append(pdp)
            for a in tqdm(pdp.articulos, desc=pdp.puid, leave=False):
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
    else:   # En vez de por partes, filtro por fecha de registro **real** en
            # la base de datos de cada artículo.
        articulos = query_articulos(producto_ginn, fini, ffin)
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
    sumbultos = sum([bultos[i] for i in bultos])
    summetros = sum([metros[i] for i in metros])
    sumkilos = sum([kilos[i] for i in kilos])
    return (round(sumbultos, 2), round(summetros, 2), round(sumkilos, 2))


def query_articulos(producto, fini, ffin):
    """
    Devuelve los registros Articulo de ginn comprendidos entre las fechas
    recibidas. Los artículos en sí no guardan la fecha y hora de fabricación.
    Son los rollo/bala/bala_cable/rollo_c/etc. los que lo hacen.
    """
    articulos = []
    tablas = (pclases.Bala, pclases.BalaCable, pclases.Caja, pclases.Bigbag,
              pclases.Rollo, pclases.RolloC)
    # PLAN: Esto se podría optimizar. Es tontería recorrer todos los artículos
    # entre las dos fechas por cada producto que el script va a comprobar
    # cuando después se va a filtrar para quedarnos con los que coincidan.
    for tabla in tablas:
        # pylint: disable=no-member
        rs = tabla.select(pclases.AND(tabla.q.fechahora >= fini,
                                      tabla.q.fechahora < ffin))
        for item in tqdm(rs, desc="Artículos (strict)", total=rs.count()):
            if item.articulo.productoVenta == producto:
                articulos.append(item.articulo)
    return articulos

# pylint:disable=too-many-branches
def get_consumos_ginn(producto_ginn, fini, ffin):
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
    bultos = {'A': 0, 'B': 0, 'C': 0}
    metros = {'A': 0.0, 'B': 0.0, 'C': 0.0}
    kilos = {'A': 0.0, 'B': 0.0, 'C': 0.0}
    PDP = pclases.ParteDeProduccion
    # pylint: disable=no-member
    pdps = PDP.select(pclases.AND(PDP.q.fecha >= fini,
                                  PDP.q.fecha < ffin))
    # pylint: disable=too-many-nested-blocks
    pcs_tratadas = []
    for pdp in tqdm(pdps, desc="Consumos {}".format(producto_ginn.descripcion)):
        # Si estamos buscando consumos de bigbags miro directamente en los
        # partes los bigbags asociados.
        if producto_ginn.es_bigbag():
            for bb in pdp.bigbags:
                articulo = bb.articulo
                if articulo.productoVenta == producto_ginn:
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
        # Pero si lo que estamos buscando son consumos de fibra, miro las
        # partidas de carga. Como dos partes pueden estar asociados a la
        # misma partida de carga, llevo el control de los ya tratados.
        elif producto_ginn.es_bala():
            try:
                pc = pdp.partidaCarga
                if not pc:  # El parte no ha consumido nada.
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
                    if articulo.productoVenta == producto_ginn:
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
    sumbultos = sum([bultos[i] for i in bultos])
    summetros = sum([metros[i] for i in metros])
    sumkilos = sum([kilos[i] for i in kilos])
    return (round(sumbultos, 2), round(summetros, 2), round(sumkilos, 2))


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
    if not "/" in cadfecha:
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
                   if f.endswith('.xls')], key=os.path.getctime)
    except ValueError:
        print("Fichero .xls no encontrado en `{}`.".format(ruta))
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


def load_inventario(fich_inventario):
    """
    Devuelve los datos del excel/ods del inventario como un Dataset de tablib.
    """
    book = tablib.Databook().load(None, open(fich_inventario, "r+b").read())
    sheets = book.sheets()
    assert 2 <= len(sheets) <= 3, "El fichero '{}' no parece ser "\
                                  "válido.".format(fich_inventario)
    found = False
    data = None
    for data in sheets:
        if "totales" in data.__repr__().lower():
            found = True
            break
    if not found:
        sys.stderr.write("Hoja de inventario no encontrada en {}.".format(
            fich_inventario))
        sys.exit(3)
    return data


def do_inventario(producto, totales, desglose):
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
           ArticulosSeries.FechaInicial AS fecha_fabricacion
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
             ArticulosSeries.CodigoTalla01_;
    """.format(codarticulo, codalmacen)
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
                         rs_desglose['fecha_fabricacion']]
        desglose.append(fila_desglose)


def main():
    """
    Rutina principal.
    """
    # # Parámetros
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
        subprocess.Popen('gvim "{}"'.format(args.fsalida))
    # # Pruebas
    productos = []
    results = []    # Resultados de las comprobaciones para cada `productos`.
    if args.codigos_productos:
        for codigo in tqdm(args.codigos_productos,
                           desc="Buscando productos ginn"):
            producto = murano.ops.get_producto_ginn(codigo)
            productos.append(producto)
    else:
        for pv in tqdm(pclases.ProductoVenta.select(orderBy="id"),
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
    data_inventario = load_inventario(fich_inventario)
    data_res = tablib.Dataset(title="Desviaciones")
    inventario = tablib.Dataset(title="Totales")
    desglose = tablib.Dataset(title="Desglose")
    data_res.headers = ['Código', 'Producto',
                        'Ini. (bultos)', 'Ini. (m²)', 'Ini. (kg)',
                        'Prod. (bultos)', 'Prod. (m²)', 'Prod. (kg)',
                        'Ventas (bultos)', 'Ventas (m²)', 'Ventas (kg)',
                        'Cons. (bultos)', 'Cons. (m²)', 'Cons. (kg)',
                        'Ajustes (bultos)', 'Ajustes (m²)', 'Ajustes (kg)',
                        'Fin. (bultos)', 'Fin. (m²)', 'Fin. (kg)',
                        'Dif. (bultos)', 'Dif. (m²)', 'Dif. (kg)']
    inventario.headers = ['Almacén', 'Familia', 'Código producto',
                          'Descripción', 'Partida', 'Calidad', 'Bultos',
                          'Peso neto', 'Peso bruto', 'Metros cuadrados']
    desglose.headers = ['Almacén', 'Familia', 'Código producto',
                        'Descripción', 'Código trazabilidad', 'Partida',
                        'Calidad', 'Bultos', 'Peso neto', 'Peso bruto',
                        'Metros cuadrados', 'Fecha importación a Murano']
    for producto in tqdm(productos, desc="Productos"):
        res = cuentalavieja(producto, data_inventario, fini, ffin, report,
                            data_res, args.debug)
        results.append((producto, res))
        do_inventario(producto, inventario, desglose)
    fallos = [p for p in results if not p[1]]
    report.write("Encontradas {} desviaciones: {}".format(
        len(fallos), "; ".join(['PV{}'.format(p[0].id) for p in fallos])))
    report.write("\n\nFecha y hora de generación del informe: {}".format(
        datetime.datetime.now().strftime("%d/%m/%Y %H:%M")))
    report.write("___\n\n")
    report.close()
    fout = args.fsalida.replace(".md", ".xls")
    book = tablib.Databook((data_res, inventario, desglose))
    with open(fout, 'wb') as f:
        # pylint: disable=no-member
        f.write(book.xls)


if __name__ == "__main__":
    main()
