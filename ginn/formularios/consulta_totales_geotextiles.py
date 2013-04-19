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
## consulta_totales_geotextiles.py -- Resumen mensual geotextiles.
###################################################################
## NOTAS:
##  Esta consulta es un tanto especial y está diseñada muy muy 
## específicamente para el cliente concreto.
###################################################################
## Changelog:
## 19 de diciembre de 2006 -> Inicio
## 
###################################################################

from ventana import Ventana
import pygtk
pygtk.require('2.0')
import gtk, utils
from framework import pclases
import mx.DateTime
from informes import geninformes
from math import ceil
from formularios import ventana_progreso

def buscar_annos_ini_fin():
    """
    Devuelve el primer y último año encontrados con 
    actividad de producción en la base de datos.
    """
    partes = pclases.ParteDeProduccion.select(orderBy = "fecha")
    anno_ini = partes[0].fecha.year
    partes = pclases.ParteDeProduccion.select(orderBy = "-fecha")
    anno_fin = partes[0].fecha.year
    return anno_ini, anno_fin

def get_produccion(fecha_ini, fecha_fin, incluir_sin_parte = False):
    """
    Devuelve la producción entre las dos fechas recibidas en forma de 
    diccionario con las claves "rollos", "metros" y "kilos". 
    Los kilos corresponden al peso teórico de los productos.
    """
    produccion = {'rollos': 0, 'metros': 0, 'kilos': 0}
    partes = pclases.ParteDeProduccion.select(pclases.AND(pclases.ParteDeProduccion.q.fecha >= fecha_ini, 
                                                          pclases.ParteDeProduccion.q.fecha <= fecha_fin))
    for parte in partes:
        if parte.es_de_geotextiles():
            rollos_en_parte = len([a for a in parte.articulos if a.es_rollo()])
            producto = parte.productoVenta
            if producto != None:
                produccion['rollos'] += rollos_en_parte + len([a for a in parte.articulos if a.es_rollo_defectuoso()])
                produccion['metros'] += (rollos_en_parte * producto.camposEspecificosRollo.metros_cuadrados) + sum([a.superficie for a in parte.articulos if a.es_rollo_defectuoso()])
                produccion['kilos'] += (rollos_en_parte * producto.camposEspecificosRollo.peso_teorico) + sum([a.rolloDefectuoso.peso_sin for a in parte.articulos if a.es_rollo_defectuoso()])
            else:
                assert rollos_en_parte == 0     # Para comprobar que no hay partes extraños con artículos pero sin productoVenta.
    if incluir_sin_parte:       # Esto solo tiene en cuenta el peso teórico y cuenta los defectuosos como normales.
        fechasqlini = fecha_ini.strftime('%Y-%m-%d')
        fechasqlfin = (fecha_fin + mx.DateTime.oneDay).strftime('%Y-%m-%d')
        articulos_de_rollos_sin_parte_de_produccion_y_entre_fechas = pclases.Articulo.select("""
        rollo_id IN (SELECT id FROM rollo WHERE fechahora >= '%s' AND fechahora < '%s') AND parte_de_produccion_id IS NULL
        """ % (fechasqlini, fechasqlfin))
        dimensiones = pclases.CamposEspecificosRollo._queryAll(  # @UndefinedVariable
        """
            SELECT ancho*metros_lineales, ancho*metros_lineales*gramos, producto_venta.id FROM campos_especificos_rollo, producto_venta
            WHERE campos_especificos_rollo.id=producto_venta.campos_especificos_rollo_id
        """)
        dic_dimensiones = {}
        for dimension in dimensiones:
            dic_dimensiones[dimension[2]] = {'metros_cuadrados': dimension[0], 'peso_teorico': dimension[1]}
        produccion['rollos'] += articulos_de_rollos_sin_parte_de_produccion_y_entre_fechas.count()
        for a in articulos_de_rollos_sin_parte_de_produccion_y_entre_fechas:
            produccion['metros'] += dic_dimensiones[a.productoVentaID]['metros_cuadrados']
            produccion['kilos'] += dic_dimensiones[a.productoVentaID]['peso_teorico']
    return produccion

