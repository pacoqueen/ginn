#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
05/01/2010

Cachea los históricos de los productos de venta de un rango de fechas.

SYNOPSIS

    cachear_historicos_pv.py [-h,--help] [-v,--verbose] [--version] aaaammdd {aaaammdd}

DESCRIPTION

    Ejecuta el conteo de existencias de productos trazables en la fecha o 
    entre las dos fechas indicadas.

AUTHOR

    Francisco José Rodríguez Bogado (frbogado@novaweb.es)

VERSION

    $Id: cachear_historicos_pv.py,v 1.1 2010/07/20 08:22:57 pacoqueen Exp $
"""

import sys, os, traceback, optparse
import time
#from pexpect import run, spawn


import mx.DateTime
# Determino dónde estoy para importar pclases y utils
diractual = os.path.split(os.path.abspath(os.path.curdir))[-1]
if diractual == "fixes":
    path_to_f = os.path.join("..", "geotexinn02", "formularios")
    os.chdir(path_to_f)
from framework import pclases
from formularios import utils
import gc
import psycopg2  # @UnusedImport
import psycopg2.extras

def convierte_a_fecha(cad):
    """
    Convierte una cadena de la forma aaaammdd a una fecha mx.
    """
    try:
        cad = cad.strip()
        anno = int(cad[:4])
        mes = int(cad[4:6])
        dia = int(cad[6:])
        fecha = mx.DateTime.DateTimeFrom(anno, mes, dia)
    except Exception, e:
        print "%s no es una fecha en formato aaaammdd.\nError:" % cad
        print e
        sys.exit(2)
    return fecha

def parsea_fechas_argumentos(args):
    fechas = []
    if len(args) == 0:
        print globals()['__doc__']
        sys.exit(1)
    elif len(args) == 2:
        ini, fin = map(convierte_a_fecha, args[:])
        if ini > fin:
            ini, fin = fin, ini
        fecha = ini
        fechas.append(fecha)
        for i in range(int((fin - ini).days)):  # @UnusedVariable
            fecha += mx.DateTime.oneDay
            fechas.append(fecha)
    else:
        fechas += map(convierte_a_fecha, args[:])
    return fechas

def parse_uri(uri):
    """
    Devuelve usuario, contraseña, host y nombre de la BD a partir de la 
    cadena recibida.
    """
    if "://" in uri:    # Es uri de pclases
        tipo, resto = uri.split("://")  # @UnusedVariable
    else:
        resto = uri
    user, resto = resto.split(":")
    password, resto = resto.split("@")
    host, database = resto.split("/")
    return user, password, host, database

def abrir_conexion_local():
    """
    Devuelve una conexión con la BD local.
    """
    uri = pclases.conn
    user, password, host, database = parse_uri(uri)
    return abrir_conexion(user, password, host, database)

def abrir_conexion_remota():
    """
    Devuelve una conexión con la BD destino.
    """
    uri = options.destino
    if uri.strip():
        user, password, host, database = parse_uri(uri)
        return abrir_conexion(user, password, host, database)
    else:
        return None

def abrir_conexion(user, password, host, database):
    return psycopg2.connect(user = user, password = password, 
                            host = host, database = database)

def recolectar_ids(ids_antes):
    con = abrir_conexion_local()
    cur = con.cursor()
    for tabla in ids_antes:
        cur.execute("SELECT id FROM %s;" % tabla)
        l = cur.fetchall()
        for tupla in l:
            ide = tupla[0]
            ids_antes[tabla].append(ide)
    con.close()

def fotografiar_ids():
    """
    Devuelve un diccionario con los IDs de las tablas de historiales.
    """
    ids_antes = {"historial_existencias": [], 
                 "historial_existencias_A": [], 
                 "historial_existencias_B": [], 
                 "historial_existencias_C": []}
    recolectar_ids(ids_antes)
    return ids_antes

def main ():
    # DONE: Dar información de tiempo restante estimado. Permitir hacer solo 
    # históricos de una clase (solo A, por ejemplo) y parciales para que 
    # se pueda parar y seguir en otro momento.
    global options, args
    fechas = parsea_fechas_argumentos(args)
    #ids_antes = fotografiar_ids()
    for fecha in fechas:
        cadfecha = "Cacheando históricos para la fecha %s" % (
            utils.str_fecha(fecha))
        print cadfecha.center(80, "=")
        prods = pclases.ProductoVenta.select(orderBy = "id")
        i = 0
        principio = time.time()
        for pv in prods:
            antes = time.time()
            print pv.get_info()
            print "\tExistencias, A, B y C:", 
            if "T" in options.clase.upper():
                print pv.get_existencias(hasta = fecha, 
                                         forzar = options.forzar, 
                                         actualizar = True), 
            else:
                print "-", 
            sys.stdout.flush()
            if "A" in options.clase.upper():
                print pv.get_existencias_A(hasta = fecha, 
                                           forzar = options.forzar, 
                                           actualizar = True), 
            else:
                print "-", 
            sys.stdout.flush()
            if "B" in options.clase.upper():
                print pv.get_existencias_B(hasta = fecha, 
                                           forzar = options.forzar, 
                                           actualizar = True), 
            else:
                print "-", 
            sys.stdout.flush()
            if "C" in options.clase.upper():
                print pv.get_existencias_C(hasta = fecha, 
                                           forzar = options.forzar, 
                                           actualizar = True), 
            else:
                print "-", 
            sys.stdout.flush()
            print
            print "\tStock, A, B y C:", 
            if "T" in options.clase.upper():
                print pv.get_stock(hasta = fecha, forzar = options.forzar, 
                                   actualizar = True), 
            else:
                print "-", 
            sys.stdout.flush()
            if "A" in options.clase.upper():
                print pv.get_stock_A(hasta = fecha, 
                                     forzar = options.forzar, 
                                     actualizar = True), 
            else:
                print "-", 
            sys.stdout.flush()
            if "B" in options.clase.upper():
                print pv.get_stock_B(hasta = fecha, 
                                     forzar = options.forzar, 
                                     actualizar = True), 
            else:
                print "-", 
            sys.stdout.flush()
            if "C" in options.clase.upper():
                print pv.get_stock_C(hasta = fecha, 
                                     forzar = options.forzar, 
                                     actualizar = True), 
            else:
                print "-", 
            sys.stdout.flush()
            print
            gc.collect()
            i += 1
            tiempo_prod = time.time() - antes
            tiempo_total = time.time() - principio
            hechos = i
            restantes = prods.count() - i 
            estimacion_n_productos= (restantes * tiempo_total) / hechos
            estimacion_1_producto = restantes * tiempo_prod
            # Media ponderada. El último producto es el que menos peso tiene  
            # en la estimación total.
            eta = (estimacion_1_producto 
                   + (estimacion_n_productos * i)) / i + 1
            eta /= 60   # En minutos
            horas_o_minutos = "minutos"
            if eta > 60:
                eta /= 60.0
                horas_o_minutos = "horas"
            print "> (%d/%d) [%.1f %%] Tiempo restante estimado: %d %s"%(
                i, prods.count(), (float(i) / prods.count()) * 100, eta, 
                horas_o_minutos)
    #ids_despues = fotografiar_ids()
    if options.no_preguntar:
        res = "S"
    else:
        res = raw_input("¿Sincronizar tablas de %s? [Sí/{No}]" % (
                        options.destino))
    try:
        res = res.upper().strip()[0]
    except:
        res = None
    if res == "S":
        #volcar_a_bd_remota(ids_antes, ids_despues)
        sincronizar_tablas()

def sincronizar_tablas():
    """
    Sincroniza las tablas de historiales entre la conexión local y la BD 
    remota en función de la clase pasada por parámetro.
    La actualización siempre es unidireccional y se comprueba que la BD 
    origen y destino sean diferentes (en host y nombre).
    """
    # 0.- Verificar que no voy a volcarme sobre mí mismo.
    uridest = options.destino
    userdest, passworddest, hostdest, databasedest = parse_uri(uridest)  # @UnusedVariable
    urilocal = pclases.conn
    userlocal, passwordlocal, hostlocal, databaselocal = parse_uri(urilocal)  # @UnusedVariable
    if hostlocal == hostdest and databasedest == databaselocal:
        print "Destino y origen son iguales. No se sincronizará nada."
    else:
        # 1.- Recorrer todos los registros de las tablas y:
        conremota = abrir_conexion_remota()
        if conremota:
            conlocal = abrir_conexion_local()
            curlocal = conlocal.cursor()
            curremoto = conremota.cursor(
                cursor_factory = psycopg2.extras.DictCursor)
            for tipo in options.clase:
                tabla = {'T': "historial_existencias", 
                         'A': "historial_existencias_a", 
                         'B': "historial_existencias_b", 
                         'C': "historial_existencias_c", 
                        }[tipo]
                curlocal.execute("SELECT * FROM %s;" % tabla)
                for tupla in curlocal.fetchall():
                    (ide, producto_venta_id, fecha, 
                     cantidad, bultos, almacen_id) = tupla
                    # 2.- Si existe en la BD remota, actualizo el registro
                    curremoto.execute("""
                        SELECT * 
                          FROM %s 
                         WHERE -- ide = %d AND 
                               producto_venta_id = %d 
                           AND fecha = '%s'
                           AND almacen_id = %d; """ 
                        % (tabla, ide, producto_venta_id, fecha, almacen_id))
                    tuplaremota = curremoto.fetchone() 
                    if tuplaremota:
                        if (tuplaremota['cantidad'] == cantidad and 
                            tuplaremota['bultos'] == bultos):
                            if options.very_verbose:
                                print "Ignorando %s..." % tuplaremota
                            continue    # No ha cambiado. Lo ignoro.
                        else:
                            print " === Actualizando %s..." % str(tuplaremota)
                            curremoto.execute("""
                                UPDATE %s 
                                   SET cantidad = %f, bultos = %d
                                 WHERE producto_venta_id = %d
                                   AND fecha = '%s'
                                   AND almacen_id = %d;
                            """ % (tabla, cantidad, bultos, producto_venta_id, 
                                   fecha.strftime("%Y-%m-%d"), almacen_id))
                            conremota.commit()
                    # 3.- Y si no, lo creo nuevo.
                    else:   
                        print " --> Insertando %s..." % str(tupla)
                        sql = """
                            INSERT INTO %s (producto_venta_id, 
                                            fecha, 
                                            cantidad, 
                                            bultos, 
                                            almacen_id)
                                    VALUES (%d, '%s', %f, %d, %d); 
                        """ % (tabla, producto_venta_id, 
                               fecha.strftime("%Y-%m-%d"), cantidad, bultos, 
                               almacen_id)
                        curremoto.execute(sql)
                        conremota.commit()
            conlocal.close()
            conremota.close()

def volcar_a_bd_remota(ids_antes, ids_despues):
    """
    Compara los diccionarios de ids y vuelca, si lo confirma el usuario, los 
    registros en la BD remota.
    """
    conremota = abrir_conexion_remota()
    if conremota:
        conlocal = abrir_conexion_local()
        curlocal = conlocal.cursor()
        curremoto = conremota.cursor()
        for tabla in ids_despues:
            for aidi in ids_despues[tabla]:
                #print aidi, type(aidi)
                if aidi not in ids_antes[tabla]:
                    tupla = curlocal.execute("SELECT * FROM %s WHERE aidi = %d;" 
                        % (tabla, aidi)).fetchone()
                    valores = ", ".join("'%s'" % v for v in tupla)
                    curremoto.execute("INSERT INTO %s VALUES (%s);" % (
                        tabla, valores))
                    print "Registro ID %d insertado." % aidi

# DONE: ¿Sabes lo que sería la repera? Poder enviar los cálculos a otro 
# ordenador y rescatar los registros e insertarlos directamente en la BD. O al 
# contrario. Que el script calcule y al final envíe los registros de 
# históricos recién creados a alfred.

if __name__ == '__main__':
    try:
        start_time = time.time()
        parser=optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), 
                                     usage=globals()['__doc__'], 
                                     version='$Id: cachear_historicos_pv.py,v 1.1 2010/07/20 08:22:57 pacoqueen Exp $')
        parser.add_option('-v', 
                          '--verbose', 
                          action='store_true', 
                          default=False, 
                          help='verbose output')
        parser.add_option('-w', 
                          '--verbose2', 
                          action = 'store_true', 
                          default = False, 
                          help = 'Very verbose output (implica -v).', 
                          dest = "very_verbose")
        parser.add_option('-c', '--clase', default = "ABCT", dest = "clase", 
                        help="A: clase A; B:clase B; C: clase C; T: Totales")
        parser.add_option("-f", "--forzar", action = "store_true", 
                          default = True, 
                          help = "Limpiar cachés antes de recalcular.", 
                          dest = "forzar")
        parser.add_option("-n", "--no-forzar", action = "store_false", 
                          help = "No limpiar cachés antes de recalcular.", 
                          dest = "forzar")
        parser.add_option("-d", "--dest", 
                          default = "geotexan:gy298d.l@alfred/ginn", 
                          dest = "destino", 
                          help = 'Volcar los registros creados en una base '
                                 ' de datos en un host diferente. Pedirá '
                                 'confirmación antes a no ser que se pase el '
                                 'parámetro "-y". Pasar la cadena '
                                 'vacía ("") para ignorar este paso. Formato '
                                 'de uri: user:password@host/database')
        parser.add_option('-y', 
                          '--yesdest', 
                          action = 'store_true', 
                          default = False, 
                          dest = "no_preguntar", 
                          help = 'No preguntar si volcar a destino.')
        (options, args) = parser.parse_args()
        #print options, args
        #if len(args) < 1:
        #    parser.error ('missing argument')
        if options.very_verbose:
            options.verbose = True
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

