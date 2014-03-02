#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2014  Francisco José Rodríguez Bogado                    #
#                          <frbogado@geotexan.com>                            #
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
## consulta_existencias_por_tipo.py
###################################################################
## NOTAS:
##  
###################################################################
## 
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk, time
from framework import pclases
from collections import defaultdict
from formularios.ventana_progreso import VentanaProgreso

class ConsultaExistenciasPorTipo(Ventana):
        
    def __init__(self, objeto = None, usuario = None):
        self.usuario = usuario
        Ventana.__init__(self, 'consulta_existencias_por_tipo.glade', 
                         objeto, self.usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_actualizar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_exportar/clicked': self.exportar, 
                       'cb_almacen/changed': self.buscar} 
        self.add_connections(connections)
        for nomtv in ("tv_fibra", "tv_gtx", "tv_cemento"):
            cols = [
                ('Producto', 'gobject.TYPE_STRING', False, True, True, None),#0
                ('A (Kg)', 'gobject.TYPE_STRING', False, True, False, None),
                ('A (#)', 'gobject.TYPE_STRING', False, True, False, None),
                ('B (Kg)', 'gobject.TYPE_STRING', False, True, False, None),
                ('B (#)', 'gobject.TYPE_STRING', False, True, False, None),
                ('C (Kg)', 'gobject.TYPE_STRING', False, True, False, None),
                ('C (#)', 'gobject.TYPE_STRING', False, True, False, None),
                ('Total (Kg)', 'gobject.TYPE_STRING', False, True, False, None),
                ('Total (#)', 'gobject.TYPE_STRING', False, True, False, None),
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None)]#(5)
            if nomtv == "tv_gtx":
                cols.insert(2, 
                  ('A (m²)', 'gobject.TYPE_STRING', False, True, False, None))
                cols.insert(5, 
                  ('B (m²)', 'gobject.TYPE_STRING', False, True, False, None))
                cols.insert(8, 
                  ('C (m²)', 'gobject.TYPE_STRING', False, True, False, None))
                cols.insert(11, 
                  ('Total (m²)', 
                      'gobject.TYPE_STRING', False, True, False, None))
            tv = self.wids[nomtv]
            utils.preparar_listview(tv, cols)
            tv.connect("row-activated", self.abrir_objeto)
            for ncol in range(1, len(cols) - 1):
                col = tv.get_column(ncol)
                col.get_cell_renderers()[0].set_property('xalign', 1.0) 
            col = tv.get_column(0)
            col.set_expand(True)
        almacenes = pclases.Almacen.select(
                pclases.Almacen.q.activo == True, 
                orderBy = "id")
        opciones = [(0, "Todos")] + [(a.id, a.nombre) for a in almacenes]
        utils.rellenar_lista(self.wids['cb_almacen'], opciones)
        utils.combo_set_from_db(self.wids['cb_almacen'], 0)
        gtk.main()
    
    def abrir_objeto(self, tv, path, view_column):
        """
        Abre el producto.
        """
        model = tv.get_model()
        puid = model[path][-1]
        objeto = pclases.getObjetoPUID(puid)
        if objeto.es_rollo() or objeto.es_rollo_c():
            from formularios.productos_de_venta_rollos \
                    import ProductosDeVentaRollos as NuevaVentana
        elif objeto.es_fibra() or objeto.es_bolsa():
            from formularios.productos_de_venta_balas \
                    import ProductosDeVentaBalas as NuevaVentana
        else:
            return  # Si no es nada de lo que pueda abrir, pasando del temita.
        v = NuevaVentana(usuario = self.usuario, objeto = objeto)
    
    def chequear_cambios(self):
        pass

    def buscar(self, boton):
        """
        Busca todos los productos de venta, los clasifica por tipo y 
        genera una estructura de datos que se mostrará después en los TreeView.
        """
        self.productos = defaultdict(lambda: [])
        # productos como propiedad de la clase por si tengo que depurar.
        for pv in pclases.ProductoVenta.select(orderBy = "descripcion"):
            if pv.es_rollo() or pv.es_rollo_c():
                tipo = "gtx"
            elif pv.es_bolsa(): # or pv.es_caja():
                tipo = "cemento"
            elif pv.es_bala() or pv.es_bala_cable() or pv.es_bigbag():
                # Equivale a pv.es_fibra(). O debería.
                tipo = "fibra"
            elif pv.es_especial():
                continue    # Estos los ignoro
            else:
                # ¿Producto vacío, sin descripción ni nada? Casi seguro.
                #raise ValueError, "consulta_existencias_por_tipo::buscar -> "\
                #                  "Producto no es fibra, geotextil ni cemento."
                # TODO: Agregar línea al log o emitir un warning o algo.
                continue
            self.productos[tipo].append(pv)
        totales = self.rellenar_treeviews()
        self.rellenar_totales(totales)

    def rellenar_treeviews(self):
        almacenid = utils.combo_get_value(self.wids['cb_almacen'])
        if almacenid != 0:
            almacen = pclases.Almacen.get(almacenid)
        else:
            almacen = None
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        totales = {'kgA':     {}, 
                   'kgB':     {}, 
                   'kgC':     {}, 
                   'kgTotal': {}, 
                   'mA':      {}, 
                   'mB':      {}, 
                   'mC':      {}, 
                   'mTotal':  {}, 
                   '#A':      {}, 
                   '#B':      {}, 
                   '#C':      {}, 
                   '#Total':  {}
                  }
        i = 0.0
        tot = sum([len(self.productos[k]) for k in self.productos.keys()])
        for nombre_tv in ("tv_fibra", "tv_gtx", "tv_cemento"):
            tv = self.wids[nombre_tv]
            model = tv.get_model()
            model.clear()
            tipo = nombre_tv.split("_")[-1]
            for pv in self.productos[tipo]:
                i += 1
                vpro.set_valor(i / tot, 
                               "Contando existencias de %s (%d) [%s]..." % (
                                    pv.nombre, pv.id, tipo))
                kgA = pv.get_stock_A(almacen = almacen)
                kgB = pv.get_stock_B(almacen = almacen)
                kgC = pv.get_stock_C(almacen = almacen)
                bultosA = pv.get_existencias_A(almacen = almacen)
                bultosB = pv.get_existencias_B(almacen = almacen)
                bultosC = pv.get_existencias_C(almacen = almacen)
                total_kg = pv.get_stock(almacen = almacen, 
                                     contar_defectuosos = True)
                total_bultos = pv.get_existencias(almacen = almacen, 
                                     contar_defectuosos = True)
                if pclases.DEBUG:
                    assert round(kgA + kgB + kgC) == round(
                            total_kg), pv.puid  # XXX 
                    # Esto de arriba, aunque mezcle metros con kilos, no 
                    # debe fallar. Ya que en el total de un producto C, 
                    # A y B se quedan a 0.0. Y al contrario. Si el producto 
                    # no es C, A y B valdrán algo y C siempre es 0.
                    assert round(bultosA + bultosB + bultosC) == round(
                            total_bultos), pv.puid  # XXX 
                if nombre_tv != "tv_gtx":
                    fila = [pv.descripcion, 
                            utils.float2str(kgA), 
                            utils.int2str(bultosA), 
                            utils.float2str(kgB), 
                            utils.int2str(bultosB), 
                            utils.float2str(kgC), 
                            utils.int2str(bultosC), 
                            utils.float2str(total_kg), 
                            utils.int2str(total_bultos), 
                            pv.puid]
                    actualizar_totales(totales, tipo, 
                            kgA, kgB, kgC, total_kg, 
                            bultosA, bultosB, bultosC, total_bultos)
                else:
                    # Los metros ya los tenía calculados. Es lo que devuelve 
                    # el get_stock. Solo que arriba lo he llamado kg*
                    metrosA = kgA
                    metrosB = kgB
                    metrosC = "N/A" # No aplicable. Solo se mide en kilos.
                    kilosA = pv.get_stock_kg_A(almacen = almacen)
                    kilosB = pv.get_stock_kg_B(almacen = almacen)
                    kilosC = kgC    # Ya estaba calculado
                    total_kilos = kilosA + kilosB + kilosC
                    total_metros = metrosA + metrosB
                    # total bultos ya se calcula arriba.
                    fila = [pv.descripcion, 
                            utils.float2str(kilosA), 
                            utils.float2str(metrosA), 
                            utils.int2str(bultosA), 
                            utils.float2str(kilosB), 
                            utils.float2str(metrosB), 
                            utils.int2str(bultosB), 
                            utils.float2str(kilosC), 
                            metrosC,  # No es aplicable. Solo kg. No m² en C.
                            utils.int2str(bultosC), 
                            utils.float2str(total_kilos), 
                            utils.float2str(total_metros), 
                            utils.int2str(total_bultos), 
                            pv.puid]
                    actualizar_totales(totales, tipo, 
                            kilosA, kilosB, kilosC, total_kilos, 
                            bultosA, bultosB, bultosC, total_bultos, 
                            metrosA, metrosB, 0.0, total_metros)
                        # m² de C es "N/A". Le paso un 0 aquí para que no pete.
                model.append(fila)
        vpro.ocultar()
        return totales

    def rellenar_totales(self, totales):
        for tipo_stock in totales:
            for tipo_producto in totales[tipo_stock]:
                nomentry = "e_%s_%s" % (tipo_producto, tipo_stock)
                entry = self.wids[nomentry]
                total = totales[tipo_stock][tipo_producto]
                entry.set_text(utils.float2str(total, autodec = True))
   
    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        pagina_activa = self.wids['nb_tipo'].get_current_page()
        if pagina_activa == 0:
            tv = self.wids['tv_fibra']
        elif pagina_activa == 1: 
            tv = self.wids['tv_gtx']
        elif pagina_activa == 2: 
            tv = self.wids['tv_cemento']
        else:
            return
        abrir_csv(treeview2csv(tv))

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        from formularios import reports
        from informes.treeview2pdf import treeview2pdf
        pagina_activa = self.wids['nb_tipo'].get_current_page()
        almacenid = utils.combo_get_value(self.wids['cb_almacen'])
        if almacenid != 0:
            almacen = pclases.Almacen.get(almacenid)
        else:
            almacen = None
        if pagina_activa == 0:
            tv = self.wids['tv_fibra']
            titulo = "Existencias de productos por tipo: fibra"
        elif pagina_activa == 1: 
            tv = self.wids['tv_gtx']
            titulo = "Existencias de productos por tipo: geotextiles"
        elif pagina_activa == 2: 
            tv = self.wids['tv_cemento']
            titulo = "Existencias de productos por tipo: fibra de cemento"
        else:
            return
        try:
            titulo += " (%s)" % almacen.nombre
        except AttributeError:
            pass
        totales = range(1, tv.get_model().get_n_columns()-1)
        extra_data = []
        reports.abrir_pdf(treeview2pdf(tv, 
                                       titulo = titulo, 
                                       apaisado = False, 
                                       pijama = True, 
                                       numcols_a_totalizar = totales, 
                                       extra_data = extra_data))


