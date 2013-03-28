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
import gtk, gtk.glade, time, gobject, pango
try:
    import pclases
except ImportError:
    from os.path import join as pathjoin
    sys.path.append(pathjoin("..", "framework"))
    import pclases
import mx, mx.DateTime
from consulta_existenciasBolsas import act_fecha 
from dynconsulta import restar_mes

pclases.DEBUG = True    # XXX

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
        connections = {'b_salir/clicked': self._salir, 
                       'b_fechaini/clicked': self.set_fecha, 
                       'b_fechafin/clicked': self.set_fecha, 
                       'e_fechaini/focus-out-event': act_fecha, 
                       'e_fechafin/focus-out-event': act_fecha, 
                       'b_atras/clicked': self.move_fecha, 
                       'b_adelante/clicked': self.move_fecha, 
                       'b_actualizar/clicked': self.rellenar_widgets}
        self.add_connections(connections)
        self.wids['e_fechaini'].set_text(utils.str_fecha(
            restar_mes(mx.DateTime.today())))
        self.wids['hbox1'].set_property("visible", False)
        self.wids['filtro_fecha'].set_visible(True)
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
        self.rellenar_widgets()
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
        self.signal_check = gobject.timeout_add(5000, self.check_audit)
        self.wids['ventana'].resize(800, 600)
        gtk.main()
    
    def set_fecha(self, boton):
        """
        Cambia la fecha de los filtros.
        """
        w = self.wids[boton.name.replace("b_", "e_")]
        try:
            fechaentry = utils.parse_fecha(w.get_text())
        except (TypeError, ValueError):
            fechaentry = mx.DateTime.today()
        w.set_text(utils.str_fecha(utils.mostrar_calendario(
                                                fecha_defecto = fechaentry, 
                                                padre = self.wids['ventana'])))

    def move_fecha(self, boton):
        for entry_name in ("e_fechaini", "e_fechafin"):
            w = self.wids[entry_name]
            try:
                fechaentry = utils.parse_fecha(w.get_text())
            except (TypeError, ValueError):
                fechaentry = mx.DateTime.today()
            if boton.name == "b_atras":
                nueva_fecha = restar_mes(fechaentry) 
            else:
                nueva_fecha = restar_mes(fechaentry, -1)
            w.set_text(utils.str_fecha(nueva_fecha))

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
                # Aprovecho para cambiar el tamaño de la fuente:
                cell.set_property("font-desc", pango.FontDescription("sans 7"))

    def chequear_cambios(self):
        pass

    def es_diferente(self):
        return False

    def rellenar_widgets(self, boton = None):
        """
        Vuelca el contenido del audit en el model.
        """
        if pclases.DEBUG: print __file__, "rellenar_widgets: 0" 
        try:
            gobject.source_remove(self.signal_check)
        except AttributeError:
            timeout_unloaded = False
        else:
            timeout_unloaded = True
        if pclases.DEBUG: print __file__, "rellenar_widgets: 1" 
        model = self.wids['tv_datos'].get_model()
        self.wids['tv_datos'].freeze_child_notify()
        self.wids['tv_datos'].set_model(None)
        model.clear()
        last_iter = None
        if pclases.DEBUG: print __file__, "rellenar_widgets: 2" 
        lineas_auditoria = self.cargar_registros_auditoria()
        if pclases.DEBUG: print __file__, "rellenar_widgets: 3" 
        self.lines_added = []
        for linea in self.filtrar_lineas(lineas_auditoria):
            if pclases.DEBUG: print __file__, "rellenar_widgets: 31" 
            last_iter = self.agregar_linea(model, linea)
            if pclases.DEBUG: print __file__, "rellenar_widgets: 32" 
        self.wids['tv_datos'].set_model(model)
        self.wids['tv_datos'].thaw_child_notify()
        if pclases.DEBUG: print __file__, "rellenar_widgets: 4" 
        self.mover_a_ultima_fila(last_iter)
        if pclases.DEBUG: print __file__, "rellenar_widgets: 5" 
        tamanno = lineas_auditoria.count()
        self.tamanno_audit = tamanno
        if timeout_unloaded: # Si la he descargado (usuario ha actualizado) 
                             # vuelvo a cargarla.
            self.signal_check = gobject.timeout_add(5000, self.check_audit)
        if pclases.DEBUG: print __file__, "rellenar_widgets: 6" 
    
    def check_audit(self):
        """
        Comprueba si ha cambiado el tamaño del audit y añade las 
        líneas nuevas.
        """
        gobject.source_remove(self.signal_check)
        lineas_auditoria = self.cargar_registros_auditoria() 
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
                    else:
                        self.mover_a_ultima_fila(last_iter)
            except ValueError:
                return False    # Fichero cerrado. "Descargo" la función.
        self.signal_check = gobject.timeout_add(5000, self.check_audit)

    def mover_a_ultima_fila(self, last_iter):
        """
        Mueve el TreeView a la última fila.
        """
        # sel = self.wids['tv_datos'].get_selection()
        # sel.select_iter(last_iter)
        sel = self.wids['tv_datos'].get_selection()
        model, selected = sel.get_selected()
        # Me muevo al final si ya estaba en el final o si no estoy  
        # investigando nada (no tengo nada seleccionado en el treeview).
        vscroll=self.wids['tv_datos'].parent.get_vscrollbar().get_adjustment()
        pos_scroll = vscroll.value
        abajo = vscroll.upper - vscroll.page_size
        if not selected or pos_scroll == abajo:
            try:
                self.wids['tv_datos'].scroll_to_cell(model.get_path(last_iter),
                                                     use_align = True)
            except TypeError:   # last_iter no es un iter. Debe ser None.
                pass

    def agregar_linea(self, model, linea):
        """
        Inserta en el model la línea recibida.
        """
        lpuid = linea.get_puid()
        if lpuid not in self.lines_added:
            added = model.append(
                            (linea.usuario and linea.usuario.usuario or "", 
                             linea.ventana and linea.ventana.fichero or "", 
                             linea.puid, 
                             linea.action, 
                             linea.ip, 
                             linea.hostname, 
                             linea.fechahora.strftime("%Y%m%d %H%M%S"), 
                             linea.descripcion, 
                             linea.get_puid()))
            self.lines_added.append(lpuid)
            return added

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

    def cargar_registros_auditoria(self):
        if pclases.DEBUG: print __file__, "cargar_registros_auditoria: 0" 
        try:
            fechaini = utils.parse_fecha(self.wids['e_fechaini'].get_text())
        except ValueError:
            fechaini = None
        try:
            fechafin = (utils.parse_fecha(self.wids['e_fechafin'].get_text())
                        + mx.DateTime.oneDay)
        except ValueError:
            fechafin = None
        if pclases.DEBUG: print __file__, "cargar_registros_auditoria: 1" 
        if fechaini and fechafin:
            res = pclases.Auditoria.select(pclases.AND(
                    pclases.Auditoria.q.fechahora >= fechaini, 
                    pclases.Auditoria.q.fechahora < fechafin), 
                orderBy = "id")
        elif fechaini and not fechafin:
            res = pclases.Auditoria.select(
                pclases.Auditoria.q.fechahora >= fechaini, 
                orderBy = "id")
        elif not fechaini and fechafin:
            res = pclases.Auditoria.select(
                pclases.Auditoria.q.fechahora < fechafin, 
                orderBy = "id")
        else:
            res = pclases.Auditoria.select(orderBy = "id")
        if pclases.DEBUG: print __file__, "cargar_registros_auditoria: 2" 
        return res



if __name__ == '__main__':
    t = AuditViewer()