def get_existencias(fecha_fin):
    """
    Devuelve el total de existencias de productos de venta 
    de tipo geotextiles en la fecha dada.
    La cantidad la saca del histórico.
    """
    existencias = {'rollos': 0, 'metros': 0, 'kilos': 0}
    productos = pclases.ProductoVenta.select(pclases.ProductoVenta.q.camposEspecificosRolloID != None)
    for p in productos:
        rollos = p.get_existencias(hasta = fecha_fin)
        existencias['rollos'] += rollos
        existencias['metros'] += rollos * p.camposEspecificosRollo.metros_cuadrados
        existencias['kilos'] += rollos * p.camposEspecificosRollo.peso_teorico
    return existencias

def get_salidas_reales(fecha_ini, fecha_fin):
    """
    Devuelve un diccionario con rollos, metros y kilos de 
    todas las salidas albaraneadas (valga la redundancia) 
    separadas por tarifas.
    Los cálculos se basan en los artículos reales salidos 
    en los albaranes en lugar de en las cantidades de sus 
    líneas de venta. Devuelve rollos, metros y kilos, pero 
    en lugar de partir de los metros cuadrados y calcular 
    los rollos teóricos, parte de los rollos reales y calcula 
    los metros y kilos teóricos.
    """
    # FIXME: TODO: MUY MUY LENTO. En cuanto verifique que cuadran las cantidades, optimizar con urgencia.
    salidas = {}
    albaranes = pclases.AlbaranSalida.select(pclases.AND(pclases.AlbaranSalida.q.fecha >= fecha_ini, 
                                                         pclases.AlbaranSalida.q.fecha <= fecha_fin))
    dimensiones = pclases.CamposEspecificosRollo._queryAll(
    """
        SELECT ancho*metros_lineales, ancho*metros_lineales*gramos, producto_venta.id FROM campos_especificos_rollo, producto_venta
        WHERE campos_especificos_rollo.id=producto_venta.campos_especificos_rollo_id
    """)
    dic_dimensiones = {}
    for dimension in dimensiones:
        dic_dimensiones[dimension[2]] = {'metros_cuadrados': dimension[0], 'peso_teorico': dimension[1]}
    for albaran in albaranes:
        articulos_por_ldv = None
        for articulo in albaran.articulos:
            if articulo.productoVenta.es_rollo():
                # ldv = articulo.get_ldv(albaran)
                if articulos_por_ldv == None:
                    articulos_por_ldv = albaran.agrupar_articulos()
                ldv = None
                for idldv in articulos_por_ldv:
                    if articulo in articulos_por_ldv[idldv]['articulos']:
                        ldv = pclases.LineaDeVenta.get(idldv)
                        break
                if ldv != None:
                    tarifa = ldv.get_tarifa()
                else:
                    print "WARNING: Artículo ID %d sin LDV en albarán ID %d." % (articulo.id, albaran.id)
                    tarifa = None
                metros = dic_dimensiones[articulo.productoVentaID]['metros_cuadrados']
                kilos = dic_dimensiones[articulo.productoVentaID]['peso_teorico']
                if tarifa not in salidas:
                    salidas[tarifa] = {'rollos': 1, 
                                       'metros': metros, 
                                       'kilos': kilos}
                else:
                    salidas[tarifa]['rollos'] += 1
                    salidas[tarifa]['metros'] += metros
                    salidas[tarifa]['kilos'] += kilos
    return salidas

