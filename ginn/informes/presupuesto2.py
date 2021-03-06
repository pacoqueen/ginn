#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2013  Francisco José Rodríguez Bogado                    #
#                          (pacoqueen@users.sourceforge.net)                  #
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

# FORK de presupuesto.py para adaptarlo a otro formato. 


from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
try:
    import Image
except ImportError:
    from PIL import Image
from reportlab.rl_config import defaultPageSize
from reportlab.lib import colors, enums
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet 
import os
from framework import pclases
from formularios import utils
from informes.geninformes import give_me_the_name_baby, escribe
from tempfile import gettempdir
from formularios.utils import sanitize
from informes.geninformes import dibujar_logo_prns
from informes.geninformes import dibujar_domicilio_fiscal_prns
from informes.geninformes import dibujar_domicilio_fabrica_prns
from informes.geninformes import dibujar_cif_prns
from informes.geninformes import dibujar_bvqi_prns
from informes.geninformes import dibujar_linea_prns
from informes.geninformes import VERDE_GTX



PAGE_HEIGHT = defaultPageSize[1]; PAGE_WIDTH = defaultPageSize[0]
estilos = getSampleStyleSheet()

def dibujar_logo(canvas, doc, ruta_logo, idioma = "es"):
    """
    Dibuja el logotipo de la empresa en la página de «canvas».
    UPDATE: Dibuja el logo y el resto de información de la cabecera nueva made
    in Parnaso.
    """
    datos_de_la_empresa = pclases.DatosDeLaEmpresa.select()[0]
    c = canvas
    width, height = PAGE_WIDTH, PAGE_HEIGHT
    lm = 0.7*cm
    rm = width - 1.2*cm
    if datos_de_la_empresa.logo:
        dibujar_logo_prns(c, lm, height, datos_de_la_empresa)
    if datos_de_la_empresa.bvqi:
        if idioma == "en":
            i10n_oferta = "Offer"
        else:
            i10n_oferta = "Oferta"
        dibujar_bvqi_prns(c, rm, height - 3.5*cm, datos_de_la_empresa,
                i10n_oferta)
    dibujar_domicilio_fiscal_prns(c, lm, height - 3.0*cm, datos_de_la_empresa)
    dibujar_domicilio_fabrica_prns(c, lm, height - 4.0*cm, datos_de_la_empresa)
    dibujar_cif_prns(c, lm, height - 5.0*cm, datos_de_la_empresa)
    dibujar_linea_prns(c, height - 5.5*cm)
#    if ruta_logo:
#        im = Image.open(ruta_logo)
#        ancho, alto = im.size
#        nuevo_alto = min(3 * cm, alto)
#        ancho_proporcional = ancho * (nuevo_alto / alto)
#        canvas.drawImage(ruta_logo, 
#                         PAGE_WIDTH - 3 * cm - ancho_proporcional, 
#                         PAGE_HEIGHT - 2 * cm - nuevo_alto, 
#                         ancho_proporcional, 
#                         nuevo_alto)

def dibujar_dir_fiscal(canvas, doc, dir_fiscal):
    if False:
    #if dir_fiscal:
        canvas.saveState()
        canvas.rotate(90)
        canvas.setFont("Helvetica", 7)
        canvas.drawCentredString(PAGE_HEIGHT / 2, 
                                 -0.5*cm,
                                 dir_fiscal, 
                                 )
        canvas.rotate(-90)
        canvas.restoreState()

