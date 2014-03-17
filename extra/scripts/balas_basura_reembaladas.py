#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
17/03/2014

Resulta que había balas B que se han intentado reciclar como balas A para 
consumir en la línea de geotextiles.
El experimento ha sido un fiasco y dos semanas más tarde es cuando me mandan 
a regularizar las existencias. Hay una serie de balas que se han desmenuzado 
y vuelto a embalar como balas B. Hay otras que se han deshecho, cargado en 
el cuarto y vuelto a sacar para volver a envasar como balas "nuevas".
La estrategia es: dar de baja las balas B para sacarlas de almacén, crear las 
nuevas balas B en un parte de reenvasado (sin consumir materia prima) y 
corregir las partidas de carga donde se consumieron las pocas que se 
consumieron. El resto deben aparecer en el almacén como B para evitar que 
se vuelvan a cargar y estropeen de nuevo la línea por baja calidad de la fibra.

NO HAY MANERA DE CONSERVAR LA TRAZABILIDAD. Y quiero que esto quede bien 
clarito. Que cuando lo enganche lo voy a enganchar ben enganchao. Cristian. 
Que te chivaste... ¿quieres sentirla en el pecho?

Primera aproximación: parte de reenvasado con el alta de todas las balas. 
Albarán interno de consumo relacionado con el parte con todas las balas que 
se tienen que dar de baja. Ajustar las partidas de carga para meter las 
balas que cree con los pesos de las que se metieron en la abridora.

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

def load_data():
    """
    Devuelve una lista de balas a dar de baja y un diccionario de pesos a dar 
    de alta como balas nuevas B según el color.
    También devuelve un diccionario con los pesos de las balas a dar de alta 
    y después de baja como consumo en la partida de carga indicada en la clave.
    """
    baja = ["B116507", "B140861", "B144685", "B147610", "B117899", "B120590", 
            "B117808", "B121526", "B150509", "B130553", "B127066", "B148407", 
            "B140868", "B122233", "B120743", "B140869", "B142937", "B133069", 
            "B133761", "B142517", "B66485", "B133402", 
            # Ahora las que se metieron en el cuarto y se volvieron a sacar.
            "B66495", "B96497", "B96580", "B120810", "B122755", "B130052", 
            "B153597", "B153599", "B153600", "B153604", "B153605", "B153609", 
            "B153613"]
    alta = {"natural": [130.80, 197.00, 214.60, 187.20, 201.40, 200.20, 
                        193.00, 196.00, 166.20, 232.20, 149.60, 193.20], 
            "negro": [150.4, 204, 200, # Estas tres proceden de la "primera" 
                                       # lista de baja. Ahora las que se 
                                       # metieron y volvieron a sacar (la 
                                       # "segunda" lista de balas.
                      246, 236, 185, 257, 267, 246, 188, 253, 256, 244, 246, 
                      228.2, 109.2, 91.6, 127, 116, 123.2], 
            "gris": [166.80, 120.00, 84.20, 187.20, 114.00, 213.00, 170.00, 
                     212.80, 134.60, 176.00]}
    # TODO: Las balas que se consumieron, al parecer, eran negras. CONFIRMAR.
    consumo = {'PC8276': [175.50, 175.50, 203.50, 203.50], 
               'PC8277': [ 161.00, 162.00, 214.60, 107.60, 199.20, 159.00]} 
    return baja, alta, consumo

def main ():
    global options, args
    print "Empezamos..."
    # TODO: ¿Y con qué fecha hacemos todas estas operaciones?
    baja, alta, consumo = load_data()
    print "Finitto."

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

