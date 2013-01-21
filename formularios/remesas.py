#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2013  Francisco José Rodríguez Bogado,                   #
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
## remesas.py - Remesas de efectos de cobro.
###################################################################
## Changelog:
## 19 de diciembre de 2012 -> Inicio
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


class Remesas(Ventana, VentanaGenerica):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self.clase = pclases.Remesa
        self.dic_campos = {# "importe":       "e_importe", 
                           "bancoID":       "cb_banco", 
                           "fechaPrevista": "e_fecha", 
                           "codigo":        "e_codigo", 
                           "fechaCobro":    "e_fechaCobro", 
                           "id":            "e_id", 
                           "aceptada":      "ch_aceptada", 
                          }
        Ventana.__init__(self, 'remesas.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_nuevo/clicked': self.nuevo,
                       'b_borrar/clicked': self.borrar,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_buscar/clicked': self.buscar,
                       "b_confirmar/clicked": self.confirmar, 
                       "b_add_efecto/clicked": self.add_efecto, 
                       "b_drop_efecto/clicked": self.drop_efecto, 
                      }  
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        self.wids['b_add_efecto'].set_property("visible", False)
        self.wids['b_drop_efecto'].set_property("visible", False)
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
                if colname in ("id", ):
                    continue
                col = self.clase._SO_columnDict[colname]
                try:
                    valor_ventana = self.leer_valor(col, 
                                                    self.dic_campos[colname])
                except (ValueError, mx.DateTime.RangeError, TypeError):
                    if isinstance(col, pclases.SODateCol):
                        valor_ventana = None
                    else:
                        igual = False
                valor_objeto = getattr(self.objeto, col.name)
                if isinstance(col, pclases.SODateCol):
                    if valor_objeto:
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
        cols = (('Confirmado', 'gobject.TYPE_BOOLEAN', True, True, False, 
                    self.confirmar_efecto),
                ('Código', 'gobject.TYPE_STRING', False, True, True, None),
                ('Cliente', 'gobject.TYPE_STRING', False, True, False, None),
                ('Importe', 'gobject.TYPE_STRING', False, True, False, None),
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
                # La última columna (oculta en la Vista) siempre es el id.
        utils.preparar_listview(self.wids['tv_efectos'], cols)
        cols = (('Porcentaje','gobject.TYPE_STRING', False, True, False, None),
                ('Cliente', 'gobject.TYPE_STRING', False, True, True, None),
                ('Importe', 'gobject.TYPE_STRING', False, True, False, None), 
                ('PUID cliente', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(self.wids['tv_concentracion'], cols)
        utils.rellenar_lista(self.wids['cb_banco'], 
                             [(p.id, p.nombre) for p in 
                                pclases.Banco.select(orderBy = "nombre")])
        self.wids['tv_efectos'].connect("row-activated", self.abrir_efecto) 
        col = self.wids['tv_efectos'].get_column(3)
        for cell in col.get_cell_renderers():
            cell.set_property("xalign", 1)
        self.wids['ch_aceptada'].set_sensitive(False)
        self.wids['b_confirmar'].set_sensitive(
                self.objeto and not self.objeto.aceptada or False)

    def add_efecto(self, boton):
        """
        Añade un pagaré o un confirming a la remesa, creando si hace falta 
        el efecto "intermedio".
        """
        raise NotImplemented, "You are not supposed to be here..."

    def drop_efecto(self, boton):
        """
        Desvincula el efecto de la remesa.
        """
        raise NotImplemented, "Too soon, little prince."

    def abrir_efecto(self, tv, path, view_column):
        model = tv.get_model()
        puid = model[path][-1]
        objeto = pclases.getObjetoPUID(puid)
        if objeto.pagareCobro:
            import pagares_cobros
            v = pagares_cobros.PagaresCobros(objeto.pagareCobro, 
                                             usuario = self.usuario)
        elif objeto.confirming:
            import confirmings
            v = confirmings.Confirmings(objeto.confirming, 
                                        usuario = self.usuario)

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
        ws = tuple(["b_confirmar", "tv_efectos", "b_borrar", 
                    "e_importe_seleccionado"] 
                   + [self.dic_campos[k] for k in self.dic_campos.keys()])
        for w in ws:
            # Caso especial. Me interesa dejar fuera el check de activado 
            # porque el usuario no lo va a editar directamente:
            if w == "ch_aceptada":
                continue
            try:
                self.wids[w].set_sensitive(s)
            except Exception, msg:
                print "Widget problemático:", w, "Excepción:", msg
                import traceback
                traceback.print_last()
        if chequear_permisos:
            self.check_permisos(nombre_fichero_ventana = "remesas.py")

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
            filas_res.append(
                    (r.id, r.codigo, r.banco and r.banco.nombre or "", 
                     sum([e.importe for e in r.efectos])))
        id = utils.dialogo_resultado(filas_res,
                                     titulo = 'SELECCIONE REMESA',
                                     cabeceras = ('ID', 'Código', 'Banco', 
                                                  'Importe'), 
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
        remesa = self.objeto
        for nombre_col in self.dic_campos:
            if nombre_col not in ("id", ):
                self.escribir_valor(remesa._SO_columnDict[nombre_col], 
                                    getattr(remesa, nombre_col), 
                                    self.dic_campos[nombre_col])
            else:
                self.wids[self.dic_campos[nombre_col]].set_text(
                        str(getattr(remesa, nombre_col)))
        self.rellenar_tabla_efectos()
        self.objeto.make_swap()
        self.wids['l_estado'].set_text("<i>%s</i>" % remesa.get_str_estado())
        self.wids['l_estado'].set_use_markup(True)
        self.wids['ch_aceptada'].set_sensitive(False)
        self.wids['b_confirmar'].set_sensitive(
                self.objeto and not self.objeto.aceptada or False)
        model = self.wids['tv_concentracion'].get_model()
        model.clear()
        concentraciones = self.objeto.calcular_concentraciones()
        for cliente in concentraciones:
            porcentaje, importe = concentraciones[cliente] 
            model.append((utils.float2str(porcentaje * 100) + " %", 
                          cliente and cliente.nombre or "", 
                          utils.float2str(importe) + " €", 
                          cliente and cliente.puid or None))

    def rellenar_tabla_efectos(self):
        model = self.wids['tv_efectos'].get_model()
        model.clear()
        total = 0.0
        for p in self.objeto.efectos:
            total += p.cantidad
            model.append((self.objeto.aceptada, # False, 
                          p.codigo, 
                          p.cliente and p.cliente.nombre or "", 
                          utils.float2str(p.cantidad), 
                          p.puid))
        self.wids['e_importe'].set_text(utils.float2str(total))
            
    def nuevo(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        remesa_anterior = self.objeto
        if remesa_anterior != None:
            remesa_anterior.notificador.desactivar()
        remesa = pclases.Remesa(banco = None, 
                                fechaPrevista = None, 
                                codigo = "", 
                                fechaCobro = None, 
                                aceptada = False)
        utils.dialogo_info('NUEVA REMESA CREADA', 
                           'Se ha creado una nueva remesa.\n'
                           'A continuación complete la información de la '
                           'misma y guarde los cambios.', 
                           padre = self.wids['ventana'])
        pclases.Auditoria.nuevo(remesa, self.usuario, __file__)
        remesa.notificador.activar(self.aviso_actualizacion)
        self.objeto = remesa
        self._objetoreciencreado = self.objeto
        self.activar_widgets(True)
        self.actualizar_ventana(objeto_anterior = remesa_anterior)

    def buscar(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        remesa = self.objeto
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR REMESA", 
                                         texto = "Introduzca código:", 
                                         padre = self.wids['ventana']) 
        if a_buscar != None:
            try:
                ida_buscar = int(a_buscar)
            except ValueError:
                ida_buscar = -1
            criterio = pclases.OR(self.clase.q.codigo.contains(a_buscar),
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
            if remesa != None:
                remesa.notificador.desactivar()
            # Pongo el objeto como actual
            try:
                remesa = resultados[0]
            except IndexError:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "Se produjo un error al recuperar la información.\nCierre y vuelva a abrir la ventana antes de volver a intentarlo.", 
                                   padre = self.wids['texto'])
                return
            # Y activo la función de notificación:
            remesa.notificador.activar(self.aviso_actualizacion)
            self.activar_widgets(True)
        self.objeto = remesa
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
            if colname not in ("id", ):
                col = self.clase._SO_columnDict[colname]
                # FIXME: Las fechas en blanco se deberían guardar como Nones. Ahora mismo vuelve al valor que tuviera antes.
                try:
                    valor_ventana = self.leer_valor(col, self.dic_campos[colname])
                    setattr(self.objeto, colname, valor_ventana)
                except (ValueError, mx.DateTime.RangeError, TypeError):
                    pass 
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
        remesa = self.objeto
        if not utils.dialogo('¿Eliminar la remesa?', 
                             'BORRAR', 
                             padre = self.wids['ventana']):
            return
        if remesa.efectos:
            utils.dialogo_info('REMESA NO ELIMINADA', 
                               'La remesa está implicada en operaciones '
                               'que impiden su borrado.', 
                               padre = self.wids['ventana'])
        else:
            remesa.notificador.desactivar()
            try:
                remesa.destroy(ventana = __file__)
            except Exception, e:
                self.logger.error("remesas.py::borrar -> Remesa ID %d no se pudo eliminar. Excepción: %s." % (remesa.id, e))
                utils.dialogo_info(titulo = "REMESA NO BORRADA", 
                                   texto = "La remesa no se pudo eliminar.\n"
                                           "\nSe generó un informe de error "
                                           "en el «log» de la aplicación.",
                                   padre = self.wids['ventana'])
                self.actualizar_ventana()
                return
            self.objeto = None
            self.ir_a_primero()

    def confirmar_efecto(self, cell, path):
        model = self.wids['tv_efectos'].get_model()
        model[path][0] = not model[path][0]
        a_confirmar = []
        iter = model.get_iter_first()
        while iter:
            if model[iter][0]:
                a_confirmar.append(pclases.getObjetoPUID(model[iter][-1]))
            iter = model.iter_next(iter)
        self.wids['e_importe_seleccionado'].set_text(
                utils.float2str(sum([o.cantidad for o in a_confirmar])))

    def confirmar(self, boton):
        # PORASQUI: ¿Botón desconfirmar?
        efectos_a_confirmar = []
        model = self.wids['tv_efectos'].get_model()
        a_confirmar = []
        iter = model.get_iter_first()
        while iter:
            if model[iter][0]:
                efectos_a_confirmar.append(
                        pclases.getObjetoPUID(model[iter][-1]))
            iter = model.iter_next(iter)
        # Los efectos no marcados vuelven a cartera.
        for e in self.objeto.efectos:
            if e not in efectos_a_confirmar:
                self.objeto.removeEfecto(e)
        # Hay que desvincular los efectos de las demás remesas
        for e in efectos_a_confirmar:
            for r in e.remesas:
                if r != self.objeto:
                    e.removeRemesa(r)
        # PLAN: ¿Cómo activo el notificador de otras posibles remesas abiertas
        # tras este cambio?
        # Y confirmar la actual marcando el campo "aceptada" y fecha de cobro.
        self.objeto.aceptada = True
        self.objeto.fechaCobro = mx.DateTime.localtime()
        self.objeto.syncUpdate()
        self.actualizar_ventana()
        self.objeto.sync()
        if not self.objeto.codigo:
            self.wids['e_codigo'].set_text('Inserte código aquí.')
            utils.dialogo_info(titulo = "COMPRUEBE DATOS", 
                               texto = "Introduzca el código de remesa "
                                       "facilitado por el banco.", 
                               padre = self.wids['ventana'])
        if not self.objeto.fechaPrevista:
            self.wids['e_fecha'].set_text(
                    utils.str_fecha(mx.DateTime.localtime() 
                                    + (mx.DateTime.oneDay * 2)))
            utils.dialogo_info(titulo = "COMPRUEBE DATOS", 
                               texto = "Corrija la fecha prevista de ingreso.",
                               padre = self.wids['ventana'])
        #self.guardar(None)

if __name__ == "__main__":
    p = Remesas()

