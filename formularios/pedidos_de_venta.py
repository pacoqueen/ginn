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
## pedidos_de_venta.py - Ventana de pedidos de venta. 
###################################################################
## NOTAS:
##  Normas de estilo: Los títulos de los diálogos modales siempre
##   en mayúsculas. Resto de elementos, ver miniguía de usabilidad.
## ----------------------------------------------------------------
## Otra forma de meter colores en TreeViews:
##To change the color of an entire column, you can change the foreground and background properties of the renderer:
##
## renderer = gtk.CellRendererText()
## renderer.set_property("foreground", "red")
## # ... and use renderer in TreeViewColumn 
##
##To change the color of specific rows or cells in a TreeView, use the foreground and background arguments to GtkTreeViewColumn. The example below demonstrates their usage:
##
## model = gtk.ListStore(str, str, str, str)
## model.append(("Henrik","Ibsen","green","#23abff"))
## model.append(("Samuel","Beckett","orange","OldLace"))
## model.append(("Thomas","Mann","yellow","peach puff"))
## treeview = gtk.TreeView(model)
## renderer = gtk.CellRendererText()
## treeview.append_column(gtk.TreeViewColumn("First Name", renderer, 
##                        text=0, foreground=2, background=3))
## treeview.append_column(gtk.TreeViewColumn("Last Name", renderer,
##                        text=1, foreground=3, background=2))
##
##As always with TreeViewColumn, the arguments indicate which field in the module carries the relevant value. For the first column in the first row, for instance, text will come from field 0 ("Henrik"), background colour from field 2 ("#23abff").
##
##(Walter Anger)
##
## ----------------------------------------------------------------
##  
###################################################################
## Changelog:
## 18 de septiembre de 2005 -> Inicio
## 18 de septiembre de 2005 -> 99% funcional
## 9 de diciembre de 2005 -> Añadido IVA por defecto.
## 12 de diciembre de 2005 -> Resuelta incidencia #0000038.
## 10 de enero de 2006 -> Añadida producción bajo demanda.
## 18 de enero de 2006 -> Cambio radical. Fork y versión 0.2.
## 22 de enero de 2006 -> Encapsulo todo en una clase. Es más 
##                        limpio y permite llamadas entre ventanas.
## 15 de febrero de 2006 -> Añadida funcionalidad de tarifas
###################################################################
## - DONE: No hay hueco en el formulario para el subtotal antes de
##         aplicar descuento e iva.
## - DONE: Falta bloquear el pedido y cerrarlo (no contar faltas 
##         aunque la cantidad pedida > servida).
## DONE: Hacer un botón facturar que emita una factura del tirón 
##       calcada al pedido. Siempre que no lleve productos de 
##       venta que requieran códigos de trazabilidad.
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time 
try:
    import pclases
except ImportError:
    import sys
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    import pclases
import mx.DateTime
from ventana_progreso import VentanaProgreso
import pango
import postomatic

def preguntar_precio(producto, ventana_padre = None):
    """
    Muestra un diálogo para preguntar el precio del producto 
    recibido como parámetro.
    Se usará para cuando no tenga un precio en tarifa y el 
    precio por defecto sea 0.
    """
    precio = utils.dialogo_entrada(titulo = "INTRODUZCA PRECIO", 
                                   texto = """
            No se encontró tarifa para el producto.                 
            Escriba un precio para el mismo:                        
            """, 
                                    padre = ventana_padre, 
                                    valor_por_defecto = '0')
    try:
        precio = utils._float(precio)
    except:
        utils.dialogo(titulo = "ERROR DE FORMATO",
                      texto = "El texto %s no es correcto.\n\nSe usará precio 0.\nCámbielo a continuación si es necesario." % (precio),
                      padre = ventana_padre)
        precio = 0
    return precio
         


