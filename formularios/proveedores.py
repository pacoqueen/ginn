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
## proveedores.py - Alta, baja, consulta y mod. de proveedores. 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 11 de octubre de 2005 -> Inicio
## 11 de octubre de 2005 -> Funcional 99%
## 13 de diciembre de 2005 -> Añadidos nuevos campos a proveedores.
## 22 de diciembre de 2005 -> Cambio en el procedimiento para 
##                            guardar datos en un intento de 
##                            mejorar el rendimiento.
## 29 de enero de 2005 -> Portado a versión 02.
###################################################################
## DONE:
## - O la forma de pago o el documento de pago sobran de la 
##   ventana. Una de las dos cosas ya no se usa (mirar la ventana
##   de clientes equivalente para seguir el mismo criterio). No. No
##   sobra nada. Cada campo es para una cosa diferente.
###################################################################
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sqlobject
try:
    import pclases
except ImportError:
    import sys
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    import pclases
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes
from informes import abrir_pdf


def imprimir_listado(boton):
    """
    Imprime el listado de todos los proveedores de la base de datos.
    """
    proveedores = pclases.Proveedor.select(
        pclases.Proveedor.q.inhabilitado == False, orderBy = "nombre")
    abrir_pdf(geninformes.listado_proveedores(proveedores))


