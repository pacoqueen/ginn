#!/usr/bin/env python.DateTime
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
## consulta_pedidos_clientes.py --
###################################################################
## NOTAS:
##
###################################################################
## Changelog:
## 4 de abril de 2006 -> Inicio
##
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sqlobject
from framework import pclases
import mx.DateTime
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes


class ConsultaPedidosCliente(Ventana):
    inicio = None
    fin = None
    cliente = None
    resultado = []

    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        global fin
        Ventana.__init__(self, 'consulta_pedidos_clientes.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin,
                       'b_exportar/clicked': self.exportar}
        self.add_connections(connections)
        utils.rellenar_lista(self.wids['cmbe_cliente'], [(c.id, c.nombre) for c in pclases.Cliente.select(orderBy='nombre')])
        cols = (('Cliente', 'gobject.TYPE_STRING', False, True, False, None),
                ('Fecha', 'gobject.TYPE_STRING', False, True, False, None),
                ('Pedido', 'gobject.TYPE_STRING', False, True, False, None),
                ('Importe', 'gobject.TYPE_STRING', False, True, False, None),
                ("Bloqueado", "gobject.TYPE_BOOLEAN", False, True, False, None),
                ("Cerrado", "gobject.TYPE_BOOLEAN", False, True, False, None),
                ('Idpedido', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_datos'], cols)
        col = self.wids['tv_datos'].get_column(3)
        for cell in col.get_cell_renderers():
            cell.set_property("xalign", 1)
        self.wids['tv_datos'].connect("row-activated", self.abrir_pedido)
        temp = time.localtime()
        self.fin = str(temp[0])+'/'+str(temp[1])+'/'+str(temp[2])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        if objeto != None:
            utils.combo_set_from_db(self.wids["cmbe_cliente"], objeto.id)
            self.wids["b_buscar"].clicked()
        gtk.main()

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        import sys, os
        sys.path.append(os.path.join("..", "informes"))
        from treeview2csv import treeview2csv
        from informes import abrir_csv
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
            import pedidos_de_venta
            ventanapedido = pedidos_de_venta.PedidosDeVenta(objeto = pedido,
                                                        usuario = self.usuario)

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, items):
        """
        Rellena el model con los items de la consulta
        """
        model = self.wids['tv_datos'].get_model()
        model.clear()
        total = 0
        importetotal = 0.0
        for i in items:
            total += 1
            importe = i.calcular_importe_total()
            importetotal += importe
            model.append((i.cliente.nombre,
                          utils.str_fecha(i.fecha),
                          i.numpedido,
                          "%s €" % (utils.float2str(importe)),
                          i.bloqueado,
                          i.cerrado,
                          i.id))
        self.wids['e_total'].set_text("%d " % total)
        self.wids['e_importe_total'].set_text("%s €" % (utils.float2str(importetotal)))

    def set_inicio(self, boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
        self.inicio = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])

    def set_fin(self, boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.fin = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])

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


    def buscar(self, boton):
        """
        Dadas fecha de inicio y de fin, lista todos los albaranes
        pendientes de facturar.
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
        import informes
        datos = []
        for i in self.resultado:
            datos.append((i.cliente.nombre,
                          utils.str_fecha(i.fecha),
                          i.numpedido,
                          "%s €" % (utils.float2str(i.calcular_importe_total())),
                          i.bloqueado and "Sí" or "No",
                          i.cerrado and "Sí" or "No"))
        datos.append(("", "", "", "---", "", ""))
        datos.append(("%s pedidos listados." % (self.wids['e_total'].get_text()),
                      "",
                      "Importe total:",
                      self.wids['e_importe_total'].get_text(),
                      "",
                      ""))
        if (self.inicio) == None:
            fechaInforme = 'Hasta ' + utils.str_fecha(time.strptime(self.fin, "%Y/%m/%d"))
        else:
            fechaInforme = utils.str_fecha(time.strptime(self.inicio, "%Y/%m/%d")) + ' - ' + utils.str_fecha(time.strptime(self.fin, "%Y/%m/%d"))

        if datos != []:
            informes.abrir_pdf(geninformes.pedidosCliente(datos, self.cliente and self.cliente.nombre or "?", fechaInforme))




if __name__ == '__main__':
    t = ConsultaPedidosCliente()

