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
## rollos_c.py - Alta de rollos «C».
###################################################################
## NOTAS:
## 
###################################################################
## Changelog:
## 2 de junio de 2008 -> Inicio
## 
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
import mx.DateTime
from informes import geninformes
from ventana_progreso import VentanaProgreso

def descontar_material_adicional(ventana_parte, articulo, restar = True):
    """
    Descuenta el material adicional correspondiente al artículo según 
    la formulación que indique la línea de fabricación.
    Si "restar" es True, descuenta. Si es False, añade la cantidad (para
    cuando se elimine un rollo del parte, por ejemplo).
    Si es necesario, se dejará material con existencias en negativo, aunque
    se avisará al usuario de la incidencia.
    """
    producto = articulo.productoVenta
    # OJO: Debe llamarse "plastico", tal cual, sin acentos ni nada. No es lo 
    # suyo, pero al menos hemos reducido el número de casos especiales.
    for consumoAdicional in producto.consumosAdicionales:
        consumido = consumoAdicional.consumir(articulo, cancelar = not restar)
        ventana_parte.logger.warning("Rollos C (%s-%s): Consumiendo %s de %s para el rollo C %s. Existencias: %s" % (
            utils.str_fecha(articulo.fechahora), 
            utils.str_hora_corta(articulo.fechahora), 
            utils.float2str(consumido), 
            consumoAdicional.productoCompra.descripcion, 
            articulo.codigo, 
            utils.float2str(consumoAdicional.productoCompra.existencias)))
    # OJO: ¿TODO?: Estos consumos no generan albaranes internos.
    #actualizar_albaran_interno_con_tubos(ventana_parte.objeto)

