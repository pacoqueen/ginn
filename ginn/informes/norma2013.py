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
from reportlab.pdfgen import canvas as reportlabcanvas
from reportlab.lib.units import cm, inch
from formularios.utils import float2str
from formularios import utils
from informes.geninformes import give_me_the_name_baby, rectangulo
from informes.geninformes import el_encogedor_de_fuentes_de_doraemon
from framework import pclases
# pylint:disable=ungrouped-imports
from informes.barcode.code39 import Extended39
from informes.barcode.code128 import Code128


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
                              "etiq_norma13_{}_{}.pdf".format(
                                  lang, give_me_the_name_baby()))
    canvas = reportlabcanvas.Canvas(nomarchivo, pagesize=(ancho, alto))

    # Medidas:
    logo = (3.8 * cm * 0.75, 2.8 * cm * 0.75)
    margen = 0.1 * cm
    marcado = (((ancho - logo[0]) / 2) - margen, (alto - margen - logo[1] - 2))

    # Imágenes:
    logo_marcado = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "imagenes", "CE.png"))

    # Datos fijos:
    # pylint: disable=bad-continuation
    _data = {  # "00 logo_marcado": None,
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
    estilos = defaultdict(lambda: ("Helvetica", 9))  # Helvética 9 por defecto
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
                producto_venta = rollo['productoVenta']
            except KeyError:
                # Si no me lo mandan en el diccionario, tiene que traer
                # el objeto rollo. Los partes mandan producto en dicccionario
                # porque a veces se genera etiqueta antes de crear el objeto
                # en la BD. Si viene de la consulta del listado de rollos,
                # como el rollo ya existe, me viene en el objeto toda la info.
                producto_venta = rollo['objeto'].productoVenta
            try:
                numpartida = utils.parse_numero(rollo['partida'])
            except KeyError:
                numpartida = utils.parse_numero(rollo['lote'])
            numrollo = rollo['nrollo']
            barcode39 = rollo['codigo39']
        else:
            producto_venta = rollo.productoVenta
            numpartida = rollo.partida.numpartida
            numrollo = rollo.numrollo
            barcode39 = rollo.codigo
        #   1.- Empresa
        try:
            # Si hay distribuidor, este texto cambia.
            distribuidor = producto_venta.camposEspecificosRollo.cliente
            if distribuidor:
                if lang == "en":
                    data["02 fabricado_por"] = helene_laanest(
                            "Distribuido por: %s") % (distribuidor.nombre)
                else:
                    data["02 fabricado_por"] = "Distribuido por: %s" % (
                                                        distribuidor.nombre)
                dird = distribuidor.get_direccion_completa()
                dircompleta = textwrap.wrap(
                        dird,
                        (len(dird) + max([len(w) for w in dird.split()])) / 2)
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
        producto = producto_venta
        if producto.annoCertificacion is not None:
            data["06 año_certif"] = "%02d" % producto.annoCertificacion
        else:
            data["06 año_certif"] = ""
        data["08 dni"] = producto.dni
        if len(producto.nombre) <= 50:
            data["12 producto"] = producto.nombre
        else:
            data["11 blanco2"], data["12 producto"] = utils.dividir_cadena(
                    producto.nombre)
            data["11 blanco2"] = data["11 blanco2"].strip()
            data["12 producto"] = data["12 producto"].strip()
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
                      autodec=True, separador_decimales="."),
            producto.camposEspecificosRollo.metrosLineales)

        rectangulo(canvas, (margen, margen), (ancho - margen, alto - margen))
        if mostrar_marcado:
            canvas.drawImage(logo_marcado,
                             marcado[0],
                             marcado[1],
                             width=logo[0], height=logo[1])
        else:
            data["01 texto_marcado"] = ""
        lineas = _data.keys()
        lineas.sort()
        # Posición y estilo de la primera línea.
        tamfuente = estilos[lineas[0]][1]
        crd_y = alto - logo[1] - 0.1 * cm - tamfuente
        # ¿Cuánto me desplazaré de línea a línea?
        offset_y = (crd_y - margen) / (len(lineas) + 3)   # 3 líneas barcode
        for linea in lineas:
            try:
                dato = data[linea]
            except KeyError:    # Si no está en los valores asignados, busco
                                # en los originales. Deben ser datos fijos.
                dato = _data[linea]
            if dato is None:
                dato = ""
            canvas.setFont(*estilos[linea])
            # canvas.drawCentredString((ancho / 2),
            #                     crd_y,
            #                     escribe(dato))
            el_encogedor_de_fuentes_de_doraemon(canvas,
                                                fuente=estilos[linea][0],
                                                tamannoini=estilos[linea][1],
                                                xini=margen,
                                                xfin=ancho - margen,
                                                y=crd_y,
                                                texto=dato,
                                                alineacion=0)
            crd_y -= offset_y
        # Lo último: el código de barras:
        #######################################################################
        canvas.saveState()
        crd_y -= 2*offset_y
        crd_y -= 0.2*cm
        codigo_rollo = barcode39
        codigobarras = Extended39(codigo_rollo, xdim=.065*cm)
        codigobarras.drawOn(canvas, margen-0.5*cm, crd_y)
        xcode = ancho / 2.0
        ycode = 0.15*cm
        canvas.setFont("Courier-Bold", 9)
        try:
            canvas.drawCentredString(xcode, ycode, codigo_rollo,
                                     charSpace=0.25*cm)
        except TypeError:   # Versión antigua de ReportLab.
            canvas.drawCentredString(xcode, ycode, codigo_rollo)
        canvas.restoreState()
        # Y el QR de regalo
        # # De momento lo desactivo porque nuestras pistolas no lo reconocen.
        # try:
        #    from lib.pyqrcode import pyqrcode
        #    bidicode = pyqrcode.create(codigo_rollo)
        #    nomfichbidi = os.path.join(gettempdir(),
        #                           "bidi_%s.svg" % give_me_the_name_baby())
        #    bidicode.svg(nomfichbidi, scale=3)
        #    from lib.svglib.svglib import svglib
        #    drawing = svglib.svg2rlg(nomfichbidi)
        #    drawing.drawOn(canvas, margen - 0.25*cm,
        #                   alto - margen - 3.0*cm + 0.25*cm)
        # except ImportError:
        #    pass    # No hay bidi porque no hay lxml instalado. Probablemente.
        #    print("No se generará código QR. Puede intentar lo siguiente:")
        #    print("C:\Python27\Scripts\easy_install.exe pip")
        #    print('pip install "D:\Informatica\Software\softwin python 2.7'
        #          '\lxml-3.7.2-cp27-cp27m-win32.whl"')
        #######################################################################
        canvas.showPage()
        # Y ahora la etiqueta adicional por si se pierde la otra y para cargar.
        create_etiqueta_backup_rollo(canvas, rollo)
        canvas.showPage()
    canvas.save()
    return nomarchivo


