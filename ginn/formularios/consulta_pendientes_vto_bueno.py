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
## consulta_pendientes_vto_bueno.py - 
###################################################################
## NOTAS:
## Se muestran las pendientes de confirmación de usuario al usuario
## aunque ya hayan obtenido el visto bueno y tengan el número de 
## control. It's not a bug. It's a feature!
###################################################################
## Changelog:
## 26/02/2007 -> Inicio
## 
###################################################################
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sqlobject
import sys
from ginn.framework import pclases
import mx.DateTime
import geninformes
import re
import ventana_progreso
from utils import _float as float


class ConsultaPendientesVtoBueno(Ventana):
    inicio = None
    fin = None
    resultado = []
        
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        global fin
        Ventana.__init__(self, 'consulta_pendientes_vto_bueno.glade', objeto, usuario = self.usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_pendientes/clicked': self.buscar,
                       'b_todas/clicked': self.buscar,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin}
        self.add_connections(connections)
        utils.rellenar_lista(self.wids['cmbe_proveedor'], [(c.id, c.nombre) for c in pclases.Proveedor.select(orderBy='nombre')])
        cols = (('Factura', 'gobject.TYPE_STRING', False, True, True, None),
                ('Código vto. bueno', 'gobject.TYPE_STRING', False, True, False, None),
                ('Proveedor', 'gobject.TYPE_STRING', False, True, False, None),
                ('Importe', 'gobject.TYPE_STRING', False, False, False, None),
                ('Fecha fra.', 'gobject.TYPE_STRING', False, True, False, None),
                ('Fecha recepción', 'gobject.TYPE_STRING', False, True, False, None),
                ('Automático', 'gobject.TYPE_BOOLEAN', False, True, False, None),
                ('Usuario', 'gobject.TYPE_BOOLEAN', False, True, False, None),
                ('Técnico', 'gobject.TYPE_BOOLEAN', False, True, False, None),
                ('Comercial', 'gobject.TYPE_BOOLEAN', False, True, False, None),
                ('D. General', 'gobject.TYPE_BOOLEAN', False, True, False, None),
                ('id', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(self.wids['tv_datos'], cols)
        self.wids['tv_datos'].connect("row-activated", self.abrir_factura)
        self.colorear(self.wids['tv_datos'])
        temp = time.localtime()
        self.fin = mx.DateTime.DateTimeFrom(day = temp[2], month = temp[1], year = temp[0])
        self.inicio = self.fin - mx.DateTime.oneWeek * 4
        self.wids['e_fechafin'].set_text(utils.str_fecha(self.fin))
        self.wids['e_fechainicio'].set_text(utils.str_fecha(self.inicio))
        sens = self.usuario == None or self.usuario.firmaUsuario or self.usuario.firmaComercial or self.usuario.firmaTecnico or self.usuario.firmaDirector or self.usuario.firmaTotal
        self.wids['b_pendientes'].set_sensitive(sens)
        self.wids['b_pendientes'].child.child.get_children()[1].set_text("Ver pendientes de mi firma (%s)" % (self.usuario and self.usuario.usuario or "cualquiera"))
        gtk.main()

    def abrir_factura(self, tv, path, view_column):
        model = tv.get_model()
        idfra = model[path][-1]
        fra = pclases.FacturaCompra.get(idfra)
        import facturas_compra          
        ventanafacturas = facturas_compra.FacturasDeEntrada(fra, usuario = self.usuario)

    def colorear(self, tv):
        def cell_func_vto_bueno(col, cell, model, itr):
            txt = model[itr][1]
            if txt != None:
                if txt.startswith("PENDIENTE"):
                    color = "IndianRed"
                else:
                    color = "LightBlue"
            else:
                color = None
            cell.set_property("cell-background", color)
        col = tv.get_column(1)
        cells = col.get_cell_renderers()
        for cell in cells:
            col.set_cell_data_func(cell, cell_func_vto_bueno)

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, fras):
    	"""
        Rellena el model con los items de la consulta
        """        
    	model = self.wids['tv_datos'].get_model()
    	model.clear()
        self.wids['e_total_fras'].set_text("%d facturas listadas." % (len(fras)))
    	for fra in fras:
            codigo_numerico_validacion = fra.get_codigo_validacion_visto_bueno()
            vtobueno = fra.vistoBuenoPago and fra.numeroControl or "PENDIENTE: %s" % (pclases.FacturaCompra.codigos_no_validacion[codigo_numerico_validacion])
            model.append((fra.numfactura,
                          vtobueno,
                          fra.proveedor and fra.proveedor.nombre or "¡Sin proveedor", 
                          utils.float2str(fra.calcular_importe_total()), 
                          utils.str_fecha(fra.fecha), 
                          utils.str_fecha(fra.fechaEntrada),
                          fra.get_visto_bueno_automatico(), 
                          fra.vistoBuenoUsuario, 
                          fra.vistoBuenoTecnico, 
                          fra.vistoBuenoComercial, 
                          fra.vistoBuenoDirector, 
                          fra.id))
        
    def set_inicio(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
        self.inicio = mx.DateTime.DateTimeFrom(year = int(temp[2]), month = int(temp[1]), day = (temp[0]))

    def set_fin(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.fin = mx.DateTime.DateTimeFrom(year = int(temp[2]), month = int(temp[1]), day = (temp[0]))

    def buscar(self,boton):
        """
        Dadas fecha de inicio y de fin, lista todos los albaranes
        pendientes de facturar.
        """
        if not self.inicio:
            facturas = pclases.FacturaCompra.select(pclases.FacturaCompra.q.fecha <= self.fin, orderBy = 'fecha')
        else:
            facturas = pclases.FacturaCompra.select(sqlobject.AND(pclases.FacturaCompra.q.fecha >= self.inicio,pclases.FacturaCompra.q.fecha <= self.fin), orderBy='fecha')       
        idproveedor = utils.combo_get_value(self.wids['cmbe_proveedor'])
        if idproveedor != None:
            proveedor = pclases.Proveedor.get(utils.combo_get_value(self.wids['cmbe_proveedor']))
            facturas = [v for v in facturas if v.proveedorID == proveedor.id]
        self.resultado = []
        condusuario = self.usuario == None or self.usuario.firmaTotal or self.usuario.firmaUsuario
        condtecnico = self.usuario == None or self.usuario.firmaTotal or self.usuario.firmaTecnico
        condcomercial = self.usuario == None or self.usuario.firmaTotal or self.usuario.firmaComercial
        conddirector = self.usuario == None or self.usuario.firmaTotal or self.usuario.firmaDirector
        for i in facturas:
            if boton.name == "b_pendientes":
                if condusuario and not i.vistoBuenoUsuario and i not in self.resultado:
                    self.resultado.append(i)
                if condtecnico and not i.vistoBuenoTecnico and i not in self.resultado:
                    self.resultado.append(i)
                if condcomercial and not i.vistoBuenoComercial and i not in self.resultado:
                    self.resultado.append(i)
                if conddirector and not i.vistoBuenoDirector and i not in self.resultado:
                    self.resultado.append(i)
            elif boton.name == "b_todas":
                self.resultado.append(i)
        self.resultado.sort(utils.cmp_fecha_id)
        self.rellenar_tabla(self.resultado)


if __name__ == '__main__':
    t = ConsultaPendientesVtoBueno()

