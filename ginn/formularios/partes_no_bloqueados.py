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
## partes_no_bloqueados.py - Partes de producción no bloqueados.
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 22 de mayo de 2006 -> Inicio
###################################################################
## BUG: Si abre dos o más partes, bloquea alguno, vuelve a la 
## ventana y actualiza con el botón Actualizar, es posible que 
## se le active el CheckBox en el cell del path que ahora ocuparía
## otro parte distinto (ya que el que ha sido verificado ya no 
## aparecería en la lista).
###################################################################

from framework import pclases
from ventana import Ventana
import gtk
import pygtk
import sys
from formularios import utils
from formularios import ventana_progreso
pygtk.require('2.0')

class PartesNoBloqueados(Ventana):
    def __init__(self, objeto = None, usuario = None):
        self.usuario = usuario
        Ventana.__init__(self, 'partes_no_bloqueados.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_editar/clicked': self.abrir_parte,
                       'b_actualizar/clicked': self.actualizar}
        self.add_connections(connections)
        cols = (('Producto', 'gobject.TYPE_STRING', False, True, True, None),
                ('Fecha','gobject.TYPE_STRING', False, True, False, None),
                ('Inicio turno','gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Fin turno','gobject.TYPE_STRING', False, True, False, None),
                ('Visto','gobject.TYPE_BOOLEAN', 
                    True, True, False, self.bloquear),
                ('Lote/Partida', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_partes'], cols)
        self.wids['tv_partes'].connect("row-activated", self.abrir_parte_tv)
        self.wids['tv_partes'].connect("cursor-changed", 
            self.mostrar_info_parte)
        self.colorear(self.wids['tv_partes'])
        try:
            ventanas_con_permiso = [p.ventana.fichero 
                for p in self.usuario.permisos if p.permiso] 
                    # and p.escritura]  # STILL UNIMPLEMENTED
        except AttributeError:
            print "De momento esta ventana sólo se puede abrir desde el menú."
            sys.exit(1)
        for w in ("rb_bolsas", "rb_balas", "rb_rollos", "rb_todos"):
            self.wids[w].set_sensitive(False)
        tiene_al_menos_un_permiso = False
        if ('partes_de_fabricacion_balas.py' in ventanas_con_permiso 
            and 'partes_de_fabricacion_rollos.py' in ventanas_con_permiso
            and 'partes_de_fabricacion_bolsas.py' in ventanas_con_permiso):
            self.wids['rb_todos'].set_active(True)
            for w in ("rb_bolsas", "rb_balas", "rb_rollos", "rb_todos"):
                self.wids[w].set_sensitive(True)
            tiene_al_menos_un_permiso = True
        else:
            if 'partes_de_fabricacion_balas.py' in ventanas_con_permiso:
                self.wids['rb_balas'].set_sensitive(True)
                self.wids['rb_balas'].set_active(True)
                tiene_al_menos_un_permiso = True
            if 'partes_de_fabricacion_rollos.py' in ventanas_con_permiso:
                self.wids['rb_rollos'].set_sensitive(True)
                self.wids['rb_rollos'].set_active(True)
                tiene_al_menos_un_permiso = True
            if 'partes_de_fabricacion_bolsas.py' in ventanas_con_permiso:
                self.wids['rb_bolsas'].set_sensitive(True)
                self.wids['rb_bolsas'].set_active(True)
                tiene_al_menos_un_permiso = True
        if tiene_al_menos_un_permiso:
            self.rellenar_partes()
            gtk.main()
        else:
            utils.dialogo_info(titulo = "USUARIO SIN PERMISOS", 
                texto = "No tiene permisos suficientes para bloquear partes.", 
                padre = self.wids['ventana'])

    def chequear_cambios(self):
        pass

    def mostrar_info_parte(self, tv):
        self.wids['ventana'].window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        while gtk.events_pending(): gtk.main_iteration(False)
        try:
            model, itr = tv.get_selection().get_selected()
        except AttributeError:
            self.wids['ventana'].window.set_cursor(None)
            return  # TreeView es None porque se estaba cerrando la ventana o 
                    # algo.
        if itr!=None and model[itr][0] == "CLIC PARA VER":
            try:
                parte = pclases.ParteDeProduccion.get(model[itr][-1])
            except pclases.SQLObjectNotFound:
                self.wids['ventana'].window.set_cursor(None)
                return  # Parte borrado
            if parte.es_de_balas() and parte.articulos != []:
                try:
                    lotepartida = parte.articulos[0].bala.lote.codigo
                except AttributeError:
                    lotepartida = parte.articulos[0].bigbag.loteCem.codigo
            elif parte.es_de_rollos() and parte.articulos != []:
                try:
                    lotepartida = parte.articulos[0].partida.codigo
                except AttributeError:
                    lotepartida = "ERROR: PARTE INCOHERENTE"
            elif parte.es_de_bolsas() and parte.articulos != []:
                try:
                    lotepartida = parte.partidaCem.codigo
                except AttributeError:
                    lotepartida = "ERROR: PARTE INCOHERENTE"
            else:
                lotepartida = 'VACIO'
            producto = (parte.articulos != [] 
                        and parte.articulos[0].productoVenta.nombre or 'VACÍO')
            model[itr][0] = producto
            model[itr][5] = lotepartida
        self.wids['ventana'].window.set_cursor(None)

    def rellenar_partes(self):
        """
        Rellena el model con los partes no bloqueados.
        """
        model = self.wids['tv_partes'].get_model()
        # Primero verifico los que ya estaban (si es que había alguno):
        for fila in model:
            idparte = fila[-1]
            try:
                pdp = pclases.ParteDeProduccion.get(idparte)
            except pclases.SQLObjectNotFound:
                continue    # El parte se ha borrado entre actualización y 
                            # actualización de la ventana.
            pdp.sync()  # ¿Hay algún cambio pendiente de rescatar en local?
            if pdp.se_solapa():
                self.logger.warning("%spartes_no_bloqueados::rellenar_partes"
                    " -> El parte ID %d se solapa con otros de la misma línea."
                    "Si estaba verificado, lo desbloqueo para que se vuelva a"
                    " revisar." % (self.usuario 
                        and self.usuario.usuario + ": " or "", pdp.id))
                pdp.bloqueado = False
        # Y ahora meto los de la consulta real:
        model.clear()
        self.wids['tv_partes'].freeze_child_notify()
        self.wids['tv_partes'].set_model(None)
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        i = 0.0
        partes = pclases.ParteDeProduccion.select(
            pclases.ParteDeProduccion.q.bloqueado == False, orderBy = "id")
        tot = partes.count()
        for parte in partes:
            vpro.set_valor(i/tot, 'Recuperando parte %s' 
                % utils.str_fecha(parte.fecha))
            parte.sync()    # ¿Algún cambio en la BD no rescatado en local?
            i += 1
            lotepartida = "CLIC PARA VER"
            if (self.wids['rb_todos'].get_active() or 
               (self.wids['rb_balas'].get_active() and parte.es_de_balas()) or 
               (self.wids['rb_rollos'].get_active() and parte.es_de_rollos()) 
                or self.wids['rb_bolsas'].get_active() and parte.es_de_bolsas()
               ):
                model.append(("CLIC PARA VER",
                              utils.str_fecha(parte.fecha),
                              parte.horainicio.strftime('%H:%M'),
                              parte.horafin.strftime('%H:%M'),
                              parte.bloqueado,
                              lotepartida,
                              parte.id))
        self.wids['tv_partes'].set_model(model)
        self.wids['tv_partes'].thaw_child_notify()
        vpro.ocultar()
    
    def actualizar(self, b):    
        self.rellenar_partes()

    def abrir_parte(self, b):
        model, itr = self.wids['tv_partes'].get_selection().get_selected()
        if itr != None:
            self.abrir_parte_tv(self.wids['tv_partes'], model.get_path(itr), 
                                None)

    def abrir_parte_tv(self, treeview, path, view_column):
        model = treeview.get_model()
        idparte = model[path][-1]
        parte = pclases.ParteDeProduccion.get(idparte)
        self.abrir_ventana_parte(parte, path)

    def abrir_ventana_parte(self, parte, path):
        """
        Abre la ventana del parte según el tipo que sea.
        path es el path que ocupa en el model.
        """
        model = self.wids['tv_partes'].get_model()
        model[path][4] = True   # OJO: Directamente se marca como visto. 
                # En los partes se asegura que no se cierre hasta que la 
                # casilla esté marcada.
        if parte.es_de_balas():
            from formularios import partes_de_fabricacion_balas
            ventana_parteb = partes_de_fabricacion_balas.PartesDeFabricacionBalas(parte)  # @UnusedVariable
        elif parte.es_de_rollos():
            from formularios import partes_de_fabricacion_rollos
            ventana_parteb = partes_de_fabricacion_rollos.PartesDeFabricacionRollos(parte)  # @UnusedVariable
        elif parte.es_de_bolsas():
            from formularios import partes_de_fabricacion_bolsas
            ventana_parteb = partes_de_fabricacion_bolsas.PartesDeFabricacionBolsas(parte)  # @UnusedVariable

    def bloquear(self, cell, path):
        """
        Abre el parte para ser revisado.
        """
        model = self.wids['tv_partes'].get_model()
        bloqueado = not cell.get_active()  # @UnusedVariable
        ide = model[path][-1]
        parte = pclases.ParteDeProduccion.get(ide)
        self.abrir_ventana_parte(parte, path)
        # Cambiado comportamiento para obligar a revisar el parte.
        #parte.bloqueado = bloqueado
        #parte.syncUpdate()

    def colorear(self, tv):
        """
        Asocia una función al treeview para resaltar los partes 
        de la misma línea que se solapan entre ellos.
        """
        def cell_func(column, cell, model, itr, numcol):
            """
            Si el parte se solapa con algún otro de su misma línea 
            lo colorea en rojo.
            """
            idparte = model[itr][-1]
            if idparte > 0:
                try:
                    parte = pclases.ParteDeProduccion.get(idparte)
                    if parte.se_solapa():
                        color = "red"
                    else:
                        color = None    # Color por defecto
                except pclases.SQLObjectNotFound:
                    color = None    # Parte borrado. Lo ignoro. En cuanto recargue la ventana desaparecerá el "error".
            cell.set_property("cell-background", color)

        cols = tv.get_columns()
        for i in (1, 2, 3): # Las columnas que corresponden a la fecha y horas 
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell, cell_func, i)

if __name__ == '__main__':
    t = PartesNoBloqueados()