def create_etiqueta_backup_rollo(canvas, rollo):
    """
    Genera en el canvas (pero hace el showPage) una etiqueta adicional
    principalmente con un código de barras enorme para poder leerla desde
    lejos a la hora de cargar el rollo.
    """
    # Dimensiones estándar de la etiqueta.
    alto = 12.55 * cm
    ancho = 8.4 * cm
    margen = 0.1 * cm
    # Parámetros a pintar que obtener del objeto recibido.
    try:
        try:
            producto = rollo['productoVenta'].descripcion
        except KeyError:
            # Si no me lo mandan en el diccionario, tiene que traer
            # el objeto rollo. Los partes mandan producto en dicccionario
            # porque a veces se genera etiqueta antes de crear el objeto
            # en la BD. Si viene de la consulta del listado de rollos,
            # como el rollo ya existe, me viene en el objeto toda la info.
            producto = rollo['objeto'].productoVenta.descripcion
        codigo_rollo = rollo['codigo39']
    except TypeError:  # He recibido un objeto directamente.
        producto = rollo.productoVenta.descripcion
        codigo_rollo = rollo.codigo
    # Dimensiones para pintar la información.
    canvas.saveState()
    xcode = ancho / 2.0
    ycode = 0.15*cm
    xprod = xcode
    yprod = alto - margen - 7
    # ## El código de rollo:
    canvas.setFont("Courier-Bold", 9)
    try:
        canvas.drawCentredString(xcode, ycode, codigo_rollo, charSpace=0.25*cm)
    except TypeError:   # Versión antigua de ReportLab.
        canvas.drawCentredString(xcode, ycode, codigo_rollo)
    # ## El producto:
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(xprod, yprod, producto)
    # ## El rectángulo exterior
    canvas.rotate(90)
    # ## El rectángulo exterior mejor lo quito para que la pistola no se
    # ## confunda.
    # canvas.rect(margen, -(ancho-margen), alto - 2*margen, ancho - 2*margen,
    #             stroke=1)
    # ## El código de barras. Rotado para ganar anchura:
    crd_x = (-5.75*margen)-(0.2*cm)
    crd_y = -(ancho - 2*margen)
    xlineablanca = 5.9*cm
    mil = 0.001*inch    # Por definición.
    # Con 40 debería llegar hasta a 9.7 metros de distancia la lectura o
    # 37.5 m la versión Auto Range.
    # altobarcodetotal = (ancho-4*margen)  # Ancho, en realidad. Está rotado.
    mils = 50*mil
    altobarcode = ancho - xlineablanca - 2*margen
    # codigobarras1 = Extended39(codigo_rollo, xdim=mils, height=altobarcode)
    codigobarras1 = Code128(codigo_rollo, xdim=mils, height=altobarcode)
    codigobarras1.drawOn(canvas, crd_x, crd_y)
    canvas.rotate(-90)
    # ## El otro código de barras.
    mils = 24*mil
    altobarcode = alto - 2*margen - 2*9
    codigobarras2 = Code128(codigo_rollo, xdim=mils, height=altobarcode)
    crd_x = -4.0 * margen
    crd_y = margen + 9
    codigobarras2.drawOn(canvas, crd_x, crd_y)
    # ## Línea auxiliar por donde está el pin roto de la impresora:
    # ## Mejor la quito para que la pistola no la cofunda con otra barra.
    # canvas.line(xlineablanca, margen, xlineablanca, alto - margen - 9)
    canvas.restoreState()


