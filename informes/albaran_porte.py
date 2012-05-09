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

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, XPreformatted, Preformatted, PageBreak, KeepTogether, CondPageBreak
from reportlab.platypus.flowables import Flowable
from reportlab.rl_config import defaultPageSize
from reportlab.lib import colors, enums
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet 
import sys, os#, Image
from factura_multipag import TablaFija

try:
    import pclases, utils
except ImportError:
    try:
        import sys, os
        sys.path.insert(0, os.path.join("..", "framework"))
        import pclases, utils
    except ImportError:
        sys.path.insert(0, ".")
        import pclases, utils
try:
    from geninformes import give_me_the_name_baby, escribe, rectangulo, el_encogedor_de_fuentes_de_doraemon, agregarFila
except ImportError:
    import sys
    sys.path.append(os.path.join("..", "informes"))
from geninformes import give_me_the_name_baby, escribe, rectangulo, el_encogedor_de_fuentes_de_doraemon, agregarFila
from tempfile import gettempdir

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

def sanitize(d):
    """
    Sustituye todo lo que no sea texto:
    - Si es float, por su representación con puntos y una coma con 2 decimales.
    - Si es entero, por su equivalente en texto.
    """
    def tostr(v):
        if isinstance(v, float):
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
                       titular, 
                       datos_albaran):
    """
    Escribe el texto "ALBARÁN/CARTA DE PORTE" y los datos del cliente.
    Los datos del cliente vienen en un diccionario con: 
    código (de cliente), cif, razón social, dirección, población, provincia.
    """
    fuente = "Helvetica"
    tamanno = 12
    canvas.drawString(1.0*cm, 
                      PAGE_HEIGHT - 1.5*cm, 
                      escribe("ALBARÁN/CARTA DE PORTE"))
    altura_linea = 16
    xCliente = (PAGE_WIDTH - 1*cm) / 2.5
    linea = (PAGE_HEIGHT-1.5*cm) - 0.10*cm 
    rectangulo(canvas, 
               (xCliente - 0.2*cm, PAGE_HEIGHT - 1.5*cm + altura_linea), 
               (PAGE_WIDTH - 1*cm, 
                (PAGE_HEIGHT- 1.5*cm + altura_linea)-(altura_linea*5 + 0.5*cm))
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
                                        escribe("Razón social: %s" 
                                            % datos_cliente['razón social']))
    #canvas.drawString(xCliente, 
    #                  linea, 
    #                  escribe("Razón social: %s"%datos_cliente['razón social']))
    linea -= altura_linea
    el_encogedor_de_fuentes_de_doraemon(canvas, 
                                        fuente, 
                                        tamanno, 
                                        xCliente, 
                                        PAGE_WIDTH - 1*cm, 
                                        linea, 
                                        escribe("Dirección: %s" 
                                            % datos_cliente['dirección']))
    #canvas.drawString(xCliente, 
    #                  linea, 
    #                  escribe("Dirección: %s" % datos_cliente['dirección']))
    linea -= altura_linea
    canvas.drawString(xCliente, 
                      linea, 
                      escribe("Población: %s" % datos_cliente['población']))
    linea -= altura_linea
    canvas.drawString(xCliente, 
                      linea, 
                      escribe("Provincia: %s" % datos_cliente['provincia']))
    # Y el pie de página:
    logo, empresa = build_logo_y_empresa_por_separado(datos_de_la_empresa)
    LineaHorizontal(0.9 * PAGE_WIDTH).drawOn(canvas, 78.0, 12.5*cm)
    LineaHorizontal(0.9 * PAGE_WIDTH).drawOn(canvas, 78.0, 12.4 *cm)
    logo.drawOn(canvas, 3*cm, 10 * cm)
    fuente = "Helvetica"
    tamanno = 10
    for i in range(len(empresa)):
        linea = 11.5 * cm
        el_encogedor_de_fuentes_de_doraemon(canvas, 
                                            fuente, 
                                            tamanno, 
                                            5.25*cm, 
                                            PAGE_WIDTH - 1*cm, 
                                            linea - (i*0.5*cm), 
                                            escribe(empresa[i]))
    #logo_y_empresa.drawOn(canvas, 10.5*cm, 78.0)
    texto = build_texto(titular)
    lineas = []
    for l in [p.text for p in texto._content]:
        lineas.extend(l.split("\n"))
    y = 9.5*cm
    tamanno = 8
    centrado = False
    for linea in lineas:
        linea = linea.replace("&nbsp;", "")
        if "<b>" in linea:
            fuente = "Times-Bold"
            linea = linea.replace("<b>", "").replace("</b>", "")
            # Aprovechando que el Pisuerga...
            centrado = True
        else:
            fuente = "Times-Roman"
        if "<font size=12>" in linea:
            tamanno = 12
            linea = linea.replace("<font size=12>", "").replace("</font>", "")
        else:
            tamanno = 10
        lineas_agregadas = agregarFila(1*cm, 
                                       y, 
                                       PAGE_WIDTH - 1*cm, 
                                       escribe(linea), 
                                       canvas, 
                                       fuente, 
                                       tamanno, 
                                       centrado = centrado)
        y -= lineas_agregadas * 10
    #canvas.drawString(PAGE_WIDTH - 2*cm, 2*cm, str(canvas.getPageNumber()))
    #texto.drawOn(canvas, 9*cm, 72.0)
    # Página x de y.
    canvas.saveState()
    canvas.setFont("Times-Italic", 9)
    canvas.drawRightString(PAGE_WIDTH - 1.5*cm, 
                           12.7*cm, 
                           escribe("Página %d de " % canvas.getPageNumber()))
    canvas.doForm("lastPageNumber")
    canvas.restoreState()
    # Cabecera.
    # Sí, ahora va aquí. No hace falta que ponga el CWT, ¿o sí?
    canvas.saveState()
    x1 = 1.0 * cm + 1
    limite = x1 + 0.9 * PAGE_WIDTH
    incremento = (limite - x1) / 4
    y1 = 24.5 * cm
    y2 = y1 - 18
    for texto, clave in (("Fecha", "fecha"), 
                         ("Nº Albarán", "número"), 
                         ("Kilos", "kilos"), 
                         ("Bultos", "bultos")):
        x2 = x1 + incremento
        canvas.setFont("Times-Roman", 12)
        rectangulo(canvas, 
                   (x1, y1), 
                   (x2, y2), 
                   texto = escribe(datos_albaran[clave]), 
                   alinTxtX = "centro", 
                   alinTxtY = "centro")
        canvas.setFont("Times-Roman", 10)
        canvas.drawString(x1+0.2*cm, y1 + 3, texto)
        x1 += incremento
    canvas.restoreState()

