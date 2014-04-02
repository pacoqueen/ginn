#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
19/02/2014

Inspector Clouseau
==================

Extrae los datos de existencias iniciales y finales (fibra, geotextiles
y fibra de cemento), producción, consumos de la línea de geotextiles y
ventas de trece ficheros CSV que se le pasan por parámetro. Construye un
nuevo CVS que saca por salida estándar con las cifras combinadas por nombre
de producto y una columna con el delta de:
e_ini + producción - (ventas + abonos) - consumos de fibra = e_fin
                                                        | diff(e_fin, e_ini)

NOTAS:
* Los ficheros se sacan de:
    - consulta_existencias_por_tipo (existencias iniciales y finales): 6
    - consulta_ventas_por_producto (ventas y abonos): 3 ficheros
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
* Peculiaridades: el consumo se mide en peso sin embalaje, mientras que las 
  existencias van con embalaje y la producción también sin. En las balas, 
  cajas y bigbags no afecta porque el embalaje es despreciable o no se puede 
  estimar. En los rollos sí importa. Suerte que hasta ahora estamos tratando 
  totales, que en el caso de rollos van en metros. Y los metros no engañan.

SYNOPSIS

    clouseau.py [-h,--help] [-v,--verbose] [--version] \
        iniciales_fibra.csv iniciales_gtx.csv iniciales_cem.csv \
        produccion_fibra.csv produccion_gtx.csv produccion_cem.csv \
        salidas_fibra.csv salidas_gtx.csv salidas_cem.csv \
        consumos.csv finales_fibra.cem finales_gtx.cem finales_cem.csv

EJEMPLO
./clouseau.py ../../tests/20140301_0000_existencias_iniciales_fib.csv \
              ../../tests/20140301_0000_existencias_iniciales_gtx.csv \
              ../../tests/20140301_0000_existencias_iniciales_cem.csv \
              ../../tests/20140401_0000_producido_fib.csv \
              ../../tests/20140401_0000_producido_gtx.csv \
              ../../tests/20140401_0000_producido_cem.csv \
              ../../tests/20140401_0000_salidas_fib.csv \
              ../../tests/20140401_0000_salidas_gtx.csv \
              ../../tests/20140401_0000_salidas_cem.csv \
              ../../tests/20140401_0000_consumido.csv \
              ../../tests/20140401_0000_existencias_finales_fib.csv \
              ../../tests/20140401_0000_existencias_finales_gtx.csv \
              ../../tests/20140401_0000_existencias_finales_cem.csv \
              > diff.csv && libreoffice diff.csv

VERSION

    $Id$
