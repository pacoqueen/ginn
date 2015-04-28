#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore

###############################################################################
# Copyright (C) 2005-2015 Francisco José Rodríguez Bogado,                    #
#                         (bogado@qinn.es)                                    #
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
## partes_de_vistia.py - Partes de visita de los comerciales.
###################################################################
## NOTAS:
## 
## ----------------------------------------------------------------
##  
###################################################################
## Changelog:
## 17 de abril de 2015 -> A git.
## 
###################################################################

import sys, os
from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk, time, mx.DateTime
try:
    from framework import pclases
    from framework.seeker import VentanaGenerica 
except ImportError:
    from framework import pclases
    from framework.seeker import VentanaGenerica 
from utils import _float as float
import datetime

NIVEL_SUPERVISOR = 1    # Nivel máximo de usuario que puede ver todas las
                        # visitas. Los niveles empiezan en 0 (admin)

class PartesDeVisita(Ventana, VentanaGenerica):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'partes_de_visita.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_nuevo/clicked': self.nuevo,
                       'b_borrar/clicked': self.borrar,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       #'b_buscar/clicked': self.buscar,
                       'b_hoy/clicked': self.ir_a_hoy,
                       'b_ir_a/clicked': self.ir_a_fecha,
                       'calendario/day-selected': self.actualizar_ventana,
                       'calendario/month-changed':
                                            self.actualizar_dias_con_visita,
                       'calendario/next-year':
                                            self.actualizar_dias_con_visita,
                       'calendario/prev-year':
                                            self.actualizar_dias_con_visita,
                       'cb_comercial/changed': self.actualizar_ventana
                      }  
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        gtk.main()

    def ir_a_primero(self):
        try:
            if self.usuario:
                self.objeto = self.usuario.get_comerciales()[0]
                self.ir_a(self.objeto)
            else:
                raise IndexError
        except IndexError:
            try:
                self.objeto = pclases.Comercial.select(pclases.AND(
                        pclases.Empleado.q.activo == True,
                        pclases.Comercial.q.empleadoID == pclases.Empleado.q.id,
                        pclases.Usuario.q.id == pclases.Empleado.q.usuarioID),
                    orderBy = pclases.Usuario.q.nivel)[0]
            except IndexError:
                self.to_log(
                        "No hay comerciales dados de alta en la aplicación.")
                self.salir(mostrar_ventana = False)
            else:
                self.ir_a(self.objeto)

    def ir_a(self, objeto = None):
        if not objeto:
            self.ir_a_primero()
        else:
            # El comercial:
            utils.combo_set_from_db(self.wids['cb_comercial'], self.objeto.id)
            self.actualizar_ventana()

    def ir_a_fecha(self, boton, fecha = None, comercial = None):
        """
        Desplaza el calendario y contenido de la ventana a la fecha para el
        comercial indicado. Si no se reciben, usa el comercial de la ventana
        y pregunta la fecha en un diálogo modal.
        """
        # TODO
        # 0.- Comprobar fecha recibida o pedir.
        # 1.- Comprobar comercial recibido y mover el combo o rescatar de
        #     la ventana si no se ha especificado.
        # 2.- Movel el calendario. La ventana se actualizará sola.

    def ir_a_hoy(self, boton):
        """
        Mueve el calendario y contenido de la ventana a la fecha del sistema.
        """
        hoy = datetime.date.today()
        self.ir_a_fecha(boton, fecha = hoy)

    def actualizar_dias_con_visita(self, calendario):
        """
        Marca en el calendario los días del mes presente con visitas.
        """
        anno, mes, dia = calendario.get_date()
        calendario.clear_marks()
        for dia in range(1, 32):
            try:
                fecha = datetime.datetime(anno, mes + 1, dia)
            except ValueError:
                continue    # La fecha es incorrecta. Se sale del mes.
            visitas = pclases.Visita.select(pclases.AND(
                pclases.Visita.q.fechahora >= fecha,
                pclases.Visita.q.fechahora <= fecha + datetime.timedelta(1)
                ))
            if visitas.count():
                calendario.mark_day(dia)
        self.actualizar_ventana()   # Digo yo que si ha cambiado el mes o el
        # año, habrá que actualizar la ventana porque la fecha es otra..

    def chequear_cambios(self):
        pass

    def es_diferente(self):
        """
        Esta función es llamada cada cierto tiempo. En esta ventana no se
        usa, pero la clase padre la usa activamente.
        """
        return True

    def cambiar_hora(self, cell, path, text):
        """
        Cambia la hora de visita y acutaliza el cell. Solo se permite
        cambiarla si el usuario tiene nivel suficiente.
        """
        model = self.wids['tv_visitas'].get_model()
        ide = model[path][-1]
        visita = pclases.getObjetoPUID(ide)
        try:
            dtdelta = mx.DateTime.DateTimeDelta(0,
                                                float(newtext.split(':')[0]),
                                                float(newtext.split(':')[1]),
                                                0)
            visita.fechahora = mx.DateTime.DateTimeFrom(
                    year = visita.horafin.year,
                    month = visita.horafin.month,
                    day = visita.horafin.day,
                    hour = dtdelta.hour,
                    minute = dtdelta.minute,
                    second = dtdelta.second)
            visita.sync()
            model[path][0] = visita.horafin.strftime('%H:%M')
        except IndexError:
            utils.dialogo_info(titulo = "ERROR", 
                               texto = 'El texto "%s" no respeta el formato '
                                       'horario (H:MM).' % newtext,
                               padre = self.wids['ventana'])
        except ValueError:
            utils.dialogo_info(titulo = "ERROR", 
                               texto = 'El texto "%s" no respeta el formato '
                                       'horario (H:M).' % newtext,
                               padre = self.wids['ventana'])    
    def cambiar_cliente(self, cell, path, text, model, ncol, model_tv):
        """Cambia el nombre del cliente de la visita."""
        model = self.wids['tv_visitas'].get_model()
        ide = model[path][-1]
        visita = pclases.getObjetoPUID(ide)
        visita.nombrecliente = text
        # No se hace comprobación de si el cliente existe en la base de datos.
        # Eso se hará en el commit. OJO: Si el cliente se crea a posteriori,
        # el cliente no queda asociado a la visita. It's not a bug, IT'S A 
        # FEATURE: permite hacer consultas sobre visitas a un cliente cuando
        # aún no era cliente.
        visita.syncUpdate()
        model[path][2] = visita.nombrecliente

    def cambiar_motivo(self, cell, path, text):
        model = self.wids['tv_visitas'].get_model()
        ide = model[path][-1]
        visita = pclases.getObjetoPUID(ide)
        if text:
            motivoVisita = pclases.MotivoVisita.search(text)
            if motivoVisita:
                visita.motivoVisita = motivoVisita
            else:
                utils.dialogo_info(titulo = "MOTIVO INCORRECTO", 
                        texto = "Debe seleccionar un motivo de los existentes.",
                        padre = self.wids['ventana'])
        else:
            visita.motivoVisita = None
        visita.syncUpdate()
        pclases.Auditoria.modificado(visita, self.usuario, __file__)
        model[path][4] = (visita.motivoVisita and visita.motivoVisita.motivo
                          or "")

    def cambiar_observaciones(self, cell, path, text):
        model = self.wids['tv_visitas'].get_model()
        ide = model[path][-1]
        visita = pclases.getObjetoPUID(ide)
        visita.observaciones = text     # PLAN: ¿Markdown?
        visita.syncUpdate()
        model[path][5] = visita.observaciones
    
    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        # Inicialización del resto de widgets:
        cols = (('Hora', 'gobject.TYPE_STRING', True, True, False,
                    self.cambiar_hora),
                ('Cliente o institución', 'gobject.TYPE_STRING', 
                    False, True, True, None),
                ('Motivo', 'gobject.TYPE_STRING', False, True, False, None),
                    #self.cambiar_motivo),
                ('Observaciones', 'gobject.TYPE_STRING', True, True, False,
                    self.cambiar_observaciones),
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
                # La última columna (oculta en la Vista) siempre es el id.
        utils.preparar_listview(self.wids['tv_visitas'], cols, multi=True)
        # Agrego un par de columnas para destacar visualmente clientes
        # confirmados en la BD y visitas ya enviadas.
        self.wids['tv_visitas'].set_model(
                # Hora, Enviada, Cliente, ¿existe?, Motivo, Observaciones, PUID
                gtk.ListStore(str, str, str, str, str, str, str))
        # Columna hora con candado si visita enviada.
        col_hora = self.wids['tv_visitas'].get_column(0)
        cellhora = col_hora.get_cell_renderers()[0]
        cellcandado = gtk.CellRendererPixbuf()
        col_hora.pack_start(cellcandado, expand = False)
        col_hora.set_attributes(cellhora, text = 0)
        col_hora.set_attributes(cellcandado, stock_id = 1)
        # Columna cliente con autocompletado y símbolo "OK" si existe en la BD.
        opts_clientes = [("%s (%s)" % (c.nombre, c.cif), c.puid)
                                    for c in pclases.Cliente.select(
                                        pclases.Cliente.q.inhabilitado == False,
                                        orderBy = "nombre")]
        handler_id = utils.cambiar_por_combo(tv = self.wids['tv_visitas'],
                                numcol = 1,
                                opts = opts_clientes,
                                clase = pclases.Visita,
                                campo = "nombrecliente",
                                ventana_padre = self.wids['ventana'],
                                entry = True,
                                numcol_model = 2)
        col_cliente = self.wids['tv_visitas'].get_column(1)
        cellcbcliente = col_cliente.get_cell_renderers()[0]
        cellcbcliente.disconnect(handler_id)
        cellcbcliente.connect("edited", self.cambiar_cliente,
                              cellcbcliente.completion.get_model(),
                              2,
                              self.wids['tv_visitas'].get_model())
        # Y ahora añadir el icono
        celldb = gtk.CellRendererPixbuf()
        col_cliente.pack_start(celldb, expand = False)
        col_cliente.set_attributes(cellcbcliente, text = 2)
        col_cliente.set_attributes(celldb, stock_id = 3)
        # Columna motivo con autocompletado
        utils.cambiar_por_combo(self.wids['tv_visitas'],
                                2,
                                [(m.motivo, m.puid) for m in
                                    pclases.MotivoVisita.select(
                                        orderBy = "motivo")],
                                pclases.Visita,
                                "motivoVisita",
                                self.wids['ventana'],
                                entry = False,
                                numcol_model = 4)
        # Columna observaciones.
        col_observaciones = self.wids['tv_visitas'].get_column(3)
        cellobservaciones = col_observaciones.get_cell_renderers()[0]
        col_observaciones.set_attributes(cellobservaciones, text = 5)
        # Comerciales visibles según usuario "logueado"
        comerciales = []
        comerciales_del_usuario = []
        if self.usuario and self.usuario.empleados:
            for e in self.usuario.empleados:
                for c in e.comerciales:
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
        utils.rellenar_lista(self.wids['cb_comercial'], opciones_comerciales)
        # Empiezo con el día actual.
        hoy = datetime.date.today()
        self.wids['calendario'].select_day(hoy.day)
        self.wids['calendario'].select_month(hoy.month - 1, hoy.year)
        # Tratamiento especial de los botones actualizar y guardar
        self.activar_widgets(True, chequear_permisos = False)
        self.wids['ventana'].resize(800, 600)

    def activar_widgets(self, s, chequear_permisos = True):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        if self.objeto == None:
            s = False
        ws = tuple(["b_borrar", "b_nuevo", "b_guardar", "b_actualizar"])
        for w in ws:
            try:
                self.wids[w].set_sensitive(s)
            except Exception, msg:
                print "Widget problemático:", w, "Excepción:", msg
                import traceback
                traceback.print_last()
        if chequear_permisos:
            self.check_permisos(nombre_fichero_ventana = "partes_de_visita.py")

    def actualizar_ventana(self, *args, **kw):
        """
        Redefinición del método de la clase base. En esta ventana no se trata
        el objeto principal como en las demás y no es necesario comprobar
        si ha cambiado, si hay que refrescar, etc.
        """
        if self.objeto:
            self.activar_widgets(True, chequear_permisos = False)
            self.rellenar_widgets()

    def salir(self, *args, **kw):
        """
        Mismo caso que actualizar_ventana.
        Quiero evitar que pregunte si guardar cambios pendientes.
        """
        self.wids['b_guardar'].set_sensitive(False)
        #super(PartesDeVisita, self).salir(*args, **kw) -> No hereda de 
                    # object, no funciona con super. Lanza un TypeError.
        Ventana.salir(self, *args, **kw)

    def rellenar_widgets(self):
        """
        Introduce la información del objeto actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        # 0.- El comercial seleccionado.
        self.objeto = pclases.Comercial.get(
                utils.combo_get_value(self.wids['cb_comercial']))
        if self.objeto:
            # 1.- La fecha 
            year, month, day = self.wids['calendario'].get_date()
            month += 1  # Gtk.Calendar empieza los meses en 0
            fecha = (year, month, day)
            fecha = datetime.datetime(*fecha)
            # 2.- Las visitas
            visitas = pclases.Visita.select(pclases.AND(
                pclases.Visita.q.fechahora >= fecha,
                pclases.Visita.q.fechahora < fecha+datetime.timedelta(days=1),
                pclases.Visita.q.comercialID == self.objeto.id),
                orderBy = "fechahora")
            # 3.- Y relleno
            model = self.wids['tv_visitas'].get_model()
            model.clear()
            pendientes = []
            for visita in visitas:
                self.add_visita_a_tv(visita)
                if not visita.enviada:
                    pendientes.append(visita)
            # 4.- Recuento de acciones pendientes de confirmar
            self.refresh_commit_button(pendientes)

    def refresh_commit_button(self, pendientes = None):
        """
        Actualiza la leyenda del botón de enviar con las visitas pendientes
        del día y comercial en pantalla.
        """
        if pendientes is None:
            pendientes = []
            model = self.wids['tv_visitas'].get_model()
            for row in model:
                visita = pclases.getObjetoPUID(row[-1])
                if not visita.enviada:
                    pendientes.append(visita)
        txtcommit = "_Confirmar"
        if pendientes:
            txtcommit += " (%d)" % len(pendientes)
        self.wids['b_guardar'].set_label(txtcommit)
        self.wids['b_guardar'].set_sensitive(pendientes and True or False)
        return pendientes

    def add_visita_a_tv(self, visita):
        fila = (utils.str_hora_corta(visita.fechahora),
                visita.enviada and gtk.STOCK_DIALOG_AUTHENTICATION or None,
                visita.nombrecliente,
                visita.cliente and gtk.STOCK_SAVE or gtk.STOCK_NEW,
                visita.motivoVisita and visita.motivoVisita.motivo or "",
                visita.observaciones,
                visita.puid)
        model = self.wids['tv_visitas'].get_model()
        model.append(fila)

    def nuevo(self, widget):
        """
        Crea una nueva visita en blanco para que la rellene el comercial.
        """
        hoy = datetime.datetime.now()
        anno, mes, dia = self.wids['calendario'].get_date()
        fecha = datetime.datetime(anno, mes + 1, dia, hoy.hour, hoy.minute)
        visita = pclases.Visita(comercial = self.objeto,
                                cliente = None,
                                nombrecliente = "",
                                motivoVisita = None,
                                fechahora = fecha,
                                lugar = None,
                                observaciones = "",
                                enviada = False)
        pclases.Auditoria.nuevo(visita, self.usuario, __file__)
        #self.actualizar_ventana()
        model = self.wids['tv_visitas'].get_model()
        self.add_visita_a_tv(visita)
        self.refresh_commit_button()
        self.wids['calendario'].mark_day(dia)

    def guardar(self, widget):
        """
        Marca como "enviada" cada visita del model y envía un correo
        electrónico para alertar de que el parte está completo.
        """
        model = self.wids['tv_visitas'].get_model()
        for row in model:
            visita = pclases.getObjetoPUID(row[-1])
            if not visita.enviada:
                model_clientes = self.wids['tv_visitas'].get_column(
                        1).get_cell_renderers()[0].completion.get_model()
                cliente = None
                for nombre, puid in model_clientes:
                    if nombre == visita.nombrecliente:
                        cliente = pclases.getObjetoPUID(puid)
                        break
                visita.cliente = cliente
                visita.enviada = True
                visita.syncUpdate()
        self.actualizar_ventana()
        # TODO: Digo yo que habría que mandar un correo o algo con las nuevas visitas confirmadas.

    def borrar(self, widget):
        """
        Elimina una visita marcada en el Treeview por el usuario.
        """
        sel = self.wids['tv_visitas'].get_selection()
        model, paths = sel.get_selected_rows()
        if paths and utils.dialogo('¿Eliminar las visitas seleccionadas?', 
                                   'BORRAR', 
                                   padre = self.wids['ventana']):
            paths_a_borrar = []
            for path in paths:
                visita = pclases.getObjetoPUID(model[path][-1])
                dia = visita.fechahora.day
                if (not visita.enviada
                        or (visita.enviada
                            and self.usuario and self.usuario.nivel <= 1)):
                    visita.destroy(ventana = __file__)
                    paths_a_borrar.append(path)
            #self.actualizar_ventana()
            paths_a_borrar.sort(reverse = True)
            for path in paths_a_borrar:
                model.remove(model.get_iter(path))
            visitas_del_dia = self.refresh_commit_button()
            if visitas_del_dia:
                self.wids['calendario'].mark_day(dia)
            else:
                self.wids['calendario'].unmark_day(dia)


def match_motivo(completion, key, itr, ncol):
    model = completion.get_model()
    text = model.get_value(itr, ncol)
    if key.upper() in text.upper():
        return True
    return False

if __name__ == "__main__":
    p = PartesDeVisita()

