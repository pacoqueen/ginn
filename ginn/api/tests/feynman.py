#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Richard Feynman

«Creo que puedo decir con seguridad que nadie entiende la mecánica cuántica.»

«Durante algún tiempo se pusieron de moda los restaurantes topless. Uno iba
allí a tomar el almuerzo, las chicas bailaban desnudas de cintura para arriba
y, al cabo de un rato, desnudas del todo. Resultó que uno de estos lugares
estaba solo a un par de kilómetros de mi casa, por lo que iba allí con mucha
frecuencia. Tomaba asiento en uno de los compartimentos y hacía un poco de
física en los mantelitos de papel de la mesa —algunos tenían un festón
ondulado—, o dibujaba a alguna de las bailarinas, o a algún cliente; lo hacía
por practicar. A Gweneth, mi mujer, que es inglesa, no le molestaba que yo
fuera a ese lugar; decía: "Los ingleses van a clubs".»

---

** WIP **

La siguiente versión de ramanujan. Debe ser más rápida. Debe centrarse
en obtener el resumen. Debe montar el resultado en tiempo real en Drive.
Debe poderse invocar para un solo producto, para varios, para una
familia, para varias o para todo. Debe poder recibir también la fecha de
inicio y de fin y buscar automáticamente la hoja de cálculo de donde
sacar los datos.
"""


from __future__ import print_function
import sys
import argparse
import unittest
import datetime


# pylint:disable=too-many-arguments
def check_existencias(iniciales, produccion, consumos, ventas, ajustes,
                      produccion_mes_pasado, consumos_mes_pasado,
                      produccion_en_curso, consumos_en_curso,
                      existencias_murano):
    """
    Comprueba que las existencias de Murano coinciden con las calculadas que
    debería haber en realidad. Devuelve la diferencia de la teoría respecto
    a Murano.
    Producciones y ajustes deben venir en positivo.
    Ventas y consumos, en negativo.
    """
    teoria = iniciales + produccion + consumos + ventas + ajustes
    teoria += produccion_mes_pasado + consumos_mes_pasado
    teoria += -produccion_en_curso - consumos_en_curso
    res = existencias_murano - teoria
    return res


def analyze(producto, desde, hasta, debug=False):
    """
    Recibe un código de producto PVnnn.
    Busca las existencias que había en Murano en la fecha "desde" del producto.
    Busca las existencias que hay en la fecha "hasta".
    Realiza los cálculos entre las dos fechas para:
    1. Producción
    2. Ventas
    3. Consumos
    4. Ajustes
    5. Pendiente de consumir en la fecha inicial.
    6. Producción pendiente de validar en la fecha inicial.
    7. Pendiente de consumir en la fecha final.
    8. Producción pendiente de volcar en la fecha final.
    9. Suma de todos los elementos anteriores.
    Con la suma y las existencias de Murano hace una comparación y devuelve
    la diferencia de Murano **sobre** las existencias calculadas. None si no
    se realizó ningún cálculo.
    Cada uno de los valores se vuelca en una hoja de cálculo en la nube.
    """
    if debug:
        iniciales = 1
        produccion = 1  # 1+1=2
        consumos = -1   # 2-1=1
        ventas = -1     # 1-1=0
        ajustes = 1     # 0+1=1
        produccion_mes_pasado = 1   # 1+1=2
        consumos_mes_pasado = -1    # 2-1=1
        produccion_en_curso = 1     # 1-(+1)=0 En Murano todavía no existe
        consumos_en_curso = -1      # 0-(-1)=1 El consumo es solo en ginn.
        existencias_murano = 1
    else:
        # TODO
        iniciales = produccion = ventas = consumos = ajustes = None
        consumos_mes_pasado = produccion_mes_pasado = None
        consumos_en_curso = produccion_en_curso = None
        existencias_murano = None
    diferencia = check_existencias(iniciales,
                                   produccion,
                                   consumos,
                                   ventas,
                                   ajustes,
                                   produccion_mes_pasado,
                                   consumos_mes_pasado,
                                   produccion_en_curso,
                                   consumos_en_curso,
                                   existencias_murano)
    return diferencia


def main():
    """
    Rutina principal.
    """
    parser = argparse.ArgumentParser(
        description='Comprueba coherencia de existencias.')
    parser.add_argument('-d', '--debug', dest="debug", action="store_true",
                        help="Modo desarrollador con depuración.",
                        default=False)
    parser.add_argument('-f', '--desde', dest="desde", default=None,
                        help="Fecha inicial")
    parser.add_argument('-t', '--hasta', dest="hasta", default=None,
                        help="Fecha final")
    parser.add_argument('-p', '--producto', dest="productos", default=None,
                        help="Productos a analizar", nargs="*")
    parser.add_argument('-u', '--unitests', dest="testing",
                        action="store_true", help="Realizar tests.",
                        default=False)
    args = parser.parse_args()
    if args.debug:
        print("DEBUG: {}\tFROM:{}\tTO:{}\nPRODUCTOS:{}\n".format(
            args.debug, args.desde, args.hasta, args.productos))
    res = {}
    if args.testing:
        unittest.main(argv=[sys.argv[0]])
    elif args.productos:
        for producto in args.productos:
            res[producto] = analyze(producto, args.desde, args.hasta,
                                    args.debug)
            if args.debug:
                print("{}: {}".format(producto, res[producto]))


# Test unitarios
class TestAnalyze(unittest.TestCase):
    """
    Test unitario sobre `analyze`. Comprueba que dado un producto, una
    fecha inicial y una fecha final, devuelve un número correcto.
    """
    def test_analyze(self):
        """
        Comprueba que lo devuelto por `analyze` es un número.
        """
        producto = "PV70"
        ini = datetime.datetime(2019, 5, 1, 6, 0, 0)
        fin = datetime.datetime(2019, 6, 1, 6, 0, 0)
        res = analyze(producto, ini, fin, debug=True)
        self.assertTrue(isinstance(res, (float, int)),
                        "Debe devolver un número (flotante o entero).")

    def test_check_existencias(self):
        """
        Comprueba que el cálculo de la diferencia de las existencias teóricas
        respecto a Murano es correcto.
        """
        res = check_existencias(1, 1, -1, -1, 1, -1, 1, -1, 1, 1)
        self.assertEqual(res, 0, "Debería dar cero.")


if __name__ == "__main__":
    main()
