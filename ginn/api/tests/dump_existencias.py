#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pruebas de exportación de ginn e importación en Murano.
"""

from __future__ import print_function

import sys
import os
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
from lib.tqdm.tqdm import tqdm  # Barra de progreso modo texto.
sys.argv = _argv


def insertar_pv(guid_proceso):
    """
    Selecciona todos los artículos de productos de venta y devuelve la lista
    de instrucciones SQL a ejecutar para lanzarlas contra las tablas TmpIME
    de MSSQLServer.
    Cada código de artículo se compone de 2 instrucciones SQL: movimiento
    de serie y movimiento de stock.
    """
    res = []
    for articulo in tqdm(pclases.Articulo.select(),
                         total=pclases.Articulo.select().count()):
        sql = murano.ops.create_articulo(articulo, guid_proceso=guid_proceso,
                                         simulate=True)
        res.append(sql)
    return res


def insertar_pc(guid_proceso):
    """
    Selecciona todos los productos de compra y devuelve una lista de
    instrucciones SQL de movimiento de stock para lanzarlas contra las
    TmpIME de MSSQLServer.
    """
    res = []
    prodscompra = pclases.ProductoCompra.select(
        pclases.ProductoCompra.q.existencias > 0)
    for pc in tqdm(prodscompra,
                   total=prodscompra.count()):
        for almacen in pclases.Almacen.select():
            cantidad = pc.get_existencias(almacen)
            if cantidad > 0:
                try:
                    sql = murano.ops.update_stock(pc, cantidad, almacen,
                                                  guid_proceso=guid_proceso,
                                                  simulate=True)
                except (AssertionError, IndexError):
                    print("El producto PC{} ({}) no se encuentra"
                          "en Murano.".format(pc.id, pc.descripcion),
                          file=sys.stderr)
                    continue
            res.append(sql)
    return res


def ejecutar_proceso(connection, sql_pv, sql_pc, guid_proceso):
    """
    Ejecuta todas las instrucciones INSERT de productos de venta y de compra
    y posteriormente lanza el proceso de importación de Murano.
    """
    for sql in tqdm(sql_pv, sql_pc):
        connection.run_sql(sql)
        murano.ops.fire(guid_proceso)


def main():
    """
    Rutina principal.
    """
    # # Parámetros
    parser = argparse.ArgumentParser(
        description="Volcado de existencias inicial a Murano.")
    parser.add_argument("-r", "--run", action="store_true",
                        help="Conecta a MSSQLServer y ejecuta el proceso "
                             "Murano. Por defecto solo simula.",
                        default=False)
    args = parser.parse_args()
    # # Volcado
    if args.run:
        print("Conectando a la base de datos...")
        con = murano.connection.Connection()
        guid_proceso = murano.ops.genera_guid(con)
    else:
        print("Simulando conexión a la base de datos...")
        murano.connection.DEBUG = True
        murano.ops.DEBUG = True
        guid_proceso = murano.ops.simulate_guid()
    print("Insertando productos de compra...")
    sql_pc = insertar_pc(guid_proceso)
    print("Insertando productos de venta...")
    sql_pv = insertar_pv(guid_proceso)
    if args.run:
        print("Lanzando proceso de importación...")
        ejecutar_proceso(con, sql_pv, sql_pc, guid_proceso)
    else:
        print("Consultas SQL generadas:")
        for sql in sql_pc + sql_pv:
            print(sql)


if __name__ == "__main__":
    main()