def build_encabezado(datos_albaran):
    """
    Devuelve una tabla de dos líneas con los datos del albarán, que es un 
    diccionario de: fecha -como texto-, número (de albarán), kilos, 
    bultos.
    """
    datos_albaran = sanitize(datos_albaran)
    datos = [["Fecha", escribe("Nº Albarán"), "Kilos", "Bultos"], 
             [datos_albaran["fecha"], datos_albaran["número"], 
                datos_albaran["kilos"], datos_albaran["bultos"]]]
    estilo_centrado = ParagraphStyle("Alineado centrado", 
                                     parent=estilos["Normal"])
    estilo_centrado.alignment = enums.TA_CENTER
    estilo_centrado.fontSize += 2
    datos = [[Paragraph(celda, estilos["Normal"]) for celda in datos[0]] ,
             [Paragraph(celda, estilo_centrado) for celda in datos[1]]]
    tabla = Table(datos, 
                  colWidths = (PAGE_WIDTH * 0.9/4,)*4) 
    tabla.setStyle(TableStyle([
        ("BOX", (0, 1), (-1, -1), 1.0, colors.black),
        ("INNERGRID", (0, 1), (-1, -1), 0.25, colors.black), 
        ("ALIGN", (0, 0), (-1, 0), "LEFT"), 
        ("ALIGN", (0, 1), (-1, 1), "CENTER"), 
        ]))
    return tabla

