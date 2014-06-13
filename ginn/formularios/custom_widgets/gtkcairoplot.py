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
# Clase para empotrar gráficos hechos con Cairo en un widget Gtk
###############################################################################

# TODO: De momento funciona para barras verticales y horizontales con CairoPlot
# Tengo a medio hacer la adaptación de cagraph, que es más potente pero igual 
# de mal documentado que CairoPlot; aunque más compleja a la hora de crear 
# las gráficas.
# Al final me quedé con las ganas de https://networkx.github.io/ porque 
# depende de matplotlib, que es enorme y no se instala por defecto.

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

import sys, os
libdir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "lib"))
sys.path.append(libdir)
from cairoplot import cairoplot

# Pruebas con cagraph
from cagraph.cagraph.ca_graph import CaGraph
from cagraph.cagraph.axis.xaxis import CaGraphXAxis
from cagraph.cagraph.axis.yaxis import CaGraphYAxis
from cagraph.cagraph.axis.taxis import CaGraphTAxis
from cagraph.cagraph.ca_graph_grid import CaGraphGrid
from cagraph.cagraph.series.line import CaGraphSeriesLine
from cagraph.cagraph.series.hbar import CaGraphSeriesHBar
from cagraph.cagraph.series.area import CaGraphSeriesArea


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
    def __init__(self, tipo, data = [], x_labels = [], y_labels = []):
        super(GtkCairoPlot, self).__init__()
        self._constructor = self._get_func(tipo)
        self._data = data
        self._x_labels = x_labels
        self._y_labels = y_labels
        self.connect("expose_event", self.expose)
        self.width = -1
        self.height = -1
        self.set_size_request(self.width, self.height)
        self._prepare_plot()

    def _prepare_plot(self):
        """
        Crea el objeto CairoPlot con los datos del atributo _data.
        """
        # Es simplemente para crear el objeto. Después se reemplazará por
        # el surface del DrawingArea en el expose.
        tempsurface = cairo.SVGSurface(None, self.width, self.height)
        # TODO: OJO porque la interfaz cambia. Esto solo vale para los bar_plot
        self.plt = self._constructor(tempsurface,
                                     self._data,
                                     self.width, self.height,
                                     x_labels = self._x_labels,
                                     y_labels = self._y_labels, 
                                     display_values = True)

    def expose(self, widget, event):
        rect = self.get_allocation()
        self.width = rect.width
        self.height = rect.height
        self.plt.dimensions[cairoplot.HORZ] = self.width
        self.plt.dimensions[cairoplot.VERT] = self.height
        try:
            self.plt.context = self.context =  widget.window.cairo_create()
        except AttributeError:
            return True
        self.render_plot()

    def render_plot(self):
        """
        Invoca la función encargada de generar el gráfico de CairoPlot en el
        surface de Cairo.
        """
        self.plt.render()
        self.plt.commit()

    @staticmethod
    def _get_func(tipo):
        """
        Devuelve el tipo de función de CairoPlot que corresponde a la macro.
        """
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

def create_cagraph_plot(tipo, data, x_labels = [], y_labels = []):
    graph = CaGraph()
    # create and add axiss to graph
    xaxis = CaGraphXAxis(graph)
    yaxis = CaGraphYAxis(graph)
    graph.axiss.append(xaxis)
    graph.axiss.append(yaxis)
    # create and add series to graph
    #graph.seriess.append(CaGraphSeriesLine(graph, 0, 1))
    graph.seriess.append(CaGraphSeriesHBar(graph, 0, 1))
    # En cagraph los valores se reciben siempre como pares x, y. Como solo 
    # recibo valores, en este caso x, completo con el y para que vayan en el 
    # orden de arriba a abajo según lo recibo.
    _data = []
    y = len(data[0]) * len(data)
    for barraset in data:
        for valor in barraset:
            _data.append((valor, y))
            y -= 1
    # add data to seriess
    graph.seriess[0].data = _data
    # automaticaly set axis ranges
    graph.auto_set_range()
    return graph


def build_test_window():
    """
    Devuelve una ventana de Gtk con un CairoPlot para pruebas.
    """
    win = gtk.Window()
    win.set_position(gtk.WIN_POS_CENTER)
    win.connect('delete-event', gtk.main_quit)
    data = [[1, 2, 3],      #  Uno █▅▂
            [4, 5, 6],      #  Dos ████▅▂
            [7, 8, 9]]      # Tres ███████▅▂
    data = [[1], [2], [3]]
    tipo = HORIZONTAL_BAR
    #tipo = VERTICAL_BAR
    plot1 = GtkCairoPlot(tipo, data, y_labels = ["Uno", "Dos", "Tres"])
                         #x_labels = ["0", "1", "2", "3"])
    box = gtk.VBox()
    box.pack_start(plot1)
    plot2 = create_cagraph_plot(tipo, data, y_labels = ["Uno", "Dos", "Tres"])
    box.pack_start(plot2)
    win.add(box)
    return win, plot1, plot2

def main():
    """
    Prueba rápida de que funciona.
    """
    wintest, plot1, plot2 = build_test_window()
    wintest.show_all()
    gtk.main()

if __name__ == "__main__":
    main()

