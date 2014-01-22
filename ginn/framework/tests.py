#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado,                   #
#                          (pacoqueen@users.sourceforge.net)                  #
#                                                                             #
# This file is part of GeotexInn.                                             #
#                                                                             #
# GeotexInn is free software; you can redistribute it and/or modify           #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation; either version 2 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# GeotexInn is distributed in the hope that it will be useful,                #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with GeotexInn; if not, write to the Free Software                    #
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA  #
###############################################################################
# NOTA: OJO: Usa decoradores para cronometrar. Necesita python 2.4 o superior.
###############################################################################
# TODO: Hay que optimizar muchos de los test, comen memoria y son lentos 
#       cosita mala.
#       Añadir un test que compruebe que las facturas tienen vencimientos y 
#       coinciden con el total de la factura (de compra y de venta).
#       Añadir también uno que compruebe que no hay facturas de abono sin 
#       abonos.
#       Añadir otro que compruebe que las fechas de las facturas ordenadas 
#       por número de factura según su serie (contador) son consecutivas.
###############################################################################

from framework import pclases
import mx.DateTime, time, sys
from formularios import utils

"""
Test de coherencia de datos para realizar periódicamente.
NO es un módulo unittest de pruebas unitarias. Es simplemente 
una forma de automatizar en un script las pruebas "de salud" 
que realizaba periódicamente a manopla.
"""

if sys.version_info[1] <= 3:
    print "WARNING: Necesitas python 2.4 para usar el decorador que mide el tiempo de ejecución de las pruebas. Comenta el código correspondiente si no lo está ya."

def sec2str(t):
    """
    Devuelve una cadena con el tiempo t en horas, minutos y segundos.
    """
    if isinstance(t, float):
        t = int(round(t, 0))
    segundos = t % 60
    t = t / 60
    minutos = t % 60
    horas = t / 60
    return "%s horas, %s minutos y %s segundos." % (horas, minutos, segundos)

def crono(funcion):
    """
    Decorador para medir el tiempo que tarda en ejecutarse una función.
    """
    def funcion_decorada(*args, **kw):
        antes = time.time()
        res = funcion(*args, **kw)
        tiempo = time.time() - antes
        print 'Tiempo en ejecutarse "%s": %s' % (funcion.func_name, sec2str(tiempo))
        return res
    return funcion_decorada

@crono      # XXX Comentar si python 2.3
def comprobar_fibra_consumida_antes_de_fecha_de_fabricacion(
        report_mode = False, 
        ignore_list = []):
    """
    Si report_mode == True, acaba el test completo. Si no, sale en cuanto encuentre 
    el primero de los artículos erróneos.
    Comprueba que toda la fibra consumida se ha hecho antes de su fecha 
    de fabricación. Para ello:
    1.- Busca todas las balas con partidaDeCarga != None.
    2.- Para cada bala compara si la propiedad fecha_fabricación es 
        menor o igual que la fecha de su partida de carga.
    3.- Si alguna no lo es, devuelve False e imprime por salida de 
        errores el ID de la bala e información relativa.
    Devuelve False si el alguna no se cumple esa condición.
    """
    res = True
    articulos = pclases.Articulo.select(
            pclases.AND(pclases.Bala.q.partidaCargaID != None, 
                        pclases.Articulo.q.balaID == pclases.Bala.q.id), 
            orderBy = "-id")
        # Empiezo por las últimas por si alguna falla, que falle cuanto antes (las más antiguas se 
        # suponen que ya han sido comprobadas anteriormente y es menos probable que sean erróneas).
    for a in articulos:
        if a in ignore_list:
            continue
        fechafab = a.fecha_fabricacion
        pc = a.bala.partidaCarga
        fechaconsumo = pc.fecha
        if fechafab > fechaconsumo:
            print >> sys.stderr, "La bala ID %d tiene como fecha de fabricación %s y como fecha de consumo %s." % (a.bala.id, 
                                    utils.str_fechahora(fechafab), utils.str_fechahora(fechaconsumo))
            res = False
            if not report_mode:
                break
    return res

@crono
def comprobar_articulos_vendidos_antes_de_fecha_de_fabricacion(
        report_mode = False, 
        ignore_list = []):
    """
    Para cada artículo vendido comprueba que su fecha de fabricación es anterior 
    a la fecha de salida en albaranes.
    """
    res = True
    articulos = pclases.Articulo.select(pclases.Articulo.q.albaranSalidaID != None, orderBy = "-id")
    for a in articulos:
        if a in ignore_list:
            continue
        ff = a.fecha_fabricacion
        fv = a.albaranSalida.fecha + mx.DateTime.oneDay # Para comparar fechahora con fecha hay que sumarle un día a la fecha.
        if ff >= fv:
            print >> sys.stderr, "El artículo ID %d tiene como fecha de fabricación %s y como fecha de salida _efectiva_ de almacén %s (albarán %s, %s)." % (
                a.id, 
                utils.str_fechahora(ff), 
                utils.str_fecha(fv), 
                a.albaranSalida.numalbaran, 
                utils.str_fecha(a.albaranSalida.fecha))
            res = False
            if not report_mode:
                break
    return res

