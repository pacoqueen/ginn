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
## muestras_pendientes.py - Muestras pendientes de analizar. 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 26 de abril de 2006 -> Inicio
## 
###################################################################
## PLAN: No estaría mal mostrar valores estadísticos como la media
##       y la desviación típica de las pruebas.
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time
try:
    import pclases
except ImportError:
    import sys
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    import pclases
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes
import mx.DateTime


class MuestrasPendientes(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'muestras_pendientes.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_actualizar/clicked': self.actualizar
                      }
        self.add_connections(connections)
        self.inicializar_ventana()
        gtk.main()

    def chequear_sigue_pendiente(self, m):
        """
        Recibe una muestra. Si la muestra pertenece a un lote en el que
        ya se han realizado todas las pruebas posibles, pone el campo
        pendiente a False y establece la hora de recepción de la muestra
        a la actual.
        """
        if m.lote and \
           m.lote.pruebasElongacion and \
           m.lote.pruebasEncogimiento and \
           m.lote.pruebasGrasa and \
           m.lote.pruebasRizo and \
           m.lote.pruebasTenacidad:
            m.pendiente = False
            m.recepcion = mx.DateTime.localtime()
        if m.partida and not m.partida.esta_pendiente():
            m.pendiente = False
            m.recepcion = mx.DateTime.localtime()

    # --------------- Funciones auxiliares ------------------------------
    def inicializar_ventana(self):
        """
        Inicializa los widgets de la ventana.
        """
        self.inicializar_tv_fibra()
        self.inicializar_tv_geotextil()
        # self.wids['ventana'].maximize()
        self.wids['ventana'].resize(640, 480)
        self.wids['ventana'].set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.actualizar()

    def inicializar_tv_fibra(self):
        cols = (('Fecha', 'gobject.TYPE_STRING', False, True, False, None),
                ('Código', 'gobject.TYPE_STRING', False, True, True, None),
                ('Observaciones', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Lote', 'gobject.TYPE_STRING', False, True, False, None),
                ('Pendiente', 'gobject.TYPE_BOOLEAN', 
                    True, True, False, self.cambiar_pendiente_f),
                ('Tenacidad', 'gobject.TYPE_STRING', False, True, False, None),
                ('Elongación', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Rizo', 'gobject.TYPE_STRING', False, True, False, None),
                ('Encogimiento', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Grasa', 'gobject.TYPE_FLOAT', False, True, False, None),
                ('ID', 'gobject.TYPE_INT64', False, True, False, None)
               )
        utils.preparar_listview(self.wids['tv_fibra'], cols)
        self.wids['tv_fibra'].connect("row-activated", 
            self.abrir_resultados_fib)
        self.colorear_fibra(self.wids['tv_fibra'])

    def inicializar_tv_geotextil(self):
        cols = (('Fecha', 'gobject.TYPE_STRING', False, True, False, None),
                ('Código', 'gobject.TYPE_STRING', False, True, True, None),
                ('Observaciones', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Partida', 'gobject.TYPE_STRING', False, True, False, None),
                ('Pendiente', 'gobject.TYPE_BOOLEAN', 
                    True, True, False, self.cambiar_pendiente_g),
                ('Longitudinal', 'gobject.TYPE_FLOAT', 
                    False, True, False, None),
                ('Transversal', 'gobject.TYPE_FLOAT', 
                    False, True, False, None),
                ('CBR', 'gobject.TYPE_FLOAT', False, True, False, None),
                ('Perforación', 'gobject.TYPE_FLOAT', 
                    False, True, False, None),
                ('Permeabilidad', 'gobject.TYPE_FLOAT', 
                    False, True, False, None),
                ('Punzonado piramidal', 'gobject.TYPE_FLOAT', 
                    False, True, False, None),
                ('ID', 'gobject.TYPE_INT64', False, True, False, None)
                )
        utils.preparar_listview(self.wids['tv_geotextil'], cols)
        self.wids['tv_geotextil'].connect("row-activated", 
            self.abrir_resultados_geo)
        self.colorear_geotextil(self.wids['tv_geotextil'])

    def abrir_resultados_fib(self, tv, path, view_column):
        mid = tv.get_model()[path][-1]
        m = pclases.Muestra.get(mid)
        lote = m.lote
        import resultados_fibra
        ventana = resultados_fibra.ResultadosFibra(lote, 
            usuario = self.usuario)

    def abrir_resultados_geo(self, tv, path, view_column):
        mid = tv.get_model()[path][-1]
        m = pclases.Muestra.get(mid)
        partida = m.partida
        import resultados_geotextiles
        ventana = resultados_geotextiles.ResultadosGeotextiles(partida, 
                    usuario = self.usuario)

    def cambiar_pendiente_f(self, cell, path):
        self.cambiar_pendiente(cell, path, self.wids['tv_fibra'])
        
    def cambiar_pendiente_g(self, cell, path):
        self.cambiar_pendiente(cell, path, self.wids['tv_geotextil'])

    def colorear_fibra(self, tv):
        def cell_func(column, cell, model, itr, i):
            idmuestra = model[itr][-1]
            muestra = pclases.Muestra.get(idmuestra)
            if i == 5:
                pruebas = muestra.lote.pruebasTenacidad
            elif i == 6:
                pruebas = muestra.lote.pruebasElongacion
            elif i == 7:
                pruebas = muestra.lote.pruebasRizo
            elif i == 8:
                pruebas = muestra.lote.pruebasEncogimiento
            elif i == 9:
                pruebas = muestra.lote.pruebasGrasa
            else:
                pruebas = True
            if pruebas:
                color = "white"
            else:
                color = "navajo white"
            cell.set_property("cell-background", color)
            if i == 9:
                cell.set_property("text", "%.2f %%" % model[itr][i])
            elif i in (5,6,7,8):
                cell.set_property("text", model[itr][i])
        # No me preguntes por qué, pero en el resto de funciones colorear 
        # que tengo por ahí no necesitaba hacer esto. Y de repente, aquí, 
        # si no pongo el property "text" a mano lo  que me mete en los cells 
        # es el valor de i, pero encima sólo para las columnas 5 a 9. Es 
        # decir, que aparece directamente en todos los rows: 5   6   7   8   9
        cols = tv.get_columns()
        for i in xrange(len(cols)):
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell, cell_func, i)

    def colorear_geotextil(self, tv):
        def cell_func(column, cell, model, itr, i):
            idmuestra = model[itr][-1]
            muestra = pclases.Muestra.get(idmuestra)
            if i == 5:
                pruebas = muestra.partida.pruebasResistenciaLongitudinal
            elif i == 6:
                pruebas = muestra.partida.pruebasResistenciaTransversal
            elif i == 7:
                pruebas = muestra.partida.pruebasCompresion
            elif i == 8:
                pruebas = muestra.partida.pruebasPerforacion
            elif i == 9:
                pruebas = muestra.partida.pruebasPermeabilidad
            elif i == 10:
                pruebas = muestra.partida.pruebasPiramidal
            else:
                pruebas = True
            if pruebas:
                color = "white"
            else:
                color = "navajo white"
            cell.set_property("cell-background", color)
            if i in (5,6,7,8,9,10):
                cell.set_property("text", "%.3f" % model[itr][i])
        cols = tv.get_columns()
        for i in xrange(len(cols)):
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell, cell_func, i)

    def rellenar_muestras_fibra(self):
        model = self.wids['tv_fibra'].get_model()
        model.clear()
        muestras = pclases.Muestra.select(pclases.AND(
            pclases.Muestra.q.loteID != None, 
            pclases.Muestra.q.pendiente == True))
        for m in muestras:
            m.sync()
            m.lote.sync()
            self.chequear_sigue_pendiente(m)
            model.append((m.envio.strftime('%d/%m/%Y %H:%M'),
                          m.codigo,
                          self.wraplines(m.observaciones, 30),
                          m.lote.numlote,
                          m.pendiente,
                          m.lote.tenacidad,
                          m.lote.elongacion,
                          m.lote.rizo,
                          m.lote.encogimiento,
                          m.lote.grasa,
                          m.id))
        
    def rellenar_muestras_geotextil(self):
        model = self.wids['tv_geotextil'].get_model()
        model.clear()
        muestras = pclases.Muestra.select(pclases.AND(
            pclases.Muestra.q.partidaID != None, 
            pclases.Muestra.q.pendiente == True))
        for m in muestras:
            m.sync()
            m.partida.sync()
            self.chequear_sigue_pendiente(m)
            model.append((m.envio.strftime('%d/%m/%Y %H:%M'),
                          m.codigo,
                          self.wraplines(m.observaciones, 30),
                          m.partida.numpartida,
                          m.pendiente,
                          m.partida.longitudinal,
                          m.partida.transversal,
                          m.partida.compresion,
                          m.partida.perforacion,
                          m.partida.permeabilidad,
                          m.partida.piramidal,
                          m.id))
 
    def wraplines(self, texto, MAX):
        """
        Hace básicamente lo mismo que el cutmaster de menu.py, 
        pero con otro tamaño. Voy con prisas y no me quiero parar
        ahora a modificarlo para que acepte el máximo por 
        parámetro, importarlo o meterlo en utils.
        """
        if len(texto) > MAX:
            palabras = texto.split(' ')
            t = ''
            l = ''
            for p in palabras:
                if len(l) + len(p) + 1 < MAX:
                    l += "%s " % p
                else:
                    t += "%s\n" % l
                    l = "%s " % p
                if len(l) > MAX:    # Se ha colado una palabra de más del MAX
                    tmp = l
                    while len(tmp) > MAX:
                        t += "%s-\n" % tmp[:MAX]
                        tmp = tmp[MAX:]
                    l = tmp
                # print t.replace("\n", "|"), "--", l, "--", p
            t += l
            res = t
        else:
            res = texto
        return res

    # --------------- Manejadores de eventos ----------------------------
    def cambiar_pendiente(self, cell, path, tv):
        model = tv.get_model()
        pendiente = not cell.get_active()
        idm = model[path][-1]
        muestra = pclases.Muestra.get(idm)
        muestra.pendiente = pendiente
        muestra.recepcion = mx.DateTime.localtime()
        model[path][4] = pendiente

    def actualizar(self, w = None):
        self.rellenar_muestras_fibra()
        self.rellenar_muestras_geotextil()


if __name__=='__main__':
    m = MuestrasPendientes()