class Proveedores(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self._objetoreciencreado = None
        Ventana.__init__(self, 'proveedores.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_pedidos/clicked': self.ver_pedidos,
                       'b_facturas/clicked': self.ver_facturas,
                       'b_productos/clicked': self.ver_productos,
                       'b_nuevo/clicked': self.crear_nuevo_proveedor,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_borrar/clicked': self.borrar,
                       'b_buscar/clicked': self.buscar_proveedor, 
                       'b_listado/clicked': imprimir_listado, 
                       'b_next/clicked':           self.siguiente, 
                       'b_back/clicked':           self.anterior
                      }  
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        gtk.main()

    def anterior(self, boton = None):
        if self.objeto:
            orden = utils.combo_get_value(self.wids['cb_orden'])
            if orden == "Orden cronológico":
                proveedores = pclases.Proveedor.select(
                        pclases.Proveedor.q.id < self.objeto.id, 
                        orderBy = "-id")
            elif orden == "Orden alfabético": 
                proveedores = pclases.Proveedor.select(
                        pclases.Proveedor.q.nombre < self.objeto.nombre, 
                        orderBy = "-nombre")
            try:
                anterior = proveedores[0]
            except IndexError:
                anterior = None
            if anterior:
                self.objeto = anterior
                self.actualizar_ventana()
            else:
                utils.dialogo_info(titulo = "NO HAY MÁS PROVEEDORES", 
                        texto = "No hay proveedores anteriores al actual.", 
                        padre = self.wids['ventana'])

    def siguiente(self, boton = None):
        if self.objeto:
            orden = utils.combo_get_value(self.wids['cb_orden'])
            if orden == "Orden cronológico":
                proveedores = pclases.Proveedor.select(
                        pclases.Proveedor.q.id > self.objeto.id, 
                        orderBy = "id")
            elif orden == "Orden alfabético": 
                proveedores = pclases.Proveedor.select(
                        pclases.Proveedor.q.nombre > self.objeto.nombre, 
                        orderBy = "nombre")
            try:
                siguiente = proveedores[0]
            except IndexError:
                siguiente = None
            if siguiente:
                self.objeto = siguiente
                self.actualizar_ventana()
            else:
                utils.dialogo_info(titulo = "NO HAY MÁS PROVEEDORES", 
                        texto = "No hay proveedores posteriores al actual.", 
                        padre = self.wids['ventana'])

    # --------------- Funciones auxiliares ------------------------------
    def leer_valor(self, widget):
        """
        Intenta leer el valor como si fuera un Entry. Si no lo 
        consigue lo hace suponiendo que es un TextView.
        Devuelve el valor leído _como cadena_.
        """
        try:
            if isinstance(widget, gtk.CheckButton): 
                res = widget.get_active()
            elif hasattr(widget, "child"):
                res = widget.child.get_text()
            else:
                res = widget.get_text()
                if "iva" in widget.name:    # es feo, lo sé.
                    try:
                        res = utils.parse_porcentaje(res, fraccion = True)
                    except ValueError:
                        res = 0.21
        except AttributeError:
            buffer = widget.get_buffer()
            res = buffer.get_text(buffer.get_start_iter(), 
                                  buffer.get_end_iter())
        return res

    def es_diferente(self):
        """
        Devuelve True si la información en pantalla es distinta a la
        del objeto en memoria.
        """
        proveedor = self.objeto
        if proveedor == None: return False	# Si no hay proveedor activo, devuelvo que no hay cambio respecto a la ventana
        condicion = True
        for c in proveedor._SO_columns:
            if c.name != "tipoDeProveedorID":
                textobj = eval('proveedor.%s' % c.name)
                textven = self.leer_valor(self.wids['e_%s' % c.name]) 
                condicion = condicion and textobj == textven
                if not condicion:
                    break
            else:
                condicion = (condicion 
                    and proveedor.tipoDeProveedorID == utils.combo_get_value(
                        self.wids['cb_tipo_de_proveedor']))
        return not condicion	# Concición verifica que sea igual

    def aviso_actualizacion(self):
        """
        Muestra una ventana modal con el mensaje de objeto 
        actualizado.
        """
        utils.dialogo_info('ACTUALIZAR',
                           'El proveedor ha sido modificado remotamente.\nDebe actualizar la información mostrada en pantalla.\nPulse el botón «Actualizar»', 
                           padre = self.wids['ventana'])
        self.wids['b_actualizar'].set_sensitive(True)

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
        utils.combo_set_from_db(self.wids['cb_orden'], 
                                self.wids['cb_orden'].get_model()[0][0])
        cols = (('Nombre', 'gobject.TYPE_STRING', False, True, True, None),
                ('Banco', 'gobject.TYPE_STRING', False, True, False, None),
                ('Swift', 'gobject.TYPE_STRING', False, True, False, None),
                ('IBAN', 'gobject.TYPE_STRING', False, True, False, None),
                ('Cuenta', 'gobject.TYPE_STRING', False, True, False, None),
                ('Nombre banco', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Observaciones', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_cuentas'], cols)
        cols = (("Tipo", "gobject.TYPE_STRING", False, True, True, None), 
                ("ID", "gobject.TYPE_STRING", False, False, False, None))
        utils.preparar_listview(self.wids['tv_tipos_de_materiales'], cols)
        utils.rellenar_lista(self.wids['cb_tipo_de_proveedor'], 
                [(t.id, t.descripcion) 
                    for t in pclases.TipoDeProveedor.select(orderBy = "id")])

    def activar_widgets(self, s, chequear_permisos = True):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        ws = ('b_borrar', 'expander1', 'expander2', 'expander3', 'vbox2', 'vbox3')
        for w in ws:
            self.wids[w].set_sensitive(s)
        if chequear_permisos:
            self.check_permisos(nombre_fichero_ventana = "proveedores.py")

    def ir_a_primero(self):
        """
        Hace que el primer registro -si lo hay- de la tabla implicada
        en el objeto del formulario sea el objeto activo.
        """
        proveedor = self.objeto
        try:
            # Anulo el aviso de actualización del envío que deja de ser activo.
            if proveedor != None: proveedor.notificador.set_func(lambda : None)
            proveedor = pclases.Proveedor.select(orderBy = "-id")[0]	# Selecciono todos y me quedo con el primero de la lista
            proveedor.notificador.set_func(self.aviso_actualizacion)		# Activo la notificación
        except:
            proveedor = None 
        self.objeto = proveedor
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
            filas_res.append((r.id, r.nombre, r.cif, 
                              r.inhabilitado and "Sí" or "No"))
        idproveedor = utils.dialogo_resultado(filas_res,
                                titulo = 'Seleccione Proveedor',
                                cabeceras = ('ID Interno', 'Nombre', 'CIF', 
                                             "Inhabilitado"), 
                                padre = self.wids['ventana'])
        if idproveedor < 0:
            return None
        else:
            return idproveedor

    def escribir_valor(self, widget, valor):
        """
        Con respecto al widget: intenta escribir el valor como si 
        fuera un Entry. Si no lo consigue lo intenta como si fuera
        un TextView.
        En cuanto al valor, lo convierte en cadena antes de escribirlo.
        """
        try:
            if isinstance(widget, gtk.ComboBoxEntry): 
                widget.child.set_text(str(valor))
            elif isinstance(widget, gtk.CheckButton):
                widget.set_active(valor)
            else:
                if "iva" in widget.name:    # era feo más arriba y sigue siendo feo aquí.
                    widget.set_text("%s %%" % utils.float2str(valor * 100, 0))
                else:
                    widget.set_text(str(valor))
        except AttributeError: # No tiene el set_text, por tanto no es un Entry.
            widget.get_buffer().set_text(valor)

    def rellenar_widgets(self):
        """
        Introduce la información del proveedor actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        proveedor = self.objeto
        if proveedor != None:
            self.wids['ventana'].set_title("Proveedores - %s" % (proveedor.nombre))
            # Aprovechando que todo son "text" y los "entry" se llaman casi igual:
            for c in proveedor._SO_columns:
                if c.name != "tipoDeProveedorID":
                    textobj = getattr(proveedor, c.name)
                    # Reparo los Nones que haya en la BD
                    if textobj == None:
                        proveedor.notificador.set_func(lambda : None)
                        textobj = ''
                        setattr(proveedor, c.name, textobj)
                        proveedor.notificador.set_func(self.aviso_actualizacion)
                    self.escribir_valor(self.wids['e_%s' % c.name], textobj) 
                else:
                    utils.combo_set_from_db(self.wids['cb_tipo_de_proveedor'], 
                            proveedor.tipoDeProveedorID)
            self.rellenar_cuentas()
            self.rellenar_tipos_de_material()
            self.objeto.make_swap()

    def rellenar_cuentas(self):
        """
        Introduce en el TreeView las cuentas usadas por el 
        proveedor en transferencias (cuentasDestino)
        """
        proveedor = self.objeto
        model = self.wids['tv_cuentas'].get_model()
        model.clear()
        for cuenta in proveedor.cuentasDestino:
            model.append((cuenta.nombre, 
                          cuenta.banco, 
                          cuenta.swif, 
                          cuenta.iban,
                          cuenta.cuenta,  
                          cuenta.nombreBanco, 
                          cuenta.observaciones, 
                          cuenta.id))

    def rellenar_tipos_de_material(self):
        model = self.wids['tv_tipos_de_materiales'].get_model()
        model.clear()
        for t in self.objeto.get_tipos_de_proveedor_secundarios():
            model.append((t.descripcion, t.id))

    # --------------- Manejadores de eventos ----------------------------
    def crear_nuevo_proveedor(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        proveedor = self.objeto
        nombre = utils.dialogo_entrada(
                    texto = 'Introduzca el nombre del proveedor:',
                    titulo = 'NOMBRE PROVEEDOR', 
                    padre = self.wids['ventana'])
        if nombre == None:
            return
        cif = utils.dialogo_entrada(titulo = "CIF DEL PROVEEDOR", 
                texto = "Introduzca CIF (campo obligatorio):", 
                padre = self.wids['ventana'])
        if cif == None:
            return
        while (utils.parse_cif(cif) == "" or 
               pclases.Proveedor.select(pclases.Proveedor.q.cif==cif).count()):
            utils.dialogo_info(titulo = "CIF INVÁLIDO", 
             texto="El CIF tecleado %s no es válido o está repetido." % (cif), 
             padre = self.wids['ventana'])
            cif = utils.dialogo_entrada(titulo = "CIF DEL PROVEEDOR", 
                    texto = "Introduzca CIF (campo obligatorio):", 
                    padre = self.wids['ventana'])
            if cif == None:
                return
        cif = utils.parse_cif(cif)
        if proveedor != None:
            proveedor.notificador.set_func(lambda : None)
        tipo_por_defecto = pclases.TipoDeProveedor.get_por_defecto()
        self.objeto = pclases.Proveedor(nombre = nombre,
                                        cif = cif,
                                        direccion = '', # La carta de 
                                                    # pago se envía a 
                                                    # esta dirección.
                                        pais = '',
                                        ciudad = '',
                                        provincia = '',
                                        cp = '',
                                        telefono = '',
                                        fax = '',
                                        contacto = '',
                                        observaciones = '',
                                        direccionfacturacion = '',    
                                            # La factura lleva esta 
                                            # dirección.
                                        paisfacturacion = '',
                                        ciudadfacturacion = '',
                                        provinciafacturacion = '',
                                        cpfacturacion = '',
                                        email = '',
                                        formadepago = '120 D.F.F.',    
                                            # Campo obsoleto.
                                        documentodepago = 'Pagaré',
                                        vencimiento = '120 D.F.F.',
                                        diadepago = '25', 
                                        inhabilitado = False, 
                                        tipoDeProveedor = tipo_por_defecto)
        proveedor = self._objetoreciencreado = self.objeto
        pclases.Auditoria.nuevo(proveedor, self.usuario, __file__)
        proveedor.notificador.set_func(self.aviso_actualizacion)
        utils.dialogo_info('PROVEEDOR CREADO', 
            'Inserte el resto de la información del proveedor', 
            padre = self.wids['ventana'])
        self.actualizar_ventana()

    def buscar_proveedor(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        proveedor = self.objeto
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR PROVEEDOR", 
                                         texto = "Introduzca nombre o CIF del proveedor:", 
                                         padre = self.wids['ventana']) 
        if a_buscar != None:
            criterio = sqlobject.OR(pclases.Proveedor.q.nombre.contains(a_buscar),
            pclases.Proveedor.q.cif.contains(a_buscar))
            resultados = pclases.Proveedor.select(criterio) 
            if resultados.count() > 1:
                ## Refinar los resultados
                idproveedor = self.refinar_resultados_busqueda(resultados)
                if idproveedor == None:
                    return
                resultados = [pclases.Proveedor.get(idproveedor)]
            elif resultados.count() < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info('SIN RESULTADOS', 
                'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.\n(Atención: Ver la lista completa puede resultar lento si el número de elementos es muy alto)', 
                                   padre = self.wids['ventana'])
                return
            ## Un único resultado
            # Primero anulo la función de actualización
            if proveedor != None:
                proveedor.notificador.set_func(lambda : None)
            # Pongo el objeto como actual
            proveedor = resultados[0]
            # Y activo la función de notificación:
            proveedor.notificador.set_func(self.aviso_actualizacion)
            self.objeto = proveedor
            self.actualizar_ventana()

    def guardar(self, widget = None):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        proveedor = self.objeto
        # Si la dirección fiscal está en blanco, copio la postal:
        if self.wids['e_direccionfacturacion'].get_text().strip() == "":
            self.wids['e_direccionfacturacion'].set_text(self.wids['e_direccion'].get_text())
            self.wids['e_ciudadfacturacion'].set_text(self.wids['e_ciudad'].get_text())
            self.wids['e_paisfacturacion'].set_text(self.wids['e_pais'].get_text())
            self.wids['e_cpfacturacion'].set_text(self.wids['e_cp'].get_text())
            self.wids['e_provinciafacturacion'].set_text(self.wids['e_provincia'].get_text())
            self.wids['e_email'].set_text(self.wids['e_correoe'].get_text())
        # Valores por defecto para forma de pago:
        if self.wids['e_diadepago'].get_text().strip() == "":
            self.wids['e_diadepago'].set_text("25")
        if self.leer_valor(self.wids['e_vencimiento']).strip() == "": 
            self.escribir_valor(self.wids['e_vencimiento'], "90 D.F.F.")
        if self.wids['e_documentodepago'].get_text().strip() == "":
            self.wids['e_documentodepago'].set_text("Pagaré")
        # campo formadepago DEPRECATED. Lo pongo igual que "vencimiento" por si acaso.
        self.wids['e_formadepago'].set_text(self.leer_valor(self.wids['e_vencimiento'])) 
        # Desactivo el notificador momentáneamente
        proveedor.notificador.set_func(lambda: None)
        # Actualizo los datos del objeto
        cif = self.wids['e_cif'].get_text()
        self.wids['e_cif'].set_text(utils.parse_cif(cif) or self.objeto.cif)
        for c in [c.name for c in proveedor._SO_columns]:
            if c != "tipoDeProveedorID":
                valor = self.leer_valor(self.wids['e_%s' % c])
            else:
                valor=utils.combo_get_value(self.wids['cb_tipo_de_proveedor'])
            setattr(proveedor, c, valor)
        # Fuerzo la actualización de la BD y no espero a que SQLObject lo 
        # haga por mí:
        proveedor.syncUpdate()
        # Vuelvo a activar el notificador
        proveedor.notificador.set_func(self.aviso_actualizacion)
        self.objeto = proveedor
        self.actualizar_ventana()
        self.wids['b_guardar'].set_sensitive(False)

    def borrar(self, widget):
        """
        Elimina el proveedor en pantalla.
        """
        proveedor = self.objeto
        if proveedor != None:
            if utils.dialogo('¿Está seguro de eliminar el proveedor actual?', '¿BORRAR PROVEEDOR?', padre = self.wids['ventana']):
                proveedor.notificador.set_func(lambda : None)
                try:
                    proveedor.destroy(ventana = __file__)
                    self.ir_a_primero()
                except:
                    utils.dialogo_info(titulo = 'PROVEEDOR NO ELIMINADO', 
                                       texto = 'El proveedor no se pudo eliminar.', 
                                       padre = self.wids['ventana'])

    def ver_pedidos(self, boton):
        """
        Muestra todos los pedidos asignados
        al proveedor actual.
        """
        proveedor = self.objeto
        if proveedor == None: return
        pedidos = [(p.id, p.numpedido, utils.str_fecha(p.fecha)) for p in proveedor.pedidosCompra]
        idpedido = utils.dialogo_resultado(pedidos, 
                                           'PEDIDOS HECHOS AL PROVEEDOR',
                                           cabeceras = ('ID', 'Número de pedido', 'Fecha'), 
                                           padre = self.wids['ventana'])
        if idpedido > 0:
            import pedidos_de_compra
            p = pedidos_de_compra.PedidosDeCompra(pclases.PedidoCompra.get(idpedido), usuario = self.usuario)
    
    def ver_facturas(self, boton):
        """
        Muestra todos los facturas asignados
        al proveedor actual.
        """
        proveedor = self.objeto
        if proveedor == None: return
        facturas = [(p.id, p.numfactura, utils.str_fecha(p.fecha)) for p in proveedor.facturasCompra]
        idfactura = utils.dialogo_resultado(facturas, 
                                            'FACTUDAS DEL PROVEEDOR',
                                            cabeceras = ('ID', 'Número de factura', 'Fecha'), 
                                            padre = self.wids['ventana'])
        if idfactura > 0:
            import facturas_compra
            p = facturas_compra.FacturasDeEntrada(pclases.FacturaCompra.get(idfactura), usuario = self.usuario)
        
    def ver_productos(self, boton):
        """
        Muestra todos los productos relacionados
        con el proveedor actual a través de los
        Pedidos<->LDV<->Artículos.
        """
        proveedor = self.objeto
        if proveedor == None: 
            return
        lista = []
        productos = proveedor.get_productos()
        for p in productos:
            lista.append((p.id, 
                          p.codigo, 
                          p.descripcion, 
                          "\n".join([pedido.numpedido for pedido in p.get_pedidos(proveedor)]), 
                          "\n".join([albaran.numalbaran for albaran in p.get_albaranes(proveedor)]), 
                          "\n".join([factura.numfactura for factura in p.get_facturas(proveedor)])
                        ))
        idproducto = utils.dialogo_resultado(lista, 
                                             'PRODUCTOS COMPRADOS AL PROVEEDOR',
                                             cabeceras = ('ID', 'Código', 'Descripción', "Pedidos", "Albaranes", "Facturas"), 
                                             padre = self.wids['ventana'])
        if idproducto > 0:
            import productos_compra
            p = productos_compra.ProductosCompra(pclases.ProductoCompra.get(idproducto))

    def launch_browser_mailer(self, dialogo, uri, tipo):
        # FIXME: De momento sólo funciona para NT-compatibles. Usar el nuevo multi-open.
        # FIXME: Aquí aún no se usa. No sé cómo relacionar un entry con esto.
        if tipo == 'email':
            if os.name == 'nt':
                try:
                    os.startfile('mailto:%s' % uri) # if pywin32 is installed we open
                except:
                    pass
            else:
                utils.dialogo_info('NO IMPLEMENTADO', 
                                   'Funcionalidad no implementada.\nDebe lanzar manualmente su cliente de correo.\nCorreo-e seleccionado: %s' % (uri), 
                                   padre = self.wids['ventana'])
        elif tipo == 'web':
            if os.name == 'nt':
                try:
                    os.startfile(uri)
                except:
                    pass
            else:
                utils.dialogo_info('NO IMPLEMENTADO', 
                                   'Funcionalidad no implementada.\nDebe lanzar manualmente su navegador web.\nURL seleccionada: %s' % (uri), 
                                   padre = self.wids['ventana'])


if __name__=='__main__':
    try:
        v = Proveedores(
            usuario = pclases.Usuario.selectBy(usuario = "marilo")[0])
    except IndexError:
        v = Proveedores()

