#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2013  Francisco José Rodríguez Bogado,                   #
#                          <frbogado@geotexan.com>                            #
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
## consulta_ofertas.py -- 
###################################################################
## NOTAS:
##  
###################################################################
## TODO:
## * ¿Filtro para que solo se puedan ver las ofertas del usuario 
##   que ha abierto la ventana?
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk, time
from framework import pclases
import mx.DateTime
from informes import geninformes
import pango 
from lib import charting
from collections import defaultdict


class ConsultaOfertas(Ventana):
        
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'consulta_ofertas.glade', objeto, self.usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       'b_exportar/clicked': self.exportar, 
                       'notebook1/switch-page': self.cambiar_grafica}
        self.add_connections(connections)
        cols = (('Número',    'gobject.TYPE_STRING', False, True, True, None),
                ('Fecha',     'gobject.TYPE_STRING', False, True, False, None),
                ('Cliente',   'gobject.TYPE_STRING', False, True, False, None),
                ('Obra',      'gobject.TYPE_STRING', False, True, False, None),
                ('Comercial', 'gobject.TYPE_STRING', False, True, False, None),
                #('Tipo',      'gobject.TYPE_STRING', False, True, False, None),
                # CWT: Solo ofertas de pedido. Nada de estudio.
                ('Adjudicada','gobject.TYPE_BOOLEAN', False, True, False, None),
                ('Estado',    'gobject.TYPE_STRING', False, True, False, None),
                ('Contacto',  'gobject.TYPE_STRING', False, True, False, None),
                ('Pedido',    'gobject.TYPE_STRING', False, True, False, None),
                ('Importe',   'gobject.TYPE_STRING', False, True, False, None),
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
        tv = self.wids['tv_datos']
        utils.preparar_listview(tv, cols)
        tv.connect("row-activated", self.abrir_objeto)
        tv.get_column(9).get_cell_renderers()[0].set_property('xalign', 1) 
        self.colorear(tv)
        cols = (('Producto', 'gobject.TYPE_STRING', False, True, True, None),
                ('Ofertado', 'gobject.TYPE_STRING', False, True, False, None),
                ('Pedido',   'gobject.TYPE_STRING', False, True, False, None), 
                ('PUID',     'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_producto'], cols)
        getcoltvpro = self.wids['tv_producto'].get_column
        getcoltvpro(1).get_cell_renderers()[0].set_property('xalign', 1) 
        getcoltvpro(2).get_cell_renderers()[0].set_property('xalign', 1) 
        cols = (('Cliente', 'gobject.TYPE_STRING', False, True, True, None),
                ('CIF',     'gobject.TYPE_STRING', False, True, False, None),
                ('Importe', 'gobject.TYPE_STRING', False, True, False, None),
                ('Forma de cobro', 
                            'gobject.TYPE_STRING', False, True, False, None),
                ('PUID',    'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_cliente'], cols)
        cell = self.wids['tv_cliente'].get_column(2).get_cell_renderers()[0]
        cell.set_property('xalign', 1) 
        self.wids['tv_cliente'].connect("row-activated", self.abrir_objeto)
        self.inicio = mx.DateTime.DateTimeFrom(day = 1, 
                                        month = mx.DateTime.localtime().month, 
                                        year = mx.DateTime.localtime().year)
        self.wids['e_fechainicio'].set_text(utils.str_fecha(self.inicio))
        self.fin = time.localtime()
        self.wids['e_fechafin'].set_text(utils.str_fecha(self.fin))
        opciones = [(c.id, c.nombre) 
                    for c in pclases.Cliente.select(orderBy = "nombre")]
        opciones.insert(0, (-1, "Todos"))
        utils.rellenar_lista(self.wids['cbe_cliente'], opciones)
        utils.combo_set_from_db(self.wids['cbe_cliente'], -1)
        opciones = [(c.id, c.get_nombre_completo()) 
                    for c in pclases.Comercial.select()
                    if c.empleado and c.empleado.activo]
        opciones.sort(key = lambda c: c[1])
        opciones.insert(0, (-1, "Todos"))
        utils.rellenar_lista(self.wids['cbe_comercial'], opciones)
        utils.combo_set_from_db(self.wids['cbe_comercial'], -1)
        cols = (('Comercial', 'gobject.TYPE_STRING', False, True, True, None),
                ('Cliente',   'gobject.TYPE_STRING', False, True, False, None),
                ('Forma de pago', 
                              'gobject.TYPE_STRING', False, True, False, None),
                ('Importe',   'gobject.TYPE_STRING', False, True, False, None),
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_comercial'], cols)
        tv = self.wids['tv_comercial']
        tv.get_column(3).get_cell_renderers()[0].set_property('xalign', 1) 
        tv.connect("row-activated", self.abrir_objeto)
        cols = (('Provincia', 'gobject.TYPE_STRING', False, True, True, None),
                ('Comercial', 'gobject.TYPE_STRING', False, True, False, None),
                ('Cliente',   'gobject.TYPE_STRING', False, True, False, None),
                ('Forma de pago', 
                              'gobject.TYPE_STRING', False, True, False, None),
                ('Importe',   'gobject.TYPE_STRING', False, True, False, None),
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_provincia'], cols)
        tv = self.wids['tv_provincia']
        tv.get_column(4).get_cell_renderers()[0].set_property('xalign', 1) 
        tv.connect("row-activated", self.abrir_objeto)
        self.wids['ventana'].set_title("Consulta de ofertas de pedido")
        self.por_oferta = {} # defaultdict(lambda: [])
        self.por_producto = defaultdict(lambda: [])
        self.por_cliente = defaultdict(lambda: [])
        self.por_comercial = defaultdict(lambda: [])
        self.por_provincia = defaultdict(lambda: [])
        gtk.main()
    
    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        if self.wids['notebook1'].get_current_page() == 0:
            tv = self.wids['tv_datos']
        elif self.wids['notebook1'].get_current_page() == 1:
            tv = self.wids['tv_cliente']
        elif self.wids['notebook1'].get_current_page() == 2:
            tv = self.wids['tv_producto']
        elif self.wids['notebook1'].get_current_page() == 3:
            tv = self.wids['tv_comercial']
        elif self.wids['notebook1'].get_current_page() == 4:
            tv = self.wids['tv_provincia']
        else:
            return
        abrir_csv(treeview2csv(tv))

    def colorear(self, tv):
        def cell_func(column, cell, model, itr, i):
            try:
                presupuesto = pclases.getObjetoPUID(model[itr][-1])
            except (AttributeError, pclases.SQLObjectNotFound):
                color = None
            else:
                if presupuesto.rechazado: 
                    color = "Indian Red"
                elif presupuesto.get_pedidos(): # FIXME: Esto es muy lento.
                    color = "light green"
                elif presupuesto.validado:
                    color = "light yellow"
                else:
                    color = None
            cell.set_property("cell-background", color)
        cols = tv.get_columns()
        for i in xrange(len(cols)):
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell, cell_func, i)

    def abrir_objeto(self, tv, path, view_column):
        """
        Abre el presupuesto, producto o cliente según corresponda.
        """
        model = tv.get_model()
        puid = model[path][-1]
        objeto = pclases.getObjectPUID(puid)
        if isinstance(objeto, pclases.Cliente):
            from formularios.clientes import Clientes as NuevaVentana
        elif isinstance(objeto, pclases.Presupuesto):
            from formularios.presupuestos import Presupuestos as NuevaVentana
        elif isinstance(objeto, pclases.ProductoVenta):
            if objeto.es_rollo():
                from formularios.productos_de_venta_rollos \
                        import ProductosDeVentaRollos as NuevaVentana
            elif objeto.es_fibra():
                from formularios.productos_de_venta_balas \
                        import ProductosDeVentaBalas as NuevaVentana
            else:
                # PLAN: Y ya iré contemplando más casos si van haciendo falta.
                return
        elif isinstance(objeto, pclases.ProductoCompra):
            from formularios.productos_compra \
                    import ProductosCompra as NuevaVentana
        elif isinstance(objeto, pclaes.PedidoVenta):
            from formularios.pedidos_de_venta \
                    import PedidosDeVenta as NuevaVentana
        elif isinstance(objeto, pclases.LineaDePresupuesto):
            objeto = objeto.presupuesto
            from formularios.presupuestos import Presupuestos as NuevaVentana
        else:
            return  # Si no es nada de lo que pueda abrir, pasando del temita.
        v = NuevaVentana(usuario = self.usuario, objeto = objeto)
    
    def chequear_cambios(self):
        pass

    def set_inicio(self, boton):
        temp = utils.mostrar_calendario(titulo = "SELECCIONE FECHA DE INICIO", 
                padre = self.wids['ventana'], 
                fecha_defecto = self.inicio)
        self.inicio = mx.DateTime.DateFrom(*temp[::-1])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(self.inicio))

    def set_fin(self, boton):
        temp = utils.mostrar_calendario(titulo = "SELECCIONE FECHA DE FIN", 
                padre = self.wids['ventana'], 
                fecha_defecto = self.fin)
        self.fin = mx.DateTime.DateFrom(*temp[::-1])
        self.wids['e_fechafin'].set_text(utils.str_fecha(self.fin))

    def buscar(self, boton):
        """
        Dadas fecha de inicio y de fin, busca todas las ofertas 
        (de pedido) entre esas dos fechas.
        """
        total_ofertas = 0.0
        total_pedidos = 0.0
        ratio = None
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        if pclases.DEBUG:
            print "self.inicio", self.inicio, "self.fin", self.fin
        vpro.set_valor(0.0, "Buscando ofertas de pedido...")
        criterios = [pclases.Presupuesto.q.estudio == False]
        idcliente = utils.combo_get_value(self.wids['cbe_cliente'])
        if idcliente != -1:
            criterios.append(pclases.Presupuesto.q.clienteID == idcliente)
        idcomercial = utils.combo_get_value(self.wids['cbe_comercial'])
        if idcomercial != -1:
            criterios.append(pclases.Presupuesto.q.comercialID == idcomercial)
        if self.inicio:
            criterios.append(pclases.Presupuesto.q.fecha >= self.inicio)
        if self.fin:
            criterios.append(pclases.Presupuesto.q.fecha <= self.fin)
        if not criterios:
            presupuestos = pclases.Presupuesto.select(orderBy = "id")
        elif len(criterios) == 1:
            presupuestos = pclases.Presupuesto.select(criterios[0], 
                                                      orderBy = "id")
        else:
            presupuestos = pclases.Presupuesto.select(pclases.AND(*criterios), 
                                                      orderBy = "id")
        tot = presupuestos.count()
        i = 0.0
        convertidos = 0
        for p in presupuestos:
            vpro.set_valor(i/tot, "Clasificando ofertas de pedido...")
            if p in self.por_oferta and pclases.DEBUG:
                txt = "consulta_ofertas.py::buscar -> "\
                      "El presupuesto %s aparece dos veces en la consulta." % (
                              p.puid)
                try:
                    sys.stdout.write(txt + "\n")
                except:
                    self.logger.warning(txt)
            self.por_oferta[p] = p
            for ldp in p.lineasDePresupuesto:
                self.por_producto[ldp.producto].append(ldp)
            self.por_cliente[p.cliente].append(p)
            self.por_comercial[p.comercial].append(p)
            self.por_provincia[p.provincia].append(p)
            importe_total = p.calcular_importe_total()
            total_ofertas += importe_total
            if p.get_pedidos():
                total_pedidos += importe_total
                convertidos += 1
            i += 1
        try:
            ratio = 100.0 * convertidos / tot
        except ZeroDivisionError:
            ratio = None
        self.rellenar_tabla_por_oferta(vpro)
        self.rellenar_tabla_por_producto(vpro)
        self.rellenar_tabla_por_cliente(vpro)
        self.rellenar_tabla_por_comercial(vpro)
        self.rellenar_tabla_por_provincia(vpro)
        vpro.ocultar()
        self.wids['e_total_ofertas'].set_text("%s €" % (
            utils.float2str(total_ofertas)))
        self.wids['e_total_pedidos'].set_text("%s €" % (
            utils.float2str(total_pedidos)))
        self.wids['e_ratio'].set_text("%s %%" % (ratio != None 
            and utils.float2str(ratio, precision = 2) or "-"))

    def rellenar_tabla_por_oferta(self, vpro):
        """
        Rellena el model de la lista de ofertas. Recibe la ventana de progreso.
        """ 
        model = self.wids['tv_datos'].get_model()
        model.clear()
        tot = len(self.por_oferta.keys())
        i = 0.0
        vpro.set_valor(i/tot, "Mostrando listado de ofertas...")
        self.pedidos_generados = []
        for p in self.por_oferta:
            vpro.set_valor(i/tot, "Mostrando listado de ofertas... (%d)" % p.id)
            presupuesto = self.por_oferta[p]  # Él mismo en la práctica.
            pedidos = presupuesto.get_pedidos()
            fila = (str(presupuesto.id), 
                    utils.str_fecha(presupuesto.fecha), 
                    presupuesto.cliente and presupuesto.cliente.nombre 
                        or presupuesto.nombrecliente, 
                    presupuesto.obra and presupuesto.obra.nombre 
                        or presupuesto.nombreobra, 
                    presupuesto.comercial 
                        and presupuesto.comercial.get_nombre_completo()
                        or "Sin comercial relacionado", 
                    presupuesto.adjudicada, 
                    presupuesto.get_str_estado(), 
                    presupuesto.personaContacto, 
                    ", ".join([pedido.numpedido for pedido in pedidos]), 
                    utils.float2str(presupuesto.calcular_importe_total()), 
                    presupuesto.puid)
            self.pedidos_generados += [ped for ped in pedidos 
                                       if ped not in self.pedidos_generados]
            model.append(fila)
            i += 1
        # Y ahora la gráfica.
        if self.wids['notebook1'].get_current_page() == 0:
            self.graficar_por_oferta()
    
    def graficar_por_oferta(self):
        datachart = []  # Cada fila: Descripción, cantidad, color (7 = gris
                        #                                          0 = amarillo
                        #                                          3 = verde)
        datachart = [["Ofertas", len(self.por_oferta), 0], 
                     ["Pedidos", len(self.pedidos_generados), 3]]
        try:
            oldchart = self.wids['eventbox_chart'].get_child()
            if oldchart != None:
                #self.wids['eventbox_chart'].remove(oldchart)
                chart = oldchart
            else:
                chart = charting.Chart(orient = "horizontal", 
                                       values_on_bars = True)
                self.wids['eventbox_chart'].add(chart)
            datachart.sort(lambda fila1, fila2: (fila1[0] < fila2[0] and -1) 
                                                 or (fila1[0] > fila2[0] and 1)
                                                 or 0)
            chart.plot(datachart)
            self.wids['eventbox_chart'].show_all()
        except Exception, msg:
            txt = "consulta_ofertas.py::graficar_por_oferta -> "\
                  "Error al dibujar gráfica (charting): %s" % msg
            print txt
            self.logger.error(txt)

    def rellenar_tabla_por_producto(self, vpro):
        """
        Rellena el model de la lista de ofertas. Recibe la ventana de progreso.
        """ 
        model = self.wids['tv_producto'].get_model()
        model.clear()
        tot = sum([len(self.por_producto[k]) 
                   for k in self.por_producto.keys()])
        i = 0.0
        vpro.set_valor(i/tot, "Mostrando ofertas por producto...")
        padres = {}
        for producto in self.por_producto:
            for ldp in self.por_producto[producto]: # ldp=linea_de_presupuesto
                vpro.set_valor(i/tot, "Mostrando ofertas por producto... (%d)" 
                                                        % ldp.presupuesto.id)
                try:
                    padre = padres[producto]
                except KeyError:
                    try:
                        nombre_producto = producto.descripcion
                        puid = producto.puid
                    except AttributeError:
                        nombre_producto = producto or ""
                        puid = None
                    padre = padres[producto] = model.append(None, 
                            (nombre_producto, "0.0", "0.0", puid))
                ofertado = ldp.cantidad
                try:
                    # FIXME: Si dos ofertas se han pasado al mismo pedido 
                    # entonces a dos líneas de presupuesto le corresponde la 
                    # misma línea de pedido. Por tanto la cantidad pedida se 
                    # duplicará. ¿Es así?
                    pedido=ldp.presupuesto.get_pedido_por_producto()[producto]
                except KeyError:
                    pedido = 0.0
                fila = ("Presupuesto %d" % ldp.presupuesto.id, 
                        utils.float2str(ofertado), 
                        utils.float2str(pedido), 
                        ldp.puid)
                model.append(padre, fila)
                # Actualizo totales fila padre.
                model[padre][1] = utils.float2str(
                        utils._float(model[padre][1]) + ofertado)
                model[padre][2] = utils.float2str(
                        utils._float(model[padre][2]) + pedido)
                i += 1
        # Y ahora la gráfica.
        if self.wids['notebook1'].get_current_page() == 1:
            self.graficar_por_producto()

    def graficar_por_producto(self):
        datachart = []
        model = self.wids['tv_producto'].get_model()
        try:
            maximo_producto = max([utils._float(f[1]) for f in model])
        except ValueError:  # empty sequence
            maximo_producto = 0
        for fila in model:
            if utils._float(fila[1]) == maximo_producto:
                color = 0
            if (fila[-1] == None or isinstance(pclases.getObjetoPUID(fila[-1]),
                                               pclases.Servicio)):
                    # Productos que no están dados de alta, no 
                    # tengo el puid de producto o es servicio.
                color = 7
            else:
                color = 3
            nombre_corto = fila[0].replace("GEOTESAN", "")  # OJO: HARCODED
            datachart.append([nombre_corto, utils._float(fila[1]), color])
        # Filtro y me quedo con el TOP5:
        datachart.sort(lambda c1, c2: int(c2[1] - c1[1]))
        _datachart = datachart[:5]
        _datachart.append(("Resto", sum([c[1] for c in datachart[5:]])))
        datachart = _datachart
        try:
            oldchart = self.wids['eventbox_chart'].get_child()
            if oldchart != None:
                self.wids['eventbox_chart'].remove(oldchart)
                #chart = oldchart
            #else:
            chart = charting.Chart(orient = "vertical", 
                                       values_on_bars = True)
            self.wids['eventbox_chart'].add(chart)
            chart.plot(datachart)
            self.wids['eventbox_chart'].show_all()
        except Exception, msg:
            txt = "consulta_ofertas.py::graficar_por_producto -> "\
                  "Error al dibujar gráfica (charting): %s" % msg
            print txt
            self.logger.error(txt)

    def rellenar_tabla_por_cliente(self, vpro):
        """
        Rellena el model de la lista de ofertas clasificada por cliente. 
        Recibe la ventana de progreso.
        """ 
        model = self.wids['tv_cliente'].get_model()
        model.clear()
        tot = sum([len(self.por_producto[k]) 
                   for k in self.por_producto.keys()])
        i = 0.0
        vpro.set_valor(i/tot, "Mostrando ofertas por cliente...")
        padres = {}
        for cliente in self.por_cliente:
            for presupuesto in self.por_cliente[cliente]: 
                vpro.set_valor(i/tot, "Mostrando ofertas por cliente... (%d)" 
                                                        % presupuesto.id)
                try:
                    padre = padres[cliente]
                except KeyError:
                    try:
                        nombre_cliente = cliente.descripcion
                        cif = cliente.cif
                        puid = cliente.puid
                    except AttributeError:
                        nombre_cliente = presupuesto.nombrecliente 
                        cif = presupuesto.cif
                        puid = None
                    padre = padres[cliente] = model.append(None, 
                            (nombre_cliente, 
                             cif, 
                             "0.0", 
                             "", 
                             puid))
                importe = presupuesto.calcular_importe_total()
                fila = ("Presupuesto %d" % presupuesto.id, 
                        utils.str_fecha(presupuesto.fecha),
                        utils.float2str(importe), 
                        presupuesto.formaDePago 
                            and presupuesto.formaDePago.toString() or "", 
                        presupuesto.puid)
                model.append(padre, fila)
                # Actualizo totales fila padre.
                model[padre][2] = utils.float2str(
                        utils._float(model[padre][2]) + importe)
                i += 1
        # Y ahora la gráfica.
        if self.wids['notebook1'].get_current_page() == 2:
            self.graficar_por_cliente()

    def graficar_por_cliente(self):
        datachart = []
        model = self.wids['tv_cliente'].get_model()
        try:
            maximo_cliente = max([utils._float(f[2]) 
                                  for f in model]) # if f[0]!="Sin cliente"])
        except ValueError:  # empty sequence
            maximo_cliente = 0
        for fila in model:
            if fila[0] == None:     # Cliente no dado de alta. No tiene PUID.
                color = 7
            elif utils._float(fila[2]) == maximo_cliente:
                color = 0
            else:
                color = 3
            datachart.append([fila[0], utils._float(fila[2]), color])
        # Filtro y me quedo con el TOP5:
        datachart.sort(lambda c1, c2: int(c2[1] - c1[1]))
        _datachart = datachart[:5]
        _datachart.append(("Resto", sum([c[1] for c in datachart[5:]])))
        datachart = _datachart
        try:
            oldchart = self.wids['eventbox_chart'].get_child()
            if oldchart != None:
                self.wids['eventbox_chart'].remove(oldchart)
                #chart = oldchart
            #else:
            chart = charting.Chart(orient = "horizontal", 
                                       values_on_bars = True)
            self.wids['eventbox_chart'].add(chart)
            chart.plot(datachart)
            self.wids['eventbox_chart'].show_all()
        except Exception, msg:
            txt = "consulta_ofertas.py::graficar_por_cliente -> "\
                  "Error al dibujar gráfica (charting): %s" % msg
            print txt
            self.logger.error(txt)

    def rellenar_tabla_por_comercial(self, vpro):
        """
        Rellena el model de la lista de ofertas clasificada por comercial. 
        Recibe la ventana de progreso.
        """ 
        model = self.wids['tv_comercial'].get_model()
        model.clear()
        tot = sum([len(self.por_producto[k]) 
                   for k in self.por_producto.keys()])
        i = 0.0
        vpro.set_valor(i/tot, "Mostrando ofertas por comercial...")
        padres = {}
        for comercial in self.por_comercial:
            for presupuesto in self.por_comercial[comercial]: 
                vpro.set_valor(i/tot, "Mostrando ofertas por comercial... (%d)" 
                                                        % presupuesto.id)
                try:
                    padre = padres[comercial]
                except KeyError:
                    try:
                        nombre_comercial = comercial.get_nombre_completo()
                        puid = comercial.puid
                    except AttributeError:
                        nombre_comercial = "Sin comercial relacionado"
                        puid = None
                    padre = padres[comercial] = model.append(None, 
                            (nombre_comercial, 
                             "", 
                             "", 
                             "0.0", 
                             puid))
                importe = presupuesto.calcular_importe_total()
                fila = ("Presupuesto %d" % presupuesto.id, 
                        presupuesto.cliente and presupuesto.cliente.nombre 
                            or presupuesto.nombrecliente,
                        presupuesto.formaDePago 
                            and presupuesto.formaDePago.toString() or "", 
                        utils.float2str(importe), 
                        presupuesto.puid)
                model.append(padre, fila)
                # Actualizo totales fila padre.
                model[padre][3] = utils.float2str(
                        utils._float(model[padre][3]) + importe)
                i += 1
        # Y ahora la gráfica.
        if self.wids['notebook1'].get_current_page() == 3:
            self.graficar_por_comercial()

    def graficar_por_comercial(self):
        datachart = []
        model = self.wids['tv_comercial'].get_model()
        try:
            maximo_comercial = max([utils._float(f[3]) for f in model 
                                    if f[0]!="Sin comercial relacionado"])
        except ValueError:  # empty sequence
            maximo_comercial = 0
        for fila in model:
            if fila[0] == None:     # Cliente no dado de alta. No tiene PUID.
                color = 7
            elif utils._float(fila[3]) == maximo_comercial:
                color = 0
            else:
                color = 3
            datachart.append([fila[0], utils._float(fila[3]), color])
        datachart.sort(lambda c1, c2: int(c2[1] - c1[1]))
        #_datachart = datachart[:5]
        #_datachart.append(("Resto", sum([c[1] for c in datachart[5:]])))
        #datachart = _datachart
        try:
            oldchart = self.wids['eventbox_chart'].get_child()
            if oldchart != None:
                self.wids['eventbox_chart'].remove(oldchart)
                #chart = oldchart
            #else:
            chart = charting.Chart(orient = "horizontal", 
                                   values_on_bars = True)
            self.wids['eventbox_chart'].add(chart)
            chart.plot(datachart)
            self.wids['eventbox_chart'].show_all()
        except Exception, msg:
            txt = "consulta_ofertas.py::graficar_por_comercial -> "\
                  "Error al dibujar gráfica (charting): %s" % msg
            print txt
            self.logger.error(txt)

    def rellenar_tabla_por_provincia(self, vpro):
        """
        Rellena el model de la lista de ofertas clasificada por comercial. 
        Recibe la ventana de progreso.
        """ 
        model = self.wids['tv_provincia'].get_model()
        model.clear()
        tot = sum([len(self.por_producto[k]) 
                   for k in self.por_producto.keys()])
        i = 0.0
        vpro.set_valor(i/tot, "Mostrando ofertas por provincia...")
        padres = {}
        for provincia in self.por_provincia:
            for presupuesto in self.por_provincia[provincia]: 
                vpro.set_valor(i/tot, "Mostrando ofertas por provincia... (%d)" 
                                                        % presupuesto.id)
                try:
                    padre = padres[provincia]
                except KeyError:
                    padre = padres[provincia] = model.append(None, 
                            (provincia, 
                             "", 
                             "", 
                             "", 
                             "0.0", 
                             None))
                importe = presupuesto.calcular_importe_total()
                try:
                    comercial = presupuesto.comercial
                    nombre_comercial = comercial.get_nombre_completo()
                except AttributeError:
                    nombre_comercial = "Sin comercial relacionado"
                fila = ("Presupuesto %d" % presupuesto.id, 
                        nombre_comercial, 
                        presupuesto.cliente and presupuesto.cliente.nombre 
                            or presupuesto.nombrecliente,
                        presupuesto.formaDePago 
                            and presupuesto.formaDePago.toString() or "", 
                        utils.float2str(importe), 
                        presupuesto.puid)
                model.append(padre, fila)
                # Actualizo totales fila padre.
                model[padre][4] = utils.float2str(
                        utils._float(model[padre][4]) + importe)
                if nombre_comercial not in model[padre][1]:
                    if not model[padre][1]:
                        model[padre][1] = nombre_comercial
                    else:
                        model[padre][1] += ", " + nombre_comercial
                i += 1
        # Y ahora la gráfica.
        if self.wids['notebook1'].get_current_page() == 4:
            self.graficar_por_provincia()

    def graficar_por_provincia(self):
        datachart = []
        model = self.wids['tv_provincia'].get_model()
        try:
            maxima_provincia = max([utils._float(f[4]) for f in model]) 
        except ValueError:  # empty sequence
            maxima_provincia = 0
        for fila in model:
            if fila[0] == "No especificada" or fila[0].strip == "": 
                color = 7
            elif utils._float(fila[4]) == maxima_provincia:
                color = 0
            else:
                color = 3
            datachart.append([fila[0], utils._float(fila[4]), color])
        # Filtro y me quedo con el TOP5:
        datachart.sort(lambda c1, c2: int(c2[1] - c1[1]))
        _datachart = datachart[:5]
        _datachart.append(("Resto", sum([c[1] for c in datachart[5:]])))
        datachart = _datachart
        try:
            oldchart = self.wids['eventbox_chart'].get_child()
            if oldchart != None:
                self.wids['eventbox_chart'].remove(oldchart)
                #chart = oldchart
            #else:
            chart = charting.Chart(orient = "horizontal", 
                                       values_on_bars = True)
            self.wids['eventbox_chart'].add(chart)
            chart.plot(datachart)
            self.wids['eventbox_chart'].show_all()
        except Exception, msg:
            txt = "consulta_ofertas.py::graficar_por_provincia -> "\
                  "Error al dibujar gráfica (charting): %s" % msg
            print txt
            self.logger.error(txt)

    def cambiar_grafica(self, nb, page, page_num):
        if page_num == 0:
            self.graficar_por_oferta()
        elif page_num == 1:
            self.graficar_por_cliente()
        elif page_num == 2:
            self.graficar_por_producto()
        elif page_num == 3: 
            self.graficar_por_comercial()
        elif page_num == 4:
            self.graficar_por_provincia()
# PORASQUI

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        # TODO
        from formularios import reports
        datos = []
        model = self.wids['tv_datos'].get_model()
        for itr in model:
            datos.append((itr[0],  itr[1],  itr[2],  itr[3],  itr[4], 
                          itr[5],  itr[6],  itr[7],  itr[8],  itr[9], 
                          itr[10], itr[11], itr[12], itr[13]))
            hijos = itr.iterchildren()
            if hijos != None:
                for hijo in hijos:
                    datos.append((hijo[0], hijo[1], hijo[2], hijo[3], hijo[4], 
                                  hijo[5], hijo[6], hijo[7], hijo[8], hijo[9], 
                                  hijo[10], hijo[11], hijo[12], hijo[13]))
            datos.append(("---", "---", "---", "---", "---", "---", "---", 
                          "---", "---", "---", "---", "---", "---", "---"))
        datos.append(("", "", "", "", "", "", "", "", "", "", "", "", "", ""))
        if self.metros_totales != 0:
            metros_totales = "TOTAL m² de geotextiles: %s " % (
                                utils.float2str(self.metros_totales))
        else:
            metros_totales = ""
        if self.kilos_totales != 0:
            kilos_totales = "TOTAL kg de fibra: %s " % (
                                utils.float2str(self.kilos_totales))
        else:
            kilos_totales = ""
        total_importe = self.wids['e_total'].get_text()
        datos.append(("" , "IMPORTE TOTAL: %s " % (total_importe), 
                      "", "", "", "%s" % (metros_totales), "", "", 
                      "%s" % (kilos_totales), "", "", "", ""))
        if not self.inicio:            
            fechaInforme = 'Hasta ' + utils.str_fecha(
                                        time.strptime(self.fin, "%Y/%m/%d"))
        else:
            fechaInforme = (utils.str_fecha(
                time.strptime(self.inicio, "%Y/%m/%d")) + ' - ' 
                + utils.str_fecha(time.strptime(self.fin, "%Y/%m/%d")))
        if datos != []:
            reports.abrir_pdf(geninformes.ofertas(datos, fechaInforme))
        from informes.treeview2pdf import treeview2pdf
        if self.wids['notebook1'].get_current_page() == 0:
            self.wids['notebook1'].next_page()
            self.wids['notebook1'].realize()
            while gtk.events_pending(): gtk.main_iteration(False)
            self.wids['notebook1'].prev_page()
        reports.abrir_pdf(treeview2pdf(self.wids['tv_producto'], 
                                        titulo = "Ofertas por producto", 
                                        fecha = fechaInforme))
        reports.abrir_pdf(treeview2pdf(self.wids['tv_cliente'], 
                                        titulo = "Facturas por cliente", 
                                        fecha = fechaInforme))
        reports.abrir_pdf(treeview2pdf(self.wids['tv_comercial'], 
                                    titulo = "Ofertas facturadas por comercial",
                                    fecha = fechaInforme))
        reports.abrir_pdf(treeview2pdf(self.wids['tv_provincia'], 
                        titulo = "Ofertas facturadas según provincia de origen",
                        fecha = fechaInforme))



if __name__ == '__main__':
    t = ConsultaOfertas()

