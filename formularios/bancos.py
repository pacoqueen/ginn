#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
## bancos.py - Ficha de bancos.
###################################################################
## Changelog:
## 17 de diciembre de 2012 -> Inicio
## 
###################################################################

import sys, os
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, mx, mx.DateTime
try:
    import pclases
    from seeker import VentanaGenerica 
except ImportError:
    sys.path.append(os.path.join('..', 'framework'))
    import pclases
    from seeker import VentanaGenerica 
from utils import _float as float


class Bancos(Ventana, VentanaGenerica):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self.clase = pclases.Banco
        self.dic_campos = {"nombre":             "e_nombre", 
                           "iban":               "e_iban", 
                           "limite":             "e_limite", 
                           "interes":            "e_interes", 
                           "comisionEstudio":    "e_comision", 
                           "concentracion":      "e_concentracion", 
                           "excesoVencimiento": "e_exceso", 
                          }
        Ventana.__init__(self, 'bancos.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_nuevo/clicked': self.nuevo,
                       'b_borrar/clicked': self.borrar,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_buscar/clicked': self.buscar,
                       'b_add_concentracion/clicked': self.add_concentracion, 
                       'b_drop_concentracion/clicked': self.drop_concentracion, 
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
                col = self.clase._SO_columnDict[colname]
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
        cols = (('Cliente', 'gobject.TYPE_STRING', False, True, True, None),
                ("Concentración máxima", "gobject.TYPE_STRING", 
                    True, True, False, self.cambiar_concentracion), 
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(self.wids['tv_concentracion'], cols)

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
        ws = tuple(["tv_concentracion", "b_borrar"] + [self.dic_campos[k] for k in self.dic_campos.keys()])
        for w in ws:
            try:
                self.wids[w].set_sensitive(s)
            except Exception, msg:
                print "Widget problemático:", w, "Excepción:", msg
                import traceback
                traceback.print_last()
        if chequear_permisos:
            self.check_permisos(nombre_fichero_ventana = "bancos.py")

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
            filas_res.append((r.id, r.nombre, r.iban))
        id = utils.dialogo_resultado(filas_res,
                                     titulo = 'SELECCIONE BANCO',
                                     cabeceras = ('ID', 'Nombre', 'IBAN'), 
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
        banco = self.objeto
        for nombre_col in self.dic_campos:
            self.escribir_valor(banco._SO_columnDict[nombre_col], 
                    getattr(banco, nombre_col), self.dic_campos[nombre_col])
        self.rellenar_tabla_concentraciones()
        self.objeto.make_swap()

    def rellenar_tabla_concentraciones(self):
        model = self.wids['tv_concentracion'].get_model()
        model.clear()
        total = 0.0
        for c in self.objeto.concentracionesRemesa:
            model.append((c.cliente.nombre, 
                          utils.float2str(c.concentracion), 
                          c.puid))

    def add_concentracion(self, boton):
        clientes = [(c.id, c.nombre) 
                    for c in pclases.Cliente.select(
                        pclases.Cliente.q.inhabilitado == False, 
                        orderBy = "nombre")
                    if c not in [cr.cliente for cr 
                                 in self.objeto.concentracionesRemesa]]
        clienteid = utils.dialogo_combo(titulo = "SELECCIONE UN CLIENTE", 
                texto = "Seleccione o teclee el nombre de un cliente:", 
                padre = self.wids['ventana'], 
                ops = clientes)
        if clienteid:
            cliente = pclases.Cliente.get(clienteid)
            pclases.ConcentracionRemesa(cliente = cliente, 
                                        banco = self.objeto, 
                                        concentracion = 0.0)
            self.rellenar_tabla_concentraciones()
    
    def drop_concentracion(self, boton):
        if not utils.dialogo(titulo = "¿BORRAR?", 
                texto = "Se eliminará la fila seleccionada. ¿Continuar?", 
                padre = self.wids['ventana']):
            return
        model,path=self.wids['tv_concentracion'].get_selection().get_selected()
        puid = model[path][-1]
        cr = pclases.getObjetoPUID(puid)
        cr.destroy(usuario = self.usuario, ventana = __file__)
        self.rellenar_tabla_concentraciones()

    def cambiar_concentracion(self, cell, path, texto):
        model = self.wids['tv_concentracion'].get_model()
        try:
            concentracion = utils._float(texto)
        except (ValueError, TypeError):
            utils.dialogo_info("ERROR EN FORMATO", 
                    "Introduzca la concentración como fracción de 1."
                    "\n(P. ej. 20% = 0.2)", 
                    padre = self.wids['ventana'])
        else:
            puid = model[path][-1]
            cr = pclases.getObjetoPUID(puid)
            if (sum([c.concentracion 
                    for c in self.objeto.concentracionesRemesa if c != cr])
                + concentracion) > 1.0:
                utils.dialogo_info(titulo = "EXCESO CONCENTRACIÓN", 
                    texto = "La concentración total no puede superar el 100%."
                            "\nSe corregirá.", 
                    padre = self.wids['ventana'])
                concentracion = 1.0 - sum([c.concentracion 
                    for c in self.objeto.concentracionesRemesa
                    if c != cr])
            cr.concentracion = concentracion
            cr.syncUpdate()
            model[path][1] = cr.concentracion
            
    def nuevo(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        objeto_anterior = self.objeto
        if objeto_anterior != None:
            objeto_anterior.notificador.desactivar()
        objeto = pclases.Banco(nombre = "Nuevo banco", 
                               limite = None, 
                               interes = None, 
                               comisionEstudio = None, 
                               concentracion = None, 
                               excesoVencimiento = None)
        utils.dialogo_info('NUEVO BANCO CREADO', 
                           'Se ha creado un nuevo banco.\nA continuación '
                           'complete la información del misma y guarde '
                           'los cambios.', 
                           padre = self.wids['ventana'])
        pclases.Auditoria.nuevo(objeto, self.usuario, __file__)
        objeto.notificador.activar(self.aviso_actualizacion)
        self.objeto = objeto
        self._objetoreciencreado = self.objeto
        self.activar_widgets(True)
        self.actualizar_ventana(objeto_anterior = objeto_anterior)

    def buscar(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        objeto = self.objeto
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR BANCO", 
                                         texto = "Introduzca nombre o cuenta:",
                                         padre = self.wids['ventana']) 
        if a_buscar != None:
            try:
                ida_buscar = int(a_buscar)
            except ValueError:
                ida_buscar = -1
            # TODO: Cambiar por el nuevo buscar de utils que combina la búsqueda de varias palabras en cualquier orden con OR.
            criterio = pclases.OR(self.clase.q.nombre.contains(a_buscar),
                                  self.clase.q.iban.contains(a_buscar),
                                  self.clase.q.id == ida_buscar)
            resultados = self.clase.select(criterio)
            if resultados.count() > 1:
                ## Refinar los resultados
                id = self.refinar_resultados_busqueda(resultados)
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
            if objeto != None:
                objeto.notificador.desactivar()
            # Pongo el objeto como actual
            try:
                objeto = resultados[0]
            except IndexError:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "Se produjo un error al recuperar la información.\nCierre y vuelva a abrir la ventana antes de volver a intentarlo.", 
                                   padre = self.wids['texto'])
                return
            # Y activo la función de notificación:
            objeto.notificador.activar(self.aviso_actualizacion)
            self.activar_widgets(True)
        self.objeto = objeto
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
            col = self.clase._SO_columnDict[colname]
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
        objeto = self.objeto
        if not utils.dialogo('¿Eliminar el banco?', 
                             'BORRAR', 
                             padre = self.wids['ventana']):
            return
        if objeto.remesas != []:
            utils.dialogo_info('BANCO NO ELIMINADO', 
                               'El banco está implicado en operaciones que '
                               'impiden su borrado.', 
                               padre = self.wids['ventana'])
        else:
            objeto.notificador.desactivar()
            try:
                objeto.destroy(usuario = self.usuario, ventana = __file__)
            except Exception, e:
                self.logger.error("bancos.py::borrar -> PUID %s no se pudo eliminar. Excepción: %s." % (objeto.puid, e))
                utils.dialogo_info(titulo = "BANCO NO BORRADO", 
                                   texto = "El banco no se pudo eliminar.\n\nSe generó un informe de error en el «log» de la aplicación.",
                                   padre = self.wids['ventana'])
                self.actualizar_ventana()
                return
            self.objeto = None
            self.ir_a_primero()

if __name__ == "__main__":
    p = Bancos()