def build_tabla_contenido(data):
    """
    Construye la tabla del contenido del albaranSalida.
    Los datos deben venir en listas. Cada línea de la tabla, una tupla o lista 
    con el código, descripción, cantidad, precio unitario (con dto. si lo 
    lleva e IVA) y número de pedido.
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
              #Paragraph("Total c/IVA", estilo_cabecera_tabla), 
              # CWT: Prefiere la carta de portes sin IVA.
              Paragraph("Total", estilo_cabecera_tabla), 
              Paragraph(escribe("Nº Pedido"), estilo_cabecera_tabla))
            ]
    for d in data:
        fila = (escribe(d[0]), 
                Paragraph(escribe(d[1]),estilos["Normal"]), 
                Paragraph(escribe(utils.float2str(d[2])),estilo_numeros_tabla),
                Paragraph(escribe(utils.float2str(d[3])),estilo_numeros_tabla),
                Paragraph(escribe(utils.float2str(d[2] * d[3])), 
                    estilo_numeros_tabla),
                escribe(d[4])
               )
        datos.append(fila)
    tabla = Table(datos, 
                  colWidths = (PAGE_WIDTH * 0.13, 
                               PAGE_WIDTH * 0.35, 
                               PAGE_WIDTH * 0.09, 
                               PAGE_WIDTH * 0.09, 
                               PAGE_WIDTH * 0.13, 
                               PAGE_WIDTH * 0.11), 
                  repeatRows = 1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey), 
        ("LINEBEFORE", (0, 0), (-1, -1), 0.25, colors.black),
        ("LINEBELOW", (0, 0), (-1, 0), 1.0, colors.black), 
        ("LINEBELOW", (0, "splitlast"), (-1, "splitlast"), 1.0, colors.black), 
        ("BOX", (0, 0), (-1, -1), 1.0, colors.black),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black), 
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

#class TablaFija(Table):
#    """
#    Tabla pero con la esquina arriba-izquierda forzada a una posición.
#    """
#    def __init__(self, ox, oy, *args, **kw):
#        Table.__init__(self, *args, **kw)
#        self.ox = ox
#        self.oy = oy

#    _old_drawOn = Table.drawOn
#    
#    def drawOn(self, canvas, x = None, y = None, *args, **kw):
#        x = self.ox
#        y = self.oy
#        self._old_drawOn(canvas, x, y, *args, **kw)

#    def split(self, availWidth, availHeight):
#        return []

