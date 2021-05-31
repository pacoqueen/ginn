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
    codigos = """Y7189
Y7089
Y7190
Y7193
Y7205
Y7209
Y7192
X2274
Y7225
X2283
Y7223
Y7257
Y7237
Y7227
Y7208
Y7256
Y7234
Y7211
Y7290
Y7287
Y7291
Y7277
Y7266
Y7267
Y7269
Y7302
Y7314
Y7309
Y7369
Y7371
Y7286
Y7311
Y7328
Y7312
Y7283
Y7378
Y7361
Y7383
Y7373
Y7372
Y7388
Y7389
Y7363
Y7391
Y7210
Y7390
Y7375
Y7300
Y7386
Y7408
Y7415
Y7387
Y7430
Y7395
Y7398
Y7429
Y7382
Y7481
Y7487
Y7489
Y7483
Y7485
Y7478
Y7482
Y7447
Y7491
Y7492
Y7494
Y7484
Y7352
Y7345
Y7358
Y7440
Y7524
Y7504
Y7412
Y7439
Y7531
Y7524
Y7525
Y7520
Y7519
Y7441"""
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
        tag = " +cgutierrez"    # Últimos rollos de cgutierrez: mayo 21
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
    res = None
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