def build_tabla_contenido(data, lang = "es"):
    """
    Construye la tabla del contenido del presupuesto.
    """
    estilo_cabecera_tabla = ParagraphStyle("Cabecera tabla", 
                                           parent=estilos["Heading3"])
    estilo_cabecera_tabla.fontName = "Times-Bold"
    estilo_cabecera_tabla.alignment = enums.TA_CENTER
    estilo_numeros_tabla = ParagraphStyle("Números tabla", 
                                           parent=estilos["Normal"])
    if lang == "en":
        strcant = "Quantity"
        strdesc = "Description"
        strprice = "Price"
        strdue = "Subtotal"
    else:
        strcant = "Cantidad"
        strdesc = escribe("Descripción")
        strprice = "Precio"
        strdue = "Importe"
    estilo_numeros_tabla.alignment = enums.TA_RIGHT
    datos = [(Paragraph(strcant, estilo_cabecera_tabla), 
              Paragraph(strdesc, estilo_cabecera_tabla), 
              Paragraph(strprice, estilo_cabecera_tabla), 
              Paragraph(strdue, estilo_cabecera_tabla))
            ]
    for d in data:
        if isinstance(d, (list, tuple)):
            fila = d[:4]
        elif isinstance(d, pclases.LineaDePedido):
            # OBSOLETO. No debería entrar nunca aquí.
            fila = (utils.float2str(d.cantidad, autodec = True), 
                    d.producto.descripcion, 
                    d.calcular_precio_unitario_coherente(precision = 2), 
                    utils.float2str(d.get_subtotal()
                                    + (d.precio * d.descuento * d.cantidad)))
        elif isinstance(d, pclases.Servicio):
            # OBSOLETO. No debería entrar nunca aquí.
            fila = (utils.float2str(d.cantidad, autodec = True), 
                    d.concepto, 
                    utils.float2str(d.precio), 
                    utils.float2str(d.get_subtotal()
                                    + (d.precio * d.descuento * d.cantidad)))
        elif isinstance(d, pclases.LineaDePresupuesto):
            try:
                unidad = d.producto.unidad
            except AttributeError:
                unidad = ""
            fila = (utils.float2str(d.cantidad, autodec = True) + " " + unidad, 
                    d.descripcion, 
                    utils.float2str(d.precio, precision = 3, 
                                    autodec = 2) + " €" 
                        + (unidad and "/" + unidad or ""), 
                    utils.float2str(d.get_subtotal()) + " €")
        _fila = (fila[0], 
                 Paragraph(escribe(fila[1]), estilos["Normal"]),
                 Paragraph(escribe(fila[2]), estilo_numeros_tabla),
                 Paragraph(escribe(fila[3]), estilo_numeros_tabla),
                )
        datos.append(_fila)
        if hasattr(d, "descuento") and d.descuento:
            if lang == "en":
                strdisc = "Discount %s %%"
            else:
                strdisc = "Descuento %s %%"
            fila_descuento = ("", 
                              strdisc 
                                % utils.float2str(d.descuento * 100, 
                                                  autodec = True), 
                              utils.float2str(-d.precio * d.descuento), 
                              utils.float2str(-d.precio*d.descuento*d.cantidad))
            _fila = (fila_descuento[0], 
                     Paragraph(escribe(fila_descuento[1]),estilo_numeros_tabla),
                     Paragraph(escribe(fila_descuento[2]),estilo_numeros_tabla),
                     Paragraph(escribe(fila_descuento[3]),estilo_numeros_tabla),
                    )
            datos.append(_fila)
    tabla = Table(datos, 
                  colWidths = (PAGE_WIDTH * 0.13, 
                               PAGE_WIDTH * 0.42, 
                               PAGE_WIDTH * 0.15, 
                               PAGE_WIDTH * 0.2), 
                  repeatRows = 1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey), 
        ("LINEBEFORE", (0, 0), (-1, -1), 0.25, colors.black),
        ("LINEBELOW", (0, 0), (-1, 0), 1.0, colors.black), 
        ("LINEBELOW", (0, "splitlast"), (-1, "splitlast"), 1.0, colors.black), 
        ("BOX", (0, 0), (-1, -1), 1.0, colors.black),
        ("VALIGN", (0, 0), (-1, 0), "CENTER"), 
        ("VALIGN", (0, 0), (0, -1), "TOP"), 
        ("ALIGN", (0, 0), (-1, 0), "CENTER"), 
        ("ALIGN", (-3, 1), (-1, -1), "RIGHT"), 
        #("ALIGN", (0, 1), (0, -1), "DECIMAL"), <- No puedo cambiar 
        #                               el pivotChar de "." a ",". No me vale.
        ("ALIGN", (0, 1), (0, -1), "CENTER"), 
        ("RIGHTPADDING", (0, 1), (0, -1), 0.75 * cm), 
        ]))
    return tabla

