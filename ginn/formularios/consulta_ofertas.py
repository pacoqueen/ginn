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
## DONE:
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
        cols = (('N.º',      'gobject.TYPE_STRING', False, True, True, None),#0
                ('Fecha',     'gobject.TYPE_STRING', False, True, False, None),
                ('Cliente',   'gobject.TYPE_STRING', False, True, False, None),
                ('Producto',  'gobject.TYPE_STRING', False, True, False, None),
                ('Cantidad',  'gobject.TYPE_STRING', False, True, False, None),
                ('Precio', 'gobject.TYPE_STRING', False, True, False, None), #5
                ('€/kg',  'gobject.TYPE_STRING', False, True, False, None),
                ('Obra',      'gobject.TYPE_STRING', False, True, False, None),
                ('Comercial', 'gobject.TYPE_STRING', False, True, False, None),
                #('Tipo',      'gobject.TYPE_STRING', False, True, False, None),
                # CWT: Solo ofertas de pedido. Nada de estudio.
                ('Adjudicada','gobject.TYPE_BOOLEAN', False, True, False, None),
                #('Estado', 'gobject.TYPE_STRING', False, True, False, None),#10
                ('Forma de pago', 
                           'gobject.TYPE_STRING', False, True, False, None),#10
                #('Contacto',  'gobject.TYPE_STRING', False, True, False, None),
                ('Pedido',    'gobject.TYPE_STRING', False, True, False, None),
                ('Importe (s/IVA)',   
                              'gobject.TYPE_STRING', False, True, False, None),
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
        tv = self.wids['tv_datos']
        utils.preparar_listview(tv, cols)
        tv.connect("row-activated", self.abrir_objeto)
        tv.get_column(4).get_cell_renderers()[0].set_property('xalign', 1) 
        tv.get_column(5).get_cell_renderers()[0].set_property('xalign', 1) 
        tv.get_column(6).get_cell_renderers()[0].set_property('xalign', 1) 
        tv.get_column(12).get_cell_renderers()[0].set_property('xalign', 1) 
        self.colorear(tv)
        cols = (('Producto', 'gobject.TYPE_STRING', False, True, True, None),
                ('Cantidad Ofertada', 
                             'gobject.TYPE_STRING', False, True, False, None),
                ('Cantidad pedida',   
                             'gobject.TYPE_STRING', False, True, False, None), 
                ('PUID',     'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_producto'], cols)
        getcoltvpro = self.wids['tv_producto'].get_column
        getcoltvpro(1).get_cell_renderers()[0].set_property('xalign', 1) 
        getcoltvpro(2).get_cell_renderers()[0].set_property('xalign', 1) 
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
        self.todos_los_comerciales = [c for c in 
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
        self.wids['ventana'].set_title("Consulta de ofertas de pedido")
        self.por_oferta = {} # defaultdict(lambda: [])
        self.pedidos_generados = []
        self.por_producto = defaultdict(lambda: [])
        self.por_cliente = defaultdict(lambda: [])
        self.por_comercial = defaultdict(lambda: [])
        self.por_provincia = defaultdict(lambda: [])
        # El resumen
        cols = (('Comercial', 'gobject.TYPE_STRING', False, True, True, None), 
                ('Fibra\nofertada', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Fibra\nen pedido', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Geotextiles\nofertados', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Geotextiles\nen pedido', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Geocem\nofertado', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Geocem\nen pedido', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Comercializados\nofertados', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Comercializados\nen pedido', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Total\nofertado', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Total\nen pedido', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('NIL', 'gobject.TYPE_STRING', False, None, False, None))
        utils.preparar_treeview(self.wids['tv_resumen'], cols)
        for ncol in range(len(cols) - 2):
            col = self.wids['tv_resumen'].get_column(ncol+1)
            for cell in col.get_cell_renderers():
                cell.set_property('xalign', 1) 
        self.colorear_resumen(self.wids['tv_resumen'])
        self.resetear_resumen()
        gtk.main()

    def resetear_resumen(self):
        #for comercial in self.todos_los_comerciales + ['Total']: 
        self.resumen = {"Total": None}
        self.resumen["Total"] = valores_defecto_resumen()

    def colorear_resumen(self, tv):
        def cell_func(column, cell, model, itr, i):
            color = None
            titulo = column.get_property("title").lower()
            try:
                concepto = model[itr].parent[0]
            except TypeError:
                concepto = model[itr][0]
            if concepto == "Total":
                color = "Plum"
                if "ofertad" in titulo and model[itr][0] != "Total":
                    color = "light blue"
                elif "pedido" in titulo and model[itr][0] != "Total":
                    color = "yellow green"
            else:
                if "total" in titulo:
                    if "ofertad" in titulo:
                        color = "light blue"
                    elif "pedido" in titulo:
                        color = "yellow green"
                elif "ofertad" in titulo:
                    color = "alice blue"
                elif "pedido" in titulo:
                    color = "light green"
            cell.set_property("cell-background", color)
        cols = tv.get_columns()
        for i in xrange(len(cols)):
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell, cell_func, i)

    def colorear(self, tv):
        def cell_func(column, cell, model, itr, i):
            try:
                presupuesto = pclases.getObjetoPUID(model[itr][-1])
            except (AttributeError, pclases.SQLObjectNotFound):
                color = None
            else:
                if presupuesto.rechazado: 
                    color = "Indian Red"
                #elif presupuesto.get_pedidos(): # FIXME: Esto es muy lento.
                elif model[itr][11]: # Esta es la columna de los pedidos.
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
        try:
            objeto = pclases.getObjetoPUID(puid)
        except AttributeError:  # puid es None
            return  # No hago nada. Mutis por el foro...
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
        elif isinstance(objeto, pclases.PedidoVenta):
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
        self.resetear_resumen()
        self.por_oferta = {} # defaultdict(lambda: [])
        self.por_producto = defaultdict(lambda: [])
        self.por_cliente = defaultdict(lambda: [])
        self.por_comercial = defaultdict(lambda: [])
        self.por_provincia = defaultdict(lambda: [])
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
            # Clasificación del presupuesto en el resumen:
            clasificar_resumen_presupuesto(p, self.resumen)
            self.por_oferta[p] = p
            for ldp in p.lineasDePresupuesto:
                producto = ldp.producto or ldp.descripcion
                self.por_producto[producto].append(ldp)
            self.por_cliente[p.cliente].append(p)
            self.por_comercial[p.comercial].append(p)
            self.por_provincia[p.provincia.upper()].append(p)
            importe_total = p.calcular_importe_total()
            total_ofertas += importe_total
            if p.get_pedidos(): # Se asume que se convierte siempre la oferta 
                            # completa, por tanto cuento el importe total 
                            # del presupuesto en lugar operar con el pedido
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
        # Ahora hay que hacer un par de cálculos para totalizar el resumen
        totalizar_resumen(self.resumen)
        # y al final rellenar la tabla
        self.rellenar_tabla_resumen(vpro)
        vpro.ocultar()
        self.wids['e_total_ofertas'].set_text("%s €" % (
            utils.float2str(total_ofertas)))
        self.wids['e_total_pedidos'].set_text("%s €" % (
            utils.float2str(total_pedidos)))
        self.wids['e_ratio'].set_text("%s %%" % (ratio != None 
            and utils.float2str(ratio, precision = 2) or "-"))

    def rellenar_tabla_resumen(self, vpro):
        resumen = self.resumen
        model = self.wids['tv_resumen'].get_model()
        model.clear()
        comerciales_y_total = self.resumen.keys()
        comerciales_y_total.remove("Total")
        comerciales_y_total.sort(key = lambda i: i.get_nombre_completo())
        comerciales_y_total.append("Total")
        for c in comerciales_y_total:
            padre = model.append(None, 
                (c != "Total" and c.get_nombre_completo() or c, 
                 "", # Fibra ofertada
                 "", # Fibra en pedido
                 "", # Gtx ofertado
                 "", # Gtx en pedido
                 "", # Geocem ofertado
                 "", # Geocem en pedido
                 "", # Comercializado ofertado
                 "", # Comercializado en pedido
                 "", # Total ofertado
                 "", # Total en pedido
                 c != "Total" and c.id or 0))
            model.append(padre, 
                ("kg", 
                 utils.float2str(resumen[c]['fibra']['ofertado']['kg']), 
                 utils.float2str(resumen[c]['fibra']['en_pedido']['kg']), 
                 utils.float2str(resumen[c]['geotextiles']['ofertado']['kg']), 
                 utils.float2str(resumen[c]['geotextiles']['en_pedido']['kg']), 
                 utils.float2str(resumen[c]['geocem']['ofertado']['kg']), 
                 utils.float2str(resumen[c]['geocem']['en_pedido']['kg']), 
                 utils.float2str(resumen[c]['comercializados']['ofertado']['kg']), 
                 utils.float2str(resumen[c]['comercializados']['en_pedido']['kg']), 
                 utils.float2str(resumen[c]['Total']['ofertado']['kg']), 
                 utils.float2str(resumen[c]['Total']['en_pedido']['kg']), 
                 0))
            model.append(padre, 
                ("Importe", 
                 utils.float2str(resumen[c]['fibra']['ofertado']['importe']), 
                 utils.float2str(resumen[c]['fibra']['en_pedido']['importe']), 
                 utils.float2str(resumen[c]['geotextiles']['ofertado']['importe']), 
                 utils.float2str(resumen[c]['geotextiles']['en_pedido']['importe']), 
                 utils.float2str(resumen[c]['geocem']['ofertado']['importe']), 
                 utils.float2str(resumen[c]['geocem']['en_pedido']['importe']), 
                 utils.float2str(resumen[c]['comercializados']['ofertado']['importe']), 
                 utils.float2str(resumen[c]['comercializados']['en_pedido']['importe']), 
                 utils.float2str(resumen[c]['Total']['ofertado']['importe']), 
                 utils.float2str(resumen[c]['Total']['en_pedido']['importe']), 
                 0))
            model.append(padre, 
                ("€/k", 
                 utils.float2str(resumen[c]['fibra']['ofertado']['€/kg']), 
                 utils.float2str(resumen[c]['fibra']['en_pedido']['€/kg']), 
                 utils.float2str(resumen[c]['geotextiles']['ofertado']['€/kg']), 
                 utils.float2str(resumen[c]['geotextiles']['en_pedido']['€/kg']), 
                 utils.float2str(resumen[c]['geocem']['ofertado']['€/kg']), 
                 utils.float2str(resumen[c]['geocem']['en_pedido']['€/kg']), 
                 utils.float2str(resumen[c]['comercializados']['ofertado']['€/kg']), 
                 utils.float2str(resumen[c]['comercializados']['en_pedido']['€/kg']), 
                 utils.float2str(resumen[c]['Total']['ofertado']['€/kg']), 
                 utils.float2str(resumen[c]['Total']['en_pedido']['€/kg']), 
                 0))
            model.append(padre, 
                ("días", 
                 utils.float2str(resumen[c]['fibra']['ofertado']['días']), 
                 utils.float2str(resumen[c]['fibra']['en_pedido']['días']), 
                 utils.float2str(resumen[c]['geotextiles']['ofertado']['días']), 
                 utils.float2str(resumen[c]['geotextiles']['en_pedido']['días']), 
                 utils.float2str(resumen[c]['geocem']['ofertado']['días']), 
                 utils.float2str(resumen[c]['geocem']['en_pedido']['días']), 
                 utils.float2str(resumen[c]['comercializados']['ofertado']['días']), 
                 utils.float2str(resumen[c]['comercializados']['en_pedido']['días']), 
                 utils.float2str(resumen[c]['Total']['ofertado']['días']), 
                 utils.float2str(resumen[c]['Total']['en_pedido']['días']), 
                 0))
        self.wids['tv_resumen'].expand_all()

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
        self.pedidos_generados = []
        presupuestos = self.por_oferta.keys()
        presupuestos.sort(key = lambda p: p.id, reverse = True)
        for p in presupuestos:
            vpro.set_valor(i/tot, "Mostrando listado de ofertas... (%d)" % p.id)
            presupuesto = self.por_oferta[p]  # Él mismo en la práctica.
            pedidos = presupuesto.get_pedidos()
            self.pedidos_generados += [ped for ped in pedidos 
                                       if ped not in self.pedidos_generados]
            cadena_pedidos=", ".join([pedido.numpedido for pedido in pedidos])
            nombreobra = (presupuesto.obra and presupuesto.obra.nombre 
                          or presupuesto.nombreobra)
            #if len(nombreobra) > 33:
            #    nombreobra = nombreobra[:33] + "..."
            if len(nombreobra) > 80:
                nombreobra = utils.wrap(nombreobra, 80)
            nombre_comercial = (presupuesto.comercial 
                            and presupuesto.comercial.get_nombre_completo()
                            or "Sin comercial relacionado")
            #estado = presupuesto.get_str_estado().replace("\n", " ")
            #if presupuesto.validado:
            #    estado += " (%s)" % presupuesto.get_str_validacion()
            try:
                str_forma_de_pago = presupuesto.formaDePago.toString(
                        presupuesto.cliente)
            except AttributeError: 
                str_forma_de_pago = ""
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
                fila = (#"%d (%s € IVA incl.)" % (presupuesto.id, 
                        #    utils.float2str(total_presupuesto)), 
                        `presupuesto.id`,     # CWT
                        utils.str_fecha(presupuesto.fecha), 
                        presupuesto.cliente and presupuesto.cliente.nombre 
                            or presupuesto.nombrecliente, 
                        nombre_producto, 
                        cantidad, 
                        precio_unitario, 
                        precio_kilo, 
                        nombreobra, 
                        nombre_comercial, 
                        presupuesto.adjudicada, 
                        #estado, 
                        str_forma_de_pago, 
                        # presupuesto.personaContacto, # CWT: Ya no
                        cadena_pedidos, 
                        #utils.float2str(presupuesto.calcular_importe_total()),
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
                color = 1   # En naranja los servicios.
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
                            and presupuesto.formaDePago.toString(
                                presupuesto.cliente) or "", 
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
                            and presupuesto.formaDePago.toString(
                                presupuesto.cliente) or "", 
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
                            and presupuesto.formaDePago.toString(
                                presupuesto.cliente) or "", 
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
        elif self.wids['notebook1'].get_current_page() == 5:
            tv = self.wids['tv_resumen']
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
            totales = [12]
            extra_data = [["", "", "===", "===", "===", 
                           "===", "===", "===", "===", ""], 
                          ["", "", 
                           "Ratio de conversión:", 
                           self.wids['e_ratio'].get_text(), 
                           "Total ofertado:", 
                           "", 
                           self.wids['e_total_ofertas'].get_text(), 
                           "Total pedido:", 
                           self.wids['e_total_pedidos'].get_text(), 
                           ""]
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
                          ["", 
                           "Total pedido:", 
                           self.wids['e_total_pedidos'].get_text(), 
                           ""], 
                          ["", 
                           "Ratio de conversión:", 
                           self.wids['e_ratio'].get_text(), ""]
                         ]
        elif self.wids['notebook1'].get_current_page() == 2:
            tv = self.wids['tv_producto']
            titulo = "Ofertas por producto"
            totales = [1, 2]
            extra_data = [["", "===", "==="], 
                          ["", 
                           "Total ofertado:", 
                           self.wids['e_total_ofertas'].get_text()], 
                          ["", 
                           "Total pedido:", 
                           self.wids['e_total_pedidos'].get_text()], 
                          ["", 
                           "Ratio de conversión:", 
                           self.wids['e_ratio'].get_text()]
                         ]
        elif self.wids['notebook1'].get_current_page() == 3:
            tv = self.wids['tv_comercial']
            titulo = "Ofertas por comercial"
            totales = [3]
            extra_data = [["===", "===", "", ""], 
                          ["Total ofertado:", 
                           self.wids['e_total_ofertas'].get_text(), "", ""], 
                          ["Total pedido:", 
                           self.wids['e_total_pedidos'].get_text(), "", ""], 
                          ["Ratio de conversión:", 
                           self.wids['e_ratio'].get_text(), "", ""]
                         ]
        elif self.wids['notebook1'].get_current_page() == 4:
            tv = self.wids['tv_provincia']
            titulo = "Ofertas por provincia"
            totales = [4]
            extra_data = [["===", "===", "", "", ""], 
                          ["Total ofertado:", 
                           self.wids['e_total_ofertas'].get_text(), 
                           "", "", ""], 
                          ["Total pedido:", 
                           self.wids['e_total_pedidos'].get_text(), 
                           "", "", ""], 
                          ["Ratio de conversión:", 
                           self.wids['e_ratio'].get_text(), 
                           "", "", ""]
                         ]
        elif self.wids['notebook1'].get_current_page() == 5:
            tv = self.wids['tv_resumen']
            titulo = "Resumen por comercial, tipo de producto y estado"
            totales = []
            extra_data = []
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

def clasificar_resumen_presupuesto(p, resumen):
    """
    «resumen» es un diccionario. «p» es un presupuesto. Sus líneas de 
    presupuesto y servicio se clasificarán en el diccionario que corresponda 
    dentro de «resumen».
    """
    c = p.comercial
    for ldp in p.lineasDePresupuesto:
        clasificar_resumen_linea(ldp, resumen, c)

def clasificar_resumen_linea(ldp, resumen, c):
    if isinstance(ldp.producto, pclases.ProductoCompra):
        tipo_producto = "comercializados"
    elif isinstance(ldp.producto, pclases.ProductoVenta):
        if ldp.producto.es_bala() or ldp.producto.es_bala_cable():
            tipo_producto = "fibra"
        elif (ldp.producto.es_rollo() or ldp.producto.es_rolloC() 
                or ldp.producto.es_rolloC()):
            tipo_producto = "geotextiles"
        elif ldp.producto.es_bigbag() or ldp.producto.es_caja():
            tipo_producto = "geocem"
        else:
            tipo_producto = "comercializados"
    else:
        tipo_producto = "comercializados"
    kg = ldp.cantidad
    if tipo_producto == "geotextiles":  # La cantidad es en metros cuadrados.
        kg *= ldp.producto.camposEspecificosRollo.gramos / 1000.0
    importe = ldp.get_subtotal()
    try:
        dias = ldp.presupuesto.formaDePago.plazo
    except AttributeError:
        dias = None
    if c not in resumen:
        resumen[c] = valores_defecto_resumen()
    resumen[c][tipo_producto]['ofertado']['kg'] += kg
    resumen[c][tipo_producto]['ofertado']['importe'] += importe
    resumen[c][tipo_producto]['ofertado']['€/kg'][0] += importe
    resumen[c][tipo_producto]['ofertado']['€/kg'][1] += kg
    resumen[c][tipo_producto]['ofertado']['días'].append(dias)
    if pclases.DEBUG:
        print " --->", resumen[c]['Total']['ofertado']['kg']
        print " +", kg, "(" + tipo_producto + ")"
    resumen[c]['Total']['ofertado']['kg'] += kg
    resumen[c]['Total']['ofertado']['importe'] += importe
    resumen[c]['Total']['ofertado']['€/kg'][0] += importe
    resumen[c]['Total']['ofertado']['€/kg'][1] += kg
    resumen[c]['Total']['ofertado']['días'].append(dias)
    if pclases.DEBUG:
        print "\t=", resumen[c]['Total']['ofertado']['kg']
    resumen['Total'][tipo_producto]['ofertado']['kg'] += kg
    resumen['Total'][tipo_producto]['ofertado']['importe'] += importe
    resumen['Total'][tipo_producto]['ofertado']['€/kg'][0] += importe
    resumen['Total'][tipo_producto]['ofertado']['€/kg'][1] += kg
    resumen['Total'][tipo_producto]['ofertado']['días'].append(dias)
    resumen['Total']['Total']['ofertado']['kg'] += kg   # Total total ???
    resumen['Total']['Total']['ofertado']['importe'] += importe
    resumen['Total']['Total']['ofertado']['€/kg'][0] += importe
    resumen['Total']['Total']['ofertado']['€/kg'][1] += kg
    resumen['Total']['Total']['ofertado']['días'].append(dias)
    if ldp.presupuesto.get_pedidos():
        resumen[c][tipo_producto]['en_pedido']['kg'] += kg
        resumen[c][tipo_producto]['en_pedido']['importe'] += importe
        resumen[c][tipo_producto]['en_pedido']['€/kg'][0] += importe
        resumen[c][tipo_producto]['en_pedido']['€/kg'][1] += kg
        resumen[c][tipo_producto]['en_pedido']['días'].append(dias)
        resumen[c]['Total']['en_pedido']['kg'] += kg
        resumen[c]['Total']['en_pedido']['importe'] += importe
        resumen[c]['Total']['en_pedido']['€/kg'][0] += importe
        resumen[c]['Total']['en_pedido']['€/kg'][1] += kg
        resumen[c]['Total']['en_pedido']['días'].append(dias)
        resumen['Total'][tipo_producto]['en_pedido']['kg'] += kg
        resumen['Total'][tipo_producto]['en_pedido']['importe'] += importe
        resumen['Total'][tipo_producto]['en_pedido']['€/kg'][0] += importe
        resumen['Total'][tipo_producto]['en_pedido']['€/kg'][1] += kg
        resumen['Total'][tipo_producto]['en_pedido']['días'].append(dias)
        resumen['Total']['Total']['en_pedido']['kg'] += kg
        resumen['Total']['Total']['en_pedido']['importe'] += importe
        resumen['Total']['Total']['en_pedido']['€/kg'][0] += importe
        resumen['Total']['Total']['en_pedido']['€/kg'][1] += kg
        resumen['Total']['Total']['en_pedido']['días'].append(dias)

def totalizar_resumen(r):
    """
    Totaliza los €/kg y hace la media de días.
    """
    for c in r:
        for tipo in r[c]:
            for ofertado_o_adjudicado in r[c][tipo]:
                e, k = r[c][tipo][ofertado_o_adjudicado]['€/kg']
                try:
                    r[c][tipo][ofertado_o_adjudicado]['€/kg'] = e/k
                except ZeroDivisionError:
                    r[c][tipo][ofertado_o_adjudicado]['€/kg'] = 0.0 # None 
                # Limpio los Nones en días de plazo de las formas de pago:
                dias_plazo_pago = [d for d in 
                        r[c][tipo][ofertado_o_adjudicado]['días']
                        if d != None]
                r[c][tipo][ofertado_o_adjudicado]['días'] = utils.media(
                        dias_plazo_pago)

def valores_defecto_resumen():
        default = {
                    'fibra': {'ofertado':  {'kg': 0.0, 
                                            'importe': 0.0, 
                                            '€/kg': [0.0, 0.0], 
                                            'días': []}, 
                              'en_pedido': {'kg': 0.0, 
                                            'importe': 0.0, 
                                            '€/kg': [0.0, 0.0], 
                                            'días': []}}, 
                    'geotextiles': {
                              'ofertado':  {'kg': 0.0, 
                                            'importe': 0.0, 
                                            '€/kg': [0.0, 0.0], 
                                            'días': []}, 
                              'en_pedido': {'kg': 0.0, 
                                            'importe': 0.0, 
                                            '€/kg': [0.0, 0.0], 
                                            'días': []}}, 
                    'geocem': {
                              'ofertado':  {'kg': 0.0, 
                                            'importe': 0.0, 
                                            '€/kg': [0.0, 0.0], 
                                            'días': []}, 
                              'en_pedido': {'kg': 0.0, 
                                            'importe': 0.0, 
                                            '€/kg': [0.0, 0.0], 
                                            'días': []}},
                    'comercializados': {
                              'ofertado': {'kg': 0.0, 
                                            'importe': 0.0, 
                                            '€/kg': [0.0, 0.0], 
                                            'días': []}, 
                              'en_pedido': {'kg': 0.0, 
                                            'importe': 0.0, 
                                            '€/kg': [0.0, 0.0], 
                                            'días': []}},  
                    'Total': {'ofertado':  {'kg': 0.0, 
                                            'importe': 0.0, 
                                            '€/kg': [0.0, 0.0], 
                                            'días': []}, 
                              'en_pedido': {'kg': 0.0, 
                                            'importe': 0.0, 
                                            '€/kg': [0.0, 0.0], 
                                            'días': []}}}
        return default


if __name__ == '__main__':
    t = ConsultaOfertas()

