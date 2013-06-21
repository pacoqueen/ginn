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
## horas_trabajadas_dia.py - Resumen de horas trabajadas por día.
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 22 de mayo de 2006 -> Inicio
## 23 de mayo de 2006 -> Fin
## 30 de julio de 2006 -> Fork de horas_trabajadas.py
###################################################################
## FIXME:
## No vendría mal rehacer esta ventana. Hay cosas muy específicas
## que pueden cascar fácilmente ante el menor cambio. Aparte de 
## que casi todo el código es una guarrería.
## (It's crap, but it works!)
## 
###################################################################
from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
import mx.DateTime


class HorasTrabajadasDia(Ventana):
    def __init__(self, objeto = None, usuario = None):
        self.usuario = usuario
        Ventana.__init__(self, 'horas_trabajadas_dia.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_fecha/clicked': self.set_fecha,
                       'b_consultar/clicked': self.rellenar_horas,
                       'b_actualizar/clicked': self.actualizar, 
                       'b_imprimir/clicked': self.imprimir, 
                       'b_exportar/clicked': self.exportar}
        self.add_connections(connections)
        cols = (('Empleado', 'gobject.TYPE_STRING', False, True, True, None),
                ('Centro trabajo', 'gobject.TYPE_STRING', False, True, False, None),
                ('H. inicio','gobject.TYPE_STRING', False, True, False, None),
                ('H. fin','gobject.TYPE_STRING', False, True, False, None),
                ('Total hrs.','gobject.TYPE_STRING', False, True, False, None),
                ('Nocturnidad','gobject.TYPE_BOOLEAN', False, True, False, None),
                ('H. extra','gobject.TYPE_STRING', False, True, False, None),
                ('Prod. gtx.','gobject.TYPE_STRING', False, True, False, None),
                ('Prod. fibra','gobject.TYPE_STRING', False, True, False, None),
                ('Prod. geocomp.','gobject.TYPE_STRING', False, True, False, None),
                ('Mant. gtx.','gobject.TYPE_STRING', False, True, False, None),
                ('Mant. fibra','gobject.TYPE_STRING', False, True, False, None),
                ('Mant. geocomp.','gobject.TYPE_STRING', False, True, False, None),
                ('Almacén','gobject.TYPE_STRING', False, True, False, None),
                ('Varios','gobject.TYPE_STRING', False, True, False, None),
                ('Observaciones','gobject.TYPE_STRING', False, True, False, None),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_horas'], cols)
        self.wids['e_fecha'].set_text(mx.DateTime.localtime().strftime('%d/%m/%Y'))
        self.wids['tv_horas'].connect('row-activated', self.abrir_item)
        self.rellenar_horas()
        self.colorear()
        gtk.main()

    def colorear(self):
        """
        Colorea las filas en función de si el trabajador tenía que venir 
        según el calendario y no vino o si cumplió menos de las 8 horas 
        de su turno.
        """
        #######################################################################
        def cell_func(column, cell, model, itr, numcol):
            """
            Colorea la fina si el emplado no ha venido y tenía que venir.
            """
            color = None
            try:
                dia, mes, anno = [int(i) for i in 
                                  self.wids['e_fecha'].get_text().split('/')]
                fecha = mx.DateTime.DateTimeFrom(day = dia, 
                                                 month = mes, 
                                                 year = anno)
            except Exception, msg:
                self.logger.warning("horas_trabajadas_dia::colorear -> Probablemenete la fecha está mal escrita. Excepción: %s" % (msg))
            else:
                if "(D)" in model[itr][0]:
                    idempleado = model[itr][-1]
                    #empleado = pclases.Empleado.get(idempleado)
                    #grupo = empleado.grupo
                    grupos = pclases.Grupo.select(pclases.OR(pclases.Grupo.q.jefeturnoID == idempleado, 
                                                             pclases.Grupo.q.operario1ID == idempleado, 
                                                             pclases.Grupo.q.operario2ID == idempleado))
                    if grupos.count() >= 1:
                        for grupo in grupos: 
                            # Si pertenece a más de un grupo (oye, allá cada 
                            # cual) y uno de ellos tenía que venir, 
                            # acabará rojo.
                            laborables = pclases.Laborable.select(pclases.AND(
                                pclases.Laborable.q.fecha == fecha, 
                                pclases.Laborable.q.grupoID == grupo.id))
                            if laborables.count() >= 1:  
                                # El currélar tenía que venire.
                                color = "red"
            cell.set_property("cell-background", color)
        ########################################################################
        cols = self.wids['tv_horas'].get_columns()
        col = cols[0]
        cells = col.get_cell_renderers()
        for cell in cells:
            col.set_cell_data_func(cell, cell_func, 0)

    def set_fecha(self, b):
        try:
            fecha_defecto = utils.parse_fecha(self.wids['e_fecha'].get_text())
        except: 
            fecha_defecto = mx.DateTime.localtime()
        else:
            self.wids['e_fecha'].set_text("/".join(["%02d" % i for i in utils.mostrar_calendario(fecha_defecto = fecha_defecto, padre = self.wids['ventana'])]))
        
    def chequear_cambios(self):
        pass

    def buscar_partes_produccion(self, fecha):
        """
        Devuelve los resultados de una consulta SQLObject sobre partes de 
        producción en la fecha recibida.
        """
        # Antes de procesar los datos es mejor concretarlos en la consulta y 
        # así generamos menos tráfico y consumimos menos CPU.
        PDP = pclases.ParteDeProduccion
        OR = pclases.OR
        AND = pclases.AND
        fecha_ini = fecha_fin = fecha
        seis_am = mx.DateTime.DateTimeFrom(hour = 6) 
        medianoche = mx.DateTime.DateTimeFrom(hour = 0)
        # Por defecto va a poner el día de hoy en la parte de 
        # la fecha, pero afortunadamente al comparar un DateTimeDelta con un 
        # DateTime, lo va a ignorar.
        # Pertenecen al rango los que comiencen el día de inicio después 
        # de las 06:00
        limiteinf = AND(PDP.q.fecha == fecha_ini, PDP.q.horainicio >= seis_am)
        # Todos los que estén entre las dos fechas límite.
        centrales = AND(PDP.q.fecha > fecha_ini, PDP.q.fecha <= fecha_fin)
        # Y los que están en la franja peligrosa de comenzar entre de las 
        # 00:00 y las 6:00 del día siguiente al límite (pertenecen en realidad 
        # a la noche del día límite) y acaban antes de las 06:00 (si han 
        # comenzado antes de las 12, están incluidos en las condiciones 
        # anteriores).
        limitesup = AND(PDP.q.fecha == fecha_fin + mx.DateTime.oneDay, 
                        PDP.q.horainicio >= medianoche, 
                        PDP.q.horainicio <= seis_am, 
                        PDP.q.horafin <= seis_am)
        # Si la consulta entera va con """...""" sí rula. En el momento que 
        # lo metes en un SQLOp falla el __sqlrepr__()
        partes = PDP.select(OR(limiteinf, centrales, limitesup))
        #solo para DEBUG:        print partes.count()
        #solo para DEBUG:        for p in partes:
        #solo para DEBUG:            print p.id, p.fecha, p.horainicio, p.horafin
        return partes

    def convertir_valores_a_cadena(self, res):
        # Conversión a cadena
        for r in res:
            r['horas'] = r['total'] != 0 and "%02d:%02d" % self.horas_minutos_from_delta(r['total']) or ""
            r['horainicio'] = "%02d:%02d" % self.horas_minutos_from_delta(r['horainicio'])
            r['horafin'] = "%02d:%02d" % self.horas_minutos_from_delta(r['horafin'])
            r['noche'] = r['noche'] != 0 or r['extra_n'] != 0
            r['extra'] = r['extra'] + r['extra_n'] 
            r['extra'] = r['extra'] != 0 and "%02d:%02d" % self.horas_minutos_from_delta(r['extra']) or ""
            r['fib'] = r['fib'] != 0 and "%02d:%02d" % self.horas_minutos_from_delta(r['fib']) or ""
            r['gtx'] = r['gtx'] != 0 and "%02d:%02d" % self.horas_minutos_from_delta(r['gtx']) or ""
            r['gmp'] = r['gmp'] != 0 and "%02d:%02d" % self.horas_minutos_from_delta(r['gmp']) or ""
            r['mfib'] = r['mfib'] != 0 and "%02d:%02d" % self.horas_minutos_from_delta(r['mfib']) or ""
            r['mgtx'] = r['mgtx'] != 0 and "%02d:%02d" % self.horas_minutos_from_delta(r['mgtx']) or ""
            r['mgmp'] = r['mgmp'] != 0 and "%02d:%02d" % self.horas_minutos_from_delta(r['mgmp']) or ""
            r['almacen'] = r['almacen'] != 0 and "%02d:%02d" % self.horas_minutos_from_delta(r['almacen']) or ""
            r['varios'] = r['varios'] != 0 and "%02d:%02d" % self.horas_minutos_from_delta(r['varios']) or ""

    def rellenar_horas(self, b = None):
        """
        Rellena el model con las horas trabajadas en cada parte del 
        rango de fechas.
        """
        try:
            dia, mes, anno = map(int, self.wids['e_fecha'].get_text().split('/'))
        except:
            utils.dialogo_info(titulo = "FECHA INCORRECTA", texto = "La fecha no es correcta. Use el formato día/mes/año", padre = self.wids['ventana'])
            return
        fecha = mx.DateTime.DateTimeFrom(day = dia, month = mes, year = anno) 
        model = self.wids['tv_horas'].get_model()
        model.clear()

        partes_produccion = self.buscar_partes_produccion(fecha)
        empleados, aux = self.preparar_datos(partes_produccion, fecha)

        fecha_ini = fecha_fin = fecha
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
        
        empleados = self.preparar_datos_recuperacion(empleados, partes_t, fecha, aux)

        self.convertir_valores_a_cadena(empleados)

        for empleado in empleados:
            e = pclases.Empleado.get(empleado['id'])
            try:
                laborable = [l for l in e.grupo.laborables if l.fecha == fecha][0]
                nombre_empleado = "%s (%s)" % (empleado['nombre'], laborable.turno.nombre[0])
            except AttributeError:
                nombre_empleado = empleado['nombre']    # No tiene grupo.
            except IndexError:
                nombre_empleado = empleado['nombre']    # No tiene laborables asignados.
            padre = model.append(None, (nombre_empleado,
                                        e.centroTrabajo and e.centroTrabajo.nombre or "",
                                        empleado['horainicio'],
                                        empleado['horafin'],
                                        empleado['horas'],
                                        empleado['noche'],
                                        empleado['extra'],
                                        empleado['gtx'],
                                        empleado['fib'],
                                        empleado['gmp'],
                                        empleado['mgtx'],
                                        empleado['mfib'],
                                        empleado['mgmp'],
                                        empleado['almacen'],
                                        empleado['varios'],
                                        empleado['observaciones'],
                                        empleado['id']))
            for parte in empleado['partes']:
                try:
                    hts = [ht for ht in parte.horasTrabajadas if ht.empleadoid == empleado['id']]
                    horas_en_parte_del_empleado = sum([ht.horas for ht in hts])
                    model.append(padre, (utils.str_fecha(parte.fecha),
                                         parte.es_de_balas() and "fibra" or "geotextil",    
                                            # PLAN: De geocompuestos y tapicerías ni hablamos.
                                         utils.str_hora_corta(parte.horainicio),
                                         utils.str_hora_corta(parte.horafin),
                                         utils.str_hora_corta(parte.get_duracion()),
                                         parte.es_nocturno(),
                                         "",
                                         not parte.es_de_balas() and \
                                            utils.str_hora_corta(horas_en_parte_del_empleado) or "",
                                         parte.es_de_balas() and \
                                            utils.str_hora_corta(horas_en_parte_del_empleado) or "",
                                         "-",   # PLAN: Hasta que esté habilitada la línea de geocompuestos.
                                         "",
                                         "",
                                         "",
                                         "",
                                         "",
                                         "",
                                         parte.id))
                except AttributeError:  # Es parte de trabajo.
                    # OJO: NOTA: HARCODED. Pero es que no encuentro otra 
                    # forma de hacerlo.
                    ct_gtx, ct_fib, ct_gmp, ct_almacen = self.get_centros()
                    ct = parte.centroTrabajo
                    mgtx = mfib = mgmp = almacen = varios = ""
                    if ct != None and ct == ct_gtx:
                        mgtx = utils.str_hora_corta(parte.horas)
                    elif ct != None and ct == ct_fib:
                        mfib = utils.str_hora_corta(parte.horas)
                    elif ct != None and ct == ct_gmp:
                        mgmp = utils.str_hora_corta(parte.horas)
                    elif ct != None and ct == ct_almacen:
                        almacen = utils.str_hora_corta(parte.horas)
                    else:
                        varios = utils.str_hora_corta(parte.horas)
                    horas_en_parte_del_empleado = parte.horas
                    model.append(padre, 
                      (utils.str_fecha(parte.horainicio),
                       parte.centroTrabajo and parte.centroTrabajo.nombre or "",
                       utils.str_hora_corta(parte.horainicio),
                       utils.str_hora_corta(parte.horafin),
                       utils.str_hora_corta(parte.horas),
                       parte.es_nocturno(),
                       "",
                       "",
                       "",
                       "-",
                       mgtx,
                       mfib,
                       mgmp,
                       almacen,
                       varios,
                       parte.trabajo,
                       parte.id))
        # Ahora los que no trabajaron:
        all_emps = pclases.Empleado.select(
            pclases.AND(pclases.Empleado.q.planta == True,
                        pclases.Empleado.q.activo == True))
        ids_emps_trabajo = [e['id'] for e in empleados]
        descanso = [e for e in all_emps if e.id not in ids_emps_trabajo]
        mesAnno = mx.DateTime.DateTimeFrom(day = 1, mes = fecha.month, year = fecha.year) 
            # Los calendarios laborales siempre tienen 1 en el día.
        calendarios = pclases.CalendarioLaboral.select(pclases.CalendarioLaboral.q.mesAnno == mesAnno)
        for e in descanso:
            categoria = e.categoriaLaboral
            motivo = ""
            motivo_abr = " (D)"
            if categoria != None:
                try:
                    calendario = [c for c in calendarios if c.lineaDeProduccion == categoria.lineaDeProduccion][0]
                    if fecha in [f.fecha for f in calendario.festivos]:
                        motivo = "FESTIVO"
                        motivo_abr = " (FS)"
                    elif fecha in [v.fecha for v in calendario.vacaciones]:
                        motivo = "VACACIONES"
                        motivo_abr = " (VC)"
                    elif fecha in [a.fecha for a in e.ausencias]:
                        ausencia = [a for a in e.ausencias if a.fecha == fecha][0]
                        if ausencia.motivo != None:
                            motivo = ausencia.motivo.descripcion
                            if ausencia.motivo.convenio:
                                motivo_abr = " (DC)"
                            else:
                                motivo_abr = " (BL)"
                        else:
                            motivo = "PERMISO SOLICITADO"
                            motivo_abr = " (AP)"
                except IndexError:
                    pass    # No hay calendario relacionado con el trabajador. Puede que le falte categoría laboral,
                            # que ésta no tenga linea de producción o que no se haya asignado aún un calendario.
            model.append(None,("%s, %s%s" % (e.apellidos, e.nombre, motivo_abr),
                               e.centroTrabajo and e.centroTrabajo.nombre or "",
                               "--",
                               "--",
                               "--",
                               "",
                               "",
                               "",
                               "",
                               "",
                               "",
                               "",
                               "",
                               "",
                               "",
                               motivo,
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
    
    def new_dic_empleado(self, aux, res, ht):
        """
        Crea un nuevo diccionario de datos de trabajo del empleado en 
        las estructuras usadas para el cálculo de horas.
        """
        aux[ht.empleado.id] = {'pos': len(res), 'fechas': {}}
        res.append({'nombre': "%s, %s" % (
                                ht.empleado.apellidos, ht.empleado.nombre),
                    'horas': mx.DateTime.DateTimeDelta(0),  # Horas regulares
                    'extra': mx.DateTime.DateTimeDelta(0),  # Horas extras día
                    'extra_n': mx.DateTime.DateTimeDelta(0),# Horas extras noche
                    'noche': mx.DateTime.DateTimeDelta(0),  # Horas noche
                    'total': mx.DateTime.DateTimeDelta(0),  # Horas totales
                    # 'horainicio': ht.partedeproduccion.horainicio,
                        # Hora de inicio del primer parte
                    # 'horafin': ht.partedeproduccion.horafin,
                        # Hora fin del último parte del trabajador
                    'horainicio': None, # Hora de inicio del primer parte
                    'horafin': None,  # Hora fin del último parte del trabajador
                    'gtx': mx.DateTime.DateTimeDelta(0),
                        # Horas de producción en geotextiles
                    'fib': mx.DateTime.DateTimeDelta(0), 
                        # Horas de producción en fibra
                    'gmp': mx.DateTime.DateTimeDelta(0), 
                        # Horas de producción en geocompuestos
                    'mgtx': mx.DateTime.DateTimeDelta(0), 
                        # Horas de mantenimiento en geotextiles
                    'mfib': mx.DateTime.DateTimeDelta(0), 
                        # Horas de mantenimiento en fibra
                    'mgmp': mx.DateTime.DateTimeDelta(0), 
                        # Horas de mantenimiento en geocompuestos
                    'almacen': mx.DateTime.DateTimeDelta(0), 
                        # Horas en almacén
                    'varios': mx.DateTime.DateTimeDelta(0), 
                        # Horas en "varios" (no producción, ni mantenimiento 
                        # ni almacén)
                    'observaciones': '',    # Observaciones.
                    'partes': [],
                    'id': ht.empleado.id})

    
    def preparar_datos(self, partes_result, fecha):
        """
        A partir de los partes de producción recibidos genera una lista de 
        diccionarios del tipo {'nombre': , 'horas': , 'extra': , 'noche': , 
        'extra_n': , 'total': , 'id': } donde se guarda una entrada por 
        empleado que contiene el nombre completo, las horas "normales" 
        trabajadas, las horas extras (día y noche), las que entran en franja 
        nocturna (de 22:00 a 6:00) y el total de horas entre todos los partes 
        en los que trabajó.
        El id no se usará, pero es el del empleado.
        Todas las horas se devolverán en formato HH:MM
        """
        # WTF: Esto hay que refactorizarlo PERO YA.
        # NOTA: fechaini y fechafin no se llegan a usar. Las conservo 
        # porque aún está en pruebas el funcionamiento de la distribución 
        # de horas (se usaba para discriminar los partes pertenecientes
        # a otra jornada laboral distinta del día natural.
        res = []
        aux = {}
        try:
            turnonoche = pclases.Turno.select(pclases.Turno.q.noche == True)[0] 
            # No debería haber ni más ni menos que 1.
        except IndexError:
            utils.dialogo_info(titulo = "TURNO DE NOCHE NO ENCONTRADO",
                               texto = "No se encontró un turno de noche definido.\nDebe configurar uno.",
                               padre = self.wids['ventana'])
            return
        ininoche = mx.DateTime.DateTimeDeltaFrom(hours = turnonoche.horainicio.hour,  # @UnusedVariable
                                                 minutes = turnonoche.horainicio.minute)
        finnoche = mx.DateTime.DateTimeDeltaFrom(hours = turnonoche.horafin.hour, 
                                                 minutes = turnonoche.horafin.minute)
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
                if ht.empleado.id not in aux:
                    self.new_dic_empleado(aux, res, ht)
                pos = aux[ht.empleado.id]['pos']
                # Hora de inicio y fin de trabajo (hora inicio del primer 
                # parte y fin del último parte)
                # fin con la fecha de fin del último parte tratado.
                # FIXME: Si por ejemplo 2 partes: de 22:00 a 5:00 y de 5:00 a 
                #   6:00, en lugar de poner horainicio y horafin a 22:00 y 6:00
                #   respectivamente, pone como horainicio 5:00 y como horafin 
                #   6:00. Sin embargo, el cómputo de horas sí es correcto.
                if res[pos]['horainicio'] == None or res[pos]['horainicio'] > ht.partedeproduccion.fechahorainicio:
                    res[pos]['horainicio'] = ht.partedeproduccion.fechahorainicio
                if res[pos]['horafin'] == None or res[pos]['horafin'] < ht.partedeproduccion.fechahorafin or \
                    ht.partedeproduccion.fechahorafin < res[pos]['fechahorainicio']:  # Es del día siguiente
                    res[pos]['horafin'] = ht.partedeproduccion.fechahorafin
                if ht.partedeproduccion not in res[pos]['partes']:
                    res[pos]['partes'].append(ht.partedeproduccion)
                # Cálculo de las horas nocturnas:
                #if ht.partedeproduccion.horainicio >= ininoche and \
                #    ht.partedeproduccion.horafin <= finnoche:
                if ht.partedeproduccion.es_nocturno():
                    # OJO: Nunca se dará un parte que cubra dos franjas 
                    # horarias de dos turnos diferentes, por tanto, si por 
                    # ejemplo un empleado hace 2 horas de un parte de 6
                    # o las 6 horas son completas de noche (y por lo tanto 
                    # las 2 del trabajador) o son de día. Resumiendo: No hay 
                    # partes que empiecen p. ej. a las 16:00 y acaben después 
                    # de las 22:00 y viceversa. De todas formas chequeo las 
                    # dos horas por si acaso. 
                    # IMPORTANTE: si se sale de la franja de noche, quedará 
                    # marcado como NO NOCTURNO.
                    noche = ht.horas
                else:
                    noche = mx.DateTime.DateTimeDeltaFrom(hours = 0)
                # Cálculo de las horas extras: El primer parte del día es el de 
                # las 6:00. 
                # Si la hora de inicio del parte es inferior a esa, se 
                # considerará del día anterior a efectos de horas extras.
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
                if ht.partedeproduccion.es_de_balas():
                    res[pos]['fib'] += ht.horas
                else:   
                    # PLAN: Hasta se que abra la línea de geocompuestos, 
                    # si no es de bala, es de geotextiles.
                    res[pos]['gtx'] += ht.horas
                res[pos]['total'] += ht.horas 
                # FIXME: No sé bien por qué no funciona el cálculo anterior 
                # de horas extras, así que:
                ocho_horas = mx.DateTime.DateTimeDeltaFrom(hours = 8)
                if res[pos]['total'] > ocho_horas:
                    res[pos]['extra'] = res[pos]['total'] - ocho_horas
            i += 1
        vpro.ocultar()
        return res, aux

    def get_solo_hora(self, fecha):
        """
        Devuelve un DateTimeDelta con solo la hora de 
        la fecha recibida.
        """
        return mx.DateTime.DateTimeDeltaFrom(hours = fecha.hour, 
                                             minutes = fecha.minute, 
                                             seconds = fecha.second)

    def preparar_datos_recuperacion(self, empleados, partes_result, fecha, aux):
        """
        A partir de los partes de producción recibidos genera una lista de diccionarios
        del tipo {'nombre': , 'horas': , 'extra': , 'noche': , 'extra_n': , 'total': , 'id': } donde se 
        guarda una entrada por empleado que contiene el nombre completo, las horas 
        "normales" trabajadas, las horas extras (día y noche), las que entran en franja nocturna 
        (de 22:00 a 6:00) y el total de horas entre todos los partes en los que trabajó.
        El id no se usará, pero es el del empleado.
        Todas las horas se devolverán en formato HH:MM
        """
        res = empleados
        # aux = {}
        try:
            turnonoche = pclases.Turno.select(pclases.Turno.q.noche == True)[0] 
        except IndexError:
            utils.dialogo_info(titulo = "TURNO DE NOCHE NO ENCONTRADO",
                               texto = "No se encontró un turno de noche definido.\nDebe configurar uno.",
                               padre = self.wids['ventana'])
            return
        ininoche = mx.DateTime.DateTimeDeltaFrom(hours = turnonoche.horainicio.hour, 
                                                 minutes = turnonoche.horainicio.minute)
        finnoche = mx.DateTime.DateTimeDeltaFrom(hours = turnonoche.horafin.hour, 
                                                 minutes = turnonoche.horafin.minute)
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
            if ht.empleado.id not in aux:
                self.new_dic_empleado(aux, res, ht)
            pos = aux[ht.empleado.id]['pos']
            # Hora de inicio y fin de trabajo (hora inicio del primer parte y fin del último parte)
            # fin con la fecha de fin del último parte tratado.
            if res[pos]['horainicio'] == None or res[pos]['horainicio'] > utils.DateTime2DateTimeDelta(ht.horainicio):
                res[pos]['horainicio'] = utils.DateTime2DateTimeDelta(ht.horainicio)
            if res[pos]['horafin'] == None or res[pos]['horafin'] < utils.DateTime2DateTimeDelta(ht.horafin) or \
               utils.DateTime2DateTimeDelta(ht.horafin) < res[pos]['horainicio']:
                res[pos]['horafin'] = utils.DateTime2DateTimeDelta(ht.horafin)
            if ht not in res[pos]['partes']:
                res[pos]['partes'].append(ht)   # Aquí HT es un parte de trabajo, que equivale a los HT de los PDP.
            # Cálculo de las horas nocturnas:
            if self.get_solo_hora(ht.horainicio) >= ininoche and \
               self.get_solo_hora(ht.horafin) <= finnoche:
                noche = ht.horas
            else:
                noche = mx.DateTime.DateTimeDeltaFrom(hours = 0)
            if self.get_solo_hora(ht.horafin) < finnoche:
                dia = (ht.horainicio - mx.DateTime.oneDay).strftime('%Y-%m-%d')
            else:
                dia = ht.horainicio.strftime('%Y-%m-%d')
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
            # OJO: NOTA: HARCODED. Pero es que no encuentro otra forma de hacerlo.
            ct_gtx, ct_fib, ct_gmp, ct_almacen = self.get_centros()
            ct = ht.centroTrabajo
            if ct != None and ct == ct_gtx:
                res[pos]['mgtx'] += ht.horas
            elif ct != None and ct == ct_fib:
                res[pos]['mfib'] += ht.horas
            elif ct != None and ct == ct_gmp:
                res[pos]['mgmp'] += ht.horas
            elif ct != None and ct == ct_almacen:
                res[pos]['almacen'] += ht.horas
            else:
                res[pos]['varios'] += ht.horas
            res[pos]['total'] += ht.horas
            res[pos]['observaciones'] += "%s " % ht.trabajo
            # FIXME: No sé bien por qué no funciona el cálculo anterior de horas extras, así que:
            ocho_horas = mx.DateTime.DateTimeDeltaFrom(hours = 8)
            if res[pos]['total'] > ocho_horas:
                res[pos]['extra'] = res[pos]['total'] - ocho_horas
            i += 1
        vpro.ocultar()
        return res
   
    def get_centros(self):
        try:
            ct_fibra = pclases.CentroTrabajo.select(pclases.OR(pclases.CentroTrabajo.q.nombre.contains('ibra'),
                                                               pclases.CentroTrabajo.q.nombre.contains('FIBRA')))[0]
        except IndexError:
            self.logger.warning("horas_trabajadas_dia.py: No se encontró centro de trabajo de fibra.")
            ct_fibra = None
        try:
            ct_gtx = pclases.CentroTrabajo.select(pclases.OR(pclases.CentroTrabajo.q.nombre.contains('eotextil'),
                                                             pclases.CentroTrabajo.q.nombre.contains('GEOTEXTIL')))[0]
        except IndexError:
            self.logger.warning("horas_trabajadas_dia.py: No se encontró centro de trabajo de geotextiles.")
            ct_gtx = None
        try:
            ct_gmp = pclases.CentroTrabajo.select(pclases.OR(
                    pclases.CentroTrabajo.q.nombre.contains('eocompuesto'),
                    pclases.CentroTrabajo.q.nombre.contains('GEOCOMPUESTO'),
                    pclases.CentroTrabajo.q.nombre.contains('omercializado'),
                    pclases.CentroTrabajo.q.nombre.contains('COMERCIALIZADO'))
                )[0]
        except IndexError:
            self.logger.warning("horas_trabajadas_dia.py: No se encontró centro de trabajo de fibra.")
            ct_gmp = None
        try:
            ct_alm = pclases.CentroTrabajo.select(pclases.OR(pclases.CentroTrabajo.q.nombre.contains('lmac'),
                                                               pclases.CentroTrabajo.q.nombre.contains('ALMAC')))[0]
        except IndexError:
            self.logger.warning("horas_trabajadas_dia.py: No se encontró centro de trabajo de fibra.")
            ct_alm = None
        return ct_gtx, ct_fibra, ct_gmp, ct_alm

    def horas_minutos_from_delta(self, delta):
        """
        Devuelve una tupla (h, m) con las horas y minutos en formato entero
        de un mx.DateTime.DateTimeDelta.
        """
        try:
            return (int(delta.hours), int(delta.minutes % 60))
        except AttributeError:      # No es un Delta.
            return (delta.hour, delta.minute)
        
    def actualizar(self, b):
        self.rellenar_horas()

    def abrir_item(self, tv, path, view_column):
        self.wids['ventana'].window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        while gtk.events_pending(): gtk.main_iteration(False)
        model = tv.get_model()
        if model[path].parent == None:
            # Empleado seleccionado
            idempleado = model[path][-1]
            empleado = pclases.Empleado.get(idempleado)
            from formularios import empleados
            self.wids['ventana'].window.set_cursor(None)
            ventanaempleado = empleados.Empleados(empleado)  # @UnusedVariable
        else:
            # Parte seleccionado.
            # OJO: Para identificar si es parte de producción o de trabajo miro la duración en producción en el model.
            if model[path][7] != "":    # Es de GTX:
                idparte = model[path][-1]
                parte = pclases.ParteDeProduccion.get(idparte)
                from formularios import partes_de_fabricacion_rollos
                self.wids['ventana'].window.set_cursor(None)
                ventanaparte = partes_de_fabricacion_rollos.PartesDeFabricacionRollos(parte)  # @UnusedVariable
            elif model[path][8] != "":   # Es de fibra
                idparte = model[path][-1]
                parte = pclases.ParteDeProduccion.get(idparte)
                from formularios import partes_de_fabricacion_balas
                self.wids['ventana'].window.set_cursor(None)
                ventanaparte = partes_de_fabricacion_balas.PartesDeFabricacionBalas(parte)  # @UnusedVariable
            else:   # Debe ser parte de trabajo, no queda otra.
                idparte = model[path][-1]
                parte = pclases.ParteDeTrabajo.get(idparte)
                from formularios import partes_de_trabajo
                self.wids['ventana'].window.set_cursor(None)
                ventanaparte = partes_de_trabajo.PartesDeTrabajo(parte)  # @UnusedVariable
    
    def imprimir(self, boton):
        """
        Imprime el TreeView de la ventana.
        """
        from informes.treeview2pdf import treeview2pdf
        from formularios.reports import abrir_pdf
        strfecha = self.wids['e_fecha'].get_text()
        abrir_pdf(treeview2pdf(self.wids['tv_horas'], titulo = "Horas trabajadas", fecha = strfecha))
    
    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a MS-Exel/OOoCalc.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        abrir_csv(treeview2csv(self.wids['tv_horas']))

if __name__ == '__main__':
    t = HorasTrabajadasDia()