def build_encabezado(datos_empresa = []):
    """
    Devuelve una lista de "Flowables" de reportlab con los datos de la empresa. 
    Los datos de la empresa se reciben como una lista de textos.
    """
    cabecera = []
    estilo_encabezado = ParagraphStyle("Encabezado", 
                                       parent = estilos["Heading2"])
    estilo_encabezado.rightIndent = PAGE_WIDTH * 0.25
    estilo_encabezado.alignment = enums.TA_JUSTIFY
    estilo_encabezado.spaceAfter = 0
    estilo_encabezado.spaceBefore = 4
    datos_empresa[0] = datos_empresa[0].upper()
    for linea in datos_empresa:
        if linea is datos_empresa[0]:
            estilo_encabezado.fontSize += 3
        p = Paragraph(escribe(linea), estilo_encabezado) 
        #cabecera.append(p)
        cabecera.append(Spacer(1, 10))
        estilo_encabezado.fontSize -= 1
        if estilo_encabezado.spaceAfter > -4:
            estilo_encabezado.spaceAfter -= 1
        estilo_encabezado.spaceBefore = estilo_encabezado.spaceAfter
        if linea is datos_empresa[0]:
            estilo_encabezado.fontSize -= 3
    return cabecera

def build_datos_cliente(datos_cliente = []):
    """
    Devuelve una lista de Flowables con las líneas recibidas como texto.
    """
    datos_c = [Spacer(1, 1*cm)]
    estilo_datos_c = ParagraphStyle("Cliente", 
                                    parent = estilos["Heading3"])
    estilo_datos_c.alignment = enums.TA_LEFT
    estilo_datos_c.spaceAfter = estilo_datos_c.spaceBefore = 2
    #estilo_datos_c.leftIndent = 0.5*cm
    if datos_cliente:
        try:
            datos_cliente[0] = "<strong>%s</strong>" % datos_cliente[0]
        except TypeError:
            datos_cliente = ["<strong>%s</strong>" % datos_cliente[0]] \
                            + list(datos_cliente[1:])
    tamanno_predeterminado = estilo_datos_c.fontSize
    for linea in datos_cliente:
        # ¡Esto debería hacerlo ReportLab, pero no sé por qué el markup 
        # sólo funciona con el estilo normal!
        if "<strong>" in linea:
            estilo_datos_c.fontSize += 4
        else:
            estilo_datos_c.fontSize = tamanno_predeterminado
        p = Paragraph(escribe(linea), estilo_datos_c) 
        datos_c.append(p)
    datos_c.append(Spacer(1, 1*cm))
    return datos_c

def build_entradilla(fecha, numpresupuesto, para_estudio, lang = "es"):
    """
    Construye la frase de entradilla. Básicamente la palabra "Presupuesto" 
    y la fecha del mismo.
    """
    if lang == "en":
        strpresupuesto = "Offer"
    else:
        strpresupuesto = "Presupuesto"
    if para_estudio:
        if lang == "en":
            texto_estudio = " for work planning"
        else:
            texto_estudio = " para estudio de obra" 
    else:
        texto_estudio = "" 
    return Paragraph("<b><u>%s%s%s%s.</u> %s</b>" % (
                        strpresupuesto, 
                        texto_estudio, 
                        numpresupuesto != None and " n.º " or "", 
                        numpresupuesto != None and numpresupuesto or "", 
                        #fecha), estilos["Normal"])
                        fecha), 
                     estilos["Heading2"])

