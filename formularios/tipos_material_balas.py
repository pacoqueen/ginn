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
## tipos_material_balas.py 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 14 de septiembre de 2005 -> Inicio
## 20 de septiembre de 2005 -> Funciones genéricas comunes.
## 23 de septiembre de 2005 -> Cambios menores
## 14 de octubre de 2005 -> Añadida confirmación al salir.
## 18 de octubre de 2005 -> Importo el módulo "time".
## 18 de octubre de 2005 -> Vuelvo a conectar "ventana/destroy" a 
##   gtk.main_quit. No termina de funcionar con el callback salir.
## 24 de octubre de 2005 -> Minor bugfix con un resultados.count en
##   vez de resultados.count() que llevaba tiempo arrastrando.
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sqlobject
try:
    import pclases
except ImportError:
    import sys
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    import pclases

class TiposMaterialBala(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        Ventana.__init__(self, 'tipos_material_balas.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_agregar/clicked': self.crear_nuevo_tipodematerialBala,
                       'b_borrar/clicked': self.eliminar_tipo_de_materialBala,
                       'b_modificar/clicked': self.modificar_tipo_de_materialBala}
        self.add_connections(connections)
        cols = (('Tipo de material de bala','gobject.TYPE_STRING',False,True,False,None),
                ('Código del material','gobject.TYPE_STRING',False,True,False,None),
                ('IdtipodematerialBala','gobject.TYPE_INT64',False,False,False,None))
        utils.preparar_listview(self.wids['tv_tipos'], cols)
        self.rellenar_tabla()
        gtk.main()


    def chequear_cambios(self):
        pass

    def rellenar_tabla(self):
    	"""
        Rellena el model con los tipos de materialBala existentes
        """        
        tipos = pclases.TipoMaterialBala.select(orderBy="descripcion")
    	model = self.wids['tv_tipos'].get_model()
    	model.clear()
    	for t in tipos:
    		model.append((t.descripcion,
                    t.codigo,        
    				t.id))
    
    
    def eliminar_tipo_de_materialBala(self,widget):
        model, iter = self.wids['tv_tipos'].get_selection().get_selected()
        if iter != None:
            idtipo = model[iter][-1]
            tipodematerialBala = pclases.TipoMaterialBala.get(idtipo)
        else:        
            utils.dialogo_info('ERROR','Seleccione material de bala a eliminar')
            return
        try:	
            tipodematerialBala.destroySelf()
        except:
            utils.dialogo_info('ERROR','No se ha podido eliminar el tipo de material de bala. Probablemente existan procesos con este tipo de material.')
        self.rellenar_tabla()
    
    def modificar_tipo_de_materialBala(self, widget):
    	model, iter = self.wids['tv_tipos'].get_selection().get_selected()
    	if iter != None:
    	    idtipo = model[iter][-1]
            tipodematerialBala = pclases.TipoMaterialBala.get(idtipo)
        else:
            utils.dialogo_info('ERROR','Seleccione material de bala a modificar')
            return
    	nuevotipo = utils.dialogo_entrada('Introduzca el nuevo tipo de material de bala para: ' + tipodematerialBala.descripcion)
    	nuevocodigo = utils.dialogo_entrada('Introduzca el codigo asociado')
    	try:	
            if nuevotipo != None:
                tipodematerialBala.descripcion = nuevotipo
            if nuevocodigo != None:
                tipodematerialBala.codigo = nuevocodigo
    	except:
    		utils.dialogo_info('ERROR','No se ha podido modificar el tipo de material de bala.')

    	self.rellenar_tabla()
    
    
    def crear_nuevo_tipodematerialBala(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
    	nuevotipo = utils.dialogo_entrada('Introduzca el nuevo tipo de material')
    	nuevocodigo = utils.dialogo_entrada('Introduzca el código asociado al material')
        if nuevotipo != None and nuevocodigo !=None :
            tipodematerialBala = pclases.TipoMaterialBala(descripcion = nuevotipo, codigo = nuevocodigo)
            pclases.Auditoria.nuevo(tipodematerialBala, self.usuario, __file__)
    	self.rellenar_tabla()
    
    
if __name__ == '__main__':
    t = TiposMaterialBala()    
