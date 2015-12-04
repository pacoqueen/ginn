#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
ruta_ginn = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "ginn"))
sys.path.append(ruta_ginn)
from framework import pclases
from api import murano


def prueba_bala():
    b = pclases.Bala.select(orderBy = "-id")[0]
    murano.create_bala(b)
    for c in b.articulo.parteDeProduccion.consumos:
        murano.consumir(c.productoCompra, c.cantidad, consumo = c)

def prueba_rollo():
    r = pclases.Rollo.select(orderBy = "-id")[0]
    murano.create_rollo(r)
    for c in r.articulo.parteDeProduccion.consumos:
        murano.consumir(c.productoCompra, c.cantidad)
    # Para probar, consumiré la partida de carga completa:
    if r.articulo.parteDeProduccion.partidaCarga:
        for b in r.articulo.parteDeProduccion.partidaCarga.balas:
            # TODO: FIXME: Habría que indicar de qué almacén se cogió la bala para consumirla. En el momento de inyectarlo en Murano b.articulo.almacen es None y da error al localizar el almacén en Murano.
            murano.delete_articulo(b.articulo)

def main():
    prueba_bala()
    prueba_rollo()

if __name__ == "__main__":
    main()
