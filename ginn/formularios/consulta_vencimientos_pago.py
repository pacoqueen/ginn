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
## consulta_vencimientos_pago.py - Vencimientos pendientes de pago.
###################################################################
## TODO:
##  En vencimientos parcialmente pagados, crear pagaré, hacer 
##  transferencia, etc. deben tomar el importe pendiente, no el 
##  importe completo del vencimiento.
###################################################################
## Changelog:
## 4 de abril de 2006 -> Inicio
## 17 de julio de 2006 -> Puesta a punto.
###################################################################
from framework import pclases
from informes import geninformes
from ventana import Ventana
import gtk
import time
import mx.DateTime
import pygtk
import re
from formularios import utils
from formularios import ventana_progreso
pygtk.require('2.0')


class ConsultaVencimientosPagos(Ventana):
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
        Ventana.__init__(self, 'consulta_vencimientos_pago.glade', objeto,
                         usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       'b_csv/clicked': self.exportar, 
                       'ch_formapago/toggled': 
                            lambda ch: self.wids['cb_formapago'].set_sensitive(
                                ch.get_active()), 
                       }
        self.wids['cb_formapago'].set_sensitive(
                self.wids['ch_formapago'].get_active())
        formaspago = [p.documentodepago.strip().split(" ")[0] 
                      for p in pclases.Proveedor.select()]
        formaspago = filtrar_tildes_lista(formaspago)
        formaspago = [e.lower() for e in formaspago]
        formaspago = utils.unificar(formaspago)
        formaspago.sort()
        self.formaspago = zip(range(len(formaspago)), formaspago)
        utils.rellenar_lista(self.wids['cb_formapago'], self.formaspago)
        self.add_connections(connections)
        utils.rellenar_lista(self.wids['cmbe_proveedor'],
                [(c.id, c.nombre) 
                    for c in pclases.Proveedor.select(orderBy='nombre')])
        cols = (('Factura','gobject.TYPE_STRING', False, True, False, None),
                ('Visto bueno','gobject.TYPE_STRING', False, True, False, None),
                ('Fecha vto.','gobject.TYPE_STRING', False, True, False, None),
                ('Importe','gobject.TYPE_STRING', False, False, False, None),
                ('Pendiente','gobject.TYPE_STRING', False, False, False, None),
                ('Fecha fra.','gobject.TYPE_STRING', False, True, False, None),
                ('Observaciones/Forma de pago','gobject.TYPE_STRING',
                    False, True, False, None),
                ('Proveedor', 'gobject.TYPE_STRING', False, True, True, None),
                ('Doc. de pago del proveedor', 'gobject.TYPE_STRING', 
                    False, True, True, None),
                ('id','gobject.TYPE_STRING',False,False,False,None))
        utils.preparar_listview(self.wids['tv_datos'], cols)
        self.wids['tv_datos'].get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        self.wids['tv_datos'].connect("row-activated", self.abrir_factura)
        self.colorear(self.wids['tv_datos'])
        col = self.wids['tv_datos'].get_column(3)
        for cell in col.get_cell_renderers():
            cell.set_property("xalign", 1)
        col = self.wids['tv_datos'].get_column(4)
        for cell in col.get_cell_renderers():
            cell.set_property("xalign", 1)
        self.wids['tv_datos'].connect('button_release_event',
                                      self.button_clicked) 
        cols = (('Año y mes','gobject.TYPE_STRING', False,True, True, None),
                ('Total','gobject.TYPE_STRING', False, True, False, None),
                ('nada','gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_totales'], cols)
        col = self.wids['tv_totales'].get_column(1)
        for cell in col.get_cell_renderers():
            cell.set_property("xalign", 1)
        temp = time.localtime()
        self.fin = mx.DateTime.DateTimeFrom(day = temp[2], 
                                            month = temp[1], 
                                            year = temp[0])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        gtk.main()

    def abrir_factura(self, tv, path, view_column):
        model = tv.get_model()
        if model[path][0] == "LOGIC":
            idlogic = model[path][-1]
            from formularios import mostrar_datos_logic
            ventanalogic = mostrar_datos_logic.MostrarDatosLogic(
                            usuario = self.usuario, 
                            padre = self.wids['ventana'], 
                            consulta = " ide = %s " % (idlogic))
        else:
            idvto = model[path][-1]
            vto = pclases.VencimientoPago.get(idvto)
            fra = vto.facturaCompra
            from formularios import facturas_compra          
            ventanafacturas = facturas_compra.FacturasDeEntrada(
                                vto.facturaCompra, 
                                usuario = self.usuario)
            # FIXME: Recargo la información aunque, OJO, es posible que el 
            # vencimiento se haya ido a otra fecha que no entre en la consulta
            # o que incluso se haya dividido en dos.
            try:
                vto = fra.vencimientosPago[0]
                vtobueno = fra.vistoBuenoPago and fra.numeroControl or "PENDIENTE" 
                pendiente = vto.calcular_importe_pdte()
                model[path] = ((vto.facturaCompra.numfactura,
                                vtobueno, 
                                utils.str_fecha(vto.fecha),
                                utils.float2str(vto.importe),
                                utils.float2str(pendiente),
                                utils.str_fecha(vto.facturaCompra.fecha),
                                vto.observaciones,
                                vto.facturaCompra.proveedor.nombre,
                                vto.facturaCompra.proveedor.documentodepago, 
                                vto.id))
            except IndexError:  # No vencimientos, quito la factura.
                model.remove(model.get_iter(path))

    def button_clicked(self, lista, event):
        if event.button == 3:
            ui_string = """<ui>
                            <popup name='Popup'>
                                <menuitem name='Pagare' action='Crear pagaré'/>
                                <menuitem name='Factura' action='Pagar en factura'/>
                                <menuitem name='Transferencia' action='Hacer transferencia'/>
                            </popup>
                           </ui>"""
            ag = gtk.ActionGroup('WindowActions')
            actions = [('Crear pagaré', gtk.STOCK_NEW, '_Crear pagaré', '<Control>c',
                        'Crea un nuevo pagaré con el vencimiento seleccionado.', 
                        self.crear_pagare),
                       ('Pagar en factura', gtk.STOCK_OPEN, '_Pagar en factura', '<Control>p',
                        'Abre la factura para anotar el pago del vencimiento allí.', 
                        self.pagar_en_factura),
                       ('Hacer transferencia', gtk.STOCK_NETWORK, '_Hacer transferencia', '<Control>h',
                        'Abre la ventana de transferencias.', 
                        self.hacer_transferencia)]
            ag.add_actions(actions)
            ui = gtk.UIManager() 
            ui.insert_action_group(ag, 0)
            ui.add_ui_from_string(ui_string)
            widget = ui.get_widget("/Popup")
            model, paths = self.wids['tv_datos'].get_selection().get_selected_rows()
            if len(paths) > 0:
                itr = model.get_iter(paths[0])
                if itr != None:
                    tiene_factura = model[itr][0] != "LOGIC"
                else:
                    tiene_factura = False
                single_selection = len(paths) == 1
                menuitem = ui.get_widget("/Popup/Factura")
                menuitem.set_sensitive(tiene_factura and single_selection)
                menuitem = ui.get_widget("/Popup/Pagare")
                menuitem.set_sensitive(itr != None)
                menuitem = ui.get_widget("/Popup/Transferencia")
                menuitem.set_sensitive(pclases.CuentaOrigen.select().count() > 0 and single_selection)
                widget.popup(None, None, None, event.button, event.time)
                #self.wids['tv_datos'].get_selection().select_range(paths[0], paths[-1])
                #self.wids['tv_datos'].get_selection().select_path(paths[-1])
 
    def crear_pagare(self, something_But_i_dont_know):
        """
        Crea un nuevo pagaré con el apunte seleccionado y abre la
        ventana de pagarés con ese nuevo objeto.
        """
        model, paths = self.wids['tv_datos'].get_selection().get_selected_rows()
        fechavto = pclases.DatosDeLaEmpresa.calcular_dia_de_pago()
        importe = 0
        observaciones = ""
        # CWT: (mrodriguez) El día de emisión debe ser el 25.
        fecha_pago = pclases.DatosDeLaEmpresa.calcular_dia_de_pago()
        pagare = pclases.PagarePago(fechaPago = fechavto, 
                                    cantidad = importe, 
                                    pagado = -1, 
                                    observaciones = observaciones, 
                                    fechaEmision = fecha_pago, 
                                    fechaCobrado = None)
        pclases.Auditoria.nuevo(pagare, self.usuario, __file__)
        erroneos = []
        for path in paths:
            itr = model.get_iter(path)
            ide = model[itr][-1]
            if model[itr][0] == "LOGIC":
                vencimiento = None
                try:
                    logic = pclases.LogicMovimientos.get(ide)
                except pclases.SQLObjectNotFound:
                    logic = None
                    erroneos.append(model[path][6])
                else:
                    fechavto = self.get_fecha_vto_logic(logic)
                    importe = logic.importe
                    factura = None
                    observaciones = logic.cuenta
                    proveedor = None
            else:
                logic = None
                try:
                    vencimiento = pclases.VencimientoPago.get(ide)
                    vencimiento.sync()
                except pclases.SQLObjectNotFound:
                    vencimiento = None
                    erroneos.append(model[path][0])
                else:
                    fechavto = vencimiento.fecha
                    #importe = vencimiento.importe
                    importe = vencimiento.calcular_importe_pdte()
                    factura = vencimiento.facturaCompra
                    observaciones = ''
                    proveedor = (vencimiento.facturaCompra
                            and vencimiento.facturaCompra.proveedor or None)
            if logic or vencimiento: # Si ambos None, el registro fue borrado
                pago = pclases.Pago(facturaCompra = factura, 
                                    proveedor = proveedor, 
                                    logicMovimientos = logic, 
                                    pagarePago = pagare, 
                                    fecha = fechavto,
                                    importe = importe, 
                                    observaciones = observaciones)
                pclases.Auditoria.nuevo(pago, self.usuario, __file__)
                # Actualizo campos del pagaré: 
                pagare.fechaPago = fechavto     # Se quedará con la fecha del vencimiento de lo último seleccionado. Todas deberían ser la misma, de cualquier modo.
                pagare.cantidad += importe
                pagare.observaciones += "%s" % (observaciones != "" and "\nCuenta logic: %s" % (observaciones) or "") 
                pagare.sync()
                ####
        if erroneos:
            utils.dialogo_info(titulo="ERROR AL CREAR PAGARÉ", 
                    texto="El pagaré se ha creado, pero los vencimientos\n"
                          "correspondientes a:\n%s\n"
                          "no se pudieron agregar.\n"
                          "A continuación se abrirá el pagaré creado.\n"
                          "Por favor, complételo manualmente." % (
                              ", ".join(erroneos)), 
                    padre=self.wids['ventana'])
        from formularios import pagares_pagos
        pp = pagares_pagos.PagaresPagos(pagare, usuario = self.usuario)  # @UnusedVariable
        try:
            self.buscar(None)   # Para recargar.
        except AttributeError, msg:  # No tenía proveedor o algo ha pasado. Lo mando al logger:
            self.logger.error("%sconsulta_vencimientos_pago::crear_pagare -> Excepción: %s" % (self.usuario and self.usuario.usuario + ": " or "", msg))

    def hacer_transferencia(self, keith_moon_lives): 
        """
        Abre la ventana de transferencias con una nueva transferencia 
        y los datos por defecto introducidos.
        """
        model, paths = self.wids['tv_datos'].get_selection().get_selected_rows()
        for path in paths:
            itr = model.get_iter(path)
            ide = model[itr][-1]
            if model[itr][0] == "LOGIC":
                logic = pclases.LogicMovimientos.get(ide)
                fechavto = self.get_fecha_vto_logic(logic)
                importe = logic.importe
                factura = None
                observaciones = "%s: %s" % (logic.cuenta, logic.comentario)
                proveedor = None
                vencimiento = None
            else:
                vencimiento = pclases.VencimientoPago.get(ide)
                fechavto = vencimiento.fecha
                importe = vencimiento.calcular_importe_pdte()
                #importe = vencimiento.importe
                factura = vencimiento.facturaCompra
                observaciones = ''
                proveedor = vencimiento.facturaCompra and vencimiento.facturaCompra.proveedor or None
                logic = None
            pago = pclases.Pago(facturaCompra = factura, 
                                proveedor = proveedor, 
                                logicMovimientos = logic, 
                                pagarePago = None, 
                                fecha = fechavto,
                                importe = importe, 
                                observaciones = "Transferencia a %s por pago de %s." % (proveedor and proveedor.nombre or "?", 
                                                                                        (factura and factura.numfactura) or observaciones), 
                                cuentaOrigen = pclases.CuentaOrigen.select(orderBy = "-id")[0], 
                                cuentaDestino = proveedor and proveedor.cuentasDestino and proveedor.cuentasDestino[0] or None)
            pclases.Auditoria.nuevo(pago, self.usuario, __file__)
            from formularios import transferencias
            tr = transferencias.Transferencias(pago, usuario = self.usuario)  # @UnusedVariable
            self.buscar(None)   # Para recargar.

    def pagar_en_factura(self, requiem_for_syd_barret): 
        """
        Abre la factura correspondiente al vencimiento y con el 
        pago ya añadido.
        """
        model, paths = self.wids['tv_datos'].get_selection().get_selected_rows()
        for path in paths:
            itr = model.get_iter(path)
            ide = model[itr][-1]
            if model[itr][0] != "LOGIC":
                vencimiento = pclases.VencimientoPago.get(ide)
                fecha = mx.DateTime.localtime() 
                #importe = vencimiento.importe
                importe = vencimiento.calcular_importe_pdte()
                factura = vencimiento.facturaCompra
                proveedor = vencimiento.facturaCompra and vencimiento.facturaCompra.proveedor or None
                if proveedor != None:
                    observaciones = proveedor.formadepago
                else:
                    observaciones = "Escriba aquí la forma de pago"
                pago = pclases.Pago(facturaCompra = factura, 
                                    proveedor = proveedor, 
                                    logicMovimientos = None, 
                                    pagarePago = None, 
                                    fecha = fecha,
                                    importe = importe, 
                                    observaciones = observaciones)
                pclases.Auditoria.nuevo(pago, self.usuario, __file__)
                from formularios import facturas_compra
                fc = facturas_compra.FacturasDeEntrada(factura, usuario = self.usuario)  # @UnusedVariable
                self.buscar(None)   # Para recargar.
     
    def colorear(self, tv):
        def cell_func(col, cell, model, itr):
            d, m, a = model[itr][2].split('/')
            fecha = mx.DateTime.DateTimeFrom(day = int(d), month = int(m), year = int(a))
            hoy = mx.DateTime.localtime()
            if fecha < hoy:
                color = "red"
            elif fecha > hoy:
                color = "white"
            else:
                color = "orange"
            cell.set_property("cell-background", color)
        def cell_func_vto_bueno(col, cell, model, itr):
            txt = model[itr][1]
            if txt == "N/A":
                color = "gray"
            elif txt == "PENDIENTE":
                color = "IndianRed"
            else:
                color = "LightBlue"
            cell.set_property("cell-background", color)
        col = tv.get_column(2)
        cells = col.get_cell_renderers()
        for cell in cells:
            col.set_cell_data_func(cell, cell_func)
        col = tv.get_column(1)
        cells = col.get_cell_renderers()
        for cell in cells:
            col.set_cell_data_func(cell, cell_func_vto_bueno)

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, items):
        """
        Rellena el model con los items de la consulta
        """        
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        ivpro = 0.0
        tot = len(items) + 1    # Por no hay items...
        vpro.set_valor(ivpro/tot, "Rellenando tabla...")
        model = self.wids['tv_datos'].get_model()
        model.clear()
        total = 0
        vencido = 0
        hoy = mx.DateTime.localtime()
        por_fecha = {}
        for i in items:
            vpro.set_valor(ivpro/tot, "Rellenando tabla...")
            ivpro += 1
            if not i[2]:  # i[2] = False cuando es vencimiento normal de la BD
                importe = i[1].importe
                anno = i[1].fecha.year
                mes = i[1].fecha.month
                pendiente = i[1].calcular_importe_pdte()
                if i[1].fecha < hoy:
                    vencido += pendiente
                    #vencido += i[1].importe
                total += pendiente
                #total += i[1].importe 
                fra = i[1].facturaCompra
                vtobueno = fra.vistoBuenoPago and fra.numeroControl or "PENDIENTE" 
                #vtobueno = i[1].facturaCompra.get_codigo_validacion_visto_bueno() == 0 and i[1].facturaCompra.numeroControl or "PENDIENTE"
                model.append((i[1].facturaCompra.numfactura,
                              vtobueno, 
                              utils.str_fecha(i[1].fecha),
                              utils.float2str(i[1].importe),
                              utils.float2str(pendiente),
                              utils.str_fecha(i[1].facturaCompra.fecha),
                              i[1].observaciones,
                              i[1].facturaCompra.proveedor.nombre,
                              i[1].facturaCompra.proveedor.documentodepago, 
                              i[1].id))
            else:   
                # i[2] = True. Es un vencimiento rescatado de LogicMovimientos.
                importe = i[1]['importe']
                anno = i[1]['fecha'].year
                mes = i[1]['fecha'].month
                total += i[1]['importe']
                if i[1]['fecha'] < hoy:
                    vencido += i[1]['importe']
                model.append(("LOGIC",  # Esto me va a valer para diferenciar 
                                        # un vto. de la BD de uno de Logic.
                              "N/A", 
                              utils.str_fecha(i[1]['fecha']),
                              utils.float2str(i[1]['importe']),
                              utils.float2str(i[1]['importe']),
                              "",
                              i[1]['comentario'],
                              i[1]['cuenta'],
                              "", 
                              i[1]['id']))
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
        ivpro = 0.0
        tot = len(annos * 12)
        for anno in annos:
            total_anno = sum([por_fecha[anno][mes] for mes in por_fecha[anno]])
            anno_padre = model.append(None, (`anno`, 
                                             utils.float2str(total_anno), 
                                             ""))
            meses = por_fecha[anno].keys()
            meses.sort()
            for mes in meses:
                vpro.set_valor(ivpro/tot, "Rellenando tabla por meses...")
                model.append(anno_padre, ("%02d - %s" % (mes, utils.MESES[mes]), 
                                          utils.float2str(por_fecha[anno][mes]),
                                          ""))
        vpro.ocultar()
        
    def set_inicio(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
#        self.inicio = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])
        self.inicio = mx.DateTime.DateTimeFrom(year = int(temp[2]), month = int(temp[1]), day = (temp[0]))


    def set_fin(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
#        self.fin = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])
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
        """
        Dadas fecha de inicio y de fin, devuelve todos los vencimientos 
        no pagados al completo.
        """
        if not self.inicio:
            vencimientos = pclases.VencimientoPago.select(
                            pclases.VencimientoPago.q.fecha <= self.fin, 
                            orderBy = 'fecha')
            #estimados = pclases.EstimacionPago.select(
            #                pclases.EstimacionPago.q.fecha <= self.fin, 
            #                orderBy = 'fecha')
        else:
            vencimientos = pclases.VencimientoPago.select(pclases.AND(
                                pclases.VencimientoPago.q.fecha >= self.inicio,
                                pclases.VencimientoPago.q.fecha <= self.fin), 
                            orderBy='fecha') 
            #estimados = pclases.EstimacionPago.select(pclases.AND(
            #                    pclases.EstimacionPago.q.fecha >= self.inicio,
            #                    pclases.EstimacionPago.q.fecha <= self.fin), 
            #                orderBy='fecha')

        idproveedor = utils.combo_get_value(self.wids['cmbe_proveedor'])
        if idproveedor is not None:
            proveedor = pclases.Proveedor.get(idproveedor)
            # Los estimados ya no se usan. No me molesto en vpro para ellos.
            #estimados = [e for e in estimados 
            #             if e.facturaCompra.proveedorID == proveedor.id]
        else:
            proveedor = None
        mostrar_solo_pendientes = self.wids['ch_pendientes'].get_active()
        self.resultado = []
        tot = vencimientos.count()
        ivpro = 0.0
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        for i in vencimientos:
            vpro.set_valor(ivpro/tot, "Buscando vencimientos...")
            ivpro += 1
            if proveedor:
                if v.facturacCompra.proveedor != proveedor:
                    continue    # Lo ignoro.
            if not self.esta_pagado(i):
                if ((mostrar_solo_pendientes and self.pagare_y_no_emitido(i)) 
                    or not mostrar_solo_pendientes):
                    self.resultado.append([i.fecha, i, False])
        vpro.ocultar()
        if idproveedor is None:     
            # Porque en Logic los proveedores no son los mismos que 
            # aquí (no están exactamente igual escritos)
            vencimientos_logic = self.buscar_vencimientos_logic(self.inicio, 
                                                                self.fin)
            for i in vencimientos_logic:
                self.resultado.append([i['fecha'], i, True])
        self.resultado = self.filtrar_por_forma_de_pago(self.resultado)
        self.resultado.sort(self.por_fecha)
        self.rellenar_tabla(self.resultado)

    def filtrar_por_forma_de_pago(self, r):
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        i = 0.0
        tot = len(r)
        vpro.set_valor(i / tot, "Filtrando por forma de pago...")
        if self.wids['ch_formapago'].get_active():
            res = []
            formapago = utils.combo_get_value(self.wids['cb_formapago'])
            if formapago != None:
                txtformapago = self.formaspago[formapago][1]
                for v in r: # v es una tupla con fecha, vencimiento o 
                    vpro.set_valor(i / tot, "Filtrando por forma de pago...")
                    # estimación y un boolean para indicar si es de LOGIC.
                    # Las formas de pago en el combo están todas en minúsuclas
                    # y sin tildes:
                    if (not v[2]
                        and txtformapago in utils.filtrar_tildes(
                            v[1].observaciones).lower()):
                        res.append(v)
                    i += 1
        else:
            res = r
        vpro.ocultar()
        return res

    def buscar_vencimientos_logic(self, fechaini, fechafin):
        """
        Devuelve una lista de diccionarios que contiene posibles vencimientos
        obtenidos de la tabla de movimientos de Logic.
        En la tabla se buscarán los apuntes que contengan "Vto" y una fecha a
        continuación, que no estén ya relacionados con ningún pago y que en 
        el propio Logic no se haya saldado ya.
        Cada uno de las tuplas encontradas se devuelve como un diccionario
        que contiene fecha de vencimiento, importe, comentario, cuenta e id.
        """
        Logic = pclases.LogicMovimientos
        ls = Logic.select(pclases.AND(Logic.q.contrapartidaInfo == '',
                                      pclases.OR(Logic.q.comentario.contains('Vto'),
                                                 Logic.q.comentario.contains('VTO'),
                                                 Logic.q.comentario.contains('vto')), 
                                      pclases.NOT(Logic.q.comentario.contains("N/Fra"))))
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
        como vencimiento, no se ha usado en ningún pago ya y ésta 
        está dentro de los criterios.
        """
        fechavto = self.get_fecha_vto_logic(tuplalogic) 
        if fechaini:
            res = (fechavto 
                   and fechavto >= fechaini 
                   and fechavto <= fechafin 
                   and tuplalogic.pagos == [])
        else:
            res = (fechavto 
                   and fechavto <= fechafin 
                   and tuplalogic.pagos == [])
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
                        # Intento fecha corta (dd/mm/aa)
                        fechafra = time.strptime(fechafra[0], '%d/%m/%y')   
                    except ValueError:
                        try:
                            # Debe estar en formato dd/mm/aaaa
                            fechafra = time.strptime(fechafra[0], '%d/%m/%Y')  
                        except:
                            print s[:pivote], fechafra
                    anno = fechafra[0]  # strptime devuelve tupla con el 
                                        # año en la primera posición.
                    dia, mes = fechavto[0].split('/')
                    res = mx.DateTime.DateTimeFrom(day = int(dia), month = int(mes), year = int(anno))
        return res

    def pagare_y_no_emitido(self, vto):
        """
        Devuelve True si la forma de pago del vencimiento es 
        pagaré o cheque y éste no se ha creado aún.
        """
        forma_pago_cheque_o_pagare = lambda obs: obs != None and ("pagar" in obs.lower() or "cheque" in obs.lower() or "tal" in obs.lower())
        def pagare_o_cheque_emitido(vto):
            """
            Devuelve True si el vencimiento tiene una factura que 
            tiene un cobro relacionado indirectamente con el vencimiento 
            y está asociado a un pagarePago.
            """
            fra = vto.facturaCompra
            vtos_pagos = fra.emparejar_vencimientos()
            tiene_pago = len(vtos_pagos[vto]) > 0
            res = tiene_pago and vtos_pagos[vto][0].pagarePago != None
            return res
        return (forma_pago_cheque_o_pagare(vto.observaciones) 
                and not pagare_o_cheque_emitido(vto))

    def esta_pagado(self, vencimiento):
        """
        Devuelve True si el vencimiento está pagado COMPLETAMENTE.
        Los pagos siempre anulan vencimientos cronológicamente (es decir, no 
        puede quedar un vencimiento pendiente antes que otro pagado con 
        fecha posterior).
        Gráficamente:
                 Vencimiento    Pago (por orden cronológico)
        01/01/08      1          1
        01/02/08      2          1
        01/03/08      1
        Total fra:    4          2   Total pagado
        Pendiente de pago: 1
        Vencimientos pendientes: 01/02 (parcialmente) y 01/03 (completo)
        """
        pagado = round(vencimiento.calcular_importe_pdte(), 2) == 0
        return pagado
        #fra = vencimiento.facturaCompra
        ##pagos = fra.pagos
        #cant_pagada = sum([p.importe for p in fra.pagos])
        #vencimientos_pendientes = fra.vencimientosPago[:]
        #vencimientos_pendientes.sort(self.cmp_fechas)
        #while cant_pagada > 0 and vencimientos_pendientes:
        #    v = vencimientos_pendientes.pop(0)
        #    if cant_pagada < v.importe:
        #        # Si no cubre al vencimiento lo devuelvo a la lista de pdtes.
        #        vencimientos_pendientes.insert(0, v)
        #    cant_pagada -= v.importe
        #res = vencimiento not in vencimientos_pendientes
        #return res
        # Los vencimientos pagados están en las posiciones 0:|pagos|. Es decir, 
        # si hay dos pagos, los vencimientos pagados serán el 0 y el 1 (a no 
        # ser que los vencimientos no se paguen por orden cronológico, que eso 
        # ya sería rizar el rizo.
        #return vencimiento in vencimientos[:len(pagos)]

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
        from formularios import reports
        datos = []
        for i in self.resultado:
            if not i[2]:    # i[2] = False cuando es vencimiento normal de la BD
                datos.append((i[1].facturaCompra.numfactura,
                              utils.str_fecha(i[1].fecha),
                              utils.float2str(i[1].importe),
                              i[1].observaciones,
                              i[1].facturaCompra.proveedor.nombre))
            else:   # i[2] = True. Es un vencimiento rescatado de LogicMovimientos.
                datos.append(("LOGIC",      # Esto me va a valer para diferenciar un vto. de la BD de uno de Logic.
                              utils.str_fecha(i[1]['fecha']),
                              utils.float2str(i[1]['importe']),
                              i[1]['comentario'],
                              i[1]['cuenta']))
        if not self.inicio:            
            fechaInforme = 'Hasta '+utils.str_fecha(self.fin)
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
            reports.abrir_pdf(geninformes.vencimientosPago(datos,fechaInforme))

    def exportar(self, boton):
        """
        Vuelva el contenido de todos los TreeViews en un solo ".csv".
        """
        tv = self.wids['tv_datos']
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        nomarchivocsv = treeview2csv(tv)
        abrir_csv(nomarchivocsv)
        nomarchivocsv = treeview2csv(self.wids['tv_totales'])
        abrir_csv(nomarchivocsv)


def filtrar_tildes_lista(lista):
    """
    Devuelve una lista con los elementos de la recibida 
    en los cuales se han sustituido las tildes por vocales
    sin tildar.
    """
    res = []
    for e in lista:
        res.append(utils.filtrar_tildes(e))
    return res

if __name__ == '__main__':
    t = ConsultaVencimientosPagos()    

