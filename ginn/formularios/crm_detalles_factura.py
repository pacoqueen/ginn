#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado,                   #
#                          (pacoqueen@users.sourceforge.net)                  #
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
## crm_detalles_factura.py - Detalles para CRM de facturas de venta.
###################################################################
## NOTAS:
## 
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, pango
try:
    from framework import pclases
except ImportError:
    import sys
    from os.path import join as pathjoin
    sys.path.append(pathjoin("..", "framework"))
    from framework import pclases
import mx, mx.DateTime
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes
import pclase2tv

def callback(treeview, allocation, column, cell):
    otherColumns = (c for c in treeview.get_columns() if c != column)
    newWidth = allocation.width - sum(c.get_width() for c in otherColumns)
    newWidth -= treeview.style_get_property("horizontal-separator") * 2
    if cell.props.wrap_width == newWidth or newWidth <= 0:
        return
    cell.props.wrap_width = newWidth
    store = treeview.get_model()
    if store:
        itr = store.get_iter_first()
        while itr and store.iter_is_valid(itr):
            store.row_changed(store.get_path(itr), itr)
            itr = store.iter_next(itr)
            treeview.set_size_request(0,-1)

def colorear_tv_alarmas(tv):
    def cell_func(column, cell, model, itr):
        color = None
        ide = model[itr][-1]
        alarma = pclases.Alarma.get(ide)
        if alarma.fechahoraAlarma <= mx.DateTime.localtime():
            if alarma.estado.pendiente:
                color = "red"
            else:
                color = "green"
        elif alarma.estado.pendiente:
            color = "orange"
        cell.set_property("cell-background", color)
    cols = tv.get_columns()
    for col in cols:
        for cell in col.get_cell_renderers():
            col.set_cell_data_func(cell, cell_func)


