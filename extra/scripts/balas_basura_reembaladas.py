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
            "B133761", "B142517", "B66485",  "B133402", 
            # Ahora las que se metieron en el cuarto y se volvieron a sacar.
            "B66495",  "B96497",  "B96580",  "B120810", "B122755", "B130052", 
            "B153598", "B153599", "B153600", "B153604", "B153605", "B153609", 
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
    # Las balas que se consumieron, al parecer, eran negras.
    consumo = {'PC12286': {"negro": [175.50, 175.50, 203.50, 203.50, 161.00,
                                     162.00, 214.60, 107.60, 199.20, 159.00]}}
    return baja, alta, consumo

def determinar_fecha_operaciones():
    # La partida de carga era de esa fecha. Así que lo hago todo con esa 
    # fecha, que además era el día de Andalucía, y no hay partes de producción.
    return mx.DateTime.DateFrom(2014, 2, 28)

def create_parte_reenvasado(alta, color, fecha, dic_consumo):
    """
    Crea un parte de reenvasado y da de alta en él las balas con el color 
    designado y calidad B; del producto que sea según el color y en un 
    lote nuevo.
    Para no solapar los partes y como serán 3, voy a crear el de negro a 
    las 6 AM, el de natural a las 14 y el de mezcla (gris) a las 22.
    Del diccionario de balas consumidas trato de sacar las del color que se 
    va a "fabricar" en este parte para meterlas y poderlas después consumir 
    en la partida de carga.
    """
    pdp = None
    if color == "negro":
        # XXX: OJO: Hay mezcladas balas de dos cortes: 6.7 y 75; dos títulos: 
        # 4.4 y 6.7; y dos colores: negro y natural. Yo, por simplificar y 
        # porque si no voy a tener que crear cuatro o cinco partes diferentes 
        # para al final sacrificar la trazabilidad igualmente, voy a crear 
        # todas las balas como 4.4/60 (que son la mayoría) y solo dos colores:
        # natural y negro (las gris las meto en otro parte de negro) y todas 
        # aclarando en las observaciones que van con mezcla de título y tal.
        # Porque hay que tener en cuenta también que cada parte debe llevar 
        # un lote diferente. Tres lotes para esta chapuza es más que 
        # suficiente.
        pv = pclases.ProductoVenta.selectBy(
                descripcion = "FIBRA PP 4.4/60 NEGRO")[0]
        hora = 6
    elif color == "natural":
        pv = pclases.ProductoVenta.selectBy(
                descripcion = "Fibra PP 4.4/75")[0] # De natural todas son a 75
        hora = 14
    else:   # color = gris
        pv = pclases.ProductoVenta.selectBy(
                descripcion = "FIBRA PP 4.4/60 NEGRO")[0]
        hora = 22
    pdp = crear_pdp_reenvasado(fecha, hora, pv)
    lote = crear_lote_nuevo()
    agregar_balas(pdp, alta[color], pv, lote)
    # Ahora intento crear las balas que se consumieron.
    for codpc in dic_consumo:
        try:
            mas_pesos = dic_consumo[codpc][color] 
        except KeyError:
            pass    # No hay más balas
        else:
            agregar_balas(pdp, mas_pesos, pv, lote)
    return pdp

def agregar_balas(pdp, pesos, pv, lote):
    """
    Agrega las balas al parte creando los artículos intermedios del producto 
    y lote recibido.
    """
    for peso in pesos:
        print "\tCreando bala con peso %.2f..." % peso
        numbala = pclases.Bala._queryOne("""
                        SELECT COALESCE(MAX(numbala), 0)+1 FROM bala""")[0]
        bala = pclases.Bala(lote = lote, 
                            numbala = numbala, 
                            codigo = "B%d" % numbala, 
                            pesobala = peso, 
                            muestra = False, 
                            claseb = True, 
                            motivo = "Mezcla de título, corte y color."
                                     " Reenvasada a partir de balas B.", 
                            partidaCarga = None)
                            # fechahora de creación dejo por defecto la de hoy
        almacen_gtx = pclases.Almacen.get_almacen_principal()
        articulo = pclases.Articulo(bala = bala, 
                                    rollo = None, 
                                    parteDeProduccion = pdp, 
                                    productoVenta = pv, 
                                    albaranSalida = None, 
                                    bigbag = None, 
                                    rolloDefectuoso = None, 
                                    balaCable = None, 
                                    rolloC = None, 
                                    almacen = almacen_gtx, 
                                    caja = None) 

def crear_lote_nuevo():
    """
    Crea un lote de fibra nuevo justo a continuación del último dado de 
    alta (por orden de número de lote) y lo devuelve.
    No tiene por qué ser el último conológicamente. (Y de hecho, casi seguro 
    que no será. Hay un lote 15.000 que se crearía por algún ajuste y 
    actualmente la fibra va por el lote seis mil y pico)
    """
    numlote = pclases.Lote.select(orderBy = "-numlote")[0].numlote + 1
    codigo = "L-%d" % numlote
    lote = pclases.Lote(numlote = numlote, codigo = codigo)
    return lote
    

