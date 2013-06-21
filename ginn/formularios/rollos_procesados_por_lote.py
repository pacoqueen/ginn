#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado                    #
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

###################################################################
## trazabilidad_articulos.py - Trazabilidad de rollo, bala o bigbag
###################################################################
## NOTAS:
##  
## ----------------------------------------------------------------
##  
###################################################################
## Changelog:
## 17 de enero de 2008 -> Inicio
###################################################################


from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
import mx.DateTime

class RollosProcesadosPorLote(Ventana):
    def __init__(self, objeto = None, usuario = None):
        self.usuario = usuario
        Ventana.__init__(self, 'rollos_procesados_por_lote.glade', 
                         objeto, 
                         self.usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir, 
                       'b_exportar/clicked': self.exportar
                      }
        self.add_connections(connections)
        cols = (('Código', 'gobject.TYPE_STRING', False, True, True, None),
                ('Partida', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Albarán', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Fecha fab.','gobject.TYPE_STRING',False,True,False,None), 
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_datos'], cols)
        self.wids['ventana'].resize(800, 600)
        self.wids['ventana'].set_position(gtk.WIN_POS_CENTER)
        self.wids['txt_nums'].grab_focus()
        gtk.main()

    def chequear_cambios(self):
        pass

    def buscar(self, boton):
        """
        Procesa los números que hay en el txt_nums y rellena la tabla 
        con la información de los mismos.
        """
        rollos = self.procesar_numeros()
        self.rellenar_tabla(rollos)

    def procesar_numeros(self):
        """
        Lee el contenido del textview de búsqueda y procesa los números que 
        contiene.
        Para cada número busca el rollo que le corresponde y devuelve una 
        lista de rollos coincidentes.
        """
        buf = self.wids['txt_nums'].get_buffer()
        nums = buf.get_text(*buf.get_bounds()).split()
        rollos = []
        for num in nums:
            rollo_s = buscar_rollo(num)
            for rollo in rollo_s:
                rollos.append(rollo)
        return rollos

    def rellenar_tabla(self, rollos):
        """
        Rellena la tabla con la información de los rollos recibidos.
        """
        model = self.wids['tv_datos'].get_model()
        model.clear()
        for r in rollos:
            model.append((r.codigo, 
                          r.partida and r.partida.codigo or "", 
                          r.albaranSalida and r.albaranSalida.numalbaran or "", 
                          utils.str_fechahora(r.fechahora), 
                          r.id))
 
    def imprimir(self, boton):
        """
        "Vuerca-vuerca" el TreeView en un PDF.
        """
        from informes.treeview2pdf import treeview2pdf
        from formularios.reports import abrir_pdf
        strfecha = utils.str_fecha(mx.DateTime.localtime())
        tv = self.wids['tv_datos']
        abrir_pdf(treeview2pdf(tv, 
                        titulo = "Resultados de proceso de búsqueda por lote", 
                        fecha = strfecha, 
                       apaisado = False))

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        tv = self.wids['tv_datos']
        abrir_csv(treeview2csv(tv))


def buscar_rollo(n):
    """
    Busca un rollo cuyo número de rollo o código sea n.
    Devuelve una lista con todos los objetos rollo coincidentes.
    """
    try:
        menosn = -int(n)
    except (ValueError, TypeError):
        menosn = n
    rollos=pclases.Rollo.select(pclases.OR(pclases.Rollo.q.numrollo == n, 
                                           pclases.Rollo.q.numrollo == menosn))
    try:
        encontrados = rollos.count()
    except: # n lleva letras y no puede compararse con un entero (q.numrollo)
        encontrados = 0
    if encontrados == 0: # Busco por código
        rollos = pclases.Rollo.select(pclases.Rollo.q.codigo == n)
        if rollos.count() == 0: # Busco por código añadiendo R al principio:
            rollos = pclases.Rollo.select(pclases.Rollo.q.codigo == "R"+n)
            if rollos.count() == 0: # Busco por código con LIKE
                rollos=pclases.Rollo.select(pclases.Rollo.q.codigo.contains(n))
    return tuple(rollos)

if __name__ == '__main__':
    t = RollosProcesadosPorLote()
