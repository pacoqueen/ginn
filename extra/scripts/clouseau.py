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
  [03/04/2014]: OBSOLETO. Ya no existe esa opción en la ventana y se saca la 
                producción C siempre.
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

AUTO_OUT = False    # Determina si genera todas las combinaciones posibles de
                    # tipos y calidades y escribe cada resultado en un fichero
                    # diferente. De otro modo, y por defecto, escribe todo el
                    # csv por salida estándar.

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


class Options:
    def __init__(self,
                 filter_zeroes=True,
                 filter_prods=True,
                 calidades=("A", "B", "C", "total"),
                 tipos=("fib", "gtx", "cem")):
        self.filter_zeroes = filter_zeroes
        self.filter_prods = filter_prods
        self.qlty = calidades
        self.tipo = tipos

#OPTIONS = Options(calidades = ("A", ), tipos = ("fib", ))
#OPTIONS = Options(True, True, ("total", ), ("gtx", ))
OPTIONS = Options()

def parse_existencias(fexistencias_ini, res=None):
    """
    Abre el CSV de existencias y devuelve un diccionario de productos con
    sus existencias.
    """
    if not res:
        res = {}
        for qlty in ("A", "B", "C", "total"):
            res[qlty] = defaultdict(lambda: 0.0)
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
            stock_a = utils.parse_float(m_a)
            stock_b = utils.parse_float(m_b)
            try:
                stock_c = utils.parse_float(m_c)
            except ValueError:  # No lleva metros de C. Geotextiles C en kg.
                stock_c = m_c
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
            stock_a = utils.parse_float(kg_a)
            stock_b = utils.parse_float(kg_b)
            stock_c = utils.parse_float(kg_c)
            total = utils.parse_float(kg_total)
        res["A"][producto] += stock_a
        res["B"][producto] += stock_b
        try:
            res["C"][producto] += stock_c
        except TypeError:   # Viene un "No Aplicable"
            pass
        res["total"][producto] += total
    f_in.close()
    return res


def parse_produccion(fproduccion_fib, fproduccion_gtx, fproduccion_cem):
    """
    Abre el fichero y devuelve un diccionario de productos con la producción.
    """
    res = {}
    for qlty in ("A", "B", "C", "total"):
        res[qlty] = defaultdict(lambda: 0.0)
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
                    prod_a = utils.parse_float(m_a)
                    prod_b = utils.parse_float(m_b)
                    prod_c = utils.parse_float(m_c)
                    producido = utils.parse_float(m_total)
                    # Caso especial para producto C. Se mide en Kg. En m_total
                    # tendrá un cero. Otros productos normales también pueden
                    # tener un cero en producción de metros, pero también lo
                    # tendrán en la columna de kg producidos. So...
                    if not producido:
                        prod_a = utils.parse_float(kg_a)
                        prod_b = utils.parse_float(kg_b)
                        prod_c = utils.parse_float(kg_c)
                        producido = utils.parse_float(kg_total)
                except ValueError:  # Es una línea de resumen.
                    continue
            else:
                prod_a = utils.parse_float(kg_a)
                prod_b = utils.parse_float(kg_b)
                prod_c = utils.parse_float(kg_c)
                producido = utils.parse_float(kg_total)
            res["A"][producto] += prod_a
            res["B"][producto] += prod_b
            res["C"][producto] += prod_c
            res["total"][producto] += producido
        f_in.close()
    return res


def parse_salidas(fsalidas_fib, fsalidas_gtx, fsalidas_cem):
    """
    Abre cada fichero y parsea las salidas de almacén devolviendo un 
    diccionario de productos y las salidas de cada uno EN SUS UNIDADES: kg 
    para fibra y metros cuadrados para geotextiles.
    """
    res = {}
    for qlty in ("A", "B", "C", "total"):
        res[qlty] = defaultdict(lambda: 0.0)
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
                    sals_a = utils.parse_float(kg_a)
                    sals_b = utils.parse_float(kg_b)
                    sals_c = utils.parse_float(kg_c)
                    salidas = utils.parse_float(kg_total)
                else:
                    sals_a = utils.parse_float(m_a)
                    sals_b = utils.parse_float(m_b)
                    sals_c = utils.parse_float(m_c)
            else:
                sals_a = utils.parse_float(kg_a)
                sals_b = utils.parse_float(kg_b)
                sals_c = utils.parse_float(kg_c)
                salidas = utils.parse_float(kg_total)
            res["A"][producto] += sals_a
            res["B"][producto] += sals_b
            res["C"][producto] += sals_c
            res["total"][producto] += salidas
        f_in.close()
    return res


