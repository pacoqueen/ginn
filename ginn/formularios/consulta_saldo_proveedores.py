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
## consulta_saldo_proveedores.py --
###################################################################
## NOTAS:
##
###################################################################

"""
Consulta de proveedores con el volumen de compra facturada, pagado y pendiente.
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


class ConsultaPedidosProveedor(Ventana):
    """
    Clase que contiene la ventana y los resultados de la consulta.
    """
    def __init__(self, objeto=None, usuario=None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'consulta_saldo_proveedores.glade', objeto,
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
        utils.rellenar_lista(self.wids['cmbe_proveedor'],
                [(0, "Todos")] +
                [(c.id, c.nombre)
                    for c in pclases.Proveedor.select(orderBy='nombre')])
        cols = (('Proveedor', 'gobject.TYPE_STRING', False, True, False, None),
                ('Fecha', 'gobject.TYPE_STRING', False, True, False, None),
                ('Factura', 'gobject.TYPE_STRING', False, True, False, None),
                ('Importe', 'gobject.TYPE_STRING', False, True, False, None),
                ('Vencimientos', 'gobject.TYPE_STRING', False, True, False, None),
                ('Pagado', 'gobject.TYPE_STRING', False, True, False, None),
                ('Pendiente', 'gobject.TYPE_STRING', False, True, False, None),
                ('DBPUID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        for ncol in (3, 4, 5, 6):
            col = self.wids['tv_datos'].get_column(ncol)
            for cell in col.get_cell_renderers():
                cell.set_property("xalign", 1)
        self.wids['tv_datos'].connect("row-activated", self.abrir_objeto)
        self.resultado = []
        self.fin = utils.str_fecha(datetime.date.today())
        self.inicio = None
        self.wids['e_fecha_fin'].set_text(self.fin)
        self.wids['e_fecha_inicio'].set_text("")
        if objeto != None:
            utils.combo_set_from_db(self.wids["cmbe_proveedor"], objeto.id)
            self.wids["b_buscar"].clicked()
        self.wids['cmbe_proveedor'].grab_focus()
        gtk.main()

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        tv = self.wids['tv_datos']
        abrir_csv(treeview2csv(tv))

    def abrir_objeto(self, tv, path, column):
        """
        Abre el factura al que se le ha hecho doble clic en una ventana nueva.
        """
        model = tv.get_model()
        dbpuid = model[path][-1]
        objeto = pclases.getObjetoPUID(dbpuid)
        if isinstacen(objeto, pclases.Proveedor):
            from formularios import proveedores
            ventanaproveedor = proveedores.Proveedores(objeto = objeto,
                                                       usuario = self.usuario)
        else:
            from formularios import facturas_de_venta
            ventanafactura = facturas_de_venta.PedidosDeVenta(objeto = objeto,
                                                        usuario = self.usuario)

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, facturas):
        """
        Rellena el model con los facturas de la consulta.
        """
        from formularios.ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        tot = facturas.count()
        vpro.mostrar()
        model = self.wids['tv_datos'].get_model()
        model.clear()
        total = 0.0
        rows_proveedor = {}
        for fra in facturas:
            vpro.set_valor(total / tot,
                           "Recuperando facturas... [%d/%d]" % (total, tot))
            total += 1
            proveedor = fra.proveedor
            importe = fra.calcular_importe_total()
            vencimientos = sum([vto.importe for vto in fra.vencimientosPago])
            pagado = sum([c.importe for c in fra.pagos])
            pendiente = importe - pagado
            try:
                row_proveedor = rows_proveedor[proveedor.puid]
            except KeyError:
                rows_proveedor[proveedor.puid] = row_proveedor = model.append(
                        None, (proveedor.nombre,
                               "",
                               "",
                               "0",
                               "0",
                               "0",
                               "0",
                               proveedor.puid))
            model.append(row_proveedor, ("",
                                         fra.numfactura,
                                         utils.str_fecha(fra.fecha),
                                         utils.float2str(importe),
                                         utils.float2str(vencimientos),
                                         utils.float2str(pagado),
                                         utils.float2str(pendiente),
                                         fra.puid))
            model[row_proveedor][3] = utils.float2str(
                    utils._float(model[row_proveedor][3]) + importe)
            model[row_proveedor][4] = utils.float2str(
                    utils._float(model[row_proveedor][4]) + vencimientos)
            model[row_proveedor][5] = utils.float2str(
                    utils._float(model[row_proveedor][5]) + pagado)
            model[row_proveedor][6] = utils.float2str(
                    utils._float(model[row_proveedor][6]) + pendiente)
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
        Dadas fecha de inicio y de fin, busca todos los facturas del
        proveedor del combo.
        """
        idproveedor = utils.combo_get_value(self.wids['cmbe_proveedor'])
        str_fini = self.wids['e_fecha_inicio'].get_text()
        criterios = []
        if str_fini:
            self.inicio = utils.parse_fecha(str_fini)
            criterios.append(pclases.FacturaCompra.q.fecha >= self.inicio)
        else:
            self.inicio = None
        try:
            str_ffin = self.wids['e_fecha_fin'].get_text()
            self.fin = utils.parse_fecha(str_ffin)
        except (ValueError, TypeError):
            self.fin = datetime.date.today()
            str_ffin = utils.str_fecha(self.fin)
            self.wids['e_fecha_fin'].set_text(str_ffin)
        criterios.append(pclases.FacturaVenta.q.fecha <= self.fin)
        if idproveedor == None:
            proveedor = None
        elif idproveedor == 0:
            proveedor = None
        else:
            idproveedor = utils.combo_get_value(self.wids['cmbe_proveedor'])
            self.proveedor = pclases.Proveedor.get(idproveedor)
            proveedor = self.proveedor
            criterios.append(
                    pclases.FacturaCompra.q.proveedorID == proveedor.id)
        facturas = pclases.FacturaCompra.select(pclases.AND(*criterios))
        self.resultado = facturas
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
                               titulo = "Consulta saldo proveedor",
                               fecha = fecha_informe,
                               numcols_a_totalizar = [3, 4, 5, 6]))


if __name__ == '__main__':
    ConsultaPedidosProveedor()

