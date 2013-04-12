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

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, \
                               TableStyle, XPreformatted, Preformatted,\
                               PageBreak, KeepTogether, CondPageBreak, Image
from reportlab.platypus.flowables import Flowable
from reportlab.rl_config import defaultPageSize
from reportlab.lib import colors, enums
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet 
import sys, os
from framework import pclases
from formularios import utils
from geninformes import give_me_the_name_baby, escribe, rectangulo, el_encogedor_de_fuentes_de_doraemon, agregarFila
from tempfile import gettempdir
import mx, mx.DateTime

PAGE_HEIGHT = defaultPageSize[1]; PAGE_WIDTH = defaultPageSize[0]
estilos = getSampleStyleSheet()

class LineaHorizontal(Flowable):
    def __init__(self, ancho = None, grosor = 1, offset = 0, 
                 color = colors.black):
        """
        offset es un desplazamiento horizontal respecto al centro de la página 
        al dibujar la línea horizontal. El resto de parámetros es bastante 
        autoexplicativo.
        """
        self.color = color
        self.offset = offset
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
        self.canv.saveState()
        self.canv.setStrokeColor(self.color)
        self.canv.line(orig + self.offset, 
                       .5 * self.line_thickness, 
                       self._width + orig + self.offset, 
                       .5 * self.line_thickness)
        self.canv.restoreState()

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

def cabecera(canvas, datos_de_la_empresa):
    """
    Escribe el texto «CERTIFICADO DE CALIDAD», el logotipo de la empresa, una 
    imagen de geotextiles y un par de rayajos de adorno.
    """
    fuente = "Helvetica-Bold"
    tamanno = 12
    canvas.saveState()
    canvas.setFont(fuente, tamanno)
    canvas.drawCentredString(PAGE_WIDTH / 2.0 + 1*cm, 
                             PAGE_HEIGHT - 2 * cm, 
                             escribe("CERTIFICADO DE CALIDAD"))
    canvas.restoreState()
    rutalogo = datos_de_la_empresa.logo
    if rutalogo:
        rutalogo = os.path.join("..", "imagenes", rutalogo)
        logo = Image(rutalogo)
        logo.drawHeight = 2*cm * logo.drawHeight / logo.drawWidth
        logo.drawWidth = 2*cm
        logo.drawOn(canvas, 2.75*cm, PAGE_HEIGHT - 1*cm - 2*cm)
    # OJO: Foto de geotextiles HARCODED.
    rutafoto = os.path.join("..", "imagenes", "foto_geotextiles.jpg")
    foto = Image(rutafoto)
    foto.drawHeight = 2*cm * foto.drawHeight / foto.drawWidth
    foto.drawWidth = 2*cm
    foto.drawOn(canvas, PAGE_WIDTH - 5*cm, PAGE_HEIGHT - 2.75*cm - 2*cm)
    canvas.saveState()
    canvas.setStrokeColor(colors.green)
    canvas.rect(PAGE_WIDTH - 5*cm, PAGE_HEIGHT - 2.75*cm - 2*cm, 2*cm, 2*cm)
    ## XXX: Esto de ahora es un poco chapuza, y como cambie algún margen se va 
    ## al carajo este trocito de línea que se supone que debería ser parte de 
    ## la sección Denominación.
    canvas.line(PAGE_WIDTH - 5*cm + 2*cm, PAGE_HEIGHT - 3.25*cm, 
                PAGE_WIDTH - 5*cm + 2.25*cm, PAGE_HEIGHT - 3.25*cm)
    ## XXX: EOChapuza
    canvas.restoreState()
    canvas.line(5*cm, PAGE_HEIGHT - 1*cm, # (x1, y1)
                5*cm, PAGE_HEIGHT - 2.5*cm) # (x2, y2)
    canvas.line(PAGE_WIDTH - 3*cm, PAGE_HEIGHT - 1*cm, # (x1, y1)
                PAGE_WIDTH - 3*cm, PAGE_HEIGHT - 2.5*cm) # (x2, y2)
    # En la primera página también debe ir el pie
    pie(canvas, datos_de_la_empresa)

