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
## consulta_ofertas_pendientes_validar.py
###################################################################
## NOTAS:
##  
###################################################################
## 
## 
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
from presupuestos import NIVEL_VALIDACION, calcular_permiso_nuevos_pedidos

class ConsultaOfertasPendientesValidar(Ventana):
        
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'consulta_ofertas_pendientes_validar.glade', 
                         objeto, self.usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       'b_exportar/clicked': self.exportar} 
        self.add_connections(connections)
        cols = (('Número',   'gobject.TYPE_STRING', False, True, True, None),#0
                ('Fecha',     'gobject.TYPE_STRING', False, True, False, None),
                ('Cliente',   'gobject.TYPE_STRING', False, True, False, None),
                ('Obra',      'gobject.TYPE_STRING', False, True, False, None),
                ('Comercial', 'gobject.TYPE_STRING', False, True, False, None),
                #('Tipo',      'gobject.TYPE_STRING', False, True, False, None),
                # CWT: Solo ofertas de pedido. Nada de estudio.
                ('Estado',  'gobject.TYPE_STRING', False, True, False, None),#5
                ('Denegada', 'gobject.TYPE_BOOLEAN', False, True, False, None),
                ('Motivo', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Importe (c/IVA)',   
                              'gobject.TYPE_STRING', False, True, False, None),
                ('Forma de pago', 
                              'gobject.TYPE_STRING', False, True, False, None),
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None)) #10
        tv = self.wids['tv_datos']
        utils.preparar_listview(tv, cols)
        tv.connect("row-activated", self.abrir_objeto)
        tv.get_column(6).get_cell_renderers()[0].set_property('xalign', 0.5) 
        tv.get_column(8).get_cell_renderers()[0].set_property('xalign', 1) 
        self.colorear(tv)
        self.inicio = None
        self.wids['e_fechainicio'].set_text("")
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
        self.wids['ventana'].set_title(
                "Consulta de ofertas pendientes de validar")
        self.por_oferta = {} # defaultdict(lambda: [])
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
                else:
                    color = None    # TODO: ¿Tal vez un color por cada motivo de no validación automática?
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
        # En realidad solo va a haber presupuestos, pero lo he heredado de 
        # otra consulta y lo voy a dejar así de momento por si en adelante 
        # se mete algún tipo de agrupación o hace falta.
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
        no validadas por el usuario entre esas dos fechas.
        """
        if pclases.DEBUG:
            print "self.inicio", self.inicio, "self.fin", self.fin
        criterios = [pclases.Presupuesto.q.estudio == False, 
                     pclases.Presupuesto.q.usuarioID == None]
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
        self.rellenar_lista_presupuestos(presupuestos)
   
    def rellenar_lista_presupuestos(self, presupuestos):
        """
        Recibe una lista de presupuestos pre-filtrados por comercial, fecha y 
        cliente. Aquí se rellenan las tablas.
        """
        if pclases.DEBUG:
            ahora = time.time()
            print "rellenar_lista_presupuestos: begin"
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso()
        vpro.mostrar()
        vpro.set_valor(0, "Buscando ofertas pendientes de validación...")
        i = 0.0
        tot = presupuestos.count()
        if pclases.DEBUG:
            print "rellenar_lista_presupuestos: Congelando TreeView..."
        model = self.wids['tv_datos'].get_model()
        self.wids['tv_datos'].freeze_child_notify()
        model.clear()
        if pclases.DEBUG:
            print "rellenar_lista_presupuestos: Refrescando Model..."
        presupuestos_grafica = {}
        total = 0.0
        pendientes = 0
        for p in presupuestos:
            # CWT: No deben salir los presupuestos ya servidos. Más que nada 
            # porque si ya están servidos, no necesita validación y no 
            # deberían estar aquí.
            i += 1
            vpro.set_valor(i/tot, 
                           "Buscando ofertas pendientes de validación...")
            if p.get_pedidos():
                continue
            str_estado = p.get_str_estado()
            importe_total = p.calcular_importe_total()
            try:
                presupuestos_grafica[str_estado] += 1
            except KeyError:
                presupuestos_grafica[str_estado] = 1
            fila = (p.id, 
                    utils.str_fecha(p.fecha), 
                    p.nombrecliente, 
                    p.nombreobra, 
                    p.comercial and p.comercial.get_nombre_completo() or "", 
                    str_estado, 
                    p.rechazado, 
                    p.motivo, 
                    utils.float2str(importe_total), 
                    p.formaDePago and p.formaDePago.toString(p.cliente), 
                    p.puid)        # Oculta. Para el get.
            total += importe_total
            pendientes += 1
            model.append(fila)
        if pclases.DEBUG:
            print "rellenar_lista_presupuestos: Descongelando TreeView..."
        self.wids['tv_datos'].thaw_child_notify()
        self.wids['e_total'].set_text("%s €" % (utils.float2str(total)))
        self.wids['e_ofertas_pendientes'].set_text("%d" % (pendientes))
        vpro.ocultar()
        self.graficar(presupuestos_grafica)
        if pclases.DEBUG:
            print "rellenar_lista_presupuestos: end (", 
            print time.time() - ahora, "segundos )"

    def graficar(self, presupuestos_grafica):
        """
        Recibe un diccionario de presupuestos clasificados por estado 
        y construye la gráfica.
        """
        datachart = []  # Cada fila: Descripción, cantidad, color (7 = gris
                        #                                          0 = amarillo
                        #                                          3 = verde)
        for e in presupuestos_grafica:
            datachart.append([e, presupuestos_grafica[e], 3])
        try:
            oldchart = self.wids['eventbox_chart'].get_child()
            if oldchart != None:
                #self.wids['eventbox_chart'].remove(oldchart)
                chart = oldchart
            else:
                chart = charting.Chart(orient = "horizontal", 
                                       values_on_bars = True)
                self.wids['eventbox_chart'].add(chart)
            datachart.sort(lambda fila1, fila2: (fila1[1] < fila2[1] and -1) 
                                                 or (fila1[1] > fila2[1] and 1)
                                                 or 0, 
                           reverse = True)
            chart.plot(datachart)
            self.wids['eventbox_chart'].show_all()
        except Exception, msg:
            txt = "consulta_ofertas.py::graficar_por_oferta -> "\
                  "Error al dibujar gráfica (charting): %s" % msg
            print txt
            self.logger.error(txt)

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        tv = self.wids['tv_datos']
        abrir_csv(treeview2csv(tv))

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        from formularios import reports
        from informes.treeview2pdf import treeview2pdf
        tv = self.wids['tv_datos']
        titulo = "Ofertas"
        totales = [6]
        extra_data = []
        if self.inicio:
            titulo += " desde %s" % utils.str_fecha(self.inicio)
        if self.fin:
            titulo += " hasta %s" % utils.str_fecha(self.fin)
        #import tempfile 
        #ruta_grafico = tempfile.NamedTemporaryFile(suffix = ".png").name
        #win = self.wids['eventbox_chart'].window
        #ancho, alto = win.get_size()
        #pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, ancho, alto)
        #captura = pb.get_from_drawable(win, win.get_colormap(), 0, 0, 0, 0, 
        #                               ancho, alto)
        # Por algún motivo, que tendrá que ver con los dpi, ppp o cualquiera 
        # sabe qué complejo cálculo gráfico, la imagen sale muy grande en el 
        # PDF. La reduzco cutremente:
        #escalado = captura.scale_simple(int(ancho * 0.75), int(alto * 0.75), 
        #                                gtk.gdk.INTERP_TILES)
        #escalado.save(ruta_grafico, "png")
        reports.abrir_pdf(treeview2pdf(tv, 
                                       titulo = titulo, 
                                       numcols_a_totalizar = totales, 
                                       #graficos = [ruta_grafico], 
                                       extra_data = extra_data))


if __name__ == '__main__':
    t = ConsultaOfertasPendientesValidar()

