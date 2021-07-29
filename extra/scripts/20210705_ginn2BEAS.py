#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=invalid-name

"""
Exportar estructuras de producto a BEAS
=======================================

Genera los ficheros de datos para las plantillas de importación de BEAS con
los que trabajará Seidor para montar la base de datos de desarrollo y test.
"""

from __future__ import print_function
import sys
import os
import datetime
import csv
# Determino dónde estoy para importar pclases y utils
DIRACTUAL = os.path.split(os.path.abspath(os.path.curdir))[-1]
if DIRACTUAL != "ginn":
    PATH_TO_F = os.path.join("..", "..", "ginn")
    sys.path.append(PATH_TO_F)
# pylint: disable=wrong-import-position,import-error
from framework import pclases   # noqa
# from api import murano          # noqa
from lib.tqdm import tqdm       # noqa


def get_datos_pv(pv):
    """Devuelve los campos que necesitamos del producto de venta."""
    try:
        peso_teorico = pv.get_peso_teorico()  # Tamaño lote (bulto) óptimo.
        peso_teorico = round(peso_teorico, 2)
    except ValueError:
        peso_teorico = 0.0
    lead_time = 1   # Tiempo de espera producción/compras
    cant_minima = 0     # Mínimo a producir para meter en planificación.
    if pv.es_bala() or pv.es_bigbag():
        cant_minima = 25000  # kg para fibra. +abahamonde
    elif pv.es_rollo():
        cant_minima = 5000  # kg para geotextiles. +abahamonde
    cant_multiple = 0   # Cantidad pedido o producción múltiple ¿?
    metodo_compra = 'M' # B = Compra, M = Producir
    mrp = 'bop-MRP'     # Si el producto entra en el MRP
    prov = pv.proveedor and pv.proveedor.id or ""  # Proveedor por defecto.
    unidad_consumo = 'kg'   # UD en la hoja original.
    metodo_emision = 'B'    # M = Manual; B = Automático
    codigo_lote = 'A'       # M = Manual; A = Automático
    explosion_mat = 'A'     # A=Por orden; B=Orientado a stock; S=Artículo fantasma, K=Ninguna; T=Componentes para compras
    version_defecto = pv.camposEspecificosRollo and pv.camposEspecificosRollo.fichaFabricacion or None
    metodo_vis = 1          # 1=Por versión; ' '=Estándar
    merma = 0.02        # Valor por defecto para partes en tablas.sql
    vida_util = 365     # Días vida útil para cálculo de fecha de caducidad.
        # En las sesiones de análisis dijimos que lo usaríamos para
        # inventariar y comprobar estado del producto, etiquetas, etc.
    codigo = "PV{}".format(pv.id)
    return (codigo, peso_teorico, lead_time, cant_minima, cant_multiple,
            metodo_compra, mrp, prov, unidad_consumo, metodo_emision,
            codigo_lote, explosion_mat, version_defecto, metodo_vis, merma,
            vida_util)


def main():
    """
    Rutina principal.
    """
    with open('BEAS_ARTICULOS EXTENDIDO.csv', 'w') as fsalida:
        campos = ['ItemCode', 'U_beas_losgr', 'LeadTime', 'MinOrderQuantity',
                  'OrderMultiple', 'ProcurementMethod',
                  'PlanningSystem', 'Mainsupplier', 'U_beas_me_verbr',
                  'IssueMethod', 'U_beas_batchroh', 'U_beas_dispo',
                  'U_BEAS_VER', 'u_beas_vercontrol', 'U_beas_aussch',
                  'U_beas_haltbark']
        csvwriter = csv.writer(fsalida, delimiter=";")
        csvwriter.writerow(campos)
        for pv in pclases.ProductoVenta.select(orderBy="id"):
            fila = get_datos_pv(pv)
            print("{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{}".format(
                *fila))
            csvwriter.writerow(fila)

if __name__ == "__main__":
    main()
