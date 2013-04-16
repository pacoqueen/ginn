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
## resultados_longitudinal.py - Resistencia alargamiento longitudinal 
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
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk, time
from framework import pclases
from utils import _float as float

# XXX
# Aprovechando que todas las pruebas sobre rollos son similares, modificando
# estas variables globales se tienen las 5 ventanas.
# ¿Por qué no hacer un único .py y cambiar estas variables en función de la
# prueba que se quiera insertar? Muy simple, porque CWT. En un futuro puede 
# cambiar el tipo de datos de un resultado o algo así y habría que crear una
# ventana nueva de cero.
puntoglade = 'resultados_perforacion.glade'    # Archivo glade
claseprueba = pclases.PruebaPerforacion    # Clase de pclases.
nombrecampo = 'pruebasPerforacion'       # Campo de "partida".
nombreprueba = 'perforacion'   # Nombre de la prueba (media de resultados) en la partida.
titulo = 'Resultados de perforación'
# XXX

class ResultadosPerforacion(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        Ventana.__init__(self, puntoglade, objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_lote/clicked': self.set_partida,
                       'b_fecha/clicked': self.fecha,
                       'b_add/clicked': self.add,
                       'b_drop/clicked': self.drop
                      }
        self.add_connections(connections)
        self.activar_widgets(False)
        self.inicializar_ventana()
        self.partida = None
        gtk.main()

    # --------------- Funciones auxiliares ------------------------------
    def activar_widgets(self, valor):
        self.ws = ('e_numpartida', 
                   'e_nombre',
                   'e_longitudinal',
                   'e_transversal',
                   'e_compresion',
                   'e_perforacion',
                   'e_permeabilidad',
                   'e_fecha',
# XXX
                   'e_poros',
                   'e_espesor',
                   'tv_lotes',
# XXX
                   'e_resultado',
                   'tv_pruebas',
                   'b_add',
                   'b_drop',
                   'b_fecha')
        for i in self.ws:
            self.wids[i].set_sensitive(valor)
    
    def crear_listview(self, tv):
        cols = (('Fecha', 'gobject.TYPE_STRING', True, True, True, self.cambiar_fecha),
                ('Resultado', 'gobject.TYPE_FLOAT', True, True, False, self.cambiar_resultado), 
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(tv, cols)
        tv.get_column(1).get_cell_renderers()[0].set_property('xalign', 0.1) 

    def inicializar_ventana(self):
        """
        Inicializa los widgets de la ventana.
        """
        self.wids['ventana'].set_title(titulo)
        self.crear_listview(self.wids['tv_pruebas'])
# XXX
        self.crear_treeview(self.wids['tv_lotes'])

    def crear_treeview(self, tv):
        cols = (('Lote y materia prima consumida', 'gobject.TYPE_STRING', False, True, True, None),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_treeview(tv, cols)
        
    def rellenar_lotes(self):
        model = self.wids['tv_lotes'].get_model()
        model.clear()
        partida = self.partida
        lotes = []
        prods = []
        for b in partida.balas:
            if b.lote not in lotes:
                lotes.append(b.lote)
                itr = model.append(None, (b.lote.numlote, b.lote.id))
            for a in b.articulos:
                for c in a.parteDeProduccion.consumos:
                    if c.productoCompra not in prods:
                        prods.append(c.productoCompra)
                        model.append(itr, (c.productoCompra.descripcion, c.id))
# XXX

    def rellenar_pruebas(self):
        """
        Introduce en el treeview las pruebas del partida seleccionado y 
        recalcula la característica del partida.
        """
        model = self.wids['tv_pruebas'].get_model()
        model.clear()
        self.calcular_caracteristicas()
        pruebas = claseprueba.select(claseprueba.q.partidaID == self.partida.id)
        for prueba in pruebas:
            model.append((utils.str_fecha(prueba.fecha), prueba.resultado, prueba.id))
       
    def calcular_caracteristicas(self):
        """
        Calcula la media de los valores de las pruebas y actualiza la partida.
        """
        partida = self.partida
        media = 0.0
        for p in getattr(partida, nombrecampo):
            media += p.resultado
        try:
            media /= len(getattr(partida, nombrecampo))
        except ZeroDivisionError:
            media = 0
        setattr(partida, nombreprueba, media)
        self.rellenar_info_partida()

    def actualizar_ventana(self):
        """
        Método que sobreescribe el "actualizar_ventana" que hereda de la clase ventana.
        PRECONDICION: self.partida no puede ser None
        """
        try:
            self.partida.sync()
            self.rellenar_widgets()
        except pclases.SQLObjectNotFound:
                utils.dialogo_info(titulo = 'REGISTRO ELIMINADO', texto = 'El registro ha sido borrado desde otro puesto.')
                self.partida = None
        self.activar_widgets(self.partida!=None)


    # --------------- Manejadores de eventos ----------------------------
    def add(self, w):
        if self.partida != None:
            fecha = self.wids['e_fecha'].get_text()
            if fecha == '':
                utils.dialogo_info(titulo = 'SIN FECHA',
                                   texto = 'Debe introducir la fecha del resultado de la prueba.')
                return
            resultado = self.wids['e_resultado'].get_text()
            if resultado == '':
                utils.dialogo_info(titulo = 'SIN RESULTADO',
                                   texto = 'Debe introducir el resultado de la prueba.')
                return
            try:
                prueba = claseprueba(fecha = time.strptime(fecha, '%d/%m/%Y'),  # @UnusedVariable
                                     resultado = resultado,
                                     partida = self.partida)
            except:
                utils.dialogo_info(titulo = 'ERROR', 
                                   texto = 'Verifique que ha introducido los datos correctamente.')
            self.wids['e_fecha'].set_text(utils.str_fecha(time.localtime()))
            self.wids['e_resultado'].set_text('')
            self.rellenar_pruebas()
        else:
            print "WARNING: Se ha intentano añadir una prueba con partida = None"
    
    def drop(self, w):
        model, itr = self.wids['tv_pruebas'].get_selection().get_selected()
        if itr != None and utils.dialogo(titulo = 'BORRAR PRUEBA', texto = '¿Está seguro?'):
            ide = model[itr][-1]
            prueba = claseprueba.get(ide)
            prueba.destroy(ventana = __file__)
            self.rellenar_pruebas()

    def set_partida(self, w):
        numpartida = utils.dialogo_entrada(titulo = 'Nº PARTIDA', 
                                        texto = 'Introduzca número de partida:')
        if numpartida != None:
            partidas = pclases.Partida.select(pclases.Partida.q.numpartida.contains(numpartida))
            if partidas.count() == 0:
                utils.dialogo_info(titulo = 'PARTIDA NO ENCONTRADA', 
                                   texto = 'No se encontró ninguna partida %s.' % numpartida)
                return
            elif partidas.count() > 1:
                filas = [(l.id, l.numpartida, l.codigo, l.longitudinal, l.transversal, l.compresion, l.perforacion, l.permeabilidad, l.poros, l.espesor) for l in partidas]
                idpartida = utils.dialogo_resultado(filas, 
                                                 titulo = 'SELECCIONE PARTIDA',
                                                 cabeceras = ('ID', 'Número', 'Código', 'Longitudinal', 'Transversal', 'CBR', 'Perforación', 'Permeabilidad', 'Poros', 'Espesor'))
                if idpartida < 0:
                    return
                partida = pclases.Partida.get(idpartida)
            else:
                partida = partidas[0]
            if len(partida.rollos) == 0:
                utils.dialogo_info(titulo = 'PARTIDA VACÍA', 
                                   texto = 'La partida no contiene rollos, no puede\nrealizar pruebas sobre una partida vacía.')
                self.partida = None
                return
            self.partida = partida
            self.actualizar_ventana()
    
    def rellenar_widgets(self):
        self.activar_widgets(self.partida != None)
        if self.partida != None:
            self.rellenar_info_partida()
            self.rellenar_pruebas()
            self.wids['e_fecha'].set_text(utils.str_fecha(time.localtime()))
            self.wids['e_resultado'].set_text('')

    def rellenar_info_partida(self):
        """
        PRECONDICIÓN: self.partida != None y len(self.partida.rollos) > 0
        """
        partida = self.partida
        self.wids['e_numpartida'].set_text("%d (%s)" % (partida.numpartida, partida.codigo))
        self.wids['e_nombre'].set_text(partida.rollos[0].articulos[0].productoVenta.nombre)
        self.wids['e_longitudinal'].set_text("%.2f" % partida.longitudinal)
        self.wids['e_transversal'].set_text("%.2f" % partida.transversal)
        self.wids['e_compresion'].set_text("%.2f" % partida.compresion)
        self.wids['e_perforacion'].set_text("%.2f" % partida.perforacion)
        self.wids['e_permeabilidad'].set_text("%.2f" % partida.permeabilidad)
# XXX
        self.wids['e_poros'].set_text("%.2f" % partida.poros)
        self.wids['e_espesor'].set_text("%.2f" % partida.espesor)
        self.rellenar_lotes()
# XXX
 
    def fecha(self, w):
        self.wids['e_fecha'].set_text(utils.str_fecha(utils.mostrar_calendario(fecha_defecto = self.objeto and self.objeto.fecha or None, padre = self.wids['ventana'])))

    def cambiar_fecha(self, cell, path, texto):
        model = self.wids['tv_pruebas'].get_model()
        prueba = claseprueba.get(model[path][-1])
        try:
            prueba.fecha = time.strptime(texto, '%d/%m/%Y')
        except:
            utils.dialogo_info('FECHA INCORRECTA', 
                               'La fecha introducida (%s) no es correcta.' % texto)
        self.rellenar_pruebas()

    def cambiar_resultado(self, tv, path, texto):
        model = self.wids['tv_pruebas'].get_model()
        prueba = claseprueba.get(model[path][-1])
        try:
            prueba.resultado = float(texto)
        except:
            utils.dialogo_info('RESULTADO INCORRECTO',
                               'El número tecleado (%s) no es correcto.' % texto)
        self.rellenar_pruebas()

if __name__=='__main__':
    a = ResultadosPerforacion()