def parse_consumos(fconsumos):
    """
    Abre el fichero y parsea los consumos devolviendo un diccionario de
    productos y la cantidad de cada uno que ha salido del almacén para 
    consumirse en la línea.
    """
    res = {}
    for qlty in ("A", "B", "C", "total"):
        res[qlty] = defaultdict(lambda: 0.0)
    f_in = open(fconsumos)
    data_in = reader(f_in, delimiter=";", lineterminator="\n")
    cabecera = True     # La primera fila son los títulos de columnas
    for linea in data_in:
        if cabecera:
            cabecera = False
            continue
        producto, cantidad, cant_a, cant_b, cant_c = linea[:5]
        try:
            cons_a = utils.parse_float(cant_a)
            cons_b = utils.parse_float(cant_b)
            cons_c = utils.parse_float(cant_c)
        except ValueError:  # No aplicable. Son productos de compra.
            cons_a = cons_b = cons_c = 0.0
        consumos = utils.parse_float(cantidad)
        res["A"][producto] += cons_a
        res["B"][producto] += cons_b
        res["C"][producto] += cons_c
        res["total"][producto] += consumos
    f_in.close()
    return res


def calculate_deltas(e_ini, prod, sals, cons, e_fin):
    """
    Construye y devuelve un nuevo diccionario con todos los productos de
    los cuatro recibidos y los valores en las cuatro claves del diccionario
    que contiene cada producto. Añade una columna más el total de los tres
    primeros valores y otra con la diferencia entre las existencias finales y
    ese total.
    """
    def empty_producto():
        dic_producto = {}
        for qlty in ("A", "B", "C", "total"):
            dic_producto[qlty] = {'inicial': 0.0,
                                  'producción': 0.0,
                                  'traspasos': 0.0, 
                                  'salidas': 0.0,
                                  'consumos': 0.0,
                                  'total': 0.0,
                                  'final': 0.0,
                                  'diff': 0.0}
        return dic_producto
    res = defaultdict(empty_producto)
    for qlty in ("A", "B", "C", "total"):
        for producto in e_ini[qlty]:
            res[producto][qlty]['inicial'] += e_ini[qlty][producto]
        for producto in prod[qlty]:
            res[producto][qlty]['producción'] += prod[qlty][producto]
        for producto in sals[qlty]:
            res[producto][qlty]['salidas'] += sals[qlty][producto]
        for producto in cons[qlty]:
            res[producto][qlty]['consumos'] += cons[qlty][producto]
        for producto in e_fin[qlty]:
            res[producto][qlty]['final'] += e_fin[qlty][producto]
        # Cálculo de subdeltas por A, B, C y delta total:
        for producto in res:
            inicial = res[producto][qlty]['inicial']
            produccion = res[producto][qlty]['producción']
            salidas = res[producto][qlty]['salidas']
            consumos = res[producto][qlty]['consumos']
            total = inicial + produccion - salidas - consumos
            res[producto][qlty]['total'] += total
            delta = res[producto][qlty]['final'] - total
            res[producto][qlty]['diff'] += delta
    return res


def dump_deltas(deltas, fout = None):
    """
    Crea un CSV que saca por salida estándar.
    """
    # TODO: Filtrar por tipo de producto: OPTIONS.tipo
    if fout == None:
        csv_out = sys.stdout
    else:
        csv_out = open(fout, "w")
    out = writer(csv_out, delimiter=";", lineterminator="\n")
    cabecera = ["Producto"]
    for qlty in OPTIONS.qlty:
        cabecera += ["Existencias iniciales [%s]" % (qlty.upper()), 
                     "Producción [%s]".encode("latin1") % (qlty.upper()),
                     "Traspasos [%s]" % (qlty.upper()), 
                     "Salidas [%s]" % (qlty.upper()), 
                     "Consumos [%s]" % (qlty.upper()), 
                     "Total [%s]" % (qlty.upper()), 
                     "Existencias finales [%s]" % (qlty.upper()),
                     "diff(final, total) [%s]" % (qlty.upper())]
    out.writerow(cabecera)
    productos = deltas.keys()
    productos.sort()
    for prod in productos:
        fila = []
        descripcion_producto = prod
        # Aquí voy a filtrar y me quito los que no son productos de venta
        es_producto_de_venta = False
        tipo = guess_tipo(prod)
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
        if not es_producto_de_venta or tipo not in OPTIONS.tipo:
            continue    # No lo incluyo en el CSV de salida.
        fila += [descripcion_producto]
        for qlty in OPTIONS.qlty:
            inicial = utils.float2str(deltas[prod][qlty]['inicial'])
            produccion = utils.float2str(deltas[prod][qlty]['producción'])
            traspasos = utils.float2str(deltas[prod][qlty]['traspasos'])
            salidas = utils.float2str(deltas[prod][qlty]['salidas'])
            consumos = utils.float2str(deltas[prod][qlty]['consumos'])
            total = utils.float2str(deltas[prod][qlty]['total'])
            final = utils.float2str(deltas[prod][qlty]['final'])
            delta = utils.float2str(deltas[prod][qlty]['diff'])
            fila += [inicial,
                     produccion,
                     traspasos,
                     salidas,
                     consumos,
                     total,
                     final,
                     delta]
        if OPTIONS.filter_prods and prod_sin_movimientos(fila):
            continue
        if OPTIONS.filter_zeroes:
            fila = filter_zeros(fila)
        out.writerow(fila)
    if fout is not None:
        csv_out.close()


