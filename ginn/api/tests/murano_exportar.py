#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys, os

parser = argparse.ArgumentParser(description = "Script para exportar datos "
                                 "de ginn con el formato esperado por las "
                                 "guías de importación de Murano.")
parser.add_argument("-a", "--productos", "--articulos",
                    help = "Exporta todos los productos de compra y venta.",
                    default = False, action = "store_true")
parser.add_argument("-c", "--clientes",
                    help = "Exporta todos los clientes con actividad en los"
                           " últimos 2 años.",
                    default = False, action = "store_true")
parser.add_argument("-p", "--proveedores",
                    help = "Exporta todos los proveedores con actividad en los"
                           " últimos 2 años.",
                    default = False, action = "store_true")
parser.add_argument("-t", "--todo",
                    help = "Exporta clientes, productos y proveedores.",
                    default = False, action = "store_true")

def do_imports():
    """
    Desde el framework se hacen algunas cosas sucias con los argumentos,
    así que tengo que hacer una importación limpia a posteriori.
    """
    sys.argv = []
    ruta_ginn = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "ginn"))
    sys.path.append(ruta_ginn)
    from framework import pclases

def main():
    if len(sys.argv) == 1:
        parser.print_help()
    args = parser.parse_args()
    do_imports()
    from api import murano
    if args.productos or args.todo:
        murano.exportar_productos()
    if args.clientes or args.todo:
        murano.exportar_clientes()
    if args.proveedores or args.todo:
        murano.exportar_proveedores()

if __name__ == "__main__":
    main()
