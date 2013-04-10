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
## facturas_no_bloqueadas.py - Facturas no bloqueadas.
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 22 de mayo de 2006 -> Inicio
###################################################################
## FIXME: 
## BUG: Si abre dos o más facturas, bloquea alguno, vuelve a la 
## ventana y actualiza con el botón Actualizar, es posible que 
## se le active el CheckBox en el cell del path que ahora ocuparía
## otra factura distinta (ya que el que ha sido verificado ya no 
## aparecería en la lista).
###################################################################
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sqlobject
try:
    from framework import pclases
except ImportError:
    import sys
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    from framework import pclases
import mx.DateTime
import ventana_progreso    

class FacturasNoBloqueadas(Ventana):
    def __init__(self, objeto = None, usuario = None):
        self.usuario = usuario
        Ventana.__init__(self, 'facturas_no_bloqueadas.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_editar/clicked': self.abrir_factura,
                       'b_actualizar/clicked': self.actualizar}
        self.add_connections(connections)
        cols = (('Nº Factura', 'gobject.TYPE_STRING', False, True, True, None),
                ('Fecha','gobject.TYPE_STRING', False, True, False, None),
                ('Cliente','gobject.TYPE_STRING', False, True, False, None),
                ('Importe','gobject.TYPE_STRING', False, True, False, None),
                ('Albarán','gobject.TYPE_STRING', False, True, False, None),
                ('Visto','gobject.TYPE_BOOLEAN', True, True, False, None),
                ('Motivo', 'gobject.TYPE_STRING', False, True, False, None),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_facturas'], cols)
        if self.usuario != None:
            ventanas_con_permiso = [p.ventana.fichero for p in self.usuario.permisos if p.permiso] # and p.escritura]    # STILL UNIMPLEMENTED
        else:
            ventanas_con_permiso = ["facturas_venta.py", ]  # Si lo arranco desde consola, que me deje editarlo todo. 
        if 'facturas_venta.py' in ventanas_con_permiso:
            self.wids['b_editar'].set_sensitive(True)
            self.wids['tv_facturas'].connect("row-activated", self.abrir_factura_tv)
        else: 
            self.wids['b_editar'].set_sensitive(False)
            self.wids['b_editar'].hide()
        cols = (('Nº Albarán', 'gobject.TYPE_STRING', False, True, True, None), 
                ('Fecha', 'gobject.TYPE_STRING', False, True, False, None),
                ('Cliente', 'gobject.TYPE_STRING', False, True, False, None),
                ('¿Parcialmente facturado?', 'gobject.TYPE_BOOLEAN', False, True, False, None),
                ('Producto', 'gobject.TYPE_STRING', False, True, False, None),
                ('Cantidad', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Bultos', 'gobject.TYPE_STRING', False, True, False, None), 
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_albaranes'], cols)
        self.wids['tv_albaranes'].connect("row-activated", self.abrir_albaran_tv)
        self.rellenar_facturas()
        self.rellenar_albaranes_no_facturados()
        gtk.main()

    def chequear_cambios(self):
        pass

    def rellenar_albaranes_no_facturados(self):
        """
        Rellena el model de albaranes no facturados.
        """
        ldvs_sin_facturar = pclases.LineaDeVenta.select(pclases.AND(pclases.LineaDeVenta.q.albaranSalidaID != None, 
                                                                    pclases.LineaDeVenta.q.facturaVentaID == None, 
                                                                    pclases.LineaDeVenta.q.prefacturaID == None))
        albaranes_no_facturados = []
        for ldv in ldvs_sin_facturar:
            if ldv.albaranSalida.facturable and ldv.albaranSalida not in albaranes_no_facturados:
                albaranes_no_facturados.append(ldv.albaranSalida)
        model = self.wids['tv_albaranes'].get_model()
        model.clear()
        self.wids['tv_albaranes'].set_model(None)
        for a in albaranes_no_facturados:
            padre = model.append(None, (a.numalbaran,
                                        utils.str_fecha(a.fecha), 
                                        a.cliente and a.cliente.nombre or "-", 
                                        a.get_facturas() != [], 
                                        "", 
                                        "",
                                        "", 
                                        a.id))
            for ldv in [ldv for ldv in a.lineasDeVenta if ldv.facturaVentaID == None or ldv.prefacturaID == None]:
                model.append(padre, ("", 
                                     "", 
                                     "", 
                                     "", 
                                     ldv.producto and ldv.producto.descripcion or "-", 
                                     ldv.get_str_cantidad(), 
                                     ldv.get_str_bultos(),
                                     ldv.id))
        self.wids['tv_albaranes'].set_model(model)

    def rellenar_facturas(self):
    	"""
        Rellena el model con las facturas no bloqueadas.
        """        
    	model = self.wids['tv_facturas'].get_model()
    	model.clear()
        self.wids['tv_facturas'].freeze_child_notify()
        self.wids['tv_facturas'].set_model(None)
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        i = 0.0
        facturas = pclases.FacturaVenta.select(pclases.FacturaVenta.q.bloqueada == False, orderBy = "id")
        prefacturas = pclases.Prefactura.select(pclases.Prefactura.q.bloqueada == False, orderBy = "id")
        tot = facturas.count() + prefacturas.count()
        for factura in facturas:
            vpro.set_valor(i/tot, 'Recuperando factura %s...' % (factura.numfactura))
            i += 1
            if factura.vencimientosCobro == []:
                motivo = "Sin vencimientos."
            elif factura.cliente.cif == None or factura.cliente.cif.strip() == "":
                motivo = "Cliente sin CIF."
            else:
                motivo = "Factura no bloqueada."
            model.append((factura.numfactura,
                          utils.str_fecha(factura.fecha),
                          factura.cliente and factura.cliente.nombre or "-",
                          "%s €" % (utils.float2str(factura.calcular_total())), 
                          ", ".join([a.numalbaran for a in factura.get_albaranes()]),
                          factura.bloqueada,
                          motivo,
                          factura.id))
        for factura in prefacturas:
            vpro.set_valor(i/tot, 'Recuperando factura %s...' % (factura.numfactura))
            i += 1
            if factura.vencimientosCobro == []:
                motivo = "Sin vencimientos."
            elif factura.cliente.cif == None or factura.cliente.cif.strip() == "":
                motivo = "Cliente sin CIF."
            else:
                motivo = "Factura no bloqueada."
            model.append((factura.numfactura,
                          utils.str_fecha(factura.fecha),
                          factura.cliente and factura.cliente.nombre or "-",
                          "%s €" % (utils.float2str(factura.calcular_total())), 
                          ", ".join([a.numalbaran for a in factura.get_albaranes()]),
                          factura.bloqueada,
                          motivo,
                          factura.id))
        self.wids['tv_facturas'].set_model(model)
        self.wids['tv_facturas'].thaw_child_notify()
        vpro.ocultar()
    
    def actualizar(self, b):    
        self.rellenar_facturas()
        self.rellenar_albaranes_no_facturados()

    def abrir_factura(self, b):
        model, iter = self.wids['tv_facturas'].get_selection().get_selected()
        if iter != None:
            self.abrir_factura_tv(self.wids['tv_facturas'], model.get_path(iter), None)

    def abrir_albaran_tv(self, treeview, path, view_column):
        """
        Abre el albarán seleccionado con doble clic.
        """
        model = treeview.get_model()
        iter = model.get_iter(path)
        padre = model[iter].parent
        if padre != None:
            idalbaran = padre[-1]
        else:
            idalbaran = model[path][-1]
        albaran = pclases.AlbaranSalida.get(idalbaran)
        import albaranes_de_salida
        ventana_alb = albaranes_de_salida.AlbaranesDeSalida(albaran)

    def abrir_factura_tv(self, treeview, path, view_column):
        model = treeview.get_model()
        self.abrir_ventana_factura(path)

    def abrir_ventana_factura(self, path):
        """
        Abre la ventana de la factura según el tipo que sea.
        path es el path que ocupa en el model.
        """
        model = self.wids['tv_facturas'].get_model()
        model[path][5] = True               # OJO: Directamente se marca como bloqueado. 
                # En las facturas se asegura que no se cierre hasta que la casilla esté marcada.
        if not utils.abrir_factura_venta(model[path][-1], model[path][0], self.usuario):
            utils.abrir_prefactura(model[path][-1], model[path][0], self.usuario)

    def bloquear(self, cell, path):
        """
        Abre la factura para ser revisado.
        """
        model = self.wids['tv_facturas'].get_model()
        bloqueada = not cell.get_active()
        self.abrir_ventana_factura(path)
        # Cambiado comportamiento para obligar a revisar la factura.
        #factura.bloqueada = bloqueada
        #factura.syncUpdate()


if __name__ == '__main__':
    t = FacturasNoBloqueadas()
 
