#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pruebas de exportación de ginn e importación en Murano.
"""

from __future__ import print_function

import sys
import os
import logging
import argparse
LOGFILENAME = "%s.log" % (".".join(os.path.basename(__file__).split(".")[:-1]))
logging.basicConfig(filename=LOGFILENAME,
                    format="%(asctime)s %(levelname)-8s : %(message)s",
                    level=logging.DEBUG)
# Desde el framework se hacen algunas cosas sucias con los argumentos,
# así que tengo que hacer una importación limpia a posteriori.
# pylint: disable=invalid-name
_argv, sys.argv = sys.argv, []
ruta_ginn = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "ginn"))
sys.path.append(ruta_ginn)
# pylint: disable=import-error,wrong-import-position
from framework import pclases
from api import murano
from lib.tqdm.tqdm import tqdm  # Barra de progreso modo texto.
sys.argv = _argv

ERRCODENOTFOUND = 1
ERRCODENOTIMPLEMENTED = 2
ERRFILENOTFOUND = 3


def prueba_bala(codigo=None):
    """
    Inserta la bala del código recibido o la última del sistema si es None.
    """
    if not codigo:
        b = pclases.Bala.select(orderBy="-id")[0]
    else:
        try:
            b = pclases.Bala.selectBy(codigo=codigo)[0]
        except IndexError:  # Debe ser una bala de cable (serie Z).
            b = pclases.BalaCable.selectBy(codigo=codigo)[0]
    logging.info("Insertando bala %s (%s) [%s]...", b.codigo,
                 b.articulo.productoVenta.descripcion, b.puid)
    murano.create_bala(b)
    if hasattr(b, "parteDeProduccion") and b.articulo.parteDeProduccion:
        # TODO: PORASQUI. ¿Se podría calcular la parte proporcional, o es
        # demasiado para unas pruebas?
        logging.warning(
            "WARNING: Considerando consumos del parte de producción completo.")
        for c in b.articulo.parteDeProduccion.consumos:
            if c.silo:
                logging.info("Consumiendo %f de %s (%s)...", c.cantidad,
                             c.productoCompra.descripcion,
                             c.silo.nombre)
            else:
                logging.info("Consumiendo %f de %s...", c.cantidad,
                             c.productoCompra.descripcion)
            murano.consumir(c.productoCompra, c.cantidad, consumo=c)


def prueba_rollo(codigo=None):
    """
    Si no se especifica, manda el último rollo (A) fabricado.
    """
    if not codigo:
        r = pclases.Rollo.select(orderBy="-id")[0]
    else:
        try:
            r = pclases.Rollo.selectBy(codigo=codigo)[0]
        except IndexError:  # Será un rollo B entonces.
            try:
                r = pclases.RolloDefectuoso.selectBy(codigo=codigo)[0]
            except IndexError:  # Es un rollo C. No queda otra.
                r = pclases.RolloC.selectBy(codigo=codigo)[0]
    logging.info("Insertando rollo %s (%s) [%s]...", r.codigo,
                 r.articulo.productoVenta.descripcion, r.puid)
    murano.create_rollo(r)
    if r.articulo.parteDeProduccion:
        logging.warning(
            "WARNING: Considerando consumos del parte de producción completo.")
        for c in r.articulo.parteDeProduccion.consumos:
            logging.info("Consumiendo %f de %s...", c.cantidad,
                         c.productoCompra.descripcion)
            murano.consumir(c.productoCompra, c.cantidad)
        # Para probar, consumiré la partida de carga completa:
        if r.articulo.parteDeProduccion.partidaCarga:
            for b in r.articulo.parteDeProduccion.partidaCarga.balas:
                # El almacén donde estaba la bala **antes** de consumirla está
                # en Murano. En ginn el almacén es None. Confiamos en Murano
                # (mediante la función delete_articulo del módulo murano)
                # para buscar e indicar de qué almacén debe consumir la bala.
                # Sería muy complicado (y más lento) determinarlo en ginn antes
                # de lanzar el consumo a la pasarela.
                logging.info("Consumiendo %s (%s)...", b.codigo, b.puid)
                murano.delete_articulo(b.articulo)


def prueba_pale(codigo=None):
    """
    Inserta el último palé o el del código recibido.
    """
    if not codigo:
        p = pclases.Pale.select(orderBy="-id")[0]
    else:
        p = pclases.Pale.selectBy(codigo=codigo)[0]
    logging.info("Insertando pale %s (%s) [%s]...", p.codigo,
                 p.productoVenta.descripcion, p.puid)
    murano.create_pale(p)
    if p.parteDeProduccion:
        logging.warning(
            "WARNING: Considerando consumos del parte de producción completo.")
        for c in p.parteDeProduccion.consumos:
            logging.info("Consumiendo %f de %s...", c.cantidad,
                         c.productoCompra.descripcion)
            murano.consumir(c.productoCompra, c.cantidad)
        # Consumo los bigbags de fibra empleados en rellenar las bolsas
        for bb in p.parteDeProduccion.bigbags:
            logging.info("Consumiendo %s (%s)...", bb.codigo, bb.puid)
            murano.delete_articulo(bb.articulo)


def prueba_bigbag(codigo=None):
    """
    Inserta el último bigbag del sistema o el del código recibido.
    """
    if not codigo:
        bb = pclases.Bigbag.select(orderBy="-id")[0]
    else:
        bb = pclases.Bigbag.selectBy(codigo=codigo)[0]
    logging.info("Insertando bigbag %s (%s) [%s]...", bb.codigo,
                 bb.articulo.productoVenta.descripcion, bb.puid)
    murano.create_bigbag(bb)
    if bb.articulo.parteDeProduccion:
        logging.warning(
            "WARNING: Considerando consumos del parte de producción completo.")
        for c in bb.articulo.parteDeProduccion.consumos:
            if c.silo:
                logging.info("Consumiendo %f de %s (%s)...", c.cantidad,
                             c.productoCompra.descripcion, c.silo.nombre)
            else:
                logging.info("Consumiendo %f de %s...", c.cantidad,
                             c.productoCompra.descripcion)
            murano.consumir(c.productoCompra, c.cantidad, consumo=c)
    # Los partes de reembolsado se ignoran. Solo la fibra fabricada
    # directamente para almacenar en bigbags en lugar de en balas.


def check_seguir():
    """
    Devuelve True si el usuario responde «S». False con cualquier otra cosa.
    """
    try:
        # pylint: disable=redefined-builtin
        input = raw_input
    except NameError:
        pass
    res = input("¿Continuar? (S/[N]): ").upper().startswith("S")
    return res


def prueba_codigo(codigo, consumir=False):
    """
    Inserta el código recibido sea del producto que sea.
    """
    # pylint: disable=too-many-branches
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
            try:
                objeto = clase_pclases.selectBy(codigo=codigo)[0]
            except IndexError:
                logging.error("El código %s no se encuentra en ginn.", codigo)
                objeto = None
            else:
                prueba_objeto(objeto, consumir)
    if not objeto:
        if codigo.startswith(pclases.PREFIJO_BOLSA):
            print("Código de bolsa detectado. Debe insertar al menos una "
                  "caja completa de bolsas.")
            if not check_seguir():
                sys.exit(ERRCODENOTIMPLEMENTED)
        elif codigo.startswith(pclases.PREFIJO_PARTIDACEM):
            print("Código de partida de cemento detectado. No soportado.")
            if not check_seguir():
                sys.exit(ERRCODENOTIMPLEMENTED)
        elif codigo.startswith(pclases.PREFIJO_LOTECEM):
            print("Código de lote de cemento detectado. No soportado.")
            if not check_seguir():
                sys.exit(ERRCODENOTIMPLEMENTED)
        elif codigo.startswith(pclases.PREFIJO_LOTE):
            print("Código de lote de fibra detectado. No soportado.")
            if not check_seguir():
                sys.exit(ERRCODENOTIMPLEMENTED)
        elif codigo.startswith(pclases.PREFIJO_PARTIDA):
            print("Código de partida de geotextiles detectado. No soportado.")
            if not check_seguir():
                sys.exit(ERRCODENOTIMPLEMENTED)
        elif codigo.startswith(pclases.PREFIJO_PARTIDACARGA):
            print("Código de partida de carga detectado. No soportado.")
            if not check_seguir():
                sys.exit(ERRCODENOTIMPLEMENTED)
        else:
            print("El código %s es incorrecto." % (codigo))
            if not check_seguir():
                sys.exit(ERRCODENOTFOUND)


def prueba_objeto(objeto, consumir=False):
    """
    Inserta el objeto recibido, sea del tipo de producto que sea.
    """
    # pylint: disable=too-many-branches
    if isinstance(objeto, (pclases.Rollo,
                           pclases.RolloDefectuoso,
                           pclases.RolloC)):
        if not consumir:
            logging.info("Insertando rollo %s (%s)...", objeto.codigo,
                         objeto.puid)
            murano.create_rollo(objeto)
        else:
            prueba_rollo(objeto.codigo)
    elif isinstance(objeto, (pclases.Bala,
                             pclases.BalaCable)):
        if not consumir:
            logging.info("Insertando bala %s (%s)...", objeto.codigo,
                         objeto.puid)
            murano.create_bala(objeto)
        else:
            prueba_bala(objeto.codigo)
    elif isinstance(objeto, pclases.Bigbag):
        if not consumir:
            logging.info("Insertando bigbag %s (%s)...", objeto.codigo,
                         objeto.puid)
            murano.create_bigbag(objeto)
        else:
            prueba_bigbag(objeto.codigo)
    elif isinstance(objeto, pclases.Caja):
        if not consumir:
            logging.info("Insertando caja %s (%s)...", objeto.codigo,
                         objeto.puid)
            murano.create_caja(objeto)
        else:
            raise NotImplementedError("No se permite la creación de cajas "
                                      "sueltas con consumo. Se debe insertar"
                                      " el palé completo.")
            # prueba_caja(objeto.codigo)
    elif isinstance(objeto, pclases.Pale):
        if not consumir:
            logging.info("Insertando palé %s (%s)...", objeto.codigo,
                         objeto.puid)
            murano.create_pale(objeto)
        else:
            prueba_pale(objeto.codigo)
    else:
        raise NotImplementedError("%s no soportado" % (objeto.puid))


def parse_file(fsource):
    """
    Función generadora. Lee los códigos a insertar de un fichero de texto.
    Devuelve un código en cada iteración.
    """
    try:
        f = open(fsource)
    except IOError:
        print("El fichero %s no existe." % (fsource))
        sys.exit(ERRFILENOTFOUND)
    else:
        for l in f.readlines():
            for codigo in l.strip().upper().split():
                if codigo == "#":   # Comentario. Ignoro el resto de la línea
                    break
                else:
                    yield codigo
    f.close()


def file_len(fsource):
    """
    Devuelve el número de códigos del fichero fuente.
    """
    res = 0
    # pylint:disable=unused-variable
    for codigo in parse_file(fsource):
        res += 1
    return res


def main():
    """
    Rutina principal.
    """
    # pylint: disable=too-many-branches
    # # Parámetros
    parser = argparse.ArgumentParser(
        description="Pruebas de movimientos de stock en Murano.")
    parser.add_argument("-b", "--balas", dest="balas",
                        help="Inserta las últimas n balas y sus consumos.",
                        default=0, type=int)
    parser.add_argument("-r", "--rollos", dest="rollos",
                        help="Inserta los últimos n rollos y sus consumos.",
                        default=0, type=int)
    parser.add_argument("-c", "--cajas", dest="cajas",
                        help="Inserta los últimos n palés y sus consumos.",
                        default=0, type=int)
    parser.add_argument("-g", "--bigbags", dest="bigbags",
                        help="Inserta los últimos n bigbags y sus consumos.",
                        default=0, type=int)
    parser.add_argument("-o", "--codigo", dest="codigo", nargs="+",
                        help="Especifica el código del artículo a insertar. "
                        "**No tiene en cuenta los consumos.**",
                        default=None, type=str)
    parser.add_argument("-f", "--file_source", dest="file_source",
                        help="Lee los códigos a insertar desde un fichero de"
                             " texto."
                             "**Realiza también los consumos relacionados.**",
                        type=str)
    if len(sys.argv) == 1:
        parser.print_help()
    args = parser.parse_args()
    # # Pruebas
    if args.balas:
        balas = pclases.Bala.select(orderBy="-id")
        for bala in balas.limit(args.balas):
            prueba_bala(bala.codigo)
    if args.rollos:
        rollos = pclases.Rollo.select(orderBy="-id")
        for rollo in rollos.limit(args.rollos):
            prueba_rollo(rollo.codigo)
    if args.cajas:
        pales = pclases.Pale.select(orderBy="-id")
        for pale in pales.limit(args.cajas):
            prueba_pale(pale.codigo)
    if args.bigbags:
        bigbags = pclases.Bigbag.select(orderBy="-id")
        for bigbag in bigbags.limit(args.bigbags):
            prueba_bigbag(bigbag.codigo)
    if args.codigo:
        pbar = tqdm(args.codigo)
        for codigo in pbar:
            pbar.set_description("Insertando sin consumos %s" % (codigo))
            prueba_codigo(codigo)
    if args.file_source:
        pbar = tqdm(parse_file(args.file_source),
                    total=file_len(args.file_source))
        for codigo in pbar:
            pbar.set_description("Insertando con consumos %s" % (codigo))
            prueba_codigo(codigo, consumir=True)


if __name__ == "__main__":
    main()
