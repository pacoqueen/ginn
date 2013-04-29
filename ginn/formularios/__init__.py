#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk, os
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