def create_etiqueta_backup_bala(canvas, bala):
    """
    Genera en el canvas (pero hace el showPage) una etiqueta adicional
    principalmente con un código de barras enorme para poder leerla desde
    lejos a la hora de cargar el bala.
    """
    # Dimensiones estándar de la etiqueta.
    ancho = 12.55 * cm
    alto = 8.4 * cm
    margen = 0.1 * cm
    # Parámetros a pintar que obtener del objeto recibido.
    try:
        try:
            producto = bala['productoVenta'].descripcion
        except KeyError:
            # Si no me lo mandan en el diccionario, tiene que traer
            # el objeto bala. Los partes mandan producto en dicccionario
            # porque a veces se genera etiqueta antes de crear el objeto
            # en la BD. Si viene de la consulta del listado de rollos,
            # como el bala ya existe, me viene en el objeto toda la info.
            producto = bala['objeto'].productoVenta.descripcion
        codigo_rollo = bala['codigo']
    except TypeError:  # He recibido un objeto directamente.
        producto = bala.productoVenta.descripcion
        codigo_rollo = bala.codigo
    # Dimensiones para pintar la información.
    canvas.saveState()
    xcode = ancho / 2.0
    ycode = 0.2*cm
    xprod = xcode
    yprod = alto - margen - 0.3*cm
    # ## El código de bala:
    canvas.setFont("Courier-Bold", 9)
    try:
        canvas.drawCentredString(xcode, ycode, codigo_rollo, charSpace=0.25*cm)
    except TypeError:   # Versión antigua de ReportLab.
        canvas.drawCentredString(xcode, ycode, codigo_rollo)
    # ## El producto:
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(xprod, yprod, producto)
    # ## El rectángulo exterior
    # ## El rectángulo exterior mejor lo quito para que la pistola no se
    # ## confunda.
    # canvas.rect(margen, -(ancho-margen), alto - 2*margen, ancho - 2*margen,
    #             stroke=1)
    # ## El código de barras.
    crd_x = 0.0*cm
    crd_y = margen + 0.5*cm
    mil = 0.001*inch    # Por definición.
    # Con 40 debería llegar hasta a 9.7 metros de distancia la lectura o
    # 37.5 m la versión Auto Range.
    mils = 45*mil
    anchobarcode = ancho - (2.0*margen)
    # codigobarras1 = Extended39(codigo_rollo, xdim=mils, height=altobarcode)
    codigobarras1 = Code128(codigo_rollo, xdim=mils, width=anchobarcode)
    codigobarras1.drawOn(canvas, crd_x, crd_y)
    # ## El otro código de barras.
    canvas.rotate(90)
    mils = 24*mil
    altobarcode = alto + 2.9*cm
    codigobarras2 = Code128(codigo_rollo, xdim=mils, height=altobarcode)
    crd_x = 1.7*cm
    crd_y = -alto - 3.5*cm
    codigobarras2.drawOn(canvas, crd_x, crd_y)
    # ## Línea auxiliar por donde está el pin roto de la impresora:
    # ## Mejor la quito para que la pistola no la cofunda con otra barra.
    # canvas.line(xlineablanca, margen, xlineablanca, alto - margen - 9)
    canvas.rotate(-90)
    canvas.restoreState()


def create_etiqueta_backup_bigbag(canvas, bigbag):
    """
    Genera en el canvas (pero hace el showPage) una etiqueta adicional
    principalmente con un código de barras enorme para poder leerla desde
    lejos a la hora de cargar el bigbag.
    """
    # Dimensiones estándar de la etiqueta.
    alto = 12.55 * cm
    ancho = 8.4 * cm
    margen = 0.1 * cm
    # Parámetros a pintar que obtener del objeto recibido.
    try:
        try:
            producto = bigbag['productoVenta'].descripcion
        except KeyError:
            # Si no me lo mandan en el diccionario, tiene que traer
            # el objeto bigbag. Los partes mandan producto en dicccionario
            # porque a veces se genera etiqueta antes de crear el objeto
            # en la BD. Si viene de la consulta del listado de bigbags,
            # como el bigbag ya existe, me viene en el objeto toda la info.
            producto = bigbag['objeto'].productoVenta.descripcion
        codigo_bigbag = bigbag['codigo39']
    except TypeError:  # He recibido un objeto directamente.
        producto = bigbag.productoVenta.descripcion
        codigo_bigbag = bigbag.codigo
    # Dimensiones para pintar la información.
    canvas.saveState()
    xcode = ancho / 2.0
    ycode = 0.15*cm
    xprod = xcode
    yprod = alto - margen - 7
    # ## El código de bigbag:
    canvas.setFont("Courier-Bold", 9)
    try:
        canvas.drawCentredString(xcode, ycode, codigo_bigbag,
                                 charSpace=0.25*cm)
    except TypeError:   # Versión antigua de ReportLab.
        canvas.drawCentredString(xcode, ycode, codigo_bigbag)
    # ## El producto:
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(xprod, yprod, producto)
    # ## El rectángulo exterior
    canvas.rotate(90)
    # ## El rectángulo exterior mejor lo quito para que la pistola no se
    # ## confunda.
    # canvas.rect(margen, -(ancho-margen), alto - 2*margen, ancho - 2*margen,
    #             stroke=1)
    # ## El código de barras. Rotado para ganar anchura:
    crd_x = (-5.75*margen)-(0.2*cm)
    crd_y = -(ancho - 2*margen)
    xlineablanca = 5.9*cm
    mil = 0.001*inch    # Por definición.
    # Con 40 debería llegar hasta a 9.7 metros de distancia la lectura o
    # 37.5 m la versión Auto Range.
    # altobarcodetotal = (ancho-4*margen)  # Ancho, en realidad. Está rotado.
    mils = 50*mil
    altobarcode = ancho - xlineablanca - 2*margen
    # codigobarras1 = Extended39(codigo_bigbag, xdim=mils, height=altobarcode)
    codigobarras1 = Code128(codigo_bigbag, xdim=mils, height=altobarcode)
    codigobarras1.drawOn(canvas, crd_x, crd_y)
    canvas.rotate(-90)
    # ## El otro código de barras.
    mils = 24*mil
    altobarcode = alto - 2*margen - 2*9
    codigobarras2 = Code128(codigo_bigbag, xdim=mils, height=altobarcode)
    crd_x = -4.0 * margen
    crd_y = margen + 9
    codigobarras2.drawOn(canvas, crd_x, crd_y)
    # ## Línea auxiliar por donde está el pin roto de la impresora:
    # ## Mejor la quito para que la pistola no la cofunda con otra barra.
    # canvas.line(xlineablanca, margen, xlineablanca, alto - margen - 9)
    canvas.restoreState()


