#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2013  Francisco José Rodríguez Bogado                    #
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
from framework import pclases
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
                ("En remesa en preparación", "gobject.TYPE_STRING", 
                    False, True, False, None), 
                ("Observaciones", "gobject.TYPE_STRING", 
                    False, True, False, None), 
                ('puid', 'gobject.TYPE_STRING', False, False, False, None))
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
        objeto_relacionado = objeto.confirming or objeto.pagareCobro
        if isinstance(objeto_relacionado, pclases.PagareCobro):
            import pagares_cobros
            v = pagares_cobros.PagaresCobros(objeto_relacionado, 
                                             usuario = self.usuario)
        elif isinstance(objeto_relacionado, pclases.Confirming):
            import confirmings
            v = confirmings.Confirmings(objeto_relacionado, 
                                        usuario = self.usuario)

    def marcar_remesar(self, cell, path):
        model = self.wids['tv_datos'].get_model()
        model[path][0] = not model[path][0]

    def chequear_cambios(self):
        pass

    def remesar(self, boton):
        model = self.wids['tv_datos'].get_model()
        a_remesar = []
        itr = model.get_iter_first()
        while itr:
            if model[itr][0]:
                a_remesar.append(pclases.getObjetoPUID(model[itr][-1]))
            itr = model.iter_next(itr)
        todas_mismo_tipo = True
        if a_remesar:
            adan = a_remesar[0]
            if adan.confirming: # Todas confirming
                for e in a_remesar:
                    if not e.confirming:
                        todas_mismo_tipo = False
                        break
            elif adan.pagareCobro.aLaOrden:     # Todas A la orden
                for e in a_remesar:
                    if not e.pagareCobro or not e.pagareCobro.aLaOrden:
                        todas_mismo_tipo = False
                        break
            else:   # Todas no a la orden
                for e in a_remesar:
                    if not e.pagareCobro or e.pagareCobro.aLaOrden:
                        todas_mismo_tipo = False
                        break
        if todas_mismo_tipo:
            self.dialogo_previsualizacion(a_remesar)
        else:
            utils.dialogo_info(titulo = "REMESA NO PERMITIDA", 
                    texto = "Todos los efectos de la remesa deben ser"
                            " del mismo tipo.", 
                    padre = self.wids['ventana'])

    def dialogo_previsualizacion(self, a_remesar):
        def mostrar_detalle(combo, detalle):
            idbanco = utils.combo_get_value(combo)
            importe = sum([i.cantidad for i in a_remesar])
            str_importe = utils.float2str(importe)
            por, imp, cli = calcular_concentracion(a_remesar)
            if por == None:
                str_concentracion_seleccion = "-"
            else:
                str_concentracion_seleccion = "%s %% (%s €) %s" % (
                                                    utils.float2str(por * 100),
                                                    utils.float2str(imp),
                                                    cli.nombre)
            if idbanco:
                banco = pclases.Banco.get(idbanco)
                concentraciones_cliente_superadas \
                        = banco.comprobar_concentracion_clientes(a_remesar)
                if concentraciones_cliente_superadas:
                    str_concentracion_seleccion = '<span foreground="red">%s'%(
                            str_concentracion_seleccion)
                    for cliente, conc_max, conc_cliente \
                            in concentraciones_cliente_superadas:
                        str_concentracion_seleccion += \
                                "\n\t\t* Cliente %s = %s %% - Máx.: %s %%" % (
                                    cliente.nombre, 
                                    utils.float2str(conc_cliente * 100), 
                                    utils.float2str(conc_max * 100))
                    str_concentracion_seleccion += "</span>"
                concentracion_actual = banco.get_concentracion_actual()
                if concentracion_actual != None:
                    str_concentracion_actual = utils.float2str(
                                                concentracion_actual[0] * 100)
                else:
                    str_concentracion_actual = "N/A"
                disponible = banco.get_disponible()
                if disponible == None:
                    str_disponible = "Sin límite"
                else:
                    str_disponible = utils.float2str(disponible)
                    if disponible < importe:
                        str_disponible = '<span foreground="red">' + str_disponible + "</span>"
                if banco.concentracion != None:
                    concentracion_banco = (0 < banco.concentracion < 1.0 
                                             and banco.concentracion * 100 
                                             or banco.concentracion)
                    str_concentracion_banco = "%s %%" % utils.float2str(
                                                           concentracion_banco)
                    if (por != None and (por * 100.0) > concentracion_banco):
                            # Porcentaje de concentración máxima de los 
                            # efectos seleccionados.
                        str_concentracion_banco = ('<span foreground="red">' 
                            + str_concentracion_banco + '</span>')
                else:
                    str_concentracion_banco = "N/A"
                txt = "Detalle línea descuento:\n"\
                        "\tImporte seleccionado: %s\n"\
                        "\tDisponible: %s\n"\
                        "\tMáxima concentración remesa seleccionada: %s\n"\
                        "\tConcentración máxima actual en banco: %s %%\n"\
                        "\tConcentración máxima permitida: %s" % (
                                str_importe, 
                                str_disponible, 
                                str_concentracion_seleccion,
                                str_concentracion_actual, 
                                str_concentracion_banco)
                detalle.set_text(txt)
                detalle.set_use_markup(True)
        def aceptar(boton, ventana, combo):
            banco = pclases.Banco.get(utils.combo_get_value(combo))
            remesa = pclases.Remesa(banco = banco, 
                                    fechaPrevista = None, 
                                    codigo = "", 
                                    fechaCobro = None, 
                                    aceptada = False)
            for efecto in a_remesar:
                remesa.addEfecto(efecto)
                #efecto.addRemesa(remesa)
                #efecto.syncUpdate()
            efecto.syncUpdate()
            ventana.destroy()
            self.buscar()
            import remesas
            remesas.Remesas(objeto = remesa, usuario = self.usuario)
        def cancelar(boton, ventana):
            ventana.destroy()
        w = gtk.Window()
        w.set_title("SELECCIONE BANCO")
        w.set_modal(True)
        w.set_transient_for(self.wids['ventana'])
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
        total = total_obs = total_no_obs = 0.0
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
                str_a_la_orden = efecto.get_str_tipo()
                padre = model.append((False, 
                                      efecto.codigo, 
                                      efecto.cliente 
                                        and efecto.cliente.nombre or "", 
                                      utils.float2str(efecto.cantidad),
                                      efecto.cuentaBancariaCliente 
                                        and efecto.cuentaBancariaCliente.banco 
                                        or "", 
                                      str_a_la_orden, 
                                      utils.str_fecha(efecto.fechaRecepcion), 
                                      utils.str_fecha(efecto.fechaVencimiento), 
                                      ", ".join(["%s (%d)" % (r.codigo, r.id)
                                                 for r in efecto.remesas]),
                                      efecto.observaciones, 
                                      efecto.puid))
                total += efecto.cantidad
                if efecto.observaciones:
                    total_obs += efecto.cantidad
                else:
                    total_no_obs += efecto.cantidad
        vpro.ocultar()
        self.wids['e_total'].set_text(utils.float2str(total))
        self.wids['e_total_obs'].set_text(utils.float2str(total_obs))
        self.wids['e_total_no_obs'].set_text(utils.float2str(total_no_obs))
        
    def set_inicio(self, boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
        self.inicio = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])


    def set_fin(self, boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.fin = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])

    def buscar(self, boton = None):
        # Un efecto puede estar en remesa 
        # pero estar también en cartera si la remesa no tiene fecha 
        # prevista de abono (es decir, no se ha enviado al banco a su estudio).
        #criteriosp = [pclases.PagareCobro.q.remesaID == None]
        #criteriosc = [pclases.Confirming.q.remesaID == None]
        criteriosp = []
        criteriosc = []
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
        #confirmings = pclases.Confirming.select(pclases.AND(*criteriosc))
        # Los confirmings no se envían en remesas al banco. Se negocian uno a 
        # uno y por otra vía.
        confirmings = []
        # Ahora filtro para quitar los efectos que ya están confirmados.
        elementos = [] 
        for p in pagares:
            if not p.remesado and p.esta_pendiente():
                if not p.efecto:
                    pclases.Efecto(pagareCobro = p, 
                                   confirming = None, 
                                   cuentaBancariaCliente = None)
                efecto = p.efecto
                elementos.append(efecto)
        for c in confirmings:
            if not c.remesado and c.esta_pendiente():
                if not c.efecto:
                    pclases.Efecto(pagareCobro = None, 
                                   confirming = c, 
                                   cuentaBancariaCliente = None)
                efecto = c.efecto
                elementos.append(efecto)
        elementos = pclases.SQLlist(elementos)
        self.rellenar_tabla(elementos)


def calcular_concentracion(efectos):
    """
    Devuelve el porcentaje máximo de importes de los efectos de un mismo 
    cliente.
    """
    concentraciones = {}
    remesa_importe = sum([p.cantidad for p in efectos])
    for p in efectos:
        try:
            concentraciones[p.cliente][1] += p.cantidad
        except KeyError:
            concentraciones[p.cliente] = [None, p.cantidad]
    for cliente in concentraciones:
        concentraciones[cliente][0] = \
                concentraciones[cliente][1] / remesa_importe
    if concentraciones:
        cliente_maximo = max(concentraciones, 
                     key = lambda cliente: concentraciones[cliente])
        res = (concentraciones[cliente_maximo][0], 
               concentraciones[cliente_maximo][1], 
               cliente_maximo)
    else:
        res = (None, None, None)
    return res


if __name__ == '__main__':
    t = ConsultaCartera()    

