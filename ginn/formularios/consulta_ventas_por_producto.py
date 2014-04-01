#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2014  Francisco José Rodríguez Bogado                    #
#                          <pacoqueen@users.sourceforge.net>                  #
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
# consulta_ventas_por_producto.py --                                          #
###############################################################################
# NOTAS:
# * No se hace la distición por almacén. Demasiadas dimensiones van ya con la
#   calidad y tipo de producto.
###############################################################################
# Changelog:
# 26 de julio de 2007 -> Inicio
# 7 de marzo de 2014 -> Rediseño.
###############################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
import mx.DateTime
from collections import defaultdict


class ConsultaVentasPorProducto(Ventana):

    def __init__(self, objeto=None, usuario=None):
        self.usuario = usuario
        Ventana.__init__(self, 'consulta_ventas_por_producto.glade',
                         objeto, usuario=usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin,
                       'b_exportar/clicked': self.exportar,
                       'e_fechainicio/focus-out-event': act_fecha,
                       'e_fechafin/focus-out-event': act_fecha,
                       'b_map/clicked': self.exportar_a_html}
        self.add_connections(connections)
        # TreeViews de fibra y cemento
        cols = [
            ('Producto', 'gobject.TYPE_STRING', False, True, True, None),
            ('kg A', 'gobject.TYPE_STRING', False, True, False, None),
            ('# A', 'gobject.TYPE_STRING', False, True, False, None),
            ('kg B', 'gobject.TYPE_STRING', False, True, False, None),
            ('# B', 'gobject.TYPE_STRING', False, True, False, None),
            ('kg C', 'gobject.TYPE_STRING', False, True, False, None),
            ('# C', 'gobject.TYPE_STRING', False, True, False, None),
            ('Total kg', 'gobject.TYPE_STRING', False, True, False, None),
            ('Total #', 'gobject.TYPE_STRING', False, True, False, None),
            ('PUID', 'gobject.TYPE_STRING', False, False, False, None)]
        for tv in (self.wids['tv_fibra'], self.wids['tv_cem']):
            utils.preparar_treeview(tv, cols)
            tv.connect("row-activated", self.abrir_producto_albaran_o_abono)
            for n in range(1, 9):
                tv.get_column(n).get_cell_renderers()[0].set_property(
                    'xalign', 1)
        # TreeView de geotextiles
        cols.insert(1,
                    ('m² A', 'gobject.TYPE_STRING', False, True, False, None))
        cols.insert(4,
                    ('m² B', 'gobject.TYPE_STRING', False, True, False, None))
        cols.insert(7,
                    ('m² C', 'gobject.TYPE_STRING', False, True, False, None))
        cols.insert(10,
                    ('Total m²', 'gobject.TYPE_STRING', False, True, False,
                     None))
        utils.preparar_treeview(self.wids['tv_gtx'], cols)
        self.wids['tv_gtx'].connect("row-activated",
                                    self.abrir_producto_albaran_o_abono)
        tv = self.wids['tv_gtx']
        for n in range(1, 13):
            tv.get_column(n).get_cell_renderers()[0].set_property('xalign', 1)
        # TreeView de otros
        cols = [
            ('Producto', 'gobject.TYPE_STRING', False, True, True, None),
            ('Cantidad', 'gobject.TYPE_STRING', False, True, False, None),
            ('PUID', 'gobject.TYPE_STRING', False, False, False, None)]
        utils.preparar_treeview(self.wids['tv_otros'], cols)
        self.wids['tv_otros'].connect("row-activated",
                                      self.abrir_producto_albaran_o_abono)
        tv = self.wids['tv_otros']
        tv.get_column(1).get_cell_renderers()[0].set_property('xalign', 1)
        fin = mx.DateTime.localtime()
        inicio = mx.DateTime.localtime() - mx.DateTime.oneWeek
        self.wids['e_fechainicio'].set_text(utils.str_fecha(inicio))
        self.wids['e_fechafin'].set_text(utils.str_fecha(fin))
        gtk.main()

    def chequear_cambios(self):
        pass

    def set_inicio(self, boton):
        temp = utils.mostrar_calendario(
            fecha_defecto=utils.parse_fecha(
                self.wids['e_fechainicio'].get_text()),
            padre=self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))

    def set_fin(self, boton):
        temp = utils.mostrar_calendario(
            fecha_defecto=utils.parse_fecha(
                self.wids['e_fechafin'].get_text()),
            padre=self.wids['ventana'])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))

    def buscar(self, boton):
        """
        A partir de las fechas de inicio y fin de la ventana busca los
        artículos con trazabilidad y los clasifica por A, B y C en metros,
        kilos reales CON embalaje y bultos. También busca los productos de
        compra con las cantidades que salieron o entraron.
        """
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre=self.wids['ventana'])
        vpro.mostrar()
        fini = utils.parse_fecha(self.wids['e_fechainicio'].get_text())
        ffin = utils.parse_fecha(self.wids['e_fechafin'].get_text())
        vpro.set_valor(0.0, "Buscando albaranes de salida...")
        self.albs = pclases.AlbaranSalida.select(
            pclases.AND(pclases.AlbaranSalida.q.fecha >= fini,
                        pclases.AlbaranSalida.q.fecha < ffin),
            orderBy="fecha")
        fib = {}
        gtx = {}
        cem = {}
        otros = {}
        i = 0.0
        tot = self.albs.count()
        for a in self.albs:
            i += 1
            vpro.set_valor(i / tot, "Analizando albarán %s..." % a.numalbaran)
            extract_data_from_albaran(a, fib, gtx, cem, otros)
        # Abonos
        vpro.set_valor(0.0, "Buscando abonos...")
        self.adedas = pclases.AlbaranDeEntradaDeAbono.select(
            pclases.AND(pclases.AlbaranDeEntradaDeAbono.q.fecha >= fini,
                        pclases.AlbaranDeEntradaDeAbono.q.fecha < ffin),
            orderBy="fecha")
        i = 0.0
        tot = self.adedas.count()
        for a in self.adedas:
            i += 1
            vpro.set_valor(i / tot, "Analizando abono %s..." % a.numalbaran)
            extract_data_from_abono(a, fib, gtx, cem, otros)
        vpro.ocultar()
        tot_fib, tot_gtx, tot_cem = self.rellenar_tabla(fib, gtx, cem, otros)
        self.rellenar_totales(tot_fib, "fibra")
        self.rellenar_totales(tot_gtx, "gtx")
        self.rellenar_totales(tot_cem, "cem")

    def rellenar_tabla(self, fib, gtx, cem, otros):
        """
        Rellena el model con los items de la consulta.
        Recibe cuatro diccionarios dependiendo del tipo de producto que habrá
        que introducir en los cuatro treeviews correspondientes.
        Los diccionarios se organizan:
        {'producto1': {'albarán1': {'m2': {'a': 0.0, 'b': 0.0, 'c': 0.0},
                                    'kg': {'a': 0.0, 'b': 0.0, 'c': 0.0},
                                    '#': {'a': 0, 'b': 0, 'c': 0}},
         'producto2': {'albarán1': {'cantidad': 0.0},
         'producto3': {'albarán2': {'kg': {'a': 0.0, 'b': 0.0, 'c': 0.0},
                                    '#': {'a': 0, 'b': 0, 'c': 0}},
        ...}
        """
        tot_fibra = {'kg': {'a': 0.0, 'b': 0.0, 'c': 0.0},
                     '#':  {'a': 0,   'b': 0,   'c': 0}
                     }
        tot_gtx = {'kg': {'a': 0.0, 'b': 0.0, 'c': 0.0},
                   '#':  {'a': 0,   'b': 0,   'c': 0},
                   'm2': {'a': 0.0, 'b': 0.0, 'c': 0.0}
                   }
        tot_cem = {'kg': {'a': 0.0, 'b': 0.0, 'c': 0.0},
                   '#':  {'a': 0,   'b': 0,   'c': 0}
                   }
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre=self.wids['ventana'])
        vpro.mostrar()
        i = 0.0
        tot = len(fib) + len(gtx) + len(cem) + len(otros)
        try:
            vpro.set_valor(i / tot, "Mostrando %s..." % (""))
        except ZeroDivisionError:
            pass    # It's Easier to Ask Forgiveness than Permission (EAFP)
        for tv, dic, dic_tot in ((self.wids['tv_fibra'], fib, tot_fibra),
                                 (self.wids['tv_gtx'], gtx, tot_gtx),
                                 (self.wids['tv_cem'], cem, tot_cem),
                                 (self.wids['tv_otros'], otros, None)):
            # "Otros" no lleva totales porque son unidades diferentes.
            model = tv.get_model()
            model.clear()
            for producto in dic:
                i += 1
                vpro.set_valor(i / tot, "Mostrando %s..." % (producto))
                fila_producto = build_fila(dic, producto)
                producto_padre = model.append(None, fila_producto)
                if dic_tot:
                    # PLAN: OPTIMIZAR: Estúpido, podrías aprovechar el bucle
                    # de los albaranes de abajo y no repetirlo en el
                    # update_total.
                    update_total(dic_tot, dic[producto])
                for albaran in dic[producto]:
                    fila_albaran = build_fila(dic[producto], albaran)
                    model.append(producto_padre, fila_albaran)
        vpro.ocultar()
        return tot_fibra, tot_gtx, tot_cem

    def rellenar_totales(self, tot, tipo):
        """
        Rellena los totales de fibra, geotextiles y cemento.
        """
        for dim in tot.keys():
            total = 0.0
            for qlty in tot[dim].keys():
                cantidad = tot[dim][qlty]
                total += cantidad
                nomentry = "e_%s_%s_%s" % (tipo, dim, qlty)
                w = self.wids[nomentry]
                w.set_text(utils.float2str(cantidad, autodec=True))
            e_total = 'e_%s_%s_total' % (tipo, dim)
            self.wids[e_total].set_text(
                utils.float2str(total, autodec=True))

    def abrir_producto_albaran_o_abono(self, tv, path, view_column):
        """
        Si la fila seleccionada es una tarifa, abre la tarifa. Si es
        un producto, abre el producto.
        """
        model = tv.get_model()
        puid = model[path][-1]
        objeto = pclases.getObjetoPUID(puid)
        if isinstance(objeto, pclases.ProductoVenta):        # ProductoVenta
            pv = objeto
            if pv.es_rollo() or pv.es_rollo_c():
                from formularios import productos_de_venta_rollos
                productos_de_venta_rollos.ProductosDeVentaRollos(
                    pv, usuario=self.usuario)
            elif (pv.es_bala() or pv.es_bala_cable() or pv.es_bigbag()
                    or pv.es_bolsa() or pv.es_caja()):
                from formularios import productos_de_venta_balas
                productos_de_venta_balas.ProductosDeVentaBalas(
                    pv, usuario=self.usuario)
            elif pv.es_especial():
                from formularios import productos_de_venta_especial
                productos_de_venta_especial.ProductosDeVentaEspecial(
                    pv, usuario=self.usuario)
        elif isinstance(objeto, pclases.ProductoCompra):
            pc = objeto
            from formularios import productos_compra
            productos_compra.ProductosCompra(
                pc, usuario=self.usuario)
        elif isinstance(objeto, pclases.AlbaranSalida):
            alb = objeto
            from formularios import albaranes_de_salida
            albaranes_de_salida.AlbaranesDeSalida(
                alb, usuario=self.usuario)
        elif isinstance(objeto, pclases.AlbaranDeEntradaDeAbono):
            abono = objeto
            from formularios import abonos_venta
            abonos_venta.AbonosVenta(
                abono, usuario=self.usuario)

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        pactiva = self.wids['notebook1'].get_current_page()
        if pactiva == 0:
            tv = self.wids['tv_fibra']
        elif pactiva == 1:
            tv = self.wids['tv_gtx']
        elif pactiva == 2:
            tv = self.wids['tv_cem']
        elif pactiva == 3:
            tv = self.wids['tv_otros']
        abrir_csv(treeview2csv(tv))

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe.
        """
        from informes.treeview2pdf import treeview2pdf
        from formularios.reports import abrir_pdf
        strfecha = "%s - %s" % (self.wids['e_fechainicio'].get_text(),
                                self.wids['e_fechafin'].get_text())
        pactiva = self.wids['notebook1'].get_current_page()
        if pactiva == 0:
            tv = self.wids['tv_fibra']
            totales = range(1, tv.get_model().get_n_columns() - 1)
        elif pactiva == 1:
            tv = self.wids['tv_gtx']
            totales = range(1, tv.get_model().get_n_columns() - 1)
        elif pactiva == 2:
            tv = self.wids['tv_cem']
            totales = range(1, tv.get_model().get_n_columns() - 1)
        elif pactiva == 3:
            tv = self.wids['tv_otros']
            totales = []
        abrir_pdf(treeview2pdf(tv,
                               titulo="Salidas de almacén agrupadas"
                                      "por producto",
                               fecha=strfecha,
                               numcols_a_totalizar=totales))

    def exportar_a_html(self, boton):
        """
        Visualiza la información de las salidas por destino de sus albaranes.
        Exporta un HTML que usa Google Visualization API (Google Charts).
        """
        from lib.google_visualization_python import gviz_api
        import tempfile
        from formularios import multi_open
        import os
        TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                    "..", "informes"))
        tmpl = open(os.path.join(TEMPLATE_DIR, "geomap_template.html"))
        page_template = "".join(tmpl.readlines())
        tmpl.close()
        # Creamos los datos:
        description = {"address": ("string", "Dirección"),
                       "euros": ("number", "€")}
        data = []
        for a in self.albs:
            if a.destino and a.destino.ciudad:
                ciudad_destino = ", ".join((a.destino.ciudad, 
                                            a.destino.pais or "ESPAÑA"))
            elif a.cliente and a.cliente.ciudad:
                ciudad_destino = ", ".join((a.cliente.ciudad, 
                                            a.cliente.pais or "ESPAÑA"))
            else:
                continue
            for dic_valores in data:
                found = False
                if dic_valores["address"] == ciudad_destino:
                    dic_valores["euros"] += a.calcular_total()
                    found = True
                    break
            if not data or not found:
                data.append({"address": ciudad_destino,
                             "euros": a.calcular_total()})
        if pclases.DEBUG:
            from lib.pprintpp import pprint
            pprint(data)
        # Cargamos en gviz_api.DataTable
        data_table = gviz_api.DataTable(description)
        data_table.LoadData(data)
        # Creando código JavaScript
        # jscode = data_table.ToJSCode("jscode_data",
        #                             columns_order = ("address", "euros"),
        #                             order_by = "euros")
        # Creando cadena JSon
        json = data_table.ToJSon(columns_order=("address", "euros"),
                                 order_by = "euros")
        # Metiendo código JS y JSon a la plantilla
        tfile = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
        fname = tfile.name
        reporttitle = "Salidas de mercancía por destino en euros"
        tfile.write(page_template % vars())
        tfile.close()
        # TODO: Contar abonos. Relacionar la gráfica con los kg y no con los
        # euros, no centrar zona en Europa si hay Chile, etc.
        multi_open.webbrowser.open(fname)


def act_fecha(entry, event):
    """
    Cambia los mnemotécnicos de fecha por la fecha debidamente formateada
    o la cadena vacía para indicar que no hay límite de fecha.
    """
    txtfecha = entry.get_text()
    try:
        txtfecha = utils.str_fecha(utils.parse_fecha(txtfecha))
    except (ValueError, TypeError):
        txtfecha = ""
    entry.set_text(txtfecha)


def update_total(dic_total, dic_producto):
    """
    Actualiza los totales a partir del diccionario de albaranes de un producto.
    """
    for albaran in dic_producto:
        for medida in dic_producto[albaran]:
            for calidad in dic_producto[albaran][medida]:
                cantidad = dic_producto[albaran][medida][calidad]
                dic_total[medida][calidad] += cantidad


def build_fila(dic, clave):
    """
    Recibe un diccionario y la clave sobre la que se construirá la fila para
    insertarla en el TreeView. La clave puede ser un PUID de producto (y en
    ese caso el diccionario es el diccionario completo de fibra, geotextiles,
    cemento u otros) o un PUID de albarán (en cuyo caso el diccionario es solo
    el "subdccionario" del producto correspondiente al albarán).
    El en caso de producto, los valores se toman de la suma de todos los
    subdiccionarios. Si es albarán, es inmediato.
    """
    puid = clave
    objeto_pclases = pclases.getObjetoPUID(puid)
    if isinstance(objeto_pclases, (
            pclases.AlbaranSalida, pclases.AlbaranDeEntradaDeAbono)):
        # Los valores están en el propio diccionario.
        producto_o_albaran = objeto_pclases.numalbaran
        m2, kg, bultos, cantidad = extract_dic_abc(dic[clave])
    else:
        # Tengo que recorrer todos los albaranes del producto para hacer la
        # suma del total.
        producto_o_albaran = objeto_pclases.descripcion
        for puidalb in dic[clave]:
            m2, kg, bultos, cantidad = extract_dic_abc(dic[clave][puidalb])
    # Construcción de la fila en sí:
    fila = [producto_o_albaran]
    if not cantidad is None:
        fila += [utils.float2str(cantidad)]
    elif not m2 is None:
        tot_m2 = (m2['a']
                  + m2['b']
                  + m2['c'])
        tot_kg = (kg['a']
                  + kg['b']
                  + kg['c'])
        tot_bultos = (bultos['a']
                      + bultos['b']
                      + bultos['c'])
        fila += [utils.float2str(m2['a']),
                 utils.float2str(kg['a']),
                 utils.float2str(bultos['a'], precision=0),
                 utils.float2str(m2['b']),
                 utils.float2str(kg['b']),
                 utils.float2str(bultos['b'], precision=0),
                 utils.float2str(m2['c']),
                 utils.float2str(kg['c']),
                 utils.float2str(bultos['c'], precision=0),
                 utils.float2str(tot_m2),
                 utils.float2str(tot_kg),
                 utils.float2str(tot_bultos)
                 ]
    else:
        tot_kg = (kg['a']
                  + kg['b']
                  + kg['c'])
        tot_bultos = (bultos['a']
                      + bultos['b']
                      + bultos['c'])
        fila += [utils.float2str(kg['a']),
                 utils.float2str(bultos['a'], precision=0),
                 utils.float2str(kg['b']),
                 utils.float2str(bultos['b'], precision=0),
                 utils.float2str(kg['c']),
                 utils.float2str(bultos['c'], precision=0),
                 utils.float2str(tot_kg),
                 utils.float2str(tot_bultos)
                 ]
    fila += [puid]
    return fila


def extract_dic_abc(d):
    """
    Devuelve los valores para m², kg y bultos de A, B y C y la cantidad del
    diccionario. Si alguno de los valores no está presente, devuelve None.
    Si el diccionario es de producto y contiene diccionario de albaranes,
    devuelve la suma.
    """
    try:
        m2 = d['m2']
    except KeyError:    # No es albarán de un geotextil
        m2 = None
    try:
        kg = d['kg']
        bultos = d['#']
        cantidad = None
    except KeyError:    # No es tampoco fibra ni cemento
        try:
            cantidad = d['cantidad']
            kg = bultos = None
        except KeyError:    # Es un producto. Tengo que sumar los diccionarios
                            # de albaranes que contiene.
            m2 = defaultdict(lambda: 0.0)
            kg = defaultdict(lambda: 0.0)
            bultos = defaultdict(lambda: 0)
            cantidad = 0.0
            for albaran in d:
                _m2, _kg, _bultos, _cantidad = extract_dic_abc(d[albaran])
                for dsum, dparcial in ((m2, _m2),
                                       (kg, _kg),
                                       (bultos, _bultos)):
                    if dparcial:
                        for qlty in dparcial.keys():
                            try:
                                dsum[qlty] += dparcial[qlty]
                            except KeyError:
                                dsum[qlty] = dparcial[qlty]
                if _cantidad:
                    cantidad += _cantidad
    return m2, kg, bultos, cantidad


def extract_data_from_albaran(alb, fib, gtx, cem, otros):
    """
    De las líneas de venta del albarán extrae las cantidades servidas de los
    productos de compra (diccionario otros).
    De los artículos extrae las cantidades en metros (si procede), kilos y
    bultos en el diccionario que corresponda según el tipo de artículo.
    """
    # Primero los procuctos sin trazabilidad:
    for ldv in alb.lineasDeVenta:
        pc = ldv.productoCompra
        if pc:
            if pc.puid not in otros:
                otros[pc.puid] = {}
            if not alb.puid in otros[pc.puid]:
                otros[pc.puid][alb.puid] = {}
            try:
                otros[pc.puid][alb.puid]['cantidad'] += ldv.cantidad
            except KeyError:
                otros[pc.puid][alb.puid]['cantidad'] = ldv.cantidad
    # Y ahora los que se tratan individualmente.
    for a in alb.articulos:
        pv = a.productoVenta
        if pv.es_bala() or pv.es_bala_cable() or pv.es_bigbag():
            dic = fib
        elif pv.es_rollo() or pv.es_rollo_c():
            dic = gtx
        elif pv.es_caja():
            dic = cem
        elif pv.es_especial():
            dic = otros
        else:
            # ¿Qué producto es este? Warning, log y tal...
            dic = None
        if dic is not None:
            if pv.puid not in dic:
                dic[pv.puid] = {}
            if not alb.puid in dic[pv.puid]:
                dic[pv.puid][alb.puid] = {}
            # Ahora determino la calidad (A, B o C) para clasificar.
            if a.es_clase_a():
                qlty = "a"
            elif a.es_clase_b():
                qlty = "b"
            elif a.es_clase_c():
                qlty = "c"
            else:
                raise ValueError("consulta_ventas_por_producto::"
                                 "extract_data_from_albaran"
                                 "El artículo «%s» no es A, B ni C." %
                                 (a.puid))
            if a.superficie is not None or a.es_rolloC():
                # Es un geotextil.
                if "m2" not in dic[pv.puid][alb.puid]:
                    dic[pv.puid][alb.puid]["m2"] = defaultdict(lambda: 0.0)
                try:
                    dic[pv.puid][alb.puid]["m2"][qlty] += a.superficie
                except TypeError:
                    pass    # Es rollo C. No tiene superficie. Solo peso.
            # XXX: OJO: Uso peso CON embalaje. Es lo mismo que se usa en
            # el get_stock_kg_* de pclases para contar existencias. PERO no
            # es el mismo criterio que usa el calcular_kilos_producidos* de
            # pclases para las consultas de producción.
            peso = a.peso
            if not peso is None:
                if "kg" not in dic[pv.puid][alb.puid]:
                    dic[pv.puid][alb.puid]["kg"] = defaultdict(lambda: 0.0)
                if "#" not in dic[pv.puid][alb.puid]:
                    dic[pv.puid][alb.puid]["#"] = defaultdict(lambda: 0)
                try:
                    dic[pv.puid][alb.puid]["kg"][qlty] += peso
                    dic[pv.puid][alb.puid]["#"][qlty] += 1
                except KeyError:
                    dic[pv.puid][alb.puid]["kg"][qlty] = peso
                    dic[pv.puid][alb.puid]["#"][qlty] = 1
            else:   # Es un producto especial. Cuento el artículo en sí mismo.
                try:
                    dic[pv.puid][alb.puid]["cantidad"] += 1
                except KeyError:
                    dic[pv.puid][alb.puid]["cantidad"] = 1


def extract_data_from_abono(alb, fib, gtx, cem, otros):
    """
    De las líneas de venta del abono extrae las cantidades servidas de los
    productos de compra (diccionario otros).
    De los artículos extrae las cantidades en metros (si procede), kilos y
    bultos en el diccionario que corresponda según el tipo de artículo.
    """
    for ldd in alb.lineasDeDevolucion:  # Las lineasDeAbono son de ajuste de
                                # precio. No implican movimiento en almacén.
        pv = ldd.productoVenta
        a = ldd.articulo
        if pv.es_bala() or pv.es_bala_cable() or pv.es_bigbag():
            dic = fib
        elif pv.es_rollo() or pv.es_rollo_c():
            dic = gtx
        elif pv.es_caja():
            dic = cem
        elif pv.es_especial():
            dic = otros
        else:
            # ¿Qué producto es este? Warning, log y tal...
            dic = None
        if dic is not None:
            if pv.puid not in dic:
                dic[pv.puid] = {}
            if alb.puid not in dic[pv.puid]:
                dic[pv.puid][alb.puid] = {}
            # Ahora determino la calidad (A, B o C) para clasificar.
            if a.es_clase_a():
                qlty = "a"
            elif a.es_clase_b():
                qlty = "b"
            elif a.es_clase_c():
                qlty = "c"
            else:
                raise ValueError("consulta_ventas_por_producto::"
                                 "extract_data_from_abono"
                                 "El artículo «%s» no es A, B ni C." %
                                 (a.puid))
            if a.superficie is not None or a.es_rolloC():
                # Es un geotextil.
                if "m2" not in dic[pv.puid][alb.puid]:
                    dic[pv.puid][alb.puid]["m2"] = defaultdict(lambda: 0.0)
                try:
                    dic[pv.puid][alb.puid]["m2"][qlty] += -a.superficie
                except TypeError:
                    pass    # Es rollo C. No tiene superficie. Solo peso.
            # XXX: OJO: Uso peso CON embalaje. Es lo mismo que se usa en
            # el get_stock_kg_* de pclases para contar existencias. PERO no
            # es el mismo criterio que usa el calcular_kilos_producidos* de
            # pclases para las consultas de producción.
            peso = a.peso
            if not peso is None:
                if "kg" not in dic[pv.puid][alb.puid]:
                    dic[pv.puid][alb.puid]["kg"] = defaultdict(lambda: 0.0)
                if "#" not in dic[pv.puid][alb.puid]:
                    dic[pv.puid][alb.puid]["#"] = defaultdict(lambda: 0)
                try:
                    dic[pv.puid][alb.puid]["kg"][qlty] += -peso
                    dic[pv.puid][alb.puid]["#"][qlty] += -1
                except KeyError:
                    dic[pv.puid][alb.puid]["kg"][qlty] = -peso
                    dic[pv.puid][alb.puid]["#"][qlty] = -1
            else:   # Es un producto especial. Cuento el artículo en sí mismo.
                try:
                    dic[pv.puid][alb.puid]["cantidad"] += -1
                except KeyError:
                    dic[pv.puid][alb.puid]["cantidad"] = -1


if __name__ == '__main__':
    t = ConsultaVentasPorProducto()
