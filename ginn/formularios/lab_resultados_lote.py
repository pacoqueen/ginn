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
## rollos_almacen.py - Muestra historial de rollos almacenados. 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 06 de febrero de 2006 -> Inicio
## 
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, time
from framework import pclases
from informes import geninformes
from utils import _float as float


class LabResultadosLote(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        Ventana.__init__(self, 'lab_resultados_lote.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_lote/clicked': self.lote,
                       'b_add_elongacion/clicked': self.add_elongacion,
                       'b_drop_elongacion/clicked': self.drop_elongacion,
                       'b_add_tenacidad/clicked': self.add_tenacidad,
                       'b_drop_tenacidad/clicked': self.drop_tenacidad,
                       'b_add_encogimiento/clicked': self.add_encogimiento,
                       'b_drop_encogimiento/clicked': self.drop_encogimiento,
                       'b_calcular/clicked': self.calcular
                      }
        self.add_connections(connections)
        self.ws = ['e_rizo_entrada','b_add_elongacion','b_drop_elongacion','b_add_tenacidad','b_drop_tenacidad','b_add_encogimiento','b_drop_encogimiento','b_calcular']
        self.activar_widgets(self.ws,False)
        self.inicializar_ventana()
        self.lote = None
        self.rizo = []
        self.tenacidad = []
        self.elongacion = []
        self.encogimiento = []
        gtk.main()

    # --------------- Funciones auxiliares ------------------------------
    def activar_widgets(self, ws, valor):
        for i in ws:
            self.wids[i].set_sensitive(valor)
    
    def es_diferente(self):
        # No hace falta en esta ventana.
        return False

    def aviso_actualizacion(self):
        # No hace falta en esta ventana.
        return False

    def ir_a_primero(self):
        # No hace falta en esta ventana.
        pass

    def crear_listview(self, tv):
        # Primero hay que crear el TreeView que mostrará 
        # el contenido de cada solapa.
        cols = (('Resultado', 'gobject.TYPE_FLOAT', False, True,  False, None), 
                ('ID',        'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(tv, cols)
        return tv

    def inicializar_ventana(self):
        """
        Inicializa los widgets de la ventana.
        """
        self.crear_listview(self.wids['tv_elongacion'])
        self.crear_listview(self.wids['tv_tenacidad'])
        self.crear_listview(self.wids['tv_encogimiento'])

    def rellenar_tablas(self):
        """
        Actualiza los valores de cada sección del formulario
        """
        model = self.wids['tv_elongacion'].get_model()
        model.clear()
        for i in self.elongacion:
            model.append((i[0],i[1]))
        model = self.wids['tv_tenacidad'].get_model()
        model.clear()
        for i in self.tenacidad:
            model.append((i[0],i[1]))
        model = self.wids['tv_encogimiento'].get_model()
        model.clear()
        for i in self.encogimiento:
            model.append((i[0],i[1]))
            
    
    def lote(self, w):
        """
        Carga los datos actuales de un lote
        """
        numero = utils.dialogo_entrada(titulo = 'NÚMERO DE LOTE',texto = 'Introduzca el número de lote', padre = self.wids['ventana'])
        try:
            lote = pclases.Lote.select(pclases.Lote.q.numlote == numero)[0]
        except:
            utils.dialogo_info(titulo = 'ERROR', texto = 'No hay registrado ningún lote con ese número', padre = self.wids['ventana'])
            return
        self.lote = lote
        self.activar_widgets(self.ws,True)
        self.wids['e_numlote'].set_text(str(lote.numlote)+'    Código: '+lote.codigo)
        self.wids['e_tenacidad'].set_text(lote.tenacidad)
        self.wids['e_elongacion'].set_text(lote.elongacion)
        self.wids['e_rizo'].set_text(lote.rizo)
        self.wids['e_rizo_entrada'].set_text(lote.rizo)
        self.wids['e_encogimiento'].set_text(lote.encogimiento)
            

    def add_tenacidad(self, w):
        """
        Añade un valor de tenacidad a la lista
        """
        tenacidad = utils.dialogo_entrada(titulo = 'VALOR DE TENACIDAD', texto = 'Introduzca el valor')
        try:
            tenacidad = tenacidad.replace(',','.')
            tenacidad = float(tenacidad)
        except:
            utils.dialogo_info(titulo = 'ERROR', texto = tenacidad + ' no es un valor numérico válido')
            return
        # El valor que se mete en la lista ya es un float
        self.tenacidad.append((tenacidad,len(self.tenacidad)))        
        self.rellenar_tablas()

    def drop_tenacidad(self, w):
        """
        Elimina un valor de tenacidad de la lista
        """
        model, itr = self.wids['tv_tenacidad'].get_selection().get_selected()
        if itr != None:
            dato, ide = model[itr]
            self.tenacidad.remove((dato,ide))
            self.rellenar_tablas()
        else:
            utils.dialogo_info(titulo = 'ERROR', texto = 'No se ha seleccionado ningún elemento a borrar')
            return 

    def add_elongacion(self, w):
        """
        Añade un valor de elongacion a la lista
        """
        elongacion = utils.dialogo_entrada(titulo = 'VALOR DE ELONGACIÓN', texto = 'Introduzca el valor')
        try:
            elongacion = elongacion.replace(',','.')
            elongacion = float(elongacion)
        except:
            utils.dialogo_info(titulo = 'ERROR', texto = elongacion + ' no es un valor numérico válido')
            return
        # El valor que se mete en la lista ya es un float
        self.elongacion.append((elongacion,len(self.elongacion)))        
        self.rellenar_tablas()

    def drop_elongacion(self, w):
        """
        Elimina un valor de elongacion de la lista
        """
        model, itr = self.wids['tv_elongacion'].get_selection().get_selected()
        if itr != None:
            dato, ide = model[itr]
            self.elongacion.remove((dato, ide))
            self.rellenar_tablas()
        else:
            utils.dialogo_info(titulo = 'ERROR', texto = 'No se ha seleccionado ningún elemento a borrar')
            return 

    def add_encogimiento(self, w):
        """
        Añade un valor de encogimiento a la lista
        """
        encogimiento = utils.dialogo_entrada(titulo = 'VALOR DE ENCOGIMIENTO', texto = 'Introduzca el valor')
        try:
            encogimiento = encogimiento.replace(',','.')
            encogimiento = float(encogimiento)
        except:
            utils.dialogo_info(titulo = 'ERROR', texto = encogimiento + ' no es un valor numérico válido')
            return
        # El valor que se mete en la lista ya es un float
        self.encogimiento.append((encogimiento,len(self.encogimiento)))        
        self.rellenar_tablas()

    def drop_encogimiento(self, w):
        """
        Elimina un valor de encogimiento de la lista
        """
        model, iter = self.wids['tv_encogimiento'].get_selection().get_selected()
        if iter != None:
            dato, ide = model[iter]
            self.encogimiento.remove((dato,id))
            self.rellenar_tablas()
        else:
            utils.dialogo_info(titulo = 'ERROR', texto = 'No se ha seleccionado ningún elemento a borrar')
            return 

    def calcular(self, w):
        """
        Calcula la media de los valores de rizo, tenacidad, encogimiento y elongación
        """
        lote = self.lote
         # La elongación depende del tipo de producto:
        try:
            dtex = lote.balas[0].articulos[0].productoVenta.camposEspecificosBala.dtex
        except:
            utils.dialogo_info(titulo = 'ERROR', texto = 'Ocurrió un error buscando el tipo de fibra')
            return       
            
        mediaTenacidad = 0
        for i in self.tenacidad:
            mediaTenacidad += i[0]
        if len(self.tenacidad) != 0:
            mediaTenacidad /= len(self.tenacidad)
            # Tenacidad: Alta(>=50), otra normal
            if mediaTenacidad >= 50:
                lote.tenacidad = 'A'
            else:
                lote.tenacidad = 'N'
        

        mediaElongacion = 0
        for i in self.elongacion:
            mediaElongacion += i[0]
        if len(self.elongacion) != 0:
            mediaElongacion /= len(self.elongacion)
            # Elongación A(>90), B(70-90), C(<70)
            if dtex == 3.3: 
                if (mediaElongacion >= 40 and mediaElongacion <= 70):
                    lote.elongacion = 'A'
                else:
                    lote.elongacion = 'N'
            elif dtex == 4.4: 
                if (mediaElongacion >= 50 and mediaElongacion <= 80):
                    lote.elongacion = 'A'
                else:
                    lote.elongacion = 'N'
            elif dtex == 6.7: 
                if (mediaElongacion >=60 and mediaElongacion <= 90):
                    lote.elongacion = 'A'
                else:
                    lote.elongacion = 'N'
            elif dtex == 8.9: 
                if (mediaElongacion >=70 and mediaElongacion <= 100):
                    lote.elongacion = 'A'
                else:
                    lote.elongacion = 'N'   
            else:
                lote.elongacion = '?'
       
        # Rizo
        if self.wids['e_rizo_entrada'].get_text() != '':
            lote.rizo = self.wids['e_rizo_entrada'].get_text()
        
        # Encogimiento
        mediaEncogimiento = 0 
        for i in self.encogimiento:
            mediaEncogimiento += i[0]
        if len(self.encogimiento) != 0:
            mediaEncogimiento /= len(self.encogimiento)
            if mediaEncogimiento <= 10:
                lote.encogimiento = 'B'
            elif (mediaEncogimiento >10 and mediaEncogimiento<=15):
                lote.encogimiento = 'N'
            elif mediaEncogimiento > 15:
                lote.encogimiento = 'A'
            else:
                lote.encogimiento = '?'
          
        if lote.tenacidad!=None:
            self.wids['e_tenacidad'].set_text(lote.tenacidad)
        else:            
            self.wids['e_tenacidad'].set_text('')
        if lote.elongacion != None:
            self.wids['e_elongacion'].set_text(lote.elongacion)
        else:
            self.wids['e_elongacion'].set_text('')
        if lote.rizo != None:
            self.wids['e_rizo'].set_text(lote.rizo)
            self.wids['e_rizo_entrada'].set_text(lote.rizo)
        else:
            self.wids['e_rizo'].set_text('')
        if lote.encogimiento != None:
            self.wids['e_encogimiento'].set_text(lote.encogimiento)
        else:
            self.wids['e_encogimiento'].set_text('')

    # --------------- Manejadores de eventos ----------------------------


if __name__=='__main__':
    a = LabResultadosLote()

