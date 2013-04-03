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

###################################################################
## historico_existencias.py -- 
###################################################################
## NOTAS:
## 
###################################################################
## Changelog:
## 7 de noviembre de 2006 -> Inicio
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, time
import sys, os
try:
    import pclases
except ImportError:
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    import pclases
import mx.DateTime
try:
    import geninformes
except ImportError:
    sys.path.append('../informes')
    import geninformes
import ventana_progreso
sys.path.insert(0, os.path.join("..", "PyChart-1.39"))
from pychart import *   # No me gusta, pero no queda otra
from tempfile import gettempdir
    

class HistoricoExistencias(Ventana):
        
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.grafico = None
        Ventana.__init__(self, 'historico_existencias.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_fecha/clicked': self.set_fecha,
                       'b_imprimir/clicked': self.imprimir,
                       'b_actualizar/clicked': self.cambiar_grafico, 
                      }
        self.add_connections(connections)
        fechactual = mx.DateTime.localtime()
        fechactual = mx.DateTime.DateTimeFrom(day = 1, month = fechactual.month, year = fechactual.year)
        primero_de_mes_corriente = utils.str_fecha(fechactual)
        self.wids['e_fecha'].set_text(primero_de_mes_corriente)
        opciones = [(p.id, p.descripcion) for p in pclases.ProductoVenta.select(orderBy = "descripcion")]
        opciones.insert(0, (-2, "Toda la fibra"))
        opciones.insert(0, (-1, "Todos los geotextiles"))
        utils.rellenar_lista(self.wids['cbe_grafico'], opciones)
        gtk.main()

    def set_fecha(self, boton):
        """
        Cambia la fecha a la seleccionada en la ventana calendario.
        """
        self.wids['e_fecha'].set_text(utils.str_fecha(
            utils.mostrar_calendario(
                fecha_defecto = self.wids['e_fecha'].get_text(), 
                padre = self.wids['ventana'])))

    def chequear_cambios(self):
        pass

    def cambiar_grafico(self, cbe):
        """
        Cambia el gráfico del histórico por el de la opción seleccionada en el 
        combobox.
        """
        id = utils.combo_get_value(self.wids['cbe_grafico'])
        if id == None:
            return
        datos = {}
        fechas = get_fechas()
        i = -13
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        act = 0.0
        tot = 13.0
        vpro.mostrar()
        if id < 0:
            # Mostrar todos los geotextiles o toda la fibra.
            if id == -1:    # Geotextiles
                productos = pclases.ProductoVenta.select(pclases.ProductoVenta.q.camposEspecificosRolloID != None)
            elif id == -2:  # Fibra
                productos = pclases.ProductoVenta.select(pclases.OR(pclases.ProductoVenta.q.camposEspecificosBalaID != None)) 
            for fecha in fechas:
                vpro.set_valor(act/tot, 'Contando existencias a %s...' % (utils.str_fecha(fecha)))
                i += 1
                datos[utils.str_fecha(fecha)] = [0, i]
                for producto in productos:
                    datos[utils.str_fecha(fecha)][0] += producto.get_stock(hasta = fecha)
                act += 1
        elif id > 0:
            producto = pclases.ProductoVenta.get(id)
            for fecha in fechas:
                vpro.set_valor(act/tot, 'Contando existencias a %s...' % (utils.str_fecha(fecha)))
                i += 1
                datos[utils.str_fecha(fecha)] = [producto.get_stock(hasta = fecha), i]
                act += 1
        vpro.set_valor(0.99, 'Generando gráfica...')
        while gtk.events_pending(): gtk.main_iteration(False)
        self.dibujar_grafico(datos)
        vpro.ocultar()

    def dibujar_grafico(self, datos):
        """
        Dibuja el gráfico a partir del diccionario de datos recibido.
        """
        if len(datos) > 0:
            theme.use_color = True  # @UndefinedVariable
            theme.reinitialize()  # @UndefinedVariable
            tempdir = gettempdir()
            formato = "png"   # NECESITA ghostscript
            nomarchivo = "%s.%s" % (mx.DateTime.localtime().strftime("ghistoricoe_%Y_%m_%d_%H_%M_%S"), formato)
            nombregraph = os.path.join(tempdir, "%s") % (nomarchivo)
            can = canvas.init(fname = nombregraph, format = formato)  # @UndefinedVariable
            data = [(datos[d][1], datos[d][0]) for d in datos]
            def cmp_data(d1, d2):
                return d1[0] - d2[0]
            data.sort(cmp_data)
            max_y = max([i[1] for i in data])
            max_y *= 1.1    # Un 10% más, para que quede bonita la gráfica.
            max_y = max(1, max_y)   # Para evitar que quede 0 como máximo.

            xaxis=axis.X(label="Fecha", tic_interval = 1)  # @UndefinedVariable
            yaxis=axis.Y(label="Existencias", tic_interval=int(max_y) / 10)  # @UndefinedVariable
            ar = area.T(x_range=(-13, 0), y_range=(0, int(max_y)), x_axis=xaxis, y_axis=yaxis, size = (640, 480))  # @UndefinedVariable
            ar.add_plot(line_plot.T(label = "existencias", data = data, data_label_format="/8{}%d"))  # @UndefinedVariable
            ar.draw()

            try:
                can.close()
                self.wids['grafico'].set_size_request(650, 490)
                self.wids['ventana'].maximize()
                self.wids['grafico'].set_from_file(nombregraph)
            except:
                utils.dialogo_info(titulo = "NECESITA GHOSTSCRIPT",
                                   texto = "Para ver gráficas en pantalla necesita instalar Ghostscript.\nPuede encontrarlo en el servidor de la aplicación o descargarlo de la web (http://www.cs.wisc.edu/~ghost/).",
                                   padre = self.wids['ventana'])
            self.grafico = nombregraph
        else:
            self.wids['grafico'].set_from_file("NOEXISTEPORTANTOVAADIBUJARUNASPA")
            self.grafico = None


    def imprimir(self,boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        fechastr = self.wids['e_fecha'].get_text()
        fecha = utils.parse_fecha(fechastr)
        fechastr = utils.str_fecha(fecha)
        fechas = pclases.HistorialExistenciasA.get_fechas_cacheadas()
        if fecha not in fechas:
            res = utils.dialogo(
                titulo = "EXISTENCIAS NO CACHEADAS. ¿CONTINUAR?", 
                texto = "La fecha seleccionada no se encuentra precalculada.\n"
                        "Esto implica que el recuento de existencias puede\n"
                        "demorarse incluso horas. Durante este tiempo es \n"
                        "posible que la aplicación no responda.\n\n"
                        "¿Está seguro de que desea continuar?", 
                padre = self.wids['ventana'])
        else:
            res = utils.dialogo(titulo = "¿CONTINUAR?", 
                texto = "La operación puede demorarse durante algún tiempo\n"
                    "y dar la impresión de que la aplicación no responde.\n"
                    "¿Desea continuar?", 
                padre = self.wids['ventana'])
        if not res:
            return
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        self.wids['ventana'].window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        vpro.mostrar()
        act = 0.0
        tot = 2 + pclases.Almacen.select(
                                    pclases.Almacen.q.activo == True).count()
        msgtexto = 'Calculando existencias a %s.' % fechastr
        vpro.set_valor(act/tot, msgtexto)
        vpro._ventana.realize()
        vpro._ventana.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        while gtk.events_pending(): gtk.main_iteration(False)
        import informes
        try:
            vpro.set_valor(act/tot, msgtexto)
            informes.abrir_pdf(geninformes.existencias_productos('rollos', 
                               fechastr, hasta = fecha))
            act += 1
            vpro.set_valor(act/tot, msgtexto)
            informes.abrir_pdf(geninformes.existencias_productos('balas', 
                               fechastr, hasta = fecha))
            act += 1
            vpro.set_valor(act/tot, msgtexto)
            for a in pclases.Almacen.select(pclases.Almacen.q.activo == True, 
                                            orderBy = "id"):
                informes.abrir_pdf(geninformes.existencias_productos('rollos', 
                                   fechastr, hasta = fecha, almacen = a))
                act += 1
                vpro.set_valor(act/tot, msgtexto)
                informes.abrir_pdf(geninformes.existencias_productos('balas', 
                                   fechastr, hasta = fecha, almacen = a))
                act += 1
                vpro.set_valor(act/tot, msgtexto)
        finally:
            vpro.ocultar()
            vpro._ventana.window.set_cursor(None)
            self.wids['ventana'].window.set_cursor(None)


def get_fechas():
    """
    Devuelve una lista de fechas mx.DateTime correspondientes 
    al día 1 de cada mes de un año atras hasta el mes actual.
    """
    fechas = []
    ultima = mx.DateTime.DateTimeFrom(day = 1, month = mx.DateTime.localtime().month, year = mx.DateTime.localtime().year)
    primera = mx.DateTime.DateTimeFrom(day = ultima.day, month = ultima.month, year = ultima.year -1)
    for incr_mes in xrange(12):
        mes = primera.month + incr_mes
        anno = primera.year
        try:
            fechas.append(mx.DateTime.DateTimeFrom(day = primera.day, month = mes, year = anno))
        except mx.DateTime.RangeError:
            anno = primera.year + (mes / 12)
            mes = mes % 12
            fechas.append(mx.DateTime.DateTimeFrom(day = primera.day, month = mes, year = anno))
    fechas.append(ultima)
    return fechas


if __name__ == '__main__':
    t = HistoricoExistencias() 

    
