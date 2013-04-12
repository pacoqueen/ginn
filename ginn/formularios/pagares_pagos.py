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
## pagares_pagos.py - Gestión de pagarés emitidos. 
###################################################################
## NOTAS:
## 
## 
###################################################################
## Changelog:
## 13 de julio de 2006 -> Inicio
## 2 de agosto de 2006 -> Impresión directa a LPT1
## 17 de noviembre de 2011 -> Renace la impresión directa por 
##                            culpa de Bankinter.
##
###################################################################
## NOTAS:
##  - Al abrir la ventana se marcarán automáticamente como pagados 
##    todos los pagarés que se hayan pasado de fecha de 
##    vencimiento. Si alguno no se ha pagado, será el usuario el 
##    que los marque manualmente como impagados.
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time
import sys, os
from framework import pclases
from informes import geninformes
import re
import mx, mx.DateTime
from formularios.utils import _float as float

# Modelos de cheques y pagarés:
MONTE, CAIXA, BANKINTER = (0, 1, 2)

class PagaresPagos(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'pagares_pagos.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_nuevo/clicked': self.crear_nuevo,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_borrar/clicked': self.borrar,
                       'b_buscar/clicked': self.buscar,
                       'b_add_pago/clicked': self.add_pago,
                       'b_drop_pago/clicked': self.drop_pago,
                       'b_fechae/clicked': self.cambiar_fechae,
                       'b_fechav/clicked': self.cambiar_fechav,
                       'b_logic/clicked': self.buscar_en_logic,
                       'b_pagare_monte/clicked': self.imprimir_pagare_monte,
                       'b_cheque_monte/clicked': self.imprimir_cheque_monte,
                       'b_pagare_caixa/clicked': self.imprimir_pagare_caixa,
                       'b_cheque_caixa/clicked': self.imprimir_cheque_caixa,
                       'b_monte/clicked': self.imprimir_monte, 
                       'b_caixa/clicked': self.imprimir_caixa,
                       'b_bankinter/clicked': self.imprimir_bankinter,
                       'tb_pendiente/clicked': self.pendiente, 
                       'b_add_manual/clicked': self.add_manual}
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
        pagare = self.objeto
        if pagare == None: return False	# Si no hay pagare activo, devuelvo que no hay cambio respecto a la ventana
        condicion = self.wids['e_fechae'].get_text() == pagare.fechaEmision.strftime('%d/%m/%Y')
        buffer = self.wids['txt_observaciones'].get_buffer()
        condicion = condicion and (buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter()) == pagare.observaciones)
        condicion = condicion and ((self.wids['e_fechav'].get_text() == pagare.fechaPago.strftime('%d/%m/%Y')) 
                                    or self.wids['e_fechav'].get_text() == "" and not pagare.fechaPago)
        condicion = condicion and ((self.wids['e_fechae'].get_text() == pagare.fechaEmision.strftime('%d/%m/%Y')) 
                                    or self.wids['e_fechae'].get_text() == "" and not pagare.fechaEmision)
        condicion = condicion and (self.wids['e_cantidad'].get_text() == "%s" % utils.float2str(pagare.cantidad))
        condicion = condicion and (self.wids['e_codigo'].get_text() == pagare.codigo)
        return not condicion	# Concición verifica que sea igual

    def aviso_actualizacion(self):
        """
        Activa el botón de actualizar.
        """
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
        self.wids['ch_imprenta'].set_active(True)
        self.wids['b_actualizar'].set_sensitive(False)
        self.wids['b_guardar'].set_sensitive(False)
        self.wids['b_nuevo'].set_sensitive(True)
        self.wids['b_buscar'].set_sensitive(True)
        cols = (('Factura', 'gobject.TYPE_STRING', False, True, True, None),
                ('Importe', 'gobject.TYPE_FLOAT', False, True, False, None),
                ('Fecha vencimiento', 'gobject.TYPE_STRING', False, True, False, None),
                ('Código Logic', 'gobject.TYPE_STRING', False, True, False, None),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_pagos'], cols)
        self.wids['tv_pagos'].connect("row-activated", self.abrir_factura)
        utils.rellenar_lista(self.wids['cbe_proveedor'], [(c.id, c.nombre) for c in pclases.Proveedor.select(orderBy="nombre")])
        def iter_proveedor_seleccionado(completion, model, itr = None):
            if itr == None:    # Si me ha llamado el changed, el iter habrá cambiado JUSTO AHORA.
                try:
                    itr = completion.get_active_iter()
                except AttributeError:
                    itr = None
            if itr != None:
                idproveedor = model[itr][0]
                utils.combo_set_from_db(self.wids['cbe_proveedor'], idproveedor)
                for p in [p for p in self.objeto.pagos if p.proveedor == None]:
                    p.proveedorID = idproveedor
            self.wids['cbe_proveedor'].set_sensitive(len([p for p in self.objeto.pagos if p.proveedor != None]) == 0)
        self.wids['cbe_proveedor'].child.get_completion().connect('match-selected', iter_proveedor_seleccionado)
        self.wids['cbe_proveedor'].connect('changed', iter_proveedor_seleccionado, 
                                                      self.wids['cbe_proveedor'].get_model(), 
                                                      self.wids['cbe_proveedor'].get_active_iter())

    def abrir_factura(self, tv, path, view_column):
        model = tv.get_model()
        idpago = model[path][-1]
        pago = pclases.Pago.get(idpago)
        fra = pago.facturaCompra
        if fra != None: 
            import facturas_compra
            ventanafacturas = facturas_compra.FacturasDeEntrada(fra)

    def activar_widgets(self, s):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        ws = ('hbuttonbox2', 'frame1', 'vbox2', 'hbox5')
        for w in ws:
            self.wids[w].set_sensitive(s)
        if self.usuario == None or self.usuario.nivel <= 2:
            self.wids['ch_lpt'].set_sensitive(True)
        else:
            self.wids['ch_lpt'].set_sensitive(False)

    def ir_a_primero(self):
        """
        Hace que el primer registro -si lo hay- de la tabla implicada
        en el objeto del formulario sea el objeto activo.
        """
        pagare = self.objeto
        try:
            # Anulo el aviso de actualización del envío que deja de ser activo.
            if pagare != None: pagare.notificador.set_func(lambda : None)
            pagare = pclases.PagarePago.select(orderBy="-id")[0]	
                # Selecciono todos y me quedo con el último creado
            pagare.notificador.set_func(self.aviso_actualizacion)		# Activo la notificación
        except:
            pagare = None 	
        self.objeto = pagare
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
            try:
                proveedor = r.pagos[0].facturaCompra.proveedor.nombre
            except (AttributeError, IndexError):
                try:
                    proveedor = r.pagos[0].proveedor.nombre
                except (AttributeError, IndexError):
                    proveedor = "" 
            if not r.fechaPago or r.fechaEmision >= r.fechaPago:
                tipo = "Cheque"
            else:
                tipo = "Pagaré"
            conceptos = "\n".join([p.concepto for p in r.pagos])
            filas_res.append((r.id, 
                              proveedor, 
                              tipo, 
                              conceptos, 
                              utils.str_fecha(r.fechaEmision), 
                              r.cantidad, 
                              utils.str_fecha(r.fechaPago), 
                              r.pendiente and "Sí" or "No"))
        idpagare = utils.dialogo_resultado(filas_res,
                                            titulo = 'Seleccione Pagaré',
                                            cabeceras = ('ID', 'Proveedor', 'Tipo', 'Conceptos', 'Fecha emisión', 'Importe', 'Vencimiento', 'Pendiente'), 
                                            padre = self.wids['ventana'])
        if idpagare < 0:
            return None
        else:
            return idpagare

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
        try:
            res = widget.get_text()
        except AttributeError:
            buffer = widget.get_buffer()
            res = buffer.get_text(buffer.get_bounds()[0], buffer.get_bounds()[1])
        return res

    def rellenar_widgets(self):
        """
        Introduce la información del pagare actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        pagare = self.objeto
        self.wids['e_codigo'].set_text(pagare.codigo)
        self.wids['e_fechae'].set_text(pagare.fechaEmision.strftime('%d/%m/%Y'))
        self.escribir_valor(self.wids['txt_observaciones'], pagare.observaciones)
        if not pagare.fechaPago:
            self.wids['e_fechav'].set_text('')
        else:
            self.wids['e_fechav'].set_text(pagare.fechaPago.strftime('%d/%m/%Y'))
        self.wids['e_cantidad'].set_text('%s' % utils.float2str(pagare.cantidad))
        self.wids['tb_pendiente'].set_active(not pagare.pendiente)
        if self.wids['tb_pendiente'].get_active():
            self.wids['tb_pendiente'].set_label('Confirmado')
        else:
            self.wids['tb_pendiente'].set_label('Pendiente')
        self.rellenar_pagos()
        self.wids['cbe_proveedor'].set_sensitive(len([p for p in pagare.pagos if p.proveedor != None]) == 0)
        if not pagare.fechaPago or pagare.fechaEmision >= pagare.fechaPago:
            self.wids['b_bankinter'].child.child.get_children()[1].set_text("Imprimir carta de cheque (Bankinter)")
        else:
            self.wids['b_bankinter'].child.child.get_children()[1].set_text("Imprimir carta de pagaré (Bankinter)")
        # Dejo modificar proveedor si los pagos que tiene asociados no tienen proveedor (por se de Logic, por ejemplo)
        self.objeto.make_swap()

    def rellenar_pagos(self):
        model = self.wids['tv_pagos'].get_model()
        model.clear()
        if self.objeto.pagos != []:
            try:
                utils.combo_set_from_db(self.wids['cbe_proveedor'], self.objeto.pagos[0].facturaCompra.proveedor.id)
            except AttributeError:
                try:
                    utils.combo_set_from_db(self.wids['cbe_proveedor'], self.objeto.pagos[0].proveedor.id)
                except AttributeError:
                    utils.combo_set_from_db(self.wids['cbe_proveedor'], -1)
        for c in self.objeto.pagos:
            model.append((c.facturaCompra != None and c.facturaCompra.numfactura or c.observaciones, 
                          c.importe, 
                          utils.str_fecha(c.fecha), 
                          c.logicMovimientos and c.logicMovimientos.get_codigo() or "", 
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
        pagare = self.objeto
        if pagare != None:
            pagare.notificador.set_func(lambda : None)
        # CWT: Fecha por defecto los 25 si no es domingo.
        fecha_defecto = mx.DateTime.localtime()
        while fecha_defecto.day != 25:
            fecha_defecto += mx.DateTime.oneDay
        if fecha_defecto.day_of_week == 6:
            fecha_defecto += mx.DateTime.oneDay
        self.objeto = pclases.PagarePago(fechaPago = fecha_defecto, 
                                         cantidad = 0, 
                                         pagado = -1, 
                                         fechaEmision = fecha_defecto, 
                                         fechaCobrado = None)
        pagare = self.objeto
        pclases.Auditoria.nuevo(pagare, self.usuario, __file__)
        pagare.notificador.set_func(self.aviso_actualizacion)
        utils.dialogo_info('PAGARÉ CREADO', 
                           '\n       Nuevo pagaré creado.        \n', 
                           padre = self.wids['ventana'])
        self.actualizar_ventana()

    def buscar(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        pagare = self.objeto
        a_buscar = utils.dialogo_entrada("Introduzca fecha o número de factura:", "BUSCAR PAGARÉ", padre = self.wids['ventana'])
        if a_buscar != None:
            if a_buscar.count('/') == 2:
                fecha = utils.parse_fecha(a_buscar) 
                resultados = pclases.PagarePago.select(pclases.OR(pclases.PagarePago.q.fechaEmision == fecha, 
                                                                     pclases.PagarePago.q.fechaPago == fecha))
                lon = resultados.count()
            elif a_buscar == "":
                resultados = pclases.PagarePago.select()
                lon = resultados.count()
            else:
                facturas = pclases.FacturaCompra.select(pclases.FacturaCompra.q.numfactura.contains(a_buscar))
                resultados = []
                for f in facturas:
                    for c in f.pagos:
                        if c.pagarePago != None and c.pagarePago not in resultados:
                            resultados.append(c.pagarePago)
                lon = len(resultados)
            if lon > 1:
                ## Refinar los resultados
                idpagare = self.refinar_resultados_busqueda(resultados)
                # print idpagare, resultados
                if idpagare == None:
                    return
                resultados = [pclases.PagarePago.get(idpagare)]
            elif lon < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info('SIN RESULTADOS', 
                                   'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.\n(Atención: Ver la lista completa puede resultar lento si el número de elementos es muy alto)', padre = self.wids['ventana'])
                return
            ## Un único resultado
            # Primero anulo la función de actualización
            if pagare != None:
                pagare.notificador.set_func(lambda : None)
            # Pongo el objeto como actual
            pagare = resultados[0]
            # Y activo la función de notificación:
            pagare.notificador.set_func(self.aviso_actualizacion)
            self.objeto = pagare
            self.actualizar_ventana()

    def guardar(self, widget = None):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        pagare = self.objeto
        codigo = self.wids['e_codigo'].get_text()
        try:
            fechae = utils.parse_fecha(self.wids['e_fechae'].get_text())
        except:
            utils.dialogo_info(titulo = "ERROR EN FORMATO DE FECHA", texto = "El texto %s no es correcto o no representa una fecha" % self.wids['e_fechae'].get_text(), padre = self.wids['ventana'])
            fechae = self.objeto.fechaEmision
        try:
            fechav = utils.parse_fecha(self.wids['e_fechav'].get_text())
        except:
            utils.dialogo_info(titulo = "ERROR EN FORMATO DE FECHA", texto = "El texto %s no es correcto o no representa una fecha" % self.wids['e_fechae'].get_text(), padre = self.wids['ventana'])
            fechav = self.objeto.fechaPago
        buffer = self.wids['txt_observaciones'].get_buffer()
        observaciones = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter())
        try:
            cantidad = utils.parse_euro(self.wids['e_cantidad'].get_text())
        except:
            utils.dialogo_info(titulo = "ERROR EN FORMATO NUMÉRICO", texto = "El texto %s no es correcto o no representa un número" % self.wids['e_cantidad'].get_text(), padre = self.wids['ventana'])
            cantidad = self.objeto.cantidad
        self.objeto.observaciones = observaciones
        self.objeto.cantidad = cantidad
        self.objeto.codigo = codigo
        self.objeto.fechaEmision = fechae
        self.objeto.fechaPago = fechav
        if self.objeto.fechaEmision == self.objeto.fechaPago:
            while self.objeto.fechaEmision.day_of_week >= 5:
                self.objeto.fechaEmision += mx.DateTime.oneDay
            self.objeto.fechaPago = self.objeto.fechaEmision
        while self.objeto.fechaPago.day_of_week >= 5:   # NOTA: La fecha de pago debe caer entre lunes y viernes.
            self.objeto.fechaPago += mx.DateTime.oneDay
        # Fuerzo la actualización de la BD y no espero a que SQLObject lo haga por mí:
        pagare.syncUpdate()
        # Vuelvo a activar el notificador
        pagare.notificador.set_func(self.aviso_actualizacion)
        self.actualizar_ventana()
        self.wids['b_guardar'].set_sensitive(False)

    def pendiente(self, w):
        if w.get_active():
            self.objeto.pagado = self.objeto.cantidad
            w.set_label('Confirmado')
        else:
            self.objeto.pagado = -1
            w.set_label('Pendiente')
        self.objeto.sync()
        self.objeto.make_swap()
        w.set_active(w.get_active())
        self.actualizar_ventana()
        
    def refinar_resultados_busqueda_proveedor(self, resultados):
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
        idproveedor = utils.dialogo_resultado(filas_res,
                                              titulo = 'Seleccione Proveedor',
                                              cabeceras = ('ID Interno', 'Nombre', 'CIF'), 
                                              padre = self.wids['ventana'])
        if idproveedor < 0:
            return None
        else:
            return idproveedor

    def buscar_proveedor(self):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        proveedor = None
        a_buscar = utils.dialogo_entrada("Introduzca nombre o CIF del proveedor:", padre = self.wids['ventana']) 
        if a_buscar != None:
            criterio = pclases.OR(pclases.Proveedor.q.nombre.contains(a_buscar),
                                    pclases.Proveedor.q.cif.contains(a_buscar))
            resultados = pclases.Proveedor.select(criterio) 
            if resultados.count() > 1:
                ## Refinar los resultados
                idproveedor = self.refinar_resultados_busqueda_proveedor(resultados)
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
            proveedor = resultados[0]
        return proveedor

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
            nombreproveedor = [r.proveedor and r.proveedor.nombre or ''][0]
            filas_res.append((r.id, r.numfactura, utils.str_fecha(r.fecha), nombreproveedor))
        idfactura = utils.dialogo_resultado(filas_res,
                                            titulo = 'Seleccione factura',
                                            cabeceras = ('ID', 'Número de factura', 'Fecha', 'Proveedor'),
                                            padre = self.wids['ventana'])
        if idfactura < 0:
            return None
        else:
            return idfactura

    def buscar_factura(self, proveedor):
        fra = None
        numfra = utils.dialogo_entrada(titulo = "NÚMERO DE FACTURA", 
                                       texto = "Introduzca el número de factura", 
                                       padre = self.wids['ventana'])
        if numfra != None:
            try:
                fras = [(f.id, f.numfactura, f.vistoBuenoPago and f.numeroControl or "", utils.str_fecha(f.fecha), "%s €" % (utils.float2str(f.importeTotal))) 
                        for f in proveedor.facturasCompra if numfra in f.numfactura and f.get_importe_primer_vencimiento_pendiente() != 0]
            except AssertionError, msg:
                self.logger.error("pagares_pagos::buscar_factura -> Aserción incumplida: %s" % msg)
            idfra = utils.dialogo_resultado(fras,
                                            titulo = "SELECCIONE FACTURA",
                                            cabeceras = ('ID', 'Número de factura', 'Número de control', 'Fecha fra.', 'Importe total'),
                                            padre = self.wids['ventana'])
            if idfra > 0:
                fra = pclases.FacturaCompra.get(idfra)
        return fra

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
        vtos = [v for v in factura.vencimientosPago]
        ests = [v for v in factura.estimacionesPago]
        pags = factura.pagos
        mas_larga = [l for l in (vtos, ests, pags) if len(l)==max(len(vtos), len(ests), len(pags))][0]
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
            if isinstance(v, pclases.VencimientoPago):
                return 0
            elif isinstance(v, pclases.EstimacionPago):
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
            utils.dialogo_info(titulo = "FACTURA SIN VENCIMIENTOS", texto = "La factura %s no tiene vencimientos.\nPara evitar incoherencias, todo pago o pagaré debe corresponderse con un vencimiento.\nCree los vencimientos antes de relacionar la factura con un pagaré." % factura.numfactura, padre = self.wids['ventana'])
            return
        vtos = [(v[0].id, utils.str_fecha(v[0].fecha), "%s €" % (utils.float2str(v[0].importe)), v[0].observaciones) for v in vtos_full \
                if v[2] == None]    # El vencimiento no tiene pago "asociado".
        idvto = utils.dialogo_resultado(vtos,
                                        titulo = "SELECCIONE VENCIMIENTO",
                                        cabeceras = ('ID', 'Fecha', 'Importe', 'Observaciones'),
                                        padre = self.wids['ventana'])
        if idvto > 0:
            vto = pclases.VencimientoPago.get(idvto)
        else:
            vto = None
        return vto

    def add_pago(self, b):
        # NOTA: Los abonos recibidos no se meten en el programa, en todo caso se cuentan como una factura negativa.
        pagare = self.objeto
        idproveedor = utils.combo_get_value(self.wids['cbe_proveedor'])
        if idproveedor > 0:
            proveedor = pclases.Proveedor.get(idproveedor)
        else:
            proveedor = self.buscar_proveedor()
        if proveedor == None:
            return
        factura = self.buscar_factura(proveedor)
        if factura == None:
            return
        vencimiento = self.buscar_vencimiento(factura)
        if vencimiento == None:
            return
        pago = pclases.Pago(facturaCompra = vencimiento.facturaCompra,
                            pagarePago = self.objeto,
                            fecha = vencimiento.fecha,
                            importe = vencimiento.importe,
                            proveedor = proveedor,
                            observaciones = 'Cubierto por el pagaré con fecha %s.' % (utils.str_fecha(self.objeto.fechaEmision)))
        pclases.Auditoria.nuevo(pago, self.usuario, __file__)
        if pagare.pagado == pagare.cantidad:
            pagare.pagado = sum([c.importe for c in pagare.pagos])
            pagare.cantidad = pagare.pagado
        else:
            pagare.cantidad = sum([c.importe for c in pagare.pagos])
        self.actualizar_ventana()
        
    def drop_pago(self, b):
        pagare = self.objeto
        txt = """
        ¿Está seguro de que desea eliminar la línea seleccionada del pagaré?          
        """
        if utils.dialogo(titulo = '¿BORRAR?', 
                         texto = txt, 
                         padre = self.wids['ventana']):
            model, path = self.wids['tv_pagos'].get_selection().get_selected()
            idc = model[path][-1]
            pago = pclases.Pago.get(idc)
            pago.destroy(ventana = __file__)
            pagare.cantidad = sum([c.importe for c in pagare.pagos])
            if pagare.pagado > pagare.cantidad:
                pagare.pagado = pagare.cantidad
            self.actualizar_ventana()

    def add_manual(self, boton):
        """
        Añade un pago al pagaré no relacionado ni con 
        factura de compra ni con asiento LOGIC. Sólo se
        debe usar para casos excepcionales en los que el 
        concepto a pagar no está en la BD y no es lo 
        suficientemente relevante como para darle alta.
        También puede servir para pequeños ajustes compensatorios.
        """
        pagare = self.objeto
        idproveedor = utils.combo_get_value(self.wids['cbe_proveedor'])
        if idproveedor > 0:
            proveedor = pclases.Proveedor.get(idproveedor)
        else:
            proveedor = self.buscar_proveedor()
        if proveedor != None:
            observaciones = utils.dialogo_entrada(titulo = "CONCEPTO",
                                                  texto = "Teclee el concepto del detalle a incluir en el pagaré:", 
                                                  padre = self.wids['ventana'])
            if observaciones != None:
                utils.dialogo_info(titulo = "FECHA DEL PAGO", 
                                   texto = "A continuación seleccione la fecha del concepto a incluir en el pagaré.", 
                                   padre = self.wids['ventana'])
                d, m, a = utils.mostrar_calendario(padre = self.wids['ventana'])
                fecha = mx.DateTime.DateTimeFrom(day = d, month = m, year = a)
                importe = utils.dialogo_entrada(titulo = "IMPORTE",
                                                texto = "Teclee el importe a añadir:", 
                                                padre = self.wids['ventana'])
                try:
                    importe = utils.parse_euro(importe)
                except ValueError:      # Ha tecleado algo que no es un número.
                    utils.dialogo_info(titulo = "VALOR INCORRECTO", 
                                       texto = "El importe tecleado (%s) no es un número válido." % (importe), 
                                       padre = self.wids['ventana'])
                    importe = None
                except AttributeError:  # Ha cancelado el diálogo anterior.
                    importe = None
                if importe != None:
                    pago = pclases.Pago(proveedor = proveedor, 
                                        logicMovimientos = None, 
                                        pagarePago = pagare, 
                                        facturaCompra = None, 
                                        fecha = fecha, 
                                        importe = importe, 
                                        observaciones = observaciones)
                    pclases.Auditoria.nuevo(pago, self.usuario, __file__)
                    if pagare.pagado == pagare.cantidad:
                        pagare.pagado = sum([c.importe for c in pagare.pagos])
                        pagare.cantidad = pagare.pagado
                    else:
                        pagare.cantidad = sum([c.importe for c in pagare.pagos])
                    self.actualizar_ventana()

    def cambiar_fechav(self, b):
        self.wids['e_fechav'].set_text(utils.str_fecha(utils.mostrar_calendario(padre = self.wids['ventana'])))

    def cambiar_fechae(self, b):
        self.wids['e_fechae'].set_text(utils.str_fecha(utils.mostrar_calendario(padre = self.wids['ventana'])))
        
    def borrar(self, widget):
        """
        Elimina el pagare en pantalla.
        """
        pagare = self.objeto
        if pagare != None:
            if utils.dialogo('¿Está seguro de eliminar el pagare actual?', 'BORRAR PAGARÉ', 
                             padre = self.wids['ventana']):
                pagare.notificador.set_func(lambda : None)
                try:
                    for c in pagare.pagos:
                        c.destroy(ventana = __file__)
                    pagare.destroy(ventana = __file__)
                    self.ir_a_primero()
                except:
                    txt = """
                    El pagare no se eliminó completamente.                          
                    Tal vez el pagaré o los vencimientos de facturas                
                    relacionados estén siendo referenciados por otros               
                    elementos de la aplicación. Contacte con el administrador.      
                    Información de depuración: 
                    """
                    for c in pagare.pagos:
                        txt += "ID pago: %d.\n" % c.id
                    txt += "ID pagaré: %d\n" % pagare.id
                    utils.dialogo_info(titulo = 'ERROR: NO SE PUDO BORRAR',
                                       texto = txt,
                                       padre = self.wids['ventana'])

    def acotar_busqueda(self, consulta, nombreproveedor):
        """
        Añade cláusulas OR en una AND para la búsqueda de asientos de LOGIC
        con las palabras completas de más 2 letras del nombre del proveedor.
        """
        import re
        Logic = pclases.LogicMovimientos
        expre = re.compile('[a-zA-Z|ñÑ][a-zA-Z|ñÑ]+')
        listapalabras = expre.findall(nombreproveedor)
        if len(listapalabras) == 1:
            consulta = pclases.AND(consulta, pclases.AND(Logic.q.comentario.contains(listapalabras[0])))
        elif len(listapalabras) > 1:
            subconsulta = pclases.OR(Logic.q.comentario.contains(listapalabras[0]), 
                                     Logic.q.comentario.contains(listapalabras[1]))
            for palabra in listapalabras[2:]:
                subconsulta = pclases.OR(subconsulta, Logic.q.comentario.contains(palabra))
            consulta = pclases.AND(consulta, subconsulta)
        return consulta

    def buscar_en_logic(self, boton):
        """
        Búsqueda en los apuntes de la base de datos de Logic para relacionar
        alguno con un nuevo pago y extraer de él la información para el pagaré.
        Si ya hay un proveedor seleccionado intenta acotar la búsqueda a los
        apuntes que tenga. 
        Mostrará los apuntes agrupados por cuenta en una nueva ventana con 
        un campo para filtrar la búsqueda por comentario.
        El apunte seleccionado que se devuelve en esa ventana es relacionado 
        con un nuevo pago que se asocia al pagaré actual.
        El resto de campos (fecha, vencimiento, factura, etc...) es MUY 
        DIFÍCIL de extraer de la BD de Logic, ya que se alternan mayúsculas 
        con minúsculas, espacios, notación extraña para las facturas y un 
        largo etcétera que hacen casi imposible la automatización completa.
        """
        pagare = self.objeto
        Logic = pclases.LogicMovimientos
        consulta = pclases.AND(Logic.q.importe >= 0, 
                               Logic.q.contrapartidaInfo == '',
                               pclases.OR(Logic.q.codigoCuenta.startswith('400'), 
                                          Logic.q.codigoCuenta.startswith('403'),
                                          Logic.q.codigoCuenta.startswith('410')),
                               pclases.NOT(Logic.q.comentario.startswith("Apertura Ejercicio")) ) 
        idproveedor = utils.combo_get_value(self.wids['cbe_proveedor'])
        if idproveedor > 0:
            proveedor = pclases.Proveedor.get(idproveedor)
            consulta = self.acotar_busqueda(consulta, proveedor.nombre)
        ventanalogic = BusquedaLogic(consulta = consulta, padre = self.wids['ventana'])
        apuntelogic = ventanalogic.get_objeto()
        if apuntelogic != None:
            # 1º Intentar localizar el proveedor.
            if idproveedor > 0:
                proveedor = pclases.Proveedor.get(idproveedor)
            else:
                # Si no está seleccionado, que lo busque, porque sacarlo del apunte
                # es imposible (abreviaturas, espacios, minúsculas...).
                proveedor = self.buscar_proveedor()
            if proveedor == None:
                return
            # 2º Buscar si se le puede asociar factura:
            utils.dialogo_info(titulo = "SELECCIONE FACTURA", 
                               texto = """
            A continuación seleccione la factura del proveedor              
            relacionada con el apunte contable.                             
                                                                            
            Si el apunte no se corresponde con una factura del              
            sistema, puede pulsar Cancelar a continuación para              
            ignorar la relación entre el pagaré y la factura de             
            compra quedando únicamente una relación entre el                
            pagaré y el asiento contable.                                   
            """,
                               padre = self.wids['ventana'])
            factura = self.buscar_factura(proveedor)
            if factura != None:
                vencimiento = self.buscar_vencimiento(factura)
            else:
                vencimiento = None
            fecha = vencimiento and vencimiento.fecha or self.rescatar_fecha_vto(apuntelogic) 
            importe = vencimiento and vencimiento.importe or apuntelogic.importe
            pago = pclases.Pago(facturaCompra = factura,
                                pagarePago = self.objeto,
                                fecha = fecha,
                                importe = importe,
                                #observaciones = 'Cubierto por el pagaré con fecha %s.' % (utils.str_fecha(self.objeto.fechaEmision)),
                                observaciones = apuntelogic.comentario,
                                proveedor = proveedor,
                                logicMovimientos = apuntelogic)
            pclases.Auditoria.nuevo(pago, self.usuario, __file__)
            if pagare.pagado == pagare.cantidad:
                pagare.pagado = sum([c.importe for c in pagare.pagos])
                pagare.cantidad = pagare.pagado
            else:
                pagare.cantidad = sum([c.importe for c in pagare.pagos])
            self.actualizar_ventana()

    def rescatar_fecha_vto(self, apuntelogic): 
        """
        Intenta obtener la fecha del vencimiento del apunte.
        Si no lo consigue, devuelve la fecha actual
        """
        res = mx.DateTime.localtime()
        efcompl = re.compile("\d+/\d+/\d+")
        efcorta = re.compile("\d+/\d+")
        c = apuntelogic.comentario
        encontrado = efcompl.findall(c)
        if len(encontrado) != 0:    # Si hay varias fechas, el vencimiento seguramente vendrá al final de la cadena.
            fecha = encontrado[-1]
            res = mx.DateTime.DateTimeFrom(day=int(fecha.split('/')[0]), 
                                           month=int(fecha.split('/')[1]),
                                           year=int(fecha.split('/')[2]))
        else:
            encontrado = efcorta.findall(c)
            if len(encontrado) != 0:
                fecha = encontrado[-1]
                res = mx.DateTime.DateTimeFrom(day=int(fecha.split('/')[0]), 
                                               month=int(fecha.split('/')[1]),
                                               year=mx.DateTime.localtime().year)
        return res
        
    def add_impr_observaciones(self, docimpreso):
        txt = "\nPagado mediante %s. Imprimido el %s." % \
            (docimpreso, utils.corregir_nombres_fecha(mx.DateTime.localtime().strftime("%d de %B de %Y")))
        buffer = self.wids['txt_observaciones'].get_buffer()
        buffer.insert_at_cursor(txt)
        self.guardar()
        
    def imprimir_cheque_monte(self, boton):
        from formularios import reports as informes
        import numerals
        pagare = self.objeto
        cantidad = pagare.cantidad
        if pagare.pagos == [] or pagare.pagos[0].proveedor == None:
            utils.dialogo_info(titulo = "SIN PROVEEDOR",
                               texto = "Debe seleccionar un proveedor antes de imprimir el pagaré.",
                               padre = self.wids['ventana'])
        else:
            receptor = pagare.pagos[0].proveedor.nombre
            euros = numerals.numerals(cantidad, moneda = 'euros', fraccion='centimos')
            fechaEmision = pagare.fechaEmision
            if self.wids['ch_lpt'].get_active():
                london_kills_me(cantidad, receptor, euros, fechaEmision, fechaEmision, pagare = False, entidad = MONTE)
            else:
                informes.abrir_pdf(geninformes.chequeMonte(cantidad,receptor,euros,fechaEmision))
            self.add_impr_observaciones("cheque El Monte")

    def imprimir_pagare_monte(self, boton):
        from formularios import reports as informes
        import numerals
        pagare = self.objeto
        fechaPago = pagare.fechaPago
        cantidad = pagare.cantidad
        if pagare.pagos == [] or pagare.pagos[0].proveedor == None:
            utils.dialogo_info(titulo = "SIN PROVEEDOR",
                               texto = "Debe seleccionar un proveedor antes de imprimir el pagaré.",
                               padre = self.wids['ventana'])
        else:
            receptor = pagare.pagos[0].proveedor.nombre
            euros = numerals.numerals(cantidad, moneda = 'euros', fraccion='centimos')
            fechaEmision = pagare.fechaEmision
            if self.wids['ch_lpt'].get_active():
                london_kills_me(cantidad, receptor, euros, fechaPago, fechaEmision, pagare = True, entidad = MONTE)
            else:
                informes.abrir_pdf(geninformes.pagareMonte(fechaPago,cantidad,receptor,euros,fechaEmision))
            self.add_impr_observaciones("pagaré El Monte")

    def imprimir_pagare_caixa(self, boton):
        from formularios import reports as informes
        import numerals
        pagare = self.objeto
        fechaPago = pagare.fechaPago
        cantidad = pagare.cantidad
        if pagare.pagos == [] or pagare.pagos[0].proveedor == None:
            utils.dialogo_info(titulo = "SIN PROVEEDOR",
                               texto = "Debe seleccionar un proveedor antes "
                                       "de imprimir el pagaré.",
                               padre = self.wids['ventana'])
        else:
            receptor = pagare.pagos[0].proveedor.nombre
            euros = numerals.numerals(cantidad, moneda = 'euros', 
                                      fraccion='centimos')
            fechaEmision = pagare.fechaEmision
            if self.wids['ch_lpt'].get_active():
                london_kills_me(cantidad, receptor, euros, fechaEmision, 
                                fechaPago, pagare = True, entidad = CAIXA)
            else:
                #informes.abrir_pdf(geninformes.pagareCaixa(fechaPago,cantidad,receptor,euros,fechaEmision))
                informes.abrir_pdf(geninformes.carta_pago(self.objeto, 
                    cheque = False, 
                    textofijo = self.wids['ch_imprenta'].get_active()))
            self.add_impr_observaciones("pagaré La Caixa")

    def imprimir_cheque_caixa(self, boton):
        from formularios import reports as informes
        import numerals
        pagare = self.objeto
        cantidad = pagare.cantidad
        if pagare.pagos == [] or pagare.pagos[0].proveedor == None:
            utils.dialogo_info(titulo = "SIN PROVEEDOR",
                               texto = "Debe seleccionar un proveedor antes de imprimir el pagaré.",
                               padre = self.wids['ventana'])
        else:
            if self.wids['ch_lpt'].get_active():
                receptor = pagare.pagos[0].proveedor.nombre
                euros = numerals.numerals(cantidad, moneda = 'euros', fraccion = 'centimos')
                fechaEmision = pagare.fechaEmision
                london_kills_me(cantidad, receptor, euros, fechaEmision, fechaEmision, pagare = False, entidad = CAIXA)
            else:
                #informes.abrir_pdf(geninformes.chequeCaixa(cantidad,receptor,euros,fechaEmision))
                informes.abrir_pdf(geninformes.carta_pago(self.objeto, textofijo = self.wids['ch_imprenta'].get_active()))
            self.add_impr_observaciones("cheque La Caixa")

    def imprimir_monte(self, boton):
        """
        Si la fecha de vencimiento es igual a la de emisión o es nula, imprime un cheque.
        En otro caso imprime un pagaré.
        """
        # CWT: Yo tampoco encuentro la necesidad de unificar los botones. No me mires así.
        pagare = self.objeto
        if not pagare.fechaPago or pagare.fechaEmision >= pagare.fechaPago:
            self.imprimir_cheque_monte(boton)
        else:
            self.imprimir_pagare_monte(boton)
        
    def imprimir_caixa(self, boton):
        """
        Si la fecha de vencimiento es igual a la de emisión o es nula, imprime un cheque.
        En otro caso imprime un pagaré.
        """
        # CWT: Yo tampoco encuentro la necesidad de unificar los botones. No me mires así.
        pagare = self.objeto
        if not pagare.fechaPago or pagare.fechaEmision >= pagare.fechaPago:
            self.imprimir_cheque_caixa(boton)
        else:
            self.imprimir_pagare_caixa(boton)

    def imprimir_bankinter(self, boton):
        """
        Si la fecha de vencimiento es igual a la de emisión o es nula, 
        imprime un cheque.
        En otro caso imprime un pagaré.
        """
        pagare = self.objeto
        if not pagare.fechaPago or pagare.fechaEmision >= pagare.fechaPago:
            self.imprimir_cheque_bankinter()
        else:
            self.imprimir_pagare_bankinter()

    def imprimir_pagare_bankinter(self):
        from formularios import reports as informes
        import numerals
        pagare = self.objeto
        fechaPago = pagare.fechaPago
        cantidad = pagare.cantidad
        if pagare.pagos == [] or pagare.pagos[0].proveedor == None:
            utils.dialogo_info(titulo = "SIN PROVEEDOR",
                               texto = "Debe seleccionar un proveedor antes "
                                       "de imprimir el pagaré.",
                               padre = self.wids['ventana'])
        else:
            receptor = pagare.pagos[0].proveedor.nombre
            euros = numerals.numerals(cantidad, moneda = 'euros', 
                                      fraccion='centimos')
            fechaEmision = pagare.fechaEmision
            if self.wids['ch_lpt'].get_active():
                london_kills_me(cantidad, receptor, euros, fechaEmision, 
                                fechaPago, pagare = True, entidad = BANKINTER)
            else:
                informes.abrir_pdf(geninformes.carta_pago(self.objeto, 
                    cheque = False, 
                    textofijo = self.wids['ch_imprenta'].get_active()))
            self.add_impr_observaciones("pagaré Bankinter")

    def imprimir_cheque_bankinter(self):
        from formularios import reports as informes
        import numerals
        pagare = self.objeto
        cantidad = pagare.cantidad
        if pagare.pagos == [] or pagare.pagos[0].proveedor == None:
            utils.dialogo_info(titulo = "SIN PROVEEDOR",
                               texto = "Debe seleccionar un proveedor antes de imprimir el pagaré.",
                               padre = self.wids['ventana'])
        else:
            if self.wids['ch_lpt'].get_active():
                receptor = pagare.pagos[0].proveedor.nombre
                euros = numerals.numerals(cantidad, moneda = 'euros', fraccion = 'centimos')
                fechaEmision = pagare.fechaEmision
                london_kills_me(cantidad, receptor, euros, fechaEmision, fechaEmision, pagare = False, entidad = BANKINTER)
            else:
                informes.abrir_pdf(geninformes.carta_pago(self.objeto, textofijo = self.wids['ch_imprenta'].get_active()))
            self.add_impr_observaciones("cheque Bankinter")


def abrir_paralelo(test = False):
    """
    Abre el puerto paralelo como un archivo independientemente
    de la plataforma windows o linux.
    """
    test = False
    import os
    if os.name == 'posix':
        try:
            if not test:
                f = open('/dev/lp0', 'wb')
            else:
                f = open("/tmp/lpt", "w")
        except IOError, msg:
            print "ERROR abriendo LPT: No hay permisos para abrir LPT1: %s" % (msg)
            f = None
    elif os.name == 'nt':
        try:
            f = open('lpt1:', 'wb')
        except IOError, msg:
            try:
                print "ERROR abriendo LPT: No se encontró 'lpt1:': %s\nIntentando 'prn:'" % (msg)
                f = open("prn:","wb")
            except IOError, msg:
                print "ERROR abriendo LPT: No se encontró 'prn:': %s" % (msg)
                f = None
    else:
        print "ERROR abriendo LPT: Plataforma no soportada."
        f = None
    return f

def ally_sheedy(texto):
    """
    Escribe en crudo en el la impresora conectada al puerto 
    paralelo el texto recibido.
    """
    lpt = abrir_paralelo()
    if lpt == None:
        utils.dialogo_info(titulo = "NO SE PUDO ABRIR LPT1",
                           texto = """
        Ocurrió un error al abrir el puerto paralelo.       
                                                            
        Si su sistema es GNU/Linux, trate de añadir         
        a su usuario al grupo "lp".                         
                                                            
        En otro caso, compruebe que su puerto LPT1          
        se encuentra bien configurado y es accesible        
        por las aplicaciones de su usuario.                 
        """) 
    else:
        lpt.write(texto)
        lpt.close()

def get_posicion_ultimo_espacio(texto, pos):
    """
    Devuelve la posición del último espacio (primero por la derecha)
    del texto recibido hasta la posición "pos".
    Si no hay ningún espacio, devuelve "pos".
    """
    try:
        return texto.rindex(' ', 0, pos)
    except ValueError:
        return pos

def corregir_long(texto, longitud = 80, cortar = True):
    """
    Corta el texto recibido para que se adapte a la longitud especificada.
    Si cortar es True, corta el texto. Si es False, lo divide en las líneas
    necesarias.
    """
    res = texto
    if len(texto) > longitud and cortar:
        res = texto[:get_posicion_ultimo_espacio(texto, longitud)]
    elif len(texto) > longitud and not cortar:
        res = ""
        while len(texto) > longitud:
            res += "%s\n" % texto[:get_posicion_ultimo_espacio(texto, longitud)]
            texto = texto[get_posicion_ultimo_espacio(texto, longitud):]
        res += texto
    return res

def build_pagare_monte(cantidad, destinatario, euros, fecha, vto):
    texto_cantidad = corregir_long(euros, longitud = 55, cortar = False)
    try:
        texto_cantidad_linea1, texto_cantidad_linea2 = texto_cantidad.split('\n')[:2]
    except ValueError:
        texto_cantidad_linea1, texto_cantidad_linea2 = texto_cantidad, ""
    texto_pagare_monte = \
"""_


            %s%s%s        %s

                   %s
        %s
%s
                                        %s%s%s




_
""" % (`vto.day`.ljust(3), 
       utils.corregir_nombres_fecha(vto.strftime('%B')).center(16),
       `vto.year`.rjust(5),
       utils.float2str(cantidad), 
       corregir_long(destinatario, longitud = 47, cortar = True), 
       texto_cantidad_linea1, 
       texto_cantidad_linea2, 
       `fecha.day`.ljust(3), 
       utils.corregir_nombres_fecha(fecha.strftime('%B')).center(16),
       `fecha.year`.rjust(5)
      )
    return texto_pagare_monte

def build_cheque_monte(cantidad, destinatario, euros, fecha):
    texto_cantidad = corregir_long(euros, longitud = 55, cortar = False)
    try:
        texto_cantidad_linea1, texto_cantidad_linea2 = texto_cantidad.split('\n')[:2]
    except ValueError:
        texto_cantidad_linea1, texto_cantidad_linea2 = texto_cantidad, ""
    texto_cheque_monte = \
"""_





                                            %s
                   %s
        %s
%s
                                    %s%s%s




_
""" % (utils.float2str(cantidad), 
       corregir_long(destinatario, longitud = 45, cortar = True), 
       texto_cantidad_linea1, 
       texto_cantidad_linea2, 
       `fecha.day`.ljust(3), 
       utils.corregir_nombres_fecha(fecha.strftime('%B')).center(20),
       `fecha.year`.rjust(5)
      )
    return texto_cheque_monte

def build_pagare_caixa(cantidad, destinatario, euros, fecha, vto):
    texto_cantidad = corregir_long(euros, longitud = 55, cortar = False)
    try:
        texto_cantidad_linea1, texto_cantidad_linea2 = texto_cantidad.split('\n')[:2]
    except ValueError:
        texto_cantidad_linea1, texto_cantidad_linea2 = texto_cantidad, ""
    texto_pagare_caixa = \
"""_




      %s de %s de %s            %s


             %s
        %s
%s
                                %s de %s de %s




_
""" % (`vto.day`.ljust(3), 
       utils.corregir_nombres_fecha(vto.strftime('%B')).center(10),
       `vto.year`.rjust(5),
       utils.float2str(cantidad), 
       corregir_long(destinatario, longitud = 55, cortar = True), 
       texto_cantidad_linea1, 
       texto_cantidad_linea2, 
       `fecha.day`.ljust(3), 
       utils.corregir_nombres_fecha(fecha.strftime('%B')).center(16),
       `fecha.year`.rjust(5)
      )
    return texto_pagare_caixa

def build_cheque_caixa(cantidad, destinatario, euros, fecha):
    texto_cantidad = corregir_long(euros, longitud = 50, cortar = False)
    try:
        texto_cantidad_linea1, texto_cantidad_linea2 = texto_cantidad.split('\n')[:2]
    except ValueError:
        texto_cantidad_linea1, texto_cantidad_linea2 = texto_cantidad, ""
    texto_cheque_caixa = \
"""_



                                                    %s

                           %s
                   %s
        %s
                            %s de %s de %s







_
""" % (utils.float2str(cantidad), 
       corregir_long(destinatario, longitud = 45, cortar = True), 
       texto_cantidad_linea1, 
       texto_cantidad_linea2, 
       `fecha.day`.ljust(3), 
       utils.corregir_nombres_fecha(fecha.strftime('%B')).center(20),
       `fecha.year`.rjust(5)
      )
    return texto_cheque_caixa

def build_pagare_bankinter(cantidad, destinatario, euros, fecha, vto):
    texto_cantidad = corregir_long(euros, longitud = 55, cortar = False)
    try:
        texto_cantidad_linea1, texto_cantidad_linea2 = texto_cantidad.split('\n')[:2]
    except ValueError:
        texto_cantidad_linea1, texto_cantidad_linea2 = texto_cantidad, ""
    texto_pagare_bankinter = \
"""_


             %s%s%s                    # %s #

       %s
             %s
    %s
                                               %s%s%s






_
""" % (`vto.day`.ljust(5), 
       utils.corregir_nombres_fecha(vto.strftime('%B')).center(12),
       `vto.year`.rjust(4),
       utils.float2str(cantidad), 
       corregir_long(destinatario, longitud = 47, cortar = True), 
       texto_cantidad_linea1, 
       texto_cantidad_linea2, 
       `fecha.day`.ljust(4), 
       utils.corregir_nombres_fecha(fecha.strftime('%B')).center(13),
       `fecha.year`.rjust(5)
      )
    return texto_pagare_bankinter

def build_cheque_bankinter(cantidad, destinatario, euros, fecha):
    texto_cantidad = corregir_long(euros, longitud = 55, cortar = False)
    try:
        texto_cantidad_linea1, texto_cantidad_linea2 = texto_cantidad.split('\n')[:2]
    except ValueError:
        texto_cantidad_linea1, texto_cantidad_linea2 = texto_cantidad, ""
    texto_cheque_bankinter = \
"""_




                                                     # %s #
                       %s
                 %s
      %s
                                             %s%s%s






_
""" % (utils.float2str(cantidad), 
       corregir_long(destinatario, longitud = 45, cortar = True), 
       texto_cantidad_linea1, 
       texto_cantidad_linea2, 
       `fecha.day`.ljust(3), 
       utils.corregir_nombres_fecha(fecha.strftime('%B')).center(16),
       `fecha.year`.rjust(5)
      )
    return texto_cheque_bankinter

def london_kills_me(cantidad, destinatario, euros, fecha, vencimiento, pagare, 
                    entidad = BANKINTER):
    if entidad == MONTE:
        if pagare:
            texto = build_pagare_monte(cantidad, destinatario, euros, fecha, 
                                       vencimiento)
        else:   # Cheque 
            texto = build_cheque_monte(cantidad, destinatario, euros, fecha)
    elif entidad == CAIXA:
        if pagare:
            texto = build_pagare_caixa(cantidad, destinatario, euros, fecha, 
                                       vencimiento)
        else:   # Cheque 
            texto = build_cheque_caixa(cantidad, destinatario, euros, fecha)
    else:   # entidad == BANKINTER: No queda otra. Valor por defecto.
        if pagare:
            texto = build_pagare_bankinter(cantidad, destinatario, euros, 
                                           fecha, vencimiento)
        else:   # Cheque 
            texto = build_cheque_bankinter(cantidad, destinatario, euros, 
                                           fecha)
    # print texto
    ally_sheedy(texto)

def sean_young():
    # De mitos eróticos de mi "despertar" va la cosa.
    """
    Imprime un cheque y un pagaré en el formato del papel contínuo de 
    Bankinter.
    """
    cantidad = 1234567.89
    destinatario = "Andy Kaufman, Bob Zmuda, George Shapiro & Tony Clifton Co."
    import numerals
    euros = numerals.numerals(cantidad, moneda = '', fraccion='céntimos')  
        # ¿Por qué lo pondría sin moneda?
    fecha = mx.DateTime.localtime()
    vencimiento = fecha + (mx.DateTime.oneDay * 7)
    print "Generando pagaré..."
    london_kills_me(cantidad, destinatario, euros, fecha, vencimiento, 
                    pagare = True)
    raw_input("Cambia el papel y dale a ENTER... ")
    print "Generando cheque..."
    london_kills_me(cantidad, destinatario, euros, fecha, vencimiento, 
                    pagare = False)


if __name__ == '__main__':
    v = PagaresPagos()
    #sean_young()

