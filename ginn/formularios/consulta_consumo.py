#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2014 Francisco José Rodríguez Bogado,                    #
#                         Diego Muñoz Escalante.                              #
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
## consulta_consumo.py --
###################################################################
## NOTAS:
##
###################################################################
## Changelog:
##
###################################################################


import pygtk
pygtk.require('2.0')
from framework import pclases
from formularios import ventana_progreso
from formularios.ventana import Ventana
from formularios import utils
#from formularios.consulta_ventas_por_producto import act_fecha
from informes import geninformes
import gtk
import time
import mx.DateTime


class ConsultaConsumo(Ventana):
    inicio = None
    fin = None
    resultado = []

    def __init__(self, objeto=None, usuario=None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        global fin
        Ventana.__init__(self, 'consulta_consumo.glade', objeto,
                         usuario=usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin,
                       'e_fechainicio/focus-out-event': utils.act_fechahora,
                       'e_fechafin/focus-out-event': utils.act_fechahora,
                       "b_exportar/clicked": self.exportar}
        self.add_connections(connections)
        cols = (('Producto', 'gobject.TYPE_STRING', False, True, False, None),
                ('Cantidad consumida', 'gobject.TYPE_STRING',
                 False, True, False, None),
                ('A', 'gobject.TYPE_STRING',
                 False, True, False, None),
                ('B', 'gobject.TYPE_STRING',
                 False, True, False, None),
                ('C', 'gobject.TYPE_STRING',
                 False, True, False, None),
                ('Media diaria', 'gobject.TYPE_STRING',
                 False, True, False, None),
                ('ID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        for ncol in range(1, 4):
            self.wids['tv_datos'].get_column(ncol).get_cell_renderers()[0].set_property("xalign", 1)
        self.fin = mx.DateTime.today() + mx.DateTime.TimeDelta(hours = 6)
        self.wids['e_fechafin'].set_text(utils.str_fechahora(self.fin))
        self.wids['e_fechainicio'].set_text(
            utils.str_fechahora(self.fin - (7 * mx.DateTime.oneDay)))
        self.inicio = utils.parse_fechahora(self.wids['e_fechainicio'].get_text())
        # self.wids['ch_fibra'].set_active(True)
        self.wids['ch_geotextiles'].set_active(True)
        gtk.main()

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        tv = self.wids['tv_datos']
        abrir_csv(treeview2csv(tv))

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, items):
        """
        Rellena el model con los items de la consulta.
        "items" es una lista de 5 elementos: Nombre producto, cantidad, ID, X
        y media diaria.
        En la última columna del model (la oculta) se guarda un string "ID:X"
        donde X es C si es un producto de compra o V si es de venta (fibra
        fabricada usada como materia prima).
        """
        model = self.wids['tv_datos'].get_model()
        model.clear()
        for item in items:
            model.append(None, (item[0],
                                item[1],
                                item[2],
                                item[3],
                                item[4],
                                item[8],
                                "%d:%s" % (item[5], item[6])))
        # : Es un TreeView, ya añadiré si se necesita información adicional en
        # los hijos. Usaré el evento "row-expanded" para no retrasar más la
        # carga inicial de datos de cada consulta.
        #   (Ver trazabilidad.py como ejemplo.)

    def set_inicio(self, boton):
        temp = utils.mostrar_calendario(
            fecha_defecto=utils.parse_fechahora(
                self.wids['e_fechainicio'].get_text()),
            padre=self.wids['ventana'])
        temp = mx.DateTime.DateFrom(day=temp[0], month=temp[1], year=temp[2]) + mx.DateTime.TimeDelta(hours = 6)
        self.wids['e_fechainicio'].set_text(utils.str_fechahora(temp))

    def set_fin(self, boton):
        temp = utils.mostrar_calendario(
            fecha_defecto=utils.parse_fechahora(
                self.wids['e_fechafin'].get_text()),
            padre=self.wids['ventana'])
        temp = mx.DateTime.DateFrom(day=temp[0], month=temp[1], year=temp[2]) + mx.DateTime.TimeDelta(hours = 6)
        self.wids['e_fechafin'].set_text(utils.str_fechahora(temp))

    def por_fecha(self, e1, e2):
        """
        Permite ordenar una lista de albaranes por fecha
        """
        if e1.fecha < e2.fecha:
            return -1
        elif e1.fecha > e2.fecha:
            return 1
        else:
            return 0

    def get_lineas_produccion(self):
        linea = pclases.LineaDeProduccion.select(
            pclases.LineaDeProduccion.q.nombre.contains('geotextil'))
        if linea.count() == 0:
            linea_gtx = None
        else:
            linea_gtx = linea[0]
        linea = pclases.LineaDeProduccion.select(
            pclases.LineaDeProduccion.q.nombre.contains('fibra'))
        if linea.count() == 0:
            linea_fib = None
        else:
            linea_fib = linea[0]
        return linea_gtx, linea_fib

    def buscar(self, boton):
        """
        Dadas fecha de inicio y de fin, busca los productos y
        materia prima consumida en los partes de producción.
        """
        try:
            fechainicio = self.inicio = utils.parse_fechahora(
                self.wids['e_fechainicio'].get_text())
        except ValueError:
            fechainicio = self.inicio = None
        try:
            fechafin = self.fin = utils.parse_fechahora(
                self.wids['e_fechafin'].get_text())
        except ValueError:
            fechafin = self.fin = mx.DateTime.today()
        PDP = pclases.ParteDeProduccion
        if not self.inicio:
            pdps = PDP.select(PDP.q.fechahorainicio < self.fin,
                              orderBy='fecha')
        else:
            pdps = PDP.select(pclases.AND(PDP.q.fechahorainicio >= self.inicio,
                                          PDP.q.fechahorainicio < self.fin),
                              orderBy='fecha')
        try:
            dias = ((fechafin - fechainicio) + mx.DateTime.oneDay).days
        except TypeError:   # Alguna de las fechas es None. Uso los partes
            dias = ((pdps[-1].fecha - pdps[0].fecha) + mx.DateTime.oneDay).days
        vpro = ventana_progreso.VentanaProgreso(padre=self.wids['ventana'])
        tot = pdps.count()
        i = 0.0
        vpro.mostrar()
        linea_gtx, linea_fib = self.get_lineas_produccion()  # @UnusedVariable
        cons_balas = {}
        cons_rollos = {}
        cons_cemento = {}
        partidas_contadas = []
        balas_contadas = []
        for pdp in pdps:
            vpro.set_valor(i / tot, 'Analizando partes %s...' % (
                utils.str_fecha(pdp.fecha)))
            if (pdp.es_de_balas() and
                    self.wids['ch_fibra'].get_active()):
                # Añado consumos de material adicional y materia prima (ambos
                # son ProductoCompra).
                for c in pdp.consumos:
                    key = "%d:C" % (c.productoCompraID)
                    if key not in cons_balas:
                        cons_balas[key] = [c.productoCompra.descripcion,
                                           c.cantidad,
                                           'N/A',
                                           'N/A',
                                           'N/A',
                                           c.productoCompra.id,
                                           'C',
                                           c.productoCompra.unidad]
                    else:
                        cons_balas[key][1] += c.cantidad
            elif (pdp.es_de_bolsas()
                  and self.wids['ch_embolsado'].get_active()):
                # Consume materiales (productos de compra).
                for c in pdp.consumos:
                    key = "%d:C" % (c.productoCompraID)
                    if key not in cons_cemento:
                        cons_cemento[key] = [c.productoCompra.descripcion,
                                             c.cantidad,
                                             'N/A',
                                             'N/A',
                                             'N/A',
                                             c.productoCompra.id,
                                             'C',
                                             c.productoCompra.unidad]
                    else:
                        cons_cemento[key][1] += c.cantidad
                # Y también consume fibra en bigbags:
                for bb in pdp.bigbags:
                    clase_a = bb.articulo.es_clase_a()
                    clase_b = bb.articulo.es_clase_b()
                    clase_c = bb.articulo.es_clase_c()
                    productoVenta = bb.articulo.productoVenta
                    key = "%d:V" % (productoVenta.id)
                    peso_sin = bb.articulo.peso_sin
                    if key not in cons_cemento:
                        cons_cemento[key] = [
                            bb.articulo.productoVenta.descripcion,
                            peso_sin,
                            clase_a and peso_sin or 0.0,
                            clase_b and peso_sin or 0.0,
                            clase_c and peso_sin or 0.0,
                            bb.articulo.productoVenta.id,
                            'V',
                            "kg"]
                    else:
                        cons_cemento[key][1] += peso_sin
                        if clase_a:
                            cons_cemento[key][2] += peso_sin
                        elif clase_b:
                            cons_cemento[key][3] += peso_sin
                        elif clase_c:
                            cons_cemento[key][4] += peso_sin
            elif (pdp.es_de_rollos() and
                  self.wids['ch_geotextiles'].get_active()):
                # Añado consumos de material adicional (ProductoCompra).
                for c in pdp.consumos:
                    key = "%d:C" % (c.productoCompraID)
                    if key not in cons_rollos:
                        cons_rollos[key] = [c.productoCompra.descripcion,
                                            c.cantidad,
                                            'N/A',
                                            'N/A',
                                            'N/A',
                                            c.productoCompra.id,
                                            'C',
                                            c.productoCompra.unidad]
                    else:
                        cons_rollos[key][1] += c.cantidad
                # Y el consumo de materia prima (ProductoVenta). Se hace por
                # PARTIDAS, ya que  los partes comparten materia prima de
                # fibra si son de la misma partida.
                if pdp.articulos != []:
                    if pdp.articulos[0].es_rollo():
                        partida = pdp.articulos[0].rollo.partida
                    elif pdp.articulos[0].es_rollo_defectuoso():
                        partida = pdp.articulos[0].rolloDefectuoso.partida
                    else:
                        partida = None
                    # Hay que evitar contar la misma partida dos veces.
                    if (partida is not None
                            and partida not in partidas_contadas
                            and partida.entra_en_cota_superior(fechafin)):
                        partidas_contadas.append(partida)
                        for bala in partida.balas:
                            if bala not in balas_contadas:  # Dos partidas
                                # pueden compartir partida de carga y por tanto
                                #  balas. Evito contar la misma dos veces.
                                balas_contadas.append(bala)
                                productoVenta = bala.articulos[0].productoVenta
                                key = "%d:V" % (productoVenta.id)
                                #peso_neto_bala = bala.pesobala
                                # En realidad es lo mismo. Pero así más claro:
                                peso_neto_bala = bala.articulo.peso_sin
                                clase_a = bala.articulo.es_clase_a()
                                clase_b = bala.articulo.es_clase_b()
                                clase_c = bala.articulo.es_clase_c()
                                if key not in cons_rollos:
                                    cons_rollos[key] = [
                                        productoVenta.descripcion,
                                        peso_neto_bala,
                                        clase_a and peso_neto_bala or 0.0,
                                        clase_b and peso_neto_bala or 0.0,
                                        clase_c and peso_neto_bala or 0.0,
                                        productoVenta.id,
                                        'V',
                                        'kg']
                                else:
                                    cons_rollos[key][1] += peso_neto_bala
                                    if clase_a:
                                        cons_rollos[key][2] += peso_neto_bala
                                    elif clase_b:
                                        cons_rollos[key][3] += peso_neto_bala
                                    elif clase_c:
                                        cons_rollos[key][4] += peso_neto_bala
            i += 1
        self.resultado = []
        for k in cons_balas:
            cantidad = "%s %s" % (utils.float2str(cons_balas[k][1], 3),
                                  cons_balas[k][7])
            media = "%s %s/día" % (utils.float2str(cons_balas[k][1] / dias),
                                   cons_balas[k][7])
            try:
                str_a = utils.float2str(cons_balas[k][2])
                str_b = utils.float2str(cons_balas[k][3])
                str_c = utils.float2str(cons_balas[k][4])
            except ValueError:
                str_a = str_b = str_c = cons_balas[k][2] # = 4 y a 5 = N/A
            self.resultado.append([cons_balas[k][0],
                                   cantidad,
                                   str_a,
                                   str_b,
                                   str_c,
                                   cons_balas[k][5],
                                   cons_balas[k][6],
                                   cons_balas[k][7],
                                   media])
        for k in cons_rollos:
            cantidad = "%s %s" % (utils.float2str(cons_rollos[k][1], 3),
                                  cons_rollos[k][7])
            media = "%s %s/día" % (utils.float2str(cons_rollos[k][1] / dias),
                                   cons_rollos[k][7])
            try:
                str_a = utils.float2str(cons_rollos[k][2])
                str_b = utils.float2str(cons_rollos[k][3])
                str_c = utils.float2str(cons_rollos[k][4])
            except ValueError:
                str_a = str_b = str_c = cons_rollos[k][3] # = 4 y a 5 = N/A
            self.resultado.append([cons_rollos[k][0],
                                   cantidad,
                                   str_a,
                                   str_b,
                                   str_c,
                                   cons_rollos[k][5],
                                   cons_rollos[k][6],
                                   cons_rollos[k][7],
                                   media])
        for k in cons_cemento:
            cantidad = "%s %s" % (utils.float2str(cons_cemento[k][1], 3),
                                  cons_cemento[k][7])
            media = "%s %s/día" % (utils.float2str(cons_cemento[k][1] / dias),
                                   cons_cemento[k][7])
            try:
                str_a = utils.float2str(cons_cemento[k][2])
                str_b = utils.float2str(cons_cemento[k][3])
                str_c = utils.float2str(cons_cemento[k][4])
            except ValueError:
                str_a = str_b = str_c = cons_cemento[k][3] # = 4 y a 5 = N/A
            self.resultado.append([cons_cemento[k][0],
                                   cantidad,
                                   str_a,
                                   str_b,
                                   str_c,
                                   cons_cemento[k][5],
                                   cons_cemento[k][6],
                                   cons_cemento[k][7],
                                   media])
        vpro.ocultar()
        self.rellenar_tabla(self.resultado)

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        from formularios import reports
        datos = []
        model = self.wids['tv_datos'].get_model()
        for i in xrange(len(model)):
            datos.append((model[i][0], model[i][1]))
        if not self.inicio:
            fechaInforme = 'Hasta ' + utils.str_fechahora(self.fin)
        else:
            fechaInforme = (utils.str_fechahora(self.inicio)
                            + ' - ' + utils.str_fechahora(self.fin))
        if datos != []:
            reports.abrir_pdf(geninformes.consumo_produccion(datos,
                                                             fechaInforme))


if __name__ == '__main__':
    t = ConsultaConsumo()
