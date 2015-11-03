#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = """
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

DELETE
------
* Eliminación de artículos.


EXTRA
-----
* Llamada a procedimiento de importación interno de Murano via 
%SYSTEMDRV%\...\Sage\Sage Murano\LCOEM.dll

REQUERIMENTS
------------
pymssql, pywin32
"""