def build_texto(texto):
    """
    El texto que encabeza la tabla.
    """
    res = None
    if texto:
        estilo_texto = ParagraphStyle("Texto", 
                                      parent = estilos["Normal"])
        estilo_texto.alignment = enums.TA_JUSTIFY
        estilo_texto.firstLineIndent = 24
        _res = [Paragraph(escribe(i), estilo_texto) for i in texto.split("\n")]
        espacio = Spacer(1, 0.25*cm)
        res = [_res[0]]
        for i in _res[1:]:
            res.extend([espacio, i])
    return res

def build_tabla_totales(dic_totales):
    """
    Construye una tabla con los totales del presupuesto.
    La tabla tiene dos columnas. En la primera están las claves del 
    diccionario «dic_totales». En la segunda los valores correspondientes.
    La última fila de la tabla estará en negrita.
    Si el diccionario de totales trae una clave "orden" (que debería) se 
    seguirá ese orden para mostrarlos en las filas.
    """
    try:
        claves = dic_totales["orden"]
    except KeyError:
        claves = dic_totales.keys()
    datos = []
    for clave in claves:
        datos += [["", clave, dic_totales[clave]]]
    a_derecha = ParagraphStyle("A derecha", 
                                parent = estilos["BodyText"])
    a_derecha.alignment = enums.TA_RIGHT
    # Pongo total en negrita
    datos[2][-1] = Paragraph("<b>%s</b>" % datos[2][-1], 
                              a_derecha)
    datos[2][1] = Paragraph("<b>%s</b>" % datos[2][1], 
                             estilos["BodyText"])
    tabla = Table(datos, 
                  colWidths = (PAGE_WIDTH * 0.55,   # HACK: Para que ocupe lo  
                               PAGE_WIDTH * 0.15,   # mismo que la otra. 
                               PAGE_WIDTH * 0.2))   # Si no, RL la centra.
    tabla.setStyle(TableStyle([
        ("BOX", (1, 0), (-1, -1), 1.0, colors.black),
        ("INNERGRID", (1, 0), (-1, -1), 0.25, colors.black), 
        ("ALIGN", (1, 0), (-2, -1), "LEFT"), 
        ("ALIGN", (-1, 0), (-1, -1), "RIGHT"), 
        ]))
    return tabla

def build_validez(validez):
    txt_validez = "OFERTA VÁLIDA POR %s DESDE LA FECHA DE ESTE PRESUPUESTO"
    if validez == 1:
        mes = "UN MES"
    else:
        from formularios.numerals import numerals
        txt_meses = numerals(validez, 
                             moneda = "", 
                             fraccion = "", 
                             autoomitir = True).upper()
        mes = "%s MESES" % txt_meses
    txt_validez = txt_validez % (mes)
    a_derecha = ParagraphStyle("A derecha", 
                                parent = estilos["Normal"])
    a_derecha.alignment = enums.TA_RIGHT
    a_derecha.fontName = "Courier"
    a_derecha.fontSize = 8
    return Paragraph(txt_validez, a_derecha)

def build_condicionado(condicionado):
    a_derecha = ParagraphStyle("A derecha", 
                                parent = estilos["Normal"])
    a_derecha.alignment = enums.TA_LEFT
    a_derecha.fontName = "Courier"
    a_derecha.fontSize = 13
    texto_condicionado = "Condiciones particulares: " + condicionado
    return Paragraph(texto_condicionado, a_derecha)

def build_texto_riesgo(texto_riesgo):
    # a_derecha = ParagraphStyle("A derecha", 
    #                             parent = estilos["Normal"])
    # a_derecha.alignment = enums.TA_RIGHT
    # a_derecha.fontName = "Courier"
    # a_derecha.fontSize = 8
    estilo_texto = ParagraphStyle("Texto", 
                                  parent = estilos["Normal"])
    estilo_texto.alignment = enums.TA_JUSTIFY
    estilo_texto.firstLineIndent = 24
    return Paragraph(texto_riesgo, estilo_texto) # , a_derecha)     # CWT