@crono
def comprobar_fibra_en_partida_de_carga_y_albaran_de_salida_a_la_vez(
        report_mode = False, 
        ignore_list = []):
    """
    Para cada artículo en partida de carga comprueba que si está en un albarán, éste 
    sea un albarán interno. En otro caso devuelve False.
    """
    res = True
    articulos = pclases.Articulo.select(pclases.AND(pclases.Articulo.q.albaranSalidaID != None, 
                                                    pclases.Articulo.q.balaID == pclases.Bala.q.id, 
                                                    pclases.Bala.q.partidaCargaID != None), 
                                        orderBy = "-id")
    for a in articulos:
        if a in ignore_list:
            continue
        alb = a.albaranSalida
        if not alb.es_interno():
            print >> sys.stderr, "La bala ID %d (%s) está en la partida de carga ID %d (%s) y el albarán de salida (no interno) ID %d (%s)." % (
                a.bala.id, a.bala.codigo, a.bala.partidaCarga.id, a.bala.partidaCarga.codigo, a.albaranSalida.id, a.albaranSalida.numalbaran)
            res = False
            if not report_mode:
                break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_articulos_con_albaran_salida_y_albaran_abono(
        report_mode = False, 
        ignore_list = []):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale al encontrar 
    el primero de los objetos que incumple el criterio.
    Comprueba que ningún artículo que esté devuelto en un albarán de entrada de abono se 
    encuentre relacionado con el mismo albarán de salida del que se supone que se ha 
    desvinculado al abonarlo.
    En resumen, se trata de llamar a check_abono en cada artículo.
    """
    res = True
    articulos = pclases.Articulo.select(orderBy = "-id")
    for a in articulos:
        if a in ignore_list:
            continue
        if not a.check_abono():
            print >> sys.stderr, "Artículo ID %d no está correctamente abonado." % (a.id)
            res = False
            if not report_mode:
                break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_articulos_con_enlaces_incorrectos(report_mode = False):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale al encontrar 
    el primero de los objetos que incumple el criterio.
    Comprueba que cada artículo está relacionado con uno y solo uno de los objetos bala, 
    bala_cable, rollo, rollo_defectuoso o bigbag.
    También comprueba que todo rollo, bala, etc. tenga relación con un artículo.
    """
    res = True
        # Cambio de estrategia. Evito recorrer los artículos que 
        # sé seguro que están bien:
    A = pclases.Articulo
    from pclases import AND, NOT, OR
    rs = AND(A.q.rolloID != None, A.q.rolloDefectuosoID == None, A.q.balaID == None, A.q.balaCableID == None, A.q.bigbagID == None)
    rsd = AND(A.q.rolloID == None, A.q.rolloDefectuosoID != None, A.q.balaID == None, A.q.balaCableID == None, A.q.bigbagID == None)
    bs = AND(A.q.rolloID == None, A.q.rolloDefectuosoID == None, A.q.balaID != None, A.q.balaCableID == None, A.q.bigbagID == None)
    bsc = AND(A.q.rolloID == None, A.q.rolloDefectuosoID == None, A.q.balaID == None, A.q.balaCableID != None, A.q.bigbagID == None)
    bbs = AND(A.q.rolloID == None, A.q.rolloDefectuosoID == None, A.q.balaID == None, A.q.balaCableID == None, A.q.bigbagID != None)
    articulos_malos = A.select(NOT(OR(rs, rsd, bs, bsc, bbs)))
    
    if A.select(rs).count() != pclases.Rollo.select().count():
        print >> sys.stderr, "Número de rollos (%d) y artículos rollo (%d) no coincide. Dado que no se pueden violar claves ajenas -integridad referencial asegurada por el motor de la BD-, lo más probable es que haya un registro rollo relacionado con dos o más artículos." % (
            A.select(rs).count(), pclases.Rollo.select().count())
        chungaletas = A._queryAll("""SELECT rollo_id 
                                                FROM articulo, rollo 
                                                WHERE rollo_id = rollo.id 
                                                GROUP BY rollo_id 
                                                HAVING COUNT(rollo_id) > 1;""")
        print >> sys.stderr, "IDs de rollo apuntados por más de un artículo: %s" % ", ".join([str(fila[0]) for fila in chungaletas])
        if not report_mode:
            return False
    if A.select(rsd).count() != pclases.RolloDefectuoso.select().count():
        print >> sys.stderr, "Número de rollos defectuosos (%d) y artículos rollo defectuoso (%d) no coincide." % (
            A.select(rsd).count(), pclases.RolloDefectuoso.select().count())
        chungaletas = A._queryAll("""SELECT rollo_defectuoso_id 
                                                FROM articulo, rollo_defectuoso 
                                                WHERE rollo_defectuoso_id = rollo_defectuoso.id 
                                                GROUP BY rollo_defectuoso_id 
                                                HAVING COUNT(rollo_defectuoso_id) > 1;""")
        print >> sys.stderr, "IDs de rollo_defectuoso apuntados por más de un artículo: %s" % ", ".join([str(fila[0]) for fila in chungaletas])
        if not report_mode:
            return False
    if A.select(bs).count() != pclases.Bala.select().count():
        print >> sys.stderr, "Número de balas (%d) y artículos bala (%d) no coincide." % (
            A.select(bs).count(), pclases.Bala.select().count())
        chungaletas = A._queryAll("""SELECT bala_id 
                                                FROM articulo, bala 
                                                WHERE bala_id = bala.id 
                                                GROUP BY bala_id 
                                                HAVING COUNT(bala_id) > 1;""")
        print >> sys.stderr, "IDs de bala apuntados por más de un artículo: %s" % ", ".join([str(fila[0]) for fila in chungaletas])
        if not report_mode:
            return False
    if A.select(bsc).count() != pclases.BalaCable.select().count():
        print >> sys.stderr, "Número de balas de cable (%d) y artículos bala de cable (%d) no coincide." % (
            A.select(bsc).count(), pclases.BalaCable.select().count())
        chungaletas = A._queryAll("""SELECT bala_cable_id 
                                                FROM articulo, bala_cable 
                                                WHERE bala_cable_id = bala_cable.id 
                                                GROUP BY bala_cable_id 
                                                HAVING COUNT(bala_cable_id) > 1;""")
        print >> sys.stderr, "IDs de bala_cable apuntados por más de un artículo: %s" % ", ".join([str(fila[0]) for fila in chungaletas])
        if not report_mode:
            return False
    if A.select(bbs).count() != pclases.Bigbag.select().count():
        print >> sys.stderr, "Número de bigbags (%d) y artículos bigbag (%d) no coincide." % (
            A.select(bbs).count(), pclases.Bigbag.select().count())
        chungaletas = A._queryAll("""SELECT bigbag_id 
                                                FROM articulo, bigbag 
                                                WHERE bigbag_id = bigbag.id 
                                                GROUP BY bigbag_id 
                                                HAVING COUNT(bigbag_id) > 1;""")
        print >> sys.stderr, "IDs de bigbag apuntados por más de un artículo: %s" % ", ".join([str(fila[0]) for fila in chungaletas])
        if not report_mode:
            return False

    #import gc     # Forzando el recolector de basura en cada iteración no come tanta memoria, pero tarda muchísimo.
    #articulos = pclases.Articulo.select(orderBy = "-id")
    for a in articulos_malos:
        relaciones = 0
        for atributo in ("balaCable", "bala", "rollo", "rolloDefectuoso", "bigbag"):
            if getattr(a, atributo) != None:
                relaciones += 1
        if relaciones != 1:
            print >> sys.stderr, "El artículo ID %d tiene %d relaciones con bala, balaCable, rollo, rolloDefectuoso o bigbag." % (a.id, relaciones)
            res = False
    #    del a
    #    gc.collect()
        if not res and not report_mode:
            break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_cantidades_albaran(report_mode = False):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar el primero de los objetos que incumple el criterio.
    Comprueba que las cantidades de las líneas de venta de los albaranes 
    coincide con las cantidades de los artículos que incuye. Ignora las líneas 
    de productos de compra y productos especiales, que no se venden por 
    artículos individuales.
    OJO: Puede dar un falso positivo si el último albarán no se ha terminado 
    de hacer aún.
    """
    res = True
    albaranes = pclases.AlbaranSalida.select(orderBy = "-id")
    for alb in albaranes:
        pvs = {}
        for ldv in alb.lineasDeVenta:
            pv = ldv.productoVenta
            if pv != None and (pv.es_bala() or pv.es_bala_cable() or pv.es_bigbag() or pv.es_rollo()):
                if pv not in pvs:
                    pvs[pv] = [ldv.cantidad, 0.0]
                else:
                    pvs[pv][0] += ldv.cantidad
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
        for pv in pvs:
            if round(pvs[pv][0], 2) != round(pvs[pv][1], 2):
                print >> sys.stderr, "El albarán ID %d (%s) tiene como cantidad total de %s, %s en líneas de venta y %s en artículos." % (
                    alb.id, alb.numalbaran, pv.descripcion, utils.float2str(pvs[pv][0]), utils.float2str(pvs[pv][1]))
                res = False
        if not res and not report_mode:
            break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_partes_solapados(report_mode = False, 
                               ignore_list = []):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale al encontrar 
    el primero de los objetos que incumple el criterio.
    Comprueba que los partes de la misma línea no se solapan entre sí.
    """
    res = True
    pdps = pclases.ParteDeProduccion.select(orderBy = "-id")
    for pdp in pdps:
        if pdp in ignore_list:
            continue
        if pdp.se_solapa(desbloquear_si_mal = False):
            print >> sys.stderr, "El parte ID %d (%s a %s) se solapa con otro de su misma línea." % (
                pdp.id, utils.str_fechahora(pdp.fechahorainicio), utils.str_fechahora(pdp.fechahorafin))
            res = False
            if not report_mode:
                break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_huecos_partes(report_mode = False, 
                            ignore_list = []):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale al encontrar 
    el primero de los objetos que incumple el criterio.
    Comprueba que en dos partes consecutivos de la misma línea la fechahora de finalización 
    del primero es igual a la fechahora de inicio del siguiente parte.
    """
    res = True
    ultima_fechahora_fibra = None
    ultima_fechahora_gtx = None
    for pdp in pclases.ParteDeProduccion.select(orderBy = "fechahorainicio"):
        if pdp in ignore_list:
            continue
        if pdp.es_de_fibra():
            if ultima_fechahora_fibra:
                no_hueco = ultima_fechahora_fibra == pdp.fechahorainicio
                if no_hueco == False:
                    res = False
                    print >> sys.stderr, "La hora de inicio del parte de fibra ID %d (%s) no concuerda con la hora de finalización del parte inmediatamente anterior (%s)." % (pdp.id, utils.str_fechahora(pdp.fechahorainicio), utils.str_fechahora(ultima_fechahora_fibra))
                    if not report_mode:
                        break
            ultima_fechahora_fibra = pdp.fechahorafin
        elif pdp.es_de_geotextiles():
            if ultima_fechahora_gtx:
                # La línea de geotextiles se cierra los fines de semana y no suele tener turno de noche, así que compruebo 
                # que la última fecha no sea de un viernes ni que la hora sea las 22:00
                no_hueco = (ultima_fechahora_gtx == pdp.fechahorainicio or 
                            ultima_fechahora_gtx.day_of_week == 4 
                            or ultima_fechahora_gtx.hour == 22)     # Puede dar falsos negativos en partes de menos de 59 minutos que 
                                                                    # empiecen a las 10 y pico, partes nocturnos (hay pocos), etc. pero 
                                                                    # lo prefiero a falsos positivos
                if no_hueco == False:
                    res = False
                    print >> sys.stderr, "La hora de inicio del parte de geotextiles ID %d (%s) no concuerda con la hora de finalización del parte inmediatamente anterior (%s)." % (pdp.id, utils.str_fechahora(pdp.fechahorainicio), ultima_fechahora_gtx)
                    if not report_mode:
                        break
            ultima_fechahora_gtx = pdp.fechahorafin
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_coherencia_fecha_y_fechahoras_partes(report_mode = False, 
                                                   ignore_list = []):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar el primero de los objetos que incumple el criterio.
    Comprueba que los campos de fecha, horainicio y horafin coinciden con 
    fechahorainicio y fechahorafin en cada parte.
    """
    res = True
    pdps = pclases.ParteDeProduccion.select(orderBy = "-id")
    for pdp in pdps:
        if pdp in ignore_list:
            continue
        if not pdp._comprobar_coherencia_campos_fechahora():
            print >> sys.stderr, "El parte de producción ID %d tiene valores distintos para fecha, horainicio, horafin y fechahoras: %s: %s -> %s; %s -> %s." % (pdp.id, utils.str_fecha(pdp.fecha), utils.str_hora_corta(pdp.horainicio), utils.str_hora_corta(pdp.horafin), 
                     utils.str_fechahora(pdp.fechahorainicio), utils.str_fechahora(pdp.fechahorafin))
            res = False
            if not report_mode:
                break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_duracion_incidencias(report_mode = False, 
                                   ignore_list = []):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar el primero de los objetos que incumple el criterio.
    Comprueba que el sumatorio de la duración de las incidencias de un parte 
    no supera la duración total del mismo.
    """
    res = True
    for pdp in pclases.ParteDeProduccion.select(orderBy = "-id"):
        if pdp in ignore_list:
            continue
        dur_incidencias = sum([i.get_duracion() for i in pdp.incidencias], mx.DateTime.DateTimeDelta(0))
        if dur_incidencias > pdp.get_duracion():
            print >> sys.stderr, "El parte ID %d (%s [%s]) contiene incidencias que superan su duración total: %s > %s." % (pdp.id, 
                utils.str_fechahora(pdp.fechahorainicio), (pdp.es_de_fibra() and "FIB") or (pdp.es_de_geotextiles() and "GTX") or "?", 
                utils.str_hora(dur_incidencias), utils.str_hora(pdp.get_duracion()))
            res = False
            if not report_mode:
                break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_horas_trabajadas_en_partes(report_mode = False, 
                                         ignore_list = []):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar el primero de los objetos que incumple el criterio.
    Comprueba que ningún empleado tiene más horas de trabajo que la duración 
    del parte de producción.
    """
    res = True
    for pdp in pclases.ParteDeProduccion.select(orderBy = "-id"):
        if pdp in ignore_list:
            continue
        pdp_duracion = pdp.get_duracion()
        for ht in pdp.horasTrabajadas:
            if ht.horas > pdp_duracion:
                print >> sys.stderr, "El parte ID %d (%s) tiene un empleado con más horas trabajadas (%s) que su duración (%s)." % (
                                pdp.id, utils.str_fecha(pdp.fecha), utils.str_hora(ht.horas), utils.str_hora(pdp_duracion))
                res = False
        if not res and not report_mode:
            break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_codificacion_articulos(report_mode = False):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar el primero de los objetos que incumple el criterio.
    Comprueba que los códigos de todos los productos coincide con la 
    numeración de su rollo, rollo_defectuoso, bala, bala_cable o bigbag.
    """
    res = True
    # Optimizando, opt-optimizando:
    articulosr = pclases.Articulo.select("""rollo_id IN 
      (SELECT id 
       FROM rollo 
       WHERE CAST(TRIM(TRAILING 'D' FROM TRIM(LEADING 'R' FROM codigo)) AS INT)
          <> ABS(numrollo)) """)
    # OJO: Corro el riesgo de dar un R100D con numrollo 100 por válido (cuando debería tener un numrollo -100); pero como hay un 
    # constraint en la BD para no repetir numrollo, implicaría que hay un R100 con numrollo -100, por lo que en el fondo da lo mismo.
    # De cualquier forma, se va a comprobar en el bucle for de abajo.
    articulosrd = pclases.Articulo.select("""rollo_defectuoso_id IN 
      (SELECT id 
       FROM rollo_defectuoso 
       WHERE CAST(TRIM(LEADING 'X' FROM codigo) AS INT) <> ABS(numrollo)) """)
    articulosb = pclases.Articulo.select("""bala_id IN 
      (SELECT id 
       FROM bala 
       WHERE CAST(TRIM(TRAILING 'D' FROM TRIM(LEADING 'B' FROM codigo)) AS INT) 
          <> ABS(numbala)) """)
    articulosbc = pclases.Articulo.select("""bala_cable_id IN 
      (SELECT id 
       FROM bala_cable 
       WHERE CAST(TRIM(LEADING 'Z' FROM codigo) AS INT) <> ABS(numbala)) """)
    articulosbb = pclases.Articulo.select("""bigbag_id IN 
      (SELECT id 
       FROM bigbag 
       WHERE CAST(TRIM(LEADING 'C' FROM codigo) AS INT) <> ABS(numbigbag)) """)
    articulos = tuple(articulosr) + tuple(articulosrd) + tuple(articulosb) + tuple(articulosbc) + tuple(articulosbb)
    # articulos = pclases.Articulo.select(orderBy = "-id")
    for a in articulos:
        if a.es_rollo():
            codigo = a.rollo.codigo
            numrollo = a.rollo.numrollo
            if numrollo < 0:
                rescode = codigo.replace("R", "").replace("D", "") == str(-1 * numrollo)
            else:
                rescode = codigo.replace("R", "") == str(numrollo)
        elif a.es_rollo_defectuoso():
            codigo = a.rolloDefectuoso.codigo
            numrollo = a.rolloDefectuoso.numrollo
            rescode = codigo.replace("X", "") == str(numrollo)
        elif a.es_bala():
            codigo = a.bala.codigo
            numbala = a.bala.numbala
            if numbala < 0:
                rescode = codigo.replace("B", "").replace("D", "") == str(-1 * numbala)
            else:
                rescode = codigo.replace("B", "") == str(numbala)
        elif a.es_bala_cable():
            codigo = a.balaCable.codigo
            numbala = a.balaCable.numbala
            rescode = codigo.replace("Z", "") == str(numbala)
        elif a.es_bigbag():
            codigo = a.bigbag.codigo
            numbigbag = a.bigbag.numbigbag
            rescode = int(codigo.replace("C", "")) == numbigbag
        else:
            print >> sys.stderr, "El artículo ID %d no es bala [cable], rollo [defectuoso] ni bigbag." % (a.id)
            continue
        if not rescode:
            print >> sys.stderr, "El código (%s) del artículo ID %d no coincide con la numeración de la bala [cable], rollo [defectuoso] o bigbag." % (a.codigo, a.id)
            res = False
            if not report_mode:
                break
        del(a)  # A ver si consigo que el GC me libere la memoria pillada por el artículo. Ya no se usa más. Debería hacerlo.
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_existencias_silos(report_mode = False):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar el primero de los objetos que incumple el criterio.
    Comprueba que las cantidades de granza de los silos coincide con las 
    existencias de los productos contenidos. Se usa una precisión de 1 único 
    decimal.
    """
    res = True
    pvs = {}
    for silo in pclases.Silo.select():
        ocupacion = silo.get_ocupacion()
        for pv in ocupacion:
            if pv not in pvs:
                pvs[pv] = ocupacion[pv]
            else:
                pvs[pv] += ocupacion[pv]
    for pv in pvs:
        if round(pvs[pv], 1) != round(pv.existencias, 1):
            print >> sys.stderr, "El producto ID %d (%s) tiene %s existencias, pero en silos hay almacenado un total de %s." % (pv.id, 
                                pv.descripcion, utils.float2str(pv.existencias), utils.float2str(pvs[pv]))
            res = False
            if not report_mode:
                break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_producciones_estandar(report_mode = False, 
                                    ignore_list = []):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar el primero de los objetos que incumple el criterio.
    Comprueba que las producciones estándar de los partes coincide con la de 
    los productos fabricados.
    """
    res = True
    pdps = pclases.ParteDeProduccion.select(orderBy = "-id")
    for pdp in pdps:
        if pdp in ignore_list:
            continue
        pv = pdp.get_producto_fabricado()
        if pv != None and pv.prodestandar != pdp.prodestandar:
            print >> sys.stderr, "El parte de producción ID %d (%s) tiene una producción estándar (%s) distinta a la del producto fabricado %s (%s)." % (pdp.id, utils.str_fecha(pdp.fecha), utils.float2str(pdp.prodestandar), pv.descripcion, utils.float2str(pv.prodestandar))
            res = False
            if not report_mode:
                break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_clientes_proveedores_en_pedidos_albaranes_facturas(
        report_mode = False, 
        ignore_list = []):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale al
    encontrar el primero de los objetos que incumple el criterio.
    Comprueba que todos los pedidos de venta, albaranes de salida y facturas de
    venta tengan un cliente; y que todos los pedidos de compra, albaranes de 
    entrada y facturas de compra tengan un proveedor.
    Si algún pedido, factura o albarán está en «ignore_list» se pasa por 
    alto.
    """
    res = True
    peds_venta = pclases.PedidoVenta.select(
        pclases.PedidoVenta.q.clienteID == None)
    albs_salida = pclases.AlbaranSalida.select(
        pclases.AlbaranSalida.q.clienteID == None)
    facts_venta = pclases.FacturaVenta.select(
        pclases.FacturaVenta.q.clienteID == None)
    peds_compra = pclases.PedidoCompra.select(
        pclases.PedidoCompra.q.proveedorID == None)
    albs_entrada = pclases.AlbaranEntrada.select(
        pclases.AlbaranEntrada.q.proveedorID == None)
    facts_compra = pclases.FacturaCompra.select(
        pclases.FacturaCompra.q.proveedorID == None)
    for p in peds_venta:
        if p in ignore_list:
            continue
        print >> sys.stderr, "El pedido de venta ID %d (%s) no tiene cliente." % (p.id, p.numpedido)
        res = False
        if not report_mode:
            break
    for a in albs_salida:
        if a in ignore_list:
            continue
        print >> sys.stderr, "El albarán de salida ID %d (%s) no tiene cliente." % (a.id, a.numalbaran)
        res = False
        if not report_mode:
            break
    for f in facts_venta:
        if a in ignore_list:
            continue
        print >> sys.stderr, "La factura de venta ID %d (%s) no tiene cliente." % (f.id, f.numfactura)
        res = False
        if not report_mode:
            break
    for p in peds_compra:
        if p in ignore_list:
            continue
        print >> sys.stderr, "El pedido de compra ID %d (%s) no tiene proveedor." % (p.id, p.numpedido)
        res = False
        if not report_mode:
            break
    for a in albs_entrada:
        if a in ignore_list:
            continue
        print >> sys.stderr, "El albarán de entrada ID %d (%s) no tiene proveedor." % (a.id, a.numalbaran)
        res = False
        if not report_mode:
            break
    for f in facts_compra:
        if f in ignore_list:
            continue
        print >> sys.stderr, "La factura de compra ID %d (%s) no tiene proveedor." % (f.id, f.numfactura)
        res = False
        if not report_mode:
            break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_albaranes_internos(report_mode = False, 
                                 ignore_list = []):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar el primero de los objetos que incumple el criterio.
    Comprueba que todos los albaranes internos de consumo contienen únicamente 
    productos de compra o balas de fibra.
    """
    res = True
    albs = pclases.AlbaranSalida.select(" es_interno(albaran_salida.id) ")
    for alb in albs:
        if alb in ignore_list:
            continue
        for ldv in alb.lineasDeVenta:
            res = res and (ldv.productoCompra != None or ldv.productoVenta.es_bala())
        if not res:
            print >> sys.stderr, "El albarán interno ID %d (%s) contiene líneas que no son de fibra ni productos de consumo." % (alb.id, alb.numalbaran)
            if not report_mode:
                break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_numeracion_articulos(report_mode = False, 
                                   ignore_list = []):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar el primero de los objetos que incumple el criterio.
    Comprueba que la numeración de las balas, balas de cable, bigbags, rollos 
    y rollos defectuosos es consecutiva. Ignora los códigos duplicados 
    (num[bala|bigbag|rollo] < 0) porque evidentemente son casos puntuales y no 
    son consecutivos.
    «ignore_list» es una lista de balas, rollos, etc. que se ignorarán.
    """
    res = True
    bs = pclases.Bala._queryAll(
      "SELECT id, numbala FROM bala WHERE numbala > 0 ORDER BY numbala;")
    bcs = pclases.BalaCable._queryAll(
      "SELECT id, numbala FROM bala_cable WHERE numbala > 0 ORDER BY numbala;")
    rs = pclases.Rollo._queryAll(
      "SELECT id, numrollo FROM rollo WHERE numrollo > 0 ORDER BY numrollo;")
    rds = pclases.RolloDefectuoso._queryAll(
      """SELECT id, numrollo 
         FROM rollo_defectuoso 
         WHERE numrollo > 0 
         ORDER BY numrollo;""")
    bbs = pclases.Bigbag._queryAll(
      "SELECT id,numbigbag FROM bigbag WHERE numbigbag > 0 ORDER BY numbigbag;")
    _ignore_list = {"Bala": [], 
                    "BalaCable": [], 
                    "Rollo": [], 
                    "RolloDefectuoso": [], 
                    "Bigbag": []}
    for a in ignore_list:
        if a.es_bala():
            _ignore_list["Bala"].append(a.balaID)
        elif a.es_bala_cable():
            _ignore_list["BalaCable"].append(a.balaCableID)
        elif a.es_bigbag():
            _ignore_list["Bigbag"].append(a.bigbagID)
        elif a.es_rollo():
            _ignore_list["Rollo"].append(a.rolloID)
        elif a.es_rollo_defectuoso():
            _ignore_list["RolloDefectuoso"].append(a.rolloDefectuosoID)
    for conjunto, tipo in ((bs, "Bala"), 
                           (bcs, "BalaCable"), 
                           (rs, "Rollo"), 
                           (rds, "RolloDefectuoso"), 
                           (bbs, "Bigbag")):
        last_num = None
        for ide, num in conjunto:
            if ide in _ignore_list[tipo]:
                continue
            if last_num != None and num - last_num != 1:
                print >> sys.stderr, "%s ID %d (número %d) no es consecutivo con el anterior (%d)." % (tipo, ide, num, last_num)
                res = False
                if not report_mode:
                    break
            last_num = num
        if not res and not report_mode:
            break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_balas_en_albaranes_internos_sin_partidacarga(
        report_mode = False, 
        fecha_filtro_anteriores_a = None):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar el primero de los objetos que incumple el criterio.
    Comprueba que todas los artículos de los albaranes internos de consumo 
    sean balas y estén relacionadas con una partida de carga.
    Si fecha_filtro_anteriores_a != None, no comprueba las partidas de carga 
    anteriores a esa fecha.
    """
    res = True
    albs = pclases.AlbaranSalida.select(" es_interno(albaran_salida.id) ")  
                    # Es un poco redundante, pero me valdrá para 
                    # comprobar que el procedimiento almacenado de la BD 
                    # funciona como se espera. "es_interno" devuelve False si 
                    # alguna de las balas no tiene PC (que es justamente lo que 
                    # se supone que iba a detectar aquí).
    for alb in albs:
        for a in alb.articulos:
            if a.bala == None or a.bala.partidaCarga == None:
                print >> sys.stderr, "El artículo ID %d del albarán interno ID %d (%s) no es una bala o no tiene partida de carga relacionada." % (a.id, alb.id, alb.numalbaran)
                res = False
                if not report_mode:
                    break
        if not res and not report_mode:
            break
    # Como esto de aquí arriba nunca va a fallar, hago otra comprobación 
    # adicional más acertada: Compruebo que todas las balas de las partidas 
    # de carga tengan albarán y que éstos cumplan "es_interno". Equivaldría 
    # a alb.get_balas_sin_albaran_interno(), cabría hacer una comprobación 
    # adicional y verificar que las balas detectadas aquí coinciden con las 
    # que devuelve el método. Pero no creo que merezca la pena.
    if not fecha_filtro_anteriores_a:
        pcs = pclases.PartidaCarga.select(orderBy = "-id")
    else:
        pcs = pclases.PartidaCarga.select(
            pclases.PartidaCarga.q.fecha >= fecha_filtro_anteriores_a, 
            orderBy = "-id")
    # print pcs.count(), pclases.PartidaCarga.select().count()
    for pc in pcs:
        for bala in pc.balas:
            if bala.albaranSalida == None:
                print >> sys.stderr, "La bala ID %d (artículo ID %d, código %s) está en la partida de carga ID %d (código %s) y no tiene albarán interno relacionado." % (
                    bala.id, bala.articulo.id, bala.codigo, pc.id, pc.codigo)
                res = False
                if not report_mode:
                    break
            elif not bala.albaranSalida.es_interno():
                print >> sys.stderr, "La bala ID %d (artículo ID %d, código %s) está en la partida de carga ID %d (código %s) y tiene albarán interno relacionado ID %d (%s) pero no es interno." % (
                    bala.id, bala.articulo.id, bala.codigo, pc.id, pc.codigo, bala.albaranSalida.id, bala.albaranSalida.numalbaran)
                res = False
                if not report_mode:
                    break
        if not res and not report_mode:
            break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_fechahora_de_articulos(report_mode = False):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar el primero de los objetos que incumple el criterio.
    Comprueba que todos los artículos rollo, rolloDefectuoso, Bala y Bigbag 
    tienen su "fechahora" dentro de las fechahora de sus partes de producción. 
    Se basa en los campos fechahora de los partes, por lo que es importante 
    que el test de coherencia de fechahora<->fecha+hora de ParteDeProduccion 
    se haya superado con éxito.
    """
    res = True
    PDP = pclases.ParteDeProduccion
    B = pclases.Bala
    BB = pclases.Bigbag
    R = pclases.Rollo
    RD = pclases.RolloDefectuoso
    A = pclases.Articulo
    articulosr = A.select(pclases.AND(A.q.parteDeProduccionID == PDP.q.id, 
                                      A.q.rolloID == R.q.id, 
                                      pclases.OR(R.q.fechahora < PDP.q.fechahorainicio, 
                                                 R.q.fechahora > PDP.q.fechahorafin)))
    articulosrd = A.select(pclases.AND(A.q.parteDeProduccionID == PDP.q.id, 
                                       A.q.rolloDefectuosoID == RD.q.id, 
                                       pclases.OR(RD.q.fechahora < PDP.q.fechahorainicio, 
                                                  RD.q.fechahora > PDP.q.fechahorafin))) 
    articulosb = A.select(pclases.AND(A.q.parteDeProduccionID == PDP.q.id, 
                                      A.q.balaID == B.q.id, 
                                      pclases.OR(B.q.fechahora < PDP.q.fechahorainicio, 
                                                 B.q.fechahora > PDP.q.fechahorafin)))
    articulosbb = A.select(pclases.AND(A.q.parteDeProduccionID == PDP.q.id, 
                                       A.q.bigbagID == BB.q.id, 
                                       pclases.OR(BB.q.fechahora < PDP.q.fechahorainicio, 
                                                  BB.q.fechahora > PDP.q.fechahorafin)))
    for conjunto, tipo in ((articulosr, "rollo"), 
                           (articulosrd, "rolloDefectuoso"), 
                           (articulosb, "bala"), 
                           (articulosbb, "bigbag")):
        for a in conjunto:
            print >> sys.stderr, "Articulo ID %d (%s) tiene fechahora (%s) fuera del rango de su parte de producción ID %d (%s -> %s)." % (
              a.id, 
              tipo, 
              a.fechahora.strftime("%d-%m-%Y %H:%M:%S"), a.parteDeProduccion.id,
              a.parteDeProduccion.fechahorainicio.strftime("%d-%m-%Y %H:%M:%S"),
              a.parteDeProduccion.fechahorafin.strftime("%d-%m-%Y %H:%M:%S"))
            res = False
            if not report_mode:
                break
        if not res and not report_mode:
            break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_consumos_granza(report_mode = False, 
                              ignore_list = []):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar el primero de los objetos que incumple el criterio.
    Comprueba que el consumo de granza por cada parte de producción de fibra 
    sea de al menos un 90% del total de kilogramos de fibra fabricada.
    """
    res = True
    pdps = pclases.ParteDeProduccion.select(orderBy = "-id")
    for pdp in pdps:
        if pdp in ignore_list:
            continue
        if pdp.es_de_fibra():
            granza_consumida = pdp.get_granza_consumida()
            fibra_fabricada = sum([a.peso for a in pdp.articulos])
            if granza_consumida < fibra_fabricada * 0.9:
                print >> sys.stderr, "El parte de producción ID %d (%s) consumió menos del 90%% de granza (%s) respecto a la fibra fabricada(%s)." % (
                    pdp.id, utils.str_fecha(pdp.fecha), utils.float2str(granza_consumida), utils.float2str(fibra_fabricada))
                res = False
                if not report_mode:
                    break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_fecha_partidas_carga(report_mode = False):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar el primero de los objetos que incumple el criterio.
    Comprueba que la fecha de cada partida de carga es inferior a la fecha del 
    primero de los partes que la consume y mayor que la fecha de la última de 
    las balas que contiene.
    Adicionalmente envía mensaje a método test() de la partida de carga para 
    comprobar que las fechas de inicio y fin de consumo son coherentes entre 
    sí.
    """
    res = True
    pcs = pclases.PartidaCarga.select(orderBy = "-id")
    for pc in pcs:
        pc.test()   # TEST adicional. Comentar si consume demasiado tiempo de 
                    # computación y ya se ha probado con anterioridad.
        fecha_inicio_consumo = pc.get_fecha_inicio()
        fechas_balas = [b.articulo.fecha_fabricacion for b in pc.balas]
        fechas_balas.sort()
        ultima_fecha_bala = fechas_balas and fechas_balas[-1] or None
        if not fecha_inicio_consumo:
            print "Ignorando partida de carga ID %d (%s, %s) por no haberse empezado a consumir." % (
                pc.id, pc.codigo, utils.str_fechahora(pc.fecha))
            continue
        if not ultima_fecha_bala:
            print "Ignorando partida de carga ID %d (%s, %s) por no tener balas cargadas." % (
                pc.id, pc.codigo, utils.str_fechahora(pc.fecha))
            continue
        # Me aseguro de estar comparando fechas absolutas, sin horas:
        fecha_inicio_consumo = mx.DateTime.DateTimeFrom(fecha_inicio_consumo.year, fecha_inicio_consumo.month, fecha_inicio_consumo.day)
        ultima_fecha_bala = mx.DateTime.DateTimeFrom(ultima_fecha_bala.year, ultima_fecha_bala.month, ultima_fecha_bala.day)
        pc_fecha_absoluta = mx.DateTime.DateTimeFrom(pc.fecha.year, pc.fecha.month, pc.fecha.day)
        if not ultima_fecha_bala <= pc_fecha_absoluta <= fecha_inicio_consumo:
            print >> sys.stderr, "La partida de carga ID %d (%s, %s) se empezó a consumir (%s) antes de la última fecha de fabricación de las balas cargadas (%s) o tiene una fecha no comprendida entre éstas." % (
                pc.id, pc.codigo, utils.str_fecha(pc.fecha), utils.str_fecha(fecha_inicio_consumo), utils.str_fecha(ultima_fecha_bala))
            res = False
            if not report_mode:
                break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_caches(report_mode = False):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar el primero de los objetos que incumple el criterio.
    Recorre y comprueba las existencias y bultos de todos los cachés de la BD. 
    También avisa si encuentra un HistorialExistencias con fecha nula.
    Los HistorialExistenciasCompra no se chequean (al menos de momento) puesto 
    que hay muchos registros forzados, productos cuyas existencias ya no se 
    controlan por software, cantidades corregidas manualmente, falta de 
    albaranes de entrada y consumos... La mayoría de problemas se podrían 
    corregir, pero no es el momento. Al menos hasta que se estabilicen al 
    menos los consumos y se haga inventario.
    """
    res = True
    for he in pclases.HistorialExistencias.select(orderBy = "-id"):
        if not he.fecha:
            print >> sys.stderr, "Registro HistorialExistencias ID %d no tiene fecha. Debería eliminarse." % (he.id)
            res = False
            if not report_mode:
                break
        else:
            ok, bultos, cantidad = he.test()
            if not ok:
                print >> sys.stderr, "Registro HistorialExistencias ID %d incorrecto. Contiene %d bultos y %s existencias. Debería tener %d bultos y %s existencias. Activar pclases.DEBUG, volver a ejecutar he.test() y corregir si es necesario." % (
                    he.id, bultos, utils.float2str(cantidad), he.bultos, utils.float2str(he.cantidad))
                res = False
                if not report_mode:
                    break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_consumos_entre_fechas(report_mode = False, n = None):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar el primero de los objetos que incumple el criterio.
    Comprueba que en consumo de fibra en partidas de carga entre «n» fechas 
    al azar del último año coincide con la suma del consumo diario entre 
    esas mismas fechas. 
    «n» es un número aleatorio entre 1 y 3.
    Se podría hacer extensible al resto de productos, pero los más sensibles 
    a fallar son los de fibra, por aquello de tener las partidas de carga 
    entre medio y demás.
    """
    # TODO: Creo que no está muy fino este test. Repasar valores.
    import random
    res = True
    if n == None or not isinstance(n, int):
        n = random.randint(1, 3)
    pvfs = [pv for pv in pclases.ProductoVenta.select() if pv.es_bala()]
    for i in range(n):  # @UnusedVariable
        fecha0 = mx.DateTime.localtime() - mx.DateTime.oneDay * random.randint(0, 365)
        fecha1 = mx.DateTime.localtime() - mx.DateTime.oneDay * random.randint(0, 365)
        if fecha0 > fecha1:
            fecha0, fecha1 = fecha1, fecha0
        bultos = sum([pv.buscar_consumos_bultos(fecha0, fecha1) for pv in pvfs])
        cantidad = sum([pv.buscar_consumos_cantidad(fecha0, fecha1) for pv in pvfs])
        sumbultos = 0
        sumcantidad = 0.0
        fecha = fecha0
        while fecha < fecha1:
            sumbultos += sum([pv.buscar_consumos_bultos(fecha, fecha + mx.DateTime.oneDay) for pv in pvfs])
            sumcantidad += sum([pv.buscar_consumos_cantidad(fecha, fecha + mx.DateTime.oneDay) for pv in pvfs])
            fecha += mx.DateTime.oneDay
        if sumbultos != bultos or sumcantidad != cantidad:
            print >> sys.stderr, "Los consumos de fibra entre %s y %s (%d bultos, %s kg) no coinciden con el sumatorio de los consumos diarios entre esas mismas fechas (%d bultos, %s kg)." % (
              utils.str_fecha(fecha0), utils.str_fecha(fecha1), bultos, utils.float2str(cantidad), sumbultos, utils.float2str(sumcantidad))
            res = False
            if not report_mode:
                break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_partidas_de_carga_sin_fibra_o_sin_produccion(report_mode = False):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar el primero de los objetos que incumple el criterio.
    Comprueba que de haber partidas sin producción, que éstas sean las 
    últimas; y que todas las partidas con producción tengan balas relacionadas.
    Para que una partida tenga producción debe haber al menos un parte de 
    producción con las partidas de geotextiles relacionadas con la partida de 
    carga (y si desde una partida se puede llegar a un PDP es porque al menos 
    hay un artículo que los relaciona).
    """
    res = True
    ultima_con_produccion = None
    ultima_con_carga = None
    for pc in pclases.PartidaCarga.select(orderBy = "-fecha"):
        tiene_carga = len(pc.balas) > 0
        tiene_produccion = len(pc._get_partes_partidas()) > 0
        if tiene_carga and ultima_con_carga == None:
            ultima_con_carga = pc
        if tiene_produccion and ultima_con_produccion == None:
            ultima_con_produccion = pc
        if not tiene_carga and ultima_con_carga != None:
            print >> sys.stderr, "La partida de carga ID %d (%s, %s) no tiene carga y no está entre las últimas. (La última con carga es la partida %s, con fecha %s)." % (
                pc.id, pc.codigo, utils.str_fechahora(pc.fecha), ultima_con_carga.codigo, utils.str_fechahora(ultima_con_carga.fecha))
            res = False
            if not report_mode:
                break
        if not tiene_produccion and ultima_con_produccion != None:
            print >> sys.stderr, "La partida de carga ID %d (%s, %s) no tiene producciÓn y no está entre las últimas. (La última con producción es la partida %s, con fecha %s)." % (
                pc.id, pc.codigo, utils.str_fechahora(pc.fecha), ultima_con_produccion.codigo, utils.str_fechahora(ultima_con_produccion.fecha))
            res = False
            if not report_mode:
                break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_partidas_con_mas_de_un_producto(
        report_mode = False, 
        fecha_filtro_anteriores_a = None):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar el primero de los objetos que incumple el criterio.
    Comprueba que todas las partidas tengan un único producto relacionado.
    Si fecha_filtro_anteriores_a es distinto de None, ignora las partidas 
    anteriores a la fecha recibida (en realidad, ignora los rollos con 
    fechahora anteriores, y por tanto sus partidas).
    OJO: Hay un montón de partidas anteriores a noviembre de 2006 
    (aproximadamente) donde habrá más de un producto por partida, puesto que 
    fue en una modificación durante esas fechas cuando se dividieron las 
    partidas en partidas de geotextiles y partidas de carga precisamente 
    para permitir estos casos sin alterar la normalización de la BD.
    """
    res = True
    if fecha_filtro_anteriores_a:
        partidas = pclases.Partida.select(pclases.AND(pclases.Rollo.q.partidaID == pclases.Partida.q.id, 
                                                      pclases.Rollo.q.fechahora >= fecha_filtro_anteriores_a), 
                                          orderBy = "-id") 
    else:
        partidas = pclases.Partida.select(orderBy = "-id")
    for partida in partidas:
        productos = pclases.ProductoVenta._queryAll(""" 
            SELECT producto_venta.id 
            FROM producto_venta, articulo, rollo 
            WHERE producto_venta.id = articulo.producto_venta_id 
                AND articulo.rollo_id = rollo.id 
                AND rollo.partida_id = %d 
            GROUP BY producto_venta.id """ % (partida.id))
        numproductos = len(productos)
        if numproductos > 1:
            print >> sys.stderr, "La partida ID %d (%s) tiene %d productos relacionados." % (partida.id, partida.codigo, numproductos)
            res = False
            if not report_mode:
                break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_partes_simultaneos_empleados(report_mode = False):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar el primero de los objetos que incumple el criterio.
    Compara que un empleado solo esté en un parte de producción a la vez. 
    O que, en caso de estar en varios, que entre todas las horas no supere la 
    duración de la hora de inicio del primer parte y la hora de finalización 
    del último (aprovechando que los partes se solapan, la duración total 
    será esa, ya que no hay huecos entre ellos).
    """
    PDP = pclases.ParteDeProduccion
    res = True
    for pdp in pclases.ParteDeProduccion.select(orderBy = "-id"):
        for ht in pdp.horasTrabajadas:
            e = ht.empleado
            partes = PDP.select(
                      pclases.AND(
                        pclases.OR(
                          pclases.AND(
                            pdp.fechahorainicio <= PDP.q.fechahorainicio, 
                            PDP.q.fechahorainicio <= pdp.fechahorafin), 
                          pclases.AND(
                            pdp.fechahorainicio <= PDP.q.fechahorafin, 
                            PDP.q.fechahorainicio <= pdp.fechahorafin)
                          ), 
                        pclases.HorasTrabajadas.q.partedeproduccionid==PDP.q.id,
                        pclases.HorasTrabajadas.q.empleadoid == e.id))
            if partes.count() > 1:  # Me cuento a mí mismo
                horas_inicio = [p.fechahorainicio for p in partes]
                horas_fin = [p.fechahorafin for p in partes]
                horas_inicio.sort()
                horas_fin.sort()
                hora_inicio_mas_temprana = horas_inicio[0]
                hora_fin_mas_tardia = horas_fin[-1]
                duracion_total = hora_fin_mas_tardia - hora_inicio_mas_temprana
                horas_totales = 0
                for parte in partes:
                    for ht in parte.horasTrabajadas:
                        if ht.empleado == e:
                            horas_totales += ht.horas
                if horas_totales > duracion_total:
                    print >> sys.stderr, "El empleado ID %d (%s) está en más de un parte (%d: %s) y tiene más horas de trabajo (%s) que la duración total (%s)." % (
                        e.id, e.nombre + " " + e.apellidos, partes.count(), 
                        ", ".join(["%d [%s a %s] %s" % (
                            p.id, 
                            utils.str_fechahora(p.fechahorainicio), 
                            utils.str_fechahora(p.fechahorafin), 
                            (p.es_de_fibra() and "FIB") or (p.es_de_geotextiles() and "GTX") or "?") for p in partes]), 
                        utils.str_hora(horas_totales), utils.str_hora(duracion_total))
                    res = False
                    if not report_mode:
                        break
        if not res and not report_mode:
            break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_codigos_unicos_en_productos_compra(report_mode = False):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar el primero de los objetos que incumple el criterio.
    Comprueba que todos los códigos de los productos de compra, tanto en el 
    campo código como en la descripción (el TPV los busca también ahí), son 
    únicos.
    """
    res = True
    pcs = pclases.ProductoCompra.select(orderBy = "id")
    dupes_totales = []
    for pc in pcs:
        if pc in dupes_totales:
            continue    # Avoid morons iterations!
        codigo = pc.codigo  # Código primario. Es el que me interesa que no 
                            # esté repetido. El código de las descripciones 
                            # es muy difícil de determinar, no siempre está 
                            # entre paréntesis. Si dos productos tienen el 
                            # código en blanco pero en sus descripciones 
                            # tienen códigos coincidentes, debería medirle el 
                            # lomo al usuario y decirle que ponga los códigos 
                            # en su sitio. El de las descripciones es auxiliar.
        dupes = pclases.ProductoCompra.select(pclases.OR(
                    pclases.ProductoCompra.q.codigo == codigo, 
                    pclases.ProductoCompra.q.descripcion.contains(codigo))
                )
        if (codigo.strip() 
            and dupes.count() > 1):
            dupes_de_verdad = []
            for dupe in dupes:
                # maybe = dupe.descripcion.replace("(", "").replace(")", "").lower().split()
                maybe = []
                for i in dupe.descripcion.split("("):
                    for j in i.split(")"):
                        maybe.append(j.strip().lower())
                if (len(codigo) > 2 
                    and codigo != "TINTADA"
                    and dupe.id != pc.id
                    and (codigo.lower() in maybe
                         or codigo.lower() == dupe.codigo.lower())):
                    # Manda pelotas que un código pueda ser "CC". Sí, igual que
                    # "centímetros cúbicos" en una descripción.
                    # También hay un "TINTADA" que hay que respetar.
                    dupes_de_verdad.append(dupe)
            if dupes_de_verdad:
                print >> sys.stderr, "Código duplicado:\n>>> %s - %s (ID %d)"%(
                    pc.codigo, pc.descripcion, pc.id)
                for dupe in dupes_de_verdad:
                    if dupe.id != pc.id:
                        print "    %s - %s (ID %d)" % (dupe.codigo, 
                                                       dupe.descripcion, 
                                                       dupe.id)
                    dupes_totales.append(dupe)
                res = False
                if not report_mode:
                    break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_mismo_cliente_pedidos_albaranes_facturas(report_mode = False, 
                                                       ignore_list = []):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar el primero de los objetos que incumple el criterio.
    Comprueba que el cliente de cada pedido, albarán y factura relacionados 
    entre sí son el mismo.
    Si el pedido, albarán o factura está en el «ignore_list» no se tendrá 
    en cuenta como incorrecto.
    """
    res = True
    pedidos_venta = pclases.PedidoVenta.select(orderBy = "-id")
    albaranes_salida = pclases.AlbaranSalida.select(orderBy = "-id")
    facturas_venta = pclases.FacturaVenta.select(orderBy = "-id")
    for p in pedidos_venta:
        if p in ignore_list:
            continue
        albaranes = utils.unificar([ldv.albaranSalida 
                                    for ldv in p.lineasDeVenta
                                    if ldv.albaranSalida != None])
        facturas = utils.unificar([ldv.facturaVenta 
                                   for ldv in p.lineasDeVenta
                                   if ldv.facturaVenta != None])
        clientes = ([p.cliente] 
                    + [a.cliente for a in albaranes] 
                    + [f.cliente for f in facturas])
        clientes = utils.unificar(clientes)
        if len(clientes) > 1:
            print >> sys.stderr, "Pedido ID %d (%s) tiene como cliente: %s" % (
                p.id, p.numpedido, p.cliente and p.cliente.nombre or "None")
            print >> sys.stderr, "    Albaranes y facturas relacionados:"
            for a in albaranes:
                print >> sys.stderr, "    Albarán ID %d (%s) -> %s" % (
                    a.id,a.numalbaran,a.cliente and a.cliente.nombre or "None")
            for f in facturas:
                print >> sys.stderr, "    Factura ID %d (%s) -> %s" % (
                    f.id,f.numfactura,f.cliente and f.cliente.nombre or "None")
            res = False
            if not report_mode:
                break
    for a in albaranes_salida:
        if a in ignore_list:
            continue
        pedidos = utils.unificar([ldv.pedidoVenta 
                                  for ldv in a.lineasDeVenta 
                                  if ldv.pedidoVenta != None])
        facturas = a.get_facturas()
        clientes = ([p.cliente for p in pedidos] 
                    + [a.cliente] 
                    + [f.cliente for f in facturas])
        clientes = utils.unificar(clientes)
        if len(clientes) > 1:
            print >> sys.stderr, "Albarán ID %d (%s) tiene como cliente: %s" % (
                a.id, a.numalbaran, a.cliente and a.cliente.nombre or "None")
            print >> sys.stderr, "    Pedidos y facturas relacionados:"
            for p in pedidos:
                print >> sys.stderr, "    Pedido ID %d (%s) -> %s" % (
                    p.id, p.numpedido, p.cliente and p.cliente.nombre or "None")
            for f in facturas:
                print >> sys.stderr, "    Factura ID %d (%s) -> %s" % (
                    f.id,f.numfactura,f.cliente and f.cliente.nombre or "None")
            res = False
            if not report_mode:
                break
    for f in facturas_venta:
        if f in ignore_list:
            continue
        pedidos = f.get_pedidos()
        albaranes = f.get_albaranes()
        clientes = ([p.cliente for p in pedidos] 
                    + [a.cliente for a in albaranes] 
                    + [f.cliente])
        clientes = utils.unificar(clientes)
        if len(clientes) > 1:
            print >> sys.stderr, "Factura ID %d (%s) tiene como cliente: %s" % (
                f.id, f.numfactura, f.cliente and f.cliente.nombre or "None")
            print >> sys.stderr, "    Pedidos y albaranes relacionados:"
            for p in pedidos:
                print >> sys.stderr, "    Pedido ID %d (%s) -> %s" % (
                    p.id, p.numpedido, p.cliente and p.cliente.nombre or "None")
            for a in albaranes:
                print >> sys.stderr, "    Albarán ID %d (%s) -> %s" % (
                    a.id,a.numalbaran,a.cliente and a.cliente.nombre or "None")
            res = False
            if not report_mode:
                break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_saltos_facturas_albaranes_pedidos_y_tickets(report_mode = False, 
                                                          tickets = True, 
                                                          pedidos = False, 
                                                          albaranes = False, 
                                                          facturas = True, 
                                                          ignore_list = []):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar el primero de los objetos que incumple el criterio.
    Comprueba que la numeración de pedidos, albaranes y facturas de venta 
    son consecutivos.
    Si facturas es False, no comprueba las facturas.
    Igual con albaranes, pedidos y tickets.
    Los objetos de ignore_list son ignorados.
    """
    res = True
    if ((not res and report_mode) or res) and facturas:
        por_serie = {}  
            # Diccionario con el último número de cada serie en cada momento
        for c in pclases.Contador.select():
            por_serie[c] = []
        fs = pclases.FacturaVenta.select(orderBy = "numfactura")
        for f in fs:
            if f in ignore_list:
                continue
            numfactura = f.get_numero_numfactura_contador()
            contador = f.get_contador()
            por_serie[contador].append(numfactura)
        for c in por_serie:
            por_serie[c].sort()
        for c in por_serie:
            lista = por_serie[c]
            if len(lista) > 1:
                for i in range(1, len(lista)):
                    if lista[i] != lista[i-1] + 1:
                        print >> sys.stderr, "Número factura %d no consecutivo con anterior %s. Contador ID %d (%s - %s)." % (lista[i], 
                                 lista[i-1],
                                 c.id,
                                 c.prefijo, 
                                 c.sufijo)
                        res = False
                        if not report_mode:
                            break
    if ((not res and report_mode) or res) and albaranes:
        albs = pclases.AlbaranSalida.select(orderBy = "numalbaran")
        nums = {} 
        for a in albs:
            if a in ignore_list:
                continue
            parte_num = str(a.get_num_numalbaran())[::-1]
            resto = a.numalbaran[::-1].replace(parte_num, "")[::-1]
            if resto not in nums:
                nums[resto] = [a.get_num_numalbaran()]
            else:
                nums[resto].append(a.get_num_numalbaran())
            for r in nums.keys():
                nums[r].sort()
            for r in nums.keys():
                lista = nums[r]
                if len(lista) > 1:
                    for i in range(1, len(lista)):
                        if lista[i] != lista[i-1] + 1:
                            print >> sys.stderr, "Número albarán %d no es consecutivo con el anterior, %d. Albarán número %s%d" % (lista[i], 
                                           lista[i-1], 
                                           r, 
                                           lista[i])
                            res = False
                            if not report_mode:
                                break
    if ((not res and report_mode) or res) and pedidos:
        peds = pclases.PedidoVenta.select(orderBy = "numpedido")
        nums = [utils.parse_numero(p.numpedido) for p in peds 
                if p not in ignore_list]
        nums.sort()
        if len(nums) > 1:
            for i in range(1, len(nums)):
                if nums[i] != nums[i-1] + 1:
                    print >> sys.stderr, "Número pedido %d no es consecutivo con anterior, %d." % (nums[i], nums[i-1])
                    res = False
                    if not report_mode:
                        break
    if ((not res and report_mode) or res) and tickets:
        ticks = pclases.Ticket.select(orderBy = "numticket")
        if ticks.count():
            annos = {}
            for t in ticks:
                if t in ignore_list:
                    continue
                if t.fechahora.year not in annos:
                    annos[t.fechahora.year] = [t.numticket]
                else:
                    annos[t.fechahora.year].append(t.numticket)
            for a in annos:
                nums = annos[a] 
                nums.sort()
                if len(nums) > 2:
                    for i in range(1, len(nums)):
                        if nums[i] != nums[i-1] + 1:
                            print >> sys.stderr, "Número ticket %d no es consecutivo con anterior, %d. Año %d" % (nums[i], nums[i-1], a)
                            res = False
                            if not report_mode:
                                break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_almacen_partidas_carga(report_mode = False, ignore_list = []):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar el primero de los objetos que incumple el criterio.
    Comprueba que no hay artículos con almacen == None y sin albaranes de 
    salida o partida de carga.
    """
    res = True
    partidasDeCarga = pclases.PartidaCarga.select(orderBy = "-id")
    for partida in partidasDeCarga:
        for bala in partida.balas:
            if bala.articulo in ignore_list:
                continue
            if bala.articulo.almacen != None:
                print >> sys.stderr, "Artículo %d (bala %s) está en la partida de carga %s y en el almacén %s a la vez." % (bala.articulo.id, bala.codigo, 
                    partida.codigo, bala.articulo.almacen.nombre)
                res = False
                if not report_mode:
                    break
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_pares_articulos(report_mode = False, ignore_list = []):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale 
    al encontrar 
    el primero de los objetos que incumple el criterio.
    Comprueba que todos los artículos y todos los objetos rollos, balas, 
    bigbags, etc. estén emparejados. Para hacerlo simplemente cuenta, así 
    que tarda mucho menos que la comprobación por objetos de rollos uno a uno.
    La única desventaja es que no te dice los objetos erróneos, simplemente 
    si están bien o no.
    Por ese mismo motivo no usa el ignore_list.
    """
    # Balas
    cardbalas = pclases.Bala.select().count()
    cardabalas = pclases.Articulo.select(
                    pclases.Articulo.q.balaID != None).count()
    res = cardbalas == cardabalas
    if not res:
        print >> sys.stderr, "#Balas = %d. #Articulos bala = %d" % (cardbalas, 
                                                                    cardabalas)
        if not report_mode:
            return res
    # Rollos
    cardrollos = pclases.Rollo.select().count()
    cardarollos = pclases.Articulo.select(
                    pclases.Articulo.q.rolloID != None).count()
    res = res and cardrollos == cardarollos
    if not res:
        print >> sys.stderr, "#Rollos = %d. #Articulos rollo = %d" % (
                    cardrollos, cardarollos)
        if not report_mode:
            return res
    # Bigbag
    cardbigbags = pclases.Bigbag.select().count()
    cardabigbags = pclases.Articulo.select(
                    pclases.Articulo.q.bigbagID != None).count()
    res = res and cardbigbags == cardabigbags
    if not res:
        print >> sys.stderr, "#Bigbags = %d. #Articulos bigbag = %d" % (
                    cardbigbags, cardabigbags)
        if not report_mode:
            return res
    # Rollos defectuosos
    cardrolloDefectuosos = pclases.RolloDefectuoso.select().count()
    cardarolloDefectuosos = pclases.Articulo.select(
                    pclases.Articulo.q.rolloDefectuosoID != None).count()
    res = res and cardrolloDefectuosos == cardarolloDefectuosos
    if not res:
        print >> sys.stderr, "#RolloDefectuosos = %d. "\
                             "#Articulos rolloDefectuoso = %d" % (
                    cardrolloDefectuosos, cardarolloDefectuosos)
        if not report_mode:
            return res
    # Balas de cable
    cardbalaCables = pclases.BalaCable.select().count()
    cardabalaCables = pclases.Articulo.select(
                    pclases.Articulo.q.balaCableID != None).count()
    res = res and cardbalaCables == cardabalaCables
    if not res:
        print >> sys.stderr, "#BalaCables = %d. #Articulos balaCable = %d" % (
                    cardbalaCables, cardabalaCables)
        if not report_mode:
            return res
    # Rollos C
    cardrolloCs = pclases.RolloC.select().count()
    cardarolloCs = pclases.Articulo.select(
                    pclases.Articulo.q.rolloCID != None).count()
    res = res and cardrolloCs == cardarolloCs
    if not res:
        print >> sys.stderr, "#RolloCs = %d. "\
                             "#Articulos rolloC = %d" % (
                    cardrolloCs, cardarolloCs)
        if not report_mode:
            return res
    return res

