#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado,                   #
#                          (pacoqueen@users.sourceforge.net                   #
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
## valor_almacen.py - Valor de productos de compra en almacén.
###################################################################
## 
###################################################################

import sys, os
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, mx, mx.DateTime
try:
    import pclases
    from seeker import VentanaGenerica 
except ImportError:
    sys.path.append(os.path.join('..', 'framework'))
    import pclases
    from seeker import VentanaGenerica 
from utils import _float as float
import ventana_progreso
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes

class ValorAlmacen(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'valor_almacen.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_actualizar/clicked': 
                        lambda *a, **kw: self.rellenar_widgets(),
                       'b_exportar/clicked': self.exportar_a_csv, 
                       'b_imprimir/clicked': self.imprimir,  
                       'b_print2/clicked': self.imprimir_totales
                      }  
        self.add_connections(connections)
        self.inicializar_ventana()
        self.rellenar_widgets()
        gtk.main()

    def exportar_a_csv(self, boton):
        """
        Exporta el TreeView de detalle a CSV.
        """
        tv = self.wids['tv_detalle']
        from treeview2csv import treeview2csv
        from informes import abrir_csv
        nomarchivocsv = treeview2csv(tv)
        abrir_csv(nomarchivocsv)

    def imprimir(self, boton):
        """
        Exporta a PDF el TreeView de detalle.
        """
        tv = self.wids['tv_detalle']
        from treeview2pdf import treeview2pdf
        from informes import abrir_pdf
        strfecha = "%s - %s" % (utils.str_fecha(mx.DateTime.localtime()), 
                                utils.str_hora(mx.DateTime.localtime()))
        abrir_pdf(treeview2pdf(tv, 
            titulo = "Valoración de productos de compra en almacén.",
            fecha = strfecha, 
            apaisado = False, 
            numcols_a_totalizar = [-1]))

    def imprimir_totales(self, boton):
        """
        Exporta a PDF el TreeView de detalle.
        """
        tv = self.wids['tv_datos']
        from treeview2pdf import treeview2pdf
        from informes import abrir_pdf
        strfecha = "%s - %s" % (utils.str_fecha(mx.DateTime.localtime()), utils.str_hora(mx.DateTime.localtime()))
        abrir_pdf(treeview2pdf(tv, 
            titulo = "Valoración de productos de compra en almacén. TOTALES.",
            fecha = strfecha, 
            apaisado = False))

    def es_diferente(self):
        """
        Devuelve True si algún valor en ventana difiere de 
        los del objeto.
        """
        return True # Para que el botón de actualizar siempre esté activo.
    
    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        cols = (('Concepto', 'gobject.TYPE_STRING', False, False, False, None),
                ("Valor en euros", "gobject.TYPE_STRING", False, False, False, None), 
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
                # La última columna (oculta en la Vista) siempre es el id.
        utils.preparar_listview(self.wids['tv_datos'], cols)
        cols = [("Código", "gobject.TYPE_STRING", False, True, True, None), 
                ("Descripción", "gobject.TYPE_STRING", 
                    False, True, False, None), 
                ("Existencias", "gobject.TYPE_STRING", 
                    False, True, False, None), 
                ("Precio valoración", "gobject.TYPE_STRING", 
                    False, True, False, None), 
                ("Total", "gobject.TYPE_STRING", False, True, True, None), 
                ("ID", "gobject.TYPE_INT", False, False, False, None)]
        utils.preparar_listview(self.wids['tv_detalle'], cols)
        tv = self.wids['tv_detalle']
        for col in tv.get_columns()[2:5]:
            for cell in col.get_cell_renderers():
                cell.set_property("xalign", 1.0)
            col.set_alignment(0.5)

    def rellenar_widgets(self):
        """
        Introduce la información de la cuenta actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        self.rellenar_tabla_datos()

    def rellenar_tabla_datos(self):
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        dde = pclases.DatosDeLaEmpresa.select()[0]
        vpro.set_valor(0.0, 'Configuración de empresa...')
        iva_empresa = dde.iva
        if dde.recargoEquivalencia:
            iva_empresa += 0.04
        filas = [("Precio defecto", -1), 
                 ("Precio valoración", -2), 
                 ("Valoración + %d%% IVA" % (iva_empresa * 100), -3)]
        tarifas = pclases.Tarifa.select(orderBy = "nombre")
        vpro.set_valor(0.2, 'Tarifas...')
        for t in tarifas:
            if t.esta_vigente():
                filas.append((t.nombre, t.id))
                filas.append((t.nombre + " + 18% IVA", 0))
        model = self.wids['tv_datos'].get_model()
        model.clear()
        for concepto, id in filas:
            if id == -1:
                vpro.set_valor(0.4, 'Valorando a precio defecto...')
                valoracion = valorar_a_precio_defecto()
            elif id == -2:
                vpro.set_valor(0.6, 'Valorando a precio valoración...')
                valoracion=valorar_a_precio_valoracion(self.wids['tv_detalle'])
            elif id == -3:  # HACK
                valoracion *= 1 + iva_empresa
                # El valoración de la iteración anterior, es decir, según la 
                # función de valoración de cada producto.
            elif id > 0:
                tarifa = pclases.Tarifa.get(id)
                vpro.set_valor(0.6, 'Valorando a tarifa %s...' % tarifa.nombre)
                valoracion = valorar_segun_tarifa(tarifa)
            else:           # HACK
                valoracion *= 1.18  # De nuevo, la valoración de la iteración 
                # anterior. Es decir, la de esta tarifa pero sin IVA.
            model.append((concepto, 
                          utils.float2str(valoracion), 
                          0))
        vpro.ocultar()

def valorar_a_precio_defecto():
    """
    Valora todos los productos de compra que tienen existencias en almacén 
    a precio por defecto (=precio de costo en la mayoría de las instalaciones).
    """
    suma = pclases.ProductoCompra.select(pclases.AND(
                pclases.ProductoCompra.q.existencias != 0, 
                pclases.ProductoCompra.q.obsoleto == False,
                pclases.ProductoCompra.q.controlExistencias == True)
            ).sumFloat("existencias * precio_defecto")
    return suma

def valorar_a_precio_valoracion(tv):
    """
    Valora todos los productos de compra con existencias distintas a cero 
    (OJO: Incluye existencias negativas) según el precio de valoración 
    definido (precio por defecto, precio medio ponderado, etc.).
    """
    pcs = pclases.ProductoCompra.select(pclases.AND(
            pclases.ProductoCompra.q.controlExistencias == True, 
            pclases.ProductoCompra.q.obsoleto == False,
            pclases.ProductoCompra.q.existencias != 0))
    model = tv.get_model()
    tv.freeze_child_notify()
    tv.set_model(None)
    model.clear()
    suma = 0.0
    for pc in pcs:
        precio_valoracion = pc.get_precio_valoracion()
        valoracion = precio_valoracion * pc.existencias
        model.append((pc.codigo, 
                      pc.descripcion, 
                      utils.float2str(pc.existencias,precision=2,autodec=True),
                      utils.float2str(precio_valoracion, precision = 2), 
                      utils.float2str(valoracion, precision = 2), 
                      pc.id))
        suma += valoracion
    tv.set_model(model)
    tv.thaw_child_notify()
    return suma

def valorar_segun_tarifa(tarifa):
    """
    Valora todos los productos de compra con existencias distintas a cero 
    (OJO: Incluye existencias negativas) según el precio de venta de la 
    tarifa recibida (precio por defecto, precio medio ponderado, etc.).
    """
    pcs = pclases.ProductoCompra.select(pclases.AND(
            pclases.ProductoCompra.q.controlExistencias == True,
            pclases.ProductoCompra.q.obsoleto == False,
            pclases.ProductoCompra.q.existencias != 0))
    suma = 0.0
    for pc in pcs:
        precio_tarifa = tarifa.obtener_precio(pc, sincronizar = False)
        valoracion = precio_tarifa * pc.existencias
        suma += valoracion
    return suma

    

if __name__ == "__main__":
    p = ValorAlmacen()

