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
## balas_cable.py - Alta de balas de cable (fibra reciclada prensa)
###################################################################
## NOTAS:
## 
###################################################################
## Changelog:
## 20 de junio de 2007 -> Inicio
## 
###################################################################
## TODO: 
## - ¿Y si tienen que tirar de material de embalar? ¿Abren un 
##   parte del otro o qué?
## - Queda también adaptar los abonos por si el cliente devuelve 
##   alguna bala de cable. Bueno, en ese caso mejor casi que se 
##   reetiqueta y santas pascuas, ¿no?
###################################################################
## NOTAS: 
## 
###################################################################
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
import mx.DateTime
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes
from ventana_progreso import VentanaProgreso


class BalasCable(Ventana):

    def __init__(self, objeto = None, usuario = None):
        self.usuario = usuario
        Ventana.__init__(self, 'balas_cable.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_aplicar/clicked': self.actualizar_tabla, 
                       'b_add/clicked': self.crear_bala, 
                       'b_drop/clicked': self.drop_or_print, 
                       'b_etiqueta/clicked': self.drop_or_print, 
                       'b_mes/clicked': self.cambiar_mes_acumulado
                       }
        self.add_connections(connections)
        productos_cable = []
        for ceb in pclases.CamposEspecificosBala.select(pclases.CamposEspecificosBala.q.reciclada == True):
            productos_cable.append((ceb.productosVenta[0].id, ceb.productosVenta[0].descripcion))
        productos_cable.sort(lambda p1, p2: (p1[-1] < p2[-1] and -1) or (p1[-1] > p2[-1] and 1) or 0)
        utils.rellenar_lista(self.wids['cbe_producto'], productos_cable)
        self.wids['sp_ver'].set_value(15)
        self.preparar_tv(self.wids['tv_balas'])
        self.actualizar_tabla()
        gtk.main()

    def drop_or_print(self, boton):
        """
        Recupera los objetos bala y genera las etiquetas 
        en PDF o los elimina, dependiendo del botón que 
        haya invocado al callback.
        """
        model, paths = self.wids['tv_balas'].get_selection().get_selected_rows()
        if paths != None and paths != []:
            balas = []
            for p in paths:
                idb = model[p][-1]
                balas.append(pclases.BalaCable.get(idb))
            if "etiqueta" in boton.name:
                self.generar_etiquetas(balas)
            elif "drop" in boton.name:
                if utils.dialogo(titulo = "¿BORRAR?", 
                                 texto = "¿Está seguro de eliminar las balas seleccionadas?", 
                                 padre = self.wids['ventana']):
                    self.borrar_balas(balas)

    def generar_etiquetas(self, balas):
        """
        Genera una lista de diccionarios con los datos de las balas 
        para generar sus etiquetas.
        """
        from listado_balas import preparar_datos_etiquetas_balas_cable
        data = preparar_datos_etiquetas_balas_cable(balas)
        if data:
            from ginn.formularios import reports as informes
            informes.abrir_pdf(geninformes.etiquetasBalasCableEtiquetadora(data))

    def borrar_balas(self, balas):
        """
        Elimina las balas recibidas y actualiza la ventana.
        """
        for b in balas:
            a = b.articulo
            a.balaCable = None
            try:
                a.destroy(ventana = __file__)
            except Exception, msg:
                self.logger.error("%sbalas_cable::borrar_balas -> Artículo ID %d de bala ID %d (%s) no se pudo eliminar. Excepción: %s" 
                    % (self.usuario and self.usuario.usuario + ": " or "", a.id, b.id, b.codigo, msg))
                a.balaCable = b
            else:
                try:
                    b.destroy(ventana = __file__)
                except Exception, msg:
                    self.logger.error("%sbalas_cable::borrar_balas -> Bala ID %d (%s) no se pudo eliminar. Excepción: %s" 
                        % (self.usuario and self.usuario.usuario + ": " or "", b.id, b.codigo, msg))
                    try:
                        b.destroy_en_cascada(ventana = __file__)
                    except Exception, msg:
                        self.logger.error("%sbalas_cable::borrar_balas -> Bala ID %d (%s) no se pudo eliminar en cascada. Excepción: %s" 
                            % (self.usuario and self.usuario.usuario + ": " or "", b.id, b.codigo, msg))
        self.actualizar_tabla()

    def crear_bala(self, boton = None, peso = None):
        """
        Crea una bala del producto mostrado en pantalla e introduce 
        su información en el TreeView. El peso lo solicita en una 
        ventana de diálogo.
        Si se recibe peso, debe ser un float.
        """
        # TODO: Hacer que el peso lo tome del puerto serie y se le pase a 
        # esta función.
        producto = utils.combo_get_value(self.wids['cbe_producto'])
        if producto == None:
            utils.dialogo_info(titulo = "SELECCIONE UN PRODUCTO", 
                    texto = "Debe seleccionar un producto en el desplegable.", 
                    padre = self.wids['ventana'])
        else:
            if peso == None:
                peso = utils.dialogo_entrada(titulo = "PESO", 
                                             texto = "Introduzca peso:", 
                                             padre = self.wids['ventana'], 
                                             valor_por_defecto = "0")
                try:
                    peso = utils._float(peso)
                except ValueError:
                    utils.dialogo_info(titulo = "ERROR", 
                                       texto = "El valor tecleado %s no es correcto." % (peso), 
                                       padre = self.wids['ventana'])
                    peso = 0
            nueva_bala = self.crear_objeto_bala(producto, peso)
            if nueva_bala == None:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "La bala no se pudo crear. Inténtelo de nuevo.", 
                                   padre = self.wids['ventana'])
            else:
                self.add_nueva_bala_tv(nueva_bala)
                try:
                    totpantalla = utils.parse_float(
                        self.wids['e_pantalla'].get_text())
                except:
                    totpantalla = 0.0
                totpantalla += peso
                self.rellenar_totales(totpantalla)

    def crear_objeto_bala(self, producto, peso):
        """
        Crea una nueva bala de cable y su artículo relacionado.
        """
        b = pclases.BalaCable(peso = peso)
        pclases.Auditoria.nuevo(b, self.usuario, __file__)
        try:
            a = pclases.Articulo(balaCable = b, 
                            bala = None, 
                            bigbag = None, 
                            rollo = None, 
                            fechahora = mx.DateTime.localtime(), 
                            productoVenta = producto, 
                            parteDeProduccion = None, 
                            albaranSalida = None, 
                            almacen = pclases.Almacen.get_almacen_principal())
            pclases.Auditoria.nuevo(a, self.usuario, __file__)
        except:
            b.destroy(ventana = __file__)
            b = None
        return b

    def add_nueva_bala_tv(self, bala):
        """
        Introduce la bala al final del TreeView y lo desplaza.
        """
        model = self.wids['tv_balas'].get_model()
        fila = (utils.str_fechahora(bala.fechahora), 
                bala.codigo, 
                utils.float2str(bala.peso, 1), 
                bala.productoVenta.descripcion, 
                bala.observaciones, 
                bala.id)
        model.append(fila)
        self.mover_al_final(self.wids['tv_balas'])

    def actualizar_tabla(self, boton = None):
        """
        Actualiza la información completa de la tabla, 
        volviendo a buscar las balas e introduciéndolas 
        en el TreeView.
        """
        balas = self.buscar()
        self.rellenar_tabla(balas)

    def chequear_cambios(self):
        pass

    def buscar(self):
        """
        Inicia la consulta para el año indicado en el widget y 
        rellena las tablas con la información obtenida.
        """
        cuantas = int(self.wids['sp_ver'].get_value())
        balas = []
        n = 0
        qbalas = pclases.BalaCable.select(orderBy = "-id")
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        if cuantas == 0:
            tot = qbalas.count() * 1.0
        else:
            tot = cuantas * 1.0
        for b in qbalas:
            b.sync()        
                # Con 999 balas se gana únicamente 1 segundo si omito 
                # la sincronización.
            try:
                balas.insert(0, (b, b.productoVenta))       
                    # Para optimizar los accesos a la BD cacheo los datos aquí.
            except:     # ¿Bala sin producto de venta? Mal asunto
                balas.insert(0, (b, None))
            vpro.set_valor(n/tot, 'Recuperando bala %s' % (b.codigo))
            n += 1
            if n == cuantas:
                break
        vpro.set_valor(1, 'Actualizando ventana...')
        vpro.ocultar()
        return balas

    def rellenar_tabla(self, balas):
        """
        Introduce las balas recibidas en el TreeView «tv» y lo 
        desplaza a la última fila (la más baja)
        """
        tv = self.wids['tv_balas']
        model = tv.get_model()
        tv.freeze_child_notify()
        tv.set_model(None)
        model.clear()
        totpantalla = 0.0
        for bala, producto in balas:
            if producto != None:
                desc = producto.descripcion
            else:
                desc = "?"
            fila = (utils.str_fechahora(bala.fechahora), 
                    bala.codigo, 
                    utils.float2str(bala.peso, 1), 
                    desc, 
                    bala.observaciones, 
                    bala.id)
            model.append(fila)
            totpantalla += bala.peso_sin
        tv.set_model(model)
        tv.thaw_child_notify()
        self.rellenar_totales(totpantalla)
        self.mover_al_final(self.wids['tv_balas'])

    def cambiar_mes_acumulado(self, boton):
        """
        Permite seleccionar un mes y un año. Después rellena los totales 
        de nuevo usando ese mes y año para el acumulado del mes.
        No se almacenan mes y año, de modo que en cuanto se refresque la 
        pantalla volverá al mes y año actual.
        """
        mes_actual = mx.DateTime.today().month
        meses = zip(range(1, 13), ("enero", 
                                   "febrero", 
                                   "marzo", 
                                   "abril", 
                                   "mayo", 
                                   "junio", 
                                   "julio", 
                                   "agosto", 
                                   "septiembre", 
                                   "octubre", 
                                   "noviembre", 
                                   "diciembre"))
        mes = utils.dialogo_combo(titulo = "MES", 
                                  texto = "Seleccione mes:", 
                                  ops = meses, 
                                  padre = self.wids['ventana'],
                                  valor_por_defecto = mes_actual)
        if mes != None:
            anno_actual = mx.DateTime.today().year
            anno = utils.dialogo_entrada(titulo = "AÑO", 
                                         texto = "Introduzca año:", 
                                         valor_por_defecto = str(anno_actual), 
                                         padre = self.wids['ventana'])
            try:
                anno = int(anno)
            except:
                anno = None
            if anno != None:
                if anno < 100:
                    anno += 2000
                self.rellenar_totales(None, mes, anno)

    def rellenar_totales(self, totpantalla, mes = None, anno = None):
        """
        Rellena los "entries" de totales:
        - En pantalla. Se recibe. Si es None no cambia el valor que haya en 
                       el entry.
        - Acumulado de todas.
        - Acumulado del mes.
        """
        totacum = pclases.BalaCable.calcular_acumulado_peso_sin()
        if mes == None or not isinstance(mes, int):
            mes = mx.DateTime.localtime().month
        if anno == None or not isinstance(anno, int):
            anno = mx.DateTime.localtime().year
        self.wids['label4'].set_text("Total mes:\n<small><i>%02d/%d</i></small>" % (
            mes, anno))
        self.wids['label4'].set_use_markup(True)
        totmes = pclases.BalaCable.calcular_acumulado_mes_peso_sin(mes, anno)
        if totpantalla != None:
            self.wids['e_pantalla'].set_text("%s kg" 
                % utils.float2str(totpantalla))
        self.wids['e_mes'].set_text("%s kg" % utils.float2str(totmes))
        self.wids['e_acumulado'].set_text("%s kg" % utils.float2str(totacum))

    def mover_al_final(self, tv):
        """
        Mueve la selección del TreeView a la última fila.
        """
        model = tv.get_model()
        try:
            last_iter = model.get_iter(model[-1].path)
        except IndexError:  # No hay balas que mostrar:
            return
        sel = tv.get_selection()
        sel.select_iter(last_iter)
        tv.scroll_to_cell(model[-1].path, use_align = True)

    def preparar_tv(self, tv):
        """
        Prepara las columnas del TreeView.
        """
        cols = (('Fecha y hora', 'gobject.TYPE_STRING', False, True, False, None),
                ('Código', 'gobject.TYPE_STRING', False, True, True, None),
                ('Peso', 'gobject.TYPE_STRING', True, True, False, self.cambiar_peso), 
                ('Color', 'gobject.TYPE_STRING', False, False, False, None), 
                ('Observaciones', 'gobject.TYPE_STRING', True, False, False, self.cambiar_observaciones),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(tv, cols)
        for col in tv.get_columns()[2:3]:
            for cell in col.get_cell_renderers():
                cell.set_property("xalign", 1.0)
            col.set_alignment(0.5)
        self.wids['tv_balas'].get_selection().set_mode(gtk.SELECTION_MULTIPLE)

    def cambiar_peso(self, cell, path, texto):
        """
        Cambia el peso de la bala editada.
        """
        try:
            peso = utils._float(texto)
        except ValueError:
            utils.dialogo_info(titulo = "ERROR", 
                               texto = "El valor tecleado %s no es correcto." % (peso), 
                               padre = self.wids['ventana'])
        else:
            model = self.wids['tv_balas'].get_model()
            try:
                bala = pclases.BalaCable.get(model[path][-1])
            except:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "No se pudo acceder a la bala.", 
                                   padre = self.wids['ventana'])
                self.actualizar_tabla()
            else:
                difpeso = bala.peso - peso
                bala.peso = peso
                bala.syncUpdate()
                model[path][2] = utils.float2str(bala.peso, 1) 
                try:
                    totpantalla = utils.parse_float(
                        self.wids['e_pantalla'].get_text())
                except:
                    totpantalla = 0.0
                totpantalla -= difpeso
                self.rellenar_totales(totpantalla)
    
    def cambiar_observaciones(self, cell, path, texto):
        """
        Cambia las observaciones de la bala de la fila editada.
        """
        model = self.wids['tv_balas'].get_model()
        try:
            bala = pclases.BalaCable.get(model[path][-1])
        except:
            utils.dialogo_info(titulo = "ERROR", 
                               texto = "No se pudo acceder a la bala.", 
                               padre = self.wids['ventana'])
            self.actualizar_tabla()
        else:
            bala.observaciones = texto
            model[path][4] = bala.observaciones

################################################################################

if __name__ == '__main__':
    v = BalasCable() 


