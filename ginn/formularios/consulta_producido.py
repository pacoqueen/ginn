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
                       "b_exportar/clicked": self.exportar}
        self.add_connections(connections)
        cols = (('Producto/Lote','gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Cantidad producida','gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Bultos', 'gobject.TYPE_INT64', False, True, False, None),
                ('Media por unidad', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Kg teóricos', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Tiempo teórico', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Tiempo real', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('ID','gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        for i in (1, 2, 3, 4, 5, 6):
            col = self.wids['tv_datos'].get_column(i)
            for cell in col.get_cell_renderers(): # One, actually
                cell.set_property("xalign", 1.0)
        cols = (('Grupo', 'gobject.TYPE_STRING', False, True, True, None), 
                ('Producción', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Kg teóricos', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Tiempo teórico', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Tiempo real', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('ID', 'gobject.TYPE_INT64', False, None, None, None))
        utils.preparar_listview(self.wids['tv_ford'], cols)
        for i in (2, 3, 4):
            col = self.wids['tv_ford'].get_column(i)
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
        self.wids['rb_todas'].set_active(True)
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
        Rellena el model con los items de la consulta.
        "items" es una lista de 4 elementos: Nombre producto, cantidad, ID y X.
        En la última columna del model (la oculta) se guarda un string "ID:X" 
        donde X es R si es un rollo (geotextil) o B si es bala (fibra).
        """        
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        i = 0.0
        tot = len(items)
        model = self.wids['tv_datos'].get_model()
        model.clear()
        for item in items:
            i += 1
            vpro.set_valor(i / tot, "Mostrando datos en ventana...")
            try:
                kilos_teoricos = utils.float2str(item[7])
            except ValueError:  # Es bala o caja. No tiene.
                kilos_teoricos = "" 
            tiempo_teorico = str_horas(
                    mx.DateTime.TimeDeltaFrom(hours = item[8]))
            tiempo_real = str_horas(
                    mx.DateTime.TimeDeltaFrom(hours = item[9]))
            itr = model.append(None, (item[0],
                                      item[1],
                                      item[4],
                                      utils.float2str(item[5]), 
                                      kilos_teoricos, 
                                      tiempo_teorico, 
                                      tiempo_real, 
                                      "%d:%s" % (item[2], item[3])))
            for lote_partida in item[6]:
                cantidad = item[6][lote_partida]['cantidad']
                bultos = item[6][lote_partida]['bultos']
                horas_teoricas = item[6][lote_partida]['tiempo']
                horas_reales = item[6][lote_partida]['t_real']
                media = cantidad / bultos
                try:
                    pv = lote_partida.rollos[0].productoVenta
                    kilos_teoricos_lote_partida = utils.float2str(
                        bultos * pv.get_peso_teorico())
                except (ValueError, IndexError, AttributeError):
                    # Es bala, cemento o especial. No tiene.
                    kilos_teoricos_lote_partida = ""
                try:
                    horas_teoricas = mx.DateTime.TimeDeltaFrom(
                            hours = horas_teoricas)
                    tiempo_teorico = str_horas(horas_teoricas)
                except ZeroDivisionError:
                    tiempo_teorico = ""
                try:
                    horas_reales = mx.DateTime.TimeDeltaFrom(
                            hours = horas_reales)
                    tiempo_real = str_horas(horas_reales)
                except ZeroDivisionError:
                    tiempo_real = ""
                model.append(itr, (lote_partida and lote_partida.codigo or "?", 
                                   utils.float2str(cantidad), 
                                   bultos, 
                                   utils.float2str(media), 
                                   # PORASQUI: Me queda: arreglar gráfica en entornos Windows 
                                   kilos_teoricos_lote_partida, 
                                   tiempo_teorico, 
                                   tiempo_real, 
                                   "%d:LP" % (lote_partida.id)
                                  ))
        vpro.ocultar()
        
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
    
    def get_lineas_produccion(self):
        linea = pclases.LineaDeProduccion.select(
                pclases.LineaDeProduccion.q.nombre.contains('geotextil'))
        if linea.count() == 0:
            linea_gtx = None
        else:
            linea_gtx = linea[0]
        linea = pclases.LineaDeProduccion.select(
                pclases.LineaDeProduccion.q.nombre.contains('fibra'))
        if linea.count() == 0:
            linea_fib = None
        else:
            linea_fib = linea[0]
        return linea_gtx, linea_fib
        
    def buscar(self,boton):
        """
        Dadas fecha de inicio y de fin, busca los productos 
        fabricados y cantidad en los partes de producción.
        """
        PDP = pclases.ParteDeProduccion
        if not self.inicio:
            pdps = PDP.select(PDP.q.fecha <= self.fin, 
                              orderBy = 'fechahorainicio')
        else:
            pdps = PDP.select(pclases.AND(PDP.q.fecha >= self.inicio, 
                                          PDP.q.fecha <= self.fin), 
                              orderBy = 'fechahorainicio')
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        tot = pdps.count()
        i = 0.0
        vpro.mostrar()
        prod_balas = {}
        prod_pales = {}
        prod_rollos = {}
        ford = {}
        self.tiempo_faltante = mx.DateTime.TimeDeltaFrom(0)
        self.huecos = []    # Lista de los últimos partes tratados por línea.
        for pdp in pdps:
            vpro.set_valor(i/tot, 'Analizando partes %s...' % (
                utils.str_fecha(pdp.fecha)))
            delta_entre_partes, parte_anterior = detectar_hueco(pdp, 
                                                                self.huecos)
            self.tiempo_faltante += delta_entre_partes
            if (pdp.es_de_balas() 
                and not "reenvas" in pdp.observaciones.lower() 
                and (self.wids['rb_todas'].get_active() 
                     or self.wids['rb_fibra'].get_active())):
                self.agregar_parte_a_dicford(ford, pdp)
                self.procesar_pdp_balas(pdp, prod_balas)
            elif (pdp.es_de_bolsas() 
                  and (self.wids['rb_todas'].get_active() 
                       or self.wids['rb_embolsado'].get_active())):
                self.agregar_parte_a_dicford(ford, pdp)
                self.procesar_pdp_cajas(pdp, prod_pales)
            elif (pdp.es_de_rollos() and 
                  (self.wids['rb_todas'].get_active() 
                   or self.wids['rb_geotextiles'].get_active())):
                self.agregar_parte_a_dicford(ford, pdp)
                self.procesar_pdp_rollos(pdp, prod_rollos)
            i += 1
        # Gráfico usando PyChart:
        data = []
        self.resultado = []
        for k in prod_balas:
            cantidad = "%s %s" % (utils.float2str(prod_balas[k][1], 1), 
                                  prod_balas[k][4])
            tiempo_teorico = prod_balas[k][7]
            try:
                peso_teorico = prod_balas[k][8]
                tiempo_real = prod_balas[k][9]
            except IndexError:
                peso_teorico = ""
                tiempo_real = prod_balas[k][8]
            self.resultado.append([prod_balas[k][0],    # ?
                                   cantidad,            # Cantidad como cadena 
                                                        # de texto, con 
                                                        # unidades.
                                   prod_balas[k][2],    # ?
                                   prod_balas[k][3],    # ?
                                   prod_balas[k][5],    # ?
                                   prod_balas[k][1] / prod_balas[k][5], # Peso
                                                        # medio por bala/saca.
                                   prod_balas[k][6],
                                   peso_teorico, 
                                   tiempo_teorico, 
                                   tiempo_real
                                  ])
            data.append((prod_balas[k][0].replace("/", "//"), 
                         prod_balas[k][1], 
                         prod_balas[k][5]))
        for k in prod_pales:
            cantidad = "%s %s" % (utils.float2str(prod_pales[k][1], 1), 
                                  prod_pales[k][4])
            tiempo_teorico = prod_pales[k][7]
            try:
                peso_teorico = prod_pales[k][8]
                tiempo_real = prod_pales[k][9]
            except IndexError:
                peso_teorico = ""
                tiempo_real = prod_pales[k][8]
            self.resultado.append([prod_pales[k][0],    # ?
                                   cantidad,            # Cantidad como cadena 
                                                        # de texto, con 
                                                        # unidades.
                                   prod_pales[k][2],    # ?
                                   prod_pales[k][3],    # ?
                                   prod_pales[k][5],    # ?
                                   prod_pales[k][1] / prod_pales[k][5], # Peso
                                                        # medio por caja.
                                   prod_pales[k][6], 
                                   peso_teorico, 
                                   tiempo_teorico, 
                                   tiempo_real
                                  ])
            data.append((prod_pales[k][0].replace("/", "//"), 
                         prod_pales[k][1], 
                         prod_pales[k][5]))
        for k in prod_rollos:
            cantidad = "%s %s" % (utils.float2str(prod_rollos[k][1], 1), 
                                  prod_rollos[k][4])
            tiempo_teorico = prod_rollos[k][7]
            try:
                peso_teorico = prod_rollos[k][8]
                tiempo_real = prod_rollos[k][9]
            except IndexError:
                peso_teorico = ""
                tiempo_real = prod_rollos[k][8]
            self.resultado.append([prod_rollos[k][0],   # ?
                                   cantidad,            # Cantidad como 
                                                        # cadena, con unidades 
                                   prod_rollos[k][2],   # ?
                                   prod_rollos[k][3],   # ?
                                   prod_rollos[k][5],   # ?
                                   prod_rollos[k][1]/prod_rollos[k][5], 
                                    # Metros cuadrados medio por rollo (no 
                                    # tiene mucho sentido, pero bueno)
                                   prod_rollos[k][6],   # Producción / partida
                                   peso_teorico, 
                                   tiempo_teorico, 
                                   tiempo_real
                                  ])
            data.append((prod_rollos[k][0].replace("/", "//"), 
                         prod_rollos[k][1], 
                         prod_rollos[k][5]))
        self.dibujar_grafico(data)
        # Totales
        self.tiempo_teorico = 0.0   # \
        self.peso_teorico = 0.0     #  }-> Se actualizan en el calcular_totales
        self.tiempo_real = 0.0      # /
        kilos, bultos_fibra = self.calcular_totales(prod_balas)
        metros, bultos_gtx = self.calcular_totales(prod_rollos)
        kilospales, bultos_pales = self.calcular_totales(prod_pales)
        self.kilos = kilos
        self.metros = metros
        self.kilospales = kilospales
        self.rollos = bultos_gtx
        self.balas = bultos_fibra
        self.pales = bultos_pales
        self.wids['e_total_fibra'].set_text("%s (%s balas)" % (
            utils.float2str(kilos), bultos_fibra))
        self.wids['e_total_pales'].set_text("%s (%s cajas)" % (
            utils.float2str(kilospales), bultos_pales))
        self.wids['e_total_gtx'].set_text("%s (%s rollos)" % (
            utils.float2str(metros), bultos_gtx))
        horas_teoricas = mx.DateTime.TimeDeltaFrom(hours = self.tiempo_teorico)
        horas_reales = mx.DateTime.TimeDeltaFrom(hours = self.tiempo_real)
        self.wids['e_total_tiempo_teorico'].set_text(
                str_horas(horas_teoricas))
        self.wids['e_total_peso_teorico'].set_text(
                utils.float2str(self.peso_teorico))
        str_tiempo_total = str_horas(horas_reales)
        if self.tiempo_faltante:
            str_tiempo_total += " + (%s hasta completar turnos)" % (
                    str_horas(self.tiempo_faltante))
        self.wids['e_total_tiempo_real'].set_text(
                str_tiempo_total)
        vpro.ocultar()
        self.rellenar_tabla(self.resultado)
        self.rellenar_tabla_fordiana(ford)

    def procesar_pdp_rollos(self, pdp, prod_rollos):
        # Añado ProductoVenta de los rollos.
        tiempo_real = pdp.get_duracion().hours
        for a in pdp.articulos:
            #key = "%d:R" % (a.productoVentaID)
            key = a.productoVenta.puid
            try:
                cantidad = a.superficie
            except AttributeError, error:
                self.logger.error("consulta_producido::procesar_pdp_rollos -> "
                                  "Falló el acceso a las propiedades "
                                  "de producto de venta del rollo: "
                                  "%s" % (error))
                cantidad = 0.0
            try: 
                prod_rollos[key][1] += cantidad
                prod_rollos[key][5] += 1
                tiempo_teorico = a.calcular_tiempo_teorico()
                try:
                    prod_rollos[key][6][a.partida]['cantidad'] += a.superficie
                    prod_rollos[key][6][a.partida]['bultos'] += 1
                    prod_rollos[key][6][a.partida]['tiempo'] += tiempo_teorico
                except KeyError:
                    prod_rollos[key][6][a.partida] = {
                            'cantidad' : a.superficie, 
                            'bultos' : 1, 
                            'tiempo': tiempo_teorico, 
                            't_real': 0.0}
                prod_rollos[key][7] += tiempo_teorico
                prod_rollos[key][8] += a.rollo.peso_teorico
            except KeyError:
                tiempo_teorico = a.calcular_tiempo_teorico()
                prod_rollos[key] = [a.productoVenta.descripcion,    # 0
                                    cantidad,                       # 1
                                    a.productoVenta.id,             # 2
                                    'R',                            # 3
                                    'm²',                           # 4
                                    1,                              # 5
                                    {a.partida:                     # 6
                                        {'cantidad': a.superficie, 
                                         'bultos': 1, 
                                         'tiempo': tiempo_teorico, 
                                         't_real': 0.0}},
                                    tiempo_teorico,                 # 7
                                    a.rollo.peso_teorico            # 8
                                   ]
        try:
            try:
                prod_rollos[key][9] += tiempo_real
            except IndexError:
                prod_rollos[key].append(tiempo_real)                # 9
            prod_rollos[key][6][a.partida]['t_real'] += tiempo_real
        except (KeyError, UnboundLocalError):
            pass        # ¿Parte sin producción? 

    def procesar_pdp_cajas(self, pdp, prod_pales):
        # Añado ProductoVenta de los palés.
        tiempo_real = pdp.get_duracion().hours
        for a in pdp.articulos:
            #key = "%d:P" % (a.productoVentaID)
            key = a.productoVenta.puid
            try: 
                prod_pales[key][1] += a.peso
                tiempo_teorico = a.calcular_tiempo_teorico()
                try:
                    prod_pales[key][6][a.partidaCem]['cantidad'] \
                        += a.peso
                    prod_pales[key][6][a.partidaCem]['bultos'] \
                        += a.caja.numbolsas
                    prod_pales[key][6][a.partidaCem]['tiempo'] \
                        += tiempo_teorico
                except KeyError:
                    prod_pales[key][6][a.partidaCem] = {
                        'cantidad':a.peso,
                        'bultos': a.caja.numbolsas, 
                        'tiempo': tiempo_teorico, 
                        't_real': 0.0}
                prod_pales[key][5] += 1
                prod_pales[key][7] += tiempo_teorico
            except KeyError:
                tiempo_teorico = a.calcular_tiempo_teorico()
                prod_pales[key] = [a.productoVenta.descripcion,         # 0
                                   a.peso, 
                                   a.productoVenta.id, 
                                   'P', 
                                   'kg', 
                                   1,                                   # 5
                                   {a.partidaCem: 
                                        {'cantidad': a.peso, 
                                         'bultos': a.caja.numbolsas, 
                                         'tiempo': tiempo_teorico, 
                                         't_real': 0.0}}, 
                                   tiempo_teorico,                      # 7
                                  ]     # No lleva peso teórico
        try:
            try:
                prod_pales[key][8] += tiempo_real
            except IndexError:
                prod_pales[key].append(tiempo_real)                # 9
            prod_pales[key][6][a.partidaCem]['t_real'] += tiempo_real
        except (KeyError, UnboundLocalError):
            pass    # `key` no instanciada. ¿Parte sin producción?

    def procesar_pdp_balas(self, pdp, prod_balas):
        # Añado ProductoVenta de las balas.
        tiempo_real = pdp.get_duracion().hours
        for a in pdp.articulos:
            #key = "%d:B" % (a.productoVentaID)
            key = a.productoVenta.puid
            try:
                peso = a.bala.pesobala
                lote = a.lote
            except AttributeError:  # Es cemento
                peso = a.bigbag.pesobigbag
                lote = a.loteCem
            tiempo_teorico = a.calcular_tiempo_teorico()
            try: 
                prod_balas[key][1] += peso
                try:
                    prod_balas[key][6][lote]['cantidad'] += peso
                    prod_balas[key][6][lote]['bultos'] += 1
                    prod_balas[key][6][lote]['tiempo'] += tiempo_teorico
                except KeyError:
                    prod_balas[key][6][lote]={'cantidad': peso,
                                              'bultos': 1, 
                                              'tiempo': tiempo_teorico, 
                                              't_real': 0.0}
                        # De verdad que es absurdo llamar «key» a la 
                        # variable que hace de "key". No tiene nombre 
                        # descriptivo y ahora no sé lo qué es. ¿Una 
                        # bala? ¿Un producto? ¿Un parte? ¿Un consumo? 
                        # ¿Ves lo que pasa, Larry? ¡¿Ves lo que pasa 
                        # cuando intentas dar por culo a un 
                        # desconocido?! ¡Esto es lo que pasa, Larry!
                prod_balas[key][5] += 1
                prod_balas[key][7] += tiempo_teorico
            except KeyError:
                tiempo_teorico = a.calcular_tiempo_teorico()
                prod_balas[key] = [a.productoVenta.descripcion,     # 0
                                   peso, 
                                   a.productoVenta.id, 
                                   'B', 
                                   'kg', 
                                   1,                               # 5
                                   {lote: {'cantidad': peso, 
                                           'bultos': 1, 
                                           'tiempo': tiempo_teorico, 
                                           't_real': 0.0}}, 
                                   tiempo_teorico                   # 7
                                  ]     # Tampoco tienen peso teórico
        try:
            try:
                prod_balas[key][8] += tiempo_real
            except IndexError:
                prod_balas[key].append(tiempo_real)                # 9
            prod_balas[key][6][lote]['t_real'] += tiempo_real
        except (KeyError, UnboundLocalError):
            pass    # `key` no instanciada. ¿Parte sin producción?


    def agregar_parte_a_dicford(self, ford, parte):
        """
        Añade la producción proporcional del parte al diccionario 
        por grupos.
        Si un parte tiene varios grupos, la producción se reparte 
        entre las horas trabajadas en total de cada grupo.
        """
        grupos = parte.get_grupos()
        produccion = parte.get_produccion()
        total_horas = sum([grupos[g] for g in grupos])
        for grupo in grupos:
            try:
                producido_proporcional = (produccion[0] 
                                      *(grupos[grupo].hours/total_horas.hours))
                try:
                    peso_teorico = parte.productoVenta.get_peso_teorico()
                    kilos_teoricos = (len(parte.articulos) * peso_teorico 
                            * (grupos[grupo].hours / total_horas.hours))
                    horas_teoricas = kilos_teoricos / parte.prodestandar 
                    horas_reales = parte.get_duracion().hours
                except (ValueError, AttributeError):
                    kilos_teoricos = 0
                    horas_teoricas = 0
                    horas_reales = 0
            except ZeroDivisionError:
                # Valor de horas nulo. No cuenta para el informe.
                producido_proporcional = 0.0
                self.to_log("[agregar_parte_a_dicford] Parte con duración 0.", 
                        {"parte de producción": parte, 
                         "producción": produccion, 
                         "total_horas": total_horas, 
                         "grupos": grupos})
            if grupo not in ford:
                ford[grupo] = {'tiempo_teorico': 0.0, 
                               'peso_teorico': 0.0, 
                               'tiempo_real': 0.0}
            if produccion[1] not in ford[grupo]:
                ford[grupo][produccion[1]] = producido_proporcional
            else:
                ford[grupo][produccion[1]] += producido_proporcional
            ford[grupo]['peso_teorico'] += kilos_teoricos
            ford[grupo]['tiempo_teorico'] += horas_teoricas
            ford[grupo]['tiempo_real'] += horas_reales

    def preparar_diccionario_ford(self, fechaini, fechafin):
        """
        Prepara un diccionario cuyas claves son una tupla (fechahorainicio, 
        fechahorafin).
        Si fechaini es None, fechahorainicio será la fecha más antigua de los 
        partes de la BD a las 6:00.
        Todas las tuplas irán en intervalo de 06:00 a 14:00, 14:00 a 
        22:00 y 22:00 a 06:00.
        DEPRECATED: Agrupo mejor por grupos, en lugar de por turnos.
        """
        dic = {}
        if not fechaini:
            fechaini = pclases.ParteDeProduccion._queryOne(
                "SELECT MIN(fecha) FROM parte_de_produccion")[0]
        fechahorainicio = fechaini + mx.DateTime.oneHour * 6
        delta = mx.DateTime.oneHour * 8
        fechahorafin = fechahorainicio + delta
        rango_sup = fechafin + mx.DateTime.oneHour * 6
        while fechahorafin < rango_sup:
            turno = (fechahorainicio, fechahorafin)
            dic[turno] = {}
        return dic
    
    def rellenar_tabla_fordiana(self, ford):
        """
        Rellena la tabla de producción por turnos.
        """
        model = self.wids['tv_ford'].get_model()
        model.clear()
        for grupo in ford:
            produccion = []
            for unidad in ford[grupo]:
                if unidad in ("peso_teorico", "tiempo_teorico", "tiempo_real"):
                    continue
                produccion.append("%s %s" % (
                    utils.float2str(ford[grupo][unidad], 3, autodec = True), 
                    unidad))
            tiempo_teorico = str_horas(mx.DateTime.TimeDeltaFrom(
                    hours = ford[grupo]['tiempo_teorico']))
            tiempo_real = str_horas(mx.DateTime.TimeDeltaFrom(
                    hours = ford[grupo]['tiempo_real']))
            peso_teorico = utils.float2str(ford[grupo]['peso_teorico'])
            nombregrupo = grupo and grupo.nombre or "Sin grupo"
            model.append((nombregrupo, 
                          "; ".join(produccion), 
                          peso_teorico, 
                          tiempo_teorico, 
                          tiempo_real, 
                          0))

    def calcular_totales(self, prod):
        """
        Calcula el total en cantidad y bultos del 
        diccionario de producción recibido.
        """
        cantidad = sum([prod[p][1] for p in prod])
        bultos = sum([prod[p][5] for p in prod])
        self.tiempo_teorico += sum([prod[p][7] for p in prod])
        try:
            self.tiempo_real += sum([prod[p][9] for p in prod])
            self.peso_teorico += sum([prod[p][8] for p in prod])
        except IndexError:  # No tiene peso teórico
            self.tiempo_real += sum([prod[p][8] for p in prod])
        return (cantidad, bultos)

    def dibujar_grafico(self, data):
        """
        Dibuja el gráfico de tarta. Si se mezclan balas y rollos, usa 
        unidades (balas o rollos). 
        Si es solo de geotextiles o de fibra, se usan sus unidades 
        (metros o kilos).
        """
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
            if self.wids['rb_todas'].get_active():
                data = [(d[0], d[2]) for d in data]
                can.show(15, 150, 
                         "/a90/12/hRNúmero de balas\ny rollos fabricados")
            else:
                data = [(d[0], d[1]) for d in data]
                if self.wids['rb_fibra'].get_active():
                    can.show(15, 150, "/a90/12/hRKilos de\nfibra fabricados")
                elif self.wids['rb_geotextiles'].get_active():
                    can.show(15, 150, 
                             "/a90/12/hRMetros cuadrados de\ngeotextiles fabricados")
            plot = pie_plot.T(data=data, arc_offsets=[0,10,0,10],
                              shadow = (2, -2, fill_style.gray50),
                              label_offset = 25,
                              arrow_style = arrow.a3)
            ar.add_plot(plot)
            ar.draw(can)
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
        from formularios import reports
        datos = []
        model = self.wids['tv_datos'].get_model()
        for i in model:
            datos.append((i[0],     # Descripción
                          i[1],     # Cantidad producida
                          i[2],     # Bultos
                          i[4],     # Kg teóricos
                          i[5]))    # Tiempo teórico
        if self.balas != 0:
            datos.append(("", "", "", "", ""))
            datos.append(("", "-" * 30 , "-" * 30, "-" * 30, "-" * 30))
            datos.append(("", "", "", "", ""))
            datos.append((" " * 50 + "TOTAL FIBRA:", 
                          "%s kg" % (utils.float2str(self.kilos)), 
                          self.balas, 
                          "", 
                          ""))
        if self.rollos != 0:
            datos.append(("", "", "", "", ""))
            datos.append(("", "-" * 30, "-" * 30, "-" * 30, "-" * 30))
            datos.append(("", "", "", "", ""))
            datos.append((" " * 50 + "TOTAL GEOTEXTILES:", 
                          "%s m²" % (utils.float2str(self.metros)), 
                          self.rollos, 
                          self.wids['e_total_peso_teorico'].get_text(), 
                          self.wids['e_total_tiempo_teorico'].get_text()))
        if (self.inicio) == None:            
            fechaInforme = 'Hasta ' + utils.str_fecha(
                    time.strptime(self.fin,"%Y/%m/%d"))
        else:
            fechaInforme = (utils.str_fecha(
                    time.strptime(self.inicio,"%Y/%m/%d")) + ' - '
                    + utils.str_fecha(time.strptime(self.fin,"%Y/%m/%d")))
        if datos != []:
            reports.abrir_pdf(
                    geninformes.producido_produccion(datos, 
                                                     fechaInforme, 
                                                     self.grafico))


def str_horas(fh):
    """
    Devuelve un TimeDelta en horas:minutos
    """
    try:
        return "%02d:%02d" % (fh.hour + fh.day * 24, fh.minute)
    except:
        return ''

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
                horas_delta = delta.hours
            if 0 < horas_delta < 8:
                # Si el hueco es de más de un turno, es que no ha habido 
                # producción en ese turno.
                tiempo_faltante = delta
                if pclases.DEBUG:
                    print(">>> %f --> Hueco detectado entre %s y %s" % (
                        horas_delta, last_parte.get_info(), pdp.get_info()))
    huecos.append(pdp)
    return tiempo_faltante, parte_anterior

if __name__ == '__main__':
    t = ConsultaProducido() 

