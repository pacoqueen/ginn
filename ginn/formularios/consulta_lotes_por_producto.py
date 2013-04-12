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
## consulta_lotes_por_producto.py 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 4 de abril de 2006 -> Inicio
##
###################################################################
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, time
from framework import pclases
import mx.DateTime
from informes import geninformes
from ventana_progreso import VentanaProgreso, VentanaActividad  # @UnusedImport
    

class ConsultaLotesPorProducto(Ventana):
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
        Ventana.__init__(self, 'consulta_lotes_por_producto.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       "b_exportar/clicked": self.exportar}
        self.add_connections(connections)
        cols = (('Num. Lote','gobject.TYPE_INT64',False,True,False,None),
                ('Código','gobject.TYPE_STRING',False,True,False,None),
                ('Tenacidad','gobject.TYPE_STRING',False,True,False,None),
                ('Elongación','gobject.TYPE_STRING',False,True,False,None),
                ('Rizo','gobject.TYPE_STRING',False,True,False,None),
                ('Encogimiento','gobject.TYPE_STRING',False,True,False,None),
                ('Grasa','gobject.TYPE_STRING',False,True,False,None),
                ('Idlote','gobject.TYPE_INT64',False,False,False,None))
        utils.preparar_listview(self.wids['tv_datos'], cols)
        self.wids['tv_datos'].connect("row-activated", self.abrir_parte_tv)
        utils.rellenar_lista(self.wids['cmbe_producto'], [(p.id, p.nombre) for p in pclases.ProductoVenta.select(pclases.ProductoVenta.q.camposEspecificosBalaID != None, orderBy = 'nombre')])
        temp = time.localtime()
        self.fin = mx.DateTime.localtime()
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
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
    
    
    def rellenar_tabla(self,lista = []):
        """
        Rellena el model con los resultados de la búsqueda almacenados
        en una lista de lotes.
        """        
        model = self.wids['tv_datos'].get_model()
        self.wids['tv_datos'].freeze_child_notify()
        self.wids['tv_datos'].set_model(None)
        model.clear()
        for elem in lista:
            model.append((elem.numlote,
                    elem.codigo,
                    str(elem.tenacidad),
                    str(elem.elongacion),
                    str(elem.rizo),
                    str(elem.encogimiento),
                    "%.2f" % elem.grasa,
                    elem.id))
        self.wids['tv_datos'].set_model(model)
        self.wids['tv_datos'].thaw_child_notify()
        
    def set_inicio(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
        self.inicio = mx.DateTime.DateTimeFrom(day = temp[0], month = temp[1], year = temp[2])


    def set_fin(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.fin = mx.DateTime.DateTimeFrom(day = temp[0], month = temp[1], year = temp[2])


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

    def get_unambiguous_fecha(self, fecha):
        try:
            res = fecha.strftime('%B %d, %Y')
        except AttributeError:  # Fecha es None
            return ""
        trans = {'January': 'enero',
                 'February': 'febrero',
                 'March': 'marzo',
                 'April': 'abril',
                 'May': 'mayo',
                 'June': 'junio',
                 'July': 'julio',
                 'August': 'agosto',
                 'September': 'septiembre',
                 'October': 'octubre',
                 'November': 'noviembre',
                 'December': 'diciembre'}
        for in_english in trans:
            res = res.replace(trans[in_english], in_english)
        return res
        
    def buscar(self,boton):
        """
        """
        idproducto = utils.combo_get_value(self.wids['cmbe_producto'])
        if idproducto == None:
            utils.dialogo_info(titulo = 'ERROR', texto = 'Seleccione un producto', padre = self.wids['ventana'])
            return
        producto = pclases.ProductoVenta.get(idproducto)
        and_fecha_inicio = "AND parte_de_produccion.fecha >= '%s'" % (self.get_unambiguous_fecha(self.inicio))
        if producto.es_rollo():     # No debería ocurrir. Lo mantengo porque es copy-paste de la consulta de partidas.
            parte_where_de_consulta = """
    partida.id IN 
        (SELECT rollo.partida_id 
         FROM rollo 
         WHERE rollo.id IN 
            (SELECT articulo.rollo_id 
             FROM articulo 
             WHERE articulo.producto_venta_id = %d AND articulo.parte_de_produccion_id IN 
                (SELECT parte_de_produccion.id 
                 FROM parte_de_produccion 
                 WHERE parte_de_produccion.fecha <= '%s' %s
                 ORDER BY parte_de_produccion.fecha
                )
            )
        ) """ %(producto.id, 
                self.get_unambiguous_fecha(self.fin), 
                self.inicio and and_fecha_inicio or "")
        else:
            parte_where_de_consulta = """
    lote.id IN 
        (SELECT bala.lote_id 
         FROM bala 
         WHERE bala.id IN 
            (SELECT articulo.bala_id 
             FROM articulo 
             WHERE articulo.producto_venta_id = %d AND articulo.parte_de_produccion_id IN 
                (SELECT parte_de_produccion.id 
                 FROM parte_de_produccion 
                 WHERE parte_de_produccion.fecha <= '%s' %s
                 ORDER BY parte_de_produccion.fecha
                )
            )
        ) """ %(producto.id, 
                self.get_unambiguous_fecha(self.fin), 
                self.inicio and and_fecha_inicio or "")
        lotes = pclases.Lote.select(parte_where_de_consulta, distinct = True)
        # Hasta aquí la consulta optimizada para obtener los lotes. Pasamos a recuperar los datos en sí:
        vpro = VentanaActividad(padre = self.wids['ventana'])
        vpro.mostrar()
        self.resultado = []
        for p in lotes:
            vpro.mover()
            self.resultado.append(p)
        vpro.ocultar()
        self.resultado = lotes
        self.rellenar_tabla(self.resultado)


        #if not self.inicio:
        #    partes = pclases.ParteDeProduccion.select(pclases.ParteDeProduccion.q.fecha <= self.fin, orderBy = 'fecha')
        #else:
        #    partes = pclases.ParteDeProduccion.select(sqlobject.AND(pclases.ParteDeProduccion.q.fecha >= self.inicio,
        #                                                            pclases.ParteDeProduccion.q.fecha <= self.fin), orderBy = 'fecha')
        ## Me quedo con los partes con articulos relacionados, que sean del tipo de bala que buscamos
        #vpro = VentanaProgreso()
        #vpro.mostrar()
        #i = 0.0
        #tot = partes.count()
        #lotes = []
        ## : Esto es muy lento. Optimizar. Cuando digo muy lento quiero decir... ¡SOPORÍFERAMENTE INUSABLE!
        ##       [...] Unos 15 minutos después, va por el 75% de carga más o menos. Y no hay ni un año completo
        ##       de producción metida en la BD.
        #for p in partes:
        #    if (p.articulos != [] and 
        #            p.articulos[0].bala != None and 
        #            p.articulos[0].productoVentaID == idproducto and 
        #            p.articulos[0].bala.lote not in lotes):
        #        lotes.append(p.articulos[0].bala.lote)
        #    vpro.set_valor(i/tot, 'Buscando lotes...')
        #    i += 1
        #vpro.ocultar()
        #self.resultado = lotes        
        #self.rellenar_tabla(self.resultado)


    def imprimir(self,boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        from formularios import reports
        datos = []
        lista = self.resultado
        for elem in lista:
            datos.append((elem.numlote,
                    elem.codigo,
                    str(elem.tenacidad),
                    str(elem.elongacion),
                    str(elem.rizo),
                    str(elem.encogimiento),
                    "%.2f" % elem.grasa))
        if (self.inicio) == None:            
            fechaInforme = 'Hasta %s' % (utils.str_fecha(self.fin))
        else:
            fechaInforme = utils.str_fecha(self.inicio)+' - '+utils.str_fecha(self.fin)


        if datos != []:
            reports.abrir_pdf(geninformes.laboratorioLotes(datos,fechaInforme))

    def abrir_parte_tv(self, treeview, path, view_column):
        idlote = treeview.get_model()[path][-1]
        lote = pclases.Lote.get(idlote)
        try:
            parte = lote.balas[0].articulos[0].parteDeProduccion 
        except AttributeError, e:
            print "No se encontró el parte: %s", e
        if parte.es_de_balas():
            import partes_de_fabricacion_balas
            ventana_parteb = partes_de_fabricacion_balas.PartesDeFabricacionBalas(parte)  # @UnusedVariable
        else:
            import partes_de_fabricacion_rollos
            ventana_parteb = partes_de_fabricacion_rollos.PartesDeFabricacionRollos(parte)  # @UnusedVariable
            

if __name__ == '__main__':
    t = ConsultaLotesPorProducto()