def get_salidas(fecha_ini, fecha_fin):
    """
    Devuelve un diccionario con rollos, metros y kilos de 
    todas las salidas albaraneadas (valga la redundancia) 
    separadas por tarifas.
    """
    salidas = {}
    albaranes = pclases.AlbaranSalida.select(pclases.AND(pclases.AlbaranSalida.q.fecha >= fecha_ini, 
                                                         pclases.AlbaranSalida.q.fecha <= fecha_fin))
    for albaran in albaranes:
        for ldv in albaran.lineasDeVenta:
            producto = ldv.producto
            if hasattr(producto, "es_rollo") and producto.es_rollo():   # Sólo me interesan geotextiles
                metros = ldv.cantidad       # OJO: No cuento los bultos que de verdad salieron del albarán. Con albaranes antiguos
                                            # es posible que se vean resultados extraños, en un futuro (y desde hace algunos meses)
                                            # no debería haber diferencia entre la cantidad de la LDV y la cantidad albaraneada del 
                                            # producto.
                try:
                    rollos = int(ceil(ldv.cantidad / producto.camposEspecificosRollo.metros_cuadrados))
                except ZeroDivisionError:
                    msg = "WARNING: consulta_totales_geotextiles.py: get_salidas: producto ID %d (%s) tiene metros_cuadrados de camposEspecificosRollo a 0." % (producto.id, producto.descripcion)
                    # DONE: Ahora mismo los únicos productos que dan este WARNING son los típicos de "huevera", "geotextiles varios", etc... En un futuro, todos estos productos deberían ir con camposEspecificosRollo == None y camposEspeciales != None, así que ya no molestarán más en esta consulta. De cualquier forma, al conteo de "rollos" y "kilos" no afecta, ya que suponen 0. Otra cosa son los metros.
                    print msg
                    rollos = 0
                kilos = rollos * producto.camposEspecificosRollo.peso_teorico
                tarifa = ldv.get_tarifa()   # None si no tiene tarifa.
                if tarifa not in salidas:
                    salidas[tarifa] = {'metros': metros, 'rollos': rollos, 'kilos': kilos}
                else:
                    salidas[tarifa]['rollos'] += rollos 
                    salidas[tarifa]['metros'] += metros
                    salidas[tarifa]['kilos'] += kilos
    return salidas

def get_salidas_composan_nacional(fecha_ini, fecha_fin):
    """
    Devuelve un diccionario con rollos, metros y kilos de 
    todas las salidas albaraneadas (valga la redundancia) 
    pertenecientes al cliente "Composan" y con tarifa nacional.
    Obsoleto. Ya no se usa en esta ventana, y diría que en ninguna otra.
    """
    # DEPRECATED.
    # FIXME: Premature optimization is the root of all evil. Ya habrá tiempo de mejorar la velocidad llamando una 
    # única vez a get_salidas en las 3 funciones para dividir por composan nacional, internacional, etc...
    tarifas_nacionales_composan = pclases.Tarifa.select(pclases.AND(pclases.Tarifa.q.nombre.contains("composan"), 
                                                                    pclases.Tarifa.q.nombre.contains("nacional")))
    tarifas_nacionales_composan = tuple(tarifas_nacionales_composan)
    # salidas = get_salidas(fecha_ini, fecha_fin)
    salidas = get_salidas_reales(fecha_ini, fecha_fin)
    salidas_nac = {'rollos': 0, 'metros': 0, 'kilos': 0}
    for tarifa in salidas:
        if tarifa in tarifas_nacionales_composan:
            salidas_nac['rollos'] += salidas[tarifa]['rollos']
            salidas_nac['metros'] += salidas[tarifa]['metros']
            salidas_nac['kilos'] += salidas[tarifa]['kilos']
    return salidas_nac

def get_salidas_composan_internacional(fecha_ini, fecha_fin):
    """
    Devuelve un diccionario con rollos, metros y kilos de 
    todas las salidas albaraneadas (valga la redundancia) 
    pertenecientes al cliente "Composan" y con tarifa internacional 
    (considerando internacional como todo lo que no sea nacional).
    """
    # OJO: Todo MUY MUY VERY VERY HARCODED.
    tarifas_nacionales_composan = pclases.Tarifa.select(pclases.AND(pclases.Tarifa.q.nombre.contains("composan"), 
                                                                    pclases.Tarifa.q.nombre.contains("nacional")))
    tarifas_nacionales_composan = tuple(tarifas_nacionales_composan)
    todas_las_tarifas_composan = pclases.Tarifa.select(pclases.AND(pclases.Tarifa.q.nombre.contains("composan")))
    tarifas_internacionales_composan = []
    for tarifa in todas_las_tarifas_composan:
        if tarifa not in tarifas_nacionales_composan:
            tarifas_internacionales_composan.append(tarifa)
    tarifas_internacionales_composan = tuple(tarifas_internacionales_composan)
    # salidas = get_salidas(fecha_ini, fecha_fin)
    salidas = get_salidas_reales(fecha_ini, fecha_fin)
    salidas_int = {'rollos': 0, 'metros': 0, 'kilos': 0}
    for tarifa in salidas:
        if tarifa in tarifas_internacionales_composan:
            salidas_int['rollos'] += salidas[tarifa]['rollos']
            salidas_int['metros'] += salidas[tarifa]['metros']
            salidas_int['kilos'] += salidas[tarifa]['kilos']
    return salidas_int

