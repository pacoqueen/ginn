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
## partes_de_trabajo.py - Partes de trabajo de NO producción. 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 28 de mayo de 2006 -> Inicio
## 25 de julio de 2006 -> Añadido calendario laboral
## 31 de julio de 2006 -> Añadido soporte para abrir por una fecha
##                        determinada (obtenida de un parte).
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time
from framework import pclases
from informes import geninformes
import time, mx, mx.DateTime
from utils import _float as float


class PartesDeTrabajo(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto). De no ser None, debe ser un 
        parte, y se mostrará la fecha correspondiente a ese parte.
        """
        self.usuario = usuario
        Ventana.__init__(self, 'partes_de_trabajo.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_add/clicked': self.add,
                       'b_drop/clicked': self.drop
                      }
        self.add_connections(connections)
        self.partes = []
        self.inicializar_ventana(objeto)
        gtk.main()

    # --------------- Funciones auxiliares ------------------------------
    def cambiar_por_combo(self, tv, numcol):
        import gobject
        # Elimino columna actual
        column = tv.get_column(numcol)
        column.clear()
        # Creo model para el CellCombo
        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT64)
        for centro in pclases.CentroTrabajo.select():
            model.append((centro.nombre, centro.id))
        # Creo CellCombo
        cellcombo = gtk.CellRendererCombo()
        cellcombo.set_property("model", model)
        cellcombo.set_property("text-column", 0)
        cellcombo.set_property("editable", True)
        cellcombo.set_property("has-entry", False)
        # Función callback para la señal "editado"
        def guardar_combo(cell, path, text, model_tv, numcol, model_combo):
            # Es lento, pero no encuentro otra cosa:
            idct = None
            for i in xrange(len(model_combo)):
                texto, id = model_combo[i]
                if texto == text:
                    idct = id
                    break
            if idct == None:
                utils.dialogo_info(titulo = "ERROR CENTRO TRABAJO", texto = "Ocurrió un error inesperado guardando centro de trabajo.\n\nContacte con los desarrolladores de la aplicación\n(Vea el diálogo «Acerca de...» desde el menú de la aplicación.)", padre = self.wids['ventana'])
            else:
                ct = pclases.CentroTrabajo.get(idct)
                model_tv[path][numcol] = text
                parte = pclases.ParteDeTrabajo.get(model_tv[path][-1])
                parte.centroTrabajo = ct
        cellcombo.connect("edited", guardar_combo, tv.get_model(), numcol, model)
        column.pack_start(cellcombo)
        column.set_attributes(cellcombo, text = numcol)

    def crear_listview(self, tv):
        cols = (('Nombre', 'gobject.TYPE_STRING', False, True, False, None),
                ('Apellidos', 'gobject.TYPE_STRING', False, True, True, None), 
                ('H. entrada', 'gobject.TYPE_STRING', True, True, False, self.cambiar_horainicio), 
                ('H. salida', 'gobject.TYPE_STRING', True, True, False, self.cambiar_horafin), 
                ('Duración', 'gobject.TYPE_STRING', True, True, False, self.cambiar_horas), 
                ('Trabajo realizado', 'gobject.TYPE_STRING', True, True, False, self.cambiar_trabajo), 
                ('Centro de trabajo', 'gobject.TYPE_STRING', False, True, False, None), 
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(tv, cols)
        self.cambiar_por_combo(tv, 6)

    def crear_listview_calendario(self, tv):
        cols = (('Nombre', 'gobject.TYPE_STRING', False, True, False, None),
                ('Apellidos', 'gobject.TYPE_STRING', False, True, True, None), 
                ('Grupo', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Cat. laboral', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Centro de trabajo', 'gobject.TYPE_STRING', False, True, False, None), 
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(tv, cols)
        tv.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        tv.connect('row-activated', self.abrir_calendario)

    def abrir_calendario(self, tv, path, vc):
        model = tv.get_model()
        empleadoid = model[path][-1]
        empleado = pclases.Empleado.get(empleadoid)
        ldp = empleado.categoriaLaboral.lineaDeProduccion
        fecha_sel = list(self.wids['cal'].get_date())
        fecha_sel[1] += 1   # En los gtk.Calendar el mes empieza en 0
        anno = fecha_sel[0]
        mes = fecha_sel[1] 
        # TODO: De momento abre el calendario pero siempre en solo-lectura
        import calendario_laboral
        ventana_calendario_laboral = calendario_laboral.CalendarioLaboral(mes = mes, 
                                                                          anno = anno, 
                                                                          ldp = ldp, 
                                                                          solo_lectura = True)

    def inicializar_ventana(self, objeto = None):
        """
        Inicializa los widgets de la ventana.
        """
        self.crear_listview(self.wids['tv_horas'])
        self.crear_listview_calendario(self.wids['tv_calendario'])
        self.wids['tv_horas'].get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        self.wids['cal'].connect('day-selected', self.cambiar_fecha)
        if objeto == None:
            self.wids['cal'].select_month(time.localtime()[1]-1, time.localtime()[0])
            self.wids['cal'].select_day(time.localtime()[2])
        else:
            dia = objeto.horainicio.day
            mes = objeto.horainicio.month
            anno = objeto.horainicio.year
            self.wids['cal'].select_month(mes-1, anno)
            self.wids['cal'].select_day(dia)
        self.rellenar_tabla()
        self.rellenar_tabla_calendario()

    def rellenar_tabla(self):
        model = self.wids['tv_horas'].get_model()
        model.clear()
        fecha_sel = list(self.wids['cal'].get_date())
        fecha_sel[1] += 1   # En los gtk.Calendar el mes empieza en 0
        fechaini = "%d-%d-%d" % (fecha_sel[0], fecha_sel[1], fecha_sel[2])
        fechafin = mx.DateTime.DateTimeFrom(year = fecha_sel[0], month = fecha_sel[1], day = fecha_sel[2]) + mx.DateTime.oneDay
        # fechafin = "%d-%d-%d" % (fecha_sel[0], fecha_sel[1], fecha_sel[2]+1)    # Formato yyyy-mm-dd
        fechafin = fechafin.strftime('%Y-%m-%d')
        self.partes = pclases.ParteDeTrabajo.select("""horainicio >= '%s' AND horainicio < '%s' """ % (fechaini, fechafin))
        for parte in self.partes:
            model.append((parte.empleado.nombre, 
                          parte.empleado.apellidos, 
                          parte.horainicio.strftime('%H:%M'), 
                          parte.horafin.strftime('%H:%M'), 
                          parte.horas.strftime('%H:%M'), 
                          parte.trabajo, 
                          parte.centroTrabajo and parte.centroTrabajo.nombre or "", 
                          parte.id))

    def rellenar_tabla_calendario(self):
        model = self.wids['tv_calendario'].get_model()
        model.clear()
        fecha_sel = list(self.wids['cal'].get_date())
        fecha_sel[1] += 1   # En los gtk.Calendar el mes empieza en 0
        fechaini = mx.DateTime.DateTimeFrom(year = fecha_sel[0], month = fecha_sel[1], day = fecha_sel[2])
        turnos_de_recuperacion = pclases.Turno.select(pclases.Turno.q.recuperacion == True)
        laborables = []
        for turno in turnos_de_recuperacion:
            laborables_turno = pclases.Laborable.select(pclases.AND(pclases.Laborable.q.fecha == fechaini, 
                                                                    pclases.Laborable.q.turnoID == turno.id))
            for l in laborables_turno:
                laborables.append(l)
        for l in laborables:
            for empleado in l.empleados:
                if empleado != None and empleado not in [p.empleado for p in self.partes]:
                    model.append((empleado.nombre,
                                  empleado.apellidos,
                                  empleado.grupo and "%s [%s]" % (empleado.get_grupo_and_rol()) or "",
                                  empleado.categoriaLaboral and empleado.categoriaLaboral.codigo or "",
                                  empleado.centroTrabajo and empleado.centroTrabajo.nombre or "",
                                  empleado.id))

    def add_empleado(self):
        empleados = pclases.Empleado.select(orderBy = 'apellidos')
        empleados = [(e.id, e.nombre, e.apellidos) for e in empleados \
                        if e.activo and (e.planta or (e.categoriaLaboral and e.categoriaLaboral.lineaDeProduccion))]
        ids = utils.dialogo_resultado(filas = empleados, 
                                      titulo = 'SELECCIONE EMPLEADOS', 
                                      cabeceras = ('ID', 'Nombre', 'Apellidos'),
                                      multi = True)
        if ids == [-1]:
            return
        for id in ids:
            try:
                e = pclases.Empleado.get(id)
                self.add_empleado_a_parte(e)
            except pclases.SQLObjectNotFound:
                utils.dialogo_info(titulo = 'NÚMERO INCORRECTO', 
                                   texto = 'El empleado con código identificador %d no existe o no se pudo agregar.' % id)

    def add_empleados(self, empleados):
        for e in empleados:
            self.add_empleado_a_parte(e)

    def add_empleado_a_parte(self, e):
        fecha_sel = list(self.wids['cal'].get_date())
        fecha_sel[1] += 1   # En los gtk.Calendar el mes empieza en 0
        hora = mx.DateTime.DateTimeFrom(year = fecha_sel[0], 
                                        month = fecha_sel[1], 
                                        day = fecha_sel[2],
                                        hour = 6,
                                        minute = 0,
                                        second = 0)
        pt = pclases.ParteDeTrabajo(empleado = e, 
                                    horainicio = hora, 
                                    horafin = hora + (mx.DateTime.oneHour * 8), 
                                    trabajo = '', 
                                    centroTrabajo = e.centroTrabajo)
        pclases.Auditoria.nuevo(pt, self.usuario, __file__)

    # --------------- Manejadores de eventos ----------------------------
    def add(self, w):
        model, paths = self.wids['tv_calendario'].get_selection().get_selected_rows()
        if paths == []:
            self.add_empleado()
        else:
            self.add_empleados([pclases.Empleado.get(model[path][-1]) for path in paths])
        self.rellenar_tabla()
        self.rellenar_tabla_calendario()
    
    def drop(self, w):
        if self.wids['tv_horas'].get_selection().count_selected_rows() == 0:
            return
        model, paths = self.wids['tv_horas'].get_selection().get_selected_rows()
        for path in paths:
            id = model[path][-1] # El id de empleado es la columna 0
            pdt = pclases.ParteDeTrabajo.get(id)
            pdt.destroy(ventana = __file__)
        self.rellenar_tabla()
        self.rellenar_tabla_calendario()

    def cambiar_fecha(self, cal):
        self.rellenar_tabla()
        self.rellenar_tabla_calendario()
        self.bloquear_partes_antiguos()
    
    def bloquear_partes_antiguos(self):
        """
        Si el parte seleccionado (el día del calendario) es anterior 
        a 4 días a partir de hoy, se muestra como bloqueado automáticamente
        a no ser que el usuario tenga privilegios suficientes.
        """
        # NOTA: "Bloqueo" partes de trabajo automáticamente 4 días más tarde.
        fecha_sel = list(self.wids['cal'].get_date())
        fecha_sel[1] += 1   # En los gtk.Calendar el mes empieza en 0
        fechafin = mx.DateTime.DateTimeFrom(year = fecha_sel[0], month = fecha_sel[1], day = fecha_sel[2]) + mx.DateTime.oneDay
        if (abs(mx.DateTime.localtime() - fechafin) >= mx.DateTime.oneDay * 4 
            and self.usuario and self.usuario.nivel > 1):
            bloqueado = True
        else:
            bloqueado = False
        self.wids['tv_horas'].set_sensitive(not bloqueado)
        self.wids['b_add'].set_sensitive(not bloqueado)
        self.wids['b_drop'].set_sensitive(not bloqueado)

        
    def cambiar_horafin(self, tv, path, newtext):
        model = self.wids['tv_horas'].get_model()
        id = model[path][-1]
        pt = pclases.ParteDeTrabajo.get(id)
        try:
            dtdelta = mx.DateTime.DateTimeDelta(0, float(newtext.split(':')[0]), float(newtext.split(':')[1]), 0)
            pt.horafin = mx.DateTime.DateTimeFrom(year = pt.horafin.year,
                                                  month = pt.horafin.month,
                                                  day = pt.horafin.day,
                                                  hour = dtdelta.hour,
                                                  minute = dtdelta.minute,
                                                  second = dtdelta.second)
            if pt.horafin < pt.horainicio:
                pt.horafin = pt.horafin + mx.DateTime.oneDay
            pt.sync()
            model[path][3] = pt.horafin.strftime('%H:%M')
            model[path][4] = pt.horas.strftime('%H:%M')
        except IndexError:
            utils.dialogo_info(titulo = "ERROR", 
                               texto = 'El texto "%s" no respeta el formato horario (H:MM).' % newtext,
                               padre = self.wids['ventana'])
        except ValueError:
            utils.dialogo_info(titulo = "ERROR", 
                               texto = 'El texto "%s" no respeta el formato horario (H:M).' % newtext,
                               padre = self.wids['ventana'])

    def cambiar_horainicio(self, tv, path, newtext):
        model = self.wids['tv_horas'].get_model()
        id = model[path][-1]
        pt = pclases.ParteDeTrabajo.get(id)
        try:
            dtdelta = mx.DateTime.DateTimeDelta(0, float(newtext.split(':')[0]), float(newtext.split(':')[1]), 0)
            duracion = pt.horas
            pt.horainicio = mx.DateTime.DateTimeFrom(year = pt.horainicio.year,
                                                     month = pt.horainicio.month,
                                                     day = pt.horainicio.day,
                                                     hour = dtdelta.hour,
                                                     minute = dtdelta.minute,
                                                     second = dtdelta.second)
            pt.horafin = pt.horainicio + duracion
            pt.sync()
            model[path][2] = pt.horainicio.strftime('%H:%M')
            model[path][3] = pt.horafin.strftime('%H:%M')
            model[path][4] = pt.horas.strftime('%H:%M')
        except IndexError:
            utils.dialogo_info(titulo = "ERROR", 
                               texto = 'El texto "%s" no respeta el formato horario (H:MM).' % newtext,
                               padre = self.wids['ventana'])
        except ValueError:
            utils.dialogo_info(titulo = "ERROR", 
                               texto = 'El texto "%s" no respeta el formato horario (H:M).' % newtext,
                               padre = self.wids['ventana'])

    def cambiar_horas(self, tv, path, newtext):
        model = self.wids['tv_horas'].get_model()
        id = model[path][-1]
        pt = pclases.ParteDeTrabajo.get(id)
        try:
            dtdelta = mx.DateTime.DateTimeDelta(0, float(newtext.split(':')[0]), float(newtext.split(':')[1]), 0)
            pt.horafin = pt.horainicio + dtdelta
            pt.sync()
            model[path][4] = (pt.horafin - pt.horainicio).strftime('%H:%M')
            model[path][3] = pt.horafin.strftime('%H:%M')
        except IndexError:
            utils.dialogo_info(titulo = "ERROR", 
                               texto = 'El texto "%s" no respeta el formato horario (H:MM).' % newtext,
                               padre = self.wids['ventana'])
        except ValueError:
            utils.dialogo_info(titulo = "ERROR", 
                               texto = 'El texto "%s" no respeta el formato horario (H:M).' % newtext,
                               padre = self.wids['ventana'])

    def cambiar_trabajo(self, cell, path, texto):
        # DONE: Desplegable:
        # ... ¿Desplegable? ¿Seguro? ¿Con qué opciones? 
        # Iba a ser un desplegable según las specs, pero al final es texto libre.
        model = self.wids['tv_horas'].get_model()
        id = model[path][-1]
        pdt = pclases.ParteDeTrabajo.get(id)
        pdt.trabajo = texto
        model[path][5] = texto
    

if __name__=='__main__':
    a = PartesDeTrabajo()

