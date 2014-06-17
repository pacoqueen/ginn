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
    import cairo
except:
    raise SystemExit

if gtk.pygtk_version < (2, 0):
    print "Se necesita PyGtk 2.0 o posterior."
    raise SystemExit

import sys, os
LIBDIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "lib"))
sys.path.append(LIBDIR)
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
from cagraph.cagraph.series.labels import CaGraphSeriesLabels


(HORIZONTAL,    # 0
 VERTICAL,      # 1
 TARTA,         # 2
 GRAFO          # 3
) = range(4)

class GtkCairoPlot(gtk.DrawingArea):
    """
    Widget que incluye un gráfico de CairoPlot en él.
    """
    def __init__(self, tipo, data = {}):
        """
        Recibe un tipo de gráfica a representar en «tipo».
        En «data» recibe un diccionario con las etiquetas de los valores como
        claves y los valores en series (listas o tuplas) de cada etiqueta.
        """
        super(GtkCairoPlot, self).__init__()
        self._tipo = tipo
        self._data, self._labels = check_data(data, tipo)
        self.width = -1
        self.height = -1
        self.plt = self._prepare_plot()
        self.set_size_request(self.width, self.height)
        self.connect("expose_event", self.expose)

    def _prepare_plot(self):
        """
        Crea el objeto de la biblioteca que corresponda según el tipo.
        """
        if self._tipo == HORIZONTAL:
            plot = CaGraph()
            xaxis = CaGraphXAxis(plot)
            yaxis = CaGraphYAxis(plot)
            yaxis.axis_style.draw_labels = yaxis.axis_style.draw_tics = False
            plot.axiss.append(xaxis)
            plot.axiss.append(yaxis)
            plot.seriess.append(CaGraphSeriesHBar(plot, 0, 1))
            plot.seriess.append(CaGraphSeriesLabels(plot, 0, 1))
            plot.seriess[0].data = self._data
            plot.seriess[1].data = self._labels
            plot.auto_set_range()
        elif self._tipo == VERTICAL:
            raise NotImplementedError("gtkcairoplot: todavía no implementado.")
        elif self._tipo == TARTA:
            # Es simplemente para crear el objeto. Después se reemplazará por
            # el surface del DrawingArea en el expose.
            tempsurface = cairo.SVGSurface(None, self.width, self.height)
            plot = cairoplot.PiePlot(tempsurface,
                                     self._data,
                                     self.width, 
                                     self.height)
            # PORASQUI: Dibuja algo, pero caca. No se ve nada. 
        elif self._tipo == GRAFO:
            raise NotImplementedError("gtkcairoplot: todavía no implementado.")
        else:
            raise ValueError("gtkcairoplot: tipo no reconocido.")
        return plot

    def expose(self, widget, event):
        rect = self.get_allocation()
        self.width = rect.width
        self.height = rect.height
        try:
            self.plt.dimensions[cairoplot.HORZ] = self.width
            self.plt.dimensions[cairoplot.VERT] = self.height
        except AttributeError:
            self.plt.set_allocation(rect)
            self.plt.expose(self, event)
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
        try:
            self.plt.render()
            self.plt.commit()
        except AttributeError:  # Es un cagraph, no un cairograph
            pass

###############################################################################

def check_data(data, tipo):
    """
    Comprueba tipo y valores recibidos para asegurar que concuerdan.
    «data» debe ser un diccionario y si el tipo es un gráfico de tarta,
    entonces los valores deben ser un número por cada clave.
    Si es un gráfico de barras horizontales o verticales, debe ser o bien
    un valor único (una barra por "label") o una lista o tupla de valores
    (varias barras por cada clave).
    """
    if tipo == TARTA:
        _data = {}
        _labels = data.keys()
        _labels.sort()
        for label in data:
            valor = data[label]
            if isinstance(valor, (tuple, list)):    # Si es una serie
                _data[label] = sum(valor)   # lo sustituyo por su suma.
            elif isinstance(valor, (int, float)):
                _data[label] = valor
            else:
                raise TypeError("gtkcairoplot:"
                                " «data» debe ser un diccionario de números")
    elif tipo in (HORIZONTAL, VERTICAL):
        _data = []
        _labels = []
        y = 0
        yoffset = 10    # No hace falta que sea proporcional al eje de abscisas
        labels = data.keys()
        labels.reverse()    # Para que salgan de arriba a abajo
        for label in labels:
            valor = data[label]
            if isinstance(valor, (int, float)):
                _data.append((valor, y))
                _labels.append((valor, y, label))
                y += yoffset
            elif isinstance(valor, (list, tuple)):
                subvalores = valor
                subvalores.reverse()
                for subvalor in subvalores:
                    _data.append((subvalor, y))
                    _labels.append((subvalor, y, 
                                    "%s (%s)" % (label, subvalor)))
                    y += yoffset
            else:
                raise TypeError("gtkcairoplot:"
                                " «data» debe ser un diccionario de listas")
        if not _labels or len(_labels) <= 1:
            raise ValueError("gtkcairoplot: "
                             "Necesita al menos dos series de datos")
    else:
        raise ValueError("gtkcairoplot:"
                         " Debe especificar un tipo de gráfico válido.")
    return _data, _labels

def build_test_window():
    """
    Devuelve una ventana de Gtk con un CairoPlot para pruebas.
    """
    win = gtk.Window()
    win.set_size_request(800, 600)
    win.set_position(gtk.WIN_POS_CENTER)
    win.connect('delete-event', gtk.main_quit)
    import collections
    data = collections.OrderedDict()
    data["Uno"] =  [1, 2, 3]  #  Uno █▅▂
    data["Dos"] =  [4, 5, 6]  #  Dos ████▅▂
    data["Tres"] = [7, 8, 9]  # Tres ███████▅▂
    plot1 = GtkCairoPlot(HORIZONTAL, data)
    #plot1 = gtk.Image()
    #plot1.set_from_stock(gtk.STOCK_MISSING_IMAGE, gtk.ICON_SIZE_DIALOG)
    box = gtk.VBox()
    box.pack_start(plot1)
    plot2 = GtkCairoPlot(TARTA, data)
    box.pack_start(plot2)
    win.add(box)
    return win, plot1, plot2

def main():
    """
    Prueba rápida de que funciona.
    """
    wintest_plot1_plot2 = build_test_window()
    wintest = wintest_plot1_plot2[0]
    wintest.show_all()
    gtk.main()

if __name__ == "__main__":
    main()

