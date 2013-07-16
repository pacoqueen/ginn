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
## facturacion_por_cliente_y_fechas.py - 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 29 de mayo de 2006 -> Inicio
## 29 de mayo de 2006 -> Testing
## 11 de febrero de 2006 -> Añadidos abonos a la facturación.
###################################################################
## DONE:
## + Añadir abonos con factura de abono generada y pendientes de 
##   descontar en una factura de venta o pagaré.
## TODO:
## + Ventana de progreso. Tarda más de lo que debería y parece 
##   como si se hubiera colgado.
###################################################################

import pygtk
pygtk.require('2.0')
import gtk
import mx.DateTime
from framework import pclases
from informes import geninformes
from informes.treeview2pdf import treeview2pdf
from informes.treeview2csv import treeview2csv
from formularios.reports import abrir_pdf, abrir_csv
from formularios.ventana_progreso import VentanaProgreso
from formularios import utils
from formularios.ventana import Ventana

import re
rex_importe_fras = re.compile("[\(\[].*[\]\)]")

def cambiar_fecha(entry, padre = None):
    """
    Cambia el texto del entry por la fecha seleccionada en un diálogo 
    centrado en la ventana "padre".
    """
    try:
        entry.set_text(utils.str_fecha(utils.mostrar_calendario(
            fecha_defecto = utils.parse_fecha(entry.get_text()), 
            padre = padre)))
    except:     # Probablemente fecha mal formada, mx.DateTime.RangeError, 
                # pero me curo en salud y capturo todas.
        entry.set_text(utils.str_fecha(utils.mostrar_calendario(padre=padre)))

def generar_color(txt):
    """
    Devuelve un gtk.gdk.Color único para el texto recibido y en función de él.
    Se asegura también que el color devuelto sea lo suficientemente 
    claro para hacer buen contraste con el texto negro.
    """
    fmul = 900      # Factor de multiplicación para aclarar el color.
    color = gtk.gdk.color_parse("white")
    if txt:
        txt = txt[::-1]
        lon = len(txt)
        if lon:
            rojo = (ord(txt[0]) * fmul) % 65536
            lon -= 1
        else:
            rojo = 32767
        if lon:
            verde = (ord(txt[1]) * fmul) % 65536
            lon -= 1
        else:
            verde = 32767
        if lon:
            azul = (ord(txt[2]) * fmul) % 65536
            lon -= 1
        else:
            azul = 32767
        color = gtk.gdk.Color(rojo, verde, azul)
    return color

