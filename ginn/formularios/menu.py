#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2011  Francisco José Rodríguez Bogado,                   #
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
## menu.py - Menú de acceso a módulos y ventanas.
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 27 de abril de 2006 -> Inicio.
## 5 de mayo -> It's alive! Alive! 
## 27 de mayo de 2006 -> Tenemos log.
###################################################################
## NOTAS:
## Si una ventana no pertenece a ningún módulo no aparecerá en los
## permisos ni en el menú. A efectos prácticos, no existirá para 
## los usuarios aunque esté en la BD y tenga relación con alguno 
## a través de la tabla "permisos".
###################################################################
## + Cambiar todos los print "WARNING... " de todos los .py por un 
## mensaje en el LOG.
## - PLAN: Crear una ventana para copias de seguridad.
## - PLAN: Mostrar ventana en tiempo real cuando cambie la salida 
##   del programa (señal de que algo ha pasado, probablemente una 
##   excepción no capturada de la que no se mostrará la ventana 
##   de enviar bugreport hasta cerrar el programa).
###################################################################

import pygtk
pygtk.require('2.0')
import gtk, gobject
import os, sys, traceback
from framework import pclases
#os.environ['LANG'] = "es_ES"
#os.environ['LANGUAGE'] = 'es_ES'
#print os.environ
#os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
#print os.getcwd()
#print os.path.realpath(sys.argv[0])
#
from formularios import gtkexcepthook

from formularios import utils
from framework.configuracion import ConfigConexion, parse_params

from formularios import custom_widgets

__version__ = '5.0.5 (beta)'
__version_info__ = tuple(
    [int(num) for num in __version__.split()[0].split('.')] + 
    [txt.replace("(", "").replace(")", "") for txt in __version__.split()[1:]]
    )


# Major: Versiones mayores. Cambios significativos en funcionalidades.
# Minor: Versión menor (subversiones). Cambios en tablas, nuevas ventanas... 
#        cosas así
# Revision: Revisiones. Pequeños incrementos, bugfixes, retoques en el código. 
#           Prácticamente ++ con cada commit del cvs.
# Las builds, obviamente no son compilaciones. En este caso representa el 
# número de actualizaciones más o menos "estables" del CVS, calculado con un 
# simple `grep -c "* " doc/ChangeLog` (es decir, se admiten pucherazos, 
# imprecisiones, bailes de cifras, señores pequeñitos y hasta a Bizcoché y 
# Ojos de huever).
# ROADMAP:
# 0.x: Primera versión de prototipos (branch geotexinn del CVS). 
# 1.0: Branch geotexinn02 del CVS.
# 1.4b: Pasaré a la versión 1.4 beta cuando acabe el laboratorio. 
# 1.5b: Versión para integración con LOGIC. 
# 1.6b: Versión para nóminas. 
# 1.7b: Cuando agregue las cosas que han ido quedando pendiente del módulo de 
#       administración. 
# 1.8b: Versión para prueba de nóminas, resultados marcado CE, balas y rollos 
#       X, consultas, listados pendientes y el resto de "hitos" importantes 
#       que aún quedan por implementar (que no deben ser muchos más de éstos).
# 1.9b: Cuando cierre "todas" las incidencias, bugs y etiquetas TO-DO|FIX-ME. 
#       (versión estable)
# 1.9.impar : Inestables.
# 1.9.par : Estables.
# 2.0rc: Versión 2.0 release candidate coincidiendo con la puesta en 
#        producción.
# 2.0: Versión 2.0 cuando acabe fase de pruebas.
# 2.0.1: Tal vez debería hacer un fork para nuevas funcionalidades generales 
#        (tickets, IRPF...) mientras congelo la RC, pero prefiero una sola 
#        rama de código, que los merge de CVS son muy duros.

class MetaF:
    """
    "Metafichero" para almacenar la salida de errores y poder 
    enviar informes de error.
    """
    def __init__(self):
        self.t = ''

    def write(self, t):
        errores_a_ignorar = ("GtkWarning", "with become" , "PangoWarning", 
            "main loop already active", 
            "Warning: g_main_context_prepare() called recursively")
        for error in errores_a_ignorar:
            if error in t:
                return
        try:
            self.t += t
        except TypeError:
            self.t += str(t)
        sys.__stdout__.write(t)
        sys.__stdout__.flush()

    def flush(self):
        sys.__stdout__.flush()

    def __repr__(self):
        return self.t

    def __str__(self):
        return self.t

    def __get__(self):
        return self.t

    def vacio(self):
        return len(self.t) == 0