def create_etiqueta_backup_pale(canvas, pale):
    """
    Genera en el canvas (pero hace el showPage) una etiqueta adicional
    principalmente con un código de barras enorme para poder leerla desde
    lejos a la hora de cargar el pale.
    """
    # Dimensiones estándar de la etiqueta.
    alto = 12.55 * cm
    ancho = 8.4 * cm
    margen = 0.1 * cm
    # Parámetros a pintar que obtener del objeto recibido.
    try:
        try:
            producto = pale['productoVenta'].descripcion
        except KeyError:
            # Si no me lo mandan en el diccionario, tiene que traer
            # el objeto pale. Los partes mandan producto en dicccionario
            # porque a veces se genera etiqueta antes de crear el objeto
            # en la BD. Si viene de la consulta del listado de pales,
            # como el pale ya existe, me viene en el objeto toda la info.
            producto = pale['objeto'].productoVenta.descripcion
        codigo_pale = pale['codigo39']
    except TypeError:  # He recibido un objeto directamente.
        producto = pale.productoVenta.descripcion
        codigo_pale = pale.codigo
    # Dimensiones para pintar la información.
    canvas.saveState()
    xcode = ancho / 2.0
    ycode = 0.15*cm
    xprod = xcode
    yprod = alto - margen - 7
    # ## El código de pale:
    canvas.setFont("Courier-Bold", 9)
    try:
        canvas.drawCentredString(xcode, ycode, codigo_pale,
                                 charSpace=0.25*cm)
    except TypeError:   # Versión antigua de ReportLab.
        canvas.drawCentredString(xcode, ycode, codigo_pale)
    # ## El producto:
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(xprod, yprod, producto)
    # ## El rectángulo exterior
    canvas.rotate(90)
    # ## El rectángulo exterior mejor lo quito para que la pistola no se
    # ## confunda.
    # canvas.rect(margen, -(ancho-margen), alto - 2*margen, ancho - 2*margen,
    #             stroke=1)
    # ## El código de barras. Rotado para ganar anchura:
    crd_x = -0.7*cm
    crd_y = -(ancho - 2*margen)
    mil = 0.001*inch    # Por definición.
    # Con 40 debería llegar hasta a 9.7 metros de distancia la lectura o
    # 37.5 m la versión Auto Range.
    # altobarcodetotal = (ancho-4*margen)  # Ancho, en realidad. Está rotado.
    mils = 35*mil
    altobarcode = 2*cm
    # codigobarras1 = Extended39(codigo_pale, xdim=mils, height=altobarcode)
    codigobarras1 = Code128(codigo_pale, xdim=mils, height=altobarcode)
    codigobarras1.drawOn(canvas, crd_x, crd_y)
    canvas.rotate(-90)
    # ## El otro código de barras.
    mils = 17*mil
    altobarcode = alto - 2*margen - 2*9
    codigobarras2 = Code128(codigo_pale, xdim=mils, height=altobarcode)
    crd_x = -4.0 * margen
    crd_y = margen + 9
    codigobarras2.drawOn(canvas, crd_x, crd_y)
    # ## Línea auxiliar por donde está el pin roto de la impresora:
    # ## Mejor la quito para que la pistola no la cofunda con otra barra.
    # canvas.line(xlineablanca, margen, xlineablanca, alto - margen - 9)
    canvas.restoreState()


