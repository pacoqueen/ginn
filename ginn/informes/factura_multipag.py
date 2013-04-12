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

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, XPreformatted, Preformatted, PageBreak, KeepTogether, CondPageBreak, LongTable
from reportlab.platypus.flowables import Flowable
from reportlab.rl_config import defaultPageSize
from reportlab.lib import colors, enums
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
import sys, os#, Image
from framework import pclases
from formularios import utils, numerals
from informes.geninformes import give_me_the_name_baby, escribe, rectangulo, el_encogedor_de_fuentes_de_doraemon, agregarFila
from tempfile import gettempdir
from fixedpoint import FixedPoint

PAGE_HEIGHT = defaultPageSize[1]; PAGE_WIDTH = defaultPageSize[0]
estilos = getSampleStyleSheet()

class lastPageNumberFlowable(Flowable):

    def __init__(self, xoffset = 0, yoffset = 0):
        Flowable.__init__(self)
        self._xoffset = xoffset
        self._yoffset = yoffset

    def draw(self):
        canvas = self.canv
        if not canvas.hasForm("lastPageNumber"):
            canvas.beginForm("lastPageNumber")
            canvas.setFont("Times-Italic", 9)
            canvas.drawString(self._xoffset,
                              self._yoffset,
                              str(canvas.getPageNumber()))
            canvas.endForm()

class LineaHorizontal(Flowable):
    def __init__(self, ancho = None, grosor = 1):
        self.line_thickness = grosor
        if ancho:
            self._width = ancho
        else:
            self._width = None

    def wrap(self, availWidth, availHeight):
        if self._width is None:
            self._width = availWidth
        self._height = self.line_thickness
        return self._width, self._height

    def draw(self):
        self.canv.setLineWidth(self.line_thickness)
        orig = (PAGE_WIDTH / 2) - (self._width / 2)
        orig -= 2.75 * cm    # Margen al llamar a mi draw desde el build.
        self.canv.line(orig,
                       .5 * self.line_thickness,
                       self._width + orig,
                       .5 * self.line_thickness)

class Linea(Flowable):
    def __init__(self, desde, hasta, grosor = 1):
        """
        desde y hasta son pares de coordenadas.
        Aunque sea flowable, se ciñe a estos puntos.
        """
        self.line_thickness = grosor
        self.desde = desde
        self.hasta = hasta

    def wrap(self, availWidth, availHeight):
        """
        No voy a robar espacio de los demás flowables, así que no
        consumo espacio.
        """
        #return availWidth, availHeight
        return 0, 0

    def drawOn(self, canvas, *args, **kw):
        canvas.setLineWidth(self.line_thickness)
        canvas.line(self.desde[0], self.desde[1],
                    self.hasta[0], self.hasta[1])


def sanitize(d):
    """
    Sustituye todo lo que no sea texto:
    - Si es float, por su representación con puntos y una coma con 2 decimales.
    - Si es entero, por su equivalente en texto.
    """
    def tostr(v):
        if isinstance(v, (float, FixedPoint)):
            v = utils.float2str(v)
        elif isinstance(v, int):
            v = utils.int2str(v)
        elif isinstance(v, (list, tuple)):
            # Recursividad, divino tesoro...
            v = sanitize(v)
        return v

    if isinstance(d, dict):
        for k in d.keys():
            d[k] = tostr(d[k])
    elif isinstance(d, (list, tuple)):
        res = []
        for i in d:
            res.append(tostr(i))
        d = type(d)(res)
    return d

