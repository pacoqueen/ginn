#!/usr/bin/env python
# -*- coding: utf-8 -*-

from informes.geninformes import give_me_the_name_baby, rectangulo, escribe
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import os
from tempfile import gettempdir
from formularios import utils
import Image
import datetime

# we know some glyphs are missing, suppress warnings
import reportlab.rl_config  # @UnusedImport
reportlab.rl_config.warnOnMissingFontGlyphs = 0
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont, TTFError
try:
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdfmetrics.registerFont(TTFont('VeraB', 'VeraBd.ttf'))
    pdfmetrics.registerFont(TTFont('VeraI', 'VeraIt.ttf'))
    pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))
    pdfmetrics.registerFont(TTFont('Liberation', 'LiberationSans-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('LiberationB', 'LiberationSans-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('LiberationI', 'LiberationSans-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('LiberationBI', 'LiberationSans-BoldItalic.ttf'))
except TTFError:
    pdfmetrics.registerFont(TTFont('Vera', os.path.join("..", "informes", 'Vera.ttf')))
    pdfmetrics.registerFont(TTFont('VeraB', os.path.join("..", "informes", 'VeraBd.ttf')))
    pdfmetrics.registerFont(TTFont('VeraI', os.path.join("..", "informes", 'VeraIt.ttf')))
    pdfmetrics.registerFont(TTFont('VeraBI', os.path.join("..", "informes", 'VeraBI.ttf')))
    pdfmetrics.registerFont(TTFont('Liberation', os.path.join("..", "informes", 'LiberationSans-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('LiberationB', os.path.join("..", "informes", 'LiberationSans-Bold.ttf')))
    pdfmetrics.registerFont(TTFont('LiberationI', os.path.join("..", "informes", 'LiberationSans-Italic.ttf')))
    pdfmetrics.registerFont(TTFont('LiberationBI', os.path.join("..", "informes", 'LiberationSans-BoldItalic.ttf')))



DEBUG = False
mm = cm / 10.0
# Formato 0b solo en python >= 2.6
#try:
#    BOLD, ITALIC, LEFT, CENTER, RIGHT = (0b1, 0b10, 0b100, 0b1000, 0b10000)
#except SyntaxError:
BOLD, ITALIC, LEFT, CENTER, RIGHT = (int('00001', 2), 
                                         int('00010', 2), 
                                         int('00100', 2), 
                                         int('01000', 2), 
                                         int('10000', 2))
FONT = "Liberation"
SIZE = 6


def print_debug(*args, **kw):
    for arg in args:
        print "\tDEBUG->", 
        print arg
    for k in kw:
        print "\tDEBUG->", 
        if isinstance(kw[k], (list, tuple)):
            print('\n\t\t'.join(
                `k`+'[{0}]: {1}'.format(*i) for i in enumerate(kw[k])))
        else:
            print "{0}: {1}".format(k, kw[k])

def etiqueta_rollos_polaco(rollos, mostrar_marcado = True):
    """
    Construye una etiqueta en polaco para Alians Trade.
    """
    # Dimensiones de la etiqueta en impresora térmica GEMINI.
    height = h = 12.55 * cm
    width = w = 8.4 * cm
    MARGEN = 0.05 * cm

    if DEBUG:
        print_debug(height = height, width = width)

    logo_marcado = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                    "..", "imagenes", "CE.png"))
    logo_alians = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                    "..", "imagenes", "alians_trade.png"))
    WM = 1.0 * cm
    WA = 1.5 * cm
    im_width, im_height = Image.open(logo_marcado).size
    WH_MARCADO = (WM, im_height * (WM / im_width))
    im_width, im_height = Image.open(logo_alians).size
    WH_ALIANS = (WA, im_height * (WA / im_width))
    if DEBUG:
        print_debug(WH_MARCADO = WH_MARCADO, WH_ALIANS = WH_ALIANS)
    # Medidas relativas sobre papel.
    H_TEXTMARCADO = 0.2 * cm
    xy_logo = (1.5*mm, h - (WH_MARCADO[1] + H_TEXTMARCADO + WH_ALIANS[1]))
    xy_ce = ((w - WH_MARCADO[0]) / 2, h - WH_MARCADO[1] - 1.5*mm)
    xy_textmarcado = (w/2, xy_logo[1] + WH_ALIANS[1] - H_TEXTMARCADO)
    if DEBUG:
        print_debug(xy_ce = xy_ce, xy_textmarcado = xy_textmarcado, 
                    xy_logo = xy_logo)
    # Datos
    texto_marcado1 = "1488-CPD-0275/Z"
    texto_marcado2 = "12"
    X_HEADER = WH_ALIANS[0] + 0.2*cm
    data = [("PRODUCENT/PRODUCER:", {'x': X_HEADER, 
                                     'format': CENTER}), 
            ("ALIANS TRADE SP. Z O.O.", {'x': X_HEADER, 
                                         'format': BOLD + CENTER}), 
            ("ul. Wyzwolenia 367a, 43-300 Bielsko-Biała", 
                {'x': X_HEADER, 'format': CENTER}), 
            ("www.alians-trade.eu", {'x': X_HEADER, 'format': CENTER}), 
            ("ZAKŁAD PRODUKCYJNY/FACTORY CODE: 34-133", 
                {'x': X_HEADER, 'format': CENTER}), 
            ("NAZWA PRODUKTU/ PRODUCT NAME:", {'format': CENTER}), 
            #("Geowłóknina PINEMA® ST ", {'format': CENTER}), 
            ("$PRODUCTO", {'format': CENTER}), 
                # Geowłóknina PINEMA® ST + Texto variable {80, 100, 180, 250} 
            ("geowłóknina wyprodukowana ze 100% polipropylenu/", 
                {'format': CENTER}), 
            ("nonwoven geotextile composed of 100% polypropilene", 
                {'format': CENTER}), 
            "NORMY/ APPLICATION STANDARDS:", 
            ("EN 13249:2000, EN 13250:2000, EN 13251:2000, EN 13252:2000,", 
                {'format': BOLD}), 
            ("EN 13253:2000, EN 13254:2000, EN 13255:2000, EN 13256:2000,", 
                {'format': BOLD}), 
            ("EN 13257:2000, EN 13265:2000,",    # Negrita
                {'format': BOLD}), 
            # Las siguientes 5 líneas en fuente más pequeña. 
            ("EN 13249:2000/A1:2005, EN 13250:2000/A1:2005, EN 13251:2000/A1:2005,", 
                {'size': SIZE-1}), 
            ("EN 13252:2000/A1:2005, EN 13253:2000/A1:2005, EN 13254:2000/AC:2003,", 
                {'size': SIZE-1}), 
            ("EN 13254:2000/A1:2005, EN 13255:2000/AC:2003, EN 13255:2000/A1:2005,", 
                {'size': SIZE-1}), 
            ("EN 13256:2000/AC:2003,EN 13256:2000/A1:2005, EN 13257:2000/AC:2003,", 
                {'size': SIZE-1}), 
            # Esta última, además de pequeña, en negrita.
            ("EN 13257:2000/A1:2005, EN 13265:2000/AC:2003, EN 13265:2000/A1:2005", 
                {'format': BOLD, 'size': SIZE-1}), 
            "ZASTOSOWANIE/ APPLICATION: w drogownictwie, kolejnictwie, w robotach ", 
            "ziemnych i konstrukcjach oporowych, w systemach drenażowych, w ", 
            "zabezpieczeniach antyerozyjnych, w budowie zbiorników wodnych i zapór, ", 
            "w budowie kanałów, tuneli i konstrukcji podziemnych, w budowie ", 
            "składowisk odpadów stałych i zbiorników odpadów ciekłych.", 
            "PRZEZNACZENIE/ INTENDED FUNCTIONS: rozdzielenie, filtracja, ", 
            "drenaż, wzmocnienie.", 
            # De aquí para abajo, en dos columnas
            (("NR ROLKI/ ", "GRAMATURA/"), 
                {'size': SIZE - 2}), 
            (("ROLL NO.:", "$NUMROLLO", "NOMINAL MASS (g/m2):", "$GRAMAJE"), 
                {'format': ITALIC, 'size': SIZE - 2}),
            (("DŁUGOŚĆ/", "SZEROKOŚĆ/"), 
                {'size': SIZE - 2}), 
            (("LENGHT (m):", "$LARGO", "WIDTH (m):", "$ANCHO"), 
                {'format': ITALIC, 'size': SIZE - 2}), 
            (("WAGA BRUTTO/", "DATA PRODUKCJI/"), 
                {'size': SIZE - 2}), 
            (("GROSS WEIGHT (kg):", "$PESO", "DATE OF PRODUCTION:", "$FECHA"), 
                {'format': ITALIC, 'size': SIZE - 2})
           ]

    # 31 líneas. En principio distribuyo uniformemente:
    alto_linea = (xy_textmarcado[1] - 2*H_TEXTMARCADO) / (len(data) + 1)
    # (0,0) está abajo. Yo relleno la etiqueta de arriba a abajo.
    y_lines = [(xy_textmarcado[1] - 2*H_TEXTMARCADO) - (y * alto_linea) 
                for y in range(len(data) +1)[1:]]
    if DEBUG:
        print_debug(y_lines = y_lines)
        print_debug(alto_linea = alto_linea)

    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
        "etiqAliansT_%s.pdf" % give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo, pagesize = (width, height))
    
    # import code; code.interact(local = locals())

    for rollo in rollos:
        # Elementos gráficos: borde etiqueta y logos.
        rectangulo(c, (MARGEN, MARGEN),
                      (width - MARGEN, height - MARGEN))
        c.drawImage(logo_alians, xy_logo[0], xy_logo[1], 
                    WH_ALIANS[0], WH_ALIANS[1])
        if mostrar_marcado and not rollo['defectuoso']:
            c.drawImage(logo_marcado, 
                        xy_ce[0], xy_ce[1],  
                        width = WH_MARCADO[0], 
                        height = WH_MARCADO[1])
            c.setFont("Helvetica-Bold", SIZE)
            c.drawCentredString(xy_textmarcado[0], 
                                xy_textmarcado[1], 
                                escribe(texto_marcado1))
            c.drawCentredString(xy_textmarcado[0], 
                                xy_textmarcado[1] - H_TEXTMARCADO, 
                                escribe(texto_marcado2))
            c.setFont(FONT, SIZE)
        # Texto de la etiqueta
        c.setFont(FONT, SIZE)
        for i in range(len(data)):
            #c.drawString(0, y_lines[i], escribe(data[i]))
            #c.drawString(2*mm, y_lines[i], data[i])
            if isinstance(data[i], (list, tuple)):
                texto = data[i][0]
                opciones = data[i][1]
                if not isinstance(opciones, dict):
                    texto = (texto, opciones)
            else:
                texto = data[i]
                opciones = {}
            render(c, 2*mm, y_lines[i], texto, opciones = opciones, 
                   fuente = FONT, tamanno = SIZE, w = w, h = h, 
                   margen = MARGEN, rollo = rollo)
        c.showPage()
    c.save()
    return nomarchivo

def render(c, x, y, texto = "", opciones = {}, fuente = "Liberation", 
           tamanno = 6, w = 8.4*cm, h = 12.55*cm, margen = 0.05*cm, 
           rollo = None):
    """Escribe en el PDF el texto en la posición (x, y) con la fuente, tamaño 
    y opciones correspondientes aplicadas.

    :c: Canvas donde escribir el texto.
    :x: Posición X del texto.
    :y: Posición Y del texto.
    :texto: Texto a escribir en el PDF.
    :opciones: Diccionario de opciones a aplicar antes de escribir el texto.
    :fuente: Fuente por defecto si no se especifica otra en las opciones.
    :tamanno: Tamaño inicial de la fuente si no se especifica otra.

    """
    if isinstance(texto, (list, tuple)):  # Tantas columnas como ítems
        textos = texto
    else:
        textos = (texto, )
    ncols = len(textos)
    offset_x = (w - x - margen) / ncols
    for texto in textos:
        fuente, tamanno = FONT, SIZE
        posx = x + (offset_x * textos.index(texto))
        texto, fuente, tamanno, dinamico = extract_texto(
                texto, fuente, tamanno, rollo)
        for o in opciones:
            if o == "size" and not dinamico:
                tamanno = opciones['size']
            elif o == "x":
                posx = opciones[o]
            elif o == "format": 
                formato = opciones[o]
                if formato & CENTER: # Centrado "manual" suponiendo que 
                    # lo hago entre la X indicada y el borde derecho.
                    posx = x + (w - x - margen) / 2
                    ancho_texto = c.stringWidth(texto, fuente, tamanno)
                    if DEBUG:
                        print_debug(texto, ancho_texto = ancho_texto)
                    posx -= ancho_texto / 2 
                if formato & BOLD and not fuente.endswith("B") and not dinamico:
                    fuente += "B"
                if (formato & ITALIC and not fuente.endswith("I") 
                        and not dinamico): # Esto es una chapuza... :(
                    # Sería mejor que el extract_text devolviera también el 
                    # formato y no andar así. Pero cuando no hay tiempo se 
                    # tira de flags. Qué remedio.
                    fuente += "I"
        c.saveState()
        c.setFont(fuente, tamanno)
        #######################################################################
        # TODO: HARCODED: Caso especial. Si gramaje 180 o más, hay que añadir 
        # la palabra "ochrona" a una de las líneas.
        try:
            cer = rollo['objeto'].productoVenta.camposEspecificosRollo
            gramos = cer.gramos
        except:
            gramos = 180
        if "wzmocnienie" in texto and gramos >= 180:
            texto = texto[:-1] + ", ochrona."
        #######################################################################
        c.drawString(posx, y, texto)
        c.restoreState()

def extract_texto(texto, fuente, tamanno, rollo):
    """Extrae la información relativa al producto.

    :texto: Texto a analizar
    :returns: Texto corregido con la información que corresponda (fecha, 
              nombre del producto, número de rollo...), fuente y tamaño.
              Devuelve también un flag si no era texto "estático" y se ha 
              modificado aquí.

    """
    if texto.startswith("$"):
        tamanno += 2
        fuente = "VeraB" 
        try:
            nombre_producto = rollo['objeto'].productoVenta.nombre
            numrollo = rollo['objeto'].numrollo
            cer = rollo['objeto'].productoVenta.camposEspecificosRollo
            peso = rollo['objeto'].peso
            try:
                fecha = rollo['objeto'].articulo.parteDeProduccion.fecha
            except AttributeError:
                fecha = datetime.date.today()
            gramos = cer.gramos
            metrosLineales = cer.metrosLineales
            ancho = cer.ancho
        except AttributeError: 
            # No registro creado todavía. Objeto es None.
            nombre_producto = rollo['productoVenta'].nombre
            numrollo = rollo['nrollo']
            cer = rollo['productoVenta'].camposEspecificosRollo
            peso = cer.pesoTeorico
            fecha = datetime.date.today()
            gramos = cer.gramos
            metrosLineales = cer.metrosLineales
            ancho = cer.ancho
        except TypeError:
            # El propio rollo es None. Datos de prueba.
            nombre_producto = "NOMBRE DEL PRODUCTO"
            numrollo = 123456
            cer = None 
            peso = 0.0
            fecha = datetime.date.today()
            gramos = 1.23
            metrosLineales = 123
            ancho = 4.5
        if texto == "$PRODUCTO": 
            texto = nombre_producto
        elif texto == "$NUMROLLO":
            texto = utils.float2str(numrollo, autodec = True)
        elif texto == "$GRAMAJE":
            texto = `gramos` + "±2.18%"
        elif texto == "$LARGO": 
            texto = utils.float2str(metrosLineales, autodec = True, 
                                    separador_decimales = ".")
        elif texto == "$ANCHO": 
            texto = utils.float2str(ancho,
                                    separador_decimales = ".")
        elif texto == "$PESO": 
            texto = utils.float2str(peso, 
                                    separador_decimales = ".")
        elif texto == "$FECHA": 
            texto = utils.str_fecha(fecha)
        dinamico = True
    else:
        dinamico = False
    return texto, fuente, tamanno, dinamico


if __name__ == "__main__":
    from formularios.reports import abrir_pdf
    from framework import pclases
    from formularios.partes_de_fabricacion_rollos import build_etiqueta
    rollos = []
    for pv in pclases.ProductoVenta.select(
            pclases.ProductoVenta.q.nombre.contains("PINEMA")):
        while len(rollos) <= 2:
            for a in pv.articulos:
                rollos.append(a.rollo)
                if len(rollos) > 2:
                    break
    if not rollos:
        rollos = [pclases.Rollo.select(orderBy = "-id")[0]]
        pv = rollos[0].productoVenta
        rollos.append(pv.articulos[-1].rollo)
    rollos = [build_etiqueta(r)[0] for r in rollos]
    abrir_pdf(etiqueta_rollos_polaco(rollos, mostrar_marcado = True))