def agregar_a_model(model, factura, padre, tv, nodos_clientes):
    """
    Introduce la información de la factura en el model.
    La factura es el nodo raíz. El primero de los cobros y de los 
    vencimientos estará también en la misma línea. Los siguientes
    se agregarán como hijos del nodo raíz. (sub-raíz en realidad.
    Tiene un nodo padre que sí es raíz en el TreeView)
    Devuelve el importe total de la factura, el importe cobrado, 
    el importe pendiente de cobro, la suma de los importes de los
    vencimientos con pagarés, la suma de los importes de los 
    vencimientos con pagarés que no están pendiente, la suma de 
    los importes de pagarés pendientes y la suma de los cobros sin 
    pagaré.
    """
    if isinstance(factura, pclases.Prefactura):
        numfactura = "* %s (%s €)" % (factura.numfactura, 
                                      utils.float2str(factura.importeTotal))
    else:
        numfactura = "%s (%s €)" % (factura.numfactura, 
                                    utils.float2str(factura.importeTotal))
    fecha = utils.str_fecha(factura.fecha)
    row = [numfactura, fecha]
    vencimientos_y_cobros = factura.emparejar_vencimientos()
    total_fra = factura.importeTotal
    total_vtos = 0.0
    cobrado = pendiente = 0.0
    total_pagares = cobrado_pagares = pendiente_pagares = 0.0
    total_otros = cobrado_otros = pendiente_otros = 0.0
    total_cobrado_strict = 0.0
    for vto, cobro, pagare in generador_vcps(vencimientos_y_cobros):
        esta_pendiente = cobro == None or (cobro.pagareCobroID != None 
                                           and cobro.pagareCobro.pendiente)
        if esta_pendiente:
            pendiente+=(vto and vto.importe) or (cobro and cobro.importe) or 0
                # Puede ser un cobro suelto (de los de None en el diccionario 
                # de vencimientos_y_cobros).
        else:
            cobrado += cobro.importe
        if vto != None:
            row.append(utils.str_fecha(vto.fecha))
            row.append(vto.importe)
            total_vtos += vto.importe
            row.append(esta_pendiente)
        else:
            row.append(""); row.append(0); row.append(esta_pendiente)
        if cobro != None:
            row.append(utils.str_fecha(cobro.fecha))
            row.append(cobro.importe)
            row.append(cobro.observaciones)
            if pagare == None:
                total_otros += cobro.importe
                if esta_pendiente:
                    pendiente_otros += cobro.importe
                else:
                    cobrado_otros += cobro.importe
            total_cobrado_strict += cobro.importe
        else:
            row.append(""); row.append(0); row.append("")
        if pagare != None:
            row.append(pagare.codigo)
            row.append(utils.str_fecha(pagare.fechaRecepcion))
            row.append(utils.str_fecha(pagare.fechaCobro))
            row.append(pagare.cantidad)
            row.append(0)
            total_pagares += cobro.importe
            if esta_pendiente:
                pendiente_pagares += cobro.importe
            else:
                cobrado_pagares += cobro.importe
        else:
            if pagare == None and vto != None:
                if cobro == None:   
                    # Si es != None, ya se ha sumado a total_otros arriba.
                    total_otros += vto.importe
                    pendiente_otros += vto.importe
            row.append(""); row.append(""); row.append(""); row.append(0); row.append(0)
        row.append(factura.id)
        # XXX
        idcliente = factura.clienteID
        anno = factura.fecha.year
        mes = factura.fecha.month
        try:
            padre = nodos_clientes[idcliente][anno][mes]
        except:
            if not idcliente in nodos_clientes:
                nodos_clientes[idcliente] = {}
            if not anno in nodos_clientes[idcliente]:
                nodos_clientes[idcliente][anno] = {}
            cliente = pclases.Cliente.get(idcliente)
            fila_cliente = [""] * 14
            fila_cliente[3] = 0.0
            fila_cliente[4] = False
            fila_cliente[6] = 0.0
            fila_cliente[11] = 0.0
            fila_cliente[12] = 0.0
            fila_cliente[-1] = idcliente
            fila_cliente[2] = cliente.nombre
            # DONE: Poner crédito asegurado y crédito concedido (y si eso el 
            #       disponible o algo) al lado de cada cliente.
            fila_cliente[7] = "Asegurado: %s; Concedido: %s" % (
             cliente.riesgoAsegurado!=-1 and cliente.riesgoAsegurado or "N/A", 
             cliente.riesgoConcedido!=-1 and cliente.riesgoConcedido or "N/A", 
             )
            padre = nodos_clientes[idcliente][anno][mes] = model.append(padre, 
                                                             fila_cliente)
        # XXX
        if row[0] != "" and row[1] != "":
            nodo_fra = model.append(padre, row)
        else:
            nodo_segundo_vto_o_superior = model.append(nodo_fra, row)  # @UnusedVariable
            # tv.expand_row(model.get_path(nodo_segundo_vto_o_superior), False)
        # Actualizo fila padre.
        model[nodos_clientes[idcliente][anno][mes]][3] += row[3]
        model[nodos_clientes[idcliente][anno][mes]][6] += row[6]
        model[nodos_clientes[idcliente][anno][mes]][11] += row[11]
        model[nodos_clientes[idcliente][anno][mes]][12] += row[12]
        row = ["", ""]
    if total_fra != total_vtos:
        try:
            model[nodo_fra][0] = model[nodo_fra][0].replace("(", "[").replace(")", "]")
        except UnboundLocalError:
            # La factura no tenía ni un triste vencimiento, por tanto... 
            # computer sayz no. No se ha creado el nodo_fra, así que allá voy.
            row += ["", 0, True, "", 0, "", "", "", "", 0, 0, factura.id]
            row[0] = row[0].replace("(", "[").replace(")", "]")
            nodo_fra = model.append(padre, row)
            # print total_fra, total_vtos, model[nodo_fra][0]
    return total_fra, cobrado, pendiente, total_pagares, cobrado_pagares, pendiente_pagares, total_otros, cobrado_otros, pendiente_otros, total_vtos, total_cobrado_strict
        

def generador_vcps(vtos_y_cobros):
    """
    Generador que devuelve un iterador que va retornando 
    en cada iteración un vencimiento, su cobro asociado y 
    el pagaré asociado al cobro (si lo tuviera).
    En cualquiera de las llamadas puede devolver None en 
    alguno de los tres valores devueltos para indicar que 
    la factura no cuenta con el vencimiento, cobro o pagaré.
    La iteración se detiene cuando no quedan vencimientos, 
    cobros ni pagarés (los tres serían None).
    """
    vtos = vtos_y_cobros['vtos']
    for vto in vtos:
        try:
            cobro = vtos_y_cobros[vto][0]
        except IndexError:
            cobro = None
        if cobro != None:
            pagare = cobro.pagareCobro
        else:
            pagare = None
        yield vto, cobro, pagare
    if vtos_y_cobros.has_key(None):
        for cobro in vtos_y_cobros[None]:
            pagare = cobro.pagareCobro
            yield None, cobro, pagare

