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
## ausencias.py - Ausencias y permisos.
###################################################################
## NOTAS:
##  Un día de ausencia, un registro.
##  Si el motivo de la ausencia implica 2 o más días, 2 o más 
##  registros a crear.
## 
###################################################################
## Changelog:
## 27 de julio de 2005 -> Inicio
## 28 de julio de 2005 -> Falta impresión permiso.
## 
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, time
from framework import pclases
from informes import geninformes


class Ausencias(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        Aunque la clase "principal" es Ausencia, self.objeto será el 
        empleado al que pertenecen las ausencias.
        """
        Ventana.__init__(self, 'ausencias.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_drop_ausencia/clicked': self.drop_ausencia,
                       'b_add_ausencia/clicked': self.add_ausencia,
                       'b_imprimir/clicked': self.imprimir_ausencia,
                       'sp_anno/changed': self.actualizar_ventana,
                       'b_add_baja/clicked': self.add_baja, 
                       'b_drop_baja/clicked': self.drop_baja
                      } 
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        gtk.main()

    def es_diferente(self):
        """
        Devuelve True si la información en pantalla es distinta a la
        del objeto en memoria.
        """
        return False

    def aviso_actualizacion(self):
        """
        Muestra una ventana modal con el mensaje de objeto 
        actualizado.
        """
        pass

    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        # Inicialmente no se muestra NADA. Sólo se le deja al
        # usuario la opción de buscar o crear nuevo.
        self.activar_widgets(False)
        self.wids['sp_anno'].set_value(mx.DateTime.localtime().year)
        self.wids['b_actualizar'].set_sensitive(False)
        self.wids['b_guardar'].set_sensitive(False)
        self.wids['b_nuevo'].set_sensitive(True)
        self.wids['b_buscar'].set_sensitive(True)
        cols = (('Fecha', 'gobject.TYPE_STRING', 
                    True, True, True, self.cambiar_fecha), 
                ('Motivo', 'gobject.TYPE_STRING', False, True, False, None),
                ('Observaciones', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_observaciones),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_ausencias'], cols)
        self.cambiar_por_combo(self.wids['tv_ausencias'], 1)
        utils.rellenar_lista(self.wids['cbe_empleado'], 
                             [(c.id, "%s %s" % (c.nombre, c.apellidos)) for c in \
                              pclases.Empleado.select(pclases.Empleado.q.activo == True, orderBy="nombre")])
        self.wids['cbe_empleado'].connect('changed', self.cambiar_seleccion_empleado)
        cols = (('Fecha inicio', 'gobject.TYPE_STRING', 
                    True, True, True, self.cambiar_fecha_inicio_baja), 
                ('Fecha fin', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_fecha_fin_baja), 
                ('Motivo', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_motivo_baja),
                ('Observaciones', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_observaciones_baja),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_bajas'], cols)

    def cambiar_fecha_inicio_baja(self, cell, path, texto):
        try:
            fecha = utils.parse_fecha(texto)
        except (ValueError, TypeError):
            utils.dialogo_info(titulo = "FECHA INCORRECTA", 
                               texto = "La fecha introducida no es válida", 
                               padre = self.wids['ventana'])
            return
        model = self.wids['tv_bajas'].get_model()
        baja = pclases.Baja.get(model[path][-1])
        for bajaexistente in self.objeto.bajas:
            if bajaexistente == baja:
                continue
            iniciorango = fecha
            finrango = baja.fechaFin or mx.DateTime.localtime()
            if iniciorango > finrango:
                iniciorango, finrango = finrango, iniciorango
            fechaintermedia = iniciorango
            while fechaintermedia < finrango:
                if bajaexistente.esta_vigente(fechaintermedia):
                    utils.dialogo_info(titulo = "BAJA SOLAPADA", 
                                       texto = "Las bajas médicas no pueden solaparse entre sí, elija otra fecha.", 
                                       padre = self.wids['ventana'])
                    return
                fechaintermedia += mx.DateTime.oneDay
        baja.fechaInicio = fecha
        if baja.fechaInicio > baja.fechaFin:
            baja.fechaInicio, baja.fechaFin = baja.fechaFin, baja.fechaInicio
        baja.sync()
        model[path][0] = utils.str_fecha(baja.fechaInicio)
        model[path][1] = utils.str_fecha(baja.fechaFin)

    def cambiar_fecha_fin_baja(self, cell, path, texto): 
        try:
            fecha = utils.parse_fecha(texto)
        except (ValueError, TypeError):
            utils.dialogo_info(titulo = "FECHA INCORRECTA", 
                               texto = "La fecha introducida no es válida", 
                               padre = self.wids['ventana'])
            return
        model = self.wids['tv_bajas'].get_model()
        baja = pclases.Baja.get(model[path][-1])
        for bajaexistente in self.objeto.bajas:
            if bajaexistente == baja:
                continue
            iniciorango = baja.fechaInicio
            finrango = fecha
            if iniciorango > finrango:
                iniciorango, finrango = finrango, iniciorango
            fechaintermedia = iniciorango
            while fechaintermedia < finrango:
                if bajaexistente.esta_vigente(fechaintermedia):
                    utils.dialogo_info(titulo = "BAJA SOLAPADA", 
                                       texto = "Las bajas médicas no pueden solaparse entre sí, elija otra fecha.", 
                                       padre = self.wids['ventana'])
                    return
                fechaintermedia += mx.DateTime.oneDay
        baja.fechaFin = fecha
        if baja.fechaInicio > baja.fechaFin:
            baja.fechaInicio, baja.fechaFin = baja.fechaFin, baja.fechaInicio
        baja.sync()
        model[path][0] = utils.str_fecha(baja.fechaInicio)
        model[path][1] = utils.str_fecha(baja.fechaFin)

    def cambiar_motivo_baja(self, cell, path, texto): 
        model = self.wids['tv_bajas'].get_model()
        baja = pclases.Baja.get(model[path][-1])
        baja.motivo = texto
        baja.sync()
        model[path][2] = baja.motivo

    def cambiar_observaciones_baja(self, cell, path, texto): 
        model = self.wids['tv_bajas'].get_model()
        baja = pclases.Baja.get(model[path][-1])
        baja.observaciones = texto
        baja.sync()
        model[path][3] = baja.observaciones

    def cambiar_fecha(self, cell, path, texto):
        model = self.wids['tv_ausencias'].get_model()
        ausencia = pclases.Ausencia.get(model[path][-1])
        try:
            ausencia.fecha = time.strptime(texto, '%d/%m/%Y')
        except:
            try:
                ausencia.fecha = time.strptime(texto, '%d/%m/%y')
            except:
                utils.dialogo_info('FECHA INCORRECTA', 
                                   'La fecha introducida (%s) no es correcta.' % texto)
        ausencia.sync()
        model[path][0] = utils.str_fecha(ausencia.fecha)

    def cambiar_observaciones(self, cell, path, texto):
        model = self.wids['tv_ausencias'].get_model()
        ausencia = pclases.Ausencia.get(model[path][-1])
        ausencia.observaciones = texto
        ausencia.sync()
        model[path][2] = ausencia.observaciones

    def cambiar_por_combo(self, tv, numcol):
        import gobject
        # Elimino columna actual
        column = tv.get_column(numcol)
        column.clear()
        # Creo model para el CellCombo
        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_INT64)
        for motivo in pclases.Motivo.select():
            model.append(("%s %s" % (motivo.descripcion, motivo.descripcionDias), motivo.id))
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
                texto, ide = model_combo[i]
                if texto == text:
                    idct = ide
                    break
            if idct == None:
                utils.dialogo_info(titulo = "ERROR MOTIVO", texto = "Ocurrió un error inesperado guardando motivo de ausencia.\n\nContacte con los desarrolladores de la aplicación\n(Vea el diálogo «Acerca de...» desde el menú de la aplicación.)", padre = self.wids['ventana'])
            else:
                ct = pclases.Motivo.get(idct)
                model_tv[path][numcol] = text
                ausencia = pclases.Ausencia.get(model_tv[path][-1])
                ausencia.motivo = ct
                self.actualizar_ventana()
        cellcombo.connect("edited", guardar_combo, tv.get_model(), numcol, model)
        column.pack_start(cellcombo)
        column.set_attributes(cellcombo, text = numcol)

    def cambiar_seleccion_empleado(self, cb):
        anterior = self.objeto
        itr = cb.get_active_iter()
        if itr == None:
            self.objeto = None
        else:
            model = cb.get_model()
            ide = model[itr][0]
            self.objeto = pclases.Empleado.get(ide)
        self.actualizar_ventana(objeto_anterior = anterior)

    def activar_widgets(self, s):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        ws = ('hbox12', 'hbox13', 'frame1', 'e_centro', 'label20', 'frame2')  
        for w in ws:
            self.wids[w].set_sensitive(s)

    def ir_a_primero(self):
        """
        Hace que el primer registro -si lo hay- de la tabla implicada
        en el objeto del formulario sea el objeto activo.
        """
        anterior = empleado = self.objeto
        try:
            # Anulo el aviso de actualización del envío que deja de ser activo.
            if empleado != None: empleado.notificador.set_func(lambda : None)
            empleado = pclases.Empleado.select(pclases.Empleado.q.activo == True, orderBy="id")[0]	
            empleado.notificador.set_func(self.aviso_actualizacion)	
        except:
            empleado = None
        self.objeto = empleado
        self.actualizar_ventana(objeto_anterior = anterior)

    def rellenar_widgets(self):
        """
        Introduce la información del empleado actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        empleado = self.objeto
        if empleado != None:
            self.wids['e_centro'].set_text(empleado.centroTrabajo and empleado.centroTrabajo.nombre or '')
            self.wids['e_dias_convenio'].set_text(empleado.categoriaLaboral 
                                                    and "%d" % (empleado.categoriaLaboral.diasConvenio) or '')
            self.wids['e_dias_asuntos_propios'].set_text(empleado.categoriaLaboral 
                                                    and "%d" % (empleado.categoriaLaboral.diasAsuntosPropios) or '')
            anno = self.wids['sp_anno'].get_value()
            diasConvenioRestantes = empleado.get_diasConvenioRestantes(anno)
            self.wids['e_dc_restantes'].set_text('%d' % diasConvenioRestantes)
            if diasConvenioRestantes > 0:
                self.wids['e_dc_restantes'].modify_base(gtk.STATE_NORMAL, 
                                                      self.wids['e_dc_restantes'].get_colormap().alloc_color("white"))
            elif diasConvenioRestantes == 0:
                self.wids['e_dc_restantes'].modify_base(gtk.STATE_NORMAL, 
                                                      self.wids['e_dc_restantes'].get_colormap().alloc_color("orange"))
            else:
                self.wids['e_dc_restantes'].modify_base(gtk.STATE_NORMAL, 
                                                      self.wids['e_dc_restantes'].get_colormap().alloc_color("red"))
            diasAsuntosPropiosRestantes = empleado.get_diasAsuntosPropiosRestantes(anno)
            self.wids['e_dap_restantes'].set_text('%d' % diasAsuntosPropiosRestantes)
            if diasAsuntosPropiosRestantes > 0:
                self.wids['e_dap_restantes'].modify_base(gtk.STATE_NORMAL, 
                                                      self.wids['e_dap_restantes'].get_colormap().alloc_color("white"))
            elif diasAsuntosPropiosRestantes == 0:
                self.wids['e_dap_restantes'].modify_base(gtk.STATE_NORMAL, 
                                                      self.wids['e_dap_restantes'].get_colormap().alloc_color("orange"))
            else:
                self.wids['e_dap_restantes'].modify_base(gtk.STATE_NORMAL, 
                                                      self.wids['e_dap_restantes'].get_colormap().alloc_color("red"))
            self.rellenar_ausencias(empleado)
            self.rellenar_bajas(empleado)
            try:
                utils.combo_set_from_db(self.wids['cbe_empleado'], empleado.id)
                # No sé qué pasa con el model cuando se abre la ventana 
                # en un objeto determinado pero casca diciendo que es 
                # None. Lo ignoro y punto. En siguientes llamadas a 
                # rellenar_widgets ya no peta.
            except:
                pass
            self.objeto = empleado
            self.objeto.make_swap()
        else:
            utils.combo_set_from_db(-1)
            self.wids['e_centro'].set_text('')
            self.wids['e_dias_convenio'].set_text('')
            self.wids['e_dias_asuntos_propios'].set_text('')
            self.wids['e_dc_restantes'].set_text('')
            self.wids['e_dap_restantes'].set_text('')
            self.rellenar_ausencias(empleado)
            self.rellenar_bajas(empleado)

    def rellenar_ausencias(self, empleado):
        model = self.wids['tv_ausencias'].get_model()
        if model != None:
            model.clear()
            if self.objeto != None:
                anno = self.wids['sp_anno'].get_value()
                for ausencia in [a for a in self.objeto.ausencias if a.fecha.year == anno]:
                    model.append((utils.str_fecha(ausencia.fecha), 
                                  ausencia.motivo \
                                     and "%s %s" % (ausencia.motivo.descripcion, ausencia.motivo.descripcionDias) \
                                     or "",
                                  ausencia.observaciones,
                                  ausencia.id))

    def rellenar_bajas(self, empleado):
        model = self.wids['tv_bajas'].get_model()
        if model != None:
            model.clear()
            if self.objeto != None:
                anno = self.wids['sp_anno'].get_value()
                for baja in [b for b in self.objeto.bajas 
                             if b.fechaInicio.year == anno]:
                    model.append(
                      (utils.str_fecha(baja.fechaInicio), 
                       baja.fechaFin and utils.str_fecha(baja.fechaFin) or "", 
                       baja.motivo, 
                       baja.observaciones,
                       baja.id))

    def add_ausencia(self, b):
        fecha = utils.str_fecha(utils.mostrar_calendario(padre = self.wids['ventana']))
        dia, mes, anno = map(int, fecha.split('/'))
        fecha = mx.DateTime.DateTimeFrom(day = dia, month = mes, year = anno)
        opciones = []
        for motivo in pclases.Motivo.select():
            opciones.append((motivo.id, "%s %s" % (motivo.descripcion, motivo.descripcionDias)))
        idmotivo = utils.dialogo_combo(titulo = "¿MOTIVO?", 
                                       texto = "Seleccione motivo de ausencia", 
                                       ops = opciones,
                                       padre = self.wids['ventana'])
        if idmotivo != None:
            motivo = pclases.Motivo.get(idmotivo)
            defecto = "%d" % motivo.excedenciaMaxima
            duracion = utils.dialogo_entrada(titulo = "DURACIÓN",
                                             texto = "Introduzca la duración en días de la ausencia.",
                                             padre = self.wids['ventana'],
                                             valor_por_defecto = defecto)
            try:
                duracion = int(duracion)
                for i in range(duracion):
                    ausencia = pclases.Ausencia(empleado = self.objeto, 
                                                fecha = fecha + (mx.DateTime.oneDay * i), 
                                                motivo = motivo)
                    pclases.Auditoria.nuevo(ausencia, self.usuario, __file__)
                self.actualizar_ventana()
            except ValueError:
                utils.dialogo_info(titulo = "VALOR INCORRECTO",
                                   texto = "Debe teclear un número. Vuelva a intentarlo",
                                   padre = self.wids['ventana'])

    def drop_ausencia(self, b):
        model, itr = self.wids['tv_ausencias'].get_selection().get_selected()
        if itr != None:
            ide = model[itr][-1]
            ausencia = pclases.Ausencia.get(ide)
            ausencia.destroy(ventana = __file__)
            self.actualizar_ventana()
        else:
            utils.dialogo_info(titulo = "SELECCIONE AUSENCIA", 
                               texto = "Seleccione la ausencia a eliminar.", 
                               padre = self.wids['ventana'])

    def add_baja(self, boton):
        """
        Crea una nueva baja laboral para el empleado actual.
        """
        fecha = utils.str_fecha(utils.mostrar_calendario(
            padre = self.wids['ventana']))
        dia, mes, anno = map(int, fecha.split('/'))
        fecha = mx.DateTime.DateTimeFrom(day = dia, month = mes, year = anno)
        bajas = self.objeto.bajas[:]
        bajas.sort(lambda f1, f2: (f1.fechaInicio < f2.fechaInicio and -1) \
                                  or (f1.fechaInicio > f2.fechaInicio and 1) \
                                  or 0)
        fechaFin = None
        for b in bajas:
            if b.fechaInicio >= fecha:
                fechaFin = b.fechaInicio
            if b.esta_vigente(fecha):
                utils.dialogo_info(titulo = "BAJA SOLAPADA", 
                                   texto = "Las bajas médicas no pueden solaparse entre sí, elija otra fecha.", 
                                   padre = self.wids['ventana'])
                return
        baja = pclases.Baja(empleado = self.objeto, 
                            fechaInicio = fecha, 
                            fechaFin = fechaFin)
        pclases.Auditoria.nuevo(baja, self.usuario, __file__)
        self.actualizar_ventana()

    def drop_baja(self, boton):
        model, itr = self.wids['tv_bajas'].get_selection().get_selected()
        if itr != None:
            ide = model[itr][-1]
            baja = pclases.Baja.get(ide)
            baja.destroy(ventana = __file__)
            self.actualizar_ventana()
        else:
            utils.dialogo_info(titulo = "SELECCIONE BAJA", 
                               texto = "Seleccione la baja a eliminar.", 
                               padre = self.wids['ventana'])

    def imprimir_ausencia(self, b):
        from formularios import reports as informes
        model, itr = self.wids['tv_ausencias'].get_selection().get_selected()
        if itr != None:
            ide = model[itr][-1]
            ausencia = pclases.Ausencia.get(ide)
            empleado = ausencia.empleado.nombre + ' ' +ausencia.empleado.apellidos
            centro = ausencia.empleado.centroTrabajo
            if centro != None:
                centro = centro.nombre
            else:
                centro = ''
            fecha = ausencia.fecha
            turno = '______'
            grupo = ausencia.empleado.grupo
            if grupo != None:
                for l in grupo.laborables:
                    if l.fecha == ausencia.fecha:
                        turno = l.turno.nombre
            motivo = ausencia.motivo
            motivos = pclases.Motivo.select()
            informes.abrir_pdf(geninformes.ausencia(empleado,centro,fecha,turno,motivo,motivos))
        else:
            utils.dialogo_info(titulo = "SELECCIONE AUSENCIA", 
                               texto = "Seleccione la ausencia a imprimir.", 
                               padre = self.wids['ventana'])


if __name__ == '__main__':
    import random
    v = Ausencias(pclases.Empleado.select()[random.randrange(pclases.Empleado.select().count())])

