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
## tpv.py - Ventana de Terminal Punto de Venta.
###################################################################
## TODO:
## ¿Necesito en la ventana de buscar ticket una opción para 
## borrarlo, modificarlo o pasarlo a la ventana de TPV principal?
## No sé si faltaría un desplegable para elegir el almacén del que 
## descontar existencias. No se va a usar de momento el TPV más 
## que para el almacén principal, pero no descartaría la opción 
## de momento.
###################################################################

import sys, os
try:
    import psyco
    psyco.full()
except ImportError:
    pass

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time
try:
    import pclases
except ImportError:
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    import pclases
import mx
try:
    import geninformes
except ImportError:
    sys.path.append('../informes')
    import geninformes
import pango
import gobject
from facturas_venta import debe_generar_recibo, generar_recibo


def check_almacen():
    """
    Si no existe almacén principal, lo crea. Es necesario desde hace unos 
    meses que exista al menos un almacén.
    """
    if pclases.DEBUG:
        print "tpv.py: Chequeando almacén principal...", 
        sys.stdout.flush()
    pclases.Almacen.crear_almacen_principal()
    if pclases.DEBUG:
        print "OK"

def intentar_imprimir_ticket(ticket):
    """
    Intenta imprimir un ticket por la impresota de tickets. Si no puede, 
    abre un fichero de texto plano con el contenido.
    """
    try:
        imprimir_ticket(ticket)
    except Exception, msg:
        utils.dialogo_info(titulo = "ERROR IMPRESORA", 
                           texto = "Ocurrió un error al acceder a la "
                                   "impresora de tickets.\nEl ticket se "
                                   "mostrará como fichero de texto plano.\n\n"
                                   "Información de depuración:\n%s" % msg)
        import tempfile, os
        fdest = os.path.join(tempfile.gettempdir(), 
                             "ticket_%d.txt" % ticket.numticket)
        dest = file(fdest, "w")
        volcar_texto_ticket(ticket, dest)
        dest.close()
        import multi_open
        multi_open.open(fdest)

def volcar_texto_ticket(ticket, dest):
    """
    Vuelca el texto que se imprimiría por ticketera en el fichero «fdest».
    """
    try:
        dde = pclases.DatosDeLaEmpresa.select()[0]
    except IndexError:
        print "tpv::imprimir_ticket -> No se encontraron los datos de la empresa. Abortando impresión..."
    else:
        ANCHO = pclases.config.get_anchoticket()
        linea0 = (" ", "RS")
        linea1 = (dde.nombre.center(ANCHO), "RSC")
        modo = "RC"
        if pclases.config.get_mostrarcontactoenticket():
            linea2 = (dde.nombreContacto.center(ANCHO), modo)
        else:
            linea2 = ("", "")
        linea3 = (("NIF %s" % (dde.cif)).center(ANCHO), modo)
        linea4 = (("%s. Tlf: %s" % (dde.direccion, dde.telefono)).center(ANCHO), modo)
        linea5 = ("", [])
        lineas = [linea1, linea2, linea3, linea4, linea5]
        lineas.append((("Ticket %d - %s %s" % (
                        ticket.numticket, 
                        utils.str_fecha(ticket.fechahora), 
                        utils.str_hora(ticket.fechahora))).center(ANCHO), 
                       "SI"))
        for ldv in ticket.lineasDeVenta:
            lineas += split_descuento(ldv, ANCHO)
        lineas.append((total_ticket(ticket, ANCHO), "A"))
        lineas.append(("\nIVA incluido - Gracias por su visita", ""))
        dest.writelines(l[0]+"\n" for l in lineas)

def split_descuento(ldv, ancho):
    """
    Devuelve una lista con la línea recibida ya procesada o la línea y otra 
    línea más de descuento si la LDV lleva descuento.
    """
    linea = (cortar_linea_ticket(ldv, ancho, "\n"), ">")
    lineas = [linea]
    if ldv.descuento != 0:
        lineas.append(build_linea_descuento(ldv, ancho))
    return lineas

def build_linea_descuento(ldv, ancho):
    """
    Devuelve una tupla con la línea de texto del descuento aplicado en el 
    formato en que espera recibirlo el procesador de impresión de tickets.
    """
    class FakeProducto:
        def __init__(self, descuento):
            desc = utils.float2str(descuento * 100, autodec = True)
            self.descripcion = "Descuento aplicado: %s %%" % desc
    class FakeLDV:
        def __init__(self, ldv):
            self.producto = FakeProducto(ldv.descuento)
            self.precio = -1 * ldv.precio * ldv.descuento
            self.cantidad = ldv.cantidad
        def get_subtotal(self, *args, **kw):
            return self.cantidad * self.precio
    ldvdesc = FakeLDV(ldv)
    ldesc = cortar_linea_ticket(ldvdesc, ancho, "\n")
    return (ldesc, ">")

def ventana_ticket(ticket, usuario, padre = None):
    """
    Muestra una ventana con la información del ticket recibido y los botones de 
    facturar e imprimir.
    """
    v = Ventana("ticket.glade", ticket, usuario = usuario)
    v.add_connections({"b_salir/clicked": v.salir,
                       "b_imprimir/clicked": 
                            lambda boton: intentar_imprimir_ticket(ticket), 
                       }) 
    v.wids['ventana'].set_transient_for(padre)
    v.wids['ventana'].show_all()
    v.wids['b_facturar'].set_property("visible", False) # Se habilitará en 
                                    # función de los permisos del usuario.
    v.wids['ventana'].set_title("TICKET %d" % ticket.numticket)
    v.wids['ventana'].resize(640, 480)
    cols = (('Venta', 'gobject.TYPE_STRING',    False, True, True, None),
            ('Código', 'gobject.TYPE_STRING',   False, True, False, None),
            ('Producto', 'gobject.TYPE_STRING', False, True, False, None),
            ('P.V.P.', 'gobject.TYPE_STRING',   False, True, False, None),
            ('Dto.', 'gobject.TYPE_STRING',     False, True, False, None),
            ('Cantidad', 'gobject.TYPE_STRING', False, True, False, None),
            ('Total', 'gobject.TYPE_STRING',    False, True, False, None),
            ('Factura', 'gobject.TYPE_STRING',  False, True, False, None),
            ('IDLDV', 'gobject.TYPE_INT64',     False, False, False, None))
    utils.preparar_treeview(v.wids['tv_ldvs'], cols)
    model = v.wids["tv_ldvs"].get_model()
    model.clear()
    totalticket = 0.0
    padre = model.append(None, (ticket.numticket, 
                                utils.str_fecha(ticket.fechahora), 
                                utils.str_hora(ticket.fechahora),
                                "", 
                                "", 
                                "", 
                                #"%s €" % (utils.float2str(
                                #    totalticket)), 
                                "", 
                                "", 
                                ", ".join([fra.numfactura for fra 
                                            in ticket.get_facturas()]), 
                                ticket.id))
    for ldv in ticket.lineasDeVenta:
        descripcion = ldv.producto.descripcion
        if len(descripcion) > 30:
            descripcion = utils.wrap(descripcion, 30)
        totalldv = ldv.get_subtotal(iva = False) * (1 + ticket.get_iva())
        model.append(padre, 
                      ("", 
                       ldv.producto.codigo, 
                       descripcion, 
                       "%s €" % (utils.float2str(ldv.precio 
                                                 * (1 + ticket.get_iva())
                                                 * (1 - ldv.descuento))),
                        # P.V.P. lleva 21% de IVA.
                       "%s" % (ldv.descuento 
                               and utils.float2str(ldv.descuento * 100, 
                                                   autodec = True) + "%" 
                               or ""), 
                       "%s" % utils.float2str(ldv.cantidad), 
                       "%s €" % utils.float2str(totalldv),
                        # Ventas de ticket llevan 21% de IVA. 
                        # Lo calculo aquí porque la 
                        # función toma el IVA en función del 
                        # cliente del pedido/albarán/factura.
                       ldv.get_factura_o_prefactura() 
                        and ldv.get_factura_o_prefactura().numfactura 
                        or "", 
                       ldv.id))
        totalticket += totalldv
    model[padre][5] = "%s €" % utils.float2str(totalticket)
    v.wids['tv_ldvs'].expand_all()
    gtk.main()