class FacturacionPorClienteYFechas(Ventana):
    def __init__(self, objeto = None, usuario = None, fini = None, ffin = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'facturacion_por_cliente_y_fechas.glade', 
                         objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_imprimir/clicked': self.imprimir, 
                       'cbe_cliente/changed': self.cambiar_cliente, 
                       'b_fechaini/clicked': self.cambiar_fechaini, 
                       'b_fechafin/clicked': self.cambiar_fechafin, 
                       'b_export/clicked': self.exportar_a_csv, }
                        #'tv_facturas/row-expanded': self.expandir_subramas}  
        self.add_connections(connections)
        self.wids['tv_facturas'].connect("row-expanded", 
                                         self.expandir_subramas)
        self.inicializar_ventana()
        if fini:
            self.wids['e_fechaini'].set_text(utils.str_fecha(fini))
        if ffin:
            self.wids['e_fechafin'].set_text(utils.str_fecha(ffin))
        if objeto != None:
            utils.combo_set_from_db(self.wids['cbe_cliente'], objeto.id)
        gtk.main()

    def expandir_subramas(self, tv, itr, path):
        """
        Expande las todas subramas del itr recibido para evitar que 
        facturas con más de un vencimiento queden ocultas en un 
        primer vistazo buscando descuadres.
        """
        # Voy a expandir solo eñ último nivel, para dejar los clientes 
        # plegados (que son muchos) y dentro de éstos aparecerán las 
        # facturas de dos vencimientos (= 2 filas) con las ramas abiertas.
        # Eso se reduce a: Si soy nivel 0 no tengo que desplegar a mis hijos
        # (clientes). Si no, sí. Para clientes hará lo que buscamos: abrir 
        # todas las facturas del tirón. Para las facturas, al no tener hijos, 
        # no hará nada aunque lo intente.
        model = tv.get_model()
        if model[path].parent:
            for i in range(model.iter_n_children(itr)):
                iterhijo = model.iter_nth_child(itr, i)
                pathhijo = model.get_path(iterhijo)
                tv.expand_to_path(pathhijo)
                self.expandir_subramas(tv, iterhijo, pathhijo)

    def cambiar_fechaini(self, boton):
        """
        Cambia la fecha de inicio del rango de búsqueda.
        """
        cambiar_fecha(self.wids['e_fechaini'])
        self.rellenar_tabla_facturas()

    def cambiar_fechafin(self, boton):
        """
        Cambia la fecha de fin del rango de búsqueda.
        """
        cambiar_fecha(self.wids['e_fechafin'])
        self.rellenar_tabla_facturas()

    # --------------- Funciones auxiliares ------------------------------
    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        cols = (('Factura', 'gobject.TYPE_STRING', False, True, True, None),   
                    # Aquí sale también el total facturado en los nodos padre.
                ('Fecha', 'gobject.TYPE_STRING', False, True, False, None),
                ('Vencimiento', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Facturado', 'gobject.TYPE_FLOAT', 
                    False, True, False, None), 
                    # Aquí sale también el total de vencimientos en los nodos 
                    # padre.
                ('Pendiente', 'gobject.TYPE_BOOLEAN', 
                    False, True, False, None),
                ('Fecha cobro', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Cobrado', 'gobject.TYPE_FLOAT', 
                    False, True, False, None),  # Aquí sale también el total 
                                            # de pagarés en los nodos padre
                ('Observaciones', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Pagaré', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Fecha', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Vto. pagaré', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Importe pagaré completo', 'gobject.TYPE_FLOAT', 
                    False, True, False, None), 
                ('Total otros', 'gobject.TYPE_FLOAT', False,True,False,None),
                    # Aquí sale también el total de "otros" en los nodos 
                    # padre.
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_facturas'], cols)
        self.wids['tv_facturas'].set_expander_column(
            self.wids['tv_facturas'].get_column(2))
        self.wids['tv_facturas'].connect("row-activated", self.abrir_factura)
        self.colorear(self.wids['tv_facturas'])
        cols = (('Factura', 'gobject.TYPE_STRING', False, True, True, None),   
                    # Aquí sale también el total facturado en los nodos padre.
                ('Fecha', 'gobject.TYPE_STRING', False, True, False, None),
                ('Vencimiento', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Facturado', 'gobject.TYPE_FLOAT', 
                    False, True, False, None), 
                    # Aquí sale también el total de vencimientos en los nodos 
                    # padre.
                ('Pendiente', 'gobject.TYPE_BOOLEAN', 
                    False, True, False, None),
                ('Fecha cobro', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Cobrado', 'gobject.TYPE_FLOAT', 
                    False, True, False, None),  # Aquí sale también el total 
                                            # de pagarés en los nodos padre
                ('Observaciones', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('Pagaré', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Fecha', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Vto. pagaré', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Importe pagaré completo', 'gobject.TYPE_FLOAT', 
                    False, True, False, None), 
                ('Total otros', 'gobject.TYPE_FLOAT', False,True,False,None),
                    # Aquí sale también el total de "otros" en los nodos 
                    # padre.
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_cliente'], cols)
        self.wids['tv_cliente'].set_expander_column(
            self.wids['tv_cliente'].get_column(2))
        self.wids['tv_cliente'].connect("row-activated", self.abrir_factura)
        self.colorear(self.wids['tv_cliente'])
        cols = (("Suplemento", 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ("NIF", 'gobject.TYPE_STRING', 
                    False, True, True, None), 
                ("Código Cesce", 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ("Fecha factura", 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ("Importe", 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ("Forma de pago", 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ("Vencimiento", 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ("Número factura", 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_cesce'], cols)
        self.wids['tv_cesce'].get_column(4).get_cell_renderers()[0].set_property("xalign", 1)
        self.wids['tv_cesce'].connect("row-activated", self.abrir_factura)
        hoy = mx.DateTime.localtime()
        fini = mx.DateTime.DateTimeFrom(day = 1, 
                                        month = hoy.month, 
                                        year = hoy.year)
        self.wids['e_fechaini'].set_text(utils.str_fecha(fini))
        self.wids['e_fechafin'].set_text(utils.str_fecha(hoy))
        lista_clientes = [(c.id, c.nombre) for c 
                          in pclases.Cliente.select(orderBy="nombre")]
        lista_clientes.insert(0, (0, "Todos los clientes"))
        utils.rellenar_lista(self.wids['cbe_cliente'], 
                             lista_clientes)
        def iter_cliente_seleccionado(completion, model, itr):
            idcliente = model[itr][0]
            utils.combo_set_from_db(self.wids['cbe_cliente'], idcliente)
        self.wids['cbe_cliente'].child.get_completion().connect(
            'match-selected', iter_cliente_seleccionado)
        for w in ("total", "pendiente", "cobrado", "total_pagares", 
                  "pendiente_pagares", "cobrado_pagares", "total_otros", 
                  "pendiente_otros", "cobrado_otros", "cobrado_strict"):
            self.wids['e_%s' % w].set_alignment(1.0)
        self.wids['cbe_cliente'].grab_focus()
        # Este entry fue un intento de detectar un posible descuadre. Ya no 
        # tiene sentido, pero conservo los cálculos por si pasa otra vez, 
        # comentar y ver en ventana la suma de los registros cobro.
        self.wids['e_cobrado_strict'].set_property("visible", False)
        self.wids['label1'].set_property("visible", False)
        # Combo para incluir prefacturas.
        self.wids['ch_prefacturas'] = gtk.CheckButton("Incluir prefacturas")
        self.wids['ch_prefacturas'].set_active(False)
        self.wids['e_fechaini'].parent.add(self.wids['ch_prefacturas'])
        if pclases.Prefactura.select().count():
            self.wids['e_fechaini'].parent.show_all()
        
    def colorear(self, tv):
        """
        Asocia una función al treeview para resaltar los vencimientos 
        del mismo pagaré.
        """
        def cell_func(column, cell, model, itr, numcol):
            """
            Si la fila corresponde a una factura cobrada en un pagaré, colorea la 
            fila completa con un color generado a partir del número de pagaré.
            """
            if "[" in model[itr][0] and "]" in model[itr][0] and numcol == 0:
                cell.set_property("cell-background", "red")
            else:
                color = gtk.gdk.color_parse("white")
                numpagare = model[itr][8]
                if numpagare:
                    color = generar_color(numpagare)
                cell.set_property("cell-background-gdk", color)
                utils.redondear_flotante_en_cell_cuando_sea_posible(column, 
                                                                    cell, 
                                                                    model, 
                                                                    itr, 
                                                                    numcol)

        cols = tv.get_columns()
        for i in xrange(len(cols)):
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell, cell_func, i)

    def leer_fechas(self):
        """
        Devuelve las fechas escritas en los widgets o None si se 
        produce algún error.
        """
        fechaini = fechafin = None
        try:
            fechaini = utils.parse_fecha(self.wids['e_fechaini'].get_text())
        except (mx.DateTime.RangeError, ValueError), excepcion:
            utils.dialogo_info(titulo = "ERROR FECHA INICIO", 
                               texto = "Compruebe la fecha inicial\n\n\nDEBUG: %s" % (excepcion), 
                               padre = self.wids['ventana'])
        if fechaini:
            try:
                fechafin = utils.parse_fecha(self.wids['e_fechafin'].get_text())
            except (mx.DateTime.RangeError, ValueError), excepcion:
                utils.dialogo_info(titulo = "ERROR FECHA FIN", 
                                   texto = "Compruebe la fecha final\n\n\nDEBUG: %s" % (excepcion), 
                                   padre = self.wids['ventana'])
        return fechaini, fechafin

    def rellenar_tabla_facturas(self):
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        idcliente = utils.combo_get_value(self.wids['cbe_cliente'])
        fechaini, fechafin = self.leer_fechas()
        if idcliente >= 0 and fechaini and fechafin:
            model = self.wids['tv_facturas'].get_model()
            model.clear()
            
            total = total_vencimientos = pendiente = cobrado = 0.0
            total_pagares = pendiente_pagares = cobrado_pagares = 0.0
            total_otros = pendiente_otros = cobrado_otros = 0.0
            total_cobrado_strict = 0.0
            subtotal = {}   # (Sub)totales de FACTURACIÓN (no vencimientos, 
                            # sino suma de totales de factura) por mes.
            nodos_clientes = {}     # Diccionario con 
                                    # "ID[anno][mes]: nodo del TreeView"
                                    # Para ir insertando las facturas de cada 
                                    # cliente en su rama.
            if idcliente == 0:
                idscliente = [c.id for c in pclases.Cliente.select()]
            else:
                idscliente = [idcliente]
            i = 0.0
            for idcliente in idscliente:
                i += 1
                vpro.set_valor(i / len(idscliente), 
                               "%d %%" % (i / len(idscliente) * 100))
                (total, pendiente, cobrado, total_pagares, pendiente_pagares, 
                 cobrado_pagares, total_otros, pendiente_otros, 
                 cobrado_otros, total_vencimientos, 
                 total_cobrado_strict)=self.procesar_cliente(idcliente, total, 
                                            pendiente, cobrado, total_pagares, 
                                            pendiente_pagares, cobrado_pagares, 
                                            total_otros, pendiente_otros, 
                                            cobrado_otros, total_vencimientos, 
                                            total_cobrado_strict, model, 
                                            fechaini, fechafin, subtotal, 
                                            nodos_clientes)
            vpro.set_valor("100 %")
            self.rellenar_pies(total, pendiente, cobrado, total_pagares, 
                               pendiente_pagares, cobrado_pagares, 
                               total_otros, pendiente_otros, cobrado_otros, 
                               total_vencimientos, total_cobrado_strict)
            # XXX 
            vpro.set_valor("Creando agrupaciones...")
            self.invertir_agrupaciones_cliente_fechas()
        vpro.ocultar()

    def invertir_agrupaciones_cliente_fechas(self):
        """
        Recoge todos los datos del model por mes y año y los agrupa por 
        cliente y mes/año (justo al contrario que en el model original).
        """
        nodos_clientes = {}
        modelfechas = self.wids['tv_facturas'].get_model()
        model = self.wids['tv_cliente'].get_model()
        model.clear()
        for fila_mes_anno in modelfechas:
            fecha = fila_mes_anno[1]  # @UnusedVariable
            # Inserto el cliente en el otro model, y si existe actualizo 
            # cantidades.
            for fila_cliente in fila_mes_anno.iterchildren():
                #print fila_cliente[2], fila_cliente[-1]
                if fila_cliente[0].strip() == "":
                    ide = fila_cliente[-1]
                    if ide not in nodos_clientes:
                        itercliente = model.append(None, fila_cliente)
                        nodos_clientes[ide] = itercliente
                    else:
                        itercliente = nodos_clientes[ide]
                        row = model[itercliente]
                        for ncol in (3, 6, 11, 12):
                            row[ncol] += fila_cliente[ncol]
                else:  # ES UN NODO DE FACTURA INCORRECTA SUELTO (celdas rojas)
                    itercliente = model.append(None, fila_cliente)
                # Ahora inserto la fila de fecha como hijo, pero tengo que 
                # ponerle las cantidades solo del cliente donde lo inserto. 
                # Que no son ni más ni menos que las que tiene la fila_cliente 
                # original.
                padre = itercliente
                iterfecha = model.append(padre, fila_mes_anno)
                model[iterfecha][0] = "0.0"    # Reinicio el total de facturas.
                for ncol in (3, 6, 11, 12):
                    model[iterfecha][ncol] = fila_cliente[ncol]
                # Y ahora cuelgo las facturas de la fila de fecha.
                for fila_factura in fila_cliente.iterchildren():
                    iterfactura = model.append(iterfecha, fila_factura)
                    try:
                        totalfacturas = utils.parse_euro(
                                          rex_importe_fras.findall(
                                            fila_factura[0])[0][1:-1])
                    except (IndexError, TypeError, ValueError):
                        totalfacturas = 0.0
                        print fila_factura[0]
                    totalfacturas += utils.parse_euro(model[iterfecha][0])
                    model[iterfecha][0] = "%s €" % (
                        utils.float2str(totalfacturas))
                    # Y si por casualidad tiene varios vencimientos:
                    for fila_vencimientos in fila_factura.iterchildren():
                        model.append(iterfactura, fila_vencimientos)
            

    def procesar_cliente(self, idcliente, total,  
                               pendiente, cobrado, total_pagares, 
                               pendiente_pagares, cobrado_pagares, 
                               total_otros, pendiente_otros, 
                               cobrado_otros, total_vencimientos, 
                               total_cobrado_strict, model, fechaini, 
                               fechafin, subtotal, nodos_clientes):
        """
        Procesa los datos de facturas, prefacturas y abonos del cliente 
        recibido y actualiza los totales y el model.
        """
        F = pclases.FacturaVenta
        facturas = F.select(pclases.AND(F.q.clienteID == idcliente, 
                                        F.q.fecha >= fechaini, 
                                        F.q.fecha <= fechafin), 
                            orderBy = "fecha")
        F = pclases.Prefactura
        prefacturas = F.select(pclases.AND(F.q.clienteID == idcliente, 
                                           F.q.fecha >= fechaini, 
                                           F.q.fecha <= fechafin), 
                               orderBy = "fecha")
        for f in facturas:
            total, pendiente, cobrado, \
            total_pagares, pendiente_pagares, cobrado_pagares, \
            total_otros, pendiente_otros, cobrado_otros, \
            total_vencimientos, \
            total_cobrado_strict = self.procesar_factura(
                f, model, subtotal, total, pendiente, cobrado, 
                total_pagares, pendiente_pagares, cobrado_pagares, 
                total_otros, pendiente_otros, cobrado_otros, 
                total_vencimientos, total_cobrado_strict, nodos_clientes)
        if self.wids['ch_prefacturas'].get_active():
            for f in prefacturas:
                total, pendiente, cobrado, \
                total_pagares, pendiente_pagares, cobrado_pagares, \
                total_otros, pendiente_otros, cobrado_otros, \
                total_vencimientos, \
                total_cobrado_strict = self.procesar_factura(
                    f, model, subtotal, total, pendiente, cobrado, 
                    total_pagares, pendiente_pagares, cobrado_pagares, 
                    total_otros, pendiente_otros, cobrado_otros, 
                    total_vencimientos, total_cobrado_strict, nodos_clientes)
        
        FA = pclases.FacturaDeAbono
        frabonos = FA.select(pclases.AND(FA.q.fecha >= fechaini, 
                                         FA.q.fecha <= fechafin), 
                             orderBy = "fecha")
        frabonos = [fa for fa in frabonos 
                    if fa.abono 
                        and fa.abono.clienteID == idcliente 
                        and not fa.abono.facturasVenta]
                        #and not [pda.facturaVenta 
                        #         for pda in fa.pagosDeAbono
                        #         if pda.facturaVenta]]
        # Si el abono se ha descontado de una factura de venta, no lo 
        # muestro porque ya forma parte del total de la factura de venta.
        for f in frabonos:
            total, pendiente, cobrado, \
            total_pagares, pendiente_pagares, cobrado_pagares, \
            total_otros, pendiente_otros, cobrado_otros, \
            total_vencimientos, \
            total_cobrado_strict = self.procesar_factura(
                f, model, subtotal, total, pendiente, cobrado, 
                total_pagares, pendiente_pagares, cobrado_pagares, 
                total_otros, pendiente_otros, cobrado_otros, 
                total_vencimientos, total_cobrado_strict, nodos_clientes)
        return (total, pendiente, cobrado, total_pagares, pendiente_pagares, 
                cobrado_pagares, total_otros, pendiente_otros, 
                cobrado_otros, total_vencimientos, 
                total_cobrado_strict)

    def procesar_factura(self, f, model, subtotal, total, pendiente, cobrado, 
                         total_pagares, pendiente_pagares, cobrado_pagares, 
                         total_otros, pendiente_otros, cobrado_otros, 
                         total_vencimientos, total_cobrado_strict, 
                         nodos_clientes):
        # Nueva consulta CESCE (jpedrero)
        if f.cliente.riesgoAsegurado != -1:
            modelcesce = self.wids['tv_cesce'].get_model()
            fdp = None
            for v in f.vencimientosCobro:
                modelcesce.append(("", 
                                   f.cliente.cif, 
                                   "", 
                                   utils.str_fecha(f.fecha), 
                                   utils.float2str(v.importe), 
                                   v.observaciones, 
                                   utils.str_fecha(v.fecha), 
                                   f.numfactura, 
                                   f.id))
        # Los otros dos TreeViews, más complejos:
        fecha = f.fecha
        mes = utils.corregir_nombres_fecha(fecha.strftime("%B '%y"))
        primero_mes = mx.DateTime.DateTimeFrom(day = 1, 
                                               month = fecha.month, 
                                               year = fecha.year)
        try:
            rowpadre = [r for r in model if r[2] == mes][0]
            padre = rowpadre.iter
        except IndexError:
            padre = model.append(None, ("", utils.str_fecha(primero_mes), 
                                        mes, 0.0, False, "", 0, "", "", "", 
                                        "", 0, 0, 0))
            subtotal[mes] = 0

        tf, cf, pf, tp, cp, pp, to, co, po, tv, tcs = agregar_a_model(
                                                    model, f, padre, 
                                                    self.wids['tv_facturas'], 
                                                    nodos_clientes)
        subtotal[mes] += tf
        total += tf
        pendiente += pf
        cobrado += cf
        total_pagares += tp
        pendiente_pagares += pp
        cobrado_pagares += cp
        total_otros += to
        pendiente_otros += po
        cobrado_otros += co
        total_vencimientos += tv    # No tiene por qué coincidir con el 
                    # total facturado, ya que puede haber facturas sin 
                    # vencimientos creados (no es lo normal, pero es lo 
                    # que se ha estado usando para facturas antiguas que 
                    # no deben aparecer como pendientes de cobro con 
                    # vencimientos pendientes de cobrar).
        total_cobrado_strict += tcs
        
        model[padre][0] = "%s €" % (utils.float2str(subtotal[mes]))     
            # Total facturado (con o sin vencimientos)
        model[padre][3] += tv
            # Total vencimientos.
        #model[padre][6] += tp                                           
            # Total en pagarés (vencidos o no)
        model[padre][6] += tcs
            # Total cobrado estricto (importe de los cobros, incluyendo
            # pagarés, vencidos o no, y pendientes o no; cheques, otros, etc.
        model[padre][12] += to
            # Total otros (cobrado o no)
        return (total, pendiente, cobrado, total_pagares, pendiente_pagares, 
                cobrado_pagares, total_otros, pendiente_otros, cobrado_otros, 
                total_vencimientos, total_cobrado_strict)

    def rellenar_pies(self, 
                      total, pendiente, cobrado, 
                      total_pagares, pendiente_pagares, cobrado_pagares, 
                      total_otros, pendiente_otros, cobrado_otros, 
                      total_vencimientos, cobrado_strict):
        """
        Rellena los entries del pie del formulario con los totales recibidos.
        CWT: Al pendiente de cobro hay que restarle lo negociado en pagaré, 
        aunque no hayan vencido o estén marcados como pendiente.
        Por tanto, el 
        pendiente = total (facturado) - total_pagares - cobrado_otros
        y (lo mismo pero jugando con las incóginitas) el 
        cobrado = total_pagares + cobrado_otros = total - pendiente
        """
        self.wids['e_total'].set_text("%s €" % utils.float2str(total))
        # self.wids['e_pendiente'].set_text("%s €" % utils.float2str(pendiente))
        self.wids['e_pendiente'].set_text("%s €" % utils.float2str(total_vencimientos - total_pagares - cobrado_otros))
        self.wids['e_cobrado_strict'].set_text("%s €" % utils.float2str(cobrado_strict))
        # self.wids['e_cobrado'].set_text("%s €" % utils.float2str(cobrado))
        self.wids['e_cobrado'].set_text("%s €" % utils.float2str(total_pagares + cobrado_otros))
        self.wids['e_total_pagares'].set_text("%s €" % utils.float2str(total_pagares))
        self.wids['e_pendiente_pagares'].set_text("%s €" % utils.float2str(pendiente_pagares))
        self.wids['e_cobrado_pagares'].set_text("%s €" % utils.float2str(cobrado_pagares))
        self.wids['e_total_otros'].set_text("%s €" % utils.float2str(total_otros))
        self.wids['e_pendiente_otros'].set_text("%s €" % utils.float2str(pendiente_otros))
        self.wids['e_cobrado_otros'].set_text("%s €" % utils.float2str(cobrado_otros))

    
    # --------------- Manejadores de eventos ----------------------------

    def cambiar_cliente(self, cb):
        self.rellenar_tabla_facturas()

    def abrir_factura(self, tv, path, view_column):
        model = tv.get_model()
        idfactura = model[path][-1]
        if idfactura > 0 and (model[path][0] != "" or tv.name == "tv_cesce"):
            if model[path][0].startswith("A"):    # Es una factura de abono
                frabono = pclases.FacturaDeAbono.get(idfactura)
                if frabono.abono:
                    from formularios import abonos_venta
                    v = abonos_venta.AbonosVenta(frabono.abono, usuario = self.usuario)  # @UnusedVariable
            elif model[path][0].startswith("*"):
                fra = pclases.Prefactura.get(idfactura)
                from formularios import prefacturas
                ventana = prefacturas.Prefacturas(fra, self.usuario)  # @UnusedVariable
            else:
                fra = pclases.FacturaVenta.get(idfactura)
                from formularios import facturas_venta
                ventana = facturas_venta.FacturasVenta(fra, self.usuario)  # @UnusedVariable
        elif idfactura > 0 and model[path][0] == "":    # Es cliente.
            cliente = pclases.Cliente.get(idfactura)
            from formularios import clientes
            ventana_clientes = clientes.Clientes(cliente, self.usuario)  # @UnusedVariable


    def imprimir(self, boton):
        """
        Vuelca el contenido del TreeView a un PDF.
        """
        #utils.dialogo_info(titulo = "NO IMPLEMENTADO", 
        #                   texto = "Computer says no. Atjo.", 
        #                   padre = self.wids['ventana'])
        if self.wids['notebook1'].get_current_page() == 0:
            tv = self.wids['tv_facturas']
        elif self.wids['notebook1'].get_current_page() == 1:
            tv = self.wids['tv_cliente']
        elif self.wids['notebook1'].get_current_page() == 2:
            tv = self.wids['tv_cesce']
            abrir_pdf(treeview2pdf(tv, 
                titulo = "Facturas de clientes con crédito concedido"))
            return
        else:
            return
        model = tv.get_model()
        datos = []
        for row in model:
            datos.append((row[2], "", "", "", "", "", "", "", ""))
            for h in row.iterchildren():
                datos.append((h[0], h[1], h[2], utils.float2str(h[3]), h[5], utils.float2str(h[6]), h[8], h[9], h[10]))
                for h2 in h.iterchildren():
                    datos.append((h2[0], h2[1], h2[2], utils.float2str(h2[3]), h2[5], utils.float2str(h2[6]), h2[8], h2[9], h2[10]))
                datos.append(("---", "---", "---", "---", "---", "---", "---", "---", "---"))
            datos.append((("Totales %s" % row[2]).upper(), "---", "---", utils.float2str(row[3]), "---", utils.float2str(row[6]), "---", "---", "---"))
            datos.append(("", ) * 9)
        datos.append(("===", ) * 9)
        datos.append(("Total facturado:", self.wids['e_total'].get_text(), "", "", "", "", "", "", ""))
        datos.append(("    Vtos. pendientes:", self.wids['e_pendiente'].get_text(), "", "", "", "", "", "", ""))
        datos.append(("    Total cobrado o negociado:", self.wids['e_cobrado'].get_text(), "", "", "", "", "", "", ""))
        datos.append(("", ) * 9)
        datos.append(("Total pagarés:", self.wids['e_total_pagares'].get_text(), "", "", "", "", "", "", ""))
        datos.append(("    No vencidos o pendientes:", self.wids['e_pendiente_pagares'].get_text(), "", "", "", "", "", "", ""))
        datos.append(("    Cobrado:", self.wids['e_cobrado_pagares'].get_text(), "", "", "", "", "", "", ""))
        datos.append(("", ) * 9)
        datos.append(("Total vtos. no cubiertos por pagaré:", self.wids['e_total_otros'].get_text(), "", "", "", "", "", "", ""))
        datos.append(("    Pendiente:", self.wids['e_pendiente_otros'].get_text(), "", "", "", "", "", "", ""))
        datos.append(("    Cobrado:", self.wids['e_cobrado_otros'].get_text(), "", "", "", "", "", "", ""))
        cliente = self.wids['cbe_cliente'].child.get_text()
        abrir_pdf(geninformes.facturacion_por_cliente_y_fechas("Facturación %s" % cliente, self.wids['e_fechaini'].get_text(), self.wids['e_fechafin'].get_text(), datos))

    def exportar_a_csv(self, boton):
        """
        Exporta el TreeView a CSV.
        """
        if self.wids['notebook1'].get_current_page() == 0:
            tv = self.wids['tv_facturas']
        elif self.wids['notebook1'].get_current_page() == 1:
            tv = self.wids['tv_cliente']
        elif self.wids['notebook1'].get_current_page() == 2:
            tv = self.wids['tv_cesce']
        else:
            return
        abrir_csv(treeview2csv(tv))


if __name__ == '__main__':
    t = FacturacionPorClienteYFechas()