def get_salidas_gea21(fecha_ini, fecha_fin):
    """
    Devuelve un diccionario con rollos, metros y kilos de las 
    cantidades servidas en LDVs de albaranes cuya tarifa sea 
    la de GEA-21.
    """
    salidas_gea = {'rollos': 0, 'metros': 0, 'kilos': 0}
    tarifas_gea = pclases.Tarifa.select(pclases.Tarifa.q.nombre.contains("gea"))
    tarifas_gea = tuple(tarifas_gea)
#    salidas = get_salidas(fecha_ini, fecha_fin)
    salidas = get_salidas_reales(fecha_ini, fecha_fin)
    for tarifa in salidas:
        if tarifa in tarifas_gea:
            salidas_gea['rollos'] += salidas[tarifa]['rollos']
            salidas_gea['metros'] += salidas[tarifa]['metros']
            salidas_gea['kilos'] += salidas[tarifa]['kilos']
    return salidas_gea

def get_salidas_otros(fecha_ini, fecha_fin):
    """
    Devuelve las salidas cuyas tarifas no son de composan nacional, ni internacional 
    ni gea o bien ni siquiera tienen tarifa (ldv.get_tarifa() == None).
    """
    salidas_otros = {'rollos': 0, 'metros': 0, 'kilos': 0}
    tarifas_otros = pclases.Tarifa.select(pclases.AND(pclases.NOT(pclases.Tarifa.q.nombre.contains("gea")), 
                                                      pclases.NOT(pclases.Tarifa.q.nombre.contains("composan"))))
    tarifas_otros = tuple(tarifas_otros)
    # salidas = get_salidas(fecha_ini, fecha_fin)
    salidas = get_salidas_reales(fecha_ini, fecha_fin)
    for tarifa in salidas:
        if tarifa in tarifas_otros:
            salidas_otros['rollos'] += salidas[tarifa]['rollos']
            salidas_otros['metros'] += salidas[tarifa]['metros']
            salidas_otros['kilos'] += salidas[tarifa]['kilos']
    return salidas_otros

