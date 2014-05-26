#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2014  Francisco José Rodríguez Bogado                    #
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
## presupuestos.py - Ofertas de precios a clientes.
###################################################################
## NOTAS:
##  
## ----------------------------------------------------------------
###################################################################
## Changelog:
## 15 de marzo de 2007 -> Inicio 
## 26 de agosto de 2013 -> A brand new version
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk, mx.DateTime
from framework import pclases
from framework.seeker import VentanaGenerica 
from formularios.ventana_progreso import VentanaActividad
from formularios.ventana_progreso import VentanaProgreso
import gobject
import sys
import pango
from formularios import postomatic
from formularios.custom_widgets import CellRendererAutoComplete
import datetime
import time
from formularios.utils import enviar_correoe

NIVEL_VALIDACION = 1
CONDICIONES_DURAS = (pclases.PLAZO_EXCESIVO, 
                     pclases.SIN_FORMA_DE_PAGO, 
                     pclases.PRECIO_INSUFICIENTE, 
                     pclases.COND_PARTICULARES, 
                     pclases.COMERCIALIZADO)
CONDICIONES_BLANDAS = (pclases.NO_VALIDABLE,    # @UnusedVariable
                       pclases.CLIENTE_DEUDOR, 
                       pclases.SIN_CIF)

class Presupuestos(Ventana, VentanaGenerica):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self.clase = pclases.Presupuesto
        self.dic_campos = {"comercialID": "cb_comercial", 
                           "fecha": "e_fecha", 
                           "adjudicada": "ch_adjudicada", 
                           "clienteID": "cbe_cliente", 
                           "cif": "e_cif", 
                           "direccion": "e_direccion", 
                           "cp": "e_cp", 
                           "ciudad": "e_ciudad", 
                           "provincia": "e_provincia", 
                           "pais": "e_pais", 
                           "telefono": "e_telefono", 
                           "email": "e_email", 
                           "obraID": "cbe_obra", 
                           "formaDePagoID": "cb_forma_cobro", 
                           "texto": "txt_condiciones", 
                           "observaciones": "txt_observaciones", 
                           "estudio": "rb_estudio", 
                           "personaContacto": "e_persona_contacto", 
                           'cerrado': "ch_cerrado", 
                           "rechazado": "ch_denegado", 
                           "motivo": "e_motivo", 
                           # Ficha de solicitud de crédito:
                           "credUte": "e_cred_ute", 
                           "credLicitador": "e_cred_licitador", 
                           "credDirfiscal": "e_cred_dirfiscal", 
                           "credCpfiscal": "e_cred_cpfiscal", 
                           "credTelefonofiscal": "e_cred_telefonofiscal", 
                           "credContactofiscal": "e_cred_contactofiscal", 
                           "credPoblacionfiscal": "e_cred_poblacionfiscal", 
                           "credFaxfiscal": "e_cred_faxfiscal", 
                           "credProvinciafiscal": "e_cred_provinciafiscal", 
                           "credEmailfiscal": "e_cred_emailfiscal", 
                           "credMovilfiscal": "e_cred_movilfiscal", 
                           "credTelefonocontratos":"e_cred_telefonocontratos",
                           "credEmailcontratos": "e_cred_emailcontratos", 
                           "credDircontratos": "e_cred_dircontratos", 
                           "credCpcontratos": "e_cred_cpcontratos", 
                           "credProvinciacontratos": 
                                                   "e_cred_provinciacontratos",
                           "credContactocontratos":"e_cred_contactocontratos",
                           "credPoblacioncontratos": 
                                                   "e_cred_poblacioncontratos", 
                           "credMovilcontratos": "e_cred_movilcontratos", 
                           "credDirobra": "e_cred_dirobra", 
                           "credCpobra": "e_cred_cpobra", 
                           "credProvinciaobra": "e_cred_provinciaobra", 
                           "credContactoobra": "e_cred_contactoobra", 
                           "credPoblacionobra": "e_cred_poblacionobra", 
                           "credMovilobra": "e_cred_movilobra", 
                           "credEntidad": "e_cred_entidad", 
                           "credOficina": "e_cred_oficina", 
                           "credDigitocontrol": "e_cred_digitocontrol", 
                           "credNumcuenta": "e_cred_numcuenta", 
                           "credFdp": "e_cred_fdp", 
                           "credDiapago1": "e_cred_diapago1", 
                           "credDiapago2": "e_cred_diapago2", 
                           "credDiapago3": "e_cred_diapago3", 
                           "credCredsolicitado": "e_cred_credsolicitado", 
                           "credVbNombrecomercial":
                               "e_cred_vb_nombrecomercial", 
                           "credVbNombreadmon":
                               "e_cred_vb_nombreadmon", 
                           "credAsegurado":
                               "e_cred_asegurado", 
                           "credFechaasegurado": "e_cred_fechaasegurado", 
                           "credConcedido": "e_cred_concedido", 
                           "credFechaconcedido": "e_cred_fechaconcedido", 
                           "credFecha": "e_cred_fecha", 
                           "credApertura": "ch_cred_apertura", 
                           "credAumento": "ch_cred_aumento", 
                           "credSolicitud": "ch_cred_solicitud", 
                           "credEntidades": "txt_cred_entidades", 
                           "credObservaciones": "txt_cred_observaciones", 
                           "credCondiciones": "txt_cred_condiciones", 
                           "credMotivoRechazo": "txt_cred_motivo_rechazo", 
                           # "ch_cred_vb_comercial", Activado si presupuesto.usuario
                           # "ch_cred_vb_admon", Activado si presupuesto.cred_usuario
                           # "e_cred_cif", Mismo que el presupuesto.cliente.cif
                           # "e_cred_nombre", Mismo que el presupuesto.cliente.nombrecliente
                           # "e_cred_obra", Mismo que presupuesto.nombreobra
                           # "e_cred_comercial", Mismo que presupuesto.comercial
                          }
        Ventana.__init__(self, 'presupuestos.glade', objeto, 
                         usuario = self.usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_nuevo/clicked': self.nuevo,
                       'b_borrar/clicked': self.borrar,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_buscar/clicked': self.buscar, 
                       'b_fecha/clicked': self.fecha,  
                       'rb_pedido/clicked': 
                          lambda rb: 
                            map(lambda item: item.set_inconsistent(False), 
                                rb.get_group()), 
                       'rb_estudio/clicked': 
                          lambda rb: 
                            map(lambda item: item.set_inconsistent(False), 
                                rb.get_group()), 
                       'b_imprimir/clicked': self.imprimir, 
                       'b_carta/clicked': self.imprimir_carta_compromiso, 
                       'b_pedido/clicked': self.hacer_y_abrir_pedido,  
                       'b_enviar/clicked': self.enviar_por_correo, 
                       "cbe_cliente/changed": self.cambiar_datos_cliente, 
                       "b_add/clicked": self.add_ldp, 
                       "b_drop/clicked": self.drop_ldp, 
                       "ch_validado/toggled": self.validar, 
                       "tv_contenido/query-tooltip": self.tooltip_query, 
                       'ch_adjudicada/toggled': self.adjudicar,
                       'b_credito/clicked': self.enviar_solicitud_credito, 
                       "b_atras/clicked": self.atras, 
                       "b_adelante/clicked": self.adelante, 
                       'ev_iconostado/button-release-event': self.mostrar_ttip,
                       "ch_denegado/toggled": self.actualizar_editable_motivo, 
                       "ch_cred_vb_admon/clicked": self.conceder_credito, 
                       "e_cred_entidad/changed": self.actualizar_dc, 
                       "e_cred_oficina/changed": self.actualizar_dc, 
                       "e_cred_numcuenta/changed": self.actualizar_dc
                      }  
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero_de_los_mios() 
        else:
            self.ir_a(objeto)
        #if self.usuario and self.usuario.nivel >= 4:
        #    self.activar_widgets(False) # Para evitar manos rápidas al abrir.
        gtk.main()

    def actualizar_dc(self, entry_llamante):
        ent = self.wids['e_cred_entidad'].get_text()
        ofi = self.wids['e_cred_oficina'].get_text()
        cue = self.wids['e_cred_numcuenta'].get_text()
        try:
            dc = utils.calcCC(ent, ofi, cue)
        except (TypeError, ValueError):
            dc = None
        if dc:
            self.objeto.credDigitocontrol = dc
            self.objeto.syncUpdate()
            self.objeto.make_swap("credDigitocontrol")
        self.wids["e_cred_digitocontrol"].set_text(
                self.objeto.credDigitocontrol)

    def actualizar_manualmente_lista_presupuestos(self, boton_o_tv):
        self.rellenar_lista_presupuestos()

    def actualizar_editable_motivo(self, ch):
        self.wids['e_motivo'].set_sensitive(ch.get_active())
        try:
            b_pedido_activado = self.wids['b_pedido'].get_sensitive()
        except AttributeError:
            b_pedido_activado = self.wids['b_pedido'].get_property("sensitive")
        self.wids['b_pedido'].set_sensitive(
                b_pedido_activado and not ch.get_active() 
                # CWT: Si ya se le ha hecho al menos 1 pedido, no permitir más
                and not (self.objeto and self.objeto.get_pedidos()))

    def mostrar_ttip(self, widget, event):
        texto_tooltip = self.wids['iconostado'].get_tooltip_text()
        if not texto_tooltip:
            try:
                texto_tooltip = self.objeto.get_str_estado()
            except AttributeError:
                texto_tooltip = None
        if texto_tooltip:
            utils.dialogo_info(titulo = "ESTADO DE LA OFERTA", 
                    texto = texto_tooltip, 
                    padre = self.wids['ventana'])

    def atras(self, boton):
        if self.objeto:
            presupuestos_anteriores = self.buscar_presupuestos_accesibles(
                    mas_criterios_de_busqueda = 
                        pclases.Presupuesto.q.id < self.objeto.id)
            try:
                anterior = presupuestos_anteriores[0]
                self.reset_cache_credito()
                self.ir_a(anterior)
            except IndexError:
                boton.set_sensitive(False)

    def adelante(self, boton):
        if self.objeto:
            try:
                presupuestos_siguientes = self.buscar_presupuestos_accesibles(
                    mas_criterios_de_busqueda = 
                        pclases.Presupuesto.q.id > self.objeto.id)
                siguiente = presupuestos_siguientes[-1]
                self.reset_cache_credito()
                self.ir_a(siguiente)
            except IndexError:
                boton.set_sensitive(False)

    def hacer_y_abrir_pedido(self, boton):
        pedido = hacer_pedido(self.objeto, self.usuario, self.wids['ventana'])
        # [18/02/2014] Nueva alerta: Si el cliente en ese momento no tiene 
        # crédito, crear el pedido pero invalidado. Y además enviar un correo 
        # a comerciales, validadores, epalomo y rparra advirtiéndoles.
        if pedido:
            self.actualizar_ventana()
            importe_pedido = self.objeto.calcular_importe_total(iva = True)
            credito = self.objeto.cliente.calcular_credito_disponible()
            if credito - importe_pedido <= 0:
                utils.dialogo_info(titulo = "CLIENTE SIN CRÉDITO", 
                        texto = "El cliente no tiene crédito suficiente para"
                                " atender al pedido completo.\n"
                                "Crédito: %s\n"
                                "Importe pedido: %s\n"
                                "El pedido %s se invalidará." % (
                                    utils.float2str(credito), 
                                    utils.float2str(importe_pedido), 
                                    pedido.numpedido), 
                        padre = self.wids['ventana'])
                pedido.validado = False
                pedido.usuario = None
                self.enviar_correo_de_riesgo(pedido)
            abrir_pedido(pedido, self.usuario)

    def detectar_cambio_pagina_notebook(self, nb, page, page_num):
        if page_num == 1:
            if not self.usuario or self.usuario.nivel > 0:
                nb.set_current_page(0)
                utils.dialogo_info(titulo = "NECESITA PERMISOS ADICIONALES", 
                        texto = "Solo los administradores pueden ver esta "
                                "información.", 
                        padre = self.wids['ventana'])
            else:
                self.rellenar_tablas_historial()

    def enviar_solicitud_credito(self, boton):
        if self.wids['b_guardar'].get_property("sensitive"):
            self.guardar(None)  # Por si acaso, primero guardo
        # Comprobación de campos obligatorios:
        falta_alguno = False
        if (self.objeto.credApertura == self.objeto.credAumento == 
                self.objeto.credSolicitud == False):
            falta_alguno = True
            color = gtk.gdk.color_parse("Red")
        else:
            color = None
        self.wids["ch_cred_apertura"].modify_base(gtk.STATE_NORMAL, color)
        self.wids["ch_cred_aumento"].modify_base(gtk.STATE_NORMAL, color)
        self.wids["ch_cred_solicitud"].modify_base(gtk.STATE_NORMAL, color)
        for obligatorio, wid in (("credFecha", "e_cred_fecha"), 
                                 ("comercial", "e_cred_comercial"), 
                                 ("cif", "e_cred_cif"), 
                                 ("nombrecliente", "e_cred_nombre"), 
                                 ("credUte", "e_cred_ute"), 
                                 ("nombreobra", "e_cred_obra"), 
                                 ("credLicitador", "e_cred_licitador"), 
                                 ("credDirfiscal", "e_cred_dirfiscal"), 
                                 ("credCpfiscal", "e_cred_cpfiscal"), 
                                 ("credPoblacionfiscal", 
                                   "e_cred_poblacionfiscal"), 
                                 ("credProvinciafiscal", 
                                    "e_cred_provinciafiscal"), 
                                 ("credTelefonofiscal", 
                                    "e_cred_telefonofiscal"), 
                                 ("credFaxfiscal", "e_cred_faxfiscal"), 
                                 ("credMovilfiscal", "e_cred_movilfiscal"), 
                                 ("credContactofiscal", 
                                    "e_cred_contactofiscal"), 
                                 ("credFdp", "e_cred_fdp"), 
                                 ("credEntidades", "txt_cred_entidades"), 
                                 ("credDiapago1", "e_cred_diapago1"), 
                                 ("credCredsolicitado", 
                                     "e_cred_credsolicitado")):
            valor = getattr(self.objeto, obligatorio)
            if valor is None or (isinstance(valor, str) 
                                 and valor.strip() == ""):
                falta_alguno = True
                color = gtk.gdk.color_parse("Red")
            else:
                color = None
            self.wids[wid].modify_base(gtk.STATE_NORMAL, color)
        if falta_alguno:
            utils.dialogo_info(titulo = "CAMPOS REQUERIDOS", 
                texto = "Debe completar los campos obligatorios"
                        " marcados en rojo.", 
                padre = self.wids['ventana'])
            return 
        self.objeto.notificador.desactivar()
        self.objeto.credVecesSolicitado += 1
        try:
            nombrecomercial = self.usuario.nombre
        except AttributeError:
            try:
                nombrecomercial = self.objeto.comercial.get_nombre_completo()
            except AttributeError:
                self.objeto.credVbNombrecomercial = ""
        self.objeto.credVbNombrecomercial = nombrecomercial 
        self.objeto.syncUpdate()
        self.objeto.make_swap("credVecesSolicitado")
        self.objeto.make_swap("credVbNombrecomercial")
        self.objeto.notificador.activar(self.aviso_actualizacion)
        fich_sol_ods = self.rellenar_plantilla_credito()
        envio_ok = self.enviar_correo_solicitud_credito(
                                            nomfich_solicitud = fich_sol_ods)
        if not envio_ok:
            utils.dialogo_info(titulo = "ERROR AL ENVIAR SOLICITUD", 
                    texto = "Ocurrió un error al enviar la notificación \n"
                            "por correo electrónico.", 
                    padre = self.wids['ventana'])
        self.actualizar_ventana()

    def rellenar_tablas_historial(self):
        model = self.wids['tv_ofertado'].get_model()
        model.clear()
        if self.objeto:
            ofertado = self.objeto.get_ofertado_por_producto()
            pedido = self.objeto.get_pedido_por_producto()
            servido = self.objeto.get_servido_por_producto()
            facturado = self.objeto.get_facturado_por_producto()
            pendiente = self.objeto.get_pendiente_pasar_a_pedido()
            for p in ofertado:
                fila = build_fila_historial(ofertado, pedido, servido, 
                                            facturado, pendiente, p)
                model.append((fila))
            # Si ha quedado algo pedido pero no ofertado, o servido no 
            # ofertado, etc. ahora es el momento de mostrarlo:
            for dic in (pedido, servido, facturado, pendiente):
                for p in dic.keys()[:]:
                    fila = build_fila_historial(ofertado, pedido, servido, 
                                                facturado, pendiente, p)

    def cerrar_presupuesto(self, ch_button):
        """
        Marca el presupuesto como cerrado guardando antes los posibles cambios.
        Permite que se envíen los correos de validación.
        """
        if pclases.DEBUG:
            print "Soy cerrar presupuesto... BEGIN"
        cerrar = ch_button.get_active()
        if self.objeto.cerrado == cerrar: #Actualizando. No ha sido el usuario.
            pass
        else:
            self.objeto.cerrado = cerrar 
            self.objeto.syncUpdate()
            # En lugar de guardar con todo lo que conlleva, guardo solo este campo
            self.objeto.swap['cerrado'] = self.objeto.cerrado
            #self.guardar(None)
            #self.actualizar_ventana()  # En guardar ya actualiza ventana.
            # self.rellenar_lista_presupuestos()
        if pclases.DEBUG:
            print "Soy cerrar presupuesto... END"

    def enviar_correo_solicitud_credito(self, nomfich_solicitud = None):
        """
        Envía un correo de solicitud de crédito al usuario correspondiente.
        """
        vpro = VentanaActividad(self.wids['ventana'], 
                "Enviando solicitud por correo electrónico.")
        vpro.mostrar()
        vpro.mover()
        ok = False
        if self.usuario and self.objeto:
            vpro.mover()
            servidor = self.usuario.smtpserver
            smtpuser = self.usuario.smtpuser
            smtppass = self.usuario.smtppassword
            rte = self.usuario.email
            vpro.mover()
            # TODO: OJO: HARDCODED
            if self.usuario and self.usuario.id == 1:
                dests = ["informatica@geotexan.com"]
            else:
                dests = ["epalomo@geotexan.com", "jpedrero@geotexan.com"]
            vpro.mover()
            # Correo de riesgo de cliente
            texto = "%s ha solicitado crédito para el cliente %s "\
                    "a través de la oferta %d. Se adjunta copia del "\
                    "formulario." % (
                        self.usuario and self.usuario.nombre or "Se", 
                        self.objeto.cliente and self.objeto.cliente.nombre 
                            or self.objeto.nombrecliente, 
                        self.objeto.id)
            if nomfich_solicitud: 
                texto += "\n\n\nSi no puede ver el adjunto en el estándar"\
                    " OpenDocument use el siguiente complemento: "\
                    "http://downloads.sourceforge.net/odf-converter/"\
                    "OdfAddInForOfficeSetup-en.3.0.5254.exe?"\
                    "use_mirror=nchc" 
                fich_sol_html = convertir_a_html(nomfich_solicitud)
                fich_sol_xls = crear_xls(self.objeto, self.wids)
                adjunto = [nomfich_solicitud, fich_sol_html, fich_sol_xls]
            else: 
                adjunto = []
            vpro.mover()
            ok = utils.enviar_correoe(rte, 
                                      dests,
                                      "Solicitud de crédito %s" % (
                                        self.wids['e_cred_nombre'].get_text()),
                                      texto, 
                                      adjuntos = adjunto, 
                                      servidor = servidor, 
                                      usuario = smtpuser, 
                                      password = smtppass)
            vpro.mover()
        vpro.ocultar()
        return ok
    
    def enviar_correo_de_riesgo(self, pedido):
        """
        Si el cliente está en riesgo, aviso por correo para que se vaya 
        preparando el personal de CRM.
        """
        # CWT: Deshabilitado. Se sustituye solo por el envío voluntario de 
        # solicitud de crédito por parte del usuario. Ahora lo uso para 
        # enviar el correo de nuevo pedido a cliente sin crédito.
        if self.usuario and self.objeto.cliente:
            importe_presupuesto = self.objeto.calcular_importe_total(
                                    iva = True)
            # Correo de riesgo de cliente
            texto = "Se ha creado el pedido %s de la oferta %d "\
                    "para el cliente %s, que está en riesgo por falta "\
                    "de crédito para el suministro completo.\n"\
                    "Importe del presupuesto: %s.\n"\
                    "El pedido se ha marcado como pendiente de validación." % (
                        pedido.numpedido, 
                        self.objeto.id, 
                        self.objeto.nombrecliente, 
                        utils.float2str(importe_presupuesto))
            # TODO: Y que no se haya enviado ya antes. Si no, no veas 
            # la paliza de correos que van a llegar cada vez que guarde 
            # un valor de la ventana.
            servidor = self.usuario.smtpserver
            smtpuser = self.usuario.smtpuser
            smtppass = self.usuario.smtppassword
            rte = self.usuario.email
            # TODO: OJO: HARDCODED
            dests = ["epalomo@geotexan.com"] 
            dests += [d for d in self.select_correo_validador()]
            comerciales = [self.objeto.comercial]
            dests += [comercial.correoe for comercial in comerciales 
                      if comercial.empleado.usuario.usuario != self.usuario]
            if self.usuario and self.usuario.id == 1:
                texto += "\n\n\nEl correo iba dirigido a: %s" % (
                        "; ".join(dests))
                dests = ["informatica@geotexan.com"]
            enviar_correoe(rte, 
                           dests,
                           "Alerta de pedido sin crédito", 
                           texto, 
                           servidor = servidor, 
                           usuario = smtpuser, 
                           password = smtppass)

    def enviar_correo_observaciones(self):
        """
        Al modificar las notas internas, se envía un correo electrónico 
        al comercial con el texto "Oferta [no] validada. Se agregaron 
        anotaciones internas..."
        """
        if self.usuario:
            # Correo de riesgo de cliente
            anotaciones_formateadas = "\n> "
            anotaciones_formateadas += "\n> ".join(
                    utils.wrap(self.objeto.observaciones,
                    76).splitlines())
            texto = "Oferta %d %svalidada.\n"\
                    "Se agregaron anotaciones internas:\n\n"\
                    "%s" % (
                        self.objeto.id, 
                        self.objeto.validado and "" or "no ", 
                        anotaciones_formateadas)
            servidor = self.usuario.smtpserver
            smtpuser = self.usuario.smtpuser
            smtppass = self.usuario.smtppassword
            rte = self.usuario.email
            dests = [d for d in self.select_correo_validador()]
            comerciales = [self.objeto.comercial]
            dests += [comercial.correoe for comercial in comerciales 
                      if comercial.empleado.usuario.usuario != self.usuario]
            if self.usuario and self.usuario.id == 1:
                texto += "\n\n\nEl correo iba dirigido a: %s" % (
                        "; ".join(dests))
                dests = ["informatica@geotexan.com"]
            enviar_correoe(rte, 
                           dests,
                           "Nuevas anotaciones en oferta %d" % self.objeto.id, 
                           texto, 
                           servidor = servidor, 
                           usuario = smtpuser, 
                           password = smtppass)

    def adjudicar(self, ch):
        if ch.get_active() != self.objeto.adjudicada:   # Es el usuario el 
                                                        # que ha hecho clic.
            if ch.get_active():     # Lo está intentando poner a True
                if utils.dialogo(titulo = "¿ADJUDICAR OFERTA?", 
                    texto = "Si considera la oferta como adjudicada se\n"
                            "iniciará la parte del proceso de paso a \n"
                            "pedido que permitan las condiciones de \n"
                            "validación.\n\n"
                            "¿Continuar?", 
                    padre = self.wids['ventana']):
                    self.objeto.adjudicada = True
                    self.objeto.syncUpdate()
                    self.objeto.make_swap()
                    self.enviar_correo_adjudicada(ch)
                    if (not self.objeto.cliente 
                            or self.comprobar_riesgo_cliente() <= 0):
                        utils.dialogo_info(titulo = "SOLICITE CRÉDITO", 
                            texto = "El cliente es nuevo o no tiene crédito "
                                    "disponible.\n\nSolicite una ampliación o "
                                    "apertura.", 
                            padre = self.wids['ventana'])
                        self.wids['nb'].set_current_page(2)
                else:
                    self.objeto.adjudicada = False
                    self.objeto.syncUpdate()
                    self.objeto.make_swap()
                    ch.set_active(False)
            else:
                self.objeto.adjudicada = False
                self.objeto.syncUpdate()
                self.objeto.make_swap()

    def enviar_correo_adjudicada(self, ch):
        # CWT: Deshabilitado. Se sustituye solo por el correo de solicitud 
        # de crédito.
        return
        servidor = self.usuario.smtpserver
        smtpuser = self.usuario.smtpuser
        smtppass = self.usuario.smtppassword
        rte = self.usuario.email
        # TODO: OJO: HARDCODED
        if self.usuario and self.usuario.id == 1:
            dests = ["informatica@geotexan.com"]
        else:
            dests = ["epalomo@geotexan.com"]
        #dests = ["informatica@geotexan.com"]
        if not self.objeto.cliente:
            # Correo de alta del cliente
            texto = "Se ha adjudicado la oferta %d. "\
                "Se debe de dar de alta al cliente:\n"\
                "\tNombre: %s\n"\
                "\tCIF: %s\n"\
                "\tDireccion: %s\n"\
                "\tCódigo postal: %s\n"\
                "\tCiudad: %s\n"\
                "\tProvincia: %s\n"\
                "\tPaís: %s\n"\
                "\tTeléfono: %s\n"\
                "\tCorreo electrónico: %s\n"\
                "\tPersona de contacto: %s" % (
                        self.objeto.id, 
                        self.objeto.nombrecliente, 
                        self.objeto.cif, 
                        self.objeto.direccion, 
                        self.objeto.cp, 
                        self.objeto.ciudad, 
                        self.objeto.provincia, 
                        self.objeto.pais, 
                        self.objeto.telefono, 
                        self.objeto.email, 
                        self.objeto.personaContacto)
            enviar_correoe(rte, 
                           dests,
                           "Alta de nuevo cliente", 
                           texto, 
                           servidor = servidor, 
                           usuario = smtpuser, 
                           password = smtppass)
        if not self.objeto.obra:
            # Correo de alta de la obra
            texto = "Se ha adjudicado la oferta %d. "\
                "Se debe de dar de alta la obra %s "\
                "en el cliente %s con los siguientes datos:\n"\
                "\tDireccion: %s\n"\
                "\tCódigo postal: %s\n"\
                "\tCiudad: %s\n"\
                "\tProvincia: %s\n"\
                "\tPaís: %s\n" % (
                        self.objeto.id, 
                        self.objeto.nombreobra, 
                        self.objeto.nombrecliente, 
                        self.objeto.direccion, 
                        self.objeto.cp, 
                        self.objeto.ciudad, 
                        self.objeto.provincia, 
                        self.objeto.pais, 
                        )
            enviar_correoe(rte, 
                           dests,
                           "Alta de nueva obra", 
                           texto, 
                           servidor = servidor, 
                           usuario = smtpuser, 
                           password = smtppass)
        # Correo de adjudicación de oferta.
        texto = "Se ha adjudicado la oferta %d del comercial %s"\
                " al cliente %s por importe de %s €." % (
                    self.objeto.id, 
                    self.objeto.comercial 
                    and self.objeto.comercial.get_nombre_completo()
                     or "¡NADIE!", 
                    self.objeto.nombrecliente, 
                    utils.float2str(
                        self.objeto.calcular_importe_total()))
        enviar_correoe(rte, 
                       dests,
                       "Alta de nueva adjudicación de oferta", 
                       texto, 
                       servidor = servidor, 
                       usuario = smtpuser, 
                       password = smtppass)

    def bloquear(self, ch):
        """
        Bloquea el presupuesto impidiendo modificaciones excepto para los 
        usuarios con nivel suficiente.
        """
        puede_bloquear = (self.usuario 
                                and self.usuario.nivel <= NIVEL_VALIDACION)
        if self.objeto.bloqueado == ch.get_active():
            pass
        else:
            self.objeto.notificador.desactivar()
            if puede_bloquear:  # Y desbloquear, claro.
                self.objeto.bloqueado = ch.get_active()
                self.objeto.make_swap("bloqueado")
                pclases.Auditoria.modificado(self.objeto, 
                    self.usuario, __file__, 
                    "Usuario %s (des)bloqueó presupuesto %d." 
                        % (self.usuario and self.usuario.usuario or "¡NADIE!", 
                           self.objeto.id))
                ch.set_active(self.objeto.bloqueado)
                self.guardar(None)  # Por si hay algo pendiente.
                # Y que se vea realmente con qué valores ha bloqueado.
                self.actualizar_ventana()
            else:
                ch.set_active(self.objeto.bloqueado)
            self.objeto.notificador.activar(self.aviso_actualizacion)

    def validar(self, ch):
        """
        Si está validado:
            - Deja el presupuesto como indica el check. Sea quien sea. Si 
              estamos rellenando los widgets, ch estará marcado o desmarcado en
              función del valor de la oferta. Si le ha dado el usuario, el ch 
              tiene el nuevo valor de validación (opuesto en este instante a 
              lo que guarda self.objeto.validado).
        Si no está validado: 
            - Si el usuario tiene nivel: valida y guarda el usuario.
            - Si el usuario no tiene nivel: no valida y muestra aviso.
        """
        if self.objeto.validado == ch.get_active():     # Estoy rellenando. No 
            # hay edición del usuario. No compruebo nada.
            pass    # OJO porque aquí puede haber BUG. ¿Qué pasa si estoy 
                    # moviéndome de un objeto ya validado a otro no  
                    # validado? Entraría por la otra rama del if confundiendo 
                    # una posible validación del usuario con una simple 
                    # actialización del widget en la ventana.
        else:   # El usuario está desvalidando o intentando validar.
            self.objeto.notificador.desactivar()
            vpro = VentanaActividad(self.wids['ventana'], 
                                    "Comprobando permisos validación...")
            vpro.mostrar()
            vpro.mover()
            tmphndlr = self.handlers_id['ch_validado']['toggled'][-1] # -1? r-u-sure?
            vpro.mover()
            if ((not self.usuario or self.usuario.nivel > NIVEL_VALIDACION)
                    and ch.get_active() # = estoy intentando validar
                    and not self.objeto.validable):     # Pero no puedo
                vpro.mover()
                ch.disconnect(tmphndlr)
                ch.set_active(False)
                self.objeto.validado = False
                self.objeto.swap['usuarioID'] = None
                self.objeto.swap['fechaValidacion'] = None
                vpro.mover()
                self.objeto.syncUpdate()
                pclases.Auditoria.modificado(self.objeto, 
                    self.usuario, __file__, 
                    "Se impide intento de validación en presupuesto %d por %s." 
                        % (self.objeto.id, 
                           self.usuario and self.usuario.usuario or "¡NADIE!"))
                vpro.mover()
                vpro.ocultar()
                utils.dialogo_info("PERMISOS INSUFICIENTES", 
                        texto = "No posee privilegios suficientes para validar "
                                "la oferta con las condiciones actuales.", 
                        padre = self.wids['ventana'])
            else:   # Estoy "desvalidando", tengo permisos o es validable.
                vpro.mover()
                ch.disconnect(tmphndlr)
                vpro.mover()
                if ch.get_active():     # Estoy validando
                    if self.usuario:
                        self.objeto.validado = self.usuario
                        self.objeto.swap['usuarioID'] = self.objeto.usuario
                        fv = self.objeto.fechaValidacion
                        if fv:
                            fv_aprox = datetime.datetime(fv.year, fv.month, 
                                    fv.day, fv.hour, fv.minute, fv.second)
                        else:
                            fv_aprox = None
                        self.objeto.swap['fechaValidacion'] = fv_aprox
                        pclases.Auditoria.modificado(self.objeto, 
                            self.usuario, __file__, 
                            "Presupuesto %d validado por %s." 
                                % (self.objeto.id, 
                                   self.objeto.usuario.usuario))
                        self.enviar_correo_notificacion_validado()
                else:   # Estoy invalidando
                    self.objeto.validado = False
                    self.objeto.adjudicada = False
                    self.wids['ch_adjudicada'].set_active(
                            self.objeto.adjudicada)
                    self.objeto.swap['usuarioID'] = None
                    self.objeto.swap['adjudicada'] = None
                    self.objeto.swap['fechaValidacion'] = None
                    pclases.Auditoria.modificado(self.objeto, 
                        self.usuario, __file__, 
                        "Presupuesto %d invalidado por %s." 
                            % (self.objeto.id, 
                               self.usuario and self.usuario.usuario 
                               or "¡NADIE!"))
                vpro.mover()
                self.objeto.syncUpdate()
                self.objeto.swap['usuarioID'] = self.objeto.usuarioID
                fv = self.objeto.fechaValidacion
                if fv:
                    fv_aprox = datetime.datetime(fv.year, fv.month, fv.day, 
                                                 fv.hour, fv.minute, fv.second)
                else:
                    fv_aprox = None
                self.objeto.swap['fechaValidacion'] = fv_aprox
                vpro.mover()
                self.refresh_validado()  # Equivale a 
                    # rellenar_widgets pero solo la parte del checkbox.
                vpro.mover()
                vpro.ocultar()
            tmphndlr = ch.connect("toggled", self.validar)
            self.handlers_id['ch_validado']['toggled'].append(tmphndlr)
            self.objeto.notificador.activar(self.aviso_actualizacion)
            self.wids['b_actualizar'].set_sensitive(False) # Falsos positivos.

    def conceder_credito(self, ch):
        """
        Si ya está condedido:
            - Deja el presupuesto como indica el check. Sea quien sea. Si 
              estamos rellenando los widgets, ch estará marcado o desmarcado en
              función del valor de la oferta. Si le ha dado el usuario, el ch 
              tiene el nuevo valor de concesión (opuesto en este instante a 
              lo que guarda self.objeto...).
        Si no está concedido: 
            - Si el usuario tiene nivel: concede y guarda el usuario.
            - Si el usuario no tiene nivel: no concede y muestra aviso.
        """
        if (self.objeto.credUsuario != None) == ch.get_active():     # Estoy rellenando. No 
            # hay edición del usuario. No compruebo nada.
            pass    # OJO porque aquí puede haber BUG. ¿Qué pasa si estoy 
                    # moviéndome de un objeto ya concedido a otro no  
                    # concedido? Entraría por la otra rama del if confundiendo 
                    # una posible concesión del usuario con una simple 
                    # actialización del widget en la ventana.
        else:   # El usuario está cancilando o intentando conceder.
            self.objeto.notificador.desactivar()
            vpro = VentanaActividad(self.wids['ventana'], 
                                    "Comprobando permisos...")
            vpro.mostrar()
            vpro.mover()
            tmphndlr = self.handlers_id['ch_cred_vb_admon']['clicked'][-1] # -1? r-u-sure?
            vpro.mover()
            if ((not self.usuario or self.usuario.nivel > NIVEL_VALIDACION)
                    and ch.get_active() # = estoy intentando conceder
                    ): 
                vpro.mover()
                ch.disconnect(tmphndlr)
                ch.set_active(False)
                self.objeto.credVbNombreadmon = "" 
                self.objeto.credUsuario = None
                self.objeto.credFechaconcedido = None
                self.objeto.make_swap("credVbNombreadmon")
                self.objeto.make_swap("credUsuario")
                self.objeto.make_swap('credFechaconcedido')
                vpro.mover()
                self.objeto.syncUpdate()
                pclases.Auditoria.modificado(self.objeto, 
                    self.usuario, __file__, 
                    "Se impide intento de concesión de crédito en presupuesto %d por %s." 
                        % (self.objeto.id, 
                           self.usuario and self.usuario.usuario or "¡NADIE!"))
                vpro.mover()
                vpro.ocultar()
                utils.dialogo_info("PERMISOS INSUFICIENTES", 
                        texto = "No posee privilegios suficientes para "
                                "conceder crédito al cliente.", 
                        padre = self.wids['ventana'])
            else:   # Estoy cancelando o tengo permisos para conceder crédito.
                vpro.mover()
                ch.disconnect(tmphndlr)
                vpro.mover()
                if ch.get_active():     # Estoy concediendo
                    if self.usuario:
                        self.objeto.credVbNombreadmon = self.usuario.nombre
                        self.objeto.credUsuario = self.usuario
                        self.objeto.make_swap("credVbNombreadmon")
                        self.objeto.make_swap("credUsuario")
                        self.objeto.credFechaconcedido = datetime.date.today()
                        self.objeto.make_swap("credFechaconcedido")
                        pclases.Auditoria.modificado(self.objeto, 
                            self.usuario, __file__, 
                            "Concedida solicitud de crédito para el "
                            "presupuesto %d por %s." 
                                % (self.objeto.id, 
                                   self.objeto.credUsuario.usuario))
                        # XXX: PLAN: Todavía no han dicho nada. Pero lo harán:
                        # self.enviar_correo_notificacion_credito_concedido()
                else:   # Estoy cancelando el crédito
                    self.objeto.credVbNombreadmon = ""
                    self.objeto.credUsuario = None
                    self.objeto.credFechaconcedido = None
                    self.objeto.make_swap("credVbNombreadmon")
                    self.objeto.make_swap("credUsuario")
                    self.objeto.make_swap("credFechaconcedido")
                    pclases.Auditoria.modificado(self.objeto, 
                        self.usuario, __file__, 
                        "Crédito %d cancelado por %s." 
                            % (self.objeto.id, 
                               self.usuario and self.usuario.usuario 
                               or "¡NADIE!"))
                vpro.mover()
                self.objeto.syncUpdate()
                self.objeto.make_swap("credVbNombreadmon")
                self.objeto.make_swap("credFechaconcedido")
                vpro.mover()
                self.wids["ch_cred_vb_admon"].set_active(
                        self.objeto.credUsuario != None and 1 or 0)
                self.wids["e_cred_vb_nombreadmon"].set_text(
                        self.objeto.credVbNombreadmon or "")
                self.wids["e_cred_fechaconcedido"].set_text(
                    utils.str_fecha(self.objeto.credFechaconcedido))
                vpro.mover()
                vpro.ocultar()
            tmphndlr = ch.connect("clicked", self.conceder_credito)
            self.handlers_id['ch_cred_vb_admon']['clicked'].append(tmphndlr)
            self.objeto.notificador.activar(self.aviso_actualizacion)
            self.wids['b_actualizar'].set_sensitive(False) # Falsos positivos.

    def fecha(self, w):
        try:
            provisional = utils.parse_fecha(self.wids['e_fecha'].get_text())
        except:
            provisional = self.objeto and self.objeto.fecha or None
        self.wids['e_fecha'].set_text(
                utils.str_fecha(
                    utils.mostrar_calendario(
                        fecha_defecto = provisional, 
                        padre = self.wids['ventana'])))

    def cambiar_datos_cliente(self, cbe):
        """
        Machaca la información de los entries de los datos del cliente 
        del presupuesto si está vacío en campo NIF y se ha seleccionado 
        un cliente del desplegable.
        """
        self.reset_cache_credito()
        idcliente = utils.combo_get_value(cbe)
        if not idcliente:
            self.wids['rating'].set_value(0)
            return
        cliente = pclases.Cliente.get(idcliente)
        #if not self.wids["e_cliente"].get_text():
        #    self.wids["e_cliente"].set_text(cliente.nombre)
        # TODO: Hacer lo mismo con la dirección del formulario de crédito.
        if not self.wids['e_cif'].get_text().strip():
            self.wids['e_cif'].set_text(cliente.cif)
        #if not self.wids["e_direccion"].get_text():
            self.wids["e_direccion"].set_text(cliente.direccion)
        #if not self.wids["e_ciudad"].get_text():
            self.wids["e_ciudad"].set_text(cliente.ciudad)
        #if not self.wids["e_provincia"].get_text():
            self.wids["e_provincia"].set_text(cliente.provincia)
        #if not self.wids["e_cp"].get_text():
            self.wids["e_cp"].set_text(cliente.cp)
        #if not self.wids["e_pais"].get_text():
            self.wids["e_pais"].set_text(cliente.pais)
        #if not self.wids["e_telefono"].get_text():
            self.wids["e_telefono"].set_text(cliente.telefono)
        #if not self.wids["e_fax"].get_text():
        #    self.wids["e_fax"].set_text(cliente.fax)
        if not self.wids['e_persona_contacto'].get_text().strip():
            self.wids['e_persona_contacto'].set_text(cliente.contacto)
        self.actualizar_obras_cliente()
        self.wids['rating'].set_value(cliente.calcular_rating())

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
                if producto.camposEspecificosEspecial.unidad:
                    txt = """Introduzca la cantidad en %s:""" % (producto.camposEspecificosEspecial.unidad)
                else:
                    txt = """Introduzca la cantidad:"""
            else:
                txterror = """presupuestos::seleccionar_cantidad -> ERROR: El producto de venta ID %d no es bala ni rollo. Verificar.""" % (producto.id)
                if pclases.DEBUG:
                    print txterror
                self.logger.error(txterror)
                txt = """Introduzca la cantidad:"""
        elif isinstance(producto, pclases.ProductoCompra):
            txt = "Introduzca la cantidad en %s." % (producto.unidad)
        else:
            txterror = "presupuestos::seleccionar_cantidad -> ERROR: Producto %s no es producto de compra ni de venta." % (producto)
            self.logger.error(txterror)
        cantidad = utils.dialogo_entrada(titulo = 'CANTIDAD', texto = txt, padre = self.wids['ventana'])
        try:
            cantidad = utils._float(cantidad)
            return cantidad
        except:
            utils.dialogo_info(titulo = 'ERROR', texto = 'La cantidad introducida no es correcta.', padre = self.wids['ventana'])
            return None
    
    def add_ldp(self, boton):
        """
        Añade una línea de presupuesto a la oferta.
        """
        self.reset_cache_credito()
        #productos = utils.buscar_producto_general(self.wids['ventana'])
        #for producto in productos:
        #    try:
        #        tarifa = self.objeto.cliente.tarifa
        #        precio = tarifa.obtener_precio(producto)
        #    except:
        #        precio = producto.preciopordefecto
        #    if precio == 0:
        #        precio = preguntar_precio(producto, self.wids['ventana'])
        #    cantidad = self.seleccionar_cantidad(producto)
        #    if cantidad == None:
        #        break
        #    if isinstance(producto, pclases.ProductoCompra):
        #        ldp = pclases.LineaDePresupuesto(
        #                                    productoVenta = None, 
        #                                    productoCompra = producto, 
        #                                    cantidad = cantidad, 
        #                                    precio = precio, 
        #                                    presupuesto = self.objeto)
        #    elif isinstance(producto, pclases.ProductoVenta):
        #        ldp = pclases.LineaDePresupuesto(
        #                                    productoVenta = producto, 
        #                                    productoCompra = None, 
        #                                    cantidad = cantidad, 
        #                                    precio = precio, 
        #                                    presupuesto = self.objeto)
        ldp = pclases.LineaDePresupuesto(productoVenta = None, 
                                         productoCompra = None, 
                                         cantidad = 0, 
                                         precio = 0,
                                         presupuesto = self.objeto)
        pclases.Auditoria.nuevo(ldp, self.usuario, __file__)
        self.rellenar_tablas()
        model = self.wids['tv_contenido'].get_model()
        itr = model.get_iter_first()
        while itr:
            if model[itr][-1] == ldp.puid:
                path = self.wids['tv_contenido'].get_model().get_path(itr)
                break
            itr = model.iter_next(itr)
        col = self.wids['tv_contenido'].get_column(1)
        self.wids['tv_contenido'].grab_focus()
        self.wids['tv_contenido'].set_cursor(path, col, True)
    
    def drop_ldp(self, boton):
        """
        Elimina las LDPs seleccionadas del presupuesto.
        """
        self.reset_cache_credito()
        sel = self.wids['tv_contenido'].get_selection()
        model, paths = sel.get_selected_rows()
        if utils.dialogo(titulo = "ELIMINAR LÍNEAS DE PRESUPUESTO", 
                texto = "Se van a eliminar %d líneas de presupuesto.\n"
                        "¿Está seguro?" % len(paths), 
                padre = self.wids['ventana']):
            fallos = []
            if  paths != None and paths != []:
                for path in paths:
                    ldp = pclases.getObjetoPUID(model[path][-1])
                    try:
                        puid = ldp.puid
                        ldp.destroy(ventana = __file__)
                    except Exception, msg:
                        fallos.append((puid, msg))
                        if pclases.DEBUG:
                            print "presupuestos.py::drop_ldp -> "\
                                  "No se pudo eliminar la línea de "\
                                  "presupuesto. Mensaje de la excepción:", msg
                self.rellenar_tablas()
                if fallos:
                    for fallo, msg in fallos:
                        self.logger.error("presupuestos::drop_ldp -> "
                                "%s no se pudo eliminar. Excepción: %s." % (
                                    fallo, msg))
                    utils.dialogo_info(titulo = "ERROR", 
                        texto = "%d líneas no se pudieron eliminar." 
                                                                % len(fallo),
                        padre = self.wids['ventana']) 
        
    def imprimir(self, boton):
        """
        Genera y abre el PDF de la carta de oferta.
        """
        #if self.objeto != None:
        #    from informes import geninformes
        #    from formularios.reports import abrir_pdf
        #    abrir_pdf(geninformes.generar_pdf_presupuesto(self.objeto))
        try:
            self.objeto.impresiones += 1
            self.objeto.make_swap('impresiones')
        except AttributeError:
            pass
        else:
            pclases.Auditoria.modificado(self.objeto, self.usuario, __file__, 
                    "Lanzada impresión n.º %d" % self.objeto.impresiones)
        self.imprimir_presupuesto(boton)

    def imprimir_presupuesto(self, boton):
        """
        Imprime el presupuesto en formato "factura" en lugar de carta.
        """
        if self.objeto != None:
            pdf_presupuesto = generar_pdf_presupuesto(self.objeto)
            from formularios.reports import abrir_pdf
            abrir_pdf(pdf_presupuesto)  # @UndefinedVariable

    def imprimir_carta_compromiso(self, boton):
        from formularios.reports import abrir_pdf
        from informes import carta_compromiso
        abrir_pdf(carta_compromiso.go_from_presupuesto(self.objeto))  # @UndefinedVariable

    def enviar_por_correo(self, boton):
        """
        Envía por correo el PDF del presupuesto desde la cuenta del 
        comerial o de la genérica "pedidos@...".
        """
        try:
            self.objeto.envios += 1
            self.objeto.make_swap('envios')
        except AttributeError:
            pass
        else:
            pclases.Auditoria.modificado(self.objeto, self.usuario, __file__, 
                    "Lanzado envío n.º %d" % self.objeto.envios)
        pdf_presupuesto = generar_pdf_presupuesto(self.objeto)
        from formularios import mail_sender
        ventana_correo = mail_sender.MailSender()
        try:
            ventana_correo.set_from(self.usuario.email)
            ventana_correo.set_to(self.objeto.email)
            if not self.usuario or self.usuario.id == 1:
                # Safety check. No sea que haciendo pruebas se me vaya un 
                # correo a quien no debe.
                ventana_correo.set_to("informatica@geotexan.com")
            # PLAN: Nada de HTML de momento...
            #texto_correo = "<html><head></head><body>"
            #texto_correo += "<p>Se le adjunta oferta solicitada.</p> <br><br>"
            #texto_correo += self.objeto.comercial.get_firma_html()
            #texto_correo += "</body></html>"
            texto_correo = "Se le adjunta oferta solicitada.\n\n\n"
            texto_correo += self.objeto.comercial.get_firma()
            ventana_correo.set_asunto("Geotexan: Oferta %d" % self.objeto.id)
            ventana_correo.set_adjunto(pdf_presupuesto)
            ventana_correo.set_smtpconf(self.usuario.smtpserver, 
                                        465,    # TODO: OJO: HARCODED!
                                        self.usuario.smtpuser, 
                                        self.usuario.smtppassword)
        except AttributeError:
            utils.dialogo_info(titulo = "CONFIGURACIÓN INCORRECTA", 
                    texto = "Existe un problema con su configuración"
                            " de correo electrónico.\nConsulte al "
                            "administrador de la aplicación o complete"
                            " la información en sus datos de usuario.", 
                    padre = self.wids['ventana'])
        else:
            ventana_correo.set_copia(True)
            ventana_correo.set_texto(texto_correo)
            enviado = ventana_correo.run()
            ventana_correo.cerrar()
            if not enviado:
                try:
                    ventana_padre = self.wids['ventana']
                except KeyError:
                    # Ya ventana ya no está disponible. Pero muestro el error 
                    # igualmente.
                    ventana_padre = None
                utils.dialogo_info(titulo = "ERROR EN ENVÍO", 
                        texto = "Ocurrió un error al enviar el correo.\n"
                                "Asegúrese de que su antivirus no está "
                                "bloqueando los correos salientes y "
                                "vuelva a intentarlo más tarde.", 
                        padre = ventana_padre)
        #utils.dialogo_info(titulo = "NO IMPLEMENTADO", 
        #        texto = "Característica en desarrollo.", 
        #        padre = self.wids['ventana'])

    def es_diferente(self):
        """
        Devuelve True si algún valor en ventana difiere de 
        los del objeto.
        """
        if self.objeto == None:
            igual = True
        else:
            igual = self.objeto != None
            for colname in self.dic_campos:
                col = self.clase.sqlmeta.columns[colname]
                try:
                    valor_ventana = self.leer_valor(col, 
                                                    self.dic_campos[colname])
                except (ValueError, mx.DateTime.RangeError, TypeError, 
                        AttributeError):
                    igual = False
                valor_objeto = getattr(self.objeto, col.name)
                if colname == "comercialID" and valor_ventana == -1:
                        valor_ventana = None
                if isinstance(col, pclases.SODateCol):
                    try:
                        valor_objeto = utils.abs_mxfecha(valor_objeto)
                    except AttributeError: # Fecha es None
                        valor_objeto = None
                if colname == "clienteID" and valor_ventana == None:
                    valor_ventana = self.wids['cbe_cliente'].child.get_text()
                    valor_objeto = self.objeto.nombrecliente
                if colname == "obraID" and valor_ventana == None:
                    valor_ventana = self.wids['cbe_obra'].child.get_text()
                    valor_objeto = self.objeto.nombreobra
                if not valor_ventana and valor_objeto:
                    igual = False
                elif valor_ventana and not valor_objeto:
                    igual = False
                else:
                    igual = igual and (valor_ventana == valor_objeto)
                if not igual:
                    if pclases.DEBUG and pclases.VERBOSE:
                        print "colname:", colname
                        print "\tvalor_ventana:", valor_ventana
                        print "\tvalor_objeto:", valor_objeto
                    #break
                # DONE: PLAN: ¿Y si en vez de un break, cojo, sigo 
                # sigo analizando y marco en algún color los campos 
                # diferentes?
                if ((not valor_ventana and valor_objeto) 
                        or (valor_ventana and not valor_objeto) 
                        or (valor_ventana != valor_objeto)):
                    color = gtk.gdk.color_parse("Light Blue")
                else:
                    color = self.wids[
                            self.dic_campos[colname]].style.base[
                                gtk.STATE_NORMAL]
                    # Si estaba marcado en rojo por algún motivo (campo 
                    # obligatorio en el crédito, por ejemplo) lo dejo como 
                    # estaba. Si no, lo vuelvo a poner en blanquito.
                    if color != gtk.gdk.color_parse("Red"):
                        color = None
                self.wids[self.dic_campos[colname]].modify_base(
                        gtk.STATE_NORMAL, 
                        color)
        return not igual
    
    def reset_cache_credito(self):
        self.cache_credito = None

    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        self.wids['comboboxentry-entry1'].set_property("can_focus", True)
        self.wids['comboboxentry-entry'].set_property("can_focus", True)
        self.wids['cb_forma_cobro'].set_wrap_width(3)
        # FIXED: Hay un bug con glade-gtk2 que convierte el Entry de los Combo
        # a can_focus=no por lo que nunca se puede llegar a meter nada a mano.
        self.wids['iconostado'].set_from_stock(gtk.STOCK_INFO, 
                                               gtk.ICON_SIZE_DND)
        self.solicitudes_validacion = {}
        self.reset_cache_credito()
        gobject.timeout_add(3 * 60 * 1000, self.reset_cache_credito)
        # Inicialmente no se muestra NADA. Sólo se le deja al
        # usuario la opción de buscar o crear nuevo.
        self.activar_widgets(False)
        self.wids['b_actualizar'].set_sensitive(False)
        self.wids['b_guardar'].set_sensitive(False)
        self.wids['b_nuevo'].set_sensitive(True)
        self.wids['b_buscar'].set_sensitive(True)
        # Inicialización del resto de widgets:
        cols = (('Cantidad', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_cantidad_ldp), 
                ('Descripción', 'gobject.TYPE_STRING', False,True,True, None),
                ('Precio', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_precio_ldp),
                ('Subtotal', 'gobject.TYPE_STRING', False, True, False, None),
                #('Aceptado', 'gobject.TYPE_BOOLEAN', False, True, False, None), 
                #('En pedido', 'gobject.TYPE_STRING', False, True, False, None),
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(self.wids['tv_contenido'], cols)
        for ncol in (0, 2, 3):
            col = self.wids['tv_contenido'].get_column(ncol)
            for cell in col.get_cell_renderers():
                cell.set_property('xalign', 1.0)
        col = self.wids['tv_contenido'].get_column(1)
        col.set_expand(True)
        self.wids['tv_contenido'].get_selection().set_mode(
                                                        gtk.SELECTION_MULTIPLE)
        # Convierto descripción en un entry con autocompletado.
        col.clear()
        liststore_productos = gtk.ListStore(str, str)
        for p in pclases.ProductoVenta.select(
                pclases.ProductoVenta.q.obsoleto == False, 
                orderBy = "descripcion"):
            liststore_productos.append((p.descripcion, p.puid))
        for p in pclases.ProductoCompra.select(
                pclases.ProductoCompra.q.obsoleto == False, 
                orderBy = "descripcion"):
            liststore_productos.append((p.descripcion, p.puid))
        #cellrenderer_combo = gtk.CellRendererCombo()
        #cellrenderer_combo.set_property("editable", True)
        #cellrenderer_combo.set_property("model", liststore_productos)
        #cellrenderer_combo.set_property("text-column", 0)
        #column_combo = col # Ya está instanciado col arriba a la columna que es
        #column_combo.pack_start(cellrenderer_combo, True)
        #column_combo.pack_start(cellrenderer_text, True)
        #column_combo.add_attribute(cellrenderer_combo, "text", 1)
        #cellrenderer_combo.connect("edited", 
        #                           self.update_prod_lpd, 
        #                           liststore_productos, 
        #                           1, 
        #                           self.wids['tv_contenido'].get_model())
        completion = gtk.EntryCompletion()
        completion.set_model(liststore_productos)
        completion.set_text_column(0)
        completion.set_match_func(match_producto, 0)
        cellrenderer_text = CellRendererAutoComplete(completion)
        cellrenderer_text.set_property("editable", True)
        cellrenderer_text.connect("edited", 
                                   self.update_prod_lpd, 
                                   liststore_productos, 
                                   1, 
                                   self.wids['tv_contenido'].get_model())
        col.pack_start(cellrenderer_text, True)
        col.add_attribute(cellrenderer_text, "text", 1)
        cellrenderer_text.set_property("text", 1)
        # Notas en cada línea de presupuesto.
        postomatic.attach_menu_notas(self.wids['tv_contenido'], 
                                     pclases.LineaDePresupuesto, 
                                     self.usuario, 
                                     1)
        self.wids['tv_contenido'].set_tooltip_column(1)
        self.wids['tv_contenido'].connect("query-tooltip", self.tooltip_query)
        self.colorear_contenido(self.wids['tv_contenido'])
        self.build_tv_presupuestos_no_validados()
        cols = (('Usuario', 'gobject.TYPE_STRING', False, True, False, None),
                ('Ventana', 'gobject.TYPE_STRING', False, True, False, None),
                ('«dbpuid»', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Acción', 'gobject.TYPE_STRING', False, True, False, None), 
                ('IP', 'gobject.TYPE_STRING', False, True, False, None), 
                ('«hostname»', 
                    'gobject.TYPE_STRING', False, True, False, None), 
                ('«fechahora»', 'gobject.TYPE_STRING', False, True, True, None),
                ('Descripción', 
                    'gobject.TYPE_STRING', False, True, False, None), 
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(self.wids['tv_auditoria'], cols)
        self.colorear_historial(self.wids['tv_auditoria'])
        self.wids['nb'].connect_after("switch-page", 
                self.detectar_cambio_pagina_notebook)
        cols = (("Producto", "gobject.TYPE_STRING", False, True, True, None), 
                ("Ofertado", "gobject.TYPE_FLOAT", False, False, True, None), 
                ("Pedido", "gobject.TYPE_FLOAT", False, False, True, None), 
                ("Servido", "gobject.TYPE_FLOAT", False, False, True, None), 
                ("Facturado", "gobject.TYPE_FLOAT", False, False, True, None), 
                ("Pendiente", "gobject.TYPE_FLOAT", False, False, True, None), 
                ("PUID", "gobject.TYPE_STRING", False, False, False, None))
        utils.preparar_listview(self.wids["tv_ofertado"], cols)
        from formularios.custom_widgets import starhscale
        self.wids['rating'] = starhscale.StarHScale(max_stars = 5, 
                                                    pixmap_size = 16)
        self.wids['rating'].set_sensitive(False)
        b_ayuda = gtk.Button(stock = gtk.STOCK_HELP)
        def show_hint(boton):
            utils.dialogo_info(titulo = "RATING", 
                    texto = pclases.Cliente.calcular_rating.__doc__, 
                    padre = self.wids['ventana'])
        b_ayuda.connect("clicked", show_hint)
        alignment = self.wids['cbe_cliente'].parent
        vbox = alignment.parent
        hbox = gtk.HBox()
        hbox.set_homogeneous(False)
        alignment.reparent(hbox)
        hbox.pack_start(self.wids['rating'], expand = False)
        hbox.pack_start(b_ayuda, expand = False)
        vbox.add(hbox)
        vbox.show_all()
        if self.usuario and self.usuario.nivel > 1:
            # De momento solo activo para admin y gerencia
            self.wids['rating'].set_property("visible", False)
            b_ayuda.set_property("visible", False)

    def build_tv_presupuestos_no_validados(self):
        cols = (('Presupuesto','gobject.TYPE_STRING',False,True,True,None), 
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(self.wids['tv_presupuestos'], cols)
        self.wids['tv_presupuestos'].set_model(
                # Cerrada, Validada, Número, Cliente, Adjudicada, Pedido, PUID
                gtk.ListStore(str, str, str, str, str, str, str))
        self.wids['tv_presupuestos'].set_tooltip_column(3)
        col = self.wids['tv_presupuestos'].get_column(0)
        celltext = col.get_cell_renderers()[0]
        self.wids['tv_presupuestos'].remove_column(col)
        hbox = gtk.HBox()
        hbox.add(gtk.Label("Pdtes. validación"))
        im_refresh = gtk.Image()
        im_refresh.set_from_stock(gtk.STOCK_REFRESH, gtk.ICON_SIZE_MENU)
        hbox.add(im_refresh)
        hbox.set_tooltip_text("Pulse para actualizar la lista.")
        hbox.set_spacing(3)
        hbox.show_all()
        col = gtk.TreeViewColumn()
        col.set_widget(hbox)
        col.set_clickable(True)
        col.connect("clicked", self.actualizar_manualmente_lista_presupuestos)
        self.wids['tv_presupuestos'].insert_column(col, 0)
        cellpb = gtk.CellRendererPixbuf()
        cellpb2 = gtk.CellRendererPixbuf()
        cellpb3 = gtk.CellRendererPixbuf()
        cellpb4 = gtk.CellRendererPixbuf()
        col.pack_start(cellpb, False)
        col.pack_start(cellpb2, False)
        col.pack_start(celltext, False)
        col.pack_start(cellpb3, True)
        col.pack_start(cellpb4, True)
        col.set_attributes(cellpb, stock_id = 0)
        col.set_attributes(cellpb2, stock_id = 1)
        col.set_attributes(celltext, text = 2)
        col.set_attributes(cellpb3, stock_id = 4)
        col.set_attributes(cellpb4, stock_id = 5)
        self.hndlr_cerrado = self.wids['ch_cerrado'].connect('clicked', 
                self.cerrar_presupuesto)
        self.hndlr_bloqueado = self.wids['ch_bloqueado'].connect('clicked', 
                self.bloquear)
        self.hndlr_presup = self.wids['tv_presupuestos'].connect(
                "cursor-changed", self.cambiar_presupuesto_activo)
        w, h = self.wids['tv_presupuestos'].size_request()
        self.wids['tv_presupuestos'].set_size_request(w, h)
        self.colorear_presupuestos()
        self.rellenar_lista_presupuestos()  # El inicial lo hago yo.

    def colorear_historial(self, tv):
        """
        Asocia una función al treeview para resaltar las acciones.
        """
        def cell_func(column, cell, model, itr, numcol):
            usuario = model[itr][0]
            if usuario == (self.usuario and self.usuario.usuario or ""):
                color_fg = "tomato"
            elif usuario == (self.objeto.comercial 
                    and self.objeto.comercial.empleado 
                    and self.objeto.comercial.empleado.usuario 
                    and self.objeto.comercial.empleado.usuario.usuario or ""):
                color_fg = "blue"
            else:
                color_fg = None
            ventana = model[itr][1]
            if ventana != "presupuestos.py":    # OJO: HARCODED
                color = "light gray"
            else:
                tipo = model[itr][3]
                if tipo == "create":
                    color = "yellow green"
                elif tipo == "drop":
                    color = "red"
                elif tipo == "update": 
                    color = "light blue"
                else:
                    # Cualquier otra cosa 
                    color = None
            cell.set_property("foreground", color_fg)
            cell.set_property("background", color)
            #cell.set_property("cell-background", color)
        cols = tv.get_columns()
        for i in xrange(len(cols)): 
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell, cell_func, i)
                # Aprovecho para cambiar el tamaño de la fuente:
                cell.set_property("font-desc", pango.FontDescription("sans 7"))

    def add_help_button(self):
        """
        Añade un botón para mostrar la leyenda de coloreado.
        """
        padre = self.wids['b_add'].parent
        b = self.wids['b_color_help'] = gtk.Button(stock = gtk.STOCK_HELP)
        padre.add(b)
        b.show()
        b.connect("clicked", self.show_color_help)

    def show_color_help(self, boton):
        """
        Crea una ventana con la leyenda de colores usada en las líneas de 
        presupuesto.
        """
        d = gtk.Dialog()
        d.add_buttons(gtk.STOCK_CLOSE, 1)
        for texto, fuente, color, color_fg in (
                ("Fibra",          "sans bold",   "gainsboro",   None), 
                ("Geotextil",      "sans bold",   "gold",        "dark green"), 
                ("Comercializado", "sans",        "olive drab",  "white"), 
                ("Servicio",       "sans italic", None,          "dark orange")):
            entry = gtk.Entry()
            entry.set_text(texto)
            entry.set_property("has-frame", False)
            entry.set_property("editable", False)
            if color_fg:
                color_fg = entry.get_colormap().alloc_color(color_fg)
            entry.modify_text(gtk.STATE_NORMAL, color_fg)
            if color:
                color = entry.get_colormap().alloc_color(color)
            entry.modify_base(gtk.STATE_NORMAL, color)
            entry.modify_font(pango.FontDescription(fuente))
            d.vbox.pack_start(entry)
        d.show_all()
        d.run()
        d.destroy()

    def colorear_contenido(self, tv):
        """
        Asocia una función al treeview para resaltar los productos.
        """
        self.add_help_button()
        def cell_func(column, cell, model, itr, numcol):
            ldpid = model[itr][-1]
            ldp = pclases.getObjetoPUID(ldpid)
            if ldp.productoVenta:       
                prod = ldp.productoVenta
                if prod.es_fibra():     # Fibra en gris
                    color = "gainsboro"
                    color_fg = None
                else:                   # Gtx. en amarillo
                    color = "gold"
                    color_fg = "dark green"
                fuente = "sans bold"
            elif ldp.productoCompra:    # Comercializado, verdito
                color = "olive drab"
                color_fg = "white"
                fuente = "sans"
            else:                       # Servicio, naranja
                color = None
                color_fg = "dark orange"
                fuente = "sans italic"
            cell.set_property("foreground", color_fg)
            cell.set_property("cell-background", color)
            if numcol == 1:     # Solo descripciones
                cell.set_property("font-desc", pango.FontDescription(fuente))
        cols = tv.get_columns()
        for i in xrange(len(cols)): 
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                if not isinstance(cell, gtk.CellRendererPixbuf):
                    # El cell del pixbuf del icono de notas lleva su 
                    # propia función de render.
                    column.set_cell_data_func(cell, cell_func, i)

    def colorear_presupuestos(self):
        def cell_func(column, cell, model, itr, i):
            try:
                presupuesto = pclases.getObjetoPUID(model[itr][-1])
            except (AttributeError, pclases.SQLObjectNotFound):
                color = None
            else:
                if presupuesto.estudio == None: # Indeterminado
                    color = "Indian Red"
                elif presupuesto.estudio:
                    color = "light yellow"
                else:                       # De pedido
                    color = "light green"
            cell.set_property("cell-background", color)
        cols = self.wids['tv_presupuestos'].get_columns()
        for i in xrange(len(cols)):
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell, cell_func, i)

    def cambiar_presupuesto_activo(self, tv):
        if pclases.DEBUG:
            print "   ------------------------> Soy cambiar_presupuesto_activo"
        model, itr = tv.get_selection().get_selected()
        if itr:
            puid = model[itr][-1]
            presupuesto_seleccionado = pclases.getObjetoPUID(puid)
            if self.objeto != presupuesto_seleccionado:
                if pclases.DEBUG:
                    print "  -----------------> ", presupuesto_seleccionado.id
                self.reset_cache_credito()
                self.ir_a(presupuesto_seleccionado) 

    def fin_edicion_cellrenderers(self, cell, nextwidget = None, 
                                  nextpath = None, nextcol = None):
        cell.stop_editing(False)
        self.rellenar_tablas()
        self.refresh_validado()
        if nextwidget != None:
            nextwidget.grab_focus()
        if nextpath != None and nextcol != None:
            self.wids['tv_contenido'].set_cursor(nextpath, nextcol, True)
        return False

    def tooltip_query(self, treeview, x, y, mode, tooltip):
        y_offset = treeview.get_bin_window().get_position()[1]
        path = treeview.get_path_at_pos(x, y - y_offset)
        if path:
            treepath, column = path[:2]  # @UnusedVariable
            model = treeview.get_model()
            itr = model.get_iter(treepath)
            ldp = pclases.getObjetoPUID(model[itr][-1])
            precioKilo = ldp.precioKilo
            if precioKilo != None:
                texto = "%s € / kg; Mínimo: %s" % (
                        utils.float2str(precioKilo), 
                        ldp.producto.precioMinimo)
                tooltip.set_text(texto)
                return True     # Muestra ya el tooltip
        return False    # No muestra tooltip.

    def update_prod_lpd(self, cell, path, text, model, ncol, model_tv):
        puidldp = model_tv[path][-1]
        ldp = pclases.getObjetoPUID(puidldp)
        ldp.descripcion = text
        # LEEEEEENTO
        # Si he tecleado un producto de compra o de venta, actualizo el 
        # registro como corresponde.
        producto = None
        for desc, puid in model:
            if text == desc:
                producto = pclases.getObjetoPUID(puid)
                break
        ldp.productoCompra = ldp.productoVenta = None
        if isinstance(producto, pclases.ProductoCompra):
            ldp.productoCompra = producto
        elif isinstance(producto, pclases.ProductoVenta):
            ldp.productoVenta = producto
        model_tv[path][ncol] = ldp.get_descripcion_producto() 
        # Pongo precio por defecto:
        if not ldp.precio:
            try:
                tarifa = self.objeto.cliente.tarifa
                precio = tarifa.obtener_precio(producto)
            except:
                try:
                    precio = ldp.producto.preciopordefecto
                except AttributeError: 
                    precio = 0
            ldp.precio = precio
            model_tv[path][2] = utils.float2str(ldp.precio, 3, autodec = True)
        # Compruebo que cantidad sea múltiplo si es un producto geotextil.
        if ldp.productoVenta and ldp.productoVenta.es_rollo():
            cantidad = ldp.cantidad
            cer = ldp.productoVenta.camposEspecificosRollo
            resto = cantidad % cer.metrosCuadrados
            if resto:
                nueva_cantidad = cantidad + cer.metrosCuadrados - resto
                if utils.dialogo(titulo = "¿CANTIDAD INCORRECTA?", 
                        texto = "El producto %s se vende por múltiplos "
                                "de %s m².\nLa línea contiene %s.\n\n"
                                "¿Corregir la cantidad a %s?" % (
                                    ldp.productoVenta.descripcion, 
                                    utils.float2str(cer.metrosCuadrados, 
                                                    autodec = True), 
                                    utils.float2str(cantidad, 
                                                    autodec = True), 
                                    utils.float2str(nueva_cantidad, 
                                                    autodec = True)), 
                        padre = self.wids['ventana']):
                    cantidad = nueva_cantidad
            ldp.cantidad = cantidad
        pclases.Auditoria.modificado(ldp, self.usuario, __file__)
        # Sigo con el foco en la cantidad.
        col = self.wids['tv_contenido'].get_column(0)
        #self.wids['tv_contenido'].grab_focus()
        #self.wids['tv_contenido'].set_cursor(path, col, True)
        gobject.idle_add(self.fin_edicion_cellrenderers, cell, 
                         self.wids['tv_contenido'], path, col)

    def cambiar_precio_ldp(self, cell, path, texto):
        """
        Cambia el precio de la LDP conforme al texto recibido.
        """
        self.reset_cache_credito()
        try:
            precio = utils._float(texto)
        except:
            utils.dialogo_info(titulo = "ERROR", 
                texto = 'El texto "%s" no es un número.' % (texto), 
                padre = self.wids['ventana'])
        else:
            model = self.wids['tv_contenido'].get_model()
            ldp = pclases.getObjetoPUID(model[path][-1])
            if ldp.precio != precio:
                ldp.precio = precio
                # Y compruebo la restricción de precio mínimo.
                if not self.objeto.check_validacion_precios():
                    self.objeto.validado = False
                    self.objeto.sync()
                    self.objeto.swap['fechaValidacion'] = None
                    self.objeto.swap['usuarioID'] = None
                pclases.Auditoria.modificado(ldp, self.usuario, __file__)
                gobject.idle_add(self.fin_edicion_cellrenderers, cell, 
                                 self.wids['b_add'])
                #self.rellenar_tablas()
                #self.refresh_validado()
                # Vuelvo al botón de añadir líneas.
                #self.wids['b_add'].grab_focus()

    def cambiar_cantidad_ldp(self, cell, path, texto):
        """
        Cambia la cantidad de la LDP conforme al texto recibido.
        """
        self.reset_cache_credito()
        try:
            cantidad = utils._float(texto)
        except:
            utils.dialogo_info(titulo = "ERROR", 
                texto = 'El texto "%s" no es un número.' % (texto), 
                padre = self.wids['ventana'])
        else:
            model = self.wids['tv_contenido'].get_model()
            ldp = pclases.getObjetoPUID(model[path][-1])
            # Si es rollo, ajusto al múltiplo de rollos completos.
            if ldp.productoVenta and ldp.productoVenta.es_rollo():
                cer = ldp.productoVenta.camposEspecificosRollo
                try:
                    resto = cantidad % cer.metrosCuadrados
                except ZeroDivisionError:  # No está bien dado de alta el prod.
                    resto = 0.0
                if resto:
                    nueva_cantidad = cantidad + cer.metrosCuadrados - resto
                    if utils.dialogo(titulo = "¿CANTIDAD INCORRECTA?", 
                            texto = "El producto %s se vende por múltiplos "
                                    "de %s m².\nHa teclado %s.\n\n"
                                    "¿Corregir la cantidad a %s?" % (
                                        ldp.productoVenta.descripcion, 
                                        utils.float2str(cer.metrosCuadrados, 
                                                        autodec = True), 
                                        utils.float2str(cantidad, 
                                                        autodec = True), 
                                        utils.float2str(nueva_cantidad, 
                                                        autodec = True)), 
                            padre = self.wids['ventana']):
                        cantidad = nueva_cantidad
            ldp.cantidad = cantidad
            pclases.Auditoria.modificado(ldp, self.usuario, __file__)
            self.rellenar_tablas()
            # Sigo con el foco en el precio.
            col = self.wids['tv_contenido'].get_column(2)
            #self.wids['tv_contenido'].grab_focus()
            #self.wids['tv_contenido'].set_cursor(path, col, True)
            gobject.idle_add(self.fin_edicion_cellrenderers, cell, 
                             self.wids['tv_contenido'], path, col)

    def activar_widgets(self, s):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        if (self.objeto and self.objeto.comercial 
            and self.usuario and self.usuario.get_comerciales()):
            es_mismo_comercial = (self.objeto.comercial 
                                  in self.usuario.get_comerciales())
            #print es_mismo_comercial
            # Excepción: que tenga nivel chachi de validar aunque 
            # tenga también perfil comercial. Si así también puede editar 
            # ofertas de otros comerciales. 
            if self.usuario.nivel > NIVEL_VALIDACION:
                s = s and es_mismo_comercial
        puede_bloquear = (self.usuario 
                                and self.usuario.nivel <= NIVEL_VALIDACION)
        s = self.objeto and (puede_bloquear or not self.objeto.bloqueado)
        if self.objeto == None:
            s = False
        ws = tuple(['b_pedido', "table1",  
                    "tv_contenido", "b_add", "b_drop", "rb_pedido",  
                   ] + [self.dic_campos[k] for k in self.dic_campos.keys()])
        for w in ws:
            try:
                self.wids[w].set_sensitive(s)
            except:
                self.logger.error("presupuestos::activar_widgets -> "
                                  "Widget %s no encontrado." % w)
                if pclases.DEBUG:
                    print w
        # Botón de hacer pedidos. Solo para ofertas de pedido validadas y si 
        # el usuario puede hacerlo.
        txt_puede_hacer_pedido = "Crea un pedido automáticamente con el "\
                                 "contenido de la oferta."
        permiso_nuevos_pedidos = calcular_permiso_nuevos_pedidos(
                                    self.usuario, self.logger)
        iconostockstado = self.wids['iconostado'].get_stock()[0]
        puede_hacer_pedido = self.objeto 
        if not puede_hacer_pedido:
            txt_puede_hacer_pedido = "No hay presupuesto activo."
        else:
            puede_hacer_pedido = permiso_nuevos_pedidos 
            if not puede_hacer_pedido:
                txt_puede_hacer_pedido="No tiene permisos para hacer pedidos."
            else:
                puede_hacer_pedido = self.objeto.esta_vigente() 
                if not puede_hacer_pedido:
                    txt_puede_hacer_pedido = "Presupuesto obsoleto."
                else:
                    puede_hacer_pedido = self.objeto.estudio == False
                    #and not self.objeto.estudio
                    # Mejor así, porque puede ser 
                    # None para estado indeterminado y en ese caso tampoco 
                    # puede pasar a pedido. 
                    if not puede_hacer_pedido:
                        txt_puede_hacer_pedido = "No se permiten pedidos "\
                                                 "de ofertas para estudio."
                    else:
                        puede_hacer_pedido = iconostockstado == gtk.STOCK_YES
                        if not puede_hacer_pedido:
                            txt_puede_hacer_pedido = "La oferta debe estar "\
                                    "validada para poder pasarla a pedido."
        puede_hacer_pedido = puede_hacer_pedido and 1 or 0   
            # and not aceptado_completo # <- Esto se chequea después. No hace 
                                        # falta
        self.wids['b_pedido'].set_sensitive(puede_hacer_pedido)
        self.wids['b_pedido'].set_tooltip_text(txt_puede_hacer_pedido)
        # Botones de imprimir y enviar por correo. Todas las ofertas de 
        # estudio y las de pedido que cumplan las restricciones "duras".
        txt_puede_imprimir = "Genera un PDF del presupuesto actual para "\
                        "imprimir, guardar o enviar por correo electrónico."
        puede_imprimir = ((self.objeto 
                           and self.objeto.estudio != None 
                           and 1) or 0) 
        if not puede_imprimir:
            txt_puede_imprimir = "Debe seleccionar el tipo de oferta."
        txt_puede_adjudicarse = "Marca la oferta como adjudicada."
        puede_adjudicarse = ((self.objeto 
                              and self.objeto.estudio != None 
                              and 1) or 0)
        if not puede_adjudicarse:
            txt_puede_adjudicarse = "Debe seleccionar el tipo de oferta."
        if self.objeto and not self.objeto.validado:
            # Si está validado, se puede imprimir sin problemas.
            if self.objeto and self.objeto.estudio == False:
                # En ofertas de pedido...
                estado = self.objeto.get_estado_validacion()
                if estado in CONDICIONES_DURAS:
                    puede_imprimir = False
                    txt_puede_imprimir = "Compruebe que la oferta tiene "\
                            "forma de pago, que cumple las restricciones "\
                            "de plazo y precio mínimo, que no tiene "\
                            "condiciones particulares y que no lleva "\
                            "comercializados"
                    if estado != pclases.COND_PARTICULARES:
                        # Una oferta con condiciones particulares sí que puede 
                        # adjudicarse. Solo que para imprimirla antes le 
                        # habrán tenido que dar el visto bueno.
                        puede_adjudicarse = False
                    txt_puede_adjudicarse = txt_puede_imprimir
            if (self.objeto and (
                    not self.objeto.lineasDePresupuesto 
                    or not self.objeto.cif
                    or not self.objeto.direccion
                    or not self.objeto.email
                    or not self.objeto.telefono)):
                # Para todas las ofertas... 
                puede_imprimir = False
                txt_puede_imprimir = "Compruebe que el contenido de la oferta"\
                        " no está vacío y que ha rellenado al menos los "\
                        "campos: CIF, dirección, correo electrónico y "\
                        "teléfono."
        self.wids['b_imprimir'].set_sensitive(puede_imprimir)
        self.wids['b_carta'].set_sensitive(puede_imprimir)
        self.wids['b_enviar'].set_sensitive(puede_imprimir)
        self.wids['ch_adjudicada'].set_sensitive(puede_adjudicarse)
        self.wids['b_imprimir'].set_tooltip_text(txt_puede_imprimir)
        self.wids['b_carta'].set_tooltip_text(txt_puede_imprimir)
        self.wids['b_enviar'].set_tooltip_text(txt_puede_imprimir)
        self.wids['ch_adjudicada'].set_tooltip_text(txt_puede_adjudicarse)
        self.actualizar_editable_motivo(self.wids['ch_denegado'])
        self.wids['txt_cred_motivo_rechazo'].set_sensitive(
                not self.wids['ch_cred_vb_admon'].get_active())
        # CWT: Si ya se había seleccionado el tipo de oferta y era de pedido, 
        # no permitir cambiarla.
        if self.objeto and self.objeto.estudio: 
            self.wids['hbox_radiobutton'].set_sensitive(False)
        elif self.objeto:
            self.wids['hbox_radiobutton'].set_sensitive(True)
        # Si el crédito ya se ha aprobado, bloqueo todo menos eso.
        if self.objeto and self.objeto.credUsuario:
            for w in self.wids.keys():
                if (("_cred_" in w and w != "ch_cred_vb_admon") 
                        or (w == "b_credito")):
                    self.wids[w].set_sensitive(False)
        # Aparte, si el usuario no tiene nivel para conceder crédito le 
        # impido tocar lo concedido y sus fechas.
        if self.usuario and self.usuario.nivel > NIVEL_VALIDACION:
            self.wids['e_cred_asegurado'].set_sensitive(False)
            self.wids['e_cred_fechaasegurado'].set_sensitive(False)
            self.wids['e_cred_concedido'].set_sensitive(False)
            self.wids['e_cred_fechaconcedido'].set_sensitive(False)

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
            filas_res.append(
                (r.id, 
                 utils.str_fecha(r.fecha), 
                 r.cliente and r.cliente.nombre or r.nombrecliente, 
                 r.obra and r.obra.nombre or r.nombreobra, 
                 r.comercial 
                    and r.comercial.empleado.nombre 
                            + " " + r.comercial.empleado.apellidos 
                    or "Sin comercial relacionado",
                r.get_str_tipo(), 
                r.adjudicada, 
                "Clic aquí para evaluar.", 
                r.personaContacto, 
                ", ".join([p.numpedido for p in r.get_pedidos()])))
        def mostrar_info_presupuesto(tv):
            model, itr = tv.get_selection().get_selected()
            if (itr and hasattr(model[itr][-3], "startswith")
                    and model[itr][-3].startswith("Clic aquí")):
                oferta = pclases.Presupuesto.get(model[itr][0])
                model[itr][-3] = oferta.get_str_estado()
        idpresupuesto = utils.dialogo_resultado(filas_res,
                            titulo = 'SELECCIONE OFERTA',
                            cabeceras = ('ID', 'Fecha', 
                                         'Nombre cliente', 
                                         'Obra', 
                                         "Comercial", 
                                         "Tipo", 
                                         "Adjudicada", 
                                         "Test de validación", 
                                         "Contacto", 
                                         "Pedido"), 
                            padre = self.wids['ventana'], 
                            func_change = mostrar_info_presupuesto)
        if idpresupuesto < 0:
            return None
        else:
            return idpresupuesto

    def rellenar_widgets(self):
        """
        Introduce la información del presupuesto actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        if pclases.DEBUG:
            print "  >>> :::::::::::::: rellenar_widgets :::::::::::::::"
        # Autobloqueo antes de nada.
        if (self.objeto and self.objeto.get_pedidos() 
                and not self.objeto.bloqueado):
            self.wids['ch_bloqueado'].disconnect(self.hndlr_bloqueado)
            self.objeto.make_swap("bloqueado")
            self.objeto.bloqueado = True
            self.objeto.syncUpdate()
            self.wids['ch_bloqueado'].set_active(self.objeto.bloqueado)
            self.hndlr_bloqueado = self.wids['ch_bloqueado'].connect(
                    'clicked', self.bloquear)
        # Botones atrás/adelante. ¿Hay anterior y siguiente?
        presupuestos_anteriores = self.buscar_presupuestos_accesibles(
                    mas_criterios_de_busqueda = 
                        pclases.Presupuesto.q.id < self.objeto.id)
        presupuestos_siguientes = self.buscar_presupuestos_accesibles(
                    mas_criterios_de_busqueda = 
                        pclases.Presupuesto.q.id > self.objeto.id)
        hay_anterior = presupuestos_anteriores.count() > 0
        self.wids['b_atras'].set_sensitive(hay_anterior)
        hay_siguiente = presupuestos_siguientes.count() > 0
        self.wids['b_adelante'].set_sensitive(hay_siguiente)
        # Formas de pago
        fdps = [(fdp.id, fdp.toString()) 
                for fdp in pclases.FormaDePago.select(
                    orderBy = "documento_de_pago_id, plazo")]
        utils.rellenar_lista(self.wids['cb_forma_cobro'], fdps)
        utils.rellenar_lista(self.wids['cbe_cliente'], 
            [(p.id, p.nombre) for p in 
             pclases.Cliente.select(orderBy = "nombre") 
             if not p.inhabilitado]) 
            # Lo pongo aquí por si crea un cliente nuevo sin cerrar esta 
            # ventana y lo quiere usar.
        # SANTABÁRBARA
        # Me aseguro de que si el cliente existe y es lo que tengo 
        # escrito, la asociación esté bien hecha.
        try:
            self.objeto.cliente = pclases.Cliente.selectBy(
                    nombre = self.objeto.nombrecliente)[0]
        except IndexError:
            pass    # Es cliente totally new. No pasa nada.
        # EOSANTABÁRBARA
        comerciales = []
        if self.usuario and self.usuario.empleados:
            for e in self.usuario.empleados:
                for c in e.comerciales:
                    comerciales.append(c)
        if not comerciales or (self.usuario 
                               and self.usuario.nivel<=NIVEL_VALIDACION):
            comerciales = pclases.Comercial.select() 
        if self.objeto.comercial and self.objeto.comercial not in comerciales:
            comerciales.append(self.objeto.comercial)
        opciones_comerciales = [
            (c.id, c.empleado and c.empleado.get_nombre_completo() 
                or "Comercial desconocido (%s)" % c.puid) 
            for c in comerciales
            if c.empleado.activo or c == self.objeto.comercial]
        opciones_comerciales.sort(key = lambda i: i[1])
        # CWT: Si no soy admin o equivalente, no puedo usar la opción de S/C
        if not self.usuario or self.usuario.nivel <= NIVEL_VALIDACION: 
            opciones_comerciales += [(-1, "Sin comercial relacionado")]
        utils.rellenar_lista(self.wids['cb_comercial'], 
                opciones_comerciales)
        self.actualizar_obras_cliente()
        presupuesto = self.objeto
        for nombre_col in self.dic_campos:
            if nombre_col == "comercialID" and not presupuesto.comercial:
                utils.combo_set_from_db(self.wids['cb_comercial'], -1)
            elif nombre_col == "clienteID" and not presupuesto.cliente:
                self.wids['cbe_cliente'].child.set_text(
                        presupuesto.nombrecliente)
            elif nombre_col == "obraID" and not presupuesto.obra:
                self.wids['cbe_obra'].child.set_text(
                        presupuesto.nombreobra)
            elif nombre_col == "cerrado":
                # En WIN el set_active IMPLICA un clicked del chbutton. Tengo 
                # que desconectarlo temporalmente.
                self.wids['ch_cerrado'].disconnect(self.hndlr_cerrado)
                # Inexplicable bug. Si lo hago con self.escribir_valor, hace 
                # llamada recursiva y machaca el cliente. WTF?!
                self.wids['ch_cerrado'].set_active(self.objeto.cerrado)
                self.hndlr_cerrado = self.wids['ch_cerrado'].connect('clicked',
                    self.cerrar_presupuesto)
            else:
                self.escribir_valor(presupuesto.sqlmeta.columns[nombre_col], 
                                    getattr(presupuesto, nombre_col), 
                                    self.dic_campos[nombre_col])
        self.rellenar_tablas()
        # Algunos campos "especialitos":
        self.wids['e_numero'].set_text(str(presupuesto.id))
        # Comprobar riesgo
        #self.comprobar_riesgo_cliente() # <-- Ya lo hago en el rellenar_tablas
        self.refresh_validado()
        self.objeto.make_swap()
        # Y ahora la lista de presupuestos.
        #self.rellenar_lista_presupuestos()
        # Para finalizar, el pedido al que se ha convertido
        numspedidos = [p.numpedido for p in presupuesto.get_pedidos()] 
        self.wids['e_pedido'].set_text(", ".join(numspedidos))
        self.wids['ch_bloqueado'].disconnect(self.hndlr_bloqueado)
        self.wids['ch_bloqueado'].set_active(self.objeto.bloqueado)
        self.hndlr_bloqueado = self.wids['ch_bloqueado'].connect('clicked', 
                self.bloquear)
        # Y ahora los "autocalculados" de la petición de crédito.
        self.wids['ch_cred_vb_comercial'].set_active(
                self.objeto.credVecesSolicitado > 0)
        self.wids["ch_cred_vb_admon"].set_active(
                self.objeto.credUsuarioID != None)
        # El nombre se guarda en un campo de texto al hacer clic en el check.
        self.wids["e_cred_cif"].set_text(self.objeto.cif)
        self.wids["e_cred_nombre"].set_text(self.objeto.nombrecliente)
        self.wids["e_cred_obra"].set_text(self.objeto.nombreobra)
        try:
            nombre_del_comercial = self.objeto.comercial.get_nombre_completo()
        except AttributeError: 
            nombre_del_comercial = ""
        self.wids["e_cred_comercial"].set_text(nombre_del_comercial)
        if pclases.DEBUG:
            print "  <<< :::::::::::::: rellenar_widgets :::::::::::::::"

    def actualizar_obras_cliente(self):
        idcliente = utils.combo_get_value(self.wids['cbe_cliente'])
        if idcliente and idcliente != -1:
            temp_cliente = pclases.Cliente.get(idcliente)
            #obras = [(o.id, o.get_str_obra()) 
            obras = [(o.id, o.nombre) 
                     for o in temp_cliente.obras]
        elif self.objeto.cliente:
            #obras = [(o.id, o.get_str_obra()) 
            obras = [(o.id, o.nombre) 
                     for o in self.objeto.cliente.obras]
        else:
            obras = []
        if (self.objeto.obra 
                and self.objeto.obra.id not in [o[0] for o in obras]):
            # Por si acaso no está la obra del presupuesto entre las del 
            # cliente por no estar la lista actualizada o lo que sea. 
            obras.append((self.objeto.obra.id, 
                          #self.objeto.obra.get_str_obra()))
                          self.objeto.obra.nombre))
        utils.rellenar_lista(self.wids['cbe_obra'], obras)

    def rellenar_lista_presupuestos(self):
        if not "tv_presupuestos" in self.wids.keys():
            # Se está creando la ventana. Cancelo y que me vuelva a llamar.
            return True 
        if pclases.DEBUG:
            ahora = time.time()
            print "rellenar_lista_presupuestos: begin"
        try:
            gobject.source_remove(self.hndlr_listado)
        except AttributeError:
            pass    # Primera vez.
        if pclases.DEBUG:
            print "rellenar_lista_presupuestos: Desconectando señal..."
        self.wids['tv_presupuestos'].disconnect(self.hndlr_presup)
        if pclases.DEBUG:
            print "rellenar_lista_presupuestos: Buscando presupuestos..."
        presupuestos = self.buscar_presupuestos_accesibles(solo_pdte = True)
        # Ya tengo los objetos. Ahora a rellenar en la interfaz.
        if pclases.DEBUG:
            print "rellenar_lista_presupuestos: Congelando TreeView..."
        model = self.wids['tv_presupuestos'].get_model()
        self.wids['tv_presupuestos'].freeze_child_notify()
        # model.clear()
        # Primero me hago una copia del model en un diccionario accesible por
        # el id del presupuesto.
        if pclases.DEBUG:
            print "rellenar_lista_presupuestos: Generando diccionario..."
        modelo = dic_presupuestos_from_model(self.wids['tv_presupuestos'])
        if pclases.DEBUG:
            print "rellenar_lista_presupuestos: Refrescando Model..."
        for p in presupuestos:
            # CWT: No deben salir los presupuestos ya servidos
            if p.get_pedidos():
                try:
                    itr = modelo.pop(p.puid)
                except KeyError:
                    pass
                else:
                    model.remove(itr)
                continue
            fila = [p.cerrado and gtk.STOCK_DIALOG_AUTHENTICATION or None,
                    p.validado and gtk.STOCK_YES or gtk.STOCK_NO, 
                    p.id, 
                    p.nombrecliente.strip() 
                        and p.nombrecliente.replace("&", "&amp;")
                        or "Oferta sin cliente", 
                        # Columna oculta. Para el tooltip
                    p.adjudicada and gtk.STOCK_APPLY or None, 
                    p.get_pedidos() and gtk.STOCK_CONNECT or None, 
                    p.puid]        # Oculta. Para el get.
            if p.adjudicada:
                fila[3] += " (oferta adjudicada)"
            pedidos = p.get_pedidos()
            if pedidos:
                fila[3] += " Servido en pedido %s" % (
                        ", ".join([p.numpedido for p in pedidos]))
            try:
                itr = modelo.pop(p.puid)
            except KeyError:
                itr = model.append(fila)
            else:
                update_fila(model, itr, fila)
            if self.objeto and self.objeto.id == p.id:
                path = model.get_path(itr)
        # Si me ha quedado algo en "modelo", son filas que no se corresponden 
        # con ningun presupuesto que deba aparecer en el TV. Lo quito:
        if pclases.DEBUG:
            print "rellenar_lista_presupuestos: Eliminando residuos..."
        for puid in modelo:
            itr = modelo[puid]
            model.remove(itr)
        # Y por fin acabé de actualizar el TreeView.
        if pclases.DEBUG:
            print "rellenar_lista_presupuestos: Descongelando TreeView..."
        self.wids['tv_presupuestos'].thaw_child_notify()
        # Lo desactivo porque tengo una manera mejor de 
        # marcar el presupuesto activo sin borrar, repoblar y redibujar
        # el model. Más que nada porque la primera llamada viene con la 
        # variable path sin instanciar. ¿Porcuá? Dunno.
        #self.wids['tv_presupuestos'].scroll_to_cell(path)
        #self.wids['tv_presupuestos'].get_selection().select_path(path)
        if pclases.DEBUG:
            print "rellenar_lista_presupuestos: Conectando señales..."
        self.hndlr_presup = self.wids['tv_presupuestos'].connect(
                            "cursor-changed", self.cambiar_presupuesto_activo)
        # DONE: Habilitar si consigo acelerar la búsqueda.
        self.hndlr_listado = gobject.timeout_add(10 * 60 * 1000, 
                self.rellenar_lista_presupuestos)
        if pclases.DEBUG:
            print "rellenar_lista_presupuestos: end (", 
            print time.time() - ahora, "segundos )"
        return True     # Para que siga llamándome indefinidamente.

    def buscar_presupuestos_accesibles(self, solo_pdte = False, 
                                       mas_criterios_de_busqueda = []):
        """
        Busca los presupuestos a los que puede acceder el usuario de la 
        ventana.
        Si "solo_pdte" es True, elimina de la lista de resultados los 
        presupuestos de estudio y los que no tengan informado ese campo; solo 
        buscará entre las ofertas de pedido que estén pendientes de 
        validación para imprimir (y por ende, no pasadas a pedido) y que no 
        hayan sido rechazadas.
        El resultado se devuelve **ordenado por id**.
        """
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        vpro.set_valor(0, "Buscando ofertas visibles...")
        # Primero determino si busco entre los presupuestos de todos los 
        # comerciales o solo los míos.
        if not self.usuario:    # Todos los presupuestos
            criterio_comercial = []
        elif (self.usuario.nivel <= NIVEL_VALIDACION 
                or calcular_permiso_nuevos_pedidos(self.usuario, self.logger)):
                # Todos los presupuestos también.
            criterio_comercial = []
        else:   # Soy usuario normal y corriente. Solo los míos y los de 
                # aquellos usuarios con menor nivel que yo.
            criterio_comercial = []
            for yo_as_comercial in self.usuario.get_comerciales():
                criterio_comercial.append(
                    pclases.Presupuesto.q.comercialID==yo_as_comercial.id)
            # Peeeeeero si tengo nivel 4 (el resto de comerciales tiene 5)
            # entonces debo dejar ver las ofertas de los demás porque soy 
            # el director de delegados comerciales. En realidad busco los 
            # que estén por debajo de mi nivel, así puedo establecer 
            # jerarquías en el futuro.
            for c in pclases.Comercial.select(pclases.AND(
                pclases.Empleado.q.usuarioID == pclases.Usuario.q.id, 
                pclases.Comercial.q.empleadoID == pclases.Empleado.q.id, 
                pclases.Usuario.q.nivel > self.usuario.nivel)):
                criterio_comercial.append(
                        pclases.Presupuesto.q.comercialID == c.id)
            criterio_comercial = pclases.OR(*criterio_comercial)
        # Ahora vamos con el criterio de "solo de pedidos pendientes de validar
        if solo_pdte:
            if mas_criterios_de_busqueda:
                mas_criterios_de_busqueda = pclases.AND(
                                    mas_criterios_de_busqueda, 
                                    pclases.Presupuesto.q.estudio == False, 
                                    pclases.Presupuesto.q.usuarioID == None, 
                                    pclases.Presupuesto.q.rechazado == False)
            else:
                mas_criterios_de_busqueda = pclases.AND(
                                    pclases.Presupuesto.q.estudio == False, 
                                    pclases.Presupuesto.q.usuarioID == None,
                                    pclases.Presupuesto.q.rechazado == False)
        # Ya tengo montados todos los criterios de selección. A JUGAAAAR:
        if criterio_comercial:
            criterios = pclases.AND(mas_criterios_de_busqueda, 
                                    criterio_comercial)
        else:
            criterios = mas_criterios_de_busqueda
        presupuestos = pclases.Presupuesto.select(pclases.AND(criterios), 
                                                  orderBy = "-id")
        # CWT: Solo los no validados PERO CON LA VALIDACIÓN QUE IMPIDE IMPRIMIR
        if solo_pdte:
            _presupuestos = []
            i = 0.0
            tot = presupuestos.count()
            for p in presupuestos:
                i += 1
                vpro.set_valor(i / tot, 
                    "Buscando ofertas visibles... (%d - %s)" 
                        % (p.id, p.nombrecliente), 
                    force_actualizar = True)
                if p.esta_servido():
                    continue    # Si ya se ha servido, validado o no, ya no 
                                # está pendiente de nada. Ya siguió su curso.
                estado = p.get_estado_validacion()
                if estado in CONDICIONES_DURAS:
                    _presupuestos.append(p)
            presupuestos = pclases.SQLlist(_presupuestos)
        vpro.ocultar()
        return presupuestos

    def refresh_validado(self):
        ch = self.wids['ch_validado']
        ch.set_active(self.objeto and self.objeto.usuario and 1 or 0)
        if self.objeto and self.objeto.usuario:
            ch.set_label("Validado por %s (%s)" % (
                self.objeto.usuario.usuario, 
                utils.str_fechahora(self.objeto.fechaValidacion)))
        else:
            ch.set_label("No validado (clic para validar)")

    def comprobar_riesgo_cliente(self):
        """
        Actualiza el icono de estado de riesgo del cliente del presupuesto.
        """
        if not self.objeto:
            return
        if pclases.DEBUG:
            print "Soy comprobar_riesgo_cliente. Objeto activo:",self.objeto.id
        self.objeto.notificador.desactivar()
        vpro = VentanaActividad(self.wids['ventana'], 
                                "Comprobando condiciones de riesgo...")
        vpro.mostrar()
        vpro.mover()
        txtestado = self.objeto.get_str_estado()
        if self.objeto.validado:    # True si ya validado manualmente.
            iconostockstado = gtk.STOCK_YES
            txtestado = "Validado por %s" % self.objeto.usuario.nombre
            color = None    # Me da igual. Ya está validado. No voy a 
                            # comprobar el crédito ni nada de eso.
        else:
            if self.objeto.cliente:
                if self.cache_credito == None:
                    vpro.mover()
                    importe_presupuesto = self.objeto.calcular_importe_total(
                                        iva = True)
                    vpro.mover()
                    self.cache_credito = self.objeto.cliente.\
                            calcular_credito_disponible(
                                    base = importe_presupuesto)
                if self.cache_credito <= 0:
                    vpro.mover()
                    color = self.wids['cbe_cliente'].child.get_colormap().\
                                alloc_color("IndianRed1")
                else:
                    color = self.wids['cbe_cliente'].child.get_colormap().\
                                alloc_color("Light Green")
                if self.objeto.get_estado_validacion() == pclases.VALIDABLE:
                    iconostockstado = gtk.STOCK_YES
                else:
                    iconostockstado = gtk.STOCK_STOP
            else:
                color = None
                iconostockstado = gtk.STOCK_DIALOG_WARNING
        vpro.mover()
        self.wids['cbe_cliente'].child.modify_base(gtk.STATE_NORMAL, color)
        vpro.mover()
        self.wids['iconostado'].set_from_stock(iconostockstado, 
                                               gtk.ICON_SIZE_DND)
        self.wids['iconostado'].set_tooltip_text(txtestado)
        # Esto de abajo ya se hace en desactivar_widgets
        #self.wids['b_pedido'].set_sensitive(
        #        iconostockstado == gtk.STOCK_YES
        #        and calcular_permiso_nuevos_pedidos(self.usuario, self.logger))
        # El equivalente a la validación automática es validarlo yo mismo.
        # Pero tengo que cuidarme de que no lo hayan validado ya antes. En ese 
        # caso no cambio nada a no ser que cambie algún precio o algo.
        if iconostockstado == gtk.STOCK_YES and not self.objeto.validado: 
        #         # Equivalente  a volver a llamar a la evaluación.
            self.objeto.validado = self.usuario
            self.objeto.swap['usuarioID'] = self.objeto.usuario
            fv = self.objeto.fechaValidacion
            if fv:
                fv_aprox = datetime.datetime(fv.year, fv.month, fv.day, 
                                             fv.hour, fv.minute, fv.second)
            else:
                fv_aprox = None
            self.objeto.swap['fechaValidacion'] = fv_aprox
            # Y si no lo dejo como estaba. No validado o validado por algún 
            # otro. Si modifico algo ya se invalidará y volverá a autovalidar
            # si es el caso.
        # else:
        #     self.objeto.validado = None
        self.actualizar_tooltip_de_cliente()
        # FIXME: A veces no se oculta la ventana de progreso en el ordenador 
        #        de Rafa. ¿Porcuá?
        vpro.ocultar()
        self.objeto.notificador.activar(self.aviso_actualizacion)        
        return self.cache_credito

    def actualizar_tooltip_de_cliente(self):
        idcliente = utils.combo_get_value(self.wids['cbe_cliente'])
        if idcliente and idcliente != -1:
            cliente = pclases.Cliente.get(idcliente)
            cliente.sync()
            if self.cache_credito == None:
                importe_pedido = self.objeto.calcular_importe_total(iva = True)
                self.cache_credito = cliente.\
                        calcular_credito_disponible(base = importe_pedido)
            credito = self.cache_credito
            if credito == sys.maxint:   # ¿maxint, te preguntarás? Ver 
                                        # docstring de calcular_credito
                                        # y respuesta hallarás.
                strcredito = "∞"
            else:
                strcredito = utils.float2str(credito)
            strfdp = cliente.textoformacobro
        else:
            strcredito = "Nuevo cliente. Sin datos de control de riesgo."
            strfdp = "No tiene"
        self.wids['cbe_cliente'].set_tooltip_text(
            "Crédito disponible (incluyendo el importe del presente"
            " presupuesto): %s\n"
            % strcredito)
        self.wids['cb_forma_cobro'].set_tooltip_text(
                "Forma de pago por defecto del cliente:\n%s" % strfdp)

    def rellenar_tablas(self):
        """
        Rellena la información de los TreeViews.
        """
        subtotal = self.rellenar_contenido()
        #total *= (1 - self.objeto.descuento)
        self.wids['e_subtotal'].set_text("%s €" % utils.float2str(subtotal))
        importe_iva = self.objeto.calcular_total_iva(subtotal)
        self.wids['e_total_iva'].set_text("%s €" % utils.float2str(
            importe_iva))
        total = subtotal + importe_iva
        self.wids['e_total'].set_text("%s €" % utils.float2str(total))
        self.wids['e_total'].modify_font(pango.FontDescription("bold"))
        self.comprobar_riesgo_cliente()
        # Y ahora el historial, que no afecta a nada.
        self.rellenar_historial()

    def rellenar_historial(self):
        """
        Busca todos los registros de auditoría de la oferta y los introduce 
        en la tabla debidamente formateados y coloreados.
        """
        w = self.wids['tv_auditoria']
        model = w.get_model()
        w.freeze_child_notify()
        w.set_model(None)
        model.clear()
        last_iter = None
        if self.objeto:
            # Cambios en el objeto en sí 
            audits = pclases.Auditoria.select(
                    pclases.Auditoria.q.dbpuid == self.objeto.puid, 
                    orderBy = "fechahora")
            self.lines_added = []
            audits = pclases.SQLlist(audits)
            # Líneas de presupuesto
            for ldpresupuesto in self.objeto.lineasDePresupuesto:
                more_audits = pclases.Auditoria.select(
                        pclases.Auditoria.q.dbpuid == ldpresupuesto.puid, 
                        orderBy = "fechahora")
                audits += [i for i in more_audits]
            # Cambios en el cliente
            if self.objeto.cliente:
                much_more_audits = pclases.Auditoria.select(
                        pclases.Auditoria.q.dbpuid == self.objeto.cliente.puid,
                        orderBy = "fechahora")
                audits += [i for i in much_more_audits]
            # Cambios en obra
            if self.objeto.obra:
                much_more_audits = pclases.Auditoria.select(
                        pclases.Auditoria.q.dbpuid == self.objeto.obra.puid,
                        orderBy = "fechahora")
                audits += [i for i in much_more_audits]
            # Cambios en pedido, albaranes y facturas relacionadas:
            for o in (self.objeto.get_pedidos() 
                        + self.objeto.get_albaranes() 
                        + self.objeto.get_facturas()):
                try:
                    much_more_audits = pclases.Auditoria.select(
                            pclases.Auditoria.q.dbpuid == o.puid,
                            orderBy = "fechahora")
                except AttributeError:  # ha devuelto None en aluna fra. o algo
                    much_more_audits = []
                audits += [i for i in much_more_audits if i not in audits]
            # Vuelco a la ventana, aunque no lleven orden de fechahora absoluto
            for a in audits:
                last_iter = self.agregar_linea_auditoria(model, a)
        w.set_model(model)
        w.thaw_child_notify()
        self.mover_a_ultima_fila(last_iter)

    def agregar_linea_auditoria(self, model, linea):
        """
        Inserta en el model la línea recibida.
        """
        lpuid = linea.get_puid()
        if lpuid not in self.lines_added:
            added = model.append(
                            (linea.usuario and linea.usuario.usuario or "", 
                             linea.ventana and linea.ventana.fichero or "", 
                             linea.dbpuid, 
                             linea.action, 
                             linea.ip, 
                             linea.hostname, 
                             utils.str_fechahora(linea.fechahora), 
                             linea.descripcion, 
                             linea.get_puid()))
            self.lines_added.append(lpuid)
            return added

    def mover_a_ultima_fila(self, last_iter):
        """
        Mueve el TreeView del historial a la última fila.
        """
        sel = self.wids['tv_auditoria'].get_selection()
        model, selected = sel.get_selected()
        # Me muevo al final si ya estaba en el final o si no estoy  
        # investigando nada (no tengo nada seleccionado en el treeview).
        vscroll = self.wids['tv_auditoria'].parent.get_vscrollbar()\
                                                            .get_adjustment()
        pos_scroll = vscroll.value
        abajo = vscroll.upper - vscroll.page_size
        if not selected or pos_scroll == abajo:
            try:
                self.wids['tv_auditoria'].scroll_to_cell(
                                                    model.get_path(last_iter),
                                                    use_align = True)
            except TypeError:   # last_iter no es un iter. Debe ser None.
                pass

    def rellenar_contenido(self):
        model = self.wids['tv_contenido'].get_model()
        model.clear()
        total = 0.0
        ldps = self.objeto.lineasDePresupuesto[:]
        ldps.sort(lambda x, y: int(x.id - y.id))
        for ldp in ldps:
            subtotal = ldp.get_subtotal(iva = False)
            total += subtotal
            # SANTABÁRBARA: Esto "reenlaza" si hiciera falta el 
            # producto{Compra|Venta} según la descripción guardada. Por si 
            # acaso...
            if ldp._link_producto():
                if pclases.DEBUG:
                    print "Línea de presupuesto %d enlazada con %s." % (
                            ldp.id, ldp.producto.puid)
            # EOSANTABÁRBARA 
            model.append((utils.float2str(ldp.cantidad), 
                          ldp.get_descripcion_producto(), 
                          utils.float2str(ldp.precio, 3, autodec = True), 
                          utils.float2str(subtotal),
                          #ldp.pedidoVenta != None,
                          #ldp.pedidoVenta and ldp.pedidoVenta.numpedido or "", 
                          ldp.puid))
        return total
    
    def nuevo(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        self.reset_cache_credito()
        presupuesto_anterior = self.objeto
        if presupuesto_anterior != None:
            presupuesto_anterior.notificador.desactivar()
        comercial = None
        if self.usuario and self.usuario.empleados:
            comerciales = []
            for e in self.usuario.empleados:
                for c in e.comerciales:
                    comerciales.append(c)
            if comerciales:
                comercial = comerciales[-1]
        presupuesto = pclases.Presupuesto(
            clienteID = None,
            fecha = mx.DateTime.localtime(), 
            nombrecliente = "", 
            nombreobra = "", 
            direccion = "", 
            ciudad = "", 
            provincia = "", 
            cp = "", 
            pais = "", 
            telefono = "", 
            fax = "", 
            texto = "", 
            despedida = "", 
            comercial = comercial, 
            validez = 0)
        pclases.Auditoria.nuevo(presupuesto, self.usuario, __file__)
        utils.dialogo_info('NUEVA OFERTA CREADA', 
                           'Nuevo presupuesto creado con éxito.\n\n'
                           'Campos obligatorios marcados en negrita.', 
                           padre = self.wids['ventana'])
        presupuesto.notificador.activar(self.aviso_actualizacion)
        self.objeto = presupuesto
        self.activar_widgets(True)
        self.actualizar_ventana(objeto_anterior = presupuesto_anterior)

    def buscar(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        presupuesto = self.objeto
        txtestudio = "Buscar solamente ofertas de estudio"
        txtpedido = "Buscar solamente ofertas de pedido"
        txtadjudicadas = "Buscar solamente ofertas adjudicadas"
        opciones_estudio_adjudicadas = {txtestudio: False, 
                                        txtpedido: False, 
                                        txtadjudicadas: False}
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR OFERTA", 
                                texto = "Introduzca número, nombre "\
                                        "del cliente u obra:", 
                                padre = self.wids['ventana'], 
                                opciones = opciones_estudio_adjudicadas) 
        if a_buscar != None:
            solopedido = opciones_estudio_adjudicadas[txtpedido]
            soloestudio = opciones_estudio_adjudicadas[txtestudio]
            adjudicadas = opciones_estudio_adjudicadas[txtadjudicadas]
            try:
                ida_buscar = int(a_buscar)
            except ValueError:
                ida_buscar = -1
            criterio = pclases.OR(
                    pclases.Presupuesto.q.nombrecliente.contains(a_buscar),
                    pclases.Presupuesto.q.nombreobra.contains(a_buscar),
                    pclases.Presupuesto.q.personaContacto.contains(a_buscar),
                    pclases.Presupuesto.q.id == ida_buscar)
            if solopedido:
                criterio = pclases.AND(criterio, 
                                       pclases.Presupuesto.q.estudio == False)
            elif soloestudio:
                criterio = pclases.AND(criterio, 
                                       pclases.Presupuesto.q.estudio == True)
            if adjudicadas:
                criterio = pclases.AND(criterio, 
                                    pclases.Presupuesto.q.adjudicada == True)
            #permiso_nuevos_pedidos = calcular_permiso_nuevos_pedidos(
            #                            self.usuario, self.logger)
            #if not(permiso_nuevos_pedidos 
            #       or (self.usuario 
            #           and self.usuario.nivel <= NIVEL_VALIDACION)):
            #    subcrit = []
            #    for yo_as_comercial in self.usuario.get_comerciales():
            #        subcrit.append(
            #            pclases.Presupuesto.q.comercialID==yo_as_comercial.id)
            #    criterio = pclases.AND(criterio, pclases.OR(*subcrit))
            #resultados = pclases.Presupuesto.select(criterio)
            resultados = self.buscar_presupuestos_accesibles(
                                        mas_criterios_de_busqueda = criterio)
            if resultados.count() > 1:
                    ## Refinar los resultados
                    idpresupuesto = self.refinar_resultados_busqueda(resultados)
                    if idpresupuesto == None:
                        return
                    resultados = [pclases.Presupuesto.get(idpresupuesto)]
                    # Me quedo con una lista de resultados de un único objeto 
                    # ocupando la primera posición.
                    # (Más abajo será cuando se cambie realmente el objeto 
                    # actual por este resultado.)
            elif resultados.count() < 1:
                    ## Sin resultados de búsqueda
                    utils.dialogo_info('SIN RESULTADOS', 
                            'La búsqueda no produjo resultados.\nPruebe a '
                            'cambiar el texto buscado o déjelo en blanco '
                            'para ver una lista completa.\n(Atención: '
                            'Ver la lista completa puede resultar lento si '
                            'el número de elementos es muy alto)',
                            padre = self.wids['ventana'])
                    return
            ## Un único resultado
            # Primero anulo la función de actualización
            if presupuesto != None:
                presupuesto.notificador.desactivar()
            # Pongo el objeto como actual
            try:
                presupuesto = resultados[0]
            except IndexError:
                utils.dialogo_info(titulo = "ERROR", 
                    texto = "Se produjo un error al recuperar la información."
                            "\nCierre y vuelva a abrir la ventana antes de "
                            "volver a intentarlo.", 
                    padre = self.wids['texto'])
                return
            # Y activo la función de notificación:
            presupuesto.notificador.activar(self.aviso_actualizacion)
            self.activar_widgets(True)
        self.objeto = presupuesto
        self.reset_cache_credito()
        self.actualizar_ventana()

    def guardar(self, widget):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        # Si guardo es que algo he modificado. Por tanto quito validación.
        # TODO: Esto no es así, en teoría las modificaciones en la solicitud 
        # de crédito no deberían invalidar la oferta... ¿o sí?
        self.objeto.validado = False
        self.objeto.swap['usuarioID'] = None
        self.objeto.swap['fechaValidacion'] = None
        # Desactivo el notificador momentáneamente
        self.objeto.notificador.activar(lambda: None)
        errores = []
        # Actualizo los datos del objeto
        ha_cambiado_el_cliente = ha_cambiado_observaciones = False
        for colname in self.dic_campos:
            col = self.clase.sqlmeta.columns[colname]
            try:
                valor_ventana = self.leer_valor(col, self.dic_campos[colname])
                if (colname == "clienteID" 
                        and valor_ventana != self.objeto.cliente):
                    ha_cambiado_el_cliente = True
                if (colname == "observaciones" 
                        and valor_ventana != self.objeto.observaciones
                        and valor_ventana.strip()):
                    ha_cambiado_observaciones = True
                if colname == "comercialID" and valor_ventana == -1:
                    valor_ventana = None
                if colname == "clienteID" and valor_ventana == None:
                    self.objeto.cliente = None
                    valor_ventana = self.wids['cbe_cliente'].child.get_text()
                    colname = "nombrecliente"
                if colname == "obraID" and valor_ventana == None:
                    cbe = self.wids['cbe_obra']
                    valor_ventana = cbe.child.get_text().strip()
                    # SAFETY DANCE!
                    try:
                        self.objeto.obra = pclases.Obra.selectBy(
                                nombre = valor_ventana)[0]
                        # Esto es por si ha escrito ex-ac-ta-men-te el nombre 
                        # de la obra pero no la ha seleccionado del desplegable
                        valor_ventana = self.objeto.obra.id
                    except IndexError:
                        self.objeto.obra = None
                        colname = "nombreobra"
                if colname == "cif":
                    _valor_ventana = utils.parse_cif(valor_ventana)
                    if _valor_ventana != valor_ventana:
                        #raise ValueError, "CIF incorrecto."
                        errores.append("CIF (formato incorrecto)")
                    valor_ventana = _valor_ventana
                setattr(self.objeto, colname, valor_ventana)
            except (ValueError, mx.DateTime.RangeError, TypeError):
                errores.append(colname)
        try:
            self.objeto.nombrecliente = self.objeto.cliente.nombre
        except AttributeError:  # El cliente no se ha dado de alta todavía.
            pass
        try:
            self.objeto.nombreobra = self.objeto.obra.nombre
        except AttributeError:  # La obra no se ha dado de alta todavía.
            pass
        # Fuerzo la actualización de la BD y no espero a que SQLObject lo 
        # haga por mí:
        self.objeto.syncUpdate()
        self.objeto.sync()
        # Vuelvo a activar el notificador
        self.objeto.notificador.activar(self.aviso_actualizacion)
        self.actualizar_ventana()
        self.wids['b_guardar'].set_sensitive(False)
        pclases.Auditoria.modificado(self.objeto, self.usuario, __file__)
        # Correos electrónicos de alarmas, altas y demás. Ahora compruebo 
        # primero que lo hayan marcado así los DELEGADOS (sic) comerciales.
        if self.objeto.cerrado and ha_cambiado_el_cliente:
            # self.enviar_correo_de_riesgo()
            pass    # CWT: Ver doc. de enviar_correo_riesgo
        if self.objeto.cerrado and self.debe_solicitar_validacion():
            self.enviar_correo_solicitud_validacion()
        if ha_cambiado_observaciones:
            self.enviar_correo_observaciones()
        if errores:
            utils.dialogo_info(titulo = "ERRORES AL GUARDAR", 
                    texto = "Se produjo un error al intentar guardar\n"
                            "los valores para los siguientes campos:\n"
                            + "\n - ".join(errores), 
                    padre = self.wids['ventana'])
        self.objeto.version += 1
        self.objeto.make_swap("version")
        pclases.Auditoria.modificado(self.objeto, self.usuario, __file__, 
                "Nueva versión %d." % self.objeto.version)

    def debe_solicitar_validacion(self):
        """
        Comprueba que no se haya solicitado ya la validación por correo. En 
        otro caso envía el correo de solicitud.
        """
        return (self.objeto 
                and not self.objeto.validado
                and self.objeto.id not in self.solicitudes_validacion)

    def enviar_correo_notificacion_validado(self):
        """
        Envía un correo de notificación de validación de la oferta al 
        comercial implicado. Pero solo si el comercial y el usuario que ha 
        validado no son el mismo.
        """
        if self.usuario and self.objeto:
            comerciales = [self.objeto.comercial]
            servidor = self.usuario.smtpserver
            smtpuser = self.usuario.smtpuser
            smtppass = self.usuario.smtppassword
            rte = self.usuario.email
            # TODO: OJO: HARDCODED
            if self.usuario and self.usuario.id == 1:   # Para depuración.
                dests = ["informatica@geotexan.com"]
            else:
                dests = [comercial.correoe for comercial in comerciales 
                         if comercial.empleado.usuario.usuario != self.usuario]
            # Correo de riesgo de cliente
            texto = "%s ha validado la oferta %d "\
                    "para el cliente %s de fecha %s." % (
                        self.objeto.usuario.nombre, 
                        self.objeto.id, 
                        self.objeto.nombrecliente, 
                        utils.str_fecha(self.objeto.fecha))
            enviar_correoe(rte, 
                           dests,
                           "Oferta %d validada." % self.objeto.id, 
                           texto, 
                           servidor = servidor, 
                           usuario = smtpuser, 
                           password = smtppass)
    
    def enviar_correo_solicitud_validacion(self):
        dests = self.select_correo_validador()
        if not isinstance(dests, (list, tuple)):
            dests = [dests]
        self.solicitudes_validacion[self.objeto.id] = dests
        servidor = self.usuario.smtpserver
        smtpuser = self.usuario.smtpuser
        smtppass = self.usuario.smtppassword
        rte = self.usuario.email
        # TODO: Habría que comprobar que la oferta está completa. Porque 
        # la primera vez que guardan casi seguro que no se valida auto.
        # dests = ["informatica@geotexan.com"]
        # Correo de riesgo de cliente
        texto = "Se ha creado la oferta %d "\
                "para el cliente %s que necesita validación manual." % (
                        self.objeto.id, 
                        self.objeto.nombrecliente)
        enviar_correoe(rte, 
                       dests,
                       "Alerta de validación manual de oferta", 
                       texto, 
                       servidor = servidor, 
                       usuario = smtpuser, 
                       password = smtppass)

    def borrar(self, widget):
        """
        Elimina el presupuesto de la tabla pero NO
        intenta eliminar ninguna de sus relaciones,
        de forma que si se incumple alguna 
        restricción de la BD, cancelará la eliminación
        y avisará al usuario.
        """
        presupuesto = self.objeto
        if utils.dialogo('¿Eliminar el presupuesto?\n\n\n'
                'SI NO ESTÁ SEGURO, RESPONDA «NO».', 
                'BORRAR', 
                padre = self.wids['ventana']):
            presupuesto.notificador.desactivar()
            try:
                presupuesto.destroy_en_cascada(ventana = __file__)
            except Exception, e:
                self.logger.error("presupuestos::borrar -> Presupuesto ID %d no se pudo eliminar. Excepción: %s." % (presupuesto.id, e))
                utils.dialogo_info(titulo = "PRESUPUESTO NO BORRADO", 
                                   texto = "El presupuesto no se pudo eliminar.\n\nSe generó un informe de error en el «log» de la aplicación.",
                                   padre = self.wids['ventana'])
                self.actualizar_ventana()
                return
            self.objeto = None
            self.reset_cache_credito()
            self.ir_a_primero_de_los_mios()

    def ir_a_primero_de_los_mios(self):
        if not self.usuario:
            self.ir_a_primero()
        else:
            if (self.usuario.nivel <= NIVEL_VALIDACION 
                    or calcular_permiso_nuevos_pedidos(self.usuario, 
                                                       self.logger)):
                try:
                    self.objeto = pclases.Presupuesto.select(orderBy="-id")[0]
                except IndexError:
                    self.objeto = None
            else:
                criterio = []
                for yo_as_comercial in self.usuario.get_comerciales():
                    criterio.append(
                        pclases.Presupuesto.q.comercialID==yo_as_comercial.id)
                presupuestos = pclases.Presupuesto.select(pclases.AND(
                                    pclases.Presupuesto.q.comercialID != None,
                                    pclases.OR(*criterio)), 
                                orderBy = "-id")
                #print presupuestos.count()
                try:
                    self.objeto = presupuestos[0]
                except IndexError:
                    self.objeto = None
        self.actualizar_ventana()
        
    def select_correo_validador(self):
        """
        Devuelve un correo de usuario con permisos de validación que 
        no sea admin. Uno diferente en cada llamada.
        """
        # TODO: OJO: HARCODED
        if not self.usuario or self.usuario.id == 1:
            return ["informatica@geotexan.com"]
        else:
            return ["nzumer@geotexan.com", "efigueroa@geotexan.com"]
        # CWT: Nada de RR. Correo a ambos.
        #round_robin = [u.email 
        #        for u in pclases.Usuario.select(
        #            pclases.Usuario.q.nivel <= NIVEL_VALIDACION)
        #        if u.usuario != "admin"]
        #if not hasattr(self, "ultimo_validador"):
        #    self.ultimo_validador = validador = round_robin[0]
        #else:
        #    posultimo = round_robin.index(self.ultimo_validador)
        #    posvalidador = posultimo + 1
        #    if posvalidador >= len(round_robin):
        #        posvalidador = 0
        #    self.ultimo_validador = validador = round_robin[posvalidador]
        #return validador


    def rellenar_plantilla_credito(self):
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.set_valor(0, "Rellenado plantilla...")
        vpro.mostrar()
        from lib.odfpy.contrib.odscell.odscell import updateCells, parseCell
        import os
        from tempfile import NamedTemporaryFile
        import shutil
        # Cargo la plantilla y creo una tabla para trabajar en ella que al 
        # principio contendrá lo mismo que la plantilla.
        plantilla = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                             "..", "informes", "solicitud_credito.ods")
        ruta_final = NamedTemporaryFile(suffix = ".ods").name
        shutil.copy(plantilla, ruta_final)
        ## Relleno los campos. Prepararsus que no son pocos:
        try:
            credsolicitado = str(int(utils._float(
                             self.wids['e_cred_credsolicitado'].get_text())))
        except ValueError:
            credsolicitado = ""
        try:
            credasegurado = str(int(utils._float(
                         self.wids['e_cred_asegurado'].get_text())))
        except ValueError:
            credasegurado  = ""
        try:
            credconcedido = str(int(utils._float(
                         self.wids['e_cred_concedido'].get_text())))
        except ValueError:
            credconcedido = ""
        celfields = {"B3": self.wids['e_cred_fecha'].get_text(), 
                     # HACK: Las celdas vacías consecutivas cuentan como 1 sola
                     #"F4": self.objeto.credApertura and "X" or " ", 
                     "D4": self.objeto.credApertura and "X" or " ", 
                     # HACK: Las celdas vacías consecutivas cuentan como 1 sola
                     #"F5": self.objeto.credAumento and "X" or " ", 
                     "E5": self.objeto.credAumento and "X" or " ", 
                     "F6": self.objeto.credSolicitud and "X" or " ", 
                     "B5": self.wids['e_cred_comercial'].get_text(), 
                    # Apartado de datos fiscales.
                     "B10": self.wids['e_cred_cif'].get_text(), 
                     "B12": self.wids['e_cred_nombre'].get_text(), 
                     "B14": self.wids['e_cred_ute'].get_text(), 
                     "B16": self.wids['e_cred_obra'].get_text(), 
                     "B18": self.wids['e_cred_licitador'].get_text(), 
                     "B20": self.wids['e_cred_dirfiscal'].get_text(), 
                     "B22": self.wids['e_cred_cpfiscal'].get_text(), 
                     "D22": self.wids['e_cred_poblacionfiscal'].get_text(), 
                     "F22": self.wids['e_cred_provinciafiscal'].get_text(), 
                     "B24": self.wids['e_cred_telefonofiscal'].get_text(), 
                     "D24": self.wids['e_cred_faxfiscal'].get_text(), 
                     "F24": self.wids['e_cred_movilfiscal'].get_text(), 
                     "B26": self.wids['e_cred_contactofiscal'].get_text(), 
                     # HACK: Las celdas vacías consecutivas cuentan como 1 sola
                     #"F26": self.wids['e_cred_emailfiscal'].get_text(), 
                     "E26": self.wids['e_cred_emailfiscal'].get_text(), 
                    # Apartado de envío de facturas y contratos. 
                     "B30": self.wids['e_cred_dircontratos'].get_text(), 
                     "B32": self.wids['e_cred_cpcontratos'].get_text(), 
                     "D32": self.wids['e_cred_poblacioncontratos'].get_text(), 
                     "F32": self.wids['e_cred_provinciacontratos'].get_text(), 
                     "B34": self.wids['e_cred_telefonocontratos'].get_text(), 
                     "D34": self.wids['e_cred_emailcontratos'].get_text(), 
                     "B36": self.wids['e_cred_contactocontratos'].get_text(), 
                     # HACK: Las celdas vacías consecutivas cuentan como 1 sola
                     #"F36": self.wids['e_cred_movilcontratos'].get_text(),  
                     "E36": self.wids['e_cred_movilcontratos'].get_text(),  
                    # Apartado de dirección de obra (envío de materiales)
                     "B40": self.wids['e_cred_dirobra'].get_text(), 
                     "B42": self.wids['e_cred_cpobra'].get_text(), 
                     "D42": self.wids['e_cred_poblacionobra'].get_text(), 
                     "F42": self.wids['e_cred_provinciaobra'].get_text(), 
                     "B44": self.wids['e_cred_movilobra'].get_text(), 
                     "B46": self.wids['e_cred_contactoobra'].get_text(), 
                    # Apartado de datos de pago 
                     "B50": self.wids['e_cred_fdp'].get_text(), 
                     "A53": self.wids['txt_cred_entidades'].get_buffer(
                         ).get_text(
                             *self.wids['txt_cred_entidades'].get_buffer(
                                 ).get_bounds()),
                     "A57": self.wids['e_cred_entidad'].get_text(), 
                     "B57": self.wids['e_cred_oficina'].get_text(), 
                     "C57": self.wids['e_cred_digitocontrol'].get_text(), 
                     "D57": self.wids['e_cred_numcuenta'].get_text(), 
                     "B59": self.wids['e_cred_diapago1'].get_text(), 
                     "C59": self.wids['e_cred_diapago2'].get_text(), 
                     "D59": self.wids['e_cred_diapago3'].get_text(), 
                    # Apartado de riesgos cliente
                     "B63": credsolicitado, 
                     "A66": self.wids['txt_cred_observaciones'].get_buffer(
                        ).get_text(
                            *self.wids['txt_cred_observaciones'].get_buffer(
                                ).get_bounds()),
                     "A69": self.wids['txt_cred_condiciones'].get_buffer(
                             ).get_text(
                                *self.wids['txt_cred_condiciones'].get_buffer(
                                    ).get_bounds()),
                    # Apartado de vistos buenos
                     "A74": self.wids['e_cred_vb_nombrecomercial'].get_text(), 
                     "C72": self.wids['e_cred_vb_nombreadmon'].get_text(), 
                     "F71": credasegurado, 
                     "F73": self.wids['e_cred_fechaasegurado'].get_text(), 
                     "F75": credconcedido, 
                     # HACK: Las celdas vacías consecutivas cuentan como 1 sola
                     #"F77": self.wids['e_cred_fechaconcedido'].get_text(), 
                     "E77": self.wids['e_cred_fechaconcedido'].get_text(), 
                    }
        celdas = celfields.keys()
        celdas.sort(cmp = cmp_celdas_lrtd)
        tot = len(celdas)
        i = 0.0
        for cell in celfields:
            i += 1
            vpro.set_valor(i/tot, "Rellenando plantilla...")
            valor = prepare_for_ods(celfields[cell])
            if valor:
                updateCells(ruta_final, 
                                0,      # Índice de la hoja dentro del .ods
                                parseCell(cell)[1],     # row
                                parseCell(cell)[0],     # col
                                1,  # Número de celdas consecutivas a cambiar X
                                1,  # Número de celdas consecutivas a cambiar Y
                                [valor])    # Espera un iterable
        ## Y por fin guardo y devuelvo la ruta.
        vpro.set_valor(1.0, 
                "Enviando plantilla por correo. Por favor, aguarde.")
        vpro.ocultar()
        return ruta_final

def calcular_permiso_nuevos_pedidos(usuario, logger = None):
    if usuario == None:
        permiso_nuevos_pedidos = True
    else:
        try:
            ventana_pedidos = pclases.Ventana.select(
                    pclases.Ventana.q.fichero == "pedidos_de_venta.py")[0]
        except IndexError:
            if logger:
                logger.error("presupuestos::calcular_permiso_nuevos_pedidos "
                    "-> Ventana de pedidos de venta no encontrada en la BD.")
            permiso_nuevos_pedidos = False
        else:
            permisos_ventana_pedidos = usuario.get_permiso(ventana_pedidos)
            permiso_nuevos_pedidos = permisos_ventana_pedidos.nuevo
    return permiso_nuevos_pedidos
    

def match_producto(completion, key, itr, ncol):
    model = completion.get_model()
    text = model.get_value(itr, ncol)
    #if text.startswith(key):
    if key.upper() in text.upper():
        return True
    return False


def dic_presupuestos_from_model(tv):
    model = tv.get_model()
    itr = model.get_iter_first()
    res = {}
    while itr:
        puid = model[itr][-1]
        res[puid] = itr
        itr = model.iter_next(itr)
    return res


def update_fila(model, itr, fila):
    i = 0
    for field in fila:
        model[itr][i] = fila[i]
        i += 1


def hacer_pedido(presupuesto, usuario, ventana_padre = None):
    """
    Crea un pedido con el cliente del presupuesto y como contenido 
    las líneas de pedido y servicios del mismo.
    """
    nuevopedido = None
    if not tiene_pedido_asignado(presupuesto, ventana_padre):
        # TODO: ¿Debo comprobar si el cliente tiene crédito 
        # suficiente para crear un pedido con toda la oferta? Pues en teoría 
        # no. Porque si no tiene crédito, necesita validación manual. Y si 
        # alguien con permisos ha validado es porque se le puede vender esta 
        # oferta aunque no tenga crédito. No tiene sentido volver a 
        # a comprobarlo a no ser que la oferta fuera válida en principio y al 
        # cabo de unos días, cuando se intente hacer el pedido, ya no tenga 
        # crédito por el motivo que sea.
        numpedido = utils.dialogo_entrada(
                texto = 'Introduzca un número de pedido.', 
                titulo = 'NÚMERO DE PEDIDO', 
                padre = ventana_padre)
        if numpedido != None:
            existe = pclases.PedidoVenta.select(
                pclases.PedidoVenta.q.numpedido == numpedido)
            if existe.count() > 0:
                nuevopedido = preguntar_si_agregar_a_pedido(
                                ventana_padre, existe, nuevopedido)
            else:
                if not presupuesto.cliente:
                    presupuesto.cliente = buscar_cliente(presupuesto, usuario)
                if not presupuesto.cliente:
                    # PLAN: Sugerir clientes con nombres parecidos o 
                    # permitir que se creen si tiene permiso.
                    nuevopedido = None
                    utils.dialogo_info(titulo = "CLIENTE NO EXISTE", 
                            texto = "Asegúrese de que el cliente\n"
                                    "«%s»\n"
                                    "existe y está correctamente escrito." % (
                                        presupuesto.nombrecliente), 
                            padre = ventana_padre)
                else:
                    if not presupuesto.obra:
                        if presupuesto.nombreobra:
                            presupuesto.obra = crear_obra(presupuesto, usuario)
                        else:
                            customer = presupuesto.cliente
                            presupuesto.obra = customer.get_obra_generica()
                    nuevopedido = crear_pedido(presupuesto, numpedido, usuario)
            if nuevopedido != None:
                for ldp in presupuesto.lineasDePresupuesto:
                    add_ldp_a_pedido(presupuesto, ldp, nuevopedido, usuario)
                #self.actualizar_ventana()
    return nuevopedido

def preguntar_si_agregar_a_pedido(ventana_padre, existe, nuevopedido):
    if utils.dialogo(titulo = "PEDIDO YA EXISTE", 
            texto = "El número de pedido ya existe. "\
                    "¿Desea agregar la oferta?", 
            padre = ventana_padre):
        nuevopedido = existe[0]
        if nuevopedido.cerrado:
            utils.dialogo_info(titulo = "PEDIDO CERRADO", 
                texto = "El pedido %s está cerrado y no admite "
                        "cambios. Corrija esta situación antes "
                        "de volver a intentarlo." % (
                            nuevopedido.numpedido), 
                padre = ventana_padre)
            nuevopedido = None
    else:
        nuevopedido = None
    return nuevopedido

def tiene_pedido_asignado(presupuesto, ventana_padre):
    if presupuesto and presupuesto.get_pedidos():
        # PLAN: Esto habrá que cambiarlo por una función que compruebe 
        # si queda algo que no haya sido pasado a pedido. No todos los 
        # presupuestos se van a convertir en un único pedido.
        # CWT: Sí que de cada presupuesto se saca un único pedido. 
        utils.dialogo_info(titulo = "NO SE PUEDE CONVERTIR A PEDIDO", 
                texto = "La oferta ya se encuentra vinculada a "
                        "los pedidos: %s" % (
                            ", ".join([p.numpedido 
                                       for p in presupuesto.get_pedidos()]
                                     )),
                padre = ventana_padre)
        return True
    return False


def abrir_pedido(nuevopedido, usuario):
    from formularios import pedidos_de_venta
    ventanapedido = pedidos_de_venta.PedidosDeVenta(    # @UnusedVariable
            objeto = nuevopedido, 
            usuario = usuario)


def add_ldp_a_pedido(presupuesto, ldp, nuevopedido, usuario):
    productoCompra = ldp.productoCompra
    productoVenta = ldp.productoVenta
    if productoCompra or productoVenta:
        nldp = pclases.LineaDePedido(pedidoVenta = nuevopedido,
                productoCompra = productoCompra, 
                productoVenta = productoVenta, 
                notas = ldp.notas, 
                precio = ldp.precio, 
                cantidad = ldp.cantidad, 
                presupuesto = presupuesto, 
                fechaEntrega = None)
        pclases.Auditoria.nuevo(nldp, usuario, __file__)
    else:   # Creo servicio entonces
        nsrv = pclases.Servicio(pedidoVenta = nuevopedido, 
                cantidad = ldp.cantidad,
                precio = ldp.precio, 
                concepto = ldp.descripcion, 
                notas = ldp.notas, 
                presupuesto = presupuesto)
        pclases.Auditoria.nuevo(nsrv, usuario, __file__)


def crear_pedido(presupuesto, numpedido, usuario):
    obra = presupuesto.obra
    try:
        ciuObra = obra.ciudad
        cpObra = obra.cp
        dirObra = obra.direccion
        nomObra = obra.nombre
        paiObra = obra.pais 
        if not paiObra:
            try:
                paiObra = presupuesto.cliente.pais
            except AttributeError:
                paiObra = ""
        proObra = obra.provincia
    except AttributeError, msg:
        if pclases.DEBUG:
            print "presupuestos.py::crear_pedido -> AttributeError:", msg
        ciuObra = cpObra = dirObra = nomObra = paiObra = proObra = ""
    nuevopedido = pclases.PedidoVenta(cliente = presupuesto.cliente, 
                            fecha = mx.DateTime.localtime(), 
                            numpedido = numpedido,
                            iva = presupuesto.cliente.iva,
                            descuento = 0,
                            transporteACargo = False,
                            bloqueado = True,
                            cerrado = False, 
                            comercial = presupuesto.comercial, 
                            obra = presupuesto.obra, 
                            formaDePago = presupuesto.formaDePago, 
                            validado = presupuesto.validado 
                                and True or False, 
                            usuario = presupuesto.usuario, 
                            ciudadCorrespondencia = ciuObra, 
                            cpCorrespondencia = cpObra, 
                            direccionCorrespondencia = dirObra, 
                            nombreCorrespondencia = nomObra, 
                            paisCorrespondencia = paiObra, 
                            provinciaCorrespondencia = proObra)
    pclases.Auditoria.nuevo(nuevopedido, usuario, __file__)
    return nuevopedido


def crear_obra(presupuesto, usuario):
    # Voy a añadir un control extra para evitar que se sigan duplicando.
    try:
        obra = pclases.Obra.selectBy(nombre = presupuesto.nombreobra)[0]
    except IndexError:
        obra = pclases.Obra(
                nombre = presupuesto.nombreobra, 
                direccion = presupuesto.direccion, 
                cp = presupuesto.cp, 
                ciudad = presupuesto.ciudad, 
                provincia = presupuesto.provincia, 
                observaciones = "Creada automáticamente desde presupuesto.", 
                pais = presupuesto.pais, 
                generica = False)
        pclases.Auditoria.nuevo(obra, usuario, __file__)
    if presupuesto.cliente not in obra.clientes:
        obra.addCliente(presupuesto.cliente)
    return obra


def buscar_cliente(presupuesto, usuario, crear_si_no_existe = False):
    """
    Crea (o recupera) el cliente del presupuesto y lo devuelve.
    """
    try:
        cliente = pclases.Cliente.selectBy(
                    nombre = presupuesto.nombrecliente.strip())[0]
    except IndexError:
        if crear_si_no_existe:
            cliente = pclases.Cliente(
                nombre = presupuesto.nombrecliente, 
                cif = presupuesto.cif, 
                direccion = presupuesto.direccion, 
                ciudad = presupuesto.ciudad, 
                provincia = presupuesto.provincia, 
                pais = presupuesto.pais, 
                cp = presupuesto.cp, 
                telefono = presupuesto.telefono, 
                email = presupuesto.email,
                vencimientos = presupuesto.formaDePago.toString(
                    presupuesto.cliente), 
                formadepago = presupuesto.formaDePago.toString(
                    presupuesto.cliente), 
                contacto = presupuesto.personaContacto)
            pclases.Auditoria.nuevo(cliente, usuario, __file__)
        else:
            cliente = None
    return cliente


def build_fila_historial(ofertado, pedido, servido, facturado, pendiente, 
                         producto):
    try:
        ofer = ofertado[producto]
    except KeyError:
        ofer = 0.0
    try:
        pedi = pedido.pop(producto)
    except KeyError:
        pedi = 0.0
    try:
        serv = servido.pop(producto)
    except KeyError:
        serv = 0.0
    try:
        fact = facturado.pop(producto)
    except KeyError:
        fact = 0.0
    try:
        pdte = pendiente.pop(producto)
    except KeyError:
        pdte = 0.0
    try:
        desc = producto.descripcion
        puid = producto.puid
    except AttributeError:
        desc = producto
        puid = ""
    fila = (desc, ofer, pedi, serv, fact, pdte, puid)
    return fila


def generar_pdf_presupuesto(objeto_presupuesto):
    modulo = pclases.config.get_modelo_presupuesto()
    import importlib
    presupuesto = importlib.import_module("." + modulo, "informes")
    #exec "import %s as presupuesto" % modulo
    pdf_presupuesto = presupuesto.go_from_presupuesto(objeto_presupuesto)
    return pdf_presupuesto

def prepare_for_xls(cadena):
    """
    Pepara la cadena para ser incluída en una hoja de cálculo en ODF (.ods).
    """
    valor = cadena
    # TODO: No me gusta cambiar el encoding --y menos a uno sin tildes--, 
    # pero tampoco encuentro la manera de que el xls me pille unicode por 
    # mucho que lo fuerzo. 
    # TODO: También habría que retocar la plantilla para que los bordes 
    # se dibujaran desde las celdas adyacentes, ya que al rellenar el valor 
    # se pierden los bordes de las celdas que relleno. Pero como además me 
    # han pasado el Excel protegido... pues tampoco puedo tocarlo 
    # (en teoría...MWHAHAHAHA. BOFH inside)
    valor = valor.encode("ascii", "replace")
    #valor = valor.replace("\n", " ").strip()
    return valor


def prepare_for_ods(cadena):
    """
    Pepara la cadena para ser incluída en una hoja de cálculo en ODF (.ods).
    """
    valor = cadena
    #valor = valor.encode("iso-8859-15")
    valor = valor.replace("\n", " ").strip()
    return valor

def cmp_celdas_lrtd(a, b):
    """
    Compara las cadenas a y b teniendo en cuenta que son etiquetas de celdas 
    de la forma Xnn donde X es la columna y nn un entero con la fila. Devuelve 
    -1 si a es menor que b. Se considera el orden de izquierda a derecha y 
    de arriba a abajo, por ejemplo: A2 < A5 < B1
    """
    # FIXME: Muy chapucero y teniendo en cuenta que no vamos a encontrar más 
    # de Z columnas.
    cola = a[0].upper()
    colb = b[0].upper()
    if cola < colb:
        res = -1
    elif cola > colb:
        res = 1
    else:
        fila = int(a[1:])
        filb = int(b[1:])
        res = fila - filb
    return res


def convertir_a_html(fods):
    # PORASQUI: Resulta que al cargar el ods original, solo llega hasta la 
    # mitad de la hoja de cálculo. El resto es como si no existiera.
    pathdest = fods + ".html"
    from lib.simple_odspy.simpleodspy.sodsspreadsheet import SodsSpreadSheet
    from lib.simple_odspy.simpleodspy.sodshtml import SodsHtml
    from lib.simple_odspy.simpleodspy.sodsods import SodsOds
    t = SodsSpreadSheet()
    tw = SodsOds(t)
    tw.load(fods)   # load carga el contenido de fods en t. fw no vale para 
    tw = SodsHtml(t)    # nada después de eso. Lo reutilizo para html
    tw.save(pathdest)
    return pathdest

def crear_xls(p, wids_ventana):
    """
    Crea "un excel" a partir de una plantilla xls en blanco (el nombre está 
    predeterminado y no se puede cambiar) con los datos del presupuesto «p».
    """
    vpro = VentanaProgreso(padre = wids_ventana['ventana'])
    vpro.set_valor(0, "Rellenado plantilla (xls)...")
    vpro.mostrar()
    from lib.odfpy.contrib.odscell.odscell import updateCells, parseCell
    from lib.xlutils.xlutils import copy
    from lib.xlwt import xlwt
    from lib.xlrd import xlrd
    import os
    from tempfile import NamedTemporaryFile
    # Cargo la plantilla y creo una tabla para trabajar en ella que al 
    # principio contendrá lo mismo que la plantilla.
    plantilla = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                         "..", "informes", "solicitud_credito.xls")
    ruta_final = NamedTemporaryFile(suffix = ".xls").name
    ## Relleno los campos. Prepararsus que no son pocos:
    try:
        credsolicitado = str(int(utils._float(
                         wids_ventana['e_cred_credsolicitado'].get_text())))
    except ValueError:
        credsolicitado = ""
    try:
        credasegurado = str(int(utils._float(
                     wids_ventana['e_cred_asegurado'].get_text())))
    except ValueError:
        credasegurado  = ""
    try:
        credconcedido = str(int(utils._float(
                     wids_ventana['e_cred_concedido'].get_text())))
    except ValueError:
        credconcedido = ""
    celfields = {"B5": wids_ventana['e_cred_fecha'].get_text(), 
                 # HACK: Las celdas vacías consecutivas cuentan como 1 sola
                 #"F4": p.credApertura and "X" or " ", 
                 "O6": p.credApertura and "X" or " ", 
                 # HACK: Las celdas vacías consecutivas cuentan como 1 sola
                 #"F5": p.credAumento and "X" or " ", 
                 "O7": p.credAumento and "X" or " ", 
                 "O8": p.credSolicitud and "X" or " ", 
                 "B7": wids_ventana['e_cred_comercial'].get_text(), 
                # Apartado de datos fiscales.
                 "B13": wids_ventana['e_cred_cif'].get_text(), 
                 "B15": wids_ventana['e_cred_nombre'].get_text(), 
                 "B17": wids_ventana['e_cred_ute'].get_text(), 
                 "B19": wids_ventana['e_cred_obra'].get_text(), 
                 "B21": wids_ventana['e_cred_licitador'].get_text(), 
                 "B23": wids_ventana['e_cred_dirfiscal'].get_text(), 
                 "B25": wids_ventana['e_cred_cpfiscal'].get_text(), 
                 "F25": wids_ventana['e_cred_poblacionfiscal'].get_text(), 
                 "M25": wids_ventana['e_cred_provinciafiscal'].get_text(), 
                 "B27": wids_ventana['e_cred_telefonofiscal'].get_text(), 
                 "G27": wids_ventana['e_cred_faxfiscal'].get_text(), 
                 "M27": wids_ventana['e_cred_movilfiscal'].get_text(), 
                 "B29": wids_ventana['e_cred_contactofiscal'].get_text(), 
                 # HACK: Las celdas vacías consecutivas cuentan como 1 sola
                 #"F26": wids_ventana['e_cred_emailfiscal'].get_text(), 
                 "M29": wids_ventana['e_cred_emailfiscal'].get_text(), 
                # Apartado de envío de facturas y contratos. 
                 "B34": wids_ventana['e_cred_dircontratos'].get_text(), 
                 "B36": wids_ventana['e_cred_cpcontratos'].get_text(), 
                 "F36": wids_ventana['e_cred_poblacioncontratos'].get_text(), 
                 "M36": wids_ventana['e_cred_provinciacontratos'].get_text(), 
                 "B38": wids_ventana['e_cred_telefonocontratos'].get_text(), 
                 "K38": wids_ventana['e_cred_emailcontratos'].get_text(), 
                 "B40": wids_ventana['e_cred_contactocontratos'].get_text(), 
                 # HACK: Las celdas vacías consecutivas cuentan como 1 sola
                 #"F36": wids_ventana['e_cred_movilcontratos'].get_text(),  
                 "M40": wids_ventana['e_cred_movilcontratos'].get_text(),  
                # Apartado de dirección de obra (envío de materiales)
                 "B45": wids_ventana['e_cred_dirobra'].get_text(), 
                 "B47": wids_ventana['e_cred_cpobra'].get_text(), 
                 "F47": wids_ventana['e_cred_poblacionobra'].get_text(), 
                 "M47": wids_ventana['e_cred_provinciaobra'].get_text(), 
                 "B49": wids_ventana['e_cred_movilobra'].get_text(), 
                 "B51": wids_ventana['e_cred_contactoobra'].get_text(), 
                # Apartado de datos de pago 
                 "C56": wids_ventana['e_cred_fdp'].get_text(), 
                 "A60": wids_ventana['txt_cred_entidades'].get_buffer(
                     ).get_text(
                         *wids_ventana['txt_cred_entidades'].get_buffer(
                             ).get_bounds()),
                 "A68": wids_ventana['e_cred_entidad'].get_text(), 
                 "D68": wids_ventana['e_cred_oficina'].get_text(), 
                 "I68": wids_ventana['e_cred_digitocontrol'].get_text(), 
                 "L68": wids_ventana['e_cred_numcuenta'].get_text(), 
                 "G70": wids_ventana['e_cred_diapago1'].get_text(), 
                 "H70": wids_ventana['e_cred_diapago2'].get_text(), 
                 "I70": wids_ventana['e_cred_diapago3'].get_text(), 
                # Apartado de riesgos cliente
                 "B75": credsolicitado, 
                 "A78": wids_ventana['txt_cred_observaciones'].get_buffer(
                    ).get_text(
                        *wids_ventana['txt_cred_observaciones'].get_buffer(
                            ).get_bounds()),
                 "A83": wids_ventana['txt_cred_condiciones'].get_buffer(
                         ).get_text(
                            *wids_ventana['txt_cred_condiciones'].get_buffer(
                                ).get_bounds()),
                # Apartado de vistos buenos
                 "A94": wids_ventana['e_cred_vb_nombrecomercial'].get_text(), 
                 ## Protegido en el original. No lo toco.
                 #"": wids_ventana['e_cred_vb_nombreadmon'].get_text(), 
                 #"": credasegurado, 
                 #"": wids_ventana['e_cred_fechaasegurado'].get_text(), 
                 #"": credconcedido, 
                 # HACK: Las celdas vacías consecutivas cuentan como 1 sola
                 #"F77": wids_ventana['e_cred_fechaconcedido'].get_text(), 
                 #"": wids_ventana['e_cred_fechaconcedido'].get_text(), 
                }
    wb = copy.copy(
            xlrd.open_workbook(plantilla, 
                               formatting_info = True, 
                               encoding_override="utf-8")
            )
    s = wb.get_sheet(0)
    tot = len(celfields.keys())
    i = 0.0
    for cell in celfields:
        i += 1
        vpro.set_valor(i/tot, "Rellenando plantilla (xls)...")
        valor = prepare_for_xls(celfields[cell])
        if valor:
            s.write(parseCell(cell)[1],     # row
                    parseCell(cell)[0],     # col
                    valor)    # Espera un iterable
    ## Y por fin guardo y devuelvo la ruta.
    vpro.set_valor(1.0, 
            "Guardando plantilla. Por favor, espere.")
    wb.save(ruta_final)
    vpro.ocultar()
    return ruta_final

def OBSOLETE_convertir_a_xls(fods):
    pathdest = fods + ".xls"
    from lib.simple_odspy.simpleodspy.sodsspreadsheet import SodsSpreadSheet
    from lib.simple_odspy.simpleodspy.sodsxls import SodsXls
    from lib.simple_odspy.simpleodspy.sodsods import SodsOds
    t = SodsSpreadSheet()
    tw = SodsOds(t)
    tw.load(fods)   # load carga el contenido de fods en t. fw no vale para 
    tw = SodsXls(t)    # nada después de eso. Lo reutilizo para xls.
    tw.save(pathdest)
    return pathdest


if __name__ == "__main__":
    p = Presupuestos()

