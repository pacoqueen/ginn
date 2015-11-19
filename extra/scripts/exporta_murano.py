#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exporta las tablas de clientes, proveedores y productos a un CSV cada uno.

Faltarían: obras, formas de pago...
"""
import os, sys
import csv

# Determino dónde estoy para importar pclases y utils
diractual = os.path.split(os.path.abspath(os.path.curdir))[-1]
assert diractual == "scripts", \
        "Debe ejecutar el script desde el directorio donde reside."
sys.path.insert(0, os.path.abspath(os.path.join("..", "..", "ginn")))
from framework import pclases


def exporta_clientes():
    fclientes = open("/tmp/clientes.csv", "w")
    csvclientes = csv.writer(fclientes)
    clientes = pclases.Cliente.select(pclases.Cliente.q.inhabilitado == False,
                                      orderBy = "nombre")
    cols = [campo.name for campo in clientes[0].sqlmeta.columnList]
    csvclientes.writerow(cols)
    for c in clientes:
        fila = []
        for col in cols:
            fila.append(getattr(c, col))
        csvclientes.writerow(fila)
    fclientes.close()

def exporta_proveedores():
    fproveedores = open("/tmp/proveedores.csv", "w")
    csvproveedores = csv.writer(fproveedores)
    proveedores = pclases.Proveedor.select(
            pclases.Proveedor.q.inhabilitado == False,
            orderBy = "nombre")
    cols = [campo.name for campo in proveedores[0].sqlmeta.columnList]
    csvproveedores.writerow(cols)
    for p in proveedores:
        fila = []
        for col in cols:
            fila.append(getattr(p, col))
        csvproveedores.writerow(fila)
    fproveedores.close()

def exporta_productos():
    # TODO: Acuérdate de que deben ir también los valores de marcado.
    pass

def main():
    exporta_clientes()
    exporta_proveedores()
    exporta_productos()

if __name__ == "__main__":
    main()

