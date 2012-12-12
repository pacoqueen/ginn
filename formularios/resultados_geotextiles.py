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
## resultados_geotextiles.py - Resultados de pruebas sobre rollos. 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 18 de mayo de 2006 -> Inicio
## 19 de mayo de 2006 -> Testing
## 23 de julio de 2007 -> Pruebas de porometría con 3 decimales.
##
###################################################################
## DONE:
## PLAN: No estaría mal mostrar valores estadísticos como la media
##       y la desviación típica de las pruebas.
## + DONE: CBR: No coge dos decimales hasta que se teclea por 2ª vez.
###################################################################
## FIXME: Al salir con el evento destroy (bolaspa) pregunta dos 
##      veces si quiere salir y la segunda vez ignora la respuesta.
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
from utils import _float as float
from resultados_fibra import comprobar_y_preguntar_si_guardar

class ResultadosGeotextiles(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'resultados_geotextiles.glade', objeto)
        connections = {'b_salir/clicked': self._salir,
                       'b_partida/clicked': self.set_partida,
                       'b_add/clicked': self.add,
                       'b_drop/clicked': self.drop, 
                       'b_guardar_obs/clicked': self.guardar_obs, 
                       'b_rollos/clicked': self.buscar_rollos, 
                       'b_marcado/clicked': self.comparar_con_marcado, 
                       'b_imprimir/clicked': self.imprimir, 
                       'ventana/delete_event': self._salir
                      }
        self.add_connections(connections)
        self.activar_widgets(False)
        self.inicializar_ventana()
        if objeto == None:
            self.partida = None
        else:
            self.partida = objeto
            self.actualizar_ventana()
        gtk.main()

    def _salir(self, *args, **kw):
        """
        Si hay cambios pendientes en observaciones, pregunta.
        Después llama a la función salir heredada.
        """
        comprobar_y_preguntar_si_guardar(self)
        self.salir(*args, **kw)

    # --------------- Funciones auxiliares ------------------------------
    def activar_widgets(self, valor):
        self.ws = ('e_nombre', 'e_numpartida', 'tv_lotes', 'vbox2', 'vbox3', 
                   'frame4', 'txt_observaciones', 'b_rollos', 'b_marcado', 
                   'tv_muestras')
        for i in self.ws:
            self.wids[i].set_sensitive(valor)
        if self.usuario:
            try:
                ventana = pclases.Ventana.select(pclases.Ventana.q.fichero == "resultados_geotextiles.py")[0]     # OJO: HARCODED
            except IndexError:
                txt = "resultados_fibra::activar_widgets -> Ventana no encontrada en BD."
                self.logger.error(txt)
                print txt
            else:
                permiso = self.usuario.get_permiso(ventana)
                if not permiso.escritura and self.usuario.nivel > 1:
                    self.wids['tv_pruebas'].set_sensitive(False)
                    self.wids['txt_observaciones'].set_sensitive(False)
                if not permiso.nuevo and self.usuario.nivel > 1:
                    self.wids['b_add'].set_sensitive(False)
 
    ## XXX Comparar con Marcado CE ############################################
    def comparar_con_marcado(self, boton):
        """
        Abre una nueva ventana con la comparación entre 
        los valores de la partida y los indicados por el 
        marcado CE para el producto de la misma.
        """
        dic_pruebas = build_dic_pruebas()
        widgets = self.build_ventana_marcado(dic_pruebas)
        self.introducir_info_marcado(widgets, dic_pruebas)
        widgets['ventana_marcado'].show_all()
    
    def build_ventana_marcado(self, dic):
        """
        Devuelve un diccionario de widgets con las pruebas de "dic" en ella.
        Para cada prueba crea un label para el valor de la prueba, un entry 
        para el valor de la partida, otro para el valor óptimo y otros dos para 
        las tolerancias del marcado. El orden de los mismos dentro del 
        contenedor horizontal vendrá determinado por el tipo de prueba de 
        manera que los valores del rango siempre estén en orden.
        Los entries llevan como nombre en el diccionario 
        "e_%s" % (valor, nombrePrueba...).
        El gtk.Window es widgets['ventana_marcado']
        """
        widgets = {}
        widgets['ventana_marcado'] = gtk.Window()
        widgets['ventana_marcado'].set_transient_for(self.wids['ventana'])
        widgets['ventana_marcado'].set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        widgets['ventana_marcado'].set_modal(True)
        widgets['ventana_marcado'].set_title("Marcado CE")
        widgets['tabla'] = gtk.Table(rows = len(dic) + 1, columns = 5)
        widgets['ventana_marcado'].add(widgets['tabla'])
        lprueba = gtk.Label("<i>Prueba</i>")
        lprueba.set_use_markup(True)
        widgets['tabla'].attach(lprueba, 0, 1, 0, 1)
        lvalor = gtk.Label("<i>Valor (diferencia)</i>")
        lvalor.set_use_markup(True) 
        widgets['tabla'].attach(lvalor, 1, 2, 0, 1)
        lestandar = gtk.Label("<i>Estándar y tolerancias</i>")
        lestandar.set_use_markup(True)
        widgets['tabla'].attach(lestandar, 2, 5, 0, 1)
        y = 1
        for nombreprueba in dic:
            self.build_container_prueba(nombreprueba, 
                                        dic[nombreprueba], widgets, y)
            y += 1
        return widgets

    def build_container_prueba(self, nombreprueba, atribprueba, widgets, y):
        """
        Introduce en el diccionario de widgets, dentro de la tabla, 
        un label y varios entries de acuerdo al tipo de prueba.
        "y" es el ordinal superior del borde de la fila.
        """
        if self.partida != None:
            producto = self.partida.get_producto()
            if producto != None:
                tabla = widgets['tabla']
                cer = producto.camposEspecificosRollo
                label = gtk.Label("%s: " % nombreprueba)
                widgets['l_%s' % (atribprueba)] = label
                tabla.attach(label, 0, 1, y, y+1)
                evalor = gtk.Entry()
                evalor.set_property("editable", False)
                evalor.set_property("has-frame", False)
                evalor.set_property("xalign", 0.5)
                widgets['e_valor%s' % (atribprueba)] = evalor
                tabla.attach(evalor, 1, 2, y, y+1)
                einf = gtk.Entry()
                einf.set_property("editable", False)
                einf.set_property("has-frame", False)
                einf.set_property("xalign", 0.5)
                widgets['e_inf%s' % (atribprueba)] = einf
                esup = gtk.Entry()
                esup.set_property("editable", False)
                esup.set_property("has-frame", False)
                esup.set_property("xalign", 0.5)
                widgets['e_sup%s' % (atribprueba)] = esup
                eopt = gtk.Entry()
                eopt.set_property("editable", False)
                eopt.set_property("has-frame", False)
                eopt.set_property("xalign", 0.5)
                widgets['e_opt%s' % (atribprueba)] = eopt
                inf = getattr(cer, "valorPrueba%sInf" % (atribprueba))
                sup = getattr(cer, "valorPrueba%sSup" % (atribprueba))
                opt = getattr(cer, "estandarPrueba%s" % (atribprueba))
                if inf <= opt <= sup:
                    tabla.attach(einf, 2, 3, y, y+1)
                    tabla.attach(eopt, 3, 4, y, y+1)
                    tabla.attach(esup, 4, 5, y, y+1)
                    einf.modify_text(gtk.STATE_NORMAL, 
                                     einf.get_colormap().alloc_color("red"))
                    eopt.modify_text(gtk.STATE_NORMAL, 
                                     eopt.get_colormap().alloc_color("black"))
                    esup.modify_text(gtk.STATE_NORMAL, 
                                     esup.get_colormap().alloc_color("red"))
                elif opt <= inf <= sup:
                    tabla.attach(eopt, 2, 3, y, y+1)
                    tabla.attach(einf, 3, 4, y, y+1)
                    tabla.attach(esup, 4, 5, y, y+1)
                    einf.modify_text(gtk.STATE_NORMAL, 
                                     einf.get_colormap().alloc_color("green"))
                    eopt.modify_text(gtk.STATE_NORMAL, 
                                     eopt.get_colormap().alloc_color("black"))
                    esup.modify_text(gtk.STATE_NORMAL, 
                                     esup.get_colormap().alloc_color("red"))
                else:
                    tabla.attach(einf, 2, 3, y, y+1)
                    tabla.attach(esup, 3, 4, y, y+1)
                    tabla.attach(eopt, 4, 5, y, y+1)
                    einf.modify_text(gtk.STATE_NORMAL, 
                                     einf.get_colormap().alloc_color("red"))
                    eopt.modify_text(gtk.STATE_NORMAL, 
                                     eopt.get_colormap().alloc_color("black"))
                    esup.modify_text(gtk.STATE_NORMAL, 
                                     esup.get_colormap().alloc_color("green"))

    def introducir_info_marcado(self, widgets, dic_pruebas):
        """
        Introduce el valor de la partida y los valores de las pruebas en 
        los widgets correspondientes. Se encarga también de poner en negrita 
        el entry del valor y colorearlo según satisfaga el marcado.
        Los valores del marcado también los colorea. Si el rango del marcado 
        tiene los valores inferior y superior por debajo del estándar, colorea 
        en verde la tolerancia más cercana al estándar y en rojo la otra. Si 
        el estándar se encuentra entre ambos valores, colorea en rojo las dos 
        tolerancias.
        """
        if self.partida != None:
            producto = self.partida.get_producto()
            if producto != None:
                fpar = self.partida.get_fecha_fabricacion()
                if fpar:
                    cer = producto.camposEspecificosRollo.buscar_marcado(fpar)
                else:
                    cer = None
                if cer == None:
                    cer = producto.camposEspecificosRollo
                for nombreprueba in dic_pruebas:
                    atribprueba = dic_pruebas[nombreprueba]
                    dif, evaluacion = self.partida.comparar_con_marcado(
                                        atribprueba, fpar)
                    valor_opt = getattr(cer, "estandarPrueba%s" % atribprueba)
                    valor_inf = getattr(cer, "valorPrueba%sInf" % atribprueba)
                    valor_sup = getattr(cer, "valorPrueba%sSup" % atribprueba)
                    evalor = widgets["e_valor%s" % (atribprueba)]
                    if evaluacion >= 0:
                        evalor.set_text("%s (%s)" % (
                            utils.float2str(dif + valor_opt), 
                            utils.float2str(dif, 3, True)))
                    else:
                        evalor.set_text("%s" % (
                            utils.float2str(dif + valor_opt)))
                    widgets["e_inf%s" % (atribprueba)].set_text(
                        utils.float2str(valor_inf, 3, True))
                    widgets["e_sup%s" % (atribprueba)].set_text(
                        utils.float2str(valor_sup, 3, True))
                    widgets["e_opt%s" % (atribprueba)].set_text(
                        utils.float2str(valor_opt, 3, True))
                    if evaluacion == 0:
                        color = "white"
                    elif evaluacion == -1:
                        color = "gray99"
                    elif evaluacion == 1:
                        color = "green"
                    elif evaluacion == 2:
                        color = "orange red"
                    elif evaluacion == 3:
                        color = "red"
                    else:
                        color = "gray"
                    evalor.modify_base(gtk.STATE_NORMAL, 
                        evalor.get_colormap().alloc_color(color))
    
    ## XXX End of Comparar con Marcado CE #####################################
    
    def buscar_rollos(self, boton):
        """
        Busca los rollos de la partida actual a los que se les ha extraído 
        muestra.
        """
        if self.partida != None:
            rollos = [r for r in self.partida.rollos 
                      if r.muestra or "muestra" in r.observaciones.lower()]
            if rollos == []:
                utils.dialogo_info(titulo = "NO SE ENCONTRARON ROLLOS", 
                    texto = "No se econtraron muestras de rollos en los "
                            "partes implicados.", 
                    padre = self.wids['ventana'])
            else:
                filas = [(r.id, r.codigo, r.observaciones, 
                          "%s %s" % (utils.str_fecha(r.fechahora), 
                          utils.str_hora(r.fechahora))
                         ) 
                         for r in rollos]
                idrollo = utils.dialogo_resultado(filas, 
                    titulo = 'ROLLOS CON MUESTRA EN LA PARTIDA %s' % (
                                self.partida.codigo),
                    cabeceras = ('ID', 'Código', 'Observaciones', 
                                 'Fecha y hora de fabricación'), 
                    padre = self.wids['ventana'])
                if idrollo != None and idrollo > 0:
                    rollo = pclases.Rollo.get(idrollo)
                    import trazabilidad_articulos
                    trazabilidad_articulos.TrazabilidadArticulos(
                        usuario = self.usuario, objeto = rollo)


    def crear_listview(self, tv):
        cols = (('Fecha', 'gobject.TYPE_STRING', 
                    True, True, True, self.cambiar_fecha),
                ('Gramaje\n(gr/m²)', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_gramaje), 
                ('Resistencia\nlongitudinal (kN/m)', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_r_longitudinal), 
                ('Alargamiento\nlongitudinal (%)', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_a_longitudinal), 
                ('Resistencia\ntransversal (kN/m)', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_r_transversal), 
                ('Alargamiento\ntransversal (%)', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_a_transversal), 
                ('CBR (kN)', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_compresion), 
                ('Cono', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_perforacion), 
                ('Espesor\n(mm)', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_espesor), 
                ('Permeabilidad\n(l/m²/s)', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_permeabilidad), 
                ('Porometría\n(mm)', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_porometria), 
                ('Punzonamiento\npiramidal (kN)', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_piramidal), 
                ('ID', 'gobject.TYPE_STRING', False, False, False, None)) 
                    # Contiene los ID de los resultados separados por ','
        utils.preparar_listview(tv, cols)
        tv.get_column(1).get_cell_renderers()[0].set_property('xalign', 0.1) 
        tv.get_column(2).get_cell_renderers()[0].set_property('xalign', 0.1) 
        tv.get_column(3).get_cell_renderers()[0].set_property('xalign', 0.1) 
        tv.get_column(4).get_cell_renderers()[0].set_property('xalign', 0.1) 
        tv.get_column(5).get_cell_renderers()[0].set_property('xalign', 0.1) 
        tv.get_column(6).get_cell_renderers()[0].set_property('xalign', 0.1) 
        tv.get_column(7).get_cell_renderers()[0].set_property('xalign', 0.1) 
        tv.get_column(8).get_cell_renderers()[0].set_property('xalign', 0.1) 
        tv.get_column(9).get_cell_renderers()[0].set_property('xalign', 0.1) 
        tv.get_column(10).get_cell_renderers()[0].set_property('xalign', 0.1) 
        tv.get_column(11).get_cell_renderers()[0].set_property('xalign', 0.1) 

    def crear_treeview(self, tv):
        cols = (('Lote y materia prima consumida', 'gobject.TYPE_STRING', 
                    False, True, True, None),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_treeview(tv, cols)
    
    def crear_treeview_muestras(self, tv):
        cols = (('Código', 'gobject.TYPE_STRING', False, True, True, None),
                ('Observaciones', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Pendiente', 'gobject.TYPE_BOOLEAN', 
                    False, True, False, None),
                ('Envío', 'gobject.TYPE_STRING', False, True, False, None),
                ('Recepción', 'gobject.TYPE_STRING', False, True, False, None),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(tv, cols)

    def inicializar_ventana(self):
        """
        Inicializa los widgets de la ventana.
        """
        self.crear_listview(self.wids['tv_pruebas'])
        self.crear_treeview(self.wids['tv_lotes'])
        self.crear_treeview_muestras(self.wids['tv_muestras'])
        self.wids['txt_observaciones'].get_buffer().connect("changed", 
            lambda txtbuffer: self.wids['b_guardar_obs'].set_sensitive(True))

    def func_sort(self, t1, t2):
        if t1[0] < t2[0]:
            return -1
        elif t1[0] > t2[0]:
            return 1
        else:
            return 0

    def preparar_pruebas(self):
        """
        Devuelve una lista de listas que contiene las pruebas ordenadas del 
        partida por fecha de la forma: 
            [(fecha, prueba título, ..., "id0,id1,...id5")]
        """
        res = []
        for p in self.partida.pruebasGramaje:
            res.append([p.fecha, p.resultado, None, None, None, None, None, 
                        None, None, None, None, None, 
                        [p.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                       ])
        for p in self.partida.pruebasResistenciaLongitudinal:
            puesto = False
            for fila in res:
                if p.fecha == fila[0] and fila[2] == None: 
                        # Hay hueco en la fecha
                    fila[2] = p.resultado
                    fila[-1][1] = p.id
                    puesto = True
                    break
            if not puesto:
                res.append([p.fecha, None, p.resultado, None, None, None, 
                            None, None, None, None, None, None, 
                            [0, p.id, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                           ])
        for p in self.partida.pruebasAlargamientoLongitudinal:
            puesto = False
            for fila in res:
                if p.fecha == fila[0] and fila[3] == None:  
                        # Hay hueco en la fecha
                    fila[3] = p.resultado
                    fila[-1][2] = p.id
                    puesto = True
                    break
            if not puesto:
                res.append([p.fecha, None, None, p.resultado, None, None, 
                            None, None, None, None, None, None, 
                            [0, 0, p.id, 0, 0, 0, 0, 0, 0, 0, 0]
                           ])
        for p in self.partida.pruebasResistenciaTransversal:
            puesto = False
            for fila in res:
                if p.fecha == fila[0] and fila[4] == None:  
                        # Hay hueco en la fecha
                    fila[4] = p.resultado
                    fila[-1][3] = p.id
                    puesto = True
                    break
            if not puesto:
                res.append([p.fecha, None, None, None, p.resultado, None, 
                            None, None, None, None, None, None, 
                            [0, 0, 0, p.id, 0, 0, 0, 0, 0, 0, 0]
                           ])
        for p in self.partida.pruebasAlargamientoTransversal:
            puesto = False
            for fila in res:
                if p.fecha == fila[0] and fila[5] == None:  
                        # Hay hueco en la fecha
                    fila[5] = p.resultado
                    fila[-1][4] = p.id
                    puesto = True
                    break
            if not puesto:
                res.append([p.fecha, None, None, None, None, p.resultado, 
                            None, None, None, None, None, None, 
                            [0, 0, 0, 0, p.id, 0, 0, 0, 0, 0, 0]
                           ])
        for p in self.partida.pruebasCompresion:
            puesto = False
            for fila in res:
                if p.fecha == fila[0] and fila[6] == None:  
                        # Hay hueco en la fecha
                    fila[6] = p.resultado
                    fila[-1][5] = p.id
                    puesto = True
                    break
            if not puesto:
                res.append([p.fecha, None, None, None, None, None, 
                            p.resultado, None, None, None, None, None, 
                            [0, 0, 0, 0, 0, p.id, 0, 0, 0, 0, 0]
                           ])
        for p in self.partida.pruebasPerforacion:
            puesto = False
            for fila in res:
                if p.fecha == fila[0] and fila[7] == None:  
                        # Hay hueco en la fecha
                    fila[7] = p.resultado
                    fila[-1][6] = p.id
                    puesto = True
                    break
            if not puesto:
                res.append([p.fecha, None, None, None, None, None, None, 
                            p.resultado, None, None, None, None, 
                            [0, 0, 0, 0, 0, 0, p.id, 0, 0, 0, 0]
                           ])
        for p in self.partida.pruebasEspesor:
            puesto = False
            for fila in res:
                if p.fecha == fila[0] and fila[8] == None:  
                        # Hay hueco en la fecha
                    fila[8] = p.resultado
                    fila[-1][7] = p.id
                    puesto = True
                    break
            if not puesto:
                res.append([p.fecha, None, None, None, None, None, None, None, 
                            p.resultado, None, None, None, 
                            [0, 0, 0, 0, 0, 0, 0, p.id, 0, 0, 0]
                           ])
        for p in self.partida.pruebasPermeabilidad:
            puesto = False
            for fila in res:
                if p.fecha == fila[0] and fila[9] == None:  
                        # Hay hueco en la fecha
                    fila[9] = p.resultado
                    fila[-1][8] = p.id
                    puesto = True
                    break
            if not puesto:
                res.append([p.fecha, None, None, None, None, None, None, None, 
                            None, p.resultado, None, None, 
                            [0, 0, 0, 0, 0, 0, 0, 0, p.id, 0, 0]
                           ])
        for p in self.partida.pruebasPoros:
            puesto = False
            for fila in res:
                if p.fecha == fila[0] and fila[10] == None:  
                        # Hay hueco en la fecha
                    fila[10] = p.resultado
                    fila[-1][9] = p.id
                    puesto = True
                    break
            if not puesto:
                res.append([p.fecha, None, None, None, None, None, None, None, 
                            None, None, p.resultado, None, 
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, p.id, 0]])
        for p in self.partida.pruebasPiramidal:
            puesto = False
            for fila in res:
                if p.fecha == fila[0] and fila[11] == None:  
                        # Hay hueco en la fecha
                    fila[11] = p.resultado
                    fila[-1][10] = p.id
                    puesto = True
                    break
            if not puesto:
                res.append([p.fecha, None, None, None, None, None, None, None, 
                            None, None, None, p.resultado, 
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, p.id]])
        res.sort(self.func_sort)
        res = [(utils.str_fecha(f[0]), 
                f[1] and "%.2f" % f[1] or "", 
                f[2] and "%.2f" % f[2] or "", 
                f[3] and "%.2f" % f[3] or "", 
                f[4] and "%.2f" % f[4] or "", 
                f[5] and "%.2f" % f[5] or "", 
                f[6] and "%.2f" % f[6] or "", 
                f[7] and "%.2f" % f[7] or "", 
                f[8] and "%.2f" % f[8] or "", 
                f[9] and "%.2f" % f[9] or "", 
                f[10] and "%.3f" % f[10] or "", 
                f[11] and "%.2f" % f[11] or "", 
                ','.join(map(str, f[12]))
               ) for f in res]
        return res

    def rellenar_pruebas(self):
        """
        Introduce en el treeview las pruebas del partida seleccionado y 
        recalcula la característica del partida.
        """
        model = self.wids['tv_pruebas'].get_model()
        model.clear()
        self.calcular_caracteristicas()
        pruebas = self.preparar_pruebas()
        for prueba in pruebas:
            model.append(prueba)

    def rellenar_lotes(self):
        model = self.wids['tv_lotes'].get_model()
        model.clear()
        partida = self.partida
        lotes = []
        prods = []
        for b in partida.balas:
            if b.lote not in lotes:
                lotes.append(b.lote)
                try:
                    titulo = "%.1f" % (
                      b.articulos[0].productoVenta.camposEspecificosBala.dtex)
                except:
                    titulo = "ERROR"
                try:
                    corte = "%d" % (
                      b.articulos[0].productoVenta.camposEspecificosBala.corte)
                except:
                    corte = "ERROR"
                infolote = "Lote: %s - Título: %s - Corte: %s" \
                            % (b.lote.numlote, 
                               titulo, 
                               corte)
                # infolote = "Lote: %s - Título: %.2f - Tenacidad: %s - Elongación: %s - Rizo: %s - Encogimiento: %s - Grasa: %s" \
                #                 % (b.lote.numlote, 
                #                    b.lote.mediatitulo, 
                #                    b.lote.tenacidad, 
                #                    b.lote.elongacion, 
                #                    b.lote.rizo, 
                #                    b.lote.encogimiento, 
                #                    b.lote.grasa)
                iter = model.append(None, (infolote, b.lote.id))
            # Esto tenía sentido cuando el consumo de balas se asociaba a un parte y no a una partida completa.
            #for a in b.articulos:
            #    if a.parteDeProduccion != None:
            #        for c in a.parteDeProduccion.consumos:
            #            if c.productoCompra not in prods:
            #                prods.append(c.productoCompra)
            #                model.append(iter, (c.productoCompra.descripcion, c.id))

    def calcular_caracteristicas(self):
        """
        Calcula las características en función de los valores de las pruebas.
        """
        partida = self.partida
        for nombreprueba, nombrecampo in (
                ('gramaje', 'pruebasGramaje'), 
                ('longitudinal', 'pruebasResistenciaLongitudinal'), 
                ('alongitudinal', 'pruebasAlargamientoLongitudinal'), 
                ('transversal', 'pruebasResistenciaTransversal'), 
                ('atransversal', 'pruebasAlargamientoTransversal'), 
                ('compresion', 'pruebasCompresion'), 
                ('perforacion', 'pruebasPerforacion'), 
                ('espesor', 'pruebasEspesor'), 
                ('permeabilidad', 'pruebasPermeabilidad'), 
                ('poros', 'pruebasPoros'), 
                ('piramidal', 'pruebasPiramidal')):
            media = 0.0
            for p in eval("partida.%s" % nombrecampo):
                media += p.resultado
            try:
                media /= len(eval("partida.%s" % nombrecampo))
            except ZeroDivisionError:
                media = 0
            eval("partida.set(%s = %f)" % (nombreprueba, media))
        self.rellenar_info_partida()

    def actualizar_ventana(self):
        """
        Método que sobreescribe el "actualizar_ventana" que hereda de la 
        clase ventana.
        PRECONDICION: self.partida no puede ser None
        """
        try:
            self.partida.sync()
            self.rellenar_widgets()
        except pclases.SQLObjectNotFound:
                utils.dialogo_info(titulo = 'REGISTRO ELIMINADO', 
                    texto = 'El registro ha sido borrado desde otro puesto.', 
                    padre = self.wids['ventana'])
                self.partida = None
        self.activar_widgets(self.partida!=None)


    # --------------- Manejadores de eventos ----------------------------
    def guardar_obs(self, boton):
        """
        Guarda el contenido del TextView en el atributo observaciones.
        """
        if self.objeto != None:
            buffer = self.wids['txt_observaciones'].get_buffer()
            self.objeto.observaciones = buffer.get_text(
                buffer.get_start_iter(), buffer.get_end_iter())
            self.wids['b_guardar_obs'].set_sensitive(False)

    def add(self, w):
        if self.partida != None:
            model = self.wids['tv_pruebas'].get_model()
            model.append((utils.str_fecha(time.localtime()),
                          "", "", "", "", "", "", "", "", "", "", "", 
                          "0,0,0,0,0,0,0,0,0,0,0"))
        else:
            print "WARNING: Se ha intentano añadir una prueba con partida=None"
    
    def drop(self, w):
        """
        Borra una línea completa de resultados.
        """
        model, iter = self.wids['tv_pruebas'].get_selection().get_selected()
        if iter != None and utils.dialogo(titulo = 'BORRAR PRUEBA', 
                                          texto = '¿Está seguro?', 
                                          padre = self.wids['ventana']):
            ids = map(int, model[iter][-1].split(','))
            for columnaid in range(len(ids)):
                id = ids[columnaid]
                if id != 0:
                    clase = self.get_clase(columnaid+1)
                    prueba = clase.get(id)
                    prueba.destroy(ventana = __file__)
            self.rellenar_pruebas()

    def set_partida(self, w):
        comprobar_y_preguntar_si_guardar(self)
        numpartida = utils.dialogo_entrada(titulo = 'Nº PARTIDA', 
                        texto = 'Introduzca número de partida:', 
                        padre = self.wids['ventana'])
        if numpartida != None:
            numpartida = numpartida.upper().replace("P-", "")
            partidas = pclases.Partida.select(
                        pclases.Partida.q.codigo.contains(numpartida))
            if partidas.count() == 0:
                utils.dialogo_info(titulo = 'PARTIDA NO ENCONTRADA', 
                    texto = 'No se encontró ninguna partida %s.' % numpartida, 
                    padre = self.wids['ventana'])
                return
            elif partidas.count() > 1:
                filas = [(l.id, 
                          l.numpartida, 
                          l.codigo, 
                          l.partidaCarga and l.partidaCarga.codigo or "" , 
                          l.longitudinal, 
                          l.transversal, 
                          l.compresion, 
                          l.perforacion, 
                          l.permeabilidad, 
                          l.poros, 
                          l.espesor, 
                          l.piramidal
                         ) for l in partidas]
                idpartida = utils.dialogo_resultado(filas, 
                    titulo = 'SELECCIONE PARTIDA',
                    cabeceras = ('ID', 'Número', 'Código', 'Partida Carga', 
                                 'Longitudinal', 'Transversal', 'CBR', 
                                 'Perforación', 'Permeabilidad', 'Poros', 
                                 'Espesor', 'Piramidal'), 
                    padre = self.wids['ventana'])
                if idpartida < 0:
                    return
                partida = pclases.Partida.get(idpartida)
            else:
                partida = partidas[0]
            if len(partida.rollos) == 0:
                utils.dialogo_info(titulo = 'PARTIDA VACÍA', 
                    texto = 'La partida no contiene rollos, no puede\n'
                            'realizar pruebas sobre una partida vacía.', 
                    padre = self.wids['ventana'])
                self.partida = None
                return
            self.partida = partida
            self.actualizar_ventana()
    
    def rellenar_widgets(self):
        self.objeto = self.partida
        self.activar_widgets(self.partida != None)
        if self.partida != None:
            self.rellenar_info_partida()
            self.rellenar_pruebas()
            self.rellenar_observaciones()
            self.rellenar_muestras()

    def rellenar_muestras(self):
        """
        Rellena el TreeView de las muestras extraídas a la partida.
        """
        model = self.wids['tv_muestras'].get_model()
        model.clear()
        if self.partida != None:
            for m in self.partida.muestras:
                model.append((m.codigo, m.observaciones, m.pendiente, 
                              utils.str_fecha(m.envio), 
                              utils.str_fecha(m.recepcion), m.id))

    def rellenar_observaciones(self):
        """
        Introduce las observaciones de la partida en el TextView.
        """
        self.wids['txt_observaciones'].get_buffer().set_text(
            self.objeto.observaciones)
        self.wids['b_guardar_obs'].set_sensitive(False)

    def rellenar_info_partida(self):
        """
        PRECONDICIÓN: self.partida != None y len(self.partida.balas) > 0
        """
        partida = self.partida
        self.wids['e_numpartida'].set_text("%d (%s) - Partida carga %s" % (
            partida.numpartida, 
            partida.codigo, 
            partida.partidaCarga and partida.partidaCarga.codigo or "?"))
        productos_de_la_partida = partida.get_productos() 
        producto_de_la_partida = ", ".join(
            [p.descripcion for p in productos_de_la_partida])
        self.wids['e_nombre'].set_text(producto_de_la_partida)
        self.wids['e_gramaje'].set_text("%.2f" % partida.gramaje)
        self.wids['e_rlongitudinal'].set_text("%.2f" % partida.longitudinal)
        self.wids['e_alongitudinal'].set_text("%.2f" % partida.alongitudinal)
        self.wids['e_rtransversal'].set_text("%.2f" % partida.transversal)
        self.wids['e_atransversal'].set_text("%.2f" % partida.atransversal)
        self.wids['e_cbr'].set_text("%.2f" % partida.compresion)
        self.wids['e_cono'].set_text("%.2f" % partida.perforacion)
        self.wids['e_espesor'].set_text("%.2f" % partida.espesor)
        self.wids['e_permeabilidad'].set_text("%.2f" % partida.permeabilidad)
        self.wids['e_porometria'].set_text("%.3f" % partida.poros)
        self.wids['e_piramidal'].set_text("%.2f" % partida.piramidal)
        self.rellenar_lotes()

    def cambiar_fecha(self, cell, path, texto):
        try:
            fecha = time.strptime(texto, '%d/%m/%Y')
        except:
            utils.dialogo_info('FECHA INCORRECTA', 
                'La fecha introducida (%s) no es correcta.' % texto, 
                padre = self.wids['ventana'])
            return
        model = self.wids['tv_pruebas'].get_model()
        model[path][0] = utils.str_fecha(fecha)
        ids = map(int, model[path][-1].split(','))
        for col in xrange(11):  # HARCODED: Muy muy feo...
            if ids[col] != 0:
                clase = self.get_clase(col+1)
                prueba = clase.get(ids[col])
                prueba.fecha = fecha

    def get_clase(self, columna):
        # HARCODED: Más feo que un frigorífico por detrás.
        if columna == 1:
            clase = pclases.PruebaGramaje
        elif columna == 2:
            clase = pclases.PruebaLongitudinal
        elif columna == 3:
            clase = pclases.PruebaAlargamientoLongitudinal
        elif columna == 4:
            clase = pclases.PruebaTransversal
        elif columna == 5:
            clase = pclases.PruebaAlargamientoTransversal
        elif columna == 6:
            clase = pclases.PruebaCompresion
        elif columna == 7:
            clase = pclases.PruebaPerforacion
        elif columna == 8:
            clase = pclases.PruebaEspesor
        elif columna == 9:
            clase = pclases.PruebaPermeabilidad
        elif columna == 10:
            clase = pclases.PruebaPoros
        elif columna == 11:
            clase = pclases.PruebaPiramidal
        else:
            self.logger.error("resultados_geotextiles::get_clase "
                "-> Columna %d no pertenece a ningún tipo de prueba. "
                "No debería entrar aquí." % (columna))
            clase = None
        return clase

    def cambiar_resultado(self, tv, path, texto, columna):
        texto = texto.replace(" ", "")
        if texto != "":
            try:
                resultado = float(texto)
            except:
                utils.dialogo_info('RESULTADO INCORRECTO',
                    'El número tecleado (%s) no es correcto.' % texto, 
                    padre = self.wids['ventana'])
                return
        clase = self.get_clase(columna)
        columnaid = columna-1    # Porque en los IDS empieza por 0
        if clase != None:
            model = self.wids['tv_pruebas'].get_model()
            ids = map(int, model[path][-1].split(','))
            id = ids[columnaid]
            if id == 0:
                if texto != "":
                    fecha = time.strptime(model[path][0], '%d/%m/%Y') 
                    prueba = clase(fecha = fecha, 
                                   resultado = resultado,
                                   partida = self.partida)
                    ids[columnaid] = prueba.id
                    model[path][-1] = ','.join(map(str, ids))
                    if columna != 10:
                        model[path][columna] = "%.2f" % resultado
                    else:
                        model[path][columna] = "%.3f" % resultado
                    ## model[path][columna] = "%.2f" % resultado
            else:
                prueba = clase.get(int(id))
                if texto == "": 
                    try:
                        prueba.destroy(ventana = __file__)
                    except:
                        utils.dialogo_info(titulo = "ERROR", 
                            texto = "El resultado no se pudo eliminar.", 
                            padre = self.wids['ventana'])
                        return
                    model[path][columna] = ""
                    ids[columnaid] = 0 
                    model[path][-1] = ','.join(map(str, ids))
                    self.rellenar_pruebas()     # Prefiero esto a comprobar 
                                    # si la fila se ha quedado vacía, etc...
                else:
                    prueba.resultado = resultado
                    if columna != 10:
                        model[path][columna] = "%.2f" % resultado
                    else:
                        model[path][columna] = "%.3f" % resultado
                    # model[path][columna] = "%.2f" % resultado
            self.calcular_caracteristicas()
            # print model[path][-1]
            # self.rellenar_pruebas()

    def cambiar_gramaje(self, tv ,path, texto):
        self.cambiar_resultado(tv, path, texto, 1)
        
    def cambiar_r_longitudinal(self, tv ,path, texto):
        self.cambiar_resultado(tv, path, texto, 2)
        
    def cambiar_a_longitudinal(self, tv ,path, texto):
        self.cambiar_resultado(tv, path, texto, 3)
        
    def cambiar_r_transversal(self, tv ,path, texto):
        self.cambiar_resultado(tv, path, texto, 4)
        
    def cambiar_a_transversal(self, tv ,path, texto):
        self.cambiar_resultado(tv, path, texto, 5)

    def cambiar_compresion(self, tv ,path, texto):
        self.cambiar_resultado(tv, path, texto, 6)

    def cambiar_perforacion(self, tv ,path, texto):
        self.cambiar_resultado(tv, path, texto, 7)

    def cambiar_espesor(self, tv ,path, texto):
        self.cambiar_resultado(tv, path, texto, 8)

    def cambiar_permeabilidad(self, tv ,path, texto):
        self.cambiar_resultado(tv, path, texto, 9)
    
    def cambiar_porometria(self, tv ,path, texto):
        self.cambiar_resultado(tv, path, texto, 10)

    def cambiar_piramidal(self, tv ,path, texto):
        self.cambiar_resultado(tv, path, texto, 11)

    def imprimir(self, boton):
        """
        Imprime la información en pantalla.
        """
        import informes, geninformes
        txt = "PARTIDA: %s\n" % (self.wids['e_numpartida'].get_text())
        txt += "PRODUCTO: %s\n\n" % (self.wids['e_nombre'].get_text())
        txt += "Lote y materia prima consumida:\n"
        model = self.wids['tv_lotes'].get_model()
        for fila in model:
            txt += "    %s\n" % (fila[0])
        txt += "\nMuestras relacionadas:\n"
        model = self.wids['tv_muestras'].get_model()
        for fila in model:
            txt += "    %s %s\n" % (fila[0], fila[1])
        txt += "\nCaracterísticas de la partida:\n"
        txt += "    Gramaje: %s\n" % (self.wids['e_gramaje'].get_text())
        txt += "    Resistencia longitudinal: %s\n" % (
            self.wids['e_rlongitudinal'].get_text())
        txt += "    Resistencia transversal: %s\n" % (
            self.wids['e_rtransversal'].get_text())
        txt += "    CBR: %s\n" % (self.wids['e_cbr'].get_text())
        txt += "    Cono: %s\n" % (self.wids['e_cono'].get_text())
        txt += "    Espesor: %s\n" % (self.wids['e_espesor'].get_text())
        txt += "    Alargamiento longitudinal: %s\n" % (
            self.wids['e_alongitudinal'].get_text())
        txt += "    Alargamiento transversal: %s\n" % (
            self.wids['e_atransversal'].get_text())
        txt += "    Permeabilidad: %s\n" % (
            self.wids['e_permeabilidad'].get_text())
        txt += "    Porometría: %s\n" % (self.wids['e_porometria'].get_text())
        txt += "    Piramidal: %s\n" % (self.wids['e_piramidal'].get_text())
        txt += "\nResultados de las pruebas:\n"
        model = self.wids['tv_pruebas'].get_model()
        for fila in model:
            txt += "    %s\n" % (fila[0])
            txt += "        Gramaje (gr/m²): %s\n" % (fila[1])
            txt += "        Resistencia longitudinal (kN/m): %s\n" % (fila[2])
            txt += "        Alargamiento longitudinal (%%): %s\n" % (fila[3])
            txt += "        Resistencia transversal (kN/m): %s\n" % (fila[4])
            txt += "        Alargamiento transversal (%%): %s\n" % (fila[5])
            txt += "        CBR (kN): %s\n" % (fila[6])
            txt += "        Cono: %s\n" % (fila[7])
            txt += "        Espesor (mm): %s\n" % (fila[8])
            txt += "        Permeabilidad (l/m²/s): %s\n" % (fila[9])
            txt += "        Porometría (mm): %s\n" % (fila[10])
            txt += "        Piramidal (kN): %s\n\n" % (fila[11])
        buffer = self.wids['txt_observaciones'].get_buffer()
        txt += "\nObervaciones: %s\n" % buffer.get_text(
            buffer.get_start_iter(), buffer.get_end_iter())
        informes.abrir_pdf(geninformes.texto_libre(txt, 
            "Resultados de laboratorio: %s" % (
                self.objeto and self.objeto.codigo or "")))
        
def build_dic_pruebas():
    """
    Devuelve un diccionario cuyas claves son los nombres 
    de las pruebas de laboratorio y sus valores son el 
    nombre que reciben los atributos de la prueba en 
    el objeto camposEspecificosRollo.
    """
    dic = {}
    dic['CBR'] = "Compresion"
    dic['Alargamiento longitudinal'] = "AlargamientoLongitudinal"
    dic['Alargamiento transversal'] = "AlargamientoTransversal"
    dic['Resistencia longitudinal'] = "Longitudinal"
    dic['Resistencia transversal'] = "Transversal"
    dic['Cono'] = "Perforacion"
    dic['Permeabilidad'] = "Permeabilidad"
    dic['Porometría'] = "Poros"
    # dic['Espesor'] = "Espesor"    # CWT: No quiere que aparezca el 
            # espesor en la ventana de comparación con el marcado CE.
    dic['Gramaje'] = "Gramaje"
    dic['Piramidal'] = "Piramidal"
    return dic
        

if __name__=='__main__':
    a = ResultadosGeotextiles()

