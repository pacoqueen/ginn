#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Crea un CSV con información relativa a los partes de producción para un estudio  de productividades que necesita Jesús Madrid.
Funciona buscando los partes entre dos fechas prefijadas en el script y volcando una serie de campos a un formato de fichero separado por punto y coma pero por salida estándar.
"""

import re
import csv
import sys
import mx
try:
    from framework import pclases
except ImportError:
    print "Trata de exportar primero el PYTHONPATH dentro de ginn tal que así: cd ...Geotex-INN/ginn; export PYTHONPATH=$PYTHONPATH:."
from formularios import utils

def volcar_info(pdp, csv):
    producto = pdp.productoVenta and pdp.productoVenta
    nombre_producto = producto and producto.descripcion or ""
    prod_estandar_parte = pdp.prodestandar
    prod_estandar_producto = producto and producto.prodestandar or ""
    fecha = utils.str_fecha(pdp.fecha)
    horaini = utils.str_hora_corta(pdp.horainicio)
    horafin = utils.str_hora_corta(pdp.horafin)
    produccion_m2 = pdp.get_produccion()[0]
    produccion_kg = sum([a.peso_sin for a in pdp.articulos])
    productividad = pdp.calcular_productividad()
    rendimiento = pdp.calcular_rendimiento()
    observaciones = pdp.observaciones
    observaciones_paradas = "; ".join(
            [parada.observaciones for parada in pdp.incidencias])
    tiempo_produccion, tiempo_paradas = calcular_tiempo_trabajado(pdp)
    csv.writerow((nombre_producto, 
                  prod_estandar_parte, 
                  prod_estandar_producto, 
                  fecha, 
                  horaini, 
                  horafin, 
                  produccion_m2, 
                  produccion_kg, 
                  productividad, 
                  rendimiento, 
                  observaciones, 
                  observaciones_paradas, 
                  tiempo_produccion, 
                  tiempo_paradas))

def calcular_tiempo_trabajado(parte):
    tiempototal = parte.get_duracion()
    paradas = [p for p in parte.incidencias]
    tiempoparadas = 0
    for parada in paradas:
        tiempoparadas += parada.get_duracion()
    return tiempototal - tiempoparadas, tiempoparadas

def buscar_partes(fini, ffin):
    pdps = pclases.ParteDeProduccion.select(pclases.AND(
        pclases.ParteDeProduccion.q.fechahorainicio >= fini, 
        pclases.ParteDeProduccion.q.fechahorafin <= ffin))
    pdps_gtx = [p for p in pdps if p.es_de_rollos()]
    return pdps_gtx
        
def main():
    fini = mx.DateTime.DateFrom(2013, 9, 1)
    ffin = mx.DateTime.DateFrom(2013, 10, 29)
    pdps = buscar_partes(fini, ffin)
    sys.stderr.write("Encontrados %d partes de producción. Volcando..." % 
            len(pdps))
    csvfile = csv.writer(sys.stdout)
    csvfile.writerow(("Descripción", 
                      "Producción estándar del parte", 
                      "Producción estándar teórica del producto", 
                      "Fecha", 
                      "Hora inicio", 
                      "Hora fin", 
                      "Producción (m²)", 
                      "Producción (kg)", 
                      "Productividad del parte", 
                      "Rendimiento", 
                      "Observaciones", 
                      "Motivo paradas", 
                      "Tiempo total producción", 
                      "Tiempo total paradas"))
    for pdp in pdps:
        volcar_info(pdp, csvfile)

if __name__ == "__main__":
    main()

