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
## cuentas_destino.py -- Cuentas bancarias de la empresa para 
##                      transferencias en pagos. 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 21 de febrero de 2007 -> Inicio
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


class CuentasDestino(Ventana, VentanaGenerica):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self.clase = pclases.CuentaDestino
        self.dic_campos = {"nombre": "e_nombre", 
                           "observaciones": "e_observaciones", 
                           "banco": "e_banco", 
                           "swif": "e_swif", 
                           "iban": "e_iban", 
                           "cuenta": "e_cuenta", 
                           "nombreBanco": "e_nombre_banco", 
                           "proveedorID": "cbe_proveedor", 
                          }
        Ventana.__init__(self, 'cuentas_destino.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_nuevo/clicked': self.nuevo,
                       'b_borrar/clicked': self.borrar,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_buscar/clicked': self.buscar
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
        cols = (('Proveedor', 'gobject.TYPE_STRING', False, True, True, None),
                ('Cuenta origen', 'gobject.TYPE_STRING', False, True, False, None),
                ('Importe', 'gobject.TYPE_STRING', False, True, False, None),
                ('Fecha', 'gobject.TYPE_STRING', False, True, False, None),
                ('Observaciones', 'gobject.TYPE_STRING', False, True, False, None),
                ('Concepto', 'gobject.TYPE_STRING', False, True, False, None),      # Número de factura o cuenta LOGIC.
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_transferencias'], cols)
        utils.rellenar_lista(self.wids['cbe_proveedor'], [(p.id, p.nombre) for p in pclases.Proveedor.select(orderBy = "nombre")])

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
        ws = tuple(["e_observaciones", "tv_transferencias", "b_borrar"] + [self.dic_campos[k] for k in self.dic_campos.keys()])
        for w in ws:
            try:
                self.wids[w].set_sensitive(s)
            except Exception, msg:
                print "Widget problemático:", w, "Excepción:", msg
        if chequear_permisos:
            self.check_permisos(nombre_fichero_ventana = "cuentas_destino.py")

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
            filas_res.append((r.id, r.nombre, r.banco, r.proveedor and r.proveedor.nombre or "-", r.observaciones))
        idcuenta = utils.dialogo_resultado(filas_res,
                                           titulo = 'SELECCIONE CUENTA BANCARIA',
                                           cabeceras = ('ID', 'Nombre', 'Banco', 'Proveedor', 'Observaciones'), 
                                           padre = self.wids['ventana'])
        if idcuenta < 0:
            return None
        else:
            return idcuenta

    def rellenar_widgets(self):
        """
        Introduce la información de la cuenta actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        cuenta = self.objeto
        for nombre_col in self.dic_campos:
            self.escribir_valor(cuenta._SO_columnDict[nombre_col], getattr(cuenta, nombre_col), self.dic_campos[nombre_col])
        self.rellenar_tabla_transferencias()
        self.objeto.make_swap()

    def rellenar_tabla_transferencias(self):
        model = self.wids['tv_transferencias'].get_model()
        model.clear()
        total = 0.0
        for p in self.objeto.pagos:
            total += p.importe
            model.append((p.proveedor and p.proveedor.nombre, 
                          p.cuentaOrigen and p.cuentaOrigen.nombre, 
                          utils.float2str(p.importe), 
                          utils.str_fecha(p.fecha), 
                          p.observaciones, 
                          p.concepto, 
                          p.id))
        self.wids['e_total'].set_text(utils.float2str(total))
            
    def nuevo(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        cuenta_anterior = self.objeto
        if cuenta_anterior != None:
            cuenta_anterior.notificador.desactivar()
        cuenta = pclases.CuentaDestino()
        pclases.Auditoria.nuevo(cuenta, self.usuario, __file__)
        utils.dialogo_info('NUEVA CUENTA CREADA', 
                           'Se ha creado una cuenta nueva.\nA continuación complete la información de la misma y guarde los cambios.', 
                           padre = self.wids['ventana'])
        cuenta.notificador.activar(self.aviso_actualizacion)
        self.objeto = cuenta
        self.activar_widgets(True)
        self.actualizar_ventana(objeto_anterior = cuenta_anterior)

    def buscar(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        cuenta = self.objeto
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR CUENTA", 
                                         texto = "Introduzca nombre de la cuenta o banco:", 
                                         padre = self.wids['ventana']) 
        if a_buscar != None:
            try:
                ida_buscar = int(a_buscar)
            except ValueError:
                ida_buscar = -1
            criterio = pclases.OR(pclases.CuentaDestino.q.nombre.contains(a_buscar),
                                 pclases.CuentaDestino.q.banco.contains(a_buscar),
                                 pclases.CuentaDestino.q.id == ida_buscar)
            resultados = pclases.CuentaDestino.select(criterio)
            if resultados.count() > 1:
                ## Refinar los resultados
                idcuenta = self.refinar_resultados_busqueda(resultados)
                if idcuenta == None:
                    return
                resultados = [pclases.CuentaDestino.get(idcuenta)]
                # Me quedo con una lista de resultados de un único objeto ocupando la primera posición.
                # (Más abajo será cuando se cambie realmente el objeto actual por este resultado.)
            elif resultados.count() < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info('SIN RESULTADOS', 'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.\n(Atención: Ver la lista completa puede resultar lento si el número de elementos es muy alto)',
                                   padre = self.wids['ventana'])
                return
            ## Un único resultado
            # Primero anulo la función de actualización
            if cuenta != None:
                cuenta.notificador.desactivar()
            # Pongo el objeto como actual
            try:
                cuenta = resultados[0]
            except IndexError:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "Se produjo un error al recuperar la información.\nCierre y vuelva a abrir la ventana antes de volver a intentarlo.", 
                                   padre = self.wids['texto'])
                return
            # Y activo la función de notificación:
            cuenta.notificador.activar(self.aviso_actualizacion)
            self.activar_widgets(True)
        self.objeto = cuenta
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
        Elimina la cuenta de la tabla pero NO
        intenta eliminar ninguna de sus relaciones,
        de forma que si se incumple alguna 
        restricción de la BD, cancelará la eliminación
        y avisará al usuario.
        """
        cuenta = self.objeto
        if not utils.dialogo('¿Eliminar la cuenta?', 'BORRAR', padre = self.wids['ventana']):
            return
        if cuenta.pagos != []:
            utils.dialogo_info('CUENTA NO ELIMINADA', 
                               'La cuenta está implicada en operaciones que impiden su borrado.', 
                               padre = self.wids['ventana'])
        else:
            cuenta.notificador.desactivar()
            try:
                cuenta.destroy(ventana = __file__)
            except Exception, e:
                self.logger.error("cuentas_destino::borrar -> Cuenta ID %d no se pudo eliminar. Excepción: %s." % (cuenta.id, e))
                utils.dialogo_info(titulo = "CUENTA NO BORRADA", 
                                   texto = "La cuenta no se pudo eliminar.\n\nSe generó un informe de error en el «log» de la aplicación.",
                                   padre = self.wids['ventana'])
                self.actualizar_ventana()
                return
            self.objeto = None
            self.ir_a_primero()

if __name__ == "__main__":
    p = CuentasDestino()

