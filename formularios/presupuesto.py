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
## presupuesto.py - Presupuesto anual.
###################################################################
## Changelog:
## 25 de enero de 2012 -> Inicio
## TODO: ¿Faltaría asegurarme de que todos los conceptos que cuelgan 
##       de proveedores de granza tienen un valor != None en proveedorID?
##       Solo se pueden meter conceptos desde esta ventana y se enlaza 
##       programáticamente. No debería haber problema ni registros 
##       de proveedores de granza sin proveedor.
## DONE: Faltan las ventas. Se puede crear a mano como un concepto más. 
##       No haría falta código nuevo para nada.
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
from ventana_progreso import VentanaProgreso, VentanaActividad
from albaranes_de_salida import buscar_proveedor
from dynconsulta import restar_mes

class Presupuesto(Ventana, VentanaGenerica):
    def __init__(self, objeto = None, usuario = None, mes_actual = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.mes_actual = mes_actual
        pclases.PresupuestoAnual.check_defaults()
        self.usuario = usuario
        self.clase = None
        self.dic_campos = {}
        Ventana.__init__(self, 'presupuesto.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_nuevo/clicked': self.nuevo,
                       'b_borrar/clicked': self.borrar,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       # 'b_guardar/clicked': self.guardar,
                       'b_buscar/clicked': self.buscar,
                       # TODO: Tooltip para ver toneladas y precio presupuestado de un proveedor de granza. Ver set_tooltip_cell de TreeView
                      }  
        self.add_connections(connections)
        self.inicializar_ventana()
        self.actualizar_ventana(None)
        self.wids['ventana'].resize(800, 600)
        gtk.main()

    def es_diferente(self):
        """
        Devuelve True si algún valor en ventana difiere de 
        los del objeto.
        """
        return False
    
    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        self.activar_widgets(False)
        self.wids['b_actualizar'].set_sensitive(True)
        self.wids['b_guardar'].set_sensitive(False)
        self.wids['b_nuevo'].set_sensitive(True)
        self.wids['b_buscar'].set_sensitive(True)
        # Inicialización del resto de widgets:
        cols = [('Concepto', 'gobject.TYPE_STRING', True, True, True, 
                 self.cambiar_concepto)]
        if not self.mes_actual:
            mes = mx.DateTime.localtime().month
        else:
            mes = self.mes_actual
        self.fecha_mes_actual = mx.DateTime.DateFrom(mx.DateTime.today().year,
                                                    mes,
                                                    1)
        self.fecha_mes_final = mx.DateTime.DateFrom(
                self.fecha_mes_actual.year + 1,
                self.fecha_mes_actual.month,
                1)
        if pclases.DEBUG:
            print __file__, self.fecha_mes_actual, self.fecha_mes_final
        for m in range(12):
            mescol = ((mes - 1 + m) % 12) + 1
            fechacol = mx.DateTime.DateTimeFrom(month = mescol, 
                    year = mx.DateTime.localtime().year + (m > 0 and 1 or 0))
            if mescol == 1:
                strmes = fechacol.strftime("%B'%y")
            else:
                strmes = fechacol.strftime("%B")
            cols += [(strmes, 'gobject.TYPE_STRING', True, True, True, 
                      self.cambiar_importe, m)]
        cols += [('PUID', 'gobject.TYPE_STRING', False, False, False, None)]
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        for n in range(1, 13):
            col = self.wids['tv_datos'].get_column(n)
            col.get_cell_renderers()[0].set_property("xalign", 1)
        col = self.wids['tv_datos'].get_column(0)
        col.set_expand(True)

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
        ws = []
        for w in ws:
            try:
                self.wids[w].set_sensitive(s)
            except Exception, msg:
                print "Widget problemático:", w, "Excepción:", msg
                import traceback
                traceback.print_last()
        if chequear_permisos:
            self.check_permisos(nombre_fichero_ventana = "presupuesto.py")

    def actualizar_ventana(self, boton = None):
        print __file__, "actualizar_ventana"
        self.rellenar_widgets()

    def rellenar_widgets(self):
        """
        Introduce la información del objeto actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        self.rellenar_tabla()
        self.wids['tv_datos'].expand_all()

    def rellenar_tabla(self):
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        model = self.wids['tv_datos'].get_model()
        model.clear()
        padres = self.cargar_conceptos(vpro, model)
        mes_actual, mes_final, filas = self.cargar_subconceptos(vpro)
        filas = self.cargar_valores(mes_actual, mes_final, filas, vpro)
        self.volcar_a_tv(filas, vpro, padres, model)
        # Ahora toca pasar el mes que se ha ido al final del año actual
        #self.ciclar_mes(vpro)
        vpro.ocultar()

    def volcar_a_tv(self, filas, vpro, padres, model):
        i = 0.0
        nodos_conceptos = {}
        for concepto in filas:
            vpro.set_valor(i / len(filas.keys()), 
                           "Montando matriz...")
            pa = concepto.presupuestoAnual
            nodo_padre = padres[pa]
            fila = [concepto.descripcion] + filas[concepto] + [concepto.puid]
            nodos_conceptos[concepto] = model.append(nodo_padre, fila)
            for mes_matriz in range(1, 13):
                try:
                    model[nodo_padre][mes_matriz] = utils.float2str(
                            utils.parse_float(model[nodo_padre][mes_matriz]) 
                            + utils.parse_float(fila[mes_matriz]))
                except (TypeError, ValueError):
                    model[nodo_padre][mes_matriz] = utils.float2str(
                            utils.parse_float(fila[mes_matriz]))
            i += 1

    def cargar_valores(self, mes_actual, mes_final, filas, vpro):
        i = 0.0
        valores = pclases.ValorPresupuestoAnual.select(
            pclases.AND(
                pclases.ValorPresupuestoAnual.q.mes >= mes_actual, 
                pclases.ValorPresupuestoAnual.q.mes < mes_final)) 
        valores_count = valores.count()
        for valor in valores:
            concepto = valor.conceptoPresupuestoAnual
            mes_offset = (valor.mes.month - mes_actual.month) % 12
            filas[concepto][mes_offset] = utils.float2str(valor.importe)
            vpro.set_valor(i / valores_count, 
                           "Cargando valores de presupuesto...") 
            i += 1
        return filas

    def cargar_subconceptos(self, vpro):
        i = 0.0
        if not self.mes_actual:
            mes = mx.DateTime.localtime().month
        else:
            mes = self.mes_actual
        mes_actual = mx.DateTime.DateTimeFrom(mx.DateTime.localtime().year, 
                                              mes,
                                              1)
        mes_final = mx.DateTime.DateTimeFrom(mes_actual.year + 1, 
                                             mes_actual.month,
                                             1)
        conceptos = pclases.ConceptoPresupuestoAnual.select()
        conceptos_count = conceptos.count()
        filas = {}
        for concepto in conceptos:
            filas[concepto] = []
            for nummes in range(12):
                filas[concepto].append(utils.float2str(0))
            vpro.set_valor(i / conceptos_count, 
                           "Cargando conceptos de presupuesto...") 
            i += 1
        return mes_actual, mes_final, filas

    def cargar_conceptos(self, vpro, model):
        vpro.set_valor(0, "Cargando conceptos de primer nivel...") 
        padres = {}
        pas = pclases.PresupuestoAnual.select()
        pas_count = pas.count()
        i = 0.0
        for pa in pas:
            fila = [pa.descripcion]
            for nummes in range(12):
                fila.append("")
            fila.append(pa.puid)
            nodo = model.append(None, fila) 
            padres[pa] = nodo 
            vpro.set_valor(i / pas_count, 
                           "Cargando conceptos de primer nivel...") 
            i += 1
        return padres

    def ciclar_mes(self, vpro):
        model = self.wids['tv_datos'].get_model()
        pasar_mes = True
        # Primero busco valores que ya existen en la BD. Porque puede ser que 
        # los valores a cero en el TreeView provengan de datos "reales" (esto 
        # es, no estimados) que se almacenan en precalc y tienen preferencia 
        # sobre los datos del presupuesto a la hora de mostrarse. En ese caso 
        # siempre se van a mostrar los valores 0 y siempre va a intentar 
        # pasar el mes de año pasado al actual, duplicando los valores en la 
        # BD.
        ultimo_mes_en_tabla = self.fecha_mes_final
        mes = ultimo_mes_en_tabla.month
        if mes == 1:
            anno = ultimo_mes_en_tabla.year - 1
            mes = 12
        else:
            mes -= 1
            anno = ultimo_mes_en_tabla.year
        penultimo_mes_en_tabla = restar_mes(ultimo_mes_en_tabla)
        valores = pclases.ValorPresupuestoAnual.select(pclases.AND(
            pclases.ValorPresupuestoAnual.q.mes <= ultimo_mes_en_tabla, 
            pclases.ValorPresupuestoAnual.q.mes > penultimo_mes_en_tabla))
        if pclases.DEBUG:
            print __file__, "ultimo_mes_en_tabla", ultimo_mes_en_tabla
            print __file__, "penultimo_mes_en_tabla", penultimo_mes_en_tabla
            print __file__, "valores.count()", valores.count()
        if not valores.count():     # Nunca se ha hecho el presupuesto para 
            # ese mes/año. Hora de crearlo a partir del año pasado (si es que 
            # no hay valores precalculados o algo y realmente está todo a 0).
            # Ahora compruebo entonces los valores actuales en el TreeView 
            # para ver si está todo a cero.
            for fila in model:
                if pclases.DEBUG:
                    print __file__, fila[0], fila[-2] and utils._float(fila[-2])
                if fila[-2] and utils._float(fila[-2]) != 0:
                    pasar_mes = False
                    break
            if pclases.DEBUG: print __file__, "(1) >>> pasar_mes", pasar_mes
            # Valores antiguos los busco en el año pasado.
            anno_pasado = restar_mes(ultimo_mes_en_tabla, 12)
            anno_pasado_mas_1_mes = restar_mes(anno_pasado, -1)
            valores_clonar = pclases.ValorPresupuestoAnual.select(pclases.AND(
                    pclases.ValorPresupuestoAnual.q.mes >= anno_pasado, 
                    pclases.ValorPresupuestoAnual.q.mes < anno_pasado_mas_1_mes
                    ))
            valores_count = valores_clonar.count()
            if (not valores_count 
                    or sum([v.importe for v in valores_clonar]) == 0):
                # No hay nada que copiar. Bucle infinito a cero.
                pasar_mes = False
            if pclases.DEBUG:
                print __file__, valores_count
                for v in valores_clonar:
                    print __file__, v.get_info(), v.importe
            if pclases.DEBUG: print __file__, "(2) >>> pasar_mes", pasar_mes
            if pasar_mes:
                # Copio a valores nuevos
                i = 0.0
                for v in valores_clonar:
                    vpro.set_valor(i / valores_count, 
                                   "Trasladando valores antiguos...") 
                    nv = v.clone(mes = restar_mes(v.mes, -12))
                    if pclases.DEBUG:
                        print __file__, "Nuevo valor:", nv.get_info(), \
                                nv.importe, utils.str_fecha(nv.mes)
                    pclases.Auditoria.nuevo(nv, self.usuario, __file__)
                    i += 1
                # Y refresco (una tónica, por favor. ¡CHISTACO!)
                self.actualizar_ventana()

    def nuevo(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        tipos = [(i.id, i.descripcion) 
                 for i in pclases.PresupuestoAnual.select()]
        tipos.insert(0, (0, "Añadir concepto de primer nivel"))
        tipo = utils.dialogo_combo(titulo = "NUEVO CONCEPTO", 
                                   texto = "Seleccione tipo:", 
                                   ops = tipos, 
                                   padre = self.wids['ventana'])
        if tipo >= 0:
            if tipo > 0:
                pa = pclases.PresupuestoAnual.get(tipo)
                if "proveedores granza" in pa.descripcion.lower():
                    # Si es del tipo de proveedores, entonces tengo que 
                    # añadir un proveedor de granza.
                    nombre = utils.dialogo_entrada(
                            titulo = "NOMBRE PROVEEDOR", 
                            texto = "Introduzca el nombre del proveedor:", 
                            padre = self.wids['ventana'])
                    if nombre != None:
                        proveedor = buscar_proveedor(nombre, 
                                self.wids['ventana'])
                        if proveedor:
                            # TODO: Check que el proveedor no esté ya en 
                            #       el presupuesto.
                            c = pclases.ConceptoPresupuestoAnual(
                                    presupuestoAnual = pa,
                                    descripcion = proveedor.nombre, 
                                    proveedor = proveedor)
                            pclases.Auditoria.nuevo(c, self.usuario, 
                                                    __file__)
                else:
                    descripcion = utils.dialogo_entrada(
                        titulo = "NUEVO CONCEPTO", 
                        texto = "Introduzca descripción:", 
                        padre = self.wids['ventana'])
                    if descripcion:
                        c = pclases.ConceptoPresupuestoAnual(
                                presupuestoAnual = pa,
                                descripcion = descripcion)
                        pclases.Auditoria.nuevo(c, self.usuario, __file__)
            else: # Concepto de primer nivel
                descripcion = utils.dialogo_entrada(
                    titulo = "NUEVO CONCEPTO", 
                    texto = "Introduzca descripción:", 
                    padre = self.wids['ventana'])
                if descripcion:
                    pa = pclases.PresupuestoAnual(descripcion = descripcion)
                    pclases.Auditoria.nuevo(pa, self.usuario, __file__)
            self.actualizar_ventana()

    def buscar(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        # TODO: Buscar dentro de todas las filas un texto tecleado y 
        #       pasarle el foco o algo.
        pass

    def borrar(self, widget):
        """
        Elimina los datos de la fila seleccionada o la fila completa.
        """
        model, iter = self.wids['tv_datos'].get_selection().get_selected()
        if iter:
            puid = model[iter][-1]
            o = pclases.getObjetoPUID(puid)
            if (isinstance(o, pclases.ConceptoPresupuestoAnual) 
                    and utils.dialogo(titulo = "ELIMINAR CONCEPTO", 
                        texto = "Se eliminará la fila completa. ¿Continuar?", 
                        padre = self.wids['ventana'])):
                o.destroy_en_cascada(ventana = __file__)
                self.actualizar_ventana(None)

    def cambiar_concepto(self, cell, path, value):
        model = self.wids['tv_datos'].get_model()
        puid = model[path][-1]
        o = pclases.getObjetoPUID(puid)
        if isinstance(o, pclases.ConceptoPresupuestoAnual): 
            # FIXME: ¿Y si es un concepto de primer nivel creado por el 
            # usuario? ¿No lo puede cambiar o qué?
            if o.proveedor:
                utils.dialogo_info(titulo = "PROVEEDOR NO MODIFICABLE", 
                        texto = "El nombre del proveedor no se puede cambiar \n"
                                "desde esta ventana, use la de proveedores.\n"
                                "Si lo que quiere es usar otro proveedor, \n"
                                "elimine la línea e introduzca un nuevo \n"
                                "proveedor en su lugar.", 
                        padre = self.wids['ventana'])
            elif o.inmutable:
                utils.dialogo_info(titulo = "CONCEPTO NO MODIFICABLE", 
                        texto = "El concepto seleccionado no se puede \n"
                                "modificar. Corresponde a cálculos \n"
                                "predefinidos por la aplicación. \n"
                                "Cree un nuevo concepto con el nuevo \n"
                                "nombre si lo necesita.", 
                        padre = self.wids['ventana'])
            else:
                o.descripcion = value
                o.syncUpdate()
                model[path][0] = o.descripcion

    def cambiar_importe(self, cell, path, value, mes_offset):
        model = self.wids['tv_datos'].get_model()
        if not model[path].parent:
            utils.dialogo_info(titulo = "NO EDITABLE", 
                    texto="La celda seleccionada es un sumatorio no editable.",
                    padre = self.wids['ventana'])
            return  # Es concepto de primer nivel. Sumatorio. No se puede edit.
        if not value:
            value = 0
        try:
            # TODO: Permitir fórmulas y mostrar precio si es un proveedor de 
            #       granza.
            value = utils._float(value)
        except (TypeError, ValueError):
            utils.dialogo_info(titulo = "ERROR", 
                    texto = "El texto introducido no es un número.", 
                    padre = self.wids['ventana'])
        else:
            puid = model[path][-1]
            o = pclases.getObjetoPUID(puid)
            if isinstance(o, pclases.ConceptoPresupuestoAnual): 
                if not self.mes_actual:
                    mes = mx.DateTime.localtime().month
                else:
                    mes = self.mes_actual
                fecha_actual = mx.DateTime.DateTimeFrom(
                                                mx.DateTime.localtime().year, 
                                                mes,
                                                1)
                mes_actual = fecha_actual.month
                mes_buscado = (mes_actual + mes_offset) % 12
                try:
                    v = [i for i in o.valoresPresupuestoAnual 
                                            if i.mes.month == mes_buscado][0]
                except (IndexError):
                    mes_importe = mx.DateTime.DateTimeFrom(fecha_actual.year,
                                                           mes_buscado, 1)
                    v = pclases.ValorPresupuestoAnual(
                            conceptoPresupuestoAnual = o, 
                            mes = mes_importe,
                            importe = value)
                    pclases.Auditoria.nuevo(v, self.usuario, __file__)
                    if v.mes < fecha_actual:
                        v.mes = v.mes + mx.DateTime.DateTimeFrom(
                                year = v.mes.year + 1, 
                                month = v.mes.month, 
                                day = 1)
                    fechas_vencimientos = o.calcular_vencimientos(mes_importe)
                    for fecha_vto in fechas_vencimientos:
                        vto = pclases.VencimientoValorPresupuestoAnual(
                                valorPresupuestoAnual = v, 
                                fecha = fecha_vto)
                # OJO: HARCODED: Texto "Proveedores granza" para identificarlo.
                if o.presupuestoAnual.descripcion == "Proveedores granza":
                    precio = utils.dialogo_entrada(titulo = "PRECIO TONELADA", 
                            texto = "Modifique el precio por tonelada estimado"
                                    "\npara %s en %s:" % (o.descripcion, 
                                                        v.mes.strftime("%B")),
                            padre = self.wids['ventana'], 
                            valor_por_defecto = utils.float2str(v.precio) 
                            )
                    if precio:
                        try:
                            precio = utils._float(precio)
                        except (TypeError, ValueError):
                            utils.dialogo_info(titulo = "ERROR DE FORMATO", 
                                    texto = "El valor tecleado («%s») no es "
                                            "válido." % precio, 
                                    padre = self.wids['ventana'])
                            return
                    else:   # Canceló
                        return
                    toneladas = utils.dialogo_entrada(titulo = "TONELADAS", 
                            texto = "Introduzca el número de toneladas "
                            "\nestimadas para el mes %s y proveedor %s:" % (
                                v.mes.strftime("%B"), 
                                o.descripcion), 
                            padre = self.wids['ventana'], 
                            valor_por_defecto=utils.float2str(value / precio))
                    if toneladas:
                        try:
                            toneladas = utils._float(toneladas)
                            value = importe = toneladas * precio
                            v.precio = precio
                        except (TypeError, ValueError):
                            utils.dialogo_info(titulo = "ERROR DE FORMATO", 
                                    texto = "El valor tecleado («%s») no es "
                                            "válido." % importe, 
                                    padre = self.wids['ventana'])
                            return
                    else:   # Canceló
                        return
                v.importe = value
                v.syncUpdate()
                valor_anterior = utils._float(model[path][mes_offset + 1])
                model[path][mes_offset + 1] = utils.float2str(v.importe)
                path_padre = model[path].parent.path
                delta = v.importe - valor_anterior
                model[path_padre][mes_offset + 1] = utils.float2str(
                        utils._float(
                            model[path_padre][mes_offset + 1]) + delta)
                if v.importe == 0:
                    v.destroy_en_cascada(usuario = self.usuario, 
                                         ventana = __file__)


if __name__ == "__main__":
    pclases.DEBUG = True
    try:    # Para testeo. 1 = Enero
        mes = int(sys.argv[1])
    except (TypeError, ValueError, IndexError):
        mes = None
    p = Presupuesto(mes_actual = mes)

