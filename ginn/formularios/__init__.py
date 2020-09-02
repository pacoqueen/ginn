#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", '3.0')
from gi import pygtkcompat
import os

try:
    from gi import pygtkcompat
except ImportError:
    pygtkcompat = None
    from gi.repository import Gtk as gtk

if pygtkcompat is not None:
    pygtkcompat.enable()
    pygtkcompat.enable_gtk(version='3.0')
    import gtk

###############################################################################
# Detalles de configuración:
#os.environ['LANG'] = "es_ES"
#os.environ['LANGUAGE'] = 'es_ES'
settings = gtk.settings_get_default()
try:
    settings.props.gtk_button_images = True
except AttributeError:  # Versión anterior de GTK.
    pass
# Si hay ficheros de estilo gtk, los cargo por orden: General de la
# aplicación y específico del usuario en WIN y UNIX. Se machacan opciones
# de por ese orden.
GTKRC = "gtkrc"
#gtk.rc_parse(os.path.join("..", GTKRC))
gtk.rc_parse(GTKRC)
if "HOME" in os.environ:
    gtk.rc_parse(os.path.join(os.environ["HOME"], GTKRC))
if "HOMEPATH" in os.environ:
    gtk.rc_parse(os.path.join(os.environ["HOMEPATH"], GTKRC))
# Ver http://www.pygtk.org/docs/pygtk/class-gtkrcstyle.html para la
# referencia de estilos. Ejemplo:
# bogado@cpus006:~/Geotexan/geotexinn02/formularios$ cat ../gtkrc
# style 'blanco_y_negro' { bg[NORMAL] = '#FFFFFF'
#                          fg[NORMAL] = '#000000'
#                          base[NORMAL] = '#FFFFFF'
#                          text[NORMAL] = '#000000'
#                        }
# class '*' style 'blanco_y_negro'
###############################################################################
# TODO: Esto de parsear el gtkrc está repetido aquí y en el menu.py. Debería dejarlo en un solo sitio y tener cuidado con el tema MS-Windows en Windows 8, Vista y algunos XP. La solución pasa por poner el tema Industrial o Redmond con el GTK2-prefs.exe. O bien usar esto:
import platform
if platform.win32_ver()[0] == ("post2008Server", "6.2.9200", "", "Multiprocessor Free"):
    # Windows 8
    gtk.rc_parse_string('gtk-theme-name = "Industrial"') # O bien
#   gtk.rc_parse_string('gtk-theme-name = "Redmond"')
# Pero teniendo cuidado de hacerlo antes de aplicar el style morado para la versión dev.

