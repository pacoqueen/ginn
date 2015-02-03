#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2014  Francisco José Rodríguez Bogado,                   #
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


###################################################################
## utils.py
##  Algunas utilidades Project Manager Geotex-INN y 
##  Enterprise Resource Manager Geotexan.
###################################################################
## NOTAS:
## 
## ----------------------------------------------------------------
## 
###################################################################
## Changelog:
##  8 Julio 2005 -> Inicio
##  22 agosto 2005 -> Añadidos precarios diálogos de info, 
##                    entrada, sí-no, etc.
##  1 septiembre 2005 -> Añadidas utilidades GTK.
##  12 de diciembre de 2005 -> Utilidades de FTP y MD5 pasadas del
##                             lanzador a aquí.
##  25 de enero de 2005 -> Floats con 2 decimales en TreeViews.
###################################################################
## DONE:
## + Es imprescindible poder meter algún tipo de texto descriptivo
##   en las ventanas y ajustar correctamente el ancho de los 
##   diálogos de forma que quepa el título correctamente.
## + Retabular. Odio que se mezclen indentaciones de 2 y 4 espacios.
## + BUG: Por algún motivo, la búsqueda interactiva en preparar_*
##   no funciona. Siempre se queda como "buscable" la 1ª columna.
###################################################################
## - TODO: BUG: Inexplicablemente, al meter el data_func (creo que es por
##   eso) el sort_column deja de funcionar.
###################################################################

try:
    import pygtk
    pygtk.require('2.0')
    import gtk
    import gobject
except (ImportError, RuntimeError), msg:
    print "WARNING: No se pudo importar GTK/pyGTK. No se podrán usar funciones gráficas:\n%s" % (msg)
import mx.DateTime, os, time, datetime, re, string, sys
try:
    from formularios import nftp
except ImportError, msg:
    print "WARNING: No se pudo importar nftp. No se podrá usar FTP:\n%s" % (msg)
from fixedpoint import FixedPoint as Ffloat
from collections import defaultdict
import re
from lib.fuzzywuzzy.fuzzywuzzy import process as fuzzyprocess


def str_fechahoralarga(fechahora):
    """
    Devuelve el fechahora recibido como una cadena que 
    muestra la fecha y la hora.
    """
    return "%s %s" % (str_fecha(fechahora), str_hora(fechahora))

def str_fechahora(fechahora):
    """
    Devuelve el fechahora recibido como una cadena que 
    muestra la fecha y la hora.
    """
    return "%s %s" % (str_fecha(fechahora), str_hora_corta(fechahora))

def str_fecha(fecha = time.localtime()):
    """
    Devuelve como una cadena de texto en el formato dd/mm/aaaa
    la fecha pasada. 
    "fecha" debe ser de tipo time.struct_time, un
    mx.DateTime o bien una tupla [dd, mm, aaaa] como
    las que devuelve "mostrar_calendario".
    Si no se pasa ningún parámetro devuelve la fecha 
    del sistema.
    Si se pasa None, devuelve la cadena vacía ''.
    Si la fecha no es de ningún tipo de los permitidos
    saltará una excepción que debe ser atendida en 
    capas superiores de la pila de llamadas.
    """
    if not fecha:    # Si es None (valor por defecto en envios)
        return ''
    if isinstance(fecha, tuple):    # Es una fecha de mostrar_calendario y ya viene ordenada
        t = fecha
    else:
        if isinstance(fecha, type(mx.DateTime.DateTimeFrom(''))):
            tuplafecha = fecha.tuple()
        elif isinstance(fecha, time.struct_time):
            tuplafecha = fecha
        elif isinstance(fecha, datetime.date):
            tuplafecha = fecha.timetuple()
        else:    # No es ni mx ni time ni None ni tupla ni nada de nada
            return None 
        t = list(tuplafecha)[2::-1]
    # Aquí ya tengo una lista [m, d, aa] o [mm, dd, aaaa]
    t = map(str, ['%02d' % i for i in t])    # "Miaque" soy rebuscado a veces. Con lo fácil que tiene que ser esto.
    t = '/'.join(t)
    return t

def str_hora(fh):
    """
    Devuelve la parte de la hora de una fecha
    completa (fecha + hora, DateTime).
    """
    try:
        return "%02d:%02d:%02d" % (fh.hour, fh.minute, fh.second)
    except:     # Por si es un datetime
        try:
            fh = mx.DateTime.DateTimeDeltaFrom(seconds = fh.total_seconds())
            return "%02d:%02d:%02d" % (fh.hour, fh.minute, fh.second)
        except:
            return ''

def str_hora_corta(fh):
    """
    Devuelve la parte de la hora de una fecha
    completa (fecha + hora, DateTime).
    """
    try:
        return "%02d:%02d" % (fh.hour, fh.minute)
    except:     # Por si es un datetime
        try:
            fh = mx.DateTime.DateTimeDeltaFrom(seconds = fh.total_seconds())
            return "%02d:%02d" % (fh.hour, fh.minute)
        except:
            return ''

def respuesta_si_no(dialog, response, res):
    res[0] = response == gtk.RESPONSE_YES

def respuesta_si_no_cancel(dialog, response, res):
    if response == gtk.RESPONSE_YES:
        res[0] = True
    elif response == gtk.RESPONSE_NO:
        res[0] = False
    else:
        res[0] = response

def parse_porcentaje(strfloat, fraccion = False):
    """
    Recibe un porcentaje como cadena. Puede incluir el un espacio,
    el signo menos (-) y el porciento (%).
    La función procesa la cadena y devuelve un flotante que se 
    corresponde con el valor del porcentaje como fracción de 1, es decir, 
    en la forma 10 % = 0.1, si «fracción» es True.
    En otro caso devuelve el valor numérico sin más una vez filtrado el 
    símbolo "%".
    """
    res = strfloat.replace('%', '')
    res = res.replace(',', '.')
    res = res.strip()
    try:
        res = _float(res)
    except ValueError, msg:
        res = 0.0
        #utils.dialogo('El número no se puede interpretar.')
        raise ValueError, "%s: El número %s no se puede interpretar como porcentaje." % (msg, strfloat)
    if fraccion:
        res /= 100.0
    return res

