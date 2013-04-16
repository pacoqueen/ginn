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
## vencimientos_pendientes_por_cliente.py - Pues eso. 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 29 de mayo de 2006 -> Inicio
## 29 de mayo de 2006 -> Testing
## 
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
import mx.DateTime
    

class VencimientosPendientesPorCliente(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        Ventana.__init__(self, 'vencimientos_pendientes_por_cliente.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'cbe_cliente/changed': self.cambiar_cliente, 
                       'b_exportar/clicked': self.exportar}  
        self.add_connections(connections)
        self.inicializar_ventana()
        gtk.main()

    # --------------- Funciones auxiliares ------------------------------
    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        tv = self.wids['tv_cobros']
        abrir_csv(treeview2csv(tv))

    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        cols = (('Factura', 'gobject.TYPE_STRING', False, True, True, None),
                ('Fecha', 'gobject.TYPE_STRING', False, True, False, None),
                ('Fecha vencimiento', 'gobject.TYPE_STRING', False, True, False, None),
                ('Importe', 'gobject.TYPE_FLOAT', False, True, False, None),
                ('Pagaré (fecha)', 'gobject.TYPE_STRING', False, True, False, None),
                ('Fecha vto. pagaré', 'gobject.TYPE_STRING', False, True, False, None),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_cobros'], cols)
        self.wids['tv_cobros'].connect("row-activated", self.abrir_cobro)
        self.colorear(self.wids['tv_cobros'])
        clientes = [(0, "Todos los clientes")] + [(c.id, c.nombre) for c in pclases.Cliente.select(orderBy="nombre")]
        utils.rellenar_lista(self.wids['cbe_cliente'], clientes)
        def iter_cliente_seleccionado(completion, model, itr):
            idcliente = model[itr][0]
            utils.combo_set_from_db(self.wids['cbe_cliente'], idcliente)
        self.wids['cbe_cliente'].child.get_completion().connect('match-selected', iter_cliente_seleccionado)

    def colorear(self, tv):
        """
        Asocia una función al treeview para resaltar los vencimientos con 
        fecha sobrepasada.
        """
        def cell_func(column, cell, model, itr, numcol):
            """
            Comprueba si la fecha efectiva del vencimiento (la del vencimiento 
            en sí o la del pagaré, si lo tiene) es inferior a la actual y colorea
            toda la fila para resaltarla.
            La función está anidada porque no se va a usar más que aquí.
            """
            color = "blue"
            if model[itr].parent != None:
                fecha = model[itr][5]
                if not fecha:
                    fecha = model[itr][2]
                if fecha:
                    fecha = utils.parse_fecha(fecha)
                    hoy = mx.DateTime.localtime()
                    if fecha < hoy:
                        color = "red"
                    elif fecha == hoy:
                        color = "orange"
                    else:
                        color = "black"
            cell.set_property("foreground", color)
            utils.redondear_flotante_en_cell_cuando_sea_posible(column, cell, model, itr, numcol)

        cols = tv.get_columns()
        for i in (2, 5):
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell, cell_func, i)

    def rellenar_vencimientos(self):
        model = self.wids['tv_cobros'].get_model()
        model.clear()
        idcliente = utils.combo_get_value(self.wids['cbe_cliente'])
        total = 0
        vencido = 0
        if idcliente > 0:
            cliente = pclases.Cliente.get(idcliente)
            for f in cliente.facturasVenta:
                total, vencido = self.agregar_factura(f, model, total, vencido)
            for fda in buscar_facturas_de_abono_sin_pagar(cliente):
                total, vencido = self.agregar_factura_de_abono(fda, model, total, vencido)
        elif idcliente == 0:
            for cliente in pclases.Cliente.select(orderBy = "nombre"):
                for f in cliente.facturasVenta:
                    total, vencido = self.agregar_factura(f, model, total, vencido)
                for fda in buscar_facturas_de_abono_sin_pagar(cliente):
                    total, vencido = self.agregar_factura_de_abono(fda, model, total, vencido)

        self.wids['e_total'].set_text("%s €" % utils.float2str(total))
        self.wids['e_vencido'].set_text("%s €" % utils.float2str(vencido))

    def agregar_factura_de_abono(self, f, model, total, vencido):
        vtos = []
        vtos_emparejados = f.emparejar_vencimientos()
        for vto in vtos_emparejados['vtos']:
            try:
                cobro = vtos_emparejados[vto][0]
            except IndexError:
                cobro = None
            vtos.append([vto, None, cobro])
            # OJO: A diferencia que con el emparejar_vencimientos de pclases.FacturaCompra, no debería haber más de un 
            # cobro por vencimiento en los abonos ni haber cobros sin vencimientos (clave None del diccionario), ya 
            # que los vencimientos son ficticios, no se corresponden con ningún registro de la BD (es una clase "closured") 
            # y se crean sobre la marcha en la función. Como tampoco se permite asociar una misma factura de abono a más 
            # de un cobro (bien en factura o bien en pagaré), nunca habrá más de un "vencimiento" por abono.
        # XXX: Hasta aquí lo que hace el preparar_vencimientos con las facturasVenta. Ahora a agregarlo al TreeView.
        vtos = [v for v in vtos if (v[2]==None or (v[2].pagareCobro != None and v[2].pagareCobro.pendiente)) and v[0] != None]
            # Todos los que no tienen pagaré o si lo tienen, que esté pendiente
            # y los que sean realmente vencimientos (hay entradas en vtos que pueden tener v[0] a None).
        for v in vtos:
            if v[2]!=None and v[2].pagareCobro!=None:
                pagare = v[2].pagareCobro
            else:
                pagare = None
            fechavto = pagare and pagare.fechaCobro or v[0].fecha   # Fecha del vencimiento final: la del vencimiento de la factura
                                                                    # si no tiene pagaré o la del vencimiento del pagaré que cubre
                                                                    # el vencimiento de la factura.
            mes = utils.corregir_nombres_fecha(fechavto.strftime("%B '%y"))
            primero_mes = mx.DateTime.DateTimeFrom(day = 1, month = fechavto.month, year = fechavto.year)
            try:
                rowpadre = [r for r in model if r[2] == mes][0]
                padre = rowpadre.iter
            except IndexError:
                padre = model.append(None, ("", utils.str_fecha(primero_mes), mes, 0.0, "", "", 0))
            factura = v[0].get_factura_o_prefactura()
            model.append(padre, ("%s (%s)" % (factura.numfactura, factura.cliente and factura.cliente.nombre or "Sin cliente"), 
                                 utils.str_fecha(factura.fecha), 
                                 utils.str_fecha(v[0].fecha),
                                 v[0].importe,
                                 pagare and "%s (%s)" % (pagare.codigo, utils.str_fecha(pagare.fechaRecepcion)) or '',
                                 pagare and utils.str_fecha(pagare.fechaCobro) or '',
                                 pagare and pagare.id or v[0].id)
                         )
            total += v[0].importe
            model[padre][3] += v[0].importe
            if pagare:
                if pagare.fechaCobro <= mx.DateTime.localtime():
                    vencido += v[0].importe
            else:
                if v[0].fecha <= mx.DateTime.localtime():
                    vencido += v[0].importe
            # NOTA: Si la fecha del vencimiento ha vencido pero la del pagaré no, no la cuento como pendiente.
        return total, vencido

    def agregar_factura(self, f, model, total, vencido):
        vtos = self.preparar_vencimientos(f)
        vtos = [v for v in vtos if (v[2]==None or (v[2].pagareCobro != None and v[2].pagareCobro.pendiente)) and v[0] != None]
            # Todos los que no tienen pagaré o si lo tienen, que esté pendiente
            # y los que sean realmente vencimientos (hay entradas en vtos que pueden tener v[0] a None).
        for v in vtos:
            if v[2]!=None and v[2].pagareCobro!=None:
                pagare = v[2].pagareCobro
            else:
                pagare = None
            fechavto = pagare and pagare.fechaCobro or v[0].fecha   # Fecha del vencimiento final: la del vencimiento de la factura
                                                                    # si no tiene pagaré o la del vencimiento del pagaré que cubre
                                                                    # el vencimiento de la factura.
            mes = utils.corregir_nombres_fecha(fechavto.strftime("%B '%y"))
            primero_mes = mx.DateTime.DateTimeFrom(day = 1, month = fechavto.month, year = fechavto.year)
            try:
                rowpadre = [r for r in model if r[2] == mes][0]
                padre = rowpadre.iter
            except IndexError:
                padre = model.append(None, ("", utils.str_fecha(primero_mes), mes, 0.0, "", "", 0))
            factura = v[0].get_factura_o_prefactura()
            model.append(padre, ("%s (%s)" % (factura.numfactura, factura.cliente and factura.cliente.nombre or "Sin cliente"), 
                                 utils.str_fecha(factura.fecha), 
                                 utils.str_fecha(v[0].fecha),
                                 v[0].importe,
                                 pagare and "%s (%s)" % (pagare.codigo, utils.str_fecha(pagare.fechaRecepcion)) or '',
                                 pagare and utils.str_fecha(pagare.fechaCobro) or '',
                                 pagare and pagare.id or v[0].id)
                         )
            total += v[0].importe
            model[padre][3] += v[0].importe
            if pagare:
                if pagare.fechaCobro <= mx.DateTime.localtime():
                    vencido += v[0].importe
            else:
                if v[0].fecha <= mx.DateTime.localtime():
                    vencido += v[0].importe
            # NOTA: Si la fecha del vencimiento ha vencido pero la del pagaré no, no la cuento como pendiente.
        return total, vencido

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
        mas_larga = [l for l in (vtos, ests, pags) if len(l)==max(len(vtos), len(ests), len(pags))][0]
        if len(mas_larga) == 0: return []
        for i in xrange(len(mas_larga)):  # @UnusedVariable
            res.append([None, None, None])
        def comp(v1, v2):
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
        mas_larga.sort(comp)
        pos = 0
        for item in mas_larga:
            res [pos][lugar(item)] = item
            pos += 1
        for lista in resto:
            mlc = mas_larga[:]
            lista.sort(comp)
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
    
    # --------------- Manejadores de eventos ----------------------------

    def cambiar_cliente(self, cb):
        self.rellenar_vencimientos()

    def abrir_cobro(self, tv, path, view_column):
        model = tv.get_model()
        if model[path][4] != "":
            idpagare = model[path][-1]
            pagare = pclases.PagareCobro.get(idpagare)
            from formularios import pagares_cobros
            ventanapagares = pagares_cobros.PagaresCobros(pagare)  # @UnusedVariable
        else:
            idvto = model[path][-1]
            if idvto > 0:
                vto = pclases.VencimientoCobro.get(idvto)
                fra = vto.get_factura_o_prefactura()
                if isinstance(fra, pclases.FacturaVenta):
                    from formularios import facturas_venta           
                    ventanafacturas = facturas_venta.FacturasVenta(fra)  # @UnusedVariable
                elif isinstance(fra, pclases.Prefactura):
                    from formularios import prefacturas
                    ventanafacturas = prefacturas.Prefacturas(fra)  # @UnusedVariable

def buscar_facturas_de_abono_sin_pagar(cliente, 
                                       fechaini = None, 
                                       fechafin = None):
    """
    Devuelve las facturas de abono del cliente que no estén abonadas 
    ya en un pagaré o descontadas en una factura de venta y entre las 
    fechas recibidas.
    """
    FDA = pclases.FacturaDeAbono
    fdas = FDA.select(pclases.AND(pclases.Abono.q.clienteID == cliente.id, 
                                  pclases.Abono.q.facturaDeAbonoID==FDA.q.id))
    sin_abonar = []
    for fda in fdas:
        if len(fda.pagosDeAbono) == 0:
            sin_abonar.append(fda)      # Sin abonar en absoluto
        else:
            for pda in fda.pagosDeAbono:    # En teoría no debería haber más de 1. Se controla en las ventanas de facturas y pagarés.
                if pda.pendiente:   
                    # El campo pendiente parece no actualizarse correctamente 
                    # en las ventanas de facturas 
                    # y pagarés. Como por defecto es True, me aseguro de que 
                    # realmente está pendiente.
                    if pda.get_factura_o_prefactura() == None or [c for c in pda.facturaDeAbono.cobros 
                            if c.pagareCobro != None and c.pagareCobro.pendiente] != []:
                        sin_abonar.append(fda)
        if fechaini and fda.fecha < fechaini and fda in sin_abonar:
            sin_abonar.remove(fda)
        if fechafin and fda.fecha > fechafin and fda in sin_abonar:
            sin_abonar.remove(fda)
    return sin_abonar


if __name__ == '__main__':
    t = VencimientosPendientesPorCliente()

