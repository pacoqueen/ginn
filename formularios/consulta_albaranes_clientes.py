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
## consulta_albaranes_clientes.py - 
###################################################################
## NOTAS:
##  
## ----------------------------------------------------------------
##  
###################################################################
## Changelog:
## 
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sqlobject
try:
    import pclases
except ImportError:
    import sys
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    import pclases
import mx
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes
    

class ConsultaAlbaranesCliente(Ventana):
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
        global fin
        Ventana.__init__(self, 'consulta_albaranes_clientes.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       'b_exportar/clicked': self.exportar}
        self.add_connections(connections)
        utils.rellenar_lista(self.wids['cmbe_cliente'], [(c.id, c.nombre) for c in pclases.Cliente.select(orderBy='nombre')])
        cols = (('Cliente','gobject.TYPE_STRING',False,True,False,None),
                ('Fecha','gobject.TYPE_STRING',False,True,False,None),
                ('Albarán','gobject.TYPE_STRING',False,True,False,None),
                ('Destinatario','gobject.TYPE_STRING',False,True,False,None),
                ('Facturado', 'gobject.TYPE_BOOLEAN', False, True, False, None),
                ('Facturas', 'gobject.TYPE_STRING', False, True, False, None),
                ('Idalbaran','gobject.TYPE_INT64',False,False,False,None))
        utils.preparar_listview(self.wids['tv_datos'], cols)
        self.wids['tv_datos'].connect("row-activated", self.abrir_albaran)
        temp = time.localtime()
        self.fin = str(temp[0])+'/'+str(temp[1])+'/'+str(temp[2])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
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

    def abrir_albaran(self, tv, path, view_column):
        """
        Abre el albarán seleccionado en una nueva pantalla.
        """
        self.wids['ventana'].window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        while gtk.events_pending(): gtk.main_iteration(False)
        model = tv.get_model()
        id = model[path][-1]
        albaran = pclases.AlbaranSalida.get(id)
        import albaranes_de_salida
        v = albaranes_de_salida.AlbaranesDeSalida(albaran)
        self.wids['ventana'].window.set_cursor(None)

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, items):
    	"""
        Rellena el model con los items de la consulta
        """        
    	model = self.wids['tv_datos'].get_model()
    	model.clear()
        total = 0
    	for i in items:            
            total += 1
            if i.cliente != None:
                cliente = i.cliente.nombre
            else:
                cliente = "-"
            model.append((cliente,
                          utils.str_fecha(i.fecha),
                          i.numalbaran,
                          i.nombre,
                          i.contar_lineas_facturadas() > 0,
                          ", ".join([f.numfactura for f in i.get_facturas()]),
                          i.id))
        self.wids['e_total'].set_text("%d " % total)
        
    def set_inicio(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
        self.inicio = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])


    def set_fin(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.fin = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])


    def por_fecha(self,e1,e2):
        """
        Permite ordenar una lista de albaranes por fecha
        """
        if e1.fecha < e2.fecha:
            return -1
        elif e1.fecha > e2.fecha:
            return 1
        else:
            return 0

        
    def buscar(self,boton):
        """
        Dadas fecha de inicio y de fin, lista todos los albaranes
        pendientes de facturar.
        """
        idcliente = utils.combo_get_value(self.wids['cmbe_cliente'])
        if idcliente == None:
            # utils.dialogo_info(titulo = 'ERROR', texto = 'Seleccione un cliente', padre = self.wids['ventana'])
            # return
            # Selecciono los albaranes de todos los clientes.
            if self.inicio == None:
                albaranes = pclases.AlbaranSalida.select(pclases.AlbaranSalida.q.fecha <= self.fin,
                                                         orderBy = 'fecha')
            else:
                albaranes = pclases.AlbaranSalida.select(sqlobject.AND(pclases.AlbaranSalida.q.fecha >= self.inicio,
                                                                       pclases.AlbaranSalida.q.fecha <= self.fin), 
                                                         orderBy='fecha')    
        else:
            self.cliente = pclases.Cliente.get(utils.combo_get_value(self.wids['cmbe_cliente']))
            cliente = self.cliente
            if self.inicio == None:
                albaranes = pclases.AlbaranSalida.select(sqlobject.AND(pclases.AlbaranSalida.q.fecha <= self.fin,
                                                                       pclases.AlbaranSalida.q.clienteID == cliente.id), 
                                                         orderBy = 'fecha')

            else:
                albaranes = pclases.AlbaranSalida.select(sqlobject.AND(pclases.AlbaranSalida.q.fecha >= self.inicio,
                                                                       pclases.AlbaranSalida.q.fecha <= self.fin, 
                                                                       pclases.AlbaranSalida.q.clienteID == cliente.id), 
                                                         orderBy='fecha')    
        self.resultado = albaranes
        self.rellenar_tabla(self.resultado)


    def imprimir(self,boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        import informes
        datos = []
        # for i in self.resultado:
        #     datos.append((i.cliente.nombre,
        #                 utils.str_fecha(i.fecha),
        #                 i.numalbaran,
        #                 i.nombre))
        model = self.wids['tv_datos'].get_model()
        for i in model:
            datos.append((i[0], i[1], i[2], i[3], i[5]))        
        if (self.inicio) == None:            
            fechaInforme = 'Hasta '+utils.str_fecha(time.strptime(self.fin,"%Y/%m/%d"))
        else:
            fechaInforme = utils.str_fecha(time.strptime(self.inicio,"%Y/%m/%d"))+' - '+utils.str_fecha(time.strptime(self.fin,"%Y/%m/%d"))
            
        if datos != []:
            informes.abrir_pdf(geninformes.albaranesCliente(datos, self.cliente and self.cliente.nombre or "", fechaInforme))


if __name__ == '__main__':
    t = ConsultaAlbaranesCliente()

