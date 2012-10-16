#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Como los números de rollo no aparecerán en la etiqueta, se pueden generar 
estáticamente. Así que simplemente devuelvo un diseño ya hecho en PDF.
"""

import os
from tempfile import gettempdir
from geninformes import give_me_the_name_baby
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

def etiqueta_nied(rollos, mostrar_marcado = False):
    """
    Genera un PDF con tantas páginas iguales como número de elementos tenga 
    la lista de rollos recibida.
    Si el rollo va a 0.80 m de ancho, devuelve en cada página el diseño 
    de GNT11_080.pdf. En otro caso usa el GNT11_120.pdf por defecto.
    """
    try:
        pv = rollos[0]['objeto'].productoVenta
    except (IndexError, AttributeError):
        nomarchivo = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                                  "GNT11_120.pdf"))
    else:
        modelo = "GNT11_120.png"
        try:
            if pv.camposEspecificosRollo.ancho == 0.8:
                modelo = "GNT11_080.png"
        except AttributeError:
            pass    # Uso modelo por defecto.
        pagina = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                              modelo))
        height = 12.55 * cm
        width = 8.4 * cm
        nomarchivo = os.path.join(gettempdir(),
                "etiqNied_%s.pdf" % give_me_the_name_baby())
        c = canvas.Canvas(nomarchivo, pagesize = (width, height))
        for rollo in rollos:
            c.drawImage(pagina, 0, 0, width, height)
            c.showPage()
        c.save()
    return nomarchivo


if __name__ == "__main__":
    # For testing purposes only.
    print etiqueta_nied(range(10))

