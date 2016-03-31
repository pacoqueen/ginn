#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Capa de "adaptación" de ginn a Murano.

Se encarga de calcular según las nuevas definiciones los pesos brutos, netos,
teóricos (iedales) y superficie de un artículo de ginn, aunque este haya
sido producido antes del cambio efectivo en ginn.
"""

from __future__ import print_function
import os
import logging
NOMFLOG = ".".join(os.path.basename(__file__).split(".")[:-1])
logging.basicConfig(filename="%s.log" % (NOMFLOG),
                    format="%(asctime)s %(levelname)-8s : %(message)s",
                    level=logging.DEBUG)

# PESOS
#   Balas:
#     Clase A y B: Peso embalaje = 200 gr. En versiones anteriores se
#      descontaba 1 ó 1.5 kg directamente en báscula y peso neto = peso neto.
#     Case C: Sin embalaje. Peso introducido directamente por operarios.
#   Rollos:
#     Clase A: Para Murano, peso neto = peso teórico.
#     Clase B y C: peso neto = peso bruto - peso embalaje
#   Bigbags:
#     Clase A, B y C: peso neto = peso bruto. Embajale despreciable.
#   Cajas:
#     Clase A, B y C: peso neto = peso teórico.
#      peso bruto = peso neto + 0.1 kg
#   Palé:
#     Clase A, B y C: peso bruto = numcajas * (peso bruto caja + 0.15 kg)
#      Como un palé no es una instancia en sí misma en Murano, no hay forma de
#      agregarle el peso adicional al palé completo. Se lo metemos también a la
#      caja.
# SUPERFICIE
#   Balas, Cajas y Bigbag: No tienen
#   Rollos:
#     Clase A: ancho * largo según ficha del producto.
#     Clase B: ancho * largo introducido en el parte.
#     Clase C: No tiene


def get_peso_bruto(articulo):
    """
    Devuelve el peso bruto del artículo que espera recibir Murano.
    """
    peso = articulo.get_peso()
    peso_sin = articulo.get_peso_sin()
    if peso == peso_sin and articulo.es_bala():    # A ó B
        # Modelo antiguo. El peso neto es igual que el peso bruto porque
        # ya en báscula se le ha descontado 1 o 1.5 kg.
        res = peso + 1.0  # No hay forma de saber el peso real que ha dado
        # en báscula ya que se almacena directamente después de haberle
        # restado 1 (si no era peso entero) ó 1.5 kg (si el peso acababa en .0)
        # Para las balas a las que descontaron 1.5 le faltarían 500 gr.
        # res += 0.5
    else:  # Balas C, rollos, bigbag y cajas
        res = peso
    return res


def get_peso_neto(articulo):
    """
    Devuelve el peso neto del artículo que espera recibir Murano. Es el peso
    bruto menos el embalaje definido para el producto al que pertenece.
    Si no es aplicable, se devuelve None
    """
    if articulo.es_rollo() and articulo.es_clase_a():  # peso neto = teórico
        res = get_peso_ideal(articulo)
    else:   # Para el resto de rollos y demás artículos,
            # neto = bruto - embalaje (que puede ser despreciable)
        res = get_peso_bruto(articulo) - get_peso_embalaje(articulo)
    return res


def get_peso_ideal(articulo):
    """
    Devuelve el peso teórico que debería tener un artículo según el
    producto al que pertenece el artículo.
    Para un artículo sin peso ideal definido se considera 0.0.
    """
    res = articulo.get_peso_teorico()
    if res is None:
        res = 0.0
    return res


def get_peso_embalaje(articulo):
    """
    Devuelve el peso del embalaje definido para el artículo. No se obtiene
    de manera directa, es estimado para cada producto. Si es despreciable,
    se devuelve 0.
    """
    res = 0.0
    if articulo.es_bala():     # Balas A ó B. 200 gr (CWT)
        res = 0.2
    elif articulo.es_bala_cable():
        res = 0.0       # Balas C. Despreciable (CWT).
    elif (articulo.es_rollo() or articulo.es_rollo_defectuoso() or
          articulo.es_rollo_c()):  # Rollos ABC, el definido en el producto.
        res = articulo.productoVenta.camposEspecificosRollo.pesoEmbalaje
    elif articulo.es_bigbag():  # Bigbag A, B y C
        res = 0.0
    elif articulo.es_caja():   # Cajas A, B y C
        res = 0.1 + 0.15    # 100 gr de la caja de cartón y bolsas y 150
        # proporcionales del palé
    return res


def get_superficie(articulo):
    """
    Devuelve la superficie del artículo: alto * largo.
    Si no es aplicable, se devuelve None.
    **No lanza un TypeError/ValueError si el producto no tiene superficie
    (balas, cajas...).** Simplemente devuelve None.
    """
    res = None
    if articulo.es_rollo() or articulo.es_rollo_defectuoso():
        res = articulo.get_superficie()
    return res