def dialogo(texto = '', 
            titulo = '', 
            padre = None, 
            icono = None, 
            cancelar = False, 
            defecto = None, 
            tiempo = None, 
            recordar = False, 
            res_recordar = [False], 
            bloq_temp = []):
    """
    Muestra un diálogo SI/NO.
    Devuelve True si se pulsó SI y False si no.
    OJO: Aquí va primero el texto y después el título para
    guardar la compatibilidad con el código del resto de 
    módulos ya escritos. En el resto de utils el titulo 
    es el primer parámetro.
    Si icon tiene algo != None (debe ser un gtk.STOCK_algo)
    se agrega un icono a la izquierda del texto.
    Si cancelar != False, se añade un botón cancelar que 
    devuelve gtk.RESPONSE_CANCEL cuando se pulsa.
    Si «recordar» es True muestra un checkbox de "No volver a preguntar" que 
    por defecto está a «res_recordar», donde guarda el valor final del 
    checkbox al pulsar Aceptar.
    bloq_temp es una lista de botones que se deshabilitarán durante 3 
    segundos para evitar que al usuario-cowboy se le vaya la mano y forzarlo 
    a leer el texto antes de que haga algo "peligroso" sin querer (al estilo 
    Firefox para instalaciones de plugins y demás). 
    La lista debe contener cadenas de texto de los botones que se desean 
    deshabilitar de manera análoga a como se recibe la respuesta por defecto.
    """
    ## HACK: Los enteros son inmutables, usaré una lista
    res = [None]
    if cancelar:
        de = gtk.Dialog(titulo,
                        padre,
                        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                        (gtk.STOCK_YES, gtk.RESPONSE_YES,
                        gtk.STOCK_NO, gtk.RESPONSE_NO,
                        gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        de.connect("response", respuesta_si_no_cancel, res)
    else: 
        de = gtk.Dialog(titulo,
                        padre,
                        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                        (gtk.STOCK_YES, gtk.RESPONSE_YES,
                        gtk.STOCK_NO, gtk.RESPONSE_NO))
        de.connect("response", respuesta_si_no, res)
    response_defecto = gtk.RESPONSE_YES
    if defecto != None:
        if defecto in ("cancelar", "cancel", "CANCELAR", "CANCEL", 
                       gtk.RESPONSE_CANCEL):
            de.set_default_response(gtk.RESPONSE_CANCEL)
            response_defecto = gtk.RESPONSE_CANCEL
        elif defecto in ("no", "No", "NO", False, gtk.RESPONSE_NO):
            de.set_default_response(gtk.RESPONSE_NO)
            response_defecto = gtk.RESPONSE_NO
        elif defecto in ("si", "Si", "SI", True, gtk.RESPONSE_YES, "yes", 
                         "Yes", "YES", "sí", "Sí", "SÍ"):
            de.set_default_response(gtk.RESPONSE_YES)
            response_defecto = gtk.RESPONSE_YES
    de.response_defecto = response_defecto # I love this dynamic shit!
    txt = gtk.Label("\n    %s    \n" % texto)
    if icono == None:
        icono = gtk.STOCK_DIALOG_QUESTION
    pixbuf = de.render_icon(icono, gtk.ICON_SIZE_MENU)
    de.set_icon(pixbuf)
    imagen = gtk.Image()
    imagen.set_from_stock(icono, gtk.ICON_SIZE_DIALOG)
    hbox = gtk.HBox(spacing = 5)
    hbox.pack_start(imagen)
    hbox.pack_start(txt)
    de.vbox.pack_start(hbox)
    de.vbox.show_all()
    de.set_transient_for(padre)
    de.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
    # XXX: Checkbox de no volver a preguntar.
    if recordar:
        txtrecordar = "_Recordar mi respuesta y no volver a preguntar."
        chrecordar = gtk.CheckButton(txtrecordar)
        chrecordar.set_active(bool(res_recordar and res_recordar[0] or False))
        chrecordar.set_property("can-default", False)
        chrecordar.set_property("can-focus", False)
        de.vbox.add(chrecordar)
        chrecordar.show()
        def guardar_recordar(cb, res_recordar):
            try:
                res_recordar[0] = cb.get_active()
            except IndexError:
                res_recordar.append(cb.get_active())
        chrecordar.connect("toggled", guardar_recordar, res_recordar)
    # XXX
    # XXX: Tiempo por defecto:
    if tiempo != None:
        tiempo_restante = [tiempo]   # Enteros son inmutables, uso una 
            # lista para poder cambiar el valor dentro del callback.
        label_tiempo = gtk.Label("<small><i>La opción por defecto será aplicada en %d segundos.</i></small>" % tiempo_restante[0])
        label_tiempo.set_use_markup(True)
        def actualizar_tiempo_restante(label, dialogo, tiempo, 
                                       response_defecto):
            tiempo[0] -= 1
            label_tiempo.set_text("<small><i>La opción por defecto será aplicada en %d segundos.</i></small>" % tiempo[0])
            label_tiempo.set_use_markup(True)
            if tiempo[0] <= 0:
                de.response(response_defecto)
            return tiempo[0] > 0
        de.vbox.add(label_tiempo)
        label_tiempo.show()
        gobject.timeout_add(1000, actualizar_tiempo_restante, label_tiempo, 
                            de, tiempo_restante, response_defecto, 
                            priority = gobject.PRIORITY_HIGH)
    # XXX
    # XXX: Bloqueo temporal de botones:
    if bloq_temp:
        # 0.- Diccionario de botones
        area = de.action_area
        pares = zip(("sí", "no", "cancelar"), 
                    area.get_children()[::-1])   # Siempre mismo orden.
        dbotones = dict(pares)
    for strb in bloq_temp:
        # 1.- Determinar a qué botón se refiere:
        if strb in ("cancelar", "cancel", "CANCELAR", "CANCEL", 
                       gtk.RESPONSE_CANCEL):
            try:
                boton = dbotones["cancelar"]
            except KeyError:
                continue # No hay botón de cancelar.
        elif strb in ("no", "No", "NO", False, gtk.RESPONSE_NO):
            boton = dbotones["no"]
        elif strb in ("si", "Si", "SI", True, gtk.RESPONSE_YES, "yes", 
                         "Yes", "YES", "sí", "Sí", "SÍ"):
            boton = dbotones["sí"]
        else:
            continue
        # 2.- Instalo la cuenta atrás.
        boton.set_sensitive(False)
        tiempo_restante = [3]   # Enteros son inmutables, uso una 
            # lista para poder cambiar el valor dentro del callback.
        label = boton.get_children()[0].get_child().get_children()[1]
        str_label = label.get_text()
        if "(" in str_label:
            str_label = str_label.split("(")[0][:-1]
        strtiempo = str_label + "<small> (%d)</small>" % tiempo_restante[0]
        label.set_text(strtiempo)
        label.set_use_markup(True)
        def actualizar_tiempo_restante(boton, tiempo, dialogo, botones):
            tiempo[0] -= 1
            boton.set_sensitive(tiempo[0] <= 0)
            try:
                label = boton.get_children()[0].get_child().get_children()[1]
            except IndexError:  # El diálogo se ha cerrado ya.
                return False
            str_label = label.get_text()
            if "(" in str_label:
                str_label = str_label.split("(")[0][:-1]
            if tiempo[0] > 0:
                strtiempo = str_label + "<small> (%d)</small>" % tiempo[0]
            else:
                strtiempo = str_label
                if dialogo.response_defecto == gtk.RESPONSE_YES:
                    dbotones["sí"].grab_focus()
                elif dialogo.response_defecto == gtk.RESPONSE_NO:
                    dbotones["no"].grab_focus()
                elif dialogo.response_defecto == gtk.RESPONSE_CANCEL:
                    dbotones["cancelar"].grab_focus()
            label.set_text(strtiempo)
            label.set_use_markup(True)
            return tiempo[0] > 0
        gobject.timeout_add(1000, actualizar_tiempo_restante, 
                            boton, tiempo_restante, de, dbotones, 
                            priority = gobject.PRIORITY_HIGH)
    # XXX
    de.run()
    de.destroy()
    return res[0]

def respuesta_ok_cancel(dialog, response, res):
    if response == gtk.RESPONSE_OK:
        try:
            res[0] = dialog.vbox.get_children()[1].get_text()
        except:
            buf = dialog.vbox.get_children()[1].get_buffer()
            res[0] = buf.get_text(buf.get_start_iter(), buf.get_end_iter())
    else:
        res[0] = False

def set_unset_urgency_hint(window, activar_hint):
    if gtk.gtk_version >= (2, 8, 0) and gtk.pygtk_version >= (2, 8, 0):
        if activar_hint > 0:
            window.props.urgency_hint = True
        else:
            window.props.urgency_hint = False

def dialogo_info(titulo='', texto='', padre=None):
    """
    Muestra un diálogo simple de información, con un único
    botón de aceptación.
    OJO: Al loro. Si el título de la ventana es "ACTUALIZAR" no 
    se muestra. En cambio se activa el hint que hace parpadear
    la ventana padre. El urgency_hint se desactivará cuando
    pulse en Actualizar o en Guardar (es decir, cuando se 
    invoque actualizar_ventana). NOTA: Esto se hace aquí para
    evitar cambiar una por una las docenas de ventanas de diálogo 
    de actualización que hay repartidas por cada formulario.
    """
    if titulo == "ACTUALIZAR":
        if padre != None:
            set_unset_urgency_hint(padre, True)
    else:
        dialog = gtk.Dialog(titulo,
                            padre,
                            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        info = gtk.Label("\n    %s    \n" % texto)
        hbox = gtk.HBox(spacing = 5)
        icono = gtk.Image()
        icono.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_DIALOG)
        hbox.pack_start(icono)
        hbox.pack_start(info)
        dialog.vbox.pack_start(hbox)
        hbox.show_all()
        dialog.set_transient_for(padre)
        dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        dialog.run()
        dialog.destroy()

def dialogo_entrada(texto= '', 
                    titulo = 'ENTRADA DE DATOS', 
                    valor_por_defecto = '', 
                    padre = None, 
                    pwd = False, 
                    modal = True, 
                    textview = False, 
                    opciones = {}, 
                    hide_entry = False):
    """
    Muestra un diálogo modal con un textbox.
    Devuelve el texto introducido o None si se
    pulsó Cancelar.
    valor_por_defecto debe ser un string.
    Si pwd == True, es un diálogo para pedir contraseña
    y ocultará lo que se introduzca.
    Si textview es True usa un TextView en lugar de un TextEntry.
    opciones: Se añadirán tantos checkboxes a la ventana como elementos 
              se reciban en este parámetros. Cada clave será el texto a usar 
              en los checkboxes y los valores serán los valores por defecto. 
              En ese mismo diccionario se almacenarán los valores 
              seleccionados en el diálogo tras darle a Aceptar.
    """
    if not isinstance(valor_por_defecto, str):
        valor_por_defecto = str(valor_por_defecto)
    ## HACK: Los enteros son inmutables, usaré una lista
    res = [None]
    if modal:
        de = gtk.Dialog(titulo,
                        padre,
                        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                        (gtk.STOCK_OK, gtk.RESPONSE_OK,
                         gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
    else:
        de = gtk.Dialog(titulo,
                        padre,
                        gtk.DIALOG_DESTROY_WITH_PARENT,
                        (gtk.STOCK_OK, gtk.RESPONSE_OK,
                         gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
    de.connect("response", respuesta_ok_cancel, res)
    txt = gtk.Label("\n    %s    \n" % texto)
    txt.set_use_markup(True)
    hbox = gtk.HBox(spacing = 5)
    icono = gtk.Image()
    icono.set_from_stock(gtk.STOCK_DIALOG_QUESTION, gtk.ICON_SIZE_DIALOG)
    hbox.pack_start(icono)
    hbox.pack_start(txt)
    de.vbox.pack_start(hbox)
    vboxopciones = gtk.VBox()
    #------------------------------------------------------------------------#
    def set_opcion(cb, claveopcion, opciones):                               #
        opciones[claveopcion] = cb.get_active()                              #
    #------------------------------------------------------------------------#
    for txtopcion in opciones:
        chbox = gtk.CheckButton(txtopcion)
        chbox.set_active(opciones[txtopcion])
        chbox.connect("toggled", set_opcion, txtopcion, opciones)
        vboxopciones.add(chbox)
    vboxopciones.show_all()
    de.vbox.pack_end(vboxopciones)
    hbox.show_all()
    if not textview:
        inpute = gtk.Entry()
        inpute.set_visibility(not pwd)
        #-----------------------------------------------------------#
        def pasar_foco(widget, event):                              #
            if event.keyval == 65293 or event.keyval == 65421:      #
                de.action_area.get_children()[1].grab_focus()       #
        #-----------------------------------------------------------#
        inpute.connect("key_press_event", pasar_foco)
    else:
        inpute = gtk.TextView()
    de.vbox.pack_start(inpute)
    inpute.show()
    if not textview:
        inpute.set_text(valor_por_defecto)
    else:
        inpute.get_buffer().set_text(valor_por_defecto)
    if len(titulo)<20:
        width = 100
    elif len(titulo)<60:
        width = len(titulo)*10
    else:
        width = 600
    de.resize(width, 80)
    de.set_transient_for(padre)
    de.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
    inpute.set_property("visible", not hide_entry)
    de.run()
    de.destroy()
    if res[0]==False:
        return None
    return res[0]

def dialogo_combo(titulo='Seleccione una opción', 
                  texto='', 
                  ops=[(0, 'Sin opciones')], 
                  padre=None, 
                  valor_por_defecto = None):
    """
    Muestra un diálogo modal con un combobox con las opciones
    pasadas.
    Las opciones deben ser (int, str)
    Devuelve el elemento seleccionado[0] -el entero de la 
    opción- o None si se cancela.
    Si valor_por_defecto != None, debe ser un entero de la lista.
    """
    ## HACK: Los enteros son inmutables, usaré una lista
    res = [None]
    de = gtk.Dialog(titulo,
                    padre,
                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                    (gtk.STOCK_OK, gtk.RESPONSE_OK,
                     gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
    #-------------------------------------------------------------------#
    def respuesta_ok_cancel_combo(dialog, response, res):               #
        if response == gtk.RESPONSE_OK:                                 #
            res[0] = combo_get_value(dialog.vbox.get_children()[1])     #
        else:                                                           #
            res[0] = False                                              #
    #-------------------------------------------------------------------#
    def pasar_foco(completion, model, itr):                            #
        de.action_area.get_children()[1].grab_focus()                   #
    #-------------------------------------------------------------------#
    de.connect("response", respuesta_ok_cancel_combo, res)
    txt = gtk.Label("\n    %s    \n" % texto)
    combo = gtk.ComboBoxEntry()
    rellenar_lista(combo, ops)
    if valor_por_defecto != None and isinstance(valor_por_defecto, int) and valor_por_defecto in [o[0] for o in ops]:
        model = combo.get_model()
        itr = model.get_iter_first()
        while (itr != None and 
               model[model.get_path(itr)][0] != valor_por_defecto):
            itr = model.iter_next(itr)
        combo.set_active_iter(itr)
    input_combo = combo.child.get_completion()
    input_combo.connect("match_selected", pasar_foco)
    hbox = gtk.HBox(spacing = 5)
    icono = gtk.Image()
    icono.set_from_stock(gtk.STOCK_DIALOG_QUESTION, gtk.ICON_SIZE_DIALOG)
    hbox.pack_start(icono)
    hbox.pack_start(txt)
    hbox.show_all()
    de.vbox.pack_start(hbox)
    combo.show()
    de.vbox.pack_start(combo)
    de.set_transient_for(padre)
    de.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
    de.run()
    de.destroy()
    if res[0] is False:
        res = None
    else:
        res = res[0]
    return res

def dialogo_radio(titulo='Seleccione una opción', 
                  texto='', 
                  ops=[(0, 'Sin opciones')], 
                  padre=None, 
                  valor_por_defecto = None):
    """
    Muestra un diálogo modal con un grupo de radiobuttons con las opciones 
    pasadas.
    Las opciones deben ser (int, str)
    Devuelve el elemento seleccionado[0] -el entero de la 
    opción- o None si se cancela.
    Si valor_por_defecto != None, debe ser un entero de la lista.
    """
    ## HACK: Los enteros son inmutables, usaré una lista
    res = [None]
    de = gtk.Dialog(titulo,
                    padre,
                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                    (gtk.STOCK_OK, gtk.RESPONSE_OK,
                     gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
    #-------------------------------------------------------------------#
    def respuesta_ok_cancel_radio(dialog, response, res, dicseleccion):
        res[0] = False
        if response == gtk.RESPONSE_OK:
            for numop in dicseleccion:
                if dicseleccion[numop].get_active():
                    res[0] = numop
                    break
    #-------------------------------------------------------------------#
    txt = gtk.Label("\n    %s    \n" % texto)
    vradio = gtk.VBox()
    dicseleccion = {}
    grupo = None
    for numop, txtop in ops:
        rb = gtk.RadioButton(grupo, label = txtop)
        if grupo == None:
            grupo = rb
        vradio.add(rb)
        dicseleccion[numop] = rb
    if (valor_por_defecto != None 
        and isinstance(valor_por_defecto, int) 
        and valor_por_defecto in [o[0] for o in ops]):
        dicseleccion[valor_por_defecto].set_active(True)
    de.connect("response", respuesta_ok_cancel_radio, res, dicseleccion)
    hbox = gtk.HBox(spacing = 5)
    icono = gtk.Image()
    icono.set_from_stock(gtk.STOCK_DIALOG_QUESTION, gtk.ICON_SIZE_DIALOG)
    hbox.pack_start(icono)
    hbox.pack_start(txt)
    hbox.show_all()
    de.vbox.pack_start(hbox)
    vradio.show_all()
    de.vbox.pack_start(vradio)
    de.set_transient_for(padre)
    de.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
    de.run()
    de.destroy()
    if res[0] is False:
        res = None
    else:
        res = res[0]
    return res

def dialogo_checks(titulo='SELECCIONE OPCIONES', 
                   texto='Seleccione una o varias opciones', 
                   ops=[], 
                   padre=None, 
                   valor_por_defecto = None):
    """
    Muestra un diálogo modal con un grupo de checkbuttons con las opciones 
    pasadas.
    Las opciones deben ser una lista de tuplas con dos posiciones: 
    (int/str, str). La primera se usará como "índice" a devolver. La segunda 
    se mostrará en su check de la ventana.
    Devuelve una lista de elementos seleccionados[0] -el entero de cada
    opción- o None si se cancela. La lista vacía será la respuesta cuando 
    acepte pero no seleccione ninguna opción.
    Si valor_por_defecto != None, debe ser una lista de enteros 
    correspondientes a los primeros índices de la lista de opciones.
    """
    res = []
    de = gtk.Dialog(titulo,
                    padre,
                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                    (gtk.STOCK_OK, gtk.RESPONSE_OK,
                     gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
    #-------------------------------------------------------------------#
    def respuesta_ok_cancel_check(dialog, response, res, dicseleccion):
        if response == gtk.RESPONSE_OK:
            for numop in dicseleccion:
                if dicseleccion[numop].get_active():
                    res.append(numop)
    #-------------------------------------------------------------------#
    txt = gtk.Label("\n    %s    \n" % texto)
    vchecks = gtk.VBox()
    dicseleccion = {}
    for numop, txtop in ops:
        ch = gtk.CheckButton(label = txtop)
        ch.set_active(numop in valor_por_defecto)
        ch.set_tooltip_markup("<tt>%s</tt>" % (numop))
        vchecks.add(ch)
        dicseleccion[numop] = ch
    de.connect("response", respuesta_ok_cancel_check, res, dicseleccion)
    hbox = gtk.HBox(spacing = 5)
    icono = gtk.Image()
    icono.set_from_stock(gtk.STOCK_DIALOG_QUESTION, gtk.ICON_SIZE_DIALOG)
    hbox.pack_start(icono)
    hbox.pack_start(txt)
    hbox.show_all()
    de.vbox.pack_start(hbox)
    vchecks.show_all()
    de.vbox.pack_start(vchecks)
    de.set_transient_for(padre)
    de.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
    response = de.run()
    de.destroy()
    if response == gtk.RESPONSE_CANCEL:
        res = False
    return res

def dialogo_entrada_combo(titulo='Seleccione una opción', 
                          texto='', 
                          ops=[(0, 'Sin opciones')], 
                          padre=None, 
                          valor_por_defecto = None):
    """
    Muestra un diálogo modal con un combobox con las opciones
    pasadas.
    Las opciones deben ser (int, str)
    Devuelve el par seleccionado de las opciones, (None, None) si
    se cancela o (None, "texto escrito") si se ha tecleado algo
    que no está en las opciones y se ha pulsado Aceptar.
    Si valor_por_defecto != None, debe ser un entero de la lista.
    """
    ## HACK: Los enteros son inmutables, usaré una lista
    res = [None, None]
    de = gtk.Dialog(titulo,
                    padre,
                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                    (gtk.STOCK_OK, gtk.RESPONSE_OK,
                     gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
    #-------------------------------------------------------------------#
    def respuesta_ok_cancel_combo(dialog, response, res):
        if response == gtk.RESPONSE_OK:
            combo = dialog.vbox.get_children()[1]
            res[0] = combo_get_value(combo)
            res[1] = combo.child.get_text()
        else:
            res[0] = False
            res[1] = None
    #-------------------------------------------------------------------#
    def pasar_foco(completion, model, itr):                            #
        de.action_area.get_children()[1].grab_focus()                   #
    #-------------------------------------------------------------------#
    de.connect("response", respuesta_ok_cancel_combo, res)
    txt = gtk.Label("\n    %s    \n" % texto)
    combo = gtk.ComboBoxEntry()
    rellenar_lista(combo, ops)
    if valor_por_defecto != None \
       and isinstance(valor_por_defecto, int) \
       and valor_por_defecto in [o[0] for o in ops]:
        model = combo.get_model()
        itr = model.get_iter_first()
        while itr != None \
              and model[model.get_path(itr)][0] != valor_por_defecto:
            itr = model.iter_next()
        combo.set_active_iter(itr)
    inpute = combo.child.get_completion()
    inpute.connect("match_selected", pasar_foco)
    hbox = gtk.HBox(spacing = 5)
    icono = gtk.Image()
    icono.set_from_stock(gtk.STOCK_DIALOG_QUESTION, gtk.ICON_SIZE_DIALOG)
    hbox.pack_start(icono)
    hbox.pack_start(txt)
    hbox.show_all()
    de.vbox.pack_start(hbox)
    combo.show()
    de.vbox.pack_start(combo)
    de.set_transient_for(padre)
    de.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
    de.run()
    de.destroy()
    if res[0] is False:
        res[0] = None
    return res

def escribir_barra_estado(wid, texto, logger = None, txt_log = ""):
    """
    Escribe el texto "texto" en la barra de estado "wid".
    Los parámetros adicionales "logger" y "txt_log" son un 
    objeto para volcar a log y un texto adicional. Típicamente el 
    texto adicional incluye información acerca del usuario 
    que ha hecho «login» en el sistema y "logger" vendrá heredado 
    e instanciado desde la clase Ventana y Autenticación 
    respectivamente.
    """
    texto = eliminar_dobles_espacios(texto)
    wid.push(wid.get_context_id(texto), texto)
    if logger != None:
        try:
            if "error" in txt_log.lower():
                logger.error("%s: %s" % (txt_log, texto))
            else:
                logger.warning("%s: %s" % (txt_log, texto))
        except IOError:
            pass    # El fichero de log se ha cerrado por algún motivo. Mutis 
                    # por el foro.

def tipo_gobject(valor):
    """
    A partir de un valor devuelve el tipo correspondiente
    según las constantes gobject.
    El tipo lo devuelve como cadena para poder montar el
    model a partir de un eval del constructor. (No hay
    forma de añadir columnas una vez el constructor del 
    ListStore ha sido llamado, así que no veo otra 
    manera de hacerlo que no sea con un eval y cadenas).
    """
    tipo = "gobject.TYPE_STRING"
    # En el peor de los casos, devuelvo un tipo cadena. Todo se puede representar con cadenas.
    if isinstance(valor, bool):     # Esto primero, porque da la casualidad de que bool es subclase de int.
        tipo = 'gobject.TYPE_BOOLEAN'
    elif isinstance(valor, int):
        #return 'gobject.TYPE_INT64'    #Ya tengo (mala) experiencia en enteros que se me pasan de rango. Me curo en salud.
        tipo = 'gobject.TYPE_STRING'    # Hay veces que la primera fila es entero, en el model se crea como entero y en 
            # alguna fila posterior me viene un float o una cadena vacía. Para que no falle, devuelvo tipo cadena para 
            # que construya el model. Cualquier cosa "entra" bien en un tipo cadena.
    elif isinstance(valor, str):
        tipo = 'gobject.TYPE_STRING'
    elif isinstance(valor, type(None)):
        tipo = 'gobject.TYPE_NONE'
    elif isinstance(valor, float):
        # return 'gobject.TYPE_FLOAT'
        tipo = 'gobject.TYPE_DOUBLE'    # Tiene más precisión. Acuérdate del caso 39672.83
    return tipo

def el_reparador_magico_de_representacion_de_flotantes_de_doraemon(filas):
    ## HACK:
    # El render usa el método __repr__ para escribir los floats en la celda.
    # Esto tiene un problema: 100.35.__repr__() devuelve 100.3499999... debido
    # a la representación interna del punto flotante <i>iecubo-sietecincocuatro</i>
    # etcétera, etcétera.
    # Al hacerle un print, operar y todas esas cosas se comporta perfectamente,
    # pero al pasar por el render, se pinta 100.349999... Eso yo lo puedo 
    # entender; pero dile a mi cliente que es por el estándar de representación
    # binaria de los flotantes, a ver dónde te manda.
    # TOTAL: Que los voy a pasar a string antes de mostrarlos, que así sí se 
    # ven correctamente: (Otra cosa curiosa que tengo que mirar a fondo
    # porque no me cuadra. ¿Por qué `0.3`!=str(0.3)? ¿Tiene algo que ver con
    # el Frente Popular de Judea y el Frente Judaico Popular?
    # ...
    # Ok, una explicación convincente de las dos formas de comportarse está
    # aquí: file:///usr/share/doc/python2.3/html/tut/node15.html
    for f in xrange(len(filas)):
        fila = list(filas[f])
        filas[f] = fila
        # OJO porque filas debe ser una lista, si no, no aceptará la asignación.
        for c in xrange(len(fila)):
            item = fila[c]
            if item == None:  
                # Voy a aprovechar el invento para quitarme los None 
                # de encima, que tampoco acaban de sentarle bien al TreeView.
                fila[c] = ''
            elif isinstance(item, float):
                #fila[c] = str(round(item, 2))
                fila[c] = float2str(item)

def construir_modelo(filas, cabeceras = None):
    """
    Devuelve un modelo listo para ser usado en un TreeView a
    partir de las filas recibidas.
    """
    try:
        fila = filas[0]
        tipos = []
        for col in fila: 
            tipos.append(tipo_gobject(col))
        model = eval('gtk.ListStore(%s)' % ','.join(tipos))
    except IndexError:     # No hay resultados
        # Pongo el modelo por defecto que he estado usando hasta ahora con 
        # el número de columnas de la cabecera si ésta no es None.
        if not cabeceras:
            model = gtk.ListStore(gobject.TYPE_INT64, 
                                  gobject.TYPE_STRING, 
                                  gobject.TYPE_STRING)
        else:
            tipos = [gobject.TYPE_INT64] + \
                    ([gobject.TYPE_STRING] * (len(cabeceras) - 1))
            model = gtk.ListStore(*tipos)
    except TypeError, ex:   # ¡No hay filas! (filas es None o no es una 
                            # lista/tupla
        print "ERROR Diálogo resultados (utils.py):", ex
        return -2           # No puedo hacer nada. Cierro la ventana.
    return model
    
def definir_columnas(filas, cabeceras):
    """
    A partir de las filas devuelve una lista
    de columnas adecuadas para usar en un 
    TreeView. Cada columna llevará como 
    cabecera el ítem correspondiente de la
    lista de cabeceras.
    """
    columns = []
    # Uso la primera fila como referencia para el número de columnas
    try:
        n_columnas = len(filas[0])
    except TypeError: #len() of unsized object
        n_columnas = len(cabeceras)
        # cabeceras al menos tendrá 3 elementos a no ser que se especifique
        # lo contrario, en cuyo caso imagino que tendré las luces suficientes
        # como para no intentar mostrar un diálogo de resultados sin columnas.
    except IndexError: #Índice fuera de rango. No hay filas[0]
        n_columnas = len(cabeceras)
    for i in xrange(n_columnas):
        try:
            columns.append(gtk.TreeViewColumn(cabeceras[i]))
        except IndexError:
            columns.append(gtk.TreeViewColumn(''))
    return columns

def cambiar_columna_busqueda(treeviewcolumn, tabla): 
    """
    Cambia la columna de búsqueda interactiva del TreeView "tabla" a 
    la columna TreeViewColumn recibida.
    """
    cols = tabla.get_columns()
    numcols = len(cols)
    numcolumn = 0
    col = tabla.get_column(0)
    while numcolumn < numcols and col != treeviewcolumn:
        numcolumn += 1
        col = tabla.get_column(numcolumn)
    tabla.set_search_column(numcolumn)

def construir_tabla(titulo, padre, filas, cabeceras):
    """
    A partir de los datos que recibe el dialogo_resultado
    construye la tabla y el contenedor y los devuelve.
    Si las filas son incorrectas, devuelve -2 tal y como 
    se especifica en la función invocadora.
    """
    ## ------------ Construyo el diálogo:
    de = gtk.Dialog(titulo,
                    padre,
                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                    (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                     gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
    ## ------------ Construyo el model: (patrón MVC)
    model = construir_modelo(filas, cabeceras)
    if model == -2: 
        return -2, None, None
    ## ------------ Añado datos al model (capa "modelo")
    for f in filas:
        try:
            model.append(f)
        except TypeError, msg:
            print "utils.py::construir_tabla -> model.append(%s): TypeError: %s" % (f, msg)
    tabla = gtk.TreeView(model)
    ## ------------ ScrolledWindow:
    contenedor = gtk.ScrolledWindow()
    contenedor.add(tabla)
    ## ------------ Defino las columnas de la capa "vista"
    columns = definir_columnas(filas, cabeceras)
    ## ------------ Añado las columnas a la tabla:
    for c in columns:
        tabla.append_column(c)
        c.connect("clicked", cambiar_columna_busqueda, tabla)
    ## ------------ Creo los "renders" para las celdas, los añado a 
    ## ------------ las columnas y los asocio: (capa "controlador")
    cells = []
    for i in xrange(len(columns)):
        if (model.get_column_type(i) == gobject.TYPE_BOOLEAN 
           or isinstance(model.get_column_type(i), bool)):
            cells.append(gtk.CellRendererToggle())
            propiedad = "active"
        else:
            cells.append(gtk.CellRendererText())
            propiedad = "text"
            hay_algun_numero_en_la_columna = False
            for fila in filas:
                if es_interpretable_como_numero(fila[i]):
                    hay_algun_numero_en_la_columna = True
                    break
            if ((model.get_column_type(i) in (gobject.TYPE_FLOAT, 
                                              gobject.TYPE_DOUBLE))
                or isinstance(model.get_column_type(i), (int, float))
                or hay_algun_numero_en_la_columna):
                cells[-1].set_property("xalign", 1)
        columns[i].pack_start(cells[i], True)
        columns[i].add_attribute(cells[i], propiedad, i)
    ## ------------ Defino la columna de búsqueda:
    if len(columns) >= 4:
        tabla.set_search_column(3)    
        # Generalmente la 4ª es la de descripciones.
    else:  
        # Si no tiene 4 columnas, que la última sea la de búsqueda por 
        # defecto (se cambiará si hace clic en alguna cabecera).
        tabla.set_search_column(len(columns)-1)
    ## ------------ Y hago que se pueda ordenar por código o descripción:
    for i in xrange(len(columns)):
        model.set_sort_func(i, funcion_orden, i)
        # model.set_sort_column_id(i)
        # columns[i].set_sort_func(i, funcion_orden, i)
        columns[i].set_sort_column_id(i)
    return tabla, contenedor, de

def dialogo_resultado(filas, 
                      titulo = '', 
                      padre = None, 
                      cabeceras = ['Id', 'Código', 'Descripción'], 
                      multi = False,
                      func_change = lambda *args, **kwargs: None, 
                      maximizar = False, 
                      defecto = [], 
                      texto = "", 
                      abrir_en_ventana_nueva = None):
    """
    Muestra un cuadro de diálogo modal con una tabla. En
    la tabla se mostrarán tantas filas como items pasados
    en el parámetro filas.
    Devuelve el índice de la fila a la que se haga clic
    (en realidad, valor de la primera columna)
    con el ratón o -1 si se pulsó Cancelar.
    Devuelve -2 si filas no es una lista de resultados.
    En las cabeceras de las columnas se mostrará el texto de 
    la lista que se pase en el parámetro "cabeceras" de forma
    consecutiva. Si la longitud de "cabeceras" es menor que el
    número de columnas de la lista de filas, las TreeViewColumns
    restantes se quedarán con una descripción en blanco ('').
    La columna de búsqueda será siempre -de momento- la 
    segunda (elemento 1 de columns).
    Si multi es True, el TreeView del diálogo será de selección
    múltiple (gtk.SELECTION_MULTIPLE) y devolverá una lista de 
    índices seleccionados o una lista cuyo primer elemento es 
    -1 si ha cancelado.
    func_change es una función que se ejecutará cada vez que 
    el cursor cambie de fila activa en el treeview de resultados. 
    Debe estar preparada para recibir el TreeView como parámetro.
    defecto es una lista de índices por defecto que aparecerán 
    marcados. Si multi es False, solo se tendrá en cuenta el primero 
    de ellos (si lo hay). Los índices se refieren a la lista de valores
    recibidos en el parámetro "filas", que coinciden con el orden de 
    las filas en el model del TreeView. 
    abrir_en_ventana_nueva puede recibir una clase derivada de Ventana y 
    un usuario. En ese caso se crea un botón que abre el elemento 
    seleccionado en una nueva ventana de la clase.
    """
    # DONE: No sé si pasa solo en el equipo de desarrollo o también en 
    #       producción. No me he dado cuenta hasta ahora. El valor 
    #       que devuelve normalmente es un ID y debería ser de tipo entero. 
    #       Sin embargo devuelve el número como string. ¿Por qué?
    #       -> Ve al construir tabla y de ahí al tipo_gobject y lee los 
    #       comentarios. Se hace así porque a veces vienen textos y cadenas 
    #       en la misma columna y petaba. Como todo entra bien por un string 
    #       a la hora de mostrar datos en el TreeView, uso string incluso 
    #       para columnas de enteros y dejo después que se haga el cast donde 
    #       caiga.
    res = [-1]
    el_reparador_magico_de_representacion_de_flotantes_de_doraemon(filas)
    tabla, contenedor, de = construir_tabla(titulo, padre, filas, cabeceras)
    if tabla == -2: 
        return -2    # FIXME: Cosa más fea, I can do better. 
    ## ----------- Si lleva texto aclaratorio:
    if texto:
        label = gtk.Label(texto)
        try:
            ca = de.get_content_area()
        except AttributeError: # PyGTK es menor a la versión 2.14
            ca = de.vbox
        ca.pack_start(label, expand = False)
        ca.reorder_child(label, 0)
        label.show()
    if abrir_en_ventana_nueva:
        boton_abrir_en_ventana_nueva = gtk.Button("Abrir en ventana nueva")
        try:
            aa = de.get_action_area()
        except AttributeError: # PyGTK es menor a la versión 2.14
            aa = de.vbox
        aa.pack_end(boton_abrir_en_ventana_nueva, expand = False)
        boton_abrir_en_ventana_nueva.show()
        def abrir_aparte(boton, tabla, clase_ventana, clase_pclases, usuario):
            model, paths = tabla.get_selection().get_selected_rows()
            for p in paths:
                ide = model[p][0]
                o = clase_pclases.get(ide)
                v = clase_ventana(objeto = o, usuario = usuario)
        boton_abrir_en_ventana_nueva.connect("clicked", 
                abrir_aparte, tabla, *abrir_en_ventana_nueva)
    ## ----------- Si el Tree debe ser de selcción múltiple:
    if multi:
        tabla.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
    ## ----------- Asocio el evento "row-activated" (doble clic sobre una fila)
    #---------------------------------------------------------------#
    def obtener_id_fila(treeview, path, columna, res):              #
        """
        Guarda en res[0] el contenido de la primera columna 
        de la fila correspondiente al path (presumiblemente 
        un id de registro).
        """                                                         #
        # FIXME: Si es de selección múltiple solo va a devolver cuando se 
        # pulse ENTER la fila que se ha seleccionado por último, no todas las 
        # seleccionadas.
        # OJO: Si es de selección simple, el valor se devuelve      #
        #      al final de la función pero el diálogo se            #
        #      destruye aquí.                                       #
        res[0] = treeview.get_model()[path][0]                      #
        de.destroy()                                                #
    #---------------------------------------------------------------#
    tabla.connect("row-activated", obtener_id_fila, res)
    tabla.connect("cursor-changed", func_change)
    ## ------------ Empaqueto la tabla en el diálogo
    contenedor.show()
    tabla.show()
    #de.vbox.pack_start(tabla)
    de.vbox.pack_start(contenedor)
    de.resize(800, 600) 
    if maximizar:
        de.maximize()   
        # BUG: FIXME: El maximize no funciona bien con beryl en Ubuntu. 
        # Redimensiono antes para que conserve el tamaño si no puede maximizar.
        # De otra forma se queda con el tamaño mínimo posible de la ventana al 
        # intentar maximizar.
    if not defecto:
        itr = tabla.get_model().get_iter_first()
        if itr:
            tabla.get_selection().select_iter(itr)
            #tabla.grab_focus()
    else:
        model = tabla.get_model()
        for indice_fila in defecto[::-1]:
            try:
                itr = model[indice_fila].iter
            except:
                itr = None
            if itr:
                tabla.get_selection().select_iter(itr)
    de.get_children()[-1].get_children()[-1].get_children()[1].grab_focus()
    ## ------------ Ejecuto el diálogo, lo destruyo y devuelvo el resultado:
    response = de.run()
    if response == gtk.RESPONSE_CANCEL:
        res[0] = -1     # -1 es Cancelar. Ver la docstring de la función. 
    elif response == gtk.RESPONSE_ACCEPT:
        model, paths = tabla.get_selection().get_selected_rows()
        # paths es la lista de rutas. Recorro la lista de rutas 
        # devolviendo una lista de la columna 0 (id) de cada una
        # de ellas en el model:
        res = [model[path][0] for path in paths]
        # Si no hay absolutamente nada seleccionado, devuelvo 
        # el mismo valor que si hubiera cancelado:
        if res == []:
            res = [-1]
    de.destroy()
    if not multi:
        # NOTA: Para preservar la compatibilidad con el interfaz que se ha
        # estado usando hasta ahora, si el TreeView no es de selección 
        # múltiple se devuelve un único id.
        return res[0]
    else:
        # NOTA: Si es de selección múltiple devuelvo una lista de ids.
        return res

def mostrar_calendario(fecha_defecto = time.localtime()[:3][::-1], 
                       padre = None, titulo = 'SELECCIONE FECHA'):
    """
    Muestra y devuelve la fecha seleccioada con un clic.
    SIEMPRE devuelve una fecha como lista de [dd, mm, aaaa]
    aunque cierre la ventana sin seleccionarla con clic.
    La fecha por defecto debe venir en formato d/m/aaaa y
    en forma de lista o tupla.
    """
    if isinstance(fecha_defecto, type(mx.DateTime.localtime())):
        fecha_defecto = fecha_defecto.tuple()[:3][::-1]
    elif isinstance(fecha_defecto, str):
        try:
            fecha_defecto = parse_fecha(fecha_defecto)
            fecha_defecto = fecha_defecto.tuple()[:3][::-1]
        except:
            fecha_defecto = time.localtime()[::3][:-1]
    elif isinstance(fecha_defecto, type(time.localtime())):
        fecha_defecto = fecha_defecto[:3][::-1]
    elif isinstance(fecha_defecto, (tuple, list)) and len(fecha_defecto) < 3:
        fecha_defecto = fecha_defecto[:3]
    elif not fecha_defecto:
        fecha_defecto = time.localtime()[:3][::-1]
    cal = gtk.Calendar()
    cal.set_display_options(gtk.CALENDAR_SHOW_HEADING |
                            gtk.CALENDAR_SHOW_DAY_NAMES |
                            gtk.CALENDAR_WEEK_START_MONDAY)
    if isinstance(fecha_defecto, datetime.date):
        factual = [fecha_defecto.day, fecha_defecto.month, fecha_defecto.year]
    else:
        factual = fecha_defecto     # Fecha en formato d/m/aaaa
    cal.select_month(factual[1]-1, factual[2])  # Enero es el mes 0, no el 1.
    cal.select_day(factual[0])
    cal.mark_day(time.localtime()[2])
    dialog = gtk.Dialog(titulo, 
                        padre, 
                        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, 
                        (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
    dialog.set_transient_for(padre)
    dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
    dialog.vbox.pack_start(cal)
    cal.show()
    dialog.run()
    dialog.destroy()
    res = cal.get_date()
    res = tuple([res[0], res[1]+1, res[2]]) 
    return res[::-1]    # Para que quede como dd/mm/aaaa

## ---- Sacado de gtk_util del WIKI de SQLObject: -------------------

def combo_fill_text(combo_widget, content_list):
    """
    Crea y rellena el model del MVC del combo
    según la lista content_list.
    Usar esta función para combos sin .child->entry
    y sólo una columna (tipo str).
    """
    liststore = gtk.ListStore(str)
    combo_widget.set_model(liststore)
    cell = gtk.CellRendererText()
    combo_widget.pack_start(cell, True)
    combo_widget.add_attribute(cell, 'text', 0)
    for item in content_list:
        combo_widget.append_text(item)

def rellenar_lista(wid, textos):
    """ 
    Crea, rellena y asocia al model de un combobox
    el ListStore que se creará a partir de una lista o
    tupla de (enteros, cadenas). La cadena que se mostrará
    en el combo es la columna 1. La columna 0 es un 
    entero y -generalmente- será el id del elemento en 
    la BD.
    Versión castiza y con autocompletado -si el combo
    lo permite y tiene un .child entry- de la
    función anterior.
    """
    model = gtk.ListStore(int, str)
    for t in textos:
        model.append(t)
    cb = wid
    cb.set_model(model)
    if type(cb) is gtk.ComboBoxEntry:
        # HACK: Para evitar un "assert - GtkWarning" en posteriores llamadas.
        if cb.get_text_column()==-1:    
            cb.set_text_column(1)
        completion = gtk.EntryCompletion()
        completion.set_model(model)
        wid.child.set_completion(completion)
        completion.old_key = None
        completion.old_scores = None
        # Agrego un atributo más al completion que guardará el texto que
        # contiene el Entry para saber si cuando se invoca el match_func lo
        # que ha cambiado es el texto o solo el iter para recorrer la lista
        # del combo. En definitiva es para no repetir el proceso de búsqueda
        # difusa si el texto no ha cambiado.
        def simple_compare(parte, todo, only_start = False):
            """Devuelve True si el texto «parte» está en «todo» según el
            parámetro especificado «starts»:
                * False -> «todo» contiene a «parte»·
                * True -> «todo» empieza por «parte».
            """
            _parte = parte.replace(" ", "").upper()
            _todo = todo.replace(" ", "").upper()
            if only_start:
                res = _todo.startswith(_parte)
            else:
                res = _parte in _todo
            return res
        def match_func(completion, key, itr, (column, choices)):
            model = completion.get_model()
            text = model.get_value(itr, column)
            key = unicode(key, "utf")
            if len(key) <= 3:
                # Si llevo escrito poco texto, me valen las opciones que
                # empiecen por esas letras.
                res = simple_compare(key, text, only_start = True)
            elif 3 < len(key) < 10:
                # Si tengo algo más, busco en cualquier parte del texto de
                # las opciones.
                res = simple_compare(key, text) 
            else:
                try:
                    entry = completion.get_entry()
                    entry.set_icon_from_stock(1, gtk.STOCK_REVERT_TO_SAVED)
                    while gtk.events_pending(): gtk.main_iteration(False)
                except:     # PyGTK < 2.16
                    pass
                # Si ya tengo bastantes caracteres, pruebo búsqueda difusa.
                if completion.old_key is None or completion.old_key != key:
                    completion.old_key = key
                    completion.old_scores = scores = dict(
                        fuzzyprocess.extract(key, choices, limit = -1))
                else:
                    scores = completion.old_scores
                try:
                    res = scores[text] >= 90
                except KeyError:
                    res = simple_compare(key, text)
                except TypeError:
                    res = simple_compare(key, text)
                try:
                    entry.set_icon_from_stock(1, None)
                    while gtk.events_pending(): gtk.main_iteration(False)
                except:     # Python < 2.16
                    pass
            return res
        completion.set_text_column(1)
        completion.set_minimum_key_length(1)
        choices = [unicode(t[1], "utf") for t in list(set(textos))]
        completion.set_match_func(match_func, (1, choices))
        # completion.set_inline_completion(True)
        #---------------------------------------------------#
        def iter_seleccionado(completion, model, itr):      #
            combo_set_from_db(wid, model[itr][0])           #
        #---------------------------------------------------#
        completion.connect('match-selected', iter_seleccionado)
    elif type(cb) is gtk.ComboBox:
        cb.clear()  # Limpia posibles cells anteriores por si se ha llamado 
                    # a rellenar_lista más de una vez en el mismo widget..
        cell = gtk.CellRendererText()
        cb.pack_start(cell, True)
        cb.add_attribute(cell, 'text', 1)

def combo_set_from_db(combo_widget, db_item, forced_value = None):
    """
    Establece como elemento activo de un widget
    el elemento del model correspondiente con 
    el db_item. Para las comparaciones usa la
    primera columna del model, el db_item por
    tanto debe ser el valor en la BD del campo
    que se corresponda con esa columna (por lo 
    general debería ser un id).
    NO acepta tuplas completas.
    Si «force_value» es algo, se usará en caso de que no se 
    encuentre el db_item en el model. 
    """
    list_model = combo_widget.get_model()
    itr = list_model.get_iter_first()
    while itr != None and list_model.get_value(itr, 0) != db_item:
        itr = list_model.iter_next(itr)
    if itr == None: # No estaba el db_item en el model.
        if not forced_value:
            combo_widget.set_active(-1)     # Por si es un comboBoxEntry
            try:
                combo_widget.child.set_text("")
            except:
                pass
        else:   # Lo inserto en el model. No queda otra.
            list_model.append((db_item, forced_value))
            combo_widget.set_active(len(list_model) - 1)
            try:
                combo_widget.child.set_text(list_model[-1][1])
            except AttributeError:  # No es un comboBoxEntry
                pass
    else:
        combo_widget.set_active_iter(itr)

def combo_get_value(widget):
    """
    Devuelve el valor actual de la primera columna
    del elemento del model que se corresponde con 
    el activo en el widget.
    Si el model está vacío o no hay elemento
    activo, devuelve None.
    """
    list_model = widget.get_model()
    itr = widget.get_active_iter()
    try:
        return list_model.get_value(itr, 0)
    except (AttributeError, TypeError):  # itr es None en vez de un GtkTreeIter
        return None     # o bien el propio model es None porque el combo 
                        # todavía se está construyendo o eliminando.

def buscar_indice_texto(combo, texto):
    """ No tengo mucho tiempo que perder. Hasta que encuentre
    el método que haga esto (¿por qué son tan retorcidos los
    diseñadores de GTK?) moveré el índice del combobox hasta
    encontrar el texto pasado.
    Devuelve el índice del texto dentro del ListStore del combo.
    Si el texto no se encuentra, devuelve -1.
    Si hay dos textos idénticos, devuelve el índice del primero
    de ellos.
    """
    m = combo.get_model()
    itr = m.get_iter_first()
    i=0
    while itr!=None and m[i][1]!=texto:
        i+=1
        itr = m.iter_next(itr)
    if itr==None: return -1
    else: return i

#def redondear_flotante_en_cell_cuando_sea_posible(column, cell, model, itr, i, numdecimales = 2):
def redondear_flotante_en_cell_cuando_sea_posible(column, 
                                                  cell, 
                                                  model, 
                                                  itr, 
                                                  data):
    if isinstance(data, int):
        i = data
        numdecimales = 3
    else:
        i, numdecimales = data
    contenido = model[itr][i]
    if isinstance(contenido, float):
        expresion = "%%.%df" % numdecimales
        numredondo = float2str(expresion % contenido, numdecimales)
        cell.set_property('text', numredondo)

def preparar_treeview(tv, cols, multi = False):
    """
    Prepara el model con las columnas recibidas y 
    lo asocia al treeview mediante una TREESTORE.
    Las columnas deben tener el formato:
    (('Nombre', 'gobject.tipo', editable, ordenable, buscable, funcion, 
      parámetros adicionales a la función), ... )
    Sólo puede haber una columna buscable.
    Si editable == True, función no debe ser None y será conectada.
    Si multi es True (por defecto no lo es) el TreeView será de selección 
    múltiple.
    Al gobject de cada columna le asigna una clave propia llamada 'q_ncol' 
    que guarda la columna (comenzando por 0) que le corresponde en el model.
    Estoy completamente seguro de que pygtk debe tener algo parecido, pero 
    llevo toda la mañana buceando en la documentación y el código fuente y no 
    lo encuentro. La utilidad fundamental es que si el usuario reordena las 
    columnas, siempre puedo saber la posición original de los datos del model 
    que se están mostrando. En otro caso, el orden de los datos de las 
    columnas en el model y en el TreeView no coinciden y no encontraría la 
    manera de saber quién es quién.
    """
    tipos = [c[1].replace("TYPE_FLOAT", "TYPE_DOUBLE") for c in cols]
    model = eval('gtk.TreeStore(%s)' % ','.join(tipos)) 
    # No encuentro otra forma de hacerlo. Sorry.
    tv.set_model(model)
    # Quito la columna que no hay que mostrar:
    cols = cols[:-1]
    columns = []
    for header in [c[0] for c in cols]:
        columns.append(gtk.TreeViewColumn(header))
    for c in columns:
        # XXX: Experimental
        #c.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        c.set_resizable(True)
        c.set_reorderable(True)
        # XXX: EOExperimental
        tv.append_column(c)
    i = 0
    #for t, e, o, b, f in [(c[1:]) for c in cols]:
    for col in [(c[1:]) for c in cols]:
        try:
            t, e, o, b, f, func_params = col
            if not isinstance(func_params, (list, tuple)):
                func_params = [func_params]
        except ValueError: 
            t, e, o, b, f = col
            func_params = []
        if t == 'gobject.TYPE_BOOLEAN':
            cell = gtk.CellRendererToggle()
            cell.set_property("activatable", e)
            columns[i].pack_start(cell, True)
            columns[i].add_attribute(cell, 'active', i)
            if e and f!=None:
                cell.connect("toggled", f, *func_params)
            if o:
                columns[i].set_sort_column_id(i)
            if b:
                tv.set_search_column(i)
        elif t == 'gobject.TYPE_FLOAT' or t == 'gobject.TYPE_DOUBLE':
            cell = gtk.CellRendererText()
            cell.set_property("editable", e) 
            columns[i].pack_start(cell, True)
            columns[i].add_attribute(cell, 'text', i)
            columns[i].set_cell_data_func(cell, 
                redondear_flotante_en_cell_cuando_sea_posible, i)
            cell.set_property('xalign', 1.0)
            if e and f != None:
                cell.connect("edited", f, *func_params)
            if o:
                columns[i].set_sort_column_id(i)
            if b:
                tv.set_search_column(i)
        else:
            cell = gtk.CellRendererText()
            cell.set_property("editable", e)
            columns[i].pack_start(cell, True)
            columns[i].add_attribute(cell, 'text', i)
            if e and f!=None:
                cell.connect("edited", f, *func_params)
            if o:
                model.set_sort_func(i, funcion_orden, i)
                columns[i].set_sort_column_id(i)
            if b:
                tv.set_search_column(i)
            if t == 'gobject.TYPE_INT' or t == 'gobject.TYPE_INT64':
                cell.set_property('xalign', 1.0)
        columns[i].set_data("q_ncol", i)
        i += 1
    for c in columns:
        # XXX: Experimental
        #c.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        c.set_resizable(True)
        c.set_reorderable(True)
        # XXX: EOExperimental
    if multi:
        tv.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
    else:
        tv.get_selection().set_mode(gtk.SELECTION_SINGLE)

def preparar_listview(tv, cols, multi = False):
    """
    Prepara el model con las columnas recibidas y 
    lo asocia al treeview mediante una LISTSTORE.
    Las columnas deben tener el formato:
    (('Nombre', 'gobject.tipo', editable, ordenable, buscable, funcion, 
      parámetros), ... )
    Sólo puede haber una columna buscable.
    Si editable == True, función no debe ser None y será conectada.
    Si «multi» es True hace el TreeView de selección multiple.
    Al gobject de cada columna le asigna una clave propia llamada 'q_ncol' 
    que guarda la columna (comenzando por 0) que le corresponde en el model.
    Estoy completamente seguro de que pygtk debe tener algo parecido, pero 
    llevo toda la mañana buceando en la documentación y el código fuente y no 
    lo encuentro. La utilidad fundamental es que si el usuario reordena las 
    columnas, siempre puedo saber la posición original de los datos del model 
    que se están mostrando. En otro caso, el orden de los datos de las 
    columnas en el model y en el TreeView no coinciden y no encontraría la 
    manera de saber quién es quién.
    """
    tipos = [c[1].replace("TYPE_FLOAT", "TYPE_DOUBLE") for c in cols]
    model = eval('gtk.ListStore(%s)' % ','.join(tipos)) 
    # No encuentro otra forma de hacerlo. Sorry.
    tv.set_model(model)
    # Quito la columna que no hay que mostrar:
    cols = cols[:-1]
    columns = [None] * len(cols)
    i = 0
    for col in cols:
        try:
            h, t, e, o, b, f, func_params = col
            if not isinstance(func_params, (list, tuple)):
                func_params = [func_params]
        except ValueError: 
            h, t, e, o, b, f = col
            func_params = []
        if t == 'gobject.TYPE_BOOLEAN':
            cell = gtk.CellRendererToggle()
            cell.set_property("activatable", e)
            columns[i] = gtk.TreeViewColumn(h, cell) 
            columns[i].add_attribute(cell, 'active', i)
            if e and f!=None:
                cell.connect("toggled", f, *func_params)
            if o:
                columns[i].set_sort_column_id(i)
            if b:
                tv.set_search_column(i)
            tv.insert_column(columns[i], -1)
        elif t == 'gobject.TYPE_FLOAT' or t == 'gobject.TYPE_DOUBLE':
            cell = gtk.CellRendererText()
            cell.set_property("editable", e) 
            columns[i] = gtk.TreeViewColumn(h, cell, text = i) 
            if e and f!=None:
                cell.connect("edited", f, *func_params)
            if b:
                tv.set_search_column(i)
            cell.set_property('text', i)
            tv.insert_column_with_data_func(-1, h, cell, redondear_flotante_en_cell_cuando_sea_posible, i)
            cell.set_property('xalign', 1.0)
            if o:
                columns[i].set_sort_column_id(i)
        else:
            cell = gtk.CellRendererText()
            cell.set_property("editable", e)
            columns[i] = gtk.TreeViewColumn(h, cell) 
            columns[i].add_attribute(cell, 'text', i)
            if e and f != None:
                cell.connect("edited", f, *func_params)
            if o:
                model.set_sort_func(i, funcion_orden, i)
                columns[i].set_sort_column_id(i)
            if b:
                tv.set_search_column(i)
            if t == 'gobject.TYPE_INT' or t == 'gobject.TYPE_INT64':
                cell.set_property('xalign', 1.0)
            tv.insert_column(columns[i], -1)
        columns[i].set_data("q_ncol", i)
        i += 1
    for c in columns:
        # XXX: Experimental
        #c.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        c.set_resizable(True)
        c.set_reorderable(True)
        # XXX: EOExperimental
    if multi:
        tv.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
    else:
        tv.get_selection().set_mode(gtk.SELECTION_SINGLE)

def comparar_enteros(n, m):
    """
    Compara n y m como enteros y devuelve 
    -1 si n es menor que m, 1 si es al contrario 
    o 0 si son iguales.
    OJO: Si ALGUNO de los dos no es entero (harto improbable estando en la misma columna)
    usará la comparación a nivel de registro de memoria, me parece, y a saber el orden
    que saldrá.
    """
    if isinstance(n, int) and isinstance(m, int):
        return n - m
    else:
        if n < m:
            return -1
        elif n > m:
            return 1
        else:
            return 0

def comparar_fechas(dato1, dato2):
    """
    Intenta comparar dato1 y dato2 como fechas en formato dd/mm/aaaa.
    NOTA: FUNCIÓN OBSOLETA.
    """
    try:
        d1, m1, a1 = map(int, dato1.split('/'))
    except:
        return 
    try:
        d2, m2, a2 = map(int, dato2.split('/'))
    except:
        return -1   # Si dato2 no es interpretable como fecha, devuelvo que dato1 es menor (dato1 al menos parece una fecha).
    if a1 < a2:
        return -1
    elif a1 > a2:
        return 1
    else:
        if m1 < m2:
            return -1
        elif m1 > m2:
            return 1
        else:
            if d1 < d2:
                return -1
            elif d1 > d2:
                return 1
            else:
                return 0

def es_interpretable_como_numero(n):
    """
    Devuelve True si "n" se puede interpretar como número.
    """
    if convertir_a_numero(n) != None:
        res = True
    else:
        res = False
    return res

def es_interpretable_como_fechahora(f):
    """
    Devuelve True si f se puede convertir a fecha.
    """
    if convertir_a_fechahora(f):
        res = True
    else:
        res = False
    return res

def es_interpretable_como_fecha(f):
    """
    Devuelve True si f se puede convertir a fecha.
    """
    if convertir_a_fecha(f):
        res = True
    else:
        res = False
    return res

def convertir_a_fecha(f):
    """
    Intenta convertir f a una fecha.
    Devuelve None si no se puede.
    """
    try:
        res = parse_fecha(f)
    except:
        res = None
    return res

def convertir_a_fechahora(f):
    """
    Intenta convertir f a una fechahora.
    Devuelve None si no se puede.
    """
    try:
        res = parse_fechahora(f)
    except:
        res = None
    return res

def convertir_a_numero(n):
    """
    Convierte n a flotante.
    Devuelve None si no se puede.
    """
    res = None
    try:
        res = _float(n)
    except:
        if isinstance(n, str) and "€" in n:
            try:
                res = parse_euro(n)
            except:
                res = None
        elif isinstance(n, str) and "%" in n:
            try:
                res = parse_porcentaje(n)
            except:
                res = None
    return res

def comparar_como_numeros(n, m):
    """
    Compara n y m como números (entero o flotante) y 
    devuelve -1, 0 ó 1 tal y como espera la función .sort.
    """
    n = convertir_a_numero(n)
    m = convertir_a_numero(m)
    if n < m:
        return -1
    elif n > m:
        return 1
    else:
        return 0

def comparar_como_fechas(n, m):
    """
    Compara n y m como fechas.
    """
    n = convertir_a_fecha(n)
    m = convertir_a_fecha(m)
    if n < m:
        return -1
    elif n > m:
        return 1
    else:
        return 0

def comparar_como_fechahora(n, m):
    """
    Compara n y m como fechas con hora (DateTime completo).
    """
    n = convertir_a_fechahora(n)
    m = convertir_a_fechahora(m)
    if n < m:
        return -1
    elif n > m:
        return 1
    else:
        return 0

def funcion_orden(model, iter1, iter2, columna):
    """
    Función para ordenar la columna "columna" de un TreeView.
    Si es fecha ordena por día/mes/año. 
    Si es número, compara como número -acepta enteros y flotantes-.
    Si no es fecha (no contiene dos '/') ni número usa el orden 
    predefinido por python para cadenas.
    """
    dato1 = model[iter1][columna]
    dato2 = model[iter2][columna]
    if es_interpretable_como_numero(dato1) and es_interpretable_como_numero(dato2):
        res = comparar_como_numeros(dato1, dato2)
    elif es_interpretable_como_fecha(dato1) and es_interpretable_como_fecha(dato2):
        res = comparar_como_fechas(dato1, dato2)
    elif es_interpretable_como_fechahora(dato1) and es_interpretable_como_fechahora(dato2):
        res = comparar_como_fechahora(dato1, dato2)
    elif isinstance(dato1, str) and isinstance(dato2, str):
        res = (dato1.upper() < dato2.upper() and -1) or (dato1.upper() > dato2.upper() and 1) or 0
    else:
        if dato1 < dato2:
            res = -1
        elif dato1 > dato2:
            res = 1
        else:
            res = 0
    return res

def mostrar_hora(horas = 0, minutos = 0, segundos = 0, titulo = 'HORA', 
                 ver_segundos = False, padre = None):
    """
    Muestra una ventana con spinbuttos y la hora pasada
    (por defecto 00:00:00) y devuelve una cadena con
    la hora seleccionada separada por ':' o None si 
    se canceló.
    """
    hora = [None]    # Listas no son inmutables
    from widgets import Widgets
    wids = Widgets('ventana_hora.glade')
    wids['ventana'].set_title(titulo)
    wids['ventana'].set_transient_for(padre)
    #-------------------------------------------------------------------------#
    def aceptar(boton, hora):                                                 #
        lista_valores = map(lambda x: wids[x].get_text(),                     #
                                ('sp_hora', 'sp_minutos', 'sp_segundos'))     #
        lista_valores = ['%02d' % int(v) for v in lista_valores]              #
        hora[0] = ':'.join(lista_valores)                                     #
        wids['ventana'].destroy()                                             #
    def cancelar(boton):                                                      #
        wids['ventana'].destroy()                                             #
    #-------------------------------------------------------------------------#
    connections = {'ventana/destroy': gtk.main_quit,
                   'b_cancelar/clicked': cancelar, 
                   'sp_hora/output': show_leading_zeros, 
                   'sp_minutos/output': show_leading_zeros, 
                   'sp_segundos/output': show_leading_zeros 
                  }
    for wid_con, func in connections.iteritems():
        wid, con = wid_con.split('/')
        wids[wid].connect(con, func)
    wids['b_aceptar'].connect('clicked', aceptar, hora)
    wids['sp_hora'].set_text("%2d" % horas)
    wids['sp_minutos'].set_text("%2d" % minutos)
    wids['sp_segundos'].set_text("%2d" % segundos)
    wids['sp_hora'].get_adjustment().set_value(horas)
    wids['sp_minutos'].get_adjustment().set_value(minutos)
    wids['sp_segundos'].get_adjustment().set_value(segundos)
    show_leading_zeros(wids['sp_hora'])
    show_leading_zeros(wids['sp_minutos'])
    show_leading_zeros(wids['sp_segundos'])
    if not ver_segundos:
        wids['sp_segundos'].set_child_visible(False)
        wids['label2'].set_child_visible(False)
    wids['sp_hora'].select_region(0, -1)
    gtk.main()
    return hora[0]

def show_leading_zeros(spin_button):
    adjustment = spin_button.get_adjustment()
    try:
        spin_button.set_text('{:02d}'.format(int(adjustment.get_value())))
    except:     # ¿Python < 2.7?
        spin_button.set_text("%02d" % (int(adjustment.get_value())))
    return True


# ----------------------- UTILS DIEGO ------------------------- #
def parse_euro(strfloat):
    """
    Recibe una cantidad monetaria como cadena. Puede incluir el un espacio,
    el signo menos (-) y el euro (€).
    La función procesa la cadena y devuelve un flotante que se 
    corresponde con el valor o lanza una excepción ValueError si 
    no se puede parsear.
    """
    if not isinstance(strfloat, str):   # Por si las moscas
        strfloat = str(strfloat)
    res = strfloat.replace('€', '')
    res = res.strip()
    try:
        res = _float(res)
    except ValueError, msg:
        res = None
        #utils.dialogo('El número no se puede interpretar.')
        raise ValueError, "%s: El número %s no se puede interpretar como moneda." % (msg, strfloat)
    return res

def prepara_hora(hora):
    lista = hora.split(":")
    if len(lista) > 3:
        lista = lista[:3]
    else:
        longit = len(lista)
        longit = 3 - longit
        for i in range(longit):
            lista.append('00')
    try:
        for i in range(3):
            int(lista[i])
    except:
        return '-1'         # Caso de hora incorrecta
    
    return ":".join(lista)  # Caso de hora correcta, la devolvemos
    

def str_booleano(valor):
    """
    Para imprimir valores booleanos. Si es TRUE devuelve 'Sí',
    si no 'No' y en caso de error ''.
    """
    try:
        if valor: 
            return 'Sí'
        elif not valor: 
            return 'No'
    except:
        return ''

#------------------------------------------------------------------------

def get_configuracion_ftp():
    """
    Lee la configuración del FTP de un archivo 
    llamado nftp.conf en el directorio actual o
    en el directorio ../framework.
    Devuelve un diccionario con los valores "host",
    "user" y "passwd" o None si no encontró el 
    archivo.
    """
    try:
        f = open('nftp.conf')
    except:
        try:
            f = open(os.path.join('..', 'framework', 'nftp.conf'))
        except:
            return None
    res = {'host': '', 'user': '', 'passwd': ''}
    for l in f.readlines():
        c, v = l.split(':')
        if c == 'host':
            res['host'] = v.strip()
        elif c == 'username':
            res['user'] = v.strip()
        elif c == 'password':
            res['passwd'] = v.strip()
    return res

def obtener_md5_remoto(archivo):
    """
    Obtiene la cadena correspondiente al MD5 del archivo
    remoto.
    """
    from ftplib import FTP
    # OJO: Configuración del cliente FTP HARCODED. Esto habría que sacarlo al archivo de configuración ginn.conf
    # conexion = FTP(host='melchor', user='geotexan', passwd='')
    # conexion = FTP(host='192.168.1.100', user='geotexan', passwd='')
    # FIXED: Ahora tira de archivo de configuración.
    conf = get_configuracion_ftp()
    conexion = FTP(host=conf['host'], user=conf['user'], passwd=conf['passwd'])
    conexion.cwd('ginn')
    conexion.cwd('md5')
    infomd5 = {'md5':'', 'archivo':''}
    def get_md5_from_line(l):
        infomd5['md5'], infomd5['archivo'] = l.split()
    conexion.retrlines('RETR %s.md5' % archivo, get_md5_from_line)
    conexion.close()
    return infomd5['md5']

def md5_iguales(archivo):
    """
    Obtiene el MD5 del archivo remoto y el MD5 del archivo
    local y los compara.
    Devuelve True si ambos son iguales.
    False en caso contrario o si ocurrió algún error (por
    ejemplo al obtener el MD5 local).
    """
    #print >> sys.stderr, "Error en el nombre del archivo: %s" % archivo 
    try:
        fmd5local = open(os.path.join('md5', '%s.md5' % archivo))
    except IOError:
        # El archivo local no existe:
        return False
    md5remoto = obtener_md5_remoto(archivo)
    try:
        md5local = fmd5local.readline().split()[0]
    except:
        return False
    # El md5 local se podría calcular tal y como viene en el wiki (ginn.sf.net/wiki), 
    # pero es bastante más rápido guardar una copia local del md5 del servidor. No 
    # es probable que se cambie un archivo localmente y no en el servidor centralizado.
    ##DEBUG: print md5local
    ##DEBUG: print md5remoto
    return md5local == md5remoto
    
def descargar(archivo, glade = True):
    """
    Descarga el archivo remoto con el nombre "archivo"
    y archivo glade que le corresponde al
    directorio de trabajo y actualiza el md5 en ./md5.
    """
    nftp.descargar_archivo(archivo)
    nftp.descargar_archivo(archivo+'.md5', True)
    if glade:    # Si el archivo es una ventana y lleva un .glade, descargarlo también
        nftp.descargar_archivo(archivo[:archivo.index('.')]+'.glade')

def verificar_source(nombre_archivo):
    """
    Comprueba el MD5 de un archivo con el del servidor, 
    si no coinciden descarga el archivo indicado y el 
    nuevo md5.
    """
    if not md5_iguales(nombre_archivo):
        descargar(nombre_archivo)

def ejecutar_interprete(source, *arguments, **keywords):
    """
    Abre el intérprete python con el fuente recibido.
    INPUT:
      source: fuente que ejecuta (obligatorio).
      arguments: lista de argumentos extra.
      keywords: diccionario de argumentos con nombre.
    """
    if os.name == 'posix':
        ejecutable = "python -u "
    else:
        ejecutable = "start /B python -u" 
    argumentos = " ".join([str(a) for a in arguments if a != None])
    os.system("%s %s %s &" % (ejecutable, source, argumentos))

def parse_fecha(txt):
    """
    Devuelve un mx.DateTime con la fecha de txt.
    Si no está en formato dd{-/\s}mm{/-\s}yy[yy] lanza una
    excepción.
    Reconoce también textos especiales para interpretar fechas:
    h -> Hoy. Fecha actual del sistema.
    d -> Días. Para sumar o restar días a la fecha que le preceda.
    pdm -> Primero de mes. Día 1 del mes corriente.
    udm -> Último de mes. Último día del mes corriente.

    doctest:

    >>> parse_fecha("01/01/2009").strftime("%d/%m/%y")
    '01/01/09'
    >>> utils.parse_fecha("010109").strftime("%d/%m/%y")
    '01/01/09'
    >>> utils.parse_fecha("01-01-2009").strftime("%d/%m/%y")
    '01/01/09'
    """
    # TODO: Aquí hay un pequeño problema. Ya no acepta fechas 22-11-1979.
    if re.compile("(\d{2}-\d{2}-(\d{4}|\d{2}))").findall(txt):
        txt = txt.replace("-", "/")
    # Navision plagiarism! (¿Quién lo diría?)
    txt = txt.strip().upper()
    if "PDM" in txt:
        tmpdate = mx.DateTime.DateTimeFrom(
            day = 1, 
            month = mx.DateTime.localtime().month, 
            year = mx.DateTime.localtime().year)
        txt = txt.replace("PDM", tmpdate.strftime("%d/%m/%Y"))
    if "UDM" in txt:
        tmpdate = mx.DateTime.DateTimeFrom(
            day = -1, 
            month = mx.DateTime.localtime().month, 
            year = mx.DateTime.localtime().year)
        txt = txt.replace("UDM", tmpdate.strftime("%d/%m/%Y"))
    if txt.count("-") == 2:
        txt = txt.replace("-", "/")
    if txt.count("/") == 1:
        txt += "/%d" % mx.DateTime.localtime().year
    if "+" in txt or "-" in txt:
        txt = txt.replace("D", " * mx.DateTime.oneDay")
        txt = txt.replace("H", "mx.DateTime.today()")
        rex = re.compile("[-]?\d+/\d+/\d+")
        for bingo in rex.findall(txt):
            try:
                _bingo = "/".join([`int(i)` for i in bingo.split("/")])
            except (TypeError, ValueError):
                pass
            try:
                if int(_bingo.split("/")[-1]) < 100: # Año con dos dígitos.
                    _bingo="/".join([`int(i)` for i in _bingo.split("/")[:2]] +
                                     [`2000 + int(_bingo.split("/")[-1])`])
            except:
                pass
            mxbingo = "mx.DateTime.DateTimeFrom(day=%s,month=%s,year=%s)" % (
                _bingo.split("/")[0], 
                _bingo.split("/")[1], 
                _bingo.split("/")[2])
            txt = txt.replace(bingo, mxbingo)
        try:
            tmpdate = eval(txt)
        except:
            raise ValueError, "%s no se pudo interpretar como fecha." % txt
        try:
            txt = tmpdate.strftime("%d/%m/%Y")
        except AttributeError:
            txt = (mx.DateTime.today() 
                    + mx.DateTime.TimeDelta(24 * tmpdate)).strftime("%d/%m/%Y")
    if "H" in txt:
        txt = txt.replace("H", mx.DateTime.today().strftime("%d/%m/%Y"))
    try:
        dia, mes, anno = map(int, txt.split('/'))
    except ValueError:
        try:
            dia, mes, anno = map(int, txt.split('-'))
        except ValueError:
            if len(txt) >= 4:
                dia = int(txt[:2])
                mes = int(txt[2:4])
                if len(txt) >= 6: 
                    anno = int(txt[4:])
                else:
                    anno = mx.DateTime.today().year
            elif 2 < len(txt) < 4 and txt.isdigit():
                dia = int(txt[0])
                mes = int(txt[-2:])
                if mes > 12:
                    dia = int(txt[:2])
                    mes = int(txt[2:])
                anno = mx.DateTime.localtime().year
            elif txt.isdigit() and len(txt) <= 2:
                dia = int(txt)
                mes = mx.DateTime.localtime().month
                anno = mx.DateTime.localtime().year
            else:
                raise ValueError, "%s no se pudo interpretar como fecha." % txt
    if anno < 1000:
        anno += 2000    
        # Han metido 31/12/06 y quiero que quede 31/12/2006 y no 31/12/0006
    return mx.DateTime.DateTimeFrom(day = dia, 
                                    month = mes, 
                                    year = anno) 

def parse_fechahora(txt):
    """
    Devuelve un mx.DateTime con la fecha y hora de
    txt.
    Si no está en formato dd{-/}mm{-/}yy[yy] HH:MM[:SS] lanza una
    excepción.
    """
    try:
        if isinstance(txt, (datetime.datetime, datetime.date)):
            txt = txt.strftime("%d/%m/%Y %H:%M:%S")
    except ImportError:
        pass
    fechamysqlstyle = re.compile("\d+-\d+-\d+ \d{2}:\d{2}")
    if fechamysqlstyle.findall(txt):
        dia, mes, anno = txt.split(" ")[0].split("-")[:3]
        hora = txt.split(" ")[-1]
        if len(dia) > len(anno):    # Viene con el año al principio. 4 dígitos
            anno, dia = dia, anno   # mayor que 2.
        # Cambio el separador a la barra, que me lo reconoce el parse_fecha
        txt = dia + "/" + mes + "/" + anno + " " + hora
    if "-" in txt and " " not in txt:
        sep = "-"
    else:
        sep = " "
    fecha, hora = "".join(txt.split(sep)[:-1]), txt.split(sep)[-1]
    fecha = parse_fecha(fecha)
    hora = parse_hora(hora)
    res = fecha + hora      # Curioso... la suma de DateTime y DateTimeDelta 
    return res              # no tiene la propiedad conmutativa.

def parse_hora(txt):
    """
    Devuelve un mx.DateTimeDelta a partir del
    texto recibido.
    """
    if ":" not in txt:
        if len(txt) <= 2:
            txt = txt + "00"
        txt = txt[:-2] + ":" + txt[-2:]
    valores = [v.strip() != "" and v or "0" for v in txt.split(":")]
    if len(valores) == 3:
        hora, minuto, segundo = map(_float, valores)
    elif len(valores) == 4:  # Lleva hasta días.
        dias = _float(valores[0])
        hora, minuto, segundo = map(_float, valores[1:])
        hora += dias*24
    else:
        segundo = 0
        hora, minuto = map(_float, valores)
    return mx.DateTime.DateTimeDeltaFrom(hours = hora,
                                         minutes = minuto,
                                         seconds = segundo)

def round_banquero(numero, precision = 2):
    """
    Redondea a "precisión" decimales. Por defecto a 2.
    Por ejemplo: 
        0.076 -> 0.08
        0.071 -> 0.07
    """
    return int(numero*(10.0**(precision)) + 0.5)/(10.0**(precision))

#round_banquero = lambda numero, precision: (int(numero*(10.0**(precision)) + 0.5))/(10.0**(precision))

def ffloat(n, precision = 2):
    """
    Convierte un float a ffloat con el redondeo correcto. 
    Para ello convierte antes a string.
    """
    if precision == 0:
        return Ffloat(int(round(n, 0)))
    elif precision > 0:
        if isinstance(n, (float, Ffloat)) or isinstance(n, int):
            if n < 0:   # Es negativo
                negativo = True
                n = -n  # Lo hago positivo y después le añadiré el signo -.
            else:
                negativo = False
            # Cutrealgoritmo Bankers Rounding. Lo hago después de comprobar si
            # es negativo para un redondeo simétrico:
            # Algo un poco más profesional pero que no logro hacer que 
            # funcione como quiero: http://fixedpoint.sourceforge.net
            n = round_banquero(n, precision)
            s = "%%.%df" % precision
            s = s % (n)
            # s = s.replace('.', ',')
            # i = s.rindex(',')
            # i -= 3
            # while i > 0:
            #     s = s[:i] + "." + s[i:]
            #     i -= 3
            if negativo:
                s = "-"+s
            return Ffloat(s)
        elif isinstance(n, str):
            if "," in n:  # Seguramente venga en formato "123.234,234" así que:
                n = n.replace('.', '')
                n = n.replace(',', '.')
            return ffloat(float(n), precision)
        else:
            raise ValueError, "(utils.py) ffloat: El parámetro n debe ser una cadena, un entero, un float o un FixedPoint."

def myround(x):
    if x > 0:
        res = round(int((float(x) * 100) + (0.5 + 0.000001))) / 100.0
    elif x < 0:
        res = round(int((float(x) * 100) - (0.5 + 0.000001))) / 100.0
    else:
        res = x
    return res

def float2str(n, precision = 2, autodec = False, separador_decimales = ","):
    """
    Devuelve una cadena con el flotante convertido a entero en 
    formato xxx.xxx.xxx[,{y}]. La "precisión" (número de decimales
    mostrados) por defecto es 2.
    Si autodec es True, autodecrementa el número de decimales para no
    mostrar ceros a la derecha en la parte fraccionaria. Si es False no hace 
    nada. Y si es un número, autodecrementa hasta quedarse con ese número 
    mínimo de lugares decimales a mostrar.
    """
    if precision == 0:
        res = str(int(round(n, 0)))
    elif precision > 0:
        try:
            from decimal import Decimal
            if isinstance(n, Decimal):
                n = float(n)
        except ImportError:
            pass
        es_de_tipo_numerico = isinstance(n, (float, Ffloat, int, long))
        if es_de_tipo_numerico:
            if n < 0:   # Es negativo
                negativo = True
                n = -n  # Lo hago positivo y después le añadiré el signo -.
            else:
                negativo = False
            # Cutrealgoritmo Bankers Rounding. Lo hago después de comprobar si 
            # es negativo para un redondeo simétrico:
            # Algo un poco más profesional pero que no logro hacer que 
            # funcione como quiero: http://fixedpoint.sourceforge.net
            if precision == 2:  # Euros, euros, dubidú
                n = myround(n)
            else:
                n = round_banquero(n, precision)
            s = "%%.%df" % precision
            s = s % (n)
            s = s.replace('.', ',')
            i = s.rindex(',')
            i -= 3
            while i > 0:
                s = s[:i] + "." + s[i:]
                i -= 3
            if negativo:
                s = "-"+s
            res = s
        elif isinstance(n, str):
            if "," in n:  # Seguramente venga en formato "123.234,234" así que:
                n = n.replace('.', '')
                n = n.replace(',', '.')
            res = float2str(float(n), precision)
        else:
            try:
                res = float2str(float(n), precision)
            except Exception:
                raise ValueError, \
                      "El valor %s no se pudo convertir a cadena." % n
    if autodec:
        parte_fraccionaria = lambda n: "," in n and n[n.rfind(',') + 1:] or ""
        while ("," in res and len(res) - res.index(",") > 2 and res[-1] == '0'
               and len(parte_fraccionaria(res)) > autodec):
            res = res[:-1]
        if res[-1] == '0' and res[-2] == ",":
            res = res[:-2]
    res = res.replace(",", separador_decimales)
    return res

def float2str_autoprecision(n, c, t, p = 2):
    """
    Devuelve un flotante como cadena con la precisión suficiente como para que 
    al multiplicarse con «c» dé «t».
    «p» es la precisión mínima deseada.
    (Similar al método usado por la clase LineaDeVenta en 
    «calcular_precio_unitario_coherente», solo que no es dependiente de ningún 
    atributo de LDV.
    """
    totlinea = t
    cantidad = c
    precision = p
    for i in range(precision, 6):
        precio = float2str(n, i)
        # Emulo lo que saldrá en pantalla, para ver si cuadra:
        strsubtotal1 = float2str(totlinea, precision)
        subtotal2 = _float(precio) * cantidad
        strsubtotal2 = float2str(subtotal2, precision)
        if strsubtotal1 == strsubtotal2:
            break
    # Reduzco los ceros por la derecha hasta llegar a la precisión mínima
    # requerida en «p».
    def numdecimales(p):
        "NOTA: El separador de decimales debe ser la coma."
        try:
            numdec = len(p) - p.index(",") - 1
        except ValueError:
            numdec = 0  # No hay separador decimal.
        return numdec
    while precio.endswith("0") and "," in precio and numdecimales(precio) > p:
        precio = precio[:-1]
    if precio.endswith(","):
        precio = precio[:-1]
    return precio

def int2str(n):
    """
    Devuelve el número entero recibido como 
    cadena con formato de punto de separación 
    cada 3 dígitos.
    P.ej: int2str(1234) = "1.234"
          int2str(0) = "0"
          etc...
    """
    # ¿Quién dijo que Python no podía ser tan críptico como Perl? 
    # Todo es ponerse ;)
    puntuar_entero = lambda s: ".".join([(i>=3 and [s[i-3:i]] or [s[:abs(0-i)]])[0] for i in range(len(s), 0, -3)][::-1])
    if isinstance(n, float):
        return puntuar_entero(str(int(round(n))))
    elif isinstance(n, str): 
        return puntuar_entero(str(int(round(float(n)))))
    elif isinstance(n, int):
        return puntuar_entero(str(n))
    else:
        return puntuar_entero(str(int(round(n))))
    
def check_num(num):
    """
    Detecta si un número que viene como cadena respeta el formato 1234.56
    Si puede, lo formatea correctamente antes de devolverlo. En otro caso
    devuelve la misma cadena recibida.
    OBSOLETO.
    """
    if isinstance(num, str):
        if ('.' in num and ',' in num) or num.count('.') > 1:
            num = num.replace('.', '')
        if ',' in num:
            num = num.replace(',', '.')
    return num

def recortar(txt, maxim = 30):
    """
    Recorta una cadena al máximo de caracteres si es más 
    larga que éste. Añade puntos suspensivos en ese caso.
    """
    res = txt
    if len(txt) > maxim:
        res = txt[:maxim-3]+"..."
    return res

#_float = lambda x: isinstance(x, str) and (("," in x and [float(x.replace(".","").replace(",","."))]) or [float(x)])[0] or float(x)

def _float(x): #, precision = 2):
    #if isinstance(x, float):
    #    x = float2str(x, precision)
    if isinstance(x, str) and x.startswith("."):
        x = "0" + x
    if isinstance(x, str) and (',' in x):
        x = x.replace(".", "")
        x = x.replace(",", ".")
    #res = ffloat(x, precision)
    res = float(x)
    return res

def corregir_nombres_fecha(s):
    """
    Porque todo hombre debe enfrentarse al menos una 
    vez en su vida a dos tipos de sistemas operativos: 
    los que se no se pasan por el forro las locales, 
    y MS-Windows.
    """
    if os.name == 'nt':
        sabado = "sabado"
        miercoles = "miercoles"
    else:
        sabado = "sábado"
        miercoles = "miércoles"
    trans = {'Monday': 'lunes',
             'Tuesday': 'martes',
             'Wednesday': miercoles,
             'Thursday': 'jueves',
             'Friday': 'viernes',
             'Saturday': sabado,
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
        s = s.replace(in_english, trans[in_english])    # .title()
        # s = s.replace(in_english.lower(), trans[in_english])
        # s = s.replace(in_english.upper(), trans[in_english])
    s = unicode(s, "iso8859-15")
    s = s.encode("utf-8")
    return s

def descamelcase_o_matic(s):
    """
    Devuelve la cadena «s» (que se recibe en formato CamelCase)
    sustituyendo las mayúsculas por "espacio-minúscula" y poniendo 
    la primera letra en mayúscula.
    """
    res = ""
    for c in s:
        if c in string.uppercase:
            res += " %c" % (c.lower())
        else:
            res += c
    res = res[0].upper() + res[1:]
    return res

def DateTime2DateTimeDelta(dt):
    """
    Devuelve un DateTimeDelta correspondiente a la hora
    del DateTime «dt» (también admite DateTimeDelta, aunque
    sea un poco inútil convertir de un tipo al mismo).
    En determinadas versiones de python y las bibliotecas de terceros puede 
    admitir datetime.time.
    """
    try:
        h = dt.hour
    except AttributeError:
        dtd = mx.DateTime.DateTimeDeltaFrom(dt.seconds)
    else:
        m = dt.minute
        s = dt.second
        dtd = mx.DateTime.DateTimeDeltaFrom(hours=h, minutes=m, seconds=s)
    return dtd

def f_sort_id(x, y):
    """
    Función para usar como cmpfunc en la ordenación de listas de relaciones 
    múltiples.
    Ordena por id de registros.
    P. ej. facturaVenta.lineasDeVenta.sort(utils.f_orden_por_id)
    """
    if x.id < y.id:
        return -1
    if x.id > y.id:
        return 1
    return 0

def cmp_mxDateTime(f1, f2):
    """
    Compara dos fechas mx.DateTime y devuelve -1, 1 ó 0.
    Útil para ordenaciones de fechas.
    REMEMBER: ¡DEBEN SER mx.DateTime!

    >>> utils.cmp_mxDateTime(mx.DateTime.today(), 
                             mx.DateTime.today() - mx.DateTime.oneDay)
    1
    >>> utils.cmp_mxDateTime(mx.DateTime.today(), mx.DateTime.today())
    0
    >>> utils.cmp_mxDateTime(None, mx.DateTime.today())
    -1
    >>> utils.cmp_mxDateTime(None, None)
    0
    >>> utils.cmp_mxDateTime(mx.DateTime.today(), None)
    1
    >>> utils.cmp_mxDateTime(mx.DateTime.today(), 
                             mx.DateTime.today() + mx.DateTime.oneDay)
    -1
    """
    if f1 and f2:
        if f1 < f2:
            return -1
        if f1 > f2:
            return 1
    elif f1 and not f2: # Los None siempre menor a lo demás.
        return 1    # f1 > None
    elif f2 and not f1:
        return -1   # f2 > None
    else:   # Sobraría, pero mejor explícito que implícito. Pythonic, isn't it?
        return 0    # Ambos None
    return 0

def dialogo_pedir_codigos(titulo = "INTRODUZCA RANGO",
                          texto = "Introduzca un número, un código, un rango de números separado por guión o un rango de códigos.\n\nEjemplos válidos:\n  100, 105\n  C100-C110, 105 107\n  etc...",
                          padre = None,
                          valor_por_defecto = ""
                         ):
    """
    Igual que el diálogo de pedir rangos pero además acepta una letra mayúscula o minúsucula (que acabará
    convirtiendo a mayúscula). Devuelve una lista iterable de códigos o números, dependiendo de si 
    se detectó la letra inicial o no.
    """
    rangos = re.compile("[a-zA-Z]*\ ?\d+[ ]*-[ ]*[a-zA-Z]*\ ?\d+")
    sueltos = re.compile("[a-zA-Z]*\ ?\d+")
    numero = re.compile("\d+")
    letras = re.compile("[a-zA-Z]+")
    res = None
    rango_entrada = dialogo_entrada(titulo = titulo, 
                                    texto = texto, 
                                    padre = padre, 
                                    valor_por_defecto = valor_por_defecto)
    if rango_entrada != '' and rango_entrada != None:
        res = []
        for rango in rangos.findall(rango_entrada):
            try:
                ini_str, fin_str = rango.split("-")
            except:     # x-y-z... ¿Triple rango? ¿De qué vas?
                continue
            try:
                ini = numero.findall(ini_str.upper().replace(" ", ""))[0]
                fin = numero.findall(fin_str.upper().replace(" ", ""))[0]
            except IndexError:  # ¿Rango de algo que no contiene un número? Tú flipas.
                continue
            if fin < ini:
                ini, fin = fin, ini
            letra_codigo = letras.findall(ini)
            if len(letra_codigo) == 0:
                letra_codigo = letras.findall(fin)
                if len(letra_codigo) == 0:
                    continue
            letra_codigo = letra_codigo[0]
            res += ["%s%d" % (letra_codigo, i) for i in xrange(ini, fin+1) if "%s%d" % (letra_codigo, i) not in res]
        for suelto in sueltos.findall(rango_entrada):
            num = suelto.upper().replace(" ", "")
            if num not in res:
                res.append(num)
    return res


def dialogo_pedir_rango(titulo = "INTRODUZCA RANGO",
                        texto = "Introduzca un número o un rango de números separado por guión.\n\nEjemplos válidos:\n  100, 105\n  100-110, 105 107\n  etc...",
                        padre = None,
                        valor_por_defecto = "", 
                        permitir_repetidos = False
                       ):
    """
    Muestra un diálogo donde introducir un rango de números o lista separada
    por comas o espacios, o todo a la vez.
    Devuelve un iterable con los NÚMEROS que entran en el rango o None si se
    cancela el diálogo.
    OJO: No acepta números negativos.
    """
    rangos = re.compile("\d+[ ]*-[ ]*\d+")
    sueltos = re.compile("\d+")
    res = None
    rango_entrada = dialogo_entrada(titulo = titulo, texto = texto, padre = padre, valor_por_defecto = valor_por_defecto)
    if rango_entrada != '' and rango_entrada != None:
        res = []
        for rango in rangos.findall(rango_entrada):
            ini, fin = [int(i) for i in rango.split("-")]
            if fin < ini:
                ini, fin = fin, ini
            res += [i for i in xrange(ini, fin+1) if i not in res]
        for suelto in sueltos.findall(rango_entrada):
            num = int(suelto)
            if permitir_repetidos or num not in res:
                res.append(num)
    return res

def enviar_correoe(remitente, 
                   destinos, 
                   asunto, 
                   texto, 
                   adjuntos = [], 
                   servidor = "localhost", 
                   usuario = None, 
                   password = None, 
                   ssl = False):
    """
    Envía un correo electrónico a las direcciones contenidas en la lista 
    "destinos" con los adjuntos de la lista y a través del servidor "servidor".
    Si usuario y contraseña != None, se usarán para hacer login en el 
    servidor SMTP.
    Devuelve True si se envió el correo electrónico sin problemas.
    AL LORO: El viruscan de los windows de los ordenadores de oficina 
    BLOQUEA las conexiones salientes al puerto 25.
    OJO: Si el servidor es gmail, como solo admite autenticación por SSL, se 
    machaca el valor del parámetro «ssl» a True.
    """
    if (servidor.endswith("gmail.com") or servidor.endswith("google.com") 
        or servidor.endswith("googlemail.com")):
        ssl = True
    #print "remitente", remitente
    #print "destinos", destinos
    #print "asunto", asunto
    #print "texto", texto
    #print "adjuntos", adjuntos
    #print "servidor", servidor
    #print "usuario", usuario
    #print "password", password
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEBase import MIMEBase
    from email.MIMEText import MIMEText
    from email.Utils import COMMASPACE, formatdate
    from email import Encoders

    assert type(destinos) is list
    assert type(adjuntos) is list

    ok = False
    if not destinos:
        return False

    msg = MIMEMultipart()
    # XXX
    msg.set_charset("utf8")
    # XXX
    msg['From'] = remitente
    msg['To'] = COMMASPACE.join(destinos)
    msg['Date'] = formatdate(localtime = True)
    # XXX
    try:
        pass
        #asunto = asunto.decode("utf8")
    except:
        pass
    try:
        #texto = texto.decode("utf8").encode("8859")
        pass
    except:
        pass
    # XXX
    msg['Subject'] = asunto

    msg.attach(MIMEText(texto, "plain", "utf8"))

    for fich in adjuntos:
        #print fich
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(fich,"rb").read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 
                        'attachment; filename="%s"' % os.path.basename(fich))
        msg.attach(part)
        #print part
    try:
        from socket import error as socket_error
        if not ssl:
            smtp = smtplib.SMTP(servidor)
        else:
            smtp = smtplib.SMTP(servidor, 587)
    except socket_error, msg:
        dialogo_info(titulo = "ERROR CONECTANDO A SERVIDOR SMTP", 
                     texto = "Ocurrió el siguiente error al conectar al "
                             "servidor de correo saliente:\n%s\n\n"
                             "Probablemente se deba a la configuración de su "
                             "firewall\no a que su antivirus está bloqueando"
                             " las conexiones salientes al puerto 25." % (msg))
        ok = False
    else:
        if ssl:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
        try:
            if usuario and password:
                smtp.login(usuario, password)
            response = smtp.sendmail(remitente, destinos, msg.as_string())  # @UnusedVariable
            ok = True
        except smtplib.SMTPAuthenticationError, msg:
            dialogo_info(titulo = "ERROR AUTENTICACIÓN", 
                         texto = "Ocurrió un error al intentar la autentificación en el servidor:\n\n%s" % (msg))
            ok = False
        except (smtplib.SMTPRecipientsRefused, smtplib.SMTPSenderRefused), msg:
            print "utils.py (enviar_correoe) -> Excepción: %s" % (msg)
            ok = False
        except (smtplib.SMTPServerDisconnected), msg:
            print "utils.py (enviar_correoe) -> Desconectado. ¿Timeout? Excepción: %s" % (msg)
            ok = False
        smtp.close()
    return ok

def cmp_fecha_id(obj1, obj2):
    """
    Función de comparación (para .sort) entre objetos.
    Deben tener campo fecha.
    Si fecha es None, compara por ID.
    """
    if obj1 == None and obj2 == None:
        return 0
    if obj1 != None and obj2 == None:
        return -1
    if obj1 == None and obj2 != None:
        return 1
    if hasattr(obj1, "fecha") and obj1.fecha and hasattr(obj2, "fecha") and obj2.fecha:
        if obj1.fecha < obj2.fecha:
            return -1
        if obj1.fecha > obj2.fecha:
            return 1
        return 0
    if hasattr(obj1, "fecha") and obj1.fecha and (not hasattr(obj2, "fecha") or not obj2.fecha):
        return -1
    if (not hasattr(obj1, "fecha") or not obj1.fecha) and hasattr(obj2, "fecha") and obj2.fecha:
        return 1
    # No fecha. Comparo por ID: OJO: ID son LONGS, no enteros. Las funciones de ordenación SIEMPRE deben devolver enteros.
    return int(obj1.id - obj2.id)

def pedir_producto_compra(padre = None, proveedor = None):
    """
    Ofrece una búsqueda de producto de compra por código o descripción.
    Devuelve un objeto producto o None si se canceló; y el texto buscado.
    padre -> Ventana padre para los diálogos.
    proveedor -> Si es != None, sólo buscará entre los productos de ese 
    proveedor.
    """
    from framework import pclases
    producto = None
    codigo_o_descripcion = dialogo_entrada(titulo = "BUSCAR PRODUCTO", 
                    texto = "Introduzca código o descripción del producto:", 
                    padre = padre)
    if codigo_o_descripcion != None:
        productos = pclases.ProductoCompra.select(pclases.OR(
          pclases.ProductoCompra.q.codigo.contains(codigo_o_descripcion), 
          pclases.ProductoCompra.q.descripcion.contains(codigo_o_descripcion)))
        if proveedor == None:
            # productos = list(productos)
            productos = [p for p in productos if not p.obsoleto]
        else:
            productos = [p for p in productos if not p.obsoleto 
                         and proveedor in p.proveedores]
        if len(productos) > 1:
            filas = [(p.id, p.codigo, p.descripcion, 
                      ", ".join([pro.nombre for pro in p.proveedores])) 
                     for p in productos]
            idproducto = dialogo_resultado(filas, 
                                "SELECCIONE PRODUCTO", 
                                padre, 
                                ("ID", "Código", "Descripción", "Proveedor"))
            try:
                producto = pclases.ProductoCompra.get(idproducto)
            except:
                pass
        elif len(productos) == 1:
            producto = productos[0]
        else:
            if proveedor != None:
                dialogo_info(titulo = "PRODUCTO NO ENCONTRADO", 
                             texto = "No se encontró el producto o bien el "
                                     "mismo no    \nha sido servido nunca "
                                     "por %s." % (proveedor.nombre), 
                             padre = padre)
            else:
                dialogo_info(titulo = "PRODUCTO NO ENCONTRADO", 
                             texto = "      No se encontró el producto.     ", 
                             padre = padre)
    return producto, codigo_o_descripcion
            
def orden_por_fecha_entrega_o_id(ldp1, ldp2):
    """
    Ordena por fecha entrega e ID. Fecha entrega tiene preferencia.
    LDP1 < LDP2 si LDP1 tiene fecha entrega o su ID es menor.
    """
    if ldp1.fechaEntrega and ldp2.fechaEntrega:
        if ldp1.fechaEntrega < ldp2.fechaEntrega:
            return -1
        if ldp1.fechaEntrega > ldp2.fechaEntrega:
            return 1
        return 0
    elif ldp1.fechaEntrega and not ldp2.fechaEntrega:
        return -1
    elif not ldp1.fechaEntrega and ldp2.fechaEntrega:
        return 1
    elif not ldp1.fechaEntrega and not ldp2.fechaEntrega:
        if ldp1.id < ldp2.id:
            return -1
        elif ldp1.id > ldp2.id:
            return 1
        return 0
    return 0

def orden_por_campo_o_id(objeto1, objeto2, campo):
    """
    Ordena por el campo recibido e ID. «campo» tiene preferencia.
    objeto1 < objeto2 si objeto1 tiene valor de campo o su ID es menor.
    """
    if hasattr(objeto1, campo) and getattr(objeto1, campo) != None and \
       hasattr(objeto2, campo) and getattr(objeto2, campo) != None:
        if getattr(objeto1, campo) < getattr(objeto2, campo):
            return -1
        if getattr(objeto1, campo) > getattr(objeto2, campo):
            return 1
        return 0
    elif hasattr(objeto1, campo) and getattr(objeto1, campo) != None and \
         hasattr(objeto2, campo) and getattr(objeto2, campo) == None:
        return -1
    elif hasattr(objeto1, campo) and getattr(objeto1, campo) == None and \
         hasattr(objeto2, campo) and getattr(objeto2, campo) != None:
        return 1
    elif hasattr(objeto1, campo) and getattr(objeto1, campo) == None and \
         hasattr(objeto2, campo) and getattr(objeto2, campo) == None:
        if objeto1.id < objeto2.id:
            return -1
        elif objeto1.id > objeto2.id:
            return 1
        return 0
    return 0

def abs_mxfecha(fecha):
    """
    Devuelve la fecha "absoluta" (esto es, sin horas, minutos, segundos, etc.; 
    o, más bien, con la hora puesta a 0) partiendo de la fecha recibida.
    Útil para comparar dos fechas, una (o las dos) de ellas contiene además 
    la hora y sólo interesa saber si comparten fecha (día concreto, vamos).
    """
    return mx.DateTime.DateTimeFrom(day = fecha.day, 
                                    month = fecha.month, 
                                    year = fecha.year) 
                                    # hour, minutes... por defecto son 0

def cmp_abs_mxfecha(f1, f2):
    """
    Función de comparación para ordenación de fechas ignorando hora del día.
    """
    if abs_mxfecha(f1) < abs_mxfecha(f2):
        return -1
    elif abs_mxfecha(f1) > abs_mxfecha(f2):
        return 1
    else:
        return 0

def acortar_palabra_con_tilde(w):
    """
    Separa la palabra por trozos en cada tilde y devuelve el trozo más 
    largo de ellos.
    Útil para hacer búsquedas "tilde-insensitives" a costa de perder un poco 
    de precisión.
    """
    # VERY ULTRA ÜBER UGLY HACK. En Windows el abecedario ya trae tildes y no 
    # veas la que me está liando.
    if len(string.letters) > 52:
        no_tildes = string.letters[:string.letters.index("z") + 1] + "1234567890"# ñÑüÜ.,-_"
    else:
        no_tildes = string.letters + "123456790"
    # CWT: Para que Iván B. pueda buscar A-4 y C/L, es necesario incluir estos 
    # símbolos 
    no_tildes += "-/"
    w += " "    # UGLY DIRTY HACK de mi propio algoritmo. Esto es para cortar 
                # al final de la palabra y que entre en la actualización de 
                # mas_larga si fuera necesario.
    mas_larga = [0, ""]
    i = 0
    _w = ""
    for l in w:
        if l in no_tildes:
            i += 1
            _w += l
        else:
            if i > mas_larga[0]:
                mas_larga = [i, _w]
            i = 0
            _w = ""
    return mas_larga[1]

def buscar_productos_compra(a_buscar, incluir_obsoletos = False):
    """
    Devuelve un resultselect con los productos 
    de compra que contengan el texto "a_buscar" 
    en el código o la descripción
    """
    ## unit testing (doctest style):
    # >>> from framework import pclases, utils
    # >>> pcs = utils.buscar_productos_compra("0")
    # >>> c = pcs.count()
    # >>> pcs[0].obsoleto = True
    # >>> assert pcs.count() == c - 1
    from framework import pclases
    PC = pclases.ProductoCompra
    _a_buscar = " ".join([acortar_palabra_con_tilde(w) 
                          for w in a_buscar.split()])
    _a_buscar, a_buscar = a_buscar, _a_buscar
    if pclases.DEBUG:
        print "utils::buscar_productos_compra -> «", _a_buscar,
        print "» se ha convertido en «", a_buscar, "»"
    subcriterios = [PC.q.codigo.contains(t) for t in a_buscar.split()]
    if subcriterios:
        crit_codigo = pclases.AND(*subcriterios)
    else:
        crit_codigo = PC.q.codigo.contains(a_buscar)
    subcriterios = [PC.q.descripcion.contains(t) for t in a_buscar.split()]
    if subcriterios:
        crit_descripcion = pclases.AND(*subcriterios)
    else:
        crit_descripcion = PC.q.descripcion.contains(a_buscar)
    try:
        ide = int(a_buscar)
    except (ValueError, TypeError):
        ide = -1
    crit_id = PC.q.id == ide
    #pcs = PC.select(pclases.OR(crit_codigo, 
    #                           crit_descripcion, 
    #                           crit_id), 
    #                orderBy = "descripcion")
    if not incluir_obsoletos:
        pcs = PC.select(pclases.AND(pclases.OR(crit_codigo, 
                                               crit_descripcion, 
                                               crit_id), 
                                    PC.q.obsoleto == False), 
                        orderBy = "descripcion")
    else:
        pcs = PC.select(pclases.OR(crit_codigo, 
                                   crit_descripcion, 
                                   crit_id), 
                        orderBy = "descripcion")
    return pcs

def buscar_productos_venta(a_buscar, incluir_obsoletos = False):
    """
    Busca entre los productos de venta el texto "a_buscar"
    en los campos de código, nombre o descripción. Al resultado
    le añade los productos que contengan "a_buscar" en el campo
    "codigoComposan" de la tabla campos_especificos_rollo.
    Devuelve una lista de objetos productoVenta.
    """
    from framework import pclases
    criterio = pclases.OR(pclases.ProductoVenta.q.codigo.contains(a_buscar),
                        pclases.ProductoVenta.q.nombre.contains(a_buscar),
                        pclases.ProductoVenta.q.descripcion.contains(a_buscar))
    prods = pclases.ProductoVenta.select(criterio)
    rollos = pclases.CamposEspecificosRollo.select(
                pclases.CamposEspecificosRollo.q.codigoComposan == a_buscar)
    productos = [p for p in prods]
    productos += [p.productosVenta[0] for p in rollos 
        if len(p.productosVenta) == 1 and p.productosVenta[0] not in productos]
    if not incluir_obsoletos:
        productos = [p for p in productos if not p.obsoleto]
    return productos

def buscar_producto_general(padre = None, 
                            mostrar_precios = False, 
                            texto_defecto = "", 
                            incluir_sin_iva = True, 
                            saltar_dialogo = False, 
                            single_result = False):
    """
    Recibe la ventana padre y devuelve una lista de 
    objetos producto de compra o de venta o una lista 
    vacía si no se encuentra.
    Muestra una ventana donde introducir un código, código de 
    Composan, descripción completa o nombre y realiza la 
    búsqueda en las tablas de producto_compra y producto_venta.
    Si «saltar_dialogo» es True va directamente a los resultados de 
    la palabra sugerida en "texto_defecto".
    Si «single_result» es True, devuelve un único valor (el primero de la 
    posible lista) o None, y no muestra el diálogo de "refinar búsqueda".
    """
    # FIXME: Esta función está como el culo de tanto parchearla. Tengo que 
    # definir un contrato en condiciones para ella y hacer que los parámetros 
    # sean coherentes entre sí.
    from framework import pclases
    res = []
    if not saltar_dialogo:
        a_buscar = dialogo_entrada(titulo = "BUSCAR PRODUCTO", 
                    texto = "Introduzca código o descripción del producto:", 
                    valor_por_defecto = texto_defecto, 
                    padre = padre)
    else:
        a_buscar = texto_defecto
    tarifas = []
    for t in pclases.Tarifa.select(orderBy = "nombre"):
        if t.vigente:
            tarifas.append(t)
    cambiar_orden_pvp = lambda tarifa: \
      ("VENTA" in tarifa.nombre.upper() and "BLICO" in tarifa.nombre.upper()) \
      or "PVP" in tarifa.nombre.upper().replace(".", "")

    if a_buscar != None:
        productos_compra = buscar_productos_compra(a_buscar)
        productos_venta = buscar_productos_venta(a_buscar)
        resultados = []
        for pc in productos_compra:
            resultados.append(["PC:%d" % (pc.id), pc.codigo, pc.descripcion])
            if mostrar_precios:
                resultados[-1].append(float2str(pc.precioDefecto))
                for tarifa in tarifas:
                    preciotarifa = tarifa.obtener_precio(pc)
                    if cambiar_orden_pvp(tarifa):
                        if incluir_sin_iva:
                            resultados[-1].insert(3, "%s (%s %%)" % (
                                float2str(preciotarifa), 
                                float2str(tarifa.get_porcentaje(pc, 
                                            precio_cache = preciotarifa), 1))
                                )
                            resultados[-1].insert(4, "%s" % (
                                float2str(preciotarifa * 1.21)))
                        else:
                            resultados[-1].insert(3, "%s (%s %%)" % (
                                float2str(preciotarifa * 1.21), 
                                float2str(tarifa.get_porcentaje(pc, 
                                    precio_cache = preciotarifa), 1))
                                )
                    else:
                        if incluir_sin_iva:
                            resultados[-1].append("%s (%s %%)" % (
                                float2str(preciotarifa), 
                                float2str(tarifa.get_porcentaje(pc, 
                                    precio_cache = preciotarifa), 1))
                                )
                            resultados[-1].append("%s" % (float2str(
                                preciotarifa * 1.21)))
                        else:
                            resultados[-1].append("%s (%s %%)" % (
                                float2str(preciotarifa * 1.21), 
                                float2str(tarifa.get_porcentaje(pc, 
                                    precio_cache = preciotarifa), 1))
                                )
        for pv in productos_venta:
            resultados.append(["PV:%d" % (pv.id), pv.codigo, pv.descripcion])
            if mostrar_precios:
                resultados[-1].append(float2str(pv.precioDefecto))
                for tarifa in tarifas:
                    preciotarifa = tarifa.obtener_precio(pv)
                    if cambiar_orden_pvp(tarifa):
                        if incluir_sin_iva:
                            resultados[-1].insert(3, "%s (%s %%)" % (float2str(preciotarifa), 
                                                  float2str(tarifa.get_porcentaje(pv, precio_cache = preciotarifa), 1)))
                            resultados[-1].insert(4, "%s" % (float2str(preciotarifa * 1.21)))
                        else:
                            resultados[-1].insert(3, "%s (%s %%)" % (float2str(preciotarifa * 1.21), 
                                                  float2str(tarifa.get_porcentaje(pv, precio_cache = preciotarifa), 1))
                                                 )
                    else:
                        if incluir_sin_iva:
                            resultados[-1].append("%s (%s %%)" % (float2str(preciotarifa), 
                                                          float2str(tarifa.get_porcentaje(pv, precio_cache = preciotarifa), 1)))
                            resultados[-1].append("%s" % (float2str(preciotarifa * 1.21))) 
                        else:
                            resultados[-1].append("%s (%s %%)" % (float2str(preciotarifa * 1.21), 
                                                  float2str(tarifa.get_porcentaje(pv, precio_cache = preciotarifa), 1))
                                                 )
        if mostrar_precios:
            # cabeceras = ["ID", "Código", "Descripción", "Precio defecto (s/IVA)"] + ["%s (c/IVA)" % tarifa.nombre for tarifa in tarifas]
            cabeceras = ["ID", "Código", "Descripción", "Precio defecto (s/IVA)"]
            for tarifa in tarifas:
                if cambiar_orden_pvp(tarifa):
                    if incluir_sin_iva:
                        cabeceras.insert(3, "%s (s/IVA)" % tarifa.nombre)
                        cabeceras.insert(4, "%s (c/IVA)" % tarifa.nombre)
                    else:
                        cabeceras.insert(3, "%s (c/IVA)" % tarifa.nombre)
                else:
                    if incluir_sin_iva:
                        cabeceras += ["%s (s/IVA)" % tarifa.nombre]
                    cabeceras += ["%s (c/IVA)" % tarifa.nombre] 
        else:
            cabeceras = ("ID", "Código", "Descripción")
        if len(resultados):
            if single_result:
                idsproducto = [resultados[0][0]]
            else:
                idsproducto = dialogo_resultado(resultados, 
                                         "Seleccione uno o varios productos", 
                                         multi = True, 
                                         padre = padre, 
                                         cabeceras = cabeceras, 
                                         maximizar = True)
        else:
            idsproducto = []
        if idsproducto != [-1]:
            for tipo_id in idsproducto:
                tipo, ide = tipo_id.split(":")
                try:
                    ide = int(ide)
                except ValueError:
                    continue
                if tipo == "PC":
                    res.append(pclases.ProductoCompra.get(ide))
                elif tipo == "PV":
                    res.append(pclases.ProductoVenta.get(ide))
            if res == []:
                try:
                    res = sugerir_alternativa(a_buscar, 
                                              padre, 
                                              mostrar_precios, 
                                              incluir_sin_iva)
                    if res is None:
                        res = []        # Porque se espera una lista como 
                                        # valor devuelto.
                        raise ValueError # Por aprovechar la rama "except".
                except (ImportError, ValueError):
                    dialogo_info(titulo = "NO ENCONTRADO", 
                                 texto = 
                            "No se econtraron productos con la búsqueda «%s»." 
                                % (a_buscar),
                                 padre = padre)
    if single_result:
        try:
            res = res[0]
        except IndexError:
            res = None
    return res

def sugerir_alternativa(txt, padre, mostrar_precios, incluir_sin_iva):
    """
    Muestra un cuadro de diálogo con algún texto parecido a «txt» según el 
    "corrector Norving".
    Devuelve un producto, si se optó por la alternativa; una lista vacía si 
    se rechazó y None si no se encontró nada parecido.
    """
    from lib import spelling
    palabras = []
    from framework import pclases
    for pc in pclases.ProductoCompra.select():
        palabras.append(pc.codigo.lower())
        palabras.append(pc.descripcion.lower())
    for pc in pclases.ProductoVenta.select():
        palabras.append(pc.codigo.lower())
        palabras.append(pc.descripcion.lower())
    palabras = " ".join(palabras)
    corrector = spelling.SpellCorrector(palabras)
    sugerencia = corrector.correct(txt.lower())
    if sugerencia != txt.lower():
        res = dialogo(titulo = "SUGERENCIA DE BÚSQUEDA", 
                texto = "No se encontró «%s», ¿tal vez quiso decir «%s»?" % (
                txt, sugerencia), 
                padre = padre)
        if res:
            return buscar_producto_general(padre, 
                                           mostrar_precios, 
                                           sugerencia, 
                                           incluir_sin_iva, 
                                           saltar_dialogo = True)
        else:
            return []
    else:
        return None

def buscar_proveedor(nombre, incluir_inhabilitados = False):
    """
    Busca y devuelve un objeto proveedor cuyo nombre contenga a "nombre".
    Si no encuentra ninguno, devuelve None. Si encuentra varios, devuelve 
    una lista de todos ellos.
    """
    from framework import pclases
    if incluir_inhabilitados:
        p = pclases.Proveedor.select(
            pclases.Proveedor.q.nombre.contains(nombre))
    else:
        p = pclases.Proveedor.select(pclases.AND(
            pclases.Proveedor.q.nombre.contains(nombre), 
            pclases.Proveedor.q.inhabilitado == False))
    if p.count() == 0:
        return None
    elif p.count() == 1:
        return p[0]
    else:
        return pclases.SQLtuple(p)
            
    
####################################################
## Utilidades pistola código de barras y básculas ##
####################################################
def get_puerto_serie(puerto = None):
    """
    Devuelve un objeto de pyserial con el 
    puerto correspondiente abierto. None 
    si no se pudo abrir.
    "puerto" es una cadena con el valor del "dev" 
    correspondiente: COM1, COM2, /dev/ttyS0... o None 
    para buscar el primer puerto serie disponible.
    """
    try:
        import serial
    except ImportError:
        dialogo_info(titulo = "ERROR IMPORTACIÓN", 
                     texto = "Debe instalar el módulo pyserial.", 
                     padre = None)
        return None
    if puerto == None:
        com = buscar_puerto_serie()
    else:
        try:
            com = serial.Serial(puerto)
        except:
            com = None
    if com != None:     # Configuración protocolo Eurobil. Misma configuración 
                        # para los Symbol Phaser P360.
        com.baudrate = 9600
        com.bytesize = 8
        com.parity = 'N'
        com.stopbits = 1
        com.timeout = None
        com.timeout = 0.5     # El timeout_add es bloqueante. Leeré cada medio segundo.
    return com

def buscar_puerto_serie():
    """
    Devuelve el primer puerto serie encontrado en 
    el sistema o None si no se contró.
    """
    try:
        import serial
    except ImportError:
        dialogo_info(titulo = "ERROR IMPORTACIÓN", 
                     texto = "Debe instalar el módulo pyserial.", 
                     padre = None)
        return None
    if os.name == "posix":
        try:
            com = serial.Serial("/dev/ttyS0")
        except:
            try:
                com = serial.Serial("/dev/ttyS1")
            except:
                com = None
    else:
        try:
            com = serial.Serial("COM1")
        except:
            try:
                com = serial.Serial("COM2")
            except:
                com = None
    return com

def leer_raw_data(puerto = "COM1", timeout = 30):
    """
    Abre el puerto serie y recibe "en crudo" todos los datos 
    almacenados en el terminal.
    Devuelve una lista con los códigos leídos.
    """
    raw_data = []
    com = get_puerto_serie(puerto)
    if com != None:
        com.timeout = timeout
        raw_data = com.readlines()
        # El P360 manda los códigos separados por \r\n, pero para ello hay que configurarlo:
        # F* -> Resetea el terminal.
        # Cuando aún está mostrando el mensaje de inicio (antes de que aparezca "scan") pulsar F y a continuación BK.
        # En el menú "0: System setup" -> "5: Set scan options" -> "3. DATA SUFFIX".
        # En el mismo submenú: "6. Edit Suffix Code" (por defecto 7013 = \r\n).
    return raw_data

def descargar_phaser(logger = None, datos = None):
    """
    Abre el puerto serie, lee los códigos del terminal de códigos de barras, 
    "parsea" los códigos almacenados y devuelve una lista de objetos rollo, 
    bala o bigbag correspondientes a esos códigos.
    Entre lista y lista de códigos (si hay más de una) debe haber un código 
    "especial" de la forma 'Axxxx', que indican un número de albarán.
    En ese caso, lo que devuelve es un diccionario con el objeto albarán como 
    clave y la lista de códigos de cada albarán como valores.
    De la misma forma, si lo que se leen son códigos "PCxxxx" se devuelve un 
    diccionario similar pero con partidas de carga como claves (aunque en 
    realidad los códigos de partida de carga no llevan sufijo, algo que 
    tarde o temprano habrá que cambiar).
    Si no consigue leer nada, devuelve None.
    Si "logger" es != None, se usará para volcar al log las incidencias.
    NOTA: Si un código se encuentra repetido, se devuelve una sola vez.
          Si un código tiene menos de 13 dígitos pero no comienza con ninguna 
          letra, se considerará un rollo (que son los más propensos a tener 
          etiquetas defectuosas por estar a la intemperie y equivocarse el 
          almacenista no tecleando la R manualmente).
          Si un código no coincide con nada de lo contemplado (bala, rollo, 
          bigbag o albarán) no se devuelve. Esto se hace así para filtrar, 
          por ejemplo, los EAN13 leídos por error.
    DEBUG: Si datos != None procesa la cadena recibida como si la hubiese 
           descargado del terminal.
    """
    if datos == None:
        i = 0
        while i < 2 and not datos:
            # Lo intento dos veces porque no tengo control ninguno de errores y a veces en el primer intento 
            # la pistola no devuelve nada aunque no se haya llegado al timeout (y no sé cómo detectar un timeout desde el objeto Serial).
            datos = leer_raw_data("COM1")
            i += 1
    else:
        datos = datos.split()
    lista_articulos = []    # Lista de rollos, bigbags y balas leídos.
    dic_articulos = {}      # Diccionario organizado por albaranes o partidas de carga, si fuera necesario.
    if datos != []:
        from framework import pclases
        clave = None
        for codigo in datos:
            codigo = codigo.strip()
            objeto = procesar_codigo(codigo, logger)
            if isinstance(objeto, (pclases.AlbaranSalida, pclases.PartidaCarga)):   # Encolar partida de carga o albarán.
                if objeto not in dic_articulos:
                    dic_articulos[objeto] = []
                if clave != None:
                    dic_articulos[clave] += lista_articulos
                clave = objeto
                lista_articulos = []
            elif objeto != None:                                                    # Encolar rollos, bigbags o balas.
                if objeto not in lista_articulos:       # Ignoro los repetidos
                    lista_articulos.append(objeto)
        if clave != None:
            dic_articulos[clave] += lista_articulos
    else:
        return None
    if dic_articulos == {}:
        return lista_articulos
    else:
        return dic_articulos

def procesar_codigo(codigo, logger = None):
    """
    Devuelve un objeto de la clase correspondiente al código 
    o None si no se pudo encontrar el código o determinar la clase.
    """
    objeto = None
    if codigo.startswith("A"):      # Procesar albaran
        objeto = procesar_albaran(codigo, logger)
    elif codigo.startswith("R"):    # Procesar rollo
        objeto = procesar_rollo(codigo, logger)
    elif codigo.startswith("B"):    # Procesar bala
        objeto = procesar_bala(codigo, logger)
    elif codigo.startswith("Y"):    # Procesar geotextil C.
        objeto = procesar_gtxc(codigo, logger)
    elif codigo.startswith("C"):    # Procesar bigbag
        objeto = procesar_bigbag(codigo, logger)
    elif codigo.startswith("PC"):    # Procesar partida de carga
        objeto = procesar_partida_carga(codigo, logger)
    else:   # O es un EAN13 por error, o se ha metido manualmente sin la letra inicial.
        if 5 < len(codigo) < 13:    # Asumo rollo
            codigo = "R%s" % (codigo)
            objeto = procesar_rollo(codigo, logger)
        elif len(codigo) <= 5:      # Asumo número de albarán
            codigo = "A%s" % (codigo)
            objeto = procesar_albaran(codigo, logger)
        else:
            txt = "IGNORO CÓDIGO %s" %(codigo)
            if logger != None:
                logger.warning(txt)
            else:
                print txt
    return objeto

def procesar_albaran(codigo, logger = None):
    """
    Busca un albarán con número `codigo.replace("A", "")` y devuelve 
    el objeto encontrado o None si no se encontró.
    """
    from framework import pclases
    numalbaran = codigo.replace("A", "")
    albaranes = pclases.AlbaranSalida.select(pclases.AlbaranSalida.q.numalbaran == numalbaran)
    if albaranes.count() == 0:
        albaran = None
    elif albaranes.count() > 1:
        txt = "Más de un albarán encontrado con el número %s. Selecciono el último." % (numalbaran)
        if logger != None:
            logger.warning(txt)
        else:
            print txt
        albaran = albaranes[-1]
    else:
        albaran = albaranes[0]
    return albaran

def procesar_rollo(codigo, logger = None):
    """
    Busca un rollo con el código recibido y devuelve 
    el objeto encontrado o None si no se encontró.
    """
    from framework import pclases
    rollos = pclases.Rollo.select(pclases.Rollo.q.codigo == codigo)
    if rollos.count() == 0:
        rollo = None
    elif rollos.count() > 1:
        txt = "Más de un rollo encontrado con el código %s. Selecciono el primero que esté en almacén." % (codigo)
        if logger != None:
            logger.warning(txt)
        else:
            print txt
        try:
            rollo = [r for r in rollos if r.albaranSalida == None][0]
        except IndexError:
            txt = "Ninguno en almacén. Devuelvo None"
            if logger != None:
                logger.warning(txt)
            else:
                print txt
    else:
        rollo = rollos[0]
    return rollo

def procesar_bala(codigo, logger = None):
    """
    Busca un bala con el código recibido y devuelve 
    el objeto encontrado o None si no se encontró.
    """
    from framework import pclases
    balas = pclases.Bala.select(pclases.Bala.q.codigo == codigo)
    if balas.count() == 0:
        bala = None
    elif balas.count() > 1:
        txt = "Más de un bala encontrado con el código %s. Selecciono el primero que esté en almacén." % (codigo)
        if logger != None:
            logger.warning(txt)
        else:
            print txt
        try:
            bala = [b for b in balas if b.en_almacen()][0]
        except IndexError:
            txt = "Ninguno en almacén. Devuelvo None"
            if logger != None:
                logger.warning(txt)
            else:
                print txt
    else:
        bala = balas[0]
    return bala

def procesar_bigbag(codigo, logger = None):
    """
    Busca un bigbag con el código recibido y devuelve 
    el objeto encontrado o None si no se encontró.
    """
    from framework import pclases
    bigbags = pclases.Bigbag.select(pclases.Bigbag.q.codigo == codigo)
    if bigbags.count() == 0:
        bigbag = None
    elif bigbags.count() > 1:
        txt = "Más de un bigbag encontrado con el código %s. Selecciono el primero que esté en almacén." % (codigo)
        if logger != None:
            logger.warning(txt)
        else:
            print txt
        try:
            bigbag = [r for r in bigbags if r.albaranSalida == None][0]
        except IndexError:
            txt = "Ninguno en almacén. Devuelvo None"
            if logger != None:
                logger.warning(txt)
            else:
                print txt
    else:
        bigbag = bigbags[0]
    return bigbag

def procesar_gtxc(codigo, logger = None):
    """
    Busca un geotextil C con el código recibido y devuelve 
    el objeto encontrado o None si no se encontró.
    """
    from framework import pclases
    gtxcs = pclases.RolloC.select(pclases.RolloC.q.codigo == codigo)
    if gtxcs.count() == 0:
        gtxc = None
    elif gtxcs.count() > 1:
        txt = "Más de un geotextil C encontrado con el código %s. Selecciono el primero que esté en almacén." % (codigo)
        if logger != None:
            logger.warning(txt)
        else:
            print txt
        try:
            gtxc = [r for r in gtxcs if r.albaranSalida == None][0]
        except IndexError:
            txt = "Ninguno en almacén. Devuelvo None"
            if logger != None:
                logger.warning(txt)
            else:
                print txt
    else:
        gtxc = gtxcs[0]
    return gtxc

def procesar_partida_carga(codigo, logger = None):
    """
    Busca una partida carga con número `codigo.replace("PC", "")` y devuelve 
    el objeto encontrado o None si no se encontró.
    """
    from framework import pclases
    #numpartida_carga = codigo.replace("PC", "")
    #partidas_carga = pclases.PartidaCarga.select(pclases.PartidaCarga.q.codigo == numpartida_carga)
    partidas_carga = pclases.PartidaCarga.select(pclases.PartidaCarga.q.codigo == codigo)
    if partidas_carga.count() == 0:
        partida_carga = None
    elif partidas_carga.count() > 1:
        txt = "Más de una partida de carga encontrada con el código %s. Selecciono el último." % (codigo)
        if logger != None:
            logger.warning(txt)
        else:
            print txt
        partida_carga = partidas_carga[-1]
    else:
        partida_carga = partidas_carga[0]
    return partida_carga

def unir_fecha_y_hora(mxfecha, mxhora):
    """
    Devuelve un DateTime con la fecha "mxfecha" y la hora "mxhora".
    Acepta DateTime y DateTimeDelta como parte «hora».
    """
    dia = mxfecha.day; mes = mxfecha.month; anno = mxfecha.year
    hora = mxhora.hour; minuto = mxhora.minute; segundo = mxhora.second
    fecha_mas_hora = mx.DateTime.DateTimeFrom(day = dia, month = mes, year = anno, 
                                              hour = hora, minute = minuto, second = segundo)
    return fecha_mas_hora

def parse_numero(cad, invertir = False):
    """
    Devuelve el primero de los números que se pueda extraer 
    de la cadena cad o None si no contiene ninguna cifra.
    Si invertir == True, devuelve el primer número encontrado por el final.
    """
    regexp = re.compile("[0-9]*")
    try:
        ultimo = [int(item) for item in regexp.findall(cad) if item!='']
        if not invertir:
            ultimo = ultimo[0]
        else:
            ultimo = ultimo[-1]
    except (IndexError, ValueError, TypeError):
        ultimo = None
    return ultimo

def parse_float(n):
    """
    "Parsea" un flotante ignorando todo lo que no sean números, 
    signo, «,» y «.».
    """
    if isinstance(n, str):
        n = "".join([l for l in n if l in "0123456789.,+-"])
        return _float(n)
    return float(n)

def parse_formula(_cad, tipo = float):
    """
    Intenta convertir la cadena recibida en un valor numérico del tipo 
    especificado (por defecto, flotante).
    Si no contiene operadores aritméticos o no puede acabar convirtiéndolo 
    todo a un número, devuelve el valor tal y cual le llega.
    """
    EOS = chr(0)    # Necesito un fin de cadena para saber cuándo he 
                    # terminado en el parser.
    cad = _cad + EOS
    operadores = ('=', 'X', 'x', '*', '+', '-', '/', '^', '(', ')')
    intentarlo = False
    for o in operadores:
        if o in cad:
            intentarlo = True
            break
    if not intentarlo:
        try:
            res = tipo(_float(_cad))
        except (ValueError, TypeError):
            res = _cad
    else:
        cad = cad.replace("=", "").replace("x", "*").replace("X", "*")
        tokens = []
        token = ""
        for letra in cad:
            if letra.isdigit():             # Si es número, apilo.
                token += letra
            elif letra not in operadores and letra != EOS:   
                    # Si punto, coma, etc... apilo. 
                token += letra
            else:                           # Operador, trato y siguiente.
                try:
                    token = float2str(_float(token), separador_decimales = ".")
                except (ValueError, TypeError):
                    res = _cad
                    break   # NaN. Me salgo y devuelvo la cadena original. 
                tokens.append(token)
                if letra in operadores:
                    tokens.append(letra)    # Apilo también el operador
                token = ""
        # He acabado de separar valores y formatear los números correctamente.
        # Toca intentar resolver la fórmula:
        expresion = "".join(tokens)
        try:
            res = eval(expresion)
        except: # Petó. Qué mala fuerte, shato.
            res = _cad
        else:
            try:
                res = tipo(res)
            except (TypeError, ValueError):
                res = _cad
    return res


#########################################
#### Utilidades con cadenas de texto ####
#########################################

def eliminar_dobles_espacios(cad):
    """
    Devuelve la cadena "cad" asegurando que no quedan dos espacios consecutivos 
    en ninguna posición.
    """
    if cad:
        return reduce(lambda x, y: x[-1] == " " and y == " " and x or x+y, cad)
    return cad

def corregir_mayusculas_despues_de_punto(cad):
    """
    Devuelve la cadena "cad" con mayúscula siempre después de punto 
    (aunque sea una falta de ortografía si el punto corresponde a una 
    abreviatura).
    """
    res = []
    for subcad in cad.split("."):
        # res.append(subcad.strip().capitalize())   
            # OJO porque al parecer capitalize me jode el encoding y el reportlab+python2.3+MSWindows después se quejan al pasarlo a cp1252
        if len(subcad.strip()) > 1:
            res.append(subcad.strip()[0].upper() + subcad.strip()[1:])
    res = ". ".join(res)
    return res 

###########################################
#### EOUtilidades con cadenas de texto ####
###########################################

def asegurar_fecha_positiva(fecha):
    """
    No estoy seguro de por qué, pero de repente la versión 
    de mx de Sid amd64 ha empezado a devolver -1 como día 
    al operar con la fecha, en lugar de convertir los valores 
    negativos en días desde el final de mes, como siempre.
    Así que lo único que hace esta función es asegurarse de 
    que el día de la fecha es positivo en la fecha devuelta 
    equivalente a la recibida.
    Esta función quedará obsoleta en cuanto se corrija el 
    bug de mx-extension.
    """
    if fecha.day < 1: 
        fecha = mx.DateTime.DateTimeFrom(day = fecha.days_in_month + fecha.day + 1, 
                                         month = fecha.month, 
                                         year = fecha.year)
    return fecha

def unificar(lista):
    """
    Devuelve una lista con valores únicos.
    """
    if not isinstance(lista, (list, tuple)):
        raise TypeError, "lista debe ser una lista, no un %s." % (type(lista))
    res = []
    for i in lista:
        if i not in res:
            res.append(i)
    return res

def unificar_textos(lista, case_sensitive = False):
    """
    Devuelve una lista de textos donde no se repite ninguno. Ignora  
    espacios al principio y al final. Por defecto es "case insensitive". 
    Los textos los devuelve tal y como estén escritos en la primera aparición 
    de ellos en lista.
    """
    if not isinstance(lista, (list, tuple)):
        raise TypeError, "lista debe ser una lista, no un %s." % (type(lista))
    res = []
    for t in lista:
        if case_sensitive:
            tmp = tuple([i.strip() for i in res])
            tmp_t = t.strip()
        else:
            tmp = tuple([i.lower().strip() for i in res])
            tmp_t = t.lower().strip()
        if tmp_t not in tmp:
            res.append(t)
    return res

def wrap(text, width):
    """
    A word-wrap function that preserves existing line breaks
    and most spaces in the text. Expects that existing line
    breaks are posix newlines (\n).
    Sacado de http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/148061
    Desconozco la licencia. Eliminar en caso de que no sea compatible con la 
    GPL cuando la averigüe.
    """
    return reduce(lambda line, word, width=width: '%s%s%s' %
                  (line,
                   ' \n'[(len(line)-line.rfind('\n')-1
                         + len(word.split('\n',1)[0]
                              ) >= width)],
                   word),
                  text.split(' ')
                 )

def update_preview_image(filechooser, preview_image):
    filename = filechooser.get_filename()
    pixbuf = None
    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file(filename)
    except:
        pass
    if pixbuf == None:
        preview_image.set_from_pixbuf(None)
        return
    pixbuf_width = pixbuf.get_width()
    pixbuf_height = pixbuf.get_height()
    if pixbuf_width > 120:
        new_pixbuf_width = 120
        new_pixbuf_height = pixbuf_height*120/pixbuf_width
        pixbuf = pixbuf.scale_simple(new_pixbuf_width, 
                                     new_pixbuf_height, 
                                     gtk.gdk.INTERP_BILINEAR)
    preview_image.set_from_pixbuf(pixbuf)

def dialogo_abrir(titulo = "ABRIR FICHERO", 
                  filtro_imagenes = False, 
                  padre = None, 
                  directorio = None):
    """
    Muestra un diálogo de abrir y devuelve el archivo seleccionado 
    o None.
    Si filtro_imagenes es True, añade al diálogo un filtro de imágenes
    a los archivos que se pueden elegir.
    """
    file_open = gtk.FileChooserDialog(title = titulo,
                                      parent = padre,
                                      action = gtk.FILE_CHOOSER_ACTION_OPEN, 
                                      buttons = (gtk.STOCK_CANCEL, 
                                                 gtk.RESPONSE_CANCEL,
                                                 gtk.STOCK_OPEN,
                                                 gtk.RESPONSE_OK))
    if directorio != None:
        file_open.set_current_folder(directorio)
    if filtro_imagenes:
        """Crear y añadir el filtro de imágenes"""
        filtro = gtk.FileFilter()
        filtro.set_name("Imágenes")
        filtro.add_mime_type("image/png")
        filtro.add_mime_type("image/jpeg")
        filtro.add_mime_type("image/gif")
        filtro.add_pattern("*.png")
        filtro.add_pattern("*.jpg")
        filtro.add_pattern("*.gif")
        file_open.add_filter(filtro)
        # Añadir preview de imágenes.
        browse_preview_image = gtk.Image()
        browse_preview_image.set_size_request(120, -1)
        file_open.set_preview_widget(browse_preview_image)
        file_open.connect("update-preview", update_preview_image, 
                                            browse_preview_image)

    """Crear y añadir el filtro de "todos los archivos"."""
    filtro = gtk.FileFilter()
    filtro.set_name("Todos los ficheros")
    filtro.add_pattern("*")
    file_open.add_filter(filtro)
    """Valor devuelto"""
    result = None
    if file_open.run() == gtk.RESPONSE_OK:
        result = file_open.get_filename()
    file_open.destroy()
    return result

def dialogo_guardar_adjunto(documento, padre = None):
    """
    Muestra una ventana de diálogo para guardar el documento adjunto recibido.
    """
    dialog = gtk.FileChooserDialog("GUARDAR DOCUMENTO ADJUNTO",
                                   None,
                                   gtk.FILE_CHOOSER_ACTION_SAVE,
                                   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                    gtk.STOCK_SAVE, gtk.RESPONSE_ACCEPT))
    dialog.set_default_response(gtk.RESPONSE_OK)
    try:
        home = os.environ['HOME']
    except KeyError:
        try:
            home = os.environ['HOMEPATH']
        except KeyError:
            from tempfile import gettempdir
            home = gettempdir()
            print "WARNING: No se pudo obtener el «home» del usuario"
    if os.path.exists(os.path.join(home, 'tmp')):
        dialog.set_current_folder(os.path.join(home, 'tmp'))
    else:
        dialog.set_current_folder(home)
    dialog.set_current_name(documento.nombre)

    if dialog.run() == gtk.RESPONSE_ACCEPT:
        nomarchivo = dialog.get_filename()
        res = documento.copiar_a(nomarchivo)
        if not res:
            dialogo_info(titulo = "NO SE PUDO GUARDAR", 
                         texto = "Ocurrió un error al guardar el archivo.\n"\
                                 "Pruebe a seleccionar un destino diferente.", 
                         padre = padre)
    dialog.destroy()

def dialogo_adjuntar(titulo, objeto, padre = None):
    """
    Muestra un diálogo y adjunta un fichero a un objeto.
    """
    from os import getenv
    fichero = dialogo_abrir(titulo, 
                            padre = padre, 
                            directorio = getenv("HOME", 
                            os.getenv("SystemDrive")))
    if fichero:
        nombre = dialogo_entrada(titulo = "NOMBRE DOCUMENTO", 
                texto = "Introduzca un nombre descriptivo para el documento:", 
                valor_por_defecto = os.path.split(fichero)[-1], 
                padre = padre)
        if nombre:
            from framework import pclases
            pclases.Documento.adjuntar(fichero, objeto, nombre)

def mover_a_tmp(ruta):
    """
    Mueve el fichero apuntado por "ruta" al directorio temporal del SO.
    """
    from tempfile import gettempdir
    import shutil
    try:
        shutil.move(ruta, gettempdir())
    except IOError:
        print "utils::mover_a_tmp -> Fichero %s no existe." % (ruta)

def buscar_factura(ventana_padre = None, multi = False, filtrar = False, cliente = None, conds_fras = [], conds_pres = []):
    """
    Muestra un diálogo para buscar facturas o prefacturas 
    y devuelve la seleccionada, una lista de seleccionadas 
    o None si se cancela.
    Si filtrar = True muestra antes un diálogo para buscar 
    por número de factura.
    Si cliente != None busca solamente entre las facturas 
    del cliente recibido.
    conds_fras y conds_pres son listas de predicados WHERE 
    de SQLObject que se combinarán con AND al resto de 
    criterios para realizar la búsqueda.
    """
    from framework import pclases
    res = None
    if filtrar:
        a_buscar = dialogo_entrada(titulo = "BUSCAR FACTURA", 
                                   texto = "Introduzca número de factura", 
                                   padre = ventana_padre)
        if a_buscar != None:
            conds_fras.append(pclases.FacturaVenta.q.numfactura.contains(a_buscar))
            conds_pres.append(pclases.Prefactura.q.numfactura.contains(a_buscar))
    if cliente != None:
        conds_fras.append(pclases.FacturaVenta.q.clienteID == cliente.id)
        conds_pres.append(pclases.Prefactura.q.clienteID == cliente.id)
    if len(conds_fras) == 0:
        fras = pclases.FacturaVenta.select()
    elif len(conds_fras) == 1:
        fras = pclases.FacturaVenta.select(conds_fras[0])
    else:
        fras = pclases.FacturaVenta.select(pclases.AND(*conds_fras))
    if len(conds_pres) == 0:
        pres = pclases.Prefactura.select()
    elif len(conds_pres) == 1:
        pres = pclases.Prefactura.select(conds_pres[0])
    else:
        pres = pclases.Prefactura.select(pclases.AND(*conds_pres))
    filas = [("FV:%d" % f.id, f.numfactura, f.cliente and f.cliente.nombre or "", str_fecha(f.fecha)) for f in fras] \
            + [("PF:%d" % f.id, f.numfactura, f.cliente and f.cliente.nombre or "", str_fecha(f.fecha)) for f in pres]
    idfactura = dialogo_resultado(filas, 
                                  titulo = "SELECCIONE FACTURA", 
                                  cabeceras = ["ID", "Número de factura", "Cliente", "Fecha"], 
                                  padre = ventana_padre, 
                                  multi = multi)
    if isinstance(idfactura, (list, tuple)):
        res = []
        if isinstance(idfactura[0], str):
            for idfra in idfactura:
                if idfra.startswith("FV"):
                    res.append(pclases.FacturaVenta.get(int(idfra.split(":")[1])))
                elif idfra.startswith("PF"):
                    res.append(pclases.Prefactura.get(int(idfra.split(":")[1])))
    elif isinstance(idfactura, str):
        if idfactura.startswith("FV"):
            res = pclases.FacturaVenta.get(int(idfactura.split(":")[1]))
        elif idfactura.startswith("PF"):
            res = pclases.Prefactura.get(int(idfactura.split(":")[1]))
    return res

def abrir_factura_venta(ide, num, usuario = None):
    """
    Intenta abrir la factura de venta con clave primaria "ide" 
    y número de factura "num". Si no coincide el num con la 
    factura id es porque no es una factura de venta y 
    devuelve False.
    En otro caso abre la ventana y devuelve True.
    """
    from framework import pclases
    try:
        fra = pclases.FacturaVenta.get(ide)
        print fra
    except pclases.SQLObjectNotFound:
        res = False
        print res
    else:
        if fra.numfactura == num:
            res = True
            from formularios import facturas_venta
            ventana = facturas_venta.FacturasVenta(fra, usuario)  # @UnusedVariable
        else:
            res = False
    return res

def abrir_prefactura(ide, num, usuario = None):
    """
    Intenta abrir la factura proforma con clave primaria "ide" 
    y número de factura "num". Si no coincide el num con la 
    factura id es porque no es una prefactura y 
    devuelve False.
    En otro caso abre la ventana y devuelve True.
    """
    from framework import pclases
    try:
        fra = pclases.Prefactura.get(ide)
    except pclases.SQLObjectNotFound:
        res = False
    else:
        if fra.numfactura == num:
            res = True
            from formularios import prefacturas
            ventana = prefacturas.Prefacturas(fra, usuario)  # @UnusedVariable
        else:
            res = False
    return res

def filtrar_tildes(s):
    """
    Devuelve la cadena s con las vocales tildadas 
    sustituídas por las mismas sin tildar.
    """
    frm = ('á', 'é', 'í', 'ó', 'ú', 'Á', 'É', 'Í', 'Ó', 'Ú')
    to =  ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
    #s = unicode(s, "utf", "replace")
    #s = s.decode("utf")
    for o, d in zip(frm, to):
        s = s.replace(o, d)
    return s

def textview_get_all_text(w):
    """
    Devuelve todo el texto de un textview.
    """
    if not isinstance(w, gtk.TextView):
        raise TypeError, "utils::tv_get_all_text -> El widget debe ser un gtk.TextView."
    buf = w.get_buffer()
    return buf.get_text(*buf.get_bounds())

def image2pixbuf(image):
    """
    http://www.daa.com.au/pipermail/pygtk/2003-June/005268.html
    """
    #import pygtk
    #pygtk.require("2.0")
    #import gtk
    import StringIO
    #import Image
    fich = StringIO.StringIO()
    image.save(fich, 'ppm')
    contents = fich.getvalue()
    fich.close()
    loader = gtk.gdk.PixbufLoader('pnm')
    loader.write(contents, len (contents))
    pixbuf = loader.get_pixbuf()
    loader.close()
    return pixbuf

# XXX: Algoritmos de dígito de control en CCC y letra del DNI:
def cccCRC(cTexto):
    """Cálculo del CRC de un número de 10 dígitos
    ajustados con ceros por la izquierda"""
    factor=(1,2,4,8,5,10,9,7,3,6)
    # Cálculo CRC
    nCRC=0
    for n in range(10):
        nCRC += int(cTexto[n])*factor[n]
    # Reducción del CRC a un dígito
    nValor=11 - nCRC%11
    if nValor==10:
        nValor=1
    elif nValor==11:
        nValor=0
    return nValor

def calcCC(cBanco, cSucursal, cCuenta):
    """Cálculo del Código de Control Bancario"""
    cTexto="00%04d%04d" % (int(cBanco),int(cSucursal))
    DC1 = cccCRC(cTexto)
    cTexto="%010d" % long(cCuenta)
    DC2 = cccCRC(cTexto)
    return "%1d%1d" % (DC1,DC2)

def calcularNIF(dni):
    if isinstance(dni, str):    # Tengo que pasar a número:
        DNI = parse_numero(dni)
    else:
        DNI = dni
    if not isinstance(DNI, int):
        raise TypeError, "El parámetro debe ser un entero o una cadena."
    # DNI=12345678 
    NIF='TRWAGMYFPDXBNJZSQVHLCKE' 
    letra = NIF[DNI % 23]
    # print "El NIF del DNI es", letra
    return letra

# XXX: EOA

def seleccionar_tipo_repuesto(ventana_padre = None):
    """
    Muestra un diálogo con un combo para seleccionar un tipo de repuesto.
    """
    from framework import pclases
    res = None
    tipos = pclases.TipoDeMaterial.select(pclases.OR(
        pclases.TipoDeMaterial.q.descripcion.contains("repuesto"), 
        pclases.TipoDeMaterial.q.descripcion.contains("aceite"), 
        pclases.TipoDeMaterial.q.descripcion.contains("lubricante")))
    if tipos.count() == 0:
        dialogo_info(titulo = "SIN DATOS", 
                     texto = "No hay repuestos dados de alta en los tipos de material.", 
                     padre = ventana_padre)
    else:
        tipos = [(t.id, t.descripcion) for t in tipos]
        idtipo = dialogo_combo(titulo = "SELECCIONE TIPO", 
                               texto = "Seleccione un tipo de material", 
                               padre = ventana_padre, 
                               ops = tipos)
        if idtipo != None:
            res = pclases.TipoDeMaterial.get(idtipo)
    return res

def seleccionar_repuesto(tipo, ventana_padre = None, dejar_crear = True, 
                         proveedor_defecto = None, usuario = None):
    """
    Muestra un dialogo_combo con los productos de compra de repuestos del 
    tipo "tipo". Si dejar_crear = True permite crear un producto no listado.
    """
    from framework import pclases
    res = None
    idtipo = tipo.id
    prods = pclases.ProductoCompra.select(pclases.AND(
        pclases.ProductoCompra.q.tipoDeMaterialID == idtipo, 
        pclases.ProductoCompra.q.obsoleto == False))
    if not dejar_crear:
        if prods.count() == 0:
            dialogo_info(titulo = "SIN DATOS", 
                         texto = "No hay repuestos dados de alta con el "
                            "tipo de material «%s»." % (
                            pclases.TipoDeMaterial.get(idtipo).descripcion), 
                         padre = ventana_padre)
        else:
            prods = [(p.id, p.descripcion) for p in prods]
            idprod = dialogo_combo(titulo = "SELECCIONE PRODUCTO", 
                                   texto = "Seleccione un respuesto:", 
                                   padre = ventana_padre, 
                                   ops = prods)
            if idprod != None:
                res = pclases.ProductoCompra.get(idprod)
    else:
        prods = [(p.id, "%s (%s)" % (p.descripcion, 
                                     float2str(p.existencias, autodec = True))) 
                 for p in prods]
        idprod, txt = dialogo_entrada_combo(titulo = "SELECCIONE PRODUCTO", 
                                            texto = "Seleccione un respuesto:", 
                                            padre = ventana_padre, 
                                            ops = prods)
        if idprod != None:
            res = pclases.ProductoCompra.get(idprod)
        elif txt != None:
            if dialogo(titulo = "¿CREAR PRODUCTO?", 
                       texto = "El producto «%s» no existe.\n¿Desea crearlo?"%(
                        txt), 
                       padre = ventana_padre):
                codigo = ""     # Podría pedirse por diálogo o algo.
                pc = pclases.ProductoCompra(tipoDeMaterial = tipo, 
                                            descripcion = txt, 
                                            controlExistencias = True, 
                                            codigo = codigo, 
                                            obsoleto = False, 
                                            proveedor = proveedor_defecto)
                pclases.Auditoria.nuevo(pc, usuario, __file__)
                res = pc
    return res

def pedir_repuesto(ventana_padre = None, dejar_crear = True, 
                   proveedor_defecto = None, usuario = None):
    """
    Muestra un diálogo con los tipos de material considerados repuestos.
    A continuación muestra otro con los productos de compra dentro de ese 
    tipo de material.
    Si dejar_crear es True, en el segundo diálogo permite introducir un texto 
    que no está en el combo y pregunta si crearlo nuevo.
    Si es False devuelve únicamente uno de los productos mostrados o bien 
    None si se cancela en algún momento.
    """
    res = None
    tipo = seleccionar_tipo_repuesto(ventana_padre)
    if tipo != None:
        producto = seleccionar_repuesto(tipo, ventana_padre, dejar_crear, 
                                        proveedor_defecto, usuario)
        res = producto
    return res

MESES = ("",        # Mes 0 no es enero. Enero es el mes 1.
         "enero", 
         "febrero", 
         "marzo", 
         "abril", 
         "mayo", 
         "junio", 
         "julio", 
         "agosto", 
         "septiembre", 
         "octubre", 
         "noviembre", 
         "diciembre")

def aplanar(l):
    """
    Devuelve una lista "plana" con todos los elementos de l y sus sublistas 
    en el mismo orden en el que se encuentren.
    Por ejemplo: aplanar([[1, 2, 3], [1, 2], 3]) -> [1, 2, 3, 1, 2, 3]
    """
    res = []
    for i in l:
        if isinstance(i, (list, tuple)):
            res += aplanar(i)
        else:
            res.append(i)
    return res

def sort_nicely(l): 
    """ Sort the given list in the way that humans expect. 
    http://www.codinghorror.com/blog/archives/001018.html
    Créditos a Ned Batchelder
    http://nedbatchelder.com/blog/200712.html#e20071211T054956
    OJO: Requiere python 2.4 o superior.
    OJO one more time: Los elementos de la lista deben ser cadenas (algo 
    obvio, por otra parte, porque para enteros no hacen falta estas alforjas). 
    No permite tampoco que la lista sea heterogénea.
    """ 
    if sys.version_info >= (2, 4): 
        #convert = lambda text: int(text) if text.isdigit() else text 
        def convert(text):
            if text.isdigit():
                return int(text)
            else:
                return text
        alphanum_key=lambda key: [convert(c) for c in re.split('([0-9]+)',key)]
        l.sort(key = alphanum_key) 
    else: 
        # Python 2.3, me temo. No soportado. Uso ordenación normal.
        l.sort()

def parse_cif(cif = None):
    """
    Si cif es None, ejecuta tests de todos los posibles.
    Devuelve un cif correcto o la cadena vacía si no se puede obtener un 
    CIF/DNI o CIF internacional válido.
    Formatos reconocidos: 
        * NIF 12345678X
        * CIF X12345678
        * Internacional: XYZ12345678
        * Griego: 123456789
        * Internacional 2: XY123456789
        * República checa: XY12345678
        * Especiales organismos oficiales: X1234567Y
        * Canadienses: 142461409RM0001
        * Gibraltar: 12345 
        * Francia: FR64 384 813 341 00029
        * Polonia: 1234567890
        * México: NNE100120TW0

    En teoría lo siguiente debería valer de unittest con 
    import doctest; doctest.testmod()

    Un par de páginas con los listados de códigos de países y VAT numbers:
    http://www.hmrc.gov.uk/vat/managing/international/esl/country-codes.htm
    http://www.alfanet.es/nif-iva.php
    http://en.wikipedia.org/wiki/VAT_identification_number


    >>> parse_cif("")
    ''
    >>> parse_cif("pendiente")
    'PENDIENTE'
    >>> parse_cif("pendient")
    ''
    >>> parse_cif("00000000T")
    '00000000T'
    >>> parse_cif("A00000000")
    'A00000000'
    >>> parse_cif("XYZ12345678")
    'XYZ12345678'
    >>> parse_cif("123456789")
    '123456789'
    >>> parse_cif("XY123456789")
    'XY123456789'
    >>> parse_cif("X1234567Y")
    'X1234567Y'
    >>> parse_cif("142461409RM0001")
    '142461409RM0001'
    >>> parse_cif("XY12345678")
    'XY12345678'
    >>> parse_cif("FR64 384 813 341 00029")
    'FR64 384 813 341 00029' 
    >>> parse_cif("1234567890")
    '1234567890'
    >>> parse_cif("DKR2013-E3577")
    'DKR2013-E3577'
    >>> parse_cif("12345678")
    '12345678'
    >>> parse_cif("NNE100120TW0")
    'NNE100120TW0'
    """
    # [Update: 29/05/2012] Javi me pasa estos formatos, que son con los que 
    #                      ellos normalmente trabajan:
    if cif is None:
        samples = {'Alemania':    'DE123456789', # DE + 9 números
                   'Bélgica':     'BE0123456789', # BE + 0|1 + 9 números
                   'Bulgaria':    'BG1234567890', # BG + 9 ó 10 números
                   'España':      'ESA23546789', # ES + 9 caracteres. 
                    # Primero y último: letra o dígitos, resto solo dígitos
                   'Francia':     'FRAA123456789', # FR + 2 letras + 9 números
                   'Mónaco':      'FR00123456789', # FR + 11 números
                   'Hungría':     'HU12345678', # HU + 8 números
                   'Italia':      'IT12345678901', # IT + 11 números
                   'Malta':       'MT12345678', # MT + 8 números
                   'Polonia':     'PL1234567890', # PL + 10 números
                   'Portugal':    'PT123456789', # PT + 9 números  
                   'Reino Unido': 'GB123123412123', # GB + 3, 4 y 2 números. 
                                      # Para grupos de empresas 3 números más.
                   'Rumania':     'RO12', # RO + 2 a 10 números.
                   'Irlanda':     'IE 6388047V', # IE + 1 número + letra o número + 5 números + letra.
                  }
        # TEST MODE
        samples['_NIF'] = '00000000T'
        samples['_CIF'] = 'X12345678'
        samples['_Internacional'] = 'XYZ12345678'
        samples['_Griego'] = '123456789'
        samples['_Internacional 2'] = 'XY123456789'
        samples['_República checa'] = 'XY12345678'
        samples['_Especiales organismos oficiales'] = 'X1234567Y'
        samples['_Canadienses'] = '142461409RM0001'
        samples['_Gibraltar'] = '12345'
        samples['_Francia'] = 'FR64 384 813 341 00029'
        samples['_Polonia'] = '1234567890'
        samples['_Senegal'] = 'DKR2013-E3577'   # No conozco exactamente 
                        # el formato. Al parecer allí el equivalente es un 
                        # número C.C. (Compte Contribuable). Pero no 
                        # encuentro más información. Este es el único ejemplo 
                        # que tengo.
        samples['_Marruecos'] = "12345678"
        samples['_México'] = "NNE100120TW0"     # Según el Registro Federal de 
                        # Contribuyentes de México, este formato es: 
                        # 3 caracteres (también valen números) + 6 números + 
                        # otros 3 caracteres alfanuméricos.
        res = {}
        aciertos = 0
        for pais in samples:
            res[pais] = parse_cif(samples[pais])
            # if res[pais]:
            if res[pais].replace(" ", "") == samples[pais].replace(" ", ""):
                aciertos += 1
            else:
                print "Error en %s: %s -> %s" % (pais,samples[pais],res[pais])
        print "WARNING: TEST MODE: %.2f %% aciertos" % (
                aciertos * 100.0 / len(samples.keys()))
    else:
        # PLAN: Chequear que si el CIF/NIF es "españolo", que sea correcto. La 
        # letra es fácil de sacar (y hasta podría metérsela en caso de que solo
        # hubiera 8 números sin letra). La comprobación de NIF de Hacienda no 
        # la conozco, pero debe andar por algún lado, porque el programa de 
        # ayuda del 349 detecta NIF incorrectos.
        cif = str(cif).upper().strip()
        letras = string.letters[string.letters.index("A"):]
        numeros = "0123456789"
        if cif.startswith("FR") or cif.startswith("DKR"):
            cif = cif.replace("\t", " ")
            while "  " in cif:
                cif = cif.replace("  ", " ")
            especiales = " -"   # El espacio, de momento, y por culpa del FR.
                                # También el guión por culpa de Senegal (Dakar)
        else:
            especiales = ""
        cif = "".join([l for l in cif if l in letras or l in numeros 
                                                     or l in especiales])
        rex = re.compile(
                         "(DKR[0-9]{4}-[A-Z][0-9]{4})"
                         "|"
                         "(FR[0-9]{2}\s[0-9]{3}\s[0-9]{3}\s[0-9]{3}\s[0-9]{5})"
                         "|"
                         '(DE[0-9]{9})'
                         "|"
                         '(BE(0|1)[0-9]{9})'
                         "|"
                         '(BG[0-9]{9}[0-9]?)' 
                         "|"
                         '(ES[A-Z][0-9]{8})' 
                         "|"
                         '(ES[0-9]{8}[A-Z])' 
                         "|"
                         '(FR[A-Z0-9]{2}[0-9]{9})' 
                         "|"
                         '(HU[0-9]{8})' 
                         "|"
                         '(IT[0-9]{11})'
                         "|"
                         '(MT[0-9]{8})'
                         "|"
                         '(PL[0-9]{10})'
                         "|"
                         '(PT[0-9]{9})'
                         "|"
                         '(GB[0-9]{9}([0-9]{3})?)' 
                         "|"
                         '(RO[0-9]{2,10})'
                         "|"
                         "(IE[0-9][0-9|A-Z][0-9]{5}[A-Z])"
                         "|"
                         "([A-Z][0-9]{8})"
                         "|"
                         "([A-Z]{2}[0-9]{9})"
                         "|"
                         "([A-Z]{2}[0-9]{8})"
                         "|"
                         "([A-Z]{3}[0-9]{8})"
                         "|"
                         "([A-Z][0-9]{7}[A-Z])"
                         "|"
                         "([0-9]{8}[A-Z])"
                         "|"
                         "([0-9]{9}[A-Z]{2}[0-9]{4})"
                         "|"
                         "([0-9]{10})"
                         "|"
                         "([0-9]{9})"
                         "|"
                         "([0-9]{8})"
                         "|"
                         "([0-9]{5})"
                         "|"
                         "([A-Z0-9]{3}[0-9]{6}[A-Z0-9]{3})"
                        )
        res = rex.findall(cif)
        try:
            res = [i for i in res[0] if i]
                # La posición donde se encuentre dependerá de con qué parte del 
                # patrón coincida:
                # 0 -> NIF 12345678X
                # 1 -> CIF X12345678
                # 2 -> Internacional: XYZ12345678
                # 3 -> Griego: 123456789
                # 4 -> Internacional 2: XY123456789
                # Etc.
            res = res[0]
        except IndexError:
            res = ""
        # CWT: CIFs pendientes, después pasa lo que pasa.
        if cif == "PENDIENTE":
            return cif 
    return res

def set_fecha(entry):
    """
    Muestra el diálogo de selección de fecha y escribe en el «entry» la 
    fecha seleccionada.
    """
    texto = entry.get_text()
    try:
        defecto = parse_fecha(texto)
    except ValueError:
        defecto = mx.DateTime.localtime()
    ventana_padre = None
    padre = entry.parent
    while padre != None:
        padre = padre.parent
    fecha = mostrar_calendario(fecha_defecto = defecto, padre = ventana_padre)
    entry.set_text(str_fecha(fecha))

def cambiar_por_combo(tv, numcol, opts, clase, campo, ventana_padre = None, 
                      entry = False):
    """
    Cambia el cell de la columna «numcoll» del TreeView «tv» por un combo con 
    las opciones recibidas en «opts», que deben respetar el formato 
    (texto, PUID) -ver get_puid y getObjetoPUID de pclases-.
    También se encarga de crear el callback para guardar los cambios.
    «clase» es la clase del objeto al que se le va a actualizar el valor de 
    la clave ajena de entre las opciones disponibles en el combo. Debe 
    recibirse directamente como una clase de pclases (i. e. pclases.Ausencia).
    «campo» es el campo como texto que se va a actualizar. Es decir, el que 
    representa la clave ajena.
    «ventana_padre» servirá como ventana padre para la ventana modal de los 
    posibles avisos de error al guardar los valores seleccionados en el combo.
    """
    from framework.pclases import getObjetoPUID, SQLObjectNotFound
    # Elimino columna actual
    column = tv.get_column(numcol)
    column.clear()
    # Creo model para el CellCombo
    model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING)
    for opt in opts:
        model.append(opt)
    # Creo CellCombo
    cellcombo = gtk.CellRendererCombo()
    cellcombo.set_property("model", model)
    cellcombo.set_property("text-column", 0)
    cellcombo.set_property("editable", True)
    cellcombo.set_property("has-entry", entry)
    # Función callback para la señal "editado"
    def guardar_combo(cell, path, text, model_tv, numcol, model_combo, 
                      entry = False):
        """
        Si el texto escrito se corresponde con algo del model, guarda 
        el entero del store en la clave ajena. Si no, deja el texto 
        escrito y pone la clave ajena a None. Si entry es True, entonces 
        permitirá meter un texto libre sin que dé error por no encontrar el 
        elemento en el store.
        """
        # Es lento, pero no encuentro otra cosa:
        idct = None
        for i in xrange(len(model_combo)):
            texto, ide = model_combo[i]
            if texto == text:
                idct = ide
                break
        if idct == None:
            if not entry:
                dialogo_info(titulo = "ERROR COMBO", 
                  texto = "Ocurrió un error inesperado guardando el valor.\n\n"
                          "Contacte con los desarrolladores de la aplicación\n"
                          "(Vea el diálogo «Acerca de...» desde el menú "
                          "principal.)", 
                  padre = ventana_padre)
            else:
                try:
                    objeto_a_actualizar = clase.get(model_tv[path][-1])
                except ValueError:
                    objeto_a_actualizar = pclases.getObjetoPUID(
                                                    model_tv[path][-1])
                setattr(objeto_a_actualizar, campo, valor)
        else:
            valor = getObjetoPUID(idct)
            try:
                objeto_a_actualizar = clase.get(model_tv[path][-1])
            except SQLObjectNotFound:
                pass    # El objeto fue eliminado de la base de datos. Ignoro.
            except ValueError:  # Es un PUID
                objeto_a_actualizar = pclases.getObjetoPUID(model_tv[path][-1])
            else:
                setattr(objeto_a_actualizar, campo, valor)
            model_tv[path][numcol] = text
            #self.actualizar_ventana()
    cellcombo.connect("edited", guardar_combo, tv.get_model(), numcol, model, 
                                               entry)
    column.pack_start(cellcombo)
    column.set_attributes(cellcombo, text = numcol)

def media(valores):
    """
    Devuelve la media aritmética de la lista de valores recibida. Si la 
    lista está vacía devuelve cero (no None ni salta excepción ni nada de eso).
    """
    assert isinstance(valores, (list, tuple))
    try:
        mean = 1.0 * sum(valores) / len(valores)
    except ZeroDivisionError:
        mean = 0.0
    return mean

def moda(lista_valores):
    """
    Devuelve la moda de los valores discretos recibidos en la lista. None si 
    la lista está vacía.
    """
    conteo = defaultdict(int)
    res = None
    moda = 0
    for i in lista_valores:
        conteo[i] += 1 
        if conteo[i] > moda:
            res = i
            moda = conteo[i]
    return res

def restar_datetime_time(t1, t2):
    """
    Devuelve la diferencia t1-t2. Si t1 es inferior a t2, le suma un día para 
    no devolver horas negativas.
    """
    t1 = parse_hora(str_hora(t1))
    t2 = parse_hora(str_hora(t2))
    if t1 < t2:
        t1 += mx.DateTime.oneDay
    res = t1 - t2
    return res

def dividir_cadena(s, trozos = 2):
    """
    Divide s en dos cadenas por el espacio más cercano al centro. Si no, 
    corta justo por el centro.
    PLAN: Si el espacio está hacia la izquierda, lo ignora. Controlar también 
    que no corte por un espacio demasiado alejado al centro. Permitir cortar 
    en varios trozos.
    Se diferencia en el "wrap" de este mismo módulo en que en lugar del 
    ancho, le indicamos los trozos en que queremos partir la cadena.
    """
    centro = len(s) / 2
    separadores = " ,.-\t\n()"
    cadena1 = s[:centro]
    cadena2 = s[centro:]
    pivote = ""
    for i in cadena2:
        if i in separadores:
            break           # Se acabó.
        else:
            pivote += i     # Paso el carácter a la primera subcadena.
            cadena2 = cadena2[1:]
    if i in separadores:
        cadena1 += pivote
    else:
        cadena2 = pivote + cadena2
    return cadena1, cadena2

def sanitize(cad, strict = False):
    """
    Cambia caracteres "problemáticos" por equivalentes en la 
    cadena para evitar errores en nombres de fichero, menús de glade...
    Si se usa el modo estricto (strict = True) cambia también caracteres 
    problemáticos en nombres de fichero (coma, retorno de carro, tildes
    y contrabarra).

    :cad: Cadena de texto
    :strict: Booleano. Si True reemplaza también comas, puntos, etc. Ojo que
             si lo que se recibe es un nombre de fichero completo porque le 
             quitará la extensión al sustituir el punto.
    :returns: Cadena de texto con caracteres reemplazados.

    """
    equivalencias = [(r"'", u"'"), 
                     (r"/", u"-")] 
    if strict:
        equivalencias += [(",", "_"), 
                          ("\n", "_"), 
                          ("\\", "_"), 
                          (".", ""), 
                          ("(", ""), 
                          (")", ""), 
                          ("`", ""), 
                          ("'", ""), 
                          ("'", ""), 
                          ("ñ", "nn"), 
                          ("Ñ", "NN"),
                          ("ç", "c"),
                          ("Ç", "C")]
    for mala, buena in equivalencias:
        cad = cad.replace(mala, buena)
    if strict:
        cad = filtrar_tildes(cad)
    return cad

def dialogo_proveedor(padre = None, inhabilitados = False):
    """
    Muestra un diálogo con un combo de proveedores. Devuelve el objeto 
    proveedor o None si se cancela.
    Si inhabilitados es True, incluye también proveedores deshabilitados.
    """
    from framework import pclases
    if not inhabilitados:
        proveedores = pclases.Proveedor.select(
                pclases.Proveedor.q.inhabilitado == False, 
                orderBy = "nombre")
    else:
        proveedores = pclases.Proveedor.select(orderBy = "nombre")
    ops = [(p.id, p.nombre) for p in proveedores]
    res = dialogo_combo(titulo = "SELECCIONE UN PROVEEDOR", 
        texto = "Seleccione un proveedor de la siguiente lista:", 
        ops = ops, 
        padre = padre)
    if res:
        try:
            res = pclases.Proveedor.get(res)
        except:     # Proveedor borrado durante el proceso.
            res = None 
    return res


if __name__=="__main__":
    print dialogo_radio(titulo='Seleccione una opción', 
                texto='Selecciona una opción del radiobutton y tal y cual.', 
                ops=[(0, 'Sin opciones'), (1, "Una opción"), (2, "Y otra"), 
                     (3, "La misoginia no es una opción, es una OBLIGACIÓN")], 
                padre = None, 
                valor_por_defecto = 3)
    sys.exit(0)
    ## --------
    print "Debe responder True: ", dialogo(titulo = "PRUEBA", texto = "Probando", defecto = True, tiempo = 5, bloq_temp = ["Sí"])
    sys.exit(0)
    print "Debe responder False: ", dialogo(titulo = "PRUEBA", texto = "Probando", defecto = False, tiempo = 4)
    print "Debe responder gtk.RESPONSE_CANCEL: ", dialogo(titulo = "PRUEBA", texto = "Probando", cancelar = True, defecto = gtk.RESPONSE_CANCEL, tiempo = 6)
    sys.exit(0)
    from framework import pclases
    #l = [filtrar_tildes(p.documentodepago.split(" ")[0].lower()) for p in pclases.Proveedor.select()]
    l = [filtrar_tildes(p.documentodepago) for p in pclases.Proveedor.select()]
    l = [e.strip().split(" ")[0].lower() for e in l]
    l = unificar(l)
    l.sort()
    for e in l:
        print e
    sys.exit()
    #print corregir_mayusculas_despues_de_punto(" Rocío. Take.  my.hand.")
    #print corregir_mayusculas_despues_de_punto(" Sin punto no hay diversión €")
    #print corregir_mayusculas_despues_de_punto(" Ivor the engine driver.")
    #print corregir_mayusculas_despues_de_punto(" Love Reign o'er me. ")
    #print corregir_mayusculas_despues_de_punto("   ")
    #print corregir_mayusculas_despues_de_punto("")
    ahora = time.time()
    buscar_producto_general(mostrar_precios = True)
    print (time.time() - ahora) / 60.0
    #print dialogo_entrada()
    #dialogo_info('Título', 'Texto\nmultilínea y tal y Pascual.')
    #dialogo_resultado(((1, 'Uno', '1'), (2, 'Dos', '2')), 'Resultados de búsqueda')
    #print mostrar_hora(14)
    #print dialogo(texto = 'Probando probando y con\nel mazo dando', 
    #              titulo = 'PRUEBA UNITARIA', 
    #              padre=None, 
    #              icono=gtk.STOCK_DIALOG_WARNING, 
    #              cancelar=True)
    #for i in ("0", 0, "0.0", 0.0, "0,0", "12", 
    #          "123.45", "123,45", "123.456,78",
    #          12.3, "1.000", "1,000"):
    #    print type(i), i, _float(i)
    #print "-"*80
    #print float2str(_float("123.456,78"))
    #print float2str(_float("123.456,78"), 3)
    #print float2str(_float("123.456,78"), 3, autodec = True)
    #for i in dialogo_pedir_rango():
    #    print i
    #enviar_correoe("xxxxxx@xxxxxxxx.xxx", 
    #               ["xxxxxxxxx.xxxxxx@xxxxx.xxx", ], 
    #               "Prueba correo desde servidor xxxxxxxxxxx", 
    #               "Esto es una prueba.\n\nTal y cual.\n\n", 
    #               adjuntos = ["./utils.py"], 
    #               servidor = "smtp.xxxxx.xx", 
    #               usuario = 'xxxxxx', 
    #               password = 'xxxxxx')
#    print "¡Hola hombre cangrejo!"
#    codigos = """A3894
#R72349
#R79622D
#B24778D
#B33724
#PC587
#C217
#"""
#    d = descargar_phaser(datos = codigos)
#    print d


