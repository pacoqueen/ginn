#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008 Francisco José Rodríguez Bogado,                   #
# (pacoqueen@users.sourceforge.net)                                           #
#                                                                             #
# This file is part of GeotexInn.                                             #
#                                                                             #
# GeotexInn is free software; you can redistribute it and/or modify           #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation; either version 2 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# GeotexInn is distributed in the hope that it will be useful,                #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with GeotexInn; if not, write to the Free Software                    #
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA  #
###############################################################################

###############################################################################
## Script para importar las tablas de BlancoPerez en CSV a ginn.             ##
###############################################################################

import mx, mx.DateTime, os, sys

from framework import pclases
from formularios import utils


import csv

def main():
    """
    Ejecuta secuencialmente las importaciones.
    """
    archivos = {"FacturaVenta": "/home/tpv/Migrate/Albaranes.csv", 
                "Cliente": "/home/tpv/Migrate/Clientes.csv", 
                "contiene": "/home/tpv/Migrate/Contiene.csv", 
                "LineaDeVenta": "/home/tpv/Migrate/Detalles_de_pedido.csv", 
                "Cobro": "/home/tpv/Migrate/Pagos.csv", 
                "PedidoVenta": "/home/tpv/Migrate/Pedidos.csv", 
                #"ProductoCompra": "/home/tpv/Migrate/Productos.csv", 
                "ProductoCompra": "productos.csv", 
                "Proveedor": "/home/tpv/Migrate/Proveedores.csv", 
                "AlbaranEntrada": "/home/tpv/Migrate/recepcion.csv", 
                "Ticket": "/home/tpv/Migrate/ventas.csv"}
    
    #tarifas, tipos_de_material, contador = crear_datos_iniciales()
    tarifas, tipos_de_material, contador = buscar_datos_iniciales()
    # proveedores = importar_proveedores(archivos["Proveedor"])
    productos = importar_productos(archivos["ProductoCompra"], tarifas, tipos_de_material)
    #clientes = importar_clientes(archivos["Cliente"], tarifas, contador)
    #ventas = importar_ventas(archivos["Ticket"])

def importar_ventas(nomarchivo):
    """
    Importa las ventas como tickets.
    Devuelve un diccionario de ID de venta y la LDV relacionada.
    """
    f = open(nomarchivo)
    r = csv.reader(f)
    res = {}
    fila_actual = 0
    for venta in r:
        if fila_actual == 0:
            fila_actual += 1
            continue
        fila_actual += 1
        for i in xrange(len(venta)):
            c = venta[i]
            c = c.strip()
            venta[i] = c.replace("\xd3", "Ó").replace("\xba", "º").replace("\xd1", "Ñ").replace("\xaa", "ª")
        id, numventa, codigo, precioventa, preciocosto, cantidad, bazzura, fecha, impuesto, descripcion = venta
        numventas = {}
        numventa = int(numventa)
        precio = utils._float(precioventa)
        cantidad = utils._float(cantidad)
        strfecha, strhora = fecha.split()
        dia, mes, anno = map(int, strfecha.split("/")); horas, minutos, segundos = map(int, strhora.split(":"))
        fecha = mx.DateTime.DateTimeFrom(day = dia, month = mes, year = anno, hour = horas, minute = minutos, second = segundos)
        if numventa not in numventas:
            numventas[numventa] = pclases.Ticket(fechahora = fecha, numticket = numventa)
        PC = pclases.ProductoCompra
        productos = PC.select(pclases.OR(pclases.AND(PC.q.codigo.contains(codigo), 
                                                     PC.q.descripcion.contains(descripcion[:5])), 
                                         pclases.AND(PC.q.descripcion.contains(codigo), 
                                                     PC.q.descripcion.contains(descripcion[:5]))))
        if productos.count() == 0:
            print "No se encontró el producto con código %s y descripción %s. Ticket %d. Me lo salto." % (codigo, descripcion, numventa)
        elif productos.count() > 1:
            print "Se econtró más de un producto con código %s y descripción %s. Ticket %d. Me lo salto." % (codigo, descripcion, numventa)
        else:
            producto = productos[0]
            ldv = pclases.LineaDeVenta(productoCompra = producto, 
                                       ticket = numventas[numventa], 
                                       pedidoVenta = None, 
                                       facturaVenta = None, 
                                       productoVenta = None, 
                                       albaranSalida = None, 
                                       fechahora = fecha, 
                                       cantidad = cantidad, 
                                       precio = precio, 
                                       descuento = 0.0)
            res[id] = ldv
    return res