def cabecera_y_cliente(canvas,
                       doc,
                       datos_cliente,
                       datos_de_la_empresa,
                       datos_factura):
    """
    Escribe el texto "FACTURA" y los datos del cliente.
    Los datos del cliente vienen en un diccionario con:
    código (de cliente), cif, razón social, dirección, población, provincia.
    """
    fuente = "Helvetica"
    tamanno = 24
    # XXX CWT: Para poder taladrar y archivar sin comerse el cuerpo.
    canvas.translate(0.6*cm, 0)
    # XXX
    canvas.saveState()
    canvas.setFont(fuente, tamanno)
    canvas.drawString(PAGE_WIDTH
                        - canvas.stringWidth(escribe("FACTURA"),fuente,tamanno)
                        - 1.0*cm,
                      PAGE_HEIGHT - 1.5*cm,
                      escribe("FACTURA"))
    canvas.restoreState()
    tamanno = 12
    altura_linea = 16
    xCliente = (PAGE_WIDTH - 1*cm) / 2.5
    linea = (PAGE_HEIGHT-1.5*cm) - 0.10*cm - 2*cm
    rectangulo(canvas,
               (xCliente - 0.2*cm, PAGE_HEIGHT - 1.5*cm + altura_linea - 2*cm),
               (PAGE_WIDTH - 1*cm,
                (PAGE_HEIGHT- 1.5*cm + altura_linea)
                -(altura_linea*5 + 0.5*cm) - 2*cm),
               doble = True
              )
    canvas.drawString(xCliente,
                      linea,
                      escribe(
                        "Cód. cliente: %s        C.I.F.: %s" % (
                            datos_cliente['código'],
                            datos_cliente['cif'])))
    linea -= altura_linea
    el_encogedor_de_fuentes_de_doraemon(canvas,
                                        fuente,
                                        tamanno,
                                        xCliente,
                                        PAGE_WIDTH - 1*cm,
                                        linea,
                                        escribe(datos_cliente['razón social']))
    linea -= altura_linea
    el_encogedor_de_fuentes_de_doraemon(canvas,
                                        fuente,
                                        tamanno,
                                        xCliente,
                                        PAGE_WIDTH - 1*cm,
                                        linea,
                                        escribe(datos_cliente['dirección']))
    linea -= altura_linea
    canvas.drawString(xCliente,
                      linea,
                      escribe(datos_cliente['población']))
    linea -= altura_linea
    canvas.drawString(xCliente,
                      linea,
                      escribe(datos_cliente['provincia']))
    # Datos de la empresa
    dibujar_datos_empresa(canvas, datos_de_la_empresa)
    # Cabecera de factura
    build_tabla_cabecera(canvas, datos_factura, 22.5*cm)

def dibujar_datos_empresa(canvas, datos_de_la_empresa):
    """
    Dibuja los datos de la empresa en la parte superior.
    """
    logo, empresa = build_logo_y_empresa_por_separado(datos_de_la_empresa)
    logo.drawOn(canvas, 1*cm, PAGE_HEIGHT - 2.8 * cm)
    fuente = "Helvetica"
    tamanno = 16
    for i in range(len(empresa)):
        if i == 1:
            tamanno -= 4  # Primera línea (nombre empresa) un poco más grande.
        linea = PAGE_HEIGHT - 1.5 * cm
        el_encogedor_de_fuentes_de_doraemon(canvas,
                                            fuente,
                                            tamanno,
                                            3.25*cm,
                                            PAGE_WIDTH - 3*cm,
                                            linea - (i*0.55*cm),
                                            escribe(empresa[i]))


def build_tabla_cabecera(canvas, datos_factura, y1):
    # Cabecera.
    canvas.saveState()
    x1 = 1.0 * cm + 1
    limite = x1 + 0.9 * PAGE_WIDTH
    incremento = (limite - x1) / 3
    #y1 = 22.5 * cm
    y2 = y1 - 18
    for texto, clave in (("Código cliente", "codcliente"),
                         ("Nº Factura", "número"),
                         ("Fecha", "fecha")):
        x2 = x1 + incremento
        canvas.setFont("Times-Roman", 12)
        dato_factura = escribe(datos_factura[clave])
        rectangulo(canvas,
                   (x1, y1),
                   (x2, y2),
                   texto = dato_factura,
                   alinTxtX = "centro",
                   alinTxtY = "centro")
        canvas.setFont("Times-Roman", 10)
        #canvas.drawString(x1+0.2*cm, y1 + 3, texto)
        canvas.drawCentredString((x1+x2)/2, y1 + 3, texto)
        x1 += incremento
    canvas.restoreState()
    # Página x de y.
    canvas.saveState()
    canvas.setFont("Times-Italic", 9)
    canvas.drawRightString(0.9 * PAGE_WIDTH - 0.5 * cm,
                           1.0 * cm,
                           escribe("Página %d de " % canvas.getPageNumber()))
    canvas.doForm("lastPageNumber")
    canvas.restoreState()

