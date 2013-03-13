#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2013  Francisco José Rodríguez Bogado,                   #
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
## logviewer.py - Visor de logs de GINN.
###################################################################
## NOTAS:
##  
## ----------------------------------------------------------------
## TODO: Permitir cargar otro fichero de log diferente al actual.
###################################################################
## Changelog:
## 2 de febrero de 2007 -> Inicio
## 7 de febrero de 2007 -> Fully functional!
## 
###################################################################
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
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    import pclases
import mx, mx.DateTime

class LogViewer(Ventana):
    """
    Visor de logs de la aplicación.
    """
    def __init__(self, objeto = None, usuario = None, ventana_padre = None, locals_adicionales = {}, fichero_log = "ginn.log"):
        self.fichero_log = fichero_log
        self.filtro = [""]
        try:
            Ventana.__init__(self, 'trazabilidad.glade', objeto)    
            # Me vale el mismo glade. Modificaré dinámicamente lo que me 
            # estorbe.
        except:     # Tal vez me estén llamando desde otro directorio
            Ventana.__init__(self, os.path.join('..', 'formularios', 'trazabilidad.glade'), objeto)
        connections = {'b_salir/clicked': self._salir}
        self.add_connections(connections)
        self.wids['hbox1'].set_property("visible", False)
        cols = (('Fecha', 'gobject.TYPE_STRING', False, True, True, None),
                ('Hora', 'gobject.TYPE_STRING', False, True, False, None),
                ('Tipo', 'gobject.TYPE_STRING', False, True, False, None),
                ('Usuario', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Texto', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Línea', 'gobject.TYPE_INT64', False, False, False, None))
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
        self.wids['ventana'].set_title("LogViewer")
        self.wids['ventana'].resize(800, 600)
        self.wids['ventana'].set_position(gtk.WIN_POS_CENTER)
        self.wids['vpaned1'].set_position(500)
        self.tamanno_log = self.rellenar_widgets()
        gobject.timeout_add(1000, self.check_log)
        try:
            self.wids['e_search'].set_property("primary-icon-stock", 
                gtk.STOCK_FIND)
            self.wids['e_search'].set_property("secondary-icon-stock", 
                gtk.STOCK_CLEAR)
            self.wids['e_search'].connect("icon-press", self.both_buttons)
        except TypeError:
            self.wids['e_search'].connect("changed", 
                                          self.mancatrlt2)
        gtk.main()
    
    def mancatrlt2(self, entry):
        self.filtrar_tvlog(entry.get_text())

    def both_buttons(self, entry, icon, event):
        if icon == gtk.ENTRY_ICON_PRIMARY:  # Buscar
            self.filtrar_tvlog(entry.get_text())
        elif icon == gtk.ENTRY_ICON_SECONDARY:  # Limpiar
            entry.set_text("")
            self.filtrar_tvlog(None)

    def filtrar_tvlog(self, texto = None):
        """
        Guarda un filtro de búsqueda que ignora las líneas del log que no 
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
        Cierra el log y sale.
        """
        self.cerrar_log(self.log)
        self.salir(w)

    def colorear(self, tv):
        """
        Asocia una función al treeview para resaltar los partes pendientes 
        de verificar.
        """
        def cell_func(column, cell, model, itr, numcol):
            """
            Si la fila corresponde a un parte de producción no verificado, 
            lo colorea en rojo oscuro, si no, lo hace en verde oscuro.
            """
            tipo = model[itr][2]
            texto = model[itr][4]
            if tipo == "DEBUG": 
                # Información de depuración.
                color = "light grey"
            elif "login" in texto.lower():
                # LOGIN con éxito.
                color = "orange"
            elif "Acceso err" in texto:
                # LOGIN fallido.
                color = "indian red"
            elif "logout" in texto.lower():
                # LOGOUT.
                color = "yellow4"
            elif "CONSUMO" in texto and "FIBRA" in texto:
                # Consumo de línea de fibra.
                color = "HotPink1"
            elif "PARTE" in texto and "Consumiendo" in texto:
                # Consumo de línea de geotextiles.
                color = "HotPink3"
            elif "Cargar:" in texto:
                # Abrir una ventana.
                color = "medium spring green"
            elif tipo == "WARNING":
                # WARNING que no entre en ningún caso anterior.
                color = "light green"
            elif tipo == "ERROR":
                # ERROR.
                color = "red"
            elif tipo == "INFO":
                # INFO que no entre en ningún caso anterior.
                color = "light blue"
            else:
                # Cualquier otra cosa (líneas de una entrada multilínea, etc...)
                color = "white" 
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
        Vuelca el contenido del log en el model.
        """
        self.log = self.abrir_log()
        model = self.wids['tv_datos'].get_model()
        self.wids['tv_datos'].freeze_child_notify()
        self.wids['tv_datos'].set_model(None)
        model.clear()
        last_iter = None
        if self.log != None:
            for linea in self.filtrar_lineas(self.log):
                last_iter = self.agregar_linea(model, linea)
            # self.cerrar_log(log)
        else:
            self.mostrar_error(model)
        self.agregar_eof(model)
        self.wids['tv_datos'].set_model(model)
        self.wids['tv_datos'].thaw_child_notify()
        self.mover_a_ultima_fila(last_iter)
        tamanno = os.path.getsize(self.fichero_log)
        return tamanno
    
    def check_log(self):
        """
        Comprueba si ha cambiado el tamaño del log y añade las 
        líneas nuevas.
        """
        if os.path.getsize(self.fichero_log) > self.tamanno_log:
            self.tamanno_log = os.path.getsize(self.fichero_log)
            try:
                for linea in self.filtrar_lineas(self.log):
                    try:
                        last_iter = self.agregar_linea(
                            self.wids['tv_datos'].get_model(), linea)
                    except (AttributeError, KeyError), e:
                        self.logger.error("logviewer::check_log -> "
                            "Error al obtener el modelo del TreeView. "
                            "Probablemente se produjo una entrada en el log "
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

    def agregar_eof(self, model):
        """
        Añade una línea de fin de fichero al model.
        DEPRECATED.
        """
        pass

    def mostrar_error(self, model):
        """
        Inserta en el model un mensaje de error.
        """
        model.append(("", "", "", "", "", -1))

    def agregar_linea(self, model, linea):
        """
        Inserta en el model la línea recibida.
        """
        fecha = utils.str_fecha(linea[0])
        hora = utils.str_hora(linea[1])
        tipo = linea[2]
        usuario = linea[3]
        texto = linea[4]
        numlinea = linea[5]
        return model.append((fecha, hora, tipo, usuario, texto, numlinea))

    def cerrar_log(self, log):
        """
        Cierra el archivo de log.
        """
        log.close()    
        
    def filtrar_lineas(self, f):
        """
        Iterador que devuelve una línea del log cada vez en forma de 
        lista:
        [fecha, hora, tipo, usuario, texto, número de línea]
        Filtra las duplicadas consecutivas para devolverlas una única vez.
        Tiene en cuenta también el filtro de búsqueda.
        """
        fecha = None
        hora = None
        tipo = ""
        usuario = ""
        texto = ""
        numlinea = 0
        linea_anterior = ""
        for linea in f.readlines():
            if linea != linea_anterior:
                ver = False
                for p in self.filtro:
                    ver = ver or (p in linea.lower())
                if not ver:
                    continue
                fecha = self.obtener_fecha(linea, fecha)
                hora = self.obtener_hora(linea, fecha, hora)
                tipo = self.obtener_tipo(linea, tipo)
                usuario = self.obtener_usuario(linea, usuario)
                texto = self.obtener_texto(linea, texto, tipo, usuario)
                numlinea += 1
                linea_anterior = linea
                yield [fecha, hora, tipo, usuario, texto, numlinea]
        raise StopIteration

    def obtener_texto(self, linea, texto_anterior, tipo, usuario = ""):
        """
        Devuelve el texto de la línea que venga a continuación 
        del tipo.
        """
        try:
            texto = linea[linea.index(tipo) + len(tipo):]
        except ValueError:
            texto = linea
        if usuario != "":
            texto = texto.replace(usuario, "", 1)
        texto = texto.replace("\n", " ").replace("\r", " ")
        try:
            texto = reduce(lambda x, y: x[-1] == " " and y == " " and x or x+y, texto)    # Elimino los espacios de más.
        except TypeError:
            pass    # texto es "" (vacío), None (no es iterable) o algo así.
        return texto

    def obtener_tipo(self, linea, tipo_anterior):
        """
        Devuelve el tipo de línea del log.
        Si no tiene, devuelve el tipo_anterior.
        """
        try:
            tipo = linea.split(" ")[2]
        except:
            tipo = tipo_anterior
        return tipo
    
    def obtener_usuario(self, linea, usuario_anterior):
        """
        Devuelve el usuario de línea del log.
        Si no tiene, devuelve "".
        """
        try:
            usuario = linea.split(" ")[3]
            if not usuario.endswith(":") or "LOGOUT" in usuario.upper():
                usuario = ""
        except IndexError:
            usuario = ""
        return usuario.replace(":", "")

    def obtener_hora(self, linea, fecha, hora_anterior):
        """
        Devuelve la hora de la línea (con la fecha incluida). 
        Si no tiene, devuelve la hora anterior. Si la hora 
        anterior es None, devuelve la época.
        PRECONDICIÓN: fecha no puede ser None.
        POSTCONDICIÓN: Se devuelve una fecha válida.
        """
        hora = mx.DateTime.Epoch
        try:
            hora_str = linea.split()[1]
            horas, minutos = map(int, hora_str.split(":")[:2])
            segundos = hora_str.split(":")[2]
            segundos, centesimas = map(int, segundos.split(","))
            dia = fecha.day
            mes = fecha.month
            anno = fecha.year
            hora = mx.DateTime.DateTimeFrom(day = dia, month = mes, year = anno, hour = horas, minute = minutos, second = segundos)
        except:
            if hora_anterior != None:
                hora = hora_anterior
        return hora


    def obtener_fecha(self, linea, fecha_anterior):
        """
        Devuelve la fecha que encabeza la línea. Si no tiene fecha, 
        devuelve la fecha anterior. Si fecha_anterior no es una 
        fecha válida, devuelve la época.
        POSCONDICIÓN: Se devuelve una fecha válida.
        """
        fecha = mx.DateTime.Epoch
        try:
            fecha_str = linea.split()[0]
            anno, mes, dia = map(int, fecha_str.split("-"))
            fecha = mx.DateTime.DateTimeFrom(day = dia, month = mes, year = anno)
        except:
            if fecha_anterior:
                fecha = fecha_anterior
        return fecha

    def abrir_log(self):
        """
        Abre el fichero del log y devuelve el objeto que lo encapsula.
        Si el archivo es muy grande, se posiciona en el primer salto 
        de línea del último mega (o el tamaño que se especifique).
        """
        MAX_SIZE = 2 * 1024 * 1024  
        # Dos megas de info es mucha info (menos de una semana en realidad en 
        # las máquinas de producción).
        import os
        try:
            f = open(self.fichero_log, "r")
            if os.path.getsize(self.fichero_log) > MAX_SIZE:
                f.seek(-MAX_SIZE, 2)
                while f.read(1) not in "\n\r":
                    pass
                if f.read(1) not in "\n\r":
                    f.seek(-1, 1)
        except IOError:
            f = None
        return f

if __name__ == '__main__':
    t = LogViewer()