def pie(canvas, datos_de_la_empresa):
    canvas.saveState()
    tamanno = 8 
    fuente = "Times-Bold"
    canvas.setFont(fuente, tamanno)
    canvas.drawString(2*cm, 2.2*cm, escribe(datos_de_la_empresa.nombre.upper()))
    fuente = "Times-Roman"
    canvas.setFont(fuente, tamanno)
    canvas.drawString(2*cm, 1.9*cm, escribe(datos_de_la_empresa.direccion))
    canvas.drawString(2*cm, 1.6*cm, escribe("%s - %s (%s), %s" % (
        datos_de_la_empresa.cp, 
        datos_de_la_empresa.ciudad, 
        datos_de_la_empresa.provincia, 
        datos_de_la_empresa.pais)))
    canvas.drawString(2*cm, 1.3*cm, escribe("Tel.: %s Fax: %s" % (
        datos_de_la_empresa.telefono, 
        datos_de_la_empresa.fax)))
    # FIXME: Está un poco chungaleta esto, pero para no meter más datos en 
    # la tabla ahora mismo y por no perder mucho tiempo con chequeos lo dejo 
    # de momento así hasta que llegue a pruebas.
    canvas.drawString(2*cm, 1*cm, escribe("Web: www.%s Correo-e: %s" % (
        datos_de_la_empresa.email.split("@")[1], 
        datos_de_la_empresa.email)))
    canvas.restoreState()

def build_head2(texto, ancho_linea = PAGE_WIDTH - 5.5*cm, offset_linea = 0.0):
    """
    Devuelve el texto con el estilo de encabezado de 2º. nivel y el subrayado.
    """
    estilo_head2 = ParagraphStyle("Header2", 
                                  parent = estilos["Normal"])
    estilo_head2.fontSize = 14
    estilo_head2.fontName = "Times-Italic"
    estilo_head2.textColor = colors.gray
    texto = Paragraph(escribe(texto), estilo_head2)
    linea = LineaHorizontal(ancho_linea, offset = offset_linea, 
                            color = colors.green)
    return KeepTogether([texto, Spacer(1, 0.1*cm), linea, Spacer(1, 0.15*cm)])

def build_denominacion(producto, albaran):
    head2 = build_head2("1. Denominación", 
                        ancho_linea = PAGE_WIDTH - 7.75 * cm, 
                        offset_linea = -1.12 * cm)
    try:
        factura = albaran.get_facturas()[0] # Si hay varias, la primera.
    except IndexError:
        factura = None
    estilo_denominacion = ParagraphStyle("Estilo denominación", 
                                         parent = estilos["Normal"])
    estilo_denominacion.fontSize = 8
    estilo_denominacion.rightIndent = 2.25*cm
    texto = Paragraph("Certificado de calidad asociado al producto %s "
                      "suministrado con el albarán %s%s." % (
                        producto.descripcion, 
                        albaran.numalbaran, 
                        factura 
                            and " y factura %s" % factura.numfactura 
                            or ""), 
                      estilo_denominacion)
    return head2, texto

