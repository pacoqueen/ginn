#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2014  Francisco José Rodríguez Bogado,                   #
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
## consulta_ventas_por_producto.py --
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 26 de julio de 2007 -> Inicio
## 7 de marzo de 2014 -> Rediseño.
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
import mx.DateTime

class ConsultaVentasPorProducto(Ventana):

    def __init__(self, objeto = None, usuario = None):
        self.usuario = usuario
        Ventana.__init__(self, 'consulta_ventas_por_producto.glade', 
                         objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       'b_exportar/clicked': self.exportar}
        self.add_connections(connections)
        cols_fib = (
            ('Producto', 'gobject.TYPE_STRING', False, True, True, None),
            ('Cantidad', 'gobject.TYPE_STRING', False, True, False, None),
            ('Cliente', 'gobject.TYPE_STRING', False, True, False, None),
            ('Fecha', 'gobject.TYPE_STRING', False, True, False, None),
            ('Albarán', 'gobject.TYPE_STRING', False, True, False, None),
            ('A', 'gobject.TYPE_STRING', False, True, False, None),
            ('B', 'gobject.TYPE_STRING', False, True, False, None),
            ('C', 'gobject.TYPE_STRING', False, True, False, None),
            ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
        cols_gtx = ()
        cols_otros = ()



        utils.preparar_treeview(self.wids['tv_datos'], cols)
        self.wids['tv_datos'].connect("row-activated", self.abrir_producto_albaran_o_abono)
        self.wids['tv_datos'].get_column(1).get_cell_renderers()[0].set_property('xalign', 1) 
        self.wids['tv_datos'].get_column(2).get_cell_renderers()[0].set_property('xalign', 1) 
        self.wids['tv_datos'].get_column(3).get_cell_renderers()[0].set_property('xalign', 0.5) 
        self.wids['tv_datos'].get_column(5).get_cell_renderers()[0].set_property('xalign', 1) 
        self.wids['tv_datos'].get_column(6).get_cell_renderers()[0].set_property('xalign', 1) 
        self.wids['tv_datos'].get_column(7).get_cell_renderers()[0].set_property('xalign', 1) 
        fin = mx.DateTime.localtime()
        inicio = mx.DateTime.localtime() - mx.DateTime.oneWeek
        self.wids['e_fechainicio'].set_text(utils.str_fecha(inicio))
        self.wids['e_fechafin'].set_text(utils.str_fecha(fin))
        gtk.main()
    
    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        tv = self.wids['tv_datos']
        abrir_csv(treeview2csv(tv))

    def abrir_producto_albaran_o_abono(self, tv, path, view_column):
        """
        Si la fila seleccionada es una tarifa, abre la tarifa. Si es 
        un producto, abre el producto.
        """
        model = tv.get_model()
        tipo, ide = model[path][-1].split(":")
        try:
            ide = int(ide)
        except:
            txt = "%sconsulta_ventas_por_producto::abrir_producto_albaran_o_abono -> Excepción al convertir ID a entero: (tipo %s) %s." % (self.usuario and self.usuario + ": " or "", tipo, id)
            print txt
            self.logger.error(txt)
        else:
            if tipo == "PV":        # ProductoVenta 
                pv = pclases.ProductoVenta.get(ide)
                if pv.es_rollo():
                    from formularios import productos_de_venta_rollos
                    v = productos_de_venta_rollos.ProductosDeVentaRollos(pv, usuario = self.usuario)  # @UnusedVariable
                elif pv.es_bala() or pv.es_bala_cable() or pv.es_bigbag():
                    from formularios import productos_de_venta_balas
                    v = productos_de_venta_balas.ProductosDeVentaBalas(pv, usuario = self.usuario)  # @UnusedVariable
                elif pv.es_especial():
                    from formularios import productos_de_venta_especial
                    v = productos_de_venta_especial.ProductosDeVentaEspecial(pv, usuario = self.usuario)  # @UnusedVariable
            elif tipo == "PC": 
                pc = pclases.ProductoCompra.get(ide)
                from formularios import productos_compra
                v = productos_compra.ProductosCompra(pc, usuario = self.usuario)  # @UnusedVariable
            elif tipo == "LDV":
                ldv = pclases.LineaDeVenta.get(ide)
                alb = ldv.albaranSalida
                from formularios import albaranes_de_salida
                v = albaranes_de_salida.AlbaranesDeSalida(alb, usuario = self.usuario)  # @UnusedVariable
            elif tipo == "LDD": 
                ldd = pclases.LineaDeDevolucion.get(ide)
                adeda = ldd.lbaranDeEntradaDeAbono
                abono = adeda.abono
                from formularios import abonos_venta
                v = abonos_venta.AbonosVenta(abono, usuario = self.usuario)  # @UnusedVariable

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, ldvs, ldds):
        """
        Rellena el model con los items de la consulta.
        ldvs es una lista de líneas de venta.
        ldds es una lista de líneas de devolución.
        Recorre ambas listas y las inserta en función del producto de cada 
        una de ellas. Para ello va guardando en un diccionario el producto, 
        la fila que ocupa (padre de la que se esté insertando en ese 
        momento) y la cantidad total del mismo.
        """ 
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        i = 0.0
        tot = len(ldvs) + len(ldds)
        vpro.set_valor(i / (tot + 1), "Analizando %s..." % ("")) #Por si tot==0
        model = self.wids['tv_datos'].get_model()
        model.clear()
        total_otros = 0.0
        total_metros = 0.0
        total_kilos = 0.0
        productos = {}
        for ldv in ldvs:
            i += 1
            vpro.set_valor(i / tot, "Analizando %s..." % (
                ldv.albaranSalida.numalbaran))
            p = ldv.producto
            if isinstance(p, pclases.ProductoVenta):
                tipo = "PV"
                cantidades = ldv.get_cantidad_albaraneada_por_calidad()
                cantidad_albaraneada = cantidades['total']['m²']
                if not cantidad_albaraneada: # ¿Será fibra? Si es gtx también 
                    cantidad_albaraneada = cantidades['total']['kg'] # será 0
