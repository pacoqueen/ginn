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
## consulta_marcado_ce.py -- Consulta de marcado CE de geotextiles.
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 22 de marzo de 2006 -> Inicio
## 
###################################################################
## TODO: Barra de progreso o algo, porque se hace bastante pesado 
## tanto buscar partidas como imprimirlas.
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
import ventana_progreso
import re
from utils import _float as float

class ConsultaMarcadoCE(Ventana):
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
        Ventana.__init__(self, 'consulta_marcado_ce.glade', objeto, 
                         usuario = self.usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar_partidas/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir, 
                       'b_fechaini/clicked': self.set_fecha, 
                       'b_fechafin/clicked': self.set_fecha}
        self.add_connections(connections)
        cols = (('Partida', 'gobject.TYPE_STRING', False, True, True, None),
                ('Código', 'gobject.TYPE_STRING', False, True, False, None),
                ('Fecha inicio fabricación', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Producto', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Observaciones', 'gobject.TYPE_STRING', 
                    False, True, False, None), 
                ('id', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(self.wids['tv_partidas'], cols)
        self.wids['tv_partidas'].connect("row-activated", 
                                         self.abrir_resultados_partida)
        self.wids['tv_partidas'].get_selection().set_mode(
                                                    gtk.SELECTION_MULTIPLE)
        utils.rellenar_lista(self.wids['cbe_producto'], 
            [(-1, "Todos los geotextiles")] 
            + [(p.id, p.descripcion) for p in pclases.ProductoVenta.select(
                    pclases.ProductoVenta.q.camposEspecificosRolloID != None, 
                orderBy = "descripcion")])
        self.wids['e_fechaini'].set_text(
            utils.str_fecha(mx.DateTime.localtime() - mx.DateTime.oneWeek * 2))
        self.wids['e_fechafin'].set_text(
            utils.str_fecha(mx.DateTime.localtime()))
        gtk.main()

    def abrir_resultados_partida(self, tv, path, view_col):
        """
        Abre la ventana del laboratorio de resultados de la 
        partida de la fila a la que se ha hecho doble clic.
        """
        idpartida = tv.get_model()[path][-1]
        import resultados_geotextiles
        ventana = resultados_geotextiles.ResultadosGeotextiles(
                    pclases.Partida.get(idpartida), 
                    usuario = self.usuario)

    def set_fecha(self, boton):
        """
        Muestra un calendario y pone la fecha seleccionada en el entry 
        que le corresponde al botón pulsado.
        """
        nombreboton = boton.get_name()
        if nombreboton == "b_fechaini":
            entry = self.wids["e_fechaini"]
        elif nombreboton == "b_fechafin":
            entry = self.wids["e_fechafin"]
        else:
            return
        fecha = utils.mostrar_calendario(
            fecha_defecto = utils.parse_fecha(entry.get_text()), 
            padre = self.wids['ventana'])
        entry.set_text(utils.str_fecha(fecha))

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, partidas):
    	"""
        Rellena el model con los items de la consulta.
        Elementos es un diccionario con objetos fecha como claves y 
        un diccionaro de dos elementos como valor. El segundo diccionario
        debe tener tres claves: 'pagos', 'vencimientos' y 'logic'. En cada
        una de ellas se guarda una lista de objetos de la clase 
        correspondiente.
        """        
    	model = self.wids['tv_partidas'].get_model()
    	model.clear()
    	for partida in partidas:
            producto = partida.get_producto()
            model.append((partida.numpartida, 
                          partida.codigo, 
                          utils.str_fecha(partida.get_fecha_fabricacion()), 
                          producto and producto.descripcion or "?", 
                          partida.observaciones, 
                          partida.id))
        
    def buscar(self, boton):
        idproducto = utils.combo_get_value(self.wids['cbe_producto'])
        fechaini = utils.parse_fecha(self.wids['e_fechaini'].get_text())
        fechafin = utils.parse_fecha(self.wids['e_fechafin'].get_text())
        if idproducto > 1:
            try:
                producto = pclases.ProductoVenta.get(idproducto)
            except:
                utils.dialogo_info(titulo = "ERROR", 
                    texto = "El producto seleccionado no se encontró.\n"
                            "Probablemente fue eliminado.\nCierre y vuelva "
                            "a abrir esta ventana antes de volver a "
                            "intentarlo.", 
                    padre = self.wids['ventana'])
            else:
                partidas = producto.get_partidas(fechaini = fechaini, 
                                                 fechafin = fechafin)
                if pclases.DEBUG:
                    print "consulta_marcado_ce.py::len(partidas", len(partidas)
                if self.wids['ch_gramaje'].get_active():
                    gramaje = producto.camposEspecificosRollo.gramos
                    cers = pclases.CamposEspecificosRollo.select(
                            pclases.CamposEspecificosRollo.q.gramos == gramaje)
                    for cer in cers:
                        try:
                            cerproducto = cer.productosVenta[0]
                        except IndexError, msg:
                            txt = "%sconsulta_marcado_ce::buscar -> "\
                                  "El registro CER ID %d no tiene producto "\
                                  "asociado. Mensaje de la excepción: %s" % (
                                    self.usuario 
                                        and self.usuario.usuario + ": " or "", 
                                    cer.id, msg)
                            print txt
                            self.logger.error(txt)
                            continue
                        if cerproducto != producto:   # Porque ya lo he 
                                                      # contado antes
                            for partida in cerproducto.get_partidas():
                                if (partida not in partidas 
                                    and fechaini 
                                        <= partida.get_fecha_fabricacion() 
                                        <= fechafin):
                                    partidas.append(partida)
                self.rellenar_tabla(partidas)
        elif idproducto == -1 or idproducto == None:    # -1 si ha marcado 
            # "Todos". None si no ha marcado nada.
            # partidas = pclases.Partida.select()
            # En lugar de filtrar todas las partidas, como será lento de 
            # pelotas y al final con lo que se van a comparar las fechas es 
            # con las de los partes de producción (ver 
            # Partida.get_fecha_fabricacion), lo que hago es buscar primero 
            # los partes de producción entre esas fechas, y a partir de ahí 
            # filtro todas sus partidas -ahora shi- por fecha.
            # OJO: Si cambia el critero de get_fecha_fabricacion (cosa harto 
            # improbable, porque si no es del parte... ¿de dónde voy a sacar 
            # la fecha de fabricación de una partida si no?) o el formato 
            # (devuelvo fechahora en vez de fecha absoluta, por ejemplo) hay 
            # que cambiar esta rutina.
            pdps = pclases.ParteDeProduccion.select(pclases.AND(
                    pclases.ParteDeProduccion.q.fechahorainicio >= fechaini, 
                    pclases.ParteDeProduccion.q.fechahorafin 
                        < fechafin + mx.DateTime.oneDay))
            partidas = []
            for pdp in pdps:
                if pdp.es_de_geotextiles() and len(pdp.articulos) > 0:
                    partida = pdp.articulos[0].partida
                    if partida not in partidas:
                        partidas.append(partida)
            # Y vuelvo a filtrar para asegurarme de que las fechas son 
            # correctas y entran en el rango:
            tmp = []
            for p in partidas:
                ffab = p.get_fecha_fabricacion()
                if ffab != None and fechaini <= ffab <= fechafin:
                    tmp.append(p)
            partidas = tmp
            self.rellenar_tabla(partidas)
        else:
            utils.dialogo_info(titulo = "SELECCIONE UN PRODUCTO", 
                texto = "Debe seleccionar un producto en el desplegable.", 
                padre = self.wids['ventana'])

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe.
        """
        from tempfile import gettempdir
        import os

        if self.wids['b_exportar'].get_active():
            ruta_csv = os.path.join(gettempdir(), 
                "csv_marcado_%s" % mx.DateTime.localtime().strftime("%Y%m%d"))
        else:
            ruta_csv = None
        if self.wids['tv_partidas'].get_selection().count_selected_rows() == 0:
            utils.dialogo_info(titulo = "SELECCIONE PARTIDAS", 
                               texto = "Debe seleccionar al menos una partida."
                                       "\nPuede usar la tecla Ctrl. y Shift "
                                       "para seleccionar varias\npartidas o un"
                                       " rango, respectivamente.", 
                               padre = self.wids['ventana'])
        else:
            idproducto = utils.combo_get_value(self.wids['cbe_producto'])
            if idproducto > 1:
                try:
                    producto = pclases.ProductoVenta.get(idproducto)
                except:
                    utils.dialogo_info(titulo = "ERROR", 
                                       texto = "El producto seleccionado no se"
                                               " encontró.\nProbablemente fue"
                                               " eliminado.\nCierre y vuelva "
                                               "a abrir esta ventana antes de"
                                               " volver a intentarlo.", 
                                       padre = self.wids['ventana'])
                else:
                    sel = self.wids['tv_partidas'].get_selection()
                    model, paths = sel.get_selected_rows()
                    partidas = [pclases.Partida.get(model[path][-1]) 
                                for path in paths]
                    from informes import abrir_pdf
                    abrir_pdf(
                      geninformes.informe_marcado_ce(producto, 
                        partidas, 
                        ventana_padre = self.wids['ventana'], 
                        ignorar_errores=self.wids['ch_gramaje'].get_active(), 
                        exportar_a_csv_a = ruta_csv))
            elif idproducto == -1 or idproducto == None:
                sel = self.wids['tv_partidas'].get_selection()
                model, paths = sel.get_selected_rows()
                partidas = [pclases.Partida.get(model[path][-1]) 
                            for path in paths]
                from informes import abrir_pdf
                # Agrupo por productos y saco un informe de cada uno (porque 
                # si no los datos estadísticos se mezclarían y saldrían 
                # falseados).
                por_gramaje = {}
                for p in partidas:
                    producto = p.get_producto()
                    gramaje = producto.camposEspecificosRollo.gramos
                    if gramaje not in por_gramaje:
                        por_gramaje[gramaje] = {'productos': [producto], 
                                                'partidas' : [p]}
                    else:
                        por_gramaje[gramaje]['productos'].append(producto)
                        if p not in por_gramaje[gramaje]['partidas']:
                            por_gramaje[gramaje]['partidas'].append(p)
                for gramaje in por_gramaje:
                    def contar_apariciones(l):
                        d = {}
                        for i in l:
                            if i not in d: d[i] = l.count(i)
                        return d
                    apariciones = contar_apariciones(por_gramaje[gramaje]['productos'])
                    prod_mas_repetido = max([(apariciones[producto], producto) for producto in apariciones])[1]
                    abrir_pdf(geninformes.informe_marcado_ce(prod_mas_repetido, 
                                             por_gramaje[gramaje]['partidas'], 
                                         ventana_padre = self.wids['ventana'], 
                                                       ignorar_errores = True,
                                                  exportar_a_csv_a = ruta_csv))


if __name__ == '__main__':
    t = ConsultaMarcadoCE()