def solo_cabecera(canvas,
                  doc,
                  datos_de_la_empresa,
                  datos_factura):
    """
    Escribe el texto "FACTURA" y los datos del cliente.
    Los datos del cliente vienen en un diccionario con:
    código (de cliente), cif, razón social, dirección, población, provincia.
    """
    fuente = "Helvetica"
    tamanno = 24
    # XXX CWT: Para poder taladrar y archivar sin comerse el cuerpo.
    canvas.translate(0.6*cm, 0)
    # XXX
    canvas.saveState()
    canvas.setFont(fuente, tamanno)
    canvas.drawString(PAGE_WIDTH
                        - canvas.stringWidth(escribe("FACTURA"),fuente,tamanno)
                        - 1.0*cm,
                      PAGE_HEIGHT - 1.5*cm,
                      escribe("FACTURA"))
    canvas.restoreState()
    # Datos de la empresa
    dibujar_datos_empresa(canvas, datos_de_la_empresa)
    #logo, empresa = build_logo_y_empresa_por_separado(datos_de_la_empresa)
    ##LineaHorizontal(0.9 * PAGE_WIDTH).drawOn(canvas, 78.0, 12.5*cm)
    ##LineaHorizontal(0.9 * PAGE_WIDTH).drawOn(canvas, 78.0, 12.4 *cm)
    #logo.drawOn(canvas, 1*cm, PAGE_HEIGHT - 2.8 * cm)
    #fuente = "Helvetica"
    #tamanno = 10
    #for i in range(len(empresa)):
    #    linea = PAGE_HEIGHT - 1.5 * cm
    #    el_encogedor_de_fuentes_de_doraemon(canvas,
    #                                        fuente,
    #                                        tamanno,
    #                                        3.25*cm,
    #                                        PAGE_WIDTH - 1*cm,
    #                                        linea - (i*0.5*cm),
    #                                        escribe(empresa[i]))
    # Cabecera.
    build_tabla_cabecera(canvas, datos_factura, 26.0*cm)

def build_tabla_contenido(data):
    """
    Construye la tabla del contenido del facturaVenta.
    Los datos deben venir en listas. Cada línea de la tabla, una tupla o lista
    con el código, descripción, cantidad, precio unitario (con dto. si lo
    lleva e IVA).
    El precio y cantidad deben ser flotantes para poder calcular el subtotal.
    """
    estilo_cabecera_tabla = ParagraphStyle("Cabecera tabla",
                                           parent=estilos["Heading3"])
    estilo_cabecera_tabla.fontName = "Times-Bold"
    estilo_cabecera_tabla.alignment = enums.TA_CENTER
    estilo_numeros_tabla = ParagraphStyle("Números tabla",
                                           parent=estilos["Normal"])
    estilo_numeros_tabla.alignment = enums.TA_RIGHT
    datos = [(Paragraph(escribe("Código"), estilo_cabecera_tabla),
              Paragraph(escribe("Descripción"), estilo_cabecera_tabla),
              Paragraph("Cantidad", estilo_cabecera_tabla),
              Paragraph("Precio/U", estilo_cabecera_tabla),
              Paragraph("Total c/IVA", estilo_cabecera_tabla))
            ]
    for d in data:
        fila = (escribe(d[0]),
                Paragraph(escribe(d[1]),estilos["Normal"]),
                Paragraph(escribe(utils.float2str(d[2])),estilo_numeros_tabla),
                Paragraph(escribe(utils.float2str(d[3])),estilo_numeros_tabla),
                Paragraph(escribe(utils.float2str(d[2] * d[3])),
                    estilo_numeros_tabla)
               )
        datos.append(fila)
    tabla = LongTable(datos,
                  colWidths = (PAGE_WIDTH * 0.13,
                               PAGE_WIDTH * 0.43,
                               PAGE_WIDTH * 0.10,
                               PAGE_WIDTH * 0.10,
                               PAGE_WIDTH * 0.14),
                  repeatRows = 1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("LINEBEFORE", (0, 0), (-1, 0), 0.25, colors.black),
        ("LINEBELOW", (0, 0), (-1, 0), 1.0, colors.black),
        ("LINEBELOW", (0, "splitlast"), (-1, "splitlast"), 1.0, colors.black),
        #("BOX", (0, 0), (-1, -1), 1.0, colors.black),
        ("LINEABOVE", (0, 0), (-1, 0), 1.0, colors.black),
        ("LINEBEFORE", (0, 0), (0, -1), 1.0, colors.black),
        ("LINEAFTER", (-1, 0), (-1, -1), 1.0, colors.black),
        #("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
        ("VALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (0, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("ALIGN", (-3, 1), (-1, -1), "RIGHT"),
        #("ALIGN", (0, 1), (0, -1), "DECIMAL"), <- No puedo cambiar
        #                               el pivotChar de "." a ",". No me vale.
        ("ALIGN", (-1, 1), (-1, -1), "CENTER"),
        ("ALIGN", (0, 1), (0, -1), "CENTER"),
        #("RIGHTPADDING", (0, 1), (0, -1), 0.75 * cm),
        ]))
    return tabla

