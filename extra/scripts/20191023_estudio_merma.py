#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=invalid-name

"""
Pequeño estudio de merma
========================

Para ver la merma de la línea de geotextiles primero hay que determinar con la
mejor exactitud posible los kg consumidos y fabricados a través de las partidas
de carga.

Primero hay que encontrar la fabricación completa perfecta: que el cuarto esté
vacío antes de empezar a fabricar geotextiles y que vuelva a estar vacío al
terminar.

Vamos a montar una tabla con los lotes, partidas de carga y partidas fabricadas
con los kg consumidos y una estimación de cómo se consumen entre las diferentes
partidas.
"""

from __future__ import print_function
import sys
import os
import datetime
# Determino dónde estoy para importar pclases y utils
DIRACTUAL = os.path.split(os.path.abspath(os.path.curdir))[-1]
if DIRACTUAL != "ginn":
    PATH_TO_F = os.path.join("..", "..", "ginn")
    sys.path.append(PATH_TO_F)
# pylint: disable=wrong-import-position,import-error
from framework import pclases   # noqa
# from api import murano          # noqa
from lib.tqdm.tqdm import tqdm  # noqa


def get_partidas_carga(lote):
    """
    Devuelve un diccionario con las partidas de carga, número de balas y kg
    consumidos en cada una de ellas para el lote recibido.
    """
    pcs = {}
    for b in lote.balas:
        peso_neto = b.articulo.peso_neto
        pcarga = b.partidaCarga
        if pcarga:
            try:
                pcs[pcarga][0] += 1
                pcs[pcarga][1] += peso_neto
            except KeyError:
                pcs[pcarga] = [1, peso_neto]
    return pcs


def get_lotes_pcarga_partida(pcarga, partida=None):
    """
    Devuelve un diccionario con los lotes, balas y kg consumidos de cada lote
    en la partida de carga que corresponde a la partida recibida.
    Se hace una estimación de los kg consumidos de cada lote para la partida
    concreta dividiendo toda la producción de la partida de carga entre todos
    los consumos y multiplicando por la producción de la partida en concreto,
    incluyendo producto C.
    Si partida es None, devuelve los consumos por lote de la partida de carga
    completa.
    """
    res = {}
    if pcarga:
        if partida:
            kgs = sum([get_kg_fabricados(p) for p in pcarga.partidas])
            try:
                ratio = get_kg_fabricados(partida)/kgs
            except ZeroDivisionError:
                # No tiene partidas o solo partidas vacías. Consumo todo.
                ratio = 1
        else:
            ratio = 1
        for bala in pcarga.balas:
            lote = bala.lote
            try:
                res[lote][0] += ratio
                res[lote][1] += bala.articulo.peso_sin * ratio
            except KeyError:
                res[lote] = [ratio, bala.articulo.peso_sin * ratio]
    return res


def calcular_kg_consumidos_por_partida(partida):
    """
    Aquí hay otro punto crítico. Es imposible saber a ciencia cierta, cuando
    una partida de carga ha generado varias partidas de geotextiles, cuántos
    kg se han consumido por cada partida.
    Pero podemos hacer una estimación. Probaremos primero con una proporción
    directa. Los kg consumidos se han repartido equitativamente entre los kg
    producidos. Nos dará una merma para la partida de carga completa.
    La mandanga está en que queremos la merma por partida de geotextiles.
    Porque sospecho que la merma va en función del producto fabricado, no de
    la línea en sí (también de las pruebas que se hagan, el propio turno...).
    Ojo también con el peso del embalaje porque es estimado. ¿No hay manera de
    sacar de la propia línea los kg fabricados _raw_?
    """
    pcarga = partida.partidaCarga
    if not pcarga:
        res = 0
    else:
        kg_cargados = sum([b.articulo.peso_neto for b in pcarga.balas])
        kg_fabricados = 0.0
        for partida_fabricada in pcarga.partidas:
            kg_fabricados += get_kg_fabricados(partida_fabricada)
        kg_partida = get_kg_fabricados(partida)
        # Puritica regla de tres
        try:
            res = (kg_cargados/kg_fabricados)*kg_partida
        except ZeroDivisionError:
            # No se ha fabricado nada. Asumo que no he consumido. Todas las
            # balas siguen en el cuarto (si es que la pcarga no está vacía
            # también).
            res = 0
    return res


