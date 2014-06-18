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

import os
import pygtk
pygtk.require('2.0')
import gtk  # @UnusedImport
import gtk.glade

LANZAR_KEY_EXCEPTION = True # Si False se devuelve None cuando se busca un 
                            # widget que no existe y se ignora la excepción.

BUILDER = False  # Flag para ver si trabajamos con libglade o con gtkBuilder.

class Widgets:
    def __init__(self, uifile):
        if not os.path.exists(uifile):
            uifile = os.path.join(
                os.path.abspath(os.path.dirname(os.path.realpath(__file__))), 
                uifile)
        try:
            self.widgets = gtk.glade.XML(uifile)
        except RuntimeError:
            self.widgets = gtk.Builder()
            self.widgets.add_from_file(uifile)
            BUILDER = True
        self.dynwidgets = {}    # Widgets generados dinámicamente
        
    def __getitem__(self, key):
        """Si USE_DEPRECATED es True, imita el antiguo comportamiento donde los 
        widgets cargados desde fichero tienen prioridad sobre los creados 
        "programáticamente". USE_DEPRECATED es una "macro" definida en 
        el código de la clase widgets.py.
        """
        USE_DEPRECATED = False
        # IMPORTANTE: Cambio el orden y ahora tienen preferencia los widgets 
        # creados dinámicamente a posteriori.
        if not USE_DEPRECATED:
            try: 
                res = self.dynwidgets[key]
            except KeyError:
                res = self.widgets.get_widget(key)
            if res == None and LANZAR_KEY_EXCEPTION:
                raise KeyError, "Widget '%s' no existe." % key
        else:
            res = self.widgets.get_widget(key)
            if res == None:  # Si no es del archivo glade...
                try:         # tal vez se haya creado "programáticamente".
                    res = self.dynwidgets[key]
                except KeyError:
                    res = None
                    if LANZAR_KEY_EXCEPTION:
                        raise KeyError, "Widget '%s' no existe." % key
        return res

    def __setitem__(self, key, value):
        self.dynwidgets[key] = value
        value.set_property("name", key)

    def keys(self):
        """
        Devuelve una lista de claves del diccionario de widgets.
        """
        try:
            listaclaves = [w.name for w in self.widgets.get_widget_prefix('')] 
        except AttributeError:
            listaclaves = [w.name for w in self.widgets.get_objects()] 
        listaclaves += self.dynwidgets.keys()
        return listaclaves

def replace_widget(current, new):
    """
    Replace one widget with another.
    'current' has to be inside a container (e.g. gtk.VBox).
    """
    container = current.parent
    assert container # is "current" inside a container widget?

    # stolen from gazpacho code (widgets/base/base.py):
    props = {}
    for pspec in gtk.container_class_list_child_properties(container):
        props[pspec.name] = container.child_get_property(current, pspec.name)

    gtk.Container.remove(container, current)
    container.add(new)

    for name, value in props.items():
        container.child_set_property(new, name, value)

