#!/usr/bin/env python
# -*- coding: utf-8 -*-

from connection import Connection 
try:
    import win32com.client
except ImportError:
    LCOEM = False
else:
    LCOEM = True

CODEMPRESA = 9999   # Empresa de pruebas. Cambiar por la 10200 en producción.

def create_bala(bala):
    """
    Crea una bala en las tablas temporales de Murano.
    Recibe un objeto bala de ginn.
    """
    pass

def create_bigabag(bigbag):
    """
    Crea un bigbag en Murano a partir de la información del bigbag en ginn.
    """
    pass

def create_rollo(rollo):
    """
    Crea un rollo en Murano a partir de la información del rollo en ginn.
    """
    pass

def create_pale(pale):
    """
    Crea un palé con todas sus cajas en Murano a partir del palé de ginn.
    """
    pass

def consulta_proveedor(nombre = None, cif = None):
    """
    Obtiene los datos de un proveedor buscando por nombre, cif o ambas cosas.
    Devuelve una lista de proveedores coincidentes.
    """

def consulta_cliente(nombre = None, cif = None):
    """
    Obtiene los datos de un cliente buscando por nombre, cif o ambas cosas.
    Devuelve una lista de clientes coincidentes.
    """
    pass

def consulta_producto(nombre = None):
    """
    Busca un producto por nombre.
    Devuelve una lista de productos coincidentes.
    """
    pass

def update_calidad(articulo, calidad):
    """
    Cambia la calidad del artículo en Murano a la recibida. Debe ser A, B o C.
    """
    if calidad not in "aAbBcC":
        raise ValueError, "El parámetro calidad debe ser A, B o C."

def update_producto(articulo, producto):
    """
    Cambia el artículo recibido al producto indicado.
    """
    pass

def update_stock(producto, delta):
    """
    Incrementa o decrementa el stock del producto en la cantidad recibida en
    en el parámetro «delta».
    El producto no debe tener trazabilidad. En otro caso deben usarse las
    funciones "crear_[bala|rollo...]".
    """
    pass

def delete_articulo(articulo):
    """
    Elimina el artículo en Murano mediante la creación de un movimiento de
    stock negativo de ese código de producto.
    """
    pass

def fire():
    """
    Lanza el proceso de importación de Murano de todos los movimientos de
    stock de la tabla temporal.
    """
    strerror = "No puede ejecutar código nativo de Murano. Necesita instalar"\
               " la biblioteca win32com y lanzar esta función desde una "\
               "plataforma donde se encuentre instalado Sage Murano."
    if not LCOEM:
        raise NotImplementedError, strerror
    burano = win32com.client.Dispatch("LogicControlOEM.OEM_EjecutaOEM")
    burano.InicializaOEM(CODEMPRESA,
                         "OEM",
                         "oem",
                         "",
                         "LOGONSERVER\\MURANO",
                         "GEOTEXAN")
    retCode = None
    operacion = "ENT_LisMunicipios" # TODO: Cambiar por la de verdad.
    burano.EjecutaOperacion(operacion, None, retCode)