def importar_clientes(nomarchivo, tarifas, contador):
    """
    Importa los clientes y devuelve un diccionario {"id": objeto_cliente} (OJO: id es string)
    """
    f = open(nomarchivo)
    r = csv.reader(f)
    res = {}
    fila_actual = 0
    for cliente in r:
        if fila_actual == 0:
            fila_actual += 1
            continue
        fila_actual += 1
        for i in xrange(len(cliente)):
            c = cliente[i]
            c = c.strip()
            c = c.replace("\xd3", "Ó").replace("\xba", "º").replace("\xd1", "Ñ").replace("\xaa", "ª")
            cliente[i] = c
        id, cif, nombre, contacto, apellidos, direccion, poblacion, provincia, cp, telefono, notas, ccc = cliente
        print "Importando cliente %s..." % (nombre)
        c = pclases.Cliente(proveedor = None, 
                            cuentaOrigen = None, 
                            tarifa = tarifas[0],
                            contador = contador,
                            cliente = None,
                            telefono = telefono,
                            nombre = nombre,
                            cif = cif,
                            direccion = direccion,
                            pais = 'España', 
                            ciudad = poblacion,
                            provincia = provincia,
                            cp = cp,
                            iva = 0.16,
                            direccionfacturacion = direccion,
                            paisfacturacion = 'España',
                            ciudadfacturacion = poblacion,
                            provinciafacturacion = provincia,
                            cpfacturacion = cp,
                            nombref = nombre,
                            email = '',
                            contacto = " ".join((contacto, apellidos)),
                            observaciones = "\n".join((notas, ccc)),
                            vencimientos = '',
                            formadepago = '',
                            documentodepago = '',
                            diadepago = '',
                            inhabilitado = False,
                            motivo = '',
                            porcentaje = 0.0,
                            enviarCorreoAlbaran = False,
                            enviarCorreoFactura = False,
                            enviarCorreoPacking = False,
                            fax = '')
        res[id] = c
    return res

def buscar_datos_iniciales():
    """
    Crea algunos datos básicos (tarifas, tipos de materiales, etc...)
    """
    t0 = pclases.Tarifa.select(pclases.Tarifa.q.nombre == 'Tarifa venta público')[0]
    t1 = pclases.Tarifa.select(pclases.Tarifa.q.nombre == 'Tarifa 1')[0]
    t2 = pclases.Tarifa.select(pclases.Tarifa.q.nombre == 'Tarifa 2')[0]
    t3 = pclases.Tarifa.select(pclases.Tarifa.q.nombre == 'Tarifa 3')[0]
    pinturas = pclases.TipoDeMaterial.select(pclases.TipoDeMaterial.q.descripcion.contains("Pintur"))[0]
    barnices = pclases.TipoDeMaterial.select(pclases.TipoDeMaterial.q.descripcion.contains("Barni"))[0]
    contador = pclases.Contador.select(pclases.Contador.q.prefijo == "F2007/")[0]
    return (t0, t1, t2, t3), {"pinturas": pinturas, "barnices": barnices}, contador

def crear_datos_iniciales():
    """
    Crea algunos datos básicos (tarifas, tipos de materiales, etc...)
    """
    t0 = pclases.Tarifa(nombre = 'Tarifa venta público', observaciones = '', periodoValidezIni = None, periodoValidezFin = None)
    t1 = pclases.Tarifa(nombre = 'Tarifa 1', observaciones = '', periodoValidezIni = None, periodoValidezFin = None)
    t2 = pclases.Tarifa(nombre = 'Tarifa 2', observaciones = '', periodoValidezIni = None, periodoValidezFin = None)
    t3 = pclases.Tarifa(nombre = 'Tarifa 3', observaciones = '', periodoValidezIni = None, periodoValidezFin = None)
    pinturas = pclases.TipoDeMaterial(descripcion = "Pintura")
    barnices = pclases.TipoDeMaterial(descripcion = "Barniz")
    contador = pclases.Contador(prefijo = "F2007/", sufijo = "", contador = 0)
    return (t0, t1, t2, t3), {"pinturas": pinturas, "barnices": barnices}, contador

