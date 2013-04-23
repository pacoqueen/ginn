#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2007 Francisco José Rodríguez Bogado                          #
#                    (pacoqueen@users.sourceforge.net)                        #
#                                                                             #
# This file is part of Dent-Inn.                                              #
#                                                                             #
# Dent-Inn is free software; you can redistribute it and/or modify            #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation; either version 2 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# Dent-Inn is distributed in the hope that it will be useful,                 #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with Dent-Inn; if not, write to the Free Software                     #
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA  #
###############################################################################

###################################################################
## trazabilidad.py - Trazabilidad GENERAL de cualquier registro.
###################################################################
## NOTAS:
##  
## ----------------------------------------------------------------
##  
###################################################################
## Changelog:
## 24 de mayo de 2006 -> Inicio
## 24 de mayo de 2006 -> It's alive!
## 9 de diciembre de 2006 -> Añadida consola.
###################################################################
## 
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
import os 
from formularios import cmdgtk

class Trazabilidad(Ventana):
    """
    Ventana de trazabilidad interna de objetos.
    Acepta tanto códigos de trazabilidad como consultas a la BD de SQLObject.
    """
    def __init__(self, objeto = None, usuario = None, ventana_padre = None, locals_adicionales = {}):
        try:
            Ventana.__init__(self, 'trazabilidad.glade', objeto, usuario = usuario)
        except:     # Tal vez me estén llamando desde otro directorio
            Ventana.__init__(self, os.path.join('..', 'formularios', 'trazabilidad.glade'), objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar}
        self.add_connections(connections)
        cols = (('ID', 'gobject.TYPE_STRING', False, False, False, None),
                ('campo', 'gobject.TYPE_STRING', False, False, False, None),
                ('valor', 'gobject.TYPE_STRING', True, False, True, self.cambiar_valor),
                ('clase', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        self.wids['e_num'].connect("key_press_event", self.pasar_foco)
        self.wids['tv_datos'].connect("row-expanded", self.expandir)
        self.wids['tv_datos'].connect("row-collapsed", self.cerrar)
        from formularios import pyconsole
        vars_locales = locals()
        for k in locals_adicionales:
            vars_locales[k] = locals_adicionales[k] 
        consola = pyconsole.attach_console(self.wids['contenedor_consola'],  # @UnusedVariable
                                           banner = "Consola python de depuración GINN", 
                                           script_inicio = """import sys, os, pygtk, gtk, gtk.glade, utils
from framework import pclases, mx.DateTime
from framework.seeker import VentanaGenerica as Ver
dir()
#Ver(self.objeto)
""", 
                                            locales = vars_locales)
        if objeto != None:
            self.rellenar_datos(objeto)
        cmd_gtk = cmdgtk.CmdGTK()
        cmd_gtk.attach_to(self.wids['boxcmd'])
        #-----------------------------------------------------------------------------------------------#
        def comprobar_que_no_me_hace_el_gato(paned, scrolltype_or_allocation_or_requisition = None):    #
            width = self.wids['ventana'].get_size()[0]                                                  #
            MIN =  width / 2                                                                            #
            MAX = width - 100                                                                           #
            posactual = paned.get_position()                                                            #
            if posactual < MIN:                                                                         #
                paned.set_position(MIN)                                                                 #
            elif posactual > MAX:                                                                       #
                paned.set_position(MAX)                                                                 #
        #-----------------------------------------------------------------------------------------------#
        self.wids['hpaned1'].connect("size_request", comprobar_que_no_me_hace_el_gato)
        self.wids['ventana'].resize(800, 600)
        self.wids['hpaned1'].set_position(self.wids['ventana'].get_size()[0] / 2)
        self.wids['ventana'].set_position(gtk.WIN_POS_CENTER)
        gtk.main()

    def pasar_foco(self, widget, event):
        if event.keyval == 65293 or event.keyval == 65421:
            self.wids['b_buscar'].grab_focus()

    def chequear_cambios(self):
        pass

    def buscar_bala(self, txt):
        ar = None
        ars = pclases.Bala.select(pclases.Bala.q.numbala.contains(txt))
        if ars.count() == 1:
            ar = ars[0]
        elif ars.count() > 1:
            filas = [(a.id, a.numbala, a.codigo) for a in ars]
            idbala = utils.dialogo_resultado(filas,
                                             titulo = "Seleccione bala", 
                                             cabeceras = ('ID', 'Número de bala', 'Código'),
                                             padre = self.wids['ventana'])
            if idbala > 0:
                ar = pclases.Bala.get(idbala)
        return ar

    def buscar_rollo(self, txt):
        ar = None
        ars = pclases.Rollo.select(pclases.Rollo.q.numrollo.contains(txt))
        if ars.count() == 1:
            ar = ars[0]
        elif ars.count() > 1:
            filas = [(a.id, a.numrollo, a.codigo) for a in ars]
            idrollo = utils.dialogo_resultado(filas, 
                                              titulo = "Seleccione rollo", 
                                              cabeceras = ('ID', 'Número de rollo', 'Código'),
                                              padre = self.wids['ventana'])
            if idrollo > 0:
                ar = pclases.Rollo.get(idrollo)
        return ar

    def buscar_articulo(self, txt):
        ar = None
        ars = pclases.Rollo.select(pclases.Rollo.q.numrollo.contains(txt))
        if ars.count() == 0:
            ar = self.buscar_bala(txt)
        elif ars.count() == 1:
            ar = ars[0]
        else:
            ar = self.buscar_rollo(txt)
        return ar

    def buscar(self, b):
        a_buscar = self.wids['e_num'].get_text()
        if "pclases." in a_buscar and ("select" in a_buscar or "get" in a_buscar):
            try:
                self.rellenar_datos(eval(a_buscar))
                articulo = None
            except:
                utils.dialogo_info(titulo = "ERROR EN CONSULTA", 
                                   texto = "La consulta:\n%s\nprovocó una excepción." % a_buscar,
                                   padre = self.wids['ventana'])
            return
        elif a_buscar.startswith('r') or a_buscar.startswith('R'):
            articulo = self.buscar_rollo(a_buscar[1:])
        elif a_buscar.startswith('b') or a_buscar.startswith('B'):
            articulo = self.buscar_bala(a_buscar[1:])
        elif a_buscar.upper().startswith('AS'):
            try:
                ide = int(a_buscar[2:])
            except ValueError:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "El ID debe ser númerico.\nIntrodujo %s." % (a_buscar[2:]), 
                                   padre = self.wids['ventana'])
                return
            try:
                articulo = pclases.AlbaranSalida.get(ide)
            except pclases.SQLObjectNotFound:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "El AlbaranSalida con ID %d no existe." % (ide), 
                                   padre = self.wids['ventana'])
                return
        elif a_buscar.upper().startswith('PDP'):
            try:
                ide = int(a_buscar[3:])
            except ValueError:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "El ID debe ser númerico.\nIntrodujo %s." % (a_buscar[3:]), 
                                   padre = self.wids['ventana'])
                return
            try:
                articulo = pclases.ParteDeProduccion.get(ide)
            except pclases.SQLObjectNotFound:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "El ParteDeProduccion con ID %d no existe." % (ide), 
                                   padre = self.wids['ventana'])
                return
        else:
            articulo = self.buscar_articulo(a_buscar)
        if articulo != None:
            articulo.sync()
            self.rellenar_datos(articulo)
        else:
            utils.dialogo_info(titulo = "NO ENCONTRADO", texto = "Producto no encontrado", padre = self.wids['ventana'])

    def rellenar_datos(self, articulo):
        model = self.wids['tv_datos'].get_model()
        model.clear()
        itr = self.insertar_rama(articulo, None, model)  # @UnusedVariable
    
    def insertar_rama(self, objeto, padre, model):
        itr = self.insertar_nombre(objeto, padre, model)
        self.insertar_campos(objeto, itr, model)
        self.insertar_ajenos(objeto, itr, model)
        self.insertar_multiples(objeto, itr, model)
        return itr
    
    def insertar_nombre(self, objeto, padre, model, nombre_opcional = ""):
        if objeto == None:
            itr = model.append(padre, ("", 
                                       nombre_opcional, 
                                       "", 
                                       ""))
            return None
        else:
            try:
                nombretabla = objeto.sqlmeta.table
            except AttributeError: # SQLObject <= 0.6.1
                nombretabla = objeto._table
            itr = model.append(padre, (objeto.id, 
                                        nombretabla, 
                                        "", 
                                        objeto.__class__.__name__))
            return itr
         
    def insertar_campos(self, objeto, padre, model):
        """
        Inserta los campos del objeto colgando de la rama "iter".
        Siempre empieza por el ID y el nombre de la tabla del objeto y 
        a continuación sus campos.
        Devuelve el iter del objeto insertado.
        """
        if padre == None: return
        try:
            campos = [c for c in objeto.sqlmeta.columns 
                      if not c.upper().endswith('ID')]
        except AttributeError:  # SQLObject > 0.6.1
            campos = [c for c in objeto.sqlmeta.columns
                      if not c.upper().endswith("ID")]
        for campo in campos:
            model.append(padre, ("", campo, getattr(objeto, campo), ""))
        # return iter

    def insertar_ajenos(self, objeto, padre, model):
        """
        Inserta los nombres de las claves ajenas del objeto
        con un "child" vacío para poder mostrar el desplegable y
        rellenar los campos de la clave ajena en cuestión en caso
        de que se despliegue.
        """
        if padre == None: return
        try:
            ajenas = [c for c in objeto.sqlmeta.columns 
                      if c.upper().endswith('ID')]
        except AttributeError:  # SQLObject > 0.6.1
            ajenas = [c for c in objeto.sqlmeta.columns
                      if c.upper().endswith('ID')]
        for ajena in ajenas:
            reg_ajena = ajena[:-2]
            obj_d = getattr(objeto, reg_ajena)
            itr = self.insertar_nombre(obj_d, padre, model, reg_ajena)
            model.append(itr, ("", "", "", ""))

    def insertar_multiples(self, objeto, padre, model):
        """
        Inserta un campo con desplegable por cada relación a muchos 
        del objeto, y dentro de éste tantos nombres de la tabla ajena
        como tuplas relacionadas que tenga.
        Además, por cada tupla creará un "child" vacío que se susituirá 
        por los datos de este registro cuando expanda la fila.
        """
        if padre == None: return
        multiples = objeto.sqlmeta.joins
        for multiple in multiples:
            lista_objs = getattr(objeto, multiple.joinMethodName)
            # print multiple.joinMethodName, lista_objs
            for obj_d in lista_objs:
                itr = self.insertar_nombre(obj_d, padre, model, multiple.otherClassName)
                model.append(itr, ("", "", "", ""))
    
    def expandir(self, tv, itr, path):
        model = tv.get_model()
        child = model[path].iterchildren().next()
        if child[0] == "" and \
           child[1] == "" and \
           child[2] == "" and \
           child[3] == "":
            model.remove(child.iter)
            ide = int(model[path][0])
            clase = model[path][-1]
