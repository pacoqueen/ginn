#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, pclases, mx.DateTime
sys.path.append(os.path.join("..", "formularios"))
import utils  # @UnresolvedImport

def buscar_rollos_existencias(fecha):
    """
    Devuelve una lista de rollos en almacén hasta (incluida) 
    la fecha dada.
    """
    sqlfecha = fecha.strftime('%Y-%m-%d')
    fecha_limite_para_comparaciones_con_fechahoras = (fecha + mx.DateTime.oneDay).strftime('%Y-%m-%d')
    albaranes_antes_de_fecha = """
        SELECT albaran_salida.id 
        FROM albaran_salida 
        WHERE albaran_salida.fecha <= '%s' 
    """ % (sqlfecha)
    partes_antes_de_fecha = """
        SELECT parte_de_produccion.id 
        FROM parte_de_produccion 
        WHERE parte_de_produccion.fecha <= '%s' 
    """ % (sqlfecha)
    articulos_de_rollos_anteriores_a_fecha = """
        SELECT rollo.id 
        FROM rollo 
        WHERE rollo.fechahora < '%s' 
    """ % (fecha_limite_para_comparaciones_con_fechahoras)
        # Porque fechahora contiene fecha y hora, y p.ej.: 1/1/2006 10:23 no es <= 1/1/2006 0:00 (que sería la fecha recibida)
    parte_where = """
         articulo.rollo_id IS NOT NULL 
         AND (articulo.parte_de_produccion_id IN (%s) OR (articulo.parte_de_produccion_id IS NULL 
                                                      AND (articulo.rollo_id IN (%s AND articulo.rollo_id = rollo.id))))
         AND (articulo.albaran_salida_id IS NULL OR articulo.albaran_salida_id NOT IN (%s)) 
    """ % (partes_antes_de_fecha, 
           articulos_de_rollos_anteriores_a_fecha, 
           albaranes_antes_de_fecha)
# ¿Daría otro resultado con "AND (articulo.albaran_salida_id IS NULL OR articulo.albaran_salida_id IN (albaranes_POSTERIORES_a_fecha))"?
    articulos_en_almacen = pclases.Articulo.select(parte_where)
    rollos = [a.rollo for a in articulos_en_almacen]
    return rollos

def buscar_rollos_fabricados(fecha_ini, fecha_fin):
    """
    Devuelve una lista de rollos fabricados entre las dos fechas recibidas.
    """
    rollos = []
    partes = pclases.ParteDeProduccion.select(pclases.AND(pclases.ParteDeProduccion.q.fecha >= fecha_ini, 
                                                          pclases.ParteDeProduccion.q.fecha <= fecha_fin))
    for parte in partes:
        if parte.es_de_geotextiles():
            for articulo in parte.articulos:
                rollos.append(articulo.rollo)
    fechasqlini = fecha_ini.strftime('%Y-%m-%d')
    fechasqlfin = (fecha_fin + mx.DateTime.oneDay).strftime('%Y-%m-%d')
    articulos_de_rollos_sin_parte_de_produccion_y_entre_fechas = pclases.Articulo.select("""
    rollo_id IN (SELECT id FROM rollo WHERE fechahora >= '%s' AND fechahora < '%s') AND parte_de_produccion_id IS NULL
    """ % (fechasqlini, fechasqlfin))
    for articulo in articulos_de_rollos_sin_parte_de_produccion_y_entre_fechas:
        rollos.append(articulo.rollo)
    return rollos

def buscar_rollos_salidos(fecha_ini, fecha_fin):
    """
    Devuelve una lista de rollos que han salido entre 
    las dos fechas recbidas (ambas incluidas).
    """
    rollos = []
    albaranes = pclases.AlbaranSalida.select(pclases.AND(pclases.AlbaranSalida.q.fecha >= fecha_ini, 
                                                         pclases.AlbaranSalida.q.fecha <= fecha_fin))
    for albaran in albaranes:
        for articulo in albaran.articulos:
            if articulo.es_rollo():
                rollos.append(articulo.rollo)
    return rollos

def main():
    """
    Devuelve un diccionario con los listados de rollos 
    en existencias, fabricados y salidos en cada periodo.
    """
    ini_enero = mx.DateTime.DateTimeFrom(day = 1, month = 1, year = 2006)  # @UnusedVariable
    fin_enero = mx.DateTime.DateTimeFrom(day = -1, month = 1, year = 2006)
    ini_febrero = mx.DateTime.DateTimeFrom(day = 1, month = 2, year = 2006)
    fin_febrero = mx.DateTime.DateTimeFrom(day = -1, month = 2, year = 2006)
    rollos_existencias_enero = buscar_rollos_existencias(fin_enero)
    print "EXISTENCIAS AL 31 DE ENERO: %s" % (utils.int2str(len(rollos_existencias_enero)))
    rollos_fabricados_febrero = buscar_rollos_fabricados(ini_febrero, fin_febrero)
    print "FABRICADO EN FEBRERO: %s" % (utils.int2str(len(rollos_fabricados_febrero)))
    rollos_salidos_febrero = buscar_rollos_salidos(ini_febrero, fin_febrero)
    print "ROLLOS SALIDOS EN FEBRERO: %s" % (utils.int2str(len(rollos_salidos_febrero)))
    len_existencias_teoria_febrero = len(rollos_existencias_enero) + len(rollos_fabricados_febrero) - len(rollos_salidos_febrero)
    existencias_teoria_febrero = rollos_existencias_enero + rollos_fabricados_febrero
    for rollo in rollos_salidos_febrero:
        try:
            existencias_teoria_febrero.remove(rollo)
        except ValueError:
            print "Busted! El rollo ID %d salió en febrero pero no estaba en enero ni se fabricó en febrero." % (rollo.id)
        if rollo in existencias_teoria_febrero:
            print "Busted! El rollo ID %d sigue estando en las existencias de febrero." % (rollo.id)
    print "TOTAL TEÓRICO AL 28 DE FEBRERO: %s [%s]" % (utils.int2str(len_existencias_teoria_febrero), 
                                                       utils.int2str(len(existencias_teoria_febrero)))
    rollos_existencias_febrero = buscar_rollos_existencias(fin_febrero)
    print "TOTAL BD AL 28 DE FEBRERO: %s" % (utils.int2str(len(rollos_existencias_febrero)))
    return {'existencias enero': rollos_existencias_enero, 
            'fabricados febrero': rollos_fabricados_febrero, 
            'salidos febrero': rollos_salidos_febrero, 
            'existencias teoria febrero': existencias_teoria_febrero, 
            'existencias febrero': rollos_existencias_febrero}

if __name__ == "__main__":
    dic_rollos = main()
    
