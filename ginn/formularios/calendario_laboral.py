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
## calendario_laboral.py - Ventana para configurar los laborables.
###################################################################
## NOTAS:
## 
###################################################################
## DONE:
## + Ya veré si meto algo para que se vea la composición de cada
##   grupo.
###################################################################
## Changelog:
## 20 de julio de 2006 -> Inicio
## 
###################################################################
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sqlobject
import sys
from framework import pclases
import mx.DateTime
try:
    import geninformes
except ImportError:
    import geninformes
sys.path.append('.')
import ventana_progreso
import re
from utils import _float as float
import os

class CalendarioLaboral(Ventana):
        
    def __init__(self, mes = None, anno = None, ldp = None, solo_lectura = False, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases  de la 
        línea de producción con la que comenzar la ventana.
        """
        self.escritura = not solo_lectura
        Ventana.__init__(self, 'calendario_laboral.glade', None)
        connections = {'b_salir/clicked': self.salir
                       }
        self.add_connections(connections)
        self.cal = []    # Los Gtk.Table no tienen método para acceder a los hijos por fila y columna (flipa!).
                         # Así que los iré guardando aquí para poderlos crear y destruir sobre la marcha.
        utils.rellenar_lista(self.wids['cbe_linea'], 
                             [(l.id, l.nombre) for l in pclases.LineaDeProduccion.select(orderBy='nombre')])
        if mes == None:
            mes = mx.DateTime.localtime().month
        if anno == None:
            anno = mx.DateTime.localtime().year
        self.wids['sp_mes'].set_value(mes)
        self.wids['sp_anno'].set_value(anno)
        self.wids['cbe_linea'].connect('changed', self.rellenar_widgets)
        self.wids['sp_mes'].connect('value-changed', self.rellenar_widgets)
        self.wids['sp_anno'].connect('value-changed', self.rellenar_widgets)
        if ldp == None:
            utils.combo_set_from_db(self.wids['cbe_linea'], pclases.LineaDeProduccion.select(orderBy='nombre')[0].id)
        else:
            utils.combo_set_from_db(self.wids['cbe_linea'], ldp.id)
        gtk.main()

    def rellenar_widgets(self, *args, **kw):
        """
        A partir de la línea de producción, mes y año; construye el calendario
        laboral por grupo y muestra los turnos asignados.
        """
        mes = int(self.wids['sp_mes'].get_value())
        anno = int(self.wids['sp_anno'].get_value())
        self.montar_tabla_turnos(mes, anno)
        self.wids['tcal'].set_sensitive(self.escritura)
    
    def destruir_tabla_anterior(self):
        for child in self.wids['tcal'].get_children():
            child.destroy()
        self.cal = []
    
    def get_calendario(self, mes, anno):
        """
        Devuelve el calendario a mostrar.
        Si no existe, lo crea.
        """
        fechacalendario = mx.DateTime.DateTimeFrom(day = 1, month = mes, year = anno)
        idldp = utils.combo_get_value(self.wids['cbe_linea'])
        if idldp == None: return None, None
        ldp = pclases.LineaDeProduccion.get(idldp)
        calendarios = pclases.CalendarioLaboral.select(pclases.AND(pclases.CalendarioLaboral.q.mesAnno == fechacalendario,
                                                                   pclases.CalendarioLaboral.q.lineaDeProduccionID == idldp))
            # Para crear y buscar calendarios siempre se usará 1 como día. Lo importante es mes y año.
        if calendarios.count() == 0: # Crear
            calendario = pclases.CalendarioLaboral(lineaDeProduccion = ldp, mesAnno = fechacalendario)
            pclases.Auditoria.nuevo(calendario, self.usuario, __file__)
            # Añado los festivos genéricos.
            festivos = tuple([(f.fecha.day, f.fecha.month) for f in pclases.FestivoGenerico.select() \
                                if f.fecha.month == calendario.mesAnno.month])
            for dia, mes in festivos:
                fechafestivo = mx.DateTime.DateTimeFrom(day = dia, month = mes, year = calendario.mesAnno.year)
                festivo = pclases.Festivo(calendarioLaboral = calendario, fecha = fechafestivo)
                pclases.Auditoria.nuevo(festivo, self.usuario, __file__)
        else:
            calendario = calendarios[0]
        return calendario, idldp 
        
    def montar_tabla_turnos(self, mes, anno):
        vpro = ventana_progreso.VentanaActividad()
        vpro.mostrar()
        cacheturnos = tuple([(t.id, "%s (%s - %s)" % (t.nombre, t.horainicio.strftime("%H:%M"), \
                                t.horafin.strftime("%H:%M"))) for t in pclases.Turno.select(orderBy='horainicio')])
        calendario, idldp = self.get_calendario(mes, anno)
        if calendario != None and idldp != None: 
            self.objeto = calendario    # Es por eficiencia, para evitar llamadas posteriores 
                                        # a la búsqueda del calendario actual.
            festivos = tuple([(f.fecha.day, f.fecha.month) for f in calendario.festivos])
            vacaciones = tuple([(f.fecha.day, f.fecha.month) for f in calendario.vacaciones])
            dias_validos = get_dias_validos(mes, anno)
            consulta = """jefeturno_id IN 
                            (SELECT id FROM empleado 
                              WHERE categoria_laboral_id IN 
                                (SELECT id FROM categoria_laboral 
                                 WHERE categoria_laboral.linea_de_produccion_id = %d
                                )
                            ) 
                          OR operario1_id IN 
                            (SELECT id FROM empleado 
                              WHERE categoria_laboral_id IN 
                                (SELECT id FROM categoria_laboral 
                                 WHERE categoria_laboral.linea_de_produccion_id = %d
                                )
                            )
                          OR operario2_id IN 
                            (SELECT id FROM empleado 
                              WHERE categoria_laboral_id IN 
                                (SELECT id FROM categoria_laboral 
                                 WHERE categoria_laboral.linea_de_produccion_id = %d
                                )
                            )
                          """ % (idldp, idldp, idldp)
            # Filtro los grupos y me quedo con los de la línea de producción en cuestión. La línea está 
            # relacionada con ellos mediante la categoría laboral de sus empleados.
            grupos = pclases.Grupo.select(consulta)
            self.destruir_tabla_anterior()
            self.wids['tcal'].resize(len(dias_validos), grupos.count()+2)
            self.cal = []
            if grupos.count() == 0:
                utils.dialogo_info(titulo = "SIN GRUPOS DE TRABAJO",
                                   texto = "Debe definir grupos de trabajo antes asignar\nturnos en el calendario laboral.",
                                   padre = self.wids['ventana'])
            else:   
                for x in xrange(grupos.count()+3):
                    l = []
                    for y in xrange(len(dias_validos)+1):
                        l.append(None)
                    self.cal.append(l)
                origen = gtk.Label("""<i>Día\Grupo</i>""")
                origen.set_use_markup(True)
                self.wids['tcal'].attach(origen, 0, 1, 0, 1)
                self.cal[0][0] = origen
                tips = gtk.Tooltips()
                for i in xrange(1,grupos.count()+1):
                    cabecera = gtk.EventBox()
                    label_cabecera = gtk.Label(grupos[i-1].nombre)
                    cabecera.add(label_cabecera)
                    empleados_grupo = "%s, %s\n%s, %s\n%s, %s" % (grupos[i-1].jefeturno.apellidos, 
                                                                  grupos[i-1].jefeturno.nombre, 
                                                                  grupos[i-1].operario1.apellidos, 
                                                                  grupos[i-1].operario1.nombre,
                                                                  grupos[i-1].operario2.apellidos, 
                                                                  grupos[i-1].operario2.nombre)
                    tips.set_tip(cabecera, empleados_grupo)
                    tips.enable()
                    # tips.set_delay(0)
                    self.wids['tcal'].attach(cabecera, i, i+1, 0, 1)
                    self.cal[i][0] = cabecera
                    vpro.mover()
                for dia in dias_validos:
                    vpro.mover()
                    labeldia = build_label_dia(dia, mes, anno)
                    self.wids['tcal'].attach(labeldia, 0, 1, dia, dia+1)
                    self.cal[0][dia] = labeldia
                    if (dia, mes) in festivos:
                        labelfestivo = gtk.Label("<big><b>F    E    S    T    I    V    O</b></big>")
                        labelfestivo.set_use_markup(True)
                        self.wids['tcal'].attach(labelfestivo, 1, grupos.count()+1, dia, dia+1)
                        self.cal[1][dia] = labelfestivo
                        vpro.mover()
                    elif (dia, mes) in vacaciones:
                        labelvacaciones = gtk.Label("<big><b>V    A    C    A    C    I    O    N    E    S</b></big>")
                        labelvacaciones.set_use_markup(True)
                        self.wids['tcal'].attach(labelvacaciones, 1, grupos.count()+1, dia, dia+1)
                        self.cal[1][dia] = labelvacaciones
                        vpro.mover()
                    else:
                        for igrupo in xrange(1, grupos.count()+1):
                            laborableactual = [l for l in self.objeto.laborables if l.fecha.day == dia and \
                                                                          l.fecha.month == self.objeto.mesAnno.month and \
                                                                          l.fecha.year == self.objeto.mesAnno.year and \
                                                                          l.grupo == grupos[igrupo-1]]
                            vpro.mover()
                            if laborableactual == []:
                                turnoid = None
                            else:
                                turnoid = laborableactual[0].turno and laborableactual[0].turno.id or None
                            combo_turno = build_combo_dia_grupo(dia, 
                                                                grupos[igrupo-1].id, 
                                                                self.actualizar_turno, 
                                                                cacheturnos, 
                                                                turnoid)
                            self.wids['tcal'].attach(combo_turno, igrupo, igrupo+1, dia, dia+1)
                            self.cal[igrupo][dia] = combo_turno
                            vpro.mover()
                    checkboxes = build_checkboxes(dia, 
                                                  self.actualizar_vacaciones, 
                                                  self.actualizar_festivo, 
                                                  self.actualizar_laborable,
                                                  (dia, mes) in vacaciones, 
                                                  (dia, mes) in festivos)
                    self.wids['tcal'].attach(checkboxes, grupos.count()+2, grupos.count()+3, dia, dia+1)
                    self.cal[grupos.count()+2][dia] = checkboxes
        self.wids['tcal'].show_all()
        vpro.ocultar()

    def actualizar_laborable(self, ch):
        dia = int(ch.get_name())
        mes = int(self.wids['sp_mes'].get_value())
        anno = int(self.wids['sp_anno'].get_value())
        calendario, idldp = self.get_calendario(mes, anno)
        if ch.get_active(): # Convierto el día en laborable. Relleno la línea de combos.
            # Borro widgets anteriores:
            cols = self.wids['tcal'].get_property("n-columns")
            for col in xrange(1, cols-2):
                if self.cal[col][dia] != None:
                    self.cal[col][dia].destroy()
            consulta = """jefeturno_id IN 
                            (SELECT id FROM empleado 
                              WHERE categoria_laboral_id IN 
                                (SELECT id FROM categoria_laboral 
                                 WHERE categoria_laboral.linea_de_produccion_id = %d
                                )
                            ) 
                          OR operario1_id IN 
                            (SELECT id FROM empleado 
                              WHERE categoria_laboral_id IN 
                                (SELECT id FROM categoria_laboral 
                                 WHERE categoria_laboral.linea_de_produccion_id = %d
                                )
                            )
                          OR operario2_id IN 
                            (SELECT id FROM empleado 
                              WHERE categoria_laboral_id IN 
                                (SELECT id FROM categoria_laboral 
                                 WHERE categoria_laboral.linea_de_produccion_id = %d
                                )
                            )
                          """ % (idldp, idldp, idldp)
            # Filtro los grupos y me quedo con los de la línea de producción en cuestión. La línea está 
            # relacionada con ellos mediante la categoría laboral de sus empleados.
            grupos = pclases.Grupo.select(consulta)
            cacheturnos = tuple([(t.id, "%s (%s - %s)" % (t.nombre, t.horainicio.strftime("%H:%M"), \
                                t.horafin.strftime("%H:%M"))) for t in pclases.Turno.select(orderBy='horainicio')])
            for igrupo in xrange(1, grupos.count()+1):
                laborableactual = [l for l in self.objeto.laborables if l.fecha.day == dia and \
                                                              l.fecha.month == self.objeto.mesAnno.month and \
                                                              l.fecha.year == self.objeto.mesAnno.year and \
                                                              l.grupo == grupos[igrupo-1]]
                if laborableactual == []:
                    turnoid = None
                else:
                    turnoid = laborableactual[0].turno and laborableactual[0].turno.id or None
                combo_turno = build_combo_dia_grupo(dia, 
                                                    grupos[igrupo-1].id, 
                                                    self.actualizar_turno, 
                                                    cacheturnos, 
                                                    turnoid)
                self.wids['tcal'].attach(combo_turno, igrupo, igrupo+1, dia, dia+1)
                self.cal[igrupo][dia] = combo_turno
                self.wids['tcal'].show_all()
        else:               # Ya no es laborable. Borro todos los laborables del día para cada grupo.
            for laborable in [l for l in self.objeto.laborables if l.fecha.day == dia and \
                                                                       l.fecha.month == mes and \
                                                                       l.fecha.year == anno]:
                laborable.destroy(ventana = __file__)


    def actualizar_festivo(self, ch):
        dia = int(ch.get_name())
        mes = int(self.wids['sp_mes'].get_value())
        anno = int(self.wids['sp_anno'].get_value())
        fecha = mx.DateTime.DateTimeFrom(day = dia, month = mes, year = anno)
        if ch.get_active(): # Convierto en festivo.
            festivo = pclases.Festivo(calendarioLaboral = self.objeto, fecha = fecha)
            pclases.Auditoria.nuevo(festivo, self.usuario, __file__)
            # Borro widgets anteriores:
            cols = self.wids['tcal'].get_property("n-columns")
            for col in xrange(1, cols-2):
                if self.cal[col][dia] != None:
                    self.cal[col][dia].destroy()
            # Y muestro nueva leyenda:
            labelfestivo = gtk.Label("<big><b>F    E    S    T    I    V    O</b></big>")
            labelfestivo.set_use_markup(True)
            self.wids['tcal'].attach(labelfestivo, 1, cols-2, dia, dia+1)
            self.cal[1][dia] = labelfestivo
            self.wids['tcal'].show_all()
        else:               # Borrarlo
            for festivo in [f for f in self.objeto.festivos if f.fecha == fecha]:
                festivo.destroy(ventana = __file__)

    def actualizar_vacaciones(self, ch):
        dia = int(ch.get_name())
        mes = int(self.wids['sp_mes'].get_value())
        anno = int(self.wids['sp_anno'].get_value())
        fecha = mx.DateTime.DateTimeFrom(day = dia, month = mes, year = anno)
        if ch.get_active(): # Convierto en vacaciones.
            vacaciones = pclases.Vacaciones(calendarioLaboral = self.objeto, fecha = fecha)
            pclases.Auditoria.nuevo(vacaciones, self.usuario, __file__)
            # Borro widgets anteriores:
            cols = self.wids['tcal'].get_property("n-columns")
            for col in xrange(1, cols-2):
                if self.cal[col][dia] != None:
                    self.cal[col][dia].destroy()
            # Y muestro nueva leyenda:
            labelvacaciones = gtk.Label("<big><b>V    A    C    A    C    I    O    N    E    S</b></big>")
            labelvacaciones.set_use_markup(True)
            self.wids['tcal'].attach(labelvacaciones, 1, cols-2, dia, dia+1)
            self.cal[1][dia] = labelvacaciones
            self.wids['tcal'].show_all()
        else:               # Borrarlo
            for vacaciones in [v for v in self.objeto.vacaciones if v.fecha == fecha]:
                vacaciones.destroy(ventana = __file__)

    def actualizar_turno(self, cbe):
        dia, idgrupo = map(int, cbe.get_name().split("_"))
        mes = int(self.wids['sp_mes'].get_value())
        anno = int(self.wids['sp_anno'].get_value())
        grupo = pclases.Grupo.get(idgrupo)
        idturno = utils.combo_get_value(cbe)
        if idturno != None:
            turno = pclases.Turno.get(idturno)
        else:
            turno = None
        laborable = [l for l in self.objeto.laborables if l.fecha.day == dia and l.grupo == grupo]
        if laborable == []:
            nuevolaborable = pclases.Laborable(turno = turno, 
                                               grupo = grupo, 
                                               calendarioLaboral = self.objeto, 
                                               fecha = mx.DateTime.DateTimeFrom(day = dia, month = mes, year = anno))
            pclases.Auditoria.nuevo(nuevolaborable, self.usuario, __file__)
        else:
            laborable = laborable[0]
            laborable.turno = turno
        cbe.child.modify_base(gtk.STATE_NORMAL, cbe.child.get_colormap().alloc_color(get_color_turno(idturno)))

    def chequear_cambios(self):
        """
        Sobreescribo método de la clase padre para que no haga nada.
        """
        pass

def build_combo_dia_grupo(dia, idgrupo, funcion, turnos, turnoid):
    """
    Construye y devuelve un comboBoxEntry.
    Conecta la señal "changed" a 'funcion'.
    El nombre estará compuesto por el día y el id del grupo separados por «_».
    Los valores de la lista son los de los turnos definidos en la BD (que como
    mínimo deberían ser: Mañana, Tarde, Noche, Recuperación)
    [Los festivos se toman de FestivosGenericos, no se consideran turno].
    [Vacaciones y festivos adicionales se pueden marcar mediante dos checkboxes
    en el lateral derecho]
    'turnos' es una lista de tuplas (id, nombre) de los turnos ordenada por 
    hora de inicio.
    turnoid es el ID del turno que debe aparecer seleccionado o None si no 
    debe tener valor.
    """
    combo = gtk.ComboBoxEntry()
    combo.set_name("%d_%d" % (dia, idgrupo))
    utils.rellenar_lista(combo, turnos)
    combo.set_size_request(100, 19)
    utils.combo_set_from_db(combo, turnoid)
    combo.child.modify_base(gtk.STATE_NORMAL, combo.child.get_colormap().alloc_color(get_color_turno(turnoid)))
    combo.connect('changed', funcion)
    return combo

def build_label_dia(dia, mes, anno):
    """
    Devuelve un gtk.Label de una cadena "Nombredía, día" con el 
    nombre del día del mes y año recibido.
    """
    diafecha = mx.DateTime.DateTimeFrom(day = dia, month = mes, year = anno)
    texto_label = utils.corregir_nombres_fecha(diafecha.strftime("%A, %d"))
    # En windows las tildes dentro de etiquetas small no se muestran bien. ¿BUG de GTK?
#    if os.name == 'nt':
#        texto_label = texto_label.replace("á", "a")
#        texto_label = texto_label.replace("é", "e")
    label = gtk.Label("<small>%s</small>" % (texto_label))
    label.set_use_markup(True)
    label.set_justify(gtk.JUSTIFY_RIGHT)
    label.set_property('xalign', 1)
    return label

def build_checkboxes(dia, funcvacaciones, funcfestivo, funclaborable, marcadovac, marcadofest):
    """
    Construye y devuelve un vbox con dos hijos: dos checkboxes donde 
    marcar vacaciones o festivo para el día dado.
    Aparecerán marcadas dependiendo de marcadovac y marcadofest.
    """
    chv=gtk.RadioButton()
    chv.set_name("%d" % (dia))
    chv.set_active(marcadovac)
    
    chl=gtk.RadioButton(group = chv)
    chl.set_name("%d" % (dia))
    chl.set_active(not marcadofest and not marcadovac)
    
    chf=gtk.RadioButton(group = chv)
    chf.set_name("%d" % (dia))
    chf.set_active(marcadofest)
    
    chv.connect('toggled', funcvacaciones)
    chf.connect('toggled', funcfestivo)
    chl.connect('toggled', funclaborable)
    
    hbox = gtk.HBox()
    
    hbox.pack_start(chv)
    label = gtk.Label("<small>Vacaciones</small>")
    label.set_use_markup(True)
    hbox.pack_start(label)
    
    hbox.pack_start(chl)
    label = gtk.Label("<small>Laborable</small>")
    label.set_use_markup(True)
    hbox.pack_start(label)

    hbox.pack_start(chf)
    label = gtk.Label("<small>Festivo</small>")
    label.set_use_markup(True)
    hbox.pack_start(label)
    
    return hbox 

def get_dias_validos(mes, anno):
    """
    Devuelve una tupla con los días válidos del mes y 
    año recibido.
    """
    fecha = mx.DateTime.DateTimeFrom(month = mes, year = anno)
    return tuple([d+1 for d in xrange(fecha.days_in_month)])

def get_color_turno(n):
    colores = ("#AAFFAA", "#AAAAFF", "#FFAAAA", "#FFAAFF", "#AAFFFF", "#FFFFAA")  # ¿Más de 6 turnos? Non credo.
    if n != None:
        n = n % len(colores)
        return colores[n]
    else:
        return "white"


if __name__ == '__main__':
    t = CalendarioLaboral()

