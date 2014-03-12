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
## consulta_producido.py -- 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 
###################################################################

import datetime
from formularios import ventana_progreso
from framework import pclases
from informes import geninformes
try:
    from pychart import * # No me gusta, pero no queda otra @UnusedWildImport
    pychart_available = True
except ImportError:
    pychart_available = False
from tempfile import gettempdir
from ventana import Ventana
import gtk
import time
import mx.DateTime
import pygtk
import os
from formularios import utils
from formularios.ventana_progreso import VentanaProgreso
from lib import charting
pygtk.require('2.0')
    

class ConsultaProducido(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.grafico = None
        self.kilos = 0
        self.metros = 0
        self.rollos = 0
        self.balas = 0
        Ventana.__init__(self, 'consulta_producido.glade', objeto, 
                         usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       "b_exportar/clicked": self.exportar, 
                       #"im_graph/button-press-event": self.alternar_grafica, 
                       #"eventbox_chart/button-press-event": 
                       #                                 self.alternar_grafica, 
                       "eventbox_hbox/button-press-event": 
                                                        self.alternar_grafica}
        self.add_connections(connections)
        cols = [['Producto/Partida','gobject.TYPE_STRING', 
                                                False, True, False, None], # 0
                ['m² A','gobject.TYPE_STRING', False, True, False, None],
                ['m² B','gobject.TYPE_STRING', False, True, False, None],
                ['m² C','gobject.TYPE_STRING', False, True, False, None],
                ['m² totales','gobject.TYPE_STRING', False, True, False, None],
                ['Kg A', 'gobject.TYPE_STRING', False, True, False, None],  # 5
                ['Kg teórico A', 
                    'gobject.TYPE_STRING', False, True, False, None], 
                ['Kg B','gobject.TYPE_STRING', False, True, False, None],
                ['Kg teórico B', 
                    'gobject.TYPE_STRING', False, True, False, None], 
                ['Kg C','gobject.TYPE_STRING', False, True, False, None],
                ['Kg totales','gobject.TYPE_STRING', 
                                                False, True, False, None], #10
                ['Bultos A', 'gobject.TYPE_INT64', 
                                                False, True, False, None], 
                ['Bultos B', 'gobject.TYPE_INT64', False, True, False, None],
                ['Bultos C', 'gobject.TYPE_INT64', False, True, False, None],
                ['Bultos totales', 'gobject.TYPE_INT64', 
                    False, True, False, None],
                ['Tiempo teórico', 'gobject.TYPE_STRING', 
                    False, True, False, None],                            # 15
                ['Tiempo real (total)', 'gobject.TYPE_STRING', 
                    False, True, False, None], 
                ['ID','gobject.TYPE_STRING', False, False, False, None]] 
        utils.preparar_treeview(self.wids['tv_gtx'], cols)
        for i in range(1, 17):
            col = self.wids['tv_gtx'].get_column(i)
            for cell in col.get_cell_renderers(): # One, actually
                cell.set_property("xalign", 1.0)
        for nombre_tv in ("tv_fibra", "tv_cem"):
            _cols = [c[:] for c in cols if not c[0].startswith('m² ') and 
                                                    not "Kg teórico" in c[0]]
            if nombre_tv == "tv_fibra": 
                _cols[0][0] = _cols[0][0].replace("Partida", "Lote")
            utils.preparar_treeview(self.wids[nombre_tv], _cols)
            for i in range(1, len(_cols) - 1):
                col = self.wids[nombre_tv].get_column(i)
                for cell in col.get_cell_renderers(): # One, actually
                    cell.set_property("xalign", 1.0)

        temp = time.localtime()
        self.fin = str(temp[0])+'/'+str(temp[1])+'/'+str(temp[2])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.wids['e_fechainicio'].set_text(
                utils.str_fecha(
                    mx.DateTime.localtime() - (7 * mx.DateTime.oneDay)))
        self.inicio = self.wids['e_fechainicio'].get_text().split('/')
        self.inicio.reverse()
        self.inicio = '/'.join(self.inicio)
        try:
            self.wids['im_graph'].set_visible(pychart_available)
        except AttributeError:
            self.wids['im_graph'].set_property("visible", pychart_available)
        self.wids['notebook1'].set_current_page(1)
        gtk.main()

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        for nombre_tv in ("tv_gtx", "tv_fibra", "tv_cem"):
            tv = self.wids[nombre_tv]
            abrir_csv(treeview2csv(tv))

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, tv, dic_prod, horas_huecos, tipo):
        """
        Rellena el model con los datos del diccionario.
        El diccionario está organizado por puid de producto y contiene 
        más diccionarios con las producciones en kg, m² (si corresponde), 
        bultos y lo mismo por lote/partida.
        """        
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        i = 0.0
        tot = len(dic_prod.keys())
        model = tv.get_model()
        model.clear()
        total_kilos_a = 0.0
        total_kilos_b = 0.0
        total_kilos_c = 0.0
        total_metros_a = 0.0
        total_metros_b = 0.0
        total_metros_c = 0.0
        total_bultos_a = 0
        total_bultos_b = 0
        total_bultos_c = 0
        total_t_teorico = mx.DateTime.DateTimeDelta(0)
        total_t_real = mx.DateTime.DateTimeDelta(0)
        total_huecos = 0.0
        for pvpuid in dic_prod:
            i += 1
            vpro.set_valor(i / tot, "Mostrando datos en ventana...")
            try:
                pv = pclases.getObjetoPUID(pvpuid)
                descripcion = pv.descripcion
            except : # Parte sin producción. Pero cuenta para tiempo.
                descripcion = "Sin producción"
            # Primero los datos por producto
            kilos_a = dic_prod[pvpuid]['kg']['a']
            total_kilos_a += kilos_a
            kilos_b = dic_prod[pvpuid]['kg']['b']
            total_kilos_b += kilos_b
            kilos_c = dic_prod[pvpuid]['kg']['c']
            total_kilos_c += kilos_c
            bultos_a = dic_prod[pvpuid]['#']['a']
            total_bultos_a += bultos_a
            bultos_b = dic_prod[pvpuid]['#']['b']
            total_bultos_b += bultos_b
            bultos_c = dic_prod[pvpuid]['#']['c']
            total_bultos_c += bultos_c
            try:
                metros_a = dic_prod[pvpuid]['m']['a']
                total_metros_a += metros_a
                metros_b = dic_prod[pvpuid]['m']['b']
                total_metros_b += metros_b
                metros_c = dic_prod[pvpuid]['m']['c']
                total_metros_c += metros_c
                peso_teorico_a = dic_prod[pvpuid]['peso_teorico']['a']
                peso_teorico_b = dic_prod[pvpuid]['peso_teorico']['b']
            except KeyError:    # Es fibra.
                metros_a = metros_b = metros_c = None
                peso_teorico_a = peso_teorico_b = None
            tiempo_teorico = dic_prod[pvpuid]['t_teorico']
            total_t_teorico += tiempo_teorico
            tiempo_real = dic_prod[pvpuid]['t_real']
            total_t_real += tiempo_real
            # Inserto la fila:
            fila = [descripcion, 
                    utils.float2str(kilos_a), 
                    utils.float2str(kilos_b), 
                    utils.float2str(kilos_c), 
                    utils.float2str(kilos_a + kilos_b + kilos_c), 
                    bultos_a, 
                    bultos_b, 
                    bultos_c, 
                    bultos_a + bultos_b + bultos_c, 
                    str_horas(tiempo_teorico), 
                    str_horas(tiempo_real), 
                    pvpuid
                   ]
            if not metros_a is None:
                fila = fila[:1] + [
                    utils.float2str(metros_a), 
                    utils.float2str(metros_b), 
                    utils.float2str(metros_c), 
                    utils.float2str(metros_a + metros_b + metros_c)] + fila[1:]
                fila.insert(6, utils.float2str(peso_teorico_a))
                fila.insert(8, utils.float2str(peso_teorico_b))
            iterproducto = model.append(None, fila)
            # Ahora los datos por lote/partida
            lista_lotes = dic_prod[pvpuid]['lotes_partidas']
            for lote_partida_puid in lista_lotes:
                try:
                    lote_partida = pclases.getObjetoPUID(lote_partida_puid)
                    codigo = lote_partida.codigo
                except: # No producción en el parte. Pero cuenta para tiempo.
                    codigo = "Sin producción"
                kilos_a = lista_lotes[lote_partida_puid]['kg']['a']
                kilos_b = lista_lotes[lote_partida_puid]['kg']['b']
                kilos_c = lista_lotes[lote_partida_puid]['kg']['c']
                bultos_a = lista_lotes[lote_partida_puid]['#']['a']
                bultos_b = lista_lotes[lote_partida_puid]['#']['b']
                bultos_c = lista_lotes[lote_partida_puid]['#']['c']
                try:
                    metros_a = lista_lotes[lote_partida_puid]['m']['a']
                    metros_b = lista_lotes[lote_partida_puid]['m']['b']
                    metros_c = lista_lotes[lote_partida_puid]['m']['c']
                    peso_teorico_a = lista_lotes[lote_partida_puid]['peso_teorico']['a']
                    peso_teorico_b = lista_lotes[lote_partida_puid]['peso_teorico']['b']
                except KeyError:    # Es fibra.
                    metros_a = metros_b = metros_c = None
                    peso_teorico_a = peso_teorico_b = None
                tiempo_teorico = lista_lotes[lote_partida_puid]['t_teorico']
                tiempo_real = lista_lotes[lote_partida_puid]['t_real']
                # Inserto la fila:
                fila = [codigo, 
                        utils.float2str(kilos_a), 
                        utils.float2str(kilos_b), 
                        utils.float2str(kilos_c), 
                        utils.float2str(kilos_a + kilos_b + kilos_c), 
                        bultos_a, 
                        bultos_b, 
                        bultos_c, 
                        bultos_a + bultos_b + bultos_c, 
                        str_horas(tiempo_teorico), 
                        str_horas(tiempo_real), 
                        lote_partida_puid
                       ]
                if not metros_a is None:
                    fila = fila[:1] + [
                        utils.float2str(metros_a), 
                        utils.float2str(metros_b), 
                        utils.float2str(metros_c), 
                        utils.float2str(metros_a + metros_b + metros_c)
                        ] + fila[1:]
                    fila.insert(6, utils.float2str(peso_teorico_a))
                    fila.insert(8, utils.float2str(peso_teorico_b))
                iterpartida = model.append(iterproducto, fila)
        self.rellenar_totales(total_kilos_a, total_kilos_b, total_kilos_c, 
                              total_bultos_a, total_bultos_b, total_bultos_c, 
                              total_metros_a, total_metros_b, total_metros_c, 
                              total_t_teorico, total_t_real, horas_huecos, 
                              tipo)
        vpro.ocultar()
    
    def rellenar_totales(self, kilos_a, kilos_b, kilos_c, bultos_a, bultos_b, 
                         bultos_c, metros_a, metros_b, metros_c, 
                         total_t_teorico, total_t_real, horas_huecos, 
                         tipo):
        if tipo == "gtx":
            pairs = [("e_%s_a_kg" % (tipo), 
                         utils.float2str(kilos_a)), 
                     ("e_%s_b_kg" % (tipo), 
                         utils.float2str(kilos_b)),
                     ("e_%s_c_kg" % (tipo), 
                         utils.float2str(kilos_c)),
                     ("e_%s_total_kg" % (tipo), 
                         utils.float2str(kilos_a + kilos_b + kilos_c)), 
                     ("e_%s_a_m2" % (tipo), 
                         utils.float2str(metros_a)), 
                     ("e_%s_b_m2" % (tipo), 
                         utils.float2str(metros_b)),
                     ("e_%s_c_m2" % (tipo), 
                         utils.float2str(metros_c)),
                     ("e_%s_total_m2" % (tipo), 
                         utils.float2str(metros_a + metros_b + metros_c)), 
                     ("e_%s_t_teorico" % (tipo), 
                         str_horas(total_t_teorico)), 
                     ("e_%s_t_real" % (tipo), 
                         str_horas(total_t_real)), 
                     ("e_%s_huecos" % (tipo), 
                         str_horas(horas_huecos)) 
                    ]
        else:
            pairs = [("e_%s_a" % (tipo), 
                         utils.float2str(kilos_a)), 
                     ("e_%s_b" % (tipo), 
                         utils.float2str(kilos_b)),
                     ("e_%s_c" % (tipo), 
                         utils.float2str(kilos_c)),
                     ("e_%s_total" % (tipo), 
                         utils.float2str(kilos_a + kilos_b + kilos_c)), 
                     ("e_%s_t_teorico" % (tipo), 
                         str_horas(total_t_teorico)), 
                     ("e_%s_t_real" % (tipo), 
                         str_horas(total_t_real)), 
                     ("e_%s_huecos" % (tipo), 
                         str_horas(horas_huecos)) 
                    ]
        for nombre_wid, dato in pairs:
            self.wids[nombre_wid].set_text(dato)
        
    def set_inicio(self, boton):
        self.inicio = utils.mostrar_calendario(padre = self.wids['ventana'], 
                fecha_defecto = self.wids['e_fechainicio'].get_text())
        self.inicio = utils.str_fecha(self.inicio)
        self.wids['e_fechainicio'].set_text(self.inicio)

    def set_fin(self, boton):
        self.fin = utils.mostrar_calendario(padre = self.wids['ventana'], 
                fecha_defecto = self.wids['e_fechafin'].get_text())
        self.fin = utils.str_fecha(self.fin)
        self.wids['e_fechafin'].set_text(self.fin)

    def buscar(self,boton):
        """
        Dadas fecha de inicio y de fin, busca los productos A y B
        fabricados y cantidad en los partes de producción.
        Para la producción C, que no lleva parte de producción, se filtra 
        directamente por la fecha y hora de los artículos. OJO: Y no 
        cuentan para los cómputos de tiempo.
        """
        PDP = pclases.ParteDeProduccion
        if not self.inicio:
            pdps = PDP.select(PDP.q.fecha < self.fin, 
                              orderBy = 'fechahorainicio')
        else:
            pdps = PDP.select(pclases.AND(PDP.q.fecha >= self.inicio, 
                                          PDP.q.fecha < self.fin), 
                              orderBy = 'fechahorainicio')
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        tot = pdps.count()
        i = 0.0
        vpro.mostrar()
        prod_balas = {}
        prod_pales = {}
        prod_rollos = {}
        huecos_fibra = 0.0
        huecos_gtx = 0.0
        huecos_cem = 0.0
        self.huecos = []    # Lista de los últimos partes tratados por línea.
        self.procesar_rollos_c(prod_rollos)
        self.procesar_balas_c(prod_balas)
        pdps_rollos = []
        for pdp in pdps:
            vpro.set_valor(i/tot, 'Analizando partes %s...' % (
                utils.str_fecha(pdp.fecha)))
            delta_entre_partes, parte_anterior = detectar_hueco(pdp, 
                                                                self.huecos)
            if (pdp.es_de_balas() 
                    and not "reenvas" in pdp.observaciones.lower()):
                self.procesar_pdp_balas(pdp, prod_balas)
                huecos_fibra += delta_entre_partes
            elif (pdp.es_de_bolsas() 
                    and not "reenvas" in pdp.observaciones.lower()):
                self.procesar_pdp_cajas(pdp, prod_pales)
                huecos_cem += delta_entre_partes
            elif pdp.es_de_rollos():
                self.procesar_pdp_rollos(pdp, prod_rollos)
                huecos_gtx += delta_entre_partes
                pdps_rollos.append(pdp)
            else:
                # WTF? ¿Nueva línea de producción? ¿Y yo con estos pelos?
                raise ValueError, "consulta_producido.py::buscar -> %s "\
                        "(%s) no es un parte de fibra, rollo ni cemento." % (
                                pdp.get_info(), pdp.puid)
            i += 1
        vpro.ocultar()
        self.rellenar_tabla(self.wids['tv_fibra'], prod_balas, huecos_fibra, 
                "fibra")
        self.rellenar_tabla(self.wids['tv_gtx'], prod_rollos, huecos_gtx, 
                "gtx")
        self.rellenar_tabla(self.wids['tv_cem'], prod_pales, huecos_cem, 
                "cem")
        self.dibujar_grafica(prod_balas, prod_rollos, prod_pales)
        self.resumen_gtx(pdps_rollos)

    def procesar_rollos_c(self, prod_rollos):
        if not self.inicio:
            rollosc = pclases.RolloC.select(
                    pclases.RolloC.q.fechahora < self.fin,
                              orderBy = 'fechahora')
        else:
            rollosc = pclases.RolloC.select(pclases.AND(
                                pclases.RolloC.q.fechahora >= self.inicio, 
                                pclases.RolloC.q.fechahora < self.fin), 
                              orderBy = 'fechahora')
        for rolloc in rollosc:
            key = rolloc.productoVenta.puid
            cantidad = rolloc.peso_sin
            tiempo_teorico = mx.DateTime.DateTimeDelta(0)
            tiempo_real = mx.DateTime.DateTimeDelta(0)
            metros = 0.0    # Producto C al peso.
            update_dic_producto(prod_rollos, rolloc.productoVenta, 'c', 
                                cantidad, metros, tiempo_teorico, tiempo_real)

    def procesar_balas_c(self, prod_balas):
        if not self.inicio:
            balasc = pclases.BalaCable.select(
                    pclases.BalaCable.q.fechahora < self.fin,
                              orderBy = 'fechahora')
        else:
            balasc = pclases.BalaCable.select(pclases.AND(
                                pclases.BalaCable.q.fechahora >= self.inicio, 
                                pclases.BalaCable.q.fechahora < self.fin), 
                              orderBy = 'fechahora')
        for balac in balasc:
            key = balac.productoVenta.puid
            cantidad = balac.peso_sin
            tiempo_teorico = mx.DateTime.DateTimeDelta(0)
            tiempo_real = mx.DateTime.DateTimeDelta(0)
            update_dic_producto(prod_balas, balac.productoVenta, 'c', cantidad,
                                0.0, tiempo_teorico, tiempo_real)

    def procesar_pdp_rollos(self, pdp, prod_rollos):
        for a in pdp.articulos:
            key = a.productoVenta.puid
            metros = a.superficie
            peso_sin = a.peso_sin
            tiempo_teorico = mx.DateTime.DateTimeDeltaFrom(
                    hours = a.calcular_tiempo_teorico())
            partida = a.partida
            try:
                peso_teorico = a.productoVenta.get_peso_teorico()
            except ValueError:
                peso_teorico = 0.0  # Producto sin peso teórico.
            if key not in prod_rollos:
                create_prod_rollo(prod_rollos, key)
            if a.es_clase_a():
                tipo = 'a'
            elif a.es_clase_b():
                tipo = 'b'
            elif a.es_clase_c():
                tipo = 'c'  # No debería, pues los partes solo llevan A y B.
            else:
                raise ValueError, "Artículo %s no es A, B ni C." % (a.puid)
            update_dic_producto(prod_rollos, a.productoVenta, tipo, peso_sin, 
                                metros, tiempo_teorico, 
                                peso_teorico = peso_teorico)
            update_lote_partida(prod_rollos[key], partida, tipo, peso_sin, 
                                metros, tiempo_teorico, 
                                peso_teorico = peso_teorico)
        # El tiempo real lo añado una vez por parte para evitar errores de 
        # precisión por redondeos.
        tiempo_real = pdp.get_duracion()
        try:
            update_dic_producto(prod_rollos, pdp.productoVenta, tipo, 0.0, 
                                0.0, mx.DateTime.DateTimeDelta(0), tiempo_real, 
                                bultos = 0, peso_teorico = 0)
            update_lote_partida(prod_rollos[pdp.productoVenta.puid], 
                                pdp.partida, tipo, 0.0, 0.0, 
                                mx.DateTime.DateTimeDelta(0), tiempo_real, 
                                bultos = 0, peso_teorico = 0)
        except (UnboundLocalError, AttributeError):
                    # No partida instanciada. No ha entrado en el for. No 
                    # artículos. No producción. No "tipo" instanciado siquiera.
            es_rollo = pdp.es_de_geotextiles()
            tipo = "a"  # Cuento el tiempo empleado como producción A para 
                        # el cálculo de productividad. Aunque no se haya 
                        # fabricado nada.
            update_dic_producto(prod_rollos, es_rollo, tipo, 0.0, 
                                0.0, mx.DateTime.DateTimeDelta(0), tiempo_real, 
                                bultos = 0, peso_teorico = 0)
            update_lote_partida(prod_rollos[None], 
                                pdp.partida, tipo, 0.0, 0.0, 
                                mx.DateTime.DateTimeDelta(0), tiempo_real, 
                                bultos = 0, peso_teorico = 0)

    def procesar_pdp_cajas(self, pdp, prod_pales):
        for a in pdp.articulos:
            key = a.productoVenta.puid
            peso_sin = a.peso_sin
            tiempo_teorico = mx.DateTime.DateTimeDeltaFrom(
                    hours = a.calcular_tiempo_teorico())
            partida = a.partidaCem
            if key not in prod_pales:
                create_prod_bala(prod_pales, key)
            if a.es_clase_a():
                tipo = 'a'
            elif a.es_clase_b():
                tipo = 'b'
            elif a.es_clase_c():
                tipo = 'c'  # No debería, pues los partes solo llevan A y B.
            else:
                raise ValueError, "Artículo %s no es A, B ni C." % (a.puid)
            update_dic_producto(prod_pales, a.productoVenta, tipo, peso_sin, 
                                tiempo_teorico = tiempo_teorico)
            update_lote_partida(prod_pales[key], partida, tipo, peso_sin, 
                                tiempo_teorico = tiempo_teorico)
        # El tiempo real lo añado una vez por parte para evitar errores de 
        # precisión por redondeos.
        tiempo_real = pdp.get_duracion()
        try:
            update_dic_producto(prod_pales, pdp.productoVenta, tipo, 0.0, 
                                tiempo_teorico = mx.DateTime.DateTimeDelta(0), 
                                tiempo_real = tiempo_real, 
                                bultos = 0)
            update_lote_partida(prod_pales[pdp.productoVenta.puid], 
                                pdp.partidaCem, tipo, 0.0, 
                                tiempo_teorico = mx.DateTime.DateTimeDelta(0), 
                                tiempo_real = tiempo_real, 
                                bultos = 0)
        except (UnboundLocalError, AttributeError):
                    # No partida instanciada. No ha entrado en el for. No 
                    # artículos. No producción. No "tipo" instanciado siquiera.
            es_rollo = pdp.es_de_geotextiles()
            tipo = "a"  # Cuento el tiempo empleado como producción A para 
                        # el cálculo de productividad. Aunque no se haya 
                        # fabricado nada.
            update_dic_producto(prod_rollos, es_rollo, tipo, 0.0, 
                                tiempo_teorico = mx.DateTime.DateTimeDelta(0), 
                                tiempo_real = tiempo_real, 
                                bultos = 0)
            update_lote_partida(prod_pales[None], 
                                pdp.partidaCem, tipo, 0.0, 
                                tiempo_teorico = mx.DateTime.DateTimeDelta(0), 
                                tiempo_real = tiempo_real, 
                                bultos = 0)

    def procesar_pdp_balas(self, pdp, prod_balas):
        for a in pdp.articulos:
            key = a.productoVenta.puid
            peso_sin = a.peso_sin
            tiempo_teorico = mx.DateTime.DateTimeDeltaFrom(
                    hours = a.calcular_tiempo_teorico())
            lote = a.lote or a.loteCem  # Dependiendo de si es fibra o 
                                        # geocem en bigbags
            if key not in prod_balas:
                create_prod_bala(prod_balas, key)
            if a.es_clase_a():
                tipo = 'a'
            elif a.es_clase_b():
                tipo = 'b'
            elif a.es_clase_c():
                tipo = 'c'  # No debería, pues los partes solo llevan A y B.
            else:
                raise ValueError, "Artículo %s no es A, B ni C." % (a.puid)
            update_dic_producto(prod_balas, a.productoVenta, tipo, peso_sin, 
                                tiempo_teorico = tiempo_teorico) 
            update_lote_partida(prod_balas[key], lote, tipo, peso_sin, 
                                tiempo_teorico = tiempo_teorico) 
        # El tiempo real lo añado una vez por parte para evitar errores de 
        # precisión por redondeos.
        tiempo_real = pdp.get_duracion() 
        try:
            update_dic_producto(prod_balas, pdp.productoVenta, tipo, 0.0, 
                                tiempo_teorico = mx.DateTime.DateTimeDelta(0), 
                                tiempo_real = tiempo_real, 
                                bultos = 0)
            update_lote_partida(prod_balas[pdp.productoVenta.puid], 
                                lote, tipo, 0.0,
                                tiempo_teorico = mx.DateTime.DateTimeDelta(0), 
                                tiempo_real = tiempo_real, 
                                bultos = 0)
        except (UnboundLocalError, AttributeError):
                    # No partida instanciada. No ha entrado en el for. No 
                    # artículos. No producción. No "tipo" instanciado siquiera.
            es_rollo = pdp.es_de_geotextiles()
            tipo = "a"  # Cuento el tiempo empleado como producción A para 
                        # el cálculo de productividad. Aunque no se haya 
                        # fabricado nada.
            update_dic_producto(prod_balas, es_rollo, tipo, 0.0, 
                                tiempo_teorico = mx.DateTime.DateTimeDelta(0), 
                                tiempo_real = tiempo_real, 
                                bultos = 0)
            # No lote. No producto.
            update_lote_partida(prod_balas[None], 
                                None, tipo, 0.0, 
                                tiempo_teorico = mx.DateTime.DateTimeDelta(0), 
                                tiempo_real = tiempo_real, 
                                bultos = 0)

    def alternar_grafica(self, *args, **kw): 
        if pychart_available:
            visible_pychart = self.wids['im_graph'].get_property("visible")
            visible_charting = self.wids['eventbox_chart'].get_property(
                                                                    "visible")
            if visible_pychart and visible_charting:
                ver_pychart = False
                ver_charting = True
            elif visible_pychart and not visible_charting:
                ver_pychart = True
                ver_charting = True
            elif not visible_pychart and visible_charting:
                ver_pychart = True
                ver_charting = False
            else:   # No debería darse nunca este estado.
                ver_pychart = True
                ver_charting = True
        else:
            ver_pychart = False
            ver_charting = True
        self.wids['im_graph'].set_property("visible", ver_pychart)
        self.wids['eventbox_chart'].set_property("visible", ver_charting)

    def dibujar_con_charting(self, data):
        try:
            oldchart = self.wids['eventbox_chart'].get_child()
            if oldchart != None:
                #self.wids['eventbox_chart'].remove(oldchart)
                chart = oldchart
            else:
                chart = charting.Chart(orient = "horizontal", 
                                       orient_vertical = False, 
                                       values_on_bars = True)
                self.wids['eventbox_chart'].add(chart)
            datachart = []
            color = 0
            for d in data:
                datachart.append((d[0], d[1], color))
                color += 1
                if color > 8:
                    color = 0
            chart.plot(datachart)
            self.wids['eventbox_chart'].show_all()
        except Exception, msg:
            txt = "consulta_producido.py::rellenar_tabla -> "\
                  "Error al dibujar gráfica (charting): %s" % msg
            print txt
            self.logger.error(txt)
 
    def dibujar_grafica(self, prod_fibra, prod_gtx, prod_cem):
        """
        Dibuja el gráfico de tarta. Si se mezclan balas y rollos, usa 
        kilogramos SOLO DE PRODUCTO A (balas o rollos). 
        """
        data = []
        for prod in (prod_fibra, prod_gtx, prod_cem):
            for pvid in prod:
                try:
                    desc = pclases.getObjetoPUID(pvid).descripcion.replace(
                            "/", "//")
                except: 
                    desc = "Sin producción"
                kg = prod[pvid]['kg']['a']
                data.append((desc, kg))
        self.dibujar_con_charting(data)
        if pychart_available and len(data) > 0:
            theme.use_color = True
            theme.reinitialize()
            tempdir = gettempdir()
            formato = "png"   # NECESITA ghostscript
            nombre_fichero = mx.DateTime.localtime().strftime(
                    "gcproducido_%Y_%m_%d_%H_%M_%S")
            nomarchivo = "%s.%s" % (nombre_fichero, formato)
            nombregraph = os.path.join(tempdir, "%s") % (nomarchivo)
            can = canvas.init(fname = nombregraph, format = formato)
            ar = area.T(size=(400, 200), 
                        legend=legend.T(), 
                        x_grid_style = None, 
                        y_grid_style = None)
            can.show(15, 150, 
                     "/a90/12/hRKg de fibra\ny geotextiles fabricados")
            plot = pie_plot.T(data=data, arc_offsets=[0,10,0,10],
                              shadow = (2, -2, fill_style.gray50),
                              label_offset = 25,
                              arrow_style = arrow.a3)
            ar.add_plot(plot)
            try:
                ar.draw(can)
            except ZeroDivisionError:
                return  # No hay datos suficientes para la gráfica.
            try:
                can.close()
                self.wids['im_graph'].set_size_request(410, 210)
                self.wids['im_graph'].set_from_file(nombregraph)
            except:
                utils.dialogo_info(titulo = "NECESITA GHOSTSCRIPT",
                    texto = "Para ver gráficas en pantalla necesita instalar"
                            " Ghostscript.\nPuede encontrarlo en el servidor"
                            " de la aplicación o descargarlo de la web "
                            "(http://www.cs.wisc.edu/~ghost/).",
                    padre = self.wids['ventana'])
            self.grafico = nombregraph
        else:
            self.wids['im_graph'].set_from_file(
                    "NOEXISTEPORTANTOVAADIBUJARUNASPA")
            self.grafico = None

    def imprimir(self,boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        from informes.treeview2pdf import treeview2pdf
        from formularios.reports import abrir_pdf
        for nombre_tv, titulo in (("tv_fibra", "Fibra"), 
                                  ("tv_gtx", "Geotextiles"),  
                                  ("tv_cem", "Fibra de cemento")):
            fecha = "[%s..%s)" % (self.inicio, self.fin)
            tv = self.wids[nombre_tv]
            totales = range(1, tv.get_model().get_n_columns() - 3)
            nome = nombre_tv.replace("tv", "e") + "_t_real"
            t_teorico = self.wids[nome].get_text()
            nome = nombre_tv.replace("tv", "e") + "_t_teorico"
            t_real = self.wids[nome].get_text()
            nome = nombre_tv.replace("tv", "e") + "_huecos"
            huecos = self.wids[nome].get_text()
            extra = (("Tiempo teórico: ", t_teorico) , 
                     ("Tiempo real: ", t_real) , 
                     ("Huecos entre partes: ", huecos))
            abrir_pdf(treeview2pdf(tv, 
                                   titulo = titulo, 
                                   fecha = fecha, 
                                   numcols_a_totalizar = totales, 
                                   extra_data = extra))

    def resumen_gtx(self, pdps):
        """
        Calcula totales del resumen únicamente en base a los partes recibidos.
        """
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        widnames = (("e_pdp_ini_gtx", obtener_fechahorainicio_primer_parte),
                    ("e_pdp_fin_gtx", obtener_fechahorafin_ultimo_parte), 
                    ("e_pdp_dif_gtx", obtener_diferencia_horas_partes), 
                    ("e_t_total_gtx", calcular_t_real_total), 
                    ("e_t_total_a_gtx", calcular_t_teorico), 
                    ("e_productividad_gtx", calcular_productividad), 
                    ("e_kg_teorico_a_gtx", calcular_kgs_teoricos_a), 
                    ("e_kg_real_a_gtx", calcular_kgs_reales_a), 
                    ("e_dif_real_teorico_gtx", calcular_diferencia_kgs_a), 
                    ("e_porcentaje_gtx", calcular_porcentaje_kgs), 
                    ("e_kg_real_b_gtx", calcular_kgs_reales_b), 
                    ("e_kg_real_c_gtx", calcular_kgs_reales_c), 
                    ("e_kg_real_total_gtx", calcular_kg_total), 
                    ("e_desviaciones_gtx", calcular_desviaciones), 
                    ("e_fibra_gtx", calcular_consumo), 
                    ("e_dif_cons_prod_gtx", calcular_diff_cons_prod)
                   )
        tot = len(widnames)
        i = 0.0
        vpro.set_valor(i / tot, "Calculando resumen de geotextiles...")
        pdps.sort(key = lambda p: p.fechahorainicio)
        for widname, func in widnames:
            i += 1
            vpro.set_valor(i / tot, 
                "Calculando resumen de geotextiles (%s)..." % (widname))
            if func.func_code.co_argcount == 1:
                result = func(pdps)
            elif func.func_code.co_argcount == 3:
                result = func(self.inicio, self.fin, pclases.RolloC)
            elif func.func_code.co_argcount == 4:
                result = func(pdps, self.inicio, self.fin, pclases.RolloC)
            else:
                # No debería
                result = None
            if result is None:
                str_result = ""
            else:
                if isinstance(result, float):
                    str_result = utils.float2str(result, precision = 2, 
                                                 autodec = True)
                elif utils.es_interpretable_como_fechahora(result):
                    str_result = utils.str_fechahora(result)
                elif isinstance(result, 
                                (type(mx.DateTime.DateTimeDelta(0)), 
                                 datetime.timedelta)):
                    str_result = str_horas(result)
                else:
                    str_result = str(result)
            self.wids[widname].set_text(str_result)
        vpro.ocultar()


def str_horas(fh):
    """
    Devuelve un TimeDelta en horas:minutos
    """
    if isinstance(fh, float):
        fh = mx.DateTime.DateTimeDeltaFrom(hours = fh)
    try:
        res = "%02d:%02d" % (fh.hour + fh.day * 24, fh.minute)
    except AttributeError:  # Es un datetime.timedelta
        hours, remainder = divmod(fh.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        res = "%02d:%02d" % (hours + fh.days * 24, minutes)
        if seconds:
            res += ":%02d" % seconds
    except:
        res = ''
    return res

def detectar_hueco(pdp, huecos):
    """
    Compara el parte con el último de los existentes de su tipo en el 
    diccionario y actualiza el tiempo faltante con la diferencia si 
    la hubiera.
    Si el tiempo entre dos partes del mismo tipo es de más de 8 horas se 
    considera que no ha habido turno y se ignora. Si es menor, se devuelve 
    el TimeDelta con la diferencia. 
    Además siempre se devuelve el parte anterior (si lo hubiera).
    """
    tiempo_faltante = mx.DateTime.DateTimeDeltaFrom(0)
    parte_anterior = None
    for last_parte in huecos[:]:    # Hay un parte de cada tipo en la lista 
                                    # para controlar huecos. Busco el de la 
                                    # misma línea que yo.
        if last_parte._es_del_mismo_tipo(pdp):
            huecos.remove(last_parte)
            parte_anterior = last_parte
            delta = pdp.fechahorainicio - last_parte.fechahorafin
            try:
                horas_delta = delta.total_seconds() / 60.0 / 60.0
            except AttributeError:
                try:
                    horas_delta = delta.hours
                except AttributeError:  # Versión <2.7 de Python
                    horas_delta = delta.days * 24 + delta.seconds / 60.0 / 60.0
            if 0 < horas_delta < 8:
                # Si el hueco es de más de un turno, es que no ha habido 
                # producción en ese turno.
                tiempo_faltante = delta
                if pclases.DEBUG:
                    print(">>> %f --> Hueco detectado entre %s y %s" % (
                        horas_delta, last_parte.get_info(), pdp.get_info()))
    huecos.append(pdp)
    return tiempo_faltante, parte_anterior

def create_prod_bala(prod_balas, puid):
    """
    Crea la estructura vacía de la producción de fibra (también palés).
    """
    prod_balas[puid]= {
            'kg': {'a': 0.0, 
                   'b': 0.0, 
                   'c': 0.0}, 
            '#': {'a': 0, 
                  'b': 0, 
                  'c': 0}, 
            't_real': mx.DateTime.DateTimeDelta(0), 
            't_teorico': mx.DateTime.DateTimeDelta(0),
            'lotes_partidas': {}
            }

def create_prod_rollo(prod_rollos, puid):
    """
    Crea la estructura vacía de la producción de geotextiles, que lleva m².
    """
    prod_rollos[puid]= {
            'kg': {'a': 0.0, 
                   'b': 0.0, 
                   'c': 0.0}, 
            'm': {'a': 0.0, 
                  'b': 0.0, 
                  'c': 0.0},
            '#': {'a': 0, 
                  'b': 0, 
                  'c': 0}, 
            't_real': mx.DateTime.DateTimeDelta(0), 
            't_teorico': mx.DateTime.DateTimeDelta(0),
            'peso_teorico': {'a': 0, 'b': 0}, 
            'lotes_partidas': {}
            }

def update_lote_partida(dic_producto, lote_partida, tipo, cantidad, 
                        metros = None, 
                        tiempo_teorico = mx.DateTime.DateTimeDelta(0), 
                        tiempo_real = mx.DateTime.DateTimeDelta(0), 
                        bultos = None, peso_teorico = 0):
    """
    Actualiza el lote/partida del producto en las cantidades 
    recibidas. Crea la clave si es necesario.
    Bultos vendrá a cero cuando queramos contar el tiempo total de un 
    parte, pero no incrementar la producción con un artículo en concreto.
    """
    try:
        puid_lote_partida = lote_partida.puid
        if bultos is None:  # No estoy actualizando tiempo total del parte.
            bultos = 1
    except AttributeError:  # CWT: No lote/partida. Parte sin producción, pero 
        puid_lote_partida = None    # cuenta para el tiempo empleado en A (sic)
        if bultos is None:  # No estoy actualizando tiempo total del parte.
            bultos = 0
    if puid_lote_partida not in dic_producto['lotes_partidas']:
        dic_producto['lotes_partidas'][puid_lote_partida] = {
                'kg': {'a': 0.0, 
                       'b': 0.0,
                       'c': 0.0}, 
                '#': {'a': 0, 
                      'b': 0, 
                      'c': 0}, 
                't_real': mx.DateTime.DateTimeDelta(0), 
                't_teorico': mx.DateTime.DateTimeDelta(0)
            }
        try:
            es_rollo = lote_partida.productoVenta.es_rollo()
        except AttributeError: # Ni siquiera tiene producto. ¿Qué hace aquí?
            # XXX: Puede entrar como tiempo teórico de un parte 
            # de rollos sin producción. lote_partida es aquí None, pero 
            # metros será None si es un parte de fibra y, al menos, 0 si es de 
            # rollos.
            es_rollo = metros != None
        if es_rollo:
            dic_producto['lotes_partidas'][puid_lote_partida]['m'] = {
                                                    'a': 0.0, 
                                                    'b': 0.0, 
                                                    'c': 0.0}
            dic_producto['lotes_partidas'][puid_lote_partida]['peso_teorico'] = {
                                                    'a': 0.0, 
                                                    'b': 0.0} # No C.
    dic_producto['lotes_partidas'][puid_lote_partida]['kg'][tipo] += cantidad
    dic_producto['lotes_partidas'][puid_lote_partida]['#'][tipo] += bultos
    dic_producto['lotes_partidas'][puid_lote_partida]['t_real'] += tiempo_real
    dic_producto['lotes_partidas'][puid_lote_partida]['t_teorico'] += tiempo_teorico
    try:
        dic_producto['lotes_partidas'][puid_lote_partida]['m'][tipo] += metros
        dic_producto['lotes_partidas'][puid_lote_partida]['peso_teorico'][tipo] += peso_teorico
    except KeyError:
        pass    # No es un rollo

def update_dic_producto(prod, pv, tipo, cantidad, metros = 0.0, 
                        tiempo_teorico = mx.DateTime.DateTimeDelta(0), 
                        tiempo_real = mx.DateTime.DateTimeDelta(0), 
                        bultos = None, peso_teorico = 0):
    """
    Actualiza la producción del artículo en el diccionario de producciones.
    Si no existe, lo agrega y después añade la información.
    """
    try:
        puid_pv = pv.puid
        es_rollo = pv.es_rollo() or pv.es_rollo_c()
        if bultos is None:  # No estoy actualizando tiempo real del parte, 
            bultos = 1      # que viene con bultos = 0.
    except AttributeError:
        puid_pv = None  # Parte sin producción.
        es_rollo = pv           # Si no tiene producción, aquí debe venir un 
                                # boolean que diga si es o no un geotextil.
        if bultos is None:  # No estoy actualizando tiempo real del parte.
            bultos = 0
    # Primero compruebo si lo creo o si ya se ha tratado y existe.
    if puid_pv not in prod:
        if es_rollo:
            create_prod_rollo(prod, puid_pv)
        else:
            create_prod_bala(prod, puid_pv)
    # Ahora actualizo de verdad.
    prod[puid_pv]['kg'][tipo] += cantidad
    prod[puid_pv]['#'][tipo] += bultos
    prod[puid_pv]['t_teorico'] += tiempo_teorico
    prod[puid_pv]['t_real'] += tiempo_real
    try:
        prod[puid_pv]['peso_teorico'][tipo] += peso_teorico
        prod[puid_pv]['m'][tipo] += metros
    except KeyError:    # No es rollo.
        pass

## Funciones auxiliares para el cálculo del resumen.
def obtener_fechahorainicio_primer_parte(pdps):
    try:
        res = min(pdps, key = lambda pdp: pdp.fechahorainicio).fechahorainicio
    except ValueError:
        res = None
    return res

def obtener_fechahorafin_ultimo_parte(pdps):
    try:
        res = max(pdps, key = lambda pdp: pdp.fechahorafin).fechahorafin
    except ValueError:
        res = None
    return res

def obtener_diferencia_horas_partes(pdps):
    ini = obtener_fechahorainicio_primer_parte(pdps)
    fin = obtener_fechahorafin_ultimo_parte(pdps)
    try:
        res = fin - ini
    except TypeError, msg:
        res = None
    return res

def calcular_t_real_total(pdps):
    res = sum([pdp.get_duracion() for pdp in pdps])
    return res

def calcular_t_teorico(pdps):
    res = sum([pdp.calcular_tiempo_teorico() for pdp in pdps])
    res = mx.DateTime.DateTimeDeltaFrom(hours = res)
    return res

def calcular_productividad(pdps):
    # Esto no lo puedo calcular como la media de los rendimientos a no ser 
    # que fuera media ponderada en función de los Kg producidos, que al final 
    # es más complejo que si lo calculamos con la misma fórmula pero aplicada 
    # al conjunto de los partes.
    #try:
    #    res = sum([pdp.calcular_rendimiento() for pdp in pdps]) / len(pdps)
    #except ZeroDivisionError:
    #    res = 0.0
    # OJO: Si volviera a cambiar la fórmula de la productividad, hay que 
    # redefinirla aquí también.
    try:
        kgs_a = sum([pdp.calcular_kilos_peso_estandar_A() for pdp in pdps])
    except ValueError:  # No soy de geotextiles.
        kgs_a = sum([pdp.calcular_kilos_producidos_A() for pdp in pdps])
    kgs_teoricos = sum([pdp.calcular_kilos_teoricos() for pdp in pdps])
    try:
        res = kgs_a * 100.0 / kgs_teoricos
    except ZeroDivisionError:
        res = 0.0
    return res

def calcular_kgs_teoricos_a(pdps):
    """
    Devuelve el total de Kgs de que deberían pesar los rollos A producidos    
    entre todos los partes recibidos.
    """
    res = 0.0
    for pdp in pdps:
        for a in pdp.articulos:
            if a.es_clase_a():
                try:
                    res += a.get_peso_teorico()
                except TypeError:   # Sin peso teórico.
                    pass
    return res

def calcular_kgs_reales_a(pdps):
    """
    Devuelve los kgs reales sin embalaje producidos en A entre todos los 
    partes.
    """
    res = sum([pdp.calcular_kilos_producidos_A() for pdp in pdps])
    return res

def calcular_diferencia_kgs_a(pdps):
    """
    Devuelve la diferencia entre los Kgs reales de A y los teóricos de A para 
    todos los partes.
    """
    reales = calcular_kgs_reales_a(pdps)
    teoricos = calcular_kgs_teoricos_a(pdps)
    res = reales - teoricos
    return res

def calcular_porcentaje_kgs(pdps):
    """
    Devuelve el porcentaje que representa la diferencia entre kgs reales y 
    teóricos sobre los kilos teóricos de A que deberían haber dado los partes.
    """
    diferencia = calcular_diferencia_kgs_a(pdps)
    teoricos = calcular_kgs_teoricos_a(pdps)
    try:
        res = diferencia * 100.0 / teoricos
    except ZeroDivisionError:
        res = 0.0
    return res

def calcular_kgs_reales_b(pdps):
    """
    Devuelve los kgs de B reales sin embalaje producidos en los partes.
    """
    res = sum([pdp.calcular_kilos_producidos_B() for pdp in pdps])
    return res

def calcular_kgs_reales_c(fini, ffin, claseC):
    """
    Devuelve los kgs de C reales sin embalaje producidos entre las fechas 
    recibidas (la fecha final no entra) del tipo de clase C recibido 
    (pclases.RolloC o pclases.BalaC).
    """
    # res = sum([pdp.calcular_kilos_producidos_C() for pdp in pdps])
    # Esto no se puede hacer así porque los artículos C no van en los partes 
    # de producción DE MOMENTO. Así que lo calculo mirando las fechas 
    # inicial y final de
    res = 0.0
    objs = claseC.select(pclases.AND(claseC.q.fechahora >= fini, 
                                     claseC.q.fechahora < ffin))
    res = sum([o.articulo.peso_sin for o in objs])
    return res

def calcular_kg_total(pdps, fini, ffin, claseC):
    """
    Devuelve los kilos reales totales fabricados de A+B+C.
    """
    A = calcular_kgs_reales_a(pdps)
    B = calcular_kgs_reales_b(pdps)
    C = calcular_kgs_reales_c(fini, ffin, claseC)
    res = A + B + C
    return res

def calcular_desviaciones(pdps, fini, ffin, claseC):
    """
    Devuelve la suma de desviaciones (artículos B, artículos C y 
    diferencia entre A teóricos y A reales) sobre A.
    """
    # Esto es casi pura programación funcional. Me va a costar mucho tiempo 
    # repitiendo llamadas a funciones para calcular los mismos resultados en 
    # varios sitios que en Erlang estaría totalmente optimizado. For sure!
    diferencia_teoricos_reales = calcular_diferencia_kgs_a(pdps)
    B = calcular_kgs_reales_b(pdps)
    C = calcular_kgs_reales_c(fini, ffin, claseC)
    res = diferencia_teoricos_reales + B + C
    return res

def calcular_consumo(pdps):
    """
    Devuelve el "consumo" de materia prima en kgs de los partes de producción 
    recibidos.
    En el caso de la fibra es la suma de consumos de granza.
    En el caso de los geotextiles es la suma de la fibra CARGADA en los 
    cuartos para las partidas fabricadas en los partes.
    En el caso del cemento es la suma de los bigbags cargados en los partes.
    En el caso de los productos C (rollos C y balas de cable) es cero porque 
    actualmente no consumen (DE MOMENTO) y además no pertenecen a partes de
    producción "estándar", así que no se le invocaría porque no habría pdps.
    """
    try:
        pdp = pdps[0]
    except IndexError:  # No partes. No consumos.
        res = 0.0
    else:
        res = sum([pdp.calcular_consumo_mp() for pdp in pdps])
    return res

def calcular_diff_cons_prod(pdps, fini, ffin, claseC):
    """
    Devuelve la diferencia entre los kilos producidos sin embalaje de A, B y C 
    con los kilos de materia prima cargados o consumidos por los partes.
    """
    producido = calcular_kg_total(pdps, fini, ffin, claseC)
    consumido = calcular_consumo(pdps)
    res = consumido - producido
    return res

if __name__ == '__main__':
    t = ConsultaProducido() 

