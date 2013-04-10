#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado,                   #
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
## consulta_libro_iva.py 
###################################################################
## NOTAS:
##  Listado de facturas entre fechas con B.I, IVA y total.
##  Similar a iva.py, pero con otro formato por petición de un 
##  cliente.
###################################################################
## Changelog:
## 
###################################################################
## TODO:
##  Meter otra pestaña para las facturas de compra.
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade
from framework import pclases
import mx, mx.DateTime
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes

class ConsultaLibroIVA(Ventana):

    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'consulta_facturas_sin_doc_pago.glade', 
                         objeto)
        self.wids['ventana'].set_title("LIBRO DE FACTURAS")
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_exportar/clicked': self.exportar, 
                       'b_fechaini/clicked': self.set_fecha_ini, 
                       'b_fechafin/clicked': self.set_fecha_fin}
        self.add_connections(connections)
        cols = [('Nº. Factura', 'gobject.TYPE_STRING', False, True, True, None),
                ('Fecha factura', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('CIF', 'gobject.TYPE_STRING', False, True, False, None),
                ('Cliente', 'gobject.TYPE_STRING', False, True, False, None),
                ('Base imponible', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('IVA', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ("Importe de la factura", "gobject.TYPE_STRING", 
                    False, True, False, None), 
                ('puid', 'gobject.TYPE_STRING', False, False, False, None)]
        utils.preparar_listview(self.wids['tv_datos'], cols)
        self.wids['tv_datos'].connect("row-activated", self.abrir_factura)
        tv = self.wids['tv_datos']
        tv.get_column(4).get_cell_renderers()[0].set_property('xalign', 1) 
        tv.get_column(5).get_cell_renderers()[0].set_property('xalign', 1) 
        tv.get_column(6).get_cell_renderers()[0].set_property('xalign', 1) 
        self.wids['e_fechaini'].set_text("")
        self.wids['e_fechafin'].set_text(
            utils.str_fecha(mx.DateTime.localtime()))
        gtk.main()

    def set_fecha_ini(self, boton):
        utils.set_fecha(self.wids['e_fechaini'])

    def set_fecha_fin(self, boton):
        utils.set_fecha(self.wids['e_fechafin'])

    def abrir_factura(self, tv, path, view_column):
        """
        Abre la factura a la que pertenece el vencimiento sobre el que se ha 
        hecho doble clic.
        """
        model = tv.get_model()
        puid = model[path][-1]
        fra = pclases.getObjetoPUID(puid)
        if isinstance(fra, pclases.FacturaVenta):
            import facturas_venta
            v = facturas_venta.FacturasVenta(fra, usuario = self.usuario)
        elif isinstance(fra. pclases.FacturaDeAbono):
            a = fra.abono
            import abonos_venta
            v = abonos_venta.AbonosVenta(a, usuario = self.usuario)

    def chequear_cambios(self):
        pass

    def buscar(self, boton):
        """
        Busca todos los productos e introduce en los TreeViews las existencias 
        de los mismos. En total y por almacén.
        El total no lo calcula, se obtiene del total global (que debería 
        coincidir con el sumatorio de...).
        """
        fechaini = self.wids['e_fechaini'].get_text().strip()
        if fechaini:
            try:
                fechaini = utils.parse_fecha(fechaini)
            except (ValueError, TypeError):
                utils.dialogo_info(titulo = "ERROR EN FECHA INICIAL", 
                 texto = "El texto «%s» no es una fecha correcta." % fechaini,
                 padre = self.wids['ventana'])
                fechaini = None
        fechafin = self.wids['e_fechafin'].get_text().strip()
        if fechafin:
            try:
                fechafin = utils.parse_fecha(fechafin)
            except (ValueError, TypeError):
                utils.dialogo_info(titulo = "ERROR EN FECHA FINAL", 
                 texto = "El texto «%s» no es una fecha correcta." % fechafin,
                 padre = self.wids['ventana'])
                fechafin = None
        if fechafin:
            FV = pclases.FacturaVenta
            FDA = pclases.FacturaDeAbono
            if fechaini:
                facturas = FV.select(pclases.AND(
                                        FV.q.fecha >= fechaini, 
                                        FV.q.fecha <= fechafin))
                # Busco los abonos (facturas de abono, en realidad, que no 
                # tienen por qué tener la misma fecha) que no hayan sido 
                # incluidos en facturas (porque si no el importe ya se habría 
                # contado en la factura anterior) ni en pagarés (porque 
                # entonces ya estarían en un documento de pago y por tanto 
                # no deberían aparecer en esta consulta)
                abonos = FDA.select(pclases.AND(
                    FDA.q.fecha >= fechaini, 
                    FDA.q.fecha <= fechafin))
            else:
                facturas = FV.select(FV.q.fecha <= fechafin)
                abonos = FDA.select(FDA.q.fecha <= fechafin)
            from ventana_progreso import VentanaProgreso
            vpro = VentanaProgreso(padre = self.wids['ventana'])
            vpro.mostrar()
            txtvpro = "Buscando facturas y abonos..."
            total = 0.0
            i = 0.0
            vpro.set_valor(i, txtvpro)
            model = self.wids['tv_datos'].get_model()
            model.clear()
            for f in facturas:
                i += 1
                vpro.set_valor(i/(facturas.count() + abonos.count()), 
                               txtvpro)
                model.append((f.numfactura, 
                            utils.str_fecha(f.fecha), 
                            f.cliente and f.cliente.cif or "¡Sin cliente!", 
                            f.cliente and f.cliente.nombre or "¡Sin cliente!", 
                            utils.float2str(f.calcular_base_imponible()), 
                            utils.float2str(f.calcular_total_iva()), 
                            utils.float2str(f.calcular_importe_total()), 
                            f.get_puid()))
                total += f.calcular_importe_total()
            for a in abonos:
                i += 1
                vpro.set_valor(i/(facturas.count() + abonos.count()), 
                               txtvpro)
                model.append((a.numfactura, 
                            utils.str_fecha(a.fecha), 
                            a.cliente and a.cliente.cif or "¡Sin cliente!", 
                            a.cliente and a.cliente.nombre or "¡Sin cliente!", 
                            utils.float2str(a.calcular_base_imponible()), 
                            utils.float2str(a.calcular_total_iva()), 
                            utils.float2str(a.calcular_importe_total()), 
                            a.get_puid()))
                total += a.calcular_importe_total()
            vpro.ocultar()
            self.wids['e_total'].set_text(utils.float2str(total))

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe.
        """
        tv = self.wids['tv_datos']
        titulo = "Libro de facturas"
        from treeview2pdf import treeview2pdf
        from informes import abrir_pdf
        strfecha = "%s - %s" % (
            self.wids['e_fechaini'].get_text(), 
            self.wids['e_fechafin'].get_text())
        nomarchivo = treeview2pdf(tv, 
            titulo = titulo,
            fecha = strfecha, 
            apaisado = False)
        abrir_pdf(nomarchivo)

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


if __name__ == '__main__':
    t = ConsultaLibroIVA()

