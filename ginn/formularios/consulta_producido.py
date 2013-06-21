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
pygtk.require('2.0')
    

class ConsultaProducido(Ventana):
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
        self.grafico = None
        self.kilos = 0
        self.metros = 0
        self.rollos = 0
        self.balas = 0
        Ventana.__init__(self, 'consulta_producido.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       "b_exportar/clicked": self.exportar}
        self.add_connections(connections)
        cols = (('Producto/Lote','gobject.TYPE_STRING', False, True, False, None),
                ('Cantidad producida','gobject.TYPE_STRING', False, True, False, None),
                ('Unidades', 'gobject.TYPE_INT64', False, True, False, None),
                ('Media por unidad', 'gobject.TYPE_STRING', False, True, False, None), 
                ('ID','gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        cols = (('Grupo', 'gobject.TYPE_STRING', False, True, True, None), 
                ('Producción', 'gobject.TYPE_STRING', False, True, False, None), 
                ('ID', 'gobject.TYPE_INT64', False, None, None, None))
        utils.preparar_listview(self.wids['tv_ford'], cols)
        temp = time.localtime()
        self.fin = str(temp[0])+'/'+str(temp[1])+'/'+str(temp[2])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.wids['e_fechainicio'].set_text(utils.str_fecha(mx.DateTime.localtime() - (7 * mx.DateTime.oneDay)))
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
        En la última columna del model (la oculta) se guarda un string "ID:X" donde X
        es R si es un rollo (geotextil) o B si es bala (fibra).
        """        
        model = self.wids['tv_datos'].get_model()
        model.clear()
        for item in items:
            itr = model.append(None, (item[0],
                                       item[1],
                                       item[4],
                                       utils.float2str(item[5]), 
                                       "%d:%s" % (item[2], item[3])))
            for lote_partida in item[6]:
                model.append(itr, (lote_partida and lote_partida.codigo or "?", 
                                    utils.float2str(item[6][lote_partida]['cantidad']), 
                                    item[6][lote_partida]['bultos'], 
                                    utils.float2str(item[6][lote_partida]['cantidad'] / item[6][lote_partida]['bultos']), 
                                    "%d:LP" % (lote_partida.id)
                                   ))
        
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
        linea = pclases.LineaDeProduccion.select(pclases.LineaDeProduccion.q.nombre.contains('geotextil'))
        if linea.count() == 0:
            linea_gtx = None
        else:
            linea_gtx = linea[0]
        linea = pclases.LineaDeProduccion.select(pclases.LineaDeProduccion.q.nombre.contains('fibra'))
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
            pdps = PDP.select(PDP.q.fecha <= self.fin, orderBy = 'fecha')
        else:
            pdps = PDP.select(pclases.AND(PDP.q.fecha >= self.inicio, 
                              PDP.q.fecha <= self.fin), orderBy='fecha')
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        tot = pdps.count()
        i = 0.0
        vpro.mostrar()
        prod_balas = {}
        prod_pales = {}
        prod_rollos = {}
        ford = {}
        for pdp in pdps:
            vpro.set_valor(i/tot, 'Analizando partes %s...' % (
                utils.str_fecha(pdp.fecha)))
            if (pdp.es_de_balas() 
                and not "reenvas" in pdp.observaciones.lower() 
                and (self.wids['rb_todas'].get_active() 
                     or self.wids['rb_fibra'].get_active())):
                self.agregar_parte_a_dicford(ford, pdp)
                # Añado ProductoVenta de las balas.
                for a in pdp.articulos:
                    key = "%d:B" % (a.productoVentaID)
                    if key not in prod_balas:
                        try:
                            prod_balas[key] = [a.productoVenta.descripcion, 
                                               a.bala.pesobala, 
                                               a.productoVenta.id, 
                                               'B', 
                                               'kg', 
                                               1, 
                                               {a.lote: {'cantidad': a.peso, 
                                                         'bultos': 1}}
                                              ]
                        except AttributeError:
                            prod_balas[key] = [a.productoVenta.descripcion, 
                                               a.bigbag.pesobigbag, 
                                               a.productoVenta.id, 
                                               'B', 
                                               'kg', 
                                               1, 
                                               {a.loteCem: {'cantidad': a.peso,
                                                            'bultos': 1}}
                                              ]
                    else:
                        try:
                            prod_balas[key][1] += a.bala.pesobala
                            try:
                                prod_balas[key][6][a.lote]['cantidad']+=a.peso
                                prod_balas[key][6][a.lote]['bultos'] += 1
                            except KeyError:
                                prod_balas[key][6][a.lote]={'cantidad':a.peso,
                                                            'bultos': 1}
                        except AttributeError:
                            prod_balas[key][1] += a.bigbag.pesobigbag
                            try:
                                prod_balas[key][6][a.loteCem]['cantidad'] += a.peso
                                prod_balas[key][6][a.loteCem]['bultos'] += 1 
                            except KeyError:
                                prod_balas[key][6][a.loteCem] = {'cantidad' : a.peso, 'bultos' : 1}
                                # De verdad que es absurdo llamar «key» a la 
                                # variable que hace de "key". No tiene nombre 
                                # descriptivo y ahora no sé lo qué es. ¿Una 
                                # bala? ¿Un producto? ¿Un parte? ¿Un consumo? 
                                # ¿Ves lo que pasa? ¿Ves lo que pasa cuando 
                                # intentas dar por culo a un desconocido? 
                        prod_balas[key][5] += 1
            elif (pdp.es_de_bolsas() 
                  and (self.wids['rb_todas'].get_active() 
                       or self.wids['rb_embolsado'].get_active())):
                self.agregar_parte_a_dicford(ford, pdp)
                # Añado ProductoVenta de los palés.
                for a in pdp.articulos:
                    key = "%d:P" % (a.productoVentaID)
                    if key not in prod_pales:
                        prod_pales[key] = [a.productoVenta.descripcion, 
                                           a.peso, 
                                           a.productoVenta.id, 
                                           'P', 
                                           'kg', 
                                           1, 
                                           {a.partidaCem: 
                                                {'cantidad': a.peso, 
                                                 'bultos': a.caja.numbolsas}}
                                          ]
                    else:
                        prod_pales[key][1] += a.peso
                        try:
                            prod_pales[key][6][a.partidaCem]['cantidad'] \
                                += a.peso
                            prod_pales[key][6][a.partidaCem]['bultos'] \
                                += a.caja.numbolsas
                        except KeyError:
                            prod_pales[key][6][a.partidaCem] = {
                                'cantidad':a.peso,
                                'bultos': a.caja.numbolsas}
                        prod_pales[key][5] += 1
            elif (pdp.es_de_rollos() and 
                  (self.wids['rb_todas'].get_active() 
                   or self.wids['rb_geotextiles'].get_active())):
                self.agregar_parte_a_dicford(ford, pdp)
                # Añado ProductoVenta de los rollos.
                for a in pdp.articulos:
                    key = "%d:R" % (a.productoVentaID)
                    try:
                        cantidad = a.superficie
                    except AttributeError, error:
                        self.logger.error("consulta_producido::buscar -> "
                                          "Falló el acceso a las propiedades "
                                          "de producto de venta del rollo: "
                                          "%s" % (error))
                    if key not in prod_rollos:
                        prod_rollos[key] = [a.productoVenta.descripcion, 
                                            cantidad, 
                                            a.productoVenta.id, 
                                            'R', 
                                            'm²', 
                                            1, 
                                            {a.partida:
                                                {'cantidad': a.superficie, 
                                                 'bultos': 1}}
                                           ]
                    else:
                        prod_rollos[key][1] += cantidad
                        prod_rollos[key][5] += 1
                        try:
                            prod_rollos[key][6][a.partida]['cantidad'] += a.superficie
                            prod_rollos[key][6][a.partida]['bultos'] += 1
                        except KeyError:
                            prod_rollos[key][6][a.partida] = {'cantidad' : a.superficie, 'bultos' : 1}
            i += 1
        # Gráfico usando PyChart:
        data = []
        self.resultado = []
        for k in prod_balas:
            cantidad = "%s %s" % (utils.float2str(prod_balas[k][1], 1), prod_balas[k][4])
            self.resultado.append([prod_balas[k][0],    # ?
                                   cantidad,            # Cantidad como cadena 
                                                        # de texto, con 
                                                        # unidades.
                                   prod_balas[k][2],    # ?
                                   prod_balas[k][3],    # ?
                                   prod_balas[k][5],    # ?
                                   prod_balas[k][1] / prod_balas[k][5], # Peso
                                                        # medio por bala/saca.
                                   prod_balas[k][6]
                                  ])
            data.append((prod_balas[k][0].replace("/", "//"), 
                         prod_balas[k][1], 
                         prod_balas[k][5]))
        for k in prod_pales:
            cantidad = "%s %s" % (utils.float2str(prod_pales[k][1], 1), 
                                  prod_pales[k][4])
            self.resultado.append([prod_pales[k][0],    # ?
                                   cantidad,            # Cantidad como cadena 
                                                        # de texto, con 
                                                        # unidades.
                                   prod_pales[k][2],    # ?
                                   prod_pales[k][3],    # ?
                                   prod_pales[k][5],    # ?
                                   prod_pales[k][1] / prod_pales[k][5], # Peso
                                                        # medio por caja.
                                   prod_pales[k][6]
                                  ])
            data.append((prod_pales[k][0].replace("/", "//"), 
                         prod_pales[k][1], 
                         prod_pales[k][5]))
        for k in prod_rollos:
            cantidad = "%s %s" % (utils.float2str(prod_rollos[k][1], 1), 
                                  prod_rollos[k][4])
            self.resultado.append([prod_rollos[k][0],   # ?
                                   cantidad,            # Cantidad como 
                                                        # cadena, con unidades 
                                   prod_rollos[k][2],   # ?
                                   prod_rollos[k][3],   # ?
                                   prod_rollos[k][5],   # ?
                                   prod_rollos[k][1]/prod_rollos[k][5], 
                                    # Metros cuadrados medio por rollo (no 
                                    # tiene mucho sentido, pero bueno)
                                   prod_rollos[k][6]    # Producción / partida
                                  ])
            data.append((prod_rollos[k][0].replace("/", "//"), 
                         prod_rollos[k][1], 
                         prod_rollos[k][5]))
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
        self.dibujar_grafico(data)
        vpro.ocultar()
        self.rellenar_tabla(self.resultado)
        self.rellenar_tabla_fordiana(ford)

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
            except ZeroDivisionError:
                # Valor de horas nulo. No cuenta para el informe.
                producido_proporcional = 0.0
                self.to_log("[agregar_parte_a_dicford] Parte con duración 0.", 
                        {"parte de producción": parte, 
                         "producción": produccion, 
                         "total_horas": total_horas, 
                         "grupos": grupos})
            if grupo not in ford:
                ford[grupo] = {}
            if produccion[1] not in ford[grupo]:
                ford[grupo][produccion[1]] = producido_proporcional
            else:
                ford[grupo][produccion[1]] += producido_proporcional

    def preparar_diccionario_ford(self, fechaini, fechafin):
        """
        Prepara un diccionario cuyas claves son una tupla (fechahorainicio, fechahorafin).
        Si fechaini es None, fechahorainicio será la fecha más antigua de los partes 
        de la BD a las 6:00.
        Todas las tuplas irán en intervalo de 06:00 a 14:00, 14:00 a 22:00 y 22:00 a 06:00.
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
                produccion.append("%s %s" % (utils.float2str(ford[grupo][unidad], 3, autodec = True), unidad))
            nombregrupo = grupo and grupo.nombre or "Sin grupo"
            model.append((nombregrupo, "; ".join(produccion), 0))

    def calcular_totales(self, prod):
        """
        Calcula el total en cantidad y bultos del 
        diccionario de producción recibido.
        """
        cantidad = sum([prod[p][1] for p in prod])
        bultos = sum([prod[p][5] for p in prod])
        return (cantidad, bultos)

    def dibujar_grafico(self, data):
        """
        Dibuja el gráfico de tarta. Si se mezclan balas y rollos, usa unidades (balas o rollos). 
        Si es solo de geotextiles o de fibra, se usan sus unidades (metros o kilos).
        """
        if pychart_available and len(data) > 0:
            theme.use_color = True
            theme.reinitialize()
            tempdir = gettempdir()
            formato = "png"   # NECESITA ghostscript
            nomarchivo = "%s.%s" % (mx.DateTime.localtime().strftime("gcproducido_%Y_%m_%d_%H_%M_%S"), formato)
            nombregraph = os.path.join(tempdir, "%s") % (nomarchivo)
            can = canvas.init(fname = nombregraph, format = formato)
            ar = area.T(size=(400, 200), legend=legend.T(), x_grid_style = None, y_grid_style = None)
            if self.wids['rb_todas'].get_active():
                data = [(d[0], d[2]) for d in data]
                can.show(15, 150, "/a90/12/hRNúmero de balas\ny rollos fabricados")
            else:
                data = [(d[0], d[1]) for d in data]
                if self.wids['rb_fibra'].get_active():
                    can.show(15, 150, "/a90/12/hRKilos de\nfibra fabricados")
                elif self.wids['rb_geotextiles'].get_active():
                    can.show(15, 150, "/a90/12/hRMetros cuadrados de\ngeotextiles fabricados")
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
                                   texto = "Para ver gráficas en pantalla necesita instalar Ghostscript.\nPuede encontrarlo en el servidor de la aplicación o descargarlo de la web (http://www.cs.wisc.edu/~ghost/).",
                                   padre = self.wids['ventana'])
            self.grafico = nombregraph
        else:
            self.wids['im_graph'].set_from_file("NOEXISTEPORTANTOVAADIBUJARUNASPA")
            self.grafico = None



    def imprimir(self,boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        from formularios import reports
        datos = []
        model = self.wids['tv_datos'].get_model()
        for i in model:
            datos.append((i[0],
                          i[1],
                          i[2]))
        if self.balas != 0:
            datos.append(("", "", ""))
            datos.append(("", "-" * 30 , "-" * 30))
            datos.append(("", "", ""))
            datos.append((" " * 50 + "TOTAL:", "%s m²" % (utils.float2str(self.kilos)), self.balas))
        if self.rollos != 0:
            datos.append(("", "", ""))
            datos.append(("", "-" * 30 , "-" * 30))
            datos.append(("", "", ""))
            datos.append((" " * 50 + "TOTAL:", "%s m²" % (utils.float2str(self.metros)), self.rollos))
        if (self.inicio) == None:            
            fechaInforme = 'Hasta '+utils.str_fecha(time.strptime(self.fin,"%Y/%m/%d"))
        else:
            fechaInforme = utils.str_fecha(time.strptime(self.inicio,"%Y/%m/%d"))+' - '+utils.str_fecha(time.strptime(self.fin,"%Y/%m/%d"))
        if datos != []:
            reports.abrir_pdf(geninformes.producido_produccion(datos, fechaInforme, self.grafico))


if __name__ == '__main__':
    t = ConsultaProducido() 

    
