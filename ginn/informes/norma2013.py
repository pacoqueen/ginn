#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A partir del 1 de julio de 2013 entra una normativa nueva que obliga a 
este formato de etiqueta para geotextiles y geocem.
"""

from informes.geninformes import give_me_the_name_baby, rectangulo, escribe
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import os
from tempfile import gettempdir
from formularios.utils import float2str
from framework import pclases

def etiqueta_rollos_portrait(rollos, mostrar_marcado = True):
    """
    Construye una etiqueta 
    """
    # Voy a tratar de reescribir esto regla en mano a ver si consigo 
    # cuadrarlo bien en la etiquetadora GEMINI.
    alto = 12.55 * cm
    ancho = 8.4 * cm

    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
        "etiq_norma13_%s.pdf" % give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo, pagesize = (ancho, alto))
    
    # Medidas:
    logo = (3.8 * cm, 2.8 * cm)
    margen = 0.2 * cm
    marcado = (((ancho - logo[0]) / 2) - margen, (alto - margen - logo[1]))
    
    # Imágenes:
    logo_marcado = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                   "..", "imagenes", "CE.png"))

    # Datos fijos:
    _data = {# "00 logo_marcado": None, 
             "01 texto_marcado": "0135",    # Fijo
             "02 fabricado_por": "Fabricado por: %s", 
             "03 direccion1": None, 
             "04 direccion2": None, 
             "05 telefono": "Tfno: +34 %s, %s", 
             "06 año_certif": None, 
             "07 blanco1": "",      # Separador
             "08 dni": None, 
             "09 iso1": "De EN13249:2001 a EN13257:2001",  # Fijo
             "10 iso2": "EN13265:2001",     # Fijo
             "11 blanco2": "",      # Separador
             "12 producto": None, 
             "13 descripcion": 
                 "Geotextil no tejido de polipropileno 100% virgen", 
             "14 uso": None, 
             "15 blanco3": "",      # Separador 
             "16 codigo": "Partida: %d Rollo: %d", 
             "17 caracteristicas": "Gramaje: %d g/m² Ancho: %.1f m Largo: %d m" 
            }
    data = {}
    # Datos de la BD dependientes del rollo
    #   1.- Empresa
    try:
        empresa = pclases.DatosDeLaEmpresa.select()[0]
        data["02 fabricado_por"] = _data["02 fabricado_por"] % empresa.nombre
        data["03 direccion1"] = empresa.direccion + ", " + empresa.cp
        data["04 direccion2"] = ", ".join((empresa.ciudad, 
                                           empresa.provincia, 
                                           empresa.pais))
        data["05 telefono"] = _data["05 telefono"] % (empresa.telefono, 
                                                      empresa.email)
    except IndexError:
        data["02 fabricado_por"] = ""
        data["03 direccion1"] = ""
        data["04 direccion2"] = ""
        data["05 telefono"] = ""
    for rollo in rollos:
    #   2.- Producto
        producto = rollo.productoVenta
        data["06 año_certif"] = producto.annoCertificacion
        data["08 dni"] = producto.dni
        data["12 producto"] = producto.nombre
        data["14 uso"] = producto.uso
    #   3.- Rollo
        data["16 codigo"] = _data["16 codigo"] % (rollo.partida.numpartida, 
                                                  rollo.numrollo)
        data["17 caracteristicas"] = _data["17 caracteristicas"] % (
            producto.camposEspecificosRollo.gramos, 
            producto.camposEspecificosRollo.ancho, 
            producto.camposEspecificosRollo.metrosLineales)


        rectangulo(c, (margen, margen),
                      (ancho - margen, alto - margen))
        if mostrar_marcado: 
            c.drawImage(logo_marcado, 
                        marcado[0], 
                        marcado[1],
                        width = logo[0], height = logo[1])
        lineas = _data.keys()
        lineas.sort()
        c.setFont("Helvetica", 10)
        y = alto - logo[1] - 0.1 * cm - 10
        offset_y = (y - margen) / len(lineas)
        for linea in lineas:
            try:
                dato = data[linea]
            except KeyError:
                dato = _data[linea]
            if dato is None:
                dato = ""
            c.drawCentredString((ancho / 2), 
                                y, 
                                escribe(dato))
            y -= offset_y
        #c.setPageRotation(-90)
        #c.rotate(-90)
        c.showPage()
    c.save()
    return nomarchivo


if __name__ == "__main__":
    from formularios.reports import abrir_pdf
    from formularios.partes_de_fabricacion_rollos import build_etiqueta
    rollos = [pclases.Rollo.select(orderBy = "-id")[0]]
    pv = rollos[0].productoVenta
    rollos.append(pv.articulos[-1].rollo)
    abrir_pdf(etiqueta_rollos_portrait(rollos))