def helene_laanest(texto):
    # En honor a la profe de inglés,
    """recibe el texto (solo hay dos o tres
    posibles) y lo devuelve en inglés."""
    # Es una cutrada, pero los requisitos
    # han llegado tarde. Muy tarde.
    translate_table = defaultdict(lambda: texto)
    translate_table["Drenaje, filtración, refuerzo y separación"] \
        = "Drainage, filtration, reinforcement and separation"
    translate_table["Drenaje, filtración, refuerzo, separación"] \
        = "Drainage, filtration, reinforcement, separation"
    translate_table["Drenaje, filtración, refuerzo, separación y protección"]\
        = "Drainage, filtration, reinforcement, separation and protection"
    translate_table["Drenaje, filtración, refuerzo, separación, protección"]\
        = "Drainage, filtration, reinforcement, separation, protection"
    translate_table["Fibra de polipropileno virgen embolsada en papel "
                    "hidrosoluble para su uso como aditivo del hormigón"] \
        = "100% polypropylene fibers in water-soluble paper bags used "\
          "like an additive for concrete"
    translate_table["Fabricado por: %s"] = "Manufactured by: %s"
    translate_table["Distribuido por: %s"] = "Distributed by: %s"
    translate_table["Tfno: %s, %s"] = "Phone: %s, %s"
    translate_table["De EN13249:2014 a EN13257:2014"] = "From EN13249:2014 "\
        "to EN13257:2014"
    translate_table["Geotextil no tejido de polipropileno 100% virgen"
                    ] = "Nonwoven geotextile of 100% polypropylene fibres."
    translate_table["Uso: %s"] = "Use: %s"
    translate_table["Partida: %d Rollo: %s"] = "Batch: %d Roll: %s"
    translate_table["Gramaje: %d g/m² Ancho: %s m Largo: %d m"
                    ] = "Mass per area: %d g/m² Width: %s m Length: %d m"
    translate_table["Filtración, separación"] = "Filtration, separation"
    translate_table["Filtración, separación, protección"] = "Filtration, "\
        "separation, protection"
    return translate_table[texto]


def etiqueta_rollos_norma13_en(rollos, mostrar_marcado=True):
    """
    Construye una etiqueta por cada objeto rollo recibido y las devuelve
    en un solo PDF. Etiqueta en inglés.
    """
    return etiqueta_rollos_norma13(rollos, mostrar_marcado, lang="en")