def guess_tipo(descripcion):
    """
    Partiendo de la descripción, trata de adivinar qué tipo de producto es:
    fibra(fib), geotextiles (gtx), cemento (cem) o ninguno de ellos (None).
    """
    tipo = None
    palabras = limpiar(descripcion)
    crits = []
    for palabra in palabras:
        crits.append(pclases.ProductoVenta.q.descripcion.contains(palabra))
    try:
        pv = pclases.ProductoVenta.select(pclases.AND(*crits))[0]
        if pv.es_bala() or pv.es_bala_cable() or pv.es_bigbag():
            tipo = "fib"
        elif pv.es_rollo() or pv.es_rollo_c(): 
            tipo = "gtx"
        elif pv.es_bolsa() or pv.es_caja(): 
            tipo = "cem"
        else:
            tipo = None
    except IndexError:
        pv = None
    return tipo


def limpiar(cad):
    """
    Dada una cadena, devuelve todas las subpalabras que no contengan 
    caracteres no ascii ni símbolos de puntuación. Por ejemplo:
    Leña de 2.15 -> [Le, a, de, 2, 15]
    """
    import string
    validos = string.ascii_letters + string.digits
    res = []
    subw = ""
    for letra in cad:
        if letra in validos:
            subw += letra
        else:
            if subw:
                res.append(subw)
            subw = ""
    if subw:
        res.append(subw)
    return res


def prod_sin_movimientos(fila):
    """
    Devuelve True si todos los valores de la fila (menos el nombre del
    producto) son 0 o nulos.
    """
    for valor in fila[1:]:
        if valor != "0,00":
            return False
    return True


def filter_zeros(fila):
    """
    Sustitule los ceros de la fila por la cadena vacía.
    """
    res = []
    for valor in fila:
        if valor == "0,00":
            res.append("")
        else:
            res.append(valor)
    return res


def main(fexistencias_ini_fib, fexistencias_ini_gtx, fexistencias_ini_cem,
         fproduccion_fib, fproduccion_gtx, fproduccion_cem,
         fsalidas_fib, fsalidas_gtx, fsalidas_cem, fconsumos,
         fexistencias_fin_fib, fexistencias_fin_gtx, fexistencias_fin_cem, 
         fout = None):
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
    check_traspasos(dic_deltas)
    if AUTO_OUT:
        for tipo in (("fib", ), ("gtx", ), ("cem", ), ("fib", "gtx", "cem")):
            for qlty in (("A", ), ("B", ), ("C", ), ("total", ), 
                         ("A", "B", "C", "total")):
                OPTIONS.tipo = tipo
                OPTIONS.qlty = qlty
                if len(tipo) == 3:
                    str_tipo = ""
                else:
                    str_tipo = "_" + "".join(tipo)
                if len(qlty) == 4:
                    str_qlty = ""
                else:
                    str_qlty = "_" + "".join(qlty)
                fout = "diff%s%s.csv" % (str_tipo, str_qlty)
                dump_deltas(dic_deltas, fout)
    else:
        dump_deltas(dic_deltas, fout)

def check_traspasos(dic_deltas):
    """
    Para los productos que tienen diferencias construye un diccionario donde 
    trata de descubrir si ha habido traspasos directos entre productos. Se 
    cumplirá cuando un producto tiene un delta = x y otro uno similar = -x. En 
    ese caso podemos asumir que se han cambiado de denominación algunos 
    artículos de ese producto durante el transcurso de existencias_ini a e_fin.
    """
    traspasos = {'A': {}, 'B': {}, 'C': {}, 'total': {}}
    # Primero recorro detectando diferencias.
    for p in dic_deltas:
        for qlty in ("A", "B", "C", "total"):
            diff = dic_deltas[p][qlty]['diff']
            if diff != 0:
                try:
                    traspasos[qlty][abs(round(diff, 2))].append(
                            {'desc_producto': p,
                             'diff': diff})
                except KeyError:
                    traspasos[qlty][abs(round(diff, 2))] = [
                            {'desc_producto': p,
                             'diff': diff}]
    # Ahora recorro la lista de difernecias que han casado.
    for qlty in ("A", "B", "C", "total"):
        for diferencia in traspasos[qlty]:
            if len(traspasos[qlty][diferencia]) > 1:
                # Si == un solo producto, diferencia no justificada.
                # TODO: ¿Se dará el caso en que haya TRES productos (o
                # cualquier otro número impar) con la misma diferencia? ¿Y si
                # son cuatro? ¿cómo puedo distinguir cuál ha ido a cada cual?
                # ¿Podría anotarlo en el propio CSV en plan
                # "NT 14 -> CR 14..." en alguna "celda"?
                for dic_diferencia in traspasos[qlty][diferencia]:
                    producto = dic_diferencia['desc_producto']
                    diff = dic_diferencia['diff']
                    dic_deltas[producto][qlty]['traspasos'] += diff
                    dic_deltas[producto][qlty]['diff'] -= diff

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
        if len(args) < 13:
            parser.error('Debe especificar trece ficheros fuente')
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
        # import ipdb; ipdb.set_trace()     # BREAKPOINT
        sys.exit(1)