def importar_productos(nomarchivo, tarifas, tipos_de_material):
    """
    Importa los productos de compra.
    Devuelve un diccionario con los IDs del archivo y el objeto 
    ProductoCompra que le ha correspondido.
    """
    f = open(nomarchivo)
    #r = csv.reader(f)
    r = csv.reader(f, delimiter = ";", lineterminator = "\n")
    res = {}
    fila_actual = 0
    for producto in r:
        if fila_actual == 0:
            fila_actual += 1
            continue
        fila_actual += 1
        for i in xrange(len(producto)):
            c = producto[i]
            c = c.strip()
            #producto[i] = c.replace("\xd3", "Ó").replace("\xba", "º").replace("\xd1", "Ñ")
            producto[i] = c.replace("?", "").replace("%", "")
        #id, codigo, precio, descripcion, color, tamanno, cifproveedor, existencias, minimo, preciocosto, ganancia, tarifa1, tarifa2, tarifa3, ean13 = producto
        id, codigo, precio, descripcion, color, tamanno, cifproveedor, existencias, minimo, preciocosto, ganancia, tarifa1, tarifa2, tarifa3, ean13 = producto
        descripcion = " ".join((descripcion, color, tamanno))
        try:
            minimo = utils._float(minimo)
        except ValueError, msg:
            print "Excepción capturada: %s. Valor erróneo para mínimo: %s" % (msg, minimo)
            minimo = 0.0
        try:
            existencias = utils._float(existencias)
        except ValueError, msg:
            print "Excepción capturada: %s. Valor erróneo para existencias: %s" % (msg, existencias)
            existencias = 0.0
        try:
            preciocosto = utils._float(preciocosto)
        except ValueError, msg:
            print "Excepción capturada: %s. Valor erróneo para preciocosto: %s" % (msg, preciocosto)
            preciocosto = 0.0
        try:
            ganancia = utils.parse_porcentaje(ganancia, True)
        except ValueError, msg:
            print "Excepción capturada: %s. Valor erróneo para ganancia: %s" % (msg, ganancia)
            ganancia = 0.0
        try:
            tarifa1 = utils.parse_porcentaje(tarifa1, True)
        except ValueError, msg:
            print "Excepción capturada: %s. Valor erróneo para tarifa1: %s" % (msg, tarifa1)
            tarifa1 = 0.0
        try:
            tarifa2 = utils.parse_porcentaje(tarifa2, True)
        except ValueError, msg:
            print "Excepción capturada: %s. Valor erróneo para tarifa2: %s" % (msg, tarifa2)
            tarifa2 = 0.0
        try:
            tarifa3 = utils.parse_porcentaje(tarifa3, True)
        except ValueError, msg:
            print "Excepción capturada: %s. Valor erróneo para tarifa3: %s" % (msg, tarifa3)
            tarifa3 = 0.0
        if ean13 != "":
            if codigo != "":
                descripcion = "%s (%s)" % (descripcion, codigo) 
            codigo = ean13
        print "Importando producto %s..." % (descripcion)
        #pc = pclases.ProductoCompra(tipoDeMaterial = "TITAN" in descripcion.upper() and tipos_de_material["pinturas"] or None, 
        #                            descripcion = descripcion,
        #                            codigo = codigo,
        #                            unidad = '',
        #                            minimo = minimo,
        #                            existencias = existencias,
        #                            precioDefecto = preciocosto,
        #                            controlExistencias = True,
        #                            fvaloracion = 'Precio medio')
        if ean13 != "":
            pcs = pclases.ProductoCompra.select(pclases.AND(pclases.ProductoCompra.q.codigo == ean13, 
                                                            pclases.ProductoCompra.q.descripcion.contains(codigo)))
        else:
            pcs = pclases.ProductoCompra.select(pclases.ProductoCompra.q.codigo == codigo)
        if pcs.count() != 1:
            print "No encuentro %s" % (descripcion), "ean13:", ean13, "codigo", codigo
            pcs = pclases.ProductoCompra.select(pclases.ProductoCompra.q.descripcion == str(descripcion.decode("ISO8859", "replace")))
            if pcs.count() != 1:
                print "Sigo sin encontrar %s" % (descripcion), "ean13:", ean13, "codigo", codigo
                pcs = pclases.ProductoCompra.select(pclases.ProductoCompra.q.descripcion.contains(str(descripcion.decode("ISO8859", "replace"))))
                if pcs.count() != 1:
                    print "Todavía no encuentro %s" % (descripcion), "ean13:", ean13, "codigo", codigo
                    pcs = pclases.ProductoCompra.select(pclases.ProductoCompra.q.codigo == codigo)
                    if pcs.count() != 1:
                        print "Todavía sigo sin encontrar %s" % (descripcion), "ean13:", ean13, "codigo", codigo
                        pcs = pclases.ProductoCompra.select(pclases.ProductoCompra.q.codigo.contains(codigo[-7:]))
                        if pcs.count() != 1:
                            print "Ni siquiera encuentro un trozo (%s) del código para %s" % (codigo[-7:], descripcion)
                            try:
                                pcs = pclases.ProductoCompra.select(pclases.ProductoCompra.q.descripcion.contains(descripcion[:descripcion.rindex("(")]))
                            except ValueError:
                                print " >>> Lo creo a manoplaler."
                                pc = pclases.ProductoCompra(tipoDeMaterial = "TITAN" in descripcion.upper() and tipos_de_material["pinturas"] or None, 
                                                            descripcion = descripcion,
                                                            codigo = codigo,
                                                            unidad = '',
                                                            minimo = minimo,
                                                            existencias = existencias,
                                                            precioDefecto = preciocosto,
                                                            controlExistencias = True,
                                                            fvaloracion = 'Precio medio')
                            if pcs.count() == 1:
                                pc = pcs[0]

                            else:
                                print "No hay nada que hacer con %s." % (descripcion), descripcion[:descripcion.rindex("(")]
                                print " >>> Lo creo a manopla."
                                pc = pclases.ProductoCompra(tipoDeMaterial = "TITAN" in descripcion.upper() and tipos_de_material["pinturas"] or None, 
                                                            descripcion = descripcion,
                                                            codigo = codigo,
                                                            unidad = '',
                                                            minimo = minimo,
                                                            existencias = existencias,
                                                            precioDefecto = preciocosto,
                                                            controlExistencias = True,
                                                            fvaloracion = 'Precio medio')

                                #import sys
                                #sys.exit()
                        else:
                            pc = pcs[0]
                            print "Cambiando código %s del producto %s por el código %s (no lo encontré por descripción)" % (pc.codigo, pc.descripcion, codigo)
                            pc.codigo = codigo
                    else:
                        pc = pcs[0]
                else:
                    pc = pcs[0]
                    print "Cambiando descripción del producto %s por %s" % (pc.descripcion, "%s (%s)" % (descripcion, codigo))
                    pc.descripcion = "%s (%s)" % (descripcion, codigo)
            else:
                pc = pcs[0]
                print "Cambiando código %s del producto %s por el código %s" % (pc.descripcion, pc.codigo, codigo)
                pc.codigo = codigo
        else:
            pc = pcs[0]
        tarifas[0].asignarTarifa(pc, preciocosto * (1 + ganancia))
        tarifas[1].asignarTarifa(pc, preciocosto * (1 + tarifa1))
        tarifas[2].asignarTarifa(pc, preciocosto * (1 + tarifa2))
        tarifas[3].asignarTarifa(pc, preciocosto * (1 + tarifa3))
        pc.precioDefecto = preciocosto
        res[id] = pc
    return res

