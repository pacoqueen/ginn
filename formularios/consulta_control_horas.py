#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado,                   #
#                          (pacoqueen@users.sourceforge.net)                  #
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
## consulta_control_horas.py -- 
###################################################################

from ventana import Ventana
import utils
import pygtk, gobject, pango
pygtk.require('2.0')
import gtk, gtk.glade, time
try:
    import pclases
except ImportError:
    import sys
    from os.path import join as pathjoin
    sys.path.append(pathjoin("..", "framework"))
    import pclases
import mx
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes
import ventana_progreso
    

class ConsultaControlHoras(Ventana):
    inicio = None
    fin = None
    resultado = []
        
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        global fin
        Ventana.__init__(self, 'consulta_control_horas.glade', objeto, usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       "b_exportar/clicked": self.exportar}
        self.add_connections(connections)
        cols = (('Fecha', 'gobject.TYPE_STRING', False, True, True, None),
                ('Horas regulares día', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Horas regulares noche', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Horas extras día', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Horas extras noche', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('ID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        for col in range(1, 5):
            columna = self.wids['tv_datos'].get_column(col)
            for cell in columna.get_cell_renderers():
                cell.set_property("xalign", 1)
        # Cuatro columnas ocultas para colorear:
        tipos = [c[1] for c in cols]
        tipos.insert(-1, "gobject.TYPE_BOOLEAN") # Baja
        tipos.insert(-1, "gobject.TYPE_BOOLEAN") # Vacaciones y asuntos prop.
        tipos.insert(-1, "gobject.TYPE_BOOLEAN") # Festivo
        tipos.insert(-1, "gobject.TYPE_BOOLEAN") # Bloqueado
        tipos = [eval(t) for t in tipos]
        new_model = gtk.TreeStore(*tipos)
        new_model.set_sort_func(0, utils.funcion_orden, 0)
        self.wids['tv_datos'].set_model(new_model)
        # ListViews de totales:
        conceptos = ("Tipo de hora", "Hora del día", "Actividad desarrollada", 
                     "Centro de trabajo")
        for c, nombretabla in zip(conceptos, 
            ("tv_tipo", "tv_hora", "tv_actividad", "tv_centro")):
            cols = ((c, "gobject.TYPE_STRING", False, True, True, False),
                    ("Horas totales", "gobject.TYPE_STRING", 
                        False, True, False, None), 
                    ("", "gobject.TYPE_STRING", False, False, False, None))
            if nombretabla == "tv_centro":
                utils.preparar_treeview(self.wids[nombretabla], cols)
            else:
                utils.preparar_listview(self.wids[nombretabla], cols)
            columna = self.wids[nombretabla].get_column(1)
            for cell in columna.get_cell_renderers():
                cell.set_property("xalign", 1)
        # Fechas iniciales de la ventana:
        temp = time.localtime()
        self.inicio = mx.DateTime.localtime() - (7*mx.DateTime.oneDay)
        self.fin = mx.DateTime.localtime()
        self.wids['e_fechafin'].set_text(utils.str_fecha(self.fin))
        self.wids['e_fechainicio'].set_text(utils.str_fecha(self.inicio))
        empleados = [(0, "Todos")]
        empleados += [(e.id, "%s, %s" % (e.apellidos, e.nombre)) 
                      for e in pclases.Empleado.select(pclases.AND(
                            pclases.Empleado.q.planta == True, 
                            pclases.Empleado.q.activo == True),
                        orderBy = "apellidos")]
        utils.rellenar_lista(self.wids['cbe_empleado'], empleados)
        utils.combo_set_from_db(self.wids['cbe_empleado'], 0)
        self.colorear()
        self.wids['tv_datos'].connect("row-activated", self.abrir_fila)
        gtk.main()

    def abrir_fila(self, tv, path, vc):
        """
        Si se ha hecho doble clic en un empleado, abre la ficha del empleado.
        Si ha sido en una fecha, abre la ventana de control de horas.
        """
        model = tv.get_model()
        tipo, id = model[path][-1].split(":")
        if tipo == "ch":
            try:
                ch = pclases.ControlHoras.get(int(id))
            except:
                pass
            else:
                import control_personal
                v = control_personal.ControlPersonal(ch, self.usuario)
        elif tipo == "e":
            try:
                e = pclases.Empleado.get(int(id))
            except:
                pass
            else:
                import empleados
                v = empleados.Empleados(e, self.usuario)

    def colorear(self):
        """
        Colorea las filas en función de si el trabajador estaba de baja, 
        de vacaciones, si el día era festivo y si el parte está bloqueado.   
        """
        #######################################################################
        def cell_func(column, cell, model, itr, numcol):
            """
            Colorea la fila en función de: 
            - Si empleado de vacaciones, lo pone en cursiva.
            - Si empleado de baja, cursiva y color de texto gris.
            - Si era festivo, color de texto rojo.
            - Si bloqueado, texto en negrita.
            El color de la baja tiene prioridad sobre los festivos.
            """
            color = None
            cursiva = False 
            negrita = False 
            baja = model[itr][5]
            vaca = model[itr][6]
            fest = model[itr][7]
            bloq = model[itr][8]
            if fest:
                color = "red"
            if bloq:
                negrita = True
            if vaca or baja:
                cursiva = True
            if baja:
                color = "gray"
            cell.set_property("foreground", color)
            if cursiva:
                cell.set_property("style", pango.STYLE_ITALIC)
            else:
                cell.set_property("style", pango.STYLE_NORMAL)
            if negrita:
                cell.set_property("weight", pango.WEIGHT_BOLD)
            else:
                cell.set_property("weight", pango.WEIGHT_NORMAL)
        #######################################################################
        cols = self.wids['tv_datos'].get_columns()
        for col in cols:
            cells = col.get_cell_renderers()
            for cell in cells:
                col.set_cell_data_func(cell, cell_func, 0)

    def chequear_cambios(self):
        pass

    def set_inicio(self, boton):
        temp = utils.mostrar_calendario(
            fecha_defecto = utils.parse_fecha(
                self.wids['e_fechainicio'].get_text()), 
            padre = self.wids['ventana'])
        self.inicio = mx.DateTime.DateTimeFrom(*temp[::-1])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(self.inicio))

    def set_fin(self, boton):
        temp = utils.mostrar_calendario(
            fecha_defecto = utils.parse_fecha(
                self.wids["e_fechafin"].get_text()), 
            padre = self.wids['ventana'])
        self.fin = mx.DateTime.DateTimeFrom(*temp[::-1])
        self.wids['e_fechafin'].set_text(utils.str_fecha(self.fin))

    def rellenar_tabla(self, empleados, por_tipo, por_hora, por_actividad, 
                       por_centro):
    	"""
        «empleados» es un diccionario que contiene por cada empleado una lista 
        de fechas (ordenada) y otro diccionario con las horas por fecha.
        Las horas están en una tupla con el orden: horas regulares, regulares 
        noche, extra y extra noche.
        """ 
        # Tablas de totales:
        for wid, dict, evchart in zip(('tv_tipo', 'tv_hora', 'tv_actividad'), 
                                       #'tv_centro'), 
                                      (por_tipo, por_hora, por_actividad, 
                                       por_centro), 
                                      ('eventbox_chart_tipo', 
                                       'eventbox_chart_hora', 
                                       'eventbox_chart_actividad')): 
                                       #'eventbox_chart_centro')):
            model = self.wids[wid].get_model()
            model.clear()
            datachart = []
            # Relleno model
            for k in dict:
                fila = (k, dict[k])
                datachart.append(fila)
                model.append((fila[0], utils.float2str(fila[1]), ""))
            # Y actualizo gráfica (esto pide refactorización a gritos):
            graficar(self.wids[evchart], datachart, self.logger)
        # Tratamiento especial a la tabla por centro de trabajo. Varios va a 
        # ser un concepto deplegable.
        model = self.wids['tv_centro'].get_model()
        model.clear()
        datachart = []
        fila_varios = ["Varios", 0.0]
        nodo_varios = model.append(None, 
                                   ("Varios", utils.float2str("0.0"), ""))
        for centro in por_centro:
            if "Varios: " not in centro:    # "Varios: %s" % concepto es lo 
                # que devuelve el método de pclases para las horas de varios.
                fila = (centro, por_centro[centro])
                datachart.append(fila)
                model.append(None, 
                             (centro, utils.float2str(por_centro[centro]), ""))
            else:
                fila_varios[1] += por_centro[centro]
                model[nodo_varios][1] = utils.float2str(
                    utils._float(model[nodo_varios][1]) + por_centro[centro])
                model.append(nodo_varios, 
                             ("".join(centro.split(":")[-1:]).strip(), 
                              utils.float2str(por_centro[centro]), 
                              ""))
        datachart.append(tuple(fila_varios))
        graficar(self.wids['eventbox_chart_centro'], datachart, self.logger)
        # Tabla principal:
    	model = self.wids['tv_datos'].get_model()
    	model.clear()
        tothrd = tothrn = tothed = tothen = 0.0
    	for empleado in empleados:
            padre = model.append(None, 
                (empleado.apellidos + ", " + empleado.nombre,
                 utils.float2str(0.0), 
                 utils.float2str(0.0),
                 utils.float2str(0.0),
                 utils.float2str(0.0),
                 False, 
                 False, 
                 False, 
                 False, 
                 "%s:%d" % ("e", empleado.id)))
            for fecha in empleados[empleado]['fechas']:
                (hrd, hrn, hed, hen, 
                 baja, vacaciones, festivo, bloqueado, 
                 chid ) = empleados[empleado]['horas'][fecha]
                model.append(padre, (utils.str_fecha(fecha), 
                                     utils.float2str(hrd), 
                                     utils.float2str(hrn), 
                                     utils.float2str(hed), 
                                     utils.float2str(hen), 
                                     baja, 
                                     vacaciones, 
                                     festivo, 
                                     bloqueado, 
                                     "%s:%d" % ("ch", chid)))
                # Actualizo fila padre
                model[padre][1] = utils.float2str(
                    utils._float(model[padre][1]) + hrd)
                model[padre][2] = utils.float2str(
                    utils._float(model[padre][2]) + hrn)
                model[padre][3] = utils.float2str(
                    utils._float(model[padre][3]) + hed)
                model[padre][4] = utils.float2str(
                    utils._float(model[padre][4]) + hen)
                # Incremento totales
                tothrd += hrd
                tothrn += hrn
                tothed += hed
                tothen += hen
        # Muestro totales
        self.wids['e_total_hrdia'].set_text(utils.float2str(tothrd))
        self.wids['e_total_hrnoche'].set_text(utils.float2str(tothrn))
        self.wids['e_total_hedia'].set_text(utils.float2str(tothed))
        self.wids['e_total_henoche'].set_text(utils.float2str(tothen))
        # Monto gráfica
        datachart = [["Regulares día", tothrd], 
                     ["Regulares noche", tothrn], 
                     ["Extra día", tothed], 
                     ["Extra noche", tothen]]
        graficar(self.wids['eventbox_chart'], datachart, self.logger, 
                 orient = "horizontal", values_on_bars = True)
        #try:
        #    import charting
        #except ImportError:
        #    import sys, os
        #    sys.path.append(os.path.join("..", "utils"))
        #    import charting
        #try:
        #    oldchart = self.wids['eventbox_chart'].get_child()
        #    if oldchart != None:
        #        #self.wids['eventbox_chart'].remove(oldchart)
        #        chart = oldchart
        #    else:
        #        chart = charting.Chart(orient = "horizontal", 
        #                               values_on_bars = True)
        #        self.wids['eventbox_chart'].add(chart)
        #    chart.plot(datachart)
        #    self.wids['eventbox_chart'].show_all()
        #except Exception, msg:
        #    txt = "consulta_control_horas.py::rellenar_tabla -> "\
        #          "Error al dibujar gráfica (charting): %s" % msg
        #    print txt
        #    self.logger.error(txt)
        
    def buscar(self, boton):
        """
        Busca los registros de control de horas entre las fechas del 
        formulario y organiza los resultados en un diccionario de empleados 
        que contiene las fechas ordenadas y una lista de horas totales 
        por fecha en un diccionario "horas" por cada empleado.
        """
        CH = pclases.ControlHoras
        eid = utils.combo_get_value(self.wids['cbe_empleado'])
        if eid == 0:
            if not self.inicio:
                chs = CH.select(CH.q.fecha <= self.fin)
            else:
                chs = CH.select(pclases.AND(
                    CH.q.fecha >= self.inicio, 
                    CH.q.fecha <= self.fin))
        else:
            if not self.inicio:
                chs = CH.select(pclases.AND(CH.q.fecha <= self.fin, 
                                            CH.q.empleadoID == eid))
            else:
                chs = CH.select(pclases.AND(
                    CH.q.fecha >= self.inicio, 
                    CH.q.fecha <= self.fin, 
                    CH.q.empleadoID == eid))
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        tot = chs.count()
        i = 0.0
        vpro.mostrar()
        empleados = {}
        por_tipo = {}
        por_hora = {}
        por_actividad = {}
        por_centro = {}
        for ch in chs:
            vpro.set_valor(i/tot, 'Analizando partes de control...')
            actualizar_dicts(ch, por_tipo, por_hora, por_actividad, por_centro)
            empleado = ch.empleado
            if empleado not in empleados:
                empleados[empleado] = {"fechas": [], 
                                       "horas": {}}
            fecha = ch.fecha
            if not ch.nocturnidad:
                hrd = ch.horasRegulares
                hrn = 0.0
            else:
                hrd = 0.0
                hrn = ch.horasRegulares
            hed = ch.calcular_total_horas_extras_dia()
            hen = ch.calcular_total_horas_extras_noche()
            if fecha not in empleados[empleado]["fechas"]:
                empleados[empleado]["fechas"].append(fecha)
                empleados[empleado]["horas"][fecha] = [hrd, hrn, hed, hen, 
                                                ch.bajaLaboral, 
                                                ch.vacacionesYAsuntosPropios, 
                                                ch.festivo, ch.bloqueado, 
                                                ch.id]
            else:
                empleados[empleado]["horas"][fecha][0] += hrd
                empleados[empleado]["horas"][fecha][1] += hrn
                empleados[empleado]["horas"][fecha][2] += hed
                empleados[empleado]["horas"][fecha][3] += hen
                # Aritmética boolena. No tiene mucho sentido porque en una sola
                # fecha nunca se van a mezclar varios registros CH del mismo 
                # empleado, pero por si acaso.
                empleados[empleado]["horas"][fecha][4] += ch.bajaLaboral
                empleados[empleado]["horas"][fecha][5] \
                    += ch.vacacionesYAsuntosPropios
                empleados[empleado]["horas"][fecha][6] += ch.festivo
                empleados[empleado]["horas"][fecha][7] += ch.bloqueado
                # Si hay más de un ID (no debería), guardo el último de todos.
                empleados[empleado]["horas"][fecha][8] = ch.id
            i += 1
        # Retoques finales a la estructura de datos:
        for empleado in empleados:
            empleados[empleado]["fechas"].sort()
        vpro.ocultar()
        self.rellenar_tabla(empleados, por_tipo, por_hora, por_actividad, 
                            por_centro)

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        import sys, os
        sys.path.append(os.path.join("..", "informes"))
        from treeview2csv import treeview2csv
        from informes import abrir_csv
        tv = self.wids['tv_datos']
        abrir_csv(treeview2csv(tv))

    def imprimir(self, boton):
        import sys, os
        sys.path.append(os.path.join("..", "informes"))
        from treeview2pdf import treeview2pdf
        from informes import abrir_pdf
        tv = self.wids['tv_datos']
        abrir_pdf(treeview2pdf(tv, 
                               titulo = "Resumen horas por empleado y día", 
                               fecha = self.wids['e_fechainicio'].get_text() 
                                       + " - " 
                                       + self.wids['e_fechafin'].get_text(), 
                               apaisado = False))


def actualizar_dicts(ch, por_tipo, por_hora, por_actividad, por_centro):
    for func, dict in zip((ch.get_por_tipo, ch.get_por_hora, 
                           ch.get_por_actividad, 
                           ch.get_por_centro_de_trabajo), 
                          (por_tipo, por_hora, por_actividad, por_centro)): 
        act_dict(func(), dict)

def act_dict(d1, d2):
    """
    Une d1 y d2 en el mismo diccionario. Suma valores si las claves se repiten.
    """
    for k in d1:
        try:
            d2[k] += d1[k]
        except KeyError:
            d2[k] = d1[k]

def graficar(widevchart, datachart, logger = None, *resto_params, **resto_kwp):
    try:
        import gtk, gobject, cairo, copy, math
    except ImportError:
        return      # No se pueden dibujar gráficas.    # TODO: Temporal.
    try:
        import charting
    except ImportError:
        import sys, os
        sys.path.append(os.path.join("..", "utils"))
        import charting
    try:
        oldchart = widevchart.get_child()
        if oldchart != None:
            chart = oldchart
        else:
            #chart = charting.Chart(orient = "vertical") 
            chart = charting.Chart(*resto_params, **resto_kwp) 
            widevchart.add(chart)
        chart.plot(datachart)
        widevchart.show_all()
    except Exception, msg:
        txt = "consulta_control_horas.py::rellenar_tabla -> "\
              "Error al dibujar gráfica (charting %s): %s" % (
                msg, widevchart.name)
        print txt
        if logger:
            logger.error(txt)

if __name__ == '__main__':
    t = ConsultaControlHoras() 

    
