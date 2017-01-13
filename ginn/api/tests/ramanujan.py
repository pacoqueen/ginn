#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
El enfermizo hindú era un hacha calculando mentalmente. Me conformo con que
este script sea capaz de cuadrar los números de existencias, producciones,
ventas y consumos de cada producto para la detección temprana de desviaciones.
"""

from __future__ import print_function
import datetime
import sys
import os
import subprocess
import logging
import argparse
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


DEFAULT_FINI = datetime.date(2016, 5, 31)  # La fecha de implantación de Murano


# pylint: disable=too-many-locals
def cuentalavieja(producto_ginn, fini, ffin, report, dev=False):
    """
    Recibe un producto de ginn y comprueba que entre las fechas fini y ffin
    (recibidas como `datetimes`) es correcto el cálculo
    existencias_1 = existencias_0 + entradas_0->1 - salidas_0->1
    Donde:
    entradas_0->1 = producción_0->1
    salidas_0->1 = ventas_albaranes_0->1 + consumos_0->1

    Los datos de existencias los obtiene de Murano.
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
    if not dev:
        producto_murano = murano.ops.get_producto_murano(producto_ginn)
        existencias_ini = get_existencias(producto_murano, fini)
        existencias_fin = get_existencias(producto_murano, ffin)
        ventas = get_ventas(producto_murano, fini, ffin)
        volcados_murano = get_altas(producto_murano, fini, ffin)
        bajas_volcadas_murano = get_bajas_consumo(producto_murano, fini, ffin)
    else:
        producto_murano = None
        existencias_ini = 0, 0, 0
        existencias_fin = 0, 0, 0
        ventas = 0, 0, 0
        volcados_murano = 0, 0, 0
        bajas_volcadas_murano = 0, 0, 0
    # 1.- Obtengo los datos de producción y consumos del ERP.
    produccion = get_produccion(producto_ginn, fini, ffin)
    consumos = get_consumos(producto_ginn, fini, ffin)
    # 2.- Cabecera del informe de resultados:
    if not dev:
        # pylint: disable=no-member
        report.write("{}: {}\n".format(producto_murano.CodigoArticulo,
                                       producto_ginn.descripcion))
    else:
        report.write("PV{}: {}\n".format(producto_ginn.id,
                                         producto_ginn.descripcion))
    # 3.- Compruebo que los datos del ERP y Murano son iguales:
    if produccion != volcados_murano:
        report.write("> Producción ginn: {}; entradas Murano: {}\n".format(
            produccion, volcados_murano))
    if consumos != bajas_volcadas_murano:
        report.write("> Consumos ginn: {}; bajas Murano: {}\n".format(
            consumos, bajas_volcadas_murano))
    entradas = produccion
    # Las salidas vienen en positivo. Si quiero restar, hay que *-1
    salidas = [-sum(x) for x in zip(ventas, consumos)]
    total = [-sum(x) for x in zip(existencias_ini, entradas, salidas)]
    desviacion = [sum(x) for x in zip(existencias_fin, total)]
    res = desviacion == [0, 0, 0]
    # 4.- Escribo los resultados al report.
    report.write("Existencias inicales: {}\n".format(existencias_ini))
    report.write("Existencias finales: {}\n".format(existencias_fin))
    report.write("Producción: {}\n".format(produccion))
    report.write("Ventas: {}\n".format(ventas))
    report.write("Consumos: {}\n".format(consumos))
    if not res:
        report.write("**")
    report.write("Desviación")
    if not res:
        report.write("**")
    report.write(": {}\n".format(desviacion))
    report.write("-"*70)
    if res:
        report.write(" _[OK]_ \n")
    else:
        report.write(" **[KO]**\n")
    report.write("\n")
    # 5.- Y devuelvo si todo cuadra (True) o hay alguna desviación (False)
    return res


