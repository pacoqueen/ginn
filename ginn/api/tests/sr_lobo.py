#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
> Soy el Sr. Lobo. Soluciono problemas.

Realiza comprobaciones para detectar si hay discrepancias entre Murano y ginn.
- Si existen los mismos artículos y sus:
    - Pesos bruto
    - Pesos neto
    - Superficies
    - Valor campo api
- Si existen los mismos productos de venta y:
    - Si sus campos son idénticos.
    - Si falta algún dato obligatorio para ginn en Murano.
- Si existen los mismos productos de compra y si sus campos sin idénticos.
"""

from __future__ import print_function
import datetime
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


# pylint: disable=too-many-branches
def sync_articulo(codigo, fsalida, simulate=True):
    """
    Sincroniza el artículo de ginn cuyo código es "codigo", con el de
    Murano. Los datos de producción son los correctos, de modo que detecta y
    corrige los valores en Murano para dejarlos como en ginn:
    - Peso bruto
    - Peso neto
    - Superficie
    - Valor campo api
    """
    report = open(fsalida, "a")
    if simulate:
        report.write("Simulando sincronización de artículo %s..." % codigo)
    else:
        report.write("Sincronizando artículo %s..." % codigo)
    articulo = pclases.Articulo.get_articulo(codigo)
    if articulo:
        if not murano.ops.existe_articulo(articulo):
            report.write("Creando...")
            if not simulate:
                res = murano.ops.create_articulo(articulo)
            else:
                res = True
        else:
            peso_bruto = articulo.peso_bruto
            peso_neto = articulo.peso_neto
            superficie = articulo.superficie
            # pylint: disable=protected-access
            if (murano.ops._get_peso_bruto_murano(articulo) != peso_bruto or
                    murano.ops._get_peso_neto_murano(articulo) != peso_neto or
                    murano.ops._get_superficie(articulo) != superficie):
                report.write("Corrigiendo dimensiones ({}, {}, {})...".format(
                    peso_bruto, peso_neto, superficie))
                if not simulate:
                    res = murano.ops.corregir_dimensiones_articulo(articulo,
                                                                   peso_bruto,
                                                                   peso_neto,
                                                                   superficie)
                else:
                    res = True
            else:
                report.write("Nada que hacer.")
                res = True
        if not articulo.api:
            report.write("Actualizando valor api...")
            if not simulate:
                articulo.api = murano.ops.existe_articulo(articulo)
                articulo.syncUpdate()
                res = articulo.api
            else:
                res = True
    else:
        report.write("Artículo no encontrado en ginn.")
        res = False
    if res:
        report.write(" [OK]\n")
    else:
        report.write(" [KO]\n")
    report.close()
    return res


def sync_producto(codigo, fsalida, simulate=True):
    """
    Sincroniza el producto de compra o venta del código recibido con el
    equivalente en ginn.
    Si en ginn no existe, lo crea.
    Si existe, actualiza sus valores con los valores no nulos de Murano.
    Comprueba también que los valores obligatorios para producción en ginn
    están informados en Murano (modelo etiqueta, gramaje, bolsas por caja...)
    """
    res = True
    report = open(fsalida, "a")
    if simulate:
        report.write("Simulando sincronización de producto %s..." % codigo)
    else:
        report.write("Sincronizando producto %s..." % codigo)
    # 0.- ¿Existe el producto?
    try:
        producto_ginn = murano.ops.get_producto_ginn(codigo)
    except pclases.SQLObjectNotFound:
        report.write("No encontrado. Creando...")
        # Ya hemos comprobado que no existe, pero por si acaso, prefiero que
        # salta una excepción antes de machacar nada... de momento.
        res = murano.ops.producto_murano2ginn(codigo, sync=False)
    else:
        # 1.- Actualizo campos conforme a lo que indica Murano.
        res = murano.ops.producto_murano2ginn(codigo, sync=True)
        # 2.- Compruebo que los valores obligatorios están "informados".
        producto_ginn.sync()    # Por si ha cambiado algo.
        if isinstance(producto_ginn, pclases.ProductoVenta):
            campos_incorrectos = check_campos_obligatorios(producto_ginn)
            for campo in campos_incorrectos:
                report.write(" !{}".format(campo))
            res = not campos_incorrectos
        else:
            # Los productos de compra no tienen campos obligatorios que
            # afeten a producción.
            res = True
    if res:
        report.write(" [OK]\n")
    else:
        report.write(" [KO]\n")
    report.close()
    return res


def check_campos_obligatorios(producto):
    """
    Devuelve False si alguno de los campos obligatorios para fabricar en ginn
    no tiene un valor correcto.
    """
    res = []
    cer = producto.camposEspecificosRollo
    ceb = producto.camposEspecificosBala
    # Campos a chequear si son rollos o balas.
    campos = {cer: ('modeloEtiqueta', 'gramos', 'ancho', 'pesoEmbalaje'),
              ceb: ['dtex', 'corte', 'color']}
    # En la fibra de cemento hay que comprobar alguno más:
    if producto.es_caja():
        campos[ceb] += ['gramosBolsa', 'bolsasCaja', 'cajasPale']
    for indirecto in campos:
        if indirecto:
            campo = campos[indirecto]
            valor = getattr(producto, campo)
            if not valor:
                res.append(campo)
    return res


def check_everything(report):
    """
    Devuelve todos los códigos de artículos que hay en el almacén en ginn (eso
    incluye, por fuerza, todo lo fabricado después del 31 de mayo de 2016, que
    fue cuando se hizo la migración). Pero de todos modos devolverá también
    todos esos artículos por si alguien ha consumido balas en partidas de
    carga o ha hecho un albarán de salida por lo que sea.
    Devuelve también todos los códigos de productos **de Murano**, que es
    donde se mantienen. Así comprobará después que en ginn existen y tienen la
    misma información.
    """
    # Sync artículos. ginn => Murano
    fini = datetime.datetime(
        2016, 5, 31, 17, 30) - datetime.timedelta(hours=17.5)
    report.write("Buscando todos los artículos...")
    # pylint: disable=bad-continuation
    articulos = pclases.Articulo.select(pclases.OR(     # NOQA
        pclases.Articulo.q.almacen != None,
        pclases.AND(pclases.Articulo.q.parteDeProduccionID ==
                        pclases.ParteDeProduccion.q.id,
                    pclases.ParteDeProduccion.q.fechahorainicio >= fini)))
    report.write("{} encontrados. Ordenando...\n".format(articulos.count()))
    codigos_articulos = [a.codigo for a in articulos]
    codigos_articulos.sort()
    # Sync productos de compra y venta. ginn <= Murano
    report.write("Buscando todos los productos de venta...")
    conn = murano.connection.Connection()
    productos = conn.run_sql(r"""SELECT CodigoArticulo FROM %s.dbo.Articulos
        WHERE CodigoArticulo LIKE 'P%';""" % (conn.get_database(),
                                              murano.connection.CODEMPRESA))
    codigos_productos = [r['CodigoArticulo'] for r in productos]
    report.write("{} encontrados.\n".format(len(codigos_productos)))
    return codigos_articulos, codigos_productos


def main():
    """
    Rutina principal.
    """
    # pylint: disable=too-many-branches
    # # Parámetros
    parser = argparse.ArgumentParser(
        description="Soy el Sr. Lobo. Soluciono problemas.")
    parser.add_argument("-a", "--articulos", dest="codigos_articulos",
                        help="Códigos de artículos a comprobar.",
                        nargs="+", default=[])
    parser.add_argument("-p", "--productos", dest="codigos_productos",
                        help="Códigos de productos a comprobar.",
                        nargs="+", default=[])
    parser.add_argument("-n", "--dry-run", dest="simulate",
                        help="Simular. No hace cambios en la base de datos.",
                        default=False, action='store_true')
    ahora = datetime.datetime.today().strftime("%Y%m%d_%H%M%S")
    parser.add_argument("-o", dest="fsalida",
                        help="Guardar resultados en fichero de salida.",
                        default="%s_sr_lobo.txt" % (ahora))
    args = parser.parse_args()
    if not args.codigos_articulos and not args.codigos_productos:
        # Si no recibo argumentos, compruebo todos los artículos y productos.
        args.codigos_articulos, args.codigos_productos = check_everything(
            args.fsalida)
    # # Pruebas
    if args.codigos_articulos:
        for codigo in tqdm(args.codigos_articulos):
            sync_articulo(codigo, args.fsalida, args.simulate)
    if args.codigos_productos:
        for codigo in tqdm(args.codigos_productos):
            sync_producto(codigo, args.fsalida, args.simulate)


if __name__ == "__main__":
    main()
