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
## confirmings.py - Gestión de confirmings recibidos. 
###################################################################
## NOTAS:
##  
## ----------------------------------------------------------------
## TODO: 
## Los confirmings (según pclases) se marcan automáticamente como 
## cobrados al pasar la fecha de vencimiento, pero para ello hay 
## que llamar a esta_pendiente. Habría que hacer un proceso 
## automático en el lado del servidor que actualizara los 
## confirmings sin intervención del usuario. 
###################################################################
## Changelog:
## 21 de noviembre de 2008 -> Inicio
## 
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
    from os.path import join as pathjoin
    sys.path.append(pathjoin("..", "framework"))
    import pclases
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes
from utils import _float as float
import mx, mx.DateTime

class Confirmings(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        Ventana.__init__(self, 'confirmings.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_nuevo/clicked': self.crear_nuevo,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_borrar/clicked': self.borrar,
                       'b_buscar/clicked': self.buscar,
                       'b_add_cobro/clicked': self.add_cobro,
                       'b_drop_cobro/clicked': self.drop_cobro,
                       'b_fechar/clicked': self.cambiar_fechar,
                       'b_fechac/clicked': self.cambiar_fechac,
                       'tb_pendiente/clicked': self.pendiente, 
                       'b_add_abono/clicked': self.add_abono, 
                       'b_recalcular/clicked': self.recalcular,
                       'b_split/clicked': self.dividir_confirming, 
                      }  
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        gtk.main()

    # --------------- Funciones auxiliares ------------------------------
    def dividir_confirming(self, boton):
        """
        Divide el confirming actual creando uno idéntico pero haciendo 
        corresponder a cada uno de ellos la mitad del importe total.
        Para que coincidan esos importes totales con el contenido del 
        confirming, duplica también los vencimientos asociados dividiendo 
        el importe en 2.
        """
        if utils.dialogo(titulo = "¿DIVIDIR PAGARÉ?", 
                         texto = "Se procederá a dividir el confirming actual"
                                 " en dos.\nAmbos serán idénticos y tendrán c"
                                 "omo importe total la mitad del importe actu"
                                 "al.\n\n¿Está seguro de dividir el confirmin"
                                 "g?", 
                         padre = self.wids['ventana']):
            original = self.objeto
            copia = pclases.Confirming(
                        codigo = original.codigo + " (DUPLICADO)", 
                        fechaRecepcion = original.fechaRecepcion, 
                        fechaCobro = original.fechaCobro,
                        cantidad = original.cantidad / 2.0, 
                        cobrado = original.cobrado, 
                        observaciones = '\n'.join((original.observaciones, 
                            'Duplicado. Cambie el número de confirming.')), 
                        fechaCobrado = original.fechaCobrado, 
                        procesado = original.procesado)
            original.cantidad = copia.cantidad
            for cobro in original.cobros:
                nuevo_cobro = pclases.Cobro(confirming = copia, 
                                facturaVenta = cobro.facturaVenta, 
                                prefactura = cobro.prefactura, 
                                facturaDeAbono = cobro.facturaDeAbono, 
                                cliente = cobro.cliente, 
                                fecha = cobro.fecha, 
                                importe = cobro.importe / 2.0, 
                                observaciones = 'Confirming con fecha ??/??/'
                                                '???? y vencimiento ??/??/??'
                                                '?? (pdte. de cobro)')
                cobro.importe = nuevo_cobro.importe
                factura = cobro.facturaVenta or cobro.prefactura
                if len(factura.vencimientosCobro) == 1:
                    vto_original = factura.vencimientosCobro[0]
                    vto_copia = pclases.VencimientoCobro(
                                    facturaVenta = vto_original.facturaVenta, 
                                    prefactura = vto_original.prefactura, 
                                    fecha = vto_original.fecha, 
                                    importe = vto_original.importe / 2.0, 
                                    observaciones='Duplicado automáticamente '
                                        'por división de confirming.')
                    vto_original.importe = vto_copia.importe
                elif len(factura.vencimientosCobro) > 1:
                    # Hay que determinar el vencimiento a duplicar.
                    pass
            self.actualizar_ventana()
            nueva_ventana = Confirmings(copia)
        
    def recalcular(self, boton):
        """
        Recalcula el total del confirming y coloca la suma de 
        los cobros que contiene en el campo correspondiente.
        No guarda la cantidad. Eso lo debe hacer el usuario si 
        está conforme.
        """
        confirming = self.objeto
        total = 0
        if confirming != None:
            for c in confirming.cobros:
                total += c.importe
        self.wids['e_cantidad'].set_text(utils.float2str(total))
                
    def es_diferente(self):
        """
        Devuelve True si la información en pantalla es distinta a la
        del objeto en memoria.
        """
        confirming = self.objeto
        if confirming == None: 
            return False	# Si no hay confirming activo, devuelvo que no 
                            # hay cambio respecto a la ventana
        condicion = self.wids['e_fechar'].get_text() \
            == confirming.fechaRecepcion.strftime('%d/%m/%Y')
        buffer = self.wids['txt_observaciones'].get_buffer()
        condicion = condicion and (buffer.get_text(buffer.get_start_iter(), 
                        buffer.get_end_iter()) == confirming.observaciones)
        condicion = condicion and (
            (self.wids['e_fechac'].get_text() 
                == confirming.fechaCobro.strftime('%d/%m/%Y')) 
             or self.wids['e_fechac'].get_text() == "" 
             and not confirming.fechaCobro)
        condicion = condicion and (
            (self.wids['e_fechar'].get_text() 
                == confirming.fechaRecepcion.strftime('%d/%m/%Y')) 
             or self.wids['e_fechar'].get_text() == "" 
             and not confirming.fechaRecepcion)
        condicion = condicion and (
            self.wids['e_cantidad'].get_text() 
                == "%s" % (utils.float2str(confirming.cantidad)))
        condicion = condicion and (
            self.wids['e_codigo'].get_text() == confirming.codigo)
        return not condicion	# Concición verifica que sea igual

    def aviso_actualizacion(self):
        """
        Muestra una ventana modal con el mensaje de objeto 
        actualizado.
        """
        utils.dialogo_info('ACTUALIZAR',
                           'El confirming ha sido modificado remotamente.\nD'
                           'ebe actualizar la información mostrada en pantal'
                           'la.\nPulse el botón «Actualizar»', 
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
        cols = (('Factura', 'gobject.TYPE_STRING', False, True, True, None),
                ('Importe', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_importe_cobro),
                ('Fecha vencimiento', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Importe total de la factura', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Vencimientos', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_cobros'], cols)
        self.colorear_cobros(self.wids['tv_cobros'])
        self.wids['tv_cobros'].connect("row-activated", self.abrir_factura)
        utils.rellenar_lista(self.wids['cbe_cliente'], 
          [(c.id, c.nombre) for c in pclases.Cliente.select(orderBy="nombre")])
        utils.combo_set_from_db(self.wids['cbe_cliente'], -1)   # Esto 
                                # quitará el elemento activo del combo.
        self.wids['cbe_cliente'].child.set_text("")
        def iter_cliente_seleccionado(completion, model, iter = None):
            if iter == None:    # Si me ha llamado el changed, el iter 
                                # habrá cambiado JUSTO AHORA.
                try:
                    iter = completion.get_active_iter()
                except AttributeError:
                    iter = None
            if iter != None:
                idcliente = model[iter][0]
                utils.combo_set_from_db(self.wids['cbe_cliente'], idcliente)
                for p in [p for p in self.objeto.cobros if p.cliente == None]:
                    p.clienteID = idcliente
            self.wids['cbe_cliente'].set_sensitive(
                len([c for c in self.objeto.cobros if c.cliente != None]) == 0)
        self.wids['cbe_cliente'].child.get_completion().connect(
            'match-selected', iter_cliente_seleccionado)
        self.wids['cbe_cliente'].connect('changed', 
            iter_cliente_seleccionado, 
            self.wids['cbe_cliente'].get_model(), 
            self.wids['cbe_cliente'].get_active_iter())

    def colorear_cobros(self, tv):
        """
        Colorea los cobros marcando en otro color aquellos 
        en los que la cantidad cubierta por el confirming (el cobro)
        difiera de la cantidad de la factura original.
        """
        def cell_func(col, cell, model, iter, numcol):
            valor = model[iter][numcol]
            if model[iter][1] != model[iter][3]:
                cell.set_property("foreground", "red")
            else:
                cell.set_property("foreground", "black")
            cell.set_property("text", valor)
        cols = tv.get_columns()
        for i in xrange(len(cols)):
            column = cols[i]
            if i == 1:
                cells = column.get_cell_renderers()
                for cell in cells:
                    column.set_cell_data_func(cell, cell_func, i)

    def abrir_factura(self, tv, path, view_column):
        model = tv.get_model()
        idcobro = model[path][-1]
        cobro = pclases.Cobro.get(idcobro)
        fra = cobro.facturaVenta
        if fra != None:
            import facturas_venta
            ventanafacturas = facturas_venta.FacturasVenta(fra)
        prefra = cobro.prefactura
        if prefra != None:
            import prefacturas
            ventanafacturas = prefacturas.Prefacturas(prefra)

    def cambiar_importe_cobro(self, cell, path, texto):
        """
        Cambia el importe del cobro.
        """
        model = self.wids['tv_cobros'].get_model()
        try:
            importe = utils.parse_euro(texto)
        except ValueError:
            utils.dialogo_info('ERROR EN FORMATO', 
                               'El importe introducido no es correcto.', 
                               padre = self.wids['ventana'])
            return
        idcobro = model[path][-1]
        cobro = pclases.Cobro.get(idcobro)
        cobro.importe = importe
        cobro.syncUpdate()
        model[path][1] = cobro.importe

    def activar_widgets(self, s):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        ws = ('hbuttonbox2', 'frame1', 'vbox2')  
        for w in ws:
            self.wids[w].set_sensitive(s)

    def ir_a_primero(self):
        """
        Hace que el primer registro -si lo hay- de la tabla implicada
        en el objeto del formulario sea el objeto activo.
        """
        confirming = self.objeto
        try:
            # Anulo el aviso de actualización del envío que deja de ser activo.
            if confirming != None: 
                confirming.notificador.set_func(lambda : None)
            confirming = pclases.Confirming.select(orderBy = "-id")[0]	
                # Selecciono todos y me quedo con el primero de la lista
            confirming.notificador.set_func(self.aviso_actualizacion)	
                # Activo la notificación
        except:
            confirming = None 	
        self.objeto = confirming
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
            cliente = r.cliente
            filas_res.append((r.id, 
                              r.codigo, 
                              cliente != None and cliente.nombre or "", 
                              utils.str_fecha(r.fechaRecepcion), 
                              "%s €" % (utils.float2str(r.cantidad)), 
                              utils.str_fecha(r.fechaCobro), 
                              r.pendiente and "Sí" or "No", 
                              ", ".join([c.numfactura for c in r.cobros])))
        idconfirming = utils.dialogo_resultado(filas_res,
                                           titulo = 'Seleccione Confirming',
                                           cabeceras = ('ID', 
                                                        'Número', 
                                                        'Cliente', 
                                                        'Fecha recepción', 
                                                        'Importe', 
                                                        'Vencimiento', 
                                                        'Pendiente', 
                                                        'Facturas'), 
                                           padre = self.wids['ventana'])
        if idconfirming < 0:
            return None
        else:
            return idconfirming

    def escribir_valor(self, widget, valor):
        """
        Con respecto al widget: intenta escribir el valor como si 
        fuera un Entry. Si no lo consigue lo intenta como si fuera
        un TextView.
        En cuanto al valor, lo convierte en cadena antes de escribirlo.
        """
        try:
            widget.set_text(str(valor))
        except AttributeError: #No tiene el set_text, por tanto no es un Entry.
            widget.get_buffer().set_text(valor)

    def leer_valor(self, widget):
        """
        Intenta leer el valor como si fuera un Entry. Si no lo 
        consigue lo hace suponiendo que es un TextView.
        Devuelve el valor leído _como cadena_.
        """
        try:
            res = widget.get_text()
        except AttributeError:
            buffer = widget.get_buffer()
            res = buffer.get_text(buffer.get_bounds()[0], 
                                  buffer.get_bounds()[1])
        return res

    def rellenar_widgets(self):
        """
        Introduce la información del confirming actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        confirming = self.objeto
        self.wids['e_codigo'].set_text(confirming.codigo)
        self.wids['e_fechar'].set_text(
            confirming.fechaRecepcion.strftime('%d/%m/%Y'))
        self.escribir_valor(self.wids['txt_observaciones'], 
                            confirming.observaciones)
        if not confirming.fechaCobro:
            self.wids['e_fechac'].set_text('')
        else:
            self.wids['e_fechac'].set_text(
                confirming.fechaCobro.strftime('%d/%m/%Y'))
        self.wids['e_cantidad'].set_text(
            '%s' % (utils.float2str(confirming.cantidad)))
        importe_facturas_cubiertas=sum([c.importe for c in confirming.cobros])
        if importe_facturas_cubiertas != confirming.cantidad:
            self.wids['e_cantidad'].modify_text(gtk.STATE_NORMAL, 
                self.wids['e_cantidad'].get_colormap().alloc_color("red"))
        else:
            self.wids['e_cantidad'].modify_text(gtk.STATE_NORMAL, 
                self.wids['e_cantidad'].get_colormap().alloc_color("black"))
        self.wids['tb_pendiente'].set_active(not confirming.pendiente)
        self.show_texto_boton_pendiente()
        self.rellenar_cobros()
        self.wids['cbe_cliente'].set_sensitive(len(confirming.cobros) == 0)
        self.objeto.make_swap()

    def show_texto_boton_pendiente(self):
        """
        Muestra el texto del botón de pendiente acorde al estado del pagaré.
        """
        confirming = self.objeto
        if not confirming:
            txtbutton = "No vencido"
        else:
            if self.wids['tb_pendiente'].get_active():
                if confirming.fechaCobrado < confirming.fechaVencimiento:
                    txtbutton = "Confirming adelantado"
                else:
                    txtbutton = 'Confirming cobrado'
            else:
                txtbutton = 'Confirming pendiente o no vencido'
        self.wids['tb_pendiente'].set_label(txtbutton)
    
    def rellenar_cobros(self):
        model = self.wids['tv_cobros'].get_model()
        model.clear()
        if self.objeto.cobros != []:
            utils.combo_set_from_db(self.wids['cbe_cliente'], 
                                    self.objeto.cobros[0].cliente.id)
        for c in self.objeto.cobros:
            if c.facturaVentaID != None:
                importe_factura = c.facturaVenta.importeTotal
                vencimientos = "(%d) "%(len(c.facturaVenta.vencimientosCobro))
                vencimientos += "; ".join(
                    ["%s: %s €" % (utils.str_fecha(v.fecha), 
                                   utils.float2str(v.importe)) 
                     for v in c.facturaVenta.vencimientosCobro])
            elif c.prefacturaID != None:
                importe_factura = c.prefactura.importeTotal
                vencimientos = "(%d) " % (len(c.prefactura.vencimientosCobro))
                vencimientos += "; ".join(["%s: %s €" % (
                        utils.str_fecha(v.fecha), 
                        utils.float2str(v.importe)) 
                    for v in c.prefactura.vencimientosCobro])
            elif c.facturaDeAbonoID != None:
                importe_factura = c.facturaDeAbono.importeTotal
                vencimientos = ""
            model.append((c.numfactura, 
                          "%s €" % (utils.float2str(c.importe)), 
                          utils.str_fecha(c.fecha), 
                          "%s €" % (utils.float2str(importe_factura)),
                          vencimientos,  
                          c.id))

    # --------------- Manejadores de eventos ----------------------------
    def crear_nuevo(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        confirming = self.objeto
        if confirming != None:
            confirming.notificador.set_func(lambda : None)
        self.objeto = pclases.Confirming(fechaCobro = mx.DateTime.localtime(), 
                                    cantidad = 0, 
                                    cobrado = -1, 
                                    fechaRecepcion = mx.DateTime.localtime(), 
                                    fechaCobrado = None,
                                    procesado = False)
        confirming = self.objeto
        confirming.notificador.set_func(self.aviso_actualizacion)
        utils.dialogo_info(titulo = 'PAGARÉ CREADO', 
                           texto = 'No olvide relacionar las facturas que '
                                   'cubre el efecto.', 
                           padre = self.wids['ventana'])
        utils.combo_set_from_db(self.wids['cbe_cliente'], -1)   # Esto quitará 
                                                # el elemento activo del combo.
        self.wids['cbe_cliente'].child.set_text("")
        self.actualizar_ventana()

    def buscar(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        confirming = self.objeto
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR PAGARÉ", 
                    texto = "Introduzca número, fecha del confirming o "
                            "número de factura:", 
                    padre = self.wids['ventana'])
        if a_buscar != None:
            if a_buscar.count('/') == 2:
                fecha = utils.parse_fecha(a_buscar) 
                resultados = pclases.Confirming.select(pclases.OR(
                                pclases.Confirming.q.fechaRecepcion == fecha, 
                                pclases.Confirming.q.fechaCobro == fecha))
                lon = resultados.count()
            else:
                resultados = pclases.Confirming.select(
                    pclases.Confirming.q.codigo.contains(a_buscar))
                resultados = list(resultados)
                facturas = pclases.FacturaVenta.select(
                    pclases.FacturaVenta.q.numfactura.contains(a_buscar))
                prefacturas = pclases.Prefactura.select(
                    pclases.Prefactura.q.numfactura.contains(a_buscar))
                if facturas.count() + prefacturas.count() > 0:
                    for f in facturas:
                        for c in f.cobros:
                            if (c.confirming != None and c.confirming 
                                not in resultados):
                                resultados.append(c.confirming)
                    for f in prefacturas:
                        for c in f.cobros:
                            if (c.confirming != None and c.confirming 
                                not in resultados):
                                resultados.append(c.confirming)
                lon = len(resultados)
            if lon > 1:
                ## Refinar los resultados
                idconfirming = self.refinar_resultados_busqueda(resultados)
                if idconfirming == None:
                    return
                resultados = [pclases.Confirming.get(idconfirming)]
            elif lon < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info('SIN RESULTADOS', 
                    'La búsqueda no produjo resultados.\nPruebe a cambiar el'
                    ' texto buscado o déjelo en blanco para ver una lista co'
                    'mpleta.\n(Atención: Ver la lista completa puede resulta'
                    'r lento si el número de elementos es muy alto)', 
                    padre = self.wids['ventana'])
                return
            ## Un único resultado
            # Primero anulo la función de actualización
            if confirming != None:
                confirming.notificador.set_func(lambda : None)
            # Pongo el objeto como actual
            confirming = resultados[0]
            # Y activo la función de notificación:
            confirming.notificador.set_func(self.aviso_actualizacion)
            self.objeto = confirming
            self.actualizar_ventana()

    def guardar(self, widget = None):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        confirming = self.objeto
        codigo = self.wids['e_codigo'].get_text()
        try:
            fechar = utils.parse_fecha(self.wids['e_fechar'].get_text())
        except:
            utils.dialogo_info(titulo = "ERROR EN FORMATO DE FECHA", 
                               texto = "El texto %s no es correcto o no repr"
                                       "esenta una fecha" % (
                                        self.wids['e_fechar'].get_text()), 
                               padre = self.wids['ventana'])
            fechar = self.objeto.fechaRecepcion
        try:
            fechac = utils.parse_fecha(self.wids['e_fechac'].get_text())
        except:
            utils.dialogo_info(titulo = "ERROR EN FORMATO DE FECHA", 
                texto = "El texto %s no es correcto o no representa una "
                        "fecha" % self.wids['e_fechar'].get_text(), 
                padre = self.wids['ventana'])
            fechac = self.objeto.fechaCobro
        buffer = self.wids['txt_observaciones'].get_buffer()
        observaciones = buffer.get_text(buffer.get_start_iter(), 
                                        buffer.get_end_iter())
        try:
            cantidad=float(self.wids['e_cantidad'].get_text().replace("€", ""))
        except:
            utils.dialogo_info(titulo = "ERROR EN FORMATO NUMÉRICO", 
                texto = "El texto %s no es correcto o no representa un "
                        "número" % self.wids['e_cantidad'].get_text(), 
                padre = self.wids['ventana'])
            cantidad = self.objeto.cantidad
        self.objeto.fechaRecepcion = fechar
        self.objeto.fechaCobro = fechac
        self.objeto.observaciones = observaciones
        self.objeto.cantidad = cantidad
        self.objeto.codigo = codigo
        # Fuerzo la actualización de la BD y no espero a que SQLObject lo 
        # haga por mí:
        confirming.syncUpdate()
        # Vuelvo a activar el notificador
        confirming.notificador.set_func(self.aviso_actualizacion)
        self.actualizar_ventana()
        self.wids['b_guardar'].set_sensitive(False)

    def pendiente(self, w):
        self.objeto.procesado = True     # Modifica manualmente, no procesar.
        if w.get_active():
            self.objeto.cobrado = self.objeto.cantidad
            # w.set_label('Confirming cobrado')
            self.objeto.fechaCobrado = mx.DateTime.today()
            self.objeto.syncUpdate()
            for c in self.objeto.cobros:
                c.fecha = self.objeto.fechaCobrado
                c.syncUpdate()
        else:
            self.objeto.cobrado = -1
            # w.set_label('Confirming pendiente')
            self.objeto.fechaCobrado = None
            self.objeto.syncUpdate()
            for c in self.objeto.cobros:
                c.fecha = self.objeto.fechaVencimiento
                c.syncUpdate()
        self.show_texto_boton_pendiente()
        self.guardar()
        self.objeto.sync()
        self.objeto.make_swap()
        w.set_active(w.get_active())
        self.actualizar_ventana()
        
    def refinar_resultados_busqueda_cliente(self, resultados):
        """
        Muestra en una ventana de resultados todos los
        registros de "resultados".
        Devuelve el id (primera columna de la ventana
        de resultados) de la fila seleccionada o None
        si se canceló.
        """
        filas_res = []
        for r in resultados:
            filas_res.append((r.id, r.nombre, r.cif))
        idcliente = utils.dialogo_resultado(filas_res,
                                titulo = 'Seleccione Cliente',
                                cabeceras = ('ID Interno', 'Nombre', 'CIF'), 
                                padre = self.wids['ventana'])
        if idcliente < 0:
            return None
        else:
            return idcliente

    def buscar_cliente(self):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        cliente = None
        a_buscar = utils.dialogo_entrada(titulo = "CIF", 
                            texto = "Introduzca nombre o CIF del cliente:", 
                            padre = self.wids['ventana']) 
        if a_buscar != None:
            criterio = pclases.OR(pclases.Cliente.q.nombre.contains(a_buscar),
                                  pclases.Cliente.q.cif.contains(a_buscar))
            resultados = pclases.Cliente.select(criterio) 
            if resultados.count() > 1:
                ## Refinar los resultados
                idcliente=self.refinar_resultados_busqueda_cliente(resultados)
                if idcliente == None:
                    return
                resultados = [pclases.Cliente.get(idcliente)]
            elif resultados.count() < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info('SIN RESULTADOS', 
                    'La búsqueda no produjo resultados.\nPruebe a cambiar el'
                    ' texto buscado o déjelo en blanco para ver una lista co'
                    'mpleta.\n(Atención: Ver la lista completa puede resulta'
                    'r lento si el número de elementos es muy alto)', 
                    padre = self.wids['ventana'])
                return
            ## Un único resultado
            cliente = resultados[0]
        return cliente

    def refinar_resultados_busqueda_factura(self, resultados):
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
            filas_res.append((r.id, r.numfactura, utils.str_fecha(r.fecha), 
                              nombrecliente))
        idsfactura = utils.dialogo_resultado(filas_res,
                titulo = 'Seleccione factura',
                cabeceras = ('ID', 'Número de factura', 'Fecha', 'Cliente'), 
                padre = self.wids['ventana'], 
                multi = True)
        if idsfactura < 0 or idfactura == [-1]:
            return None
        else:
            return idsfactura

    def buscar_factura(self, cliente):
        fras = None
        numfra = utils.dialogo_entrada(titulo = "NÚMERO DE FACTURA", 
                    texto = "Introduzca el número de factura", 
                    padre = self.wids['ventana'])
        if numfra != None:
            fras = [("FV:%d" % f.id, f.numfactura, utils.str_fecha(f.fecha), 
                     "%s €" % (utils.float2str(f.importeTotal))) 
                    for f in cliente.facturasVenta 
                        if numfra.upper() in f.numfactura.upper()]
            fras += [("PF:%d" % f.id, f.numfactura, utils.str_fecha(f.fecha), 
                      "%s €" % (utils.float2str(f.importeTotal))) 
                    for f in cliente.prefacturas 
                        if numfra.upper() in f.numfactura.upper()]
            if len(fras) > 1:
                idsfra = utils.dialogo_resultado(fras,
                            titulo = "SELECCIONE FACTURA",
                            cabeceras = ('ID', 'Número de factura', 
                                         'Fecha', 'Importe total'),
                            padre = self.wids['ventana'], 
                            multi = True)
            elif len(fras) == 1:
                idsfra = [fras[0][0]]
            else:
                utils.dialogo_info(titulo = "FACTURA NO ENCONTRADA", 
                                   texto = "No se encontró ninguna factura.", 
                                   padre = self.wids['ventana'])
                idsfra = []
            fras = []
            if len(idsfra) > 0 and idsfra[0] != -1:
                for tipo, id in [f.split(":") for f in idsfra]:
                    idfra = int(id)
                    if tipo == "FV":
                        fras.append(pclases.FacturaVenta.get(idfra))
                    elif tipo == "PF":
                        fras.append(pclases.Prefactura.get(idfra))
        return fras

    def preparar_vencimientos(self, factura):
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
        res = []
        vtos = [v for v in factura.vencimientosCobro]
        ests = [v for v in factura.estimacionesCobro]
        pags = factura.cobros
        mas_larga = [l for l in (vtos, ests, pags) 
                     if len(l)==max(len(vtos), len(ests), len(pags))][0]
        if len(mas_larga) == 0: return []
        for i in xrange(len(mas_larga)):
            res.append([None, None, None])
        def cmp(v1, v2):
            if v1.fecha < v2.fecha: return -1
            if v1.fecha > v2.fecha: return 1
            return 0
        def distancia(v1, v2):
            return abs(v1.fecha - v2.fecha)
        def lugar(v):
            if isinstance(v, pclases.VencimientoCobro):
                return 0
            elif isinstance(v, pclases.EstimacionCobro):
                return 1
            else:
                return 2
        resto = [vtos, ests, pags]
        resto.remove(mas_larga)
        mas_larga.sort(cmp)
        pos = 0
        for item in mas_larga:
            res [pos][lugar(item)] = item
            pos += 1
        for lista in resto:
            mlc = mas_larga[:]
            lista.sort(cmp)
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

    def buscar_vencimiento(self, factura):
        vtos_full = self.preparar_vencimientos(factura)
        if len(vtos_full) == 0:
            utils.dialogo_info(titulo = "FACTURA SIN VENCIMIENTOS", 
                texto = "La factura %s no tiene vencimientos.\nPara evitar in"
                        "coherencias, todo cobro o confirming debe correspond"
                        "erse con un vencimiento.\nCree los vencimientos ante"
                        "s de relacionar la factura con un confirming." % (
                            factura.numfactura), 
                padre = self.wids['ventana'])
            return None
        vtos = [(v[0].id, 
                 utils.str_fecha(v[0].fecha), 
                 "%s €" % (utils.float2str(v[0].importe)), 
                 v[0].observaciones, 
                 v[2] != None 
                    and v[2].confirmingID != None 
                    and v[2].confirming.codigo 
                    or "") 
                for v in vtos_full if v[0] != None] #\
                # if v[2] == None] # El vencimiento no tiene cobro "asociado".
        if len(vtos) > 1:
            idvto = utils.dialogo_resultado(vtos,
                        titulo = "SELECCIONE VENCIMIENTO",
                        cabeceras = ('ID', 'Fecha', 'Importe', 
                                     'Observaciones', 
                                     'Cubierto en confirming'),
                        padre = self.wids['ventana'])
        elif len(vtos) == 1:
            idvto = vtos[0][0]
        else:
            utils.dialogo_info(titulo = "FACTURA SIN VENCIMIENTOS", 
                texto = "La factura no tiene vencimientos o ya han sido "
                        "cubiertos en otro confirming.", 
                padre = self.wids['ventana'])
            idvto = -1
        if idvto > 0:
            vto = pclases.VencimientoCobro.get(idvto)
        else:
            vto = None
        return vto

    def add_cobro(self, b):
        confirming = self.objeto
        idcliente = utils.combo_get_value(self.wids['cbe_cliente'])
        if idcliente > 0:
            cliente = pclases.Cliente.get(idcliente)
        else:
            cliente = self.buscar_cliente()
        if cliente == None:
            return
        facturas = self.buscar_factura(cliente)
        if facturas == None:
            return
        for factura in facturas:
            if (factura.id in [c.facturaVentaID or c.prefacturaID 
                                for c in self.objeto.cobros] 
                and len(factura.vencimientosCobro) < 2):
                utils.dialogo_info(titulo = "FACTURA YA INCLUIDA", 
                    texto = "La factura %s ya ha sido incluida en este confi"
                            "rming." % (factura.numfactura), 
                    padre = self.wids['ventana'])
                continue
                # TODO: No controlo que no se pueda pagar el mismo vencimiento 
                # de la misma factura en dos confirmings diferentes.
            vencimiento = self.buscar_vencimiento(factura)
            if vencimiento == None:
                continue
            antes = sum([c.importe for c in confirming.cobros])
            if antes == confirming.cantidad:
                actualizar_cantidad = True  # Como el importe es la suma de 
                    # los cobros, el nuevo que añado ahora tiene que 
                    # actualizar la cantidad.
                    # Si no fuera así (el importe es distinto a la suma de 
                    # los cobros) es que se ha introducido a mano y por tanto 
                    # debo respetarlo.
            else:
                actualizar_cantidad = False
            observaciones = "Confirming %s con fecha %s y vencimiento %s" % (
                self.objeto.codigo, 
                utils.str_fecha(self.objeto.fechaRecepcion), 
                utils.str_fecha(self.objeto.fechaCobro))
            cobro = pclases.Cobro(facturaVenta = vencimiento.facturaVenta,
                                  prefactura = vencimiento.prefactura, 
                                  confirming = self.objeto,
                                  fecha = vencimiento.fecha,
                                  importe = vencimiento.importe,
                                  observaciones = observaciones, 
                                  facturaDeAbono = None)
            if actualizar_cantidad:
                if confirming.cobrado == confirming.cantidad:
                    confirming.cobrado = sum([c.importe 
                                                for c in confirming.cobros])
                    confirming.cantidad = confirming.cobrado
                else:
                    confirming.cantidad = sum([c.importe 
                                                for c in confirming.cobros])
            self.actualizar_ventana()
    
    def add_abono(self, boton):
        """
        Añade un "cobro" de una factura de abono (cobro con cantidad 
        negativa) al confirming de cobro actual.
        """
        confirming = self.objeto
        idcliente = utils.combo_get_value(self.wids['cbe_cliente'])
        if idcliente > 0:
            cliente = pclases.Cliente.get(idcliente)
        else:
            cliente = self.buscar_cliente()
        if cliente == None:
            return
        frabono = self.buscar_factura_de_abono(cliente)
        if frabono == None:
            return
        antes = sum([c.importe for c in confirming.cobros])
        observaciones = "Confirming %s con fecha %s y vencimiento %s" % (
                            self.objeto.codigo, 
                            utils.str_fecha(self.objeto.fechaRecepcion), 
                            utils.str_fecha(self.objeto.fechaCobro))
        c = pclases.Cobro(facturaVenta = None,
                          confirming = self.objeto,
                          fecha = frabono.fecha,
                          importe = frabono.importeTotal,
                          observaciones = observaciones, 
                          facturaDeAbono = frabono)
        if antes == confirming.cantidad:
            actualizar_cantidad = True  # Como el importe es la suma de los 
                # cobros, el nuevo que añado ahora tiene que actualizar la 
                # cantidad.
                # Si no fuera así (el importe es distinto a la suma de los 
                # cobros) es que se ha introducido a mano y por tanto debo 
                # respetarlo.
        else:
            actualizar_cantidad = False
        if actualizar_cantidad:
            if confirming.cobrado == confirming.cantidad:
                confirming.cobrado = sum([c.importe 
                                            for c in confirming.cobros])
                confirming.cantidad = confirming.cobrado
            else:
                confirming.cantidad = sum([c.importe 
                                            for c in confirming.cobros])
        self.actualizar_ventana()

    def buscar_factura_de_abono(self, cliente):
        """
        Busca, a través de diálogos, facturas de abono del cliente 
        recibido.
        PRECONDICIÓN: cliente no puede ser None.
        """
        frabono = None
        numabono = utils.dialogo_entrada(
                    titulo = "NÚMERO DE FACTURA DE ABONO", 
                    texto = "Introduzca el número de la factura de abono "
                            "que busca:", 
                    padre = self.wids['ventana'])
        if numabono != None:
            abonos = pclases.Abono.select(
                pclases.Abono.q.numabono.contains(numabono))
            if abonos.count() == 0:
                utils.dialogo_info(titulo = "ABONO NO ENCONTRADO", 
                    texto = "Factura con número de abono %s no encontrada." % (
                                numabono), 
                    padre = self.wids['ventana'])
            elif abonos.count() == 1:
                abono = abonos[0]
                frabono = abono.facturaDeAbono
                if frabono == None:
                    utils.dialogo_info(titulo = "ABONO SIN FACTURAR", 
                        texto = "El abono %s no ha generado factura de abono"
                                ".\n\n\n  Si el abono está completo, genere "
                                "la factura desde la ventana de abonos y vue"
                                "lva a intentarlo." % (abono.numabono), 
                        padre = self.wids['ventana'])
            else:
                abono = self.refinar_busqueda_abonos(abonos)
                if abono != None:
                    frabono = abono.facturaDeAbono
                    if frabono == None:
                        utils.dialogo_info(titulo = "ABONO SIN FACTURAR", 
                            texto = "El abono %s no ha generado factura de "
                                    "abono.\n\n\n  Si el abono está complet"
                                    "o, genere la factura desde la ventana "
                                    "de abonos y vuelva a intentarlo." % (
                                        abono.numabono), 
                            padre = self.wids['ventana'])
        return frabono

    def refinar_busqueda_abonos(self, abonos):
        """
        Recibe un SelectResults de abonos y muestra una ventana
        con la información de todos ellos.
        Devuelve la factura del abono seleccionado o None si cancela.
        """
        abono = None
        filas = [(a.id, 
                  utils.str_fecha(a.fecha), 
                  a.clienteID and a.cliente.nombre or "", 
                  a.importeSinIva, a.facturaDeAbonoID and a.numabono or "")
                 for a in abonos]
        idabono = utils.dialogo_resultado(filas, 
                                          titulo = "SELECCIONE ABONO", 
                                          cabeceras = ('ID', 
                                                       'Fecha', 
                                                       'Cliente', 
                                                       'Importe sin IVA', 
                                                       'Factura de abono'), 
                                          padre = self.wids['ventana'])
        if idabono != None and idabono != -1:
            abono = pclases.Abono.get(idabono)
        return abono
 
    def drop_cobro(self, b):
        confirming = self.objeto
        txt = """
        ¿Está seguro de desligar la factura seleccionada del confirming?       
        """
        if not utils.dialogo(titulo = '¿BORRAR?', 
                             texto = txt):
            return
        model, path = self.wids['tv_cobros'].get_selection().get_selected()
        idc = model[path][-1]
        cobro = pclases.Cobro.get(idc)
        antes = sum([c.importe for c in confirming.cobros])
        if antes == confirming.cantidad:
            actualizar_cantidad = True  # Como el importe es la suma de los 
                    # cobros, el nuevo que añado ahora tiene que actualizar 
                    # la cantidad. Si no fuera así (el importe es distinto a 
                    # la suma de los cobros) es que se ha introducido a mano
                    # y por tanto debo respetarlo.
        else:
            actualizar_cantidad = False
        cobro.destroySelf()
        if actualizar_cantidad:
            confirming.cantidad = sum([c.importe for c in confirming.cobros])
            if confirming.cobrado > confirming.cantidad:
                confirming.cobrado = confirming.cantidad
        self.actualizar_ventana()
        
    def cambiar_fechac(self, b):
        self.wids['e_fechac'].set_text(utils.str_fecha(
            utils.mostrar_calendario(padre = self.wids['ventana'])))

    def cambiar_fechar(self, b):
        self.wids['e_fechar'].set_text(utils.str_fecha(
            utils.mostrar_calendario(padre = self.wids['ventana'])))
        
    def borrar(self, widget):
        """
        Elimina el confirming en pantalla.
        """
        confirming = self.objeto
        if confirming != None:
            if utils.dialogo('¿Está seguro de eliminar el confirming actual?', 
                             'BORRAR PAGARÉ', 
                             padre = self.wids['ventana']):
                confirming.notificador.set_func(lambda : None)
                try:
                    for c in confirming.cobros:
                        c.destroySelf()
                    confirming.destroySelf()
                    self.ir_a_primero()
                except:
                    txt = """
                    El confirming no se eliminó completamente.                 
                    Tal vez el confirming o los vencimientos de facturas       
                    relacionados estén siendo referenciados por otros          
                    elementos de la aplicación. Contacte con el administrador. 
                    Información de depuración: 
                    """
                    for c in confirming.cobros:
                        txt += "ID cobro: %d.\n" % c.id
                    txt += "ID confirming: %d\n" % confirming.id
                    utils.dialogo_info(titulo = 'ERROR: NO SE PUDO BORRAR',
                                       texto = txt)


if __name__ == '__main__':
    v = Confirmings()

