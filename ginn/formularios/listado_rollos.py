#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2014  Francisco José Rodríguez Bogado,                   #
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

class ListadoRollos(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'listado_rollos.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin,
                       'b_buscar/clicked': self.buscar_rollos,
                       'b_imprimir/clicked': self.imprimir,
                       'b_etiquetas/clicked': self.etiquetar,
                       'b_exportar/clicked': self.exportar
                      }
        self.add_connections(connections)
        cols=(('Código rollo', 'gobject.TYPE_STRING',
                    True, True, False, self.cambiar_numrollo),
              ('Fecha Fab.','gobject.TYPE_STRING',False,True,False,None),
              ('Fecha parte.','gobject.TYPE_STRING',False,True,False,None),
              ('Partida','gobject.TYPE_STRING',False,True,False,None),
              ('Albarán','gobject.TYPE_STRING',False,True,False,None),
              ('Metros l.', 'gobject.TYPE_STRING', False, True, False, None),
              ('Almacén', 'gobject.TYPE_STRING', False, True, False, None),
              ('Idlistado_rollos','gobject.TYPE_INT64',False,False,False,None))
        utils.preparar_listview(self.wids['tv_rollos'], cols)
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
        model = tv.get_model()
        idarticulo = model[path][-1]
        codigo = model[path][0]
        if idarticulo != None and idarticulo > 0:
            articulo = pclases.Articulo.get(idarticulo)
            if codigo.upper().startswith("Y"):
                rollo = articulo.rolloC
            elif codigo.upper().startswith("X"):
                rollo = articulo.rolloDefectuoso
            else:
                rollo = articulo.rollo
            from formularios import trazabilidad_articulos
            trazabilidad_articulos.TrazabilidadArticulos(
                usuario = self.usuario, objeto = rollo)

    def imprimir(self, boton):
        """
        Crea un PDF con el contenido del TreeView.
        """
        datos = []
        model = self.wids['tv_rollos'].get_model()
        for i in model:
            pas = pclases.AlbaranSalida
            if i[4] == "-" or pas.str_tipos[pas.MOVIMIENTO] in i[4]:
                en_almacen = i[6]
            else:
                en_almacen = ""
            if (  (self.wids['ch_filtrar'].get_active()
                   and i[4] == "-"
                   or pas.str_tipos[pas.MOVIMIENTO] in i[4])
                or
                  (not self.wids['ch_filtrar'].get_active())):
                datos.append((i[0], i[1], i[3], i[4], en_almacen, i[5]))
        datos.append(("---", ) * 6)
        datos.append(("Total almacén (no defectuosos):", self.wids['e_total_almacen'].get_text(), "Total fabricado (incluye defectuosos):", self.wids['e_total_fabricado'].get_text(), ""))
        if not self.inicio:
            fechaInforme = 'Hasta: %s' % (utils.str_fecha(self.fin))
        else:
            fechaInforme = utils.str_fecha(self.inicio) + ' - ' + utils.str_fecha(self.fin)
        if datos != []:
            desc_producto = self.wids['e_descripcion'].get_text()
            listado_pdf = geninformes.listado_rollos(datos, desc_producto,
                                                     fechaInforme)
            from formularios import reports
            reports.abrir_pdf(listado_pdf)

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
                    model[itr][2] = utils.str_fecha(
                        articulo.parteDeProduccion.fecha)
                elif articulo.es_rolloC():
                    model[itr][2] = utils.str_fechahora(
                        articulo.rolloC.fechahora)
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

    def rellenar_tabla(self, lista, defectuosos, gtxcs, producto):
        """
        Rellena el model con el listado de rollos correspondiente.
        OJO: Los rollos defectuosos se listan, pero no se cuentan para los
        totales. Los rollos de Gtx C van aparte siempre.
        """
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        model = self.wids['tv_rollos'].get_model()
        model.clear()
        metros_almacen = 0
        rollos_almacen = 0
        metros_fabricados = 0
        kilosc_fabricados = kilosc = 0.0
        rollosc_fabricados = rollosc = 0
        i = 0.0
        # tot = len(lista)
        tot = lista.count() + defectuosos.count() + gtxcs.count()
        vpro.mostrar()
        # XXX Primer intento de acelerar los treeview
        self.wids['tv_rollos'].freeze_child_notify()
        self.wids['tv_rollos'].set_model(None)
        # XXX
        for a in defectuosos:
            metros2 = a.superficie
            metros_fabricados += metros2
            vpro.set_valor(i/tot, 'Añadiendo rollo %s...' % a.codigo)
            if a.albaranSalida != None and a.albaranSalida.fecha <= self.fin:
                # FILTRO LOS ALBARANES FUERA DEL RANGO SUPERIOR DE FECHAS PARA
                # QUE APAREZCAN COMO QUE ESTABAN EN ALMACÉN ANTES DE ESE DÍA.
                try:
                    info_albaran = self.cache_albaranes[a.albaranSalida]
                except KeyError:
                    info_albaran = "%s (%s - %s)" % (a.albaranSalida.numalbaran, utils.str_fecha(a.albaranSalida.fecha), a.albaranSalida.get_str_tipo())
                    self.cache_albaranes[a.albaranSalida] = info_albaran
                model.append((a.codigo,
                              utils.str_fecha(a.rolloDefectuoso.fechahora),
                              "CLIC PARA VER",
                              a.partida.codigo,
                              info_albaran,
                              utils.float2str(a.get_largo(), autodec = True),
                              a.almacen and a.almacen.nombre or "",
                              a.id))
            else:
                model.append((a.codigo,
                              utils.str_fecha(a.rolloDefectuoso.fechahora),
                              utils.str_fecha(a.rolloDefectuoso.fechahora),
                              a.partida.codigo,
                              '-',
                              utils.float2str(a.get_largo(), autodec = True),
                              a.almacen and a.almacen.nombre or "",
                              a.id))
            i += 1
        for a in gtxcs:
            vpro.set_valor(i/tot, 'Añadiendo rollo %s...' % a.codigo)
            rollosc_fabricados += 1
            kilosc_fabricados += a.peso
            if a.albaranSalida != None and a.albaranSalida.fecha <= self.fin:
                # FILTRO LOS ALBARANES FUERA DEL RANGO SUPERIOR DE FECHAS PARA
                # QUE APAREZCAN COMO QUE ESTABAN EN ALMACÉN ANTES DE ESE DÍA.
                try:
                    info_albaran = self.cache_albaranes[a.albaranSalida]
                except KeyError:
                    info_albaran = "%s (%s - %s)" % (a.albaranSalida.numalbaran, utils.str_fecha(a.albaranSalida.fecha), a.albaranSalida.get_str_tipo())
                    self.cache_albaranes[a.albaranSalida] = info_albaran
                model.append((a.codigo,
                              utils.str_fecha(a.rolloC.fechahora),
                              utils.str_hora(a.rolloC.fechahora),
                              "N/A",
                              info_albaran,
                              "%s kg" % utils.float2str(a.peso),
                              a.almacen and a.almacen.nombre or "",
                              a.id))
                # Si tienen albarán hay un caso en que cuentan para almacén:
                if a.albaranSalida and a.albaranSalida.es_de_movimiento():
                    kilosc += a.peso
                    rollosc += 1
            else:
                model.append((a.codigo,
                              utils.str_fecha(a.rolloC.fechahora),
                              utils.str_hora(a.rolloC.fechahora),
                              "N/A",
                              '-',
                              "%s kg" % utils.float2str(a.peso),
                              a.almacen and a.almacen.nombre or "",
                              a.id))
                kilosc += a.peso
                rollosc += 1
            i += 1
        for t in lista:
            metros2 = t.productoVenta.camposEspecificosRollo.metrosLineales * t.productoVenta.camposEspecificosRollo.ancho
            metros_fabricados += metros2
            vpro.set_valor(i/tot, 'Añadiendo rollo %s...' % t.rollo.codigo)
            if t.albaranSalida != None and t.albaranSalida.fecha <= self.fin:
                # FILTRO LOS ALBARANES FUERA DEL RANGO SUPERIOR DE FECHAS PARA
                # QUE APAREZCAN COMO QUE ESTABAN EN ALMACÉN ANTES DE ESE DÍA.
                try:
                    info_albaran = self.cache_albaranes[t.albaranSalida]
                except KeyError:
                    info_albaran = "%s (%s - %s)" % (t.albaranSalida.numalbaran, utils.str_fecha(t.albaranSalida.fecha), t.albaranSalida.get_str_tipo())
                    self.cache_albaranes[t.albaranSalida] = info_albaran
                model.append((t.rollo.codigo,
                        utils.str_fecha(t.rollo.fechahora),
                        # -----------------------------------------------------
                        # t.rollo.articulos[0].parteDeProduccion and utils.str_fecha(t.rollo.articulos[0].parteDeProduccion.fecha) or '',
                        # utils.str_fecha(t.rollo.fechahora),
                        "CLIC PARA VER",
                        # -----------------------------------------------------
                        t.rollo.partida.codigo,
                        info_albaran,
                        utils.float2str(t.get_largo(), autodec = True),
                        t.almacen and t.almacen.nombre or "",
                        t.id))
                # Si tienen albarán hay un caso en que cuentan para almacén:
                if t.albaranSalida and t.albaranSalida.es_de_movimiento():
                    metros_almacen += metros2
                    rollos_almacen += 1
            else:
                model.append((t.rollo.codigo,
                        utils.str_fecha(t.rollo.fechahora),
                        # -----------------------------------------------------
                        # t.rollo.articulos[0].parteDeProduccion and utils.str_fecha(t.rollo.articulos[0].parteDeProduccion.fecha) or '',
                        utils.str_fecha(t.rollo.fechahora),
                        # -----------------------------------------------------
                        t.rollo.partida.codigo,
                        '-',
                        utils.float2str(t.get_largo(), autodec = True),
                        t.almacen and t.almacen.nombre or "",
                        t.id))
                metros_almacen += metros2
                rollos_almacen += 1
            i += 1
        # XXX Primer intento de acelerar los treeview
        self.wids['tv_rollos'].set_model(model)
        self.wids['tv_rollos'].thaw_child_notify()
        # XXX
        vpro.ocultar()

        # self.wids['e_total_almacen'].set_text(str(metros_almacen)+' m²')
        # self.wids['e_total_fabricado'].set_text(str(metros_fabricados)+' m²')
        if producto.es_rolloC():
            self.wids['e_total_almacen'].set_text('%s kg (%d rollos)'
                % (utils.float2str(kilosc, 2), rollosc))
            self.wids['e_total_fabricado'].set_text('%s kg (%d rollos)'
                % (utils.float2str(kilosc_fabricados, 2), rollosc_fabricados))
        else:
            self.wids['e_total_almacen'].set_text('%s m² (%d rollos)'
                % (utils.float2str(metros_almacen, 0), rollos_almacen))
            self.wids['e_total_fabricado'].set_text('%s m² (%d rollos)'
                % (utils.float2str(metros_fabricados, 0), tot))

    def cambiar_numrollo(self, cell, path, newtext):
        ##utils.dialogo_info(titulo = "NO IMPLEMENTADO", texto = "Funcionalidad no implementada.", padre = self.wids['ventana'])
        return
        # FIXME: Cambiar o repasar esto porque ni cambia el código del rollo
        # ni devuelve nada (y tiene una llamada recursiva).
        try:
            numrollo = int(newtext)
        except:
            utils.dialogo_info(titulo = 'NÚMERO NO VÁLIDO', texto = '%s no es un número de rollo válido.' % newtext)
            return
        model = self.wids['tv_rollos'].get_model()
        fila = model[path]
        ide = fila[-1]
        rollo = pclases.Articulo.get(ide).rollo
        if numrollo != rollo.numrollo:
            nuevo_numrollo = rollo.cambiar_numrollo(numrollo)
            if nuevo_numrollo != numrollo:
                utils.dialogo_info(titulo = 'NÚMERO DE ROLLO NO CAMBIADO',
                                texto = 'Número no cambiado. Verifique que no existe ya un rollo con el número %d.' % numrollo)
            else:
                itr = model.get_iter(path)
                model.set_value(itr, 0, nuevo_numrollo)

    def refinar_resultados_busqueda(self, resultados):
        """
        Muestra en una ventana de resultados todos los
        registros de "resultados".
        Devuelve el id (primera columna de la ventana
        de resultados) de la fila seleccionada o None
        si se canceló.
        """
        filas_res = []
        for r in resultados:
            filas_res.append((r.id, r.codigo, r.descripcion))
        idproducto = utils.dialogo_resultado(filas_res,
                                             titulo = 'Seleccione producto',
                                             cabeceras = ('ID Interno', 'Código', 'Descripción'),
                                             padre = self.wids['ventana'])
        if idproducto < 0:
            return None
        else:
            return idproducto

    def buscar_rollos(self,wid):
        """
        Pide el código de un producto y busca todos las unidades de ese producto
        """
        self.cache_albaranes = {}   # Reinicio la caché en cada búsqueda.
        a_buscar = utils.dialogo_entrada(titulo = 'INTRODUZCA DATOS',
                        texto = 'Introduzca el código o descripción\n'
                                'del producto que desea listar:',
                        padre = self.wids['ventana'])
        if a_buscar != None:
            criterio = pclases.OR(pclases.ProductoVenta.q.codigo.contains(a_buscar),
                                            pclases.ProductoVenta.q.descripcion.contains(a_buscar))
            criterio = pclases.AND(criterio,
                    pclases.ProductoVenta.q.camposEspecificosRolloID != None,
                    pclases.ProductoVenta.q.obsoleto==False)
            resultados = pclases.ProductoVenta.select(criterio)
            if resultados.count() > 1:
                    ## Refinar los resultados
                    idproducto = self.refinar_resultados_busqueda(resultados)
                    if idproducto == None:
                        return
                    resultados = [pclases.ProductoVenta.get(idproducto)]
            elif resultados.count() < 1:
                    ## Sin resultados de búsqueda
                    utils.dialogo_info(
                            titulo='ERROR',
                            texto='No hay ningún producto con ese código',
                            padre=self.wids['ventana'])
                    return
            ## Un único resultado
            # Pongo el objeto como actual
            producto = resultados[0]

            self.wids['e_descripcion'].set_text(producto.descripcion)

            # articulos_rollo = [i for i in producto.articulos if i.rolloID!=None]
            and_fecha_inicio = "AND fechahora >= '%s'" % (self.get_unambiguous_fecha(self.inicio))
            articulos_rollo = pclases.Articulo.select("""rollo_id IS NOT NULL AND producto_venta_id = %d
                                                         AND rollo_id IN (SELECT id FROM rollo WHERE fechahora <= '%s' %s ) """ \
                              % (producto.id,
                                 self.get_unambiguous_fecha(
                                    self.fin + mx.DateTime.oneDay),
                                 self.inicio and and_fecha_inicio or ""))
            articulos_defectuosos = pclases.Articulo.select("""rollo_defectuoso_id IS NOT NULL AND producto_venta_id = %d
                              AND rollo_defectuoso_id IN (SELECT id FROM rollo_defectuoso WHERE fechahora <= '%s' %s ) """ \
                              % (producto.id,
                                 self.get_unambiguous_fecha(
                                    self.fin + mx.DateTime.oneDay),
                                 self.inicio and and_fecha_inicio or ""))
            gtxcs = pclases.Articulo.select("""
                rollo_c_id IS NOT NULL AND producto_venta_id = %d
                AND rollo_c_id IN (
                    SELECT id
                    FROM rollo_c
                    WHERE fechahora <= '%s' %s )
            """ % (producto.id,
                   self.get_unambiguous_fecha(self.fin + mx.DateTime.oneDay),
                   self.inicio and and_fecha_inicio or ""))
            self.rellenar_tabla(articulos_rollo,
                                articulos_defectuosos,
                                gtxcs,
                                producto)

    def colorear(self, tv):
        def cell_func(column, cell, model, itr):
            pas = pclases.AlbaranSalida
            numalbaran = model[itr][4]
            if (numalbaran != '-' and
                not pas.str_tipos[pas.MOVIMIENTO] in numalbaran):
                color = "red"
            else:
                codrollo = model[itr][0]
                if "X" in codrollo.upper():
                    color = "DarkOrange1"
                elif "D" in codrollo.upper():
                    color = "LightGray"
                elif "Y" in codrollo.upper():
                    color = "Light blue"
                else:
                    color = "white"
            cell.set_property("cell-background", color)

        cols = tv.get_columns()
        for i in xrange(len(cols)):
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell,cell_func)

    def _dialogo_entrada(self, texto='', titulo='ENTRADA DE DATOS',
                         valor_por_defecto='', padre=None, pwd=False,
                         marcado_disabled=False):
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
        if marcado_disabled:
            marcado.set_active(False)
            marcado.set_sensitive(False)
        else:   # Por defecto "de que sí".
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
        if (not self.usuario
            or self.usuario.get_permiso(
                pclases.Ventana.select(
                    pclases.Ventana.q.fichero
                        == "listado_rollos.py")[0]).escritura): # OJO: HARCODED
            tvrollos = self.wids['tv_rollos']
            model, paths = tvrollos.get_selection().get_selected_rows()
            rollos_por_defecto = []
            solo_rollos_b = True
            for path in paths:
                codigo_rollo = model[path][0]
                rollos_por_defecto.append(codigo_rollo)
                if codigo_rollo.startswith("R"):
                    solo_rollos_b = False
            rollos_por_defecto.sort()
            rollos_por_defecto = ', '.join(rollos_por_defecto)
            from formularios import reports
            entrada, mostrar_marcado = self._dialogo_entrada(
                    titulo='ETIQUETAS',
                    texto="Introduzca los números de rollo, separados por "
                          "coma, que desea etiquetar:",
                    valor_por_defecto=rollos_por_defecto,
                    padre=self.wids['ventana'],
                    marcado_disabled=solo_rollos_b)
            if entrada != None:
                codigos = [cod.strip() for cod in entrada.split(",")]
                temp = []
                for codigo in codigos:
                    if codigo.upper().startswith("R"):
                        try:
                            temp.append(pclases.Rollo.select(
                                pclases.Rollo.q.codigo == codigo.upper())[0])
                        except Exception, msg:
                            self.logger.error(
                                "listado_rollos::etiquetar -> %s" % (msg))
                    elif codigo.upper().startswith("X"):
                        try:
                            temp.append(pclases.RolloDefectuoso.select(
                                pclases.RolloDefectuoso.q.codigo
                                    == codigo.upper())[0])
                        except Exception, msg:
                            self.logger.error(
                                "listado_rollos::etiquetar -> %s" % (msg))
                    elif codigo.upper().startswith("Y"):
                        try:
                            temp.append(pclases.RolloC.select(
                                pclases.RolloC.q.codigo == codigo.upper())[0])
                        except Exception, msg:
                            self.logger.error(
                                "listado_rollos::etiquetar -> %s" % (msg))
                    else:
                        # No lo encuentro, paso de dar un mensaje de error.
                        pass
                rollos = []
                rollosc = []
                for r in temp:
                    fetiqueta = None
                    if isinstance(r, pclases.RolloC):
                        rollosc.append(r)
                    else:
                        elemento, fetiqueta = build_etiqueta(r)
                        rollos.append(elemento)
                    pclases.Auditoria.modificado(r, self.usuario, __file__,
                      "Impresión de etiqueta para rollo %s" % r.get_info())
                    if rollos:
                        reports.abrir_pdf(
                            geninformes.etiquetasRollosEtiquetadora(
                                rollos,
                                mostrar_marcado,
                                fetiqueta)) # Etiquetas térmicas pequeñas.
                    if rollosc:
                        data = preparar_datos_etiquetas_rollos_c(rollosc)
                        if data:
                            reports.abrir_pdf(
                                geninformes.etiquetasRollosCEtiquetadora(data))
        else:
            utils.dialogo_info(titulo="USUARIO SIN PRIVILEGIOS",
                    texto="Para poder crear etiquetas de rollos existentes es"
                          " necesario\nque tenga permiso de escritura sobre "
                          "la ventana actual.",
                    padre=self.wids['ventana'])

def preparar_datos_etiquetas_rollos_c(rollos):
    """
    Recibe una lista de objetos rolloC y devuelve una lista de
    diccionarios con los datos que lleva una etiqueta de rollos
    de geotextiles C: básicamente número, código y peso.
    """
    data = []
    for rollo in rollos:
        pv = rollo.productoVenta
        r = {'descripción': pv.descripcion,
             'codigoBarra': pv.codigo,
             'codigo': rollo.codigo,
             'peso': utils.float2str(rollo.peso, autodec = True)
            }
        data.append(r)
    return data

if __name__ == '__main__':
    t = ListadoRollos()

