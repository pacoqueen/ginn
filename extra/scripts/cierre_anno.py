#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
04/01/2010

Paso de año en ginn.
Básicamente lo único que hace es clonar los contadores del año indicado y 
reasignar sus clientes en un contador nuevo.

SYNOPSIS

    cierre_anno [-h,--help] [-v,--verbose] [--version]

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


def detect_anno_cierre():
    """
    Si la fecha actual es de enero, estamos cerrando el año pasado. Si estamos 
    en diciembre es que estamos cerrando el año actual. 
    NOTA: En realidad cojo junio como pivote, no enero ni diciembre.
    """
    hoy = mx.DateTime.today()
    if hoy.month <= 6:
        return hoy.year - 1
    return hoy.year

def buscar_contadores(anno):
    """
    Devuelve todos los contadores que hayan facturado algo en el año recibido.
    """
    FV = pclases.FacturaVenta
    fras = FV.select(pclases.AND(
        FV.q.fecha >= mx.DateTime.DateTimeFrom(anno, 1, 1), 
        FV.q.fecha <= mx.DateTime.DateTimeFrom(anno, 12, 31)))
    conts = utils.unificar([fra.get_contador() for fra in fras])
    return conts

def pasar_presufi(s):
    """
    Detecta en la cadena «s» la posible aparición del año y devuelve la 
    misma cadena pero con todos los números (completos, no sus cifras por 
    separado) que encuentre incrementados en uno.
    """
    def agregar(c, l):
        """
        Si «c» es del mismo tipo que los caracteres del último grupo de «l» 
        devuelve True.
        """
        if len(l) and len(l[-1]):
            if l[-1][-1].isalpha() and c.isalpha():
                return True
            if l[-1][-1].isdigit() and c.isdigit():
                return True
        return False
    # Primero separo letras y números.
    letras_nums = []
    for c in s:
        if agregar(c, letras_nums):
            letras_nums[-1].append(c)
        else:
            letras_nums.append([c])
    # Ahora intento pasar año:
    res = ""
    for grupo_de_letras_o_nums in letras_nums:
        palabraca = "".join(grupo_de_letras_o_nums)
        numeraco = utils.parse_numero(palabraca)
        if isinstance(numeraco, int):
            numeraco += 1
            palabraca = `numeraco`
        res += palabraca
    return res

def pasar_contador(contador):
    """
    Crea un contador nuevo basado en el recibido y reasigna sus clientes.
    """
    prefijo = pasar_presufi(contador.prefijo)
    sufijo = pasar_presufi(contador.sufijo)
    try:    # Puede que ya exista el contador. Lo reutilizo
        nuevocontador = pclases.Contador.select(pclases.AND(
                pclases.Contador.q.prefijo == prefijo, 
                pclases.Contador.q.sufijo == sufijo), 
            orderBy = "-id")[0]
    except IndexError:  # Si no existe, entonces sí que lo creo.
        nuevocontador = contador.clone(prefijo = prefijo, sufijo = sufijo, 
                                       contador = 1)
    print "\tPasando contador %s (%d facturas)." % (contador, 
                                                len(contador.get_facturas()))
    print "\tContador %s creado o reusado." % nuevocontador
    print "\tPasando %d clientes..." % len(contador.clientes), 
    sys.stdout.flush()
    for cliente in contador.clientes:
        cliente.contador = nuevocontador
        cliente.sync()
        print ".", 
        sys.stdout.flush()
    print 

def main ():
    global options, args
    anno_cierre = detect_anno_cierre()
    contadores = buscar_contadores(anno_cierre)
    print "Pasando %d contadores..." % len(contadores)
    for contador in contadores:
        pasar_contador(contador)

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

