#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Ajusta los consumos en base a la producción desde el 1 de octubre
en adelante.
"""

import sys
sys.path.append("../framework")
sys.path.append("../formularios")
import pclases
import utils
import mx, mx.DateTime

UNO_OCT = mx.DateTime.DateTimeFrom(day = 1, month = 10, year = 2006)

def inicializar_existencias():
    """
    Inicializa las existencias de los materiales (productoCompra) a 
    una cantidad determinada y "harcodeada".
    """
    # El diccionario de productos es: {"descripcion": cantidad, ...}
    productos = {   # Fibra
                 "FILTROS 200 DOS TELAS": 686.0, 
                 "ANTIUVI (PP 8006)": 8075.0, 
                 "COLORANTE FIBRA (NEGRO) (MASTERBASH NEGRO)": 6825.0, 
                 "ENSIMAJE": 4600.0, 
                 "FLEJES DE PLASTICO PARA BALAS": 57.0 * 3810,  # 57 bobina = 3810 metros lineales.
                 "PLASTICOS BALAS (Superior)": 1650.0, 
                 "PLASTICO BALAS EXTENSIBLE (Inferior)": 1683.0,
                 "FILTRO CORONA CIRCULAR": 227.0, 
                 "BIG BAGS 95X95X200 CM CIRCULAR, 1250, PLASTIFICADO": 500.0, 
                 "ENSIMAJE": 4600.0, 
                 "PALÉ": 0.0,
                    # Geotextiles
                 "ANTIESTATICOS (KATAX ESA 204)": 2400.0, 
                 'AGUJAS PLACAS DE 3,5"': 106000.0, 
                 "ENSIMAJE": 7100.0, 
                 "PRECINTO ADHESIVO": 8 * 32 * 132,     # Una caja = 32 cintas de 132 metros
                 "NUCLEOS DE CARTON": 2866.0, 
                 "GRAPAS PARA CASQUILLOS": 4 * 5000,    # Una caja = 5000 unidades
                 "CASQUILLOS DE PLASTICO": 16416.0, 
                 "PLASTICO SERIG. 6,0 M.": 2325.0, 
                 "SELBANA UN (con antiestatico incorporado)": 2500.0, 
                 'AGUJAS PLACAS DE 3"': 41000.0, 
                 "NUCLEOS DE CARTON 117": 71, 
                }
    for descripcion in productos:
        try:
            producto = pclases.ProductoCompra.select(pclases.ProductoCompra.q.descripcion == descripcion)[0]
        except IndexError:
            print "Producto %s no encontrado." % (descripcion)
            sys.exit(1)
        else:
            if pclases.ProductoCompra.select(pclases.ProductoCompra.q.descripcion == descripcion).count() > 1:
                print "¡UUUPSS! Más de un producto con misma descripción."
                sys.exit(2)
            producto.existencias = productos[descripcion]

def get_partes_balas_fabricadas(fecha = UNO_OCT):
    """
    Devuelve los partes de fabricación de balas (ojo, no bigbags) a 
    partir de la fecha recibida.
    """
    res = []
    partes = pclases.ParteDeProduccion.select(""" fecha >= '%s' AND observaciones LIKE '%%;%%;%%;%%;%%;%%' """ % fecha.strftime("%Y-%m-%d"))
    for parte in partes:
        if parte.articulos and parte.articulos[0].es_bala():
            res.append(parte)
    return res

def get_partes_rollos_fabricados(fecha = UNO_OCT):
    """
    Devuelve los partes de producción de rollos a partir de la fecha
    recibida.
    """
    res = []
    partes = pclases.ParteDeProduccion.select(""" fecha >= '%s' AND NOT observaciones LIKE '%%;%%;%%;%%;%%;%%' """ % fecha.strftime("%Y-%m-%d"))
    for parte in partes:
        if parte.articulos and parte.articulos[0].es_rollo():
            res.append(parte)
    return res

def get_partes_bigbags_fabricados(fecha = UNO_OCT):
    """
    Devuelve los partes de producción de bigbags (ojo, no balas) 
    de la fecha recibida en adelante.
    """
    res = []
    partes = pclases.ParteDeProduccion.select(""" fecha >= '%s' AND observaciones LIKE '%%;%%;%%;%%;%%;%%' """ % fecha.strftime("%Y-%m-%d"))
    for parte in partes:
        if parte.articulos and parte.articulos[0].es_bigbag():
            res.append(parte)
    return res

def anular_consumos(parte):
    """
    Anula los consumos que no sean de granza del parte actual.
    """
    for c in parte.consumos:
        if not c.es_de_granza():
            c.destroySelf()

def consumir(parte, consumos, producciones):
    """
    Consume los materiales según formula de los artículos 
    contenidos en el parte.
    En el diccionario consumos agrega (o actualiza) el consumo 
    del material correspondiente. 
    En el de producciones agrega (o actualiza) el número de kgs o 
    m² y bultos fabricados del producto del parte.
    """
    anular_consumos(parte)
    for articulo in parte.articulos:
        producto = articulo.productoVenta
        if producto not in producciones:
            producciones[producto] = {'bultos': 0, 'kilos': 0, 'metros': 0}
        producciones[producto]['bultos'] += 1
        kilos = articulo.peso
        if kilos != None:
            producciones[producto]['kilos'] += kilos
        metros = articulo.superficie
        if metros != None:
            producciones[producto]['metros'] += metros
        for consumoAdicional in producto.consumosAdicionales:
            consumido = consumoAdicional.consumir(articulo)
            if consumoAdicional.productoCompra not in consumos:
                consumos[consumoAdicional.productoCompra] = 0
            consumos[consumoAdicional.productoCompra] += consumido
    parte.unificar_consumos()


def mostrar_resumen(consumos, producciones):
    """
    Muestra por pantalla un resumen de los consumos y producciones 
    de los diccionarios recibidos.
    """
    print ".-------------------------------------."
    print "| Resumen de consumos y producciones: |"
    print "'-------------------------------------'"
    print "CONSUMOS:"
    for productoCompra in consumos:
        print "    %s: %s" % (productoCompra.descripcion, utils.float2str(consumos[productoCompra]))
    print "-" * 80
    for productoVenta in producciones:
        print "    %s: %d bultos; %s kilos; %s metros" % (productoVenta.descripcion, 
                                                          producciones[productoVenta]['bultos'],
                                                          producciones[productoVenta]['kilos'],
                                                          producciones[productoVenta]['metros'])

def get_entradas(fecha = UNO_OCT):
    """
    Devuelve las LDC de entradas correspondientes a una fecha 
    posterior al 1 de octubre.
    """
    ldcs = pclases.LineaDeCompra.select(""" albaran_entrada_id IN (SELECT id 
                                                                  FROM albaran_entrada 
                                                                  WHERE fecha >= '%s') """ % (fecha.strftime("%Y-%m-%d")))
    return ldcs

def aumentar_existencias(ldcs):
    """
    Aumenta las existencias de los productos de entrada 
    conforme a las líneas de compra recibidas (que deben 
    pertenecer a albaranes de entrada).
    """
    entradas = {}
    for ldc in ldcs:
        ldc.productoCompra.existencias += ldc.cantidad
        if ldc.productoCompra not in entradas:
            entradas[ldc.productoCompra] = ldc.cantidad
        else:
            entradas[ldc.productoCompra] += ldc.cantidad
    return entradas
    
def mostrar_resumen_entradas(entradas):
    """
    Muestra un resumen por producto de los aumentos de 
    existencias en productos de compra realizados a 
    partir de las líneas de compra de albaranes.
    """
    print ""
    print ".----------------------."
    print "| RESUMEN DE ENTRADAS: |"
    print "'----------------------'"
    for producto in entradas:
        print "    %s: %s" % (producto.descripcion, utils.float2str(entradas[producto]))


if __name__ == "__main__":
    consumos = {}
    producciones = {}
    print "Inicializando existencias..."
    inicializar_existencias()

    print "Actualizando entradas en almacén..."
    ldcs = get_entradas()
    entradas = aumentar_existencias(ldcs)

    print "Buscando producciones..."
    partes_balas = get_partes_balas_fabricadas()
    partes_rollos = get_partes_rollos_fabricados()
    partes_bigbags = get_partes_bigbags_fabricados()

    print "Rearrancando consumos..."
    for parte in partes_balas:
        consumir(parte, consumos, producciones)

    for parte in partes_rollos:
        consumir(parte, consumos, producciones)

    for parte in partes_bigbags:
        consumir(parte, consumos, producciones)

    mostrar_resumen_entradas(entradas)
    mostrar_resumen(consumos, producciones)

