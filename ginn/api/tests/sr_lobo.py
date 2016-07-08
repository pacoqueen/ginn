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
import subprocess
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


# pylint: disable=too-many-branches,too-many-statements
def sync_articulo(codigo, fsalida, simulate=True):
    """
    Sincroniza el artículo de ginn cuyo código es "codigo", con el de
    Murano. Los datos de producción son los correctos, de modo que detecta y
    corrige los valores en Murano para dejarlos como en ginn:
    - Peso bruto
    - Peso neto
    - Superficie
    - Valor campo api
    - Código palé
    """
    report = open(fsalida, "a", 0)
    if simulate:
        report.write("Simulando sincronización de artículo %s... " % codigo)
    else:
        report.write("Sincronizando artículo %s... " % codigo)
    articulo = pclases.Articulo.get_articulo(codigo)
    if articulo:
        if not murano.ops.existe_articulo(articulo):
            report.write("Creando... ")
            if not simulate:
                res = murano.ops.create_articulo(articulo)
            else:
                res = True
        else:
            altered = False
            peso_bruto = articulo.peso_bruto
            peso_neto = articulo.peso_neto
            superficie = articulo.superficie
            if superficie is None:
                superficie = 0.0    # Es como lo devuelve Murano. Como float.
            # pylint: disable=protected-access
            (peso_bruto_murano,
             peso_neto_murano,
             superficie_murano) = murano.ops._get_dimensiones_murano(articulo)
            if (peso_bruto_murano != peso_bruto or
                    peso_neto_murano != peso_neto or
                    superficie_murano != superficie):
                report.write("Corrigiendo dimensiones ({} -> {}, {} -> {},"
                             " {} -> {})... ".format(peso_bruto_murano,
                                                     peso_bruto,
                                                     peso_neto_murano,
                                                     peso_neto,
                                                     superficie_murano,
                                                     superficie))
                altered = True
                if not simulate:
                    res = murano.ops.corregir_dimensiones_articulo(articulo,
                                                                   peso_bruto,
                                                                   peso_neto,
                                                                   superficie)
                else:
                    res = True
            if articulo.caja and articulo.caja.pale:
                pale_murano = murano.ops._get_codigo_pale(articulo)
                codigo_pale_ginn = articulo.caja.pale.codigo
                if pale_murano != codigo_pale_ginn:
                    report.write("Corrigiendo palé "
                                 "({} -> {})...".format(pale_murano,
                                                        codigo_pale_ginn))
                    altered = True
                    if not simulate:
                        res = murano.ops.corregir_pale(articulo)
                    else:
                        res = True
            if not altered:
                report.write("Nada que hacer.")
                res = True
        if not articulo.api:
            report.write("Actualizando valor api... ")
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
    report = open(fsalida, "a", 0)
    if simulate:
        report.write("Simulando sincronización de producto %s... " % codigo)
    else:
        report.write("Sincronizando producto %s... " % codigo)
    # 0.- ¿Existe el producto?
    try:
        producto_ginn = murano.ops.get_producto_ginn(codigo)
    except pclases.SQLObjectNotFound:
        report.write("No encontrado. Creando... ")
        # Ya hemos comprobado que no existe, pero por si acaso, prefiero que
        # salta una excepción antes de machacar nada... de momento.
        res = murano.ops.producto_murano2ginn(codigo, sync=False)
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


def check_everything(fsalida):
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
    report = open(fsalida, "a", 0)
    # Sync artículos. ginn => Murano
    fini = datetime.datetime(
        2016, 5, 31, 17, 30) - datetime.timedelta(hours=17.5)
    report.write("Buscando todos los artículos... ")
    # pylint: disable=bad-continuation
    articulos_en_almacen = pclases.Articulo.select(     # NOQA
        pclases.Articulo.q.almacen != None)
    partes_fabricacion = pclases.ParteDeProduccion.select(
        pclases.ParteDeProduccion.q.fechahorainicio >= fini)
    articulos = set(articulos_en_almacen)
    for pdp in partes_fabricacion:
        articulos.update(set(pdp.articulos))
    # Completo con balas y rollos C, que no tienen parte de producción:
    for bc in pclases.BalaCable.select(pclases.BalaCable.q.fechahora >= fini):
        articulos.add(bc.articulo)
    for rc in pclases.RolloC.select(pclases.RolloC.q.fechahora >= fini):
        articulos.add(rc.articulo)
    report.write("{} encontrados. Ordenando...\n".format(len(articulos)))
    codigos_articulos = [a.codigo for a in articulos]
    codigos_articulos.sort()
    # Sync productos de compra y venta. ginn <= Murano
    report.write("Buscando todos los productos de venta... ")
    conn = murano.connection.Connection()
    sql = "SELECT CodigoArticulo FROM {}.dbo.Articulos".format(
        conn.get_database())
    sql += " WHERE CodigoArticulo LIKE 'P%'"
    sql += " AND CodigoEmpresa = '{}';".format(murano.connection.CODEMPRESA)
    productos = conn.run_sql(sql)
    codigos_productos = [r['CodigoArticulo'] for r in productos]
    report.write("{} encontrados.\n".format(len(codigos_productos)))
    report.close()
    return codigos_articulos, codigos_productos


