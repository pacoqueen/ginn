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
## consulta_pedidos_clientes.py --
###################################################################
## NOTAS:
##
###################################################################
## Changelog:
## 4 de abril de 2006 -> Inicio
##
###################################################################

"""
Consulta con los pedidos realizados por un cliente entre fechas.
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

# TODO: Añadir un Gtk.CairoPlot para ver los totales por producto. Para eso 
# antes tendré que adaptar la clase a cagraph o usar los parámetros de 
# cairoplot para, al menos, mostrar los valores.

class ConsultaPedidosCliente(Ventana):
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
        Ventana.__init__(self, 'consulta_pedidos_clientes.glade', objeto,
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
        utils.rellenar_lista(self.wids['cmbe_cliente'],
                [(c.id, c.nombre)
                    for c in pclases.Cliente.select(orderBy='nombre')])
        cols = (('Cliente', 'gobject.TYPE_STRING', False, True, False, None),
                ('Fecha', 'gobject.TYPE_STRING', False, True, False, None),
                ('Pedido', 'gobject.TYPE_STRING', False, True, False, None),
                ('Producto', 'gobject.TYPE_STRING', False, True, False, None),
                ('Cantidad\npedida', 'gobject.TYPE_STRING',
                                                    False, True, False, None),
                ('Cantidad\nservida', 'gobject.TYPE_STRING',
                                                    False, True, False, None),
                ('Importe\npedido\n(c/IVA)', 'gobject.TYPE_STRING',
                                                    False, True, False, None),
                ('Importe\nservido\n(c/IVA)', 'gobject.TYPE_STRING',
                                                    False, True, False, None),
                ("Bloqueado", "gobject.TYPE_BOOLEAN", False, True, False, None),
                ("Cerrado", "gobject.TYPE_BOOLEAN", False, True, False, None),
                ('Idpedido', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_datos'], cols)
        for ncol in (4, 5, 6, 7):
            col = self.wids['tv_datos'].get_column(ncol)
            for cell in col.get_cell_renderers():
                cell.set_property("xalign", 1)
        self.wids['tv_datos'].connect("row-activated", self.abrir_pedido)
        self.resultado = []
        self.fin = utils.str_fecha(datetime.date.today())
        self.inicio = None
        self.wids['e_fecha_fin'].set_text(self.fin)
        self.wids['e_fecha_inicio'].set_text("")
        if objeto != None:
            utils.combo_set_from_db(self.wids["cmbe_cliente"], objeto.id)
            self.wids["b_buscar"].clicked()
        self.add_widgets_extra()
        gtk.main()

    def add_widgets_extra(self):
        """
        No tengo glade-gtk2 en prometheus. Too old for rock'n roll but too 
        youg to die.
        """
        self.wids['e_total_servido'] = gtk.Entry()
        self.wids['e_total_servido'].set_property("editable", False)
        self.wids['e_total_servido'].set_property("has-frame", False)
        lab_total_servido = gtk.Label("Importe total servido:")
        self.wids['e_total'].parent.pack_start(lab_total_servido)
        self.wids['e_total'].parent.pack_start(self.wids['e_total_servido'])
        self.wids['e_total'].parent.show_all()

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        tv = self.wids['tv_datos']
        abrir_csv(treeview2csv(tv))

    def abrir_pedido(self, tv, path, column):
        """
        Abre el pedido al que se le ha hecho doble clic en una ventana nueva.
        """
        model = tv.get_model()
        idpedido = model[path][-1]
        try:
            pedido = pclases.PedidoVenta.get(idpedido)
        except Exception, e:
            utils.dialogo_info(titulo = "ERROR RECUPERANDO PEDIDO",
                               texto = "El pedido ID %d no se ha encontrado."
                               "\n\n"
                               "Compruebe que no haya sido eliminado recargando"
                               " la consulta y vuelva a intentarlo."
                               "\n\n\n"
                               "Información de depuración:"
                               "\n%s" % (idpedido, e),
                               padre = self.wids['ventana'])
        else:
            from formularios import pedidos_de_venta
            ventanapedido = pedidos_de_venta.PedidosDeVenta(objeto = pedido,
                                                        usuario = self.usuario)

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, pedidos):
        """
        Rellena el model con los pedidos de la consulta.
        """
        from formularios.ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        tot = pedidos.count()
        vpro.mostrar()
        model = self.wids['tv_datos'].get_model()
        model.clear()
        total = 0.0
        importetotal = 0.0
        importetotal_servido = 0.0
        for p in pedidos:
            vpro.set_valor(total / tot, "Buscando productos en pedidos..."
                                        "\n(ignorando servicios) [%d/%d]" % (
                                            total, tot))
            total += 1
            prods = p.get_pendiente_servir()[0] # Devuelve 3 cosas.
            for producto in prods:
                importe_ldp = sum([ldp.calcular_subtotal(iva = True) 
                                    for ldp in p.lineasDePedido 
                                    if ldp.producto == producto])
                importe_ldv = sum([ldv.calcular_subtotal(iva = True) 
                                    for ldv in p.lineasDeVenta
                                    if ldv.albaranSalida 
                                        and ldv.producto == producto])
                importetotal += importe_ldp
                importetotal_servido += importe_ldv
                cantidad_ldp = prods[producto]['pedido']
                cantidad_ldv = prods[producto]['servido']
                model.append((p.cliente.nombre,
                              utils.str_fecha(p.fecha),
                              p.numpedido,
                              producto.descripcion,
                              utils.float2str(cantidad_ldp),
                              utils.float2str(cantidad_ldv),
                              utils.float2str(importe_ldp),
                              utils.float2str(importe_ldv),
                              p.bloqueado,
                              p.cerrado,
                              p.id))
        vpro.ocultar()
        self.wids['e_total'].set_text("%d " % total)
        self.wids['e_importe_total'].set_text(
                "%s €" % (utils.float2str(importetotal)))
        self.wids['e_total_servido'].set_text(
                "%s €" % (utils.float2str(importetotal_servido)))

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
        Dadas fecha de inicio y de fin, busca todos los pedidos del
        cliente del combo.
        """
        idcliente = utils.combo_get_value(self.wids['cmbe_cliente'])
        if idcliente == None:
            utils.dialogo_info(titulo = 'ERROR',
                               texto = 'Seleccione un cliente',
                               padre = self.wids['ventana'])
        else:
            idcliente = utils.combo_get_value(self.wids['cmbe_cliente'])
            self.cliente = pclases.Cliente.get(idcliente)
            cliente = self.cliente
            str_fini = self.wids['e_fecha_inicio'].get_text()
            if str_fini:
                self.inicio = utils.parse_fecha(str_fini)
            else:
                self.inicio = None
            str_ffin = self.wids['e_fecha_fin'].get_text()
            self.fin = utils.parse_fecha(str_ffin)
            if not self.inicio:
                pedidos = pclases.PedidoVenta.select(pclases.AND(
                                pclases.PedidoVenta.q.fecha <= self.fin,
                                pclases.PedidoVenta.q.clienteID == cliente.id),
                            orderBy = 'fecha')
            else:
                pedidos = pclases.PedidoVenta.select(pclases.AND(
                                pclases.PedidoVenta.q.fecha >= self.inicio,
                                pclases.PedidoVenta.q.fecha <= self.fin,
                                pclases.PedidoVenta.q.clienteID == cliente.id),
                            orderBy='fecha')
            self.resultado = pedidos
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
                               titulo = "Pedidos por cliente", 
                               fecha = fecha_informe, 
                               numcols_a_totalizar = [6, 7]))


if __name__ == '__main__':
    ConsultaPedidosCliente()

