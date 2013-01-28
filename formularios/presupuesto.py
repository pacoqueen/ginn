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
## TODO: Falta también doble clic o clic secundario para ver de 
##       dónde vienen los datos precalculados y tal. (Ventana inspect)
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


class Presupuesto(Ventana, VentanaGenerica):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
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
                      }  
        self.add_connections(connections)
        self.inicializar_ventana()
        self.actualizar_ventana(None)
        self.wids['tv_datos'].expand_all()
        self.wids['ventana'].resize(800, 600)
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
        self.wids['b_actualizar'].set_sensitive(True)
        self.wids['b_guardar'].set_sensitive(False)
        self.wids['b_nuevo'].set_sensitive(True)
        self.wids['b_buscar'].set_sensitive(True)
        # Inicialización del resto de widgets:
        cols = [('Concepto', 'gobject.TYPE_STRING', True, True, True, 
                 self.cambiar_concepto)]
        for m in range(12):
            mes = ((mx.DateTime.localtime().month - 1 + m) % 12) + 1
            strmes = mx.DateTime.DateTimeFrom(month = mes).strftime("%B")
            cols += [(strmes, 'gobject.TYPE_STRING', True, True, True, 
                      self.cambiar_importe, m)]
        cols += [('PUID', 'gobject.TYPE_STRING', False, False, False, None)]
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        for n in range(1, 13):
            col = self.wids['tv_datos'].get_column(n).get_cell_renderers()[0].set_property("xalign", 1)
        self.wids['tv_datos'].connect("row-activated", self.inspect)

    def inspect(self, tv, path, col):
        """
        Muestra de dónde vienen los datos precalculados.
        """
        # TODO: PORASQUI: Hay que revisar las notas porque esto ya no es así. 
        # Lo que he hecho y lo que quieren ahora es como la noche y el día.
        pass

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

    def rellenar_tabla(self):
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        model = self.wids['tv_datos'].get_model()
        model.clear()
        vpro.set_valor(0, "Cargando conceptos de primer nivel...") 
        padres = {}
        pas = pclases.PresupuestoAnual.select()
        pas_count = pas.count()
        i = 0.0
        for pa in pas:
            fila = (pa.descripcion, 
                    "", "", "", "", "", "", "", "", "", "", "", "", # 12 meses
                    pa.puid)
            nodo = model.append(None, fila) 
            padres[pa] = nodo 
            vpro.set_valor(i / pas_count, 
                           "Cargando conceptos de primer nivel...") 
            i += 1
        i = 0.0
        mes_actual = mx.DateTime.DateTimeFrom(mx.DateTime.localtime().year, 
                                              mx.DateTime.localtime().month,
                                              1)
        mes_final = mx.DateTime.DateTimeFrom(mx.DateTime.localtime().year + 1, 
                                             mx.DateTime.localtime().month,
                                             1)
        precalculo = precalcular_mes_actual(mes_actual, self.wids['ventana'])
        conceptos = pclases.ConceptoPresupuestoAnual.select()
        conceptos_count = conceptos.count()
        filas = {}
        for c in conceptos:
            filas[c] = [0, 0, 0, 0, 
                        0, 0, 0, 0, 
                        0, 0, 0, 0]
            vpro.set_valor(i / conceptos_count, 
                           "Cargando conceptos de presupuesto...") 
            i += 1
        i = 0.0
        valores = pclases.ValorPresupuestoAnual.select(pclases.AND(
            pclases.ValorPresupuestoAnual.q.mes >= mes_actual, 
            pclases.ValorPresupuestoAnual.q.mes < mes_final)) 
        valores_count = valores.count()
        for v in valores:
            c = v.conceptoPresupuestoAnual
            mes_offset = (v.mes.month - mes_actual.month) % 12
            if (v.mes.month == mes_actual.month 
                    and c.presupuestoAnual.descripcion 
                            == "Proveedores granza"): # OJO: HARCODED
                # Este valor no lo muestro. Tengo que tirar de datos reales.
                try:
                    filas[c][mes_offset] = precalculo[c]
                except KeyError: # Se ha metido a mano. No hay datos reales.
                    filas[c][mes_offset] = v.importe
            else:
                filas[c][mes_offset] = v.importe
            vpro.set_valor(i / conceptos_count, 
                           "Cargando valores de presupuesto...") 
            i += 1
        i = 0.0
        nodos_conceptos = {}
        for c in filas:
            vpro.set_valor(i / len(filas.keys()), 
                           "Montando matriz...")
            pa = c.presupuestoAnual
            nodo_padre = padres[pa]
            fila = [c.descripcion] + filas[c] + [c.puid]
            nodos_conceptos[c] = model.append(nodo_padre, fila)
            for i in range(1, 13):
                try:
                    model[nodo_padre][i] = utils.float2str(
                        utils.parse_float(model[nodo_padre][i]) + fila[i])
                except (TypeError, ValueError):
                    model[nodo_padre][i] = utils.float2str(fila[i])
            i += 1
        # Vuelvo a volcar todos los valores precalculados. Puede que alguno 
        # no se mostrara en el primer bucle por no haber valores antiguos de 
        # ese mes y no entrara en la rama "if" (ver arriba).
        i = 0.0
        for c in precalculo:
            vpro.set_valor(i / len(precalculo.keys()),
                    "Aplicando sustitución por valores reales...")
            pa = c.presupuestoAnual
            nodo_padre = padres[pa]
            nodo_concepto = nodos_conceptos[c]
            model[nodo_concepto][1] = utils.float2str(precalculo[c])
            try:
                model[nodo_padre][1] = utils.float2str(
                    utils.parse_float(model[nodo_padre][1]) + precalculo[c])
            except (TypeError, ValueError):
                model[nodo_padre][1] = utils.float2str(precalculo[c])
            i += 1
        vpro.ocultar()
            
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
        tipo = utils.dialogo_combo(titulo = "NUEVO CONCEPTO", 
                                   texto = "Seleccione tipo:", 
                                   ops = tipos, 
                                   padre = self.wids['ventana'])
        if tipo:
            pa = pclases.PresupuestoAnual.get(tipo)
            descripcion = utils.dialogo_entrada(titulo = "NUEVO CONCEPTO", 
                    texto = "Introduzca descripción:", 
                    padre = self.wids['ventana'])
            if descripcion:
                c = pclases.ConceptoPresupuestoAnual(presupuestoAnual = pa, 
                        descripcion = descripcion)
                pclases.Auditoria.nuevo(c, self.usuario, __file__)
                self.actualizar_ventana()

    def buscar(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        # TODO: : Buscar dentro de todas las filas un texto tecleado y pasarle el foco o algo.
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
            o.descripcion = value
            o.syncUpdate()
            model[path][0] = o.descripcion
            #self.actualizar_ventana(None)

    def cambiar_importe(self, cell, path, value, mes_offset):
        try:
            # TODO: Permitir fórmulas y mostrar precio si es un proveedor de granza.
            # TODO: Si es un valor precalculado no debe dejar cambiarlo. Aunque realmente no se cambia, al refrescar se vuelve a machacar el valor tecleado.
            value = utils._float(value)
        except (TypeError, ValueError):
            utils.dialogo(titulo = "ERROR", 
                    texto = "El texto introducido no es un número.", 
                    padre = self.wids['ventana'])
        else:
            model = self.wids['tv_datos'].get_model()
            puid = model[path][-1]
            o = pclases.getObjetoPUID(puid)
            if isinstance(o, pclases.ConceptoPresupuestoAnual): 
                fecha_actual = mx.DateTime.DateTimeFrom(
                                                mx.DateTime.localtime().year, 
                                                mx.DateTime.localtime().month,
                                                1)
                mes_actual = fecha_actual.month
                mes_buscado = (mes_actual + mes_offset) % 12
                try:
                    v = [i for i in o.valoresPresupuestoAnual 
                                            if i.mes.month == mes_buscado][0]
                except (IndexError):
                    v = pclases.ValorPresupuestoAnual(
                            conceptoPresupuestoAnual = o, 
                            mes = mx.DateTime.DateTimeFrom(fecha_actual.year,
                                mes_buscado, 1))
                    pclases.Auditoria.nuevo(v, self.usuario, __file__)
                    if v < fecha_actual:
                        v.mes = v.mes + mx.DateTime.DateTimeFrom(
                                year = v.mes.year + 1, 
                                month = v.mes.month, 
                                day = 1)
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
                model[path_padre][mes_offset + 1] = utils._float(
                        model[path_padre][mes_offset + 1]) + delta 


def precalcular_mes_actual(fecha_actual, ventana_padre = None, usuario = None):
    """
    Devuelve un diccionario de conceptos con el valor del mes en curso. Si el 
    concepto no existe, lo crea en la base de datos
    """
    vpro = VentanaActividad(ventana_padre, 
            "Precalculando datos reales del mes en curso...")
    vpro.mostrar()
    # Valores que puedo conocer del ERP (de momento):
    # 1.- IVA (soportado - repercutido)
    # TODO: PORASQUI
    # 2.- Entradas de granza
    vpro.mover()
    primes = fecha_actual
    finmes = mx.DateTime.DateTimeFrom(primes.year, primes.month, -1)
    vpro.mover()
    # Primero: productos granza:
    granzas = pclases.ProductoCompra.select(pclases.AND(
        pclases.ProductoCompra.q.descripcion.contains("granza"), 
        pclases.ProductoCompra.q.obsoleto == False, 
        pclases.ProductoCompra.q.tipoDeMaterialID 
            == pclases.TipoDeMaterial.select(
                 pclases.TipoDeMaterial.q.descripcion.contains("prima")
                )[0].id))
    # Saco datos de facturas:
    fras = pclases.FacturaCompra.select(pclases.AND(
        pclases.FacturaCompra.q.fecha >= primes, 
        pclases.FacturaCompra.q.fecha <= finmes))
    if pclases.DEBUG:
        print __file__, fras.count(), "facturas encontradas."
    # Filtro para quedarme con las de granza:
    vpro.mover()
    res = {}
    for f in fras:
        for ldc in f.lineasDeCompra:
            if ldc.productoCompra in granzas:
                if pclases.DEBUG:
                    print __file__, a.get_info(), ldc.get_info()
                concepto = buscar_concepto_proveedor_granza(ldc.proveedor, 
                                                            usuario)
                try:
                    res[concepto] += ldc.get_subtotal()
                except KeyError:
                    res[concepto] = ldc.get_subtotal()
            vpro.mover()
    # Y ahora de los albaranes no facturados.
    albs = pclases.AlbaranEntrada.select(pclases.AND(
        pclases.AlbaranEntrada.q.fecha >= primes, 
        pclases.AlbaranEntrada.q.fecha <= finmes))
    if pclases.DEBUG:
        print __file__, albs.count(), "albaranes encontrados."
    # Filtro para quedarme con los de granza:
    vpro.mover()
    for a in albs:
        for ldc in a.lineasDeCompra:
            # Solo quiero lo no facturado.
            if not ldc.facturaCompraID and ldc.productoCompra in granzas:
                if pclases.DEBUG:
                    print __file__, a.get_info(), ldc.get_info()
                concepto = buscar_concepto_proveedor_granza(ldc.proveedor, 
                                                            usuario)
                try:
                    res[concepto] += ldc.get_subtotal()
                except KeyError:
                    res[concepto] = ldc.get_subtotal()
            vpro.mover()
    vpro.ocultar()
    if pclases.DEBUG:
        print __file__, res
    return res

def buscar_concepto_proveedor_granza(proveedor, usuario = None):
    """
    Busca el concepto del presupuesto anual correspondiente al proveedor. Si 
    no lo encuentra, lo crea.
    """
    try:
        concepto = pclases.ConceptoPresupuestoAnual.select(
          pclases.ConceptoPresupuestoAnual.q.descripcion==proveedor.nombre)[0]
    except IndexError:
        concepto = pclases.ConceptoPresupuestoAnual(
                descripcion = proveedor.nombre, 
                presupuestoAnual = pclases.PresupuestoAnual.select(
                    pclases.PresupuestoAnual.q.descripcion 
                        == "Proveedores granza")[0] # EXISTE. Hay un check al 
                                            # principio que se asegura de eso.
                )
        pclases.Auditoria.nuevo(concepto, usuario, __file__)
    return concepto


if __name__ == "__main__":
    pclases.DEBUG = True
    p = Presupuesto()

