#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
ruta_ginn = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "ginn"))
sys.path.append(ruta_ginn)
from framework import pclases
from api import murano


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

def main():
    balas = pclases.Bala.select(orderBy = "-id")[:100]
    for bala in balas:
        prueba_bala(bala.codigo)
    rollos = pclases.Rollo.select(orderBy = "-id")[:100]
    for rollo in rollos:
        prueba_rollo(rollo.codigo)

if __name__ == "__main__":
    main()
