#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado,                   #
#                          (pacoqueen@users.sourceforge.net)                  #
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
## consulta_existencias_por_producto.py 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade
try:
    import pclases
except ImportError:
    import sys
    from os.path import join as pathjoin
    sys.path.append(pathjoin("..", "framework"))
    import pclases
import mx, mx.DateTime
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes

class ConsultaExistenciasPorAlmacen(Ventana):

    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'consulta_existencias_por_almacen.glade', 
                         objeto)
        while self.wids['notebook'].get_n_pages() > 1:
            self.wids['notebook'].remove_page(-1)
        self.wids['notebook'].set_tab_label_text(self.wids["scrolledwindow1"], 
                                                 "Por producto")
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_exportar/clicked': self.exportar}
        self.add_connections(connections)
        cols = [('Código', 'gobject.TYPE_STRING', False, True, False, None),
                ('Producto', 'gobject.TYPE_STRING', False, True, True, None),
                ("Total", "gobject.TYPE_STRING", False, True, False, None), 
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None)]
        for a in pclases.Almacen.select(pclases.Almacen.q.activo == True, 
                                        orderBy = "-id"):
            # Por cada almacén una columna en el treeview 
            cols.insert(2, (a.nombre, "gobject.TYPE_STRING", 
                            False, True, False, None))
            # ...y una hoja más en el notebook
            self.add_hoja_notebook(a)
        utils.preparar_listview(self.wids['tv_por_producto'], cols)
        self.wids['tv_por_producto'].connect("row-activated", 
                                             self.abrir_producto)
        for numcol in range(2, len(cols)-1):
            self.wids['tv_por_producto'].get_column(numcol).get_cell_renderers()[0].set_property('xalign', 1) 
        self.wids['ventana'].maximize()
        tipos = [(tdm.id, tdm.descripcion) for tdm in pclases.TipoDeMaterial.select(orderBy = "descripcion")]
        tipos.insert(0, (0, "Todos los productos"))
        tipos.insert(1, (-1, "Todos los productos de venta"))
        tipos.insert(2, (-2, "Todos los productos de compra"))
        utils.rellenar_lista(self.wids['cbe_tipo'], tipos)
        utils.combo_set_from_db(self.wids['cbe_tipo'], 0)
        gtk.main()

    def add_hoja_notebook(self, almacen):
        """
        Añade una hoja al notebook "notebook" con el nombre del almacén "a" y 
        un listview cuyo nombre será "tv_aID", donde ID será el identificador 
        -clave primaria- del almacén.
        """
        contenedor = gtk.ScrolledWindow()
        tv = gtk.TreeView()
        contenedor.add_with_viewport(tv)
        cols = (('Código', 'gobject.TYPE_STRING', False, True, False, None),
                ('Producto', 'gobject.TYPE_STRING', False, True, True, None),
                ("Total", "gobject.TYPE_STRING", False, True, False, None), 
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(tv, cols)
        tv.connect("row-activated", self.abrir_producto)
        tv.get_column(2).get_cell_renderers()[0].set_property('xalign', 1) 
        self.wids['notebook'].insert_page(contenedor, 
                                          gtk.Label(almacen.nombre), 1)
        contenedor.show_all()
        tv.set_property("name", "tv_%d" % almacen.id)
        self.wids['tv_%d' % almacen.id] = tv
    
    def abrir_producto(self, tv, path, view_column):
        """
        Si es un producto, abre el producto.
        """
        model = tv.get_model()
        tipo, id = model[path][-1].split(":")
        try:
            id = int(id)
        except:
            txt = "%sconsulta_existencias_por_almacen.py::abrir_producto -> Excepción al convertir ID a entero: (tipo %s) %s." % (self.usuario and self.usuario + ": " or "", tipo, id)
            print txt
            self.logger.error(txt)
        else:
            if tipo == "PV":        # ProductoVenta 
                pv = pclases.ProductoVenta.get(id)
                if pv.es_rollo():
                    import productos_de_venta_rollos
                    v = productos_de_venta_rollos.ProductosDeVentaRollos(pv, usuario = self.usuario)
                elif pv.es_bala() or pv.es_bala_cable() or pv.es_bigbag():
                    import productos_de_venta_balas
                    v = productos_de_venta_balas.ProductosDeVentaBalas(pv, usuario = self.usuario)
                elif pv.es_especial():
                    import productos_de_venta_especial
                    v = productos_de_venta_especial.ProductosDeVentaEspecial(pv, usuario = self.usuario)
            elif tipo == "PC": 
                pc = pclases.ProductoCompra.get(id)
                import productos_compra
                v = productos_compra.ProductosCompra(pc, usuario = self.usuario)

    def chequear_cambios(self):
        pass

    def buscar(self, boton):
        """
        Busca todos los productos e introduce en los TreeViews las existencias 
        de los mismos. En total y por almacén.
        El total no lo calcula, se obtiene del total global (que debería 
        coincidir con el sumatorio de...).
        """
        tipo = utils.combo_get_value(self.wids['cbe_tipo'])
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        txtvpro = "Recuperando existencias por almacén..."
        i = 0.0
        vpro.set_valor(i, txtvpro)
        almacenes = pclases.Almacen.select(pclases.Almacen.q.activo == True, 
                                           orderBy = "id")
        itotal = (pclases.ProductoCompra.select(
                    pclases.ProductoCompra.q.obsoleto == False).count() 
                 + pclases.ProductoVenta.select().count())
        model = self.wids['tv_por_producto'].get_model()
        model.clear()
        for a in almacenes:
            self.wids['tv_%d' % a.id].get_model().clear()
        if tipo in (0, -2) or tipo > 0:
            for pc in pclases.ProductoCompra.select(
                    pclases.ProductoCompra.q.obsoleto == False):
                if ((tipo > 0 and pc.tipoDeMaterialID == tipo) 
                    or tipo in (0, -2)):
                    fila = [pc.codigo, pc.descripcion]
                    total = pc.existencias
                    for a in almacenes:
                        existencias_almacen = a.get_existencias(pc)
                        if existencias_almacen == None:
                            existencias_almacen = 0
                        fila.append(utils.float2str(existencias_almacen))
                        if existencias_almacen != 0:
                            self.wids['tv_%d' % a.id].get_model().append(
                                (pc.codigo, pc.descripcion, 
                                 utils.float2str(existencias_almacen), 
                                 pc.get_puid()))
                    fila.append(utils.float2str(total))
                    fila.append(pc.get_puid())
                    model.append(fila)
                txtvpro = "Recuperando existencias por almacén... (%s)" % (
                    pc.get_puid())
                i += 1
                vpro.set_valor(i/itotal, txtvpro)
        else:
            i += pclases.ProductoCompra.select(
                pclases.ProductoCompra.q.obsoleto == False).count()
        txtvpro = "Recuperando existencias por almacén..."
        if tipo in (0, -1):
            for pv in pclases.ProductoVenta.select():
                fila = [pv.codigo, pv.descripcion and pv.descripcion 
                        or pv.nombre]
                total = 0   # Sumaré los almacenes para no desperdiciar 
                            # tiempo de computación.
                for a in almacenes:
                    existencias_almacen = a.get_existencias(pv)
                    if existencias_almacen == None:
                        existencias_almacen = 0
                    total += existencias_almacen 
                    fila.append(utils.float2str(existencias_almacen))
                    if existencias_almacen != 0:
                        self.wids['tv_%d' % a.id].get_model().append(
                            (pv.codigo, 
                             pv.descripcion and pv.descripcion or pv.nombre, 
                             utils.float2str(existencias_almacen), 
                             pv.get_puid()))
                fila.append(utils.float2str(total))
                fila.append(pv.get_puid())
                model.append(fila)
                txtvpro = "Recuperando existencias por almacén... (%s)" % (
                    pv.get_puid())
                vpro.set_valor(i/itotal, txtvpro)
                i += 1
        else:
            i += pclases.ProductoVenta.select().count()
        vpro.ocultar()

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe.
        """
        pagina_activa = self.wids['notebook'].get_current_page()
        if pagina_activa == 0:
            tv = self.wids['tv_por_producto']
            titulo = "Existencias por almacén"
        else:
            pagina = 0
            almacenes = pclases.Almacen.select(pclases.Almacen.q.activo==True,
                                               orderBy = "id")
            for a in almacenes:
                pagina += 1
                if pagina == pagina_activa:
                    tv = self.wids['tv_%d' % a.id]
                    titulo = "Existencias por almacén: %s" % a.nombre
        from treeview2pdf import treeview2pdf
        from informes import abrir_pdf
        strfecha = "%s - %s" % (utils.str_fecha(mx.DateTime.localtime()), 
                                utils.str_hora(mx.DateTime.localtime()))
        fichpdf = treeview2pdf(tv, 
                               titulo = titulo,
                               fecha = strfecha)
        abrir_pdf(fichpdf)

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        import sys, os
        sys.path.append(os.path.join("..", "informes"))
        from treeview2csv import treeview2csv
        from informes import abrir_csv
        pagina_activa = self.wids['notebook'].get_current_page()
        if pagina_activa == 0:
            tv = self.wids['tv_por_producto']
        else:
            pagina = 0
            almacenes = pclases.Almacen.select(orderBy = "id")
            for a in almacenes:
                pagina += 1
                if pagina == pagina_activa:
                    tv = self.wids['tv_%d' % a.id]
        abrir_csv(treeview2csv(tv))


if __name__ == '__main__':
    t = ConsultaExistenciasPorAlmacen()