"""

import sys
import os
import traceback
import optparse
import time
#from pexpect import run, spawn


#import mx.DateTime
# Determino dónde estoy para importar pclases y utils
DIRACTUAL = os.path.split(os.path.abspath(os.path.curdir))[-1]
try:
    FULLDIRPADRE = os.path.split(os.path.abspath(os.path.curdir))[0]
    DIRPADRE = os.path.split(FULLDIRPADRE)[-1]
except IndexError:
    sys.exit(2) # Where The Fuck am I?
assert DIRACTUAL == "scripts" or DIRPADRE == "tests", \
                    "Debe ejecutar el script desde el directorio donde reside"\
                    " o bien desde un subdirectorio de `tests`."
sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "ginn")))
from framework import pclases
from formularios import utils
from collections import defaultdict
from csv import writer, reader


def parse_existencias(fexistencias_ini, res=None):
    """
    Abre el CSV de existencias y devuelve un diccionario de productos con
    sus existencias.
    """
    if not res:
        res = defaultdict(lambda: 0.0)
    f_in = open(fexistencias_ini)
    data_in = reader(f_in, delimiter=";", lineterminator="\n")
    cabecera = True     # La primera fila son los títulos de columnas
    for linea in data_in:
        if cabecera:
            cabecera = False
            continue
        try:
            (producto, kg_a, m_a, b_a, kg_b, m_b, b_b, kg_c, m_c, b_c,
                kg_total, m_total, b_total) = linea
            total = utils.parse_float(m_total)
            if total == 0.0:    # Puede que sea un producto C. No lo puedo
                # saber únicamente por los datos de la hoja de cálculo. Uso
                # como total los kg. En el caso de los geotextiles normales
                # será también cero. No pasa nada. Solo habré perdido tiempo
                # parseando el valor. Pero si se mide en kg como los C,
                # entonces es el valor que me interesa.
                total = utils.parse_float(kg_total)
        except ValueError:  # Es el listado de fibra. No lleva metros.
            (producto, kg_a, b_a, kg_b, b_b, kg_c, b_c,
                kg_total, b_total) = linea
            total = utils.parse_float(kg_total)
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
        data_in = reader(f_in, delimiter=";", lineterminator="\n")
        cabecera = True     # La primera fila son los títulos de columnas
        for linea in data_in:
            if cabecera:
                cabecera = False
                continue
            try:
                (producto,
                 m_a, m_b, m_c, m_total,
                 kg_a, kg_teorico_a, kg_b, kg_teorico_b, kg_c, kg_total,
                 b_a, b_b, b_c, b_total,
                 t_teorico, t_real) = linea
                es_gtx = True
            except ValueError:  # Hay valores de menos. No es geotextiles.
                (producto,
                 kg_a, kg_b, kg_c, kg_total,
                 b_a, b_b, b_c, b_total,
                 t_teorico, t_real) = linea
                es_gtx = False
            if producto.startswith(">"):
                continue    # Es un desglose. No me interesa.
            if producto == "Sin producción".encode("latin1"):
                continue    # Es un resumen de tiempo sin producir. 
            if es_gtx:
                try:
                    producido = utils.parse_float(m_total)
                    # Caso especial para producto C. Se mide en Kg. En m_total
                    # tendrá un cero. Otros productos normales también pueden
                    # tener un cero en producción de metros, pero también lo
                    # tendrán en la columna de kg producidos. So...
                    if not producido:
                        producido = utils.parse_float(kg_total)
                except ValueError:  # Es una línea de resumen.
                    continue
            else:
                producido = utils.parse_float(kg_total)
            res[producto] += producido
        f_in.close()
    return res


def parse_salidas(fsalidas_fib, fsalidas_gtx, fsalidas_cem):
    """
    Abre cada fichero y parsea las salidas de almacén devolviendo un 
    diccionario de productos y las salidas de cada uno EN SUS UNIDADES: kg 
    para fibra y metros cuadrados para geotextiles.
    """
    # TODO: Ya de paso hacer todo con A, B y C en la hoja que genero.
    res = defaultdict(lambda: 0.0)
    for fname in fsalidas_fib, fsalidas_gtx, fsalidas_cem:
        f_in = open(fname)
        data_in = reader(f_in, delimiter=";", lineterminator="\n")
        cabecera = True     # La primera fila son los títulos de columnas
        for linea in data_in:
            if cabecera:
                cabecera = False
                continue
            try:
                (producto,
                 m_a, kg_a, b_a, 
                 m_b, kg_b, b_c, 
                 m_c, kg_c, b_c, 
                 m_total, kg_total, b_total) = linea
                es_gtx = True
            except ValueError:  # Hay valores de menos. No es geotextiles.
                (producto,
                 kg_a, b_a, 
                 kg_b, b_b, 
                 kg_c, b_c, 
                 kg_total, b_total) = linea
                es_gtx = False
            if es_gtx:
                salidas = utils.parse_float(m_total)
                # Caso especial para producto C. Se mide en Kg. En m_total
                # tendrá un cero. Otros productos normales también pueden
                # tener un cero en producción de metros, pero también lo
                # tendrán en la columna de kg producidos. So...
                if not salidas:
                    salidas = utils.parse_float(kg_total)
            else:
                salidas = utils.parse_float(kg_total)
            res[producto] += salidas
        f_in.close()
    return res


def parse_consumos(fconsumos):
    """
    Abre el fichero y parsea los consumos devolviendo un diccionario de
    productos y la cantidad de cada uno que ha salido del almacén para 
    consumirse en la línea.
    """
    res = defaultdict(lambda: 0.0)
    f_in = open(fconsumos)
    data_in = reader(f_in, delimiter=";", lineterminator="\n")
    cabecera = True     # La primera fila son los títulos de columnas
    for linea in data_in:
        if cabecera:
            cabecera = False
            continue
        producto, cantidad, a, b, c = linea[:5]
        salidas = utils.parse_float(cantidad)
        res[producto] += salidas
    f_in.close()
    return res


def calculate_deltas(e_ini, prod, salidas, cons, e_fin):
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
    for producto in prod:
        res[producto]['producción'] += prod[producto]
    for producto in salidas:
        res[producto]['salidas'] += salidas[producto]
    for producto in cons:
        res[producto]['consumos'] += cons[producto]
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
    out = writer(sys.stdout, delimiter=";", lineterminator="\n")
    out.writerow(("Producto", "Existencias iniciales", 
                  "Producción".encode("latin1"),
                  "Salidas", "Consumos", "Total", "Existencias finales",
                  "diff(final, total)"))
    productos = deltas.keys()
    productos.sort()
    for prod in productos:
        descripcion_producto = prod
        # Aquí voy a filtrar y me quito los que no son productos de venta
        es_producto_de_venta = False
        try:
            try:
                objeto = pclases.ProductoVenta.selectBy(descripcion=prod)[0]
            except:  # DataError:
                prod = prod.decode("latin1").encode("utf-8")
                objeto = pclases.ProductoVenta.selectBy(descripcion=prod)[0]
            if objeto:
                es_producto_de_venta = True
        except IndexError:
            # Casos especiales. Problemas de codificación:
            if ((prod.startswith("Geow") and "PINEMA" in prod)
                    or ("bolsas" in prod 
                        and "caja" in prod 
                        and "pal" in prod)):
                es_producto_de_venta = True
            # Cambios de nombre en el producto:
            # Si no es un producto de compra ahora, es que (almost) fue un pv:
            try:
                objeto = pclases.ProductoCompra.selectBy(descripcion=prod)[0]
                es_producto_de_venta = False
            except IndexError:
                # A no ser que haya más problemas de codificación
                if ("Filtro bomba" in prod
                        or (prod.startswith("PAL") 
                            and len(prod.split()) == 1)):
                    es_producto_de_venta = False
                else:
                    es_producto_de_venta = True
        if not es_producto_de_venta:
            continue    # No lo incluyo en el CSV de salida.
        inicial = utils.float2str(deltas[prod]['inicial'])
        produccion = utils.float2str(deltas[prod]['producción'])
        salidas = utils.float2str(deltas[prod]['salidas'])
        consumos = utils.float2str(deltas[prod]['consumos'])
        total = utils.float2str(deltas[prod]['total'])
        final = utils.float2str(deltas[prod]['final'])
        delta = utils.float2str(deltas[prod]['diff'])
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
         fsalidas_fib, fsalidas_gtx, fsalidas_cem, fconsumos,
         fexistencias_fin_fib, fexistencias_fin_gtx, fexistencias_fin_cem):
    """
    Abre y parsea uno por uno los ficheros de entrada. Construye una serie 
    de diccionarios con la información de existencias, salidas, consumos y 
    producción. A partir de esos diccionarios genera un fichero CSV que 
    muestra por salida estándar.
    """
    existencias_ini = parse_existencias(fexistencias_ini_fib)
    existencias_ini = parse_existencias(fexistencias_ini_gtx,
                                        existencias_ini)
    existencias_ini = parse_existencias(fexistencias_ini_cem,
                                        existencias_ini)
    produccion = parse_produccion(fproduccion_fib,
                                  fproduccion_gtx,
                                  fproduccion_cem)
    salidas = parse_salidas(fsalidas_fib, fsalidas_gtx, fsalidas_cem)
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
        parser = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'],
            version='$Id$')
        parser.add_option('-v',
                          '--verbose',
                          action='store_true',
                          default=False,
                          help='verbose output')
        (options, args) = parser.parse_args()
        if len(args) < 9:
            parser.error('Debe especificar once ficheros fuente')
        if options.verbose:
            print >> sys.stderr, time.asctime()
        main(*args)
        if options.verbose:
            print >> sys.stderr, time.asctime()
        if options.verbose:
            print >> sys.stderr, 'Tiempo total en minutos: ',
        if options.verbose:
            print >> sys.stderr, (time.time() - start_time) / 60.0
        sys.exit(0)
    except KeyboardInterrupt, exception:  # Ctrl-C
        raise exception
    except SystemExit, exception:  # sys.exit()
        raise exception
    except Exception, exception:
        print >> sys.stderr, 'Error, excepción inesperada.'
        print >> sys.stderr, str(exception)
        traceback.print_exc()
        sys.exit(1)