def actualizar_totales(totales, tipo_de_producto, kgA, kgB, kgC, kg_total, 
                       bultosA, bultosB, bultosC, bultos_total, 
                       metrosA = None, metrosB = None, metrosC = None, 
                       metros_total = None):
    """
    Actualiza el diccionario de totales.
    tipo_de_producto es 'gtx', 'fibra' o 'cemento'.
    totales es un diccionario organizado por tipo de existencias (kgA, kgB, 
    kgC, kgTotal, etc.) y dentro de éstas, por tipo de producto (fibra, 
    gtx o cemento).
    kgA, kgB, kgC y total son las existencias en sí con las que se actualizará 
    el diccionario en función del tipo de existencias y del tipo de producto.
    """
    for tipo_de_stock, stock_de_ese_tipo in (('kgA', kgA), 
                                             ('kgB', kgB), 
                                             ('kgC', kgC), 
                                             ('kgTotal', kg_total), 
                                             ('mA', metrosA), 
                                             ('mB', metrosB), 
                                             ('mC', metrosC), 
                                             ('mTotal', metros_total), 
                                             ('#A', bultosA), 
                                             ('#B', bultosB), 
                                             ('#C', bultosC), 
                                             ('#Total', bultos_total)):
        if stock_de_ese_tipo is None:
            continue
        try:
            totales[tipo_de_stock][tipo_de_producto] += stock_de_ese_tipo
        except KeyError:
            totales[tipo_de_stock][tipo_de_producto] = stock_de_ese_tipo

if __name__ == '__main__':
    t = ConsultaExistenciasPorTipo()

