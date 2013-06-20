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
## facturas_compra.py -- Facturas de entrada de mercancía (compras). 
###################################################################
## Changelog:
## 13 de diciembre de 2005 -> Inicio
## 14 de diciembre de 2005 -> 99% funcional
## 23 de enero de 2006 -> Portado usando clase Ventana. 
## 3 de abril de 2006 -> Añadida funcionalidad de vencimientos.
## 24 de mayo de 2006 -> Vencimientos por defecto... fulminados.
## 21 de noviembre de 2006 -> Soporte a LDC sin albarán.
###################################################################
## DONE:
## + Falta controlar los permisos de usuario y que el director 
##   técnico no pueda cambiar el visto bueno del comercial, el 
##   comercial el del director, etc...
## + Ventana para ver facturas sin visto bueno y que los tres 
##   encargados den cada uno el suyo.
## + Ahora me entero de que pueden haber facturas con IVAs 
##   mezclados (véase 0700166 de Viajes El Monte). Se pueden 
##   meter cargando una diferencia en el descuento de la línea
##   con el IVA diferente y así cuadrar el total, pero faltaría 
##   un campo observaciones donde dejarlo anotado.
## + Meter una forma de pago en el vencimiento (sin tener que 
##   esperar a tener un registro pago relacionado) para poder 
##   filtrar pagarés pendientes o transferencias pendientes y 
##   saber de antemano qué documento cargar a la hora de imprimir 
##   los pagos, ya que si es "transferencia El Monte" hay que 
##   imprimir determinado documento de fax, si es "pagaré La Caixa"
##   hay que imprimir otro tipo de documento, etc...
## + Meter también una cuenta bancaria (para las transferencias y 
##   domiciliaciones) por defecto pero que se pueda cambiar para 
##   una factura concreta -por ejemplo: caso Telefónica. De las 
##   tres facturas mensuales, 2 están domiciliadas en La Caixa y 
##   la otra en El Monte-.
## + Ver qué hacer con las facturas en moneda extranjera: Meterlas
##   en euros y anotar el cambio de moneda del día en el campo
##   observaciones.
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk, time
from framework import pclases
from utils import _float as float
import mx.DateTime

