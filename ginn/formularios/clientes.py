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
## clientes.py - Alta, baja, consulta y mod. de clientes.
###################################################################
## NOTAS:
##  Los vencimientos se introducen y almacenan en la BD como un
##  texto. No se verifica formato ninguno (!). Es tarea de la
##  ventana de facturas el parsear correctamente los vencimientos.
##  El texto debe ser de la forma "30-60", "30-60-90", etc...
## ----------------------------------------------------------------
##
###################################################################
## Changelog:
## 11 de octubre de 2005 -> Inicio
## 11 de octubre de 2005 -> 99% funcional
## 20 de octubre de 2005 -> Añadidos vencimientos por defecto.
## 9 de diciembre de 2005 -> Añadidos campos adicionales (#0000025)
## 9 de diciembre de 2005 -> Añadido IVA por defecto
## 29 de enero de 2005 -> Portado a versión 02.
## 7 de febrero de 2005 -> Añadida la funcionalidad de los pagos
## 13 de febrero de 2005 -> Añadida funcionalidad de contadores
## 4 de julio de 2006 -> CIF como campo obligatorio.
###################################################################
## PLAN: Sería interesante abrir las ventanas de pedidos y produc-
##       tos desde las búsquedas del "expander" «Consultas».
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
import gobject
pygtk.require('2.0')
import gtk, time
from framework import pclases
from informes import geninformes
from formularios.reports import abrir_pdf
from ventana_progreso import VentanaActividad
from formularios import pclase2tv
from lib.myprint import myprint