def get_salidas_compnac_compint_gea_otros(fecha_ini, fecha_fin):
    """
    Devuelve los cuatro diccionarios. Optimización para llamar al 
    get_salidas general una sola vez.
    """
    tarifas_nacionales_composan = pclases.Tarifa.select(pclases.AND(pclases.Tarifa.q.nombre.contains("composan"), 
                                                                    pclases.Tarifa.q.nombre.contains("nacional")))
    tarifas_nacionales_composan = tuple(tarifas_nacionales_composan)
    todas_las_tarifas_composan = pclases.Tarifa.select(pclases.AND(pclases.Tarifa.q.nombre.contains("composan")))
    tarifas_internacionales_composan = []
    for tarifa in todas_las_tarifas_composan:
        if tarifa not in tarifas_nacionales_composan:
            tarifas_internacionales_composan.append(tarifa)
    tarifas_internacionales_composan = tuple(tarifas_internacionales_composan)
    tarifas_gea = pclases.Tarifa.select(pclases.Tarifa.q.nombre.contains("gea"))
    tarifas_gea = tuple(tarifas_gea)
    tarifas_otros = pclases.Tarifa.select(pclases.AND(pclases.NOT(pclases.Tarifa.q.nombre.contains("gea")), 
                                                      pclases.NOT(pclases.Tarifa.q.nombre.contains("composan"))))
    tarifas_otros = tuple(list(tarifas_otros) + [None])
    salidas_nac = {'rollos': 0, 'metros': 0, 'kilos': 0}
    salidas_int = {'rollos': 0, 'metros': 0, 'kilos': 0}
    salidas_gea = {'rollos': 0, 'metros': 0, 'kilos': 0}
    salidas_otros = {'rollos': 0, 'metros': 0, 'kilos': 0}
    salidas_totales = {'rollos': 0, 'metros': 0, 'kilos': 0}
    salidas = get_salidas_reales(fecha_ini, fecha_fin)
    # salidas = get_salidas(fecha_ini, fecha_fin)
    for tarifa in salidas:
        if tarifa in tarifas_nacionales_composan:
            salidas_nac['rollos'] += salidas[tarifa]['rollos']
            salidas_nac['metros'] += salidas[tarifa]['metros']
            salidas_nac['kilos'] += salidas[tarifa]['kilos']
        if tarifa in tarifas_internacionales_composan:
            salidas_int['rollos'] += salidas[tarifa]['rollos']
            salidas_int['metros'] += salidas[tarifa]['metros']
            salidas_int['kilos'] += salidas[tarifa]['kilos']
        if tarifa in tarifas_gea:
            salidas_gea['rollos'] += salidas[tarifa]['rollos']
            salidas_gea['metros'] += salidas[tarifa]['metros']
            salidas_gea['kilos'] += salidas[tarifa]['kilos']
        if tarifa in tarifas_otros:
            salidas_otros['rollos'] += salidas[tarifa]['rollos']
            salidas_otros['metros'] += salidas[tarifa]['metros']
            salidas_otros['kilos'] += salidas[tarifa]['kilos']
        salidas_totales['rollos'] += salidas[tarifa]['rollos']
        salidas_totales['metros'] += salidas[tarifa]['metros']
        salidas_totales['kilos'] += salidas[tarifa]['kilos']
    return salidas_nac, salidas_int, salidas_gea, salidas_otros, salidas_totales

def get_pedidos_pendientes(fecha):
    """
    Devuelve las cantidades de geotextiles de los pedidos que 
    estaban pendientes en la fecha dada.
    Los pedidos pendientes hasta una fecha son todos aquellos 
    pedidos cuya fecha sea inferior a la dada y cuyas LDV no han 
    sido servidas aún o fueron servidas en un albarán de 
    fecha mayor estricto a la fecha en cuestión.
    """
    pendiente = {'rollos': 0, 'metros': 0, 'kilos': 0}
    pedidos_hasta_fecha = pclases.PedidoVenta.select(pclases.PedidoVenta.q.fecha <= fecha)
    for pedido in pedidos_hasta_fecha:
        pedido_y_servido_por_producto = {}
        # CANTIDADES PEDIDAS POR PRODUCTO
        for ldp in pedido.lineasDePedido:
            producto = ldp.productoVenta
            if hasattr(producto, "es_rollo") and producto.es_rollo():
                if producto not in pedido_y_servido_por_producto:
                    pedido_y_servido_por_producto[producto] = {'pedido': ldp.cantidad, 'servido': 0}
                else:
                    pedido_y_servido_por_producto[producto]['pedido'] += ldp.cantidad
        # CANTIDADES SERVIDAS POR PRODUCTO 
        for ldv in pedido.lineasDeVenta:
            producto = ldv.producto
            if hasattr(producto, "es_rollo") and producto.es_rollo():
                if ldv.albaranSalida == None or ldv.albaranSalida.fecha > fecha:
                    # Si aún no se ha servido o se sirvió después de la fecha "pivote", es que en dicha 
                    # fecha aún estaba pendiente de servir.
                    if producto not in pedido_y_servido_por_producto:
                        pedido_y_servido_por_producto[producto] = {'pedido': 0, 'servido': ldv.cantidad}
                    else:
                        pedido_y_servido_por_producto[producto]['servido'] += ldv.cantidad
        # FINALEMENTE, OBTENEMOS LO PENDIENTE
        # NOTA: Considero pendiente solo aquello cuya diferencia entre pedido y servido sea estrictamente positiva.
        for producto in pedido_y_servido_por_producto:
            cantidad_pendiente = pedido_y_servido_por_producto[producto]['pedido'] - pedido_y_servido_por_producto[producto]['servido']
            if cantidad_pendiente > 0:
                metros = cantidad_pendiente
                try:
                    rollos = int(ceil(cantidad_pendiente / producto.camposEspecificosRollo.metros_cuadrados))
                except ZeroDivisionError:
                    msg = "WARNING: consulta_totales_geotextiles.py: get_pedidos_pendientes: producto ID %d (%s) tiene metros_cuadrados de camposEspecificosRollo a 0." % (producto.id, producto.descripcion)
                    print msg
                    rollos = 0
                kilos = rollos * producto.camposEspecificosRollo.peso_teorico
                pendiente['metros'] += metros
                pendiente['kilos'] += kilos
                pendiente['rollos'] += rollos
    return pendiente


