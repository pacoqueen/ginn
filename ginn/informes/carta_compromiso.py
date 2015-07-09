#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2013  Francisco José Rodríguez Bogado                    #
#                          <frbogado@geotexan.com>                            #
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

# Carta de compromiso imprimible desde presupuestos. 


from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, \
                               TableStyle, XBox
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


PAGE_HEIGHT = defaultPageSize[1]; PAGE_WIDTH = defaultPageSize[0]
estilos = getSampleStyleSheet()

def dibujar_logo(canvas, doc, ruta_logo, lineas_datos_empresa, datos_fiscales, 
                 logo_marcado = None):
    """
    Dibuja el logotipo de la empresa en la página de «canvas».
    También dibuja el pie porque se hace con onLaterPages, que no es llamada 
    en la primera página. Así que aquí hay que hacer las dos cosas.
    """
    if ruta_logo:
        im = Image.open(ruta_logo)
        ancho, alto = im.size
        nuevo_alto = min(5 * cm, alto)
        ancho_proporcional = ancho * (nuevo_alto / alto)
        canvas.drawImage(ruta_logo, 
                         (PAGE_WIDTH - ancho_proporcional) / 2, 
                         PAGE_HEIGHT - 2 * cm - nuevo_alto, 
                         ancho_proporcional, 
                         nuevo_alto)
    if logo_marcado:
        im = Image.open(logo_marcado)
        ancho, alto = im.size
        nuevo_alto = min(2.5 * cm, alto)
        ancho_proporcional = ancho * (nuevo_alto / alto)
        canvas.drawImage(logo_marcado, 
                         PAGE_WIDTH - 6 * cm, 
                         PAGE_HEIGHT - 2 * cm - nuevo_alto, 
                         ancho_proporcional, 
                         nuevo_alto)
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        # OJO: HARCODED (como en todos los PDF que llevan marcado CE)
        texto_marcado = 'CE 1035-CPD-ES033858'  # Ojito: el de rollos, que es 
            # el que tenía puesto José Manuel Hurtado. Todas las críticas al 
            # formato, a él. He copiado tal cual su carta de compromiso. 
        canvas.drawCentredString(PAGE_WIDTH - 6*cm + (ancho_proporcional / 2), 
                                 PAGE_HEIGHT - 2*cm - nuevo_alto - 8, 
                                 escribe(texto_marcado))
        canvas.restoreState()
    dibujar_pie(canvas, doc, lineas_datos_empresa, datos_fiscales)

def dibujar_pie(canvas, doc, lineas_empresa, datos_fiscales):
    nlinea = 0
    canvas.saveState()
    for linea in lineas_empresa[::-1]:
        if nlinea == len(lineas_empresa) - 1:
            canvas.setFont("Helvetica-Bold", 12)
        else:
            canvas.setFont("Helvetica", 11)
        canvas.drawCentredString(PAGE_WIDTH / 2, 
                                 2 * cm + (nlinea * 15), 
                                 linea)
        nlinea += 1
    # Y ahora los datos fiscales en el lateral
    canvas.rotate(90)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(PAGE_HEIGHT / 2, 
                             -1.5*cm, 
                             datos_fiscales)
    canvas.rotate(-90)
    canvas.restoreState()

def build_encabezado(datos_empresa = [], idioma = "es"):
    """
    Devuelve una lista de "Flowables" de reportlab con los datos de la empresa. 
    Los datos de la empresa se reciben como una lista de textos.
    """
    estilo = ParagraphStyle("empepinao", parent = estilos["Heading1"])
    estilo.fontSize += 2
    estilo.alignment = enums.TA_CENTER
    if idioma == "en":
        strcarta = "<u>LETTER OF COMMITMENT</u>"
    else:
        strcarta = "<u>CARTA COMPROMISO</u>"
    cabecera = Paragraph(strcarta, estilo)
    return cabecera

