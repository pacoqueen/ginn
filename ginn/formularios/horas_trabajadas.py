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
##  
###################################################################
## Changelog:
## 22 de mayo de 2006 -> Inicio
## 23 de mayo de 2006 -> Fin
## 30 de julio de 2006 -> ¿Fin? JA
###################################################################
## PLAN: Usar TreeView y meter en cada empleado los partes y horas
##       trabajadas en el periodo de tiempo.
###################################################################
from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
import mx.DateTime
import datetime
    

class HorasTrabajadas(Ventana):
    def __init__(self, objeto = None, usuario = None):
        self.usuario = usuario
        Ventana.__init__(self, 'horas_trabajadas.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_fecha_ini/clicked': self.set_fecha_ini,
                       'b_fecha_fin/clicked': self.set_fecha_fin,
                       'b_consultar/clicked': self.rellenar_horas,
                       'b_actualizar/clicked': self.actualizar, 
                       'b_imprimir/clicked': self.imprimir,
                       'b_exportar/clicked': self.exportar}
        self.add_connections(connections)
        cols = (('Empleado', 'gobject.TYPE_STRING', False, True, True, None),
                ('Horas regulares','gobject.TYPE_STRING', False, True, False, None),
                ('Horas noche','gobject.TYPE_STRING', False, True, False, None),
                ('H. extra','gobject.TYPE_STRING', False, True, False, None),
                ('H. extra noche','gobject.TYPE_STRING', False, True, False, None),
                ('Total','gobject.TYPE_STRING', False, True, False, None),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_horas'], cols)
        self.wids['tv_horas'].connect("row-activated", self.mostrar_horas)
        self.wids['e_fecha_ini'].set_text(mx.DateTime.localtime().strftime('%d/%m/%Y'))
        self.wids['e_fecha_fin'].set_text(mx.DateTime.localtime().strftime('%d/%m/%Y'))
        self.rellenar_horas()
        gtk.main()

    def mostrar_horas(self, tv, path, vc):
        """
        Abre una ventana de búsqueda con las horas trabajadas en 
        partes de producción y partes de trabajo.
        """
        # EMPLEADO
        self.wids['ventana'].window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        while gtk.events_pending(): gtk.main_iteration(False)
        model = tv.get_model()
        idempleado = model[path][-1]
        empleado = pclases.Empleado.get(idempleado)
        # PARTES DE PRODUCCIÓN
        try:
            dia, mes, anno = map(int, self.wids['e_fecha_ini'].get_text().split('/'))
        except:
            utils.dialogo_info(titulo = "FECHA INCORRECTA", texto = "La fecha inicial no es correcta. Use el formato día/mes/año")
        else:
            fecha_ini = mx.DateTime.DateTimeFrom(day = dia, month = mes, year = anno) 
            dia, mes, anno = map(int, self.wids['e_fecha_fin'].get_text().split('/'))
            try:
                fecha_fin = mx.DateTime.DateTimeFrom(day = dia, month = mes, year = anno) 
            except:
                utils.dialogo_info(titulo = "FECHA INCORRECTA", texto = "La fecha inicial no es correcta. Use el formato día/mes/año")
            else:
                partes_produccion = self.buscar_partes_produccion(fecha_ini, fecha_fin)
                horas_trabajadas = []   # Horas en partes de producción
                horas_recuperacion = [] # Horas en partes de trabajo
                for pdp in partes_produccion:
                    for ht in pdp.horasTrabajadas:
                        if ht.empleado == empleado:
                            horas_trabajadas.append(("PDP:%d" % (ht.parteDeProduccion.id), 
                                                     utils.str_fecha(pdp.fecha), 
                                                     utils.str_hora_corta(pdp.horainicio), 
                                                     utils.str_hora_corta(pdp.horafin), 
                                                     utils.str_hora_corta(pdp.get_duracion()), 
                                                     utils.str_hora_corta(ht.horas), 
                                                     pdp))
        # PARTES DE TRABAJO
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
                partes_trabajo = pclases.ParteDeTrabajo.select("""horainicio >= '%s' AND horainicio < '%s' """ % (ftini, ftfin))
                for pdt in partes_trabajo:
                    if pdt.empleado == empleado:
                        horas_recuperacion.append(("PDT:%d" % (pdt.id), 
                                                   utils.str_fecha(pdt.horainicio), 
                                                   utils.str_hora_corta(pdt.horainicio), 
                                                   utils.str_hora_corta(pdt.horafin), 
                                                   utils.str_hora_corta(pdt.get_duracion()), 
                                                   utils.str_hora_corta(pdt.get_duracion()), 
                                                   pdt)) 
                horas = horas_trabajadas + horas_recuperacion
                horas.sort(lambda x, y: utils.orden_por_campo_o_id(x[-1], y[-1], "fecha"))
                horas = [i[:-1] for i in horas]
        # DIÁLOGO RESULTADOS
                id_parte = utils.dialogo_resultado(horas, 
                                                   "Horas trabajadas de producción y partes de trabajo de %s %s:" % (empleado.nombre, empleado.apellidos), 
                                                   multi = False, 
                                                   padre = self.wids['ventana'], 
                                                   cabeceras = ("ID", "Fecha", "Hora inicio", "Hora fin", "Duración", "Horas trabajadas"))
                if id_parte != -1:
                    tipo, ide = id_parte.split(":")
                    self.wids['ventana'].window.set_cursor(None)
                    if tipo == "PDP": 
                        parte = pclases.ParteDeProduccion.get(ide)
                        if parte.es_de_geotextiles():
                            from formularios import partes_de_fabricacion_rollos
                            v = partes_de_fabricacion_rollos.PartesDeFabricacionRollos(objeto = parte, usuario = self.usuario)  # @UnusedVariable
                        elif parte.es_de_fibra():
                            from formularios import partes_de_fabricacion_balas
                            v = partes_de_fabricacion_balas.PartesDeFabricacionBalas(objeto = parte, usuario = self.usuario)  # @UnusedVariable
                    elif tipo == "PDT": 
                        parte = pclases.ParteDeTrabajo.get(ide)
                        from formularios import partes_de_trabajo
                        v = partes_de_trabajo.PartesDeTrabajo(objeto = parte, usuario = self.usuario)  # @UnusedVariable
        self.wids['ventana'].window.set_cursor(None)

    def set_fecha_ini(self, b):
        try:
            fecha_defecto = utils.parse_fecha(self.wids['e_fecha_ini'].get_text())
        except: 
            fecha_defecto = mx.DateTime.localtime()
        else:
            self.wids['e_fecha_ini'].set_text(utils.str_fecha(utils.mostrar_calendario(fecha_defecto = fecha_defecto, padre = self.wids['ventana'])))
        
    def set_fecha_fin(self, b):
        try:
            fecha_defecto = utils.parse_fecha(self.wids['e_fecha_fin'].get_text())
        except: 
            fecha_defecto = mx.DateTime.localtime()
        else:
            self.wids['e_fecha_fin'].set_text(utils.str_fecha(utils.mostrar_calendario(fecha_defecto = fecha_defecto, padre = self.wids['ventana'])))
        
    def chequear_cambios(self):
        pass

    def buscar_partes_produccion(self, fecha_ini, fecha_fin):
        """
        Devuelve los resultados de una consulta SQLObject sobre partes de producción
        entre las fechas recibidas.
        """
        # Antes de procesar los datos es mejor concretarlos en la consulta y así generamos menos tráfico y consumimos menos CPU.
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
        #            pclases.ParteDeProduccion.q.fecha >= fecha_ini,
        #            pclases.ParteDeProduccion.q.fecha <= (fecha_fin+mx.DateTime.oneDay)
        #            ))
        # XXX:
        #solo para DEBUG:        print partes.count()
        #solo para DEBUG:        for p in partes:
        #solo para DEBUG:            print p.id, p.fecha, p.horainicio, p.horafin
        return partes

    def rellenar_horas(self, b = None):
        """
        Rellena el model con las horas trabajadas en cada parte del 
        rango de fechas.
        """
        try:
            dia, mes, anno = map(int, self.wids['e_fecha_ini'].get_text().split('/'))
        except:
            utils.dialogo_info(titulo = "FECHA INCORRECTA", texto = "La fecha inicial no es correcta. Use el formato día/mes/año")
            return
        fecha_ini = mx.DateTime.DateTimeFrom(day = dia, month = mes, year = anno) 
        dia, mes, anno = map(int, self.wids['e_fecha_fin'].get_text().split('/'))
        try:
            fecha_fin = mx.DateTime.DateTimeFrom(day = dia, month = mes, year = anno) 
        except:
            utils.dialogo_info(titulo = "FECHA INCORRECTA", texto = "La fecha inicial no es correcta. Use el formato día/mes/año")
            return
        model = self.wids['tv_horas'].get_model()
        model.clear()

        partes_produccion = self.buscar_partes_produccion(fecha_ini, fecha_fin)

        empleados = self.preparar_datos(partes_produccion, fecha_ini, fecha_fin)
        
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
        empleados += self.preparar_datos_recuperacion(partes_t, fecha_ini, fecha_fin)
        for empleado in empleados:
            model.append((empleado['nombre'],
                          empleado['horas'],
                          empleado['noche'],
                          empleado['extra'],
                          empleado['extra_n'],
                          empleado['total'],
                          empleado['id']))
        # Ahora los que no trabajaron:
        all_emps = pclases.Empleado.select(pclases.Empleado.q.planta == True)
        ids_emps_trabajo = [e['id'] for e in empleados]
        descanso = [e for e in all_emps if e.id not in ids_emps_trabajo]
        for e in descanso:
            model.append(("%s, %s (D)" % (e.apellidos, e.nombre),
                          "-",
                          "-",
                          "-",
                          "-",
                          "-",
                          e.id))
                           
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
        #ininoche = mx.DateTime.DateTimeDeltaFrom(hours = 22, minutes = 0)
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
                if ht.parteDeProduccion.se_solapa():
                    self.logger.warning("horas_trabajadas::preparar_datos -> El parte ID %d se solapa con otros de la misma línea. Si estaba verificado, lo desbloqueo para que se vuelva a revisar y lo ignoro para el cálculo actual." % (ht.parteDeProduccion.id))
                    ht.parteDeProduccion.bloqueado = False
                    ht.parteDeProduccion.syncUpdate()
                    continue
                if ht.empleado.id not in aux:
                    aux[ht.empleado.id] = {'pos': len(res), 'fechas': {}}
                    res.append({'nombre': "%s, %s" % (ht.empleado.apellidos, ht.empleado.nombre),
                                'horas': mx.DateTime.DateTimeDelta(0),
                                'extra': mx.DateTime.DateTimeDelta(0),
                                'extra_n': mx.DateTime.DateTimeDelta(0),
                                'noche': mx.DateTime.DateTimeDelta(0),
                                'total': mx.DateTime.DateTimeDelta(0),
                                'id': ht.empleado.id})
                pos = aux[ht.empleado.id]['pos']
                # Cálculo de las horas nocturnas:
                if ht.partedeproduccion.es_nocturno():
                    # OJO: Nunca se dará un parte que cubra dos franjas horarias de dos turnos
                    # diferentes, por tanto, si por ejemplo un empleado hace 2 horas de un parte de 6
                    # o las 6 horas son completas de noche (y por lo tanto las 2 del trabajador) o son 
                    # de día. Resumiendo: No hay partes que empiecem p. ej. a las 16:00 y acaben después 
                    # de las 22:00 y viceversa. De todas formas chequeo las dos horas por si acaso.
                    noche = ht.horas
                else:
                    noche = mx.DateTime.DateTimeDeltaFrom(hours = 0)
                # Cálculo de las horas extras: El primer parte del día es el de las 6:00. 
                # Si la hora de inicio del parte es inferior a esa, se considerará del día 
                # anterior a efectos de horas extras.
                # Compruebo qué tipo de fechas estoy manejando y preparo 
                # la variable de hora de fin de noche.
                if isinstance(ht.partedeproduccion.horainicio, datetime.time):
                    finnoche = datetime.time(hour = 6)
                else:
                    finnoche = mx.DateTime.DateTimeDeltaFrom(hours = 6, 
                                                             minutes = 0)
                if ht.partedeproduccion.horainicio < finnoche:
                    dia = (ht.partedeproduccion.fecha - mx.DateTime.oneDay)
                else:
                    dia = ht.partedeproduccion.fecha
                if dia not in aux[ht.empleado.id]['fechas']:
                    aux[ht.empleado.id]['fechas'][dia] = mx.DateTime.DateTimeDelta(0)
                if aux[ht.empleado.id]['fechas'][dia] + ht.horas > mx.DateTime.DateTimeDeltaFrom(hours = 8):
                    extra = aux[ht.empleado.id]['fechas'][dia] + \
                            ht.horas - \
                            mx.DateTime.DateTimeDeltaFrom(hours = 8)
                    aux[ht.empleado.id]['fechas'][dia] = mx.DateTime.DateTimeDeltaFrom(hours = 8) 
                else:
                    extra = mx.DateTime.DateTimeDelta(0)
                    aux[ht.empleado.id]['fechas'][dia] += ht.horas
                # Ya tengo las horas nocturas (variable noche) y las extras (extra). 
                # Guardo valores en el diccionario de resultados globales:
                if noche != 0:  # Un mx.DateTime... == 0 da True si es de 0 horas, 0 minutos...
                    res[pos]['noche'] += noche - extra
                    res[pos]['extra_n'] += extra
                else:
                    res[pos]['horas'] += ht.horas - extra
                    res[pos]['extra'] += extra
                res[pos]['total'] += ht.horas 
            i += 1
        for r in res:
            r['horas'] = r['horas'] != 0 and "%02d:%02d" % self.horas_minutos_from_delta(r['horas']) or ""
            r['extra_n'] = r['extra_n'] != 0 and "%02d:%02d" % self.horas_minutos_from_delta(r['extra_n']) or ""
            r['extra'] = r['extra'] != 0 and "%02d:%02d" % self.horas_minutos_from_delta(r['extra']) or ""
            r['noche'] = r['noche'] != 0 and "%02d:%02d" % self.horas_minutos_from_delta(r['noche']) or ""
            r['total'] = "%02d:%02d" % self.horas_minutos_from_delta(r['total']) or ""
        vpro.ocultar()
        return res

    def get_solo_hora(self, fecha):
        """
        Devuelve un DateTimeDelta con solo la hora de 
        la fecha recibida.
        """
        return mx.DateTime.DateTimeDeltaFrom(hours = fecha.hour, minutes = fecha.minute, seconds = fecha.second)

    def preparar_datos_recuperacion(self, partes_result, fecha_ini, fecha_fin):
        """
        A partir de los partes de producción recibidos genera una lista de diccionarios
        del tipo {'nombre': , 'horas': , 'extra': , 'noche': , 'extra_n': , 'total': , 'id': } donde se 
        guarda una entrada por empleado que contiene el nombre completo, las horas 
        "normales" trabajadas, las horas extras (día y noche), las que entran en franja nocturna 
        (de 22:00 a 6:00) y el total de horas entre todos los partes en los que trabajó.
        El id no se usará, pero es el del empleado.
        Todas las horas se devolverán en formato HH:MM
        """
        # TODO: Al calcularse de forma independiente, NO SE SUMA A LAS HORAS EXTRA (si lo fueran) y 
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
        res = []
        aux = {}
        #ininoche = mx.DateTime.DateTimeDeltaFrom(hours = 22, minutes = 0)
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
        for parte_de_trabajo in partes:
            vpro.set_valor(i/tot, "Analizando partes de trabajo...")
            if parte_de_trabajo.empleado.id not in aux:
                aux[parte_de_trabajo.empleado.id] = {'pos': len(res), 'fechas': {}}
                res.append({'nombre': "%s, %s (R)" % (parte_de_trabajo.empleado.apellidos, parte_de_trabajo.empleado.nombre),
                            'horas': mx.DateTime.DateTimeDelta(0),
                            'extra': mx.DateTime.DateTimeDelta(0),
                            'extra_n': mx.DateTime.DateTimeDelta(0),
                            'noche': mx.DateTime.DateTimeDelta(0),
                            'total': mx.DateTime.DateTimeDelta(0),
                            'id': parte_de_trabajo.empleado.id})
            pos = aux[parte_de_trabajo.empleado.id]['pos']
            # Cálculo de las horas nocturnas:
            if parte_de_trabajo.es_nocturno():
                noche = parte_de_trabajo.horas
            else:
                noche = mx.DateTime.DateTimeDeltaFrom(hours = 0)
            # Compruebo qué tipo de fechas estoy manejando y preparo 
            # la variable de hora de fin de noche.
            if isinstance(parte_de_trabajo.horafin, datetime.time):
                finnoche = datetime.time(hour = 6)
            else:
                finnoche = mx.DateTime.DateTimeDeltaFrom(hours = 6, 
                                                         minutes = 0)
            if self.get_solo_hora(parte_de_trabajo.horafin) < finnoche:
                dia = (parte_de_trabajo.horainicio - mx.DateTime.oneDay).strftime('%Y-%m-%d')
            else:
                dia = parte_de_trabajo.horainicio.strftime('%Y-%m-%d')
            if dia not in aux[parte_de_trabajo.empleado.id]['fechas']:
                aux[parte_de_trabajo.empleado.id]['fechas'][dia] = mx.DateTime.DateTimeDelta(0)
            if aux[parte_de_trabajo.empleado.id]['fechas'][dia] + parte_de_trabajo.horas > mx.DateTime.DateTimeDeltaFrom(hours = 8):
                extra = aux[parte_de_trabajo.empleado.id]['fechas'][dia] + \
                        parte_de_trabajo.horas - \
                        mx.DateTime.DateTimeDeltaFrom(hours = 8)
                aux[parte_de_trabajo.empleado.id]['fechas'][dia] = mx.DateTime.DateTimeDeltaFrom(hours = 8) 
            else:
                extra = mx.DateTime.DateTimeDelta(0)
                aux[parte_de_trabajo.empleado.id]['fechas'][dia] += parte_de_trabajo.horas
            # Ya tengo las horas nocturas (variable noche) y las extras (extra). 
            # Guardo valores en el diccionario de resultados globales:
            if noche != 0:  # Un mx.DateTime... == 0 da True si es de 0 horas, 0 minutos...
                res[pos]['noche'] += noche - extra
                res[pos]['extra_n'] += extra
            else:
                res[pos]['horas'] += parte_de_trabajo.horas - extra
                res[pos]['extra'] += extra
            res[pos]['total'] += parte_de_trabajo.horas 
            i += 1
        for r in res:
            r['horas'] = r['horas'] != 0 and "%02d:%02d" % self.horas_minutos_from_delta(r['horas']) or ""
            r['extra_n'] = r['extra_n'] != 0 and "%02d:%02d" % self.horas_minutos_from_delta(r['extra_n']) or ""
            r['extra'] = r['extra'] != 0 and "%02d:%02d" % self.horas_minutos_from_delta(r['extra']) or ""
            r['noche'] = r['noche'] != 0 and "%02d:%02d" % self.horas_minutos_from_delta(r['noche']) or ""
            r['total'] = "%02d:%02d" % self.horas_minutos_from_delta(r['total']) or ""
        vpro.ocultar()
        return res
   
    def horas_minutos_from_delta(self, delta):
        """
        Devuelve una tupla (h, m) con las horas y minutos en formato entero
        de un mx.DateTime.DateTimeDelta.
        """
        return (int(delta.hours), int(delta.minutes % 60))
        
    def actualizar(self, b):
        self.rellenar_horas()

    def imprimir(self, boton):
        """
        Imprime el TreeView de la ventana.
        """
        from informes.treeview2pdf import treeview2pdf
        from formularios.reports import abrir_pdf
        strdiaini = self.wids['e_fecha_ini'].get_text()
        strdiafin = self.wids['e_fecha_fin'].get_text()
        abrir_pdf(treeview2pdf(self.wids['tv_horas'], titulo = "Horas trabajadas", fecha = "Del %s al %s" % (strdiaini, strdiafin)))
    
    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a MS-Exel/OOoCalc.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        abrir_csv(treeview2csv(self.wids['tv_horas']))

if __name__ == '__main__':
    t = HorasTrabajadas()
