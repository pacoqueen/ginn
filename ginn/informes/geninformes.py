#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008 Francisco José Rodríguez Bogado,                    #
#                          Diego Muñoz Escalante.                             #
# (pacoqueen@users.sourceforge.net, escalant3@users.sourceforge.net)          #
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


# Usando ReportLab como herramienta para la generación de informes
# en GeotexINN.



############## DONE-LIST #############################
# 27 - XI - 2005
# A parte de hacer todos los informes que quedan. Hay varios
# puntos que tenemos que comentar y arreglar:
# + DONE: Codificación de caracteres para correcta visualización de
# + DONE: Nombre de cliente salta una excepción por excesiva recursividad
# - ¿DONE?: Tratamiento de informes de varias página, sólo aproximación
#           momentánea
# + Dejar más espacio para cantidad en facturas y quitar de precio unitario.
# 19 - VII - 2005
# + DONE: Crear los PDF en el temporal del usuario (ver import tempfile)
# + Hacer las facturas de abono con el mismo diseño que las facturas normales.
# + Buscar función para poner título a los PDF que genero (todos tienen
#   "untitled", que es el valor por defecto de ReportLab).
########################################################



from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch, cm
import mx.DateTime

import sys, os
from framework import pclases
from formularios import utils
import time
from tempfile import gettempdir
import Image
import re

# Un par de fuentes TrueType con soporte casi completo para UTF-8.
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
    pdfmetrics.registerFont(TTFont('Vera', os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "..", "informes", 'Vera.ttf')))
    pdfmetrics.registerFont(TTFont('VeraB', os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "..", "informes", 'VeraBd.ttf')))
    pdfmetrics.registerFont(TTFont('VeraI', os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "..", "informes", 'VeraIt.ttf')))
    pdfmetrics.registerFont(TTFont('VeraBI', os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "..", "informes", 'VeraBI.ttf')))
    pdfmetrics.registerFont(TTFont('Liberation', os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "..", "informes", 'LiberationSans-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('LiberationB', os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "..", "informes", 'LiberationSans-Bold.ttf')))
    pdfmetrics.registerFont(TTFont('LiberationI', os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "..", "informes", 'LiberationSans-Italic.ttf')))
    pdfmetrics.registerFont(TTFont('LiberationBI', os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "..", "informes", 'LiberationSans-BoldItalic.ttf')))


# Medidas fundamentales
# Ancho y alto
global width, height, tm , bm, lm, rm, linea
width, height = A4
MAXLINEAS = 47 #47 es el numero correcto
MAXLINAB = 28
# Márgenes (Considero el margen superior lo que está por debajo del
# encabezamiento.)
tm, bm, lm, rm = (680, 56.69, 28.35, 566.92)

def apaisar(apaisar = True):
    global width, height, rm, tm, MAXLINEAS # ¿Por qué globales? ¡¿POR QUÉ?!
                                            # Repito: ¡¡¡¡¡¡ POR QUÉ !!!!!!!
    if apaisar:
        width, height = landscape(A4)
        rm = width - 0.5 * cm
        tm = height - 5.8 * cm      # Por probar con algo de margen
        MAXLINEAS = 30              # Por poner algo, pero que sepas que esto
                                    # NO ES CORRECTO. El número de líneas no
                                    # es fijo.
    else:
        width, height = A4
        rm = 566.92
        tm = 680
        MAXLINEAS = 47  # Por poner algo, pero que sepas que esto
                        # NO ES CORRECTO. El número de líneas no es fijo.
    return rm, tm, width, height, MAXLINEAS

def cursiva(c,              # Canvas
            x,              # Posición X
            y,              # Posición y,
            text,           # Texto a escribir
            fontName,       # Fuente
            fontSize,       # Tamaño
            fillColor,      # Color
            skewAngle,      # Ángulo de inclinación
           ):
    from reportlab.graphics.shapes import skewX

    skewMatrix = skewX(skewAngle)
    c.saveState()
    c.setFillColor(fillColor)
    c.setFont(fontName, fontSize)
    for t in text:
        c.saveState()
        c.translate(x, y)
        c.transform(*skewMatrix)
        c.drawString(0, 0, t)
        c.restoreState()
        x += c.stringWidth(t, fontName, fontSize)
    c.restoreState()

def give_me_the_name_baby():
    return time.strftime("%Y%m%d%H%M%S")

def escribe(cadena_original, limite = None):
    """
    Dada una cadena la convierte a un formato en el que
    ReportLab es capaz de escribir tildes.
    """
    # TODO: ¿Límite? ¿Por qué y para qué recibe "limite"?
    cadena = str(cadena_original)
    if (reportlab.__version__
        != ' $Id: geninformes.py,v 1.496 2012/02/06 09:13:05 pacoqueen Exp $ '
        and '2877 2006-05-18 15:11:23Z andy ' not in reportlab.__version__):
        # Compruebo la versión porque la de la máquina de desarrollo SÍ
        # soporta UTF y falla con cp1252.
        try:
            cadena = cadena.encode('cp1252')
        except Exception, msg:
            print 'geninformes.py (escribe): No se pudo cambiar codificación '\
                  'de cadena "%s". Mensaje de la excepción: %s' % (cadena, msg)
            try:
                cadena = cadena.decode("utf-8", "ignore").encode("cp1252")
            except Exception, msg:
                print 'geninformes.py (escribe): No se pudo decodificar de '\
                      'UTF-8 la cadena "%s". Mensaje de la excepción: %s' % (
                        cadena, msg)
                try:
                    cadena = cambiar_tildes(cadena)
                except Exception, msg:
                    print 'geninformes.py (escribe): No se pudieron sustituir'\
                          ' los acentos gráficos de "%s". Mensaje de la '\
                          'excepción: %s' % (cadena, msg)
                    cadena = ''
    # TODO: No activar hasta que pruebe que funciona en producción. Sin esto
    # la única máquina que da problemas con la codificación es el Windows XP
    # del VirtualBox en la Debian de nostromo.
    try:
        canvas_tmp = canvas.Canvas(os.path.join(gettempdir(), "tmp.pdf"))
        ancho = canvas_tmp.stringWidth(cadena, "Helvetica", 10)  # @UnusedVariable
    except UnicodeDecodeError:
        cadena = cadena_original
    return cadena

def cambiar_tildes(cadena):
    """
    Cambia las tildes de la cadena con caracteres sin tilde.
    """
    res = cadena
    dic = {'á': 'a',
           'Á': 'A',
           'é': 'e',
           'É': 'E',
           'í': 'i',
           'Í': 'I',
           'ó': 'o',
           'Ó': 'O',
           'ú': 'u',
           'Ú': 'U'}
    for con_tilde in dic:
        res = res.replace(con_tilde, dic[con_tilde])
    return res

def cambiar_caracteres_problematicos(cadena):
    cadena = cambiar_tildes(cadena)
    for mala, buena in (("ñ", "nn"), ("Ñ", "NN"), 
                        ("ü", "u"), ("Ü", "U"), 
                        ("ç", "c"), ("Ç", "C"), 
                        ("(", ""), (")", ""), 
                        ("'", "")):
        cadena = cadena.replace(mala, buena)
    return cadena

def sigLinea(valor = 15, actual = None):
    if actual == None:
        actual = linea
    return actual - valor

def primLinea():
    return tm - 15

def hello(c):
    # Uso la pulgada como medida standard para los márgenes. (Oh, sí, qué gran
    # idea, usar la pulgada. Pensar en centímetros, medir en centímetros...
    # pero usar la pulgada. Ganas de matar aumentando.)
    c.drawString(0 + inch, height - inch , escribe('Hola holita, vecinito.'))

def cabecera(c, texto, fecha = None, apaisado = False):
    """
    Dibuja la cabecera del informe
    """
    datos_empresa = pclases.DatosDeLaEmpresa.select()[0]

    global lm, rm, bm, tm, width, height
    if apaisado:
        rm, tm, width, height, MAXLINEAS = apaisar()
    else:
        rm, tm, width, height, MAXLINEAS = apaisar(False)

    xIzquierda = lm -4
    rectangulo(c, (xIzquierda, tm+2*inch), (rm, bm-0.2*inch))
    c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', datos_empresa.logo),
                lm+0.1*inch, height - 1*inch, 0.7*inch, 0.7*inch)
    c.setFont("Helvetica", 20)

    el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 20, lm+inch, rm,
                                        height-0.75*inch, texto, alineacion=0)
    #c.drawString(lm+inch, height-0.75*inch, escribe(texto))
    c.line(xIzquierda, height-inch, rm, height-inch)
    c.setFont("Helvetica", 10)
    if fecha:
        xFecha = rm - 5
        yFecha = tm + 1.8*inch
        c.drawRightString(xFecha, yFecha, escribe(fecha))

def pie(c, actualPagina, totalPagina, apaisado = False):
    """
    Pone el número de página y una línea en el pie
    """
    global width, height, rm, tm

    if apaisado:
        rm, tm, width, height, MAXLINEAS = apaisar()
    else:
        rm, tm, width, height, MAXLINEAS = apaisar(False)

    x = width / 2
    linea = bm - 0.6*inch
    #c.line(lm, linea, rm, linea)
    c.setFont('Times-Italic', 12)
    # TODO: Esto hay que corregirlo tarde o temprano. De momento corrijo las
    # últimas páginas al vuelo para que no quede "Página 7 de 4". Al menos que
    # ponga "7 de 7" aunque al final sean 8.
    if actualPagina > totalPagina:
        totalPagina = actualPagina
    label = "Página %d de %d" % (actualPagina, totalPagina)
    c.drawCentredString(x, linea, escribe(label))

def existencias_no_nulas(hasta = None, exportar_a_csv_a = None, 
                         ventana_padre = None):
    """
    Imprime un informe de existencias al día actual si "hasta" es None
    o hasta la fecha indicada.
    Esta función deja obsoleta a la anterior, que ahora se llama _existencias.
    Si ventana_padre viene instanciado se muestra un diálogo de progreso 
    modal hijo de la ventana "padre_dialogo".
    """
    if ventana_padre:
        from formularios.ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = ventana_padre)
        vpro.mostrar()
        vpro.set_valor(0.0, "Inicializando...")
    if hasta == None:
        nomarchivo = os.path.join(gettempdir(),
                        "existencias_no_nulas_%s.pdf"%give_me_the_name_baby())
        fecha = None
        fecha_limite = " - %s, %s" % (
            utils.str_fecha(mx.DateTime.localtime()), time.strftime("%H:%M"))
    else:
        nomarchivo = os.path.join(gettempdir(),
            "existencias_no_nulas_a_%s_%s.pdf" % (
                hasta.strftime("%Y_%m_%d"),
                give_me_the_name_baby()))
        fecha = utils.str_fecha(hasta)
        fecha_limite = " a %s" % (utils.str_fecha(hasta))
    titulo = 'Inventario de materiales (existencias no nulas) %s' % (
                fecha_limite)
    campos = [('Descripción', 22),
              ('Mínimo', 7),
              ('Stock', 7),
              ('Valoración', 8),
              ('Pedidos pendientes', 17),
              ('unidades', 6),      # Stock inicial
              ('euros', 7),
              ('unidades', 6),      # Entradas
              ('euros', 7),
              ('unidades', 6),      # Salidas
              ('euros', 7),
             ]
    datos = []
    productos = pclases.ProductoCompra.select(pclases.AND(
                        pclases.ProductoCompra.q.controlExistencias == True,
                        pclases.ProductoCompra.q.obsoleto == False, 
                        pclases.ProductoCompra.q.existencias != 0),
                    orderBy = "descripcion")
    total_valoracion = 0
    total_pendiente = 0
    total_inicial = 0
    total_entradas = 0
    total_salidas = 0
    i = 0.0
    total = productos.count()
    tiempos = []
    for p in productos:
        i += 1
        if ventana_padre or pclases.VERBOSE:
            tiempo = time.time()
            txt_info = "%d/%d (%d %%)..." % (i, total, 100.0 * i / total)
            if ventana_padre:
                vpro.set_valor(i / total, txt_info)
            if pclases.VERBOSE:
                print txt_info,
                sys.stdout.flush()
        existencias, valoracion, existencias_1_enero, stock_entradas, \
        valoracion_entradas, stock_salidas, valoracion_salidas, \
        pedidos_pendientes = buscar_datos_existencias(p, hasta)
        if ventana_padre or pclases.VERBOSE:
            tiempo = time.time() - tiempo
            tiempos.append(tiempo)
            eta = (total - i) * (sum(tiempos) / len(tiempos))
            txt_info2 = "%.2f segundos. "\
                      "Tiempo restante estimado en minutos: %d'%02d\"" % (
                        tiempo, eta / 60, eta % 60)
            if ventana_padre:
                vpro.set_valor(i / total, txt_info + " " + txt_info2)
            if pclases.VERBOSE:
                print txt_info2

        ## XXX: DEBUG: PLAN: Esto debería ir en una función aparte de pclases
        # para ejecutarla de vez en cuando y corregir existencias que
        # hayan podido ser "manipuladas" y estén mal -en el sentido de que son
        # incoherentes-.
        #quiero_cambiar_las_existencias_palabrita_de_baden_powell = False
        #if existencias != existencias_1_enero+stock_entradas-stock_salidas:
        #    diff = (existencias_1_enero + stock_entradas -
        #              stock_salidas) - existencias
        #    try:
        #        porcentaje = diff * 100.0 / existencias
        #    except ZeroDivisionError:
        #        porcentaje = 100
        #    if abs(porcentaje) >= 0.1:
        #        print "¡TATE!", diff, "(%.2f%%)" % (porcentaje), \
        #           p.descripcion, existencias, existencias_1_enero, \
        #           stock_entradas, stock_salidas
        #    if (abs(porcentaje) >= 0.1 and
        #        quiero_cambiar_las_existencias_palabrita_de_baden_powell):
        #        p.existencias = (existencias_1_enero + stock_entradas
        #                           - stock_salidas)
        #        p.sync()
        #else:
        #    p.descripcion, "está OK."
        ## XXX: EODEBUG

        total_entradas += valoracion_entradas
        total_salidas += valoracion_salidas
        if valoracion != None:
            str_valoracion = "%s €" % (utils.float2str(valoracion))
            total_valoracion += valoracion
            valoracion_inicial = (existencias_1_enero
                                    * p.get_precio_valoracion())
            total_inicial += valoracion_inicial
            str_valoracion_inicial = "%s €" % (
                utils.float2str(valoracion_inicial))
        else:
            str_valoracion = "N/D"
            str_valoracion_inicial = "N/D"
        if len(pedidos_pendientes) > 0:
            pedido = pedidos_pendientes.keys()[0]
            primer_pedido = "%s: %s %s (%s €)" % (pedido.numpedido,
                utils.float2str(pedidos_pendientes[pedido]['cantidad']),
                p.unidad,
                utils.float2str(pedidos_pendientes[pedido]['valor']))
            total_pendiente += pedidos_pendientes[pedido]['valor']
        else:
            primer_pedido = ""
        datos.append((p.descripcion,
            "%s %s" % (utils.float2str(p.minimo), p.unidad),
            "%s %s" % (utils.float2str(existencias), p.unidad),
            str_valoracion,
            primer_pedido,
            "%s %s" % (utils.float2str(existencias_1_enero), p.unidad),
            str_valoracion_inicial, # Al mismo precio que la valoración actual
            "%s %s" % (utils.float2str(stock_entradas), p.unidad),
            "%s €" % (utils.float2str(valoracion_entradas)),
            "%s %s" % (utils.float2str(stock_salidas), p.unidad),
            "%s €" % (utils.float2str(valoracion_salidas))
            ))
        total_pendiente_del_producto_cantidad = 0
        total_pendiente_del_producto_valor = 0
        for pedido in pedidos_pendientes.keys()[1:]:
            datos.append(("",
                          "",
                          "",
                          "",
                          "%s: %s %s (%s €)" % (pedido.numpedido,
                    utils.float2str(pedidos_pendientes[pedido]['cantidad']),
                    p.unidad,
                    utils.float2str(pedidos_pendientes[pedido]['valor'])),
                          "",
                          "",
                          "",
                          "",
                          "",
                          ""))
            total_pendiente += pedidos_pendientes[pedido]['valor']
            total_pendiente_del_producto_cantidad \
                += pedidos_pendientes[pedido]['cantidad']
            total_pendiente_del_producto_valor \
                += pedidos_pendientes[pedido]['valor']
        if len(pedidos_pendientes) > 1:
            datos.append(("",
                          "",
                          "",
                          "",
                          "Total pendiente: %s %s (%s €)" % (
                    utils.float2str(total_pendiente_del_producto_cantidad),
                    p.unidad,
                    utils.float2str(total_pendiente_del_producto_valor)),
                          "",
                          "",
                          "",
                          "",
                          "",
                          ""))
    datos.append(("", "---", "---", "---", "---", "---",
                  "---", "---", "---", "---", "---"))
    datos.append((" " * 20 + "TOTAL: ",
                  "",
                  "",
                  "%s €" % (utils.float2str(total_valoracion)),
                  "%s €" % (utils.float2str(total_pendiente)),
                  "",
                  "%s €" % (utils.float2str(total_inicial)),
                  "",
                  "%s €" % (utils.float2str(total_entradas)),
                  "",
                  "%s €" % (utils.float2str(total_salidas)),
                  ))
    generated_files = imprimir2(archivo = nomarchivo,
                     titulo = titulo,
                     campos = campos,
                     datos = datos,
                     fecha = fecha,
                     cols_a_derecha = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
                     graficos = [],
                     apaisado = True,
                     sobrecampos = (("Stock inicial", 71 - 3),
                                    ("Entradas", 84 - 3),
                                    ("Salidas", 96 -3)),
                     lineas_verticales = ((61, True),
                                          (61 + 6 + 7, True),
                                          (61 + 2 * (6 + 7), True),
                                          (22, True),
                                          (22 + 7 + 7 + 8, True), ),
                     exportar_a_csv_a = exportar_a_csv_a)
    vpro.ocultar()
    return generated_files

def existencias(hasta = None, exportar_a_csv_a = None, ventana_padre = None):
    """
    Imprime un informe de existencias al día actual si "hasta" es None
    o hasta la fecha indicada.
    Esta función deja obsoleta a la anterior, que ahora se llama _existencias.
    Si se recibe "padre" se mostrará una ventana de progreso modal hija de la 
    ventana padre que se indica.
    """
    if hasta == None:
        nomarchivo = os.path.join(gettempdir(),
                                "existencias_%s.pdf" % give_me_the_name_baby())
        fecha = None
        fecha_limite = " - %s, %s" % (utils.str_fecha(mx.DateTime.localtime()),
                                      time.strftime("%H:%M"))
    else:
        nomarchivo = os.path.join(gettempdir(), "existencias_a_%s_%s.pdf" % (
            hasta.strftime("%Y_%m_%d"), give_me_the_name_baby()))
        fecha = utils.str_fecha(hasta)
        fecha_limite = " a %s" % (utils.str_fecha(hasta))
    titulo = 'Inventario de materiales%s' % (fecha_limite)
    campos = [('Descripción', 22),
              ('Mínimo', 7),
              ('Stock', 7),
              ('Valoración', 8),
              ('Pedidos pendientes', 17),
              ('unidades', 6),      # Stock inicial
              ('euros', 7),
              ('unidades', 6),      # Entradas
              ('euros', 7),
              ('unidades', 6),      # Salidas
              ('euros', 7),
             ]
    datos = []
    productos = pclases.ProductoCompra.select(pclases.AND(
            pclases.ProductoCompra.q.controlExistencias == True,
            pclases.ProductoCompra.q.obsoleto == False), 
        orderBy = "descripcion")
    total_valoracion = 0
    total_pendiente = 0
    total_inicial = 0
    total_entradas = 0
    total_salidas = 0
    if pclases.DEBUG or ventana_padre:
        i = 0.0
        tot = productos.count()
    if ventana_padre:
        from formularios.ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = ventana_padre)
        vpro.mostrar()
        vpro.set_valor(0.0, "Procesando...")
    for p in productos:
        if pclases.DEBUG or ventana_padre:
            i += 1
        if pclases.DEBUG:
            try:
                print "[{0:>6.2%}]".format(i/tot),
                print "{i:.0f} de {tot:.0f}\t|".format(**locals()), 
            except SyntaxError: #Python 2.5. Don't bother, man!
                print "[%.2f]" % (i/tot),
                print "%.0f de %.0f\t|" % (i, tot), 
            print p.get_puid(), p.descripcion
        if ventana_padre:
            vpro.set_valor(i/tot, "Procesando %s...\t[%s]" % (p.descripcion, 
                                                              p.get_puid()))
        existencias, valoracion, existencias_1_enero, stock_entradas\
            , valoracion_entradas, stock_salidas, valoracion_salidas\
            , pedidos_pendientes = buscar_datos_existencias(p, hasta)

        ## XXX: DEBUG: PLAN: Esto debería ir en una función aparte de pclases
        # para ejecutarla de vez en cuando y corregir existencias que
        # hayan podido ser "manipuladas" y estén mal -en el sentido de que son
        # incoherentes-.
        #quiero_cambiar_las_existencias_palabrita_de_baden_powell = False
        #if existencias != existencias_1_enero+stock_entradas-stock_salidas:
        #    diff = (existencias_1_enero + stock_entradas
        #               - stock_salidas) - existencias
        #    try:
        #        porcentaje = diff * 100.0 / existencias
        #    except ZeroDivisionError:
        #        porcentaje = 100
        #    if abs(porcentaje) >= 0.1:
        #        print "¡TATE!", diff, "(%.2f%%)" % (porcentaje), \
        # p.descripcion, existencias, existencias_1_enero, stock_entradas\
        # , stock_salidas
        #    if (abs(porcentaje) >= 0.1 and
        #        quiero_cambiar_las_existencias_palabrita_de_baden_powell):
        #        p.existencias = (existencias_1_enero + stock_entradas
        #                           - stock_salidas)
        #        p.sync()
        #else:
        #    p.descripcion, "está OK."
        ## XXX: EODEBUG

        total_entradas += valoracion_entradas
        total_salidas += valoracion_salidas
        if valoracion != None:
            str_valoracion = "%s €" % (utils.float2str(valoracion))
            total_valoracion += valoracion
            valoracion_inicial = existencias_1_enero*p.get_precio_valoracion()
            total_inicial += valoracion_inicial
            str_valoracion_inicial="%s €"%(utils.float2str(valoracion_inicial))
        else:
            str_valoracion = "N/D"
            str_valoracion_inicial = "N/D"
        if len(pedidos_pendientes) > 0:
            pedido = pedidos_pendientes.keys()[0]
            primer_pedido = "%s: %s %s (%s €)" % (pedido.numpedido,
                utils.float2str(pedidos_pendientes[pedido]['cantidad']),
                p.unidad,
                utils.float2str(pedidos_pendientes[pedido]['valor']))
            total_pendiente += pedidos_pendientes[pedido]['valor']
        else:
            primer_pedido = ""
        datos.append((p.descripcion,
                      "%s %s" % (utils.float2str(p.minimo), p.unidad),
                      "%s %s" % (utils.float2str(existencias), p.unidad),
                      str_valoracion,
                      primer_pedido,
                      "%s %s" % (utils.float2str(existencias_1_enero),
                                 p.unidad),
                      str_valoracion_inicial,
                        # Al mismo precio que la valoración actual
                      "%s %s" % (utils.float2str(stock_entradas), p.unidad),
                      "%s €" % (utils.float2str(valoracion_entradas)),
                      "%s %s" % (utils.float2str(stock_salidas), p.unidad),
                      "%s €" % (utils.float2str(valoracion_salidas))
                    ))
        total_pendiente_del_producto_cantidad = 0
        total_pendiente_del_producto_valor = 0
        for pedido in pedidos_pendientes.keys()[1:]:
            datos.append(("",
                          "",
                          "",
                          "",
                          "%s: %s %s (%s €)" % (pedido.numpedido,
                    utils.float2str(pedidos_pendientes[pedido]['cantidad']),
                    p.unidad,
                    utils.float2str(pedidos_pendientes[pedido]['valor'])),
                          "",
                          "",
                          "",
                          "",
                          "",
                          ""))
            total_pendiente += pedidos_pendientes[pedido]['valor']
            total_pendiente_del_producto_cantidad \
                += pedidos_pendientes[pedido]['cantidad']
            total_pendiente_del_producto_valor \
                += pedidos_pendientes[pedido]['valor']
        if len(pedidos_pendientes) > 1:
            datos.append(("",
                          "",
                          "",
                          "",
                          "Total pendiente: %s %s (%s €)" % (
                    utils.float2str(total_pendiente_del_producto_cantidad),
                    p.unidad,
                    utils.float2str(total_pendiente_del_producto_valor)),
                          "",
                          "",
                          "",
                          "",
                          "",
                          ""))
    datos.append(("", "---", "---", "---", "---", "---",
                  "---", "---", "---", "---", "---"))
    datos.append((" " * 20 + "TOTAL: ",
                  "",
                  "",
                  "%s €" % (utils.float2str(total_valoracion)),
                  "%s €" % (utils.float2str(total_pendiente)),
                  "",
                  "%s €" % (utils.float2str(total_inicial)),
                  "",
                  "%s €" % (utils.float2str(total_entradas)),
                  "",
                  "%s €" % (utils.float2str(total_salidas)),
                  ))
    vpro.ocultar()
    return imprimir2(archivo = nomarchivo,
                     titulo = titulo,
                     campos = campos,
                     datos = datos,
                     fecha = fecha,
                     cols_a_derecha = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
                     graficos = [],
                     apaisado = True,
                     sobrecampos = (("Stock inicial", 71 - 3),
                                    ("Entradas", 84 - 3),
                                    ("Salidas", 96 -3)),
                     lineas_verticales = ((61, True),
                                          (61 + 6 + 7, True),
                                          (61 + 2 * (6 + 7), True),
                                          (22, True),
                                          (22 + 7 + 7 + 8, True), ),
                     exportar_a_csv_a = exportar_a_csv_a)

def repuestos_no_nulos(hasta = None, exportar_a_csv_a = None):
    """
    Imprime un informe de existencias al día actual si "hasta" es None
    o hasta la fecha indicada.
    OJO: Los repuestos deben tener como tipo de material uno que tenga en
    su descripción "aceite", "lubricante" o "repuesto".
    Devuelve tantos nombres de archivo como tipos de material de repuestos
    haya en la base de datos.
    """
    if hasta == None:
        nomarchivo = os.path.join(gettempdir(),
                        "repuestos_no_nulos_%s.pdf" % give_me_the_name_baby())
        fecha = None
        fecha_limite = " - %s, %s"%(utils.str_fecha(mx.DateTime.localtime()),
                                    time.strftime("%H:%M"))
    else:
        nomarchivo = os.path.join(gettempdir(),
            "repuestos_no_nulos_a_%s_%s.pdf" % (hasta.strftime("%Y_%m_%d"),
                                                give_me_the_name_baby()))
        fecha = utils.str_fecha(hasta)
        fecha_limite = " a %s" % (utils.str_fecha(hasta))
    titulo = 'Inventario de repuestos (existencias no nulas) %s'%(fecha_limite)
    campos = [('Artículo', 55),
              ('Cantidad', 15),
              ('Precio', 15),
              ('Total', 15),
             ]
    datos = []
    productos = pclases.ProductoCompra.select(pclases.AND(
            pclases.ProductoCompra.q.controlExistencias == True,
            pclases.ProductoCompra.q.existencias != 0, 
            pclases.ProductoCompra.q.obsoleto == False),
        orderBy = "descripcion")
    tipos_repuestos = pclases.TipoDeMaterial.select(pclases.OR(
        pclases.TipoDeMaterial.q.descripcion.contains("repuesto"),
        pclases.TipoDeMaterial.q.descripcion.contains("aceite"),
        pclases.TipoDeMaterial.q.descripcion.contains("lubricante")))
    ids_reps = [t.id for t in tipos_repuestos]
    productos = [p for p in productos if p.tipoDeMaterialID in (ids_reps)]
    por_tipo = {}
    for p in productos:
        if p.tipoDeMaterial not in por_tipo:
            por_tipo[p.tipoDeMaterial] = [p]
        else:
            por_tipo[p.tipoDeMaterial].append(p)
    ficheros = []
    for tipo in por_tipo:
        datos = []
        total = 0.0
        for p in por_tipo[tipo]:
            p.sync()
            precio_medio = p.get_precio_medio()
            if precio_medio == None:
                precio_medio = p.precioDefecto
            subtotal = precio_medio * p.existencias
            datos.append((p.descripcion,
                          utils.float2str(p.existencias),
                          utils.float2str(precio_medio),
                          utils.float2str(subtotal)))
            total += subtotal
        datos.append(("", "", "TOTAL", utils.float2str(total)))
        if exportar_a_csv_a != None:
            exportar_a_csv_a = "%s_%d" % (exportar_a_csv_a, tipo.id)
        _nomarchivo = "%s_%d.pdf" % (nomarchivo.replace(".pdf", ""), tipo.id)
        fichpdf = imprimir2(archivo = _nomarchivo,
                            titulo = tipo.descripcion + " - " + titulo,
                            campos = campos,
                            datos = datos,
                            fecha = fecha,
                            cols_a_derecha = (1, 2, 3),
                            graficos = [],
                            apaisado = False,
                            exportar_a_csv_a = exportar_a_csv_a)
        ficheros.append(fichpdf)
    return ficheros

def repuestos(hasta = None, exportar_a_csv_a = None):
    """
    Imprime un informe de existencias al día actual si "hasta" es None
    o hasta la fecha indicada.
    OJO: Los repuestos deben tener como tipo de material uno que tenga en
    su descripción "aceite", "lubricante" o "repuesto".
    Devuelve tantos nombres de archivo como tipos de material de repuestos
    haya en la base de datos.
    """
    if hasta == None:
        nomarchivo = os.path.join(gettempdir(),
            "repuestos_%s.pdf" % give_me_the_name_baby())
        fecha = None
        fecha_limite = " - %s, %s"%(utils.str_fecha(mx.DateTime.localtime()),
                                    time.strftime("%H:%M"))
    else:
        nomarchivo = os.path.join(gettempdir(), "repuestos_%s_%s.pdf" % (
            hasta.strftime("%Y_%m_%d"), give_me_the_name_baby()))
        fecha = utils.str_fecha(hasta)
        fecha_limite = " a %s" % (utils.str_fecha(hasta))
    titulo = 'Inventario de repuestos %s' % (fecha_limite)
    campos = [('Artículo', 55),
              ('Cantidad', 15),
              ('Precio', 15),
              ('Total', 15),
             ]
    datos = []
    productos = pclases.ProductoCompra.select(pclases.AND(
            pclases.ProductoCompra.q.controlExistencias == True,
            pclases.ProductoCompra.q.obsoleto == False), 
        orderBy = "descripcion")
    tipos_repuestos = pclases.TipoDeMaterial.select(pclases.OR(
        pclases.TipoDeMaterial.q.descripcion.contains("repuesto"),
        pclases.TipoDeMaterial.q.descripcion.contains("aceite"),
        pclases.TipoDeMaterial.q.descripcion.contains("lubricante")))
    ids_reps = [t.id for t in tipos_repuestos]
    productos = [p for p in productos if p.tipoDeMaterialID in (ids_reps)]
    por_tipo = {}
    for p in productos:
        if p.tipoDeMaterial not in por_tipo:
            por_tipo[p.tipoDeMaterial] = [p]
        else:
            por_tipo[p.tipoDeMaterial].append(p)
    ficheros = []
    for tipo in por_tipo:
        datos = []
        total = 0.0
        for p in por_tipo[tipo]:
            p.sync()
            precio_medio = p.get_precio_medio()
            if precio_medio == None:
                precio_medio = p.precioDefecto
            subtotal = precio_medio * p.existencias
            datos.append((p.descripcion,
                          utils.float2str(p.existencias),
                          utils.float2str(precio_medio),
                          utils.float2str(subtotal)))
            total += subtotal
        datos.append(("", "", "TOTAL", utils.float2str(total)))
        if exportar_a_csv_a != None:
            _exportar_a_csv_a = "%s_%d" % (exportar_a_csv_a, tipo.id)
            if not _exportar_a_csv_a.endswith(".csv"):
                _exportar_a_csv_a += ".csv"
        else:
            _exportar_a_csv_a = None
        _nomarchivo = "%s_%d.pdf" % (nomarchivo.replace(".pdf", ""), tipo.id)
        fichpdf = imprimir2(archivo = _nomarchivo,
                            titulo = tipo.descripcion + " - " + titulo,
                            campos = campos,
                            datos = datos,
                            fecha = fecha,
                            cols_a_derecha = (1, 2, 3),
                            graficos = [],
                            apaisado = False,
                            exportar_a_csv_a = _exportar_a_csv_a)
        ficheros.append(fichpdf)
    return ficheros

def resumen_totales_geotextiles(datos, str_fecha, str_anno):
    """
    Informe resumen de totales de producción, existencias, salidas y
    pedidos de geotextiles.
    """
    nomarchivo = os.path.join(gettempdir(),
        "resumen_totales_gtx_%(y)s_%(nombre)s.pdf" % {
                'y': str_anno,
                'nombre': give_me_the_name_baby()})
    titulo = "Resumen totales geotextiles - %s" % (str_anno)
    campos = (("Mes", 4),
              ("rollos", 3),
              ("m²", 4),
              ("kg", 5),
              ("rollos", 3),
              ("m²", 4),
              ("kg", 5),
              ("rollos", 3),
              ("m²", 4),
              ("kg", 5),
              ("rollos", 3),
              ("m²", 4),
              ("kg", 5),
              ("rollos", 3),
              ("m²", 4),
              ("kg", 5),
              ("rollos", 3),
              ("m²", 4),
              ("kg", 5),
              ("rollos", 3),
              ("m²", 4),
              ("kg", 5),
              ("rollos", 3),
              ("m²", 4),
              ("kg", 5))
    return imprimir2(archivo = nomarchivo,
                     titulo = titulo,
                     campos = campos,
                     datos = datos,
                     fecha = str_fecha,
                     cols_a_derecha = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                                       13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                       23, 24),
                     graficos = [],
                     apaisado = True,
                     sobrecampos = (("Producción", 10),
                                    ("Existencias", 22),
                                    ("Salidas", 34),
                                    ("Comp. nac.", 46),
                                    ("Comp. int.", 58),
                                    ("Gea", 70),
                                    ("Otros", 82),
                                    ("Pendiente", 94)),
                     lineas_verticales = ((4, True),
                                          (7, False),
                                          (11, False),
                                          (16, True),
                                          (19, False),
                                          (23, False),
                                          (28, True),
                                          (31, False),
                                          (35, False),
                                          (40, True),
                                          (43, False),
                                          (47, False),
                                          (52, True),
                                          (55, False),
                                          (59, False),
                                          (64, True),
                                          (67, False),
                                          (71, False),
                                          (76, True),
                                          (79, False),
                                          (83, False),
                                          (88, True),
                                          (91, False),
                                          (95, False)) )


def buscar_datos_existencias(p, hasta):
    """
    Devuelve los datos del producto p para el informe de existencias
    en función de si hay fecha límite o no.
    """
    uno_del_anno_corriente = mx.DateTime.DateTimeFrom(day = 1,
                                        month = 1,
                                        year = mx.DateTime.localtime().year)
    p.sync()    # Las existencias se están moviendo constantemente, mejor me
                # aseguro de leer el valor actual.
    if hasta == None:
        existencias = p.existencias
    else:
        existencias = p.get_existencias_historico(hasta)
    precio_valoracion = p.get_precio_valoracion(fechafin = hasta)
    if precio_valoracion != None:
        valoracion = existencias * precio_valoracion
    else:
        valoracion = None
    existencias_1_enero = p.get_existencias_historico(uno_del_anno_corriente)
    entradas = p.get_entradas(fechaini=uno_del_anno_corriente, fechafin=hasta)
    stock_entradas = 0
    valoracion_entradas = 0
    for fecha in entradas:
        for albaran in entradas[fecha]['albaranes']:
            for ldc in albaran.lineasDeCompra:
                stock_entradas += ldc.cantidad
                valoracion_entradas += ldc.get_subtotal()
    salidas = p.get_salidas(fechaini=uno_del_anno_corriente, fechafin=hasta)
    stock_salidas = 0
    valoracion_salidas = 0
    try:
        precio_medio = valoracion_entradas / stock_entradas
    except ZeroDivisionError:
        precio_medio = 0
    for fecha in salidas:
        for albaran in salidas[fecha]['albaranes']:
            for ldv in albaran.lineasDeVenta:
                stock_salidas += ldv.cantidad
                valoracion_salidas += ldv.get_subtotal()
        for parte in salidas[fecha]['partes']:
            stock_salidas += salidas[fecha]['partes'][parte]
            valoracion_salidas += salidas[fecha]['partes'][parte]*precio_medio
    pedidos_pendientes = p.get_pendientes(fechafin = hasta)
    return (existencias, valoracion, existencias_1_enero, stock_entradas,
            valoracion_entradas, stock_salidas, valoracion_salidas,
            pedidos_pendientes)


def _existencias(hasta = None):
    """
    Crea un informe relativo a los materiales bajo mínimos
    """

    global linea, tm, lm, rm, bm
    x, y = lm, tm  # @UnusedVariable

    # Creo la hoja
    if hasta == None:
        nomarchivo = os.path.join(gettempdir(),
            "existencias_simple_%s.pdf" % give_me_the_name_baby())
    else:
        nomarchivo = os.path.join(gettempdir(),
            "existencias_simple_a_%s_%s.pdf" % (hasta.strftime("%Y_%m_%d"),
                                                give_me_the_name_baby()))
    c = canvas.Canvas(nomarchivo)
    # Ponemos la cabecera
    if hasta != None:
        fecha_limite = " a %s" % (utils.str_fecha(hasta))
    else:
        fecha_limite = " - %s" % (utils.str_fecha(mx.DateTime.localtime()))
    cabecera(c, 'Inventario de materiales%s' % (fecha_limite))
    # El cuerpo
    c.setFont("Helvetica-Bold", 10)

    linea = tm + inch

    # Campos
    c.drawString(x, linea, escribe('Codigo'))
    c.drawString(25*4, linea, escribe('Descripción'))
    c.drawString(75*5, linea, escribe('Mínimo'))
    c.drawString(90*5, linea, escribe('Stock'))

    c.line(lm, linea-2, rm, linea-2)
    c.setFont("Helvetica", 10)
    productos = pclases.ProductoCompra.select(orderBy = "descripcion")

    # 41 es el número máximo de líneas en el área de impresión
    paginas = (productos.count() / MAXLINEAS) +1
    x = lm
    y = linea  # @UnusedVariable
    # contLinea se va incrementando con cada elemento y llegado al tope de
    # líneas provoca la creación de una nueva página
    contLinea = 0
    actualPagina = 1
    linea = sigLinea()
    for item in productos:

            c.drawString(x, linea, escribe(item.codigo))
            el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, 25 * 4,
                                                75*5, linea, item.descripcion)
            c.drawString(75*5, linea, escribe(utils.float2str(item.minimo, 2)))
            if hasta != None:
                existencias = item.get_existencias_historico(hasta)
            else:
                existencias = item.existencias
            # En rojo si está por debajo del mínimo
            if existencias < item.minimo:
                c.setFillColorRGB(255, 0, 0)
            c.drawRightString(100*5, linea, escribe("%s" % (
                utils.float2str(existencias, 2))))
            c.drawString(101*5, linea, escribe(" %s" % (item.unidad)))
            c.setFillColorRGB(0, 0, 0)
            contLinea += 1
            if contLinea == MAXLINEAS:
                pie(c, actualPagina, paginas)
                c.showPage()
                contLinea = 0
                actualPagina += 1
                cabecera(c, 'Inventario de materiales%s' % (fecha_limite))
                linea = tm + inch
                # El cuerpo
                x, y = lm, tm + inch  # @UnusedVariable
                c.setFont("Helvetica-Bold", 10)
                c.drawString(x, linea, escribe('Codigo'))
                c.drawString(25*5, linea, escribe('Descripción'))
                c.drawString(75*5, linea, escribe('Mínimo'))
                c.drawString(90*5, linea, escribe('Stock'))
                c.line(lm, linea-2, rm, linea-2)
                c.setFont("Helvetica", 10)
                x = lm
                y = tm + inch  # @UnusedVariable
                linea = sigLinea()
            else:
                linea = sigLinea()
                y = linea  # @UnusedVariable
                x = lm

    # Ponemos el pie
    pie(c, actualPagina, paginas)
    # Salvamos la página
    c.showPage()
    # Salvamos el documento
    c.save()

    return nomarchivo


def existencias_productos(informe, fecha, hasta = None, almacen = None, 
                          ruta_csv = None):
    """
    Crea un informe relativo a los geotextiles o balas bajo mínimos.
    El parametro informe puede valer 'rollos' o 'balas'.
    Si ruta_csv es != None volcará los datos del PDF en un CSV en esa ruta.
    """
    # Campos que se muestran: Código, nombre, descripción, Mínimo, Stock

    global linea, tm, lm, rm, bm

    # Datos en matriz para CSV:
    csv_cabecera = []
    csv_data = []

    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
        "existencias_productos%s.pdf" % give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo)

    # Campos
    xDescripcion = lm + 4
    xMinimo = rm - 3*inch
    xStock = rm - 2*inch
    xExist = rm - inch

    if informe == 'rollos':
        productos = [p for p in
                     pclases.ProductoVenta.select(orderBy = "descripcion")
                     if p.es_rollo()] \
                    + ["total"] \
                    + [p for p in
                       pclases.ProductoVenta.select(orderBy = "descripcion")
                       if p.es_rolloC()] \
                    + ["gtxb"]  # gtxb = rollos defectuosos.
        unidad = "m²"
    elif informe == 'balas':
        productos = [p for p in
                     pclases.ProductoVenta.select(orderBy = "descripcion")
                     if p.es_bala() or p.es_bigbag() or p.es_bala_cable()
                         or p.es_bolsa()]
        productos.sort(lambda p1, p2: 
            int(p1.lineaDeProduccionID - p2.lineaDeProduccionID))
        productos += ["total"]
        unidad = "kg"
    else:
        print '"informe" debe ser "rollos" o "balas".'
        return

    # 41 es el número máximo de líneas en el área de impresión
    maxlineas = MAXLINEAS - 2
    paginas = (len(productos) + 5)/maxlineas + 1
    total_stock = 0.0
    total_bultos = 0
    hay_prods_en_cursiva = False
    for i in range(paginas):
        # Ponemos la cabecera
        if almacen:
            txtalmacen = ": " + almacen.nombre
        else:
            txtalmacen = ""
        if informe == 'rollos':
            cabecera(c, 'Inventario de geotextiles%s' % txtalmacen, fecha)
            c.setTitle("Inventario de geotextiles%s" % txtalmacen)
        elif informe == 'balas':
            cabecera(c, 'Inventario de fibras%s' % txtalmacen, fecha)
            c.setTitle("Inventario de fibras%s" % txtalmacen)
        # El cuerpo
        c.setFont("Helvetica-Bold", 10)

        linea = tm + 1*inch
        c.drawString(xDescripcion, linea, escribe('Descripción'))
        c.drawRightString(xMinimo, linea, escribe('Mínimo'))
        c.drawRightString(xStock, linea, escribe('Existencias'))
        c.drawRightString(xExist, linea, escribe('Bultos'))
        csv_cabecera = (("Descripción", 0), 
                        ("Mínimo", 0), 
                        ("Existencias", 0), 
                        ("Bultos", 0))

        linea = linea -2
        c.line(lm, linea, rm, linea)
        c.setFont("Helvetica", 10)

        actualPagina = i+1
        lineaActual = 0
        linea = sigLinea()

        pagina = i
        inicio = maxlineas * pagina
        fin = maxlineas * (pagina+1)
        for p in productos[inicio:fin]:
            if p == "total":
                c.line(xDescripcion, linea, xExist, linea)
                linea = sigLinea()
                c.drawRightString(xMinimo, linea, escribe("TOTAL: "))
                c.drawRightString(xStock, linea,
                    escribe("%s %s" % (utils.float2str(total_stock, 1),
                                       unidad)))
                c.drawRightString(xExist, linea, escribe(total_bultos))
                if hay_prods_en_cursiva:
                    c.setFont("Helvetica-BoldOblique", 7)
                    linea = sigLinea()
                    txt = "NOTA: Los productos en cursiva"\
                          " no computan en el total."
                    c.drawRightString(rm - 0.5*cm, linea, escribe(txt))
                linea = sigLinea()
            elif p == "gtxb":   # CWT: Si tienes un alma sensible, ignora esta
                                # chapuza. Por tu bien.
                RD = pclases.RolloDefectuoso
                PDP = pclases.ParteDeProduccion
                A = pclases.Articulo
                if hasta:
                    rdefs = RD.select(pclases.AND(
                                    A.q.rolloDefectuosoID == RD.q.id,
                                    A.q.parteDeProduccionID == PDP.q.id,
                                    PDP.q.fecha <= hasta))
                    peso_gtxb = 0.0
                    metros2 = 0.0
                    bultos = 0
                    if rdefs.count() > 0:
                        for r in rdefs:
                            if (r.albaranSalidaID == None
                                or r.albaranSalida.fecha > hasta):
                                peso_gtxb += r.peso
                                metros2 += r.articulo.superficie
                                bultos += 1

                else:
                    rdefs = RD.select(pclases.AND(
                            A.q.rolloDefectuosoID == RD.q.id,
                            A.q.albaranSalidaID == None,
                        ))
                    if rdefs.count() > 0:
                        peso_gtxb = rdefs.sum("peso")
                        metros2 = rdefs.sum("ancho * metros_lineales")
                        bultos = rdefs.count()
                    else:
                        peso_gtxb = 0.0
                        metros2 = 0.0
                        bultos = 0
                c.saveState()
                c.setFont("Helvetica-Oblique", 10)
                hay_prods_en_cursiva = bultos != 0
                c.drawString(xDescripcion, linea,
                             escribe("Geotextiles B (varios productos)"))
                c.drawRightString(xStock, linea,
                                  escribe("%s kg"%utils.float2str(peso_gtxb)))
                c.drawRightString(xMinimo, linea,
                                  escribe("%s m²" % utils.float2str(metros2)))
                c.drawRightString(xExist, linea,
                                  escribe("%d" % bultos))
                csv_data.append(("Geotextiles B (varios productos)", 
                                 peso_gtxb, 
                                 metros2, 
                                 bultos))
                unidad = None   # Para que no entren tampoco en el total.
                c.restoreState()
            else:
                unidad_producto = p.get_unidad()
                if unidad != unidad_producto:
                    c.saveState()
                    c.setFont("Helvetica-Oblique", 10)
                    hay_prods_en_cursiva = True
                c.drawString(xDescripcion, linea, escribe(p.descripcion))
                if not p.es_rolloC() or p.minimo != 0:
                    c.drawRightString(xMinimo, linea,
                                  escribe("%s" % utils.float2str(p.minimo, 1)))
                # En rojo si está por debajo del mínimo
                #stock = p.get_stock(hasta, almacen = almacen)
                stock = p.get_stock_A(hasta, almacen = almacen) # Nada de 
                    # rollos defectuosos (remember: rollos X, largo inferior, 
                    # no los quiero).
                if stock < p.minimo:
                    c.setFillColorRGB(255, 0, 0)
                if stock == None:
                    print "===============> El stock de %s es None!!!", p.descripcion
                    stock = 0
                try:
                    strstock = utils.float2str(stock, 1)
                except ValueError:  
                    strstock = "-"
                c.drawRightString(xStock, linea,
                                  escribe("%s %s"%(strstock, unidad_producto)))
                bultos = p.get_existencias_A(hasta, almacen = almacen)# Nada 
                    # de rollos defectuosos (remember: rollos X, largo 
                    # inferior, no los quiero).
                c.drawRightString(xExist, linea, escribe(bultos))
                c.setFillColorRGB(0, 0, 0)
                csv_data.append((p.descripcion, p.minimo, stock, bultos))
                if unidad == unidad_producto:  # No cuento los
                        # productos que no comparten unidad con
                        # el total, como el caso de los gtx C.
                    total_stock += stock
                    total_bultos += bultos
                else:
                    c.restoreState()
                lineaActual += 1
                if lineaActual == maxlineas:
                    break
            linea = sigLinea()
        #if actualPagina == paginas:
        #    # TOTAL en LA ÚLTIMA PÁGINA:
        #    c.line(xDescripcion, linea, xExist, linea)
        #    linea = sigLinea()
        #    c.drawRightString(xMinimo, linea, escribe("TOTAL: "))
        #    c.drawRightString(xStock, linea, escribe("%s %s" % (
        #       utils.float2str(total_stock, 1), unidad)))
        #    c.drawRightString(xExist, linea, escribe(total_bultos))
        #    if hay_prods_en_cursiva:
        #        c.setFont("Helvetica-BoldOblique", 7)
        #        linea = sigLinea()
        #        txt="NOTA: Los productos en cursiva no computan en el total."
        #        c.drawRightString(rm - 0.5*cm, linea, escribe(txt))

        # Ponemos el pie
        pie(c, actualPagina, paginas)
        # Salvamos la página
        c.showPage()
    # Salvamos el documento
    c.save()

    if ruta_csv:
        exportar_a_csv(ruta_csv, csv_cabecera, csv_data)

    return nomarchivo


def rectangulo(hoja,
               esquina1,
               esquina2,
               texto = '',
               alinTxtX = None,
               alinTxtY = None,
               doble = False,
               color_relleno = None):
    """
    Dada la tupla esquina superior izquierda y la
    tupla inferior derecha traza un rectángulo
    Si se pasa un texto como parámetro lo escribe en la
    esquina superior izquierda por dentro
    """
    if doble:
        hoja.saveState()
        hoja.setLineWidth(0.5)
        hoja.line(esquina1[0], esquina1[1], esquina1[0], esquina2[1])
        hoja.line(esquina1[0], esquina2[1], esquina2[0], esquina2[1])
        hoja.line(esquina2[0], esquina2[1], esquina2[0], esquina1[1])
        hoja.line(esquina2[0], esquina1[1], esquina1[0], esquina1[1])

        hoja.line(esquina1[0]+2, esquina1[1]-2, esquina1[0]+2, esquina2[1]+2)
        hoja.line(esquina1[0]+2, esquina2[1]+2, esquina2[0]-2, esquina2[1]+2)
        hoja.line(esquina2[0]-2, esquina2[1]+2, esquina2[0]-2, esquina1[1]-2)
        hoja.line(esquina2[0]-2, esquina1[1]-2, esquina1[0]+2, esquina1[1]-2)
        hoja.restoreState()
    else:
        hoja.line(esquina1[0], esquina1[1], esquina1[0], esquina2[1])
        hoja.line(esquina1[0], esquina2[1], esquina2[0], esquina2[1])
        hoja.line(esquina2[0], esquina2[1], esquina2[0], esquina1[1])
        hoja.line(esquina2[0], esquina1[1], esquina1[0], esquina1[1])

    if color_relleno:
        hoja.saveState()
        hoja.setFillColorRGB(*color_relleno)
        hoja.rect(esquina1[0], esquina1[1],
                  esquina2[0] - esquina1[0], esquina2[1] - esquina1[1],
                  fill = 1)
        hoja.restoreState()

    if alinTxtY == None:
        lin = esquina2[1]+4
    elif alinTxtY == 'arriba':
        lin = esquina1[1] - 11
    elif alinTxtY == 'centro':
        lin = ((esquina1[1] + esquina2[1]) / 2) - 5

    fuente = hoja._fontname
    tamannoini = hoja._fontsize
    if texto: # != "":
        if alinTxtX == None or alinTxtX == 'izquierda':
            # el_encogedor_de_fuentes_de_doraemon(hoja, fuente, tamannoini,
            # esquina1[0]+5, esquina2[0]-2, lin, escribe(texto), alineacion=-1)
            el_encogedor_de_fuentes_de_doraemon(hoja, fuente, tamannoini,
                esquina1[0]+5, esquina2[0]-2, lin, texto, alineacion = -1)
            # hoja.drawString(esquina1[0]+5, lin, escribe(texto))
        elif alinTxtX == 'centro':
            #el_encogedor_de_fuentes_de_doraemon(hoja, fuente, tamannoini,
            # esquina1[0]+5, esquina2[0]-2, lin, escribe(texto), alineacion=0)
            el_encogedor_de_fuentes_de_doraemon(hoja, fuente, tamannoini,
                esquina1[0]+5, esquina2[0]-2, lin, texto, alineacion = 0)
            #hoja.drawCentredString((esquina1[0]+esquina2[0])/2, lin,
            #   escribe(texto))
        elif alinTxtX == 'derecha':
            #el_encogedor_de_fuentes_de_doraemon(hoja, fuente, tamannoini,
            # esquina1[0]+5, esquina2[0]-2, lin, escribe(texto), alineacion 1)
            el_encogedor_de_fuentes_de_doraemon(hoja, fuente, tamannoini,
                esquina1[0]+5, esquina2[0]-2, lin, texto, alineacion = 1)
            #hoja.drawRightString(esquina2[0]-2, lin, escribe(texto))


def albaran(composan, cliente, envio, general, lineas, observaciones, destino,
            transporte, conformeT, conformeD):
    """
    Con los datos de entrada genera el albarán.

    @params

    composan --> es un valor booleano que si es True genera el
    albarán de composán (amarillo) y si es False genera el
    albarán de Geotexan (verde)

    cliente --> datos del cliente (no los de envio), es un diccionario con:
        - 'nombre'
        - 'direccion'
        - 'cp'
        - 'localidad'
        - 'provincia'
        - 'pais'
        ' 'telf'

    envio --> datos que se ven en el sobre, es un diccionario con:
        - 'nombre'
        - 'direccion'
        - 'cp'
        - 'localidad'
        - 'provincia'
        - 'pais'
        - 'telf'

    general --> datos de la cabecera del albarán, diccionario con:
        - 'albnum' Número de albarán
        - 'fecha'
        - 'exp' Expedido en
        - 'clinum' Número de cliente
        - 'pednum' Número de pedido
        - 'numref' Número de referencia
        ' 'sref' MIRAR Viene en el albarán como S/REFERENCIA

    lineas --> datos del cuerpo del albarán, es una lista (un elemento
    por línea) de diccionarios con:
        - 'bultos'
        - 'codigo' //Debe soportar 13 digitos en la hoja
        - 'descripcion'
        - 'cantidad' Cantidad servida
        - 'numped' Número de pedido

    observaciones --> una cadena

    destino --> una cadena

    transporte --> una cadena

    conformeT --> datos del transportista para la firma de conforme. Es
    un diccionario con:
        - 'nombre'
        - 'dni'
        - 'telf'
        - 'matricula'

    conformeD --> conforme destino sólo para el albarán de composán. Es None
    para el normal y para el de composán es un diccionario con:
        - 'nombre'
        - 'dni'
        - 'telf'
        - 'matricula'

    """
    datos_empresa = pclases.DatosDeLaEmpresa.select()[0]

    # TODO: No se ha dado todavía el caso, pero si el albarán tiene más de una
    #       página, falla estrepitosamente y se mete todo en la misma página.
    global linea, tm, lm, rm, bm
    x, y = lm, tm  # @UnusedVariable
    global linea

    # Creo la hoja
    if composan:
        nomarchivo = os.path.join(gettempdir(),
            "albaranComposan_%s.pdf" % give_me_the_name_baby())
    else:
        nomarchivo = os.path.join(gettempdir(),
            "albaran_%s.pdf" % give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo)
    # La cabecera
    if composan:
        if datos_empresa.logo2:
            c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', datos_empresa.logo2),
                        lm+0.5*inch, height - 0.5*inch, 2*inch, 0.5*inch)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width/2, tm+inch, escribe('ALBARÁN'))
        c.setFont("Helvetica", 8)
        linea = height-15
        c.drawString(width-2.5*inch, linea, escribe(datos_empresa.nomalbaran2))
        linea = sigLinea()
        c.drawString(width-2.5*inch, linea, escribe('%s %s' % (
            datos_empresa.diralbaran2, datos_empresa.cpalbaran2)))
        linea = sigLinea()
        c.drawString(width-2.5*inch, linea, escribe('%s. %s' % (
            datos_empresa.ciualbaran2, datos_empresa.proalbaran2)))
        linea = sigLinea()
        c.drawString(width-2.5*inch, linea, escribe('Tel: %s Fax: %s' % (
            datos_empresa.telalbaran2, datos_empresa.faxalbaran2)))
    else:
        ruta_logo = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', datos_empresa.logo)
        im = Image.open(ruta_logo)
        ancho, alto = im.size
        nuevo_alto = 1.5 * inch
        ancho_proporcional = ancho * (nuevo_alto / alto)
        c.drawImage(ruta_logo,
                    lm+0.5*inch,
                    height - 1.5*inch,
                    ancho_proporcional,
                    nuevo_alto)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width/2, tm+inch, escribe('ALBARÁN'))
        if datos_empresa.bvqi:
            # c.drawImage(os.path.join('..', 'imagenes',
            #   datos_empresa.logoiso1), rm-1.5*inch, tm+0.75*inch, inch,
            #   0.65*inch)
            c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', datos_empresa.logoiso1),
                        rm-1.75*inch,
                        tm+0.65*inch,
                        width = 119,
                        height = 65)
            c.setFont("Helvetica", 6)
            c.drawCentredString(rm-0.94*inch, tm+0.66*inch, escribe('Geotextiles CE 1035-CPD-ES033858'))
            c.drawCentredString(rm-0.94*inch, tm+0.56*inch, escribe('Fibra CE 1035-CPD-9003712'))
        c.setFont("Helvetica", 8)
        linea = height-15
        if datos_empresa.direccion != datos_empresa.dirfacturacion:
            if not datos_empresa.esSociedad:
                c.drawString(width/2-1.5*inch, linea,
                             escribe(datos_empresa.nombreContacto))
                c.drawString(width-2.5*inch, linea,
                             escribe(datos_empresa.nombre))
            else:
                c.drawString(width/2-1.5*inch, linea, 
                             escribe('DOMICILIO SOCIAL'))
                c.drawString(width-2.5*inch, linea, escribe('FÁBRICA'))
            linea -= 10
            c.drawString(width/2-1.5*inch, linea,
                         escribe(datos_empresa.dirfacturacion))
            c.drawString(width-2.5*inch, linea,
                         escribe(datos_empresa.direccion))
            linea -= 10
            c.drawString(width/2-1.5*inch, linea, escribe('%s %s%s, %s' % (
                datos_empresa.cpfacturacion,
                datos_empresa.ciudadfacturacion,
                datos_empresa.provinciafacturacion
                    != datos_empresa.ciudadfacturacion
                    and " (%s)" % (datos_empresa.provinciafacturacion) or "",
                datos_empresa.paisfacturacion)))
            c.drawString(width-2.5*inch, linea, escribe('%s %s%s, %s' % (
                datos_empresa.cp,
                datos_empresa.ciudad,
                datos_empresa.provincia != datos_empresa.ciudad
                    and " (%s)" % (datos_empresa.provincia) or "",
                datos_empresa.pais)))
            linea -= 10
            c.drawString(width/2-1.5*inch, linea,
                escribe('Telf: %s' % (datos_empresa.telefonofacturacion)))
            c.drawString(width-2.5*inch, linea,
                escribe('Telf: %s' % (datos_empresa.telefono)))
            linea -= 10
            c.drawString(width/2-1.5*inch, linea,
                escribe('Fax: %s' % (datos_empresa.faxfacturacion)))
            c.drawString(width-2.5*inch, linea,
                escribe('Fax: %s' % (datos_empresa.fax)))
        else:
            c.drawString(width-2.5*inch, linea, escribe('DIRECCIÓN'))
            linea -= 10
            c.drawString(width-2.5*inch, linea,
                         escribe(datos_empresa.direccion))
            linea -= 10
            c.drawString(width-2.5*inch, linea, escribe('%s %s%s, %s' % (
                datos_empresa.cp,
                datos_empresa.ciudad,
                datos_empresa.provincia != datos_empresa.ciudad
                    and " (%s)" % (datos_empresa.provincia) or "",
                datos_empresa.pais)))
            linea -= 10
            c.drawString(width-2.5*inch, linea,
                escribe('Telf: %s' % (datos_empresa.telefono)))
            linea -= 10
            c.drawString(width-2.5*inch, linea,
                escribe('Fax: %s' % (datos_empresa.fax)))
    # Los cuadros de datos del cliente y datos de envío
    c.setFont("Helvetica", 10)
    if composan:
        c.setFillColorRGB(1, 1, 0.9)
    else:
        c.setFillColorRGB(0.9, 1, 0.9)
    c.rect(lm+0.5*inch, tm+0.5*inch, 2.9*inch, -1.5*inch, fill=1)
    c.setFillColorRGB(0, 0, 0)
    rectangulo(c, (width/2, tm+0.5*inch), (rm, tm-inch))
    c.drawString(lm+0.5*inch, tm+0.5*inch+5, 'DATOS CLIENTE')
    c.drawString(width/2, tm+0.5*inch+5, 'DATOS ENVIO')
    ### DATA
    if cliente != None:
        linea = tm+0.5*inch-25
        xcliente = lm+0.5*inch+4
        #c.drawString(xcliente, linea, escribe(cliente['nombre'][:29]))
        #c.drawString(xcliente, linea, escribe(cliente['nombre']))
        lineas_agregadas = agregarFila(xcliente, linea, (width/2+3) - 0.8*cm,
            escribe(cliente["nombre"]), c, "Helvetica", 10)
        for linea_agregada in range(lineas_agregadas):  # @UnusedVariable
            linea = sigLinea()
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xcliente,
            (width/2+3) - 0.8*cm, linea, cliente['direccion'])
        linea = sigLinea()
        c.drawString(xcliente, linea, escribe(cliente['provincia']))
        linea = sigLinea()
        if cliente['cp']:
            c.drawString(xcliente, linea, escribe("%s, %s" % (cliente['cp'],
                         cliente['ciudad'])))
        else:
            c.drawString(xcliente, linea, escribe("%s" % (cliente['ciudad'])))
        linea = sigLinea()
        c.drawString(xcliente, linea, escribe(cliente['pais']))
        linea = sigLinea()

    if envio != None:
        #linea = tm+0.5*inch-30
        linea = tm+0.5*inch-25
        lineas_agregadas = agregarFila(width/2+3, linea, width - 0.8 * cm,
                                       escribe(envio["nombre"]),
                                       c, "Helvetica", 10)
        for linea_agregada in range(lineas_agregadas):  # @UnusedVariable
            linea = sigLinea()
        #c.drawString(width/2+3, linea, escribe(envio['nombre']))
        #linea = sigLinea()
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, width/2+3, rm,
                                            linea, envio['direccion'])
        #el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, width/2+3,
        #                                    width, linea, envio['direccion'])
        linea = sigLinea()
        c.drawString(width/2+3, linea,
                     escribe(envio['cp']+' '+envio['localidad']))
        linea = sigLinea()
        c.drawString(width/2+3, linea, escribe(envio['pais']))
        linea = sigLinea()
        c.drawString(width/2+3, linea, escribe(envio['telefono']))

    # Datos generales (Esquina superior izquierda x=lm+0.5*inch, y=tm-1.2*inch)
    rectangulo(c, (lm+0.5*inch, tm-1.2*inch), (width/2, tm-1.2*inch-16),
                'ALBARÁN Nº:')
    rectangulo(c, (width/2, tm-1.2*inch), (width/2+1.5*inch, tm-1.2*inch-16),
                'FECHA:')
    rectangulo(c, (width/2+1.5*inch, tm-1.2*inch), (rm, tm-1.2*inch-16),
                'EXPEDIDO EN:')
    rectangulo(c, (lm+0.5*inch, tm-1.2*inch-16),
                (width/2 - inch, tm-1.2*inch-32), 'Nº CLIENTE:')
    rectangulo(c, (width/2 - inch, tm-1.2*inch-16),
                (width/2+1.5*inch, tm-1.2*inch-32), 'Nº PEDIDO:')
    rectangulo(c, (width/2+1.5*inch, tm-1.2*inch-16),
                (rm, tm-1.2*inch-32), 'Nº REFERENCIA:')
    rectangulo(c, (lm+0.5*inch, tm-1.2*inch-32), (rm, tm-1.2*inch-48),
                'S/REFERENCIA:')
    # DATA
    linea = tm-1.2*inch-12
    c.drawRightString(width/2-4, linea, escribe(general['albnum']))
    c.drawRightString(width/2+1.5*inch-4, linea, escribe(general['fecha']))
    c.drawRightString(rm-4, linea, escribe(general['exp']))
    linea = sigLinea()
    c.drawRightString(width/2-inch-4, linea, escribe(general['numcli']))
    xnumpedizq = width/2 - inch + c.stringWidth("Nº PEDIDO:", "Helvetica", 10)
    xnumpedder = width/2+1.5*inch-4
    el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xnumpedizq,
        xnumpedder, linea, general['numped'], alineacion = 1)
    c.drawRightString(rm-4, linea, escribe(general['numref']))
    linea = sigLinea()
    c.drawString(lm+1.8*inch, linea, escribe(general['sref']))

    # El cuerpo
    # -- Cuadro global
    rectangulo(c, (lm+0.5*inch, tm-1.2*inch-58), (rm, bm+inch))
    # -- Cabeceras
    rectangulo(c, (lm+0.5*inch, tm-1.2*inch-58),
                (lm+1.3*inch, tm-1.2*inch-85), 'BULTOS', 'centro')
    rectangulo(c, (lm+1.3*inch, tm-1.2*inch-58),
                (lm+2.4*inch, tm-1.2*inch-85), 'CÓDIGO', 'centro')
    rectangulo(c, (lm+2.4*inch, tm-1.2*inch-58),
                (rm-1.8*inch, tm-1.2*inch-85), 'DESCRIPCIÓN', 'centro')
    rectangulo(c, (rm-1.8*inch, tm-1.2*inch-58), (rm-inch, tm-1.2*inch-85),
                'SERVIDA')
    ### UGLY HACK (buscar una función que pinte varias líneas
    c.drawCentredString((rm-1.8*inch+rm-1*inch)/2, tm-1.2*inch-70,
                        escribe('CANTIDAD'))
    rectangulo(c, (rm-inch, tm-1.2*inch-58), (rm, tm-1.2*inch-85),
                'Nº PEDIDO', 'centro')

    # -- Columnas de datos
    rectangulo(c, (lm+0.5*inch, tm-1.2*inch-85), (lm+1.3*inch, bm+inch+98))
    if composan:
        c.setFillColorRGB(1, 1, 0.9)
    else:
        c.setFillColorRGB(0.9, 1, 0.9)
    c.rect(lm+1.3*inch, tm-1.2*inch-85, 1.1*inch, bm+inch+98-tm+1.2*inch+85,
           fill=1)
    c.rect(rm-1.8*inch, tm-1.2*inch-85, 0.8*inch, bm-tm+2.2*inch+183, fill=1)
    c.setFillColorRGB(0, 0, 0)

    rectangulo(c, (lm+2.4*inch, tm-1.2*inch-85), (rm-1.8*inch, bm+inch+98))
    rectangulo(c, (rm-inch, tm-1.2*inch-85), (rm, bm+inch+98))

    # DATA
    linea = tm-2.55*inch
    xbulto = lm+1.3*inch-4
    xcodigo = lm+1.8*inch+4
    xdescripcion = lm+2.4*inch+3
    xcantidad = rm-inch-4
    xpedido = rm-0.5*inch  # @UnusedVariable
    if lineas != None:
        for l in lineas:
            c.drawRightString(xbulto, linea,
                              escribe(l['bulto']!=0 and l['bulto'] or "-"))
            c.drawCentredString(xcodigo, linea, escribe(l['codigo']))
            #c.drawString(xdescripcion, linea, escribe(l['descripcion']))
            lineas_agregadas = agregarFila(xdescripcion, linea,
                xdescripcion + 8 * cm, escribe(l['descripcion']), c,
                "Helvetica", 10)
            for i in range(lineas_agregadas - 1):  # @UnusedVariable
                linea = sigLinea(10)
            #c.drawRightString(xcantidad, linea,
            #                  escribe("%s %s" % (
            #                    utils.float2str(l['cantidad']), 
            #                    l['unidad'])))
            el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, 
                                    rm-1.8*inch, xcantidad,
                                    linea, 
                                    "%s %s" % (utils.float2str(l['cantidad']), 
                                               l['unidad']), 
                                    alineacion = 1)
            el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, rm-inch+2,
                                                rm - 2, linea, l['numped'])
            linea = sigLinea()

    # -- Observaciones
    rectangulo(c, (lm+0.5*inch, bm+inch+98), (rm, bm+inch+14))
    rectangulo(c, (lm+0.5*inch, bm+inch+98), (lm+2.1*inch, bm+inch+82),
                    'Observaciones:')
    # DATA
    if observaciones != None:
        # c.drawString(lm+0.5*inch+4, bm+1.9*inch, escribe(observaciones))
        agregarFila(lm+0.5*inch + 0.1*cm, bm+1.9*inch, rm - 0.1*cm,
            escribe(observaciones), c, "Helvetica", 10)

    # -- Transporte
    rectangulo(c, (lm+0.5*inch, bm+inch+14), (rm, bm+inch), 'TRANSPORTE:')
    # DATA
    if transporte != None:
        c.drawString(lm+1.7*inch, bm+inch+4, escribe(transporte))

    # Pie de albarán (Conforme transportista)
    c.setFont("Helvetica-Bold", 8)
    linea = bm+0.75*inch
    xtransportista = lm + 0.5*inch
    xalmacen = width/3 + 0.75*inch
    xdestino = 2*width/3 + 0.5*inch
    c.drawString(xtransportista, linea, escribe('CONFORME TRANSPORTISTA'))
    if composan:
        c.drawString(xalmacen, linea, escribe('CONFORME DESTINO'))
    else:
        c.drawString(xalmacen, linea, escribe('Vº Bº JEFE DE ALMACÉN'))
    c.drawString(xdestino, linea, escribe('CONFORME DESTINO'))
    linea = sigLinea()
    c.drawString(xtransportista, linea, escribe('Nombre:'))
    if composan:
        c.drawString(xalmacen, linea, escribe('Nombre:'))
    c.drawString(xdestino, linea, escribe('Nombre y apellidos:'))
    linea = sigLinea()
    c.drawString(xtransportista, linea, escribe('DNI:'))
    if composan:
        c.drawString(xalmacen, linea, escribe('DNI:'))
    linea = sigLinea()
    c.drawString(xtransportista, linea, escribe('Tfno. Contacto:'))
    if composan:
        c.drawString(xalmacen, linea, escribe('Tfno. Contacto:'))
    c.drawString(xdestino, linea, escribe('DNI:'))
    linea = sigLinea()
    c.drawString(xtransportista, linea, escribe('Matrícula:'))
    if composan:
        c.drawString(xalmacen, linea, escribe('Matrícula:'))
    linea = sigLinea()
    c.drawString(xtransportista, linea, escribe('FIRMA'))
    if composan:
        c.drawString(xalmacen, linea, escribe('FIRMA'))
    c.drawString(xdestino, linea, escribe('FIRMA'))

    # DATA
    linea = bm+0.75*inch
    linea = sigLinea()
    xconformeT = lm+1.45*inch
    if conformeT != None:
        c.drawString(xconformeT, linea, escribe(conformeT['nombre']))
        linea = sigLinea()
        c.drawString(xconformeT, linea, escribe(conformeT['dni']))
        linea = sigLinea()
        c.drawString(xconformeT, linea, escribe(conformeT['telf']))
        linea = sigLinea()
        c.drawString(xconformeT, linea, escribe(conformeT['matricula']))

    if composan and conformeD != None:
        linea = bm+0.75*inch
        linea = sigLinea()
        xconformeD = width/2+2*inch
        c.drawString(xconformeD, linea, escribe(conformeD['nombre']))
        linea = sigLinea()
        c.drawString(xconformeD, linea, escribe(conformeD['dni']))
        linea = sigLinea()
        c.drawString(xconformeD, linea, escribe(conformeD['telf']))
        linea = sigLinea()
        c.drawString(xconformeD, linea, escribe(conformeD['matricula']))




    # Nota de margen
    c.rotate(90)
    c.setFont("Helvetica", 7)
    if composan:
        c.drawCentredString(height/2, -lm-32,
                            escribe(datos_empresa.regalbaran2))
    else:
        c.drawCentredString(height/2, -lm-32,
                            escribe(datos_empresa.registroMercantil))


    # Salvamos la página
    c.showPage()
    # Salvamos el documento
    c.save()

    return nomarchivo


def albaranValorado(cliente,
                    envio,
                    general,
                    lineas,
                    observaciones,
                    destino,
                    transporte,
                    conformeT, 
                    valorar_con_iva = True):
    """
    Con los datos de entrada genera el albarán.

    cliente --> datos del cliente (no los de envio), es un diccionario con:
        - 'nombre'
        - 'direccion'
        - 'cp'
        - 'localidad'
        - 'provincia'
        - 'pais'
        ' 'telf'

    envio --> datos que se ven en el sobre, es un diccionario con:
        - 'nombre'
        - 'direccion'
        - 'cp'
        - 'localidad'
        - 'provincia'
        - 'pais'
        - 'telf'

    general --> datos de la cabecera del albarán, diccionario con:
        - 'albnum' Número de albarán
        - 'fecha'
        - 'exp' Expedido en
        - 'clinum' Número de cliente
        - 'pednum' Número de pedido
        - 'numref' Número de referencia
        ' 'sref' MIRAR Viene en el albarán como S/REFERENCIA

    lineas --> datos del cuerpo del albarán, es una lista (un elemento
    por línea) de diccionarios con:
        - 'bultos'
        - 'codigo' //Debe soportar 13 digitos en la hoja
        - 'descripcion'
        - 'cantidad' Cantidad servida
        - 'numped' Número de pedido
        - 'precio unitario' // Precio unitario como cadena.
        - 'total' // Total de línea como cadena

    observaciones --> una cadena

    destino --> una cadena

    transporte --> una cadena

    conformeT --> datos del transportista para la firma de conforme. Es
    un diccionario con:
        - 'nombre'
        - 'dni'
        - 'telf'
        - 'matricula'
    """
    datos_empresa = pclases.DatosDeLaEmpresa.select()[0]

    # TODO: No se ha dado todavía el caso, pero si el albarán tiene más de una
    # página, falla estrepitosamente y se mete todo en la misma página.
    global linea, tm, lm, rm, bm
    x, y = lm, tm  # @UnusedVariable
    global linea
    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
                              "albaran_%s.pdf" % give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo)
    # La cabecera
    ruta_logo = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', datos_empresa.logo)
    im = Image.open(ruta_logo)
    ancho, alto = im.size
    nuevo_alto = 1.5 * inch
    ancho_proporcional = ancho * (nuevo_alto / alto)
    c.drawImage(ruta_logo,
                lm+0.5*inch,
                height - 1.5*inch,
                ancho_proporcional,
                nuevo_alto)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, tm+inch, escribe('ALBARÁN'))
    if datos_empresa.bvqi:
        c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', datos_empresa.logoiso1),
                    rm-1.75*inch,
                    tm+0.65*inch,
                    width = 119,
                    height = 65)
        c.setFont("Helvetica", 6)
        c.drawCentredString(rm-0.94*inch, tm+0.66*inch, escribe('Geotextiles CE 1035-CPD-ES033858'))
        c.drawCentredString(rm-0.94*inch, tm+0.56*inch, escribe('Fibra CE 1035-CPD-9003712'))
    c.setFont("Helvetica", 8)
    linea = height-15
    if datos_empresa.direccion != datos_empresa.dirfacturacion:
        if not datos_empresa.esSociedad:
            c.drawString(width/2-inch,
                         linea,
                         escribe(datos_empresa.nombreContacto))
            c.drawString(width-2.5*inch, linea, escribe(datos_empresa.nombre))
        else:
            c.drawString(width/2-inch, linea, escribe('DOMICILIO SOCIAL'))
            c.drawString(width-2.5*inch, linea, escribe('FÁBRICA'))
        linea -= 10
        c.drawString(width/2 - inch,
                     linea,
                     escribe(datos_empresa.dirfacturacion))
        c.drawString(width - 2.5*inch,
                     linea,
                     escribe(datos_empresa.direccion))
        linea -= 10
        c.drawString(width/2-inch,
                     linea,
                     escribe('%s %s%s, %s' % (
                        datos_empresa.cpfacturacion,
                        datos_empresa.ciudadfacturacion,
                        datos_empresa.provinciafacturacion !=
                            datos_empresa.ciudadfacturacion
                            and " (%s)" % (datos_empresa.provinciafacturacion)
                            or "",
                        datos_empresa.paisfacturacion)
                        )
                     )
        c.drawString(width-2.5*inch,
                     linea,
                     escribe('%s %s%s, %s' % (
                        datos_empresa.cp,
                        datos_empresa.ciudad,
                        datos_empresa.provincia !=
                            datos_empresa.ciudad
                            and " (%s)" % (datos_empresa.provincia) or "",
                        datos_empresa.pais)
                        )
                     )
        linea -= 10
        c.drawString(width/2-inch,
                     linea,
                     escribe('Telf: %s' % (datos_empresa.telefonofacturacion)))
        c.drawString(width-2.5*inch,
                     linea,
                     escribe('Telf: %s' % (datos_empresa.telefono)))
        linea -= 10
        if datos_empresa.faxfacturacion:
            c.drawString(width/2-inch,
                         linea,
                         escribe('Fax: %s' % (datos_empresa.faxfacturacion)))
        if datos_empresa.fax:
            c.drawString(width-2.5*inch,
                         linea,
                         escribe('Fax: %s' % (datos_empresa.fax)))
    else:
        c.drawString(width-2.5*inch, linea, escribe('DIRECCIÓN'))
        linea -= 10
        c.drawString(width-2.5*inch, linea, escribe(datos_empresa.direccion))
        linea -= 10
        c.drawString(width-2.5*inch,
                     linea,
                     escribe('%s %s%s, %s' % (
                        datos_empresa.cp,
                        datos_empresa.ciudad,
                        datos_empresa.provincia !=
                            datos_empresa.ciudad
                            and " (%s)" % (datos_empresa.provincia) or "",
                        datos_empresa.pais)))
        linea -= 10
        c.drawString(width-2.5*inch,
                     linea,
                     escribe('Telf: %s' % (datos_empresa.telefono)))
        linea -= 10
        c.drawString(width-2.5*inch,
                     linea,
                     escribe('Fax: %s' % (datos_empresa.fax)))
    # Los cuadros de datos del cliente y datos de envío
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.9, 1, 0.9)
    c.rect(lm+0.5*inch, tm+0.5*inch, 2.9*inch, -1.5*inch, fill=1)
    c.setFillColorRGB(0, 0, 0)
    rectangulo(c, (width/2, tm+0.5*inch), (rm, tm-inch))
    c.drawString(lm+0.5*inch, tm+0.5*inch+5, 'DATOS CLIENTE')
    c.drawString(width/2, tm+0.5*inch+5, 'DATOS ENVIO')
    ### DATA
    if cliente != None:
        linea = tm+0.5*inch-25
        xcliente = lm+0.5*inch+4
        lineas_agregadas = agregarFila(xcliente,
                                       linea,
                                       (width/2+3) - 0.8*cm,
                                       escribe(cliente["nombre"]),
                                       c,
                                       "Helvetica",
                                       10)
        for linea_agregada in range(lineas_agregadas):  # @UnusedVariable
            linea = sigLinea()
        el_encogedor_de_fuentes_de_doraemon(c,
                                            "Helvetica",
                                            10,
                                            xcliente,
                                            (width/2+3) - 0.8*cm,
                                            linea,
                                            cliente['direccion'])
        linea = sigLinea()
        c.drawString(xcliente, linea, escribe(cliente['provincia']))
        linea = sigLinea()
        if cliente['cp']:
            c.drawString(xcliente,
                         linea,
                         escribe("%s, %s" % (cliente['cp'],
                                             cliente['ciudad'])))
        else:
            c.drawString(xcliente, linea, escribe("%s" % (cliente['ciudad'])))
        linea = sigLinea()
        c.drawString(xcliente, linea, escribe(cliente['pais']))
        linea = sigLinea()

    if envio != None:
        #linea = tm+0.5*inch-30
        linea = tm+0.5*inch-25
        lineas_agregadas = agregarFila(width/2+3,
                                       linea,
                                       width - 0.8 * cm,
                                       escribe(envio["nombre"]),
                                       c,
                                       "Helvetica",
                                       10)
        for linea_agregada in range(lineas_agregadas):  # @UnusedVariable
            linea = sigLinea()
        el_encogedor_de_fuentes_de_doraemon(c,
                                            "Helvetica",
                                            10,
                                            width/2+3,
                                            rm,
                                            linea,
                                            envio['direccion'])
        linea = sigLinea()
        c.drawString(width/2+3,
                     linea,
                     escribe(envio['cp']+' '+envio['localidad']))
        linea = sigLinea()
        c.drawString(width/2+3, linea, escribe(envio['pais']))
        linea = sigLinea()
        c.drawString(width/2+3, linea, escribe(envio['telefono']))
    # Datos generales
    # (Esquina superior izquierda x = lm+0.5*inch, y = tm-1.2*inch)
    rectangulo(c,
               (lm+0.5*inch, tm-1.2*inch),
               (width/2, tm-1.2*inch-16),
               'ALBARÁN Nº:')
    rectangulo(c,
               (width/2, tm-1.2*inch),
               (width/2+1.5*inch, tm-1.2*inch-16),
               'FECHA:')
    rectangulo(c,
               (width/2+1.5*inch, tm-1.2*inch),
               (rm, tm-1.2*inch-16),
               'EXPEDIDO EN:')
    rectangulo(c,
               (lm+0.5*inch, tm-1.2*inch-16),
               (width/2 - inch, tm-1.2*inch-32),
               'Nº CLIENTE:')
    rectangulo(c,
               (width/2 - inch, tm-1.2*inch-16),
               (width/2+1.5*inch, tm-1.2*inch-32),
               'Nº PEDIDO:')
    rectangulo(c,
               (width/2+1.5*inch, tm-1.2*inch-16),
               (rm, tm-1.2*inch-32),
               'Nº REFERENCIA:')
    rectangulo(c,
               (lm+0.5*inch, tm-1.2*inch-32),
               (rm, tm-1.2*inch-48),
               'S/REFERENCIA:')
    # DATA
    linea = tm-1.2*inch-12
    c.drawRightString(width/2-4, linea, escribe(general['albnum']))
    c.drawRightString(width/2+1.5*inch-4, linea, escribe(general['fecha']))
    c.drawRightString(rm-4, linea, escribe(general['exp']))
    linea = sigLinea()
    c.drawRightString(width/2-inch-4, linea, escribe(general['numcli']))
    xnumpedizq = width/2 - inch + c.stringWidth("Nº PEDIDO:", "Helvetica", 10)
    xnumpedder = width/2+1.5*inch-4
    el_encogedor_de_fuentes_de_doraemon(c,
                                        "Helvetica",
                                        10,
                                        xnumpedizq,
                                        xnumpedder,
                                        linea,
                                        general['numped'],
                                        alineacion = 1)
    c.drawRightString(rm-4, linea, escribe(general['numref']))
    linea = sigLinea()
    c.drawString(lm+1.8*inch, linea, escribe(general['sref']))

    # El cuerpo
    # -- Cuadro global
    rectangulo(c, (lm+0.5*inch, tm - 1.2*inch - 58), (rm, bm+inch))
    # XXX
    xcantidad1, xcantidad2 = lm + 0.5*inch, lm + 1.2*inch
    xcodigo1, xcodigo2 = xcantidad2, xcantidad2 + 1.1*inch
    xdescripcion1, xdescripcion2 = xcodigo2, xcodigo2 + 2.8*inch
    xprecio1, xprecio2 = xdescripcion2, xdescripcion2 + 0.8*inch
    xtotal1, xtotal2 = xprecio2, xprecio2 + 0.9*inch
    xpedido1, xpedido2 = xtotal2, rm
    # -- Cabeceras
    ### UGLY HACK (buscar una función que pinte varias líneas)
    c.drawCentredString((xcantidad1 + xcantidad2) / 2,
                        tm - 1.2*inch - 70,
                        escribe('CANTIDAD'))
    rectangulo(c,
               (xcantidad1, tm-1.2*inch-58),
               (xcantidad2, tm-1.2*inch-85),
               'SERVIDA',
               'centro')
    rectangulo(c,
               (xcodigo1, tm-1.2*inch-58),
               (xcodigo2, tm-1.2*inch-85),
               'CÓDIGO',
               'centro')
    rectangulo(c,
               (xdescripcion1, tm-1.2*inch-58),
               (xdescripcion2, tm-1.2*inch-85),
               'DESCRIPCIÓN',
               'centro')
    rectangulo(c,
               (xprecio1, tm-1.2*inch-58),
               (xprecio2, tm-1.2*inch-85),
               'PRECIO/U')
    if valorar_con_iva:
        cab_total_linea = 'TOTAL c/IVA'
    else:
        cab_total_linea = "TOTAL s/IVA"
    rectangulo(c,
               (xtotal1, tm - 1.2*inch - 58),
               (xtotal2, tm - 1.2*inch - 85),
               cab_total_linea,
               'centro')
    rectangulo(c,
               (xpedido1, tm - 1.2*inch - 58),
               (xpedido2, tm - 1.2*inch - 85),
               'Nº PEDIDO',
               'centro')

    # -- Columnas de datos
    rectangulo(c,
               (xcantidad1, tm - 1.2*inch - 85),
               (xcantidad2, bm + inch + 98))
    rectangulo(c,
               (xdescripcion1, tm - 1.2*inch - 85),
               (xdescripcion2, bm + inch + 98))
    rectangulo(c,
               (xtotal1, tm - 1.2*inch - 85),
               (xtotal2, bm + inch + 98))
    c.setFillColorRGB(0.9, 1, 0.9)
    c.rect(xcodigo1,
           tm - 1.2*inch - 85,
           xcodigo2 - xcodigo1,
           bm - tm + 2.2*inch + 183,
           fill=1)
    c.rect(xprecio1,
           tm - 1.2*inch - 85,
           xprecio2 - xprecio1,
           bm - tm + 2.2*inch + 183,
           fill=1)
    c.rect(xpedido1,
           tm - 1.2*inch - 85,
           xpedido2 - xpedido1,
           bm - tm + 2.2*inch + 183,
           fill=1)
    c.setFillColorRGB(0, 0, 0)

    # XXX
    xcantidad = xcantidad2 - 4
    xcodigo = (xcodigo1 + xcodigo2) / 2
    xdescripcion = xdescripcion1 + 4
    xprecio = xprecio2 - 4
    xtotal = xtotal2 -4
    # DATA
    linea = tm - 2.55*inch
    if lineas != None:
        for l in lineas:
            if isinstance(l['cantidad'], str):
                cantidad = escribe(l['cantidad'])
            else:
                cantidad = escribe(utils.float2str(l['cantidad'],
                                   autodec=True))
            c.drawRightString(xcantidad,
                              linea,
                              cantidad)
            c.drawCentredString(xcodigo, linea, escribe(l['codigo']))
            lineas_agregadas = agregarFila(xdescripcion,
                                           linea,
                                           xdescripcion2,
                                           escribe(l['descripcion']),
                                           c,
                                           "Helvetica",
                                           10)
            for i in range(lineas_agregadas - 1):  # @UnusedVariable
                linea = sigLinea(10)
            precio_u = l['precio unitario']
            if not valorar_con_iva:
                precio_u = utils.float2str(utils._float(precio_u) / 1.16, 2)
            c.drawRightString(xprecio,
                              linea,
                              escribe(precio_u))
            total_linea = l['total']
            if not valorar_con_iva:
                total_linea = utils.float2str(utils._float(total_linea) / 1.16, 2)
            c.drawRightString(xtotal,
                              linea,
                              escribe(total_linea))
            el_encogedor_de_fuentes_de_doraemon(c,
                                                "Helvetica",
                                                10,
                                                xpedido1,
                                                xpedido2,
                                                linea,
                                                l['numped'],
                                                alineacion = 0)
            linea = sigLinea()

    # -- Observaciones
    rectangulo(c, (lm+0.5*inch, bm+inch+98), (rm, bm+inch+14))
    rectangulo(c,
               (lm + 0.5*inch, bm + inch + 98),
               (lm + 2.1*inch, bm + inch + 82),
               'Observaciones:')
    # DATA
    if observaciones != None:
        agregarFila(lm + 0.5*inch + 0.1*cm,
                    bm + 1.9*inch,
                    rm - 0.1*cm,
                    escribe(observaciones),
                    c,
                    "Helvetica",
                    10)

    # -- Transporte
    rectangulo(c,
               (lm + 0.5*inch, bm+inch+14),
               (rm, bm + inch),
               'TRANSPORTE:')
    # DATA
    if transporte != None:
        c.drawString(lm + 1.7*inch, bm + inch + 4, escribe(transporte))

    # Pie de albarán (Conforme transportista)
    c.setFont("Helvetica-Bold", 10)
    linea = bm + 0.75*inch
    c.drawString(lm + 0.5*inch,
                 linea,
                 escribe('CONFORME TRANSPORTISTA'))
    c.drawString(width/2 + 0.5*inch, linea, escribe('Vº Bº JEFE DE ALMACÉN'))
    linea = sigLinea()
    c.drawString(lm + 0.5*inch, linea, escribe('Nombre:'))
    linea = sigLinea()
    c.drawString(lm + 0.5*inch, linea, escribe('DNI:'))
    linea = sigLinea()
    c.drawString(lm + 0.5*inch, linea, escribe('Tfno. Contacto:'))
    linea = sigLinea()
    c.drawString(lm + 0.5*inch, linea, escribe('Matrícula:'))
    linea = sigLinea()
    c.drawString(lm + 0.5*inch, linea, escribe('FIRMA'))

    # DATA
    linea = bm + 0.75*inch
    linea = sigLinea()
    xconformeT = lm + 2*inch
    if conformeT != None:
        c.drawString(xconformeT, linea, escribe(conformeT['nombre']))
        linea = sigLinea()
        c.drawString(xconformeT, linea, escribe(conformeT['dni']))
        linea = sigLinea()
        c.drawString(xconformeT, linea, escribe(conformeT['telf']))
        linea = sigLinea()
        c.drawString(xconformeT, linea, escribe(conformeT['matricula']))

    # Nota de margen
    c.rotate(90)
    c.setFont("Helvetica", 7)
    c.drawCentredString(height/2,
                        -lm - 32,
                        escribe(datos_empresa.registroMercantil))

    # Salvamos la página
    c.showPage()
    # Salvamos el documento
    c.save()

    return nomarchivo


################ Albaran de compra ########################

def albaranEntrada(general, lineas, observaciones):
    """
    Con los datos de entrada genera el albarán.

    @params

    general --> datos de la cabecera del albarán, diccionario con:
        - 'albnum' Número de albarán
        - 'fecha'
        - 'proveedor' --> una cadena con los proveedores separados por comas:
        - 'pednum' Número de los pedidos asociados al albarán

    lineas --> datos del cuerpo del albarán, es una lista (un elemento
    por línea) de diccionarios con:
        - 'codigo' //Debe soportar 13 digitos en la hoja
        - 'descripcion'
        - 'cantidad' Cantidad servida
        - 'numped' Pedido al que está asociada la línea

    observaciones --> una cadena
    """

    datos_empresa = pclases.DatosDeLaEmpresa.select()[0]

    global linea, tm, lm, rm, bm
    x, y = lm, tm  # @UnusedVariable
    global linea

    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
                              "albaranCompra_%s.pdf" % give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo)
    # La cabecera
    c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', datos_empresa.logo),
                lm+0.5*inch, height - 1.5*inch, 1.5*inch, 1.5*inch)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, tm+inch, escribe('ALBARÁN DE ENTRADA'))
    fuente = "Helvetica"
    tamano = 8
    if datos_empresa.bvqi:
        c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', datos_empresa.logoiso1),
                    rm-1.75*inch, tm+0.65*inch, width = 119, height = 65)
        c.setFont(fuente, tamano - 2)
        c.drawCentredString(rm-0.94*inch, tm+0.66*inch, escribe('Geotextiles CE 1035-CPD-ES033858'))
        c.drawCentredString(rm-0.94*inch, tm+0.56*inch, escribe('Fibra CE 1035-CPD-9003712'))
    c.setFont(fuente, tamano)
    linea = height-15
    if datos_empresa.direccion != datos_empresa.dirfacturacion:
        if datos_empresa.esSociedad:
            c.drawString(width/2-inch, linea, escribe('DOMICILIO SOCIAL'))
            c.drawString(width-2.5*inch, linea, escribe('FÁBRICA'))
        else:
            c.drawString(width/2-inch, linea, escribe('DIRECCIÓN FISCAL'))
            c.drawString(width-2.5*inch, linea, escribe('TIENDA'))
        linea -= 10
        c.drawString(width/2-inch, linea,
                     escribe(datos_empresa.dirfacturacion))
        c.drawString(width-2.5*inch, linea, escribe(datos_empresa.direccion))
        linea -= 10
        c.drawString(width/2-inch, linea, escribe('%s %s%s, %s' % (
            datos_empresa.cpfacturacion,
            datos_empresa.ciudadfacturacion,
            datos_empresa.provinciafacturacion
                != datos_empresa.ciudadfacturacion
                and " (%s)" % (datos_empresa.provinciafacturacion) or "",
            datos_empresa.paisfacturacion)))
        c.drawString(width-2.5*inch, linea, escribe('%s %s%s, %s' % (
            datos_empresa.cp,
            datos_empresa.ciudad,
            datos_empresa.provincia != datos_empresa.ciudad
                and " (%s)" % (datos_empresa.provincia) or "",
            datos_empresa.pais)))
        linea -= 10
        c.drawString(width/2-inch, linea,
            escribe('Telf: %s' % (datos_empresa.telefonofacturacion)))
        c.drawString(width-2.5*inch, linea,
            escribe('Telf: %s' % (datos_empresa.telefono)))
        linea -= 10
        c.drawString(width/2-inch, linea,
            escribe('Fax: %s' % (datos_empresa.faxfacturacion)))
        c.drawString(width-2.5*inch, linea,
            escribe('Fax: %s' % (datos_empresa.fax)))
    else:
        c.drawString(width-2.5*inch, linea, escribe('DIRECCIÓN'))
        linea -= 10
        c.drawString(width-2.5*inch, linea, escribe(datos_empresa.direccion))
        linea -= 10
        c.drawString(width-2.5*inch, linea, escribe('%s %s%s, %s' % (
            datos_empresa.cp,
            datos_empresa.ciudad,
            datos_empresa.provincia != datos_empresa.ciudad
                and " (%s)" % (datos_empresa.provincia) or "",
            datos_empresa.pais)))
        linea -= 10
        c.drawString(width-2.5*inch, linea,
            escribe('Telf: %s' % (datos_empresa.telefono)))
        linea -= 10
        c.drawString(width-2.5*inch, linea,
            escribe('Fax: %s' % (datos_empresa.fax)))

    # Datos generales (Esquina superior izquierda x=lm+0.5*inch, y=tm-1.2*inch)
    linea = tm + 0.2*inch
    rectangulo(c, (lm+0.5*inch, linea), (rm, linea-0.8*inch))
    linea = linea - 12
    # DATA
    xCuadro = lm + 0.6*inch
    c.drawString(xCuadro, linea, escribe('Nº ALBARÁN: '+general['albnum']))
    linea -= 12
    c.drawString(xCuadro, linea, escribe('PROVEEDOR: '+general['proveedor']))
    linea -= 12
    c.drawString(xCuadro, linea, escribe('FECHA: '+general['fecha']))
    linea -= 12
    c.drawString(xCuadro, linea,
                 escribe('PEDIDOS RELACIONADOS: '+general['pednum']))

    # El cuerpo
    # -- Cuadro global
    linea = tm - 1 * inch
    lineaAbajo = linea - 16
    finDatos = bm + 1.8*inch
    rectangulo(c, (lm+0.5*inch, linea), (rm, finDatos))
    # -- Cabeceras
    rectangulo(c, (lm+0.5*inch, linea), (lm+1.5*inch, lineaAbajo),
                'CÓDIGO', 'centro')
    rectangulo(c, (lm+1.5*inch, linea), (rm-1.8*inch, lineaAbajo),
                'DESCRIPCIÓN', 'centro')
    rectangulo(c, (rm-1.8*inch, linea), (rm-inch, lineaAbajo), 'CANTIDAD')
    rectangulo(c, (rm-inch, linea), (rm, lineaAbajo), 'Nº PEDIDO', 'centro')

    # -- Columnas de datos

    rectangulo(c, (lm+0.5*inch, linea), (lm+1.5*inch, finDatos))
    rectangulo(c, (lm+1.5*inch, linea), (rm-1.8*inch, finDatos))
    rectangulo(c, (rm-1.8*inch, linea), (rm-inch, finDatos))
    rectangulo(c, (rm-inch, linea), (rm, finDatos))

    # DATA
    linea = tm-1.4*inch
    xcodigo = lm+0.95*inch+4
    xdescripcion = lm+1.55*inch+3
    topeDescripcion = rm - 1.77*inch
    xcantidad = rm-inch-4
    xpedido = rm-0.5*inch
    if lineas != None:
        for l in lineas:
            c.drawCentredString(xcodigo, linea, escribe(l['codigo']))
            saltos = agregarFila(xdescripcion, linea, topeDescripcion,
                                 l['descripcion'], c, fuente, tamano)
            c.drawRightString(xcantidad, linea, escribe(l['cantidad']))
            c.drawCentredString(xpedido, linea, escribe(l['numped']))
            for i in range(saltos):  # @UnusedVariable
                linea = sigLinea()

    # -- Observaciones
    rectangulo(c, (lm+0.5*inch, finDatos), (rm, finDatos - inch))
    rectangulo(c, (lm+0.5*inch, finDatos), (lm+1.6*inch, finDatos - 15),
                'OBSERVACIONES:')
    # DATA
    if observaciones != None:
        linea = finDatos -15
        agregarFila(lm+1.65*inch, linea, rm, observaciones, c, fuente, tamano)

    # Nota de margen
    c.rotate(90)
    c.setFont("Helvetica", 7)
    c.drawCentredString(height/2, -lm-32,
                        escribe(datos_empresa.registroMercantil))


    # Salvamos la página
    c.showPage()
    # Salvamos el documento
    c.save()
    return nomarchivo



################ Pedido de compra ########################

def pedidoCompra(general, proveedor, lineas, entregas, observaciones,
                 formapago, direntrega0, direntrega1, direntrega2, 
                 responsable0, responsable1, portes0, portes1, 
                 mostrar_precios = True, observaciones0 = "", 
                 observaciones1 = ""):
    """
    Con los datos de entrada genera el impreso.

    @params

    general --> datos de la cabecera del albarán, diccionario con:
        - 'pednum' Número de pedido
        - 'proveedor'
        - 'fecha'
        - 'iva'
        - 'descuento'
        - 'subtotal'
        - 'totalIVA'
        - 'totalDescuento
        - 'total'

    lineas --> datos del cuerpo del albarán, es una lista (un elemento
    por línea) de diccionarios con:
        - 'codigo' //Debe soportar 13 digitos en la hoja
        - 'descripcion'
        - 'cantidad' Cantidad servida

    observaciones --> una cadena
    mostrar_precios --> Si False, oculta la columna de los precios.
    """

    datos_empresa = pclases.DatosDeLaEmpresa.select()[0]

    global linea, tm, lm, rm, bm
    x, y = lm, tm  # @UnusedVariable
    global linea

    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
                              "pedidoCompra_%s.pdf" % give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo)
    # La cabecera
    c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', datos_empresa.logo),
                lm+0.5*inch, height - 1.5*inch, 1.5*inch, 1.5*inch)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, tm+inch, escribe('PEDIDO DE COMPRA'))
    fuente = "Helvetica"
    tamano = 8
    if datos_empresa.bvqi:
        c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', datos_empresa.logoiso1),
                    rm-1.75*inch, tm+0.65*inch, width = 119, height = 65)
        c.setFont(fuente, tamano - 2)
        c.drawCentredString(rm-0.94*inch, tm+0.66*inch, escribe('Geotextiles CE 1035-CPD-ES033858'))
        c.drawCentredString(rm-0.94*inch, tm+0.56*inch, escribe('Fibra CE 1035-CPD-9003712'))
    c.setFont(fuente, tamano)
    linea = height-15
    if datos_empresa.direccion != datos_empresa.dirfacturacion:
        posx_dirfiscal = (width / 2) - (1.5 * inch)
        if datos_empresa.esSociedad:
            c.drawString(posx_dirfiscal, linea, escribe('DOMICILIO SOCIAL'))
            c.drawString(width-2.5*inch, linea, escribe('FÁBRICA'))
        else:
            c.drawString(posx_dirfiscal, linea, escribe('DIRECCIÓN FISCAL'))
            c.drawString(width-2.5*inch, linea, escribe('TIENDA'))
        linea -= 10
        c.drawString(posx_dirfiscal, linea,
                     escribe(datos_empresa.dirfacturacion))
        c.drawString(width-2.5*inch, linea, escribe(datos_empresa.direccion))
        linea -= 10
        c.drawString(posx_dirfiscal, linea, escribe('%s %s%s, %s' % (
            datos_empresa.cpfacturacion,
            datos_empresa.ciudadfacturacion,
            datos_empresa.provinciafacturacion
                != datos_empresa.ciudadfacturacion
                and " (%s)" % (datos_empresa.provinciafacturacion) or "",
            datos_empresa.paisfacturacion)))
        c.drawString(width-2.5*inch, linea, escribe('%s %s%s, %s' % (
            datos_empresa.cp,
            datos_empresa.ciudad,
            datos_empresa.provincia != datos_empresa.ciudad
                and " (%s)" % (datos_empresa.provincia) or "",
            datos_empresa.pais)))
        linea -= 10
        c.drawString(posx_dirfiscal, linea,
            escribe('Tlf.: %s' % (datos_empresa.telefonofacturacion)))
        c.drawString(width-2.5*inch, linea,
            escribe('Tlf.: %s' % (datos_empresa.telefono)))
        linea -= 10
        c.drawString(posx_dirfiscal, linea,
            escribe('Fax: %s' % (datos_empresa.faxfacturacion)))
        c.drawString(width-2.5*inch, linea,
            escribe('Fax: %s' % (datos_empresa.fax)))
    else:
        c.drawString(width-2.5*inch, linea, escribe('DIRECCIÓN'))
        linea -= 10
        c.drawString(width-2.5*inch, linea, escribe(datos_empresa.direccion))
        linea -= 10
        c.drawString(width-2.5*inch, linea, escribe('%s %s%s, %s' % (
            datos_empresa.cp,
            datos_empresa.ciudad,
            datos_empresa.provincia != datos_empresa.ciudad
                and " (%s)" % (datos_empresa.provincia) or "",
            datos_empresa.pais)))
        linea -= 10
        c.drawString(width-2.5*inch, linea,
            escribe('Tlf.: %s' % (datos_empresa.telefono)))
        linea -= 10
        c.drawString(width-2.5*inch, linea,
            escribe('Fax: %s' % (datos_empresa.fax)))
    linea -= 0.6 * inch
    c.setFont(fuente, 6)
    c.drawString(lm+0.4*inch, linea,
        escribe('C.I.F. / VAT NUMBER:ES     %s' % (datos_empresa.cif)))
    c.setFont(fuente, tamano)


    # Datos generales (Esquina superior izquierda x=lm+0.5*inch, y=tm-1.2*inch)
    linea = tm + 0.2*inch
    # Cuadro con datos del pedido
    izq = lm + 0.5*inch
    der = lm + 2.2*inch
    arr = linea
    aba = linea - 1.1*inch
    aux = linea - 0.2*inch
    xCuadro = lm + 0.6*inch
    rectangulo(c, (izq, arr), (der, aba))
    rectangulo(c, (izq, arr), (der, aux), escribe('PEDIDO / PURCHASE ORDER'))
    linea = sigLinea()
    linea = sigLinea()
    c.drawString(xCuadro, linea, escribe('Fecha / Date: '+general['fecha']))
    linea = sigLinea()
    c.drawString(xCuadro, linea, escribe('Nº: '+general['pednum']))
    linea = sigLinea()
    c.drawString(xCuadro, linea, escribe('Moneda / Currency:      EUR'))

    # Cuadro con los datos del proveedor
    izq = lm + 2.3*inch
    der = rm
    xCuadro = izq + 4
    xFax = xCuadro + 2.5*inch
    xCif = xFax + 1.5*inch
    rectangulo(c, (izq, arr), (der, aba))
    rectangulo(c, (izq, arr), (der, aux),
                escribe('DIRECCION PROVEEDOR / SUPPLIER ADDRESS'))
    linea = arr
    linea = sigLinea()
    linea = sigLinea(12)
    c.drawString(xCuadro, linea, escribe('EMPRESA: '+proveedor['nombre']))
    linea = sigLinea(12)
    c.drawString(xCuadro, linea, escribe('DIRECCIÓN: '+proveedor['direccion']))
    linea = sigLinea(12)
    c.drawString(xCuadro + c.stringWidth('DIRECCIÓN: ', fuente, tamano),
                 linea, escribe(proveedor['direccion2']))
    linea = sigLinea(12)
    c.drawString(xCuadro, linea, escribe('TELEFONO: '+proveedor['telefono']))
    c.drawString(xFax, linea, escribe('FAX: '+proveedor['fax']))
    c.drawString(xCif, linea, escribe('C.I.F: '+proveedor['cif']))
    linea = sigLinea(12)
    if proveedor['contacto']:
        c.drawString(xCuadro, linea,
                     escribe('Contacto: '+proveedor['contacto']))
    if proveedor['correoe'] != "" and proveedor['correoe'] != None:
        from reportlab.lib import colors
        c.saveState()
        c.setFont("Courier", 8)
        c.setFillColor(colors.blue)
        c.drawRightString(rm - 0.5 * cm, linea, proveedor['correoe'])
        ancho = c.stringWidth(proveedor['correoe'], "Courier", 8)
        rect = (rm - 0.6 * cm - ancho, linea + 8,
                rm - 0.4 * cm, linea - 2)   # x1, y1, x2, y2
        c.linkURL("mailto:%s" % (proveedor['correoe']), rect)
        c.restoreState()


    # El cuerpo
    # -- Cuadro global
    linea = tm - 1 * inch
    lineaAbajo = linea - 16
    finDatos = bm + 2.75*inch
    rectangulo(c, (lm+0.5*inch, linea), (rm, finDatos))
    # -- Cabeceras
    rectangulo(c, (lm+0.5*inch, linea), (lm+1.5*inch, lineaAbajo),
                'CÓDIGO', 'centro')
    xcantidad = rm - 2.2 * inch
    xprecio = rm - inch
    if not mostrar_precios:
        xcantidad, xprecio = xprecio - 1 * cm, rm
    rectangulo(c, (lm+1.5*inch, linea), (xcantidad, lineaAbajo),
                'DESCRIPCIÓN', 'centro')
    rectangulo(c, (xcantidad, linea), (xprecio, lineaAbajo), 'CANTIDAD',
                'centro')
    if mostrar_precios:
        rectangulo(c, (xprecio, linea), (rm, lineaAbajo), 'PRECIO', 'centro')

    # -- Columnas de datos

    rectangulo(c, (lm+0.5*inch, linea), (lm+1.5*inch, finDatos))
    rectangulo(c, (lm+1.5*inch, linea), (xcantidad, finDatos))
    rectangulo(c, (xcantidad, linea), (xprecio, finDatos))
    rectangulo(c, (xprecio, linea), (rm, finDatos))

    # DATA
    linea = tm-1.4*inch
    xcodigo = lm+0.95*inch+4
    xdescripcion = lm+1.55*inch+3
    topeDescripcion = xcantidad
    if lineas != None:
        for l in lineas:
            c.drawCentredString(xcodigo, linea, escribe(l['codigo']))
            saltos = agregarFila(xdescripcion, linea, topeDescripcion,
                                 l['descripcion'], c, fuente, tamano)
            cantidad = l['cantidad'].split()[0]
            unidad = " ".join(l['cantidad'].split()[1:])
            xcentroidecantidad = xcantidad + ((xprecio - xcantidad) * (3/5.0))
            c.drawRightString(xcentroidecantidad, linea, escribe(cantidad))
            c.saveState()
            c.setFont("Helvetica", 6)
            c.drawString(xcentroidecantidad + 0.1 * cm, linea, escribe(unidad))
            c.restoreState()

            if mostrar_precios:
                xcentroideprecio = xprecio + ((rm - 0.5*cm - xprecio)*(4/5.0))
                c.drawRightString(xcentroideprecio, linea,
                                  escribe("%s €" % (l['precio'])))
                if unidad and unidad != " ":
                    c.saveState()
                    c.setFont("Helvetica", 6)
                    c.drawString(xcentroideprecio + 0.05 * cm, linea,
                                 "/%s" % (escribe(unidad)))
                    c.restoreState()

            for i in range(saltos):
                linea = sigLinea()
            if l['entrega'] != None and l['entrega'].strip() != '':
                c.saveState()
                c.setFont("Times-Italic", 10)
                c.drawRightString(xcantidad - 0.1 * cm, linea,
                                  "ENTREGA: %s" % (escribe(l['entrega'])))
                linea = sigLinea()
                c.restoreState()
    if entregas != []:
        c.saveState()
        fuente = "Times-Italic"
        tamano = 10
        c.setFont(fuente, tamano)
        linea = sigLinea()
        for e in entregas:
            saltos = agregarFila(xdescripcion, linea, topeDescripcion,
                                 escribe(e), c, fuente, tamano)
            for i in xrange(saltos):
                linea = sigLinea()
        c.restoreState()

    # Texto de condiciones: [GINN-70]
    txt = "La factura de los materiales y/o servicios contenidos en este "\
          "pedido deberán estar en poder de %s en %s; %s - %s (%s, %s) antes "\
          "del día 10 del mes siguiente al del suministro. En caso contrario "\
          "el procedimiento de aceptación y pago de la factura se pospondrá "\
          "al mes siguiente." % (
            datos_empresa.nombre, 
            datos_empresa.direccion, 
            datos_empresa.cp, 
            datos_empresa.ciudad, 
            datos_empresa.provincia, 
            datos_empresa.pais)
    # TODO: Calcular en cuántas líneas tengo que dividir el texto para que 
    #       quepa en el ancho del folio.
    c.saveState()
    fuente, tamanno = "Helvetica-Oblique", 8    # "Times-Italic", 10
    c.setFont(fuente, tamanno)
    ancho_condiciones = c.stringWidth(txt, fuente, tamanno)
    ancho_max = rm - (lm+.5*inch)
    from math import ceil
    numlineas = int(ceil(ancho_condiciones / ancho_max))
    import textwrap
    txt = textwrap.wrap(txt, len(txt) / numlineas)
    for i in range(numlineas):
        c.drawCentredString((lm+.5*inch) + ((rm - (lm+0.5*inch))/2), 
                            finDatos - 0.4*cm - (i * (tamanno + 2)),
                            escribe(txt[i]))
    c.restoreState()

    # Dirección de entrega
    arr = bm + 2.2*inch
    aba = bm + 1.6*inch
    izq = lm + 0.5*inch
    der = width/2
    aux = arr - 0.2*inch
    xCuadro = izq + 4
    rectangulo(c, (izq, arr), (der, aba))
    rectangulo(c, (izq, arr), (der, aux),
                'Dirección de entrega / Delivery address')
    linea = aux
    linea = sigLinea(9)
    #c.drawString(xCuadro, linea, escribe(datos_empresa.nombre))
    c.drawString(xCuadro, linea, escribe(direntrega0))
    linea = sigLinea(9)
    #c.drawString(xCuadro, linea, escribe(datos_empresa.direccion))
    c.drawString(xCuadro, linea, escribe(direntrega1))
    linea = sigLinea(9)
    #c.drawString(xCuadro, linea, escribe("%s %s (%s), %s" % (datos_empresa.cp,
    #                                                datos_empresa.ciudad,
    #                                                datos_empresa.provincia,
    #                                                datos_empresa.pais)))
    c.drawString(xCuadro, linea, escribe(direntrega2))

    # Forma de pago
    arr = bm + 2.2*inch
    aba = bm + 1.6*inch
    izq = width/2 + 0.1*inch
    der = rm
    aux = arr - 0.2*inch
    xCuadro = izq + 4
    rectangulo(c, (izq, arr), (der, aba))
    rectangulo(c, (izq, arr), (der, aux), 'Forma de pago / Payment terms')
    linea = aux
    linea = sigLinea(9)
    c.drawString(xCuadro, linea, escribe(formapago))



    # Persona responsable
    arr = bm + 1.5*inch
    aba = bm + inch
    izq = lm + 0.5*inch
    der = width/2
    aux = arr - 0.2*inch
    xCuadro = izq + 4
    rectangulo(c, (izq, arr), (der, aba))
    rectangulo(c, (izq, arr), (der, aux),
                'Persona responsable / People in charge')
    linea = aux
    linea = sigLinea(9)
    #c.drawString(xCuadro, linea,
    #             escribe('%s  %s'%(datos_empresa.nombreResponsableCompras,
    #                               datos_empresa.telefonoResponsableCompras)))
    c.drawString(xCuadro, linea,
                 escribe(responsable0))
    linea = sigLinea(9)
    #c.drawString(xCuadro, linea,
    #             escribe('%s' % (datos_empresa.emailResponsableCompras)))
    c.drawString(xCuadro, linea,
                 escribe(responsable1))

    # Portes
    arr = bm + 1.5*inch
    aba = bm + inch
    izq = width/2 + 0.1*inch
    der = rm
    aux = arr - 0.2*inch
    xCuadro = izq + 4
    rectangulo(c, (izq, arr), (der, aba))
    rectangulo(c, (izq, arr), (der, aux), 'Portes / Freight')
    linea = aux
    linea = sigLinea(9)
    c.drawString(xCuadro, linea, escribe(portes0))
    c.drawString(xCuadro, linea-0.3*cm, escribe(portes1))
    #c.drawString(xCuadro, linea, escribe('PORTES PAGADOS.'))
    #if datos_empresa.direccion != datos_empresa.dirfacturacion:
    #    if datos_empresa.esSociedad:
    #        c.drawString(xCuadro, linea - 0.3 * cm,
    #                     escribe('ENTREGA EN NUESTRA FÁBRICA DE %s.' % (
    #                                datos_empresa.ciudad.upper())))
    #    else:
    #        c.drawString(xCuadro, linea - 0.3 * cm,
    #                     escribe('ENTREGA EN NUESTRA TIENDA DE %s.' % (
    #                                datos_empresa.ciudad.upper())))

    # Observaciones
    arr = bm + 0.9*inch
    aba = bm
    izq = lm + 0.5*inch
    der = rm
    aux = arr - 0.2*inch
    rectangulo(c, (izq, arr), (der, aba) )
    rectangulo(c, (izq, arr), (der, aux), escribe('Observaciones / Remarks:'))
    linea = aux - 0.5 * cm
    if observaciones0 != None:
        lineas_agregadas = agregarFila(izq + 0.1 * cm, linea, der, 
                                       escribe(observaciones0), c,
                                       fuente, tamano)
        for i in xrange(lineas_agregadas):
            linea = sigLinea()
    if observaciones1 != None:
        lineas_agregadas = agregarFila(izq + 0.1 * cm, linea, der, 
                                       escribe(observaciones1), c,
                                       fuente, tamano)
        for i in xrange(lineas_agregadas):
            linea = sigLinea()
    if observaciones != None:
        lineas_agregadas = agregarFila(izq + 0.1 * cm, linea, der, 
                                       escribe(observaciones), c,
                                       fuente, tamano)
        for i in xrange(lineas_agregadas):
            linea = sigLinea()

    # Despedida
    c.setFont("Helvetica", 8)
    linea = bm - 0.2*inch
    xCuadro = lm + 0.5*inch
    c.drawString(xCuadro, linea,
        escribe('Esperamos su acuse de recibo y les saludamos atentamente.'))
    linea = sigLinea(8)
    c.drawString(xCuadro, linea,
        escribe('Waiting for your acknoledgement. Yours faithfully.'))

    # Nota de margen
    c.rotate(90)
    c.setFont("Helvetica", 7)
    c.drawCentredString(height/2, -lm-32,
                        escribe(datos_empresa.registroMercantil))


    # Salvamos la página
    c.showPage()
    # Salvamos el documento
    c.save()
    return nomarchivo


def el_encogedor_de_fuentes_de_doraemon(canvas, fuente, tamannoini, xini,
                                        xfin, y, texto, alineacion = -1):
    """
    Comenzando por el tamaño inicial "tamannoini", encoge el texto
    hasta que quepa en los límites fijados y después lo escribe.
    Convierte el texto por si está en una codificación no soportada.
    Al finalizar, devuelve las propiedades de texto del canvas a
    su estado original y la fuente a su tamaño inicial.
    NO AVANZA LÍNEA.
    Si alineacion == -1: Alineación a la izquierda. Si 0, centrado y si 1, a
    la derecha.
    """
    # PLAN: No estaría mal pasar un tamaño mínimo de fuente, y si se alcanza o
    # se supera, cortar la línea con agregarFila y el último tamaño de fuente
    # válido. Claro que entonces habría que devolver también las líneas
    # avanzadas, etc...
    canvas.saveState()
    size = tamannoini
    texto = escribe(texto)
    while canvas.stringWidth(texto, fuente, size) > (xfin - xini) and size > 4:
        size -= 1
    canvas.setFont(fuente, size)
    if alineacion == -1:
        canvas.drawString(xini, y, texto)
    elif alineacion == 1:
        canvas.drawRightString(xfin, y, texto)
    elif alineacion == 0:
        canvas.drawCentredString((xfin + xini) / 2.0, y, texto)
    else:
        print "geninformes.py::el_encogedor_de_fuentes_de_doraemon -> Error "\
              "alineación. Uso alineación a la izquierda por defecto."
        canvas.drawString(xini, y, texto)
    canvas.restoreState()


############################################################

def factura(cliente,
            factdata,
            lineas,
            arancel,
            vencimiento,
            texto,
            totales,
            impuesto = 1.16, 
            orden_ventanas = None, 
            es_copia = False):
    """
    Con los datos de entrada genera la factura.

    @params

    cliente --> es un diccionario con:
        - 'numcli' Número de cliente
        - 'nombre'
        - 'cif'
        - 'direccion'
        - 'cp'
        - 'localidad'
        - 'pais'
        - 'telf'
        - 'fax'

    factdata --> datos de la cabecera de la factura, es diccionario con:
        - 'facnum' Número de factura
        - 'fecha'
        - 'pedido'
        - 'albaranes'
        - 'observaciones'

    lineas --> datos del cuerpo de la factura, es una lista (un elemento
    por línea) de diccionarios con:
        - 'codigo'
        - 'cantidad'
        - 'descripcion'
        - 'precio' precio unitario
        - 'descuento'

    arancel --> una cadena con el código de arancel, si no es para extranjero
                es None y se aplica el impuesto. Con arancel el impuesto es 0

    vencimiento --> diccionario con:
        'fecha' --> fecha de vencimiento
        'pago' --> forma de pago
        'documento' --> es un diccionario con el documento de pago, con:
            -'forma' --> modo de pago y cuenta de destino del pago
            -'iban' --> iban de la cuenta destino
            -'swift' --> swift de la cuenta destino

    texto --> cadena que se pone en el cuadro IMPORTA LA PRESENTE FACTURA

    totales -->diccionario con:
        -'subtotal'
        -'cargo' None si no tiene
        -'descuento' None si no tiene
        -'totaliva'
        -'total'
        -'totirpf'
        -'irpf'
        -'recargo_equivalencia': Si no lleva, esta clave no existe en el
                                 diccionario.
        -'totrecargo_equivalencia': Cadena con importe total del recargo de
                                    equivalencia.

    impuesto --> valor numerico con el impuesto aplicado. Con arancel se pone
                 a 0 automaticamente
    """
    if orden_ventanas is None:  # Solo si no recibo el parámetro miro la 
                                # configuración general.
        try:
            orden_ventanas = pclases.config.get_orden_ventanas()
        except:
            orden_ventanas = "cf"  # Orden por defecto.

    datos_empresa = pclases.DatosDeLaEmpresa.select()[0]

    global linea#, tm, lm, rm, bm
    tmbak, bmbak, lmbak, rmbak = tm, bm, lm, rm = (680, 56.69, 05.35, 566.92)  # @UnusedVariable
    x, y = lm, tm  # @UnusedVariable
    # Creo la hoja
    nombre_chachi = cliente['nombre'].replace(" ", "_")
    nombre_chachi = abreviar(nombre_chachi, 10)
    nombre_chachi = cambiar_caracteres_problematicos(nombre_chachi)
    nomarchivo = os.path.join(gettempdir(), 
        "factura_%s_%s.pdf" % (nombre_chachi, give_me_the_name_baby()))
    if es_copia:
        numcopia = 1
        nomarchivo = "%s_COPIA%d.pdf" % (nomarchivo.replace(".pdf", ""), 
                                         numcopia)
        while os.path.exists(nomarchivo) and numcopia < 100: 
            # ¿Más de 100 copias? No creo. 
            _numcopia = numcopia
            numcopia += 1
            nomarchivo = "%s_COPIA%d.pdf" % (
                nomarchivo.replace(".pdf", "").replace(
                    "_COPIA%d" % _numcopia, ""), 
                numcopia)
    c = canvas.Canvas(nomarchivo)
    c.setTitle("factura %s %s" % (cliente['nombre'], factdata['fecha']))
    suma = 0.0
    # Caben 11 líneas por página. Tenemos que cortar de 11 en 11 para las
    # distintas páginas que pudiera haber
    MAXLINEAS = 12
    _lineas, lineas = lineas, []
    for linea in _lineas:
        lineas.append(linea)
        if linea.has_key("descuento"):
            tiene_descuento = (linea['descuento'] != "" and 
                               float(linea['descuento']) != 0)
            if tiene_descuento:
                lineas.append({})
    numpagina = 0
    from math import ceil
    paginastotales = ceil(len(lineas) / float(MAXLINEAS))
    buffer_texto = texto  # @UnusedVariable
    buff = lineas[MAXLINEAS:]
    lineas = lineas[:MAXLINEAS]
    while (lineas != []):
        bm, tm = bmbak, tmbak
        numpagina += 1
        # La marca de agua:
        if es_copia:
            marca_de_agua(c, " COPIA ", fontsize = 56)
        # La cabecera
        if datos_empresa.logo:
            ruta_logo = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', datos_empresa.logo)
            im = Image.open(ruta_logo)
            ancho, alto = im.size
            nuevo_alto = 1.5 * inch
            ancho_proporcional = ancho * (nuevo_alto / alto)
            #ancho_proporcional = 1.5*inch
            c.drawImage(ruta_logo,
                        lm+0.5*inch,
                        height - 1.5*inch,
                        ancho_proporcional,
                        nuevo_alto)
        if datos_empresa.bvqi:
            c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..','imagenes',datos_empresa.logoiso2),
                        rm-1.65*inch, height - 2.5*cm, 3.3*cm, 1.85*cm)

        # XXX
        if not datos_empresa.esSociedad:
            if datos_empresa.logo2 != "":
                c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..','imagenes',datos_empresa.logo2),
                            rm-1.65*inch, height - 2.5*cm, 3.3*cm, 1.85*cm)
        # XXX


        #c.drawCentredString(rm-inch, tm+1.40*inch, escribe('ESPMDD00433'))
        # XXX (Subo para que encaje en la ventana del sobre): linea = height-50
        linea = height-50 + 0.7*cm
        c.setFont("Helvetica", 18)
        c.drawCentredString(rm-inch, tm+1*inch, escribe('Factura'))
        c.drawCentredString(width/2, linea, escribe(datos_empresa.nombre))
        linea = sigLinea()


        # XXX
        if (not datos_empresa.esSociedad
            and datos_empresa.nombreContacto != datos_empresa.nombre):
            c.setFont("Helvetica-Bold", 12)
            c.drawCentredString(width/2, linea,
                                escribe(datos_empresa.nombreContacto))
            linea = sigLinea()
        # XXX


        c.setFont("Helvetica", 10)
        c.drawCentredString(width/2, linea,
                            escribe(datos_empresa.dirfacturacion))
        linea = sigLinea()

        c.drawCentredString(width/2, linea, escribe('%s %s%s, %s' % (
            datos_empresa.cpfacturacion,
            datos_empresa.ciudadfacturacion,
            datos_empresa.provinciafacturacion
                != datos_empresa.ciudadfacturacion
                and " (%s)" % (datos_empresa.provinciafacturacion) or "",
            datos_empresa.paisfacturacion)))
        linea = sigLinea()

        # DONE: El criterio del IRPF no es correcto.
        c.drawCentredString(width/2, linea, escribe('%s: %s' % (
            datos_empresa.str_cif_o_nif(), datos_empresa.cif)))
        #c.drawCentredString(width/2, linea, escribe('%s: %s' % (
        # datos_empresa.irpf == 0 and "C.I.F." or "N.I.F.",
        # datos_empresa.cif)))  # Si en datos de la empresa IRPF == 0 es
        # empresa y tiene C.I.F. Si no, considero que es empresario individual
        # y tiene N.I.F. en lugar de C.I.F.
        linea = sigLinea()
        if datos_empresa.bvqi:
            # Marcado CE Geotextiles
            anchotexto = c.stringWidth(
                            escribe('Geotextiles CE 1035-CPD-ES033858'),
                            "Courier", 8)
            anchosemitexto = c.stringWidth(
                                escribe('Geotextiles '),
                                "Courier", 8)
            posx = (width - anchotexto)/2 
            cursiva(c, posx,
                    linea,
                    escribe('Geotextiles    1035-CPD-ES033858'),
                    "Courier", 8, (0, 0, 0), 10)
            c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', "CE.png"),
                        posx + anchosemitexto, 
                        linea, 
                        0.40*cm, 
                        0.20*cm)
            # Marcado CE fibra
            anchotexto = c.stringWidth(
                            escribe('Fibra CE 1035-CPD-9003712'),
                            "Courier", 8)
            anchosemitexto = c.stringWidth(
                                escribe('Fibra '),
                                "Courier", 8)
            posx = (width - anchotexto)/2 
            cursiva(c, posx,
                    linea - 8,
                    escribe('Fibra    1035-CPD-9003712'),
                    "Courier", 8, (0, 0, 0), 10)
            c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', "CE.png"),
                        posx + anchosemitexto, 
                        linea - 8, 
                        0.40*cm, 
                        0.20*cm)
        c.setFont("Helvetica", 10)


        # La fecha y el número de factura fuera del cuadro

        # XXX
        if not datos_empresa.esSociedad:
            linea = sigLinea(0) + (15 * 1)
        # XXX

        linea = sigLinea(15)
        # Si en la cabecera de la empresa hay solo 3 líneas , la fecha y
        # número de factura pisa al texto "Factura", que está en tm + 1
        # pulgada.
        if linea + 10 > tm+1*inch:
            #print "¡BAJANDO!"
            linea = sigLinea()

        c.setFont("Times-Italic", 10)
        c.drawString(lm + 3 * cm, linea, escribe('FECHA FACTURA:'))
        xNumFactura = width/2 + 3 * cm
        c.drawString(xNumFactura, linea, escribe('Nº FACTURA:'))
        c.setFont("Helvetica-Bold", 10)
        c.drawString(lm + 3 * cm + c.stringWidth('FECHA FACTURA: ',
                                                 'Times-Italic', 10),
                     linea, escribe(factdata['fecha']))
        xNumFactura = width/2 + 3 * cm + c.stringWidth('Nº FACTURA: ',
                                                       'Times-Italic', 10)
        c.drawString(xNumFactura, linea, escribe(factdata['facnum']))

        # Los cuadros de datos fiscales y datos de envío
        xLocal = lm+inch
        xFact = width/2 + 0.7*inch
        xLocalTitulo = xLocal - 37
        xFactTitulo = xFact - 37

        linea = sigLinea(2)

        # La doble línea:
        c.saveState()
        if datos_empresa.irpf != 0:
            c.setStrokeColorRGB(1.0, 0.3, 0.3)
        else:
            c.setStrokeColorRGB(0.1, 0.1, 1.0)
        c.line(xLocalTitulo, linea-4, rm, linea-4)
        c.line(xLocalTitulo, linea-1, rm, linea-1)
        c.restoreState()

        # El doble rectángulo
        c.saveState()
        c.setLineWidth(0.5)
            # ------
        c.line(xLocalTitulo, linea-8, rm, linea-8)
        c.line(xLocalTitulo+2, linea-10, rm-2, linea-10)
            # ______
        c.line(xLocalTitulo+2, linea-8-15, rm-2, linea-8-15)
        c.line(xLocalTitulo, linea-10-15, rm, linea-10-15)
            # |
        c.line(xLocalTitulo, linea-8, xLocalTitulo, linea-10-15)
        c.line(xLocalTitulo+2, linea-10, xLocalTitulo+2, linea-8-15)
            #      |
        c.line(rm-2, linea-10, rm-2, linea-8-15)
        c.line(rm, linea-8, rm, linea-10-15)
        c.drawString(xLocalTitulo + 14, linea - 20,
                     escribe('Cliente: %s' % (cliente['numcli'])))
        c.drawString(width/2 + 10, linea - 20,
                     escribe('CIF: %s' % (cliente['cif'])))
        c.restoreState()

        linea = sigLinea(32) # Ponía 10. Después ponía 35. Se queda en 32.
        c.setFont("Helvetica", 8)
        txti, txtd = "Dirección de correspondencia:", "Dirección fiscal:"
        if orden_ventanas == "fc":
            txti, txtd = txtd, txti
        # Aprovecho para limpiar datos. No sé de dónde habrán sacado los datos 
        # de algunos clientes, pero vienen repletos de tabuladores, que se 
        # convierten después en cuadrados negros en el PDF.
        txti,txtd=txti.replace("\t", "").strip(),txtd.replace("\t", "").strip()
        c.drawString(xLocalTitulo, linea-1, escribe(txti))
        c.drawString(xFactTitulo, linea-1, escribe(txtd))
        c.setFont("Helvetica", 10)
        #rectangulo(c,
        #           (lm+0.45*inch, tm - 0.1 * cm),
        #           (xFact-50,     tm-inch - 0.1 * cm),
        #           doble = True)
        #rectangulo(c,
        #           (xFact-40, tm - 0.1 * cm),
        #           (rm,       tm-inch - 0.1 * cm),
        #           doble = True)
        # XXX: Subo un poco para encajar mejor en ventana. (0.7*cm + 3)
        rectangulo(c,
                   (lm+0.45*inch, tm - 0.1 * cm + 0.7*cm+3),
                   (xFact-50,     tm-inch - 0.1 * cm + 0.6*cm+3),
                   doble = True)
        rectangulo(c,
                   (xFact-40, tm - 0.1 * cm + 0.7*cm+3),
                   (rm,       tm-inch - 0.1 * cm + 0.6*cm+3),
                   doble = True)
        ### DATA
        # XXX: Subo para encajar mejor en ventana: linea = tm+0.45*inch-30
        linea = tm+0.45*inch-30 + 0.7*cm+3
        linea = sigLinea()

        c.setFont("Helvetica", 8)
        c.drawString(xLocalTitulo, linea, escribe('Nombre:'))
        c.drawString(xFactTitulo, linea, escribe('Nombre:'))
        c.setFont("Helvetica", 10)
        txti, txtd = cliente['nombre'], cliente['nombref']
        if orden_ventanas == "fc":
            txti, txtd = txtd, txti
        # Aprovecho para limpiar datos. No sé de dónde habrán sacado los datos 
        # de algunos clientes, pero vienen repletos de tabuladores, que se 
        # convierten después en cuadrados negros en el PDF.
        txti,txtd=txti.replace("\t", "").strip(),txtd.replace("\t", "").strip()
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xLocal,
                                            xFact - 50, linea,
                                            txti)
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xFact, rm - 2,
                                            linea, txtd)
        linea = sigLinea()
        c.setFont("Helvetica", 8)
        c.drawString(xLocalTitulo, linea, escribe('Dirección:'))
        c.drawString(xFactTitulo, linea, escribe('Dirección:'))
        c.setFont("Helvetica", 10)
        txti, txtd = cliente['direccion'], cliente['direccionf']
        if orden_ventanas == "fc":
            txti, txtd = txtd, txti
        # Aprovecho para limpiar datos. No sé de dónde habrán sacado los datos 
        # de algunos clientes, pero vienen repletos de tabuladores, que se 
        # convierten después en cuadrados negros en el PDF.
        txti,txtd=txti.replace("\t", "").strip(),txtd.replace("\t", "").strip()
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xLocal,
                                            xFact - 50, linea, txti)
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xFact, rm - 2,
                                            linea, txtd)
        linea = sigLinea()
        c.setFont("Helvetica", 8)
        c.drawString(xLocalTitulo, linea, escribe('Localidad:'))
        c.drawString(xFactTitulo, linea, escribe('Localidad:'))
        c.setFont("Helvetica", 10)
        txti, txtd = cliente['localidad'], cliente['localidadf']
        if orden_ventanas == "fc":
            txti, txtd = txtd, txti
        # Aprovecho para limpiar datos. No sé de dónde habrán sacado los datos 
        # de algunos clientes, pero vienen repletos de tabuladores, que se 
        # convierten después en cuadrados negros en el PDF.
        txti,txtd=txti.replace("\t", "").strip(),txtd.replace("\t", "").strip()
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xLocal,
                                            xFact - 50, linea, txti)
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xFact, rm - 2,
                                            linea, txtd)
        linea = sigLinea()
        c.setFont("Helvetica", 8)
        c.drawString(xLocalTitulo, linea, escribe('CP:'))
        c.drawString(xFactTitulo, linea, escribe('CP:'))
        c.setFont("Helvetica", 10)
        txti, txtd = ("%s %s" % (cliente['cp'], cliente['provincia']), 
                      "%s %s" % (cliente['cpf'], cliente['provinciaf']))
        if orden_ventanas == "fc":
            txti, txtd = txtd, txti
        # Aprovecho para limpiar datos. No sé de dónde habrán sacado los datos 
        # de algunos clientes, pero vienen repletos de tabuladores, que se 
        # convierten después en cuadrados negros en el PDF.
        txti,txtd=txti.replace("\t", "").strip(),txtd.replace("\t", "").strip()
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xLocal,
                                            xFact - 50, linea,
                                            txti)
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xFact, rm - 2,
                                            linea, txtd)
        linea = sigLinea()
        c.setFont("Helvetica", 8)
        c.drawString(xLocalTitulo, linea, escribe('País:'))
        c.drawString(xFactTitulo, linea, escribe('País:'))
        c.setFont("Helvetica", 10)
        txti, txtd = cliente['pais'], cliente['paisf']
        if orden_ventanas == "fc":
            txti, txtd = txtd, txti
        # Aprovecho para limpiar datos. No sé de dónde habrán sacado los datos 
        # de algunos clientes, pero vienen repletos de tabuladores, que se 
        # convierten después en cuadrados negros en el PDF.
        txti,txtd=txti.replace("\t", "").strip(),txtd.replace("\t", "").strip()
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xLocal,
                                            xFact - 50, linea, txti)
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xFact, rm - 2,
                                            linea, txtd)

        linea = sigLinea(10)
        # XXX Como he subido para encajar en la ventana del sobre, bajo ahora:
        linea -= 0.7*cm+3


        # Datos generales (Esquina superior
        # izquierda x=lm+0.5*inch, y=tm-1.2*inch)
        if factdata['pedido'] != None and factdata['pedido'].strip() != "":
            origen = lm + 2*inch
            # XXX: [epalomo] Negrita en números de pedido que se facturan.
            c.saveState()
            linea = tm - 1.2*inch
            c.drawString(lm + 0.5*inch, linea,
                         escribe('Su pedido (albarán): '))
            fuente = "Helvetica-Bold"
            tamanno = 10
            c.setFont(fuente, tamanno)
            textoPedidos = factdata['pedido']
            longitud = c.stringWidth(textoPedidos, fuente, tamanno)
            longitudLimite = rm - origen
            if longitud < longitudLimite:
                c.drawString(origen, linea, escribe(textoPedidos))
            else:
                renglones = longitud / longitudLimite
                renglones = int(renglones) + 1
                corte = int(len(textoPedidos)/renglones)
                memcorte = corte
                for i in range(renglones):  # @UnusedVariable
                    while (len(textoPedidos) > corte
                           and textoPedidos[corte-1] != ', '
                           and corte < 2*memcorte):
                        corte += 1
                    if corte == 2*memcorte:
                        corte = memcorte
                    c.drawString(origen, linea, escribe(textoPedidos[:corte]))
                    linea = sigLinea(10)
                    textoPedidos = textoPedidos[corte:]
                    corte = memcorte
            c.restoreState()
            # XXX: [epalomo] EONegrita en números de pedido que se facturan.

        if numpagina < paginastotales:
            offset = -1.5 * cm
            linea += offset
            bm += offset
            tm += offset

        # El cuerpo
        # -- Cuadro global
        rectangulo(c, (lm+0.5*inch, tm-0.75*inch-58), (rm, bm+inch+98))
        # -- Cabeceras
        x0precio = rm-2.15*inch
        rectangulo(c, (lm+0.5*inch, tm-0.75*inch-58),
                   (lm+1.65*inch, tm-0.75*inch-74), 'Código', 'centro')
        rectangulo(c, (lm+1.65*inch, tm-0.75*inch-58),
                   (lm+2.5*inch, tm-0.75*inch-74), 'Cantidad', 'centro')
        rectangulo(c, (lm+2.5*inch, tm-0.75*inch-74),
                   (rm-2.15*inch, tm-0.75*inch-74), 'Descripción', 'centro')
        rectangulo(c, (x0precio, tm-0.75*inch-58),
                   (rm-1.2*inch, tm-0.75*inch-74), 'Precio Unitario', 'centro')
        rectangulo(c, (rm-1.2*inch, tm-0.75*inch-58), (rm, tm-0.75*inch-74),
                   'TOTAL', 'centro')

        # -- Columnas de datos
        rectangulo(c,(lm+0.5*inch, tm-0.75*inch-74),(lm+1.65*inch, bm+inch+98))
        rectangulo(c,(lm+1.65*inch, tm-0.75*inch-74),(lm+2.5*inch, bm+inch+98))
        rectangulo(c,(lm+2.5*inch, tm-0.75*inch-74),(rm-2.15*inch, bm+inch+98))
        rectangulo(c,(x0precio, tm-0.75*inch-74),(rm-1.2*inch, bm+inch+98))
        rectangulo(c,(rm-1.2*inch, tm-0.75*inch-74),(rm, bm+inch+98))


        # DATA
        # Caben exactamente 11 líneas de venta. Debemos hacer una
        # segunda página en caso de que haya más

        linea = tm-1.92*inch
        xcodigo = lm+1.65*inch-4
        xcantidad = lm+1.9*inch
        xdescripcion = lm+2.5*inch+3
        xprecio = rm-1.25*inch
        xtotal = rm-0.2*inch
        if lineas != None:
            for l in lineas:
                if not l:
                    continue    # Es una línea nula que emula la que ocupa el 
                                # descuento. No hay que hacer nada salvo 
                                # saltar a la siguiente.
                # Chapuza formatos (refactorizar ya y mirar el lenguaje de
                # marcas de ReportLab. No reinventes la rueda).
                fuente = "Liberation"
                #fuente = "Helvetica"
                tamanno = 10
                alineacion_descripcion = -1     # -1: Izquierda, 0: Centrado,
                                                # 1: Derecha
                if ("<formatolinea>" in l['codigo']
                    and "</formatolinea>" in l['codigo']):
                    l['codigo'] = l['codigo'].replace("<formatolinea>", "")\
                                    .replace("</formatolinea>", "")
                    if "n" in l['codigo'] and "i" in l['codigo']:
                        fuente = "Helvetica-BoldOblique"
                        l['codigo'] = l['codigo'].replace("n", "", 1)
                        l['codigo'] = l['codigo'].replace("i", "", 1)
                    elif "i" in l['codigo']:
                        fuente = "Helvetica-Oblique"
                        l['codigo'] = l['codigo'].replace("i", "", 1)
                    elif "n" in l['codigo']:
                        fuente = "Helvetica-Bold"
                        l['codigo'] = l['codigo'].replace("n", "", 1)
                    if "c" in l['codigo']:
                        alineacion_descripcion = 0
                        l['codigo'] = l['codigo'].replace("c", "", 1)
                    elif "d" in l['codigo']:
                        alineacion_descripcion = 1
                        l['codigo'] = l['codigo'].replace("d", "", 1)
                # Data
                c.setFont(fuente, tamanno)
                c.drawRightString(xcodigo, linea, escribe(l['codigo']))
                try:
                    cantidad_sin_cero = utils.float2str(float(l['cantidad']),2)
                except ValueError, msg:
                    if isinstance(l['cantidad'], str):
                        cantidad_sin_cero = l['cantidad']
                    else:
                        raise ValueError, msg
                try:
                    unidad = l['unidad']
                except KeyError:
                    unidad = ""
                cantidad_sin_cero = "%s %s" % (cantidad_sin_cero, unidad)
                # i 10096
                el_encogedor_de_fuentes_de_doraemon(c, fuente, tamanno, 
                                                    xcantidad - 15, 
                                                    xdescripcion - 3,
                                                    linea, cantidad_sin_cero, 
                                                    1)
                # c.drawRightString(xdescripcion-5, linea,
                #                   escribe(cantidad_sin_cero))
                c.setFont(fuente, tamanno)
                descripcion = l['descripcion']
                origen = xdescripcion
                limite = rm-2.15*inch
                # --------- 8< ----------
                longitud = c.stringWidth(descripcion, fuente, tamanno)
                longitudLimite = limite - origen
                if longitud < longitudLimite:
                    if alineacion_descripcion < 0:
                        c.drawString(origen, linea, escribe(descripcion))
                    elif alineacion_descripcion > 0:
                        c.drawRightString(x0precio - 0.1*cm, linea,
                                          escribe(descripcion))
                    else:
                        c.drawCentredString((origen + x0precio) / 2, linea,
                                            escribe(descripcion))
                else:
                    palabras = descripcion.split(" ")
                    palabras.reverse()
                    while palabras: # Mientras queden palabras
                        linea_a_imprimir = []
                        while c.stringWidth(" ".join(linea_a_imprimir),
                              fuente, tamanno) <= longitudLimite and palabras:
                            linea_a_imprimir.append(palabras.pop())
                        if c.stringWidth(" ".join(linea_a_imprimir), fuente,
                                         tamanno) > longitudLimite:
                            palabras.append(linea_a_imprimir.pop())
                        if linea_a_imprimir == []:  # La palabra es demasiado
                                # larga para una línea. NOTA: La parto a 30,
                                # que seguro que cabe.
                            palabrota = palabras.pop()
                            linea_a_imprimir.append(palabrota[:30])
                            palabras.append(palabrota[30:])
                        # c.drawString(xdescripcion, linea,
                        #               escribe(" ".join(linea_a_imprimir)))
                        if alineacion_descripcion < 0:
                            c.drawString(xdescripcion, linea,
                                         escribe(" ".join(linea_a_imprimir)))
                        elif alineacion_descripcion > 0:
                            c.drawRightString(x0precio - 0.1*cm, linea,
                                        escribe(" ".join(linea_a_imprimir)))
                        else:
                            c.drawCentredString((xdescripcion + x0precio) / 2,
                                linea, escribe(" ".join(linea_a_imprimir)))
                        if palabras:    # Si no quedan palabras no tengo que
                                        # pasar de línea, queda por escribir
                                        # el precio y eso en la actual.
                            linea = sigLinea()
                # --------- >8 ----------
                c.rotate(90)
                c.setFont("Times-Roman", 8)
                c.drawCentredString(height/2, -lm-32,
                                    escribe(datos_empresa.registroMercantil))
                c.rotate(-90)

                c.setFont(fuente, tamanno)
                #try:
                #    c.drawRightString(xprecio, linea,
                #       escribe(utils.float2str(l['precio'], 3)))
                #except ValueError, msg:
                #    if isinstance(l['precio'], str):
                #        c.drawRightString(xprecio,linea,escribe(l['precio']))
                #    else:
                #        raise ValueError, msg
                if isinstance(l['precio'], str):
                    c.drawRightString(xprecio, linea, escribe(l['precio']))
                else:
                    try:
                        c.drawRightString(xprecio, linea,
                            escribe(utils.float2str(l['precio'], 4)))
                    except ValueError, msg:
                        raise ValueError, msg
                c.setFont(fuente, tamanno)
                try:
                    total = utils._float(l['precio'])
                    total *= utils._float(l['cantidad'])
                    c.drawRightString(xtotal,
                                      linea,
                                      escribe(utils.float2str(total, 2)))
                except ValueError, msg:
                    if l['precio'] != "" and l['cantidad'] !=  "":
                        # Si el contenido viene desglosado, precio y cantidad
                        # son cadenas vacías, por tanto la excepción no es un
                        # error y no debo avisar con falsos positivos.
                        print >> sys.stderr, "geninformes::factura -> %s" % msg
                    total = 0
                suma += total
                if l['descuento'] != "" and float(l['descuento']) != 0:
                    linea = sigLinea()
                    c.drawString(xdescripcion, linea,
                        escribe('    DESCUENTO %.2f %%' % (
                            float(l['descuento'])*100)))
                    desctotal = float('-'+l['descuento'])*total
                    suma += desctotal
                    c.drawRightString(xtotal, linea,
                                      escribe(utils.float2str(desctotal)))
                linea = sigLinea(20)
            # END OF for l in lineas:

        if buff == []:    # Si no va a haber segunda página, escribo los
                            # cuadros de los totales.
            # -- Cuadro final
            c.setFont('Times-Roman', 8)
            c.drawString(lm + 0.5*inch, bm+inch+90,
                         "IMPORTA LA PRESENTE FACTURA:")

            rectangulo(c, (lm+0.5*inch, bm+inch+88), (rm-2.2*inch, bm+inch+30))
            origen = lm+0.5*inch + 4
            linea = bm + inch + 75
            # DATA
            if texto != None:
                c.setFont('Helvetica', 10)
                lineas_agregadas = agregarFila(origen, linea, rm - 2.2*inch,
                    escribe(texto), c, "Helvetica", 10)
                for i in xrange(lineas_agregadas):  # @UnusedVariable
                    linea = sigLinea()
            c.saveState()
            c.setFont('Times-Roman', 8)
            if factdata['observaciones'] != "":
                texto = escribe("Obs.: %s" % (factdata['observaciones']))
            else:
                texto = ""
            # Hay que hacer destacar las observaciones.
            borde_izq_obs = lm + 0.6*inch
            borde_der_obs = rm - 2.2*inch
            hlinea = 8
            sizefont = 8
            topeinferior = bm + inch + 30   # Sacado del rectángulo de 
                                            # unas líneas más arriba.
            lineas_sumadas = 0
            while ((linea - lineas_sumadas*hlinea) > topeinferior 
                   and sizefont < 12):  # CWT: Antes era 18 el máximo.
                sizefont += 1
                hlinea += 1
                lineas_sumadas = agregarFila(borde_izq_obs, 
                                             linea, 
                                             borde_der_obs, 
                                             texto, 
                                             c,
                                             "Times-Roman", 
                                             sizefont, 
                                             altura_linea = hlinea, 
                                             simular = True)
            sizefont -= 1
            hlinea -= 1
            lineas_sumadas = agregarFila(borde_izq_obs, 
                                         linea, 
                                         borde_der_obs, 
                                         texto, 
                                         c,
                                         "Times-Roman", 
                                         sizefont, 
                                         altura_linea = hlinea, 
                                         simular = False, 
                                         subrayador_fosforito = (1, 1, 0) )
            #agregarFila(lm + 0.6*inch, linea, rm-2.2*inch, texto, c,
            #            "Times-Roman", 8)
            c.restoreState()


            # -- Arancel
            if arancel != None and arancel.strip() != "":
                rectangulo(c, (lm+0.5*inch, bm+inch+21), (rm, bm+inch+7),
                           'ARANCEL:')
                c.drawString(lm+1.4*inch, bm+inch+11,
                    escribe(arancel+'  Exención del I.V.A. Art. 25 1.a Ley 3'\
                                    '7/1992 de 29 de Diciembre del I.V.A.'))


            # -- Totales
            if totales['irpf'] != "0 %":
                linea = bm+2.2*inch
            else:
                linea = bm+2.1*inch
            c.drawString(rm-2.1*inch, linea, escribe('Subtotal'))
            rectangulo(c, (rm-1.2*inch, linea+10), (rm, linea-4),
                       totales['subtotal'], 'derecha')
            linea = sigLinea()
            if totales['descuento'] != None:
                c.drawString(rm-2.1*inch, linea, escribe('Descuento'))
                rectangulo(c, (rm-1.2*inch, linea+10), (rm, linea-4),
                           totales['descuento'], 'derecha')

            linea = sigLinea()
            c.drawString(rm-2.1*inch, linea,
                         escribe('IVA ('+totales['iva']+')'))
            rectangulo(c, (rm-1.2*inch, linea+10), (rm, linea-4),
                       totales['totaliva'], 'derecha')
            linea = sigLinea()
            if ("recargo_equivalencia" in totales
                and totales["recargo_equivalencia"] != None):
                c.drawString(rm - 2.1*inch,
                             linea,
                             escribe("R. E. (%s)" %
                                totales['recargo_equivalencia']))
                rectangulo(c,
                           (rm - 1.2 * inch, linea + 10),
                           (rm, linea - 4),
                           totales['totrecargo_equivalencia'],
                           "derecha")
                linea = sigLinea()
            if totales['irpf'] != "0 %":
                c.drawString(rm-2.1*inch, linea,
                             escribe('IRPF (%s)' % (totales['irpf'])))
                rectangulo(c, (rm-1.2*inch, linea+10), (rm, linea-4),
                           totales['totirpf'], 'derecha')
                linea = sigLinea()
            c.drawString(rm-2.1*inch, linea, escribe('TOTAL'))
            rectangulo(c, (rm-1.2*inch, linea+10), (rm, linea-4),
                       totales['total'], 'derecha')
            c.setFont("Helvetica", 10)
            # -- TEXTO
            origen = lm+0.5*inch
            linea = bm+0.85*inch
            rectangulo(c, (origen, bm+inch), (rm, bm))
            # DATA
            if vencimiento != None:
                xvencimiento = lm+0.5*inch+4
                c.drawString(xvencimiento, linea,
                             escribe('VENCIMIENTO: ' + vencimiento['fecha']))
                linea = sigLinea()
                if (vencimiento['pago'] and vencimiento['pago'].strip() != "0"
                    and vencimiento['pago'].strip() != ""):
                    c.drawString(xvencimiento, linea,
                        escribe('FORMA DE PAGO: ' + vencimiento['pago']))
                    linea = sigLinea()
                c.drawString(xvencimiento, linea,
                             escribe('DOCUMENTO DE PAGO: '))
                origen = lm + 2.2*inch
                textoDocumento = vencimiento['documento']
                longitud = c.stringWidth(textoDocumento, 'Helvetica', 10)
                longitudLimite = rm - origen
                if longitud < longitudLimite:
                    c.drawString(origen, linea, escribe(textoDocumento))
                else:
                    renglones = longitud / longitudLimite
                    renglones = int(renglones) + 1
                    corte = int(len(textoDocumento)/renglones)
                    memcorte = corte
                    for i in range(renglones):  # @UnusedVariable
                        while (len(textoDocumento) > corte
                               and textoDocumento[corte-1] != ' '
                               and corte < 2*memcorte):
                            corte += 1
                        if corte == 2*memcorte:
                            corte = memcorte
                        c.drawString(origen, linea,
                                     escribe(textoDocumento[:corte]))
                        linea = sigLinea()
                        textoDocumento = textoDocumento[corte:]
                        corte = memcorte

        else:
            textopaginas = "Página %d de %d" % (numpagina, paginastotales)
            anchotextopaginas = c.stringWidth(texto, "Helvetica", 10)  # @UnusedVariable
            c.drawRightString(rm - 0.1 * cm, bm + 0.8 * inch, textopaginas)


        bm, tm = bmbak, tmbak
        # Pie de factura
        linea = bm-0.25*inch
            # Cuadro verde:
        if datos_empresa.direccion != datos_empresa.dirfacturacion:
            c.saveState()
            c.setFillColorRGB(0.6, 1, 0.6)
            c.setStrokeColorRGB(0.6, 1, 0.6)
            c.rect(lm + 0.5 * inch, linea - 20, rm - (lm + 0.5 *inch), 15 * 2,
                   stroke = 1, fill = 1)
                # 15 es el valor por defecto para el alto de una línea
                # de texto.
            c.restoreState()
                # Texto dentro:
            c.setFont("Helvetica", 8)
            pos_pie = lm + 0.5 * inch + ((rm - (lm + 0.5 * inch)) / 2)
            c.drawCentredString(pos_pie, linea,
                                escribe('DIRECCIÓN DE OFICINAS Y CORRESPO'\
                                        'NDENCIA: %s. %s - %s (%s)' % (
                                            datos_empresa.direccion,
                                            datos_empresa.cp,
                                            datos_empresa.ciudad,
                                            datos_empresa.provincia)))
            linea = sigLinea()
            if datos_empresa.fax:
                c.drawCentredString(pos_pie,
                                    linea,
                                    escribe('Tlf. %s  Fax %s' % (
                                        datos_empresa.telefono,
                                        datos_empresa.fax))
                                    )
            else:
                c.drawCentredString(pos_pie,
                                    linea,
                                    escribe('Tlf. %s' % (
                                        datos_empresa.telefono))
                                    )


        # Salvamos la página
        c.showPage()
        lineas = buff[:MAXLINEAS]
        buff = buff[MAXLINEAS:]

    # Salvamos el documento
    c.save()
    return nomarchivo

def marca_de_agua(c, texto="BORRADOR", color=(1.0, 0.7, 0.7), fontsize=42):
    """
    c es un canvas donde se dibujará en ángulo el texto recibido
    como marca de agua.
    color debe ser una lista de 3 valores (RGB) entre 0.0 y 1.0
    """
    # Marca "borrador"
    c.saveState()
    c.setFont("Courier-BoldOblique", fontsize)
    ancho = c.stringWidth(texto, "Courier-BoldOblique", fontsize)
    c.translate(A4[0] / 2.0, A4[1] / 2.0)
    c.rotate(45)
    c.setLineWidth(3)
    c.setStrokeColorRGB(*color)
    c.setFillColorRGB(*color)
    c.rect((-ancho - 10) / 2.0, -5, (ancho + 10), fontsize - 10, fill = False)
    c.drawCentredString(0, 0, texto)
    c.rotate(-45)
    c.restoreState()
    # EOMarca "borrador"

def prefactura(cliente, factdata, lineas, arancel, vencimiento, texto,
               totales, impuesto = 1.16, orden_ventanas = None):
    """
    Con los datos de entrada genera la prefactura o factura pro forma.

    @params

    cliente --> es un diccionario con:
        - 'numcli' Número de cliente
        - 'nombre'
        - 'cif'
        - 'direccion'
        - 'cp'
        - 'localidad'
        - 'pais'
        - 'telf'
        - 'fax'

    factdata --> datos de la cabecera de la factura, es diccionario con:
        - 'facnum' Número de factura
        - 'fecha'
        - 'pedido'
        - 'albaranes'
        - 'observaciones'

    lineas --> datos del cuerpo de la factura, es una lista (un elemento
    por línea) de diccionarios con:
        - 'codigo'
        - 'cantidad'
        - 'descripcion'
        - 'precio' precio unitario
        - 'descuento'

    arancel --> una cadena con el código de arancel, si no es para extranjero
                es None y se aplica el impuesto. Con arancel el impuesto es 0

    vencimiento --> diccionario con:
        'fecha' --> fecha de vencimiento
        'pago' --> forma de pago
        'documento' --> es un diccionario con el documento de pago, con:
            -'forma' --> modo de pago y cuenta de destino del pago
            -'iban' --> iban de la cuenta destino
            .'swift' --> swift de la cuenta destino

    texto --> cadena que se pone en el cuadro IMPORTA LA PRESENTE FACTURA

    totales -->diccionario con:
        -'subtotal'
        -'cargo' None si no tiene
        -'descuento' None si no tiene
        -'totaliva'
        -'total'
        -'totirpf'
        -'irpf'

    impuesto --> valor numerico con el impuesto aplicado. Con arancel se pone
                 a 0 automaticamente
    """

    if orden_ventanas is None:  # Solo si no recibo el parámetro miro la 
                                # configuración general.
        try:
            orden_ventanas = pclases.config.get_orden_ventanas()
        except:
            orden_ventanas = "cf"  # Orden por defecto.

    datos_empresa = pclases.DatosDeLaEmpresa.select()[0]

    global linea#, tm, lm, rm, bm
    tmbak, bmbak, lmbak, rmbak = tm, bm, lm, rm = (680, 56.69, 05.35, 566.92)  # @UnusedVariable
    x, y = lm, tm  # @UnusedVariable
    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
                              "factura_%s.pdf" % give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo)
    c.setTitle("factura %s %s" % (cliente['nombre'], factdata['fecha']))
    suma = 0.0
    # Caben 11 líneas por página. Tenemos que cortar de 11 en 11 para las
    # distintas páginas que pudiera haber
    MAXLINEAS = 13
    _lineas, lineas = lineas, []
    for linea in _lineas:
        lineas.append(linea)
        if linea.has_key("descuento"):
            tiene_descuento = (linea['descuento'] != "" and 
                               float(linea['descuento']) != 0)
            if tiene_descuento:
                lineas.append({})
    numpagina = 0
    from math import ceil
    paginastotales = ceil(len(lineas) / float(MAXLINEAS))
    buffer_texto = texto  # @UnusedVariable
    buff = lineas[MAXLINEAS:]
    lineas = lineas[:MAXLINEAS]
    while (lineas != []):
        bm, tm = bmbak, tmbak
        numpagina += 1
        marca_de_agua(c, "PREFACTURA")
        linea = height-50
        c.setFont("Helvetica", 18)
        c.drawCentredString(rm-inch, tm+1*inch, escribe('Factura pro forma'))
        linea = sigLinea()
        # XXX
        if (not datos_empresa.esSociedad
            and datos_empresa.nombreContacto != datos_empresa.nombre):
            c.setFont("Helvetica-Bold", 12)
            linea = sigLinea()
        # XXX
        c.setFont("Helvetica", 10)
        linea = sigLinea()
        linea = sigLinea()
        if datos_empresa.bvqi:
            # Marcado CE Geotextiles
            anchotexto = c.stringWidth(
                            escribe('Geotextiles CE 1035-CPD-ES033858'),
                            "Courier", 8)
            anchosemitexto = c.stringWidth(
                                escribe('Geotextiles '),
                                "Courier", 8)
            posx = (width - anchotexto)/2 
            cursiva(c, posx,
                    linea,
                    escribe('Geotextiles    1035-CPD-ES033858'),
                    "Courier", 8, (0, 0, 0), 10)
            c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', "CE.png"),
                        posx + anchosemitexto, 
                        linea, 
                        0.40*cm, 
                        0.20*cm)
            # Marcado CE fibra
            anchotexto = c.stringWidth(
                            escribe('Fibra CE 1035-CPD-9003712'),
                            "Courier", 8)
            anchosemitexto = c.stringWidth(
                                escribe('Fibra '),
                                "Courier", 8)
            posx = (width - anchotexto)/2 
            cursiva(c, posx,
                    linea - 8,
                    escribe('Fibra    1035-CPD-9003712'),
                    "Courier", 8, (0, 0, 0), 10)
            c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', "CE.png"),
                        posx + anchosemitexto, 
                        linea - 8, 
                        0.40*cm, 
                        0.20*cm)
        c.setFont("Helvetica", 10)
        linea = sigLinea()
        # La fecha y el número de factura fuera del cuadro
        # XXX
        if not datos_empresa.esSociedad:
            linea = sigLinea(0) + (15 * 1)
        # XXX
        linea = sigLinea(15)
        c.setFont("Times-Italic", 10)
        c.drawString(lm + 3 * cm, linea, escribe('FECHA PREFACTURA:'))
        xNumFactura = width/2 + 3 * cm
        c.drawString(xNumFactura, linea, escribe('Nº PREFACTURA:'))
        c.setFont("Helvetica-Bold", 10)
        c.drawString(lm + 3 * cm + c.stringWidth('FECHA PREFACTURA: ',
            'Times-Italic', 10), linea, escribe(factdata['fecha']))
        xNumFactura = (width/2 + 3 * cm
                        + c.stringWidth('Nº PREFACTURA: ', 'Times-Italic', 10))
        c.drawString(xNumFactura, linea, escribe(factdata['facnum']))
        # Los cuadros de datos fiscales y datos de envío
        xLocal = lm+inch
        xFact = width/2 + 0.7*inch
        xLocalTitulo = xLocal - 37
        xFactTitulo = xFact - 37
        linea = sigLinea(2)
        # La doble línea:
        c.saveState()
        if datos_empresa.irpf != 0:
            c.setStrokeColorRGB(0.8, 0.9, 0.2)
        else:
            c.setStrokeColorRGB(0.0, 0.9, 0.0)
        c.line(xLocalTitulo, linea-4, rm, linea-4)
        c.line(xLocalTitulo, linea-1, rm, linea-1)
        c.restoreState()
        # El doble rectángulo
        c.saveState()
        c.setLineWidth(0.5)
            # ------
        c.line(xLocalTitulo, linea-8, rm, linea-8)
        c.line(xLocalTitulo+2, linea-10, rm-2, linea-10)
            # ______
        c.line(xLocalTitulo+2, linea-8-15, rm-2, linea-8-15)
        c.line(xLocalTitulo, linea-10-15, rm, linea-10-15)
            # |
        c.line(xLocalTitulo, linea-8, xLocalTitulo, linea-10-15)
        c.line(xLocalTitulo+2, linea-10, xLocalTitulo+2, linea-8-15)
            #      |
        c.line(rm-2, linea-10, rm-2, linea-8-15)
        c.line(rm, linea-8, rm, linea-10-15)
        c.drawString(xLocalTitulo + 14, linea - 20,
                     escribe('Cliente: %s' % (cliente['numcli'])))
        c.drawString(width/2 + 10, linea - 20,
                     escribe('CIF: %s' % (cliente['cif'])))
        c.restoreState()
        linea = sigLinea(35) # Ponía 10
        c.setFont("Helvetica", 8)
        c.setFont("Helvetica", 8)
        txti, txtd = "Dirección de correspondencia:", "Dirección fiscal:"
        if orden_ventanas == "fc":
            txti, txtd = txtd, txti
        # Aprovecho para limpiar datos. No sé de dónde habrán sacado los datos 
        # de algunos clientes, pero vienen repletos de tabuladores, que se 
        # convierten después en cuadrados negros en el PDF.
        txti,txtd=txti.replace("\t", "").strip(),txtd.replace("\t", "").strip()
        c.drawString(xLocalTitulo, linea-1, escribe(txti))
        c.drawString(xFactTitulo, linea-1, escribe(txtd))
        c.setFont("Helvetica", 10)
        rectangulo(c, (lm+0.45*inch, tm - 0.1 * cm),
                    (xFact-50, tm-inch - 0.1 * cm), doble = True)
        rectangulo(c, (xFact-40,     tm - 0.1 * cm), (rm, tm-inch - 0.1 * cm),
                    doble = True)
        ### DATA
        linea = tm+0.45*inch-30
        linea = sigLinea()
        c.setFont("Helvetica", 8)
        c.drawString(xLocalTitulo, linea, escribe('Nombre:'))
        c.drawString(xFactTitulo, linea, escribe('Nombre:'))
        c.setFont("Helvetica", 10)
        txti, txtd = cliente['nombre'], cliente['nombref']
        if orden_ventanas == "fc":
            txti, txtd = txtd, txti
        # Aprovecho para limpiar datos. No sé de dónde habrán sacado los datos 
        # de algunos clientes, pero vienen repletos de tabuladores, que se 
        # convierten después en cuadrados negros en el PDF.
        txti,txtd=txti.replace("\t", "").strip(),txtd.replace("\t", "").strip()
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xLocal,
                                            xFact - 50, linea,
                                            txti)
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xFact, rm - 2,
                                            linea, txtd)
        linea = sigLinea()
        c.setFont("Helvetica", 8)
        c.drawString(xLocalTitulo, linea, escribe('Dirección:'))
        c.drawString(xFactTitulo, linea, escribe('Dirección:'))
        c.setFont("Helvetica", 10)
        txti, txtd = cliente['direccion'], cliente['direccionf']
        if orden_ventanas == "fc":
            txti, txtd = txtd, txti
        # Aprovecho para limpiar datos. No sé de dónde habrán sacado los datos 
        # de algunos clientes, pero vienen repletos de tabuladores, que se 
        # convierten después en cuadrados negros en el PDF.
        txti,txtd=txti.replace("\t", "").strip(),txtd.replace("\t", "").strip()
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xLocal,
                                            xFact - 50, linea, txti)
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xFact, rm - 2,
                                            linea, txtd)
        linea = sigLinea()
        c.setFont("Helvetica", 8)
        c.drawString(xLocalTitulo, linea, escribe('Localidad:'))
        c.drawString(xFactTitulo, linea, escribe('Localidad:'))
        c.setFont("Helvetica", 10)
        txti, txtd = cliente['localidad'], cliente['localidadf']
        if orden_ventanas == "fc":
            txti, txtd = txtd, txti
        # Aprovecho para limpiar datos. No sé de dónde habrán sacado los datos 
        # de algunos clientes, pero vienen repletos de tabuladores, que se 
        # convierten después en cuadrados negros en el PDF.
        txti,txtd=txti.replace("\t", "").strip(),txtd.replace("\t", "").strip()
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xLocal,
                                            xFact - 50, linea, txti)
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xFact, rm - 2,
                                            linea, txtd)
        linea = sigLinea()
        c.setFont("Helvetica", 8)
        c.drawString(xLocalTitulo, linea, escribe('CP:'))
        c.drawString(xFactTitulo, linea, escribe('CP:'))
        c.setFont("Helvetica", 10)
        txti, txtd = ("%s %s" % (cliente['cp'], cliente['provincia']), 
                      "%s %s" % (cliente['cpf'], cliente['provinciaf']))
        if orden_ventanas == "fc":
            txti, txtd = txtd, txti
        # Aprovecho para limpiar datos. No sé de dónde habrán sacado los datos 
        # de algunos clientes, pero vienen repletos de tabuladores, que se 
        # convierten después en cuadrados negros en el PDF.
        txti,txtd=txti.replace("\t", "").strip(),txtd.replace("\t", "").strip()
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xLocal,
                                            xFact - 50, linea,
                                            txti)
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xFact, rm - 2,
                                            linea, txtd)
        linea = sigLinea()
        c.setFont("Helvetica", 8)
        c.drawString(xLocalTitulo, linea, escribe('País:'))
        c.drawString(xFactTitulo, linea, escribe('País:'))
        c.setFont("Helvetica", 10)
        txti, txtd = cliente['pais'], cliente['paisf']
        if orden_ventanas == "fc":
            txti, txtd = txtd, txti
        # Aprovecho para limpiar datos. No sé de dónde habrán sacado los datos 
        # de algunos clientes, pero vienen repletos de tabuladores, que se 
        # convierten después en cuadrados negros en el PDF.
        txti,txtd=txti.replace("\t", "").strip(),txtd.replace("\t", "").strip()
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xLocal,
                                            xFact - 50, linea, txti)
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xFact, rm - 2,
                                            linea, txtd)

        linea = sigLinea(10)
        # Datos generales (Esquina superior izquierda
        # x = lm+0.5*inch, y = tm-1.2*inch)
        if factdata['pedido'] != None and factdata['pedido'].strip() != "":
            origen = lm + 2*inch
            linea = tm - 1.2*inch
            c.drawString(lm + 0.5*inch, linea,
                         escribe('Su pedido (albarán): '))
            textoPedidos = factdata['pedido']
            longitud = c.stringWidth(textoPedidos, 'Helvetica', 10)
            longitudLimite = rm - origen
            if longitud < longitudLimite:
                c.drawString(origen, linea, escribe(textoPedidos))
            else:
                renglones = longitud / longitudLimite
                renglones = int(renglones) + 1
                corte = int(len(textoPedidos)/renglones)
                memcorte = corte
                for i in range(renglones):  # @UnusedVariable
                    while (len(textoPedidos) > corte
                           and textoPedidos[corte-1] != ', '
                           and corte < 2*memcorte):
                        corte += 1
                    if corte == 2*memcorte:
                        corte = memcorte
                    c.drawString(origen, linea, escribe(textoPedidos[:corte]))
                    linea = sigLinea(10)
                    textoPedidos = textoPedidos[corte:]
                    corte = memcorte
        if numpagina < paginastotales:
            offset = -1.5 * cm
            linea += offset
            bm += offset
            tm += offset
        # El cuerpo
        # -- Cuadro global
        rectangulo(c, (lm+0.5*inch, tm-0.75*inch-58), (rm, bm+inch+98))
        # -- Cabeceras
        x0precio = rm-2.15*inch
        rectangulo(c, (lm+0.5*inch, tm-0.75*inch-58),
                    (lm+1.65*inch, tm-0.75*inch-74), 'Código', 'centro')
        rectangulo(c, (lm+1.65*inch, tm-0.75*inch-58),
                    (lm+2.5*inch, tm-0.75*inch-74), 'Cantidad', 'centro')
        rectangulo(c, (lm+2.5*inch, tm-0.75*inch-74),
                    (rm-2.15*inch, tm-0.75*inch-74), 'Descripción', 'centro')
        rectangulo(c, (x0precio, tm-0.75*inch-58),
                    (rm-1.2*inch, tm-0.75*inch-74), 'Precio Unitario',
                    'centro')
        rectangulo(c, (rm-1.2*inch, tm-0.75*inch-58), (rm, tm-0.75*inch-74),
                    'TOTAL', 'centro')
        # -- Columnas de datos
        rectangulo(c,(lm+0.5*inch, tm-0.75*inch-74),(lm+1.65*inch, bm+inch+98))
        rectangulo(c,(lm+1.65*inch, tm-0.75*inch-74),(lm+2.5*inch, bm+inch+98))
        rectangulo(c,(lm+2.5*inch, tm-0.75*inch-74),(rm-2.15*inch, bm+inch+98))
        rectangulo(c,(x0precio, tm-0.75*inch-74),(rm-1.2*inch, bm+inch+98))
        rectangulo(c,(rm-1.2*inch, tm-0.75*inch-74),(rm, bm+inch+98))
        # DATA
        # Caben exactamente 11 líneas de venta. Debemos hacer una
        # segunda página en caso de que haya más
        linea = tm-1.92*inch
        xcodigo = lm+1.65*inch-4
        xcantidad = lm+1.9*inch
        xdescripcion = lm+2.5*inch+3
        xprecio = rm-1.25*inch
        xtotal = rm-0.2*inch
        if lineas != None:
            for l in lineas:
                if not l:
                    continue
                # Chapuza formatos (refactorizar ya y mirar el lenguaje de
                # marcas de ReportLab. No reinventes la rueda).
                fuente = "Helvetica"
                tamanno = 10
                alineacion_descripcion = -1     # -1: Izquierda, 0: Centrado,
                                                # 1: Derecha
                if ("<formatolinea>" in l['codigo']
                    and "</formatolinea>" in l['codigo']):
                    l['codigo'] = l['codigo'].replace("<formatolinea>", "")\
                                    .replace("</formatolinea>", "")
                    if "n" in l['codigo'] and "i" in l['codigo']:
                        fuente = "Helvetica-BoldOblique"
                        l['codigo'] = l['codigo'].replace("n", "", 1)
                        l['codigo'] = l['codigo'].replace("i", "", 1)
                    elif "i" in l['codigo']:
                        fuente = "Helvetica-Oblique"
                        l['codigo'] = l['codigo'].replace("i", "", 1)
                    elif "n" in l['codigo']:
                        fuente = "Helvetica-Bold"
                        l['codigo'] = l['codigo'].replace("n", "", 1)
                    if "c" in l['codigo']:
                        alineacion_descripcion = 0
                        l['codigo'] = l['codigo'].replace("c", "", 1)
                    elif "d" in l['codigo']:
                        alineacion_descripcion = 1
                        l['codigo'] = l['codigo'].replace("d", "", 1)
                # Data
                c.setFont(fuente, tamanno)
                c.drawRightString(xcodigo, linea, escribe(l['codigo']))
                try:
                    cantidad_sin_cero = utils.float2str(float(l['cantidad']),2)
                except ValueError, msg:
                    if isinstance(l['cantidad'], str):
                        cantidad_sin_cero = l['cantidad']
                    else:
                        raise ValueError, msg
                # i 10096
                el_encogedor_de_fuentes_de_doraemon(c, fuente, tamanno, 
                                                    xcantidad - 15, 
                                                    xdescripcion - 3,
                                                    linea, cantidad_sin_cero, 
                                                    1)
                # c.drawRightString(xdescripcion-5, linea,
                #                   escribe(cantidad_sin_cero))
                c.setFont(fuente, tamanno)
                descripcion = l['descripcion']
                origen = xdescripcion
                limite = rm-2.15*inch
                # --------- 8< ----------
                longitud = c.stringWidth(descripcion, fuente, tamanno)
                longitudLimite = limite - origen
                if longitud < longitudLimite:
                    if alineacion_descripcion < 0:
                        c.drawString(origen, linea, escribe(descripcion))
                    elif alineacion_descripcion > 0:
                        c.drawRightString(x0precio - 0.1*cm, linea,
                                          escribe(descripcion))
                    else:
                        c.drawCentredString((origen + x0precio) / 2, linea,
                                            escribe(descripcion))
                else:
                    palabras = descripcion.split(" ")
                    palabras.reverse()
                    while palabras: # Mientras queden palabras
                        linea_a_imprimir = []
                        while (c.stringWidth(" ".join(linea_a_imprimir),
                                             fuente, tamanno) <= longitudLimite
                               and palabras):
                            linea_a_imprimir.append(palabras.pop())
                        if c.stringWidth(" ".join(linea_a_imprimir),
                                         fuente, tamanno) > longitudLimite:
                            palabras.append(linea_a_imprimir.pop())
                        if linea_a_imprimir == []:  # La palabra es demasiado
                            # larga para una línea. NOTA: La parto a 30, que
                            # seguro que cabe.
                            palabrota = palabras.pop()
                            linea_a_imprimir.append(palabrota[:30])
                            palabras.append(palabrota[30:])
                        # c.drawString(xdescripcion, linea,
                        #              escribe(" ".join(linea_a_imprimir)))
                        if alineacion_descripcion < 0:
                            c.drawString(xdescripcion, linea,
                                         escribe(" ".join(linea_a_imprimir)))
                        elif alineacion_descripcion > 0:
                            c.drawRightString(x0precio - 0.1*cm, linea,
                                escribe(" ".join(linea_a_imprimir)))
                        else:
                            c.drawCentredString((xdescripcion + x0precio) / 2,
                                linea, escribe(" ".join(linea_a_imprimir)))
                        if palabras:    # Si no quedan palabras no tengo que
                                        # pasar de línea, queda por escribir
                                        # el precio y eso en la actual.
                            linea = sigLinea()
                # --------- >8 ----------
                c.setFont(fuente, tamanno)
                if isinstance(l['precio'], str):
                    c.drawRightString(xprecio, linea, escribe(l['precio']))
                else:
                    try:
                        c.drawRightString(xprecio,
                                    linea,
                                    escribe(utils.float2str(l['precio'], 3)))
                    except ValueError, msg:
                        raise ValueError, msg
                c.setFont(fuente, tamanno)
                try:
                    total=utils._float(l['precio'])*utils._float(l['cantidad'])
                    c.drawRightString(xtotal, linea,
                                      escribe(utils.float2str(total, 2)))
                except ValueError, msg:
                    total = 0
                suma += total
                if l['descuento'] != "" and float(l['descuento']) != 0:
                    linea = sigLinea()
                    c.drawString(xdescripcion, linea,
                                 escribe('    DESCUENTO %.2f %%' % (
                                    float(l['descuento'])*100)))
                    desctotal = float('-'+l['descuento'])*total
                    suma += desctotal
                    c.drawRightString(xtotal, linea,
                                      escribe(utils.float2str(desctotal)))
                linea = sigLinea(20)
            # END OF for l in lineas:

        if buff == []:    # Si no va a haber segunda página, escribo los
                            # cuadros de los totales.
            # -- Cuadro final
            c.setFont('Times-Roman', 8)
            c.drawString(lm + 0.5*inch, bm+inch+90,
                         "IMPORTA LA PRESENTE PREFACTURA:")

            rectangulo(c, (lm+0.5*inch, bm+inch+88), (rm-2.2*inch, bm+inch+30))
            origen = lm+0.5*inch + 4
            linea = bm + inch + 75
            # DATA
            if texto != None:
                c.setFont('Helvetica', 10)
                lineas_agregadas = agregarFila(origen, linea, rm - 2.2*inch,
                                               escribe(texto), c, "Helvetica",
                                               10)
                for i in xrange(lineas_agregadas):  # @UnusedVariable
                    linea = sigLinea()
            c.saveState()
            c.setFont('Times-Roman', 8)
            if factdata['observaciones'] != "":
                texto = escribe("Obs.: %s" % (factdata['observaciones']))
            else:
                texto = ""
            agregarFila(lm + 0.6*inch, linea, rm-2.2*inch, texto, c,
                        "Times-Roman", 8)
            c.restoreState()


            # -- Arancel
            if arancel != None and arancel.strip() != "":
                rectangulo(c, (lm+0.5*inch, bm+inch+21), (rm, bm+inch+7),
                           'ARANCEL:')
                c.drawString(lm+1.4*inch, bm+inch+11,
                             escribe(arancel+'  Exención del I.V.A. Art. 25 '\
                             '1.a Ley 37/1992 de 29 de Diciembre del I.V.A.'))


            # -- Totales
            if totales['irpf'] != "0 %":
                linea = bm+2.2*inch
            else:
                linea = bm+2.1*inch
            c.drawString(rm-2.1*inch, linea, escribe('Subtotal'))
            rectangulo(c, (rm-1.2*inch, linea+10), (rm, linea-4),
                       totales['subtotal'], 'derecha')
            linea = sigLinea()
            if totales['descuento'] != None:
                c.drawString(rm-2.1*inch, linea, escribe('Descuento'))
                rectangulo(c, (rm-1.2*inch, linea+10), (rm, linea-4),
                           totales['descuento'], 'derecha')

            linea = sigLinea()
            #c.drawString(rm-2.1*inch, linea,
            # escribe('IVA ('+totales['iva']+')'))
            #rectangulo(c, (rm-1.2*inch, linea+10), (rm, linea-4),
            # totales['totaliva'], 'derecha')
            linea = sigLinea()
            if totales['irpf'] != "0 %":
                c.drawString(rm-2.1*inch, linea,
                             escribe('IRPF (%s)' % (totales['irpf'])))
                rectangulo(c, (rm-1.2*inch, linea+10), (rm, linea-4),
                           totales['totirpf'], 'derecha')
                linea = sigLinea()
            #c.drawString(rm-2.1*inch, linea, escribe('TOTAL'))
            #rectangulo(c, (rm-1.2*inch, linea+10), (rm, linea-4),
            # totales['total'], 'derecha')
            c.setFont("Helvetica", 10)
            # -- TEXTO
            origen = lm+0.5*inch
            linea = bm+0.85*inch
            rectangulo(c, (origen, bm+inch), (rm, bm))
            # DATA
            if vencimiento != None:
                xvencimiento = lm+0.5*inch+4
                c.drawString(xvencimiento, linea,
                             escribe('VENCIMIENTO: ' + vencimiento['fecha']))
                linea = sigLinea()
                if (vencimiento['pago']
                    and vencimiento['pago'].strip() != "0"
                    and vencimiento['pago'].strip() != ""):
                    c.drawString(xvencimiento, linea,
                        escribe('FORMA DE PAGO: ' + vencimiento['pago']))
                    linea = sigLinea()
                c.drawString(xvencimiento, linea,
                             escribe('DOCUMENTO DE PAGO: '))
                origen = lm + 2.2*inch
                textoDocumento = vencimiento['documento']
                longitud = c.stringWidth(textoDocumento, 'Helvetica', 10)
                longitudLimite = rm - origen
                if longitud < longitudLimite:
                    c.drawString(origen, linea, escribe(textoDocumento))
                else:
                    renglones = longitud / longitudLimite
                    renglones = int(renglones) + 1
                    corte = int(len(textoDocumento)/renglones)
                    memcorte = corte
                    for i in range(renglones):  # @UnusedVariable
                        while (len(textoDocumento) > corte
                               and textoDocumento[corte-1] != ' '
                               and corte < 2*memcorte):
                            corte += 1
                        if corte == 2*memcorte:
                            corte = memcorte
                        c.drawString(origen, linea,
                                     escribe(textoDocumento[:corte]))
                        linea = sigLinea()
                        textoDocumento = textoDocumento[corte:]
                        corte = memcorte

        else:
            textopaginas = "Página %d de %d" % (numpagina, paginastotales)
            c.drawRightString(rm - 0.1 * cm, bm + 0.8 * inch, textopaginas)


        bm, tm = bmbak, tmbak

        # Salvamos la página
        c.showPage()
        lineas = buff[:11]
        buff = buff[11:]

    # Salvamos el documento
    c.save()
    return nomarchivo


def abono(cliente, factdata, lineasAbono, lineasDevolucion, arancel,
          vencimiento, texto, totales, impuesto = 1.21,
          facturas_abonadas = None, 
          orden_ventanas = None):
    """
    Con los datos de entrada genera la factura.

    @params

    cliente --> es un diccionario con:
        - 'numcli' Número de cliente
        - 'nombre'
        - 'cif'
        - 'direccion'
        - 'cp'
        - 'localidad'
        - 'pais'
        - 'telf'
        - 'fax'

    factdata --> datos de la cabecera de la factura, es diccionario con:
        - 'facnum' Número de factura
        - 'fecha'
        - 'pedido'
        - 'albaranes'
        - 'observaciones'

    lineas --> datos del cuerpo de la factura, es una lista (un elemento
    por línea) de diccionarios con:
        - 'codigo'
        - 'cantidad'
        - 'descripcion'
        - 'precio' precio unitario
        - 'descuento'

    arancel --> una cadena con el código de arancel, si no es para extranjero
                es None y se aplica el impuesto. Con arancel el impuesto es 0

    vencimiento --> diccionario con:
        'fecha' --> fecha de vencimiento
        'pago' --> forma de pago
        'documento' --> es un diccionario con...^H^H^H^H^H^H DE DICCIONARIO
                        NADA, MONADA.

    texto --> cadena que se pone en el cuadro IMPORTA LA PRESENTE FACTURA

    totales -->diccionario con:
        -'subtotal'
        -'cargo' None si no tiene
        -'descuento' None si no tiene
        -'totaliva'
        -'total'

    impuesto --> valor numerico con el impuesto aplicado. Con arancel se pone
                 a 0 automaticamente
    """
    datos_empresa = pclases.DatosDeLaEmpresa.select()[0]
    if orden_ventanas is None:  # Solo si no recibo el parámetro miro la 
                                # configuración general.
        try:
            orden_ventanas = pclases.config.get_orden_ventanas()
        except:
            orden_ventanas = "cf"  # Orden por defecto.

    global linea#, tm, lm, rm, bm
    tm, bm, lm, rm = (680, 56.69, 05.35, 566.92)
    tmbak, bmbak, lmbak, rmbak = tm, bm, lm, rm = (680, 56.69, 05.35, 566.92)  # @UnusedVariable
    x, y = lm, tm  # @UnusedVariable
    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
                              "factura_abono_%s.pdf" % give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo)
    suma = 0.0
    lineas = lineasAbono + lineasDevolucion
    # Caben 11 líneas por página. Tenemos que cortar de 11 en 11 para las
    # distintas páginas que pudiera haber
    numpagina = 0
    from math import ceil
    paginastotales = ceil(len(lineas) / 11.0)
    buffer_texto = texto
    buff = lineas[11:]
    lineas = lineas[:11]
    while (lineas != []):
        bm, tm = bmbak, tmbak
        numpagina += 1
        # La cabecera
        c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', datos_empresa.logo),
                    lm+0.5*inch, height - 1.5*inch, 1.5*inch, 1.5*inch)
        if datos_empresa.bvqi:
            c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', datos_empresa.logoiso2),
                        rm-1.65*inch, height - 2.5*cm, 3.3*cm, 1.85*cm)

        linea = height-50
        c.setFont("Helvetica", 18)
        c.drawCentredString(rm-inch, tm+1*inch, escribe('Factura de abono'))
        c.drawCentredString(width/2, linea, escribe(datos_empresa.nombre))
        linea = sigLinea()
        c.setFont("Helvetica", 10)
        c.drawCentredString(width/2, linea,
                            escribe(datos_empresa.dirfacturacion))
        linea = sigLinea()
        c.drawCentredString(width/2, linea, escribe('%s %s%s, %s' % (
            datos_empresa.cpfacturacion,
            datos_empresa.ciudadfacturacion,
            datos_empresa.provinciafacturacion
                != datos_empresa.ciudadfacturacion
                and " (%s)" % (datos_empresa.provinciafacturacion) or "",
            datos_empresa.paisfacturacion)))
        linea = sigLinea()
        c.drawCentredString(width/2, linea, escribe('%s: %s' % (
            datos_empresa.str_cif_o_nif(), datos_empresa.cif)))
        linea = sigLinea()
        if datos_empresa.bvqi:
            # Marcado CE Geotextiles
            anchotexto = c.stringWidth(
                            escribe('Geotextiles CE 1035-CPD-ES033858'),
                            "Courier", 8)
            anchosemitexto = c.stringWidth(
                                escribe('Geotextiles '),
                                "Courier", 8)
            posx = (width - anchotexto)/2 
            cursiva(c, posx,
                    linea,
                    escribe('Geotextiles    1035-CPD-ES033858'),
                    "Courier", 8, (0, 0, 0), 10)
            c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', "CE.png"),
                        posx + anchosemitexto, 
                        linea, 
                        0.40*cm, 
                        0.20*cm)
            # Marcado CE fibra
            anchotexto = c.stringWidth(
                            escribe('Fibra CE 1035-CPD-9003712'),
                            "Courier", 8)
            anchosemitexto = c.stringWidth(
                                escribe('Fibra '),
                                "Courier", 8)
            posx = (width - anchotexto)/2 
            cursiva(c, posx,
                    linea - 8,
                    escribe('Fibra    1035-CPD-9003712'),
                    "Courier", 8, (0, 0, 0), 10)
            c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', "CE.png"),
                        posx + anchosemitexto, 
                        linea - 8, 
                        0.40*cm, 
                        0.20*cm)
        c.setFont("Helvetica", 10)


        # La fecha y el número de factura fuera del cuadro
        linea = sigLinea(15)
        c.setFont("Times-Italic", 10)
        c.drawString(lm + 3 * cm, linea, escribe('FECHA FACTURA:'))
        xNumFactura = width/2 + 3 * cm
        c.drawString(xNumFactura, linea, escribe('Nº FACTURA:'))
        c.setFont("Helvetica-Bold", 10)
        c.drawString(lm + 3 * cm +
                     c.stringWidth('FECHA FACTURA: ', 'Times-Italic', 10),
                     linea, escribe(factdata['fecha']))
        xNumFactura = width/2 + 3 * cm + c.stringWidth('Nº FACTURA: ',
                                                        'Times-Italic', 10)
        c.drawString(xNumFactura, linea, escribe(factdata['facnum']))

        # Los cuadros de datos fiscales y datos de envío
        xLocal = lm+inch
        xFact = width/2 + 0.7*inch
        xLocalTitulo = xLocal - 37
        xFactTitulo = xFact - 37

        linea = sigLinea(2)

        # La doble línea:
        c.saveState()
        c.setStrokeColorRGB(0.1, 0.1, 1.0)
        c.line(xLocalTitulo, linea-4, rm, linea-4)
        c.line(xLocalTitulo, linea-1, rm, linea-1)
        c.restoreState()

        # El doble rectángulo
        c.saveState()
        c.setLineWidth(0.5)
            # ------
        c.line(xLocalTitulo, linea-8, rm, linea-8)
        c.line(xLocalTitulo+2, linea-10, rm-2, linea-10)
            # ______
        c.line(xLocalTitulo+2, linea-8-15, rm-2, linea-8-15)
        c.line(xLocalTitulo, linea-10-15, rm, linea-10-15)
            # |
        c.line(xLocalTitulo, linea-8, xLocalTitulo, linea-10-15)
        c.line(xLocalTitulo+2, linea-10, xLocalTitulo+2, linea-8-15)
            #      |
        c.line(rm-2, linea-10, rm-2, linea-8-15)
        c.line(rm, linea-8, rm, linea-10-15)
        c.drawString(xLocalTitulo + 14, linea - 20,
                     escribe('Cliente: %s' % (cliente['numcli'])))
        c.drawString(width/2 + 10, linea - 20,
                     escribe('CIF: %s' % (cliente['cif'])))
        c.restoreState()

        linea = sigLinea(35) # Ponia 10
        c.setFont("Helvetica", 8)
        txti, txtd = "Dirección de correspondencia:", "Dirección fiscal:"
        if orden_ventanas == "fc":
            txti, txtd = txtd, txti
        # Aprovecho para limpiar datos. No sé de dónde habrán sacado los datos 
        # de algunos clientes, pero vienen repletos de tabuladores, que se 
        # convierten después en cuadrados negros en el PDF.
        txti,txtd=txti.replace("\t", "").strip(),txtd.replace("\t", "").strip()
        c.drawString(xLocalTitulo, linea-1,escribe(txti))
        c.drawString(xFactTitulo, linea-1, escribe(txtd))
        c.setFont("Helvetica", 10)
        rectangulo(c, (lm+0.45*inch, tm - 0.1 * cm),
                    (xFact-50, tm-inch - 0.1 * cm), doble = True)
        rectangulo(c, (xFact-40,     tm - 0.1 * cm),
                    (rm, tm-inch - 0.1 * cm), doble = True)
        ### DATA
        linea = tm+0.45*inch-30
        linea = sigLinea()

        c.setFont("Helvetica", 8)
        c.drawString(xLocalTitulo, linea, escribe('Nombre:'))
        c.drawString(xFactTitulo, linea, escribe('Nombre:'))
        c.setFont("Helvetica", 10)
        txti, txtd = cliente['nombre'], cliente['nombref']
        if orden_ventanas == "fc":
            txti, txtd = txtd, txti
        # Aprovecho para limpiar datos. No sé de dónde habrán sacado los datos 
        # de algunos clientes, pero vienen repletos de tabuladores, que se 
        # convierten después en cuadrados negros en el PDF.
        txti,txtd=txti.replace("\t", "").strip(),txtd.replace("\t", "").strip()
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xLocal,
            xFact - 50, linea, txti)
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xFact, rm - 2,
                                            linea, txtd)
        linea = sigLinea()
        c.setFont("Helvetica", 8)
        c.drawString(xLocalTitulo, linea, escribe('Dirección:'))
        c.drawString(xFactTitulo, linea, escribe('Dirección:'))
        c.setFont("Helvetica", 10)
        txti, txtd = cliente['direccion'], cliente['direccionf']
        if orden_ventanas == "fc":
            txti, txtd = txtd, txti
        # Aprovecho para limpiar datos. No sé de dónde habrán sacado los datos 
        # de algunos clientes, pero vienen repletos de tabuladores, que se 
        # convierten después en cuadrados negros en el PDF.
        txti,txtd=txti.replace("\t", "").strip(),txtd.replace("\t", "").strip()
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xLocal,
            xFact - 50, linea, txti)
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xFact, rm - 2,
            linea, txtd)
        linea = sigLinea()
        c.setFont("Helvetica", 8)
        c.drawString(xLocalTitulo, linea, escribe('Localidad:'))
        c.drawString(xFactTitulo, linea, escribe('Localidad:'))
        c.setFont("Helvetica", 10)
        txti, txtd = cliente['localidad'], cliente['localidadf']
        if orden_ventanas == "fc":
            txti, txtd = txtd, txti
        # Aprovecho para limpiar datos. No sé de dónde habrán sacado los datos 
        # de algunos clientes, pero vienen repletos de tabuladores, que se 
        # convierten después en cuadrados negros en el PDF.
        txti,txtd=txti.replace("\t", "").strip(),txtd.replace("\t", "").strip()
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xLocal,
            xFact - 50, linea, txti)
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xFact, rm - 2,
            linea, txtd)
        linea = sigLinea()
        c.setFont("Helvetica", 8)
        c.drawString(xLocalTitulo, linea, escribe('CP:'))
        c.drawString(xFactTitulo, linea, escribe('CP:'))
        c.setFont("Helvetica", 10)
        txti, txtd = ("%s %s" % (cliente['cp'], cliente['provincia']), 
                      "%s %s" % (cliente['cpf'], cliente['provinciaf']))
        if orden_ventanas == "fc":
            txti, txtd = txtd, txti
        # Aprovecho para limpiar datos. No sé de dónde habrán sacado los datos 
        # de algunos clientes, pero vienen repletos de tabuladores, que se 
        # convierten después en cuadrados negros en el PDF.
        txti,txtd=txti.replace("\t", "").strip(),txtd.replace("\t", "").strip()
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xLocal,
            xFact - 50, linea, txti)
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xFact, rm - 2,
            linea, txtd)
        linea = sigLinea()
        c.setFont("Helvetica", 8)
        c.drawString(xLocalTitulo, linea, escribe('País:'))
        c.drawString(xFactTitulo, linea, escribe('País:'))
        c.setFont("Helvetica", 10)
        txti, txtd = cliente['pais'], cliente['paisf']
        if orden_ventanas == "fc":
            txti, txtd = txtd, txti
        # Aprovecho para limpiar datos. No sé de dónde habrán sacado los datos 
        # de algunos clientes, pero vienen repletos de tabuladores, que se 
        # convierten después en cuadrados negros en el PDF.
        txti,txtd=txti.replace("\t", "").strip(),txtd.replace("\t", "").strip()
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xLocal,
                                            xFact - 50, linea, txti)
        el_encogedor_de_fuentes_de_doraemon(c, "Helvetica", 10, xFact, rm - 2,
                                            linea, txtd)

        linea = sigLinea(10)

        if facturas_abonadas != None and facturas_abonadas.strip() != "":
            c.drawString(lm + 0.5*inch, tm - 1.4 * inch,
                         escribe('Facturas abonadas: %s' % facturas_abonadas))

        if numpagina < paginastotales:
            offset = -1.5 * cm
            linea += offset
            bm += offset
            tm += offset

        # El cuerpo
        # -- Cuadro global
        rectangulo(c, (lm+0.5*inch, tm-0.75*inch-58), (rm, bm+inch+98))
        # -- Cabeceras
        rectangulo(c, (lm+0.5*inch, tm-0.75*inch-58),
                   (lm+1.65*inch, tm-0.75*inch-74), 'Código', 'centro')
        rectangulo(c, (lm+1.65*inch, tm-0.75*inch-58),
                   (lm+2.5*inch, tm-0.75*inch-74), 'Cantidad', 'centro')
        rectangulo(c, (lm+2.5*inch, tm-0.75*inch-74),
                   (rm-2.15*inch, tm-0.75*inch-74), 'Descripción', 'centro')
        rectangulo(c, (rm-2.15*inch, tm-0.75*inch-58),
                   (rm-1.2*inch, tm-0.75*inch-74), 'Precio Unitario', 'centro')
        rectangulo(c, (rm-1.2*inch, tm-0.75*inch-58),
                   (rm, tm-0.75*inch-74), 'TOTAL', 'centro')

        # -- Columnas de datos
        rectangulo(c,(lm+0.5*inch, tm-0.75*inch-74),(lm+1.65*inch, bm+inch+98))
        rectangulo(c,(lm+1.65*inch, tm-0.75*inch-74),(lm+2.5*inch, bm+inch+98))
        rectangulo(c,(lm+2.5*inch, tm-0.75*inch-74),(rm-2.15*inch, bm+inch+98))
        rectangulo(c,(rm-2.15*inch, tm-0.75*inch-74),(rm-1.2*inch, bm+inch+98))
        rectangulo(c,(rm-1.2*inch, tm-0.75*inch-74),(rm, bm+inch+98))


        # DATA
        # Caben exactamente 11 líneas de venta. Debemos hacer una
        # segunda página en caso de que haya más

        linea = tm-1.92*inch
        xcodigo = lm+1.65*inch-4
        xcantidad = lm+1.9*inch
        xdescripcion = lm+2.5*inch+3
        xprecio = rm-1.25*inch
        xtotal = rm-0.2*inch
        if lineas != None:
            for l in lineas:
                fuente, tamanno = "Helvetica", 10
                c.setFont(fuente, tamanno)
                c.drawRightString(xcodigo, linea, escribe(l['codigo']))
                cantidad_sin_cero = utils.float2str(
                                        utils._float(l['cantidad']), 2) # WTF?
                # XXX Si no es un float, que salte la excepción.
                # i 10096
                el_encogedor_de_fuentes_de_doraemon(c, fuente, tamanno, 
                                                    xcantidad - 15, 
                                                    xdescripcion - 3,
                                                    linea, cantidad_sin_cero, 
                                                    1)
                # c.drawRightString(xdescripcion-5, linea,
                #                   escribe(cantidad_sin_cero))
                # TODO: Si la descripción pasa de 2 líneas, la cagaste Burt
                #       Lancaster. Ya no cabrían 11 productos y los últimos se
                #       irían del cuadro.
                c.setFont("Helvetica", 10)
                descripcion = l['descripcion']
                origen = xdescripcion
                limite = rm-2.4*inch
                # --------- 8< ----------
                longitud = c.stringWidth(descripcion, 'Helvetica', 10)
                longitudLimite = limite - origen
                lineasSumadas = 1  # @UnusedVariable
                if longitud < longitudLimite:
                    c.drawString(origen, linea, escribe(descripcion))
                else:
                    palabras = descripcion.split(" ")
                    palabras.reverse()
                    while palabras: # Mientras queden palabras
                        linea_a_imprimir = []
                        while (c.stringWidth(" ".join(linea_a_imprimir),
                                            'Helvetica', 10) <= longitudLimite
                               and palabras):
                            linea_a_imprimir.append(palabras.pop())
                        if (c.stringWidth(" ".join(linea_a_imprimir),
                                          'Helvetica', 10) > longitudLimite):
                            palabras.append(linea_a_imprimir.pop())
                        if linea_a_imprimir == []:  # La palabra es demasiado
                                # larga para una línea. NOTA: La parto a 30,
                                # que seguro que cabe.
                            palabrota = palabras.pop()
                            linea_a_imprimir.append(palabrota[:30])
                            palabras.append(palabrota[30:])
                        c.drawString(xdescripcion, linea,
                                     escribe(" ".join(linea_a_imprimir)))
                        if palabras:    # Si no quedan palabras no tengo que
                                # pasar de línea, queda por escribir el precio
                                # y eso en la actual.
                            linea = sigLinea()
                # --------- >8 ----------
                c.rotate(90)
                c.setFont("Times-Roman", 8)
                c.drawCentredString(height/2, -lm-32,
                                    escribe(datos_empresa.registroMercantil))
                c.rotate(-90)
                c.setFont("Helvetica", 10)

                c.setFont("Helvetica", 10)
                try:
                    c.drawRightString(xprecio, linea,
                                      escribe(l['precio']))
                except:
                    c.drawRightString(xprecio, linea,
                                      escribe(utils.float2str(l['precio'], 3)))
                c.setFont("Helvetica", 10)
                total = utils._float(l['precio'])* utils._float(l['cantidad'])
                c.drawRightString(xtotal, linea,
                                  escribe(utils.float2str(total, 2)))
                suma += total
                if l['descuento'] != "" and float(l['descuento']) != 0:
                    linea = sigLinea()
                    c.drawString(xdescripcion, linea,
                        escribe('    DESCUENTO %.2f %%' % (
                            utils._float(l['descuento'])*100)))
                    desctotal = utils._float('-'+l['descuento'])*total
                    suma += desctotal
                    c.drawRightString(xtotal, linea,
                                      escribe(utils.float2str(desctotal)))
                linea = sigLinea(20)

        if buff == []:    # Si no va a haber segunda página, escribo los
                            # cuadros de los totales.
            # -- Cuadro final
            c.saveState()
            c.setFont('Times-Roman', 8)
            c.drawString(lm + 0.5*inch, bm+inch+90,
                         "IMPORTA LA PRESENTE FACTURA:")

            rectangulo(c, (lm+0.5*inch, bm+inch+88), (rm-2.2*inch, bm+inch+30))
            origen = lm+0.5*inch + 4
            linea = bm + inch + 75
            # DATA
            c.setFont('Helvetica', 10)
            if texto != None:
                longitud = c.stringWidth(texto, 'Helvetica', 10)
                longitudLimite = (rm - 2.2*inch) - origen
                lineasSumadas = 1  # @UnusedVariable
                if longitud < longitudLimite:
                    c.drawString(origen, linea, escribe(texto))
                else:
                    linea = sigLinea(-15)
                    renglones = longitud / longitudLimite
                    renglones = int(renglones) + 1
                    corte = int(len(texto)/renglones)
                    memcorte = corte
                    for i in range(renglones):  # @UnusedVariable
                        while (len(texto) > corte and texto[corte-1] != ' '
                               and corte < 2*memcorte):
                            corte += 1
                        if corte == 2*memcorte:
                            corte = memcorte
                        linea = sigLinea()
                        c.drawString(origen, linea, escribe(texto[:corte]))
                        texto = texto[corte:]
                        corte = memcorte
                texto = buffer_texto
            linea = sigLinea()
            c.restoreState()
            c.saveState()
            c.setFont('Times-Roman', 8)
            if factdata['observaciones'] != "":
                texto = escribe("Obs.: %s" % (factdata['observaciones']))
            else:
                texto = ""
            agregarFila(lm + 0.6*inch, linea, rm-2.2*inch, texto, c,
                        "Times-Roman", 8)
            c.restoreState()


            # -- Arancel
            if arancel != None and arancel.strip() != "":
                rectangulo(c, (lm+0.5*inch, bm+inch+21), (rm, bm+inch+7),
                           'ARANCEL:')
                impuesto = 0  # @UnusedVariable
                c.drawString(lm+1.4*inch, bm+inch+11,
                    escribe(arancel+'  Exención del I.V.A. Art. 25 1.a '\
                            'Ley 37/1992 de 29 de Diciembre del I.V.A.'))


            # -- Totales
            linea = bm+2.1*inch
            c.drawString(rm-2.1*inch, linea, escribe('Subtotal'))
            rectangulo(c, (rm-1.2*inch, linea+10), (rm, linea-4),
                       "%s €" % (totales['subtotal']), 'derecha')
            linea = sigLinea()
            if totales['descuento'] != None:
                c.drawString(rm-2.1*inch, linea, escribe('Descuento'))
                rectangulo(c, (rm-1.2*inch, linea+10), (rm, linea-4),
                           "%s €" % (totales['descuento']), 'derecha')

            linea = sigLinea()
            if "%" not in totales['iva']:
                totales['iva'] += " %"
            c.drawString(rm-2.1*inch, linea,
                         escribe('IVA ('+totales['iva']+')'))
            rectangulo(c, (rm-1.2*inch, linea+10), (rm, linea-4),
                       "%s €" % (totales['totaliva']), 'derecha')
            linea = sigLinea()
            c.drawString(rm-2.1*inch, linea, escribe('TOTAL'))
            rectangulo(c, (rm-1.2*inch, linea+10), (rm, linea-4),
                       "%s €" % (totales['total']), 'derecha')
            c.setFont("Helvetica", 10)
            # -- TEXTO
            origen = lm+0.5*inch
            linea = bm+0.85*inch
            rectangulo(c, (origen, bm+inch), (rm, bm))
            # DATA
            if vencimiento != None:
                xvencimiento = lm+0.5*inch+4
                c.drawString(xvencimiento, linea,
                             escribe('VENCIMIENTO: '+vencimiento['fecha']))
                linea = sigLinea()
                c.drawString(xvencimiento, linea,
                             escribe('FORMA DE PAGO: '+vencimiento['pago']))
                linea = sigLinea()
                c.drawString(xvencimiento, linea,
                             escribe('DOCUMENTO DE PAGO: '))
                origen = lm + 2.2*inch
                textoDocumento = vencimiento['documento']
                longitud = c.stringWidth(textoDocumento, 'Helvetica', 10)
                longitudLimite = rm - origen
                if longitud < longitudLimite:
                    c.drawString(origen, linea, escribe(textoDocumento))
                else:
                    renglones = longitud / longitudLimite
                    renglones = int(renglones) + 1
                    corte = int(len(textoDocumento)/renglones)
                    memcorte = corte
                    for i in range(renglones):  # @UnusedVariable
                        while (len(textoDocumento) > corte
                               and textoDocumento[corte-1] != ' '
                               and corte < 2*memcorte):
                            corte += 1
                        if corte == 2*memcorte:
                            corte = memcorte
                        c.drawString(origen, linea,
                                     escribe(textoDocumento[:corte]))
                        linea = sigLinea()
                        textoDocumento = textoDocumento[corte:]
                        corte = memcorte
        else:
            textopaginas = "Página %d de %d" % (numpagina, paginastotales)
            anchotextopaginas = c.stringWidth(texto, "Helvetica", 10)  # @UnusedVariable
            c.drawRightString(rm - 0.1 * cm, bm + 0.8 * inch, textopaginas)

        bm, tm = bmbak, tmbak
        # Pie de factura
        linea = bm-0.25*inch
            # Cuadro verde:
        c.saveState()
        c.setFillColorRGB(0.6, 1, 0.6)
        c.setStrokeColorRGB(0.6, 1, 0.6)
        c.rect(lm + 0.5 * inch, linea - 20, rm - (lm + 0.5 *inch), 15 * 2,
               stroke = 1, fill = 1)
            # 15 es el valor por defecto para el alto de una línea de texto.
        c.restoreState()

            # Texto dentro:
        c.setFont("Helvetica", 8)
        pos_pie = lm + 0.5 * inch + ((rm - (lm + 0.5 * inch)) / 2)
        if datos_empresa.direccion != datos_empresa.dirfacturacion:
            c.drawCentredString(pos_pie, linea,
                escribe('DIRECCIÓN DE OFICINAS Y CORRESPONDENCIA'\
                        ': %s. %s - %s (%s)' % (datos_empresa.direccion,
                                                datos_empresa.cp,
                                                datos_empresa.ciudad,
                                                datos_empresa.provincia)))
            linea = sigLinea()
            c.drawCentredString(pos_pie, linea,
                escribe('Tlf. %s  Fax %s' % (datos_empresa.telefono,
                                             datos_empresa.fax)))


        # Salvamos la página
        c.showPage()
        lineas = buff[:11]
        buff = buff[11:]

    # Salvamos el documento
    c.save()
    return nomarchivo




def empleados():
    """
    Crea un informe con el código asociado a cada empleado
    """
    archivo = os.path.join(gettempdir(),
                           'empleados_%s' % give_me_the_name_baby())
    titulo = 'Códigos de empleados'
    campos = [('Código', 20), ('Apellidos, Nombre', 60), ("DNI", 20)]
    empleados = pclases.Empleado.select(pclases.Empleado.q.activo == True,
                                        orderBy="apellidos")
    datos = []
    for e in empleados:
        datos.append((e.id, e.apellidos+', '+e.nombre, e.dni))
    return imprimir2(archivo, titulo, campos, datos)

def consulta_productividad(titulo, str_fecha, datos):
    """
    Construye y devuelve un PDF con los datos recibidos de la
    consulta de productividad global.
    """
    archivo = os.path.join(gettempdir(),
                           'productividad_global_%s' % give_me_the_name_baby())
    campos = (("Fecha", 25),
              ("Turno", 25),
              ("Producción", 25),
              ("Productividad", 25))
    return imprimir2(archivo, titulo, campos, datos, fecha = str_fecha,
                     cols_a_derecha = (2, 3))

def facturacion_por_cliente_y_fechas(titulo, fechaini, fechafin, datos):
    """
    Construye y devuelve un PDF con los datos recibidos.
    """
    archivo = os.path.join(gettempdir(),
        "facturacion_por_cliente_%s" % (give_me_the_name_baby()))
    campos = (('Factura', 20),
              ('Fecha', 10),
              ('Vencimiento', 10),
              ('Importe', 10),
              ('Fecha cobro', 10),
              ('Importe', 10),
              ('Pagaré', 10),
              ('Fecha', 10),
              ('Vencimiento', 10))
    str_fecha = "%s - %s" % (fechaini, fechafin)
    return imprimir2(archivo, titulo, campos, datos, fecha = str_fecha,
                     cols_a_derecha = (3, 5))

def trazabilidad(texto):
    """
    Simplemente vuelca el texto recibido en un PDF.
    """
    una_linea = -12
    tm, bm, lm, rm = (680, 56.69, 28.35, 566.92)
    nomarchivo = os.path.join(gettempdir(),
        "trazabilidad_%s.pdf" % (give_me_the_name_baby()))
    c = canvas.Canvas(nomarchivo)
    c.setPageSize(A4)
    fuente, tamanno = "Helvetica", 10
    c.setFont(fuente, tamanno)
    lineas = texto.split("\n")
    while lineas:
        cabecera(c, 'Informe de trazabilidad',
                 utils.str_fecha(mx.DateTime.localtime()))
        # Marca "borrador"
        c.saveState()
        c.setFont("Courier-BoldOblique", 42)
        ancho = c.stringWidth("BORRADOR", "Courier-BoldOblique", 42)
        c.translate(A4[0] / 2.0, A4[1] / 2.0)
        c.rotate(45)
        c.setLineWidth(3)
        c.setStrokeColorRGB(1.0, 0.7, 0.7)
        c.setFillColorRGB(1.0, 0.7, 0.7)
        c.rect((-ancho - 10) / 2.0, -5, (ancho + 10), 37, fill = False)
        c.drawCentredString(0, 0, "BORRADOR")
        c.rotate(-45)
        c.restoreState()
        # EOMarca "borrador"
        x, y = lm, tm + 2.5 * cm
        while y >= bm and lineas:
            linea = lineas.pop(0)
            saltos = agregarFila(x, y, rm, escribe(linea), c, fuente, tamanno,
                                 a_derecha = False, altura_linea = -una_linea)
            y += una_linea * saltos
        c.showPage()
    c.save()
    return nomarchivo

def crm_generar_pdf_detalles_factura(factura):
    """
    A partir de un objeto factura genera el PDF con su información CRM:
    - Datos de la factura.
    - Contactos.
    - Anotaciones.
    - Vencimientos.
    """
    assert isinstance(factura, (pclases.SuperFacturaVenta))
    una_linea = -12
    tm, bm, lm, rm = (680, 56.69, 28.35, 566.92)
    nomarchivo = os.path.join(gettempdir(),
        "crm_factura_%s_%s.pdf" % (factura.numfactura.replace("/", "_"), 
                                   give_me_the_name_baby()))
    c = canvas.Canvas(nomarchivo)
    c.setPageSize(A4)
    fuente, tamanno = "Helvetica", 10
    c.setFont(fuente, tamanno)
    # Preparo datos
    lineas = []
        # Datos de factura
    lineas.append(("Factura %s" % factura.numfactura, "Helvetica-Bold", 12))
    lineas.append(("    Cliente: %s" % factura.cliente.nombre, 
                   fuente, tamanno))
    if factura.obra and not factura.obra.generica:
        lineas.append(("    Obra: %s" % factura.obra.get_str_obra(), 
                       fuente, tamanno))
    lineas.append(("    Fecha: %s" % utils.str_fecha(factura.fecha), 
                   fuente, tamanno))
    lineas.append(("    Total: %s €" % utils.float2str(
        factura.calcular_importe_total()), fuente, tamanno))
    lineas.append(("    Vencido: %s €" % utils.float2str(
        factura.calcular_vencido()), fuente, tamanno))
    lineas.append(("    Cobrado: %s €" % utils.float2str(
        factura.calcular_cobrado()), fuente, tamanno))
    lineas.append(("    Pendiente de cobro: %s €" % utils.float2str(
        factura.calcular_pendiente_cobro()), fuente, tamanno))
    if factura.observaciones:
        lineas.append(("    Observaciones: %s" % factura.observaciones, 
                       fuente, tamanno))
        # Datos de contactos:
    if factura.obra and factura.obra.contactos:
        lineas.append(("", fuente, tamanno))
        lineas.append(("    Contactos:", "Helvetica-Bold", 10))
        for contacto in factura.obra.contactos:
            lineas.append(("        %s" % contacto.get_str_contacto(), 
                           fuente, tamanno))
        # Anotaciones
    if factura.notas:
        lineas.append(("", fuente, tamanno))
        lineas.append(("Anotaciones:", "Helvetica-Bold", 10))
        notas = list(factura.notas)
        notas.sort(key = lambda n: n.fechahora, reverse = True)
        for nota in notas:
            txtnota = nota.get_str_nota()
            lineas.append((txtnota, fuente, tamanno))
        # Vencimientos: 
    if factura.vencimientosCobro or factura.cobros:
        vtoscobros = factura.emparejar_vencimientos()
        lineas.append(("", fuente, tamanno))
        lineas.append(("Vencimientos y cobros:", "Helvetica-Bold", 10))
        txtvto = ""
        for vto in vtoscobros['vtos']:
            txtvto += "%s (%s €) [%s]" % (utils.str_fecha(vto.fecha), 
                                          utils.float2str(vto.importe), 
                                          vto.observaciones)
            lineas.append((txtvto, fuente, tamanno))
            if vtoscobros[vto]:
                for cobro in vtoscobros[vto]:
                    pagare_o_confirming = ""
                    if cobro.pagareCobro or cobro.confirming:
                        poc = cobro.pagareCobro or cobro.confirming
                        pagare_o_confirming = "%s %s, de %s €."\
                            " Recibido el %s. Vence el %s."\
                            " Fecha de cobro: %s" % (
                            isinstance(poc, pclases.PagareCobro) and "Pagaré" 
                                or "Confirming", 
                            poc.codigo, 
                            utils.float2str(poc.cantidad), 
                            utils.str_fecha(poc.fechaRecepcion), 
                            utils.str_fecha(poc.fechaCobro), 
                            utils.str_fecha(poc.fechaCobrado))
                    txtcobros = " * Cobrado el %s (%s €). %s [%s]" % (
                        utils.str_fecha(cobro.fecha), 
                        utils.float2str(cobro.importe), 
                        pagare_o_confirming, 
                        cobro.observaciones)
                    lineas.append((txtcobros, "Helvetica-Oblique", tamanno))
        if None in vtoscobros.keys():    # Hay cobros sin vencimientos:
            lineas.append(("Resto de cobros: ", fuente, tamanno))
            txtcobros = []
            for cobro in vtoscobros[None]:
                txtcobros.append("%s (%s €)" % (
                    utils.str_fecha(cobro.fecha), 
                    utils.float2str(cobro.importe)))
            txtcobros = "; ".join(txtcobros)
            lineas.append((txtcobros, fuente, tamanno))
    # EOPreparo datos
    #lineas = texto.split("\n")
    while lineas:
        cabecera(c, 'CRM: Detalles de factura. %s.' % factura.numfactura,
                 utils.str_fecha(mx.DateTime.localtime()))
        # Marca "borrador"
        #c.saveState()
        #c.setFont("Courier-BoldOblique", 42)
        #ancho = c.stringWidth("BORRADOR", "Courier-BoldOblique", 42)
        #c.translate(A4[0] / 2.0, A4[1] / 2.0)
        #c.rotate(45)
        #c.setLineWidth(3)
        #c.setStrokeColorRGB(1.0, 0.7, 0.7)
        #c.setFillColorRGB(1.0, 0.7, 0.7)
        #c.rect((-ancho - 10) / 2.0, -5, (ancho + 10), 37, fill = False)
        #c.drawCentredString(0, 0, "BORRADOR")
        #c.rotate(-45)
        #c.restoreState()
        # EOMarca "borrador"
        x, y = lm, tm + 2.5 * cm
        while y >= bm and lineas:
            linea, fuente, tamanno = lineas.pop(0)
            c.setFont(fuente, tamanno)
            saltos = agregarFila(x, y, rm, escribe(linea), c, fuente, tamanno,
                                 a_derecha = False, altura_linea = -una_linea)
            y += una_linea * saltos
        c.showPage()
    c.save()
    return nomarchivo


def texto_libre(texto, txtcabecera = "", incluir_fecha_del_dia = True):
    """
    Simplemente vuelca el texto recibido en un PDF.
    """
    una_linea = -12
    tm, bm, lm, rm = (680, 56.69, 28.35, 566.92)
    nomarchivo = os.path.join(gettempdir(),
        "trazabilidad_%s.pdf" % (give_me_the_name_baby()))
    c = canvas.Canvas(nomarchivo)
    c.setPageSize(A4)
    fuente, tamanno = "Courier", 10
    c.setFont(fuente, tamanno)
    lineas = texto.split("\n")
    while lineas:
        cabecera(c, txtcabecera, incluir_fecha_del_dia
                 and utils.str_fecha(mx.DateTime.localtime()) or "")
        x, y = lm, tm + 2.5 * cm
        while y >= bm and lineas:
            linea = lineas.pop(0)
            if len(linea) > 0:
                sangria = 0
                i = 0
                car = linea[i]
                while car == ' ' and i < len(linea):
                    sangria += 0.2*cm
                    i += 1
                    car = linea[i]
                x = lm + sangria
            saltos = agregarFila(x, y, rm, escribe(linea), c, fuente, tamanno,
                                 a_derecha = False, altura_linea = -una_linea)
            y += una_linea * saltos
        c.showPage()
    c.save()
    return nomarchivo


def listado_clientes_solo_riesgos(clientes):
    """
    Imprime un listado de clientes. Los clientes a
    imprimir los recibe como lista o como SelectResult.
    """
    archivo = os.path.join(gettempdir(),
                           'riesgos_%s' % give_me_the_name_baby())
    titulo = 'Listado de clientes'
    campos = [('Nombre', 26),
              ('CIF', 7),
              ('Dirección', 19),
              ('Teléfono', 9),
              ('Fax', 9),
              ('Correo-e', 10),
              ('Riesgo asegurado', 10),
              ('Riesgo concedido', 10)]
    datos = []
    fechafin = mx.DateTime.localtime()
    fechaini = mx.DateTime.DateTimeFrom(day=1, month=1, year=fechafin.year)  # @UnusedVariable
    total_comprado = total_pagado = total_pendiente = 0  # @UnusedVariable
    #dibujar_linea_divisoria = False
    for cli in clientes:
        #if dibujar_linea_divisoria:
        #    datos.append(("---",) * len(campos))
        #else:
        #    dibujar_linea_divisoria = True  # Me salto el primero.
        asegurado = cli.riesgoAsegurado
        if asegurado < 0:
            asegurado = " - "
        else:
            asegurado = "%s €" % utils.float2str(asegurado, 2)
        concedido = cli.riesgoConcedido
        if concedido < 0:
            concedido = " - "
        else:
            concedido = "%s €" % utils.float2str(concedido, 2)
        datos.append((cli.nombre,
                      cli.cif,
                      cli.get_direccion_completa(),
                      cli.telefono,
                      cli.fax,
                      cli.email,
                      asegurado,
                      concedido
                     ))
    return imprimir2(archivo, titulo, campos, datos,
                     utils.str_fecha(mx.DateTime.localtime()),
                     apaisado = True,
                     cols_a_derecha = (6, 7))

def listado_clientes(clientes):
    """
    Imprime un listado de clientes. Los clientes a
    imprimir los recibe como lista o como SelectResult.
    """
    archivo = os.path.join(gettempdir(),
                           'clientes_%s' % give_me_the_name_baby())
    titulo = 'Listado de clientes'
    campos = [('Nombre', 22),
              ('CIF', 7),
              ('Dirección', 13),
              ('Teléfono', 7),
              ('Fax', 7),
              ('Correo-e', 12),
              ('Forma de pago', 11),
              ('Total', 7),
              ('Cobrado', 7),
              ('Pendiente', 7)]
    datos = []
    fechafin = mx.DateTime.localtime()
    fechaini = mx.DateTime.DateTimeFrom(day=1, month=1, year=fechafin.year)
    total_comprado = total_pagado = total_pendiente = 0
    dibujar_linea_divisoria = False
    for cli in clientes:
        if dibujar_linea_divisoria:
            datos.append(("---", "---", "---", "---", "---", 
                          "---", "---", "---", "---", "---"))
        else:
            dibujar_linea_divisoria = True  # Me salto el primero.
        formapago = ""
        if cli.documentodepago != None and cli.documentodepago.strip() != "":
            formapago = "%s, " % (cli.documentodepago)
        if cli.vencimientos != None and cli.vencimientos.strip() != "":
            formapago += "%s " % (cli.vencimientos)
        if cli.diadepago != None and cli.diadepago.strip() != "":
            formapago += "los días %s" % (cli.diadepago)
        comprado = cli.calcular_comprado(fechaini, fechafin)
        pagado = cli.calcular_cobrado(fechaini, fechafin)
        pendiente = cli.calcular_pendiente_cobro(fechaini, fechafin)
        datos.append((cli.nombre,
                      cli.cif,
                      cli.get_direccion_completa(),
                      cli.telefono,
                      cli.fax,
                      cli.email,
                      formapago,
                      "%s €" % (utils.float2str(comprado)),
                      "%s €" % (utils.float2str(pagado)),
                      "%s €" % (utils.float2str(pendiente))
                     ))
        total_comprado += comprado
        total_pagado += pagado
        total_pendiente += pendiente
        # Créditos, obras y contactos de las obras:
        asegurado = cli.riesgoAsegurado
        if asegurado < 0:
            asegurado = " - "
        else:
            asegurado = "%s €" % utils.float2str(asegurado, 2)
        datos.append(("Riesgo asegurado: %s" % asegurado, 
                      "", "", "", "", "", "", "", "", ""))
        concedido = cli.riesgoConcedido
        if concedido < 0:
            concedido = " - "
        else:
            concedido = "%s €" % utils.float2str(concedido, 2)
        datos.append(("Riesgo concedido: %s" % concedido, 
                      "", "", "", "", "", "", "", "", ""))
        for obra in cli.obras:
            datos.append(("Obra: %s" % obra.nombre, 
                          "", 
                          obra.get_str_direccion(), 
                          "", "", "", "", "", "", ""))
            for contacto in obra.contactos:
                datos.append(("* %s" % contacto.get_str_contacto(), 
                              "", "", "", "", "", "", "", "", ""))
        comerciales_y_pedidos = cli.buscar_comerciales()
        for comercial in comerciales_y_pedidos:
            if not comercial:
                continue # Me salto los pedidos sin comercial (comercial None).
            pedidos = comerciales_y_pedidos[comercial]
            datos.append(("Comercial: %s (%d pedidos)" % (
                            comercial.get_nombre_completo(), 
                            len(pedidos)), 
                          "", "", "", "", "", "", "", "", ""))
    datos.append(("", "", "", "", "", "", "---", "---", "---", "---"))
    datos.append(("", "", "", "", "", "", "TOTAL",
                  "%s €" % (utils.float2str(total_comprado)),
                  "%s €" % (utils.float2str(total_pagado)),
                  "%s €" % (utils.float2str(total_pendiente)) ))
    return imprimir2(archivo, titulo, campos, datos,
                     utils.str_fecha(mx.DateTime.localtime()),
                     apaisado = True,
                     sobrecampos = (('Volumen de facturación en el año', 90),),
                     cols_a_derecha = (7, 8, 9))

def listado_proveedores(proveedores):
    """
    Imprime un listado de provedores. Los proveedores a
    imprimir los recibe como lista o como SelectResult.
    """
    archivo = os.path.join(gettempdir(),
                           'proveedores_%s' % give_me_the_name_baby())
    titulo = 'Listado de proveedores'
    campos = [('Nombre', 28),
              ('CIF', 7),
              ('Teléfono', 10),
              ('Fax', 10),
              ('Web', 10),
              ('Forma de pago', 11),
              ('Total', 8),
              ('Pagado', 8),
              ('Pendiente', 8)]
    datos = []
    fechafin = mx.DateTime.localtime()
    fechaini = mx.DateTime.DateTimeFrom(day=1, month=1, year=fechafin.year)
    total_comprado = total_pagado = total_pendiente = 0
    for pro in proveedores:
        formapago = ""
        if pro.documentodepago != None and pro.documentodepago.strip() != "":
            formapago = "%s, " % (pro.documentodepago)
        if pro.vencimiento != None and pro.vencimiento.strip() != "":
            formapago += "%s " % (pro.vencimiento)
        if pro.diadepago != None and pro.diadepago.strip() != "":
            formapago += "los días %s" % (pro.diadepago)
        comprado = pro.calcular_comprado(fechaini, fechafin)
        pagado = pro.calcular_pagado(fechaini, fechafin)
        pendiente = pro.calcular_pendiente_pago(fechaini, fechafin)
        datos.append((pro.nombre,
                      pro.cif,
                      pro.telefono,
                      pro.fax,
                      pro.web,
                      formapago,
                      "%s €" % (utils.float2str(comprado)),
                      "%s €" % (utils.float2str(pagado)),
                      "%s €" % (utils.float2str(pendiente))
                     ))
        total_comprado += comprado
        total_pagado += pagado
        total_pendiente += pendiente
    datos.append(("", "", "", "", "", "---", "---", "---", "---"))
    datos.append(("", "", "", "", "", "TOTAL",
                  "%s €" % (utils.float2str(total_comprado)),
                  "%s €" % (utils.float2str(total_pagado)),
                  "%s €" % (utils.float2str(total_pendiente)) ))
    return imprimir2(archivo,
                     titulo,
                     campos,
                     datos,
                     utils.str_fecha(mx.DateTime.localtime()),
                     apaisado = True,
                     sobrecampos = (('Volumen de compras en el año', 92), ),
                     cols_a_derecha = (6, 7, 8))

def bajoMinimos(titulo, datos, fecha, proveedor = ""):
    """
    Crea un informe con los productos por debajo del mínimo en almacen
    """
    archivo = os.path.join(gettempdir(),
                           'bajoMinimos_%s' % give_me_the_name_baby())
    campos = [('Código', 20),
              ('Descripción', 50),
              ('Mínimo', 10),
              ('Stock', 10)]
    if proveedor:
        titulo += ": " + proveedor
    return imprimir2(archivo, titulo, campos, datos, fecha = fecha)

def albaranesFacturados(datos, fecha = None, clienteproveedor = "Cliente"):
    """
    Crea un informe de los albaranes ya facturados para un periodo de fecha
    dado.
    """
    archivo = os.path.join(gettempdir(),
                           'facturados_%s' % give_me_the_name_baby())
    titulo = 'Albaranes facturados'
    campos = [('Fecha', 20), ('Nº Albarán', 20), (clienteproveedor, 40),
              ('Nº Factura', 20)]
    return imprimir2(archivo, titulo, campos, datos, fecha)

def albaranesSinFacturar(datos, fecha = None, clienteproveedor = "Cliente"):
    """
    Crea un informe de los albaranes NO facturados para un periodo de fecha
    dado.
    OBSOLETO. DEPRECATED.
    """
    archivo = os.path.join(gettempdir(),
                           'nofacturados_%s' % give_me_the_name_baby())
    titulo = 'Albaranes por facturar'
    campos = [('Fecha', 20), ('Nº Albarán', 20), (clienteproveedor, 60)]
    return imprimir2(archivo, titulo, campos, datos, fecha)


def compras(datos, fecha = None):
    """
    Crea un informe relativo a las compras realizadas en un periodo de fecha
    dado.
    """
    archivo = os.path.join(gettempdir(),
                           'compras_%s' % give_me_the_name_baby())
    titulo = 'Listado de compras'
    campos = [('Fecha', 15), ('Producto', 25), ('Cantidad', 10),
              ('Precio', 10), ('Nº Pedido', 20), ('Nº Albarán', 10)]
    return imprimir2(archivo, titulo, campos, datos, fecha)

def ventas(datos, fecha = None):
    """
    Crea un informe relativo a las ventas realizadas en un periodo de fecha
    dado.
    """
    archivo = os.path.join(gettempdir(), 'ventas_%s' % give_me_the_name_baby())
    titulo = 'Listado de ventas'
    campos = [('F. Alb.', 4),
              ('Producto', 12),
              ('Cantidad', 6),
              ('Precio', 5),
              ('Total', 6),
              ('Cliente', 14),
              ('Pedido', 7),
              ('Comercial', 7),
              ('Albarán', 4),
              ('Transporte', 5),
              ('Destino', 12),
              ('Factura', 4), 
              ('Forma de pago', 7), 
              ('Cobro real', 7)]
    return imprimir2(archivo, titulo, campos, datos, fecha,
                     cols_a_derecha = (2, 3, 4), apaisado = True)


def pedidosCliente(datos, cliente, fecha = None):
    """
    Crea un informe relativo a los pedidos realizados por un cliente dado
    """
    archivo = os.path.join(gettempdir(),
                           'pedidosCli_%s' % give_me_the_name_baby())
    titulo = 'Listado de pedidos de %s' % (cliente)
    campos = [('Cliente', 40), ('Fecha', 10), ('Nº pedido', 21),
              ('Importe', 10), ('Bloqueado', 7), ('Cerrado', 7)]
    return imprimir2(archivo, titulo, campos, datos, fecha,
                     cols_a_derecha = (3, 4, 5))

def albaranesCliente(datos, nombrecliente, fecha = None):
    """
    Crea un informe relativo a los albaranes realizados por un cliente dado
    """
    archivo = os.path.join(gettempdir(),
                           'albaranesCli_%s' % give_me_the_name_baby())
    titulo = 'Listado de albaranes%s' % (
                nombrecliente != "" and " de " + nombrecliente or "")
    campos = [('Cliente', 35), ('Fecha', 8), ('NºAlb.', 5),
              ('Destinatario', 37), ('Fras.', 15)]
    return imprimir2(archivo, titulo, campos, datos, fecha)

def incidencias(datos, fecha = None):
    """
    Crea un informe relativo a las incidencias en un periodo dado
    """
    archivo = os.path.join(gettempdir(),
                           'incidencias_%s' % give_me_the_name_baby())
    titulo = 'Listado de incidencias'
    campos = [('Tipo', 15), ('H.Inicio', 8), ('H.Fin', 8), ('Fecha', 10),
              ('Turno', 10), ('Observaciones', 49)]
    return imprimir2(archivo, titulo, campos, datos, fecha)

def imprimir_tarifa(datos, nombre = "", fecha = None):
    """
    Imprime una tarifa con su lista de precios.
    """
    archivo = os.path.join(gettempdir(), 'tarifa_%s' % give_me_the_name_baby())
    titulo = "Tarifa de precios %s" % (nombre)
    campos = [("Código", 20), ("Descripción", 50), ("Precio por defecto", 15),
              ("Precio tarifa", 15)]
    return imprimir2(archivo, titulo, campos, datos, fecha,
                     cols_a_derecha = (2, 3))

def vencimientosPago(datos, fecha = None):
    """
    Crea un informe relativo a las incidencias en un periodo dado
    """
    archivo = os.path.join(gettempdir(),
                           'venPago_%s' % give_me_the_name_baby())
    titulo = 'Vencimientos de pagos'
    campos = [('Factura', 12), ('Fecha', 12), ('Importe', 11),
              ('Observaciones', 35), ('Proveedor', 15)]
    return imprimir2(archivo, titulo, campos, datos, fecha)

def vencimientosCobro(datos, fecha = None):
    """
    Crea un informe relativo a las incidencias en un periodo dado
    """
    archivo = os.path.join(gettempdir(),
                           'venCobro_%s' % give_me_the_name_baby())
    titulo = 'Vencimientos de cobros'
    campos = [('Factura', 15), ('Fecha vto.', 15), ('Importe', 10),
              ('Observaciones', 35), ('Cliente', 25)]
    return imprimir2(archivo, titulo, campos, datos, fecha)

def entradasAlmacen(datos, fecha = None, cols_a_derecha = ()):
    """
    Crea un informe de valoración de entradas en almacén.
    """
    archivo = os.path.join(gettempdir(),
                           'entradasAlmacen_%s' % give_me_the_name_baby())
    titulo = 'Valoración de entradas en almacén'
    campos = [('Proveedor', 21),
              ('Albarán', 10),
              ('Fecha', 9),
              ('Producto', 25),
              ('Cantidad', 11),
              ('Precio', 11),
              ('Total', 13)]
    return imprimir2(archivo, titulo, campos, datos, fecha, cols_a_derecha)

def laboratorioLotes(datos, fecha = None):
    """
    Crea un informe con los resultados de pruebas
    sobre lotes en el laboratorio
    """
    archivo = os.path.join(gettempdir(),
                           'labLotes_%s' % give_me_the_name_baby())
    titulo = 'Pruebas de lotes'
    campos = [('NºLote', 15), ('Código', 15), ('Tenacidad', 15),
              ('Elongación', 15), ('Rizo', 10), ('Encogimiento', 15),
              ('Grasa', 15)]
    return imprimir2(archivo, titulo, campos, datos, fecha)


def laboratorioPartidas(datos, fecha = None):
    """
    Crea un informe con los resultados de pruebas
    sobre partidas en el laboratorio
    """
    archivo = os.path.join(gettempdir(),
                           'labPartidas_%s' % give_me_the_name_baby())
    titulo = 'Pruebas de partidas'
    campos = [('NºPartida', 13), ('Longitudinal', 11), ('Transversal', 11),
              ('Compresión', 11), ('Perforación', 11), ('Permeabilidad', 15),
              ('Poros', 9), ('Espesor', 11), ('Piramidal', 8)]
    return imprimir2(archivo, titulo, campos, datos, fecha)

def consumo_fibra_partida(datos, fecha = None, cols_a_derecha = ()):
    """
    Crea un informe con un listado de balas de fibra
    consumidas por una partida de geotextiles.
    """
    archivo = os.path.join(gettempdir(),
        'consumo_fibra_partida_%s' % give_me_the_name_baby())
    titulo = 'Carga %d.\nPartidas gtx.: %s' % (datos['partida'].numpartida,
                                               datos['partidas_gtx'])
    campos = [('Nº Bala', 40),
              ('Peso', 15),
              ("", 45)]
    return imprimir2(archivo, titulo, campos, datos['balas'], fecha,
                     cols_a_derecha)

def marcoParte(c, texto):
    """
    Dibuja la cabecera del parte
    """
    datos_empresa = pclases.DatosDeLaEmpresa.select()[0]

    rectangulo(c, (lm, tm+2*inch), (rm, bm-0.5*inch))
    c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', datos_empresa.logo),
                lm+0.1*inch, height - 1*inch, 0.7*inch, 0.7*inch)
    c.setFont("Helvetica", 20)
    c.drawString(lm+inch, height-0.8*inch, escribe(texto))
    c.line(lm, height-inch, rm, height-inch)
    c.setFont("Helvetica", 10)


def parteBalas(datos, lineas):
    """
    Crea un informe con los datos de
    un parte de la línea de fibra
    """
    global linea, tm, lm, rm, bm
    x, y = lm, tm  # @UnusedVariable
    global linea
    MAXLINEAS = 40

    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
                              "parteBalas_%s.pdf" % give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo)
    paginasTotales = len(lineas)/MAXLINEAS+1
    for i in range(paginasTotales):
        # La cabecera
        texto = 'CONTROL DE PRODUCCIÓN (Línea de fibras)'
        marcoParte(c, texto)
        linea = height-1.2*inch
        x1 = lm+4
        x2 = width/2 -inch
        x3 = rm - 2.5*inch
        # DONE?: Poner concatenaciones con los datos recibidos
        c.drawString(x1, linea, escribe('FECHA: '+datos['e_fecha']))
        c.drawString(x2, linea, escribe('DTEX: '+datos['e_dtex']))
        c.drawString(x3, linea, escribe('LOTE: '+datos['e_numlote']))
        linea = sigLinea()
        c.drawString(x1, linea, escribe('ARTICULO: '+datos['e_articulo']))
        c.drawString(x2, linea, escribe('LONGITUD: '+datos['e_longitud']))
        c.drawString(x3, linea, escribe('PROD/STAN: '+datos['e_o80']))
        linea = sigLinea()
        c.drawString(x1, linea, escribe('HORA COM.: '+datos['e_hora_ini']))
        c.drawString(x2, linea, escribe('HORA FIN: '+datos['e_hora_fin']))
        linea = sigLinea() + 4
        c.line(lm, linea, rm, linea)
        # Cuerpo
        linea = sigLinea()
        xnbala = lm + 5
        xpeso = xnbala + inch
        xmotivo = xpeso + 0.8*inch
        xcomienzo = xmotivo + 1.3*inch
        xfin = xcomienzo + 0.8*inch
        xduracion = xfin + 0.5*inch
        xobservaciones = xduracion + inch
        c.line(xnbala, linea-3, rm-0.8*inch, linea-3)

        c.drawString(xnbala, linea, escribe('Nº BALA'))
        c.drawString(xpeso, linea, escribe('PESO'))
        c.drawString(xmotivo, linea, escribe('MOTIVO PARADA'))
        c.drawString(xcomienzo, linea, escribe('H.INICIO'))
        c.drawString(xfin, linea, escribe('H.FIN'))
        c.drawString(xduracion, linea, escribe('DURACION'))
        c.drawString(xobservaciones, linea, escribe('OBSERVACIONES'))
        linea = sigLinea()
        # 40 lineas máximo
        auxLineas = lineas[:MAXLINEAS]
        for l in auxLineas:
            # Bala, peso, motivo parada, hora comienzo, hora terminacion,
            # duracion observaciones,
            if l[7]:
                tipob = ' B'
            else:
                tipob = ''
            c.drawString(xnbala, linea, escribe(l[0])+tipob)
            c.drawString(xpeso, linea, escribe(l[1]))
            c.drawString(xmotivo, linea, escribe(l[2]))
            c.drawString(xcomienzo, linea, escribe(l[3]))
            c.drawString(xfin, linea, escribe(l[4]))
            c.drawString(xduracion, linea, escribe(l[5]))
            c.drawString(xobservaciones, linea, escribe(l[6]))
            linea = sigLinea(14)
        # Datos Resumen
        x1 = lm + 4
        x2 = lm + 1.7*inch
        x3 = width/2
        x4 = x3 + 1.7*inch
        linea = bm + 0.9*inch
        c.drawString(x1, linea, escribe('Nº BALAS: '+datos['e_num_balas']))
        c.drawString(x2, linea, escribe('PESO TOTAL: '+datos['e_peso_total']))
        c.drawString(x3, linea,
            escribe('TR TRABAJADO: '+datos['e_tiempo_real_trabajado']))
        c.drawString(x4, linea,
            escribe('PRODUCTIVIDAD: '+datos['e_productividad']))
        c.line(lm, linea+14, rm, linea+14)
        linea = sigLinea()
        c.drawString(x1, linea, escribe('Nº BALAS A: '+datos['e_numA']))
        c.drawString(x2, linea, escribe('PESO TOTAL A: '+datos['e_pesoA']))
        c.drawString(x3, linea, escribe('Nº BALAS B: '+datos['e_numB']))
        c.drawString(x4, linea, escribe('PESO TOTAL B:: '+datos['e_pesoB']))

        # Pie
        linea = bm + 0.6*inch
        lineaAbajo = bm - 0.5*inch
        xobservaciones = lm + 4
        xempleados = width/2 +4
        rectangulo(c, (lm, linea), (width/2, lineaAbajo), 'OBSERVACIONES: ',
                   alinTxtY = 'arriba')
        rectangulo(c, (width/2, linea), (rm, lineaAbajo), 'OPERARIOS: ',
                   alinTxtY = 'arriba')
        linea = sigLinea() - 10
        agregarFila(xobservaciones, linea, width/2, datos['observaciones'], c,
                    "Helvetica", 10)
        for e in datos['empleados']:
            c.drawString(xempleados, linea, escribe(e.nombre+' '+e.apellidos))
            linea = sigLinea()

        lineas = lineas[MAXLINEAS:]
        c.drawString(rm, 3, str(i+1)+'/'+str(paginasTotales))
        c.showPage()
    c.save()
    return nomarchivo



def parteRollos(datos, lineas):
    """
    Crea un informe con los datos de
    un parte de la línea de geotextil
    """
    global linea, tm, lm, rm, bm
    x, y = lm, tm  # @UnusedVariable
    global linea
    MAXLINEAS = 40

    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
                              "parteRollos_%s.pdf" % give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo)
    paginasTotales = (len(lineas)/MAXLINEAS+1)
    for i in range(paginasTotales):
        # La cabecera
        texto = 'CONTROL DE PRODUCCIÓN (Línea de geotextil)'
        marcoParte(c, texto)
        linea = height-1.2*inch
        x1 = lm+4
        x2 = width/2 -inch
        x3 = width/2 + 0.7*inch
        x4 = rm - 1.5*inch
        # DONE?: Poner concatenaciones con los datos recibidos
        c.drawString(x1, linea, escribe('FECHA: '+datos['e_fecha']))
        c.drawString(x2, linea, escribe('GRS/M²: '+datos['e_grsm2']))
        c.drawString(x3, linea, escribe('MERMA: '+datos['sp_merma']))
        c.drawString(x4, linea, escribe('PARTIDA: '+datos['e_partida']))
        linea = sigLinea()
        c.drawString(x1, linea, escribe('ARTICULO: '+datos['e_articulo']))
        c.drawString(x2, linea, escribe('ANCHO: '+datos['e_ancho']))
        c.drawString(x3, linea, escribe('LONG. ROLLO: '+datos['e_long_rollo']))
        linea = sigLinea()
        c.drawString(x1, linea, escribe('HORA COM.: '+datos['e_hora_ini']))
        c.drawString(x2, linea, escribe('HORA FIN: '+datos['e_hora_fin']))
        c.drawString(x3, linea, escribe('T.TOTAL: '+datos['e_tiempo_total']))
        c.drawString(x4, linea, escribe('PROD/STAN: '+datos['e_o11']))
        linea = sigLinea() + 4
        c.line(lm, linea, rm, linea)
        # Cuerpo
        linea = sigLinea()
        xnbala = lm + 5
        xpeso = xnbala + 0.75 * inch
        xgrm2 = xpeso + 0.50 * inch
        xmotivo = xgrm2 + 0.50 * inch
        xcomienzo = xmotivo + 1.15 * inch
        xfin = xcomienzo + 0.5 * inch
        xduracion = xfin + 0.5 * inch
        xobservaciones = xduracion + 0.75 * inch
        c.line(lm, linea-3, rm, linea-3)

        c.saveState()
        c.setFont("Times-Roman", 8)
        c.drawString(xnbala, linea + 2, escribe('Nº ROLLO'))
        c.drawString(xpeso, linea + 2, escribe('PESO'))
        c.drawString(xgrm2, linea + 2, escribe('gr/m²'))
        c.drawString(xmotivo, linea + 2, escribe('MOTIVO PARADA'))
        c.drawString(xcomienzo, linea + 2, escribe('H.INICIO'))
        c.drawString(xfin, linea + 2, escribe('H.FIN'))
        c.drawString(xduracion, linea + 2, escribe('DURACION'))
        c.drawString(xobservaciones, linea + 2, escribe('OBSERVACIONES'))
        c.restoreState()
        linea = sigLinea()
        auxLineas = lineas[:MAXLINEAS]
        for l in auxLineas:
            c.drawString(xnbala, linea, escribe(l[0]))
            c.drawString(xpeso, linea, escribe(l[1]))
            c.drawString(xgrm2, linea, escribe(l[2]))
            c.drawString(xmotivo, linea, escribe(l[3]))
            c.drawString(xcomienzo, linea, escribe(l[4]))
            c.drawString(xfin, linea, escribe(l[5]))
            c.drawString(xduracion, linea, escribe(l[6]))
            c.saveState()
            c.setFont("Times-Roman", 8)
            c.drawString(xobservaciones, linea, escribe(l[7]))
            c.restoreState()
            linea = sigLinea(14)

        # Datos Resumen
        x1 = lm + 4
        x2 = lm + 2*inch
        x3 = width/2 + 1.5*inch
        x4 = x3 + 2*inch
        linea = bm + 0.9*inch
        c.drawString(x1, linea, escribe('Nº ROLLOS: '+datos['e_num_rollos']))
        c.drawString(x2, linea,
                     escribe('METROS LINEALES: '+datos['e_metros_lineales']))
        c.drawString(x3, linea, escribe('PESO APROX.: '+datos['e_peso_total']))
        c.line(lm, linea+14, rm, linea+14)
        linea = sigLinea()
        c.drawString(x1, linea,
            escribe('TR TRABAJADO: '+datos['e_tiempo_real_trabajado']))
        c.drawString(x2, linea,
            escribe('PRODUCTIVIDAD: '+datos['e_productividad']))
        c.drawString(x3, linea,
            escribe('CONSUMO EST.: '+datos['e_consumo_estimado']))

        # Pie
        linea = bm + 0.6*inch
        lineaAbajo = bm - 0.5*inch
        xobservaciones = lm + 4
        xempleados = width/2 +4

        rectangulo(c, (lm, linea), (width/2, lineaAbajo), 'OBSERVACIONES: ',
                   alinTxtY = 'arriba')
        rectangulo(c, (width/2, linea), (rm, lineaAbajo), 'OPERARIOS: ',
                   alinTxtY = 'arriba')
        linea = sigLinea() - 10
        agregarFila(xobservaciones, linea, width/2,
                    escribe(datos['observaciones']), c, "Times-Roman", 8)
        for e in datos['empleados']:
            c.drawString(xempleados, linea, escribe(e.nombre+' '+e.apellidos))
            linea = sigLinea()

        lineas = lineas[MAXLINEAS:]
        c.drawString(rm, 3, str(i+1)+'/'+str(paginasTotales))
        c.showPage()

    c.save()
    return nomarchivo

def agregarFila(origen,
                linea,
                limite,
                cadena,
                hoja,
                fuente,
                tamano,
                a_derecha = False,
                altura_linea = 10,
                centrado = False, 
                simular = False, 
                subrayador_fosforito = None):
    """
    Intenta escribir el texto en el espacio comprendido entre
    origen y limite. Si no tiene espacio suficiente la corta
    en las líneas que sean necesarias y devuelve el número
    de líneas que ha avanzado.

    Si a_derecha == True, dibuja el texto alineado a la derecha.
    altura_linea es la altura de la línea (en positivo).

    Si «simular» es True no escribe nada, simplemente devuelve las líneas 
    que se sumarían en caso de hacerlo.

    Si «subrayador_fosforito» es una tupla de tres números entre 0 y 1, 
    subraya las líneas escritas en el color RGB de la tupla.
    """
    #print "fuente", fuente
    #print "tamaño", tamano
    # XXX: Refactorizar. Menudo spaghetti code.
    cadena = cadena.replace("\n", ". ").strip()
    # Había un caso extremo (espacio al final de la cadena) que acababa en
    # bucle infinito.
    try:
        cadena = unicode(cadena)
        # OJO: IMPORTANTE: Verificar que esto (que funciona bien para el
        # ReportLab de la máquina de desarrollo "nostromo") va igual de bien
        # en "melchor", "alfred" y en producción.
    except UnicodeDecodeError:
        pass
        # Efectivamente, con la versión en producción de ReportLab casca.
        # No convierto.
    longitud = hoja.stringWidth(cadena, fuente, tamano)
    longitudLimite = limite - origen
    lineasSumadas = 1
    hoja.saveState()
    hoja.setFont(fuente, tamano)
    # ------------------------------------------------------------------- 
    def make_subrayado(color_rgb, hoja, x, y, cadena, alto):
        #global fuente, tamano
        if color_rgb and cadena:
            ancho = hoja.stringWidth(cadena, fuente, tamano)
            hoja.saveState()
            hoja.setFillColorRGB(*(color_rgb))
            hoja.setStrokeColorRGB(*(color_rgb))
            hoja.rect(x, 
                      y - 4, 
                      ancho, 
                      alto, 
                      stroke = 0, fill = 1)
            hoja.restoreState()
    # ------------------------------------------------------------------- 
    if longitud < longitudLimite:
        if a_derecha:
            try:
                if not simular:
                    make_subrayado(subrayador_fosforito, hoja, limite - 0.1*cm, linea, 
                                   cadena, altura_linea)
                    hoja.drawRightString(limite - 0.1 * cm, linea, cadena)
            except KeyError:
                # Alguna tilde dando por culo y el texto no se ha filtrado
                # por "escribe". Lo intento yo aquí.
                if not simular:
                    make_subrayado(subrayador_fosforito, hoja, limite - 0.1*cm, linea, 
                                   escribe(cadena), altura_linea)
                    hoja.drawRightString(limite - 0.1 * cm, linea, 
                                         escribe(cadena))
        elif centrado:
            izquierda = limite - 0.1 * cm
            derecha = origen
            centro_x = (derecha + izquierda) / 2.0
            try:
                if not simular:
                    make_subrayado(subrayador_fosforito, hoja, 
                                   centro_x - limite/2.0, 
                                   linea, cadena, altura_linea)
                    hoja.drawCentredString(centro_x, linea, cadena)
            except KeyError:
                # Alguna tilde dando por culo y el texto no se ha filtrado
                # por "escribe". Lo intento yo aquí.
                if not simular:
                    make_subrayado(subrayador_fosforito, hoja, centro_x - limite/2.0, 
                                   linea, escribe(cadena), altura_linea)
                    hoja.drawCentredString(centro_x, linea, escribe(cadena))
        else:
            try:
                if not simular:
                    make_subrayado(subrayador_fosforito, hoja, origen, linea, 
                                   cadena, altura_linea)
                    hoja.drawString(origen, linea, cadena)
            except KeyError:
                if not simular:
                    make_subrayado(subrayador_fosforito, hoja, origen, linea, 
                                   escribe(cadena), altura_linea)
                    hoja.drawString(origen, linea, escribe(cadena))
    else:
        cadena1 = cadena
        cadena2 = cadena
        # OJO: Si una palabra es más larga que longitudLimite, no se corta y
        # lo sobrepasará (mejor eso que el bucle infinito en el caía antes).
        while (hoja.stringWidth(cadena2, fuente, tamano) > longitudLimite
               and " " in cadena2):
            #print "cadena1", cadena1, "cadena2", cadena2, "tamano", tamano
            i = 1
            cadena = cadena1 = cadena2
            while (i <= len(cadena)
                   and (hoja.stringWidth(cadena1, fuente, tamano)
                        > longitudLimite or cadena1[-1] != " ")):
                #print "i", i, "cad", cadena, "cad1", cadena1, "cad2", cadena2
                cadena1 = cadena[:-i]
                cadena2 = cadena[-i:]
                i += 1
            if len(cadena1) <= 1:   # He repetido el bucle y no he conseguido
                                    # que entre en el hueco cortando por
                                    # espacios. Reduzco la fuente:
                #print "TATE"
                tamano -= 1
                cadena1 = cadena2 = cadena
                continue
            if a_derecha:
                try:
                    if not simular:
                        make_subrayado(subrayador_fosforito, hoja, limite - 0.1*cm, linea, 
                                       cadena1, altura_linea)
                        hoja.drawRightString(limite - 0.1 * cm, linea, cadena1)
                except KeyError:
                    if not simular:
                        make_subrayado(subrayador_fosforito, hoja, limite - 0.1*cm, linea, 
                                       escribe(cadena1), altura_linea)
                        hoja.drawRightString(limite - 0.1 * cm, linea,
                                         escribe(cadena1))
            elif centrado:
                izquierda = limite - 0.1 * cm
                derecha = origen
                centro_x = (derecha + izquierda) / 2
                try:
                    if not simular:
                        make_subrayado(subrayador_fosforito, hoja, centro_x - limite/2.0, 
                                       cadena, limite, altura_linea)
                        hoja.drawCentredString(centro_x, linea, cadena)
                except KeyError:
                    # Alguna tilde dando por culo y el texto no se ha filtrado
                    # por "escribe". Lo intento yo aquí.
                    if not simular:
                        make_subrayado(subrayador_fosforito, hoja, centro_x - limite/2.0, 
                                       escribe(cadena), limite, altura_linea)
                        hoja.drawCentredString(centro_x, linea, escribe(cadena))
            else:
                try:
                    if not simular:
                        make_subrayado(subrayador_fosforito, hoja, origen, linea, 
                                       cadena1, altura_linea)
                        hoja.drawString(origen, linea, cadena1)
                except KeyError:
                    if not simular:
                        make_subrayado(subrayador_fosforito, hoja, origen, linea, 
                                       escribe(cadena1), altura_linea)
                        hoja.drawString(origen, linea, escribe(cadena1))
            linea -= altura_linea
            lineasSumadas += 1
            cadena1 = cadena2
        cadena = cadena2
        if a_derecha:
            try:
                if not simular:
                    make_subrayado(subrayador_fosforito, hoja, limite - 0.1*cm, linea, 
                                   cadena, altura_linea)
                    hoja.drawRightString(limite - 0.1 * cm, linea, cadena)
            except KeyError:
                if not simular:
                    make_subrayado(subrayador_fosforito, hoja, limite - 0.1*cm, linea, 
                                   cadena, altura_linea)
                    hoja.drawRightString(limite - 0.1 * cm, linea, cadena)
        elif centrado:
            izquierda = limite - 0.1 * cm
            derecha = origen
            centro_x = (derecha + izquierda) / 2
            try:
                if not simular:
                    make_subrayado(subrayador_fosforito, hoja, centro_x - limite/2.0, 
                                   linea, cadena, altura_linea)
                    hoja.drawCentredString(centro_x, linea, cadena)
            except KeyError:
                # Alguna tilde dando por culo y el texto no se ha filtrado
                # por "escribe". Lo intento yo aquí.
                if not simular:
                    make_subrayado(subrayador_fosforito, hoja, centro_x - limite/2.0, 
                                   linea, escribe(cadena), altura_linea)
                    hoja.drawCentredString(centro_x, linea, escribe(cadena))
        else:
            try:
                if not simular:
                    make_subrayado(subrayador_fosforito, hoja, origen, linea, 
                                   cadena, altura_linea)
                    hoja.drawString(origen, linea, cadena)
            except KeyError:
                if not simular:
                    make_subrayado(subrayador_fosforito, hoja, origen, linea, 
                                   cadena, altura_linea)
                    hoja.drawString(origen, linea, cadena)
    hoja.restoreState()
    return lineasSumadas

def exportar_a_csv(ruta, cabecera, datos):
    import treeview2csv
    from formularios.reports import abrir_csv
    datos_iso = []
    for fila in datos:
        fila_iso = []
        for item in fila:
            if isinstance(item, bool):
                item = item and u"Sí".encode("iso-8859-15") or "No"
            else:
                item = ("%s" % item).replace(";", ",")
                try:
                    item.encode("iso-8859-15")
                    item = item.replace("€", chr(164))
                        # Lo hago a manopla porque no sé por que el encoding
                        # no se cepilla el euro y lo cambia por el chr(164).
                except Exception, msg:
                    print msg
            fila_iso.append(item)
        datos_iso.append(fila_iso)
    cabecera_iso = []
    for item in cabecera:
        try:
            item = item[0].encode("iso-8859-15")
        except:
            pass
        cabecera_iso.append(item)
    treeview2csv.generar_csv(ruta, cabecera_iso, datos_iso)
    abrir_csv(ruta)

def parse_fuente(cad, hoja):
    """
    Si la cadena contiene algo de la forma [fuente=%s] intenta reconocer  
    la fuente y devuelve la misma cadena sin la subcadena 
    reconocida.
    La subcadena debe ser de la forma "nombre fuente::tamaño"
    Fuentes reconocidas (al menos):
    ['Courier',
     'Courier-Bold',
     'Courier-BoldOblique',
     'Courier-Oblique',
     'Helvetica',
     'Helvetica-Bold',
     'Helvetica-BoldOblique',
     'Helvetica-Oblique',
     'Symbol',
     'Times-Bold',
     'Times-BoldItalic',
     'Times-Italic',
     'Times-Roman',
     'ZapfDingbats']
    Devuelve None donde no pueda reconocer fuente o tamaño.
    """
    try:
        fuente_tamanno = re.compile("\[fuente=\w+\-?\w*::\d+\]").findall(cad)[0]
    except IndexError:
        fuente = tamanno = None
    else:
        cad = cad.replace(fuente_tamanno, "")
        fuente_tamanno = fuente_tamanno[1:-1]   # Quito corchetes.
        fuente_tamanno = fuente_tamanno.replace("fuente=", "")
        fuente, tamanno = fuente_tamanno.split("::")
        tamanno = int(tamanno)  # Lanzará ValueError si no es un entero.
        if fuente not in hoja.getAvailableFonts():
            raise ValueError, "geninformes::parse_fuente: La fuente debe es"\
                              "tar en %s." % hoja.getAvailableFonts()
    #print cad, fuente, tamanno, type(tamanno)
    return cad, fuente, tamanno

def imprimir2(archivo,
              titulo,
              campos,
              datos,
              fecha = None,
              cols_a_derecha = (),
              graficos = [],
              apaisado = False,
              sobrecampos = (),
              lineas_verticales = (),
              exportar_a_csv_a = None,
              cols_centradas = (), 
              pijama = False):
    """
    Veamos, veamos. La idea es tener este método y pasarle chorrecientos
    parámetros de modo que luego el método se encargue de ordenar las cosas.
    Hay varios problemas inciales:
    - Cada informe imprime unos datos que no tienen porqué tener nada que ver
      con el formulario o el objeto en pantalla. Incluso pueden imprimirse
      desde el menú principal, es decir, sin ningún objeto en memoria.
    - Cada informe imprime unos campos, cada campo tiene un tamaño máximo y
      han de ajustarse de modo que quepan todos al mismo tiempo que la cosa
      quede elegante.

    Parámetros a pasar:
    - Nombre del archivo de salida *.pdf
    - Título (cabecera) del informe
    - Lista de campos (los títulos) y el ancho máximo de cada uno de modo que
      una funcioncilla calcule el ancho de cada uno en el papel. Hay que tener
      en cuenta que la longitud horizontal de impresión es de rm-lm pixeles.
      Esto no es tan fácil además que las fuentes no son Monospace, ummm.
      Bueno, hay otra salida: Considerar los porcentajes que debe ocupar cada
      campo y así dividirlo y ubicarlo sobre la marcha. Así que finalmente el
      parámetro campos es una lista de tuplas de la forma ('Campo',
      porcentaje). El porcentaje es lo que ocupa ese campo. Lo primero será
      comprobar que la suma de los porcentajes no es mayor que 100.
    - Lista de datos: Es sencillo. Una lista con todas las filas del informe.
      Cada fila es una tupla cuya longitud (y orden) debe ser igual al número
      de campos.

    cols_a_derecha es una lista de los índices de las columnas
    (empezando por 0) que deben ser alineadas a la derecha.

    graficos es una lista de NOMBRES DE ARCHIVO que contienen imágenes que
    serán colocadas una tras otra al final del informe.

    Seguimos complicando el tema. "sobrecampos" es una lista de
    (('palabra1', x1%), ('palabra2', x2%), ...) que se colocarán en la
    cabecera de los campos, un poco más arriba de los títulos, centradas en
    las posiciones "x" indicadas (tanto porciento respecto al ancho de la
    página).

    ¡No se vayan todavía, aún hay más! Si algún campo contiene la cadena de
    texto "---" se dibujará una línea en el ancho de ese campo. Si es "==="
    dibujará una línea doble.

    Seguimos aumentando la lista interminable de parámetros:
    "lineas_verticales" es una lista de posiciones (siempre en tantos por
    ciento) donde se dibujarán líneas verticales que irán desde el borde
    superior de la cabecera hasta el borde inferior del cuadro del cuerpo si
    el segundo elemento de cada sublista es False o desde el borde superior de
    la cabecera hasta el borde inferior de la página si es True:
    P.ej: ((20, False), (50, True)) produce:
    -----------------
    |        |      |
    -----------------
    |   |    |      |
    |   |    |      |
    -----------------

    Ahora acepta colores en el texto. Hay que pasarlos en cualquier posición
    del texto a colorear de la siguiente forma:
        (ejemplo) "Uno de los valores[color=rojo]"  -> Escribirá "Uno de los
        valores" en rojo.
        De momento acepta:
            [color=rojo]
            [color=azul]
            [color=verde]
            [color=gris]

    "Mais" cositas: Si un campo contiene la cadena ">->", se extenderá el
    límite del campo anterior al límite de ese campo de forma que el texto
    del campo anterior ocupará el espacio de su campo y el del que contiene
    ">->".

    Otro parámetro one more time: exportar_a_csv_a. Si es None no hace nada.
    Si es una cadena de texto volcará una versión en formato CSV del informe
    generado (es decir, cabecera + datos, básicamente). El archivo resultante
    se abre directamente con el programa relacionado, NO SE DEVUELVE, SE RECIBE
    EL NOMBRE DEL FICHERO DESTINO.

    «pijama» es un parámetro de última hornada que sirve para irte a la cama a 
    soñar con la teniente Ellen Ripley. También vale para que las líneas se 
    dibujen con color de fondo alternativo al estilo de los viejos rollos de 
    papel contínuo en verde-blanco.
    """
    if exportar_a_csv_a:
        exportar_a_csv(exportar_a_csv_a, campos, datos)
    from reportlab.lib import colors

    if len(datos) == 0:
        return

    global linea, tm, lm, rm, tm, MAXLINEAS, bm

    if archivo.lower().endswith(".pdf"):
        archivo = archivo[:-4]
    if apaisado:
        rm, tm, width, height, MAXLINEAS = apaisar()
        hoja = canvas.Canvas("%s.pdf" % (archivo), pagesize = landscape(A4))
    else:
        rm, tm, width, height, MAXLINEAS = apaisar(False)
        hoja = canvas.Canvas(archivo + ".pdf", pagesize = A4)

    hoja.setTitle(titulo)

    x, y = lm, tm + inch  # @UnusedVariable

    texto = hoja.beginText()
    # Ponemos la cabecera
    cabecera(hoja, titulo, fecha, apaisado = apaisado)
    linea = tm + 0.8*inch
    # El cuerpo
    fuente = "Helvetica-Bold"
    tamanno = 9
    hoja.setFont(fuente, tamanno)
    suma = sum([i[1] for i in campos])
    if suma > 100:
        #print 'ERROR: Los campos ocupan más de lo que permite la hoja'
        #return
        # En lugar de abortar, recorto campos hasta llegar al 100.
        campos = [list(c) for c in campos]
        c = len(campos)
        while sum([i[1] for i in campos]) > 100:
            c -= 1
            campos[c][1] -= 1
            if c <= 0:
                # Vuelvo a empezar
                c = len(campos)
    if len(datos[0]) != len(campos):
        print 'ERROR: Los datos no concuerdan con los campos del informe'
        return
    # xcampo guarda la coordenada x donde irá cada campo
    xcampo = [lm]
    anchoHoja = rm - lm
    for i in campos:
        xcampo.append( (i[1]*anchoHoja/100) + xcampo[len(xcampo)-1] )
    xcampo = xcampo[:-1]
    yCabecera = tm + inch
    for sobrecampo, posicion in sobrecampos:
        posicion_sobrecampo = (lm - 4) + (1.0 * posicion * anchoHoja / 100)
        hoja.drawCentredString(posicion_sobrecampo, yCabecera + 0.3 * cm,
                               escribe(sobrecampo))
    hoja.saveState()
    for linea_vertical, hasta_arriba in lineas_verticales:
        # El porqué de toda esta incoherencia entre anchos, márgenes y ajustes
        # manuales chapuceros es que la ignorancia es muy atrevida.
        # Hay que hacerle una limpieza de código total a esto. Me metí a
        # toquetear sin conocer bien el ReportLab y... en fin.
        ancho = anchoHoja
        arriba = height - inch
        abajo = bm - 0.2 * inch
        medio = yCabecera - 2
        # Para que no pise a las columnas alineadas a la dcha.:
        posicion_linea_vertical = ((lm - 4)
                                    + (1.0 * linea_vertical * ancho / 100) + 2)
        if hasta_arriba:
            hoja.setLineWidth(0.4)
            hoja.setDash()
            hoja.line(posicion_linea_vertical, arriba,
                      posicion_linea_vertical, medio)
        hoja.setLineWidth(0.2)
        hoja.setDash(1, 4)  # 1 punto negro, 4 blancos
        hoja.line(posicion_linea_vertical, medio, posicion_linea_vertical,
                  abajo)
    hoja.restoreState()
    for i in range(len(campos)):
        try:
            #hoja.drawCentredString((xcampo[i]+xcampo[i+1])/2, yCabecera,
            #                       escribe(campos[i][0]))
            el_encogedor_de_fuentes_de_doraemon(hoja, fuente, tamanno,
                xcampo[i], xcampo[i+1], yCabecera, campos[i][0], alineacion=0)
        except IndexError:
            #hoja.drawCentredString((xcampo[i]+rm)/2, yCabecera,
            #                       escribe(campos[i][0]))
            el_encogedor_de_fuentes_de_doraemon(hoja, fuente, tamanno,
                xcampo[i], rm, yCabecera, campos[i][0], alineacion = 0)
    hoja.line(lm - 4, yCabecera-2, rm, yCabecera-2)
    linea = yCabecera
    fuente = old_fuente = "Helvetica"
    tamanno = old_tamanno = 6
    hoja.setFont(fuente, tamanno)
    # 41 es el número máximo de líneas en el área de impresión
    paginas = int(len(datos) / MAXLINEAS) +1
    x = lm  # @UnusedVariable
    y = linea  # @UnusedVariable
    # contLinea se va incrementando con cada elemento y llegado al tope de
    # líneas provoca la creación de una nueva página.
    contLinea = 0
    actualPagina = 1
    lineasASaltar = []
    linea = sigLinea()
    for dato in datos:
        # LE PIYAMA
        # Hay que hacerlo ANTES de escribir porque no hay manera de ordenar 
        # capas en el canvas. ¿Problema? Que no sé el alto de la fila hasta 
        # que no termine de escribir todas las columnas.
        if pijama:
            xizq = lm - 4   #OJO: HARCODED. Ver def cabecera.
            xder = rm
            draw_fondo_pijama(hoja, 
                              xizq, linea, 
                              xder,  
                              datos.index(dato), 
                              dato, xcampo, fuente, tamanno, 
                              cols_a_derecha, cols_centradas)
        # EOLP

        d = list(dato)
        lineasASaltar = []
        for i in range(len(d)):
            try:
                xizq, xder = xcampo[i], xcampo[i+1]
            except IndexError:
                xizq, xder = xcampo[i], rm
            ## "Parser" de códigos especiales: ################
            # Extensión de límite derecho (">->")
            j = i+1
            while j < len(d) and d[j] == ">->":
                try:
                    xder = xcampo[j+1]
                except IndexError:
                    xder = rm
                j += 1
            if d[i] == "---":
                hoja.saveState()
                hoja.setLineWidth(0.5)
                lineasSumadas = 1
                hoja.line(xizq, linea, xder, linea)
                hoja.restoreState()
            elif d[i] == "===":
                hoja.saveState()
                hoja.setLineWidth(0.5)
                lineasSumadas = 1
                hoja.line(xizq, linea+1, xder, linea+1)
                hoja.line(xizq, linea-1, xder, linea-1)
                hoja.restoreState()
            elif d[i] == ">->":
                pass    # No escribo nada en el PDF. El espacio ya ha sido
                        # ocupado por la columna anterior cuyo dato != >->
            else:
                # Colores   (de momento es un poco cutre, pero no voy a
                #            escribir un compilador ni me voy a inventar un
                #            lenguaje de marcado sólo para poder poner un par
                #            de colores cómodamente).
                hoja.setFillColor(colors.black)
                try:
                    keycad_rgb = "[color=RGB{"
                    endkeycad_rgb = "}]"
                    if "[color=rojo]" in d[i]:
                        d[i] = d[i].replace("[color=rojo]", "")
                        hoja.setFillColor(colors.red)
                    elif "[color=verde]" in d[i]:
                        d[i] = d[i].replace("[color=verde]", "")
                        hoja.setFillColor(colors.green)
                    elif "[color=azul]" in d[i]:
                        d[i] = d[i].replace("[color=azul]", "")
                        hoja.setFillColor(colors.blue)
                    elif "[color=gris]" in d[i]:
                        d[i] = d[i].replace("[color=gris]", "")
                        hoja.setFillColor(colors.gray)
                    elif keycad_rgb in d[i]:
                        desde = d[i].index(keycad_rgb) + len(keycad_rgb)
                        hasta = d[i].index(endkeycad_rgb) 
                        strcolor = d[i][desde:hasta]
                        d[i] = d[i][:desde] + d[i][hasta:]
                        d[i] = d[i].replace(keycad_rgb, "")
                        d[i] = d[i].replace(endkeycad_rgb, "")
                        r, g, b = map(float, strcolor.split(","))
                        hoja.setFillColorRGB(r, g, b)
                    # XXX: Cambio de fuente. 
                    old_fuente = fuente
                    old_tamanno = tamanno
                    d[i], fuente, tamanno = parse_fuente(d[i], hoja)
                    if fuente == None:
                        fuente = old_fuente
                    if tamanno == None:
                        tamanno = old_tamanno
                except TypeError, msg:      # Se nos ha colado un entero, @UnusedVariable
                                            # probablemente.
                    # print msg, type(d[i]), d[i]
                    pass
            ## EOP ############################################
                lineasSumadas = agregarFila(xizq,
                                            linea,
                                            xder,
                                            escribe(d[i]),
                                            hoja,
                                            fuente,
                                            tamanno,
                                            a_derecha = i in cols_a_derecha,
                                            centrado = i in cols_centradas)
            lineasASaltar.append(lineasSumadas)
            # Restauro fuente y tamaño:
            fuente = old_fuente
            tamanno = old_tamanno
            # Si he cambiado de color, vuelvo al negro.
            hoja.setFillColor(colors.black) 

        contLinea += max(lineasASaltar)
        if contLinea >= MAXLINEAS:
            pie(hoja, actualPagina, paginas, apaisado = apaisado)
            hoja.showPage()
            contLinea = 0
            actualPagina += 1
            cabecera(hoja, titulo, fecha, apaisado = apaisado)
            linea = yCabecera
            # El cuerpo
            x, y = lm, tm  # @UnusedVariable
            yCabecera = tm + inch
            hoja.setFont("Helvetica-Bold", 9)
            #hoja.setFont("Helvetica-Bold", 10)
            for sobrecampo, posicion in sobrecampos:
                posicion_sobrecampo = ((lm - 4)
                                        + (1.0 * posicion * anchoHoja / 100))
                hoja.drawCentredString(posicion_sobrecampo,
                                       yCabecera + 0.3 * cm,
                                       escribe(sobrecampo))
            hoja.saveState()
            for linea_vertical, hasta_arriba in lineas_verticales:
                ancho = anchoHoja
                arriba = height - inch
                abajo = bm - 0.2 * inch
                medio = yCabecera - 2
                posicion_linea_vertical = ((lm - 4)
                    + (1.0 * linea_vertical * ancho / 100) + 2)   # Para que
                                # no pise a las columnas alineadas a la dcha.
                if hasta_arriba:
                    hoja.setLineWidth(0.4)
                    hoja.setDash()
                    hoja.line(posicion_linea_vertical, arriba,
                              posicion_linea_vertical, medio)
                hoja.setLineWidth(0.2)
                hoja.setDash(1, 4)  # 1 punto negro, 4 blancos
                hoja.line(posicion_linea_vertical, medio,
                          posicion_linea_vertical, abajo)
            hoja.restoreState()
            for i in range(len(campos)):
                try:
                    #hoja.drawCentredString((xcampo[i]+xcampo[i+1])/2,
                    #                       yCabecera, escribe(campos[i][0]))
                    el_encogedor_de_fuentes_de_doraemon(hoja, fuente, tamanno,
                        xcampo[i], xcampo[i+1], yCabecera, campos[i][0],
                        alineacion = 0)
                except IndexError:
                    #hoja.drawCentredString((xcampo[i]+rm)/2, yCabecera,
                    #                       escribe(campos[i][0]))
                    el_encogedor_de_fuentes_de_doraemon(hoja, fuente, tamanno,
                        xcampo[i], rm, yCabecera, campos[i][0], alineacion = 0)
            hoja.line(lm, yCabecera-2, rm, yCabecera-2)
            hoja.setFont(fuente, tamanno)
            x = lm  # @UnusedVariable
            linea = sigLinea()
        else:
            for i in range(max(lineasASaltar)):
                linea = sigLinea()
            x = lm  # @UnusedVariable
    hoja.drawText(texto)
    # AQUÍ LOS GRÁFICOS.
    for imagen in graficos:
        ancho, alto = get_ancho_alto(imagen, limiteh = rm - lm)
    # TODO: Comprobar que no se sale de los márgenes ni de la página, que se
    # pasa de página si no cabe, que se incrementa el número de páginas, etc...
        linea = linea - alto
        hoja.drawImage(imagen, lm, linea - 1 * cm)
    # Ponemos el pie
    pie(hoja, actualPagina, paginas, apaisado = apaisado)
    # Salvamos la página
    hoja.showPage()
    # Salvamos el documento
    hoja.save()
    # Antes de salir voy a dejar las globales como estaban (vaya horror,
    # coños, andar a estas alturas peleándome con globales, grrrr):
    rm, tm, width, height, MAXLINEAS = apaisar(False)
    return archivo+'.pdf'

def draw_fondo_pijama(c, x0, y0, x1, contador, 
                      datos_col, xcoords, fuente, tamanno, 
                      cols_a_derecha, cols_centradas, 
                      rgbcolor = (0.8, 0.9, 0.7)):
    """
    Dibuja un rectángulo del color recibido entre las coordenadas (x0, y0) y 
    (x1, y0 + #líneas de texto * altura) siempre que el contador sea impar.
    La coordenada "y" final puede no coincidir con la recibida si para 
    mostrar los textos de «datos_col» se necesita más de una línea.
    """
    if contador % 2:
        # Miro la altura final con la ayuda de 
        # el_encogedor_de_fuentes_de_doraemon
        d = list(datos_col)
        xcampo = xcoords
        lineasASaltar = []
        for i in range(len(d)):
            try:
                xizq, xder = xcampo[i], xcampo[i+1]
            except IndexError:
                xizq, xder = xcampo[i], rm
            ## "Parser" de códigos especiales: ################
            # Extensión de límite derecho (">->")
            j = i+1
            while j < len(d) and d[j] == ">->":
                try:
                    xder = xcampo[j+1]
                except IndexError:
                    xder = rm
                j += 1
            lineasSumadas = agregarFila(xizq,
                                        y0,
                                        xder,
                                        escribe(d[i]),
                                        c,
                                        fuente,
                                        tamanno,
                                        a_derecha = i in cols_a_derecha,
                                        centrado = i in cols_centradas, 
                                        simular = True)
            lineasASaltar.append(lineasSumadas)
        lineas = (max(lineasASaltar))
        altura_linea = 10   # OJO: HARCODED a valor por defecto de agregarFila
        h = lineas * altura_linea
        for i in range(lineas-1):
            y0 = sigLinea(valor = altura_linea, actual = y0)
        # Dibujo el fondo en sí.
        r, g, b = rgbcolor
        c.saveState()
        c.setFillColorRGB(r, g, b)
        c.setStrokeColorRGB(r, g, b)
        c.setLineWidth(1)
        c.rect(x0+1, y0 - 7, 
               abs(x1-x0-2), h + 5, 
               fill = 1)
        c.restoreState()

def get_ancho_alto(imagen, limitev = None, limiteh = None):
    """
    Devuelve el ancho y el alto de la imagen
    correspondiente al nombre de fichero recibido.
    ¡Necesita PIL!
    Si limiteh es distinto de None, se redimensiona la
    imagen en caso de que supere el límite horizontal.
    Lo mismo con limitev.
    """
    try:
        import Image
    except ImportError:
        print "geninformes.py (get_ancho_alto): Necesita instalar PIL"
        return (0, 0)
    try:
        i = Image.open(imagen)
    except IOError:
        print "geninformes.py (get_ancho_alto): Imagen %s no encontrada." % (
            imagen)
        return (0, 0)
    ancho, alto = i.size
    ratio = float(alto) / ancho
    if limiteh:
        ancho = int(limiteh)
        alto = int(ancho * ratio)
    if limitev:
        if alto > limitev:
            alto = int(limitev)
            ancho = int((1 / ratio) * alto)
    i = i.resize((ancho, alto), Image.BICUBIC)
    i.save(imagen)
    return i.size

def etiquetasRollos(rollos, mostrar_marcado):
    """
    Crea etiquetas para los rollos de
    un parte de la línea de geotextil.
    4 por folio (A4).
    """
    global linea, tm, lm, rm, bm
    x, y = lm, tm  # @UnusedVariable
    global linea
    MAXLINEAS = 40

    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
                              "etiqRollos_%s.pdf" % give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo)

    c.setPageRotation(90)

    # arribaArriba significa linea de "arriba" de los cuadros de "Arriba"
    # El 0 vertical es el borde de abajo
    # El 0 horizontal es el margen derecho
    arribaArriba = height - 15
    abajoArriba = height/2 + 15
    arribaAbajo = height/2 - 15
    abajoAbajo = 15

    izqIzq = width - 20
    izqDer = width/2 - 20
    derIzq = width/2 + 20
    derDer = 20

    xCE1 = height/4
    xCE = (xCE1, height-xCE1, xCE1, height-xCE1)

    yCE1 = inch
    yCE = (yCE1, yCE1, width/2 + yCE1, width/2 + yCE1)

    xCodigoCE1 = xCE1
    xCodigoCE = (xCodigoCE1, height-xCodigoCE1, xCE1, height-xCE1)

    yCodigoCE1 = yCE1 + 0.4*inch
    yCodigoCE = (yCodigoCE1, yCodigoCE1, width/2 + yCodigoCE1,
                 width/2 + yCodigoCE1)

    xDescripcion1 = xCE1
    xDescripcion = (xDescripcion1, height-xDescripcion1, xDescripcion1,
                    height-xDescripcion1)

    yDescripcion1 = yCodigoCE1 + 0.4*inch
    yDescripcion = (yDescripcion1, yDescripcion1, width/2 + yDescripcion1,
                    width/2 + yDescripcion1)

    xDensidad1 = xCE1
    xDensidad = (xDensidad1, height-xDensidad1, xDensidad1, height-xDensidad1)

    yDensidad1 = yDescripcion1 + 0.4*inch
    yDensidad = (yDensidad1, yDensidad1, width/2 + yDensidad1,
                 width/2 + yDensidad1)

    xIzquierda1 = 20
    xIzquierda = (xIzquierda1, height/2 +xIzquierda1, xIzquierda1,
                  height/2+xIzquierda1)

    xDerecha1 = height/3 -100
    xDerecha = (xDerecha1, height/2 + xDerecha1, xDerecha1,
                height/2 + xDerecha1)

    yPrimeraLinea1 = yDensidad1 +0.4*inch
    yPrimeraLinea = (yPrimeraLinea1, yPrimeraLinea1, width/2 + yPrimeraLinea1,
                     width/2 + yPrimeraLinea1)

    ySegundaLinea1 = yPrimeraLinea1 + 0.3*inch
    ySegundaLinea = (ySegundaLinea1, ySegundaLinea1, width/2 + ySegundaLinea1,
                     width/2 + ySegundaLinea1)

    yTerceraLinea1 = ySegundaLinea1 + 0.3*inch
    yTerceraLinea = (yTerceraLinea1, yTerceraLinea1, width/2 + yTerceraLinea1,
                     width/2 + yTerceraLinea1)

    yCuartaLinea1 = yTerceraLinea1 + 0.5*inch
    yCuartaLinea = (yCuartaLinea1, yCuartaLinea1, width/2 + yCuartaLinea1,
                    width/2 + yCuartaLinea1)

    for j in range(len(rollos)/4+1):  # @UnusedVariable
        temp = rollos[:4]
        if temp == []:
            break

        rectangulo(c, (izqIzq, arribaArriba), (derIzq, abajoArriba))
        rectangulo(c, (izqDer, arribaArriba), (derDer, abajoArriba))
        rectangulo(c, (izqIzq, arribaAbajo), (derIzq, abajoAbajo))
        rectangulo(c, (izqDer, arribaAbajo), (derDer, abajoAbajo))

        c.rotate(90)

        for i in range(len(temp)):
            if mostrar_marcado:
                c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', 'CE.png'),
                            xCE[i] - (3 * cm / 2), -yCE[i], width = 2 * cm,
                            height = 1.64 * cm)
                c.setFont("Helvetica", 20)
                c.drawCentredString(xCodigoCE[i], -yCodigoCE[i],
                                    "1035-CPD-ES033858")
            c.setFont("Helvetica-Bold", 26)
            c.drawCentredString(xDescripcion[i], -yDescripcion[i],
                                escribe(temp[i]['descripcion']))
            c.setFont("Helvetica", 20)
            c.drawCentredString(xDensidad[i], -yDensidad[i],
                                escribe(temp[i]['densidad']+" gr/m²"))
            c.setFont("Helvetica", 14)
            c.drawString(xIzquierda[i], -yPrimeraLinea[i],
                         escribe("Ancho: "+temp[i]['ancho']))
            c.drawString(xDerecha[i], -yPrimeraLinea[i],
                         escribe("M²: "+temp[i]['m2']))
            c.drawString(xIzquierda[i], -ySegundaLinea[i],
                         escribe("Peso: "+temp[i]['peso']))
            c.drawString(xDerecha[i], -ySegundaLinea[i],
                         escribe("M.lin: "+temp[i]['mlin']))
            c.drawString(xIzquierda[i], -yTerceraLinea[i],
                         escribe("Partida: "+temp[i]['partida']))

            c.setFont("Helvetica-Bold", 28)
            c.drawString(xIzquierda[i], -yCuartaLinea[i],
                         escribe("Nº rollo: "+temp[i]['nrollo']))
            from barcode.EANBarCode import EanBarCode
            bar = EanBarCode()
            c.drawImage(bar.getImage(temp[i]['codigo']), xDerecha[i]+115,
                        -ySegundaLinea[i])
            from barcode import code39
            codigobarras = code39.Extended39(temp[i]['codigo39'],
                                             xdim = .015*inch)
            codigobarras.drawOn(c, xDerecha[i]+inch, -yCuartaLinea[i]+10)
            c.setFont("Helvetica", 8)
            c.drawString(xDerecha[i]+2*inch, -yCuartaLinea[i],
                         escribe(temp[i]['codigo39']))

        c.rotate(-90)

        rollos = rollos[4:]

        c.showPage()

    c.save()
    return nomarchivo

def etiquetasBalas(balas):
    """
    Crea etiquetas para las balas de
    un parte de la línea de fibra.
    4 por folio (A4)
    """
    global linea, tm, lm, rm, bm
    x, y = lm, tm  # @UnusedVariable
    global linea
    MAXLINEAS = 40

    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
                              "etiqBalas_%s.pdf" % give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo)

    c.setPageRotation(90)

    # arribaArriba significa linea de "arriba" de los cuadros de "Arriba"
    # El 0 vertical es el borde de abajo
    # El 0 horizontal es el margen derecho
    arribaArriba = height - 15
    abajoArriba = height/2 + 15
    arribaAbajo = height/2 - 15
    abajoAbajo = 15

    izqIzq = width - 20
    izqDer = width/2 - 20
    derIzq = width/2 + 20
    derDer = 20

    xLogo1 = height /4 + 0.5*inch
    xLogo = (xLogo1, height/2 + xLogo1, xLogo1, height/2 + xLogo1)

    yLogo1 = inch
    yLogo = (yLogo1, yLogo1, width/2 + yLogo1, width/2 + yLogo1)

    xIzquierda1 = 20
    xIzquierda = (xIzquierda1, height/2 +xIzquierda1, xIzquierda1,
                  height/2+xIzquierda1)

    xDerecha1 = height/3 -50
    xDerecha = (xDerecha1, height/2 +xDerecha1, xDerecha1,
                height/2 + xDerecha1)

    yPrimeraLinea1 = yLogo1 +0.7*inch
    yPrimeraLinea = (yPrimeraLinea1, yPrimeraLinea1, width/2 + yPrimeraLinea1,
                     width/2 + yPrimeraLinea1)

    ySegundaLinea1 = yPrimeraLinea1 + 0.5*inch
    ySegundaLinea = (ySegundaLinea1, ySegundaLinea1, width/2 + ySegundaLinea1,
                     width/2 + ySegundaLinea1)

    yTerceraLinea1 = ySegundaLinea1 + 0.5*inch
    yTerceraLinea = (yTerceraLinea1, yTerceraLinea1, width/2 + yTerceraLinea1,
                     width/2 + yTerceraLinea1)

    yCuartaLinea1 = yTerceraLinea1 + 0.5*inch
    yCuartaLinea = (yCuartaLinea1, yCuartaLinea1, width/2 + yCuartaLinea1,
                    width/2 + yCuartaLinea1)

    yQuintaLinea1 = yCuartaLinea1 + 0.5*inch
    yQuintaLinea = (yQuintaLinea1, yQuintaLinea1, width/2 + yQuintaLinea1,
                    width/2 + yQuintaLinea1)

    xCodigo1 = xDerecha1 + 0.9*inch
    xCodigo = (xCodigo1, height/2 + xCodigo1, xCodigo1, height/2 + xCodigo1)

    yCodigo1 = 1.1+inch
    yCodigo = (yCodigo1, yCodigo1, width/2 + yCodigo1, width/2 + yCodigo1)

    for j in range(len(balas)/4+1):  # @UnusedVariable
        temp = balas[:4]
        if temp == []:
            break

        rectangulo(c, (izqIzq, arribaArriba), (derIzq, abajoArriba))
        rectangulo(c, (izqDer, arribaArriba), (derDer, abajoArriba))
        rectangulo(c, (izqIzq, arribaAbajo), (derIzq, abajoAbajo))
        rectangulo(c, (izqDer, arribaAbajo), (derDer, abajoAbajo))

        c.rotate(90)

        for i in range(len(temp)):
            c.setFont("Helvetica-Bold", 26)
            c.drawRightString(xLogo[i], -yLogo[i], "GEOTEXAN S.A.")
            c.setFont("Helvetica", 14)
            c.drawString(xIzquierda[i], -yPrimeraLinea[i],
                         escribe("CODIGO: "+temp[i]['codigo']))

            from barcode import code39
            codigobarras = code39.Extended39(temp[i]['codigo'],
                                             xdim = .015*inch)
            codigobarras.drawOn(c, xIzquierda[i]+20, -yPrimeraLinea[i]+15)

            c.drawString(xDerecha[i], -yPrimeraLinea[i],
                         escribe("COLOR: "+temp[i]['color']))
            c.drawString(xIzquierda[i], -ySegundaLinea[i],
                         escribe("LOTE: "+temp[i]['lote']))
            c.drawString(xDerecha[i], -ySegundaLinea[i],
                         escribe("PESO KG: "+temp[i]['peso']))
            c.drawString(xIzquierda[i], -yTerceraLinea[i],
                         escribe("TIPO: "+temp[i]['tipo']))
            c.drawString(xDerecha[i], -yTerceraLinea[i],
                         escribe("LONGITUD: "+temp[i]['longitud']))
            c.drawString(xIzquierda[i], -yCuartaLinea[i],
                         escribe("BALA Nº: "+temp[i]['nbala']))
            c.drawString(xDerecha[i], -yCuartaLinea[i],
                         escribe("DTEX: "+temp[i]['dtex']))
            c.drawString(xDerecha[i], -yQuintaLinea[i],
                         escribe("ACABADO: "+temp[i]['acabado']))

            from barcode.EANBarCode import EanBarCode
            bar = EanBarCode()
            c.drawImage(bar.getImage(temp[i]['codigoBarra']), xCodigo[i],
                        -yCodigo[i])


        c.rotate(-90)

        balas = balas[4:]

        c.showPage()

    c.save()
    return nomarchivo

def etiquetasBigbags(bigbags):
    """
    Crea etiquetas en cuartillas (A5) para los
    bigbags recibidos.
    """
    datos_empresa = pclases.DatosDeLaEmpresa.select()[0]

    from reportlab.lib.pagesizes import A5
    from barcode import code39
    from barcode.EANBarCode import EanBarCode

    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
                              "etiqBigbags_%s.pdf" % give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo, pagesize = landscape(A5))
    # El 0 vertical es el borde de abajo
    # El 0 horizontal es el margen derecho
    height, width = A5

    derecha = width - 1 * cm
    izquierda = 1 * cm
    arriba = height - 1 * cm
    abajo = 1 * cm
    xgeotexan, ygeotexan = (height / 2, 1.7 * cm)
    xproducto, yproducto = (width * 5 / 9.0, arriba - 2.5 * cm)
    xnumbb, ynumbb = (izquierda + 5 * cm, arriba - 4.35 * cm)
    xpeso, ypeso = (izquierda + 5 * cm, arriba - 5.70 * cm)
    xcorte, ycorte = (izquierda + 5 * cm, arriba - 7.05 * cm)
    xlote, ylote = (izquierda + 5 * cm , arriba - 8.40 * cm)
    xean, yean = (derecha - 2.5 * cm, abajo + 1 * cm)
    x39, y39 = (izquierda , abajo + 1 * cm)
    xbbcode, ybbcode = (izquierda + 5 * cm, abajo + 0.5 * cm)
    ximage, yimage = (izquierda + 0.5 * cm, arriba - 3.2 * cm)

    for bigbag in bigbags:
        rectangulo(c, (izquierda, arriba), (derecha, abajo), doble = True)

        c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', datos_empresa.logo),
                    ximage, yimage, 3 * cm, 3 * cm)
        c.setFont("Times-Roman", 20)
        c.rotate(90)
        c.drawCentredString(xgeotexan, -ygeotexan, datos_empresa.nombre)
        c.rotate(-90)
        c.setFont("Helvetica-Bold", 42)
        c.drawCentredString(xproducto, yproducto,
                            escribe(bigbag.articulo.productoVenta.descripcion))
        c.setFont("Helvetica", 28)
        c.drawString(xcorte, ycorte,
            escribe("CORTE: %d mm" % (
                bigbag.articulo.productoVenta.camposEspecificosBala.corte)))
        c.drawString(xpeso, ypeso, escribe("PESO: %s Kg" % bigbag.pesobigbag))
        c.drawString(xlote, ylote, escribe("LOTE %s" % bigbag.loteCem.codigo))
        c.drawString(xnumbb, ynumbb, escribe("BIGBAG %s" % bigbag.codigo))
        bar = EanBarCode()
        nombreficheroean13 = bar.getImage(bigbag.articulo.productoVenta.codigo)
        ean13rotado = Image.open(nombreficheroean13)
        ean13rotado = ean13rotado.rotate(90)
        ean13rotado.save(nombreficheroean13)
        c.drawImage(nombreficheroean13, xean, yean)
        codigotrazabilidad = code39.Extended39(bigbag.codigo, xdim = .045*inch)
        codigotrazabilidad.drawOn(c, x39, y39)
        c.setFont("Helvetica", 12)
        c.drawString(xbbcode, ybbcode, escribe(bigbag.codigo))

        c.showPage()

    c.save()
    return nomarchivo


def consumoPartida(partida, salida = "txt"):
    """
    Recibe una partida e imprime un listado de consumos de los partes de
    fabricación de todos los rollos de esa partida y el listado de balas
    empleadas en la misma.
    La partida debe ser un OBJETO partida de PCLASES.
    Si salida == "txt" devuelve una cadena de texto con el resultado de
    la consulta.
    Si salida == "pdf" devuelve el nombre del archivo PDF generado.
    """
    balas = partida.balas
    rollos = partida.rollos
    rollosDefectuosos = partida.rollosDefectuosos
    partes = []
    for rollo in rollos + rollosDefectuosos:
        pdp = rollo.articulos[0].parteDeProduccion
        if pdp == None:
            print "geninformes::consumoPartida -> ¡Rollo [defectuoso] no "\
                  "tiene parte de producción!\n%s" % (rollo)
        if pdp not in partes and pdp != None:
            partes.append(rollo.articulos[0].parteDeProduccion)
    # Diccionario de productos (de compra) consumidos: [cantidad, unidad]
    productos = {}
    for parte in partes:
        for consumo in parte.consumos:
            if consumo.productoCompra.id not in productos:
                prodc = consumo.productoCompra
                productos[prodc.id] = [prodc, 0.0, prodc.unidad]
            productos[consumo.productoCompra.id][1] += consumo.cantidad
    if salida.lower() == "txt":
        res = "CONSUMO DE MATERIALES:\n"
        for ide in productos:
            res += "\t%s\t%.2f\t%s\n" % (productos[ide][0].descripcion,
                                         productos[ide][1], productos[ide][2])
        res += "\nCONSUMO DE MATERIA PRIMA DE LA CARGA DE CUARTOS "\
               "COMPLETA%s:\n" % (partida.partidaCarga
                                  and " " + partida.partidaCarga.codigo or "")
        for bala in balas:
            res += "\t%s\t%.2f\t%s\n" % (
                bala.articulos[0].productoVenta.descripcion,
                bala.pesobala,
                bala.codigo)
    elif salida.lower() == "pdf":
        ### TODO: Generar PDF:
        print "Funcionalidad no disponible temporalmente."
        res = None
    return res

def packingListBalas(datos, numpagina = 1, titulo = "Packing list"):
    """
    Imprime el packing list de una serie de balas.
    numpagina es el número de página del packing list.
    Si el albarán tiene varias LDVs, se llamará a esta función
    para crear una hoja de packing list por producto. En cada
    llamada numpagina traerá el valor correspondiente, y
    se usará para diferenciar los archivos generados (ya que
    se crearán todos a la vez y probablemente con la misma
    fecha y hora).
    """
    global linea, tm, lm, rm, bm

    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(), "packing_list%s_pag_%d.pdf" % (
        give_me_the_name_baby(), numpagina))
    c = canvas.Canvas(nomarchivo)

    fecha = datos['fecha']

    balas = datos['balas']

    xDestino = lm +4
    xEmpresa = width/2 + 4
    xProducto = width/2 - 1.5*inch
    xTipo = width/2 + 2*inch

    # Ponemos la cabecera
    cabecera(c, titulo, fecha)
    # El cuerpo
    c.setFont("Helvetica-Bold", 10)


    linea = tm + 1*inch

    c.drawString(xDestino, linea, escribe(datos['envio']['nombre']))
    c.drawString(xEmpresa, linea, escribe(datos['empresa']['linea0']))
    linea = sigLinea()
    c.drawString(xDestino, linea, escribe(datos['envio']['direccion']))
    c.drawString(xEmpresa, linea, escribe(datos['empresa']['linea1']))
    linea = sigLinea()
    c.drawString(xDestino, linea,
                 escribe(datos['envio']['ciudad'] + datos['envio']['cp']))
    c.drawString(xEmpresa, linea, escribe(datos['empresa']['linea2']))
    linea = sigLinea()
    c.drawString(xDestino, linea, escribe(datos['envio']['pais']))
    c.drawString(xEmpresa, linea, escribe(datos['empresa']['linea3']))
    linea = sigLinea()
    linea = sigLinea()

    el_encogedor_de_fuentes_de_doraemon(c, "Helvetica-Bold", 10, xDestino,
                                        xProducto - 0.5*cm, linea,
                                        'Nº DE LOTE: %s' % (datos['lote']))
    #c.drawString(xDestino, linea, escribe('Nº DE LOTE: ' + datos['lote']))
    el_encogedor_de_fuentes_de_doraemon(c, "Helvetica-Bold", 10, 
                                    xProducto - 0.5*cm, xTipo - 2.75*cm, linea,
                                    escribe('PRODUCTO: '+datos['producto']))
    #c.drawString(xProducto - 0.5*cm, linea, 
    #             escribe('PRODUCTO: ' + datos['producto']))
    c.drawString(xTipo - 2.75*cm, linea, escribe('TIPO: '+ datos['tipo']))
    # XXX: Código de barras EAN del producto
    #from barcode import code39
    from barcode import code128
    from barcode.EANBarCode import EanBarCode
    imbarcode = EanBarCode().getImage(datos['codigo_producto'])
    c.drawImage(imbarcode, rm - 4*cm, linea - 0.25*cm, height = 1.25*cm)
    # XXX

    linea = sigLinea()

    xBala1 = lm + 3 * cm
    xPeso1 = xBala1 + 2.75 * cm
    xCode1 = ((xPeso1 + rm) / 2.0) + 1*cm
    xCode = [xCode1]
    xBala = [xBala1] 
    xPeso = [xPeso1] 
    c.setFont("Helvetica", 8)
    c.drawCentredString(xBala1, linea, escribe('CÓDIGO'))
    c.drawCentredString(xPeso1, linea, escribe('CANTIDAD'))
    c.drawCentredString(xCode1, linea, escribe('CÓDIGO DE BARRAS DEL ARTÍCULO'))
    linea = sigLinea(25)
    i = 0
    balaskeys = list(balas)
    balaskeys.sort(lambda b1, b2: ((b1[0] < b2[0] and -1) 
                                   or (b1[0] > b2[0] and 1) 
                                   or 0))
    for b in balaskeys:
        # XXX: Código de trazabilidad en packing list 
        #      (para Laura Moncho -domher-)
        #anchocodigo = 7.0 * cm
        codigodomenech = b[4]
        # XXX: DOMENECH (Copiado de domenech_h_etiquetasBalasEtiquetadora 
        #                NO MOAR COPYPASTA PLZ!):
        barcodedomenech = code128.Code128(codigodomenech,
                                          #xdim = 0.0205 * inch,
                                          xdim=0.01*cm+(0.005*cm*((11/2)+1)), 
                                            #* ((balaskeys.index(b) / 2) + 1)),
                                          #height = 0.95 * cm)
                                          height = 10 + (0.25*cm * 1))
                                            #* (balaskeys.index(b)%2)))
        ydom = linea 
        xdom = xCode[i] - (barcodedomenech.width / 2.0)
        barcodedomenech.drawOn(c, xdom, ydom)
        c.saveState()
        c.setFont("Courier", 6)
        c.drawCentredString(xdom + (barcodedomenech.width / 2.0),
                            ydom - 0.20 * cm,
                            codigodomenech)
        c.restoreState()
        # XXX: EODOMENECH
        # XXX
        c.drawCentredString(xBala[i], linea, b[0])
        c.drawCentredString(xPeso[i], linea, b[1])
        #c.drawString(rm - 0.4*cm, linea, str(balaskeys.index(b)))
        i += 1
        #if (i*2 == 8):
        #if (i*2 == 6):  # Necesito más espacio, hamijo.
        if (i*2 == 2):  # Necesito más espacio, hamijo.
            i = 0
            linea = sigLinea(30)

        if linea < bm:
            # Me pasé de espacio. Creo la siguiente página.
            c.showPage()
            cabecera(c, titulo + " (cont.)", fecha)
            c.setFont("Helvetica", 8)
            linea = tm + 1*inch

    if i:   # La última fila está coja. Meto espacio.
        linea = sigLinea(20)

    c.setFont("Helvetica", 10)

    c.drawString(xDestino, linea,
                 escribe('TOTAL BULTOS: ' + datos['total']
                         + '    CANTIDAD TOTAL: ' + datos['peso']))
    # Salvamos la página
    c.showPage()
    # Salvamos el documento
    c.save()

    return nomarchivo

def oldPackingListBalas(datos, numpagina = 1, titulo = "Packing list"):
    """
    Imprime el packing list de una serie de balas.
    numpagina es el número de página del packing list.
    Si el albarán tiene varias LDVs, se llamará a esta función
    para crear una hoja de packing list por producto. En cada
    llamada numpagina traerá el valor correspondiente, y
    se usará para diferenciar los archivos generados (ya que
    se crearán todos a la vez y probablemente con la misma
    fecha y hora).
    """
    global linea, tm, lm, rm, bm

    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(), "packing_list%s_pag_%d.pdf" % (
        give_me_the_name_baby(), numpagina))
    c = canvas.Canvas(nomarchivo)

    fecha = datos['fecha']

    balas = datos['balas']

    xDestino = lm +4
    xEmpresa = width/2 + 4
    xProducto = width/2 - 1.5*inch
    xTipo = width/2 + 2*inch

    # Ponemos la cabecera
    cabecera(c, titulo, fecha)
    # El cuerpo
    c.setFont("Helvetica-Bold", 10)


    linea = tm + 1*inch

    c.drawString(xDestino, linea, escribe(datos['envio']['nombre']))
    c.drawString(xEmpresa, linea, escribe(datos['empresa']['linea0']))
    linea = sigLinea()
    c.drawString(xDestino, linea, escribe(datos['envio']['direccion']))
    c.drawString(xEmpresa, linea, escribe(datos['empresa']['linea1']))
    linea = sigLinea()
    c.drawString(xDestino, linea,
                 escribe(datos['envio']['ciudad'] + datos['envio']['cp']))
    c.drawString(xEmpresa, linea, escribe(datos['empresa']['linea2']))
    linea = sigLinea()
    c.drawString(xDestino, linea, escribe(datos['envio']['pais']))
    c.drawString(xEmpresa, linea, escribe(datos['empresa']['linea3']))
    linea = sigLinea()
    linea = sigLinea()

    el_encogedor_de_fuentes_de_doraemon(c, "Helvetica-Bold", 10, xDestino,
                                        xProducto, linea,
                                        'Nº DE LOTE: %s' % (datos['lote']))
    #c.drawString(xDestino, linea, escribe('Nº DE LOTE: ' + datos['lote']))
    c.drawString(xProducto, linea, escribe('PRODUCTO: ' + datos['producto']))
    c.drawString(xTipo, linea, escribe('TIPO: '+ datos['tipo']))

    linea = sigLinea()

    xBala1 = lm + 50
    xPeso1 = xBala1 + (inch*0.80)
    xBala2 = xPeso1 + (inch*0.80) + 10
    xPeso2 = xBala2 + (inch*0.80)
    xBala3 = xPeso2 + (inch*0.80) + 10
    xPeso3 = xBala3 + (inch*0.80)
    xBala4 = xPeso3 + (inch*0.80) + 10
    xPeso4 = xBala4 + (inch*0.80)
    xBala = [xBala1, xBala2, xBala3, xBala4]
    xPeso = [xPeso1, xPeso2, xPeso3, xPeso4]
    c.setFont("Helvetica", 8)
    c.drawCentredString(xBala1, linea, escribe('CÓDIGO'))
    c.drawCentredString(xPeso1, linea, escribe('CANTIDAD'))
    c.drawCentredString(xBala2, linea, escribe('CÓDIGO'))
    c.drawCentredString(xPeso2, linea, escribe('CANTIDAD'))
    c.drawCentredString(xBala3, linea, escribe('CÓDIGO'))
    c.drawCentredString(xPeso3, linea, escribe('CANTIDAD'))
    c.drawCentredString(xBala4, linea, escribe('CÓDIGO'))
    c.drawCentredString(xPeso4, linea, escribe('CANTIDAD'))
    linea = sigLinea()
    i = 0
    for b in balas:
        c.drawCentredString(xBala[i], linea, b[0])
        c.drawCentredString(xPeso[i], linea, b[1])
        i += 1
        if (i*2 == 8):
            i = 0
            linea = sigLinea(10)

    linea = sigLinea()
    linea = sigLinea()
    linea = sigLinea()
    linea = sigLinea()

    c.setFont("Helvetica", 10)

    c.drawString(xDestino, linea,
                 escribe('TOTAL BULTOS: ' + datos['total']
                         + '    CANTIDAD TOTAL: ' + datos['peso']))
    # Salvamos la página
    c.showPage()
    # Salvamos el documento
    c.save()

    return nomarchivo

def _packingListBalas(datos, numpagina = 1, titulo = "Packing list"):
    """
    Imprime el packing list de una serie de balas.
    numpagina es el número de página del packing list.
    Si el albarán tiene varias LDVs, se llamará a esta función
    para crear una hoja de packing list por producto. En cada
    llamada numpagina traerá el valor correspondiente, y
    se usará para diferenciar los archivos generados (ya que
    se crearán todos a la vez y probablemente con la misma
    fecha y hora).
    BACKUP: Este a mí me funciona. Por tanto lo copio para poder jugar con el 
    otro, a ver si Laura Moncho se compra una buena pistola de código de 
    barras.
    """
    from barcode import code128
    from barcode.EANBarCode import EanBarCode
    global linea, tm, lm, rm, bm

    # Creo el fichero
    nomarchivo = os.path.join(gettempdir(), "packing_list%s_pag_%d.pdf" % (
        give_me_the_name_baby(), numpagina))
    c = canvas.Canvas(nomarchivo)

    fecha = datos['fecha']
    balas = datos['balas']

    ## Medidas
    xDestino = lm +4
    xEmpresa = width/2 + 4
    xProducto = width/2 - 1.5*inch
    xTipo = width/2 + 2*inch

    ## Marco y cabecera
    cabecera(c, titulo, fecha)

    ## El cuerpo. Y no me refiero a Rocío.
    c.setFont("Helvetica-Bold", 10)


    linea = tm + 1*inch

    c.drawString(xDestino, linea, escribe(datos['envio']['nombre']))
    c.drawString(xEmpresa, linea, escribe(datos['empresa']['linea0']))
    linea = sigLinea()
    c.drawString(xDestino, linea, escribe(datos['envio']['direccion']))
    c.drawString(xEmpresa, linea, escribe(datos['empresa']['linea1']))
    linea = sigLinea()
    c.drawString(xDestino, linea,
                 escribe(datos['envio']['ciudad'] + datos['envio']['cp']))
    c.drawString(xEmpresa, linea, escribe(datos['empresa']['linea2']))
    linea = sigLinea()
    c.drawString(xDestino, linea, escribe(datos['envio']['pais']))
    c.drawString(xEmpresa, linea, escribe(datos['empresa']['linea3']))
    linea = sigLinea()
    linea = sigLinea()

    el_encogedor_de_fuentes_de_doraemon(c, "Helvetica-Bold", 10, xDestino,
                                        xProducto - 0.5*cm, linea,
                                        'Nº DE LOTE: %s' % (datos['lote']))
    #c.drawString(xDestino, linea, escribe('Nº DE LOTE: ' + datos['lote']))
    el_encogedor_de_fuentes_de_doraemon(c, "Helvetica-Bold", 10, 
                                    xProducto - 0.5*cm, xTipo - 2.75*cm, linea,
                                    escribe('PRODUCTO: '+datos['producto']))
    #c.drawString(xProducto - 0.5*cm, linea, 
    #             escribe('PRODUCTO: ' + datos['producto']))
    c.drawString(xTipo - 2.75*cm, linea, escribe('TIPO: '+ datos['tipo']))
    # XXX: Código de barras EAN del producto
    #from barcode import code39
    imbarcode = EanBarCode().getImage(datos['codigo_producto'])
    c.drawImage(imbarcode, rm - 4*cm, linea - 0.25*cm, height = 1.25*cm)
    # XXX

    linea = sigLinea()

    #xBala1 = lm + 50
    xCode1 = lm - 0.5*cm
    xBala1 = xCode1 + 7.25*cm
    xPeso1 = xBala1 + (inch*0.60)
    xCode2 = xPeso1 + 1*cm
    xBala2 = xCode2 + 7.25*cm
    xPeso2 = xBala2 + (inch*0.60)
    xCode = [xCode1, xCode2]
    xBala = [xBala1, xBala2] #, xBala3] #, xBala4]
    xPeso = [xPeso1, xPeso2] #, xPeso3] #, xPeso4]
    c.setFont("Helvetica", 8)
    c.drawCentredString(xBala1, linea, escribe('CÓDIGO'))
    c.drawCentredString(xPeso1, linea, escribe('CANTIDAD'))
    c.drawCentredString(xBala2, linea, escribe('CÓDIGO'))
    c.drawCentredString(xPeso2, linea, escribe('CANTIDAD'))
    linea = sigLinea(25)
    i = 0
    for b in balas:
        # XXX: Código de trazabilidad en packing list 
        #      (para Laura Moncho -domher-)
        #anchocodigo = 7.0 * cm
        codigodomenech = b[4]
        # XXX: DOMENECH (Copiado de domenech_h_etiquetasBalasEtiquetadora 
        #                NO MOAR COPYPASTA PLZ!):
        barcodedomenech = code128.Code128(codigodomenech,
                                          #xdim = 0.0205 * inch,
                                          xdim = 0.0105 * inch,
                                          #height = 0.95 * cm)
                                          height = 10)
        ydom = linea 
        xdom = (xCode[i] + xBala[i])/2.0 - (barcodedomenech.width / 2.0)
        barcodedomenech.drawOn(c, xdom, ydom)
        c.saveState()
        c.setFont("Courier", 6)
        c.drawCentredString(xdom + (barcodedomenech.width / 2.0),
                            ydom - 0.20 * cm,
                            codigodomenech)
        c.restoreState()
        # XXX: EODOMENECH
        # XXX
        c.drawCentredString(xBala[i], linea, b[0])
        c.drawCentredString(xPeso[i], linea, b[1])
        i += 1
        #if (i*2 == 8):
        #if (i*2 == 6):  # Necesito más espacio, hamijo.
        if (i*2 == 4):  # Necesito más espacio, hamijo.
            i = 0
            linea = sigLinea(20)

        if linea < bm:
            # Me pasé de espacio. Creo la siguiente página.
            c.showPage()
            cabecera(c, titulo + " (cont.)", fecha)
            c.setFont("Helvetica", 8)
            linea = tm + 1*inch

    if i:   # La última fila está coja. Meto espacio.
        linea = sigLinea(20)

    c.setFont("Helvetica", 10)

    c.drawString(xDestino, linea,
                 escribe('TOTAL BULTOS: ' + datos['total']
                         + '    CANTIDAD TOTAL: ' + datos['peso']))
    # Salvamos la página
    c.showPage()
    # Salvamos el documento
    c.save()

    return nomarchivo


# XXX: Prueba de código de barras:
#from reportlab.extensions.barcode import code93
from barcode import code93
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Frame
from reportlab.lib.units import mm


def prueba():
    c = Canvas("barcode.pdf")

    story = []
    story.append(code93.Extended93("Un codigo de barras", xdim = mm*0.22))
    f = Frame(10*mm, 10*mm, 190*mm, 277*mm, showBoundary=0)
    f.addFromList(story, c)
    c.save()

def prueba2():
    from barcode.EANBarCode import EanBarCode
    bar = EanBarCode()
    p = pclases.ProductoVenta.select()[0]
    # nombrefich = bar.makeFakeCode(p.codigo)
    # El makeFakeCode no genera códigos correctos. Hay que usar:
    nombrefich = bar.getImage(p.codigo)  # @UnusedVariable
    # Antiguamente mostraba el código de barras en la ventana con:
    # self.wids['i_codigoarticulo'].set_from_file(nombrefich)
    # Finalmente, si no interesa que ocupe espacio en disco y ya se ha
    # terminado de usar, borrar con:
    # os.unlink(nombrefich)

def abreviar(cad, l = 8):
    """
    Acorta una cadena hasta dejarla en una longitud «l» intentando 
    respetar la primera palabra.
    """
    separadores = (" ", "_", ",", ".")
    while len(cad) > l:
        for separador in separadores:
            palabras = cad.split(separador)
            # Si de entrada la primera palabra ya es mayor, mal empezamos.
            if len(palabras[0]) > l:
                palabras[0] = palabras[0][:-1]
            # Intento respetar la primera palabra y acorto solo las demás.
            if sum([len(p) for p in palabras]) > l:
                for i in range(1, len(palabras)):
                    palabras[i] = palabras[i][:-1]
            cad = separador.join(palabras)
            # Si solo en separadores me voy a comer el espacio...
            if cad.count(separador) > l:
                cad = cad[::-1].replace(separador, "", 1)[::-1]
            cad = cad.strip()
    return cad

def corregir_nombres_fecha(s):
    """
    Porque todo hombre debe enfrentarse al menos una
    vez en su vida a dos tipos de sistemas operativos:
    los que se no se pasan por el forro las locales,
    y MS-Windows.
    """
    trans = {'Monday': 'lunes',
             'Tuesday': 'martes',
             'Wednesday': 'miércoles',
             'Thursday': 'jueves',
             'Friday': 'viernes',
             'Saturday': 'sábado',
             'Sunday': 'domingo',
             'January': 'enero',
             'February': 'febrero',
             'March': 'marzo',
             'April': 'abril',
             'May': 'mayo',
             'June': 'junio',
             'July': 'julio',
             'August': 'agosto',
             'September': 'septiembre',
             'October': 'octubre',
             'November': 'noviembre',
             'December': 'diciembre'}
    for in_english in trans:
        s = s.replace(in_english, trans[in_english])
    return s



def chequeMonte(cantidad, destinatario, euros, fecha):
    """
    Imprime un cheque de El Monte
    """
    CM = inch / 2.54
    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
        "chequeMonte_%s.pdf" % (give_me_the_name_baby()))
    c = canvas.Canvas(nomarchivo)

    c.setFont("Helvetica", 8)

    alto = 7.7*CM
    ancho = 16.6*CM
    c.setPageSize((ancho, alto))

    xCantidad = 10.6*CM
    yCantidad = alto - 2.3*CM

    xDestinatario = 4.5*CM
    yDestinatario = alto - 2.7*CM

    xEuros = 1.9*CM
    yEuros = alto - 3.1*CM
    yEuros2 = alto - 3.5*CM

    xDia = 5.5*CM
    xMes = 10.5*CM
    xAno = 14.5*CM
    yFecha = alto - 3.9*CM


    fecha = corregir_nombres_fecha(fecha.strftime("%d de %B de %Y"))
    dia, mes, ano = fecha.split(' de ')

    euros2 = ''
    if len(euros) > 95:
        indice = 95
        while euros[indice] != ' ':
            indice -= 1
        euros2 = euros[indice:]
        euros = euros[:indice]

    c.drawString(xCantidad, yCantidad, escribe(cantidad))
    c.drawString(xDestinatario, yDestinatario, escribe(destinatario))
    c.drawString(xEuros, yEuros, escribe(euros))
    c.drawString(xEuros, yEuros2, escribe(euros2))
    c.drawString(xDia, yFecha, escribe(dia))
    c.drawString(xMes, yFecha, escribe(mes))
    c.drawString(xAno, yFecha, escribe(ano))
    c.showPage()
    c.save()

    return nomarchivo

def pagareCaixa(fechaPago, cantidad, proveedor, euros, fechaEmision):
    """
    Imprime un pagaré de La Caixa
    """
    CM = inch / 2.54
    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
        "pagareCaixa_%s.pdf" % (give_me_the_name_baby()))
    c = canvas.Canvas(nomarchivo)

    c.setFont("Helvetica", 8)

    alto = 7.7*CM
    ancho = 16.6*CM
    c.setPageSize((ancho, alto))

    xVencimiento = 2.5*CM
    yVencimiento =  alto - 2.3*CM

    xCantidad = 11.6*CM
    yCantidad = alto - 2.3*CM

    xProveedor = 1*CM
    yProveedor = alto - 3.1*CM

    xEuros = 3.3*CM
    yEuros = alto - 3.5*CM
    yEuros2 = alto - 3.9*CM  # @UnusedVariable

    xFecha = 4.5*CM
    yFecha = alto - 4.3*CM

    vencimiento = corregir_nombres_fecha(fechaPago.strftime("%d de %B de %Y"))

    euros2 = ''  # @UnusedVariable
    if len(euros) > 95:
        indice = 95
        while euros[indice] != ' ':
            indice -= 1
        euros2 = euros[indice:]  # @UnusedVariable
        euros = euros[:indice]

    fecha = corregir_nombres_fecha(fechaEmision.strftime("%A, %d de %B de %Y"))

    c.drawString(xVencimiento, yVencimiento, escribe(vencimiento))
    c.drawString(xCantidad, yCantidad, escribe(cantidad))
    c.drawString(xProveedor, yProveedor, escribe(proveedor))
    c.drawString(xEuros, yEuros, escribe(euros))
    c.drawString(xFecha, yFecha, escribe(fecha))
    c.showPage()
    c.save()

    return nomarchivo


def pagareMonte(fechaPago, cantidad, proveedor, euros, fechaEmision):
    """
    Imprime un pagaré de El Monte
    """
    CM = inch / 2.54
    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
        "pagareMonte_%s.pdf" % (give_me_the_name_baby()))
    c = canvas.Canvas(nomarchivo)

    c.setFont("Helvetica", 8)

    alto = 7.7*CM
    ancho = 16.6*CM
    c.setPageSize((ancho, alto))

    xVencimientoDia = 3*CM
    xVencimientoMes = 4.5*CM
    xVencimientoAno = 7.7*CM
    yVencimiento = alto - 2.3*CM

    xCantidad = 11.6*CM
    yCantidad = alto - 2.3*CM

    xProveedor = 1*CM
    yProveedor = alto - 3.1*CM

    xEuros = 3.3*CM
    yEuros = alto - 3.5*CM
    yEuros2 = alto - 3.9*CM

    xDia = 9*CM
    xMes = 11*CM
    xAno = 14.5*CM
    yFecha = alto - 4.3*CM


    fecha = corregir_nombres_fecha(fechaPago.strftime("%d de %B de %Y"))
    vencimientoDia, vencimientoMes, vencimientoAno = fecha.split(' de ')

    euros2 = ''
    if len(euros) > 95:
        indice = 95
        while euros[indice] != ' ':
            indice -= 1
        euros2 = euros[indice:]
        euros = euros[:indice]

    fecha = corregir_nombres_fecha(fechaEmision.strftime("%d de %B de %Y"))
    dia, mes, ano = fecha.split(' de ')

    c.drawString(xVencimientoDia, yVencimiento, escribe(vencimientoDia))
    c.drawString(xVencimientoMes, yVencimiento, escribe(vencimientoMes))
    c.drawString(xVencimientoAno, yVencimiento, escribe(vencimientoAno))
    c.drawString(xCantidad, yCantidad, escribe(cantidad))
    c.drawString(xProveedor, yProveedor, escribe(proveedor))
    c.drawString(xEuros, yEuros, escribe(euros))
    c.drawString(xEuros, yEuros2, escribe(euros2))
    c.drawString(xDia, yFecha, escribe(dia))
    c.drawString(xMes, yFecha, escribe(mes))
    c.drawString(xAno, yFecha, escribe(ano))
    c.showPage()
    c.save()

    return nomarchivo

def chequeCaixa(cantidad, destinatario, euros, fecha):
    """
    Imprime un cheque de La Caixa
    """
    CM = inch / 2.54
    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
        "chequeCaixa_%s.pdf" % (give_me_the_name_baby()))
    c = canvas.Canvas(nomarchivo)

    alto = 7.7*CM
    ancho = 16.6*CM
    c.setPageSize((ancho, alto))

    c.setFont("Helvetica", 8)
    xCantidad = 10.6*CM
    yCantidad = alto - 2.3*CM

    xDestinatario = 4.5*CM
    yDestinatario = alto - 2.7*CM

    xEuros = 1.9*CM
    yEuros = alto - 3.1*CM
    yEuros2 = alto - 3.5*CM

    xFecha = 5.5*CM
    yFecha = alto - 3.9*CM

    fecha = corregir_nombres_fecha(fecha.strftime("%A, %d de %B de %Y"))

    euros2 = ''
    if len(euros) > 95:
        indice = 95
        while euros[indice] != ' ':
            indice -= 1
        euros2 = euros[indice:]
        euros = euros[:indice]

    c.drawString(xCantidad, yCantidad, escribe(cantidad))
    c.drawString(xDestinatario, yDestinatario, escribe(destinatario))
    c.drawString(xEuros, yEuros, escribe(euros))
    c.drawString(xEuros, yEuros2, escribe(euros2))
    c.drawString(xFecha, yFecha, escribe(fecha))
    c.showPage()
    c.save()

    return nomarchivo

def generar_etiqueta_pale(pales, tipo = 0):
    """
    Genera una etiqueta por cada palé recibido (o del único recibido si el 
    parámetro no es una lista) del tipo especificado:
    0: Etiqueta completa
    1: Etiqueta sin nombre empresa.
    2: Etiqueta mínima.
    """
    # 0.- Compruebo parámetros.
    if not isinstance(pales, (list, tuple)):
        pales = [pales]
    rangotipos = range(0, 3)
    if not tipo in rangotipos:
        raise ValueError, "El tipo debe estar en el rango %s." % rangotipos
    # 1.- Preparo el lienzo.
    ancho = 12.55 * cm
    alto = 8.4 * cm
    nomarchivo = os.path.join(gettempdir(),
                              "etiq_pale_%s_%d.pdf" % (give_me_the_name_baby(), 
                                                       tipo))
    c = canvas.Canvas(nomarchivo, pagesize = (ancho, alto))
    for pale in pales:
        # 1.1.- Preparo datos en función del tipo de etiqueta.
        data = generar_data_pale(pale, tipo)
        # 1.2.- Imprimo datos en canvas. (Las medidas van en función del tipo 
        #       y se determinan dentro de la función).
        pintar_data_pale(c, data, ancho, alto, tipo)
        # 1.3.- Guardo canvas.
        c.showPage()
    # 2.- Guardo canvas y devuelvo nombre de archivo generado.
    c.save()
    return nomarchivo

def calcular_posiciones_etiqueta_pale(ancho, alto, tipo = 0):
    """
    Devuelve un diccionario de posiciones, fuentes y tamaños donde se 
    dibujarán los textos de la etiqueta en función del tipo recibido.
    """
    res = {}
    res['código'] = (ancho / 2.0, 2*cm, ancho - 0.5*cm, "Courier-Bold", 20)
    res['partida'] = (ancho / 2.0, 1*cm, ancho - 0.5*cm, "Courier-Bold", 18)
    res['marcado'] = (ancho - 3*cm, alto-1.5*cm, ancho - 0.5*cm, 
                      "Helvetica-Bold", 10)
    if tipo >= 1:
        res['producto'] = (ancho / 2.0, 5*cm, ancho, "Courier-Bold", 14)
        res['fibra'] = (ancho / 2.0, 4*cm, ancho, "Courier-Bold", 14)
        if tipo >= 2:
            res['empresa'] = (ancho / 2.0, 6*cm, ancho-0.5*cm, 
                              "Times-Bold", 22)
    return res

def pintar_data_pale(c, data, ancho, alto, tipo = 0):
    """
    Escribe en el canvas, en las posiciones indicadas por el tipo de 
    etiqueta, los datos del palé recibidos en «data».
    """
    sizes = calcular_posiciones_etiqueta_pale(ancho, alto, tipo)
    for campo in data:
        # CWT: Ya no vamos a pintar el código debajo del código de barras:
        if campo == "código": 
            continue
        x, y, anchotexto, fuente, tamanno = sizes[campo]
        cadena = data[campo]
        c.setFont(fuente, tamanno)
        if c.stringWidth(escribe(cadena), fuente, tamanno) < anchotexto:
            c.drawCentredString(x, y, escribe(cadena))
        else:
            # Divido por el espacio central:
            cadena1, cadena2 = utils.dividir_cadena(cadena)
            c.drawCentredString(x, y + (tamanno/2.0) + 1, escribe(cadena1))
            c.drawCentredString(x, y - (tamanno/2.0) - 1, escribe(cadena2))
    # Código de trazabilidad.
    from barcode import code39
    codigobarras = code39.Extended39(data['código'], xdim = .020*inch)
    xcodigobarras = (ancho - codigobarras.width) / 2.0
    codigobarras.drawOn(c, xcodigobarras, sizes['código'][1] + 15)
    # Logotipo de marcado CE.
    anchomarcado = 2 * cm / 2.0
    altomarcado = 1.64 * cm / 2.0
    c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', 'CE.png'), 
                sizes['marcado'][0] - anchomarcado / 2.0, 
                sizes['marcado'][1] + 0.35*cm, 
                width = anchomarcado, height = altomarcado)

def generar_data_pale(pale, tipo = 0):
    """
    Devuelve un diccionario de datos de palé que se van a mostrar en la 
    etiqueta. Todos los datos van ya como texto.
    """
    res = {}
    res['código'] = pale.codigo
    # CWT: Mejor el código al lado de la partida y con la palabra "bolsas".
    #res['partida'] = pale.partidaCem and pale.partidaCem.codigo or ""
    res['partida'] = "%s bolsas. %s" % (
        pale.codigo, pale.partidaCem and pale.partidaCem.codigo or "")
    #res['marcado'] = "9003712-1035"    # (jmadrid) El número no era así. Es: 
    res['marcado'] = "1035-CPD-9003712"
    if tipo >= 1:
        pv = pale.productoVenta
        try:
            res['producto'] = pv.nombre
        except AttributeError:
            res['producto'] = ""
        try:
            ceb = pv.camposEspecificosBala
            res['fibra'] = "Fibra de %s virgen" % (
                                ceb.tipoMaterialBala.descripcion)
            # CWT: dtex = "%s dtex" % utils.float2str(ceb.dtex, autodec = True)
            # CWT: corte = "%d mm" % ceb.corte
        except AttributeError:
            res['fibra'] = "" 
            # CWT: dtex = ""
            # CWT: corte = ""
        if tipo >= 2:
            try:
                empresa = pclases.DatosDeLaEmpresa.select()[0]
                res['empresa'] = empresa.nombre
            except IndexError:
                res['empresa'] = ""
    return res

def generar_etiqueta_caja(cajas, tipo = 0):
    """
    Genera una etiqueta por cada caja recibida (o de la única recibido si el 
    parámetro no es una lista) del tipo especificado:
    0: Etiqueta completa
    1: Etiqueta sin nombre empresa.
    2: Etiqueta mínima.
    """
    # 0.- Compruebo parámetros.
    if not isinstance(cajas, (list, tuple)):
        cajas = [cajas]
    rangotipos = range(0, 3)
    if not tipo in rangotipos:
        raise ValueError, "El tipo debe estar en el rango %s." % rangotipos
    # 1.- Preparo el lienzo.
    ancho = 12.55 * cm
    alto = 8.4 * cm
    nomarchivo = os.path.join(gettempdir(),
                              "etiq_caja_%s_%d.pdf" % (give_me_the_name_baby(), 
                                                       tipo))
    c = canvas.Canvas(nomarchivo, pagesize = (ancho, alto))
    for caja in cajas:
        # 1.1.- Preparo datos en función del tipo de etiqueta.
        data = generar_data_caja(caja, tipo)
        # 1.2.- Imprimo datos en canvas. (Las medidas van en función del tipo 
        #       y se determinan dentro de la función).
        pintar_data_caja(c, data, ancho, alto, tipo)
        # 1.3.- Guardo canvas.
        c.showPage()
    # 2.- Guardo canvas y devuelvo nombre de archivo generado.
    c.save()
    return nomarchivo

def calcular_posiciones_etiqueta_caja(ancho, alto, tipo = 0):
    """
    Devuelve un diccionario de posiciones, fuentes y tamaños donde se 
    dibujarán los textos de la etiqueta en función del tipo recibido.
    """
    res = {}
    res['código'] = (ancho / 2.0, 2*cm, ancho - 0.5*cm, "Courier-Bold", 20)
    res['marcado'] = (ancho/2.0, alto-1.5*cm, ancho/2.0 - 0.20*cm, 
                      "Helvetica-Bold", 10)
    res['descripción'] = (ancho / 2.0, 4.20*cm, ancho, "Courier-Bold", 14)
    res['partida'] = (ancho / 4.0, 1*cm, ancho / 2.0, "Courier-Bold", 12)
    res['palé'] = (3*ancho / 4.0, 1*cm, ancho / 2.0, "Courier-Bold", 12)
    if tipo >= 1:
        res['marcado'] = (ancho - 3*cm, alto-1.5*cm, ancho - 0.5*cm, 
                          "Helvetica-Bold", 10)
        res['descripción'] = (ancho / 2.0, 5.20*cm, ancho, "Courier-Bold", 14)
        res['producto'] = (ancho / 2.0, 4.35*cm, ancho, "Courier-Bold", 14)
        res['fibra'] = (ancho / 2.0, 3.5*cm, ancho, "Courier-Bold", 14)
        if tipo >= 2:
            res['empresa'] = (ancho / 2.0, 6*cm, ancho-0.5*cm, 
                              "Times-Bold", 22)
    return res

def pintar_data_caja(c, data, ancho, alto, tipo = 0):
    """
    Escribe en el canvas, en las posiciones indicadas por el tipo de 
    etiqueta, los datos de la caja recibida en «data».
    """
    sizes = calcular_posiciones_etiqueta_caja(ancho, alto, tipo)
    for campo in data:
        x, y, anchotexto, fuente, tamanno = sizes[campo]
        cadena = data[campo]
        c.setFont(fuente, tamanno)
        if c.stringWidth(escribe(cadena), fuente, tamanno) < anchotexto:
            c.drawCentredString(x, y, escribe(cadena))
        else:
            # Divido por el espacio central:
            cadena1, cadena2 = utils.dividir_cadena(cadena)
            c.drawCentredString(x, y + (tamanno/2.0) + 1, escribe(cadena1))
            c.drawCentredString(x, y - (tamanno/2.0) - 1, escribe(cadena2))
    # Código de trazabilidad.
    from barcode import code39
    codigobarras = code39.Extended39(data['código'], xdim = .020*inch)
    xcodigobarras = (ancho - codigobarras.width) / 2.0
    codigobarras.drawOn(c, xcodigobarras, sizes['código'][1] + 15)
    # Logotipo de marcado CE.
    anchomarcado = 2 * cm / 2.0
    altomarcado = 1.64 * cm / 2.0
    c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', 'CE.png'), 
                sizes['marcado'][0] - anchomarcado / 2.0, 
                sizes['marcado'][1] + 0.35*cm, 
                width = anchomarcado, height = altomarcado)

def generar_data_caja(caja, tipo = 0):
    """
    Devuelve un diccionario de datos de caja que se van a mostrar en la 
    etiqueta. Todos los datos van ya como texto.
    """
    res = {}
    res['código'] = caja.codigo
    res['partida'] = (caja.partidaCem and 
        "Partida %s" % caja.partidaCem.codigo or "")
    res['marcado'] = "1035-CPD-9003712"
    res['descripción'] = "Caja de %d bolsas" % (caja.numbolsas)
    res['palé'] = "Palé %s" % caja.pale.codigo
    if tipo >= 1:
        pv = caja.productoVenta
        try:
            res['producto'] = pv.nombre
        except AttributeError:
            res['producto'] = ""
        try:
            ceb = pv.camposEspecificosBala
            res['fibra'] = "Fibra de %s virgen" % (
                                ceb.tipoMaterialBala.descripcion)
            # CWT: dtex = "%s dtex" % utils.float2str(ceb.dtex, autodec = True)
            # CWT: corte = "%d mm" % ceb.corte
        except AttributeError:
            res['fibra'] = "" 
            # CWT: dtex = ""
            # CWT: corte = ""
        if tipo >= 2:
            try:
                empresa = pclases.DatosDeLaEmpresa.select()[0]
                res['empresa'] = empresa.nombre
            except IndexError:
                res['empresa'] = ""
    return res

def etiquetasBalasEtiquetadora(*args, **kw):
    #return domenech_v_etiquetasBalasEtiquetadora(*args, **kw)
    return domenech_h_etiquetasBalasEtiquetadora(*args, **kw)
    #return _DEPRECATED_etiquetasBalasEtiquetadora(*args, **kw)

def _DEPRECATED_etiquetasBalasEtiquetadora(balas):
    """
    Crea etiquetas para las balas de
    un parte de la línea de fibra.
    Una por etiqueta del tamaño estándar de la impresora CAB: 12.55 x 8.4.
    """
    global linea, tm, lm, rm, bm
    x, y = lm, tm  # @UnusedVariable
    global linea
    MAXLINEAS = 40
    width= 12.55 * cm
    height = 8.4 * cm

    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
        "etiqBalasPeq_%s.pdf" % give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo, pagesize = (width, height))
    ancho, alto = width, height

    # arribaArriba significa linea de "arriba" de los cuadros de "Arriba"
    # El 0 vertical es el borde de abajo
    # El 0 horizontal es el margen derecho
    arriba = alto - 5
    abajo = 5
    izq = width - 5
    der = 5
    xLogo = der + 0.5 * cm
    yLogo = arriba - 1.5 * cm
    xIzquierda = 20
    xDerecha = ancho/2 + 0.25*inch
    yPrimeraLinea = yLogo - 0.7*inch
    ySegundaLinea = yPrimeraLinea - 0.35*inch
    yTerceraLinea = ySegundaLinea - 0.35*inch
    yCuartaLinea = yTerceraLinea - 0.35*inch
    yQuintaLinea = yCuartaLinea - 0.35*inch
    xCodigo = xDerecha + 2.6 * cm
    yCodigo = arriba - 3.75 * cm

    for j in range(len(balas)):  # @UnusedVariable
        temp = balas[0]
        if temp == []:
            break

        rectangulo(c, (izq, arriba), (der, abajo))

        c.setFont("Helvetica-Bold", 26)
        c.drawString(xLogo, yLogo, "GEOTEXAN S.A.")
        c.setFont("Helvetica", 14)
        c.drawString(xIzquierda, yPrimeraLinea,
                     escribe("CODIGO: "+temp['codigo']))

        from barcode import code39
        codigobarras = code39.Extended39(temp['codigo'], xdim = .020*inch)
        codigobarras.drawOn(c, xIzquierda - 0.5 * cm, yPrimeraLinea + 15)

        #c.drawString(xDerecha, yPrimeraLinea,
        #             escribe("COLOR: "+temp['color']))
        c.drawString(xIzquierda, yQuintaLinea,
                     escribe("COLOR: %s" % (temp['color'])))
        c.drawString(xIzquierda, ySegundaLinea,
                     escribe("LOTE: %s" % (temp['lote'])))
        c.drawString(xDerecha, ySegundaLinea,
                     escribe("PESO KG: %s" % (temp['peso'])))
        c.drawString(xIzquierda, yTerceraLinea,
                     escribe("TIPO: %s" % (temp['tipo'])))
        c.drawString(xDerecha, yTerceraLinea,
                     escribe("LONGITUD: %s" % (temp['longitud'])))
        c.drawString(xIzquierda, yCuartaLinea,
                     escribe("BALA Nº: %s" % (temp['nbala'])))
        c.drawString(xDerecha, yCuartaLinea,
                     escribe("DTEX: %s" % (temp['dtex'])))
        c.drawString(xDerecha, yQuintaLinea,
                     escribe("ACABADO: %s" % (temp['acabado'])))

        from barcode.EANBarCode import EanBarCode
        bar = EanBarCode()
        nombreficheroean13 = bar.getImage(temp['codigoBarra'])
        ean13rotado = Image.open(nombreficheroean13)
        ean13rotado = ean13rotado.rotate(90)
        ean13rotado.save(nombreficheroean13)
        c.drawImage(nombreficheroean13, xCodigo, yCodigo)

        balas = balas[1:]

        # XXX: DOMENECH: Por si acaso llegamos a ceder ante el cliente y hay
        # que meter otro código más. Esto se llama bajada de pantacas:
        from barcode import code128
        renteros = re.compile("\d*")
        numerolote = [n for n in renteros.findall(temp['lote']) if n != ""]
        if numerolote != []:
            numerolote = numerolote[0]
            numerobala = [n for n in renteros.findall(temp['codigo']) if n!=""]
            if numerobala != []:
                numerobala = numerobala[0]
                pesobala = temp['peso'].replace(",", ".")
                try:
                    pesobalaenteros, pesobaladecimales = pesobala.split(".")
                    numerolote = int(numerolote)
                    numerobala = int(numerobala)
                    pesobalaenteros = int(pesobalaenteros)
                    pesobaladecimales = int(pesobaladecimales)
                except Exception, msg:
                    print "geninformes::etiquetasBalasEtiquetadora: No se pu"\
                          "dieron extraer los datos para el code128 de Domen"\
                          "ech. Excepción: %s" % (msg)
                else:
                    codigodomenech = "%010d%015d%03d%02d" % (numerolote,
                        numerobala, pesobalaenteros, pesobaladecimales)
                    barcodedomenech = code128.Code128(codigodomenech,
                        xdim = 0.015 * inch, height = 0.5 * cm)
                    ydom = -(width - 0.5 * cm)
                    xdom = (height - barcodedomenech.width) / 2.0
                    c.rotate(90)
                    barcodedomenech.drawOn(c, xdom, ydom)
                    c.saveState()
                    c.setFont("Courier", 5)
                    c.drawCentredString(xdom + (barcodedomenech.width / 2.0),
                        ydom - 0.25 * cm, codigodomenech)
                    c.rotate(-90)
                    c.restoreState()
        # XXX: EODOMENECH

        c.showPage()

    c.save()
    return nomarchivo

def tmp_domenech_etiquetasBalasEtiquetadora(balas):
    """
    Crea etiquetas para las balas de
    un parte de la línea de fibra.
    Una por etiqueta del tamaño estándar de la impresora CAB: 12.55 x 8.4.
    """
    # OJO: Incluye 7 dígitos antes del código de Domenech por requisito del
    # cliente. No instalar hasta que confirme Nicolás.
    global linea, tm, lm, rm, bm
    x, y = lm, tm  # @UnusedVariable
    global linea
    MAXLINEAS = 40
    width= 12.55 * cm
    height = 8.4 * cm

    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
        "tmp_etiqBalasPeq_%s.pdf" % give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo, pagesize = (width, height))
    ancho, alto = width, height

    # arribaArriba significa linea de "arriba" de los cuadros de "Arriba"
    # El 0 vertical es el borde de abajo
    # El 0 horizontal es el margen derecho
    arriba = alto - 5
    abajo = 5
    izq = width - 5
    der = 5
    xLogo = der + 0.5 * cm
    yLogo = arriba - 1.5 * cm
    xIzquierda = 20
    xDerecha = ancho/2 + 0.25*inch
    yPrimeraLinea = yLogo - 0.7*inch
    ySegundaLinea = yPrimeraLinea - 0.35*inch
    yTerceraLinea = ySegundaLinea - 0.35*inch
    yCuartaLinea = yTerceraLinea - 0.35*inch
    yQuintaLinea = yCuartaLinea - 0.35*inch
    xCodigo = xDerecha + 2.6 * cm
    yCodigo = arriba - 3.75 * cm

    for j in range(len(balas)):  # @UnusedVariable
        temp = balas[0]
        if temp == []:
            break

        rectangulo(c, (izq, arriba), (der, abajo))

        c.setFont("Helvetica-Bold", 26)
        c.drawString(xLogo, yLogo, "GEOTEXAN S.A.")
        c.setFont("Helvetica", 14)
        c.drawString(xIzquierda, yPrimeraLinea,
                     escribe("CODIGO: "+temp['codigo']))

        from barcode import code39
        codigobarras = code39.Extended39(temp['codigo'], xdim = .020*inch)
        codigobarras.drawOn(c, xIzquierda - 0.5 * cm, yPrimeraLinea + 15)

        #c.drawString(xDerecha, yPrimeraLinea,
        #             escribe("COLOR: "+temp['color']))
        c.drawString(xIzquierda, yQuintaLinea,
                     escribe("COLOR: %s" % (temp['color'])))
        c.drawString(xIzquierda, ySegundaLinea,
                     escribe("LOTE: %s" % (temp['lote'])))
        c.drawString(xDerecha, ySegundaLinea,
                     escribe("PESO KG: %s" % (temp['peso'])))
        c.drawString(xIzquierda, yTerceraLinea,
                     escribe("TIPO: %s" % (temp['tipo'])))
        c.drawString(xDerecha, yTerceraLinea,
                     escribe("LONGITUD: %s" % (temp['longitud'])))
        c.drawString(xIzquierda, yCuartaLinea,
                     escribe("BALA Nº: %s" % (temp['nbala'])))
        c.drawString(xDerecha, yCuartaLinea,
                     escribe("DTEX: %s" % (temp['dtex'])))
        c.drawString(xDerecha, yQuintaLinea,
                     escribe("ACABADO: %s" % (temp['acabado'])))

        from barcode.EANBarCode import EanBarCode
        bar = EanBarCode()
        nombreficheroean13 = bar.getImage(temp['codigoBarra'])
        ean13rotado = Image.open(nombreficheroean13)
        ean13rotado = ean13rotado.rotate(90)
        ean13rotado.save(nombreficheroean13)
        c.drawImage(nombreficheroean13, xCodigo, yCodigo)

        balas = balas[1:]

        # XXX: DOMENECH: Por si acaso llegamos a ceder ante el cliente y hay
        # que meter otro código más. Esto se llama bajada de pantacas:
        from barcode import code128
        renteros = re.compile("\d*")
        numerolote = [n for n in renteros.findall(temp['lote']) if n != ""]
        if numerolote != []:
            numerolote = numerolote[0]
            numerobala = [n for n in renteros.findall(temp['codigo'])
                          if n != ""]
            if numerobala != []:
                numerobala = numerobala[0]
                pesobala = temp['peso'].replace(",", ".")
                try:
                    pesobalaenteros, pesobaladecimales = pesobala.split(".")
                    numerolote = int(numerolote)
                    numerobala = int(numerobala)
                    pesobalaenteros = int(pesobalaenteros)
                    pesobaladecimales = int(pesobaladecimales)
                except Exception, msg:
                    print "geninformes::etiquetasBalasEtiquetadora: No se pu"\
                          "dieron extraer los datos para el code128 de Domen"\
                          "ech. Excepción: %s" % (msg)
                else:
                    # codigodomenech = "%010d%015d%03d%02d" % (numerolote,
                    #   numerobala, pesobalaenteros, pesobaladecimales)
                    # XXX: TMP: Para probar nuevas etiquetas de domenech.
                    # Temporal. Esto irá en una nueva tabla.
                    tmp_domenech = {}
                    for p in pclases.ProductoVenta.select(pclases.AND(
                        pclases.ProductoVenta.q.descripcion.contains("6.7"),
                        pclases.NOT(
                         pclases.ProductoVenta.q.descripcion.contains("NEGRO"))
                        )):
                        tmp_domenech[p.codigo] = "007336"
                    for p in pclases.ProductoVenta.select(pclases.AND(
                         pclases.ProductoVenta.q.descripcion.contains("6.7"),
                         pclases.ProductoVenta.q.descripcion.contains("NEGRO"))
                        ):
                        tmp_domenech[p.codigo] = "007337"
                    for p in pclases.ProductoVenta.select(pclases.AND(
                         pclases.ProductoVenta.q.descripcion.contains("4.4"),
                         pclases.ProductoVenta.q.descripcion.contains("NEGRO"))
                        ):
                        tmp_domenech[p.codigo] = "07674"
                    for p in pclases.ProductoVenta.select(pclases.AND(
                        pclases.ProductoVenta.q.descripcion.contains("4.4"),
                        pclases.NOT(
                         pclases.ProductoVenta.q.descripcion.contains("NEGRO"))
                        )):
                        tmp_domenech[p.codigo] = "007852"
                    ean_domenech = int(tmp_domenech[temp['codigoBarra']])
                    codigodomenech = "%07d%010d%015d%03d%02d" % (
                                                        ean_domenech,
                                                        numerolote,
                                                        numerobala,
                                                        pesobalaenteros,
                                                        pesobaladecimales)
                    # barcodedomenech = code128.Code128(codigodomenech,
                    # xdim = 0.015 * inch, height = 0.5 * cm)
                    barcodedomenech = code128.Code128(codigodomenech,
                                                      xdim = 0.012 * inch,
                                                      height = 0.5 * cm)
                    # EOPRUEBASDOMENECH: XXX: TMP: Para probar nuevas
                    # etiquetas de domenech. Temporal. Esto irá en una nueva
                    # tabla.
                    ydom = -(width - 0.5 * cm)
                    xdom = (height - barcodedomenech.width) / 2.0
                    c.rotate(90)
                    barcodedomenech.drawOn(c, xdom, ydom)
                    c.saveState()
                    c.setFont("Courier", 5)
                    c.drawCentredString(xdom + (barcodedomenech.width / 2.0),
                                        ydom - 0.25 * cm,
                                        codigodomenech)
                    c.rotate(-90)
                    c.restoreState()
        # XXX: EODOMENECH

        c.showPage()

    c.save()
    return nomarchivo

def domenech_v_etiquetasBalasEtiquetadora(balas, seriep = None, numped = None):
    """
    Crea etiquetas para las balas de
    un parte de la línea de fibra.
    Una por etiqueta del tamaño estándar de la impresora CAB: 12.55 x 8.4.
    Lleva el código especial para Domenech en vertical.
    «seriep» es la serie del pedido y si no es None, se muestra en los
    3 primeros dígitos.
    «numped» es el número de pedido procedente de Domenech y si no es None se
    muestra en 6 dígitos tras la serie (si la hubiera).
    Estos dos grupos de dígitos opcionales («seriep» y «numped») son comunes
    a toda la serie de balas de las que se generarán las etiquetas.
    El formato completo es:
    * 3 dígitos: serie del pedido, completado con ceros por la derecha.
    * 6 dígitos: número de pedido, completado con ceros por la derecha.
    * 6 dígitos: código de producto: (Solían ser 7 hasta verano'08. Confirmado 
                                      6 en octubre de 2008)
         - 007336 FIBRA PP 6.7 Dtx NATURAL.
         - 007337 FIBRA PP 6.7 Dtx NEGRO.
         - 007674 FIBRA PP 4.5 Dtx NEGRO.
         - 007852 FIBRA PP 4.5 Dtx NATURAL.
    * 10 dígitos: número de lote, completado con ceros por la derecha.
    * 15 dígitos: número de bala, completado con ceros por la derecha.
    * 3 dígitos: parte entera del peso de la bala en kilogramos,
                 completado con ceros por la derecha.
    * 2 dígitos: parte decimal del peso de la bala en kilogramos,
                 completado con ceros por la izquierda.

    Por ejemplo, el código correspondiente a una bala de fibra negra de
    polipropileno de 6.7 dtex, correspondiente al lote 660, de número
    57394, con 286.50 kg de peso y solicitada en el pedido 4/2158; sería:
    0040021580007337000000066000000000005739428650
    """
    global linea, tm, lm, rm, bm
    x, y = lm, tm  # @UnusedVariable
    global linea
    MAXLINEAS = 40
    width= 12.55 * cm
    height = 8.4 * cm
    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
                              "tmp_dv_etiqbala_%s.pdf"%give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo, pagesize = (width, height))
    ancho, alto = width, height
    # arribaArriba significa linea de "arriba" de los cuadros de "Arriba"
    # El 0 vertical es el borde de abajo
    # El 0 horizontal es el margen derecho
    arriba = alto - 5
    abajo = 5
    izq = width - 5
    der = 5
    xLogo = der + 0.5 * cm
    yLogo = arriba - 1.5 * cm
    xIzquierda = 20
    xDerecha = ancho/2 + 0.25*inch
    yPrimeraLinea = yLogo - 0.7*inch
    ySegundaLinea = yPrimeraLinea - 0.35*inch
    yTerceraLinea = ySegundaLinea - 0.35*inch
    yCuartaLinea = yTerceraLinea - 0.35*inch
    yQuintaLinea = yCuartaLinea - 0.35*inch
    xCodigo = xDerecha + 2.6 * cm
    yCodigo = arriba - 3.75 * cm
    for j in range(len(balas)):  # @UnusedVariable
        temp = balas[0]
        if temp == []:
            break
        #rectangulo(c, (izq, arriba), (der, abajo))
        # Saco etiqueta Doménech Hermanos fuera del cuadro para darle más 
        # espacio.
        rectangulo(c, (izq - 1.40*cm, arriba), (der, abajo))
        c.setFont("Helvetica-Bold", 26)
        c.drawString(xLogo, yLogo, "GEOTEXAN S.A.")
        c.setFont("Helvetica", 14)
        c.drawString(xIzquierda,
                     yPrimeraLinea,
                     escribe("CODIGO: " + temp['codigo']))
        from barcode import code39
        codigobarras = code39.Extended39(temp['codigo'], xdim = .020*inch)
        codigobarras.drawOn(c, xIzquierda - 0.5 * cm, yPrimeraLinea + 15)
        #c.drawString(xDerecha, yPrimeraLinea,
        #             escribe("COLOR: "+temp['color']))
        c.drawString(xIzquierda,
                     yQuintaLinea,
                     escribe("COLOR: %s" % (temp['color'])))
        c.drawString(xIzquierda,
                     ySegundaLinea,
                     escribe("LOTE: %s" % (temp['lote'])))
        c.drawString(xDerecha,
                     ySegundaLinea,
                     escribe("PESO KG: %s" % (temp['peso'])))
        c.drawString(xIzquierda,
                     yTerceraLinea,
                     escribe("TIPO: %s" % (temp['tipo'])))
        c.drawString(xDerecha,
                     yTerceraLinea,
                     escribe("LONGITUD: %s" % (temp['longitud'])))
        c.drawString(xIzquierda,
                     yCuartaLinea,
                     escribe("BALA Nº: %s" % (temp['nbala'])))
        c.drawString(xDerecha,
                     yCuartaLinea,
                     escribe("DTEX: %s" % (temp['dtex'])))
        c.drawString(xDerecha,
                     yQuintaLinea,
                     escribe("ACABADO: %s" % (temp['acabado'])))
        from barcode.EANBarCode import EanBarCode
        bar = EanBarCode()
        nombreficheroean13 = bar.getImage(temp['codigoBarra'])
        ean13rotado = Image.open(nombreficheroean13)
        ean13rotado = ean13rotado.rotate(90)
        ean13rotado.save(nombreficheroean13)
        c.drawImage(nombreficheroean13, xCodigo - 0.5*cm, yCodigo)
        balas = balas[1:]
        # XXX: DOMENECH:
        from barcode import code128
        codigodomenech = _build_codigo_domenech(temp, seriep, numped)
        if codigodomenech:
            if len(codigodomenech) > 37:
                barcodedomenech = code128.Code128(codigodomenech,
                                                  xdim = 0.010 * inch,
                                                  height = 0.5 * cm)
            else:
                barcodedomenech = code128.Code128(codigodomenech,
                                                  #xdim = 0.012 * inch,
                                                  xdim = 0.0135 * inch,
                                                  height = 0.95 * cm)
            ydom = -(width - 0.5 * cm)
            xdom = (height - barcodedomenech.width) / 2.0
            c.rotate(90)
            barcodedomenech.drawOn(c, xdom, ydom)
            c.saveState()
            c.setFont("Courier", 5)
            c.drawCentredString(xdom + (barcodedomenech.width / 2.0),
                                ydom - 0.25 * cm,
                                codigodomenech)
            c.rotate(-90)
            c.restoreState()
        # XXX: EODOMENECH
        c.showPage()
    c.save()
    return nomarchivo

def domenech_h_etiquetasBalasEtiquetadora(balas, seriep = None, numped = None):
    """
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
    global linea, tm, lm, rm, bm
    x, y = lm, tm  # @UnusedVariable
    global linea
    MAXLINEAS = 40
    width= 12.55 * cm
    height = 8.4 * cm
    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
                              "dh_etiqbala_%s.pdf"%give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo, pagesize = (width, height))
    ancho, alto = width, height
    # arribaArriba significa linea de "arriba" de los cuadros de "Arriba"
    # El 0 vertical es el borde de abajo
    # El 0 horizontal es el margen derecho
    arriba = alto - 1.45*cm
    #arriba = alto - 5
    abajo = 5
    #abajo = 1.45*cm
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
    for j in range(len(balas)):  # @UnusedVariable
        temp = balas[0]
        if temp == []:
            break
        rectangulo(c, (izq, arriba), (der, abajo))
        c.setFont("Helvetica-Bold", 28)
        c.drawString(xLogo, yLogo, "GEOTEXAN S.A.")
        c.setFont("Helvetica", 14)
        c.drawString(xIzquierda,
                     yPrimeraLinea,
                     escribe("CÓDIGO: " + temp['codigo']))
        from barcode import code39
        codigobarras = code39.Extended39(temp['codigo'], xdim = .020*inch)
        codigobarras.drawOn(c, xIzquierda - 0.5 * cm, yPrimeraLinea + 15)
        #c.drawString(xDerecha, yPrimeraLinea,
        #             escribe("COLOR: "+temp['color']))
        c.drawString(xIzquierda,
                     yQuintaLinea,
                     escribe("COLOR: %s" % (temp['color'])))
        c.drawString(xIzquierda,
                     ySegundaLinea,
                     escribe("LOTE: %s" % (temp['lote'])))
        c.drawString(xDerecha,
                     ySegundaLinea,
                     escribe("PESO KG: %s" % (temp['peso'])))
        c.drawString(xIzquierda,
                     yTerceraLinea,
                     escribe("TIPO: %s" % (temp['tipo'])))
        c.drawString(xDerecha,
                     yTerceraLinea,
                     escribe("LONGITUD: %s" % (temp['longitud'])))
        c.drawString(xIzquierda,
                     yCuartaLinea,
                     escribe("BALA Nº: %s" % (temp['nbala'])))
        c.drawString(xDerecha,
                     yCuartaLinea,
                     escribe("DTEX: %s" % (temp['dtex'])))
        c.drawString(xDerecha,
                     yQuintaLinea,
                     escribe("ACABADO: %s" % (temp['acabado'])))
        from barcode.EANBarCode import EanBarCode
        bar = EanBarCode()
        nombreficheroean13 = bar.getImage(temp['codigoBarra'])
        ean13rotado = Image.open(nombreficheroean13)
        ean13rotado = ean13rotado.rotate(90)
        ean13rotado.save(nombreficheroean13)
        c.drawImage(nombreficheroean13, xCodigo, yCodigo)
        balas = balas[1:]
        # XXX: DOMENECH:
        from barcode import code128
        codigodomenech = _build_codigo_domenech(temp, seriep, numped)
        if codigodomenech:
            barcodedomenech = code128.Code128(codigodomenech,
                                              #xdim = 0.015 * inch,
                                              #height = 0.5 * cm)
                                              xdim = 0.0205 * inch,
                                              height = 0.95 * cm)
            #barcodedomenech = code39.Extended39(codigodomenech,
            #                                  #xdim = 0.015 * inch,
            #                                  #height = 0.5 * cm)
            #                                  xdim = 0.0094 * inch,
            #                                  height = 0.95 * cm)
            ydom = alto - 1.2 * cm
            #ydom = 0.4 * cm
            xdom = (width - barcodedomenech.width) / 2.0
            barcodedomenech.drawOn(c, xdom, ydom)
            c.saveState()
            c.setFont("Courier-Bold", 8)
            c.drawCentredString(xdom + (barcodedomenech.width / 2.0),
                                ydom - 0.20 * cm,
                                codigodomenech)
            c.restoreState()
        # XXX: EODOMENECH
        # XXX: Marca para identificar las nuevas.
        c.saveState()
        c.setFillColorRGB(0, 0, 0)
        c.circle(izq - 0.3*cm, yQuintaLinea, 0.1*cm, fill=1)
        c.restoreState()
        # XXX: EOMarca
        c.showPage()
    c.save()
    return nomarchivo

def _build_codigo_domenech(bala, seriep = None, numped = None):
    """
    Devuelve una cadena con el código domenech completo correspondiente a
    una bala y una serie de pedidos y pedido si los hubiera.
    Si no se pudiese construir el código devuelve None.
    «bala» es un diccionario con información sobre la bala tal cual se
    recibe en la función para generar etiquetas.
    «seriep» y «numped» son opcionales y corresponderían a una serie numérica
    de pedidos y a un número de pedido.
    """
    codigodomenech = None
    renteros = re.compile("\d*")
    numerolote = [n for n in renteros.findall(bala['lote']) if n != ""]
    if numerolote != []:
        numerolote = numerolote[0]
        numerobala=[n for n in renteros.findall(bala['codigo']) if n != ""]
        if numerobala != []:
            numerobala = numerobala[0]
            pesobala = bala['peso'].replace(",", ".")
            try:
                pesobalaenteros, pesobaladecimales = pesobala.split(".")
                numerolote = int(numerolote)
                numerobala = int(numerobala)
                pesobalaenteros = int(pesobalaenteros)
                pesobaladecimales = int(pesobaladecimales)
            except Exception, msg:
                print "geninformes::etiquetasBalasEtiquetadora: "\
                      "No se pudieron extraer los datos para el code128 "\
                      "de Domenech. Excepción: %s" % (msg)
            else:
                try:
                    ean_domenech = _get_ean_domenech(bala['codigoBarra'])
                except KeyError:    # No hay código "Dom-EAN" para este prod.
                    ean_domenech = 0
                #codigodomenech = "%07d%010d%015d%03d%02d" % (
                codigodomenech = "%06d%010d%015d%03d%02d" % (
                    ean_domenech,
                    numerolote,
                    numerobala,
                    pesobalaenteros,
                    pesobaladecimales)
                if numped:
                    try:
                        if not isinstance(numped, (int, str)):
                            numped = str(numped)
                        if isinstance(numped, str):
                            numped = [n for n in renteros.findall(numped)
                                      if n != ""][0]
                        intnumped = int(numped)
                        codnumped = "%06d" % intnumped
                        codigodomenech = codnumped + codigodomenech
                    except (IndexError, ValueError, TypeError), msg:
                        print "geninformes: Domenech. " + msg
                if seriep:
                    try:
                        if not isinstance(seriep, (int, str)):
                            seriep = str(seriep)
                        if isinstance(seriep, str):
                            seriep = [n for n in renteros.findall(seriep)
                                      if n != ""][0]
                        intseriep = int(seriep)
                        codseriep = "%03d" % intseriep
                        codigodomenech = codseriep + codigodomenech
                    except (IndexError, ValueError, TypeError), msg:
                        print "geninformes: Domenech. " + msg
    return codigodomenech

def _get_ean_domenech(codigo):
    """
    Dado un código de producto, devuelve el código "EAN8" (muy entre comillas)
    del cliente Domenech. Todo esto presumíblemente irá donde corresponde:
    como atributo del producto, etcétera. Pero no es definitivo y hay que
    mandar pruebas de etiquetas al cliente.
    """
    tmp_domenech = {}
    for p in pclases.ProductoVenta.select(pclases.AND(
          pclases.ProductoVenta.q.descripcion.contains("6.7"),
          pclases.NOT(pclases.ProductoVenta.q.descripcion.contains("NEGRO")))):
        tmp_domenech[p.codigo] = "007336"
    for p in pclases.ProductoVenta.select(pclases.AND(
          pclases.ProductoVenta.q.descripcion.contains("6.7"),
          pclases.ProductoVenta.q.descripcion.contains("NEGRO"))):
        tmp_domenech[p.codigo] = "007337"
    for p in pclases.ProductoVenta.select(pclases.AND(
          pclases.ProductoVenta.q.descripcion.contains("4.4"),
          pclases.ProductoVenta.q.descripcion.contains("NEGRO"))):
        tmp_domenech[p.codigo] = "07674"
    for p in pclases.ProductoVenta.select(pclases.AND(
          pclases.ProductoVenta.q.descripcion.contains("4.4"),
          pclases.NOT(pclases.ProductoVenta.q.descripcion.contains("NEGRO")))):
        tmp_domenech[p.codigo] = "007852"
    ean_domenech = int(tmp_domenech[codigo])
    return ean_domenech

def etiquetasBalasCableEtiquetadora(balas):
    """
    Crea etiquetas para las balas de cable de
    un parte de la línea de fibra.
    Una por etiqueta del tamaño estándar de la impresora CAB: 12.55 x 8.4.
    """
    global linea, tm, lm, rm, bm
    x, y = lm, tm  # @UnusedVariable
    global linea
    MAXLINEAS = 40
    width= 12.55 * cm
    height = 8.4 * cm

    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
        "etiqBalasCablePeq_%s.pdf" % give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo, pagesize = (width, height))
    ancho, alto = width, height

    # arribaArriba significa linea de "arriba" de los cuadros de "Arriba"
    # El 0 vertical es el borde de abajo
    # El 0 horizontal es el margen derecho
    arriba = alto - 5
    abajo = 5
    izq = width - 5
    der = 5
    xLogo = der + 0.5 * cm
    yLogo = arriba - 3.0 * cm
    xIzquierda = 20
    xDerecha = ancho/2 + 0.25*inch
    yPrimeraLinea = yLogo - 0.7*inch
    ySegundaLinea = yPrimeraLinea - 0.35*inch
    yTerceraLinea = ySegundaLinea - 0.35*inch
    yCuartaLinea = yTerceraLinea - 0.35*inch
    yQuintaLinea = yCuartaLinea - 0.35*inch  # @UnusedVariable
    xCodigo = xDerecha + 3.0 * cm
    yCodigo = arriba - 4.00 * cm

    for j in range(len(balas)):  # @UnusedVariable
        temp = balas[0]
        if temp == []:
            break

        rectangulo(c, (izq, arriba), (der, abajo))

        c.setFont("Helvetica-Bold", 26)
        c.drawString(xLogo, yLogo, "GEOTEXAN S.A.")
        c.setFont("Helvetica", 14)
        c.drawString(xIzquierda, yPrimeraLinea,
                     escribe("CODIGO: "+temp['codigo']))

        from barcode import code39
        codigobarras = code39.Extended39(temp['codigo'], xdim = .020*inch)
        codigobarras.drawOn(c, xIzquierda - 0.5 * cm, yPrimeraLinea + 15)
        c.drawString(xIzquierda, ySegundaLinea,
                     escribe("PESO KG: %s" % (temp['peso'])))
        agregarFila(xIzquierda, yTerceraLinea, ancho, escribe(temp['color']),
                    c, "Helvetica", 14, a_derecha = False, altura_linea = 16)
        from barcode.EANBarCode import EanBarCode
        bar = EanBarCode()
        nombreficheroean13 = bar.getImage(temp['codigoBarra'])
        ean13rotado = Image.open(nombreficheroean13)
        ean13rotado = ean13rotado.rotate(90)
        ean13rotado.save(nombreficheroean13)
        c.drawImage(nombreficheroean13, xCodigo, yCodigo)
        c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', 'reciclar.gif'),
                    (ancho - 157 / 3.0)/ 2.0,
                     arriba - 156 / 3.0 - 0.2 * cm,
                     width = 157 / 3.0,
                     height = 156 / 3.0)

        balas = balas[1:]

        c.showPage()

    c.save()
    return nomarchivo

def etiquetasRollosCEtiquetadora(rollos):
    """
    Crea etiquetas para las rollos de cable de
    un parte de la línea de fibra.
    Una por etiqueta del tamaño estándar de la impresora CAB: 12.55 x 8.4.
    """
    global linea, tm, lm, rm, bm
    x, y = lm, tm  # @UnusedVariable
    global linea
    MAXLINEAS = 40
    width= 12.55 * cm
    height = 8.4 * cm

    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
        "etiqRollosCPeq_%s.pdf" % give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo, pagesize = (width, height))
    ancho, alto = width, height

    # arribaArriba significa linea de "arriba" de los cuadros de "Arriba"
    # El 0 vertical es el borde de abajo
    # El 0 horizontal es el margen derecho
    arriba = alto - 5
    abajo = 5
    izq = width - 5
    der = 5
    xLogo = der + 0.5 * cm
    yLogo = arriba - 3.0 * cm
    xIzquierda = 20
    xDerecha = ancho/2 + 0.25*inch
    yPrimeraLinea = yLogo - 0.7*inch
    ySegundaLinea = yPrimeraLinea - 0.35*inch
    yTerceraLinea = ySegundaLinea - 0.35*inch
    yCuartaLinea = yTerceraLinea - 0.35*inch
    yQuintaLinea = yCuartaLinea - 0.35*inch  # @UnusedVariable
    xCodigo = xDerecha + 3.0 * cm
    yCodigo = arriba - 4.00 * cm

    for j in range(len(rollos)):  # @UnusedVariable
        temp = rollos[0]
        if temp == []:
            break

        rectangulo(c, (izq, arriba), (der, abajo))

        c.setFont("Helvetica-Bold", 26)
        c.drawString(xLogo, yLogo, "GEOTEXAN S.A.")
        c.setFont("Helvetica", 14)
        c.drawString(xIzquierda, yPrimeraLinea,
                     escribe("CODIGO: "+temp['codigo']))

        from barcode import code39
        codigobarras = code39.Extended39(temp['codigo'], xdim = .020*inch)
        codigobarras.drawOn(c, xIzquierda - 0.5 * cm, yPrimeraLinea + 15)
        c.drawString(xIzquierda,
                     ySegundaLinea,
                     escribe("PESO KG: %s" % (temp['peso'])))
        agregarFila(xIzquierda,
                    yTerceraLinea,
                    ancho,
                    escribe(temp['descripción']),
                    c,
                    "Courier-BoldOblique",
                    18,
                    a_derecha = False,
                    altura_linea = 16)
        from barcode.EANBarCode import EanBarCode
        bar = EanBarCode()
        nombreficheroean13 = bar.getImage(temp['codigoBarra'])
        ean13rotado = Image.open(nombreficheroean13)
        ean13rotado = ean13rotado.rotate(90)
        ean13rotado.save(nombreficheroean13)
        c.drawImage(nombreficheroean13, xCodigo, yCodigo)
        c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', 'mpp.png'),
                    (ancho - 686 / 5.0)/ 2.0,
                     arriba - 152 / 5.0 - 0.6 * cm,
                     width = 686 / 5.0,
                     height = 152 / 5.0)

        rollos = rollos[1:]

        c.showPage()

    c.save()
    return nomarchivo


def _etiquetasRollosEtiquetadora(rollos, mostrar_marcado):
    """
    Crea etiquetas para los rollos de
    un parte de la línea de geotextil
    """
    global linea, tm, lm, rm, bm
    x, y = lm, tm  # @UnusedVariable
    global linea
    MAXLINEAS = 40

    CM = inch / 2.54
    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
        "etiqRollosPeq_%s.pdf" % give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo)
    alto = 12.6*CM
    ancho = 12.4*CM
    c.setPageSize((ancho, alto))

    # arribaArriba significa linea de "arriba" de los cuadros de "Arriba"
    # El 0 vertical es el borde de abajo
    # El 0 horizontal es el margen derecho
    arriba = alto - 5
    abajo = 5

    izq = 8*CM
    der = 5

    xCE = alto/2
    yCE = 0.8*inch
    xCodigoCE = xCE
    yCodigoCE = yCE + 0.4*inch
    xDescripcion = xCE
    yDescripcion = yCodigoCE + 0.4*inch
    xDensidad = xCE
    yDensidad = yDescripcion + 0.3*inch
    xIzquierda = 20
    xDerecha = alto/2 - 0.5*inch
    yPrimeraLinea = yDensidad +0.3*inch
    ySegundaLinea = yPrimeraLinea + 0.2*inch
    yTerceraLinea = ySegundaLinea + 0.2*inch
    yCuartaLinea = yTerceraLinea + 0.4*inch

    for j in range(len(rollos)):  # @UnusedVariable
        temp = rollos[0]
        if temp == []:
            break

        rectangulo(c, (izq, arriba), (der, abajo))

        c.rotate(90)

        if mostrar_marcado:
            c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', 'CE.png'),
                xCE - (3 * cm / 2), -yCE, width = 2 * cm, height = 1.64 * cm)
            c.setFont("Helvetica", 20)
            c.drawCentredString(xCodigoCE, -yCodigoCE, "1035-CPD-ES033858")
        c.setFont("Helvetica-Bold", 26)
        c.drawCentredString(xDescripcion, -yDescripcion,
            escribe(temp['descripcion']))
        c.setFont("Helvetica", 20)
        c.drawCentredString(xDensidad, -yDensidad,
            escribe(temp['densidad']+" gr/m²"))
        c.setFont("Helvetica", 14)
        c.drawString(xIzquierda, -yPrimeraLinea,
            escribe("Ancho: "+temp['ancho']))
        c.drawString(xDerecha, -yPrimeraLinea, escribe("M²: "+temp['m2']))
        c.drawString(xIzquierda, -ySegundaLinea,
            escribe("Peso: "+temp['peso']))
        c.drawString(xDerecha, -ySegundaLinea, escribe("M.lin: "+temp['mlin']))
        c.drawString(xIzquierda, -yTerceraLinea,
            escribe("Partida: "+temp['partida']))

        c.setFont("Helvetica-Bold", 28)
        c.drawString(xIzquierda, -yCuartaLinea,
            escribe("Nº rollo: "+temp['nrollo']))
        from barcode.EANBarCode import EanBarCode
        bar = EanBarCode()
        c.drawImage(bar.getImage(temp['codigo']), xDerecha+1.25*inch,
            -ySegundaLinea)
        from barcode import code39
        codigobarras = code39.Extended39(temp['codigo39'], xdim = .015*inch)
        codigobarras.drawOn(c, xDerecha+0.9*inch, -yCuartaLinea+10)
        c.setFont("Helvetica", 8)
        c.drawString(xDerecha+1.9*inch, -yCuartaLinea,
            escribe(temp['codigo39']))

        c.rotate(-90)
        rollos = rollos[1:]
        c.setPageRotation(90)
        c.showPage()

    c.save()
    return nomarchivo

def cuadrito(c, x, y, relleno):
    """
    Dibuja en checkbox en el pdf y lo rellena
    si el parámetro está a 1
    """
    c.rect(x, y, 4, 4, fill = relleno)

def ausencia(empleado, centro, fecha, turno, motivo, motivos):
    """
    Imprime un informe para una ausencia dada
    """
    datos_empresa = pclases.DatosDeLaEmpresa.select()[0]

    global linea, lm, rm, tm, bm
    # Creo la hoja
    nomarchivo = os.path.join(gettempdir(),
        "ausencia_%s.pdf" % give_me_the_name_baby())
    c = canvas.Canvas(nomarchivo)
    # Ponemos la cabecera
    titulo1 = 'GEOTEXAN S.A.'
    titulo = 'COMUNICACIÓN DE PERMISOS Y ASUNTOS PROPIOS DEL PERSONAL'
    xIzquierda = lm -4
    c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', datos_empresa.logo),
                lm+0.1*inch, height - 1.2*inch, 0.9*inch, 0.9*inch)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(lm+3.2*inch, height-0.65*inch, escribe(titulo1))
    c.drawString(lm+1.1*inch, height-inch, escribe(titulo))
    rectangulo(c, (xIzquierda, height-25), (rm, height-1.20*inch))

    xIzquierda = lm
    yPrimeraLinea = height - 2*inch

    xDerecha = width/2 + (1.5 * inch)

    ySegundaLinea = yPrimeraLinea - 20
    yTerceraLinea = ySegundaLinea - 20
    yCuartaLinea = yTerceraLinea - 10
    yQuintaLinea = yCuartaLinea -15

    yPrimeraLineaFinal = 3*inch
    ySegundaLineaFinal = yPrimeraLineaFinal - 20
    yTerceraLineaFinal = ySegundaLineaFinal - 30
    yCuartaLineaFinal = yTerceraLineaFinal - 15
    yCuartaLineaFinal1 = yCuartaLineaFinal - 10
    yQuintaLineaFinal = yCuartaLineaFinal - inch

    c.drawString(width/2, ySegundaLinea, escribe('COMUNICA'))

    # Lista de motivos
    c.setFont("Helvetica", 10)
    xMotivo1 = xIzquierda + (1/4.0 * inch)
    xMotivo2 = xDerecha
    linea = yQuintaLinea
    motivos = list(motivos)
    #############################################
    def sort_por_descripcion(m1, m2):           #
        if m1.descripcion < m2.descripcion:     #
            return -1                           #
        elif m1.descripcion > m2.descripcion:   #
            return 1                            #
        return 0                                #
    #############################################
    motivos.sort(sort_por_descripcion)
    for m in motivos:
        if m == motivo:
            # Marco el que sea
            relleno = 1
        else:
            relleno = 0
        cuadrito(c, xMotivo1-6, linea+1, relleno)
        c.setFont("Helvetica", 10)
        #c.drawString(xMotivo1, linea, escribe("%s%s" % (m.descripcion,
        # m.penaliza and " (*)" or "")))
        saltos = agregarFila(xMotivo1, linea, xMotivo2,
            escribe("%s%s" % (m.descripcion, m.penaliza and " (*)" or "")), c,
            "Helvetica", 10, a_derecha = False, altura_linea = 12)
        for i in xrange(saltos - 1):  # @UnusedVariable
            linea = sigLinea(12)
        c.setFont("Helvetica", 8)
        c.drawString(xMotivo2, linea, escribe(m.descripcionDias))
        linea = sigLinea(14)
    c.saveState()
    c.setFont("Helvetica-Bold", 8)
    #c.drawString(xMotivo1, linea, escribe("Notas:"))
    linea = sigLinea(12)
    cursiva(c, xMotivo1, linea, escribe("Notas:"), "Helvetica-Bold", 8,
            (0, 0, 0), 10)
    c.line(xMotivo1, linea - 2, xMotivo1 + 90, linea - 2)
    linea = sigLinea(12)
    c.setFont("Helvetica", 8)
    c.drawString(xMotivo1, linea,
      escribe("Clase 1: Cónyuge, hijos, padres, padres políticos y hermanos."))
    linea = sigLinea(12)
    c.drawString(xMotivo1, linea,
        escribe("Clase 2: Abuelos, nietos y hermanos políticos."))
    linea = sigLinea(12)
    c.drawString(xMotivo1, linea, escribe("Clase 3: Tíos y sobrinos."))
    linea = sigLinea(12)
    c.drawString(xMotivo1, linea,
        escribe("Clase 4: Persona que conviva en el hogar familiar."))
    c.restoreState()
    # Impreso
    c.setFont("Helvetica", 11)

    c.drawString(xIzquierda, yPrimeraLinea, escribe('D/Dña ' + empleado))
    c.drawString(xDerecha, yPrimeraLinea, escribe('Centro trabajo: ' + centro))

    fecha_cad = corregir_nombres_fecha(fecha.strftime("%A, %d de %B de %Y"))
    c.drawString(xIzquierda, yTerceraLinea,
        escribe('Que el próximo día %s, siendo su turno %s, no acudirá '\
                'a su puesto de' % (fecha_cad, turno)))
    c.drawString(xIzquierda, yCuartaLinea,
        escribe('trabajo por el siguiente motivo:'))

    c.drawString(xIzquierda, yPrimeraLineaFinal,
        escribe('(*) Estos motivos de ausencia al puesto de trabajo penalizan'\
                ' en el cómputo para el Plus de no absentismo'))
    c.drawString(xDerecha, ySegundaLineaFinal, escribe('Fdo. El Trabajador'))
    c.drawString(xDerecha, yTerceraLineaFinal, escribe('Fecha:'))
    rectangulo(c, (xIzquierda, yCuartaLineaFinal), (rm/3, yQuintaLineaFinal))
    rectangulo(c, (rm/3, yCuartaLineaFinal), (2*rm/3, yQuintaLineaFinal))
    rectangulo(c, (2*rm/3, yCuartaLineaFinal), (rm, yQuintaLineaFinal))
    c.drawRightString(rm/4, yCuartaLineaFinal1, escribe('VºBº Gerencia'))
    c.drawCentredString(rm/2, yCuartaLineaFinal1,
        escribe('VºBº Dción Técnica'))
    c.drawString(3*rm/4, yCuartaLineaFinal1, escribe('VºBº Encargado'))
    try:
        datos_empresa = pclases.DatosDeLaEmpresa.select()[0]
    except IndexError:
        print "geninformes::ausencia -> No se encontraron los datos de la "\
              "empresa en la tabla datos_de_la_empresa."
    else:
        c.setFont("Times-Roman", 10)
        c.drawCentredString((rm - lm)/2.0, bm - 0.5*cm,
            escribe(datos_empresa.nombre))
    c.setFont("Times-Italic", 8)
    c.drawCentredString((rm - lm)/2.0, bm - 1.0*cm,
        escribe("Dpto. Admón-Contabilidad"))
    # Salvamos la página
    c.showPage()
    # Salvamos el documento
    c.save()
    return nomarchivo

def pendiente_recibir(exportar_a_csv_a = None):
    """
    Crea un informe los pedidos pendientes de recibir.
    """
    archivo = os.path.join(gettempdir(),
        'pendiente_recibir_%s' % give_me_the_name_baby())
    titulo = 'Pendiente de recibir'
    campos = [('Pedido', 9),
              ('Fecha', 9),
              ('Proveedor', 27),
              ('Producto', 25),
              ('Cantidad', 8),
              ('Precio/u', 8),
              ('Entrega', 14), ]
    LDPC = pclases.LineaDePedidoDeCompra
    lineas_de_compra = LDPC.select("""
        pedido_compra_id IN (SELECT id
                             FROM pedido_compra
                             WHERE cerrado = FALSE) """,
        orderBy="pedidoCompraID")
    datos = []
    for ldpc in lineas_de_compra:
        if ldpc.productoCompra and ldpc.productoCompra.obsoleto:
            continue
        pendiente = ldpc.cantidadPendiente
        if pendiente > 0:
            if ldpc.pedidoCompraID == None:     # Con la reescritura de la
            # consulta esto ya nunca se va a cumplir. Lo dejo por si acaso...
                print "geninformes.py (pendiente_recibir): ¡LDPC ID %s no ti"\
                      "ene pedido de compra! Eliminando..." % (ldpc.id),
                try:
                    ldpc.destroySelf()
                    print "OK"
                except Exception, msg:
                    print "KO: %s" % (msg)
                continue
            numpedido = ldpc.pedidoCompra.numpedido
            fechapedido = (ldpc.pedidoCompra.fecha
                and ldpc.pedidoCompra.fecha.strftime('%d/%m/%Y') or "-")
            proveedor = (ldpc.pedidoCompra.proveedor
                and ldpc.pedidoCompra.proveedor.nombre or "-")
            producto = ldpc.productoCompra.descripcion
            cantidad = utils.float2str(pendiente)
            precio = utils.float2str(ldpc.precio)
            datos.append((numpedido,
                          fechapedido,
                          proveedor,
                          producto,
                          cantidad,
                          precio,
                          "%s %s" % (utils.str_fecha(ldpc.fechaEntrega),
                                     ldpc.textoEntrega)))
    return imprimir2(archivo,
                     titulo,
                     campos,
                     datos,
                     fecha = mx.DateTime.localtime().strftime('%d/%m/%Y'),
                     cols_a_derecha = (4, 5),
                     exportar_a_csv_a = exportar_a_csv_a)

def pendiente_servir(tipo, porpedido, porproducto, nombrecliente = ""):
    """
    Crea un informe los pedidos pendientes de servir.
    tipo debe ser "geotextiles" o "fibra".
    Recibe los datos a mostrar por pedido y por producto.
    """
    assert tipo == "geotextiles" or tipo == "fibra" or tipo == "otros"

    archivo = os.path.join(gettempdir(),
        'pendiente_servir_%s_%s' % (tipo, give_me_the_name_baby()))
    titulo = 'Pdte. servir: %s%s' % (tipo,
        nombrecliente != "" and " - %s" % (nombrecliente) or "")
    campos = [('Pedido',         9),
              ('Fecha',          7),
              ('Cliente',       19),
              ('Producto',      19),
              ('Pendiente',      8),
              ('Stock total',    8),
              ('Fecha',          7),
              ('entrega',       12), 
              ('Forma de pago', 11) ]
    datos = []
    for fila in porpedido:
        datos.append(fila[:-1])
    datos.append(("", ) * 9)
    datos.append(("", ) * 9)
    datos.append(("", ) * 3 + ("POR PRODUCTO:", ) + ("", ) * 4)
    #datos.append(("", ) * 3 + ("-"*30, ) + ("", ) * 4)
    datos.append(("", ) * 3 + ("---", ) + ("", ) * 5)
    for fila in porproducto:
        datos.append(("",
                      "",
                      "",
                      fila[0],
                      fila[1],
                      fila[2],
                      fila[3],
                      ""))
    return imprimir2(archivo,
                     titulo,
                     campos,
                     datos,
                     fecha = mx.DateTime.localtime().strftime('%d/%m/%Y'),
                     cols_a_derecha = (4, 5), 
                     apaisado = True)

def consumo_fibra_produccion_gtx(datos, fecha = None):
    """
    titulo = 'Producción: consumo de materiales.'
    """
    archivo = os.path.join(gettempdir(),
        'consumo_fibra_produccion_gtx_%s' % give_me_the_name_baby())
    titulo = 'Consumo de fibra por partida de geotextiles.'
    campos = [('Partida de carga', 26),
              ('kg cons.', 14),
              ('kg prod.(real)', 14),
              ('kg prod.(teórico)', 14),
              ('balas cons.', 10),
              ('rollos prod.', 10),
              ('m² prod.', 12)]
    return imprimir2(archivo, titulo, campos, datos, fecha, (1, 2, 3, 4, 5, 6))

def consumo_produccion(datos, fecha = None):
    """
    Consulta de consumos de producción.
    """
    archivo = os.path.join(gettempdir(),
        'consulta_consumo_produccion_%s' % (give_me_the_name_baby()))
    titulo = 'Consumos'
    campos = [("", 25),
              ('Producto', 25),
              ('Cantidad consumida', 25),
              ("", 25),     # Es simplemente para hacer hueco
             ]
    _datos = []
    for dato in datos:
        _datos.append(("", dato[0], dato[1], ""))
    return imprimir2(archivo, titulo, campos, _datos, fecha, (2, ))

def listado_balas(datos, desc_producto, fecha = None):
    """
    Listado de balas de un producto concreto (listado_balas.py).
    """
    desc_producto_norm = "".join([i for i in desc_producto if i.isalpha()])
    archivo = os.path.join(gettempdir(),
        'listado_balas_%s_%s' % (desc_producto_norm, give_me_the_name_baby()))
    titulo = "Listado balas %s" % (desc_producto)
    campos = [('Código', 15),
              ('Fecha alta', 10),
              ('Peso', 10),
              ('Lote', 10),
              ('Albarán', 15),
              ('Partida', 10),
              ('En almacén', 10),
              ('Analizada', 10),
              ('Clase B', 10),
             ]
    return imprimir2(archivo, titulo, campos, datos, fecha,
                     (1, 2, 3, 4, 5, 6, 7, 8))

def listado_rollos(datos, desc_producto, fecha = None):
    """
    Listado de balas de un producto concreto (listado_balas.py).
    """
    desc_producto_norm = "".join([i for i in desc_producto if i.isalpha()])
    archivo = os.path.join(gettempdir(),
        'listado_rollos_%s_%s' % (desc_producto_norm, give_me_the_name_baby()))
    titulo = "Listado rollos %s" % (desc_producto)
    campos = [('Código', 20),
              ('Fecha alta', 15),
              ('Partida', 15),
              ('Albarán', 20),
              ('En almacén', 15),
              ('Metros lineales', 15)
             ]
    return imprimir2(archivo, titulo, campos, datos, fecha, (1, 2, 3, 4, 5))

def existencias_fibra_por_lote(fecha = None):
    """
    Imprime las existencias de fibra en almacén desglosadas por lote.
    """
    from formularios.ventana_progreso import VentanaProgreso
    vpro = VentanaProgreso()
    vpro.mostrar()
    balas = pclases.Bala.select("""
        bala.id IN (SELECT articulo.bala_id
                    FROM articulo
                    WHERE articulo.albaran_salida_id IS NULL
                        AND articulo.bala_id IS NOT NULL)
                        AND bala.partida_carga_id IS NULL """)
    bigbags = pclases.Bigbag.select("""
        bigbag.id IN (SELECT articulo.bigbag_id
                      FROM articulo
                      WHERE articulo.albaran_salida_id IS NULL
                      AND articulo.bigbag_id IS NOT NULL) """)
    i = 0.0
    tot = balas.count() + bigbags.count()
    productos = {}
    for bala in balas:
        vpro.set_valor(i/tot, 'Contando fibra por lote...')
        i += 1
        producto = bala.articulo.productoVenta
        if producto not in productos:
            productos[producto] = {'bultos': 0, 'kilos': 0.0, 'lotes': {},
                                   'bultosb': 0, 'kilosb': 0.0}
        lote = bala.lote
        if lote not in productos[producto]['lotes']:
            productos[producto]['lotes'][lote] = {'balas': 0, 'kilos': 0.0,
                                                  'balasb': 0, 'kilosb': 0.0}
        productos[producto]['lotes'][lote]['balas'] += 1
        productos[producto]['lotes'][lote]['kilos'] += bala.pesobala
        productos[producto]['bultos'] += 1
        productos[producto]['kilos'] += bala.pesobala
        if bala.claseb:
            productos[producto]['lotes'][lote]['balasb'] += 1
            productos[producto]['lotes'][lote]['kilosb'] += bala.pesobala
            productos[producto]['bultosb'] += 1
            productos[producto]['kilosb'] += bala.pesobala
    for bigbag in bigbags:
        vpro.set_valor(i/tot, 'Contando fibra de cemento por lote...')
        i += 1
        producto = bigbag.articulo.productoVenta
        if producto not in productos:
            productos[producto] = {'bultos': 0, 'kilos': 0, 'lotes': {},
                                   'bultosb': 0, 'kilosb': 0.0}
        loteCem = bigbag.loteCem
        if loteCem not in productos[producto]['lotes']:
            productos[producto]['lotes'][loteCem] = {'bigbags': 0,
                'kilos': 0.0, 'bigbagsb': 0, 'kilosb': 0.0}
        productos[producto]['lotes'][loteCem]['bigbags'] += 1
        productos[producto]['lotes'][loteCem]['kilos'] += bigbag.pesobigbag
        productos[producto]['bultos'] += 1
        productos[producto]['kilos'] += bigbag.pesobigbag
        if bigbag.claseb:
            productos[producto]['lotes'][loteCem]['bigbagsb'] += 1
            productos[producto]['lotes'][loteCem]['kilosb']+=bigbag.pesobigbag
            productos[producto]['bultosb'] += 1
            productos[producto]['kilosb'] += bigbag.pesobigbag
    def cmp_prod(p1, p2):
        if p1 == None:
            d1 = None
        else:
            d1 = p1.descripcion.upper()
        if p2 == None:
            d2 = None
        else:
            d2 = p2.descripcion.upper()
        if d1 < d2:
            return -1
        if d1 > d2:
            return 1
        return 0

    def cmp_lote(l1, l2):
        if l1.codigo < l2.codigo:
            return -1
        if l1.codigo > l2.codigo:
            return 1
        return 0

    productos_keys = productos.keys()
    productos_keys.sort(cmp_prod)
    datos = []
    tot = len(productos_keys)
    i = 0.0
    for producto in productos_keys:
        vpro.set_valor(i/tot, 'Analizando lotes...')
        i += 1
        if producto == None or producto.camposEspecificosBalaID == None:
            material = "?"
            dtex = "?"
            corte = "?"
            color = "?"
            antiuv = "?"
        else:
            material = (producto.camposEspecificosBala.tipoMaterialBala
               and producto.camposEspecificosBala.tipoMaterialBala.descripcion
               or "?")
            dtex = producto.camposEspecificosBala.dtex
            corte = producto.camposEspecificosBala.corte
            color = producto.camposEspecificosBala.color
            antiuv = producto.camposEspecificosBala.antiuv
        datos.append((producto and producto.descripcion
                        or "PRODUCTO DESCONOCIDO (?)",
            "",
            "Material: %s - Dtex: %s - Corte: %s - Color: %s - Antiuv: %s" % (
                material,
                dtex,
                corte,
                color,
                antiuv and "Sí" or "No"),
            "",
            ""
            ))
        lotes_keys = productos[producto]['lotes'].keys()
        lotes_keys.sort(cmp_lote)
        for lote in lotes_keys:
            if isinstance(lote, pclases.Lote):
                datos.append(("",
                  lote.codigo,
                   "Elong.: %s (%s) - Ten.: %s (%s) - Rizo: %s (%s) - Encog.:"\
                   " %s (%s)" % (
                        utils.float2str(lote.calcular_elongacion_media(),
                                        2, autodec = True),
                        lote.elongacion,
                        utils.float2str(lote.calcular_tenacidad_media(),
                                        2, autodec = True),
                        lote.tenacidad,
                        utils.float2str(lote.calcular_rizo_medio(),
                                        2, autodec = True),
                        lote.rizo,
                        utils.float2str(lote.calcular_encogimiento_medio(),
                                        2, autodec = True),
                        lote.encogimiento),
                  "%d balas (%d A + %d B)" % (
                    productos[producto]['lotes'][lote]['balas'],
                  (productos[producto]['lotes'][lote]['balas']
                    - productos[producto]['lotes'][lote]['balasb']),
                  productos[producto]['lotes'][lote]['balasb']),
                  "%s (%s A + %s B)" % (
                  utils.float2str(productos[producto]['lotes'][lote]['kilos']),
                  utils.float2str(productos[producto]['lotes'][lote]['kilos']
                    - productos[producto]['lotes'][lote]['kilosb']),
                  utils.float2str(productos[producto]['lotes'][lote]['kilosb'])
                  )))
            elif isinstance(lote, pclases.LoteCem):
                datos.append(("",
                 lote.codigo,
                 "",
                 "%d bigbags (%d A + %d B)" % (
                     productos[producto]['lotes'][lote]['bigbags'],
                 productos[producto]['lotes'][lote]['bigbags']
                     - productos[producto]['lotes'][lote]['bigbagsb'],
                 productos[producto]['lotes'][lote]['bigbagsb']),
                 "%s (%s A + %s B)" % (
                 utils.float2str(productos[producto]['lotes'][lote]['kilos']),
                 utils.float2str(productos[producto]['lotes'][lote]['kilos']
                     - productos[producto]['lotes'][lote]['kilosb']),
                 utils.float2str(productos[producto]['lotes'][lote]['kilosb']))
                 ))
        datos.append(("",
                      "",
                      " " * 20 + "Total producto: ",
                      "%d (%d A + %d B)" % (
                        productos[producto]['bultos'],
                        productos[producto]['bultos']
                            - productos[producto]['bultosb'],
                        productos[producto]['bultosb']),
                      "%s (%s A + %s B)" % (
                        utils.float2str(productos[producto]['kilos']),
                        utils.float2str(productos[producto]['kilos']
                            - productos[producto]['kilosb']),
                        utils.float2str(productos[producto]['kilosb']))
                     ))
        datos.append(("", "", "", "", ""))
    datos.append(("", "", "", "", ""))
    datos.append(("",
                  "",
                  " " * 30 + "TOTAL :",
                  "%d (%d A + %d B)" % (
                    sum([productos[producto]['bultos']
                         for producto in productos]),
                    sum([productos[producto]['bultos']
                         for producto in productos])
                      - sum([productos[producto]['bultosb']
                             for producto in productos]),
                    sum([productos[producto]['bultosb']
                         for producto in productos])),
                  "%s (%s A + %s B)" % (
                    utils.float2str(sum([productos[producto]['kilos']
                                         for producto in productos])),
                    utils.float2str(sum([productos[producto]['kilos']
                                         for producto in productos])
                                    - sum([productos[producto]['kilosb']
                                           for producto in productos])),
                    utils.float2str(sum([productos[producto]['kilosb']
                                         for producto in productos])))
                 ))
    archivo = os.path.join(gettempdir(),
        'existencias_fibra_por_lote_%s' % give_me_the_name_baby())
    titulo = 'Existencias de fibra en almacén por lote.'
    campos = [('Producto', 20),
              ('Lote', 5),
              ('Características', 40),
              ('Bultos', 15),
              ('kg en almacén', 20),
             ]
    vpro.ocultar()
    return imprimir2(archivo, titulo, campos, datos, fecha, (1, 3, 4, ))

def producido_produccion(datos, fecha = None, grafico = None):
    """
    titulo = 'Producción: Productos terminados.'
    """
    archivo = os.path.join(gettempdir(),
        'producido_produccion_%s' % give_me_the_name_baby())
    titulo = 'Producción: Productos terminados.'
    campos = [('Producto', 55), ('Cantidad', 25), ('Bultos', 20)]
    if grafico == None:
        graficos = []
    else:
        graficos = [grafico]
    return imprimir2(archivo, titulo, campos, datos, fecha, (1, 2, ),
                     graficos = graficos)

def etiquetasRollosEtiquetadora(rollos, mostrar_marcado, hook = None):
    """
    Crea etiquetas para los rollos de
    un parte de la línea de geotextil.
    Una por etiqueta del tamaño estándar de la impresora GEMINI: 12.55 x 8.4.
    «hook» es una función con la misma interfaz que esta para generar 
    etiquetas alternativas según la configuración del producto.
    """
    if hook:
        nomarchivo = hook(rollos, mostrar_marcado)
    else:   # Etiqueta de geotextiles por defecto
        # Voy a tratar de reescribir esto regla en mano a ver si consigo 
        # uadrarlo bien en la etiquetadora GEMINI.
        global linea, tm, lm, rm, bm
        x, y = lm, tm  # @UnusedVariable
        global linea
        MAXLINEAS = 40
        width = 12.55 * cm
        height = 8.4 * cm

        # Creo la hoja
        nomarchivo = os.path.join(gettempdir(),
            "etiqRollos_%s.pdf" % give_me_the_name_baby())
        c = canvas.Canvas(nomarchivo, pagesize = (width, height))

        for rollo in rollos:
            rectangulo(c, (0.3 * cm, 0.3 * cm),
                          (width - 0.3 * cm, height - 0.3 * cm))

            if mostrar_marcado and not rollo['defectuoso']:
                c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', 'CE.png'),
                            width/2 - (2 * cm / 2),
                            height - 0.3 * cm - 0.1 * cm - 1.64 * cm,
                            width = 2 * cm,
                            height = 1.64 * cm)
                c.setFont("Helvetica", 18)
                c.drawCentredString(width/2, height - 2.7 * cm ,
                                    "1035-CPD-ES033858")
            if rollo['defectuoso']:
                # DONE: If 'defectuoso' hay que quitar el marcado CE y poner 
                # las medidas reales y una marca especial en la etiqueta.
                # El rollo se puede obtener a partir del ID que viene en 
                # idrollo y vale != 0
                idrollo = rollo['idrollo']
                rollobd = rollo['objeto']
                if isinstance(rollobd, pclases.Rollo):
                    prollo = pclases.Rollo.get(idrollo)
                    campos = prollo.productoVenta.camposEspecificosRollo
                    producto = prollo.productoVenta
                    partida = (prollo.partida and prollo.partida.codigo
                               or "¡SIN PARTIDA!")
                    largo = 1000 * prollo.peso / prollo.densidad / campos.ancho
                        # 1000 * gr / gr/m² / m = m
                    rollo['descripcion'] = producto.nombre
                    rollo['densidad'] = utils.float2str(prollo.densidad)
                    rollo['ancho'] = "%s m" % (campos.ancho) # Ancho se supone
                    # fijo. Los rollos no tienen campo ancho. Es el del 
                    # producto.
                    rollo['peso'] = "%s kg" % (utils.float2str(prollo.peso)) 
                                    # Peso total. No teórico sin embalaje como 
                                    # en las etiquetas originales.
                    rollo['m2'] = "%s m²" % (utils.float2str(campos.ancho 
                                                             * largo))
                    rollo['mlin'] = "%s m" % (utils.float2str(largo))
                    rollo['nrollo'] = str(prollo.numrollo)
                    rollo['partida'] = partida
                    rollo['codigo'] = producto.codigo
                    rollo['codigo39'] = prollo.codigo
                elif isinstance(rollobd, pclases.RolloDefectuoso):
                    prollo = pclases.RolloDefectuoso.get(idrollo)
                        # Ahora (08/03/07) viene en el diccionario. Es tontería
                        # volver a buscar en la BD. De todas formas lo hago. :P
                else:
                    txterr = "geninformes::etiquetasRollosEtiquetadora"\
                             " -> Si 'defectuoso' es True, el rollo DE"\
                             "BE existir y ser del tipo plcases.Rollo "\
                             "o pclases.RolloDefectuoso."
                    raise TypeError, txterr 
                c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', 'none.png'),
                            width/2 - (1 * cm / 2),
                            height - 0.6 * cm - 0.2 * cm - 0.82 * cm,
                            width = 1 * cm,
                            height = 0.82 * cm)
                # CWT: No debe aparecer el motivo en la etiqueta. Pensaba que 
                # así se identificarían mejor, pero no. No debe aparecer nada 
                # que indique que el rollo es malo salvo el logotipo de la 
                # "bolaspa".
                # c.setFont("Helvetica", 14)
                # el_encogedor_de_fuentes_de_doraemon(
                #   c, "Helvetica", 14, 0.2 * cm,
                #   width - 0.2*cm, height - 2.5 * cm, prollo.observaciones,
                #   alineacion = 0)

            c.setFont("Helvetica-Bold", 24)
            c.drawCentredString(width/2, height - 3.6 * cm,
                                escribe(rollo['descripcion']))
            c.setFont("Helvetica", 20)
            c.drawCentredString(width/2, height - 4.15 * cm,
                                escribe("%s gr/m²" % (rollo['densidad'])))
            c.setFont("Helvetica", 14)
            c.drawString(0.5 * cm, height - 4.4 * cm,
                         escribe("Ancho: %s" % (rollo['ancho'])))
            c.drawString(0.5 * cm, height - 6.2 * cm,
                         escribe("M²: %s" % (rollo['m2'])))
            c.drawString(0.5 * cm, height - 5.0 * cm,
                         escribe("Peso: %s" % (rollo['peso'])))
            c.drawString(4.0 * cm, height - 6.2 * cm,
                         escribe("M.lin: %s" % (rollo['mlin'])))
            c.drawString(0.5 * cm, height - 5.6 * cm,
                         escribe("Partida: %s" % (rollo['partida'])))
            c.setFont("Helvetica-Bold", 22)
            #c.drawString(0.6 * cm, 1 * cm,
            # escribe("Nº rollo: %s" % (rollo['nrollo'])))
            c.drawString(4.0 * cm, height - 5.0 * cm,
                         escribe("Nº rollo: %s" % (rollo['nrollo'])))
            if rollo['defectuoso']:
                _dibujare_simbolitor_en_la_etiquetar(
                    c, 9.5*cm, 0.25*cm, 2.6*cm)
            else:
                from barcode.EANBarCode import EanBarCode
                bar = EanBarCode()
                #c.drawImage(bar.getImage(rollo['codigo']), 8.0 * cm, 0.5 * cm,
                #            width = 4.1 * cm)
                nombreficheroean13 = bar.getImage(rollo['codigo'], height = 50)
                ean13rotado = Image.open(nombreficheroean13)
                ean13rotado = ean13rotado.rotate(90)
                ean13rotado.save(nombreficheroean13)
                c.drawImage(
                    nombreficheroean13, 10.5*cm, 0.5*cm, width = 1.5*cm)
            from barcode import code39
            codigobarras = code39.Extended39(rollo['codigo39'], 
                                             xdim = 0.065 * cm)
            #codigobarras.drawOn(c, 3.5 * cm, 2.9 * cm)
            codigobarras.drawOn(c, 0.6 * cm, 0.9 * cm)
            c.setFont("Helvetica", 8)
            #c.drawString(6.8 * cm, 2.6 * cm, escribe(rollo['codigo39']))
            c.drawString((0.6 - 3.5 + 6.8) * cm, (0.9 - 2.9 + 2.6) * cm,
                         escribe(rollo['codigo39']))

            # XXX
            # c.setPageRotation(-90)
            # c.rotate(-90)
            # XXX

            c.showPage()
        c.save()
    return nomarchivo

def _dibujare_simbolitor_en_la_etiquetar(c, x, y, ancho):
    """
    Dibuja un símbolo de prohibido en la esquina (x,y) con el ancho "ancho",
    donde se supone que debería ir el EAN-13 de la etiqueta a la que
    corresponde el canvas "c".
    """
    from reportlab.graphics.shapes import Drawing, Line
    from reportlab.graphics.widgets import signsandsymbols
    from reportlab.graphics import renderPDF
    from reportlab.lib.colors import black, Color, red  # @UnusedImport

    d = Drawing(ancho, ancho)
    signoprohibido = signsandsymbols.NotAllowed()
    signoprohibido.x, signoprohibido.y = 0, 0   # Posición _dentro_ del
                                                # «drawing».
    signoprohibido.size = ancho
    barras = Line(10, 37, ancho-10, 37, strokeColor = black,
                  strokeWidth = ancho / 3,
                  strokeDashArray = [1, 3, 1, 2, 1, 1])
    diagonal = Line(11, 18, ancho - 11, ancho - 18, strokeColor = red,
                    strokeWidth = 8)
    d.add(signoprohibido)
    d.add(barras)
    d.add(diagonal)
    renderPDF.draw(d, c, x, y, showBoundary = False)

# XXX ------- CARTAS DE PAGOS CON PAGARÉS Y CHEQUES --------------------vvv---

def calcular_medidas(cheque):
    """
    Si «cheque» es True devuelve las medidas para un cheque, si no, las
    devuelve para un pagaré.
    """
    lm = 1.5*cm     # Margen izquierdo
    medidas = {'proveedor': [11.2*cm, 25.5*cm - 1*cm],
               'fecha': [13.3*cm, 19.8*cm],
               'facturas': [lm, 17*cm - 1*cm],
               'observaciones': [lm, 9.25*cm + 1*cm]
              }
    if cheque:
        medidas['importe'] = [15*cm, 5.7*cm]
        medidas['paguese'] = [8.2*cm, 5.2*cm]
        medidas['euros1'] = [6.4*cm, 4.7*cm]
        medidas['euros2'] = [4.4*cm, 4.2*cm]
        medidas['fecha_emision'] = [8.8*cm, 3.7*cm]
    else:
        medidas['importe'] = [15*cm, 5.7*cm]
        medidas['paguese'] = [4.8*cm, 4.5*cm]
        medidas['euros1'] = [6.4*cm, 4.0*cm]
        medidas['euros2'] = [4.4*cm, 3.5*cm]
        medidas['fecha_emision'] = [8.8*cm, 3.0*cm]
        medidas['fecha_vencimiento'] = [6.4*cm, 5.7*cm]
    # Corrección sobre las medidas originales. Depende de dónde se imprima.
    # Hay que jugar con estos parámetros y el autocentrado del
    # visor PDF para ajustar del todo los textos. En Foxit Reader lo ideal es
    # tamaño 100% y no autocentrado ni autoajuste.
    for key in medidas:
        incx, incy = (0.6 * cm, -0.0 * cm)
        medidas[key][0] += incx
        medidas[key][1] += incy
    medidas['tope_ventana_sobre'] = [19.1*cm, 21.7*cm]  # Esquina inferior
                                            # derecha de la ventana del sobre.
    # Las medidas del texto fijo (logos, texto, etc.)
    L = -0.75*cm     # Alto de una línea
    l = L * 10   # Línea "contador"
    tm, bm, lm, rm = (29*cm, 1.0*cm, 1.5*cm, 20*cm) # "Top", "bottom",
                                                    # "left" y "right margin"
    lm2 = 3.5*cm
    lm3 = lm + (2+13 / 2.0)*cm
    lm4 = lm + 15*cm
    medidas['logo0_cabecera'] =     [lm,        tm - 3.7*cm, 4*cm, 3.6*cm]
                                    # x, y, ancho y alto
    medidas['logo1_cabecera'] =     [rm - 4*cm, tm - 2*cm, 119, 65]
                                    # x, y, ancho y alto
    medidas['ciudad'] =             [lm3 - 0.7*cm, 20.0 * cm]; l += 4*L
    medidas['entradilla'] =         [lm,        tm + l]; l += 1*L
    medidas['texto'] =              [lm,        tm + l]; l += 1*L
    medidas['cabecera_desglose0'] = [lm2,        tm + l]
    medidas['cabecera_desglose1'] = [lm3,       tm + l]
    medidas['cabecera_desglose2'] = [lm4,       tm + l]
    #medidas['despedida'] =          [lm,        11 * cm]
    #medidas['firma'] =              [lm3,       10 * cm]
        # 10 cm es el borde superior del cheque/pagaré.
    medidas['despedida'] =          [lm,        10 * cm]
    medidas['firma'] =              [lm3,       9 * cm]
        # 10 cm es el borde superior del cheque/pagaré.

    return medidas

def _escribir_textofijo(c, medidas):
    """
    Escribe en el canvas "c" el texto fijo que debería
    traer el folio de imprenta, que son los dos logos de
    la empresa y un poco de texto estándar. Las posiciones
    del folio vienen determinadas por el diccionario "medidas".
    """
    try:
        datos_empresa = pclases.DatosDeLaEmpresa.select()[0]
    except IndexError:
        print "geninformes::_escribir_textofijo -> No se encontraron los "\
              "datos de la empresa en la tabla datos_de_la_empresa."
    else:
        c.saveState()
        # Voy a imprimir 2 pequeñas marcas para saber por dónde doblar el
        # folio y que entre en el sobrei.
        c.line(1*cm, A4[1]/3, 1.2*cm, A4[1]/3)
        c.line(1*cm, (A4[1]*2/3), 1.2*cm, (A4[1]*2/3))
        # Y ahora los logos y el texto fijo de verdad.
        c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', datos_empresa.logo),
                    medidas['logo0_cabecera'][0],
                    medidas['logo0_cabecera'][1],
                    medidas['logo0_cabecera'][2],
                    medidas['logo0_cabecera'][3])
        if datos_empresa.bvqi:
            c.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..','imagenes',datos_empresa.logoiso1),
                        medidas['logo1_cabecera'][0],
                        medidas['logo1_cabecera'][1],
                        medidas['logo1_cabecera'][2],
                        medidas['logo1_cabecera'][3])
            c.setFont("Helvetica", 6)
            c.drawCentredString(medidas['logo1_cabecera'][0]
                                    + medidas['logo1_cabecera'][2]/2.0,
                                medidas['logo1_cabecera'][1] + 0.02*cm,
                                escribe('Geotextiles CE 1035-CPD-ES033858'))
            c.drawCentredString(medidas['logo1_cabecera'][0]
                                    + medidas['logo1_cabecera'][2]/2.0,
                                medidas['logo1_cabecera'][1] - 0.2*cm,
                                escribe('Fibra CE 1035-CPD-9003712'))
        c.setFont("Times-Roman", 14)
        c.drawString(medidas['ciudad'][0], medidas['ciudad'][1],
                     escribe("%s," % (datos_empresa.ciudad)))
        c.drawString(medidas['entradilla'][0], medidas['entradilla'][1],
                     escribe("Muy Srs. míos."))
        c.drawString(medidas['texto'][0], medidas['texto'][1],
                     escribe("Adjunto les remito nuestro talón o pagaré "\
                             "correspondiente a su/s factura/s:"))
        c.drawString(medidas['cabecera_desglose0'][0],
                     medidas['cabecera_desglose0'][1],
                     escribe("FECHA FACTURA"))
        c.drawCentredString(medidas['cabecera_desglose1'][0],
                            medidas['cabecera_desglose1'][1],
                            escribe("Nº FACTURA"))
        c.drawRightString(medidas['cabecera_desglose2'][0],
                          medidas['cabecera_desglose2'][1], escribe("IMPORTE"))
        c.drawString(medidas['despedida'][0], medidas['despedida'][1],
                     escribe("Sin otro particular le saluda muy atentamente."))
        c.drawString(medidas['firma'][0], medidas['firma'][1],
                     escribe("Dpto. administración."))
        c.restoreState()


def carta_pago(pagare, cheque = True, textofijo = True):
    """
    Recibe un pagaré de pclases y genera un PDF con el texto debidamente
    formateado.
    Si «cheque» == True imprime un cheque al pie del documento.
    Si es False imprime un pagaré.
    Si "textofijo" es True, imprimo el texto que no cambia en las cartas de
    pago. Si es False se supone que los folios vienen de la imprenta con
    ese texto ya escrito y lo omito.
    """
    ## Tamaños que usaré
    una_linea = -16
    medidas = calcular_medidas(cheque)

    ## Preparo el archivo y el canvas
    nomarchivo = os.path.join(gettempdir(),
                              "cartapago_%s.pdf" % (give_me_the_name_baby()))
    c = canvas.Canvas(nomarchivo)
    fuente, tamanno = "Helvetica", 12
    c.setFont(fuente, tamanno)
    c.setPageSize(A4)

    ## Escribo los textos fijos si se me indica:
    if textofijo:
        _escribir_textofijo(c, medidas)

    ## Preparo los datos a imprimir...
    fecha_corta = corregir_nombres_fecha(
                    pagare.fechaEmision.strftime("%d de %B de %Y"))
    #fecha_larga = corregir_nombres_fecha(
    #   pagare.fechaEmision.strftime("%A, %d de %B de %Y"))  # CWT: No quiere
                                                        # el nombre del
    fecha_larga = corregir_nombres_fecha(
        pagare.fechaEmision.strftime("%d de %B de %Y")) # día en la fecha.
                                                        # Qué se le va a hacer.
    fecha_vencimiento = corregir_nombres_fecha(
        pagare.fechaPago.strftime("%d de %B de %Y"))
    euros1, euros2 = get_lineas_euros(pagare.cantidad)
    nombre_proveedor, direccion_proveedor = get_lineas_proveedor(pagare)

    ## ... y los escribo
    xpro, ypro = medidas['proveedor']
    for linea in direccion_proveedor.split("\n"):
        # Opción A: Partir las líneas.
        saltos = agregarFila(xpro, ypro, medidas['tope_ventana_sobre'][0],
                             escribe(linea), c, fuente, tamanno,
                             a_derecha = False, altura_linea = -una_linea)
        ypro += una_linea * saltos
        # Opción B: Encoger la línea hasta que quepa.
        #el_encogedor_de_fuentes_de_doraemon(c, fuente, tamanno, xpro,
        #   medidas['tope_ventana_sobre'][0], ypro, linea)
        #ypro += una_linea
    c.drawString(medidas['fecha'][0], medidas['fecha'][1],
                 escribe(fecha_corta))
    xpago, ypago = medidas['facturas']
    for pago in pagare.pagos:
        #fecha_pago = utils.str_fecha(pago.fecha)
        fecha_factura = (pago.facturaCompra
                         and utils.str_fecha(pago.facturaCompra.fecha)
                         or utils.str_fecha(pago.fecha))
        importe_pago = "%s €" % (utils.float2str(pago.importe))
        if pago.facturaCompra != None:
            numfactura_pago = pago.facturaCompra.numfactura
        else:
            numfactura_pago = pago.observaciones
        c.drawString(xpago + 2*cm, ypago, escribe(fecha_factura))
        c.drawCentredString(xpago + (2+13/2.0)*cm, ypago,
                            escribe(numfactura_pago))
        c.drawRightString(xpago + 15*cm, ypago, escribe(importe_pago))
        ypago += una_linea
    if len(pagare.pagos) > 1:
        c.drawString(xpago + 9*cm, ypago, escribe("TOTAL PAGO: "))
        c.drawRightString(xpago + 15*cm, ypago,
                          escribe("%s €" % utils.float2str(
                            sum([p.importe for p in pagare.pagos]))))
        ypago += una_linea
    ypago += una_linea  # Para dejar un poco de espacio debajo
                        # del listado de pagos.
    if pagare.observaciones.strip() != "":
        agregarFila(xpago, ypago, 20.1*cm,
                    escribe("Observaciones: %s" % (pagare.observaciones)),
                    c, fuente, tamanno - 2, a_derecha = True,
                    altura_linea = -una_linea)
    tamanno = 10
    c.setFont(fuente, tamanno)
    c.drawString(medidas['importe'][0], medidas['importe'][1],
                 escribe("# %s #" % (utils.float2str(pagare.cantidad))))
    c.drawString(medidas['paguese'][0], medidas['paguese'][1],
                 escribe(nombre_proveedor))
    # Escribo las líneas de euros...
    c.drawString(medidas['euros1'][0], medidas['euros1'][1], escribe(euros1))
    c.drawString(medidas['euros2'][0], medidas['euros2'][1], escribe(euros2))
    # Y sendas rayas desde que acaban hasta el fin de línea.
    c.line(medidas['euros1'][0] + c.stringWidth(euros1, fuente, tamanno),
           medidas['euros1'][1] + 4, rm, medidas['euros1'][1] + 4)
    c.line(medidas['euros2'][0] + c.stringWidth(euros2, fuente, tamanno),
           medidas['euros2'][1] + 4, rm, medidas['euros2'][1] + 4)
    # Y sigo con el resto de datos:
    c.drawString(medidas['fecha_emision'][0], medidas['fecha_emision'][1],
                 escribe(fecha_larga))
    if not cheque:
        c.drawString(medidas['fecha_vencimiento'][0],
                     medidas['fecha_vencimiento'][1],
                     escribe(fecha_vencimiento))

    ## Por último guardo y devuelvo el nombre del PDF generado (no hace falta
    ## showPage, «save» lo hace por mí antes de escribir el PDF).
    c.save()
    return nomarchivo

def get_lineas_proveedor(pagare):
    """
    Devuelve la dirección completa del proveedor del pagaré dividida en líneas.
    """
    res = "ERROR PROVEEDOR", "ERROR PROVEEDOR"
    if pagare.pagos != []:
        pro = pagare.pagos[0].proveedor
        res = pro.nombre, "\n".join((
            pro.nombre,
            pro.direccion,
            " ".join((pro.cp,
                      pro.ciudad,
                      pro.provincia != pro.ciudad
                        and pro.provincia
                        and pro.provincia.split() != ""
                        and " (%s)" % (pro.provincia)
                        or "", pro.pais))))
    return res

def get_lineas_euros(cantidad, n = 80, mayusculas = False):
    """
    Devuelve la cantidad recibida en letras, dividido en
    dos líneas si el número de caracteres de la misma es
    superior a "n".
    """
    from formularios.numerals import numerals
    euros = numerals(cantidad, moneda = "euros", fraccion = "céntimos",
                     autoomitir = True)
    if mayusculas:
        euros = euros.upper()
    euros2 = ''
    if len(euros) > n:
        indice = n
        while euros[indice] != ' ':
            indice -= 1
        euros2 = euros[indice:]
        euros = euros[:indice]
    return euros, euros2

# XXX ------- CARTAS DE PAGOS CON PAGARÉS Y CHEQUES --------------------^^^---

def calcular_medidas_fax():
    """
    Devuelve las medidas de los campos de la hoja de fax.
    """
    L = -0.75*cm     # Alto de una línea
    l = L * 4   # Línea "contador"
    tm, bm, lm, rm = (29*cm, 1.0*cm, 1.5*cm, 20*cm) # "Top", "bottom",
                                                    # "left" y "right margin"
    lm2 = lm + 3*cm    # 2º Margen izquierdo (columna de textos variables)
    lm3 = lm2 + 4*cm    # 3º Margen izquierdo (columna de textos variables
                        # para cuentas y firmas)
    lm4 = lm3 + 6*cm
    lm5 = lm4 + 3*cm
    medidas = {}
    medidas['logo0_cabecera'] = \
        [lm,            tm - 2.3*cm, 2.5*cm, 2.2*cm]      # x, y, ancho y alto
    # medidas['logo1_cabecera'] = \
    #   [rm - 4*cm,     tm - 2*cm, 2.54*cm, 1.651*cm]      # x, y, ancho y alto
    medidas['logo1_cabecera'] =         [rm - 4*cm,     tm - 2*cm, 99, 54]
        # x, y, ancho y alto
    medidas['empresa_cabecera'] =       [lm,            tm + l]; l += 0.75*L
    medidas['direccion0_cabecera'] =    [lm,            tm + l]; l += 0.75*L
    medidas['direccion1_cabecera'] =    [lm,            tm + l]; l += 0.75*L
    medidas['telefono_cabecera'] =      [lm,            tm + l]; l += 0.75*L
    medidas['fax_cabecera'] =           [lm,            tm + l]; l += 0.75*L
    medidas['mail_cabecera'] =          [lm,            tm + l]; l += 2*L

    medidas['titulo_fax'] =             [(lm + rm)/2.0, tm + l]; l += 2*L
    medidas['empresa0'] =               [lm,            tm + l]
    medidas['empresa1'] =               [lm2,           tm + l]; l += L
    medidas['contacto0'] =              [lm,            tm + l]
    medidas['contacto1'] =              [lm2,           tm + l]; l += L
    medidas['fax0'] =                   [lm,            tm + l]
    medidas['fax1'] =                   [lm2,           tm + l]
    medidas['telefono0'] =              [lm4,           tm + l]
    medidas['telefono1'] =              [lm5,           tm + l]; l += L
    medidas['de0'] =                    [lm,            tm + l]
    medidas['de1'] =                    [lm2,           tm + l]; l += L
    medidas['asunto0'] =                [lm,            tm + l]
    medidas['asunto1'] =                [lm2,           tm + l]; l += L
    medidas['fecha0'] =                 [lm4,           tm + l]
    medidas['fecha1'] =                 [lm5,           tm + l]; l += L
    medidas['paginas'] =                [lm,            tm + l]; l += 2*L
    medidas['comentario'] =             [lm,            tm + l]; l += L
    medidas['texto'] =                  [lm,            tm + l]; l += L
    medidas['beneficiario0'] =          [lm,            tm + l]
    medidas['beneficiario1'] =          [lm3,           tm + l]; l += L
    medidas['cuentaben0'] =             [lm,            tm + l]
    medidas['cuentaben1'] =             [lm3,           tm + l]; l += L
    medidas['cuentaben2'] =             [lm3,           tm + l]; l += L
    medidas['observaciones0'] =         [lm,            tm + l]
    medidas['observaciones1'] =         [lm3,           tm + l]; l += L
    medidas['porcuenta0'] =             [lm,            tm + l]
    medidas['porcuenta1'] =             [lm3,           tm + l]; l += L
    medidas['cuentaord0'] =             [lm,            tm + l]
    medidas['cuentaord1'] =             [lm3,           tm + l]; l += L
    medidas['concepto0'] =              [lm,            tm + l]
    medidas['concepto1'] =              [lm2,           tm + l]; l += L
    medidas['importe0'] =               [lm,            tm + l]
    medidas['importe1'] =               [lm2,           tm + l]; l += L
    medidas['saludo'] =                 [lm,            tm + l]; l += 3*L
    medidas['firma0'] =                 [lm2,           tm + l]
    medidas['firma1'] =                 [lm3,           tm + l]

    medidas['pie0'] =                   [(lm + rm)/2.0, bm - 1.0*L]
    medidas['pie1'] =                   [(lm + rm)/2.0, bm - 0.5*L]
    return medidas

def fax_transferencia(empresa,      # Banco a través del que se hace la
                                    # transferencia.
                      contacto,     # Contacto en el banco
                      fax,          # Fax del banco
                      telefono,     # Teléfono del banco
                      de,           # Nombre del remitente del fax (no procede
                                    # de la BD)
                      asunto,       # Asunto del fax. Generalmente
                                    # "TRANSFERENCIA" (no procede de la BD)
                      fecha,        # Fecha de orden de la transferencia
                      beneficiario, # Nombre del proveedor de la cuenta destino
                      banco,        # Banco de la cuenta destino
                      cuenta,       # Cuenta destino (completa, con IBAN y
                                    # demás si fuese necesario/extranjero)
                      porcuenta,    # Nombre de la "propia_empresa".
                      ccc,          # Cuenta de la cuenta origen.
                      concepto,     # Número de factura de la transferencia
                                    # (atributo concepto de Transferencia)
                      importe,      # Importe en euros.
                      firmado,      # Nombre para firma del fax
                      swift = "",   # SWIFT. En blanco si no es necesario
                                    # imprimirlo (no es cuenta extranjera)
                      iban = "",    # IBAN. En blanco si no es necesario
                                    # imprimirlo (no es cuenta extranjera)
                      observaciones = "",   # Observaciones. Se imprimirán
                                            # debajo de la cuenta beneficiaria.
                                            # En blanco si no es necesario
                                            # imprimirlo.
                      conceptoLibre = ""):
    """
    Recibe los datos a imprimir en el fax *como cadenas*.
    """
    ## Tamaños que usaré
    una_linea = -16  # @UnusedVariable
    medidas = calcular_medidas_fax()

    ## Preparo el archivo y el canvas
    nomarchivo = os.path.join(gettempdir(),
        "fax_transferencia_%s.pdf" % (give_me_the_name_baby()))
    c = canvas.Canvas(nomarchivo)
    c.setPageSize(A4)

    ## Fuentes
    fuentes = {'normal': {'fuente': "Helvetica", 'tamaño': 12},
               'negrita': {'fuente': "Helvetica-Bold", 'tamaño': 12},
               'grande': {'fuente': "Times-Roman", 'tamaño': 48},
               'cabecera': {'fuente': "Times-Italic", 'tamaño': 10},
               'cabecera_negrita': {'fuente': "Times-Bold", 'tamaño': 12},
               'pie': {'fuente': "Times-Roman", 'tamaño': 8},
               'pequeña': {'fuente': "Helvetica", 'tamaño': 10}}
    c.setFont(fuentes['negrita']['fuente'], fuentes['negrita']['tamaño'])
    escribir_cabecera(c, medidas, fuentes)
    escribir_pie(c, medidas, fuentes)
    # Hasta aquí tenemos una plantilla más o menos estándar con cabecera y
    # pie de página.
    escribir_cuerpo_fax(c, medidas, fuentes, empresa, contacto, fax, telefono,
                        de, asunto, fecha, beneficiario, banco, cuenta,
                        porcuenta, ccc, concepto, importe, firmado,
                           swift, iban, observaciones, conceptoLibre)
    ## Por último guardo y devuelvo el nombre del PDF generado (no hace falta
    ## «showPage», el «save» lo hace por mí antes de escribir el PDF).
    c.save()
    return nomarchivo

def escribir_cuerpo_fax(canvas, medidas, fuentes, empresa, contacto, fax,
                        telefono, de, asunto, fecha, beneficiario, banco,
                        cuenta, porcuenta, ccc, concepto, importe, firmado,
                        swift, iban, observaciones, conceptoLibre):
    """
    Cuerpo del fax.
    """
    canvas.setFont(fuentes['grande']['fuente'], fuentes['grande']['tamaño'])
    canvas.drawCentredString(medidas['titulo_fax'][0],
                             medidas['titulo_fax'][1], escribe("FAX"))

    canvas.setFont(fuentes['negrita']['fuente'], fuentes['negrita']['tamaño'])
    canvas.drawString(medidas['empresa0'][0], medidas['empresa0'][1],
                      escribe("Empresa: "))
    canvas.drawString(medidas['contacto0'][0], medidas['contacto0'][1],
                      escribe("A/A: "))
    canvas.drawString(medidas['fax0'][0], medidas['fax0'][1],
                      escribe("Nº fax: "))
    canvas.drawString(medidas['telefono0'][0], medidas['telefono0'][1],
                      escribe("Tlf: "))
    canvas.drawString(medidas['de0'][0], medidas['de0'][1], escribe("De: "))
    canvas.drawString(medidas['asunto0'][0], medidas['asunto0'][1],
                      escribe("Asunto: "))
    canvas.drawString(medidas['fecha0'][0], medidas['fecha0'][1],
                      escribe("Fecha: "))
    canvas.drawString(medidas['paginas'][0], medidas['paginas'][1],
                      escribe("Nº de páginas incluida esta: 1"))
    canvas.drawString(medidas['comentario'][0], medidas['comentario'][1],
                      escribe("Comentario: "))
    canvas.drawString(medidas['beneficiario0'][0],
                      medidas['beneficiario0'][1], escribe("BENEFICIARIO: "))
    canvas.drawString(medidas['cuentaben0'][0], medidas['cuentaben0'][1],
                      escribe("CUENTA BENEFICIARIA: "))
    if observaciones != "":
        canvas.drawString(medidas['observaciones0'][0],
                          medidas['observaciones0'][1],
                          escribe("OBSERVACIONES: "))
    canvas.drawString(medidas['porcuenta0'][0], medidas['porcuenta0'][1],
                      escribe("POR CUENTA DE: "))
    canvas.drawString(medidas['cuentaord0'][0], medidas['cuentaord0'][1],
                      escribe("Nº DE CUENTA ORDENANTE: "))
    canvas.drawString(medidas['concepto0'][0], medidas['concepto0'][1],
                      escribe("CONCEPTO: "))
    canvas.drawString(medidas['importe0'][0], medidas['importe0'][1],
                      escribe("IMPORTE: "))
    canvas.drawString(medidas['firma0'][0], medidas['firma0'][1],
                      escribe("Fdo: "))

    canvas.setFont(fuentes['normal']['fuente'], fuentes['normal']['tamaño'])
    canvas.drawString(medidas['saludo'][0], medidas['saludo'][1],
                      escribe("Un saludo."))
    canvas.drawString(medidas['texto'][0], medidas['texto'][1],
        escribe("Por la presente ruego realice la siguiente transferencia:"))
    canvas.drawString(medidas['empresa1'][0], medidas['empresa1'][1],
                      escribe(empresa))
    canvas.drawString(medidas['contacto1'][0], medidas['contacto1'][1],
                      escribe(contacto))
    canvas.drawString(medidas['fax1'][0], medidas['fax1'][1], escribe(fax))
    canvas.drawString(medidas['telefono1'][0], medidas['telefono1'][1],
                      escribe(telefono))
    canvas.drawString(medidas['de1'][0], medidas['de1'][1], escribe(de))
    canvas.drawString(medidas['asunto1'][0], medidas['asunto1'][1],
                      escribe(asunto))
    canvas.drawString(medidas['fecha1'][0], medidas['fecha1'][1],
                      escribe(fecha))
    canvas.drawString(medidas['beneficiario1'][0],
                      medidas['beneficiario1'][1], escribe(beneficiario))
    #canvas.drawString(medidas['cuentaben1'][0], medidas['cuentaben1'][1],
    #                  escribe(banco))
    canvas.drawString(medidas['cuentaben1'][0], medidas['cuentaben1'][1],
                      escribe(cuenta))
    #canvas.drawString(medidas['cuentaben2'][0], medidas['cuentaben2'][1],
    #                  escribe(cuenta))
    swift_iban = ""
    if swift != "":
        swift_iban += "SWIFT: %s " % (swift)
    if iban != "":
        swift_iban += "IBAN: %s" % (iban)
    canvas.saveState()
    canvas.setFont(fuentes['pequeña']['fuente'], fuentes['pequeña']['tamaño'])
    canvas.drawString(medidas['cuentaben2'][0], medidas['cuentaben2'][1],
                      escribe(swift_iban))
    canvas.restoreState()
    if observaciones != "":
        canvas.saveState()
        canvas.setFont(fuentes['pequeña']['fuente'],
                       fuentes['pequeña']['tamaño'])
        canvas.drawString(medidas['observaciones1'][0],
                          medidas['observaciones1'][1], escribe(observaciones))
        canvas.restoreState()
    canvas.drawString(medidas['porcuenta1'][0], medidas['porcuenta1'][1],
                      escribe(porcuenta))
    canvas.drawString(medidas['cuentaord1'][0], medidas['cuentaord1'][1],
                      escribe(ccc))
    canvas.drawString(medidas['concepto1'][0], medidas['concepto1'][1],
                      escribe(". ".join((concepto, conceptoLibre))))
    canvas.drawString(medidas['importe1'][0], medidas['importe1'][1],
                      escribe(importe))
    canvas.drawString(medidas['firma1'][0], medidas['firma1'][1],
                      escribe(firmado))

def escribir_pie(canvas, medidas, fuentes):
    """
    Pie del fax (dirección).
    """
    datos_empresa = pclases.DatosDeLaEmpresa.select()[0]
    canvas.setFont(fuentes['pie']['fuente'], fuentes['pie']['tamaño'])
    if datos_empresa.direccion != datos_empresa.dirfacturacion:
        dirtitle = " de oficinas y correspondencia"
    else:
        dirtitle = ""
    canvas.drawCentredString(medidas['pie0'][0], medidas['pie0'][1],
        escribe('Dirección%s: %s. %s - %s (%s)' % (dirtitle,
                                                   datos_empresa.direccion,
                                                   datos_empresa.cp,
                                                   datos_empresa.ciudad,
                                                   datos_empresa.provincia)))
    if ("CIF" in datos_empresa.cif.upper()
        or "C.I.F" in datos_empresa.cif.upper()):
        ciftitle = ""
    else:
        ciftitle = "C.I.F.: "
    canvas.drawCentredString(medidas['pie1'][0], medidas['pie1'][1],
                             escribe('%s%s' % (ciftitle, datos_empresa.cif)))

def escribir_cabecera(canvas, medidas, fuentes):
    """
    Escribe la cabecera del fax.
    """
    datos_empresa = pclases.DatosDeLaEmpresa.select()[0]
    canvas.drawImage(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', datos_empresa.logo),
                     medidas['logo0_cabecera'][0],
                     medidas['logo0_cabecera'][1],
                     medidas['logo0_cabecera'][2],
                     medidas['logo0_cabecera'][3])
    if datos_empresa.bvqi:
        canvas.drawImage(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'imagenes', datos_empresa.logoiso1),
            medidas['logo1_cabecera'][0],
            medidas['logo1_cabecera'][1],
            medidas['logo1_cabecera'][2],
            medidas['logo1_cabecera'][3])
        canvas.setFont("Helvetica", 6)
        canvas.drawCentredString(medidas['logo1_cabecera'][0]
                                    + medidas['logo1_cabecera'][2]/2.0,
                                 medidas['logo1_cabecera'][1] + 0.02*cm,
                                 escribe('Geotextiles CE 1035-CPD-ES033858'))
        canvas.drawCentredString(medidas['logo1_cabecera'][0]
                                    + medidas['logo1_cabecera'][2]/2.0,
                                 medidas['logo1_cabecera'][1] - 0.2*cm,
                                 escribe('Fibra CE 1035-CPD-9003712'))
    canvas.setFont(fuentes['cabecera_negrita']['fuente'],
                   fuentes['cabecera_negrita']['tamaño'])
    canvas.drawString(medidas['empresa_cabecera'][0],
                      medidas['empresa_cabecera'][1],
                      escribe(datos_empresa.nombre))
    canvas.setFont(fuentes['cabecera']['fuente'],
                   fuentes['cabecera']['tamaño'])
    canvas.drawString(medidas['direccion0_cabecera'][0],
                      medidas['direccion0_cabecera'][1],
                      escribe(datos_empresa.direccion))
    canvas.drawString(medidas['direccion1_cabecera'][0],
                      medidas['direccion1_cabecera'][1],
                      escribe("%s %s (%s), %s" % (datos_empresa.cp,
                                                  datos_empresa.ciudad,
                                                  datos_empresa.provincia,
                                                  datos_empresa.pais)))
    canvas.drawString(medidas['telefono_cabecera'][0],
                      medidas['telefono_cabecera'][1],
                      escribe("Telf.: %s" % (datos_empresa.telefono)))
    canvas.drawString(medidas['fax_cabecera'][0],
                      medidas['fax_cabecera'][1],
                      escribe("Fax: %s" % (datos_empresa.fax)))
    # mail
    from reportlab.lib import colors
    canvas.saveState()
    canvas.setFont("Courier", 10)
    canvas.setFillColor(colors.blue)
    canvas.drawString(medidas['mail_cabecera'][0],
                      medidas['mail_cabecera'][1],
                      escribe(datos_empresa.email))
    ancho = canvas.stringWidth(datos_empresa.email, "Courier", 10)
    rect = (medidas['mail_cabecera'][0], medidas['mail_cabecera'][1],
            medidas['mail_cabecera'][0] + ancho,
            medidas['mail_cabecera'][1]+0.5*cm)
    canvas.linkURL("mailto:%s" % (datos_empresa.email), rect)
    canvas.restoreState()

def calcular_medidas_presupuesto():
    """
    Devuelve las medidas de los campos de la hoja de fax.
    """
    L = -0.60*cm     # Alto de una línea
    l = L * 4   # Línea "contador"
    tm, bm, lm, rm = (29*cm, 1.0*cm, 1.5*cm, 20*cm)
        # "Top", "bottom", "left" y "right margin"
    medidas = {}
    medidas['logo0_cabecera'] = \
        [lm,            tm - 2.3*cm, 2.5*cm, 2.2*cm]      # x, y, ancho y alto
    medidas['logo1_cabecera'] = \
        [rm - 4*cm,     tm - 2*cm, 2.54*cm, 1.651*cm]      # x, y, ancho y alto
    medidas['empresa_cabecera'] =       [lm,            tm + l]; l += 0.75*L
    medidas['direccion0_cabecera'] =    [lm,            tm + l]; l += 0.75*L
    medidas['direccion1_cabecera'] =    [lm,            tm + l]; l += 0.75*L
    medidas['telefono_cabecera'] =      [lm,            tm + l]; l += 0.75*L
    medidas['fax_cabecera'] =           [lm,            tm + l]; l += 0.75*L
    medidas['mail_cabecera'] =          [lm,            tm + l]; l += 2*L

    medidas['fecha'] =                  [lm,            tm + l]; l += L
    medidas['atencion'] =               [lm,            tm + l]; l += L
    medidas['nombrecliente'] =          [lm,            tm + l]; l += L
    medidas['direccion0'] =             [lm,            tm + l]; l += L
    medidas['direccion1'] =             [lm,            tm + l]; l += L
    medidas['telefono'] =               [lm,            tm + l]; l += L
    medidas['fax'] =                    [lm,            tm + l]; l += L
    medidas['texto'] =                  [lm,            tm + l]; l += L
        # productos, servicios y despedida irán a continuación del texto.
        # Donde acabe el párrafo anterior.
    medidas['firmado0'] =               [lm + 10 * cm,  bm - 4.75*L]
    medidas['firmado1'] =               [lm + 10 * cm,  bm - 3.75*L]
    medidas['firmado2'] =               [lm + 10 * cm,  bm - 2.75*L]
    medidas['firmado3'] =               [lm + 10 * cm,  bm - 1.75*L]

    medidas['pie0'] =                   [(lm + rm)/2.0, bm - 0.75*L]
    medidas['pie1'] =                   [(lm + rm)/2.0, bm - 0.25*L]
    return medidas

def generar_pdf_presupuesto(presupuesto):
    """
    Recibe un objeto Presupuesto con el que genera una carta de oferta de
    precio.
    """
    ## Tamaños que usaré
    una_linea = -17
    medidas = calcular_medidas_presupuesto()

    ## Preparo el archivo y el canvas
    nomarchivo = os.path.join(gettempdir(),
        "oferta_de_precio_%s.pdf" % (give_me_the_name_baby()))
    c = canvas.Canvas(nomarchivo)
    c.setPageSize(A4)

    ## Fuentes
    fuentes = {'normal': {'fuente': "Helvetica", 'tamaño': 12},
               'negrita': {'fuente': "Helvetica-Bold", 'tamaño': 12},
               'grande': {'fuente': "Times-Roman", 'tamaño': 48},
               'cabecera': {'fuente': "Times-Italic", 'tamaño': 10},
               'cabecera_negrita': {'fuente': "Times-Bold", 'tamaño': 12},
               'pie': {'fuente': "Times-Roman", 'tamaño': 8}}
    c.setFont(fuentes['negrita']['fuente'], fuentes['negrita']['tamaño'])
    escribir_cabecera(c, medidas, fuentes)
    escribir_pie(c, medidas, fuentes)
    # Hasta aquí tenemos una plantilla más o menos estándar con cabecera y
    # pie de página.
    escribir_cuerpo_presupuesto(c, medidas, fuentes, presupuesto, una_linea)
    if presupuesto.validez:
        txt_validez = "OFERTA VÁLIDA POR %s DESDE LA FECHA DE ESTE PRESUPUESTO"
        if presupuesto.validez == 1:
            mes = "UN MES"
        else:
            from formularios.numerals import numerals
            txt_meses = numerals(presupuesto.validez,
                                 moneda = "",
                                 fraccion = "",
                                 autoomitir = True).upper()
            mes = "%s MESES" % txt_meses
        txt_validez = txt_validez % (mes)
        centrox = A4[0] / 2.0
        y = 0.75 * cm
        c.saveState()
        c.setFont("Courier", 10)
        c.drawCentredString(centrox, y, escribe(txt_validez))
        c.restoreState()
    ## Por último guardo y devuelvo el nombre del PDF generado (no hace falta
    ## «showPage», el «save» lo hace por mí antes de escribir el PDF).
    c.save()
    return nomarchivo

def escribir_cuerpo_presupuesto(c, medidas, fuentes, presupuesto, una_linea):
    """
    Cuerpo del fax.
    """
    try:
        datos_empresa = pclases.DatosDeLaEmpresa.select()[0]
    except IndexError:
        print "geninformes::_escribir_textofijo -> No se encontraron los "\
              "datos de la empresa en la tabla datos_de_la_empresa."
    else:
        c.setFont(fuentes['normal']['fuente'], fuentes['normal']['tamaño'])
        fecha_corta = corregir_nombres_fecha(
            presupuesto.fecha.strftime("%d de %B de %Y"))
        textofecha = "%s a %s" % (datos_empresa.ciudad, fecha_corta)
        c.drawString(medidas['fecha'][0], medidas['fecha'][1],
                     escribe(textofecha))

        if presupuesto.personaContacto != "":
            c.setFont(fuentes['negrita']['fuente'],
                      fuentes['negrita']['tamaño'])
            c.drawString(medidas['atencion'][0], medidas['atencion'][1],
                escribe("A la atención de %s" % (presupuesto.personaContacto)))
        c.setFont(fuentes['normal']['fuente'], fuentes['normal']['tamaño'])
        c.drawString(medidas['nombrecliente'][0], medidas['nombrecliente'][1],
                     escribe(presupuesto.nombrecliente))
        c.drawString(medidas['direccion0'][0], medidas['direccion0'][1],
                     escribe(presupuesto.direccion))
        listadireccion = [presupuesto.cp, presupuesto.ciudad]
        if presupuesto.ciudad.strip() != presupuesto.provincia.strip():
            listadireccion.append(presupuesto.provincia)
        listadireccion.append(presupuesto.pais)
        segunda_linea_direccion = " ".join([token.strip() for token
                                            in listadireccion
                                            if token.strip() != ""])
        c.drawString(medidas['direccion1'][0], medidas['direccion1'][1],
                     escribe(segunda_linea_direccion))
        if presupuesto.telefono.strip() != "":
            c.drawString(medidas['telefono'][0], medidas['telefono'][1],
                         escribe("Tlf.: %s" % (presupuesto.telefono)))
        if presupuesto.fax.strip() != "":
            c.drawString(medidas['fax'][0], medidas['fax'][1],
                         escribe("Fax.: %s" % (presupuesto.fax)))

        lineatexto = escribir_texto_presupuesto(presupuesto, medidas,
            medidas['texto'][1], c, fuentes, una_linea)
        lineatexto = escribir_productos_presupuesto(presupuesto, medidas,
            lineatexto, c, fuentes, una_linea)
        lineatexto = escribir_servicios_presupuesto(presupuesto, medidas,
            lineatexto, c, fuentes, una_linea)
        lineatexto = escribir_despedida_presupuesto(presupuesto, medidas,
            lineatexto, c, fuentes, una_linea)

        if not presupuesto.comercial:
            elabajofirmante = {
                'nombre': datos_empresa.nombreResponsableCompras, 
                'correoe': datos_empresa.emailResponsableCompras, 
                'telefono': datos_empresa.telefonoResponsableCompras, 
                'cargo': None}
        else:
            comercial = presupuesto.comercial
            elabajofirmante = {
                'nombre': (comercial.empleado.nombre 
                            + " " + comercial.empleado.apellidos), 
                'correoe': comercial.correoe, 
                'telefono': comercial.telefono, 
                'cargo': comercial.cargo}
        c.drawString(medidas['firmado0'][0], medidas['firmado0'][1],
                     escribe(elabajofirmante['nombre']))
        if elabajofirmante['cargo'] is None:
            escribir_mail(c, medidas['firmado1'][0], medidas['firmado1'][1],
                          escribe(elabajofirmante['correoe']))
            c.drawString(medidas['firmado2'][0], medidas['firmado2'][1],
                         escribe(elabajofirmante['telefono']))
        else:
            c.drawString(medidas['firmado1'][0], medidas['firmado1'][1],
                         escribe(elabajofirmante['cargo']))
            c.drawString(medidas['firmado2'][0], medidas['firmado2'][1],
                         escribe(elabajofirmante['telefono']))
            escribir_mail(c, medidas['firmado3'][0], medidas['firmado3'][1],
                          escribe(elabajofirmante['correoe']))

def escribir_despedida_presupuesto(presupuesto, medidas, lineatexto, c,
                                   fuentes, una_linea):
    c.setFont(fuentes['normal']['fuente'], fuentes['normal']['tamaño'])
    for parrafo in presupuesto.despedida.split("\n"):
        saltos = agregarFila(medidas['texto'][0], lineatexto, rm,
                             escribe(parrafo), c, fuentes['normal']['fuente'],
                             fuentes['normal']['tamaño'],
                             altura_linea = -una_linea)
        lineatexto += saltos * una_linea
        lineatexto = comprobar_nueva_pagina_presupuesto(c, lineatexto,
            medidas, fuentes)
    return lineatexto

def escribir_productos_presupuesto(presupuesto, medidas, lineatexto, c,
                                   fuentes, una_linea):
    c.setFont(fuentes['negrita']['fuente'], fuentes['negrita']['tamaño'])
    for ldp in presupuesto.lineasDePedido:
        cantidad = utils.float2str(ldp.cantidad)
        precio = utils.float2str(ldp.precio*(1-ldp.descuento), 3, autodec=True)
        if ldp.productoVenta != None:
            descripcion = ldp.productoVenta.descripcion.capitalize()
            if ldp.productoVenta.es_rollo():
                unidad = "m²"
                descripcion += " (%d gr/m²)" % (
                    ldp.productoVenta.camposEspecificosRollo.gramos)
            elif ldp.productoVenta.es_bala or ldp.productoVenta.es_bigbag():
                unidad = "kg"
                descripcion += " (corte: %d; título: %s dtex)" % (
                  ldp.productoVenta.camposEspecificosBala.corte,
                  utils.float2str(ldp.productoVenta.camposEspecificosBala.dtex,
                                  1))
            elif ldp.productoVenta.es_especial():
                unidad = ldp.productoVenta.camposEspecificosEspecial.unidad
            else:
                print "geninformes::escribir_productos_presupuesto -> No se "\
                      "pudo determinar tipo de producto de venta."
                unidad = "?"
        elif ldp.productoCompra != None:
            unidad = ldp.productoCompra.unidad
            descripcion = ldp.productoCompra.descripcion.title()
        else:
            print "geninformes::escribir_productos_presupuesto -> No se pudo"\
                  " determinar producto de la línea de pedido."
            unidad = descripcion = "?"
        texto_producto = "%s %s de %s a %s €/%s." % (cantidad,
                                                     unidad,
                                                     descripcion,
                                                     precio,
                                                     unidad)
        saltos = agregarFila(medidas['texto'][0], lineatexto, rm,
                             escribe(texto_producto), c,
                             fuentes['negrita']['fuente'],
                             fuentes['negrita']['tamaño'],
                             altura_linea = -una_linea)
        lineatexto += saltos * una_linea
        lineatexto = comprobar_nueva_pagina_presupuesto(c, lineatexto,
                                                        medidas, fuentes)
    lineatexto += una_linea / 2.0
    return lineatexto

def escribir_servicios_presupuesto(presupuesto, medidas, lineatexto, c,
                                   fuentes, una_linea):
    c.setFont(fuentes['negrita']['fuente'], fuentes['negrita']['tamaño'])
    for srv in presupuesto.servicios:
        if srv.cantidad == 1:
            cantidad = ""
            total = ""
        else:
            cantidad = "%s " % (utils.float2str(srv.cantidad, 3,
                                autodec = True))
            total = " (%s € en total)" % (utils.float2str(srv.get_subtotal()))
        precio = "%s €" % (
            utils.float2str(srv.precio * (1-srv.descuento), 3, autodec = True))
        srvconcepto = utils.corregir_mayusculas_despues_de_punto(srv.concepto)
        texto_servicio = "%s%s %s %s%s." % (cantidad, srvconcepto,
            srvconcepto.strip().endswith(".") and "A" or "a", precio, total)
        saltos = agregarFila(medidas['texto'][0], lineatexto, rm,
                             escribe(texto_servicio), c,
                             fuentes['negrita']['fuente'],
                             fuentes['negrita']['tamaño'],
                             altura_linea = -una_linea)
        lineatexto += saltos * una_linea
        lineatexto = comprobar_nueva_pagina_presupuesto(c, lineatexto,
                                                        medidas, fuentes)
    if presupuesto.descuento:
        texto_dto = "Descuento global del %s %% (%s €)." % (
            utils.float2str(presupuesto.descuento * 100, autodec = True),
            utils.float2str(
                presupuesto.calcular_subtotal(incluir_descuento = False)
                * presupuesto.descuento))
        saltos = agregarFila(medidas['texto'][0], lineatexto, rm,
            escribe(texto_dto), c, fuentes['negrita']['fuente'],
            fuentes['negrita']['tamaño'], altura_linea = -una_linea)
        lineatexto += saltos * una_linea
        lineatexto = comprobar_nueva_pagina_presupuesto(c, lineatexto,
                                                        medidas, fuentes)
    lineatexto += una_linea / 2.0
    return lineatexto

def escribir_texto_presupuesto(presupuesto, medidas, lineatexto, c, fuentes,
                               una_linea):
    c.setFont(fuentes['normal']['fuente'], fuentes['normal']['tamaño'])
    for parrafo in presupuesto.texto.split("\n"):
        saltos = agregarFila(medidas['texto'][0], lineatexto, rm,
                             escribe(parrafo), c, fuentes['normal']['fuente'],
                             fuentes['normal']['tamaño'],
                             altura_linea = -una_linea)
        lineatexto += saltos * una_linea
        lineatexto = comprobar_nueva_pagina_presupuesto(c, lineatexto,
                                                        medidas, fuentes)
    lineatexto += una_linea / 2.0
    return lineatexto

def comprobar_nueva_pagina_presupuesto(c, lineatexto, medidas, fuentes):
    """
    Si lineatexto está cerca del pie de la hoja, avanza el canvas
    una página y vuelve a la posición inicial.
    """
    if abs(lineatexto - medidas['firmado0'][1]) <= 0.5*cm:
        c.showPage()
        escribir_cabecera(c, medidas, fuentes)
        escribir_pie(c, medidas, fuentes)
        lineatexto = medidas['atencion'][1]
    return lineatexto

def escribir_mail(c, x, y, email):
    """
    Escribe y hace "clicable" la dirección de correo electrónico «email»
    en la posición (x, y) del canvas «c».
    """
    from reportlab.lib import colors
    c.saveState()
    c.setFont("Courier", 10)
    c.setFillColor(colors.blue)
    c.drawString(x, y, escribe(email))
    ancho = c.stringWidth(email, "Courier", 10)
    rect = (x, y, x + ancho, y + 0.5*cm)
    c.linkURL("mailto:%s" % (email), rect)
    c.restoreState()


# XXX ------------------------------------------------------------------------

def informe_marcado_ce(producto,
                       rango_partidas = None,
                       ventana_padre = None,
                       ignorar_errores = False,
                       exportar_a_csv_a = None):
    """
    Genera un PDF con el informe de marcado CD para el producto "producto".
    Si "rango_partida" es != None, mostrará en el PDF solo las partidas de
    la lista o tupla de objetos partida.
    Si en el rango hay una partida que no pernece al producto la ignora.
    Si "rango_partida" es None, imprime todas las partidas del producto.
    En el informe generado las partidas se ordenan por número de partida
    independientemente del orden en que se reciban (si es que la lista de
    partidas no es None).
    Si "ventana_padre" es diferente de None, los mensajes de error los mostrará
    en un diálogo a la vez que por salida estándar.
    """
    # Pruebas en orden en que aparecerán en el listado.
    pruebas = ("Gramaje", "Compresion", "Longitudinal", "Transversal",
               "AlargamientoLongitudinal", "AlargamientoTransversal",
               "Perforacion", "Espesor", "Permeabilidad", "Poros", 
               "Piramidal")
    trans = {'Gramaje': 'gramaje',
             'Longitudinal': 'longitudinal',
             'Transversal': 'transversal',
             'AlargamientoLongitudinal': 'alongitudinal',
             'AlargamientoTransversal': 'atransversal',
             'Compresion': 'compresion',
             'Perforacion': 'perforacion',
             'Espesor': 'espesor',
             'Permeabilidad': 'permeabilidad',
             'Poros': 'poros', 
             'Piramidal': 'piramidal'
            }  # "Traducción" de la prueba al nombre del campo en la partida.
    dic_pruebas = {
        'Gramaje': 'pruebasGramaje',
        'Longitudinal': 'pruebasResistenciaLongitudinal',
        'Transversal': 'pruebasResistenciaTransversal',
        'AlargamientoLongitudinal':'pruebasAlargamientoLongitudinal',
        'AlargamientoTransversal': 'pruebasAlargamientoTransversal',
        'Compresion': 'pruebasCompresion',
        'Perforacion': 'pruebasPerforacion',
        'Espesor': 'pruebasEspesor',
        'Permeabilidad': 'pruebasPermeabilidad',
        'Poros': 'pruebasPoros', 
        'Piramidal': 'pruebasPiramidal'
       } #"Traducción" de la prueba al nombre del campo de la lista de pruebas.
    cer = producto.camposEspecificosRollo
    datos = []
    medias = []
    partidas_del_producto = producto.get_partidas()
    fecha_mas_antigua = None
    if rango_partidas == None:
        rango_partidas = partidas_del_producto
    for partida in rango_partidas:
        producto_partida = partida.get_producto()
        if not ignorar_errores and producto_partida != producto:
            txt = "geninformes::informe_marcado_ce -> La partida ID %d no es "\
                  "del producto %d (%s), sino de %d (%s)." % (partida.id,
                    producto.id, producto.descripcion, producto_partida.id,
                    producto_partida.descripcion)
            print txt
            if ventana_padre:
                utils.dialogo_info(titulo = "PARTIDA INCOHERENTE",
                                   texto = "La partida %s no se mostrará, dad"\
                    "o que combina\nvarios productos con características dife"\
                    "rentes\ny el principal no es el seleccionado.\nProductos"\
                    " que contiene la partida:\n%s.\n\nPulse «Aceptar» para c"\
                    "ontinuar." % (partida.codigo,
                                   "\n".join([p.descripcion for p
                                              in partida.get_productos()])),
                                   padre = ventana_padre)
        else:
            producto = partida.get_producto()
            descproducto = producto and producto.descripcion or ""
            fecha_fabricacion = partida.get_fecha_fabricacion()
            if not fecha_mas_antigua or fecha_fabricacion < fecha_mas_antigua:
                fecha_mas_antigua = fecha_fabricacion
            fila = [partida.numpartida,
                    "%s (%d)" % (partida.codigo, len(partida.muestras)),
                    descproducto,
                    utils.str_fecha(fecha_fabricacion)]
            filamedias = []
            for prueba in pruebas:
                valor = getattr(partida, trans[prueba])
                if len(getattr(partida, dic_pruebas[prueba])) == 0:
                    valor = None
                fecha_partida = partida.get_fecha_fabricacion()
                dif, evaluacion = cer.comparar_con_marcado(valor,  # @UnusedVariable
                                                           prueba,
                                                           fecha_partida)
                if valor == None:
                    valor = 0   # Una vez evaluado con None, lo vuelvo a
                                # poner a 0 para imprimir el valor numérico
                                # con float2str abajo y tal.
                if evaluacion == 0:
                    color = "[color=azul]"
                elif 1 <= evaluacion <= 2:
                    color = "[color=verde]"
                elif evaluacion >= 3:
                    color = "[color=rojo]"
                elif evaluacion == -1:
                    color = "[color=gris]"
                else:
                    color = ""
                fila.append("%s%s" % (
                            utils.float2str(valor, 3, autodec = True), color))
                filamedias.append(valor)
            datos.append(fila)
            if len(partida.observaciones.strip()) > 0:
                datos.append((partida.numpartida, ) + ("",)*3
                            + ("Observaciones: " + partida.observaciones, )
                            + (">->", ) * 9)
            medias.append(filamedias)
    datos.sort(lambda f1, f2: (f1[0] < f2[0] and -1)
                              or (f1[0] > f2[0] and 1) or 0)
    datos = [f[1:] for f in datos]      # El número de partida era sólo para
                            # ordenar, ya no lo necesito ni quiero imprimirlo.

    # Resumen
    #   Datos estadísticos
    calmedias = [0, ] * len(pruebas)
    calsigmas = [0, ] * len(pruebas)
    if medias != []:
        for i in xrange(len(medias[0])):
            calmedias[i] = sum([m[i] for m in medias]) / len(medias)
            if len(medias) > 1:
                calsigmas[i]=((sum([(m[i] - calmedias[i])**2 for m in medias])
                              / (len(medias) - 1)) ** 0.5)

    ##                                                                       ##
    # Perlitas de Huelva: «Anote; Zúmer, con Zeta. Sí, Ece-u-eme-e-erre.»     #
    # Perlitas de Huelva: «Sí, el paquete es para mandarlo AL NORTE DE        #
    #                       CAROLINA, en Estados Unidos.»                     #
    ##                                                                       ##

    datos.append(("---", ) * (3 + len(pruebas))) # 3 por las tres columnas que 
        # no son valores de pruebas, sino el cód. de partida, prod. y fecha.
    datos.append(("", "Desv. típica", "")
        + tuple([utils.float2str(m, 4, autodec = True) for m in calsigmas]))
    datos.append(("", "Media", "")
        + tuple([utils.float2str(m, 4, autodec = True) for m in calmedias]))

    #   Datos estadísticos ignorando valores nulos
    calmedias = [0, ] * 10
    calsigmas = [0, ] * 10
    if medias != []:
        for i in xrange(len(medias[0])):
            valores_no_nulos = [m[i] for m in medias if m[i] != 0]
            if len(valores_no_nulos) > 0:
                calmedias[i] = sum(valores_no_nulos) / len(valores_no_nulos)
            if len(valores_no_nulos) > 1:
                calsigmas[i] = ((sum([(v - calmedias[i])**2
                                      for v
                                      in valores_no_nulos])
                                    / (len(valores_no_nulos) - 1)) ** 0.5)
    datos.append(("---", ) * (3 + len(pruebas)))
    datos.append(("", "Desv. típica valores no nulos", "")
                    + tuple([utils.float2str(m, 4, autodec = True)
                    for m in calsigmas]))
    datos.append(("", "Media ignorando valores nulos", "")
                    + tuple([utils.float2str(m, 4, autodec = True)
                    for m in calmedias]))
    datos.append(("===", ) * (3 + len(pruebas)))
    fila = ["", "Marcado CE:[color=azul]", ""]
    marcado = cer.buscar_marcado(fecha_mas_antigua)
    if marcado:
        cer = marcado
    for prueba in pruebas:
        valor_marcado = getattr(cer, "estandarPrueba%s" % (prueba))
        fila.append("%s[color=azul]" % (
            utils.float2str(valor_marcado, 3, autodec = True)))
    datos.append(fila)

    # Ya tengo los datos, a construir el informe en sí:
    archivo = os.path.join(gettempdir(), 'marcadoCE_%s_%s' % (
        producto.codigo.replace(" ", "_"), give_me_the_name_baby()))
    titulo = "Resumen marcado CE para %s" % (producto.nombre)
        # La descripción incluye el ancho, no tiene por qué ser
        # el mismo para todas las filas del informe.
    campos = (('(muestras)', 7),
              ('Producto', 20),
              ('Fecha', 7),
              ('Gramaje', 6),
              ('CBR', 6),
              ('R. long.', 6),
              ('R. trans.', 6),
              ('A. long', 6),
              ('A. trans.', 6),
              ('Cono', 6),
              ('Espesor', 6),
              ('Perme.', 6),
              ('Porom.', 6),
              ('Piram.', 6))
    return imprimir2(archivo, titulo, campos, datos,
                     cols_a_derecha = range(3, 3+len(pruebas)),
                     lineas_verticales = 
                        ((sum([c[1] for c in campos[:3]]), True), ),
                     fecha = "Fecha impresión: %s" % (
                        utils.str_fecha(mx.DateTime.localtime())),
                     sobrecampos = (("Partida", 3),),
                     exportar_a_csv_a = exportar_a_csv_a)


def get_str_pedidos_albaranes(factura):
    """
    Devuelve una cadena con los pedidos y albaranes entre paréntesis de las
    LDV de la factura.
    """
    peds = {'-': []}
    for ldv in factura.lineasDeVenta:
        if ldv.pedidoVenta == None and ldv.albaranSalida != None:
            peds['-'].append(ldv.albaranSalida.numalbaran)
        elif ldv.pedidoVenta != None:
            if ldv.pedidoVenta.numpedido not in peds:
                peds[ldv.pedidoVenta.numpedido] = []
            if ldv.albaranSalida != None:
                if (not ldv.albaranSalida.numalbaran
                    in peds[ldv.pedidoVenta.numpedido]):
                    peds[ldv.pedidoVenta.numpedido].append(
                        ldv.albaranSalida.numalbaran)
    pedsalbs = ""
    for p in peds:
        if p == '-' and peds[p] == []:
            continue
        pedsalbs += "%s(%s) " % (p, ', '.join(peds[p]))
    return pedsalbs


####################### RECIBOS BANCARIOS #####################################

def calcular_medidas_recibo():
    """
    Devuelve un diccionario con las medidas de los elementos que componen
    el PDF de un recibo.
    Son medidas relativas. Hay que sumarles los márgenes y el desplazamiento
    deseado antes de usarlas en el canvas.
    """
    L = -0.9 * cm     # "Alto" de una línea
    Y = 9.0 * cm
    XINI = 2.25 * cm
    X = XINI
    ALTO = 9.25 * cm
    ANCHO = 18 * cm

    medidas = {}
    medidas['recibo'] = [0, 0, ANCHO + 0.25 * cm, ALTO]     # x, y, ancho, alto
    medidas['lateral0'] = [0.5 * cm, ALTO / 2, 9*cm, 2*cm]  # x, y, ancho y
        # alto (rotar antes)
    medidas['lateral1'] = [0.9 * cm, ALTO / 2, 9*cm, 2*cm]      # x, y, ancho
        # y alto (rotar antes)
    medidas['lateral2'] = [1.3 * cm, ALTO / 2, 9*cm, 2*cm]      # x, y, ancho
        # y alto (rotar antes)
    medidas['lateral3'] = [1.7 * cm, ALTO / 2, 9*cm, 2*cm]      # x, y, ancho
        # y alto (rotar antes)

    medidas['numrecibo'] = [X, Y, 2.5*cm, L]; X += medidas['numrecibo'][2]
    medidas['lugar_libramiento'] = [X, Y, 9*cm, L]
    X += medidas['lugar_libramiento'][2]
    medidas['importe'] = [X, Y, ANCHO - X, L]; X = XINI; Y += L

    medidas['fecha_libramiento'] = [X, Y, (ANCHO - X)/ 2, L]
    X += medidas['fecha_libramiento'][2]
    medidas['vencimiento'] = [X, Y, ANCHO - X, L]; X = XINI; Y += L - 0.4 * cm

    medidas['codigo_cliente'] = [X, Y, (ANCHO - XINI) / 4, L]
    X += medidas['codigo_cliente'][2]
    medidas['numfactura'] = [X, Y, (ANCHO - XINI) / 4, L]
    X += medidas['numfactura'][2]
    medidas['fechafactura'] = [X, Y, (ANCHO - XINI) / 4, L]
    X += medidas['fechafactura'][2]
    medidas['persona_pago'] = [X, Y, (ANCHO - XINI) / 4, L]
    X = XINI; Y += L - 0.4 * cm

    medidas['importe_letras'] = [X, Y, (ANCHO - XINI), L]; Y += L - 0.4 * cm

    medidas['domicilio_pago'] = [X, Y, (ANCHO - XINI), L]; Y += L
    medidas['cuenta_pago'] = [X, Y, (ANCHO - XINI), L]; Y += L - 0.4 * cm

    medidas['nombre_librado'] = [X, Y, 10.5 * cm, L]
    X += medidas['nombre_librado'][2]
    medidas['por_poder0'] = [X + 0.1 * cm, Y - 0.5 * cm, ANCHO - X, L]
    Y += L; X = XINI
    medidas['direccion_librado'] = [X, Y, medidas['nombre_librado'][2], L]
    X += medidas['direccion_librado'][2]
    medidas['por_poder1'] = [X + 0.1 * cm, Y, medidas['por_poder0'][2], L]
    return medidas


def recibo(numrecibo, lugar_libramiento, importe, fecha_libramiento,
           vencimiento, codigo_cliente, numfactura, fechafactura,
           persona_pago, domicilio_pago, cuenta_pago, nombre_librado,
           direccion_librado):
    """
    Recibe los datos a imprimir en el recibo *como cadenas*.
    """
    ## Tamaños que usaré
    una_linea = -16  # @UnusedVariable
    medidas = calcular_medidas_recibo()

    ## Preparo el archivo y el canvas
    nomarchivo = os.path.join(gettempdir(),
                              "recibo_%s.pdf" % (give_me_the_name_baby()))
    c = canvas.Canvas(nomarchivo)
    c.setPageSize(A4)

    ## Fuentes
    fuentes = {'normal': {'fuente': "Helvetica", 'tamaño': 12},
               'negrita': {'fuente': "Helvetica-Bold", 'tamaño': 12},
               'grande': {'fuente': "Times-Roman", 'tamaño': 48},
               'cursiva': {'fuente': "Times-Italic", 'tamaño': 10},
               'cabecera_negrita': {'fuente': "Times-Bold", 'tamaño': 12},
               'pie': {'fuente': "Times-Roman", 'tamaño': 8},
               'pequeña': {'fuente': "Helvetica", 'tamaño': 8}}

    ## Genero un recibo en la primera posición:
    tm, bm, lm, rm = (29*cm, 1.0*cm, 1.5*cm, 20*cm)    # "Top", "bottom",
        # "left" y "right margin"
    xoffset, yoffset = lm, tm - medidas['recibo'][3]
    from formularios.numerals import numerals
    try:
        importe_letras = numerals(utils.parse_euro(importe), moneda = "",
                                  fraccion = "", autoomitir = True).upper()
    except:
        importe_letras = "ERROR"
    datos = {"numrecibo": numrecibo,
             "lugar_libramiento": lugar_libramiento,
             "importe": importe,
             "importe_letras": importe_letras,
             "fecha_libramiento": fecha_libramiento,
             "vencimiento": vencimiento,
             "codigo_cliente": codigo_cliente,
             "numfactura": numfactura,
             "fechafactura": fechafactura,
             "persona_pago": persona_pago,
             "domicilio_pago": domicilio_pago,
             "cuenta_pago": cuenta_pago,
             "nombre_librado": nombre_librado,
             "direccion_librado": direccion_librado}
    generar_recibo(c, medidas, fuentes, xoffset, yoffset, datos)

    ## Y otro a continuación:
    yoffset -= medidas['recibo'][3] # + 0.1 * cm
    generar_recibo(c, medidas, fuentes, xoffset, yoffset, datos)

    ## Por último guardo y devuelvo el nombre del PDF generado (no hace falta
    ## «showPage», el «save» lo hace por mí antes de escribir el PDF).
    c.save()
    return nomarchivo

def generar_recibo(c, medidas, fuentes, xoffset, yoffset, datos):
    """
    Dibuja en el canvas «c» un recibo usando las medidas y datos recibidos.
    A cada medida le suma el offset en X e Y antes de aplicarla.
    """
    try:
        dde = pclases.DatosDeLaEmpresa.select()[0]
        dde0 = dde.nombre.upper()
        if dde.nombreContacto != dde.nombre:
            contacto = dde.nombreContacto + " - "
        else:
            contacto = ""
        dde1 = "%s%c.I.F.: %s - %s" % (contacto, dde.irpf == 0 and "C" or "N",
                                       dde.cif, dde.dirfacturacion)
        dde2 = "%s: %s - Tlf.: %s" % (not dde.esSociedad and dde.irpf == 0
                                        and "Tienda" or "Ofic.",
                                      dde.direccion, dde.telefono)
        dde3 = "%s - %s (%s)" % (dde.cp, dde.ciudad, dde.provincia)
        dde_por_poder = dde.nombre
    except IndexError:
        print "geninformes::generar_recibo -> Datos de la empresa no "\
              "encontrados."
        dde0 = "SIN DATOS"
        dde1 = "-"
        dde2 = "sin datos"
        dde3 = "-"
        dde_por_poder = ""

    mer = medidas['recibo'][:]
    mer[0] += xoffset; mer[1] += yoffset
    rectangulo(c, (mer[0], mer[1]), (mer[0] + mer[2], mer[1] + mer[3]))

    c.setFont(fuentes['normal']['fuente'], fuentes['normal']['tamaño'])
    mer = medidas['numrecibo'][:]
    mer[0] += xoffset; mer[1] += yoffset
    rectangulo(c, (mer[0], mer[1]), (mer[0] + mer[2], mer[1] + mer[3]),
               texto = datos['numrecibo'], alinTxtX = "centro")
    def escribir_cabecera_campo(x, y, txt):
        c.saveState()   # scope de c (canvas) entra en la función anidada.
        c.setFont(fuentes['pequeña']['fuente'], fuentes['pequeña']['tamaño'])
        c.drawString(x + 0.1 * cm, y - 0.3 * cm, escribe(txt)); \
        c.restoreState()
    escribir_cabecera_campo(mer[0], mer[1], "Nº Recibo")

    c.saveState()
    c.setFont(fuentes['negrita']['fuente'], fuentes['negrita']['tamaño'])
    mer = medidas['lateral0'][:]
    mer[0] += xoffset; mer[1] += yoffset
    c.translate(mer[0], mer[1])
    c.rotate(90)
    c.drawCentredString(0, 0, dde0)
    c.restoreState()

    c.saveState()
    c.setFont(fuentes['pequeña']['fuente'], fuentes['pequeña']['tamaño'])
    mer = medidas['lateral1'][:]
    mer[0] += xoffset; mer[1] += yoffset
    c.translate(mer[0], mer[1])
    c.rotate(90)
    c.drawCentredString(0, 0, dde1)
    c.restoreState()

    c.saveState()
    c.setFont(fuentes['pequeña']['fuente'], fuentes['pequeña']['tamaño'])
    mer = medidas['lateral2'][:]
    mer[0] += xoffset; mer[1] += yoffset
    c.translate(mer[0], mer[1])
    c.rotate(90)
    c.drawCentredString(0, 0, dde2)
    c.restoreState()

    c.saveState()
    c.setFont(fuentes['pequeña']['fuente'], fuentes['pequeña']['tamaño'])
    mer = medidas['lateral3'][:]
    mer[0] += xoffset; mer[1] += yoffset
    c.translate(mer[0], mer[1])
    c.rotate(90)
    c.drawCentredString(0, 0, dde3)
    c.restoreState()

    mer = medidas['lugar_libramiento'][:]
    mer[0] += xoffset; mer[1] += yoffset
    rectangulo(c, (mer[0], mer[1]), (mer[0] + mer[2], mer[1] + mer[3]),
               texto = datos['lugar_libramiento'], alinTxtX = "centro")
    escribir_cabecera_campo(mer[0], mer[1], "Lugar de emisión")

    mer = medidas['importe'][:]
    mer[0] += xoffset; mer[1] += yoffset
    rectangulo(c, (mer[0], mer[1]), (mer[0] + mer[2], mer[1] + mer[3]),
               texto = "# " + datos['importe'] + " #", alinTxtX = "centro")
    escribir_cabecera_campo(mer[0], mer[1], "Importe")

    mer = medidas['fecha_libramiento'][:]
    mer[0] += xoffset; mer[1] += yoffset
    rectangulo(c, (mer[0], mer[1]), (mer[0] + mer[2], mer[1] + mer[3]),
               texto = datos['fecha_libramiento'], alinTxtX = "centro")
    escribir_cabecera_campo(mer[0], mer[1], "Fecha de emisión")

    mer = medidas['vencimiento'][:]
    mer[0] += xoffset; mer[1] += yoffset
    rectangulo(c, (mer[0], mer[1]), (mer[0] + mer[2], mer[1] + mer[3]),
               texto = datos['vencimiento'], alinTxtX = "centro")
    escribir_cabecera_campo(mer[0], mer[1], "Vencimiento")

    mer = medidas['codigo_cliente'][:]
    mer[0] += xoffset; mer[1] += yoffset
    rectangulo(c, (mer[0], mer[1]), (mer[0] + mer[2], mer[1] + mer[3]),
               texto = datos['codigo_cliente'], alinTxtX = "centro")
    escribir_cabecera_campo(mer[0], mer[1], "Código de cliente")

    mer = medidas['numfactura'][:]
    mer[0] += xoffset; mer[1] += yoffset
    rectangulo(c, (mer[0], mer[1]), (mer[0] + mer[2], mer[1] + mer[3]),
               texto = datos['numfactura'], alinTxtX = "centro")
    escribir_cabecera_campo(mer[0], mer[1], "Número de factura")

    mer = medidas['fechafactura'][:]
    mer[0] += xoffset; mer[1] += yoffset
    rectangulo(c, (mer[0], mer[1]), (mer[0] + mer[2], mer[1] + mer[3]),
               texto = datos['fechafactura'], alinTxtX = "centro")
    escribir_cabecera_campo(mer[0], mer[1], "Fecha de factura")

    if datos['persona_pago'] != "":
        mer = medidas['persona_pago'][:]
        mer[0] += xoffset; mer[1] += yoffset
        rectangulo(c, (mer[0], mer[1]), (mer[0] + mer[2], mer[1] + mer[3]),
                   texto = datos['persona_pago'], alinTxtX = "centro")
        escribir_cabecera_campo(mer[0], mer[1], "Persona de pago")

    mer = medidas['importe_letras'][:]
    mer[0] += xoffset; mer[1] += yoffset
    rectangulo(c, (mer[0], mer[1]), (mer[0] + mer[2], mer[1] + mer[3]),
               texto = "--- " + datos['importe_letras'] + " ---",
               alinTxtX = "centro")
    escribir_cabecera_campo(mer[0], mer[1], "Por este recibo pagará usted al"\
        " vencimiento expresado la cantidad de")

    mer = medidas['domicilio_pago'][:]
    mer[0] += xoffset; mer[1] += yoffset
    #rectangulo(c, (mer[0], mer[1]), (mer[0] + mer[2], mer[1] + mer[3]),
    # texto = datos['domicilio_pago'], alinTxtX = "centro")
    c.drawCentredString(mer[0] + (mer[2] / 2), mer[1] - 0.8 * cm,
                        datos['domicilio_pago'])
    escribir_cabecera_campo(mer[0], mer[1], "Domicilio y cuenta de pago")

    mer = medidas['cuenta_pago'][:]
    mer[1] = medidas['domicilio_pago'][1]
    mer[3] = medidas['domicilio_pago'][3] + medidas['cuenta_pago'][3]
    mer[0] += xoffset; mer[1] += yoffset
    rectangulo(c, (mer[0], mer[1]), (mer[0] + mer[2], mer[1] + mer[3]),
               texto = datos['cuenta_pago'], alinTxtX = "centro")

    mer = medidas['nombre_librado'][:]
    mer[0] += xoffset; mer[1] += yoffset
    #rectangulo(c, (mer[0], mer[1]), (mer[0] + mer[2], mer[1] + mer[3]),
    # texto = datos['nombre_librado'], alinTxtX = "centro")
    el_encogedor_de_fuentes_de_doraemon(c,
                                        fuentes['normal']['fuente'],
                                        fuentes['normal']['tamaño'],
                                        mer[0],
                                        mer[0] + mer[2],
                                        mer[1] - 0.8 * cm,
                                        datos['nombre_librado'],
                                        alineacion = 0)
    # c.drawCentredString(mer[0] + (mer[2] / 2), mer[1] - 0.8 * cm,
    # datos['nombre_librado'])
    escribir_cabecera_campo(mer[0], mer[1], "Nombre y dirección del librado")

    mer = medidas['direccion_librado'][:]
    mer[1] = medidas['nombre_librado'][1]
    mer[3] = medidas['nombre_librado'][3] + medidas['direccion_librado'][3]
    mer[0] += xoffset; mer[1] += yoffset
    rectangulo(c, (mer[0], mer[1]), (mer[0] + mer[2], mer[1] + mer[3]),
               texto = datos['direccion_librado'], alinTxtX = "centro")

    c.setFont(fuentes['pequeña']['fuente'], fuentes['pequeña']['tamaño'])
    mer = medidas['por_poder1'][:]
    mer[0] += xoffset; mer[1] += yoffset
    if dde.nombreContacto != dde.nombre:
        c.drawString(mer[0], mer[1], "Por poder.")

    c.setFont(fuentes['cursiva']['fuente'], fuentes['cursiva']['tamaño'])
    mer = medidas['por_poder0'][:]
    mer[0] += xoffset; mer[1] += yoffset
    c.drawString(mer[0], mer[1], dde_por_poder)

def calcular_medidas_cmr():
    """
    Medidas del CMR.
    """
    dic = {}
    dic['marco'] = [[1*cm, 28.5*cm], [20*cm, 1*cm]]
    dic['doc'] = [[dic['marco'][0][0], dic['marco'][0][1]],
                  [dic['marco'][1][0] / 2, dic['marco'][0][1] - 2*cm]]
    dic['rte'] = [[dic['marco'][0][0], dic['doc'][1][1]],
                  [dic['marco'][1][0] / 2, dic['doc'][1][1] - 3*cm]]
    dic['dest'] = [[dic['marco'][0][0], dic['rte'][1][1]],
                   [dic['marco'][1][0] / 2, dic['rte'][1][1] - 3*cm]]
    dic['entrega'] = [[dic['marco'][0][0], dic['dest'][1][1]],
                      [dic['marco'][1][0] / 2, dic['dest'][1][1] - 3*cm]]
    dic['fecha'] = [[dic['marco'][0][0], dic['entrega'][1][1]],
                    [dic['marco'][1][0] / 2, dic['entrega'][1][1] - 3*cm]]
    dic['inst'] = [[dic['marco'][0][0], dic['fecha'][1][1]],
                   [dic['marco'][1][0] / 2, dic['fecha'][1][1] - 3*cm]]
    dic['anexos'] = [[dic['marco'][0][0], dic['inst'][1][1]],
                     [dic['marco'][1][0] / 2, dic['inst'][1][1] - 3*cm]]
    dic['desc'] = [[dic['marco'][0][0], dic['anexos'][1][1]],
                   [dic['marco'][1][0] / 2, dic['anexos'][1][1] - 3*cm]]
    dic['form'] = [[dic['marco'][0][0], dic['desc'][1][1]],
                   [dic['marco'][1][0] / 2, dic['desc'][1][1] - 2*cm]]
    dic['cargadora'] = [[dic['marco'][0][0], dic['form'][1][1]],
                        [dic['marco'][1][0] / 3, dic['form'][1][1] - 2.5*cm]]
    dic['transp'] = [[dic['cargadora'][1][0], dic['form'][1][1]],
                     [(2*dic['marco'][1][0] / 3), dic['form'][1][1] - 2.5*cm]]
    dic['fdest'] = [[dic['transp'][1][0], dic['form'][1][1]],
                    [dic['marco'][1][0], dic['form'][1][1] - 2.5*cm]]

    dic['num'] = [[dic['marco'][1][0] / 2, dic['marco'][0][1]],
                  [dic['marco'][1][0], dic['marco'][0][1] - 2*cm]]
    dic['etransp'] = [[dic['marco'][1][0] / 2, dic['num'][1][1]],
                      [dic['marco'][1][0], dic['num'][1][1] - 4*cm]]
    dic['porteadores'] = [[dic['marco'][1][0] / 2, dic['etransp'][1][1]],
                          [dic['marco'][1][0], dic['etransp'][1][1] - 3*cm]]
    dic['reservas'] = [[dic['marco'][1][0] / 2, dic['porteadores'][1][1]],
                       [dic['marco'][1][0], dic['porteadores'][1][1] - 3*cm]]
    dic['estipulaciones'] = [[dic['marco'][1][0] / 2, dic['reservas'][1][1]],
                             [dic['marco'][1][0],
                              dic['reservas'][1][1] - 8*cm]]
    dic['bruto'] = [[dic['marco'][1][0] / 2, dic['estipulaciones'][1][1]],
                    [(dic['marco'][1][0] / 2) * (4.0/3.0),
                     dic['estipulaciones'][1][1] - 3*cm]]
    dic['neto'] = [[(dic['marco'][1][0] / 2) * (4.0/3.0),
                    dic['estipulaciones'][1][1]],
                   [(dic['marco'][1][0] / 2) * (5.0/3.0),
                    dic['estipulaciones'][1][1] - 3*cm]]
    dic['vol'] = [[(dic['marco'][1][0] / 2) * (5.0/3.0),
                   dic['estipulaciones'][1][1]],
                  [dic['marco'][1][0], dic['estipulaciones'][1][1] - 3*cm]]
    dic['pagado'] = [[dic['marco'][1][0] / 2, dic['vol'][1][1]],
                     [(dic['marco'][1][0] / 2) * (1.5),
                      dic['vol'][1][1] - 2*cm]]
    dic['debido'] = [[(dic['marco'][1][0] / 2) * (1.5), dic['vol'][1][1]],
                     [dic['marco'][1][0], dic['vol'][1][1] - 2*cm]]
    return dic

def escribir_info_cmr(c, a, m, f, lugar_entrega = "", transportista = "",
                      porteadores = "", lugar_carga_linea1 = "", 
                      lugar_carga_linea2 = ""):
    #cmr_control(c, m['marco'], f)
    cmr_control(c, m['doc'], f)
    cmr_rte(c, m['rte'], f)
    cmr_dest(c, m['dest'], f, a)
    cmr_entrega(c, m['entrega'], f, lugar_entrega)
    cmr_fecha(c, m['fecha'], f, a, lugar_carga_linea1, lugar_carga_linea2)
    cmr_inst(c, m['inst'], f)
    cmr_anexos(c, m['anexos'], f, a)
    cmr_descr(c, m['desc'], f, a)
    cmr_form(c, m['form'], f, a)
    cmr_cargadora(c, m['cargadora'], f)
    cmr_transp(c, m['transp'], f, transportista)
    cmr_fdest(c, m['fdest'], f)

    cmr_num(c, m['num'], f, a)
    cmr_etransp(c, m['etransp'], f, a, transportista)
    cmr_porteadores(c, m['porteadores'], f, porteadores)
    cmr_reservas(c, m['reservas'], f)
    cmr_estipulaciones(c, m['estipulaciones'], f)
    cmr_bruto(c, m['bruto'], f)
    cmr_neto(c, m['neto'], f, a)
    cmr_vol(c, m['vol'], f)
    cmr_pagado(c, m['pagado'], f)
    cmr_debido(c, m['debido'], f)

def cmr_control(c, m, f):
    rectangulo(c, m[0], m[1], texto = 'DOCUMENTO DE CONTROL',
               alinTxtX = 'centro', alinTxtY = 'arriba', doble = False)
    rectangulo(c, m[0], m[1], texto = 'Orden FOM/238/2003',
               alinTxtX = 'centro', alinTxtY = 'centro', doble = False)

def cmr_rte(c, m, f):
    rectangulo(c, m[0], m[1], texto = 'Remitente (nombre y domicilio)',
               alinTxtX = None, alinTxtY = 'arriba', doble = False)
    offset = 0.5*cm
    c.line(m[0][0], m[0][1] - offset, m[1][0], m[0][1] - offset)
    dde = pclases.DatosDeLaEmpresa.select()
    if dde.count() > 0:
        dde = dde[0]
        if dde.fax.strip() != "":
            telfax = "Tél.: " + dde.telefono + " - Fax:" + dde.fax
        else:
            telfax = dde.telefono
        ciudadprovincia = dde.cp + " " + dde.ciudad
        if dde.provincia.strip() != "":
            ciudadprovincia += " (%s)" % dde.provincia
        el_encogedor_de_fuentes_de_doraemon(c, f['negrita']['fuente'],
                                            f['negrita']['tamaño'],
                                            m[0][0], m[1][0], m[0][1] - 1*cm,
                                            dde.nombre, alineacion = 0)
        el_encogedor_de_fuentes_de_doraemon(c, f['normal']['fuente'],
                                            f['normal']['tamaño'],
                                            m[0][0], m[1][0], m[0][1] - 1.5*cm,
                                            telfax, alineacion = 0)
        el_encogedor_de_fuentes_de_doraemon(c, f['normal']['fuente'],
                                            f['normal']['tamaño'],
                                            m[0][0], m[1][0], m[0][1] - 2*cm,
                                            dde.direccion, alineacion = 0)
        el_encogedor_de_fuentes_de_doraemon(c, f['normal']['fuente'],
                                            f['normal']['tamaño'],
                                            m[0][0], m[1][0], m[0][1] - 2.5*cm,
                                            ciudadprovincia, alineacion = 0)


def cmr_dest(c, m, f, a):
    rectangulo(c, m[0], m[1], texto = 'Destinatario (nombre y domicilio)',
               alinTxtX = None, alinTxtY = 'arriba', doble = False)
    offset = 0.5*cm
    c.line(m[0][0], m[0][1] - offset, m[1][0], m[0][1] - offset)
    el_encogedor_de_fuentes_de_doraemon(c, f['normal']['fuente'],
                                        f['normal']['tamaño'],
                                        m[0][0], m[1][0], m[0][1] - 1*cm,
                                        a.nombre, alineacion = 0)
    el_encogedor_de_fuentes_de_doraemon(c, f['normal']['fuente'],
                                        f['normal']['tamaño'],
                                        m[0][0], m[1][0], m[0][1] - 1.5*cm,
                                        a.direccion, alineacion = 0)
    el_encogedor_de_fuentes_de_doraemon(c, f['normal']['fuente'],
                                        f['normal']['tamaño'],
                                        m[0][0], m[1][0], m[0][1] - 2*cm,
                                        a.cp, alineacion = 0)
    el_encogedor_de_fuentes_de_doraemon(c, f['normal']['fuente'],
                                        f['normal']['tamaño'],
                                        m[0][0], m[1][0], m[0][1] - 2.5*cm,
                                        a.ciudad + " " + a.pais, alineacion=0)

def cmr_entrega(c, m, f, lugar_entrega):
    rectangulo(c, m[0], m[1], texto = 'Lugar de entrega de la mercancía',
               alinTxtX = None, alinTxtY = 'arriba', doble = False)
    offset = 0.5*cm
    c.line(m[0][0], m[0][1] - offset, m[1][0], m[0][1] - offset)
    lineas = lugar_entrega.split("\n")
    i = 0
    for linea in lineas:
        el_encogedor_de_fuentes_de_doraemon(c, f['normal']['fuente'],
                                            f['normal']['tamaño'],
                                            m[0][0], m[1][0],
                                            m[0][1]-((1.0*cm) + (0.5*cm * i)),
                                            linea,
                                            alineacion = 0)
        i += 1

def cmr_fecha(c, m, f, a, 
              lugar_de_carga_linea1 = "", 
              lugar_de_carga_linea2 = ""):
    rectangulo(c, m[0], m[1],
               texto = 'Lugar y fecha de la carga de la mercancía',
               alinTxtX = None, alinTxtY = 'arriba', doble = False)
    offset = 0.5*cm
    c.line(m[0][0], m[0][1] - offset, m[1][0], m[0][1] - offset)
    # Lugar
    el_encogedor_de_fuentes_de_doraemon(c, f['normal']['fuente'],
        f['normal']['tamaño'], m[0][0], m[1][0], m[0][1] - 1.25 *cm,
        lugar_de_carga_linea1,
        alineacion = 0)
    el_encogedor_de_fuentes_de_doraemon(c, f['normal']['fuente'],
        f['normal']['tamaño'], m[0][0], m[1][0], m[0][1] - 1.75 *cm,
        lugar_de_carga_linea2,
        alineacion = 0)
    # Fecha
    el_encogedor_de_fuentes_de_doraemon(c, f['normal']['fuente'],
        f['normal']['tamaño'], m[0][0], m[1][0], m[0][1] - 2.5 * cm,
        utils.corregir_nombres_fecha(a.fecha.strftime("%A, %d de %B de %Y")),
        alineacion = 0)

def cmr_inst(c, m, f):
    rectangulo(c, m[0], m[1], texto = 'Intrucciones del remitente',
               alinTxtX = None, alinTxtY = 'arriba', doble = False)
    offset = 0.5*cm
    c.line(m[0][0], m[0][1] - offset, m[1][0], m[0][1] - offset)

def cmr_anexos(c, m, f, a):
    rectangulo(c, m[0], m[1], texto = 'Documentos anexos', alinTxtX = None,
               alinTxtY = 'arriba', doble = False)
    offset = 0.5*cm
    c.line(m[0][0], m[0][1] - offset, m[1][0], m[0][1] - offset)
    el_encogedor_de_fuentes_de_doraemon(c, f['normal']['fuente'],
                                        f['normal']['tamaño'],
                                        m[0][0], m[1][0], m[0][1] - 2*cm,
                                        "Albarán " + a.numalbaran,
                                        alineacion = 0)

def cmr_descr(c, m, f, a):
    rectangulo(c, m[0], m[1],
               texto='Descripción de la mercancía (naturaleza y nº de bultos)',
               alinTxtX = None, alinTxtY = 'arriba', doble = False)
    offset = 0.5*cm
    c.line(m[0][0], m[0][1] - offset, m[1][0], m[0][1] - offset)
    if len(a.articulos):
        desc_articulos = "Fibra polipropileno - %d bultos" % len(a.articulos)
    else:
        desc_articulos = ""
    el_encogedor_de_fuentes_de_doraemon(c, f['normal']['fuente'],
                        f['normal']['tamaño'],
                        m[0][0], m[1][0], m[0][1] - 2*cm,
                        desc_articulos,
                        alineacion = 0)

def cmr_form(c, m, f, a):
    rectangulo(c, m[0], m[1], texto = 'Formalizado en:', alinTxtX = None,
               alinTxtY = 'arriba', doble = False)
    offset = 0.5*cm
    c.line(m[0][0], m[0][1] - offset, m[1][0], m[0][1] - offset)
    try:
        ciudad = pclases.DatosDeLaEmpresa.select()[0].ciudad
    except:
        "Minas de Riotinto"
    el_encogedor_de_fuentes_de_doraemon(c, f['normal']['fuente'],
                                f['normal']['tamaño'],
                                m[0][0], m[1][0], m[0][1] - 1.5*cm,
                                "%s, %s" % (ciudad, utils.str_fecha(a.fecha)),
                                alineacion = 0)

def cmr_cargadora(c, m, f):
    rectangulo(c, m[0], m[1], texto = 'Firma y sello Empresa cargadora',
               alinTxtX = None, alinTxtY = 'arriba', doble = False)
    offset = 0.5*cm
    c.line(m[0][0], m[0][1] - offset, m[1][0], m[0][1] - offset)

def cmr_transp(c, m, f, transportista):
    rectangulo(c, m[0], m[1], texto = 'Firma y sello Empresa transportista',
               alinTxtX = None, alinTxtY = 'arriba', doble = False)
    offset = 0.5*cm
    c.line(m[0][0], m[0][1] - offset, m[1][0], m[0][1] - offset)
    lineas = transportista.split("\n")  # @UnusedVariable

def cmr_fdest(c, m, f):
    rectangulo(c, m[0], m[1], texto = 'Firma y sello Empresa destinataria',
               alinTxtX = None, alinTxtY = 'arriba', doble = False)
    offset = 0.5*cm
    c.line(m[0][0], m[0][1] - offset, m[1][0], m[0][1] - offset)

def cmr_num(c, m, f, a):
    #rectangulo(c, m[0], m[1], texto = 'DOCUMENTO Nº %s/%d' % (
    # mx.DateTime.localtime().strftime("%d%m%y"), 1),
    #           alinTxtX = 'centro', alinTxtY = 'centro', doble = False)
    albaranes = [i for i in pclases.AlbaranSalida.select(
                    pclases.AlbaranSalida.q.fecha == a.fecha, orderBy = "id")
                 if not i.es_interno()]
    try:
        numsecuencial = albaranes.index(a) + 1
    except ValueError:
        numsecuencial = 0
    rectangulo(c, m[0], m[1],
               texto = 'DOCUMENTO Nº %s/%d' % (a.fecha.strftime("%d%m%y"),
                                               numsecuencial),
               alinTxtX = 'centro', alinTxtY = 'centro', doble = False)

def cmr_etransp(c, m, f, a, transportista):
    rectangulo(c, m[0], m[1],
               texto = 'Empresa transportista (nombre y domicilio)',
               alinTxtX = None, alinTxtY = 'arriba', doble = False)
    offset = 0.5*cm
    c.line(m[0][0], m[0][1] - offset, m[1][0], m[0][1] - offset)
    lineas = transportista.split("\n")
    i = 0
    for linea in lineas:
        el_encogedor_de_fuentes_de_doraemon(c, f['normal']['fuente'],
                                            f['normal']['tamaño'],
                                            m[0][0], m[1][0],
                                            m[0][1]-((1.0*cm) + (0.5*cm * i)),
                                            linea, alineacion = 0)
        i += 1
    if a.transportista != None:
        matricula_tractor, matricula_semirremolque \
            = a.transportista.parse_matricula()
    else:
        matricula_tractor, matricula_semirremolque = ("", "")
    matr_tractor = "Matrícula vehículo tractor %s" % matricula_tractor
    el_encogedor_de_fuentes_de_doraemon(c, f['normal']['fuente'],
                                        f['normal']['tamaño'],
                                        m[0][0] + 0.1*cm, m[1][0],
                                        m[0][1] - ((1.0*cm) + (0.5*cm * i)),
                                        matr_tractor,
                                        alineacion = -1)
    i += 1
    matr_remolque = "Matrícula vehículo semirremolque %s" % (
        matricula_semirremolque)
    el_encogedor_de_fuentes_de_doraemon(c, f['normal']['fuente'],
                                        f['normal']['tamaño'],
                                        m[0][0] + 0.1*cm, m[1][0],
                                        m[0][1] - ((1.0*cm) + (0.5*cm * i)),
                                        matr_remolque, alineacion = -1)

def cmr_porteadores(c, m, f, porteadores):
    rectangulo(c, m[0], m[1],
               texto = 'Porteadores sucesivos (nombre y domicilio)',
               alinTxtX = None, alinTxtY = 'arriba', doble = False)
    offset = 0.5*cm
    c.line(m[0][0], m[0][1] - offset, m[1][0], m[0][1] - offset)
    lineas = porteadores.split("\n")
    i = 0
    for linea in lineas:
        el_encogedor_de_fuentes_de_doraemon(c, f['normal']['fuente'],
                                            f['normal']['tamaño'],
                                            m[0][0], m[1][0],
                                            m[0][1] - ((1.0*cm)+(0.5*cm * i)),
                                            linea, alineacion = 0)
        i += 1

def cmr_reservas(c, m, f):
    rectangulo(c, m[0], m[1],
               texto = 'Reservas y observaciones del transportista',
               alinTxtX = None, alinTxtY = 'arriba', doble = False)
    offset = 0.5*cm
    c.line(m[0][0], m[0][1] - offset, m[1][0], m[0][1] - offset)

def cmr_estipulaciones(c, m, f):
    rectangulo(c, m[0], m[1], texto = 'Estipulaciones particulares',
               alinTxtX = None, alinTxtY = 'arriba', doble = False)
    offset = 0.5*cm
    c.line(m[0][0], m[0][1] - offset, m[1][0], m[0][1] - offset)
    # CWT: Solo hay que dejar el último punto que me envió jpedrero. Sustituye 
    # al resto, no lo complementa como yo pensaba.
    #lineas_agregadas = agregarFila(m[0][0] + 0.1 * cm, m[0][1] - 1*cm,
    #    m[1][0],
    #    escribe("1.- Las condiciones del presente contrato se regirán por lo"\
    #            " dispuesto en la ley 16/1987 de ordenación de los Transport"\
    #            "es Terrestres y normas de desarrollo."),
    #    c, f['pequeña']['fuente'], f['pequeña']['tamaño'])
    #lineas_agregadas += agregarFila(m[0][0] + 0.1 * cm, m[0][1] -
    #    (1*cm + 0.35 * cm * lineas_agregadas), m[1][0],
    #    escribe("2.- El límite de responsabilidad queda fijado según el artíc"\
    #            "ulo 3 del ROTT en 6,61 euros por kg."),
    #            c, f['pequeña']['fuente'], f['pequeña']['tamaño'])
    #lineas_agregadas += agregarFila(m[0][0] + 0.1 * cm,
    #    m[0][1] - (1*cm + 0.35 * cm * lineas_agregadas), m[1][0],
    #    escribe("3.- Se informa a la empresa cargadora de la posibilidad de s"\
    #            "uscribir un seguro especial para cubrir el valor declarado d"\
    #            "e la mercancía. El coste de la prima será por cuenta de quie"\
    #            "n lo solicite"),
    #    c, f['pequeña']['fuente'], f['pequeña']['tamaño'])
    #lineas_agregadas += agregarFila(m[0][0] + 0.1 * cm,
    #    m[0][1] - (1*cm + 0.35 * cm * lineas_agregadas), m[1][0],
    #    escribe("4.- La indemnización por retraso no superará el límite estab"\
    #            "lecido en la condición 2.19 de la Orden de 25.04.97 por las "\
    #           "que se establecen las condiciones Generales de contratación."),
    #    c, f['pequeña']['fuente'], f['pequeña']['tamaño'])
    #lineas_agregadas += agregarFila(m[0][0] + 0.1 * cm,
    #    m[0][1] - (1*cm + 0.35 * cm * lineas_agregadas), m[1][0],
    #    escribe("5.- Las controversias de carácter mercantil surgidas en rela"\
    #            "ción con el cumplimiento, ejecución o interpretación del pre"\
    #            "sente contrato se someterán a la Junta Arbitral del Transpor"\
    #            "te de Sevilla independientemente del límite cuantitativo est"\
    #            "ablecido en el artículo 38 de la LOTT."),
    #    c, f['pequeña']['fuente'], f['pequeña']['tamaño'])
    #lineas_agregadas += agregarFila(m[0][0] + 0.1 * cm,
    #    m[0][1] - (1*cm + 0.35 * cm * lineas_agregadas), m[1][0],
    #    escribe("6.- De acuerdo con el art. 22 de la LOTT las operaciones de "\
    #            "carga-descarga de la mercancía serán por cuenta respectiva d"\
    #            "el cargador o expedidor y del destinatario."),
    #    c, f['pequeña']['fuente'], f['pequeña']['tamaño'])
    lineas_agregadas = 1 
    lineas_agregadas += agregarFila(m[0][0] + 0.1 * cm,
        m[0][1] - (1*cm + 0.35 * cm * lineas_agregadas), m[1][0],
        escribe("Sometimiento a arbitraje."),
        c, f['pequeña']['fuente'], f['pequeña']['tamaño'])
    lineas_agregadas += 1   # Para hacer más hueco y que quede el texto más 
                            # homogéneo en el hueco.
    lineas_agregadas += agregarFila(m[0][0] + 0.1 * cm,
        m[0][1] - (1*cm + 0.35 * cm * lineas_agregadas), m[1][0],
        escribe("Las partes se someten para la solución de cualquier "
                "controversia relativa a la interpretación y ejecución del "
                "contrato de transporte al que se refiere el presente "
                "documento a la Junta Arbitral de trasnporte que proceda "
                "conforme a lo establecido en la Ley 15/1987 de Ordenación "
                "de los Transportes Terrestres y sus normas de desarrollo."),
        #c, f['pequeña']['fuente'], f['pequeña']['tamaño'])
        c, f['pequeña']['fuente'], f['pequeña']['tamaño'] + 2, 
        altura_linea = 15)

def cmr_bruto(c, m, f):
    rectangulo(c, m[0], m[1], texto = 'Peso bruto en kgs.', alinTxtX = None,
               alinTxtY = 'arriba', doble = False)
    offset = 0.5*cm
    c.line(m[0][0], m[0][1] - offset, m[1][0], m[0][1] - offset)

def cmr_neto(c, m, f, a):
    rectangulo(c, m[0], m[1], texto = 'Peso neto en kgs.', alinTxtX = None,
               alinTxtY = 'arriba', doble = False)
    offset = 0.5*cm
    c.line(m[0][0], m[0][1] - offset, m[1][0], m[0][1] - offset)
    pesototal = sum([art.peso for art in a.articulos])
    str_peso = utils.float2str(pesototal, 2,
                               autodec = True)
    # TODO: Preguntar si en geotextiles usar peso real como está ahora o peso
    # teórico.
    if pesototal != 0:
        cadpeso = "%s kg" % str_peso
    else:
        cadpeso = ""
    el_encogedor_de_fuentes_de_doraemon(c, f['normal']['fuente'],
                                        f['normal']['tamaño'],
                                        m[0][0], m[1][0], m[0][1] - 2*cm,
                                        cadpeso, alineacion = 0)

def cmr_vol(c, m, f):
    rectangulo(c, m[0], m[1], texto = 'Volumen en m³', alinTxtX = None,
               alinTxtY = 'arriba', doble = False)
    offset = 0.5*cm
    c.line(m[0][0], m[0][1] - offset, m[1][0], m[0][1] - offset)

def cmr_pagado(c, m, f):
    rectangulo(c, m[0], m[1], texto = 'Porte pagado', alinTxtX = None,
               alinTxtY = 'centro', doble = False)
    rectangulo(c, (m[1][0] - 1*cm, m[0][1] - 0.8*cm), (m[1][0] - 0.5*cm,
               m[0][1] - 1.3*cm))

def cmr_debido(c, m, f):
    rectangulo(c, m[0], m[1], texto = 'Porte debido', alinTxtX = None,
               alinTxtY = 'centro', doble = False)
    rectangulo(c, (m[1][0] - 1*cm, m[0][1] - 0.8*cm), (m[1][0] - 0.5*cm,
               m[0][1] - 1.3*cm))

def cmr(albaran, lugar = "", transportista = "", porteadores = "", 
        lugar_carga = ""):
    """
    Crea un PDF con el CMR del albarán de salida recibido.
    (En realidad es la carta de portes, pero ya se le ha
    quedado el nombre de CMR).
    """
    una_linea = -17  # @UnusedVariable
    medidas = calcular_medidas_cmr()

    ## Preparo el archivo y el canvas
    nomarchivo = os.path.join(gettempdir(),
                              "cmr_%s.pdf" % (give_me_the_name_baby()))
    c = canvas.Canvas(nomarchivo)
    c.setTitle("CMR_%s" % albaran.numalbaran)
    c.setPageSize(A4)

    ## Fuentes
    fuentes = {'normal': {'fuente': "Helvetica", 'tamaño': 12},
               'pequeña': {'fuente': "Helvetica", 'tamaño': 9},
               'negrita': {'fuente': "Helvetica-Bold", 'tamaño': 12},
               'grande': {'fuente': "Times-Roman", 'tamaño': 48},
               'cabecera': {'fuente': "Times-Italic", 'tamaño': 10},
               'cabecera_negrita': {'fuente': "Times-Bold", 'tamaño': 12},
               'pie': {'fuente': "Times-Roman", 'tamaño': 8}}
    c.setFont(fuentes['normal']['fuente'], fuentes['normal']['tamaño'])
    # NUEVO: Lugar de carga. Si viene vacío uso los datos de la empresa 
    # que se usan (usaban) en el segundo albarán...
    if not lugar_carga:
        # ... pero si hay un almacén relacionado con el albarán, uso el del 
        # albarán.
        almacenalbaran = albaran.almacenOrigen
        if almacenalbaran != None:
            linea1 = almacenalbaran.direccion
            linea2 = "%s - %s (%s)" % (almacenalbaran.cp, 
                                       almacenalbaran.ciudad, 
                                       almacenalbaran.provincia)
            lugar_carga = "\n".join((linea1, linea2))
        else:
            try:
                dde = pclases.DatosDeLaEmpresa.select()[0]
                linea1 = dde.diralbaran2
                linea2 = "%s - %s (%s)" % (dde.cpalbaran2, 
                                           dde.ciualbaran2, 
                                           dde.proalbaran2)
                lugar_carga = "\n".join((linea1, linea2))
            except IndexError:
                pass
    if "\n" in lugar_carga:
        sep = "\n"
    elif " " in lugar_carga:
        sep = " "
    else:
        sep = " "
        pivote = len(lugar_carga)/2
        lugar_carga = lugar_carga[:pivote] + sep + lugar_carga[pivote:]
    lugar_carga_linea1 = lugar_carga.split(sep)[0]
    lugar_carga_linea2 = " ".join(lugar_carga.split(sep)[1:])
    escribir_info_cmr(c, albaran, medidas, fuentes, lugar, transportista,
                      porteadores, lugar_carga_linea1, lugar_carga_linea2)
    ## Por último guardo y devuelvo el nombre del PDF generado (no hace falta
    ## «showPage», el «save» lo hace por mí antes de escribir el PDF).
    c.save()
    return nomarchivo



######################### END OF RECIBOS BANCARIOS ############################


# ------------------------- PRUEBINES, GUAJE -------------------------

def pruebines():
    """
    Prepara los datos para llamar al generador de informes
    """
    _factura = pclases.FacturaVenta.select(orderBy = "-id")[0]
    cliente = {'numcli':str(_factura.cliente.id),
               'nombre':_factura.cliente.nombre,
               'nombref': _factura.cliente.nombref,
               'cif':_factura.cliente.cif,
               'direccion':_factura.cliente.direccion,
               'cp':_factura.cliente.cp,
               'localidad':_factura.cliente.ciudad,
               'provincia':_factura.cliente.provincia,
               'pais':_factura.cliente.pais,
               'telf':_factura.cliente.telefono,
               'fax':'',
               'direccionf':_factura.cliente.direccionfacturacion,
               'cpf':_factura.cliente.cpfacturacion,
               'localidadf':_factura.cliente.ciudadfacturacion,
               'provinciaf':_factura.cliente.provinciafacturacion,
               'paisf':_factura.cliente.paisfacturacion}
    numpeds = get_str_pedidos_albaranes(_factura)

    factdata = {'facnum':_factura.numfactura,
        'fecha':utils.str_fecha(_factura.fecha),
        'pedido':numpeds,
        'albaranes':'',
        'observaciones': _factura.observaciones}
    lineas = []
    for l in _factura.lineasDeVenta:
        linea = {'codigo':l.productoVenta.codigo,
            'cantidad':l.cantidad,
            'descripcion':l.productoVenta.descripcion,
            'precio': l.precio,
            'descuento':str(l.descuento)}
        lineas.append(linea)
    if _factura.cliente.pais.upper().replace(' ', '') != 'ESPAÑA':
        arancel_lista = [ldv.productoVenta.arancel
                         for ldv in _factura.lineasDeVenta
                         if ldv.productoVenta.arancel != ""
                             and ldv.productoVenta.arancel != None]
        # OJO: NOTA: El arancel es siempre el mismo. Muestro el del primer
        # articulo que encuentre con arancel != "".
        if arancel_lista != []:
            arancel = arancel_lista[0]
        else:
            arancel = None
    else:
        arancel = None
    for l in _factura.servicios:
        descripcion = l.concepto
        linea = {'codigo': "",
                 'cantidad': l.cantidad,
                 'descripcion': descripcion,
                 'precio': l.precio,
                 'descuento': str(l.descuento)}
        lineas.append(linea)
    fechasVencimiento = (', '.join([utils.str_fecha(v.fecha)
                                    for v in _factura.vencimientosCobro]))
    vencimiento = {'fecha':fechasVencimiento,
                   'pago':_factura.cliente.vencimientos,
                   'documento':_factura.cliente.documentodepago}
    from formularios import numerals
    total = "1.234.567,89 €"
    total = total.replace('€', '')
    total = total.replace(' ', '')
    totalfra = utils._float(total)  # Si ya lo tengo aquí calculado... ¿para
                                    # qué volver a hacerlo?
    totales = {}
    totales['subtotal'] = "123.456,78 €"
    cargo = "123 €"
    if cargo == '0.00 €':
        cargo = None
    totales['cargo'] = cargo
    descuento = "-0.00 €"
    if descuento == '-0.00 €':
        descuento = None
    else:
        descuento = descuento+' ( 13% )'
    totales['descuento'] = descuento
    totales['iva'] = " 16 "
    totales['totaliva'] = "123.4 €"
    totales['total'] = "12.345.678,09 €"
    texto = numerals.numerals(totalfra, moneda = "euros",
                              fraccion = "céntimos").upper()
    impuesto = None  # @UnusedVariable
    nomarchivo = factura(cliente, factdata, lineas, arancel, vencimiento,
                         texto, totales)
    from formularios.reports import abrir_pdf
    abrir_pdf(nomarchivo)

def pruebines_bibales():
    from formularios.reports import abrir_pdf
    abrir_pdf(etiquetasBigbags(pclases.Bigbag.select()[:2]))
    return

def pruebines2():
    from formularios.reports import abrir_pdf
    producto = pclases.ProductoVenta.select(
        pclases.ProductoVenta.q.camposEspecificosRolloID != None)[-2]
    campos = producto.camposEspecificosRollo
    r = producto.articulos[0].rollo
    elemento = {'descripcion': producto.nombre,
                'densidad':str(campos.gramos),
                'ancho':str(campos.ancho),
                'peso':str(int((
                    campos.ancho*campos.metrosLineales*campos.gramos/1000)
                    +campos.pesoEmbalaje)),
                'm2':str(campos.ancho*campos.metrosLineales),
                'mlin':str(campos.metrosLineales),
                'nrollo':str(r.numrollo),
                'partida':str(r.partida.numpartida),
                'codigo': producto.codigo,
                'codigo39': r.codigo, 
                'defectuoso': r.rollob}
    nomarchivo = etiquetasRollosEtiquetadora([elemento], True)
    abrir_pdf(nomarchivo)

def pruebines3():
    from formularios.reports import abrir_pdf
    from time import sleep

    abrir_pdf(carta_pago(pclases.PagarePago.select()[-1]))
    sleep(1)
    abrir_pdf(carta_pago(pclases.PagarePago.select()[-1], cheque = False))
    sleep(1)
    abrir_pdf(carta_pago(pclases.PagarePago.select()[-1], textofijo = False))
    sleep(1)
    abrir_pdf(carta_pago(pclases.PagarePago.select()[-1], cheque = False,
              textofijo = False))

def pruebines5():
    from formularios.reports import abrir_pdf

    #abrir_pdf(trazabilidad("Texto de trazabilidad de prueba."))
    abrir_pdf(generar_pdf_presupuesto(pclases.Presupuesto.select()[-1]))
    #abrir_pdf(informe_marcado_ce(pclases.ProductoVenta.get(102),
    #          pclases.ProductoVenta.get(102).get_partidas()[-5:]))

def probar_fuentes_disponibles():
    """
    Crea y abre un PDF con las fuentes disponibles en la
    instalación de ReportLab local.
    """
    from formularios.reports import abrir_pdf

    y = A4[1] - 3 * cm
    nomarchivo = os.path.join(gettempdir(), "muestrafuentes.pdf")
    c = canvas.Canvas(nomarchivo, pagesize = A4)
    i = 0
    for fuente in c.getAvailableFonts():
        c.drawString(3 * cm, y, '%d.- "%s":' % (i, fuente))
        y -= 0.75 * cm
        c.saveState()
        c.setFont(fuente, 14)
        c.drawString(4 * cm, y, "%s a 14." % (fuente))
        c.restoreState()
        y -= 0.75 * cm
        i += 1
    c.save()
    abrir_pdf(nomarchivo)

def pruebines4():
    from formularios.reports import abrir_pdf

    pclases.PagarePago.select()[-1]
    empresa = "Quadrophenia"
    contacto = "Pete Thownshend"
    fax = "959 66 69 99"
    telefono = "959 99 96 66"
    de = "Keith Moon"
    asunto = "Transferencia"
    fecha = "22/11/2006"
    beneficiario = "The Who"
    banco = "Brightonbank"
    cuenta = "1234567890-12-123456-789012"
    porcuenta = "My generation"
    ccc = "1234567890-09-87654321-09876"
    concepto = "The exodus is here"
    importe = "1.234,55 €"
    firmado = "D. Roger Daltrey y D. John Entwistle"

    abrir_pdf(fax_transferencia(empresa,
                                contacto,
                                fax,
                                telefono,
                                de,
                                asunto,
                                fecha,
                                beneficiario,
                                banco,
                                cuenta,
                                porcuenta,
                                ccc,
                                concepto,
                                importe,
                                firmado))

def pruebines6():
    from formularios.reports import abrir_pdf

    #abrir_pdf(trazabilidad("Texto de trazabilidad de prueba."))
    #abrir_pdf(generar_pdf_presupuesto(pclases.Presupuesto.select()[0]))
    abrir_pdf(recibo("1", "Brighton", "12.123,45 €", "31/12/2007",
                     "31/12/2007", "12345", "2007/TAL", "01/01/2007",
                     "Johnny Yen", "C/ Goser el goseriano",
                     "1234-1234-12-1234567890", "Iggy Pop",
                     "C/ Goser el destructor"))

def pruebines_nuevas_etiquetas_domenech():
    from formularios.listado_balas import preparar_datos_etiquetas_balas
    balas = [pclases.Bala.select(orderBy = "-id")[0]]
    balas = preparar_datos_etiquetas_balas(
        #pclases.Bala.select(orderBy = "-id")[:2])
        balas)
    from formularios.reports import abrir_pdf
    #import time
    #abrir_pdf(domenech_v_etiquetasBalasEtiquetadora(balas, "4", "2158"))
    #time.sleep(1)
    #abrir_pdf(domenech_v_etiquetasBalasEtiquetadora(balas))
    #abrir_pdf(domenech_h_etiquetasBalasEtiquetadora(balas, "4", "2158"))
    #time.sleep(1)
    abrir_pdf(domenech_h_etiquetasBalasEtiquetadora(balas))

def prueba_cmr():
    from formularios.reports import abrir_pdf
    abrir_pdf(cmr(pclases.AlbaranSalida.get(2216)))

def pruebines_pales_guaje():
    from formularios.reports import mandar_a_imprimir_con_ghostscript, abrir_pdf  # @UnusedImport
    pale = pclases.Pale.select(orderBy = "-id")[0]
    pale = [pale, pclases.Pale.select(orderBy = "id")[0]]
    for i in range(3):
        filetiqpale = generar_etiqueta_pale(pale, i)
        abrir_pdf(filetiqpale)
        #mandar_a_imprimir_con_ghostscript(filetiqpale)

def pruebines_cajas_guaje():
    from formularios.reports import mandar_a_imprimir_con_ghostscript, abrir_pdf  # @UnusedImport
    caja = pclases.Caja.select(orderBy = "-id")[0]
    caja = [caja, pclases.Caja.select(orderBy = "id")[0]]
    for i in range(3):
        filetiqcaja = generar_etiqueta_caja(caja, i)
        abrir_pdf(filetiqcaja)
        #mandar_a_imprimir_con_ghostscript(filetiqpale)

# XXX ------------------------------------------------------------------------


if __name__=='__main__':
    # consumoPartida(pclases.Partida.select(
    #   pclases.Partida.q.numpartida == 1148)[0])
    #pruebines2()
    # probar_fuentes_disponibles()
    #pruebines_nuevas_etiquetas_domenech()
    #pruebines5()
    #prueba_cmr()
    #pruebines_pales_guaje()
    #pruebines_cajas_guaje()
    pclases.VERBOSE = True
    print existencias_no_nulas()


