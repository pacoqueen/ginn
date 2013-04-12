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
## resultados_fluidez.py - Resultados de pruebas de fluidez en MP. 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 26 de abril de 2006 -> Inicio
## 
###################################################################
## PLAN: No estaría mal mostrar valores estadísticos como la media
##       y la desviación típica de las pruebas.
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time
from framework import pclases
from informes import geninformes
from utils import _float as float
import mx, mx.DateTime

class ResultadosFluidez(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'resultados_fluidez.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_lote/clicked': self.set_mp,
                       'b_fecha/clicked': self.fecha,
                       'b_add/clicked': self.add,
                       'b_drop/clicked': self.drop, 
                       'b_imprimir/clicked': self.imprimir, 
                       'b_exportar/clicked': self.exportar
                      }
        self.add_connections(connections)
        self.activar_widgets(False)
        self.inicializar_ventana()
        self.producto = None
        gtk.main()

    # --------------- Funciones auxiliares ------------------------------
    def activar_widgets(self, valor):
        self.ws = ('e_codigo', 
                   'e_nombre',
                   'e_proveedor',
                   'e_fluidez',
                   'frame3', 
                   'e_fecha',
                   'e_resultado1',
                   'e_resultado2',
                   'e_mfi',
                   'e_silo',
                   'e_lote',
                   'tv_pruebas',
                   'b_add',
                   'b_drop',
                   'b_fecha')
        for i in self.ws:
            self.wids[i].set_sensitive(valor)
        if self.usuario:
            try:
                ventana = pclases.Ventana.select(
                    pclases.Ventana.q.fichero == "resultados_fluidez.py")[0]
                # OJO: HARCODED
            except IndexError:
                txt = "resultados_fibra::activar_widgets -> Ventana no encontrada en BD."
                print txt
                self.logger.error(txt)
            else:
                permiso = self.usuario.get_permiso(ventana)
                if not permiso or (not permiso.escritura 
                                   and self.usuario.nivel > 1):
                    #self.wids['tv_pruebas'].set_sensitive(False)
                    # Ya no se pueden editar valores en el TreeView, así que 
                    # no lo deshabilito para permitir ordenar por fecha.
                    self.wids['b_drop'].set_sensitive(False)
                if not permiso or (not permiso.nuevo 
                                   and self.usuario.nivel > 1):
                    self.wids['b_add'].set_sensitive(False)
     
    def crear_listviewes(self):
        tv = self.wids['tv_pruebas']
        #cols = (('Fecha análisis', 'gobject.TYPE_STRING', True, True, True, self.cambiar_fecha),
        #        ('MFI proveedor', 'gobject.TYPE_STRING', True, True, False, self.cambiar_mfi), 
        #        ('Lote', 'gobject.TYPE_STRING', True, True, False, self.cambiar_lote), 
        #        ('Silo', 'gobject.TYPE_STRING', True, True, False, self.cambiar_silo), 
        #        ('MFI laboratorio 1', 'gobject.TYPE_STRING', True, True, False, self.cambiar_resultado),
        #        ('MFI laboratorio 2', 'gobject.TYPE_STRING', True, True, False, self.cambiar_resultado),
        #        ('Media MFI laboratorio', 'gobject.TYPE_STRING', True, True, False, self.cambiar_resultado),
        #        ('ID1:ID2', 'gobject.TYPE_STRING', False, False, False, None))
        cols = (('Fecha análisis', 'gobject.TYPE_STRING', False, True, True, None),
                ('MFI proveedor', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Lote', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Silo', 'gobject.TYPE_STRING', False, True, False, None), 
                ('MFI laboratorio 1', 'gobject.TYPE_STRING', False, True, False, None),
                ('MFI laboratorio 2', 'gobject.TYPE_STRING', False, True, False, None),
                ('Media MFI lab.', 'gobject.TYPE_STRING', False, True, False, None),
                ('ID1:ID2', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(tv, cols)
        tv.get_column(1).get_cell_renderers()[0].set_property('xalign', 1) 
        tv.get_column(2).get_cell_renderers()[0].set_property('xalign', 0.5) 
        tv.get_column(3).get_cell_renderers()[0].set_property('xalign', 0.5) 
        tv.get_column(4).get_cell_renderers()[0].set_property('xalign', 0.9) 
        tv.get_column(5).get_cell_renderers()[0].set_property('xalign', 0.9) 
        tv.get_column(6).get_cell_renderers()[0].set_property('xalign', 0.9) 
        self.colorear(tv)
        tv = self.wids['tv_media']
        cols = (('Lote', 'gobject.TYPE_STRING', False, True, True, None),
                ('Fluidez media', 'gobject.TYPE_FLOAT', False, True, False, None),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(tv, cols)
        tv.get_column(1).get_cell_renderers()[0].set_property('xalign', 0.1) 

    def cambiar_lote(self, tv, path, texto):
        """
        Cambia el lote (texto en la BD, sin relación con ninguna otra entidad) por 
        el tecleado.
        """
        model = self.wids['tv_pruebas'].get_model()
        prueba = pclases.PruebaGranza.get(model[path][-1])
        prueba.lote = texto.strip()
        self.rellenar_pruebas()

    def cambiar_fecha_entrada(self, tv, path, texto):
        """
        Cambia la fecha de entrada en el resultado de fluidez.
        Debería ser la del albarán, pero como las pruebas se 
        realizan a veces en días diferentes a la entrada del 
        albarán, se guardan manualmente aquí también. Además, 
        no hay forma actualmente de relacionar una prueba con 
        un albarán concreto.
        """
        model = self.wids['tv_pruebas'].get_model()
        prueba = pclases.PruebaGranza.get(model[path][-1])
        try:
            prueba.fechaEntrada = utils.parse_fecha(texto)
        except:
            utils.dialogo_info('FECHA INCORRECTA', 
                               'La fecha introducida (%s) no es correcta.' % texto, 
                               padre = self.wids['ventana'])
        self.rellenar_pruebas()

    def cambiar_mfi(self, tv, path, texto):
        """
        I don't need no educ^H^H^H^H explanation.
        """
        model = self.wids['tv_pruebas'].get_model()
        prueba = pclases.PruebaGranza.get(model[path][-1])
        texto = texto.replace(",", ".")
        try:
            prueba.mfi = float(texto)
        except:
            utils.dialogo_info('RESULTADO INCORRECTO',
                               'El número tecleado (%s) no es correcto.\nDebe introducir exclusivamente una cantidad numércica, sin unidades\nde medida y usando únicamente el punto como signo de separación decimal.' % texto,
                               padre = self.wids['ventana'])
        self.rellenar_pruebas()

    def inicializar_ventana(self):
        """
        Inicializa los widgets de la ventana.
        """
        self.crear_listviewes()

    def colorear(self, tv):
        """
        Colorea el listview dependiendo de si la cantidad pendiente de 
        servir es superior a las existencias en almacén.
        """
        def cell_func(column, cell, model, itr, colgtx = 4):
            """
            Si la fluidez que ha dado es superior a la del fabricante, 
            la colorea en azul. Si es inferior la colorea en rojo y 
            si es igual, la colorea en verde.
            """
            fgtx = model[itr][colgtx]
            fpro = model[itr][1] 
            if fgtx > fpro:
                color = "blue"
            elif fgtx < fpro:
                color = "red"
            else:
                color = "green"
            cell.set_property("foreground", color)
        cols = tv.get_columns()
        for i in (4, 5):
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell, cell_func, i)
        column = cols[1]
        cells = column.get_cell_renderers()
        for cell in cells:
            cell.set_property("foreground", "green")


    def rellenar_pruebas(self):
        """
        Introduce en el treeview las pruebas del producto seleccionado y 
        muestra la media.
        PRECONDICIÓN: El producto no puede ser None.
        """
        model = self.wids['tv_pruebas'].get_model()
        model.clear()
        self.calcular_caracteristicas()
        pruebas = pclases.PruebaGranza.select(
            pclases.PruebaGranza.q.productoCompraID == self.producto.id)
        pruebas = list(pruebas)
        pruebas.sort(lambda x, y: int(x.id - y.id))
        for i in range(0, len(pruebas), 2):
            prueba1 = pruebas[i]
            try:
                prueba2 = pruebas[i+1]
            except IndexError:
                prueba2 = None
            if prueba2 != None:
                fila = (utils.str_fecha(prueba2.fecha), 
                        "%.2f gr/10 min." % prueba2.mfi, 
                        prueba2.lote, 
                        prueba2.silo, 
                        "%.2f gr/10 min." % prueba1.resultado, 
                        "%.2f gr/10 min." % prueba2.resultado, 
                        "%.2f gr/10 min." % (
                            (prueba1.resultado+prueba2.resultado)/2.0),
                        "%d:%d" % (prueba1.id, prueba2.id))
            else:
                fila = (utils.str_fecha(prueba2.fecha), 
                        "%.2f gr/10 min." % prueba2.mfi, 
                        prueba2.lote, 
                        prueba2.silo, 
                        "%.2f gr/10 min." % prueba1.resultado, 
                        "-", 
                        "%.2f gr/10 min." % prueba1.resultado,
                        "%d:%d" % (prueba1.id, 0))
            model.append(fila)
            
    def calcular_caracteristicas(self):
        """
        Calcula la media de las pruebas de fluidez del producto.
        """
        producto = self.producto
        media = 0.0
        porlote = {}
        for p in producto.pruebasGranza:
            media += p.resultado
            if p.lote not in porlote:
                porlote[p.lote] = [p.resultado]
            else:
                porlote[p.lote].append(p.resultado)
        try:
            media /= len(producto.pruebasGranza)
        except ZeroDivisionError:
            media = 0.0
        for lote in porlote:
            try:
                porlote[lote] = sum(porlote[lote]) / len(porlote[lote])
            except ZeroDivisionError:
                porlote[lote] = 0.0
        self.rellenar_info_producto(media, porlote)

    def actualizar_ventana(self):
        """
        Método que sobreescribe el "actualizar_ventana" que hereda de la clase ventana.
        PRECONDICION: self.producto no puede ser None
        """
        try:
            self.producto.sync()
            self.rellenar_widgets()
        except pclases.SQLObjectNotFound:
                utils.dialogo_info(titulo = 'REGISTRO ELIMINADO', texto = 'El registro ha sido borrado desde otro puesto.')
                self.producto = None
        self.activar_widgets(self.producto!=None)


    # --------------- Manejadores de eventos ----------------------------
    def add(self, w):
        if self.producto != None:
            fecha = self.wids['e_fecha'].get_text()
            if fecha == '':
                utils.dialogo_info(titulo = 'SIN FECHA',
                                   texto = 'Debe introducir la fecha del resultado de la prueba.')
                return
            resultado1 = self.wids['e_resultado1'].get_text()
            if resultado1 == '':
                utils.dialogo_info(titulo = 'SIN RESULTADO',
                                   texto = 'Debe introducir el resultado de la prueba en resultado1.', 
                                   padre = self.wids['ventana'])
                return
            resultado2 = self.wids['e_resultado2'].get_text()
            try:
                mfi = utils._float(self.wids['e_mfi'].get_text())
            except:
                utils.dialogo_info(titulo = "MFI INCORRECTO", 
                    texto = "No ha introducido un valor correcto para el MFI del proveedor.", 
                    padre = self.wids['ventana'])
                return
            try:
                resultado = float(resultado1)
                prueba = pclases.PruebaGranza(fecha = utils.parse_fecha(fecha),
                                                         resultado = resultado,
                                                productoCompra = self.producto, 
                                        fechaEntrada = mx.DateTime.localtime(), 
                                         silo = self.wids['e_silo'].get_text(), 
                                         lote = self.wids['e_lote'].get_text(), 
                                                                     mfi = mfi)
                pclases.Auditoria.nuevo(prueba, self.usuario, __file__)
                if resultado2:
                    try:
                        resultado = float(resultado2)
                        prueba = pclases.PruebaGranza(
                            fecha = utils.parse_fecha(fecha),
                            resultado = resultado,
                            productoCompra = self.producto, 
                            fechaEntrada = mx.DateTime.localtime(), 
                            silo = self.wids['e_silo'].get_text(), 
                            lote = self.wids['e_lote'].get_text(),
                            mfi = mfi)
                        pclases.Auditoria.nuevo(prueba, self.usuario, __file__)
                    except Exception, msg:
                        utils.dialogo_info(titulo = 'ERROR', 
                                           texto = 'Verifique que ha introducido los datos correctamente.\n\n\nInformación de depuración: %s' % (msg), 
                                           padre = self.wids['ventana'])
            except Exception, msg:
                utils.dialogo_info(titulo = 'ERROR', 
                                   texto = 'Verifique que ha introducido los datos correctamente.\n\n\nInformación de depuración: %s' % (msg), 
                                   padre = self.wids['ventana'])
            self.wids['e_fecha'].set_text(utils.str_fecha(time.localtime()))
            self.wids['e_resultado1'].set_text('')
            self.wids['e_resultado2'].set_text('')
            self.wids['e_lote'].set_text('')
            self.wids['e_silo'].set_text('')
            self.wids['e_mfi'].set_text('0')
            self.rellenar_pruebas()
        else:
            txt = "WARNING: Se ha intentano añadir una prueba con producto None"
            self.logger.warning("%s%s" % (
                self.usuario and self.usuario.usuario + ": " or "", txt))
    
    def drop(self, w):
        model, iter = self.wids['tv_pruebas'].get_selection().get_selected()
        if iter != None and utils.dialogo(titulo = 'BORRAR PRUEBA', texto = '¿Está seguro?'):
            id1, id2 = [int(i) for i in model[iter][-1].split(":")]
            prueba = pclases.PruebaGranza.get(id1)
            prueba.destroy(ventana = __file__)
            if id2 > 0:
                prueba = pclases.PruebaGranza.get(id2)
                prueba.destroy(ventana = __file__)
            self.rellenar_pruebas()

    def proveedores(self, p):
        """
        Devuelve una cadena con los proveedores de un 
        producto separados por coma.
        """
        # OJO: Esto puede ser bastante lento.
        provs = []
        for ldc in p.lineasDeCompra:
            if (ldc.pedidoCompra and ldc.pedidoCompra.proveedor 
                and ldc.pedidoCompra.proveedor.nombre not in provs):
                provs.append(ldc.pedidoCompra.proveedor.nombre)
        return ', '.join(provs)

    def set_mp(self, w):
        a_buscar = utils.dialogo_entrada(titulo = 'BUSCAR PRODUCTO', 
                                texto = 'Introduzca código o descripción:', 
                                padre = self.wids['ventana'])
        if a_buscar != None:
            try:
                materiaprima = pclases.TipoDeMaterial.select(
                    pclases.TipoDeMaterial.q.descripcion.contains("prima"))[0]
            except IndexError:
                prods = pclases.ProductoCompra.select(
                    pclases.AND(
                     pclases.OR(
                      pclases.ProductoCompra.q.codigo.contains(a_buscar), 
                      pclases.ProductoCompra.q.descripcion.contains(a_buscar)),
                     pclases.ProductoCompra.q.obsoleto == False))
            else:
                prods = pclases.ProductoCompra.select(
                  pclases.AND(
                    pclases.OR(
                      pclases.ProductoCompra.q.codigo.contains(a_buscar), 
                      pclases.ProductoCompra.q.descripcion.contains(a_buscar)
                    ), 
                    pclases.ProductoCompra.q.tipoDeMaterialID==materiaprima.id,
                    pclases.ProductoCompra.q.obsoleto == False
                  )
                )
            if prods.count() == 0:
                utils.dialogo_info(titulo = 'PRODUCTO NO ENCONTRADO', 
                    texto = 'No se encontró ningún producto al buscar "%s"\n'
                            'en código y descripción.' % a_buscar, 
                    padre = self.wids['ventana'])
                return
            elif prods.count() > 1:
                filas = [(l.id, l.codigo, l.descripcion, self.proveedores(l)) 
                         for l in prods]
                # CWT: Esto es probablemente lo más guarro que he hecho nunca:
                if "050" in a_buscar:
                    filas = [i for i in filas 
                             if "SACOS" in i[2] or "GRANEL" in i[2]]
                idprod = utils.dialogo_resultado(filas, 
                    titulo = 'SELECCIONE PRODUCTO',
                    cabeceras = ('ID', 'Código', 'Descripción', 'Proveedor'), 
                    padre = self.wids['ventana'])
                if idprod < 0:
                    return
                prod = pclases.ProductoCompra.get(idprod)
            else:
                prod = prods[0]
            self.producto = prod
            self.actualizar_ventana()
    
    def rellenar_widgets(self):
        self.activar_widgets(self.producto != None)
        if self.producto != None:
            self.rellenar_info_producto()
            self.rellenar_pruebas()
            self.wids['e_fecha'].set_text(utils.str_fecha(time.localtime()))
            self.wids['e_resultado1'].set_text('')
            self.wids['e_resultado2'].set_text('')
            self.wids['e_lote'].set_text('')
            self.wids['e_mfi'].set_text('')
            self.wids['e_silo'].set_text('')

    def rellenar_info_producto(self, fluidez = 0.0, porlote = {}):
        """
        PRECONDICIÓN: self.producto != None
        """
        producto = self.producto
        self.wids['e_codigo'].set_text(self.producto.codigo)
        self.wids['e_nombre'].set_text(self.producto.descripcion)
        self.wids['e_proveedor'].set_text(self.proveedores(self.producto))
        self.wids['e_fluidez'].set_text("%.2f" % fluidez)
        model = self.wids['tv_media'].get_model()
        model.clear()
        for lote in porlote:
            model.append((lote, porlote[lote], 0))

    def fecha(self, w):
        self.wids['e_fecha'].set_text(utils.str_fecha(utils.mostrar_calendario(fecha_defecto = self.objeto and self.objeto.fecha or None, padre = self.wids['ventana'])))

    def cambiar_fecha(self, cell, path, texto):
        model = self.wids['tv_pruebas'].get_model()
        prueba = pclases.PruebaGranza.get(model[path][-1])
        try:
            prueba.fecha = time.strptime(texto, '%d/%m/%Y')
        except:
            utils.dialogo_info('FECHA INCORRECTA', 
                               'La fecha introducida (%s) no es correcta.' % texto, 
                               padre = self.wids['ventana'])
        self.rellenar_pruebas()

    def cambiar_silo(self, tv, path, texto):
        """
        Cambia el silo de descarga. Se guarda como texto. No está relacionado 
        con los "Silo" de la BD. (Aunque debería, pero como se hicieron en dos 
        momentos diferentes, aún no existía esa tabla.)
        """
        model = self.wids['tv_pruebas'].get_model()
        prueba = pclases.PruebaGranza.get(model[path][-1])
        prueba.silo = texto
        model[path][2] = prueba.silo
        # self.rellenar_pruebas()

    def cambiar_resultado(self, tv, path, texto):
        model = self.wids['tv_pruebas'].get_model()
        prueba = pclases.PruebaGranza.get(model[path][-1])
        texto = texto.replace(",", ".")
        try:
            prueba.resultado = float(texto)
        except:
            utils.dialogo_info('RESULTADO INCORRECTO',
                               'El número tecleado (%s) no es correcto.\nDebe introducir exclusivamente una cantidad numércica, sin unidades\nde medida y usando únicamente el punto como signo de separación decimal.' % texto,
                               padre = self.wids['ventana'])
        self.rellenar_pruebas()

    def imprimir(self, boton):
        """
        "Vuerca-vuerca" el TreeView en un PDF.
        """
        from informes.treeview2pdf import treeview2pdf
        from formularios.reports import abrir_pdf
        strfecha = utils.str_fecha(mx.DateTime.localtime())
        tv = self.wids['tv_pruebas']
        desc_prod = self.wids['e_nombre'].get_text()
        abrir_pdf(treeview2pdf(tv, 
                               titulo = "Resultados fluidez %s" % desc_prod, 
                               fecha = strfecha, 
                               apaisado = False))

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        tv = self.wids['tv_pruebas']
        abrir_csv(treeview2csv(tv))


if __name__=='__main__':
    a = ResultadosFluidez()
    #a = ResultadosFluidez(usuario = pclases.Usuario.selectBy(
    #    usuario = "jmadrid")[0])

