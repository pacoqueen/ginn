#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
> Edgar Frank Codd, el bueno de Ted, propone el modelo relacional de bases
> de datos y el lenguaje de acceso SQL en 1970. Años más tarde llegó Murano
> y se pasó las formas normales por el forro.

Realiza comprobaciones de existencias para corregir incoherencias internas
del propio Murano entre las tablas de (stock de) series y las tablas de
acumulados de existencias.
"""

from __future__ import print_function
from collections import defaultdict
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
# from framework import pclases
from api import murano
from lib.tqdm.tqdm import tqdm  # Barra de progreso modo texto.
sys.argv = _argv


def fix_stock_producto(codigo, fsalida, simulate=True):
    """
    Recorre la tabla de series del producto, agrupándolos por almacén, calidad
    y partida. Acumula las dos unidades de medida y corrije la tabla de
    acumulados para el periodo global (99, que representa el total).
    """
    report = open(fsalida, "a", 0)
    if simulate:
        report.write("Simulando stock de producto %s... " % codigo)
    else:
        report.write("Corrigiendo stock de producto %s... " % codigo)
    # 0.- Localizo el producto en Murano.
    prod = murano.ops.get_producto_murano(codigo)
    # 1.- Busco las series disponibles del producto.
    resultset = search_series(prod)
    # 2.- Agrupo por almacén, calidad y partida.
    data = group_data(resultset)
    # 3.- Actualizo la tabla de acumulados.
    res = update_acumulados(data, prod, simulate)
    if res:
        report.write(" [OK]\n")
    else:
        report.write(" [KO]\n")
    report.close()
    return res


def search_series(producto):
    """
    Lanza una consulta SQL contra la base de datos de Murano y revuelve una
    lista de diccionarios con los nombres de las columnas como clave y
    los datos de cada registro como valores.
    """
    rs = []
    conn = murano.connection.Connection()
    sql = """SELECT CodigoAlmacen,
                    Partida,
                    CodigoTalla01_,
                    COUNT(UnidadesSerie) AS bultos,
                    SUM(PesoNeto_) AS peso_neto,
                    SUM(MetrosCuadrados) AS metros_cuadrados
               FROM {}.dbo.ArticulosSeries
              WHERE CodigoEmpresa = '{}'
                AND CodigoArticulo = '{}'
                AND UnidadesSerie <> 0
             GROUP BY CodigoAlmacen,
                      CodigoTalla01_,
                      Partida;""".format(conn.get_database(),
                                         murano.connection.CODEMPRESA,
                                         producto.CodigoArticulo)
    rs = conn.run_sql(sql)
    return rs


def group_data(rs):
    """
    Agrupa los datos por almacén, calidad y partida, conteniendo el diccionario
    el total de bultos, metros cuadrados y peso neto.
    """
    res = defaultdict(lambda: defaultdict(dict))
    for registro in rs:
        almacen = registro['CodigoAlmacen']
        partida = registro['Partida']
        calidad = registro['CodigoTalla01_']
        bultos = registro['bultos']
        peso_neto = registro['peso_neto']
        metros_cuadrados = registro['metros_cuadrados']
        res[almacen][calidad][partida] = {'bultos': bultos,
                                          'peso_neto': peso_neto,
                                          'metros_cuadrados': metros_cuadrados}
    return res


# pylint: disable=too-many-branches,too-many-locals
def update_acumulados(data, producto, simulate=True):
    """
    Lanza una consulta SQL contra la tabla de acumulados para cambiar los
    totales del producto en cada dimensión, por partida, almacén y calidad,
    según los datos recibidos.
    El resto de registros los pone a cero por si hubiera cantidades negativas
    o algo en otros almacenes o partidas sin stock.
    """
    # Reset de todos los registros 99 del producto.
    if simulate:
        ejercicio = datetime.date.today().year
        codempresa = 10200
        database = "GEOTEXAN"
    else:
        conn = murano.connection.Connection()
        ejercicio = conn.run_sql("""SELECT MAX(Ejercicio)
                                    FROM {}.dbo.AcumuladoStock
                                    WHERE CodigoEmpresa = {};
                                 """.format(conn.get_database(),
                                            murano.connection.CODEMPRESA))[0]
        codempresa = murano.connection.CODEMPRESA
        database = conn.get_database()
    periodo = 99    # En Murano, 99 = total. Si no, es el mes del 1 al 12.
    sql = """UPDATE {}.dbo.AcumuladoStock
             SET UnidadSaldo = 0,
                 UnidadSaldoTipo_ = 0
             WHERE CodigoEmpresa = {}
               AND Ejercicio = {}
               AND Periodo = {}
          """.format(database,
                     codempresa,
                     ejercicio,
                     periodo)
    if simulate:
        print("SQL:", sql)
        res = True
    else:
        res = conn.run_sql(sql)
    # pylint: disable=too-many-nested-blocks
    if res:
        for almacen in data:
            if res:
                for calidad in data[almacen]:
                    if res:
                        for partida in data[almacen][calidad]:
                            dicpartida = data[almacen][calidad][partida]
                            bultos = dicpartida['bultos']
                            stock = dicpartida['metros_cuadrados']
                            if not stock:
                                stock = dicpartida['peso_neto']
                            sql = """UPDATE {}.dbo.AcumuladoStock
                                     SET UnidadSaldo = {},
                                         UnidadSaldoTipo_ = {}
                                     WHERE CodigoEmpresa = {}
                                       AND Ejercicio = {}
                                       AND Periodo = {}
                                       AND CodigoAlmacen = '{}'
                                       AND Partida = '{}'
                                       AND CodigoArticulo = '{}';
                                  """.format(database,
                                             bultos,
                                             stock,
                                             murano.connection.CODEMPRESA,
                                             ejercicio,
                                             periodo,
                                             almacen,
                                             partida,
                                             producto.CodigoArticulo)
                            if simulate:
                                print("SQL:", sql)
                                res = True
                            else:
                                conn = murano.connection.Connection()
                                res = conn.run_sql(sql)
    return res


def main():
    """
    Rutina principal.
    """
    # # Parámetros
    parser = argparse.ArgumentParser(
        description="Soy Ted Codd abrazado a mi premio Turing revolviéndome"
                    " en mi tumba.")
    parser.add_argument("-p", "--productos", dest="codigos_productos",
                        help="Códigos de productos a comprobar.",
                        nargs="+", default=[])
    parser.add_argument("-n", "--dry-run", dest="simulate",
                        help="Simular. No hace cambios en la base de datos.",
                        default=False, action='store_true')
    ahora = datetime.datetime.today().strftime("%Y%m%d_%H")
    parser.add_argument("-o", dest="fsalida",
                        help="Guardar resultados en fichero de salida.",
                        default="%s_sr_lobo.txt" % (ahora))
    parser.add_argument("-v", "--view", dest="ver_salida",
                        help="Abre el fichero de salida en un editor externo.",
                        default=False, action='store_true')
    args = parser.parse_args()
    if args.ver_salida:
        if not os.path.exists(args.fsalida):
            open(args.fsalida, 'a').close()
        subprocess.Popen('gvim "{}"'.format(args.fsalida))
    # # Pruebas
    if args.codigos_productos:
        for codigo in tqdm(args.codigos_productos, desc="Productos"):
            fix_stock_producto(codigo, args.fsalida, args.simulate)


if __name__ == "__main__":
    main()
