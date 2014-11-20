#!/usr/bin/env python
# -*- coding: utf-8 -*-

from informes.geninformes import give_me_the_name_baby, rectangulo, escribe
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import os
from tempfile import gettempdir
from formularios.utils import float2str

def etiqueta_rollos_portrait(rollos, mostrar_marcado = True):
    """
    Construye una etiqueta 
    """
    # Voy a tratar de reescribir esto regla en mano a ver si consigo 
    # cuadrarlo bien en la etiquetadora GEMINI.
    height = 12.55 * cm
    width = 8.4 * cm

    # Escala
    ancho = 7.2  # @UnusedVariable
    alto = 11.3
    scale = height / alto 
    
    # Medidas en papel.
    brand = (0.4 * scale, (alto - 2.0) * scale)
    logo = (3.8 * scale, (alto - 2.8) * scale)
    marcado = ((7.2/2) * scale, (alto - 3.0) * scale)
    column1 = .35 * scale
    column2 = logo[0]
    lineas = map(lambda x: (alto - x) * scale, 
                 [3.4 + (i*.6) for i in range(13)])
    
    # Datos
    data = {'brand': "EkoTex", 
            "c100": "UK Distributor", 
            "c108": "Product Name", 
            "c109": "Roll Number", 
            "c110": "Product Dimensions", 
            "c111": "Polymer", 
            "c112": "Product Classification", 
            "c200": "Geosynthetics Limited", 
            "c201": "Fleming Road", 
            "c202": "Harrowbrook Ind Est", 
            "c203": "Hinckley", 
            "c204": "Leicestershire", 
            "c205": "LE10 3 DU", 
            "c206": "Tel 01455 617139", 
            "c207": "Fax 01455 617140", 
            "c211": "Polypropylene", 
            "c212": "GTX-N", 
            "marcado": "0799-CPD", # Hay que incluirle el logotipo CE delante.
            }
    data["logo"] = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                   "..", "imagenes", "logo_ekotex.png")) 
                                                # Ruta absoluta 
                                                # a la imagen del logotipo. 
    try:
        logo_marcado = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       "..", "imagenes", "CE.png"))
    except IOError:     # Reportlab o PIL sin soporte libzip
        logo_marcado = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                       "..", "imagenes", "CE.gif"))
    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
        "etiqEkotex_%s.pdf" % give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo, pagesize = (width, height))

    for rollo in rollos:
        try:
            data["c208"] = rollo['objeto'].productoVenta.nombre
            data["c209"] = rollo['objeto'].numrollo
            cer = rollo['objeto'].productoVenta.camposEspecificosRollo
        except AttributeError:  # No se ha creado el objeto todavía. Es None.
            data["c208"] = rollo['productoVenta'].nombre
            data["c209"] = rollo['nrollo']
            cer = rollo['productoVenta'].camposEspecificosRollo
        data["c210"] = "%sm x %dm" % (float2str(cer.ancho, 
                                                autodec = True, 
                                                separador_decimales = "."),
                                      cer.metrosLineales) 
        rectangulo(c, (0.3 * cm, 0.3 * cm),
                      (width - 0.3 * cm, height - 0.3 * cm))
        c.setFont("Helvetica-Bold", 16)
        c.drawString(brand[0], brand[1], escribe(data['brand']))
        c.setFont("Helvetica-Bold", 10)
        c.drawString(column1, lineas[0], escribe(data['c100']))
        c.drawString(column1, lineas[8], escribe(data['c108']))
        c.drawString(column1, lineas[9], escribe(data['c109']))
        c.drawString(column1, lineas[10], escribe(data['c110']))
        c.drawString(column1, lineas[11], escribe(data['c111']))
        c.drawString(column1, lineas[12], escribe(data['c112']))
        c.drawString(column2, lineas[0], escribe(data['c200']))
        c.drawString(column2, lineas[1], escribe(data['c201']))
        c.drawString(column2, lineas[2], escribe(data['c202']))
        c.drawString(column2, lineas[3], escribe(data['c203']))
        c.drawString(column2, lineas[4], escribe(data['c204']))
        c.drawString(column2, lineas[5], escribe(data['c205']))
        c.drawString(column2, lineas[6], escribe(data['c206']))
        c.drawString(column2, lineas[7], escribe(data['c207']))
        c.drawString(column2, lineas[8], escribe(data['c208']))
        c.drawString(column2, lineas[9], escribe(data['c209']))
        c.drawString(column2, lineas[10], escribe(data['c210']))
        c.drawString(column2, lineas[11], escribe(data['c211']))
        c.drawString(column2, lineas[12], escribe(data['c212']))
        c.drawImage(data['logo'], logo[0], logo[1], 
                    2.5 * cm, 2.5 * cm)
        if mostrar_marcado and not rollo['defectuoso']:
            c.drawImage(logo_marcado, 
                        marcado[0] 
                            - ((0.30*cm
                                + c.stringWidth(data['marcado']) ) / 2),
                        marcado[1],
                        width = 0.35 * cm,
                        height = 6)
            c.setFont("Helvetica-Bold", 8)
            c.drawCentredString(marcado[0] + ((0.35*cm) / 2), 
                                marcado[1], 
                                escribe(data["marcado"]))

        #c.setPageRotation(-90)
        #c.rotate(-90)
        c.showPage()
    c.save()
    return nomarchivo


if __name__ == "__main__":
    from formularios.reports import abrir_pdf
    from framework import pclases
    from formularios.partes_de_fabricacion_rollos import build_etiqueta
    rollos = [pclases.Rollo.select(orderBy = "-id")[0]]
    pv = rollos[0].productoVenta
    rollos.append(pv.articulos[-1].rollo)
    rollos = [build_etiqueta(r)[0] for r in rollos]
    abrir_pdf(etiqueta_rollos_portrait(rollos, mostrar_marcado = True))

