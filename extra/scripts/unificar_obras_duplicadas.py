#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Después de corregir las obras huérfanas, me he dado cuenta de que hay un
montón de obras duplicadas (se llaman exactamente igual). Este script las
detecta y unifica en una sola.
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
from lib.textprogressbar.progress.bar import IncrementalBar, ShadyBar
from collections import defaultdict


def corregir_nombres_obra():
    """
    Corrige los nombres de obra eliminando los retornos de carro.
    """
    cambiadas = []
    obras = pclases.Obra.select()
    suffix = '%(percent)d%% [%(elapsed_td)s / %(eta_td)s]'
    txt = "Corrigiendo nombres"
    for obra in ShadyBar(txt, suffix=suffix, max=obras.count()).iter(obras):
        nombre_anterior = obra.nombre
        obra.nombre = obra.nombre.replace("\t", " ").replace("\n", " ").strip()
        obra.nombre = obra.nombre.replace("“", '"').replace("”", '"')
        obra.nombre = utils.eliminar_dobles_espacios(obra.nombre)
        obra.syncUpdate()
        if obra.nombre != nombre_anterior:
            cambiadas.append((nombre_anterior, obra))
    return cambiadas

def load_obras_duplicadas():
    """
    Devuelve las obras duplicadas en un diccionario agrupando por nombre.
    """
    obras = pclases.Obra.select(orderBy = "nombre")
    suffix = '%(percent)d%% [%(elapsed_td)s / %(eta_td)s]'
    bar = ShadyBar("Buscando duplicadas", suffix=suffix, 
                   max=obras.count())
    dupes = defaultdict(lambda: [])
    for obra in bar.iter(obras):
        nombre = obra.nombre
        if pclases.Obra.selectBy(nombre=nombre).count() > 1:
            dupes[nombre].append(obra)
    return dupes


def unificar_obras(dest, dupe):
    """
    Pasa las ofertas, pedidos, facturas, abonos, contactos y clientes de «dupe»
    a «dest».
    Combina los datos de dirección al más completo de los dos registros. Las
    observaciones las concatena si no son idénticas. Las fechas inicial y
    final las adelanta o atrasa a la más temprana o tardía respectivamente de
    de las dos obras.
    La obra «dupe» se eliminará al terminar.
    """
    # 0.- Datos
    ## ¿genérica? Entonces intercambio origen y destino.
    if dupe.generica and not dest.generica:
        dest, dupe = dupe, dest
    if not dest.direccion.strip():
        dest.direccion = dupe.direccion
        dest.cp = dupe.cp
        dest.coudad = dupe.ciudad
        dest.provincia = dupe.provincia
        dest.pais = dupe.pais
    ## fechas
    if dest.fechainicio and dupe.fechainicio:
        dest.fechainicio = min(dest.fechainicio, dupe.fechainicio)
    elif dupe.fechainicio and not dest.fechainicio:
        dest.fechainicio = dupe.fechainicio
    if dest.fechafin and dupe.fechafin:
        dest.fechafin = min(dest.fechafin, dupe.fechafin)
    elif dupe.fechafin and not dest.fechafin:
        dest.fechafin = dupe.fechafin
    ## observaciones
    if dupe.observaciones and dest.observaciones != dupe.observaciones:
        if dest.observaciones.strip():
            dest.observaciones += ". " + dupe.observaciones
        else:
            dest.observaciones = dupe.observaciones
    dest.observaciones = ("[obra unificada] %s" % dest.observaciones).strip()
    puid_dupe = dupe.puid
    # 1.- Ofertas (1 a m)
    for presupuesto in dupe.presupuestos:
        presupuesto.obra = dest
        presupuesto.syncUpdate()
    # 2.- Pedidos (1 a m)
    for pedido in dupe.pedidosVenta:
        pedido.obra = dest
        pedido.syncUpdate()
    # 3.- Facturas (1 a m)
    for factura in dupe.facturasVenta:
        factura.obra = dest
        factura.syncUpdate()
    # 4.- Abonos (1 a m)
    for abono in dupe.abonos:
        abono.obra = dest
        abono.syncUpdate()
    # 5.- Contactos (n a m)
    for contacto in dupe.contactos:
        if contacto not in dest.contactos:
            dest.addContacto(contacto)
        dupe.removeContacto(contacto)
    # 6.- Clientes (n a m)
    for cliente in dupe.clientes:
        if cliente not in dest.clientes:
            dest.addCliente(cliente)
        dupe.removeCliente(cliente)
    # 7.- Y matarile al duplicado.
    dupe.destroy()  # Pasa por auditoría.
    # Devuelvo la obra que ha quedado viva y el PUID de la que he eliminado.
    return dest, puid_dupe

def report(cambiadas, unificadas):
    """
    Saca por pantalla un listado de nombres de obra corregidos y obras
    unificadas.
    """
    out = open("unificar_obras_duplicadas.txt", 'w')
    out.write("Nombres de obra corregidos\n")
    out.write("==========================\n")
    for anterior, nuevo in cambiadas:
        out.write("%s -> %s\n" % (anterior, nuevo.nombre))
    out.write("\n")
    out.write("%d nombres de obra cambiados.\n" % len(cambiadas))
    out.write("\n")
    out.write(("*" * 79) + "\n")
    out.write("\n")
    out.write("Obras unificadas\n")
    out.write("================\n")
    for obra in unificadas:
        out.write("%s (%d obras unificadas):\n" % (obra.nombre,
                                                   len(unificadas[obra])))
        out.write("\t%s <- (%s)\n" % (obra.puid, "; ".join(unificadas[obra])))
    out.write("\n")
    out.write("%d obras unificadas en total.\n" % sum(
        [len(unificadas[o]) for o in unificadas]))
    out.close()
    out = open("unificar_obras_duplicadas.txt", "r")
    for linea in out.readlines():
        print linea,
    out.close()

def main():
    """
    Busca conjuntos de obras duplicadas y las unifica según su nombre.
    Aprovecho para corregir también nombres con retornos de carro, etc.
    """
    cambiadas = corregir_nombres_obra()
    unificadas = defaultdict(lambda: [])
    obras = load_obras_duplicadas()
    total = sum([len(obras[nombre]) for nombre in obras])
    suffix = '%(index)d/%(max)d [%(elapsed_td)s/%(eta_td)s]'
    barra = IncrementalBar('Unificando obras...', max=total, suffix=suffix)
    for nombreobra in obras:
        try:
            # Si hay alguna genérica, la tomo como destino.
            obradest = [obra for obra in obras[nombreobra] if obra.generica][0]
        except IndexError:
            # Elijo la primera arbitrariamente como destino.
            obradest = obras[nombreobra][0]
        barra.next()
        for obra in obras[nombreobra]:
            if obra != obradest:
                dest, puid_deleted = unificar_obras(obradest, obra)
                unificadas[dest].append(puid_deleted)
                barra.next()
    barra.finish()
    report(cambiadas, unificadas)


if __name__ == "__main__":
    main()