def build_tabla_totales(totales):
    """
    Construye una tabla con los totales del albaranSalida.
    La tabla tiene dos filas, cabecera y desglose. La variable «totales» es 
    una lista con los totales *en el siguiente orden*:
    base imponible, porcentaje IVA en fracción de 1, y total.
    La base imponible incluye los descuentos de las LDVs y demás.
    """
    try:
        striva = "%d%% IVA" % (totales[1]*100)
    except TypeError:
        striva = "  % IVA"
    try:
        strimpiva = totales[2] - totales[0]
    except TypeError:
        strimpiva = ""
    datos = [["Base imponible", striva, "Total"], 
             [totales[0], strimpiva, totales[2]]] 
    datos = sanitize(datos)
    estilo_numeros_tabla = ParagraphStyle("Números tabla", 
                                           parent=estilos["Normal"])
    estilo_numeros_tabla.alignment = enums.TA_RIGHT
    estilo_numeros_tabla.fontSize += 2
    datos = [[Paragraph(celda, estilos["Normal"]) for celda in datos[0]] ,
             [Paragraph(celda, estilo_numeros_tabla) for celda in datos[1]]]
    tabla = TablaFija(78, 
                      13.2*cm,
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

def build_texto(titular):
    """
    Construye el texto genérico de la carta de portes.
    """
    estilo_texto = ParagraphStyle("Texto", 
                                  parent = estilos["Normal"])
    estilo_texto.alignment = enums.TA_JUSTIFY
    estilo_texto.firstLineIndent = 24
    estilo_texto.fontSize = 8
    estilo_texto.leading = 9
    texto = """%s hace constar que esta materia se admite al transporte por carretera de acuerdo con las disposiciones del proyecto europeo del transporte de mercancías peligrosas por carretera (ADR) y del reglamento nacional para el transporte de mercancías peligrosas por carretera (TPC).
            El abajo firmante (conductor y/o transportista) declara:
            1.- Que el vehículo cargado cumple las condiciones que establece el reglamento nacional para el transporte de mercancías peligrosas por carretera (ADR/TPC).
            2.- Que se ha efectuado correctamente la carga y/o estiba de la mercancía de acuerdo con el citado reglamento.
            3.- Que ha recibido la hoja de instrucciones escritas respecto a:
                &nbsp;&nbsp;&nbsp;&nbsp;- Naturaleza del peligro de la mercancía a transportar.
                &nbsp;&nbsp;&nbsp;- Medidas de seguridad y otras a tener en cuenta en caso de accidentes, incendio, derrame y otros, todas las cuales ha leído y conoce.
            4.- Conocer las disposiciones generales y especiales sobre vehículos, carga, descarga y manipulación de la mercancía, circulación y otras que se establecen para este transporte en el citado reglamento.
            5.- El transportista asume la responsabilidad por cualquier accidente ocurrido durante el transporte, sea cual fuere el lugar del siniestro una vez que la mercancía le haya sido entregada.
            """ % titular
    p = [Paragraph(escribe(t), estilo_texto) for t in texto.split("\n")]
    estilo_texto2 = ParagraphStyle("Texto2", 
                                   parent = estilo_texto)
    estilo_texto2.alignment = enums.TA_CENTER
    estilo_texto2.firstLineIndent = 0
    #estilo_texto2.fontSize = 8
    texto2 = """<b><font size=12>UN 1263, PINTURAS O PRODUCTOS PARA LA PINTURA, 3, II, ADR</b></font>"""
    texto3 = """

GRG    DEPÓSITO 600L    BIDÓN 200L    BIDÓN 100L    ENVASES METÁLICOS    GARRAFAS 60L    GARRAFAS 25L

LEY 11/79 (ART.18.1 DEL REGLAMENTO) el responsable de la entrega del envase usado será el poseedor final

Fdo. Conductor  Matrícula:         Fdo. El expedidor        Fdo. El cliente        Fdo. Central de carga
            """
    p.append(XPreformatted(escribe(texto2), estilo_texto2))
    p.append(XPreformatted(escribe(texto3), estilo_texto2))
    return KeepTogether(p)

def build_mas_texto(titular):
    """
    Construye más texto genérico de la carta de portes.
    """
    estilo_texto = ParagraphStyle("Texto", 
                                  parent = estilos["Normal"])
    estilo_texto.alignment = enums.TA_JUSTIFY
    estilo_texto.firstLineIndent = 24
    estilo_texto.fontSize = 8
    texto = """%s hace constar que esta materia se admite al transporte por carretera, de acuerdo con las disposiciones del proyecto europeo del transporte de mercancías peligrosas por carretera (ADR) y del reglamento nacional para el transporte de mercancías peligrosas por carretera (TPC).
            El abajo firmante (conductor y/o transportista) declara:
            6.- Que el vehículo cargado cumple las condiciones que establece el Reglamento Nacional para el Transporte de Mercancías Peligrosas por carretera (ADR/TPC).
            7.- Que se ha efectuado correctamente la carga y/o estiba de la mercancía de acuerdo con el citado Reglamento.
            8.- Que ha recibido la hoja de instrucciones escrita respecto a:
                &nbsp;&nbsp;&nbsp;&nbsp;- Naturaleza del peligro de la mercancía a transportar.
                &nbsp;&nbsp;&nbsp;- Medidas de seguridad y otras a tener en cuenta en caso de accidentes, incendio, derrame y otros, todas las cuales ha leído y conoce.
            9.- Conocer las disposiciones generales y especiales sobre vehículos, carga, descarga y manipulación de la mercancía, circulación y otras que se establecen para este transporte en el citado Reglamento.
            10.- El transportista asume la responsabilidad por cualquier accidente ocurrido durante el transporte, sea cual fuere el lugar del siniestro una vez que la mercancía le haya sido entregada.
            """ % titular
    p = [Paragraph(escribe(t), estilo_texto) for t in texto.split("\n")]
    estilo_texto2 = ParagraphStyle("Texto2", 
                                   parent = estilo_texto)
    estilo_texto2.alignment = enums.TA_CENTER
    estilo_texto2.firstLineIndent = 0
    #estilo_texto2.fontSize = 8
    texto2 = """<b><font size=12>UN 1263, PINTURAS O PRODUCTOS PARA LA PINTURA, 3, II, ADR</b></font>

GRG    DEPÓSITO 600L    BIDÓN 200L    BIDÓN 100L    ENVASES METÁLICOS    GARRAFAS 60L    GARRAFAS 25L

LEY 11/79 (ART.18.1 DEL REGLAMENTO) EL RESPONSABLE DE LA ENTREGA DEL ENVASE USADO SERÁ EL POSEEDOR FINAL

FDO. CONDUCTOR  MATRÍCULA:         FDO. EL EXPEDIDOR        FDO. EL CLIENTE
    """
    p.append(XPreformatted(escribe(texto2), estilo_texto2))
    p.append(XPreformatted("    FECHA:", estilo_texto))
    return p

def build_todavia_mas_texto():
    """
    Construye más texto genérico de la carta de portes.
    """
    estilo_texto = ParagraphStyle("Texto", 
                                  parent = estilos["Normal"])
    estilo_texto.alignment = enums.TA_JUSTIFY
    estilo_texto.firstLineIndent = 24
    estilo_texto.fontSize = 12
    texto = """
    Transporte que no excede de los límites establecidos en el capítulo 1.1.3.6.
    """
    estilo_texto2 = ParagraphStyle("Texto2", 
                                   parent = estilo_texto)
    estilo_texto2.alignment = enums.TA_CENTER
    estilo_texto2.firstLineIndent = 0
    #estilo_texto2.fontSize = 8
    p = Paragraph(escribe(texto), estilo_texto2)
    return p

def cuadritos_en_ruta():
    """
    Devuelve dos flowables:
    Un texto centrado con el texto de "ENVASES VACÍOS..." y una tabla 
    con el texto y los cuadraditos que se rellenan a mano durante la ruta 
    del transportista.
    """
    estilo_centrado = ParagraphStyle("Alineado centrado", 
                                    parent=estilos["Normal"])
    estilo_centrado.alignment = enums.TA_CENTER
    cab = Paragraph(escribe("ENVASES VACÍOS SIN LIMPIAR, 3 A.D.R."), 
                    estilo_centrado)
    datos = [["G.R.G. 1.000L", "", "", "BIDONES 100L", ""], 
             ["",              "", "", "",             ""], 
             ["DEPÓSITO 600L", "", "", "BIDONES 50L",  ""], 
             ["",              "", "", "",             ""], 
             ["BIDONES 200L",  "", "", "GARRAFAS 60L", ""],
             ["",              "", "", "",             ""], 
             ["BIDONES 25L",   "", "", "BIDONES 10L", ""]]
    datos = [[escribe(c) for c in fila] for fila in datos]
    tabla = Table(datos, 
                  colWidths = (3*cm, 0.75*cm, 5*cm, 3*cm, 0.75*cm))
    tabla.setStyle(TableStyle([
        ("BOX", (1, 0), (1, 0), 1.0, colors.black),
        ("BOX", (4, 0), (4, 0), 1.0, colors.black),
        ("BOX", (1, 2), (1, 2), 1.0, colors.black),
        ("BOX", (4, 2), (4, 2), 1.0, colors.black),
        ("BOX", (1, 4), (1, 4), 1.0, colors.black),
        ("BOX", (4, 4), (4, 4), 1.0, colors.black),
        ("BOX", (1, 6), (1, 6), 1.0, colors.black),
        ("BOX", (4, 6), (4, 6), 1.0, colors.black),
        ]))
    return KeepTogether([Spacer(1, 0.3*cm), cab, Spacer(1, 0.5*cm), tabla])

def go(titulo, 
       ruta_archivo, 
       datos_cliente, 
       datos_albaran, 
       lineas_contenido, 
       totales, 
       datos_de_la_empresa, 
       titular, 
       recogida = True):
    """
    Recibe el título del documento y la ruta completa del archivo PDF, 
    los datos del cliente en un diccionario, los del albarán también como 
    diccionario, las líneas como lista de listas, los totales como lista 
    y otra lista con la ruta al logotipo como primer elemento y tantas líneas 
    como datos de la empresa se quieran mostrar junto al logo.
    Devuelve uno o dos nombres de ficheros en PDF con el albarán/carta de 
    porte y (opcionalmente) el documento de recogida de envases.
    «titular» es el nombre legal del responsable de la mercancía.
    """
    # CWT: ¡JODER! Lo juro, en el CVS hay una versión de este fichero que era 
    # una joyita y usaba ReportLab/Platypus en todo su esplendor para 
    # construir una más que decente carta de portes. 
    doc = SimpleDocTemplate(ruta_archivo, 
                            title = titulo, 
                            topMargin = 6.00*cm, 
                            bottomMargin = 13.2*cm) 
                            #leftMargin = 1*cm, 
                            #rigthMargin = 1*cm)
    #encabezado = build_encabezado(datos_albaran)
    contenido = build_tabla_contenido(lineas_contenido)
    totales = build_tabla_totales(totales)
    #texto = build_texto()
    story = [#Spacer(1, 1.60 * cm),   # Chispa más o menos los datos de cliente.
             #encabezado, 
             #Spacer(1, 0.15 * cm), 
             contenido, 
             Spacer(1, 0.15 * cm), 
             totales, 
             lastPageNumberFlowable(PAGE_WIDTH - 1.5*cm, 12.7*cm)] 
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
                                                          titular, 
                                                          datos_albaran)
    doc.build(story, 
              onFirstPage = _cabecera_y_cliente, 
              onLaterPages = _cabecera_y_cliente)
    if recogida:
        ruta_archivo_envases = ruta_archivo[::-1].replace(".pdf"[::-1], 
                                                          "_env.pdf"[::-1], 
                                                          1)[::-1] 
        doc2 = SimpleDocTemplate(ruta_archivo_envases, 
                                 title = titulo + " (doc. recogida envases)") 
        mas_texto = build_mas_texto(titular)
        logo_y_empresa = build_marco_logo_y_empresa(datos_de_la_empresa)
        story = [#Última página: más texto genérico y cosas rellenables a mano.
                 #PageBreak(), 
                 logo_y_empresa, 
                 mas_texto, 
                 Spacer(1, 4 * cm), # firmas, 
                 KeepTogether([LineaHorizontal(0.9 * PAGE_WIDTH), 
                               Spacer(1, 0.05 * cm), 
                               LineaHorizontal(0.9 * PAGE_WIDTH)]), 
                 cuadritos_en_ruta(), 
                 Spacer(1, 2*cm), 
                 build_todavia_mas_texto(), 
                ]
        story = utils.aplanar([i for i in story if i])
        doc2.build(story) 
    else:
        ruta_archivo_envases = None
    return ruta_archivo, ruta_archivo_envases