def get_existencias(producto, fecha):
    """
    Devuelve las existencias que Murano tenía en la fecha `fecha`. Se hace
    filtrando los movimientos de series por la fecha recibida (no incluida).
    No es un métido muy exacto o fiable, pero no hay otra forma.
    Devuelve una tupla (bultos, m², kg).
    Obtiene todos los datos de la tabla ArticulosSerie.
    **Solo se consulta sobre el almacén GTX.**
    """
    # PLAN: ¿Y si las recibo por parámetro en la línea de comandos o desde un
    # fichero externo?
    almacen = "GTX"
    fini = DEFAULT_FINI.strftime("%Y-%m-%d")
    ffin = fecha.strftime("%Y-%m-%d")
    # pylint: disable=no-member
    codigo = murano.ops.get_producto_murano(producto).CodigoArticulo
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
        --  AND ArticulosSeries.Partida = 'P-11253'
          AND ArticulosSeries.CodigoAlmacen = '{}'
          AND ArticulosSeries.FechaInicial >= '{}'
          AND ArticulosSeries.FechaInicial < '{}'
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
          ArticulosSeries.CodigoTalla01_;""".format(codigo, almacen, fini,
                                                    ffin)
    conn = connection.Connection()
    totales = conn.run_sql(sql)
    #  No debería haber series sin calidad (''), pero por si acaso las cuento:
    bultos = {'A': 0, 'B': 0, 'C': 0, '': 0}
    metros = {'A': 0.0, 'B': 0.0, 'C': 0.0, '': 0.0}
    kilos = {'A': 0.0, 'B': 0.0, 'C': 0.0, '': 0.0}
    for total in totales:
        calidad = total['calidad']
        bultos[calidad] += total['bultos']
        metros[calidad] += total['metros_cuadrados']
        kilos[calidad] += total['peso_neto']
    sumbultos = sum([bultos[i] for i in bultos])
    summetros = sum([metros[i] for i in metros])
    sumkilos = sum([kilos[i] for i in kilos])
    return (sumbultos, summetros, sumkilos)


def get_ventas(producto, fini, ffin):
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
    # pylint: disable=no-member
    codigo = murano.ops.get_producto_murano(producto).CodigoArticulo
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
                AND CodigoAlmacen = {}'
              ORDER BY FechaRegistro;""".format(fini, ffin, codigo, almacen)
    conn = connection.Connection()
    totales = conn.run_sql(sql)
    for total in totales:
        calidad = total['CodigoTalla01_']
        unidad = total['UnidadMedida1_']
        bultos[calidad] += total['Unidades2_']
        if unidad == 'M2':
            totalmetros = total['Unidades']
            totalkilos = total['PesoNeto_']
        else:
            totalkilos = total['Unidades']
            totalmetros = total['MetrosCuadrados']
        metros[calidad] += totalmetros
        kilos[calidad] += totalkilos
    sumbultos = sum([bultos[i] for i in bultos])
    summetros = sum([metros[i] for i in metros])
    sumkilos = sum([kilos[i] for i in kilos])
    return (sumbultos, summetros, sumkilos)


# pylint: disable=too-many-arguments
def get_volcados(producto, fini, ffin, origen_documento, tipo_movimiento,
                 origen_movimiento, codigo_canal, comentario=None):
    """
    Devuelve los volcados realizados de cada tipo, que viene determinado por
    los parámetros a pasar a la consulta SQL.
    El parámetro «Comentario» se tratará con LIKE y debe incluir los comodines.
    No se agregan aquí. Si la primera letra es `!`, entonces se hará un
    NOT LIKE.
    """
    almacen = "GTX"
    fini = fini.strftime("%Y-%m-%d")
    ffin = ffin.strftime("%Y-%m-%d")
    # pylint: disable=no-member
    codigo = murano.ops.get_producto_murano(producto).CodigoArticulo
    bultos = {'A': 0, 'B': 0, 'C': 0, '': 0}
    metros = {'A': 0.0, 'B': 0.0, 'C': 0.0, '': 0.0}
    kilos = {'A': 0.0, 'B': 0.0, 'C': 0.0, '': 0.0}
    # Aquí primero se obtienen 2 dimensiones de una tabla
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
            comentario = comentario[1:]
            sql += "AND Comentario NOT LIKE '{}' ".format(comentario)
        else:
            sql += "AND Comentario LIKE '{}' ".format(comentario)
    sql += "ORDER BY FechaRegistro;"
    conn = connection.Connection()
    totales = conn.run_sql(sql)
    for total in totales:
        calidad = total['CodigoTalla01_']
        unidad = total['UnidadMedida1_']
        bultos[calidad] += total['Unidades2_']
        if unidad == 'M2':
            totalmetros = total['Unidades']
            metros[calidad] += totalmetros
        else:
            totalkilos = total['Unidades']
            kilos[calidad] += totalkilos
    # Y la dimensión adicional (metros cuadrados o kilos) de otra:
    # (Aunque también se podría haber obtenido todo de aquí, pero así me
    # aseguro --double-check-- de que es coherente entre las 2 tablas)
    sql = """USE GEOTEXAN;
             SELECT *
               FROM MovimientoStock
              WHERE CodigoEmpresa = '10200'
                AND Fecha >= '{}'
                AND Fecha < '{}'
                AND CodigoArticulo = '{}'
                AND CodigoAlmacen = '{}'
                AND TipoMovimiento = {}
                AND OrigenMovimiento = '{}'
                AND CodigoCanal = '{}'
              ORDER BY FechaRegistro;""".format(fini, ffin, codigo, almacen,
                                                tipo_movimiento,
                                                origen_movimiento,
                                                codigo_canal)
    conn = connection.Connection()
    totales = conn.run_sql(sql)
    for total in totales:
        calidad = total['CodigoTalla01_']
        unidad = total['UnidadMedida1_']
        if unidad == 'ROLLO' and total['MetrosCuadrados'] != 0:
            totalkilos = total['PesoNeto_']
            kilos[calidad] += totalkilos
        else:   # Serán cero seguro, pero por... belleza.
            totalmetros = total['MetrosCuadrados']
            metros[calidad] += totalmetros
    sumbultos = sum([bultos[i] for i in bultos])
    summetros = sum([metros[i] for i in metros])
    sumkilos = sum([kilos[i] for i in kilos])
    return (sumbultos, summetros, sumkilos)


