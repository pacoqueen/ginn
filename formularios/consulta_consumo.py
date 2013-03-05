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
## consulta_consumo.py -- 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sqlobject
try:
    import pclases
except ImportError:
    import sys
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    import pclases
import mx
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes
import ventana_progreso
    

class ConsultaConsumo(Ventana):
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
        Ventana.__init__(self, 'consulta_consumo.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       "b_exportar/clicked": self.exportar}
        self.add_connections(connections)
        cols = (('Producto', 'gobject.TYPE_STRING', False, True, False, None),
                ('Cantidad consumida', 'gobject.TYPE_STRING', False, True, False, None),
                ('Media diaria', 'gobject.TYPE_STRING', False, True, False, None), 
                ('ID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_datos'], cols)
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
        import sys, os
        sys.path.append(os.path.join("..", "informes"))
        from treeview2csv import treeview2csv
        from informes import abrir_csv
        tv = self.wids['tv_datos']
        abrir_csv(treeview2csv(tv))

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, items):
    	"""
        Rellena el model con los items de la consulta.
        "items" es una lista de 5 elementos: Nombre producto, cantidad, ID, X y media diaria.
        En la última columna del model (la oculta) se guarda un string "ID:X" donde X
        es C si es un producto de compra o V si es de venta (fibra fabricada usada
        como materia prima).
        """        
    	model = self.wids['tv_datos'].get_model()
    	model.clear()
    	for item in items:
            iter = model.append(None, (item[0],
                                       item[1],
                                       item[4], 
                                       "%d:%s" % (item[2], item[3])))
        # : Es un TreeView, ya añadiré si se necesita información adicional en los hijos. Usaré
        #   el evento "row-expanded" para no retrasar más la carga inicial de datos de cada consulta.
        #   (Ver trazabilidad.py como ejemplo.)
        
    def set_inicio(self, boton):
        temp = utils.mostrar_calendario(fecha_defecto = utils.parse_fecha(self.wids['e_fechainicio'].get_text()), 
                                        padre = self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
        self.inicio = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])


    def set_fin(self, boton):
        temp = utils.mostrar_calendario(fecha_defecto = utils.parse_fecha(self.wids["e_fechafin"].get_text()), 
                                        padre = self.wids['ventana'])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.fin = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])


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
        
    def buscar(self, boton):
        """
        Dadas fecha de inicio y de fin, busca los productos y 
        materia prima consumida en los partes de producción.
        """
        PDP = pclases.ParteDeProduccion
        if not self.inicio:
            pdps = PDP.select(PDP.q.fecha <= self.fin, orderBy = 'fecha')
        else:
            pdps = PDP.select(sqlobject.AND(PDP.q.fecha >= self.inicio, PDP.q.fecha <= self.fin), orderBy='fecha')
        fechainicio = mx.DateTime.DateTimeFrom(day = int(self.inicio.split("/")[2]), 
                                               month = int(self.inicio.split("/")[1]), 
                                               year = int(self.inicio.split("/")[0])) 
        fechafin = mx.DateTime.DateTimeFrom(day = int(self.fin.split("/")[2]), 
                                               month = int(self.fin.split("/")[1]), 
                                               year = int(self.fin.split("/")[0])) 
        dias = ((fechafin - fechainicio) + mx.DateTime.oneDay).days
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        tot = pdps.count()
        i = 0.0
        vpro.mostrar()
        linea_gtx, linea_fib = self.get_lineas_produccion()
        cons_balas = {}
        cons_rollos = {}
        partidas_contadas = []
        balas_contadas = []
        for pdp in pdps:
            vpro.set_valor(i/tot, 'Analizando partes %s...' % (utils.str_fecha(pdp.fecha)))
            if pdp.es_de_balas() and \
               (self.wids['rb_todas'].get_active() or self.wids['rb_fibra'].get_active()):
                # Añado consumos de material adicional y materia prima (ambos son ProductoCompra).
                for c in pdp.consumos:
                    key = "%d:C" % (c.productoCompraID)
                    if key not in cons_balas:
                        cons_balas[key] = [c.productoCompra.descripcion, c.cantidad, c.productoCompra.id, 'C', c.productoCompra.unidad]
                    else:
                        cons_balas[key][1] += c.cantidad
            elif pdp.es_de_rollos() and \
                 (self.wids['rb_todas'].get_active() or self.wids['rb_geotextiles'].get_active()):
                # Añado consumos de material adicional (ProductoCompra).
                for c in pdp.consumos:
                    key = "%d:C" % (c.productoCompraID)
                    if key not in cons_rollos:
                        cons_rollos[key] = [c.productoCompra.descripcion, c.cantidad, c.productoCompra.id, 'C', c.productoCompra.unidad]
                    else:
                        cons_rollos[key][1] += c.cantidad
                # Y el consumo de materia prima (ProductoVenta). Se hace por PARTIDAS, ya que 
                # los partes comparten materia prima de fibra si son de la misma partida.
                if pdp.articulos != []:
                    if pdp.articulos[0].es_rollo():
                        partida = pdp.articulos[0].rollo.partida
                    elif pdp.articulos[0].es_rollo_defectuoso():
                        partida = pdp.articulos[0].rolloDefectuoso.partida
                    else:
                        partida = None
                    # Hay que evitar contar la misma partida dos veces.
                    if partida != None and partida not in partidas_contadas and partida.entra_en_cota_superior(fechafin):
                        partidas_contadas.append(partida)
                        for bala in partida.balas:
                            if bala not in balas_contadas:  # Dos partidas pueden compartir partida de carga y por tanto 
                                                            # balas. Evito contar la misma dos veces.
                                balas_contadas.append(bala)
                                productoVenta = bala.articulos[0].productoVenta
                                key = "%d:V" % (productoVenta.id)
                                if key not in cons_rollos:
                                    cons_rollos[key] = [productoVenta.descripcion, bala.pesobala, productoVenta.id, 'V', 'kg']
                                else:
                                    cons_rollos[key][1] += bala.pesobala
            i += 1
        self.resultado = []
        for k in cons_balas:
            cantidad = "%s %s" % (utils.float2str(cons_balas[k][1], 3), cons_balas[k][4])
            media = "%s %s/día" % (utils.float2str(cons_balas[k][1] / dias), cons_balas[k][4])
            self.resultado.append([cons_balas[k][0], cantidad, cons_balas[k][2], cons_balas[k][3], media])
        for k in cons_rollos:
            cantidad = "%s %s" % (utils.float2str(cons_rollos[k][1], 3), cons_rollos[k][4])
            media = "%s %s/día" % (utils.float2str(cons_rollos[k][1] / dias), cons_rollos[k][4])
            self.resultado.append([cons_rollos[k][0], cantidad, cons_rollos[k][2], cons_rollos[k][3], media])
        vpro.ocultar()
        self.rellenar_tabla(self.resultado)


    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        import informes
        datos = []
        model = self.wids['tv_datos'].get_model()
        for i in xrange(len(model)):
            datos.append((model[i][0], model[i][1]))
        if (self.inicio) == None:            
            fechaInforme = 'Hasta '+utils.str_fecha(time.strptime(self.fin, "%Y/%m/%d"))
        else:
            fechaInforme = utils.str_fecha(time.strptime(self.inicio, "%Y/%m/%d"))+' - '+utils.str_fecha(time.strptime(self.fin, "%Y/%m/%d"))
        if datos != []:
            informes.abrir_pdf(geninformes.consumo_produccion(datos, fechaInforme))


if __name__ == '__main__':
    t = ConsultaConsumo() 

    