#            print clase, ide
            try:
                objeto = eval('pclases.%s.get(%d)' % (clase, ide))
            except pclases.SQLObjectNotFound:
                utils.dialogo_info(titulo = "ERROR", texto = "El objeto %s con ID %d no existe." % (clase, ide))
            padre = model.get_iter(path)
            try:
                objeto.sync()
            except pclases.SQLObjectNotFound:
                model[path][0] = ""
                model[path][2] = ""
                model[path][3] = ""
            self.insertar_campos(objeto, padre, model)
            self.insertar_ajenos(objeto, padre, model)
            self.insertar_multiples(objeto, padre, model)
            tv.expand_row(path, False)

    def cerrar(self, tv, itr, path):
        model = tv.get_model()
        iterador = model[path].iterchildren()
        try:
            hijo = iterador.next()
            while (1):
                model.remove(hijo.iter)
                hijo = iterador.next()
        except StopIteration:
            pass
        model.append(itr, ("", "", "", ""))

    def cambiar_valor(self, cell, path, text):
        model = self.wids['tv_datos'].get_model()
        if model[path][0] == "":
            if model[path].parent != None:
                ide = model[path].parent[0]
                clase = model[path].parent[-1]
                campo = model[path][1]
                objeto = eval("pclases.%s.get(%d)" % (clase, int(ide)))
                objeto.syncUpdate()
                try:
                    try:
                        setattr(objeto, campo, text)
                    except Exception, inner_e:
                        try:
                            setattr(objeto, campo, utils._float(text))
                        except Exception, float_e:  # @UnusedVariable
                            try:
                                setattr(objeto, campo, int(text))
                            except Exception, int_e:  # @UnusedVariable
                                raise inner_e
                    model[path][2] = getattr(objeto, campo)
                except Exception, e:
                    utils.dialogo_info(titulo = "ERROR", 
                        texto = "Valor incorrecto para este campo."
                                "\n\n{0}".format(e), 
                        padre = self.wids['ventana'])
    
