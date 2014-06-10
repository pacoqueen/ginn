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
    def __init__(self, data = {}):
        self.BORDER_WIDTH = 1
        self.data = data
        super(Mapamundi, self).__init__()
        #self.window.show_all()
        self.render_data()
        self.set_size_request(self.__pixbuf.get_width(),
                              self.__pixbuf.get_height())
        self.connect("expose_event", self.expose)

    def setPixbuf(self, pixbuf):
        if type(pixbuf) != gtk.gdk.Pixbuf:
            raise TypeError("Pixbuf debe ser %s. Recibido %s" % (
                gtk.gdk.Pixbuf, type(pixbuf)))
        self.__pixbuf = pixbuf
        self.emit("expose-event", gtk.gdk.Event(gtk.gdk.EXPOSE))

    def expose(self, widget, event):
        x, y, ancho, alto = self.allocation
        try:
            context =  widget.window.cairo_create()
        except AttributeError:
            return True
        if self.__pixbuf != None:
            scaledPixbuf = self.__pixbuf.scale_simple(ancho,
                            alto,
                            gtk.gdk.INTERP_BILINEAR)
            ct = gtk.gdk.CairoContext(context)
            ct.set_source_pixbuf(scaledPixbuf, 
                                 self.BORDER_WIDTH, self.BORDER_WIDTH)
            context.paint()
            context.stroke()

    def load_pixbuf(self):
        """
        Crea y devuelve un pixbuf que contiene el SVG correspondiente 
        al gráfico de pygal creado con los datos con que inicializó el widget.
        """
        import sys, os
        sys.path.append(os.path.abspath(os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 
            "..", "..")))
        from lib.cairoplot import cairoplot
        data = [[1,2,3],[4,5,6],[7,8,9]]  
        test = cairoplot.HorizontalBarPlot("/tmp/object_way.svg", 
                                           data, 640, 480)  
        test.render()  
        test.commit()
        pb = gtk.gdk.pixbuf_new_from_file("/tmp/object_way.svg")
        #fsvg.close()
        return pb

    def render_data(self):
        """
        Crea el SVG y lo carga en el widget.
        """
        pb = self.load_pixbuf()
        self.setPixbuf(pb)


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