class TablaFija(Table):
    """
    Tabla pero con la esquina arriba-izquierda forzada a una posición.
    """
    def __init__(self, ox, oy, *args, **kw):
        Table.__init__(self, *args, **kw)
        self.ox = ox
        self.oy = oy

    _old_drawOn = Table.drawOn

    def wrap(self, availWidth, availHeight):
        w, h = Table.wrap(self, availWidth, availHeight)
        #print h, w, availHeight, availWidth
        h = 3*cm
        w = 0.9 * PAGE_WIDTH
        #return availWidth, availHeight
        return (w, h)

    def drawOn(self, canvas, x = None, y = None, *args, **kw):
        #print x, y, args, kw
        #print self.ox, self.oy
        #if self.oy > y:
        #    canvas.showPage()
        x = self.ox
        y = self.oy
        self._old_drawOn(canvas, x, y, *args, **kw)

    def draw(self, *args, **kw):
        #print args, kw
        Table.draw(self, *args, **kw)

    def split(self, availWidth, availHeight):
        return []

def build_tabla_totales(totales):
    """
    Construye una tabla con los totales del facturaVenta.
    La tabla tiene dos filas, cabecera y desglose. La variable «totales» es
    una lista con los totales *en el siguiente orden*:
    base imponible, porcentaje IVA en fracción de 1, y total.
    La base imponible incluye los descuentos de las LDVs y demás.
    """
    datos = [["Base imponible", "%d%% IVA" % (totales[1]*100), "Total"],
             [totales[0], totales[2] - totales[0], totales[2]]]
    datos = sanitize(datos)
    estilo_numeros_tabla = ParagraphStyle("Números tabla",
                                           parent=estilos["Normal"])
    estilo_numeros_tabla.alignment = enums.TA_RIGHT
    estilo_numeros_tabla.fontSize += 2
    datos = [[Paragraph(celda, estilos["Normal"]) for celda in datos[0]] ,
             [Paragraph(celda, estilo_numeros_tabla) for celda in datos[1]]]
    tabla = TablaFija(78,
                      2.5*cm + 3*cm + 0.25*cm,
                      datos,
                      colWidths = (PAGE_WIDTH * (0.9/3),)*3)
    #tabla = Table(datos,
    #              colWidths = (PAGE_WIDTH * (0.9/3),)*3)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("LINEBELOW", (0, 0), (-1, 0), 1.0, colors.black),
        ("BOX", (0, 0), (-1, -1), 1.0, colors.black),
        ("INNERGRID", (0, 0), (-1, -1), 1.0, colors.black),
        ("ALIGN", (0, 0), (-1, 0), "LEFT"),
        ]))
    return tabla

