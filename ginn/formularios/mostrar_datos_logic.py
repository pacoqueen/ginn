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
## mostrar_datos_logic.py - Muestra los datos de LOGIC en crudo.
###################################################################
## NOTAS:
## 
## 
###################################################################
## Changelog:
## 23 de mayo de 2006 -> Inicio
##  
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import sys, os
import sqlobject
import gtk, gtk.glade, time
try:
    import pclases
except ImportError:
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    import pclases
import mx.DateTime
import csv
import time
from ventana_progreso import VentanaProgreso
try:
    import psycopg
except ImportError:
    import psycopg2 as psycopg
import pango
from utils import _float as float
try:
    from psycopg import ProgrammingError as psycopg_ProgrammingError
except ImportError:
    from psycopg2 import ProgrammingError as psycopg_ProgrammingError



class MostrarDatosLogic(Ventana):
    def __init__(self, objeto = None, consulta = "", padre = None, usuario = None):
        """
        consulta es la parte *interna* de la consulta cuyos resultados
        se mostrarán en la búsqueda. Es decir, pclases.LogicMovimientos.select(->consulta<-).
        self.objeto guarda el objeto seleccionado en la ventana y que se puede
        recuperar mediante .get_objeto. Se asigna objeto a self.objeto inicialmente, 
        por lo que puede valer de valor por defecto en caso de que se salga 
        de la ventana sin seleccionar ningún resultado.
        """
        if str(consulta) == "":
            Logic = pclases.LogicMovimientos
            self.consulta = pclases.AND(Logic.q.importe >= 0, 
                                        Logic.q.contrapartidaInfo == '',
                                        pclases.OR(Logic.q.codigoCuenta.startswith('400'), 
                                                   Logic.q.codigoCuenta.startswith('403'),
                                                   Logic.q.codigoCuenta.startswith('410')),
                                        pclases.NOT(Logic.q.comentario.startswith("Apertura Ejercicio")) ) 
        else:
            self.consulta = consulta
        Ventana.__init__(self, 'mostrar_datos_logic.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_limpiar/clicked': self.limpiar,
                       'b_aplicar/clicked': self.aplicar,
                       'b_select/clicked': self.aceptar,
                       'tb_expand/toggled': self.expandircontraer,
                       'tb_ver/toggled': self.cambiar_vista}
        self.add_connections(connections)
        if padre != None:
            self.wids['ventana'].set_transient_for(padre)
            self.wids['ventana'].set_modal(padre != None)
        self.wids['txt_sqlobject'].get_buffer().connect("changed", self.limpiar_criterios_manuales)
        cols = (('ID', 'gobject.TYPE_STRING', False, True, False, None),
                ('asiento', 'gobject.TYPE_STRING', False, True, True, None),
                ('orden', 'gobject.TYPE_STRING', False, True, False, None),
                ('fecha', 'gobject.TYPE_STRING', False, True, False, None),
                ('cargoAbono', 'gobject.TYPE_STRING', False, True, False, None),
                ('codigoCuenta', 'gobject.TYPE_STRING', False, True, False, None),
                ('cuenta', 'gobject.TYPE_STRING', False, True, False, None),
                ('contrapartidaInfo', 'gobject.TYPE_STRING', False, True, False, None),
                ('comentario', 'gobject.TYPE_STRING', False, True, False, None),
                ('importe', 'gobject.TYPE_STRING', False, True, False, None),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_logic'], cols)
        self.wids['tv_logic'].set_expander_column(self.wids['tv_logic'].get_column(5))
        self.wids['tv_logic'].connect("row-activated", self.seleccionar_fila)
        font = pango.FontDescription("Monospace 9")
        self.wids['txt_sqlobject'].modify_font(font)
        self.vpro = VentanaProgreso(padre = self.wids['ventana'])
        self.rellenar_logic()
        col = self.wids['tv_logic'].get_column(9)
        for cell in col.get_cell_renderers():
            cell.set_property('xalign', 1.0)
        gtk.main()

    def chequear_cambios(self):
        pass

    def rellenar_logic(self):
        try:
            self.wids['txt_sqlobject'].get_buffer().set_text("%s" % (self.consulta))
        except AssertionError, msg:
            self.wids['txt_sqlobject'].get_buffer().set_text("AssertionError: %s" % msg)
        self.vpro.mostrar()
        model = self.wids['tv_logic'].get_model()
        # Las siguientes 3 líneas son para acelerar la inserción de datos en el TreeView
        # self.wids['tv_logic'].set_property ('fixed-height-mode', True) # FIXME: Falla un assert. Ya lo miraré.
        self.wids['tv_logic'].freeze_child_notify()
        self.wids['tv_logic'].set_model(None)
        model.clear()
        i = 0.0
        try:
            if self.consulta.__str__() == "": self.consulta = None
                # OJO: En todas las comparaciones de self.consulta usar el método .__str__().
            ls = pclases.LogicMovimientos.select(self.consulta, orderBy="id")
            nousados = self.wids['ch_nousados'].get_active()
            tot = ls.count()
            padres = {}
            cuenta = 0
            for l in ls:
                self.vpro.set_valor(i/tot, "Mostrando asiento %s..." % l.get_codigo())
                i += 1
                if nousados and l.pagos != []:
                    continue  # No añado asientos usados en pagos si está marcada la casilla de mostrar solo no usados.
                if l.codigoCuenta[:3] not in padres.keys():
                    padres[l.codigoCuenta[:3]] = model.append(None, ("", 
                                                                     "", 
                                                                     "", 
                                                                     "", 
                                                                     "", 
                                                                     "%s." % l.codigoCuenta[:3],
                                                                     "",
                                                                     "", 
                                                                     "", 
                                                                     "", 
                                                                     0))
                model.append(padres[l.codigoCuenta[:3]], (l.id, 
                                                          l.asiento, 
                                                          l.orden, 
                                                          utils.str_fecha(l.fecha), 
                                                          l.cargoAbono,
                                                          l.codigoCuenta,
                                                          l.cuenta,
                                                          l.contrapartidaInfo,
                                                          l.comentario,
                                                          utils.float2str(l.importe),
                                                          l.id))
                cuenta += 1
            self.wids['e_count'].set_text("%d" % cuenta)
        finally:
            self.wids['tv_logic'].set_model(model)
            self.expandircontraer(self.wids['tb_expand'])
            self.wids['tv_logic'].thaw_child_notify()
            self.vpro.ocultar()

    def expandircontraer(self, tb):
        if tb.get_active():
            self.wids['tb_expand'].set_label("Árbol expandido")
            self.wids['tv_logic'].expand_all()
        else:
            self.wids['tb_expand'].set_label("Árbol contraído")
            self.wids['tv_logic'].collapse_all()

    def cambiar_vista(self, tb):
        mostrar = not tb.get_active()    # Pulsado = vista simple
        tb.set_label(mostrar and "Vista completa" or "Vista simplificada")
        for numcol in (0, 1, 2, 4, 7):
            columna = self.wids['tv_logic'].get_column(numcol)
            columna.set_visible(mostrar)

    def limpiar_criterios_manuales(self, txtbuff):
        self.wids['e_cuenta'].set_text('')
        self.wids['e_nomcuenta'].set_text('')
        self.wids['e_comentario'].set_text('')

    def limpiar(self, b):
        self.wids['e_cuenta'].set_text('')
        self.wids['e_nomcuenta'].set_text('')
        self.wids['e_comentario'].set_text('')
        self.wids['txt_sqlobject'].get_buffer().set_text('')
        self.consulta = ""

    def aplicar(self, b):
        cuenta = self.wids['e_cuenta'].get_text()
        nomcuenta = self.wids['e_nomcuenta'].get_text()
        comentario = self.wids['e_comentario'].get_text()
        consultabak = self.consulta
        if cuenta != "" or comentario != "" or nomcuenta != '':
            Logic = pclases.LogicMovimientos
            # Construir esa consulta
            buffer = self.wids['txt_sqlobject'].get_buffer()
            bini, bfin = buffer.get_bounds()
            consulta = buffer.get_text(bini, bfin)
            if consulta != "": 
                self.consulta = pclases.AND(Logic.q.importe >= 0, 
                                            Logic.q.contrapartidaInfo == '',
                                            pclases.OR(Logic.q.codigoCuenta.startswith('400'), 
                                                       Logic.q.codigoCuenta.startswith('403'),
                                                       Logic.q.codigoCuenta.startswith('410')),
                                            pclases.NOT(Logic.q.comentario.startswith("Apertura Ejercicio")) ) 
                # Me mantengo en el rango de las cuentas 400, 403, 410 a no ser que se indique específicamente 
                # (editando el cuadro inferior de la consulta sqlobject) que se va a buscar en toda la tabla.
            else:   # Ha limpiado todos los campos. Quiere buscar en TODA la tabla:
                self.consulta = pclases.AND(Logic.q.importe >= 0, Logic.q.contrapartidaInfo == '')
                # NOTA: Un apunte de Logic que se importó con contrapartidaInfo == '' se mantendrá así aunque 
                # una vez usado en un pago y anotado en la contabilidad de Logic se vuelva a importar, ya que
                # se vigila que los apuntes no existan usando cuenta, asiento y orden. Por tanto, ese mismo 
                # asiento, que ya en Logic tiene algo en contrapartidaInfo, se saltará en la importación.
            if cuenta != "":
                if "." in cuenta:   # Sustituir por los 0 que haga falta hasta longitud 9 (notación contable)
                    cuenta = cuenta.replace('.', '0'*(9-len(cuenta)+1))
                self.consulta = pclases.AND(self.consulta, Logic.q.codigoCuenta.contains(cuenta))
            if nomcuenta != "":
                self.consulta = pclases.AND(self.consulta, Logic.q.cuenta.contains(nomcuenta))
            if comentario != "":
                self.consulta = pclases.AND(self.consulta, Logic.q.comentario.contains(comentario))
        else:
            # Ejecutar la del cuadro de texto
            buffer = self.wids['txt_sqlobject'].get_buffer()
            bini, bfin = buffer.get_bounds()
            consulta = buffer.get_text(bini, bfin)
            self.consulta = consulta
        try:
            self.rellenar_logic()
        except psycopg_ProgrammingError, msg:
            LENLINEA = 240
            msg = msg.__str__()
            for i in xrange(len(msg)/LENLINEA):
                pos = (i+1)*LENLINEA
                msg = msg[:pos]+"\n"+msg[pos:]
            self.vpro.ocultar()
            utils.dialogo_info(titulo = "ERROR EN LA CONSULTA", 
                               texto = """
            Ocurrió un error al ejecutar la búsqueda.
            
            Se restauró la consulta anterior.
            Vuelva a pulsar en «Aplicar» para actualizar o introduzca nuevos valores para la consulta.
            
            DEBUG:
            %s""" % msg, 
                               padre = self.wids['ventana'])
            self.consulta = consultabak
            buffer.set_text("%s" % self.consulta)

    def get_objeto(self):
        return self.objeto

    def seleccionar_fila(self, treeview, path, view_column):
        self.aceptar(None)

    def aceptar(self, boton):
        res = None
        model, iter = self.wids['tv_logic'].get_selection().get_selected()
        if iter != None:
            id = model[iter][-1]
            res = pclases.LogicMovimientos.get(id)
            self.wids['ventana'].destroy()
        else:
            utils.dialogo(titulo = "¿CERRAR?", 
                          texto = "No ha seleccionado ningún asiento.\n¿Desea cerrar la ventana?",
                          padre = self.wids['ventana'])
        self.objeto = res
        return res

if __name__ == '__main__':
    t = MostrarDatosLogic()
    print t.get_objeto()

