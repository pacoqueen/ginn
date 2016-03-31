#!/usr/bin/env python
# -*- coding: utf-8 -*-

r"""
API de conexión con Sage Murano
===============================

Proporciona un interfaz CRUD de intercambio de datos con Sage Murano.

CREATE
------
* Creación de balas de fibra (A, B y C).
* Creación de bigbags de fibra (A).
* Creación de rollos de geotextiles (A, B y C).
* Creación de palés y cajas de fibra de cemento embolsada (A).

READ
----
* Consulta de datos de proveedores.
* Consulta de datos de clientes.
* Consulta de datos de productos.

UPDATE
------
* Modificación de calidad de un artículo.
* Cambio de producto de un artículo.
* Incremento o decremento del stock de un producto.
* Decremento de un producto de compra (consumo).

DELETE
------
* Eliminación de artículos.


EXTRA
-----
* Llamada a procedimiento de importación interno de Murano via
%SYSTEMDRV%\...\Sage\Sage Murano\LCOEM.dll
* Exportación a CSV y SQL de todos los productos, clientes y proveedores.

REQUERIMENTS
------------
pymssql, pywin32
"""

from ginn.api.murano.ops import create_bala, create_rollo, consumir
from ginn.api.murano.ops import create_pale, create_bigbag, delete_articulo
from ginn.api.murano.export import exportar_productos, exportar_clientes
from ginn.api.murano.export import exportar_proveedores

__all__ = ["create_bala", "create_rollo", "consumir", "delete_articulo",
           "exportar_productos", "exportar_clientes", "exportar_proveedores",
           "create_bigbag", "create_pale"]
