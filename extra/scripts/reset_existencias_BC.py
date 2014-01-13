#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
13/01/2014

Se ponen todas las existencias B y C de todos los productos a cero mediante 
un albarán de ajuste de primeros de 2014.

"""

import sys, os, traceback, optparse
import time
import re
#from pexpect import run, spawn


import mx, mx.DateTime
NUMALBARAN = "A_AJUSTE_ENE_DOSMILCATORCE"
FECHA_AJUSTE = mx.DateTime.DateFrom(2014, 1, 1)
# Determino dónde estoy para importar pclases y utils
diractual = os.path.split(os.path.abspath(os.path.curdir))[-1]
assert diractual == "scripts", \
        "Debe ejecutar el script desde el directorio donde reside."
sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "ginn")))
from framework import pclases
from formularios import utils

def anular(a, alb):
    """
    Agrega el producto a al albarán de ajuste recibido o creado.
    """
    a.almacen = None
    a.albaranSalida = alb
    a.sync()

def buscar_o_crear_albaran_ajuste():
    """
    Busca un albarán de ajuste MUY específico. 
    """
    try:
        alb = pclases.AlbaranSalida.select(pclases.AND(
            pclases.AlbaranSalida.q.fecha == FECHA_AJUSTE, 
            pclases.AlbaranSalida.q.numalbaran == NUMALBARAN))[0]
        print "Albarán %s encontrado." % alb.numalbaran
    except IndexError:
        empresa = pclases.DatosDeLaEmpresa.get_propia_empresa_como_cliente()
        alb = pclases.AlbaranSalida(numalbaran = NUMALBARAN, 
                fecha = FECHA_AJUSTE, 
                facturable = False, 
                cliente = empresa, 
                bloqueado = False, 
                transportista = None, 
                motivo = "Albarán de ajuste de existencias B y C", 
                almacenOrigen = pclases.Almacen.get_almacen_principal(), 
                almacenDestino = None)
        print "Albarán %s creado." % alb.numalbaran
    return alb


def main ():
    global options, args
    print "Empezamos..."
    articulos = pclases.Articulo.select(orderBy = "id")
    tot = articulos.count()
    i = 0
    puntos = 0
    alb = buscar_o_crear_albaran_ajuste()
    for a in articulos:
        i += 1
        if a.en_almacen() and (a.es_clase_b() or a.es_clase_c()):
            print "Anulando %s (%d/%d)." % (a.codigo, i, tot)
            anular(a, aajuste)
        else:
            puntos += 1
            print ".", 
            if puntos >= 100:
                puntos = 0
                print "<%d/%d>" % (i, tot), 
            sys.stdout.flush()
    print "Finitto. Ahora abre el albarán %s para que se creen "\
            "automáticamente las líneas de venta y bloquéalo si todo está "\
            "correcto." % NUMALBARAN

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

