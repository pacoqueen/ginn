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
## busca_partida.py 
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

class BuscaPartida(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'busca_partida.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_ayuda/clicked': self.ayuda}
        self.add_connections(connections)
        cols = (('Num. Partida', 'gobject.TYPE_INT64', 
                    False, True, False, None),
                ('Código', 'gobject.TYPE_STRING', False, True, False, None),
                ('Longitudinal', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Transversal', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Compresión', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Perforación', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Permeabilidad', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Poros', 'gobject.TYPE_STRING', False, True, False, None),
                ('Espesor', 'gobject.TYPE_STRING', False, True, False, None),
                ('Piramidal', 'gobject.TYPE_STRING', False, True, False, None),
                ('Idpartida', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_resultado'], cols)
        combos = ('cmb_longitudinal', 'cmb_transversal', 'cmb_compresion', 
                  'cmb_perforacion', 'cmb_permeabilidad', 'cmb_poros', 
                  'cmb_piramidal', 'cmb_espesor')
        for c in combos:
            utils.rellenar_lista(self.wids[c], 
                enumerate(("<", "<=", "=", ">=", ">", "<>")))
                # [(0, '<'), (1, '='), (2, '>')])
            utils.combo_set_from_db(self.wids[c], 2)
        
        utils.rellenar_lista(self.wids['cmbe_producto'], 
            [(p.id, p.descripcion) 
             for p in pclases.ProductoVenta.select(
                pclases.ProductoVenta.q.camposEspecificosRolloID != None, 
                orderBy = 'descripcion')
            ])
        self.rellenar_tabla()
        # Valores por defecto:
        self.wids['e_longitudinal'].set_text('0')
        self.wids['e_transversal'].set_text('0')
        self.wids['e_compresion'].set_text('0')
        self.wids['e_perforacion'].set_text('0')
        self.wids['e_permeabilidad'].set_text('0')
        self.wids['e_poros'].set_text('0')
        self.wids['e_piramidal'].set_text('0')
        self.wids['e_espesor'].set_text('0')
        self.wids['chk_longitudinal'].set_active(True)
        self.wids['chk_transversal'].set_active(True)
        self.wids['chk_compresion'].set_active(True)
        self.wids['chk_perforacion'].set_active(True)
        self.wids['chk_permeabilidad'].set_active(True)
        self.wids['chk_poros'].set_active(True)
        self.wids['chk_piramidal'].set_active(False)
        self.wids['chk_espesor'].set_active(True)
        self.wids['chk_producto'].set_active(True)
        gtk.main()


    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, lista = []):
        """
        Rellena el model con los resultados de la búsqueda almacenados
        en una lista de partidas.
        """        
        model = self.wids['tv_resultado'].get_model()
        model.clear()
        for elem in lista:
            model.append((elem.numpartida,
                    elem.codigo,
                    "%.2f" % elem.longitudinal,
                    "%.2f" % elem.transversal,
                    "%.2f" % elem.compresion,
                    "%.2f" % elem.perforacion,
                    "%.2f" % elem.permeabilidad,
                    "%.2f" % elem.poros,
                    "%.2f" % elem.espesor,
                    "%.2f" % elem.piramidal,
                    elem.id))
    
    def buscar(self, boton):
        """
        Realiza una búsqueda de lotes sobre los parámetros activados mediante
        los checkboxes cuyos datos coincidad con el contenido de los entries
        """
        from ventana_progreso import VentanaProgreso
        if self.wids['chk_producto'].get_active():
            idproducto = utils.combo_get_value(self.wids['cmbe_producto'])
            if idproducto == None:
                utils.dialogo_info(titulo = 'ERROR', 
                    texto = 'Si desea hacer una búsqueda con filtrado por '
                            'producto, debe seleccionar uno', 
                    padre = self.wids['ventana'])
                return
            
            # Optimizacion de la búsqueda
            articulos = pclases.Articulo.select(pclases.AND(
                pclases.Articulo.q.albaranSalidaID == None,
                pclases.Articulo.q.productoVentaID == idproducto))
        else:
            articulos = pclases.Articulo.select(pclases.AND(
                pclases.Articulo.q.albaranSalidaID == None, 
                pclases.Articulo.q.rolloID != None))
        # TODO: Creo que se pueden agilizar un poco más las consultas. 
        partidaids = []
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar() 
        i = 0.0
        tot = articulos.count()
        for a in articulos:
            partidaid = ((a.rollo and a.rollo.partidaID) 
                         or (a.rolloDefectuoso 
                             and a.rolloDefectuoso.partidaID) 
                         or None)
            if partidaid != None:
                if partidaid not in partidaids:
                    partidaids.append(partidaid)
            else:
                txt = "%sbusca_partida::buscar -> "\
                      "Artículo rollo o rolloDefectuoso sin partida:"\
                      " ID %d." % (self.usuario 
                                    and self.usuario.usuario + ": " or "", 
                                   a.id)
                if pclases.DEBUG:
                    print txt
            vpro.set_valor(i/tot, 'Buscando en el almacén...')
            i += 1
        vpro.ocultar()
        criterio = True
        campos = ('chk_longitudinal', 'chk_transversal', 'chk_compresion', 
                  'chk_perforacion', 'chk_permeabilidad', 'chk_poros', 
                  'chk_piramidal', 'chk_espesor')
        for c in campos:
            if self.wids[c].get_active():
                valorCombo = utils.combo_get_value(self.wids['cmb'+c[3:]])
                if valorCombo == 0:
                    operador = ' < '
                elif valorCombo == 1:
                    operador = ' <= '
                elif valorCombo == 2:
                    operador = ' == '
                elif valorCombo == 3:
                    operador = ' >= '
                elif valorCombo == 4:
                    operador = ' > '
                elif valorCombo == 5:
                    operador = ' != '
                cadena = ('pclases.AND(criterio, pclases.Partida.q.' 
                          + c[4:] + operador 
                          + 'self.wids[\'e'+c[3:]+'\'].get_text())')
                criterio = eval(cadena)
        partidas = pclases.Partida.select(criterio)
        resultado = [p for p in partidas if p.id in partidaids]
        self.rellenar_tabla(resultado)

    def ayuda(self, boton):
        """
        Muestra un cuadro de ayuda
        """
        utils.dialogo_info(texto = "Seleccione que criterios de búsqueda "
                                   "que quiere utilizar con las casillas "
                                   "de verificación.\nLa búsqueda sólo "
                                   "filtrará los datos introducidos cuya "
                                   "casilla esté activa", 
                           titulo = 'AYUDA', 
                           padre = self.wids['ventana'])


if __name__ == '__main__':
    b = BuscaPartida()    
