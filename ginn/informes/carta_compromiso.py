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


from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import Image
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

def dibujar_logo(canvas, doc, ruta_logo):
    """
    Dibuja el logotipo de la empresa en la página de «canvas».
    """
    if ruta_logo:
        im = Image.open(ruta_logo)
        ancho, alto = im.size
        nuevo_alto = min(3 * cm, alto)
        ancho_proporcional = ancho * (nuevo_alto / alto)
        canvas.drawImage(ruta_logo, 
                         (PAGE_WIDTH / 2) - ancho_proporcional, 
                         PAGE_HEIGHT - 2 * cm - nuevo_alto, 
                         ancho_proporcional, 
                         nuevo_alto)

def dibujar_pie(canvas, doc, lineas_empresa):
    nlinea = 0
    for linea in lineas_empresa:
        canvas.drawCenteredString(PAGE_WIDTH / 2, 
                                  PAGE_HEIGHT - 4 * cm - (nlinea * 15), 
                                  linea)
        nlinea += 1

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
    try:
        datos_empresa[0] = datos_empresa[0].upper()
    except TypeError:
        datos_empresa = list(datos_empresa)
        datos_empresa[0] = datos_empresa[0].upper()
    for linea in datos_empresa:
        if linea is datos_empresa[0]:
            estilo_encabezado.fontSize += 3
        p = Paragraph(escribe(linea), estilo_encabezado) 
        cabecera.append(p)
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

def build_entradilla(fecha, numpresupuesto):
    """
    Construye la frase de entradilla. Básicamente la palabra "Presupuesto" 
    y la fecha del mismo.
    """
    return Paragraph("<b><u>Presupuesto%s%s.</u> %s</b>" % (
                        numpresupuesto != None and " " or "", 
                        numpresupuesto != None and numpresupuesto or "", 
                        fecha), estilos["Normal"])

def build_fecha(fecha):
    res = None
    if fecha:
        estilo_texto = ParagraphStyle("Texto", 
                                      parent = estilos["Normal"])
        estilo_texto.alignment = enums.TA_RIGHT
        res = Paragraph(escribe("Fecha: %s" % (utils.str_fecha(fecha))), 
                        estilo_texto)
    return res

def build_datos_obra(obra):
    """
    Un cuadro con la referencia recibida de la obra dentro.
    """
    res = None
    if obra:
        estilo_texto = ParagraphStyle("Texto", 
                                      parent = estilos["Normal"])
        estilo_texto.alignment = enums.TA_RIGHT
        res = [Paragraph(escribe("REF. OBRA:"), estilo_texto), 
               Paragraph(escribe(obra), estilo_texto)]
    return res

def go(titulo, 
       ruta_archivo, 
       lineas_datos_empresa, 
       datos_cliente, 
       ref_obra, 
       datos_comercial, 
       fecha = None, 
       ruta_logo = None, 
      ):
    """
    Recibe el título del documento y la ruta completa del archivo.
    """
    doc = SimpleDocTemplate(ruta_archivo, title = titulo)
    # Secciones
    encabezado = build_encabezado(lineas_datos_empresa) # Logos y "título"
    datos_cliente = build_datos_cliente(datos_cliente)  # Datos del cliente
    par_fecha = build_fecha(fecha)  # Fecha a la derecha
    datos_obra = build_datos_obra(ref_obra) # Cuadro con datos de la obra
    story = [encabezado, 
             datos_cliente, 
             par_fecha, 
             Spacer(1, 0.2 * cm), 
             datos_obra]
    story = utils.aplanar([i for i in story if i])
    _dibujar_logo = lambda c, d: dibujar_logo(c, d, ruta_logo)
    _dibujar_pie = lambda c, d: dibujar_pie(c, d, lineas_datos_empresa)
    doc.build(story, onFirstPage = _dibujar_logo, onLaterPages = _dibujar_pie)
# PORASQUI
    return ruta_archivo

def go_from_presupuesto(presupuesto):
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
                          "Telf.: %s" % (dde.telefono)]
        if dde.fax:
            lineas_empresa.append("Fax: %s" % (dde.fax))
        if presupuesto.comercial and presupuesto.comercial.correoe:
            lineas_empresa.append(presupuesto.comercial.correoe)
        else:
            lineas_empresa.append(dde.email)
    except IndexError:
        lineas_empresa = []
    #lineas_contenido = presupuesto.lineasDePedido + presupuesto.servicios
    lineas_contenido = presupuesto.lineasDePresupuesto 
    datos_cliente = []
    if presupuesto.personaContacto != "":
        datos_cliente.append("A la atención de %s" % (presupuesto.personaContacto))
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
        datos_cliente.append("Tlf.: %s" % (presupuesto.telefono))
    if presupuesto.fax.strip() != "":
        datos_cliente.append("Fax.: %s" % (presupuesto.fax))
    fecha_entradilla = utils.str_fecha(presupuesto.fecha)
    try:
        dde = pclases.DatosDeLaEmpresa.select()[0]
        iva = dde.iva
    except IndexError:
        iva = 0.21
    totales = {"orden": ["Base imponible", 
                         "IVA %d%%" % (iva * 100), 
                         "TOTAL"], 
               "Base imponible":
                    utils.float2str(presupuesto.calcular_base_imponible()), 
               "IVA %d%%" % (iva * 100): 
                    utils.float2str(presupuesto.calcular_total_iva()), 
               "TOTAL": 
                    utils.float2str(presupuesto.calcular_importe_total())
               }
    if presupuesto.descuento:
        fila_descuento = "Descuento %s %%" % (
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
    if (not presupuesto.cliente 
        or presupuesto.cliente.calcular_credito_disponible(
            base = presupuesto.calcular_importe_total(iva = True)) <= 0):
        texto_riesgo = "Esta operación está sujeta a la concesión de "\
                       "crédito por parte de %s." % dde.nombre
    else:
        texto_riesgo = None
    nomarchivo = os.path.join(gettempdir(), 
                              "presupuesto_%s.pdf" % give_me_the_name_baby())
    if presupuesto.texto:
        condicionado = "Condiciones particulares:\n" + presupuesto.texto
    else:
        condicionado = None
    nomarchivo = go(
      "Carta compromiso", 
       nomarchivo, 
       lineas_empresa, 
       datos_cliente, 
       ref_obra, 
       datos_comercial, 
       fecha_entradilla, 
       ruta_logo = logo)  
    return nomarchivo


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
               os.path.dirname(__file__), "..", "imagenes", "dorsia.png"))

