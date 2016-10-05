#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2016  Francisco José Rodríguez Bogado,                   #
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
#  partes_de_fabricacion_balas.py - Parte de producción para balas.
###################################################################
#  NOTAS:
#
###################################################################
#  Changelog:
#  2 de noviembre de 2005 -> Inicio
#  15 de noviembre de 2005 -> 99% funcional (ufff, ¡dos semanas!)
#  23 de enero de 2006 -> Portado a clase.
#  26 de enero de 2006 -> Funcional al 99% one more time.
#  12 de enero de 2006 -> Añadido agregar balas por rango.
#  9 de mayo de 2006 -> Añadidos permisos.
#  10 de mayo de 2006 -> Cambiado comportamiento de set_articulo.
#  3 de agosto de 2006 -> Corregida búsqueda empleados del turno.
#  31 de julio de 2007 -> Nueva casilla "versión de la ficha de
#                         producción" usada (texto libre).
###################################################################
#  NOTAS:
#  OJO: El consumo de filtros tiene como cantidad válida el campo
#  cantidad. No se usan "antes" ni "después" y ambos están a -1
#  para distinguirlos del consumo de granza. No se permite que
#  a través de la ventana un consumo de granza llegue a tener
#  cantidades negativas en antes y después, por tanto no debería
#  haber problemas para usar esto como flag distintivo.
#  - Comprobar que las horas del parte no pisan a otro parte de balas.
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk
import time
import mx.DateTime
from framework import pclases
from informes import geninformes
from utils import _float as float
from ventana_progreso import VentanaActividad, VentanaProgreso
import pango
import re
from formularios import reports
import datetime
from lib.myprint import myprint
import time
try:
    from api import murano
    MURANO = True
except ImportError:
    MURANO = False

def verificar_solapamiento(partedeproduccion, padre=None,
                           fecha_anterior=None, horaini_anterior=None,
                           horafin_anterior=None):
    """
    Comprueba que el parte no se pise con otro de la misma línea.
    En caso de que comparta horas con otros partes, mostrará un
    mensaje de error.
    No puedo asegurar que la hora sea correcta porque eso implicaría
    buscar "huecos" en los días de producción que coincidieran con
    la fecha y hora actual, con el agravante de que si el parte se ha
    duplicado por error no quedaría hueco y habría que eliminar uno
    de los dos, etc...
    Lo que sí se hace es desbloquear el parte para que aparezca como
    no verificado y lo corrija el jefe de línea en caso de dudas de
    los operarios de planta.
    Si se recibe la fecha, la hora inicial o la hora final anterior se
    vuelve a poner el parte a esos valores.
    """
    if partedeproduccion.se_solapa():
        utils.dialogo_info(titulo="HORARIO ERRÓNEO",
                           texto="""

        La fecha o las horas de inicio y fin del parte no son correctas.
        El parte actual se solapa con otro de la misma línea. Compruebe
        la fecha y horas y corrija el error.

        """,
                           padre=padre)
        partedeproduccion.bloqueado = False
        if fecha_anterior or horaini_anterior or horafin_anterior:
            if fecha_anterior:
                partedeproduccion.fecha = fecha_anterior
            if horaini_anterior:
                partedeproduccion.horainicio = horaini_anterior
            if horafin_anterior:
                partedeproduccion.horafin = horafin_anterior
            partedeproduccion._corregir_campos_fechahora()
        partedeproduccion.syncUpdate()


