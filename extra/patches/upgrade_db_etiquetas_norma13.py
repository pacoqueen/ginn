#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Crea los campos y actualiza los productos para las nuevas etiquetas de la 
norma del 1 de julio de 2013.
"""

import os, sys
sys.path.insert(0, (os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                    "..", "..", "ginn")))
os.chdir(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "..",
                      "ginn"))
from framework import pclases

def alter_tables():
    cmd = """echo "ALTER TABLE producto_venta ADD COLUMN anno_certificacion INT DEFAULT NULL; ALTER TABLE producto_venta ADD COLUMN dni TEXT DEFAULT ''; ALTER TABLE producto_venta ADD COLUMN uso TEXT DEFAULT ''; UPDATE producto_venta SET anno_certificacion = NULL; UPDATE producto_venta SET dni = ''; UPDATE producto_venta SET uso = '';" | psql dev_ginn """
    os.system(cmd)
    cmd = """echo "ALTER TABLE producto_venta ADD COLUMN anno_certificacion INT DEFAULT NULL; ALTER TABLE producto_venta ADD COLUMN dni TEXT DEFAULT ''; ALTER TABLE producto_venta ADD COLUMN uso TEXT DEFAULT ''; UPDATE producto_venta SET anno_certificacion = NULL; UPDATE producto_venta SET dni = ''; UPDATE producto_venta SET uso = '';" | psql ginn """
    os.system(cmd)

def update_values_producto(p):
    modificado = True
    if "GEOTESAN" in p.nombre.upper() and " 10 " in p.descripcion:
        p.annoCertificacion = 8
        p.dni = "0001 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo y separación"
    elif "GEOTESAN" in p.nombre.upper() and " 11 " in p.descripcion:
        p.annoCertificacion = 4
        p.dni = "0002 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo y separación"
    elif "GEOTESAN" in p.nombre.upper() and " 12 " in p.descripcion:
        p.annoCertificacion = 4
        p.dni = "0003 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo y separación"
    elif "GEOTESAN" in p.nombre.upper() and " 13 " in p.descripcion:
        p.annoCertificacion = 4
        p.dni = "0004 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo y separación"
    elif "GEOTESAN" in p.nombre and " 14 " in p.descripcion:
        p.annoCertificacion = 8
        p.dni = "0005 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo y separación"
    elif "GEOTESAN" in p.nombre.upper() and " 120 " in p.descripcion:
        p.annoCertificacion = 13
        p.dni = "0006 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo y separación"
    elif "GEOTESAN" in p.nombre.upper() and " 15 " in p.descripcion:
        p.annoCertificacion = 4
        p.dni = "0007 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo y separación"
    elif "GEOTESAN" in p.nombre.upper() and " 155 " in p.descripcion:
        p.annoCertificacion = 11
        p.dni = "0008 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo y separación"
    elif "GEOTESAN" in p.nombre.upper() and " 17 " in p.descripcion:
        p.annoCertificacion = 4
        p.dni = "0009 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo y separación"
    elif "GEOTESAN" in p.nombre.upper() and " 175 " in p.descripcion:
        p.annoCertificacion = 4
        p.dni = "0010 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo y separación"
    elif "GEOTESAN" in p.nombre.upper() and " 18 " in p.descripcion:
        p.annoCertificacion = 8
        p.dni = "0011 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo y separación"
    elif "GEOTESAN" in p.nombre.upper() and " 21 " in p.descripcion:
        p.annoCertificacion = 4
        p.dni = "0012 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo, separación y protección"
    elif "GEOTESAN" in p.nombre.upper() and " 23 " in p.descripcion:
        p.annoCertificacion = 4
        p.dni = "0013 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo, separación y protección"
    elif "GEOTESAN" in p.nombre.upper() and " 235 " in p.descripcion:
        p.annoCertificacion = 11
        p.dni = "0014 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo, separación y protección"
    elif "GEOTESAN" in p.nombre.upper() and " 25 " in p.descripcion:
        p.annoCertificacion = 8
        p.dni = "0015 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo, separación y protección"
    elif "GEOTESAN" in p.nombre.upper() and " 30 " in p.descripcion:
        p.annoCertificacion = 4
        p.dni = "0016 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo, separación y protección"
    elif "GEOTESAN" in p.nombre.upper() and " 305 " in p.descripcion:
        p.annoCertificacion = 11
        p.dni = "0017 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo, separación y protección"
    elif "GEOTESAN" in p.nombre.upper() and " 35 " in p.descripcion:
        p.annoCertificacion = 4
        p.dni = "0018 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo, separación y protección"
    elif "GEOTESAN" in p.nombre.upper() and " 40 " in p.descripcion:
        p.annoCertificacion = 4
        p.dni = "0019 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo, separación y protección"
    elif "GEOTESAN" in p.nombre.upper() and " 46 " in p.descripcion:
        p.annoCertificacion = 4
        p.dni = "0020 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo, separación y protección"
    elif "GEOTESAN" in p.nombre.upper() and " 58 " in p.descripcion:
        p.annoCertificacion = 4
        p.dni = "0021 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo, separación y protección"
    elif "GEOTESAN" in p.nombre.upper() and " 69 " in p.descripcion:
        p.annoCertificacion = 8
        p.dni = "0022 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo, separación y protección"
    elif "GEOTESAN" in p.nombre.upper() and " 70 " in p.descripcion:
        p.annoCertificacion = 8
        p.dni = "0023 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo, separación y protección"
    elif "GEOTESAN" in p.nombre.upper() and " 80 " in p.descripcion:
        p.annoCertificacion = 9
        p.dni = "0024 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo, separación y protección"
    elif "GEOTESAN" in p.nombre.upper() and " 85 " in p.descripcion:
        p.annoCertificacion = 13
        p.dni = "0025 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo, separación y protección"
    elif "GEOTESAN" in p.nombre.upper() and " 200 " in p.descripcion:
        p.annoCertificacion = 8
        p.dni = "0026 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo y separación"
    elif "GEOTESAN" in p.nombre.upper() and " 90 " in p.descripcion:
        p.dni = "0027 - GEOTEXTIL - 20130701"
        p.uso = "Drenaje, filtración, refuerzo, separación y protección"
    elif "GEOCEM" in p.nombre.upper():
        if p.es_caja():
            p.uso = "Fibra de polipropileno virgen embolsada en papel hidrosoluble para su uso como aditivo del hormigón"
            if p.camposEspecificosBala.dtex == 6.7:
                p.nombre = "GEOCEM 31 - %d" % p.camposEspecificosBala.corte
                p.annoCertificacion = 9
                if p.camposEspecificosBala.corte == 6:
                    p.dni = "0001 – GEOCEM - 20130701"
                elif p.camposEspecificosBala.corte == 12:
                    p.dni = "0002 – GEOCEM - 20130701"
                elif p.camposEspecificosBala.corte == 18:
                    p.dni = "0003 – GEOCEM - 20130701"
                elif p.camposEspecificosBala.corte == 24:
                    p.dni = "0004 – GEOCEM - 20130701"
                else:
                    modificado = False
            elif p.camposEspecificosBala.dtex == 4.4:
                p.nombre = "GEOCEM 31 - 12"
                p.dni = "0005 – GEOCEM - 20130701"
                p.annoCertificacion = 13
            else:
                modificado = False
    else:
        modificado = False
    print p.dni
    return modificado

def set_values():
    """
    Establece los valores por defecto de acuerdo a la tabla de Jesús.
    """
    no_modificados = []
    for p in pclases.ProductoVenta.select():
        print "\t", p.descripcion, "...", 
        sys.stdout.flush()
        modificado = update_values_producto(p)
        if not modificado:
            no_modificados.append(p)
    print "-"*80
    print 
    print "Productos no modificados:"
    print 
    for p in no_modificados:
        print p.nombre, "-", p.descripcion

def main():
    print "Altering tables..."
    alter_tables()
    print "Setting values..."
    set_values()
    print "Done!"

if __name__ == "__main__":
    main()