def crear_etiquetas_pales(pales, mostrar_marcado=True, lang="es"):
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
                              "etiq_pale13_%s_%s.pdf" % (
                                  lang, give_me_the_name_baby()))
    canvas = reportlabcanvas.Canvas(nomarchivo, pagesize=(ancho, alto))

    # Medidas:
    logo = (3.8 * cm * 0.75, 2.8 * cm * 0.75)
    margen = 0.1 * cm
    marcado = (((ancho - logo[0]) / 2) - margen, (alto - margen - logo[1] - 2))

    # Imágenes:
    logo_marcado = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "imagenes", "CE.png"))

    # Datos fijos:
    # pylint: disable=bad-continuation
    _data = {  # "00 logo_marcado": None,
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
    estilos = defaultdict(lambda: ("Helvetica-Bold", 11))  # Helv. 11 defecto
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
        producto_venta = pale.productoVenta
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
                dird = distribuidor.get_direccion_completa()
                dircompleta = textwrap.wrap(
                        dird,
                        (len(dird) + max([len(w) for w in dird.split()])) / 2)
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
        producto = producto_venta
        if producto.annoCertificacion is not None:
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
            produso = textwrap.wrap(
                produso,
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

        rectangulo(canvas, (margen, margen),
                   (ancho - margen, alto - margen))
        if mostrar_marcado:
            canvas.drawImage(logo_marcado,
                             marcado[0],
                             marcado[1],
                             width=logo[0],
                             height=logo[1])
        else:
            data["01 texto_marcado"] = ""
        lineas = _data.keys()
        lineas.sort()
        # Posición y estilo de la primera línea.
        tamfuente = estilos[lineas[0]][1]
        crd_y = alto - logo[1] - 0.1 * cm - tamfuente
        # ¿Cuánto me desplazaré de línea a línea?
        offset_y = (crd_y - margen) / len(lineas)
        for linea in lineas:
            try:
                dato = data[linea]
            except KeyError:    # Si no está en los valores asignados, busco
                                # en los originales. Deben ser datos fijos.
                dato = _data[linea]
            if dato is None:
                dato = ""
            canvas.setFont(*estilos[linea])
            # canvas.drawCentredString((ancho / 2),
            #                     crd_y,
            #                     escribe(dato))
            el_encogedor_de_fuentes_de_doraemon(canvas,
                                                fuente=estilos[linea][0],
                                                tamannoini=estilos[linea][1],
                                                xini=margen,
                                                xfin=ancho - margen,
                                                y=crd_y,
                                                texto=dato,
                                                alineacion=0)
            crd_y -= offset_y
        canvas.showPage()
        # Y ahora la etiqueta adicional por si se pierde la otra y para cargar.
        create_etiqueta_backup_pale(canvas, pale)
        canvas.showPage()
    canvas.save()
    return nomarchivo


def crear_etiquetas_bigbags(bigbags, mostrar_marcado=True, lang="es"):
    """
    Construye una etiqueta por cada objeto bigbag recibido y las devuelve
    en un solo PDF.
    Si lang = "en", etiqueta en inglés. Si "es", en castellano.
    """
    # Voy a tratar de reescribir esto regla en mano a ver si consigo
    # cuadrarlo bien en la etiquetadora GEMINI.
    alto = 12.55 * cm
    ancho = 8.4 * cm

    # Creo la hoja
    nomarchivo = os.path.join(
        gettempdir(),
        "etiq_bigbag13_%s_%s.pdf" % (lang, give_me_the_name_baby()))
    canvas = reportlabcanvas.Canvas(nomarchivo, pagesize=(ancho, alto))

    # Medidas:
    logo = (3.8 * cm * 0.75, 2.8 * cm * 0.75)
    margen = 0.1 * cm
    marcado = (((ancho - logo[0]) / 2) - margen, (alto - margen - logo[1] - 2))

    # Imágenes:
    logo_marcado = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "imagenes", "CE.png"))

    # Datos fijos:
    # pylint: disable=bad-continuation
    _data = {  # "00 logo_marcado": None,
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
             # "16 1 separador": "",     # Fijo
             "16 codigo": "Lote {} · Bigbag {}",  # Código bigbag y cód. lote.
             "17 caracteristicas": "Corte: {} mm · Peso: {} kg/br"  # Cort&Peso
            }
    if lang == "en":
        for k in _data:
            _data[k] = helene_laanest(_data[k])
    estilos = defaultdict(lambda: ("Helvetica-Bold", 11))  # Helv. 11 defecto
    estilos["01 texto_marcado"] = ("Times-Bold", 9)
    estilos["02 fabricado_por"] = ("Helvetica-Bold", 13)
    estilos["12 producto"] = ("Courier-Bold", 17)
    estilos["14 uso"] = ("Helvetica-Bold", 10)
    estilos["15 blanco3"] = ("Helvetica-Bold", 10)
    estilos["16 codigo"] = ("Courier-Bold", 13)
    estilos["17 caracteristicas"] = ("Helvetica-Bold", 14)
    data = {}
    # Datos de la BD dependientes del bigbag
    for bigbag in bigbags:
        # 0.- ¿En qué formato viene? Si es el antiguo (datos en diccionario)
        #     me quedo con el objeto de pclases en sí.
        producto_venta = bigbag.articulo.productoVenta
        numpartida = bigbag.articulo.loteCem.codigo
        numbigbag = bigbag.codigo
        #   1.- Empresa
        try:
            # Si hay distribuidor, este texto cambia.
            ceb = bigbag.articulo.productoVenta.camposEspecificosBala
            distribuidor = ceb.cliente
            if distribuidor:
                if lang == "en":
                    data["02 fabricado_por"] = helene_laanest(
                            "Distribuido por: %s") % (distribuidor.nombre)
                else:
                    data["02 fabricado_por"] = "Distribuido por: %s" % (
                                                        distribuidor.nombre)
                dird = distribuidor.get_direccion_completa()
                dircompleta = textwrap.wrap(
                    dird,
                    (len(dird) + max([len(w) for w in dird.split()])) / 2)
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
        producto = producto_venta
        if producto.annoCertificacion is not None:
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
            if len(produso) > 30:   # Wrap si el texto es largo.
                produso = textwrap.wrap(
                    produso,
                    (len(produso) + max([len(w) for w in produso.split()]))/2)
                data["14 uso"] = produso[0]
                data["15 blanco3"] = produso[1]     # Era un separador, pero
                # necesito el espacio.
            else:
                data["14 uso"] = produso
        else:
            data["14 uso"] = ""
    #   3.- Bigbag
        data["16 codigo"] = _data["16 codigo"].format(numpartida,
                                                      numbigbag)
        corte = producto.camposEspecificosBala.corte
        peso = float2str(bigbag.articulo.peso_bruto)
        corte_peso = _data["17 caracteristicas"].format(corte, peso)
        data["17 caracteristicas"] = corte_peso

        rectangulo(canvas, (margen, margen),
                   (ancho - margen, alto - margen))
        if mostrar_marcado:
            canvas.drawImage(logo_marcado,
                             marcado[0],
                             marcado[1],
                             width=logo[0], height=logo[1])
        else:
            data["01 texto_marcado"] = ""
        lineas = _data.keys()
        lineas.sort()
        # Posición y estilo de la primera línea.
        tamfuente = estilos[lineas[0]][1]
        crd_y = alto - logo[1] - 0.1 * cm - tamfuente
        # ¿Cuánto me desplazaré de línea a línea?
        offset_y = (crd_y - margen) / len(lineas)
        for linea in lineas:
            try:
                dato = data[linea]
            except KeyError:    # Si no está en los valores asignados, busco
                                # en los originales. Deben ser datos fijos.
                dato = _data[linea]
            if dato is None:
                dato = ""
            canvas.setFont(*estilos[linea])
            # canvas.drawCentredString((ancho / 2),
            #                     crd_y,
            #                     escribe(dato))
            el_encogedor_de_fuentes_de_doraemon(canvas,
                                                fuente=estilos[linea][0],
                                                tamannoini=estilos[linea][1],
                                                xini=margen,
                                                xfin=ancho - margen,
                                                y=crd_y,
                                                texto=dato,
                                                alineacion=0)
            crd_y -= offset_y
        canvas.showPage()
        # Y ahora la etiqueta adicional por si se pierde la otra y para cargar.
        create_etiqueta_backup_bigbag(canvas, bigbag)
        canvas.showPage()
    canvas.save()
    return nomarchivo


