#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=invalid-name

"""
Reciclar rollos en fibra para consumir
======================================

Consume una lista de rollos B o C que se usaron para crear bigbag de fibra
reciclada que se consume en la línea de geotextiles.
"""

from __future__ import print_function
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


def cargar_rollos_a_reciclar():
    """Devuelve la lista de códigos de rollos para dar de baja en Murano."""
    codigos = """Y7526
Y7531
Y7529
Y7518
Y7477
Y7488
Y7515
Y7449
Y7534
Y7476
Y7503
Y7444
Y7451
Y7517
Y7452
Y7454
Y7450
Y7498
Y7542
Y7523
Y7541
Y7545
Y7513
Y7427
Y7563
Y7546
Y7583
Y7584
Y7571
Y7585
Y7575
Y7572
Y7574
Y7588
Y7573
Y7577
Y7587
Y7576"""
    cods = codigos.split()
    rollos = []
    for cod in tqdm.tqdm(cods, "Cargando rollos a reciclar..."):
        rollos.append(pclases.Articulo.get_articulo(cod))
    assert len(rollos) == len(cods)
    return rollos

def consumir_articulo(articulo, simulate=True, strict_mode=False, tag=None):
    """
    Da de baja el artículo en Murano como si se hubiera consumido. Pero sin
    trazabilidad con partidas de carga ni bigbag producidos en el proceso.
    Primero comprueba que esté en almacén. Si no está en almacén y el modo
    estricto está a True, devuelve False. Si strict_mode es False, devuelve
    False solo si el rollo no está en almacén pero no se ha consumido ya
    como fibra reciclada.
    """
    if tag is None:
        tag = " +abahamonde"    # Rollos anotados por abahamonde
    if murano.ops.esta_en_almacen(articulo):
        if not simulate:
            res = murano.ops.delete_articulo(articulo, observaciones="Consum. como reciclada {}{}".format(datetime.date.today().strftime("%b%y"), tag))
            if res:
                print("Artículo {} consumido.".format(articulo.codigo))
            else:
                print("[ERROR] Artículo {} no se pudo consumir.".format(articulo.codigo))
        else:
            res = True
            print("\t>>> [SIMULATE ON] consumo de artículo {}.".format(articulo.codigo))
    elif strict_mode:
        res = False
        print("[STRICT ON] El artículo {} no está en almacén.".format(articulo.codigo))
    else:
        if ya_consumido(articulo):
            res = True
            print("Artículo {} ya consumido anteriormente.".format(articulo.codigo))
        else:
            res = False
            print("El artículo {} no está en almacén.".format(articulo.codigo))
    return res

def ya_consumido(articulo):
    """
    Devuelve True si el artículo ya se consumió en meses anteriores como
    fibra reciclada.
    No mira la serie ni el tipo de movimiento. Solo los comentarios.
    """
    res = None
    lastop = murano.ops.get_ultimo_movimiento_articulo_serie(
                murano.connection.Connection(), articulo)
    if not lastop:
        res = False
    else:
        if lastop['Comentario'].startswith("Consum. como reciclada"):
            res = True
        elif lastop['Comentario'].startswith("Consumo desgarradora"):
            res = True
        else:
            res = False
    return res

def consumir_rollos(articulos, simulate=True):
    """
    Comprueba si el artículo existe en Murano y si está disponible en almacén.
    Si no lo está, comprueba que se ha dado de baja como consumo de fibra
    reciclada. Si no, imprime un mensaje de alerta.
    Si el rollo está en almacén lo da de baja con un comentario especial para
    facilitar la trazabilidad.
    """
    res = True
    for articulo in tqdm.tqdm(articulos, "Consumiendo artículos..."):
        res = consumir_articulo(articulo, simulate=simulate) and res
    print("{} artículos tratados.".format(len(articulos)))
    return res

def main():
    """
    Rutina principal.
    """
    rollos = cargar_rollos_a_reciclar()
    res = consumir_rollos(rollos, simulate=True)
    if res:
        print("OK")
    else:
        print("KO")


if __name__ == "__main__":
    main()
