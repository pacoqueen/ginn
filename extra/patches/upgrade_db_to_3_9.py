#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Realiza los cambios en la base de datos para actualizar desde la versión 2.8 
a la 2.9:
    - Añadir columna proveedor a la tabla de productos de compra.
"""

import sys, os

from framework import pclases

def get_dbname():
    dsn = pclases.ProductoCompra._connection.dsn  # @UndefinedVariable
    dsndict = dict([(k, v) for k, v in [i.split("=") for i in dsn.split()]])
    return dsndict['dbname']

def insert_column():
    dbname = get_dbname()
    command = """echo "ALTER TABLE producto_compra ADD COLUMN proveedor_id INT REFERENCES proveedor; UPDATE producto_compra SET proveedor_id = NULL;" | psql %s""" % dbname
    os.system(command)

def update_values():
    for p in pclases.ProductoCompra.selectBy(obsoleto = False):
        try:
            p.proveedor=p.get_proveedores()[-1]  #Se supone que el más reciente
        except IndexError:
            p.proveedor = None
        p.syncUpdate()
        print ".", 
        sys.stdout.flush()

def main():
    clase_no_tiene_proveedor = not hasattr(pclases.ProductoCompra, 
                                           "proveedorID")
    try:
        pc = pclases.ProductoCompra.select()[0]
    except IndexError:
        pass
    except:
        clase_no_tiene_proveedor = True
    else:
        try:
            p = pc.proveedor
        except:
            clase_no_tiene_proveedor = True
    if clase_no_tiene_proveedor:
        print "Modificando base de datos..."
        insert_column()
        print "Actualizando valores..."
        update_values()
        print "Finito"

if __name__ == "__main__": 
    main()

