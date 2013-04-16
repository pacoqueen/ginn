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
## trazabilidad_articulos.py - Trazabilidad de rollo, bala o bigbag
###################################################################
## NOTAS:
##  
## ----------------------------------------------------------------
##  
###################################################################
## Changelog:
## 24 de mayo de 2006 -> Inicio
## 24 de mayo de 2006 -> It's alive!
###################################################################
## DONE: Imprimir toda la información en PDF sería lo suyo.
###################################################################


from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
from informes.barcode import code39
from informes.barcode.EANBarCode import EanBarCode
from reportlab.lib.units import cm

class TrazabilidadArticulos(Ventana):
    def __init__(self, objeto = None, usuario = None):
        self.usuario = usuario
        Ventana.__init__(self, 'trazabilidad_articulos.glade', objeto, 
                         self.usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir
                      }
        self.add_connections(connections)
        #self.wids['e_num'].connect("key_press_event", self.pasar_foco)
        self.wids['ventana'].resize(800, 600)
        self.wids['ventana'].set_position(gtk.WIN_POS_CENTER)
        if objeto != None:
            self.rellenar_datos(objeto)
        self.wids['e_num'].grab_focus()
        gtk.main()

    def imprimir(self, boton):
        """
        Vuelca toda la información de pantalla en bruto a un PDF.
        """
        from formularios import reports
        from informes import geninformes
        datos = "Código de trazabilidad: %s\n\n"%self.wids['e_num'].get_text()
        for desc, txt in (("Producto:\n", self.wids['txt_producto']), 
                          ("Lote/Partida:\n", self.wids['txt_lp']), 
                          ("Albarán de salida:\n", self.wids['txt_albaran']), 
                          ("Producción:\n", self.wids['txt_produccion'])):
            buff = txt.get_buffer()
            texto = buff.get_text(buff.get_start_iter(), 
                                    buff.get_end_iter())
            datos += desc + texto + "\n\n"
        reports.abrir_pdf(geninformes.trazabilidad(datos))

    def pasar_foco(self, widget, event):
        if event.keyval == 65293 or event.keyval == 65421:
            self.wids['b_buscar'].grab_focus()

    def chequear_cambios(self):
        pass

    def buscar_bigbag(self, txt):
        ar = None
        if isinstance(txt, str):
            txt = utils.parse_numero(txt)
        ars = pclases.Bigbag.select(pclases.Bigbag.q.numbigbag == txt)
        if ars.count() == 1:
            ar = ars[0]
        elif ars.count() > 1:
            filas = [(a.id, a.numbigbag, a.codigo) for a in ars]
            idbigbag = utils.dialogo_resultado(filas, 
                        titulo = "Seleccione bigbag", 
                        cabeceras = ('ID', 'Número de bigbag', 'Código'), 
                        padre = self.wids['ventana'])
            if idbigbag > 0:
                ar = pclases.Bigbag.get(idbigbag)
        return ar

    def buscar_bala(self, txt):
        ar = None
        if isinstance(txt, str):
            txt = utils.parse_numero(txt)
        ars = pclases.Bala.select(pclases.Bala.q.numbala == txt)
        if ars.count() == 1:
            ar = ars[0]
        elif ars.count() > 1:
            filas = [(a.id, a.numbala, a.codigo) for a in ars]
            idbala = utils.dialogo_resultado(filas, 
                        titulo = "Seleccione bala", 
                        cabeceras = ('ID', 'Número de bala', 'Código'), 
                        padre = self.wids['ventana'])
            if idbala > 0:
                ar = pclases.Bala.get(idbala)
        return ar

    def buscar_rollo(self, txt):
        ar = None
        if isinstance(txt, str):
            txt = utils.parse_numero(txt)
        ars = pclases.Rollo.select(pclases.Rollo.q.numrollo == txt)
        if ars.count() == 1:
            ar = ars[0]
        elif ars.count() > 1:
            filas = [(a.id, a.numrollo, a.codigo) for a in ars]
            idrollo = utils.dialogo_resultado(filas, 
                        titulo = "Seleccione rollo", 
                        cabeceras = ('ID', 'Número de rollo', 'Código'), 
                        padre = self.wids['ventana'])
            if idrollo > 0:
                ar = pclases.Rollo.get(idrollo)
        return ar

    def buscar_articulo(self, txt):
        ar = None
        if isinstance(txt, str):
            txt = utils.parse_numero(txt)
        ars = pclases.Rollo.select(pclases.Rollo.q.numrollo == txt)
        if ars.count() == 0:
            ar = self.buscar_bala(txt)
        elif ars.count() == 1:
            ar = ars[0]
        else:
            ar = self.buscar_rollo(txt)
        return ar

    def buscar(self, b):
        a_buscar = self.wids['e_num'].get_text().strip().upper()
        if a_buscar.startswith(pclases.PREFIJO_ROLLO):
            try:
                objeto = pclases.Rollo.select(
                    pclases.Rollo.q.codigo == a_buscar)[0]
            except IndexError:
                objeto = self.buscar_rollo(a_buscar[1:])
        elif a_buscar.startswith(pclases.PREFIJO_BALA):
            try:
                objeto = pclases.Bala.select(
                    pclases.Bala.q.codigo == a_buscar)[0]
            except IndexError:
                objeto = self.buscar_bala(a_buscar[1:])
        elif a_buscar.startswith(pclases.PREFIJO_LOTECEM):
            try:
                loteCem = pclases.LoteCem.select(
                    pclases.LoteCem.q.codigo == a_buscar)[0]
            except IndexError:
                utils.dialogo_info(titulo = "LOTE NO ENCONTRADO", 
                    texto = "El lote de fibra de cemento %s no se encontró." 
                        % (a_buscar), 
                    padre = self.wids['ventana'])
                loteCem = None
            objeto = loteCem
        elif a_buscar.startswith(pclases.PREFIJO_LOTE):
            try:
                lote = pclases.Lote.select(
                    pclases.Lote.q.numlote == int(a_buscar[2:]))[0]     
            except IndexError:
                try:
                    lote = pclases.Lote.select(
                        pclases.Lote.q.codigo == a_buscar)[0]     
                except IndexError:
                    utils.dialogo_info(titulo = "LOTE NO ENCONTRADO", 
                        texto = "El lote de fibra %s no se encontró." % (
                            a_buscar), 
                        padre = self.wids['ventana'])
                    lote = None
            except ValueError:
                utils.dialogo_info(titulo = "ERROR BUSCANDO LOTE", 
                    texto = "El texto %s provocó un error en la búsqueda." % (
                        a_buscar), 
                    padre = self.wids['ventana'])
                lote = None
            objeto = lote
        elif a_buscar.startswith(pclases.PREFIJO_PARTIDA):
            try:
                partida = pclases.Partida.select(
                    pclases.Partida.q.numpartida == int(a_buscar[2:]))[0]
            except IndexError:
                try:
                    partida = pclases.Partida.select(
                        pclases.Partida.q.codigo == a_buscar)[0]
                except IndexError:
                    utils.dialogo_info(titulo = "PARTIDA NO ENCONTRADA", 
                        texto = "La partida de geotextiles %s "
                                "no se encontró." % (a_buscar), 
                        padre = self.wids['ventana'])
                    partida = None
            except ValueError:
                utils.dialogo_info(titulo = "ERROR BUSCANDO PARTIDA", 
                    texto = "El texto %s provocó un error en la búsqueda." % (
                        a_buscar), 
                    padre = self.wids['ventana'])
                partida = None
            objeto = partida
        elif a_buscar.startswith(pclases.PREFIJO_PARTIDACEM):
            try:
                partidaCem = pclases.PartidaCem.select(
                    pclases.PartidaCem.q.numpartida == int(a_buscar[2:]))[0]
            except IndexError:
                try:
                    partidaCem = pclases.PartidaCem.select(
                        pclases.PartidaCem.q.codigo == a_buscar)[0]
                except IndexError:
                    utils.dialogo_info(
                        titulo = "PARTIDA DE FIBRA EMBOLSADA NO ENCONTRADA", 
                        texto = "La partida de fibra embolsada %s "
                                "no se encontró." % (a_buscar), 
                        padre = self.wids['ventana'])
                    partidaCem = None
            except ValueError:
                utils.dialogo_info(
                    titulo = "ERROR BUSCANDO PARTIDA DE FIBRA EMBOLSADA", 
                    texto = "El texto %s provocó un error en la búsqueda." % (
                        a_buscar), 
                    padre = self.wids['ventana'])
                partidaCem = None
            objeto = partidaCem
        elif a_buscar.startswith(pclases.PREFIJO_PARTIDACARGA):
            try:
                partidacarga = pclases.PartidaCarga.select(
                    pclases.PartidaCarga.q.numpartida == int(a_buscar[2:]))[0]
            except IndexError:
                try:
                    partidacarga = pclases.PartidaCarga.select(
                        pclases.PartidaCarga.q.codigo == a_buscar)[0]
                except IndexError:
                    utils.dialogo_info(titulo="PARTIDA DE CARGA NO ENCONTRADA",
                        texto = "La partida de carga %s no se encontró." % (
                            a_buscar), 
                        padre = self.wids['ventana'])
                    partidacarga = None
            except ValueError:
                utils.dialogo_info(titulo = "ERROR BUSCANDO PARTIDA DE CARGA", 
                    texto = "El texto %s provocó un error en la búsqueda." % (
                        a_buscar), 
                    padre = self.wids['ventana'])
                partidacarga = None
            objeto = partidacarga
        elif a_buscar.startswith(pclases.PREFIJO_BIGBAG):
            try:
                objeto = pclases.Bigbag.select(
                    pclases.Bigbag.q.codigo == a_buscar)[0]
            except IndexError:
                objeto = self.buscar_bigbag(a_buscar[1:])
        elif a_buscar.startswith(pclases.PREFIJO_ROLLODEFECTUOSO):
            try:
                objeto = pclases.RolloDefectuoso.select(
                    pclases.RolloDefectuoso.q.codigo == a_buscar)[0]
            except IndexError:
                objeto = None       # O lo busca bien o que se vaya a "puirla".
        elif a_buscar.startswith(pclases.PREFIJO_BALACABLE):
            try:
                objeto = pclases.BalaCable.select(
                    pclases.BalaCable.q.codigo == a_buscar)[0]
            except IndexError:
                objeto = None       # O lo busca bien o que se vaya a "puirla".
        elif a_buscar.startswith(pclases.PREFIJO_ROLLOC):
            try:
                objeto = pclases.RolloC.select(
                    pclases.RolloC.q.codigo == a_buscar)[0]
            except IndexError:
                objeto = None       # O lo busca bien o que se vaya a "puirla".
        elif a_buscar.startswith(pclases.PREFIJO_PALE):
            try:
                objeto = pclases.Pale.select(
                    pclases.Pale.q.codigo == a_buscar)[0]
            except IndexError:
                objeto = None       # O lo busca bien o que se vaya a "puirla".
        elif a_buscar.startswith(pclases.PREFIJO_CAJA):
            try:
                objeto = pclases.Caja.select(
                    pclases.Caja.q.codigo == a_buscar)[0]
            except IndexError:
                objeto = None       # O lo busca bien o que se vaya a "puirla".
        elif a_buscar.startswith(pclases.PREFIJO_BOLSA):
        # No more bolsas como tal.
        #    try:
        #        objeto = pclases.Bolsa.select(
        #                    pclases.Bolsa.q.codigo == a_buscar.upper())[0]
        #    except IndexError:
        #        objeto = None     # O lo busca bien o que se vaya a "puirla".
        # Voy a buscar la caja a la que pertenece la bolsa:
            objeto = pclases.Caja.get_caja_from_bolsa(a_buscar)
        else:
            objeto = self.buscar_articulo(a_buscar)
        if objeto != None:
            objeto.sync()
            if hasattr(objeto, "codigo"):
                self.wids['e_num'].set_text(objeto.codigo)
            else:
                self.wids['e_num'].set_text("DEBUG: __hash__ %s" % (
                    objeto.__hash__()))
            self.rellenar_datos(objeto)
        else:
            utils.dialogo_info(titulo = "NO ENCONTRADO", 
                               texto = "Producto no encontrado", 
                               padre = self.wids['ventana'])

    def rellenar_datos(self, objeto):
        """
        "objeto" es el objeto sobre el que se va a mostar la información.
        """
        objeto.sync()
        if isinstance(objeto, (pclases.Bala, pclases.Rollo, pclases.Bigbag, 
                               pclases.RolloDefectuoso, pclases.BalaCable, 
                               pclases.RolloC, pclases.Pale, pclases.Caja, 
                               )):
                                # pclases.Bolsa)):
            try:
                objeto.articulo.sync()
            except AttributeError:
                pass    # Es una caja o un palé. No tiene artículo concreto 
                        # que sincronizar.
            self.rellenar_producto(objeto)
            self.rellenar_lotepartida(objeto)
            self.rellenar_albaran(objeto)
            self.rellenar_produccion(objeto)
            self.wids['e_num'].set_text(objeto.codigo)
        elif isinstance(objeto, pclases.PartidaCarga):
            from ventana_progreso import VentanaProgreso
            vpro = VentanaProgreso(padre = self.wids['ventana'])
            vpro.mostrar()
            i = 0.0
            tot = 5
            vpro.set_valor(i/tot, "Buscando..."); i += 1
            import time; time.sleep(0.5)
            vpro.set_valor(i/tot, "Producto..."); i += 1
            self.rellenar_producto_partida_carga(objeto)
            vpro.set_valor(i/tot, "Lote/Partida..."); i += 1
            self.rellenar_partida_carga(objeto)
            vpro.set_valor(i/tot, "Albarán de salida..."); i += 1
            self.rellenar_albaran_partida_carga(objeto)
            vpro.set_valor(i/tot, "Producción..."); i += 1
            self.rellenar_produccion_partida_carga(objeto)
            self.wids['e_num'].set_text(objeto.codigo)
            vpro.ocultar()
        elif isinstance(objeto,(pclases.Lote, pclases.LoteCem,
                                pclases.Partida, pclases.PartidaCem)):
            vpro = VentanaProgreso(padre = self.wids['ventana'])
            vpro.mostrar()
            i = 0.0
            tot = 5
            vpro.set_valor(i/tot, "Buscando..."); i += 1
            time.sleep(0.5)
            vpro.set_valor(i/tot, "Producto..."); i += 1
            self.rellenar_producto_lote_o_partida(objeto)
            vpro.set_valor(i/tot, "Lote/Partida..."); i += 1
            self.rellenar_lote_o_partida(objeto)
            vpro.set_valor(i/tot, "Albarán de salida..."); i += 1
            self.rellenar_albaran_lote_o_partida(objeto)
            vpro.set_valor(i/tot, "Producción..."); i += 1
            self.rellenar_produccion_lote_o_partida(objeto)
            self.wids['e_num'].set_text(objeto.codigo)
            vpro.ocultar()
   
    def rellenar_producto_partida_carga(self, pcarga):
        """
        Muestra los productos de fibra que componen la partida de carga.
        """
        txtvw = self.wids['txt_producto']
        borrar_texto(txtvw)
        prodsfibra = {}
        total = 0.0
        for bala in pcarga.balas:
            a = bala.articulo
            pv = a.productoVenta
            l = bala.lote
            if pv not in prodsfibra:
                prodsfibra[pv] = {}
            if bala.lote not in prodsfibra[pv]:
                prodsfibra[pv][l] = {'balas': [], 'total': 0.0}
            prodsfibra[pv][l]['balas'].append(bala)
            prodsfibra[pv][l]['total'] += bala.pesobala
            total += bala.pesobala
        for pv in prodsfibra:
            escribir(txtvw, 
                     "%s kg de %s\n" % (utils.float2str(sum(
                        [prodsfibra[pv][l]['total'] for l in prodsfibra[pv]])),
                        pv.descripcion), 
                     ("negrita"))
            for l in prodsfibra[pv]:
                escribir(txtvw, "\t%d balas del lote %s; %s kg\n" % (
                    len(prodsfibra[pv][l]['balas']), 
                    l.codigo, 
                    utils.float2str(prodsfibra[pv][l]['total'])))
        escribir(txtvw, 
                 "Total cargado: %s kg\n" % (utils.float2str(total)), 
                 ("negrita", "grande"))

    def rellenar_partida_carga(self, pcarga):
        """
        Muestra la partida de carga, fecha y partidas de geotextiles 
        relacionados con ella.
        """
        txtvw = self.wids['txt_lp']
        borrar_texto(txtvw)
        escribir(txtvw, "Partida de carga %s (%s)\n" % (
            pcarga.numpartida, pcarga.codigo), ("negrita"))
        escribir(txtvw, "Fecha y hora de creación: %s %s\n" % (
                    utils.str_fecha(pcarga.fecha), 
                    utils.str_hora_corta(pcarga.fecha)), 
                 ("cursiva"))
        escribir(txtvw, "Partidas de geotextiles relacionados:\n")
        for partida in pcarga.partidas:
            escribir(txtvw, "\tPartida %s (%s)\n" % (partida.numpartida, 
                                                     partida.codigo))

    def rellenar_albaran_partida_carga(self, pcarga):
        """
        Muestra los albaranes internos relacionados con las balas de la 
        partida de carga.
        """
        txtvw = self.wids['txt_albaran']
        borrar_texto(txtvw)
        albs = []
        for bala in pcarga.balas:
            alb = bala.articulo.albaranSalida
            if alb != None and alb not in albs:
                albs.append(alb)
                escribir(txtvw, "Albarán %s (%s): %s\n" % (alb.numalbaran, 
                                    utils.str_fecha(alb.fecha), 
                                    alb.cliente and alb.cliente.nombre or "-"))

    def rellenar_produccion_partida_carga(self, pcarga):
        """
        Muestra los rollos fabricados, metros cuadrados y kilos reales 
        por parte de produccion.
        """
        txtvw = self.wids['txt_produccion']
        borrar_texto(txtvw)
        fab = {}
        for partida in pcarga.partidas:
            for rollo in partida.rollos:
                pv = rollo.productoVenta
                metros = pv.camposEspecificosRollo.get_metros_cuadrados()
                if pv not in fab:
                    fab[pv] = {'rollos': [rollo], 
                               'peso_real': rollo.peso, 
                               'peso_sin': rollo.peso_sin, 
                               'peso_teorico': rollo.peso_teorico, 
                               'metros': metros}
                else:
                    fab[pv]['rollos'].append(rollo)
                    fab[pv]['peso_real'] += rollo.peso
                    fab[pv]['peso_sin'] += rollo.peso_sin
                    fab[pv]['peso_teorico'] += rollo.peso_teorico
                    fab[pv]['metros'] += metros 
        total_peso_real=total_peso_sin=total_peso_teorico=total_metros=0.0
        total_rollos = 0
        for pv in fab:
            escribir(txtvw, "%s:\n" % (pv.descripcion), ("negrita"))
            escribir(txtvw, "\t%d rollos.\n" % (len(fab[pv]['rollos'])))
            total_rollos += len(fab[pv]['rollos'])
            escribir(txtvw, "\t%s kg peso real.\n" % (
                                utils.float2str(fab[pv]['peso_real'])))
            total_peso_real += fab[pv]['peso_real']
            escribir(txtvw, "\t%s kg peso sin embalaje.\n" % (
                                utils.float2str(fab[pv]['peso_sin'])))
            total_peso_sin += fab[pv]['peso_sin']
            escribir(txtvw, "\t%s kg peso teórico.\n" % (
                                utils.float2str(fab[pv]['peso_teorico'])))
            total_peso_teorico += fab[pv]['peso_teorico']
            escribir(txtvw, "\t%s m².\n" % utils.float2str(fab[pv]['metros']))
            total_metros += fab[pv]['metros']
        escribir(txtvw, "Total fabricado:\n", ("negrita", "grande"))
        escribir(txtvw, "\t%d rollos.\n" % (total_rollos), ("negrita"))
        escribir(txtvw, "\t%s kg peso real.\n" % (
                            utils.float2str(total_peso_real)), ("negrita"))
        escribir(txtvw, "\t%s kg peso sin embalaje.\n" % (
                            utils.float2str(total_peso_sin)), ("negrita"))
        escribir(txtvw, "\t%s kg peso teórico.\n" % (
                            utils.float2str(total_peso_teorico)), ("negrita"))
        escribir(txtvw, "\t%s m².\n" % (utils.float2str(total_metros)), 
                                        ("negrita"))
 
    def rellenar_producto_lote_o_partida(self, objeto):
        """
        Determina el producto (o productos, para lotes antiguos) 
        al que pertenece el lote, lote de cemento o partida y lo 
        muestra en el cuadro correspondiente.
        """
        txtvw = self.wids['txt_producto']
        borrar_texto(txtvw)
        productos = []
        if isinstance(objeto, pclases.Lote):
            for bala in objeto.balas:
                if (bala.articulo and bala.articulo.productoVenta 
                    and bala.articulo.productoVenta not in productos):
                    productos.append(bala.articulo.productoVenta)
        elif isinstance(objeto, pclases.LoteCem):
            for bigbag in objeto.bigbags:
                if (bigbag.articulo and bigbag.articulo.productoVenta 
                    and bigbag.articulo.productoVenta not in productos):
                    productos.append(bigbag.articulo.productoVenta)
        elif isinstance(objeto, pclases.Partida):
            for rollo in objeto.rollos:
                if (rollo.articulo and rollo.articulo.productoVenta 
                    and rollo.articulo.productoVenta not in productos):
                    productos.append(rollo.articulo.productoVenta)
        elif isinstance(objeto, pclases.PartidaCem):
            for pale in objeto.pales:
                if (pale.productoVenta 
                    and pale.productoVenta not in productos):
                    productos.append(pale.productoVenta)
        for producto in productos:
            self.rellenar_info_producto_venta(producto, txtvw)

    def rellenar_lote_o_partida(self, objeto):
        """
        Muestra la información del lote o partida
        """
        txtvw = self.wids['txt_lp']
        borrar_texto(txtvw)
        if isinstance(objeto, pclases.Lote): 
            self.rellenar_info_lote(objeto, txtvw) 
        elif isinstance(objeto, pclases.LoteCem):
            self.rellenar_info_lote_cemento(objeto, txtvw) 
        elif isinstance(objeto, pclases.Partida):
            self.rellenar_info_partida(objeto, txtvw)
        elif isinstance(objeto, pclases.PartidaCem):
            self.rellenar_info_partidaCem(objeto, txtvw)
    
    def rellenar_albaran_lote_o_partida(self, objeto):
        """
        Busca los artículos que siguen en almacén del lote o partida y muestra 
        también la relación de albaranes de los que han salido.
        """
        txtvw = self.wids['txt_albaran']
        borrar_texto(txtvw)
        albs = {}
        en_almacen = 0
        if isinstance(objeto, pclases.LoteCem):
            bultos = objeto.bigbags
        elif isinstance(objeto, pclases.Lote):
            bultos = objeto.balas 
        elif isinstance(objeto, pclases.Partida):
            bultos = objeto.rollos
        elif isinstance(objeto, pclases.PartidaCem):
            bultos = []
            for pale in objeto.pales:
                for caja in pale.cajas:
                    bultos.append(caja)
        for bulto in bultos:
            albaran = bulto.articulo.albaranSalida
            if albaran == None:
                en_almacen += 1
            else:
                if albaran not in albs:
                    albs[albaran] = 1
                else:
                    albs[albaran] += 1
        self.mostrar_info_albaranes_lote_o_partida(txtvw, 
                                                   bultos, 
                                                   albs, 
                                                   en_almacen)

    def mostrar_info_albaranes_lote_o_partida(self, 
                                              txtvw, 
                                              bultos, 
                                              albs, 
                                              en_almacen):
        """
        Introduce la información en sí en el TextView.
        """
        escribir(txtvw, "Bultos en almacén: %d\n" % (en_almacen))
        escribir(txtvw, "Bultos vendidos: %d\n" % (len(bultos) - en_almacen))
        for albaran in albs:
            escribir(txtvw, "\t%d en el albarán %s.\n" % (albs[albaran], 
                                                          albaran.numalbaran))

    def rellenar_produccion_lote_o_partida(self, objeto):
        """
        Muestra el número de bultos y kg o metros fabricados
        para el lote, loteCem o partida en cuestión.
        Si el objeto es una partida, muestra además el consumo 
        de materia prima.
        """
        txtvw = self.wids['txt_produccion']
        borrar_texto(txtvw)
        if isinstance(objeto, pclases.LoteCem):
            self.mostrar_produccion_lote_cemento(objeto, txtvw)
        elif isinstance(objeto, pclases.Lote):
            self.mostrar_produccion_lote(objeto, txtvw)
        elif isinstance(objeto, pclases.Partida):
            self.mostrar_produccion_partida(objeto, txtvw)
        elif isinstance(objeto, pclases.PartidaCem):
            self.mostrar_produccion_partidaCem(objeto, txtvw)

    def mostrar_produccion_lote(self, objeto, txtvw):
        """
        Muestra las balas del lote producidas, desglosadas en 
        clase A y clase B; y los partes donde se fabricaron.
        """
        ba = {'bultos': 0, 'peso': 0.0}
        bb = {'bultos': 0, 'peso': 0.0}
        partes = []
        for b in objeto.balas:
            if (b.articulo.parteDeProduccion != None 
                and b.articulo.parteDeProduccion not in partes):
                partes.append(b.articulo.parteDeProduccion)
            if b.claseb:
                bb['bultos'] += 1
                bb['peso'] += b.pesobala
            else:
                ba['bultos'] += 1
                ba['peso'] += b.pesobala
        escribir(txtvw, 
                 "Balas clase A: %d; %s kg\n" % (ba['bultos'], 
                                                 utils.float2str(ba['peso'])))
        escribir(txtvw, 
                 "Balas clase B: %d; %s kg\n" % (bb['bultos'], 
                                                 utils.float2str(bb['peso'])))
        escribir(txtvw, 
                 "TOTAL: %d balas; %s kg\n" % (ba['bultos'] + bb['bultos'], 
                                               utils.float2str(
                                                    ba['peso'] + bb['peso'])))
        escribir(txtvw, "\nLote de fibra fabricado en los partes:\n")
        partes.sort(lambda p1, p2: int(p1.id - p2.id))
        for parte in partes:
            escribir(txtvw, 
                     "%s (%s-%s)\n" % (utils.str_fecha(parte.fecha), 
                                       utils.str_hora_corta(parte.horainicio),
                                       utils.str_hora_corta(parte.horafin)))

    def mostrar_produccion_partida(self, objeto, txtvw):
        """
        Muestra la producción de los rollos de la partida.
        """
        rs = {'bultos': 0, 
              'peso': 0.0, 
              'peso_sin': 0.0, 
              'metros2': 0.0, 
              'bultos_d': 0, 
              'peso_d': 0.0, 
              'peso_sin_d': 0.0, 
              'peso_teorico': objeto.get_kilos_teorico(
                                    contar_defectuosos = False),
              'peso_teorico_d': objeto.get_kilos_teorico(
                                    contar_defectuosos = True),
              'metros2_d': 0.0}
        partes = []
        for r in objeto.rollos:
            if (r.articulo.parteDeProduccion != None 
                and r.articulo.parteDeProduccion not in partes):
                partes.append(r.articulo.parteDeProduccion)
            rs['bultos'] += 1
            rs['peso'] += r.peso
            rs['peso_sin'] += r.peso_sin
            rs['metros2'] += r.articulo.superficie
        for r in objeto.rollosDefectuosos:
            if (r.articulo.parteDeProduccion != None 
                and r.articulo.parteDeProduccion not in partes):
                partes.append(r.articulo.parteDeProduccion)
            rs['bultos_d'] += 1
            rs['peso_d'] += r.peso
            rs['peso_sin_d'] += r.peso_sin
            rs['metros2_d'] += r.articulo.superficie
        escribir(txtvw, 
                 "TOTAL:\n\t%d rollos;\n"
                 "\t%d rollos defectuosos;\n"
                 "\t\t%d rollos en total.\n"
                 "\t%s kg reales (%s kg + %s kg en rollos defectuosos).\n"
                 "\t%s kg sin embalaje (%s kg + %s kg en rollos defectuosos)."
                 "\n""\t%s kg teóricos (%s kg teóricos incluyendo rollos "
                 "defectuosos).\n"
                 "\t%s m² (%s m² + %s m² en rollos defectuosos).\n" % (
                            rs['bultos'], 
                            rs['bultos_d'], 
                            rs['bultos'] + rs['bultos_d'], 
                            utils.float2str(rs['peso'] + rs['peso_d']), 
                            utils.float2str(rs['peso']), 
                            utils.float2str(rs['peso_d']), 
                            utils.float2str(rs['peso_sin'] + rs['peso_sin_d']),
                            utils.float2str(rs['peso_sin']), 
                            utils.float2str(rs['peso_sin_d']), 
                            utils.float2str(rs['peso_teorico']), 
                            utils.float2str(rs['peso_teorico_d']), 
                            utils.float2str(rs['metros2'] + rs['metros2_d']), 
                            utils.float2str(rs['metros2']), 
                            utils.float2str(rs['metros2_d'])))
        escribir(txtvw, "\nPartida de geotextiles fabricada en los partes:\n")
        partes.sort(lambda p1, p2: int(p1.id - p2.id))
        for parte in partes:
            escribir(txtvw, 
                     "%s (%s-%s)\n" % (utils.str_fecha(parte.fecha), 
                                       utils.str_hora_corta(parte.horainicio), 
                                       utils.str_hora_corta(parte.horafin)))
        escribir(txtvw, "\n\nConsumos:\n", ("rojo, negrita"))
        from informes import geninformes
        escribir(txtvw, geninformes.consumoPartida(objeto), ("rojo"))

    def mostrar_produccion_lote_cemento(self, objeto, txtvw):
        """
        Muestra el total de bigbags del lote y su peso total, 
        también muestra los de clase A y B y las fechas y turnos
        de los partes en los que se fabricaron.
        """
        bba = {'bultos': 0, 'peso': 0.0}
        bbb = {'bultos': 0, 'peso': 0.0}
        partes = []
        for bb in objeto.bigbags:
            if (bb.articulo.parteDeProduccion != None 
                and bb.articulo.parteDeProduccion not in partes):
                partes.append(bb.articulo.parteDeProduccion)
            if bb.claseb:
                bbb['bultos'] += 1
                bbb['peso'] += bb.pesobigbag
            else:
                bba['bultos'] += 1
                bba['peso'] += bb.pesobigbag
        escribir(txtvw, "Bigbags clase A: %d; %s kg\n" % (
            bba['bultos'], utils.float2str(bba['peso'])))
        escribir(txtvw, "Bigbags clase B: %d; %s kg\n" % (
            bbb['bultos'], utils.float2str(bbb['peso'])))
        escribir(txtvw, "TOTAL: %d bigbags; %s kg\n" % (
            bba['bultos'] + bbb['bultos'], 
            utils.float2str(bba['peso'] + bbb['peso'])))
        escribir(txtvw, 
            "\nLote de fibra de cemento fabricado en los partes:\n")
        partes.sort(lambda p1, p2: int(p1.id - p2.id))
        for parte in partes:
            escribir(txtvw, "%s (%s-%s)\n" % (
                utils.str_fecha(parte.fecha), 
                utils.str_hora_corta(parte.horainicio), 
                utils.str_hora_corta(parte.horafin)))

    def mostrar_produccion_partidaCem(self, objeto, txtvw):
        """
        Muestra el total de palés de la partida de cemento y su peso total, 
        también muestra los de clase A y B y las fechas y turnos
        de los partes en los que se fabricaron.
        """
        palesa = {'cajas': 0, 'bultos': 0, 'peso': 0.0}
        palesb = {'cajas': 0, 'bultos': 0, 'peso': 0.0}
        partes = []
        for pale in objeto.pales:
            if (pale.parteDeProduccion != None 
                and pale.parteDeProduccion not in partes):
                partes.append(pale.parteDeProduccion)
            if pale.claseb:
                palesb['bultos'] += 1
                palesb['peso'] += pale.calcular_peso()
                palesb['cajas'] += len(pale.cajas)  # Más realista en caso de 
                        # incoherencias en la base de datos que pale.numcajas.
            else:
                palesa['bultos'] += 1
                palesa['peso'] += pale.calcular_peso()
                palesa['cajas'] += len(pale.cajas)  
        escribir(txtvw, "Palés clase A: %d; %s kg (%d cajas)\n" % (
            palesa['bultos'], utils.float2str(palesa['peso']), 
            palesa['cajas']))
        escribir(txtvw, "Palés clase B: %d; %s kg (%d cajas)\n" % (
            palesb['bultos'], utils.float2str(palesb['peso']), 
            palesb['cajas']))
        escribir(txtvw, "TOTAL: %d palés; %s kg (%d cajas)\n" % (
            palesa['bultos'] + palesb['bultos'], 
            utils.float2str(palesa['peso'] + palesb['peso']), 
            palesa['cajas'] + palesb['cajas']))
        escribir(txtvw, "\nPartida de fibra de cemento embolsada "
                        "fabricada en los partes:\n")
        partes.sort(lambda p1, p2: int(p1.id - p2.id))
        for parte in partes:
            escribir(txtvw, "%s (%s-%s)\n" % (
                utils.str_fecha(parte.fecha), 
                utils.str_hora_corta(parte.horainicio), 
                utils.str_hora_corta(parte.horafin)))

    def rellenar_info_lote(self, lote, txtvw):
        """
        Recibe un lote y escribe en txtvw toda la información del mismo.
        """
        escribir(txtvw, "Lote número: %d\n" % (lote.numlote))
        escribir(txtvw, "Código de lote: %s\n" % (lote.codigo), 
                      ("negrita", ))
        escribir(txtvw, "Tenacidad: %s" % (lote.tenacidad))
        escribir(txtvw, " (%s)\n" % (
            utils.float2str(lote.calcular_tenacidad_media())), ("azul"))
        escribir(txtvw, "Elongación: %s" % (lote.elongacion))
        escribir(txtvw, " (%s)\n" % (
            utils.float2str(lote.calcular_elongacion_media())), ("azul"))
        escribir(txtvw, "Rizo: %s" % (lote.rizo))
        escribir(txtvw, " (%s)\n" % (
            utils.float2str(lote.calcular_rizo_medio())), ("azul"))
        escribir(txtvw, "Encogimiento: %s" % (lote.encogimiento))
        escribir(txtvw, " (%s)\n" % (
            utils.float2str(lote.calcular_encogimiento_medio())), ("azul"))
        escribir(txtvw, "Grasa: %s" % (utils.float2str(lote.grasa)))
        escribir(txtvw, " (%s)\n" % (
            utils.float2str(lote.calcular_grasa_media())), ("azul"))
        escribir(txtvw, "Media de título: %s" % (
            utils.float2str(lote.mediatitulo)))
        escribir(txtvw, " (%s)\n" % (
            utils.float2str(lote.calcular_titulo_medio())), ("azul"))
        escribir(txtvw, "Tolerancia: %s\n" % (
            utils.float2str(lote.tolerancia)))
        escribir(txtvw, "Muestras extraídas en el lote: %d\n" % 
            len(lote.muestras))
        escribir(txtvw, "Pruebas de estiramiento realizadas: %d\n" % 
            len(lote.pruebasElongacion))
        escribir(txtvw, "Pruebas de medida de rizo realizadas: %d\n" % 
            len(lote.pruebasRizo))
        escribir(txtvw, "Pruebas de encogimiento realizadas: %d\n" % 
            len(lote.pruebasEncogimiento))
        escribir(txtvw, "Pruebas de tenacidad realizadas: %d\n" % 
            len(lote.pruebasTenacidad))
        escribir(txtvw, "Pruebas de grasa realizadas: %d\n" % 
            len(lote.pruebasGrasa))
        escribir(txtvw, "Pruebas de título realizadas: %d\n" % 
            len(lote.pruebasTitulo))

    def rellenar_info_partida_cemento(self, partida, txtvw):
        """
        Rellena la información de la partida de fibra de cemento.
        """
        escribir(txtvw, "Partida de cemento número: %s\n" % (
            partida and str(partida.numpartida) or "Sin partida relacionada."))
        escribir(txtvw, "Código de partida: %s\n" % (
            partida and partida.codigo or "Sin partida relacionada."), 
            ("negrita", ))

    def rellenar_info_lote_cemento(self, lote, txtvw):
        """
        Rellena la información del lote de cemento.
        """
        escribir(txtvw, "Lote número: %d\n" % (lote.numlote))
        escribir(txtvw, "Código de lote: %s\n" % (lote.codigo), 
            ("negrita", ))
        escribir(txtvw, "Tenacidad: %s" % (lote.tenacidad))
        escribir(txtvw, " (%s)\n" % (lote.calcular_tenacidad_media()), 
            ("azul"))
        escribir(txtvw, "Elongación: %s" % (lote.elongacion))
        escribir(txtvw, " (%s)\n" % (lote.calcular_elongacion_media()), 
            ("azul"))
        escribir(txtvw, "Encogimiento: %s" % (lote.encogimiento))
        escribir(txtvw, " (%s)\n" % (lote.calcular_encogimiento_medio()), 
            ("azul"))
        escribir(txtvw, "Grasa: %s" % (
            lote.grasa and utils.float2str(lote.grasa) or "-"))
        escribir(txtvw, " (%s)\n" % (lote.calcular_grasa_media()), 
            ("azul"))
        escribir(txtvw, "Humedad: %s" % (lote.humedad))
        escribir(txtvw, " (%s)\n" % (lote.calcular_humedad_media()), 
            ("azul"))
        escribir(txtvw, "Media de título: %s" % (
            lote.mediatitulo and utils.float2str(lote.mediatitulo) or "-"))
        escribir(txtvw, " (%s)\n" % (lote.calcular_titulo_medio()), 
            ("azul"))
        escribir(txtvw, "Tolerancia: %s\n" % (
            lote.tolerancia and utils.float2str(lote.tolerancia) or "-"))
        escribir(txtvw, "Muestras extraídas en el lote: %d\n" % (
            len(lote.muestras)))
        escribir(txtvw, "Pruebas de estiramiento realizadas: %d\n" % (
            len(lote.pruebasElongacion)))
        escribir(txtvw, "Pruebas de encogimiento realizadas: %d\n" % (
            len(lote.pruebasEncogimiento)))
        escribir(txtvw, "Pruebas de grasa realizadas: %d\n" % (
            len(lote.pruebasGrasa)))
        escribir(txtvw, "Pruebas de medida de humedad realizadas: %d\n" %
            (len(lote.pruebasHumedad)))
        escribir(txtvw, "Pruebas de tenacidad realizadas: %d\n" % (
            len(lote.pruebasTenacidad)))
        escribir(txtvw, "Pruebas de título realizadas: %d\n" % (
            len(lote.pruebasTitulo)))

    def rellenar_info_partida(self, partida, txtvw):
        """
        Muestra la información de la partida en el txtvw.
        """
        escribir(txtvw, "Número de partida: %d\n" % (partida.numpartida))
        escribir(txtvw, "Código de partida: %s\n" % (partida.codigo), 
                 ("negrita"))
        escribir(txtvw, "Gramaje: %s" % (utils.float2str(partida.gramaje)))
        escribir(txtvw, 
                 " (%s)\n" % utils.float2str(partida.calcular_gramaje_medio()),
                 ("azul"))
        escribir(txtvw, 
                 "Resistencia longitudinal: %s" % (
                    utils.float2str(partida.longitudinal)))
        escribir(txtvw, 
                 " (%s)\n" % (utils.float2str(
                    partida.calcular_resistencia_longitudinal_media())), 
                 ("azul"))
        escribir(txtvw, 
                 "Alargamiento longitudinal: %s" % (
                    utils.float2str(partida.alongitudinal)))
        escribir(txtvw, 
                 " (%s)\n" % (utils.float2str(
                    partida.calcular_alargamiento_longitudinal_medio())), 
                 ("azul"))
        escribir(txtvw, 
                 "Resistencia transversal: %s" % (
                    utils.float2str(partida.transversal)))
        escribir(txtvw, 
                 " (%s)\n" % (utils.float2str(
                    partida.calcular_resistencia_transversal_media())), 
                 ("azul"))
        escribir(txtvw, 
                 "Alargamiento transversal: %s" % (
                    utils.float2str(partida.atransversal)))
        escribir(txtvw, 
                 " (%s)\n" % (utils.float2str(
                    partida.calcular_alargamiento_transversal_medio())), 
                 ("azul"))
        escribir(txtvw, "CBR: %s" % (utils.float2str(partida.compresion)))
        escribir(txtvw, 
                 " (%s)\n" % (
                    utils.float2str(partida.calcular_compresion_media())), 
                 ("azul"))
        escribir(txtvw, 
                 "Perforación: %s" % (utils.float2str(partida.perforacion)))
        escribir(txtvw, 
                 " (%s)\n" % (
                    utils.float2str(partida.calcular_perforacion_media())), 
                 ("azul"))
        escribir(txtvw, 
                 "Espesor: %s" % (utils.float2str(partida.espesor)))
        escribir(txtvw, 
                 " (%s)\n" % (
                    utils.float2str(partida.calcular_espesor_medio())), 
                 ("azul"))
        escribir(txtvw, 
                 "Permeabilidad: %s" % (
                    utils.float2str(partida.permeabilidad)))
        escribir(txtvw, 
                 " (%s)\n" % (
                    utils.float2str(partida.calcular_permeabilidad_media())), 
                 ("azul"))
        escribir(txtvw, 
                 "Apertura de poros: %s" % (utils.float2str(partida.poros)))
        escribir(txtvw, 
                 " (%s)\n" % (
                    utils.float2str(partida.calcular_poros_medio())),
                 ("azul"))
        escribir(txtvw, 
                 "Resistencia al punzonado piramidal: %s" % (
                    utils.float2str(partida.piramidal)))
        escribir(txtvw, 
                 " (%s)\n" % (
                    utils.float2str(partida.calcular_piramidal_media())),
                 ("azul"))
        escribir(txtvw, 
                 "Muestras extraídas en la partida: %d\n" % len(
                    partida.muestras))
        escribir(txtvw, 
                 "Pruebas de alargamiento longitudinal realizadas: %d\n" % len(
                    partida.pruebasAlargamientoLongitudinal))
        escribir(txtvw, 
                 "Pruebas de alargamiento transversal realizadas: %d\n" % len(
                    partida.pruebasAlargamientoTransversal))
        escribir(txtvw, 
                 "Pruebas de compresión realizadas: %d\n" % len(
                    partida.pruebasCompresion))
        escribir(txtvw, 
                 "Pruebas de espesor realizadas: %d\n" % len(
                    partida.pruebasEspesor))
        escribir(txtvw, 
                 "Pruebas de gramaje realizadas: %d\n" % len(
                    partida.pruebasGramaje))
        escribir(txtvw, 
                 "Pruebas de perforación realizadas: %d\n" % len(
                    partida.pruebasPerforacion))
        escribir(txtvw, 
                 "Pruebas de permeabilidad realizadas: %d\n" % len(
                    partida.pruebasPermeabilidad))
        escribir(txtvw, 
                 "Pruebas de poros realizadas: %d\n"%len(partida.pruebasPoros))
        escribir(txtvw, 
                 "Pruebas de resistencia longitudinal realizadas: %d\n" % len(
                    partida.pruebasResistenciaLongitudinal))
        escribir(txtvw, 
                 "Pruebas de resistencia transversal realizadas: %d\n" % len(
                    partida.pruebasResistenciaTransversal))
        escribir(txtvw, 
                 "Pruebas de punzonado piramidal realizadas: %d\n" % len(
                    partida.pruebasPiramidal))

    def rellenar_info_partidaCem(self, partida, txtvw):
        """
        Muestra la información de la partida de cemento en el txtvw.
        """
        escribir(txtvw, "Número de partida: %d\n" % (partida.numpartida))
        escribir(txtvw, "Código de partida: %s\n" % (partida.codigo), 
                 ("negrita"))

    def rellenar_lotepartida(self, articulo):
        txtvw = self.wids['txt_lp']
        borrar_texto(txtvw)
        if isinstance(articulo, pclases.Bala):
            self.rellenar_info_lote(articulo.lote, txtvw)
        elif isinstance(articulo, (pclases.Rollo, pclases.RolloDefectuoso)):
            self.rellenar_info_partida(articulo.partida, txtvw)
        elif isinstance(articulo, pclases.Bigbag):
            lote = articulo.loteCem
            self.rellenar_info_lote_cemento(articulo.loteCem, txtvw)
        elif isinstance(articulo, (pclases.BalaCable, pclases.RolloC)):
            lote = None     # Las balas de cable no se agrupan por lotes.
        elif isinstance(articulo, (pclases.Pale, pclases.Caja)):
            #, pclases.Bolsa)):
            lote = articulo.partidaCem
            self.rellenar_info_partida_cemento(lote, txtvw)
        else:
            escribir(txtvw, "¡NO SE ENCONTRÓ INFORMACIÓN!\n"
                "Posible inconsistencia de la base de datos. "
                "Contacte con el administrador.")
            self.logger.error("trazabilidad_articulos.py::"
                              "rellenar_lote_partida -> "
                              "No se encontró información acerca del "
                              "artículo ID %d." % (articulo.id))

    def rellenar_albaran(self, articulo):
        txtvw = self.wids['txt_albaran']
        borrar_texto(txtvw)
        if isinstance(articulo, pclases.Pale):
            pale = articulo
            cajas_a_mostrar = []
            albaranes_tratados = []
            for caja in pale.cajas:
                articulo_caja = caja.articulo
                alb = articulo_caja.albaranSalida
                if alb not in albaranes_tratados:
                    albaranes_tratados.append(alb)
                    cajas_a_mostrar.append(caja)
            for caja in cajas_a_mostrar:
                self.rellenar_albaran(caja)
        else:
            try:
                a = articulo.articulos[0]
            except IndexError, msg:
                self.logger.error("ERROR trazabilidad_articulos.py "
                                  "(rellenar_albaran): %s" % (msg))
            else:
                for fecha, objeto, almacen in a.get_historial_trazabilidad():
                    if isinstance(objeto, pclases.AlbaranSalida):
                        escribir(txtvw, "Albarán número: %s (%s)\n" % (
                                       objeto.numalbaran, 
                                       objeto.get_str_tipo()), 
                                      ("_rojoclaro", ))
                        escribir(txtvw, "Fecha: %s\n" % 
                            utils.str_fecha(objeto.fecha))
                        escribir(txtvw, "Transportista: %s\n" % (
                            objeto.transportista 
                                and objeto.transportista.nombre or ''))
                        escribir(txtvw, "Cliente: %s\n" % (
                            objeto.cliente and objeto.cliente.nombre or ''), 
                            ("negrita", ))
                        destino = (objeto.almacenDestino and 
                                   objeto.almacenDestino.nombre or 
                                   objeto.nombre)
                        escribir(txtvw, "Origen: %s\n" % (
                            objeto.almacenOrigen 
                            and objeto.almacenOrigen.nombre 
                            or "ERROR - ¡Albarán sin almacén de origen!"))
                        escribir(txtvw, "Destino: %s\n" % (destino))
                    elif isinstance(objeto, pclases.Abono):
                        escribir(txtvw, 
                            "El artículo fue devuelto el %s a %s en el abono"
                            " %s.\n" % (utils.str_fecha(fecha), 
                                      almacen.nombre, 
                                      objeto.numabono), 
                            ("rojo", ))
                        # Y si ya está efectivamente en almacén, lo digo:
                        adeda = None
                        for ldd in objeto.lineasDeDevolucion:
                            if ldd.articulo == a:    # ¡Te encontré, sarraceno!
                                adeda = ldd.albaranDeEntradaDeAbono
                        if not adeda:
                            escribir(txtvw,"El artículo aún no ha entrado"
                                " en almacén. El abono no ha generado albarán "
                                "de entrada de mercancía.\n", 
                                ("negrita", ))
                        else:
                            escribir(txtvw, "El artículo se recibió en "
                                "el albarán de entrada de abono %s el día "
                                "%s.\n" % (
                                    adeda.numalbaran, 
                                    utils.str_fecha(adeda.fecha)))
                    elif isinstance(objeto, pclases.PartidaCarga):
                        escribir(txtvw, 
                            "Se consumió el %s en la partida de carga %s.\n"%(
                                utils.str_fecha(fecha), 
                                objeto.codigo), 
                            ("_rojoclaro", "cursiva"))
                if articulo.articulo.en_almacen():
                    escribir(txtvw, 
                                  "El artículo está en almacén: %s.\n" % (
                                    articulo.articulo.almacen 
                                        and articulo.articulo.almacen.nombre 
                                        or "¡Error de coherencia en la BD!"), 
                                  ("_verdeclaro", ))
                if (hasattr(articulo, "parteDeProduccionID") 
                    and articulo.parteDeProduccionID):
                    # Ahora también se pueden consumir los Bigbags.
                    pdp = articulo.parteDeProduccion
                    if pdp:
                        if isinstance(articulo, pclases.Bigbag):
                            escribir(txtvw, 
                                "\nBigbag consumido el día %s para producir la"
                                " partida de fibra de cemento embolsado %s."%(
                                    utils.str_fecha(pdp.fecha), 
                                    pdp.partidaCem.codigo), 
                                    ("_rojoclaro", "cursiva"))


    def func_orden_ldds_por_albaran_salida(self, ldd1, ldd2):
        """
        Devuelve -1, 1 ó 0 dependiendo de la fecha de los albaranes de salida
        relacionados con las líneas de devolución. Si las fechas son iguales, 
        ordena por ID de las LDD.
        """
        if ldd1.albaranSalida and (ldd2.albaranSalida == None 
                or ldd1.albaranSalida.fecha < ldd2.albaranSalida.fecha):
            return -1
        if ldd2.albaranSalida and (ldd1.albaranSalida == None 
                or ldd1.albaranSalida.fecha > ldd2.albaranSalida.fecha):
            return 1
        if ldd1.id < ldd2.id:
            return -1
        if ldd1.id > ldd2.id:
            return 1
        return 0

    def mostrar_info_abonos(self, articulo):
        """
        Muestra la información de los abonos del artículo.
        """
        if articulo.lineasDeDevolucion:
            txtvw = self.wids['txt_albaran']
            ldds = articulo.lineasDeDevolucion[:]
            ldds.sort(self.func_orden_ldds_por_albaran_salida)
            for ldd in ldds:
                try:
                    escribir(txtvw, 
                             "Salida del almacén el día %s en el albarán "
                             "%s para %s.\n" % (
                                    utils.str_fecha(ldd.albaranSalida.fecha), 
                                    ldd.albaranSalida.numalbaran, 
                                    ldd.albaranSalida.cliente 
                                        and ldd.albaranSalida.cliente.nombre 
                                        or "?"), 
                             ("_rojoclaro", "cursiva"))
                    escribir(txtvw, 
                             "Devuelto el día %s en el albarán de entrada "
                             "de abono %s.\n" % (
                                utils.str_fecha(
                                    ldd.albaranDeEntradaDeAbono.fecha), 
                                ldd.albaranDeEntradaDeAbono.numalbaran), 
                             ("_verdeclaro", "cursiva"))
                except AttributeError, msg:
                    escribir(txtvw, 
                             "ERROR DE INCONSISTENCIA. Contacte con el "
                             "administrador de la base de datos.\n", 
                             ("negrita", ))
                    txterror="trazabilidad_articulos.py::mostrar_info_abonos"\
                             " -> Excepción capturada con artículo "\
                             "ID %d: %s." % (articulo.id, msg)
                    print txterror
                    self.logger.error(txterror)
            escribir(txtvw, "\n")

    def rellenar_produccion(self, articulo):
        txtvw = self.wids['txt_produccion']
        borrar_texto(txtvw)
        mostrar_parte = True
        if isinstance(articulo, pclases.Bala):
            escribir(txtvw, "Bala número: %s\n" % articulo.numbala)
            escribir(txtvw, "Código de trazabilidad: %s\n" % articulo.codigo)
            escribir(txtvw, "Fecha y hora de fabricación: %s\n" 
                              % articulo.fechahora.strftime('%d/%m/%Y %H:%M'))
            escribir(txtvw, "Peso: %s\n" % (
                        utils.float2str(articulo.pesobala, 1)), ("negrita",))
            escribir(txtvw, "Se extrajo muestra para laboratorio: %s\n" % (
                                articulo.muestra and "Sí" or "No"))
            escribir(txtvw, articulo.claseb and "CLASE B\n" or "")
            escribir(txtvw, "Observaciones: %s\n" % (articulo.motivo or "-"))
        elif isinstance(articulo, pclases.Bigbag):
            escribir(txtvw, "BigBag número: %s\n" % articulo.numbigbag)
            escribir(txtvw, "Código de trazabilidad: %s\n" % articulo.codigo)
            escribir(txtvw, "Fecha y hora de fabricación: %s\n" % 
                                articulo.fechahora.strftime('%d/%m/%Y %H:%M'))
            escribir(txtvw, 
                     "Peso: %s\n" % (utils.float2str(articulo.pesobigbag, 1)), 
                     ("negrita",))
            escribir(txtvw, 
                     "Se extrajo muestra para laboratorio: %s\n" % (
                        articulo.muestra and "Sí" or "No"))
            escribir(txtvw, articulo.claseb and "CLASE B\n" or "")
            escribir(txtvw, "Observaciones: %s\n" % (articulo.motivo or "-"))
        elif isinstance(articulo, (pclases.Rollo, pclases.RolloDefectuoso)):
            escribir(txtvw, "Rollo número: %d\n" % articulo.numrollo)
            escribir(txtvw, "Código de trazabilidad: %s\n" % articulo.codigo)
            escribir(txtvw, 
                     "Fecha y hora de fabricación: %s\n" % 
                        articulo.fechahora.strftime('%d/%m/%Y %H:%M'))
            escribir(txtvw, 
                     "Marcado como defectuoso: %s\n" % (
                      (isinstance(articulo, pclases.RolloDefectuoso) and "Sí") 
                       or (articulo.rollob and "Sí" or "No")
                      )
                    )
            escribir(txtvw, "Observaciones: %s\n" % articulo.observaciones)
            escribir(txtvw, "Se extrajo muestra para laboratorio: %s\n" % (
                                hasattr(articulo, "muestra") 
                                and articulo.muestra and "Sí" or "No"))
            escribir(txtvw, 
                     "Peso: %s\n" % (utils.float2str(articulo.peso, 1)), 
                     ("negrita",))
            escribir(txtvw, 
                     "Densidad: %s\n" % (
                        utils.float2str(articulo.densidad, 1)))
        elif isinstance(articulo, (pclases.BalaCable, pclases.RolloC)):
            escribir(txtvw, "Código de trazabilidad: %s\n" % articulo.codigo)
            escribir(txtvw, "Peso: %s\n" % (utils.float2str(articulo.peso, 1)),
                     ("negrita",))
            escribir(txtvw, 
                     "Observaciones: %s\n" % (articulo.observaciones or "-"))
            escribir(txtvw, 
                     "Fecha y hora de embalado: %s\n" % 
                        utils.str_fechahora(articulo.fechahora))
            mostrar_parte = False   # Más que nada porque específicamente 
                                    # no tienen.
            pdps = buscar_partes_fibra_fecha_y_hora(articulo.fechahora)
            opers = operarios_de_partes(pdps)
            if opers:
                escribir(txtvw, 
                         "\nOperarios del turno en la línea de fibra:\n")
                for oper in opers:
                    escribir(txtvw, 
                             "    %s, %s\n" % (oper.apellidos, oper.nombre))
        else:
            self.logger.error("trazabilidad_articulos.py::rellenar_produccion"
                              " -> Objeto ID %d no es de la clase bala, rollo"
                              " ni bigbag." % (articulo.id))
        if mostrar_parte:
            escribir(txtvw, "\n-----------------------------------\n", 
                     ("cursiva"))
            escribir(txtvw, "Información del parte de producción\n", 
                     ("cursiva"))
            escribir(txtvw, "-----------------------------------\n", 
                     ("cursiva"))
            try:
                pdp = articulo.articulos[0].parteDeProduccion
            except IndexError, msg:
                self.logger.error("ERROR trazabilidad_articulos.py "
                                  "(rellenar_produccion): %s" % (msg))
                pdp = None
            except AttributeError:
                pdp = articulo.parteDeProduccion
            if pdp == None:
                escribir(txtvw, 
                         "¡No se econtró el parte de producción para la "
                         "fabricación del artículo!\n", 
                         ("rojo", ))
            else:
                escribir(txtvw, 
                         "Fecha del parte: %s\n" % utils.str_fecha(pdp.fecha))
                escribir(txtvw, 
                         "Hora de inicio: %s\n" 
                            % pdp.horainicio.strftime('%H:%M'))
                escribir(txtvw, 
                         "Hora de fin: %s\n" % pdp.horafin.strftime('%H:%M'))
                escribir(txtvw, 
                         "Parte verificado y bloqueado: %s\n" % (
                            pdp.bloqueado and "Sí" or "No"))
                escribir(txtvw, "Empleados:\n")
                for ht in pdp.horasTrabajadas:
                    escribir(txtvw, 
                             "\t%s, %s (%s)\n" % (ht.empleado.apellidos, 
                                                  ht.empleado.nombre, 
                                                  ht.horas.strftime('%H:%M')))

    def rellenar_producto(self, articulo):
        """
        articulo es un pclases.Rollo, un pclases.Bala, un pclases.Bigbag o un 
        pclases.BalaCable o un pclases.Pale o un pclases.Caja.
        """
        txtvw = self.wids['txt_producto']
        borrar_texto(txtvw)
        if isinstance(articulo, (pclases.Caja, pclases.Pale)):
            producto = articulo.productoVenta
        else:
            try:
                producto = articulo.articulos[0].productoVenta
            except IndexError, msg:
                self.logger.error("ERROR trazabilidad_articulos.py"
                                  " (rellenar_albaran): %s" % (msg))
                producto = None
        if producto == None:
            escribir(txtvw, 
                     "¡NO SE ENCONTRÓ INFORMACIÓN!\nPosible inconsistencia "
                     "de la base de datos. Contacte con el administrador.")
            self.logger.error("trazabilidad_articulos.py::rellenar_producto"
                              " -> Objeto %s no tiene producto asociado." % (
                                articulo))
        else:
            escribir(txtvw, 
                          "\nCódigo de trazabilidad: %s\n" % articulo.codigo, 
                          ("negrita", ))
            try:
                codigobarras39 = code39.Extended39(articulo.codigo, 
                                            xdim = .070 * cm).guardar_a_png()
                codigobarras39 = gtk.gdk.pixbuf_new_from_file(codigobarras39)
            except Exception, e:
                self.logger.error("trazabilidad_articulos::rellenar_producto"
                                  " -> No se pudo guardar o mostrar el código"
                                  " %s. Excepción: %s" % (articulo.codigo, e))
            else:
                insertar_imagen(txtvw, codigobarras39)
            if isinstance(articulo, pclases.Pale):
                escribir(txtvw, "\nPalé de %d cajas (salidas en rojo):\n\t" 
                                     % len(articulo.cajas))
                cajas = articulo.cajas[:]
                cajas.sort(lambda c1, c2: int(c1.numcaja) - int(c2.numcaja))
                i = 0
                for caja in cajas:
                    codcaja = caja.codigo
                    if caja.en_almacen():
                        escribir(txtvw, codcaja, ("negrita", "cursiva",))
                    else:
                        escribir(txtvw, codcaja, ("negrita","cursiva","rojo"))
                    i += 1
                    if i < len(cajas):
                        escribir(txtvw, ", ")
                    else:
                        escribir(txtvw, "\n\n")
            elif isinstance(articulo, pclases.Caja):
                dict_bolsas = articulo.get_bolsas()
                codsbolsas = ", ".join([dict_bolsas[b]['código'] 
                                        for b in dict_bolsas])
                escribir(txtvw, "\nCaja de %d bolsas: %s\n\n" 
                                     % (articulo.numbolsas, codsbolsas), 
                              ("negrita", "cursiva"))
            self.rellenar_info_producto_venta(producto, txtvw)

    def rellenar_info_producto_venta(self, producto, txtvw):
        """
        Agrega la información del producto al txtvw.
        """
        escribir(txtvw, "\n\t")
        insertar_imagen(txtvw, gtk.gdk.pixbuf_new_from_file(
                                    EanBarCode().getImage(producto.codigo)))
        escribir(txtvw, "\nProducto: ", ("negrita", "azul"))
        escribir(txtvw, "%s\n" % (producto.nombre), 
                      ("negrita", "azul", "grande"))
        escribir(txtvw, "Descripción: %s\n" % (producto.descripcion), 
                      ("negrita"))
        escribir(txtvw, "Código: %s\n" % (producto.codigo))
        escribir(txtvw, "Arancel: %s\n" % (producto.arancel))
        if producto.camposEspecificosRollo != None:
            escribir(txtvw, "Código de Composán: %s\n" % 
                producto.camposEspecificosRollo.codigoComposan)
            escribir(txtvw, "gr/m²: %d\n" % 
                producto.camposEspecificosRollo.gramos)
            escribir(txtvw, "Ancho: %s\n" % (utils.float2str(
                producto.camposEspecificosRollo.ancho, 2)))
            escribir(txtvw, "Diámetro: %d\n" % 
                producto.camposEspecificosRollo.diametro)
            escribir(txtvw, "Metros lineales: %d\n" % 
                producto.camposEspecificosRollo.metrosLineales)
            escribir(txtvw, "Rollos por camión: %d\n" % 
                producto.camposEspecificosRollo.rollosPorCamion)
            escribir(txtvw, "Peso del embalaje: %s\n" % (
                utils.float2str(producto.camposEspecificosRollo.pesoEmbalaje)))
        if producto.camposEspecificosBala != None:
            escribir(txtvw, "Material: %s\n" % (
                producto.camposEspecificosBala.tipoMaterialBala and 
                producto.camposEspecificosBala.tipoMaterialBala.descripcion or 
                "-"))
            escribir(txtvw, "DTEX: %s\n" % (utils.float2str(
                producto.camposEspecificosBala.dtex)))
            escribir(txtvw, "Corte: %d\n" % (
                producto.camposEspecificosBala.corte))
            escribir(txtvw, "Color: %s\n" % (
                producto.camposEspecificosBala.color))
            escribir(txtvw, "Antiuv: %s\n" % (
                producto.camposEspecificosBala.antiuv and "SÍ" or "NO"))
        if producto.camposEspecificos != []:
            escribir(txtvw, "Campos definidos por el usuario:\n")
            for cee in producto.camposEspecificos:
                escribir(txtvw, "\t%s: %s\n" % (cee.nombre, cee.valor))
        if producto.camposEspecificosEspecial != None:
            escribir(txtvw, "Stock: %s\n" % (
                utils.float2str(producto.camposEspecificosEspecial.stock)))
            escribir(txtvw, "Existencias: %s\n" % (utils.float2str(
                producto.camposEspecificosEspecial.existencias, 0)))
            escribir(txtvw, "Unidad: %s\n" % (
                producto.camposEspecificosEspecial.unidad))
            escribir(txtvw, "Observaciones: %s\n" % (
                producto.camposEspecificosEspecial.observaciones))

