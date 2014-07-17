#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Cambio de varios rollos de producto a petición de Jesús Madrid con el visto
bueno de Nicolás y Kiko. Correo del 30 de junio de 2014.
"""

import sys
import os

#import mx.DateTime
# Determino dónde estoy para importar pclases y utils
DIRACTUAL = os.path.split(os.path.abspath(os.path.curdir))[-1]
try:
    FULLDIRPADRE = os.path.split(os.path.abspath(os.path.curdir))[0]
    DIRPADRE = os.path.split(FULLDIRPADRE)[-1]
except IndexError:
    sys.exit(2)  # Where The Fuck am I?
assert DIRACTUAL == "scripts" or DIRPADRE == "tests", \
                    "Debe ejecutar el script desde el directorio donde reside"\
                    " o bien desde un subdirectorio de `tests`."
sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "ginn")))
from framework import pclases
#from framework import tests_coherencia
from formularios import utils
from lib.textprogressbar.progress.bar import IncrementalBar


def _load_rollos():
    """
    Devuelve un diccionario con los productos a los que hay que pasar cada
    rollo que está en la lista de cada clave.
    """
    nt15 = (350516, 350518, 350523, 350524, 350527)                         # 5
    nt23 = (341302, 341303, 341304, 341305, 341306, 341307, 349848, 349849,
            349850, 349851, 349854, 349855, 349859, 349862, 349866, 349867) #16
    nt30 = (349894, 349898, 349904, 349905, 349906, 349909)                 # 6
    pvnt15 = pclases.ProductoVenta.select(pclases.AND(
                pclases.ProductoVenta.q.descripcion.contains("NT 15 "),
                pclases.NOT(
                    pclases.ProductoVenta.q.descripcion.contains("NT 155")),
                pclases.ProductoVenta.q.camposEspecificosRolloID ==
                    pclases.CamposEspecificosRollo.q.id,
                pclases.CamposEspecificosRollo.q.metrosLineales == 100,
                pclases.CamposEspecificosRollo.q.ancho == 5.5),
            orderBy="id")[0]
    pvnt23 = pclases.ProductoVenta.select(pclases.AND(
                pclases.ProductoVenta.q.descripcion.contains("NT 23 "),
                pclases.NOT(
                    pclases.ProductoVenta.q.descripcion.contains("NT 235")),
                pclases.ProductoVenta.q.camposEspecificosRolloID ==
                    pclases.CamposEspecificosRollo.q.id,
                pclases.CamposEspecificosRollo.q.metrosLineales == 100,
                pclases.CamposEspecificosRollo.q.ancho == 5.5),
            orderBy="id")[0]
    pvnt30 = pclases.ProductoVenta.select(pclases.AND(
                pclases.ProductoVenta.q.descripcion.contains("NT 30"),
                pclases.NOT(
                    pclases.ProductoVenta.q.descripcion.contains("NT 305")),
                pclases.ProductoVenta.q.camposEspecificosRolloID ==
                    pclases.CamposEspecificosRollo.q.id,
                pclases.CamposEspecificosRollo.q.metrosLineales == 90,
                pclases.CamposEspecificosRollo.q.ancho == 5.5),
            orderBy="id")[0]
    res = {pvnt15: [],
           pvnt23: [],
           pvnt30: []}
    for codigo in nt15:
        rollo = pclases.Rollo.selectBy(numrollo=codigo)[0]
        assert "NT 155 5.5X100" in rollo.productoVenta.descripcion
        res[pvnt15].append(rollo)
    for codigo in nt23:
        rollo = pclases.Rollo.selectBy(numrollo=codigo)[0]
        assert "NT 235 5.5X100" in rollo.productoVenta.descripcion
        res[pvnt23].append(rollo)
    for codigo in nt30:
        rollo = pclases.Rollo.selectBy(numrollo=codigo)[0]
        assert "NT 305 5.5X90" in rollo.productoVenta.descripcion
        res[pvnt30].append(rollo)
    return res


def load_rollos():
    """
    Devuelve un diccionario con los productos a los que hay que pasar cada
    rollo que está en la lista de cada clave.
    Guarda en el diccionario de productividades los rendimientos de los partes
    antes de tocarlos más adelante.
    """
    nt12 = (354096, 354097, 354098, 354099, 354100,  # 5
            354101, 354102, 354103, 354104, 354105,  # 10
            354106, 354107)                          # 12
    pvnt12 = pclases.ProductoVenta.select(pclases.AND(
                pclases.ProductoVenta.q.descripcion.contains("NT 12 "),
                pclases.NOT(
                    pclases.ProductoVenta.q.descripcion.contains("NT 125")),
                pclases.ProductoVenta.q.camposEspecificosRolloID ==
                    pclases.CamposEspecificosRollo.q.id,
                pclases.CamposEspecificosRollo.q.metrosLineales == 100,
                pclases.CamposEspecificosRollo.q.ancho == 1.83),
            orderBy="id")[0]
    res = {pvnt12: []}
    for codigo in nt12:
        rollo = pclases.Rollo.selectBy(numrollo=codigo)[0]
        res[pvnt12].append(rollo)
    return res


def cambiar_producto(rollo, producto):
    """
    Cambia el producto del rollo a recibido.
    """
    # Me aseguro de que al menos tienen mismo largo y ancho
    assert (rollo.productoVenta.camposEspecificosRollo.metrosLineales ==
                                producto.camposEspecificosRollo.metrosLineales)
    assert (rollo.productoVenta.camposEspecificosRollo.ancho ==
                                producto.camposEspecificosRollo.ancho)
    rollo.productoVenta = producto
    rollo.sync()


def main():
    """
    Carga la lista de rollos y cambia el producto de venta de cada uno de ellos
    """
    rollos = load_rollos()
    total_rollos = sum([len(rollos[p]) for p in rollos])
    barra = IncrementalBar('Reasignando rollos', max=total_rollos)
    for producto in rollos:
        for rollo in rollos[producto]:
            cambiar_producto(rollo, producto)
            barra.next()
    barra.finish()


if __name__ == "__main__":
    main()
