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
## listado_rollos.py --
###################################################################
## NOTAS:
##
###################################################################
## Changelog:
##
##
###################################################################

from framework import pclases
from informes import geninformes
from partes_de_fabricacion_rollos import build_etiqueta
from ventana import Ventana
import gtk
import time
import mx.DateTime
import pygtk
from formularios import utils
pygtk.require('2.0')

class ListadoRollosDefectuosos(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'listado_rollos_defectuosos.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin,
                       'b_buscar/clicked': self.buscar_rollos, 
                       'b_imprimir/clicked': self.imprimir, 
                       'b_etiquetas/clicked': self.etiquetar, 
                       'b_exportar/clicked': self.exportar
                      }
        self.add_connections(connections)
        cols = (('Código rollo','gobject.TYPE_STRING',False,True,False,None),
                ('Fecha Fab.','gobject.TYPE_STRING',False,True,False,None),
                ('Fecha parte.','gobject.TYPE_STRING',False,True,False,None),
                ('Partida','gobject.TYPE_STRING',False,True,False,None),
                ('Albarán','gobject.TYPE_STRING',False,True,False,None),
                ('Metros l.', 'gobject.TYPE_STRING', False, True, False, None),
                ('Id','gobject.TYPE_INT64',False,False,False,None))
        utils.preparar_treeview(self.wids['tv_rollos'], cols)
        self.wids['tv_rollos'].get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        self.wids['tv_rollos'].connect("row-activated", self.mostrar_rollo)
        self.colorear(self.wids['tv_rollos'])
        self.wids['tv_rollos'].connect("cursor-changed", self.mostrar_hora_parte)
        # self.rellenar_tabla()
        temp = time.localtime()
        self.fin = mx.DateTime.localtime()
        self.inicio = None
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        gtk.main()

    def buscar_rollos(self, boton):
        rollosdef = pclases.RolloDefectuoso.select()
        por_producto = {}
        for rd in rollosdef:
            # Ignoro rollos defectuosos fuera del rango.
            if self.inicio and rd.fechahora < self.inicio:
                continue
            if self.fin and rd.fechahora > self.fin:
                continue
            prod = rd.articulo.productoVenta
            if prod not in por_producto:
                por_producto[prod] = [rd]
            else:
                por_producto[prod].append(rd)
        self.rellenar_tabla(por_producto)

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        tv = self.wids['tv_rollos']
        abrir_csv(treeview2csv(tv))

    def mostrar_rollo(self, tv, path, view_col):
        """
        Muestra el rollo en la ventana de trazabilidad.
        """
        if tv.get_model()[path].parent != None:
            ide = tv.get_model()[path][-1]
            if ide != None and ide > 0:
                rollo = pclases.Articulo.get(ide).rolloDefectuoso
                from formularios import trazabilidad_articulos
                trazabilidad_articulos.TrazabilidadArticulos(
                    usuario = self.usuario, 
                    objeto = rollo)
 
    def imprimir(self, boton):
        """
        Crea un PDF con el contenido del TreeView.
        """
        from informes.treeview2pdf import treeview2pdf
        from formularios.reports import abrir_pdf
        tv = self.wids['tv_rollos']
        model = tv.get_model()
        model.append(None, ("===", "===", "===", "===", "===", "===", 0))
        model.append(None, ("", 
                            "TOTAL ALMACÉN:", 
                            self.wids['e_total_almacen'].get_text(), 
                            "TOTAL FABRICADO:", 
                            self.wids['e_total_fabricado'].get_text(), 
                            "", 
                            0))
        fecha = "%s hasta %s" % (self.wids['e_fechainicio'].get_text(),
                                 self.wids['e_fechafin'].get_text())
        fpdf = treeview2pdf(tv, 
                            titulo = "Rollos defectuosos", 
                            fecha = fecha)
        del model[-1]
        del model[-1]
        abrir_pdf(fpdf)

    def mostrar_hora_parte(self, tv):
        """
        Muestra la hora del parte del artículo donde se 
        encuentra el cursor en el TreeView.
        """
        model, paths = tv.get_selection().get_selected_rows()
        for path in paths:
            itr = model.get_iter(path)
            if itr != None and model[itr][2] == "CLIC PARA VER":
                articulo = pclases.Articulo.get(model[itr][-1])
                if articulo.parteDeProduccionID != None:
                    model[itr][2] = utils.str_fecha(articulo.parteDeProduccion.fecha)
                else:
                    model[itr][2] = "¡Sin parte de producción!"
    
    def set_inicio(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
        self.inicio = mx.DateTime.DateTimeFrom(day = temp[0], month = temp[1], year = temp[2])

    def get_unambiguous_fecha(self, fecha):
        try:
            res = fecha.strftime('%B %d, %Y')
        except AttributeError:  # Fecha es None
            return ""
        trans = {'January': 'enero',
                 'February': 'febrero',
                 'March': 'marzo',
                 'April': 'abril',
                 'May': 'mayo',
                 'June': 'junio',
                 'July': 'julio',
                 'August': 'agosto',
                 'September': 'septiembre',
                 'October': 'octubre',
                 'November': 'noviembre',
                 'December': 'diciembre'}
        for in_english in trans:
            res = res.replace(trans[in_english], in_english)
        return res


    def set_fin(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.fin = mx.DateTime.DateTimeFrom(day = temp[0], month = temp[1], year = temp[2])

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, rollos_por_producto):
        """
        Rellena el model con el listado de rollos correspondiente.
        """
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        model = self.wids['tv_rollos'].get_model()
        model.clear()
        metros_almacen = 0
        rollos_almacen = 0
        metros_fabricados = 0
        i = 0.0
        totales_por_producto = {}   
            # Totales por producto. Fabricados y en almacén.
        tot = sum([len(rollos_por_producto[p]) 
                   for p in rollos_por_producto.keys()])
        vpro.mostrar()
        # XXX Primer intento de acelerar los treeview
        self.wids['tv_rollos'].freeze_child_notify()
        self.wids['tv_rollos'].set_model(None)
        # XXX
        for p in rollos_por_producto:
            nodo_producto = model.append(None, (p.descripcion, 
                                                "", 
                                                "", 
                                                p.codigo, 
                                                "", 
                                                "", 
                                                p.id))
            if nodo_producto not in totales_por_producto:
                totales_por_producto[nodo_producto] = [0, 0, 0.0, 0.0]
                # Rollos fabricados, rollos en almacén.
                # Metros cuadrados fabricados, metros cuadrados en almacén.
            for rd in rollos_por_producto[p]:
                a = rd.articulo
                metros2 = a.superficie 
                vpro.set_valor(i/tot, 'Añadiendo rollo %s...' % a.codigo)
                if (a.albaranSalida != None 
                    and a.albaranSalida.fecha <= self.fin):
                    # FILTRO LOS ALBARANES FUERA DEL RANGO SUPERIOR DE 
                    # FECHAS PARA QUE APAREZCAN COMO QUE ESTABAN EN ALMACÉN 
                    # ANTES DE ESE DÍA.
                    info_albaran = "%s (%s)" % (a.albaranSalida.numalbaran, 
                                    utils.str_fecha(a.albaranSalida.fecha))
                    model.append(nodo_producto, 
                                 (a.codigo,
                                  utils.str_fecha(a.rolloDefectuoso.fechahora),
                                  "CLIC PARA VER", 
                                  a.partida.codigo,
                                  info_albaran,
                                  utils.float2str(a.get_largo(), autodec=True), 
                                  a.id))
                else:   # En almacén en el rango de fechas especificado.
                    model.append(nodo_producto, 
                                 (a.codigo,
                                  utils.str_fecha(a.rolloDefectuoso.fechahora),
                                  utils.str_fecha(a.rolloDefectuoso.fechahora),
                                  a.partida.codigo,
                                  '-',
                                  utils.float2str(a.get_largo(), autodec=True), 
                                  a.id))
                    totales_por_producto[nodo_producto][1] += 1
                    totales_por_producto[nodo_producto][3] += metros2
                    metros_almacen += metros2
                    rollos_almacen += 1
                metros_fabricados += metros2
                i += 1
                totales_por_producto[nodo_producto][0] += 1
                totales_por_producto[nodo_producto][2] += metros2
        # XXX Primer intento de acelerar los treeview
        self.wids['tv_rollos'].set_model(model)
        self.wids['tv_rollos'].thaw_child_notify()
        # XXX
        vpro.ocultar()
        # self.wids['e_total_almacen'].set_text(str(metros_almacen)+' m²')
        # self.wids['e_total_fabricado'].set_text(str(metros_fabricados)+' m²')
        self.wids['e_total_almacen'].set_text('%s m² (%d rollos)' % (utils.float2str(metros_almacen, 0), rollos_almacen))
        self.wids['e_total_fabricado'].set_text('%s m² (%d rollos)' % (utils.float2str(metros_fabricados, 0), tot))
        for itr in totales_por_producto:
            model[itr][5] = "%d (%s) / %d (%s)" % (
                totales_por_producto[itr][1], 
                utils.float2str(totales_por_producto[itr][3]),
                totales_por_producto[itr][0], 
                utils.float2str(totales_por_producto[itr][2]))

    def colorear(self, tv):
        def cell_func(column, cell, model, itr):
            numalbaran = model[itr][4]
            if model[itr].parent != None:
                if numalbaran != '-':
                    color = "red"
                else:
                    codrollo = model[itr][0]
                    if "X" in codrollo:
                        color = "DarkOrange1"
                    elif "D" in codrollo:
                        color = "LightGray"
                    else:
                        color = "white"
            else:
                color = None
            cell.set_property("cell-background", color)

        cols = tv.get_columns()
        for i in xrange(len(cols)):
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell,cell_func)
    
    def _dialogo_entrada(self, texto= '', titulo = 'ENTRADA DE DATOS', valor_por_defecto = '', padre=None, pwd = False):
        """
        Muestra un diálogo modal con un textbox.
        Devuelve el texto introducido o None si se
        pulsó Cancelar.
        valor_por_defecto debe ser un string.
        Si pwd == True, es un diálogo para pedir contraseña
        y ocultará lo que se introduzca.

        CALCADO de partes_de_fabricacion_rollos.py (de momento, hasta
        que lo saque del objeto ventana y lo importe desde aquí).
        """
        ## HACK: Los enteros son inmutables, usaré una lista
        res = [None]
        de = gtk.Dialog(titulo,
                        padre,
                        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                        (gtk.STOCK_OK, gtk.RESPONSE_OK,
                         gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        de.connect("response", utils.respuesta_ok_cancel, res)
        txt = gtk.Label(texto)
        de.vbox.pack_start(txt)
        txt.show()
        einput = gtk.Entry()
        einput.set_visibility(not pwd)
        def pasar_foco(widget, event):
            if event.keyval == 65293 or event.keyval == 65421:
                de.action_area.get_children()[1].grab_focus()
        einput.connect("key_press_event", pasar_foco)
        de.vbox.pack_start(einput)
        einput.show()
        einput.set_text(valor_por_defecto)
        marcado = gtk.CheckButton("Mostrar etiqueta de marcado CE")
        marcado.set_active(True)
        de.vbox.pack_start(marcado)
        marcado.show()
        if len(titulo)<20:
            width = 100
        elif len(titulo)<60:
            width = len(titulo)*10
        else:
            width = 600
        de.resize(width, 80)
        de.run()
        de.destroy()
        if res[0]==False:
            return None, None
        return res[0], marcado.get_active()

    def etiquetar(self, boton):
        """
        Genera el PDF de las etiquetas seleccionadas en el TreeView.
        Para poder imprimir es necesario que el usuario tenga el permiso 
        "escritura" sobre la ventana.
        """
        mywin = pclases.Ventana.select(
                    pclases.Ventana.q.fichero == "listado_rollos.py")[0]
        if (self.usuario == None 
            or self.usuario.get_permiso(mywin).escritura): # OJO: HARCODED
            sel = self.wids['tv_rollos'].get_selection()
            model, paths = sel.get_selected_rows()
            rollos_defecto = []
            for path in paths: 
                rollos_defecto.append(model[path][0])
                rollos_defecto.sort()
            rollos_defecto = ', '.join(rollos_defecto)
            from formularios import reports
            entrada, mostrar_marcado = self._dialogo_entrada(titulo='ETIQUETAS', 
                                                             texto="Introduzca los números de rollo, separados por coma, que desea etiquetar:",
                                                             valor_por_defecto = rollos_defecto,
                                                             padre = self.wids['ventana'])
            if entrada != None:
                codigos = [cod.strip() for cod in entrada.split(",")]
                temp = []
                for codigo in codigos:
                    if codigo.startswith("R"):
                        try:
                            temp.append(pclases.Rollo.select(pclases.Rollo.q.codigo == codigo)[0])
                        except Exception, msg:
                            self.logger.error("listado_rollos::etiquetar -> %s" % (msg))
                    elif codigo.startswith("X"):
                        try:
                            temp.append(pclases.RolloDefectuoso.select(pclases.RolloDefectuoso.q.codigo == codigo)[0])
                        except Exception, msg:
                            self.logger.error("listado_rollos::etiquetar -> %s" % (msg))
                    else:
                        pass    # No lo encuentro, paso de dar un mensaje de error.
                rollos = []
                fetiqueta = None
                for r in temp:
                    elemento, fetiqueta = build_etiqueta(r)
                    rollos.append(elemento)
                    pclases.Auditoria.modificado(r, self.usuario, __file__, 
                      "Impresión de etiqueta para rollo %s" % r.get_info())
                reports.abrir_pdf(geninformes.etiquetasRollosEtiquetadora(
                    rollos, mostrar_marcado, hook = fetiqueta))    
                    # Etiquetas térmicas pequeñas.
        else:
            utils.dialogo_info(titulo = "USUARIO SIN PRIVILEGIOS", 
                               texto = "Para poder crear etiquetas de rollos"
                                       " existentes es necesario\nque tenga "
                                       "permiso de escritura sobre la ventana"
                                       " actual.", 
                               padre = self.wids['ventana'])


if __name__ == '__main__':
    t = ListadoRollosDefectuosos()