class Menu:
    def __init__(self, user = None, passwd = None, fconfig = None):
        """
        user: Usuario. Si es None se solicitará en la ventana de 
        autentificación.
        passwd: Contraseña. Si es None, se solicitaré en la ventana de 
        autentificación.
        Si user y passwd son distintos a None, no se mostrará la ventana de 
        autentificación a no ser que sean incorrectos.
        """
        self.fconfig = fconfig
        from formularios import gestor_mensajes, autenticacion
        login = autenticacion.Autenticacion(user, passwd)
        if not login.loginvalido():
            sys.exit(1)
        self.logger = login.logger
        pclases.logged_user = self.usuario = login.loginvalido()
        # Configuración del correo para informes de error:
        gtkexcepthook.devs_to = "informatica@geotexan.com"
        if self.usuario.cuenta:
            gtkexcepthook.feedback = self.usuario.cuenta
            gtkexcepthook.password = self.usuario.cpass
            if not self.usuario.smtpserver:
                gtkexcepthook.smtphost = "smtp.googlemail.com"
                gtkexcepthook.ssl = True
                gtkexcepthook.port = 587
            else:
                gtkexcepthook.smtphost = self.usuario.smtpserver
                gtkexcepthook.ssl = (
                    gtkexcepthook.smtphost.endswith("googlemail.com") 
                     or gtkexcepthook.smtphost.endswith("gmail.com")) 
                gtkexcepthook.port = gtkexcepthook.ssl and 587 or 25 
        else:
            try:
                gtkexcepthook.feedback = pclases.Usuario.selectBy(usuario = "admin")[0].feedback
                gtkexcepthook.password = pclases.Usuario.selectBy(usuario = "admin")[0].password
                gtkexcepthook.smtphost = pclases.Usuario.selectBy(usuario = "admin")[0].smtphost
            except IndexError:
                gtkexcepthook.feedback = "informatica@geotexan.com"
                gtkexcepthook.smtphost = "smtp.googlemail.com"
            gtkexcepthook.ssl = (
                gtkexcepthook.smtphost.endswith("googlemail.com") 
                 or gtkexcepthook.smtphost.endswith("gmail.com")) 
            gtkexcepthook.port = gtkexcepthook.ssl and 587 or 25 
        # Continúo con el gestor de mensajes y resto de ventana menú.
        if pclases.VERBOSE:
            print "Cargando gestor de mensajes..."
        self.__gm = gestor_mensajes.GestorMensajes(self.usuario)
        # DONE: Dividir la ventana en expansores con los módulos del programa 
        # (categorías) y dentro de ellos un IconView con los iconos de cada 
        # ventana. Poner también en lo alto del VBox el icono de la aplicación.
        # (Ya va siendo hora de un poquito de eyecandy).
        if pclases.VERBOSE:
            print "Cargando menú principal..."
        self.construir_ventana()
        utils.escribir_barra_estado(self.statusbar, 
                                    "Menú iniciado", 
                                    self.logger, 
                                    self.usuario.usuario)

    def get_usuario(self):
        return self.usuario

    def salir(self, 
              boton, 
              event = None, 
              mostrar_ventana = True, 
              ventana = None):
        """
        Muestra una ventana de confirmación y 
        sale de la ventana cerrando el bucle
        local de gtk_main.
        Si mostrar_ventana es False, sale directamente
        sin preguntar al usuario.
        """
        res = False
        if event == None:
            # Me ha invocado el botón
            if (not mostrar_ventana 
                or utils.dialogo('¿Desea cerrar el menú principal?', 
                                 'SALIR', 
                                 padre = ventana, 
                                 icono = gtk.STOCK_QUIT)):
                ventana.destroy()
                self.logger.warning("LOGOUT: %s" % (self.usuario.usuario))
                res = False
            else:
                res = True
        else:
            res = (not mostrar_ventana 
                   or not utils.dialogo('¿Desea cerrar el menú principal?', 
                                        'SALIR', 
                                        padre = ventana, 
                                        icono = gtk.STOCK_QUIT))
            if not res: 
                self.logger.warning("LOGOUT: %s" % (self.usuario.usuario))
        return res

    def construir_ventana(self):
        self.statusbar = gtk.Statusbar()
        self.ventana = gtk.Window()
        self.ventana.set_position(gtk.WIN_POS_CENTER)
        self.ventana.resize(800, 600)
        self.ventana.set_title('Menú GINN')
        self.ventana.set_icon(gtk.gdk.pixbuf_new_from_file(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                         "..", "imagenes", 'logo_w.xpm')))
        self.ventana.set_border_width(10)
        self.ventana.connect("delete_event", self.salir, True, self.ventana)
        self.caja = gtk.VBox()
        self.caja.set_spacing(5)
        self.ventana.add(self.caja)
        self.cabecera = gtk.HBox()
        imagen = gtk.Image()
        config = ConfigConexion()
        pixbuf_logo = gtk.gdk.pixbuf_new_from_file(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                         '..', 'imagenes', config.get_logo()))
        pixbuf_logo = escalar_a(300, 200, pixbuf_logo)
        imagen.set_from_pixbuf(pixbuf_logo)
        self.cabecera.pack_start(imagen, fill=True, expand=False)
        texto = gtk.Label("""
        <big><big><big><b>%s</b></big>        

        <u>Menú de acceso a módulos de la aplicación</u></big>        

        <i>v.%s</i></big>         
        <small><b>%s</b> en <b>%s</b></small>         
        """ % (config.get_title(), __version__, config.get_dbname(), 
               config.get_host()))
        texto.set_justify(gtk.JUSTIFY_CENTER)
        texto.set_use_markup(True)
        event_box = gtk.EventBox()
            # Porque el gtk.Label no permite cambiar el background.
        event_box.add(texto)
        event_box.modify_bg(gtk.STATE_NORMAL, 
                            event_box.get_colormap().alloc_color("white"))
        half_header = gtk.VBox()
        half_header.add(event_box)
        txtchangelog = read_changelog()
        if txtchangelog:
            marquee_changelog = custom_widgets.MarqueeLabel(
                    txtchangelog, init_long = 61)
            little_label = gtk.Label(
                    "<small><i>Últimas actualizaciones:</i></small>")
            little_label.set_use_markup(True)
            little_label.set_property("xalign", 0.1)
            half_header.add(little_label)
            marquee_changelog_event = gtk.EventBox()
            marquee_changelog_event.add(marquee_changelog)
            half_header.add(marquee_changelog_event)
            def reset(*args, **kw):
                marquee_changelog.rewind()
            marquee_changelog_event.connect("button-press-event", reset)
        self.cabecera.pack_start(half_header)
        self.caja.pack_start(self.cabecera, fill=True, expand=False)
        self.current_frame = None
        cuerpo_central = self.create_menu()
        self.caja.pack_start(cuerpo_central)
        self.caja.pack_start(self.statusbar, False, True)

    def create_menu(self):
        model = gtk.ListStore(str, gtk.gdk.Pixbuf)
        modulos = {}
        usuario = self.get_usuario()
        if pclases.VERBOSE:
            print "Analizando permisos (1/2)..."
        if pclases.VERBOSE:
            i = 0
            tot = pclases.Modulo.select().count()
        for m in pclases.Modulo.select(orderBy = "nombre"):
            if pclases.VERBOSE:
                i += 1
                print "Analizando permisos (1/2)... (%d/%d)" % (i, tot)
            modulos[m] = []
        if pclases.VERBOSE:
            i = 0
            tot = pclases.Permiso.select(
                pclases.Permiso.q.usuarioID == usuario.id).count()
        if pclases.VERBOSE:
            print "Analizando permisos (2/2)..."
        for permusu in usuario.permisos:
            if pclases.VERBOSE:
                i += 1
                print "Analizando permisos (2/2)... (%d/%d)" % (i, tot)
            if permusu.permiso:
                v = permusu.ventana
                m = v.modulo
                if m != None:
                    modulos[m].append(v)
        modulos_sorted = modulos.keys()
        def fsortalfabeticamente(m1, m2):
            if m1.nombre < m2.nombre:
                return -1
            if m1.nombre > m2.nombre:
                return 1
            return 0
        modulos_sorted.sort(fsortalfabeticamente)
        for modulo in modulos_sorted:
            if modulos[modulo]:
                fichicono = os.path.join(
                    os.path.dirname(os.path.realpath(__file__)), 
                    '..', 'imagenes', modulo.icono)
                pixbuf = gtk.gdk.pixbuf_new_from_file(fichicono)
                model.append([modulo.nombre, pixbuf])
        # Módulo favoritos
        pixbuf = gtk.gdk.pixbuf_new_from_file(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 
                '..', 'imagenes', "favoritos.png"))
        iterfav = model.append(("Favoritos", pixbuf))
        
        contenedor = gtk.ScrolledWindow()
        icon_view = gtk.IconView(model)
        icon_view.set_text_column(0)
        icon_view.set_pixbuf_column(1)
        icon_view.set_orientation(gtk.ORIENTATION_VERTICAL)
        icon_view.set_selection_mode(gtk.SELECTION_SINGLE)
        icon_view.connect('selection-changed', self.on_select, model)
        icon_view.set_columns(1)
        icon_view.set_item_width(110)
        icon_view.set_size_request(140, -1)
        
        contenedor.add(icon_view)
        self.content_box = gtk.HBox(False)
        self.content_box.pack_start(contenedor, fill=True, expand=False)
        #icon_view.select_path((0,)) 
        icon_view.select_path(model.get_path(iterfav))
            # Al seleccionar una categoría se creará el frame 
        # Sanity check. 
        if hasattr(icon_view, "scroll_to_path"):    # Si pygtk >= 2.8
            icon_view.scroll_to_path(model.get_path(iterfav), False, 0, 0)
        else:
            # ¿No hay equivalente en pyGTK 2.6?
            pass
        return self.content_box 
 
    def on_select(self, icon_view, model=None):
        selected = icon_view.get_selected_items()
        if len(selected) == 0: return
        i = selected[0][0]
        category = model[i][0]
        if self.current_frame is not None:
            self.content_box.remove(self.current_frame)
            self.current_frame.destroy()
            self.current_frame = None
        if category != "Favoritos":
            modulo = pclases.Modulo.select(
                pclases.Modulo.q.nombre == category)[0]
        else:
            modulo = "Favoritos"
        self.current_frame = self.create_frame(modulo)
        utils.escribir_barra_estado(self.statusbar, category, self.logger, 
                                    self.usuario.usuario)
        self.content_box.pack_end(self.current_frame, fill=True, expand=True)
        self.ventana.show_all()
        
    def create_frame(self, modulo):
        if modulo != "Favoritos":
            frame = gtk.Frame(modulo.descripcion)
            frame.add(self.construir_modulo(modulo.descripcion, 
                            [p.ventana for p in self.get_usuario().permisos 
                             if p.permiso and p.ventana.modulo == modulo]))
        else:
            frame = gtk.Frame("Ventanas más usadas")
            usuario = self.get_usuario()
            stats = pclases.Estadistica.select(
             pclases.Estadistica.q.usuarioID == usuario.id, orderBy = "-veces")
            # Se filtran las ventanas en las que ya no tiene permisos aunque 
            # estén en favoritos.
            stats = [s for s in stats 
                     if usuario.get_permiso(s.ventana) 
                         and usuario.get_permiso(s.ventana).permiso][:6]
            stats.sort(lambda s1, s2: (s1.ultimaVez > s2.ultimaVez and -1) 
                                      or (s1.ultimaVez < s2.ultimaVez and 1) 
                                      or 0)
            ventanas = [s.ventana for s in stats]
            frame.add(self.construir_modulo("Ventanas más usadas", 
                                            ventanas, 
                                            False))
        return frame        
        
    def cutmaister(self, texto, MAX = 20):
        """
        Si el texto tiene una longitud superior a 20 caracteres de ancho lo
        corta en varias líneas.
        """
        if len(texto) > MAX:
            palabras = texto.split(' ')
            t = ''
            l = ''
            for p in palabras:
                if len(l) + len(p) + 1 < MAX:
                    l += "%s " % p
                else:
                    t += "%s\n" % l
                    l = "%s " % p
                if len(l) > MAX:    # Se ha colado una palabra de más del MAX
                    tmp = l
                    while len(tmp) > MAX:
                        t += "%s-\n" % tmp[:MAX]
                        tmp = tmp[MAX:]
                    l = tmp
                # print t.replace("\n", "|"), "--", l, "--", p
            t += l
            res = t
        else:
            res = texto
        res = "\n".join([s.center(MAX) for s in res.split("\n")])
        return res
    
    def construir_modulo(self, nombre, ventanas, ordenar = True):
        """
        Crea un IconView con las
        ventanas que contiene el módulo.
        Recibe una lista de objetos ventana de pclases.
        Si «ordenar» es False usa el orden de la lista de ventanas 
        recibidas. En otro caso las organiza por orden alfabético.
        """
        model = gtk.ListStore(str, gtk.gdk.Pixbuf, str, str)
        # ventanas.sort(key=lambda v: v.descripcion)
        # En Python2.3 parece ser que no estaba la opción de especificar 
        # la clave de ordenación.
        if ordenar:
            ventanas.sort(lambda s1, s2: 
                            (s1.descripcion>s2.descripcion and 1) or 
                            (s1.descripcion<s2.descripcion and -1) or 0)
        for ventana in ventanas:
            try:
                pixbuf = gtk.gdk.pixbuf_new_from_file(
                    os.path.join(
                                 os.path.dirname(os.path.realpath(__file__)), 
                                 '..', 'imagenes', ventana.icono))
            except (gobject.GError, AttributeError, TypeError):  
                # Icono es "" o None (NULL en la tabla).
                pixbuf = gtk.gdk.pixbuf_new_from_file(
                    os.path.join(
                                 os.path.dirname(os.path.realpath(__file__)), 
                                 '..', 'imagenes', 'dorsia.png'))
            model.append((self.cutmaister(ventana.descripcion), 
                          pixbuf, ventana.fichero, ventana.clase))
            # El model tiene: nombre (descripción), icono, archivo, clase, 
            # descripción detallada (hint).
            # NOTA: No se pueden mostrar hints en el IconView (al menos yo no 
            #       sé cómo), así que ahora lo que tiene es el icono.
        contenedor = gtk.ScrolledWindow()
        iview = gtk.IconView(model)
        iview.set_text_column(0)
        iview.set_pixbuf_column(1)
        iview.set_item_width(180)
        iview.connect('selection-changed', self.mostrar_item_seleccionado, 
                      model)
        contenedor.add(iview)
        #iview.connect('item-activated', self.abrir, model)
        # HACK: PyGTK 2.28 en Windows con python 2.7 no reconoce el 
        # gtk.gdk._2BUTTON_PRESS y se pierde el doble clic que abre las 
        # ventanas. No llega a lanzarse nunca la señal "item-activated".
        # Esto es un pequeño apaño muy chapu.
        def button_press(widget, event):
            try:
                widget.clics += 1
            except AttributeError:
                widget.clics = 1
        def motion(widget, event):
            widget.clics = 0
            return True
        def button_release(widget, event):
            if widget.clics >= 2:
                # Este es el segundo. Lanzo el item-activated
                try:
                    paths = widget.get_selected_items()
                    path = paths[0]
                except IndexError:
                    pass    # "Nada seleccionado"
                else:
                    #widget.item_activated(path)
                    self.abrir(widget, path, model)
                    widget.clics = 0
            return True
        def key_pressed(widget, event):
            # Abro ventanas también con espacio y ENTER porque he desactivado 
            # el item-activated.
            if event.keyval == gtk.gdk.keyval_from_name("Return"):
                try:
                    paths = widget.get_selected_items()
                    path = paths[0]
                except IndexError:
                    pass    # "Nada seleccionado"
                else:
                    #widget.item_activated(path)
                    self.abrir(widget, path, model)
        iview.connect('button-press-event', button_press)
        iview.connect('motion-notify-event', motion)
        iview.connect('button-release-event', button_release)
        iview.connect('key-press-event', key_pressed)
        return contenedor

    def mostrar_item_seleccionado(self, icon_view, model):
        selected = icon_view.get_selected_items()
        if len(selected) == 0: return
        i = selected[0][0]
        descripcion_icono_seleccionado = model[i][0]
        descripcion_icono_seleccionado = descripcion_icono_seleccionado.replace('\n', ' ')
        utils.escribir_barra_estado(self.statusbar, descripcion_icono_seleccionado, self.logger, self.usuario.usuario)

    def volver_a_cursor_original(self):
        # print "Patrick Bateman sabe que es una chapuza y que no hay que hacer suposiciones de tiempo."
        try:
            self.ventana.window.set_cursor(None)
        except AttributeError:
            pass    # La ventana ya no existe.
        return False

    def abrir(self, iview, path, model):
        clase = model[path][3]
        archivo = model[path][2]
        pclases.Estadistica.incrementar(self.usuario, archivo)
        self.abrir_ventana(archivo, clase)

    def abrir_ventana_usuario(self, archivo):
        self.ventana.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        exec "import %s" % archivo
        gobject.timeout_add(5000, self.volver_a_cursor_original)
        if archivo == "usuarios": 
            from formularios import usuarios
            v = usuarios.Usuarios(self.get_usuario())  # @UnusedVariable
        elif archivo == "ventana_usuario":
            from formularios import ventana_usuario
            v = ventana_usuario.Usuarios(self.get_usuario())  # @UnusedVariable

    def abrir_ventana(self, archivo, clase):
        if archivo.endswith('.py'):  # Al importar no hay que indicar extensión
            archivo = archivo[:archivo.rfind('.py')]
        if clase == 'gajim' and archivo == 'gajim':
            utils.escribir_barra_estado(self.statusbar, 
                                        "Iniciar: gajim...", 
                                        self.logger, 
                                        self.usuario.usuario)
            self.abrir_gajim()
        elif clase == 'acerca_de' and archivo == 'acerca_de':
            utils.escribir_barra_estado(self.statusbar, 
                                        'Abrir: "acerca de..."', 
                                        self.logger, 
                                        self.usuario.usuario)
            self.acerca_de()
        elif 'usuario' in archivo:
            utils.escribir_barra_estado(self.statusbar, 
                                        "Cargar: %s.py" % archivo, 
                                        self.logger, 
                                        self.usuario.usuario)
            self.abrir_ventana_usuario(archivo)
        elif "pruebas_periodicas" in clase:
            utils.escribir_barra_estado(self.statusbar, 
                                        "Pruebas de coherencia de datos", 
                                        self.logger, 
                                        self.usuario.usuario)
            self.abrir_pruebas_coherencia()
        else:
            utils.escribir_barra_estado(self.statusbar, 
                                        "Cargar: %s.py" % archivo, 
                                        self.logger, 
                                        self.usuario.usuario)
            self.abrir_ventana_modulo_python(archivo, clase)

    def abrir_ventana_modulo_python(self, archivo, clase):
        try:
            self.ventana.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
            while gtk.events_pending(): gtk.main_iteration(False)
            # HACK: Debe haber una forma mejor de hacerlo. De momento me 
            #       aprovecho de que el mainloop no va a atender al 
            #       timeout aunque se cumpla el tiempo, ya que está 
            #       ocupado en abrir la ventana, con lo que el cursor 
            #       sale del "busy" justo cuando debe, al abrirse la 
            #       ventana.
            v = None 
            gobject.timeout_add(5000, self.volver_a_cursor_original)
            # NOTA: OJO: TODO: Usuario harcoded. Cambiar en cuanto sea 
            #                  posible.
            if ((self.get_usuario().usuario == "geotextil" or 
                 self.get_usuario().usuario == "fibra" or 
                 self.get_usuario().nivel >= 3) 
                and "partes_de_fabricacion" in archivo
                and self.get_usuario().usuario != "cemento"):
                exec "import %s" % archivo
                v = eval('%s.%s' % (archivo, clase))
                try:
                    v(permisos = "rx", usuario = self.get_usuario())
                except TypeError:   # La ventana no soporta el modelo 
                                    # antiguo de permisos.
                    v(usuario = self.get_usuario())
                #v.wids['ventana'].set_icon_from_filename(icowindow)
            else:
                try:
                    #raise NotImplementedError, \
                    #        "Lanzador multiproceso en desarrollo..."
                    self.lanzar_ventana(archivo, clase)
                except Exception, e:
                    print e
                    sys.stderr.write(`e`)
                    self._lanzar_ventana(archivo, clase)
        except:
            self.ventana.window.set_cursor(None)
            utils.escribir_barra_estado(self.statusbar, 
                "Error detectado. Iniciando informe por correo.", 
                self.logger, 
                self.usuario.usuario)
            self.enviar_correo_error_ventana()

    def _lanzar_ventana(self, archivo, clase):
        """
        DEPRECATED
        """
        exec "import %s" % archivo
        v = eval('%s.%s' % (archivo, clase))
        v(usuario = self.get_usuario())
        #v.wids['ventana'].set_icon_from_filename(icowindow)
        # Podría incluso guardar los objetos ventana que se van 
        # abriendo para controlar... no sé, algo, contar las ventanas 
        # abiertas o qué se yo.

    def __lanzar_ventana(self, archivo, clase):
        """
        EXPERIMENTAL
        Da violaciones de segmento en GNU/Linux y salta excepción en Windows. 
        DISASTER!
        """
        #self._lanzar_ventana(archivo, clase)
        #return
        # XXX
        from multiprocessing import Process
        v = Process(target = importar_e_instanciar, 
                    args = (archivo, clase, self.get_usuario()))
        try:
            self.ventanas_abiertas.append(v)
        except (AttributeError):
            self.ventanas_abiertas = [v]
        v.start()
        # Esto debería ir en otra función al salir:
        for v in self.ventanas_abiertas:
            v.join()
            
    def lanzar_ventana(self, archivo, clase):
        """
        VERY PRETTY EXPERIMENTAL
        """
        # La idea es que los datos que requieren las ventanas que vienen desde 
        # el menú se pasen por un pipe en lugar de acceder de forma compartida 
        # por el fork (no hay exec multiplataforma). De este modo el menú y la 
        # nueva ventana serán procesos completamente indepentientes. No se 
        # necesitan compartir más datos una vez abierta la ventana. Así que 
        # guay. No más segfaults en el join ni excepciones de pickle.
        from formularios import launcher
        launcher.run(archivo, clase, self.usuario, self.fconfig)

    def enviar_correo_error_ventana(self):
        print "Se ha detectado un error"
        texto = ''
        for e in sys.exc_info():
            texto += "%s\n" % e
        tb = sys.exc_info()[2]
        texto += "Línea %s\n" % tb.tb_lineno
        info = MetaF() 
        traceback.print_tb(tb, file = info)
        texto += "%s\n" % info
        enviar_correo(texto, self.get_usuario())

    def abrir_gajim(self):
        try:
            pwd = os.path.abspath(os.curdir)
            os.chdir(os.path.join('..', 'gajim-0.9.1', 'src'))
            # TODO: En la versión final hay que intentar que el usuario 
            #       que se conecte sea el mismo de la aplicación, o bien 
            #       compartir el mismo usuario para todos los que usen el 
            #       mismo ordenador (por aquello de que la cuenta se guarda
            #       en el .gajim y se conecta automáticamente).
            ## FIXME: OJO: Esto inicia un nuevo proceso (es multiplataforma). 
            ##             La desventaja es que entonces me impide manejar 
            ##             gajim "desde dentro". No puedo pasarle la cuenta 
            ##             de usuario (tendría que volcarla a un .gajim antes 
            ##             de arrancarlo), etc...
            if os.name == 'posix':
                # pid = os.spawnl(os.P_NOWAIT, "gajim.py")
                # Inexplicablemente -juraría que antes funcionaba- el spawnl 
                # ya no rula.
                os.system("cd .. && ./launch.sh >/dev/null &")
            elif os.name == 'nt':
                os.startfile("gajim.pyw")  # @UndefinedVariable
            else:
                utils.dialogo_info(titulo = "PLATAFORMA NO SOPORTADA",
                    texto = "La ayuda on-line solo funciona en arquitecturas"
                            " con plataformas POSIX o NT\n(GNU/Linux, "
                            "MS-Windows, *BSD...).",
                    padre = self.ventana)
        except:
            print "Se ha detectado un error. Volviendo a %s." % (pwd)
            if '.' in sys.path:
                sys.path.remove('.')
            os.chdir(pwd)
            texto = ''
            for e in sys.exc_info():
                texto += "%s\n" % e
            tb = sys.exc_info()[2]
            texto += "Línea %s\n" % tb.tb_lineno
            info = MetaF() 
            traceback.print_tb(tb, file = info)
            texto += "%s\n" % info
            enviar_correo(texto, self.get_usuario())
        else:
            if '.' in sys.path:
                sys.path.remove('.')
            os.chdir(pwd)
    
    def abrir_pruebas_coherencia(self):
        if os.name == 'posix':
            w = gtk.Window()
            w.set_title("SALIDA CHECKLIST WINDOW")
            scroll = gtk.ScrolledWindow()
            w.add(scroll)
            tv = gtk.TextView()
            scroll.add(tv)
            def forzar_iter_gtk(*args, **kw):
                while gtk.events_pending(): 
                    gtk.main_iteration(False)
            def printstdout(msg):
                tv.get_buffer().insert_at_cursor(msg)
                forzar_iter_gtk()
            w.show_all()
            forzar_iter_gtk()
            from formularios import runapp
            # SOLO PARA NOSTROMO:
            #os.system("./checklist_window.py 2>&1 | tee > ../../fixes/salida_check_`date +%Y_%m_%d_%H_%M`.txt &")
            comando = "./checklist_window.py 2>&1 | tee > "\
                      "../../fixes/salida_check_`date +%Y_%m_%d_%H_%M`.txt &"
            runapp.runapp(comando, printstdout)
            #os.system("./checklist_window.py 2>&1 | tee > salida_check_`date +%Y_%m_%d_%H_%M`.txt &")
        elif os.name == 'nt':
            os.startfile("checklist_window.py")  # @UndefinedVariable
        else:
            utils.dialogo_info(titulo = "PLATAFORMA NO SOPORTADA",
                texto = "Pruebas de coherencia solo funcionan en arquitecturas"
                        " con plataformas POSIX o NT\n(GNU/Linux, MS-Windows, "
                        "*BSD...).",
                padre = self.ventana)

    def mostrar(self):
        self.ventana.show_all()
        self.ventana.connect('destroy', gtk.main_quit)
        gtk.main()

    def launch_browser_mailer(self, dialogo, uri, tipo):
        # FIXME: De momento sólo funciona para NT-compatibles. Usar el nuevo multi_open.
        if tipo == 'email':
            if os.name == 'nt':
                try:
                    os.startfile('mailto:%s' % uri) # if pywin32 is installed we open @UndefinedVariable
                except:
                    pass
            else:
                utils.dialogo_info('NO IMPLEMENTADO', 
                                   'Funcionalidad no implementada.\nDebe lanzar manualmente su cliente de correo.\nCorreo-e seleccionado: %s' % uri,
                                   padre = self.ventana)
        elif tipo == 'web':
            if os.name == 'nt':
                try:
                    os.startfile(uri)  # @UndefinedVariable
                except:
                    pass
            else:
                utils.dialogo_info('NO IMPLEMENTADO', 
                                   'Funcionalidad no implementada.\nDebe lanzar manualmente su navegador web.\nURL seleccionada: %s' % uri, 
                                   self.ventana)

    def acerca_de(self):
        gtk.about_dialog_set_email_hook(self.launch_browser_mailer, 'email')
        gtk.about_dialog_set_url_hook(self.launch_browser_mailer, 'web')
        vacerca = gtk.AboutDialog()
        vacerca.set_name('Geotex-INN')
        vacerca.set_version(__version__)
        vacerca.set_comments('Software ERP para Geotexan')
        vacerca.set_authors(['Francisco José Rodríguez Bogado '
                             '<rodriguez.bogado@gmail.com>', 
                             'Diego Muñoz Escalante <escalant3@gmail.com>'])
        config = ConfigConexion()
        logo = gtk.gdk.pixbuf_new_from_file(os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 
                '..', 'imagenes', config.get_logo()))
        logo = escalar_a(300, 200, logo)
        vacerca.set_logo(logo)
        vacerca.set_license(open(os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 
                '..', 'gpl.txt')).read())
        vacerca.set_website('http://ginn.sf.net')
        vacerca.set_artists(['Iconos gartoon por Kuswanto (a.k.a. Zeus) '
                             '<zeussama@gmail.com>'])
        vacerca.set_copyright('Copyright 2005-2013  Francisco José Rodríguez'
                              ' Bogado, Diego Muñoz Escalante.')
        vacerca.run()
        vacerca.destroy()