@crono  # XXX Comentar si python <= 2.3
def comprobar_almacenes_albaranes(report_mode = False, ignore_list = []):
    """
    Si report_mode es True acaba la función completa. En caso contrario sale al encontrar 
    el primero de los objetos que incumple el criterio.
    Comprueba que todos los albaranes de salida y de entrada tienen asignado 
    un albarán de origen y uno de destino respectivamente.
    """
    res = True
    albaranesSalida = pclases.AlbaranSalida.select()
    for alb in albaranesSalida:
        if alb in ignore_list:
            continue
        almacen = alb.almacenOrigen
        if almacen == None:
            print >> sys.stderr, "El albarán de salida %s (ID %d) no tiene almacén de origen." % (alb.numalbaran, alb.id)
            res = False
            if not report_mode:
                break
    albaranesEntrada = pclases.AlbaranEntrada.select()
    for alb in albaranesEntrada:
        if alb in ignore_list:
            continue
        almacen = alb.almacen
        if almacen == None:
            print >> sys.stderr, "El albarán de entrada %s (ID %d) no tiene almacén de destino." % (alb.numalbaran, alb.id)
            res = False
            if not report_mode:
                break
    return res

############# PLANTILLA ########################################################

#@crono  # XXX Comentar si python <= 2.3
#def comprobar_<++>(report_mode = False, ignore_list = []):
#    """
#    Si report_mode es True acaba la función completa. En caso contrario sale al encontrar 
#    el primero de los objetos que incumple el criterio.
#    <++>
#    """
#    res = True
#    <++>
#    for <++> in <++>:
#        if <++> in ignore_list:
#            continue
#        <++>
#        if <++>:
#            print >> sys.stderr, "<++>" % (<++>)
#            res = False
#            if not report_mode:
#                break
#    return res

