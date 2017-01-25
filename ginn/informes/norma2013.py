#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A partir del 1 de julio de 2013 entra una normativa nueva que obliga a
este formato de etiqueta para geotextiles y geocem.
"""

import os
import textwrap
from collections import defaultdict
from tempfile import gettempdir
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from formularios.utils import float2str
from formularios import utils
from informes.geninformes import give_me_the_name_baby, rectangulo
from informes.geninformes import el_encogedor_de_fuentes_de_doraemon
from framework import pclases
from informes.barcode.code39 import Extended39


# pylint: disable=too-many-locals,too-many-branches,too-many-statements
def etiqueta_rollos_norma13(rollos, mostrar_marcado=True, lang="es"):
    """
    Construye una etiqueta por cada objeto rollo recibido y las devuelve
    en un solo PDF.
    Si lang = "en", etiqueta en inglés. Si "es", en castellano.
    """
    # Voy a tratar de reescribir esto regla en mano a ver si consigo
    # cuadrarlo bien en la etiquetadora GEMINI.
    alto = 12.55 * cm
    ancho = 8.4 * cm

    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
        "etiq_norma13_%s_%s.pdf" % (lang, give_me_the_name_baby()))
    c = canvas.Canvas(nomarchivo, pagesize = (ancho, alto))

    # Medidas:
    logo = (3.8 * cm * 0.75, 2.8 * cm * 0.75)
    margen = 0.1 * cm
    marcado = (((ancho - logo[0]) / 2) - margen, (alto - margen - logo[1] - 2))

    # Imágenes:
    logo_marcado = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   "..", "imagenes", "CE.png"))

    # Datos fijos:
    _data = {# "00 logo_marcado": None,
             "01 texto_marcado": "1035",    # Fijo
             "02 fabricado_por": "Fabricado por: %s",
             "03 direccion1": None,
             "04 direccion2": None,
             "05 telefono": "Tfno: %s, %s",
             "06 año_certif": None,
             "07 blanco1": "",      # Separador
             "08 dni": None,
             # "09 iso1": "De EN13249:2001 a EN13257:2001",  # Fijo
             # "10 iso2": "EN13265:2001",     # Fijo
             # La norma ha cambiado. Ahora nos regimos por la del 2014
             "09 iso1": "De EN13249:2014 a EN13257:2014",  # Fijo
             "10 iso2": "EN13265:2014",     # Fijo
             "11 blanco2": "",      # Separador
             "12 producto": None,
             "13 descripcion":
                 "Geotextil no tejido de polipropileno 100% virgen",
             "14 uso": "Uso: %s",
             "15 blanco3": "",      # Separador
             "16 codigo": "Partida: %d Rollo: %s",
             "17 caracteristicas": "Gramaje: %d g/m² Ancho: %s m Largo: %d m"
            }
    if lang == "en":
        for k in _data:
            _data[k] = helene_laanest(_data[k])
    estilos = defaultdict(lambda: ("Helvetica", 9)) # Helvética a 9 por defecto
    estilos["02 fabricado_por"] = ("Helvetica-Bold", 11)
    estilos["12 producto"] = ("Helvetica-Bold", 17)
    estilos["16 codigo"] = ("Helvetica-Bold", 17)
    estilos["17 caracteristicas"] = ("Helvetica-Bold", 13)
    data = {}
    # Datos de la BD dependientes del rollo
    for rollo in rollos:
        # 0.- ¿En qué formato viene? Si es el antiguo (datos en diccionario)
        #     me quedo con el objeto de pclases en sí.
        if isinstance(rollo, dict):
            try:
                productoVenta = rollo['productoVenta']
            except KeyError:
                # Si no me lo mandan en el diccionario, tiene que traer
                # el objeto rollo. Los partes mandan producto en dicccionario
                # porque a veces se genera etiqueta antes de crear el objeto
                # en la BD. Si viene de la consulta del listado de rollos,
                # como el rollo ya existe, me viene en el objeto toda la info.
                productoVenta = rollo['objeto'].productoVenta
            numpartida = utils.parse_numero(rollo['partida'])
            numrollo = rollo['nrollo']
            barcode39 = rollo['codigo39']
        else:
            productoVenta = rollo.productoVenta
            numpartida = rollo.partida.numpartida
            numrollo = rollo.numrollo
            barcode39 = rollo.codigo
        #   1.- Empresa
        try:
            # Si hay distribuidor, este texto cambia.
            distribuidor = productoVenta.camposEspecificosRollo.cliente
            if distribuidor:
                if lang == "en":
                    data["02 fabricado_por"] = helene_laanest(
                            "Distribuido por: %s") % (distribuidor.nombre)
                else:
                    data["02 fabricado_por"] = "Distribuido por: %s" % (
                                                        distribuidor.nombre)
                d = distribuidor.get_direccion_completa()
                dircompleta = textwrap.wrap(d,
                        (len(d) + max([len(w) for w in d.split()])) / 2)
                data["03 direccion1"] = dircompleta[0]
                data["04 direccion2"] = dircompleta[1]
                data["05 telefono"] = _data["05 telefono"] % (
                        distribuidor.telefono, distribuidor.email)
            else:   # Sigo con los datos de "propia empresa". Distribuyo yo.
                empresa = pclases.DatosDeLaEmpresa.select()[0]
                data["02 fabricado_por"] = _data["02 fabricado_por"] % (
                                                                empresa.nombre)
                data["03 direccion1"] = empresa.direccion + ", " + empresa.cp
                data["04 direccion2"] = ", ".join((empresa.ciudad,
                                                   empresa.provincia,
                                                   empresa.pais))
                data["05 telefono"] = _data["05 telefono"] % (empresa.telefono,
                                                              empresa.email)
            # Para los clientes sin teléfono o sin email:
            data["05 telefono"] = data["05 telefono"].strip()
            if data["05 telefono"].startswith(","):
                data["05 telefono"] = data["05 telefono"][1:]
            if data["05 telefono"].endswith(","):
                data["05 telefono"] = data["05 telefono"][:-1]
            if len(data["05 telefono"]) <= 7:
                data["05 telefono"] = ""
        except IndexError:
            data["02 fabricado_por"] = ""
            data["03 direccion1"] = ""
            data["04 direccion2"] = ""
            data["05 telefono"] = ""
    #   2.- Producto
        producto = productoVenta
        if producto.annoCertificacion != None:
            data["06 año_certif"] = "%02d" % producto.annoCertificacion
        else:
            data["06 año_certif"] = ""
        data["08 dni"] = producto.dni
        if len(producto.nombre) <= 50:
            data["12 producto"] = producto.nombre
        else:
            #if "//" in producto.nombre: # Productos Intermas
            #    data["11 blanco2"], data["12 producto"] = producto.nombre.split("//")
            #else:
            data["11 blanco2"], data["12 producto"] = utils.dividir_cadena(
                    producto.nombre)
            data["11 blanco2"] = data["11 blanco2"].strip()
            data["12 producto"] =data["12 producto"].strip()
            estilos["11 blanco2"] = estilos["12 producto"]
        if producto.uso:
            if lang == "en":
                data["14 uso"] = _data["14 uso"] % helene_laanest(producto.uso)
            else:
                data["14 uso"] = _data["14 uso"] % producto.uso
        else:
            data["14 uso"] = ""
    #   3.- Rollo
        data["16 codigo"] = _data["16 codigo"] % (numpartida,
                                                  numrollo)
        data["17 caracteristicas"] = _data["17 caracteristicas"] % (
            producto.camposEspecificosRollo.gramos,
            float2str(producto.camposEspecificosRollo.ancho,
                      autodec = True, separador_decimales = "."),
            producto.camposEspecificosRollo.metrosLineales)

        rectangulo(c, (margen, margen),
                      (ancho - margen, alto - margen))
        if mostrar_marcado:
            c.drawImage(logo_marcado,
                        marcado[0],
                        marcado[1],
                        width = logo[0], height = logo[1])
        else:
            data["01 texto_marcado"] = ""
        lineas = _data.keys()
        lineas.sort()
        # Posición y estilo de la primera línea.
        tamfuente = estilos[lineas[0]][1]
        y = alto - logo[1] - 0.1 * cm - tamfuente
        # ¿Cuánto me desplazaré de línea a línea?
        offset_y = (y - margen) / (len(lineas) + 3)   # 3 líneas para barcode
        for linea in lineas:
            try:
                dato = data[linea]
            except KeyError:    # Si no está en los valores asignados, busco
                                # en los originales. Deben ser datos fijos.
                dato = _data[linea]
            if dato is None:
                dato = ""
            c.setFont(*estilos[linea])
            #c.drawCentredString((ancho / 2),
            #                    y,
            #                    escribe(dato))
            el_encogedor_de_fuentes_de_doraemon(c,
                                                fuente=estilos[linea][0],
                                                tamannoini=estilos[linea][1],
                                                xini=margen,
                                                xfin=ancho - margen,
                                                y=y,
                                                texto=dato,
                                                alineacion=0)
            y -= offset_y
        # Lo último: el código de barras:
        #######################################################################
        c.saveState()
        y -= 2*offset_y
        y -= 0.2*cm
        codigo_rollo = barcode39
        codigobarras = Extended39(codigo_rollo, xdim=.060*cm)
        codigobarras.drawOn(c, margen-0.2*cm, y)
        xcode = ancho / 2.0
        ycode = 0.15*cm
        c.setFont("Courier-Bold", 9)
        try:
            c.drawCentredString(xcode, ycode, codigo_rollo, charSpace=0.25*cm)
        except TypeError:   # Versión antigua de ReportLab.
            c.drawCentredString(xcode, ycode, codigo_rollo)
        c.restoreState()
        # Y el QR de regalo
        try:
            from lib.pyqrcode import pyqrcode
            bidicode = pyqrcode.create(codigo_rollo)
            nomfichbidi = os.path.join(gettempdir(),
                                       "bidi_%s.svg" % give_me_the_name_baby())
            bidicode.svg(nomfichbidi, scale=3)
            from lib.svglib.svglib import svglib
            drawing = svglib.svg2rlg(nomfichbidi)
            drawing.drawOn(c, margen, alto - margen - 1.0*cm)
        except ImportError:
            pass    # No hay bidi porque no hay lxml instalado. Probablemente.
            print("No se generará código QR. Puede intentar lo siguiente:")
            print("C:\Python27\Scripts\easy_install.exe pip")
            print('pip install "D:\Informatica\Software\softwin python 2.7'
                  '\lxml-3.7.2-cp27-cp27m-win32.whl"')
        #######################################################################
        c.showPage()
    c.save()
    return nomarchivo

def helene_laanest(texto):
    # En honor a la profe de inglés,
    """recibe el texto (solo hay dos o tres
    posibles) y lo devuelve en inglés."""
    # Es una cutrada, pero los requisitos
    # han llegado tarde. Muy tarde.
    translate_table = defaultdict(lambda: texto)
    translate_table["Drenaje, filtración, refuerzo y separación"] \
            = "Drainage, filtration, reinforcement and separation"
    translate_table["Drenaje, filtración, refuerzo, separación y protección"]\
            = "Drainage, filtration, reinforcement, separation and protection"
    translate_table["Fibra de polipropileno virgen embolsada en papel hidrosoluble para su uso como aditivo del hormigón"] \
            = "100% polypropylene fibers in water-soluble paper bags used like an additive for concrete"
    translate_table["Fabricado por: %s"] = "Manufactured by: %s"
    translate_table["Distribuido por: %s"] = "Distributed by: %s"
    translate_table["Tfno: %s, %s"] = "Phone: %s, %s"
    translate_table["De EN13249:2014 a EN13257:2014"] = "From EN13249:2014 to EN13257:2014"
    translate_table["Geotextil no tejido de polipropileno 100% virgen"] = "Nonwoven geotextile of 100% polypropylene fibres."
    translate_table["Uso: %s"] = "Use: %s"
    translate_table["Partida: %d Rollo: %s"] = "Batch: %d Roll: %s"
    translate_table["Gramaje: %d g/m² Ancho: %s m Largo: %d m"] = "Mass per area: %d g/m² Width: %s m Length: %d m"
    return translate_table[texto]


def etiqueta_rollos_norma13_en(rollos, mostrar_marcado = True):
    """
    Construye una etiqueta por cada objeto rollo recibido y las devuelve
    en un solo PDF. Etiqueta en inglés.
    """
    return etiqueta_rollos_norma13(rollos, mostrar_marcado, lang = "en")

def crear_etiquetas_pales(pales, mostrar_marcado = True, lang = "es"):
    """
    Construye una etiqueta por cada objeto palé recibido y las devuelve
    en un solo PDF.
    Si lang = "en", etiqueta en inglés. Si "es", en castellano.
    """
    # Voy a tratar de reescribir esto regla en mano a ver si consigo
    # cuadrarlo bien en la etiquetadora GEMINI.
    alto = 12.55 * cm
    ancho = 8.4 * cm

    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
        "etiq_pale13_%s_%s.pdf" % (lang, give_me_the_name_baby()))
    c = canvas.Canvas(nomarchivo, pagesize = (ancho, alto))

    # Medidas:
    logo = (3.8 * cm * 0.75, 2.8 * cm * 0.75)
    margen = 0.1 * cm
    marcado = (((ancho - logo[0]) / 2) - margen, (alto - margen - logo[1] - 2))

    # Imágenes:
    logo_marcado = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   "..", "imagenes", "CE.png"))

    # Datos fijos:
    _data = {# "00 logo_marcado": None,
             "01 texto_marcado": "1035",    # Fijo
             "02 fabricado_por": "Fabricado por: %s",
             "03 direccion1": None,
             "04 direccion2": None,
             "05 telefono": "Tfno: %s, %s",
             "06 año_certif": None,
             "07 blanco1": "",      # Separador
             "08 dni": None,
             "09 iso1": "EN 14889-2:2008",  # Fijo
             "11 blanco2": "",      # Separador
             "12 producto": None,
             "13 descripcion": "",
             "14 uso": None,
             "15 blanco3": "",      # Separador
             "16 1 separador": "",     # Fijo
             "16 codigo": "%s %s",  # Código de palé y código de lote.
             "17 caracteristicas": None     # Descripción del producto.
            }
    if lang == "en":
        for k in _data:
            _data[k] = helene_laanest(_data[k])
    estilos = defaultdict(lambda: ("Helvetica-Bold", 11)) # Helvética a 11 por defecto
    estilos["01 texto_marcado"] = ("Times-Bold", 9)
    estilos["02 fabricado_por"] = ("Helvetica-Bold", 13)
    estilos["12 producto"] = ("Courier-Bold", 17)
    estilos["16 codigo"] = ("Courier-Bold", 17)
    estilos["17 caracteristicas"] = ("Helvetica-Bold", 15)
    data = {}
    # Datos de la BD dependientes del palé
    for pale in pales:
        # 0.- ¿En qué formato viene? Si es el antiguo (datos en diccionario)
        #     me quedo con el objeto de pclases en sí.
        productoVenta = pale.productoVenta
        numpartida = pale.partidaCem.codigo
        numpale = pale.codigo
        #   1.- Empresa
        try:
            # Si hay distribuidor, este texto cambia.
            distribuidor = pale.productoVenta.camposEspecificosBala.cliente
            if distribuidor:
                if lang == "en":
                    data["02 fabricado_por"] = helene_laanest(
                            "Distribuido por: %s") % (distribuidor.nombre)
                else:
                    data["02 fabricado_por"] = "Distribuido por: %s" % (
                                                        distribuidor.nombre)
                d = distribuidor.get_direccion_completa()
                dircompleta = textwrap.wrap(d,
                        (len(d) + max([len(w) for w in d.split()])) / 2)
                data["03 direccion1"] = dircompleta[0]
                data["04 direccion2"] = dircompleta[1]
                data["05 telefono"] = _data["05 telefono"] % (
                        distribuidor.telefono, distribuidor.email)
            else:   # Sigo con los datos de "propia empresa". Distribuyo yo.
                empresa = pclases.DatosDeLaEmpresa.select()[0]
                data["02 fabricado_por"] = _data["02 fabricado_por"] % (
                                                                empresa.nombre)
                data["03 direccion1"] = empresa.direccion + ", " + empresa.cp
                data["04 direccion2"] = ", ".join((empresa.ciudad,
                                                   empresa.provincia,
                                                   empresa.pais))
                data["05 telefono"] = _data["05 telefono"] % (empresa.telefono,
                                                              empresa.email)
            # Para los clientes sin teléfono o sin email:
            data["05 telefono"] = data["05 telefono"].strip()
            if data["05 telefono"].startswith(","):
                data["05 telefono"] = data["05 telefono"][1:]
            if data["05 telefono"].endswith(","):
                data["05 telefono"] = data["05 telefono"][:-1]
            if len(data["05 telefono"]) <= 7:
                data["05 telefono"] = ""
        except IndexError:
            data["02 fabricado_por"] = ""
            data["03 direccion1"] = ""
            data["04 direccion2"] = ""
            data["05 telefono"] = ""
    #   2.- Producto
        producto = productoVenta
        if producto.annoCertificacion != None:
            data["06 año_certif"] = "%02d" % producto.annoCertificacion
        else:
            data["06 año_certif"] = ""
        data["08 dni"] = producto.dni
        data["12 producto"] = producto.nombre
        if producto.uso:
            if lang == "en":
                produso = helene_laanest(producto.uso)
            else:
                produso = producto.uso
            produso = textwrap.wrap(produso,
                    (len(produso) + max([len(w) for w in produso.split()])) / 2)
            data["14 uso"] = produso[0]
            data["15 blanco3"] = produso[1]     # Era un separador, pero
                                                # necesito el espacio.
        else:
            data["14 uso"] = ""
    #   3.- Palé
        data["16 codigo"] = _data["16 codigo"] % (numpartida,
                                                  numpale)
        data["17 caracteristicas"] = producto.descripcion

        rectangulo(c, (margen, margen),
                      (ancho - margen, alto - margen))
        if mostrar_marcado:
            c.drawImage(logo_marcado,
                        marcado[0],
                        marcado[1],
                        width = logo[0], height = logo[1])
        else:
            data["01 texto_marcado"] = ""
        lineas = _data.keys()
        lineas.sort()
        # Posición y estilo de la primera línea.
        tamfuente = estilos[lineas[0]][1]
        y = alto - logo[1] - 0.1 * cm - tamfuente
        # ¿Cuánto me desplazaré de línea a línea?
        offset_y = (y - margen) / len(lineas)
        for linea in lineas:
            try:
                dato = data[linea]
            except KeyError:    # Si no está en los valores asignados, busco
                                # en los originales. Deben ser datos fijos.
                dato = _data[linea]
            if dato is None:
                dato = ""
            c.setFont(*estilos[linea])
            #c.drawCentredString((ancho / 2),
            #                    y,
            #                    escribe(dato))
            el_encogedor_de_fuentes_de_doraemon(c,
                                                fuente=estilos[linea][0],
                                                tamannoini=estilos[linea][1],
                                                xini=margen,
                                                xfin=ancho - margen,
                                                y=y,
                                                texto=dato,
                                                alineacion=0)
            y -= offset_y
        c.showPage()
    c.save()
    return nomarchivo

def test_rollos():
    from formularios.reports import abrir_pdf
    prods = [p for p in pclases.ProductoVenta.select()]
    prods.sort(key = lambda p: len(p.nombre), reverse = True)
    #for p in pclases.ProductoVenta.select():
    #    if "EkoTex" in p.nombre and " 06 " in p.descripcion and p.articulos:
    #        rollos = [a.rollo for a in p.articulos[:2]]
    #        break
    p = prods[0]
    rollos = [a.rollo for a in p.articulos[:2]]
    abrir_pdf(etiqueta_rollos_norma13(rollos, False))
    abrir_pdf(etiqueta_rollos_norma13_en(rollos))

def test_pales():
    from formularios.reports import abrir_pdf
    pales = pclases.Pale.select(orderBy = "-id")[:2]
    abrir_pdf(crear_etiquetas_pales(pales))
    import time
    time.sleep(1)
    abrir_pdf(crear_etiquetas_pales(pales, lang = "en"))

if __name__ == "__main__":
    test_rollos()

