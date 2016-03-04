#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

ERRCODENOTFOUND = 1
ERRCODENOTIMPLEMENTED = 2

import argparse
import sys, os
# Desde el framework se hacen algunas cosas sucias con los argumentos,
# así que tengo que hacer una importación limpia a posteriori.
_argv, sys.argv = sys.argv, []
ruta_ginn = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "ginn"))
sys.path.append(ruta_ginn)
from framework import pclases
from api import murano
sys.argv = _argv

def prueba_bala(codigo = None):
    if not codigo:
        b = pclases.Bala.select(orderBy = "-id")[0]
    else:
        b = pclases.Bala.selectBy(codigo = codigo)[0]
    print("Insertando bala %s (%s) [%s]..." % (b.codigo,
        b.articulo.productoVenta.descripcion,
        b.puid))
    murano.create_bala(b)
    for c in b.articulo.parteDeProduccion.consumos:
        if c.silo:
            print("Consumiendo %f de %s (%s)..." % (c.cantidad,
                c.productoCompra.descripcion,
                c.silo.nombre))
        else:
            print("Consumiendo %f de %s..." % (c.cantidad,
                                               c.productoCompra.descripcion))
        murano.consumir(c.productoCompra, c.cantidad, consumo = c)

def prueba_rollo(codigo = None):
    if not codigo:
        r = pclases.Rollo.select(orderBy = "-id")[0]
    else:
        r = pclases.Rollo.selectBy(codigo = codigo)[0]
    print("Insertando rollo %s (%s) [%s]..." % (r.codigo,
        r.articulo.productoVenta.descripcion,
        r.puid))
    murano.create_rollo(r)
    for c in r.articulo.parteDeProduccion.consumos:
        print("Consumiendo %f de %s..." % (c.cantidad,
                                           c.productoCompra.descripcion))
        murano.consumir(c.productoCompra, c.cantidad)
    # Para probar, consumiré la partida de carga completa:
    if r.articulo.parteDeProduccion.partidaCarga:
        for b in r.articulo.parteDeProduccion.partidaCarga.balas:
            # El almacén donde estaba la bala **antes** de consumirla está 
            # en Murano. En ginn el almacén es None. Confiamos en Murano
            # (mediante la función delete_articulo del módulo murano)
            # para buscar e indicar de qué almacén debe consumir la bala. Sería
            # muy complicado (y más lento) determinarlo en ginn antes de lanzar
            # el consumo a la pasarela.
            print("Consumiendo %s (%s)..." % (b.codigo, b.puid))
            murano.delete_articulo(b.articulo)

def prueba_pale(codigo = None):
    if not codigo:
        p = pclases.Pale.select(orderBy = "-id")[0]
    else:
        p = pclases.Pale.selectBy(codigo = codigo)[0]
    print("Insertando pale %s (%s) [%s]..." % (p.codigo,
        p.productoVenta.descripcion,
        p.puid))
    murano.create_pale(p)
    for c in p.parteDeProduccion.consumos:
        print("Consumiendo %f de %s..." % (c.cantidad,
                                           c.productoCompra.descripcion))
        murano.consumir(c.productoCompra, c.cantidad)
    # Consumo los bigbags de fibra empleados en rellenar las bolsas
    for bb in p.parteDeProduccion.bigbags:
        print("Consumiendo %s (%s)..." % (bb.codigo, bb.puid))
        murano.delete_articulo(bb.articulo)

def prueba_bigbag(codigo = None):
    if not codigo:
        bb = pclases.Bigbag.select(orderBy = "-id")[0]
    else:
        bb = pclases.Bigbag.selectBy(codigo = codigo)[0]
    print("Insertando bigbag %s (%s) [%s]..." % (bb.codigo,
        bb.articulo.productoVenta.descripcion,
        bb.puid))
    murano.create_bigbag(bb)
    for c in bb.articulo.parteDeProduccion.consumos:
        if c.silo:
            print("Consumiendo %f de %s (%s)..." % (c.cantidad,
                c.productoCompra.descripcion,
                c.silo.nombre))
        else:
            print("Consumiendo %f de %s..." % (c.cantidad,
                                               c.productoCompra.descripcion))
        murano.consumir(c.productoCompra, c.cantidad, consumo = c)
    # Los partes de reembolsado se ignoran. Solo la fibra fabricada
    # directamente para almacenar en bigbags en lugar de en balas.

