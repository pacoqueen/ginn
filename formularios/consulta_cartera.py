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
## consulta_cartera.py - Consulta de efectos en cartera.
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 17 de diciembre de 2012 - Inicio.
###################################################################
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sqlobject
import sys
try:
    import pclases
except ImportError:
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    import pclases
import mx, mx.DateTime
try:
    import geninformes
except ImportError:
    sys.path.append('../informes')
    import geninformes
sys.path.append('.')
from ventana_progreso import VentanaProgreso
from utils import _float as float

class ConsultaCartera(Ventana):
        
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'consulta_cartera.glade', objeto, 
                usuario = self.usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_remesar/clicked': self.remesar,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       'b_buscar/clicked': self.buscar
                      }
        self.add_connections(connections)
        cols = (('Remesar', 'gobject.TYPE_BOOLEAN', True, True, True, 
                    self.marcar_remesar),
                ('Código', 'gobject.TYPE_STRING', False, True, True, None),
                ('Cliente', 'gobject.TYPE_STRING', False, True, False, None),
                ('Importe', 'gobject.TYPE_STRING', False, True, False, None),
                ('Banco', 'gobject.TYPE_STRING', False, True, False, None),
                ('Tipo', 'gobject.TYPE_STRING', False, True, False, None),
                ('Fecha recepción', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Fecha vencimiento', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('id','gobject.TYPE_STRING',False,False,False,None))
        utils.preparar_listview(self.wids['tv_datos'], cols)
        self.wids['tv_datos'].connect("row-activated", self.abrir_efecto)
        col = self.wids['tv_datos'].get_column(3)
        for cell in col.get_cell_renderers():
            cell.set_property("xalign", 1)
        temp = time.localtime()
        self.fin = None
        self.inicio = str(temp[0])+'/'+str(temp[1])+'/'+str(temp[2])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
        utils.rellenar_lista(self.wids['cbe_cliente'], 
                [(c.id, c.nombre) for c in pclases.Cliente.select(
                    pclases.Cliente.q.inhabilitado == False, 
                    orderBy = "nombre")])
        gtk.main()

    def abrir_efecto(self, tv, path, view_column):
        model = tv.get_model()
        puid = model[path][-1]
        objeto = pclases.getObjetoPUID(puid)
        if isinstance(objeto, pclases.PagareCobro):
            import pagares_cobros
            v = pagares_cobros.PagaresCobros(objeto, usuario = self.usuario)
        elif isinstance(objeto, pclases.Confirming):
            import confirmings
            v = confirmings.Confirmings(objeto, usuario = self.usuario)

    def marcar_remesar(self, cell, path):
        model = self.wids['tv_datos'].get_model()
        model[path][0] = not model[path][0]

    def chequear_cambios(self):
        pass

    def remesar(self, boton):
        model = self.wids['tv_datos'].get_model()
        a_remesar = []
        iter = model.get_iter_first()
        while iter:
            if model[iter][0]:
                a_remesar.append(pclases.getObjetoPUID(model[iter][-1]))
            iter = model.iter_next(iter)
        self.dialogo_previsualizacion(a_remesar)

    def dialogo_previsualizacion(self, a_remesar):
        def mostrar_detalle(combo, detalle):
            idbanco = utils.combo_get_value(combo)
            if idbanco:
                banco = pclases.Banco.get(idbanco)
                concentracion_actual = banco.get_concentracion_actual()
                if concentracion_actual != None:
                    str_concentracion_actual = utils.float2str(
                                                        concentracion_actual)
                else:
                    str_concentracion_actual = "N/A"
                disponible = banco.get_disponible()
                if disponible == None:
                    str_disponible = "Sin límite"
                else:
                    str_disponible = utils.float2str(disponible)
                txt = "Detalle línea descuento:\n"\
                        "\tDisponible: %s\n"\
                        "\tConcentración: %s %%\n"\
                        "\tConcentración máxima: %s %%" % (
                                str_disponible, 
                                str_concentracion_actual, 
                                banco.concentracion != None
                                    and utils.float2str(banco.concentracion)
                                    or "N/A")
                detalle.set_text(txt)
        def aceptar(boton, ventana, combo):
            banco = pclases.Banco.get(utils.combo_get_value(combo))
            remesa = pclases.Remesa(banco = banco, 
                                    fechaPrevista = None, 
                                    codigo = "", 
                                    fechaCobro = None, 
                                    aceptada = False)
            for efecto in a_remesar:
                efecto.remesa = remesa
                efecto.syncUpdate()
            ventana.destroy()
            import remesas
            remesas.Remesas(objeto = remesa, usuario = self.usuario)
        def cancelar(boton, ventana):
            ventana.destroy()
        w = gtk.Window()
        w.set_title("SELECCIONE BANCO")
        cbe = gtk.ComboBoxEntry()
        bancos = [(b.id, b.nombre) 
                  for b in pclases.Banco.select(orderBy = "nombre")]
        utils.rellenar_lista(cbe, bancos)
        detalle = gtk.Label("Detalle banco seleccionado.")
        cbe.connect("changed", mostrar_detalle, detalle)
        botonera = gtk.HBox()
        b_cancelar = gtk.Button("Cancelar")
        b_aceptar = gtk.Button("Aceptar")
        b_cancelar.connect("clicked", cancelar, w)
        b_aceptar.connect("clicked", aceptar, w, cbe)
        botonera.add(b_cancelar)
        botonera.add(b_aceptar)
        box = gtk.VBox()
        box.add(cbe)
        box.add(detalle)
        box.add(botonera)
        w.add(box)
        w.show_all()

    def rellenar_tabla(self, elementos):
    	"""
        Rellena el model con los items de la consulta.
        Elementos es un diccionario con objetos fecha como claves y 
        un diccionaro de dos elementos como valor. El segundo diccionario
        debe tener tres claves: 'pagos', 'vencimientos' y 'logic'. En cada
        una de ellas se guarda una lista de objetos de la clase correspondiente.
        """        
    	model = self.wids['tv_datos'].get_model()
    	model.clear()
        total = 0.0
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        vpro.set_valor(0.0, "Filtrando efectos... (%d/%d)" 
                % (0, elementos.count()))
        i = 0.0
        tot = elementos.count()
        clienteid = utils.combo_get_value(self.wids['cbe_cliente'])
        if clienteid:
            cliente = pclases.Cliente.get(clienteid)
        else:
            cliente = None
    	for efecto in elementos:
            i += 1
            vpro.set_valor(i / tot, "Filtrando efectos... (%d/%d)" 
                    % (i, elementos.count()))
            if cliente and efecto.cliente != cliente:
                continue
            if efecto.get_estado() == pclases.CARTERA:
                if hasattr(efecto, "aLaOrden"):
                    if efecto.aLaOrden:
                        str_a_la_orden = "Pagaré a la orden"
                    else:
                        str_a_la_orden = "Pagaré no a la orden"
                else:
                    str_a_la_orden = "Confirming"
                padre = model.append((False, 
                                      efecto.codigo, 
                                      efecto.cliente 
                                        and efecto.cliente.nombre or "", 
                                      utils.float2str(efecto.cantidad),
                                      efecto.banco and efecto.banco.nombre 
                                        or "", 
                                      str_a_la_orden, 
                                      utils.str_fecha(efecto.fechaRecepcion), 
                                      utils.str_fecha(efecto.fechaVencimiento), 
                                      efecto.puid))
                total += efecto.cantidad
        vpro.ocultar()
        self.wids['e_total'].set_text(utils.float2str(total))
        
    def set_inicio(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
        self.inicio = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])


    def set_fin(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.fin = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])

    def buscar(self,boton):
        criteriosp = [pclases.PagareCobro.q.remesaID == None]
        criteriosc = [pclases.Confirming.q.remesaID == None]
        if self.inicio:
            criteriosp.append(
                    pclases.PagareCobro.q.fechaCobro >= self.inicio)
            criteriosc.append(
                    pclases.Confirming.q.fechaCobro >= self.inicio)
        if self.fin:
            criteriosp.append(
                    pclases.PagareCobro.q.fechaCobro <= self.fin)
            criteriosc.append(
                    pclases.Confirming.q.fechaCobro <= self.fin)
        try:
            importe = float(self.wids['e_importe'].get_text())
        except (ValueError, TypeError):
            pass
        else:
            criteriosp.append(pclases.PagareCobro.q.cantidad >= importe)
            criteriosc.append(pclases.Confirming.q.cantidad >= importe)
        pagares = pclases.PagareCobro.select(pclases.AND(*criteriosp))
        confirmings = pclases.Confirming.select(pclases.AND(*criteriosc))
        elementos = pclases.SQLlist(pclases.SQLlist(pagares) 
                                    + pclases.SQLlist(confirmings))
        self.rellenar_tabla(elementos)
        

if __name__ == '__main__':
    t = ConsultaCartera()    