class RollosC(Ventana):

    def __init__(self, objeto = None, usuario = None):
        self.usuario = usuario
        Ventana.__init__(self, 'rollos_c.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_aplicar/clicked': self.actualizar_tabla, 
                       'b_add/clicked': self.crear_rollo, 
                       'b_drop/clicked': self.drop_or_print, 
                       'b_etiqueta/clicked': self.drop_or_print, 
                       'b_mes/clicked': self.cambiar_mes_acumulado
                       }
        self.add_connections(connections)
        productos_gtxc = []
        for cer in pclases.CamposEspecificosRollo.select(
            pclases.CamposEspecificosRollo.q.c == True):
            try:
                productos_gtxc.append((cer.productosVenta[0].id, 
                                       cer.productosVenta[0].descripcion))
            except IndexError:  # Producto mal borrado, CER desparejado.
                mensaje = "%srollos_c::__init__ -> CamposEspecificosRollo ID %d sin productosVenta. Intento eliminar." % (self.usuario and self.usuario.usuario + ": " or "", cer.id)
                self.logger.error(mensaje)
                print mensaje
                if not cer.productosVenta:  # Sobra. Lo borro.
                    try:
                        cer.destroy(ventana = __file__)
                    except Exception, msg:
                        mensaje = "%srollos_c::__init__ -> CamposEspecificosRollo ID %d sin productosVenta no se pudo eliminar. Excepción: %s" % (self.usuario and self.usuario.usuario + ": " or "", cer.id, msg)
                        print mensaje
                        self.logger.error(mensaje)
        productos_gtxc.sort(lambda p1, p2: (p1[-1] < p2[-1] and -1) or (p1[-1] > p2[-1] and 1) or 0)
        utils.rellenar_lista(self.wids['cbe_producto'], productos_gtxc)
        if len(productos_gtxc) > 0:
            utils.combo_set_from_db(self.wids['cbe_producto'], 
                                    productos_gtxc[0][0])
        self.wids['sp_ver'].set_value(15)
        self.preparar_tv(self.wids['tv_rollos'])
        self.actualizar_tabla()
        gtk.main()

    def drop_or_print(self, boton):
        """
        Recupera los objetos rollo y genera las etiquetas 
        en PDF o los elimina, dependiendo del botón que 
        haya invocado al callback.
        """
        model,paths=self.wids['tv_rollos'].get_selection().get_selected_rows()
        if paths != None and paths != []:
            rollos = []
            for p in paths:
                idb = model[p][-1]
                rollos.append(pclases.RolloC.get(idb))
            if "etiqueta" in boton.name:
                self.generar_etiquetas(rollos)
            elif "drop" in boton.name:
                if utils.dialogo(titulo = "¿BORRAR?", 
                                 texto = "¿Está seguro de eliminar los rollos seleccionados?", 
                                 padre = self.wids['ventana']):
                    self.borrar_rollos(rollos)

    def generar_etiquetas(self, rollos):
        """
        Genera una lista de diccionarios con los datos de los rollos 
        para generar sus etiquetas.
        """
        from listado_rollos import preparar_datos_etiquetas_rollos_c
        data = preparar_datos_etiquetas_rollos_c(rollos)
        if data:
            from formularios import reports
            reports.abrir_pdf(geninformes.etiquetasRollosCEtiquetadora(data))

    def borrar_rollos(self, rollos):
        """
        Elimina los rollos recibidas y actualiza la ventana.
        """
        for b in rollos:
            self.anular_consumo(b)
            a = b.articulo
            a.rolloC = None
            try:
                a.destroy(ventana = __file__)
            except Exception, msg:
                self.logger.error("%srollos_c::borrar_rollos -> Artículo ID %d de rollo ID %d (%s) no se pudo eliminar. Excepción: %s" 
                    % (self.usuario and self.usuario.usuario + ": " or "", a.id, b.id, b.codigo, msg))
                a.rolloC = b
                self.consumir(b)
            else:
                try:
                    b.destroy(ventana = __file__)
                except Exception, msg:
                    self.logger.error("%srollos_c::borrar_rollos -> Rollo ID %d (%s) no se pudo eliminar. Excepción: %s" 
                        % (self.usuario and self.usuario.usuario + ": " or "", b.id, b.codigo, msg))
                    try:
                        b.destroy_en_cascada(ventana = __file__)
                    except Exception, msg:
                        self.logger.error("%srollos_c::borrar_rollos -> Rollo ID %d (%s) no se pudo eliminar en cascada. Excepción: %s" 
                            % (self.usuario and self.usuario.usuario + ": " or "", b.id, b.codigo, msg))
                        self.consumir(b)
        self.actualizar_tabla()

    def crear_rollo(self, boton = None, peso = None):
        """
        Crea una rollo del producto mostrado en pantalla e introduce 
        su información en el TreeView. El peso lo solicita en una 
        ventana de diálogo.
        Si se recibe peso, debe ser un float.
        """
        # ¿TODO?: Hacer que el peso lo tome del puerto serie y se le pase a esta función.
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
            nuevo_rollo = self.crear_objeto_rollo(producto, peso)
            if nuevo_rollo == None:
                utils.dialogo_info(titulo = "ERROR", 
                    texto = "El rollo no se pudo crear. Inténtelo de nuevo.", 
                    padre = self.wids['ventana'])
            else:
                self.consumir(nuevo_rollo)
                self.add_nuevo_rollo_tv(nuevo_rollo)
                try:
                    totpantalla = utils.parse_float(
                        self.wids['e_pantalla'].get_text())
                except:
                    totpantalla = 0.0
                totpantalla += peso
                self.rellenar_totales(totpantalla)

    def consumir(self, rollo):
        """
        Consume los materiales de la formulación para el rollo creado.
        """
        descontar_material_adicional(self, rollo.articulo)

    def anular_consumo(self, rollo):
        """
        Anula los consumos (consume en negativo) del rollo eliminado.
        """
        descontar_material_adicional(self, rollo.articulo, False)

    def crear_objeto_rollo(self, producto, peso):
        """
        Crea una nueva rollo «C» y su artículo relacionado.
        """
        b = pclases.RolloC(peso = peso)
        pclases.Auditoria.nuevo(b, self.usuario, __file__)
        try:
            a = pclases.Articulo(rolloC = b, 
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

    def add_nuevo_rollo_tv(self, rollo):
        """
        Introduce el rollo al final del TreeView y lo desplaza.
        """
        model = self.wids['tv_rollos'].get_model()
        fila = (utils.str_fechahora(rollo.fechahora), 
                rollo.codigo, 
                utils.float2str(rollo.peso, 2), 
                rollo.productoVenta.descripcion, 
                rollo.observaciones, 
                rollo.id)
        model.append(fila)
        self.mover_al_final(self.wids['tv_rollos'])

    def actualizar_tabla(self, boton = None):
        """
        Actualiza la información completa de la tabla, 
        volviendo a buscar los rollos e introduciéndolas 
        en el TreeView.
        """
        rollos = self.buscar()
        self.rellenar_tabla(rollos)

    def chequear_cambios(self):
        pass

    def buscar(self):
        """
        Inicia la consulta paral año indicado en el widget y 
        rellena las tablas con la información obtenida.
        """
        #import time
        #antes = time.time()
        cuantos = int(self.wids['sp_ver'].get_value())
        rollos = []
        n = 0
        qrollos = pclases.RolloC.select(orderBy = "-id")
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        if cuantos == 0:
            tot = qrollos.count() * 1.0
        else:
            tot = cuantos * 1.0
        for b in qrollos:
            b.sync()        
                # Con 999 rollos se gana únicamente 1 segundo si omito 
                # la sincronización.
            try:
                rollos.insert(0, (b, b.productoVenta))       
                    # Para optimizar los accesos a la BD cacheo los datos aquí.
            except:     # ¿Rollo sin producto de venta? Mal asunto
                rollos.insert(0, (b, None))
            vpro.set_valor(n/tot, 'Recuperando rollo %s' % (b.codigo))
            n += 1
            if n == cuantos:
                break
        vpro.set_valor(1, 'Actualizando ventana...')
        vpro.ocultar()
        #print time.time() - antes
        return rollos

    def rellenar_tabla(self, rollos):
        """
        Introduce los rollos recibidas en el TreeView «tv» y lo 
        desplaza a la última fila (la más baja)
        """
        tv = self.wids['tv_rollos']
        model = tv.get_model()
        tv.freeze_child_notify()
        tv.set_model(None)
        model.clear()
        totpantalla = 0.0
        for rollo, producto in rollos:
            if producto != None:
                desc = producto.descripcion
            else:
                desc = "?"
            fila = (utils.str_fechahora(rollo.fechahora), 
                    rollo.codigo, 
                    utils.float2str(rollo.peso, 2), 
                    desc, 
                    rollo.observaciones, 
                    rollo.id)
            model.append(fila)
            totpantalla += rollo.peso_sin
        tv.set_model(model)
        tv.thaw_child_notify()
        self.rellenar_totales(totpantalla)
        self.mover_al_final(self.wids['tv_rollos'])

    def cambiar_mes_acumulado(self, boton):
        """
        Permite seleccionar un mes y un año. Después rellena los totales 
        de nuevo usando ese mes y año paral acumulado del mes.
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
        - En pantalla. Se recibe. Si es None no cambial valor que haya en 
                       el entry.
        - Acumulado de todas.
        - Acumulado del mes.
        """
        totacum = pclases.RolloC.calcular_acumulado_peso_sin()
        if mes == None or not isinstance(mes, int):
            mes = mx.DateTime.localtime().month
        if anno == None or not isinstance(anno, int):
            anno = mx.DateTime.localtime().year
        self.wids['label4'].set_text("Total mes:\n<small><i>%02d/%d</i></small>" % (
            mes, anno))
        self.wids['label4'].set_use_markup(True)
        totmes = pclases.RolloC.calcular_acumulado_mes_peso_sin(mes, anno)
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
            if len(model) > 0:
                last_iter = model.get_iter(model[-1].path)
                sel = tv.get_selection()
                sel.select_iter(last_iter)
                tv.scroll_to_cell(model[-1].path, use_align = True)
        except IndexError:  # No hay rollos que mostrar:
            return

    def preparar_tv(self, tv):
        """
        Prepara las columnas del TreeView.
        """
        cols = (('Fecha y hora', 'gobject.TYPE_STRING', False,True,False,None),
                ('Código', 'gobject.TYPE_STRING', False, True, True, None),
                ('Peso', 'gobject.TYPE_STRING', True, True, False, 
                    self.cambiar_peso), 
                ('Producto', 'gobject.TYPE_STRING', False, False, False, None), 
                ('Observaciones', 'gobject.TYPE_STRING', True, False, False, 
                    self.cambiar_observaciones),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(tv, cols)
        for col in tv.get_columns()[2:3]:
            for cell in col.get_cell_renderers():
                cell.set_property("xalign", 1.0)
            col.set_alignment(0.5)
        self.wids['tv_rollos'].get_selection().set_mode(gtk.SELECTION_MULTIPLE)

    def cambiar_peso(self, cell, path, texto):
        """
        Cambial peso del rollo editado.
        """
        try:
            peso = utils._float(texto)
        except ValueError:
            utils.dialogo_info(titulo = "ERROR", 
                               texto = "El valor tecleado %s no es correcto." % (peso), 
                               padre = self.wids['ventana'])
        else:
            model = self.wids['tv_rollos'].get_model()
            try:
                rollo = pclases.RolloC.get(model[path][-1])
            except:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "No se pudo acceder al rollo.", 
                                   padre = self.wids['ventana'])
                self.actualizar_tabla()
            else:
                difpeso = rollo.peso - peso
                rollo.peso = peso
                rollo.syncUpdate()
                model[path][2] = utils.float2str(rollo.peso, 2)
                try:
                    totpantalla = utils.parse_float(
                        self.wids['e_pantalla'].get_text())
                except:
                    totpantalla = 0.0
                totpantalla -= difpeso
                self.rellenar_totales(totpantalla)
    
    def cambiar_observaciones(self, cell, path, texto):
        """
        Cambia las observaciones del rollo de la fila editada.
        """
        model = self.wids['tv_rollos'].get_model()
        try:
            rollo = pclases.RolloC.get(model[path][-1])
        except:
            utils.dialogo_info(titulo = "ERROR", 
                               texto = "No se pudo acceder al rollo.", 
                               padre = self.wids['ventana'])
            self.actualizar_tabla()
        else:
            rollo.observaciones = texto
            model[path][4] = rollo.observaciones

################################################################################

if __name__ == '__main__':
    v = RollosC() 


