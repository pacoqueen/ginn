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
## horas_trabajadas.py - Consulta de horas trabajadas.
###################################################################
## NOTAS:
## El cálculo de horas se ha copiado directamente de 
## horas_trabajadas.py.
## 
###################################################################
## Changelog:
## 31 de julio de 2006 -> Inicio
## 
## 
###################################################################
# TODO: Con versiones modernas de SQLObject, las horas de los partes vienen 
# como datetime y no pueden operar con los mx.DateTime.

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
import mx.DateTime
import datetime

class Nominas(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        """
        Ventana.__init__(self, 'nominas.glade', objeto, usuario = usuario)
        self.meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 
                      'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
        utils.combo_fill_text(self.wids['cb_mes'], self.meses)
        self.wids['cb_mes'].set_active(mx.DateTime.localtime().month-1)
        self.wids['sp_anno'].set_value(mx.DateTime.localtime().year)
        connections = {'b_salir/clicked': self.salir,
                       'sp_anno/value-changed': self.actualizar,
                       'cb_mes/changed': self.actualizar,
                       'b_actualizar/clicked': self.actualizar,
                       'b_calcular/clicked': self.crear_nominas_por_defecto, 
                       'b_exportar/clicked': self.exportar, 
                       'b_fechaini/clicked': self.buscar_fecha, 
                       'b_fechafin/clicked': self.buscar_fecha, 
                       'b_imprimir/clicked': self.imprimir, 
                       'b_guardar_obs/clicked': self.guardar_obs
                      }
        self.add_connections(connections)
        cols = (('Empleado', 'gobject.TYPE_STRING', False, True, True, None),
                ('Categoría laboral', 'gobject.TYPE_STRING', False, True, False, None),
                ('Gratificación', 'gobject.TYPE_STRING', True, True, False, self.cambiar_gratificacion),
                ('Plus jefe turno', 'gobject.TYPE_STRING', True, True, False, self.cambiar_plus_jefeturno),
                ('Plus no absentismo', 'gobject.TYPE_STRING', True, True, False, self.cambiar_plus_noabsentismo),
                ('Plus festivos', 'gobject.TYPE_STRING', True, True, False, self.cambiar_plus_festivos),
                ('Plus turnicidad', 'gobject.TYPE_STRING', True, True, False, self.cambiar_plus_turnicidad),
                ('Plus mantenimiento\nsábados', 'gobject.TYPE_STRING', True, True, False, self.cambiar_plus_sabados),
                ('Total horas extras', 'gobject.TYPE_STRING', True, True, False, self.cambiar_total_extra),
                ('Total nocturnidad', 'gobject.TYPE_STRING', True, True, False, self.cambiar_nocturnidad),
                ('Base', 'gobject.TYPE_STRING', True, True, False, self.cambiar_base),
                ('Otros', 'gobject.TYPE_STRING', True, True, False, self.cambiar_otros),
                ('Total nómina', 'gobject.TYPE_STRING', True, True, False, self.cambiar_total),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_nominas'], cols)
        for col in xrange(2, 13):
            column = self.wids['tv_nominas'].get_column(col)
            for cell in column.get_cell_renderers():
                cell.set_property("xalign", 1)
        self.wids['tv_nominas'].connect('row-activated', self.abrir_empleado)
        self.no_crear_por_defecto = False   # Cosas de una mala implementación... ARRRGGHHH!!!1oneoneone :(
        self.rellenar_nominas()
        self.wids['b_guardar_obs'].set_sensitive(False)
        self.wids['txt_observaciones'].get_buffer().connect("changed", lambda txtbuffer: self.wids['b_guardar_obs'].set_sensitive(True))
        gtk.main()

    def guardar_obs(self, boton, mes = None, anno = None):
        """
        Guarda el texto del TextView en un registro observaciones para el mes y 
        año de la nómina.
        Si existe el registro lo machaca, y si no, lo crea.
        """
        if mes == None:
            mes = self.meses.index(utils.combo_get_value(self.wids['cb_mes'])) + 1
        if anno == None:
            anno = int(self.wids['sp_anno'].get_value())
        observaciones = pclases.ObservacionesNominas.select(""" date_part('month', fecha) = %d AND date_part('year', fecha) = %d """ % (mes, anno))
        bounds = self.wids['txt_observaciones'].get_buffer().get_bounds()
        texto = self.wids['txt_observaciones'].get_buffer().get_text(bounds[0], bounds[1])
        self.wids['b_guardar_obs'].set_sensitive(False)
        if observaciones.count() == 0:
            obs = pclases.ObservacionesNominas(fecha = mx.DateTime.DateTimeFrom(day = 1, month = mes, year = anno), 
                                               observaciones = texto)
            pclases.Auditoria.nuevo(obs, self.usuario, __file__)
        else:
            obs = observaciones[0]
            if observaciones.count() > 1:
                self.logger.error("nominas::guardar_obs -> Inconsistencia en la BD. No debe haber más de un registro observaciones para las nóminas del mes %d y año %d." % (mes, anno))
            obs = observaciones[0]
            obs.observaciones = texto

    def buscar_fecha(self, boton):
        """
        Abre el diálogo del calendario.
        """
        e_fecha = boton.name.replace("b_", "e_")
        try:
            valor_anterior = utils.parse_fecha(self.wids[e_fecha].get_text())
        except:
            valor_anterior = None
        self.wids[e_fecha].set_text(utils.str_fecha(utils.mostrar_calendario(valor_anterior, padre = self.wids['ventana'])))

    def abrir_empleado(self, tv, path, view_column):
        self.wids['ventana'].window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        while gtk.events_pending(): gtk.main_iteration(False)
        model = tv.get_model()
        idnomina = model[path][-1]
        nomina = pclases.Nomina.get(idnomina)
        empleado = nomina.empleado
        from formularios import empleados
        self.wids['ventana'].window.set_cursor(None)
        ventanaempleado = empleados.Empleados(empleado)  # @UnusedVariable

    def get_float_tv(self, path, texto, col):
        model = self.wids['tv_nominas'].get_model()
        idnomina = model[path][-1]
        nomina = pclases.Nomina.get(idnomina)
        try:
            valor = utils._float(texto)
            model[path][col] = utils.float2str(valor, 3, autodec = True)
        except ValueError:
            utils.dialogo_info(titulo = "VALOR INCORRECTO", 
                               texto = "El valor introducido no es correcto.", 
                               padre = self.wids['ventana'])
            valor = None
        return nomina, valor

    def recalcular_total_nomina(self, nomina, path):
        # total = nomina.gratificacion + nomina.plusJefeTurno + nomina.plusNoAbsentismo + nomina.plusFestivo + \
        #         nomina.plusTurnicidad + nomina.plusMantenimientoSabados + nomina.totalHorasExtra + \
        #         nomina.totalHorasNocturnidad
        total = nomina.calcular_total(actualizar = False)
        nomina.cantidad = total
        nomina.syncUpdate()
        model = self.wids['tv_nominas'].get_model()
        model[path][12] = utils.float2str(nomina.cantidad, 3, autodec = True)

    def cambiar_gratificacion(self, cell, path, texto):
        nomina, valor = self.get_float_tv(path, texto, 2)
        if valor != None:
            nomina.gratificacion = valor
            self.recalcular_total_nomina(nomina, path)

    def cambiar_plus_jefeturno(self, cell, path, texto):
        nomina, valor = self.get_float_tv(path, texto, 3)
        if valor != None:
            nomina.plusJefeTurno = valor
            self.recalcular_total_nomina(nomina, path)

    def cambiar_plus_noabsentismo(self, cell, path, texto):
        nomina, valor = self.get_float_tv(path, texto, 4)
        if valor != None:
            nomina.plusNoAbsentismo = valor
            self.recalcular_total_nomina(nomina, path)

    def cambiar_plus_festivos(self, cell, path, texto):
        nomina, valor = self.get_float_tv(path, texto, 5)
        if valor != None:
            nomina.plusFestivo = valor
            self.recalcular_total_nomina(nomina, path)

    def cambiar_plus_turnicidad(self, cell, path, texto):
        nomina, valor = self.get_float_tv(path, texto, 6)
        if valor != None:
            nomina.plusTurnicidad = valor
            self.recalcular_total_nomina(nomina, path)

    def cambiar_plus_sabados(self, cell, path, texto):
        nomina, valor = self.get_float_tv(path, texto, 7)
        if valor != None:
            nomina.plusMantenimientoSabados = valor
            self.recalcular_total_nomina(nomina, path)

    def cambiar_total_extra(self, cell, path, texto):
        nomina, valor = self.get_float_tv(path, texto, 8)
        if valor != None:
            nomina.totalHorasExtra = valor
            self.recalcular_total_nomina(nomina, path)

    def cambiar_nocturnidad(self, cell, path, texto):
        nomina, valor = self.get_float_tv(path, texto, 9)
        if valor != None:
            nomina.totalHorasNocturnidad = valor
            self.recalcular_total_nomina(nomina, path)
    
    def cambiar_base(self, cell, path, texto):
        nomina, valor = self.get_float_tv(path, texto, 10)
        if valor != None:
            nomina.base = valor
            self.recalcular_total_nomina(nomina, path)
    
    def cambiar_otros(self, cell, path, texto):
        nomina, valor = self.get_float_tv(path, texto, 11)
        if valor != None:
            nomina.otros = valor
            self.recalcular_total_nomina(nomina, path)

    def cambiar_total(self, cell, path, texto):
        nomina, valor = self.get_float_tv(path, texto, 12)
        if valor != None:
            nomina.cantidad = valor

    def chequear_cambios(self):
        pass

    def buscar_partes_produccion(self, fecha_ini, fecha_fin):
        """
        Devuelve los resultados de una consulta SQLObject sobre partes de producción
        entre las fechas recibidas.
        """
        PDP = pclases.ParteDeProduccion
        OR = pclases.OR
        AND = pclases.AND
        # seis_am = mx.DateTime.DateTimeDelta(6.0/24)
        # Extrañamente, SQLObject no conoce el tipo DateTimeDelta en las consultas (!)
        medianoche = mx.DateTime.DateTimeFrom(hour = 0)
        seis_am = mx.DateTime.DateTimeFrom(hour = 6)   # Por defecto va a poner el día de hoy en la parte de 
        # la fecha, pero afortunadamente al comparar un DateTimeDelta con un DateTime, lo va a ignorar.
        # diez_pm = mx.DateTime.DateTimeDelta(22.0/24)
        limiteinf = AND(PDP.q.fecha == fecha_ini, PDP.q.horainicio >= seis_am)
        # limiteinf = AND(PDP.q.fecha == fecha_ini, """ horainicio >= '6:00' """)
        centrales = AND(PDP.q.fecha > fecha_ini, PDP.q.fecha <= fecha_fin)
        limitesup = AND(PDP.q.fecha == fecha_fin + mx.DateTime.oneDay, 
                        PDP.q.horainicio >= medianoche, 
                        PDP.q.horainicio <= seis_am, 
                        PDP.q.horafin <= seis_am)
        # limitesup = AND(PDP.q.fecha == fecha_fin + mx.DateTime.oneDay, """ horafin <= '6:00' """)
        # Si la consulta entera va con """...""" sí rula. En el momento que lo metes en un SQLOp falla el __sqlrepr__()
        partes = PDP.select(OR(limiteinf, centrales, limitesup))
        # partes = pclases.ParteDeProduccion.select(sqlobject.AND(\
        #     pclases.ParteDeProduccion.q.fecha >= fecha_ini,
        #     pclases.ParteDeProduccion.q.fecha <= (fecha_fin+mx.DateTime.oneDay)
        #     ))
        #solo para DEBUG:        print partes.count()
        #solo para DEBUG:        for p in partes:
        #solo para DEBUG:            print p.id, p.fecha, p.horainicio, p.horafin
        return partes

    def calcular_horas(self, fecha_ini, fecha_fin):
        """
        Calcula las horas trabajadas en cada parte del 
        rango de fechas.
        """
        partes_produccion = self.buscar_partes_produccion(fecha_ini, fecha_fin)

        empleados, aux = self.preparar_datos(partes_produccion, fecha_ini, fecha_fin)
        
        ftini = mx.DateTime.DateTimeFrom(year = fecha_ini.year, 
                                         month = fecha_ini.month, 
                                         day = fecha_ini.day, 
                                         hour = 6, 
                                         minute = 0, 
                                         second = 0).strftime('%Y-%m-%d %H:%M:%S')
        ftfin = (mx.DateTime.DateTimeFrom(year = fecha_fin.year, 
                                         month = fecha_fin.month, 
                                         day = fecha_fin.day, 
                                         hour = 6, 
                                         minute = 0, 
                                         second = 0) + mx.DateTime.oneDay).strftime('%Y-%m-%d %H:%M:%S')
        partes_t = pclases.ParteDeTrabajo.select("""horainicio >= '%s' AND horainicio < '%s' """ % (ftini, ftfin))
        empleados = self.preparar_datos_recuperacion(partes_t, fecha_ini, fecha_fin, empleados, aux)
        # Ahora los que no trabajaron:
        all_emps = pclases.Empleado.select(pclases.Empleado.q.planta == True)
        ids_emps_trabajo = [e['id'] for e in empleados]
        descanso = [e for e in all_emps if e.id not in ids_emps_trabajo]  # @UnusedVariable
        return empleados
                           
    def func_sort_partes(self, p1, p2):
        if p1.fecha < p2.fecha:
            return -1
        elif p1.fecha > p2.fecha:
            return 1
        else:
            if p1.horainicio < p2.horainicio:
                return -1
            elif p1.horainicio > p2.horainicio:
                return 1
            else:
                return 0
                
    def func_sort_partes_t(self, p1, p2):
        if p1.horainicio < p2.horainicio:
            return -1
        elif p1.horainicio > p2.horainicio:
            return 1
        else:
            return 0
    
    def preparar_datos(self, partes_result, fecha_ini, fecha_fin):
        """
        A partir de los partes de producción recibidos genera una lista de diccionarios
        del tipo {'nombre': , 'horas': , 'extra': , 'noche': , 'extra_n': , 'total': , 'id': } donde se 
        guarda una entrada por empleado que contiene el nombre completo, las horas 
        "normales" trabajadas, las horas extras (día y noche), las que entran en franja nocturna 
        (de 22:00 a 6:00) y el total de horas entre todos los partes en los que trabajó.
        El id no se usará, pero es el del empleado.
        Todas las horas se devolverán en formato HH:MM
        """
        # WTF: Esto hay que refactorizarlo PERO YA.
        # NOTA: fechaini y fechafin no se llegan a usar. Las conservo porque aún está en pruebas
        # el funcionamiento de la distribución de horas (se usaba para discriminar los partes pertenecientes
        # a otra jornada laboral distinta del día natural.
        res = []
        aux = {}
        ininoche = mx.DateTime.DateTimeDeltaFrom(hours = 22, minutes = 0)  # @UnusedVariable
        finnoche = mx.DateTime.DateTimeDeltaFrom(hours = 6, minutes = 0)
        # Hay que ordenar los partes por fecha y hora para que se contabilicen 
        # bien las horas extras.
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        i = 0.0
        tot = partes_result.count()
        partes = []
        for p in partes_result:
            vpro.set_valor(i/tot, "Obteniendo partes de producción...")
            partes.append(p)
            i += 1
        vpro.set_valor(1, "Ordenando partes de producción...")
        partes.sort(self.func_sort_partes)
        i = 0.0
        for p in partes:
            vpro.set_valor(i/tot, "Analizando partes de producción...")
            for ht in p.horasTrabajadas:
                ht_horas = ht.horas
                if isinstance(ht_horas, datetime.time):
                    ht_horas = mx.DateTime.DateTimeDeltaFrom(
                        hours = ht_horas.hour, 
                        minutes = ht_horas.minute)
                if ht.empleado.id not in aux:
                    aux[ht.empleado.id] = {'pos': len(res), 'fechas': {}}
                    res.append({'nombre': "%s, %s" % (ht.empleado.apellidos, ht.empleado.nombre),
                                'horas': mx.DateTime.DateTimeDelta(0),
                                'extra': mx.DateTime.DateTimeDelta(0),
                                'extra_n': mx.DateTime.DateTimeDelta(0),
                                'noche': mx.DateTime.DateTimeDelta(0),
                                'total': mx.DateTime.DateTimeDelta(0),
                                'sabados': mx.DateTime.DateTimeDelta(0),
                                'festivos': mx.DateTime.DateTimeDelta(0),
                                'id': ht.empleado.id})
                pos = aux[ht.empleado.id]['pos']
                # Cálculo de las horas nocturnas:
                #if ht.partedeproduccion.horainicio >= ininoche and \
                #    ht.partedeproduccion.horafin <= finnoche:
                if ht.partedeproduccion.es_nocturno():
                    # OJO: Nunca se dará un parte que cubra dos franjas horarias de dos turnos
                    # diferentes, por tanto, si por ejemplo un empleado hace 2 horas de un parte de 6
                    # o las 6 horas son completas de noche (y por lo tanto las 2 del trabajador) o son 
                    # de día. Resumiendo: No hay partes que empiecem p. ej. a las 16:00 y acaben después 
                    # de las 22:00 y viceversa. De todas formas chequeo las dos horas por si acaso.
                    noche = ht_horas
                else:
                    noche = mx.DateTime.DateTimeDeltaFrom(hours = 0)
                # Cálculo de las horas extras: El primer parte del día es el de las 6:00. 
                # Si la hora de inicio del parte es inferior a esa, se considerará del día 
                # anterior a efectos de horas extras.
                try:
                    anterior_finnoche=ht.partedeproduccion.horainicio<finnoche
                except TypeError:   # horainicio es datetime.time
                    horainicio_parte = mx.DateTime.DateTimeDeltaFrom(
                        hours = ht.partedeproduccion.horainicio.hour, 
                        minutes = ht.partedeproduccion.horainicio.minute)
                    anterior_finnoche = horainicio_parte < finnoche
                if anterior_finnoche:
                    dia = (ht.partedeproduccion.fecha - mx.DateTime.oneDay)
                else:
                    dia = ht.partedeproduccion.fecha
                if dia not in aux[ht.empleado.id]['fechas']:
                    aux[ht.empleado.id]['fechas'][dia] = mx.DateTime.DateTimeDelta(0)
                try:
                    tmp = aux[ht.empleado.id]['fechas'][dia] + ht_horas
                except TypeError:
                    tmp = (aux[ht.empleado.id]['fechas'][dia] 
                        + mx.DateTime.DateTimeDeltaFrom(hours = ht_horas.hour, 
                                                    minutes = ht_horas.minute))
                if tmp > mx.DateTime.DateTimeDeltaFrom(hours = 8):
                    extra = aux[ht.empleado.id]['fechas'][dia] + \
                            ht_horas - \
                            mx.DateTime.DateTimeDeltaFrom(hours = 8)
                    aux[ht.empleado.id]['fechas'][dia] = mx.DateTime.DateTimeDeltaFrom(hours = 8) 
                else:
                    extra = mx.DateTime.DateTimeDelta(0)
                    try:
                        aux[ht.empleado.id]['fechas'][dia] += ht_horas
                    except TypeError:
                        aux[ht.empleado.id]['fechas'][dia] += \
                          mx.DateTime.DateTimeDeltaFrom(hours = ht_horas.hour, 
                                                    minutes = ht_horas.minute)
                # Cálculo de festivos y sábados:
                # OJO: Joder, qué dolor de cabeza. Aquí día si es una fecha...
                # fdia = mx.DateTime.DateTimeFrom(year = int(dia.split('-')[0]), month = int(dia.split('-')[1]), day = int(dia.split('-')[2])) 
                fdia = dia
                try:
                    calendario = ht.empleado.categoriaLaboral and \
                                 ht.empleado.categoriaLaboral.lineaDeProduccion and \
                                 [c for c in ht.empleado.categoriaLaboral.lineaDeProduccion.calendariosLaborales if \
                                    c.mesAnno.month == fdia.month and c.mesAnno.year == fdia.year][0] or\
                                 None
                except IndexError:
                    calendario = None
                if calendario != None:
                    festivos = [f.fecha for f in calendario.festivos]
                    if fdia in festivos:
                        res[pos]['festivos'] += ht_horas
                if fdia.day_of_week == 5:    # 0 es lunes
                    res[pos]['sabados'] += ht_horas
                # Ya tengo las horas nocturas (variable noche) y las extras (extra). 
                # Guardo valores en el diccionario de resultados globales:
                if noche != 0:  # Un mx.DateTime... == 0 da True si es de 0 horas, 0 minutos...
                    res[pos]['noche'] += noche - extra
                    res[pos]['extra_n'] += extra
                else:
                    res[pos]['horas'] += ht_horas - extra
                    res[pos]['extra'] += extra
                res[pos]['total'] += ht_horas 
            i += 1
        vpro.ocultar()
        return res, aux

    def get_solo_hora(self, fecha):
        """
        Devuelve un DateTimeDelta con solo la hora de 
        la fecha recibida.
        """
        return mx.DateTime.DateTimeDeltaFrom(hours = fecha.hour, minutes = fecha.minute, seconds = fecha.second)

    def preparar_datos_recuperacion(self, partes_result, fecha_ini, fecha_fin, res, aux):
        """
        A partir de los partes de producción recibidos genera una lista de diccionarios
        del tipo {'nombre': , 'horas': , 'extra': , 'noche': , 'extra_n': , 'total': , 'id': } donde se 
        guarda una entrada por empleado que contiene el nombre completo, las horas 
        "normales" trabajadas, las horas extras (día y noche), las que entran en franja nocturna 
        (de 22:00 a 6:00) y el total de horas entre todos los partes en los que trabajó.
        El id no se usará, pero es el del empleado.
        Todas las horas se devolverán en formato HH:MM
        """
        # NOTA: OJO: Al calcularse de forma independiente, NO SE SUMA A LAS HORAS EXTRA (si lo fueran) y 
        # además puede llegarse a mostrar un mismo trabajador con (R) y en producción -cosa que 
        # supongo será correcta-. Esta función hay que PROBARLA MUCHO y A FONDO.
        # Por ejemplo: Hay un caso que no debería darse, pero aún así, habrá que tenerlo en cuenta tarde o 
        # temprano. Si un trabajador echa 4 horas entre las 20:00 y las 00:00 se le contarán las 4 como 
        # horas diurnas. Se solucionaría añadiendo las 2 horas de día y las 2 de noche por separado.
        # Además, el cambio de turno es a las 22:00. No debería haber un trabajador que empiece en un turno y 
        # acabe después de empezar el siguiente. De todas formas: TENLO EN CUENTA por si acaso.
        # WTF: Esto hay que refactorizarlo PERO YA.
        # NOTA: fechaini y fechafin no se llegan a usar. Las conservo porque aún está en pruebas
        # el funcionamiento de la distribución de horas (se usaba para discriminar los partes pertenecientes
        # a otra jornada laboral distinta del día natural.
        ininoche = mx.DateTime.DateTimeDeltaFrom(hours = 22, minutes = 0)
        finnoche = mx.DateTime.DateTimeDeltaFrom(hours = 6, minutes = 0)
        # Hay que ordenar los partes por fecha y hora para que se contabilicen 
        # bien las horas extras.
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        i = 0.0
        tot = partes_result.count()
        partes = []
        for p in partes_result:
            vpro.set_valor(i/tot, "Obteniendo partes de trabajo...")
            partes.append(p)
            i += 1
        vpro.set_valor(1, "Ordenando partes de trabajo...")
        partes.sort(self.func_sort_partes_t)
        i = 0.0
        for ht in partes:
            vpro.set_valor(i/tot, "Analizando partes de trabajo...")
            ht_horas = ht.horas
            if isinstance(ht_horas, datetime.time):
                ht_horas = mx.DateTime.DateTimeDeltaFrom(
                    hours = ht_horas.hour, 
                    minutes = ht_horas.minute)            
            if ht.empleado.id not in aux:
                aux[ht.empleado.id] = {'pos': len(res), 'fechas': {}}
                res.append({'nombre': "%s, %s (R)" % (ht.empleado.apellidos, ht.empleado.nombre),
                            'horas': mx.DateTime.DateTimeDelta(0),
                            'extra': mx.DateTime.DateTimeDelta(0),
                            'extra_n': mx.DateTime.DateTimeDelta(0),
                            'noche': mx.DateTime.DateTimeDelta(0),
                            'total': mx.DateTime.DateTimeDelta(0),
                            'sabados': mx.DateTime.DateTimeDelta(0),
                            'festivos': mx.DateTime.DateTimeDelta(0),
                            'id': ht.empleado.id})
            pos = aux[ht.empleado.id]['pos']
            # Cálculo de las horas nocturnas:
            if self.get_solo_hora(ht.horainicio) >= ininoche and \
               self.get_solo_hora(ht.horafin) <= finnoche:
                noche = ht_horas
            else:
                noche = mx.DateTime.DateTimeDeltaFrom(hours = 0)
            if self.get_solo_hora(ht.horafin) < finnoche:
                dia = (ht.horainicio - mx.DateTime.oneDay).strftime('%Y-%m-%d')
            else:
                dia = ht.horainicio.strftime('%Y-%m-%d')
            if dia not in aux[ht.empleado.id]['fechas']:
                aux[ht.empleado.id]['fechas'][dia] = mx.DateTime.DateTimeDelta(0)
            if aux[ht.empleado.id]['fechas'][dia] + ht_horas > mx.DateTime.DateTimeDeltaFrom(hours = 8):
                extra = aux[ht.empleado.id]['fechas'][dia] + \
                        ht_horas - \
                        mx.DateTime.DateTimeDeltaFrom(hours = 8)
                aux[ht.empleado.id]['fechas'][dia] = mx.DateTime.DateTimeDeltaFrom(hours = 8) 
            else:
                extra = mx.DateTime.DateTimeDelta(0)
                aux[ht.empleado.id]['fechas'][dia] += ht_horas
            # Cálculo de festivos y sábados:
            fdia = mx.DateTime.DateTimeFrom(year = int(dia.split('-')[0]), month = int(dia.split('-')[1]), day = int(dia.split('-')[2])) 
            try:
                calendario = ht.empleado.categoriaLaboral and \
                             ht.empleado.categoriaLaboral.lineaDeProduccion and \
                             [c for c in ht.empleado.categoriaLaboral.lineaDeProduccion.calendariosLaborales if \
                                c.mesAnno.month == fdia.month and c.mesAnno.year == fdia.year][0] or\
                             None
            except IndexError:
                calendario = None
            festivos = [mx.DateTime.DateTimeFrom(day = f.fecha.day, month = f.fecha.month, year = int(dia.split("-")[0])) for f in pclases.FestivoGenerico.select()]
            if calendario != None:
                festivos += [f.fecha for f in calendario.festivos]
            if fdia in festivos:
                res[pos]['festivos'] += ht_horas
            if fdia.day_of_week == 5:    # 0 es lunes
                res[pos]['sabados'] += ht_horas
            # Ya tengo las horas nocturas (variable noche) y las extras (extra). 
            # Guardo valores en el diccionario de resultados globales:
            if noche != 0:  # Un mx.DateTime... == 0 da True si es de 0 horas, 0 minutos...
                res[pos]['noche'] += noche - extra
                res[pos]['extra_n'] += extra
            else:
                res[pos]['horas'] += ht_horas - extra
                res[pos]['extra'] += extra
            res[pos]['total'] += ht_horas 
            i += 1
        vpro.ocultar()
        return res
   
    def horas_minutos_from_delta(self, delta):
        """
        Devuelve una tupla (h, m) con las horas y minutos en formato entero
        de un mx.DateTime.DateTimeDelta.
        """
        return (int(delta.hours), int(delta.minutes % 60))
        
    def actualizar(self, b):
        self.no_crear_por_defecto = False
        self.rellenar_nominas()

    def crear_nominas_por_defecto(self, boton, mes = None, anno = None, borrar = True, fechaini = None, fechafin = None):
        """
        Si borrar es True, borra todas las nóminas que ya existan para el 
        mes y año indicados.
        Crea las nóminas para todos los empleados activos con la fecha 1 del 
        mes y año recibidos y los cálculos correctos a partir de los partes
        de trabajo, categoría laboral y demás.
        Si fechaini y fechafin son None usará el día 1 o último de mes 
        respectivamente.
        """
        txt = """
                                                                                    
        Al recalcular las nóminas se perderán todos los datos introducidos          
        para las ya existentes.                                                     
                                                                                    
        ¿Está seguro de que desea recalcular todas las nóminas?                     
                                                                                    
        """
        if mes == None:
            mes = self.meses.index(utils.combo_get_value(self.wids['cb_mes'])) + 1
        if anno == None:
            anno = int(self.wids['sp_anno'].get_value())
        nominas = pclases.Nomina.select("""date_part('month', fecha) = %d AND date_part('year', fecha) = %d""" 
                                        % (mes, anno))
        if not fechaini:
            try:
                fechaini = utils.parse_fecha(self.wids['e_fechaini'].get_text())
            except:
                fechaini = mx.DateTime.DateTimeFrom(day = 1, month = mes, year = anno)
        if not fechafin:
            try:
                fechafin = utils.parse_fecha(self.wids['e_fechafin'].get_text())
            except:
                fechafin = mx.DateTime.DateTimeFrom(day = -1, month = mes, year = anno)
        if nominas.count() > 0 and \
           borrar and \
           utils.dialogo(titulo = "¿RECALCULAR NÓMINAS?", texto = txt, padre = self.wids['ventana']):
            # Borrar y crear
            for nomina in nominas:
                nomina.destroy(ventana = __file__)
            self.crear_nominas(mes, anno, fechaini, fechafin)
            self.rellenar_nominas()
        else:
            # Crear sin más
            self.crear_nominas(mes, anno, fechaini, fechafin)
            self.rellenar_nominas()

    def calcular_horasExtra(self, e, empleado):
        # return empleado['extra_n'] + empleado['extra']
        return empleado['extra'].hours    # Sólo las extra de día. 

    def calcular_horasNocturnidad(self, e, empleado):
        return empleado['extra_n'].hours #+ empleado['noche']
        # La nocturnidad es un recargo que se aplica por noche completa.
        # Aquí se calculan las horas extras de noche.
    
    def calcular_plusJefeTurno(self, e):
        try:
            return e.categoriaLaboral.precioPlusJefeTurno
        except AttributeError:
            return 0
    
    def calcular_plusFestivo(self, e, empleado):
        try:
            horas_en_festivo = empleado['festivos'].hours
            return e.categoriaLaboral.precioPlusFestivo * horas_en_festivo
        except AttributeError:
            return 0
     
    def calcular_plusTurnicidad(self, e):
        """
        Para que afecte sólo a fibra debe estar bien configurado en la categoría laboral.
        """
        try:
            return e.categoriaLaboral.precioPlusTurnicidad
        except AttributeError:
            return 0
     
    def calcular_plusMantenimientoSabados(self, e, empleado):
        try:
            horas_en_sabado = empleado['sabados'].hours
            return e.categoriaLaboral.precioPlusMantenimientoSabados * horas_en_sabado
        except AttributeError:
            return 0
     
    def calcular_totalHorasExtra(self, e, empleado):
        try:
            return (e.categoriaLaboral.precioHoraExtra * empleado['extra'].hours) + \
                    (e.categoriaLaboral.precioHoraNocturnidad * empleado['extra_n'].hours)
        except AttributeError:
            return 0
     
    def calcular_totalHorasNocturnidad(self, e, empleado):
        """
        Lo que devuelve es el recargo por noche trabajada por el número de noches trabajadas.
        El recargo es por cada 8 horas de trabajo de noche. Las horas extras de noche se calculan
        aparte y se guardan en total junto con las horas extras normales.
        CAMBIO 2 de mayo de 2007: Si no trabaja una noche completa se le devuelve la parte 
        proporcional.
        """
        if empleado['noche'].hours > 0:
            try:
                #res = e.categoriaLaboral.precioPlusNocturnidad * ceil((empleado['noche'].hours / 8.0))
                precio_hora_noche = e.categoriaLaboral.precioPlusNocturnidad / 8.0
                res = empleado['noche'].hours * precio_hora_noche
            except AttributeError:
                res = 0
        else:
            res = 0
        return res
            
    def crear_nominas(self, mes, anno, fecha_ini, fecha_fin):
        fecha = mx.DateTime.DateTimeFrom(day = 1, month = mes, year = anno) # Mes natural al que corresponde la fecha
        #fecha_fin = mx.DateTime.DateTimeFrom(day = fecha_ini.days_in_month, month = mes, year = anno)
        empleados = self.calcular_horas(fecha_ini, fecha_fin)
        if empleados == []:
            utils.dialogo_info(titulo = "NO SE ENCONTRARON PARTES", 
                               texto = "No se encontraron partes de producción ni trabajo para el mes indicado.\nAsegúrese de que se registran las horas de trabajo en el sistema\ny vuelva a intentarlo abriendo de nuevo la ventana o\npulsando el botón de recalcular nóminas.",
                               padre = self.wids['ventana'])
            self.no_crear_por_defecto = True
        for empleado in empleados:
            e = pclases.Empleado.get(empleado['id'])
            horasExtra = self.calcular_horasExtra(e, empleado)
            horasNocturnidad = self.calcular_horasNocturnidad(e, empleado)
            plusJefeTurno = self.calcular_plusJefeTurno(e)
            plusFestivo = self.calcular_plusFestivo(e, empleado)
            plusTurnicidad = self.calcular_plusTurnicidad(e)
            plusMantenimientoSabados = self.calcular_plusMantenimientoSabados(e, empleado)
            totalHorasExtra = self.calcular_totalHorasExtra(e, empleado)
            totalHorasNocturnidad = self.calcular_totalHorasNocturnidad(e, empleado)
            if e.nomina != None:
                base_nomina = utils._float(e.nomina)
            else:
                base_nomina = 0
            nomina = pclases.Nomina(empleado = e, 
                                    fecha = fecha, 
                                    cantidad = 0, 
                                    horasExtra = horasExtra,
                                    horasNocturnidad = horasNocturnidad,
                                    gratificacion = 0,
                                    plusJefeTurno = plusJefeTurno,
                                    plusNoAbsentismo = 0,
                                    plusFestivo = plusFestivo, 
                                    plusTurnicidad = plusTurnicidad, 
                                    plusMantenimientoSabados = plusMantenimientoSabados,
                                    totalHorasExtra = totalHorasExtra,
                                    totalHorasNocturnidad = totalHorasNocturnidad, 
                                    base = base_nomina, 
                                    fechaini = fecha_ini, 
                                    fechafin = fecha_fin
                                   )
            pclases.Auditoria.nuevo(nomina, self.usuario, __file__)
            nomina.calcular_total()
        
    def rellenar_nominas(self, boton = None):
        # Si no existe ninguna nómina en el mes de la ventana, crearlas por defecto
        # para todos los empleados activos.
        mes = self.meses.index(utils.combo_get_value(self.wids['cb_mes'])) + 1
        anno = int(self.wids['sp_anno'].get_value())
        nominas = pclases.Nomina.select(""" date_part('month', fecha) = %d AND date_part('year', fecha) = %d """ 
                                        % (mes, anno))
        observaciones = pclases.ObservacionesNominas.select(""" date_part('month', fecha) = %d AND date_part('year', fecha) = %d """ % (mes, anno))
        if observaciones.count() == 1:
            self.wids['txt_observaciones'].get_buffer().set_text(observaciones[0].observaciones)
        elif observaciones.count() > 1:
            self.logger.error("nominas::rellenar_nominas -> Inconsistencia en la BD. No debe haber más de un registro observaciones para las nóminas del mes %d y año %d." % (mes, anno))
            self.wids['txt_observaciones'].get_buffer().set_text(observaciones[0].observaciones)
        else:
            self.wids['txt_observaciones'].get_buffer().set_text("")
        self.wids['b_guardar_obs'].set_sensitive(False)
        if nominas.count() == 0:
            primero_mes = mx.DateTime.DateTimeFrom(day = 1, month = mes, year = anno)
            fin_de_mes = mx.DateTime.DateTimeFrom(day = -1, month = mes, year = anno)
            self.wids['e_fechaini'].set_text(utils.str_fecha(primero_mes))
            self.wids['e_fechafin'].set_text(utils.str_fecha(fin_de_mes))
            if not self.no_crear_por_defecto:   # Si la primera vez no creó nada. No sigue intentándolo.
                self.crear_nominas_por_defecto(None, mes, anno, fechaini = primero_mes, fechafin = fin_de_mes)
        else:
            model = self.wids['tv_nominas'].get_model()
            model.clear()
            for nomina in nominas:
                model.append(("%s, %s" % (nomina.empleado.apellidos, nomina.empleado.nombre), 
                              nomina.empleado.categoriaLaboral and nomina.empleado.categoriaLaboral.puesto or "", 
                              utils.float2str(nomina.gratificacion, 3, autodec = True), 
                              utils.float2str(nomina.plusJefeTurno, 3, autodec = True), 
                              utils.float2str(nomina.plusNoAbsentismo, 3, autodec = True), 
                              utils.float2str(nomina.plusFestivo, 3, autodec = True), 
                              utils.float2str(nomina.plusTurnicidad, 3, autodec = True), 
                              utils.float2str(nomina.plusMantenimientoSabados, 3, autodec = True), 
                              utils.float2str(nomina.totalHorasExtra, 3, autodec = True), 
                              utils.float2str(nomina.totalHorasNocturnidad, 3, autodec = True), 
                              utils.float2str(nomina.base, 3, autodec = True), 
                              utils.float2str(nomina.otros, 3, autodec = True), 
                              utils.float2str(nomina.cantidad, 3, autodec = True), 
                              nomina.id
                            ))
            # Las fechas las tomo de la última nómina. En teoría todas las nóminas del mes llevan las mismas fechaini y fin.
            self.wids['e_fechaini'].set_text(utils.str_fecha(nomina.fechaini))
            self.wids['e_fechafin'].set_text(utils.str_fecha(nomina.fechafin))
    
    def imprimir(self, boton):
        """
        Imprime el TreeView de la ventana.
        """
        from informes.treeview2pdf import treeview2pdf
        from formularios.reports import abrir_pdf
        mes = utils.combo_get_value(self.wids['cb_mes'])
        anno = int(self.wids['sp_anno'].get_value())
        strfecha = "%s de %s (%s a %s)" % (mes, anno, self.wids['e_fechaini'].get_text(), self.wids['e_fechafin'].get_text())
        tv = self.crear_fake_treeview(self.wids['tv_nominas'], catlaboral = False)  
        abrir_pdf(treeview2pdf(tv, titulo = "Pluses y nóminas", fecha = strfecha, apaisado = True))
    
    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a MS-Exel/OOoCalc.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        tv = self.crear_fake_treeview(self.wids['tv_nominas'], catlaboral = True) 
        abrir_csv(treeview2csv(tv))

    def crear_fake_treeview(self, tvorig, catlaboral = True):
        """
        Crea y devuelve un TreeView que llevará o no la columna de 
        categoría laboral si «catlaboral» es True o False.
        También llevará como última fila del model los totales y una 
        última fila con las observaciones de la ventana en la primera 
        columna.
        """
        tv = gtk.TreeView()
        tv.set_name(tvorig.get_name())
        cols = [('Empleado', 'gobject.TYPE_STRING', False, True, True, None),
                ('Gratificación', 'gobject.TYPE_STRING', True, True, False, self.cambiar_gratificacion),
                ('Plus jefe turno', 'gobject.TYPE_STRING', True, True, False, self.cambiar_plus_jefeturno),
                ('Plus no absentismo', 'gobject.TYPE_STRING', True, True, False, self.cambiar_plus_noabsentismo),
                ('Plus festivos', 'gobject.TYPE_STRING', True, True, False, self.cambiar_plus_festivos),
                ('Plus turnicidad', 'gobject.TYPE_STRING', True, True, False, self.cambiar_plus_turnicidad),
                ('Plus mantenimiento\nsábados', 'gobject.TYPE_STRING', True, True, False, self.cambiar_plus_sabados),
                ('Total horas extras', 'gobject.TYPE_STRING', True, True, False, self.cambiar_total_extra),
                ('Total nocturnidad', 'gobject.TYPE_STRING', True, True, False, self.cambiar_nocturnidad),
                ('Base', 'gobject.TYPE_STRING', True, True, False, self.cambiar_base),
                ('Otros', 'gobject.TYPE_STRING', True, True, False, self.cambiar_otros),
                ('Total nómina', 'gobject.TYPE_STRING', True, True, False, self.cambiar_total),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None)]
        if catlaboral:
            cols.insert(1, ('Categoría laboral', 'gobject.TYPE_STRING', False, True, False, None))
        utils.preparar_listview(tv, cols)
        for i in xrange(len(tv.get_columns())):
            col = tv.get_column(i)
            if i >= len(tv.get_columns()) - 11:
                for cell in col.get_cell_renderers():
                    cell.set_property("xalign", 1.0)
            col.set_alignment(5.0)
            col.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
            col.set_fixed_width(tvorig.get_column(i).get_width())
        model = tv.get_model()
        totales = ["Totales"] + [0.0] * 11 + [0]
        if catlaboral: 
            totales.insert(1, "")
        for roworig in tvorig.get_model():
            filaorig = [i for i in roworig]
            if not catlaboral:
                filaorig = filaorig[0:1] + filaorig[2:]
            if catlaboral:
                model.append(filaorig)
            else:
                model.append(filaorig)
            if catlaboral:
                offset = 2
            else:
                offset = 1
            for i in xrange(11):
                totales[offset + i] += utils._float(filaorig[offset + i])
        model.append(["---"] * (catlaboral and 13 or 12) + [-1])
        _totales = []
        for dato in totales:
            if isinstance(dato, type(0.1)):
                _totales.append(utils.float2str(dato))
            else:
                _totales.append(dato)
        model.append(_totales)
        model.append(["==="] * (catlaboral and 13 or 12) + [-1])
        bounds = self.wids['txt_observaciones'].get_buffer().get_bounds()
        texto = self.wids['txt_observaciones'].get_buffer().get_text(bounds[0], bounds[1])
        model.append([texto] + [">->"] * (len(cols) - 2) + [-2])
        return tv

if __name__ == '__main__':
    t = Nominas()

