#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado,                   #
#                          (pacoqueen@users.sourceforge.net)                  #
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
## consulta_facturas_sin_doc_pago.py 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
import mx.DateTime

class ConsultaFacturasSinDocumentoDePago(Ventana):

    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'consulta_facturas_sin_doc_pago.glade', 
                         objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_exportar/clicked': self.exportar, 
                       'b_fechaini/clicked': self.set_fecha_ini, 
                       'b_fechafin/clicked': self.set_fecha_fin}
        self.add_connections(connections)
        cols = [('Cliente', 'gobject.TYPE_STRING', False, True, False, None),
                ('Nº. Factura', 'gobject.TYPE_STRING', False, True, True, None),
                ('Fecha', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Vencimiento', 'gobject.TYPE_STRING',False,True,False,None), 
                ("Importe pendiente", "gobject.TYPE_STRING", 
                    False, True, False, None), 
                #("Contacto", "gobject.TYPE_STRING", False, True, False, None), 
                ('idvto', 'gobject.TYPE_INT64', False, False, False, None)]
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        self.wids['tv_datos'].connect("row-activated", self.abrir_factura)
        self.wids['tv_datos'].get_column(4).get_cell_renderers()[0].set_property('xalign', 1) 
        self.wids['tv_datos'].get_column(3).get_cell_renderers()[0].set_property('xalign', 0.5) 
        #self.wids['ventana'].maximize()
        self.wids['e_fechaini'].set_text("")
        self.wids['e_fechafin'].set_text(
            utils.str_fecha(mx.DateTime.localtime()))
        gtk.main()

    def set_fecha_ini(self, boton):
        utils.set_fecha(self.wids['e_fechaini'])

    def set_fecha_fin(self, boton):
        utils.set_fecha(self.wids['e_fechafin'])

    def abrir_factura(self, tv, path, view_column):
        """
        Abre la factura a la que pertenece el vencimiento sobre el que se ha 
        hecho doble clic.
        """
        model = tv.get_model()
        ide = model[path][-1]
        if ide > 0:  # Si es negativo es un ID de cliente. No me interesa.
            fra = pclases.FacturaVenta.get(ide)
            import facturas_venta
            v = facturas_venta.FacturasVenta(fra, usuario = self.usuario)  # @UnusedVariable
        elif ide < 0:    # Ahora los ide negativos son de abonos, no clientes.
            fda = pclases.FacturaDeAbono.get(-ide)
            a = fda.abono
            import abonos_venta
            v = abonos_venta.AbonosVenta(a, usuario = self.usuario)  # @UnusedVariable

    def chequear_cambios(self):
        pass

    def buscar(self, boton):
        """
        Busca todos los productos e introduce en los TreeViews las existencias 
        de los mismos. En total y por almacén.
        El total no lo calcula, se obtiene del total global (que debería 
        coincidir con el sumatorio de...).
        """
        # DONE: Faltan los abonos por descontar.
        fechaini = self.wids['e_fechaini'].get_text().strip()
        if fechaini:
            try:
                fechaini = utils.parse_fecha(fechaini)
            except (ValueError, TypeError):
                utils.dialogo_info(titulo = "ERROR EN FECHA INICIAL", 
                 texto = "El texto «%s» no es una fecha correcta." % fechaini,
                 padre = self.wids['ventana'])
                fechaini = None
        fechafin = self.wids['e_fechafin'].get_text().strip()
        if fechafin:
            try:
                fechafin = utils.parse_fecha(fechafin)
            except (ValueError, TypeError):
                utils.dialogo_info(titulo = "ERROR EN FECHA FINAL", 
                 texto = "El texto «%s» no es una fecha correcta." % fechafin,
                 padre = self.wids['ventana'])
                fechafin = None
        if fechafin:
            FV = pclases.FacturaVenta
            VC = pclases.VencimientoCobro   # Para asegurarme de 
                                            # que tiene vencimientos.
            FDA = pclases.FacturaDeAbono
            C = pclases.Cobro  # @UnusedVariable
            if fechaini:
                facturas = FV.select(pclases.AND(
                                        FV.q.fecha >= fechaini, 
                                        FV.q.fecha <= fechafin, 
                                        VC.q.facturaVentaID == FV.q.id))
                # Busco los abonos (facturas de abono, en realidad, que no 
                # tienen por qué tener la misma fecha) que no hayan sido 
                # incluidos en facturas (porque si no el importe ya se habría 
                # contado en la factura anterior) ni en pagarés (porque 
                # entonces ya estarían en un documento de pago y por tanto 
                # no deberían aparecer en esta consulta)
                abonos = FDA.select(pclases.AND(
                    FDA.q.fecha >= fechaini, 
                    FDA.q.fecha <= fechafin))
            else:
                facturas = FV.select(pclases.AND(
                                        FV.q.fecha <= fechafin, 
                                        VC.q.facturaVentaID == FV.q.id))
                abonos = FDA.select(FDA.q.fecha <= fechafin)
            # No me queda otra que filtrar así aunque sea lento:
            abonos_pendientes = []
            for a in abonos:
                if not a.abono:
                    continue # ¿Error de borrado de un abono? Mmm... mal rollo.
                # Los abonos, por norma general, van a tener facturas de venta 
                # relacionadas. Eso no debería excluirlos de la lista de 
                # pendientes de documentar. Se comprobará cuando se filtren 
                # más adelante.
                #if a.abono.facturasVenta:
                #    continue
                if a.cobros or a.pagosDeAbono:    
                                # Cada cobro de abono está relacionado 
                                # con un pagaré (o con lo que sea en un 
                                # posible futuro, el caso es que no 
                                # estaría pendiente).
                    continue
                abonos_pendientes.append(a)
            from ventana_progreso import VentanaProgreso
            vpro = VentanaProgreso(padre = self.wids['ventana'])
            vpro.mostrar()
            txtvpro = "Buscando facturas sin documento de pago..."
            nodos_clientes = {}  # @UnusedVariable
            total = 0.0
            i = 0.0
            vpro.set_valor(i, txtvpro)
            model = self.wids['tv_datos'].get_model()
            model.clear()
            facturas_tratadas = []  # Porque la consulta duplica facturas si 
                # tienen 2 vencimientos. Triplica si 3, etc.
            for f in facturas:
                i += 1
                vpro.set_valor(i/(facturas.count() + len(abonos_pendientes)), 
                               txtvpro)
                if f in facturas_tratadas:
                    continue
                facturas_tratadas.append(f)
                # Aquí voy a hacer un segundo filtro usando la cantidad 
                # pendiente de cobro de cada factura.
                #pendiente = f.calcular_pendiente_cobro()
                pendiente = f.calcular_pendiente_de_documento_de_pago()
                pendiente = round(pendiente, 2)
                if pendiente: 
                    #cliente = f.cliente
                    #if cliente not in nodos_clientes:
                    #    nodos_clientes[cliente] = model.append(None, 
                    #        (cliente.nombre, "", "", "", "0", 
                    #         -cliente.id))
                    total += pendiente
                    fechas_vto = f.vencimientosCobro[:]
                    fechas_vto.sort(lambda v1, v2: (v1.fecha < v2.fecha and -1)
                                                or (v1.fecha > v2.fecha and 1)
                                                or 0)
                    fechas_vto = [utils.str_fecha(v.fecha) 
                                      for v in f.vencimientosCobro]
                    vtos = "; ".join(fechas_vto)
                    # CWT: Resulta que quería un listado con los contactos de 
                    # las empresas para llamarlos y que paguen, pero ahora 
                    # prefiere que no aparezcan esos contactos porque la 
                    # mayoría están mal.
                    #info_contacto = "\n".join(
                    # (f.cliente.telefono, 
                    #  f.cliente.fax, 
                    #  "\n".join(f.cliente.email.replace(",", " ").replace(";", " ").split()), 
                    #  f.cliente.contacto))
                    # CWT: Prefiere listview, se acabó agrupar por cliente.
                    #nodo_padre = nodos_clientes[f.cliente]
                    nodo_padre = None
                    model.append(nodo_padre, 
                                 #("", 
                                 (f.cliente.nombre, 
                                  f.numfactura, 
                                  utils.str_fecha(f.fecha), 
                                  vtos, 
                                  utils.float2str(pendiente), 
                                  # info_contacto, 
                                  f.id))
                    #model[nodo_padre][4] = utils.float2str(
                    #    utils._float(model[nodo_padre][4]) + pendiente)
            for a in abonos_pendientes:
                pendiente = a.calcular_importe_total()  # O está descontada 
                # entera o no lo está. Con los abonos no hay pagos parciales.
                pendiente = round(pendiente, 2)
                if pendiente: 
                    total += pendiente
                    vtos = utils.str_fecha(a.fecha)  # Tampoco tiene 
                    # vencimientos. La obligación nace desde el mismo día 
                    # en que el abono se convierte en factura de abono.
                    nodo_padre = None
                    model.append(nodo_padre, 
                                 (a.cliente.nombre, 
                                  a.numfactura, 
                                  utils.str_fecha(a.fecha), 
                                  vtos, 
                                  utils.float2str(pendiente), 
                                  -a.id)) # Para distinguirlo de las facturas. 
                i += 1
                vpro.set_valor(i/(facturas.count() + len(abonos_pendientes)), 
                               txtvpro)
            vpro.ocultar()
            self.wids['e_total'].set_text(utils.float2str(total))

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe.
        """
        from informes.treeview2pdf import treeview2pdf
        from formularios.reports import abrir_pdf
        strfecha = "%s - %s" % (
            self.wids['e_fechaini'].get_text(), 
            self.wids['e_fechafin'].get_text())
        tv = self.wids['tv_datos']
        nomarchivo = treeview2pdf(tv, 
            titulo = "Facturas sin documento de pago",
            fecha = strfecha, 
            apaisado = False)
        abrir_pdf(nomarchivo)

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        tv = self.wids['tv_datos']
        abrir_csv(treeview2csv(tv))


if __name__ == '__main__':
    t = ConsultaFacturasSinDocumentoDePago()

