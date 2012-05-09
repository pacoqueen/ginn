#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pclases

def descontar_material_adicional_balas(pdp, articulo, restar = True):
    """
    Descuenta el material adicional correspondiente al artículo según 
    la formulación que indique la línea de fabricación.
    Si "restar" es True, descuenta. Si es False, añade la cantidad (para
    cuando se elimine un rollo del parte, por ejemplo).
    Si es necesario, se dejará material con existencias en negativo, aunque
    se avisará al usuario de la incidencia.
    """
    linea = pclases.LineaDeProduccion.select(pclases.LineaDeProduccion.q.nombre.contains('de fibra'))
    if linea.count() == 0:
        print "WARNING: La línea de fibra no está correctamente dada de alta."
    else:
        linea = linea[0]
        formulacion = linea.formulacion
        for ca in [ca_con_p for ca_con_p in formulacion.consumosAdicionales if ca_con_p.productoCompra != None]:
            if ca.nombre == "antiuvi" and not articulo.productoVenta.camposEspecificosBala.antiuv:
                break
            if ca.nombre == "negro" and articulo.productoVenta.camposEspecificosBala.color.upper() != "NEGRO":
                break
            if ca.nombre == "titanio" and articulo.productoVenta.camposEspecificosBala.color.upper() != "TITANIO": 
                break
#                print " >>> Descuento de %s" % ca.productoCompra.descripcion
            if restar:
                cantidad = ca.cantidad * -1
            else:
                cantidad = ca.cantidad
            # WTF: Casos especiales (AAAARRRGHHHH)
            if "%" in ca.unidad:
                peso = articulo.bala.pesobala
                cantidad = (cantidad * peso) / 100
                antes = ca.productoCompra.existencias
#                ca.productoCompra.existencias += cantidad
                consumo = pclases.Consumo(parteDeProduccion = pdp,
                                          productoCompra = ca.productoCompra,
                                          actualizado = True,
                                          antes = -2,
#                                              despues = ca.productoCompra.existencias,
                                          despues = -2,
                                          cantidad = -cantidad)
            else: 
                antes = ca.productoCompra.existencias
#                ca.productoCompra.existencias += cantidad 
                consumo = pclases.Consumo(parteDeProduccion = pdp,
                                          productoCompra = ca.productoCompra,
                                          actualizado = True,
                                          antes = -2,
#                                              despues = ca.productoCompra.existencias,
                                          despues = -2,
                                          cantidad = -cantidad)
                # OJO: No verifico que las unidades del catálogo de productos sean las mismas que en la formulación


def descontar_material_adicional_rollos(pdp, articulo, restar = True):
    """
    Descuenta el material adicional correspondiente al artículo según 
    la formulación que indique la línea de fabricación.
    Si "restar" es True, descuenta. Si es False, añade la cantidad (para
    cuando se elimine un rollo del parte, por ejemplo).
    Si es necesario, se dejará material con existencias en negativo, aunque
    se avisará al usuario de la incidencia.
    """
    linea = pclases.LineaDeProduccion.select(pclases.LineaDeProduccion.q.nombre.contains('de geotextiles'))
    if linea.count() == 0:
        print "WARNING: La línea de geotextiles no está correctamente dada de alta."
    else:
        linea = linea[0]
        formulacion = linea.formulacion
        # Descuento de plástico.
        plastico = [ca.productoCompra for ca in formulacion.consumosAdicionales if "plastico" in ca.nombre][0] 
        if plastico != None:
            try:
                ca = [ca_con_p for ca_con_p in formulacion.consumosAdicionales 
                        if "plastico" in ca_con_p.nombre][0]
                if restar:
                    cantidad = ca.cantidad * -1
                else:
                    cantidad = ca.cantidad
                if "5.5" in ca.unidad:
                    ancho = articulo.productoVenta.camposEspecificosRollo.ancho
                    cantidad *= ancho/5.5
                antes = plastico.existencias
                plastico.existencias += cantidad
                consumo_plastico = pclases.Consumo(parteDeProduccion = pdp,
                                                   productoCompra = plastico,
                                                   actualizado = True,
                                                   antes = antes,
                                                   despues = plastico.existencias,
                                                   cantidad = -cantidad)
            except IndexError:
                print "WARNING: No se encontró formulación para el plástico de envolver"
        for ca in [ca_con_p for ca_con_p in formulacion.consumosAdicionales 
                    if ca_con_p.productoCompra != None and not "plastico" in ca_con_p.nombre]:
