#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2018  Francisco José Rodríguez Bogado,                   #
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
# # partes_no_bloqueados.py - Partes de producción no bloqueados.
###################################################################
# # NOTAS:
# #
###################################################################
# # Changelog:
# # 22 de mayo de 2006 -> Inicio
###################################################################
# # BUG: Si abre dos o más partes, bloquea alguno, vuelve a la
# # ventana y actualiza con el botón Actualizar, es posible que
# # se le active el CheckBox en el cell del path que ahora ocuparía
# # otro parte distinto (ya que el que ha sido verificado ya no
# # aparecería en la lista).
###################################################################

from __future__ import print_function
from framework import pclases
from ventana import Ventana
import gtk
import pygtk
import sys
from formularios import utils
from formularios import ventana_progreso
pygtk.require('2.0')


class PartesNoBloqueados(Ventana):
    def __init__(self, objeto=None, usuario=None):
        self.usuario = usuario
        Ventana.__init__(self, 'partes_no_bloqueados.glade', objeto,
                         usuario=usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_editar/clicked': self.abrir_parte,
                       'b_actualizar/clicked': self.actualizar}
        self.add_connections(connections)
        cols = (('Producto', 'gobject.TYPE_STRING', False, True, True, None),
                ('Fecha', 'gobject.TYPE_STRING', False, True, False, None),
                ('Inicio turno', 'gobject.TYPE_STRING',
                    False, True, False, None),
                ('Fin turno', 'gobject.TYPE_STRING', False, True, False, None),
                ('Visto', 'gobject.TYPE_BOOLEAN',
                    True, True, False, self.bloquear),
                ('Lote/Partida', 'gobject.TYPE_STRING',
                    False, True, False, None),
                ('#', 'gobject.TYPE_STRING', False, True, False, None),
                ('m²', 'gobject.TYPE_STRING', False, True, False, None),
                ('kg ℮', 'gobject.TYPE_STRING', False, True, False, None),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_partes'], cols)
        self.wids['tv_partes'].connect("row-activated", self.abrir_parte_tv)
        self.colorear(self.wids['tv_partes'])
        try:
            ventanas_con_permiso = [p.ventana.fichero
                                    for p in self.usuario.permisos
                                    if p.permiso]
            # and p.escritura]  # STILL UNIMPLEMENTED
        except AttributeError:
            print("De momento esta ventana sólo se puede abrir desde el menú.")
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
            txt_dialogo = "No tiene permisos suficientes para bloquear partes."
            utils.dialogo_info(titulo="USUARIO SIN PERMISOS",
                               texto=txt_dialogo,
                               padre=self.wids['ventana'])

    def chequear_cambios(self):
        pass

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
                txt_warn = "%spartes_no_bloqueados::rellenar_partes"
                " -> El parte ID %d se solapa con otros de la misma línea."
                "Si estaba verificado, lo desbloqueo para que se vuelva a"
                " revisar." % (self.usuario
                               and self.usuario.usuario + ": " or "", pdp.id)
                self.logger.warning(txt_warn)
                pdp.bloqueado = False
        # Y ahora meto los de la consulta real:
        model.clear()
        self.wids['tv_partes'].freeze_child_notify()
        self.wids['tv_partes'].set_model(None)
        vpro = ventana_progreso.VentanaProgreso(padre=self.wids['ventana'])
        vpro.mostrar()
        i = 0.0
        partes = pclases.ParteDeProduccion.select(
            pclases.ParteDeProduccion.q.bloqueado==False, orderBy="id")  # noqa
        tot = partes.count()
        for parte in partes:
            vpro.set_valor(i/tot, 'Recuperando parte %s' % utils.str_fecha(
                parte.fecha))
            parte.sync()    # ¿Algún cambio en la BD no rescatado en local?
            i += 1
            if (self.wids['rb_todos'].get_active()
                    or (self.wids['rb_balas'].get_active()
                        and parte.es_de_balas())
                    or (self.wids['rb_rollos'].get_active()
                        and parte.es_de_rollos())
                    or (self.wids['rb_bolsas'].get_active()
                        and parte.es_de_bolsas())):
                producto = parte.get_producto_fabricado()
                if producto:
                    str_producto = "{}: {}".format(producto.id,
                                                   producto.descripcion)
                    lotepartida = get_str_lote_partida(parte)
                else:
                    str_producto = "VACÍO"
                    lotepartida = ""
                bultos = len(parte.articulos)
                metros = utils.float2str(
                        sum([a.superficie and a.superficie or 0
                             for a in parte.articulos]))
                kilos = utils.float2str(
                        sum([a.peso_neto for a in parte.articulos]))
                model.append((str_producto,
                              utils.str_fecha(parte.fecha),
                              parte.horainicio.strftime('%H:%M'),
                              parte.horafin.strftime('%H:%M'),
                              parte.bloqueado,
                              lotepartida,
                              bultos,
                              metros,
                              kilos,
                              parte.id))
        self.wids['tv_partes'].set_model(model)
        self.wids['tv_partes'].thaw_child_notify()
        vpro.ocultar()

    def actualizar(self, b):
        self.rellenar_partes()

    def abrir_parte(self, b):
        model, itr = self.wids['tv_partes'].get_selection().get_selected()
        if itr is not None:
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
        from formularios import launcher
        model = self.wids['tv_partes'].get_model()
        model[path][4] = True   # OJO: Directamente se marca como visto.
        # En los partes se asegura que no se cierre hasta que la
        # casilla esté marcada.
        # HARCODED: Esas rutas a las ventanas de partes de producción...
        if parte.es_de_balas():
            try:
                raise NotImplementedError
                launcher.run("partes_de_fabricacion_balas",
                             "PartesDeFabricacionBalas",
                             self.usuario, pclases.confi, parte.puid)
            except:     # noqa
                from formularios import partes_de_fabricacion_balas as pdpb
                ventana_parteb = pdpb.PartesDeFabricacionBalas(parte)
        elif parte.es_de_rollos():
            try:
                raise NotImplementedError
                launcher.run("partes_de_fabricacion_rollos",
                             "PartesDeFabricacionRollos",
                             self.usuario, pclases.confi, parte.puid)
            except:     # noqa
                from formularios import partes_de_fabricacion_rollos as pdpr
                ventana_parteb = pdpr.PartesDeFabricacionRollos(parte)
        elif parte.es_de_bolsas():
            try:
                raise NotImplementedError
                launcher.run("partes_de_fabricacion_bolsas",
                             "PartesDeFabricacionBolsas",
                             self.usuario, pclases.confi, parte.puid)
            except:     # noqa
                from formularios import partes_de_fabricacion_bolsas as pdpc
                ventana_parteb = pdpc.PartesDeFabricacionBolsas(parte)  # noqa

    def bloquear(self, cell, path):
        """
        Abre el parte para ser revisado.
        """
        model = self.wids['tv_partes'].get_model()
        bloqueado = not cell.get_active()  # noqa
        ide = model[path][-1]
        parte = pclases.ParteDeProduccion.get(ide)
        self.abrir_ventana_parte(parte, path)
        # Cambiado comportamiento para obligar a revisar el parte.
        # parte.bloqueado = bloqueado
        # parte.syncUpdate()

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
                    color = None    # Parte borrado. Lo ignoro. En cuanto
                    # recargue la ventana desaparecerá el "error".
            cell.set_property("cell-background", color)

        cols = tv.get_columns()
        for i in (1, 2, 3):  # Las columnas que corresponden a la fecha y horas
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell, cell_func, i)


def get_str_lote_partida(parte):
    """
    Código de lote o partida del parte recibido o cadena vacía si no tiene
    producción.
    """
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
        lotepartida = ''
    return lotepartida


if __name__ == '__main__':
    t = PartesNoBloqueados()