def prueba_codigo(codigo):
    mapping = {pclases.PREFIJO_ROLLO: pclases.Rollo,
               pclases.PREFIJO_BALA: pclases.Bala,
               pclases.PREFIJO_BIGBAG: pclases.Bigbag,
               pclases.PREFIJO_PALE: pclases.Pale,
               pclases.PREFIJO_CAJA: pclases.Caja,
               pclases.PREFIJO_BALACABLE: pclases.BalaCable,
               pclases.PREFIJO_ROLLOC: pclases.RolloC,
               pclases.PREFIJO_ROLLODEFECTUOSO: pclases.RolloDefectuoso}
    objeto = None
    for prefijo in mapping:
        if codigo.startswith(prefijo):
            clase_pclases = mapping[prefijo]
            objeto = clase_pclases.selectBy(codigo = codigo)[0]
            prueba_objeto(objeto)
    if not objeto:
        if codigo.startswith(pclases.PREFIJO_BOLSA):
            print("Código de bolsa detectado. Debe insertar al menos una "
                  "caja completa de bolsas.")
            sys.exit(ERRCODENOTIMPLEMENTED)
        elif codigo.startswith(pclases.PREFIJO_PARTIDACEM):
            print("Código de partida de cemento detectado. No soportado.")
            sys.exit(ERRCODENOTIMPLEMENTED)
        elif codigo.startswith(pclases.PREFIJO_LOTECEM):
            print("Código de lote de cemento detectado. No soportado.")
            sys.exit(ERRCODENOTIMPLEMENTED)
        elif codigo.startswith(pclases.PREFIJO_LOTE):
            print("Código de lote de fibra detectado. No soportado.")
            sys.exit(ERRCODENOTIMPLEMENTED)
        elif codigo.startswith(pclases.PREFIJO_PARTIDA):
            print("Código de partida de geotextiles detectado. No soportado.")
            sys.exit(ERRCODENOTIMPLEMENTED)
        elif codigo.startswith(pclases.PREFIJO_PARTIDACARGA):
            print("Código de partida de carga detectado. No soportado.")
            sys.exit(ERRCODENOTIMPLEMENTED)
        else:
            print("El código %s no se reconoce.")
            sys.exit(ERRCODENOTFOUND)

def prueba_objeto(objeto):
    if isinstance(objeto, (pclases.Rollo,
                           pclases.RolloDefectuoso,
                           pclases.RolloC)):
        murano.create_rollo(objeto)
    elif isinstance(objeto, (pclases.Bala,
                             pclases.BalaCable)):
        murano.create_bala(objeto)
    elif isinstance(objeto, pclases.Bigbag):
        murano.create_bigbag(objeto)
    elif isinstance(objeto, pclases.Caja):
        murano.create_caja(objeto)
    elif isinstance(objeto, pclases.Pale):
        murano.create_pale(objeto)
    else:
        raise NotImplementedError, "%s no soportado" % (objeto.puid)

def main():
    ## Parámetros
    parser = argparse.ArgumentParser(
            description = "Pruebas de movimientos de stock en Murano.")
    parser.add_argument("-b", "--balas", dest = "balas",
            help = "Inserta las últimas n balas y sus consumos.",
            default = 0, type = int)
    parser.add_argument("-r", "--rollos", dest = "rollos",
            help = "Inserta los últimos n rollos y sus consumos.",
            default = 0, type = int)
    parser.add_argument("-c", "--cajas", dest ="cajas",
            help = "Inserta los últimos n palés y sus consumos.",
            default = 0, type = int)
    parser.add_argument("-g", "--bigbags", dest = "bigbags",
            help = "Inserta los últimos n bigbags y sus consumos.",
            default = 0, type = int)
    parser.add_argument("-o", "--codigo", dest = "codigo",
            help = "Especifica el código del artículo a insertar. "
                   "**No tiene en cuenta los consumos relacionados.**",
            default = None, type = str)
    if len(sys.argv) == 1:
        parser.print_help()
    args = parser.parse_args()
    ## Pruebas
    if args.balas:
        balas = pclases.Bala.select(orderBy = "-id")
        for bala in balas.limit(args.balas):
            prueba_bala(bala.codigo)
    if args.rollos:
        rollos = pclases.Rollo.select(orderBy = "-id")
        for rollo in rollos.limit(args.rollos):
            prueba_rollo(rollo.codigo)
    if args.cajas:
        pales = pclases.Pale.select(orderBy = "-id")
        for pale in pales.limit(args.cajas):
            prueba_pale(pale.codigo)
    if args.bigbags:
        bigbags = pclases.Bigbag.select(orderBy = "-id")
        for bigbag in bigbags.limit(args.bigbags):
            prueba_bigbag(bigbag.codigo)
    if args.codigo:
        prueba_codigo(args.codigo)

if __name__ == "__main__":
    main()