def go(titulo, 
       ruta_archivo, 
       lineas_datos_empresa, 
       datos_cliente, 
       lineas_contenido, 
       fecha_entradilla, 
       totales = {}, 
       texto = None, 
       despedida = None, 
       ruta_logo = None, 
       validez = None, 
       condicionado = None, 
       texto_riesgo = None, 
       numpresupuesto = "", 
       incluir_condicionado_general = True, 
       forma_de_pago = None, 
       dir_fiscal = None, 
       firma_comercial = None, 
       para_estudio = False,
       idioma = "es"):
    """
    Recibe el título del documento y la ruta completa del archivo.
    Si validez != None escribe una frase con la validez del presupuesto.
    """
    if idioma not in ("en", "es"):
        raise NotImplementedError,\
                __file__ + ": Idioma '%s' no implementado." % idioma
    doc = SimpleDocTemplate(ruta_archivo, title = titulo)
    encabezado = build_encabezado(lineas_datos_empresa)
    try:
        nombrecliente = datos_cliente[0].replace(" ", "_")
    except:
        nombrecliente = ""
    datos_cliente = build_datos_cliente(datos_cliente)
    entradilla = build_entradilla(fecha_entradilla, numpresupuesto, 
                                  para_estudio, 
                                  lang = idioma)
    texto = build_texto(texto)
    contenido = build_tabla_contenido(lineas_contenido, lang = idioma)
    totales = build_tabla_totales(totales)
    despedida = build_texto(despedida)
    forma_pago = build_texto(forma_de_pago)
    comercial = build_texto(firma_comercial)
    story = [encabezado, 
             datos_cliente, 
             entradilla, 
             Spacer(1, 0.2 * cm), 
             contenido, 
             Spacer(1, 0.25 * cm), 
             totales, 
             Spacer(1, 1 * cm),
             forma_pago, 
             Spacer(1, 2 * cm), 
             texto, 
             Spacer(1, 0.2 * cm), 
             despedida, 
             Spacer(1, 0.5 * cm), 
             comercial]
    #if validez:
        #story.insert(9, build_validez(validez))
    if texto_riesgo:
        story.insert(-8, build_texto_riesgo(texto_riesgo))
    #if condicionado: # El condicionado es el texto en sí.
    #    story.insert(-2, Spacer(1, 2 * cm))
    #    story.insert(-2, build_condicionado(condicionado))
    story = utils.aplanar([i for i in story if i])
    _dibujar_logo = lambda c, d: dibujar_logo(c, d, ruta_logo, idioma)
    _dibujar_dir_fiscal = lambda c, d: dibujar_dir_fiscal(c, d, dir_fiscal)
    def dibujar_logo_y_dir_fiscal(c, d):
        _dibujar_logo(c, d)
        _dibujar_dir_fiscal(c, d)
    doc.build(story, onFirstPage = dibujar_logo_y_dir_fiscal, 
                     onLaterPages = _dibujar_dir_fiscal)
    # Agrego condiciones generales:
    if incluir_condicionado_general:
        from lib.PyPDF2 import PyPDF2
        pdf_presupuesto = open(ruta_archivo, "rb")
        if idioma == "en":
            fcond = "condiciones_generales_en.pdf"
        else:
            fcond = "condiciones_generales.pdf"
        pdf_condiciones = open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                         fcond), 
            "rb")
        merger = PyPDF2.PdfFileMerger()
        merger.append(pdf_presupuesto)
        merger.append(pdf_condiciones)
        combinado = os.path.join(gettempdir(),
                    "oferta_%d_%s_%s.pdf" % (numpresupuesto, 
                        sanitize(nombrecliente, strict = True), 
                        give_me_the_name_baby()))
        merger.write(open(combinado, "wb"))
        ruta_archivo = combinado
    return ruta_archivo