def enviar_correo(texto, usuario = None):
    """
    Envía **silenciosamente** un correo electrónico con el texto recibido.
    Si no se puede enviar o no se recibe usuario, se guarda el texto en 
    disco.
    """
    import smtplib
    if usuario:
        gmail_user = usuario.cuenta
        gmail_pwd = usuario.cpass
    else:
        gmail_user = "practicas.geotexan@gmail.com" # Utilizo una cuenta "genérica"
        gmail_pwd = "20mesa20" # FIXME !!!
    gmail_from = gmail_user
    gmail_to = ['frbogado@geotexan.com'] 
    gmail_subject = "Geotex-INN: Informe de error"
    gmail_text = texto
    # TODO: No estaría de más meter algo de información extra del tipo: 
    #       fecha, hora (aunque esté en la cabecera del correo), IP, nombre 
    #       usuario, host, etc...

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (gmail_from, ", ".join(gmail_to), gmail_subject, gmail_text)
    try:
        #server = smtplib.SMTP(SERVER) 
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(gmail_from, gmail_to, message)
        #server.quit()
        server.close()
    except:
        guardar_error_a_log(usuario, texto)
        
def guardar_error_a_log(usuario, texto):
    """
    Guarda el texto en el log de la aplicación. Si no se recibe usuario (es 
    None) utiliza el registrado en pclases.
    """
    from ventana import get_ginn_logger
    logger = get_ginn_logger()
    if not usuario:
        try:
            nombre_usuario = pclases.logged_user.usuario  # @UndefinedVariable
        except AttributeError:
            nombre_usuario = "N/A"
    else:
        nombre_usuario = usuario.usuario
    texto_a_log = "%s: -> %s" % (nombre_usuario, texto)
    logger.error(texto_a_log)