def build_texto(datos_de_la_empresa):
    """
    Construye el texto genérico de la carta de portes.
    """
    estilo_texto = ParagraphStyle("Texto", 
                                  parent = estilos["Normal"])
    estilo_texto.alignment = enums.TA_JUSTIFY
    estilo_texto.firstLineIndent = 24
    estilo_texto.fontSize = 8
    estilo_texto.leading = 9
    texto = """Norma UNE EN 13249:2001 y UNE EN 13249:2001/A1:2005, Norma UNE EN 13250:2001 y UNE EN 13250:2001/A1:2005, Norma UNE EN 13251:2001 y UNE EN 13251:2001/A1:2005, Norma UNE EN 13252:2001, UNE EN 13252/Erratum:2002 y UNE EN 13252:2001/A1:2005, Norma UNE EN 13253:2001 y UNE EN 13253:2001/A1:2005, Norma UNE EN 13254:2001, UNE EN 13254/AC:2003 y UNE EN 13254:2001/A1:2005, Norma UNE EN 13255:2001, UNE EN 13255/AC:2003 y UNE EN 13255:2001/A1:2005, Norma UNE EN 13256:2001, UNE EN 13256/AC:2003 y UNE EN 13256:2001/A1:2005,Norma UNE EN 13257:2001, UNE EN 13257/AC:2003 y UNE EN 13257:2001/A1:2005, Norma UNE EN 13265:2001, UNE EN 13265/AC:2003 y UNE EN 13265:2001/A1:2005.

Geotextil no tejido formado por fibras vírgenes <b>100% de polipropileno</b>, unidas mecánicamente por un proceso de agujado con posterior termofijado. Campo de aplicación: en carreteras y otras zonas de tráfico, construcciones ferroviarias, movimientos de tierras, cimentaciones y estructuras de contención, sistemas de drenaje, control de la erosión (protección costera y revestimiento de taludes), construcción de embalses y presas, construcción de canales, construcción de túneles y estructuras subterráneas, vertederos de residuos sólidos, proyectos de contenedores de residuos sólidos.
    """ 
    p = [Paragraph(escribe(t), estilo_texto) for t in texto.split("\n") if t]
    p.insert(1, Spacer(1, 0.25*cm))
    logo_ce = Image(os.path.join("..", "imagenes", "CE.png"))
    logo_ce.drawHeight = 0.75*cm
    logo_ce.drawWidth = 1*cm
    p.insert(0, logo_ce)
    p.insert(1, Spacer(1, 0.15*cm))
    estilo_numero_marcado = ParagraphStyle("NumeroMarcado", 
                                           parent = estilos["Normal"])
    estilo_numero_marcado.alignment = enums.TA_CENTER
    estilo_numero_marcado.fontSize = 7
    estilo_numero_marcado.fontName = "Courier"
    p.insert(2, Paragraph(escribe("9000122-1035"), estilo_numero_marcado))
    estilo_nombre_empresa = ParagraphStyle("NombreEmpresa", 
                                           parent = estilos["Normal"])
    estilo_nombre_empresa.alignment = enums.TA_CENTER
    estilo_nombre_empresa.fontSize = 7
    estilo_nombre_empresa.fontName = "Courier-Bold"
    nombre_empresa = datos_de_la_empresa.nombre
    p.insert(3, Paragraph(escribe(nombre_empresa.upper()), 
                          estilo_nombre_empresa))
    p.insert(4, Spacer(1, 0.15*cm))
    return KeepTogether(p)

def build_marcado(datos_de_la_empresa):
    head2 = build_head2("2. Marcado CE")
    texto = build_texto(datos_de_la_empresa)
    return head2, texto

def build_caracteristicas(dic_valores, orden = None):
    """
    Si recibe una lista de valores en "orden" la seguirá para recorrer los 
    valores a mostrar. En caso contrario el orden es aleatorio.
    """
    head2 = build_head2("3.- Características técnicas")
    if not orden:
        orden = dic_valores.keys()
    # Voy construyendo párrafos para los datos de la tabla.
    datos = [[escribe("Característica"), escribe("Método de ensayo"), 
              escribe("Unidad"),         escribe("Valor")]]
    for caracteristica in orden:
        try:
            datos.append([escribe(dic_valores[caracteristica]["descripción"]), 
                          escribe(dic_valores[caracteristica]['método']), 
                          escribe(dic_valores[caracteristica]['unidad']), 
                          escribe(dic_valores[caracteristica]['valor'])])
        except KeyError:
            if (caracteristica in dic_valores 
                and "valor" in dic_valores[caracteristica]):
                datos.append([escribe(caracteristica), 
                              "", 
                              "", 
                              escribe(dic_valores[caracteristica]['valor'])])
    estilo_centrado = ParagraphStyle("Alineado centrado", 
                                     parent = estilos["Normal"])
    estilo_centrado.alignment = enums.TA_CENTER
    estilo_centrado.textColor = colors.white
    estilo_centrado.fontSize = 8
    estilo_tabla = ParagraphStyle("Estilo tabla", 
                                  parent = estilo_centrado)
    estilo_tabla.alignment = enums.TA_JUSTIFY
    estilo_tabla.textColor = colors.black
    estilo_centrado_negro = ParagraphStyle("Estilo centrado negro", 
                                           parent = estilo_centrado)
    estilo_centrado_negro.textColor = colors.black
    _datos = [[Paragraph(celda, estilo_centrado) for celda in datos[0]]]
    for fila in datos[1:]:
        primera_celda, resto = fila[0], fila[1:]
        _datos.append([Paragraph(primera_celda, estilo_tabla)] 
                      + [Paragraph(celda, estilo_centrado_negro) 
                         for celda in resto])
    _datos.append([Paragraph(escribe("Durabilidad"), estilo_tabla), 
                   [
                       Paragraph(escribe("- A recubrir en el día de la "
                                         "instalación para refuerzos y en dos"
                                         " semanas para otras aplicaciones."), 
                                 estilo_tabla), 
                       Paragraph(escribe("- Durabilidad prevista para un "
                                         "mínimo de 25 años en suelos "
                                         "naturales con 4&lt;pH&lt;9 y una "
                                         "temperatura &lt;25 ºC."), 
                                 estilo_tabla)
                  ], 
                  "", 
                  ""])
    #print len(_datos), len(datos)
    tabla = Table(_datos, 
        style = [("SPAN",       (-3, -1), (-1, -1)), 
                 ("BOX",        ( 0,  0), (-1, -1), 0.50, colors.black), 
                 ("INNERGRID",  ( 0,  0), (-1, -1), 0.50, colors.black), 
                 ("BACKGROUND", ( 0,  0), (-1,  0), colors.green), 
                 ("TEXTCOLOR",  ( 0,  0), (-1,  0), colors.white), 
                 ("VALIGN",     ( 0,  0), (-1, -1), "MIDDLE"), ], 
        colWidths = (PAGE_WIDTH / 3.0, 
                     PAGE_WIDTH / 7.0, 
                     PAGE_WIDTH / 8.0, 
                     PAGE_WIDTH / 8.0))
    return head2, tabla