def build_despedida(datos_comercial = [], idioma = "es"):
    estilo = ParagraphStyle("despedida", parent = estilos["Normal"])
    estilo.fontSize += 4
    if idioma == "en":
        strdespedida = "<b>Best regards:</b>"
    else:
        strdespedida = "<b>Atentamente:</b>"
    par = [Paragraph(strdespedida, estilo)]
    estilo.fontSize -= 2
    estilo.spaceAfter = 4
    par.append(Spacer(1, 0.3 * cm))
    for linea in datos_comercial:
        if datos_comercial.index(linea) == 1:
            linea = "<b>%s</b>" % linea
        par.append(Paragraph(linea, estilo))
    return par

def build_datos_cliente(datos_cliente = [], idioma = "es"):
    """
    Devuelve una lista de Flowables con las líneas recibidas como texto.
    """
    if idioma == "en":
        strclienteup = "CUSTOMER:"
        strcliente = "Customer"
    else:
        strclienteup = "CLIENTE:"
        strcliente = "Cliente"
    datos_c = [Spacer(1, 1*cm), Paragraph(strclienteup, estilos["Heading2"])]
    estilo_datos_c = ParagraphStyle(strcliente, 
                                    parent = estilos["Heading2"])
    estilo_datos_c.alignment = enums.TA_LEFT
    estilo_datos_c.spaceAfter = estilo_datos_c.spaceBefore = 2
    #estilo_datos_c.leftIndent = 0.5*cm
    filas_cliente = []
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
        filas_cliente.append([p])
    tabla = Table(filas_cliente)
    tabla.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1.0, colors.black)
        ]))
    datos_c.append(tabla)
    datos_c.append(Spacer(1, 1*cm))
    return datos_c

def build_fecha(fecha, idioma):
    res = None
    if fecha:
        estilo_texto = ParagraphStyle("Texto", 
                                      parent = estilos["Normal"])
        estilo_texto.alignment = enums.TA_RIGHT
        estilo_texto.fontSize += 2
        if not isinstance(fecha, str):
            fecha = utils.str_fecha(fecha)
        if idioma == "en":
            strdate = "Date: %s"
        else:
            strdate = "Fecha: %s"
        res = Paragraph(escribe(strdate % fecha), 
                        estilo_texto)
    return res

def build_datos_obra(obra, idioma = "es"):
    """
    Un cuadro con la referencia recibida de la obra dentro.
    """
    res = None
    if obra:
        if idioma == "en":
            strobra = "WORK REF."
            strobralo = "Building site"
        else:
            strobra = "REF. OBRA:"
            strobralo = "Obra"
        estilo_texto = ParagraphStyle(strobralo, 
                                      parent = estilos["Heading2"])
        tabla = Table([[Paragraph(escribe(obra), estilo_texto)]])
        tabla.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 1.0, colors.black)
            ]))
        res = [Paragraph(escribe(strobra), estilos["Heading2"]), 
                #XBox(PAGE_WIDTH, 2*cm, text = escribe(obra))]
               tabla]
    return res

def build_texto(idioma = "es"):
    estilo = ParagraphStyle("Texto", 
                            parent = estilos["Normal"])
    estilo.fontSize += 2
    estilo.alignment = enums.TA_JUSTIFY
    if idioma == "en":
        txt = "Serve hereby to formalize our commitment to working with your"\
                " company, in case of winning the works mentioned above, "\
                "according to the project specifications and conditions "\
                "in our offer."
    else:
        txt = "Sirva por la presente formalizar nuestro compromiso de "\
            "colaboración con su empresa, caso de ser la adjudicataria de las"\
            " obras y los trabajos anteriormente mencionados, de acuerdo con"\
            " las especificaciones de proyecto y condiciones de nuestra "\
            "oferta."
    par = Paragraph(txt, estilo)
    return par