def _build_dict_etiqueta_articulo_bala(articulo):
    """
    Construye y devuelve un diccionario con los campos que espera imprimir la
    etiqueta para balas.
    """
    b = articulo.bala
    producto = articulo.productoVenta
    campos = producto.camposEspecificosBala
    elemento = {'descripcion': producto.descripcion,
                'codigo': b.codigo,
                'color': str(campos.color),
                'peso': str(b.pesobala),
                'lote': str(b.lote.numlote),
                'tipo': campos.tipoMaterialBala and str(
                    campos.tipoMaterialBala.descripcion) or "",
                'longitud': str(campos.corte),
                'nbala': str(b.numbala),
                'dtex': str(campos.dtex),
                'dia': utils.str_fecha(b.fechahora),
                'acabado': campos.antiuv and '1' or '0',
                'codigoBarra': producto.codigo,
                'objeto': articulo}
    return elemento


def crear_etiquetas_balas(balas, mostrar_marcado=True, lang="es"):
    """
    Construye una etiqueta por cada objeto bala recibido y las devuelve
    en un solo PDF.
    Si lang = "en", etiqueta en inglés. Si "es", en castellano.

    Crea etiquetas para las balas de
    un parte de la línea de fibra.
    Una por etiqueta del tamaño estándar de la impresora CAB: 12.55 x 8.4.
    Lleva el código especial para Domenech en horizontal.
    «seriep» es la serie del pedido y si no es None, se muestra en los
    3 primeros dígitos.
    «numped» es el número de pedido procedente de Domenech y si no es None se
    muestra en 6 dígitos tras la serie (si la hubiera).
    Estos dos grupos de dígitos opcionales («seriep» y «numped») son comunes
    a toda la serie de balas de las que se generarán las etiquetas.
    El formato completo es:
    * 3 dígitos: serie del pedido, completado con ceros por la izquierda.
    * 6 dígitos: número de pedido, completado con ceros por la izquierda.
    *-7-dígitos:-código-de-producto:--- YA NO (tercera vez que vuelven a ser 6)
    * 6 dígitos: código de producto:
         - 007336 FIBRA PP 6.7 Dtx NATURAL.
         - 007337 FIBRA PP 6.7 Dtx NEGRO.
         - 007674 FIBRA PP 4.5 Dtx NEGRO.
         - 007852 FIBRA PP 4.5 Dtx NATURAL.
    * 10 dígitos: número de lote, completado con ceros por la izquierda.
    * 15 dígitos: número de bala, completado con ceros por la izquierda.
    * 3 dígitos: parte entera del peso de la bala en kilogramos,
                 completado con ceros por la izquierda.
    * 2 dígitos: parte decimal del peso de la bala en kilogramos,
                 completado con ceros por la derecha.

    Por ejemplo, el código correspondiente a una bala de fibra negra de
    polipropileno de 6.7 dtex, correspondiente al lote 660, de número
    57394, con 286.50 kg de peso y solicitada en el pedido 4/2158; sería:
    004002158007337000000066000000000005739428650
    007337000000066000000000005739428650 Si no lleva serie ni pedido.
    """
    # TODO: De momento solo español. No hay inglés. Se ignora el parámetro.
    from reportlab.pdfgen import canvas as pdfcanvas
    from informes.geninformes import escribe, _build_codigo_domenech
    try:
        import Image
    except ImportError:
        from PIL import Image
    width = 12.55 * cm
    height = 8.4 * cm
    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
                              "dh_etiqbala_%s.pdf" % give_me_the_name_baby())
    canvas = pdfcanvas.Canvas(nomarchivo, pagesize=(width, height))
    ancho, alto = width, height
    # arribaArriba significa linea de "arriba" de los cuadros de "Arriba"
    # El 0 vertical es el borde de abajo
    # El 0 horizontal es el margen derecho
    arriba = alto - 1.45*cm
    # arriba = alto - 5
    abajo = 5
    # abajo = 1.45*cm
    izq = width - 5
    der = 5     # ¿Va a resultar al final que también soy disléxico?
    xLogo = der + 0.5 * cm
    yLogo = arriba - 1.3 * cm
    xIzquierda = 20
    xDerecha = ancho/2 + 0.25*inch
    yPrimeraLinea = yLogo - 0.8*inch
    ySegundaLinea = yPrimeraLinea - 0.31*inch
    yTerceraLinea = ySegundaLinea - 0.31*inch
    yCuartaLinea = yTerceraLinea - 0.31*inch
    yQuintaLinea = yCuartaLinea - 0.31*inch
    xCodigo = xDerecha + 3.50 * cm
    yCodigo = arriba - 3.75 * cm
    for bala in balas:  # @UnusedVariable
        if not bala:    # Es None. Por lo que sea :o
            continue
        if isinstance(bala, pclases.Articulo):
            bala = _build_dict_etiqueta_articulo_bala(bala)
        rectangulo(canvas, (izq, arriba), (der, abajo))
        canvas.setFont("Helvetica-Bold", 28)
        canvas.drawString(xLogo, yLogo, "GEOTEXAN S.A.")
        canvas.setFont("Helvetica", 14)
        canvas.drawString(xIzquierda,
                          yPrimeraLinea,
                          escribe("CÓDIGO: " + bala['codigo']))
        from barcode import code39
        codigobarras = code39.Extended39(bala['codigo'], xdim=.020*inch)
        codigobarras.drawOn(canvas, xIzquierda - 0.5 * cm, yPrimeraLinea + 15)
        canvas.drawString(xIzquierda,
                          yQuintaLinea,
                          escribe("COLOR: %s" % (bala['color'])))
        canvas.drawString(xIzquierda,
                          ySegundaLinea,
                          escribe("LOTE: %s" % (bala['lote'])))
        canvas.drawString(xDerecha,
                          ySegundaLinea,
                          escribe("PESO KG: %s" % (bala['peso'])))
        canvas.drawString(xIzquierda,
                          yTerceraLinea,
                          escribe("TIPO: %s" % (bala['tipo'])))
        canvas.drawString(xDerecha,
                          yTerceraLinea,
                          escribe("LONGITUD: %s" % (bala['longitud'])))
        canvas.drawString(xIzquierda,
                          yCuartaLinea,
                          escribe("BALA Nº: %s" % (bala['nbala'])))
        canvas.drawString(xDerecha,
                          yCuartaLinea,
                          escribe("DTEX: %s" % (bala['dtex'])))
        canvas.drawString(xDerecha,
                          yQuintaLinea,
                          escribe("ACABADO: %s" % (bala['acabado'])))
        from barcode.EANBarCode import EanBarCode
        bar = EanBarCode()
        nombreficheroean13 = bar.getImage(bala['codigoBarra'])
        ean13rotado = Image.open(nombreficheroean13)
        ean13rotado = ean13rotado.rotate(90)
        ean13rotado.save(nombreficheroean13)
        canvas.drawImage(nombreficheroean13, xCodigo, yCodigo)
        # XXX: DOMENECH:
        from barcode import code128
        seriep = None   # Esto ya no se usa. Serie del pedido para el cliente
        numped = None   # Esto ya no se usa. Núm. del pedido para el cliente
        codigodomenech = _build_codigo_domenech(bala, seriep, numped)
        if codigodomenech:
            barcodedomenech = code128.Code128(codigodomenech,
                                              # xdim = 0.015 * inch,
                                              # height = 0.5 * cm)
                                              xdim=0.0205 * inch,
                                              height=0.95 * cm)
            # barcodedomenech = code39.Extended39(codigodomenech,
            #                                  #xdim = 0.015 * inch,
            #                                  #height = 0.5 * cm)
            #                                  xdim = 0.0094 * inch,
            #                                  height = 0.95 * cm)
            ydom = alto - 1.2 * cm
            # ydom = 0.4 * cm
            xdom = (width - barcodedomenech.width) / 2.0
            barcodedomenech.drawOn(canvas, xdom, ydom)
            canvas.saveState()
            canvas.setFont("Courier-Bold", 8)
            canvas.drawCentredString(xdom + (barcodedomenech.width / 2.0),
                                     ydom - 0.20 * cm,
                                     codigodomenech)
            canvas.restoreState()
        # XXX: EODOMENECH
        # XXX: Marca para identificar las nuevas.
        canvas.saveState()
        canvas.setFillColorRGB(0, 0, 0)
        canvas.circle(izq - 0.3*cm, yQuintaLinea, 0.1*cm, fill=1)
        canvas.restoreState()
        # XXX: EOMarca
        # print "Imprimiendo segunda etiquetas..."
        canvas.showPage()
        # Y ahora la etiqueta adicional por si se pierde la otra y para cargar.
        create_etiqueta_backup_bala(canvas, bala)
        canvas.showPage()
    canvas.save()
    return nomarchivo


