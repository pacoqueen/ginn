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


# pylint: disable=too-many-branches,too-many-statements,too-many-locals
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
    - Producto de venta
    """
    report = open(fsalida, "a", 0)
    if simulate:
        report.write("Simulando sincronización de artículo %s... " % codigo)
    else:
        report.write("Sincronizando artículo %s... " % codigo)
    articulo = pclases.Articulo.get_articulo(codigo)
    if articulo:
        if not murano.ops.existe_articulo(articulo):
            if murano.ops.esta_en_almacen(articulo) == 'GTX':
                # No existe como ese producto, pero sí que existe porque está
                # almacén, pero con otro producto entonces. Hay que cambiarlo
                # a su producto correcto según ginn:
                report.write("Cambiando producto en Murano...")
                if not simulate:
                    obs = "[sr_lobo] Producto dif. ginn y Murano."
                    res = murano.ops.update_producto(articulo,
                                                     articulo.productoVenta,
                                                     observaciones=obs)
                else:
                    res = True
            elif murano.ops.esta_en_almacen(articulo):
                # Está en otro almacén que no es el principal.
                report.write("Artículo como otro producto en almacén {}"
                             ".".format(murano.ops.esta_en_almacen(articulo)))
                # Corregir a mano cambiando el producto en ginn o lo que sea.
                res = False
            else:
                # No existe con el producto de ginn, pero puede que con algún
                # otro y ya no está en almacén o que no exista en absoluto.
                movserie = murano.ops.get_ultimo_movimiento_articulo_serie(
                    murano.connection.Connection(), articulo)
                if not movserie:
                    report.write("Creando... ")
                    if not simulate:
                        obs = "[sr_lobo] Art. en ginn pero no en Murano"
                        res = murano.ops.create_articulo(articulo,
                                                         observaciones=obs)
                    else:
                        res = True
                else:   # Hay un movserie, seguramente de salida de albarán.
                    pvmurano = movserie['CodigoArticulo']
                    report.write("Arículo ya vendido como {}. ".format(
                        pvmurano))
                    res = True
        else:   # Si el artículo ya existe:
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
            # Solo trabajamos con 2 decimales. Redondeo para evitar falsos
            # positivos en != por 0.00000001 unidad y cosas así.
            peso_bruto = round(peso_bruto, 2)
            peso_neto = round(peso_neto, 2)
            superficie = round(superficie, 2)
            peso_bruto_murano = round(peso_bruto_murano, 2)
            peso_neto_murano = round(peso_neto_murano, 2)
            superficie_murano = round(superficie_murano, 2)
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
            # Si además es de tipo fibra de cemento, compruebo el palé:
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
            # Y por último compruebo el producto:
            prod_en_murano = murano.ops.get_producto_articulo_murano(articulo)
            prod_en_ginn = articulo.productoVenta
            if prod_en_murano != prod_en_ginn:
                # Creo que esta rama está "muerta". Aquí no entraría nunca.
                report.write("Corrigiendo producto de {}: {} -> {}".format(
                    articulo.codigo, prod_en_murano.descripcion,
                    prod_en_ginn.descripcion))
                altered = True
                if not simulate:
                    obs = "[sr_lobo] Prod. corregido acorde a ginn"
                    res = murano.ops.update_producto(articulo, prod_en_ginn,
                                                     obs)
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
        producto_ginn = murano.ops.producto_murano2ginn(codigo, sync=False)
    # 1.- Actualizo campos conforme a lo que indica Murano.
    res = murano.ops.producto_murano2ginn(codigo, sync=True)
    # 2.- Compruebo que los valores obligatorios están "informados".
    producto_ginn.sync()    # Por si ha cambiado algo.
    if (isinstance(producto_ginn, pclases.ProductoVenta)
            and not producto_ginn.obsoleto):
        # Si hemos marcado el producto como obsoleto, me da igual entonces.
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
    canal = murano.ops.get_canal(producto)
    res = []
    if not canal:
        res.append('CANAL')
    elif canal not in (murano.connection.RESIDUOS_FIBRA,
                       murano.connection.RESIDUOS_GEOTEXTIL,
                       murano.connection.COMERCIALIZADO):
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
                for campo in campos[indirecto]:
                    valor = getattr(indirecto, campo)
                    if not valor:
                        res.append(campo)
    return res


# pylint: disable=too-many-locals
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
    # pylint: disable=bad-continuation, no-member
    articulos_en_almacen = pclases.Articulo.select(     # NOQA
        pclases.Articulo.q.almacen != None)
    partes_fabricacion = pclases.ParteDeProduccion.select(
        pclases.ParteDeProduccion.q.fechahorainicio >= fini)
    articulos = set(articulos_en_almacen)
    for pdp in tqdm(partes_fabricacion, total=partes_fabricacion.count(),
                    unit="pdp", desc="Partes de producción"):
        articulos.update(set(pdp.articulos))
    # Completo con balas y rollos C, que no tienen parte de producción:
    balas_cable = pclases.BalaCable.select(
        pclases.BalaCable.q.fechahora >= fini)
    for bc in tqdm(balas_cable, total=balas_cable.count(), unit="bc",
                   desc="Balas de cable"):
        articulos.add(bc.articulo)
    rollos_c = pclases.RolloC.select(pclases.RolloC.q.fechahora >= fini)
    for rc in tqdm(rollos_c, total=rollos_c.count(), unit="rc",
                   desc="Rollos C"):
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
    report.write("{} procesos pendientes encontrados.\n".format(len(guids)))
    for proceso in tqdm(guids, desc="Procesos pendientes"):
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
    for sql in tqdm(sqls, total=tot, desc="Dimensiones nulas"):
        sql = sql.format(conn.get_database(), murano.connection.CODEMPRESA)
        codigos = conn.run_sql(sql)
        report.write("{}/{}: {} artículos encontrados:\n".format(i, tot,
                                                                 len(codigos)))
        for registro in tqdm(codigos, leave=False, desc="SQL {}".format(i)):
            codigo = registro['NumeroSerieLc']
            res = sync_articulo(codigo, fsalida, simulate) and res
        i += 1
    report.close()
    return res


def make_consumos(fsalida, simulate=True, fini=None, ffin=None):
    """
    Realiza todos los consumos de materiales y de balas cargadas en la línea.
    """
    make_consumos_materiales(fsalida, simulate, fini, ffin)
    make_consumos_balas(fsalida, simulate, fini, ffin)
    make_consumos_bigbags(fsalida, simulate, fini, ffin)


def make_consumos_bigbags(fsalida, simulate=True, fini=None, ffin=None):
    """
    Realiza los consumos de fibra en bigbag por parte de la línea de cemento.
    """
    # Check de parámetros
    report = open(fsalida, "a", 0)
    if not fini:
        fini = datetime.date(2016, 5, 31)   # Fecha en que entró Murano.
    if not ffin:
        ffin = datetime.date.today() + datetime.timedelta(days=1)
    # pylint: disable=no-member, singleton-comparison
    pdps = pclases.ParteDeProduccion.select(pclases.AND(
        pclases.ParteDeProduccion.q.fecha >= fini,
        pclases.ParteDeProduccion.q.fecha < ffin,
        pclases.ParteDeProduccion.q.bloqueado == True))
    report.write("Consumos bigbag: {} partes encontrados.\n".format(
        pdps.count()))
    res = True
    for pdp in tqdm(pdps, total=pdps.count(),
                    desc="Partes a consumir (bigbags)", unit="pdp"):
        for bb in pdp.bigbags:
            # Ignoro los ya tratados y los que no se completaron en ginn (el
            # parte está sin verificar).
            if not bb.api:
                if murano.ops.esta_en_almacen(bb.articulo) == "GTX":
                    res = consumir_bigbag(report, bb, simulate) and res
                else:
                    # El bigbag está en otro almacén o no está. Me da igual.
                    # No lo puedo consumir ni se podrá consumir jamás. Hay que
                    # corregirlo a mano.
                    report.write("El bigbag está en otro almacén o no está.")
                    res = False
    report.close()
    return res


def consumir_bigbag(report, bb, simulate=True):
    """
    Descuenta el bigbag del almacén de Murano indicando que es un consumo
    de un parte de la línea de cemento embolsado en el movimiento de serie.
    """
    report.write("Consumiendo bigbag {} [id {} ({})] de {}:\n".format(
        bb.codigo, bb.id, bb.articulo.puid,
        bb.articulo.productoVenta.descripcion))
    # Aquí hacemos efectivo el rebaje de stock
    res = murano.ops.consume_bigbag(bb, simulate=simulate)
    report.write("\tValor de retorno: {}\n".format(res))
    return res


def make_consumos_balas(fsalida, simulate=True, fini=None, ffin=None):
    """
    Realiza los consumos de balas cargadas en las partidas de carga para
    consumo de la línea de geotextiles.
    """
    res = True
    # Check de parámetros
    report = open(fsalida, "a", 0)
    if not fini:
        fini = datetime.date(2016, 5, 31)   # Fecha en que entró Murano.
    if not ffin:
        ffin = datetime.date.today() + datetime.timedelta(days=1)
    # pylint: disable=no-member, singleton-comparison
    pcargas = pclases.PartidaCarga.select(pclases.AND(
        pclases.PartidaCarga.q.fecha >= fini,
        pclases.PartidaCarga.q.fecha <= ffin,
        pclases.PartidaCarga.q.api == False))
    # DONE: Debería meter un filtro más para no consumir las partidas de carga
    # que no tengan todos los partes de producción verificados. Así doy margen
    # a Jesús para que pueda modificarlas. Si no tiene partes, no volcar tampoco.
    report.write("{} partidas de carga encontradas.\n".format(pcargas.count()))
    for pcarga in tqdm(pcargas, total=pcargas.count(),
                       desc="Partidas de carga", unit="partida"):
        respartida = True
        if not pcarga.balas:    # Partida de carga vacía. No modifico `api`
            report.write("Partida de carga {} vacía. Se ignora.\n".format(
                pcarga.codigo))
            continue
        pdps_sin_verificar = [pdp for pdp in pcarga.partes_partidas
                              if not pdp.bloqueado]
        if pdps_sin_verificar:
            report.write("Partida de carga {} con {}/{} partes sin verificar"
                         ". Se ignora.".format(pcarga.codigo,
                                               len(pdps_sin_verificar),
                                               len(pcarga.partes_partidas)))
            continue
        if not pcarga.partes_partidas:
            report.write("Partida de carga {} sin partes de producción."
                         "Se ignora.".format(pcarga.codigo))
            continue
        for bala in pcarga.balas:
            report.write("Consumiendo bala {} [id {} ({})] de {}:\n".format(
                bala.codigo, bala.id, bala.articulo.puid,
                bala.articulo.productoVenta.descripcion))
            # Aquí hacemos efectivo el rebaje de stock
            fecha_consumo = murano.ops.esta_consumido(bala.articulo)
            if fecha_consumo:
                _res = True
                report.write("\tBala ya consumida el {}\n".format(
                    fecha_consumo))
            else:
                _res = murano.ops.consume_bala(bala, simulate=simulate)
                report.write("\tValor de retorno: {}\n".format(_res))
            respartida = respartida and _res
        if respartida and not simulate:
            pcarga.api = True
            pcarga.sync()
            report.write("\tValor api partida de carga actualizado.\n")
        res = res and respartida
    report.close()
    return res


def make_consumos_materiales(fsalida, simulate=True, fini=None, ffin=None):
    """
    Recorre todos los consumos entre la fecha inicial y la final. Para cada
    consumo realiza el rebaje de stock en Murano mediante un movimiento de
    salida y marca el _flag_ `api` a True para indicarlo.
    Si simualte es True, no hace nada y solo actualiza el log de `fsalida`.
    Devuelve True si todos los consumos pendientes se han realizado. False si
    alguno de ellos ha dado error.
    """
    # Check de parámetros
    report = open(fsalida, "a", 0)
    if not fini:
        fini = datetime.date(2016, 5, 31)   # Fecha en que entró Murano.
    if not ffin:
        ffin = datetime.date.today() + datetime.timedelta(days=1)
    # pylint: disable=no-member, singleton-comparison
    pdps = pclases.ParteDeProduccion.select(pclases.AND(
        pclases.ParteDeProduccion.q.fechahorainicio >= fini,
        pclases.ParteDeProduccion.q.fechahorafin <= ffin,
        pclases.ParteDeProduccion.q.bloqueado == True))
    report.write("{} partes encontrados.\n".format(pdps.count()))
    res = True
    for pdp in tqdm(pdps, total=pdps.count(),
                    desc="Partes a consumir (materia prima)", unit="pdp"):
        for consumo in pdp.consumos:
            # Ignoro los ya tratados y los que no se completaron en ginn.
            if not consumo.api and consumo.actualizado:
                res = consumir_mp(consumo, report, simulate) and res
    report.close()
    return res


def consumir_mp(consumo, report, simulate=True):
    """
    Descuenta las cantidades que indica el consumo en el producto de compra
    del mismo.
    """
    producto = consumo.productoCompra
    idmurano = "PC{}".format(producto.id)
    cantidad = -1.0 * consumo.cantidad
    productomurano = murano.ops.get_producto_murano(idmurano)
    unidad = productomurano['UnidadMedida2_']
    # Todos los consumos siempre se hacen del almacén principal
    stockmurano = murano.ops.get_stock_murano(producto,
                                              'GTX', '', unidad)
    report.write("Actualizando {} ({}) en Murano:\n".format(
        producto.descripcion, idmurano))
    report.write("\tExistencias anteriores: {} {}\n".format(
        stockmurano, unidad))
    report.write("\tCantidad a descontar: {} {}\n".format(
        cantidad, producto.unidad))
    # Aquí hacemos efectivo el rebaje de stock
    res = murano.ops.update_stock(producto, cantidad, 'GTX',
                                  simulate=simulate)
    report.write("\tValor de retorno: {}\n".format(res))
    if res and not simulate:
        consumo.api = True
        consumo.sync()
        report.write("\tValor api consumo actualizado.\n")
    stockmuranoact = murano.ops.get_stock_murano(producto,
                                                 'GTX', '', unidad)
    report.write("\tExistencias actual: {} {}\n".format(
        stockmuranoact, unidad))
    return res


def check_unidades_series_positivas():
    """
    Si algún artículo de la empresa 10200 tiene el campo UnidadesSerie en
    negativo, lanzo una excepción. Hay que corregir eso manualmente antes de
    hacer nada más. Ni consumos ni nada. Lo primero es lo primero.
    """
    conn = murano.connection.Connection()
    sql = """SELECT * FROM {}.dbo.ArticulosSeries
              WHERE UnidadesSerie < 0 AND CodigoEmpresa = {};""".format(
                  conn.get_database(), murano.connection.CODEMPRESA)
    articulos = conn.run_sql(sql)
    assert len(articulos) == 0, "Se detectaron artículos con UnidadesSerie "\
            "negativas: {}".format("; ".join(
                [a['NumeroSerieLc'] for a in articulos]))


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
    parser.add_argument("-c", "--consumos", dest="consumos",
                        help="Realiza los consumos atrasados",
                        default=False, action='store_true')
    args = parser.parse_args()
    if args.ver_salida:
        if not os.path.exists(args.fsalida):
            open(args.fsalida, 'a').close()
        subprocess.Popen('gvim "{}"'.format(args.fsalida))
    # Primero termino de procesar todas las posibles imortaciones pendientes:
    finish_pendientes(args.fsalida, args.simulate)
    # Y corrijo las posibles dimensiones nulas:
    corregir_dimensiones_nulas(args.fsalida, args.simulate)
    if (not args.codigos_articulos and not args.codigos_productos and
            not args.consumos):
        # Si no recibo argumentos, compruebo todos los artículos y productos.
        args.codigos_articulos, args.codigos_productos = check_everything(
            args.fsalida)
        # Y los consumos
        args.consumos = True
    # # Pruebas
    check_unidades_series_positivas()
    # ## Consumos
    if args.consumos:
        make_consumos(args.fsalida, args.simulate)
    if args.codigos_productos:
        for codigo in tqdm(args.codigos_productos, desc="Productos"):
            sync_producto(codigo, args.fsalida, args.simulate)
    if args.codigos_articulos:
        for codigo in tqdm(args.codigos_articulos, desc="Artículos"):
            sync_articulo(codigo, args.fsalida, args.simulate)


if __name__ == "__main__":
    main()
