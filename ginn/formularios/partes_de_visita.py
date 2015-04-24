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

# TODO: Meter los registros de Auditoría.[nuevo|borrado|modificado] aquí también.

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
                       'b_buscar/clicked': self.buscar,
                       'calendario/day-selected': self.actualizar_ventana,
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

    def chequear_cambios(self):
        pass

    def es_diferente(self):
        """
        Esta función es llamada cada cierto tiempo. En esta ventana no se
        usa, pero la clase padre la usa activamente.
        """
        return True

    def modificar_hora(self, cell, path, text):
# TODO
        pass
    
    def modificar_cliente(self, cell, path, text):
# TODO
        pass

    def modificar_motivo(self, cell, path, text):
# TODO
        pass

    def modificar_observaciones(self, cell, path, text):
# TODO
        pass
    
    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        # Inicialización del resto de widgets:
        cols = (('Hora', 'gobject.TYPE_STRING', True, True, False,
                    self.modificar_hora),
                ('Cliente o institución', 'gobject.TYPE_STRING',
                    True, True, True, self.modificar_cliente),
                ('Motivo', 'gobject.TYPE_STRING', True, True, False,
                    self.modificar_motivo),
                ('Observaciones', 'gobject.TYPE_STRING', True, True, False,
                    self.modificar_observaciones),
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
                # La última columna (oculta en la Vista) siempre es el id.
        utils.preparar_listview(self.wids['tv_visitas'], cols, multi=True)
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
        #super(PartesDeVisita, self).salir(*args, **kw)
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
                pclases.Visita.q.comercialID == self.objeto.id))
            # 3.- Y relleno
            model = self.wids['tv_visitas'].get_model()
            model.clear()
            pendientes = []
            for visita in visitas:
                self.add_visita_a_tv(visita)
                if not visita.enviada:
                    pendientes.append(visita)
            # 4.- Recuento de acciones pendientes de confirmar
            self.refresh_commit(pendientes)

    def refresh_commit(self, pendientes = None):
        """
        """
        # TODO: Si pendientes es None, contar las visitas pendientes del model.
# PORASQUI
        txtcommit = "_Confirmar"
        if pendientes:
            txtcommit += " (%d)" % len(pendientes)
        self.wids['b_guardar'].set_label(txtcommit)
        self.wids['b_guardar'].set_sensitive(pendientes and True or False)

    def add_visita_a_tv(self, visita):
        fila = (utils.str_hora_corta(visita.fechahora),     # TODO: Y un icono de candado si la visita está enviada.
                visita.nombrecliente,   # TODO: Y un icono de "guay" si el cliente existe en la BD.
                visita.motivoVisita and visita.motivoVisita.motivo,
                visita.observaciones,
                visita.puid)
        model = self.wids['tv_visitas'].get_model()
        model.append(fila)

    def nuevo(self, widget):
        """
        Crea una nueva visita en blanco para que la rellene el comercial.
        """
        visita = pclases.Visita(comercial = self.objeto,
                                cliente = None,
                                nombrecliente = "",
                                motivoVisita = None,
                                fechahora = datetime.datetime.now(),
                                lugar = None,
                                observaciones = "",
                                enviada = False)
        pclases.Auditoria.nuevo(visita, self.usuario, __file__)
        #self.actualizar_ventana()
        model = self.wids['tv_visitas'].get_model()
        self.add_visita_a_tv(visita)
        # TODO: Actualizar el label del botón "commit".

    def guardar(self, widget):
        """
        Marca como "enviada" cada visita del model y envía un correo
        electrónico para alertar de que el parte está completo.
        """
        model = self.wids['tv_visitas'].get_model()
        for itr in model:
            visita = pclases.getObjetoPUID(model[itr][-1])
            visita.enviada = True
            visita.syncUpdate()
        self.actualizar_ventana() # TODO: PORASQUI: A ver cómo me las ingenio para al escribir un nombre de cliente lo enlace con el cliente de verdad si existe. INCLUSO AUNQUE SE CREE A POSTERIORI. Y marcar los días que ya tienen visitas en el calendario.

    def borrar(self, widget):
        """
        Elimina una visita marcada en el Treeview por el usuario.
        """
        sel = self.wids['tv_visitas'].get_selection()
        model, paths = sel.get_selected_rows()
        if paths and utils.dialogo('¿Eliminar las visitas seleccionadas?', 
                                   'BORRAR', 
                                   padre = self.wids['ventana']):
            for path in paths:
                visita = pclases.getObjetoPUID(model[path][-1])
                if (not visita.enviada
                        or (visita.enviada
                            and self.usuario and self.usuario.nivel <= 1)):
                    visita.destroy(ventana = __file__)
            self.actualizar_ventana()

if __name__ == "__main__":
    p = PartesDeVisita()

