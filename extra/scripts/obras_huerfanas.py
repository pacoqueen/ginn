#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Con el trajín de obras creadas desde presupuesto, añadir y quitar obras
de los clientes, se han quedado algunas obras huérfanas de cliente que
a veces incluso tienen pedidos y facturas. Este script elimina y corrige
esas obras según si son huérfanas sin facturas ni pedidos --en ese caso
las borra por completo-- o huérfanas por error con alguna factura o pedido
--en cuyo caso agrega el cliente a la obra--.
"""

import sys
import os

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
from lib.textprogressbar.progress.bar import IncrementalBar
from lib.textprogressbar.progress.spinner import MoonSpinner


def load_obras():
    """
    Devuelve las obras huérfanas de cliente de la BD.
    """
    spinner = MoonSpinner("Buscando obras sin cliente...")
    obras = []
    for obra in pclases.Obra.select():
        spinner.next()
        if not obra.clientes:
            obras.append(obra)
    return obras


def corregir_obra(obra):
    """
    Si la obra tiene pedidos o facturas, la asigna al cliente o clientes
    de esos pedidos o facturas. Si no tiene facturas, pedidos, abonos ni
    presupuestos, como tampoco tiene clientes, la elimina (incluyendo contactos
    si tuviera y no estuvieran asignados a otras obras).
    """
    eliminada = False
    # Corrección si es huérfana por error y tiene documentos asignados
    relaciones = (obra.presupuestos, obra.pedidosVenta,
                  obra.facturasVenta, obra.abonos)
    for lista_relacionados in relaciones:
        for objeto in lista_relacionados:
            cliente = objeto.cliente
            if cliente and cliente not in obra.clientes:
                # Los presupuestos pueden no tener cliente porque no se
                # haya dado de alta todavía.
                obra.addCliente(cliente)
    # Eliminación si es huérfana total
    if not obra.clientes and not obra.presupuestos:
        for contacto in obra.contactos:
            contacto.removeObra(obra)
            if not contacto.obras:    # Solo era contacto de esta obra:
                contacto.destroySelf()
        obra.destroySelf()
        eliminada = True
    return eliminada


def main():
    """
    Busca y recorre las obras huérfanas y las corrige.
    """
    obras = load_obras()
    total_obras = len(obras)
    barra = IncrementalBar('Obras huérfanas', max=total_obras)
    res = {'eliminadas': [], 'corregidas': []}
    for obra in obras:
        nombre_obra = obra.nombre
        puid_obra = obra.puid
        if corregir_obra(obra):
            clave = 'eliminadas'
        else:
            clave = 'corregidas'
        res[clave].append((puid_obra, nombre_obra))
        barra.next()
    barra.finish()
    print "%d obras eliminadas. %d corregidas." % (len(res['eliminadas']),
                                                   len(res['corregidas']))
    print "************** OBRAS ELIMINADAS ***************"
    for puid, nombre in res['eliminadas']:
        print puid, nombre
    print "************** OBRAS CORREGIDAS ***************"
    for puid, nombre in res['corregidas']:
        print puid, nombre


if __name__ == "__main__":
    main()