def go_from_albaranSalida(albaranSalida, 
                          kilos = None, 
                          imprimir_recogida = True):
    """
    Construye el PDF a partir de un objeto albaranSalida y no de sus datos 
    sueltos.
    «kilos» es un texto que se imprimirá en el cuadro correspondiente. Si es 
    none intenta calcularlo.
    «imprimir_recogida» es un booleano. Si es False no genera la última página.
    """
    cliente = albaranSalida.cliente
    datos_cliente = {"código": cliente.id,
                     "cif": cliente.cif, 
                     "razón social": cliente.nombre, 
                     "dirección": cliente.direccion, 
                     "población": cliente.ciudad, 
                     "provincia": cliente.provincia}
    if cliente.cp and cliente.cp.strip():
        datos_cliente["población"] = (cliente.cp + " - " 
                                      + datos_cliente["población"])
    if kilos is None:
        try:
            kilos = utils.float2str(
                        sum([ldv.producto.calcular_kilos() * ldv.cantidad  
                             for ldv in albaranSalida.lineasDeVenta]))
        except (TypeError, ValueError):
            kilos = ""
    datos_albaran = {"fecha": utils.str_fecha(albaranSalida.fecha), 
                     "número": albaranSalida.numalbaran, 
                     "kilos": kilos, 
                     "bultos": utils.float2str(
                                sum([ldv.cantidad for ldv 
                                    in albaranSalida.lineasDeVenta]), 
                                autodec = True)}
    iva = cliente.iva
    lineas_contenido = [(ldv.producto.codigo, 
                         ldv.producto.descripcion, 
                         ldv.cantidad, 
                         #ldv.precio * (1.0 - ldv.descuento) * (1 + iva), 
                         # CWT: Ahora prefiere los precios sin IVA.
                         ldv.precio * (1.0 - ldv.descuento), 
                         ldv.pedidoVenta and ldv.pedidoVenta.numpedido or "")
                        for ldv in albaranSalida.lineasDeVenta]
    totales = [albaranSalida.calcular_total(iva_incluido = False), 
               iva,
               albaranSalida.calcular_total(iva_incluido = True)]
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
        titular = dde.nombreContacto
    except IndexError:
        datos_de_la_empresa = [None]
        titular = ""
    nomarchivo = os.path.join(gettempdir(), 
                              "albaranSalida_%s.pdf" % give_me_the_name_baby())
    return go("Albaran de salida - Carta de portes %s (%s)" % (
                albaranSalida.cliente.nombre, 
                utils.str_fecha(albaranSalida.fecha)), 
              nomarchivo, 
              datos_cliente, 
              datos_albaran, 
              lineas_contenido, 
              totales, 
              datos_de_la_empresa, 
              titular, 
              imprimir_recogida)

