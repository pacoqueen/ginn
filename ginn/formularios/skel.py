#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado,                   #
#                          (pacoqueen@users.sourceforge.net                   #
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
## skel.py - Esqueleto para ventanas.
###################################################################
## NOTAS:
##  Usar ESTA ventana a partir de ahora para crear nuevas.
##  Hereda de ventana y ventana genérica, y la mayoría de funciones
##  están automatizadas partiendo tan solo de la clase y un 
##  diccionario que empareje widgets y atributos.
## ----------------------------------------------------------------
##  
###################################################################
## Changelog:
## 17 de diciembre de 2007 -> Inicio
## 
###################################################################

import sys, os
from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk, time, mx.DateTime
try:
    from framework import pclases
    from framework.seeker import VentanaGenerica 
except ImportError:
    from framework import pclases
    from framework.seeker import VentanaGenerica 
from utils import _float as float

# TODO: Meter los registros de Auditoría.[nuevo|borrado|modificado] aquí también.

class XXXSkel(Ventana, VentanaGenerica):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self.clase = pclases.XXXClaseDePclases
        self.dic_campos = {"XXXcampo_de_pclases": "XXXnombre_del_widget_en_glade", 
                          }
        Ventana.__init__(self, 'XXXfichero_glade.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_nuevo/clicked': self.nuevo,
                       'b_borrar/clicked': self.borrar,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_buscar/clicked': self.buscar,
                       # XXX: Más widgets y señales si se necesitan.
                      }  
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        gtk.main()

    def es_diferente(self):
        """
        Devuelve True si algún valor en ventana difiere de 
        los del objeto.
        """
        if self.objeto == None:
            igual = True
        else:
            igual = self.objeto != None
            for colname in self.dic_campos:
                col = self.clase.sqlmeta.columns[colname]
                try:
                    valor_ventana = self.leer_valor(col, self.dic_campos[colname])
                except (ValueError, mx.DateTime.RangeError, TypeError):
                    igual = False
                valor_objeto = getattr(self.objeto, col.name)
                if isinstance(col, pclases.SODateCol):
                    valor_objeto = utils.abs_mxfecha(valor_objeto)
                igual = igual and (valor_ventana == valor_objeto)
                if not igual:
                    break
        return not igual
    
    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        # Inicialmente no se muestra NADA. Sólo se le deja al
        # usuario la opción de buscar o crear nuevo.
        self.activar_widgets(False)
        self.wids['b_actualizar'].set_sensitive(False)
        self.wids['b_guardar'].set_sensitive(False)
        self.wids['b_nuevo'].set_sensitive(True)
        self.wids['b_buscar'].set_sensitive(True)
        # Inicialización del resto de widgets:
        # XXX: Aquí generalmente se inicializan los TreeViews y combos.
        cols = (('XXXNombreCol', 'gobject.TYPE_STRING', XXXEditable, XXXOrdenable, XXXBuscable, XXXCallbackEdicion),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
                # La última columna (oculta en la Vista) siempre es el id.
        utils.preparar_listview(self.wids['XXXtv_treeview'], cols)
        utils.rellenar_lista(self.wids['XXXcbe_comboboxentry'], 
                             [(p.id, p.XXXcampo) for p in 
                                pclases.XXXClase.select(orderBy = "XXXcampo")])

    def activar_widgets(self, s, chequear_permisos = True):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        if self.objeto == None:
            s = False
        ws = tuple(["XXXWidgets_que_no_tengan_«adaptador»_en_el_diccionario_del_constructor", "XXXtv_treeview", "b_borrar"] + [self.dic_campos[k] for k in self.dic_campos.keys()])
            # XXX: b_nuevo y b_buscar no se activan/desactivan aquí, sino en el
            #      chequeo de permisos.
        for w in ws:
            try:
                self.wids[w].set_sensitive(s)
            except Exception, msg:
                print "Widget problemático:", w, "Excepción:", msg
                import traceback
                traceback.print_last()
        if chequear_permisos:
            self.check_permisos(nombre_fichero_ventana = "XXXskel.py")

    def refinar_resultados_busqueda(self, resultados):
        """
        Muestra en una ventana de resultados todos los
        registros de "resultados".
        Devuelve el id (primera columna de la ventana
        de resultados) de la fila seleccionada o None
        si se canceló.
        """
        filas_res = []
        for r in resultados:
            filas_res.append((r.id, r.XXXcampo1, r.XXXcampo2))
        ide = utils.dialogo_resultado(filas_res,
                                     titulo = 'SELECCIONE XXXLO_QUE_SEA',
                                     cabeceras = ('ID', 'XXXCampo1', 'XXXCampo2'), 
                                     padre = self.wids['ventana'])
        if id < 0:
            return None
        else:
            return id

    def rellenar_widgets(self):
        """
        Introduce la información del objeto actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        XXXobjeto = self.objeto
        for nombre_col in self.dic_campos:
            self.escribir_valor(XXXobjeto.sqlmeta.columns[nombre_col], getattr(XXXobjeto, nombre_col), self.dic_campos[nombre_col])
        self.rellenar_tabla_XXX()
        self.objeto.make_swap()

    def rellenar_tabla_XXX(self):
        model = self.wids['XXXtv_treeview'].get_model()
        model.clear()
        total = 0.0
        for p in self.objeto.XXXunoamuchos:
            total += p.XXXcampoacumulable
            model.append((p.XXXcampo1, 
                          utils.float2str(p.XXXcampoacumulable), 
                          p.id))
        self.wids['XXXe_total_si_lo_hay'].set_text(utils.float2str(total))
            
    def nuevo(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        XXXobjeto_anterior = self.objeto
        if XXXobjeto_anterior != None:
            XXXobjeto_anterior.notificador.desactivar()
        XXXobjeto = pclases.XXXClase()
        utils.dialogo_info('NUEVO XXX CREADO', 
                           'Se ha creado un nuevo XXX.\nA continuación complete la información del misma y guarde los cambios.', 
                           padre = self.wids['ventana'])
        pclases.Auditoria.nuevo(XXXobjeto, self.usuario, __file__)
        XXXobjeto.notificador.activar(self.aviso_actualizacion)
        self.objeto = XXXobjeto
        self._objetoreciencreado = self.objeto
        self.activar_widgets(True)
        self.actualizar_ventana(objeto_anterior = XXXobjeto_anterior)

    def buscar(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        XXXobjeto = self.objeto
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR XXX", 
                                         texto = "Introduzca XXX:", 
                                         padre = self.wids['ventana']) 
        if a_buscar != None:
            try:
                ida_buscar = int(a_buscar)
            except ValueError:
                ida_buscar = -1
            # TODO: Cambiar por el nuevo buscar de utils que combina la búsqueda de varias palabras en cualquier orden con OR.
            criterio = pclases.OR(self.clase.q.campo1.contains(a_buscar),
                                  self.clase.q.campo2.contains(a_buscar),
                                  self.clase.q.id == ida_buscar)
            resultados = self.clase.select(criterio)
            if resultados.count() > 1:
                ## Refinar los resultados
                ide = self.refinar_resultados_busqueda(resultados)
                if id == None:
                    return
                resultados = [self.clase.get(id)]
                # Me quedo con una lista de resultados de un único objeto ocupando la primera posición.
                # (Más abajo será cuando se cambie realmente el objeto actual por este resultado.)
            elif resultados.count() < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info('SIN RESULTADOS', 'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.\n(Atención: Ver la lista completa puede resultar lento si el número de elementos es muy alto)',
                                   padre = self.wids['ventana'])
                return
            ## Un único resultado
            # Primero anulo la función de actualización
            if XXXobjeto != None:
                XXXobjeto.notificador.desactivar()
            # Pongo el objeto como actual
            try:
                XXXobjeto = resultados[0]
            except IndexError:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "Se produjo un error al recuperar la información.\nCierre y vuelva a abrir la ventana antes de volver a intentarlo.", 
                                   padre = self.wids['texto'])
                return
            # Y activo la función de notificación:
            XXXobjeto.notificador.activar(self.aviso_actualizacion)
            self.activar_widgets(True)
        self.objeto = XXXobjeto
        self.actualizar_ventana()

    def guardar(self, widget):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        # Desactivo el notificador momentáneamente
        self.objeto.notificador.activar(lambda: None)
        # Actualizo los datos del objeto
        for colname in self.dic_campos:
            col = self.clase.sqlmeta.columns[colname]
            try:
                valor_ventana = self.leer_valor(col, self.dic_campos[colname])
                setattr(self.objeto, colname, valor_ventana)
            except (ValueError, mx.DateTime.RangeError, TypeError):
                pass    # TODO: Avisar al usuario o algo. El problema es que no hay una forma "limpia" de obtener el valor que ha fallado.
        # Fuerzo la actualización de la BD y no espero a que SQLObject lo haga por mí:
        self.objeto.syncUpdate()
        self.objeto.sync()
        # Vuelvo a activar el notificador
        self.objeto.notificador.activar(self.aviso_actualizacion)
        self.actualizar_ventana()
        self.wids['b_guardar'].set_sensitive(False)

    def borrar(self, widget):
        """
        Elimina el objeto de la tabla pero NO
        intenta eliminar ninguna de sus relaciones,
        de forma que si se incumple alguna 
        restricción de la BD, cancelará la eliminación
        y avisará al usuario.
        """
        XXXobjeto = self.objeto
        if not utils.dialogo('¿Eliminar el XXX?', 
                             'BORRAR', 
                             padre = self.wids['ventana']):
            return
        if XXXobjeto.pagos != []:
            utils.dialogo_info('XXX NO ELIMINADO', 
                               'El XXX está implicado en operaciones que impiden su borrado.', 
                               padre = self.wids['ventana'])
        else:
            XXXobjeto.notificador.desactivar()
            try:
                XXXobjeto.destroy(ventana = __file__)
            except Exception, e:
                self.logger.error("XXXskel.py::borrar -> XXX ID %d no se pudo eliminar. Excepción: %s." % (XXXobjeto.id, e))
                utils.dialogo_info(titulo = "XXX NO BORRADO", 
                                   texto = "El XXX no se pudo eliminar.\n\nSe generó un informe de error en el «log» de la aplicación.",
                                   padre = self.wids['ventana'])
                self.actualizar_ventana()
                return
            self.objeto = None
            self.ir_a_primero()

if __name__ == "__main__":
    p = XXXSkel()
