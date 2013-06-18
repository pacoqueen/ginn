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
## resultados_titulo.py - Resultados de pruebas de título. 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 26 de abril de 2006 -> Inicio
## 
##
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk, time
from framework import pclases
from utils import _float as float


class ResultadosTitulo(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        Ventana.__init__(self, 'resultados_titulo.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_lote/clicked': self.set_lote,
                       'b_fecha/clicked': self.fecha,
                       'b_add/clicked': self.add,
                       'b_drop/clicked': self.drop,
                       'sp_tolerancia/value-changed': self.cambiar_tolerancia
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
                   'b_fecha',
                   'e_media',
                   'e_desvtipica',
                   'sp_tolerancia')
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
        pruebas = pclases.PruebaTitulo.select(pclases.PruebaTitulo.q.loteID == self.lote.id, orderBy="id")
        for prueba in pruebas:
            model.append((utils.str_fecha(prueba.fecha), prueba.resultado, prueba.id))
            
    def calcular_caracteristicas(self):
        """
        Calcula la media, desviación típica y marca los valores según tolerancia. 
        """
        lote = self.lote
        # La tolerancia depende del tipo de producto:
        try:
            dtex = lote.balas[0].articulos[0].productoVenta.camposEspecificosBala.dtex
        except:
            utils.dialogo_info(titulo = 'ERROR', 
                               texto = 'Ocurrió un error buscando el tipo de fibra.',
                               padre = self.wids['ventana'])
            return       
        mediatitulo = 0
        sumatorio = 0
        desvtipica = 0
        for p in lote.pruebasTitulo:
            mediatitulo += p.resultado
            sumatorio += p.resultado**2.0
        try:
            mediatitulo /= len(lote.pruebasTitulo)
            desvtipica = sumatorio / len(lote.pruebasTitulo)
            desvtipica -= mediatitulo**2.0
            desvtipica = desvtipica**0.5    # ValueError cuando intente hacer raíz de número negativo. No debería ocurrir.
        except ZeroDivisionError:
            mediatitulo = 0
            desvtipica = 0
        lote.mediatitulo = mediatitulo
        self.wids['e_desvtipica'].set_text("%.2f" % desvtipica)
        self.marcar_tolerancia(dtex, mediatitulo, lote.tolerancia)
        self.rellenar_info_lote()

    def marcar_tolerancia(self, dtex, mediatitulo, tolerancia):
        self.wids['ruler'].set_sensitive(False)
        diferencia = abs(mediatitulo-dtex)
        porcentaje = (diferencia*100)/dtex   # En formato 0 a 100 porque las posiciones del ruler son de -100 a 100
        if mediatitulo < dtex:
            porcentaje *= -1
        self.wids['ruler'].set_property('position', porcentaje)
        difmax = dtex*tolerancia
        if round(diferencia,2) > difmax:
            self.wids['e_media'].modify_base(gtk.STATE_NORMAL, self.wids['e_media'].get_colormap().alloc_color("red"))
        else:
            self.wids['e_media'].modify_base(gtk.STATE_NORMAL, self.wids['e_media'].get_colormap().alloc_color("green"))
        self.colorear(self.wids['tv_pruebas'], dtex, difmax)

    def colorear(self, tv, dtex, diferencia):
        """
        diferencia es la diferencia máxima en valor absoluto que debe 
        haber entre el resultado y el título del artículo.
        """
        def cell_func(col, cell, model, itr, (dtex, dif)):
            resultado = model[itr][1]
            if round(abs(resultado-dtex),2) > dif:
                color = "red"
            else:
                color = "green"
            cell.set_property("cell-background", color)
            cell.set_property("text", "%.2f" % model[itr][1])
        cols = tv.get_columns()
        col = cols[1]
        cells = col.get_cell_renderers()
        for cell in cells:
            col.set_cell_data_func(cell, cell_func, (dtex, diferencia))

    def actualizar_ventana(self):
        """
        Método que sobreescribe el "actualizar_ventana" que hereda de la clase ventana.
        PRECONDICION: self.lote no puede ser None
        """
        try:
            self.lote.sync()
            self.rellenar_widgets()
        except pclases.SQLObjectNotFound:
                utils.dialogo_info(titulo = 'REGISTRO ELIMINADO', 
                                   texto = 'El registro ha sido borrado desde otro puesto.',
                                   padre = self.wids['ventana'])
                self.lote = None
        self.activar_widgets(self.lote!=None)


    # --------------- Manejadores de eventos ----------------------------
    def add(self, w):
        if self.lote != None:
            fecha = self.wids['e_fecha'].get_text()
            if fecha == '':
                utils.dialogo_info(titulo = 'SIN FECHA',
                                   texto = 'Debe introducir la fecha del resultado de la prueba.',
                                   padre = self.wids['ventana'])
                return
            resultado = self.wids['e_resultado'].get_text()
            if resultado == '':
                utils.dialogo_info(titulo = 'SIN RESULTADO',
                                   texto = 'Debe introducir el resultado de la prueba.',
                                   padre = self.wids['ventana'])
                return
            try:
                prueba = pclases.PruebaTitulo(fecha = utils.parse_fecha(fecha),
                                                    resultado = resultado,
                                                    lote = self.lote)
                pclases.Auditoria.nuevo(prueba, self.usuario, __file__)
            except:
                utils.dialogo_info(titulo = 'ERROR', 
                                   texto = 'Verifique que ha introducido los datos correctamente.',
                                   padre = self.wids['ventana'])
            self.wids['e_fecha'].set_text(utils.str_fecha(time.localtime()))
            self.wids['e_resultado'].set_text('')
            self.rellenar_pruebas()
        else:
            print "WARNING: Se ha intentano añadir una prueba con lote = None"
    
    def drop(self, w):
        model, itr = self.wids['tv_pruebas'].get_selection().get_selected()
        if itr != None and utils.dialogo(titulo = 'BORRAR PRUEBA', 
                                          texto = '¿Está seguro?', 
                                          padre = self.wids['ventana']):
            ide = model[itr][-1]
            prueba = pclases.PruebaTitulo.get(ide)
            prueba.destroy(ventana = __file__)
            self.rellenar_pruebas()

    def set_lote(self, w):
        numlote = utils.dialogo_entrada(titulo = 'Nº LOTE', 
                                        texto = 'Introduzca número de lote:',
                                        padre = self.wids['ventana'])
        if numlote != None:
            lotes = pclases.Lote.select(pclases.Lote.q.numlote.contains(numlote))
            if lotes.count() == 0:
                utils.dialogo_info(titulo = 'LOTE NO ENCONTRADO', 
                                   texto = 'No se encontró ningún lote %s.' % numlote,
                                   padre = self.wids['ventana'])
                return
            elif lotes.count() > 1:
                filas = [(l.id, l.numlote, l.codigo, l.tenacidad, l.elongacion, l.rizo, l.encogimiento) for l in lotes]
                idlote = utils.dialogo_resultado(filas, 
                                                 titulo = 'SELECCIONE LOTE',
                                                 cabeceras = ('ID', 'Número', 'Código', 'Tenacidad', 'Elongación', 'Rizo', 'Encogimiento'),
                                                 padre = self.wids['ventana'])
                if idlote < 0:
                    return
                lote = pclases.Lote.get(idlote)
            else:
                lote = lotes[0]
            if len(lote.balas) == 0:
                utils.dialogo_info(titulo = 'LOTE VACÍO', 
                                   texto = 'El lote no contiene balas, no puede\nrealizar pruebas sobre un lote vacío.',
                                   padre = self.wids['ventana'])
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
        self.wids['e_media'].set_text("%.2f" % lote.mediatitulo or 0)
        try:
            self.wids['sp_tolerancia'].set_value(lote.tolerancia*100.0)
        except:
            self.wids['sp_tolerancia'].set_value(20)
            lote.tolerancia = 0.2

    def fecha(self, w):
        self.wids['e_fecha'].set_text(utils.str_fecha(utils.mostrar_calendario(fecha_defecto = self.objeto and self.objeto.fecha or None, padre = self.wids['ventana'])))

    def cambiar_fecha(self, cell, path, texto):
        model = self.wids['tv_pruebas'].get_model()
        prueba = pclases.PruebaTitulo.get(model[path][-1])
        try:
            prueba.fecha = utils.parse_fecha(texto)
        except:
            utils.dialogo_info('FECHA INCORRECTA', 
                               'La fecha introducida (%s) no es correcta.' % texto,
                               padre = self.wids['ventana'])
        self.rellenar_pruebas()

    def cambiar_resultado(self, tv, path, texto):
        model = self.wids['tv_pruebas'].get_model()
        prueba = pclases.PruebaTitulo.get(model[path][-1])
        try:
            prueba.resultado = float(texto)
        except:
            utils.dialogo_info('RESULTADO INCORRECTO',
                               'El número tecleado (%s) no es correcto.' % texto,
                               padre = self.wids['ventana'])
        self.rellenar_pruebas()

    def cambiar_tolerancia(self, sp):
        lote = self.lote
        try:
            lote.tolerancia = float(sp.get_value() / 100)
            self.calcular_caracteristicas()
        except ValueError:
            utils.dialogo_info(titulo = 'VALOR INCORRECTO', 
                               texto = 'El valor %s no es correcto.' % sp.get_value(),
                               padre = self.wids['ventana'])

if __name__=='__main__':
    a = ResultadosTitulo()