class PedidosDeVenta(Ventana):

    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self.ldvs = {}
        self.ldps = {}
        self._objetoreciencreado = None
        Ventana.__init__(self, 'pedidos_de_venta.glade', objeto, 
                         usuario = self.usuario)
        connections = {'b_nuevo/clicked': self.crear_nuevo_pedido,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_buscar/clicked': self.buscar_pedido,
                       'b_fecha/clicked': self.buscar_fecha,
                       'b_add_ldp/clicked': self.add_ldp,
                       'b_drop_ldp/clicked': self.drop_ldp,
                       'b_add_ldv/clicked': self.add_ldv,
                       'b_drop_ldv/clicked': self.drop_ldv,
                       'b_borrar/clicked': self.borrar,
                       'cbe_cliente/changed': 
                            self.cambiar_datos_relacionados_con_cliente, 
                       'b_aplicar_tarifa/clicked': self.aplicar_tarifa,
                       'b_vencimientos/clicked': self.ver_vencimientos,
                       'b_cobros/clicked': self.ver_cobros,
                       'b_facturas/clicked': self.ver_facturas,
                       'b_abonos/clicked': self.ver_abonos,
                       'b_tarifa_ldv/clicked': self.cambiar_tarifa_ldv,
                       'ch_transporte/toggled': self.cambiar_cargo_transporte,
                       'b_ver_albaranes/clicked': self.ver_albaranes,
                       'b_unificar/clicked': self._unificar_ldps, 
                       'b_salir/clicked': self.salir, 
                       'b_add_srv/clicked': self.add_servicio, 
                       'b_drop_srv/clicked': self.drop_servicio, 
                       'b_reciente/pressed': self.abrir_recientes, 
                       'b_facturar/clicked': self.facturar, 
                       #'cb_obra/changed': 
                       #     self.cambiar_direccionCorrespondencia
                       }  
        self.add_connections(connections)
        self.inicializar_ventana()
        self.conectar_dircorrespondencia()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        gtk.main()

    def conectar_dircorrespondencia(self):
        """
        Conecta la señal changed del combo de obra para que cambie la 
        dirección de correspondencia.
        """
        self.handler_obra = self.wids['cb_obra'].connect(
            "changed", self.cambiar_direccionCorrespondencia)

    def desconectar_dircorrespondencia(self):
        """
        Desconecta el manejador que cambia la dirección de correspondencia al 
        cambiar de obra.
        """
        self.wids['cb_obra'].disconnect(self.handler_obra)

    def cambiar_datos_relacionados_con_cliente(self, combo):
        #self.cambiar_direccionCorrespondencia(combo)
        self.rellenar_obras(combo)

    def rellenar_obras(self, combo):
        """
        Rellena el model del comboBox de obras con las obras del cliente y 
        selecciona la genérica en caso de que el pedido no tenga obra o 
        la que tenga no pertenezca al cliente.
        """
        idcliente = utils.combo_get_value(combo)
        if idcliente:
            cliente = pclases.Cliente.get(idcliente)
            cliente.sync()
            if self.objeto.obra not in cliente.obras or not self.objeto.obra:
                self.objeto.obra = cliente.get_obra_generica()
            utils.rellenar_lista(self.wids['cb_obra'], 
                                 [(o.id, o.nombre) for o in cliente.obras])
            utils.combo_set_from_db(self.wids['cb_obra'], self.objeto.obra.id)
        else:
            self.objeto.obra = None
            utils.rellenar_lista(self.wids['cb_obra'], [])
            utils.combo_set_from_db(self.wids['cb_obra'], None)

    def cambiar_direccionCorrespondencia(self, combo):
        #idcliente = utils.combo_get_value(combo)
        #if idcliente:
        #    cliente = pclases.Cliente.get(idcliente)
        #    nombre_correspondencia = cliente.nombre
        #    direccion_correspondencia = cliente.direccion
        #    cp_correspondencia = cliente.cp
        #    ciudad_correspondencia = cliente.ciudad
        #    provincia_correspondencia = cliente.provincia
        #    pais_correspondencia = cliente.pais
        #    self.wids['e_nombreCorrespondencia'].set_text(
        #        nombre_correspondencia)
        #    self.wids['e_direccionCorrespondencia'].set_text(
        #        direccion_correspondencia)
        #    self.wids['e_cpCorrespondencia'].set_text(cp_correspondencia)
        #    self.wids['e_ciudadCorrespondencia'].set_text(
        #        ciudad_correspondencia)
        #    self.wids['e_provinciaCorrespondencia'].set_text(
        #        provincia_correspondencia)
        #    self.wids['e_paisCorrespondencia'].set_text(pais_correspondencia)
        # GTX4
        idobra = utils.combo_get_value(self.wids['cb_obra'])
        if idobra:
            obra = pclases.Obra.get(idobra)
            nombre_correspondencia = obra.nombre
            direccion_correspondencia = obra.direccion
            cp_correspondencia = obra.cp
            ciudad_correspondencia = obra.ciudad
            provincia_correspondencia = obra.provincia
            idcliente = utils.combo_get_value(self.wids['cbe_cliente'])
            try:
                cliente = pclases.Cliente.get(idcliente)
                pais_correspondencia = cliente.pais
            except AttributeError:
                pais_correspondencia = ""
            self.wids['e_nombreCorrespondencia'].set_text(
                nombre_correspondencia)
            self.wids['e_direccionCorrespondencia'].set_text(
                direccion_correspondencia)
            self.wids['e_cpCorrespondencia'].set_text(cp_correspondencia)
            self.wids['e_ciudadCorrespondencia'].set_text(
                ciudad_correspondencia)
            self.wids['e_provinciaCorrespondencia'].set_text(
                provincia_correspondencia)
            self.wids['e_paisCorrespondencia'].set_text(
                pais_correspondencia)

    # XXX: Lista de objetos recientes.
    def abrir_recientes(self, boton):
        """
        Muestra un desplegable con los pedidos recientemente abiertos. Al 
        hacer clic en uno de ellos, se abre en la ventana actual.
        """
        reg = pclases.ListaObjetosRecientes.buscar("pedidos_de_venta.py", 
                                                   self.usuario) 
        if reg:
            lista = []
            ui_string = """
                        <ui>
                            <popup name='Popup'>
                        """
            for id in reg.get_lista():
                try:
                    p = pclases.PedidoVenta.get(id)
                except pclases.SQLObjectNotFound:
                    pass    # Pedido borrado.
                else:
                    ui_string += "<menuitem action='%s'/>" % (
                            utils.sanitize(p.get_info()))
                    lista.append((utils.sanitize(p.get_info()), p.id))
            ui_string += """
                            </popup>
                        </ui>
                        """
            ag = gtk.ActionGroup("Recientes")
            actions = []
            for info, id in lista:
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
        Abre en la ventana actual el pedido seleccionado en el popup.
        """
        accel_path = action.get_accel_path()
        txt_entrada = "/".join(accel_path.split("/")[2:])
        for txt, id in lista:
            if txt == txt_entrada:
                pedido = pclases.PedidoVenta.get(id)
                # XXX: Añado a objetos recientes.
                objsr = pclases.ListaObjetosRecientes.buscar(
                                                        "pedidos_de_venta.py", 
                                                        self.usuario, 
                                                        crear = True)
                objsr.push(pedido.id)
                # XXX: End Of Añado a objetos recientes.
                self.desconectar_dircorrespondencia()
                self.ir_a(pedido)
                self.conectar_dircorrespondencia()

    # XXX: End Of Lista de objetos recientes.

    def add_servicio(self, widget):
        """
        Añade un servicio al pedido.
        """
        if self.objeto != None:
            concepto = utils.dialogo_entrada(titulo = "CONCEPTO", 
                        texto = "Introduzca el concepto del servicio o "
                                "transporte:", 
                        padre = self.wids['ventana'])
            if concepto != None:
                srv = pclases.Servicio(pedidoVenta = self.objeto, 
                                       facturaVenta = None, 
                                       albaranSalida = None, 
                                       concepto = concepto, 
                                       cantidad = 0, 
                                       precio = 0, 
                                       descuento = 0)
                pclases.Auditoria.nuevo(srv, self.usuario, __file__)
                self.actualizar_ventana()

    def drop_servicio(self, widget):
        """
        Elimina el servicio seleccionado del pedido.
        Si el servicio tiene pedido, albarán y factura a None 
        lo elimina también de la base de datos.
        """
        seleccion = self.wids['tv_servicios'].get_selection()
        model, iter = seleccion.get_selected()
        if iter == None: 
            utils.dialogo_info('SELECCIONE UN SERVICIO', 
                               'Debe seleccionar el servicio a eliminar del '
                               'pedido.', 
                               padre = self.wids['ventana'])
            return
        txt = "\n\t¿Está seguro de que desea eliminar el servicio "\
              "seleccionado del pedido?\t"
        if not utils.dialogo(titulo = '¿BORRAR?', 
                             texto = txt, 
                             padre = self.wids['ventana']):
            return
        idsrv = model[iter][-1]
        srv = pclases.Servicio.get(idsrv)
        if (srv.albaranSalida != None or srv.facturaVenta != None 
            or srv.prefactura != None):
            txt =  """
            La línea seleccionada corresponde a un servicio que         
            ya ha sido vinculado con un albarán o incluso ya            
            se ha facturado.                                            
            Compruébelo y elimine primero el servicio del               
            albarán o factura y vuelva a intentarlo.
            """ % (srv.albaranSalida.numalbaran)
            utils.dialogo_info(titulo = 'NO SE PUDO ELIMINAR',
                               texto = txt, 
                               padre = self.wids['ventana'])
            return
        srv.pedidoVenta = None
        if srv.presupuesto == None:
            try:
                srv.destroy(ventana = __file__)
            except:
                self.logger.error("%spedidos_de_venta.py::drop_servicio -> No"
                                  " se pudo eliminar el servicio ID %d." % (
                                    self.usuario 
                                    and self.usuario.usuario + ": " 
                                    or "", srv.id))
        self.guardar(None)  # Por si no están guardadas la fecha y proveedor
        self.actualizar_ventana()

 

    def _unificar_ldps(self, boton):
        """
        Wrapper.
        """
        unificar_ldps(self.objeto)
        self.actualizar_ventana()

    def pedir_producto(self):
        """
        Solicita un código, nombre o descripcicón 
        de producto, muestra una ventana de resultados 
        coincidentes con la búsqueda y devuelve una 
        lista de ids de productos o [] si se cancela o 
        no se encuentra.
        """
        productos = []
        txt = utils.dialogo_entrada(texto = 'Introduzca código, nombre o '
                                            'descripción de producto.\nPuede '
                                            'usar también el código de '
                                            'COMPOSAN si está buscando '
                                            'geotextiles.', 
                                    titulo = 'CÓDIGO PRODUCTO', 
                                    padre = self.wids['ventana'])
        if txt != None:
            criterio = pclases.OR(pclases.ProductoVenta.q.codigo.contains(txt),
                            pclases.ProductoVenta.q.nombre.contains(txt),
                            pclases.ProductoVenta.q.descripcion.contains(txt))
            prods = pclases.ProductoVenta.select(criterio)
            rollos = pclases.CamposEspecificosRollo.select(
                        pclases.CamposEspecificosRollo.q.codigoComposan == txt)
            productos = [p.id for p in prods]
            productos += [p.productosVenta[0].id for p in rollos if len(p.productosVenta) == 1 and p.productosVenta[0].id not in productos]
        return productos
        
    def refinar_busqueda(self, resultados):
        """
        resultados es una lista de id de productos.
        """
        resultados = [pclases.ProductoVenta.get(id) for id in resultados]
        filas_res = [(p.id, p.codigo, p.nombre, p.descripcion, "CLIC PARA VER", "CLIC PARA VER") for p in resultados]
        idproducto = utils.dialogo_resultado(filas_res,
                                             titulo = 'Seleccione producto',
                                             cabeceras = ('ID Interno', 'Código', 'Nombre', 'Descripción', 'Existencias (uds.)', 'Stock'),
                                             func_change = self.mostrar_info_stock, 
                                             padre = self.wids['ventana'])
        if idproducto < 0:
            return None
        else:
            return [idproducto]

    def mostrar_info_stock(self, tv):
        model, iter = tv.get_selection().get_selected()
        if iter!=None and model[iter][-1] == "CLIC PARA VER":
            vpro = VentanaProgreso(padre = self.wids['ventana'])
            vpro.mostrar()
            vpro.set_valor(0.0, "Contando existencias en almacén...")   
                # PLAN: Algún día habrá que cachear el rollo de las existencias, porque recontar cada 
                # vez que se necesita es un coñazo y dentro de poco va a ser lento de cojones.
            producto = pclases.ProductoVenta.get(model[iter][0])   # En los diálogos de resultado va al revés.
            vpro.set_valor(0.25, "Contando existencias en almacén...")   
            stock = producto.get_stock()
            vpro.set_valor(0.5, "Contando existencias en almacén...")   
            model[iter][-1] = stock
            vpro.set_valor(0.75, "Contando existencias en almacén...")   
            model[iter][-2] = producto.existencias
            vpro.ocultar()

    def get_ldvs_from_pedido(self, pedido):
        """
        Devuelve las líneas de venta que pertenecen 
        al self.objeto especificado como un SelectResults.
        Si self.objeto es None u ocurre un error, devuelve None.
        """
        if self.objeto == None:
            return None
        return pclases.LineaDeVenta.select(pclases.LineaDeVenta.q.pedidoVentaID==pedido.id)

    def es_diferente(self):
        """
        Devuelve True si la información en pantalla es distinta a la
        del objeto en memoria.
        """
        self.objeto
        if self.objeto == None: return False # Si no hay self.objeto activo, devuelvo que no hay cambio respecto a la ventana
        condicion = self.objeto.numpedido == self.wids['e_numpedido'].get_text()
        condicion = condicion and (utils.str_fecha(self.objeto.fecha) == self.wids['e_fecha'].get_text())
        try:
            condicion = (condicion and 
                        ((self.objeto.tarifa == None and utils.combo_get_value(self.wids['cbe_tarifa']) == None) or 
                        (self.objeto.tarifa.id == utils.combo_get_value(self.wids['cbe_tarifa']))))
        except AttributeError:  # No tiene cliente pero en cbe_tarifa hay algo activo
            return True # Es diferente y no sigo chequeando campos
        try:
            condicion = (condicion and 
                        ((self.objeto.cliente == None and utils.combo_get_value(self.wids['cbe_cliente']) == None) or 
                        (self.objeto.cliente.id == utils.combo_get_value(self.wids['cbe_cliente']))))
        except AttributeError:  # No tiene cliente pero en cbe_cliente hay algo activo
            return True # Es diferente y no sigo chequeando campos
        try:
            condicion = condicion and (self.objeto.descuento == utils.parse_porcentaje(self.wids['e_descuento'].get_text(), fraccion = True))
            condicion = condicion and ((self.objeto.iva < 0)
                                       or (self.objeto.iva == utils.parse_porcentaje(self.wids['e_iva'].get_text(), True)))
        except ValueError, msg:
            self.logger.error("pedidos_de_venta::es_diferente-> Error al intepretar porcentaje: %s" % (msg))
        condicion = condicion and self.objeto.bloqueado == self.wids['bloqueado'].get_active()
        condicion = condicion and self.objeto.cerrado == self.wids['cerrado'].get_active()
        condicion = condicion and self.objeto.transporteACargo == self.wids['ch_transporte'].get_active()
        idcomercial = utils.combo_get_value(self.wids['cbe_comercial'])
        if idcomercial == -1:
            idcomercial = None
        condicion = condicion and self.objeto.comercialID == idcomercial
        idfdp = utils.combo_get_value(self.wids['cbe_fdp'])
        condicion = condicion and self.objeto.formaDePagoID == idfdp
        condicion = condicion and self.objeto.direccionCorrespondencia == self.wids['e_direccionCorrespondencia'].get_text()
        condicion = condicion and self.objeto.nombreCorrespondencia == self.wids['e_nombreCorrespondencia'].get_text()
        condicion = condicion and self.objeto.cpCorrespondencia == self.wids['e_cpCorrespondencia'].get_text()
        condicion = condicion and self.objeto.ciudadCorrespondencia == self.wids['e_ciudadCorrespondencia'].get_text()
        condicion = condicion and self.objeto.provinciaCorrespondencia == self.wids['e_provinciaCorrespondencia'].get_text()
        condicion = condicion and self.objeto.paisCorrespondencia == self.wids['e_paisCorrespondencia'].get_text()
        condicion = condicion and self.objeto.textoObra == self.wids['e_obra'].get_text()
        try:
            condicion = (condicion and 
                ((self.objeto.obra == None 
                  and utils.combo_get_value(self.wids['cb_obra']) == None) 
                 or 
                 (self.objeto.obra.id 
                    == utils.combo_get_value(self.wids['cb_obra']))))
        except AttributeError:  # No tiene cliente pero en cb_obra hay algo activo
            return True # Es diferente y no sigo chequeando campos
        return not condicion    # Condición verifica que sea igual

    def cambiar_por_combo(self, tv, numcol):
        # OJO: NO USAR.
        # Con una columna aparte tipo texto y tal sí funciona.
        # Cuando intento hacerlo con dos columnas en el combo y asociando el 
        # float del precio... 
        # violación de segmento. Algo estaré haciendo mal, pero no sé el qué. 
        # Tampoco me parece buena idea asociar LDVs con tarifas de forma 
        # independiente, así que lo dejo como está.
        import gobject
        column = tv.get_column(numcol)
        column.clear()
        model = gtk.ListStore(gobject.TYPE_FLOAT, gobject.TYPE_STRING)
        model.append((0.1, "Tarifa 1"))
        model.append((0.2, "Parifa 2"))
        cellcombo = gtk.CellRendererCombo()
        cellcombo.set_property("model", model)
        cellcombo.set_property("text-column", 0)
        cellcombo.set_property("editable", True)
        def guardar_combo(cell, path, text, model, numcol):
            print model[path][numcol], text, " -> "
            model[path][numcol] = text
            print model[path][numcol], text
        cellcombo.connect("edited", guardar_combo, tv.get_model(), numcol)
        # column = gtk.TreeViewColumn("Test", cellcombo)
        column.pack_start(cellcombo)
        column.set_attributes(cellcombo, text = numcol)
        # tv.insert_column(column, 4)

    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
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
        self.wids['e_total_ldvs'].modify_base(gtk.STATE_NORMAL, 
                self.wids['e_total_ldvs'].get_colormap().alloc_color(
                    "PaleGreen"))
        font_desc = pango.FontDescription('Sans Oblique Condensed 8')
        self.wids['e_total_ldvs'].modify_font(font_desc)
        self.wids['e_subtotal'].set_alignment(1.0)
        self.wids['e_total_ldvs'].set_alignment(0.0)
        # Inicialización del resto de widgets:
        utils.rellenar_lista(self.wids['cbe_cliente'], 
                             [(c.id, "%s (%s, %s - %s)" % (
                                c.nombre, 
                                c.cif, 
                                c.ciudad, 
                                c.provincia)) 
                              for c 
                              in pclases.Cliente.select(
                                pclases.Cliente.q.inhabilitado == False, 
                                orderBy="nombre")
                             ])
        cols = (('Código', 'gobject.TYPE_STRING', False, True, False, None),
                ('Descripción', 'gobject.TYPE_STRING', False, True, True, None),
                ('Cantidad', 'gobject.TYPE_FLOAT', True, False, False, 
                    self.cambiar_cantidad),
                ('Precio', 'gobject.TYPE_FLOAT', True, False, False, 
                    self.cambiar_precio),
                ('Descuento', 'gobject.TYPE_STRING', True, False, False, 
                    self.cambiar_descuento),
                ('Total de línea', 'gobject.TYPE_FLOAT', False, False, False, 
                    None),
                ('Bultos', 'gobject.TYPE_INT64', False, False, False, None),
                ('Albarán', 'gobject.TYPE_STRING', False, True, False, None),
                ('Fecha albarán', 'gobject.TYPE_STRING', False, True, False, 
                    None), 
                ('Factura', 'gobject.TYPE_STRING', False, True, False, None),
                ('Fecha factura', 'gobject.TYPE_STRING', False, True, False, 
                    None), 
                ('IDLDV', 'gobject.TYPE_INT64', False, False, False, None)
               )
        utils.preparar_listview(self.wids['tv_ldvs'], cols)
        cell = self.wids['tv_ldvs'].get_column(4).get_cell_renderers()[0]
        cell.set_property('xalign', 1.0)
        postomatic.attach_menu_notas(self.wids['tv_ldvs'], 
                                     pclases.LineaDeVenta, self.usuario, 1)
        # CWT: 4 decimales en precio y subtotal:
        self.wids['tv_ldvs'].get_column(3).set_cell_data_func(
                self.wids['tv_ldvs'].get_column(3).get_cell_renderers()[0], 
                utils.redondear_flotante_en_cell_cuando_sea_posible, 
                (3, 4))
        self.wids['tv_ldvs'].get_column(5).set_cell_data_func(
                self.wids['tv_ldvs'].get_column(5).get_cell_renderers()[0], 
                utils.redondear_flotante_en_cell_cuando_sea_posible, 
                (5, 4))
        cols = (('Código', 'gobject.TYPE_STRING', False, True, False, None),
                ('Descripción', 'gobject.TYPE_STRING', False, True, True, None),
                ('Cantidad', 'gobject.TYPE_FLOAT', True, False, False, 
                    self.cambiar_cantidad_ldp),
                ('Precio', 'gobject.TYPE_FLOAT', True, False, False, 
                    self.cambiar_precio_ldp),
                ('Descuento', 'gobject.TYPE_STRING', True, False, False, 
                    self.cambiar_descuento_ldp),
                ('Total de línea', 'gobject.TYPE_FLOAT', False, False, False, 
                    None),
                ('Bultos', 'gobject.TYPE_INT64', False, False, False, None),
                ('Fecha entrega', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_fecha_entrega), 
                ('Texto entrega', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_texto_entrega), 
                ('Total solicitado del producto', 'gobject.TYPE_FLOAT', 
                    False, False, False, None),
                ('Cantidad servida', 'gobject.TYPE_FLOAT', 
                    False, False, False, None),
                ('IDLDP', 'gobject.TYPE_INT64', False, False, False, None)
               )
        utils.preparar_listview(self.wids['tv_ldps'], cols)
        cell = self.wids['tv_ldps'].get_column(4).get_cell_renderers()[0]
        cell.set_property('xalign', 1.0)
        # Para acelerar el colorear he metido dos columnas nuevas, que en el 
        # fondo no es necesario que vea el usuario, "so", las oculto:
        self.wids['tv_ldps'].get_column(9).set_visible(False)
        self.wids['tv_ldps'].get_column(10).set_visible(False)
        self.colorear()
        postomatic.attach_menu_notas(self.wids['tv_ldps'], 
                                     pclases.LineaDePedido, self.usuario, 1)
        # self.cambiar_por_combo(self.wids['tv_ldvs'], 3)        # Esto de 
            # las tarifas por LDV es un sinsentido.
        self.wids['tv_ldvs'].connect("row-activated", self.abrir_producto)
        self.wids['tv_ldps'].connect("row-activated", 
            self.abrir_producto_from_ldp)
        cols = (('Producto', 'gobject.TYPE_STRING', False, True, True, None), 
                ('Cantidad', 'gobject.TYPE_FLOAT', False, True, False, None), 
                ('IDProducto', 'gobject.TYPE_STRING', False, False, False, 
                    None))
        utils.preparar_listview(self.wids['tv_pendiente'], cols)
        cols = (('Producto', 'gobject.TYPE_STRING', False, True, True, None), 
                ('Cantidad', 'gobject.TYPE_FLOAT', False, True, False, None), 
                ('IDProducto', 'gobject.TYPE_STRING', False, False, False, 
                    None))
        utils.preparar_listview(self.wids['tv_pendiente_fact'], cols)
        cols = (('Cantidad', 'gobject.TYPE_STRING', True, True, False, 
                    self.editar_cantidad_srv), 
                ('Concepto', 'gobject.TYPE_STRING', True, True, True, 
                    self.editar_concepto_srv), 
                ('Precio', 'gobject.TYPE_STRING',  True, True, False, 
                    self.editar_precio_srv), 
                ('Descuento', 'gobject.TYPE_STRING', True, True, False, 
                    self.editar_descuento_srv), 
                ('Total', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Albarán', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Factura', 'gobject.TYPE_STRING', False, True, False, None), 
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_servicios'], cols)
        cell = self.wids['tv_servicios'].get_column(3).get_cell_renderers()[0]
        cell.set_property('xalign', 1.0)
        postomatic.attach_menu_notas(self.wids['tv_servicios'], 
                                     pclases.Servicio, self.usuario, 1)
        # ---------------------------------------------------------------------
        def iter_cliente_seleccionado(completion, model, iter):
            idcliente = model[iter][0]
            utils.combo_set_from_db(self.wids['cbe_cliente'], idcliente)
            try:
                #if self.objeto.tarifa == None:
                if 1:   #CWT: (BP) Que se ponga _siempre_ la tarifa 
                        # por defecto del cliente.
                    try:
                        utils.combo_set_from_db(self.wids['cbe_tarifa'], 
                                pclases.Cliente.get(idcliente).tarifa.id)
                    except:     # La tarifa ya no es válida para el pedido
                        objtarifa  = pclases.Cliente.get(idcliente).tarifa
                        txttarifa = (objtarifa and objtarifa.nombre 
                                     or "sin tarifa")
                        utils.dialogo_info(titulo = "ERROR TARIFA", 
                            texto = "La tarifa del cliente (%s) puede que no"
                                    " sea correcta.\nVerifique las fechas de "
                                    "validez de la misma y la del pedido." 
                                        % txttarifa, 
                            padre = self.wids['ventana'])
                        self.wids['cbe_tarifa'].set_active(-1)
                        self.wids['cbe_tarifa'].child.set_text('')
            except:
                self.wids['cbe_tarifa'].set_active(-1)
                self.wids['cbe_tarifa'].child.set_text('')
            iva = pclases.Cliente.get(idcliente).get_iva_norm() 
            self.wids['e_iva'].set_text('%s %%' % (utils.float2str(iva*100,0)))
        # ---------------------------------------------------------------------
        def cambiar_tarifa(combo):
            model = self.wids['cbe_cliente'].get_model()
            idcliente = utils.combo_get_value(combo)
            try:
                cliente = pclases.Cliente.get(idcliente)
                tarifa = cliente.tarifa
                if tarifa != None:
                    try:
                        utils.combo_set_from_db(self.wids['cbe_tarifa'], 
                                pclases.Cliente.get(idcliente).tarifa.id)
                    except:     # La tarifa ya no es válida para el pedido
                        objtarifa  = pclases.Cliente.get(idcliente).tarifa
                        txttarifa = (objtarifa and objtarifa.nombre 
                                     or "sin tarifa")
                        utils.dialogo_info(titulo = "ERROR TARIFA", 
                            texto = "La tarifa del cliente (%s) puede que no "
                                    "sea correcta.\nVerifique las fechas de "
                                    "validez de la misma y la del pedido." 
                                        % txttarifa, 
                            padre = self.wids['ventana'])
                        self.wids['cbe_tarifa'].set_active(-1)
                        self.wids['cbe_tarifa'].child.set_text('')
            except:
                self.wids['cbe_tarifa'].set_active(-1)
                self.wids['cbe_tarifa'].child.set_text('')
            try:
                iva = cliente.get_iva_norm() 
            except:
                iva = 0.21
            self.wids['e_iva'].set_text('%s %%' % (utils.float2str(iva*100,0)))
        # ---------------------------------------------------------------------
        self.wids['cbe_cliente'].child.get_completion().connect(
            'match-selected', iter_cliente_seleccionado)
        self.wids['cbe_cliente'].connect("changed", cambiar_tarifa)
        self.wids['e_descuento'].set_alignment(1.0)
        self.wids['e_total_descuento'].set_alignment(1.0)
        self.wids['e_iva'].set_alignment(1.0)
        self.wids['e_total_iva'].set_alignment(1.0)
        self.wids['e_total'].set_alignment(1.0)
        # --- LISTA DE COMERCIALES
        comerciales = pclases.Comercial.select()
        utils.rellenar_lista(self.wids['cbe_comercial'], 
            [(c.id, c.empleado and c.empleado.get_nombre_completo() 
                or "ERR_INC_BD") 
              for c in comerciales] + [(-1, "Sin comercial relacionado")]) 
        utils.rellenar_lista(self.wids['cb_obra'], [])
        # --- Forma de cobro
        t = self.wids['e_descuento'].parent
        ncols = t.get_property("n-columns")
        nrows = t.get_property("n-rows")
        t.resize(ncols, nrows + 1)
        label = gtk.Label("Forma de cobro: ")
        label.set_justify(gtk.JUSTIFY_RIGHT)
        t.attach(label, 1, 2, nrows, nrows + 1)
        label.show()
        self.wids['cbe_fdp'] = gtk.ComboBoxEntry()
        self.wids['cbe_fdp'].show()
        fdps = [(fdp.id, fdp.toString()) 
                for fdp in pclases.FormaDePago.select(
                    pclases.FormaDePago.q.activa == True, 
                    orderBy = ("documento_de_pago_id", "plazo"))]
        #fdps.sort(key = lambda p: p[1])
        # TODO: Sería usable que se marcara con un astersico, en negrita o 
        #       algo la forma de pago del cliente. Para que el usuario lo 
        #       pudiera seleccionar ya que no se permite un valor por defecto
        #       para obligar al usuario a rellenarlo y evitar errores entre el 
        #       teclado y la silla.
        utils.rellenar_lista(self.wids['cbe_fdp'], fdps)
        t.attach(self.wids['cbe_fdp'], 2, ncols, nrows, nrows + 1)

    def abrir_producto_from_ldp(self,tv, path, view_column):
        """
        Abre el producto en la ventana de productos.
        """
        idldp = tv.get_model()[path][-1]
        ldp = pclases.LineaDePedido.get(idldp)
        # Abro el producto
        producto = ldp.productoVenta
        if producto != None:
            if producto.es_bala() or producto.es_bigbag():
                import productos_de_venta_balas
                ventana = productos_de_venta_balas.ProductosDeVentaBalas(
                    producto, usuario = self.usuario)
            elif producto.es_rollo():
                import productos_de_venta_rollos
                ventana = productos_de_venta_rollos.ProductosDeVentaRollos(
                    producto, usuario = self.usuario)
            elif producto.es_especial():
                import productos_de_venta_especial
                ventana = productos_de_venta_especial.ProductosDeVentaEspecial(
                    producto, usuario = self.usuario)
            else:
                self.logger.error("pedidos_de_venta.py::abrir_producto: "
                    "El producto ID %d no es bala, rollo ni bigbag." 
                        % producto.id)
        else:
            producto = ldp.productoCompra
            import productos_compra
            ventana = productos_compra.ProductosCompra(producto, 
                                                       usuario = self.usuario)

    def abrir_producto(self, tv, path, view_column):
        idldv = tv.get_model()[path][-1]
        ldv = pclases.LineaDeVenta.get(idldv)
        if ldv.albaranSalidaID != None:
            # Abro el albarán
            albaran = ldv.albaranSalida
            import albaranes_de_salida
            ventana = albaranes_de_salida.AlbaranesDeSalida(albaran)
        elif ldv.facturaVentaID != None:
            # Abro la factura
            factura = ldv.facturaVenta
            import facturas_venta
            ventana = facturas_venta.FacturasVenta(factura)
        elif ldv.prefacturaID != None:
            # Abro la prefactura
            factura = ldv.prefactura
            import prefacturas
            ventana = prefacturas.Prefacturas(factura)
        else:
            # Abro el producto
            producto = ldv.producto
            if isinstance(producto, pclases.ProductoVenta):
                if producto.es_bala() or producto.es_bigbag():
                    import productos_de_venta_balas
                    ventana = productos_de_venta_balas.ProductosDeVentaBalas(
                        producto)
                elif producto.es_rollo():
                    import productos_de_venta_rollos
                    ventana = productos_de_venta_rollos.ProductosDeVentaRollos(
                        producto)
                else:
                    self.logger.error("pedidos_de_venta.py::abrir_producto: "
                                      "El producto ID %d no es bala, bigbag "
                                      "ni rollo" % producto.id)
            elif isinstance(producto, pclases.ProductoCompra):
                import productos_compra
                ventana = productos_compra.ProductosCompra(producto)
    
    def check_permisos(self):
        """
        Activa o desactiva los controles dependiendo de los 
        permisos del usuario.
        """
        self.wids['b_facturar'].set_sensitive(not self.usuario 
                                              or self.usuario.nivel < 2)
        VENTANA = "pedidos_de_venta.py"
        if self.usuario != None and self.usuario.nivel > 0:
            ventanas = pclases.Ventana.select(
                pclases.Ventana.q.fichero == VENTANA)
            if ventanas.count() == 1:   # Siempre debería ser 1.
                permiso = self.usuario.get_permiso(ventanas[0])
                if permiso.escritura:
                    if self.usuario.nivel <= 1:
                        # print "Activo widgets para usuario con nivel de 
                        # privilegios <= 1."
                        self.activar_widgets(True, chequear_permisos = False)
                    else:
                        # print "Activo widgets porque permiso de escritura "\
                        #       "y objeto no bloqueado o recién creado."
                        self.activar_widgets(self.objeto != None and 
                                (not self.objeto.bloqueado 
                                 or self._objetoreciencreado == self.objeto), 
                            chequear_permisos = False)
                else:   # No tiene permiso de escritura. Sólo puede modificar 
                        # el objeto que acaba de crear.
                    if self._objetoreciencreado == self.objeto: 
                        # print "Activo widgets porque objeto recién creado"\
                        #       " aunque no tiene permiso de escritura."
                        self.activar_widgets(True, chequear_permisos = False)
                    else:
                        # print "Desactivo widgets porque no permiso de "\
                        #       "escritura."
                        self.activar_widgets(False, chequear_permisos = False)
                self.wids['b_buscar'].set_sensitive(permiso.lectura)
                # XXX: Modificación para recientes.
                self.wids['b_reciente'].set_sensitive(permiso.lectura)
                # XXX: EOModificación para recientes.
                self.wids['b_nuevo'].set_sensitive(permiso.nuevo)
        else:
            self.activar_widgets(True, chequear_permisos = False)

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
        ws = ('e_numpedido', 'e_fecha', 'b_fecha', 'cbe_cliente', 
              'cbe_tarifa', 'tv_ldps', 'bloqueado', 'cerrado', 
              'b_unificar', 'b_add_ldv', 'b_drop_ldv', 'b_borrar', 'tv_ldvs', 
              'b_tarifa_ldv', 'b_add_ldp', 'b_drop_ldp', 
              'b_aplicar_tarifa', 'ch_transporte', 'e_iva', 'e_descuento', 
              'tv_servicios', 'b_add_srv', 'b_drop_srv', 'cbe_cliente', 
              'cbe_comercial', 'e_nombreCorrespondencia', 
              'e_direccionCorrespondencia', 'e_cpCorrespondencia', 
              'e_ciudadCorrespondencia', 'e_provinciaCorrespondencia', 
              'e_paisCorrespondencia', 'cb_obra')
        if self.objeto == None:
            s = False
        for w in ws:
            self.wids[w].set_sensitive(s)
        # if self.usuario and self.usuario.nivel >= 2:
        #     self.wids['b_nuevo'].set_sensitive(False)
        # Aquí no se puede editar nada, dejemos que esté habilitado porque 
        # si no no se puede ni hacer scroll.
        self.wids['frame1'].set_sensitive(True)
        self.wids['frame2'].set_sensitive(True)
        self.wids['scrolledwindow3'].set_sensitive(True)
        if chequear_permisos:
            self.check_permisos()
        
    def ir_a_primero(self):
        """
        Hace que el primer registro -si lo hay- de la tabla implicada
        en el objeto del formulario sea el objeto activo.
        """
        self.desconectar_dircorrespondencia()
        try:
            # Anulo el aviso de actualización del envío que deja de ser activo.
            if self.objeto != None: self.objeto.notificador.desactivar()
            self.objeto = pclases.PedidoVenta.select(orderBy = "-id")[0] 
                # Selecciono todos y me quedo con el primero de la lista
            self.objeto.notificador.activar(self.aviso_actualizacion)        
                # Activo la notificación
        except IndexError:
            self.objeto = None   
        self.actualizar_ventana()
        self.conectar_dircorrespondencia()

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
                              r.numpedido, 
                              utils.str_fecha(r.fecha), 
                              r.get_nombre_cliente(), 
                              r.cerrado, 
                              r.bloqueado))
        idpedido = utils.dialogo_resultado(filas_res,
                                           titulo = 'Seleccione pedido',
                                           cabeceras = ('ID', 'Número de pedido', 'Fecha', 'Cliente', "Cerrado", "Bloqueado"),
                                           padre = self.wids['ventana'])
        if idpedido < 0:
            return None
        else:
            return idpedido

    def rellenar_widgets(self):
        """
        Introduce la información del pedido actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        if pclases.DEBUG:
            import time
            antes = time.time()
            print "Empieza rellenar_widgets:", antes
        self.rellenar_desplegable_tarifas()
        if pclases.DEBUG: 
            print "Después de rellenar_desplegable_tarifas:", time.time()-antes
        try:
            self.wids['e_numpedido'].set_text(self.objeto.numpedido)
        except:
            self.wids['e_numpedido'].set_text('')
        self.wids['e_fecha'].set_text(utils.str_fecha(self.objeto.fecha))
        self.suspender(self.wids['cbe_cliente'])
        if self.objeto.cliente != None:
            if self.objeto.cliente.inhabilitado:        
                # XXX Para los inhabilitados
                self.wids['cbe_cliente'].get_model().append(
                    (self.objeto.cliente.id, 
                     self.objeto.cliente.nombre + " (Inhabilitado)"))
            utils.combo_set_from_db(self.wids['cbe_cliente'], 
                                    self.objeto.cliente.id)
        else:
            self.wids['cbe_cliente'].set_active(-1)
            self.wids['cbe_cliente'].child.set_text('')
        self.revivir(self.wids['cbe_cliente'])
        if pclases.DEBUG: 
            print "Después suspender y revivir cliente:", time.time()-antes
        if self.objeto.tarifa != None:
            try:
                utils.combo_set_from_db(self.wids['cbe_tarifa'], 
                                        self.objeto.tarifa.id)
            except:     # La tarifa ya no es válida para el pedido
                utils.dialogo_info(titulo = "ERROR TARIFA", 
                                   texto = "La tarifa del pedido puede que "
                                           "no sea correcta.\nVerifique las "
                                           "fechas de validez de la misma y "
                                           "la del pedido.", 
                                   padre = self.wids['ventana'])
                self.wids['cbe_tarifa'].set_active(-1)
                self.wids['cbe_tarifa'].child.set_text('')
        else:
            self.wids['cbe_tarifa'].set_active(-1)
            self.wids['cbe_tarifa'].child.set_text('')
        if pclases.DEBUG: 
            print "Después de tarifa:", time.time()-antes
        subtotal_servido = self.rellenar_tabla(self.wids['tv_ldvs'])
        if pclases.DEBUG: 
            print "Después de rellenar_tabla:", time.time()-antes
        self.wids['e_total_ldvs'].set_text("%s € servidos (s/IVA)" % (
                                            utils.float2str(subtotal_servido)))
        subtotal = self.rellenar_tabla_ldp(self.wids['tv_ldps'])
        if pclases.DEBUG: 
            print "Después de rellenar_tabla_ldp:", time.time()-antes
        subtotal += self.rellenar_servicios()
        if pclases.DEBUG: 
            print "Después de rellenar_servicios:", time.time()-antes
        self.wids['e_subtotal'].set_text("%s €" % (utils.float2str(subtotal)))
        self.wids['e_descuento'].set_text('%.2f %%' % (
            self.objeto.descuento * 100))
        totdto = subtotal * (self.objeto.descuento)
        subtotal = subtotal - totdto
        self.wids['e_total_descuento'].set_text(utils.float2str(totdto))
        # OJO: Chequeo que haya un IVA válido y si no, corto por lo sano y 
        #      LO MACHACO para evitar problemas más adelante.
        self.wids['e_iva'].set_text('%s %%' % (
            utils.float2str(self.objeto.iva * 100, 0)))
        totiva = subtotal * self.objeto.iva
        self.wids['e_total_iva'].set_text(utils.float2str(totiva))
        total = subtotal + totiva
        self.wids['e_total'].set_text(utils.float2str(total))
        # self.objeto.transporteACargo = self.objeto.transporteACargo and len(self.objeto.servicios) == 0
        self.wids['ch_transporte'].set_active(self.objeto.transporteACargo)
        self.wids['cerrado'].set_active(self.objeto.cerrado)
        self.wids['bloqueado'].set_active(self.objeto.bloqueado)
        if pclases.DEBUG: 
            print "Después de rellenar totales:", time.time()-antes
        # Comerciales:
        utils.combo_set_from_db(self.wids['cbe_comercial'], 
            self.objeto.comercial and self.objeto.comercialID or -1)
        self.rellenar_pendiente()
        self.wids['e_obra'].set_text(self.objeto.textoObra)
        if pclases.DEBUG: 
            print "Después de comerciales:", time.time()-antes
        # Forma de pago:
        utils.combo_set_from_db(self.wids['cbe_fdp'], 
                self.objeto.formaDePago and self.objeto.formaDePagoID or None)
        # Dirección de correspondencia
        self.wids['e_nombreCorrespondencia'].set_text(
            self.objeto.nombreCorrespondencia)
        self.wids['e_direccionCorrespondencia'].set_text(
            self.objeto.direccionCorrespondencia)
        self.wids['e_cpCorrespondencia'].set_text(
            self.objeto.cpCorrespondencia)
        self.wids['e_ciudadCorrespondencia'].set_text(
            self.objeto.ciudadCorrespondencia)
        self.wids['e_provinciaCorrespondencia'].set_text(
            self.objeto.provinciaCorrespondencia)
        self.wids['e_paisCorrespondencia'].set_text(
            self.objeto.paisCorrespondencia)
        if pclases.DEBUG: 
            print "Después de dirección correspondencia:", time.time()-antes
        self.rellenar_obras(self.wids['cbe_cliente'])
        if pclases.DEBUG: 
            print "Después de rellenar_obras:", time.time()-antes
        self.objeto.make_swap()

    def rellenar_desplegable_tarifas(self):
        """
        Rellena el deplegable de tarifas solo con las que tienen una fecha 
        de validez final superior a la fecha del pedido o a la fecha actual
        si el pedido no tiene fecha, y al contrario con el periodo de validez 
        inicial. Añade también al principio una línea vacía para indicar y 
        seleccionar "Sin tarifa".
        """
        fecha_pedido = (self.objeto.fecha and self.objeto.fecha  
                        or mx.DateTime.localtime())
        tarifas_validas = pclases.Tarifa.select(pclases.AND(
            pclases.OR(pclases.Tarifa.q.periodoValidezIni == None, 
                       pclases.Tarifa.q.periodoValidezIni <= fecha_pedido), 
            pclases.OR(pclases.Tarifa.q.periodoValidezFin == None, 
                       pclases.Tarifa.q.periodoValidezFin >= fecha_pedido)), 
            orderBy="nombre")
        utils.rellenar_lista(self.wids['cbe_tarifa'], [(-1, "")] + [(t.id, t.nombre) for t in tarifas_validas])

    def rellenar_servicios(self):
        """
        Rellena el TreeView de servicios del pedido.
        Devuelve la suma de los subtotales de los servicios.
        """
        total = 0
        model = self.wids['tv_servicios'].get_model()
        model.clear()
        for srv in self.objeto.servicios:
            model.append((utils.float2str(srv.cantidad), 
                          srv.concepto, 
                          utils.float2str(srv.precio), 
                          "%s %%" % (utils.float2str(srv.descuento * 100)), 
                          utils.float2str(srv.get_subtotal()), 
                          srv.albaranSalidaID and srv.albaranSalida.numalbaran or "", 
                          (srv.facturaVentaID and srv.facturaVenta.numfactura) or (srv.prefacturaID and srv.prefactura.numfactura) or "", 
                          srv.id))
            total += srv.get_subtotal()
        return total

    def rellenar_pendiente(self):
        """
        Rellena el cuadro de pendiente de servir.
        OJO: No tiene en cuenta a qué precios se han servido las líneas de 
        pedido, cosa que sí se hace en los albaranes porque hay veces en que 
        se sirve un mismo producto a dos precios diferentes y hay que 
        calcular qué producto ha "caído" en cada línea de venta.
        """
        model = self.wids['tv_pendiente'].get_model()
        model.clear()
        productos, productos_pendientes, servicios_pendientes = \
            self.objeto.get_pendiente_servir()
        if (len(productos_pendientes) == 0 
            and len(self.objeto.lineasDePedido) > 0
            and len(servicios_pendientes) == 0):
            # Cierre automático del pedido si ya está todo servido.
            self.objeto.cerrado = True
            self.wids['cerrado'].set_active(self.objeto.cerrado)
        for producto in productos:
            pendiente = productos[producto]['pedido'] - productos[producto]['servido']
            if pendiente != 0:      # NOTA: Si es negativo TAMBIÉN LO QUIERO 
                                    # VER. Así puedo detectar casos de 
                                    # LDVs en albaranes sin pedido porque se 
                                    # hayan borrado del pedido después de 
                                    # hacer el albarán o algo. 
                model.append((producto.descripcion, pendiente, producto.id))
        self.wids['tv_pendiente'].set_sensitive(not self.objeto.cerrado)
        # Pendiente de facturar:
        model = self.wids['tv_pendiente_fact'].get_model()
        model.clear()
        productos_pendientes, servicios_pendientes = \
            self.objeto.get_pendiente_facturar()
        for producto in productos_pendientes:
            pendiente = (productos_pendientes[producto]['pedido'] 
                         - productos_pendientes[producto]['facturado'])
            if pendiente != 0:      # NOTA: Si es negativo TAMBIÉN LO QUIERO 
                                    # VER. Así puedo detectar casos de 
                                    # LDVs en albaranes sin pedido porque se 
                                    # hayan borrado del pedido después de 
                                    # hacer el albarán o algo. 
                model.append((producto.descripcion, pendiente, producto.id))
        self.wids['tv_pendiente_fact'].set_sensitive(not self.objeto.cerrado)


    def colorear(self):
        def cell_func(column, cell, model, itr, i):
            try:
                ldp = pclases.LineaDePedido.get(model[itr][-1])
            except pclases.SQLObjectNotFound:
                print "LDP ID %d no encontrada. Probablemente borrada "\
                      "justo durante el coloreado." % (model[itr][-1])
                return
            color = None
            # Usaré una especie de caché de stock que se refrescará en 
            # cada rellenar_$(TreeView)
            #cantidad_servida = ldp.cantidadServida
            cantidad_servida = model[itr][-2]
            #cantidad_pedida = ldp.cantidadPedida
            cantidad_pedida = model[itr][-3]
            if cantidad_servida > 0 and cantidad_servida < cantidad_pedida:
                color = "LightYellow"
            elif cantidad_servida == cantidad_pedida:
                color = "green"
            elif cantidad_servida > cantidad_pedida:
                color = "orange"
            elif ldp.cantidad > self.ldps[ldp.producto]:
                if (not hasattr(ldp.producto, "controlExistencias") 
                    or ldp.producto.controlExistencias):
                    color = "red"
            cell.set_property("cell-background", color)
            contenido = model[itr][i]
            if (isinstance(contenido, type(0.1)) 
                and not isinstance(cell, gtk.CellRendererPixbuf)):
                if i in (3, 5): # CWT: 4 decimales en precio y subtotal
                    cell.set_property("text", (utils.float2str(contenido, 4)))
                else:
                    cell.set_property('text', (utils.float2str(contenido, 3)))

        cols = self.wids['tv_ldps'].get_columns()
        for i in xrange(len(cols)):
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell, cell_func, i)

    def rellenar_tabla(self, tabla):
        """
        Borra el contenido del model y lo vuelve a 
        rellenar con las LDV del pedido.
        Devuelve la suma de las LDV.
        """
        self.objeto
        subtotal = 0
        model = self.wids['tv_ldvs'].get_model()
        model.clear()
        for ldv in self.objeto.lineasDeVenta:
            if ldv.albaranSalidaID == None and ldv.facturaVentaID == None and ldv.prefactura == None:
                try:
                    ldv.destroy(ventana = __file__)
                    self.logger.error("%spedidos_de_venta.py::rellenar_tabla -> Eliminada LDV ID %d sin albarán ni factura(s)." % (self.usuario and self.usuario.usuario + ": " or "", ldv.id))
                    continue
                except:
                    txt = "No se pudo eliminar LDV ID %d sin albarán ni factura." % (ldv.id)
                    print txt
                    self.logger.error("%spedidos_de_venta.py::rellenar_tabla -> %s" % (self.usuario and self.usuario.usuario + ": " or "", txt))
            ldvtotal = ldv.precio * (1-ldv.descuento) * ldv.cantidad
            try:
                datos_rollo = ldv.productoVenta.camposEspecificosRollo
                m2rollo = int(datos_rollo.metrosLineales * datos_rollo.ancho)
                try:
                    bultos = int(ldv.cantidad / m2rollo)
                except ZeroDivisionError:
                    bultos = 0
            except AttributeError:  # producto no tiene campos específicos. Es bala.
                bultos = 0
            if hasattr(ldv.producto, "nombre") and len(ldv.producto.descripcion) < len(ldv.producto.nombre):
                descripcion = ldv.producto.nombre
            else:
                descripcion = ldv.producto.descripcion
            model.append((ldv.producto.codigo,
                          descripcion,
                          ldv.cantidad,
                          ldv.precio,
                          "%s %%" % (utils.float2str(ldv.descuento * 100)), 
                          ldvtotal,
                          bultos,
                          ldv.albaranSalida and ldv.albaranSalida.numalbaran or "",
                          ldv.albaranSalida and utils.str_fecha(ldv.albaranSalida.fecha) or "", 
                          (ldv.facturaVenta and ldv.facturaVenta.numfactura) or (ldv.prefactura and ldv.prefactura.numfactura) or "",
                          (ldv.facturaVenta and utils.str_fecha(ldv.facturaVenta.fecha)) or (ldv.prefactura and utils.str_fecha(ldv.prefactura.fecha)) or "", 
                          ldv.id))
            subtotal += ldvtotal
            if hasattr(ldv.producto, "get_stock"):
                self.ldvs[ldv.producto] = ldv.producto.get_stock()
            else:
                self.ldvs[ldv.producto] = ldv.producto.existencias
        #self.colorear()
        return subtotal
        
    def rellenar_tabla_ldp(self, tabla):
        """
        Borra el contenido del model y lo vuelve a 
        rellenar con las LDP del pedido.
        Devuelve la suma de las LDP.
        """
        self.objeto
        subtotal = 0
        model = self.wids['tv_ldps'].get_model()
        model.clear()
        ldps = self.objeto.lineasDePedido[:]
        ldps.sort(lambda l1, l2: int(l1.id - l2.id))
        for ldp in ldps:
            ldptotal = ldp.precio * (1-ldp.descuento) * ldp.cantidad
            try:
                datos_rollo = ldp.productoVenta.camposEspecificosRollo
                m2rollo = int(datos_rollo.metrosLineales * datos_rollo.ancho)
                try:
                    bultos = int(ldp.cantidad / m2rollo)
                except ZeroDivisionError:
                    bultos = 0
            except AttributeError:  # producto no tiene campos específicos. 
                                    # Es bala.
                bultos = 0
            if ldp.productoVentaID != None:
                if len(ldp.productoVenta.descripcion) >= len(
                                                    ldp.productoVenta.nombre):
                    descripcion = ldp.productoVenta.descripcion
                else:
                    descripcion = ldp.productoVenta.nombre
                codigo = ldp.productoVenta.codigo
                self.ldps[ldp.productoVenta] = ldp.productoVenta.get_stock()
            elif ldp.productoCompraID != None:
                descripcion = ldp.productoCompra.descripcion
                codigo = ldp.productoCompra.codigo
                self.ldps[ldp.productoCompra] = ldp.productoCompra.existencias
            model.append((codigo,
                          descripcion,
                          ldp.cantidad,
                          ldp.precio,
                          "%s %%" % (utils.float2str(ldp.descuento * 100)), 
                          ldptotal,
                          bultos,
                          utils.str_fecha(ldp.fechaEntrega),
                          ldp.textoEntrega,
                          ldp.cantidadPedida, 
                          ldp.cantidadServida, 
                          ldp.id))
            subtotal += ldptotal
        #self.colorear()
        return subtotal

    # --------------- Manejadores de eventos ----------------------------
    
    def editar_cantidad_srv(self, cell, path, texto):
        """
        Cambia la cantidad del servicio.
        """
        try:
            cantidad = utils._float(texto)
        except:
            return
        model = self.wids['tv_servicios'].get_model()
        srv = pclases.Servicio.get(model[path][-1])
        if srv.cantidad != cantidad:
            if srv.presupuesto != None:
                if utils.dialogo(titulo = "¿CAMBIAR CANTIDAD?", texto = "Esta línea proviene de una oferta de precio.\nCambiando la cantidad en el pedido se alteran las condiciones del presupuesto.\n\n¿Está seguro de querer cambiarlo?", padre = self.wids['ventana']):
                    srvoriginal = srv
                    srv = srvoriginal.clone(presupuesto = None)
                    srvoriginal.pedidoVenta = None
                else:
                    return
            srv.cantidad = cantidad
            self.actualizar_ventana()
    
    def editar_concepto_srv(self, cell, path, texto):
        """
        Cambia el concepto del servicio.
        """
        model = self.wids['tv_servicios'].get_model()
        srv = pclases.Servicio.get(model[path][-1])
        srv.concepto = texto
        self.actualizar_ventana()
    
    def editar_precio_srv(self, cell, path, texto):
        """
        Cambia el precio del servicio.
        """
        try:
            precio = utils.parse_formula(texto)
        except:
            return
        model = self.wids['tv_servicios'].get_model()
        try:
            srv = pclases.Servicio.get(model[path][-1])
        except pclases.SQLObjectNotFound:
            self.actualizar_ventana()
        else:
            if precio != srv.precio:
                if srv.presupuesto != None:
                    if utils.dialogo(titulo = "¿CAMBIAR PRECIO?", 
                            texto = "Esta línea proviene de una oferta de "
                                    "precio.\nCambiando el precio en el "
                                    "pedido se alteran las condiciones del "
                                    "presupuesto.\n\n¿Está seguro de querer "
                                    "cambiarlo?", 
                            padre = self.wids['ventana']):
                        srvoriginal = srv
                        srv = srvoriginal.clone(presupuesto = None)
                        srvoriginal.pedidoVenta = None
                    else:
                        return
                try:
                    srv.precio = precio
                except (ValueError, TypeError, 
                        pclases.include.validators.InvalidField):
                    return
                self.actualizar_ventana()
    
    def editar_descuento_srv(self, cell, path, texto):
        """
        Cambia el descuento del servicio.
        """
        try:
            descuento = utils.parse_porcentaje(texto) / 100.0
        except:
            return
        model = self.wids['tv_servicios'].get_model()
        srv = pclases.Servicio.get(model[path][-1])
        if srv.descuento != descuento:
            if srv.presupuesto != None:
                if utils.dialogo(titulo = "¿CAMBIAR DESCUENTO?", texto = "Esta línea proviene de una oferta de precio.\nCambiando el descuento en el pedido se alteran las condiciones del presupuesto.\n\n¿Está seguro de querer cambiarlo?", padre = self.wids['ventana']):
                    srvoriginal = srv
                    srv = srvoriginal.clone(presupuesto = None)
                    srvoriginal.pedidoVenta = None
                else:
                    return
            srv.descuento = descuento
            self.actualizar_ventana()
    
    def cambiar_precio(self, cell, path, texto):
        """
        Cambia el precio de la LDV conforme al texto recibido.
        """
        try:
            precio = utils._float(texto)
        except:
            return
        model = self.wids['tv_ldvs'].get_model()
        ldv = pclases.LineaDeVenta.get(model[path][-1])
        ldv.precio = precio
        self.actualizar_ventana()
        
    def cambiar_cantidad(self, cell, path, texto):
        """
        Cambia la cantidad de la LDV conforme al texto recibido.
        """
        try:
            cantidad = utils._float(texto)
        except:
            return
        model = self.wids['tv_ldvs'].get_model()
        ldv = pclases.LineaDeVenta.get(model[path][-1])
        ldv.cantidad = cantidad
        self.actualizar_ventana()

    def cambiar_descuento(self, cell, path, texto):
        """
        Cambia el descuento de la LDV conforme al texto recibido.
        """
        try:
            descuento = utils.parse_porcentaje(texto, fraccion = True)
        except:
            return
        model = self.wids['tv_ldvs'].get_model()
        ldv = pclases.LineaDeVenta.get(model[path][-1])
        ldv.descuento = descuento
        self.actualizar_ventana()

    def cambiar_precio_ldp(self, cell, path, texto):
        """
        Cambia el precio de la LDP conforme al texto recibido.
        """
        try:
            precio = utils._float(texto)
        except:
            return
        model = self.wids['tv_ldps'].get_model()
        try:
            ldp = pclases.LineaDePedido.get(model[path][-1])
        except IndexError:
            # ¿Cómo demonios ha conseguido que el path llege desfasado o nulo?
            ## Errores en segundo plano. La stderr contiene:
            ## Traceback (most recent call last):
            ##  File "Q:\formularios\pedidos_de_venta.py", line 956, in cambiar_precio_ldp
            ##    ldp = pclases.LineaDePedido.get(model[path][-1])
            ## IndexError: could not find tree path
            return
        if ldp.precio != precio:
            if ldp.presupuesto != None:
                if utils.dialogo(titulo = "¿CAMBIAR PRECIO?", texto = "Esta línea proviene de una oferta de precio.\nCambiando el precio en el pedido se alteran las condiciones del presupuesto.\n\n¿Está seguro de querer cambiarlo?", padre = self.wids['ventana']):
                    ldporiginal = ldp
                    ldp = ldporiginal.clone(presupuesto = None)
                    ldporiginal.pedidoVenta = None
                else:
                    return
            ldp.precio = precio
            if ldp.get_lineas_de_venta() != [] \
               and utils.dialogo(
                            titulo = "¿CAMBIAR PRECIO PRODUCTOS SERVIDOS?", 
                            texto = """
                ¿Desea cambiar el precio de todos los artículos servidos                
                de este producto?                                                       
                                                                                        
                Si lo hace, se cambiará también en la factura en caso de                
                que se haya facturado el albarán o albaranes                            
                correspondientes.                                                       
                """, 
                            padre = self.wids['ventana']):
                for ldv in ldp.get_lineas_de_venta():
                    ldv.precio = ldp.precio
            self.actualizar_ventana()
        
    def cambiar_cantidad_ldp(self, cell, path, texto):
        """
        Cambia la cantidad de la LDP conforme al texto recibido.
        """
        try:
            cantidad = utils._float(texto)
        except:
            return
        model = self.wids['tv_ldps'].get_model()
        ldp = pclases.LineaDePedido.get(model[path][-1])
        if ldp.cantidad != cantidad:
            if ldp.presupuesto != None:
                if utils.dialogo(titulo = "¿CAMBIAR CANTIDAD?", 
                        texto = "Esta línea proviene de una oferta de precio."
                                "\nCambiando la cantidad ofertada en el "
                                "pedido se alteran las condiciones del "
                                "presupuesto.\n\n¿Está seguro de querer "
                                "cambiarlo?", 
                        padre = self.wids['ventana']):
                    ldporiginal = ldp
                    ldp = ldporiginal.clone(presupuesto = None)
                    ldporiginal.pedidoVenta = None
                else:
                    return
            ldp.cantidad = cantidad
            self.actualizar_ventana()

    def cambiar_descuento_ldp(self, cell, path, texto):
        """
        Cambia el descuento de la LDP conforme al texto recibido.
        """
        try:
            descuento = utils.parse_porcentaje(texto, fraccion = True)
        except:
            return
        model = self.wids['tv_ldps'].get_model()
        ldp = pclases.LineaDePedido.get(model[path][-1])
        if descuento != ldp.descuento:
            if ldp.presupuesto != None:
                if utils.dialogo(titulo = "¿CAMBIAR DESCUENTO?", 
                        texto = "Esta línea proviene de una oferta de "
                                "precio.\nCambiando el descuento se alteran "
                                "las condiciones del presupuesto.\n\n"
                                "¿Está seguro de querer cambiar el "
                                "descuento?", 
                        padre = self.wids['ventana']):
                    ldporiginal = ldp
                    ldp = ldporiginal.clone(presupuesto = None)
                    ldporiginal.pedidoVenta = None
                else:
                    return
            ldp.descuento = descuento
            self.actualizar_ventana()
        
    def cambiar_texto_entrega(self, cell, path, texto):
        """
        Cambia el textoEntrega de la LDP conforme al texto recibido.
        """
        model = self.wids['tv_ldps'].get_model()
        ldp = pclases.LineaDePedido.get(model[path][-1])
        ldp.textoEntrega = texto
        self.actualizar_ventana()
        
    def cambiar_fecha_entrega(self, cell, path, texto):
        """
        Cambia el descuento de la LDP conforme al texto recibido.
        """
        try:
            fecha = utils.parse_fecha(texto)
        except:
            if texto == "":
                fecha = None
            else:
                utils.dialogo_info(titulo = "ERROR FORMATO", 
                                   texto = "El texto %s no se corresponde con"
                                           " una fecha válida." % (texto), 
                                   padre = self.wids['ventana'])
                return
        model = self.wids['tv_ldps'].get_model()
        ldp = pclases.LineaDePedido.get(model[path][-1])
        ldp.fechaEntrega = fecha
        self.actualizar_ventana()

    def crear_nuevo_pedido(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan self.objeto aquí.
        """
        ultimo_pedido_mas_uno = str(
            pclases.PedidoVenta.get_siguiente_numero_numpedido())
        numpedido = utils.dialogo_entrada(
            texto = 'Introduzca un número de pedido.', 
            titulo = 'NÚMERO DE PEDIDO', 
            padre = self.wids['ventana'], 
            valor_por_defecto = ultimo_pedido_mas_uno)
        if numpedido == None:
            return
        existe = pclases.PedidoVenta.select(
            pclases.PedidoVenta.q.numpedido == numpedido)
        if existe.count() > 0:
            utils.dialogo_info(titulo = "PEDIDO YA EXISTE", 
                texto = "El número de pedido ya existe. Use otro número.", 
                padre = self.wids['ventana'])
            return
        try:
            tarifa_defecto = pclases.Tarifa.select(
                pclases.Tarifa.q.nombre == "Tarifa 1")[0]
        except IndexError:
            tarifa_defecto = None
        if self.objeto != None: self.objeto.notificador.desactivar()
        self._objetoreciencreado = self.objeto = pclases.PedidoVenta(
            cliente = None, 
            fecha = time.localtime(), 
            numpedido = numpedido,
            iva = 0.21,
            descuento = 0,
            transporteACargo = False,
            bloqueado = True,
            cerrado = False, 
            tarifa = tarifa_defecto)
        pclases.Auditoria.nuevo(self.objeto, self.usuario, __file__)
        self.objeto.notificador.activar(self.aviso_actualizacion)
        # XXX: Añado a objetos recientes.
        objsr = pclases.ListaObjetosRecientes.buscar("pedidos_de_venta.py", 
                                                self.usuario, 
                                                crear = True)
        objsr.push(self.objeto.id)
        # XXX: End Of Añado a objetos recientes.
        self.desconectar_dircorrespondencia()
        self.actualizar_ventana()
        self.conectar_dircorrespondencia()
        utils.dialogo_info('PEDIDO CREADO', 
                           'Se ha creado el pedido %s.\nComplete a '
                           'continuación el resto de información acerca del '
                           'mismo.' % (self.objeto.numpedido), 
                           padre = self.wids['ventana'])

    def buscar_pedido(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        self.objeto
        txtopabiertos = "Buscar solamente pedidos abiertos"
        opcion_abiertos = {txtopabiertos: True}
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR PEDIDO", 
                texto = "Introduzca número de pedido o nombre del cliente:",
                padre = self.wids['ventana'], 
                opciones = opcion_abiertos) 
        PedV = pclases.PedidoVenta
        if a_buscar != None:
            buscar_solo_abiertos = opcion_abiertos[txtopabiertos]
            resultados = buscar_pedidos(a_buscar, buscar_solo_abiertos)
            if resultados.count() > 1:
                    ## Refinar los resultados
                    idpedido = self.refinar_resultados_busqueda(resultados)
                    if idpedido == None:
                        return
                    resultados = [PedV.get(idpedido)]
                    # Se supone que la comprensión de listas es más rápida que 
                    # hacer un nuevo get a SQLObject. Me quedo con una lista 
                    # de resultados de un único objeto ocupando la primera 
                    # posición. (Más abajo será cuando se cambie realmente el 
                    # objeto actual por este resultado.)
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
            if self.objeto != None:
                self.objeto.notificador.desactivar()
            # Pongo el objeto como actual
            self.objeto = resultados[0]
            # XXX: Añado a objetos recientes.
            objsr = pclases.ListaObjetosRecientes.buscar("pedidos_de_venta.py",
                                                    self.usuario, 
                                                    crear = True)
            objsr.push(self.objeto.id)
            # XXX: End Of Añado a objetos recientes.
            # Y activo la función de notificación:
            self.objeto.notificador.activar(self.aviso_actualizacion)
        self.desconectar_dircorrespondencia()
        self.actualizar_ventana()
        self.conectar_dircorrespondencia()

    def guardar(self, widget):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        self.objeto
        # Campos del objeto que hay que guardar:
        numpedido = self.wids['e_numpedido'].get_text()
        if numpedido == '' or numpedido == None:
            utils.dialogo_info(titulo = 'PEDIDO SIN NÚMERO', texto = 'Está totalmente desaconsejado almacenar pedidos sin número.\nAsigne un número al pedido si quiere relacionarlo más tarde con albaranes y facturas.', padre = self.wids['ventana'])
        fecha = self.wids['e_fecha'].get_text()
        idcliente = utils.combo_get_value(self.wids['cbe_cliente'])
        try:
            idtarifa = utils.combo_get_value(self.wids['cbe_tarifa'])
        except:
            idtarifa = -1   # Probablemente no hay tarifas en la BD.
        descuentostr = self.wids['e_descuento'].get_text()
        try:
            descuento = utils.parse_porcentaje(descuentostr, fraccion = True)
        except ValueError:
            descuento = 0
        ivastr = self.wids['e_iva'].get_text()
        try:
            iva = utils.parse_porcentaje(ivastr, fraccion = True)
        except ValueError:
            iva = 0.21
        if idcliente != None:
            try:
                idcliente = pclases.Cliente.get(idcliente)
            except pclases.SQLObjectNotFound:   # Cliente borrado después de empezar el pedido.
                icliente = None
        # Desactivo el notificador momentáneamente
        self.objeto.notificador.desactivar()
        # Actualizo los datos del objeto
        self.objeto.numpedido = numpedido
        self.objeto.cliente = idcliente
        self.objeto.bloqueado = self.wids['bloqueado'].get_active()
        self.objeto.cerrado = self.wids['cerrado'].get_active()
        tarifa_anterior = self.objeto.tarifa
        if idtarifa == -1:
            self.objeto.tarifa = None
        else:
            self.objeto.tarifaID = idtarifa
        if self.objeto.tarifa != None and \
           not self.objeto.tarifa.esta_vigente(self.objeto.fecha) \
           and not utils.dialogo(titulo = "TARIFA SIN VIGENCIA", 
                                 texto = "La tarifa seleccionada no está vigente en la fecha del pedido.\n¿Desea asignarla de todos modos?", 
                                 padre = self.wids['ventana']):
            self.objeto.tarifa = tarifa_anterior
        try:
            #self.objeto.fecha = mx.DateTime.DateTimeFrom(
            #    day = int(fecha.split('/')[0]), 
            #    month = int(fecha.split('/')[1]), 
            #    year = int(fecha.split('/')[2])) 
            self.objeto.fecha = utils.parse_fecha(fecha)
        except:
            self.objeto.fecha = time.localtime()
        self.objeto.descuento = descuento
        self.objeto.iva = iva
        self.objeto.direccionCorrespondencia = self.wids['e_direccionCorrespondencia'].get_text()
        self.objeto.nombreCorrespondencia = self.wids['e_nombreCorrespondencia'].get_text()
        self.objeto.cpCorrespondencia = self.wids['e_cpCorrespondencia'].get_text()
        self.objeto.ciudadCorrespondencia = self.wids['e_ciudadCorrespondencia'].get_text()
        self.objeto.provinciaCorrespondencia = self.wids['e_provinciaCorrespondencia'].get_text()
        self.objeto.paisCorrespondencia = self.wids['e_paisCorrespondencia'].get_text()
        self.objeto.textoObra = self.wids['e_obra'].get_text()
        self.objeto.obraID = utils.combo_get_value(self.wids['cb_obra'])
        if not self.objeto.obra:
            # CWT: Ningún pedido sin obra.
            if self.objeto.cliente:
                self.objeto.obra = self.objeto.cliente.get_obra_generica()
            else:
                utils.dialogo_info(titulo = "SELECCIONE CLIENTE", 
                    texto = "Debe seleccionar un cliente para el pedido.", 
                    padre = self.wids['ventana'])
                try:
                    dde = pclases.DatosDeLaEmpresa.select()[0]
                    self.objeto.cliente = dde.get_propia_empresa_como_cliente()
                    self.objeto.syncUpdate()
                    self.actualizar_ventana()
                except IndexError:
                    pass    # No hay Datos de la empresa.
        # Fuerzo la actualización de la BD y no espero a que SQLObject lo 
        # haga por mí:
        idcomercial = utils.combo_get_value(self.wids['cbe_comercial'])
        if idcomercial == -1:
            idcomercial = None
        self.objeto.comercialID = idcomercial
        idfdp = utils.combo_get_value(self.wids['cbe_fdp'])
        while not idfdp:
            fdps = [(fdp.id, fdp.toString()) 
                    for fdp in pclases.FormaDePago.select(
                        pclases.FormaDePago.q.activa == True, 
                        orderBy = ("documento_de_pago_id", "plazo"))]
            #fdps.sort(key = lambda p: p[1])
            # CWT: No hay forma de pago por defecto.
            #fdp = pclases.FormaDePago.porDefecto()
            idfdp = utils.dialogo_combo(titulo = "FORMA DE PAGO INCORRECTA", 
                    texto = "No ha seleccionado una forma de pago.\n"
                    "No podrá continuar hasta seleccionar una del\n"
                    "desplegable a continuación.", 
                    padre = self.wids['ventana'], 
                    ops = fdps)  
                    # valor_por_defecto = fdp.id)
        self.objeto.formaDePagoID = idfdp
        self.objeto.syncUpdate()
        self.actualizar_ventana()
        self.wids['b_guardar'].set_sensitive(False)
        # Vuelvo a activar el notificador
        self.objeto.notificador.activar(self.aviso_actualizacion)

    def buscar_fecha(self, boton):
        fecha = utils.mostrar_calendario(
            fecha_defecto = self.objeto and self.objeto.fecha or None, 
            padre = self.wids['ventana'])
        if pclases.DEBUG:
            print fecha
        self.wids['e_fecha'].set_text(utils.str_fecha(fecha))

    def add_ldv(self, boton):
        """
        Añade una nueva LDV creada a partir de la 
        información recogida mediante diálogos
        modales.
        """
        self.guardar(None)  # Por si no están guardadas la fecha y proveedor
        productos = utils.buscar_producto_general(self.wids['ventana'], 
                                                  mostrar_precios = True)
        for producto in productos:
            try:
                tarifa = self.objeto.tarifa
                precio = tarifa.obtener_precio(producto)
            except:
                precio = producto.preciopordefecto
            if precio == 0:
                precio = preguntar_precio(producto, self.wids['ventana'])
            cantidad = self.seleccionar_cantidad(producto)
            if cantidad == None:
                break
            ldv = pclases.LineaDeVenta(pedidoVenta = self.objeto, 
                                       albaranSalida = None, 
                                       productoVenta = producto, 
                                       facturaVenta = None,
                                       cantidad = cantidad, 
                                       precio = precio, 
                                       descuento = 0)
            pclases.Auditoria.nuevo(ldv, self.usuario, __file__)
        self.actualizar_ventana()

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
            if (producto.es_bala() or producto.es_bigbag() 
                or producto.es_bala_cable() or producto.es_rolloC() 
                or producto.es_bolsa()):
                txt = """Introduzca la cantidad en kilos:"""
            elif producto.es_rollo():
                txt = """Introduzca la cantidad en metros cuadrados:"""
            elif producto.es_especial():
                if producto.camposEspecificosEspecial.unidad:
                    txt = """Introduzca la cantidad en %s:""" % (
                        producto.camposEspecificosEspecial.unidad)
                else:
                    txt = """Introduzca la cantidad:"""
            else:
                txterror = """pedidos_de_venta::seleccionar_cantidad -> ERROR: El producto de venta ID %d no es bala ni rollo. Verificar.""" % (producto.id)
                print txterror
                self.logger.error(txterror)
                txt = """Introduzca la cantidad:"""
        elif isinstance(producto, pclases.ProductoCompra):
            txt = "Introduzca la cantidad en %s." % (producto.unidad)
        else:
            txterror = "pedidos_de_venta::seleccionar_cantidad -> "\
                       "ERROR: Producto %s no es producto de compra "\
                       "ni de venta." % (producto)
            self.logger.error(txterror)
        cantidad = utils.dialogo_entrada(titulo = 'CANTIDAD', 
                                         texto = txt, 
                                         padre = self.wids['ventana'], 
                                         valor_por_defecto = '1')
        if cantidad is None:
            return
        try:
            cantidad = utils._float(cantidad)
            return cantidad
        except:
            utils.dialogo_info(titulo = 'ERROR', 
                            texto = 'La cantidad introducida no es correcta.', 
                            padre = self.wids['ventana'])
            return None

    def cambiar_tarifa_ldv(self, boton):
        seleccion = self.wids['tv_ldps'].get_selection()
        model, iter = seleccion.get_selected()
        if iter == None: 
            utils.dialogo_info('SELECCIONE UN PRODUCTO', 
                               'Debe seleccionar el producto al que cambiar '
                               'el precio.', 
                               padre = self.wids['ventana'])
            return
        idldp = model[iter][-1]
        ldp = pclases.LineaDePedido.get(idldp)
        idtarifa = utils.combo_get_value(self.wids['cbe_tarifa'])
        if idtarifa != -1 and idtarifa != None:
            tarifa = pclases.Tarifa.get(idtarifa)
            ldp.precio = tarifa.obtener_precio(ldp.producto)
            self.actualizar_ventana()

    def drop_ldv(self, boton):
        """
        Elimina una LDV del pedido e intenta 
        eliminarla también de la BD. Si la LDV
        tiene relación con otras tablas sólo se
        desvinculará del pedido actual y quedará
        como venta pendiente para poder volver a
        ser seleccionada desde el botón 
        correspondiente.
        """
        seleccion = self.wids['tv_ldvs'].get_selection()
        model, iter = seleccion.get_selected()
        if iter == None: 
            utils.dialogo_info('SELECCIONE UN PRODUCTO', 
                               'Debe seleccionar el producto a eliminar del '
                               'pedido.', 
                               padre = self.wids['ventana'])
            return
        txt = """
        ¿Está seguro de que desea eliminar la línea seleccionada del pedido?
        """
        if not utils.dialogo(titulo = '¿BORRAR?', 
                             texto = txt, 
                             padre = self.wids['ventana']):
            return
        idldv = model[iter][-1]
        ldv = pclases.LineaDeVenta.get(idldv)
        if ldv.albaranSalida != None:
            txt =  """
            La línea seleccionada corresponde a un artículo que          
            ya ha salido del almacén en el albarán %s. Elimine
            el producto primero del albarán y a continuación
            vuelva a intentarlo en el self.objeto.
            """ % (ldv.albaranSalida.numalbaran)
            utils.dialogo_info(titulo = 'NO SE PUDO ELIMINAR',
                               texto = txt, 
                               padre = self.wids['ventana'])
            return
        # DONE: Hacer lo mismo con las facturas. Cuando estén.
        ldv.pedidoVenta = None
        ldv.eliminar()  # Ya se ha chequeado que no tenga facturas ni albaranes. No debería fallar.
        self.guardar(None)  # Por si no están guardadas la fecha y proveedor
        self.actualizar_ventana()

    def borrar(self, boton):
        """
        Elimina el self.objeto de la BD e intenta eliminar
        también las LDV relacionadas. En caso de que
        las LDV estén implicadas en otras operaciones
        sólo se eliminará el self.objeto y se pondrá el 
        idpedido de las LDV a None.
        """
        if not utils.dialogo('Borrar un pedido cuyas ventas estén relacionadas con albaranes de salida, facturas, etc. puede ser contraproducente.\n¿Está seguro de que desea eliminar el pedido?', 'BORRAR PEDIDO', padre = self.wids['ventana']): 
            return
        # Ya está avisado el usuario. Hago un destroy en cascada y a correr.
        # Desactivo notificador:
        self.objeto.notificador.desactivar()
        # Y por último destruyo el self.objeto:
        self.objeto.destroy_en_cascada(ventana = __file__)
        self.ir_a_primero()

    def aplicar_tarifa(self, cb):
        self.guardar(None)
        idtarifa = utils.combo_get_value(self.wids['cbe_tarifa'])
        if idtarifa == -1 or idtarifa == None:
            for ldp in self.objeto.lineasDePedido:
                if ldp.producto.precioDefecto:
                    ldp.precio = ldp.producto.precioDefecto
        else:
            tarifa = pclases.Tarifa.get(idtarifa)
            for ldp in self.objeto.lineasDePedido:
                if tarifa.obtener_precio(ldp.producto):
                    ldp.precio = tarifa.obtener_precio(ldp.producto)
        self.rellenar_widgets()

    
    def ver_vencimientos(self,boton):
        """
        Muestra un dialogo con los vencimientos
        asociados a las lineas del pedido
        """
        pedido = self.objeto
        vencimientos = []
        for l in pedido.lineasDeVenta:
            fra = l.get_factura_o_prefactura()
            if fra != None:
                for v in fra.vencimientosCobro:
                    vencimientos.append(v)
        if vencimientos != []:
            mensaje = 'Vencimientos asociados con este pedido de venta:\n\n'
        else:
            mensaje = 'No hay vencimientos asociadas a este pedido'
        for v in vencimientos:
            mensaje += 'Fecha: ' + utils.str_fecha(v.fecha) + '  -  Importe: ' + ("%.2f" % (v.importe)) + ' (%s)\n' % (v.get_factura_o_prefactura() and v.get_factura_o_prefactura().numfactura or '¡SIN FACTURA!')
        utils.dialogo_info(titulo = 'VENCIMIENTOS', texto = mensaje, padre = self.wids['ventana'])


    def ver_cobros(self,boton):
        """
        Muestra un dialogo con cobros asociados 
        a las lineas del pedido
        """
        pedido = self.objeto
        cobros = []
        for l in pedido.lineasDeVenta:
            fra = l.get_factura_o_prefactura()
            if fra != None:
                for c in fra.cobros:
                    cobros.append(c)
        if cobros != []:
            mensaje = 'Cobros asociados con este pedido de venta:\n\n'
        else:
            mensaje = 'No hay cobros asociadas a este pedido'
        for c in cobros:
            mensaje += 'Fecha: ' + utils.str_fecha(c.fecha) + '  -  Importe: ' + ("%.2f" % (c.importe)) + '\n'
        utils.dialogo_info(titulo = 'COBROS', texto = mensaje, padre = self.wids['ventana'])

        
    def ver_facturas(self,boton):
        """
        Muestra un dialogo con las facturas
        asociadas a las líneas del pedido
        """
        pedido = self.objeto
        facturas = []
        for l in pedido.lineasDeVenta:
            fra = l.get_factura_o_prefactura()
            if fra != None:
                facturas.append(fra)
        if facturas != []:
            mensaje = 'Facturas asociadas con este pedido de venta:\n\n'
        else:
            mensaje = 'No hay facturas asociadas a este pedido'
        for f in facturas:
            mensaje += 'Factura: ' + f.numfactura + '  -  Fecha: ' + utils.str_fecha(f.fecha) + '\n'
        utils.dialogo_info(titulo = 'FACTURAS', texto = mensaje, padre = self.wids['ventana'])

    def ver_albaranes(self,boton):
        """
        Muestra un dialogo con las facturas
        asociadas a las líneas del pedido
        """
        pedido = self.objeto
        albaranes = []
        for l in pedido.lineasDeVenta:
            if l.albaranSalidaID != None and l.albaranSalida not in albaranes:
                albaranes.append(l.albaranSalida)
        def ordenar_por_numalbaran(a1, a2):
            if a1.numalbaran < a2.numalbaran:
                return -1
            if a1.numalbaran > a2.numalbaran:
                return 1
            return 0
        albaranes.sort(ordenar_por_numalbaran)
        if albaranes != []:
            mensaje = 'Albaranes asociados con este pedido de venta:\n\n'
        else:
            mensaje = 'No hay albaranes asociados a este pedido'
        for a in albaranes:
            mensaje += 'Albarán: ' + a.numalbaran + '  -  Fecha: ' + utils.str_fecha(a.fecha) + '\n'
        utils.dialogo_info(titulo = 'ALBARANES', texto = mensaje, padre = self.wids['ventana'])
                 
    def ver_abonos(self,boton):
        """
        Muestra un dialogo con los abonos
        asociados a las lineas del pedido
        """
        pedido = self.objeto
        abonos = []
        for l in pedido.lineasDeVenta:
            for a in l.lineasDeAbono:
                if a.abonoID != None:
                    abonos.append(a.abono)
        if abonos != []:
            mensaje = 'Abonos asociados a este pedido de venta:\n\n'
        else:
            mensaje = 'No hay abonos asociados a este pedido'
        for a in abonos:
            mensaje +=  'Abono: ' + a.numabono + '  -  Fecha:' + utils.str_fecha(a.fecha) + '\n'
        utils.dialogo_info(titulo = 'ABONOS', texto = mensaje, padre = self.wids['ventana'])
    
    def cambiar_cargo_transporte(self, tb):
        self.objeto.notificador.desactivar()
        self.objeto.transporteACargo = tb.get_active()
        self.objeto.syncUpdate
        tb.set_active(self.objeto.transporteACargo)
        self.objeto.make_swap()
        self.objeto.notificador.activar(self.aviso_actualizacion)

    def add_ldp(self, boton):
        """
        Añade una nueva LDP creada a partir de la 
        información recogida mediante diálogos
        modales.
        """
        self.guardar(None)  # Por si no están guardadas la fecha y proveedor
        #productos = self.pedir_producto()
        #if len(productos) == 0:
        #    utils.dialogo_info(titulo = 'NO ENCONTRADO', texto = 'No se encontró ningún producto.', padre = self.wids['ventana'])
        #    return
        #elif len(productos) > 1:
        #    productos = self.refinar_busqueda(productos)
        #    if productos == None:
        #        return  # Pulsó cancelar.
        ## Aquí ya hay un único producto en productos.
        #idproducto = productos[0] 
        #producto = pclases.ProductoVenta.get(idproducto)
        #try:
        #    tarifa = self.objeto.tarifa
        #    precio = tarifa.obtener_precio(producto)
        #except:
        #    precio = producto.preciopordefecto
        #if precio == 0:
        #    precio = preguntar_precio(producto)
        #cantidad = self.seleccionar_cantidad(producto)
        #if cantidad == None:
        #    return
        #ldp = pclases.LineaDePedido(pedidoVenta = self.objeto, 
        #                            productoVenta = producto, 
        #                            cantidad = cantidad, 
        #                            precio = precio, 
        #                            descuento = 0, 
        #                            fechaEntrega = None, 
        #                            textoEntrega = "")
        #self.actualizar_ventana()
        productos = utils.buscar_producto_general(self.wids['ventana'], 
                                                  mostrar_precios = True)
        for producto in productos:
            try:
                tarifa = self.objeto.tarifa
                precio = tarifa.obtener_precio(producto)
            except:
                precio = producto.preciopordefecto
            if precio == 0:
                precio = preguntar_precio(producto, self.wids['ventana'])
            cantidad = self.seleccionar_cantidad(producto)
            if cantidad == None:
                break
            if isinstance(producto, pclases.ProductoCompra):
                ldp = pclases.LineaDePedido(pedidoVenta = self.objeto, 
                                            productoVenta = None, 
                                            productoCompra = producto, 
                                            cantidad = cantidad, 
                                            precio = precio, 
                                            descuento = 0, 
                                            fechaEntrega = None, 
                                            textoEntrega = "")
                pclases.Auditoria.nuevo(ldp, self.usuario, __file__)
            elif isinstance(producto, pclases.ProductoVenta):
                ldp = pclases.LineaDePedido(pedidoVenta = self.objeto, 
                                            productoVenta = producto, 
                                            cantidad = cantidad, 
                                            precio = precio, 
                                            descuento = 0, 
                                            fechaEntrega = None, 
                                            textoEntrega = "")
                pclases.Auditoria.nuevo(ldp, self.usuario, __file__)
        self.actualizar_ventana()

    def drop_ldp(self, boton):
        """
        Elimina una LDV del pedido e intenta 
        eliminarla también de la BD. Si la LDV
        tiene relación con otras tablas sólo se
        desvinculará del pedido actual y quedará
        como venta pendiente para poder volver a
        ser seleccionada desde el botón 
        correspondiente.
        """
        seleccion = self.wids['tv_ldps'].get_selection()
        model, iter = seleccion.get_selected()
        if iter == None: 
            utils.dialogo_info('SELECCIONE UN PRODUCTO', 
                               'Debe seleccionar el producto a eliminar del '
                               'pedido.', 
                               padre = self.wids['ventana'])
            return
        txt = """
        ¿Está seguro de que desea eliminar la línea seleccionada del pedido?
        """
        if not utils.dialogo(titulo = '¿BORRAR?', 
                             texto = txt):
            return
        idldp = model[iter][-1]
        ldp = pclases.LineaDePedido.get(idldp)
        if ldp.albaranesSalida != []:
            txt =  """
            La línea seleccionada corresponde a un artículo que         
            ya ha salido del almacén en el albarán %s. ¿Está 
            seguro de querer eliminar la línea de pedido?               
            NOTA: Si elimina la línea de pedido no se eliminará del     
            albarán a no ser que lo haga manualmente desde el propio    
            albarán.
            """ % (", ".join([a and a.numalbaran or "-" 
                              for a in ldp.albaranesSalida]))
            if not utils.dialogo(titulo = 'LÍNEA EN ALBARÁN',
                                 texto = txt,
                                 padre = self.wids['ventana']):
                return
        ldp.pedidoVenta = None
        if ldp.presupuesto == None:
            try:
                ldp.destroy(ventana = __file__)
            except:
                self.logger.error("%spedidos_de_venta.py::drop_ldp -> No se pudo eliminar la LDP ID %d." % (self.usuario and self.usuario.usuario + ": " or "", ldp.id))
        self.guardar(None)  # Por si no están guardadas la fecha y proveedor
        self.actualizar_ventana()

    def satisface_riesgo(self):
        """
        Comprueba si el cliente tiene control de riesgo y en ese caso que el 
        crédito disponible permita facturar el pedido actual.
        Si el usuario es administrador, se le deja a su elección. En otro 
        caso, se le avisa y se impide que continúe devolviendo FALSE.
        """
        importe_pedido = self.objeto.calcular_importe_total(iva = True)
        credito = self.objeto.cliente.calcular_credito_disponible()
        if importe_pedido > credito:
            texto = "El crédito actual del cliente es de %s.\n"\
                     "El importe del pedido es %s.\n" % (
                        utils.float2str(credito), 
                        utils.float2str(importe_pedido))
            if self.usuario and self.usuario.nivel == 0:
                res = utils.dialogo(titulo = "¿FACTURAR SIN CRÉDITO?", 
                    texto = texto + "\n¿Continuar?", 
                    padre = self.wids['ventana'])
            else:
                utils.dialogo_info(titulo = "CRÉDITO INSUFICIENTE", 
                    texto = texto + "\nSe denegó la operación.", 
                    padre = self.wids['ventana'])
                res = False
        else:
            res = True
        return res

    def facturar(self, boton):
        """
        Crea un albarán con las líneas de venta idénticas a las del pedido, 
        y seguidamente una factura con esas mismas líneas de venta.
        Si la LDV contiene productos de venta (que necesitan código de traza-
        bilidad para completar el albarán) deja el albarán y la factura 
        como no bloqueadas.
        Abre una ventana para el nuevo albarán y otra para la nueva factura.
        """
        pedido = self.objeto
        pedido.sync()
        if not self.satisface_riesgo():
            return
        if pedido.cerrado and self.usuario and self.usuario.nivel > 1:
            utils.dialogo_info(titulo = "PERMISOS INUFICIENTES", 
                texto = "El pedido está cerrado y no tiene nivel de permisos"
                        " suficiente para hacer una factura directa.", 
                padre = self.wids['ventana'])
            return
        if not pedido.cliente.contador:
            utils.dialogo_info(titulo = "CLIENTE SIN CONTADOR", 
                texto = "El cliente del pedido no tiene contador asignado.\n"
                        "Debe asignarle uno desde la ventana correspondiente.",
                padre = self.wids['ventana'])
            return
        # 0.- Compruebo que tengo datos mínimos suficientes: cliente y líneas 
        # que facturar.
        productos, servicios = self.objeto.get_pendiente_facturar()
        len_pendiente_facturar = len(servicios) + len(productos)
        if (not pedido.cliente 
            or len_pendiente_facturar == 0):
            utils.dialogo_info(titulo = "PEDIDO NO SE PUEDE FACTURAR", 
                texto = "El pedido no se puede facturar. Compruebe que tiene "
                        "un cliente asignado y líneas que facturar.", 
                padre = self.wids['ventana'])
        else:
            # 1.- Creo el albarán de salida.
            alb_salida = crear_nuevo_albaran_salida(self.objeto)
            # 2.- Asocio los servicios al albarán de salida.
            for srv in servicios:
                srv.albaranSalida = alb_salida
                srv.syncUpdate()
            # 3.- Creo líneas de venta de los productos no trazables.
            entro_todo = True
            lineas_de_venta_creadas = []
            for producto in productos:
                if isinstance(producto, pclases.ProductoVenta):
                    # Salto los trazables.
                    entro_todo = False
                    continue
                textos_y_fechas = []
                fechas = productos[producto]['fechaEntrega']
                textos = productos[producto]['textoEntrega']
                i = 0
                for i in range(min(len(fechas), len(textos))):
                    textos_y_fechas.append("%s: %s" % (
                        utils.str_fecha(fechas[i]), textos[i]))
                j = i
                while j < len(fechas):
                    textos_y_fechas.append(utils.str_fecha(fechas[j]))
                    j += 1
                j = i
                while j < len(textos):
                    textos_y_fechas.append(textos[j])
                    j += 1
                desc_compl = "; ".join(textos_y_fechas)
                ldv = pclases.LineaDeVenta(
                    pedidoVenta = self.objeto, 
                    facturaVenta = None, # De momento. Después la relacionaré.
                    productoVenta = None, 
                    productoCompra = producto, 
                    albaranSalida = alb_salida, 
                    fechahora = mx.DateTime.localtime(), 
                    cantidad = (productos[producto]['pedido'] 
                                - productos[producto]['facturado']), 
                    precio = productos[producto]['precio'], 
                    descuento = productos[producto]['descuento'], 
                    notas = "\n\n".join(productos[producto]['notas']), 
                    descripcionComplementaria = desc_compl) 
                pclases.Auditoria.nuevo(ldv, self.usuario, __file__)
                lineas_de_venta_creadas.append(ldv)
            # 4.- Asocio las LDVs al albarán de salida. (Hecho arriba)
            # 5.- Cierro el albarán si ha entrado todo.
            if entro_todo:
                alb_salida.bloqueado = True
            # 6.- Abro el albarán en una nueva ventana.
            ## Mejor que no, porque es bloqueante.
            #import albaranes_de_salida
            #v = albaranes_de_salida.AlbaranesDeSalida(
            #    objeto = alb_salida, 
            #    usuario = self.usuario)
            # 7.- Creo la factura de venta.
            fra = crear_nueva_factura_venta(self.objeto)
            # 8.- Asocio los servicios del albarán a la factura.
            for srv in servicios:
                srv.facturaVenta = fra
            # 9.- Asocio las LDVs a la factura.
            for ldv in lineas_de_venta_creadas:
                ldv.facturaVenta = fra
            # 10.- Abro la factura en una ventana nueva. Se cerrará sola 
            #      cuando el usuario la imprima.
            import facturas_venta
            vfras = facturas_venta.FacturasVenta(objeto = fra, 
                                                 usuario = self.usuario)
            # 11.- Pregunto si crear nuevo pedido al mismo cliente.
            if utils.dialogo(titulo = "¿CREAR NUEVO PEDIDO?", 
                             texto = "¿Desea crear un nuevo pedido "
                                     "para el mismo cliente?", 
                             padre = self.wids['ventana']):
                puidsldv = pedir_clonar_ldvs(self.objeto, self.wids['ventana'])
                if puidsldv:
                    nuevo_pedido = self.objeto.clone(
                      fecha = mx.DateTime.localtime(), 
                      numpedido = 
                        `pclases.PedidoVenta.get_siguiente_numero_numpedido()`,
                      bloqueado = False, 
                      cerrado = False)
                    for puid in puidsldv:
                        ldp_o_srv = pclases.getObjetoPUID(puid)
                        try:
                            ldp_o_srv.clone(pedidoVenta = nuevo_pedido, 
                                            prefactura = None, 
                                            facturaVenta = None, 
                                            presupuesto = None, 
                                            albaranSalida = None)
                        except TypeError: # No es un servicio. ¿LDP? Sure, man!
                            ldp_o_srv.clone(pedidoVenta = nuevo_pedido, 
                                            presupuesto = None, 
                                            fechahora = mx.DateTime.localtime())
                    self.actualizar_ventana()
                    self.desconectar_dircorrespondencia()
                    self.ir_a(nuevo_pedido)
                    self.conectar_dircorrespondencia()
                else:
                    self.actualizar_ventana()

def unificar_ldps(pedido):
    """
    Unifica las LDPs de pedidos que sean idénticas.
    """
    ldps_copia = pedido.lineasDePedido[:]
    for i in xrange(len(ldps_copia)):
        borradas = []
        for j in xrange(i+1, len(ldps_copia)):
            if j not in borradas and ldps_iguales(ldps_copia[j], ldps_copia[i]):
                total_sin_descuento = (ldps_copia[i].precio * ldps_copia[i].cantidad) + (ldps_copia[j].precio * ldps_copia[j].cantidad)
                total_con_descuento = ldps_copia[i].get_subtotal(iva = False) + ldps_copia[j].get_subtotal(iva = False)
                ldps_copia[i].descuento = 1 - (total_con_descuento / total_sin_descuento)
                ldps_copia[i].cantidad += ldps_copia[j].cantidad
                if ldps_copia[j].notas:
                    ldps_copia[i].notas += "\n%s" % ldps_copia[j].notas
                ldps_copia[j].destroy(ventana = __file__)
                borradas.append(j)

def ldps_iguales(ldp1, ldp2):
    """
    Devuelve True si los campos de las dos LDPs son 
    iguales (a excepción de los ID, fechahora, cantidad
    y descuento).
    """
    def atributos_iguales(at1, at2):
        """
        Devuelve True si los dos valores son iguales.
        Si son del tipo float, redondea al tercer decimal.
        """
        if type(at1) == type(at2) and isinstance(at1, type(0.1)):
            return utils.float2str(at1, 3) == utils.float2str(at2, 3)
        return at1 == at2

    #campos = ("pedidoVentaID", "productoVentaID", "precio", "descuento", "fechaEntrega", "textoEntrega")
    campos = ("pedidoVentaID", "productoVentaID", "productoCompraID", "precio", "fechaEntrega", "textoEntrega")
    res = True
    for c in campos:
        res = res and atributos_iguales(getattr(ldp1, c), getattr(ldp2, c))
    return res

def crear_nuevo_albaran_salida(pedido):
    """
    Crea un nuevo albarán de salida con los datos por defecto obtenidos del 
    pedido de venta.
    Crea el albarán sí o sí, aunque no haya almacén del que descontar 
    existencias.
    """
    numalbaran = pclases.AlbaranSalida.get_siguiente_numero_numalbaran_str() 
    almacen = pclases.Almacen.get_almacen_principal_id_or_none()
    if not almacen:
        self.logger.error("%spedidos_de_venta.py::crear_nuevo_albaran_salida"
                          " -> ¡No hay almacén principal! No se descontarán"
                          " existencias por almacén, solo globales." % (
                          self.usuario and self.usuario.usuario + ": " or ""))
    albaran = pclases.AlbaranSalida(numalbaran = numalbaran, 
                                    transportista = None, 
                                    cliente = pedido.cliente, 
                                    bloqueado = False, 
                                    facturable = True, 
                                    destino = None, 
                                    fecha = pedido.fecha, 
                                    almacenOrigen = almacen, 
                                    almacenDestino = None)
    pclases.Auditoria.nuevo(albaran, None, __file__)
    return albaran

def crear_nueva_factura_venta(pedido):
    """
    Crea una factura de venta con los datos por defecto obtenidos del pedido.
    OJO: No se chequea que el pedido no tenga cliente o que éste no tenga 
    contador asignado.
    """
    cliente = pedido.cliente
    contador = cliente.contador
    last_fra = contador.get_last_factura_creada()
    if last_fra:
        if last_fra.fecha <= pedido.fecha:
            fecha = pedido.fecha
        else:
            fecha = max(last_fra.fecha, mx.DateTime.localtime())
    else:
        fecha = pedido.fecha 
    ### XXX: Este botón lo voy a usar yo, y a mí me viene mejor ponerle 
    ###      siempre la fecha actual, ya que siempre facturo los 25.
    fecha = max(fecha, mx.DateTime.today())
    ###
    dde = pclases.DatosDeLaEmpresa.select()[0]
    numfactura = contador.get_next_numfactura(commit = True)
    fra = pclases.FacturaVenta(
        cliente = cliente, 
        obra = pedido.obra, 
        fecha = fecha, 
        numfactura = numfactura, 
        descuento = pedido.descuento, 
        observaciones = "", 
        iva = pedido.iva, 
        bloqueada = False, 
        irpf = dde.irpf)
    pclases.Auditoria.nuevo(fra, None, __file__)
    return fra


def buscar_pedidos(a_buscar, buscar_solo_abiertos):
    """
    Busca pedidos de venta por cliente o número de pedido y según la opción 
    de solo abiertos o no.
    Devuelve un "result select".
    """
    PedV = pclases.PedidoVenta
    crit_numpedido_or_cliente = PedV.q.numpedido.contains(a_buscar)
    # And now... ¡también por cliente!
    if a_buscar and a_buscar.strip():
        clientes = pclases.Cliente.select(
            pclases.Cliente.q.nombre.contains(a_buscar))
        clientes = pclases.SQLtuple(clientes)
    else:
        clientes = pclases.SQLtuple()
    if clientes:
        subcrits = [crit_numpedido_or_cliente]
        for c in clientes:
            subcrits.append(PedV.q.clienteID == c.id)
        crit_numpedido_or_cliente = pclases.OR(*subcrits)
    if buscar_solo_abiertos:
        resultados = PedV.select(pclases.AND(
                        crit_numpedido_or_cliente,
                        PedV.q.cerrado == False))
    else:
        resultados = PedV.select(crit_numpedido_or_cliente)
    return resultados

def pedir_clonar_ldvs(pedido, ventana_padre = None):
    """
    Muestra un diálogo con el contenido del pedido recibido y devuelve los 
    PUID de las líneas de pedido y de servicio seleccionadas.
    Devuelve None si se cancela.
    """
    opciones = {}
    puids = {}
    for ldp in pedido.lineasDePedido:
        info = ldp.get_info()
        puid = ldp.get_puid()
        opciones[info] = True  # Por defecto todo marcado
        puids[info] = puid
    for srv in pedido.servicios:
        info = srv.get_info()
        puid = srv.get_puid()
        opciones[info] = True  # Por defecto todo marcado
        puids[info] = puid 
    resp = utils.dialogo_entrada(titulo = "SELECCIONE LÍNEAS", 
                        texto = "Seleccione las líneas de pedido o servicios\n"
                                "que desa copiar al nuevo pedido:", 
                        padre = ventana_padre, 
                        opciones = opciones, 
                        hide_entry = True)
    if resp == None:
        res = None
    else:
        res = []
        for k in opciones:
            if opciones[k]:
                res.append(puids[k])
    return res

if __name__=='__main__':
#    p = pclases.PedidoVenta.select()[-1]
    v = PedidosDeVenta()

