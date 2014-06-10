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
    import cairo
except:
    raise SystemExit

if gtk.pygtk_version < (2, 0):
    print "Se necesita PyGtk 2.0 o posterior."
    raise SystemExit

(HORIZONTAL_BAR,    # 0
 VERTICAL_BAR,      # 1
 DONUT,             # 2
 PIE,               # 3
 DOT,               # 4
 FUNCTION,          # 5
 SCATTER,           # 6
 GANTT              # 7
) = range(8)

class GtkCairoPlot(gtk.DrawingArea):
    """
    Widget que incluye un gráfico de CairoPlot en él.
    """
    def __init__(self, tipo, data = []):
        self.BORDER_WIDTH = 1
        super(GtkCairoPlot, self).__init__()
        self._constructor = self._get_func(tipo)
        self._data = data
        self.width = 400
        self.height = 300
        self.set_size_request(self.width + self.BORDER_WIDTH,
                              self.height + self.BORDER_WIDTH)
        self.connect("expose_event", self.expose)

    def expose(self, widget, event):
        x, y, ancho, alto = self.allocation
        try:
            self.context =  widget.window.cairo_create()
        except AttributeError:
            return True
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 
                self.width + self.BORDER_WIDTH, 
                self.height + self.BORDER_WIDTH)
        self.render_plot()
        self.show_all()

    def render_plot(self):
        """
        Invoca la función encargada de generar el gráfico de CairoPlot en el 
        surface de Cairo.
        """
        # TODO: OJO porque la interfaz cambia. Esto solo vale para los bar_plot
        plt = self._constructor(self.surface, self._data, 
                                self.width, self.height)
        # TODO: PORASQUI: A SVG va bien. Pero si le paso el cairosurface directamente no rula. ¿Qué estoy haciendo mal?
        plt.render()
        plt.commit()

    @staticmethod
    def _get_func(tipo):
        """
        Devuelve el tipo de función de CairoPlot que corresponde a la macro.
        """
        import sys, os
        libdir = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "..", "lib"))
        sys.path.append(libdir)
        from cairoplot import cairoplot
        if tipo == HORIZONTAL_BAR:
            func = cairoplot.HorizontalBarPlot
        elif tipo == VERTICAL_BAR:
            func = cairoplot.VerticalBarPlot
        elif tipo == DONUT:
            raise NotImplementedError
        elif tipo == PIE:
            raise NotImplementedError
        elif tipo == DOT:
            raise NotImplementedError
        elif tipo == FUNCTION:
            raise NotImplementedError
        elif tipo == SCATTER:
            raise NotImplementedError
        elif tipo == GANTT:
            raise NotImplementedError
        else:
            raise ValueError, "tipo no reconocido. Consulte gtkcairoplot.py"
        return func
            

###############################################################################

def main():
    """
    Prueba rápida de que funciona.
    """
    win = gtk.Window()
    win.connect('delete-event', gtk.main_quit)
    data = [[1,2,3],[4,5,6],[7,8,9]] 
    tipo = HORIZONTAL_BAR
    plot = GtkCairoPlot(tipo, data)
    win.add(plot)
    win.set_position(gtk.WIN_POS_CENTER)
    win.show_all()
    gtk.main()

if __name__ == "__main__":
    main()