if __name__ == "__main__":
    try:
        print go_from_albaranSalida(pclases.AlbaranSalida.get(3397))
        raise Exception, "Comentar línea 767 para mostrar datos reales."
    except Exception, msg:
        sys.stderr.write(`msg`)
        datos_cliente = {"código": 123,
                         "cif": "12345678-Z", 
                         "razón social": "Fulanito de tal y pascual, S.L.U.", 
                         "dirección": "Rue del percebe, 13. 4º B", 
                         "población": "Chiquitistán", 
                         "provincia": "Huelva"}
        datos_albaran = {"fecha": "10/06/2008", 
                         "número": "A12314", 
                         "kilos": 123.45, 
                         "bultos": 13}
        lineas_contenido = [
            ("COD1", "Una cosa "*20, 1.234, 1.245, "PEDIDO 1"), 
            ("", "Grñai mama", 1, 1, ""), 
            ("1234567890123", "Otra cosa", 10, 0.33, "123154a")] * 7
        totales = [100.0, 0.16, 116.0]
        datos_de_la_empresa = ["../imagenes/dorsia.png", 
                               "Línea empresa 1", 
                               "Línea empresa 2", 
                               "Línea empresa 3"]
        titular = "Fulanito de tal"
        # Comentar las siguientes líneas para que no salga el ejemplo en blanco:
        datos_cliente = {"código": "",
                         "cif": "", 
                         "razón social": "", 
                         "dirección": "", 
                         "población": "", 
                         "provincia": ""}
        datos_albaran = {"fecha": "", 
                         "número": "", 
                         "kilos": "", 
                         "bultos": ""}
        lineas_contenido = []
        totales = [".", "", ""]
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
            titular = dde.nombreContacto
        except IndexError:
            titular = ""
            datos_de_la_empresa = ["../imagenes/dorsia.png", 
                                   "Línea empresa 1", 
                                   "Línea empresa 2", 
                                   "Línea empresa 3"]
        print go("AlbaranSalida", 
                 "/tmp/albaranSalida.pdf", 
                 datos_cliente, 
                 datos_albaran, 
                 lineas_contenido, 
                 totales, 
                 datos_de_la_empresa, 
                 titular, 
                 True)