def escalar_a(ancho, alto, pixbuf):
    """
    Devuelve un pixbuf escalado en proporción para que como máximo tenga 
    de ancho y alto las medidas recibidas.
    """
    if pixbuf.get_width() > ancho:
        nuevo_ancho = ancho
        nuevo_alto = int(pixbuf.get_height() 
                         * ((1.0 * ancho) / pixbuf.get_width()))
        colorspace = pixbuf.get_property("colorspace")
        has_alpha = pixbuf.get_property("has_alpha")
        bits_per_sample = pixbuf.get_property("bits_per_sample")
        pixbuf2 = gtk.gdk.Pixbuf(colorspace, 
                                 has_alpha, 
                                 bits_per_sample, 
                                 nuevo_ancho, 
                                 nuevo_alto)
        pixbuf.scale(pixbuf2, 
                     0, 0, 
                     nuevo_ancho, nuevo_alto, 
                     0, 0,
                     (1.0 * nuevo_ancho) / pixbuf.get_width(), 
                     (1.0 * nuevo_alto) / pixbuf.get_height(), 
                     gtk.gdk.INTERP_BILINEAR)
        pixbuf = pixbuf2
    if pixbuf.get_height() > alto:
        nuevo_alto = alto
        nuevo_ancho = int(pixbuf.get_width() 
                          * ((1.0 * alto) / pixbuf.get_height()))
        colorspace = pixbuf.get_property("colorspace")
        has_alpha = pixbuf.get_property("has_alpha")
        bits_per_sample = pixbuf.get_property("bits_per_sample")
        pixbuf2 = gtk.gdk.Pixbuf(colorspace, 
                                 has_alpha, 
                                 bits_per_sample, 
                                 nuevo_ancho, 
                                 nuevo_alto)
        pixbuf.scale(pixbuf2, 
                     0, 0, 
                     nuevo_ancho, nuevo_alto, 
                     0, 0,
                     (1.0 * nuevo_ancho) / pixbuf.get_width(), 
                     (1.0 * nuevo_alto) / pixbuf.get_height(), 
                     gtk.gdk.INTERP_BILINEAR)
        pixbuf = pixbuf2
    return pixbuf


