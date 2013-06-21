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
## DONE:No estaría mal poner un plot en rojo con el mínimo del 
## producto cuando elija una gráfica de un solo producto.
###################################################################

from formularios import ventana_progreso
from framework import pclases
from informes import geninformes
from math import log10 as log
try:
    from pychart import * # No me gusta, pero no queda otra @UnusedWildImport
    pychart_available = True
except ImportError:
    pychart_available = False
from tempfile import gettempdir
from ventana import Ventana
import gtk
import mx.DateTime
import os
import pygtk
from formularios import utils
pygtk.require('2.0')

class HistoricoExistenciasCompra(Ventana):
        
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.grafico = None
        Ventana.__init__(self, 'historico_existencias.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_fecha/clicked': self.set_fecha,
                       'b_imprimir/clicked': self.imprimir,
                       'b_actualizar/clicked': self.cambiar_grafico, 
                      }
        self.add_connections(connections)
        self.wids['ventana'].set_title(
            "Histórico de existencias de productos de compra")
        fechactual = mx.DateTime.localtime()
        fechactual = mx.DateTime.DateTimeFrom(
            day = 1, month = fechactual.month, year = fechactual.year)
        primero_de_mes_corriente = utils.str_fecha(fechactual)
        self.wids['e_fecha'].set_text(primero_de_mes_corriente)
        opciones = [(p.id, p.descripcion) 
                    for p in pclases.ProductoCompra.select(
                        pclases.ProductoCompra.q.obsoleto == False, 
                        orderBy = "descripcion") 
                    if p.controlExistencias]
        opciones.insert(0, (-3, "Toda la materia prima"))
        opciones.insert(0, (-2, "Toda la granza"))
        opciones.insert(0, (-1, "Todos (escala logarítmica)"))
        utils.rellenar_lista(self.wids['cbe_grafico'], opciones)
        gtk.main()

    def set_fecha(self, boton):
        """
        Cambia la fecha a la seleccionada en la ventana calendario.
        """
        self.wids['e_fecha'].set_text(utils.str_fecha(
            utils.mostrar_calendario(padre = self.wids['ventana'])))

    def chequear_cambios(self):
        pass

    def cambiar_grafico(self, cbe):
        """
        Cambia el gráfico del histórico por el de la opción seleccionada en el 
        combobox.
        """
        ide = utils.combo_get_value(self.wids['cbe_grafico'])
        if ide == None:
            return
        datos = {}
        datos_por_producto = {}
        fechas = get_fechas()
        i = -13
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        act = 0.0
        tot = 13.0
        vpro.mostrar()
        if ide < 0:
            # Mostrar todos o toda la materia prima.
            if ide == -1:    # Todos.
                productos = pclases.ProductoCompra.select(pclases.AND(
                        pclases.ProductoCompra.q.existencias >0, 
                        pclases.ProductoCompra.q.controlExistencias == True, 
                        pclases.ProductoCompra.q.obsoleto == False), 
                    orderBy = "descripcion")    # Es que todos, todos... no se 
                                                # ve nada.
            elif ide == -2:  # Toda la granza.
                productos = pclases.ProductoCompra.select(pclases.AND(
                      pclases.ProductoCompra.q.descripcion.contains("GRANZA"), 
                      pclases.ProductoCompra.q.controlExistencias == True, 
                      pclases.ProductoCompra.q.obsoleto == False), 
                    orderBy = "descripcion")
            elif ide == -3:  # Toda la MP.
                try:
                    matprima = pclases.TipoDeMaterial.select(
                         pclases.TipoDeMaterial.q.descripcion.contains("prima")
                        )[0]
                except IndexError:
                    utils.dialogo_info(
                        titulo = "ERROR BUSCANDO TIPO DE MATERIAL", 
                        texto = 'No se encontró el tipo de material "Materia'
                                ' Prima".\nSe mostrará únicamente la granza.', 
                        padre = self.wids['ventana'])
                    productos = pclases.ProductoCompra.select(pclases.AND(
                      pclases.ProductoCompra.q.descripcion.contains("granza"), 
                      pclases.ProductoCompra.q.controlExistencias == True, 
                      pclases.ProductoCompra.q.obsoleto == False), 
                      orderBy = "descripcion")
                else:
                    productos = pclases.ProductoCompra.select(pclases.AND(
                      pclases.ProductoCompra.q.tipoDeMaterialID == matprima.id,
                      pclases.ProductoCompra.q.controlExistencias == True, 
                      pclases.ProductoCompra.q.obsoleto == False), 
                      orderBy = "descripcion") 
            for fecha in fechas:
                vpro.set_valor(act/tot, 'Contando existencias a %s...' % (
                    utils.str_fecha(fecha)))
                i += 1
                for producto in productos:
                    if ide == -1:
                        if producto not in datos_por_producto:
                            datos_por_producto[producto] = {}
                        strfecha = utils.str_fecha(fecha)
                        datos_por_producto[producto][strfecha] = [0, i]
                        if (fecha.strftime("%d/%m/%Y") 
                            != mx.DateTime.localtime().strftime("%d/%m/%Y")):
                            datos_por_producto[producto][strfecha][0] \
                                = producto.get_existencias_historico(fecha)
                        else:
                            datos_por_producto[producto][strfecha][0] \
                                = producto.existencias
                    else:
                        if utils.str_fecha(fecha) not in datos:
                            datos[utils.str_fecha(fecha)] = [0, i]
                        if (fecha.strftime("%d/%m/%Y") 
                            != mx.DateTime.localtime().strftime("%d/%m/%Y")):
                            datos[utils.str_fecha(fecha)][0] \
                                += producto.get_existencias_historico(fecha)
                        else:
                            datos[utils.str_fecha(fecha)][0] \
                                += producto.existencias
                act += 1
        elif ide > 0:
            producto = pclases.ProductoCompra.get(ide)
            for fecha in fechas:
                vpro.set_valor(act/tot, 'Contando existencias a %s...' % (
                    utils.str_fecha(fecha)))
                i += 1
                if (fecha.strftime("%d/%m/%Y") 
                        != mx.DateTime.localtime().strftime("%d/%m/%Y")):
                    datos[utils.str_fecha(fecha)] \
                        = [producto.get_existencias_historico(fecha), i]
                else:
                    datos[utils.str_fecha(fecha)] = [producto.existencias, i]
                act += 1
        vpro.set_valor(0.99, 'Generando gráfica...')
        while gtk.events_pending(): gtk.main_iteration(False)
        self.dibujar_grafico(datos, datos_por_producto, producto)
        vpro.ocultar()

    def dibujar_grafica_multiple(self, datos_por_producto):
        """
        Dibuja un plot con una línea por cada producto.
        """
        try:
            theme.get_options()  # @UndefinedVariable
        except TypeError:
            pass    # Error en esta versión de PyChart.
        theme.use_color = True  # @UndefinedVariable
        theme.reinitialize()  # @UndefinedVariable
        tempdir = gettempdir()
        formato = "png"   # NECESITA ghostscript
        nomarchivo = "%s.%s" % (mx.DateTime.localtime().strftime(
            "ghistoricoprodcompra_%Y_%m_%d_%H_%M_%S"), formato)
        nombregraph = os.path.join(tempdir, "%s") % (nomarchivo)
        can = canvas.init(fname = nombregraph, format = formato)  # @UndefinedVariable

        # Máximos y mínimos:
        min_global = 0
        max_global = 1
        for producto in datos_por_producto:
            datos = datos_por_producto[producto]
            data = [[datos[d][1], d.replace("/","//"), 
                     log([datos[d][0] > 0 and datos[d][0] or 1][0])] 
                    for d in datos]
            def cmp_data(d1, d2):
                return d1[0] - d2[0]
            data.sort(cmp_data)
            data = [[i[1], i[2]] for i in data]
            max_y = max([i[1] for i in data])
            max_y *= 1.1    # Un 10% más, para que quede bonita la gráfica.
            min_y = min([i[1] for i in data])
            min_y *= 1.1
            min_global = min(0, min_y, min_global)   # Para evitar que quede 
                                            # un valor positivo como mínimo.
            max_global = max(1, max_y, max_global)

        xaxis = axis.X(label="Fecha")  # @UndefinedVariable
        yaxis = axis.Y(label="Existencias", tic_interval=int(max_y) / 10)  # @UndefinedVariable
        ar = area.T(x_coord = category_coord.T(data, 0), x_range=(-13, 0),  # @UndefinedVariable
                    y_range=(int(min_global), int(max_global)), 
                    x_axis = xaxis, y_axis = yaxis, size = (640, 480))

        for producto in datos_por_producto:
            datos = datos_por_producto[producto]
            data = [[datos[d][1], d.replace("/","//"), 
                     log([datos[d][0] > 0 and datos[d][0] or 1][0])] 
                    for d in datos]
            def cmp_data(d1, d2):
                return d1[0] - d2[0]
            data.sort(cmp_data)
            data = [[i[1], i[2]] for i in data]

            ar.add_plot(line_plot.T(  # @UndefinedVariable
                label = producto.descripcion.replace("/", "//")[:30], 
                data = data))

        ar.draw()

        try:
            can.close()
            self.wids['grafico'].set_size_request(650, 490)
            self.wids['ventana'].maximize()
            self.wids['grafico'].set_from_file(nombregraph)
        except:
            utils.dialogo_info(titulo = "NECESITA GHOSTSCRIPT",
                texto = "Para ver gráficas en pantalla necesita instalar "
                        "Ghostscript.\nPuede encontrarlo en el servidor de la"
                        " aplicación o descargarlo de la web "
                        "(http://www.cs.wisc.edu/~ghost/).",
                padre = self.wids['ventana'])
        self.grafico = nombregraph

    def dibujar_grafico(self, datos, datos_por_producto, producto = None):
        """
        Dibuja el gráfico a partir del diccionario de datos recibido.
        Si se va a dibujar únicamente un producto, éste debe recibirse como 
        parámetro.
        """
        if pychart_available and datos_por_producto != {}:
            self.dibujar_grafica_multiple(datos_por_producto) 
        elif pychart_available and len(datos) > 0:
            try:
                theme.get_options()  # @UndefinedVariable
            except TypeError:
                pass    # ¿Peta esta versión de PyChart?
            theme.use_color = True  # @UndefinedVariable
            theme.reinitialize()  # @UndefinedVariable
            tempdir = gettempdir()
            formato = "png"   # NECESITA ghostscript
            nomarchivo = "%s.%s" % (
                mx.DateTime.localtime().strftime(
                    "ghistoricoprodcompra_%Y_%m_%d_%H_%M_%S"), 
                formato)
            nombregraph = os.path.join(tempdir, "%s") % (nomarchivo)
            can = canvas.init(fname = nombregraph, format = formato)  # @UndefinedVariable
            data = [[datos[d][1], d.replace("/","//"), datos[d][0]] 
                    for d in datos]
            def cmp_data(d1, d2):
                return d1[0] - d2[0]
            data.sort(cmp_data)
            # Una línea con el mínimo del producto:
            try:
                minimoproducto = producto.minimo
            except AttributeError:
                minimoproducto = 0
            data = [[i[1], i[2], minimoproducto] for i in data]
            max_y = max([i[1] for i in data])
            max_y *= 1.1    # Un 10% más, para que quede bonita la gráfica.
            max_y = max(1, max_y)   # Para evitar que quede 0 como máximo.
            min_y = min([i[1] for i in data])
            min_y *= 1.1
            min_y = min(0, min_y)   # Para evitar que quede un valor positivo 
                                    # como mínimo.
            xaxis = axis.X(label="Fecha")  # @UndefinedVariable
            yaxis = axis.Y(label="Existencias", tic_interval=int(max_y) / 10)  # @UndefinedVariable
            ar = area.T(x_coord = category_coord.T(data, 0),  # @UndefinedVariable
                        x_range=(-13, 0), 
                        y_range=(int(min_y), 
                        int(max_y)), 
                        x_axis = xaxis, 
                        y_axis = yaxis, 
                        size = (640, 480)) 
            ar.add_plot(line_plot.T(label="existencias", data=data, ycol=1),  # @UndefinedVariable
                        line_plot.T(label = "mínimo", data = data, ycol=2))  # @UndefinedVariable
            ar.draw()

            try:
                can.close()
                self.wids['grafico'].set_size_request(650, 490)
                self.wids['ventana'].maximize()
                self.wids['grafico'].set_from_file(nombregraph)
            except:
                utils.dialogo_info(titulo = "NECESITA GHOSTSCRIPT",
                    texto = "Para ver gráficas en pantalla necesita instalar"
                            " Ghostscript.\nPuede encontrarlo en el servidor"
                            " de la aplicación o descargarlo de la web"
                            " (http://www.cs.wisc.edu/~ghost/).",
                    padre = self.wids['ventana'])
            self.grafico = nombregraph
        else:
            self.wids['grafico'].set_from_file(
                "NOEXISTEPORTANTOVAADIBUJARUNASPA")
            self.grafico = None

    def imprimir(self,boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        from formularios import reports
        fechastr = self.wids['e_fecha'].get_text()
        fecha = utils.parse_fecha(fechastr)
        reports.abrir_pdf(
            geninformes.existencias(hasta = fecha, 
                                    ventana_padre = self.wids['ventana']))

def get_fechas():
    """
    Devuelve una lista de fechas mx.DateTime correspondientes 
    al día 1 de cada mes de un año atras hasta el mes actual.
    """
    fechas = []
    ultima = mx.DateTime.DateTimeFrom(day = 1, 
                                      month = mx.DateTime.localtime().month, 
                                      year = mx.DateTime.localtime().year)
    primera = mx.DateTime.DateTimeFrom(day = ultima.day, 
                                       month = ultima.month, 
                                       year = ultima.year -1)
    for incr_mes in xrange(12):
        mes = primera.month + incr_mes
        anno = primera.year
        try:
            fechas.append(mx.DateTime.DateTimeFrom(day = primera.day, 
                                                   month = mes, 
                                                   year = anno))
        except mx.DateTime.RangeError:
            anno = primera.year + (mes / 12)
            mes = mes % 12
            fechas.append(mx.DateTime.DateTimeFrom(day = primera.day, 
                                                   month = mes, 
                                                   year = anno))
    fechas.append(ultima)
    fechas.append(mx.DateTime.localtime())
    return fechas


if __name__ == '__main__':
    t = HistoricoExistenciasCompra() 
