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
## consulta_vencimientos_cobro.py - Vencimientos pendientes de cobro.
###################################################################
## NOTAS:
## Proviene de consulta...pagos. Se conserva el código 
## correspondiente a Logic por si acaso cambian las 
## especificaciones y es necesario importar cobros de Logic en el
## futuro.
###################################################################
## Changelog:
## 4 de abril de 2006 -> Inicio
## 17 de julio de 2006 -> Puesta a punto.
## DONE: Al "pagar en factura" ha puesto "Pagaré" en la forma de
## pago en lugar de "Introduzca aquí tal y cual". It's not a bug, 
## it's a feature! Lo que pone en observaciones por defecto es la
## forma de pago del cliente.
###################################################################

from formularios.ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk, time
import sys
from framework import pclases
import mx.DateTime
from informes import geninformes
import ventana_progreso
from vencimientos_pendientes_por_cliente import buscar_facturas_de_abono_sin_pagar

class ConsultaVencimientosCobros(Ventana):
    inicio = None
    fin = None
    resultado = []
        
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        global fin
        Ventana.__init__(self, 'consulta_vencimientos_cobro.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       'b_exportar/clicked': self.exportar}
        self.add_connections(connections)
        utils.rellenar_lista(self.wids['cmbe_cliente'], [(c.id, c.nombre) for c in pclases.Cliente.select(orderBy='nombre')])
        cols = (('Factura','gobject.TYPE_STRING',False,True, False,None),
                ('Fecha vto.','gobject.TYPE_STRING',False,True,False,None),
                ('Importe','gobject.TYPE_STRING',False,False,False,None),
                ('Observaciones/Forma de cobro','gobject.TYPE_STRING',False,True, False,None),
                ('Cliente', 'gobject.TYPE_STRING', False, True, True, None),
                ('id','gobject.TYPE_STRING',False,False,False,None))
        utils.preparar_listview(self.wids['tv_datos'], cols)
        self.wids['tv_datos'].connect("row-activated", self.abrir_factura)
        self.colorear(self.wids['tv_datos'])
        col = self.wids['tv_datos'].get_column(2)
        for cell in col.get_cell_renderers():
            cell.set_property("xalign", 1)
        self.wids['tv_datos'].connect('button_press_event', self.button_clicked)
        self.wids['tv_datos'].set_hover_selection(True)
        cols = (('Año y mes','gobject.TYPE_STRING', False,True, True, None),
                ('Total','gobject.TYPE_STRING', False, True, False, None),
                ('nada','gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_totales'], cols)
        col = self.wids['tv_totales'].get_column(1)
        for cell in col.get_cell_renderers():
            cell.set_property("xalign", 1)
        temp = time.localtime()
        self.fin = mx.DateTime.DateTimeFrom(day = temp[2], month = temp[1], year = temp[0])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.inicio = mx.DateTime.DateTimeFrom(day = 1, month = mx.DateTime.localtime().month, year = mx.DateTime.localtime().year)
        self.wids['e_fechainicio'].set_text(utils.str_fecha(self.inicio))
        gtk.main()
    
    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        tv = self.wids['tv_datos']
        abrir_csv(treeview2csv(tv))
        tv = self.wids['tv_totales']
        abrir_csv(treeview2csv(tv))

    def abrir_factura(self, tv, path, view_column):
        model = tv.get_model()
        if model[path][0] == "LOGIC":
            idlogic = model[path][-1].replace("L:", "")
            from formularios import mostrar_datos_logic
            ventanalogic = mostrar_datos_logic.MostrarDatosLogic(usuario = self.usuario, padre = self.wids['ventana'], consulta = " id == %d " % (idlogic))  # @UnusedVariable
        elif model[path][-1].startswith("A:"):
            idfrabono = model[path][-1].replace("A:", "")
            frabono = pclases.FacturaDeAbono.get(idfrabono)
            abono = frabono.abono
            if abono:
                from formularios import abonos_venta
                ventanabonos = abonos_venta.AbonosVenta(objeto = abono,  # @UnusedVariable
                                                        usuario = self.usuario)
            else:
                pass    # TODO: Algo debería hacer con las facturas de abono 
                        # sin abono. Empezando por descubrir cómo coño han 
                        # podido sobrevivir. NO PUEDE HABER FACTURAS DE ABONO 
                        # SIN ABONOS. Cojones ya. El mileniarismo va a shegar.
        else:
            idvto = model[path][-1].replace("V:", "")
            vto = pclases.VencimientoCobro.get(idvto)
            if vto.facturaVenta != None:
                from formularios import facturas_venta           
                ventanafacturas = facturas_venta.FacturasVenta(  # @UnusedVariable
                                    vto.facturaVenta, 
                                    usuario = self.usuario)
            elif vto.prefactura != None:
                import prefacturas
                ventanafacturas = prefacturas.Prefacturas(vto.prefactura,  # @UnusedVariable
                                                        usuario = self.usuario)

    def button_clicked(self, lista, event):
        model, itr = self.wids['tv_datos'].get_selection().get_selected()
        # DONE: URGENTE: La selección no devuelve el itr correcto 
        # hasta DESPUÉS de procesar el button_clicked, por tanto, la 
        # primera vez devuelve None y en sucesivas veces es posible que 
        # devuelva la selección anterior. Sólo rula bien cuando se selecciona 
        # primero con el izquierdo y después se saca el menú con el derecho. 
        # ARREGLADO HACIENDO QUE LA SELECCIÓN SIGA EL CURSOR CON LA PROPIEDAD
        # hover-selection DEL TREEVIEW.
        if itr == None: return
        ide = model[itr][-1]
        if event.button == 3 and not ide.startswith("A:"):
            ui_string = """<ui>
                            <popup name='Popup'>
                                <menuitem name='Pagare' action='Crear pagaré'/>
                                <menuitem name='Factura' action='Pagar en factura'/>
                            </popup>
                           </ui>"""
            ag = gtk.ActionGroup('WindowActions')
            actions = [('Crear pagaré', gtk.STOCK_NEW, '_Crear pagaré', '<control>C',
                        'Crea un nuevo pagaré con el vencimiento seleccionado.', 
                        self.crear_pagare),
                       ('Pagar en factura', gtk.STOCK_OPEN, '_Pagar en factura', '<control>P',
                        'Abre la factura para anotar el cobro del vencimiento allí.', 
                        self.pagar_en_factura)]
            ag.add_actions(actions)
            ui = gtk.UIManager() 
            ui.insert_action_group(ag, 0)
            ui.add_ui_from_string(ui_string)
            widget = ui.get_widget("/Popup")
            if itr != None:
                tiene_factura = model[itr][0] != "LOGIC"
            else:
                tiene_factura = False
            menuitem = ui.get_widget("/Popup/Factura")
            menuitem.set_sensitive(tiene_factura)
            menuitem = ui.get_widget("/Popup/Pagare")
            menuitem.set_sensitive(itr != None)
            widget.popup(None, None, None, event.button, event.time)
 
    def crear_pagare(self, something_But_i_dont_know):
        """
        Crea un nuevo pagaré con el apunte seleccionado y abre la
        ventana de pagarés con ese nuevo objeto.
        """
        model, itr = self.wids['tv_datos'].get_selection().get_selected()
        ide = model[itr][-1][model[itr][-1].index(":")+1:]
        if model[itr][0] == "LOGIC":
            logic = pclases.LogicMovimientos.get(ide)
            fechavto = self.get_fecha_vto_logic(logic)
            importe = logic.importe
            factura = None
            observaciones = logic.cuenta
            cliente = None
            vencimiento = None
        else:
            vencimiento = pclases.VencimientoCobro.get(ide)
            fechavto = vencimiento.fecha
            importe = vencimiento.importe
            factura = vencimiento.facturaVenta or vencimiento.prefactura
            observaciones = ''
            cliente = (vencimiento.facturaVenta and vencimiento.facturaVenta.cliente) \
                      or (vencimiento.prefactura and vencimiento.prefactura.cliente) or None
            logic = None
        pagare = pclases.PagareCobro(fechaCobro = fechavto, 
            cantidad = importe, 
            cobrado = -1, 
            observaciones = "Generado automáticamente.%s" \
                % (observaciones != "" 
                   and "\nCuenta logic: %s" % (observaciones) or 
                   ""), 
            fechaRecepcion = mx.DateTime.localtime(), 
            fechaCobrado = None, 
            procesado = False)
        pclases.Auditoria.nuevo(pagare, self.usuario, __file__)
        cobro = pclases.Cobro(facturaVenta = factura, 
                              cliente = cliente, 
                              # logicMovimientos = logic, 
                              pagareCobro = pagare, 
                              fecha = fechavto,
                              importe = importe, 
                              observaciones = observaciones, 
                              facturaDeAbono = None)
        pclases.Auditoria.nuevo(cobro, self.usuario, __file__)
        import pagares_cobros
        pp = pagares_cobros.PagaresCobros(pagare)  # @UnusedVariable
        self.buscar(None)   # Para recargar.

    def pagar_en_factura(self, requiem_for_syd_barret): 
        """
        Abre la factura correspondiente al vencimiento y con el 
        cobro ya añadido.
        """
        model, itr = self.wids['tv_datos'].get_selection().get_selected()
        ide = model[itr][-1][model[itr][-1].index(":")+1:]
        if model[itr][0] != "LOGIC":
            vencimiento = pclases.VencimientoCobro.get(ide)
            fecha = mx.DateTime.localtime() 
            importe = vencimiento.importe
            factura = vencimiento.facturaVenta or vencimiento.prefactura
            cliente = (vencimiento.facturaVenta and vencimiento.facturaVenta.cliente) \
                      or (vencimiento.prefactura and vencimiento.prefactura.cliente) or None
            if cliente != None:
                observaciones = cliente.documentodepago
            else:
                observaciones = "Escriba aquí la forma de pago"
            cobro = pclases.Cobro(facturaVenta = factura, 
                                  cliente = cliente, 
                                  # logicMovimientos = None, 
                                  pagareCobro = None, 
                                  fecha = fecha,
                                  importe = importe, 
                                  observaciones = observaciones, 
                                  facturaDeAbono = None)
            pclases.Auditoria.nuevo(cobro, self.usuario, __file__)
            import facturas_venta
            fc = facturas_venta.FacturasVenta(factura)  # @UnusedVariable
            self.buscar(None)   # Para recargar.
     
    def colorear(self, tv):
        def cell_func(col, cell, model, itr):
            d, m, a = model[itr][1].split('/')
            fecha = mx.DateTime.DateTimeFrom(day = int(d), month = int(m), year = int(a))
            hoy = mx.DateTime.localtime()
            if fecha < hoy:
                color = "red"
            elif fecha > hoy:
                color = "white"
            else:
                color = "orange"
            cell.set_property("cell-background", color)
        col = tv.get_column(1)
        cells = col.get_cell_renderers()
        for cell in cells:
            col.set_cell_data_func(cell, cell_func)

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, items):
        """
        Rellena el model con los items de la consulta
        """        
        model = self.wids['tv_datos'].get_model()
        model.clear()
        total = 0
        vencido = 0
        hoy = mx.DateTime.localtime()
        por_fecha = {}
        for i in items:
            if not i[2]:  # i[2] = False cuando es vencimiento normal de la BD
                if isinstance(i[1], pclases.FacturaDeAbono):
                    importe = i[1].calcular_importe_total()
                    anno = i[1].fecha.year
                    mes = i[1].fecha.month
                    total += importe 
                    if i[1].fecha < hoy:
                        vencido += importe
                    model.append((i[1].numfactura,
                                  utils.str_fecha(i[1].fecha),
                                  utils.float2str(importe),
                                  "",
                                  i[1].cliente and i[1].cliente.nombre or "",
                                  "A:" + `i[1].id`))
                else:
                    total += i[1].importe 
                    importe = i[1].importe
                    anno = i[1].fecha.year
                    mes = i[1].fecha.month
                    if i[1].fecha < hoy:
                        vencido += i[1].importe
                    fra = i[1].facturaVenta or i[1].prefactura
                    model.append((fra.numfactura,
                                  utils.str_fecha(i[1].fecha),
                                  utils.float2str(importe),
                                  i[1].observaciones,
                                  fra.cliente.nombre,
                                  "V:" + `i[1].id`))
            else:   # i[2] = True. Es un vencimiento rescatado de LogicMovimientos.
                importe = i[1]['importe']
                anno = i[1]['fecha'].year
                mes = i[1]['fecha'].month
                total += i[1]['importe']
                if i[1]['fecha'] < hoy:
                    vencido += i[1]['importe']
                model.append(("LOGIC",      # Esto me va a valer para diferenciar un vto. de la BD de uno de Logic.
                              utils.str_fecha(i[1]['fecha']),
                              utils.float2str(i[1]['importe']),
                              i[1]['comentario'],
                              i[1]['cuenta'],
                              "L:" + i[1]['id']))
            if anno not in por_fecha:
                por_fecha[anno] = {}
            if mes not in por_fecha[anno]:
                por_fecha[anno][mes] = 0.0
            por_fecha[anno][mes] += importe
        self.wids['e_total'].set_text("%s €" % utils.float2str(total))
        self.wids['e_vencido'].set_text("%s €" % utils.float2str(vencido))
        # Relleno el model de totales.
        annos = por_fecha.keys()
        annos.sort()
        model = self.wids['tv_totales'].get_model()
        model.clear()
        for anno in annos:
            total_anno = sum([por_fecha[anno][mes] for mes in por_fecha[anno]])
            anno_padre = model.append(None, (`anno`, 
                                             utils.float2str(total_anno), 
                                             ""))
            meses = por_fecha[anno].keys()
            meses.sort()
            for mes in meses:
                model.append(anno_padre, ("%02d - %s" % (mes, utils.MESES[mes]), 
                                          utils.float2str(por_fecha[anno][mes]),
                                          ""))
        
    def set_inicio(self,boton):
        temp = utils.mostrar_calendario(fecha_defecto = utils.parse_fecha(self.wids['e_fechainicio'].get_text()), 
                                        padre = self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
        self.inicio = mx.DateTime.DateTimeFrom(year = int(temp[2]), month = int(temp[1]), day = (temp[0]))

    def set_fin(self,boton):
        temp = utils.mostrar_calendario(fecha_defecto = utils.parse_fecha(self.wids['e_fechafin'].get_text()), 
                                        padre = self.wids['ventana'])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.fin = mx.DateTime.DateTimeFrom(year = int(temp[2]), month = int(temp[1]), day = (temp[0]))

    def por_fecha(self,e1,e2):
        """
        Permite ordenar una lista de cadenas de fecha
        """
        fecha1 = e1[0]
        fecha2 = e2[0]
        if fecha1 < fecha2:
            return -1
        elif fecha1 > fecha2:
            return 1
        else:
            return 0

    def buscar(self,boton):
        if not self.inicio:
            vencimientos = pclases.VencimientoCobro.select(
                pclases.VencimientoCobro.q.fecha <= self.fin, 
                orderBy = 'fecha')
            estimados = pclases.EstimacionCobro.select(
                pclases.EstimacionCobro.q.fecha <= self.fin, 
                orderBy = 'fecha')
        else:
            vencimientos = pclases.VencimientoCobro.select(pclases.AND(
                    pclases.VencimientoCobro.q.fecha >= self.inicio,
                    pclases.VencimientoCobro.q.fecha <= self.fin), 
                orderBy='fecha')       
            estimados = pclases.EstimacionCobro.select(pclases.AND(
                    pclases.EstimacionCobro.q.fecha >= self.inicio,
                    pclases.EstimacionCobro.q.fecha <= self.fin), 
                orderBy='fecha')       
        
        idcliente = utils.combo_get_value(self.wids['cmbe_cliente'])
        if idcliente != None:
            cliente = pclases.Cliente.get(
                utils.combo_get_value(self.wids['cmbe_cliente']))
            vencimientos = [v for v in vencimientos 
                            if (v.facturaVenta 
                                and v.facturaVenta.clienteID == cliente.id) 
                               or 
                               (v.prefactura 
                                and v.prefactura.clienteID == cliente.id)]
            estimados = [e for e in estimados 
                         if (e.facturaVenta 
                             and e.facturaVenta.clienteID == cliente.id) 
                            or
                            (e.prefactura 
                             and e.prefactura.clienteID == cliente.id)]
            abonos = buscar_facturas_de_abono_sin_pagar(cliente, 
                                                        self.inicio, self.fin)
        else:
            abonos = []
            for cliente in pclases.Cliente.select():
                abonos += buscar_facturas_de_abono_sin_pagar(cliente, 
                                                             self.inicio, 
                                                             self.fin)

        self.resultado = [[a.fecha, a, False] for a in abonos]
        for i in vencimientos:
            if not self.esta_cobrado(i):
                self.resultado.append([i.fecha,i,False])
        # XXX Esto estaba comentado. ¿Por qué? Ya sé el porqué. Porque de 
        # LOGIC solo sacamos las obligaciones de pago, no las de cobro.
        #if idcliente == None:     # Porque en Logic los clientes no son los mismos que 
        #                          # aquí (no están exactamente igual escritos)
        #    vencimientos_logic = self.buscar_vencimientos_logic(self.inicio, self.fin)
        #    for i in vencimientos_logic:
        #        self.resultado.append([i['fecha'],i,True])
        # XXX
        self.resultado.sort(self.por_fecha)
        self.rellenar_tabla(self.resultado)

    def buscar_vencimientos_logic(self, fechaini, fechafin):
        """
        Devuelve una lista de diccionarios que contiene posibles vencimientos
        obtenidos de la tabla de movimientos de Logic.
        En la tabla se buscarán los apuntes que contengan "Vto" y una fecha a
        continuación, que no estén ya relacionados con ningún cobro y que en 
        el propio Logic no se haya saldado ya.
        Cada uno de las tuplas encontradas se devuelve como un diccionario
        que contiene fecha de vencimiento, importe, comentario, cuenta e id.
        """
        Logic = pclases.LogicMovimientos
        ls = Logic.select(pclases.AND(Logic.q.contrapartidaInfo == '',
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
               'id': tuplalogic.id}
        return res

    def cumple_requisitos(self, tuplalogic, fechaini, fechafin):
        """
        Devuelve True si la tupla tiene una fecha válida interpretable 
        como vencimiento, no se ha usado en ningún cobro ya y ésta 
        está dentro de los criterios.
        """
        fechavto = self.get_fecha_vto_logic(tuplalogic) 
        res = (fechavto 
               and fechavto >= fechaini 
               and fechavto <= fechafin 
               and tuplalogic.cobros == [])
        return res

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

    def esta_cobrado(self, vencimiento):
        """
        Devuelve True si el vencimiento está cobrado.
        """
        fra = vencimiento.facturaVenta or vencimiento.prefactura
        cobros = fra.cobros
        vencimientos = fra.vencimientosCobro[:]
        vencimientos.sort(self.cmp_fechas)
        # Los vencimientos cobrados están en las posiciones 0:|cobros|. Es decir, si 
        # hay dos cobros, los vencimientos cobrados serán el 0 y el 1 (a no ser que 
        # los vencimientos no se paguen por orden cronológico, que eso ya sería 
        # rizar el rizo.
        return vencimiento in vencimientos[:len(cobros)]

    def cmp_fechas(self, r1, r2):
        """
        Compara dos CAMPOS fecha de dos REGISTROS. (Diferente a self.por_fecha)
        """
        if r1.fecha < r2.fecha:
            return -1
        elif r1.fecha > r2.fecha:
            return 1
        else:
            return 0

    def imprimir(self,boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        from formularios import reports as informes
        datos = []
        for i in self.resultado:
            if not i[2]:    # i[2] = False cuando es vencimiento normal de la BD
                if isinstance(i[1], pclases.FacturaDeAbono):
                    importe = i[1].calcular_importe_total()
                    datos.append((i[1].numfactura,
                                  utils.str_fecha(i[1].fecha),
                                  utils.float2str(importe),
                                  "",
                                  i[1].cliente and i[1].cliente.nombre or ""))
                else:
                    fra = i[1].facturaVenta or i[1].prefactura
                    datos.append((fra.numfactura,
                                  utils.str_fecha(i[1].fecha),
                                  utils.float2str(i[1].importe),
                                  i[1].observaciones,
                                  fra.cliente.nombre))
            else:   # i[2] = True. Es un vencimiento rescatado de LogicMovimientos.
                datos.append(("LOGIC",      # Esto me va a valer para diferenciar un vto. de la BD de uno de Logic.
                              utils.str_fecha(i[1]['fecha']),
                              utils.float2str(i[1]['importe']),
                              i[1]['comentario'],
                              i[1]['cuenta']))
        if (self.inicio) == None:            
            fechaInforme = 'Hasta %s' % (utils.str_fecha(self.fin))
        else:
            fechaInforme = utils.str_fecha(self.inicio)+' - '+utils.str_fecha(self.fin)
        if datos != []:
            model = self.wids['tv_totales'].get_model()
            datos.append(("---", )*5)
            datos.append(("TOTALES POR MES Y AÑO", ">->", ">->", ">->", ">->"))
            for fila in model:
                datos.append((fila[0], "", fila[1], "", ""))
                iter_filames = model.iter_children(fila.iter)
                while iter_filames:
                    filames = model[iter_filames]
                    datos.append(("", filames[0], filames[1], "", ""))
                    iter_filames = model.iter_next(iter_filames)
            datos.append(("---", )*5)
            datos.append(("", 
                          "Total", 
                          self.wids['e_total'].get_text(), 
                          "Vencido a la fecha", 
                          self.wids['e_vencido'].get_text()))
            informes.abrir_pdf(geninformes.vencimientosCobro(datos,fechaInforme))

if __name__ == '__main__':
    t = ConsultaVencimientosCobros()

