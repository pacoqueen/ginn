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
## 30 de enero de 2006 -> Inicio
## 
##
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sys, os
from framework import pclases
from informes import geninformes


class RollosAlmacen(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.meses = ['TOTAL', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 
                      'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'] 
        Ventana.__init__(self, 'rollos_almacen.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_actualizar/clicked': self.actualizar
                      }
        self.add_connections(connections)
        self.w_cargando = self.crear_ventana_cargando()
        self.inicializar_ventana()
        import gobject
        gobject.timeout_add (100, self.actualizar_valor_ventana_cargando, priority = gobject.PRIORITY_HIGH)
        self.wids['ventana'].resize(800, 600)
        self.ir_a_mes_actual()
        self.wids['ventana'].resize(800, 600)
        gtk.main()

    def ir_a_mes_actual(self):
        import time
        year = time.localtime().tm_year
        pos = self.years.index(year)
        self.wids['nb_year'].set_current_page(pos)
        mes = time.localtime().tm_mon
        nb = self.wids['nb_year'].get_nth_page(self.wids['nb_year'].get_current_page())
        nb.set_current_page(mes)

    def cambiar_mes(self, notebook, page, pagenumber):
        pos = self.wids['nb_year'].get_current_page()
        year = self.years[pos]
        # Limpio el model de la página actual
        tv = notebook.get_nth_page(notebook.get_current_page()).child.child
        model = tv.get_model()
        if model != None:
            model.clear()
        # Cojo el model de la próxima página (que se convertirá en la actual)
        tv = notebook.get_nth_page(pagenumber).child.child 
        model = tv.get_model()
        if model != None:
            model.clear()
        mes = self.meses[pagenumber]
        self.rellenar_lista(tv, mes, year) 

    # --------------- Funciones auxiliares ------------------------------
    def crear_ventana_cargando(self):
        """
        Crea una ventana con una progressBar dentro.
        Devuelve el objeto GTK de la ventana.
        """
        v = gtk.Window()
        v.set_transient_for(self.wids['ventana'])
        v.set_title('POR FAVOR, ESPERE')
        v.set_modal(True)
        pb = gtk.ProgressBar()
        v.add(pb)
        pb.show()
        v.resize(300,50)
        self.cargando_visible = False
        self.cargando_texto = ''
        self.cargando_valor = 0.0
        return v

    def mostrar_ventana_cargando(self):
        self.w_cargando.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        self.w_cargando.show()
        self.cargando_visible = True
    
    def ocultar_ventana_cargando(self):
        self.w_cargando.hide()
        self.cargando_visible = False 

    def set_valor_ventana_cargando(self, valor, texto):
        """
        valor debe estar entre 0.0 y 0.1
        """
        self.cargando_texto = texto
        self.cargando_valor = valor
        while gtk.events_pending():
            gtk.main_iteration(False)

    def actualizar_valor_ventana_cargando(self):
        if self.cargando_visible:
            pb = self.w_cargando.get_children()[0]
            pb.set_text(self.cargando_texto)
            pb.set_fraction(self.cargando_valor)
        return True

    def es_diferente(self):
        # No hace falta en esta ventana.
        return False

    def aviso_actualizacion(self):
        # No hace falta en esta ventana.
        return False

    def ir_a_primero(self):
        # No hace falta en esta ventana.
        pass

    def colorear(self, tv):
        def cell_func(column, cell, model, itr):
            if model[itr].parent != None:
                numalbaran = model[itr][3]
                if numalbaran != '': 
                    color = "red"
                else:
                    color = "white"
            else:
                color = None
            cell.set_property("cell-background", color)

        cols = tv.get_columns()
        for i in xrange(len(cols)):
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell,cell_func)

    def rellenar_lista(self, tv, mes, year):
        """
        Rellena el model de la lista tv en función del 
        mes y el año recibido.
        Si el mes == 'TOTAL', muestra todos los rollos
        del año year sin filtrar por meses.
        """
        tv.hide()
        self.mostrar_ventana_cargando()
        model = tv.get_model()
        if model == None:
            return
        model.clear()
            # Si no tiene fechahora prefiero que salte una excepción. Ídem con articulos[0]
        if mes != 'TOTAL': # self.meses.index(mes)
            rsproductos, tot = self.get_productos_fabricados_en(year, self.meses.index(mes))
        else:
            rsproductos, tot = self.get_productos_fabricados_en(year)
        tv.freeze_child_notify()
        tv.set_model(None)
        rollostotales = 0
        kilostotales = 0.0
        metrostotales = 0
        rollosvendidos = 0
        kilosvendidos = 0.0
        metrosvendidos = 0
        for producto in rsproductos:
            rollosvendidosdelproducto = 0
            p = producto 
            rollos, tot = self.get_rollos_fabricados_en(year, mes != 'TOTAL' and self.meses.index(mes) or None, p.id)
            metros = tot * producto.camposEspecificosRollo.metrosCuadrados
            kilos_teoricos = tot * producto.camposEspecificosRollo.pesoTeorico
            rollostotales += tot
            kilostotales += kilos_teoricos
            metrostotales += metros
            iterpadre = model.append(None, ('', p.codigo, '%s kg teóricos, ' % (utils.float2str(kilos_teoricos, 2)), 
                                            '%s m², %d rollos de ' % (utils.float2str(metros, 1), tot), p.descripcion, p.id))
            i = 0.0
            for r in rollos:
                self.set_valor_ventana_cargando(i/tot, "Cargando %d/%d de %s..." % (i, tot, p.nombre))
                model.append(iterpadre, 
                             (r[0], 
                              r[1], 
                              r[2], 
                              r[3], 
                              p.nombre,
                              r[4]))
                if r[3]:    # r[3] es el número de albarán. '' si no tiene.
                    rollosvendidosdelproducto += 1
                i += 1
            kilosvendidos += rollosvendidosdelproducto * producto.camposEspecificosRollo.pesoTeorico
            metrosvendidos += rollosvendidosdelproducto * producto.camposEspecificosRollo.metrosCuadrados
            rollosvendidos += rollosvendidosdelproducto
        self.ocultar_ventana_cargando()
        tv.set_model(model)
        tv.thaw_child_notify()
        self.colorear(tv)
        tv.show()
        tv.grab_focus()
        self.wids['e_metros'].set_text("%s m², de los cuales han salido %s m²." % (utils.float2str(metrostotales, 1), 
                                                                                   utils.float2str(metrosvendidos, 1)))
        self.wids['e_kilos'].set_text("%s kg, de los cuales se han vendido %s kg." % (utils.float2str(kilostotales, 2), 
                                                                                      utils.float2str(kilosvendidos, 2)))
        self.wids['e_rollos'].set_text("%d, de los cuales se han vendido %d" % (rollostotales, rollosvendidos))

    def get_albaran_salida(self, idrollo):
        """
        Devuelve el número del albarán de salida o "" relacionado
        con el rollo idrollo.
        """
        rs = pclases.AlbaranSalida.select("""
            albaran_salida.id IN (SELECT albaran_salida_id 
                                  FROM articulo 
                                  WHERE rollo_id = %d) 
            """ % (idrollo))
        if rs.count() == 0:
            return ""
        else:
            return rs[0].numalbaran

    def get_productos_fabricados_en(self, anno, mes = None):
        """
        Devuelve un resultSelect de SQLObject y el número de tuplas 
        correspondientes a los productos de venta de tipo rollo fabricados en el 
        mes y año recibidos (no los rollos ni artículos, solo productoVenta).
        """
        if mes == None:
            rs = pclases.ProductoVenta.select("""
                producto_venta.id IN 
                    (SELECT articulo.producto_venta_id 
                     FROM articulo 
                     WHERE rollo_id IN 
                        (SELECT id 
                         FROM rollo 
                         WHERE date_part('year', fechahora) = %d 
                        )
                    ) """ % (anno), orderBy = "descripcion") 
        else:
            rs = pclases.ProductoVenta.select("""
                producto_venta.id IN 
                    (SELECT articulo.producto_venta_id 
                     FROM articulo 
                     WHERE rollo_id IN 
                        (SELECT id 
                         FROM rollo 
                         WHERE date_part('year', fechahora) = %d 
                            AND date_part('month', fechahora) = %d
                        )
                    ) """ % (anno, mes), orderBy = "descripcion") 
        return rs, rs.count()

    def get_rollos_fabricados_en(self, anno, mes = None, idproducto = None):
        """
        Devuelve un resultSelect de rollos y el número de tuplas 
        fabricados en el año -y mes- recibidos. Si se recibe también un 
        idproducto realiza la consulta sobre rollos de ese producto únicamente.
        """
        if mes != None:
            parte_mes = "AND date_part('month', fechahora) = %d " % (mes)
        else:
            parte_mes = ""
        if idproducto != None:
            parte_producto = "AND rollo.id IN (SELECT rollo_id FROM articulo WHERE producto_venta_id = %d) " % (idproducto)
        else:
            parte_producto = ""
        # rs = pclases.Rollo.select("""date_part('year', fechahora) = %d %s %s """ % (anno, parte_mes, parte_producto),
        #                           orderBy = "id")
        queryBase = """
        SELECT to_char(rollo.fechahora, 'DD/MM/YYYY - HH:MI') AS fecha_fabricacion, 
               rollo.codigo, 
               partida.numpartida, 
               albaran_salida.numalbaran, 
               rollo.id 
        FROM rollo, albaran_salida, articulo, partida 
        WHERE rollo.id = articulo.rollo_id 
                AND albaran_salida.id = articulo.albaran_salida_id 
                AND rollo.partida_id = partida.id """
        rs = pclases.Rollo._connection.queryAll("""%s AND date_part('year', rollo.fechahora) = %d %s %s ORDER BY rollo.numrollo""" \
                                                % (queryBase, anno, parte_mes, parte_producto))
        # Separo en la lista los servidos primero y a continuación los que siguen en almacén. 
        queryBase = """
        SELECT to_char(rollo.fechahora, 'DD/MM/YYYY - HH:MI') AS fecha_fabricacion, 
               rollo.codigo, 
               partida.numpartida, 
               '' AS numalbaran, 
               rollo.id 
        FROM rollo, articulo, partida 
        WHERE rollo.id = articulo.rollo_id 
                AND albaran_salida_id IS NULL 
                AND rollo.partida_id = partida.id """
        rs_almacen = pclases.Rollo._connection.queryAll("""%s AND date_part('year', rollo.fechahora) = %d %s %s ORDER BY rollo.numrollo""" \
                                                % (queryBase, anno, parte_mes, parte_producto))
        #DEBUG: print len(rs), len(rs_almacen)
        rs = rs + rs_almacen
        return rs, len(rs)

    def crear_listview(self, mes, year):
        # Primero hay que crear el TreeView que mostrará 
        # el contenido de cada solapa.
        tv = gtk.TreeView()
        cols = (('Fecha y hora', 'gobject.TYPE_STRING', False, True,  False, None), 
                ('Nº Rollo',     'gobject.TYPE_STRING', False, True,  True,  None), 
                ('Partida',      'gobject.TYPE_STRING', False, True,  False, None), 
                ('Nº Albarán',   'gobject.TYPE_STRING', False, True,  False, None), 
                ('Nombre',       'gobject.TYPE_STRING', False, True,  False, None), 
                ('ID',           'gobject.TYPE_INT64',  False, False, False, None))
        utils.preparar_treeview(tv, cols)
        tv.show()
        tv.set_search_column(1)     # Pasa de mí.
        return tv

    def crear_notebook(self, year):
        # Ahora creo cada una de las solapas de los meses.
        nb_mes = gtk.Notebook()
        for mes in self.meses:   
            contenedor = gtk.ScrolledWindow()
            contenedor.add_with_viewport(self.crear_listview(mes, year))
            label = gtk.Label(mes)
            nb_mes.append_page(contenedor, label)
            contenedor.show()
        nb_mes.connect('switch-page', self.cambiar_mes)
        nb_mes.show()
        return nb_mes
 
    def inicializar_ventana(self):
        """
        Inicializa los widgets de la ventana.
        """
        # Creo las solapas del notebook de años en función 
        # de los años de todos los rollos de la BD.
        rollos = pclases.Rollo.select()
        self.years = []
        for r in rollos:
            year = r.fechahora.year
            if year not in self.years:
                self.years.append(year)
        self.years.sort()
        self.limpiar_nb(self.wids['nb_year'])
        for year in self.years:
            self.wids['nb_year'].append_page(self.crear_notebook(year), gtk.Label(str(year)))
        self.wids['nb_year'].show()
        self.wids['ventana'].set_position(gtk.WIN_POS_CENTER_ALWAYS)

    def limpiar_nb(self, nb):
        """
        Limpia todas las hojas del notebook.
        """
        while nb.get_n_pages() > 0:
            nb.remove_page(-1)

    # --------------- Manejadores de eventos ----------------------------

    def actualizar(self, w):
        pos = self.wids['nb_year'].get_current_page()
        year = self.years[pos]
        # Limpio el model de la página actual
        notebook = self.wids['nb_year'].get_nth_page(pos)
        tv = notebook.get_nth_page(notebook.get_current_page()).child.child
        model = tv.get_model()
        if model != None:
            model.clear()
        # Obtengo el mes y vuelvo a rellenar la lista
        mes = self.meses[notebook.get_current_page()]
        self.ocultar_ventana_cargando()
        self.rellenar_lista(tv, mes, year) 
        

if __name__=='__main__':
    a = RollosAlmacen()