def build_tabla_vencimientos(observaciones, vencimientos, forma_de_pago):
    """
    Los tres parámetros pueden ser una única cadena o una lista de cadenas.
    Si es lo segundo, cada elemento irá en una celda independiente.
    """
    datos = [["Observaciones", "Vencimientos", "Forma de pago"]]
    for columna, lista in ((0, observaciones),
                           (1, vencimientos),
                           (2, forma_de_pago)):
        if isinstance(lista, str):
            lista = [lista]
        fila = 1
        for elemento in lista:
            try:
                datos[fila][columna] = elemento
            except IndexError:
                datos.append(["", "", ""])
                datos[fila][columna] = elemento
            finally:
                fila += 1
    datos = sanitize(datos)
    estilo_cont_tabla = ParagraphStyle("Contenido tabla",
                                       parent=estilos["Normal"])
    estilo_cont_tabla.alignment = enums.TA_JUSTIFY
    if len(observaciones) > 2: # Si trae más observaciones aparte del importe 
            # en letra de la factura, hay que reducir la fuente para que no 
            # se me suba el borde superior y me tape los importes.
        estilo_cont_tabla.fontSize -= 2
        estilo_cont_tabla.spaceAfter -= 2
    else:
        estilo_cont_tabla.fontSize += 2
    _datos = []
    fila = []
    for celda in datos[0]:
        #fila.append(Paragraph(celda, estilos["Normal"]))
        fila.append(escribe(celda))
    _datos.append(fila)
    for fila_datos in datos[1:]:
        fila = []
        for celda in fila_datos:
             fila.append(Paragraph(escribe(celda), estilo_cont_tabla))
        _datos.append(fila)
    datos = _datos
    tabla = TablaFija(78,
                      3*cm,
                      datos,
                      colWidths = (PAGE_WIDTH * 0.9 * 0.5,
                                   PAGE_WIDTH * 0.9 * 0.25,
                                   PAGE_WIDTH * 0.9 * 0.25))
    #tabla = Table(datos,
    #              colWidths = (PAGE_WIDTH * (0.9/3),)*3)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("LINEBELOW", (0, 0), (-1, 0), 1.0, colors.black),
        ("BOX", (0, 0), (-1, -1), 1.0, colors.black),
        ("LINEBEFORE", (1, 1), (1, -1), 0.5, colors.black),
        ("LINEBEFORE", (2, 1), (2, -1), 0.5, colors.black),
        #("INNERGRID", (0, 0), (-1, -1), 1.0, colors.black),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ]))
    return tabla

