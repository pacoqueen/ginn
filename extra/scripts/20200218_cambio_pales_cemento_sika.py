#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=invalid-name

"""
Cambio de palés de SIKA a GEOCEM
================================

jmhurtado pidió cambiar todo lo que había de SIKA en almacén (1.088 cajas) a
GEOCEM para encasquetárselo a otro cliente. No tuvo en cuenta, o no quiso
tenerlo en cuenta, que la fibra que pedía el cliente era de 6 mm y la de SIKA
es de 12. Después de más de 12 horas de trabajo y sacar todas las etiquetas
nuevas, resulta que el cliente no quiere la fibra (lógico) y hay que volver a
cambiar al producto original.
"""

from __future__ import print_function
from math import factorial
import sys
import os
import datetime
# Determino dónde estoy para importar pclases y utils
DIRACTUAL = os.path.split(os.path.abspath(os.path.curdir))[-1]
if DIRACTUAL != "ginn":
    PATH_TO_F = os.path.join("..", "..", "ginn")
    sys.path.append(PATH_TO_F)
# pylint: disable=wrong-import-position,import-error
from framework import pclases   # noqa
from api import murano          # noqa
from lib.tqdm import tqdm       # noqa

NUMCAJAS = 34*32  # Hay que mover 34 palés de 32 cajas/palé (y 12 bolsas/caja).


def cargar_articulos(codigos_pale):
    """
    Devuelve una lista de pclases.Articulo cajas a cambiar. Recibe los códigos
    de los palés que engloban esas cajas.
    """
    res = []
    for codigo_pale in tqdm.tqdm(codigos_pale, desc="Cargando palés"):
        pale = pclases.Articulo.get_articulo(codigo_pale)
        for caja in pale.cajas:
            res.append(caja.articulo)
    return res


def cambiar_cajas_de_producto_murano(cajas, pv, simulate=True):
    """
    Crea los movimientos de stock y de serie para cambiar de producto todas las
    cajas recibidas al pv indicado. Solo en Murano. No toca los artículos de
    ginn.
    `cajas` es una lista de artículos de ginn.
    """
    # Trataré de hacerlo todo en un solo lote de importación. Si no, prepárate
    # paras las 5 o 6 horas largas. guid_proceso se instanciará con la
    # primera caja y lo reutilizaré en las siguientes llamadas.
    guid_proceso = None
    for a in tqdm.tqdm(cajas, desc="Bajas"):
        assert pv == a.productoVenta, "El artículo debe tener el producto "\
                                      "correcto en ginn."
        guid_proceso = murano.ops.delete_articulo(
            a,
            observaciones="Vuelta al prod. orig. +alorenzo +jmhurtado",
            guid_proceso=guid_proceso,
            procesar=False,
            simulate=simulate,
            serie="MAN")
    if not simulate:
        res = murano.ops.fire(guid_proceso)
    else:
        res = guid_proceso
    guid_proceso = None
    for a in tqdm.tqdm(cajas, desc="Altas"):
        guid_proceso = murano.ops.create_articulo(
            a,
            observaciones="Vuelta al prod. orig. +alorenzo +jmhurtado",
            guid_proceso=guid_proceso,
            procesar=False,
            simulate=simulate,
            serie="MAN")
    if not simulate:
        res = murano.ops.fire(guid_proceso) and res
    else:
        res += guid_proceso
    return res


# pylint: disable=too-many-locals, too-many-statements
def main():
    """
    Rutina principal.
    """
    codigos_pale = """H13363/12
    H13364/12
    H13365/12
    H13366/12
    H13367/12
    H13368/12
    H13369/12
    H13370/12
    H13371/12
    H13372/12
    H13373/12
    H13374/12
    H13375/12
    H13376/12
    H13377/12
    H13378/12
    H13379/12
    H13380/12
    H13381/12
    H13382/12
    H13383/12
    H13384/12
    H13385/12
    H13386/12
    H13387/12
    H13388/12
    H13389/12
    H13396/12
    H13397/12
    H13398/12
    H13399/12
    H13812/12
    H13813/12
    H13814/12""".split()
    cajas = cargar_articulos(codigos_pale)
    assert len(cajas) == NUMCAJAS, "Número de cajas cargadas incorrecta."
    pvdest = pclases.ProductoVenta.get(597)
    res = cambiar_cajas_de_producto_murano(cajas, pvdest, simulate=False)
    if res:
        print("OK")
    else:
        print("KO")


if __name__ == "__main__":
    main()
