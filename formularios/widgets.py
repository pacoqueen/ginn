#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado,                   #
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


import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade

LANZAR_KEY_EXCEPTION = True # Si False se devuelve None cuando se busca un 
                            # widget que no existe y se ignora la excepción.

class Widgets:
    def __init__(self, file):
        self.widgets = gtk.glade.XML(file)
        self.dynwidgets = {}    # Widgets generados dinámicamente
        
    def __getitem__(self, key):
        res = self.widgets.get_widget(key)
        if res == None:  # Si no es del archivo glade...
            try:         # tal vez se haya creado "programáticamente".
                res = self.dynwidgets[key]
            except KeyError, msg:
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
        return [w.name for w in self.widgets.get_widget_prefix('')] + self.dynwidgets.keys()