def go(titulo, 
       ruta_archivo, 
       lineas_datos_empresa, 
       datos_cliente, 
       ref_obra, 
       datos_comercial, 
       fecha = None, 
       ruta_logo = None, 
       datos_fiscales = "", 
       logo_marcado = None,
       idioma = "es"
      ):
    """
    Recibe el título del documento y la ruta completa del archivo.
    """
    doc = SimpleDocTemplate(ruta_archivo, title = titulo)
    # Secciones
    encabezado = build_encabezado(idioma = idioma) # Logos y "título"
    datos_cliente = build_datos_cliente(datos_cliente, idioma)  # Datos cliente
    par_fecha = build_fecha(fecha, idioma)  # Fecha a la derecha
    datos_obra = build_datos_obra(ref_obra, idioma) # Cuadro con datos de obra
    texto = build_texto(idioma)   # El texto es fijo.
    despedida = build_despedida(datos_comercial, idioma)
    story = [Spacer(1, 4 * cm), 
             encabezado, 
             datos_cliente, 
             par_fecha, 
             Spacer(1, 0.2 * cm), 
             datos_obra, 
             Spacer(1, 0.4 * cm), 
             texto, 
             Spacer(1, 1 * cm), 
             despedida
            ]
    story = utils.aplanar([i for i in story if i])
    _dibujar_logo = lambda c, d: dibujar_logo(c, d, ruta_logo, 
                                              lineas_datos_empresa, 
                                              datos_fiscales, 
                                              logo_marcado)
    _dibujar_pie = lambda c, d: dibujar_pie(c, d, lineas_datos_empresa, 
                                            datos_fiscales)
    doc.build(story, onFirstPage = _dibujar_logo) #, onLaterPages = _dibujar_pie)
    return ruta_archivo

