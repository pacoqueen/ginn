#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2015  Francisco José Rodríguez Bogado,                   #
#                          <frbogado@geotexan.com>                            #
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
## consulta_partes_de_visita.py --
###################################################################
## NOTAS:
##
###################################################################

"""
Consulta de partes de visitas realizadas por los comerciales.
"""

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk, time
from framework import pclases
from informes import geninformes
from formularios.consulta_existenciasBolsas import act_fecha
import datetime
from formularios.custom_widgets import gtkcairoplot
from collections import defaultdict
try:
    from collections import OrderedDict
except ImportError:
    from lib.ordereddict import OrderedDict

NIVEL_SUPERVISOR = 1    # Nivel máximo de usuario que puede ver todas las
                        # visitas. Los niveles empiezan en 0 (admin)

class ConsultaPartesDeVisita(Ventana):
    """
    Clase que contiene la ventana y los resultados de la consulta.
    """
    # TODO: Meter tablas hamster con las franjas horarias en que se reciben visitas, un heatmap de visitas/comercial y tal.
    def __init__(self, objeto=None, usuario=None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'consulta_partes_de_visita.glade', objeto,
                         usuario=usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_fecha,
                       'b_fecha_fin/clicked': self.set_fecha,
                       'b_exportar/clicked': self.exportar,
                       'e_fecha_inicio/focus-out-event': act_fecha,
                       'e_fecha_fin/focus-out-event': act_fecha,
                      }
        self.add_connections(connections)
        # Comerciales visibles según usuario "logueado"
        comerciales = []
        comerciales_del_usuario = []
        if self.usuario and self.usuario.empleados:
            for e in self.usuario.empleados:
                for c in e.comerciales:
                    comerciales_del_usuario.append(c)
            # También debe tener acceso a los comerciales por debajo de su nivel
            for c in pclases.Comercial.select():
                try:
                    activo = c.empleado.activo
                    nivel = c.empleado.usuario.nivel
                except AttributeError:
                    continue
                if activo and nivel > self.usuario.nivel:
                    comerciales_del_usuario.append(c)
        if not comerciales_del_usuario or (self.usuario
                               and self.usuario.nivel <= NIVEL_SUPERVISOR):
            comerciales = pclases.Comercial.select()
        else:
            comerciales = comerciales_del_usuario[:]
        opciones_comerciales = [
            (c.id, c.empleado and c.empleado.get_nombre_completo()
                or "Comercial desconocido (%s)" % c.puid)
            for c in comerciales
            if c.empleado.activo or c in comerciales_del_usuario]
        opciones_comerciales.sort(key = lambda i: i[1])
        utils.rellenar_lista(self.wids['cb_comercial'],
                [(0, "Todos los visibles por mí")] + opciones_comerciales)
        cols = (('Comercial | Cliente/Institución', 'gobject.TYPE_STRING',
                    False, True, False, None),
                ('Fecha', 'gobject.TYPE_STRING', False, True, False, None),
                ('Motivo', 'gobject.TYPE_STRING', False, True, False, None),
                ('Observaciones', 'gobject.TYPE_STRING',
                    False, True, False, None),
                ('DBPUID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        self.wids['tv_datos'].connect("row-activated", self.abrir_objeto)
        self.resultado = []
        self.fin = utils.str_fecha(datetime.date.today())
        self.inicio = None
        self.wids['e_fecha_fin'].set_text(self.fin)
        self.wids['e_fecha_inicio'].set_text("")
        if objeto != None:
            utils.combo_set_from_db(self.wids["cb_comercial"], objeto.id)
            self.wids["b_buscar"].clicked()
        else:
            utils.combo_set_from_db(self.wids['cb_comercial'], 0)
        self.wids['cb_comercial'].grab_focus()
        gtk.main()

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        tv = self.wids['tv_datos']
        abrir_csv(treeview2csv(tv, desglosar = True))

    def abrir_objeto(self, tv, path, column):
        """
        Abre la visita a la que se le ha hecho doble clic en una ventana nueva.
        """
        model = tv.get_model()
        dbpuid = model[path][-1]
        objeto = pclases.getObjetoPUID(dbpuid)
        # Se le pasa un comercial o una visita concreta. La ventana destino
        # decide qué hacer en cada caso.
        from formularios import partes_de_visita
        ventanapartes = partes_de_visita.PartesDeVisita(objeto = objeto,
                                                        usuario = self.usuario)

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, visitas):
        """
        Rellena el model con las visitas de la consulta.
        """
        from formularios.ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        tot = visitas.count()
        vpro.mostrar()
        model = self.wids['tv_datos'].get_model()
        model.clear()
        total = 0.0
        dias = set()
        rows_comercial = {}
        visitas_comercial = {}
        first_day = None
        last_day = None
        for visita in visitas:
            vpro.set_valor(total / tot,
                           "Recuperando visitas... [%d/%d]" % (total, tot))
            comercial = visita.comercial
            if not first_day or visita.fechahora.date() < first_day:
                first_day = visita.fechahora.date()
            if not last_day or visita.fechahora.date() > last_day:
                last_day = visita.fechahora.date()
            total += 1
            cliente = visita.nombrecliente
            dias.add(visita.fechahora.date())
            try:
                row_comercial = rows_comercial[comercial.puid]
            except KeyError:
                visitas_comercial[comercial.puid] = {'visitas': [], 
                                                     'clientes': set()}
                rows_comercial[comercial.puid] = row_comercial = model.append(
                        None, (comercial.get_nombre_completo(),
                               "",
                               "",
                               "",
                               comercial.puid))
            visitas_comercial[comercial.puid]['visitas'].append(visita)
            visitas_comercial[comercial.puid]['clientes'].add(cliente)
            model.append(row_comercial, (cliente,
                                         utils.str_fechahora(visita.fechahora),
                                         visita.motivoVisita
                                            and visita.motivoVisita.motivo
                                            or "",
                                         visita.observaciones,
                                         visita.puid))
        # Totales en TreeView
        clientes_totales = set()
        for row in model:
            puid = row[-1]
            row[3] = "%d visitas a %d clientes diferentes." % (
                    len(visitas_comercial[puid]['visitas']),
                    len(visitas_comercial[puid]['clientes']))
            clientes_totales = clientes_totales.union(
                    visitas_comercial[puid]['clientes'])
        # Totales en ventana
        try:
            str_media = utils.float2str(total / len(dias), autodec = True)
        except ZeroDivisionError:
            str_media = ""
        self.wids['e_media'].set_text(str_media)
        self.wids['e_total'].set_text(utils.float2str(total, autodec = True)
                + " (%d clientes diferentes)" % len(clientes_totales))
        try:
            dias_rango = (last_day - first_day).days + 1
        except (AttributeError, TypeError):
            dias_rango = 0
        self.wids['e_dias'].set_text(
                "%d días con visita | %d días totales" % (
                    len(dias), dias_rango))
        vpro.ocultar()

    def set_fecha(self, boton):
        """
        Cambia la fecha de los filtros.
        """
        w = self.wids[boton.name.replace("b_", "e_")]
        try:
            fechaentry = utils.parse_fecha(w.get_text())
        except (TypeError, ValueError):
            fechaentry = datetime.date.today()
        w.set_text(utils.str_fecha(utils.mostrar_calendario(
                                                fecha_defecto = fechaentry,
                                                padre = self.wids['ventana'])))

    def buscar(self, boton):
        """
        Dadas fecha de inicio y de fin, busca todos las visitas del
        comercial del combo.
        """
        idcomercial = utils.combo_get_value(self.wids['cb_comercial'])
        str_fini = self.wids['e_fecha_inicio'].get_text()
        criterios = [pclases.Visita.q.enviada == True]
        if str_fini:
            self.inicio = utils.parse_fecha(str_fini)
            criterios.append(pclases.Visita.q.fechahora >= self.inicio)
        else:
            self.inicio = None
        try:
            str_ffin = self.wids['e_fecha_fin'].get_text()
            # Le añado un día porque las visitas llevan hora también y la 
            # fecha parseada es a las 00:00 del día en cuestión (me faltarían
            # todas las visitas entres las 00:00 y las 23:59 de ese día).
            self.fin = utils.parse_fecha(str_ffin) + datetime.timedelta(1)
        except (ValueError, TypeError):
            self.fin = datetime.date.today()
            str_ffin = utils.str_fecha(self.fin) + datetime.timedelta(1)
            self.wids['e_fecha_fin'].set_text(str_ffin)
        criterios.append(pclases.Visita.q.fechahora < self.fin)
        if idcomercial == None:
            self.comercial = None
        elif idcomercial == 0:
            self.comercial = None
        else:
            idcomercial = utils.combo_get_value(self.wids['cb_comercial'])
            self.comercial = pclases.Comercial.get(idcomercial)
            criterios.append(
                    pclases.Visita.q.comercial == self.comercial)
        visitas = pclases.Visita.select(pclases.AND(*criterios))
        self.resultado = visitas
        self.rellenar_tabla(self.resultado)

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        from informes.treeview2pdf import treeview2pdf
        from formularios.reports import abrir_pdf
        if not self.inicio:
            fecha_informe = 'Hasta ' + utils.str_fecha(self.fin)
        else:
            fecha_informe = (utils.str_fecha(self.inicio)
                            + ' - '
                            + utils.str_fecha(self.fin))
        abrir_pdf(treeview2pdf(self.wids['tv_datos'],
                               titulo = "Consulta visitas realizadas",
                               fecha = fecha_informe))


if __name__ == '__main__':
    ConsultaPartesDeVisita()

