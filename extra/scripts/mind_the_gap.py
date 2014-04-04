#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
04/04/2014

Mind the gap
============

Detecta los posibles errores de existencias en la fecha dada.

Gaps:
    * Artículos con fecha de fabricación posterior a la fecha de entrada en
      almacén: pertenecen a un parte de producción con fecha > `fecha` pero
      el artículo (su `fechahora`) en realidad se fabricó antes de `fecha`.

SYNOPSIS

    mind_the_gap.py [-h,--help] [-v,--verbose] [--version] dd[/mm[/aa[aa]]]

EJEMPLO
./mind_the_gap.py 01/04/2014

VERSION

    $Id$
"""

import sys
import os
import traceback
import optparse
import time
#from pexpect import run, spawn
from collections import defaultdict

#import mx.DateTime
# Determino dónde estoy para importar pclases y utils
DIRACTUAL = os.path.split(os.path.abspath(os.path.curdir))[-1]
try:
    FULLDIRPADRE = os.path.split(os.path.abspath(os.path.curdir))[0]
    DIRPADRE = os.path.split(FULLDIRPADRE)[-1]
except IndexError:
    sys.exit(2)  # Where The Fuck am I?
assert DIRACTUAL == "scripts" or DIRPADRE == "tests", \
                    "Debe ejecutar el script desde el directorio donde reside"\
                    " o bien desde un subdirectorio de `tests`."
sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "ginn")))
from framework import pclases
#from framework import tests_coherencia
from formularios import utils


def fabricados_fuera_del_parte(pivote):
    """
    Busca artículos fabricados en la fecha `pivote` pero que pertenecen a
    una producción anterior a esa fecha o posterior a la misma. Es decir:
    1. El artículo se dió de alta el 31 de marzo y su parte es del 2 de abril:
       el artículo habrá contado como existencias el día 1 y además entra como
       producción del 1 al 30 de abril. Se cuenta dos veces:
            existencias(31 marzo) + produción(1 al 30 abril) = 2
            existencias_reales(1 mayo) = 1
            diff(final, total) = -1
    2.- El artículo es posterior a su parte de producción: el artículo es del
        día 2 de abril pero su parte de producción es del 31 de marzo. No
        entrará en el cálculo de existencias finales pero sí entra como
        existencia real:
            existencias(31 marzo) + producción(1 al 30 abril) = 0
            existencias_reales(1 mayo) = 1
            diff(final, total) = 1
    """
    prods_gap1 = defaultdict(lambda: [])
    prods_gap2 = defaultdict(lambda: [])
    print "Detectando gap 1.1"
    for subclase in (pclases.Bala, 
                     pclases.BalaCable, 
                     pclases.Bigbag, 
                     pclases.Caja, 
                     pclases.Rollo, 
                     pclases.RolloDefectuoso, 
                     pclases.RolloC):
        subobjetos = subclase.select(subclase.q.fechahora < pivote)
        tot = subobjetos.count() 
        i = 0.0
        for subobjeto in subobjetos:
            i += 1 
            sys.stdout.write("\r[%s] %3d/%d" % (subclase.__name__, i, tot))
            sys.stdout.flush()
            #fecha_alta = mx.DateTime.DateFrom(a.fechahora)
            articulo = subobjeto.articulo
            if articulo.fecha_fabricacion > pivote:
                prodventa = articulo.productoVenta
                prods_gap1[prodventa].append(articulo)
        sys.stdout.write("\n")
    print "Detectando gap 1.2"
    for subclase in (pclases.Bala, 
                     pclases.BalaCable, 
                     pclases.Bigbag, 
                     pclases.Caja, 
                     pclases.Rollo, 
                     pclases.RolloDefectuoso, 
                     pclases.RolloC):
        subobjetos = subclase.select(subclase.q.fechahora >= pivote)
        tot = subobjetos.count()
        i = 0
        for subobjeto in subobjetos:
            i += 1 
            sys.stdout.write("\r[%s] %3d/%d" % (subclase.__name__, i, tot))
            sys.stdout.flush()
            #fecha_alta = mx.DateTime.DateFrom(a.fechahora)
            articulo = subobjeto.articulo
            if articulo.fecha_fabricacion < pivote:
                prodventa = articulo.productoVenta
                prods_gap2[prodventa].append(articulo)
        sys.stdout.write("\n")
    return prods_gap1, prods_gap2


def dump(dic, desc="", sentido=+1):
    """
    Escupe por salida estándar (de momento) el listado de productos y
    cantidades del diccionario. Las cantidades van en el `sentido` recibido:
    +1 si hay que compensarlas sumando porque la diferencia entre las
    existencias finales y lo calculado es negativa.
    -1 si hay que compensar restando porque la diferencia entre las
    existencias finales y lo calculado es positiva.
    """
    print desc
    for producto in dic:
        cant = sum([a.get_cantidad() for a in dic[producto]])
        cant *= sentido
        desc_prod = producto.descripcion
        print "\t[%s]" % "; ".join([a.codigo for a in dic[producto]])
        print "\t\t%s: %s" % (desc_prod, utils.float2str(cant))


def main(fecha):
    """
    Recorre todos los artículos de la base de datos en busca de "gaps" en la
    fecha recibida.
    """
    pivote = utils.parse_fecha(fecha)
    gap1, gap2 = fabricados_fuera_del_parte(pivote)
    dump(gap1, "Artículos en almacén antes de ser fabricados", +1)
    dump(gap2, "Artículos fabricados antes de entrar en almacén", -1)

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
        if len(args) < 1:
            parser.error('Debe especificar una fecha')
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
