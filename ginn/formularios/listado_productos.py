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
## listado_productos.py - Listado simple de productos para imprimir
###################################################################
## TODO: Barra de progreso. Aunque habría varios puntos donde 
##       meterla, no solo en el rellenar_tabla. También en las 
##       sugerencias, en el buscar...
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
import mx.DateTime

class ListadoProductos(Ventana):
    inicio = None
    fin = None
    cliente = None
    resultado = []

    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        global fin
        Ventana.__init__(self, 'listado_productos.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_limpiar/clicked': self.limpiar_tv, 
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_exportar/clicked': self.exportar}
        self.add_connections(connections)
        cols = (('Código', 'gobject.TYPE_STRING', False, True, False, None),
                ('Descripción', 'gobject.TYPE_STRING', False,True,False,None),
                ('PVP', 'gobject.TYPE_STRING', False,True,False,None),
                ('ID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(self.wids['tv_datos'], cols)
        col = self.wids['tv_datos'].get_column(2)
        for cell in col.get_cell_renderers():
            cell.set_property("xalign", 1)
        self.wids['tv_datos'].connect("row-activated", self.abrir_producto)
        self.wids['e_buscar'].grab_focus()
        gtk.main()

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        tv = self.wids['tv_datos']
        abrir_csv(treeview2csv(tv))

    def abrir_producto(self, tv, path, column):
        """
        Abre el producto al que se le ha hecho doble clic en una ventana nueva.
        """
        model = tv.get_model()
        idproducto = model[path][-1]
        try:
            if "PV" in idproducto:
                producto = pclases.ProductoVenta.get(idproducto.split(":")[1])
                if producto.es_rollo():
                    from formularios import productos_de_venta_rollos
                    V = productos_de_venta_rollos.ProductosDeVentaRollos
                    ventana_producto = V(producto, usuario = self.usuario)  # @UnusedVariable
                elif producto.es_bala() or producto.es_bigbag():
                    from formularios import productos_de_venta_balas
                    V = productos_de_venta_balas.ProductosDeVentaBalas
                    ventana_producto = V(producto, usuario = self.usuario)  # @UnusedVariable
            elif "PC" in idproducto:
                producto = pclases.ProductoCompra.get(idproducto.split(":")[1])
                from formularios import productos_compra
                V = productos_compra.ProductosCompra
                ventana_producto = V(producto, usuario = self.usuario)  # @UnusedVariable
        except Exception, e:
            utils.dialogo_info(titulo = "ERROR RECUPERANDO PRODUCTO",
                               texto = "El producto ID %d no se ha encontrado."
                               "\n\n"
                               "Compruebe que no haya sido eliminado recargand"
                               "o la consulta y vuelva a intentarlo."
                               "\n\n\n"
                               "Información de depuración:"
                               "\n%s" % (idproducto, e),
                               padre = self.wids['ventana'])

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, items):
        """
        Rellena el model con los items de la consulta
        """
        model = self.wids['tv_datos'].get_model()
        #model.clear()
        try:
            dde = pclases.DatosDeLaEmpresa.select()[0]
            iva = dde.iva
        except IndexError:
            iva = 0.21
        tarifa = pclases.Tarifa.get_tarifa_defecto()
        for i in items:
            if tarifa:
                pvp = tarifa.obtener_precio(i) * (1 + iva)
            else:
                pvp = i.precioDefecto * (1 + iva)
            model.append((i.codigo,
                          i.descripcion,
                          utils.float2str(pvp),
                          i.get_puid()))

    def buscar(self, boton):
        a_buscar = self.wids['e_buscar'].get_text()
        productos = []
        for p in utils.buscar_productos_compra(a_buscar):
            productos.append(p)
        for p in utils.buscar_productos_venta(a_buscar):
            productos.append(p)
        if not len(productos) and len(a_buscar): 
            # Busca algo de texto pero no se encontró
            try:
                productos = self.sugerir_productos(a_buscar)
            except (ImportError, ValueError):
                utils.dialogo_info(titulo = "SIN RESULTADOS", 
                                   texto = "No se encontraron productos con el"
                                           "texto «%s»." % a_buscar, 
                                   padre = self.wids['ventana'])
        self.rellenar_tabla(productos)

    def sugerir_productos(self, txt):
        """
        Intenta sugerir productos según el corrector Norving.
        """
        from lib import spelling
        palabras = []
        for pc in pclases.ProductoCompra.select():
            palabras.append(pc.codigo.lower())
            palabras.append(pc.descripcion.lower())
        for pc in pclases.ProductoVenta.select():
            palabras.append(pc.codigo.lower())
            palabras.append(pc.descripcion.lower())
        palabras = " ".join(palabras)
        corrector = spelling.SpellCorrector(palabras)
        sugerencia = corrector.correct(txt.lower())
        if sugerencia != txt:
            res = utils.dialogo(titulo = "SUGERENCIA DE BÚSQUEDA", 
                    texto="No se encontró «%s», ¿tal vez quiso decir «%s»?" % (
                            txt, sugerencia), 
                    padre = self.wids['ventana'])
            if res:
                res = ([p for p in utils.buscar_productos_compra(sugerencia)]+ 
                       [p for p in utils.buscar_productos_venta(sugerencia)])
            else:
                res = []
        else:
            raise ValueError, "Sin alternativas que sugerir."
        return res

    def limpiar_tv(self, boton):
        """
        Limpia el TreeView.
        """
        model = self.wids['tv_datos'].get_model()
        model.clear()

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        from informes.treeview2pdf import treeview2pdf
        from formularios.reports import abrir_pdf
        strfecha = utils.str_fecha(mx.DateTime.localtime())
        informe = treeview2pdf(self.wids['tv_datos'], 
                        titulo="Listado de productos con PVP (IVA incluido)", 
                        fecha = strfecha) 
        if informe:
            abrir_pdf(informe)

if __name__ == '__main__':
    t = ListadoProductos()