#                print " >>> Descuento de %s" % ca.productoCompra.descripcion
            if restar:
                cantidad = ca.cantidad * -1
            else:
                cantidad = ca.cantidad
            # WTF: Casos especiales (AAAARRRGHHHH)
            if "%" in ca.unidad:
                peso = articulo.rollo.peso
                cantidad = (cantidad * peso) / 100
                antes = ca.productoCompra.existencias
#                ca.productoCompra.existencias += cantidad
                consumo = pclases.Consumo(parteDeProduccion = pdp,
                                          productoCompra = ca.productoCompra,
                                          actualizado = True,
                                          antes = antes,
                                          despues = ca.productoCompra.existencias,
                                          cantidad = -cantidad)
            elif "u" and "5.5" in ca.unidad:
                ancho = articulo.productoVenta.camposEspecificosRollo.ancho
                anchosestandar = (1.83, 2.75, 5.5)  # NOTA: OJO: WTF: Very very very harcoded, gñe.
                for a in anchosestandar:
                    if ancho not in anchosestandar and ancho < a:
                        ancho = a
                cantidad *= ancho/5.5
                antes = ca.productoCompra.existencias
#                ca.productoCompra.existencias += cantidad
                consumo = pclases.Consumo(parteDeProduccion = pdp,
                                          productoCompra = ca.productoCompra,
                                          actualizado = True,
                                          antes = antes,
                                          despues = ca.productoCompra.existencias,
                                          cantidad = -cantidad)
                # Bueno. Empieza el más difícil todavía. Si se descuentan unidades completas por cada 5.5
                # metros de ancho, hay que vigilar que cada 2 ó 3 descuentos queden números enteros en la BD.
                # Si el ancho es 2.75 no hay problema. Pero si es 1.83 deben quedar las unidades como x.33, x.66 ó x.00
                if round(abs(1.0 - ca.productoCompra.existencias % 1.0), 1) == 0:
                    ca.productoCompra.existencias = round(ca.productoCompra.existencias, 0)
            elif "5.5" in ca.unidad:
                ancho = articulo.productoVenta.camposEspecificosRollo.ancho
                cantidad *= ancho/5.5
                antes = ca.productoCompra.existencias
#                ca.productoCompra.existencias += cantidad
                consumo = pclases.Consumo(parteDeProduccion = pdp,
                                          productoCompra = ca.productoCompra,
                                          actualizado = True,
                                          antes = antes,
                                          despues = ca.productoCompra.existencias,
                                          cantidad = -cantidad)
            else: 
                antes = ca.productoCompra.existencias
#                ca.productoCompra.existencias += cantidad 
                consumo = pclases.Consumo(parteDeProduccion = pdp,
                                          productoCompra = ca.productoCompra,
                                          actualizado = True,
                                          antes = antes,
                                          despues = ca.productoCompra.existencias,
                                          cantidad = -cantidad)
                # OJO: No verifico que las unidades del catálogo de productos sean las mismas que en la formulación

for pdp in pclases.ParteDeProduccion.select(orderBy = "fecha"):
    print "Descontando M.A. de parte %d (%s)..." % (pdp.id, pdp.fecha.strftime("%d/%m/%Y"))
    for a in pdp.articulos:
        if pdp.es_de_balas():
            print "    Descontando M.A. de balas..."
            descontar_material_adicional_balas(pdp, a)
        else:
            print "    Descontando M.A. de rollos..."
            descontar_material_adicional_rollos(pdp, a)

