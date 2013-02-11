#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2013  Francisco José Rodríguez Bogado                    #
#                          <pacoqueen@users.sourceforge.net>                  #
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
## dynconsulta.py - Consulta dinámica resumen de análisis financiero
###################################################################
## Changelog:
## 8 de febrero de 2012 -> Inicio
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
from widgets import replace_widget


class DynConsulta(Ventana, VentanaGenerica):
    def __init__(self, objeto = None, usuario = None, mes_actual = None, 
                 num_meses = 12):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.mes_actual = mes_actual
        self.num_meses = num_meses != None and num_meses or 12
        self.usuario = usuario
        self.clase = None
        self.dic_campos = {}
        Ventana.__init__(self, 'dynconsulta.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_nuevo/clicked': self.nuevo,
                       'b_borrar/clicked': self.borrar,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       # 'b_guardar/clicked': self.guardar,
                       'b_buscar/clicked': self.buscar,
                       'sp_mes_actual/value-changed': self.update_mes_actual, 
                       'sp_num_meses/value-changed': self.update_num_meses
                      }  
        self.inicializar_ventana()
        self.actualizar_ventana(None)
        self.wids['tv_datos'].expand_all()
        self.wids['ventana'].resize(800, 600)
        self.add_connections(connections)
        gtk.main()

    def es_diferente(self):
        """
        Devuelve True si algún valor en ventana difiere de 
        los del objeto.
        """
        return False

    def update_mes_actual(self, sp):
        self.mes_actual = sp.get_value_as_int()
        self.inicializar_ventana()
        self.actualizar_ventana(None)
    
    def update_num_meses(self, sp):
        self.num_meses = sp.get_value_as_int()
        self.inicializar_ventana()
        self.actualizar_ventana(None)

    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        antiguo_tv_datos = self.wids['tv_datos']
        nuevo_tv_datos = gtk.TreeView()
        nuevo_tv_datos.show()
        replace_widget(antiguo_tv_datos,nuevo_tv_datos)
        self.wids['tv_datos'] = nuevo_tv_datos
        self.wids['sp_mes_actual'].set_value(self.mes_actual)
        self.wids['sp_num_meses'].set_value(self.num_meses)
        self.activar_widgets(False)
        self.wids['b_actualizar'].set_sensitive(True)
        self.wids['b_guardar'].set_sensitive(False)
        self.wids['b_buscar'].set_sensitive(True)
        for b in ("b_nuevo", "b_guardar", "b_borrar"):
            self.wids[b].set_property("visible", False)
        # Inicialización del resto de widgets:
        cols = [('Concepto', 'gobject.TYPE_STRING', False, True, True, None)]
        if not self.mes_actual:
            mes = mx.DateTime.localtime().month
        else:
            mes = self.mes_actual
        for m in range(self.num_meses):
            mescol = ((mes - 1 + m) % 12) + 1 
            fechacol = mx.DateTime.DateTimeFrom(month = mescol, 
                    year = mx.DateTime.localtime().year + (m > 0 and 1 or 0))
            if mescol == 1:
                strmes = fechacol.strftime("%B'%y")
            else:
                strmes = fechacol.strftime("%B")
            cols.append((strmes,'gobject.TYPE_STRING',False,True,True,None))
        cols += [('PUID', 'gobject.TYPE_STRING', False, False, False, None)]
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        for n in range(1, self.num_meses + 1):
            col = self.wids['tv_datos'].get_column(n).get_cell_renderers()[0]\
                    .set_property("xalign", 1)
        self.wids['tv_datos'].connect("row-activated", self.inspect)

    def inspect(self, tv, path, col):
        """
        Muestra de dónde vienen los datos precalculados.
        """
        indexcol = get_col_pos(tv, col)
        mes = self.mes_actual + indexcol - 1
        print mes
        print col.get_property("title")
        print tv.get_model()[path][-1]
        # TODO: 

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
            self.check_permisos(nombre_fichero_ventana = "dynconsulta.py")

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
            fila = [pa.descripcion] 
            for m in range(self.num_meses):
                fila.append("")
            fila.append(pa.puid)
            nodo = model.append(None, fila) 
            padres[pa] = nodo 
            vpro.set_valor(i / pas_count, 
                           "Cargando conceptos de primer nivel...") 
            i += 1
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
        anno_final = mes_actual.year
        mes_final = mes_actual.month + self.num_meses
        while mes_final > 12:
            anno_final += 1
            mes_final -= 12
        mes_final = mx.DateTime.DateTimeFrom(anno_final, 
                                             mes_final, 
                                             1)
        # Esto va en dynconsulta. No se utilizan valores reales aquí.
        precalculo = precalcular_mes_actual(mes_actual, self.wids['ventana'])
        conceptos = pclases.ConceptoPresupuestoAnual.select()
        conceptos_count = conceptos.count()
        filas = {}
        for c in conceptos:
            filas[c] = []
            for m in range(self.num_meses):
                filas[c].append(0)
            vpro.set_valor(i / conceptos_count, 
                           "Cargando conceptos de dynconsulta...") 
            i += 1
        i = 0.0
        valores = pclases.ValorPresupuestoAnual.select(pclases.AND(
            pclases.ValorPresupuestoAnual.q.mes >= mes_actual, 
            pclases.ValorPresupuestoAnual.q.mes < mes_final)) 
        valores_count = valores.count()
        for v in valores:
            c = v.conceptoPresupuestoAnual
            mes_offset = (v.mes.month - mes_actual.month) % self.num_meses
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
            vpro.set_valor(i / valores_count, 
                           "Cargando valores de dynconsulta...") 
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
            for mes_matriz in range(1, self.num_meses + 1):
                try:
                    model[nodo_padre][mes_matriz] = utils.float2str(
                            utils.parse_float(model[nodo_padre][mes_matriz]) 
                            + fila[mes_matriz])
                except (TypeError, ValueError):
                    model[nodo_padre][mes_matriz] = utils.float2str(
                            fila[mes_matriz])
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
        # Ahora toca pasar el mes que se ha ido al final del año actual
        pasar_mes = False
        for fila in model:
            if fila[-2] and utils._float(fila[-2]) != 0:
                pasar_mes = True
                break
        if not pasar_mes:
            # Valores antiguos
            mes_final = mx.DateTime.DateTimeFrom(mes_actual.year, mes, 1)
            if mes == 1:
                anno = mes_final.year - 1
                mes = 12
            else:
                anno = mes_final.year
                mes = mes - 1
            mes_anterior = mx.DateTime.DateTimeFrom(anno, mes, 1)
            # Copio a valores nuevos
            valores = pclases.ValorPresupuestoAnual.select(pclases.AND(
                pclases.ValorPresupuestoAnual.q.mes >= mes_anterior, 
                pclases.ValorPresupuestoAnual.q.mes < mes_final)) 
            valores_count = valores.count()
            if not valores_count or sum([v.importe for v in valores]) == 0:
                # No hay nada que copiar. Bucle infinito a cero.
                pass
            else:
                for v in valores:
                    vpro.set_valor(i / valores_count, 
                                   "Trasladando valores antiguos...") 
                    nv = v.clone(mes = mx.DateTime.DateTimeFrom(
                        year = mes_anterior.year + 1, 
                        month = mes_anterior.month, 
                        day = 1))
                    pclases.Auditoria.nuevo(nv, self.usuario, __file__)
                    i += 1
                # Y refresco (una tónica, por favor)
                self.actualizar_ventana()
        vpro.ocultar()
            
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
                    print __file__, f.get_info(), ldc.get_info()
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
    Busca el concepto del dynconsulta anual correspondiente al proveedor. Si 
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

def get_col_pos(tv, col):
    """
    Devuelve la posición (índice entero comenzando por 0) de la columna en 
    el TreeView.
    """
    return tv.get_columns().index(col)


if __name__ == "__main__":
    """
    Primer parámetro: número de meses a mostrar.
    Segundo parámetro: primer mes a mostrar (1 = enero).
    """
    pclases.DEBUG = True
    try:
        num_meses = int(sys.argv[1])
    except (TypeError, ValueError, IndexError):
        num_meses = None
    try:    # Para testeo. 1 = Enero
        mes = int(sys.argv[2])
    except (TypeError, ValueError, IndexError):
        mes = None
    p = DynConsulta(mes_actual = mes, num_meses = num_meses)