def go_from_presupuesto(presupuesto, idioma = "es"):
    """
    Construye el PDF a partir de un objeto presupuesto y no de sus datos 
    sueltos.
    Si idioma es "en", lo genera en inglés. En otro caso, castellano por
    defecto.
    """
    try:
        dde = pclases.DatosDeLaEmpresa.select()[0]
        lineas_empresa = [dde.nombre, 
                          dde.direccion + "%s %s (%s), %s" % (dde.cp, 
                                                              dde.ciudad, 
                                                              dde.provincia, 
                                                              dde.pais), 
                          "T.: %s F.: %s" % (dde.telefono, dde.fax), 
                          "W.: %s E.: %s" % (dde.web, dde.email)]
        #if dde.fax:
        #    lineas_empresa.append("Fax: %s" % (dde.fax))
        #if presupuesto.comercial and presupuesto.comercial.correoe:
        #    lineas_empresa.append(presupuesto.comercial.correoe)
        #else:
        #    lineas_empresa.append(dde.email)
        strdatosfiscales = "Datos fiscales:"
        if idioma == "en":
            strdatosfiscales = "Corp. data:"
        datos_fiscales = " ".join((strdatosfiscales, 
                                   dde.nombre.upper(), 
                                   dde.get_dir_facturacion_completa()))
    except IndexError:
        lineas_empresa = []
        datos_fiscales = ""
    #lineas_contenido = presupuesto.lineasDePedido + presupuesto.servicios
    lineas_contenido = presupuesto.lineasDePresupuesto 
    datos_cliente = []
    #if presupuesto.personaContacto != "":
    #    datos_cliente.append("A la atención de %s" % (presupuesto.personaContacto))
    datos_cliente.append(presupuesto.nombrecliente)
    datos_cliente.append(presupuesto.direccion)
    listadireccion = [presupuesto.cp, presupuesto.ciudad]
    if presupuesto.ciudad.strip() != presupuesto.provincia.strip():
        listadireccion.append(presupuesto.provincia)
    listadireccion.append(presupuesto.pais)
    segunda_linea_direccion = " ".join([token.strip() 
                                        for token in listadireccion 
                                        if token.strip() != ""])
    datos_cliente.append(segunda_linea_direccion)
    if presupuesto.telefono.strip() != "":
        datos_cliente.append("Tel.: %s" % (presupuesto.telefono))
    if presupuesto.fax.strip() != "":
        datos_cliente.append("Fax.: %s" % (presupuesto.fax))
    fecha_entradilla = utils.str_fecha(presupuesto.fecha)
    try:
        dde = pclases.DatosDeLaEmpresa.select()[0]
        iva = dde.iva
    except IndexError:
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
                    utils.float2str(presupuesto.calcular_base_imponible()), 
               striva: 
                    utils.float2str(presupuesto.calcular_total_iva()), 
               strtot: 
                    utils.float2str(presupuesto.calcular_importe_total())
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
        if dde.bvqi:
            logo_marcado = dde.get_ruta_completa_logo(dde.logoiso1)
        else:
            logo_marcado = None
    except IndexError:
        logo = None
        logo_marcado = None
    if presupuesto.validez:
        validez = presupuesto.validez
    else:
        validez = None
    if presupuesto.texto:
        condiciones = presupuesto.texto + "\n"
    else:
        condiciones = None
    # Condiciones "blandas" del presupuesto
    if (not presupuesto.cliente 
        or presupuesto.cliente.calcular_credito_disponible(
            base = presupuesto.calcular_importe_total(iva = True)) <= 0):
        if idioma == "en":
            texto_riesgo = "Operation conditioned by a previous credit "\
                           "approbation by %s." % dde.nombre
        else:
            texto_riesgo = "Esta operación está sujeta a la concesión de "\
                           "crédito por parte de %s." % dde.nombre
    else:
        texto_riesgo = None
    nomarchivo = os.path.join(gettempdir(), 
            "%s.pdf" % plantilla_nombre_carta_compromiso(presupuesto))
    if presupuesto.texto:
        if idioma == "en":
            condicionado = "Particular conditions:\n" + presupuesto.texto
        else:
            condicionado = "Condiciones particulares:\n" + presupuesto.texto
    else:
        condicionado = None
    ref_obra = presupuesto.nombreobra
    try:
        datos_comercial = presupuesto.comercial.get_firma().split("\n")
    except AttributeError:
        datos_comercial = ""
    if idioma == "en":
        strcarta = "Letter of commitment"
    else:
        strcarta = "Carta compromiso"
    nomarchivo = go(
       strcarta, 
       nomarchivo, 
       lineas_empresa, 
       datos_cliente, 
       ref_obra, 
       datos_comercial, 
       fecha_entradilla, 
       ruta_logo = logo, 
       datos_fiscales = datos_fiscales, 
       logo_marcado = logo_marcado,
       idioma = idioma)
    return nomarchivo

def plantilla_nombre_carta_compromiso(presupuesto):
    """
    Devuelve el nombre del fichero (sin extensión) para la carta de compromiso.
    """
    nombre = "CC oferta estudio (%d)" % presupuesto.id
    return nombre


if __name__ == "__main__":
    try:
        go_from_presupuesto(pclases.Presupuesto.select()[-1])
    except:
        lineas_empresa = ("American woman, co.", 
                          "Johnny Cash", 
                          "Alabama - 3213", 
                          "United States of America")
        datos_cliente = ("Lori Meyers", 
                         "los lunes se levanta a partir de las 2.", 
                         "con el sol", 
                         "qué calor")
        ref_obra = '“Modernización de las instalaciones de riego de la '\
                   'Comunidad de Regantes “Vega Campo-Baza”, en el T.M. '\
                   'de Baza (Granada)”'
        datos_comercial = ("Perlita de Huelva", 
                           "Arte puro", 
                           "Huelva", 
                           "+00 123 456 789")
        import time
        fecha_entradilla = utils.str_fecha(time.localtime())
        go("Presupuesto", 
           "/tmp/presupuesto.pdf", 
           lineas_empresa, 
           datos_cliente, 
           ref_obra, 
           datos_comercial, 
           fecha_entradilla, 
           ruta_logo = os.path.join(
               os.path.dirname(__file__), "..", "imagenes", "dorsia.png"), 
           datos_fiscales = "DATOS FISCALES " * 5)