def test_rollos():
    """ Pruebas de impresión de rollos. """
    from formularios.reports import abrir_pdf
    todos = pclases.Rollo.select(orderBy="-id")
    from random import randrange
    rollos = (todos[randrange(todos.count())],
              todos[randrange(todos.count())])
    # abrir_pdf(etiqueta_rollos_norma13(rollos, False))
    abrir_pdf(etiqueta_rollos_norma13_en(rollos))


def test_pales():
    """ Pruebas de impresión de etiquetas de palé. """
    from formularios.reports import abrir_pdf
    pales = pclases.Pale.select(orderBy="-id")[:2]
    abrir_pdf(crear_etiquetas_pales(pales))
    import time
    time.sleep(1)
    abrir_pdf(crear_etiquetas_pales(pales, lang="en"))


def test_bigbags():
    """ Pruebas de impresión de etiquetas de bigbag. """
    from formularios.reports import abrir_pdf
    bigbags = pclases.Bigbag.select(orderBy="-id")[:2]
    abrir_pdf(crear_etiquetas_bigbags(bigbags))
    import time
    time.sleep(1)
    abrir_pdf(crear_etiquetas_bigbags(bigbags, lang="en"))


def test_balas():
    """ Pruebas de impresión de etiquetas de balas. """
    from formularios.reports import abrir_pdf
    balas = (pclases.Articulo.get_articulo("B215047"), )
    abrir_pdf(crear_etiquetas_balas(balas))
    import time
    time.sleep(1)
    abrir_pdf(crear_etiquetas_balas(balas, lang="en"))


if __name__ == "__main__":
    test_rollos()
    test_pales()
    test_bigbags()
    test_balas()