def go_from_presupuesto(presupuesto, 
                        incluir_condicionado_general = True,
                        idioma = "es"):
    """
    Construye el PDF a partir de un objeto presupuesto y no de sus datos 
    sueltos.
    """
    try:
        dde = pclases.DatosDeLaEmpresa.select()[0]
        lineas_empresa = [dde.nombre, 
                          dde.direccion, 
                          "%s %s (%s), %s" % (dde.cp, 
                                              dde.ciudad, 
                                              dde.provincia, 
                                              dde.pais), 
                          "Tel.: %s" % (dde.telefono)]
        if dde.fax:
            lineas_empresa.append("Fax: %s" % (dde.fax))
        if dde.email:
            lineas_empresa.append(dde.email)
        elif presupuesto.comercial and presupuesto.comercial.correoe:
            lineas_empresa.append(presupuesto.comercial.correoe)
        if dde.web:
            lineas_empresa.append('<a href=http://%s>%s</a>' % (
                dde.web, dde.web))
        # Son pocos textos. No merece la pena tirar de gettext hasta que
        # no me pidan un tercer idioma.
        if idioma == "en":
            strfiscal = "Corp. data: %s %s %s %s"
        else:
            strfiscal = "Datos fiscales: %s %s %s %s"
        dir_fiscal = strfiscal % (
                dde.nombre, 
                dde.get_dir_facturacion_completa(), 
                dde.str_cif_o_nif(), 
                dde.cif)
    except IndexError:
        lineas_empresa = []
        dir_fiscal = ""
    #lineas_contenido = presupuesto.lineasDePedido + presupuesto.servicios
    lineas_contenido = presupuesto.lineasDePresupuesto 
    lineas_contenido.sort(key = lambda ldp: ldp.id)
    datos_cliente = []
    nombre_cliente = presupuesto.nombrecliente
    datos_cliente.append(nombre_cliente)
    cif = presupuesto.cliente and presupuesto.cliente.cif or presupuesto.cif
    datos_cliente.append(" <small>(%s)</small>" % cif)
    if presupuesto.personaContacto != "":
        if idioma == "en":
            stratt = "Att: %s"
        else:
            stratt = "A la atención de %s"
        datos_cliente.append(stratt % (
            presupuesto.personaContacto))
    datos_cliente.append(presupuesto.direccion)
    listadireccion = [presupuesto.cp, presupuesto.ciudad]
    if presupuesto.ciudad.strip() != presupuesto.provincia.strip():
        if presupuesto.ciudad.strip():
            listadireccion.append("(" + presupuesto.provincia + ")")
        else: 
            listadireccion.append(presupuesto.provincia)
    listadireccion.append(presupuesto.pais)
    segunda_linea_direccion = " ".join([token.strip() 
                                        for token in listadireccion 
                                        if token.strip() != ""])
    datos_cliente.append(segunda_linea_direccion)
    if presupuesto.telefono.strip() != "":
        if idioma == "en":
            strphone = "Phone n.: %s"
        else:
            strphone = "Tlf.: %s"
        datos_cliente.append(strphone % (presupuesto.telefono))
    if presupuesto.fax.strip() != "":
        datos_cliente.append("Fax.: %s" % (presupuesto.fax))
    if presupuesto.obra or presupuesto.nombreobra.strip():
        try:
            ref_obra = presupuesto.obra.obra.get_str_obra()
        except AttributeError:
            ref_obra = presupuesto.nombreobra
        if idioma == "en":
            strobra = "Ref.: <b>%s</b>"
        else:
            strobra = "Ref. obra: <b>%s</b>"
        datos_cliente.append(strobra % ref_obra)
    fecha_entradilla = utils.str_fecha(presupuesto.fecha)
    try:
        iva = presupuesto.cliente.get_iva_norm()
    except AttributeError:
        if (presupuesto.pais and presupuesto.pais.upper() 
                not in ("ESPAÑA", "ESPAñA", "SPAIN")):
            iva = 0
        else:
            iva = 0.21
    if idioma == "en":
        strbimp = "Subtotal"
        striva = "VAT %d%%" % (iva * 100)
        strtot = "TOTAL"
    else:
        strbimp = "Base imponible"
        striva = "IVA %d%%" % (iva * 100)
        strtot = "TOTAL"
    totales = {"orden": [strbimp, 
                         striva, 
                         strtot], 
               strbimp:
                    utils.float2str(presupuesto.calcular_base_imponible())+" €",
               striva: 
                    utils.float2str(presupuesto.calcular_total_iva())+" €", 
               strtot: 
                    utils.float2str(presupuesto.calcular_importe_total())+" €", 
               }
    if presupuesto.descuento:
        if idioma == "en":
            strdto = "Descuento %s %%"
        else:
            strdto = "Discount %s %%"
        fila_descuento = strdto % (
            utils.float2str(presupuesto.descuento*100, autodec = True))
        totales['orden'].insert(0, fila_descuento) 
        totales[fila_descuento] = utils.float2str(
            presupuesto.calcular_subtotal(incluir_descuento = False) 
            * presupuesto.descuento * -1)
        fila_subtotal = "Subtotal"
        totales['orden'].insert(0, fila_subtotal) 
        totales[fila_subtotal] = utils.float2str(
            presupuesto.calcular_subtotal(incluir_descuento = False))
    total_irpf = presupuesto.calcular_total_irpf()
    if total_irpf != 0:
        try:
            dde = pclases.DatosDeLaEmpresa.select()[0]
            irpf = dde.irpf
        except IndexError:
            irpf = None
        texto_irpf = "IRPF"
        if irpf:
            texto_irpf += " (%d%%)" % (irpf*100)
        totales[texto_irpf] = utils.float2str(total_irpf)
        totales["orden"].insert(-2, texto_irpf)
    try:
        dde = pclases.DatosDeLaEmpresa.select()[0]
        logo = dde.get_ruta_completa_logo()
    except IndexError:
        logo = None
    if presupuesto.validez:
        validez = presupuesto.validez
    else:
        validez = None
    if presupuesto.texto:
        condiciones = presupuesto.texto + "\n"
    else:
        condiciones = None
    # Condiciones "blandas" del presupuesto
    # CWT: Se debe imprimir en todos los presupuestos, por si a la hora de 
    # formalizarlo como pedido se ha quedado sin crédito por alguna operación 
    # anterior al pedido y posterior a la oferta.
    #if (not presupuesto.cliente 
    #    or presupuesto.cliente.calcular_credito_disponible(
    #        base = presupuesto.calcular_importe_total(iva = True)) <= 0):
    if True:
        if idioma == "en":
            texto_riesgo = "Operation conditioned by a previous credit "\
                           "approbation by %s." % dde.nombre
        else:
            texto_riesgo = "Esta operación está sujeta a la concesión de "\
                           "crédito por parte de %s." % dde.nombre
    else:
        texto_riesgo = None
    nomarchivo = os.path.join(gettempdir(), 
                              "presupuesto_%s.pdf" % give_me_the_name_baby())
    if presupuesto.texto:
        if idioma == "en":
            condicionado = "Particular conditions:\n" + presupuesto.texto
        else:
            condicionado = "Condiciones particulares:\n" + presupuesto.texto
    else:
        condicionado = None
    try:
        if idioma == "en":
            strpresupuesto = "Offer "
            fdp = "Payment terms: %s" % presupuesto.formaDePago.toString(
                    presupuesto.cliente)
        else:
            strpresupuesto = "Presupuesto"
            fdp = "Forma de pago: %s" % presupuesto.formaDePago.toString(
                    presupuesto.cliente)
    except AttributeError:
        fdp = ""
    if presupuesto.comercial:
        firma_comercial = '<b>%s %s</b>\n<i>%s</i>\n%s\n<u>'\
                          '<a href="mailto:%s">%s</a></u>'\
                          '<b> </b>' % (
                presupuesto.comercial.empleado.nombre
                    and presupuesto.comercial.empleado.nombre or "", 
                presupuesto.comercial.empleado.apellidos 
                    and presupuesto.comercial.empleado.apellidos or "", 
                presupuesto.comercial.cargo
                    and presupuesto.comercial.cargo or "", 
                presupuesto.comercial.telefono 
                    and presupuesto.comercial.telefono or "", 
                presupuesto.comercial.correoe 
                    and presupuesto.comercial.correoe or "", 
                presupuesto.comercial.correoe 
                    and presupuesto.comercial.correoe or "")
    else:
        firma_comercial = ""
    nomarchivo = go(
      "%s %s (%s)" % (strpresupuesto, 
                      presupuesto.nombrecliente, 
                      utils.str_fecha(presupuesto.fecha)), 
       nomarchivo, 
       lineas_empresa, 
       datos_cliente, 
       lineas_contenido, 
       fecha_entradilla, 
       totales, 
       condicionado, 
       presupuesto.despedida, 
       ruta_logo = logo, 
       validez = validez, 
       texto_riesgo = texto_riesgo, 
       #numpresupuesto = presupuesto.numpresupuesto)
       numpresupuesto = presupuesto.id, 
       forma_de_pago = fdp, 
       dir_fiscal = dir_fiscal, 
       firma_comercial = firma_comercial, 
       para_estudio = presupuesto.estudio, 
       idioma = idioma)
    return nomarchivo