def build_marco_logo_y_empresa(dde):
    """
    dde es una lista con la ruta al logotipo de la empresa (o None) y una
    serie de líneas de texto con los datos a mostrar de la empresa.
    Devuelve una tabla con los marcos transparentes con el logo y las
    líneas.
    """
    if dde[0] != None:
        logo = Image(dde[0])
        logo.drawHeight = 2*cm * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 2*cm
    else:
        logo = Paragraph("", estilos["Normal"])
    lineas_empresa = dde[1:]
    if len(lineas_empresa) <= 3:
        empresa = Preformatted("\n".join(lineas_empresa), estilos["Normal"])
    else:
        texto_empresa = lineas_empresa[0] + "\n"
            #+ ". ".join(lineas_empresa[1:])
        resto_lineas = lineas_empresa[1:]
        pivot = len(resto_lineas)/2
        r1, r2 = resto_lineas[:pivot], resto_lineas[pivot:]
        texto_empresa += ". ".join(r1) + "\n" + ". ".join(r2)
        empresa = Preformatted(texto_empresa, estilos["Normal"])
    datos = [[logo, empresa]]
    tabla = Table(datos,
                  colWidths = (PAGE_WIDTH * 0.25,
                               PAGE_WIDTH * 0.65))
    tabla.setStyle(TableStyle([
        ("ALIGN", (0, 0), (1, 0), "RIGHT"),
        ("ALIGN", (1, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "CENTER"),
        ]))
    return tabla

def build_logo_y_empresa_por_separado(dde):
    """
    Ganas de matar aumentando...
    dde es una lista con la ruta al logotipo de la empresa (o None) y una
    serie de líneas de texto con los datos a mostrar de la empresa.
    Devuelve una imagen con el logotipo y una lista de líneas con los
    datos de la empresa para dibujarlas (drawText) al lado.
    Si no hay logo, devuelve None y la lista de líneas.
    """
    if dde[0] != None:
        logo = Image(dde[0])
        logo.drawHeight = 2*cm * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 2*cm
    else:
        logo = None
    lineas_empresa = dde[1:]
    if len(lineas_empresa) <= 3:
        while len(lineas_empresa) < 3:
            lineas_empresa.append("")
        empresa = lineas_empresa
    else:
        texto_empresa = lineas_empresa[0] + "\n"
            #+ ". ".join(lineas_empresa[1:])
        resto_lineas = lineas_empresa[1:]
        pivot = len(resto_lineas)/2
        r1, r2 = resto_lineas[:pivot], resto_lineas[pivot:]
        texto_empresa += ". ".join(r1) + "\n" + ". ".join(r2)
        # Escuse moi, pero necesito aprovechar lo que ya hay. Un split no
        # hace daño a nadie, si acaso "un poquito" al rendimiento.
        lineas_empresa = texto_empresa.split("\n")
    return logo, lineas_empresa

def go(titulo,
       ruta_archivo,
       datos_cliente,
       datos_factura,
       lineas_contenido,
       totales,
       datos_de_la_empresa,
       observaciones = "",
       vencimientos = [],
       forma_de_pago = ""):
    """
    Recibe el título del documento y la ruta completa del archivo PDF,
    los datos del cliente en un diccionario, los del factura también como
    diccionario, las líneas como lista de listas, los totales como lista
    y otra lista con la ruta al logotipo como primer elemento y tantas líneas
    como datos de la empresa se quieran mostrar junto al logo.
    """
    doc = SimpleDocTemplate(ruta_archivo,
                            title = titulo,
                            topMargin = 4.30*cm,
                            #bottomMargin = 2*cm)
                            bottomMargin = 4*cm)
                            #leftMargin = 1*cm,
                            #rigthMargin = 1*cm)
    contenido = build_tabla_contenido(lineas_contenido)
    tabla_totales = build_tabla_totales(totales)
    vencimientos = build_tabla_vencimientos(observaciones,
                                            vencimientos,
                                            forma_de_pago)
    #texto = build_texto()
    story = [#Spacer(1, 1.60 * cm),   # Chispa más o menos los datos de cliente.
             #encabezado,
             Spacer(1, 3.50 * cm),
             contenido,
             Linea((1.05*cm, 24.5*cm - 3*cm),
                   (1.05*cm, 2.5*cm + 3*cm + 0.25*cm)),
             Linea((PAGE_WIDTH - 1.05*cm, 24.5*cm - 3*cm),
                   (PAGE_WIDTH - 1.05*cm, 2.5*cm + 3*cm + 0.25*cm)),
             Spacer(1, 0.15 * cm),
             tabla_totales,
             Spacer(1, 0.25 * cm),
             vencimientos,
             lastPageNumberFlowable(0.9*PAGE_WIDTH - 0.5*cm + 1, 1.0*cm)]
             #Spacer(1, 0.15 * cm),
             # Línea doble.
             #KeepTogether([LineaHorizontal(0.9 * PAGE_WIDTH),
             #              Spacer(1, 0.05 * cm),
             #              LineaHorizontal(0.9 * PAGE_WIDTH)]),
             #Spacer(1, 0.15 * cm),
             #CondPageBreak(13*cm),
             #logo_y_empresa,
             #Spacer(1, 0.25 * cm),
             #texto]
    story = utils.aplanar([i for i in story if i])
    _cabecera_y_cliente = lambda c, d: cabecera_y_cliente(c,
                                                          d,
                                                          datos_cliente,
                                                          datos_de_la_empresa,
                                                          datos_factura)
    _solo_cabecera = lambda c, d: solo_cabecera(c,
                                                d,
                                                datos_de_la_empresa,
                                                datos_factura)
    doc.build(story,
              onFirstPage = _cabecera_y_cliente,
              onLaterPages = _solo_cabecera)
    return ruta_archivo

def go_from_facturaVenta(facturaVenta):
    """
    Construye el PDF a partir de un objeto facturaVenta y no de sus datos
    sueltos.
    """
    cliente = facturaVenta.cliente
    datos_cliente = {"código": cliente.id,
                     "cif": cliente.cif,
                     "razón social": cliente.nombre,
                     "dirección": cliente.direccion,
                     "población": cliente.ciudad,
                     "provincia": cliente.provincia}
    if cliente.cp and cliente.cp.strip():
        datos_cliente["población"] = (cliente.cp + " - "
                                      + datos_cliente["población"])
    datos_factura = {"fecha": utils.str_fecha(facturaVenta.fecha),
                     "número": facturaVenta.numfactura,
                     "codcliente": facturaVenta.cliente
                                    and `facturaVenta.cliente.id`
                                    or ""}
    iva = cliente.iva
    # TODO: ¿Usar el float2str_autoprecision?
    lineas_contenido = [(ldv.producto.codigo,
                         ldv.producto.descripcion,
                         ldv.cantidad,
                         ldv.precio * (1.0 - ldv.descuento) * (1 + iva))
                        for ldv in facturaVenta.lineasDeVenta]
    lineas_contenido += [("",
                          srv.concepto,
                          srv.cantidad,
                          srv.precio * (1.0 - srv.descuento) * (1 + iva))
                         for srv in facturaVenta.servicios]
    totales = [facturaVenta.calcular_base_imponible(),
               iva,
               facturaVenta.calcular_total()]
    try:
        dde = pclases.DatosDeLaEmpresa.select()[0]
        datos_de_la_empresa = [os.path.join("..", "imagenes", dde.logo),
                               dde.nombre +
                                (dde.cif and " (" + dde.str_cif_o_nif() +": " + dde.cif + ")" or ""),
                               dde.direccion,
                               "%s %s (%s), %s" % (dde.cp,
                                                   dde.ciudad,
                                                   dde.provincia,
                                                   dde.pais),
                               ]
        if dde.fax:
            if dde.fax.strip() == dde.telefono.strip():
                datos_de_la_empresa.append("Telf. y fax: %s" % dde.telefono)
            else:
                datos_de_la_empresa.append("Telf.: %s" % (dde.telefono))
                datos_de_la_empresa.append("Fax: %s" % (dde.fax))
        if dde.email:
            datos_de_la_empresa.append(dde.email)
    except IndexError:
        lineas_empresa = [None]
    nomarchivo = os.path.join(gettempdir(),
                              "facturaVenta_%s.pdf" % give_me_the_name_baby())
    vencimientos = []
    forma_de_pago = []
    vtos = facturaVenta.vencimientosCobro[:]
    vtos.sort(lambda v1, v2: (v1.fecha < v2.fecha and 1)
                              or (v1.fecha > v2.fecha and -1)
                              or 0)
    for v in vtos:
        strvto = "%s (%s €)" % (utils.str_fecha(v.fecha),
                                utils.float2str(v.importe))
        vencimientos.append(strvto)
        forma_de_pago.append(v.observaciones)
    observaciones = ["Importa la presente factura:",
                     numerals.numerals(totales[-1],
                                       moneda = "EUROS",
                                       fraccion = "CÉNTIMOS").upper()]
    if facturaVenta.observaciones:
        observaciones.append(facturaVenta.observaciones)
    return go("Factura de venta %s (%s)" % (
                facturaVenta.cliente.nombre,
                utils.str_fecha(facturaVenta.fecha)),
              nomarchivo,
              datos_cliente,
              datos_factura,
              lineas_contenido,
              totales,
              datos_de_la_empresa,
              observaciones,
              vencimientos,
              forma_de_pago)

if __name__ == "__main__":
    try:
        #print go_from_facturaVenta(pclases.FacturaVenta.select()[-1])
        print go_from_facturaVenta(pclases.FacturaVenta.get(115))
    #except Exception, msg:
    except ZeroDivisionError, msg:
        sys.stderr.write(`msg`)
        datos_cliente = {"código": 123,
                         "cif": "12345678-Z",
                         "razón social": "Fulanito de tal y pascual, S.L.U.",
                         "dirección": "Rue del percebe, 13. 4º B",
                         "población": "Chiquitistán",
                         "provincia": "Huelva"}
        datos_factura = {"fecha": "10/06/2008",
                         "número": "A12314",
                         "codcliente": "12"}
        lineas_contenido = [
            ("COD1", "Una cosa "*20, 1.234, 1.245, "PEDIDO 1"),
            ("", "Grñai mama", 1, 1, ""),
            ("1234567890123", "Otra cosa", 10, 0.33, "123154a")] * 7
        totales = [100.0, 0.16, 116.0]
        datos_de_la_empresa = ["../imagenes/dorsia.png",
                               "Línea empresa 1",
                               "Línea empresa 2",
                               "Línea empresa 3"]
        print go("FacturaVenta",
                 "/tmp/facturaVenta.pdf",
                 datos_cliente,
                 datos_factura,
                 lineas_contenido,
                 totales,
                 datos_de_la_empresa)