def main():
    # Si hay ficheros de estilo gtk, los cargo por orden: General de la 
    # aplicación y específico del usuario en WIN y UNIX. Se machacan opciones 
    # por ese orden.
    GTKRC2 = ".gtkrc-2.0" # Depende de la versión...
    GTKRC = "gtkrc"
    gtk.rc_parse(os.path.join(
        os.path.dirname(__file__), "..", GTKRC))
    gtk.rc_parse(os.path.join(
        os.path.dirname(__file__),"..", GTKRC2))    # Si no existe se ignora  
                                                    # de manera silenciosa.
    if "HOME" in os.environ:
        gtk.rc_parse(os.path.join(os.environ["HOME"], GTKRC))
        gtk.rc_parse(os.path.join(os.environ["HOME"], GTKRC2))
    if "HOMEPATH" in os.environ:
        gtk.rc_parse(os.path.join(os.environ["HOMEPATH"], GTKRC))
        gtk.rc_parse(os.path.join(os.environ["HOMEPATH"], GTKRC2))
    # Ver http://www.pygtk.org/docs/pygtk/class-gtkrcstyle.html para la 
    # referencia de estilos. Ejemplo: 
    # bogado@cpus006:~/Geotexan/geotexinn02/formularios$ cat ../gtkrc 
    # style 'blanco_y_negro' { bg[NORMAL] = '#FFFFFF'
    #                          fg[NORMAL] = '#000000' 
    #                          base[NORMAL] = '#FFFFFF' 
    #                          text[NORMAL] = '#000000' 
    #                        }
    # class '*' style 'blanco_y_negro'
    ##
    user, passwd, modulo, clase, fconfig, verbose, debug, obj_puid = parse_params() 
    #salida = MetaF()
    #sys.stdout = salida
    errores = MetaF()
    sys.stderr = errores
    m = Menu(user, passwd, fconfig)
    m.mostrar()
    if not errores.vacio():
        print "Se han detectado algunos errores en segundo plano durante "\
              "la ejecución."
        enviar_correo('Errores en segundo plano. La stderr contiene:\n%s' 
                        % (errores), 
                      m.get_usuario())

def read_changelog():
    """
    Carga el ChangeLog de git del fichero ChangeLog.git.txt o ejecuta un 
    git-log directamente si no lo encuentra.
    """
    try:
        directorido = os.path.abspath(os.path.dirname(__file__))
        f = open(os.path.join(directorido, "ChangeLog.git.txt", 'r'))
    except IOError:
        gitcommand = 'git log | grep -v "commit " | grep -v "Author:" | egrep -v "$^" | grep -v "Merge: "'
        f = os.popen(gitcommand)
    content = " ".join([l.replace("\n", " ").replace("Date: ", " |") 
                        for l in f.readlines()])
    f.close()
    return content


def importar_e_instanciar(archivo, clase, usuario):
    exec "import %s" % archivo
    v = eval('%s.%s' % (archivo, clase))
    v(usuario = usuario)
    

if __name__ == '__main__':
    # Import Psyco if available
    try:
        import psyco
        psyco.full()
        #psyco.log()
        #psyco.profile()
    except ImportError:
        print "Optimizaciones no disponibles."
    main()
