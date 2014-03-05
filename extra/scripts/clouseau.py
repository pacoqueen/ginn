#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
19/02/2014

Inspector Clouseau
==================

Extrae los datos de existencias iniciales y finales (fibra, geotextiles 
y fibra de cemento), producción, consumos de la línea de geotextiles y 
ventas de nueve ficheros CSV que se le pasan por parámetro. Construye un 
nuevo CVS que saca por salida estándar con las cifras combinadas por nombre 
de producto y una columna con el delta de:
e_ini + producción - (ventas + abonos) - consumos de fibra = e_fin 
                                                        | diff(e_fin, e_ini)

NOTAS:
* Los ficheros se sacan de:
    - consulta_existencias_por_tipo (existencias iniciales y finales): 6
    - consulta_ventas_por_producto (ventas y abonos): 1 fichero
    - consulta_producido (producción): 3 ficheros
    - consulta_consumo (para consumo de fibra en la línea de geotextiles): 1
* Los consumos de fibra de las partidas de carga solían llevar un albarán 
  interno que debía generar el usuario manualmente. Lógicamente, lleva siglos 
  sin hacerse. Al menos en enero '14 no hay ni un albarán interno de consumo 
  de fibra en línea de geotextiles. __Hay que tenerlo en cuenta porque si 
  se empezaran otra vez a generar, se contarían dos veces: en los consumos 
  de línea y en las salidas como albaranes internos.__ También hay que tener 
  en cuenta que los posibles descuadres de fibra se pueden deber precisamente 
  a las balas cargadas físicamente en la línea pero aún no descontadas en el 
  programa porque el operario no ha llevado las etiquetas de las balas 
  cargadas al usuario.
* Los bigbag que se consumen en la línea de embolsado no deberían incluirse en 
  la consulta de consumos porque también llevan su propio albarán interno de 
  consumo de materiales y materia prima. Por lo tanto se contarían dos veces 
  si se marcara la opción `Línea de embolsado` en la consulta
* En la consulta de producido hay que indicar que se quiere también sacar la 
  producción C (aunque no entren para el cálculo de horas, totales y eso) para 
  que cuadre con las existencias inciales, finales y ventas.
* Hay que tener en cuenta que dos productos que se llamen igual, aunque uno 
  esté desabilitado (caso ARIAROLL 180), se van a combinar en una sola 
  fila de la hoja de cálculo.

SYNOPSIS

    clouseau.py [-h,--help] [-v,--verbose] [--version] iniciales_fibra.csv \
        iniciales_gtx.csv iniciales_cem.csv produccion.csv salidas.csv \
        finales_fibra.cem finales_gtx.cem finales_cem.csv

EJEMPLO
./clouseau.py ../../tests/20140101_0600_existencias_iniciales_fib.csv ../../tests/20140101_0600_existencias_iniciales_gtx.csv ../../tests/20140101_0600_existencias_iniciales_cem.csv ../../tests/20140201_0600_producido_fib.csv ../../tests/20140201_0600_producido_gtx.csv ../../tests/20140201_0600_producido_cem.csv ../../tests/20140201_0600_salidas.csv ../../tests/20140201_0600_consumido.csv ../../tests/20140201_0600_existencias_finales_fib.csv ../../tests/20140201_0600_existencias_finales_gtx.csv ../../tests/20140201_0600_existencias_finales_cem.csv > diff.csv && libreoffice diff.csv

VERSION

    $Id$
