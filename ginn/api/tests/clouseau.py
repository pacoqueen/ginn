#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
El Inspector Jefe Jacques Clouseau es un torpe e incompetente inspector de la
Sûreté francesa, cuyas investigaciones siempre están marcadas por el caos, la
destrucción, los desastres y accidentes causados en gran medida por él mismo.

En esta versión 2.0 se va a encargar de seguir el rastro **bulto a bulto** de
todas las series generadas en ginn y su devenir en Murano, para ver finalmente
con todo el detalle posible de dónde viene una desviación.

La versión 1.0 (en Geotex-INN/extra/script) hacía básicamente lo mismo que
ramanujan, pero pero sin Murano.
"""

# pylint: disable=too-many-lines

from __future__ import print_function
import time
import datetime
import sys
import os
import subprocess
import logging
import argparse
try:
    import tablib
except ImportError:
    sys.stderr.write("Es necesario instalar tablib para leer las existencias"
                     " inciales: pip install tablib")
    sys.exit(1)
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
from api.murano import connection
# from api.murano.extra import get_peso_neto, get_superficie
from api.tests.ramanujan import find_fich_inventario, parse_fecha_xls
# from api.tests.ramanujan import load_inventario
from api.tests.ramanujan import get_articulos_consumidos_ginn
from api.tests.ramanujan import get_registros_movimientoarticuloserie
from api.tests.ramanujan import query_articulos_from_partes
from lib.tqdm.tqdm import tqdm  # Barra de progreso modo texto.
sys.argv = _argv


# pylint: disable=too-many-arguments,too-many-locals,too-many-branches,too-many-statements
def investigar(producto_ginn, fini, ffin, report,
               data_res, dev=False):
    """
    Para ver qué series están provocado la desviación, coge los bultos
    iniciales y los producidos durante el periodo, y analiza uno por uno
    si han sido vendidos, consumidos, ajustados o siguen en almacén.
    Las producciones y los consumos los hace por partida doble: en ERP y
    en Murano. Así sabremos si la desviación está en la API.
    """
    res = True
    # 0.- Localizo los consumos y producciones por calidad.
    consumos_ginn = buscar_bultos_consumidos_ginn(producto_ginn, fini, ffin)
    consumos_murano = buscar_bultos_consumidos_murano(producto_ginn, fini, ffin)
    producciones_ginn = buscar_bultos_producidos_ginn(producto_ginn, fini, ffin)
    producciones_murano = buscar_bultos_producidos_murano(producto_ginn, fini,
                                                          ffin)
    # 1,- La investigasió
    ginn_no_murano = {"consumos": {}, "producción": {}}
    murano_no_ginn = {"consumos": {}, "producción": {}}
    # 1.1.- Los que están consumidos/fabricados en ginn pero no en Murano
    for dic_ginn, dic_murano, category in (
            (consumos_ginn, consumos_murano, "consumos"),
            (producciones_ginn, producciones_murano, "producción")):
        for calidad in dic_ginn:
            for articulo in dic_ginn[calidad]:
                if (calidad not in dic_murano
                        or articulo.codigo not in dic_murano[calidad]):
                    try:
                        ginn_no_murano[category][calidad].append(articulo.codigo)
                    except KeyError:
                        ginn_no_murano[category][calidad] = [articulo.codigo]
    # 1.2.- Los que se han consumido/fabricado en Murano pero no en ginn
        for calidad in dic_murano:
            for codigo in dic_murano[calidad]:
                if (calidad not in dic_ginn
                        or codigo not in [a.codigo for a in dic_ginn[calidad]]):
                    try:
                        murano_no_ginn[category][calidad].append(codigo)
                    except KeyError:
                        murano_no_ginn[category][calidad] = [codigo]
    # 2.- Cabecera del informe de resultados:
    if not dev:
        # pylint: disable=no-member
        try:
            producto_murano = murano.ops.get_producto_murano("PV{}".format(
                producto_ginn.id))
            report.write("{}: {}\n".format(producto_murano.CodigoArticulo,
                                           producto_ginn.descripcion))
        except AttributeError:
            report.write("{}: _({}) {}_\n".format(
                "***¡Producto no encontrado en Murano!***",
                producto_ginn.puid, producto_ginn.descripcion))
    else:
        report.write("PV{}: {}\n".format(producto_ginn.id,
                                         producto_ginn.descripcion))
    # 3.- Escribo los resultados al report.
    # 3.1.- Consumos en ginn no volcados a Murano.
    report.write("## Artículos consumidos en ginn pero no en Murano\n")
    for calidad in ginn_no_murano["consumos"]:
        report.write("### Calidad {}:\n".format(calidad))
        for codigo in ginn_no_murano["consumos"][calidad]:
            articulo = pclases.Articulo.get_articulo(codigo)
            if articulo.es_bala():
                parte_o_partidacarga = articulo.bala.partidaCarga.codigo
                fecha_consumo = articulo.bala.partidaCarga.fecha.strftime("%d/%m/%Y %H:%M")
            elif articulo.es_bigbag():
                bigbag = articulo.bigbag
                parte_o_partidacarga = bigbag.parteDeProduccion.id
                fecha_consumo = bigbag.parteDeProduccion.fechahorainicio.strftime(
                    "%d/%m/%Y %H:%M")
            else:
                parte_o_partidacarga = "¿?"
                fecha_consumo = "¿?"
            report.write(" * {} (Consumido el {} en {})\n".format(
                articulo.codigo, fecha_consumo, parte_o_partidacarga))
            # 5.- Guardo los resultados en el Dataset para exportarlos después.
            # ['Código', 'Producto', 'Serie', 'Calidad', 'Cons. ginn', 'Cons. Murano',
            #  'Prod. ginn', 'Prod. Murano', 'Bultos', 'm²', 'kg']
            data_res.append(['PV{}'.format(producto_ginn.id),
                             producto_ginn.descripcion,
                             articulo.codigo,
                             calidad,
                             "",
                             "",
                             fecha_consumo,
                             "",
                             1,
                             articulo.get_superficie(),
                             articulo.peso_neto
                            ])
    # 3.2.- Consumos en Murano pero no en ginn.
    report.write("## Artículos consumidos en Murano pero no en ginn\n")
    for calidad in murano_no_ginn["consumos"]:
        report.write("### Calidad {}:\n".format(calidad))
        for codigo in murano_no_ginn["consumos"][calidad]:
            # 5.- Guardo los resultados en el Dataset para exportarlos después.
            # ['Código', 'Producto', 'Serie', 'Calidad', 'Cons. ginn', 'Cons. Murano',
            #  'Prod. ginn', 'Prod. Murano', 'Bultos', 'm²', 'kg']
            articulo = pclases.Articulo.get_articulo(codigo)
            fecha_consumo = murano.ops.esta_consumido(articulo)
            if fecha_consumo:
                # pylint: disable=no-member
                fecha_consumo = fecha_consumo.strftime("%d/%m/%Y %H:%M")
            report.write(" * {} (Volcado como consumo el {})\n".format(codigo,
                                                                       fecha_consumo))
            # pylint: disable=protected-access
            superficie = murano.ops._get_superficie_murano(articulo)
            peso_neto = murano.ops._get_peso_neto_murano(articulo)
            if codigo not in data_res['Serie']:
                data_res.append(['PV{}'.format(producto_ginn.id),
                                 producto_ginn.descripcion,
                                 codigo,
                                 calidad,
                                 "",
                                 "",
                                 "",
                                 fecha_consumo,
                                 1,
                                 superficie,
                                 peso_neto
                                ])
            else:
                index = data_res['Serie'].index(codigo)
                row = list(data_res[index])
                row[7] = fecha_consumo
                row[9] = superficie
                row[10] = peso_neto
                data_res[index] = row
    # 3.3.- Producciones en ginn pero no en Murano.
    report.write("## Artículos fabricados en ginn pero sin alta en Murano "
                 "en el mismo periodo\n")
    for calidad in ginn_no_murano["producción"]:
        report.write("### Calidad {}:\n".format(calidad))
        for articulo in ginn_no_murano["producción"][calidad]:
            fecha_produccion = articulo.parteDeProduccion.fechahorainicio
            superficie = articulo.get_superficie()
            peso_neto = articulo.peso_neto
            report.write(" * {} (Fabricada el {} en el parte del {})\n".format(
                articulo.codigo, articulo.fechahora, fecha_produccion))
            if codigo not in data_res['Serie']:
                data_res.append(['PV{}'.format(producto_ginn.id),
                                 producto_ginn.descripcion,
                                 codigo,
                                 calidad,
                                 fecha_produccion.strftime("%d/%m/%Y %H:%M"),
                                 "",
                                 "",
                                 "",
                                 1,
                                 superficie,
                                 peso_neto
                                ])
            else:
                index = data_res['Serie'].index(codigo)
                row = list(data_res[index])
                row[4] = fecha_produccion.strftime("%d/%m/%Y %H:%M")
                row[9] = superficie
                row[10] = peso_neto
                data_res[index] = row
    # 3.4.- Producciones en Murano pero no en ginn.
    report.write("## Artículos con alta en Murano pero no fabricados en ginn\n")
    for calidad in murano_no_ginn["producción"]:
        report.write("### Calidad {}:\n".format(calidad))
        for codigo in murano_no_ginn["producción"][calidad]:
            articulo = pclases.Articulo.get_articulo(codigo)
            fecha_produccion = murano.ops.get_fecha_entrada(articulo)
            report.write(" * {} (Volcada como producción en Murano el {})"
                         "\n".format(codigo, fecha_produccion))
            # 5.- Guardo los resultados en el Dataset para exportarlos después.
            # ['Código', 'Producto', 'Serie', 'Calidad', 'Cons. ginn', 'Cons. Murano',
            #  'Prod. ginn', 'Prod. Murano', 'Bultos', 'm²', 'kg']
            # pylint: disable=protected-access
            superficie = murano.ops._get_superficie_murano(articulo)
            peso_neto = murano.ops._get_peso_neto_murano(articulo)
            if codigo not in data_res['Serie']:
                data_res.append(['PV{}'.format(producto_ginn.id),
                                 producto_ginn.descripcion,
                                 codigo,
                                 calidad,
                                 "",
                                 fecha_produccion.strftime("%d/%m/%Y %H:%M"),
                                 "",
                                 "",
                                 1,
                                 superficie,
                                 peso_neto
                                ])
            else:
                index = data_res['Serie'].index(codigo)
                row = list(data_res[index])
                row[5] = fecha_produccion.strftime("%d/%m/%Y %H:%M")
                row[9] = superficie
                row[10] = peso_neto
                data_res[index] = row
    # 3.5.- Fin del report para el producto.
    res = not ginn_no_murano and not murano_no_ginn
    report.write("-"*70)
    if res:
        report.write(" _[OK]_ \n")
    else:
        report.write(" **[KO]**\n")
    report.write("\n")
    # 6.- Y devuelvo si todo cuadra (True) o hay alguna desviación (False)
    return res


def buscar_bultos_consumidos_murano(producto_ginn, fini, ffin):
    """
    Busca todos los números de serie consumidos del producto según Murano.
    Los devuelve agrupados por calidad y solo devuelve el código de
    trazabilidad. No los objetos de ginn.
    """
    res = {}
    codigo = "PV{}".format(producto_ginn.id)
    almacen = 'GTX'
    origen_documento = 11
    comentario = "Consumo %"
    serie = '!MAN'
    regs = get_registros_movimientoarticuloserie(fini, ffin, codigo, almacen,
                                                 origen_documento, comentario,
                                                 serie)
    for reg in regs:
        calidad = reg['CodigoTalla01_']
        codigo = reg['NumeroSerieLc']
        try:
            res[calidad].append(codigo)
        except KeyError:
            res[calidad] = [codigo]
    # Ordeno por código antes de devolver el resultado
    for calidad in res:
        res[calidad].sort()
    return res


def buscar_bultos_consumidos_ginn(producto, fini, ffin):
    """
    Devuelve los artículos de ginn consumidos según ginn entre las fechas
    recibidas agrupados por calidad.
    """
    res = {}
    articulos = get_articulos_consumidos_ginn(producto, fini, ffin)
    for a in articulos:
        calidad = a.get_str_calidad()
        try:
            res[calidad].append(a)
        except KeyError:
            res[calidad] = [a]
    # Ordeno por código antes de devolver el resultado
    for calidad in res:
        res[calidad].sort(key=lambda a: a.codigo)
    return res


def buscar_bultos_producidos_murano(producto_ginn, fini, ffin):
    """
    Busca todos los números de serie consumidos del producto según Murano.
    Los devuelve agrupados por calidad y solo devuelve el código de
    trazabilidad. No los objetos de ginn.
    """
    res = {}
    codigo = "PV{}".format(producto_ginn.id)
    almacen = 'GTX'
    origen_documento = 2
    serie = 'FAB'
    altas = get_registros_movimientoarticuloserie(fini, ffin, codigo, almacen,
                                                  origen_documento,
                                                  serie=serie)
    origen_documento = 11
    serie = 'FAB'
    comentario = "!Consumo %"
    bajas = get_registros_movimientoarticuloserie(fini, ffin, codigo, almacen,
                                                  origen_documento, comentario,
                                                  serie)
    for reg in altas:
        calidad = reg['CodigoTalla01_']
        codigo = reg['NumeroSerieLc']
        try:
            res[calidad].append(codigo)
        except KeyError:
            res[calidad] = [codigo]
    for reg in bajas:
        calidad = reg['CodigoTalla01_']
        codigo = reg['NumeroSerieLc']
        try:
            res[calidad].remove(codigo)
        except KeyError:
            # Ni siquiera hay artículos de esa calidad todavía.
            pass
        except ValueError:
            # El artículo pertenece a otro periodo. No se ha fabricado en las
            # mismas fechas que se ha eliminado. ¿Tendría que hacer algo?
            pass
    # Ordeno por código antes de devolver el resultado
    for calidad in res:
        res[calidad].sort()
    return res


def buscar_bultos_producidos_ginn(producto, fini, ffin):
    """
    Devuelve los artículos de ginn consumidos según ginn entre las fechas
    recibidas agrupados por calidad.
    """
    res = {}
    articulos = query_articulos_from_partes(producto, fini, ffin)
    for a in articulos:
        calidad = a.get_str_calidad()
        try:
            res[calidad].append(a)
        except KeyError:
            res[calidad] = [a]
    # Ordeno por código antes de devolver el resultado
    for calidad in res:
        res[calidad].sort(key=lambda a: a.codigo)
    return res


def main():
    """
    Rutina principal.
    """
    # # Parámetros
    tini = time.time()
    parser = argparse.ArgumentParser(
        description="Soy el inspector Clouseau.\n"
                    "Le sigo la pista a cada uno de los bultos que se han "
                    "fabricado, vendido, consumido o ajustado para ver si hay"
                    "alguna posible desviación.\n"
                    "La pantera rosa no se ha movido del almacén pricipal. "
                    "Así que de momento solo investigo ahí.")
    def_fich_ini = '.'
    parser.add_argument("--fichero_stock_inicial", dest="fich_inventario",
                        default=def_fich_ini)
    parser.add_argument("-p", "--productos", dest="codigos_productos",
                        help="Códigos de productos a comprobar.",
                        nargs="+", default=[])
    ahora = datetime.datetime.today().strftime("%Y%m%d_%H")
    parser.add_argument("-o", dest="fsalida",
                        help="Guardar resultados en fichero de salida.",
                        default="%s_clouseau.md" % (ahora))
    parser.add_argument("-v", "--view", dest="ver_salida",
                        help="Abre el fichero de salida en un editor externo.",
                        default=False, action='store_true')
    parser.add_argument("-d", "--debug", dest="debug", help="Modo depuración.",
                        default=False, action="store_true")
    parser.add_argument("--ffin", dest='ffin', help="Fecha fin (no incluida)",
                        default=None)
    args = parser.parse_args()
    if args.debug:
        connection.DEBUG = True
    if args.ver_salida:
        if not os.path.exists(args.fsalida):
            open(args.fsalida, 'a').close()
        subprocess.Popen(["gvim", args.fsalida])
    # # Pruebas
    productos = []
    results = []    # Resultados de las comprobaciones para cada `productos`.
    if args.codigos_productos:
        for codigo in tqdm(args.codigos_productos,
                           desc="Buscando productos ginn"):
            producto = murano.ops.get_producto_ginn(codigo)
            productos.append(producto)
    else:
        for pv in tqdm(pclases.ProductoVenta.select(orderBy="id"),
                       desc="Buscando productos ginn"):
            productos.append(pv)
    fich_inventario = find_fich_inventario(args.fich_inventario)
    fini = parse_fecha_xls(fich_inventario)
    today = datetime.date.today()
    # Para evitar problemas con las fechas que incluyen horas, y para que
    # éstas entren en el intervalo, agrego un día a la fecha final y hago
    # el filtro con menor estricto: una producción del 02/01/17 23:00
    # la consideramos como que entra en el día 2, y entraría en el filtro
    # [01/01/17..02/01/17] porque en realidad sería [01/01/17..03/01/17).
    if not args.ffin:
        ffin = today + datetime.timedelta(days=1)
    else:
        if "/" in args.ffin:
            ffin = datetime.date(*[int(a) for a in args.ffin.split("/")[::-1]])
        else:
            if int(args.ffin[:4]) >= 2017:
                args.ffin = args.ffin[6:] + args.ffin[4:6] + args.ffin[:4]
            ffin = datetime.date(day=int(args.ffin[:2]),
                                 month=int(args.ffin[2:4]),
                                 year=int(args.ffin[4:]))
    report = open(args.fsalida, "a", 0)
    report.write("Analizando desde {} a {}, fin no incluido.\n".format(
        fini.strftime("%d/%m/%Y"), ffin.strftime("%d/%m/%Y")))
    report.write("=========================================================="
                 "\n")
    report.write("## Todas las cantidades son en (bultos, m², kg).\n")
    # data_inventario = load_inventario(fich_inventario)
    data_res = tablib.Dataset(title="Incoherencias")
    data_res.headers = ['Código', 'Producto', 'Serie', 'Calidad',
                        'Prod. ginn', 'Prod. Murano',
                        'Cons. ginn', 'Cons. Murano',
                        'Bultos', 'm²', 'kg']
    for producto in tqdm(productos, desc="Productos"):
        res = investigar(producto, fini, ffin, report, data_res, args.debug)
        results.append((producto, res))
    fallos = [p for p in results if not p[1]]
    report.write("Encontrados {} productos con incoherencias: {}".format(
        len(fallos), "; ".join(['PV{}'.format(p[0].id) for p in fallos])))
    report.write("\n\nFecha y hora de generación del informe: {}\n".format(
        datetime.datetime.now().strftime("%d/%m/%Y %H:%M")))
    tfin = time.time()
    hours, rem = divmod(tfin - tini, 3600)
    minutes, seconds = divmod(rem, 60)
    report.write("Tiempo transcurrido: {:0>2}:{:0>2}:{:05.2f}\n".format(
        int(hours), int(minutes), seconds))
    report.write("\n\n___\n\n")
    report.close()
    fout = args.fsalida.replace(".md", ".xls")
    book = tablib.Databook((data_res, ))
    with open(fout, 'wb') as f:
        # pylint: disable=no-member
        f.write(book.xls)


if __name__ == "__main__":
    main()
