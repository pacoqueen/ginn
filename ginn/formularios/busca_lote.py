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
## busca_lote.py -- 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
##
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases

class BuscaLote(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        Ventana.__init__(self, 'busca_lote.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_ayuda/clicked': self.ayuda}
        self.add_connections(connections)
        cols = (('Num. Lote','gobject.TYPE_INT64',False,True,False,None),
                ('Código','gobject.TYPE_STRING',False,True,False,None),
                ('Tenacidad','gobject.TYPE_STRING',False,True,False,None),
                ('Elongación','gobject.TYPE_STRING',False,True,False,None),
                ('Rizo','gobject.TYPE_STRING',False,True,False,None),
                ('Encogimiento','gobject.TYPE_STRING',False,True,False,None),
                ('Idlote','gobject.TYPE_INT64',False,False,False,None))
        utils.preparar_listview(self.wids['tv_resultado'], cols)
        utils.rellenar_lista(self.wids['cmbe_producto'], [(p.id, p.nombre) for p in pclases.ProductoVenta.select(pclases.ProductoVenta.q.camposEspecificosBalaID != None, orderBy = 'nombre')])
        self.rellenar_tabla()
        # Valores por defecto:
        self.wids['e_tenacidad'].set_text('A')
        self.wids['e_elongacion'].set_text('A')
        self.wids['e_rizo'].set_text('6-7')
        self.wids['e_encogimiento'].set_text('A')
        self.wids['chk_tenacidad'].set_active(True)
        self.wids['chk_elongacion'].set_active(True)
        self.wids['chk_rizo'].set_active(True)
        self.wids['chk_encogimiento'].set_active(True)
        self.wids['chk_producto'].set_active(True)
        
        gtk.main()


    def chequear_cambios(self):
        pass

    def rellenar_tabla(self,lista = []):
        """
        Rellena el model con los resultados de la búsqueda almacenados
        en una lista de lotes.
        """        
        model = self.wids['tv_resultado'].get_model()
        model.clear()
        for elem in lista:
            model.append((elem.numlote,
                    elem.codigo,
                    "%s (%s)" % (str(elem.tenacidad), utils.float2str(elem.calcular_tenacidad_media())),
                    "%s (%s)" % (str(elem.elongacion), utils.float2str(elem.calcular_elongacion_media())),
                    "%s (%s)" % (elem.rizo, utils.float2str(elem.calcular_rizo_medio())),
                    "%s (%s)" % (elem.encogimiento, utils.float2str(elem.calcular_encogimiento_medio())),
                    elem.id))
    
    def buscar(self,boton):
        """
        Realiza una búsqueda de lotes sobre los parámetros activados mediante
        los checkboxes cuyos datos coincidad con el contenido de los entries
        """
        from ventana_progreso import VentanaProgreso
        
        if self.wids['chk_producto'].get_active():
            idproducto = utils.combo_get_value(self.wids['cmbe_producto'])
            if idproducto == None:
                utils.dialogo_info(titulo = 'ERROR', 
                                   texto = 'Si desea hacer una búsqueda filtrada por producto, debe seleccionar uno',
                                   padre = self.wids['ventana'])
                return
            # Optimizacion de la búsqueda
            articulos = pclases.Articulo.select(pclases.AND(pclases.Articulo.q.albaranSalidaID == None,
                                                              pclases.Articulo.q.productoVentaID == idproducto))
        else:
            articulos = pclases.Articulo.select(pclases.AND(pclases.Articulo.q.albaranSalidaID == None, 
                                                              pclases.Articulo.q.balaID != None))
        # TODO: Creo que se pueden mejorar las consultas un poco más.
        loteids = []
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar() 
        i = 0.0
        tot = articulos.count()
        for a in articulos:
            if a.bala.loteID not in loteids:
                loteids.append(a.bala.loteID)
            vpro.set_valor(i/tot, 'Buscando en el almacén...')
            i += 1
        vpro.ocultar()       
        
        criterio = True
        
        if self.wids['chk_tenacidad'].get_active():
            criterio = pclases.AND(criterio,pclases.Lote.q.tenacidad == self.wids['e_tenacidad'].get_text())
        if self.wids['chk_elongacion'].get_active():
            criterio = pclases.AND(criterio,pclases.Lote.q.elongacion == self.wids['e_elongacion'].get_text())
        if self.wids['chk_rizo'].get_active():
            rizo = self.wids['e_rizo'].get_text()
            if '-' in rizo:
                criterioRizo = False
                temp = rizo.split('-')
                try:
                    a = int(temp[0])
                    b = int(temp[1])+1
                except:
                    utils.dialogo_info(titulo = 'ERROR', 
                                       texto = 'Los valores de rizo deben ser enteros y los rangos deben separarse con un guión',
                                       padre = self.wids['ventana'])
                    return
                for i in range(a,b):
                    criterioRizo = pclases.OR(criterioRizo,pclases.Lote.q.rizo == str(i)) 
                criterio = pclases.AND(criterio, criterioRizo)
            else:
                criterio = pclases.AND(criterio,pclases.Lote.q.rizo == self.wids['e_rizo'].get_text())
        if self.wids['chk_encogimiento'].get_active():
            criterio = pclases.AND(criterio,pclases.Lote.q.encogimiento == self.wids['e_encogimiento'].get_text())
        lotes = pclases.Lote.select(criterio)

        resultado = [l for l in lotes if l.id in loteids]
                        
        self.rellenar_tabla(resultado)

    def ayuda(self,boton):
        """
        Muestra un cuadro de ayuda
        """
        utils.dialogo_info(texto = "Seleccione que criterios de búsqueda que quiere utilizar con las casillas de verificación.\nLa búsqueda sólo filtrará los datos introducidos cuya casilla esté activa",
                           titulo = 'AYUDA',
                           padre = self.wids['ventana'])

if __name__ == '__main__':
    b = BuscaLote()    