def get_altas(producto, fini, ffin):
    """
    Devuelve los movimientos de series de tipo FAB (las que proceden del API
    de ginn)  en Murano con fecha de registro entre las recibidas para contar
    los bultos.
    Busca los movimientos de stock para las unidades: m² o kg.
    Las altas a contar para producción son las entradas **menos** las salidas
    (eliminaciones de artículos) procedentes de fabricación.
    La serie 'FAB' también se podría usar para filtrar, pero con
    el OrigenDocumento 'F' nos vale.
    Altas:
        MovimientoArticuloSerie:
            OrigenDocumento = 2 (Fabricación)
        MovimientoStock:
            tipoMovimiento = 1 (entrada)
            origenMovimiento = 'F' (Fabricación)
            CodigoCanal = ''
    Bajas:
        MovimientoArticuloSerie:
            OrigenDocumento = 11 (Salida de stock)
            Comentario NOT LIKE 'Consumo%'
        MovimientoStock:
            tipoMovimiento = 2 (salida)
            origenMovimiento = 'F' (Fabricación)
            CodigoCcanal = ''
    """
    # Lo primero son las altas:
    altas = get_volcados(producto, fini, ffin, 2, 1, 'F', '')
    # Ahora las bajas por eliminación desde partes, no por consumo.
    bajas = get_volcados(producto, fini, ffin, 11, 2, 'F', '', '!Consumo%',)
    # Y ahora las sumo (los movimientos de salida vienen en positivo de Murano
    # y viene todo sumado, sin desglose por calidades).
    sumbultos = altas[0] - bajas[0]
    summetros = altas[1] - bajas[1]
    sumkilos = altas[2] - bajas[2]
    return (sumbultos, summetros, sumkilos)


def get_bajas_consumo(producto, fini, ffin):
    """
    Devuelve los movimientos de series de tipo FAB (las que proceden del API
    de ginn) con fecha de registro entre las recibidas y que sean de consumos.
    Tanto de balas en las partidas de carga como de bigbags en los partes de
    embolsado. Son:
    MovimientoArticuloSerie:
        OrigenDocumento = 11 (Salida de stock)
        Comentario LIKE 'Consumo%'
    MovimientoStock:
        tipoMovimiento = 2 (salida)
        origenMovimiento = 'F' (Fabricación)
        CodigoCanal: CONSFIB|CONSBB
    """
    consumos_balas = get_volcados(producto, fini, ffin, 11, 2, 'F',
                                  'CONSFIB', 'Consumo%')
    consumos_bigbags = get_volcados(producto, fini, ffin, 11, 2, 'F',
                                    'CONSBB', 'Consumo%')
    sumbultos = consumos_balas[0] + consumos_bigbags[0]
    summetros = consumos_balas[1] + consumos_bigbags[1]
    sumkilos = consumos_balas[2] + consumos_bigbags[2]
    return (sumbultos, summetros, sumkilos)


def get_produccion(producto, fini, ffin, strict=False):
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
    if not strict:
        PDP = pclases.ParteDeProduccion
        A = pclases.Articulo
        pdps = PDP.select(pclases.AND(PDP.q.fechahorafin >= fini,
                                      PDP.q.fechahorafin < ffin,
                                      A.q.parteDeProduccionID == PDP.q.id,
                                      A.q.productoVentaID == producto.id))
        for pdp in tqdm(pdps, desc="Producción {}".format(producto.puid),
                        leave=False):
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
        articulos = pclases.Articulo.select(pclases.AND(
            pclases.Articulo.q.fechahora >= fini,
            pclases.Articulo.q.fechahora < ffin,
            pclases.Articulo.q.productoVentaID == producto.id))
        for a in tqdm(articulos, desc="Artículos"):
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
    return (sumbultos, summetros, sumkilos)


