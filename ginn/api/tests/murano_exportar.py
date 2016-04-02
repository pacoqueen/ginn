#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exporta clientes, proveedores, domicilios (obras) y contactos a tres
ficheros CSV: clientesproveedores.csv, domicilios.csv y contactos.csv
"""

import argparse
import sys
import os

# pylint: disable=invalid-name
parser = argparse.ArgumentParser(description="Script para exportar datos "
                                 "de ginn con el formato esperado por las "
                                 "guías de importación de Murano.")
parser.add_argument("-a", "--productos", "--articulos",
                    help="Exporta todos los productos de compra y venta.",
                    default=False, action="store_true")
parser.add_argument("-c", "--clientes",
                    help="Exporta todos los clientes con actividad en los"
                    " últimos 2 años.",
                    default=False, action="store_true")
parser.add_argument("-p", "--proveedores",
                    help="Exporta todos los proveedores con actividad en los"
                    " últimos 2 años.",
                    default=False, action="store_true")
parser.add_argument("-t", "--todo",
                    help="Exporta clientes, productos y proveedores.",
                    default=False, action="store_true")


def do_imports():
    """
    Desde el framework se hacen algunas cosas sucias con los argumentos,
    así que tengo que hacer una importación limpia a posteriori.
    """
    sys.argv = []
    ruta_ginn = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "ginn"))
    sys.path.append(ruta_ginn)
    # from framework import pclases


def main():
    """
    Si existen los ficheros destino, los elimina. Después exporta los
    registros indicados en los parámetros del comando.
    """
    if len(sys.argv) == 1:
        parser.print_help()
    args = parser.parse_args()
    do_imports()
    # pylint: disable=import-error
    from api import murano
    destproductos = 'productos.csv'
    destclientesproveedores = 'clientesproveedores.csv'
    destdomicilios = 'domicilios.csv'
    destcontactos = 'contactos.csv'
    if args.productos or args.todo:
        try:
            os.unlink(destproductos)
        except OSError:
            pass    # El fichero no existía
        murano.exportar_productos(destproductos)
    if args.clientes or args.proveedores:
        for dest in (destclientesproveedores, destdomicilios, destcontactos):
            try:
                os.unlink(dest)
            except OSError:
                pass    # El fichero no existe
    if args.clientes or args.todo:
        murano.exportar_clientes(destclientesproveedores, destdomicilios,
                                 destcontactos)
    if args.proveedores or args.todo:
        murano.exportar_proveedores(destclientesproveedores)

if __name__ == "__main__":
    main()
