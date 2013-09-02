#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado                    #
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
                         PAGE_WIDTH - 3 * cm - ancho_proporcional, 
                         PAGE_HEIGHT - 2 * cm - nuevo_alto, 
                         ancho_proporcional, 
                         nuevo_alto)

def dibujar_dir_fiscal(canvas, doc, dir_fiscal):
    if dir_fiscal:
        canvas.saveState()
        canvas.rotate(90)
        canvas.setFont("Helvetica", 7)
        canvas.drawCentredString(PAGE_HEIGHT / 2, 
                                 -0.5*cm,
                                 dir_fiscal, 
                                 )
        canvas.rotate(-90)
        canvas.restoreState()

def build_tabla_contenido(data):
    """
    Construye la tabla del contenido del presupuesto.
    """
    estilo_cabecera_tabla = ParagraphStyle("Cabecera tabla", 
                                           parent=estilos["Heading3"])
    estilo_cabecera_tabla.fontName = "Times-Bold"
    estilo_cabecera_tabla.alignment = enums.TA_CENTER
    estilo_numeros_tabla = ParagraphStyle("Números tabla", 
                                           parent=estilos["Normal"])
    estilo_numeros_tabla.alignment = enums.TA_RIGHT
    datos = [(Paragraph("Cantidad", estilo_cabecera_tabla), 
              Paragraph(escribe("Descripción"), estilo_cabecera_tabla), 
              Paragraph("Precio", estilo_cabecera_tabla), 
              Paragraph("Importe", estilo_cabecera_tabla))
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
                    # TODO: Añadir unidades del producto.
                    d.descripcion, 
                    utils.float2str(d.precio) + " €" 
                        + (unidad and "/" + unidad or ""), 
                    utils.float2str(d.get_subtotal()) + " €")
        _fila = (fila[0], 
                 Paragraph(escribe(fila[1]), estilos["Normal"]),
                 Paragraph(escribe(fila[2]), estilo_numeros_tabla),
                 Paragraph(escribe(fila[3]), estilo_numeros_tabla),
                )
        datos.append(_fila)
        if hasattr(d, "descuento") and d.descuento:
            fila_descuento = ("", 
                              "Descuento %s %%" 
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
                  colWidths = (PAGE_WIDTH * 0.1, 
                               PAGE_WIDTH * 0.45, 
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
    a_derecha = ParagraphStyle("A derecha", 
                                parent = estilos["Normal"])
    a_derecha.alignment = enums.TA_RIGHT
    a_derecha.fontName = "Courier"
    a_derecha.fontSize = 8
    return Paragraph(texto_riesgo, a_derecha)

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
       dir_fiscal = None):
    """
    Recibe el título del documento y la ruta completa del archivo.
    Si validez != None escribe una frase con la validez del presupuesto.
    """
    doc = SimpleDocTemplate(ruta_archivo, title = titulo)
    encabezado = build_encabezado(lineas_datos_empresa)
    try:
        nombrecliente = datos_cliente[0].replace(" ", "_")
    except:
        nombrecliente = ""
    datos_cliente = build_datos_cliente(datos_cliente)
    entradilla = build_entradilla(fecha_entradilla, numpresupuesto)
    texto = build_texto(texto)
    contenido = build_tabla_contenido(lineas_contenido)
    totales = build_tabla_totales(totales)
    despedida = build_texto(despedida)
    forma_pago = build_texto(forma_de_pago)
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
             despedida]
    #if validez:
        #story.insert(9, build_validez(validez))
    if texto_riesgo:
        story.insert(-6, build_texto_riesgo(texto_riesgo))
    #if condicionado: # El condicionado es el texto en sí.
    #    story.insert(-2, Spacer(1, 2 * cm))
    #    story.insert(-2, build_condicionado(condicionado))
    story = utils.aplanar([i for i in story if i])
    _dibujar_logo = lambda c, d: dibujar_logo(c, d, ruta_logo)
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
        pdf_condiciones = open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                         "condiciones_generales.pdf"), 
            "rb")
        merger = PyPDF2.PdfFileMerger()
        merger.append(pdf_presupuesto)
        merger.append(pdf_condiciones)
        combinado = os.path.join(gettempdir(),
                    "oferta_%s_%s.pdf" % (nombrecliente, 
                                          give_me_the_name_baby()))
        merger.write(open(combinado, "wb"))
        ruta_archivo = combinado
    return ruta_archivo

def go_from_presupuesto(presupuesto, 
                        incluir_condicionado_general = True):
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
        dir_fiscal = "Datos fiscales: %s %s %s %s" % (
                dde.nombre, 
                dde.get_dir_facturacion_completa(), 
                dde.str_cif_o_nif(), 
                dde.cif)
    except IndexError:
        lineas_empresa = []
        dir_fiscal = ""
    #lineas_contenido = presupuesto.lineasDePedido + presupuesto.servicios
    lineas_contenido = presupuesto.lineasDePresupuesto 
    datos_cliente = []
    if presupuesto.personaContacto != "":
        datos_cliente.append("A la atención de %s" % (
            presupuesto.personaContacto))
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
                    utils.float2str(presupuesto.calcular_base_imponible())+" €",
               "IVA %d%%" % (iva * 100): 
                    utils.float2str(presupuesto.calcular_total_iva())+" €", 
               "TOTAL": 
                    utils.float2str(presupuesto.calcular_importe_total())+" €", 
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
    try:
        fdp = "Forma de pago: %s" % presupuesto.formaDePago.toString()
    except AttributeError:
        fdp = ""
    nomarchivo = go(
      "Presupuesto %s (%s)" % (presupuesto.nombrecliente, 
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
       dir_fiscal = dir_fiscal)
    return nomarchivo


if __name__ == "__main__":
    try:
        go_from_presupuesto(pclases.Presupuesto.select()[-1])
    except:
        lineas_contenido = [(1.234, "Una cosa "*20, "1.245", `1.234*1.245`), 
                            (1, "Grñai mama", "1", "0.25"), 
                            ("0,25", "Otra cosa", "1", "0.25")] * 7
        lineas_empresa = ("American woman, co.", 
                          "Johnny Cash", 
                          "Alabama - 3213", 
                          "United States of America")
        datos_cliente = ("Lori Meyers", 
                         "los lunes se levanta a partir de las 2.", 
                         "con el sol", 
                         "qué calor")
        totales = {"Base imponible": "100.50 €", 
                   "IVA 21%": 100.5 * 0.21, 
                   "TOTAL": 100.5 * 1.21, 
                   "orden": ("Base imponible", "IVA 16%", "TOTAL")}
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

