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
## iva.py - Cuentas de IVA devengado y soportado.
###################################################################
## NOTAS:
## 
###################################################################
## Changelog:
## 26 de junio de 2007 -> Inicio
## 
###################################################################
## TODO: 
## - Aparte del resumen por factura y total, hacer un calco del 
##   modelo de la AEAT con los datos en su sitio para imprimir y 
##   entregar.
###################################################################
## NOTAS: 
## 
###################################################################
from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
import mx.DateTime


class IVA(Ventana):

    def __init__(self, objeto = None, usuario = None):
        self.usuario = usuario
        Ventana.__init__(self, 'iva.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_aplicar_trimestre/clicked': self.aplicar_trimestre, 
                       'b_fecha_inicio/clicked': self.set_fecha, 
                       'b_fecha_fin/clicked': self.set_fecha, 
                       'b_imprimir/clicked': self.imprimir, 
                       'b_buscar/clicked': self.actualizar_tabla, 
                       }
        self.add_connections(connections)
        self.preparar_tv(self.wids['tv_datos'])
        self.wids['e_fecha_fin'].set_text(utils.str_fecha(mx.DateTime.localtime()))
        gtk.main()

    def imprimir(self, boton):
        """
        Imprime la relación de facturas y los dos totales.
        """
        # TODO
        utils.dialogo_info(titulo = "NO DISPONIBLE", 
                           texto = "Funcionalidad no disponible.", 
                           padre = self.wids['ventana'])

    def aplicar_trimestre(self, boton):
        """
        Pone las fechas del trimestre seleccionado en los "entries".
        """
        anno = mx.DateTime.localtime().year
        if self.wids['rd1t'].get_active():
            fini = mx.DateTime.DateTimeFrom(day = 1, month = 1, year = anno)
            ffin = mx.DateTime.DateTimeFrom(day = 31, month = 3, year = anno)
        elif self.wids['rd2t'].get_active():
            fini = mx.DateTime.DateTimeFrom(day = 1, month = 4, year = anno)
            ffin = mx.DateTime.DateTimeFrom(day = 30, month = 6, year = anno)
        elif self.wids['rd3t'].get_active():
            fini = mx.DateTime.DateTimeFrom(day = 1, month = 7, year = anno)
            ffin = mx.DateTime.DateTimeFrom(day = 30, month = 9, year = anno)
        elif self.wids['rd4t'].get_active():
            fini = mx.DateTime.DateTimeFrom(day = 1, month = 10, year = anno)
            ffin = mx.DateTime.DateTimeFrom(day = 31, month = 12, year = anno)
        else:
            fini = mx.DateTime.DateTimeFrom(day = 1, month = 1, year = anno)
            ffin = mx.DateTime.DateTimeFrom(day = 31, month = 12, year = anno)
        self.wids['e_fecha_inicio'].set_text(utils.str_fecha(fini))
        self.wids['e_fecha_fin'].set_text(utils.str_fecha(ffin))
        self.wids["b_buscar"].grab_focus()

    def set_fecha(self, boton):
        """
        Muestra el diálogo de selección de fecha en calendario.
        """
        if "inicio" in boton.name:
            e = self.wids['e_fecha_inicio']
        elif "fin" in boton.name:
            e = self.wids['e_fecha_fin']
        else:
            return
        try:
            e.set_text(utils.str_fecha(utils.mostrar_calendario(e.get_text(), self.wids['ventana'])))
        except:
            e.set_text(utils.str_fecha(utils.mostrar_calendario(padre = self.wids['ventana'])))

    def actualizar_tabla(self, boton = None):
        """
        Actualiza la información completa de la tabla, 
        volviendo a buscar las balas e introduciéndolas 
        en el TreeView.
        """
        facturas = self.buscar()
        self.rellenar_tabla(facturas)

    def chequear_cambios(self):
        pass

    def buscar(self):
        """
        Buscar las facturas de compra y de venta comprendidas entre 
        las fechas de la ventana, las ordena por fecha y devuelve 
        una lista de las mismas.
        """
        try:
            txt_fini = self.wids['e_fecha_inicio'].get_text()
            fini = utils.parse_fecha(txt_fini)
        except:
            utils.dialogo_info(titulo = "ERROR FORMATO", 
                               texto = "El texto %s no es una fecha correcta." % txt_fini, 
                               padre = self.wids['ventana'])
            return []
        try:
            txt_ffin = self.wids['e_fecha_fin'].get_text()
            ffin = utils.parse_fecha(txt_ffin)
        except:
            utils.dialogo_info(titulo = "ERROR FORMATO", 
                               texto = "El texto %s no es una fecha correcta." % txt_ffin, 
                               padre = self.wids['ventana'])
            return []
        fraventas = pclases.FacturaVenta.select(pclases.AND(pclases.FacturaVenta.q.fecha >= fini, 
                                                            pclases.FacturaVenta.q.fecha <= ffin))
        fracompras = pclases.FacturaCompra.select(pclases.AND(pclases.FacturaCompra.q.fecha >= fini, 
                                                              pclases.FacturaCompra.q.fecha <= ffin))
        #facturas = list(fraventas) + list(fracompras)
        # Me quito las facturas con IVA 0 (usualmente generadas para 
        # controlar ingresos a Hacienda y SS) y las de Portugal (23% de IVA) 
        # que irían en adquisiciones intracomunitarias en caso de que la 
        # empresa esté dada de alta como operador intracomunitario y sería 
        # autorrepercutido, etc. 
        # [19/02/2013] Aprovecho que el IVA en España está ya al 21% para 
        # filtrar por ahí en lugar de por la nacionalidad del 
        # proveedor. POTENTIAL RISK!
        facturas = list(fraventas) + [f for f in fracompras if not f.iva_homogeneo() or (f.iva != 0.0 and f.iva < 0.23)]
        facturas.sort(lambda f1, f2: utils.orden_por_campo_o_id(f1, f2, "fecha"))
        return facturas

    def rellenar_tabla(self, fras):
        """
        Introduce las facturas recibidas en el TreeView y 
        calcula el total de IVA para las facturas de compra 
        y de venta por separado.
        """
        tv = self.wids['tv_datos']
        model = tv.get_model()
        tv.freeze_child_notify()
        tv.set_model(None)
        model.clear()
        devengado = 0.0
        soportado = 0.0
        base_devengado = 0.0
        for fra in fras:
            if isinstance(fra, pclases.FacturaVenta):
                iva = fra.calcular_total_iva()
                base_devengado += fra.calcular_base_imponible()
                devengado += iva
                fila = [utils.str_fecha(fra.fecha), 
                        "%s (%s)" % (fra.numfactura, 
                                     fra.cliente and fra.cliente.nombre or ""),
                        "%s €" % utils.float2str(fra.calcular_importe_total()), 
                        "%s €" % utils.float2str(iva), 
                        "", 
                        "", 
                        "", 
                        "FV:%d" % fra.id
                        ]
            elif isinstance(fra, pclases.FacturaCompra):
                iva = fra.calcular_importe_iva()
                soportado += iva
                fila = [utils.str_fecha(fra.fecha), 
                        "", 
                        "",
                        "", 
                        "%s (%s)" % (fra.numfactura, fra.proveedor and fra.proveedor.nombre or ""), 
                        "%s €" % utils.float2str(fra.calcular_importe_total()), 
                        "%s €" % utils.float2str(iva), 
                        "FC:%d" % fra.id
                        ]
            else:
                self.logger.error("iva::rellenar_tabla -> Factura %s no es FacturaVenta ni FacturaCompra." % fra)
                continue
            model.append(fila)
        tv.set_model(model)
        tv.thaw_child_notify()
        self.mostrar_totales(devengado, soportado, base_devengado)

    def mostrar_totales(self, devengado, soportado, base_devengado):
        """
        Muestra los totales, la diferencia de ambos y colorea los Entries.
        """
        # Base imponible de las facturas de venta. (Si trabajara con más IVAs debería haber una línea por cada tipo de IVA)
        self.wids['e_base_devengado'].set_text("%s €" % (utils.float2str(base_devengado, 2)))
        # Devengado
        self.wids['e_devengado'].set_text("%s €" % utils.float2str(devengado, 2))
        tips = gtk.Tooltips()
        tips.set_tip(self.wids['e_devengado'], str(devengado))
        tips.enable()
        self.wids['e_devengado'].modify_text(gtk.STATE_NORMAL, self.wids['e_devengado'].get_colormap().alloc_color("red"))
        # Soportado
        self.wids['e_soportado'].set_text("%s €" % utils.float2str(soportado, 2))
        tips = gtk.Tooltips()
        tips.set_tip(self.wids['e_soportado'], str(soportado))
        tips.enable()
        self.wids['e_soportado'].modify_text(gtk.STATE_NORMAL, self.wids['e_soportado'].get_colormap().alloc_color("blue"))
        # Diferencia
        diferencia = devengado - soportado
        self.wids['e_diferencia'].set_text("%s €" % utils.float2str(diferencia, 2))
        tips = gtk.Tooltips()
        tips.set_tip(self.wids['e_diferencia'], str(diferencia))
        tips.enable()
        if diferencia > 0:
            self.wids['e_diferencia'].modify_text(gtk.STATE_NORMAL, self.wids['e_diferencia'].get_colormap().alloc_color("red"))
        else:
            self.wids['e_diferencia'].modify_text(gtk.STATE_NORMAL, self.wids['e_diferencia'].get_colormap().alloc_color("blue"))

    def preparar_tv(self, tv):
        """
        Prepara las columnas del TreeView.
        """
        cols = (('Fecha', 'gobject.TYPE_STRING', False, True, True, None),
                ('Factura venta', 'gobject.TYPE_STRING', False, True, False, None),
                ('Importe', 'gobject.TYPE_STRING', False, True, False, None), 
                ('IVA', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Factura compra', 'gobject.TYPE_STRING', False, True, False, None),
                ('Importe', 'gobject.TYPE_STRING', False, True, False, None), 
                ('IVA', 'gobject.TYPE_STRING', False, True, False, None), 
                ('ID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(tv, cols)
        for col in tv.get_columns()[2:4] + tv.get_columns()[5:7]:
            for cell in col.get_cell_renderers():
                cell.set_property("xalign", 1.0)
            col.set_alignment(0.5)
        tv.connect("row-activated", self.abrir_factura)

    def abrir_factura(self, tv, path, vc):
        """
        Abre la factura a la que se le ha hecho doble clic en el TreeView.
        """
        tid = tv.get_model()[path][-1]
        tipo, ide = tid.split(":")
        ide = int(ide)
        if tipo == "FV":
            from formularios import facturas_venta
            v = facturas_venta.FacturasVenta(pclases.FacturaVenta.get(id), usuario = self.usuario)  # @UnusedVariable
        elif tipo == "FC":
            from formularios import facturas_compra
            v = facturas_compra.FacturasDeEntrada(pclases.FacturaCompra.get(id), usuario = self.usuario)  # @UnusedVariable


################################################################################

if __name__ == '__main__':
    v = IVA() 


