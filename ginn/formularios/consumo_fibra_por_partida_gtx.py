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
## consumo_fibra_por_partida_gtx.py
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 6 de noviembre de 2006 -> Inicio
## 
###################################################################
## NOTA: Es posible que incluya partidas gtx. de un día anterior o 
## posterior al inicio o fin de rango, ya que lo que busca son 
## partidas de carga y después muestra todas las partidas de 
## geotextiles fabricadas. No mostrar una partida de gtx. fabricada
## con una partida de carga por no entrar en el rango de fechas 
## implicaría que en la suma final de "consumido" aparecería una 
## diferencia grande respecto a "producido" (que lógicamente, es 
## la cantidad de esa partida no incluida). Ver en código el 
## criterio final adoptado: entran en fecha aquellas partidas de 
## carga completamente consumidas antes de la fecha final.
###################################################################
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sqlobject
try:
    from framework import pclases
except ImportError:
    import sys
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    from framework import pclases
import mx.DateTime
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes
import ventana_progreso


class ConsumoFibraPorPartidaGtx(Ventana):
    inicio = None
    fin = None
        
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self.partidas_carga = {}
        global fin
        Ventana.__init__(self, 'consumo_fibra_por_partida_gtx.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       'b_exportar/clicked': self.exportar}
        self.add_connections(connections)
        cols = (('Partida', 'gobject.TYPE_STRING', False, True, False, None),
         ('kg consumidos', 'gobject.TYPE_STRING', False, False, False, None), 
         ('kg prod. (real)', 'gobject.TYPE_STRING', False, False, False, None),
         ('kg prod. (teórico)', 'gobject.TYPE_STRING', False,False,False,None),
         ('balas cons.', 'gobject.TYPE_STRING', False, False, False, None), 
         ('rollos prod.', 'gobject.TYPE_STRING', False, False, False, None), 
         ('m² producidos', 'gobject.TYPE_STRING', False, False, False, None), 
         ('ID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        for col in self.wids['tv_datos'].get_columns()[1:]:
            for cell in col.get_cell_renderers():
                cell.set_property("xalign", 1.0)
            col.set_alignment(1.0)
        self.colorear(self.wids['tv_datos'])
        temp = time.localtime()
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.wids['e_fechainicio'].set_text(utils.str_fecha(mx.DateTime.localtime() - (7 * mx.DateTime.oneDay)))
        self.inicio = utils.parse_fecha(self.wids['e_fechainicio'].get_text())
        self.fin = utils.parse_fecha(self.wids['e_fechafin'].get_text())
        self.wids['rb_pesoreal'].child.set_property("use-markup", True)
        self.wids['rb_teorico'].child.set_property("use-markup", True)
        self.wids['rb_pesosin'].child.set_property("use-markup", True)
        self.wids['rb_pesosin'].set_active(True)
        gtk.main()
    
    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        import sys, os
        sys.path.append(os.path.join("..", "informes"))
        from treeview2csv import treeview2csv
        from informes import abrir_csv
        tv = self.wids['tv_datos']
        abrir_csv(treeview2csv(tv))

    def colorear(self, tv):
        """
        Asocia una función al treeview para resaltar los partes pendientes 
        de verificar.
        """
        def cell_func(column, cell, model, itr, numcol):
            """
            Si la fila corresponde a un parte de producción no verificado, 
            lo colorea en rojo oscuro, si no, lo hace en verde oscuro.
            """
            consumido = model[itr][1]
            producido = model[itr][2]
            try:
                consumido = utils._float(consumido)
                producido = utils._float(producido)
                if consumido < producido:
                    if numcol == 1:
                        color = "red"
                    elif numcol == 2:
                        color = "blue"
                else:
                    if numcol == 1:
                        color = "blue"
                    else:
                        color = "red"
            except:
                color = None
            if consumido == 0 or producido == 0:
                color = None
                cell.set_property("cell-background", "red")
            else:
                cell.set_property("cell-background", None)
            cell.set_property("foreground", color)

        cols = tv.get_columns()
        for i in (1, 2):
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell, cell_func, i)

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, partidas_carga):
    	"""
        Rellena el model con los items de la consulta.
        partidas_carga es un diccionario... (mirar 
        abajo, en "buscar").
        """        
    	model = self.wids['tv_datos'].get_model()
    	model.clear()
        datachart = []
        for pc in partidas_carga:
            abuelo = model.append(None, 
                      (pc.codigo, 
                       utils.float2str(partidas_carga[pc]['kilos_consumidos']), 
                       utils.float2str(partidas_carga[pc]['kilos_producidos']), 
                       utils.float2str(partidas_carga[pc]['kilos_teoricos']), 
                       str(partidas_carga[pc]['balas']), 
                       str(partidas_carga[pc]['rollos']), 
                       utils.float2str(partidas_carga[pc]['metros']), 
                       pc.id))
            datachart.append([pc.codigo, 
                              partidas_carga[pc]['kilos_consumidos']])
            padre = model.append(abuelo, 
                                 ("Partidas de geotextiles producidas", 
                                  '', 
                                  '', 
                                  '', 
                                  '', 
                                  '', 
                                  '', 
                                  ''))
            for pgtx in partidas_carga[pc]['partidas']:
                model.append(padre, 
                             ("%s: %s" % (pgtx['código'], pgtx['producto']), 
                              "", 
                              utils.float2str(pgtx['kilos']), 
                              utils.float2str(pgtx['kilos_teoricos']), 
                              "", 
                              str(pgtx['rollos']), 
                              utils.float2str(pgtx['metros']),
                              ''))
            padre = model.append(abuelo, 
                                 ("Lotes de fibra consumidos", 
                                  '', 
                                  '', 
                                  '', 
                                  '', 
                                  '', 
                                  '', 
                                  ''))
            for lote in partidas_carga[pc]['lotes']:
                model.append(padre, 
                             ("%s: %s" % (lote['código'], lote['producto']), 
                              utils.float2str(lote['kilos']), 
                              '', 
                              '',  
                              str(lote['balas']), 
                              '', 
                              '', 
                              '',  
                              ))
        # Y ahora la gráfica.
        try:
            import gtk, gobject, cairo, copy, math
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
                chart = charting.Chart()
                self.wids['eventbox_chart'].add(chart)
            datachart.sort(lambda fila1, fila2: (fila1[0] < fila2[0] and -1) or (fila1[0] > fila2[0] and 1) or 0)
            for data in datachart:
                data.append(6)  # Barras de color rojo.
            chart.plot(datachart)
            self.wids['eventbox_chart'].show_all()
        except Exception, msg:
            txt = "consumo_fibra_por_partida_gtx.py::rellenar_tabla -> "\
                  "Error al dibujar gráfica (charting): %s" % msg
            print txt
            self.logger.error(txt)
        
    def set_inicio(self, boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
        self.inicio = utils.parse_fecha(self.wids['e_fechainicio'].get_text()) 

    def set_fin(self, boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.fin = utils.parse_fecha(self.wids['e_fechafin'].get_text()) 

    def por_fecha(self, e1, e2):
        """
        Permite ordenar una lista de albaranes por fecha
        """
        if e1.fecha < e2.fecha:
            return -1
        elif e1.fecha > e2.fecha:
            return 1
        else:
            return 0
        
    def buscar(self, boton):
        """
        Dadas fecha de inicio y de fin, busca los partes de 
        producción de geotextiles entre esas fechas.
        Para cada parte de producción extrae las partidas de 
        geotextiles fabricadas y las agrupa por partida de 
        carga.
        Finalmente, de cada partida de carga cuenta los kilogramos 
        de fibra y número de balas en ella. También divide las balas
        por lotes y cuenta los kg y bultos de cada lote que ha entrado
        en cada carga de cuarto.
        OJO: El criterio finalmente queda: en cada mes se cuenta el 
        consumo y la producción de las partidas cuyas partidas de carga 
        hayan sido terminadas. Una partida que comienza en un fin de 
        mes (por ejemplo) y acaba en el mes siguiente (cualquier fecha, en 
        general) cuenta para el mes siguiente. Esto es así porque hay que 
        tomar las partidas de carga como una unidad, como un todo, si se 
        quiere discernir bien los kg producidos y consumidos, ya que no hay 
        relación directa entre rollo y bala consumida (se pierde definición 
        al haber una tabla de una relación muchos a muchos entre medio).
        """
        PDP = pclases.ParteDeProduccion
        if not self.inicio:
            pdps = PDP.select(""" fecha <= '%s' AND observaciones NOT LIKE '%%;%%;%%;%%;%%;%%' """ % (self.fin.strftime('%Y-%m-%d')))
        else:
            pdps = PDP.select(""" fecha >= '%s' AND fecha <= '%s' AND observaciones NOT LIKE '%%;%%;%%;%%;%%;%%' """ % (self.inicio.strftime('%Y-%m-%d'), self.fin.strftime('%Y-%m-%d')))
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        tot = pdps.count()
        pdps = pdps.orderBy("fecha")
        i = 0.0
        vpro.mostrar()
        partidas_carga = {}
        # "Constantes" (nótense las comillas).
        PESOREAL = 1
        PESOTEORICO = 2
        PESOSIN = 3
        if self.wids['rb_pesoreal'].get_active():
            metodo = PESOREAL
        elif self.wids['rb_teorico'].get_active():
            metodo = PESOTEORICO
        elif self.wids['rb_pesosin'].get_active():
            metodo = PESOSIN
        else:
            txt = "consumo_fibra_por_partida_gtx.py::buscar -> ¡NO HAY SELEC"\
                  "CIONADO NINGÚN RADIOBUTTON DEL GRUPO!"
            self.logger.error(txt)
            print txt
            return
        for pdp in pdps:
            vpro.set_valor(i/tot, 'Analizando producción %s...' % (
                utils.str_fecha(pdp.fecha)))
            if pdp.articulos:
                articulo = pdp.articulos[0]
                if articulo.es_rollo():
                    partida = articulo.rollo.partida
                elif articulo.es_rollo_defectuoso():
                    partida = articulo.rolloDefectuoso.partida
                else:
                    partida = None
                if partida!=None and partida.entra_en_cota_superior(self.fin):
                    partida_carga = partida.partidaCarga
                    if partida_carga == None:   # Partidas sin partida de carga
                                                # ... eso es malo.
                        txt = "consumo_fibra_por_partida_gtx.py::buscar -> ¡P"\
                              "artida %s no tiene partida de carga!" % (
                                partida.get_info())
                        print txt
                        self.logger.error("%s%s" % (
                            self.usuario and self.usuario.usuario + ": " 
                            or "", txt))
                    else:
                        if partida_carga not in partidas_carga: # Aquí ya se 
                        # asegura que no se contará dos veces la misma 
                        # bala -partida de carga-.
                            partidas_carga[partida_carga] = {
                                'partidas': [], 
                                'lotes': [], 
                                'kilos_consumidos': 0.0, 
                                'balas': 0, 
                                'kilos_producidos': 0.0, 
                                'kilos_teoricos': 0.0, 
                                'rollos': 0, 
                                'metros': 0.0, }
                            for partida in partida_carga.partidas:
                                if metodo == PESOSIN:
                                    kilos_producidos = partida.get_kilos()
                                elif metodo == PESOTEORICO:
                                    kilos_producidos \
                                        = partida.get_kilos_teorico()
                                elif metodo == PESOREAL:
                                    kilos_producidos \
                                        = partida.get_kilos_totales()
                                else:
                                    txt = "consumo_fibra_por_partida_gtx.py "\
                                          "-> No se pudo determinar el métod"\
                                          "o de cálculo. Se usará el peso te"\
                                          "órico."
                                    self.logger.warning(txt)
                                    print txt
                                    kilos_producidos \
                                        = partida.get_kilos_teorico()
                                kilos_teoricos = partida.get_kilos_teorico()
                                metros_producidos = partida.get_metros()
                                producto = partida.get_producto()
                                partidas_carga[partida_carga]\
                                  ['partidas'].append(
                                    {'código': partida.codigo, 
                                     'kilos': kilos_producidos, 
                                     'kilos_teoricos': kilos_teoricos, 
                                     'metros': metros_producidos, 
                                     'rollos': len(partida.rollos), 
                                     'producto': producto 
                                                    and producto.descripcion 
                                                    or "SIN PRODUCCIÓN"
                                     })
                                partidas_carga[partida_carga]\
                                    ['kilos_producidos'] += kilos_producidos
                                partidas_carga[partida_carga]\
                                    ['kilos_teoricos'] += kilos_teoricos
                                partidas_carga[partida_carga]\
                                    ['rollos'] += len(partida.rollos)
                                partidas_carga[partida_carga]\
                                    ['metros'] += metros_producidos
                            lotes = partida_carga.get_lotes()
                            for lote in lotes:
                                balas = pclases.Bala.select(pclases.AND(
                                    pclases.Bala.q.loteID == lote.id, 
                                    pclases.Bala.q.partidaCargaID 
                                        == partida_carga.id))
                                kilos_consumidos = sum(
                                    [b.pesobala for b in balas])
                                partidas_carga[partida_carga]['lotes'].append(
                                 {'código': lote.codigo, 
                                  'kilos': kilos_consumidos, 
                                  'balas': balas.count(), 
                                  'producto': 
                                   balas[0].articulo.productoVenta.descripcion
                                  })
                                   # NOTA: el get_lotes() ya asegura que al 
                                   # menos hay una bala en la consulta "balas".
                                partidas_carga[partida_carga]\
                                    ['kilos_consumidos'] += kilos_consumidos
                                partidas_carga[partida_carga]\
                                    ['balas'] += balas.count()
            i += 1
        vpro.ocultar()
        self.partidas_carga = partidas_carga
        self.rellenar_tabla(partidas_carga)

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        if self.partidas_carga  != {}:
            if self.wids['rb_pesoreal'].get_active():
                metodo = "reales tomados en la línea (incluyendo embalajes)." 
            elif self.wids['rb_teorico'].get_active():
                metodo = "teóricos."
            elif self.wids['rb_pesosin'].get_active():
                metodo = "reales tomados en la línea (sin embalajes)."
            else:
                txt = "consumo_fibra_por_partida_gtx.py::imprimir -> ¡NO HAY SELECCIONADO NINGÚN RADIOBUTTON DEL GRUPO!"
                self.logger.error(txt)
                print txt
                return
            partidas_carga = self.partidas_carga
            from ginn.formularios import reports as informes
            datos = []
            total_kilos_consumidos = 0.0
            total_kilos_producidos = 0.0
            total_kilos_teoricos = 0.0
            total_balas_consumidas = 0
            total_rollos_producidos = 0
            total_metros_producidos = 0.0
            def cmp_codigo(pc1, pc2):
                if pc1.codigo < pc2.codigo:
                    return -1
                if pc1.codigo > pc2.codigo:
                    return 1
                return 0
            claves = partidas_carga.keys()
            claves.sort(cmp_codigo)
            for pc in claves:
                datos.append((pc.codigo, 
                              utils.float2str(partidas_carga[pc]['kilos_consumidos']), 
                              utils.float2str(partidas_carga[pc]['kilos_producidos']), 
                              utils.float2str(partidas_carga[pc]['kilos_teoricos']), 
                              str(partidas_carga[pc]['balas']), 
                              str(partidas_carga[pc]['rollos']), 
                              utils.float2str(partidas_carga[pc]['metros']), 
                             ))
                total_kilos_producidos += partidas_carga[pc]['kilos_producidos']
                total_kilos_teoricos += partidas_carga[pc]['kilos_teoricos']
                total_kilos_consumidos += partidas_carga[pc]['kilos_consumidos']
                total_metros_producidos += partidas_carga[pc]['metros']
                total_balas_consumidas += partidas_carga[pc]['balas']
                total_rollos_producidos += partidas_carga[pc]['rollos']
                padre = datos.append(("     >>> Lotes de fibra consumidos", '', '', '', '', '', ''))
                for lote in partidas_carga[pc]['lotes']:
                    datos.append(("               %s: %s" % (lote['código'], lote['producto']), 
                                  utils.float2str(lote['kilos']), 
                                  '',  
                                  '',  
                                  str(lote['balas']), 
                                  '', 
                                  '', 
                                 ))
                padre = datos.append(("     >>> Partidas de geotextiles producidas:", '', '', '', '', '', ''))
                for pgtx in partidas_carga[pc]['partidas']:
                    datos.append(("               %s: %s" % (pgtx['código'], pgtx['producto']), 
                                  "", 
                                  utils.float2str(pgtx['kilos']), 
                                  utils.float2str(pgtx['kilos_teoricos']), 
                                  "", 
                                  str(pgtx['rollos']), 
                                  utils.float2str(pgtx['metros']),
                                 ))
                datos.append(("---", ) * 7)
            datos.append(("", ) * 7)
            datos.append(("===", ) * 7)
            datos.append(("     TOTALES: ", 
                          utils.float2str(total_kilos_consumidos), 
                          utils.float2str(total_kilos_producidos), 
                          utils.float2str(total_kilos_teoricos), 
                          str(total_balas_consumidas), 
                          str(total_rollos_producidos), 
                          utils.float2str(total_metros_producidos)
                         ))
            datos.append(("", "", "", "", "", "", ""))
            datos.append(("", "", "", "", "", "", ""))

            if (self.inicio) == None: 
                fechaInforme = 'Hasta '+utils.str_fecha(self.fin)
            else:
                fechaInforme = "%s - %s" % (utils.str_fecha(self.inicio), utils.str_fecha(self.fin))
            if datos != []:
                informes.abrir_pdf(geninformes.consumo_fibra_produccion_gtx(datos, fechaInforme))


if __name__ == '__main__':
    t = ConsumoFibraPorPartidaGtx() 

    
