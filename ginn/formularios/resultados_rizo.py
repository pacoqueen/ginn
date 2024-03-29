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
## resultados_rizo.py - Resultados de pruebas de elongación. 
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


class ResultadosRizo(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        Ventana.__init__(self, 'resultados_rizo.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_lote/clicked': self.set_lote,
                       'b_fecha/clicked': self.fecha,
                       'b_add/clicked': self.add,
                       'b_drop/clicked': self.drop
                      }
        self.add_connections(connections)
        self.activar_widgets(False)
        self.inicializar_ventana()
        self.lote = None
        gtk.main()

    # --------------- Funciones auxiliares ------------------------------
    def activar_widgets(self, valor):
        self.ws = ('e_codigo', 
                   'e_nombre',
                   'e_dtex',
                   'e_corte',
                   'e_color',
                   'e_tenacidad',
                   'e_elongacion',
                   'e_rizo',
                   'e_encogimiento',
                   'e_fecha',
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
        self.crear_listview(self.wids['tv_pruebas'])

    def rellenar_pruebas(self):
        """
        Introduce en el treeview las pruebas del lote seleccionado y 
        recalcula la característica del lote.
        """
        model = self.wids['tv_pruebas'].get_model()
        model.clear()
        self.calcular_caracteristicas()
        pruebas = pclases.PruebaRizo.select(pclases.PruebaRizo.q.loteID == self.lote.id)
        for prueba in pruebas:
            model.append((utils.str_fecha(prueba.fecha), prueba.resultado, prueba.id))
            
    def calcular_caracteristicas(self):
        """
        Calcula la media de los valores de rizo, tenacidad, encogimiento y elongación.
        """
        lote = self.lote
        # La elongación depende del tipo de producto:
        try:
            dtex = lote.balas[0].articulos[0].productoVenta.camposEspecificosBala.dtex  # @UnusedVariable
        except:
            utils.dialogo_info(titulo = 'ERROR', texto = 'Ocurrió un error buscando el tipo de fibra')
            return       
        mediaRizo = 0
        for p in lote.pruebasRizo:
            mediaRizo += p.resultado
        try:
            mediaRizo /= len(lote.pruebasRizo)
        except ZeroDivisionError:
            mediaRizo = 0
        ## Rizo
        lote.rizo = str(int(round(mediaRizo)))
        ## Encogimiento
        #mediaEncogimiento = 0 
        #for i in self.encogimiento:
        #    mediaEncogimiento += i[0]
        #if len(self.encogimiento) != 0:
        #    mediaEncogimiento /= len(self.encogimiento)
        #    if mediaEncogimiento <= 10:
        #        lote.encogimiento = 'B'
        #    elif (mediaEncogimiento >10 and mediaEncogimiento<=15):
        #        lote.encogimiento = 'N'
        #    elif mediaEncogimiento > 15:
        #        lote.encogimiento = 'A'
        #    else:
        #        lote.encogimiento = '?'
        self.rellenar_info_lote()

    def actualizar_ventana(self):
        """
        Método que sobreescribe el "actualizar_ventana" que hereda de la clase ventana.
        PRECONDICION: self.lote no puede ser None
        """
        try:
            self.lote.sync()
            self.rellenar_widgets()
        except pclases.SQLObjectNotFound:
                utils.dialogo_info(titulo = 'REGISTRO ELIMINADO', texto = 'El registro ha sido borrado desde otro puesto.')
                self.lote = None
        self.activar_widgets(self.lote!=None)


    # --------------- Manejadores de eventos ----------------------------
    def add(self, w):
        if self.lote != None:
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
                prueba = pclases.PruebaRizo(fecha = utils.parse_fecha(fecha),
                                            resultado = resultado,
                                            lote = self.lote)
                pclases.Auditoria.nuevo(prueba, self.usuario, __file__)
            except:
                utils.dialogo_info(titulo = 'ERROR', 
                                   texto = 'Verifique que ha introducido los datos correctamente.')
            self.wids['e_fecha'].set_text(utils.str_fecha(time.localtime()))
            self.wids['e_resultado'].set_text('')
            self.rellenar_pruebas()
        else:
            print "WARNING: Se ha intentano añadir una prueba con lote = None"
    
    def drop(self, w):
        model, itr = self.wids['tv_pruebas'].get_selection().get_selected()
        if itr != None and utils.dialogo(titulo = 'BORRAR PRUEBA', texto = '¿Está seguro?'):
            ide = model[itr][-1]
            prueba = pclases.PruebaRizo.get(ide)
            prueba.destroy(ventana = __file__)
            self.rellenar_pruebas()

    def set_lote(self, w):
        numlote = utils.dialogo_entrada(titulo = 'Nº LOTE', 
                                        texto = 'Introduzca número de lote:')
        if numlote != None:
            lotes = pclases.Lote.select(pclases.Lote.q.numlote.contains(numlote))
            if lotes.count() == 0:
                utils.dialogo_info(titulo = 'LOTE NO ENCONTRADO', 
                                   texto = 'No se encontró ningún lote %s.' % numlote)
                return
            elif lotes.count() > 1:
                filas = [(l.id, l.numlote, l.codigo, l.tenacidad, l.elongacion, l.rizo, l.encogimiento) for l in lotes]
                idlote = utils.dialogo_resultado(filas, 
                                                 titulo = 'SELECCIONE LOTE',
                                                 cabeceras = ('ID', 'Número', 'Código', 'Tenacidad', 'Elongación', 'Rizo', 'Encogimiento'))
                if idlote < 0:
                    return
                lote = pclases.Lote.get(idlote)
            else:
                lote = lotes[0]
            if len(lote.balas) == 0:
                utils.dialogo_info(titulo = 'LOTE VACÍO', 
                                   texto = 'El lote no contiene balas, no puede\nrealizar pruebas sobre un lote vacío.')
                self.lote = None
                return
            self.lote = lote
            self.actualizar_ventana()
    
    def rellenar_widgets(self):
        self.activar_widgets(self.lote != None)
        if self.lote != None:
            self.rellenar_info_lote()
            self.rellenar_pruebas()
            self.wids['e_fecha'].set_text(utils.str_fecha(time.localtime()))
            self.wids['e_resultado'].set_text('')

    def rellenar_info_lote(self):
        """
        PRECONDICIÓN: self.lote != None y len(self.lote.balas) > 0
        """
        lote = self.lote
        self.wids['e_codigo'].set_text("%d (%s)" % (lote.numlote, lote.codigo))
        self.wids['e_nombre'].set_text(lote.balas[0].articulos[0].productoVenta.nombre)
        self.wids['e_dtex'].set_text("%.1f" % lote.balas[0].articulos[0].productoVenta.camposEspecificosBala.dtex)
        self.wids['e_corte'].set_text(`lote.balas[0].articulos[0].productoVenta.camposEspecificosBala.corte`)
        self.wids['e_color'].set_text(lote.balas[0].articulos[0].productoVenta.camposEspecificosBala.color or '')
        self.wids['e_tenacidad'].set_text(lote.tenacidad or '')
        self.wids['e_elongacion'].set_text(lote.elongacion or '')
        self.wids['e_rizo'].set_text(lote.rizo or '')
        self.wids['e_encogimiento'].set_text(lote.encogimiento or '')

    def fecha(self, w):
        self.wids['e_fecha'].set_text(utils.str_fecha(utils.mostrar_calendario(fecha_defecto = self.objeto and self.objeto.fecha or None, padre = self.wids['ventana'])))

    def cambiar_fecha(self, cell, path, texto):
        model = self.wids['tv_pruebas'].get_model()
        prueba = pclases.PruebaRizo.get(model[path][-1])
        try:
            prueba.fecha = utils.parse_fecha(texto)
        except:
            utils.dialogo_info('FECHA INCORRECTA', 
                               'La fecha introducida (%s) no es correcta.' % texto)
        self.rellenar_pruebas()

    def cambiar_resultado(self, tv, path, texto):
        model = self.wids['tv_pruebas'].get_model()
        prueba = pclases.PruebaRizo.get(model[path][-1])
        try:
            prueba.resultado = float(texto)
        except:
            utils.dialogo_info('RESULTADO INCORRECTO',
                               'El número tecleado (%s) no es correcto.' % texto)
        self.rellenar_pruebas()

if __name__=='__main__':
    a = ResultadosRizo()

