#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado                    #
# (pacoqueen@users.sourceforge.net)                                           #
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
## productos.py - Búsqueda interactiva de productos. 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 8 de mayo de 2007 -> Inicio
## 
## 
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, time
from framework import pclases
from informes import geninformes
from utils import _float as float

class Productos(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'productos.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.rellenar_widgets, 
                       'b_imprimir/clicked': self.imprimir, 
                       'b_exportar/clicked': self.exportar}  
        self.add_connections(connections)
        self.inicializar_ventana()
        gtk.main()

    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        # Inicialmente no se muestra NADA. Sólo se le deja al
        # usuario la opción de buscar o crear nuevo.
        cols = [('ID', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Código', 'gobject.TYPE_STRING', False, True, True, None), 
                ('Descripción', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_descripcion), 
                ('Existencias', 'gobject.TYPE_STRING', 
                    True, True, False, 
                    self.cambiar_existencias), 
                ('Precio defecto (s/IVA)', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_precio_defecto)]
        self.__tarifas = [t for t in pclases.Tarifa.select(orderBy = "nombre") 
                          if t.vigente]
        for tarifa in self.__tarifas:
            cols.append(("%s (c/IVA)" % tarifa.nombre, 
                         "gobject.TYPE_STRING", 
                         None, 
                         True, 
                         False, 
                         None))
        cols.append(('id', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_datos'], cols)
        for numcol in [3, 4] + [5 + i for i in range(len(self.__tarifas))]:
            col = self.wids['tv_datos'].get_column(numcol)
            if col != None:
                for cell in col.get_cell_renderers():
                    cell.set_property("xalign", 1)
                    if numcol in [5 + i for i in range(len(self.__tarifas))]:
                        cell.set_property("editable", True)
                        cell.connect("edited", 
                                     self.cambiar_precio_tarifa, numcol)
            else:
                txt = "productos.py::inicializar_ventana -> La columna %d "\
                      "es None. No formateo ni hago editable en TreeView." % (
                        numcol)
                if pclases.DEBUG:
                    print txt
                self.logger.warning(txt)
        col = self.wids['tv_datos'].get_column(1)
        for cell in col.get_cell_renderers():
            cell.set_property("xalign", 0.5)
        self.wids['tv_datos'].connect("row-activated", self.abrir_producto)
        self.wids['e_a_buscar'].connect("key_press_event", pasar_foco_enter, 
                                        self.wids['b_buscar'])
        self.wids['e_a_buscar'].grab_focus()
        self.wids['ventana'].resize(640, 480)

    def cambiar_existencias(self, cell, path, texto):
        # Chequeo permiso de escritura para camibar precios, existencias y 
        # demás:
        try:
            ventana = pclases.Ventana.select(
                                pclases.Ventana.q.fichero == "productos.py")[0]
            if self.usuario and (
                    not self.usuario.get_permiso(ventana).escritura 
                    or self.usuario.nivel >= 2):
                utils.dialogo_info(titulo = "USUARIO SIN PRIVILEGIOS", 
                                   texto = "Necesita permiso de escritura "
                                           "para modificar las existencias.", 
                                   padre = self.wids['ventana'])
                return
        except IndexError:
            if self.usuario and self.usuario.nivel >= 2:
                utils.dialogo_info(titulo = "USUARIO SIN PRIVILEGIOS", 
                                   texto = "No tiene permisos suficientes "
                                           "para modificar las existencias.", 
                                   padre = self.wids['ventana'])
                return

        model = self.wids['tv_datos'].get_model()
        ide = model[path][-1]
        try:
            existencias = utils._float(texto)
        except ValueError:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", 
                               texto = "El texto %s no es correcto." % (texto), 
                               padre = self.wids['ventana'])
        else:
            if "PC" in model[path][0]:
                producto = pclases.ProductoCompra.get(id)
                producto.sync()
                #producto.existencias = existencias
                producto.set_existencias(existencias)
                producto.syncUpdate()
                model[path][3] = utils.float2str(producto.existencias)

    def cambiar_descripcion(self, cell, path, texto):
        """
        Cambia la descripción del producto seleccionado.
        """
        try:
            ventana = pclases.Ventana.select(pclases.Ventana.q.fichero == "productos.py")[0]
            if self.usuario and (not self.usuario.get_permiso(ventana).escritura or self.usuario.nivel >= 2):
                utils.dialogo_info(titulo = "USUARIO SIN PRIVILEGIOS", 
                                   texto = "Necesita permiso de escritura para modificar el precio.", 
                                   padre = self.wids['ventana'])
                return
        except IndexError:
            if self.usuario and self.usuario.nivel >= 2:
                utils.dialogo_info(titulo = "USUARIO SIN PRIVILEGIOS", 
                                   texto = "No tiene permisos suficientes para modificar el precio.", 
                                   padre = self.wids['ventana'])
                return
        model = self.wids['tv_datos'].get_model()
        ide = model[path][-1]
        if "PC" in model[path][0]:
            producto = pclases.ProductoCompra.get(id)
        elif "PV" in model[path][0]:
            producto = pclases.ProductoVenta.get(id)
        else:
            return
        producto.sync()
        producto.descripcion = texto
        producto.syncUpdate()
        model[path][2] = producto.descripcion

    def cambiar_precio_defecto(self, cell, path, texto):
        # Chequeo permiso de escritura para camibar precios, existencias y demás:
        try:
            ventana = pclases.Ventana.select(pclases.Ventana.q.fichero == "productos.py")[0]
            if self.usuario and (not self.usuario.get_permiso(ventana).escritura or self.usuario.nivel >= 2):
                utils.dialogo_info(titulo = "USUARIO SIN PRIVILEGIOS", 
                                   texto = "Necesita permiso de escritura para modificar el precio.", 
                                   padre = self.wids['ventana'])
                return
        except IndexError:
            if self.usuario and self.usuario.nivel >= 2:
                utils.dialogo_info(titulo = "USUARIO SIN PRIVILEGIOS", 
                                   texto = "No tiene permisos suficientes para modificar el precio.", 
                                   padre = self.wids['ventana'])
                return

        model = self.wids['tv_datos'].get_model()
        ide = model[path][-1]
        try:
            precio = utils._float(texto)
        except ValueError:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", 
                               texto = "El texto %s no es correcto." % (texto), 
                               padre = self.wids['ventana'])
        else:
            if "PC" in model[path][0]:
                producto = pclases.ProductoCompra.get(id)
            elif "PV" in model[path][0]:
                producto = pclases.ProductoVenta.get(id)
            else:
                return
            for numcol in range(5, 5 + len(self.__tarifas)):
                tarifa = self.__tarifas[numcol - 5]
                porcentaje = tarifa.get_porcentaje(producto, True)
                precio_tarifa = precio * (1 + porcentaje)
                tarifa.asignarTarifa(producto, precio_tarifa)
                precio_tarifa *= 1.21
                porcentaje *= 100.0
                model[path][numcol] = "%s (%s %%)" % (utils.float2str(precio_tarifa), 
                                                      utils.float2str(porcentaje, 1))
            producto.sync()
            producto.precioDefecto = precio
            producto.syncUpdate()
            model[path][4] = utils.float2str(producto.precioDefecto)
    
    def cambiar_precio_tarifa(self, cell, path, texto, numcol):
        # Chequeo permiso de escritura para camibar precios, existencias y demás:
        try:
            ventana = pclases.Ventana.select(pclases.Ventana.q.fichero == "productos.py")[0]
            if self.usuario and (not self.usuario.get_permiso(ventana).escritura or self.usuario.nivel >= 2):
                utils.dialogo_info(titulo = "USUARIO SIN PRIVILEGIOS", 
                                   texto = "Necesita permiso de escritura para modificar el precio.", 
                                   padre = self.wids['ventana'])
                return
        except IndexError:
            if self.usuario and self.usuario.nivel >= 2:
                utils.dialogo_info(titulo = "USUARIO SIN PRIVILEGIOS", 
                                   texto = "No tiene permisos suficientes para modificar el precio.", 
                                   padre = self.wids['ventana'])
                return

        model = self.wids['tv_datos'].get_model()
        ide = model[path][-1]
        if "PC" in model[path][0]:
            producto = pclases.ProductoCompra.get(id)
        elif "PV" in model[path][0]:
            producto = pclases.ProductoVenta.get(id)
        else:
            return
        try:
            precio = utils._float(texto)
        except ValueError:
            try:
                porcentaje = utils.parse_porcentaje(texto, True)
                precio = producto.precioDefecto * (1.0 + porcentaje) * 1.21
            except ValueError:
                utils.dialogo_info(titulo = "ERROR DE FORMATO", 
                                   texto = "El texto %s no es correcto." % (texto), 
                                   padre = self.wids['ventana'])
                return
        tarifa = self.__tarifas[numcol - 5]
        precio_tarifa, porcentaje = calcular_precio(precio, producto.precioDefecto)
        tarifa.asignarTarifa(producto, precio_tarifa)
        precio_tarifa *= 1.21
        model[path][numcol] = "%s (%s %%)" % (utils.float2str(precio_tarifa), utils.float2str(porcentaje, 1))

    def imprimir(self, boton):
        """
        "Vuerca-vuerca" el TreeView en un PDF.
        """
        from informes.treeview2pdf import treeview2pdf
        from formularios.reports import abrir_pdf
        import mx.DateTime
        strfecha = utils.str_fecha(mx.DateTime.localtime())
        tv = self.wids['tv_datos']
        abrir_pdf(treeview2pdf(tv, titulo = "Productos", fecha = strfecha, apaisado = True))

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        tv = self.wids['tv_datos']
        abrir_csv(treeview2csv(tv))

    def abrir_producto(self, tv, path, vc):
        """
        Abre el producto al que se le ha hecho doble clic en una ventana nueva.
        """
        model = tv.get_model()
        ide = model[path][-1]
        if "PV" in model[path][0]:
            producto = pclases.ProductoVenta.get(ide)
            if producto.es_rollo():
                import productos_de_venta_rollos
                ventana_producto = productos_de_venta_rollos.ProductosDeVentaRollos(producto, usuario = self.usuario)
            elif producto.es_bala() or producto.es_bigbag():
                import productos_de_venta_balas
                ventana_producto = productos_de_venta_balas.ProductosDeVentaBalas(producto, usuario = self.usuario)
        elif "PC" in model[path][0]:
            producto = pclases.ProductoCompra.get(ide)
            import productos_compra
            ventana_producto = productos_compra.ProductosCompra(producto, usuario = self.usuario)

    def rellenar_widgets(self, boton = None):
        """
        Busca los productos coincidentes con la cadena del entry y los muestra en el TreeView.
        """
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        a_buscar = self.wids['e_a_buscar'].get_text()
        pvs = pclases.ProductoVenta.select(
            pclases.OR(pclases.ProductoVenta.q.codigo.contains(a_buscar), 
                       pclases.ProductoVenta.q.descripcion.contains(a_buscar)), 
            orderBy = "descripcion")
        pcs = pclases.ProductoCompra.select(pclases.AND(
           pclases.OR(pclases.ProductoCompra.q.codigo.contains(a_buscar), 
                      pclases.ProductoCompra.q.descripcion.contains(a_buscar)),
           pclases.ProductoCompra.q.obsoleto == False), 
           orderBy = "descripcion")
        resultados = []
        i = 0.0
        len_pvs = pvs.count() + pcs.count()
        tot = len_pvs * len(self.__tarifas) + len_pvs
        for pv in pvs:
            vpro.set_valor(i/tot, 'Recuperando %s...' % pv.descripcion)
            fila = ["PV:%d" % pv.id, 
                    pv.codigo, 
                    pv.descripcion, 
                    utils.float2str(pv.existencias), 
                    utils.float2str(pv.precioDefecto)]
            for tarifa in self.__tarifas:
                if tarifa.esta_en_tarifa(pv):
                    porcentaje = tarifa.get_porcentaje(pv)
                    precio = tarifa.obtener_precio(pv)
                    fila.append("%s (%s %%)" % (utils.float2str(precio * 1.21), 
                                                utils.float2str(porcentaje, 1)))
                else:
                    fila.append("-")
                i += 1
            fila.append(pv.id)
            resultados.append(fila)
            i += 1
        for pc in pcs:
            vpro.set_valor(i/tot, 'Recuperando %s...' % pc.descripcion)
            fila = ["PC:%d" % pc.id, 
                    pc.codigo, 
                    pc.descripcion, 
                    utils.float2str(pc.existencias), 
                    utils.float2str(pc.precioDefecto)]
            for tarifa in self.__tarifas:
                if tarifa.esta_en_tarifa(pc):
                    porcentaje = tarifa.get_porcentaje(pc)
                    precio = tarifa.obtener_precio(pc)
                    fila.append("%s (%s %%)" % (utils.float2str(precio * 1.21), 
                                                utils.float2str(porcentaje, 1)))
                else:
                    fila.append("-")
                i += 1
            fila.append(pc.id)
            resultados.append(fila)
            i += 1
        resultados.sort(func_por_descripcion)
        model = self.wids['tv_datos'].get_model()
        self.wids['tv_datos'].freeze_child_notify()
        self.wids['tv_datos'].set_model(None)
        model.clear()
        for e in resultados:
            model.append(e)
        self.wids['tv_datos'].set_model(model)
        self.wids['tv_datos'].thaw_child_notify()
        vpro.ocultar()

def func_por_descripcion(p1, p2):
    """
    Compara el tercer campo de cada lista recibida (para ordenar por descripción el TreeView).
    """
    if p1[2].upper() < p2[2].upper():
        return -1
    if p1[2].upper() > p2[2].upper():
        return 1
    return 0

def pasar_foco_enter(widget, event, destino):
    """
    Pasa el foco al widget destino.
    """
    if event.keyval == 65293 or event.keyval == 65421:
        destino.grab_focus()
        return True # Así corto la cadena de eventos y evito 
                    # que la superclase Ventana vuelva a pasar el foco.

def calcular_precio(precio, preciocosto):
    precio_sin_iva = precio / 1.21
    try:
        porcentaje = 100.0 * ((precio_sin_iva / preciocosto) - 1)
    except ZeroDivisionError:
        porcentaje = 0.0
    return precio_sin_iva, porcentaje

if __name__=='__main__':
    v = Productos()