class PartesDeFabricacionBalas(Ventana):
    def __init__(self, objeto=None, permisos="rwx", usuario=None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self.__lecturaescritura = None
        self.__permisos = permisos
        self.producto = None    # Producto relacionado con el parte.
        # Debe coincidir con el de todas las balas de "Detalles de producción"
        Ventana.__init__(self, 'partes_de_fabricacion_balas.glade', objeto,
                         usuario=usuario)
        connections = {'b_salir/clicked': self._salir,
                       'ventana/delete_event': self._salir,
                       'b_nuevo/clicked': self.crear_nuevo_partedeproduccion,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_buscar/clicked': self.buscar_partedeproduccion,
                       'b_borrar/clicked': self.borrar_parte,
                       'b_articulo/clicked': self.set_articulo,
                       'b_fecha/clicked': self.mostrar_calendario,
                       'b_hora_fin/clicked': self.set_hora_final,
                       'b_hora_ini/clicked': self.set_hora_inicial,
                       'b_add_bala/clicked': self.add_bala,
                       'b_drop_bala/clicked': self.drop_bala,
                       'b_add_incidencia/clicked': self.add_incidencia,
                       'b_drop_incidencia/clicked': self.drop_incidencia,
                       'b_add_empleado/clicked': self.add_empleado,
                       'b_cambiar_lote/clicked': self.cambiar_lote,
                       'b_drop_empleado/clicked': self.drop_empleado,
                       'b_add_granza/clicked': self.add_granza,
                       'b_drop_granza/clicked': self.drop_granza,
                       'b_add_filtro/clicked': self.add_filtro,
                       'b_drop_filtro/clicked': self.drop_filtro,
                       'ch_bloqueado/clicked': self.bloquear,
                       'b_imprimir/clicked': self.imprimir,
                       'b_etiquetas/clicked': self.etiquetas,
                       'b_etiq_peq/clicked': self.etiquetasPeq,
                       'b_add_desecho/clicked': self.add_desecho,
                       'b_drop_desecho/clicked': self.drop_desecho,
                       'b_bascula/clicked': self.iniciar_pesaje_auto,
                       'b_add_consumo/clicked': self.consumir_manual,
                       'b_next/clicked': self.siguiente,
                       'b_back/clicked': self.anterior
                       }
        self.add_connections(connections)
        try:
            self.linea = pclases.LineaDeProduccion.select(
                pclases.LineaDeProduccion.q.nombre == 'Línea de fibra')[0]
        except IndexError:
            self.logger.error(
                "La línea de fibra no está correctamente dada de alta.")
            self.linea = None
        if pclases.DEBUG:
            antes = time.time()
            myprint(__file__, " 0.- >>> inicializar_ventana")
        self.inicializar_ventana()
        if pclases.DEBUG:
            myprint(__file__, " 1.- <<< inicializar_ventana: %.2f" %
                    (time.time() - antes))
            antes = time.time()
        if not self.objeto:
            self.ir_a_primero()
        else:
            self.objeto = None
            self.ir_a(objeto)
        if pclases.DEBUG:
            myprint(__file__, " 2.- <<< ir_a...: %.2f" %
                    (time.time() - antes))
            antes = time.time()
        gtk.main()

    def anterior(self, boton=None):
        if self.objeto:
            siguiente = self.objeto.anterior()
            if siguiente:
                self.objeto = siguiente
                self.actualizar_ventana()
            else:
                utils.dialogo_info(titulo="NO MÁS PARTES",
                                   texto="No hay partes de producción "
                                         "anteriores al actual",
                                   padre=self.wids['ventana'])

    def siguiente(self, boton=None):
        if self.objeto:
            anterior = self.objeto.siguiente()
            if anterior:
                self.objeto = anterior
                self.actualizar_ventana()
            else:
                utils.dialogo_info(titulo="NO MÁS PARTES",
                                   texto="No hay partes de producción "
                                         "posteriores al actual",
                                   padre=self.wids['ventana'])

    # --------------- Funciones auxiliares ------------------------------
    def formatear_observaciones(self, obs):
        """
        Si recibe una cadena la separa tomando como límite de
        los campos el ";". Devuelve un diccionario de claves
        predefinidas (e_granza, e_plast_sup, e_plast_inf,
        e_fleje, e_antiuv) con los valores obtenidos del
        texto y por este orden.
        Si lo que recibe es un diccionario, devuelve los valores
        de las claves por el orden anterior, separados por
        punto y coma y en forma de cadena.
        Si no es diccionario ni texto o hay algún tipo de
        error devuelve None.
        """
        listacampos = ['e_granza',
                       'e_plast_sup',
                       'e_plast_inf',
                       'e_fleje',
                       'e_antiuv',
                       'txt_observaciones']
        if isinstance(obs, str):
            listavalores = obs.split(';')
            if len(listavalores) > 6:
                listavalores = listavalores[:5] + [";".join(listavalores[5:])]
            while len(listavalores) < 6:
                listavalores.insert(0, "")
            dic = {}
            for par in zip(listacampos, listavalores):
                dic[par[0]] = par[1]
            res = dic
        elif isinstance(obs, dict):
            listavalores = []
            for campo in listacampos:
                listavalores.append(obs[campo])
            txt = ';'.join(listavalores)
            res = txt
        else:
            res = None
        return res

    def procesar_observaciones(self):
        """
        Obtiene el texto de los widgets correspondientes a
        las observaciones y los devuelve como diccionario
        de widget:valor.
        """
        lisv = []
        listacampos = ['e_granza',
                       'e_plast_sup',
                       'e_plast_inf',
                       'e_fleje',
                       'e_antiuv',
                       'txt_observaciones']
        for w in listacampos:
            try:
                lisv.append(self.wids[w].get_text())
            except AttributeError:
                bounds = self.wids[w].get_buffer().get_bounds()
                buf = self.wids[w].get_buffer()
                lisv.append(buf.get_text(bounds[0], bounds[1]))
        lisv = ';'.join(lisv)
        return lisv

    def es_diferente(self):
        """
        Devuelve True si la información en pantalla es distinta a la
        del objeto en memoria.
        """
        partedeproduccion = self.objeto
        if not partedeproduccion:
            return False  # Si no hay partedeproduccion activo, devuelvo que
            # no hay cambio respecto a la ventana
        condicion = (utils.str_fecha(partedeproduccion.fecha) ==
                     self.wids['e_fecha'].get_text())
        try:
            condicion = (condicion and (
                self.wids['e_fichaproduccion'].get_text() ==
                partedeproduccion.fichaproduccion))
            condicion = (condicion and (
                partedeproduccion.horainicio.strftime('%H:%M') ==
                self.wids['e_hora_ini'].get_text()))
            condicion = (condicion and (
                partedeproduccion.horafin.strftime('%H:%M') ==
                self.wids['e_hora_fin'].get_text()))
        except AttributeError as msg:
            txt = "partes_de_fabricacion_balas.py: es_diferente: Devuelvo "\
                  "True; Excepción 'AttributeError': %s" % (msg)
            self.logger.error(txt)
            partedeproduccion.sync()
            condicion = False
        condicion = (condicion and (str(partedeproduccion.prodestandar) ==
                     self.wids['e_o80'].get_text()))
        # NOTA: Nada más a comparar. La info del artículo es la de alguno de
        # las balas introducidas y se elige mediante el botón correspondiente
        # (determinará las búsquedas y la información a pedir a la hora de
        # añadir balas en "detalles de producción".)
        obs = self.formatear_observaciones(partedeproduccion.observaciones)
        # Las observaciones, que además en este caso llevan un formateado
        # especial: "granza; plástico; ...; observaciones"
        for clave in obs:
            try:
                condicion = condicion and (self.wids[clave].get_text() ==
                                           obs[clave])
            except AttributeError:
                bounds = self.wids[clave].get_buffer().get_bounds()
                buf = self.wids[clave].get_buffer()
                condicion = (condicion and
                             (buf.get_text(bounds[0], bounds[1]) ==
                              obs[clave]))
        return not condicion    # Condición verifica que sea igual

    # def aviso_actualizacion(self):
    #     """
    #     Muestra una ventana modal con el mensaje de objeto
    #     actualizado.
    #     """
    #     utils.dialogo_info('ACTUALIZAR',
    #                        'El parte ha sido modificado remotamente.\n'
    #                        'Debe actualizar la información mostrada en '
    #                        'pantalla.\nPulse el botón «Actualizar»')
    #     self.wids['b_actualizar'].set_sensitive(True)

    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        if pclases.DEBUG:
            antes = time.time()
            myprint(__file__, " 1.- >>> inicializar_ventana (dentro)")
        check_last_balas_bien_creadas(self.logger)
        if pclases.DEBUG:
            myprint(__file__, " 2.- +++ inicializar_ventana: EOComprobación:"
                    " %.2f" % (time.time() - antes))
            antes = time.time()
        # CWT: No se debe poder editar la producción estándar desde el parte.
        # Siempre debe ser la del producto, so...
        self.wids['e_o80'].set_has_frame(False)
        self.wids['e_o80'].set_property("editable", False)
        # Inicialmente no se muestra NADA. Sólo se le deja al
        # usuario la opción de buscar o crear nuevo.
        self.activar_widgets(False)
        self.wids['b_actualizar'].set_sensitive(False)
        self.wids['b_guardar'].set_sensitive(False)
        self.wids['b_nuevo'].set_sensitive(True)
        self.wids['b_buscar'].set_sensitive(True)
        # Inicialización del resto de widgets:
        # (Nombre, tipo, editable, ordenable, buscable, función_actualización)
        cols = (('Lote', 'gobject.TYPE_STRING', False, True, False, None),
                ('Nº Bala', 'gobject.TYPE_STRING', False, True, True, None),
                ('Peso', 'gobject.TYPE_FLOAT',
                    True, True, False, self.cambiar_peso_bala),
                ('Clase B', 'gobject.TYPE_BOOLEAN',
                    True, True, False, self.cambiar_claseb),
                ('Motivo parada', 'gobject.TYPE_STRING',
                    False, True, False, self.cambiar_motivo_incidencia),
                ('Hora comienzo', 'gobject.TYPE_STRING',
                    True, True, False, self.cambiar_inicio_incidencia),
                ('Hora terminación', 'gobject.TYPE_STRING',
                    True, True, False, self.cambiar_fin_incidencia),
                ('Duración', 'gobject.TYPE_STRING',
                    False, True, False, None),
                ('Observaciones', 'gobject.TYPE_STRING',
                    True, False, False, self.cambiar_observaciones),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None)
                )
        utils.preparar_listview(self.wids['tv_balas'], cols)
        self.wids['tv_balas'].get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        self.wids['tv_balas'].add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.wids['tv_balas'].connect('button_press_event',
                                      self.button_clicked)
        cols = (('Id.', 'gobject.TYPE_INT64', False, True, False, None),
                ('Nombre', 'gobject.TYPE_STRING', False, True, False, None),
                ('Apellidos', 'gobject.TYPE_STRING', False, True, True, None),
                ('Horas', 'gobject.TYPE_STRING', True, True, False,
                    self.cambiar_horas_trabajadas),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_empleados'], cols)
        self.colorear_tabla_empleados()
        cols = (('Producto', 'gobject.TYPE_STRING', False, True, True, None),
                ('Cant. antes', 'gobject.TYPE_FLOAT',
                    True, True, False, self.cambiar_cantidad_antes),
                ('Cant. después', 'gobject.TYPE_FLOAT',
                    True, True, False, self.cambiar_cantidad_despues),
                ('Cantidad', 'gobject.TYPE_FLOAT',
                    True, True, False, self.cambiar_cantidad_consumo),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_granza'], cols)
        cols = (('Producto', 'gobject.TYPE_STRING', False, True, True, None),
                ('Cantidad', 'gobject.TYPE_FLOAT',
                    True, True, False, self.cambiar_cantidad_filtro),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_filtros'], cols)
        cols = (('Silo', 'gobject.TYPE_STRING', False, True, False, None),
                ('Producto', 'gobject.TYPE_STRING', False, True, True, None),
                ('Cantidad', 'gobject.TYPE_STRING', False, True, False, None),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_consumos'], cols)
        cols = (('Hora inicio', 'gobject.TYPE_STRING',
                 False, True, False, None),
                ('Hora fin', 'gobject.TYPE_STRING', False, True, True, None),
                ('Silo', 'gobject.TYPE_STRING', False, True, False, None),
                ('Porcentaje', 'gobject.TYPE_STRING',
                 False, True, False, None),
                ('Materia prima', 'gobject.TYPE_STRING',
                 False, True, False, None),
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_granza_silos'], cols)
        col = self.wids['tv_granza_silos'].get_column(3)
        col.get_cell_renderers()[0].set_property("xalign", 1.0)
        cols = (('Producto', 'gobject.TYPE_STRING', False, True, True, None),
                ('Cantidad', 'gobject.TYPE_STRING', True, True, False,
                    self.cambiar_cantidad_descuento_material),
                ('Observaciones', 'gobject.TYPE_STRING', True, True, False,
                    self.cambiar_observaciones_descuento_material),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_desecho'], cols)
        self.wids['tv_desecho'].get_selection().set_mode(
            gtk.SELECTION_MULTIPLE)
        if pclases.DEBUG:
            myprint(__file__, " 3.- +++ inicializar_ventana: EOTreeViews:"
                    " %.2f" % (time.time() - antes))
            antes = time.time()
        self.scales = []
        for silo in pclases.Silo.select(orderBy="nombre"):
            ch_silo = gtk.CheckButton(label=silo.nombre)
            adjustment = gtk.Adjustment(value=0, lower=0, upper=100,
                                        step_incr=0.5, page_incr=10,
                                        page_size=0)
            escala = gtk.HScale(adjustment)
            ch_silo.connect("toggled", self.activar_silo, escala)
            self.scales.append((ch_silo, escala))
            escala.set_value_pos(gtk.POS_BOTTOM)
            vbox = gtk.VBox()
            l_silo = gtk.Label()
            font_desc = pango.FontDescription("Sans 8")
            l_silo.modify_font(font_desc)
            mostrar_carga_silo(l_silo, silo)
            try:
                carga_mas_antigua = murano.ops.get_carga_mas_antigua_silo(silo)
            except:
                self.logger.error(
                    "Error al leer silos de Murano. Fallback a ginn.")
                carga_mas_antigua = silo.get_carga_mas_antigua()
            if carga_mas_antigua is None:
                l_carga_silo = gtk.Label("vacío")
            else:
                txtcarga = (carga_mas_antigua.productoCompra and
                            carga_mas_antigua.productoCompra.descripcion.upper(
                            ).replace("GRANZA", "").replace("GRANEL", "") or
                            "?")
                if len(txtcarga) > 30:
                    txtcarga = txtcarga[:27] + "..."
                if len(txtcarga) > 15:
                    l_carga_silo = gtk.Label("<small><small>" + txtcarga +
                                             "</small></small>")
                else:
                    l_carga_silo = gtk.Label("<small>" + txtcarga + "</small>")
                if (carga_mas_antigua.productoCompra and
                        carga_mas_antigua.productoCompra.obsoleto):
                    ch_silo.set_sensitive(False)
                    ch_silo.set_active(False)
                else:
                    ch_silo.set_sensitive(True)
            l_carga_silo.modify_font(font_desc)
            vbox.pack_start(ch_silo)
            vbox.pack_start(l_silo)
            vbox.pack_start(l_carga_silo)
            l_carga_silo.set_use_markup(True)
            vbox.pack_start(escala)
            self.wids['ch_silo_ID%d' % (silo.id)] = ch_silo
            ch_silo.set_name('ch_silo_ID%d' % (silo.id))
            self.wids['escala_ID%d' % (silo.id)] = escala
            escala.set_name('escala_ID%d' % (silo.id))
            self.wids['vbox_ID%d' % (silo.id)] = vbox
            self.wids['l_ID%d' % (silo.id)] = l_silo
            l_silo.set_name('l_ID%d' % (silo.id))
            self.wids['hbox_silos'].add(vbox)
        vreciclada0 = self.build_combo_reciclada(self.scales, 0)
        vreciclada1 = self.build_combo_reciclada(self.scales, 1)
        self.wids['hbox_silos'].add(vreciclada0)
        self.wids['hbox_silos'].add(vreciclada1)
        self.wids['hbox_silos'].show_all()
        for scale in self.scales:
            scale[1].connect("value-changed", self.cambiar_valor_silo,
                             self.scales)
            # scale[0].set_active(False)  # De paso, inicio la ventana con el
            #                            # consumo de silos desactivado.
            # scale[1].set_sensitive(False)
        if pclases.DEBUG:
            myprint(__file__, " 4.- +++ inicializar_ventana: EOScales silos:"
                    " %.2f" % (time.time() - antes))
            antes = time.time()
        if pclases.DEBUG:
            myprint(__file__, " 5.- +++ inicializar_ventana: EOConf_silos:"
                    " %.2f" % (time.time() - antes))
            antes = time.time()
        self.wids['e_bultos_a_lote'].set_alignment(1.0)
        self.wids['e_bultos_b_lote'].set_alignment(1.0)
        self.wids['e_kgs_a_lote'].set_alignment(1.0)
        self.wids['e_kgs_b_lote'].set_alignment(1.0)
        if pclases.DEBUG:
            myprint(__file__, " 6.- +++ inicializar_ventana: EOResto widgets:"
                    " %.2f" % (time.time() - antes))
            antes = time.time()
        if self.usuario and self.usuario.nivel > 0:
            # Yo no necesito el rollo de que esté maximizada para picar código.
            self.wids['ventana'].maximize()
            time.sleep(0.5)
            self.wids['ventana'].unmaximize()
            time.sleep(0.5)
            # En algunos windows hay un "glitch" que congela la
            # ventana. Se arregla cambiando el foco o restaurando y volviendo
            # a maximizar, por ejemplo. Que es justo lo que hago aquí.
            self.wids['ventana'].maximize()
        if pclases.DEBUG:
            myprint(__file__, " 6.- <<< inicializar_ventana: EOMaximizar:"
                    " %.2f" % (time.time() - antes))
            antes = time.time()

    def load_conf_silos(self):
        """
        Rescata la información de porcentajes marcados para consumir en los
        silos y ajusta los scales según esa configuración.
        """
        if self.objeto:
            confsilos = self.objeto.get_conf_silos()    # La última almacenada.
            for silo in confsilos:
                checksilo = self.wids['ch_silo_ID%d' % (silo.id)]
                scalesilo = self.wids['escala_ID%d' % (silo.id)]
                if confsilos[silo]:     # Si para ese silo hay registro de
                                        # configuración en la base de datos:
                    checksilo.set_active(True)
                    scalesilo.set_sensitive(True)
                    scalesilo.set_value(confsilos[silo].porcentaje)
                else:
                    checksilo.set_active(False)
                    scalesilo.set_sensitive(False)

    def save_conf_silos(self):
        """
        Guarda los porcentajes, productos y silos marcados para consumir en
        un registro nuevo de configuración de silos *solo* si ha cambiado
        respecto al último (pero de eso se encarga el método del PDP).
        """
        pdp = self.objeto
        fechahora = datetime.datetime.now()
        # Me aseguro de que la hora de consumo está dentro del parte.
        if not (self.objeto.fechahorainicio <= fechahora <=
                self.objeto.fechahorafin):
            fechahora = max(self.objeto.fechahorainicio, fechahora)
            fechahora = min(self.objeto.fechahorafin, fechahora)
        confs = {}
        for scale in self.scales:
            check_marcado, escala_porcentaje = scale
            if check_marcado.get_active():
                if "reciclada" in escala_porcentaje.name:
                    numreciclada = int(escala_porcentaje.name.split("_")[-1])
                    numsilo = silo = None
                    idgranza = utils.combo_get_value(
                        self.wids["cbe_reciclada_%d" % (numreciclada)])
                    producto = pclases.ProductoCompra.get(idgranza)
                    silo_key = numreciclada
                else:
                    idsilo = escala_porcentaje.name.split("_")[-1]
                    numsilo = int(idsilo.replace("ID", ""))
                    silo = pclases.Silo.get(numsilo)
                    numreciclada = None
                    try:
                        carga_mas_baja_en_silo = murano.ops.get_carga_mas_antigua_silo(silo)
                    except:
                        self.logger.error(
                            "Error al leer silos de Murano. Fallback a ginn.")
                        carga_mas_baja_en_silo = silo.get_carga_mas_antigua()
                    producto = carga_mas_baja_en_silo.productoCompra
                    silo_key = silo
                porcentaje = escala_porcentaje.get_value() / 100
                confs[silo_key] = {'productoCompra': producto,
                                   'porcentaje': porcentaje}
        try:
            pdp.save_conf_silos(confs, fechahora)
        except AssertionError as err:
            # AttributeError
            # raise AssertionError, err # Para que me lo envíe por correo.
            self.logger.error("partes_de_fabricacion_balas::"
                              "save_conf_silos -> %s - %s" % (err, confs))
            self.wids['tv_granza_silos'].set_sensitive(False)

    def cambiar_observaciones_descuento_material(self, cell, path, newtext):
        """
        Cambia las observaciones del registro.
        """
        model = self.wids['tv_desecho'].get_model()
        ide = model[path][-1]
        desecho = pclases.DescuentoDeMaterial.get(ide)
        desecho.observaciones = newtext
        # Actualizo la fecha y hora.
        desecho.fechahora = mx.DateTime.localtime()
        self.objeto.unificar_desechos()
        self.rellenar_tabla_desechos()

    def rellenar_tabla_desechos(self):
        """
        Rellena la tabla de desechos del parte.
        """
        parte = self.objeto
        if parte is not None:
            model = self.wids['tv_desecho'].get_model()
            self.wids['tv_desecho'].set_model(None)
            model.clear()
            desechos = parte.descuentosDeMaterial[:]
            try:
                desechos.sort(lambda c1, c2:
                              c1 is not None and c2 is not None and
                              int(c1.id - c2.id) or 0)
            except TypeError as msg:
                self.logger.error("partes_de_fabricacion_balas.py "
                                  "(rellenar_tabla_desechos): "
                                  "Error ordenando descuento de material "
                                  "(%s):\n%s" % (msg, desechos))
            for c in desechos:
                if c.productoCompraID is not None:
                    unidad = c.productoCompra.unidad
                    producto = c.productoCompra.descripcion
                else:
                    unidad = ""
                    producto = ""
                model.append((producto,
                              "%s %s" % (utils.float2str(c.cantidad), unidad),
                              c.observaciones,
                              c.id))
            self.wids['tv_desecho'].set_model(model)

    def cambiar_cantidad_descuento_material(self, cell, path, newtext):
        """
        Cambia la cantidad descontada del registro y actualiza el
        producto de venta a la nueva cantidad (suma la cantidad
        anterior y resta la nueva).
        """
        model = self.wids['tv_desecho'].get_model()
        ide = model[path][-1]
        desecho = pclases.DescuentoDeMaterial.get(ide)
        try:
            newtext = newtext.replace(desecho.productoCompra.unidad,
                                      "").strip()
            nueva_cantidad = utils._float(newtext)
        except ValueError:
            utils.dialogo_info(titulo="ERROR FORMATO NUMÉRICO",
                               texto='El texto "%s" no es una cantidad '
                                     'correcta.' % (newtext),
                               padre=self.wids['ventana'])
        else:
            cantidad_desecho_inicial = desecho.cantidad
            productoCompra = desecho.productoCompra
            productoCompra.sync()
            antes = productoCompra.existencias
            cantidad_desecho_final = desecho.cambiar_cantidad(nueva_cantidad)
            despues = desecho.productoCompra.existencias
            self.logger.warning("%spartes_de_fabricacion_balas::"
                                "cambiar_cantidad_descuento_material -> "
                                "Cambiada cantidad de descuento existente. "
                                "Stock de %s antes: %f, después: %f. "
                                "Cantidad de desecho antes: %f. "
                                "Después: %f." % (self.usuario and
                                                  self.usuario.usuario +
                                                  ": " or "",
                                                  productoCompra.descripcion,
                                                  antes,
                                                  despues,
                                                  cantidad_desecho_inicial,
                                                  cantidad_desecho_final))
            if cantidad_desecho_final != nueva_cantidad:
                utils.dialogo_info(titulo="EXISTENCIAS INSUFICIENTES",
                                   texto="No había existencias suficientes del"
                                         " producto para cambiar la\ncantidad"
                                         " desechada a %s." % (
                                             utils.float2str(nueva_cantidad)),
                                   padre=self.wids['ventana'])
            self.objeto.unificar_desechos()
            self.rellenar_tabla_desechos()

    def activar_granza_reciclada(self, ch, escala, combo):
        """
        Activa el consumo de granza reciclada seleccionando la primera
        opción del combo. Si no hay, no se activa.
        También actúa sobre la barra inferior poniendo el porcentaje
        adecuado.
        """
        escala.set_sensitive(ch.get_active())
        model = combo.get_model()
        if len(model) > 0 and ch.get_active():
            utils.combo_set_from_db(combo, model[0][0])
            combo.set_sensitive(True)
            escala.set_value(100)
        else:
            utils.combo_set_from_db(combo, -1)
            combo.set_sensitive(False)
            ch.set_active(False)
            escala.set_value(0)

    def build_checkbox_reciclada(self, numcombo=0):
        """
        Devuelve CheckBox de granza reciclada con callback y listo
        para empaquetar.
        """
        ch_reciclada = gtk.CheckButton(
            label="<small>Granza\nrecuperada %d</small>" % (numcombo + 1))
        ch_reciclada.get_children()[0].set_use_markup(True)
        nombre = "ch_reciclada_%d" % (numcombo)
        ch_reciclada.set_name(nombre)
        self.wids[nombre] = ch_reciclada
        return ch_reciclada

    def build_comboboxentry_reciclada(self, numcombo=0):
        """
        Devuelve el ComboBoxEntry (no confundir con build_combo_reciclada, que
        crea todo el conjunto de widgets) para la granza reciclada con el
        callback y listo para empaquetar, señora.
        """
        combo = gtk.ComboBoxEntry()
        try:
            granzas = pclases.ProductoCompra.select(pclases.AND(
                pclases.ProductoCompra.q.descripcion.contains("granza"),
                pclases.ProductoCompra.q.obsoleto == False,     # NOQA
                pclases.ProductoCompra.q.tipoDeMaterialID ==
                    pclases.TipoDeMaterial.select(
                    pclases.TipoDeMaterial.q.descripcion.contains("prima")
                  )[0].id),
                orderBy="descripcion")
        except IndexError:
            self.logger.warning("partes_de_fabricacion_balas.py: "
                                "No se encontró granza reciclada.",
                                exc_info=True)
            opciones_granza = []
        else:
            opciones_granza = [(g.id, g.descripcion) for g in granzas]
        utils.rellenar_lista(combo, opciones_granza)
        nombre_combo = "cbe_reciclada_%d" % (numcombo)
        combo.set_name(nombre_combo)
        self.wids[nombre_combo] = combo
        combo.connect("changed", lambda c: c.child.set_position(-1))
        combo.set_size_request(120, -1)
        return combo

    def build_escala_reciclada(self, scales, ch_reciclada, combo,
                               numcombo=0):
        """
        Escala de 0 a 100 de granza reciclada.
        "scales" es el resto de scales (de silos) al que se agrega él mismo.
        """
        adjustment = gtk.Adjustment(value=0, lower=0, upper=100,
                                    step_incr=0.5, page_incr=10,
                                    page_size=0)
        escala = gtk.HScale(adjustment)
        escala.set_value_pos(gtk.POS_BOTTOM)
        escala.set_sensitive(False)
        combo.set_sensitive(False)
        nombre_escala = "s_reciclada_%d" % (numcombo)
        escala.set_name(nombre_escala)
        self.wids[nombre_escala] = escala
        # escala.connect("value-changed", self.cambiar_valor_silo, scales)
        scales.append((ch_reciclada, escala))
        ch_reciclada.connect("toggled", self.activar_granza_reciclada, escala,
                             combo)
        return escala

    def build_combo_reciclada(self, scales, numcombo=0):
        """
        Construye un VBox con el combo de granza reciclada y un slider
        de porcentaje a consumir de la misma.
        "numcombo" es el número del combo de granza reciclada, ya que puede
        haber más de uno (actualmente 2).
        """
        ch_reciclada = self.build_checkbox_reciclada(numcombo)
        combo = self.build_comboboxentry_reciclada(numcombo)
        escala = self.build_escala_reciclada(scales, ch_reciclada, combo,
                                             numcombo)
        vbox = gtk.VBox()
        vbox.pack_start(ch_reciclada)
        vbox.add(combo)
        vbox.pack_start(escala)
        return vbox

    def activar_silo(self, ch, escala):
        """
        Activa o desactiva el consumo de un silo.
        Recibe la escala relacionada con el silo.
        """
        if ch.get_active():
            idsilo = int(ch.get_name()[ch.get_name().index("ID") + 2:])
            silo = pclases.Silo.get(idsilo)
            try:
                ocupado = murano.ops.get_ocupado_silo(silo)
            except:
                self.logger.error(
                    "No se pudo leer Silo en Murano. Fallback a ginn.")
                ocupado = silo.ocupado
            if ocupado <= 0:
                ch.set_active(False)
                escala.set_value(0)
            else:
                escala.set_value(100)
        else:
            escala.set_value(0)
        escala.set_sensitive(ch.get_active())

    def cambiar_valor_silo(self, scale, scales):
        """
        Recibe el control scale y el resto de scales de la ventana.
        Ajusta todos los scales (excepto él mismo) para que el valor
        total sea de 100%.
        """
        valor_total = sum([a[1].get_value() for a in scales
                           if a[0].get_active()])
        resto = 100.0 - valor_total
        scales_menos_yo = [a for a in scales
                           if a[1] != scale and a[0].get_active()]
        try:
            incremento = resto * 1.0 / len(scales_menos_yo)
            incremento -= incremento % 0.5
        except ZeroDivisionError:
            incremento = 0
        for check, scale in scales_menos_yo:  # @UnusedVariable
            scale.set_value(scale.get_value() + incremento)

    def add_filtro(self, b):
        producto = self.buscar_producto_compra("FILTRO")
        if producto is None:
            return
        cantidad = utils.dialogo_entrada(titulo='CANTIDAD',
                                         texto='Introduzca la cantidad '
                                               'consumida:')
        if cantidad is None:
            return
        try:
            cantidad = float(cantidad)
        except ValueError:
            utils.dialogo_info('Cantidad incorrecta')
            return
        if cantidad > producto.existencias:
            utils.dialogo_info(titulo='CANTIDAD INSUFICIENTE',
                texto='No hay existencias suficientes en almacén.\nVerifique '
                      'que ha tecleado la cantidad correctamente\ny que las '
                      'entradas en almacén del producto han sido '
                      'contabilizadas.',
                padre=self.wids['ventana'])
            return
        # NOTA: OJO: (Esto hay que cambiarlo tarde o temprano). Si antes y despues = -1, es consumo de filtros.
        #            Si antes y despues = -2 es consumo de material adicional que no es granza.
        consumo = pclases.Consumo(antes=-1,
                                  despues=-1,
                                  cantidad=cantidad,
                                  actualizado=False,
                                  parteDeProduccion=self.objeto,
                                  productoCompra=producto)
        pclases.Auditoria.nuevo(consumo, self.usuario, __file__)
        self.actualizar_consumo(consumo, True)
        self.objeto.unificar_consumos()
        self.rellenar_filtros()

    def drop_filtro(self, b):
        model, itr = self.wids['tv_filtros'].get_selection().get_selected()
        if itr == None:
            return
        idconsumo = model[itr][-1]
        consumo = [c for c in self.objeto.consumos if c.id == idconsumo][0]
        self.actualizar_consumo(consumo, False)
        consumo.parteDeProduccion = None
        consumo.destroy(ventana=__file__)
        self.rellenar_filtros()

    def cambiar_cantidad_antes(self, cell, path, texto):
        try:
            antes = float(texto)
        except:
            utils.dialogo_info(titulo="ERROR DE FORMATO",
                    texto="El texto introducido (%s) no respeta el formato"
                          " numérico.\nUse solo números y el punto como "
                          "separador decimal." % texto,
                    padre=self.wids['ventana'])
            return
        model = self.wids['tv_granza'].get_model()
        idc = model[path][-1]
        consumo = pclases.Consumo.get(idc)
        if antes < consumo.despues or antes < 0:
            utils.dialogo_info(titulo="ERROR",
                               texto="La cantidad después de producir no "
                                       "puede ser superior a la de antes de"
                                       "\nempezar la fabricación y ninguna "
                                       "debe ser negativa.",
                               padre=self.wids['ventana'])
            return
        consumo.antes = antes
        consumo.cantidad = consumo.antes - consumo.despues
        model[path][1] = consumo.antes
        model[path][2] = consumo.despues
        model[path][3] = consumo.cantidad
        self.actualizar_consumo(consumo, True)
        cantidad = 0
        for consumo in [c for c in self.objeto.consumos if (c.antes != -1 and c.despues != -1) and (c.antes != -2 and c.despues != -2)]:
            cantidad += consumo.cantidad
        self.wids['e_total_granza'].set_text(utils.float2str(cantidad))

    def cambiar_cantidad_despues(self, cell, path, texto):
        try:
            despues = float(texto)
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", texto = "El texto introducido (%s) no respeta el formato numérico.\nUse solo números y el punto como separador decimal." % texto)
            return
        model = self.wids['tv_granza'].get_model()
        idc = model[path][-1]
        consumo = pclases.Consumo.get(idc)
        if consumo.antes < despues or despues < 0:
            utils.dialogo_info(titulo = "ERROR", texto = "La cantidad después de producir no puede ser superior a la de antes de\nempezar la fabricación y ninguna debe ser negativa.")
            return
        consumo.despues = despues
        consumo.cantidad = consumo.antes - consumo.despues
        model[path][1] = consumo.antes
        model[path][2] = consumo.despues
        model[path][3] = consumo.cantidad
        self.actualizar_consumo(consumo, True)
        cantidad = 0
        for consumo in [c for c in self.objeto.consumos if (c.antes != -1 and c.despues != -1) and (c.antes != -2 and c.despues != -2)]:
            cantidad += consumo.cantidad
        self.wids['e_total_granza'].set_text(utils.float2str(cantidad))

    def cambiar_cantidad_consumo(self, cell, path, texto):
        try:
            cantidad = float(texto)
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", texto = "El texto introducido (%s) no respeta el formato numérico.\nUse solo números y el punto como separador decimal." % texto)
            return
        model = self.wids['tv_granza'].get_model()
        idc = model[path][-1]
        consumo = pclases.Consumo.get(idc)
        consumo.cantidad = cantidad
        consumo.despues = consumo.antes - consumo.cantidad
        model[path][1] = consumo.antes
        model[path][2] = consumo.despues
        model[path][3] = consumo.cantidad
        self.actualizar_consumo(consumo, True)
        cantidad = 0
        for consumo in [c for c in self.objeto.consumos if (c.antes != -1 and c.despues != -1) and (c.antes != -2 and c.despues != -2)]:
            cantidad += consumo.cantidad
        self.wids['e_total_granza'].set_text(utils.float2str(cantidad))

    def cambiar_cantidad_filtro(self, cell, path, texto):
        try:
            cantidad = float(texto)
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", texto = "El texto introducido (%s) no respeta el formato numérico.\nUse solo números y el punto como separador decimal." % texto)
            return
        model = self.wids['tv_filtros'].get_model()
        idc = model[path][-1]
        consumo = pclases.Consumo.get(idc)
        cantidad_anterior = consumo.cantidad
        consumo.productoCompra.existencias += cantidad_anterior
        consumo.productoCompra.add_existencias(cantidad_anterior)
        consumo.cantidad = cantidad
        model[path][1] = consumo.cantidad
        self.actualizar_consumo(consumo, True)
        cantidad = 0
        for consumo in [c for c in self.objeto.consumos if c.antes == -1 and c.despues == -1]:
            cantidad += consumo.cantidad
        self.wids['e_total_filtros'].set_text(str(cantidad))

    def activar_widgets(self, s):
        """
        Activa o desactiva (sensitive=True/False) todos
        los widgets de la ventana que dependan del
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        s = s and ((self.usuario != None and self.usuario.nivel <= 2) or not self.objeto.bloqueado or self.usuario == None)
        # s = s and ("w" in self.__permisos or not self.objeto.bloqueado)
        if self.objeto:
            s = s or self.objeto.id == self.__lecturaescritura
        ws = ('table1', 'tv_balas', 'hbox1', 'hbox2', 'frame1', 'hbox4',
              'frame3', 'b_fecha', 'b_hora_ini', 'b_hora_fin', 'b_articulo',
              'b_add_bala', 'b_drop_bala', 'b_add_incidencia',
              'b_drop_incidencia', 'b_borrar', 'ch_bloqueado', 'hbox7',
              'e_fichaproduccion')
        for w in ws:
            self.wids[w].set_sensitive(s)
        self.wids['ch_bloqueado'].set_sensitive("w" in self.__permisos)

    def ir_a_primero(self):
        """
        Hace activo en la ventana el último parte creado en el sistema.
        """
        partedeproduccion = self.objeto
        try:
            if partedeproduccion != None:
                partedeproduccion.notificador.desactivar()
            # Anulo el aviso de actualización del parte que deja de ser
            # activo.
            # OJO: Debe haber más formas de distinguirlos e incluso más
            # lógicas, pero de momento me voy a guiar por el formateo de
            # las observaciones. Si tiene 6 campos concatenados con ';' es
            # de balas y si no es de rollos.
            partesdeproduccion = pclases.ParteDeProduccion.select(
                    """partida_cem_id IS NULL
                       AND observaciones LIKE '%;%;%;%;%;%'""")
            partesdeproduccion = partesdeproduccion.orderBy("-id")
            partedeproduccion=partesdeproduccion[0]
            partedeproduccion.notificador.activar(self.aviso_actualizacion)
        except:
            partedeproduccion = None
        self.objeto = partedeproduccion
        self.actualizar_ventana()

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
            filas_res.append((r.id,
                              utils.str_fecha(r.fecha),
                              utils.str_hora(r.horainicio),
                              utils.str_hora(r.horafin),
                              "CLIC PARA VER"))
        idpartedeproduccion = utils.dialogo_resultado(
                filas_res,
                titulo = 'Seleccione parte de producción de fibra',
                cabeceras = ('ID Interno',
                             'Fecha',
                             'Hora inicio',
                             'Hora fin',
                             'Lote'),
                func_change = self.mostrar_info_parte,
                padre = self.wids['ventana'])
        if idpartedeproduccion < 0:
            return None
        else:
            return idpartedeproduccion

    def mostrar_info_parte(self, tv):
        model, itr = tv.get_selection().get_selected()
        if itr!=None and model[itr][-1] == "CLIC PARA VER":
            parte = pclases.ParteDeProduccion.get(model[itr][0])    # En los
                                        # diálogos de resultado va al revés.
            if parte.es_de_balas() and parte.articulos != []:
                try:
                    lotepartida = parte.articulos[0].bala.lote.codigo
                except AttributeError:
                    lotepartida = parte.articulos[0].bigbag.loteCem.codigo
            elif not parte.es_de_balas() and parte.articulos != []:
                lotepartida = parte.articulos[0].rollo.partida.codigo
            else:
                lotepartida = 'VACIO'
            producto = parte.articulos != [] and parte.articulos[0].productoVenta.nombre or 'VACÍO'  # @UnusedVariable
            model[itr][-1] = lotepartida


    def rellenar_widgets(self):
        """
        Introduce la información del partedeproduccion actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a
        esta función en ese caso.
        """
        partedeproduccion = self.objeto
        self.wids['ch_bloqueado'].set_active(self.objeto.bloqueado)
        # Información global:
        strfecha = utils.str_fecha(partedeproduccion.fecha)
        self.wids['e_fecha'].set_text(strfecha)
        strhoraini = partedeproduccion.horainicio.strftime('%H:%M')
        self.wids['e_hora_ini'].set_text(strhoraini)
        strhorafin = partedeproduccion.horafin.strftime('%H:%M')
        self.wids['e_hora_fin'].set_text(strhorafin)
        self.wids['e_o80'].set_text(str(partedeproduccion.prodestandar))
        fichaprod = partedeproduccion.fichaproduccion
        self.wids['e_fichaproduccion'].set_text(fichaprod)
        obs = self.formatear_observaciones(partedeproduccion.observaciones)
        listacampos = ['e_granza',
                       'e_plast_sup',
                       'e_plast_inf',
                       'e_fleje',
                       'e_antiuv',
                       'txt_observaciones']
        for campo in listacampos:
            try:
                self.wids[campo].set_text(obs[campo])
            except AttributeError:  #Si no tiene set_text será el TextView
                self.wids[campo].get_buffer().set_text(obs[campo])
        # Información de detalle:
        if self.objeto.articulos != []:
            self.producto = self.objeto.articulos[0].productoVenta
            # Esto es por si ya tiene balas añadidas, para que trinque el
            # artículo del parte a partir de ellas y no se quede con el None
            # del inicio o con el producto del parte anterior (si es que se
            # ha visto un parte antes que este).
        self.rellenar_datos_articulo(self.producto)
        self.rellenar_tabla_empleados()
        self.rellenar_granza()
        self.rellenar_filtros()
        # Pongo el lote de la primera de las balas que encuentre con lote.
        for a in self.objeto.articulos:
            try:
                if a.es_bala():
                    self.wids['e_numlote'].set_text(a.bala.lote.codigo)
                    col = self.wids['tv_balas'].get_column(1)
                    col.set_title("Nº Bala")
                    self.wids['b_add_bala'].set_label("Añadir bala")
                    self.wids['b_drop_bala'].set_label("Eliminar bala")
                    break
                elif a.es_bigbag():
                    self.wids['e_numlote'].set_text(a.bigbag.loteCem.codigo)
                    col = self.wids['tv_balas'].get_column(1)
                    col.set_title("Nº Bigbag")
                    self.wids['b_add_bala'].set_label("Añadir bigbag")
                    self.wids['b_drop_bala'].set_label("Eliminar bigbag")
                    break
            except:
                self.wids['e_numlote'].set_text('')
        self.rellenar_tabla_balas()
        self.rellenar_tabla_desechos()
        self.check_permisos()
        self.objeto.make_swap()
        self.wids['b_back'].set_sensitive(
                self.objeto and self.objeto.anterior() and 1 or 0)
        self.wids['b_next'].set_sensitive(
                self.objeto and self.objeto.siguiente() and 1 or 0)
        #self.load_conf_silos() # TODO: PORASQUI: ¿Afectará a si cambio el porcentaje de un silo y recargo la ventana? Seguro, porque no se ha guardado la configuración. Pero si quiero fabricar una bala y no me he dado cuenta de que ha vuelto a los valores anteriores... caca. También está pendiente lo de cargar la última configuración de silos al abrir un parte.

    def check_permisos(self):
        if "w" in self.__permisos:  # Puede modificar los partes:
            self.activar_widgets(True)
        else:   # Sólo puede modificar el parte que haya creado nuevo (si es que ha creado alguno)
                # o si no está bloqueado.
            if self.__lecturaescritura == self.objeto.id or not self.objeto.bloqueado:
                self.activar_widgets(True)
            else:
                self.activar_widgets(False)
        # Compruebo primero este porque habilita o deshabilita todos los botones, incluso los que
        # dependen de los otros dos permisos.
        if "r" in self.__permisos:  # Puede leer partes anteriores, habilito el buscar:
            self.wids['b_buscar'].set_sensitive(True)
        else:
            self.wids['b_buscar'].set_sensitive(False)
        if "x" in self.__permisos:  # Puede crear nuevos:
            self.wids['b_nuevo'].set_sensitive(True)
        else:
            self.wids['b_nuevo'].set_sensitive(False)

    def cmpfechahora(self, detalle1, detalle2):
        if detalle1.fechahora < detalle2.fechahora:
            return -1
        elif detalle1.fechahora > detalle2.fechahora:
            return 1
        else:
            return 0

    def lote(self, a):
        try:
            if a.es_bala():
                return a.bala.lote.codigo
            elif a.es_bigbag():
                return a.bigbag.loteCem.codigo
            elif a.es_bala_cable():
                return "-"
            else:
                return ""
        except:
            return ''

    def bala(self, a):
        try:
            return a.codigo_interno
        except:
            return ''

    def peso(self, a):
        try:
            return a.peso_real
        except:
            return 0.0

    def motivo(self, i):
        try:
            return i.tipoDeIncidencia.descripcion
        except:
            return ''

    def horaini(self, i):
        try:
            return i.horainicio.strftime('%H:%M')
        except:
            return ''

    def horafin(self, i):
        try:
            return i.horafin.strftime('%H:%M')
        except:
            return ''

    def duracionhh(self, d):
        try:
            duracion = (d.horafin - d.horainicio)
            try:
                res = duracion.strftime('%H:%M')
            except AttributeError:
                res = "%d:%02d" % (duracion.seconds / 3600,
                                   duracion.seconds / 60 % 60)
        except AttributeError:
            res = ''
        return res

    def observaciones(self, d):
        try:
            if d.es_bala():
                return d.bala.motivo
            elif d.es_bigbag():
                return d.bigbag.motivo
            elif d.es_bala_cable():
                return d.balaCable.observaciones
            else:
                return d.observaciones
        except:     # No es bala.
            if hasattr(d, "observaciones"):
                return d.observaciones
            else:
                return ""

    def duracion(self, d):
        return self.duracionhh(d)

    def claseb(self, d):
        try:
            return d.bala.claseb
        except AttributeError:
            try:
                return d.bigbag.claseb
            except:
                return False

    def calcular_duracion(self, hfin, hini):
        if isinstance(hfin, mx.DateTime.DateTimeDeltaType):
            hfin = hfin + mx.DateTime.oneDay
        duracion = hfin - hini
        if duracion.day > 0:
            duracion -= mx.DateTime.oneDay
        if duracion.day > 0:
            myprint("WARNING: partes_de_fabricacion_balas: calcular_duracion:"
                    " ID %d: ¿Seguro que dura más de un día completo?" % (
                        self.objeto.id))
        return duracion

    def calcular_tiempo_trabajado(self, parte):
        tiempototal = parte.get_duracion()
        paradas = [p for p in parte.incidencias]
        tiempoparadas = 0
        for parada in paradas:
            tiempoparadas += parada.get_duracion()
        return tiempototal, tiempototal - tiempoparadas

    def colorear_tabla_empleados(self):
        """
        Prepara y asocia la función para resaltar los empleados
        cuyas horas trabajadas sean inferiores o superiores a
        la duración del parte.
        """
        def cell_func(column, cell, model, itr, numcol):
            idht = model[itr][-1]
            try:
                ht = pclases.HorasTrabajadas.get(idht)
            except:     # Ya no existe el idht, lo ignoro.
                return
            duracion_parte = self.objeto.get_duracion()
            ht_horas = ht.horas
            try:
                supera_parte = ht_horas > duracion_parte
            except TypeError:   # ht.horas es datetime.time
                ht_horas = utils.DateTime2DateTimeDelta(ht_horas)
                supera_parte = ht_horas > duracion_parte

            if supera_parte:
                color = "orange"
            elif ht_horas < duracion_parte:
                color = "red"
            else:
                color = "black"
            cell.set_property("foreground", color)

        cols = self.wids['tv_empleados'].get_columns()
        numcol = len(cols) - 1
        column = cols[numcol]
        cells = column.get_cell_renderers()
        for cell in cells:
            column.set_cell_data_func(cell, cell_func, numcol)

    def colorear(self, tv):
        def cell_func(column, cell, model, itr, i):
            muestra = False
            if model[itr][1] != '':
                ide = model[itr][-1]
                try:
                    articulo = pclases.Articulo.get(ide)
                except pclases.SQLObjectNotFound:
                    myprint("partes_de_fabricacion_balas.py: "
                            "cell_func en colorear: "
                            "El artículo ID %d ya no existe. "
                            "No aplico función de render." % (ide))
                    return
                try:
                    if articulo.es_bala():
                        cosa = articulo.bala
                    elif articulo.es_bigbag():
                        cosa = articulo.bigbag
                    elif articulo.es_balaCable():
                        cosa = articulo.balaCable
                except pclases.SQLObjectNotFound:
                    # Esto se produce porque se ejecuta el cell_func mientras
                    # aún se está eliminando el artículo. Riesgo 0.
                    myprint("partes_de_fabricacion_balas.py (cell_func): "
                            "Artículo no encontrado: %s" % (msg))
                    return
                except AttributeError:
                    # Esto ya sería más grave. El artículo existe pero ya no tiene bala asociada.
                    myprint("partes_de_fabricacion_balas.py (cell_func): "
                            "Bala no encontrada: %s" % (msg))
                    return
                try:
                    muestra = cosa.muestra
                except AttributeError:  # Sólo debería saltar cuando hay un artículo con bala == None.
                                        # Se supone que cuando corrija el error que lo produce (estoy en ello)
                                        # no debería pasar más.
                    muestra = False
                if i != 3:      # i == 3 es el CellRendererToggle, que no acepta color "de frente".
                    cell.set_property("foreground", None)
            elif model[itr][4].strip() != "":
                if i != 3:      # i == 3 es el CellRendererToggle, que no acepta color "de frente".
                    cell.set_property("foreground", "saddle brown")
            else:
                if i != 3:      # i == 3 es el CellRendererToggle, que no acepta color "de frente".
                    cell.set_property("foreground", None)
            # Clase B:
            claseB = model[itr][3]
            if claseB and not muestra:
                color = "yellow"
            elif claseB and muestra:
                color = "orange"
            elif muestra:
                color = "grey"
            else:
                # color = "white"
                color = None    # Color por defecto del tema
            cell.set_property("cell-background", color)
            utils.redondear_flotante_en_cell_cuando_sea_posible(column, cell, model, itr, i)
        cols = tv.get_columns()
        for i in xrange(len(cols)):
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell, cell_func, i)

    def rellenar_tabla_balas(self):
        model = self.wids['tv_balas'].get_model()
        model.clear()
        detallesdeproduccion = [i for i in self.objeto.incidencias] + [a for a in self.objeto.articulos]
            # El + sin más hace un join, así que no tengo más remedio que
            # recorrer las listas.
        detallesdeproduccion.sort(self.cmpfechahora)
        # De paso calculo totales:
        numA = numB = 0
        pesoA = pesoB = 0.0
        # Filas del TreeView
        last_iter_bala = None
        for detalle in detallesdeproduccion:
            itr = model.append((self.lote(detalle),
                                self.bala(detalle),
                                self.peso(detalle),
                                self.claseb(detalle),
                                self.motivo(detalle),
                                self.horaini(detalle),
                                self.horafin(detalle),
                                self.duracion(detalle),
                                self.observaciones(detalle),
                                detalle.id))
            if pclases.VERBOSE:
                myprint(detalle, self.lote(detalle), self.peso(detalle))
            if self.bala(detalle) != '':
                last_iter_bala = itr
        for articulo in self.objeto.articulos:
            if (articulo.bala and articulo.bala.claseb) or (articulo.bigbag and articulo.bigbag.claseb):
                numB += 1
                pesoB += articulo.peso
            else:
                numA += 1
                pesoA += articulo.peso
        self.colorear(self.wids['tv_balas'])
        # Campos del pie de la tabla:
        self.wids['e_numA'].set_text(str(numA))
        self.wids['e_numB'].set_text(str(numB))
        self.wids['e_pesoA'].set_text("%s" % (utils.float2str(pesoA)))
        self.wids['e_pesoB'].set_text("%s" % (utils.float2str(pesoB)))
        articulos = [d for d in self.objeto.articulos]
        self.wids['e_num_balas'].set_text(str(len(articulos)))
        pesos = [b.peso for b in articulos]
        self.wids['e_peso_total'].set_text(utils.float2str(sum(pesos)))
        partedeproduccion = self.objeto
        tiempototal, tiemporeal = self.calcular_tiempo_trabajado(partedeproduccion)
        self.wids['e_tiempo_real_trabajado'].set_text(tiemporeal.strftime('%H:%M'))
        try:
            productividad = (tiemporeal.seconds / tiempototal.seconds) * 100
        except ZeroDivisionError:
            productividad = 100   # A falta de infinito...
        self.wids['e_productividad'].set_text("%.2f %%" % productividad)
        o80 = partedeproduccion.prodestandar
        pteorica = o80 * tiempototal.hours  # @UnusedVariable
        # Me muevo abajo del todo del TreeView usando los adjustments:
        # vadj = self.wids['scrolledwindow1'].get_vadjustment()
        # myprint(vadj.lower, vadj.upper, vadj.page_size)
        # vadj.set_value(vadj.upper)
        if last_iter_bala != None:
            sel = self.wids['tv_balas'].get_selection()
            sel.select_iter(last_iter_bala)
            self.wids['tv_balas'].scroll_to_cell(model.get_path(last_iter_bala),
                                                 use_align = True)
        self.rellenar_datos_lote()
        self.rellenar_tabla_consumos()
        self.rellenar_tabla_conf_silos()

    def rellenar_tabla_consumos(self):
        """
        Rellena la tabla de consumos del parte.
        """
        parte = self.objeto
        if parte != None:
            model = self.wids['tv_consumos'].get_model()
            self.wids['tv_consumos'].set_model(None)
            model.clear()
            consumos = parte.consumos[:]
            try:
                consumos.sort(lambda c1, c2: c1 != None and c2 != None and int(c1.id - c2.id) or 0)
            except TypeError, msg:
                myprint("partes_de_fabricacion_balas.py (rellenar_tabla_consumos): Error ordenando consumos (%s):\n%s" % (msg, consumos))
            for c in parte.consumos:
                if c.productoCompraID != None:
                    unidad = c.productoCompra.unidad
                    producto = c.productoCompra.descripcion
                else:
                    unidad = ""
                    producto = ""
                model.append((c.siloID and c.silo.nombre or "",
                              producto,
                              "%s %s" % (utils.float2str(c.cantidad), unidad),
                              c.id))
            self.wids['tv_consumos'].set_model(model)

    def rellenar_tabla_conf_silos(self):
        """
        Rellena la tablas de consumo de granza de silos en el parte actual.
        """
        parte = self.objeto
        if parte != None:
            model = self.wids['tv_granza_silos'].get_model()
            #self.wids['tv_granza_silos'].set_model(None)
            model.clear()
            try:
                confs_silos = self.objeto.get_historial_conf_silos()
            except AssertionError, err:
                #raise AssertionError, err # Para que me lo envíe por correo.
                self.logger.error("partes_de_fabricacion_balas::"
                                  "rellenar_tabla_conf_silos -> %s" % err)
                confs_silos = []    # Pero que siga funcionando la ventana.
                self.wids['tv_granza_silos'].set_sensitive(False)
            for horaini in confs_silos:
                self.wids['tv_granza_silos'].set_sensitive(True)
                try:
                    horafin = confs_silos.keys()[
                            confs_silos.keys().index(horaini) + 1]
                except IndexError:
                    horafin = self.objeto.fechahorafin
                configs = confs_silos[horaini]
                if configs:     # Si no tiene nada, prefiero no mostrar nada.
                    padre = model.append(None, (utils.str_fechahora(horaini),
                                                utils.str_fechahora(horafin),
                                                "", "", "", ""))
                    for silo in configs:
                        cs = configs[silo]
                        porcentaje = cs.porcentaje
                        pc = cs.productoCompra
                        try:
                            nombresilo = silo.nombre
                        except AttributeError:  # Es de reciclada
                            nombresilo = "Silo ficticio n.º %d" % cs.reciclada
                        fila = ("", #utils.str_fechahora(horaini),
                                "", #utils.str_fechahora(horafin),
                                nombresilo,
                                utils.float2str(porcentaje * 100.0, autodec=True),
                                pc.descripcion,
                                cs.puid)
                        model.append(padre, fila)
            #self.wids['tv_granza_silos'].set_model(model)

    def get_lote(self):
        """
        Devuelve un lote (clase Lote), lote de cemento
        (clase LoteCem) o None si no hay lote activo en
        el parte.
        Los lotes de fibra se buscan por número y por código,
        los de cemento sólo por código, por lo que siempre
        el texto a buscar debe llevar "C-".
        """
        codigolote = self.wids['e_numlote'].get_text()
        if codigolote == None or codigolote.strip() == "":
            # No hay lote seleccionado. Devuelvo None antes de que salte una excepción al "parsear" el texto.
            lote = None
        elif codigolote.upper().startswith("C-"):
            try:
                lote = pclases.LoteCem.select(
                    pclases.LoteCem.q.codigo == codigolote)[0]
            except IndexError:
                lote = None
        else:
            try:
                codigolote = int(codigolote.replace("L-", ""))
                lote = pclases.Lote.select(pclases.Lote.q.numlote == codigolote)[0]
            except IndexError:
                try:
                    lote = pclases.LoteCem.select(pclases.LoteCem.q.codigo == codigolote)[0]
                except IndexError:
                    lote = None
            except ValueError, msg:
                lote = None
                self.logger.warning("partes_de_fabricacion_balas::get_lote -> Valor de lote incorrecto: %s. Parte ID %d. Excepción: %s." % (codigolote, self.objeto.id, msg))
            except Exception, e:
                self.logger.error("partes_de_fabricacion_balas::get_lote -> Busco lote por contenido del parte en lugar de por el entry. Parte ID %d. Excepción %s." % (self.objeto.id, e))
                lote = None
                if self.objeto.articulos != []:
                    lote = self.objeto.articulos[0].bala.lote
        return lote

    def rellenar_datos_lote(self):
        """
        Introduce en los "entry" los datos de las balas
        para el lote completo.
        """
        lote = self.get_lote()
        bultos_a = 0
        bultos_b = 0
        kgs_a = 0
        kgs_b = 0
        if isinstance(lote, pclases.Lote):
            tipo_bulto = "balas"
            for bala in lote.balas:
                if bala.claseb:
                    bultos_b += 1
                    kgs_b += bala.pesobala
                else:
                    bultos_a += 1
                    kgs_a += bala.pesobala
        elif isinstance(lote, pclases.LoteCem):
            tipo_bulto = "bigbags"
            for bigbag in lote.bigbags:
                if bigbag.claseb:
                    bultos_b += 1
                    kgs_b += bigbag.pesobigbag
                else:
                    bultos_a += 1
                    kgs_a += bigbag.pesobigbag
        else:
            tipo_bulto = "?"
        self.wids['e_bultos_a_lote'].set_text("%d %s" % (bultos_a, tipo_bulto))
        self.wids['e_bultos_b_lote'].set_text("%d %s" % (bultos_b, tipo_bulto))
        self.wids['e_kgs_a_lote'].set_text(utils.float2str(kgs_a))
        self.wids['e_kgs_b_lote'].set_text(utils.float2str(kgs_b))

    def rellenar_datos_producto(self, producto):
        """
        Introduce la información que puede a partir del producto
        recibido.
        """
        self.wids['e_articulo'].set_text(producto.descripcion)
        self.wids['e_dtex'].set_text("%.2f" % producto.camposEspecificosBala.dtex)
        self.wids['e_longitud'].set_text(`producto.camposEspecificosBala.corte`)

    def rellenar_datos_articulo(self, producto):
        """
        A partir del artículo recibido, completa la información
        de la cabecera del formulario (DTEX, etc...) en
        función de los datos de la bala.
        Lo que recibe en realidad es una lista de detalles de
        producción que tienen una bala asociada.
        """
        if producto == None:
            self.wids['e_articulo'].set_text('')
            self.wids['e_dtex'].set_text('')
            self.wids['e_longitud'].set_text('')
        else:
            self.wids['e_articulo'].set_text(producto.nombre)
            self.wids['e_dtex'].set_text(producto.camposEspecificosBala and str(producto.camposEspecificosBala.dtex) or '')
            self.wids['e_longitud'].set_text(producto.camposEspecificosBala and str(producto.camposEspecificosBala.corte) or '')

    # --------------- Manejadores de eventos ----------------------------
    def cambiar_horas_trabajadas(self, cell, path, newtext):
        newtext = newtext.replace(".", ":").replace(",", ":")
        if ":" not in newtext:
            if len(newtext) < 4:
                newtext = ("0" * (4 - len(newtext))) + newtext
            newtext = "%s:%s" % (newtext[:-2], newtext[-2:])
        model = self.wids['tv_empleados'].get_model()
        ide = model[path][-1]
        ht = pclases.HorasTrabajadas.get(ide)
        try:
            dtdelta = mx.DateTime.DateTimeDelta(0, float(newtext.split(':')[0]), float(newtext.split(':')[1]), 0)
            if dtdelta > self.objeto.get_duracion():
                utils.dialogo_info(titulo = "TIEMPO INCORRECTO",
                                   texto = "El tiempo trabajado no puede superar la\nduración del parte de producción.",
                                   padre = self.wids['ventana'])
                return
            ht.horas = newtext
            ht.sync()
            model[path][3] = ht.horas.strftime('%H:%M')
            # self.rellenar_tabla_empleados()
        except (ValueError, IndexError):
            utils.dialogo_info(titulo = "ERROR",
                               texto = 'El texto "%s" no representa el formato horario.' % (newtext),
                               padre = self.wids['ventana'])

    def cambiar_peso_bala(self, cell, path, newtext):
        model = self.wids['tv_balas'].get_model()
        if model[path][1] == 0 or model[path][1] == '': # Nº bala, no tiene, no es una bala.
            return
        codigo = model[path][1]
        silo_marcado = False
        for silo in pclases.Silo.select():
            silo_marcado = silo_marcado or self.wids['ch_silo_ID%d' % (silo.id)].get_active()
        silo_marcado = silo_marcado or self.wids['ch_reciclada_0'].get_active() or self.wids['ch_reciclada_1'].get_active()
        if silo_marcado == False:
            utils.dialogo_info(titulo = "NO PUEDE CAMBIAR LA PRODUCCIÓN",
                               texto = "No puede cambiar el peso total de la producción si no marca el silo\noriginal de donde consumió la bala %s." % (codigo),
                               padre = self.wids['ventana'])
            return
        try:
            bala = pclases.Bala.select(pclases.Bala.q.codigo == codigo)[0]
            self.descontar_material_adicional(bala.articulos[0], restar = False)
            try:
                bala.pesobala = float(newtext)
            except ValueError:
                utils.dialogo_info('NÚMERO INCORRECTO', 'El peso de la bala debe ser un número.', padre = self.wids['ventana'])
                return
            self.descontar_material_adicional(bala.articulos[0], restar = True)
            model[path][2] = bala.pesobala
        except IndexError:
            bigbag = pclases.Bigbag.select(pclases.Bigbag.q.codigo == codigo)[0]
            self.descontar_material_adicional(bigbag.articulos[0], restar = False)
            try:
                bigbag.pesobigbag = float(newtext)
            except ValueError:
                utils.dialogo_info('NÚMERO INCORRECTO', 'El peso del bigbag debe ser un número.', padre = self.wids['ventana'])
                return
            self.descontar_material_adicional(bigbag.articulos[0], restar = True)
            model[path][2] = bigbag.pesobigbag
        itr = model.get_iter(path)
        itr = model.iter_next(itr)
        if itr != None:
            path = model.get_path(itr)
            column = self.wids['tv_balas'].get_column(2)
            self.wids['tv_balas'].set_cursor_on_cell(path, column, cell, start_editing=False)
        pesos = [b.peso for b in self.objeto.articulos]
        self.wids['e_peso_total'].set_text(utils.float2str(sum(pesos)))
        self.rellenar_datos_lote()

    def cambiar_observaciones(self, cell, path, newtext):
        model = self.wids['tv_balas'].get_model()
        ide = model[path][-1]
        if model[path][1] != '':    # Nº bala, tiene, no es una incidencia.
            # Verifico que sea de clase B y cambio el campo motivo.
            articulo = pclases.Articulo.get(ide)
            if articulo.es_bala():
                bala_o_bb = articulo.bala
            elif articulo.es_bigbag():
                bala_o_bb = articulo.bigbag
            else:
                bala_o_bb = None
            if not bala_o_bb.claseb and newtext != '':
                if utils.dialogo(titulo = 'FIBRA CLASE A',
                                 texto = 'Esta fibra está marcada actualmente como clase A.\n¿Marcar como clase B?',
                                 padre = self.wids['ventana']):
                    bala_o_bb.claseb = True
            bala_o_bb.motivo = newtext
        else:
            incidencia = pclases.Incidencia.get(ide)
            incidencia.observaciones = newtext
        self.rellenar_tabla_balas()

    def cambiar_claseb(self, cell, path):
        model = self.wids['tv_balas'].get_model()
        if model[path][1] == '':    # Nº bala, no tiene, por tanto es una incidencia.
            return
        ide = model[path][-1]
        articulo = pclases.Articulo.get(ide)
        if articulo.es_bala():
            bala_o_bb = articulo.bala
        elif articulo.es_bigbag():
            bala_o_bb = articulo.bigbag
        else:
            bala_o_bb = None
        bala_o_bb.claseb = not bala_o_bb.claseb
        self.rellenar_tabla_balas()

    def cambiar_motivo_incidencia(self, cell, path, newtext):
        # Funcionalidad no implementada.
        pass

    def cambiar_inicio_incidencia(self, cell, path, newtext):
        model = self.wids['tv_balas'].get_model()
        if model[path][1] != '':    # Nº bala, tiene, no es una incidencia.
            return
        ide = model[path][-1]
        incidencia = pclases.Incidencia.get(ide)
        self.objeto.sync()
        try:
            incidencia.horainicio = mx.DateTime.DateTimeFrom(day = self.objeto.fecha.day,
                                                             month = self.objeto.fecha.month,
                                                             year = self.objeto.fecha.year,
                                                             hour = int(newtext.split(":")[0]),
                                                             minute = int(newtext.split(":")[1]))
            if (incidencia.horafin - incidencia.horainicio).days > 1:
                incidencia.horainicio + mx.DateTime.oneDay
            while incidencia.horainicio < self.objeto.fechahorainicio: # El
                # parte está en la franja de medianoche y la incidencia
                # comienza después de las 12.
                try:
                    incidencia.horainicio += mx.DateTime.oneDay   # Debe llevar
                                                # la fecha del día siguiente.
                    incidencia.horafin += mx.DateTime.oneDay
                except TypeError:   # Es un datetime
                    incidencia.horainicio += datetime.timedelta(1)
                    incidencia.horafin += datetime.timedelta(1)
        except (ValueError, IndexError):
            utils.dialogo_info('HORA INCORRECTA',
                               'La fecha y hora deben respetar el formato '
                               'inicial.\nSe va a reestablecer el valor '
                               'antiguo,\na continuación trate de editar este'
                               ' valor conservando su formato.',
                               padre = self.wids['ventana'])
            return
        if incidencia.horainicio > incidencia.horafin:      # NOTA: No va a
            # entrar nunca. Por ejemplo, 12:00 no es menor que 11:00, ya que
            # las 11:00 _son del día siguiente_ cuando llega aquí, tal vez
            # debiera mejor controlar que ninguna parada sea de más de 8 horas
            # o algo así. O de más duración del parte... o algo.
            (incidencia.horainicio,
             incidencia.horafin) = (incidencia.horafin, incidencia.horainicio)
        self.rellenar_tabla_balas()

    def cambiar_fin_incidencia(self, cell, path, newtext):
        model = self.wids['tv_balas'].get_model()
        if model[path][1] != '':    # Nº bala, tiene, no es una incidencia.
            return
        ide = model[path][-1]
        incidencia = pclases.Incidencia.get(ide)
        self.objeto.sync()
        try:
            incidencia.horafin = mx.DateTime.DateTimeFrom(
                    day = self.objeto.fecha.day,
                    month = self.objeto.fecha.month,
                    year = self.objeto.fecha.year,
                    hour = int(newtext.split(":")[0]),
                    minute = int(newtext.split(":")[1]))
            if (incidencia.horafin - incidencia.horainicio).days < 0:
                incidencia.horafin += mx.DateTime.oneDay
            while incidencia.horainicio < self.objeto.fechahorainicio: # El
                # parte está en la franja de medianoche y la incidencia
                # comienza después de las 12.
                try:
                    incidencia.horainicio += mx.DateTime.oneDay   # Debe llevar
                    incidencia.horafin += mx.DateTime.oneDay    # la fecha del
                                                                # día siguiente
                except TypeError:   # Es un datetime
                    incidencia.horainicio += datetime.timedelta(1)
                    incidencia.horafin += datetime.timedelta(1)
        except (ValueError, IndexError):
            utils.dialogo_info('HORA INCORRECTA',
                               'La fecha y hora deben respetar el formato'
                               ' inicial.\nSe va a reestablecer el valor '
                               'antiguo,\na continuación trate de editar este'
                               ' valor conservando su formato.',
                               padre = self.wids['ventana'])
            return
        if incidencia.horainicio > incidencia.horafin:
            (incidencia.horainicio,
             incidencia.horafin) = incidencia.horafin, incidencia.horainicio
        self.rellenar_tabla_balas()

    def crear_nuevo_partedeproduccion(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        partedeproduccion = self.objeto
            # Datos a pedir: Ninguno. Lo planto todo con valores por defecto y listo.
        if not utils.dialogo('Se creará un nuevo parte de producción vacío.',
                             'NUEVO PARTE',
                             padre = self.wids['ventana']):
            return
        if partedeproduccion != None:
            partedeproduccion.notificador.desactivar()
        horainicio = time.struct_time(time.localtime()[:4]+(0,0)+time.localtime()[6:])
        horafin = time.struct_time(time.localtime()[:3]+((time.localtime()[3]+8)%24, 0,0)+time.localtime()[6:])
        partedeproduccion = pclases.ParteDeProduccion(fecha = mx.DateTime.localtime(),
                                                      horainicio = horainicio,
                                                      horafin = horafin,
                                                      prodestandar = 0,
                                                      observaciones = ';;;;;',
                                                      bloqueado = False)
        pclases.Auditoria.nuevo(partedeproduccion, self.usuario, __file__)
        partedeproduccion._corregir_campos_fechahora()
        self.objeto = partedeproduccion
        self.wids['e_numlote'].set_text('')
        self.add_empleados_calendario()
        self.__lecturaescritura = self.objeto.id
        self.actualizar_ventana()
        self.objeto.notificador.activar(self.aviso_actualizacion)
        verificar_solapamiento(partedeproduccion, self.wids['ventana'])

    def buscar_partedeproduccion(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        partedeproduccion = self.objeto
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR PARTE",
            texto = "Introduzca fecha del parte o nombre del producto:",
            padre = self.wids['ventana'])
        if a_buscar != None:
            try:
                if a_buscar != '':
                    a_buscar = a_buscar.replace("-", "/")
                    if a_buscar.count('/') == 1:
                        a_buscar = "%s/%d" % (a_buscar,
                                              mx.DateTime.localtime().year)
                    try:
                        fecha = utils.parse_fecha(a_buscar)
                    except ValueError:
                        fecha = ""
                    resultados = pclases.ParteDeProduccion.select(
                        pclases.ParteDeProduccion.q.fecha == fecha)
                else:
                    resultados = pclases.ParteDeProduccion.select()
                resultados = [p for p in resultados if p.es_de_balas()]
            except:     # TODO: No funciona bien la búsqueda por producto. Al
                        # buscar Fibra 6.7/90, como hay un "/" busca por fecha.
                producto = pclases.ProductoVenta.select(pclases.AND(
                    pclases.ProductoVenta.q.nombre.contains(a_buscar),
                    pclases.ProductoVenta.q.camposEspecificosBalaID != None))
                resultados = pclases.ParteDeProduccion.select()
                # Pongo la barra porque con muchos partes esto tarda
                vpro = VentanaProgreso(padre = self.wids['ventana'])
                vpro.mostrar()
                i = 0.0
                tot = resultados.count()
                partes = []
                if producto.count() > 1:
                    idproducto = self.refinar_resultados_busqueda_producto(
                                    producto)
                    if idproducto != None:
                        #for p in resultados:
                        #    if p.articulos != [] and p.articulos[0].productoVentaID == idproducto:
                        #        partes.append(p)
                        for p in pclases.ParteDeProduccion.select("""
                            id IN (SELECT parte_de_produccion_id
                                   FROM articulo
                                   WHERE articulo.producto_venta_id = %d)
                            """ % (idproducto)):
                            partes.append(p)
                            vpro.set_valor(i/tot, 'Buscando partes')
                            i += 1
                    else:
                        vpro.ocultar()
                        return
                elif producto.count() == 1:
                    #for p in resultados:
                    #    if p.articulos != [] and p.articulos[0].productoVentaID == producto[0].id:
                    #        partes.append(p)
                        for p in pclases.ParteDeProduccion.select("""
                            id IN (SELECT parte_de_produccion_id
                                   FROM articulo
                                   WHERE articulo.producto_venta_id = %d)
                            """ % (producto[0].id)):
                            partes.append(p)
                        vpro.set_valor(i/tot, 'Buscando partes')
                        i += 1
                else:
                    for p in resultados:
                        if p.es_de_balas():
                            partes.append(p)
                        vpro.set_valor(i/tot, 'Buscando partes')
                        i += 1
                vpro.ocultar()
                resultados = partes
            # NOTA: Ver ir_a_primero para comprender el criterio de seleccion.
            # OJO: Se usa en dos partes del código: refactorizar y crear una
            # funcioncita por si hay que cambiarlo en el futuro.
            if len(resultados) > 1:
                ## Refinar los resultados
                idpartedeproduccion=self.refinar_resultados_busqueda(resultados)
                if idpartedeproduccion == None:
                    return
                resultados = [pclases.ParteDeProduccion.get(idpartedeproduccion)]
            elif len(resultados) < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info('SIN RESULTADOS',
                    'La búsqueda no produjo resultados.\nPruebe a cambiar el'\
                    ' texto buscado o déjelo en blanco para ver una lista co'\
                    'mpleta.\n(Atención: Ver la lista completa puede resulta'\
                    'r lento si el número de elementos es muy alto)',
                    padre = self.wids['ventana'])
                return
            ## Un único resultado
            # Primero anulo la función de actualización
            if partedeproduccion != None:
                partedeproduccion.notificador.desactivar()
            # Pongo el objeto como actual
            try:
                partedeproduccion = resultados[0]
            except IndexError:
                utils.dialogo_info(titulo = "ERROR",
                    texto = "Se produjo un error al recuperar la información."\
                    "\nCierre y vuelva a abrir la ventana antes de volver a i"\
                    "ntentarlo.",
                    padre = self.wids['ventana'])
                return None
            # Y activo la función de notificación:
            partedeproduccion.notificador.activar(self.aviso_actualizacion)
        self.objeto = partedeproduccion
        self.actualizar_ventana()

    def guardar(self, widget):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        partedeproduccion = self.objeto
        (ye_olde_fecha,
         ye_olde_horainicio,
         ye_olde_horafin) = (partedeproduccion.fecha,
                             partedeproduccion.horainicio,
                             partedeproduccion.horafin)
        ye_olde_horainicio = utils.str_hora_corta(partedeproduccion.horainicio)
        ye_olde_horafin = utils.str_hora_corta(partedeproduccion.horafin)
            # Campos del objeto que hay que guardar:
        # Fecha, horainicio, horafin, prodestandar y observaciones con el
        # formateado especial.
        fecha = self.wids['e_fecha'].get_text()
        horainicio = self.wids['e_hora_ini'].get_text()
        horainicio = horainicio.replace(".", ":").replace(",", ":")
        if ":" not in horainicio:
            if len(horainicio) < 4:
                horainicio = ("0" * (4 - len(horainicio))) + horainicio
            horainicio = "%s:%s" % (horainicio[:-2], horainicio[-2:])
        if not horainicio or horainicio.strip() == "":
            msg = "partes_de_fabricacion_balas.py::guardar -> Error al leer hora inicio. Parte ID %d. horainicio = %s. Pongo horainicio a valor actual del parte." % (self.objeto.id, horainicio)
            self.logger.error(msg)
            myprint(msg)
            horainicio = utils.str_hora_corta(self.objeto.horainicio)
        horafin = self.wids['e_hora_fin'].get_text()
        horafin = horafin.replace(".", ":").replace(",", ":")
        if ":" not in horafin:
            if len(horafin) < 4:
                horafin = ("0" * (4 - len(horafin))) + horafin
            horafin = "%s:%s" % (horafin[:-2], horafin[-2:])
        if not horafin or horafin.strip() == "":
            msg = "partes_de_fabricacion_balas.py::guardar -> Error al leer hora inicio. Parte ID %d. horafin = %s. Pongo horafin a valor actual del parte." % (self.objeto.id, horafin)
            self.logger.error(msg)
            myprint(msg)
            horafin = utils.str_hora_corta(self.objeto.horafin)
        prodestandar = self.wids['e_o80'].get_text()
        try:
            prodestandar = float(prodestandar)
        except:
            prodestandar = 0
        observaciones = self.procesar_observaciones()
        # Desactivo el notificador momentáneamente
        partedeproduccion.notificador.activar(lambda: None)
        # Actualizo los datos del objeto
        try:
            partedeproduccion.fecha = utils.parse_fecha(fecha)
        except:
            partedeproduccion.fecha = mx.DateTime.localtime()
        partedeproduccion.sync()    # Para forzar a que el atributo fecha sea una fecha "válida" dentro del dominio antes de leerlo para guardar la hora.
        try:
            partedeproduccion.horainicio = mx.DateTime.DateTimeFrom(
                day = partedeproduccion.fecha.day,
                month = partedeproduccion.fecha.month,
                year = partedeproduccion.fecha.year,
                hour = int(horainicio.split(":")[0]),
                minute = int(horainicio.split(":")[1]))
            partedeproduccion.horafin = mx.DateTime.DateTimeFrom(
                day = partedeproduccion.fecha.day,
                month = partedeproduccion.fecha.month,
                year = partedeproduccion.fecha.year,
                hour = int(horafin.split(":")[0]),
                minute = int(horafin.split(":")[1]))
        except Exception, e:
            msg = "partes_de_fabricacion_balas.py::guardar -> Error al guardar la hora. Parte ID %d. horainicio = %s; horafin = %s. Excepción: %s" % (self.objeto.id, horainicio, horafin, e)
            myprint(msg)
            self.logger.error(msg)
        partedeproduccion.prodestandar = prodestandar
        partedeproduccion.observaciones = observaciones
        partedeproduccion.fichaproduccion = self.wids['e_fichaproduccion'].get_text()
        partedeproduccion._corregir_campos_fechahora()
        # Verificación de que no se solapa con otros partes:
        verificar_solapamiento(partedeproduccion, self.wids['ventana'],
                               ye_olde_fecha, ye_olde_horainicio,
                               ye_olde_horafin)
        # Guardo configuración de silos
        self.save_conf_silos()
        # Fuerzo la actualización de la BD y no espero a que SQLObject lo haga por mí:
        partedeproduccion.syncUpdate()
        # Vuelvo a activar el notificador
        partedeproduccion.notificador.activar(self.aviso_actualizacion)
        self.actualizar_ventana()
        self.wids['b_guardar'].set_sensitive(False)

    def borrar_parte(self, boton):
        if not utils.dialogo('Se va a intentar eliminar el parte actual.\nSi hay operaciones complejas implicadas se cancelará el borrado.\nDe cualquier forma, no se aconseja eliminar ningún parte que ya tenga producción, paradas o empleados relacionados.\n¿Está seguro de borrar el parte actual?', 'ELIMINAR PARTE', padre = self.wids['ventana']):
            return
        partedeproduccion = self.objeto
        partedeproduccion.notificador.desactivar()
        if (len(partedeproduccion.incidencias) == 0
            and len(partedeproduccion.articulos) == 0):
            try:
                #partedeproduccion.destroy(ventana = __file__)
                partedeproduccion.destroy_en_cascada(ventana = __file__)
            except:
                utils.dialogo_info('PARTE NO BORRADO', 'El parte no se eliminó.\nSi tiene producción, incidencias o empleados asociados, trate primero de eliminarlos y vuelva a intentarlo.', padre = self.wids['ventana'])
                return
            self.ir_a_primero()

    def mostrar_calendario(self, boton):
        self.wids['e_fecha'].set_text(utils.str_fecha(utils.mostrar_calendario(fecha_defecto = self.objeto and self.objeto.fecha or None, padre = self.wids['ventana'])))
        self.guardar(None)
        self.add_empleados_calendario()
        self.rellenar_tabla_empleados()

    def set_hora_inicial(self, boton):
        valor_hora_ini = self.wids['e_hora_ini'].get_text()
        try:
            valor_hora_ini = [int(v) for v in valor_hora_ini.split(':')] + [0]
            assert len(valor_hora_ini) >= 3
        except:
            valor_hora_ini = [0,0,0]
        hora_ini = utils.mostrar_hora(valor_hora_ini[0], valor_hora_ini[1], valor_hora_ini[2], 'HORA INICIO PARTE')
        if hora_ini != None:
            partedeproduccion = self.objeto
            partedeproduccion.notificador.desactivar()
            partedeproduccion.horainicio = hora_ini
            partedeproduccion._corregir_campos_fechahora()
            self.set_hora_final(boton)      # Ahí se cambiarán los empleados si es preciso.
            self.actualizar_ventana()
            partedeproduccion.notificador.activar(self.aviso_actualizacion)
            verificar_solapamiento(partedeproduccion, self.wids['ventana'])

    def set_hora_final(self, boton):
        valor_hora_fin = self.wids['e_hora_fin'].get_text()
        try:
            valor_hora_fin = [int(v) for v in valor_hora_fin.split(':')] + [0]
            assert len(valor_hora_fin) >= 3
        except:
            valor_hora_fin = [0,0,0]
        hora_fin = utils.mostrar_hora(valor_hora_fin[0], valor_hora_fin[1], valor_hora_fin[2], 'HORA FIN PARTE')
        if hora_fin != None:
            partedeproduccion = self.objeto
            partedeproduccion.notificador.desactivar()
            partedeproduccion.horafin = hora_fin
            partedeproduccion._corregir_campos_fechahora()
            partedeproduccion.syncUpdate()
            partedeproduccion.sync()
            self.add_empleados_calendario()
            self.actualizar_ventana()
            partedeproduccion.notificador.activar(self.aviso_actualizacion)
            verificar_solapamiento(partedeproduccion, self.wids['ventana'])

    def buscar_producto(self, criterio_lineas):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        producto = None
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR PRODUCTO",
                texto = "Introduzca código, nombre o descripción de producto:",
                padre = self.wids['ventana'])
        if a_buscar != None:
            try:
                ida_buscar = int(a_buscar)
            except ValueError:
                ida_buscar = -1
            criterio = pclases.OR(
                    pclases.ProductoVenta.q.codigo.contains(a_buscar),
                    pclases.ProductoVenta.q.descripcion.contains(a_buscar),
                    pclases.ProductoVenta.q.nombre.contains(a_buscar),
                    pclases.ProductoVenta.q.id == ida_buscar)
            no_obsoleto = pclases.ProductoVenta.q.obsoleto == False
            criterio = pclases.AND(criterio, criterio_lineas, no_obsoleto)
            resultados = pclases.ProductoVenta.select(criterio)
            if resultados.count() > 1:
                    ## Refinar los resultados
                    idproducto = self.refinar_resultados_busqueda_producto(resultados)
                    if idproducto == None:
                        return None
                    resultados = [pclases.ProductoVenta.get(idproducto)]
                    # Se supone que la comprensión de listas es más rápida que hacer un nuevo get a SQLObject.
                    # Me quedo con una lista de resultados de un único objeto ocupando la primera posición.
                    # (Más abajo será cuando se cambie realmente el objeto actual por este resultado.)
            elif resultados.count() < 1:
                    ## Sin resultados de búsqueda
                    utils.dialogo_info('SIN RESULTADOS', 'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.\n(Atención: Ver la lista completa puede resultar lento si el número de elementos es muy alto)',
                                       padre = self.wids['ventana'])
                    return None
            ## Un único resultado
            # Pongo el objeto como actual
            try:
                producto = resultados[0]
            except IndexError:
                utils.dialogo_info(titulo = "ERROR",
                                   texto = "Se produjo un error al recuperar la información.\nCierre y vuelva a abrir la ventana antes de volver a intentarlo.",
                                   padre = self.wids['ventana'])
                return None
        return producto

    def refinar_resultados_busqueda_producto(self, resultados):
        """
        Muestra en una ventana de resultados todos los
        registros de "resultados".
        Devuelve el id (primera columna de la ventana
        de resultados) de la fila seleccionada o None
        si se canceló.
        """
        filas = [(p.id,
                  p.codigo,
                  p.camposEspecificosBala and p.camposEspecificosBala.dtex or 0.0,
                  p.camposEspecificosBala and p.camposEspecificosBala.corte or 0.0,
                  p.nombre,
                  p.descripcion) for p in resultados]
                # Si no tiene camposEspecificosBala prefiero que salte una excepción.
        idproducto = utils.dialogo_resultado(filas, 'SELECCIONE PRODUCTO',
                                             cabeceras = ['ID', 'Código', 'dtex', 'corte', 'Nombre', 'Descripción'],
                                             padre = self.wids['ventana'])
        if idproducto < 0:
            return None
        else:
            return idproducto


    def set_articulo(self, boton):
        """
        Muestra un cuadro de búsqueda de productos*.
        El seleccionado pasará a ser el
        artículo del parte, mostrándose su información en la
        cabecera y limitando las opciones al añadir líneas.
        * Productos que sean balas o tengan como línea de
        producción la línea de fibra.
        No se permite cambiar de artículo si el parte ya tiene
        balas relacionadas.
        """
        if self.objeto.articulos != []:
            txt = """
            Ya se ha iniciado la producción de un artículo. Si cambia el producto del parte actual
            cambiará también en las balas ya fabricadas pertenecientes al parte.
            Si lo que desea es iniciar una nueva producción use el botón "Nuevo parte" y comience
            un nuevo parte de producción. Si lo que quiere es cambiar el producto del parte actual
            y todas sus balas fabricadas pulse "Sí".
            ¿Desea cambiar el producto fabricado en el parte?
            """
            if not utils.dialogo(titulo = '¿CAMBIAR LA PRODUCCIÓN?', texto = txt, padre = self.wids['ventana']):
                return
        try:
            idlineafibra = pclases.LineaDeProduccion.select(
                    pclases.LineaDeProduccion.q.nombre=='Línea de fibra')[0]
            # OJO: Debe llamarse EXACTAMENTE Línea de fibra en la BD.
        except:     # No hay línea de fibra
            utils.dialogo_info('ERROR LÍNEA DE FIBRA',
                               'No se encontró línea de fibra en la base de datos del sistema.\nCierre el programa y contacte con el administrador.',
                               padre = self.wids['ventana'])
            return
        criterio = pclases.AND(pclases.ProductoVenta.q.lineaDeProduccionID == idlineafibra.id,
                               pclases.ProductoVenta.q.camposEspecificosBalaID != None)
        producto = self.buscar_producto(criterio)
        if not producto:    # Canceló
            return
        self.producto = producto
        if producto.es_bala_cable():
            utils.dialogo_info(titulo = "NO APLICABLE",
                               texto = "Las balas de material para reciclar se gestionan desde otra ventana.\nSeleccione otro producto.",
                               padre = self.wids['ventana'])
            producto = None
        if producto != None:
            self.wids['e_o80'].set_text(utils.float2str(self.producto.prodestandar))
            self.guardar(None)
            self.producto = producto
            self.rellenar_datos_producto(self.producto)
            # TODO: Meter una barra de progreso. Al conectar con Murano, tarda.
            for a in self.objeto.articulos:
                a.productoVenta = self.producto
                self.logger.debug("Cambiando producto de %s en Murano a %s "
                                  "[%s]." % (
                    a.codigo, producto.descripcion, producto.puid))
                murano.ops.update_producto(a, producto)

    def comprobar_silos_marcados(self):
        """
        Devuelve True si hay al menos un silo marcado.
        """
        # XXX: Caso especial para reenvasado de bigbags: 27 de marzo de 2007.
        if self.objeto.es_parte_de_reenvasado():
            silo_marcado = True     # Engaño a la ventana y le digo que sí se
                # ha marcado un silo aunque sea mentira. No se va a consumir
                # de él de todas formas.
        else:
        # XXX
            silo_marcado = False
            for silo in pclases.Silo.select():
                silo_marcado = silo_marcado or self.wids['ch_silo_ID%d' % (silo.id)].get_active()
            silo_marcado = silo_marcado or self.wids['ch_reciclada_0'].get_active() or self.wids['ch_reciclada_1'].get_active()
            if silo_marcado == False:
                utils.dialogo_info(titulo = "NO PUEDE PRODUCIR",
                                   texto = "¡No puede producir fibra si no marca un silo de donde consumir granza!",
                                   padre = self.wids['ventana'])
        return silo_marcado

    def comprobar_silos_existencias(self):
        """
        Comprueba que todos los silos, incuyendo los "virtuales" de granza
        reciclada, tienen existencias por encima de 0 (no comprueba que haya
        existencias suficientes para determinado consumo ya que aún no se
        ha producido y tampoco es necesario ser tan estrictos; al fin y al
        cabo todos los consumos son aproximados).
        Devuelve False y muestra un diálogo de error si algún silo o producto
        de compra que actúa como granza reciclada está a 0 o tiene existencias
        negativas.
        También verifica que si hay granza reciclada marcada, se haya
        seleccionado también un producto en el combo.
        """
        res = True
        # XXX: Caso especial para reenvasado de bigbags: 27 de marzo de 2007.
        if self.objeto.es_parte_de_reenvasado():
            res = True  # Engaño a la ventana y le digo que sí se ha marcado el 100%
        else:
            # XXX
            for silo in [s for s in pclases.Silo.select() if self.wids['ch_silo_ID%d' % (s.id)].get_active()]:
                try:
                    ocupado = murano.ops.get_ocupado_silo(silo)
                except:
                    self.logger.error(
                        "No se pudo leer Silo en Murano. Fallback a ginn.")
                    ocupado = silo.ocupado
                if ocupado <= 0:
                    utils.dialogo_info(titulo = "NO PUEDE PRODUCIR",
                                       texto = 'El silo "%s" está vacío.\nCompruébelo y corríjalo desde la ventana correspondiente si fuera necesario.' % (silo.nombre),
                                       padre = self.wids['ventana'])
                    res = False
            if res:
                for numreciclada in (0, 1):
                    if self.wids['ch_reciclada_%d' % (numreciclada)].get_active():
                        idgranza = utils.combo_get_value(self.wids["cbe_reciclada_%d" % (numreciclada)])
                        if idgranza > 0:
                            granza = pclases.ProductoCompra.get(idgranza)
                            if granza.existencias <= 0:
                                utils.dialogo_info(titulo = "NO PUEDE PRODUCIR",
                                                   texto = 'El producto "%s" no tiene existencias.\n\nCompruébelo y corríjalo desde la ventana correspondiente si fuese necesario.' % (granza.descripcion),
                                                   padre = self.wids['ventana'])
                                res = False
                        else:
                            utils.dialogo_info(titulo = "NO PUEDE PRODUCIR",
                                               texto = "Ha seleccionado consumir granza reciclada, sin embargo no ha especificado cuál.",
                                               padre = self.wids['ventana'])
                            res = False
        return res

    def comprobar_silos_porcenajes(self):
        """
        Comprueba que la suma de porcentajes de comsumo de silos
        es del 100% en total.
        Devuelve False y muestra un diálogo de error en caso contario.
        """
        res = True
        porcentaje_total = 0
        for silo in [s for s in pclases.Silo.select() if self.wids['ch_silo_ID%d' % (s.id)].get_active()]:
            porcentaje = self.wids['escala_ID%d' % (silo.id)].get_value() / 100
            porcentaje_total += porcentaje
        for numreciclada in (0, 1):
            if self.wids['ch_reciclada_%d' % (numreciclada)].get_active():
                porcentaje = self.wids['s_reciclada_%d' % (numreciclada)].get_value() / 100.0
                porcentaje_total += porcentaje
        if porcentaje_total < 1.0:
            # XXX: Caso especial para reenvasado de bigbags: 27 marzo 2007.
            if self.objeto.es_parte_de_reenvasado():
                res = True  # Engaño a la ventana y le digo que sí se ha
                            # marcado el 100%
            else:
            # XXX
                utils.dialogo_info(titulo = "NO PUEDE PRODUCIR",
                        texto = "El porcentaje total de consumo de silos"
                                " debe ser del 100%.",
                        padre = self.wids['ventana'])
            res = False
        return res

    def comprobar_configuracion_consumos_silo(self):
        """
        Devuelve True si la configuración de los consumos de silos es
        correcta.
        Muestra una ventana de error y devuelve False (por este orden)
        en caso contrario.
        La configuración de los silos es correcta sii al menos hay un silo
        marcado ^ ningún silo marcado está a 0
            ^ sumatorio(porcentajes de silos) == 100.
        """
        res = False
        # XXX: Caso especial para reenvasado de bigbags: 27 de marzo de 2007.
        if self.objeto.es_parte_de_reenvasado():
            res = True #Engaño a la ventana y le digo que sí hay silos marcados
        else:
        # XXX
            # Compruebo que al menos hay un silo marcado.
            if self.comprobar_silos_marcados():
                # Compruebo que todos los silos están por encima de 0. Incluída la granza reciclada.
                if self.comprobar_silos_existencias():
                    # Compruebo que la suma de porcentajes es 100.
                    if self.comprobar_silos_porcenajes():
                        res = True
        return res

    def add_bala(self, boton):
        """
        Añade una bala al parte, chequeando primero que hay un producto
        válido seleccionado. Crea a la vez el registro artículo y bala
        correspondiente.
        1.- Chequea que self.producto != None.
        1 y 1/2.- Chequea que haya silos marcados, que no esté ninguno a 0 y que entre todos sumen 100%.
        2.- Chequea que haya un número de lote en la ventana.
        3.- Pide un número de bala o un rango completo.
        4.- Si ha metido un único número:
            4.1.- Pide el peso y número de la bala.
            4.2.- Crea una bala con código = str(número)
            4.3.- Asocia la bala al lote.
            4.4.- Crea el artículo relacionado con la bala.
            4.5.- Asocia el artículo al parte.
        5.- Si ha metido un rango:
            5.-1 Repite los pasos 4.2 a 4.5 para cada número del rango
                 y pide el peso de cada uno de ellos.
        6.- NUEVO -> Descuenta el material adicional por cada una de las balas.
        7.- NUEVO -> Guarda la configuración de consumo de los silos.
        """
        if self.comprobar_configuracion_consumos_silo():
            if self.producto == None:
                utils.dialogo_info(titulo = 'SELECCIONAR PRODUCTO',
                        texto = 'Seleccione primero el producto fabricado.',
                        padre = self.wids['ventana'])
                return
            codigolote = self.wids['e_numlote'].get_text()
            if "C-" in codigolote:
                try:
                    codigolote = int(codigolote.replace("C-", ""))
                    lote = pclases.LoteCem.select(
                        pclases.LoteCem.q.numlote == codigolote)[0]
                except IndexError:
                    try:
                        lote = pclases.LoteCem.select(
                            pclases.LoteCem.q.codigo == codigolote)[0]
                    except IndexError:
                        utils.dialogo_info(titulo = 'LOTE ERRÓNEO',
                            texto = 'El lote %s no se encontró.\nSeleccione '
                                    'otro o cree un lote nuevo.'%(codigolote),
                            padre = self.wids['ventana'])
                        return
            else:
                try:
                    codigolote = int(codigolote.replace("L-", ""))
                    lote = pclases.Lote.select(
                        pclases.Lote.q.numlote == codigolote)[0]
                except (IndexError, ValueError):
                    try:
                        lote = pclases.LoteCem.select(
                            pclases.LoteCem.q.codigo == codigolote)[0]
                    except IndexError:
                        utils.dialogo_info(titulo = 'LOTE ERRÓNEO',
                            texto = 'El lote %s no se encontró.\nSeleccione '
                                    'otro o cree un lote nuevo.'%(codigolote),
                            padre = self.wids['ventana'])
                        return
            if "C" in lote.codigo and self.producto.es_bigbag():
                fibracemento = True
            elif "C" not in lote.codigo and self.producto.es_bala():
                fibracemento = False
            else:
                utils.dialogo_info(titulo = "ERROR LOTE O PRODUCTO",
                                   texto = "El tipo de producto no concuerda "
                                           "con el lote seleccionado.",
                                   padre = self.wids['ventana'])
                return
            if ((self.usuario == None or self.usuario.nivel > 3)
                and (self.producto != None and self.producto.es_bala())
                and utils.get_puerto_serie() != None):
                self.iniciar_pesaje_auto(None)
            else:
                numbala, pedir_peso = self.pedir_numbala(
                                                fibracemento=fibracemento)
                if numbala == None:
                    return  # Ha cancelado el diálogo.
                for bala in numbala:
                    if pedir_peso:
                        peso = self.pedir_peso(bala, fibracemento=fibracemento)
                        if peso == None:
                            return # Ha cancelado el diálogo.
                    else:
                        peso = 0
                    #myprint("Voy a crear...")
                    self.crear_bala(bala, peso, lote,
                                    fibracemento=fibracemento)
                    #myprint("Creada...")
            self.save_conf_silos()
            self.rellenar_tabla_conf_silos()

    def ventana_peso(self, titulo, texto):
        ventana = gtk.Window()
        ventana.set_title(titulo)
        vbox = gtk.VBox(3)
        ltxt = gtk.Label(texto)
        e_peso = gtk.Entry()
        vbox.add(ltxt)
        vbox.add(e_peso)
        hbox = gtk.HBox(2)
        cancelar = gtk.Button(stock = gtk.STOCK_CANCEL)
        aceptar = gtk.Button(stock = gtk.STOCK_OK)
        vbox.add(hbox)
        hbox.add(cancelar)
        hbox.add(aceptar)
        ventana.add(vbox)
        def ok(b, ventana, peso):
            peso[0] = e_peso.get_text()
            ventana.destroy()
        def ko(b, ventana):
            ventana.destroy()
        peso = [None]
        aceptar.connect("clicked", ok, ventana, peso)
        cancelar.connect("clicked", ko, ventana)
        ventana.show_all()
        return peso[0]

    def pedir_peso(self, numbala, fibracemento = False):
        """
        Si el peso es incorrecto devuelve None. Devuelve el PESO BRUTO
        introducido por el usuario.
        """
        pesobala = None
        peso = utils.dialogo_entrada(titulo = 'PESO %s %d' % (fibracemento and "BIGBAG" or "BALA", numbala),
                                     texto = 'Introduzca el peso %s número %d: ' % (fibracemento and "del bigbag" or "de la bala", numbala),
                                     padre = self.wids['ventana'])
        if peso != None:
            try:
                pesobala = float(peso)
            except ValueError:
                utils.dialogo_info(titulo = 'PESO INCORRECTO',
                                   texto = 'El número introducido (%s) no es correcto.' % (peso),
                                   padre = self.wids['ventana'])
        return pesobala

    def dialogo_entrada_numbala(self,
                                texto= '',
                                titulo = 'ENTRADA DE DATOS',
                                valor_por_defecto = '',
                                padre=None,
                                pwd = False,
                                modal = True):
        """
        Muestra un diálogo modal con un textbox.
        Devuelve el texto introducido o None si se
        pulsó Cancelar.
        valor_por_defecto debe ser un string.
        Si pwd == True, es un diálogo para pedir contraseña
        y ocultará lo que se introduzca.
        """
        ## HACK: Los enteros son inmutables, usaré una lista
        res = [None]
        if modal:
            de = gtk.Dialog(titulo,
                            padre,
                            gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_OK, gtk.RESPONSE_OK,
                             gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        else:
            de = gtk.Dialog(titulo,
                            padre,
                            gtk.DIALOG_DESTROY_WITH_PARENT,
                            (gtk.STOCK_OK, gtk.RESPONSE_OK,
                             gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
        de.connect("response", utils.respuesta_ok_cancel, res)
        txt = gtk.Label(texto)
        de.vbox.pack_start(txt)
        txt.show()
        inpute = gtk.Entry()
        inpute.set_visibility(not pwd)
        def pasar_foco(widget, event):
            if event.keyval == 65293 or event.keyval == 65421:
                de.action_area.get_children()[1].grab_focus()
        inpute.connect("key_press_event", pasar_foco)
        de.vbox.pack_start(inpute)
        inpute.show()
        inpute.set_text(valor_por_defecto)
        ch_pedir_peso = gtk.CheckButton('Pedir pesos')
        ch_pedir_peso.set_active(True)
        ch_pedir_peso.show()
        de.vbox.pack_start(ch_pedir_peso)
        de.run()
        pedir_peso = ch_pedir_peso.get_active()
        de.destroy()
        if res[0]==False:
            return None, pedir_peso
        return res[0], pedir_peso

    def pedir_numbala(self, fibracemento = False):
        """
        Si se cancela o el número de bala es incorrecto, devuelve None.
        En otro caso devuelve un generador de números de bala dentro del
        rango introducido o el mismo generador pero con un único elemento
        si se ha tecleado un solo número de bala.
        """
        if fibracemento:
            try:
                numdefecto = str(pclases.Bigbag.select(
                    orderBy = "-numbigbag")[0].numbigbag + 1)
            except (AttributeError, IndexError):
                numdefecto = "1"
        else:
            try:
                numdefecto = str(pclases.Bala.select(
                    orderBy = "-numbala")[0].numbala + 1)
            except (AttributeError, IndexError):
                numdefecto = "1"
        numbala, pedir_peso = self.dialogo_entrada_numbala("Introduzca el número %s o un rango de números separados por guión: " % (fibracemento and "del bigbag" or "de la bala"),
                                                           'NÚMERO %s' % (fibracemento and "BIGBAG" or "BALA"),
                                                           padre = self.wids['ventana'],
                                                           valor_por_defecto = numdefecto)
        if numbala == None:
            return None, pedir_peso
        if '-' in numbala:
            try:
                ini, fin = map(int, numbala.split('-'))
            except:
                utils.dialogo_info(titulo = 'RANGO INCORRECTO', texto = 'El rango "%s" introducido no es correcto.' % numbala, padre = self.wids['ventana'])
                return None, pedir_peso
            if fin < ini:
                ini, fin = fin, ini
            if abs(fin - ini) > 100:
                if not utils.dialogo(titulo = '¿ESTÁ SEGURO?',
                                     texto = "Está a punto de añadir %d "
                                             "artículos al parte. ¿Está "
                                             "seguro de que esa cantidad es"
                                             " correcta?" % abs(fin-ini),
                                     padre = self.wids['ventana']):
                    return None, pedir_peso
        else:
            try:
                numbala = int(numbala)
            except ValueError:
                utils.dialogo_info(titulo='NÚMERO INCORRECTO',
                        texto='El número introducido (%s) no es correcto.' % (
                            numbala),
                        padre=self.wids['ventana'])
                return None, pedir_peso
            ini, fin = numbala, numbala
        return xrange(ini, fin+1), pedir_peso

    def crear_bala(self, numbala, peso, lote, fibracemento=False):
        """
        Recibe el **peso bruto** tecleado por el usuario.
        """
        if not MURANO:
            utils.dialogo_info(titulo="ERROR DE CONEXIÓN CON MURANO",
                           texto="No puede crear balas. Solo consultas.",
                   padre=self.wids['ventana'])
            return
        if fibracemento:
            articulo = self.crear_bigbag(numbala, peso, lote)
        else:
            codigo = 'B'+str(numbala)
            try:
                bala = pclases.Bala(lote=lote,
                                    partidaCarga=None,
                                    numbala=numbala,
                                    codigo=codigo,
                                    pesobala=peso-pclases.PESO_EMBALAJE_BALAS,
                                    claseb=False,
                                    motivo='',
                                    muestra=False)
                pclases.Auditoria.nuevo(bala, self.usuario, __file__)
            except:
                utils.dialogo_info(titulo = 'BALA NO CREADA',
                    texto = 'La bala no se pudo crear. Verifique que el '
                            'número %d no esté duplicado.' % numbala,
                    padre = self.wids['ventana'])
                return
            articulo = pclases.Articulo(bala=bala,
                            rollo=None,
                            bigbag=None,
                            parteDeProduccion=self.objeto,
                            productoVenta=self.producto,
                            albaranSalida=None,
                            almacen=pclases.Almacen.get_almacen_principal(),
                            pesoReal=peso)
            pclases.Auditoria.nuevo(articulo, self.usuario, __file__)
            self.logger.debug("Volcando bala %s a Murano..." % articulo.codigo)
            volcado_a_murano = murano.ops.create_articulo(articulo)
            self.logger.debug("Resultado del volcado: %s -> %s" % (
                articulo.codigo, volcado_a_murano))
        if articulo != None:
            self.descontar_material_adicional(articulo)
            self.actualizar_ventana()

    def crear_bigbag(self, numero, peso, lote):
        """
        Crea un bigbag con los datos recibidos y devuelve
        el artículo relacionado con el mismo.
        """
        if not MURANO:
            utils.dialogo_info(titulo="ERROR DE CONEXIÓN CON MURANO",
                               texto="No puede crear balas. Solo consultas.",
                               padre=self.wids['ventana'])
            return
        codigo = "C%d" % (numero)
        try:
            bigbag = pclases.Bigbag(loteCem = lote,
                                    numbigbag = numero,
                                    codigo = codigo,
                                    pesobigbag=peso-pclases.PESO_EMBALAJE_BIGBAGS,
                                    muestra = False,
                                    claseb = False,
                                    motivo = "")
            pclases.Auditoria.nuevo(bigbag, self.usuario, __file__)
        except:
            utils.dialogo_info(titulo = "BIGBAG NO CREADO",
                               texto = "El bigbag no se pudo crear. Verifique que el número %d no esté duplicado." % (numero),
                               padre = self.wids['ventana'])
            return None
        articulo = pclases.Articulo(bala = None,
                            rollo = None,
                            bigbag = bigbag,
                            parteDeProduccion = self.objeto,
                            productoVenta = self.producto,
                            albaranSalida = None,
                            almacen = pclases.Almacen.get_almacen_principal(),
                            pesoReal = peso)
        pclases.Auditoria.nuevo(articulo, self.usuario, __file__)
        murano.ops.create_articulo(articulo)
        return articulo

    def drop_bala(self, boton):
        if not MURANO:
            utils.dialogo_info(titulo="ERROR DE CONEXIÓN CON MURANO",
                           texto="No puede eliminar balas. Solo consultas.",
                   padre=self.wids['ventana'])
            return
        model, paths=self.wids['tv_balas'].get_selection().get_selected_rows()
        if paths == None or paths == []:
            utils.dialogo_info('BALA NO SELECCIONADA',
                               'Debe seleccionar la bala que desee eliminar '
                               'del parte.',
                               padre = self.wids['ventana'])
            return
        else:
            if not utils.dialogo('¿Eliminar del parte?',
                                 'BORRAR BALA DE CONTROL DE PRODUCCIÓN',
                                 padre = self.wids['ventana']):
                return
            for path in paths:
                codbala = model[path][1]
                if codbala == 0 or codbala == "": #El número de bala está vacío
                    utils.dialogo_info('BALA NO SELECCIONADA',
                                       'Debe seleccionar una bala.\nPara eliminar una incidencia use «Eliminar incidencia».',
                                       padre = self.wids['ventana'])
                else:
                    ide = model[path][-1]
                    articulo = pclases.Articulo.get(ide)
                    if articulo.albaranSalida != None or (articulo.es_bala() and articulo.bala.partidaCarga != None):
                        utils.dialogo_info(titulo = 'NO SE PUEDE ELIMINAR',
                                           texto = 'La fibra ya ha sido usada o vendida.\nNo se eliminará.',
                                           padre = self.wids['ventana'])
                    else:
                        try:
                            if articulo.es_bala():
                                es_bala = True
                                es_bigbag = False
                                bala = articulo.bala
                            elif articulo.es_bigbag():
                                es_bigbag = True
                                es_bala = False
                                bigbag = articulo.bigbag
                            else:
                                es_bigbag = False
                                es_bala = False
                            self.descontar_material_adicional(articulo, restar = False)
                            ret_murano = murano.ops.delete_articulo(articulo)
                            # TODO: Falta aumentar la granza al igual que se hace cuando se cambia el peso de una bala.
                            #articulo.bala = None
                            #articulo.bigbag = None
                            articulo.parteDeProduccion = None
                            articulo.destroy(ventana = __file__)
                            if es_bala:
                                bala.destroy(ventana = __file__)
                            if es_bigbag:
                                bigbag.destroy(ventana = __file__)
                        except ZeroDivisionError:
                            utils.dialogo_info(titulo = 'ERROR', texto = 'Ocurrió un error. No se pudo eliminar completamente.\nAnote el número de bala (%s) y contacte con el administrador de la aplicación\npara subsanar la inconsistencia.' % (bala and bala.codigo or "no disponible"), padre = self.wids['ventana'])
                            # bala.parteDeProduccion = self.objeto
                            try:
                                articulo.sync()    # Si no salta la excepción, aún existe.
                                if es_bala:
                                    articulo.bala = bala
                                if es_bigbag:
                                    articulo.bigbag = bigbag
                                self.descontar_material_adicional(articulo, restar = True)
                                if ret_murano:
                                    murano.ops.create_articulo(articulo)
                            except pclases.SQLObjectNotFound:
                                pass
                            except AttributeError:  # Existe el artículo pero ya no tiene bala
                                self.logger.error("El artículo ID %s ya no tiene bala, no se ha podido sumar el material empleado al borrarlo y tampoco se pudo eliminar el artículo en sí." % articulo.id, padre = self.wids['ventana'])
            self.actualizar_ventana()


    def add_incidencia(self, boton):
        ii = pclases.TipoDeIncidencia.select()
        idincidencia = utils.dialogo_combo(
            'SELECCIONE UN TIPO DE INCIDENCIA',
            'Seleccine un tipo de incidencia del desplegable inferior',
            [(i.id, i.descripcion) for i in ii],
            padre = self.wids['ventana'])
        if idincidencia == None:
            return
        utils.dialogo_info('HORA INICIO',
            'A continuación seleccione la hora de inicio de la incidencia.',
            padre = self.wids['ventana'])
        horaini = utils.mostrar_hora(time.localtime()[3],
                                     time.localtime()[4],
                                     0,
                                     'HORA INICIO')
        if not horaini:
            return
        utils.dialogo_info('HORA FIN',
            'A continuación seleccione la hora de finalización de la'
            ' incidencia.',
            padre = self.wids['ventana'])
        horafin = utils.mostrar_hora(time.localtime()[3],
                                     time.localtime()[4],
                                     0,
                                     'HORA FIN')
        if not horafin:
            return
        self.objeto.sync()
        horaini = mx.DateTime.DateTimeFrom(day = self.objeto.fecha.day,
                                           month = self.objeto.fecha.month,
                                           year = self.objeto.fecha.year,
                                           hour  = int(horaini.split(":")[0]),
                                           minute = int(horaini.split(":")[1]),
                                           second = 0)
        horafin = mx.DateTime.DateTimeFrom(day = self.objeto.fecha.day,
                                           month = self.objeto.fecha.month,
                                           year = self.objeto.fecha.year,
                                           hour  = int(horafin.split(":")[0]),
                                           minute = int(horafin.split(":")[1]),
                                           second = 0)
        if horaini > horafin:
            horafin = horafin + mx.DateTime.oneDay
        while horaini < self.objeto.fechahorainicio:   # El parte está en la
            # franja de medianoche y la incidencia comienza después de las 12.
            horaini += mx.DateTime.oneDay   # Debe llevar la fecha del día
                                            # siguiente.
            horafin += mx.DateTime.oneDay
        if entran_en_turno(self.objeto, horaini, horafin):
            observaciones = utils.dialogo_entrada(titulo = 'OBSERVACIONES',
                texto = 'Introduzca observaciones sobre la incidencia:',
                padre = self.wids['ventana'])
            if observaciones == None:
                return
            incidencia = pclases.Incidencia(
                tipoDeIncidencia = pclases.TipoDeIncidencia.get(idincidencia),
                horainicio = horaini,
                horafin = horafin,
                parteDeProduccion = self.objeto,
                observaciones = observaciones)
            pclases.Auditoria.nuevo(incidencia, self.usuario, __file__)
            if incidencia.horainicio > incidencia.horafin:
                incidencia.horainicio, incidencia.horafin = incidencia.horafin, incidencia.horainicio
            self.actualizar_ventana()
        else:
            utils.dialogo_info(titulo = 'ERROR HORARIO',
                texto = 'La franja horaria que ha seleccionado no entra en '
                        'el turno del parte.',
                padre = self.wids['ventana'])

    def drop_incidencia(self, boton):
        model, paths = self.wids['tv_balas'].get_selection().get_selected_rows()
        if paths == None or paths == []:
            utils.dialogo_info('INCIDENCIA NO SELECCIONADA', 'Debe seleccionar la incidencia que desee eliminar del parte.', padre = self.wids['ventana'])
        else:
            if not utils.dialogo('¿Eliminar del parte?', 'BORRAR INCIDENCIA DE CONTROL DE PRODUCCIÓN', padre = self.wids['ventana']):
                return
            for path in paths:
                ide = model[path][-1]
                if model[path][1] != '':    # El número de bala NO está vacío
                    utils.dialogo_info('BALA SELECCIONADA', 'Ha seleccionado una bala en lugar de una incidencia.\nUse «Quitar bala» para eliminarla.', padre = self.wids['ventana'])
                else:
                    incidencia = pclases.Incidencia.get(ide)
                    incidencia.parteDeProduccion = None
                    try:
                        incidencia.destroy(ventana = __file__)
                    except:
                        utils.dialogo_info(titulo = 'INCIDENCIA NO ELIMINADA', texto = 'Ocurrió un error al intentar eliminar la incidencia.', padre = self.wids['ventana'])
            self.actualizar_ventana()

    def add_empleado(self, w):
        empleados = pclases.Empleado.select(
                pclases.AND(pclases.Empleado.q.activo == True,
                            pclases.Empleado.q.planta == True),
                orderBy='apellidos')
        empleados = [(e.id, e.nombre, e.apellidos) for e in empleados \
                     if e.planta and \
                        e.activo and \
                        e.categoriaLaboral and \
                        e.categoriaLaboral.planta]
                        # e.categoriaLaboral.planta and \
                        # e.categoriaLaboral.lineaDeProduccion == self.linea]
        ids = utils.dialogo_resultado(filas = empleados,
                                      titulo = 'SELECCIONE EMPLEADOS',
                                      cabeceras = ('ID', 'Nombre', 'Apellidos'),
                                      multi = True,
                                      padre = self.wids['ventana'])
        if ids == [-1]:
            return
        for ide in ids:
            try:
                e = pclases.Empleado.get(ide)
                self.objeto.addEmpleado(e)
            except:
                utils.dialogo_info(titulo = 'NÚMERO INCORRECTO',
                                   texto = 'El empleado con código identificador %d no existe o no se pudo agregar.' % ide,
                                   padre = self.wids['ventana'])
        self.rellenar_tabla_empleados()

    def drop_empleado(self, w):
        if self.wids['tv_empleados'].get_selection().count_selected_rows() == 0:
            return
        model, path = self.wids['tv_empleados'].get_selection().get_selected()
        ide = model[path][0] # El ide de empleado es la columna 0
        e = pclases.Empleado.get(ide)
        self.objeto.removeEmpleado(e)
        self.rellenar_tabla_empleados()

    def rellenar_tabla_empleados(self):
        model = self.wids['tv_empleados'].get_model()
        model.clear()
        horas_parte = self.objeto.get_duracion()
        for ht in self.objeto.horasTrabajadas:
            try:
                supera_duracion_parte = ht.horas > horas_parte
            except TypeError:
                supera_duracion_parte = (
                    utils.DateTime2DateTimeDelta(ht.horas) > horas_parte)
            if supera_duracion_parte:
                ht.horas = horas_parte.strftime('%H:%M')
                ht.sync()
            model.append((ht.empleado.id,
                          ht.empleado.nombre,
                          ht.empleado.apellidos,
                          ht.horas.strftime('%H:%M'), ht.id))

    def cambiar_lote(self, w):
        """
        Pide un número de lote por teclado y cambia a él.
        """
        texto = """
        Al cambiar el lote del parte, se cambiará el lote de
        todos los productos relacionados con él. Si quiere
        comenzar la producción de un nuevo lote sin afectar
        a los ya existentes, cree un nuevo parte.

        ¿Desea cambiar el lote actual?
        """
        if (self.objeto.articulos != []
            and not utils.dialogo(titulo = '¿ESTÁ SEGURO?',
                                  texto = texto,
                                  padre = self.wids['ventana'])):
            return
        numlote = utils.dialogo_entrada(titulo = '¿NÚMERO DE LOTE?',
            texto = 'Introduzca el número o código de lote:\n\nTenga en '
                    'cuenta que los productos almacenados en \nbigbags '
                    'pertenecen a lotes que comienzan por "C-".',
            padre = self.wids['ventana'])
        if numlote == None:
            return      # Canceló
        try:
            numlote = int(numlote)
        except TypeError:
            return      # Si le dan a cancelar se manda None
        except ValueError:      # No ha tecleado un número, busco por código.
            numlote = numlote
        # Obtengo el código del número de lote. Si es un entero, el lote es el
        # string del entero y no es de fibra de cemento.
        # Si no es un entero, el numlote es un código de lote en formato
        # cadena y será tal cual si es fibra de polipropileno y
        # C-001 si es fibra de cemento.
        if isinstance(numlote, type(1)):
            codigo = str(numlote)
        else:
            numlote = numlote.upper()
            if "C" in numlote:
                numlote = numlote.replace("C", "").replace("-", "")
                try:
                    numlote = "C-%03d" % (int(numlote))
                except TypeError:
                    utils.dialogo_info(titulo = "ERROR NÚMERO DE LOTE",
                            texto = "El texto %s no es un número de lote "
                                    "correcto." % (numlote),
                            padre = self.wids['ventana'])
                    return
            codigo = numlote
        try:
            codigo = int(codigo.replace("L-", ""))
            lote = pclases.Lote.select(pclases.Lote.q.numlote == codigo)[0]
            self.wids['e_numlote'].set_text(lote.codigo)
        except (IndexError, ValueError):
            try:
                # OJO: codigo es str, aunque venga de numlote, que a pesar del
                # nombre, también es un string (¡vergüensa de tus hijoh!)
                if not isinstance(codigo, str):
                    codigo = str(codigo)
                lote = pclases.LoteCem.select(
                    pclases.LoteCem.q.codigo == codigo)[0]
                self.wids['e_numlote'].set_text(lote.codigo)
            except IndexError:
                if not utils.dialogo(titulo='¿CREAR LOTE?',
                                     texto='No se encontró el lote %s.\n¿Desea crear uno nuevo?' % (codigo),
                                     padre = self.wids['ventana']):
                    return
                else:
                    lote = self.nuevo_lote(codigo)
        if lote != None:
            col = self.wids['tv_balas'].get_column(1)
            if isinstance(lote, pclases.LoteCem):
                col.set_title("Nº Bigbag")
                self.wids['b_add_bala'].set_label("Añadir bigbag")
                self.wids['b_drop_bala'].set_label("Eliminar bigbag")
            elif isinstance(lote, pclases.Lote):
                col.set_title("Nº Bala")
                self.wids['b_add_bala'].set_label("Añadir bala")
                self.wids['b_drop_bala'].set_label("Eliminar bala")
            else:
                col.set_title("?")
            self.wids['e_numlote'].set_text(lote.codigo)
            self.rellenar_datos_lote()
            for a in self.objeto.articulos:
                if a.es_bala():
                    a.bala.lote = lote
                elif a.es_bigbag():
                    a.bigbag.loteCem = lote

    def nuevo_lote(self, codigo):
        if not isinstance(codigo, str):
            #codigo = `codigo`
            codigo = str(codigo)
        if "C-" in codigo:
            try:
                numlote = int(codigo.replace("C-", ""))
            except ValueError:
                utils.dialogo_info(titulo = "LOTE NO SE PUDO CREAR",
                                   texto = "El lote de fibra de cemento %s no se puede crear." % (codigo),
                                   padre = self.wids['ventana'])
            else:
                if self.producto != None and not self.producto.es_bigbag():
                    utils.dialogo_info(titulo = "NO PUEDE CAMBIAR DE LOTE",
                                       texto = "No puede cambiar a un lote de fibra de cemento\nsi lo que está produciendo (%s)\nno es fibra de cemento." % (self.producto.descripcion),
                                       padre = self.wids['ventana'])
                    return None
                lote = pclases.LoteCem(codigo = codigo,
                                       numlote = numlote,
                                       tenacidad = None,
                                       elongacion = None,
                                       encogimiento = None,
                                       grasa = None,
                                       tolerancia = 0.4,
                                       humedad = None,
                                       mediatitulo = 0.0)
                pclases.Auditoria.nuevo(lote, self.usuario, __file__)
        else:
            codigo = codigo.upper()
            if "L-" not in codigo:
                codigo = "L-" + codigo.replace("L", "")
            try:
                numlote = int(codigo.replace("L-", ""))
            except ValueError:
                utils.dialogo_info(titulo = "LOTE NO SE PUDO CREAR",
                                   texto = "El lote %s no se puede crear." % (codigo),
                                   padre = self.wids['ventana'])
            else:
                if self.producto != None and not self.producto.es_bala():
                    utils.dialogo_info(titulo = "NO PUEDE CAMBIAR DE LOTE",
                                       texto = "No puede cambiar a un lote de fibra PP\nsi lo que está produciendo (%s)\nes fibra de cemento." % (self.producto.descripcion),
                                       padre = self.wids['ventana'])
                    return None
                lote = pclases.Lote(numlote = numlote, codigo = codigo)
                pclases.Auditoria.nuevo(lote, self.usuario, __file__)
        for a in self.objeto.articulos:
            if a.es_bala():
                a.bala.lote = lote
            elif a.es_bigbag():
                a.bigbag.loteCem = lote
        # self.wids['e_numlote'].set_text(lote.codigo)
        return lote

    def rellenar_filtros(self):
        model = self.wids['tv_filtros'].get_model()
        model.clear()
        cantidad = 0
        for consumo in [c for c in self.objeto.consumos
                        if c.antes == -1 and c.despues == -1]:
            model.append((consumo.productoCompra.descripcion,
                          consumo.cantidad, consumo.id))
            cantidad += consumo.cantidad
        self.wids['e_total_filtros'].set_text(str(cantidad))

    def rellenar_granza(self):
        model = self.wids['tv_granza'].get_model()
        model.clear()
        cantidad = 0
        for consumo in [c for c in self.objeto.consumos
                        if (c.antes != -1 and c.despues != -1)
                           and (c.antes != -2 and c.despues != -2)]:
            model.append((consumo.productoCompra.descripcion,
                          consumo.antes,
                          consumo.despues,
                          consumo.cantidad,
                          consumo.id))
            cantidad += consumo.cantidad
        self.wids['e_total_granza'].set_text(utils.float2str(cantidad))

    def actualizar_consumo(self, consumo, descontar):
        """
        Pone el campo actualizado del consumo a True y
        descuenta la cantidad del producto de compra.
        """
        consumo.actualizado = descontar
        if descontar:
            consumo.productoCompra.existencias -= consumo.cantidad
            consumo.productoCompra.add_existencias(-consumo.cantidad)
        else:
            consumo.productoCompra.existencias += consumo.cantidad
            consumo.productoCompra.add_existencias(consumo.cantidad)

    def buscar_producto_compra(self, defecto = "",
                               titulo_defecto = "BUSCAR PRODUCTO"):
        a_buscar = utils.dialogo_entrada(titulo = titulo_defecto,
                    texto = 'Introduzca código o descripción del producto:',
                    valor_por_defecto = defecto,
                    padre = self.wids['ventana'])
        if a_buscar == None:
            return None
        productos = pclases.ProductoCompra.select(pclases.AND(
            pclases.OR(pclases.ProductoCompra.q.descripcion.contains(a_buscar),
                       pclases.ProductoCompra.q.codigo.contains(a_buscar)),
            pclases.ProductoCompra.q.controlExistencias == True,
            pclases.ProductoCompra.q.obsoleto == False,
            pclases.ProductoCompra.q.existencias > 0))
        if productos.count() == 0:
            utils.dialogo_info(titulo = 'PRODUCTO NO ENCONTRADO',
                        texto = 'Producto no encontrado o sin existencias.',
                        padre = self.wids['ventana'])
            return None
        elif productos.count() > 1:
            filas = [(p.id, p.codigo, p.descripcion, p.existencias)
                     for p in productos]
            idproducto = utils.dialogo_resultado(filas,
                    'SELECCIONE PRODUCTO',
                    cabeceras = ['ID', 'Código', 'Descripción', 'Existencias'],
                    padre = self.wids['ventana'])
            if idproducto > 0:
                productos = [pclases.ProductoCompra.get(idproducto)]
            else:
                return None
        producto = productos[0]
        return producto

    def add_granza(self, w):
        producto = self.buscar_producto_compra("GRANZA")
        if producto == None:
            return
        cantidad = utils.dialogo_entrada(titulo = 'CANTIDAD',
            texto = 'Introduzca la cantidad que había en el silo antes de '
                    'comenzar el parte de producción:',
            padre = self.wids['ventana'])
        if cantidad == None:
            return
        try:
            cantidad = float(cantidad)
        except ValueError:
            utils.dialogo_info('Cantidad incorrecta')
            return
        if cantidad > producto.existencias:
            utils.dialogo_info(titulo = 'CANTIDAD INSUFICIENTE',
                               texto = 'No hay existencias suficientes en almacén.\nVerifique que ha tecleado la cantidad correctamente\ny que las entradas en almacén del producto han sido contabilizadas.')
            return
        consumo = pclases.Consumo(antes = cantidad,
                                  despues = cantidad,
                                  cantidad = 0,
                                  actualizado = False,
                                  parteDeProduccion = self.objeto,
                                  productoCompra = producto)
        pclases.Auditoria.nuevo(consumo, self.usuario, __file__)
        # self.actualizar_consumo(consumo, True)
        self.objeto.unificar_consumos()
        self.rellenar_granza()

    def drop_granza(self, w):
        model, itr = self.wids['tv_granza'].get_selection().get_selected()
        if itr == None:
            return
        idconsumo = model[itr][-1]
        consumo = [c for c in self.objeto.consumos if c.id == idconsumo][0]
        self.actualizar_consumo(consumo, False)
        consumo.parteDeProduccion = None
        consumo.destroy(ventana = __file__)
        self.rellenar_granza()

    # XXX vvv
    def button_clicked(self, lista, event):
        if event.button == 3:
            ui_string = """<ui>
                            <popup name='Popup'>
                                <menuitem action='Enviar muestra'/>
                                <menuitem action='Limpiar marca muestra'/>
                            </popup>
                           </ui>"""
            ag = gtk.ActionGroup('WindowActions')
            actions = [('Enviar muestra', gtk.STOCK_COLOR_PICKER, '_Enviar muestra', '<control>E',
                        'Envia una muestra del lote o partida correspondiente al parte a laboratorio',
                        self.enviar_a_laboratorio),
                       ('Limpiar marca muestra', gtk.STOCK_CLEAR, '_Limpiar la marca de muestra de la bala', '<control>l',
                        'Elimina únicamente la marca de muestra. No cancela las muestras ya enviadas.',
                        self.limpiar_marcas)]
            ag.add_actions(actions)
            ui = gtk.UIManager()    #gtk.UI_MANAGER_POPUP
            ui.insert_action_group(ag, 0)
            ui.add_ui_from_string(ui_string)
            widget = ui.get_widget("/Popup")
            widget.popup(None, None, None, event.button, event.time)

    def limpiar_marcas(self, parametro):
        """
        Marca el rollo seleccionado como defectuoso.
        """
        parte = self.objeto
        if not parte.articulos:
            utils.dialogo_info(titulo = "PARTE VACÍO", texto = "En el parte seleccionado no hubo producción.", padre = self.wids['ventana'])
        else:
            model, paths = self.wids['tv_balas'].get_selection().get_selected_rows()
            for path in paths:
                if model[path][1] != '':    # Nº bala o bigbag. Tiene, no es una incidencia.
                    ide = model[path][-1]
                    articulo = pclases.Articulo.get(ide)
                    if articulo.es_bala():
                        bala_o_bb = articulo.bala
                    elif articulo.es_bigbag():
                        bala_o_bb = articulo.bigbag
                    if bala_o_bb.muestra:       # Si no tiene muestra no quiero limpiarle las observaciones.
                        bala_o_bb.muestra = False
                        bala_o_bb.motivo = ''
                        model[path][-2] = bala_o_bb.motivo

    def enviar_a_laboratorio(self, parametro):
        # NOTA: Ni idea de qué es lo que traerá el parámetro, sólo me interesa
        # el parte que está seleccionado en el treeview.
        parte = self.objeto
        if not parte.articulos:
            utils.dialogo_info(titulo = "PARTE VACÍO", texto = "En el parte seleccionado no hubo producción.")
        else:
            a = parte.articulos[0]  # Al menos tiene 1 artículo. Con el primero me vale.
            if a.es_bala():
                lote = a.bala.lote
                partida = None
            elif a.es_bigbag():
                lote = a.bigbag.lote
                partida = None
            elif a.es_rollo():
                lote = None
                partida = a.rollo.partida
            else:
                lote = None
                partida = None
            codigo = self.crear_muestra(lote, partida)
            if codigo != '':
                model, paths = self.wids['tv_balas'].get_selection().get_selected_rows()
                for path in paths:
                    if model[path][1] != '':    # Nº bala o bigbag, tiene, no es una incidencia.
                        ide = model[path][-1]
                        articulo = pclases.Articulo.get(ide)
                        if articulo.es_bala():
                            bala_o_bb = articulo.bala
                        elif articulo.es_bigbag():
                            bala_o_bb = articulo.bigbag
                        bala_o_bb.muestra = True
                        bala_o_bb.motivo += '>>> Muestra %s' % codigo
                        model[path][-2] += '>>> Muestra %s' % codigo

    def crear_muestra(self, lote, partida):
        _codigo = ['']
        dialogo = gtk.Dialog("DATOS DE LA MUESTRA",
                             self.wids['ventana'],
                             gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                             (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                              gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
        dialogo.connect("response", self.crear_muestra_ok_cancel, lote, partida, _codigo)
        texto = """
        Introduzca, si lo desea, los datos para la muestra
        de%s número %d.
        """ % (partida and " la partida" or "l lote",
               partida and partida.numpartida or lote.numlote)
        txt = gtk.Label(texto)
        dialogo.vbox.pack_start(txt)
        dialogo.vbox.pack_start(gtk.Label("\nCódigo de muestra:"))
        codigo = gtk.Entry()
        codigo.set_text("M(%s)" % (partida and partida.codigo or lote.codigo))
        dialogo.vbox.pack_start(codigo)
        dialogo.vbox.pack_start(gtk.Label("\nObservaciones:"))
        observaciones = gtk.Entry()
        dialogo.vbox.pack_start(observaciones)
        dialogo.vbox.show_all()
        dialogo.run()
        dialogo.destroy()
        return _codigo[0]

    def crear_muestra_ok_cancel(self, dialogo, respuesta, lote, partida, _codigo):
        if respuesta == gtk.RESPONSE_ACCEPT:
            codigo = dialogo.vbox.get_children()[2].get_text()
            observaciones = dialogo.vbox.get_children()[4].get_text()
            m = pclases.Muestra(lote = lote,
                                partida = partida,
                                codigo = codigo,
                                observaciones = observaciones,
                                pendiente = True,
                                envio = mx.DateTime.localtime(),
                                recepcion = None,
                                loteCem = None)
            pclases.Auditoria.nuevo(m, self.usuario, __file__)
            _codigo[0] = codigo
            if utils.dialogo(titulo = "MUESTRA ENVIADA",
                             texto = "Muestra creada, enviada y pendiente para su análisis en laboratorio.\n¿Desea enviar una alerta?",
                             padre = self.wids['ventana']):
                usuarios = [(u.id, u.usuario)
                        for u in pclases.Usuario.select(orderBy = 'usuario')]
                usuario = utils.dialogo_combo(titulo = "SELECCIONE USUARIO",
                                              texto = "Seleccione del desplegable inferior al usuario que quiere alertar acerca de la muestra.",
                                              ops = usuarios,
                                              padre = self.wids['ventana'])
                if usuario != None:
                    user = pclases.Usuario.get(usuario)
                    if m.codigo:
                        msj = "La muestra %s está " % m.codigo
                    else:
                        msj = "Tiene una muestra "
                    msj += "pendiente de analizar."
                    user.enviar_mensaje(msj)
    # XXX ^^^

    def bloquear(self, ch, mostrar_alerta = True):
        # Si el parte tiene menos de un día y se encuentra bloqueado, dejo que lo pueda desbloquear cualquiera.
        if mx.DateTime.localtime() - self.objeto.fecha <= mx.DateTime.oneDay and (self.objeto.bloqueado or ch.get_active()):
            self.objeto.bloqueado = False
        elif ch.get_active() != self.objeto.bloqueado:
            # NEW!: Los partes bloqueados solo los pueden desbloquear usuarios con nivel <= 1.
            if self.objeto.bloqueado:
                if self.usuario and self.usuario.nivel <= 2: # and self.objeto.bloqueado and not ch.get_active():
                    self.objeto.bloqueado = False
            else:
                if "w" in self.__permisos:  # Tiene permiso para bloquear el parte
                    self.objeto.bloqueado = True
                else:
                    if mostrar_alerta:
                        utils.dialogo_info(titulo = "USUARIO SIN PRIVILEGIOS",
                                           texto = "No tiene permisos suficientes para bloquear y verificar partes de producción.",
                                           padre = self.wids['ventana'])
        self.objeto.sync()
        self.objeto.make_swap()
        ch.set_active(self.objeto.bloqueado)

    def imprimir(self, boton):
        self.guardar(None)
        parte = self.objeto
        ws = ('e_fecha', 'e_dtex', 'e_numlote', 'e_articulo', 'e_longitud', 'e_hora_ini', 'e_hora_fin', 'e_o80', 'e_num_balas', 'e_peso_total', 'e_tiempo_real_trabajado', 'e_productividad', 'e_numA', 'e_pesoA', 'e_numB', 'e_pesoB')
        datos = {}
        for w in ws:
            datos[w] = self.wids[w].get_text()
        empleados = []
        for h in parte.horasTrabajadas:
            empleados.append(h.empleado)
        datos['empleados'] = empleados

        bounds = self.wids['txt_observaciones'].get_buffer().get_bounds()
        datos['observaciones'] = self.wids['txt_observaciones'].get_buffer().get_text(bounds[0], bounds[1]).replace("º", "o.")

        detallesdeproduccion = [i for i in self.objeto.incidencias] + [a for a in self.objeto.articulos]
            # El + sin más, hace un join, así que no tengo más remedio que recorrer las listas.
        detallesdeproduccion.sort(self.cmpfechahora)
        lineas = []
        for detalle in detallesdeproduccion:
            obs = self.observaciones(detalle)
            if len(obs) > 25:
                obs = obs[:25]+'...'
            lineas.append((self.bala(detalle),
                           self.peso(detalle),
                           self.motivo(detalle),
                           self.horaini(detalle),
                           self.horafin(detalle),
                           self.duracion(detalle),
                           obs,
                           self.claseb(detalle)))
        # reports.abrir_pdf(geninformes.parteBalas(datos, lineas))
        reports.imprimir_con_gs(geninformes.parteBalas(datos, lineas),
                                 impresora = "OFICINA",
                                 blanco_y_negro = True)

    def consumir_segun_formulacion(self, producto, articulo, restar):
        """
        Realiza los consumos según la formulación de la línea de producción.
        Devuelve el peso de los aditivos (productos consumidos que componen
        la fibra y no son granza -ensimajes, antiuvi, colorantes...-.
        """
        aditivos = 0
        for consumoAdicional in producto.consumosAdicionales:
            caprod = consumoAdicional.productoCompra
            if caprod and caprod.obsoleto:
                continue
            consumido = consumoAdicional.consumir(articulo,
                                                  cancelar = not restar)
            # OJO: Para el cálculo de aditivos los nombres en la formulación
            # deben ser exactamente estos:
            if consumoAdicional.nombre.lower() == "antiuvi" or \
               consumoAdicional.nombre.lower() == "ensimaje" or \
               consumoAdicional.nombre.lower() == "negro":
                aditivos += consumido
            self.logger.warning("CONSUMO LÍNEA FIBRA: "
                "Consumiendo %s de %s para la bala o bigbag %s" % (
                    utils.float2str(consumido),
                    consumoAdicional.productoCompra.descripcion,
                    articulo.codigo_interno))
        # Ahora el consumo de granza: Por cada kilo de fibra - aditivos,
        # 1 kilo de granza.
        aditivos = abs(aditivos)
        return aditivos

    def consumir_granza_silos(self, articulo, aditivos, restar):
        """
        Descarga de los silos la cantidad de fibra producida sin aditivos en
        la proporción indicada en el parte.
        """
        for silo in [s for s in pclases.Silo.select()
                     if self.wids['ch_silo_ID%d' % (s.id)].get_active()]:
            peso_sin_aditivos = articulo.peso - aditivos
            porcentaje = self.wids['escala_ID%d' % (silo.id)].get_value() / 100
            if restar:
                if pclases.DEBUG:
                    myprint(__file__, " -> Intentando consumo silos...")
                diccionario_consumido = silo.consumir(peso_sin_aditivos * porcentaje, parte_de_produccion = self.objeto)
                if pclases.DEBUG:
                    myprint(__file__, " -> ", diccionario_consumido)
                consumido = sum([diccionario_consumido[p] for p in diccionario_consumido])
                if pclases.DEBUG:
                    myprint(__file__, " -> ", articulo.peso, aditivos,
                            peso_sin_aditivos, porcentaje)
                try:
                    ocupado = murano.ops.get_ocupado_silo(silo)
                except:
                    self.logger.error(
                        "No se pudo leer Silo en Murano. Fallback a ginn.")
                    ocupado = silo.ocupado
                self.logger.warning("CONSUMO LÍNEA FIBRA: Consumiendo %s de "
                        "granza del silo %s para la bala o bigbag %s. "
                        "Ocupado: %s" % (utils.float2str(consumido),
                                         silo.nombre,
                                         articulo.codigo_interno,
                                         utils.float2str(ocupado)))
                if pclases.DEBUG:
                    myprint(__file__, " -> ", diccionario_consumido)
            else:
                # No hay que cargar el silo. ¡SOLO HAY QUE ANULAR EL CONSUMO!
                try:
                    carga_mas_baja_en_silo = murano.ops.get_carga_mas_antigua_silo(silo)
                except:
                    self.logger.error(
                        "Error al leer silos de Murano. Fallback a ginn.")
                    carga_mas_baja_en_silo = silo.get_carga_mas_antigua()
                if carga_mas_baja_en_silo != None:
                    producto_consumido = carga_mas_baja_en_silo.productoCompra
                    cargado = peso_sin_aditivos * porcentaje
                    consumo = pclases.Consumo(silo = silo,
                            parteDeProduccionID = self.objeto.id,
                            productoCompra = producto_consumido,
                            actualizado = True,
                            antes = producto_consumido.existencias,
                            despues = producto_consumido.existencias + cargado,
                            cantidad = -cargado)
                    pclases.Auditoria.nuevo(consumo, self.usuario, __file__)
                    try:
                        ocupado = murano.ops.get_ocupado_silo(silo)
                    except:
                        self.logger.error(
                            "No se pudo leer Silo en Murano. Fallback a ginn.")
                        ocupado = silo.ocupado
                    self.logger.warning("CONSUMO LÍNEA FIBRA: "
                            "%s anulado de silo %s. Ocupado: %s" % (
                                utils.float2str(cargado),
                                silo.nombre,
                                ocupado))
                else:
                    utils.dialogo_info(titulo = "ERROR EN SILO",
                            texto = "No se pudo determinar el producto "
                                    "consumido del silo para la bala o "
                                    "bigbag %s.\nDebe ajustar el silo "
                                    "manualmente." % (articulo.codigo_interno),
                            padre = self.wids['ventana'])
            mostrar_carga_silo(self.wids['l_ID%d' % (silo.id)], silo)

    def consumir_granza_reciclada(self, articulo, aditivos, restar):
        """
        Descuenta de las existencias de almacén la proporción de granza
        consumida en función de lo indicado en el parte y el peso de la
        bala sin aditivos.
        """
        # OJO: No compruebo que la granza tenga existencias positivas. (Tampoco
        # estoy seguro de querer hacerlo. Aquí se hace mucho el gato.)
        # OJO: Número de silos de reciclada HARCODED (empiezo a darme asca con
        # tanto harcoded).
        for numreciclada in (0, 1):
            if self.wids['ch_reciclada_%d' % (numreciclada)].get_active():
                peso_sin_aditivos = articulo.peso - aditivos
                porcentaje = self.wids[
                        's_reciclada_%d' % (numreciclada)].get_value() / 100.0
                if restar:
                    cantidad_a_consumir = peso_sin_aditivos * porcentaje
                else:
                    cantidad_a_consumir = -peso_sin_aditivos * porcentaje
                idgranza = utils.combo_get_value(
                        self.wids["cbe_reciclada_%d" % (numreciclada)])
                if idgranza > 0:
                    granza = pclases.ProductoCompra.get(idgranza)
                    consumo = pclases.Consumo(silo=None,
                            parteDeProduccion=self.objeto,
                            productoCompra=granza,
                            actualizado=True,
                            antes=granza.existencias,
                            despues=granza.existencias - cantidad_a_consumir,
                            cantidad=cantidad_a_consumir)
                    pclases.Auditoria.nuevo(consumo, self.usuario, __file__)
                    granza.existencias -= cantidad_a_consumir
                    granza.syncUpdate()
                    granza.add_existencias(-cantidad_a_consumir)
                    self.logger.warning("CONSUMO LÍNEA FIBRA: Consumiendo %s"
                        " kg de granza reciclada (%s) para la bala o bigbag "
                        "%s. Queda en almacén: %s %s" % (
                            utils.float2str(cantidad_a_consumir),
                            granza.descripcion,
                            articulo.codigo_interno,
                            utils.float2str(granza.existencias),
                            granza.unidad))

    def descontar_material_adicional(self, articulo, restar = True):
        """
        Descuenta el material adicional correspondiente al artículo según
        la formulación que indique la línea de fabricación.
        Si "restar" es True, descuenta. Si es False, añade la cantidad (para
        cuando se elimine un rollo del parte, por ejemplo).
        Si es necesario, se dejará material con existencias en negativo, aunque
        se avisará al usuario de la incidencia.
        """
        # XXX: Caso especial para reenvasado de bigbags: 27 de marzo de 2007.
        if self.objeto.es_parte_de_reenvasado():
            self.logger.warning("%spartes_de_fabricacion_balas::descontar_material_adicional -> Reenvasando bulto %s. Se ignora el consumo de material. Será necesario descontar después la fibra reenvasada manualmente del almacén." % (self.usuario and self.usuario.usuario + ": " or "", articulo.codigo))
        else:
        # XXX
            producto = articulo.productoVenta
            aditivos = self.consumir_segun_formulacion(producto, articulo,
                                                       restar)
            self.consumir_granza_silos(articulo, aditivos, restar)
            self.consumir_granza_reciclada(articulo, aditivos, restar)
            self.objeto.unificar_consumos()

    def etiquetas(self, boton):
        """
        Imprime las etiquetas de los
        balas del parte seleccionados
        """
        entrada = utils.dialogo_entrada(titulo='ETIQUETAS',
                                        texto='Introduzca el número de bala o el rango (usando el \'-\') que desea etiquetar',
                                        padre = self.wids['ventana'])
        if entrada != None:
            if '-' in entrada:
                rango = entrada.split('-')
                try:
                    a = int(rango[0])
                    b = int(rango[1])
                    if a <= b:
                        b += 1
                    else:
                        aux = a
                        a = b
                        b = aux+1
                except:
                    utils.dialogo_info(titulo='ERROR', texto='Los números de balas introducidos no son válidos', padre = self.wids['ventana'])
                    return
                valido = True
                for i in range(a, b):
                    if not self.objeto.balaEnParte(i):
                        valido = False
                        break
                if not valido:
                    utils.dialogo_info(titulo='ERROR', texto='El número de bala %d introducido no pertece al parte.\nCompruébelo y vuelva a intentarlo.' % i, padre = self.wids['ventana'])
                    return
                temp = []
                for i in range(a, b):
                    temp.append(pclases.Bala.select(
                        pclases.Bala.q.numbala == i)[0])
            else:
                try:
                    a = int(entrada)
                except:
                    utils.dialogo_info(titulo='ERROR', texto='El número de bala (%s) introducido no es válido' % entrada, padre = self.wids['ventana'])
                    return
                if not self.objeto.balaEnParte(a):
                    utils.dialogo_info(titulo='ERROR', texto='El número de bala (%i) introducido no pertece al parte.' % a, padre = self.wids['ventana'])
                    return
                else:
                    temp = [pclases.Bala.select(
                        pclases.Bala.q.numbala == a)[0]]
            balas = []
            producto = temp[0].articulos[0].productoVenta
            campos = producto.camposEspecificosBala
            for b in temp:
                pclases.Auditoria.modificado(b.articulo, self.usuario,
                        __file__,
                        "Impresión de etiqueta para bala %s" % (
                            b.articulo.get_info()))
                if campos.antiuv:
                    acabado = '1'
                else:
                    acabado = '0'
                elemento = {'descripcion': producto.descripcion,
                            'codigo':b.codigo,
                            'color':str(campos.color),
                            'peso':str(b.pesobala),
                            'lote':str(b.lote.numlote),
                            'tipo': campos.tipoMaterialBala and str(campos.tipoMaterialBala.descripcion) or "",
                            'longitud':str(campos.corte),
                            'nbala':str(b.numbala),
                            'dtex':str(campos.dtex),
                            'dia':utils.str_fecha(b.fechahora),
                            'acabado':acabado,
                            'codigoBarra':producto.codigo}
                balas.append(elemento)
            reports.abrir_pdf(geninformes.etiquetasBalas(balas))

    def etiquetasPeq(self, boton):
        """
        Imprime las etiquetas de las balas
        en la etiquetadora del parte seleccionado
        """
        model,paths = self.wids['tv_balas'].get_selection().get_selected_rows()
        if self.producto != None and self.producto.es_bigbag():
            bigbags_defecto = []
            for path in paths:
                bigbags_defecto.append(model[path][1].upper())
            bigbags_defecto.sort()
            bigbags_defecto = ", ".join(bigbags_defecto)
            imprimir_etiquetas_bigbags(bigbags_defecto, self)
        else:
            balas_defecto = []
            for path in paths:
                balas_defecto.append(model[path][1].upper().replace("B", ""))
            balas_defecto.sort()
            balas_defecto = ', '.join(balas_defecto)

            entrada = utils.dialogo_entrada(titulo='ETIQUETAS',
                        texto='Introduzca el número de bala o '
                              'el rango (usando el \'-\') que desea '
                              'etiquetar:',
                        valor_por_defecto = balas_defecto,
                        padre = self.wids['ventana'])
            if entrada != None:
                if '-' in entrada:
                    rango = entrada.split('-')
                    try:
                        a = int(rango[0])
                        b = int(rango[1])
                        if a <= b:
                            b += 1
                        else:
                            a, b = b, a+1
                    except:
                        utils.dialogo_info(titulo='ERROR',
                            texto = 'Los números de bala introducidos no son '
                                    'válidos',
                            padre = self.wids['ventana'])
                        return
                    valido = True
                    for i in range(a, b):
                        if not self.objeto.balaEnParte(i):
                            valido = False
                            break
                    if not valido:
                        utils.dialogo_info(titulo='ERROR',
                            texto='El número de bala %d introducido no '
                                  'pertece al parte.\nCompruébelo y vuelva a'
                                  ' intentarlo.' % i,
                            padre = self.wids['ventana'])
                        return
                    temp = []
                    for i in range(a, b):
                        temp.append(pclases.Bala.select(
                                        pclases.Bala.q.numbala == i)[0])
                else:
                    regexp = re.compile("\d*")
                    try:
                        balas = [int(i) for i in regexp.findall(entrada)
                                 if i != ""]
                    except:
                        utils.dialogo_info(titulo='ERROR',
                            texto='El texto %s no es válido' % (entrada),
                            padre = self.wids['ventana'])
                        return
                    for a in balas:
                        if not self.objeto.balaEnParte(a):
                            utils.dialogo_info(titulo='ERROR',
                                texto = 'El número de bala (%i) introducido '
                                        'no pertece al parte.' % a,
                                padre = self.wids['ventana'])
                            return
                    temp = [pclases.Bala.select(pclases.Bala.q.numbala == a)[0]
                            for a in balas]
                balas = []
                producto = temp[0].articulos[0].productoVenta
                campos = producto.camposEspecificosBala
                for b in temp:
                    pclases.Auditoria.modificado(b.articulo, self.usuario,
                        __file__,
                        "Impresión de etiqueta para bala %s" % (
                            b.articulo.get_info()))
                    if campos.antiuv:
                        acabado = '1'
                    else:
                        acabado = '0'
                    elemento = {'descripcion': producto.descripcion,
                                'codigo':b.codigo,
                                'color':str(campos.color),
                                'peso': utils.float2str(b.pesobala),
                                'lote': b.lote.codigo,
                                'tipo': campos.tipoMaterialBala
                                  and str(campos.tipoMaterialBala.descripcion)
                                  or "",
                                'longitud':str(campos.corte),
                                'nbala':str(b.numbala),
                                'dtex':str(campos.dtex),
                                'dia':utils.str_fecha(b.fechahora),
                                'acabado':acabado,
                                'codigoBarra':producto.codigo}
                    balas.append(elemento)
                try:
                    reports.abrir_pdf(
                        geninformes.etiquetasBalasEtiquetadora(balas))
                except (IOError, OSError), msg:
                    txt = "%spartes_de_fabricacion_balas::etiquetasPeq -> "\
                          "IOError: %s" % (
                            self.usuario
                                and self.usuario.usuario + ": "
                                or "",
                            msg)
                    self.logger.error(txt)
                    txt = """
                    Se produjo un error al imprimir la etiqueta.
                    Compruebe que queda espacio en la unidad y elimine los
                    archivos temporales si fuera necesario.

                    Información de depuración:
                    %s
                    """ % txt
                    utils.dialogo_info(titulo = "ERROR DE IMPRESIÓN",
                                       texto = txt,
                                       padre = self.wids['ventana'])

    def _salir(self, w, event = None):
        if ("w" in self.__permisos
            and self.objeto
            and not self.objeto.bloqueado
            and self.objeto.fecha < mx.DateTime.localtime()-mx.DateTime.oneDay
           ): #Tiene permiso para bloquear el parte y este tiene más de un día.
            res = utils.dialogo(titulo = "DEBE VERIFICAR EL PARTE",
                                texto = "Antes de cerrar el parte debe verifi"
                                        "carlo.\n¿Marcar como verificado?",
                                padre = self.wids['ventana'],
                                bloq_temp = ["Sí"])
            self.objeto.bloqueado = res
            self.wids['ch_bloqueado'].set_active(self.objeto.bloqueado)
            self.objeto.make_swap()
            # return True
        if not self.salir(w, mostrar_ventana = event == None):
            # Devuelve True cuando se cancela el cierre de la ventana (por temas de event-chain).
            try:
                padre = self.wids['ventana']
            except KeyError:
                padre = None
            vpro = VentanaActividad(texto = "Comprobando disparo de alertas...",
                                    padre = padre)
            vpro.mostrar()
            linea = self.linea
            vpro.mover()
            if linea == None:
                myprint("WARNING: La línea de fibra no está correctamente dada de alta.")
                self.logger.error("partes_de_fabricacion_balas::_salir; La línea de fibra no está correctamente dada de alta.")
            else:
                vpro.mover()
                formulacion = linea.formulacion
                for ca in [ca_con_p for ca_con_p
                           in formulacion.consumosAdicionales
                           if ca_con_p.productoCompra != None
                              and not ca_con_p.productoCompra.obsoleto]:
                    vpro.mover()
                    # Verifico que no haya productos bajo mínimos:
                    if (ca.productoCompra.existencias
                            < ca.productoCompra.minimo):
                        vpro.mover()
                        try:
                            v = pclases.Ventana.select(pclases.Ventana.q.fichero == "pedidos_de_compra.py")[0]
                        except IndexError:
                            txterror = "WARNING: ¡La ventana de pedidos"\
                                       " de compra SE HA PERDIDO!"
                            myprint(txterror)
                            self.logger.warning(txterror)
                        mensaje = "El producto %s tiene las existencias bajo mínimos. Considere hacer un pedido de compra." % ca.productoCompra.descripcion
                        for u in [p.usuario for p in v.permisos if p.nuevo]:
                            vpro.mover()
                            u.enviar_mensaje(mensaje)
                    # Y Verifico que no haya existencias negativas:
                    if ca.productoCompra.existencias < 0:
                        vpro.mover()
                        try:
                            v = pclases.Ventana.select(pclases.Ventana.q.fichero == "pedidos_de_compra.py")[0]
                        except IndexError:
                            myprint("WARNING: ¡La ventana de pedidos de compra SE HA PERDIDO!")
                            self.logger.error("¡La ventana de pedidos de compra SE HA PERDIDO!")
                        vpro.mover()
                        mensaje = "El producto %s tiene existencias NEGATIVAS. Corrija el error lo antes posible." % ca.productoCompra.descripcion
                        for u in [p.usuario for p in v.permisos if p.nuevo]:
                            vpro.mover()
                            u.enviar_mensaje(mensaje)
            vpro.mover()
            vpro.ocultar()

    def add_empleados_calendario(self):
        """
        Añade los empleados planificados según el calendario laboral
        para la línea de producción.
        1.- Obtener el calendario para self.linea.
        2.- Obtener los laborables del calendario correspondiente a la fecha del objeto.
        3.- Filtrar los laborables en función del turno correspondiente a la hora del objeto.
        4.- Obtener los empleados del laborable resultante.
        5.- Eliminar los empleados actuales. (PREGUNTAR PRIMERO)
        6.- Insertarlos los nuevos en el parte.
        """
        if self.linea != None:
            idldp = self.linea.id
            CAL = pclases.CalendarioLaboral
            calendarios = CAL.select("""linea_de_produccion_id = %d AND
                                        date_part('month', mes_anno) = %d AND
                                        date_part('year', mes_anno) = %d""" \
                                        % (idldp, self.objeto.fecha.month, self.objeto.fecha.year))
            if calendarios.count() == 1:
                calendario = calendarios[0]
                empleados = self.get_empleados_de_calendario(calendario)
                # Si hay empleados
                if self.objeto.horasTrabajadas != []:
                    # Si no son los mismos del calendario y los quiere borrar.
                    if [ht.empleado for ht in self.objeto.horasTrabajadas] != empleados \
                       and utils.dialogo(titulo = "¿ELIMINAR OPERARIOS?",
                                         texto="El parte ya tiene empleados "
                                         "relacionados.\n¿Desea eliminarlos "
                                         "y asociar los definidos en el "
                                         "turno?",
                                         padre=self.wids['ventana']):
                        for ht in self.objeto.horasTrabajadas:
                            self.objeto.removeEmpleado(ht.empleado)
                    else:
                        # Si no los quiere borrar, cancelo todo.
                        return
                # Si no había empleados o no eran los mismos y los ha borrado.
                # Añado empleados de los laborables que cumplan el turno y sean de producción (no-recuperación).
                for empleado in empleados:
                    self.objeto.addEmpleado(empleado)
            elif calendarios.count() > 1:
                self.logger.error("partes_de_fabricacion_balas.py: Existe más de un calendario laboral para el mes, año y línea de producción: fecha %s - idldp %d - idparte %s." % (self.objeto.fecha, idldp, self.objeto.id))

    def get_empleados_de_calendario(self, calendario):
        res = []
        LAB = pclases.Laborable
        dia_lab_parte = self.objeto.fecha
        seis_am = mx.DateTime.DateTimeDeltaFrom(hours = 6)
        medianoche = mx.DateTime.DateTimeDeltaFrom(hours = 0)
        if self.objeto.horainicio >= medianoche and \
           self.objeto.horainicio <= seis_am and \
           self.objeto.horafin <= seis_am:  # No se mezclan turnos, esta última comprobación podría no hacer falta.
            dia_lab_parte -= mx.DateTime.oneDay
        laborables = LAB.select("""calendario_laboral_id = %d AND date_part('day', fecha) = %d""" \
                                    % (calendario.id, dia_lab_parte.day))
        for laborable in laborables:
            turno = laborable.turno
            if turno == None:
                mensaje = "partes_de_fabricacion_balas.py::get_empleados_de_calendario -> Laborable ID %d no tiene turno relacionado. Intento eliminarlo de la BD." % (laborable.id)
                self.logger.error(mensaje)
                try:
                    laborable.destroy(ventana = __file__)
                    idlaborable = laborable.id
                    self.logger.warning("partes_de_fabricacion_balas.py::get_empleados_de_calendario -> Registro laborable ID %d ELIMINADO SATISFACTORIAMENTE." % (idlaborable))
                except:
                    self.logger.error("partes_de_fabricacion_balas.py::get_empleados_de_calendario -> Registro laborable ID %d NO ELIMINADO." % (laborable.id))
                myprint("ERROR: %s" % (mensaje))
                continue
            turnohorainicio = utils.DateTime2DateTimeDelta(turno.horainicio)
            turnohorafin = utils.DateTime2DateTimeDelta(turno.horafin)
            objetohorainicio = utils.DateTime2DateTimeDelta(self.objeto.horainicio)
            objetohorafin = utils.DateTime2DateTimeDelta(self.objeto.horafin)
            if not turno.recuperacion:
                ohi = objetohorainicio
                ohf = objetohorafin
                thi = turnohorainicio
                thf = turnohorafin
                if thi > thf: thf += mx.DateTime.oneDay
                if ohi > ohf: ohf += mx.DateTime.oneDay
                if ohi >= medianoche and ohi < seis_am: ohi += mx.DateTime.oneDay
                if ohf >= medianoche and ohf <= seis_am: ohf += mx.DateTime.oneDay
                if thi <= ohi <= thf and thi <= ohf <= thf:
                    for empleado in laborable.empleados:
                        res.append(empleado)
        return res

    def iniciar_pesaje_auto(self, boton):
        """
        Abre la ventana de pesaje automático.
        """
        # XXX: Caso especial para reenvasado de bigbags: 27 de marzo de 2007.
        if self.objeto.es_parte_de_reenvasado():
            silo_marcado = True     # Engaño a la ventana y le digo que sí se ha marcado un silo aunque sea mentira. No se va a consumir de él de todas formas.
        else:
        # XXX
            silo_marcado = False
            for silo in pclases.Silo.select():
                silo_marcado = silo_marcado or self.wids['ch_silo_ID%d' % (silo.id)].get_active()
            # OJO: Número de "silos virtuales" de granza reciclada
            # HARCODED (aquí y arriba).
            silo_marcado = silo_marcado or self.wids['ch_reciclada_0'].get_active() or self.wids['ch_reciclada_1'].get_active()
            if silo_marcado == False:
                utils.dialogo_info(titulo = "NO PUEDE PRODUCIR",
                    texto = "¡No puede producir fibra si no marca un "
                            "silo del que consumir granza!",
                    padre = self.wids['ventana'])
        if silo_marcado:
            ventana_pesaje = crear_ventana_pesaje(self,  # @UnusedVariable
                                padre = self.wids['ventana'])

    def consumir_manual(self, boton):
        """
        Crea un registro de consumo manualmente y unifica los
        consumos a continuación.
        Si algún consumo acaba con cantidad 0 (porque se haya
        agregado un consumo negativo que haya restado a otro)
        se elimina antes de salir de la rutina.
        """
        # Pedir producto(s) a consumir.
        producto, texto_buscado = utils.pedir_producto_compra(  # @UnusedVariable
                                                padre = self.wids['ventana'])
        # Pedir cantidad.
        if producto != None:
            unidad = ""
            try:
                producto_unidad = producto.unidad
                if producto_unidad != "":
                    unidad = " en %s" % (producto_unidad)
            except AttributeError, msg:
                self.logger.error("%sEl producto tipo %s ID %d no tiene atributo unidad. Excepción AttributeError: %s."
                    % (self.usuario and self.usuario.usuario + ": " or "",
                       type(producto),
                       producto != None and producto.id or "NONE",
                       msg))
            descripcion = producto.descripcion
            cantidad = utils.dialogo_entrada(titulo = "CANTIDAD",
                        texto = "Introduzca la cantidad a consumir de %s%s."%(
                            descripcion, unidad),
                        padre = self.wids['ventana'])
            if cantidad != None:
                try:
                    cantidad_a_consumir = utils._float(cantidad)
                except (TypeError, ValueError):
                    utils.dialogo_info(titulo = "ERROR DE FORMATO",
                        texto = 'El texto introducido "%s" no es un número.'%(
                            cantidad),
                        padre = self.wids['ventana'])
                else:
                    # Crear consumo.
                    producto.sync()
                    consumo = pclases.Consumo(silo = None,
                        parteDeProduccion = self.objeto,
                        productoCompra = producto,
                        actualizado = True,
                        antes = producto.existencias,
                        despues = producto.existencias - cantidad_a_consumir,
                        cantidad = cantidad_a_consumir)
                    pclases.Auditoria.nuevo(consumo, self.usuario, __file__)
                    # Actualizar existencias
                    producto.existencias -= cantidad_a_consumir
                    producto.syncUpdate()
                    producto.add_existencias(-cantidad_a_consumir)
                    self.logger.warning("%sCONSUMO LÍNEA FIBRA -> PARTE %d "
                            "-> Consumiendo manualmente %f %s de %s (ID %d). "
                            "Existencias: %f."
                                        % (self.usuario
                                            and self.usuario.usuario + ": "
                                            or "",
                                           self.objeto.id,
                                           cantidad_a_consumir,
                                           producto.unidad,
                                           producto.descripcion,
                                           producto.id,
                                           producto.existencias))
                    # Unificar consumos.
                    self.objeto.unificar_consumos()
                    # Eliminar consumos con cantidad cero.
                    for c in self.objeto.consumos:
                        if c.cantidad == 0:
                            try:
                                c.destroy(ventana = __file__)
                            except Exception, msg:
                                self.logger.error("%sConsumo ID %d no se pudo eliminar. Excepción: %s"
                                                  % (self.usuario and self.usuario.usuario + ": " or "",
                                                     c.id,
                                                     msg))
                    self.rellenar_tabla_consumos()
                    # Buscar y crear (si no existe) el albarán interno de consumos.
                    self.objeto.buscar_o_crear_albaran_interno()

    def add_desecho(self, boton):
        """
        Crea un registro de consumo de material desechado y
        actualiza la tabla.
        """
        producto = self.buscar_producto_compra(defecto = "",
                                titulo_defecto = "BUSCAR PRODUCTO A DESECHAR")
        if producto != None:
            cantidad = utils.dialogo_entrada(titulo = "INTRODUZCA CANTIDAD",
                        texto = "Teclee la cantidad que se desechará de %s:"%(
                            producto.descripcion),
                        padre = self.wids['ventana'])
            if cantidad != None:
                try:
                    cantidad = utils._float(cantidad)
                except ValueError:
                    utils.dialogo_info(titulo = "ERROR EN FORMATO",
                        texto="El texto tecleado %s no es un número válido."%(
                            cantidad),
                        padre = self.wids['ventana'])
                else:
                    observaciones = utils.dialogo_entrada(
                        titulo = "OBSERVACIONES",
                        texto = "Teclee, si lo desea, el motivo por el cual "
                                "la cantidad desechada de %s se considera "
                                "defectuosa:" % (producto.descripcion),
                        padre = self.wids['ventana'])
                    if observaciones != None:
                        try:
                            desecho = pclases.DescuentoDeMaterial.desechar(
                                producto, cantidad, self.objeto, observaciones)
                        except AssertionError, msg:
                            self.logger.error("%spartes_de_fabricacion_balas::add_desecho -> AssertionError: %s" % (self.usuario and self.usuario.usuario + ": " or "", msg))
                        if desecho.cantidad != cantidad:
                            utils.dialogo_info(titulo = "EXISTENCIAS INSUFICIENTES",
                                               texto = "La cantidad de %s en almacén era inferior a la cantidad tecleada (%s).\nSe ha descontado %s en su lugar." % (desecho.productoCompra.descripcion, utils.float2str(cantidad), utils.float2str(desecho.cantidad)),
                                               padre = self.wids['ventana'])
                        self.objeto.unificar_desechos()
                        self.rellenar_tabla_desechos()

    def drop_desecho(self, boton):
        """
        Cancela el desecho seleccionado.
        """
        model, paths = self.wids['tv_desecho'].get_selection().get_selected_rows()
        if  paths != None and paths != []:
            for path in paths:
                idddm = model[path][-1]
                ddm = pclases.DescuentoDeMaterial.get(idddm)
                try:
                    ddm.anular()
                except AssertionError, msg:
                    self.logger.error("%spartes_de_fabricacion_balas::drop_desecho -> AssertionError: %s" % (self.usuario and self.usuario.usuario + ": " or "", msg))
                    utils.dialogo_info(titulo = "ERROR",
                                       texto = "Ocurrió un error anulando un descuento de material.\nPulse «Aceptar» para continuar.\n\n\n\nInformación de depuración:\n\n%s" % (msg),
                                       padre = self.wids['ventana'])
                self.rellenar_tabla_desechos()
                self.objeto.unificar_desechos()



def crear_ventana_pesaje(ventana_parte, padre = None):
    """
    Crea una ventana de pesaje.
    Necesita python-serial.
    Se usa "COM1" como puerto si el sistema es MS-Windows. "/dev/ttyS0" o
    "/dev/ttyS1" (por este orden) si el sistema es GNU/Linux.
    """
    import gobject
    com = utils.get_puerto_serie()
    if com != None:
        ventana, l_peso, e_numbala, b_cancelar, b_aceptar, l_estable, l_peso_sin = build_ventana(padre)
        src_id = gobject.timeout_add(1500, recv_serial, com, ventana, l_peso, ventana_parte, e_numbala, l_estable, l_peso_sin)
        b_cancelar.connect("clicked", cerrar_ventana_bascula, ventana, com, src_id)
        ventana.connect("destroy", cerrar_ventana_bascula, ventana, com, src_id)
        b_aceptar.connect("clicked", leer_nueva_bala, l_peso, l_estable, e_numbala, ventana_parte, l_peso_sin)
        ultimo_mas_uno = pclases.Bala._queryOne("""SELECT COALESCE(MAX(numbala), 0)+1 FROM bala""")
        proximo_numbala = `int(ultimo_mas_uno[0])`
        e_numbala.set_text("B%s" % (proximo_numbala))
        ventana.show_all()
    else:
        utils.dialogo_info(titulo = "ERROR PUERTO SERIE",
            texto = "Fue imposible determinar y abrir el puerto serie.",
            padre = ventana_parte.wids['ventana'])

def leer_nueva_bala(boton, l_peso, l_estable, e_numbala, ventana_parte,
                    l_peso_sin):
    """
    Crea una nueva bala tomando el peso del label.
    Si l_estable es distinto de "Estable" da error y
    no crea la bala. Si crea la bala, actualiza e_numbala.
    """
    peso_str = l_peso_sin.get_text().replace("[", "").replace("]", "").strip()
    peso_real_str = l_peso.get_text()
    try:
        peso_sin = float(peso_str)
        peso_real = utils.parse_float(peso_real_str)
    except ValueError:
        utils.dialogo_info(titulo="PESO INCORRECTO",
                           texto='"%s" no es un peso correcto.' % (peso_str),
                           padre=ventana_parte.wids['ventana'])
    else:
        if l_estable.get_text().lower() != "estable":
            utils.dialogo_info(titulo="PESO NO ESTABILIZADO",
                texto="Debe esperar a que se estabilice la báscula.",
                padre=ventana_parte.wids['ventana'])
        else:
            codigo_bala = e_numbala.get_text()
            try:
                numbala = int(
                    codigo_bala.upper().replace("B", "").replace("L", ""))
            except ValueError:
                utils.dialogo_info(titulo="BALA INCORRECTA",
                                   texto="El código %s no es correcto.",
                                   padre=ventana_parte.wids['ventana'])
            else:
                nueva_bala = crear_nueva_bala(numbala, codigo_bala, peso_sin,
                                              peso_real, ventana_parte)
                if nueva_bala != None:
                    ultimo_mas_uno = pclases.Bala._queryOne("""
                        SELECT COALESCE(MAX(numbala), 0)+1 FROM bala""")
                    proximo_numbala = `int(ultimo_mas_uno[0])`
                    e_numbala.set_text("B%s" % (proximo_numbala))

def crear_nueva_bala(numbala, codigo_bala, peso_neto, peso_real, ventana_parte):
    """
    Crea un nuevo artículo y su bala asociada y lo relaciona
    con el parte de la ventana. Actualiza también la ventana
    del parte para ver los cambios en tiempo real e imprime
    la etiqueta.
    Devuelve la bala creada o None si ocurrió algún problema.
    """
    bala = None
    lote = ventana_parte.get_lote()
    if (ventana_parte.comprobar_configuracion_consumos_silo() and
        lote != None and isinstance(lote, pclases.Lote)):
        # De momento esto no vale para fibra de cemento.
        balas = pclases.Bala.select(pclases.Bala.q.codigo == codigo_bala)
        if balas.count() == 0:
            bala = pclases.Bala(lote=lote,
                                partidaCarga=None,
                                numbala=numbala,
                                codigo=codigo_bala,
                                pesobala=peso_neto,  # OJO: Peso SIN embalaje
                                muestra=False,
                                claseb=False,
                                motivo="")
            pclases.Auditoria.nuevo(bala, ventana_parte.usuario, __file__)
            parte = ventana_parte.objeto
            producto = ventana_parte.producto
            articulo = pclases.Articulo(bala=bala,
                            rollo=None,
                            bigbag=None,
                            parteDeProduccion=parte,
                            albaranSalida=None,
                            productoVenta=producto,
                            almacen=pclases.Almacen.get_almacen_principal(),
                            pesoReal=peso_real)
            pclases.Auditoria.nuevo(articulo, ventana_parte.usuario, __file__)
            ventana_parte.descontar_material_adicional(articulo)
            try:
                imprimir_etiqueta(articulo, ventana_parte)
            except IOError, msg:
                txt = "%spartes_de_fabricacion_balas::crear_nueva_bala -> IOError: %s" % (ventana_parte.usuario and ventana_parte.usuario.usuario + ": " or "", msg)
                ventana_parte.logger.error(txt)
                txt = """
                Se produjo un error al imprimir la etiqueta.
                Compruebe que queda espacio en la unidad y elimine los
                archivos temporales si fuera necesario.

                Información de depuración:
                %s
                """ % txt
                utils.dialogo_info(titulo = "ERROR DE IMPRESIÓN",
                                   texto = txt,
                                   padre = ventana_parte.wids['ventana'])
            ventana_parte.logger.debug("Volcando bala %s a Murano..." % articulo.codigo)
            volcado_a_murano = murano.ops.create_articulo(articulo)
            ventana_parte.logger.debug("Resultado del volcado: %s -> %s" % (
                articulo.codigo, volcado_a_murano))
            ventana_parte.actualizar_ventana()
    return bala

def imprimir_etiqueta(articulo, ventana_parte):
    """
    Imprime una etiqueta de la bala del artículo recibido.
    PRECONDICIÓN: El artículo debe estar relacionado con una bala.
    """
    producto = articulo.productoVenta
    b = articulo.bala
    campos = producto.camposEspecificosBala
    if campos.antiuv:
        acabado = '1'
    else:
        acabado = '0'
    elemento = {'descripcion': producto.descripcion,
                'codigo': b.codigo,
                'color': campos.color,
                'peso': utils.float2str(b.pesobala),
                'lote': b.lote.codigo,
                'tipo': campos.tipoMaterialBala
                            and campos.tipoMaterialBala.descripcion or "",
                'longitud': str(campos.corte),
                'nbala': str(b.numbala),
                'dtex': str(campos.dtex),
                'dia': utils.str_fecha(b.fechahora),
                'acabado': acabado,
                'codigoBarra': producto.codigo}
    balas = [elemento]
    # reports.abrir_pdf(geninformes.etiquetasBalasEtiquetadora(balas))
    reports.mandar_a_imprimir_con_ghostscript(
        geninformes.etiquetasBalasEtiquetadora(balas))
    pclases.Auditoria.modificado(articulo, None, __file__,
            "Impresión de etiqueta para bala %s." % (articulo.get_info()))

def build_ventana(padre):
    """
    Construye un gtk.Window con los widgets
    para el control del pesaje automático.
    """
    ventana = gtk.Window()
    ventana.set_title("LECTURA AUTOMÁTICA DE BÁSCULA")
    ventana.set_transient_for(padre)
    ventana.set_modal(True)
    contenedor = gtk.VBox()
    ventana.add(contenedor)
    box_bala = gtk.HBox()
    box_bala.add(gtk.Label("Código de bala: "))
    e_numbala = gtk.Entry()
    e_numbala.set_property("editable", False)
    e_numbala.set_property("has-frame", False)
    box_bala.add(e_numbala)
    b_cancelar = gtk.Button(stock = gtk.STOCK_CANCEL)
    l_peso = gtk.Label('<big><span color="dark green">Esperando peso...</span></big>')
    l_peso.set_use_markup(True)
    l_peso.set_justify(gtk.JUSTIFY_CENTER)
    l_peso.set_property('xalign', 0.5)
    l_peso_sin = gtk.Label('<span color="dark green"> (Esperando peso...) </span>')
    l_peso_sin.set_use_markup(True)
    l_peso_sin.set_justify(gtk.JUSTIFY_CENTER)
    l_peso_sin.set_property('xalign', 0.5)
    l_estable = gtk.Label('<span color="black">No lectura</span>')
    l_estable.set_use_markup(True)
    l_estable.set_justify(gtk.JUSTIFY_CENTER)
    l_estable.set_property('xalign', 0.5)
    # ch_marcado = gtk.CheckButton("_Marcado CE")
    # ch_marcado.set_active(True)
    contenedor.add(box_bala)
    contenedor.add(l_peso)
    contenedor.add(l_peso_sin)
    contenedor.add(l_estable)
    # contenedor.add(ch_marcado)
    b_aceptar_peso = gtk.Button(label = "_Aceptar peso")
    contenedor.add(b_aceptar_peso)
    contenedor.add(b_cancelar)
    ventana.resize(300, 200)
    return ventana, l_peso, e_numbala, b_cancelar, b_aceptar_peso, l_estable, l_peso_sin    #, ch_marcado

def cerrar_ventana_bascula(boton, ventana, com, src_id):
    """
    Cierra (destruye, más bien) la ventana de
    pesaje y cierra el puerto serie.
    """
    import gobject
    gobject.source_remove(src_id)
    ventana.destroy()
    com.close()

def recv_serial(com, ventana, l_peso, ventana_parte, e_numbala, l_estable, l_peso_sin):
    """
    A diferencia del de rollos, este simplemente actualiza el peso mostrado en pantalla.
    La bala se creará con el peso mediante el botón correspondiente.
    """
    try:
        c = com.readline(eol = '\r')
    except TypeError:   # Versión que no soporta especificar fin de línea.
        import io
        sio = io.TextIOWrapper(io.BufferedRWPair(com, com))
        try:
            c = sio.readline()
        except ValueError:  # ¿Puerto cerrado?
            com = utils.get_puerto_serie()
            sio = io.TextIOWrapper(io.BufferedRWPair(com, com))
            try:
                c = sio.readline()
            except UnicodeDecodeError:
                c = "" # Basurilla. La lectura no es perfecta. Vuelvo a iterar.
        except UnicodeDecodeError:
            c = ""  # Ha leído mierda. Vuelvo a iterar.
    com.flushInput()    # Evito que datos antiguos se queden en el
    com.flush()         # buffer impidiendo nuevas lecturas.
    if c.strip() != '':
        # Tratar
        try:
            estable, algo, peso_str = c.split()  # @UnusedVariable
        except ValueError, msg:  # @UnusedVariable
            # utils.dialogo_info(titulo = "ERROR DE PESAJE",
            #                    texto = "Ocurrió un error en la comunicación con la báscula.\nCierre y vuelva a abrir la ventana de lectura de báscula.",
            #                    padre = ventana_parte.wids['ventana'])
            # myprint(c, msg)
            # No ha leído bien. Salgo y lo volveré a leer en la siguiente iteración.
            pass
        else:
            if estable == '0':
                l_estable.set_text('<span color="red">Peso inestable</span>')
            elif estable == '2':
                l_estable.set_text('<span color="green">Estable</span>')
            elif estable == '3':
                l_estable.set_text('<span color="orange">Peso nulo</span>')
            else:
                l_estable.set_text('<span color="black">Código desconocido</span>')
            l_estable.set_use_markup(True)
            l_estable.set_justify(gtk.JUSTIFY_CENTER)
            l_estable.set_property('xalign', 0.5)

            try:
                peso = float(peso_str)
                #if peso % 1 != 0:   # Le quito un kilo
                #    peso_sin = peso - 1.0
                #else:   # CWT: Le quito kilo y medio si es peso "redondo"
                #    peso_sin = peso - 1.5
                # HARCODED: Peso embalaje debería estar definido en algún sitio
                peso_sin = peso - pclases.PESO_EMBALAJE_BALAS
                l_peso.set_text('<b><span color="dark green">%s</span></b>' % (
                    utils.float2str(peso)))
                l_peso_sin.set_text('<b><big><span color="dark green">'
                    '%s</span></big></b>' % (utils.float2str(peso_sin)))
            except ValueError:
                peso = 0
                l_peso.set_text('<b><big><span color="dark green">'
                    'ERROR</span></big></b>')
                l_peso_sin.set_text('<b><big><span color="dark green">'
                    'ERROR</span></big></b>')
            l_peso.set_use_markup(True)
            l_peso_sin.set_use_markup(True)
    #DEBUG:         myprint("Recibido peso: %s" % (peso_str)) #DEBUG:
    return True

def imprimir_etiquetas_bigbags(lista_bbs_defecto = [], ventana_parte = None):
    """
    Muestra un diálogo donde introducir los CÓDIGOS (completos, "Cxxx") de
    bigbags a imprimir y construye y muestra el PDF.
    """
    if ventana_parte != None:
        ventana_padre = ventana_parte.wids['ventana']
    else:
        ventana_padre = None
    codigos = utils.dialogo_pedir_codigos(
        titulo="INTRODUZCA CÓDIGOS DE BIGBAGS",
        texto="Introduzca códigos de bigbags separados por coma o espacios."
                "\nPuede introducir también rangos separados por guión.",
        padre=ventana_padre,
        valor_por_defecto=lista_bbs_defecto)
    if codigos is not None:     # Es None si cancela.
        bigbags = []
        no_encontrados = []
        for codigo in codigos:
            if "C" in codigo.upper():       # OJO: Si cambia el tema de que
                # los códigos de geocem empiecen por "C", cambiar aquí también.
                try:
                    bb = pclases.Bigbag.select(
                            pclases.Bigbag.q.codigo == codigo)[0]
                except IndexError:
                    no_encontrados.append(codigo)
                    continue
                else:
                    bigbags.append(bb)
            else:
                try:
                    bb = pclases.Bigbag.select(
                            pclases.Bigbag.q.numbigbag == codigo)[0]
                except (ValueError, IndexError):
                    no_encontrados.append(codigo)
                    continue
                else:
                    bigbags.append(bb)
        reports.abrir_pdf(geninformes.etiquetasBigbags(bigbags))
        for bb in bigbags:
            pclases.Auditoria.modificado(bb.articulo, None, __file__,
                "Impresión de etiqueta para bigbag %s." % (
                    bb.articulo.get_info()))


def mostrar_carga_silo(label, silo):
    """
    Muestra la carga del silo «silo» en el label recibido.
    """
    try:
        ocupado = murano.ops.get_ocupado_silo(silo)
    except:
        #print "No se pudo leer carga de silo %s en Murano. Fallback a ginn."%(
        #        silo.nombre)
        ocupado = silo.ocupado
    strocupado = utils.float2str(ocupado, 1)
    capacidad = silo.capacidad
    if ocupado < capacidad / 4:
        strocupado = '<span foreground="red">%s</span>' % strocupado
    label.set_text(" %s/<small>%s</small> " % (strocupado,
                   utils.float2str(capacidad/1000, 0) + '<i>k</i>'))
    label.set_use_markup(True)


def entran_en_turno(selfobjeto, hi, hf):
    # TODO: Falta comprobar que además de que entran en el turno no se
    # pisen con otras incidencias del mismo parte.
    hini = mx.DateTime.DateTimeDeltaFrom(':'.join(map(str, hi.tuple()[3:6])))
    hfin = mx.DateTime.DateTimeDeltaFrom(':'.join(map(str, hf.tuple()[3:6])))
    tini = selfobjeto.horainicio
    if not isinstance(tini, type(hini)):
        # Can't compare datetime.time to mx.DateTime.DateTimeDelta.
        tini = utils.DateTime2DateTimeDelta(tini)
    tfin = selfobjeto.horafin
    if not isinstance(tfin, type(hfin)):
        # Can't compare datetime.time to mx.DateTime.DateTimeDelta.
        tfin = utils.DateTime2DateTimeDelta(tfin)
    if tini <= tfin:
        hini_dentro = hini >= tini and hini <= tfin
        hfin_dentro = hfin >= tini and hfin <= tfin
    else:
        hini_dentro = hini >= tini or hini <= tfin
        hfin_dentro = hfin >= tini or hfin <= tfin
    return hini_dentro and hfin_dentro


def check_last_balas_bien_creadas(logger = None):
    """
    Compruebo que la última bala está bien creada para evitarme
    problemas. He tenido un par de casos en los que se ha ido la luz y
    deja el parte inusable a causa de esto.
    """
    max_a_comprobar = 2
    i = 0
    for i in range(max_a_comprobar):
        bala = pclases.Bala.select(orderBy = "-id")[i]
        try:
            a = bala.articulo
        except IndexError:
            txtmsg = "partes_de_fabricacion_balas::"\
                     "rellenar_widgets -> Elimino bala «huérfana» de "\
                     "artículo %s." % bala.puid
            if logger:
                logger.warning(txtmsg)
            myprint(txtmsg)
            bala.destroy(ventana = __file__)
    # EOComprobación


if __name__ == "__main__":
    p = PartesDeFabricacionBalas()