class ConsultaTotalesGeotextiles(Ventana):
        
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'consulta_totales_geotextiles.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_exportar/clicked': self.exportar
                      }
        self.add_connections(connections)
        cols = (('Mes', 'gobject.TYPE_STRING', False, False, False, None), 
                ('Producción: rollos', 'gobject.TYPE_STRING', False, False, False, None),
                ('Producción: m²', 'gobject.TYPE_STRING', False, False, False, None),
                ('Producción: kg', 'gobject.TYPE_STRING', False, False, False, None),
                ('Existencias: rollos', 'gobject.TYPE_STRING', False, False, False, None),
                ('Existencias: m²', 'gobject.TYPE_STRING', False, False, False, None), 
                ('Existencias: kg', 'gobject.TYPE_STRING', False, False, False, None),
                ('Salidas: total: rollos', 'gobject.TYPE_STRING', False, False, False, None),
                ('Salidas: total: m²', 'gobject.TYPE_STRING', False, False, False, None),
                ('Salidas: total: kg', 'gobject.TYPE_STRING', False, False, False, None), 
                ('Salidas: C. nac.: rollos', 'gobject.TYPE_STRING', False, False, False, None),
                ('Salidas: C. nac.: m²', 'gobject.TYPE_STRING', False, False, False, None),
                ('Salidas: C. nac.: kg', 'gobject.TYPE_STRING', False, False, False, None), 
                ('Salidas: C. int.: rollos', 'gobject.TYPE_STRING', False, False, False, None),
                ('Salidas: C. int.: m²', 'gobject.TYPE_STRING', False, False, False, None),
                ('Salidas: C. int.: kg', 'gobject.TYPE_STRING', False, False, False, None), 
                ('Salidas: G.: rollos', 'gobject.TYPE_STRING', False, False, False, None),
                ('Salidas: G.: m²', 'gobject.TYPE_STRING', False, False, False, None),
                ('Salidas: G.: kg', 'gobject.TYPE_STRING', False, False, False, None), 
                ('Salidas: Otros: rollos', 'gobject.TYPE_STRING', False, False, False, None),
                ('Salidas: Otros: m²', 'gobject.TYPE_STRING', False, False, False, None),
                ('Salidas: Otros: kg', 'gobject.TYPE_STRING', False, False, False, None), 
                ('Peds. pendientes: rollos', 'gobject.TYPE_STRING', False, False, False, None),
                ('Peds. pendientes: m²', 'gobject.TYPE_STRING', False, False, False, None),
                ('Peds. pendientes: kg', 'gobject.TYPE_STRING', False, False, False, None), 
                ('mes', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_datos'], cols)
        for numcol in xrange(1, 25):
            col = self.wids['tv_datos'].get_column(numcol)
            for cell in col.get_cell_renderers():
                cell.set_property('xalign', 1.0)
        anno_ini, anno_fin = buscar_annos_ini_fin()
        opciones = [(anno, anno) for anno in xrange(anno_ini, anno_fin + 1)]
        utils.rellenar_lista(self.wids['cbe_year'], opciones)
        utils.combo_set_from_db(self.wids['cbe_year'], -1)
        gtk.main()

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        tv = self.wids['tv_datos']
        abrir_csv(treeview2csv(tv))

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, items):
        """
        Rellena el model con los items de la consulta
        """ 
        model = self.wids['tv_datos'].get_model()
        model.clear()
        for fila in items:
            model.append(fila)
        
    def buscar(self, boton):
        """
        Dadas fecha de inicio y de fin, lista todos los albaranes
        pendientes de facturar.
        """
        anno = utils.combo_get_value(self.wids['cbe_year'])
        resultado = []
        if anno == -1 or anno == None:
            # Intento leerlo del entry
            str_anno = self.wids['cbe_year'].child.get_text()
            try:
                anno = int(str_anno)
            except:
                pass
        if anno != -1 and anno != None:
            vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
            act = 0.0; tot = 8.0 * 12
            vpro.mostrar()
            total_produccion = {'rollos': 0, 'metros': 0, 'kilos': 0}
            total_existencias = {'rollos': 0, 'metros': 0, 'kilos': 0}
            total_composan_nacional = {'rollos': 0, 'metros': 0, 'kilos': 0}
            total_composan_internacional = {'rollos': 0, 'metros': 0, 'kilos': 0}
            total_gea21 = {'rollos': 0, 'metros': 0, 'kilos': 0}
            total_otros = {'rollos': 0, 'metros': 0, 'kilos': 0}
            total_salidas = {'rollos': 0, 'metros': 0, 'kilos': 0}
            total_pendiente = {'rollos': 0, 'metros': 0, 'kilos': 0}
            # DEBUG: for mes in xrange(1, 3):
            for mes in xrange(1, 13):
                fecha_ini = mx.DateTime.DateTimeFrom(day = 1, month = mes, year = anno)
                fecha_fin = mx.DateTime.DateTimeFrom(day = -1, month = mes, year = anno)    # Último día del mes
                mes_str = utils.corregir_nombres_fecha(mx.DateTime.Month[mes]).title()
                act = 1 + ((mes -1) * 8)
                vpro.set_valor(act/tot, "Calculando producción %s..." % (mes_str))
                produccion = get_produccion(fecha_ini, fecha_fin, incluir_sin_parte = True)
                act = 2 + ((mes -1) * 8)
                vpro.set_valor(act/tot, "Calculando existencias %s..." % (mes_str))
                existencias = get_existencias(fecha_fin)
                #act = 3 + ((mes -1) * 8)
                #vpro.set_valor(act/tot, "Calculando Composan nacional %s..." % (mes_str))
                #salidas_composan_nacional = get_salidas_composan_nacional(fecha_ini, fecha_fin)
                #act = 4 + ((mes -1) * 8)
                #vpro.set_valor(act/tot, "Calculando Composan internacional %s..." % (mes_str))
                #salidas_composan_internacional = get_salidas_composan_internacional(fecha_ini, fecha_fin)
                #act = 5 + ((mes -1) * 8)
                #vpro.set_valor(act/tot, "Calculando Gea 21 %s..." % (mes_str))
                #salidas_gea21 = get_salidas_gea21(fecha_ini, fecha_fin)
                #act = 6 + ((mes -1) * 8)
                #vpro.set_valor(act/tot, "Calculando Otros %s..." % (mes_str))
                #salidas_otros = get_salidas_otros(fecha_ini, fecha_fin)
                act = 5 + ((mes -1) * 8)
                vpro.set_valor(act/tot, "Calculando salidas por tarifa %s..." % (mes_str))
                salidas_composan_nacional, \
                salidas_composan_internacional, \
                salidas_gea21, \
                salidas_otros, \
                total_salidas_mes = get_salidas_compnac_compint_gea_otros(fecha_ini, fecha_fin)
                #act = 7 + ((mes -1) * 8)
                #vpro.set_valor(act/tot, "Calculando salidas totales %s..." % (mes_str))
                #total_salidas_mes = {}
                #for c in ('rollos', 'metros', 'kilos'): 
                #    total_salidas_mes[c] = salidas_composan_nacional[c] + salidas_composan_internacional[c] + salidas_gea21[c] + salidas_otros[c]
                act = 8 + ((mes -1) * 8)
                vpro.set_valor(act/tot, "Calculando pedidos pendientes %s..." % (mes_str))
                pedidos_pendientes = get_pedidos_pendientes(fecha_fin)
                resultado.append((mes_str, 
                                  produccion['rollos'], 
                                  utils.int2str(produccion['metros']), 
                                  utils.float2str(produccion['kilos']), 
                                  existencias['rollos'], 
                                  utils.int2str(existencias['metros']), 
                                  utils.float2str(existencias['kilos']), 
                                  total_salidas_mes['rollos'], 
                                  utils.int2str(total_salidas_mes['metros']), 
                                  utils.float2str(total_salidas_mes['kilos']), 
                                  salidas_composan_nacional['rollos'], 
                                  utils.int2str(salidas_composan_nacional['metros']), 
                                  utils.float2str(salidas_composan_nacional['kilos']),
                                  salidas_composan_internacional['rollos'], 
                                  utils.int2str(salidas_composan_internacional['metros']), 
                                  utils.float2str(salidas_composan_internacional['kilos']), 
                                  salidas_gea21['rollos'], 
                                  utils.int2str(salidas_gea21['metros']), 
                                  utils.float2str(salidas_gea21['kilos']), 
                                  salidas_otros['rollos'], 
                                  utils.int2str(salidas_otros['metros']), 
                                  utils.float2str(salidas_otros['kilos']), 
                                  pedidos_pendientes['rollos'], 
                                  utils.int2str(pedidos_pendientes['metros']), 
                                  utils.float2str(pedidos_pendientes['kilos']), 
                                  mes))
                for campo in ('rollos', 'metros', 'kilos'):
                    for total, parcial in ((total_produccion, produccion), 
                                           (total_existencias, existencias), 
                                           (total_composan_nacional, salidas_composan_nacional), 
                                           (total_composan_internacional, salidas_composan_internacional), 
                                           (total_gea21, salidas_gea21), 
                                           (total_otros, salidas_otros), 
                                           (total_salidas, total_salidas_mes), 
                                           (total_pendiente, pedidos_pendientes)):
                        total[campo] += parcial[campo]
            resultado.append(("TOTAL", 
                              total_produccion['rollos'], 
                              utils.int2str(total_produccion['metros']),
                              utils.float2str(total_produccion['kilos']), 
                              total_existencias['rollos'],
                              utils.int2str(total_existencias['metros']),
                              utils.float2str(total_existencias['kilos']), 
                              total_salidas['rollos'],
                              utils.int2str(total_salidas['metros']),
                              utils.float2str(total_salidas['kilos']), 
                              total_composan_nacional['rollos'],
                              utils.int2str(total_composan_nacional['metros']),
                              utils.float2str(total_composan_nacional['kilos']),
                              total_composan_internacional['rollos'],
                              utils.int2str(total_composan_internacional['metros']),
                              utils.float2str(total_composan_internacional['kilos']), 
                              total_gea21['rollos'],
                              utils.int2str(total_gea21['metros']),
                              utils.float2str(total_gea21['kilos']), 
                              total_otros['rollos'],
                              utils.int2str(total_otros['metros']),
                              utils.float2str(total_otros['kilos']), 
                              total_pendiente['rollos'],
                              utils.int2str(total_pendiente['metros']),
                              utils.float2str(total_pendiente['kilos']), 
                              13))
            vpro.ocultar()
        self.rellenar_tabla(resultado)

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        from formularios import reports
        datos = []
        model = self.wids['tv_datos'].get_model()
        for itr in model:
            row = []
            for i in xrange(25):
                row.append(itr[i])
            datos.append(tuple(row))
        datos.insert(-1, ("---", )*25)  # La línea horizontal antes del TOTAL
        if datos != []:
            anno = self.wids['cbe_year'].child.get_text()
            reports.abrir_pdf(geninformes.resumen_totales_geotextiles(datos, utils.str_fecha(mx.DateTime.localtime()), anno))


if __name__ == '__main__':
    t = ConsultaTotalesGeotextiles()