class FacturasDeEntrada(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self._objetoreciencreado = None
        Ventana.__init__(self, 'facturas_compra.glade', objeto, 
                         usuario = self.usuario)
        connections = {'b_nuevo/clicked': self.crear_nueva_factura,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_buscar/clicked': self.buscar_factura,
                       'b_fecha/clicked': self.buscar_fecha,
                       'b_add_albaran/clicked': self.add_albaran,
                       'b_drop_albaran/clicked': self.drop_albaran,
                       'b_borrar/clicked': self.borrar_factura,
                       'b_salir/clicked': self._salir,
                       'ventana/delete_event': self._salir,
                       'b_add_vto/clicked': self.add_vto,
                       'b_drop_vto/clicked': self.drop_vto,
                       'b_vtos_defecto/clicked': 
                            self.crear_vencimientos_por_defecto, 
                       'b_add_ldc/clicked': self.add_linea_de_compra, 
                       'b_drop_ldc/clicked': self.drop_linea_de_compra,
                       'ch_visto_bueno_automatico/clicked': 
                            self.mostrar_visto_bueno_auto,
                       'b_fecha_visto_bueno_comercial/clicked': 
                            self.cambiar_fecha_visto_bueno, 
                       'b_fecha_visto_bueno_tecnico/clicked': 
                            self.cambiar_fecha_visto_bueno, 
                       'b_fecha_visto_bueno_director/clicked': 
                            self.cambiar_fecha_visto_bueno,
                       'b_fecha_entrada/clicked': self.cambiar_fecha_entrada,
                       'b_comisiones_y_transportes/clicked': 
                            self.add_transporte_y_comisiones, 
                       'cmbe_proveedor/changed': self.cambiar_iva_defecto, 
                       'b_comprobar_visto_bueno/clicked': 
                            self.comprobar_visto_bueno,
                       'b_add_adjunto/clicked': self.adjuntar,
                        # XXX: Código para adjuntos.
                       'b_drop_adjunto/clicked': self.drop_adjunto,
                        # XXX: Código para adjuntos.
                       'b_ver_adjunto/clicked': self.ver_adjunto,
                        # XXX: Código para adjuntos.
                       'b_reciente/pressed': self.abrir_recientes 
                      }
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        gtk.main()
    
    # XXX: Lista de objetos recientes.
    def abrir_recientes(self, boton):
        """
        Muestra un desplegable con los pedidos recientemente abiertos. Al 
        hacer clic en uno de ellos, se abre en la ventana actual.
        """
        reg = pclases.ListaObjetosRecientes.buscar("facturas_compra.py", 
                                              self.usuario) 
        if reg:
            lista = []
            ui_string = """
                        <ui>
                            <popup name='Popup'>
                        """
            for ide in reg.get_lista():
                try:
                    p = pclases.FacturaCompra.get(ide)
                except pclases.SQLObjectNotFound:
                    pass    # La factura ya no existe
                else:
                    ui_string += "<menuitem action='%s'/>" % (p.get_info())
                    lista.append((p.get_info(), p.id))
            ui_string += """
                            </popup>
                        </ui>
                        """
            ag = gtk.ActionGroup("Recientes")
            actions = []
            for info, ide in lista:
                actions.append((info, None, info, None, "Abrir " + info, 
                                self.abrir_reciente))
            ag.add_actions(actions, lista)
            ui = gtk.UIManager()
            ui.insert_action_group(ag, 0)
            ui.add_ui_from_string(ui_string)
            widget = ui.get_widget("/Popup")
            event = gtk.gdk.Event(gtk.gdk.BUTTON_PRESS)
            widget.popup(None, None, None, event.button, event.time)

    def abrir_reciente(self, action, lista):
        """
        Abre en la ventana actual la factura seleccionada en el popup.
        """
        accel_path = action.get_accel_path()
        txt_entrada = "/".join(accel_path.split("/")[2:])
        for txt, ide in lista:
            if txt == txt_entrada:
                factura = pclases.FacturaCompra.get(ide)
                # XXX: Añado a objetos recientes.
                objsr = pclases.ListaObjetosRecientes.buscar(
                                                        "facturas_compra.py", 
                                                        self.usuario, 
                                                        crear = True)
                objsr.push(factura.id)
                # XXX: End Of Añado a objetos recientes.
                if self.objeto != None:
                    self.verificar_si_vencimientos()
                self.ir_a(factura)

    # XXX: End Of Lista de objetos recientes.

    def check_permisos(self):
        """
        Activa o desactiva los controles dependiendo de los 
        permisos del usuario.
        """
        VENTANA = "facturas_compra.py"
        if self.usuario != None and self.usuario.nivel > 0:
            ventanas = pclases.Ventana.select(
                        pclases.Ventana.q.fichero == VENTANA)
            if ventanas.count() == 1:   # Siempre debería ser 1.
                permiso = self.usuario.get_permiso(ventanas[0])
                if permiso.escritura:
                    if self.usuario.nivel <= 2:
                        if pclases.DEBUG and pclases.VERBOSE:
                            print "Activo widgets para usuario con nivel "\
                                    "de privilegios <= 1."
                        self.activar_widgets(True, chequear_permisos = False)
                    else:
                        if pclases.DEBUG and pclases.VERBOSE:
                            print "Activo widgets porque permiso de "\
                                    "escritura y objeto no bloqueado o "\
                                    "recién creado."
                        self.activar_widgets(self.objeto != None 
                            and (not self.objeto.bloqueado 
                                 or self._objetoreciencreado == self.objeto), 
                            chequear_permisos = False)
                else:   # No tiene permiso de escritura. Sólo puede modificar 
                        # el objeto que acaba de crear.
                    if self._objetoreciencreado == self.objeto: 
                        if pclases.DEBUG and pclases.VERBOSE:
                            print "Activo widgets porque objeto recién creado"\
                                    " aunque no tiene permiso de escritura."
                        self.activar_widgets(True, chequear_permisos = False)
                    else:
                        if pclases.DEBUG and pclases.VERBOSE:
                            print "Desactivo widgets porque no permiso de "\
                                    "escritura."
                        self.activar_widgets(False, chequear_permisos = False)
                self.wids['b_buscar'].set_sensitive(permiso.lectura)
                # XXX: Modificación para recientes.
                self.wids['b_reciente'].set_sensitive(permiso.lectura)
                # XXX: EOModificación para recientes.
                self.wids['b_nuevo'].set_sensitive(permiso.nuevo)
        else:
            self.activar_widgets(True, chequear_permisos = False)

    def cambiar_iva_defecto(self, cb):
        """
        Cambia el IVA en la ventana y pone el del proveedor.
        """
        idproveedor = utils.combo_get_value(cb)
        if idproveedor != None and self.objeto and not self.objeto.bloqueada:
            proveedor = pclases.Proveedor.get(idproveedor)
            self.wids['e_iva'].set_text(
                    "%s %%" % (utils.float2str(proveedor.iva * 100, 0)))

    def cambiar_fecha_visto_bueno(self, boton):
        """
        Cambia la fecha del visto bueno correspondiente al botón 
        que ha ejecutado el callback.
        """
        mapa = (("tecnico", "e_fecha_visto_bueno_tecnico"),
                ("director", "e_fecha_visto_bueno_director"),
                ("comercial", "e_fecha_visto_bueno_comercial"))
        for nombre, entry in mapa:
            if nombre in boton.name:
                self.wids[entry].set_text(utils.str_fecha(
                    utils.mostrar_calendario(padre = self.wids['ventana'])))

    def mostrar_visto_bueno_auto(self, chbox):
        """
        Impide que se cambie manualmente el visto bueno automático
        mostrando siempre el valor del mismo en la factura.
        """
        chbox.set_active(self.objeto.vistoBuenoAutomatico)

    def refinar_busqueda_albaran(self, resultados):
        filas_res = []
        for r in resultados:
            if r.proveedor != None:
                proveedor = r.proveedor.nombre
            else:
                proveedor = ''
            filas_res.append((r.id, r.numalbaran, utils.str_fecha(r.fecha), 
                              proveedor, ))
        idalbaran = utils.dialogo_resultado(filas_res,
            titulo = 'Seleccione albarán',
            cabeceras = ('ID Interno', 'Num. Albarán', 'Fecha', 'Proveedor'), 
            padre = self.wids['ventana'], 
            multi = True) 
        if not idalbaran or idalbaran[0] < 0:
            return []
        else:
            return idalbaran

    def pedir_albaran(self):
        """
        Solicita un número de albarán, muestra una
        ventana de resultados coincidentes con la 
        búsqueda de ese número y devuelve uno o varios  
        albaranes seleccionados de entre
        los resultados, o None si se cancela o 
        no se encuentra.
        """
        albaran = None
        codigo = utils.dialogo_entrada('Introduzca número de albarán.', 
                                       'NÚMERO DE ALBARÁN', 
                                       padre = self.wids['ventana'])
        if codigo != None:
            albaranes = pclases.AlbaranEntrada.select(
                    pclases.AlbaranEntrada.q.numalbaran.contains(codigo))
            encontrados = albaranes.count()
            proveedor = utils.combo_get_value(self.wids['cmbe_proveedor'])
            if proveedor == None:
                albaranes = [a for a in albaranes 
                        if [ldc for ldc in a.lineasDeCompra 
                            if ldc.facturaCompra == None] != []]
            else:
                albaranes = [a for a in albaranes 
                             if [ldc for ldc in a.lineasDeCompra 
                                 if ldc.facturaCompra == None] != [] 
                                    and a.proveedorID == proveedor]
            if len(albaranes) > 1:
                idsalbaranes = self.refinar_busqueda_albaran(albaranes)
                if idsalbaranes != None and len(idsalbaranes) > 0:
                    #albaranes = [p for p in albaranes if p.ide == idalbaran]
                    albaranes = [pclases.AlbaranEntrada.get(ide) 
                                 for ide in idsalbaranes]
                else:
                    return None
            elif len(albaranes) < 1:
                if encontrados > len(albaranes):
                    if proveedor == None:
                        mens_error = "El albarán buscado ya se encuentra " \
                            "facturado. Verifíquelo desde la ventana de " \
                            "albaranes de entrada."
                    else:
                        mens_error = "El albaran buscado ya se encuentra " \
                            "facturado o no pertenece al proveedor de la " \
                            "factura.\nVerifíquelo en la ventana de " \
                            "albaranes de entrada."
                else:
                    mens_error = 'No se encontró ningún albarán con ese ' \
                                 'número.'
                utils.dialogo_info('ALBARÁN NO ENCONTRADO', 
                                   mens_error, 
                                   padre = self.wids['ventana'])
                return None
            albaran = albaranes
        return albaran

    def es_diferente(self):
        """
        Devuelve True si la información en pantalla es distinta a la
        del objeto en memoria.
        """
        # NOTA: No hay que preocuparse por el exceso de cómputo. Estas 
        # comparaciones son bastante rápidas al tener python -como los 
        # lenguajes de verdad y no los jueguetes tipo VB- las operaciones 
        # lógicas cortocircuitadas, de forma que si condición pasa a False no 
        # se evalúa lo que esté detrás del and en las instrucciones 
        # posteriores.
        factura = self.objeto
        if factura == None: return False    # Si no hay factura activo, 
                    # devuelvo que no hay cambio respecto a la ventana
        condicion = (str(factura.numfactura) 
                == self.wids['e_numfactura'].get_text())
        bounds = self.wids['txt_observaciones'].get_buffer().get_bounds()
        condicion = condicion and (
                self.wids['txt_observaciones'].get_buffer().get_text(
                    bounds[0],bounds[1]) 
                == factura.observaciones)
        condicion = condicion and (
                utils.str_fecha(factura.fecha) 
                == self.wids['e_fecha'].get_text())
        condicion = condicion and (
                utils.str_fecha(factura.fechaEntrada) 
                == self.wids['e_fecha_entrada'].get_text())
        condicion = condicion and (
                utils.combo_get_value(self.wids['cmbe_proveedor']) 
                == factura.proveedorID) 
        condicion = condicion and (
                self.wids['e_descuento'].get_text() 
                == "%s %%" % (utils.float2str(factura.descuento * 100, 
                                              autodec = True)))
        condicion = condicion and (
                self.wids['e_iva'].get_text() 
                == "%s %%" % (utils.float2str(factura.iva * 100, 0)))
        condicion = condicion and (
                self.wids['e_cargo'].get_text() 
                == utils.float2str(factura.cargo, 2))
        condicion = condicion and (
                self.wids['chk_bloqueada'].get_active() == factura.bloqueada)
        condicion = condicion and (
                self.wids['ch_visto_bueno_comercial'].get_active() 
                == factura.vistoBuenoComercial)
        condicion = condicion and (
                self.wids['ch_visto_bueno_tecnico'].get_active() 
                == factura.vistoBuenoTecnico)
        condicion = condicion and (
                self.wids['ch_visto_bueno_director'].get_active() 
                == factura.vistoBuenoDirector)
        condicion = condicion and (
                self.wids['e_fecha_visto_bueno_comercial'].get_text() 
                == utils.str_fecha(factura.fechaVistoBuenoComercial))
        condicion = condicion and (
                self.wids['e_fecha_visto_bueno_tecnico'].get_text() 
                == utils.str_fecha(factura.fechaVistoBuenoTecnico))
        condicion = condicion and (
                self.wids['e_fecha_visto_bueno_director'].get_text() 
                == utils.str_fecha(factura.fechaVistoBuenoDirector))
        return not condicion    # "condicion" verifica que sea igual


    def aviso_actualizacion(self):
        """
        Muestra una ventana modal con el mensaje de objeto 
        actualizado.
        """
        utils.dialogo_info('ACTUALIZAR',
                           'La factura ha sido modificada remotamente.\nDebe'
                           ' actualizar la información mostrada en pantalla.'
                           '\nPulse el botón «Actualizar»',
                           padre = self.wids['ventana'])
        self.wids['b_actualizar'].set_sensitive(True)

    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        import pango
        self.wids['e_numerocontrol'].modify_base(gtk.STATE_NORMAL, 
            self.wids['e_numerocontrol'].get_colormap().alloc_color("gray"))
        self.wids['e_numerocontrol'].modify_font(
            pango.FontDescription("Sans Bold 12"))
        self.wids['e_numerocontrol'].set_alignment(0.5)
        # Inicialmente no se muestra NADA. Sólo se le deja al
        # usuario la opción de buscar o crear nuevo.
        self.activar_widgets(False)
        self.wids['b_actualizar'].set_sensitive(False)
        self.wids['b_guardar'].set_sensitive(False)
        self.wids['b_nuevo'].set_sensitive(True)
        self.wids['b_buscar'].set_sensitive(True)
        # XXX: Modificación para recientes.
        self.wids['b_reciente'].set_sensitive(True)
        # XXX: EOModificación para recientes.
        # Inicialización del resto de widgets:
        provs = pclases.Proveedor.select(orderBy = 'nombre')
        lista_provs = [(p.id, p.nombre) for p in provs if not p.inhabilitado]
        utils.rellenar_lista(self.wids['cmbe_proveedor'], lista_provs)
        cols = (('Código', 'gobject.TYPE_STRING', False, True, False, None),
                ('Descripción', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_descripcion),
                ('Cantidad', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_cantidad_ldc),
                ('Precio', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_precio_ldc),
                ('IVA', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_iva_ldc),
                ('Descuento', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_descuento_ldc),
                ('Subtotal s/IVA', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Subtotal c/IVA', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Pedido', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Albarán', 'gobject.TYPE_STRING', False, True, False, None), 
                ('IDLDC', 'gobject.TYPE_INT64', False, False, False, None)
               )
        utils.preparar_treeview(self.wids['tv_ldvs'], cols)
        for n in (2, 3, 4, 5, 6, 7):
            for cel in self.wids['tv_ldvs'].get_column(n).get_cell_renderers():
                cel.set_property('xalign', 1.0)
        cols = (('Vencimiento', 'gobject.TYPE_STRING', True, True, True, 
                    self.cambiar_vto),
                ('Cantidad', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_cantidad), 
                ('Forma de pago', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_observaciones_vto),
                ('Realizado', 'gobject.TYPE_BOOLEAN', False,True,False,None),
                ('Fecha pago', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_fecha_pago),
                ('Importe del pago', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_importe_pago),
                ('Observaciones', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_observaciones),
                ('IDs', 'gobject.TYPE_STRING', False, False, False, None)
               )
                # HACK: La última columna -oculta- va a tener una cadena con 
                #       los IDs involucrados en la fila separados por coma y 
                #       como cadena para aprovechar el preparar_listview sin 
                #       tener que cambiar nada.
        utils.preparar_listview(self.wids['tv_vencimientos'], cols)
        self.wids['e_subtotal'].set_alignment(1.0)
        self.wids['e_totdescuento'].set_alignment(1.0)
        self.wids['e_totcargo'].set_alignment(1.0)
        self.wids['e_totiva'].set_alignment(1.0)
        self.wids['e_total'].set_alignment(1.0)
        cols = (('Tipo', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Número', 'gobject.TYPE_STRING', False, True, True, None),
                ('Fecha', 'gobject.TYPE_STRING', False, True, False, None),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None)
               )
        utils.preparar_listview(self.wids['tv_peds_y_albs'], cols)
        self.wids['tv_peds_y_albs'].connect("row-activated", 
                                            self.abrir_pedido_o_albaran)
        
        # XXX: Código para adjuntos:
        cols = (('Nombre', 'gobject.TYPE_STRING', True, True, True, 
                    self.cambiar_nombre_adjunto), 
                ('Observaciones', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_observaciones_adjunto),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_adjuntos'], cols)
        self.wids['tv_adjuntos'].connect("row-activated",abrir_adjunto_from_tv)
    
    # XXX: Código para adjuntos.
    def cambiar_nombre_adjunto(self, cell, path, texto): 
        model = self.wids['tv_adjuntos'].get_model() 
        iddoc = model[path][-1]
        pclases.Documento.get(iddoc).nombre = texto
        model[path][0] = pclases.Documento.get(iddoc).nombre

    # XXX: Código para adjuntos.
    def cambiar_observaciones_adjunto(self, cell, path, texto): 
        model = self.wids['tv_adjuntos'].get_model() 
        iddoc = model[path][-1]
        pclases.Documento.get(iddoc).observaciones = texto
        model[path][1] = pclases.Documento.get(iddoc).observaciones

    def cambiar_iva_ldc(self, cell, path, texto):
        try:
            iva = utils.parse_porcentaje(texto) / 100.0
        except:
            utils.dialogo_info(titulo = "ERROR", 
                    texto = "La cantidad %s no es un número válido." % (texto),
                    padre = self.wids['ventana'])
            return
        model = self.wids['tv_ldvs'].get_model()
        idldc = model[path][-1]
        if model[path].parent == None:
            if idldc != -1:
                ldc = pclases.LineaDeCompra.get(idldc)
                ldc.iva = iva
        else:
            s = pclases.ServicioTomado.get(idldc)
            s.iva = iva
        self.rellenar_widgets()

    def cambiar_descuento_ldc(self, cell, path, texto):
        try:
            descuento = utils.parse_porcentaje(texto) / 100.0
        except:
            utils.dialogo_info(titulo = "ERROR", 
                    texto = "La cantidad debe ser numérica, en fracción de la"
                            " unidad y sin símbolos de porcentaje", 
                    padre = self.wids['ventana'])
            return
        model = self.wids['tv_ldvs'].get_model()
        idldc = model[path][-1]
        if model[path].parent == None:
            if idldc != -1:
                ldc = pclases.LineaDeCompra.get(idldc)
                ldc.descuento = descuento
        else:
            s = pclases.ServicioTomado.get(idldc)
            s.qdescuento = descuento
        self.rellenar_widgets()

    def cambiar_precio_ldc(self, cell, path, texto):
        """
        Si es una línea de compra, cambia el precio y vuelve a chuequear los 
        vistos buenos.
        Si es una línea de servicio, simplemente cambia el precio.
        Si contiene el símbolo "=" al principio, interpreta la cantidad como 
        una operación matemática.
        """
        texto = texto.strip()
        if texto.startswith("="):
            texto = eval(texto[1:], {})
        try:
            precio = float(texto)
        except:
            utils.dialogo_info(titulo = "ERROR", 
                    texto = "La cantidad debe ser numérica", 
                    padre = self.wids['ventana'])
            return
        model = self.wids['tv_ldvs'].get_model()
        idldc = model[path][-1]
        if model[path].parent == None:
            if idldc != -1:
                ldc = pclases.LineaDeCompra.get(idldc)
                txt = "El albarán ya ha sido valorado con el precio %s € para"\
                      " esta línea.\n  ¿Está seguro de querer cambiarlo a "\
                      "%s €?" % (utils.float2str(ldc.precio, 4, autodec=True), 
                                 utils.float2str(precio, 4, autodec = True))
                if ((ldc.albaranEntradaID != None 
                        and ldc.precio != 0 
                        and ldc.precio != precio 
                        and utils.dialogo(
                            titulo = "¿CAMIBAR PRECIO?", 
                            texto = txt, 
                            padre = self.wids['ventana'])) 
                    or (ldc.albaranEntradaID == None or ldc.precio == 0)): 
                        # No tiene albarán o no estaba valorado
                    ldc.precio = precio
                    self.objeto.vistoBuenoUsuario = True    # Partimos de que 
                        # si el precio lo ha cambiado el usuario, 
                        # tiene su propio visto bueno. (De verdad que me 
                        # parece absurdísimo el tema del visto bueno del 
                        # usuario). Pero CWT.
                    if not self.objeto.vistoBuenoAutomatico:
                        self.objeto.vistoBuenoUsuario \
                                = self.objeto.vistoBuenoDirector \
                                = self.objeto.vistoBuenoTecnico \
                                = self.objeto.vistoBuenoComercial = False
                        self.objeto.fechaVistoBuenoUsuario \
                                = self.objeto.fechaVistoBuenoDirector \
                                = self.objeto.fechaVistoBuenoTecnico \
                                = self.objeto.fechaVistoBuenoComercial = None
                    else:
                        self.objeto.vistoBuenoUsuario \
                                = self.objeto.vistoBuenoDirector \
                                = self.objeto.vistoBuenoTecnico \
                                = self.objeto.vistoBuenoComercial = True
                        self.objeto.fechaVistoBuenoUsuario \
                                = self.objeto.fechaVistoBuenoDirector \
                                = self.objeto.fechaVistoBuenoTecnico \
                                = self.objeto.fechaVistoBuenoComercial \
                                = mx.DateTime.localtime()
            else:  # Caso servicio que viene de albarán salida.
                s = pclases.ServicioTomado.get(idldc)
                s.qprecio = precio
        else: # Caso servicio metido a mano.
            s = pclases.ServicioTomado.get(idldc)
            s.qprecio = precio
        self.rellenar_widgets()

    def cambiar_descripcion(self, cell, path, texto):
        """
        Cambia la descripción de un servico. Si la línea es una 
        línea de compra impide que se cambie.
        """
        model = self.wids['tv_ldvs'].get_model()
        try:
            idldc = model[path][-1]
        except IndexError, e:
            self.logger.error("facturas_compra.py::cambiar_descripcion -> "
                              "%s.\npath: %s" % (e, path))
        else:
            if model[path].parent != None:
                s = pclases.ServicioTomado.get(idldc)
                s.qconcepto = texto
            self.rellenar_widgets()

    def cambiar_cantidad_ldc(self, cell, path, texto):
        # ¡HAY QUE PROBAR LAS COSAS! Esta ventana ha llegado a MARZO con la 
        # mitad de las cosas por implementar y la otra mitad fallando. Cojones 
        # ya. El mileniarismo va a chegaaar.
        try:
            cantidad = float(texto)
        except:
            utils.dialogo_info(titulo = "ERROR", 
                    texto = "La cantidad debe ser numérica", 
                    padre = self.wids['ventana'])
            return
        model = self.wids['tv_ldvs'].get_model()
        idldc = model[path][-1]
        if model[path].parent == None:
            if idldc != -1:
                ldc = pclases.LineaDeCompra.get(idldc)
                if ldc.albaranEntradaID == None:
                    ldc.cantidad = cantidad
                else:
                    utils.dialogo_info(titulo = "CANTIDAD INCORRECTA", 
                        texto = "La cantidad tecleada (%s) no se corresponde\n"
                                " con la entrada en almacén reflejada en el \n"
                                "albarán. Si la cantidad es incorrecta, \n"
                                "cambie el albarán de entrada. Si lo que \n"
                                "quiere es facturar más cantidad de la \n"
                                "recibida, cree una línea sin albarán del \n"
                                "mismo producto." % (texto), 
                        padre = self.wids['ventana'])
        else:
            s = pclases.ServicioTomado.get(idldc)
            s.qcantidad = cantidad
        self.rellenar_widgets()

    def rellenar_tabla(self, tabla = None):
        """
        Rellena el model del TreeView de líneas de compra.
        """
        subtotal = 0
        factura = self.objeto
        if tabla == None:
            tabla = self.wids['tv_ldvs']
        if factura != None:
            lineas = factura.lineasDeCompra
            model = self.wids['tv_ldvs'].get_model()
            model.clear()
            for l in lineas:
                model.append(None, (l.productoCompra.codigo,
                                    l.productoCompra.descripcion,
                                    utils.float2str(l.cantidad),
                                    utils.float2str(l.precio, 4, autodec=True),
                                    "%s %%" % (utils.float2str(l.iva*100, 0)),
                                    "%s %%" % (utils.float2str(
                                        l.descuento * 100, 0)),
                                    utils.float2str(l.get_subtotal(iva=False), 
                                                    3, autodec = True),
                                    utils.float2str(l.get_subtotal(iva = True),
                                                    3, autodec = True),
                                    l.pedidoCompra 
                                        and l.pedidoCompra.numpedido or "", 
                                    l.albaranEntrada 
                                        and l.albaranEntrada.numalbaran or "", 
                                    l.id))
                subtotal += l.get_subtotal(iva = False)
            if factura.serviciosTomados:
                nodo_servicios = model.append(None, 
                        ("SERVICIOS", "", "", "", "", "", "", "", "", "", -1))
            servicios = factura.serviciosTomados[:]
            servicios.sort(lambda s1, s2: int(s1.id - s2.id))
            for servicio in servicios:
                if servicio.transporteACuentaID != None:
                    trpte = servicio.transporteACuenta
                    trpte.sync()
                    NumAlbaranSalida = trpte.albaranSalida.numalbaran
                    albaran_salida = "Ntro. Alb. %s" % (NumAlbaranSalida)
                    pedido = "-"
                elif servicio.comisionID != None:
                    NumAlbaranSalida=servicio.comision.albaranSalida.numalbaran
                    albaran_salida = "Ntro. Alb. %s" % (NumAlbaranSalida)
                    NumFactura = ((servicio.comision.facturaVenta 
                                and servicio.comision.facturaVenta.numfactura) 
                            or (servicio.comision.prefactura 
                                and servicio.comision.prefactura.numfactura) 
                            or "-")
                    pedido = "Ntra. Fra. %s" % (NumFactura)
                else:
                    albaran_salida = "-"
                    pedido = "-"
                totservicio = servicio.get_subtotal(iva = False)
                model.append(nodo_servicios, ("SERVICIO", 
                    servicio.qconcepto, 
                    utils.float2str(servicio.qcantidad), 
                    utils.float2str(servicio.qprecio, 4, autodec = True), 
                    "%s %%" % (utils.float2str(servicio.iva * 100, 0)), 
                    "%s %%" % (utils.float2str(servicio.qdescuento * 100, 0)), 
                    utils.float2str(totservicio, 3, autodec = True),
                    utils.float2str(servicio.get_subtotal(iva = True), 3, 
                                    autodec = True),
                    pedido, 
                    albaran_salida,  
                    servicio.id))
                subtotal += totservicio 
            self.wids['tv_ldvs'].expand_all()
        return subtotal


    def activar_widgets(self, s, chequear_permisos = True):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        Si chequear_permisos se debe poner a False para 
        evitar recursión infinita.
        """
        if (self.objeto and self.objeto.bloqueada and self.usuario 
                and self.usuario.nivel >= 2) or (not self.objeto):
            s = False
        ws = ('b_add_albaran', 'b_borrar', 'e_numfactura', 'hbox6', 
              'b_drop_albaran', 'cmbe_proveedor',  
              'b_fecha', 'tv_ldvs', 'e_fecha', 'e_fecha_entrada', 'b_add_vto', 
              'b_drop_vto', 'b_vtos_defecto', 
              'b_add_ldc', 'b_drop_ldc', 'b_comisiones_y_transportes', 
              'b_fecha_entrada', 'b_comprobar_visto_bueno', 
              'vbox_adjuntos')  # XXX: Código para adjuntos.
        for w in ws:
            if w == 'b_comisiones_y_transportes' or w == 'b_add_albaran':
                self.wids[w].set_sensitive(s 
                        and self.wids[w].get_property("sensitive"))
            else:
                self.wids[w].set_sensitive(s)
        if (self.objeto and self.objeto.bloqueada and self.usuario 
            and self.usuario.nivel == 3):
            # Si el usuario tiene nivel 3 y permiso sobre la ventana (si ha 
            # podido abrirla es que sí), 
            # le dejo editar los vencimientos y cobros.
            self.wids['expander1'].set_sensitive(True)
        self.habilitar_firmas()
        if chequear_permisos:
            self.check_permisos()

    def habilitar_firmas(self):
        """
        Habilita o deshabilita los widgets para las firmas digitales.
        """
        txtws = []
        if self.usuario:
            prews = ("ch_", "e_fecha_", "b_fecha_")
            txtws.append(("visto_bueno_comercial", 
                self.usuario.firmaComercial or self.usuario.firmaTotal))
            txtws.append(("visto_bueno_director", 
                self.usuario.firmaDirector or self.usuario.firmaTotal))
            txtws.append(("visto_bueno_tecnico", 
                self.usuario.firmaTecnico or self.usuario.firmaTotal))
            for prew in prews:
                for txtw, sens in txtws:
                    self.wids["%s%s" % (prew, txtw)].set_sensitive(sens)
            self.wids['b_comprobar_visto_bueno'].set_sensitive(
                    self.usuario.firmaUsuario or self.usuario.firmaTotal)

    def ir_a_primero(self):
        """
        Hace que el primer registro -si lo hay- de la tabla implicada
        en el objeto del formulario sea el objeto activo.
        """
        factura = self.objeto
        try:
            # Anulo el aviso de actualización del envío que deja de ser activo.
            if factura != None: factura.notificador.desactivar()
            factura = pclases.FacturaCompra.select(orderBy = "-id")[0]    
                # Selecciono todos los facturaes de compra y me quedo con el 
                # primero de la lista.
            factura.notificador.activar(self.aviso_actualizacion) 
        except IndexError:
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
            filas_res.append((r.id, r.numfactura, utils.str_fecha(r.fecha), 
                              r.proveedorID and r.proveedor.nombre  or "", 
                              r.numeroControl, 
                              utils.float2str(r.importeTotal)))
        idfactura = utils.dialogo_resultado(filas_res,
                        titulo = 'SELECCIONE FACTURA',
                        cabeceras = ('ID Interno', 'Número de factura', 
                                     'Fecha', 'Proveedor', 'Código control', 
                                     'Importe'), 
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
        provs = pclases.Proveedor.select(orderBy = 'nombre')
        lista_provs = [(p.id, p.nombre) for p in provs if not p.inhabilitado]
        utils.rellenar_lista(self.wids['cmbe_proveedor'], lista_provs)
        factura = self.objeto
        if factura != None:
            self.wids['ventana'].set_title("Facturas de compra - %s" % (
                factura.numfactura))
        else:
            self.wids['ventana'].set_title("Facturas de compra")
        self.wids['e_numfactura'].set_text(factura.numfactura)
        self.wids['e_fecha'].set_text(utils.str_fecha(factura.fecha))
        self.wids['e_fecha_entrada'].set_text(utils.str_fecha(
            factura.fechaEntrada))
        utils.combo_set_from_db(self.wids['cmbe_proveedor'], 
                factura.proveedorID) 
        iva_homogeneo = factura.iva_es_correcto()
        self.wids['e_iva'].set_text("%s %%" % (
            utils.float2str(factura.iva * 100, 0)))
        self.wids['e_iva'].set_sensitive(iva_homogeneo)
        self.wids['label16'].set_sensitive(iva_homogeneo)
        subtotal = self.rellenar_tabla(self.wids['tv_ldvs'])
        try: 
            totiva = factura.importeIva
        except AssertionError, msg:
            self.logger.error('facturas_compra::rellenar_widgets -> Disparada'
                              ' "assertion" de totales: %s' % msg)
            totiva = subtotal * (1-factura.descuento) * factura.iva     # Pongo el iva que en teoría 
                # debería salir en total y ya veré en el log qué ha pasado.
        self.wids['e_totiva'].set_text("%s €" % (utils.float2str(totiva)))
        try:
            self.wids['e_total'].set_text("%s €" % (
                utils.float2str(self.objeto.importeTotal)))
        except AssertionError, msg:
            print msg
            self.wids['e_total'].set_text("0,0 €")
        self.wids['txt_observaciones'].get_buffer().set_text(
                factura.observaciones)
        # Totales
        self.wids['e_cargo'].set_text(utils.float2str(factura.cargo))
        self.wids['e_descuento'].set_text("%s %%" % (
            utils.float2str(factura.descuento * 100, autodec = True)))
        self.wids['chk_bloqueada'].set_active(factura.bloqueada)
        self.wids['e_subtotal'].set_text("%s €" % (utils.float2str(subtotal)))
        subtotal *= (1 - factura.descuento)
        self.wids['e_totdescuento'].set_text("%s €" % (
            utils.float2str(subtotal)))
        subtotal += utils._float(factura.cargo)
        self.wids['e_totcargo'].set_text("%s €" % (utils.float2str(subtotal)))
        #subtotal = round(subtotal, 2)
        self.rellenar_vistos_buenos()
        self.rellenar_vencimientos()
        self.rellenar_pedidos_y_albaranes()
        self.comprobar_si_comisiones_y_transportes_pendientes()
        self.comprobar_si_albaranes_pendientes()
        self.objeto.make_swap()
        self.rellenar_adjuntos()    # XXX: Código para adjuntos.

    def rellenar_adjuntos(self):    # XXX: Código para adjuntos.
        """
        Introduce los adjuntos del objeto en la tabla de adjuntos.
        """
        model = self.wids['tv_adjuntos'].get_model()
        model.clear()
        if self.objeto != None:
            docs = self.objeto.documentos[:]
            docs.sort(lambda x, y: utils.orden_por_campo_o_id(x, y, "id"))
            for adjunto in self.objeto.documentos:
                model.append((adjunto.nombre,adjunto.observaciones,adjunto.id))

    def comprobar_si_albaranes_pendientes(self):
        """
        Comprueba si al proveedor le quedan albaranes pendientes 
        de facturar y habilita el botón o no en función de eso.
        """
        pendiente = True    # Para que si no hay proveedor le deje buscar 
                            # entre todos los albaranes.
        if self.objeto.proveedorID != None:
            prov = self.objeto.proveedor
            pendiente = len(prov.get_albaranes_pendientes_de_facturar()) != 0
        self.wids['b_add_albaran'].set_sensitive(pendiente)

    def comprobar_si_comisiones_y_transportes_pendientes(self):
        """
        Si el proveedor actual tiene comisiones y transportes pendientes 
        de facturar, habilita el botón.
        """
        pendiente = False
        if self.objeto.proveedorID != None:
            prov = self.objeto.proveedor
            pendiente = (len(prov.get_comisiones_pendientes_de_facturar()) 
                         + len(prov.get_transportes_pendientes_de_facturar()) 
                         != 0)
        self.wids['b_comisiones_y_transportes'].set_sensitive(pendiente)

    def abrir_pedido_o_albaran(self, tv, path, col):
        """
        Abre el pedido de compra o albarán de entrada al 
        que se le ha hecho doble clic.
        """
        model = tv.get_model()
        tipo = model[path][0]
        ide = model[path][-1]
        if "PED" in tipo.upper():
            from formularios import pedidos_de_compra
            pedido = pclases.PedidoCompra.get(ide)
            ventana = pedidos_de_compra.PedidosDeCompra(pedido)  # @UnusedVariable
        if "ALB" in tipo.upper():
            from formularios import albaranes_de_entrada
            albaran = pclases.AlbaranEntrada.get(ide)
            ventana = albaranes_de_entrada.AlbaranesDeEntrada(albaran)  # @UnusedVariable

    def rellenar_pedidos_y_albaranes(self):
        """
        Rellena el TreeView con los pedidos y albaranes que contiene la 
        factura.
        """
        model = self.wids['tv_peds_y_albs'].get_model()
        model.clear()
        peds = []
        albs = []
        claves = self.objeto.lineasDeCompra[:]
        claves.sort(utils.cmp_fecha_id)
        for ldc in claves:
            if ldc.pedidoCompraID != None and ldc.pedidoCompraID not in peds:
                model.append(("Pedido ", 
                              ldc.pedidoCompra.numpedido, 
                              utils.str_fecha(ldc.pedidoCompra.fecha), 
                              ldc.pedidoCompra.id))
                peds.append(ldc.pedidoCompraID)
            if (ldc.albaranEntradaID != None 
                    and ldc.albaranEntradaID not in albs):
                model.append(("Albarán ", 
                              ldc.albaranEntrada.numalbaran, 
                              utils.str_fecha(ldc.albaranEntrada.fecha), 
                              ldc.albaranEntrada.id))
                albs.append(ldc.albaranEntradaID)

    
    def rellenar_vistos_buenos(self):
        """
        Introduce la información de los vistos buenos en la ventana.
        """
        factura = self.objeto
        vto_bueno_auto = factura.vistoBuenoAutomatico
        self.wids['ch_visto_bueno_automatico'].set_active(vto_bueno_auto)
        if vto_bueno_auto:
            factura.vistoBuenoComercial \
                    = factura.vistoBuenoTecnico \
                    = factura.vistoBuenoDirector = vto_bueno_auto
            if not factura.fechaVistoBuenoComercial:
                factura.fechaVistoBuenoComercial = mx.DateTime.localtime()
            if not factura.fechaVistoBuenoTecnico:
                factura.fechaVistoBuenoTecnico = mx.DateTime.localtime()
            if not factura.fechaVistoBuenoDirector:
                factura.fechaVistoBuenoDirector = mx.DateTime.localtime()
            self.wids['e_motivo_vto_bueno'].modify_base(gtk.STATE_NORMAL, 
                    self.wids['e_numerocontrol'].get_colormap().alloc_color(
                        "YellowGreen"))
        else:
            self.wids['e_motivo_vto_bueno'].modify_base(gtk.STATE_NORMAL, 
                    self.wids['e_numerocontrol'].get_colormap().alloc_color(
                        "OrangeRed"))
        cod_vtob = factura.get_codigo_validacion_visto_bueno()
        self.wids['e_motivo_vto_bueno'].set_text(
                pclases.FacturaCompra.codigos_no_validacion[cod_vtob])
        if (factura.vistoBuenoComercial and factura.vistoBuenoTecnico 
                and factura.vistoBuenoDirector):
            self.wids['e_numerocontrol'].set_text(factura.numeroControl)
            self.wids['e_numerocontrol'].modify_base(gtk.STATE_NORMAL, 
                    self.wids['e_numerocontrol'].get_colormap().alloc_color(
                        "LightBlue"))
        else:
            self.wids['e_numerocontrol'].set_text("PENDIENTE")
            self.wids['e_numerocontrol'].modify_base(gtk.STATE_NORMAL, 
                    self.wids['e_numerocontrol'].get_colormap().alloc_color(
                        "IndianRed"))
        self.wids['ch_visto_bueno_comercial'].set_active(
                factura.vistoBuenoComercial)
        self.wids['ch_visto_bueno_tecnico'].set_active(
                factura.vistoBuenoTecnico)
        self.wids['ch_visto_bueno_director'].set_active(
                factura.vistoBuenoDirector)
        self.wids['ch_visto_bueno_comercial'].set_sensitive(not vto_bueno_auto)
        self.wids['ch_visto_bueno_tecnico'].set_sensitive(not vto_bueno_auto)
        self.wids['ch_visto_bueno_director'].set_sensitive(not vto_bueno_auto)
        self.wids['e_fecha_visto_bueno_comercial'].set_sensitive(
                not vto_bueno_auto)
        self.wids['e_fecha_visto_bueno_tecnico'].set_sensitive(
                not vto_bueno_auto)
        self.wids['e_fecha_visto_bueno_director'].set_sensitive(
                not vto_bueno_auto)
        self.wids['b_fecha_visto_bueno_comercial'].set_sensitive(
                not vto_bueno_auto)
        self.wids['b_fecha_visto_bueno_tecnico'].set_sensitive(
                not vto_bueno_auto)
        self.wids['b_fecha_visto_bueno_director'].set_sensitive(
                not vto_bueno_auto)
        self.wids['e_fecha_visto_bueno_comercial'].set_text(
                utils.str_fecha(factura.fechaVistoBuenoComercial))
        self.wids['e_fecha_visto_bueno_tecnico'].set_text(
                utils.str_fecha(factura.fechaVistoBuenoTecnico))
        self.wids['e_fecha_visto_bueno_director'].set_text(
                utils.str_fecha(factura.fechaVistoBuenoDirector))

    def add_albaran(self, widget):
        """
        Añade un albarán de entrada a la factura de compra.
        """
        # CWT: Agárrate los machos. Al loro: después de meter el 
        # albarán mmpppffff... espérate que me da la risa... después 
        # de meter el albarán... ¡tiene que preguntarle al usuario el 
        # importe total de la factura para ver si coincide con el que 
        # calcula el ordenador! ¿Alguien dijo Minglanillas?
        factura = self.objeto
        if factura != None:
            albaranes = self.pedir_albaran()
            if albaranes:
                lineas = []
                for albaran in albaranes:
                    lineas += list(pclases.LineaDeCompra.select(
                        pclases.LineaDeCompra.q.albaranEntradaID==albaran.id))
                filas = [(ldc.id, 
                          ldc.albaranEntrada.numalbaran, 
                          utils.float2str(ldc.cantidad), 
                          ldc.productoCompra.descripcion, 
                          "%s €" % utils.float2str(ldc.precio,4,autodec=True), 
                          "%s %%" % utils.float2str(ldc.iva), 
                          "%s %%" % utils.float2str(ldc.descuento),
                          "%s €" % utils.float2str(ldc.get_subtotal(iva=True)))
                          for ldc in lineas if ldc.facturaCompra == None]
                lineas = utils.dialogo_resultado(
                            filas = filas, 
                            titulo = "SELECCIONE LÍNEAS A FACTURAR", 
                            padre = self.wids['ventana'], 
                            cabeceras = ["ID", 
                                         "Albarán", 
                                         "Cantidad", 
                                         "Descripción", 
                                         "Precio", 
                                         "IVA", 
                                         "Descuento", 
                                         "Subtotal"], 
                            multi = True, 
                            defecto = range(len(filas)))
                if lineas[0] > 0:
                    self.objeto.anular_vistos_buenos()
                for idl in lineas:
                    l = pclases.LineaDeCompra.get(idl)
                    if l.facturaCompra == None:
                        l.facturaCompra = factura
                if self.objeto.proveedorID == None:
                    self.objeto.proveedor = albaran.proveedor
                self.actualizar_ventana()
                # ¿Ves? Al final lo hemos tenido que quitar. 
                # Ains, Minglanillas...
                #if self.importe_total_factura_coincide_con_usuario():
                #    factura.vistoBuenoUsuario = True
                #    factura.fechaVistoBuenoUsuario = mx.DateTime.localtime()
                #else:
                #    factura.vistoBuenoUsuario = False
                #    factura.fechaVistoBuenoUsuario = None
                #self.actualizar_ventana()

    def comprobar_visto_bueno(self, boton):
        """
        Pregunta al usuario el total de factura para ver si coincide con 
        el calculado y comprueba el visto bueno automático.
        """
        factura = self.objeto
        if factura:
            if self.importe_total_factura_coincide_con_usuario():
                factura.vistoBuenoUsuario = True
                factura.fechaVistoBuenoUsuario = mx.DateTime.localtime()
            else:
                factura.vistoBuenoUsuario = False
                factura.fechaVistoBuenoUsuario = None
            self.actualizar_ventana()

    def importe_total_factura_coincide_con_usuario(self):
        """
        Devuelve True si la cantidad tecleada por el usuario coincide 
        con el total de la factura.
        """
        cantidad = utils.dialogo_entrada(
                titulo = "INTRODUZCA TOTAL DE LA FACTURA", 
                texto = "Introduzca el importe total de la factura para "
                        "comprobar que coincide con el importe calculado:", 
                padre = self.wids['ventana'])
        try:
            cantidad = float(cantidad)
        except:
            utils.dialogo_info(titulo = "ERROR FORMATO", 
                texto = "El texto introducido (%s) no es un número"%(cantidad),
                padre = self.wids['ventana'])
            return self.importe_total_factura_coincide_con_usuario()
        try:
            e_total = utils.parse_euro(self.wids['e_total'].get_text())
        except ValueError:
            e_total = 0
        return cantidad == e_total

    def drop_albaran(self, widget):
        """
        Elimina de la factura de compra, el albarán al que
        pertenece la linea de compra seleccionada
        """
        factura = self.objeto  # @UnusedVariable
        model, itr = self.wids['tv_ldvs'].get_selection().get_selected()
        if itr != None:
            idldc = model[itr][-1]
            if model[itr].parent == None and model[itr][-1] != -1:
                lineadecompra = pclases.LineaDeCompra.get(idldc)
                albaran = lineadecompra.albaranEntrada
                for l in albaran.lineasDeCompra:
                    l.facturaCompra = None
                self.objeto.anular_vistos_buenos()
                self.actualizar_ventana()
            else:
                utils.dialogo_info(titulo = "ERROR", 
                    texto = "Ha seleccionado un servicio.\n Seleccione una"
                            " línea de albarán para eliminar el albarán de "
                            "la factura actual.", 
                    padre = self.wids['ventana'])
        else:
            utils.dialogo_info('ERROR', 
                    'Seleccione una línea de compra de la factura.\nSe '
                    'eliminarán todas las líneas pertenecientes al albarán '
                    'de dicha línea.', 
                    padre = self.wids['ventana'])

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
        if self.objeto != None:
            self.verificar_si_vencimientos()
        provs = pclases.Proveedor.select(orderBy = 'nombre')
        lista_provs = [(p.id, p.nombre) for p in provs if not p.inhabilitado]
        idproveedor = utils.dialogo_combo(titulo = "SELECCIONAR PROVEEDOR", 
                            texto = "Seleccione el proveedor de la factura:", 
                            ops = lista_provs, 
                            padre = self.wids['ventana'])
        if idproveedor == None: 
            return
        numfactura = utils.dialogo_entrada(
            'Introduzca un número para la factura.', 
            'NÚMERO DE FACTURA', 
            padre = self.wids['ventana'])
        if numfactura == None: 
            return
        proveedor = pclases.Proveedor.get(idproveedor)
        facturas_existentes = pclases.FacturaCompra.select(pclases.AND(
            pclases.FacturaCompra.q.numfactura.contains(numfactura), 
            pclases.FacturaCompra.q.proveedorID == idproveedor, 
            pclases.FacturaCompra.q.fecha >= mx.DateTime.DateFrom(
                mx.DateTime.today().year, 1, 1), 
            pclases.FacturaCompra.q.fecha <= mx.DateTime.DateFrom(
                mx.DateTime.today().year, 12, 31))
        )
        facturas_existentes = [f for f in facturas_existentes 
                               if f.numfactura.upper() == numfactura.upper()]
        if facturas_existentes != []:
            if proveedor == None:
                nombreproveedor = ""
            else:
                nombreproveedor = "del proveedor %s" % (proveedor.nombre)
            utils.dialogo_info(titulo = "ERROR CREANDO FACTURA", 
                texto = "La factura %s %s ya existe.\n"
                        "No puede crear una factura duplicada." % (
                            numfactura, nombreproveedor), 
                padre = self.wids['ventana'])
        else:
            if factura != None: 
                factura.notificador.set_func(lambda : None)
            if proveedor != None:
                iva = proveedor.iva
                if iva == None:
                    iva = 0.0
            else:
                iva = 0.21
            factura = pclases.FacturaCompra(fecha = mx.DateTime.localtime(),
                                        numfactura = numfactura,
                                        proveedor = proveedor, 
                                        vistoBuenoComercial = False, 
                                        fechaVistoBuenoComercial = None, 
                                        vistoBuenoTecnico = False, 
                                        fechaVistoBuenoTecnico = None, 
                                        vistoBuenoDirector = False, 
                                        fechaVistoBuenoDirector = None, 
                                        fechaEntrada = mx.DateTime.localtime(),
                                        iva = iva, 
                                        vistoBuenoUsuario = None,
                                        fechaVistoBuenoUsuario = None, 
                                        bloqueada = False, 
                                        vencimientosConfirmados = False)
            pclases.Auditoria.nuevo(factura, self.usuario, __file__)
            factura.notificador.set_func(self.aviso_actualizacion)
            self.objeto = self._objetoreciencreado = factura
            # XXX: Añado a objetos recientes.
            objsr = pclases.ListaObjetosRecientes.buscar("facturas_compra.py",
                                                    self.usuario, 
                                                    crear = True)
            objsr.push(self.objeto.id)
            # XXX: End Of Añado a objetos recientes.
            self.actualizar_ventana()
            utils.dialogo_info('FACTURA CREADA', 
                'La factura %s ha sido creada.\n\nIntroduzca a continuación '
                'el resto de información.\nNo olvide crear los vencimientos '
                'al finalizar.' % (factura.numfactura), 
                padre = self.wids['ventana'])

    def buscar_factura(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        if self.objeto != None:
            self.verificar_si_vencimientos()
        factura = self.objeto
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR FACTURA", 
                    texto = "Introduzca número de factura o proveedor:",
                    padre = self.wids['ventana']) 
        if a_buscar != None:
            proveedor = utils.buscar_proveedor(a_buscar)
            if proveedor:
                try:
                    if len(proveedor) > 1:
                        resultados = []
                        for p in proveedor:
                            resultados += p.facturasCompra
                        resultados = pclases.SQLtuple(resultados)
                    else:
                        raise ValueError, "Solo se encontró un proveedor."
                except (TypeError, ValueError):
                    resultados = pclases.SQLtuple(proveedor.facturasCompra)
            else:
                resultados = pclases.FacturaCompra.select(
                    pclases.FacturaCompra.q.numfactura.contains(a_buscar))
            if resultados.count() > 1:
                ## Refinar los resultados
                idfactura = self.refinar_resultados_busqueda(resultados)
                if idfactura == None:
                    return
                resultados = [pclases.FacturaCompra.get(idfactura)]
            elif resultados.count() < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info('SIN RESULTADOS', 
                    'La búsqueda no produjo resultados.\nPruebe a cambiar '
                    'el texto buscado o déjelo en blanco para ver una lista '
                    'completa.\n(Atención: Ver la lista completa puede '
                    'resultar lento si el número de elementos es muy alto)', 
                    padre = self.wids['ventana'])
                return
            ## Un único resultado
            # Primero anulo la función de actualización
            if factura != None:
                factura.notificador.set_func(lambda : None)
            # Pongo el objeto como actual
            factura = resultados[0]
            # XXX: Añado a objetos recientes.
            objsr = pclases.ListaObjetosRecientes.buscar("facturas_compra.py", 
                                                    self.usuario, 
                                                    crear = True)
            objsr.push(factura.id)
            # XXX: End Of Añado a objetos recientes.
            # Y activo la función de notificación:
            factura.notificador.set_func(self.aviso_actualizacion)
        self.objeto = factura
        self.actualizar_ventana()

    def comprobar_numfactura_y_proveedor(self, numfactura = None, 
                                         idproveedor = None, 
                                         fecha = None):
        """
        Comprueba que el número de factura no exista para el proveedor y año 
        ya en la BD. Si no se recibe numfactura, fecha o idproveedor, toma 
        los de la ventana.
        """
        if numfactura == None:
            numfactura = self.wids['e_numfactura'].get_text()
        if idproveedor == None:
            proveedor = utils.combo_get_value(self.wids['cmbe_proveedor'])
            if proveedor == None:
                idproveedor = None
            else:
                proveedor = pclases.Proveedor.get(proveedor)
                idproveedor = proveedor.id
        if not fecha:
            try:
                fecha = utils.parse_fecha(self.wids['e_fecha'].get_text())
            except (TypeError, ValueError):
                fecha = mx.DateTime.today()
        anno = fecha.year
        facturas_existentes = pclases.FacturaCompra.select(pclases.AND(
            pclases.FacturaCompra.q.numfactura.contains(numfactura), 
            pclases.FacturaCompra.q.proveedorID == idproveedor, 
            pclases.FacturaCompra.q.fecha >= mx.DateTime.DateFrom(anno, 1, 1), 
            pclases.FacturaCompra.q.fecha <= mx.DateTime.DateFrom(anno, 12, 31)
        ))
        # Quito la factura actual para no contarme a mí misma como duplicada 
        # de mí misma:
        facturas_existentes = [f for f in facturas_existentes 
                if f != self.objeto 
                   and f.numfactura.upper() == numfactura.upper()]
        if facturas_existentes != []:
            if proveedor == None:
                nombreproveedor = ""
            else:
                nombreproveedor = "del proveedor %s" % (proveedor.nombre)
            utils.dialogo_info(titulo = "ERROR: FACTURA DUPLICADA", 
                texto = "La factura %s %s ya existe." % (numfactura, 
                                                          nombreproveedor), 
                padre = self.wids['ventana'])
            return False
        else:
            return True

    def mismo_proveedor_en_factura_y_albaranes(self):
        """
        Devuelve True si el proveedor de la factura es el mismo que el de 
        los albaranes. 
        Si no tiene albaranes, también devuelve True.
        """
        res = True
        if self.objeto != None:
            for ldc in self.objeto.lineasDeCompra:
                if ldc.albaranEntrada != None:
                    if ldc.albaranEntrada.proveedor != self.objeto.proveedor:
                        res = False
                        break
        return res

    def guardar(self, widget):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        factura = self.objeto
            # Campos del objeto que hay que guardar:
        numfactura = self.wids['e_numfactura'].get_text()
        idproveedor = utils.combo_get_value(self.wids['cmbe_proveedor'])
        fecha = self.wids['e_fecha'].get_text()
        if idproveedor != None:
            proveedor = pclases.Proveedor.get(idproveedor)
        else:
            proveedor = None
        if not self.comprobar_numfactura_y_proveedor():
            numfactura = factura.numfactura
            proveedor = factura.proveedor
            fecha = factura.fecha
        try:
            iva = utils.parse_porcentaje(self.wids['e_iva'].get_text()) / 100.0
        except:
            utils.dialogo_info(titulo = "ERROR FORMATO NUMÉRICO", 
                    texto = 'El iva debe ser un número', 
                    padre = self.wids['ventana'])
            self.wids['e_iva'].set_text("%s %%" % (
                utils.float2str(factura.iva * 100, 0)))
            iva = factura.iva
        try:
            cargo = float(self.wids['e_cargo'].get_text())
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", 
                    texto = 'El cargo debe ser un número', 
                    padre = self.wids['ventana'])
            self.wids['e_cargo'].set_text(str(factura.cargo))
            cargo = factura.cargo
        texto_descuento = self.wids['e_descuento'].get_text()
        if "%" in texto_descuento:
            try:
                descuento = utils.parse_porcentaje(texto_descuento, 
                                                   fraccion = True)
            except:
                utils.dialogo_info(titulo = "ERROR FORMATO NUMÉRICO", 
                                   texto = 'El descuento debe ser un número', 
                                   padre = self.wids['ventana'])
                self.wids['e_descuento'].set_text("%s %%" % (
                    utils.float2str(factura.descuento * 100, autodec = True)))
                descuento = factura.descuento
        else:
            try:
                dineuros = utils.parse_euro(texto_descuento)
                total_fra = factura.calcular_importe_total()
                total_fra_sin_iva = total_fra - factura.calcular_importe_iva()
                porcentaje = dineuros / total_fra_sin_iva
                descuento = porcentaje
            except:
                utils.dialogo_info(titulo = "ERROR FORMATO NUMÉRICO", 
                    texto = '«%s» no es un número' % texto_descuento, 
                    padre = self.wids['ventana'])
                self.wids['e_descuento'].set_text("%s %%" % (
                    utils.float2str(factura.descuento * 100, autodec = True)))
                descuento = factura.descuento
        # Desactivo el notificador momentáneamente
        factura.notificador.set_func(lambda: None)
        # Actualizo los datos del objeto
        bounds = self.wids['txt_observaciones'].get_buffer().get_bounds()
        buf = self.wids['txt_observaciones'].get_buffer()
        factura.observaciones = buf.get_text(bounds[0], bounds[1])
        factura.numfactura = numfactura
        factura.proveedor = proveedor 
        if (proveedor != None 
                and not self.mismo_proveedor_en_factura_y_albaranes()):
            utils.dialogo_info(titulo = "PROVEEDOR DIFERENTE", 
                texto = "El proveedor de la factura difiere del de los "
                        "albaranes.", 
                padre = self.wids['ventana'])
        if (factura.iva != iva # El IVA ha cambiado, actualizo todas las líneas
            and factura.iva_homogeneo):
            for linea in factura.lineasDeCompra + factura.serviciosTomados:
                linea.iva = iva
        factura.iva = iva
        factura.cargo = cargo
        factura.descuento = descuento
        try:
            factura.fecha = utils.parse_fecha(fecha)
        except Exception:
            factura.fecha = mx.DateTime.localtime()
        try:
            factura.fechaEntrada = utils.parse_fecha(
                    self.wids['e_fecha_entrada'].get_text())
        except:
            factura.fechaEntrada = mx.DateTime.localtime()

        # Si los vistos buenos no han cambiado, significa (ya que el botón 
        # guardar se ha habilitado) que lo que ha cambiado es algún campo de 
        # los demás, por lo tanto reseteo vistos buenos:
        if (factura.vistoBuenoDirector 
                == self.wids['ch_visto_bueno_director'].get_active() and 
           factura.vistoBuenoTecnico 
                == self.wids['ch_visto_bueno_tecnico'].get_active() and 
           factura.vistoBuenoComercial 
                == self.wids['ch_visto_bueno_comercial'].get_active() and 
           (factura.vistoBuenoDirector 
               or factura.vistoBuenoTecnico 
               or factura.vistoBuenoComercial)):
            # Pero antes aviso
            utils.dialogo_info(titulo = "CAMBIOS EN FACTURA YA FIRMADA", 
                texto = "Se van a guardar cambios en una factura ya "
                        "autorizada.\nLos vistos buenos se reiniciarán "
                        "debido a estos cambios.\nSerá necesario que se "
                        "vuelva a firmar la factura antes de proceder "
                        "al pago.", 
                padre = self.wids['ventana'])
            # TODO: Quedaría un fleco: Las fechas de los vistos buenos. Si se 
            #       enciende guardar por cambiar una de esas 
            #       fechas también anula los vistos buenos.
            self.objeto.anular_vistos_buenos()
        else:   # Y si no, los guardo.
            factura.bloqueada = self.wids['chk_bloqueada'].get_active()
            factura.vistoBuenoDirector = self.wids[
                    'ch_visto_bueno_director'].get_active()
            factura.vistoBuenoTecnico = self.wids[
                    'ch_visto_bueno_tecnico'].get_active()
            factura.vistoBuenoComercial = self.wids[
                    'ch_visto_bueno_comercial'].get_active()
        if factura.vistoBuenoDirector:
            try:
                factura.fechaVistoBuenoDirector = utils.parse_fecha(
                        self.wids['e_fecha_visto_bueno_director'].get_text())
            except:
                factura.fechaVistoBuenoDirector = mx.DateTime.localtime()
        else:
            factura.fechaVistoBuenoDirector = None
        if factura.vistoBuenoTecnico:
            try:
                factura.fechaVistoBuenoTecnico = utils.parse_fecha(
                        self.wids['e_fecha_visto_bueno_tecnico'].get_text())
            except:
                factura.fechaVistoBuenoTecnico = mx.DateTime.localtime()
        else:
            factura.fechaVistoBuenoTecnico = None
        if factura.vistoBuenoComercial:
            try:
                factura.fechaVistoBuenoComercial = utils.parse_fecha(
                        self.wids['e_fecha_visto_bueno_comercial'].get_text())
            except:
                factura.fechaVistoBuenoComercial = mx.DateTime.localtime()
        else:
            factura.fechaVistoBuenoComercial = None
        # Fuerzo la actualización de la BD y no espero a que SQLObject lo 
        # haga por mí:
        factura.syncUpdate()
        # Vuelvo a activar el notificador
        factura.notificador.set_func(self.aviso_actualizacion)
        self.actualizar_ventana()
        self.wids['b_guardar'].set_sensitive(False)

    def cambiar_fecha_entrada(self, boton):
        self.wids['e_fecha_entrada'].set_text(utils.str_fecha(
            utils.mostrar_calendario(self.objeto 
                                     and self.objeto.fechaEntrada or None, 
                                     padre = self.wids['ventana'])))
        
    def buscar_fecha(self, boton):
        self.wids['e_fecha'].set_text(utils.str_fecha(
            utils.mostrar_calendario(self.objeto 
                                     and self.objeto.fecha or None, 
                                     padre = self.wids['ventana'])))
        
    def borrar_factura(self, boton):
        """
        Elimina la factura de la BD
        """
        if not utils.dialogo('Se eliminará la factura actual y todas sus '
                             'relaciones con ventas, pedidos, etc.\n'
                             '¿Está seguro?', 
                             'BORRAR FACTURA', 
                             padre = self.wids['ventana']): 
            return
        factura = self.objeto
        factura.notificador.set_func(lambda : None)
        try:
            factura.destroy(ventana = __file__)
        except:
            # Si tiene relaciones desvinculo las LDC primero para que no se 
            # eliminen, ya que  deben seguir apareciendo en los albaranes 
            # de entrada.
            for l in factura.lineasDeCompra:
                l.facturaCompra = None
                if l.albaranEntradaID == None:
                    l.destroy(ventana = __file__)
            for s in factura.serviciosTomados:
                try:
                    s.destroy(ventana = __file__)
                except:
                    txt = "facturas_compra.py::borrar_factura -> No se "\
                          "pudo eliminar el servicioTomado ID %d" % (s.id)
                    self.logger.error(txt)
                    print txt
            factura.destroy_en_cascada(ventana = __file__)
        else:
            self.ir_a_primero()
        self.actualizar_ventana()



    def add_vto(self, boton):
        """
        Pide a través de diálogos información sobre un nuevo vencimiento
        y lo inserta en la factura actual.
        """
        factura = self.objeto
        estimado = False
        fecha = utils.mostrar_calendario(padre = self.wids['ventana'])
        cantidad = self.objeto.calcular_importe_total() - sum(
                [vto.importe for vto in self.objeto.vencimientosPago])
        cantidad = round(cantidad, 2)
        if not estimado:
            vto = pclases.VencimientoPago(facturaCompra = factura,
                    fecha = mx.DateTime.DateTimeFrom(day = fecha[0], 
                                                     month = fecha[1], 
                                                     year = fecha[2]),
                    importe = cantidad,
                    observaciones = factura.proveedor 
                        and factura.proveedor.textoformapago or "", 
                    fechaPagado = None, 
                    procesado = False)
        else:
            vto = pclases.EstimacionPago(facturaCompra = factura,
                    fecha = mx.DateTime.DateTimeFrom(day = fecha[0], 
                                                     month = fecha[1], 
                                                     year = fecha[2]),
                    importe = cantidad,
                    observaciones = '')
            pclases.Auditoria.nuevo(vto, self.usuario, __file__)
        self.objeto.vencimientosConfirmados = False
        self.objeto.make_swap() # Para evitar falso positivo de actualización
        self.rellenar_vencimientos()
        
    def drop_vto(self, boton):
        """
        Me cargo los vencimientos (estimado y no) que estén
        en la línea seleccionada. El pago no lo toco.
        """
        model,itr=self.wids['tv_vencimientos'].get_selection().get_selected()
        if itr == None: return
        ids = model[itr][-1]
        ids = [int(i) for i in ids.split(',')]
        idvto = ids[0]
        idest = ids[1]
        if idvto > 0:   # Si realmente hay un vto. (ver rellenar_vencimientos).
            vto = pclases.VencimientoPago.get(idvto)
            vto.destroy(ventana = __file__)
        if idest > 0:
            est = pclases.EstimacionPago.get(idest)
            est.destroy(ventana = __file__)
        self.objeto.vencimientosConfirmados = False
        self.objeto.make_swap() # Para evitar falso positivo de actualización
        self.rellenar_vencimientos()

    def cambiar_vto(self, cell, path, texto):
        """
        Cambia la fecha del vencimiento por la 
        nueva introducida por teclado.
        """
        try:
            fecha = utils.parse_fecha(texto)
        except ValueError:
            utils.dialogo_info('ERROR EN FORMATO DE FECHA', 
                               'Introduzca las fechas separadas por / y en '
                               'la forma dia/mes/año.', 
                               padre = self.wids['ventana'])
            return
        model = self.wids['tv_vencimientos'].get_model()
        idvto = int(model[path][-1].split(',')[0])   # WTF?
            # Al escribirlo no parecía tan lioso. Lo juro.
        if idvto > 0:   # Es -1 si no había.
            vto = pclases.VencimientoPago.get(idvto)
            vto.fecha = fecha
        elif idvto == -1:   
            # Para el resto de valores rebota-rebota y en tu culo explota.
            factura = self.objeto
            vto = pclases.VencimientoPago(
                    fecha = fecha,
                    facturaCompra = factura,
                    importe = 0, 
                    observaciones = factura.proveedor 
                                    and factura.proveedor.textoformapago or "",
                    fechaPagado = None, 
                    procesado = False)
            pclases.Auditoria.nuevo(vto, self.usuario, __file__)
        self.objeto.vencimientosConfirmados = False
        self.objeto.make_swap() # Para evitar falso positivo de actualización
        # Para no sobrecargar mucho la red volviendo a rellenar LDVs y tal.
        self.rellenar_vencimientos()        

    def cambiar_estimado(self, cell, path, texto):
        """
        Cambia la fecha del vencimiento estimado
        por la nueva introducida por teclado.
        """
        try:
            fecha = time.strptime(texto, '%d/%m/%Y')
            anno, mes, dia = fecha[:3]
            fecha = mx.DateTime.DateFrom(day = dia, month = mes, year = anno)
        except ValueError:
            utils.dialogo_info('ERROR EN FORMATO DE FECHA', 
                    'Introduzca las fechas separadas por / y en la forma '
                    'dia/mes/año.', 
                    padre = self.wids['ventana'])
            return
        model = self.wids['tv_vencimientos'].get_model()
        idvto = int(model[path][-1].split(',')[1])
            # Al escribirlo no parecía tan lioso. Lo juro.
        if idvto > 0:   # Es -1 si no había.
            vto = pclases.EstimacionPago.get(idvto)
            vto.fecha = fecha
        elif idvto == -1:   # Para el resto de valores rebota-rebota y 
                            # en tu culo explota.
            factura = self.objeto
            vto = pclases.EstimacionPago(fecha = fecha,
                                          facturaCompra = factura,
                                          importe = 0)
            pclases.Auditoria.nuevo(vto, self.usuario, __file__)
        self.rellenar_vencimientos()

    def borrar_vencimientos_y_estimaciones(self, factura):
        for vto in factura.vencimientosPago:
            vto.factura = None
            vto.destroy(ventana = __file__)
        for est in factura.estimacionesPago:
            est.factura = None
            est.destroy(ventana = __file__)


    def crear_vencimientos_por_defecto(self, w):
        """
        Crea e inserta los vencimientos por defecto
        definidos por el proveedor en la factura
        actual y en función de las LDV que tenga
        en ese momento (concretamente del valor
        del total de la ventana calculado a partir
        de las LDV.)
        Devuelve True si los creó o False si no pudo.
        """
        res = True
        factura = self.objeto
        proveedor = factura.proveedor
        # DONE: NOTA: Cuando cambie el total al añadir,
        #       quitar o cambiar LDVs, hay que
        #       cambiar el valor de los vencimientos.
        if proveedor == None:
            utils.dialogo_info(texto = 'No hay proveedor seleccionado', 
            titulo = 'ERROR', 
            padre = self.wids['ventana'])
            res = False
        else:
            if proveedor.vencimiento != None and proveedor.vencimiento != '':
                try:
                    vtos = proveedor.get_vencimientos()
                    if not vtos:
                        raise
                except:
                    utils.dialogo_info('ERROR VENCIMIENTOS POR DEFECTO', 
                        'Los vencimientos por defecto del proveedor no se pud'
                        'ieron procesar correctamente.\nVerifique que están b'
                        'ien escritos y el formato es correcto en la ventana '
                        'de proveedores.', padre = self.wids['ventana'])
                    res = False  # Los vencimientos no son válidos o no tiene.
                else:
                    self.borrar_vencimientos_y_estimaciones(factura)
                    total = utils.parse_euro(self.wids['e_total'].get_text())
                    numvtos = len(vtos)
                    cantidad = total/numvtos
                    if not factura.fecha:
                        factura.fecha = mx.DateTime.localtime()
                    if (proveedor.diadepago != None 
                        and proveedor.diadepago != ''
                        and proveedor.diadepago != "-"):
                        try:
                            diaest = int(proveedor.diadepago) 
                        except:
                            diaest = None
                            utils.dialogo_info(titulo = "ERROR DÍA ESTIMADO", 
                                texto = "El proveedor tiene como día de pago"
                                        " un valor incorrecto: %s\nDebe usar"
                                        " únicamente números.\nCorrija este "
                                        "dato desde la ventana de clientes."%(
                                            proveedor.diadepago), 
                                padre = self.wids['ventana'])
                    else:
                        diaest = False
                    for incr in vtos:
                        fechavto = mx.DateTime.DateFrom(factura.fecha) + incr
                        vto = pclases.VencimientoPago(
                                fecha = mx.DateTime.DateFrom(factura.fecha) + incr,
                                importe = cantidad,
                                facturaCompra = factura, 
                                observaciones = factura.proveedor 
                                    and factura.proveedor.textoformapago or "",
                                fechaPagado = None,
                                procesado = False) 
                        pclases.Auditoria.nuevo(vto, self.usuario, __file__)
                        if diaest:
                            while True:
                                try:
                                    fechaest = mx.DateTime.DateTimeFrom(
                                        day = diaest, 
                                        month = fechavto.month, 
                                        year = fechavto.year)
                                    break
                                except:
                                    diaest -= 1
                                    if diaest <= 0:
                                        diaest = 31
                            if fechaest < fechavto:     
                                # El día estimado cae ANTES del día del 
                                # vencimiento. 
                                # No es lógico, la estimación debe ser 
                                # posterior. Cae en el mes siguiente, pues.
                                mes = fechaest.month + 1
                                anno = fechaest.year
                                if mes > 12:
                                    mes = 1
                                    anno += 1
                                fechaest = mx.DateTime.DateTimeFrom(
                                    day = diaest, month = mes, year = anno)
                            vto.fecha = fechaest 
                        # Si la fecha de vencimiento cae en sábado o domingo, 
                        # lo paso al lunes siguiente.
                        while mx.DateTime.DateFrom(vto.fecha).day_of_week >= 5:   
                            # 0 = lunes... 5 = sábado, 6 = domingo
                            vto.fecha = mx.DateTime.DateFrom(vto.fecha) + mx.DateTime.oneDay
                        vto.fecha = utils.asegurar_fecha_positiva(vto.fecha)
                    # Si los he creado automáticamente, son válidos.
                    self.objeto.vencimientosConfirmados = True
                    self.objeto.make_swap() 
                    self.rellenar_vencimientos()
            else:
                utils.dialogo_info(titulo = "SIN DATOS", 
                    texto = "El proveedor no tiene los datos necesarios para"
                            " crear vencimientos por defecto.", 
                    padre = self.wids['ventana'])
                res = False
        return res

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
                utils.dialogo_info('ERROR EN FORMATO', 
                    'Introduzca el importe usando el punto (.) como separador'
                    ' decimal y sin símbolos de separación de millares ni mon'
                    'etarios.', 
                    padre = self.wids['ventana'])
                return
        try:
            cantidad = float(texto)
        except ValueError:
            utils.dialogo_info('ERROR EN FORMATO', 
                    'Introduzca el importe usando el punto (.) como separador'
                    ' decimal y sin símbolos de separación de millares ni '
                    'monetarios.', 
                    padre = self.wids['ventana'])
            return
        model = self.wids['tv_vencimientos'].get_model()
        idvto = int(model[path][-1].split(',')[0])
            # Al escribirlo no parecía tan lioso. Lo juro.
        if idvto > 0:   # Es -1 si no había.
            vto = pclases.VencimientoPago.get(idvto)
            vto.importe = cantidad
        elif idvto == -1:   # Para el resto de valores rebota-rebota y en tu 
                            # culo explota.
            factura = self.objeto
            vto = pclases.VencimientoPago(fecha = mx.DateTime.localtime(),
                                          facturaCompra = factura,
                                          importe = cantidad, 
                                          fechaPagado = None)
            pclases.Auditoria.nuevo(vto, self.usuario, __file__)
        self.objeto.vencimientosConfirmados = False
        self.objeto.make_swap() # Para evitar falso positivo de actualización
        # Para no sobrecargar mucho la red volviendo a rellenar LDVs y tal.
        self.rellenar_vencimientos()

    def rellenar_vencimientos(self):
        """
        Mete la información de los vencimientos, pagos, etc.
        del factura actual en la tabla tv_vencimientos.
        """
        # PLAN:Colorear vencimientos incumplidos, con estimaciones rebasadas...
        # OJO: Además, también hay que emparejar por proximidad de fechas 
        # los pagos realizados (clase Pago) con los vencimientos a los que 
        # corresponderían (no hay relación directa).
        vtos = self.preparar_vencimientos()
        # BUG: (?) Se llama a preparar_vencimientos hasta 4 veces (!) al 
        # mostar una factura en pantalla.    
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
                ids = '%d,' % vto[0].id
            else:
                cantidad = 0
                fechavto = ''
                ids = '-1,' # OJO: Si no hay, el ID lo considero -1.
                formapago = ""
            total_vtos += cantidad
            if vto[1] != None:
                fechaest = utils.str_fecha(vto[1].fecha)  # @UnusedVariable
                # OJO: Actualizo la cantidad de la estimación a la cantidad 
                # del vencimiento real:
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
                if vto[2].pagarePago:
                    pagare = "Pagaré con fecha %s y vencimiento %s" % (
                            utils.str_fecha(vto[2].pagarePago.fechaEmision), 
                            utils.str_fecha(vto[2].pagarePago.fechaPago))
                    if vto[2].pagarePago.pendiente:
                        pagare += " (pdte. de pago)"
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
                          utils.float2str(cantidad, 2), 
                          formapago, 
                          realizado,
                          fechapag,
                          utils.float2str(importe, 2),
                          pagare,
                          ids))
        pendiente = total_vtos - total_pagado
        self.wids['e_total_vtos'].set_text(
                "%s" % utils.float2str(total_vtos, 2)) 
        self.wids['e_total_pagado'].set_text(
                "%s" % utils.float2str(total_pagado, 2))
        self.wids['e_total_vencido'].set_text(
                "%s" % utils.float2str(total_vencido, 2))
        self.wids['e_pendiente'].set_text("%s" % utils.float2str(pendiente, 2))
        if total_pagado < total_vencido:
            self.wids['e_total_pagado'].modify_base(gtk.STATE_NORMAL,
                self.wids['e_total_pagado'].get_colormap().alloc_color("red"))
        elif total_pagado == total_vencido:
            self.wids['e_total_pagado'].modify_base(gtk.STATE_NORMAL,
                self.wids['e_total_pagado'].get_colormap().alloc_color(
                    "white"))
        else:
            self.wids['e_total_pagado'].modify_base(gtk.STATE_NORMAL,
                self.wids['e_total_pagado'].get_colormap().alloc_color("blue"))
   

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
        # PLAN: Se podría meter una columna "vencido/pagado hasta el momento" 
        #       con el SUM{i=0→n}(cantidad[i]) siendo n la fila actual.
        factura = self.objeto
        # Joder... para esto de relaciones inyectivas entre
        # conjuntos debe haber un algoritmo más o menos eficiente
        # por ahí, ¿no? Seguro que el mamón de Dijsktra se 
        # inventó algo. Y yo sin internete.
        res = []
        vtos = [v for v in factura.vencimientosPago]
        ests = [v for v in factura.estimacionesPago]
        pags = factura.pagos
        # mas_larga = max(vtos, ests, pags)   # No rula y no sé por qué
        mas_larga = [l for l in (vtos, ests, pags) if len(l)==max(len(vtos), 
                     len(ests), 
                     len(pags))][0]
        if len(mas_larga) == 0: return []
        for i in xrange(len(mas_larga)):  # @UnusedVariable
            res.append([None, None, None])
        def comp(v1, v2):
            if v1.fecha < v2.fecha: return -1
            if v1.fecha > v2.fecha: return 1
            return 0
        def distancia(v1, v2):
            return abs(v1.fecha - v2.fecha)
        def lugar(v):
            if isinstance(v, pclases.VencimientoPago):
                return 0
            elif isinstance(v, pclases.EstimacionPago):
                return 1
            else:
                return 2
            # try:
            #     if v.estimado: return 1
            #     else: return 0
            # except AttributeError:
            #     return 2
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


    def cambiar_pago(self, cell, path, texto):
        """
        Cambia la fecha del pago 
        por la nueva introducida por teclado.
        """
        model = self.wids['tv_vencimientos'].get_model()
        idpago = int(model[path][-1].split(',')[2])
            # Al escribirlo no parecía tan lioso. Lo juro.
        if texto == "":
            # Texto vacío, borrar pago si lo había.
            if idpago > 0:
                pago = pclases.Pago.get(idpago)
                pago.destroy(ventana = __file__)
                self.rellenar_vencimientos()
                return
        try:
            fecha = time.strptime(texto, '%d/%m/%Y')
            anno, mes, dia = fecha[:3]
            fecha = mx.DateTime.DateFrom(day = dia, month = mes, year = anno)
        except ValueError:
            utils.dialogo_info('ERROR EN FORMATO DE FECHA', 
                    'Introduzca las fechas separadas por / y en la forma '
                    'dia/mes/año.', 
                    padre = self.wids['ventana'])
            return
        if idpago > 0:  # Es -1 si no había.
            pago = pclases.Pago.get(idpago)
            pago.fecha = fecha
        elif idpago == -1:  # Para el resto de valores rebota-rebota y en 
                            # tu culo explota.
            factura = self.objeto
            pago = pclases.Pago(fecha = fecha,
                                  facturaCompra = factura,
                                  importe = 0)
            pclases.Auditoria.nuevo(pago, self.usuario, __file__)
        self.rellenar_vencimientos()

    def cambiar_fecha_pago(self, cell, path, texto):
        model = self.wids['tv_vencimientos'].get_model()
        idpago = int(model[path][-1].split(',')[2])
            # Al escribirlo no parecía tan lioso. Lo juro.
        if texto == "":
            # Texto vacío, borrar pago si lo había.
            if idpago > 0:
                pago = pclases.Pago.get(idpago)
                pago.destroy(ventana = __file__)
            self.rellenar_vencimientos()
            return
        try:
            fecha = utils.parse_fecha(texto) 
        except ValueError:
            utils.dialogo_info('ERROR EN FORMATO', 
                    'Introduzca la fecha en formato dd/mm/aaaa.', 
                    padre = self.wids['ventana'])
            return
        if idpago > 0:  # Es -1 si no había.
            pago = pclases.Pago.get(idpago)
            pago.fecha = fecha
        elif idpago == -1:  # Para el resto de valores rebota-rebota y en tu 
                            # culo explota.
            factura = self.objeto
            model = self.wids['tv_vencimientos'].get_model()
            pago = pclases.Pago(fecha = fecha,
                facturaCompra = factura,
                importe = utils._float(model[path][1]))
            pclases.Auditoria.nuevo(pago, self.usuario, __file__)
        self.rellenar_vencimientos()


    def cambiar_importe_pago(self, cell, path, texto):
        model = self.wids['tv_vencimientos'].get_model()
        idpago = int(model[path][-1].split(',')[2])
            # Al escribirlo no parecía tan lioso. Lo juro.
        if texto == "":
            # Texto vacío, borrar pago si lo había.
            if idpago > 0:
                pago = pclases.Pago.get(idpago)
                pago.destroy(ventana = __file__)
                self.rellenar_vencimientos()
                return
        try:
            importe = float(texto)
        except ValueError:
            utils.dialogo_info('ERROR EN FORMATO NUMÉRICO', 
                    'Introduzca un número sin símbolo de moneda.', 
                    padre = self.wids['ventana'])
            return
        if idpago > 0:  # Es -1 si no había.
            pago = pclases.Pago.get(idpago)
            pago.importe = importe
        elif idpago == -1:  # Para el resto de valores rebota-rebota 
                            # y en tu culo explota.
            factura = self.objeto
            pago = pclases.Pago(fecha = mx.DateTime.localtime(),
                                  facturaCompra = factura,
                                  importe = importe)
            pclases.Auditoria.nuevo(pago, self.usuario, __file__)
        self.rellenar_vencimientos()
        
    def cambiar_observaciones_vto(self, cell, path, texto):
        model = self.wids['tv_vencimientos'].get_model() 
        idvto = int(model[path][-1].split(',')[0])
        if idvto > 0:
            vto = pclases.VencimientoPago.get(idvto)
            vto.observaciones = texto
            model[path][2] = vto.observaciones
        else:
            utils.dialogo_info(titulo = "VENCIMIENTO INCORRECTO", 
                texto = "Seleccione un vencimiento válido.", 
                padre = self.wids['ventana'])
        # self.rellenar_vencimientos()
        
    def cambiar_observaciones(self, cell, path, texto):
        model = self.wids['tv_vencimientos'].get_model() 
        idpago = int(model[path][-1].split(',')[2])
        if idpago > 0:
            pago = pclases.Pago.get(idpago)
            pago.observaciones = texto
            model[path][-2] = pago.observaciones
        else:
            utils.dialogo_info(titulo = "VENCIMIENTO NO PAGADO", 
                    texto = "El vencimiento está pendiente de pago.\n"
                            "Introduzca una fecha de pago y vuelva a "
                            "intentarlo.", 
                    padre = self.wids['ventana'])
        # self.rellenar_vencimientos()

    def add_transporte_y_comisiones(self, boton):
        """
        Añade todos los transportes y comisiones pendientes a la factura
        actual.
        """
        proveedor = self.objeto.proveedor
        if proveedor != None:
            filas = []
            transps_pdtes = proveedor.get_transportes_pendientes_de_facturar()
            for transporte in transps_pdtes:
                filas.append(("T%d" % (transporte.id), 
                              "TRANSPORTE", 
                              transporte.albaranSalida 
                                and transporte.albaranSalida.numalbaran or "", 
                              transporte.concepto, 
                              utils.float2str(transporte.precio), 
                              transporte.observaciones, 
                              utils.str_fecha(transporte.fecha)))
            for comision in proveedor.get_comisiones_pendientes_de_facturar():
                filas.append(("C%d" % (comision.id), 
                              "COMISIÓN", 
                              comision.albaranSalida 
                                and comision.albaranSalida.numalbaran or "", 
                              comision.concepto, 
                              utils.float2str(comision.precio), 
                              comision.observaciones, 
                              utils.str_fecha(comision.fecha)))
            resultados = utils.dialogo_resultado(filas,
                    titulo = 'SELECCIONE TRANSPORTES Y COMISIONES A FACTURAR',
                    cabeceras = ('ID', "Tipo", 'Albarán', 'Concepto', 
                                 'Precio', 'Observaciones', 'Fecha'), 
                    padre = self.wids['ventana'], 
                    multi = True)
            if resultados != [] and resultados[0] != -1:
                for stuff in resultados:
                    if "C" in stuff:
                        ide = int(stuff.replace("C", ""))
                        comision = pclases.Comision.get(ide)
                        comision.facturar(self.objeto)
                    elif "T" in stuff:
                        ide = int(stuff.replace("T", ""))
                        transporte = pclases.TransporteACuenta.get(ide)
                        transporte.facturar(self.objeto)
                    else:
                        self.logger.error("facturas_compra::"
                            "add_transporte_y_comisiones -> "
                            "Valor devuelto no es transporte ni comisión: %s" 
                                % stuff)
                self.actualizar_ventana()

    def add_linea_de_compra(self, boton):
        """
        Añade una línea de compra a la factura.
        """
        if self.objeto == None:
            return
        producto, texto_buscado = utils.pedir_producto_compra(
            self.wids['ventana'], self.objeto.proveedor)
        if producto != None:
            ldc = pclases.LineaDeCompra(productoCompra = producto, 
                                        pedidoCompra = None, 
                                        albaranEntrada = None, 
                                        silo = None, 
                                        cargaSilo = None, 
                                        facturaCompra = self.objeto, 
                                        cantidad = 0,       
                                            # Que lo ponga el usuario después
                                        precio = 0,         # Ídem
                                        descuento = 0,      # Ídem de ídem
                                        iva = self.objeto.iva,  # El IVA de la 
                                            # línea por defecto es el de la 
                                            # factura.
                                        entrega = '')
            pclases.Auditoria.nuevo(ldc, self.usuario, __file__)
            self.objeto.vistoBuenoUsuario = True    # Si no lleva albaranes 
                                    # no necesita el visto bueno del usuario
            self.objeto.fechaVistoBuenoUsuario = mx.DateTime.localtime()
            self.actualizar_ventana()
        else:
            if utils.dialogo(titulo = "AÑADIR SERVICIO", 
                             texto = "¿Desea añadir un servicio?", 
                             padre = self.wids['ventana']):
                if texto_buscado == None:
                    texto_buscado = ""
                concepto = utils.dialogo_entrada(titulo = "CONCEPTO", 
                                texto = "Introduzca el concepto del servicio", 
                                padre = self.wids['ventana'], 
                                valor_por_defecto = texto_buscado)
                if concepto != None:
                    servicio = pclases.ServicioTomado(
                            facturaCompra = self.objeto, 
                            precio = 0, 
                            descuento = 0, 
                            cantidad = 1, 
                            concepto = concepto, 
                            transporteACuenta = None, 
                            comision = None, 
                            iva = self.objeto.iva)
                    pclases.Auditoria.nuevo(servicio, self.usuario, __file__)
                    self.objeto.vistoBuenoUsuario = True    
                        # Si no lleva albaranes no necesita el visto bueno 
                        # del usuario
                    self.objeto.fechaVistoBuenoUsuario=mx.DateTime.localtime()
                    self.actualizar_ventana()

    def drop_linea_de_compra(self, boton):
        """
        Elimina la línea de compra seleccionada de la factura.
        Si la línea de compra, una vez quitada de la factura, no 
        tiene más enlaces con albaranes o pedidos, la elimina 
        también de la base de datos.
        """
        model, itr = self.wids['tv_ldvs'].get_selection().get_selected()
        if itr != None:
            idldc = model[itr][-1]
            if idldc != -1 and model[itr].parent == None:
                try:
                    ldc = pclases.LineaDeCompra.get(idldc)
                except:
                    return
                ldc.facturaCompra  = None
                if ldc.albaranEntrada == None and ldc.pedidoCompra == None:
                    try:
                        ldc.destroy(ventana = __file__)
                    except:
                        self.logger.error("facturas_compra.py "
                                "(drop_linea_de_compra): LDC ID %d no se pudo"
                                " eliminar. Debe tener relaciones activas.")
            elif idldc != -1 and model[itr].parent != None:
                try:
                    s = pclases.ServicioTomado.get(idldc)
                except:
                    return
                transporte = s.transporteACuenta
                comision = s.comision
                if transporte == None and comision == None:
                    s.destroy(ventana = __file__)
                else:
                    if transporte != None:
                        transporte.facturar(None)
                    if comision != None:
                        comision.facturar(None)
            if (len(self.objeto.lineasDeCompra) == 0 
                and len(self.objeto.serviciosTomados) == 0):
                self.objeto.vistoBuenoUsuario \
                        = self.objeto.vistoBuenoDirector \
                        = self.objeto.vistoBuenoTecnico \
                        = self.objeto.vistoBuenoComercial = False
                self.objeto.fechaVistoBuenoUsuario \
                        = self.objeto.fechaVistoBuenoDirector \
                        = self.objeto.fechaVistoBuenoTecnico \
                        = self.objeto.fechaVistoBuenoComercial = None
            self.actualizar_ventana()

    def verificar_si_vencimientos(self):
        """
        Comprueba que la factura tiene al menos un vencimiento 
        asociado. Si no es así, pregunta si desea crearlos 
        automáticamente.
        Si tiene vencimientos pero no coinciden con el total de la 
        factura, también pregunta.
        """
        try:
            if self.usuario:
                ventana = pclases.Ventana.selectBy(
                        fichero = "facturas_compra.py")[0]
                permiso = self.usuario.get_permiso(ventana)
                if permiso == None:
                    return
                if self._objetoreciencreado == self.objeto:
                    if not permiso.nuevo:
                        return
                else:
                    if not permiso.escritura:
                        return
        except Exception, msg:
            self.logger.error("facturas_compra::verificar_si_vencimientos "
                              "-> Excepción: %s" % msg)
            pass
        if self.objeto.vencimientosPago != []:
            total = utils.parse_euro(self.wids['e_total'].get_text())
            totvencimientos = sum([v.importe 
                                   for v in self.objeto.vencimientosPago])
            # Compruebo totales de de factura y vencimientos.
            if abs(totvencimientos - total) > 0.1:
                resp = utils.dialogo(titulo = "VENCIMIENTOS NO COINCIDEN", 
                    texto = "El total de los vencimientos (%s) no coincide "
                            "con el total de la factura (%s).\n¿Desea regen"
                            "erarlos automáticamente ahora?" % (
                                utils.float2str(totvencimientos), 
                                utils.float2str(total)), 
                    padre = self.wids['ventana'], 
                    defecto = False, 
                    tiempo = 15)
                if resp:
                    if not self.crear_vencimientos_por_defecto(None):
                        utils.dialogo_info(titulo = "VENCIMIENTOS NO CREADOS", 
                            texto = "Los vencimientos de la factura %s no se "
                                    "pudieron crear. Debe hacerlo manualmente"
                                    "." % (self.objeto.numfactura), 
                            padre = self.wids['ventana']) 
            # Compruebo que las fechas de los vencimientos son correctas, y 
            # si no, aviso.
            if not self.comprobar_fechas_vencimientos():
                if not self.objeto.vencimientosConfirmados:
                    res_recordar = [False]
                    resp = utils.dialogo(titulo = "VENCIMIENTOS NO COINCIDEN", 
                        texto = "Las fechas o el número de vencimientos no coi"
                                "nciden con los vencimientos por defecto del p"
                                "roveedor.\n¿Desea regenerarlos automáticament"
                                "e ahora?",
                        padre = self.wids['ventana'], 
                        defecto = False, 
                        tiempo = 15, 
                        recordar = True, 
                        res_recordar = res_recordar)
                    try:
                        self.objeto.vencimientosConfirmados = res_recordar[0]
                    except IndexError:
                        try:
                            self.objeto.vencimientosConfirmados = res_recordar
                        except:     # ¿ValueError? ¿formencode.api.Invalid?
                            self.objeto.vencimientosConfirmados = False
                    self.objeto.make_swap() 
                    if resp:
                        if not self.crear_vencimientos_por_defecto(None):
                            utils.dialogo_info(
                                titulo = "VENCIMIENTOS NO CREADOS", 
                                texto = "Los vencimientos de la factura %s no"
                                        " se pudieron crear. Debe hacerlo man"
                                        "ualmente." % (self.objeto.numfactura), 
                                padre = self.wids['ventana'])
        # Compruebo que existen vencimientos.
        txt = "La factura %s (%s) no tiene vencimientos.\n¿Desea que se inte"\
              "nten crear automáticamente?" % (
                self.objeto.numfactura, 
                self.objeto.proveedor and self.objeto.proveedor.nombre 
                    or "¡sin proveedor!")
        if self.objeto.vencimientosPago == [] \
           and not self.objeto.bloqueada \
           and utils.dialogo(titulo = "¿CREAR VENCIMIENTOS POR DEFECTO?", 
                             texto = txt, 
                             padre = self.wids['ventana'], 
                             icono = gtk.STOCK_DIALOG_WARNING, 
                             defecto = False):
            if not self.crear_vencimientos_por_defecto(None):
                utils.dialogo_info(titulo = "VENCIMIENTOS NO CREADOS", 
                    texto = "Los vencimientos de la factura %s no se "
                            "pudieron crear. Debe hacerlo manualmente." % (
                                self.objeto.numfactura), 
                    padre = self.wids['ventana'])

    def comprobar_fechas_vencimientos(self):
        """
        Comprueba que las fechas de los vencimientos de la factura coinciden 
        con las fechas de los vencimientos que se crearían automáticamente.
        Si el proveedor no tiene datos suficientes para crear vencimientos 
        automáticos o los vencimientos automáticos coincidirían con los de 
        la factura, devuelve True.
        Si las fechas de los vencimientos no coinciden con los automáticos o 
        bien la factura tiene menos vencimientos que los especificados por 
        defecto o no tiene, devuelve False.
        """
        factura = self.objeto
        proveedor = factura.proveedor
        if proveedor != None:
            vtos = proveedor.get_vencimientos()
            if vtos != None:
                if factura.fecha:
                    fechas_vtos_por_defecto \
                        = proveedor.get_fechas_vtos_por_defecto(factura.fecha)
                    if fechas_vtos_por_defecto:
                        res = self.comparar_fechas_vencimientos(
                                                    fechas_vtos_por_defecto)
                    else:
                        res = True
                else:
                    res = True
        return res

    def comparar_fechas_vencimientos(self, fvtosdef):
        """
        Compara que las fechas de los vencimientos de la factura 
        de la ventana coinciden con la lista de fechas recibida.
        Si la factura no tiene vencimientos o las fechas de éstos 
        coinciden, devuelve True.
        Si hay diferente número de vencimientos que de fechas en la 
        lista recibida o las fechas no coinciden, devuelve False.
        """
        fvtosfra = [vto.fecha for vto in self.objeto.vencimientosPago]
        fvtosfra.sort()
        if len(fvtosfra) == len(fvtosdef):
            res = True
            for fvtofra, fvtodef in zip(fvtosfra, fvtosdef):
                if fvtofra != fvtodef:
                    res = res and False
        else:
            res = False
        return res

    def _salir(self, w, event = None):
        """
        Se ejecuta antes de salir e invoca al procedimiento 
        que verifica que la factura tenga vencimientos.
        """
        # Hacer lo que haya que hacer... 
        if self.objeto != None:
            self.verificar_si_vencimientos()
        # ...y salir. OJO: Se va a ejecutar lo de arriba antes o después de 
        # la ventana de "¿desea salir?"
        # dependiendo de si ha pulsado la X -después- o el botón "Salir" 
        # -se ejecuta antes de mostrar la ventana-.
        self.salir(w, mostrar_ventana = event == None)

    def adjuntar(self, boton):  # XXX: Código para adjuntos
        """
        Adjunta un documento a la factura de compra.
        """
        if self.objeto != None:
            utils.dialogo_adjuntar("ADJUNTAR DOCUMENTO A FACTURA", 
                                   self.objeto, self.wids['ventana'])
            self.rellenar_adjuntos()

    def drop_adjunto(self, boton):  # XXX: Código para adjuntos.
        """
        Elimina el adjunto seleccionado.
        """
        model, itr = self.wids['tv_adjuntos'].get_selection().get_selected()
        if itr != None and utils.dialogo(titulo = "BORRAR DOCUMENTO", 
                            texto = '¿Borrar documento adjunto seleccionado?', 
                            padre = self.wids['ventana']):
            docid = model[itr][-1]
            documento = pclases.Documento.get(docid)
            utils.mover_a_tmp(documento.get_ruta_completa())
            documento.destroy(ventana = __file__)
            self.rellenar_adjuntos()

    def ver_adjunto(self, boton):   # XXX: Código para adjuntos.
        """
        Intenta abrir el adjunto seleccionado.
        """
        from multi_open import open as mopen
        model, itr = self.wids['tv_adjuntos'].get_selection().get_selected()
        if itr != None:
            docid = model[itr][-1]
            documento = pclases.Documento.get(docid)
            self.wids['ventana'].window.set_cursor(
                    gtk.gdk.Cursor(gtk.gdk.WATCH))
            while gtk.events_pending(): gtk.main_iteration(False)
            try:
                if not mopen(documento.get_ruta_completa()):
                    utils.dialogo_info(titulo = "NO SOPORTADO", 
                        texto = "La aplicación no conoce cómo abrir el tipo "
                                "de fichero.", 
                        padre = self.wids['ventana'])
            except:
                utils.dialogo_info(titulo = "ERROR", 
                    texto = "Se produjo un error al abrir el archivo.\nLa "
                            "plataforma no está soportada, no se conoce el "
                            "tipo de archivo o no hay un programa asociado "
                            "al mismo.", 
                    padre = self.wids['ventana'])
            import gobject
            gobject.timeout_add(2000, 
                lambda *args,**kw:self.wids['ventana'].window.set_cursor(None))

def abrir_adjunto_from_tv(tv, path, col):   # XXX: Código para adjuntos.
    """
    Abre el adjunto con el programa asociado al mime-type del mismo.
    """
    model = tv.get_model()
    ide = model[path][-1]
    documento = pclases.Documento.get(ide)
    from multi_open import open as mopen
    mopen(documento.get_ruta_completa())


if __name__=='__main__':
    a = FacturasDeEntrada(usuario = pclases.Usuario.select(
        pclases.Usuario.q.usuario.contains("maril"))[0])
    #a = FacturasDeEntrada()