class CRM_DetallesFactura(Ventana):

    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'crm_detalles_factura.glade', 
                         objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_abrir_factura/clicked': self.abrir_factura, 
                       'b_buscar/clicked': self.buscar, 
                       'b_abrir_cliente/clicked': self.abrir_cliente, 
                       'b_add_adjunto/clicked': self.adjuntar,
                       'b_drop_adjunto/clicked': self.drop_adjunto,
                       'b_abrir_adjunto/clicked': self.ver_adjunto,
                       'b_imprimir/clicked': self.imprimir, 
                       'b_drop_anotaciones/clicked': self.drop_tvitem, 
                       'b_drop_alertas/clicked': self.drop_tvitem, 
                       'b_drop_contactos/clicked': self.drop_tvitem, 
                       'b_drop_vencimientos/clicked': self.drop_tvitem, 
                       'b_save/clicked': self.guardar_adjunto, 
                       'b_add_anotaciones/clicked': self.add_tvitem, 
                       'b_add_alertas/clicked': self.add_tvitem, 
                       'b_add_contactos/clicked': self.add_tvitem, 
                       'b_add_vencimientos/clicked': self.add_tvitem, 
                       'b_add_documentos_pago/clicked': self.add_docpago, 
                       'b_drop_documentos_pago/clicked': self.drop_docpago, 
                       }
        self.add_connections(connections)
        if not objeto:
            try:
                objeto = pclases.FacturaVenta.select(orderBy = "-id")[0]
            except IndexError:
                utils.dialogo_info(titulo = "NO SE ENCONTRARON FACTURAS", 
                    texto = "No se encontraron facturas que mostrar", 
                    padre = self.wids['ventana'])
                return
        self.objeto = objeto
        cols = (('Nombre', 'gobject.TYPE_STRING', 
                    True, True, True, self.cambiar_nombre_adjunto), 
                ('Observaciones', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_observaciones_adjunto),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_adjuntos'], cols)
        self.wids['tv_adjuntos'].connect("row-activated",abrir_adjunto_from_tv)
        cols = (("Codigo", 'gobject.TYPE_STRING', False, True, True, None),
                ("Fecha recepción", 'gobject.TYPE_STRING', 
                    False, True, False, self.cambiar_nombre_adjunto),
                ("Fecha cobro", 'gobject.TYPE_STRING',False,True,False,None),
                ("Importe", 'gobject.TYPE_STRING', False, True, False, None),
                ("Observaciones", 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_observaciones_pagare),
                ("Plazo pago real", "gobject.TYPE_STRING", 
                    False, True, False, None), 
                ("Diferencia vtos.", "gobject.TYPE_STRING", 
                    False, True, False, None), 
                ("PUID", 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(self.wids['tv_documentos_pago'], cols)
        self.wids['tv_documentos_pago'].connect("row-activated",
                                                self.abrir_docpago)
        self.tvanotaciones = pclase2tv.Pclase2tv(pclases.Nota, 
                                            self.wids['tv_anotaciones'], 
                                            self.objeto, 
                                            cols_a_ignorar=["facturaVentaID"], 
                                            nombres_col = ["Fecha y hora"])
        # TODO: No funciona bien lo del wrap de celda. Hay que probarlo mejor 
        # antes de subir a producción. Mientras, habilito la barra horizontal:
        self.wids['scrolledwindow1'].set_policy(gtk.POLICY_AUTOMATIC, 
                                                gtk.POLICY_AUTOMATIC)
        #for col in self.wids['tv_anotaciones'].get_columns()[-2]:
        #    for cell in col.get_cell_renderers():
        #        self.wids['tv_anotaciones'].connect_after("size-allocate", 
        #                                                  callback, col, cell)
        self.tvcontactos = pclase2tv.Pclase2tv(pclases.Contacto, 
                                          self.wids['tv_contactos'], 
                                          self.objeto,
                                          cols_a_ignorar = [""])
        self.tvcontactos.rellenar_tabla = self.rellenar_tabla_contactos
        self.tvalertas = pclase2tv.Pclase2tv(pclases.Alarma, 
                                        self.wids['tv_alertas'], 
                                        self.objeto, 
                                        cols_a_ignorar = [
                    "facturaVentaID", "objetoRelacionado", "estadoID"], 
                    nombres_col = ["Fecha y hora", "Texto", 
                                   "Fecha y hora de alarma", "Observaciones"])
        self.colorear_alarmas()
        self.tvvencimientos = pclase2tv.Pclase2tv(pclases.VencimientoCobro, 
                                            self.wids['tv_vencimientos'], 
                                            self.objeto, 
                                            cols_a_ignorar = [
            "facturaVentaID", "prefacturaID", "cuentaOrigenID", "reciboID"])
        self.rellenar_widgets()
        gtk.main()

    def abrir_docpago(self, tv, path, col):
        """
        Abre el documento de pago al que se le ha hecho doble clic en una 
        ventana nueva.
        """
        model = tv.get_model()
        tipo, id = model[path][-1].split(":")
        if tipo == "PAGC":
            clase = pclases.PagareCobro
            from pagares_cobros import PagaresCobros as ventana
        elif tipo == "C": 
            clase = pclases.Confirming
            from confirmings import Confirmings as ventana
        else:
            return
        documento_pago = clase.get(id)
        v = ventana(usuario = self.usuario, objeto = documento_pago)

    def drop_docpago(self, boton):
        """
        Elimina el documento de pago seleccionado.
        """
        sel = self.wids["tv_documentos_pago"].get_selection()
        model, itr = sel.get_selected()
        if itr:
            objeto = pclases.getObjetoPUID(model[itr][-1])
            objeto.destroy_en_cascada(ventana = __file__)
            model.remove(itr)

    def add_docpago(self, boton):
        """
        Dependiendo de la forma de pago de la factura abre la ventana de 
        documentos de pago correspondiente con el objeto ya creado.
        """
        fra = self.objeto
        if fra and fra.vencimientosCobro:
            from pagares_cobros import preparar_vencimientos
            vtos_full = preparar_vencimientos(fra)
            vtos_sin_cobro = [v for v in vtos_full if not v[2]]
            # Voy a intentar adivinar la forma de pago de los vencimientos.
            pagares = []
            confirmings = []
            resto = []
            for v, estimacion, cobros in vtos_sin_cobro:
                if ("PAGARE" in v.observaciones.upper() 
                    or "PAGARÉ" in v.observaciones.upper()
                    or "PAGARé" in v.observaciones.upper()):
                    pagares.append(v)
                elif ("CONFIRMIN" in v.observaciones.upper()):
                    confirmings.append(v)
                else:
                    resto.append(v)
            # Creo objetos y abro ventanas:
            estados_no_pendientes = pclases.Estado.select(
                pclases.Estado.q.pendiente == False, 
                orderBy = "-id")
            try:
                estado_no_pendiente = estados_no_pendientes[1]  # Cerrada.
            except IndexError:
                estado_no_pendiente = estados_no_pendientes[0]  
                    # Por si no tiene la configuración de estados estándar.
            else:
                estado_no_pendiente = None  # Borraré las alertas.
            if pagares:
                total_vtos = sum([v.importe for v in pagares])
                pagare = pclases.PagareCobro(codigo = "",
                    fechaRecepcion = mx.DateTime.localtime(), 
                    fechaCobro = pagares[0].fecha, 
                    cantidad = total_vtos, 
                    cobrado = -1, 
                    observaciones = "Creado desde CRM.", 
                    fechaCobrado = None, 
                    procesado = False)
                pclases.Auditoria.nuevo(pagare, self.usuario, __file__)
                for v in pagares:
                    observaciones="Pagaré %s con fecha %s y vencimiento %s" % (
                                pagare.codigo, 
                                utils.str_fecha(pagare.fechaRecepcion), 
                                utils.str_fecha(pagare.fechaCobro))
                    c = pclases.Cobro(confirming = None, 
                                      pagareCobro = pagare, 
                                      facturaVenta = v.facturaVenta, 
                                      prefactura = None, 
                                      facturaDeAbono = None, 
                                      cliente = v.facturaVenta 
                                            and v.facturaVenta.cliente or None,
                                      fecha = v.fecha, 
                                      importe = v.importe, 
                                      observaciones = observaciones) 
                    pclases.Auditoria.nuevo(c, self.usuario, __file__)
                    # Anulo alarmas pendientes:
                    for a in v.facturaVenta.alarmas:
                        if estado_no_pendiente:
                            a.estado = estado_no_pendiente
                        else:
                            a.destroy(ventana = __file__)
                import pagares_cobros
                pagares_cobros.PagaresCobros(usuario = self.usuario, 
                                             objeto = pagare)
                self.actualizar_ventana()
            if confirmings:
                total_vtos = sum([v.importe for v in confirmings])
                confirming = pclases.Confirming(codigo = "",
                    fechaRecepcion = mx.DateTime.localtime(), 
                    fechaCobro = confirmings[0].fecha, 
                    cantidad = total_vtos, 
                    cobrado = -1, 
                    observaciones = "Creado desde CRM.", 
                    fechaCobrado = None, 
                    procesado = False)
                pclases.Auditoria.nuevo(confirming, self.usuario, __file__)
                for v in confirmings:
                    observaciones = "Confirming %s con fecha %s "\
                                    "y vencimiento %s" % (
                                confirming.codigo, 
                                utils.str_fecha(confirming.fechaRecepcion), 
                                utils.str_fecha(confirming.fechaCobro))
                    c = pclases.Cobro(confirming = confirming, 
                                      pagareCobro = None, 
                                      facturaVenta = v.facturaVenta, 
                                      prefactura = None, 
                                      facturaDeAbono = None, 
                                      cliente = v.facturaVenta 
                                        and v.facturaVenta.cliente or None, 
                                      fecha = v.fecha, 
                                      importe = v.importe, 
                                      observaciones = observaciones) 
                    pclases.Auditoria.nuevo(c, self.usuario, __file__)
                    # Anulo alarmas pendientes:
                    for a in v.facturaVenta.alarmas:
                        if estado_no_pendiente:
                            a.estado = estado_no_pendiente
                        else:
                            a.destroy(ventana = __file__)
                import confirmings as ventana_confirming 
                ventana_confirming.Confirmings(usuario = self.usuario, 
                                               objeto = confirming)
                self.actualizar_ventana()
            if resto:
                txtvtos = ["%s, %s €, %s" % (utils.str_fecha(v.fecha), 
                                             utils.float2str(v.importe), 
                                             v.observaciones)
                           for v in resto]
                utils.dialogo_info(titulo = "FORMA DE PAGO INCORRECTA", 
                    texto = "La forma de pago de los siguientes vencimientos\n"
                        "no se puede liquidar mediante documentos de pago:\n%s"
                        % "\n".join(txtvtos),
                    padre = self.wids['ventana'])

    def colorear_alarmas(self):
        colorear_tv_alarmas(self.wids['tv_alertas'])

    def cambiar_observaciones_pagare(self, cell, path, texto):
        model = self.wids['tv_documentos_pago'].get_model() 
        puid = model[path][-1]
        objeto = pclases.getObjetoPUID(puid)
        objeto.observaciones = texto
        model[path][4] = objeto.observaciones

    def rellenar_tabla_contactos(self, *args, **kw):
        """
        Es relación muchos a muchos, no puedo usar el pclases2tv (de momento).
        """
        model = self.wids['tv_contactos'].get_model()
        model.clear()
        if self.objeto.obra:
            for c in self.objeto.obra.contactos:
                if c.id not in [fila[-1] for fila in model]:
                    model.append((c.nombre, c.apellidos, c.cargo, c.telefono, 
                                  c.fax, c.movil, c.correoe, c.web, 
                                  c.observaciones, c.id))

    def abrir_cliente(self, boton):
        """
        Abre el cliente de la factura en pantalla.
        """
        import clientes
        v = clientes.Clientes(self.objeto.cliente, self.usuario)

    def rellenar_widgets(self):
        self.wids['e_numfactura'].set_text(self.objeto.numfactura)
        self.wids['e_numfactura'].modify_font(
            pango.FontDescription("Monospace 18"))
        self.wids['e_fecha'].set_text(utils.str_fecha(self.objeto.fecha))
        self.wids['e_cliente'].set_text(self.objeto.cliente.nombre)
        self.wids['e_obra'].set_text(self.objeto.obra 
                                     and self.objeto.obra.nombre or "")
        self.tvanotaciones.rellenar_tabla() 
        self.tvcontactos.rellenar_tabla()
        self.tvalertas.rellenar_tabla()
        totales = self.tvvencimientos.rellenar_tabla(sumatorios = ["importe"])
        self.wids['e_total'].set_text(
            utils.float2str(self.objeto.calcular_importe_total()))
        self.wids['e_pendiente'].set_text(
            utils.float2str(self.objeto.calcular_pendiente_cobro()))
        self.wids['e_total_vtos'].set_text(
            utils.float2str(totales[0]))
        self.wids['e_vencido'].set_text(
            utils.float2str(self.objeto.calcular_vencido()))
        self.rellenar_adjuntos()
        self.rellenar_pagares()

    def rellenar_pagares(self):
        """
        Rellena la tabla de documentos de pago con pagarés y confirmings.
        """
        model = self.wids['tv_documentos_pago'].get_model()
        model.clear()
        for c in self.objeto.cobros:
            if c.confirming:
                o = c.confirming
            elif c.pagareCobro:
                o = c.pagareCobro
            else:
                continue
            model.append((o.codigo, utils.str_fecha(o.fechaRecepcion), 
                          utils.str_fecha(o.fechaCobro), 
                          utils.float2str(o.cantidad), 
                          o.observaciones, 
                          c.calc_plazo_pago_real(), 
                          c.calc_diferencia_plazo_pago(), 
                          o.get_puid()))

    def adjuntar(self, boton):
        """
        Adjunta un documento a la factura de compra.
        """
        if self.objeto != None:
            utils.dialogo_adjuntar("ADJUNTAR DOCUMENTO A FACTURA", 
                                   self.objeto, self.wids['ventana'])
            self.rellenar_adjuntos()

    def drop_adjunto(self, boton):
        """
        Elimina el elemento seleccionado.
        """
        import shutil
        model, itr = self.wids['tv_adjuntos'].get_selection().get_selected()
        if itr != None and utils.dialogo(titulo = "BORRAR DOCUMENTO", 
                            texto = '¿Borrar documento adjunto seleccionado?', 
                            padre = self.wids['ventana']):
            docid = model[itr][-1]
            documento = pclases.Documento.get(docid)
            try:
                utils.mover_a_tmp(documento.get_ruta_completa())
            except shutil.Error, msg:
                txt = "%scrm_detalles_factura.py::drop_adjunto -> No se pudo "\
                      "mover el fichero al directorio temporal. Probablemen"\
                      "te ya exista allí. Mensaje de la excepción: %s" % (
                        self.usuario and self.usuario.usuario or "", msg)
                print txt
                self.logger.error(txt)
            documento.destroy(ventana = __file__)
            self.rellenar_adjuntos()

    def ver_adjunto(self, boton):
        """
        Intenta abrir el adjunto seleccionado.
        """
        from multi_open import open as mopen
        model, itr = self.wids['tv_adjuntos'].get_selection().get_selected()
        if itr != None:
            docid = model[itr][-1]
            documento = pclases.Documento.get(docid)
            self.wids['ventana'].window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
            while gtk.events_pending(): gtk.main_iteration(False)
            try:
                if not mopen(documento.get_ruta_completa()):
                    utils.dialogo_info(titulo = "NO SOPORTADO", 
                                       texto = "La aplicación no conoce cómo abrir el tipo de fichero.", 
                                       padre = self.wids['ventana'])
            except:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "Se produjo un error al abrir el archivo.\nLa plataforma no está soportada, no se conoce el tipo de archivo o no hay un programa asociado al mismo.", 
                                   padre = self.wids['ventana'])
            import gobject
            gobject.timeout_add(2000, lambda *args, **kw: self.wids['ventana'].window.set_cursor(None))

    def rellenar_adjuntos(self):
        """
        Introduce los adjuntos del objeto en la tabla de adjuntos.
        """
        model = self.wids['tv_adjuntos'].get_model()
        model.clear()
        if self.objeto != None:
            docs = self.objeto.documentos[:]
            docs.sort(lambda x, y: utils.orden_por_campo_o_id(x, y, "id"))
            for adjunto in self.objeto.documentos:
                model.append((adjunto.nombre, adjunto.observaciones, adjunto.id))

    def cambiar_nombre_adjunto(self, cell, path, texto):
        model = self.wids['tv_adjuntos'].get_model() 
        iddoc = model[path][-1]
        pclases.Documento.get(iddoc).nombre = texto
        model[path][0] = pclases.Documento.get(iddoc).nombre

    def cambiar_observaciones_adjunto(self, cell, path, texto):
        model = self.wids['tv_adjuntos'].get_model() 
        iddoc = model[path][-1]
        pclases.Documento.get(iddoc).observaciones = texto
        model[path][1] = pclases.Documento.get(iddoc).observaciones

    def abrir_factura(self, boton):
        """
        Abre la factura en una ventana nueva.
        """
        import facturas_venta
        v = facturas_venta.FacturasVenta(objeto = self.objeto, 
                                         usuario = self.usuario)

    def drop_tvitem(self, boton):
        """
        Elimina la tarea seleccionada en el TreeView.
        """
        tv_name = boton.name.replace("b_drop_", "tv_")
        clase = {'tv_anotaciones': pclases.Nota, 
                 'tv_contactos': pclases.Contacto, 
                 'tv_alertas': pclases.Alarma, 
                 'tv_vencimientos': pclases.VencimientoCobro,  
                 }[tv_name]
        model, itr = self.wids[tv_name].get_selection().get_selected()
        if itr:
            ide = model[itr][-1]
            objeto = clase.get(ide)
            try:
                if isinstance(objeto, pclases.Contacto):
                    objeto.removeObra(self.objeto.obra) # Si hay contactos en 
                        # el TreeView, hay obra en self.objeto.
                objeto.destroy(ventana = __file__)
            except Exception, msg:
                utils.dialogo_info(titulo = "ERROR", 
                    texto = "Ocurrió un error y no se pudo eliminar la fila"\
                            " seleccionada.\n\n\nInformación de depuración:"\
                            "\n%s" % msg, 
                    padre = self.wids['ventana'])
            else:
                model.remove(itr)

    def add_tvitem(self, boton):
        """
        Añade una elemento al TreeView.
        """
        tv_name = boton.name.replace("b_add_", "tv_")
        if tv_name == "tv_contactos":
            if not self.objeto.obra:
                self.objeto.obra = self.elegir_o_crear_obra()
            if self.objeto.obra:
                nombre = utils.dialogo_entrada(
                    titulo = "NOMBRE DEL NUEVO CONTACTO", 
                    texto = "Introduzca el nombre (sin apellidos) del nuevo "\
                            "contacto.", 
                    padre = self.wids['ventana'])
                if not nombre:
                    return      # Canceló.
                contactos = self.objeto.cliente.get_contactos_obras()
                contactos = [c for c in contactos 
                             if nombre.upper().strip() in c.nombre]
                if contactos:
                    ops = [(c.id, c.get_str_contacto()) for c in contactos]
                    idcontacto = utils.dialogo_combo(
                        titulo = "SELECCIONE CONTACTO", 
                        texto = "Si puede ver al contacto en la lista del \n"\
                                "desplegable inferior, selecciónelo.\n"\
                                "En otro caso, pulse en «Cancelar»", 
                        padre = self.wids['ventana'], 
                        ops = ops)
                    if not idcontacto:
                        contacto = pclases.Contacto(nombre = nombre, 
                                                    apellidos = "", 
                                                    cargo = "", 
                                                    telefono = "", 
                                                    fax = "", 
                                                    movil = "", 
                                                    correoe = "", 
                                                    web = "", 
                                                    observaciones = "")
                        pclases.Auditoria.nuevo(contacto, self.usuario, 
                                                __file__)
                    else:
                        contacto = pclases.Contacto.get(idcontacto)
                else:
                        contacto = pclases.Contacto(nombre = nombre, 
                                                    apellidos = "", 
                                                    cargo = "", 
                                                    telefono = "", 
                                                    fax = "", 
                                                    movil = "", 
                                                    correoe = "", 
                                                    web = "", 
                                                    observaciones = "")
                        pclases.Auditoria.nuevo(contacto, self.usuario, 
                                                __file__)
                if contacto not in self.objeto.obra.contactos:
                    contacto.addObra(self.objeto.obra)
                self.wids['e_obra'].set_text(self.objeto.obra 
                    and self.objeto.obra.nombre or "")
                self.tvcontactos.rellenar_tabla()
        else:
            try:
                estado = pclases.Estado.get(1)  # *Debería* existir.
            except:
                estado = None
            clase, valores_defecto, params_relacion = {
                'tv_anotaciones': (pclases.Nota, 
                                   {}, 
                                   {"facturaVenta": self.objeto}), 
                'tv_alertas': (pclases.Alarma, 
                               {"estado": estado, 
                                "fechahoraAlarma": mx.DateTime.localtime() + 
                                                   mx.DateTime.oneDay, 
                                "fechahora": mx.DateTime.localtime(), 
                                "objetoRelacionado": None}, 
                               {"facturaVenta": self.objeto}), 
                'tv_vencimientos': (pclases.VencimientoCobro, 
                                    {"fecha": mx.DateTime.localtime()}, 
                                    {"facturaVenta": self.objeto}), 
                }[tv_name]
            params = {}
            for dict in valores_defecto, params_relacion:
                for k in dict:
                    params[k] = dict[k]
            objeto = clase(**params)
            self.actualizar_ventana()

    def elegir_o_crear_obra(self):
        """
        Crea una nueva obra relacionada con la factura de venta de la ventana.
        """
        obras = pclases.Obra.select(orderBy = "nombre")
        obras = [o for o in obras 
                 if self.objeto.cliente in o.clientes]
        idobra = utils.dialogo_combo(titulo = "SELECCIONE OBRA", 
            texto = "Es necesario relacionar una obra con la factura."\
                    "\nSeleccione una del desplegable inferior o cree una "\
                    "nueva", 
            padre = self.wids['ventana'], 
            ops = [(0, "Crear una obra nueva")] + [(o.id, o.nombre) 
                                                    for o in obras]) 
        if idobra == 0:
            nombre = utils.dialogo_entrada(titulo = "NOMBRE DE OBRA", 
                texto = "Introduzca el nombre de la obra:", 
                padre = self.wids['ventana'])
            if not nombre:
                return None
            direccion = utils.dialogo_entrada(titulo = "DIRECCIÓN", 
                texto = "Introduzca la dirección de la obra:", 
                padre = self.wids['ventana'])
            if direccion == None:
                return None 
            ciudad = utils.dialogo_entrada(titulo = "CIUDAD", 
                texto = "Introduzca la ciudad:", 
                padre = self.wids['ventana'])
            if ciudad == None:
                return None
            cp = utils.dialogo_entrada(titulo = "CÓDIGO POSTAL", 
                texto = "Introduzca el código postal", 
                padre = self.wids['ventana'])
            if cp == None:
                return None
            provincia = utils.dialogo_entrada(titulo = "PROVINCIA", 
                texto = "Introduzca la provincia:", 
                padre = self.wids['ventana'])
            if provincia == None:
                return None
            # De fecha de inicio, fecha de fin de obra y observacione pasamos a 
            # este nivel. Eso se afina en la ventana de obras.
            obra = pclases.Obra(nombre = nombre, direccion = direccion, 
                    cp = cp, ciudad = ciudad, provincia = provincia, 
                    fechainicio = None, fechafin = None, 
                    observaciones = "Creada desde módulo CRM: detalles de "\
                                    "factura.", 
                    generica = False)
            pclases.Auditoria.nuevo(obra, self.usuario, __file__)
            obra.addCliente(self.objeto.cliente)
        elif idobra:
            obra = pclases.Obra.get(idobra)
        else:
            obra = None
        return obra

    def ver_factura_en_tv(self, tv, path, view_column):
        """
        Despliega en el TreeView de facturas la factura de la tarea y sitúa 
        el cursor en ella.
        """
        # print "Pintinho"
        model = tv.get_model()
        id = model[path][-1]
        tarea = pclases.Tarea.get(id)
        model = self.wids['tv_datos'].get_model()
        for fila in model:
            #print fila
            for hijo in model[fila.iter].iterchildren(): 
                #print model[hijo.iter[-1]]
                if model[hijo.iter][-1] == tarea.facturaVentaID:
                    path = model.get_path(hijo.iter)
                    self.wids['tv_datos'].expand_to_path(path) 
                    self.wids['tv_datos'].set_cursor(path) 

    def chequear_cambios(self):
        pass

    def buscar(self, boton):
        numfra = utils.dialogo_entrada(titulo = "BUSCAR FACTURA", 
            texto = "Introduzca el número de factura a buscar:", 
            padre = self.wids['ventana'])
        if numfra:
            fra = None
            fras = pclases.FacturaVenta.select(
                pclases.FacturaVenta.q.numfactura.contains(numfra))
            if fras.count() == 0:
                utils.dialogo_info(titulo = "FACTURA NO ENCONTRADA", 
                    texto = "No se encontraron facturas con el número «%s»" % (
                        numfra), 
                    padre = self.wids['ventana'])
            else:
                if fras.count() == 1:
                    fra = fras[0]
                else:
                    facturas = [(f.id, f.numfactura, f.cliente.nombre, 
                                 utils.str_fecha(f.fecha), 
                                 utils.float2str(f.calcular_importe_total()))
                                for f in fras]
                    fra = utils.dialogo_resultado(
                        titulo = "SELECCIONE FACTURA",  
                        padre = self.wids['ventana'], 
                        cabeceras = ["ID", "Número de factura", "Cliente", 
                                     "Fecha", "Importe total"], 
                        filas = facturas)
                    fra = pclases.FacturaVenta.get(fra)
                if fra:
                    self.objeto = fra
                    # Cambio los filtros de los TreeView, que siguen 
                    # relacionados con el objeto antiguo.
                    filtro=lambda o:getattr(o,"facturaVentaID")==self.objeto.id
                    self.tvanotaciones.filtro = filtro
                    self.tvalertas.filtro = filtro
                    self.tvvencimientos.filtro = filtro
                    self.rellenar_widgets()

    def guardar_adjunto(self, boton):
        """
        Ofrece al usuario una ventana para guardar el adjunto seleccionado.
        """
        model, itr = self.wids['tv_adjuntos'].get_selection().get_selected()
        if itr != None:
            docid = model[itr][-1]
            documento = pclases.Documento.get(docid)
            utils.dialogo_guardar_adjunto(documento)

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe.
        """
        from ginn.formularios.reports import abrir_pdf
        abrir_pdf(geninformes.crm_generar_pdf_detalles_factura(self.objeto))

def abrir_adjunto_from_tv(tv, path, col):
    """
    Abre el adjunto con el programa asociado al mime-type del mismo.
    """
    model = tv.get_model()
    ide = model[path][-1]
    documento = pclases.Documento.get(ide)
    from multi_open import open as mopen
    mopen(documento.get_ruta_completa())



if __name__ == '__main__':
    #t = CRM_DetallesFactura(pclases.FacturaVenta.select(orderBy = "-id")[0])
    f = pclases.FacturaVenta.select(
                pclases.FacturaVenta.q.numfactura == "X111172", 
                orderBy = "-id")[0]
    t = CRM_DetallesFactura(objeto = f)
    pclases.DEBUG = True
    # t = CRM_DetallesFactura()

