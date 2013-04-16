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
## consulta_cobros.py - Cobros y vencimientos de cobro (pendientes o no).
###################################################################
## NOTAS:
## Procede de consulta_pagos. Se conserva el código Logic por si 
## fuera necesario en una próxima versión.
###################################################################
## Changelog:
## 4 de abril de 2006 -> Inicio
## 17 de julio de 2006 -> Puesta a punto.
###################################################################
from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk, time
from framework import pclases
import mx.DateTime
from formularios import ventana_progreso
import re


class ConsultaCobros(Ventana):
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
        Ventana.__init__(self, 'consulta_cobros.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       'b_exportar/clicked': self.exportar}
        self.add_connections(connections)
        cols = (('Fecha','gobject.TYPE_STRING',False,True, True, None),
                ('Vencimientos','gobject.TYPE_STRING',False,False,False,None),
                ('Factura(Cliente)', 'gobject.TYPE_STRING',False,True, False,None),
                ('Cobros','gobject.TYPE_STRING',False,False,False,None),
                ('Factura(Cliente)', 'gobject.TYPE_STRING',False,True, False,None),
                ('id','gobject.TYPE_STRING',False,False,False,None))
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        col = self.wids['tv_datos'].get_column(1)
        for cell in col.get_cell_renderers():
            cell.set_property("xalign", 1)
        col = self.wids['tv_datos'].get_column(3)
        for cell in col.get_cell_renderers():
            cell.set_property("xalign", 1)
        temp = time.localtime()
        self.fin = str(temp[0])+'/'+str(temp[1])+'/'+str(temp[2])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        tempinicio = mx.DateTime.localtime() - mx.DateTime.oneDay * 30
        tempinicio = utils.str_fecha(tempinicio)
        self.inicio = tempinicio
        self.wids['e_fechainicio'].set_text(tempinicio)
        self.wids['e_estimados'].set_property('visible', False)
        self.wids['label8'].set_property('visible', False)
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

    def corregir_nombres_fecha(self, s):
        """
        Porque todo hombre debe enfrentarse al menos una 
        vez en su vida a dos tipos de sistemas operativos: 
        los que tienen en cuenta las locales y los que se 
        lo pasan por el forro.
        """
        trans = {'Monday': 'lunes',
                 'Tuesday': 'martes',
                 'Wednesday': 'miércoles',
                 'Thursday': 'jueves',
                 'Friday': 'viernes',
                 'Saturday': 'sábado',
                 'Sunday': 'domingo',
                 'January': 'enero',
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
            s = s.replace(in_english, trans[in_english])
        return s

    def rellenar_tabla(self, elementos):
        """
        Rellena el model con los items de la consulta.
        Elementos es un diccionario con objetos fecha como claves y 
        un diccionaro de dos elementos como valor. El segundo diccionario
        debe tener tres claves: 'cobros', 'vencimientos' y 'logic'. En cada
        una de ellas se guarda una lista de objetos de la clase correspondiente.
        """        
        model = self.wids['tv_datos'].get_model()
        model.clear()
        cobros = 0
        vencimientos = 0
        for fecha in elementos:
            sumvtos = 0 
            frasvtos = []
            cobrosvencimientos = elementos[fecha]
            for p in cobrosvencimientos['vencimientos']:
                if p.facturaVenta != None:
                    frasvtos.append("%s(%s)" % (p.facturaVenta.numfactura, 
                        p.facturaVenta.cliente and p.facturaVenta.cliente.nombre or ""))
                if p.prefactura != None:
                    frasvtos.append("%s(%s)" % (p.prefactura.numfactura, 
                        p.prefactura.cliente and p.prefactura.cliente.nombre or ""))
                sumvtos += p.importe
            for p in cobrosvencimientos['logic']:
                sumvtos += p['importe']
                frasvtos.append(p['codigo'])
            sumcobros = 0 
            frascobros = []
            for p in cobrosvencimientos['cobros']:
                if p.facturaVenta != None:
                    frascobros.append("%s(%s)" % (p.facturaVenta.numfactura, 
                        p.facturaVenta.cliente and p.facturaVenta.cliente.nombre or ""))
                if p.prefactura != None:
                    frascobros.append("%s(%s)" % (p.prefactura.numfactura, 
                        p.prefactura.cliente and p.prefactura.cliente.nombre or ""))
                # if p.logicMovimientos != None:   # Es posible que venga de Logic.
                #     if p.facturaVenta != None:
                #         frascobros[-1] = "%s [LOGIC:%s]" % (frascobros[-1], p.logicMovimientos.get_codigo())
                #     else:
                #         frascobros.append("[LOGIC:%s]" % (p.logicMovimientos.get_codigo()))
                sumcobros += p.importe
            cobros += sumcobros
            vencimientos += sumvtos
            fras = ", ".join([f[:f.index("(")] for f in frasvtos])
            vtos = ", ".join([f[:f.index("(")] for f in frascobros])
            MAX_LINEA = 50
            # padre = model.append(None, (self.corregir_nombres_fecha(fecha.strftime('%A, %d de %B de %Y')), 
            padre = model.append(None, (utils.str_fecha(fecha), 
                                        utils.float2str(sumvtos), 
                                        len(fras) > MAX_LINEA 
                                            and "%s..." % fras[:MAX_LINEA-3] 
                                            or fras,
                                        utils.float2str(sumcobros),
                                        len(vtos) > MAX_LINEA 
                                            and "%s..." % vtos[:MAX_LINEA-3] 
                                            or vtos,
                                        ""))
            for i in xrange(max(len(cobrosvencimientos['cobros']), 
                                len(cobrosvencimientos['vencimientos'])+len(cobrosvencimientos['logic']))):
                if i < len(cobrosvencimientos['cobros']):
                    p = cobrosvencimientos['cobros'][i]
                    if p.facturaVenta != None:
                        fracobro = "%s(%s)" % (p.facturaVenta.numfactura, 
                            p.facturaVenta.cliente and p.facturaVenta.cliente.nombre or "")
                    if p.prefactura != None:
                        fracobro = "%s(%s)" % (p.prefactura.numfactura, 
                            p.prefactura.cliente and p.prefactura.cliente.nombre or "")
                    # if p.logicMovimientos != None:   # Es posible que venga de Logic.
                    #     if p.facturaVenta != None:
                    #         fracobro = "%s [LOGIC:%s]" % (fracobro, p.logicMovimientos.get_codigo())
                    #     else:
                    #         fracobro = "[LOGIC:%s]" % (p.logicMovimientos.get_codigo())
                    importecobro = p.importe
                else:
                    importecobro = ""
                    fracobro = ""
                if i < len(cobrosvencimientos['vencimientos']):
                    p = cobrosvencimientos['vencimientos'][i]
                    if p.facturaVenta != None:
                        fravto = "%s(%s)" % (p.facturaVenta.numfactura, 
                            p.facturaVenta.cliente and p.facturaVenta.cliente.nombre or "")
                    if p.prefactura != None:
                        fravto = "%s(%s)" % (p.prefactura.numfactura, 
                            p.prefactura.cliente and p.prefactura.cliente.nombre or "")
                    importevto = p.importe
                else:
                    j = i-len(cobrosvencimientos['vencimientos'])
                    if j < len(cobrosvencimientos['logic']):
                        p = cobrosvencimientos['logic'][j]
                        importevto = p['importe']
                        fravto = "%s(%s)" % (p['comentario'], p['cuenta'])
                    else:
                        importevto = ""
                        fravto = ""
                model.append(padre, ("", 
                                     importevto != "" and utils.float2str(importevto) or "",
                                     fravto,
                                     importecobro != "" and utils.float2str(importecobro) or "",
                                     fracobro,
                                     ""))
        total = vencimientos - cobros
        self.wids['e_total'].set_text("%s €" % utils.float2str(total))
        self.wids['e_cobros'].set_text("%s €" % utils.float2str(cobros))
        self.wids['e_vencimientos'].set_text("%s €" % utils.float2str(vencimientos))
        
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
        Permite ordenar una lista de cadenas de fecha
        """
        fecha1 = time.strptime(e1[0],"%d/%m/%Y")
        fecha2 = time.strptime(e2[0],"%d/%m/%Y")
        if fecha1 < fecha2:
            return -1
        elif fecha1 > fecha2:
            return 1
        else:
            return 0

        
    def buscar(self,boton):
        if not self.inicio:
            cobros = pclases.Cobro.select(pclases.Cobro.q.fecha <= self.fin, orderBy = 'fecha')
        else:
            cobros = pclases.Cobro.select(pclases.AND(pclases.Cobro.q.fecha >= self.inicio,
                                                      pclases.Cobro.q.fecha <= self.fin), orderBy = 'fecha')
        if not self.inicio:
            vencimientos = pclases.VencimientoCobro.select(pclases.VencimientoCobro.q.fecha <= self.fin, 
                                                           orderBy = 'fecha')
        else:
            vencimientos = pclases.VencimientoCobro.select(
                                pclases.AND(pclases.VencimientoCobro.q.fecha >= self.inicio,
                                              pclases.VencimientoCobro.q.fecha <= self.fin), orderBy = 'fecha')
        elementos = {}
        for item in cobros:
            if item.fecha not in elementos:
                elementos[item.fecha] = {'cobros': [], 'vencimientos': [], 'logic': []}
            elementos[item.fecha]['cobros'].append(item)
        for item in vencimientos:
            if item.fecha not in elementos:
                elementos[item.fecha] = {'cobros': [], 'vencimientos': [], 'logic': []}
            elementos[item.fecha]['vencimientos'].append(item)
        # for item in self.buscar_vencimientos_logic(self.inicio, self.fin):
        #     if item['fecha'] not in elementos:
        #         elementos[item['fecha']] = {'cobros': [], 'vencimientos': [], 'logic': []}
        #     elementos[item['fecha']]['logic'].append(item)
        self.rellenar_tabla(elementos)
        
    def buscar_vencimientos_logic(self, fechaini, fechafin):
        """
        Devuelve una lista de diccionarios que contiene posibles vencimientos
        obtenidos de la tabla de movimientos de Logic.
        En la tabla se buscarán los apuntes que contengan "Vto" y una fecha a
        continuación y que en el propio Logic no se haya saldado ya (porque 
        si se han saldado antes de importarlas por primera vez, significa que
        son apuntes antiguos que no se van a pagar por el programa).
        Cada uno de las tuplas encontradas se devuelve como un diccionario
        que contiene fecha de vencimiento, importe, comentario, cuenta e id.
        """
        Logic = pclases.LogicMovimientos
        ls = Logic.select(pclases.AND(Logic.q.contrapartidaInfo == '',
                                      Logic.q.importe >= 0,
                                      pclases.OR(Logic.q.comentario.contains('Vto'),
                                                 Logic.q.comentario.contains('VTO'),
                                                 Logic.q.comentario.contains('vto'))))
        vpro = ventana_progreso.VentanaActividad(texto = "Procesando tablas Logic...", padre = self.wids['ventana'])
        vpro.mostrar()
        res = []
        try:
            for l in ls:
                vpro.mover()
                if self.cumple_requisitos(l, fechaini, fechafin):
                    res.append(self.convertir_a_dicc(l))
        finally:
            vpro.ocultar()
        return res

    def convertir_a_dicc(self, tuplalogic):
        res = {'fecha': self.get_fecha_vto_logic(tuplalogic),
               'importe': tuplalogic.importe,
               'comentario': tuplalogic.comentario, 
               'cuenta': tuplalogic.cuenta,
               'codigo': tuplalogic.get_codigo(),
               'id': tuplalogic.id}
        return res

    def cumple_requisitos(self, tuplalogic, fechaini, fechafin):
        """
        Devuelve True si la tupla tiene una fecha válida interpretable 
        como vencimiento y ésta está dentro de los criterios.
        """
        fechavto = self.get_fecha_vto_logic(tuplalogic) 
        return fechavto and fechavto >= fechaini and fechavto <= fechafin

    def get_fecha_vto_logic(self, l):
        """
        Devuelve una fecha con el vencimiento de la tupla Logic l o 
        None si no se pudo.
        """
        res = None
        s = l.comentario.upper()
        pivote = s.index('VTO')
        refdate = re.compile('\d+/\d+/\d+') # Regexp para fecha completa (con año)
        resdate = re.compile('\d+/\d+')     # Regexp para fecha con día/mes.
        fechavto = refdate.findall(s[pivote:])
        if fechavto != []:      # Fecha vencimiento viene completa
            try:
                res = time.strptime(fechavto[0], '%d/%m/%y')    # Intento fecha corta (dd/mm/aa)
            except ValueError:
                res = time.strptime(fechavto[0], '%d/%m/%Y')    # Debe ser fecha larga (dd/mm/aaaa)
        else:
            fechavto = resdate.findall(s[pivote:])
            if fechavto != []:       # Sólo tengo día y mes de vencimiento.
                # Tengo que buscarle el año de la fecha de la factura.
                fechafra = refdate.findall(s[:pivote])  # Solo busco la fecha con año. Sin año no me vale.
                if fechafra != []:  # Si la encuentro:
                    # TEMP: --------- Hay una fecha que me está jodiendo la vida: 
                    # ValueError: time data did not match format:  data=07/003/06  fmt=%d/%m/%Y
                    fechafra[0] = '/'.join([i[-2:] for i in fechafra[0].split('/')])
                    # END OF TEMP ---
                    try:
                        fechafra = time.strptime(fechafra[0], '%d/%m/%y')   # Intento fecha corta (dd/mm/aa)
                    except ValueError:
                        try:
                            fechafra = time.strptime(fechafra[0], '%d/%m/%Y')   # Debe estar en formato dd/mm/aaaa
                        except:
                            print s[:pivote], fechafra
                    anno = fechafra[0]  # strptime devuelve tupla con el año en la primera posición.
                    dia, mes = fechavto[0].split('/')
                    res = mx.DateTime.DateTimeFrom(day = int(dia), month = int(mes), year = int(anno))
        return res

    def imprimir(self,boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        from informes.treeview2pdf import treeview2pdf
        from formularios.reports import abrir_pdf
        strdiaini = self.wids['e_fechainicio'].get_text()
        strdiafin = self.wids['e_fechafin'].get_text()
        abrir_pdf(treeview2pdf(self.wids['tv_datos'], titulo = "Vencimientos y cobros por fecha", fecha = "Del %s al %s" % (strdiaini, strdiafin)))


if __name__ == '__main__':
    t = ConsultaCobros()

