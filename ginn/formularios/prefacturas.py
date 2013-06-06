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
## prefacturas.py - Ventana de facturas proforma (ventas) 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 8 de noviembre de 2005 -> Inicio
## 
###################################################################

from albaranes_de_salida import ajustar_existencias
from framework import pclases
from informes import geninformes
from utils import ffloat, _float as float
from ventana import Ventana
import gtk
import time
import mx.DateTime
from formularios import postomatic
import pygtk
from formularios import utils
pygtk.require('2.0')
try:
    from psycopg import ProgrammingError as psycopg_ProgrammingError
except ImportError:
    from psycopg2 import ProgrammingError as psycopg_ProgrammingError

def buscar_cuentaOrigen(nombre, ventana_padre = None):
    """
    Busca un cuentaOrigen por su nombre. Si no lo encuentra solo con el 
    parámetro recibido o si encuentra más de uno, muestra una ventana 
    con los resultados para que el usuario elija uno de ellos.
    Devuelve el cuentaOrigen seleccionado o None.
    """
    cuentaOrigen = None
    cuentaOrigenes = pclases.CuentaOrigen.select(pclases.OR(pclases.CuentaOrigen.q.nombre.contains(nombre), 
                                                            pclases.CuentaOrigen.q.banco.contains(nombre), 
                                                            pclases.CuentaOrigen.q.ccc.contains(nombre)))
    numresultados = cuentaOrigenes.count()
    if numresultados == 0:
        cuentaOrigenes = pclases.CuentaOrigen.select()
    if numresultados != 1:
        filas_res = [(p.id, p.nombre, p.banco, p.ccc, p.observaciones) for p in cuentaOrigenes]
        idcuentaOrigen = utils.dialogo_resultado(filas_res,
                                                 titulo = 'Seleccione cuenta',
                                                 cabeceras = ('ID', 'Nombre', 'Banco', 'C.C.C.', 'Observaciones'),  
                                                 padre = ventana_padre) 
        if idcuentaOrigen > 0:
            cuentaOrigen = pclases.CuentaOrigen.get(idcuentaOrigen)
    elif numresultados == 1:
        cuentaOrigen = cuentaOrigenes[0]
    return cuentaOrigen
    

