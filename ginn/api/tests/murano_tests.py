#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys, os
# Desde el framework se hacen algunas cosas sucias con los argumentos,
# así que tengo que hacer una importación limpia a posteriori.
_argv, sys.argv = sys.argv, []
ruta_ginn = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "ginn"))
sys.path.append(ruta_ginn)
from framework import pclases
from api import murano
sys.argv = _argv

def prueba_bala(codigo = None):
    if not codigo:
        b = pclases.Bala.select(orderBy = "-id")[0]
    else:
        b = pclases.Bala.selectBy(codigo = codigo)[0]
    murano.create_bala(b)
    for c in b.articulo.parteDeProduccion.consumos:
        murano.consumir(c.productoCompra, c.cantidad, consumo = c)

def prueba_rollo(codigo = None):
    if not codigo:
        r = pclases.Rollo.select(orderBy = "-id")[0]
    else:
        r = pclases.Rollo.selectBy(codigo = codigo)[0]
    murano.create_rollo(r)
    for c in r.articulo.parteDeProduccion.consumos:
        murano.consumir(c.productoCompra, c.cantidad)
    # Para probar, consumiré la partida de carga completa:
    if r.articulo.parteDeProduccion.partidaCarga:
        for b in r.articulo.parteDeProduccion.partidaCarga.balas:
            # El almacén donde estaba la bala **antes** de consumirla está 
            # en Murano. En ginn el almacén es None. Confiamos en Murano para
            # buscar e indicar de qué almacén debe consumir la bala. Sería
            # muy complicado (y más lento) determinarlo en ginn antes de lanzar
            # el consumo a la pasarela.
            murano.delete_articulo(b.articulo)

def prueba_pale(codigo = None):
    if not codigo:
        p = pclases.Pale.select(orderBy = "-id")[0]
    else:
        p = pclases.Pale.selectBy(codigo = codigo)[0]
    murano.create_pale(p)
    for c in p.parteDeProduccion.consumos:
        murano.consumir(c.productoCompra, c.cantidad)
    # Consumo los bigbags de fibra empleados en rellenar las bolsas
    for bb in p.parteDeProduccion.bigbags:
        murano.delete_articulo(bb.articulo)

def prueba_bigbag(codigo = None):
    if not codigo:
        bb = pclases.Bigbag.select(orderBy = "-id")[0]
    else:
        bb = pclases.Bigbag.selectBy(codigo = codigo)[0]
    murano.create_bigbag(bb)
    for c in bb.articulo.parteDeProduccion.consumos:
        murano.consumir(c.productoCompra, c.cantidad, consumo = c)
    # Los partes de reembolsado se ignoran. Solo la fibra fabricada
    # directamente para almacenar en bigbags en lugar de en balas.


def main():
    ## Parámetros
    parser = argparse.ArgumentParser(
            description = "Pruebas de movimientos de stock en Murano.")
    parser.add_argument("-b", "--balas", dest = "balas",
            help = "Inserta las últimas 100 balas y sus consumos.",
            default = False, action = "store_true")
    parser.add_argument("-r", "--rollos", dest = "rollos",
            help = "Inserta los últimos 100 rollos y sus consumos.",
            default = False, action = "store_true")
    parser.add_argument("-c", "--cajas", dest ="cajas",
            help = "Inserta los últimos 10 palés y sus consumos.",
            default = False, action = "store_true")
    parser.add_argument("-g", "--bigbags", dest = "bigbags",
            help = "Inserta los últimos 100 bigbags y sus consumos.",
            default = False, action = "store_true")
    if len(sys.argv) == 1:
        parser.print_help()
    args = parser.parse_args()
    ## Pruebas
    if args.balas:
        balas = pclases.Bala.select(orderBy = "-id")[:100]
        for bala in balas:
            prueba_bala(bala.codigo)
    if args.rollos:
        rollos = pclases.Rollo.select(orderBy = "-id")[:100]
        for rollo in rollos:
            prueba_rollo(rollo.codigo)
    if args.cajas:
        pales = pclases.Pale.select(orderBy = "-id")[:10]
        for pale in pales:
            prueba_pale(pale.codigo)
    if args.bigbags:
        bigbags = pclases.Bigbag.select(orderBy = "-id")[:100]
        for bigbag in bigbags:
            prueba_bigbag(bigbag.codigo)

if __name__ == "__main__":
    main()
