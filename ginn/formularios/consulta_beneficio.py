#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado                    #
#                          (pacoqueen@users.sourceforge.net)                  #
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
## consulta_beneficio.py - sum((PVP - IVA) * porcentaje_tarifa)
###################################################################
## NOTAS:
##  - No cuenta tickets de caja ni prefacturas.
###################################################################
## Changelog:
## 
###################################################################
## 
###################################################################
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sqlobject
import sys, os
try:
    import pclases
except ImportError:
    sys.path.append(os.path.join('..', 'framework'))
    import pclases
import mx.DateTime
try:
    import geninformes
except ImportError:
    sys.path.append(os.path.join('..', 'informes'))
    import geninformes
try:
    from treeview2pdf import treeview2pdf
except ImportError:
    sys.path.append(os.path.join("..", "informes"))
    from treeview2pdf import treeview2pdf
try:
    from treeview2csv import treeview2csv
except ImportError:
    sys.path.append(os.path.join("..", "informes"))
    from treeview2pdf import treeview2pdf
from informes import abrir_pdf, abrir_csv
import ventana_progreso

class ConsultaBeneficio(Ventana):
    def __init__(self, objeto = None, usuario = None):
        Ventana.__init__(self, 'consulta_beneficio.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_exportar/clicked': self.exportar,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin}
        self.add_connections(connections)
        cols = (('Fecha','gobject.TYPE_STRING', False, True, False, None),
                ('Nº Factura','gobject.TYPE_STRING', False, True, True, None),
                ('Cliente','gobject.TYPE_STRING', False, True, False, None),
                ('Importe','gobject.TYPE_STRING', False, True, False, None),
                ('Base imponible','gobject.TYPE_STRING', False, True, False, None),
                ('Beneficio sobre tarifa','gobject.TYPE_STRING', False, True, False, None),
                ('Idfactura','gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        for col in self.wids['tv_datos'].get_columns()[0:2] + self.wids['tv_datos'].get_columns()[3:]:
            for cell in col.get_cell_renderers():
                cell.set_property("xalign", 1.0)
            col.set_alignment(0.5)
        self.fin = mx.DateTime.localtime()
        self.inicio = mx.DateTime.DateTimeFrom(day = 1, month = self.fin.month, year = self.fin.year)
        self.wids['e_fechafin'].set_text(utils.str_fecha(self.fin))
        self.wids['e_fechainicio'].set_text(utils.str_fecha(self.inicio))
        gtk.main()

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, facturas):
        """
        Rellena el model con los items de la consulta
        """        
        model = self.wids['tv_datos'].get_model()
        model.clear()
        totfact = totsiniva = totbeneficio = 0.0
        self.wids['tv_datos'].freeze_child_notify()
        self.wids['tv_datos'].set_model(None)
        for f in facturas:
            total = f.calcular_total()
            iva = f.calcular_total_iva()
            irpf = f.calcular_total_irpf()
            siniva = total - iva - irpf
            beneficio = f.calcular_beneficio()
            totfact += total
            totsiniva += siniva
            totbeneficio += beneficio
            padre = model.append(None, (utils.str_fecha(f.fecha), 
                                       f.numfactura, 
                                       f.cliente and f.cliente.nombre or "", 
                                       utils.float2str(total), 
                                       utils.float2str(siniva), 
                                       utils.float2str(beneficio), 
                                       f.id))
            for srv in f.servicios:
                model.append(padre, (utils.float2str(srv.cantidad, autodec = True), 
                                     utils.float2str(srv.precio), 
                                     srv.concepto, 
                                     utils.float2str(srv.calcular_subtotal() * (1 + f.iva)), 
                                     utils.float2str(srv.calcular_subtotal()), 
                                     utils.float2str(srv.calcular_beneficio()), 
                                     srv.id))
            for ldv in f.lineasDeVenta:
                model.append(padre, (utils.float2str(ldv.cantidad, autodec = True), 
                                     utils.float2str(ldv.precio), 
                                     ldv.producto.descripcion, 
                                     utils.float2str(ldv.calcular_subtotal() * (1 + f.iva)), 
                                     utils.float2str(ldv.calcular_subtotal()), 
                                     utils.float2str(ldv.calcular_beneficio()), 
                                     ldv.id))
        self.rellenar_totales(totfact, totsiniva, totbeneficio)
        self.wids['tv_datos'].set_model(model)
        self.wids['tv_datos'].thaw_child_notify()

    def rellenar_totales(self, totf, tots, totb):
        """
        Introduce los totales en los "entries".
        """
        self.wids['e_total'].set_text(utils.float2str(totf))
        self.wids['e_siniva'].set_text(utils.float2str(tots))
        try:
            beneficio = totb * 100.0 / tots
        except ZeroDivisionError:
            beneficio = 0
        self.wids['e_beneficio'].set_text("%s (%s %%)" % (utils.float2str(totb), utils.float2str(beneficio, 4, autodec = True)))

    def set_inicio(self, boton):
        temp = utils.mostrar_calendario(fecha_defecto = self.inicio, padre = self.wids['ventana'])
        self.inicio = mx.DateTime.DateTimeFrom(day = temp[0], month = temp[1], year = temp[2])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(self.inicio))

    def set_fin(self, boton):
        temp = utils.mostrar_calendario(fecha_defecto = self.fin, padre = self.wids['ventana'])
        self.fin = temp
        self.fin = mx.DateTime.DateTimeFrom(day = temp[0], month = temp[1], year = temp[2])
        self.wids['e_fechafin'].set_text(utils.str_fecha(self.fin))

    def buscar(self,boton):
        """
        Dadas fecha de inicio y de fin, lista todos los albaranes
        pendientes de facturar.
        """
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        self.resultado = []
        facturas = pclases.FacturaVenta.select(pclases.AND(pclases.FacturaVenta.q.fecha >= self.inicio, 
                                                           pclases.FacturaVenta.q.fecha <= self.fin))
        act = 0.0; tot = facturas.count()
        for f in facturas:
            vpro.set_valor(act/tot, "Calculando beneficio factura %s..." % (f.numfactura))
            self.resultado.append(f)
        self.resultado.sort(lambda f1, f2: utils.orden_por_campo_o_id(f1, f2, "fecha"))
        self.rellenar_tabla(self.resultado)
        vpro.ocultar()

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe.
        """
        resp = utils.dialogo(titulo = "¿IMPRIMIR DESGLOSE?", 
                             texto = "Puede imprimir un resumen o todo el contenido de la consulta\n¿Desea imprimir toda la información desglosada?", 
                             padre = self.wids['ventana'])
        if resp:
            tv = self.wids['tv_datos']
            tv.expand_all()
            while gtk.events_pending(): gtk.main_iteration(False)
        else:
            tv = self.wids['tv_datos']
            tv.collapse_all()
            while gtk.events_pending(): gtk.main_iteration(False)
            from consulta_ventas_por_producto import convertir_a_listview
            tv = convertir_a_listview(tv)
        strfecha = "De %s a %s" % (self.wids['e_fechainicio'].get_text(), self.wids['e_fechafin'].get_text())
        abrir_pdf(treeview2pdf(tv, titulo = "Beneficio sobre tarifa", fecha = strfecha))

    def exportar(self, boton):
        """
        Exporta el TreeView a CSV.
        """
        abrir_csv(treeview2csv(self.wids['tv_datos']))


if __name__ == '__main__':
    t = ConsultaBeneficio()