def crear_pdp_reenvasado(fecha, hora, pv):
    """
    Crea un parte interno de reenvasado de fibra que empieza en la fecha y 
    hora especificadas y acaba 8 horas más tarde.
    """
    horaini = mx.DateTime.TimeFrom(hours = hora)
    horafin = mx.DateTime.TimeFrom(hours = hora + 8)
    if horafin.day > 0:     # Cae en el día siguiente
        horafin -= mx.DateTime.oneDay
    fechahoraini = utils.unir_fecha_y_hora(fecha, horaini)
    fechahorafin = utils.unir_fecha_y_hora(fecha, horafin)
    if fechahorafin < fechahoraini:     # Acaba la madrugada siguiente.
        fechahorafin += mx.DateTime.oneDay
    pdp = pclases.ParteDeProduccion(fecha = fecha, 
                                    horainicio = horaini,
                                    horafin = horafin,
                                    fechahorainicio = fechahoraini, 
                                    fechahorafin = fechahorafin, 
                                    prodestandar = pv.prodestandar,
                                    observaciones = ';;;;;REENVASADO',
                                    bloqueado = True)
    return pdp

def consumir_en_albaran_interno(codsbalas, pdp):
    """
    Obtiene el albarán interno del parte de producción donde se "consumirán" 
    las balas cuyos códigos he recibido.
    De este modo puedo guardar algo parecido a la trazabilidad, aunque de 
    entrada requiera una operación manual porque el programa no soporta este 
    tipo de trazabilidad entre balas y partes de reenvasado con nuevas balas.
    """
    alb = pdp.buscar_o_crear_albaran_interno()
    alb.facturable = False  # Se supone que ya lo era, pero por si acaso.
    alb.motivo = "Albarán de consumo de balas B para reembolsar en parte %s."%(
            pdp.get_info())
    prods = []
    for cod in codsbalas[:]:
        b = pclases.Bala.selectBy(codigo = cod)[0]
        color_bala = b.articulo.productoVenta.camposEspecificosBala.color 
        color_pdp = pdp.productoVenta.camposEspecificosBala.color
        if color_bala == color_pdp:
            # DONE: Cada bala que doy de baja debe ir a un albarán 
            # interno diferente en función del color ya que se habrán 
            # consumido en el parte de producción de las nuevas balas de ese 
            # color (NOTA: ¿Y las grises?). 
            b.articulo.albaranSalida = alb
            b.articulo.almacen = None
            codsbalas.remove(cod)
            if b.articulo.productoVenta not in prods:
                prods.append(b.articulo.productoVenta)
    # Creo las líneas de venta con el producto pero a 0 porque no tienen pedido
    for p in prods:
        pclases.LineaDeVenta(productoVenta = p, 
                             albaranSalida = alb, 
                             pedidoVenta = None, 
                             facturaVenta = None, 
                             prefactura = None, 
                             # fechahora por defecto
                             cantidad = 0, 
                             precio = 0, 
                             descuento = 0, 
                             productoCompra = None, 
                             ticket = None, 
                             notas = "Creado por regularización de conversión"
                                " de balas B en otras nuevas para consumir.", 
                             descripcionComplementaria = "")

def consumir_fibra(dic_consumo, pdp):
    """
    Agrega las balas reconvertidas y consumidas en la línea de geotextiles 
    a la partida de carga que corresponde.
    De las balas inicialmente tengo el peso en dic_consumo; pero recibo 
    también el parte de producción donde se han creado, así que busco 
    según el peso la primera bala que esté en almacén en ese momento y la 
    saco de almacén a la vez que la agrego a la partida de carga.
    """
    for codpc in dic_consumo:
        pc = pclases.PartidaCarga.selectBy(codigo = codpc)[0]
        for color in dic_consumo[codpc]: # El color en realidad da igual porque
                        # las tengo controladas y localizadas como fibra negra.
            for peso in dic_consumo[codpc][color]:
                bala = buscar_bala_por_peso(pdp, peso)
                bala.articulo.almacen = None
                bala.partidaCarga = pc

def buscar_bala_por_peso(pdp, peso):
    """
    Devuelve la primera de las balas del parte recibido cuyo peso coincida 
    con el del parámetro y esté en almacén.
    """
    for a in pdp.articulos:
        if a.peso_sin == peso and a.en_almacen() and a.bala:
            return a.bala
    return None     # Esto no debería pasar

def main ():
    global options, args
    print "Empezamos..."
    fecha = determinar_fecha_operaciones()
    baja, alta, consumo = load_data()
    # Primero el parte de reenvasado. De donde sacaré además el albarán 
    # interno de consumo donde poder dar de baja las balas.
    print "Creando partes de reenvasado (1/3)..."
    pdp_natural = create_parte_reenvasado(alta, "natural", fecha, consumo)
    print "Creando partes de reenvasado (2/3)..."
    pdp_negro = create_parte_reenvasado(alta, "negro", fecha, consumo)
    print "Creando partes de reenvasado (3/3)..."
    pdp_gris = create_parte_reenvasado(alta, "gris", fecha, consumo)
    print "Baja de balas B en albarán interno (1/3)..."
    alb_natural = consumir_en_albaran_interno(baja, pdp_natural)
    print "Baja de balas B en albarán interno (2/3)..."
    alb_negro = consumir_en_albaran_interno(baja, pdp_negro)
    print "Baja de balas B en albarán interno (3/3)..."
    alb_gris = consumir_en_albaran_interno(baja, pdp_gris)
    print "Creando y consumiendo fibra reconvertida..."
    consumir_fibra(consumo, pdp_negro)
    print "Finitto."
    print "Creados los partes:"
    for pdp in (pdp_natural, pdp_negro, pdp_gris):
        print "\t%s" % pdp.get_info()
    print "Creados los albaranes:"
    for pdp in (pdp_natural, pdp_negro, pdp_gris):
        print "\t%s" % pdp.get_albaran_interno().get_info()
    print "Y ajustada la partida de carga %s" % consumo.keys()[0]

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

