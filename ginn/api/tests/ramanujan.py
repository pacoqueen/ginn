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
from lib.tqdm.tqdm import tqdm  # Barra de progreso modo texto.
sys.argv = _argv


def cuentalavieja(producto_ginn, fini, ffin, fsalida):
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
    """
    report = open(fsalida, "a", 0)
    res = False
    # 0.- Localizo el producto en Murano.
    producto_murano = murano.ops.get_producto_murano(producto_ginn)

    # TODO: Magic happens here.
    report.write(producto_murano.CodigoArticulo, producto_ginn.descripcion)

    # -1.- Escribo el resultado.
    if res:
        report.write(" [OK]\n")
    else:
        report.write(" [KO]\n")
    report.close()
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
    parser.add_argument("fecha_inicial", dest="fini")
    parser.add_argument("fecha_final", dest="ffin")
    parser.add_argument("-p", "--productos", dest="codigos_productos",
                        help="Códigos de productos a comprobar.",
                        nargs="+", default=[])
    ahora = datetime.datetime.today().strftime("%Y%m%d_%H")
    parser.add_argument("-o", dest="fsalida",
                        help="Guardar resultados en fichero de salida.",
                        default="%s_ramanujan.txt" % (ahora))
    parser.add_argument("-v", "--view", dest="ver_salida",
                        help="Abre el fichero de salida en un editor externo.",
                        default=False, action='store_true')
    args = parser.parse_args()
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
    for producto in tqdm(productos, desc="Productos"):
        res = cuentalavieja(producto, args.fini, args.ffin, args.fsalida)
        results.append(res)


if __name__ == "__main__":
    main()
