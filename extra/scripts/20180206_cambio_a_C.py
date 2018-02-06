#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=invalid-name

"""
06/02/2018

Cambio de rollos en existencias de Murano por partida a calidad C.
Del listado de partidas recibidas busca las series que están en almacén según
Murano y las pasa a calidad C tras pedir confirmación.


SYNOPSIS

    ./20180206_cambio_a_C.py [-h,--help] [-v,--verbose] [--version]

VERSION

    $Id$
"""

from __future__ import print_function
import sys
import os
import traceback
import optparse
import time
import csv
from collections import OrderedDict
# Determino dónde estoy para importar pclases y utils
DIRACTUAL = os.path.split(os.path.abspath(os.path.curdir))[-1]
if DIRACTUAL != "ginn":
    PATH_TO_F = os.path.join("..", "..", "ginn")
    sys.path.append(PATH_TO_F)
# pylint: disable=wrong-import-position
from framework import pclases
from api import murano

def parse_input(filename):
    """
    Abre el fichero CSV y devuelve un diccionario de códigos de producto que
    contienen las partidas y a su vez estas guardan el número entero de
    artículos a pasar a C (debe coincidir con las existencias de Murano en ese
    momento para ese producto y partida), kg brutos, netos y metros cuadrados.
    """
    res = OrderedDict()
    with open(filename, "r") as finput:
        reader = csv.reader(finput)
        for row in reader:
            codigo = row[2]
            descripcion = row[3]
            partida = row[4]
            try:
                unidades = int(row[6])
            except ValueError:  # Es fila cabecera. Pasando
                continue
            neto = float(row[7].replace(".", "").replace(",", "."))
            bruto = float(row[8].replace(".", "").replace(",", "."))
            m2 = float(row[9].replace(".", "").replace(",", "."))
            struct_partida = {'código': partida,
                              'unidades': unidades,
                              'neto': neto,
                              'bruto': bruto,
                              'm2': m2}
            try:
                res[(codigo, descripcion)].append(struct_partida)
            except KeyError:
                res[(codigo, descripcion)] = [struct_partida]
    return res

def buscar_en_almacen(codigo_partida):
    """
    Devuelve una lista con las series en Murano de la partida recibida y con
    existencias en almacén.
    """
    res = []
    print(" » Buscando existencias para {}...".format(codigo_partida))
    conn = murano.connection.Connection()
    sql = """SELECT NumeroSerieLc
             FROM {}.dbo.ArticulosSeries
             WHERE UnidadesSerie > 0 AND CodigoTalla01_ = 'A'
             AND Partida = '{}';""".format(conn.get_database(),
                                           codigo_partida,
                                           murano.connection.CODEMPRESA)
    res = [fila['NumeroSerieLc'] for fila in conn.run_sql(sql)]
    return res

def main(filename):
    """
    1. Lee las partidas de un fichero.
    2. Busca las series de esa partida con existencias en Murano.
    3. Confirma el número de series a pasar a calidad C.
    4. Para cada serie, a través de la API, da de baja el artículo en A y lo
       da de alta como C.
    """
    productos = parse_input(filename)
    # pylint: disable=too-many-nested-blocks
    for producto in productos:
        codigo_producto, descripcion = producto
        print("## {}: {}".format(codigo_producto, descripcion))
        for partida in productos[producto]:
            print("### Partida {}: {} series ({} kg netos, {} kg brutos, {} m²".format(
                partida['código'], partida['unidades'], partida['neto'],
                partida['bruto'], partida['m2']))
            codigos_rollo = buscar_en_almacen(partida['código'])
            if len(codigos_rollo) == partida['unidades']:
                for codigo in codigos_rollo:
                    articulo = pclases.Articulo.get_articulo(codigo)
                    try:
                        if murano.ops.update_calidad(articulo, 'C', force=True):
                            print("Código {} pasado a calidad C.".format(articulo.codigo))
                        else:
                            print("[!] Código {} no se pudo pasar a C.".format(articulo.codigo))
                    except NotImplementedError:
                        print("Ignorando {}.".format(articulo.codigo))
            else:
                msgerror = "[!] {}: {} - Partida {}\n".format(
                    codigo_producto, descripcion, partida['código'])
                msgerror += "\tEn listado: {} ud, {} kg neto, {} kg bruto, {} m².\n".format(
                    partida['unidades'], partida['neto'], partida['neto'], partida['m2'])
                msgerror += "\tEn Murano: {} ud".format(len(codigos_rollo))
                print(msgerror)

if __name__ == '__main__':
    try:
        start_time = time.time()
        fileinput = '20180206_gtx_a_C.csv'
        parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(),
                                       usage=globals()['__doc__'],
                                       version='$Id$')
        parser.add_option('-v',
                          '--verbose',
                          action='store_true',
                          default=False,
                          help='información por pantalla')
        parser.add_option('-i', dest='fileinput', default='20180206_gtx_a_C.csv',
                          help='fichero de entrada')
        (options, args) = parser.parse_args()
        #if len(args) < 1:
        #    parser.error ('missing argument')
        if options.verbose:
            print(time.asctime())
        main(fileinput)
        if options.verbose:
            print(time.asctime())
        if options.verbose:
            print('Tiempo total en minutos: ', (time.time() - start_time) / 60.0)
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:    # pylint: disable=broad-except
        print('Error, excepción inesperada.')
        print(str(e))
        traceback.print_exc()
        sys.exit(1)