def borrar_texto(txt):
    txt.get_buffer().set_text('')
    
def insertar_imagen(txt, imagen):
    """
    Inserta una imagen en el TextView txt en la 
    posición actual del texto.
    """
    buff = txt.get_buffer()
    mark = buff.get_insert()
    itr = buff.get_iter_at_mark(mark)
    buff.insert_pixbuf(itr, imagen)
    buff.insert_at_cursor("\n")

def buscar_partes_fibra_fecha_y_hora(fechahora):
    """
    Busca los partes de fibra que hubiera en la fecha y hora recibida.
    Devuelve una lista con todos ellos.
    """
    pdps = pclases.ParteDeProduccion.select(pclases.AND(
            pclases.ParteDeProduccion.q.fechahorainicio <= fechahora, 
            pclases.ParteDeProduccion.q.fechahorafin >= fechahora))
    res = []
    for pdp in pdps:
        if pdp.es_de_fibra():
            res.append(pdp)
    return res

def operarios_de_partes(partes):
    """
    Recibe una lista de partes de producción y devuelve 
    otra lista con los operarios de los mismos.
    """
    opers = []
    for pdp in partes:
        for ht in pdp.horasTrabajadas:
            if ht.empleado not in opers:
                opers.append(ht.empleado)
    return opers
    
def escribir(txt, texto, estilos = ()):
    """
    Escribe "texto" en el buff del TextView "txt".
    """
    buff = txt.get_buffer()
    if estilos == ():
        buff.insert_at_cursor(texto)
    else:
        import pango
        iter_insert = buff.get_iter_at_mark(buff.get_insert())
        tag = buff.create_tag()
        if "negrita" in estilos:
            tag.set_property("weight", pango.WEIGHT_BOLD)
            #tag.set_property("stretch", pango.STRETCH_ULTRA_EXPANDED)
        if "cursiva" in estilos:
            tag.set_property("style", pango.STYLE_ITALIC)
        if "rojo" in estilos:
            tag.set_property("foreground", "red")
        if "azul" in estilos:
            tag.set_property("foreground", "blue")
        if "_rojoclaro" in estilos:
            tag.set_property("background", "pale violet red")
        if "_verdeclaro" in estilos:
            tag.set_property("background", "pale green")
        if "grande" in estilos:
            tag.set_property("size_points", 14)
        buff.insert_with_tags(iter_insert, texto, tag)



if __name__ == '__main__':
    t = TrazabilidadArticulos(usuario = pclases.Usuario.get(1))
    