"""

import sys, os, traceback, optparse
import time
import re
#from pexpect import run, spawn


import mx, mx.DateTime
# Determino dónde estoy para importar pclases y utils
diractual = os.path.split(os.path.abspath(os.path.curdir))[-1]
assert diractual == "scripts", \
        "Debe ejecutar el script desde el directorio donde reside."
sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "ginn")))
from framework import pclases
from formularios import utils
from collections import defaultdict
from csv import writer, reader

def parse_existencias(fexistencias_ini, res = None):
    """
    Abre el CSV de existencias y devuelve un diccionario de productos con 
    sus existencias.
    """
    if not res:
        res = defaultdict(lambda: 0.0)
    f_in = open(fexistencias_ini)
    data_in = reader(f_in, delimiter = ";", lineterminator = "\n")
    cabecera = True     # La primera fila son los títulos de columnas
    for linea in data_in:
        if cabecera:
            cabecera = False
            continue
        try:
            (producto, kgA, mA, bA, kgB, mB, bB, kgC, mC, bC, 
                    kgTotal, mTotal, bTotal) = linea
            total = utils.parse_float(mTotal)
            if total == 0.0:    # Puede que sea un producto C. No lo puedo 
                # saber únicamente por los datos de la hoja de cálculo. Uso 
                # como total los kg. En el caso de los geotextiles normales 
                # será también cero. No pasa nada. Solo habré perdido tiempo 
                # parseando el valor. Pero si se mide en kg como los C, 
                # entonces es el valor que me interesa.
                total = utils.parse_float(kgTotal)
        except ValueError: # Es el listado de fibra. No lleva metros.
            (producto, kgA, bA, kgB, bB, kgC, bC, 
                    kgTotal, bTotal) = linea
            total = utils.parse_float(kgTotal)
        res[producto] += total
    f_in.close()
    return res

def parse_produccion(fproduccion_fib, fproduccion_gtx, fproduccion_cem):
    """
    Abre el fichero y devuelve un diccionario de productos con la producción.
    """
    res = defaultdict(lambda: 0.0)
    for fproduccion in (fproduccion_fib, fproduccion_gtx, fproduccion_cem):
        f_in = open(fproduccion)
        data_in = reader(f_in, delimiter = ";", lineterminator = "\n")
        cabecera = True     # La primera fila son los títulos de columnas
        for linea in data_in:
            if cabecera:
                cabecera = False
                continue
            try:
                (producto, 
                 mA, mB, mC, mTotal, 
                 kgA, kgB, kgC, kgTotal, 
                 bA, bB, bC, bTotal, 
                 t_teorico, t_real) = linea
                es_gtx = True
            except ValueError:  # Hay valores de menos. No es geotextiles.
                (producto, 
                 kgA, kgB, kgC, kgTotal, 
                 bA, bB, bC, bTotal, 
                 t_teorico, t_real) = linea
                es_gtx = False
            if producto.startswith(">"):
                continue    # Es un desglose. No me interesa.
            if es_gtx:
                producido = utils.parse_float(mTotal)
                # Caso especial para producto C. Se mide en Kg. En mTotal tendrá 
                # un cero. Otros productos normales también pueden tener un cero 
                # en producción de metros, pero también lo tendrán en la columna 
                # de kg producidos. So... 
                if not producido: 
                    producido = utils.parse_float(kgTotal)
            else:
                producido = utils.parse_float(kgTotal)
            res[producto] += producido
        f_in.close()
    return res

def parse_salidas(fventas):
    """
    Abre el fichero y parsea las ventas devolviendo un diccionario de 
    productos y las salidas de cada uno.
    """
    # TODO: Adaptar al nuevo formato de la consulta con A, B y C.
    # TODO: Y ya de paso hacer todo con A, B y C en la hoja que genero.
    res = defaultdict(lambda: 0.0)
    f_in = open(fventas)
    data_in = reader(f_in, delimiter = ";", lineterminator = "\n")
    cabecera = True     # La primera fila son los títulos de columnas
    for linea in data_in:
        if cabecera:
            cabecera = False
            continue
        producto, cantidad, cliente, fecha, albaran = linea
        if producto.startswith(">"):
            continue    # Es un desglose. No me interesa.
        cantidad = cantidad.split("(")[0]
        salidas = utils.parse_float(cantidad)
        res[producto] += salidas
    f_in.close()
    return res

def parse_consumos(fconsumos):
    """
    Abre el fichero y parsea las ventas devolviendo un diccionario de 
    productos y las salidas de cada uno.
    """
    res = defaultdict(lambda: 0.0)
    f_in = open(fconsumos)
    data_in = reader(f_in, delimiter = ";", lineterminator = "\n")
    cabecera = True     # La primera fila son los títulos de columnas
    for linea in data_in:
        if cabecera:
            cabecera = False
            continue
        producto, cantidad, media = linea
        salidas = utils.parse_float(cantidad)
        res[producto] += salidas
    f_in.close()
    return res

def calculate_deltas(e_ini, p, s, c, e_fin):
    """
    Construye y devuelve un nuevo diccionario con todos los productos de 
    los cuatro recibidos y los valores en las cuatro claves del diccionario 
    que contiene cada producto. Añade una columna más el total de los tres 
    primeros valores y otra con la diferencia entre las existencias finales y 
    ese total.
    """
    res = defaultdict(lambda: {'inicial': 0.0, 
                               'producción': 0.0, 
                               'salidas': 0.0, 
                               'consumos': 0.0, 
                               'total': 0.0, 
                               'final': 0.0, 
                               'diff': 0.0})
    for producto in e_ini:
        res[producto]['inicial'] += e_ini[producto]
    for producto in p:
        res[producto]['producción'] += p[producto]
    for producto in s:
        res[producto]['salidas'] += s[producto]
    for producto in c:
        res[producto]['consumos'] += c[producto]
    for producto in e_fin:
        res[producto]['final'] += e_fin[producto]
    for producto in res:
        inicial = res[producto]['inicial']
        produccion = res[producto]['producción']
        salidas = res[producto]['salidas']
        consumos = res[producto]['consumos']
        total = inicial + produccion - salidas - consumos
        res[producto]['total'] += total
        delta = res[producto]['final'] - total
        res[producto]['diff'] += delta 
    return res

def dump_deltas(deltas):
    """
    Crea un CSV que saca por salida estándar.
    """
    out = writer(sys.stdout, delimiter = ";", lineterminator = "\n")
    out.writerow(("Producto", "Existencias iniciales", "Producción", 
                  "Salidas", "Consumos", "Total", "Existencias finales", 
                  "diff(final, total)"))
    productos = deltas.keys()
    productos.sort()
    for p in productos:
        descripcion_producto = p
        # Aquí voy a filtrar y me quito los que no son productos de venta
        es_producto_de_venta = False
        try:
            try:
                objeto = pclases.ProductoVenta.selectBy(descripcion = p)[0]
            except: # DataError:
                p = p.decode("latin1").encode("utf-8")
                objeto = pclases.ProductoVenta.selectBy(descripcion = p)[0]
            if objeto:
                es_producto_de_venta = True
        except IndexError:
            # Casos especiales. Problemas de codificación:
            if ((p.startswith("Geow") and "PINEMA" in p) 
                    or ("bolsas" in p and "caja" in p and "pal" in p)):
                es_producto_de_venta = True
            # Cambios de nombre en el producto:
            # Si no es un producto de compra ahora, es que (almost) fue un pv:
            try:
                objeto = pclases.ProductoCompra.selectBy(descripcion = p)[0]
                es_producto_de_venta = False
            except IndexError:
                # A no ser que haya más problemas de codificación
                if ("Filtro bomba" in p 
                    or (p.startswith("PAL") and len(p.split()) == 1)):
                    es_producto_de_venta = False
                else:
                    es_producto_de_venta = True
        if not es_producto_de_venta:
            continue    # No lo incluyo en el CSV de salida.
        inicial = utils.float2str(deltas[p]['inicial'])
        produccion = utils.float2str(deltas[p]['producción'])
        salidas = utils.float2str(deltas[p]['salidas'])
        consumos = utils.float2str(deltas[p]['consumos'])
        total = utils.float2str(deltas[p]['total'])
        final = utils.float2str(deltas[p]['final'])
        delta = utils.float2str(deltas[p]['diff'])
        out.writerow((descripcion_producto, 
                      inicial, 
                      produccion, 
                      salidas, 
                      consumos, 
                      total, 
                      final, 
                      delta))

def main(fexistencias_ini_fib, fexistencias_ini_gtx, fexistencias_ini_cem, 
         fproduccion_fib, fproduccion_gtx, fproduccion_cem, 
         fventas, fconsumos, 
         fexistencias_fin_fib, fexistencias_fin_gtx, fexistencias_fin_cem):
	existencias_ini = parse_existencias(fexistencias_ini_fib)
	existencias_ini = parse_existencias(fexistencias_ini_gtx, 
                                            existencias_ini)
	existencias_ini = parse_existencias(fexistencias_ini_cem, 
                                            existencias_ini)
	produccion = parse_produccion(fproduccion_fib, 
                                      fproduccion_gtx, 
                                      fproduccion_cem)
        salidas = parse_salidas(fventas)
        consumos = parse_consumos(fconsumos)
        existencias_fin = parse_existencias(fexistencias_fin_fib)
        existencias_fin = parse_existencias(fexistencias_fin_gtx, 
                                            existencias_fin)
        existencias_fin = parse_existencias(fexistencias_fin_cem, 
                                            existencias_fin)
        dic_deltas = calculate_deltas(existencias_ini, 
                                      produccion, 
                                      salidas, 
                                      consumos, 
                                      existencias_fin)
        dump_deltas(dic_deltas)

if __name__ == '__main__':
    try:
        start_time = time.time()
        parser=optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), 
                                     usage=globals()['__doc__'], 
                                     version='$Id$')
        parser.add_option ('-v', 
                           '--verbose', 
                           action='store_true', 
                           default=False, 
                           help='verbose output')
        (options, args) = parser.parse_args()
        if len(args) < 9:
            parser.error ('Debe especificar once ficheros fuente')
        if options.verbose: print >> sys.stderr, time.asctime()
        main(*args)
        if options.verbose: print >> sys.stderr, time.asctime()
        if options.verbose: print >> sys.stderr, 'Tiempo total en minutos: ', 
        if options.verbose: print >> sys.stderr, (time.time() - start_time) / 60.0
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print >> sys.stderr, 'Error, excepción inesperada.'
        print >> sys.stderr, str(e)
        traceback.print_exc()
        os._exit(1)

