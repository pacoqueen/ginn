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
## consulta_pagos_realizados.py - Vencimientos pagados por fecha.
###################################################################
## Changelog:
## 22 de noviembre de 2011 - > Inicio
## 
###################################################################
from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk, time
from framework import pclases
import mx.DateTime
from informes import geninformes
from ventana_progreso import VentanaProgreso, VentanaActividad

COLORES = {'otras': 'gray', 
           'en_pagares': 'IndianRed', 
           'en_recibos': 'LightBlue', 
           'en_transf': 'PaleGreen'}

class ConsultaVencimientosPagados(Ventana):
    inicio = None
    fin = None
    resultado = []

    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        global fin
        Ventana.__init__(self, 'consulta_pagos_realizados.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       'b_csv/clicked': self.exportar, 
                       'ch_formapago/toggled': lambda ch: 
                    self.wids['cb_formapago'].set_sensitive(ch.get_active()), 
                       }
        self.wids['cb_formapago'].set_sensitive(
            self.wids['ch_formapago'].get_active())
        formaspago = [p.documentodepago.strip().split(" ")[0] 
                      for p in pclases.Proveedor.select()]
        formaspago = filtrar_tildes_lista(formaspago)
        formaspago = [e.lower() for e in formaspago]
        formaspago = utils.unificar(formaspago)
        formaspago.sort()
        self.formaspago = zip(range(len(formaspago)), formaspago)
        utils.rellenar_lista(self.wids['cb_formapago'], self.formaspago)
        self.add_connections(connections)
        utils.rellenar_lista(self.wids['cmbe_proveedor'], 
                             [(c.id, c.nombre) for c in 
                                pclases.Proveedor.select(orderBy='nombre')])

        cols = (('Factura', 'gobject.TYPE_STRING', False, True, False, None),
                ('Fecha fra.', 'gobject.TYPE_STRING', False, True, False, None),
                ('Importe', 'gobject.TYPE_STRING', False, False, False, None),
                ('Proveedor', 'gobject.TYPE_STRING', False, True, True, None),
                ('Observaciones/Forma de pago', 'gobject.TYPE_STRING',
                    False, True, False, None),
                ('Emisión pago', 'gobject.TYPE_STRING', 
                    False, True, True, None),
                ('Vencimiento fra.', 'gobject.TYPE_STRING', 
                    False, True, True, None),
                ('Vencimiento pago', 'gobject.TYPE_STRING', 
                    False, True, True, None),
                ('id', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(self.wids['tv_datos'], cols)
        self.wids['tv_datos'].get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        self.wids['tv_datos'].connect("row-activated", self.abrir_factura)
        col = self.wids['tv_datos'].get_column(2)
        for cell in col.get_cell_renderers():
            cell.set_property("xalign", 1)
        cols = (('Año y mes','gobject.TYPE_STRING', False,True, True, None),
                ('Total','gobject.TYPE_STRING', False, True, False, None),
                ('nada','gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_totales'], cols)
        col = self.wids['tv_totales'].get_column(1)
        for cell in col.get_cell_renderers():
            cell.set_property("xalign", 1)
        temp = time.localtime()
        self.fin = mx.DateTime.DateTimeFrom(day = temp[2], 
                                            month = temp[1], 
                                            year = temp[0])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.wids['ventana'].set_title("Consulta de pagos realizados")
        # O migro de una vez a GTK3 o... o no sé. Pero no puedo seguir 
        # sin el diseñador de interfaces glade. Es un coñazo hacerlo por 
        # código. Aquí van los totales:
        self.crear_tabla_totales()
        self.wids['ch_pendientes'].set_property("visible", False)
        self.colorear(self.wids['tv_datos'])
        gtk.main()

    def crear_tabla_totales(self):
        """
        Añade un gtk.Table con todos los totales por forma de pago.
        """
        hbox = self.wids['e_total'].parent
        vbox = hbox.parent
        tabla = gtk.Table(rows = 5, columns = 2)
        l_en_pagares = gtk.Label("En pagarés ")
        l_en_transf = gtk.Label("En transferencia ")
        l_en_recibos = gtk.Label("En recibos ")
        l_otras = gtk.Label("Otras formas de pago ")
        l_total = gtk.Label("Total periodo ")
        tabla.attach(l_en_pagares, 0, 1, 0, 1)
        tabla.attach(l_en_transf,  0, 1, 1, 2)
        tabla.attach(l_en_recibos, 0, 1, 2, 3)
        tabla.attach(l_otras,      0, 1, 3, 4)
        tabla.attach(l_total,      0, 1, 4, 5)
        self.wids['e_en_pagares'] = e_en_pagares = gtk.Entry()
        self.wids['e_en_transf'] = e_en_transf = gtk.Entry()
        self.wids['e_en_recibos'] = e_en_recibos = gtk.Entry()
        self.wids['e_otras'] = e_otras = gtk.Entry()
        e_total = self.wids['e_total']
        hbox.remove(self.wids['e_total'])
        hbox.add(tabla)
        for e in (e_en_pagares, e_en_transf, e_en_recibos, e_otras, e_total):
            e.set_property("editable", False)
            e.set_property("xalign", 1)
            e.set_property("has-frame", False)
        tabla.attach(e_en_pagares, 1, 2, 0, 1)
        tabla.attach(e_en_transf,  1, 2, 1, 2)
        tabla.attach(e_en_recibos, 1, 2, 2, 3)
        tabla.attach(e_otras,      1, 2, 3, 4)
        tabla.attach(e_total,      1, 2, 4, 5)
        self.wids['label5'].set_text("Totales por forma de pago: ")
        # Coloreo los totales para mejor identificación:
        for tipo in COLORES:
            wid = self.wids['e_' + tipo]
            color = wid.get_colormap().alloc_color(COLORES[tipo])
            wid.modify_base(gtk.STATE_NORMAL, color)
        vbox.show_all()

    def abrir_factura(self, tv, path, view_column):
        model = tv.get_model()
        idpago = model[path][-1]
        pago = pclases.Pago.get(idpago)
        if pago.facturaCompra:
            from formularios import facturas_compra          
            ventanafacturas = facturas_compra.FacturasDeEntrada(  # @UnusedVariable
                                pago.facturaCompra, 
                                usuario = self.usuario)
        else:   # ¿Cómo han metido este pago? ¿Es de LOGIC o algo?
            utils.dialogo_info(titulo = "FACTURA NO DISPONIBLE", 
                texto = "No hay factura de compra asociada a este pago.", 
                padre = self.wids['ventana'])
 
    def colorear(self, tv):
        def cell_func_vto_bueno(col, cell, model, itr):
            ide = model[itr][-1]
            try:
                tipo = self.tipo_pago[ide]
            except KeyError:
                tipo = guess_keyformapago(pclases.Pago.get(ide))
            color = COLORES[tipo]
            cell.set_property("cell-background", color)
        col = tv.get_column(4)
        cells = col.get_cell_renderers()
        for cell in cells:
            col.set_cell_data_func(cell, cell_func_vto_bueno)

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, items):
        """
        Rellena el model con los items de la consulta
        """        
        numpagos = len(items)
        vpro = VentanaActividad(padre = self.wids['ventana'], 
                texto = "Mostrando datos de %d pagos realizados..." % numpagos)
        vpro.mostrar()
        model = self.wids['tv_datos'].get_model()
        model.clear()
        total = 0
        vencido = 0  # @UnusedVariable
        hoy = mx.DateTime.localtime()  # @UnusedVariable
        por_fecha = {}
        por_formapago = {'en_pagares': 0.0, 
                         'en_transf': 0.0, 
                         'en_recibos': 0.0, 
                         'otras': 0.0}
        self.tipo_pago = {}
        for pago in items:
            vpro.mover()
            importe = pago.importe
            anno = pago.fecha.year
            mes = pago.fecha.month
            total += pago.importe 
            fra = pago.facturaCompra
            # Busco a qué vencimiento corresponde un pago:
            vto = None
            try:
                dvtos = fra.emparejar_vencimientos()
            except AttributeError:  # Sin factura.
                dvtos = []
            for vtokey in dvtos:
                if isinstance(vtokey, str):
                    continue    # Hay una lista de cobros y vencimientos
                        # además de la lista de pagos por vencimiento y demás.
                        # Eso me lo salto porque son solo listas de todo que 
                        # no emparejan realmente los vtos. con los cobros.
                if pago in dvtos[vtokey]:
                    vto = vtokey
                    break
            txt_formapago = get_txtformapago(pago, vto)
            txt_fecha = get_txtfecha(pago, vto)
            txt_fechavtopago = get_txtfechavtopago(pago)
            txt_fecha_emision = utils.str_fecha(pago.get_fecha_emision())
            model.append((fra and fra.numfactura or "",
                          fra and utils.str_fecha(fra.fecha) or "",
                          utils.float2str(pago.importe),
                          fra and fra.proveedor.nombre or "",
                          txt_formapago, 
                          txt_fecha_emision, 
                          txt_fecha, 
                          txt_fechavtopago, 
                          pago.id))
            if anno not in por_fecha:
                por_fecha[anno] = {}
            if mes not in por_fecha[anno]:
                por_fecha[anno][mes] = 0.0
            por_fecha[anno][mes] += importe
            key_formapago = guess_keyformapago(pago)
            por_formapago[key_formapago] += importe
            self.tipo_pago[pago.id] = key_formapago
        self.wids['e_total'].set_text("%s €" % utils.float2str(total))
        # Relleno el model de totales.
        annos = por_fecha.keys()
        annos.sort()
        model = self.wids['tv_totales'].get_model()
        model.clear()
        for anno in annos:
            vpro.mover()
            total_anno = sum([por_fecha[anno][mes] for mes in por_fecha[anno]])
            anno_padre = model.append(None, (`anno`, 
                                             utils.float2str(total_anno), 
                                             ""))
            meses = por_fecha[anno].keys()
            meses.sort()
            for mes in meses:
                vpro.mover()
                model.append(anno_padre,("%02d - %s" % (mes, utils.MESES[mes]),
                                         utils.float2str(por_fecha[anno][mes]),
                                         ""))
        for key_formapago in por_formapago:
            self.wids["e_" + key_formapago].set_text("%s €" % 
                utils.float2str(por_formapago[key_formapago]))
        vpro.ocultar()
        
    def set_inicio(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
        self.inicio = mx.DateTime.DateTimeFrom(year = int(temp[2]), 
                                               month = int(temp[1]), 
                                               day = (temp[0]))

    def set_fin(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.fin = mx.DateTime.DateTimeFrom(year = int(temp[2]), 
                                    month = int(temp[1]), 
                                    day = (temp[0]))

    def por_fecha(self,e1,e2):
        """
        Permite ordenar una lista de cadenas de fecha
        """
        fecha1 = e1[0]
        fecha2 = e2[0]
        if fecha1 < fecha2:
            return -1
        elif fecha1 > fecha2:
            return 1
        else:
            return 0
        
    def buscar(self,boton):
        """
        Dadas fecha de inicio y de fin, devuelve todos los vencimientos 
        no pagados al completo.
        """
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        if not self.inicio:
            pagos = pclases.Pago.select(pclases.Pago.q.fecha <= self.fin, 
                                        orderBy = "fecha")
            pagares = pclases.PagarePago.select(
                        pclases.PagarePago.q.fechaEmision <= self.fin, 
                        orderBy = "fechaEmision")
        else:
            pagos = pclases.Pago.select(pclases.AND(
                                pclases.Pago.q.fecha >= self.inicio,
                                pclases.Pago.q.fecha <= self.fin), 
                            orderBy='fecha') 
            pagares = pclases.PagarePago.select(pclases.AND(
                            pclases.PagarePago.q.fechaEmision >= self.inicio,
                            pclases.PagarePago.q.fechaEmision <= self.fin), 
                        orderBy='fechaEmision') 
        i = 0.0
        tot = pagos.count() + pagares.count()
        proveedor = None
        idproveedor = utils.combo_get_value(self.wids['cmbe_proveedor'])
        if idproveedor != None:
            idproveedor = utils.combo_get_value(self.wids['cmbe_proveedor'])
            proveedor = pclases.Proveedor.get(idproveedor)
        self.resultado = []
        filtrar_por_formapago = self.wids['ch_formapago'].get_active()
        formapago = utils.combo_get_value(self.wids['cb_formapago'])
        for pago in pagos:
            i += 1
            vpro.set_valor(i/tot, "Buscando pagos... (%d/%d)" % (i, tot))
            # Si es un pagaré, se trata en el siguiente bucle.
            if pago.pagarePago:
                continue
            if (not proveedor or 
                (proveedor and pago.facturaCompra 
                    and pago.facturaCompra.proveedor == proveedor)):
                try:
                    txtformapago = self.formaspago[formapago][1]
                except TypeError:   # formapago es None. No se está filtrando 
                                    # por forma de pago.
                    filtrar_por_formapago = False
                    self.wids['ch_formapago'].set_active(False)
                if (not filtrar_por_formapago or 
                    (txtformapago in 
                     utils.filtrar_tildes(pago.observaciones).lower())):
                    self.resultado.append(pago)
        for pagare in pagares:
            i += 1
            vpro.set_valor(i/tot, "Buscando pagos... (%d/%d)" % (i, tot))
            for pago in pagare.pagos:
                if (not proveedor or 
                    (proveedor and pago.facturaCompra 
                        and pago.facturaCompra.proveedor == proveedor)):
                    try:
                        txtformapago = self.formaspago[formapago][1]
                    except TypeError:   # formapago es None. No se está 
                                        # filtrando por forma de pago.
                        filtrar_por_formapago = False
                        self.wids['ch_formapago'].set_active(False)
                    if (not filtrar_por_formapago or 
                        (txtformapago in 
                         utils.filtrar_tildes(pago.observaciones).lower())):
                        self.resultado.append(pago)
        vpro.ocultar()
        self.rellenar_tabla(self.resultado)

    def imprimir(self,boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        from formularios import reports
        datos = []
        for pago in self.resultado:
            datos.append((pago.facturaCompra.numfactura,
                          utils.str_fecha(pago.fecha),
                          utils.float2str(pago.importe),
                          pago.observaciones,
                          pago.facturaCompra.proveedor.nombre))
        if (self.inicio) == None:            
            fechaInforme = 'Hasta '+utils.str_fecha(self.fin)
        else:
            fechaInforme = (utils.str_fecha(self.inicio) + ' - ' 
                            + utils.str_fecha(self.fin))
        if datos != []:
            model = self.wids['tv_totales'].get_model()
            datos.append(("---", )*5)
            datos.append(("TOTALES POR MES Y AÑO", ">->", ">->", ">->", ">->"))
            for fila in model:
                datos.append((fila[0], "", fila[1], "", ""))
                iter_filames = model.iter_children(fila.iter)
                while iter_filames:
                    filames = model[iter_filames]
                    datos.append(("", filames[0], filames[1], "", ""))
                    iter_filames = model.iter_next(iter_filames)
            datos.append(("---", )*5)
            datos.append(("", 
                          "Total", 
                          self.wids['e_total'].get_text(), 
                          "", 
                          ""))
            reports.abrir_pdf(geninformes.vencimientosPago(datos,fechaInforme))

    def exportar(self, boton):
        """
        Vuelva el contenido de todos los TreeViews en un solo ".csv".
        """
        tv = self.wids['tv_datos']
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        nomarchivocsv = treeview2csv(tv)
        abrir_csv(nomarchivocsv)
        nomarchivocsv = treeview2csv(self.wids['tv_totales'])
        abrir_csv(nomarchivocsv)


def filtrar_tildes_lista(lista):
    """
    Devuelve una lista con los elementos de la recibida 
    en los cuales se han sustituido las tildes por vocales
    sin tildar.
    """
    res = []
    for e in lista:
        res.append(utils.filtrar_tildes(e))
    return res

def get_txtfechavtopago(pago):
    """
    Devuelve la fecha de vencimiento del propio pago.
    """
    res = ""
    if pago and pago.fecha:
        res = utils.str_fecha(pago.fecha)
        if pago.pagarePago:
            res = utils.str_fecha(pago.pagarePago.fechaVencimiento)
    return res

def get_txtfecha(pago, vto):
    """
    Devuelve la fecha de vencimiento al que corresponde el pago. Si no hay 
    vencimiento, entonces la fecha del pago en sí. Y si no, cadena vacía.
    """
    res = ""
    if vto:
        res = utils.str_fecha(vto.fecha)
    elif pago and pago.fecha:
        res = utils.str_fecha(pago.fecha)
    return res

def get_txtformapago(pago, vto):
    """
    Devuelve la forma de pago del vencimiento. Si no hay nada en las 
    observaciones del pago -que es donde debería aparecer la forma de 
    pago que finalmente se ha usado- lo intento con el vencimiento en sí. 
    Si tampoco hubiera suerte, devuelvo la forma genérica de pago del 
    proveedor.
    """
    if pago and pago.observaciones:
        res = pago.observaciones
    elif vto and vto.observaciones:
        res = vto.observaciones
    else:
        proveedor = pago.proveedor or pago.facturaCompra.proveedor
        try:
            res = ("Forma de pago del proveedor: " 
                    + proveedor.get_texto_forma_pago())
        except AttributeError:
            res = ""
    return res

def guess_keyformapago(pago):
    """
    Dependiendo del texto recibido devuelte una forma de pago tal y como 
    espera encontrarse en un diccionario que se construye al rellenar los 
    totales de la ventana de consulta de pagos emitidos.
    """
    if pago.pagarePago:
        res = 'en_pagares'
    else:   # Es transferencia, domiciliación u otra
        obs = pago.observaciones.upper()
        # Mismo criterio que en pclases para saber si es recibo bancario.
        # (Ver 'actualizar_estado_pago_domiciliaciones')
        if "DOMICILIA" in obs or "RECIBO" in obs or "BANC" in obs:
            res = "en_recibos"
        elif "TRANSF" in obs or pago.cuentaDestino:    
            # Cuenta origen se utiliza para las 
            # domiciliaciones bancarias también. Debo usar esto como criterio 
            # para adivinar si es una transferencia. 
            # 3FN... ortogonalidad...  where are you? 
            res = 'en_transf'
            # Hay transferencias que no se emiten desde el programa, por tanto 
            # no tienen cuenta destino.
        else:
            res = 'otras'
    return res

if __name__ == '__main__':
    t = ConsultaVencimientosPagados()  

