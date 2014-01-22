#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
22/01/2014

Recorre los albaranes de salida detectando aquellos en los que la cantidad 
agregada como artículos difiere de la cantidad facturada.
Ignora albaranes internos y de ajuste de existencias.

SYNOPSIS

    detectar_albaranes_mal_facturados.py [-h,--help] [-v,--verbose] [--version]

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

def comprobar_cantidades_albaran(alb):
    """
    Lo primero que determina es que el albarán sea facturable y tenga factura. 
    Si lo es, lo ignora en caso de que sea un albarán de movimiento, de respuestos, 
    interno o vacío. En otro caso cuenta las cantidades agregadas al 
    albarán en forma de artículos con trazabilidad y las compara con las 
    que dice la factura que han salido. Si no coinciden devuelve False.
    En otro caso devuelve True.
    """
    res = True
    pvs = {}
    total_articulos = 0.0
    total_factura = 0.0
    if alb.facturable and alb.get_facturas() and (alb.get_str_tipo() 
            == pclases.AlbaranSalida.str_tipos[pclases.AlbaranSalida.NORMAL]):
        # Suma de cantidades según las líneas de venta facturadas.
        for ldv in alb.lineasDeVenta:
            pv = ldv.productoVenta
            if pv != None and (pv.es_bala() or pv.es_bala_cable() or pv.es_bigbag() or pv.es_rollo() or pv.es_rollo_c() or pv.es_caja()):
                if pv not in pvs:
                    pvs[pv] = [ldv.cantidad, 0.0]
                else:
                    pvs[pv][0] += ldv.cantidad
        # Suma de cantidades según artículos con trazabilidad agregados.
        for articulo in alb.articulos + [ldd.articulo 
                                         for ldd in alb.lineasDeDevolucion]:
            pv = articulo.productoVenta
            if pv.es_rollo():
                cantidad_articulo = articulo.superficie
            elif pv.es_bala() or pv.es_bala_cable() or pv.es_bigbag() or pv.es_caja() or pv.es_rollo_c():
                cantidad_articulo = articulo.peso
            else:
                print >> sys.stderr, "Artículo ID %d no es bala [cable], rollo [defectuoso] ni bigbag." % (articulo.id)
                continue
            if pv not in pvs:
                pvs[pv] = [0.0, cantidad_articulo]
            else:
                pvs[pv][1] += cantidad_articulo
        #for pv in pvs:
        #    if round(pvs[pv][0], 2) != round(pvs[pv][1], 2):
        #        print >> sys.stderr, "El albarán ID %d (%s) tiene como cantidad total de %s, %s en líneas de venta y %s en artículos." % (
        #            alb.id, alb.numalbaran, pv.descripcion, utils.float2str(pvs[pv][0]), utils.float2str(pvs[pv][1]))
        #        res = False
        #segun_precios_pedido_y_articulos = alb.calcular_total(iva_incluido = False, segun_factura = False)
        #segun_factura = alb.calcular_total(iva_incluido = False, segun_factura = True)
        #res = (round(segun_precios_pedido_y_articulos, 2) - round(segun_factura, 2)) == 0.0
        # Voy a hacer un calculote feo "porcima" para evitar los errores de cambios de producto y redondeos extraños en el cuarto decimal.
        total_factura = sum([pvs[pv][0] for pv in pvs])
        total_articulos = sum([pvs[pv][1] for pv in pvs])
        res = abs(int(total_factura) - int(total_articulos)) == 0
        #if not res:    # DEBUG
        #    print total_factura, total_articulos
    return res, total_articulos, total_factura

def buscar_albaranes(fecha_inicio = None, fecha_fin = None):
    if fecha_inicio and fecha_fin:
        albs = pclases.AlbaranSalida.select(
            pclases.AND(
                pclases.AlbaranSalida.q.fecha >= fecha_inicio, 
                pclases.AlbaranSalida.q.fecha <= fecha_fin), 
            orderBy = "-fecha")
    elif fecha_inicio:
        albs = pclases.AlbaranSalida.select(
            pclases.AlbaranSalida.q.fecha >= fecha_inicio, 
            orderBy = "-fecha")
    elif fecha_fin:
        albs = pclases.AlbaranSalida.select(
            pclases.AlbaranSalida.q.fecha <= fecha_fin, 
            orderBy = "-fecha")
    else:
        albs = pclases.AlbaranSalida.select(orderBy = "-fecha")
    return albs

def main ():
    global options, args
    albs = buscar_albaranes()
    print "Comprobando %d albaranes..." % albs.count()
    for a in albs:
        correcto, en_alb, en_fra = comprobar_cantidades_albaran(a)
        diferencia = en_fra - en_alb
        if not correcto:
            print "Albarán %s (%s) incorrecto. Factura %s. Se facturó a %s aproximadamente %d de %s." % (
                a.numalbaran, utils.str_fecha(a.fecha), ", ".join([f.numfactura for f in a.get_facturas()]), 
                a.cliente.nombre, abs(diferencia), diferencia >= 0 and "más" or "menos")

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
        #if len(args) < 1:
        #    parser.error ('missing argument')
        if options.verbose: print time.asctime()
        main()
        if options.verbose: print time.asctime()
        if options.verbose: print 'Tiempo total en minutos: ', 
        if options.verbose: print (time.time() - start_time) / 60.0
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'Error, excepción inesperada.'
        print str(e)
        traceback.print_exc()
        os._exit(1)