def calcular_kg_fabricados_por_lote(partida, lote):
    """
    Hace una estimación directa de los kg fabricados según los kg de un lote
    determinado cargados.
    """
    # Puritica regla de tres.
    # El total fabricado de la partida entre los kg totales cargados en la
    # única partida de carga que une la partida con el lote da la proporción
    # de kg fabricados por kg cargado. Con eso ya podríamos estimar un
    # porcentaje de merma. Multiplicamos eso por los kg de las balas del lote
    # cargadas en la partida de carga y tenemos la estimación de los kg
    # fabricados con lo cargado de ese lote.
    fabricado = get_kg_fabricados(partida)
    pcarga = partida.partidaCarga
    cargado = sum([b.articulo.peso_sin for b in pcarga.balas])
    consumido = 0.0
    for bala in pcarga.balas:
        if bala.lote == lote:
            consumido += bala.articulo.peso_sin
    try:
        ratio = fabricado/cargado
    except ZeroDivisionError:
        # Partida de carga vacía, probablemente.
        res = fabricado
    else:
        res = ratio * consumido
    return res


def get_kg_fabricados(partida, C=True):
    """
    Devuelve los kg reales netos (según estimación del peso de embalaje)
    fabricados en la partida. Incluye el producto C si C es True.
    """
    res = sum([r.articulo.peso_real - r.articulo.peso_embalaje
               for r in partida.rollos])
    if C:
        res += get_fabricado_c(partida)[1]
    return res


def get_fabricado_c(partida):
    """
    A partir de las fechas de los partes de producción de la partida devuelve
    los kg de geotextiles C fabricados durante la partida.
    """
    kg = 0.0
    bultos = 0
    for pdp in partida.get_partes_de_produccion():
        fini = pdp.fechahorainicio
        ffin = pdp.fechahorafin
        rollosc = pclases.RolloC.select(
            pclases.AND(pclases.RolloC.q.fechahora >= fini,
                        pclases.RolloC.q.fechahora < ffin))
        for rolloc in rollosc:
            # Otra aproximación. El peso neto de un rollo C incluye el embalaje
            # que lógicamente no es estándar y no sabemos cuánto pesa el
            # embalaje de cada rollo. Ni siquiera estimado.
            kg += rolloc.articulo.peso_neto
            bultos += 1
    return bultos, kg