def finish_pendientes(fsalida, simulate=True):
    """
    Busca todos los registros de importaciones pendientes de procesar y las
    completa si simulate viene a False.
    """
    report = open(fsalida, "a", 0)
    conn = murano.connection.Connection()
    sql = """SELECT IdProcesoIME
             FROM {}.dbo.Iniciador_TmpIME
             WHERE FechaFin IS NULL;""".format(conn.get_database())
    guids = conn.run_sql(sql)
    report.write("{} procesos pendients encontrados.\n".format(len(guids)))
    for proceso in tqdm(guids):
        guid = proceso['IdProcesoIME']
        if not simulate:
            report.write("Procesando {}...".format(guid))
            res = murano.ops.fire(guid)
        else:
            report.write("Simulando {}...".format(guid))
            res = True
        if res:
            report.write(" [OK]\n")
        else:
            report.write(" [KO]\n")
    report.close()


def corregir_dimensiones_nulas(fsalida, simulate=True):
    """
    En lugar de buscar en ginn todos los artículos y recorrerlos para
    comprobarlos en Murano, buscamos en Murano los artículos mal traspasados
    y los corregimos según lo que tengan en ginn (más rápido).
    Este preproceso acelerará también los posteriores.
    """
    report = open(fsalida, "a", 0)
    conn = murano.connection.Connection()
    sqls = ("""SELECT CodigoArticulo, NumeroSerieLc,
                    PesoBruto_, PesoNeto_, MetrosCuadrados
              FROM {}.dbo.ArticulosSeries
             WHERE CodigoEmpresa = '{}'
               AND NumeroSerieLc LIKE 'B%'
               AND (PesoBruto_ = 0.0 OR PesoNeto_ = 0.0); -- Balas (A y B)
            """,
            """SELECT CodigoArticulo, NumeroSerieLc,
                    PesoBruto_, PesoNeto_, MetrosCuadrados
              FROM {}.dbo.ArticulosSeries
             WHERE CodigoEmpresa = '{}'
               AND NumeroSerieLc LIKE 'Z%'
               AND (PesoBruto_ = 0.0 OR PesoNeto_ = 0.0); -- Balas de cable (C)
            """,
            """SELECT CodigoArticulo, NumeroSerieLc,
                    PesoBruto_, PesoNeto_, MetrosCuadrados
              FROM {}.dbo.ArticulosSeries
             WHERE CodigoEmpresa = '{}'
               AND NumeroSerieLc LIKE 'C%'
               AND (PesoBruto_ = 0.0 OR PesoNeto_ = 0.0); -- Bigbag (A, B, C)
            """,
            """SELECT CodigoArticulo, NumeroSerieLc,
                    PesoBruto_, PesoNeto_, MetrosCuadrados, CodigoPale
              FROM {}.dbo.ArticulosSeries
             WHERE CodigoEmpresa = '{}'
               AND NumeroSerieLc LIKE 'J%'
               AND (PesoBruto_ = 0.0 OR PesoNeto_ = 0.0
                    OR CodigoPale = '');                  -- Cajas (A, B, C)
            """,
            """SELECT CodigoArticulo, NumeroSerieLc,
                    PesoBruto_, PesoNeto_, MetrosCuadrados
              FROM {}.dbo.ArticulosSeries
             WHERE CodigoEmpresa = '{}'
               AND NumeroSerieLc LIKE 'R%'
               AND (MetrosCuadrados = 0.0 OR PesoBruto_ = 0.0
                    OR PesoNeto_ = 0.0);                  -- Rollos (A)
            """,
            """SELECT CodigoArticulo, NumeroSerieLc,
                    PesoBruto_, PesoNeto_, MetrosCuadrados
              FROM {}.dbo.ArticulosSeries
             WHERE CodigoEmpresa = '{}'
               AND NumeroSerieLc LIKE 'X%'
               AND (MetrosCuadrados = 0.0 OR PesoBruto_ = 0.0
                    OR PesoNeto_ = 0.0);            -- Rollos defectuosos (B)
            """,
            """SELECT CodigoArticulo, NumeroSerieLc,
                    PesoBruto_, PesoNeto_, MetrosCuadrados
              FROM {}.dbo.ArticulosSeries
             WHERE CodigoEmpresa = '{}'
               AND NumeroSerieLc LIKE 'Y%'
               AND (PesoBruto_ = 0.0 OR PesoNeto_ = 0.0); -- Rollos C

             """)
    i = 1
    tot = len(sqls)
    res = True
    for sql in sqls:
        sql = sql.format(conn.get_database(), murano.connection.CODEMPRESA)
        codigos = conn.run_sql(sql)
        report.write("{}/{}: {} artículos encontrados:\n".format(i, tot,
                                                                 len(codigos)))
        for registro in tqdm(codigos):
            codigo = registro['NumeroSerieLc']
            res = sync_articulo(codigo, fsalida, simulate) and res
        i += 1
    report.close()
    return res


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
    ahora = datetime.datetime.today().strftime("%Y%m%d_%H")
    parser.add_argument("-o", dest="fsalida",
                        help="Guardar resultados en fichero de salida.",
                        default="%s_sr_lobo.txt" % (ahora))
    parser.add_argument("-v", "--view", dest="ver_salida",
                        help="Abre el fichero de salida en un editor externo.",
                        default=False, action='store_true')
    args = parser.parse_args()
    if args.ver_salida:
        subprocess.Popen('gvim "{}"'.format(args.fsalida))
    # Primero termino de procesar todas las posibles imortaciones pendientes:
    finish_pendientes(args.fsalida, args.simulate)
    # Y corrijo las posibles dimensiones nulas:
    corregir_dimensiones_nulas(args.fsalida, args.simulate)
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