class Clientes(Ventana):
    def __init__(self, objeto=None, usuario=None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self._objetoreciencreado = None
        self.objeto = objeto
        Ventana.__init__(self, 'clientes.glade', self.objeto, usuario=usuario)
        if self.objeto and not isinstance(self.objeto, pclases.Cliente):
            # Intento su ID o PUID
            try:
                self.objeto = pclases.Cliente.get(int(self.objeto))
            except (pclases.SQLObjectNotFound, TypeError, ValueError):
                try:
                    self.objeto = pclases.getObjetoPUID(self.objeto)
                except ValueError:  # Y si no, intento por nombre
                    try:
                        self.objeto = pclases.Cliente.select(
                            pclases.Cliente.q.nombre.contains(self.objeto),
                            orderBy="id")[0]
                    except IndexError:
                        self.objeto = None
        connections = {'b_salir/clicked': self.salir,
                       'b_pedidos/clicked': self.ver_pedidos,
                       'b_productos/clicked': self.ver_productos,
                       'b_nuevo/clicked': self.crear_nuevo_cliente,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_borrar/clicked': self.borrar,
                       'b_nuevo_contador/clicked': self.crear_nuevo_contador,
                       'cmb_contador/changed': self.seleccionar_contador,
                       'b_tarifa/clicked': self.asignar_tarifa,
                       'b_buscar/clicked': self.buscar_cliente,
                       'b_listado/clicked': self.listado_clientes,
                       'b_listado_riesgos/clicked': self.listado_riesgos,
                       'b_presupuestos/clicked': self.ver_presupuestos,
                       'b_ayuda_formapago/clicked': self.ayuda_forma_pago,
                       'b_add_cuenta/clicked': self.add_cuenta,
                       'b_drop_cuenta/clicked': self.drop_cuenta,
                       'b_por_zona/clicked': self.listar_por_zona,
                       'b_proforma/clicked': self.listar_facturas_proforma,
                       'b_facturas/clicked': self.listar_facturas,
                       'b_productos_proforma/clicked':
                            self.listar_productos_proforma,
                       'notebook1/switch-page': self.actualizar_riesgo,
                       'ch_ign_asegurado/toggled': self.cambiar_ch_asegurado,
                       'ch_ign_concedido/toggled': self.cambiar_ch_concedido,
                       'b_add_obra/clicked': self.add_obra,
                       'b_drop_obra/clicked': self.drop_obra,
                       'b_add_contacto/clicked': self.add_contacto,
                       'b_drop_contacto/clicked': self.drop_contacto,
                       'b_unificar_obras/clicked': self.unificar_obras,
                       'b_globalizar_contacto/clicked':
                                                   self.globalizar_contacto,
                       'b_copiar_correspondencia/clicked':
                                                   self.copiar_correspondencia,
                       'b_copiar_fiscal/clicked':  self.copiar_fiscal,
                       'b_next/clicked':           self.siguiente,
                       'b_back/clicked':           self.anterior
                      }
        self.inicializar_ventana()
        if not self.objeto:
            self.ir_a_primero()
        else:
            self.ir_a(self.objeto, deep_refresh=False)
        self.add_connections(connections)
        gtk.main()

    def anterior(self, boton=None):
        if self.objeto:
            orden = utils.combo_get_value(self.wids['cb_orden'])
            if orden == "Orden cronológico":
                clientes = pclases.Cliente.select(
                        pclases.Cliente.q.id < self.objeto.id,
                        orderBy="-id")
            elif orden == "Orden alfabético":
                clientes = pclases.Cliente.select(
                        pclases.Cliente.q.nombre < self.objeto.nombre,
                        orderBy="-nombre")
            try:
                anterior = clientes[0]
            except IndexError:
                anterior = None
            if anterior:
                self.objeto = anterior
                self.actualizar_ventana()
            else:
                utils.dialogo_info(titulo="NO HAY MÁS CLIENTES",
                        texto="No hay clientes anteriores al actual.",
                        padre=self.wids['ventana'])

    def siguiente(self, boton=None):
        if self.objeto:
            orden = utils.combo_get_value(self.wids['cb_orden'])
            if orden == "Orden cronológico":
                clientes = pclases.Cliente.select(
                        pclases.Cliente.q.id > self.objeto.id,
                        orderBy="id")
            elif orden == "Orden alfabético":
                clientes = pclases.Cliente.select(
                        pclases.Cliente.q.nombre > self.objeto.nombre,
                        orderBy="nombre")
            try:
                siguiente = clientes[0]
            except IndexError:
                siguiente = None
            if siguiente:
                self.objeto = siguiente
                self.actualizar_ventana()
            else:
                utils.dialogo_info(titulo="NO HAY MÁS CLIENTES",
                        texto="No hay clientes posteriores al actual.",
                        padre=self.wids['ventana'])

    def copiar_correspondencia(self, boton=None):
        """Copia al portapapeles la dirección de correspondencia del cliente
        en pantalla.
        """
        direccion = "\n".join((self.objeto.nombre,
                               self.objeto.direccion,
                               self.objeto.ciudad,
                               self.objeto.cp
                                 and self.objeto.cp+" "+self.objeto.provincia
                                 or self.objeto.provincia,
                               self.objeto.pais))
        copy_to_clipboard(direccion)

    def copiar_fiscal(self, boton=None):
        """Copia al portapapeles la dirección fiscal completa del cliente
        en pantalla.
        """
        direccion = "\n".join((self.objeto.nombref,
                               self.objeto.direccionfacturacion,
                               self.objeto.ciudadfacturacion,
                               self.objeto.cpfacturacion
                                 and self.objeto.cpfacturacion +
                                    " " + self.objeto.provinciafacturacion
                                 or self.objeto.provinciafacturacion,
                               self.objeto.paisfacturacion))
        copy_to_clipboard(direccion)

    def globalizar_contacto(self, boton):
        """
        Añade los contactos seleccionados a todas las obras del cliente.
        """
        sel = self.wids['tv_contactos'].get_selection()
        model, iters = sel.get_selected_rows()
        if not iters:
            utils.dialogo_info(titulo="SELECCIONE CONTACTO",
                texto="Debe seleccionar al menos un contacto \n"
                        "para hacerlo global a todas las obras \n"
                        "del cliente.",
                padre=self.wids['ventana'])
        else:
            for itr in iters:
                copiadas = 0
                idcontacto = model[itr][-1]
                contacto = pclases.Contacto.get(idcontacto)
                for obra in self.objeto.obras:
                    if contacto not in obra.contactos:
                        obra.addContacto(contacto)
                        copiadas += 1
            utils.dialogo_info(titulo="CONTACTO COPIADO",
                texto="El contacto se copió a %d obras." % copiadas,
                padre=self.wids['ventana'])
            # No hace falta recargar. Cuando mueva el cursor lo verá, y en la
            # obra actual ya estaba, así que lo sigue viendo.

    def unificar_obras(self, boton):
        """
        Une dos o varias obras en una sola.
        Primero elige, de entre todas las obras seleccionadas, cuál es la que
        tiene los datos correctos. Después, para el resto de obras, agrega
        sus contactos, facturas, pedidos y abonos a la obra seleccionada -el
        cliente ya lo tiene, porque por eso ha salido en esta ventana-.
        Acaba desligando todos esos datos de las obras y eliminándolas (si
        no tiene más clientes esa obra).
        """
        sel = self.wids['tv_obras'].get_selection()
        model, iters = sel.get_selected_rows()
        if not iters or len(iters) < 2:
            utils.dialogo_info(titulo="SELECCIONE OBRA",
                texto="Debe seleccionar dos o más obras.",
                padre=self.wids['ventana'])
        else:
            obras = [pclases.Obra.get(model[itr][-1]) for itr in iters]
            ops = [(o.id, o.get_str_obra()) for o in obras]
            buena = utils.dialogo_combo(titulo="SELECCIONE OBRA",
                texto="Seleccione la obra base.\n"\
                      "El resto de obras se eliminarán y sus facturas,\n"\
                      "contactos, pedidos y abonos pasarán a la que \n"\
                      "seleccione en el desplegable inferior.",
                padre=self.wids['ventana'],
                ops=ops)
            if not buena:
                return
            buena = pclases.Obra.get(buena)
            malas = [o for o in obras if o != buena]
            for mala in malas:
                for contacto in mala.contactos:
                    if not contacto.existe_en(buena):
                        buena.addContacto(contacto)
                    mala.removeContacto(contacto)
                for pedido in mala.pedidosVenta:
                    pedido.obra = buena
                for factura in mala.facturasVenta:
                    factura.obra = buena
                for abono in mala.abonos:
                    abono.obra = buena
                mala.removeCliente(self.objeto)
                try:
                    mala.destroy(ventana=__file__)
                except: # Queda algún cliente relacionado con la obra. No
                        # la termino de eliminar.
                    pass
            self.rellenar_obras()

    def add_contacto(self, boton):
        """
        Añade un contacto al cliente a través de la(s) obra(s) seleccionada en
        el TreeView de obras. Si no hay seleccionada ninguna mostrará un
        mensaje al usuario para que lo haga.
        """
        sel = self.wids['tv_obras'].get_selection()
        model, iters = sel.get_selected_rows()
        if not iters:
            utils.dialogo_info(titulo="SELECCIONE OBRA",
                texto="Debe seleccionar al menos una obra con la que\n"
                      "relacionar el nuevo contacto.",
                padre=self.wids['ventana'])
        else:
            nombre = utils.dialogo_entrada(titulo = "NOMBRE",
                texto = "Introduzca el nombre -sin apellidos- del "
                        "nuevo contacto:",
                padre = self.wids['ventana'])
            if nombre:
                apellidos = utils.dialogo_entrada(titulo = "APELLIDOS",
                    texto = "Introduzca ahora los apellidos:",
                    padre = self.wids['ventana'])
                if apellidos != None:
                    c = self.buscar_contacto_existente(nombre, apellidos)
                    if not c:
                        c = pclases.Contacto(nombre = nombre,
                                             apellidos = apellidos)
                        pclases.Auditoria.nuevo(c, self.usuario, __file__)
                    for itr in iters:
                        idobra = model[itr][-1]
                        obra = pclases.Obra.get(idobra)
                        c.addObra(obra)
                    self.rellenar_contactos()

    def buscar_contacto_existente(self, _nombre, _apellidos):
        """
        Busca un contacto con los nombres y apellidos recibidos. Si lo
        encuentra lo sugiere y devuelve el objeto contacto. En caso contrario
        devuelve None.
        """
        from lib import spelling
        nombres_bd = []
        apellidos_bd = []
        for c in pclases.Contacto.select():
            for n in c.nombre.split():
                nombres_bd.append(n.lower())
            for a in c.apellidos.split():
                apellidos_bd.append(a.lower())
        corrnombre = spelling.SpellCorrector(" ".join(nombres_bd))
        corrapellidos = spelling.SpellCorrector(" ".join(apellidos_bd))
        nombres = [n.lower() for n in _nombre.split()]
        apellidos = [a.lower() for a in _apellidos.split()]
        nomcorregido = []
        apecorregido = []
        for nombre in nombres:
            sugerencia = corrnombre.correct(nombre)
            nomcorregido.append(sugerencia)
        for apellido in apellidos:
            sugerencia = corrapellidos.correct(apellido)
            apecorregido.append(sugerencia)
        nombre = " ".join(nomcorregido)
        apellidos = " ".join(apecorregido)
        #contacto = pclases.Contacto.select(pclases.AND(
        #                pclases.Contacto.q.nombre == nombre,
        #                pclases.Contacto.q.apellidos == apellidos))
        contacto = pclases.Contacto.select("""
            nombre ILIKE '%s' AND apellidos ILIKE '%s' """
            % (nombre, apellidos))
        if contacto.count() == 0:
            res = None
        else:
            res = contacto[0]
            if not utils.dialogo(titulo = "BUSCAR CONTACTO",
                    texto = "¿El contacto que está buscando es:\n"
                        "%s %s\nCargo: %s\nTeléfono:%s?" % (
                        res.nombre, res.apellidos,
                        res.cargo and res.cargo
                            or '"sin cargo definido"',
                        res.telefono and res.telefono
                            or '"sin teléfono definido"'),
                    padre = self.wids['ventana']):
                res = None
        return res

    def drop_contacto(self, boton):
        """
        Elimina el contacto seleccionado, desvinculándolo previamente de
        cuantas obras tuviera.
        """
        sel = self.wids['tv_contactos'].get_selection()
        model, iters = sel.get_selected_rows()
        if not iters:
            return
        res = utils.dialogo(titulo = "ELIMINAR CONTACTO",
            texto = "¿Desea eliminar el contacto por completo?\n"
                "\nSi pulsa «Sí» se eliminará el contacto.\n"
                "Si pulsa «No» se desvinculará de la obra seleccionada\n"
                "pero no se eliminará el contacto de otras posibles obras.\n"
                "Si pulsa «Cancelar» no se hará nada.",
            padre = self.wids['ventana'],
            cancelar = True,
            defecto = gtk.RESPONSE_CANCEL,
            bloq_temp = [gtk.RESPONSE_YES, gtk.RESPONSE_NO])
        if res != gtk.RESPONSE_CANCEL:
            for itr in iters:
                ide = model[itr][-1]
                c = pclases.Contacto.get(ide)
                if res == True:
                    for o in c.obras:
                        o.removeContacto(c)
                    c.destroy(ventana = __file__)
                else:
                    sel = self.wids['tv_obras'].get_selection()
                    modelobras, itersobras = sel.get_selected_rows()
                    for iterobras in itersobras:
                        idobra = modelobras[iterobras][-1]
                        obra = pclases.Obra.get(idobra)
                        obra.removeContacto(c)
                        # No lo borro aunque no le queden obras por si lo
                        # busca en el futuro.
            self.rellenar_contactos()

    def add_obra(self, boton):
        """
        Añade una nueva obra al cliente.
        """
        nombre = utils.dialogo_entrada(titulo = "NOMBRE DE OBRA",
            texto = "Introduzca el nombre de la nueva obra:",
            padre = self.wids['ventana'])
        if nombre:
            obra = pclases.Obra(nombre = nombre,
                                direccion = "",
                                cp = "",
                                ciudad = "",
                                provincia = "",
                                fechainicio = None,
                                fechafin = None,
                                observaciones = "",
                                pais = "",
                                generica = False)
            pclases.Auditoria.nuevo(obra, self.usuario, __file__)
            obra.addCliente(self.objeto)
            self.rellenar_obras()

    def drop_obra(self, boton):
        """
        Elimina la obra seleccionada pero no sus contactos.
        """
        sel = self.wids['tv_obras'].get_selection()
        model, iters = sel.get_selected_rows()
        se_borro_algo = False
        for itr in iters:
            ide = model[itr][-1]
            obra = pclases.Obra.get(ide)
            obra.sync()
            facturas_del_cliente = [f for f in obra.facturasVenta
                                    if f.cliente == self.objeto]
            pedidos_del_cliente = [p for p in obra.pedidosVenta
                                   if p.cliente == self.objeto]
            if facturas_del_cliente or pedidos_del_cliente:
                strfras = ", ".join([f.numfactura for f in facturas_del_cliente])
                strfras += "\n"
                strfras += ", ".join([p.numpedido for p in pedidos_del_cliente])
                ans = utils.dialogo(titulo = "OBRA IMPLICADA EN FACTURACIÓN",
                    texto = "La obra está relacionada con los siguientes "\
                        "pedidos y facturas:\n%s\n\n"
                        "Para eliminar esta obra necesitará cambiar estas\n"
                        "facturas. ¿Desea asignar las facturas a otra obra?"%(
                            strfras),
                    padre = self.wids['ventana'])
                if ans:
                    id_nueva_obra = utils.dialogo_combo(
                        titulo = "SELECCIONE OBRA",
                        texto = "Seleccione una obra del desplegable.\n"
                            "Todas las facturas anteriores se le asignarán\n"
                            "a menos que estén bloqueadas y no tenga \n"
                            "suficientes permisos.",
                        padre = self.wids['ventana'],
                        ops = [(o.id, o.nombre) for o
                               in pclases.Obra.select(orderBy = "nombre")])
                    if id_nueva_obra:
                        fras_o_peds = (len(facturas_del_cliente)
                                       + len(pedidos_del_cliente))
                        fropeds_cambiados = 0
                        nueva_obra = pclases.Obra.get(id_nueva_obra)
                        for froped in (facturas_del_cliente
                                       + pedidos_del_cliente):
                            try:
                                bloqueada = froped.bloqueada
                            except AttributeError:
                                bloqueada = froped.bloqueado
                            if (not bloqueada
                                or (self.usuario and self.usuario.nivel <= 3)):
                                froped.obra = nueva_obra
                                froped.sync()
                                fropeds_cambiados += 1
                        texto_dialogo = "Se reasignaron %d de %d facturas"\
                                        " y pedidos." % (
                            fropeds_cambiados, fras_o_peds)
                        if fropeds_cambiados == fras_o_peds:
                            texto_dialogo += \
                                "\nTrate ahora de eliminar la obra."
                        else:
                            texto_dialogo += \
                                "\nDebe corregir manualmente el resto de "\
                                "facturas."
                        utils.dialogo_info(titulo="OPERACIÓN FINALIZADA",
                                           texto=texto_dialogo,
                                           padre=self.wids['ventana'])
            else:
                obra.removeCliente(self.objeto)
                se_borro_algo = True
                obra.sync()
                if not obra.clientes:   # Si esta obra no pertenece a ningún
                    # cliente más, entonces trato de eliminarla por completo.
                    # TODO: Y aún así hay obras huérfanas en la base de datos.
                    contactos = obra.contactos[:]
                    for c in contactos:
                        obra.removeContacto(c)
                    try:
                        obra.destroy(ventana=__file__)
                    except Exception, msg:
                        obra.addCliente(self.objeto)
                        for c in contactos:
                            obra.addContacto(c)
                        utils.dialogo_info(titulo="OBRA NO SE PUDO BORRAR",
                            texto="No fue posible eliminar la obra.\n\n"
                                  "Información de depuración:\n%s" % msg,
                            padre=self.wids['ventana'])
                    else:
                        se_borro_algo = True
        if se_borro_algo:
            self.rellenar_obras()

    def rellenar_obras(self):
        """
        Rellena la tabla de obras con las obras del cliente.
        """
        self.wids['tv_obras'].get_selection().disconnect(self.hndlr_obras)
        if self.objeto:
            obras = pclases.SQLtuple(self.objeto.obras)
            self.tvobras.rellenar_tabla(objetos = obras)
                #filtro = lambda o: self.objeto in o.clientes)
        # Vuelvo a conectar el callback de los contactos.
        self.hndlr_obras = self.wids['tv_obras'].get_selection().connect(
                                            "changed", self.rellenar_contactos)

    def rellenar_contactos(self, *args, **kw):
        """
        Rellena la tabla de contactos en función de las obras seleccionadas
        en el primer TreeView.
        """
        if self.objeto:
            ##################################################################
            def filtro_pertenece_a_obra(objeto, obras, contactos_ya_puestos):
                """
                Devuelve True si alguna de las obras del objeto está en la
                lista recibida.
                """
                res = False
                for obra in objeto.obras:
                    if (obra in obras
                        and objeto.id not in contactos_ya_puestos):
                        res = True
                        break
                return res
            ##################################################################
            selection = self.wids['tv_obras'].get_selection()
            model,iters = selection.get_selected_rows()
            if not model:
                return
            if not iters:
                model = self.wids['tv_obras'].get_model()
                iters = []
                itr = model.get_iter_first()
                while itr:
                    iters.append(itr)
                    itr = model.iter_next(itr)
            obras = []
            contactos_ya_puestos = []
            primera_obra = True
            for itr in iters:
                idobra = model[itr][-1]
                obra = pclases.Obra.get(idobra)
                obras.append(obra)
                contactos_de_la_obra = pclases.SQLtuple(obra.contactos)
                self.tvcontactos.rellenar_tabla(
                                #filtro = filtro_pertenece_a_obra,
                                filtro = lambda *args, **kw: True,
                                padre = self.wids['ventana'],
                                limpiar_model = primera_obra,
                                objetos = contactos_de_la_obra, 
                                obras = obras,
                                contactos_ya_puestos = contactos_ya_puestos)
                contactos_ya_puestos += [c.id for c in obra.contactos]
                primera_obra = False

    def cambiar_ch_asegurado(self, ch):
        self.wids['e_riesgoAsegurado'].set_sensitive(not ch.get_active())
        if ch.get_active():
            self.wids['e_riesgoAsegurado'].set_text(utils.float2str(-1))
        else:
            self.wids['e_riesgoAsegurado'].set_text(utils.float2str(0))

    def cambiar_ch_concedido(self, ch):
        self.wids['e_riesgoConcedido'].set_sensitive(not ch.get_active())
        if ch.get_active():
            self.wids['e_riesgoConcedido'].set_text(utils.float2str(-1))
        else:
            self.wids['e_riesgoConcedido'].set_text(utils.float2str(0))

    def actualizar_riesgo(self, nb, ptr_pag, num_pag):
        """
        Si el notebook ha cambiado la página a la de gestión de riesgos,
        actualiza y muestra la información.
        Así evito cargarla desde el principio y ralentizar la ventana completa
        en espera de esos datos.
        OJO: Nada de prefacturas. Solo facturas oficiales.
        """
        if num_pag == 4:
            self.rellenar_riesgo_campos_objeto()
            if not(#self.wids['ch_ign_asegurado'].get_active() and
                   self.wids['ch_ign_concedido'].get_active()):
                self.rellenar_riesgo_campos_calculados()
        elif num_pag == 5:
            self.rellenar_obras()
            # La primera vez relleno todos los contactos. Las siguientes será
            # como callback al seleccionar una obra concreta.
            self.rellenar_contactos()

    def rellenar_riesgo_campos_objeto(self):
        self.wids['ch_ign_concedido'].set_active(self.objeto.riesgoConcedido<0)
        self.wids['ch_ign_asegurado'].set_active(self.objeto.riesgoAsegurado<0)
        self.wids['e_riesgoConcedido'].set_text(utils.float2str(
            self.objeto.riesgoConcedido))
        self.wids['e_riesgoAsegurado'].set_text(utils.float2str(
            self.objeto.riesgoAsegurado))
        # Esto lo machacará el rellenar_...calculados si fuera oportuno.
        self.wids['e_credito'].set_text("N/A")
        self.wids['tv_facturas'].get_model().clear()
        self.wids['tv_pdte_doc'].get_model().clear()
        self.wids['tv_no_vencidas'].get_model().clear()
        self.wids['tv_impagadas'].get_model().clear()
        self.wids['tv_cobradas'].get_model().clear()
        self.wids['tv_abonos'].get_model().clear()

    def rellenar_tabla_facturas(self, nombre_tv, nombre_func_fras,
                                ventana_progreso, nombre_entry_total = None,
                                cache = {}, ignorar_total = False,
                                nombre_func_importe = "calcular_importe_total"
                               ):
        try:
            model = self.wids[nombre_tv].get_model()
            model.clear()
        except (AttributeError, TypeError):
            # Será None. No hay que rellenar tabla.
            model = None
        cliente = self.objeto
        fras = getattr(cliente, nombre_func_fras)(cache = cache)
        total = 0.0
        for f in fras:
            if not ignorar_total:
                calcular_importe = getattr(f, nombre_func_importe)
                importe = calcular_importe()
            else:
                importe = 0.0
            total += importe
            if model:
                model.append((f.numfactura,
                              utils.str_fecha(f.fecha),
                              # utils.float2str(f.calcular_importe_total()),
                              f.get_puid()))
            ventana_progreso.mover()
        if nombre_entry_total:
            self.wids[nombre_entry_total].set_text(utils.float2str(total))
        return total

    def rellenar_pdte_doc(self, ventana_progreso, cache = {}):
        total = self.rellenar_tabla_facturas("tv_pdte_doc",
                                             "get_facturas_sin_doc_pago",
                                             ventana_progreso,
                                             "e_pdte_doc",
                                             cache,
                                             nombre_func_importe =
                                              "calcular_importe_no_documentado"
                                            )
        return total

    def rellenar_no_vencidas(self, ventana_progreso, cache = {}):
        total = self.rellenar_tabla_facturas('tv_no_vencidas',
                                             "get_facturas_doc_no_vencidas",
                                             ventana_progreso,
                                             "e_no_vencidas",
                                             cache)
        return total

    def rellenar_impagadas(self, ventana_progreso, cache = {}):
        total = self.rellenar_tabla_facturas('tv_impagadas',
                                             "get_facturas_impagadas",
                                             ventana_progreso,
                                             "e_impagadas",
                                             cache)
        return total

    def rellenar_pdte_abonar(self, ventana_progreso, cache = {}):
        total = self.rellenar_tabla_facturas(None,
                                             "get_facturas_no_abonadas",
                                             ventana_progreso,
                                             "e_no_abonadas",
                                             cache)
        return total

    def rellenar_cobradas(self, ventana_progreso, cache = {},
                          ignorar_total = True):
        total = self.rellenar_tabla_facturas('tv_cobradas',
                                             "get_facturas_cobradas",
                                             ventana_progreso,
                                             cache = cache,
                                             ignorar_total = ignorar_total)
        return total

    def rellenar_abonos(self, ventana_progreso, cache = {}):
        total = self.rellenar_tabla_facturas('tv_abonos',
                                             "get_abonos",
                                             ventana_progreso,
                                             cache = cache)
        return total

    def rellenar_facturas_y_abonos(self, ventana_progreso, cache = {}):
        model = self.wids['tv_facturas'].get_model()
        model.clear()
        cliente = self.objeto
        facturas_y_abonos = cliente.get_facturas_y_abonos()
        for f in facturas_y_abonos:
            str_estado = f.get_str_estado(cache = cache)
            model.append((f.numfactura,
                          utils.str_fecha(f.fecha),
                          utils.float2str(f.calcular_importe_total()),
                          utils.float2str(f.calcular_importe_no_documentado()),
                          utils.float2str(f.calcular_importe_documentado()),
                          utils.float2str(f.calcular_importe_vencido()),
                          utils.float2str(f.calcular_importe_cobrado()),
                          str_estado,
                          f.obra and f.obra.nombre or "Sin obra relacionada",
                          f.puid))
            ventana_progreso.mover()

    def rellenar_riesgo_campos_calculados(self):
        if pclases.DEBUG:
            antes = time.time()
            myprint("0.- clientes.py::rellenar_riesgo_campos_calculados -> "
                    "Düsseldorf")
        self.wids['ventana'].window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        vpro = VentanaActividad(texto = "Esta operación puede tardar unos "
                                        "minutos...",
                                padre = self.wids['ventana'])
        if pclases.DEBUG:
            myprint("1.- clientes.py::rellenar_riesgo_campos_calculados ->",
                    time.time() - antes)
        global seguir
        seguir = True
        def mover_progreso(vpro):
            global seguir
            vpro.mover()
            while gtk.events_pending(): gtk.main_iteration(False)
            return seguir
        if pclases.DEBUG:
            myprint("2.- clientes.py::rellenar_riesgo_campos_calculados ->",
                    time.time() - antes)
        gobject.timeout_add(50, mover_progreso, vpro,
                            priority = gobject.PRIORITY_HIGH_IDLE + 20)
        vpro.mostrar()
        while gtk.events_pending(): gtk.main_iteration(False)
        if pclases.DEBUG:
            myprint("2.5.- clientes.py::rellenar_riesgo_campos_calculados ->",
                    time.time() - antes)
        # XXX ¡OPTIMIZACION! ¡Puños fuera!
        cache = {}
        for f in self.objeto.get_facturas_y_abonos():
            vpro.mover()
            cache[f.puid] = f.get_estado()
        # XXX
        if pclases.DEBUG:
            myprint("3.- clientes.py::rellenar_riesgo_campos_calculados ->",
                    time.time() - antes)
        # Nuevos TreeViews de facturas pendientes:
        sin_documentar = self.rellenar_pdte_doc(vpro, cache)
        if pclases.DEBUG:
            myprint("4.- clientes.py::rellenar_riesgo_campos_calculados ->",
                    time.time() - antes)
        sin_vencer = self.rellenar_no_vencidas(vpro, cache)
        if pclases.DEBUG:
            myprint("5.- clientes.py::rellenar_riesgo_campos_calculados ->",
                    time.time() - antes)
        impagado = self.rellenar_impagadas(vpro, cache)
        if pclases.DEBUG:
            myprint("6.- clientes.py::rellenar_riesgo_campos_calculados ->",
                    time.time() - antes)
        #cobrado = self.rellenar_cobradas(vpro, cache)
        self.rellenar_cobradas(vpro, cache, ignorar_total = True)
        if pclases.DEBUG:
            myprint("7.- clientes.py::rellenar_riesgo_campos_calculados ->",
                    time.time() - antes)
        self.rellenar_facturas_y_abonos(vpro, cache)
        self.rellenar_abonos(vpro, cache)
        if pclases.DEBUG:
            myprint("8.- clientes.py::rellenar_riesgo_campos_calculados ->",
                    time.time() - antes)
        credito = self.objeto.calcular_credito_disponible(impagado,
                                                          sin_documentar,
                                                          sin_vencer)
        if pclases.DEBUG:
            myprint("9.- clientes.py::rellenar_riesgo_campos_calculados ->",
                    time.time() - antes)
        self.wids['e_credito'].set_text(utils.float2str(credito))
        if credito <= 0:
            self.wids['e_credito'].modify_text(gtk.STATE_NORMAL,
                self.wids['e_credito'].get_colormap().alloc_color("red"))
        else:
            self.wids['e_credito'].modify_text(gtk.STATE_NORMAL, None)
        if pclases.DEBUG:
            myprint("10.- clientes.py::rellenar_riesgo_campos_calculados ->",
                    time.time() - antes)
        impagado = self.rellenar_pdte_abonar(vpro, cache)
        if pclases.DEBUG:
            myprint("11.- clientes.py::rellenar_riesgo_campos_calculados ->",
                    time.time() - antes)
        self.wids['rating'].set_value(self.objeto.calcular_rating())
        if pclases.DEBUG:
            myprint("12.- clientes.py::rellenar_riesgo_campos_calculados ->",
                    time.time() - antes)
        seguir = False
        vpro.ocultar()
        self.wids['ventana'].window.set_cursor(None)
        if pclases.DEBUG:
            myprint("13.- clientes.py::rellenar_riesgo_campos_calculados ->",
                    time.time() - antes)

    def listar_facturas_proforma(self, boton):
        """
        Lista todas las facturas proforma del cliente en un diálogo de
        resultados de búsqueda.
        """
        if self.objeto:
            proformas = pclases.Prefactura.select(
                pclases.Prefactura.q.clienteID == self.objeto.id,
                orderBy = "fecha")
            fras = [(f.id,
                     f.numfactura,
                     utils.str_fecha(f.fecha),
                     utils.float2str(f.calcular_importe_total()),
                     f.bloqueada)
                    for f in proformas]
            fra = utils.dialogo_resultado(fras,
                                          titulo = 'FACTURAS PROFORMA',
                                          cabeceras = ('ID',
                                                       'Número',
                                                       'Fecha',
                                                       'Total',
                                                       'Bloqueada'),
                                          padre = self.wids['ventana'])
            if fra and fra > 0:
                try:
                    fra = pclases.Prefactura.get(fra)
                except:
                    return
                from formularios import prefacturas
                v = prefacturas.Prefacturas(objeto=fra, usuario=self.usuario)

    def listar_facturas(self, boton):
        """
        Lista todas las facturas del cliente en un diálogo de
        resultados de búsqueda.
        """
        if self.objeto:
            facturas = pclases.FacturaVenta.select(
                pclases.FacturaVenta.q.clienteID == self.objeto.id,
                orderBy = "fecha")
            fras = [(f.id,
                     f.numfactura,
                     utils.str_fecha(f.fecha),
                     utils.float2str(f.calcular_importe_total()),
                     utils.float2str(f.calcular_pendiente_cobro()),
                     f.bloqueada)
                    for f in facturas]
            fra = utils.dialogo_resultado(fras,
                        titulo = 'FACTURAS DE %s' % self.objeto.nombre,
                        cabeceras = ('ID',
                                     'Número',
                                     'Fecha',
                                     'Total (IVA incl.)',
                                     'Pendiente de cobro',
                                     'Bloqueada'),
                        padre = self.wids['ventana'])
            if fra and fra > 0:
                try:
                    fra = pclases.FacturaVenta.get(fra)
                except:
                    return
                from formularios import facturas_venta
                v = facturas_venta.FacturasVenta(objeto = fra,
                                                 usuario = self.usuario)

    def listar_productos_proforma(self, boton):
        """
        Muestra los productos comprados en prefacturas, junto con sus totales,
        y abre el seleccionado en la ventana correspondiente.
        """
        if self.objeto:
            proformas = pclases.Prefactura.select(
                pclases.Prefactura.q.clienteID == self.objeto.id,
                orderBy = "fecha")
            productos = {}
            for fra in proformas:
                for ldv in fra.lineasDeVenta:
                    producto = ldv.producto
                    if producto not in productos:
                        productos[producto] = {
                                        "cantidad": ldv.cantidad,
                                        "subtotal": ldv.calcular_subtotal(),
                                        "beneficio": ldv.calcular_beneficio()}
                    else:
                        productos[producto]["cantidad"] += ldv.cantidad
                        productos[producto]["subtotal"] \
                            += ldv.calcular_subtotal()
                        productos[producto]["beneficio"] \
                            += ldv.calcular_beneficio()
            pros = [("%s:%d" % (
                        isinstance(p, pclases.ProductoVenta) and "PV" or "PC",
                        p.id),
                     p.codigo,
                     p.descripcion,
                     utils.float2str(productos[p]["cantidad"]),
                     utils.float2str(productos[p]["subtotal"]),
                     utils.float2str(productos[p]["beneficio"]),
                    )
                    for p in productos]
            pro = utils.dialogo_resultado(pros,
                                    titulo = 'PRODUCTOS EN FACTURAS PROFORMA',
                                    cabeceras = ('ID',
                                                 'Código',
                                                 'Descripción',
                                                 'Cantidad total',
                                                 'Importe total',
                                                 'Beneficio calculado'),
                                    padre = self.wids['ventana'])
            if pro and pro > 0:
                idproducto = pro
                try:
                    if "PV" in idproducto:
                        producto = pclases.ProductoVenta.get(
                                        idproducto.split(":")[1])
                        if producto.es_rollo():
                            from formularios import productos_de_venta_rollos as pdvr
                            ventana_producto = pdvr.ProductosDeVentaRollos(  # @UnusedVariable
                                            producto, usuario = self.usuario)
                        elif producto.es_bala() or producto.es_bigbag():
                            from formularios import productos_de_venta_balas as pdvb
                            ventana_producto = pdvb.ProductosDeVentaBalas(  # @UnusedVariable
                                            producto, usuario = self.usuario)
                    elif "PC" in idproducto:
                        producto = pclases.ProductoCompra.get(
                                        idproducto.split(":")[1])
                        from formularios import productos_compra
                        ventana_producto = productos_compra.ProductosCompra(  # @UnusedVariable
                                            producto, usuario = self.usuario)
                except:
                    pass

    def abrir_pedido(self, tv):
        """
        Abre una ventana con el pedido marcado en el TreeView recibido.
        """
        model, itr = tv.get_selection().get_selected()
        if itr != None:
            ide = model[itr][0]
            pedido = pclases.PedidoVenta.get(ide)
            from formularios import pedidos_de_venta
            ventana = pedidos_de_venta.PedidosDeVenta(objeto = pedido,  # @UnusedVariable
                                                      usuario = self.usuario)

    def ayuda_forma_pago(self, boton):
        """
        Muestra un texto de ayuda.
        """
        utils.dialogo_info(titulo = "FORMA DE PAGO",
                           texto = """
        D.F.F.: Días a partir de la fecha de factura.
        D.F.R.: Días a partir de la fecha de recepción de la factura (en la
                práctica es similar a D.F.F.).
        D.U.D.M.F.F.: Días a partir del último días del mes de la fecha de
                factura.
        Si usa otras siglas se ignorarán, teniendo en cuenta solo los días
        indicados en número. Si los vencimientos son múltiples (por ejemplo,
        a «30, 60 y 120 días fecha factura», puede usar guiones, comas o
        espacios como separación: «30-60-120 D.F.F.».
                           """,
                           padre = self.wids['ventana'])

    def listado_clientes(self, boton):
        """
        Muestra un listado de todos los clientes
        habilitados.
        """
        campos = [(0, "nombre", "Nombre"),
                  (1, ["pais", "provincia", "ciudad", "cp", "nombre"], "Ciudad y provincia"),
                    # BUG: En SQL Barcelona < ALICANTE < BARCELONA
                  (2, ["formadepago", "nombre"], "Forma de pago")]
        orden = utils.dialogo_combo(
                  titulo = "ORDEN DEL LISTADO",
                  texto = "Seleccione el campo por el que ordenar el informe.",
                  ops = [(c[0], c[2]) for c in campos],
                  padre = self.wids['ventana'],
                  valor_por_defecto = 0)
        if orden != None:
            clientes = pclases.Cliente.select(
                        pclases.Cliente.q.inhabilitado == False,
                        orderBy = campos[orden][1])
            listado = geninformes.listado_clientes(clientes)
            abrir_pdf(listado)

    def listado_riesgos(self, boton):
        """
        Muestra un listado de todos los clientes
        habilitados con los riesgos asegurados y concedidos.
        """
        campos = [(0, "nombre", "Nombre"),
                  (1, ["pais", "provincia", "ciudad", "cp", "nombre"], "Ciudad y provincia"),
                    # BUG: En SQL Barcelona < ALICANTE < BARCELONA
                  (2, ["formadepago", "nombre"], "Forma de pago")]
        orden = utils.dialogo_combo(
                  titulo = "ORDEN DEL LISTADO",
                  texto = "Seleccione el campo por el que ordenar el informe.",
                  ops = [(c[0], c[2]) for c in campos],
                  padre = self.wids['ventana'],
                  valor_por_defecto = 0)
        if orden != None:
            clientes = pclases.Cliente.select(
                        pclases.Cliente.q.inhabilitado == False,
                        orderBy = campos[orden][1])
            listado = geninformes.listado_clientes_solo_riesgos(clientes)
            abrir_pdf(listado)

    def listar_por_zona(self, boton):
        """
        Muestra un listado de todos los clientes
        habilitados.
        """
        ciudades = [c.ciudad for c in pclases.Cliente.select()]
        ciudades = utils.unificar(ciudades)
        ciudades.sort()
        opciones = zip(range(len(ciudades)), ciudades)
        ciudad = utils.dialogo_combo(titulo = "SELECCIONE CIUDAD",
                                     texto = "Seleccione una ciudad del desplegable.",
                                     ops = opciones,
                                     padre = self.wids['ventana'])
        if ciudad != None and isinstance(ciudad, int):
            clientes = pclases.Cliente.select(pclases.AND(pclases.Cliente.q.inhabilitado == False,
                                                          pclases.Cliente.q.ciudad == opciones[ciudad][1]),
                                              orderBy = "nombre")
            listado = geninformes.listado_clientes(clientes)
            abrir_pdf(listado)

    # --------------- Funciones auxiliares ------------------------------
    def es_diferente(self):
        """
        Devuelve True si la información en pantalla es distinta a la
        del objeto en memoria.
        """
        cliente = self.objeto
        if cliente == None: return False    # Si no hay cliente activo, 
                    # devuelvo que no hay cambio respecto a la ventana
        condicion = True
        lista = [cli for cli in cliente.sqlmeta.columnList
                    if cli.name!='tarifaID'
                        and cli.name != 'contadorID'
                        and cli.name != 'formadepago'
                        and cli.name != 'formaPagoFija'
                        and cli.name != "clienteID"
                        and cli.name != "porcentaje"
                        and cli.name != "validacionManual"
                        and cli.name != "enviarCorreoAlbaran"
                        and cli.name != "enviarCorreoFactura"
                        and cli.name != "enviarCorreoPacking"
                        and cli.name != "proveedorID"
                        and cli.name != "cuentaOrigenID"
                        and cli.name != "riesgoConcedido"
                        and cli.name != "riesgoAsegurado"
                        and cli.name != "tipoDeClienteID"
                        and cli.name != "copiasFactura"]
            # Quito la columna tarifa que no se muestra en el formulario
            # de clientes
        for c in lista:
            textobj = str(eval('cliente.%s' % c.name))
            # NOTA: El str es para comparar todo como texto (para evitar una
            #       comparación especial del campo IVA, que es el único
            #       numérico).
            if c.name == 'iva':
                try:
                    ivaparseado = utils.parse_porcentaje(
                        self.wids['e_iva'].get_text(), fraccion = True)
                except ValueError:
                    ivaparseado = 0
                textven = str(ivaparseado)
            else:
                textven = self.leer_valor(self.wids['e_%s' % c.name])
            if isinstance(textven, bool):
                if (c.name == "packingListConCodigo"
                    or c.name == "facturarConAlbaran"):
                    condicion = condicion and textven == getattr(cliente,
                                                                 c.name)
                else:
                    condicion = condicion and textven == getattr(cliente,
                                                               "inhabilitado")
            else:
                condicion = condicion and textobj == textven
            if not condicion:
                break
        try:
            condicion = (condicion
                         and cliente.contador.prefijo
                                == self.wids['e_prefijo'].get_text())
            condicion = (condicion
                         and cliente.contador.sufijo
                                == self.wids['e_sufijo'].get_text())
        except:
            pass
        condicion = (condicion
                and utils.combo_get_value(self.wids['cbe_comercial'])
                        ==  cliente.clienteID)
        condicion = (condicion
                and utils.combo_get_value(self.wids['cbe_proveedor'])
                        == cliente.proveedorID)
        condicion = (condicion
                and utils.combo_get_value(self.wids['cbe_cuenta'])
                        == cliente.cuentaOrigenID)
        condicion = (condicion
                and utils.combo_get_value(self.wids['cb_tipo_de_cliente'])
                        == cliente.tipoDeClienteID)
        condicion = (condicion
                and self.wids['e_porcentaje'].get_text()
                        == "%s %%" % (utils.float2str(cliente.porcentaje * 100)))
        condicion = (condicion
                and self.wids['ch_validacionManual'].get_active()
                        == cliente.validacionManual)
        condicion = (condicion
                and self.wids['ch_envio_albaran'].get_active()
                        == cliente.enviarCorreoAlbaran)
        condicion = (condicion
                and self.wids['ch_envio_factura'].get_active()
                        == cliente.enviarCorreoFactura)
        condicion = (condicion
                and self.wids['ch_envio_packing'].get_active()
                        == cliente.enviarCorreoPacking)
        condicion = (condicion
                and self.wids['ch_formaPagoFija'].get_active()
                        == cliente.formaPagoFija)
        condicion = (condicion
                and self.wids['e_riesgoConcedido'].get_text()
                        == utils.float2str(self.objeto.riesgoConcedido))
        condicion = (condicion
                and self.wids['e_riesgoAsegurado'].get_text()
                        == utils.float2str(self.objeto.riesgoAsegurado))
        condicion = (condicion
                and self.wids['sp_copias'].get_value()
                        == cliente.copiasFactura)
        return not condicion    # Concición verifica que sea igual

    def aviso_actualizacion(self):
        """
        Muestra una ventana modal con el mensaje de objeto
        actualizado.
        """
        utils.dialogo_info('ACTUALIZAR',
                           'El cliente ha sido modificado remotamente.\n'
                           'Debe actualizar la información mostrada en '
                           'pantalla.\nPulse el botón «Actualizar»',
                           padre = self.wids['ventana'])
        b_actualizar = self.wids['b_actualizar']
        if b_actualizar != None:
            b_actualizar.set_sensitive(True)

    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        if pclases.DEBUG:
            antes = time.time()
            myprint("0.- clientes.py::inicializar_ventana -> Hey, ho!")
        self.wids['ch_validacionManual'].child.set_use_markup(True)
        # Inicialmente no se muestra NADA. Sólo se le deja al
        # usuario la opción de buscar o crear nuevo.
        self.activar_widgets(False)
        self.wids['b_actualizar'].set_sensitive(False)
        self.wids['b_guardar'].set_sensitive(False)
        self.wids['b_nuevo'].set_sensitive(True)
        self.wids['b_buscar'].set_sensitive(True)
        utils.combo_set_from_db(self.wids['cb_orden'],
                                self.wids['cb_orden'].get_model()[0][0])
        self.wids['cb_orden'].connect("changed",
                self.actualizar_botones_anterior_siguiente)
        contadores = []
        if pclases.DEBUG:
            myprint("1.- clientes.py::inicializar_ventana ->",
                    time.time() - antes)
        for contador in pclases.Contador.select(orderBy = "prefijo"):
            if contador.prefijo == None:
                contador.prefijo = ""
            if contador.sufijo == None:
                contador.sufijo = ""
            contadores.append((contador.id, "%s | %s" % (contador.prefijo,
                                                         contador.sufijo)))
        if pclases.DEBUG:
            myprint("2.- clientes.py::inicializar_ventana ->",
                    time.time() - antes)
        utils.rellenar_lista(self.wids['cmb_contador'], contadores)
        utils.rellenar_lista(self.wids['cbe_comercial'],
            [(c.id, c.nombre)
                for c in pclases.Cliente.select(orderBy = "nombre")])
        utils.rellenar_lista(self.wids['cbe_proveedor'],
            [(c.id, c.nombre)
                for c in pclases.Proveedor.select(orderBy = "nombre")])
        utils.rellenar_lista(self.wids['cbe_cuenta'],
            [(c.id, "%s: %s %s" % (c.nombre, c.banco, c.ccc))
                for c in pclases.CuentaOrigen.select(orderBy = "nombre")])
        utils.rellenar_lista(self.wids['cb_tipo_de_cliente'],
            [(c.id, c.descripcion)
                for c in pclases.TipoDeCliente.select(orderBy = "id")])
        cols = (('Cliente', 'gobject.TYPE_STRING', False, True, True, None),
                ('Comisión', 'gobject.TYPE_STRING', False, True, False, None),
                ('IDCliente', 'gobject.TYPE_INT64', False, True, False, None))
        utils.preparar_listview(self.wids['tv_clientes'], cols)
        cols = (('Banco', 'gobject.TYPE_STRING',
                    True, True, True, self.cambiar_banco),
                ('Swif', 'gobject.TYPE_STRING',
                    True, True, False, self.cambiar_swif),
                ('Iban', 'gobject.TYPE_STRING',
                    True, True, False, self.cambiar_iban),
                ('CCC', 'gobject.TYPE_STRING',
                    True, True, False, self.cambiar_cuenta),
                ('Observaciones', 'gobject.TYPE_STRING',
                    True, True, False, self.cambiar_observaciones),
                ('IDCuentaBancariaCliente', 'gobject.TYPE_INT64',
                    False, True, False, None))
        utils.preparar_listview(self.wids['tv_cuentas'], cols)
        if pclases.DEBUG:
            myprint("3.- clientes.py::inicializar_ventana ->",
                    time.time() - antes)
        self.wids['tv_cuentas'].get_selection().set_mode(
            gtk.SELECTION_MULTIPLE)
        cols = (("Nº. Factura", 'gobject.TYPE_STRING', False,True,True,None),
                ("Fecha", 'gobject.TYPE_STRING', False, True, False, None),
                ("Importe", 'gobject.TYPE_STRING', False, True, False, None),
                ("No documentado", 'gobject.TYPE_STRING',
                    False, True, False, None),
                ("Documentado", 'gobject.TYPE_STRING',
                    False, True, False, None),
                ("Vencido", 'gobject.TYPE_STRING',
                    False, True, False, None),
                ("Cobrado", 'gobject.TYPE_STRING', False, True, False, None),
                ("Estado", 'gobject.TYPE_STRING', False, True, False, None),
                ("Obra", 'gobject.TYPE_STRING', False, True, False, None),
                ("PUID", 'gobject.TYPE_STRING', False, True, False, None))
        utils.preparar_listview(self.wids['tv_facturas'], cols)
        self.wids['tv_facturas'].connect("row-activated",
                                         self.abrir_factura_puid)
        getcol = self.wids['tv_facturas'].get_column
        getcol(2).get_cell_renderers()[0].set_property('xalign', 1.0)
        getcol(3).get_cell_renderers()[0].set_property('xalign', 1.0)
        getcol(4).get_cell_renderers()[0].set_property('xalign', 1.0)
        getcol(5).get_cell_renderers()[0].set_property('xalign', 1.0)
        getcol(6).get_cell_renderers()[0].set_property('xalign', 1.0)
        orden = ('nombre', 'direccion', 'cp', 'ciudad', 'provincia', 'pais',
                 'fechainicio', 'fechafin', 'observaciones', 'generica')
        if pclases.DEBUG:
            myprint("4.- clientes.py::inicializar_ventana ->",
                    time.time() - antes)
        self.tvobras = pclase2tv.Pclase2tv(pclases.Obra,
                                           self.wids['tv_obras'],
                                           # self.objeto, # Es muchos a muchos.
                                           seleccion_multiple = True,
                                           orden = orden)
        if pclases.DEBUG:
            myprint("5.- clientes.py::inicializar_ventana ->",
                    time.time() - antes)
        self.tvcontactos = pclase2tv.Pclase2tv(pclases.Contacto,
                                               self.wids['tv_contactos'],
                                               seleccion_multiple = True)
        self.hndlr_obras = self.wids['tv_obras'].get_selection().connect(
                                            "changed", self.rellenar_contactos)
        cols = (("Nº. Factura", 'gobject.TYPE_STRING', False,True,True,None),
                ("Fecha", 'gobject.TYPE_STRING', False, True, False, None),
                # ("Importe", 'gobject.TYPE_STRING', False, True, False, None),
                ("PUID", 'gobject.TYPE_STRING', False, True, False, None))
        if pclases.DEBUG:
            myprint("6.- clientes.py::inicializar_ventana ->",
                    time.time() - antes)
        for tv in (self.wids['tv_pdte_doc'], self.wids['tv_no_vencidas'],
                   self.wids['tv_impagadas'], self.wids['tv_cobradas'], 
                   self.wids['tv_abonos']):
            utils.preparar_listview(tv, cols)
            tv.connect("row-activated", self.abrir_factura_puid)
            tv.get_column(1).get_cell_renderers()[0].set_property('xalign',1.0)
            tv.connect("cursor-changed", self.seleccionar_en_tv_superior)
        if pclases.DEBUG:
            myprint("7.- clientes.py::inicializar_ventana ->",
                    time.time() - antes)
        utils.rellenar_lista(self.wids['cbe_documentodepago'],
                [(d.id, d.documento) for d in
                    pclases.DocumentoDePago.select(orderBy = "id")])
        if pclases.DEBUG:
            myprint("8.- clientes.py::inicializar_ventana ->",
                    time.time() - antes)
        self.add_texto_complementario()
        self.add_fdp_fija()
        if pclases.DEBUG:
            myprint("9.- clientes.py::inicializar_ventana ->",
                    time.time() - antes)
        tabla = self.wids['e_riesgoAsegurado'].parent
        tabla.resize(tabla.get_property("n-rows") + 1,
                     tabla.get_property("n-columns"))
        from formularios.custom_widgets import starhscale
        self.wids['rating'] = starhscale.StarHScale(max_stars = 5)
        self.wids['rating'].set_sensitive(False)
        f = tabla.get_property("n-rows")
        l_rating = gtk.Label("Calificación")
        tabla.attach(l_rating, 0, 1, f, f + 1, gtk.FILL, gtk.FILL)
        tabla.attach(self.wids['rating'], 1, 2, f, f + 1, gtk.FILL, gtk.FILL)
        #self.wids['rating'].set_tooltip_text(
        #        pclases.Cliente.calcular_rating.__doc__)
        # Como esto de arriba no funciona, lo hago explícito.
        b_ayuda = gtk.Button(stock = gtk.STOCK_HELP)
        def show_hint(boton):
            utils.dialogo_info(titulo = "RATING",
                    texto = pclases.Cliente.calcular_rating.__doc__,
                    padre = self.wids['ventana'])
        b_ayuda.connect("clicked", show_hint)
        tabla.attach(b_ayuda, 2, 3, f, f + 1, gtk.SHRINK, gtk.SHRINK)
        tabla.show_all()
        if self.usuario and self.usuario.nivel > 2:
            # De momento solo activo para admin y gerencia.
            # [16/06/2014] Subo un nivel más para ver si es realmente fiable.
            self.wids['rating'].set_property("visible", False)
            b_ayuda.set_property("visible", False)
            l_rating.set_property("visible", False)
        if pclases.DEBUG:
            myprint("10.- clientes.py::inicializar_ventana ->",
                    time.time() - antes)

    def add_fdp_fija(self):
        boton = self.wids['b_ayuda_formapago']
        tabla = boton.parent
        h = gtk.HBox()
        boton.reparent(h)
        fdpfija = self.wids['ch_formaPagoFija'] = gtk.CheckButton(
                label = "Obligatoria para las ofertas de este cliente")
        h.pack_start(fdpfija, expand = True)
        h.show_all()
        # OJO: HARCODED. Pero porque no hay forma fácil de obtener fila y 
        # columna de un widget dentro de una gtk.Table.
        tabla.attach(h, 2, 3, 0, 1, xoptions = gtk.FILL, yoptions = 0)

    def add_texto_complementario(self):
        t = self.wids['e_diadepago'].parent
        v = gtk.VBox()
        l = gtk.Label("<small>Texto complementario a la forma de pago</small>")
        l.set_property("xalign", 0.0)
        l.set_use_markup(True)
        e = gtk.Entry()
        v.pack_start(l, expand = True)
        v.pack_start(e, expand = True)
        self.wids['e_textoComplementarioFormaDePago'] = e
        t.remove(self.wids['e_diadepago'])
        h = gtk.HBox()
        h.pack_start(self.wids['e_diadepago'], expand = False)
        h.pack_start(v, expand = True)
        t.attach(h, 1, 3, 1, 2, xoptions = gtk.FILL, yoptions = 0)
        t.show_all()

    def seleccionar_en_tv_superior(self, tv):
        """
        Selecciona en el TreeView de todas las facturas la fila de la
        factura seleccionada en el TreeView que recibe la señal.
        """
        model, itr = tv.get_selection().get_selected()
        if not itr:
            return
        puid = model[itr][-1]
        model_superior = self.wids['tv_facturas'].get_model()
        itr = model_superior.get_iter_first()
        while itr:
            if model_superior[itr][-1] == puid:
                sel = self.wids['tv_facturas'].get_selection()
                sel.select_iter(itr)
                self.wids['tv_facturas'].scroll_to_cell(
                    model_superior.get_path(itr), use_align = True)
                break
            itr = model_superior.iter_next(itr)

    def abrir_factura_puid(self, tv, path, view_column):
        self.wids['ventana'].window.set_cursor(gtk.gdk.Cursor(gtk.gdk.WATCH))
        while gtk.events_pending(): gtk.main_iteration(False)
        model = tv.get_model()
        puid = model[path][-1]
        objeto = pclases.getObjetoPUID(puid)
        if isinstance(objeto, pclases.FacturaVenta):
            from formularios import facturas_venta
            ventanafacturas = facturas_venta.FacturasVenta(objeto,
                                usuario = self.usuario)
        elif isinstance(objeto, pclases.FacturaDeAbono):
            from formularios import abonos_venta
            ventanaabonos = abonos_venta.AbonosVenta(objeto.abono,
                                usuario = self.usuario)
        try:
            self.wids['ventana'].window.set_cursor(None)
        except KeyError:
            pass    # La ventana se cerró antes que la factura que abrió.

    def abrir_cliente(self, tv, path, view_column):
        """
        Abre el cliente seleccionado en el TreeView en una nueva ventana.
        """
        idcliente = tv.get_model()[path][-1]
        cliente = pclases.Cliente.get(idcliente)
        nueva_ventana = Clientes(cliente)  # @UnusedVariable

    def activar_widgets(self, s, chequear_permisos = True):
        """
        Activa o desactiva (sensitive=True/False) todos
        los widgets de la ventana que dependan del
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        ws = ('b_borrar','expander1','vbox2','vbox3','vbox4','vbox5','vbox8',
              'vbox7')
        for w in ws:
            self.wids[w].set_sensitive(s)
        if chequear_permisos:
            self.check_permisos(nombre_fichero_ventana = "clientes.py")

    def ir_a_primero(self):
        """
        Hace que el primer registro -si lo hay- de la tabla implicada
        en el objeto del formulario sea el objeto activo.
        """
        anterior = cliente = self.objeto
        try:
            # Anulo el aviso de actualización del envío que deja de ser activo.
            if cliente != None: cliente.notificador.set_func(lambda : None)
            # Selecciono todos y me quedo con el primero de la lista
            cliente = pclases.Cliente.select(orderBy = "-id")[0]
            # Activo la notificación
            cliente.notificador.set_func(self.aviso_actualizacion)
        except:
            cliente = None
        self.objeto = cliente
        self.actualizar_ventana(objeto_anterior = anterior,
                                deep_refresh = False)

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
            filas_res.append((r.id,
                              r.nombre,
                              r.cif,
                              r.get_direccion_completa(),
                              "; ".join([o.nombre for o in r.obras]),
                              r.observaciones
                             ))
        idcliente = utils.dialogo_resultado(filas_res,
                                            titulo = 'Seleccione Cliente',
                                            cabeceras = ('ID Interno',
                                                         'Nombre',
                                                         'CIF',
                                                         'Dirección',
                                                         "Obras",
                                                         "Observaciones"),
                                            padre = self.wids['ventana'])
        if idcliente < 0:
            return None
        else:
            return idcliente

    def escribir_valor(self, widget, valor):
        """
        Con respecto al widget: intenta escribir el valor como si
        fuera un Entry. Si no lo consigue lo intenta como si fuera
        un TextView.
        En cuanto al valor, lo convierte en cadena antes de escribirlo.
        """
        try:
            widget.set_text(str(valor))
        except AttributeError: # No tiene el set_text, por tanto no es un Entry.
            widget.get_buffer().set_text(valor)

    def leer_valor(self, widget):
        """
        Intenta leer el valor como si fuera un Entry. Si no lo
        consigue lo hace suponiendo que es un TextView.
        Devuelve el valor leído _como cadena_.
        """
        if isinstance(widget, (gtk.ToggleButton, gtk.CheckButton)):
            res = widget.get_active()
        else:
            try:
                res = widget.get_text()
            except AttributeError:
                try:
                    buff = widget.get_buffer()
                    res = buff.get_text(*buff.get_bounds())
                except AttributeError:
                    try:
                        # FIXME: Esto falla con versiones antiguas de Gtk
                        res = widget.child.get_text()
                    except AttributeError:
                        # HACK: Lo cambio por un Entry normal.
                        widget = self.very_ugly_dirty_hack(widget)
                        res = widget.get_text()
        return res

    def very_ugly_dirty_hack(self, w):
        """Apaño para cambiar el GtkComboBoxEntry por un Entry normal. En
        versiones de pygtk antiguas contra libglade el Entry hijo del combo
        se convierte en un CellRenderer que no tiene child para hacerle un
        set_text.

        El nombre es temporal (porque pienso arreglarlo en condiciones y
        acabar con esta mierda).
        """
        nombrew = w.get_property('name')
        nuevo = gtk.Entry()
        self.wids[nombrew] = nuevo
        #nuevo.set_properties(*w.get_properties())
        #self.wids.widgets.pop(nombrew)
        #myprint(self.wids.keys(), nombrew in self.wids.keys())
        from formularios.widgets import replace_widget
        replace_widget(w, nuevo)
        nuevo.show()
        return nuevo

    def rellenar_widgets(self):
        """
        Introduce la información del cliente actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a
        esta función en ese caso.
        """
        if pclases.DEBUG:
            antes = time.time()
            myprint("0.- clientes.py::rellenar_widgets -> Let's go!")
        if not self.objeto:
            self.activar_widgets(False)
            return
        cliente = self.objeto
        try:
            orden = utils.combo_get_value(self.wids['cb_orden'])
        except KeyError:    # Ventana destruyéndose a la vez que se ha pulsado
                            # F5 para actualizar. Mutis por el foro...
            return
        if orden == "Orden cronológico":
            clientes = pclases.Cliente.select(orderBy = "id")
        elif orden == "Orden alfabético":
            clientes = pclases.Cliente.select(orderBy = "nombre")
        clientes_count = clientes.count()
        yo_index = pclases.SQLlist(clientes).index(self.objeto) + 1
        self.wids['ventana'].set_title("Clientes - %s (%d de %d)" % (
            cliente.nombre, yo_index, clientes_count))
        self.wids['e_telefono'].set_text(cliente.telefono or '')
        self.wids['e_nombre'].set_text(cliente.nombre or '')
        self.wids['e_cif'].set_text(cliente.cif or '')
        self.wids['e_direccion'].set_text(cliente.direccion or '')
        self.wids['e_pais'].set_text(cliente.pais or '')
        self.wids['e_ciudad'].set_text(cliente.ciudad or '')
        self.wids['e_provincia'].set_text(cliente.provincia or '')
        self.wids['e_cp'].set_text(cliente.cp or '')
        if cliente.iva == None or cliente.iva == '':
            cliente.notificador.desactivar()
            cliente.iva = 0.21
            cliente.sync()
            cliente.notificador.activar(self.aviso_actualizacion)
        if pclases.DEBUG:
            myprint("1.- clientes.py::rellenar_widgets ->",
                    time.time() - antes)
        self.wids['e_iva'].set_text(utils.float2str(cliente.iva * 100, 0)+' %')
        self.wids['e_nombref'].set_text(cliente.nombref or '')
        self.wids['e_direccionfacturacion'].set_text(
            cliente.direccionfacturacion or '')
        self.wids['e_paisfacturacion'].set_text(cliente.paisfacturacion or '')
        self.wids['e_ciudadfacturacion'].set_text(
            cliente.ciudadfacturacion or '')
        self.wids['e_provinciafacturacion'].set_text(
            cliente.provinciafacturacion or '')
        self.wids['e_cpfacturacion'].set_text(cliente.cpfacturacion or '')
        self.wids['e_email'].set_text(cliente.email or '')
        self.wids['e_contacto'].set_text(cliente.contacto or '')
        # FIXME: Esto falla en versiones antiguas de Gtk.
        txtvtos = cliente.vencimientos or ''
        if isinstance(self.wids['e_vencimientos'], gtk.Entry):
            self.wids['e_vencimientos'].set_text(txtvtos)
        else:
            try:
                self.wids['e_vencimientos'].child.set_text(txtvtos)
            except AttributeError:
                self.wids['e_vencimientos'] = self.very_ugly_dirty_hack(
                        self.wids['e_vencimientos'])
                self.wids['e_vencimientos'].set_text(txtvtos)
        self.wids['e_diadepago'].set_text(cliente.diadepago or '')
        self.wids['e_documentodepago'].set_text(cliente.documentodepago or '')
        self.wids['e_motivo'].set_text(cliente.motivo)
        self.wids['e_inhabilitado'].set_active(cliente.inhabilitado)
        if pclases.DEBUG:
            myprint("2.- clientes.py::rellenar_widgets ->",
                    time.time() - antes)
        if cliente.contador != None:
            self.wids['e_prefijo'].set_text(cliente.contador.prefijo)
            self.wids['e_sufijo'].set_text(cliente.contador.sufijo)
            utils.combo_set_from_db(self.wids['cmb_contador'],
                cliente.contadorID)
        else:
            self.wids['e_prefijo'].set_text('')
            self.wids['e_sufijo'].set_text('')
            utils.combo_set_from_db(self.wids['cmb_contador'], None)
        if pclases.DEBUG:
            myprint("3.- clientes.py::rellenar_widgets ->",
                    time.time() - antes)
        if cliente.tarifa != None:
            self.wids['e_tarifa'].set_text(cliente.tarifa.nombre)
        else:
            self.wids['e_tarifa'].set_text('')
        buff = self.wids['e_observaciones'].get_buffer()
        buff.set_text(cliente.observaciones)
        utils.combo_set_from_db(self.wids['cbe_comercial'], cliente.clienteID)
        utils.combo_set_from_db(self.wids['cbe_proveedor'],
                                cliente.proveedorID)
        utils.combo_set_from_db(self.wids['cbe_cuenta'],
                                cliente.cuentaOrigenID)
        utils.combo_set_from_db(self.wids['cb_tipo_de_cliente'],
                                cliente.tipoDeClienteID)
        self.wids['e_porcentaje'].set_text(
            "%s %%" % (utils.float2str(cliente.porcentaje * 100)))
        if pclases.DEBUG:
            myprint("4.- clientes.py::rellenar_widgets ->",
                    time.time() - antes)
        self.wids['ch_validacionManual'].set_active(cliente.validacionManual)
        self.wids['ch_envio_albaran'].set_active(cliente.enviarCorreoAlbaran)
        self.wids['ch_envio_factura'].set_active(cliente.enviarCorreoFactura)
        self.wids['ch_envio_packing'].set_active(cliente.enviarCorreoPacking)
        self.wids['e_packingListConCodigo'].set_active(
            cliente.packingListConCodigo)
        self.wids['e_facturarConAlbaran'].set_active(
            cliente.facturarConAlbaran)
        self.wids['e_fax'].set_text(cliente.fax != None and cliente.fax or '')
        self.wids['ch_formaPagoFija'].set_active(cliente.formaPagoFija)
        try:
            self.wids['e_textoComplementarioFormaDePago'].set_text(
                                        cliente.textoComplementarioFormaDePago)
        except AttributeError:
            pass    # Versiones anteriores de la BD. No tiene este campo.
        # Este cliente es comercial de otros clientes: oculto el desplegable y
        # muestro la pestaña de datos de comercial:
        self.wids['hbox_comercial'].set_property("visible",
                                                 cliente.clientes == [])
        pagina_comercial = self.wids['notebook1'].get_nth_page(3)
        pagina_comercial.set_property("visible", cliente.clientes != [])
        model = self.wids['tv_clientes'].get_model()
        model.clear()
        for c in cliente.clientes:
            model.append((c.nombre,
                          "%s %%" % (utils.float2str(c.porcentaje*100)), c.id))
        if pclases.DEBUG:
            myprint("5.- clientes.py::rellenar_widgets ->",
                    time.time() - antes)
        self.rellenar_cuentas()
        self.rellenar_riesgo_campos_objeto()
        if pclases.DEBUG:
            myprint("6.- clientes.py::rellenar_widgets ->",
                    time.time() - antes)
        if (self.wids['notebook1'].get_current_page() == 4
            and not self.wids['ch_ign_concedido'].get_active()):
            self.rellenar_riesgo_campos_calculados()
        if self.wids['notebook1'].get_current_page() == 5:
            self.rellenar_obras()
            self.rellenar_contactos()
        self.wids['sp_copias'].set_value(cliente.copiasFactura)
        ch = self.wids['ch_ign_asegurado']
        self.wids['e_riesgoAsegurado'].set_sensitive(not ch.get_active())
        ch = self.wids['ch_ign_concedido']
        self.wids['e_riesgoConcedido'].set_sensitive(not ch.get_active())
        if pclases.DEBUG:
            myprint("7.- clientes.py::rellenar_widgets ->",
                    time.time() - antes)
        self.objeto.make_swap()
        if pclases.DEBUG:
            myprint("8.- clientes.py::rellenar_widgets ->",
                    time.time() - antes)
        try:
            doc_from_db = self.objeto.get_documentoDePago().documento
        except AttributeError:
            doc_from_db = None
        if (doc_from_db
              and doc_from_db.upper() == self.objeto.documentodepago.upper()
              # Y efectivamente no son iguales. Porque si ya los son, ¿para qué
              # actualizarla y malgastar espacio en la tabla de auditoría?
              and doc_from_db != self.objeto.documentodepago):
            self.objeto.documentodepago = doc_from_db
            self.objeto.syncUpdate()
            self.wids['e_documentodepago'].set_text(
                    self.objeto.documentodepago)
            pclases.Auditoria.modificado(self.objeto, self.usuario, __file__,
                    "Actualización automática de la forma de pago para "
                    "hacerla coincidir con la descripción exacta de la tabla "
                    "de documentos de pago válidos.")
        if doc_from_db and doc_from_db != self.objeto.documentodepago:
            if utils.dialogo(titulo = "CORREGIR DOCUMENTO DE PAGO",
                    texto = "El cliente actual tiene como documento de pago:\n"
                            "«%s». Se aconseja usar «%s».\n"
                            "¿Corregirlo automáticamente?\n\n"
                            "(Responda «No» si la forma de pago es correcta \n"
                            "o prefiere corregirlo manualmente)" % (
                                self.objeto.documentodepago,
                                doc_from_db),
                    padre = self.wids['ventana']):
                self.objeto.documentodepago = doc_from_db
                self.objeto.syncUpdate()
                self.wids['e_documentodepago'].set_text(
                        self.objeto.documentodepago)
                pclases.Auditoria.modificado(self.objeto, self.usuario,
                        __file__,
                        "Corrección propuesta del texto de forma de pago "
                        "aceptada por el usuario.")
                self.objeto.make_swap()
        if pclases.DEBUG:
            myprint("9.- clientes.py::rellenar_widgets ->",
                    time.time() - antes)
        ### Botones anterior/siguiente
        self.actualizar_botones_anterior_siguiente()
        if pclases.DEBUG:
            myprint("10.- clientes.py::rellenar_widgets ->",
                    time.time() - antes)

    def actualizar_botones_anterior_siguiente(self, *args, **kw):
        if self.objeto:
            orden = utils.combo_get_value(self.wids['cb_orden'])
            if orden == "Orden cronológico":
                anteriores = pclases.Cliente.select(
                        pclases.Cliente.q.id < self.objeto.id).count()
                siguientes = pclases.Cliente.select(
                        pclases.Cliente.q.id > self.objeto.id).count()
            elif orden == "Orden alfabético":
                anteriores = pclases.Cliente.select(
                        pclases.Cliente.q.nombre < self.objeto.nombre).count()
                siguientes = pclases.Cliente.select(
                        pclases.Cliente.q.nombre > self.objeto.nombre).count()
            self.wids['b_back'].set_sensitive(anteriores)
            self.wids['b_next'].set_sensitive(siguientes)

    def rellenar_cuentas(self):
        """
        Introduce las cuentas bancarias del cliente en el ListView
        """
        if self.objeto != None:
            model = self.wids['tv_cuentas'].get_model()
            model.clear()
            cuentas = self.objeto.cuentasBancariasCliente[:]
            cuentas.sort(lambda c1, c2:
                    (c1.id < c2.id and -1) or (c1.id > c2.id and 1) or 0)
            for c in cuentas:
                model.append((c.banco, c.swif, c.iban, c.cuenta,
                              c.observaciones, c.id))

    def add_cuenta(self, boton):
        """
        Crea una nueva cuenta asociada con el cliente.
        """
        if self.objeto != None:
            c = pclases.CuentaBancariaCliente(clienteID = self.objeto.id,
                    banco = "Nueva cuenta bancaria",
                    observaciones = "Introduzca la información de la cuenta.")
            pclases.Auditoria.nuevo(c, self.usuario, __file__)
            self.rellenar_cuentas()

    def drop_cuenta(self, boton):
        """
        Elimina la(s) cuenta(s) seleccionadas.
        """
        treeview = self.wids['tv_cuentas']
        model, paths = treeview.get_selection().get_selected_rows()
        if  paths != None and paths != [] and utils.dialogo(
                titulo = "¿BORRAR CUENTAS SELECCIONADAS?",
                texto = "¿Está seguro de que desea eliminar las cuentas"
                        " seleccionadas?",
                padre = self.wids['ventana']):
            for path in paths:
                ide = model[path][-1]
                c = pclases.CuentaBancariaCliente.get(ide)
                try:
                    c.destroy(ventana = __file__)
                except:
                    txt = """
                    La cuenta está implicada en operaciones, cobro de
                    recibos, etc.
                    ¿Desea eliminar la cuenta y todas estas operaciones?

                    NOTA: Los borrados masivos en cascada no son aconsejables.
                          Si no está completamente seguro, responda «No» y
                          cambie la cuenta por otra allí donde aparezca antes
                          de volver a intentar eliminarla.
                    """
                    if utils.dialogo(titulo = "ERROR: CUENTA USADA",
                                     texto = txt,
                                     padre = self.wids['ventana']):
                        #for r in c.recibos:
                        #    r.cuentaBancariaCliente = None
                        c.destroy_en_cascada(ventana = __file__)
            self.rellenar_cuentas()

    # --------------- Manejadores de eventos ----------------------------
    def cambiar_banco(self, cell, path, text):
        """
        Cambia el banco de la cuentaBancariaCliente.
        """
        model = self.wids['tv_cuentas'].get_model()
        ide = model[path][-1]
        c = pclases.CuentaBancariaCliente.get(ide)
        c.banco = text
        self.rellenar_cuentas()

    def cambiar_swif(self, cell, path, text):
        """
        Cambia el SWIF de la cuentaBancariaCliente.
        """
        model = self.wids['tv_cuentas'].get_model()
        ide = model[path][-1]
        c = pclases.CuentaBancariaCliente.get(ide)
        c.swif = text
        self.rellenar_cuentas()

    def cambiar_iban(self, cell, path, text):
        """
        Cambia el IBAN de la cuentaBancariaCliente.
        """
        model = self.wids['tv_cuentas'].get_model()
        ide = model[path][-1]
        c = pclases.CuentaBancariaCliente.get(ide)
        c.iban = text
        self.rellenar_cuentas()

    def cambiar_cuenta(self, cell, path, text):
        """
        Cambia la cuenta de la cuentaBancariaCliente.
        """
        model = self.wids['tv_cuentas'].get_model()
        ide = model[path][-1]
        c = pclases.CuentaBancariaCliente.get(ide)
        c.cuenta = text
        self.rellenar_cuentas()

    def cambiar_observaciones(self, cell, path, text):
        """
        Cambia las observaciones de la cuentaBancariaCliente.
        """
        model = self.wids['tv_cuentas'].get_model()
        ide = model[path][-1]
        c = pclases.CuentaBancariaCliente.get(ide)
        c.observaciones = text
        self.rellenar_cuentas()

    def crear_nuevo_cliente(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        anterior = cliente = self.objeto
        nombre = utils.dialogo_entrada(
                    texto = 'Introduzca el nombre del cliente:',
                    titulo = 'NOMBRE',
                    padre = self.wids['ventana'])
        if nombre != None:
            if cliente != None:
                cliente.notificador.set_func(lambda : None)
            tarifa_por_defecto = pclases.Tarifa.get_tarifa_defecto()
            tipo_defecto = pclases.TipoDeCliente.get_por_defecto()
            self.objeto = pclases.Cliente(nombre=nombre,
                                          tarifa=tarifa_por_defecto,
                                          contadorID=None,
                                          telefono='',
                                          cif='PENDIENTE',
                                          direccion='',
                                          pais='',
                                          ciudad='',
                                          provincia='',
                                          cp='',
                                          vencimientos='180 D.F.F.',
                                          iva=0.21,
                                          direccionfacturacion='',
                                          nombref='',
                                          paisfacturacion='',
                                          ciudadfacturacion='',
                                          provinciafacturacion='',
                                          cpfacturacion='',
                                          email='',
                                          contacto='',
                                          observaciones='',
                                          documentodepago='Pagaré a la orden',
                                          diadepago='25',
                                          formadepago='180 D.F.F.',
                                          inhabilitado=False,
                                          porcentaje=0.0,
                                          clienteID=None,
                                          enviarCorreoAlbaran=False,
                                          enviarCorreoFactura=False,
                                          enviarCorreoPacking=False,
                                          fax='',
                                          packingListConCodigo=False,
                                          facturarConAlbaran=True,
                                          tipoDeCliente=tipo_defecto)
            pclases.Auditoria.nuevo(self.objeto, self.usuario, __file__)
            self._objetoreciencreado = self.objeto
            self.objeto.notificador.set_func(self.aviso_actualizacion)
            self.actualizar_ventana(objeto_anterior=anterior,
                                    deep_refresh=False)
            check_presupuestos_sin_cliente(self.objeto, self.wids['ventana'])
            utils.dialogo_info(titulo='CLIENTE CREADO',
                texto='Inserte el resto de la información del cliente.',
                padre=self.wids['ventana'])

    def buscar_cliente(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        anterior = cliente = self.objeto
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR CLIENTE",
            texto = "Introduzca obra, CIF o nombre del cliente a buscar:",
            padre = self.wids['ventana'])
        if a_buscar != None:
            clientes_obras = buscar_clientes_obras(a_buscar)
            criterio = pclases.OR(
                            pclases.Cliente.q.nombre.contains(a_buscar),
                            pclases.Cliente.q.cif.contains(a_buscar),
                            pclases.Cliente.q.observaciones.contains(a_buscar))
            clientes_clientes = pclases.Cliente.select(criterio)
            resultados = []
            for c in clientes_obras:
                if c not in resultados:
                    resultados.append(c)
            for c in clientes_clientes:
                if c not in resultados:
                    resultados.append(c)
            resultados = pclases.SQLtuple(resultados)
            if resultados.count() > 1:
                ## Refinar los resultados
                idcliente = self.refinar_resultados_busqueda(resultados)
                if idcliente == None:
                    return
                resultados = [pclases.Cliente.get(idcliente)]
            elif resultados.count() < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info('SIN RESULTADOS',
                    'La búsqueda no produjo resultados.\nPruebe a cambiar el '
                    'texto buscado o déjelo en blanco para ver una lista '
                    'completa.\n(Atención: Ver la lista completa puede '
                    'resultar lento si el número de elementos es muy alto)',
                    padre = self.wids['ventana'])
                return
            ## Un único resultado
            # Primero anulo la función de actualización
            if cliente != None:
                cliente.notificador.set_func(lambda : None)
            # Pongo el objeto como actual
            cliente = resultados[0]
            # Y activo la función de notificación:
            self.objeto = cliente
            self.actualizar_ventana(objeto_anterior = anterior)
            cliente.notificador.set_func(self.aviso_actualizacion)

    def guardar(self, widget = None):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        cliente = self.objeto
        asegurado_antes = cliente.riesgoAsegurado
        concedido_antes = cliente.riesgoConcedido
        bakcif = cliente.cif
        # Si no tiene dirección de facturación se copia la postal.
        copiar = True
        for wpostal, wfacturacion in (
            (self.wids['e_direccion'], self.wids['e_direccionfacturacion']),
            (self.wids['e_nombre'], self.wids['e_nombref']),
            (self.wids['e_pais'], self.wids['e_paisfacturacion']),
            (self.wids['e_provincia'], self.wids['e_provinciafacturacion']),
            (self.wids['e_ciudad'], self.wids['e_ciudadfacturacion']),
            (self.wids['e_cp'], self.wids['e_cpfacturacion'])):
            copiar = copiar and (
                wfacturacion.get_text() == ""
                or wfacturacion.get_text() == None)
        if copiar:
            for wpostal, wfacturacion in (
                (self.wids['e_direccion'], self.wids['e_direccionfacturacion']),
                (self.wids['e_nombre'], self.wids['e_nombref']),
                (self.wids['e_pais'], self.wids['e_paisfacturacion']),
                (self.wids['e_provincia'], self.wids['e_provinciafacturacion']),
                (self.wids['e_ciudad'], self.wids['e_ciudadfacturacion']),
                (self.wids['e_cp'], self.wids['e_cpfacturacion'])):
                wfacturacion.set_text(wpostal.get_text())
        datos = {}
        for c in [c.name for c in cliente.sqlmeta.columnList
                  if c.name != 'tarifaID'
                      and c.name != 'contadorID'
                      and c.name != 'formadepago'
                      and c.name != 'formaPagoFija'
                      and c.name != "clienteID"
                      and c.name != "porcentaje"
                      and c.name != "validacionManual"
                      and c.name != "enviarCorreoAlbaran"
                      and c.name != "enviarCorreoFactura"
                      and c.name != "enviarCorreoPacking"
                      and c.name != "proveedorID"
                      and c.name != "cuentaOrigenID"
                      and c.name != "tipoDeClienteID"
                      and c.name != "copiasFactura"]:
                        # Omito columna tarifa
            datos[c] = self.leer_valor(self.wids['e_%s' % c])
            if pclases.DEBUG:
                if c == "observaciones":
                    myprint("Campo", c, ":", datos[c])
        # Desactivo el notificador momentáneamente
        cliente.notificador.set_func(lambda: None)
        # Auditoría: Swap para comparar después con lo que se haya guardado.
        self.objeto.make_swap()
        # Actualizo los datos del objeto
        for c in datos:
            # OJO: Hay que tener cuidado con los campos numéricos:
            if c == 'iva':
                try:
                    ivaparseado = utils.parse_porcentaje(datos[c],
                                                         fraccion = True)
                    cliente.set(iva = ivaparseado)
                except:
                    self.logger.warning("clientes.py-> El IVA no se pudo conv"
                                      "ertir a entero. Pongo IVA por defecto.")
                    cliente.set(iva = 0.21)
            elif c == "riesgoConcedido":
                try:
                    cliente.riesgoConcedido = utils._float(datos[c])
                except (ValueError, TypeError):
                    cliente.riesgoCondedido = -1
            elif c == "riesgoAsegurado":
                try:
                    cliente.riesgoAsegurado = utils._float(datos[c])
                except (ValueError, TypeError):
                    cliente.riesgoAsegurado = -1
            else:
                setattr(cliente, c, datos[c])
                if pclases.DEBUG:
                    if c == "observaciones":
                        myprint(datos[c])
                # eval('cliente.set(%s = "%s")' % (c, datos[c]))
        # CWT: Chequeo que tenga CIF, y si no lo tiene, lo pido por
        #      diálogo ad eternum.
        while utils.parse_cif(cliente.cif) == "":
            cliente.cif = utils.dialogo_entrada(texto="El CIF del cliente "
                            "no puede estar en blanco ni tener el valor «%s»"
                            ".\nEs un campo obligatorio.\nIntroduzca un CIF c"
                            "orrecto:" % cliente.cif,
                            titulo="CIF",
                            padre=self.wids['ventana'])
            if cliente.cif == None:
                cliente.cif = bakcif
                break
        if cliente.cif != bakcif:
            cliente.cif = utils.parse_cif(cliente.cif)
        # formadepago ya no se muestra en ventana, pero es posible que se
        # use en algún sitio, así que lo igualo a vencimientos,
        # que es el campo que ha unificado los dos Entries originales:
        cliente.formadepago = cliente.vencimientos

        cliente.clienteID = utils.combo_get_value(self.wids['cbe_comercial'])
        cliente.proveedorID = utils.combo_get_value(self.wids['cbe_proveedor'])
        cliente.cuentaOrigenID = utils.combo_get_value(self.wids['cbe_cuenta'])
        cliente.tipoDeClienteID = utils.combo_get_value(
                                            self.wids['cb_tipo_de_cliente'])
        try:
            cliente.porcentaje = utils.parse_porcentaje(
                self.wids['e_porcentaje'].get_text(),
                fraccion = True)
        except ValueError:
            cliente.porcentaje = 0
        cliente.validacionManual = self.wids['ch_validacionManual'].get_active()
        cliente.enviarCorreoAlbaran = self.wids['ch_envio_albaran'].get_active()
        cliente.enviarCorreoFactura = self.wids['ch_envio_factura'].get_active()
        cliente.enviarCorreoPacking = self.wids['ch_envio_packing'].get_active()
        cliente.formaPagoFija = self.wids['ch_formaPagoFija'].get_active()
        try:
            copias = int(self.wids['sp_copias'].get_value())
        except (ValueError, TypeError):
            copias = 0
        cliente.copiasFactura = copias
        # Auditoría de cambios
        if (asegurado_antes != cliente.riesgoAsegurado
                or concedido_antes != cliente.riesgoConcedido):
            pclases.Auditoria.modificado(cliente, self.usuario, __file__,
                descripcion = "%s: Riesgo asegurado: %s; concedido: %s."\
                              "(Antes: asegurado: %s; concedido: %s)" %
                                    (cliente.get_info(),
                                     utils.float2str(cliente.riesgoAsegurado),
                                     utils.float2str(cliente.riesgoConcedido),
                                     utils.float2str(asegurado_antes),
                                     utils.float2str(concedido_antes)))
        # Fuerzo la actualización de la BD y no espero a que SQLObject lo
        # haga por mí:
        cliente.syncUpdate()
        # Y ahora la auditoría, que comparará lo guardado en el objeto con los
        # valores "swapeados" (cacheados en el diccionario swap) antes de
        # guardar.
        pclases.Auditoria.modificado(cliente, self.usuario, __file__)
        # Vuelvo a activar el notificador
        cliente.notificador.set_func(self.aviso_actualizacion)
        self.actualizar_ventana(deep_refresh = False)
        self.wids['b_guardar'].set_sensitive(False)
        if cliente.es_extranjero() and cliente.iva != 0:
            utils.dialogo_info(titulo = "ADVERTENCIA",
                               texto = "El I.V.A. para los clientes "
                                       "extranjeros debería ser 0 %.",
                               padre = self.wids['ventana'])

    def borrar(self, widget):
        """
        Elimina el cliente en pantalla.
        """
        cliente = self.objeto
        if cliente != None:
            if utils.dialogo('¿Está seguro de eliminar el cliente actual?',
                             'BORRAR CLIENTE',
                             padre = self.wids['ventana']):
                cliente.notificador.set_func(lambda : None)
                try:
                    if cliente.destroy(ventana=__file__):
                        self.ir_a_primero()
                    else:
                        raise 
                except:
                    txt = """
                    El cliente no se eliminó por tener pedidos, facturas,
                    obras u ofertas relacionadas.
                    Si desea eliminarlo, borre antes los elementos relacionados
                    con el cliente.
                    Los pedidos relacionados son:
                    """
                    for p in cliente.pedidosVenta:
                        txt += "Pedido número %s. Fecha %s.\n" % (
                                p.numpedido, p.fecha.strftime('%d/%m/%y'))
                    for o in cliente.presupuestos:
                        txt += "Oferta número %d. Fecha %s.\n" % (
                                o.id, o.fecha.strftime('%d/%m/%y'))
                    utils.dialogo_info(titulo = 'ERROR: NO SE PUDO BORRAR',
                                       texto = txt,
                                       padre = self.wids['ventana'])

    def _ver_pedidos(self, boton):
        """
        Muestra todos los pedidos asignados
        al cliente actual.
        """
        cliente = self.objeto
        if cliente == None: return
        pedidosventa = pclases.PedidoVenta.select(
                        pclases.PedidoVenta.q.clienteID == cliente.id,
                        orderBy = "fecha")
        pedidos = [(p.id, p.numpedido, utils.str_fecha(p.fecha))
                   for p in pedidosventa]
        idpedido = utils.dialogo_resultado(pedidos,
                                           'PEDIDOS HECHOS POR EL CLIENTE',
                                           cabeceras = ('ID',
                                                        'Número de pedido',
                                                        'Fecha'),
                                           padre = self.wids['ventana'],
                                           func_change = self.abrir_pedido)
        if idpedido > 0:
            from formularios import pedidos_de_venta
            p = pedidos_de_venta.PedidosDeVenta(
                    pclases.PedidoVenta.get(idpedido),
                    usuario = self.usuario)

    def ver_pedidos(self, boton):
        """
        Nuevo ver pedidos. Sustituye al diálogo resultado que se abría antes.
        Ahora se abre la consulta adecuada con el cliente de la ventana.
        CWT
        """
        from formularios import consulta_pedidos_clientes
        ventana = consulta_pedidos_clientes.ConsultaPedidosCliente(  # @UnusedVariable
                    usuario = self.usuario,
                    objeto = self.objeto)

    def ver_presupuestos(self, boton):
        """
        Muestra todos los presupuestos hechos
        al cliente actual.
        """
        cliente = self.objeto
        if cliente == None:
            return
        presupuestos = [(p.id,
                         utils.str_fecha(p.fecha),
                         p.nombrecliente,
                         p.personaContacto,
                         ", ".join([pedido.numpedido
                                    for pedido in p.get_pedidos()]))
                        for p in cliente.presupuestos]
        idpresupuesto = utils.dialogo_resultado(presupuestos,
                            'OFERTAS HECHAS AL CLIENTE %s' % (cliente.nombre),
                            cabeceras = ('ID', 'Fecha', "Cliente final",
                                         "Contacto", "Pedidos relacionados"),
                            padre = self.wids['ventana'])
        if idpresupuesto > 0:
            from formularios import presupuestos
            p = presupuestos.Presupuestos(
                    objeto = pclases.Presupuesto.get(idpresupuesto),
                    usuario = self.usuario)

    def ver_productos(self, boton):
        from formularios import consulta_productos_comprados
        ventana = consulta_productos_comprados.ConsultaProductosComprados(  # @UnusedVariable
                    usuario = self.usuario,
                    objeto = self.objeto)

    def _ver_productos(self, boton):
        """
        Muestra todos los productos relacionados
        con el cliente actual a través de las
        Facturas<->LDV<->Artículos.
        """
        cliente = self.objeto
        if cliente == None: return
        productos = {}
        #for pedido in cliente.pedidosVenta:
        for factura in cliente.facturasVenta:
            for ldv in factura.lineasDeVenta:
                producto = ldv.producto
                if ldv.productoVenta != None:
                    linea_producto = ["PV:%d" % (ldv.productoVenta.id),
                                      ldv.productoVenta.codigo,
                                      ldv.productoVenta.descripcion,
                                      ldv.cantidad]
                elif ldv.productoCompra != None:
                    linea_producto = ["PC:%d" % (ldv.productoCompra.id),
                                      ldv.productoCompra.codigo,
                                      ldv.productoCompra.descripcion,
                                      ldv.cantidad]
                else:
                    continue
                if not producto in productos:
                    productos[producto] = linea_producto
                else:
                    productos[producto][-1] += linea_producto[-1]
        productos = [tuple(productos[p][:-1]) + ("%s %s" % (
                        utils.float2str(productos[p][-1], autodec = True),
                        p.unidad),)
                     for p in productos]
        idproducto = utils.dialogo_resultado(productos,
                        'PRODUCTOS COMPRADOS POR EL CLIENTE',
                        cabeceras=('ID', 'Código', 'Descripción', "Facturado"),
                        padre = self.wids['ventana'])
        if idproducto not in (-1, -2):
            if "PV" in idproducto:
                producto = pclases.ProductoVenta.get(idproducto.split(":")[1])
                if producto.es_rollo():
                    from formularios import productos_de_venta_rollos
                    NewWin = productos_de_venta_rollos.ProductosDeVentaRollos
                elif producto.es_bala() or producto.es_bigbag():
                    from formularios import productos_de_venta_balas
                    NewWin = productos_de_venta_balas.ProductosDeVentaBalas
            elif "PC" in idproducto:
                producto = pclases.ProductoCompra.get(idproducto.split(":")[1])
                from formularios import productos_compra
                NewWin = productos_compra.ProductosCompra
            else:
                NewWin = None
            if NewWin:
                ventana_producto = NewWin(producto, usuario=self.usuario)

    def crear_nuevo_contador(self,boton):
        """
        Crea un nuevo contador y lo asocia al cliente actual
        """
        if self.usuario and self.usuario.nivel > 2:
            utils.dialogo_info(titulo = "USUARIO SIN PRIVILEGIOS",
                texto = "No puede crear nuevos contadores desde esta ventana.",
                padre = self.wids['ventana'])
            return
        prefijo = utils.dialogo_entrada(titulo = 'PREFIJO',
                    texto = 'Introduzca el prefijo para el contador',
                    padre = self.wids['ventana'])
        sufijo = utils.dialogo_entrada(titulo = 'SUFIJO',
                    texto = 'Introduzca el sufijo para el contador',
                    padre = self.wids['ventana'])
        if prefijo != None and sufijo != None:
            contador = pclases.Contador(contador = 0, prefijo = prefijo,
                                        sufijo = sufijo)
            pclases.Auditoria.nuevo(contador, self.usuario, __file__)
        else:
            return
        cliente = self.objeto
        cliente.notificador.set_func(lambda: None)
        cliente.contador = contador
        cliente.syncUpdate()
        # Vuelvo a activar el notificador
        cliente.notificador.set_func(self.aviso_actualizacion)
        self.actualizar_ventana(objeto_anterior = cliente)
        self.wids['cmb_contador'].clear()
        utils.rellenar_lista(self.wids['cmb_contador'],
            [(c.id, 'Prefijo:'+c.prefijo +' |Sufijo:'+c.sufijo)
             for c in pclases.Contador.select(orderBy="prefijo")])

    def seleccionar_contador(self, wid):
        """
        Asigna el contador seleccionado mediante el combo al cliente
        """
        # DONE: Hacer que si tenía ya un contador seleccionado, se actualicen
        # todas sus facturas cambiando (si es posible) el prefijo y sufijo del antiguo por el nuevo.
        idcontador = utils.combo_get_value(wid)
        if idcontador != None:
            contador = pclases.Contador.get(idcontador)
            cliente = self.objeto
            contador_antiguo = cliente.contador
            cliente.notificador.set_func(lambda : None)
            if self.wids['b_guardar'].get_property("sensitive") == True:
                self.guardar()
            cliente.contador = contador
            cliente.syncUpdate()
            # for fra in cliente.facturasVenta:
            #     numfactura = fra.numfactura
            #     numfactura = numfactura.replace(contador_antiguo.prefijo, '')
            #     numfactura = numfactura.replace(contador_antiguo.sufijo, '')
            #     numfactura = "%s%s%s" % (contador.prefijo, numfactura, contador.sufijo)
            #     fra.numfactura = numfactura
            cliente.notificador.set_func(self.aviso_actualizacion)
            if contador_antiguo != contador:
                self.actualizar_ventana()

    def asignar_tarifa(self,wid):
        """
        Muestra las tarifas registradas en el sistema y
        permite asignársela a un cliente
        """
        tarifas = pclases.Tarifa.select()
        ops = []
        for t in tarifas:
            ops.append((t.id,t.nombre))
        if ops == []:
            utils.dialogo_info(titulo = 'ERROR',
                    texto = 'No hay tarifas registradas en el sistema',
                    padre = self.wids['ventana'])
        else:
            self.objeto.tarifa = utils.dialogo_combo(
                    titulo = 'Seleccione tarifa',
                    ops = ops,
                    padre = self.wids['ventana'])
            self.actualizar_ventana(deep_refresh = False)


def buscar_clientes_obras(txt):
    """
    Busca y devuelve un SQLlist con todos los clientes correspondientes a
    obras cuyo nombre coincida en parte con el texto recibido.
    """
    criterios = []
    for palabra in txt.split():
        criterios.append(pclases.Obra.q.nombre.contains(palabra))
    if len(criterios) > 1:
        obras = pclases.Obra.select(pclases.AND(*criterios))
    elif len(criterios) == 1:
        obras = pclases.Obra.select(criterios[0])
    else:
        obras = pclases.Obra.select()
    res = []
    for o in obras:
        for cliente in o.clientes:
            if cliente and cliente not in res:
                res.append(cliente)
    res = pclases.SQLlist(res)
    return res

def copy_to_clipboard(texto):
    """Copia el texto recibido en el portapapeles y lo hace disponible a
    otras aplicaciones.

    :texto: Texto a copiar
    """
    try:
        from Tkinter import Tk
        r = Tk()
        r.clipboard_append(texto)
    except ImportError:
        # Solo funciona entre aplicaciones GTK. MERDE!
        # Parece que Tkinter tiene algo mejor para mí. Intento eso primero.
        clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(texto)
        try:
            clipboard.store()
        except:    # pyGTK < 2.6
            pass

def check_presupuestos_sin_cliente(cliente, ventana_padre = None):
    """
    Comprueba si el cliente que se acaba de dar de alta es porque se le
    ha creado un presupuesto. En ese caso hay que relacionarlos.
    """
    from formularios.ventana_progreso import VentanaProgreso
    vpro = VentanaProgreso(padre = ventana_padre)
    vpro.mostrar()
    sincliente = pclases.Presupuesto.select(
            pclases.Presupuesto.q.cliente == None)
    tot = sincliente.count()
    i = 0.0
    for p in sincliente:
        vpro.set_valor(i / tot, "Comprobando ofertas con cliente pendiente...")
        if p.nombrecliente == cliente.nombre:
            p.cliente = cliente
            p.syncUpdate()
        i += 1
    vpro.ocultar()


if __name__ == '__main__':
    v = Clientes()