def build_pie(datos_de_la_empresa):
    estilo_pie = ParagraphStyle("Estilo pie", 
                                parent = estilos["Normal"])
    estilo_pie.alignment = enums.TA_CENTER
    texto_fecha = Paragraph("En %s a %s" % (
                        datos_de_la_empresa.ciudad, 
                        utils.corregir_nombres_fecha(
                          mx.DateTime.localtime().strftime("%d de %B de %Y"))), 
                      estilo_pie)
    tabla_firmas = Table([["Responsable de laboratorio", 
                           "Responsable de calidad"]], 
                         colWidths = (PAGE_WIDTH / 2.0, PAGE_WIDTH / 2.0), 
                         style = [
                            ("FONT", (0, 0), (0, 0), "Times-Roman", 10), 
                            ("ALIGN", (0, 0), (-1, -1), "CENTER"), 
                         ])
    return KeepTogether([texto_fecha, Spacer(1, 1.0*cm), tabla_firmas])

def go(ruta_archivo, producto, dic_valores, datos_de_la_empresa, albaran, 
       orden = None):
    """
    Genera, a partir de los datos recibidos, el PDF del certificado de calidad.
    Solo un producto.

    IN:
        ruta_archivo: Nombre del PDF que se generará.
        producto : Objeto pclases del producto.
        dic_valores: diccionario con las características a mostrar, el 
                     método de ensayo, la unidad y el valor numérico (como 
                     texto).
        albaran: Albarán de salida implicado en el certificado.
        datos_de_la_empresa: Registro de pclases con los datos de la empresa.

    OUT: 
        ruta_archivo: La ruta completa en el dir. temp. del archivo generado.
    """
    ruta_archivo = os.path.join(gettempdir(), ruta_archivo)
    doc = SimpleDocTemplate(ruta_archivo, 
                            title = "CERTIFICADO DE CALIDAD", 
                            topMargin = 2.5*cm, 
                            bottomMargin = 3*cm) 
                            #leftMargin = 1*cm, 
                            #rigthMargin = 1*cm)
    denominacion = build_denominacion(producto, albaran)
    marcado = build_marcado(datos_de_la_empresa)
    caracteristicas = build_caracteristicas(dic_valores, orden)
    pie = build_pie(datos_de_la_empresa)
    story = [denominacion, 
             Spacer(1, 0.30 * cm), 
             marcado, 
             Spacer(1, 0.30 * cm), 
             caracteristicas, 
             Spacer(1, 1.00 * cm), 
             pie]
    story = utils.aplanar([i for i in story if i])
    _encabezado = lambda c, d: cabecera(c, datos_de_la_empresa)
    _pie = lambda c, d: pie(c, datos_de_la_empresa)
    doc.build(story, 
              onFirstPage = _encabezado, 
              onLaterPages = _pie)
    return ruta_archivo

def go_from_albaranSalida(albaranSalida):
    """
    Abre la ventana del certificado de calidad con el albarán recibido.
    """
    os.chdir("../formularios")
    from formularios import certificado_calidad
    v = certificado_calidad.CertificadoCalidad(albaranSalida)

if __name__ == "__main__":
    go_from_albaranSalida(pclases.AlbaranSalida.selectBy(numalbaran="6343")[0])

