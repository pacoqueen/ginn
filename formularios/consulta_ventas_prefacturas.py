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
## consulta_ventas_prefacturas.py -- 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 2 de diciembre 2007 -> Inicio
## 
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, time
try:
    import pclases
except ImportError:
    import sys
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    import pclases
import mx.DateTime

class ConsultaVentasPrefacturas(Ventana):
    inicio = None
    fin = None
    resultado = []
        
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        global fin
        Ventana.__init__(self, 'consulta_ventas.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin}
        self.add_connections(connections)
        cols = (('Cliente','gobject.TYPE_STRING',False,True,False,None),
                ('Factura','gobject.TYPE_STRING',False,True,True,None),
                ('Fecha','gobject.TYPE_STRING',False,True,False,None),
                ('Total','gobject.TYPE_STRING',False,True,False,None),
                ('Beneficio','gobject.TYPE_STRING',False,True,False,None),
                ('Pendiente','gobject.TYPE_STRING',False,True,False,None),
                ('Id','gobject.TYPE_INT64',False,False,False,None))
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        self.wids['tv_datos'].connect("row-activated", self.abrir_prefactura)
        self.wids['tv_datos'].get_column(3).get_cell_renderers()[0].set_property('xalign', 1) 
        self.wids['tv_datos'].get_column(4).get_cell_renderers()[0].set_property('xalign', 1) 
        self.wids['tv_datos'].get_column(5).get_cell_renderers()[0].set_property('xalign', 1) 
        temp = time.localtime()
        self.fin = str(temp[0])+'/'+str(temp[1])+'/'+str(temp[2])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.metros_totales = 0.0
        self.kilos_totales = 0.0
        opciones = [(c.id, c.nombre) for c in pclases.Cliente.select(orderBy = "nombre")]
        opciones.insert(0, (-1, "Todos"))
        utils.rellenar_lista(self.wids['cbe_cliente'], opciones)
        utils.combo_set_from_db(self.wids['cbe_cliente'], -1)
        self.wids['label7'].set_text("Total beneficio estimado: ")
        #self.wids['label7'].set_property("visible", False)
        #self.wids['e_total_kilos'].set_property("visible", False)
        self.wids['label8'].set_property("visible", False)
        self.wids['e_total_metros'].set_property("visible", False)
        self.wids['label9'].set_property("visible", False)
        self.wids['cbe_cliente'].set_property("visible", False)
        self.wids['ventana'].set_title("Listado de prefacturas")
        self.wids['notebook1'].remove_page(1)
        self.wids['label1'].set_text("Por cliente")
        labpdte = gtk.Label("Total pendiente:")
        labpdte.show()
        self.wids['hbox4'] = gtk.HBox()
        self.wids['hbox4'].add(labpdte)
        self.wids['e_totpdte'] = gtk.Entry()
        self.wids['e_totpdte'].set_property("editable", False)
        self.wids['e_totpdte'].set_property("has-frame", False)
        self.wids['hbox4'].add(self.wids['e_totpdte'])
        self.wids['hbox4'].show_all()
        self.wids['vbox2'].add(self.wids['hbox4'])
        self.wids['vbox2'].reorder_child(self.wids['hbox4'], 2)
        self.wids['e_totpdte'].show()
        gtk.main()
    
    def abrir_prefactura(self, tv, path, view_column):
        """
        Si la fila seleccionada es una tarifa, abre la tarifa. Si es 
        un producto, abre el producto.
        """
        model = tv.get_model()
        id = model[path][-1]
        if id > 0 and model[path].parent != None: # Es prefactura
            prefactura = pclases.Prefactura.get(id)
            import prefacturas
            v = prefacturas.Prefacturas(prefactura)

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, items):
        """
        Rellena el model con los items de la consulta
        """ 
        model = self.wids['tv_datos'].get_model()
        model.clear()
        total = totben = totpdte = 0.0
        clientes = {}
        for f in items:
            cliente = f.cliente
            if cliente not in clientes:
                clientes[cliente] = model.append(None, (cliente and cliente.nombre or "Sin cliente", 
                                                        "", 
                                                        "", 
                                                        "0.0", 
                                                        "0.0", 
                                                        "0.0", 
                                                        cliente and cliente.id or 0))
            nodo_padre = clientes[cliente]
            totalpfra = f.importeTotal
            beneficio = f.calcular_beneficio()
            pdte = f.calcular_pendiente_cobro()
            model.append(nodo_padre, ("", 
                                      f.numfactura,
                                      utils.str_fecha(f.fecha), 
                                      utils.float2str(totalpfra), 
                                      utils.float2str(beneficio),
                                      utils.float2str(pdte), 
                                      f.id))
            model[nodo_padre][3] = utils.float2str(
                utils._float(model[nodo_padre][3]) + totalpfra)
            model[nodo_padre][4] = utils.float2str(
                utils._float(model[nodo_padre][4]) + beneficio)
            model[nodo_padre][5] = utils.float2str(
                utils._float(model[nodo_padre][5]) + pdte)
            total += totalpfra
            totben += beneficio
            totpdte += pdte
        self.wids['e_total'].set_text("%s" % (utils.float2str(total)))
        self.wids['e_total_kilos'].set_text("%s" % (utils.float2str(totben)))
        self.wids['e_totpdte'].set_text("%s" % (utils.float2str(totpdte)))
        # Y ahora la gráfica.
        datachart = [["Total", total], 
                     ["Beneficio", totben], 
                     ["Pendiente", totpdte]]
        try:
            import gtk, gobject, cairo, copy, math  # @UnusedImport
        except ImportError:
            return      # No se pueden dibujar gráficas. # TODO: Temporal.
        try:
            import charting
        except ImportError:
            import sys, os
            sys.path.append(os.path.join("..", "utils"))
            import charting
        try:
            oldchart = self.wids['eventbox_chart'].get_child()
            if oldchart != None:
                #self.wids['eventbox_chart'].remove(oldchart)
                chart = oldchart
            else:
                chart = charting.Chart(orient = "horizontal")
                self.wids['eventbox_chart'].add(chart)
            chart.plot(datachart)
            self.wids['eventbox_chart'].show_all()
        except Exception, msg:
            txt = "consulta_ventas_prefacturas.py::rellenar_tabla -> "\
                  "Error al dibujar gráfica (charting): %s" % msg
            print txt
            self.logger.error(txt)

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
        Permite ordenar una lista de objetos por fecha (deben tener un atributo fecha).
        """
        if e1.fecha < e2.fecha:
            return -1
        elif e1.fecha > e2.fecha:
            return 1
        else:
            return 0
        
    def buscar(self, boton):
        """
        Dadas fecha de inicio y de fin, busca todas las ventas 
        (facturadas) entre esas dos fechas.
        """
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        # print self.fin, self.inicio
        vpro.set_valor(0.0, "Analizando prefacturas...")
        idcliente = utils.combo_get_value(self.wids['cbe_cliente'])
        self.resultado = []
        fechafin = mx.DateTime.DateTimeFrom(day = int(self.fin.split("/")[2]), 
                                            month = int(self.fin.split("/")[1]), 
                                            year = int(self.fin.split("/")[0]))
        if not self.inicio:
            prefacturas = pclases.Prefactura.select(pclases.Prefactura.q.fecha <= fechafin, orderBy = 'fecha')
            vpro.set_valor(0.5, "Analizando prefacturas...")
        else:
            fechainicio = mx.DateTime.DateTimeFrom(
                                    day = int(self.inicio.split("/")[2]), 
                                    month = int(self.inicio.split("/")[1]), 
                                    year = int(self.inicio.split("/")[0]))
            prefacturas = pclases.Prefactura.select(pclases.AND(
                                    pclases.Prefactura.q.fecha >= fechainicio,
                                    pclases.Prefactura.q.fecha <= fechafin), 
                                orderBy='fecha')
            vpro.set_valor(0.5, "Analizando prefacturas...")
        self.resultado = list(prefacturas)
        vpro.set_valor(0.8, "Analizando prefacturas...")
        self.resultado.sort(self.por_fecha)
        vpro.set_valor(0.9, "Analizando prefacturas...")
        vpro.ocultar()
        self.rellenar_tabla(self.resultado)

    def imprimir(self,boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        import sys, os, mx, mx.DateTime
        sys.path.append(os.path.join("..", "informes"))
        from treeview2pdf import treeview2pdf
        from informes import abrir_pdf
        fechafin = mx.DateTime.DateTimeFrom(day = int(self.fin.split("/")[2]), 
                                            month = int(self.fin.split("/")[1]), 
                                            year = int(self.fin.split("/")[0]))
        strfecha = utils.str_fecha(fechafin)
        if self.inicio:
            fechainicio = mx.DateTime.DateTimeFrom(day = int(self.inicio.split("/")[2]), 
                                                   month = int(self.inicio.split("/")[1]), 
                                                   year = int(self.inicio.split("/")[0]))
            strfecha = "Del %s al %s" % (utils.str_fecha(fechainicio), strfecha)
        tv = self.wids['tv_datos']
        abrir_pdf(treeview2pdf(tv, titulo = "Listado facturas pro forma", fecha = strfecha, apaisado = False))


if __name__ == '__main__':
    t = ConsultaVentasPrefacturas()

