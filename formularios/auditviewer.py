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
## auditviewer.py - Visor amigable de la tabla de auditoría.
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 4 de marzo de 2013 -> Inicio
## 
###################################################################

import sys, os 
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, gobject
try:
    import pclases
except ImportError:
    from os.path import join as pathjoin
    sys.path.append(pathjoin("..", "framework"))
    import pclases
import mx, mx.DateTime

class AuditViewer(Ventana):
    """
    Visor de la tabla de auditoría de la aplicación.
    """
    def __init__(self, objeto = None, usuario = None, ventana_padre = None, 
                 locals_adicionales = {}):
        self.filtro = [""]
        try:
            Ventana.__init__(self, 'trazabilidad.glade', objeto)    
            # Me vale el mismo glade. Modificaré dinámicamente lo que me 
            # estorbe.
        except:     # Tal vez me estén llamando desde otro directorio
            Ventana.__init__(self, os.path.join('..', 'formularios', 
                             'trazabilidad.glade'), objeto, usuario)
        connections = {'b_salir/clicked': self._salir}
        self.add_connections(connections)
        self.wids['hbox1'].set_property("visible", False)
        cols = (('Usuario', 'gobject.TYPE_STRING', False, True, False, None),
                ('Ventana', 'gobject.TYPE_STRING', False, True, False, None),
                ('«puid»', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Acción', 'gobject.TYPE_STRING', False, True, False, None), 
                ('IP', 'gobject.TYPE_STRING', False, True, False, None), 
                ('«hostname»', 
                    'gobject.TYPE_STRING', False, True, False, None), 
                ('«fechahora»', 'gobject.TYPE_STRING', False, True, True, None),
                ('Descripción', 
                    'gobject.TYPE_STRING', False, True, False, None), 
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(self.wids['tv_datos'], cols)
        self.colorear(self.wids['tv_datos'])
        import pyconsole
        vars_locales = locals()
        for k in locals_adicionales:
            vars_locales[k] = locals_adicionales[k] 
        consola = pyconsole.attach_console(self.wids['contenedor_consola'], 
                                banner = "Consola python de depuración GINN", 
                                script_inicio = """import sys, os, pygtk, gtk, gtk.glade, utils
sys.path.append(os.path.join("..", "framework"))
import pclases, mx, mx.DateTime
dir()
""", 
                                locals = vars_locales)
        self.wids['frame2'].set_property("visible", False)
        self.wids['ventana'].set_title("AuditViewer")
        self.wids['ventana'].set_position(gtk.WIN_POS_CENTER)
        self.tamanno_audit = self.rellenar_widgets()
        try:
            self.wids['e_search'].set_property("primary-icon-stock", 
                gtk.STOCK_FIND)
            self.wids['e_search'].set_property("secondary-icon-stock", 
                gtk.STOCK_CLEAR)
            self.wids['e_search'].connect("icon-press", self.both_buttons)
        except TypeError:
            self.wids['e_search'].connect("changed", 
                                          self.mancatrlt2)
        self.wids['vbox1'].set_size_request(640, 480)
        self.wids['tv_datos'].set_size_request(-1, 350)
        self.wids['e_search'].grab_focus()
        self.wids['e_search'].set_text("!Alerta:")
        self.filtrar_tvaudit("!Alerta:")
        gobject.timeout_add(1000, self.check_audit)
        self.wids['ventana'].resize(800, 600)
        gtk.main()
    
    def mancatrlt2(self, entry):
        self.filtrar_tvaudit(entry.get_text())

    def both_buttons(self, entry, icon, event):
        if icon == gtk.ENTRY_ICON_PRIMARY:  # Buscar
            self.filtrar_tvaudit(entry.get_text())
        elif icon == gtk.ENTRY_ICON_SECONDARY:  # Limpiar
            entry.set_text("")
            self.filtrar_tvaudit(None)

    def filtrar_tvaudit(self, texto = None):
        """
        Guarda un filtro de búsqueda que ignora las líneas del audit que no 
        coicidan con el texto recibido. None si no se desea filtro.
        """
        if not texto:
            self.filtro = [""]
        else:
            self.filtro = [isinstance(i, str) 
                            and i.strip().lower() 
                            or `i`.strip().lower() 
                           for i in texto.split()]
        self.rellenar_widgets()
    
    def _salir(self, w):
        """
        Cierra el audit y sale.
        """
        self.salir(w)

    def colorear(self, tv):
        """
        Asocia una función al treeview para resaltar las acciones.
        """
        def cell_func(column, cell, model, itr, numcol):
            tipo = model[itr][3]
            if tipo == "create":
                color = "green"
            elif tipo == "drop":
                color = "red"
            elif tipo == "update": 
                color = "light blue"
            else:
                # Cualquier otra cosa 
                color = None
            #cell.set_property("cell-background", color)
            cell.set_property("background", color)

        cols = tv.get_columns()
        for i in xrange(len(cols)): 
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell, cell_func, i)

    def chequear_cambios(self):
        pass

    def es_diferente(self):
        return False

    def rellenar_widgets(self):
        """
        Vuelca el contenido del audit en el model.
        """
        model = self.wids['tv_datos'].get_model()
        self.wids['tv_datos'].freeze_child_notify()
        self.wids['tv_datos'].set_model(None)
        model.clear()
        last_iter = None
        lineas_auditoria = cargar_registros_auditoria()
        for linea in self.filtrar_lineas(lineas_auditoria):
            last_iter = self.agregar_linea(model, linea)
        self.wids['tv_datos'].set_model(model)
        self.wids['tv_datos'].thaw_child_notify()
        self.mover_a_ultima_fila(last_iter)
        tamanno = lineas_auditoria.count()
        return tamanno
    
    def check_audit(self):
        """
        Comprueba si ha cambiado el tamaño del audit y añade las 
        líneas nuevas.
        """
        lineas_auditoria = cargar_registros_auditoria() 
        if lineas_auditoria.count() > self.tamanno_audit:
            self.tamanno_audit = lineas_auditoria.count()
            try:
                for linea in self.filtrar_lineas(lineas_auditoria):
                    try:
                        last_iter = self.agregar_linea(
                            self.wids['tv_datos'].get_model(), linea)
                    except (AttributeError, KeyError), e:
                        self.logger.error("auditviewer::check_audit -> "
                            "Error al obtener el modelo del TreeView. "
                            "Probablemente se produjo una entrada en el audit "
                            "justo cuando se cerraba la ventana: %s" % e)
                        return False
                try:
                    self.mover_a_ultima_fila(last_iter)
                except UnboundLocalError:
                    pass    # No ha habido cambios en el fichero.
            except ValueError:
                return False    # Fichero cerrado. "Descargo" la función.
        return True

    def mover_a_ultima_fila(self, last_iter):
        """
        Mueve el TreeView a la última fila.
        """
        # sel = self.wids['tv_datos'].get_selection()
        # sel.select_iter(last_iter)
        model = self.wids['tv_datos'].get_model()
        try:
            self.wids['tv_datos'].scroll_to_cell(model.get_path(last_iter), 
                                                 use_align = True)
        except TypeError:   # last_iter no es un iter. Debe ser None.
            pass

    def agregar_linea(self, model, linea):
        """
        Inserta en el model la línea recibida.
        """
        return model.append((linea.usuario and linea.usuario.usuario or "", 
                             linea.ventana and linea.ventana.fichero or "", 
                             linea.puid, 
                             linea.action, 
                             linea.ip, 
                             linea.hostname, 
                             linea.fechahora.strftime("%Y%m%d %H%M%S"), 
                             linea.descripcion, 
                             linea.get_puid()))

    def filtrar_lineas(self, select_query):
        """
        Iterador que devuelve una línea del audit cada vez en forma de 
        objeto de pclases:
        Filtra las duplicadas consecutivas para devolverlas una única vez.
        Tiene en cuenta también el filtro de búsqueda.
        """
        linea_anterior = None
        for linea in select_query:
            if linea != linea_anterior:
                ver = False
                for p in self.filtro:
                    if p.startswith("!"):
                        ver = ver or (p[1:] not in linea.get_info().lower())
                    else:
                        ver = ver or (p in linea.get_info().lower())
                if not ver:
                    continue
                linea_anterior = linea
                yield linea
        raise StopIteration


def cargar_registros_auditoria():
    return pclases.Auditoria.select(orderBy = "id")

if __name__ == '__main__':
    t = AuditViewer()