# pylint: disable=too-many-locals
def main():
    """
    Rutina principal.
    """
    try:
        anno = int(sys.argv[1])
    except IndexError:
        anno = datetime.date.today().year
    except (ValueError, TypeError):
        print("Indica año o nada para el año actual.")
        sys.exit(2)
    fout = open("estudio_de_merma_{}.txt".format(anno), "w")
    fini = datetime.datetime(anno, 1, 1)
    ffin = datetime.datetime(anno+1, 1, 1)
    primerabala = pclases.Bala.select(pclases.Bala.q.fechahora >= fini,
                                      orderBy="fechahora")[0]
    ultimabala = pclases.Bala.select(pclases.Bala.q.fechahora < ffin,
                                     orderBy="-fechahora")[0]
    lotes = pclases.Lote.select(
        pclases.AND(pclases.Lote.q.numlote >= primerabala.lote.numlote,
                    pclases.Lote.q.numlote <= ultimabala.lote.numlote),
        orderBy="numlote")
    primerrollo = pclases.Rollo.select(pclases.Rollo.q.fechahora >= fini,
                                       orderBy="fechahora")[0]
    ultimorollo = pclases.Rollo.select(pclases.Rollo.q.fechahora < ffin,
                                       orderBy="-fechahora")[0]
    partidas = pclases.Partida.select(
        pclases.AND(
            pclases.Partida.q.numpartida >= primerrollo.partida.numpartida,
            pclases.Partida.q.numpartida <= ultimorollo.partida.numpartida),
        orderBy="numpartida")
    fout.write(("\t".join(["Lote",
                           "kg cargados",
                           "Partida de carga",
                           "kg consumidos",
                           "Partida",
                           "kg fabricados totales (A+B+C)",
                           "kg fabricados proporcional (A+B+C)",
                           "merma (consumido-fabricado)",
                           "kg fabricados partida (A+B)",
                           "# balas lote",
                           "kg lote",
                           "# balas cargadas partida carga",
                           "kg balas cargadas partida carga",
                           "# rollos partida",
                           "# rollos partida + C"])))
    fout.write("\n")
    for partida in tqdm(partidas, total=partidas.count()):
        kg_consumidos = calcular_kg_consumidos_por_partida(partida)
        kg_fabricados = get_kg_fabricados(partida, C=False)
        bultos_c, kg_fabricados_c = get_fabricado_c(partida)
        kg_fabricados_totales = kg_fabricados + kg_fabricados_c
        # cargas = get_partidas_carga(lote)
        pcarga = partida.partidaCarga
        if pcarga:
            lotes = get_lotes_pcarga_partida(pcarga, partida)
        else:
            lotes = []
        if lotes:   # Con partida de carga y partida de carga no vacía.
            kg_pcarga_completa = sum(
                [b.articulo.peso_sin for b in pcarga.balas])
            for lote in sorted(lotes.keys(), key=lambda l: l.numlote):
                kg_lote_completo = sum([b.articulo.peso_sin
                                        for b in lote.balas])
                kg_cargados = lotes[lote][1]
                kg_proporcional = calcular_kg_fabricados_por_lote(partida,
                                                                  lote)
                merma = kg_cargados - kg_proporcional   # Así es sumable
                fout.write("\t".join(
                    [lote.codigo,
                     str(kg_cargados).replace(".", ","),
                     pcarga.codigo,
                     str(kg_consumidos).replace(".", ","),
                     partida.codigo,
                     str(kg_fabricados_totales).replace(".", ","),
                     str(kg_proporcional).replace(".", ","),
                     str(merma).replace(".", ","),
                     str(kg_fabricados).replace(".", ","),
                     str(len(lote.balas)),
                     str(kg_lote_completo).replace(".", ","),
                     str(len(pcarga.balas)),
                     str(kg_pcarga_completa).replace(".", ","),
                     str(len(partida.rollos)),
                     str(len(partida.rollos)+bultos_c)
                     ]))
                fout.write("\n")
        else:   # Partida sin partida de carga y por tanto sin lote.
            lote = None
            kg_pcarga_completa = 0.0
            kg_lote_completo = 0.0
            kg_cargados = 0.0
            kg_proporcional = kg_fabricados_totales
            merma = kg_cargados - kg_proporcional   # Así es sumable
            fout.write("\t".join(
                [lote and lote.codigo or "",
                 str(kg_cargados).replace(".", ","),
                 pcarga and pcarga.codigo or "",
                 str(kg_consumidos).replace(".", ","),
                 partida.codigo,
                 str(kg_fabricados_totales).replace(".", ","),
                 str(kg_proporcional).replace(".", ","),
                 str(merma).replace(".", ","),
                 str(kg_fabricados).replace(".", ","),
                 str(lote and len(lote.balas) or 0),
                 str(kg_lote_completo).replace(".", ","),
                 str(pcarga and len(pcarga.balas) or 0),
                 str(kg_pcarga_completa).replace(".", ","),
                 str(len(partida.rollos)),
                 str(len(partida.rollos)+bultos_c)
                 ]))
            fout.write("\n")
    fout.close()


if __name__ == "__main__":
    main()
