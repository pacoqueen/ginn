#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2014       Francisco José Rodríguez Bogado,                   #
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
# Mapamundi en un Widget usando Cairo (pygal)
###############################################################################

try:
    import gtk
    import gobject
    from gtk import gdk
except:
    raise SystemExit


if gtk.pygtk_version < (2, 0):
    print "Se necesita PyGtk 2.0 o posterior."
    raise SystemExit

class Mapamundi(gtk.DrawingArea):
    """
    Mapa del mundo que representa series de datos en los paises.
    """
    def __init__(self):
        super(Mapamundi, self).__init__()
        self.connect("expose_event", self.expose)
        self.set_size_request(800,500)

    def expose(self, widget, event):
        cr = widget.window.cairo_create()
        rect = self.get_allocation()

        # you can use w and h to calculate relative positions which
        # also change dynamically if window gets resized
        w = rect.width
        h = rect.height

        # here is the part where you actually draw
        cr.move_to(0,0)
        cr.line_to(w/2, h/2)
        cr.stroke()

###############################################################################

def main():
    """
    Prueba rápida de que funciona.
    """
    win = gtk.Window()
    win.connect('delete-event', gtk.main_quit)
    data = {'es': 12345.67, 
            'fr': -15}
    mapamundi = Mapamundi(data)
    win.add(mapamundi)
    win.set_position(gtk.WIN_POS_CENTER)
    win.show_all()
    gtk.main()

if __name__ == "__main__":
    main()