class Prefacturas(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self._objetoreciencreado = None
        Ventana.__init__(self, 'facturas_venta.glade', objeto, usuario = self.usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_nuevo/clicked': self.crear_nueva_factura,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_buscar/clicked': self.buscar_factura,
                       'b_fecha/clicked': self.cambiar_fecha,
                       'b_numfactura/clicked': self.cambiar_numfactura,
                       'b_borrar/clicked': self.borrar_factura,
                       'b_add_src/clicked': self.add_src,
                       'b_drop_ldv/clicked': self.drop_ldv,
                       'b_add_ldv/clicked': self.add_nueva_ldv,
                       'b_add_vto/clicked': self.add_vto,
                       'b_drop_vto/clicked': self.drop_vto,
                       'b_crear_servicio/clicked': self.add_srv,
                       'b_clonar_servicio/clicked': self.clon_srv,
                       'b_drop_servicio/clicked': self.drop_srv,
                       'b_imprimir/clicked': self.imprimir,
                       'b_vtos_defecto/clicked': self.crear_vencimientos_por_defecto,
                       'b_abonos/clicked': self.buscar_abonos,
                       'b_drop_abono/clicked': self.drop_abono
                      }  
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        gtk.main()


    # --------------- Funciones auxiliares ------------------------------
    def es_diferente(self):
        """
        Devuelve True si la información en pantalla es distinta a la
        del objeto en memoria.
        """
        factura = self.objeto
        if factura == None: return False    # Si no hay factura activo, devuelvo que no hay cambio respecto a la ventana
        condicion = factura.numfactura == self.wids['e_numfactura'].get_text()
        condicion = condicion and (factura.bloqueada == self.wids['ch_bloqueada'].get_active())
        condicion = condicion and (factura.observaciones == self.wids['e_observaciones'].get_text())
        condicion = condicion and (utils.str_fecha(factura.fecha) == self.wids['e_fecha'].get_text())
        try:
            condicion = condicion and (utils.parse_porcentaje(self.wids['e_descuento'].get_text())/100.0 == factura.descuento)
            condicion = condicion and (utils.parse_porcentaje(self.wids['e_iva'].get_text(), fraccion = True) == factura.iva)
            condicion = condicion and (utils.parse_porcentaje(self.wids['e_irpf'].get_text(), fraccion = True) == factura.irpf)
        except ValueError, msg:
            self.logger.error("prefacturas.py::es_diferente -> Error, probablemente al parsear pordentaje: %s" % (msg))
        return not condicion    # Condición verifica que sea igual

    def aviso_actualizacion(self):
        """
        Muestra una ventana modal con el mensaje de objeto 
        actualizado.
        """
        utils.dialogo_info('ACTUALIZAR',
                           'La factura ha sido modificada remotamente.\nDebe actualizar la información mostrada en pantalla.\nPulse el botón «Actualizar»',
                           padre = self.wids['ventana'])
        self.wids['b_actualizar'].set_sensitive(True)

    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        self.wids['hbox_obra'].set_property("visible", False)
        self.wids['ventana'].set_title("Prefacturas")
        self.wids['label1'].set_text("<b><u>Pre</u>factura nº: </b>")
        self.wids['label1'].set_use_markup(True)
        # Inicialmente no se muestra NADA. Sólo se le deja al
        # usuario la opción de buscar o crear nuevo.
        self.activar_widgets(False)
        self.wids['b_actualizar'].set_sensitive(False)
        self.wids['b_guardar'].set_sensitive(False)
        self.wids['b_nuevo'].set_sensitive(True)
        self.wids['b_buscar'].set_sensitive(True)
        # Inicialización del resto de widgets:
        cols = (('Código', 'gobject.TYPE_STRING', False, True, False, None),
                ('Descripción', 'gobject.TYPE_STRING', False, True, False, None),
                ('Descripción complementaria', 'gobject.TYPE_STRING', True, True, False, self.cambiar_descripcion_complementaria), 
                ('Cantidad', 'gobject.TYPE_DOUBLE', True, True, False, self.cambiar_cantidad_ldv),
                ('Precio', 'gobject.TYPE_STRING', True, True, False, self.cambiar_precio),
                ('Dto. (%)', 'gobject.TYPE_STRING', True, True, False, self.cambiar_descuento),
                ('Total de línea', 'gobject.TYPE_DOUBLE', False, True, False, None),
                ('Albarán Nº', 'gobject.TYPE_STRING', False, True, False, None),
                ('Pedido Nº', 'gobject.TYPE_STRING', False, True, False, None),
                ('IDLDV', 'gobject.TYPE_INT64', False, True, False, None)
               )
        utils.preparar_listview(self.wids['tv_ldvs'], cols)
        postomatic.attach_menu_notas(self.wids['tv_ldvs'], pclases.LineaDeVenta, self.usuario, 1)
        cols = (('Código', 'gobject.TYPE_STRING', True, True, False, None),
                ('Descripción', 'gobject.TYPE_STRING', False, True, False, None),
                ('Cantidad', 'gobject.TYPE_STRING', False, True, False, None),
                ('Precio', 'gobject.TYPE_STRING', False, True, False, None),
                ('Descuento', 'gobject.TYPE_STRING', False, True, False, None),
                ('Total de línea', 'gobject.TYPE_STRING', False, True, False, None),
                ('Pedido', 'gobject.TYPE_STRING', False, True, False, None),
                ('Albarán', 'gobject.TYPE_STRING', False, True, False, None),
                ('IDLDV', 'gobject.TYPE_INT64', False, False, False, None)
               )
        utils.preparar_treeview(self.wids['tv_srcs'], cols)
        postomatic.attach_menu_notas(self.wids['tv_srcs'], pclases.LineaDeVenta, self.usuario, 1)
        for col in self.wids['tv_srcs'].get_columns():
            col.connect("clicked", self.cambiar_columna_busqueda)
        self.wids['tv_srcs'].get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        cols = (('Vencimiento', 'gobject.TYPE_STRING', True, True, True, self.cambiar_vto),
                ('Cantidad', 'gobject.TYPE_DOUBLE', True, True, False, self.cambiar_cantidad),
                ('Forma de pago', 'gobject.TYPE_STRING', True, True, False, self.cambiar_observaciones_vto),
                ('Cuenta', 'gobject.TYPE_STRING', True, True, False, self.cambiar_cuenta_transferencia),
                ('Cobrado', 'gobject.TYPE_BOOLEAN', False, True, False, None),
                ('Fecha cobro', 'gobject.TYPE_STRING', True, True, False, self.cambiar_cobro),
                ('Importe del cobro', 'gobject.TYPE_DOUBLE', True, True, False, self.cambiar_importe_cobro),
                ('Forma de cobro', 'gobject.TYPE_STRING', True, True, False, self.cambiar_observaciones),
                ('IDs', 'gobject.TYPE_STRING', False, False, False, None)
               )
                # HACK: La última columna -oculta- va a tener una cadena con los IDs 
                #       involucrados en la fila separados por coma y como cadena para
                #       aprovechar el preparar_listview sin tener que cambiar nada.
        utils.preparar_listview(self.wids['tv_vencimientos'], cols)
        #-----------------------------------------------------------------------------------------------#
        def comprobar_que_no_me_hace_el_gato(paned, scrolltype_or_allocation_or_requisition = None):    #
            MIN = 109                                                                                   #
            MAX = 720                                                                                   #
            posactual = paned.get_position()                                                            #
            if posactual < MIN:                                                                         #
                paned.set_position(MIN)                                                                 #
            elif posactual > MAX:                                                                       #
                paned.set_position(MAX)                                                                 #
        #-----------------------------------------------------------------------------------------------#
        self.wids['hpaned1'].connect("size_request", comprobar_que_no_me_hace_el_gato)
        cols = (('Cantidad', 'gobject.TYPE_DOUBLE', True, True, False, self.cambiar_cantidad_srv),
                ('Concepto', 'gobject.TYPE_STRING', True, True, True, self.cambiar_concepto_srv),
                ('Precio', 'gobject.TYPE_DOUBLE', True, True, False, self.cambiar_precio_srv),
                ('Descuento', 'gobject.TYPE_DOUBLE', True, True, False, self.cambiar_descuento_srv),
                ('Total', 'gobject.TYPE_DOUBLE', False, True, False, None),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_servicios'], cols)
        postomatic.attach_menu_notas(self.wids['tv_servicios'], pclases.Servicio, self.usuario, 1)
        cols = (('Nº Abono', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Importe', 'gobject.TYPE_DOUBLE', False, True, False, None),
                ('ID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(self.wids['tv_abonos'], cols)
        self.wids['e_subtotal'].set_alignment(1.0)
        self.wids['e_cargo'].set_alignment(1.0)
        self.wids['e_total_iva'].set_alignment(1.0)
        self.wids['e_total_irpf'].set_alignment(1.0)
        self.wids['e_tot_dto'].set_alignment(1.0)
        self.wids['e_total'].set_alignment(1.0)
        try:
            if pclases.DatosDeLaEmpresa.select()[0].irpf != 0.0:
                self.wids['label36'].set_property("visible", True)
                self.wids['e_irpf'].set_property("visible", True)
                self.wids['e_total_irpf'].set_property("visible", True)
        except (IndexError, AttributeError), msg:
            self.logger.error("prefacturas::inicializar_ventana -> No se encontraron los datos de la empresa. Excepción: %s" % (msg))

    def cambiar_columna_busqueda(self, treeviewcolumn): 
        cols = self.wids['tv_srcs'].get_columns()
        numcols = len(cols)
        numcolumn = 0
        col = self.wids['tv_srcs'].get_column(0)
        while numcolumn < numcols and col != treeviewcolumn:
            numcolumn += 1
            col = self.wids['tv_srcs'].get_column(numcolumn)
        self.wids['tv_srcs'].set_search_column(numcolumn)

    def activar_widgets(self, s):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        if (self.objeto 
            and self.objeto.bloqueada 
            and self.usuario 
            and self.usuario.nivel >= 3):
            s = False
        ws = ('hbox1', 'hbox5', 'alignment4', 'hbox_observaciones', 'hpaned1', 
              #'expander1', 
              'b_borrar', 
              # 'expander2', 
              'frame4')
        for w in ws:
            self.wids[w].set_sensitive(s)
        if (self.objeto 
            and self.objeto.bloqueada 
            and self.usuario 
            and self.usuario.nivel <= 2):
            # Si el usuario tiene nivel 2 y permiso sobre la ventana (si ha 
            # podido abrirla es que sí), le dejo editar los vencimientos y 
            # cobros.
            #self.wids['expander1'].set_sensitive(True)
            #self.wids['hpaned1'].set_sensitive(True)
            self.wids['vbox2'].set_sensitive(True)
        # Oculto la columna de descripción complementaria para usuarios 
        # sin permiso.
        col = self.wids['tv_ldvs'].get_column(2)
        if col != None: # Si ya se ha construido el widget
            col.set_property("visible", not(self.usuario and self.usuario.nivel > 2))

    def ir_a_primero(self):
        """
        Hace que el primer registro -si lo hay- de la tabla implicada
        en el objeto del formulario sea el objeto activo.
        """
        factura = self.objeto
        try:
            # Anulo el aviso de actualización del envío que deja de ser activo.
            if factura != None: factura.notificador.set_func(lambda : None)
            factura = pclases.Prefactura.select(orderBy="-id")[0]    # Selecciono todos y me quedo con el primero de la lista
            factura.notificador.set_func(self.aviso_actualizacion)        # Activo la notificación
        except:
            factura = None     
        self.objeto = factura
        self.actualizar_ventana()

    def refinar_resultados_busqueda(self, resultados):
        """
        Muestra en una ventana de resultados todos los
        registros de "resultados".
        Devuelve el id (primera columna de la ventana
        de resultados) de la fila seleccionada o None
        si se canceló.
        """
        filas_res = []
        for r in resultados:
            nombrecliente = [r.cliente and r.cliente.nombre or ''][0]
            filas_res.append((r.id, r.numfactura, utils.str_fecha(r.fecha), nombrecliente))
        idfactura = utils.dialogo_resultado(filas_res,
                                            titulo = 'Seleccione factura',
                                            cabeceras = ('ID', 'Número de factura', 'Fecha', 'Cliente'), 
                                            padre = self.wids['ventana'])
        if idfactura < 0:
            return None
        else:
            return idfactura

    def rellenar_widgets(self):
        """
        Introduce la información del factura actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        factura = self.objeto
        self.wids['ventana'].set_title("Prefacturas - %s" % (factura.numfactura))
        self.wids['e_numfactura'].set_text(factura.numfactura)
        self.wids['e_observaciones'].set_text(factura.observaciones)
        self.wids['e_fecha'].set_text(utils.str_fecha(factura.fecha))
        cliente = factura.cliente
        self.wids['frame1'].set_sensitive(cliente != None)
        self.wids['hpaned1'].set_sensitive(cliente != None)
        #self.wids['expander1'].set_sensitive(cliente != None)
        # Ninguna factura debe tener un cliente None, así que si es así que 
        # salte una excepción en la siguiente línea.
        self.wids['e_cliente'].set_text(cliente.nombre)
        self.wids['ch_bloqueada'].set_active(factura.bloqueada)
        self.rellenar_contenido()
        self.rellenar_servicios()
        self.rellenar_abonos()
        self.wids['e_estado'].set_text(self.objeto.get_str_estado())
        self.objeto.make_swap()

    def rellenar_contenido(self):
        """
        Rellena el contenido de la factura.
        Aquí no se chequea que en cbe_cliente haya
        un cliente válido, por tanto hay que
        hacerlo antes de llamar a esta función.
        """
        factura = self.objeto  # @UnusedVariable
        self.rellenar_ldvs()
        self.rellenar_sources()
        self.rellenar_vencimientos()

    def rellenar_totales(self):
        """
        Calcula los totales de la factura a partir de 
        las LDVs, servicios, cargo, descuento y abonos.
        """
        factura = self.objeto
        # XXX: 20101011
        #subtotal = self.total_ldvs(factura) + self.total_srvs(factura)
        subtotal = self.objeto.calcular_subtotal()
        # XXX
        self.wids['e_subtotal'].set_text("%s €" % utils.float2str(subtotal))
        self.wids['e_cargo'].set_text("%s €" % utils.float2str(factura.cargo))
        self.wids['e_descuento'].set_text("%d %%" % (factura.descuento * 100))
        try:
            tot_dto = ffloat(-1 * (subtotal + factura.cargo)*factura.descuento)
        except TypeError:
            tot_dto = ffloat(-1 * (subtotal + float(factura.cargo)) 
                                * float(factura.descuento))
        self.wids['e_tot_dto'].set_text("%s €" % utils.float2str(tot_dto))
        if tot_dto < 0:
            self.wids['e_tot_dto'].modify_text(gtk.STATE_NORMAL, 
                    self.wids['e_tot_dto'].get_colormap().alloc_color("red"))
        else:
            self.wids['e_tot_dto'].modify_text(gtk.STATE_NORMAL, 
                    self.wids['e_tot_dto'].get_colormap().alloc_color("black"))
        self.wids['e_iva'].set_text("%d %%" % (factura.iva * 100))
        self.wids['e_irpf'].set_text("%d %%" % (factura.irpf * 100))
        abonos = sum([pa.importe for pa in self.objeto.pagosDeAbono])
        tot_iva = self.total_iva(factura.iva, 
                                 subtotal, 
                                 tot_dto, 
                                 factura.cargo, 
                                 abonos)
        tot_irpf = self.total_irpf(subtotal, factura.irpf)
        self.wids['e_total_irpf'].set_text("%s €" % utils.float2str(tot_irpf))
        self.wids['e_total_iva'].set_text("%s €" % utils.float2str(tot_iva))
        self.wids['e_total'].set_text("%s €" 
            % utils.float2str(self.total(subtotal, 
                                         factura.cargo, 
                                         tot_dto, 
                                         tot_iva, 
                                         abonos, 
                                         tot_irpf)))

    def total(self, subtotal, cargo, dto, iva, abonos, irpf):
        # XXX: 20101011
        #return ffloat(subtotal + cargo + dto + iva + abonos + irpf)
        return self.objeto.calcular_total()
        # XXX

    def total_irpf(self, base_imponible, irpf):
        return ffloat(base_imponible * irpf)

    def total_iva(self, iva, subtotal, tot_dto, cargo, abonos):
        return ffloat(subtotal + tot_dto + cargo + abonos) * iva

    def total_ldvs(self, factura):
        """
        Total de las líneas de venta. Sin IVA.
        """
        return sum([ffloat((l.cantidad * l.precio) * (1 - l.descuento)) 
                    for l in factura.lineasDeVenta])
        
    def total_srvs(self, factura):
        """
        Total de servicios. Sin IVA.
        """
        return sum([ffloat((s.precio * s.cantidad) * (1 - s.descuento)) 
                    for s in factura.servicios])

    def actualizar_vencimientos(self):
        """
        Actualiza los vencimientos NO estimados a la
        cantidad adecuada para que la suma de todos
        ellos sea igual que el total de factura.
        """
        factura = self.objeto
        vtos = [v for v in factura.vencimientosCobro if v.estimado == False]
        total = utils._float(self.wids['e_total'].get_text())
        numvtos = len(vtos)
        try:
            cantidad = total/numvtos
        except ZeroDivisionError:
            return    # No hay vencimientos.
        for vto in vtos:
            vto.cantidad = cantidad
        self.rellenar_vencimientos()
        # NOTA: Si el usuario quiere que el ordenador recalcule los 
        #       vencimientos que edite momentáneamente alguna LDV y pulse 
        #       ENTER. Aunque no cambie el valor, se invocará el 
        #       actualizar_totales y tal.

    def rellenar_ldvs(self):
        """
        Introduce las LDV de la factura en la tabla y devuelve la 
        suma de los totales de línea sin IVA.
        """
        factura = self.objeto 
        model = self.wids['tv_ldvs'].get_model()
        model.clear()
        peds = {'-': []}
        lineasdeventa = [ldv for ldv in factura.lineasDeVenta]
        lineasdeventa.sort(utils.f_sort_id)
        for ldv in lineasdeventa:
            totlinea = ldv.get_subtotal()
            cantidad = ldv.cantidad
            precio = ldv.calcular_precio_unitario_coherente()
            model.append((ldv.producto.codigo,
                          ldv.producto.descripcion,
                          ldv.descripcionComplementaria, 
                          cantidad,
                          precio,
                          "%.2f %%" % (ldv.descuento*100),  
                            # El dto. se guarda como fracción de 100
                          totlinea,
                          (ldv.albaranSalida and ldv.albaranSalida.numalbaran) \
                            or (ldv.ticket 
                                and "TICKET %d" % ldv.ticket.numticket) \
                            or '-',
                          ldv.pedidoVenta and ldv.pedidoVenta.numpedido or '-',
                          ldv.id))
            if (ldv.pedidoVenta == None 
                and ldv.albaranSalida != None 
                and ldv.albaranSalida.numalbaran not in peds['-']):
                peds['-'].append(ldv.albaranSalida.numalbaran)
            elif ldv.pedidoVenta != None:
                if ldv.pedidoVenta.numpedido not in peds:
                    peds[ldv.pedidoVenta.numpedido] = []
                if ldv.albaranSalida != None:
                    if (not ldv.albaranSalida.numalbaran 
                        in peds[ldv.pedidoVenta.numpedido]):
                        peds[ldv.pedidoVenta.numpedido].append(
                            ldv.albaranSalida.numalbaran)
        # Busco albaranes y pedidos de servicios:
        for srv in self.objeto.servicios:
            if (srv.pedidoVenta == None 
                and srv.albaranSalida != None 
                and srv.albaranSalida.numalbaran not in peds['-']):
                peds['-'].append(srv.albaranSalida.numalbaran)
            elif srv.pedidoVenta != None:
                if srv.pedidoVenta.numpedido not in peds:
                    peds[srv.pedidoVenta.numpedido] = []
                if srv.albaranSalida != None:
                    if not srv.albaranSalida.numalbaran in peds[srv.pedidoVenta.numpedido]:
                        peds[srv.pedidoVenta.numpedido].append(srv.albaranSalida.numalbaran)

        pedsalbs = ""
        for p in peds:
            if p == '-' and peds[p] == []:
                continue
            pedsalbs += "%s(%s) " % (p, ','.join(peds[p]))
        self.wids['e_peds_albs'].set_text(pedsalbs)
        self.rellenar_totales()

    def separar_ldvs(self, ldvs):
        """
        Separa las líneas de venta en un diccionario con 
        tres listas. La primera de identificadores de
        líneas de venta sin factura y pertenecientes a 
        pedidos. La segunda con albaranes y sus líneas 
        de venta sin facturar (aunque se repitan en la 
        lista de pedidos también). La tercera es una 
        lista de ventas sin pedido, albarán ni factura 
        asociada.
        El diccionario, por tanto, quedará:
        {'pedidos': {IDpedido: [IDldv, IDldv, IDldv...], IDpedido2: [...], ...},
         'albaranes': {IDalbarán: [IDldv, ...], ...},
         'pendientes': [IDldv, IDldv, ...]}
        """
        srcs = {'pedidos': {},
                'albaranes': {},
                'pendientes': []}
        for ldv in ldvs:
            if ldv.pedidoVenta != None:
                if not ldv.pedidoVenta in srcs['pedidos']:
                    srcs['pedidos'][ldv.pedidoVenta.id] = []
                srcs['pedidos'][ldv.pedidoVenta.id].append(ldv.id)
            if ldv.albaranSalida != None:
                if not ldv.albaranSalida in srcs['albaranes']:
                    srcs['albaranes'][ldv.albaranSalida.id] = []
                srcs['albaranes'][ldv.albaranSalida.id].append(ldv.id)
            if ldv.pedidoVenta == None and ldv.albaranSalida == None:
                srcs['pendientes'].append(ldv.id)
        # PLAN: Podría aprovechar y calcular aquí los totales del pedido para 
        #       insertarlos en las cabeceras del model más tarde.
        return srcs

    def rellenar_sources(self):
        model = self.wids['tv_srcs'].get_model()
        model.clear()
        cliente = self.objeto.cliente
        # Cambios: Ya no se puede facturar nada sin albarán y además el 
        # albarán debe ser facturable.
        ldvs = pclases.LineaDeVenta.select("""
            (albaran_salida_id IN (SELECT id FROM albaran_salida 
                                   WHERE cliente_id = %d AND 
                                         albaran_salida.facturable = True) 
            ) AND factura_venta_id IS NULL AND prefactura_id IS NULL 
            """ % (cliente.id))
        srvs = pclases.Servicio.select("""
            (factura_venta_id IS NULL AND prefactura_id IS NULL) 
            AND (albaran_salida_id IN (SELECT id FROM albaran_salida WHERE 
                                       cliente_id = %d AND albaran_salida.facturable = True)) 
        """ % (cliente.id))
        for ldv in ldvs:
            self.insertar_ldv_en_model(ldv, None, model)
        for srv in srvs:
            self.insertar_servicio_en_model(srv, None, model)
        
    def insertar_ldv_en_model(self, ldv, padre, model):
        """
        Inserta la LDV correspondiente al id recibido en el
        model de la tabla de orígenes (sources; tv_srcs).
        """
        totlinea = ldv.cantidad * ldv.precio * (1.0 - ldv.descuento)
        model.append(padre,
                     (ldv.producto.codigo,
                      ldv.producto.descripcion,
                      utils.float2str(ldv.cantidad, 3, autodec = True), 
                      utils.float2str(ldv.precio, 3, autodec = True),
                      utils.float2str(ldv.descuento, 3, autodec = True),
                      utils.float2str(totlinea, 3, autodec = True),
                      ldv.pedidoVenta and ldv.pedidoVenta.numpedido or '-',
                      ldv.albaranSalida and ldv.albaranSalida.numalbaran or '-',
                      ldv.id))
        
    def insertar_servicio_en_model(self, srv, padre, model):
        """
        Inserta la LDV correspondiente al id recibido en el
        model de la tabla de orígenes (sources; tv_srcs).
        """
        totlinea = srv.cantidad * srv.precio * (1.0 - srv.descuento)
        model.append(padre,
                     ("TRANSPORTE Y OTROS",
                      utils.recortar(srv.concepto, 30),
                      utils.float2str(srv.cantidad, 3, autodec = True),
                      utils.float2str(srv.precio, 3, autodec = True),
                      utils.float2str(srv.descuento, 3, autodec = True),
                      utils.float2str(totlinea, 3, autodec = True),
                      '-',
                      srv.albaranSalida and srv.albaranSalida.numalbaran or '-',
                      srv.id))

    def rellenar_vencimientos(self):
        """
        Mete la información de los vencimientos, pagos, etc.
        del factura actual en la tabla tv_vencimientos.
        """
        # PLAN: Colorear vencimientos incumplidos, con estimaciones rebasadas...
        # OJO: Además, también hay que emparejar por proximidad de fechas los pagos realizados
        #      (clase Pago) con los vencimientos a los que corresponderían (no hay relación directa).
        vtos = self.preparar_vencimientos()
        # FIXME: (?) Se llama a preparar_vencimientos hasta 4 veces (!) al mostar una factura en pantalla.    
        model = self.wids['tv_vencimientos'].get_model()
        model.clear()
        total_vtos = 0
        total_pagado = 0
        total_vencido = 0
        pendiente = 0  # @UnusedVariable
        for vto in vtos:
            if vto[0] != None:
                cantidad = vto[0].importe
                fechavto = utils.str_fecha(vto[0].fecha)
                if vto[0].fecha < mx.DateTime.localtime():   # Ha vencido ya
                    total_vencido += cantidad
                formapago = vto[0].observaciones
                cuenta =  vto[0].cuentaOrigen and vto[0].cuentaOrigen.get_info() or "" 
                ids = '%d,' % vto[0].id
            else:
                cantidad = 0
                fechavto = ''
                ids = '-1,'    # OJO: Si no hay, el ID lo considero -1.
                formapago = cuenta = ""
            total_vtos += cantidad
            if vto[1] != None:
                fechaest = utils.str_fecha(vto[1].fecha)  # @UnusedVariable
                # OJO: Actualizo la cantidad de la estimación a la cantidad 
                #      del vencimiento real:
                vto[1].importe = cantidad
                ids += '%d,' % vto[1].id
            else:
                fechaest = ''  # @UnusedVariable
                ids += '%d,' % -1
            if vto[2] != None:
                fechapag = utils.str_fecha(vto[2].fecha)
                realizado = True
                ids += '%d' % vto[2].id
                importe = vto[2].importe
                if vto[2].pagareCobro:
                    pagare = "Pagaré %s con fecha %s y vencimiento %s" % (vto[2].pagareCobro.codigo, 
                                                                          utils.str_fecha(vto[2].pagareCobro.fechaRecepcion), 
                                                                          utils.str_fecha(vto[2].pagareCobro.fechaCobro))
                    if vto[2].pagareCobro.pendiente:
                        pagare += " (pdte. de cobro)"
                    vto[2].observaciones = pagare
                else:
                    pagare = vto[2].observaciones
            else:
                fechapag = ''
                realizado = False
                ids += '%d' % -1
                importe = 0
                pagare = ""
            total_pagado += importe
            model.append((fechavto, 
                          cantidad, 
                          formapago, 
                          cuenta, 
                          realizado,
                          fechapag,
                          importe,
                          pagare,
                          ids))
            # BUG: Que no es tal. Es el rollo de los float y el __repr__. Tengo que buscar la forma de
            #      que el cell tipo float de la tabla corte en dos/tres decimales. Queda muy feo ver
            #      100.2399998 cuando se ha escrito 100.24 (o 34457.801 cuando en la BD hay 34457.800).
        pendiente = total_vtos - total_pagado
        self.wids['e_total_vtos'].set_text(utils.float2str(total_vtos))
        self.wids['e_total_pagado'].set_text(utils.float2str(total_pagado))
        self.wids['e_total_vencido'].set_text(utils.float2str(total_vencido))
        self.wids['e_pendiente'].set_text(utils.float2str(pendiente))
        if total_pagado < total_vencido:
            self.wids['e_total_pagado'].modify_base(gtk.STATE_NORMAL,
                                                self.wids['e_total_pagado'].get_colormap().alloc_color("red"))
        elif total_pagado == total_vencido:
            self.wids['e_total_pagado'].modify_base(gtk.STATE_NORMAL,
                                                self.wids['e_total_pagado'].get_colormap().alloc_color("white"))
        else:
            self.wids['e_total_pagado'].modify_base(gtk.STATE_NORMAL,
                                                self.wids['e_total_pagado'].get_colormap().alloc_color("blue"))
        # COMPRUEBO SI LOS VENCIMIENTOS COINCIDEN
        total_fra = utils._float(self.wids['e_total'].get_text().replace("€", ""))
        if (total_vtos != 0 and 
            round(total_vtos*100) != round(total_fra*100)):
            utils.dialogo_info(titulo = "VENCIMIENTOS NO COINCIDEN",
                               texto = "El importe de los vencimientos no coincide con el total de la factura.",
                               padre = self.wids['ventana'])
                
    def preparar_vencimientos(self):
        """
        A partir de los vencimientos y pagos asociados a la 
        factura construye una lista de listas de la forma:
        [[vencimiento, vencimiento_estimado, pago],
         [vencimiento, vencimiento_estimado, pago],
         ...]
        Cualquiera de los tres objetos puede ser None en
        alguna fila donde no haya, por ejemplo, una estimación
        o un pago para un vencimiento.
        La lista se construye emparejando por proximidad de
        fechas entre los tres grupos (vto., vto. estimado y
        pago) y no se tiene en cuenta ningún otro criterio.
        """
        # PLAN: Se podría meter una columna "vencido/pagado hasta el momento" con el SUM{i=0→n}(cantidad[i]) siendo n la fila actual.
        factura = self.objeto
        # Joder... para esto de relaciones inyectivas entre
        # conjuntos debe haber un algoritmo más o menos eficiente
        # por ahí, ¿no? Seguro que el mamón de Dijsktra se 
        # inventó algo. Y yo sin internete.
        res = []
        vtos = [v for v in factura.vencimientosCobro]
        ests = [v for v in factura.estimacionesCobro]
        pags = factura.cobros
        # mas_larga = max(vtos, ests, pags)     # No rula y no sé por qué
        mas_larga = [l for l in (vtos, ests, pags) if len(l)==max(len(vtos), len(ests), len(pags))][0]
        if len(mas_larga) == 0: return []
        for i in xrange(len(mas_larga)):  # @UnusedVariable
            res.append([None, None, None])
        #---------------------------------------------------#
        def comp(v1, v2):                                  #
            if v1.fecha < v2.fecha: return -1               #
            if v1.fecha > v2.fecha: return 1                #
            return 0                                        #
        def distancia(v1, v2):                             #
            return abs(v1.fecha - v2.fecha)                 #
        def lugar(v):                                      #
            if isinstance(v, pclases.VencimientoCobro):     #
                return 0                                    #
            elif isinstance(v, pclases.EstimacionCobro):    #
                return 1                                    #
            else:                                           #
                return 2                                    #
        #---------------------------------------------------#
        resto = [vtos, ests, pags]
        resto.remove(mas_larga)
        mas_larga.sort(comp)
        pos = 0
        for item in mas_larga:
            res [pos][lugar(item)] = item
            pos += 1
        for lista in resto:
            mlc = mas_larga[:]
            lista.sort(comp)
            while lista:
                item2 = lista.pop()
                mindist = distancia(item2, mlc[0])
                sol = mlc[0]
                for item1 in mlc:
                    if distancia(item1, item2) < mindist:
                        sol = item1
                        mindist = distancia(item1, item2)
                res[mas_larga.index(sol)][lugar(item2)] = item2 
                mlc.remove(sol)
        return res
        # Creo que aunque lo comente, tampoco se va a entender. Vaya traca 
        # de algoritmo.

    def desvincular_ldv_de_factura(self, ldv):
        """
        Pone el factura de la ldv a None, con lo
        que se desvincula de la factura. 
        """
        ldv.prefactura = None

    def add_pedido(self, idpedido):
        """
        Añade todas las LDV sin facturar del pedido a la 
        factura actual.
        """
        factura = self.objeto
        pedido = pclases.PedidoVenta.get(idpedido)
        for ldv in [l for l in pedido.lineasDeVenta if l.facturaVenta == None and l.prefactura == None]:
            ldv.prefactura = factura
        
    def add_albaran(self, idalbaran):
        """
        Añade todas las LDV del albarán sin facturar a
        la factura actual.
        """
        factura = self.objeto
        albaran = pclases.AlbaranSalida.get(idalbaran)
        for ldv in [l for l in albaran.lineasDeVenta if l.facturaVenta == None and l.prefactura == None]:
            ldv.prefactura = factura
        for srv in [s for s in albaran.servicios if s.facturaVenta == None and s.prefactura == None]:
            srv.prefactura = factura
        
    def add_servicio(self, idsrv):
        """
        Añade el servicio correspondiente a "idsrv" a la
        factura actual.
        """
        factura = self.objeto
        srv = pclases.Servicio.get(idsrv)
        if srv.prefactura == None and srv.prefactura == None:
            # Por si se ha facturado casi simultáneamente en otro puesto.
            srv.prefactura = factura
        else:
            utils.dialogo_info('SERVICIO FACTURADO', 'El servicio ya ha sido usado en la factura número %d.' % srv.factura.numfactura, padre = self.wids['ventana'])

    def add_ldv(self, idldv):
        """
        Añade la LDV correspondiente a "idldv" a la
        factura actual.
        """
        factura = self.objeto
        try:
            ldv = pclases.LineaDeVenta.get(idldv)
        except pclases.SQLObjectNotFound:
            return
        if ldv.prefactura == None and ldv.prefactura == None:
            # Por si se ha facturado casi simultáneamente en otro puesto.
            tolerancia = 0.1
            # print "DEBUG: (TEMPORAL, NO ES UN ERROR): ¿%f == %f - %f?" % (abs(ldv.cantidad - ldv.cantidad_albaraneada), ldv.cantidad, ldv.cantidad_albaraneada)
            if abs(ldv.cantidad_total_solicitada_del_producto - ldv.cantidad_albaraneada) > tolerancia:
                # TODO: La tolerancia es hasta que encuentre el error de 
                # cálculo que hace que aunque las cantidades sean 
                # "teóricamente" iguales, no sean ==.
                txt = """
                La línea de venta perteneciente al pedido %s difiere 
                respecto a la cantidad servida en el albarán %s.
                Si continúa, se facturará la cantidad DEL PEDIDO                    
                ORIGINAL. Edite el albarán de salida o el pedido                    
                para ajustar las cantidades solicitadas, servidas                   
                y facturadas.                                                       
                
                Cantidad total solicitada por el cliente: %s
                Cantidad servida en albarán: %s
                
                ¿Desea facturar %s %s de %s?
                """ % (ldv.pedidoVenta and ldv.pedidoVenta.numpedido or "-", 
                       ldv.albaranSalida and ldv.albaranSalida.numalbaran or "-", 
                       ldv.cantidad_total_solicitada_del_producto, 
                       ldv.cantidad_albaraneada, 
                       ldv.cantidad, 
                       ldv.productoVentaID and (ldv.productoVenta.es_rollo() and "m²" or "kg") or ldv.productoCompra.unidad, 
                       ldv.productoVentaID and ldv.productoVenta.nombre or ldv.producto.descripcion)
                if not utils.dialogo(titulo = "ALBARÁN INCONSISTENTE", 
                                     texto = txt,
                                     padre = self.wids['ventana']):
                    return
            if len(factura.lineasDeVenta) == 0:
                factura.descuento = ldv.pedidoVenta and ldv.pedidoVenta.descuento or 0
            ldv.prefactura = factura
        else:
            utils.dialogo_info('VENTA FACTURADA', 'La venta ya ha sido facturada en la factura número %d.' % (ldv.facturaVenta and ldv.facturaVenta.numfactura or ldv.prefactura.numfactura), 
                               padre = self.wids['ventana'])

    #===========================================================================
    # def buscar_articulos(self):
    #     a_buscar = utils.dialogo_entrada('Introduzca código de producto, código interno o descripción', 
    #                                      'BUSCAR ARTÍCULO', 
    #                                      padre = self.wids['ventana'])
    #     # Tengo que buscar entre balas, rollos y productos para obtener una lista de artículos.
    #     productos = pclases.Producto.select(sqlobject.OR(pclases.Producto.q.codigo.contains(a_buscar), 
    #                                                      pclases.Producto.q.descripcion.contains(a_buscar)))
    #     rollos = pclases.Rollo.select(pclases.Rollo.q.codigo.contains(a_buscar))
    #     balas = pclases.Bala.select(pclases.Bala.q.codigo.contains(a_buscar))
    #     articulos = []
    #     for p in productos:
    #         for a in p.articulos:
    #             if not a in articulos:
    #                 articulos.append(a)
    #     for r in rollos:
    #         if r.idarticulo != None and not r.idarticulo in articulos:
    #             articulos.append(r.idarticulo)
    #     for b in balas:
    #         if b.idarticulo != None and not b.idarticulo in articulos:
    #             articulos.append(b.idarticulo)
    #     return articulos
    #===========================================================================

    def borrar_vencimientos_y_estimaciones(self, factura):
        for vto in factura.vencimientosCobro:
            vto.factura = None
            vto.destroy(ventana = __file__)
        for est in factura.estimacionesCobro:
            est.factura = None
            est.destroy(ventana = __file__)

    def get_numero_numfactura_from(self, numfactura, cliente):
        """
        Devuelve el número de factura sin prefijo ni 
        sufijo y como entero.
        Salta una excepción si no se pudo determinar
        la parte numérica del número de factura.
        """
        try:
            numero = pclases.Prefactura.get_numero_numfactura_from(numfactura)
        except (TypeError, AssertionError, ValueError), msg:
            txt = "No se pudo determinar número de factura. Mensaje de la excepción: %s" % msg
            self.logger.error("%sprefacturas.py::get_numero_numfactura_from -> %s" % (self.usuario and self.usuario.usuario + ": " or "", txt))
            numero = 0
        return numero


    # --------------- Manejadores de eventos ----------------------------
    def crear_nueva_factura(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        factura = self.objeto
            # Datos a pedir: Cliente y número de factura.
        clientes = [(c.id, c.nombre) for c in pclases.Cliente.select(pclases.Cliente.q.inhabilitado == False, orderBy='nombre')]
        idcliente = utils.dialogo_combo('SELECCIONE CLIENTE',
                'Seleccione un cliente. Si no encuentra el cliente buscado, '
                'verifique\nque existe en la aplicación mediante la ventana '
                'de clientes y que no esté inhabilitado.',
            clientes, 
            padre = self.wids['ventana'])
        try:
            cliente = pclases.Cliente.get(idcliente)
            cliente.sync()
        except:
            return  # El cliente no existe o canceló.
        d, m, y = utils.mostrar_calendario(padre = self.wids['ventana'])
        fecha = mx.DateTime.DateTimeFrom(day = d, month = m, year = y)
        try:
            numfactura_defecto = pclases.Prefactura.get_next_numfactura(fecha.year)
        except Exception, msg:
            txtexcept = "%sprefacturas.py::get_numero_numfactura_from -> %s" % (self.usuario and self.usuario.usuario + ": " or "", msg)
            self.logger.error(txtexcept)
            utils.dialogo_info(titulo = "ERROR", 
                               texto = "No se pudo determinar el número de factura.\n\nInformación de depuración:\n%s" % txtexcept, 
                               padre = self.wids['ventana'])
        else:
            if factura != None:
                factura.notificador.desactivar()
            iva = 0.0
            try:
                irpf = pclases.DatosDeLaEmpresa.select()[0].irpf
            except (IndexError, AttributeError), msg:
                self.logger.error("prefacturas::crear_nueva_factura -> No se encontraron los datos de la empresa. Excepción: %s" % (msg))
                irpf = 0.0
            numfactura = utils.dialogo_entrada(titulo = "NÚMERO DE PREFACTURA", 
                                               texto = "Introduzca un número de prefactura.\nDeje el que aparece por defecto si no está seguro:", 
                                               padre = self.wids['ventana'], 
                                               valor_por_defecto = numfactura_defecto)
            if numfactura != None:
                factura = pclases.Prefactura(fecha = fecha, 
                                             numfactura = numfactura,
                                             cliente = cliente,
                                             iva = iva,
                                             cargo = 0,
                                             bloqueada = False, 
                                             irpf = irpf)
                pclases.Auditoria.nuevo(factura, self.usuario, __file__)
                self.objeto = self._objetoreciencreado = factura
                self.actualizar_ventana()
                factura.notificador.set_func(self.aviso_actualizacion)

    def buscar_factura(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        factura = self.objeto
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR PREFACTURA", 
                                         texto = "Introduzca número o parte del número de factura pro forma:", 
                                         padre = self.wids['ventana']) 
        # PLAN: Ya haré para que se pueda buscar también por cliente y eso.
        if a_buscar != None:
            resultados = pclases.Prefactura.select(pclases.Prefactura.q.numfactura.contains(a_buscar), 
                                                     orderBy = "numfactura")
            if resultados.count() > 1:
                ## Refinar los resultados
                idfactura = self.refinar_resultados_busqueda(resultados)
                if idfactura == None:
                    return
                resultados = [pclases.Prefactura.get(idfactura)]
            elif resultados.count() < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info('SIN RESULTADOS', 
                                   'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.\n(Atención: Ver la lista completa puede resultar lento si el número de elementos es muy alto)', 
                                   padre = self.wids['ventana'])
                return
            ## Un único resultado
            # Primero anulo la función de actualización
            if factura != None:
                factura.notificador.set_func(lambda : None)
            # Pongo el objeto como actual
            factura = resultados[0]
            # Y activo la función de notificación:
            factura.notificador.set_func(self.aviso_actualizacion)
            self.objeto = factura
            self.actualizar_ventana()

    def guardar(self, widget):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        factura = self.objeto
        # Campos del objeto que hay que guardar: IVA. Fecha y numfactura no, tienen botón propio.
        # Desactivo el notificador momentáneamente
        factura.notificador.set_func(lambda: None)
        # Actualizo los datos del objeto
        try:
            iva = utils.parse_porcentaje(self.wids['e_iva'].get_text(), fraccion = True)
        except ValueError:
            iva = 0
        factura.iva = iva
        try:
            irpf = utils.parse_porcentaje(self.wids['e_irpf'].get_text(), fraccion = True)
            if irpf > 0.0:      # El IRPF _siempre_ se descuenta (lo retiene el cliente).
                irpf *= -1
        except ValueError:
            irpf = 0
        factura.irpf = irpf
        # Comprueba el país del cliente.
        if factura.clienteID and factura.cliente.es_extranjero() and (factura.cliente.get_iva_norm() != 0 or factura.iva != 0):
            utils.dialogo_info(titulo = "VERIFIQUE EL IVA", 
                               texto = """
                Los clientes extranjeros suelen llevar IVA 0 %%.            
                El IVA actual de la factura es %d %% y                      
                el del cliente %d %%.                                       
                Cancele la impresión si considera que                       
                estos datos son incorrectos.""" % (factura.iva * 100, factura.cliente.get_iva_norm() * 100), 
                                padre = self.wids['ventana'])
        try:
            dto = utils.parse_porcentaje(self.wids['e_descuento'].get_text()) / 100.0
        except ValueError:
            dto = 0
        factura.descuento = dto
        factura.observaciones = self.wids['e_observaciones'].get_text()
        
        # Si no tiene permisos para bloquear, no guardar "bloqueada":
        condicion_modificacion = self.usuario
        try:
            ventana = pclases.Ventana.selectBy(fichero = "prefacturas.py")[0]
        except:
            pass
        else:
            if self.usuario:
                permisos = self.usuario.get_permiso(ventana)
                condicion_modificacion = permisos and condicion_modificacion and \
                                        (permisos.escritura or (permisos.nuevo and self.objeto == self._objetoreciencreado))
                condicion_modificacion = condicion_modificacion or self.usuario.nivel <= 2
            if not condicion_modificacion and self.usuario != None:
                utils.dialogo_info(titulo = "OPERACIÓN NO PERMITIDA",
                                   texto = "No tiene privilegios suficientes para cambiar el bloqueo de facturas.",
                                   padre = self.wids['ventana'])
            else:
                factura.bloqueada = self.wids['ch_bloqueada'].get_active()
                bloquear_albaranes(factura)
        try:
            cargo = self.wids['e_cargo'].get_text()
            cargo = cargo.replace('€', '')
            cargo = cargo.replace(' ', '')
            cargo = utils._float(cargo)
        except:
            cargo = 0
        factura.cargo = cargo
        factura.syncUpdate()
        # Vuelvo a activar el notificador
        factura.notificador.set_func(self.aviso_actualizacion)
        self.actualizar_ventana()
        self.wids['b_guardar'].set_sensitive(False)

    def buscar_fecha(self):
        fecha = utils.str_fecha(utils.mostrar_calendario(fecha_defecto = self.objeto and self.objeto.fecha or None, padre = self.wids['ventana']))
        return fecha

    def cambiar_fecha(self, w):
        self.objeto.notificador.desactivar()
        fecha = self.buscar_fecha()
        nueva_fecha = utils.parse_fecha(fecha)
        # factura_anterior, factura_posterior, ok = self.chequear_cambio_fecha(self.objeto, nueva_fecha)
        ok = True   # No se llevará control de numeración consecutiva por fechas.
        if ok: 
            self.objeto.fecha = nueva_fecha
            self.objeto.make_swap()
            self.wids['e_fecha'].set_text(utils.str_fecha(self.objeto.fecha))
            self.objeto.notificador.activar(self.aviso_actualizacion)
        #else:
        #    utils.dialogo_info(titulo = "ERROR EN FECHA",
        #                       texto = """
        #    No puede asignar una fecha anterior a la de la factura inmediatamente           
        #    anterior ni posterior a la de la siguiente factura en su serie.                 
        #    Factura anterior:
        #        - Nº factura %s.
        #        - Fecha %s.
        #    Factura posterior:
        #        - Nº factura %s.
        #        - Fecha %s.
        #    """ % (factura_anterior and factura_anterior.numfactura or "-",
        #           factura_anterior and utils.str_fecha(factura_anterior.fecha) or "-",
        #           factura_posterior and factura_posterior.numfactura or "-",
        #           factura_posterior and utils.str_fecha(factura_posterior.fecha) or "-"))

    def chequear_cambio_fecha(self, factura, fecha):
        """ UNUSED -ByTheMoment(R)- """
        # HACK:
        clientes = [`c.id` for c in factura.cliente.contador.clientes]
        clientes = ','.join(clientes)
        #print clientes
        facturas = pclases.Prefactura.select("cliente_id IN (%s)" % clientes)
        # Any better?
        facturas = [fra for fra in facturas if fra.numfactura.startswith(factura.cliente.contador.prefijo) \
                                               and fra.numfactura.endswith(factura.cliente.contador.sufijo)]
        #print [f.numfactura for f in facturas]
        facturas.sort(lambda f1, f2: f1.get_numero_numfactura() - f2.get_numero_numfactura())
        # Divido la lista en dos tomando como eje -no incluido- la factura actual:
        i_actual = facturas.index(factura)
        anteriores = facturas[:i_actual]
        posteriores = facturas[i_actual+1:]
        factura_anterior = anteriores and anteriores[-1] or None
        factura_posterior = posteriores and posteriores[0] or None
        ok = True
        if factura_anterior:
            ok = ok and factura_anterior.fecha <= fecha
        if factura_posterior:
            ok = ok and factura_posterior.fecha >= fecha
        return factura_anterior, factura_posterior, ok

    def cambiar_numfactura(self, w):
        self.objeto.notificador.desactivar()
        numfactura = utils.dialogo_entrada(titulo = 'NÚMERO DE FACTURA',
                                           texto = 'Introduzca nuevo número de factura:',
                                           padre = self.wids['ventana'], 
                                           valor_por_defecto = self.objeto.numfactura)
        if numfactura == None:
            return
        try:
            anno, numero = pclases.Prefactura.get_numero_numfactura_y_anno_from(numfactura)  # @UnusedVariable
        except (AssertionError, ValueError, TypeError):
            nuevo_numero = None
        else:
            nuevo_numero = numfactura
        if nuevo_numero == None:
            utils.dialogo_info(titulo = 'NÚMERO ERRÓNEO',
                               texto = 'El número de factura %s no es correcto.\nTenga en cuenta que debe cumplir el formato x/aaaa\n(donde «x» es un número y «aaaa» el año con cuatro dígitos).' % (numfactura), 
                               padre = self.wids['ventana'])
        else:
            ok = self.chequear_cambio_numero(nuevo_numero)
            if ok: 
                self.objeto.numfactura = nuevo_numero
                self.objeto.make_swap()
                self.wids['e_numfactura'].set_text(self.objeto.numfactura)
                self.objeto.notificador.activar(self.aviso_actualizacion)
            else:
                utils.dialogo_info(titulo = "ERROR EN NÚMERO DE FACTURA",
                                   texto = "El número %s ya existe." % (nuevo_numero), 
                                   padre = self.wids['ventana'])

    def chequear_cambio_numero(self, numfactura):
        """ numero debe ser el entero con el número, sin prefijos ni sufijos. """
        count_facturas = pclases.Prefactura.selectBy(numfactura = numfactura).count()
        ok = count_facturas == 0 or (numfactura == self.objeto.numfactura)
        return ok

    def activar_contenido(self, boton):
        """
        Activa los widgets que dependen del cliente seleccionado 
        en función de si éste es válido o no.
        DEPRECATED
        """
        factura = self.objeto
        idcliente = factura.clienteID 
        #self.wids['frame1'].set_sensitive(idcliente != None)
        self.wids['alignment4'].set_sensitive(idcliente != None)
        self.wids['hbox_observaciones'].set_sensitive(idcliente != None)
        self.wids['hpaned1'].set_sensitive(idcliente != None)
        #self.wids['expander1'].set_sensitive(idcliente != None)
        if idcliente != None:
            self.rellenar_contenido() 

    def borrar_factura(self, boton):
        """
        Elimina el factura de la BD y anula la relación entre
        él y sus LDVs.
        NO decrementa (ni debe) el contador de facturas.
        """
        if utils.dialogo(texto = 'Se eliminará la factura actual y todas sus relaciones con ventas, pedidos, etc.\n¿Está seguro?', 
                             titulo = 'BORRAR FACTURA', 
                             padre = self.wids['ventana']): 
            factura = self.objeto
            factura.notificador.set_func(lambda : None)
            for ldv in factura.lineasDeVenta:
                self.desvincular_ldv_de_factura(ldv)
                # De paso, intento eliminarla por completo, por si no tiene relación con pedidos y demás.
                ldv.eliminar()
            for servicio in factura.servicios:
                servicio.destroy(ventana = __file__)
            for estimacion in factura.estimacionesCobro:
                estimacion.destroy(ventana = __file__)
            for vencimiento in factura.vencimientosCobro:
                vencimiento.destroy(ventana = __file__)
            for cobro in factura.cobros:
                cobro.destroy(ventana = __file__)
            try:
                factura.destroy(ventana = __file__)
            except psycopg_ProgrammingError:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "No se pudo borrar la factura por completo.", 
                                   padre = self.wids['ventana'])
            else:   # Borrado correctamente
                self.ir_a_primero()

    def add_src(self, boton):
        """
        Añade la LDV seleccionada en la tabla "tv_srcs" a la factura
        actual. Si lo que se ha seleccionado es un pedido, añade el 
        pedido completo. Al igual ocurre con los albaranes.
        """
        model, paths = self.wids['tv_srcs'].get_selection().get_selected_rows()
        if paths != None and paths != []: 
            for path in paths:
                src = model[path]
                if 'edido' in src[0]:
                    self.add_pedido(src[-1])
                elif 'lbar' in src[0]:
                    self.add_albaran(src[-1])
                elif "TRANSPORTE Y OTROS" in src[0]:
                    self.add_servicio(src[-1])
                    self.rellenar_servicios() 
                    self.rellenar_vencimientos()    # Para que verifique si los totales coinciden
                else:
                    self.add_ldv(src[-1])
            self.rellenar_contenido()

    def drop_ldv(self, boton):
        """
        Elimina de la factura la LDV seleccionada en
        la tabla "tv_ldvs".
        """
        model, itr = self.wids['tv_ldvs'].get_selection().get_selected()
        if itr == None: return
        idldv = model[itr][-1]
        ldv = pclases.LineaDeVenta.get(idldv)
        ldv.prefactura = None
        if ldv.albaranSalidaID == None:     # Si no tiene ni factura ni albarán, la intento eliminar
            try:
                ldv.destroy(ventana = __file__)
            except:
                print "prefacturas.py (drop_ldv): LDV ID %d sin factura ni albarán, pero no se pudo eliminar." % (ldv.id)
        self.rellenar_contenido()

    def add_nueva_ldv(self, boton):
        """
        Añade una nueva LDV creada a partir de la 
        información recogida mediante diálogos
        modales.
        """
        self.crear_ldv()
        self.rellenar_contenido()

    def seleccionar_cantidad(self, producto):
        """
        Muestra un diálogo para introducir la cantidad.
        Si el producto es un rollo, se introducirá en 
        metros cuadrados.
        Si es una bala, se introducirá en kilos.
        En las LDV se mantendrán también estas unidades
        ya que el precio por unidad va en función de 
        kilos y rollos en el producto.
        Cuando se haga el albarán es cuando habrá que
        calcular cuantos rollos (y cuáles en concreto)
        y cuántas balas entran. Aunque en realidad es 
        el usuario el que las seleccionará y el programa
        irá informando si se satisface la LDV o no.
        """
        if isinstance(producto, pclases.ProductoVenta):
            if producto.es_bala() or producto.es_bigbag():
                txt = """Introduzca la cantidad en kilos:"""
            elif producto.es_rollo():
                txt = """Introduzca la cantidad en metros cuadrados:"""
            elif producto.es_especial():
                txt = """Introduzca la cantidad en %s.""" % (producto.camposEspecificosEspecial.unidad)
            else:
                self.logger.error("ERROR: El producto %s no es bala, rollo ni bigbag. Verificar." % (producto))
        elif isinstance(producto, pclases.ProductoCompra):
            txt = "Introduzca la cantidad en %s:" % (producto.unidad)
        else:
            txt = "Introduzca cantidad:"
        cantidad = utils.dialogo_entrada(titulo = 'CANTIDAD', texto = txt, padre = self.wids['ventana'])
        try:
            cantidad = utils._float(cantidad)
            return cantidad
        except:
            utils.dialogo_info(titulo = 'ERROR', texto = 'La cantidad introducida no es correcta.', padre = self.wids['ventana'])
            return None

    def pedir_producto(self):
        """
        Solicita un código, nombre o descripcicón 
        de producto, muestra una ventana de resultados 
        coincidentes con la búsqueda y devuelve una 
        lista de ids de productos o [] si se cancela o 
        no se encuentra.
        """
        productos = []
        txt = utils.dialogo_entrada('Introduzca código, nombre o descripción de producto.\nPuede usar también el código de COMPOSAN si está buscando geotextiles.', 
                                    'CÓDIGO PRODUCTO', 
                                    padre = self.wids['ventana'])
        if txt != None:
            criterio = pclases.OR(pclases.ProductoVenta.q.codigo.contains(txt),
                                    pclases.ProductoVenta.q.nombre.contains(txt),
                                    pclases.ProductoVenta.q.descripcion.contains(txt))
            prods = pclases.ProductoVenta.select(criterio)
            rollos = pclases.CamposEspecificosRollo.select(pclases.CamposEspecificosRollo.q.codigoComposan == txt)
            productos = [p.id for p in prods]
            productos += [p.productosVenta[0].id for p in rollos if p.productosVenta[0].id not in productos]
        return productos

    def refinar_busqueda(self, resultados):
        """
        resultados es una lista de ide de productos.
        """
        resultados = [pclases.ProductoVenta.get(ide) for ide in resultados]
        filas_res = [(p.id, p.codigo, p.nombre, p.descripcion, p.existencias, p.get_stock()) for p in resultados]
        idproducto = utils.dialogo_resultado(filas_res,
                                             titulo = 'Seleccione producto',
                                             cabeceras = ('ID Interno', 'Código', 'Nombre', 'Descripción', 'Existencias (uds.)', 'Stock'), 
                                             padre = self.wids['ventana']) 
        if idproducto < 0:
            return None
        else:
            return [idproducto]

    def crear_ldv(self):
        productos = utils.buscar_producto_general(self.wids['ventana'], mostrar_precios = True)
        for producto in productos:
            try:
                tarifa = self.objeto.cliente.tarifa
                precio = tarifa.obtener_precio(producto)
            except:
                precio = producto.preciopordefecto
            cantidad = self.seleccionar_cantidad(producto)
            if cantidad == None:
                break
            if isinstance(producto, pclases.ProductoVenta):
                productoVenta = producto 
                productoCompra = None
            elif isinstance(producto, pclases.ProductoCompra):
                productoVenta = None 
                productoCompra = producto
            else:
                productoVenta = productoCompra = None
            ldv = pclases.LineaDeVenta(pedidoVenta = None,
                    albaranSalida = None, 
                    productoVenta = productoVenta,
                    productoCompra = productoCompra,
                    prefactura = self.objeto,
                    facturaVenta = None, 
                    cantidad = cantidad, 
                    precio = precio, 
                    descuento = 0)
                    #almacenOrigen = pclases.Almacen.get_almacen_principal())
            pclases.Auditoria.nuevo(ldv, self.usuario, __file__)
            descontar_existencias(ldv, nueva = True, usuario = self.usuario)
        self.actualizar_ventana()

    def crear_servicio(self):
        # Datos a pedir: Concepto, descuento y precio... Bah, el descuento que lo cambie en el TreeView.
        concepto = utils.dialogo_entrada(titulo = "CONCEPTO",
                                         texto = 'Introduzca el concepto del servicio facturable:', 
                                         padre = self.wids['ventana'])
        if concepto != None:
            precio = utils.dialogo_entrada(titulo = "PRECIO", 
                                           texto = 'Introduzca el precio unitario sin IVA del servicio:', 
                                           padre = self.wids['ventana'])
            if precio != None:
                try:
                    precio = utils._float(precio)
                    servicio = pclases.Servicio(prefactura = self.objeto, 
                                                facturaVenta = None, 
                                                concepto = concepto,
                                                precio = precio,
                                                descuento = 0)
                    pclases.Auditoria.nuevo(servicio, self.usuario, __file__)
                    # Cantidad es 1 por defecto.
                except Exception, e:
                    utils.dialogo_info(texto = """
                    Ocurrió un error al crear el servicio.                                      
                    Asegúrese de haber introducido correctamente los datos,                     
                    especialmente el precio (que no debe incluir símbolos                       
                    monetarios), y vuelva a intentarlo.

                    DEBUG:
                    %s
                    """ %(e), 
                                       titulo = "ERROR", 
                                       padre = self.wids['ventana'])
                    return
                self.rellenar_servicios()
                self.rellenar_vencimientos()    # Para que verifique si los totales coinciden

    def cambiar_concepto_srv(self, cell, path, texto):
        model = self.wids['tv_servicios'].get_model()
        idsrv = model[path][-1]
        srv = pclases.Servicio.get(idsrv)
        srv.concepto = texto
        self.rellenar_servicios()

    def cambiar_cantidad_srv(self, cell, path, texto):
        model = self.wids['tv_servicios'].get_model()
        idsrv = model[path][-1]
        srv = pclases.Servicio.get(idsrv)
        try:
            srv.cantidad = utils._float(texto)
            srv.syncUpdate()
            # self.rellenar_servicios()
            model[path][0] = srv.cantidad
            model[path][4] = srv.precio * (1.0 - srv.descuento) * srv.cantidad
            self.rellenar_totales()
            self.rellenar_vencimientos()    # Para que verifique si los totales coinciden
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", texto = 'Formato numérico incorrecto', padre = self.wids['ventana'])

    def cambiar_precio_srv(self, cell, path, texto):
        model = self.wids['tv_servicios'].get_model()
        idsrv = model[path][-1]
        srv = pclases.Servicio.get(idsrv)
        try:
            srv.precio = utils._float(texto)
            # print srv.precio, utils._float(texto), texto
            self.rellenar_servicios()
            self.rellenar_vencimientos()    # Para que verifique si los totales coinciden
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", texto = 'Formato numérico incorrecto', padre = self.wids['ventana'])

    def cambiar_descuento_srv(self, cell, path, texto):
        model = self.wids['tv_servicios'].get_model()
        idsrv = model[path][-1]
        srv = pclases.Servicio.get(idsrv)
        try:
            try:
                srv.descuento = utils.parse_porcentaje(texto)
            except ValueError:
                srv.descuento = 0
            if srv.descuento > 1.0:
                srv.descuento /= 100.0
            self.rellenar_servicios()
            self.rellenar_vencimientos()    # Para que verifique si los totales coinciden
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", texto = 'Formato numérico incorrecto', padre = self.wids['ventana'])

    def rellenar_servicios(self):
        model = self.wids['tv_servicios'].get_model()
        model.clear()
        for servicio in self.objeto.servicios:
            # print servicio.precio, utils._float(servicio.precio)
            model.append((servicio.cantidad,
                          servicio.concepto, 
                          servicio.precio, 
                          servicio.descuento, 
                          servicio.precio * (1.0 - servicio.descuento) * servicio.cantidad,
                          servicio.id))
        self.rellenar_totales()

    def add_srv(self, boton):
        self.crear_servicio()

    def clon_srv(self, boton):
        """
        Busca un servicio existente en la BD (previamente facturado, 
        por tanto) y crea un nuevo servicio idéntico pero asociado a
        la factura actual.
        """
        a_buscar = utils.dialogo_entrada(titulo = 'BUSCAR SERVICIO FACTURADO',
                                         texto = 'Introduzca un concepto (o parte) ya facturado:', 
                                         padre = self.wids['ventana'])
        servicios = pclases.Servicio.select(pclases.Servicio.q.concepto.contains(a_buscar), orderBy = "concepto")
        filas = [(s.id,
                  s.concepto, 
                  s.precio, 
                  (s.prefactura and s.prefactura.numfactura) or (s.prefactura and s.prefactura.numfactura) or '', 
                  (s.prefactura and s.prefactura.cliente and s.prefactura.cliente.nombre) or 
                    (s.prefactura and s.prefactura.cliente and s.prefactura.cliente.nombre) or '')
                  for s in servicios]
        res = utils.dialogo_resultado(filas,
                                      "SELECCIONE SERVICIO",
                                      cabeceras = ('ID', 'Concepto', 'Precio', 'Facturado en', 'Cliente'),
                                      multi = True, 
                                      padre = self.wids['ventana'])
        if res[0] > 0:
            for idservicio in res:
                servicio = pclases.Servicio.get(idservicio)
                nuevo_servicio = pclases.Servicio(prefactura = self.objeto, 
                                                  facturaVenta = None, 
                                                  concepto = servicio.concepto,
                                                  precio = servicio.precio,
                                                  descuento = servicio.descuento)
                pclases.Auditoria.nuevo(nuevo_servicio, self.usuario, __file__)
            self.rellenar_servicios()
            self.rellenar_vencimientos()    # Para que verifique si los totales coinciden
        
    def drop_srv(self, boton):
        if self.wids['tv_servicios'].get_selection().count_selected_rows() != 0:
            model, itr = self.wids['tv_servicios'].get_selection().get_selected()
            idservicio = model[itr][-1]
            servicio = pclases.Servicio.get(idservicio)
            servicio.prefactura = None
            if servicio.albaranSalida == None:
                servicio.destroy(ventana = __file__)  # No debería saltar ninguna excepción. 
            self.rellenar_servicios()
            self.rellenar_contenido()   # Por si provenía de un albarán, que vuelva a él.
        
    def add_vto(self, boton):
        """
        Pide a través de diálogos información sobre un nuevo vencimiento
        y lo inserta en la factura actual.
        """
        factura = self.objeto
        estimado = False
        fecha = utils.mostrar_calendario(padre = self.wids['ventana'])
        cantidad = float(utils.float2str(factura.importeTotal, 2)) / (len(factura.vencimientosCobro) + 1.0)
        for vto in factura.vencimientosCobro:
            vto.importe = cantidad
        if not estimado:
            vto = pclases.VencimientoCobro(prefactura = factura,
                                           facturaVenta = None, 
                                           fecha = mx.DateTime.DateTimeFrom(day = fecha[0], month = fecha[1], year = fecha[2]),
                                           importe = cantidad,
                                           observaciones = factura.cliente and factura.cliente.textoformacobro or "",
                                           cuentaOrigen = factura.cliente and factura.cliente.cuentaOrigen or None)
        else:
            vto = pclases.EstimacionCobro(prefactura = factura,
                                          facturaVenta = None, 
                                          fecha = mx.DateTime.DateTimeFrom(day = fecha[0], month = fecha[1], year = fecha[2]),
                                          importe = cantidad,
                                          observaciones = '')
        pclases.Auditoria.nuevo(vto, self.usuario, __file__)
        self.rellenar_contenido()
        
    def drop_vto(self, boton):
        """
        Me cargo los vencimientos (estimado y no) que estén
        en la línea seleccionada. El pago no lo toco.
        """
        model, itr = self.wids['tv_vencimientos'].get_selection().get_selected()
        if itr == None: return
        ids = model[itr][-1]
        ids = [int(i) for i in ids.split(',')]
        idvto = ids[0]
        idest = ids[1]
        if idvto > 0:    # Si realmente hay un vto. (ver rellenar_vencimientos).
            vto = pclases.VencimientoCobro.get(idvto)
            vto.destroy(ventana = __file__)
        if idest > 0:
            est = pclases.EstimacionCobro.get(idest)
            est.destroy(ventana = __file__)
        self.rellenar_contenido()

    def cambiar_vto(self, cell, path, texto):
        """
        Cambia la fecha del vencimiento por la 
        nueva introducida por teclado.
        """
        try:
            fecha = utils.parse_fecha(texto)
        except ValueError:
            utils.dialogo_info('ERROR EN FORMATO DE FECHA', 'Introduzca las fechas separadas por / y en la forma dia/mes/año.', padre = self.wids['ventana'])
            return
        idvto = int(self.wids['tv_vencimientos'].get_model()[path][-1].split(',')[0])   # WTF?
            # Al escribirlo no parecía tan lioso. Lo juro.
        if idvto > 0:    # Es -1 si no había.
            vto = pclases.VencimientoCobro.get(idvto)
            vto.fecha = fecha
        elif idvto == -1:    # Para el resto de valores rebota-rebota y en tu culo explota.
            factura = self.objeto
            vto = pclases.VencimientoCobro(fecha = fecha,
                                           prefactura = factura, 
                                           facturaVenta = None, 
                                           importe = 0,
                                           observaciones = factura.cliente and factura.cliente.textoformacobro or "",
                                           cuentaOrigen = factura.cliente and factura.cliente.cuentaOrigen or None)
            pclases.Auditoria.nuevo(vto, self.usuario, __file__)
        self.rellenar_vencimientos()        # Para no sobrecargar mucho la red volviendo a rellenar LDVs y tal.

    def cambiar_estimado(self, cell, path, texto):
        """
        Cambia la fecha del vencimiento estimado
        por la nueva introducida por teclado.
        """
        try:
            fecha = utils.parse_fecha(texto)
        except ValueError:
            utils.dialogo_info('ERROR EN FORMATO DE FECHA', 'Introduzca las fechas separadas por / y en la forma dia/mes/año.', padre = self.wids['ventana'])
            return
        idvto = int(self.wids['tv_vencimientos'].get_model()[path][-1].split(',')[1])
            # Al escribirlo no parecía tan lioso. Lo juro.
        if idvto > 0:    # Es -1 si no había.
            vto = pclases.EstimacionCobro.get(idvto)
            vto.fecha = fecha
        elif idvto == -1:    # Para el resto de valores rebota-rebota y en tu culo explota.
            factura = self.objeto
            vto = pclases.EstimacionCobro(fecha = fecha,
                                          prefactura = factura, 
                                          facturaVenta = None, 
                                          importe = 0)
            pclases.Auditoria.nuevo(vto, self.usuario, __file__)
        self.rellenar_vencimientos()

    def cambiar_cobro(self, cell, path, texto):
        """
        Cambia la fecha del cobro 
        por la nueva introducida por teclado.
        """
        idcobro = int(self.wids['tv_vencimientos'].get_model()[path][-1].split(',')[2])
            # Al escribirlo no parecía tan lioso. Lo juro.
        if texto == "":
            # Texto vacío, borrar pago si lo había.
            if idcobro > 0:
                cobro = pclases.Cobro.get(idcobro)
                cobro.destroy(ventana = __file__)
                self.rellenar_vencimientos()
                return
        try:
            fecha = utils.parse_fecha(texto)
        except ValueError:
            utils.dialogo_info('ERROR EN FORMATO DE FECHA', 'Introduzca las fechas separadas por / y en la forma dia/mes/año.', padre = self.wids['ventana'])
            return
        if idcobro > 0:    # Es -1 si no había.
            cobro = pclases.Cobro.get(idcobro)
            cobro.fecha = fecha
        elif idcobro == -1:    # Para el resto de valores rebota-rebota y en tu culo explota.
            factura = self.objeto
            cobro = pclases.Cobro(fecha = fecha,
                                  prefactura = factura,
                                  facturaVenta = None, 
                                  importe = 0, 
                                  facturaDeAbono = None, 
                                  cliente = 
                                    factura and factura.cliente or None)
            pclases.Auditoria.nuevo(cobro, self.usuario, __file__)
        self.rellenar_vencimientos()

    def cambiar_importe_cobro(self, cell, path, texto):
        idcobro = int(self.wids['tv_vencimientos'].get_model()[path][-1].split(',')[2])
            # Al escribirlo no parecía tan lioso. Lo juro.
        if texto == "":
            # Texto vacío, borrar pago si lo había.
            if idcobro > 0:
                cobro = pclases.Cobro.get(idcobro)
                cobro.destroy(ventana = __file__)
                self.rellenar_vencimientos()
                return
        try:
            importe = utils._float(texto)
        except ValueError:
            utils.dialogo_info('ERROR EN FORMATO NUMÉRICO', 'Introduzca un número sin símbolo de moneda.')
            return
        if idcobro > 0:    # Es -1 si no había.
            cobro = pclases.Cobro.get(idcobro)
            cobro.importe = importe
        elif idcobro == -1:    # Para el resto de valores rebota-rebota y en tu culo explota.
            factura = self.objeto
            cobro = pclases.Cobro(fecha = time.localtime(),
                                  prefactura = factura, 
                                  facturaVenta = None, 
                                  importe = importe, 
                                  facturaDeAbono = None, 
                                  cliente = 
                                    factura and factura.cliente or None)
            pclases.Auditoria.nuevo(cobro, self.usuario, __file__)
        self.rellenar_vencimientos()
   
    def cambiar_cuenta_transferencia(self, cell, path, texto):
        """
        Busca una cuenta de la empresa a partir del texto introducido y la 
        relaciona con el vencimiento de la fila.
        """
        model = self.wids['tv_vencimientos'].get_model()
        idvto = int(model[path][-1].split(',')[0])
        if idvto > 0:
            vto = pclases.VencimientoCobro.get(idvto)
            if texto.strip() == "":
                vto.cuentaOrigen = None
                model[path][3] = ""
            else:
                cuentaOrigen = buscar_cuentaOrigen(texto, self.wids['ventana'])
                if cuentaOrigen != None:
                    vto.cuentaOrigen = cuentaOrigen
                    model[path][3] = vto.cuentaOrigen.get_info()
        else:
            utils.dialogo_info(titulo = "VENCIMIENTO INCORRECTO", texto = "Seleccione un vencimiento válido.", padre = self.wids['ventana'])
    
    def cambiar_observaciones_vto(self, cell, path, texto):
        model = self.wids['tv_vencimientos'].get_model() 
        idvto = int(model[path][-1].split(',')[0])
        if idvto > 0:
            vto = pclases.VencimientoCobro.get(idvto)
            vto.observaciones = texto
            model[path][2] = vto.observaciones
        else:
            utils.dialogo_info(titulo = "VENCIMIENTO INCORRECTO", texto = "Seleccione un vencimiento válido.", padre = self.wids['ventana'])
        # self.rellenar_vencimientos()

    def cambiar_observaciones(self, cell, path, texto):
        model = self.wids['tv_vencimientos'].get_model() 
        idcobro = int(model[path][-1].split(',')[2])
        if idcobro > 0:
            cobro = pclases.Cobro.get(idcobro)
            cobro.observaciones = texto
            model[path][-2] = cobro.observaciones
        else:
            utils.dialogo_info(titulo = "VENCIMIENTO NO COBRADO", texto = "El vencimiento está pendiente de cobro.\nIntroduzca una fecha de cobro y vuelva a intentarlo.", padre = self.wids['ventana'])

    def crear_vencimientos_por_defecto(self, w):
        """
        Crea e inserta los vencimientos por defecto
        definidos por el cliente en la factura
        actual y en función de las LDV que tenga
        en ese momento (concretamente del valor
        del total de la ventana calculado a partir
        de las LDV.)
        """
        # TODO: Refactorizar esto y hacer el cálculo del día del vencimiento un método. 
        factura = self.objeto
        cliente = factura.cliente
        if cliente.vencimientos != None and cliente.vencimientos != '':
            try:
                vtos = cliente.get_vencimientos(factura.fecha)
            except:
                utils.dialogo_info('ERROR VENCIMIENTOS POR DEFECTO', 'Los vencimientos por defecto del cliente no se pudieron procesar correctamente.\nVerifique que están bien escritos y el formato es correcto en la ventana de clientes.', padre = self.wids['ventana'])
                return    # Los vencimientos no son válidos o no tiene.
            self.borrar_vencimientos_y_estimaciones(factura)
            total = utils._float(self.wids['e_total'].get_text().replace("€", ""))
            numvtos = len(vtos)
            cantidad = total/numvtos
            if not factura.fecha:
                factura.fecha = time.localtime()
            if cliente.diadepago != None and cliente.diadepago != '':
                diaest = cliente.get_dias_de_pago()
            else:
                diaest = False
            for incr in vtos:
                fechavto = factura.fecha + (incr * mx.DateTime.oneDay)
                vto = pclases.VencimientoCobro(fecha = fechavto,
                                               importe = cantidad,
                                               prefactura = factura, 
                                               facturaVenta = None, 
                                               observaciones = factura.cliente and factura.cliente.textoformacobro or "", 
                                               cuentaOrigen = factura.cliente and factura.cliente.cuentaOrigen or None)
                pclases.Auditoria.nuevo(vto, self.usuario, __file__)
                if diaest:
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
                        # print utils.str_fecha(fechavto), utils.str_fecha(fechaest)
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
                                fechaest = mx.DateTime.DateTimeFrom(day = -1, month = mes, year = anno)
                        fechas_est.append(fechaest)
                    fechas_est.sort(utils.cmp_mxDateTime)
                    fechaest = fechas_est[0]
                    vto.fecha = fechaest 
            self.rellenar_vencimientos()
        else:
            utils.dialogo_info(titulo = "SIN DATOS", texto = "El cliente no tiene datos suficientes para crear vencimientos por defecto.", padre = self.wids['ventana'])
        
    def cambiar_descripcion_complementaria(self, cell, path, texto):
        if self.usuario != None and self.usuario.nivel > 2:
            utils.dialogo_info(titulo = "CAMBIO NO PERMITIDO", 
                               texto = "No tiene suficiente nivel de privilegios para establecer una descripción complementaria.", 
                               padre = self.wids['ventana'])
        else:
            idldv = self.wids['tv_ldvs'].get_model()[path][-1]
            pclases.LineaDeVenta.get(idldv).descripcionComplementaria = texto
            self.rellenar_ldvs()

    def cambiar_cantidad_ldv(self, cell, path, texto):
        """
        Cambia la cantidad, etcétera etcétera.
        """
        if self.usuario != None and self.usuario.nivel > 2:
            utils.dialogo_info(titulo = "CAMBIO NO PERMITIDO", 
                               texto = "No tiene suficiente nivel de privilegios para cambiar la cantidad.", 
                               padre = self.wids['ventana'])
        else:
            # Truqui:
            if "/" in texto:
                num, den = texto.split('/')
                try:
                    num = float(num)
                    den = float(den)
                    texto = num/den
                except ValueError:
                    utils.dialogo_info('ERROR EN FORMATO', 'La única operación soportada es la división y debe usarse con el siguiente formato: x/y', padre = self.wids['ventana'])
                    return
            try:
                cantidad = utils._float(texto)
            except ValueError:
                utils.dialogo_info('ERROR EN FORMATO', 'Introduzca el importe usando el punto (.) como separador decimal y sin símbolos de separación de millares ni monetarios.', padre = self.wids['ventana'])
                return
            idldv = self.wids['tv_ldvs'].get_model()[path][-1]
            ldv = pclases.LineaDeVenta.get(idldv)
            cantidad_anterior = ldv.cantidad
            ldv.cantidad = cantidad
            ajustar_existencias(ldv, cantidad_anterior)
            ldv.sync()
            self.rellenar_ldvs()

    def cambiar_cantidad(self, cell, path, texto):
        """
        Cambia la cantidad, etcétera etcétera.
        """
        # Truqui:
        if "/" in texto:
            num, den = texto.split('/')
            try:
                num = float(num)
                den = float(den)
                texto = num/den
            except ValueError:
                utils.dialogo_info('ERROR EN FORMATO', 'Introduzca el importe usando el punto (.) como separador decimal y sin símbolos de separación de millares ni monetarios.', padre = self.wids['ventana'])
                return
        try:
            cantidad = utils._float(texto)
        except ValueError:
            utils.dialogo_info('ERROR EN FORMATO', 'Introduzca el importe usando el punto (.) como separador decimal y sin símbolos de separación de millares ni monetarios.', padre = self.wids['ventana'])
            return
        idvto = int(self.wids['tv_vencimientos'].get_model()[path][-1].split(',')[0])
            # Al escribirlo no parecía tan lioso. Lo juro.
        if idvto > 0:    # Es -1 si no había.
            vto = pclases.VencimientoCobro.get(idvto)
            vto.importe = cantidad
        elif idvto == -1:    # Para el resto de valores rebota-rebota y en tu culo explota.
            factura = self.objeto
            vto = pclases.VencimientoCobro(fecha = time.localtime(),
                                           prefactura = factura, 
                                           facturaVenta = None, 
                                           importe = cantidad,
                                           observaciones = factura.cliente and factura.cliente.textoformacobro or "", 
                                           cuentaOrigen = factura.cliente and factura.cliente.cuentaOrigen or None)
            pclases.Auditoria.nuevo(vto, self.usuario, __file__)
        self.rellenar_vencimientos()        # Para no sobrecargar mucho la red volviendo a rellenar LDVs y tal.

    def cambiar_precio(self, cell, path, texto):
        """
        Cambia el precio y el total de la LDV seleccionada
        en "tv_ldvs".
        """
        model = self.wids['tv_ldvs'].get_model()
        try:
            cantidad = utils._float(texto)
        except ValueError:
            utils.dialogo_info('ERROR EN FORMATO', 'Introduzca el importe usando el punto (.) como separador decimal y sin símbolos de separación de millares ni monetarios.', padre = self.wids['ventana'])
            return
        idldv = model[path][-1]
        ldv = pclases.LineaDeVenta.get(idldv)
        if not ldv.pedidoVentaID or (ldv.pedidoVentaID and not ldv.pedidoVenta.bloqueado):
            ldv.precio = cantidad
            self.rellenar_ldvs()
            self.rellenar_vencimientos()    # Para que verifique si los totales coinciden
        else:
            if self.usuario and self.usuario.nivel >= 2:
                utils.dialogo_info(titulo = "OPERACIÓN NO PERMITIDA",
                                   texto = "El pedido de venta (%s) se encuentra bloqueado.\nCambie el precio allí o desbloquéelo primero." % (ldv.pedidoVenta.numpedido),
                                   padre = self.wids['ventana'])
            else:
                if utils.dialogo(titulo = "PEDIDO BLOQUEADO", 
                                 texto = """
                                                                                            
                    El pedido de venta relacionado (%s) se encuentra 
                    verificado y bloqueado.                                                 
                                                                                            
                    ¿Está seguro de que quiere cambiar el precio?                           
                                                                                            
                    """ % (ldv.pedidoVenta.numpedido), 
                                padre = self.wids['ventana']):
                    ldv.precio = cantidad
                    self.rellenar_ldvs()
                    self.rellenar_vencimientos()    # Redundante. Esto se puede refactorizar. ¿Es hora de probar el Bicycle Repair Man?

    def cambiar_descuento(self, cell, path, texto):
        """
        Cambia el descuento y el total de la LDV seleccionada
        en "tv_ldvs".
        """
        model = self.wids['tv_ldvs'].get_model()
        if "=" in texto:
            texto = str(eval(texto.replace("=", "")))
        try:
            cantidad = utils.parse_porcentaje(texto)
            if cantidad > 1: cantidad /= 100.0
        except ValueError:
            utils.dialogo_info('ERROR EN FORMATO', 'Introduzca el descuento como número seguido de % o\ncomo fracción de la unidad (por ejemplo: 10% ó 0.1).', padre = self.wids['ventana'])
            return
        idldv = model[path][-1]
        ldv = pclases.LineaDeVenta.get(idldv)
        if (ldv.pedidoVenta and not ldv.pedidoVenta.bloqueado) or self.usuario == None:
            ldv.descuento = cantidad
            self.rellenar_ldvs()
            self.rellenar_vencimientos()    # Para que verifique si los totales coinciden
        else:
            condicion_modificacion = self.usuario
            try:
                ventana = pclases.Ventana.selectBy(fichero = "prefacturas.py")[0]
            except:
                pass
            else:
                if self.usuario:
                    permisos = self.usuario.get_permiso(ventana)
                    condicion_modificacion = condicion_modificacion and \
                                            (permisos.escritura or (permisos.nuevo and self.objeto == self._objetoreciencreado))
                    condicion_modificacion = condicion_modificacion or self.usuario.nivel <= 2
                if not condicion_modificacion and self.usuario != None:
                    utils.dialogo_info(titulo = "OPERACIÓN NO PERMITIDA",
                                       texto = "No tiene privilegios suficientes para cambiar el descuento.",
                                       padre = self.wids['ventana'])
                else:
                    ldv.descuento = cantidad
                    self.rellenar_ldvs()
                    self.rellenar_vencimientos()    # Para que verifique si los totales coinciden



    def get_str_pedidos_albaranes(self):
        """
        Devuelve una cadena con los pedidos y albaranes entre paréntesis de las 
        LDV de la factura.
        """
        factura = self.objeto 
        peds = {'-': []}
        for ldv in factura.lineasDeVenta:
            if ldv.pedidoVenta == None and ldv.albaranSalida != None and ldv.albaranSalida.numalbaran not in peds['-']:
                peds['-'].append(ldv.albaranSalida.numalbaran)
            elif ldv.pedidoVenta != None:
                if ldv.pedidoVenta.numpedido not in peds:
                    peds[ldv.pedidoVenta.numpedido] = []
                if ldv.albaranSalida != None:
                    if not ldv.albaranSalida.numalbaran in peds[ldv.pedidoVenta.numpedido]:
                        peds[ldv.pedidoVenta.numpedido].append(ldv.albaranSalida.numalbaran)
        pedsalbs = ""
        for p in peds:
            if p == '-' and peds[p] == []:
                continue
            pedsalbs += "%s(%s) " % (p, ','.join(peds[p]))
        return pedsalbs

    def imprimir(self, boton):
        """
        Prepara los datos para llamar al generador de informes
        """
        if self.objeto is None:
            return
        self.guardar(None)  # Si se ha olvidado guardar, guardo yo.
        factura = self.objeto
        if len(factura.vencimientosCobro) == 0:
            self.crear_vencimientos_por_defecto(None)
            if len(factura.vencimientosCobro) == 0:
                v = pclases.VencimientoCobro(fecha = factura.fecha, 
                        prefactura = factura, 
                        facturaVenta = None, 
                        importe = factura.importeTotal, 
                        observaciones = factura.cliente 
                                        and factura.cliente.textoformacobro 
                                        or "", 
                        cuentaOrigen = factura.cliente 
                                        and factura.cliente.cuentaOrigen 
                                        or None)
                pclases.Auditoria.nuevo(v, self.usuario, __file__)
            self.rellenar_vencimientos()
        cliente = {'numcli':str(factura.cliente.id),
                   'nombre':factura.cliente.nombre,
                   'nombref':factura.cliente.nombref,
                   'cif':factura.cliente.cif,
                   'direccion':factura.cliente.direccion,
                   'cp':factura.cliente.cp,
                   'localidad':factura.cliente.ciudad,
                   'provincia':factura.cliente.provincia,
                   'pais':factura.cliente.pais,
                   'telf':factura.cliente.telefono,
                   'fax':'',
                   'direccionf':factura.cliente.direccionfacturacion,
                   'cpf':factura.cliente.cpfacturacion,
                   'localidadf':factura.cliente.ciudadfacturacion,
                   'provinciaf':factura.cliente.provinciafacturacion,
                   'paisf':factura.cliente.paisfacturacion}
        numpeds = self.get_str_pedidos_albaranes()
        facdata = {'facnum':factura.numfactura,
                   'fecha':utils.str_fecha(factura.fecha),
                   'pedido':numpeds,
                   'albaranes':'',
                   'observaciones': factura.observaciones}
        # desglosar_albaranes = (len(factura.get_albaranes(incluir_nones = True)) > 1 and 
        #                        utils.dialogo(titulo = "¿DESGLOSAR ALBARANES?", 
        #                                      texto = "La factura contiene más de un albarán.\n¿Desea desglosarlos en el detalle?", 
        #                                      padre = self.wids['ventana']))
        # CWT: *Ahora* prefiere el deslose por pedidos en vez de por albaranes.
        desglosar_pedidos=(len(factura.get_pedidos(incluir_nones = True))>1 and 
                           utils.dialogo(titulo = "¿DESGLOSAR PEDIDOS?", 
                            texto = "La factura contiene más de un pedido.\n¿"
                                    "Desea desglosarlos en el detalle?", 
                            padre = self.wids['ventana']))
        lineas = []
        if desglosar_pedidos:
            pedidos = desglosar_ldvs_por_pedido(factura.lineasDeVenta)
            for p in pedidos:
                if len(pedidos) > 1:  # No quiero desglose si solo hay un albarán.
                    # Encabezado albarán: Número de albarán, fecha y pedidos que contiene.
                    linea = {'codigo': "<formatolinea>cin</formatolinea>", 
                             'cantidad': "", 
                             'descripcion': p and "Pedido: %s - Fecha: %s" % (p.numpedido, utils.str_fecha(p.fecha)) \
                                              or "Ventas sin pedido", 
                             'precio': "", 
                             'descuento': ""}
                    lineas.append(linea)
                # Líneas de venta del albarán:
                for l in pedidos[p]:
                    linea = {'codigo': l.producto.codigo,
                             'cantidad': l.cantidad,
                             'descripcion': l.producto.descripcion,
                             #'precio': l.precio,
                             'precio': l.calcular_precio_unitario_coherente(),
                             'descuento': str(l.descuento)}
                    if l.descripcionComplementaria:
                        linea['descripcion'] += " (%s)" % l.descripcionComplementaria
                    lineas.append(linea)
                if len(pedidos) > 1:  # No quiero desglose si solo hay un albarán.
                    # Pie del albarán: Total del mismo sin IVA.
                    linea = {'codigo': "<formatolinea>di</formatolinea>", 
                             'cantidad': "", 
                             'descripcion': "Subtotal %s(s/IVA)" % (p and "pedido %s " % (p.numpedido) or ""), 
                             'precio': p and p.calcular_importe_total(iva = False) \
                                         or sum([l.precio * l.cantidad * (1 - l.descuento) for l in pedidos[p]]), 
                             'descuento': ""}
                    lineas.append(linea)
        else:
            lineasdeventa = [ldv for ldv in factura.lineasDeVenta]
            lineasdeventa.sort(utils.f_sort_id)
            for l in lineasdeventa:
                linea = {'codigo': l.producto.codigo,
                         'cantidad': l.cantidad,
                         'descripcion': l.producto.descripcion,
                         'precio': l.calcular_precio_unitario_coherente(),
                         #'precio': l.precio,
                         'descuento': str(l.descuento)}
                if l.descripcionComplementaria:
                    linea['descripcion'] += " (%s)" % l.descripcionComplementaria
                lineas.append(linea)
        if factura.cliente.es_extranjero() and factura.iva == 0:
                # CWT: Doble comprobación. Debe ser extranjero y el IVA 0 (aunque una cosa implica la otra, la verdad).
            arancel_lista = [ldv.productoVenta.arancel for ldv in factura.lineasDeVenta \
                             if ldv.productoVentaID and ldv.productoVenta.arancel != "" and ldv.productoVenta.arancel != None]
            # OJO: NOTA: El arancel es siempre el mismo. Muestro el del primer articulo que encuentre con arancel != "".
            if arancel_lista != []:
                arancel = arancel_lista[0]
            else:
                arancel = None
        else:
            arancel = None
        for l in factura.servicios:
            descripcion = l.concepto
            linea = {'codigo': "",
                     'cantidad': l.cantidad,
                     'descripcion': descripcion,
                     'precio': l.precio,
                     'descuento': str(l.descuento)}
            lineas.append(linea)
        # fechasVencimiento = (', '.join([utils.str_fecha(v.fecha) for v in factura.vencimientosCobro]))
        # documentos = ', '.join(["%s %s" % (v.observaciones, v.cuentaOrigen and "%s: %s" % (v.cuentaOrigen.banco, v.cuentaOrigen.ccc) or "") for v in factura.vencimientosCobro])
        fechasVencimiento = []
        documentosDePago = []
        for fila_vto in self.wids['tv_vencimientos'].get_model():
            idvto = int(fila_vto[-1].split(',')[0])
            if idvto > 0:
                vto = pclases.VencimientoCobro.get(idvto)
                fechasVencimiento.append("%s (%s €)" % (utils.str_fecha(vto.fecha), utils.float2str(vto.importe)))
                if vto.cuentaOrigen:
                    cuenta = "a %s %s" % (vto.cuentaOrigen.banco, vto.cuentaOrigen.ccc)
                else:
                    cuenta = ""
                documentosDePago.append("%s %s" % (vto.observaciones, cuenta))
        documentosDePago = utils.unificar(documentosDePago)
        vencimiento = {'fecha': "; ".join(fechasVencimiento),
                       'pago': factura.cliente.vencimientos,
                       'documento': "; ".join(documentosDePago)}
        from formularios import numerals
        total = self.wids['e_total'].get_text()
        total = total.replace('€', '')
        total = total.replace(' ', '')
        totalfra = utils._float(total)   # Si ya lo tengo aquí calculado... ¿para qué volver a hacerlo?
        totales = {}
        totales['subtotal'] = self.wids['e_subtotal'].get_text()
        cargo = self.wids['e_cargo'].get_text()
        if cargo == '0.00 €' or cargo == '0,00 €':
            cargo = None
        totales['cargo'] = cargo
        descuento = self.wids['e_tot_dto'].get_text()
        if descuento == '-0.00 €' or descuento == '0.00 €' or \
           descuento == '-0,00 €' or descuento == '0,00 €':         # WFT !!!!!
            descuento = None
        else:
            descuento = descuento+' ('+self.wids['e_descuento'].get_text()+')'
        totales['descuento'] = descuento
        totales['iva'] = self.wids['e_iva'].get_text()
        totales['totaliva'] = self.wids['e_total_iva'].get_text()
        totales['total'] = self.wids['e_total'].get_text()
        totales['irpf'] = self.wids['e_irpf'].get_text()
        totales['totirpf'] = self.wids['e_total_irpf'].get_text()
        texto = numerals.numerals(totalfra, moneda = "euros", fraccion = "céntimos").upper()
        if len(lineas) > 0:
            nomarchivo = geninformes.prefactura(cliente, 
                                                facdata, 
                                                lineas, 
                                                arancel, 
                                                vencimiento, 
                                                texto, 
                                                totales)
            self.abrir_factura_imprimida(nomarchivo)
            if not self.objeto.bloqueada:
                txt = """
                    Verifique minuciosamente la factura impresa.                                    
                                                                                                    
                    Si es correcta, responda "sí" para bloquear la factura.                         
                                                                                                    
                    En otro caso responda "no". La factura quedará entonces                         
                    pendiente de verificar hasta que sea imprimida correctamente.                   
                                                                                                    
                                                                                                    
                    ¿Se imprimió correctamente la factura?                                          
                                                                                                    
                    """
                if utils.dialogo(titulo = "¿ES CORRECTA LA FACTURA?",
                                 texto = txt, 
                                 padre = self.wids['ventana']):
                    self.objeto.bloqueada = True
                    bloquear_albaranes(factura)
                    self.objeto.make_swap()
                    self.actualizar_ventana()
        else:
            utils.dialogo_info(titulo = "FACTURA VACÍA", 
                               texto = "La factura está vacía. Se canceló la impresión.", 
                               padre = self.wids['ventana'])
    
    def abrir_factura_imprimida(self, nomarchivo):
        """
        Muestra la factura generada en PDF.
        """
        from formularios import reports
        reports.abrir_pdf(nomarchivo)

    def buscar_abonos(self, w):
        """
        Busca facturas de abono en la base de datos para que el usuario 
        pueda agregar una o varias a la factura de venta actual.
        Crea los pagos de abono correspondientes que se muestran en 
        la ventana.
        """
        cliente = self.objeto.cliente
        abonos = pclases.Abono.select(pclases.AND(pclases.Abono.q.clienteID == cliente.id,
                                                    pclases.Abono.q.facturaDeAbonoID != None))
        # Si tienen pagos de abono en la factura de abono es que ya se ha usado en otra factura.
        abonos = [a for a in abonos if a.facturaDeAbono.pagosDeAbono == []]
        # NOTA: OJO: Una factura de abono, un abono.
        filas = [(a.facturaDeAbono.id,
                  utils.str_fecha(a.facturaDeAbono.fecha),
                  a.numabono,
                  utils.str_fecha(a.fecha)) 
                 for a in abonos if a.facturaDeAbono != None]
        fas = utils.dialogo_resultado(filas, 'SELECCIONE UNA FACTURA DE ABONO DEL CLIENTE',
                                      cabeceras = ('ID', 'Fecha de factura de abono', 'Número de abono', 'Fecha del abono'),
                                      multi = True, 
                                      padre = self.wids['ventana'])
        if fas[0] > 0:
            for faid in fas:
                fa = pclases.FacturaDeAbono.get(faid)
                # NOTA: OJO: Una factura de abono, un abono.
                importe = fa.abonos[0].importeSinIva
                pa = pclases.PagoDeAbono(prefactura = self.objeto, 
                                         facturaVenta = None, 
                                         facturaDeAbono = fa,
                                         importe = importe)
                pclases.Auditoria.nuevo(pa, self.usuario, __file__)
            self.rellenar_abonos()

    def rellenar_abonos(self):
        model = self.wids['tv_abonos'].get_model()
        model.clear()
        for pa in self.objeto.pagosDeAbono:
            model.append((pa.facturaDeAbono.abonos[0].numabono,
                          pa.importe,
                          pa.id))
        self.rellenar_totales()

    def drop_abono(self, b):
        model, itr = self.wids['tv_abonos'].get_selection().get_selected()
        if itr != None:
            idpa = model[itr][-1]
            pa = pclases.PagoDeAbono.get(idpa)
            try:
                pa.destroy(ventana = __file__)
            except:
                utils.dialogo_info(titulo = "ERROR AL ELIMINAR ABONO", texto = "Se produjo un error al eliminar el pago de abono.\nConsulte al administrador de la aplicación o inténtelo de nuevo después de cerrar y volver a abrir la ventana.", padre = self.wids['ventana'])
                # Capturar una excepción para mostrar un simple diálogo es digno de un artículo de 
                # lazy programmers de Joel on software, pero es que este caso NO DEBERÍA OCURRIR.
            self.rellenar_abonos()

def desglosar_ldvs_por_pedido(ldvs):
    """
    Devuelve un diccionario con las LDVs por pedido. Para las 
    LDV sin pedido el diccionario contiene una clave None con 
    las mismas.
    """
    res = {}
    ldvs.sort(utils.f_sort_id)
    for ldv in ldvs:
        ped = ldv.pedidoVenta
        if ped not in res:
            res[ped] = (ldv, )
        else:
            res[ped] += (ldv, )
    return res

def desglosar_ldvs_por_albaran(ldvs):
    """
    Devuelve un diccionario con las LDVs por albarán. Para las 
    LDV sin albarán el diccionario contiene una clave None con 
    las mismas.
    """
    res = {}
    ldvs.sort(utils.f_sort_id)
    for ldv in ldvs:
        alb = ldv.albaranSalida
        if alb not in res:
            res[alb] = (ldv, )
        else:
            res[alb] += (ldv, )
    return res

def descontar_existencias(ldv, nueva = False, usuario = None):
    """
    Usado al crear o actualizar una LDV manualmente.
    Si el producto es un producto de venta no «especial», o se 
    ha descontado en un albarán externo o interesa hacerlo manualmente 
    por un ajuste de existencias, una preventa, etc. Al ser control de 
    existencias de los PV basado en la contabilidad de productos 
    individuales, las existencias no se alteran (no se crean ni 
    destruyen objetos artículo).
    Si el producto es un producto de compra con control de existencias 
    por software o un producto especial, se busca un albarán de salida 
    del cliente de la factura donde asignar la [nueva] ldv y se actualizan 
    las existencias.
    El albarán de salida se determina según:
        - Si la factura no tiene albaranes asociados no bloqueados, 
          creo uno con la fecha de la factura.
        - Si tiene albaranes no bloqueados, elijo el de la fecha más 
          cercana a la factura.
    El albarán que se cree (y el resto de albaranes en general) se bloqueará 
    al bloquear la factura siempre y cuando no tenga líneas pendientes de 
    facturar (ver).
    """
    if ((isinstance(ldv.producto, pclases.ProductoVenta) 
         and ldv.producto.es_especial())
        or isinstance(ldv.producto, pclases.ProductoCompra)):
        if nueva:
            ajustar_existencias(ldv)
        else:
            ajustar_existencias(ldv, ldv.cantidad)
    try:
        control_existencias = ldv.producto.controlExistencias
    except AttributeError:
        control_existencias = True
    if control_existencias:
        factura = ldv.facturaVenta or ldv.prefactura
        albs = [a for a in factura.get_albaranes(False, True) 
                if not a.bloqueado]
        if not albs:
            try:
                numalbaran = pclases.AlbaranSalida.get_siguiente_numero_numalbaran_str()
                alb = pclases.AlbaranSalida(destino = None, 
                                            transportista = None, 
                                            cliente = factura.cliente, 
                                            numalbaran = numalbaran, 
                                            fecha = factura.fecha, 
                                            nombre = "", 
                                            direccion = "", 
                                            cp = "", 
                                            ciudad = "", 
                                            telefono = "", 
                                            pais = "", 
                                            observaciones = "", 
                                            facturable = True, 
                                            motivo ="", 
                                            bloqueado = False)
                pclases.Auditoria.nuevo(alb, usuario, __file__)
            except Exception, msg:
                texto = """
                No se pudo crear albarán de salida número %s.
                Elimine la línea y vuelva a intentarlo. Si el 
                error persiste, cree el albarán manualmente.
                Información de depuración:
                %s
                """ % (numalbaran, msg)
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = texto, 
                                   padre = None)
                alb = None
        else:
            albs.sort(utils.cmp_mxDateTime)
            mas_cercano = albs[0]
            for a in albs:
                if a.fecha and a.fecha < factura.fecha:
                    mas_cercano = a
            alb = mas_cercano
        ldv.albaranSalida = alb

def bloquear_albaranes(f):
    """
    Si la factura está bloqueada, bloquea todos los albaranes 
    de entrada relacionados si éstos no tienen líneas pendientes 
    de facturar.
    """
    if f.bloqueada:
        for a in f.get_albaranes(False, True):
            if (a.contar_lineas_facturadas() == len(a.lineasDeVenta) 
                and len([srv for srv in a.servicios if srv.facturaVentaID == None and srv.prefacturaID == None]) == 0):
                a.bloqueado = True


if __name__ == '__main__':
    # v = Prefacturas(usuario = pclases.Usuario.select(pclases.Usuario.q.usuario.contains("Maril"))[0])
    v = Prefacturas()

