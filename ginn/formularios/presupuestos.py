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
## presupuestos.py - Ofertas de precios a clientes.
###################################################################
## NOTAS:
##  
## ----------------------------------------------------------------
##  
###################################################################
## Changelog:
## 15 de marzo de 2007 -> Inicio 
## 
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk, mx.DateTime
from framework import pclases
from framework.seeker import VentanaGenerica 
from pedidos_de_venta import preguntar_precio
from formularios.ventana_progreso import VentanaActividad
import gobject
import sys

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
                       'b_pedido/clicked': self.hacer_pedido,  
                       "cbe_cliente/changed": self.cambiar_datos_cliente, 
                      }  
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        if self.usuario and self.usuario.nivel >= 4:
            self.activar_widgets(False) # Para evitar manos rápidas al abrir.
        gtk.main()

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
        del presupuesto si están vacíos.
        """
        idcliente = utils.combo_get_value(cbe)
        if not idcliente:
            return
        cliente = pclases.Cliente.get(idcliente)
        #if not self.wids["e_persona_contacto"].get_text():
        #    self.wids["e_persona_contacto"].set_text(cliente.contacto.strip())
        #if not self.wids["e_cliente"].get_text():
        #    self.wids["e_cliente"].set_text(cliente.nombre)
        if not self.wids["e_direccion"].get_text():
            self.wids["e_direccion"].set_text(cliente.direccion)
        if not self.wids["e_ciudad"].get_text():
            self.wids["e_ciudad"].set_text(cliente.ciudad)
        if not self.wids["e_provincia"].get_text():
            self.wids["e_provincia"].set_text(cliente.provincia)
        if not self.wids["e_cp"].get_text():
            self.wids["e_cp"].set_text(cliente.cp)
        if not self.wids["e_pais"].get_text():
            self.wids["e_pais"].set_text(cliente.pais)
        if not self.wids["e_telefono"].get_text():
            self.wids["e_telefono"].set_text(cliente.telefono)
        #if not self.wids["e_fax"].get_text():
        #    self.wids["e_fax"].set_text(cliente.fax)

    def hacer_pedido(self, boton):
        """
        Crea un pedido con el cliente del presupuesto y como contenido 
        las líneas de pedido y servicios del mismo.
        """
        utils.dialogo_info(titulo = "NO IMPLEMENTADO", 
                texto = "Característica en desarrollo.", 
                padre = self.wids['ventana'])
        return
        numpedido = utils.dialogo_entrada(texto = 'Introduzca un número de pedido.', titulo = 'NÚMERO DE PEDIDO', padre = self.wids['ventana'])
        if numpedido != None:
            existe = pclases.PedidoVenta.select(
                pclases.PedidoVenta.q.numpedido == numpedido)
            if existe.count() > 0:
                if utils.dialogo(titulo = "PEDIDO YA EXISTE", texto = "El número de pedido ya existe. ¿Desea agregar la oferta?", padre = self.wids['ventana']):
                    nuevopedido = existe[0]
                    if nuevopedido.cerrado:
                        utils.dialogo_info(titulo = "PEDIDO CERRADO", 
                                           texto = "El pedido %s está cerrado y no admite cambios. Corrija esta situación antes de volver a intentarlo.", 
                                           padre = self.wids['ventana'])
                        nuevopedido = None
                else:
                    nuevopedido = None
            else:
                nuevopedido = pclases.PedidoVenta(cliente=self.objeto.cliente, 
                                        fecha = mx.DateTime.localtime(), 
                                        numpedido = numpedido,
                                        iva = self.objeto.cliente.iva,
                                        descuento = 0,
                                        transporteACargo = False,
                                        bloqueado = True,
                                        cerrado = False, 
                                        comercial = self.objeto.comercial, 
                                        obra = self.objeto.obra)
                pclases.Auditoria.nuevo(nuevopedido, self.usuario, __file__)
            if nuevopedido != None:
                for ldp in self.objeto.lineasDePedido:
                    if ldp.pedidoVenta == None:
                        ldp.pedidoVenta = nuevopedido
                for srv in self.objeto.servicios:
                    if srv.pedidoVenta == None:
                        srv.pedidoVenta = nuevopedido
                self.actualizar_ventana()
                from formularios import pedidos_de_venta
                ventanapedido = pedidos_de_venta.PedidosDeVenta(objeto = nuevopedido, usuario = self.usuario)  # @UnusedVariable

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
        Añade una línea de pedido al presupuesto.
        """
        productos = utils.buscar_producto_general(self.wids['ventana'])
        for producto in productos:
            try:
                tarifa = self.objeto.cliente.tarifa
                precio = tarifa.obtener_precio(producto)
            except:
                precio = producto.preciopordefecto
            if precio == 0:
                precio = preguntar_precio(producto, self.wids['ventana'])
            cantidad = self.seleccionar_cantidad(producto)
            if cantidad == None:
                break
            if isinstance(producto, pclases.ProductoCompra):
                ldp = pclases.LineaDePresupuesto(pedidoVenta = None, 
                                            productoVenta = None, 
                                            productoCompra = producto, 
                                            cantidad = cantidad, 
                                            precio = precio, 
                                            descuento = 0, 
                                            fechaEntrega = None, 
                                            textoEntrega = "", 
                                            presupuesto = self.objeto)
            elif isinstance(producto, pclases.ProductoVenta):
                ldp = pclases.LineaDePresupuesto(pedidoVenta = None, 
                                            productoVenta = producto, 
                                            cantidad = cantidad, 
                                            precio = precio, 
                                            descuento = 0, 
                                            fechaEntrega = None, 
                                            textoEntrega = "", 
                                            presupuesto = self.objeto)
            pclases.Auditoria.nuevo(ldp, self.usuario, __file__)
        self.rellenar_tablas()
    
    def drop_ldp(self, boton):
        """
        Elimina las LDPs seleccionadas del presupuesto.
        """
        model, paths = self.wids['tv_contenido'].get_selection().get_selected_rows()
        fallo = False
        if  paths != None and paths != []:
            for path in paths:
                idldp = model[path][-1]
                ldp = pclases.LineaDePresupuesto.get(idldp)
                if ldp.pedidoVenta == None:
                    try:
                        ldp.destroy(ventana = __file__)
                    except:
                        fallo = True
                else:
                    fallo = True
            self.rellenar_tablas()
            if fallo:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "Algunas líneas no se pudieron eliminar por estar relacionadas con pedidos que han supuesto la aceptación del presupuesto.", 
                                   padre = self.wids['ventana']) 
    
    def add_srv(self, boton):
        """
        Añade un servicio al presupuesto. 
        """
        if self.objeto != None:
            concepto = utils.dialogo_entrada(titulo = "CONCEPTO", 
                                             texto = "Introduzca el concepto del servicio o transporte:", 
                                             padre = self.wids['ventana'])
            if concepto != None:
                srv = pclases.Servicio(pedidoVenta = None, 
                                       facturaVenta = None, 
                                       albaranSalida = None, 
                                       concepto = concepto, 
                                       cantidad = 0, 
                                       precio = 0, 
                                       descuento = 0, 
                                       presupuesto = self.objeto)
                pclases.Auditoria.nuevo(srv, self.usuario, __file__)
                self.rellenar_tablas()
    
    def drop_srv(self, boton):
        """
        Elimina los servicios seleccionados del presupuesto. 
        """
        model, paths = self.wids['tv_servicios'].get_selection().get_selected_rows()
        fallo = False
        if  paths != None and paths != []:
            for path in paths:
                idsrv = model[path][-1]
                srv = pclases.Servicio.get(idsrv)
                if srv.pedidoVenta == None and srv.albaranSalida == None and srv.get_factura_o_prefactura() == None:
                    try:
                        srv.destroy(ventana = __file__)
                    except:
                        fallo = True
                else:
                    fallo = True
            self.rellenar_tablas()
            if fallo:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "Algunos transportes no se pudieron eliminar por estar relacionados con pedidos,\nalbaranes o facturas que han supuesto la aceptación del presupuesto.", 
                                   padre = self.wids['ventana']) 

    
    def imprimir(self, boton):
        """
        Genera y abre el PDF de la carta de oferta.
        """
        utils.dialogo_info(titulo = "NO IMPLEMENTADO", 
                texto = "Característica en desarrollo.", 
                padre = self.wids['ventana'])
        return
        if self.objeto != None:
            from informes import geninformes
            from formularios.reports import abrir_pdf
            abrir_pdf(geninformes.generar_pdf_presupuesto(self.objeto))
        self.imprimir_presupuesto(boton)

    def imprimir_presupuesto(self, boton):
        """
        Imprime el presupuesto en formato "factura" en lugar de carta.
        """
        if self.objeto != None:
            modulo = pclases.config.get_modelo_presupuesto()
            import importlib
            presupuesto = importlib.import_module("." + modulo, "informes")
            #exec "import %s as presupuesto" % modulo
            from formularios.reports import abrir_pdf
            abrir_pdf(presupuesto.go_from_presupuesto(self.objeto))  # @UndefinedVariable

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
                except (ValueError, mx.DateTime.RangeError, TypeError):
                    igual = False
                valor_objeto = getattr(self.objeto, col.name)
                if colname == "comercialID" and valor_ventana == -1:
                        valor_ventana = None
                if isinstance(col, pclases.SODateCol):
                    valor_objeto = utils.abs_mxfecha(valor_objeto)
                if colname == "clienteID" and valor_ventana == None:
                    valor_ventana = self.wids['cbe_cliente'].child.get_text()
                    valor_objeto = self.objeto.nombrecliente
                if colname == "obraID" and valor_ventana == None:
                    valor_ventana = self.wids['cbe_obra'].child.get_text()
                    valor_objeto = self.objeto.nombreobra
                igual = igual and (valor_ventana == valor_objeto)
                if not igual:
                    if pclases.DEBUG and pclases.VERBOSE:
                        print "colname:", colname
                        print "\tvalor_ventana:", valor_ventana
                        print "\tvalor_objeto:", valor_objeto
                    break
        return not igual
    
    def reset_cache_credito(self):
        self.cache_credito = None

    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        self.reset_cache_credito()
        gobject.timeout_add(5 * 60 * 1000, self.reset_cache_credito)
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
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_contenido'], cols)
        self.wids['tv_contenido'].get_selection().set_mode(gtk.SELECTION_MULTIPLE)
    
    def cambiar_precio_ldp(self, cell, path, texto):
        """
        Cambia el precio de la LDP conforme al texto recibido.
        """
        try:
            precio = utils._float(texto)
        except:
            utils.dialogo_info(titulo = "ERROR", 
                               texto = 'El texto "%s" no es un número.' % (texto), 
                               padre = self.wids['ventana'])
        else:
            model = self.wids['tv_contenido'].get_model()
            ldp = pclases.LineaDePresupuesto.get(model[path][-1])
            if ldp.precio != precio:
                ldp.precio = precio
                if ldp.get_lineas_de_venta() != [] \
                   and utils.dialogo(titulo = "¿CAMBIAR PRECIO PRODUCTOS SERVIDOS?", 
                                 texto = """
                Al cambiar el precio de una parte del presupuesto ofertado,             
                se cambian automáticamente los precios de los pedidos                   
                involucrados. También puede cambiar los albaranes y facturas            
                si el pedido ya ha sido servido.                                        
                                                                                        
                ¿Desea cambiar el precio de todos los artículos servidos                
                de este producto?                                                       
                                                                                        
                Si lo hace, se cambiará también en la factura en caso de                
                que se haya facturado el albarán o albaranes                            
                correspondientes.                                                       
                """, 
                                padre = self.wids['ventana']):
                    for ldv in ldp.get_lineas_de_venta():
                        ldv.precio = ldp.precio
            self.rellenar_tablas()

    def cambiar_cantidad_ldp(self, cell, path, texto):
        """
        Cambia la cantidad de la LDP conforme al texto recibido.
        """
        try:
            cantidad = utils._float(texto)
        except:
            utils.dialogo_info(titulo = "ERROR", 
                               texto = 'El texto "%s" no es un número.' % (texto), 
                               padre = self.wids['ventana'])
        else:
            model = self.wids['tv_contenido'].get_model()
            ldp = pclases.LineaDePresupuesto.get(model[path][-1])
            ldp.cantidad = cantidad
            self.rellenar_tablas()

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
            s = s and es_mismo_comercial

        if self.objeto == None:
            s = False
        ws = tuple(['b_pedido', "table1",  
                    "tv_contenido", "b_add", "b_drop", 
                   ] + [self.dic_campos[k] for k in self.dic_campos.keys()])
        for w in ws:
            try:
                self.wids[w].set_sensitive(s)
            except:
                print w
        permiso_nuevos_pedidos = calcular_permiso_nuevos_pedidos(
                                    self.usuario, self.logger)
        self.wids['b_pedido'].set_sensitive(
            self.objeto != None 
            # and not aceptado_completo 
            and permiso_nuevos_pedidos 
            and self.objeto.esta_vigente())

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
                 r.comercial and r.comercial.empleado.nombre + " " + r.comercial.empleado.apellidos or "Sin comercial relacionado"))
        idpresupuesto = utils.dialogo_resultado(filas_res,
                            titulo = 'SELECCIONE OFERTA',
                            cabeceras = ('ID', 'Fecha', 
                                         'Nombre cliente', 
                                         'Obra', 
                                         "Comercial"), 
                            padre = self.wids['ventana'])
        if idpresupuesto < 0:
            return None
        else:
            return idpresupuesto

    def rellenar_widgets(self):
        """
        Introduce la información de el presupuesto actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        fdps = [(fdp.id, fdp.toString()) 
                for fdp in pclases.FormaDePago.select(orderBy = "plazo")]
        utils.rellenar_lista(self.wids['cb_forma_cobro'], fdps)
        utils.rellenar_lista(self.wids['cbe_cliente'], 
            [(p.id, p.nombre) for p in 
            pclases.Cliente.select(orderBy = "nombre") if not p.inhabilitado]) 
            # Lo pongo aquí por si crea un cliente nuevo sin cerrar esta 
            # ventana y lo quiere usar.
        comerciales = []
        if self.usuario and self.usuario.empleados:
            for e in self.usuario.empleados:
                for c in e.comerciales:
                    comerciales.append(c)
        if not comerciales or (self.usuario and self.usuario.nivel <= 2):
            comerciales = pclases.Comercial.select() 
        if self.objeto.comercial and self.objeto.comercial not in comerciales:
            comerciales.append(self.objeto.comercial)
        utils.rellenar_lista(self.wids['cb_comercial'], 
            [(c.id, c.empleado and c.empleado.get_nombre_completo() 
                or "Comercial desconocido (%s)" % c.puid) 
              for c in comerciales] + [(-1, "Sin comercial relacionado")]) 
        if self.objeto.cliente:
            obras = [(o.id, o.get_str_obra()) 
                     for o in self.objeto.cliente.obras]
        else:
            obras = []
        utils.rellenar_lista(self.wids['cbe_obra'], obras)
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
            else:
                self.escribir_valor(presupuesto.sqlmeta.columns[nombre_col], 
                                    getattr(presupuesto, nombre_col), 
                                    self.dic_campos[nombre_col])
        self.rellenar_tablas()
        # Algunos campos "especialitos":
        self.wids['e_numero'].set_text(str(presupuesto.id))
        # Comprobar riesgo
        self.comprobar_riesgo_cliente()
        self.objeto.make_swap()

    def comprobar_riesgo_cliente(self):
        """
        Actualiza el icono de estado de riesgo del cliente del presupuesto.
        """
        self.objeto.notificador.desactivar()
        vpro = VentanaActividad(self.wids['ventana'], 
                                "Comprobando condiciones de riesgo...")
        vpro.mostrar()
        vpro.mover()
        if self.objeto.cliente:
            if self.cache_credito == None:
                vpro.mover()
                importe_presupuesto = self.objeto.calcular_importe_total(
                                    iva = True)
                vpro.mover()
                self.cache_credito = self.objeto.cliente.\
                        calcular_credito_disponible(base = importe_presupuesto)
            if self.cache_credito < 0:
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
        txtestado = self.objeto.get_str_estado()
        self.wids['iconostado'].set_from_stock(iconostockstado, 
                                               gtk.ICON_SIZE_DND)
        self.wids['iconostado'].set_tooltip_text(txtestado)
        self.wids['b_pedido'].set_sensitive(
                iconostockstado == gtk.STOCK_YES
                and calcular_permiso_nuevos_pedidos(self.usuario, self.logger))
        self.actualizar_tooltip_de_cliente()
        vpro.ocultar()
        self.objeto.notificador.activar(self.aviso_actualizacion)        

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
        total = 0.0
        total += self.rellenar_contenido()
        total *= (1 - self.objeto.descuento)
        self.wids['e_total'].set_text("%s €" % (utils.float2str(total)))

    def rellenar_contenido(self):
        model = self.wids['tv_contenido'].get_model()
        model.clear()
        total = 0.0
        ldps = self.objeto.lineasDePresupuesto[:]
        ldps.sort(lambda x, y: int(x.id - y.id))
        for ldp in ldps:
            subtotal = ldp.get_subtotal()
            total += subtotal
            model.append((utils.float2str(ldp.cantidad), 
                          ldp.productoVenta 
                            and ldp.productoVenta.descripcion 
                            or ldp.productoCompra.descripcion, 
                          utils.float2str(ldp.precio, 3, autodec = True), 
                          utils.float2str(subtotal),
                          #ldp.pedidoVenta != None,
                          #ldp.pedidoVenta and ldp.pedidoVenta.numpedido or "", 
                          ldp.id))
        return total
    
    def nuevo(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
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
            comercial = comercial)
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
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR OFERTA", 
                                texto = "Introduzca número, nombre "\
                                        "del cliente u obra:", 
                                padre = self.wids['ventana']) 
        if a_buscar != None:
            try:
                ida_buscar = int(a_buscar)
            except ValueError:
                ida_buscar = -1
            criterio = pclases.OR(
                    pclases.Presupuesto.q.nombrecliente.contains(a_buscar),
                    pclases.Presupuesto.q.nombreobra.contains(a_buscar),
                    pclases.Presupuesto.q.personaContacto.contains(a_buscar),
                    pclases.Presupuesto.q.id == ida_buscar)
            resultados = pclases.Presupuesto.select(criterio)
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
                    utils.dialogo_info('SIN RESULTADOS', 'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.\n(Atención: Ver la lista completa puede resultar lento si el número de elementos es muy alto)',
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
                                   texto = "Se produjo un error al recuperar la información.\nCierre y vuelva a abrir la ventana antes de volver a intentarlo.", 
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
        # Desactivo el notificador momentáneamente
        self.objeto.notificador.activar(lambda: None)
        errores = []
        # Actualizo los datos del objeto
        for colname in self.dic_campos:
            col = self.clase.sqlmeta.columns[colname]
            try:
                valor_ventana = self.leer_valor(col, self.dic_campos[colname])
                if valor_ventana == -1 and colname == "comercialID":
                    valor_ventana = None
                if valor_ventana == None and colname == "clienteID":
                    self.objeto.cliente = None
                    valor_ventana = self.wids['cbe_cliente'].child.get_text()
                    colname = "nombrecliente"
                if valor_ventana == None and colname == "obraID":
                    self.objeto.obra = None
                    valor_ventana = self.wids['cbe_obra'].child.get_text()
                    colname = "nombreobra"
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
        if errores:
            utils.dialogo_info(titulo = "ERRORES AL GUARDAR", 
                    texto = "Se produjo un error al intentar guardar\n"
                            "los valores para los siguientes campos:\n"
                            + "\n - ".join(errores), 
                    padre = self.wids['ventana'])

    def borrar(self, widget):
        """
        Elimina el presupuesto de la tabla pero NO
        intenta eliminar ninguna de sus relaciones,
        de forma que si se incumple alguna 
        restricción de la BD, cancelará la eliminación
        y avisará al usuario.
        """
        presupuesto = self.objeto
        if utils.dialogo('¿Eliminar el presupuesto?\n\n\nATENCIÓN: Tenga en cuenta que si el presupuesto está aceptado se eliminará también \nla parte correspondiente de los pedidos relacionados con el mismo, etc...\n\n\nSI NO ESTÁ SEGURO, RESPONDA «NO».', 'BORRAR', padre = self.wids['ventana']):
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
            self.ir_a_primero()


def calcular_permiso_nuevos_pedidos(usuario, logger = None):
    if usuario == None:
        permiso_nuevos_pedidos = True
    else:
        try:
            ventana_pedidos = pclases.Ventana.select(pclases.Ventana.q.fichero == "pedidos_de_venta.py")[0]
        except IndexError:
            if logger:
                logger.error("presupuestos::activar_widgets -> Ventana de pedidos de venta no encontrada en la BD.")
            permiso_nuevos_pedidos = False
        else:
            permisos_ventana_pedidos = usuario.get_permiso(ventana_pedidos)
            permiso_nuevos_pedidos = permisos_ventana_pedidos.nuevo
    return permiso_nuevos_pedidos


if __name__ == "__main__":
    p = Presupuestos()

