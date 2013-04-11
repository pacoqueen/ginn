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
## consulta_albaranesPorFacturar.py - 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 
###################################################################
## DONE: 
## + Mostrar transportes y comisiones por facturar.
## + Convertir en TreeView y mostrar descripción del material y 
##   cantidad.
## + Mostrar un total agrupado por descripción de material y total 
##   de cantidades.
## + Modificar impreso para mostrar productos y totales.
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
    

class ConsultaAlbaranesPorFacturar(Ventana):
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
        Ventana.__init__(self, 'consulta_albaranesPorFacturar.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       'b_exportar_ae/clicked': self.exportar, 
                       'b_exportar_as/clicked': self.exportar, 
                       'b_exportar_totales/clicked': self.exportar}
        self.add_connections(connections)
        cols = (('Fecha','gobject.TYPE_STRING', False, True, False, None),
                ('Nº Albarán','gobject.TYPE_STRING', False, True, True, None),
                ('Descripción del material', 'gobject.TYPE_STRING', 
                    False, True, True, None), 
                ('Cantidad', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Cliente','gobject.TYPE_STRING', False, True, False, None),
                ('Idalbaran','gobject.TYPE_STRING', False, False, False, None))
        for tv in ('tv_entrada', 'tv_salida'):
            utils.preparar_treeview(self.wids[tv], cols)
            self.wids[tv].connect("row-activated", self.abrir_albaran)
            self.wids[tv].get_column(3).get_cell_renderers()[0].set_property(
                'xalign', 1.0)
        self.cambiar_cabecera_columna(self.wids['tv_entrada'], "Proveedor")
        cols = (("Descripción", "gobject.TYPE_STRING", False, True, True,None), 
                ("Entradas", "gobject.TYPE_STRING", False, True, False, None), 
                ("Salidas", "gobject.TYPE_STRING", False, True, False, None), 
                ("Entradas - Salidas", "gobject.TYPE_STRING", 
                    False, True, False, None), 
                ("IDProducto", "gobject.TYPE_INT64", False, True, False, None))
        utils.preparar_listview(self.wids['tv_producto'], cols)
        for numcol in (1, 2, 3):
            self.wids['tv_producto'].get_column(numcol)\
                .get_cell_renderers()[0].set_property('xalign', 1.0)
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
        if boton.name == "b_exportar_as": 
            tv = "tv_salida"
        elif boton.name == "b_exportar_ae": 
            tv = "tv_entrada"
        else:
            tv = "tv_producto"
        tv = self.wids[tv]
        abrir_csv(treeview2csv(tv))

    def abrir_albaran(self, tv, path, view_column):
        """
        Abre el albarán seleccionado en una nueva pantalla.
        Si la fila marcada es una LDV o LDC, abre el albarán 
        al que pertenece.
        """
        self.wids['ventana'].window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        while gtk.events_pending(): gtk.main_iteration(False)
        model = tv.get_model()
        id = model[path][-1]
        tipo, id = id.split(":")
        id = int(id)
        if tipo == "AE":
            albaran = pclases.AlbaranEntrada.get(id)
            import albaranes_de_entrada
            v = albaranes_de_entrada.AlbaranesDeEntrada(albaran, 
                                                        usuario = self.usuario)
        elif tipo == "C":
            comision = pclases.Comision.get(id)
            albaran = comision.albaranSalida
            if albaran != None:
                import albaranes_de_salida
                v = albaranes_de_salida.AlbaranesDeSalida(albaran, 
                                                          usuario=self.usuario)
        elif tipo == "T":
            transporte = pclases.Transporte.get(id)
            albaran = transporte.albaranSalida
            if albaran != None:
                import albaranes_de_salida
                v = albaranes_de_salida.AlbaranesDeSalida(albaran, 
                                                          usuario=self.usuario)
        elif tipo == "LDC":
            ldc = pclases.LineaDeCompra.get(id)
            albaran = ldc.albaranEntrada
            if albaran != None:
                import albaranes_de_entrada
                v = albaranes_de_entrada.AlbaranesDeEntrada(albaran, 
                                                        usuario = self.usuario)
        elif tipo == "AS":
            albaran = pclases.AlbaranSalida.get(id)
            import albaranes_de_salida
            v = albaranes_de_salida.AlbaranesDeSalida(albaran, 
                                                      usuario = self.usuario)
        elif tipo == "LDV": 
            ldv = pclases.LineaDeVenta.get(id)
            albaran = ldv.albaranSalida
            if albaran != None:
                import albaranes_de_salida
                v = albaranes_de_salida.AlbaranesDeSalida(albaran, 
                                                          usuario=self.usuario)
        self.wids['ventana'].window.set_cursor(None)

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, items, comisiones, transportes):
    	"""
        Rellena el model con los items de la consulta
        """        
    	models = self.wids['tv_salida'].get_model()
    	models.clear()
    	modele = self.wids['tv_entrada'].get_model()
    	modele.clear()
    	modelp = self.wids['tv_producto'].get_model()
    	modelp.clear()
        total_entrada = total_salida = 0.0
        euros_entrada = euros_salida = 0.0
        por_producto = {}   
            # Diccionario de productos cuyos valores son 
            # una lista [entradas, salidas]
    	for i in items:
            try:
                if i.cliente == None:
                    cliente = '-'
                else:
                    cliente = i.cliente.nombre
            except AttributeError:
                if i.proveedorID == None:
                    cliente = "-"
                else:
                    cliente = i.proveedor.nombre
            if isinstance(i, pclases.AlbaranSalida):
                total_salida += 1
                padre = models.append(None, 
                                      (utils.str_fecha(i.fecha),
                                       i.numalbaran,
                                       "", 
                                       "", 
                                       cliente,
                                       "AS:%s" % (i.id)))
                for ldv in i.lineasDeVenta:
                    if ldv.facturaVenta == None or ldv.prefactura == None:
                        models.append(padre, ("", 
                                              "", 
                                              ldv.producto.descripcion, 
                                              utils.float2str(ldv.cantidad), 
                                              "", 
                                              "LDV:%d" % ldv.id))
                        p = ldv.producto
                        euros_salida += ldv.get_subtotal(iva = True)
                        if p not in por_producto:
                            por_producto[p] = [0, 0]
                        por_producto[p][1] += ldv.cantidad
            elif isinstance(i, pclases.AlbaranEntrada):
                total_entrada += 1
                padre = modele.append(None, 
                                      (utils.str_fecha(i.fecha),
                                       i.numalbaran,
                                       "", 
                                       "", 
                                       cliente,
                                       "AE:%s" % (i.id)))
                for ldc in i.lineasDeCompra:
                    if ldc.facturaCompra == None:
                        modele.append(padre, ("", 
                                              "", 
                                              ldc.productoCompra.descripcion, 
                                              utils.float2str(ldc.cantidad), 
                                              "", 
                                              "LDC:%d" % ldc.id))
                        euros_entrada += ldc.get_subtotal(iva = True)
                        p = ldc.productoCompra
                        if p not in por_producto:
                            por_producto[p] = [0, 0]
                        por_producto[p][0] += ldc.cantidad
        for c in comisiones:
            total_entrada += 1
            modele.append(None, 
                          (utils.str_fecha(c.fecha), 
                           c.concepto, 
                           "", 
                           "", 
                           c.cliente.proveedor.nombre, 
                           "C:%d" % (c.id)))
            euros_entrada += c.precio
        for t in transportes:
            total_entrada += 1
            modele.append(None, 
                          (utils.str_fecha(t.fecha), 
                           "%s (Albarán %s)" % (t.concepto, 
                                                t.albaranSalida.numalbaran), 
                           "", 
                           "", 
                           t.proveedor.nombre, 
                           "T:%d" % (t.id)))
            euros_entrada += t.precio
        for p in por_producto:
            modelp.append((p.descripcion, 
                           utils.float2str(por_producto[p][0]), 
                           utils.float2str(por_producto[p][1]), 
                           utils.float2str(
                                por_producto[p][0] - por_producto[p][1]), 
                           p.id
                          ))
        self.wids['e_total_entrada'].set_text("%d " % total_salida)
        self.wids['e_total_salida'].set_text("%d " % total_entrada)
        self.wids['e_euros_entrada'].set_text(utils.float2str(euros_entrada))
        self.wids['e_euros_salida'].set_text(utils.float2str(euros_salida))
        
    def set_inicio(self,boton):
        try:
            fini = map(int, self.inicio.split("/"))[::-1]
        except:
            fini = None
        temp = utils.mostrar_calendario(fecha_defecto = fini, padre = self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
        self.inicio = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])

    def set_fin(self,boton):
        try:
            ffin = map(int, self.fin.split("/"))[::-1]
        except:
            ffin = None
        temp = utils.mostrar_calendario(fecha_defecto = ffin, 
                                        padre = self.wids['ventana'])
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

    def cambiar_cabecera_columna(self, tv, txt):
        """
        Cambia la cabecera de la columna destinada a Cliente/Proveedor 
        por el texto recibido.
        """
        col = tv.get_column(2)
        col.set_title(txt)

    def buscar(self,boton):
        """
        Dadas fecha de inicio y de fin, lista todos los albaranes
        pendientes de facturar.
        """
        self.resultado = []
        self.comisiones = []
        self.transportes = []
        selfinicio = self.inicio and utils.parse_fecha("/".join(self.inicio.split("/")[::-1])) or None
        selffin = utils.parse_fecha("/".join(self.fin.split("/")[::-1]))
        if not selfinicio:
            albaranesentrada = pclases.AlbaranEntrada.select(pclases.AlbaranEntrada.q.fecha <= selffin, orderBy = 'fecha')
        else:
            albaranesentrada = pclases.AlbaranEntrada.select(sqlobject.AND(pclases.AlbaranEntrada.q.fecha >= selfinicio,
                                                                   pclases.AlbaranEntrada.q.fecha <= selffin), 
                                                     orderBy='fecha')
        for proveedor in pclases.Proveedor.select():
            if not selfinicio:
                self.comisiones += [c for c in proveedor.get_comisiones_pendientes_de_facturar() 
                                    if c.fecha <= selffin and c not in self.comisiones]
                self.transportes += [t for t in proveedor.get_transportes_pendientes_de_facturar() 
                                     if t.fecha <= selffin and t not in self.transportes] 
            else:
                for c in proveedor.get_comisiones_pendientes_de_facturar():
                    if selfinicio <= c.fecha <= selffin and c not in self.comisiones:
                        self.comisiones.append(c)
                for t in proveedor.get_transportes_pendientes_de_facturar():
                    if selfinicio <= t.fecha <= selffin and t not in self.transportes:
                        self.transportes.append(t)
        if not selfinicio:
            albaranessalida = pclases.AlbaranSalida.select(pclases.AND(pclases.AlbaranSalida.q.fecha <= selffin, 
                                                                 pclases.AlbaranSalida.q.facturable == True), 
                                                     orderBy = 'fecha')
        else:
            albaranessalida = pclases.AlbaranSalida.select(sqlobject.AND(pclases.AlbaranSalida.q.fecha >= selfinicio,
                                                                   pclases.AlbaranSalida.q.fecha <= selffin, 
                                                                   pclases.AlbaranSalida.q.facturable == True), 
                                                     orderBy='fecha')
        for a in albaranessalida:
            total_lineas = len(a.lineasDeVenta)
            if a.contar_lineas_facturadas() < total_lineas: 
                self.resultado.append(a)
        for a in albaranesentrada:
            total_lineas = len(a.lineasDeCompra)
            if a.contar_lineas_facturadas() < total_lineas: 
                self.resultado.append(a)
        self.resultado.sort(self.por_fecha)
        self.comisiones.sort(self.por_fecha)
        self.transportes.sort(self.por_fecha)
        self.rellenar_tabla(self.resultado, self.comisiones, self.transportes)
        self.wids['tv_producto'].get_columns()[0].set_expand(True)

    def imprimir(self,boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        import sys, os
        sys.path.append(os.path.join("..", "informes"))
        from treeview2pdf import treeview2pdf
        from informes import abrir_pdf
        if not self.inicio:
            fechaInforme = 'Hasta '+utils.str_fecha(time.strptime(self.fin,"%Y/%m/%d"))
        else:
            fechaInforme = utils.str_fecha(time.strptime(self.inicio,"%Y/%m/%d"))+' - '+utils.str_fecha(time.strptime(self.fin,"%Y/%m/%d"))
        abrir_pdf(treeview2pdf(self.wids['tv_entrada'], 
                               titulo = "Albaranes de entrada pendientes de facturar", 
                               fecha = fechaInforme))
        abrir_pdf(treeview2pdf(self.wids['tv_salida'], 
                               titulo = "Albaranes de salida pendientes de facturar", 
                               fecha = fechaInforme))
        abrir_pdf(treeview2pdf(self.wids['tv_producto'], 
                               titulo = "Pendiente de facturar por producto", 
                               fecha = fechaInforme))

if __name__ == '__main__':
    t = ConsultaAlbaranesPorFacturar()