class TPV(Ventana):

    DIAS_TREEVIEW = pclases.config.get_diastpv()

    def __init__(self, objeto = None, usuario = None):
        self.usuario = usuario
        Ventana.__init__(self, 'tpv.glade', objeto, usuario = self.usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_articulo/clicked': self.add_ldv, 
                       'b_venta/clicked': self.cerrar_venta, 
                       'b_drop_venta/clicked': self.borrar_venta, 
                       'b_facturar/clicked': self.facturar, 
                       'b_actualizar/clicked': self.actualizar_ventana, 
                       'b_cajon/clicked': self.abrir_cajon, 
                       'b_buscarticket/clicked': self.buscar_ticket, 
                       'b_arqueo/clicked': self.arqueo
                      }
        self.add_connections(connections)
        self.inicializar_ventana()
        #import thread
        #gtk.gdk.threads_init()
        #thread.start_new_thread(gtk.main, ())
        # https://arco.inf-cr.uclm.es/pipermail/python/2005-January/000105.html
        gtk.main()

    def buscar_ticket(self, boton):
        """
        Busca un ticket por número o fecha y muestra una ventana desde la que 
        se puede imprimir o facturar el ticket. No se permite eliminarlo ni 
        editarlo, ya que modificaría el arqueo de caja del día al que pertenece.
        Si fuera un ticket actual, el usuario puede editarlo desde el propio 
        TPV, así que no tiene por qué recurrir a esta ventana para ello.
        """
        ticket_o_fecha = utils.dialogo_entrada(
            titulo = "TPV: BUSCAR TICKET", 
            texto="Introduzca número de ticket o fecha en formato dd/mm/aaaa:",
            padre = self.wids['ventana'])
        if ticket_o_fecha:
            try:
                fecha = utils.parse_fecha(ticket_o_fecha)
                tickets = pclases.Ticket.select(pclases.AND(
                    pclases.Ticket.q.fechahora >= fecha, 
                    pclases.Ticket.q.fechahora < fecha + mx.DateTime.oneDay))
            except ValueError:
                tickets = pclases.Ticket.select(
                    pclases.Ticket.q.numticket == ticket_o_fecha)
            if tickets.count() > 0:
                resultados = [(t.id, 
                               t.numticket, 
                               utils.str_fechahora(t.fechahora), 
                               utils.float2str(t.calcular_total(
                                                        iva_incluido = True)), 
                               len(t.lineasDeVenta)) for t in tickets]
                ticket = utils.dialogo_resultado(resultados, 
                                                 "Seleccione un ticket:", 
                                                 multi = False, 
                                                 padre = self.wids['ventana'], 
                                                 cabeceras = ("ID", 
                                                              "Número", 
                                                              "Fecha y hora", 
                                                              "Total", 
                                                              "Líneas"))
                if ticket and ticket > 0:
                    ticket = pclases.Ticket.get(ticket)
                    ventana_ticket(ticket, 
                                   self.usuario, 
                                   padre = self.wids['ventana'])
            else:
                utils.dialogo_info(titulo = "SIN RESULTADOS", 
                                   texto = "No se encontraron tickets.", 
                                   padre = self.wids['ventana'])

    def _add_buttons_dto(self):
        """
        Añade dos botones equivalentes a los icons del entry de descuento.
        """
        b_lineas = self.wids['b_lineas']
        b_ticket = self.wids['b_ticket']
        try:
            b_lineas.set_tooltip_text(
                "Aplicar descuento a las líneas seleccionadas.")
            b_ticket.set_tooltip_text(
                "Aplicar descuento al ticket actual completo.")
        except AttributeError:
            pass    # No acepta tooltip. Versión antiquísima de pygtk.
        b_lineas.connect("clicked", self.aplicar_descuento_lineas)
        b_ticket.connect("clicked", self.aplicar_descuento_ticket)
        b_lineas.set_property("visible", True)
        b_ticket.set_property("visible", True)

    def _config_boton_descuento(self):
        """
        Añade un botón para aplicar descuento al precio en la línea de venta 
        actual, a un ticket completo o a las líneas seleccionadas en 
        función de los dos pequeños iconos pulsables del Entry.
        OJO: Requiere gtk
        """
        self.wids['b_lineas'].set_property("visible", False)
        self.wids['b_ticket'].set_property("visible", False)
        #self.wids['e_descuento'].set_text("0 %")
        try:
            # Este aplicará el descuento a las líneas seleccionadas:
            self.wids['e_descuento'].set_property("primary-icon-stock", 
                                                  gtk.STOCK_APPLY)
            self.wids['e_descuento'].set_property("primary-icon-tooltip-text", 
                "Aplicar descuento a las líneas seleccionadas.")
            # Este aplicará el descuento al ticket completo:
            self.wids['e_descuento'].set_property("secondary-icon-stock", 
                                                  gtk.STOCK_CONVERT)
            self.wids['e_descuento'].set_property(
                "secondary-icon-tooltip-text", 
                "Aplicar descuento al ticket actual completo.")
            self.wids['e_descuento'].set_tooltip_text("Descuento a aplicar en "
                "la venta actual. Pulse en los iconos para aplicar el "
                "descuento a las líneas seleccionadas o al ticket completo.")
            self.wids['e_descuento'].connect("icon-press", 
                                             self.__aplicar_descuento)
        except Exception, e: # Versión pygtk < 2.16
            self._add_buttons_dto()
        self.wids['e_descuento'].set_range(0, 100)
        self.wids['e_descuento'].set_increments(1, 10)
        self.wids['e_descuento'].connect("changed", self.actualizar_subtotal)
        self.wids['e_descuento'].connect("key_press_event", 
                                         pasar_foco_enter, 
                                         self.wids, 
                                         'b_articulo')

    def __aplicar_descuento(self, entry, icono, evento):
        """
        Aplica el descuento escrito en el Entry a las líneas marcadas en el 
        TreeView de tickets o a toda la venta actual.
        """
        self.wids['e_descuento'].update()    # Me aseguro de que el 
            # valor que me va a devolver el get_value es realmente el que 
            # hay en pantalla. Si se escribe un número y se pulsan los 
            # stock_icons sin perder el foco, el valor devuelto es el anterior.
        if icono == gtk.ENTRY_ICON_PRIMARY:  # A líneas seleccionadas del T.V.
            self.aplicar_descuento_lineas()
        elif icono == gtk.ENTRY_ICON_SECONDARY:  # A todo el ticket actual
            self.aplicar_descuento_ticket()
    
    def aplicar_descuento_lineas(self, *arg, **kw):
        """
        Aplica el descuento a las líneas seleccionadas en el TreeView.
        """
        dto = self.get_dto()
        if dto < 1: # Viene como fracción, en ventana *100
            dto_dialogo = dto * 100
        else:
            dto_dialogo = dto
        ldvs = []
        if self.wids['tv_ventas'].get_selection().count_selected_rows() != 0: 
            if utils.dialogo(titulo = "DESCUENTO TICKETS", 
                             texto = "¿Aplicar descuento de %d %% a las líneas"
                                     " seleccionadas?" % dto_dialogo, 
                             padre = self.wids['ventana']):
                model, paths = self.wids['tv_ventas'].get_selection().get_selected_rows()
                for path in paths:
                    iter = model.get_iter(path)
                    if model[iter].parent == None:  # Es un ticket
                        idticket = model[iter][-1]
                        ticket = pclases.Ticket.get(idticket)
                        for ldv in ticket.lineasDeVenta:
                            if ldv not in ldvs:
                                ldvs.append(ldv)
                    else:   # Es una LDV
                        idldv = model[iter][-1] 
                        ldv = pclases.LineaDeVenta.get(idldv)
                        if ldv not in ldvs:
                            ldvs.append(ldv)
        self.aplicar_descuento(ldvs, dto)

    def aplicar_descuento_ticket(self, *args, **kw):
        """
        Aplica el descuento a la venta completa actual.
        """
        dto = self.get_dto()
        print dto
        ldvs = []
        print self.ticket
        if self.ticket != None:
            for ldv in self.ticket.lineasDeVenta:
                ldvs.append(ldv)
        self.aplicar_descuento(ldvs, dto)

    def get_dto(self):
        """
        Devuelve el descuento presente en la ventana.
        """
        dto = self.wids['e_descuento'].get_value_as_int()
        if dto >= 1: # Viene como entero:
            dto /= 100.0
        return dto

    def aplicar_descuento(self, ldvs, dto):
        """
        Aplica el descuento a todas las líneas de venta recibidas y actualiza 
        la ventana.
        """
        for ldv in ldvs:
            ldv.descuento = dto
            ldv.syncUpdate()
        self.actualizar_ventana(machacar_precio_producto = False)

    def inicializar_ventana(self):
        """
        Inicializa controles, TreeViews, etc.
        """
        self.comprobar_boton_facturar()
        cols = (('Venta', 'gobject.TYPE_STRING', True, True, True, 
                    self.cambiar_numventa),
                ('Código', 'gobject.TYPE_STRING', False, True, False, None),
                ('Producto', 'gobject.TYPE_STRING', False, True, False, None),
                ('P.V.P.', 'gobject.TYPE_STRING', False, True, False, None),
                ('Dto.', 'gobject.TYPE_STRING',     False, True, False, None),
                ('Cantidad', 'gobject.TYPE_STRING', False, True, False, None),
                ('Total', 'gobject.TYPE_STRING', False, True, False, None),
                ('Factura', 'gobject.TYPE_STRING', False, True, False, None),
                ('IDLDV', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_ventas'], cols)
        self.wids['tv_ventas'].get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        self.wids['tv_ventas'].connect("row-activated", self.activar_ticket)
        for col in (self.wids['tv_ventas'].get_columns()[0:1]
                    + self.wids['tv_ventas'].get_columns()[3:6]):
            for cell in col.get_cell_renderers():
                cell.set_property("xalign", 1.0)
        tarifas = [(t.id, t.nombre) 
                    for t in pclases.Tarifa.select(orderBy = "nombre") 
                    if ((t.periodoValidezIni == None 
                         or t.periodoValidezIni <= mx.DateTime.localtime()) 
                        and (t.periodoValidezFin == None 
                             or t.periodoValidezFin>=mx.DateTime.localtime()))]
        utils.rellenar_lista(self.wids['cbe_tarifa'], tarifas)
        self.wids['cbe_tarifa'].connect("changed", self.mostrar_info_producto)
        self.rellenar_ultimas_ventas()
        self.wids['e_cantidad'].set_text('1')
        self.producto = None
        #try:
        #    self.ticket = pclases.Ticket.select(orderBy = "-id")[0]
        #except:
        #    self.ticket = None
        self.ticket = None  
            # Prefiero que empiece por uno nuevo, que ya me conozco al 
            # personal y fijo que lo meten todo en el último ticket. Si 
            # quieren segurilo, que le hagan doble clic.
        self.mostrar_info_ticket()
        # Aquí se redefinen algunas señales que interfieren con el movimiento 
        # del foco de los entry que se hace en la clase padre. Desconecto los 
        # "activate" de los entry:
        for w in self.wids.keys():
            if w in self.handlers_id and "activate" in self.handlers_id[w]:
                for h_id in self.handlers_id[w]["activate"]:
                    self.wids[w].disconnect(h_id)
        # Y ahora hago las conexiones que me interesan:
        self.wids['e_precio'].connect("changed", self.actualizar_subtotal)
        self.wids['e_precio'].connect("key_press_event", 
                                      pasar_foco_enter, 
                                      self.wids, 
                                      'b_articulo')
        self.wids['e_cantidad'].connect("changed", self.actualizar_subtotal)
        self.handler_buscador_codigo = self.wids['e_codigo'].connect("changed",
            self.intentar_determinar_producto)
        #self.wids['e_cantidad'].connect("key_press_event", pasar_foco_enter, self.wids['b_articulo'])
        self.wids['e_cantidad'].connect("key_press_event", 
                                        pasar_foco_enter_cantidad, 
                                        self.wids['b_articulo'], 
                                        self.wids['e_codigo'])
        #self.wids['e_codigo'].connect("key_press_event", 
        #                              pasar_foco_enter, 
        #                              self.wids['b_articulo'])
        self.wids['e_codigo'].connect("key_press_event", 
                                      pasar_foco_enter, 
                                      self.wids, 
                                      'e_cantidad') # CWT
        self.wids['e_codigo'].connect("key-release-event", 
                                      self.resaltar_resto_codigo)
        font_desc = pango.FontDescription("Sans Bold 32")
        self.wids['e_total'].modify_font(font_desc)
        font_desc = pango.FontDescription("Sans Bold 24")
        self.wids['e_subtotal'].modify_font(font_desc)
        self.mostrar_tarifa_defecto()
        self.wids['e_codigo'].grab_focus()
        self.wids['b_articulo'].connect("key-press-event", 
            self.pasar_a_cant_si_es_numero)
        #self.wids['e_codigo'].connect("focus-in-event",self.limpiar_si_escape)
        self.wids['b_buscar'].connect("focus-in-event", 
            lambda *args, **kw: self.wids['e_codigo'].grab_focus())
        self._config_boton_descuento()
        try:
            from socket import gethostname
            hostname = gethostname()
            if hostname not in ("nostromo", "melchor", "little-richard"):
                # ¡HARTO de restaurar la ventana en desarrollo!
                self.wids['ventana'].maximize()
        except:
            self.wids['ventana'].maximize()

    def limpiar_si_escape(self, w, e):
        #w.select_region(0,-1)
        #print e.send_event
        pass

    def resaltar_resto_codigo(self, w, e):
        #print e.keyval, e.string
        if e.keyval == 65307:   # Escape
            w.select_region(0, -1)
        else:
            if (self.producto 
               and w.get_text() in self.producto.codigo 
               and e.string):
                pos_fin_anterior = w.get_position()
                w.set_text(self.producto.codigo)
                w.select_region(pos_fin_anterior, -1)

    def pasar_a_cant_si_es_numero(self, w, e):
        # print e.string, e.keyval, gtk.gdk.keyval_name(e.keyval)
        if e.string in [str(i) for i in range(10)]:
            self.wids['e_cantidad'].set_text(e.string)
            self.wids['e_cantidad'].grab_focus()
            self.wids['e_cantidad'].set_position(-1)

    def mostrar_tarifa_defecto(self):
        """
        La tarifa por defecto para el TPV se debe llamar 
        tarifa venta público 
        o 
        tarifa 1
        (aproximadamente) y por este orden de preferencia.
        """
        tarifa = pclases.Tarifa.get_tarifa_defecto()
        if tarifa != None:
            utils.combo_set_from_db(self.wids['cbe_tarifa'], tarifa.id)
        else:
            utils.combo_set_from_db(self.wids['cbe_tarifa'], None)

    def intentar_determinar_producto(self, gtkeditable):
        """
        Intenta localizar el producto buscando el texto del Entry 
        en el código o la descripción. Si encuentra un único resultado 
        lo coloca en ventana.
        """
        if pclases.DEBUG:
            print "    --> tpv:intentar_determinar_producto"
        texto = gtkeditable.get_text()
        # XXX: OPTIMIZACIÓN:    (11/01/2010)
        # ¿Para qué buscar entre tantísimos productos con menos de 3 letras? 
        # Van a aparecer casi todos y consume mucho tiempo de procesador. 
        if len(texto.strip()) >= 3:
        # XXX: EOOPTIMIZACIÓN
            pcs = pclases.ProductoCompra.select(pclases.OR(
                        pclases.ProductoCompra.q.codigo.contains(texto), 
                        pclases.ProductoCompra.q.descripcion.contains(texto)))
            pvs = pclases.ProductoVenta.select(pclases.OR(
                        pclases.ProductoVenta.q.codigo.contains(texto), 
                        pclases.ProductoVenta.q.descripcion.contains(texto)))
            pcscount = pcs.count()
            pvscount = pvs.count()
            if pcscount + pvscount == 1:
                if pcscount == 1:
                    self.producto = pcs[0]
                    self.mostrar_info_producto(machacar_codigo = False)
                elif pvscount == 1:
                    self.producto = pvs[0]
                    self.mostrar_info_producto(machacar_codigo = False)
                else:
                    print "tpv::intentar_determinar_producto -> Error. "\
                          "¡No se pudo determinar si el producto encontrado"\
                          " es PC o PV !"
            else:
                self.producto = None
                self.wids['txt_descripcion'].get_buffer().set_text("")
        if pclases.DEBUG:
            print "    <-- tpv:intentar_determinar_producto"

    def actualizar_subtotal(self, gtkeditable):
        """
        Actualiza el campo subtotal de la ventana con el 
        resultado de multiplicar la cantidad actual por el 
        precio actual.
        Actualiza también el total de compra.
        """
        try:
            cantidad = utils._float(self.wids['e_cantidad'].get_text())
        except (ValueError, TypeError):
            cantidad = 0.0
        try:
            precio = utils._float(self.wids['e_precio'].get_text())
        except (ValueError, TypeError):
            precio = 0.0
        subtotal = cantidad * precio    # (El precio es PVP, ya lleva el IVA)
        dto = self.get_dto()
        subtotal *= (1 - dto)
        self.wids['e_subtotal'].set_text((utils.float2str(subtotal)))
        self.mostrar_totales()

    def activar_ticket(self, tv, path, vc):
        """
        Hace activo el ticket seleccionado.
        """
        if pclases.DEBUG:
            print "    --> activar_ticket"
        model = tv.get_model()
        if model[path].parent != None:
            idticket = model[path].parent[-1]
            idldv = model[path][-1]
            ldv = pclases.LineaDeVenta.get(idldv)
            cantidad = ldv.cantidad
            precio = ldv.precio
            strcantidad = utils.float2str(cantidad, 2, autodec = True)
            self.wids['e_cantidad'].set_text(strcantidad)
            uno_mas_iva = pclases.Ticket.get(idticket).get_iva() + 1
            strprecio = utils.float2str(precio * uno_mas_iva, 2, autodec=True)
            self.wids['e_precio'].set_text(strprecio)
            self.wids['e_descuento'].set_value(100 * ldv.descuento)
            self.producto = ldv.producto
            try:
                ldv.destroySelf()
            except:
                texto = "tpv::activar_ticket -> No se pudo eliminar LDV ID "\
                        "%d al hacerle doble clic para editarla." % (ldv.id)
                self.logger.error(texto)
                print texto
            else:
                actualizar_existencias(self.producto, -cantidad)
        else:
            idticket = model[path][-1]
        self.ticket = pclases.Ticket.get(idticket)
        self.actualizar_ventana(machacar_precio_producto = False)
        if pclases.DEBUG:
            print "    <-- activar_ticket"

    def _wrap_actualizar_ventas(self, func):
        """
        Wrapper para lanzar el _actualizar_ventana (el original) 
        """
        if pclases.DEBUG:
            print "    --> _wrap_actualizar_ventas: ", func.__name__
        gobject.idle_add(func, 
                         priority = gobject.PRIORITY_LOW)
        #func()
        if pclases.DEBUG:
            print "    <-- _wrap_actualizar_ventas"

    def actualizar_ventana(self, boton=None, machacar_precio_producto=True):
        # XXX
        if pclases.DEBUG:
            import time
            inicio = time.time()
        # XXX
        self.comprobar_boton_facturar()
        # XXX
        if pclases.DEBUG:
            print "Tras comprobar botón facturar.", time.time() - inicio
        # XXX
        self.mostrar_info_ticket()
        # XXX
        if pclases.DEBUG:
            print "Tras comprobar datos ticket actual.", time.time() - inicio
        # XXX
        if boton != None:
            #self._rellenar_ultimas_ventas()
            self._wrap_actualizar_ventas(self._rellenar_ultimas_ventas)
            self.wids['e_codigo'].grab_focus()
            # XXX
            if pclases.DEBUG:
                print "Tras rellenar últimas ventas (no opt.).", time.time() - inicio
            # XXX
        else:
            #self.rellenar_ultimas_ventas()
            self._wrap_actualizar_ventas(self.rellenar_ultimas_ventas)
            # XXX
            if pclases.DEBUG:
                print "Tras rellenar últimas ventas (opt.).", time.time() - inicio
            # XXX
        self.mostrar_info_producto(
            machacar_precio_producto = machacar_precio_producto)
        # XXX
        if pclases.DEBUG:
            print "Tras mostrar datos producto.", time.time() - inicio
        # XXX
        self.mostrar_totales()
        # XXX
        if pclases.DEBUG:
            print "Tras mostrar totales.", time.time() - inicio
            print "=== End Of Actualizar_ventana ==="
        # XXX

    def comprobar_boton_facturar(self):
        """
        Comprueba y activa o desactiva el botón de facturar 
        tickets en función de si el usuario tiene permiso para 
        crear nuevas facturas.
        """
        try:
            permiso_facturar = self.usuario.get_permiso(
                pclases.Ventana.selectBy(fichero = "facturas_venta.py")[0])
        except AttributeError:  # Usuario es None o no es un usuario.
            permiso_facturar = False
        puede_facturar = (self.usuario != None and permiso_facturar != None 
                          and permiso_facturar.nuevo)
        if not self.usuario:
            puede_facturar = True # Para pruebas cuando se arranca de consola.
        self.wids['b_facturar'].set_sensitive(puede_facturar)

    def mostrar_totales(self):
        """
        Muestra el subtotal del precio actual por la 
        cantidad actual en pantalla y el total del 
        ticket.
        """
        if self.producto != None:
            try:
                precio = utils._float(self.wids['e_precio'].get_text())
            except ValueError:
                precio = 0.0
            try:
                cantidad = utils._float(self.wids['e_cantidad'].get_text())
            except ValueError:
                cantidad = 0.0
            subtotal = precio * cantidad
        else:
            subtotal = 0.0
        if self.ticket != None:
            total = self.ticket.calcular_total()
            self.wids['e_total'].set_text("%s €" % (utils.float2str(total + subtotal)))
        else:
            self.wids['e_total'].set_text("")

    def mostrar_info_ticket(self):
        """
        Muestra la información del ticket actual en ventana:
        """
        if self.ticket == None:
            self.wids['e_numventa'].set_text("")
            self.wids['e_fecha'].set_text("")
        else:
            self.wids['e_numventa'].set_text(str(self.ticket.numticket))
            self.wids['e_fecha'].set_text("%s - %s" % (
                utils.str_fecha(self.ticket.fechahora), 
                utils.str_hora(self.ticket.fechahora)))

    def _rellenar_ultimas_ventas(self):
        """
        Introduce en el TreeView las ventas de TPV de los últimos días que 
        indique DIAS_TREEVIEW.
        """
        if pclases.DEBUG:
            import time
            inicio = time.time()
            print "    --> _rellenar_ultimas_ventas"
        tickets = pclases.Ticket.select(
            pclases.Ticket.q.fechahora >= 
                (mx.DateTime.localtime() - 
                    (mx.DateTime.oneDay * self.DIAS_TREEVIEW)), 
            orderBy = "-id")
        model = self.wids['tv_ventas'].get_model()
        model.clear()
        self.wids['tv_ventas'].freeze_child_notify()
        self.wids['tv_ventas'].set_model(None)
        for ticket in tickets:
            self.insertar_ticket(ticket, model)
        self.wids['tv_ventas'].set_model(model)
        self.wids['tv_ventas'].thaw_child_notify()
        try:
            self.wids['tv_ventas'].expand_row(model[0].path, False)
        except IndexError:
            pass    # El model está "vacido".
        if pclases.config.get_desplegar_tickets():
            self.wids['tv_ventas'].expand_all() #CWT
        if pclases.DEBUG:
            print "    <-- _rellenar_ultimas_ventas", time.time() - inicio

    def insertar_ticket(self, ticket, model):
        """
        Inserta el ticket recibido en el model del TreeView.
        """
        #totalticket = ticket.calcular_total()
        totalticket = 0.0
        padre = model.append(None, (ticket.numticket, 
                                    utils.str_fecha(ticket.fechahora), 
                                    utils.str_hora(ticket.fechahora),
                                    "", 
                                    "", 
                                    "", 
                                    #"%s €" % (utils.float2str(
                                    #    totalticket)), 
                                    "", 
                                    ", ".join([fra.numfactura for fra 
                                                in ticket.get_facturas()]), 
                                    ticket.id))
        for ldv in ticket.lineasDeVenta:
            totalldv = self.insertar_ldv(ldv, model, padre)
            totalticket += totalldv
        model[padre][5] = "%s €" % utils.float2str(totalticket)

    def insertar_ldv(self, ldv, model, padre):
        """
        Inserta la línea de venta como nodo hijo de «padre» en «model».
        """
        descripcion = ldv.producto.descripcion
        if len(descripcion) > 30:
            descripcion = utils.wrap(descripcion, 30)
        try:
            uno_mas_iva = ldv.ticket.get_iva() + 1
        except AttributeError:
            uno_mas_iva = 1.21
        totalldv = ldv.get_subtotal(iva = False) * uno_mas_iva
        model.append(padre, 
                      ("", 
                       ldv.producto.codigo, 
                       descripcion, 
                       "%s €" % (utils.float2str(ldv.precio * uno_mas_iva 
                                                 * (1 - ldv.descuento))),
                        # P.V.P. lleva 21% de IVA.
                       "%s" % (ldv.descuento 
                               and utils.float2str(ldv.descuento * 100, 
                                                   autodec = True) + "%" 
                               or ""), 
                       "%s" % utils.float2str(ldv.cantidad), 
                       "%s €" % utils.float2str(totalldv),
                        # Ventas de ticket llevan 21% de IVA. 
                        # Lo calculo aquí porque la 
                        # función toma el IVA en función del 
                        # cliente del pedido/albarán/factura.
                       ldv.get_factura_o_prefactura() 
                        and ldv.get_factura_o_prefactura().numfactura 
                        or "", 
                       ldv.id))
        return totalldv

    def rellenar_ultimas_ventas(self):
        """
        Introduce en el TreeView las ventas de TPV de los últimos días (según
        indique el valor de DIAS_TREEVIEW).
        """
        tickets = pclases.Ticket.select(
            pclases.Ticket.q.fechahora >= 
                (mx.DateTime.localtime() - 
                    (mx.DateTime.oneDay * self.DIAS_TREEVIEW)), 
            orderBy = "-id")
        model = self.wids['tv_ventas'].get_model()
        #model.clear()
        fila = 0
        self.wids['tv_ventas'].freeze_child_notify()
        self.wids['tv_ventas'].set_model(None)
        for ticket in tickets:
            try:
                actual_en_model = model[fila]
            except IndexError:
                actual_en_model = None
            if actual_en_model and actual_en_model[-1] == ticket.id:
                totalticket = ticket.calcular_total()
                if "%s €" % utils.float2str(totalticket) == actual_en_model[5]:
                    #ldvs = len(ticket.lineasDeVenta)
                    ldvs = ticket._connection.queryOne(
                        "SELECT COUNT(id) "
                        "FROM linea_de_venta "
                        "WHERE ticket_id = %d" % ticket.id)[0]
                    iter = model.get_iter(fila)
                    en_model = model.iter_n_children(iter)
                    if ldvs == en_model:
                        fila += 1
                        # Si el ID es el mismo, el total también y el número 
                        # de líneas del ticket (importante para precio == 0 o 
                        # cantidad = 0 en la nueva LDV), no lo toco.
                        continue
            self.insertar_ticket_completo(model, fila, actual_en_model, ticket)
            fila += 1
        self.wids['tv_ventas'].set_model(model)
        self.wids['tv_ventas'].thaw_child_notify()
        try:
            self.wids['tv_ventas'].expand_row(model[0].path, False)
        except IndexError:
            pass    # El model está "vacido".
        if pclases.config.get_desplegar_tickets():
            self.wids['tv_ventas'].expand_all() #CWT

    def insertar_ticket_completo(self, model, fila, actual_en_model, ticket):
        """
        Inserta un ticket con sus LDVs en el model en la posición «fila».
        Si actual_en_model != None y tiene el mismo ID que el ticket que 
        queremos insertar, hay que sustituirlo por el ticket nuevo.
        """
        if actual_en_model and actual_en_model[-1] == ticket.id:
            del model[fila]
        totalticket = 0.0
        padre = model.insert(None, 
                             fila, 
                             (ticket.numticket, 
                              utils.str_fecha(ticket.fechahora), 
                              utils.str_hora(ticket.fechahora),
                              "", 
                              "", 
                              "", 
                              "", 
                              ", ".join([fra.numfactura for fra 
                                         in ticket.get_facturas()]), 
                              ticket.id))
        for ldv in ticket.lineasDeVenta:
            descripcion = ldv.producto.descripcion
            if len(descripcion) > 30:
                descripcion = utils.wrap(descripcion, 30)
            try:
                uno_mas_iva = ldv.ticket.get_iva() + 1
            except AttributeError:
                uno_mas_iva = 1.21
            totalldv = ldv.get_subtotal(iva = False) * uno_mas_iva
            model.append(padre, 
                          ("", 
                           ldv.producto.codigo, 
                           descripcion, 
                           "%s €" % (utils.float2str(ldv.precio * uno_mas_iva
                                                     * (1 - ldv.descuento))),
                            # P.V.P. lleva 21% de IVA.
                           "%s" % (ldv.descuento 
                                   and utils.float2str(ldv.descuento * 100, 
                                                       autodec = True) + "%" 
                               or ""), 
                           "%s" % utils.float2str(ldv.cantidad), 
                           "%s €" % utils.float2str(totalldv),
                            # Ventas de ticket llevan 21% de IVA. 
                            # Lo calculo aquí porque la 
                            # función toma el IVA en función del 
                            # cliente del pedido/albarán/factura.
                           ldv.get_factura_o_prefactura() 
                            and ldv.get_factura_o_prefactura().numfactura 
                            or "", 
                           ldv.id))
            totalticket += totalldv
        model[padre][5] = "%s €" % utils.float2str(totalticket)

    def buscar(self, boton):
        """
        Busca un producto por descripción e introduce el código, descripción, 
        precio, etc. en los entries correspondientes
        """
        idtarifa = utils.combo_get_value(self.wids['cbe_tarifa'])
        if idtarifa != None:
            tarifa = pclases.Tarifa.get(idtarifa)
        else:
            tarifa = None
        # self.producto = buscar_producto(padre = self.wids['ventana'], tarifa = tarifa, texto_defecto = self.wids['e_codigo'].get_text())
        productos = utils.buscar_producto_general(padre = self.wids['ventana'], 
                            mostrar_precios = True, 
                            texto_defecto = self.wids['e_codigo'].get_text(), 
                            incluir_sin_iva = False)
        try:
            self.producto = productos[0]
        except (IndexError, TypeError):
            self.producto = None
        if self.producto != None:
            self.mostrar_info_producto()

    def mostrar_info_producto(self, machacar_codigo = True, 
                              machacar_precio_producto = True):
        """
        Coloca el código, descripción y precio en los entries.
        """
        idtarifa = utils.combo_get_value(self.wids['cbe_tarifa'])
        if idtarifa != None:
            tarifa = pclases.Tarifa.get(idtarifa)
        else:
            tarifa = None
        if self.producto != None:
            self.producto.sync()
            codigo = self.producto.codigo
            descripcion = self.producto.descripcion
            if tarifa != None:
                precio = tarifa.obtener_precio(self.producto, 
                         tarifa_defecto = pclases.Tarifa.get_tarifa_defecto())
            else:
                if hasattr(self.producto, "precioPorDefecto"):
                    precio = self.producto.precioPorDefecto
                elif hasattr(self.producto, "precioDefecto"):
                    precio = self.producto.precioDefecto
                else:
                    txt = "%stpv::mostrar_info_producto::No se pudo determinar el precio de: %s" % (self.usuario and self.usuario + ": " or "", self.producto)
                    self.logger.error(txt)
                    print txt
                    precio = 0.0
            hoy = mx.DateTime.localtime()
            if (hoy >= mx.DateTime.DateFrom(2010, 7, 1)
                and hoy <= mx.DateTime.DateFrom(2012, 9, 1)):
                ivahoy = 0.18
            elif hoy < mx.DateTime.DateFrom(2010, 7, 1):
                ivahoy = 0.16
            else:
                ivahoy = 0.21
            uno_mas_iva = 1 + ivahoy
            precio_con_iva = precio * uno_mas_iva
                # En tickets se debe mostrar siempre el P.V.P. con 21% de IVA.
            if (hasattr(self.producto, "controlExistencias") 
                and self.producto.controlExistencias):
                existencias = utils.float2str(self.producto.existencias, 
                                              autodec = True)
            else:
                existencias = "-"
        else:
            codigo = ""
            descripcion = ""
            precio_con_iva = 0
            existencias = "-"
        if machacar_codigo:
            self.wids['e_codigo'].disconnect(self.handler_buscador_codigo)
                # Para que no me machaque el producto actual
            self.wids['e_codigo'].set_text(codigo)
            self.handler_buscador_codigo = self.wids['e_codigo'].connect(
                                "changed", self.intentar_determinar_producto)
        self.wids['txt_descripcion'].get_buffer().set_text(descripcion)
        if machacar_precio_producto:
            self.wids['e_precio'].set_text(utils.float2str(precio_con_iva))
                # Siempre PVP
        self.wids['e_existencias'].set_text(existencias)

    def add_ldv(self, boton):
        """
        Crea una LDV de TPV con el producto, precio y cantidad que están en 
        pantalla.
        Al finalizar, borra la información del producto para introducir el 
        siguiente y pone la cantidad al valor por defecto (1).
        """
        if pclases.DEBUG:
            import time
            inicio = time.time()
        if self.producto != None:
            # XXX
            if pclases.DEBUG:
                print "Tras comprobar producto != None", time.time() - inicio
            # XXX
            if self.ticket == None:
                self.ticket = pclases.Ticket()
                pclases.Auditoria.nuevo(self.ticket, self.usuario, __file__)
                # XXX
                if pclases.DEBUG:
                    print "Tras crear nuevo ticket", time.time() - inicio
                # XXX
            if isinstance(self.producto, pclases.ProductoVenta): 
                productoVenta = self.producto
                productoCompra = None
            elif isinstance(self.producto, pclases.ProductoCompra): 
                productoVenta = None
                productoCompra = self.producto
            # XXX
            if pclases.DEBUG:
                print "Tras determinar tipo de producto.", time.time() - inicio
            # XXX
            try:
                cantidad = utils._float(self.wids['e_cantidad'].get_text())
            except ValueError:
                cantidad = 0.0
            if cantidad > 99999:    # Me aseguro de que no haya metido un 
                cantidad = 1        # código en la cantidad.
            hoy = mx.DateTime.localtime()
            if (hoy >= mx.DateTime.DateFrom(2010, 7, 1)
                and hoy <= mx.DateTime.DateFrom(2012, 9, 1)):
                ivahoy = 0.18
            elif hoy < mx.DateTime.DateFrom(2010, 7, 1):
                ivahoy = 0.16
            else:
                ivahoy = 0.21
            uno_mas_iva = 1 + ivahoy
            try:
                precio = utils._float(self.wids['e_precio'].get_text()) / uno_mas_iva
                # En la LDV no debe llevar IVA.
            except ValueError:
                precio = 0.0
            #descuento = 0.0  # "Impepinablemente" (hasta que se decida otra 
                        # cosa, grrr...), no hay descuentos en ventas de caja.
            descuento = self.get_dto()  # Y llegó el día (BP2).
            # XXX
            if pclases.DEBUG:
                print "Tras determinar cantidad y precio.", time.time() - inicio
            # XXX
            self.producto.sync()
            # XXX
            if pclases.DEBUG:
                print "Tras sincronizar producto.", time.time() - inicio
            # XXX
            if isinstance(self.producto, pclases.ProductoVenta):
                existencias = self.producto.stock
            else:
                existencias = self.producto.existencias
            # XXX
            if pclases.DEBUG:
                print "Tras instanciar existencias.", time.time() - inicio
            # XXX
            if (existencias - cantidad < 0 
                and hasattr(self.producto, "controlExistencias") 
                and self.producto.controlExistencias):
                str_existencias = crear_str_existencias(self.producto)
                #if utils.dialogo(titulo = "EXISTENCIAS INSUFICIENTES", 
                #                 texto = "Existencias de %s: %s.\n\nPulse «sí» para continuar la venta usando %s como cantidad.\nPulse «no» para cancelar." % (self.producto.descripcion, str_existencias, utils.float2str(existencias)), 
                #                 padre = self.wids['ventana']):
                #    cantidad = existencias
                if not utils.dialogo(titulo = "EXISTENCIAS INSUFICIENTES", 
                        texto = "Existencias de %s: %s.\n\nPulse «sí» para "
                                "continuar la venta o «no» para cancelar." % (
                                    self.producto.descripcion, 
                                    str_existencias), 
                    padre = self.wids['ventana']):
                    return
            # XXX
            if pclases.DEBUG:
                print "Tras comprobar existencias suficientes.", \
                      time.time() - inicio
            # XXX
            ldv_existente = None
            for linea in self.ticket.lineasDeVenta:
                if (linea.productoVenta == productoVenta 
                    and linea.productoCompra == productoCompra 
                    and round(linea.precio, 2) == round(precio, 2)): 
                    ldv_existente = linea
                    break
            # XXX
            if pclases.DEBUG:
                print "Tras verificar si actualiza LDV.", time.time() - inicio
            # XXX
            if ldv_existente != None:
                ldv = ldv_existente
                ldv.cantidad += cantidad
                # XXX
                if pclases.DEBUG:
                    print "Tras actualizar cantidad en LDV.", \
                          time.time() - inicio
                # XXX
            else:
                ldv = pclases.LineaDeVenta(productoCompra = productoCompra, 
                                           ticket = self.ticket, 
                                           pedidoVenta = None, 
                                           facturaVenta = None, 
                                           productoVenta = productoVenta, 
                                           albaranSalida = None, 
                                           fechahora = mx.DateTime.localtime(), 
                                           cantidad = cantidad, 
                                           precio = precio, 
                                           descuento = descuento)
                pclases.Auditoria.nuevo(ldv, self.usuario, __file__)
                # XXX
                if pclases.DEBUG:
                    print "Tras crear nueva LDV.", time.time() - inicio
                # XXX
            actualizar_existencias(self.producto, cantidad)
            # XXX
            if pclases.DEBUG:
                print "Tras actualizar existencias en producto.", time.time() - inicio
            # XXX
            self.producto = None
            self.wids['e_cantidad'].set_text("1")
            self.mostrar_tarifa_defecto()
            # XXX
            if pclases.DEBUG:
                print "Tras mostrar la tarifa por defecto.", time.time() - inicio
            # XXX
            self.actualizar_ventana()
            # XXX
            if pclases.DEBUG:
                print "Tras actualizar ventana.", time.time() - inicio
            # XXX
        self.wids['e_codigo'].grab_focus()

    def cerrar_venta(self, boton):
        """
        Cierra la venta, muestra el total e imprime el ticket.
        Si el último producto aún no se ha añadido a la venta, 
        lo introduce antes de cerrarla.
        Muestra en pantalla el siguiente número de venta, que 
        corresponderá a la venta nueva que se inicia.
        """
        if self.producto != None:
            self.add_ldv(None)
        self.abrir_cajon() # TODO: Comprobar que realmente hay cajón, porque 
                            # si no se queda eternamente esperando y cuelga 
                            # el TPV cuando se prueba o cambian tickets en 
                            # oficinas.
        self.mostrar_ventana_total_venta()
        self.ticket = None
        self.producto = None
        self.wids['e_descuento'].set_value(0)
        self.actualizar_ventana()
        self.wids['e_codigo'].grab_focus()

    def mostrar_ventana_total_venta(self):
        if self.ticket == None:
            return
        importe_total = self.ticket.calcular_total()
        dialog = gtk.Dialog("TOTAL DE VENTA TICKET %d" % self.ticket.numticket,
                            self.wids['ventana'],
                            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        total = gtk.Entry()
        font_desc = pango.FontDescription("Sans Bold 32")
        total.modify_font(font_desc)
        total.set_text(self.wids['e_total'].get_text())
        total.set_property("editable", False)
        total.set_property("xalign", 1)
        total.set_property("can-focus", False)

        font_desc16 = pango.FontDescription("Sans Bold 16")
        entregado = gtk.Entry()
        entregado.modify_font(font_desc16)
        entregado.set_property("xalign", 1)
        def actualizar_cambio(gtkeditable = None):
            try:
                v_entregado = utils.parse_float(entregado.get_text())
            except (ValueError, TypeError):
                v_entregado = 0
            importe_cambio = -1 * (importe_total - v_entregado)
            cambio.set_text(utils.float2str(importe_cambio, 2) + " €")
        def atender_teclado(entry, evento):
            boton_aceptar = dialog.action_area.get_children()[0]
            if evento.keyval in (gtk.gdk.keyval_from_name("KP_Enter"), 
                                 gtk.gdk.keyval_from_name("Return")):
                boton_aceptar.clicked()
        entregado.connect("changed", actualizar_cambio)
        entregado.connect("key_press_event", atender_teclado)

        cambio = gtk.Entry()
        cambio.modify_font(font_desc16)
        cambio.set_property("editable", False)
        cambio.set_property("xalign", 1)
        cambio.set_property("can-focus", False)

        table_entregado_cambio = gtk.Table(2, 2)
        table_entregado_cambio.attach(gtk.Label("Entregado: "), 0, 1, 0, 1)
        table_entregado_cambio.attach(entregado, 1, 2, 0, 1)
        table_entregado_cambio.attach(gtk.Label("Cambio: "), 0, 1, 1, 2)
        table_entregado_cambio.attach(cambio, 1, 2, 1, 2)

        vbox_info = gtk.VBox(spacing = 3)
        vbox_info.pack_start(total)
        vbox_info.pack_start(table_entregado_cambio)

        hbox = gtk.HBox(spacing = 5)
        icono = gtk.Image()
        icono.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_DIALOG)
        hbox.pack_start(icono)
        hbox.pack_start(vbox_info)
        dialog.vbox.pack_start(hbox)
        hbox.show_all()
        dialog.set_transient_for(self.wids['ventana'])
        dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        #dialog.action_area.get_children()[0].grab_focus()
        entregado.grab_focus()
        dialog.resize(500, 200)
        dialog.run()
        dialog.destroy()
        

    def chequear_cambios(self):
        pass

    def imprimir(self, boton):
        """
        Imprime un ticket por puerto paralelo y abre el cajón.
        """
        tickets_a_imprimir = []
        if self.wids['tv_ventas'].get_selection().count_selected_rows() != 0: 
            if utils.dialogo(titulo = "IMPRIMIR TICKETS", 
                             texto = "¿Imprimir tickets seleccionados?", 
                             padre = self.wids['ventana']):
                model, paths = self.wids['tv_ventas'].get_selection().get_selected_rows()
                for path in paths:
                    iter = model.get_iter(path)
                    if model[iter].parent == None:  # Es un ticket
                        idticket = model[iter][-1]
                        ticket = pclases.Ticket.get(idticket)
                        tickets_a_imprimir.append(ticket)
                    else:   # Es una LDV
                        idldv = model[iter][-1] 
                        ldv = pclases.LineaDeVenta.get(idldv)
                        ticket = ldv.ticket
                        if ticket != None and ticket not in tickets_a_imprimir:
                            tickets_a_imprimir.append(ticket)
        else:
            num_a_buscar = utils.dialogo_entrada(titulo = "¿NÚMERO DE TICKET?", 
                        texto = "Introduzca el número del ticket a buscar:", 
                        padre = self.wids['ventana'])
            if num_a_buscar != None and num_a_buscar != "":
                try:
                    numticket = int(num_a_buscar)
                    ticket = pclases.Ticket.select(
                                pclases.Ticket.q.numticket == numticket)[0]
                except (IndexError, ValueError):
                    utils.dialogo_info(titulo = "TICKET NO ENCONTRADO", 
                        texto = "El ticket no se encontró o el texto «%s» no"
                                " es un número de ticket válido." % (
                                    num_a_buscar), 
                        padre = self.wids['ventana'])
                else:
                    tickets_a_imprimir.append(ticket)
        for ticket in tickets_a_imprimir:
            try:
                imprimir_ticket(ticket)
            except Exception, msg:
                utils.dialogo_info(titulo = "ERROR IMPRESORA", 
                                   texto = "Ocurrió un error al acceder a la impresora de tickets.\n\nInformación de depuración:\n%s" % msg, 
                                   padre = self.wids['ventana'])

    def abrir_cajon(self, boton = None):
        """
        Abre el cajón portamonedas.
        """
        puerto_lpt = pclases.config.get_puerto_ticketera()
        if pclases.config.get_oki():
            printer = LPTOKI(puerto_lpt)
        else:
            printer = LPT(puerto_lpt)
        try:
            printer.abrir(set_codepage = pclases.config.get_codepageticket())
            printer.abrir_cajon(pclases.config.get_cajonserie())
            printer.cerrar()
        except:
            print "No se pudo operar sobre el cajón/ticketera."

    def cambiar_numventa(self, cell, path, texto):
        """
        Cambia el número del ticket siempre y cuando no exista ya 
        otro ticket con ese número y del mismo año.
        """
        model = self.wids['tv_ventas'].get_model()
        if model[path].parent == None:  # Es un ticket
            try:
                numventa = int(texto)
            except (ValueError, TypeError):
                utils.dialogo_info(titulo = "VALOR INCORRECTO", 
                                   texto = "El texto %s no es un número correcto." % (texto), 
                                   padre = self.wids['ventana'])
            else:
                ticket = pclases.Ticket.get(model[path][-1])
                tickets = pclases.Ticket.select(""" numticket = %d AND date_part('year', fechahora) = %d """ % (numventa, ticket.fechahora.year))
                if tickets.count() > 0:
                    utils.dialogo_info(titulo = "NÚMERO DE TICKET REPETIDO", 
                                       texto = "El ticket %d ya existe en el año %d." % (numventa, ticket.fechahora.year), 
                                       padre = self.wids['ventana'])
                else:
                    ticket.numticket = numventa
                    ticket.sync()
                    model[path][0] = ticket.numticket
                    #self.rellenar_ultimas_ventas()
                    self.mostrar_info_ticket()
                        # Por si han cambiado el número del ticket actual.

    def borrar_venta(self, boton):
        """
        Borra un ticket completo a una línea dependiendo 
        de la selección del TreeView.
        """
        if (self.wids['tv_ventas'].get_selection().count_selected_rows() != 0 
            and utils.dialogo(titulo = "BORRAR TICKETS", 
                              texto = "¿Está seguro de querer borrar las ventas seleccionadas?", 
                              padre = self.wids['ventana'])):
            model, paths = self.wids['tv_ventas'].get_selection().get_selected_rows()
            for path in paths:
                iter = model.get_iter(path)
                if model[iter].parent == None:  # Es un ticket
                    idticket = model[iter][-1]
                    ticket = pclases.Ticket.get(idticket)
                    facturas_ticket = ticket.get_facturas()
                    if facturas_ticket != []:
                        utils.dialogo_info(titulo = "VENTA FACTURADA", 
                                           texto = "La venta ya ha sido facturada en %s.\nElimine primero las facturas antes de cancelar la venta." % ([fra.numfactura for fra in facturas_ticket]))
                    else:
                        for ldv in ticket.lineasDeVenta:
                            actualizar_existencias(ldv.producto, -ldv.cantidad)
                        if ticket == self.ticket:   # Estoy borrando el actual:
                            self.ticket = None
                            self.mostrar_info_ticket()
                        ticket.destroy_en_cascada()
                else:   # Es una LDV
                    idldv = model[iter][-1]
                    try: 
                        ldv = pclases.LineaDeVenta.get(idldv)
                    except:  # Es posible que ya se haya borrado
                        continue
                    if ldv.get_factura_o_prefactura() != None:
                        utils.dialogo_info(titulo = "VENTA FACTURADA", 
                                           texto = "La venta ya ha sido facturada en %s.\nCancele la venta en la factura antes de eliminarla del ticket." % (ldv.get_factura_o_prefactura().numfactura))
                    else:
                        try:
                            producto = ldv.producto
                            cantidad = ldv.cantidad
                            ldv.destroySelf()
                        except Exception, msg:
                            utils.dialogo_info(titulo = "ERROR DE BORRADO", 
                                               texto = "La venta no se pudo eliminar.\nTal vez esté implicada en otras operaciones que impiden su borrado.\n\n\nInformación de depuración:\n%s" % (msg))
                        else:
                            actualizar_existencias(producto, -cantidad)
            self.rellenar_ultimas_ventas()

    # XXX: Código a refactorizar que se usa únicamente para generar la factura. (se repite en al menos 3 ventanas)
    def crear_vencimientos_por_defecto(self, factura):
        """
        Crea e inserta los vencimientos por defecto
        definidos por el cliente en la factura
        actual y en función de las LDV que tenga
        en ese momento (concretamente del valor
        del total de la ventana calculado a partir
        de las LDV.)
        """
        ok = False
        # NOTA: Casi-casi igual al de facturas_venta.py. Si cambia algo 
        # importante aquí, cambiar también allí y viceversa.
        cliente = factura.cliente
        if cliente.vencimientos != None and cliente.vencimientos != '':
            try:
                vtos = cliente.get_vencimientos(factura.fecha)
            except:
                utils.dialogo_info(titulo = 'ERROR VENCIMIENTOS POR DEFECTO', 
                                   texto = 'Los vencimientos por defecto del cliente no se pudieron procesar correctamente.\nVerifique que están bien escritos y el formato es correcto en la ventana de clientes.', 
                                   padre = self.wids['ventana'])
                return ok   # Los vencimientos no son válidos o no tiene.
            self.borrar_vencimientos_y_estimaciones(factura)
            total = self.rellenar_totales(factura)
            numvtos = len(vtos)
            cantidad = total/numvtos
            if not factura.fecha:
                factura.fecha = time.localtime()
            if (cliente.diadepago != None 
               and cliente.diadepago != ''
               and cliente.diadepago.strip() != "-"):
                diaest = cliente.get_dias_de_pago()
            else:
                diaest = False
            for incr in vtos:
                fechavto = factura.fecha + (incr * mx.DateTime.oneDay)
                vto = pclases.VencimientoCobro(fecha = fechavto,
                                               importe = cantidad,
                                               facturaVenta = factura, 
                                               observaciones = factura.cliente and factura.cliente.textoformacobro or "", 
                                               cuentaOrigen = factura.cliente and factura.cliente.cuentaOrigen or None)
                pclases.Auditoria.nuevo(vto, self.usuario, __file__)
                if diaest:
# XXX 24/05/06
                    # Esto es más complicado de lo que pueda parecer a simple vista. Ante poca inspiración... ¡FUERZA BRUTA!
                    fechas_est = []
                    for dia_estimado in diaest:
                        while True:
                            try:
                                fechaest = mx.DateTime.DateTimeFrom(day = dia_estimado, month = fechavto.month, year = fechavto.year)
                                break
                            except:
                                dia_estimado -= 1
                                if dia_estimado <= 0:
                                    dia_estimado = 31
                        if fechaest < fechavto:     # El día estimado cae ANTES del día del vencimiento. 
                                                    # No es lógico, la estimación debe ser posterior.
                                                    # Cae en el mes siguiente, pues.
                            mes = fechaest.month + 1
                            anno = fechaest.year
                            if mes > 12:
                                mes = 1
                                anno += 1
                            try:
                                fechaest = mx.DateTime.DateTimeFrom(day = dia_estimado, month = mes, year = anno)
                            except mx.DateTime.RangeError:
                                # La ley de comercio dice que se pasa al último día del mes:
                                fechaest = mx.DateTime.DateTimeFrom(day = -1, month = mes, year = anno)
                        fechas_est.append(fechaest)
                    fechas_est.sort(utils.cmp_mxDateTime)
                    fechaest = fechas_est[0]
                    vto.fecha = fechaest 
            ok = True
        else:
            utils.dialogo_info(titulo = "SIN DATOS", 
                               texto = "El cliente no tiene datos suficientes para crear vencimientos por defecto.", 
                               padre = self.wids['ventana'])
        return ok
    
    def borrar_vencimientos_y_estimaciones(self, factura):
        for vto in factura.vencimientosCobro:
            vto.factura = None
            vto.destroySelf()
        for est in factura.estimacionesCobro:
            est.factura = None
            est.destroySelf()
    
    def rellenar_totales(self, factura):
        """
        Calcula los totales de la factura a partir de 
        las LDVs, servicios, cargo, descuento y abonos.
        """
        subtotal = self.total_ldvs(factura) + self.total_srvs(factura)
        tot_dto = utils.ffloat(-1 * (subtotal + factura.cargo) * factura.descuento)
        abonos = sum([pa.importe for pa in factura.pagosDeAbono])
        tot_iva = self.total_iva(factura.iva, subtotal, tot_dto, factura.cargo, abonos)
        return self.total(subtotal, factura.cargo, tot_dto, tot_iva, abonos)

    def total(self, subtotal, cargo, dto, iva, abonos):
        return utils.ffloat(subtotal + cargo + dto + iva + abonos)

    def total_iva(self, iva, subtotal, tot_dto, cargo, abonos):
        return utils.ffloat(subtotal + tot_dto + cargo + abonos) * iva

    def total_ldvs(self, factura):
        """
        Total de las líneas de venta. Sin IVA.
        """
        return sum([utils.ffloat((l.cantidad * l.precio) * (1 - l.descuento)) for l in factura.lineasDeVenta])
        
    def total_srvs(self, factura):
        """
        Total de servicios. Sin IVA.
        """
        return sum([utils.ffloat((s.precio * s.cantidad) * (1 - s.descuento)) for s in factura.servicios])
    # XXX: EOCódigo a refactorizar que se usa únicamente para generar la factura. (se repite en al menos 3 ventanas)

    def facturar(self, boton):
        """
        Pide un cliente y crea una factura con los 
        tickets seleccionados.
        Al terminar, pregunta si desea eliminar los 
        tickets o no (CWT: BP lo quiere así porque no 
        quiere separar los tickets facturados a la 
        hora de llevarlos a la gestoría).
        """
        if self.wids['tv_ventas'].get_selection().count_selected_rows() != 0: 
            clientes = [(c.id, c.nombre) 
                        for c in pclases.Cliente.select(
                            pclases.Cliente.q.inhabilitado == False, 
                            orderBy = "nombre")]
            nombrecliente = ""
            while nombrecliente != None and nombrecliente.strip() == "":
                idcliente, nombrecliente = utils.dialogo_entrada_combo(
                    titulo = "SELECCIONE UN CLIENTE", 
                    texto = "Si el cliente no se encuentra en el desplegable, "
                            "teclee el nombre comercial; \nse le pedirá el "
                            "resto de información necesaria para crearlo.", 
                    ops = clientes, 
                    padre = self.wids['ventana'])
            if pclases.DEBUG:
                print "tpv.py::facturar -> idcliente", idcliente
                print "tpv.py::facturar -> nombrecliente", nombrecliente
            if nombrecliente != None and idcliente == None:
                clientes = pclases.Cliente.select(
                    "nombre ILIKE('%%%s%%') "
                    "AND inhabilitado = FALSE " % nombrecliente)
                # Es posible que lo haya escrito en mayúsculas y esté en 
                # la BD en minúsculas, etc.
                if pclases.DEBUG:
                    print "tpv.py::facturar "\
                          "-> clientes.count()", clientes.count()
                if clientes.count() > 0:
                    idcliente = clientes[0].id
                else:
                    idcliente = None
                    if nombrecliente.strip() == "": 
                        utils.dialogo_info(titulo = "NOMBRE VACÍO", 
                            texto = "Debe escribir un nombre para el nuevo "
                                    "cliente.\nVuelva a iniciar el proceso.", 
                            padre = self.wids['ventana'])
                    else:
                        if utils.dialogo(titulo = "¿CREAR NUEVO?", 
                                texto = "El cliente %s no existe, ¿desea "
                                        "crearlo?" % nombrecliente, 
                                padre = self.wids['ventana'], 
                                defecto = True, 
                                tiempo = 10):
                            idcliente = crear_nuevo_cliente(nombrecliente, 
                                                        self.wids['ventana'])
            if idcliente != None:
                cliente = pclases.Cliente.get(idcliente)
                factura = crear_factura(cliente, padre = self.wids['ventana'])
                if factura != None:
                    sel = self.wids['tv_ventas'].get_selection()
                    model, paths = sel.get_selected_rows()
                    ldvs_facturadas = []
                    for path in paths:
                        iter = model.get_iter(path)
                        if model[iter].parent == None:  # Es un ticket
                            idticket = model[iter][-1]
                            ticket = pclases.Ticket.get(idticket)
                            for ldv in ticket.lineasDeVenta:
                                if ldv.get_factura_o_prefactura() == None:
                                    ldv.facturaVenta = factura
                                    ldvs_facturadas.append(ldv)
                                elif ldv.get_factura_o_prefactura() != factura:
                                    txt = "tpv::facturar -> La LDV ID %d "\
                                          "ya está facturada en %s. "\
                                          "No se añadirá a %s." % (
                                            ldv.id, 
                                            ldv.get_factura_o_prefactura()\
                                                .numfactura, 
                                            factura.numfactura)
                                    print txt
                                    self.logger.warning(txt)
                        else:   # Es una LDV
                            idldv = model[iter][-1] 
                            ldv = pclases.LineaDeVenta.get(idldv)
                            if ldv.get_factura_o_prefactura() == None:
                                ldv.facturaVenta = factura
                                ldvs_facturadas.append(ldv)
                            elif ldv.get_factura_o_prefactura() != factura:   # Se acaba de facturar en el bucle de arriba.
                                txt = "tpv::facturar -> La LDV ID %d ya está facturada en %s. No se añadirá a %s." % (ldv.id, ldv.get_factura_o_prefactura().numfactura, factura.numfactura)
                                print txt
                                self.logger.warning(txt)
                    if ldvs_facturadas != []:
                        ok = self.crear_vencimientos_por_defecto(factura)
                        if not ok:
                            import facturas_venta
                            utils.dialogo_info(titulo = "FACTURA CREADA", 
                                               texto = "Se creó con éxito la factura %s.\n\nA continuación se abrirá en una nueva ventana.\nVerifique todos los datos y cree los vencimientos antes de imprimir y bloquear la factura." % (factura.numfactura), 
                                               padre = self.wids['ventana'])
                            ventana = facturas_venta.FacturasVenta(objeto = factura, usuario = self.usuario)
                        else:
                            if utils.dialogo(titulo = "¿COBRAR FACTURA DE %s?" 
                                                % factura.cliente.get_info(), 
                                             texto = "¿Marcar factura como cobrada?\n\nResponda «No» para dejar los vencimientos como pendientes de cobro.\nResponda «Sí» si ha cobrado el importe total de la factura.", 
                                             padre = self.wids['ventana']):
                                # Creo tantos cobros como vencimientos creados:
                                for v in factura.vencimientosCobro:
                                    c = pclases.Cobro(prefactura = None, 
                                                      pagareCobro = None, 
                                                      facturaVenta = factura, 
                                                      facturaDeAbono = None, 
                                                      cliente=factura.cliente, 
                                                      fecha = v.fecha, 
                                                      importe = v.importe, 
                                                      observaciones = "Cobrado al facturar desde TPV.")
                                    pclases.Auditoria.nuevo(c, 
                                                            self.usuario, 
                                                            __file__)
                            if debe_generar_recibo(factura, 
                                                   self.wids['ventana']):
                                generar_recibo(factura, 
                                               self.usuario, 
                                               self.logger, 
                                               self.wids['ventana'])
                            factura.bloqueada = True
                            from informes import mandar_a_imprimir_con_foxit
                            from albaranes_de_salida import imprimir_factura
                            mandar_a_imprimir_con_foxit(
                                imprimir_factura(factura, self.usuario, False))
                            # CWT: 2 copias.
                            mandar_a_imprimir_con_foxit(
                                imprimir_factura(factura, self.usuario, False)) 
                        if utils.dialogo(titulo = "ELIMINAR LÍNEAS FACTURADAS", 
                                         texto = "¿Desea desvincular del TPV las ventas de caja y tickets facturados?", 
                                         padre = self.wids['ventana']):
                            for ldv in ldvs_facturadas:
                                if len(ldv.ticket.lineasDeVenta) == 1:  
                                    # Sólo quedo yo, elimino para que no 
                                    # queden tickets vacíos.
                                    ticket = ldv.ticket
                                    ldv.ticket = None
                                    ticket.destroySelf()
                                ldv.ticket = None
                                if ldv.albaranSalida==ldv.facturaVenta==None:
                                    ldv.destroySelf()
                            #self.actualizar_ventana()
                            #self._rellenar_ultimas_ventas()
                            self.wids['b_actualizar'].clicked()
                    else:
                        utils.dialogo_info(titulo = "NO SE CREÓ LA FACTURA", 
                                           texto = "Todas las líneas seleccionadas ya se encuentran facturadas.\nNo se pueden volver a facturar.", 
                                           padre = self.wids['ventana'])
                        factura.destroySelf()
                    self.actualizar_ventana()

    def arqueo(self, boton):
        """
        Imprime números de ticket y totales de la caja del día seleccionado.
        """
        fecha = utils.mostrar_calendario(padre = self.wids['ventana'])
        fecha = mx.DateTime.DateTimeFrom(*(fecha[::-1]))
        dias = self.wids['sp_dias'].get_value()
        fecha_fin = fecha + (mx.DateTime.oneDay * dias)
        tickets = pclases.Ticket.select(
            pclases.AND(
                pclases.Ticket.q.fechahora >= fecha, 
                pclases.Ticket.q.fechahora < fecha_fin), 
            orderBy = "fechahora")
        #for t in tickets:
        #    print (t.numticket, 
        #           utils.str_fechahora(t.fechahora), 
        #           utils.float2str(t.calcular_total()))
        imprimir_arqueo(tickets)

def crear_factura(cliente, padre = None):
    """
    Crea una factura vacía para el cliente recibido.
    Devuelve None si la factura no se pudo crear.
    """
    factura = None
    try:
        irpf = pclases.DatosDeLaEmpresa.select()[0].irpf
    except (IndexError, AttributeError), msg:
        print "tpv::crear_factura -> No se pudo obtener el IRPF de la empresa"\
              " de la tabla datos_de_la_empresa. Excepción: %s" % (msg)
        irpf = .0
    if cliente.contador == None:
        print "tpv::crear_factura -> El cliente no tiene contador. "\
              "No se creará factura"
        utils.dialogo_info(titulo = "FACTURA NO CREADA", 
            texto = "La factura no se pudo crear por no tener contador el "
                    "cliente %s." % cliente.nombre, 
            padre = padre)
    else:
        try:
            factura = pclases.FacturaVenta(cliente = cliente, 
                        numfactura = cliente.contador.get_next_numfactura(), 
                        fecha = mx.DateTime.localtime(), 
                        descuento = 0.0, 
                        cargo = 0.0, 
                        observaciones = "", 
                        iva = 0.21, 
                        bloqueada = False, 
                        irpf = irpf)
            pclases.Auditoria.nuevo(factura, self.usuario, __file__)
        except Exception, msg:
            factura = None
            print "tpv::crear_factura -> No se pudo crear la factura. "\
                  "Excepción: %s." % msg
        if factura != None:
            # TODO: Quedaría comprobar las restricciones de secuencialidad y 
            # esas cosas y borrar la factura si no las cumpliera.
            cliente.contador.get_and_commit_numfactura()
    return factura

def buscar_producto(padre = None, tarifa = None, texto_defecto = ""):
    """
    Recibe la ventana padre y devuelve una lista de 
    objetos producto de compra o de venta o una lista 
    vacía si no se encuentra.
    Muestra una ventana donde introducir un código, código de 
    Composan, descripción completa o nombre y realiza la 
    búsqueda en las tablas de producto_compra y producto_venta.
    """
    sys.path.append(os.path.join("..", "framework"))
    import pclases
    res = None 
    a_buscar = utils.dialogo_entrada(titulo = "BUSCAR PRODUCTO", 
                                     texto = "Introduzca código o descripción del producto:", 
                                     padre = padre, 
                                     valor_por_defecto = texto_defecto)
    if a_buscar != None:
        productos_compra = utils.buscar_productos_compra(a_buscar)
        productos_venta = utils.buscar_productos_venta(a_buscar)
        resultados = []
        for pc in productos_compra:
            if tarifa != None:
                precio = tarifa.obtener_precio(pc, 
                         tarifa_defecto = pclases.Tarifa.get_tarifa_defecto())
            else:
                precio = pc.precioDefecto
            resultados.append(("PC:%d" % (pc.id), pc.codigo, pc.descripcion, "%s €" % (utils.float2str(precio * 1.21)), "%s %s" % (utils.float2str(pc.existencias), pc.unidad)))
        for pv in productos_venta:
            if tarifa != None:
                precio = tarifa.obtener_precio(pv, 
                         tarifa_defecto = pclases.Tarifa.get_tarifa_defecto())
            else:
                precio = pv.precioDefecto
            resultados.append(("PV:%d" % (pv.id), pv.codigo, pv.descripcion, "%s €" % (utils.float2str(precio * 1.21)), pv.get_str_stock()))
        resultados.sort(func_ordenar_por_item_dos)
        idproducto = utils.dialogo_resultado(resultados, 
                                             "Seleccione un producto:", 
                                             multi = False, 
                                             padre = padre, 
                                             cabeceras = ("ID", 
                                                          "Código", 
                                                          "Descripción", 
                                                          "P.V.P.", 
                                                          "Existencias"))
        if idproducto > 0:
            tipo, id = idproducto.split(":")
            try:
                id = int(id)
            except ValueError:
                res = None
            if tipo == "PC":
                res = pclases.ProductoCompra.get(id)
            elif tipo == "PV":
                res = pclases.ProductoVenta.get(id)
        elif idproducto != -1:
            utils.dialogo_info(titulo = "NO ENCONTRADO", 
                               texto = "No se econtraron productos con la búsqueda %s." % (a_buscar),
                               padre = padre)
    return res

def func_ordenar_por_item_dos(p1, p2):
    """
    Función para ordenar por el segundo elemento de las dos listas recibidas.
    Se usa en la búsqueda de productos para ordenar por descripción.
    Ignora mayúsculas y minúsculas.
    """
    d1 = p1[2].upper()
    d2 = p2[2].upper()
    if d1 < d2:
        return -1
    if d1 > d2:
        return 1
    return 0

def crear_str_existencias(producto):
    """
    Devuelve una cadena con las existencias y unidades del 
    producto recibido.
    """
    res = "?"
    try:
        res = producto.get_str_existencias()
    except AttributeError:
        if isinstance(producto, pclases.ProductoCompra):
            res = "%s %s" % (utils.float2str(producto.existencias), producto.unidad)
        else:
            if hasattr(producto, existencias):
                res = utils.float2str(producto.existencias)
            else:
                print "No sé cómo acceder a las existencias del producto %s" % (producto)
    return res

def actualizar_existencias(producto, cantidad):
    """
    Resta la cantidad recibida a las existencias del producto.
    Si es un producto de venta con artículos... ¿cómo lo hago?
    """
    producto.sync()
    if hasattr(producto, "controlExistencias") and producto.controlExistencias:
        if cantidad != 0:   # Para evitar tráfico innecesario. Si no hay 
                # cambios en las existencias de los productos, no los toco.
            producto.sync()
            if isinstance(producto, pclases.ProductoCompra):
                producto.existencias -= cantidad
                # Ajusto también las existencias del almacén origen.
                almacenorigen = pclases.Almacen.get_almacen_principal()
                producto.add_existencias(-cantidad, almacenorigen)
            elif (isinstance(producto, pclases.ProductoVenta) 
                  and producto.es_especial()):
                try:
                    cantidad_por_bulto = producto.stock / producto.existencias
                    bultos = cantidad / cantidad_por_bulto
                except ZeroDivisionError:
                    bultos = 0
                # TODO: PORASQUI: No hay rastro de las existencias por almacén 
                # en los productos de venta especiales. FUUUUUUUUUUUUUUUU
                producto.camposEspecificosEspecial.stock -= cantidad
                producto.camposEspecificosEspecial.existencias -= int(bultos)
                # TODO: ¿Qué pasa con los bultos en los almacenes?
                producto.camposEspecificosEspecial.sync()
            else:
                # TODO:
                print "No sé cómo descontar existencias de productos de "\
                      "venta con artículos. Debería restar", cantidad
            producto.syncUpdate()
        producto.sync()
    
def imprimir_ticket(ticket):
    """
    Imprime el objeto ticket recibido por el puerto paralelo.
    """
    try:
        dde = pclases.DatosDeLaEmpresa.select()[0]
    except IndexError:
        print "tpv::imprimir_ticket -> No se encontraron los datos de la "\
              "empresa. Abortando impresión..."
    else:
        # ANCHO = 48
        ANCHO = pclases.config.get_anchoticket()
        puerto_lpt = pclases.config.get_puerto_ticketera()
        if pclases.config.get_oki():
            ticketera = LPTOKI(puerto_lpt)
        else:
            ticketera = LPT(puerto_lpt)
        try:
            ticketera.abrir(set_codepage = pclases.config.get_codepageticket())
            linea0 = (" ", "RS")
            linea1 = (dde.nombre.center(ANCHO), "RSC")
            if isinstance(ticketera, LPTOKI):
                modo = ""
            else:
                modo = "RC"
            if pclases.config.get_mostrarcontactoenticket():
                linea2 = (dde.nombreContacto.center(ANCHO), modo)
            else:
                linea2 = ("", "")
            linea3 = (("NIF %s" % (dde.cif)).center(ANCHO), modo)
            linea4 = (("%s. Tlf: %s" % (dde.direccion, dde.telefono)).center(ANCHO), modo)
            linea5 = ("", [])
            lineas = [linea1, linea2, linea3, linea4, linea5]
            lineas.append((("Ticket %d - %s %s" % (
                                ticket.numticket, 
                                utils.str_fecha(ticket.fechahora), 
                                utils.str_hora(ticket.fechahora))
                           ).center(ANCHO), 
                           "SI"))
            for ldv in ticket.lineasDeVenta:
                lineas += split_descuento(ldv, ANCHO)
                 # lineas.append((cortar_linea_ticket(ldv, ANCHO), ">"))
            lineas.append((total_ticket(ticket, ANCHO), "A"))
            lineas.append(("\nIVA incluido - Gracias por su visita", ""))
            for linea, modo in lineas:
                ticketera.escribir(linea, modo)
            for lineas_blanco in range(pclases.config.get_largoticket()):
                ticketera.escribir("", "")
            ticketera.cortar()
        finally:
            ticketera.cerrar()

def imprimir_arqueo(tickets):
    """
    Imprime las "cabeceras" de los tickets recibidos, agrupados por 
    fecha y el total de cada fecha.
    """
    tickets = list(tickets)
    tickets.sort(lambda t1, t2: (t1.fechahora < t2.fechahora and -1) or
                                (t1.fechahora > t2.fechahora and 1) or
                                0)
    dias = {}
    total_totaloso = 0.0
    for t in tickets:
        dia = mx.DateTime.DateTimeFrom(day = t.fechahora.day, 
                                       month = t.fechahora.month, 
                                       year = t.fechahora.year)
        if dia not in dias:
            dias[dia] = [t]
        else:
            dias[dia].append(t)
    ANCHO = pclases.config.get_anchoticket()
    puerto_lpt = pclases.config.get_puerto_ticketera()
    dias_in_orden = dias.keys()
    dias_in_orden.sort()
    if pclases.config.get_oki():
        ticketera = LPTOKI(puerto_lpt)
    else:
        ticketera = LPT(puerto_lpt)
    if pclases.DEBUG:
        from tempfile import gettempdir
        import os
        ticketera = LPT(os.path.join(gettempdir(), "salida_tpv.txt"))
    try:
        try:
            ticketera.abrir(set_codepage = pclases.config.get_codepageticket())
        except IOError, msg:
            utils.dialogo_info(titulo = "ERROR ABRIENDO PUERTO PARALELO", 
                texto = "Ocurrió un error al abrir el puerto paralelo.\n"
                        "Probablemente no cuente con permisos suficientes. "
                        "Contacte con el administrador.") 
            raise IOError, msg
        for dia in dias_in_orden:
            total_dia = 0.0
            linea0 = (" ", "RS")
            linea1 = (utils.str_fecha(dia), "RSC")
            lineas = [linea0, linea1]
            for t in dias[dia]:
                texto = "%d - %s" % (t.numticket, 
                                     utils.str_hora(t.fechahora))
                subtotal = utils.float2str(t.calcular_total())
                texto += " "*(ANCHO - len(texto) - len(subtotal)) + subtotal
                lineas.append((texto, ">"))
                total_dia += t.calcular_total()
            total_totaloso += total_dia
            txt_total = utils.float2str(total_dia)
            linea_total = "TOTAL: %s" % txt_total
            lineas.append((linea_total, "DNA"))
            lineas.append(("", ""))
            for linea, modo in lineas:
                ticketera.escribir(linea, modo)
                if pclases.DEBUG: print linea, modo
        if len(dias.keys()) > 1:
            linea, modo = utils.float2str(total_totaloso), "CANS"
            ticketera.escribir(linea, modo)
            if pclases.DEBUG: print linea, modo
        for lineas_blanco in range(pclases.config.get_largoticket()):
            ticketera.escribir("", "")
        ticketera.cortar()
    finally:
        ticketera.cerrar()

def total_ticket(ticket, ancho):
    """
    Devuelve una cadena con el total del ticket.
    """
    total = "%s Euros" % (utils.float2str(ticket.calcular_total()))
    cad_total = "TOTAL %s" % total
    return "\n" + " " * (ancho - len(cad_total)) + cad_total

def cortar_linea_ticket(ldv, ancho, separador_lineas = ""):
    """
    Devuelve una cadena con la cantidad, producto y subtotal de 
    línea de la línea de venta.
    """
    try:
        uno_mas_iva = ldv.ticket.get_iva() + 1
    except AttributeError:
        uno_mas_iva = 1.21
    IZQ = 5
    DER = 7
    CENDER = 6    # Centro derecha (precio unitario)
    CEN = ancho - IZQ - DER - CENDER - 3
    cant = utils.float2str(ldv.cantidad, 2, autodec = True)
    cant = " " * (IZQ - len(cant)) + cant
    precio = utils.float2str(ldv.precio * uno_mas_iva)
    precio = " " * (CENDER - len(precio)) + precio
    # El descuento va en una línea aparte en el ticket en papel.
    tot = utils.float2str(ldv.get_subtotal(iva = False, 
                                           descuento = False) * uno_mas_iva)
    tot = " " * (DER - len(tot)) + tot
    desc = ldv.producto.descripcion
    lineas = []
    i = 0
    while i < len(desc):
        lineas.append([" " * IZQ, desc[i:i+CEN], " " * CENDER, " " * DER])
        i += CEN
    lineas[0][0] = cant
    lineas[-1][1] = lineas[-1][1] + " " * (CEN - len(lineas[-1][1]))
    lineas[-1][2] = precio
    lineas[-1][3] = tot
    for i in xrange(len(lineas)):
        lineas[i] = "%s %s % s %s" % (lineas[i][0], 
                                      lineas[i][1], 
                                      lineas[i][2], 
                                      lineas[i][3])
    texto = separador_lineas.join(lineas)
    return texto

class LPT:
    def __init__(self, puerto = "/dev/lp0"):
        self.__puerto = puerto
        self.__f = None

    def abrir(self, set_codepage = True):
        """
        Si set_codepage es False no intenta establecer la 
        codificación por defecto para la impresora.
        """
        self.__f = open(self.__puerto, "w")
        if set_codepage:
            character_set = chr(0x1B) + chr(0x52) + chr(11)
            character_set = ""
            codepage = chr(0x1B) + chr(0x47) + chr(2)
            self.__f.write(character_set + codepage)
            self.__f.write("\n")
            self.__f.flush()

    def cortar(self, avanzar = True):
        if avanzar:
            self.avanzar(2)
        texto = chr(0x1B) + chr(0x6D)
        self.__f.write(texto)
        self.__f.write("\n")
        self.__f.flush()

    def abrir_cajon(self, serie = False):
        if not serie:
            #texto = chr(27) + chr(112) + chr(0) + chr(60) + chr(240)
            texto = chr(0x1B) + chr(0x70) + chr(0) + chr(60) + chr(240)
            #texto = chr(0x10) + chr(0x14) + chr(1) + chr(0) + chr(20)
            self.__f.write(texto)
            #self.__f.write("\n")
            self.__f.flush()
        else:
            import serial
            try:
                s = serial.Serial("COM1")
            except:
                s = serial.Serial("/dev/ttyS0")
            s.open()
            s.write("1")    # Cualquier cosa vale para activar el pin.
            s.close()
            del(s)

    def retroceder(self, n = 1):
        for i in xrange(n):
            texto = chr(0x1B) + chr(0x65) + chr(4)
            self.__f.write(texto)
            self.__f.write("\n")
            self.__f.flush()

    def insertar_retorno_de_carro(self):
        """
        Proof of concept. No usar.
        """
        texto = chr(0xA)
        self.__f.write(texto)
        self.__f.flush()

    def avanzar(self, n = 1):
        for i in xrange(n):
            texto = chr(0x1B) + chr(0x64) + chr(1)
            self.__f.write(texto)
            self.__f.write("\n")
            self.__f.flush()

    def _reset_textmode(self):
        "Modos normales para los modos soportados."
        textmode = ""
        textmode += chr(0x1B) + chr(0x61) + chr(0)
        textmode += chr(0x1B) + chr(0x47) + chr(0)
        textmode += chr(0x1B) + chr(0x45) + chr(0)
        textmode += chr(0x1B) + chr(0x2D) + chr(0)
        textmode += chr(0x1D) + "!" + chr(0x00)
        self.__f.write(textmode)
        self.__f.flush()        

    def _reparar_texto(self, t):
        """
        Devuelve el texto con las tildes y eñes reemplazadas 
        por caracteres ascii estándar.
        """
        return t.encode("cp850", "replace")

    def escribir(self, texto, modo = []):
        texto = self._reparar_texto(texto)
        textmode = ""
        if "R" in modo or "r" in modo:      # Resaltado
            textmode += chr(0x1B) + chr(0x45) + chr(1)
        else:
            textmode += chr(0x1B) + chr(0x45) + chr(0)
        if "N" in modo or "n" in modo:      # Negrita (doble resaltado)
            textmode += chr(0x1B) + chr(0x47) + chr(1)
        else:
            textmode += chr(0x1B) + chr(0x47) + chr(0)
        if "S" in modo or "s" in modo:      # Subrayado
            textmode += chr(0x1B) + chr(0x2D) + chr(1)
        else:
            textmode += chr(0x1B) + chr(0x2D) + chr(0)
        if "A" in modo or "a" in modo:      # Ancho (caracteres doble de ancho)
            textmode += chr(0x1D) + "!" + chr(0x11)
        else:
            textmode += chr(0x1D) + "!" + chr(0x00)
        if "I" in modo or "i" in modo:      # Texto justificado a la izquierda
            textmode += chr(0x1B) + chr(0x61) + chr(0)
            texto = texto.strip()   # No tienen sentido los espacios 
                # adicionales si la máquina lo va a justificar en el papel 
                # antes de imprimir la línea.
        if "C" in modo or "c" in modo:      # Texto centrado
            textmode += chr(0x1B) + chr(0x61) + chr(1)
            texto = texto.strip()   # No tienen sentido los espacios 
                # adicionales si la máquina lo va a centrar en el papel 
                # antes de imprimir la línea.
        if "D" in modo or "d" in modo:      # Texto justificado a la derecha
            textmode += chr(0x1B) + chr(0x61) + chr(2)
            texto = texto.strip()   # No tienen sentido los espacios 
                # adicionales si la máquina lo va a justificar en el papel 
                # antes de imprimir la línea.
        if not modo:
            textmode += chr(0x1B) + chr(0x61) + chr(0)
            textmode += chr(0x1B) + chr(0x47) + chr(0)
            textmode += chr(0x1B) + chr(0x45) + chr(0)
            textmode += chr(0x1B) + chr(0x2D) + chr(0)
            textmode += chr(0x1D) + "!" + chr(0x00)
        # Empezamos con los casos especiales. Si el modo es ">" el texto 
        # va con tipografía normal excepto la última palabra que va en negrita.
        if ">" in modo:
            self._reset_textmode()
            textmode = ""
            normal = chr(0x1B) + chr(0x47) + chr(0)
            negrita = chr(0x1B) + chr(0x47) + chr(1)
            hasta_ultimo_espacio = texto[:texto.rindex(" ")]
            ultima_palabra = texto[texto.rindex(" "):]
            texto = normal + hasta_ultimo_espacio + negrita + ultima_palabra
        self.__f.write(textmode + texto)
        self.__f.write("\n")
        self.__f.flush()
        #print(texto)

    def cerrar(self):
        try:
            self.__f.close()
        except AttributeError, msg:
            print "No se pudo cerrar el puerto porque probablemente no estaba abierto. AttributeError: %s" % (msg)

class LPTOKI(LPT):
    def __init__(self, puerto = "/dev/lp0"):
        self.__puerto = puerto
        self.__f = None

    def abrir(self, set_codepage = True):
        """
        Si set_codepage es False no intenta establecer la 
        codificación por defecto para la impresora.
        """
        self.__f = open(self.__puerto, "w")
        if set_codepage:
            codepage = chr(0x1B) + chr(0x1D) + chr(0x74) + chr(4)
            character_set = chr(0x1B) + chr(0x52) + chr(7)
            self.__f.write(character_set + codepage)
            self.__f.write("\n")
            self.__f.flush()

    def cortar(self, avanzar = True):
        if avanzar:
            self.avanzar(4)
        self.__f.write("\n")
        self.__f.flush()

    def abrir_cajon(self, serie = False):
        if not serie:
            texto = chr(0x1c) + chr(0x07) + chr(20) + chr(20)
            self.__f.write(texto)
            self.__f.flush()
        else:
            import serial
            try:
                s = serial.Serial("COM1")
            except:
                s = serial.Serial("/dev/ttyS0")
            s.open()
            s.write("1")    # Cualquier cosa vale para activar el pin.
            s.close()
            del(s)

    def retroceder(self, n = 1):
        self.__f.flush()

    def avanzar(self, n = 1):
        for i in xrange(n):
            texto = chr(0x1B) + chr(0x64) + chr(1)
            self.__f.write(texto)
            self.__f.write("\n")
            self.__f.flush()

    def _reset_textmode(self):
        "Modos normales para los modos soportados."
        textmode = ""
        textmode += chr(0x1B) + chr(0x4D)   # Fuente 7x9 (half dots).
        textmode += chr(0x14) # Cancela impresión expandida.
        textmode += chr(0x1B) + chr(0x68) + chr(0)  # Cancela altura doble.
        textmode += chr(0x1B) + chr(0x46) # Cancela negritas.
        textmode += chr(0x1B) + chr(0x2D) + chr(0) # Cancela subrayado.
        self.__f.write(textmode)
        self.__f.flush()        

    def _reparar_texto(self, t):
        """
        Devuelve el texto con las tildes y eñes reemplazadas 
        por caracteres ascii estándar.
        """
        return t.encode("cp850", "replace")

    def escribir(self, texto, modo = []):
        texto = self._reparar_texto(texto)
        textmode = ""
        if "R" in modo or "r" in modo:      # Resaltado (ancho doble)
            textmode += chr(0x1B) + chr(0x57) + chr(1)
        else:
            textmode += chr(0x1B) + chr(0x57) + chr(0)
        if "N" in modo or "n" in modo:      # Negrita (doble resaltado)
            textmode += chr(0x1B) + chr(0x45) 
        else:
            textmode += chr(0x1B) + chr(0x46) 
        if "S" in modo or "s" in modo:      # Subrayado
            textmode += chr(0x1B) + chr(0x2D) + chr(1)
        else:
            textmode += chr(0x1B) + chr(0x2D) + chr(0)
        if "A" in modo or "a" in modo:      # Ancho (caracteres doble de alto)
            textmode += chr(0x1B) + chr(0x68) + chr(1)
        else:
            textmode += chr(0x1B) + chr(0x68) + chr(0) 
        if "I" in modo or "i" in modo:      # Texto justificado a la izquierda
            textmode += chr(0x1B) + chr(0x1d) + chr(0x61) + chr(0)
            texto = texto.strip()   # No tienen sentido los espacios 
                # adicionales si la máquina lo va a justificar en el papel 
                # antes de imprimir la línea.
        if "C" in modo or "c" in modo:      # Texto centrado
            textmode += chr(0x1B) + chr(0x1d) + chr(0x61) + chr(1)
            texto = texto.strip()   # No tienen sentido los espacios 
                # adicionales si la máquina lo va a centrar en el papel 
                # antes de imprimir la línea.
        if "D" in modo or "d" in modo:      # Texto justificado a la derecha
            textmode += chr(0x1B) + chr(0x1d) + chr(0x61) + chr(2)
            texto = texto.strip()   # No tienen sentido los espacios 
                # adicionales si la máquina lo va a justificar en el papel 
                # antes de imprimir la línea.
        if not modo:
            textmode += chr(0x1B) + chr(0x68) + chr(0) 
            textmode += chr(0x1B) + chr(0x46) 
            textmode += chr(0x1B) + chr(0x2D) + chr(0)
            textmode += chr(0x1B) + chr(0x57) + chr(0)
        # Empezamos con los casos especiales. Si el modo es ">" el texto 
        # va con tipografía normal excepto la última palabra que va en negrita.
        if ">" in modo:
            self._reset_textmode()
            textmode = ""
            normal = chr(0x1B) + chr(0x46)
            negrita = chr(0x1B) + chr(0x45)
            hasta_ultimo_espacio = texto[:texto.rindex(" ")]
            ultima_palabra = texto[texto.rindex(" "):]
            texto = normal + hasta_ultimo_espacio + negrita + ultima_palabra
        self.__f.write(textmode + texto)
        self.__f.write("\n")
        self.__f.flush()
        #print(texto)

    def cerrar(self):
        try:
            self.__f.close()
        except AttributeError, msg:
            print "No se pudo cerrar el puerto porque probablemente no estaba abierto. AttributeError: %s" % (msg)

def pasar_foco_enter_cantidad(widget, event, boton, entry):
    """
    TODO: Falta docstring.
    """
    if event.keyval == 65293 or event.keyval == 65421:
        boton.clicked()
        entry.grab_focus()

def pasar_foco_enter(widget, event, wids, destino):
    """
    Pasa el foco al widget destino.
    """
    if event.keyval == 65293 or event.keyval == 65421:
        destino = wids[destino]    # Para evitar:
        # <gtk.Entry object at 0x1473aa0 (uninitialized at 0x0)>
        destino.grab_focus() 

def dialogo_nuevo_cliente(nombre, padre = None):
    # TODO: PORASQUI: No se comprueba que el CIF del cliente sea válido.
    res = [None]
    de = gtk.Dialog("DATOS DEL CLIENTE",
                    padre,
                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                    (gtk.STOCK_OK, gtk.RESPONSE_OK,
                     gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
    #-----------------------------------------------------------#
    def _respuesta_ok_cancel(dialog, response, res):
        if response == gtk.RESPONSE_OK:
            valores = []
            tabla_valores = dialog.vbox.get_children()[1]
            for hijo in tabla_valores.get_children():
                if isinstance(hijo, gtk.Entry):
                    entry = hijo
                    valores.append(entry.get_text())
            res[0] = valores.pop(0)
            for v in valores:
                res.append(v)
        else:
            res[0] = False
    #-----------------------------------------------------------#
    de.connect("response", _respuesta_ok_cancel, res)
    txt = gtk.Label("Introduzca los datos del nuevo cliente:")
    hbox = gtk.HBox(spacing = 5)
    icono = gtk.Image()
    icono.set_from_stock(gtk.STOCK_DIALOG_QUESTION, gtk.ICON_SIZE_DIALOG)
    hbox.pack_start(icono)
    hbox.pack_start(txt)
    de.vbox.pack_start(hbox)
    hbox.show_all()

    tabla = gtk.Table(7, 2)
    tabla.attach(gtk.Label("Nombre: "), 0, 1, 0, 1)
    tabla.attach(gtk.Label("CIF: "), 0, 1, 1, 2)
    tabla.attach(gtk.Label("Dirección: "), 0, 1, 2, 3)
    tabla.attach(gtk.Label("Código postal: "), 0, 1, 3, 4)
    tabla.attach(gtk.Label("Ciudad: "), 0, 1, 4, 5)
    tabla.attach(gtk.Label("Provincia: "), 0, 1, 5, 6)
    tabla.attach(gtk.Label("País: "), 0, 1, 6, 7)
    tabla.attach(gtk.Entry(), 1, 2, 0, 1)
    tabla.get_children()[0].set_text(nombre) # La lista de get_children es LIFO.
    tabla.attach(gtk.Entry(), 1, 2, 1, 2)
    tabla.attach(gtk.Entry(), 1, 2, 2, 3)
    tabla.attach(gtk.Entry(), 1, 2, 3, 4)
    tabla.attach(gtk.Entry(), 1, 2, 4, 5)
    tabla.get_children()[0].set_text("Huelva")
    tabla.attach(gtk.Entry(), 1, 2, 5, 6)
    tabla.get_children()[0].set_text("Huelva")
    tabla.attach(gtk.Entry(), 1, 2, 6, 7)
    tabla.get_children()[0].set_text("España")

    de.vbox.pack_start(tabla)
    tabla.show_all()
    de.set_transient_for(padre)
    de.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
    de.run()
    de.destroy()
    if res[0]==False:
        return None
    return res[::-1]

def crear_nuevo_cliente(nombre, padre = None):
    """
    Recibe un nombre y pide el resto de datos para 
    crear un nuevo cliente.
    Devuelve el id del cliente creado o None si se 
    cancela.
    «padre» es la ventana padre para los diálogos.
    """
    idcliente = None
    res = dialogo_nuevo_cliente(nombre, padre)
    if res != None:
        try:
            nombre, cif, direccion, cp, ciudad, provincia, pais = map(
                lambda x: x.strip(), res)
        except:
            nombre = None
        if nombre:
            parecidos, sugerencia = buscar_clientes_parecidos(nombre)
            if parecidos.count():
                cliente = seleccionar_parecido(parecidos, nombre, sugerencia,  
                                               ventana_padre = padre)
                if cliente == -1:
                    cliente = None
                else:
                    idcliente, cliente = cliente, pclases.Cliente.get(cliente)
            else:
                cliente = None
            if not cliente:
                contadores = pclases.Contador.select(orderBy = "-id")
                if contadores.count():
                    contador = contadores[0]
                else:
                    contador = None
                try:
                    cliente = pclases.Cliente(nombre = nombre,
                                              tarifaID = None,
                                              contador = contador,
                                              telefono = '',
                                              cif = cif,
                                              direccion = direccion,
                                              pais = pais,
                                              ciudad = ciudad,
                                              provincia = provincia,
                                              cp = cp,
                                              vencimientos = "0",
                                              iva = 0.21,
                                              direccionfacturacion = direccion,
                                              nombref = nombre,
                                              paisfacturacion = pais,
                                              ciudadfacturacion = ciudad,
                                              provinciafacturacion = provincia,
                                              cpfacturacion = cp,
                                              email = '',
                                              contacto = '',
                                              observaciones="Creado desde el TPV.",
                                              documentodepago = "",
                                              diadepago = '',
                                              formadepago = '0',
                                              inhabilitado = False, 
                                              porcentaje = 0.0, 
                                              clienteID = None, 
                                              enviarCorreoAlbaran = False, 
                                              enviarCorreoFactura = False, 
                                              enviarCorreoPacking = False, 
                                              fax = '', 
                                              riesgoAsegurado = -1, 
                                              riesgoConcedido = -1)
                    pclases.Auditoria.nuevo(cliente, self.usuario, __file__)
                    idcliente = cliente.id
                except Exception, msg: # CIF duplicado o cualquier historia así.
                    utils.dialogo_info(titulo = "ERROR", 
                        texto = "Se produjo un error al crear el cliente:"
                                "\n\n%s" % msg,
                        padre = padre)
    else:
        idcliente = None
    return idcliente 

def buscar_clientes_parecidos(nombre, ventana_padre = None):
    """
    Busca clientes con nombre parecido al recibido y devuelve un ResultSelect.
    """
    try:
        import spelling
    except ImportError:
        sys.path.append(os.path.join("..", "utils"))
        import spelling
    nombres = ""
    for cliente in pclases.Cliente.selectBy(inhabilitado = False):
        nombres += cliente.nombre + "\n"
    corrector = spelling.SpellCorrector(nombres)
    nombre_encontrado = corrector.correct(nombre)
    res = pclases.Cliente.select(
            pclases.Cliente.q.nombre.contains(nombre_encontrado))
    return res, nombre_encontrado

def seleccionar_parecido(clientes, buscado, sugerido, ventana_padre = None):
    """
    Muestra la lista de clientes en ventana y devuelve el seleccionado por 
    el usuario.
    """
    resultados = []
    for c in clientes:
        resultados.append((c.id, c.nombre, c.cif, c.get_direccion_completa(), 
                           c.telefono, c.observaciones))
    texto = "Buscó «%s», pero se encontraron %d resultados para «%s».\n"\
            "¿Se refería tal vez a alguno de estos clientes?\n"\
            "Seleccione uno de ellos si es el caso o cancele\n"\
            "para crear uno nuevo como «%s»." % (
                buscado, len(resultados), sugerido, buscado)
    cliente = utils.dialogo_resultado(resultados, 
                                      texto = texto, 
                                      multi = False, 
                                      padre = ventana_padre, 
                                      cabeceras = ("ID", 
                                                   "Nombre", 
                                                   "CIF", 
                                                   "Dirección", 
                                                   "Teléfono", 
                                                   "Observaciones"))
    return cliente


# XXX: Creo el almacén principal si no existe o no lo he creado yo en la 
#      actualización de algún cliente.
check_almacen()

if __name__ == '__main__':
    #pclases.DEBUG = True
    t = TPV()


