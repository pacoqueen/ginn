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
## consulta_ofertas_estudio.py -- 
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

class ConsultaOfertasEstudio(Ventana):
        
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'consulta_ofertas_estudio.glade', 
                         objeto, self.usuario)
        # Son ofertas de estudio. Quito todo lo de pedidos.
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       'b_exportar/clicked': self.exportar, 
                       'notebook1/switch-page': self.cambiar_grafica}
        self.add_connections(connections)
        cols = (('Número',   'gobject.TYPE_STRING', False, True, True, None),#0
                ('Fecha',     'gobject.TYPE_STRING', False, True, False, None),
                ('Cliente',   'gobject.TYPE_STRING', False, True, False, None),
                ('Producto',  'gobject.TYPE_STRING', False, True, False, None),
                ('Cantidad',  'gobject.TYPE_STRING', False, True, False, None),
                ('Precio', 'gobject.TYPE_STRING', False, True, False, None), #5
                ('€/kg',  'gobject.TYPE_STRING', False, True, False, None),
                ('Obra',      'gobject.TYPE_STRING', False, True, False, None),
                ('Comercial', 'gobject.TYPE_STRING', False, True, False, None),
                ('Importe (s/IVA)',   
                              'gobject.TYPE_STRING', False, True, False, None),
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
        tv = self.wids['tv_datos']
        utils.preparar_listview(tv, cols)
        tv.connect("row-activated", self.abrir_objeto)
        tv.get_column(4).get_cell_renderers()[0].set_property('xalign', 1) 
        tv.get_column(5).get_cell_renderers()[0].set_property('xalign', 1) 
        tv.get_column(6).get_cell_renderers()[0].set_property('xalign', 1) 
        self.colorear(tv)
        cols = (('Producto', 'gobject.TYPE_STRING', False, True, True, None),
                ('Cantidad Ofertada', 
                             'gobject.TYPE_STRING', False, True, False, None),
                ('PUID',     'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_producto'], cols)
        getcoltvpro = self.wids['tv_producto'].get_column
        getcoltvpro(1).get_cell_renderers()[0].set_property('xalign', 1) 
        self.wids['tv_producto'].connect("row-activated", self.abrir_objeto)
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
        ### Combo clientes
        opciones = [(c.id, c.nombre) 
                    for c in pclases.Cliente.select(orderBy = "nombre")]
        opciones.insert(0, (-1, "Todos"))
        utils.rellenar_lista(self.wids['cbe_cliente'], opciones)
        utils.combo_set_from_db(self.wids['cbe_cliente'], -1)
        ### Combo comerciales
        comerciales_que_puedo_ver = [c for c 
                in pclases.Comercial.select(pclases.AND(
            pclases.Comercial.q.empleadoID == pclases.Empleado.q.id, 
            pclases.Empleado.q.usuarioID == pclases.Usuario.q.id, 
            pclases.Usuario.q.nivel > self.usuario.nivel))]
        for c in self.usuario.comerciales: # Los que están por debajo de mi 
                            # nivel (0 = máximo, 5 = mínimo) más y myself.
            comerciales_que_puedo_ver.append(c)
        opciones = [(c.id, c.get_nombre_completo()) 
                    for c in pclases.Comercial.select()
                    if c.empleado and c.empleado.activo 
                    and c in comerciales_que_puedo_ver]
        todos_los_comerciales = [c for c in 
                pclases.Comercial.select() if c.empleado.activo]
        opciones.sort(key = lambda c: c[1])
        if len(comerciales_que_puedo_ver) > 1:  # Con el esquema de permisos 
            # actual lo único que puedo hacer es asumir que si puede ver las 
            # ofertas de alguien más que no sea él mismo, entonces es que 
            # tiene permisos "de facto" para ver todas las ofertas.
            opciones.insert(0, (-1, "Todos"))
        utils.rellenar_lista(self.wids['cbe_comercial'], opciones)
        if -1 in [item[0] for item in self.wids['cbe_comercial'].get_model()]:
            utils.combo_set_from_db(self.wids['cbe_comercial'], -1)
        else:
            utils.combo_set_from_db(self.wids['cbe_comercial'], 
                    self.usuario.comerciales 
                        and self.usuario.comerciales[0].id or None)
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
        self.wids['ventana'].set_title("Consulta de ofertas de estudio")
        self.por_oferta = {} # defaultdict(lambda: [])
        self.por_producto = defaultdict(lambda: [])
        self.por_cliente = defaultdict(lambda: [])
        self.por_comercial = defaultdict(lambda: [])
        self.por_provincia = defaultdict(lambda: [])
        gtk.main()
    
    def colorear(self, tv):
        def cell_func(column, cell, model, itr, i):
            try:
                presupuesto = pclases.getObjetoPUID(model[itr][-1])
            except (AttributeError, pclases.SQLObjectNotFound):
                color = None
            else:
                if presupuesto.rechazado: 
                    color = "Indian Red"
                elif presupuesto.validado:
                    # En ofertas de estudio, básicamente es si el cliente 
                    # está dado de alta o no.
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
        objeto = pclases.getObjetoPUID(puid)
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
        (de estudio) entre esas dos fechas.
        """
        self.por_oferta = {} # defaultdict(lambda: [])
        self.por_producto = defaultdict(lambda: [])
        self.por_cliente = defaultdict(lambda: [])
        self.por_comercial = defaultdict(lambda: [])
        self.por_provincia = defaultdict(lambda: [])
        total_ofertas = 0.0
        total_ofertas_siva = 0.0
        ratio = None
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        if pclases.DEBUG:
            print "self.inicio", self.inicio, "self.fin", self.fin
        vpro.set_valor(0.0, "Buscando ofertas de estudio...")
        criterios = [pclases.Presupuesto.q.estudio == True]
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
        for p in presupuestos:
            vpro.set_valor(i/tot, "Clasificando ofertas de estudio...")
            if p in self.por_oferta and pclases.DEBUG:
                txt = "consulta_ofertas_estudio.py::buscar -> "\
                      "El presupuesto %s aparece dos veces en la consulta." % (
                              p.puid)
                try:
                    sys.stdout.write(txt + "\n")
                except:
                    self.logger.warning(txt)
            self.por_oferta[p] = p
            for ldp in p.lineasDePresupuesto:
                producto = ldp.producto or ldp.descripcion
                self.por_producto[producto].append(ldp)
            self.por_cliente[p.cliente].append(p)
            self.por_comercial[p.comercial].append(p)
            self.por_provincia[p.provincia.upper()].append(p)
            importe_total = p.calcular_importe_total()
            total_ofertas += importe_total
            importe_total_siva = p.calcular_importe_total(iva = False)
            total_ofertas_siva += importe_total_siva
            i += 1
        self.rellenar_tabla_por_oferta(vpro)
        self.rellenar_tabla_por_producto(vpro)
        self.rellenar_tabla_por_cliente(vpro)
        self.rellenar_tabla_por_comercial(vpro)
        self.rellenar_tabla_por_provincia(vpro)
        vpro.ocultar()
        self.wids['e_total_ofertas'].set_text("%s €" % (
            utils.float2str(total_ofertas)))
        self.wids['e_total_ofertas_siva'].set_text("%s €" % (
            utils.float2str(total_ofertas_siva)))
        self.wids['e_numero_ofertas'].set_text("%d" % (tot)) # assert i == tot

    def rellenar_tabla_por_oferta(self, vpro):
        """
        Rellena el model de la lista de ofertas. Recibe la ventana de progreso.
        """ 
        model = self.wids['tv_datos'].get_model()
        model.clear()
        tot = len(self.por_oferta.keys())
        i = 0.0
        try:
            vpro.set_valor(i/tot, "Mostrando listado de ofertas...")
        except ZeroDivisionError:
            return  # No hay ofertas que mostrar.
        presupuestos = self.por_oferta.keys()
        presupuestos.sort(key = lambda p: p.id, reverse = True)
        for p in presupuestos:
            vpro.set_valor(i/tot, "Mostrando listado de ofertas... (%d)" % p.id)
            presupuesto = self.por_oferta[p]  # Él mismo en la práctica.
            nombreobra = (presupuesto.obra and presupuesto.obra.nombre 
                          or presupuesto.nombreobra)
            #if len(nombreobra) > 33:
            #    nombreobra = nombreobra[:33] + "..."
            if len(nombreobra) > 80:
                nombreobra = utils.wrap(nombreobra, 80)
            nombre_comercial = (presupuesto.comercial 
                            and presupuesto.comercial.get_nombre_completo()
                            or "Sin comercial relacionado")
            estado = presupuesto.get_str_estado().replace("\n", " ")
            if presupuesto.validado:
                estado += " (%s)" % presupuesto.get_str_validacion()
            total_presupuesto = presupuesto.calcular_importe_total()
            for ldp in presupuesto.lineasDePresupuesto:
                if ldp.productoVenta:
                    #unidad = " " + ldp.productoVenta.unidad
                    nombre_producto = ldp.productoVenta.descripcion
                    try:
                        precio_kilo = utils.float2str(ldp.precioKilo)
                    except ValueError:  # No tiene
                        precio_kilo = "" 
                else:
                    #unidad = ""
                    nombre_producto = ldp.descripcion
                    precio_kilo = ""
                cantidad = utils.float2str(ldp.cantidad) 
                    #+ unidad Me jode poder operar si exporto a hoja de cálculo
                precio_unitario = utils.float2str(ldp.precio)
                fila = ("%d (%s € IVA incl.)" % (presupuesto.id, 
                            utils.float2str(total_presupuesto)), 
                        utils.str_fecha(presupuesto.fecha), 
                        presupuesto.cliente and presupuesto.cliente.nombre 
                            or presupuesto.nombrecliente, 
                        nombre_producto, 
                        cantidad, 
                        precio_unitario, 
                        precio_kilo, 
                        nombreobra, 
                        nombre_comercial, 
                        utils.float2str(ldp.get_subtotal()), 
                        presupuesto.puid)
                model.append(fila)
            i += 1
        # Y ahora la gráfica.
        if self.wids['notebook1'].get_current_page() == 0:
            self.graficar_por_oferta()
    
    def graficar_por_oferta(self):
        datachart = []  # Cada fila: Descripción, cantidad, color (7 = gris
                        #                                          0 = amarillo
                        #                                          3 = verde)
        datachart = [["De estudio", len(self.por_oferta), 1], 
                     #["De pedido", self.de_pedido, 3], 
                     #["Indeterminado", self.indeterminadas, 7], 
                     #["Total", self.total, 0]
                    ] 
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
            txt = "consulta_ofertas_estudio.py::graficar_por_oferta -> "\
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
        try:
            vpro.set_valor(i/tot, "Mostrando ofertas por producto...")
        except ZeroDivisionError:
            return  # No hay ofertas.
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
                            (nombre_producto, "0.0", puid))
                ofertado = ldp.cantidad
                fila = ("Presupuesto %d" % ldp.presupuesto.id, 
                        utils.float2str(ofertado), 
                        ldp.puid)
                model.append(padre, fila)
                # Actualizo totales fila padre.
                model[padre][1] = utils.float2str(
                        utils._float(model[padre][1]) + ofertado)
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
        _datachart.append(("Resto", sum([c[1] for c in datachart[5:]]), 7))
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
            txt = "consulta_ofertas_estudio.py::graficar_por_producto -> "\
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
        try:
            vpro.set_valor(i/tot, "Mostrando ofertas por cliente...")
        except ZeroDivisionError:
            return  # No hay ofertas que mostrar.
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
        _datachart.append(("Resto", sum([c[1] for c in datachart[5:]]), 7))
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
            txt = "consulta_ofertas_estudio.py::graficar_por_cliente -> "\
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
        try:
            vpro.set_valor(i/tot, "Mostrando ofertas por comercial...")
        except ZeroDivisionError:
            return  # No hay ofertas que mostrar
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
                                    if f[0] != "Sin comercial relacionado"])
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
            txt = "consulta_ofertas_estudio.py::graficar_por_comercial -> "\
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
        try:
            vpro.set_valor(i/tot, "Mostrando ofertas por provincia...")
        except ZeroDivisionError:
            return  # No hay ofertas que mostrar
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
                        model[padre][1] += "; " + nombre_comercial
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
        _datachart.append(("Resto", sum([c[1] for c in datachart[5:]]), 7))
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
            txt = "consulta_ofertas_estudio.py::graficar_por_provincia -> "\
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

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        from formularios import reports
        from informes.treeview2pdf import treeview2pdf
        if self.wids['notebook1'].get_current_page() == 0:
            tv = self.wids['tv_datos']
            titulo = "Ofertas"
            totales = [9]
            extra_data = [["", "", "===", "===", "===", 
                           "===", "===", "===", "===", ""], 
                          ["", "", 
                           "", 
                           "", 
                           "Total ofertado:", 
                           "", 
                           self.wids['e_total_ofertas'].get_text()
                          ]
                         ]
        elif self.wids['notebook1'].get_current_page() == 1:
            tv = self.wids['tv_cliente']
            titulo = "Ofertas por cliente"
            totales = [2]
            extra_data = [["==="] * 4, 
                          ["", 
                           "Total ofertado:", 
                           self.wids['e_total_ofertas'].get_text(),
                           ""], 
                         ]
        elif self.wids['notebook1'].get_current_page() == 2:
            tv = self.wids['tv_producto']
            titulo = "Ofertas por producto"
            totales = [1]
            extra_data = [["", "===", "==="], 
                          ["", 
                           "Total ofertado:", 
                           self.wids['e_total_ofertas'].get_text()], 
                         ]
        elif self.wids['notebook1'].get_current_page() == 3:
            tv = self.wids['tv_comercial']
            titulo = "Ofertas por comercial"
            totales = [3]
            extra_data = [["===", "===", "", ""], 
                          ["Total ofertado:", 
                           self.wids['e_total_ofertas'].get_text(), "", ""], 
                         ]
        elif self.wids['notebook1'].get_current_page() == 4:
            tv = self.wids['tv_provincia']
            titulo = "Ofertas por provincia"
            totales = [4]
            extra_data = [["===", "===", "", "", ""], 
                          ["Total ofertado:", 
                           self.wids['e_total_ofertas'].get_text(), 
                           "", "", ""], 
                         ]
        else:
            return
        if self.inicio:
            titulo += " desde %s" % utils.str_fecha(self.inicio)
        if self.fin:
            titulo += " hasta %s" % utils.str_fecha(self.fin)
        import tempfile 
        ruta_grafico = tempfile.NamedTemporaryFile(suffix = ".png").name
        win = self.wids['eventbox_chart'].window
        ancho, alto = win.get_size()
        pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, ancho, alto)
        captura = pb.get_from_drawable(win, win.get_colormap(), 0, 0, 0, 0, 
                                       ancho, alto)
        # Por algún motivo, que tendrá que ver con los dpi, ppp o cualquiera 
        # sabe qué complejo cálculo gráfico, la imagen sale muy grande en el 
        # PDF. La reduzco cutremente:
        escalado = captura.scale_simple(int(ancho * 0.75), int(alto * 0.75), 
                                        gtk.gdk.INTERP_TILES)
        escalado.save(ruta_grafico, "png")
        reports.abrir_pdf(treeview2pdf(tv, 
                                       titulo = titulo, 
                                       numcols_a_totalizar = totales, 
                                       graficos = [ruta_grafico], 
                                       extra_data = extra_data))


if __name__ == '__main__':
    t = ConsultaOfertasEstudio()