def importar_proveedores(nomarchivo):
    """
    Importa los proveedores.
    Lee los proveedores del archivo, los inserta en la table Proveedores y 
    devuelve un diccionario con los CIFs del archivo y el objeto proveedor en 
    la nueva tabla que le ha correspondido.
    """
    f = open(nomarchivo)
    r = csv.reader(f)
    res = {}
    fila_actual = 0
    for cif, nombre, telefono1, telefono2, direccion, cp, poblacion, provincia, actividad, pendiente in r:
        if fila_actual == 0:
            fila_actual += 1
            continue
        fila_actual += 1
        _cif = cif
        cif = cif.replace(".", "").replace("-", "").replace(" ", "").strip()
        telefono1 = telefono1.replace("(", "").replace(")", "").replace("-", "").replace(" ", "").strip()
        telefono2 = telefono2.replace("(", "").replace(")", "").replace("-", "").replace(" ", "").strip()
        print "Importando proveedor %s..." % (nombre)
        p = pclases.Proveedor(nombre = nombre, 
                              cif = cif, 
                              direccion = direccion, 
                              pais = "España", 
                              ciudad = poblacion, 
                              provincia = provincia, 
                              cp = cp, 
                              telefono = telefono1, 
                              fax = telefono2, 
                              contacto = '', 
                              observaciones = actividad, 
                              direccionfacturacion = direccion, 
                              paisfacturacion = 'España', 
                              ciudadfacturacion = poblacion, 
                              provinciafacturacion = provincia, 
                              cpfacturacion = cp, 
                              email = '', 
                              formadepago = '0', 
                              documentodepago = '', 
                              vencimiento = '0', 
                              diadepago = '', 
                              correoe = '', 
                              web = '', 
                              banco = '', 
                              swif = '', 
                              iban = '', 
                              cuenta = '', 
                              inhabilitado = False, 
                              motivo = '', 
                              iva = 0.16, 
                              nombreBanco = '')
        res[_cif] = p
    return res


if __name__ == "__main__":
    main()