# TODO: PORASQUI: Al final voy a tener que rediseñar la ventana completa. No hay manera de mezclar metros, kilos, otras unidades para los productos de compra, etc. y que quede más o menos homogéneo. 
            elif isinstance(p, pclases.ProductoCompra):
                tipo = "PC"
                cantidad_albaraneada = ldv.get_cantidad_albaraneada()
            else:
                tipo = "?"
                txt = "%sconsulta_ventas_por_producto::rellenar_tabla -> Tipo de producto desconocido: LDV ID: %d, Representación del objeto producto: %s" % (self.usuario and self.usuario + ": " or "", ldv.id, p)
                print txt
                self.logger.error(txt)
                cantidad_albaraneada = 0
            if p not in productos:
                fila = model.append(None, (p.descripcion, 
                                           "", 
                                           "", 
                                           "", 
                                           "", 
                                           "", 
                                           "", 
                                           "", 
                                           "%s:%d" % (tipo, p.id)))
                productos[p] = [fila, cantidad_albaraneada]
            else:
                fila = productos[p][0]
                if not ldv.albaranSalida.es_de_movimiento():
                    productos[p][1] += cantidad_albaraneada
            if tipo == "PV":
                cantidad = cantidad_albaraneada
                # TODO: PORASQUI: A ver cómo me las arreglo para distinguir
                # A, B y C de la cantidad albaraneada sin que tarde todavía 
                # más. Que actualmente ya es demasiado.
                A = B = C = ""
                if (p.es_bala() or p.es_bigbag() or p.es_bala_cable() 
                        or p.es_rollo_c() or p.es_caja()):
                    total_kilos += cantidad
                elif p.es_rollo():
                    total_metros += cantidad
                elif p.es_especial():
                    total_otros += cantidad
            elif tipo == "PC":
                cantidad = cantidad_albaraneada 
                total_otros += cantidad * ldv.precio
                A = B = C = "N/A"
            else:
                cantidad = 0
                A = B = C = "N/A"
            model.append(fila, ("", utils.float2str(cantidad), 
                                    ldv.albaranSalida.cliente 
                                        and ldv.albaranSalida.cliente.nombre 
                                        or "", 
                                    utils.str_fecha(ldv.albaranSalida.fecha),
                                    ldv.albaranSalida.numalbaran, 
                                    A, 
                                    B, 
                                    C, 
                                    "LDV:%d" % (ldv.id)))
            if ldv.albaranSalida.es_de_movimiento():
                # Añado la misma línea pero en negativo, de ese modo se 
                # anularán. La consulta no es por almacén, sino general.
                model.append(fila, ("", utils.float2str(-cantidad), 
                                    ldv.albaranSalida.cliente 
                                        and ldv.albaranSalida.cliente.nombre 
                                        or "", 
                                    utils.str_fecha(ldv.albaranSalida.fecha),
                                    ldv.albaranSalida.numalbaran, 
                                    "", 
                                    "", 
                                    "", 
                                    "LDV:%d" % (ldv.id)))
        for ldd in ldds:
            i += 1
            vpro.set_valor(i / tot, "Analizando %s..." % (
                ldd.abono.numabono))
            p = ldd.producto
            tipo = "PV" # De momento los abonos, más concretamente las LDD, 
            # no soportan otra cosa que no sea un (artículo de) ProductoVenta.
            if p not in productos:
                fila = model.append(None, 
                                    (p.descripcion, 
                                     "", 
                                     "", 
                                     "", 
                                     "", 
                                     "", 
                                     "", 
                                     "", 
                                     "%s:%d" % (tipo, p.id)))
                productos[p] = [fila, ldv.get_cantidad_albaraneada()]
            else:
                fila = productos[p][0]
                productos[p][1] += ldv.get_cantidad_albaraneada()
            cantidad = ldd.cantidad
            if (p.es_bala() or p.es_bigbag() or p.es_bala_cable() 
                    or p.es_rollo_c() or p.es_caja()):
                total_kilos += cantidad
            elif p.es_rollo():
                total_metros += cantidad
            elif p.es_especial():
                total_otros += cantidad * ldd.precio
            model.append(fila, 
                    ("", 
                     utils.float2str(cantidad), 
                     ldd.abono.cliente and ldd.abono.cliente.nombre or "", 
                     utils.str_fecha(ldd.albaranDeEntradaDeAbono.fecha),
                     ldd.albaranDeEntradaDeAbono.numalbaran, 
                     "", 
                     "", 
                     "", 
                     "LDD:%d" % (ldd.id)))
        # Actualizo los totales de los productos en las filas del TreeView
        total_metros_en_kilos_teoricos = 0.0
        i = 0.0
        tot = len(productos.keys())
        for p in productos:
            i += 1
            vpro.set_valor(i/tot, "Actualizando totales...")
            cantidad = "%s %s" % (utils.float2str(productos[p][1]), p.unidad)
            try:
                if p.es_rollo():
                    metros_en_kilos_teoricos = (
                            (productos[p][1] * p.camposEspecificosRollo.gramos)
                            / 1000.0)
                    total_metros_en_kilos_teoricos += metros_en_kilos_teoricos
                    cantidad += " (%s kg)" % utils.float2str(
                            metros_en_kilos_teoricos)
                # TODO: FIXME: Esto de los kilos teóricos... con rollos B y tal... Mal, ¿eh?
            except AttributeError:  # It's Easier to Ask Forgiveness than Permission (EAFP)
                pass
            fila = productos[p][0]
            model[fila][1] = cantidad
        self.wids['e_total_otros'].set_text(
                "%s € " % (utils.float2str(total_otros)))
        self.wids['e_total_kilos'].set_text(
                "%s kg" % (utils.float2str(total_kilos)))
        self.wids['e_total_metros'].set_text(
                "%s m² (%s kg)" % (
                    utils.float2str(total_metros), 
                    utils.float2str(total_metros_en_kilos_teoricos)))
        vpro.ocultar()

    def set_inicio(self, boton):
        temp = utils.mostrar_calendario(fecha_defecto = utils.parse_fecha(self.wids['e_fechainicio'].get_text()), 
                                        padre = self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))

    def set_fin(self, boton):
        temp = utils.mostrar_calendario(fecha_defecto = utils.parse_fecha(self.wids['e_fechafin'].get_text()), 
                                        padre = self.wids['ventana'])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))

    def buscar(self, boton):
        """
        A partir de las fechas de inicio y fin de la ventana busca las LDVs y LDDs de 
        albaranes de salida y albaranes de entrada de abonos entre ellas.
        Rellena el TreeView con el resultado de la búsqueda.
        """
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        fini = utils.parse_fecha(self.wids['e_fechainicio'].get_text())
        ffin = utils.parse_fecha(self.wids['e_fechafin'].get_text())
        vpro.set_valor(0.3, "Buscando albaranes de salida...")
        albs = pclases.AlbaranSalida.select(pclases.AND(
                                    pclases.AlbaranSalida.q.fecha >= fini, 
                                    pclases.AlbaranSalida.q.fecha < ffin), 
                                            orderBy = "fecha")
        ldvs = []
        for a in albs:
            for ldv in a.lineasDeVenta: # Lo hago así para cargar aquí todo el peso de traer las LDVs, y así aligero el rellenar_tabla.
                ldvs.append(ldv)
        vpro.set_valor(0.6, "Analizando albaranes y abonos...")
        adedas = pclases.AlbaranDeEntradaDeAbono.select(pclases.AND(
                            pclases.AlbaranDeEntradaDeAbono.q.fecha >= fini, 
                            pclases.AlbaranDeEntradaDeAbono.q.fecha < ffin), 
                                                        orderBy = "fecha")
        ldds = []
        for a in adedas:
            for ldd in a.lineasDeDevolucion:
                ldds.append(ldd)
        vpro.set_valor(0.9, "Actualizando ventana...")
        vpro.ocultar()
        self.rellenar_tabla(ldvs, ldds)

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe.
        """
        from informes.treeview2pdf import treeview2pdf
        from formularios.reports import abrir_pdf
        strfecha = "%s - %s" % (self.wids['e_fechainicio'].get_text(), 
                                self.wids['e_fechafin'].get_text())
        resp = utils.dialogo(titulo = "¿IMPRIMIR DESGLOSE?", 
                             texto = "Puede imprimir únicamente los productos"
                                     " o toda la información de la ventana.\n"
                                     "¿Desea imprimir toda la información "
                                     "desglosada?", 
                             padre = self.wids['ventana'])
        tv = clone_treeview(self.wids['tv_datos'])  # Para respetar el orden 
        # del treeview original y que no afecte a las filas de totales que 
        # añado después. Si las añado al original directamente se mostrarán 
        # en el orden que correspondería en lugar de al final.
        model = tv.get_model()
        fila_sep = model.append(None, ("===",) * 9)
        fila_total_gtx = model.append(None, ("Total m² geotextiles", self.wids['e_total_metros'].get_text(), "", "", "", "", "", "", ""))
        fila_total_fibra = model.append(None, ("Total kg fibra", self.wids['e_total_kilos'].get_text(), "", "", "", "", "", "", ""))
        fila_total_otros = model.append(None, ("Total € otros", self.wids['e_total_otros'].get_text(), "", "", "", "", "", "", ""))
        if resp:
            tv.expand_all()
            while gtk.events_pending(): gtk.main_iteration(False)
        else:
            tv.collapse_all()
            while gtk.events_pending(): gtk.main_iteration(False)
            tv = convertir_a_listview(tv)
            # Para este caso particular me sobran las columnas de albarán y eso
            tv.remove_column(tv.get_columns()[-4])
            tv.remove_column(tv.get_columns()[-4])
            tv.remove_column(tv.get_columns()[-4])
        abrir_pdf(treeview2pdf(tv, 
            titulo = "Salidas de almacén agrupadas por producto", 
            fecha = strfecha))
        model.remove(fila_sep)
        model.remove(fila_total_gtx)
        model.remove(fila_total_fibra)
        model.remove(fila_total_otros)

def clone_treeview(otv):
    """
    Clona un treeview en uno nuevo.
    """
    ntv = gtk.TreeView()
    ntv.set_name(otv.get_name())
    omodel = otv.get_model()
    tipos = [omodel.get_column_type(i) for i in range(omodel.get_n_columns())]
    nmodel = gtk.TreeStore(*tipos)
    ntv.set_model(nmodel)
    for fila_nivel_1 in omodel:
        def agregar_fila(model, padre, fila):
            iterpadre = model.append(padre, fila)
            if hasattr(fila, 'iterchildren'):
                for hijo in fila.iterchildren():
                    agregar_fila(model, iterpadre, hijo)
        agregar_fila(nmodel, None, fila_nivel_1)
    for ocol in otv.get_columns():
        title = ocol.get_title()
        ocell = ocol.get_cell_renderers()[0]
        ncell = type(ocell)()
        ncol = gtk.TreeViewColumn(title, ncell)
        ncol.set_data("q_ncol", ocol.get_data("q_ncol"))
        ncol.get_cell_renderers()[0].set_property('xalign', 
                ocol.get_cell_renderers()[0].get_property('xalign')) 
        ntv.append_column(ncol)
    return ntv

def convertir_a_listview(otv):
    """
    Convierte el TreeView en un ListView con los mismos datos que el original y 
    lo devuelve.
    """
    ntv = gtk.TreeView()
    ntv.set_name(otv.get_name())
    omodel = otv.get_model()
    tipos = [omodel.get_column_type(i) for i in range(omodel.get_n_columns())]
    nmodel = gtk.ListStore(*tipos)
    ntv.set_model(nmodel)
    for fila in omodel:
        nmodel.append([e for e in fila])
    for ocol in otv.get_columns():
        title = ocol.get_title()
        ocell = ocol.get_cell_renderers()[0]
        ncell = type(ocell)()
        ncol = gtk.TreeViewColumn(title, ncell)
        ncol.set_data("q_ncol", ocol.get_data("q_ncol"))
        ncol.get_cell_renderers()[0].set_property('xalign', 
                ocol.get_cell_renderers()[0].get_property('xalign')) 
        ntv.append_column(ncol)
    return ntv

if __name__ == '__main__':
    t = ConsultaVentasPorProducto()