# pylint:disable=too-many-branches
def get_consumos(producto, fini, ffin):
    """
    Devuelve los consumos del producto entre las fechas. Los consumos se toman
    de ginn y la fecha usada para determinar si entra en el filtro es la
    fecha de la partida de carga.
    Las partidas de carga, a diferencia de las producciones, no se vuelcan a
    Murano instantáneamente. Para permitir al operario irlas metiendo poco a
    poco en sus ratos "libres" lo que se hace es ejecutar cada cierto tiempo
    un script que busca las pendientes de volcar y da de baja las balas/bigbag
    en Murano en forma de movimiento de serie FAB en el canal CONS*.
    Todos los consumos se hacen sobre el almacén GTX. No es necesario filtrar
    por almacén.
    """
    bultos = {'A': 0, 'B': 0, 'C': 0}
    metros = {'A': 0.0, 'B': 0.0, 'C': 0.0}
    kilos = {'A': 0.0, 'B': 0.0, 'C': 0.0}
    PDP = pclases.ParteDeProduccion
    # pylint: disable=no-member
    pdps = PDP.select(pclases.AND(PDP.q.fechahorafin >= fini,
                                  PDP.q.fechahorafin < ffin))
    # pylint: disable=too-many-nested-blocks
    for pdp in tqdm(pdps, desc="Consumos {}".format(producto.descripcion)):
        # Si estamos buscando consumos de bigbags miro directamente en los
        # partes los bigbags asociados.
        if producto.es_bigbag():
            for bb in pdp.bigbags:
                articulo = bb.articulo
                if articulo.productoVenta == producto:
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
        # partidas de carga. Aunque dos partes pueden estar asociados a la
        # misma partida de carga, como solo contamos los consumos del producto
        # recibido, me da igual tratar una misma partida en varias llamadas
        # consecutivas. Solo se contará el consumo de un mismo producto una
        # vez. En consecutivas llamadas ya será otro producto y no duplicará
        # el resultado.
        elif producto.es_bala():
            try:
                pc = pdp.partidaCarga
                if not pc:  # El parte no ha consumido nada.
                    continue
            except ValueError:
                # No es un parte de geotextiles.
                pass
            else:
                for bala in pc.balas:
                    articulo = bala.articulo
                    if articulo.productoVenta == producto:
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
    return (sumbultos, summetros, sumkilos)


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


def main():
    """
    Rutina principal.
    """
    # # Parámetros
    parser = argparse.ArgumentParser(
        description="Soy Srinivasa Iyengar Ramanujan.\n"
                    "Calculo entradas y salidas por producto para detectar "
                    "desviaciones en las existencias entre dos fechas.\n"
                    "Todavía no me ha encontrado Hardy, así que de momento"
                    "solo sé hacer los cálculos para productos de venta y "
                    "el almacén principal.")
    def_fini = DEFAULT_FINI.strftime("%d-%m-%Y")
    parser.add_argument("--fecha_inicial", dest="fini", default=def_fini)
    today = datetime.datetime.today().strftime("%d%m%Y")
    parser.add_argument("--fecha_final", dest="ffin", default=today)
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
    fini = parse_fecha(args.fini)
    ffin = parse_fecha(args.ffin)
    # Para evitar problemas con las fechas que incluyen horas, y para que
    # éstas entren en el intervalo, agrego un día a la fecha final y hago
    # el filtro con menor estricto: una producción del 02/01/17 23:00
    # la consideramos como que entra en el día 2, y entraría en el filtro
    # [01/01/17..02/01/17] porque en realidad sería [01/01/17..03/01/17).
    ffin += datetime.timedelta(days=1)
    report = open(args.fsalida, "a", 0)
    report.write("Analizando desde {} a {}, ambas incluidas.\n".format(
        fini.strftime("%d/%m/%Y"), ffin.strftime("%d/%m/%Y")))
    report.write("=========================================================="
                 "\n")
    for producto in tqdm(productos, desc="Productos"):
        res = cuentalavieja(producto, fini, ffin, report,
                            args.debug)
        # TODO: ¿Has visto el tablib? ¿Has visto que exporta a Excel? Pues eso.
        results.append(res)
    report.close()


if __name__ == "__main__":
    main()