# XXX XXX XXX XXX XXX XXX

##!/usr/bin/env python
## -*- coding: utf-8 -*-

################################################################################
## Copyright (C) 2005-2008  Francisco José Rodríguez Bogado,                   #
##                          Diego Muñoz Escalante.                             #
## (pacoqueen@users.sourceforge.net, escalant3@users.sourceforge.net)          #
##                                                                             #
## This file is part of GeotexInn.                                             #
##                                                                             #
## GeotexInn is free software; you can redistribute it and/or modify           #
## it under the terms of the GNU General Public License as published by        #
## the Free Software Foundation; either version 2 of the License, or           #
## (at your option) any later version.                                         #
##                                                                             #
## GeotexInn is distributed in the hope that it will be useful,                #
## but WITHOUT ANY WARRANTY; without even the implied warranty of              #
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
## GNU General Public License for more details.                                #
##                                                                             #
## You should have received a copy of the GNU General Public License           #
## along with GeotexInn; if not, write to the Free Software                    #
## Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA  #
################################################################################


## Sacado de la página de Python Recipes (ASPN).
## Créditos a quien corresponda (ya lo buscaré).

#import pygtk
#pygtk.require('2.0')
#import gtk

#class Browser:
#    def make_row( self, piter, name, value ):
#        info = repr(value)
#        if not hasattr(value, "__dict__"):
#            if len(info) > 80:
#                # it's a big list, or dict etc. 
#                info = info[:80] + "..."
#        _piter = self.treestore.append( piter, [ name, type(value).__name__, info ] )
#        return _piter