if __name__ == "__main__":
    try:
        go_from_presupuesto(pclases.Presupuesto.select()[-1])
    except:
        lineas_contenido = [(1.234, "Una cosa "*20, "1.245", `1.234*1.245`), 
                            (1, "Grñai mama", "1", "0.25"), 
                            ("0,25", "Otra cosa", "1", "0.25")] * 7
        lineas_empresa = ["American woman, co.", 
                          "Johnny Cash", 
                          "Alabama - 3213", 
                          "United States of America"]
        datos_cliente = ("Lori Meyers", 
                         "los lunes se levanta a partir de las 2.", 
                         "con el sol", 
                         "qué calor")
        totales = {"Base imponible": "100.50 €", 
                   "IVA 21%": 100.5 * 0.21, 
                   "TOTAL": 100.5 * 1.21, 
                   "orden": ("Base imponible", "IVA 21%", "TOTAL")}
        texto = """Estimado señor Floppy:
                    Es un placer decirle a la cara que usted apesta.
                    No te digo «na» y te lo digo «to».


                    Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur eu odio. Ut dapibus. In quis diam mattis est volutpat luctus. Quisque pharetra diam vel mauris. Etiam blandit gravida augue. Phasellus justo dolor, porta vehicula, sagittis sed, viverra vitae, velit. Ut lorem nibh, volutpat at, faucibus sit amet, dapibus sit amet, est. Nunc iaculis nunc at risus. Phasellus porta felis. Suspendisse lorem leo, faucibus ut, aliquam sed, faucibus id, lorem. Nulla aliquet, sapien eu pulvinar suscipit, turpis purus varius metus, eu dignissim est orci luctus neque. Nam scelerisque elit eu nisi. Aenean tincidunt. Sed adipiscing eros ut magna. Proin varius. In hac habitasse platea dictumst.
        """
        despedida = """
        Firmado:

            Al Bundy.
        """
        import time
        fecha_entradilla = utils.str_fecha(time.localtime())
        go("Presupuesto", 
           "/tmp/presupuesto.pdf", 
           lineas_empresa, 
           datos_cliente, 
           lineas_contenido, 
           fecha_entradilla, 
           totales, 
           texto, 
           despedida, 
           ruta_logo = "../imagenes/dorsia.png")