#    def make_instance( self, value, piter ):
#        if hasattr( value, "__dict__" ):
#            for _name, _value in value.__dict__.items():
#                _piter = self.make_row( piter, "."+_name, _value )
#                _path = self.treestore.get_path( _piter )
#                self.otank[ _path ] = (_name, _value)

#    def make_mapping( self, value, piter ):
#        keys = []
#        if hasattr( value, "keys" ):
#            keys = value.keys()
#        elif hasattr( value, "__len__"):
#            keys = range( len(value) )
#        for key in keys:
#            _name = "[%s]"%str(key)
#            _piter = self.make_row( piter, _name, value[key] )
#            _path = self.treestore.get_path( _piter )
#            self.otank[ _path ] = (_name, value[key])

#    def make(self, name=None, value=None, path=None, depth=1):
#        if path is None:
#            # make root node
#            piter = self.make_row( None, name, value )
#            path = self.treestore.get_path( piter )
#            self.otank[ path ] = (name, value)
#        else:
#            name, value = self.otank[ path ]

#        piter = self.treestore.get_iter( path )
#        if not self.treestore.iter_has_child( piter ):
#            self.make_mapping( value, piter )
#            self.make_instance( value, piter )

#        if depth:
#            for i in range( self.treestore.iter_n_children( piter ) ):
#                self.make( path = path+(i,), depth = depth - 1 )

#    def row_expanded( self, treeview, piter, path ):
#        self.make( path = path )

#    def delete_event(self, widget, event, data=None):
#        gtk.main_quit()
#        return False

#    def __init__(self, name, value):
#        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
#        self.window.set_title("Browser")
#        self.window.set_size_request(512, 320)
#        self.window.connect("delete_event", self.delete_event)

#        # Nombre, tipo y __repr__ (los tres de tipo str): 
#        columns = [str,str,str]
#        self.treestore = gtk.TreeStore(*columns)

#        # otank es para saber qué objeto está en cada nodo del árbol
#        self.otank = {} # map path -> (name,value)
#        self.make( name, value )

#        self.treeview = gtk.TreeView(self.treestore)
#        self.treeview.connect("row-expanded", self.row_expanded )

#        self.tvcolumns = [ gtk.TreeViewColumn() for _type in columns ]
#        i = 0
#        for tvcolumn in self.tvcolumns:
#            self.treeview.append_column(tvcolumn)
#            cell = gtk.CellRendererText()
#            tvcolumn.pack_start(cell, True)
#            tvcolumn.add_attribute(cell, 'text', i)
#            i = i + 1

#        self.window.add(self.treeview)
#        self.window.show_all()

#def dump( name, value ):
#    browser = Browser( name, value )
#    gtk.main()

#def test():
#    class Nil:
#        pass
#    a = Nil()
#    b = Nil()
#    c = Nil()
#    d = Nil()
#    a.b=b
#    b.c=c
#    c.d=d
#    d.a=a # circular chain
#    dump( "a", a )

#if __name__ == "__main__":
#    test()
# XXX XXX XXX XXX XXX XXX

if __name__ == '__main__':
    t = Trazabilidad()
    #dump("Rollo", pclases.Rollo.select()[0])
    
