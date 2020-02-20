#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2017  Francisco José Rodríguez Bogado,                   #
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
# # partes_de_fabricacion_bolsas.py - Partes embolsado fibra cem.
###################################################################
#  NOTAS:
##
#  ----------------------------------------------------------------
##
###################################################################
#  Changelog:
#  5 de mayo de 2009 -> Inicio
##
###################################################################
#  NOTAS:
##
###################################################################


# import sys, os
# sys.stdout = open("salida_debug.txt", "a")

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk, time
from framework import pclases
import mx.DateTime
import datetime
from informes import geninformes
from utils import _float as float
from ventana_progreso import VentanaActividad, VentanaProgreso
from partes_de_fabricacion_balas import verificar_solapamiento, \
                                        entran_en_turno
from partes_de_fabricacion_rollos import descontar_material_adicional
try:
    from api import murano
    MURANO = True
except ImportError:
    MURANO = False

def copy2(entry1, evento, entry2, sumar = 0):
    """
    Simplemente copia el contenido del entry1 en el entry2.
    Si sumar es algo distinto de 0 intenta convertir el contenido del entry 1
    a entero y escribirlo en el segundo como cadena tras sumarle el número
    en cuestión.
    """
    # No es más que para evitarme escribir la fecha de fin en 2 de cada 3
    # partes.
    if not sumar:
        entry2.set_text(entry1.get_text())
    else:
        # Y ahora la hora. Menos tecleo, más rapidez. Menos tonterías, más
        # felicidad. (Rocío TM).
        try:
            num = int(entry1.get_text())
        except:
            entry2.set_text(entry1.get_text())
        else:
            entry2.set_text(str((num + sumar) % 24))

MEMENTO_MORI = {'tipo': None,
                'que_imprimir': None}   # Tipo de etiqueta y qué imprimir
                # (caja, palé o palé + cajas) hasta que cierren la ventana
                # o cambien de parte.

class PartesDeFabricacionBolsas(Ventana):
    def __init__(self, objeto = None, usuario = None):
        self.SHOW_PALES_COMPLETOS = False   # Si True meterá también cajas y
                                            # bolsas en el treeview. Igual a
                                            # mucho más lento.
        self.NIVEL_POR_LOTES = 2    # Mínimo nivel (o máximo, según se vea)
                                    # para poder crear palés por lote.
        self.objeto = objeto
        if not isinstance(usuario, pclases.Usuario):
            try:
                usuario = pclases.Usuario.selectBy(usuario = usuario)[0]
            except IndexError:
                usuario = None
        self.usuario = usuario
        self.producto = None    # Producto relacionado con el parte.
        self.__lecturaescritura = objeto and objeto.id or None
        if usuario:
            nombreventana = "partes_de_fabricacion_bolsas.py"
            try:
                ventana = pclases.Ventana.selectBy(fichero = nombreventana)[0]
                self.__permisos = usuario.get_permiso(ventana)
            except IndexError:
                txt = "WARNING: partes_de_fabricacion_bolsas.py::__init__ -> "\
                      "No se pudieron determinar permisos de %s para la venta"\
                      "na %s." % (self.usuario.usuario, nombreventana)
                print txt
                self.logger.error(txt)
            else:
                self.__lecturaescritura = (self.__permisos.escritura
                    and self.objeto and self.objeto.id or None)
        else:
            class FakePermisos:
                def __init__(self):
                    self.lectura=self.escritura=self.permiso=self.nuevo=True
            self.__permisos = FakePermisos()
        Ventana.__init__(self, 'partes_de_fabricacion_bolsas.glade', objeto,
                         usuario = usuario)
        connections = {'b_salir/clicked': self._salir,
                       'ventana/delete_event' : self._salir,
                       'b_add_empleado/clicked': self.add_empleado,
                       'b_drop_empleado/clicked': self.drop_empleado,
                       "b_partida/clicked": self.seleccionar_partida,
                       "b_producto/clicked": self.seleccionar_producto,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_nuevo/clicked': self.crear_nuevo_partedeproduccion,
                       'b_borrar/clicked': self.borrar_parte,
                       'b_buscar/clicked': self.buscar_partedeproduccion,
                       'ch_bloqueado/clicked': self.bloquear,
                       'b_add_consumo/clicked': self.add_consumo,
                       'b_add_bigbag/clicked': self.add_bigbag,
                       'b_drop_consumo/clicked': self.drop_consumo,
                       'b_add_incidencia/clicked': self.add_incidencia,
                       'b_drop_incidencia/clicked': self.drop_incidencia,
                       'b_add_pale/clicked': self.add_pale,
                       'b_drop_pale/clicked': self.drop_pale,
                       'b_etiquetar/clicked': self.etiquetar,
                       'b_next/clicked': self.siguiente,
                       'b_back/clicked': self.anterior
                      }
        self.add_connections(connections)
        self.wids['e_fechaini'].connect("key-release-event",
                                        copy2,
                                        self.wids['e_fechafin'])
        self.wids['e_horaini'].connect("key-release-event",
                                       copy2,
                                       self.wids['e_horafin'],
                                       8)
        try:
            linea = pclases.LineaDeProduccion.select(
                pclases.LineaDeProduccion.q.nombre.contains('de embolsado'))[0]  # @UndefinedVariable
        except IndexError:
            print "WARNING: La línea de embolsado no está correctamente dada "\
                  "a de alta. La creo sobre la marcha."
            linea = pclases.LineaDeProduccion(formulacion = None,
                    nombre = "Línea de embolsado",
                    descripcion = "Línea de embolsado de fibra de cemento.",
                    observaciones = "Produce bolsas de fibra de cemento a par"\
                        "tir de bigbags fabricados en la línea de fibra.")
            pclases.Auditoria.nuevo(linea, self.usuario, __file__)
        self.linea = linea
        self.formulacion = linea.formulacion
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        gtk.main()

    def anterior(self, boton = None):
        if self.objeto:
            anterior = self.objeto.anterior()
            if anterior:
                self.objeto = anterior
                # Reinicio preferencias de etiqueta.
                global MEMENTO_MORI
                MEMENTO_MORI = {'que_imprimir': None, 'tipo': None}
                self.actualizar_ventana()
            else:
                utils.dialogo_info(titulo = "NO MÁS PARTES",
                    texto="No hay partes de producción anteriores al actual",
                    padre = self.wids['ventana'])

    def siguiente(self, boton = None):
        if self.objeto:
            siguiente = self.objeto.siguiente()
            if siguiente:
                self.objeto = siguiente
                # Reinicio preferencias de etiqueta.
                global MEMENTO_MORI
                MEMENTO_MORI = {'que_imprimir': None, 'tipo': None}
                self.actualizar_ventana()
            else:
                utils.dialogo_info(titulo = "NO MÁS PARTES",
                    texto="No hay partes de producción posteriores al actual",
                    padre = self.wids['ventana'])

    # --------------- Funciones auxiliares ------------------------------
    def leer_valores_ventana(self):
        """
        Devuelve un diccionario con los nombres de los campos del objeto
        como claves y los valores de la ventana ya tratados como valores.
        """
        res = {}
        try:
            fecha = utils.parse_fecha(self.wids['e_fechaini'].get_text())
        except (TypeError, ValueError):
            fecha = mx.DateTime.localtime()
            #self.wids['e_fechaini'].set_text(utils.str_fecha(fecha))
            # ¿Qué parte de LEER no entendiste? ¿Por qué cambias el entry?
        res["fecha"] = fecha
        try:
            hora = utils.parse_hora(self.wids['e_horaini'].get_text())
        except (TypeError, ValueError):
            hora = mx.DateTime.DateTimeDelta(0.0)
        res["horainicio"] = hora
        try:
            hora = utils.parse_hora(self.wids['e_horafin'].get_text())
        except (TypeError, ValueError):
            hora = mx.DateTime.DateTimeDelta(0.0)
        res["horafin"] = hora
        res["prodestandar"] = 0 # No se usa
        res["merma"] = 0.0      # Tampoco se usa
        res["bloqueado"] = self.wids['ch_bloqueado'].get_active()
        buff = self.wids['txt_observaciones'].get_buffer()
        txt = buff.get_text(buff.get_start_iter(), buff.get_end_iter())
        res["observaciones"] = txt
        res["fechahorainicio"] = res["fecha"] + res["horainicio"]
        try:
            fechafin = utils.parse_fecha(self.wids['e_fechafin'].get_text())
        except (TypeError, ValueError):
            fechafin = mx.DateTime.localtime()
            #self.wids['e_fechafin'].set_text(utils.str_fecha(fechafin))
        res["fechahorafin"] = fechafin + res["horafin"]
        codpartida = self.wids['e_partida'].get_text()
        try:
            partida = pclases.PartidaCem.selectBy(codigo = codpartida)[0]
            res["partidaCemID"] = partida.id
        except IndexError:
            print "partes_de_fabricacion_bolsas.py::leer_valores_ventana -> "\
                  "No se encontró partida con código '%s'. Probablemente "\
                  "no se haya terminado de cargar la ventana." % codpartida
            partida = None
            res["partidaCemID"] = None
        return res

    def es_diferente(self):
        """
        Devuelve True si la información en pantalla es distinta a la
        del objeto en memoria.
        """
        partedeproduccion = self.objeto
        if partedeproduccion == None:
            return False    # Si no hay partedeproduccion activo, devuelvo
                            # que no hay cambio respecto a la ventana
        condicion = True
        valores = self.leer_valores_ventana()
        for campo in valores:
            valor_objeto = getattr(self.objeto, campo)
            # XXX: El nuevo psycopg2 devuelve datetimes. Aaaargh!
            if "hora" in campo and not "fecha" in campo:
                valor_objeto = utils.DateTime2DateTimeDelta(valor_objeto)
            # XXX
            valor_ventana = valores[campo]
            condicion = condicion and valor_ventana == valor_objeto
            if not condicion:
                if pclases.DEBUG:
                    print "partes_de_fabricacion_bolsas.py::es_diferente -> ",\
                          campo, \
                          "ventana", type(valor_ventana), valor_ventana, \
                          "objeto", valor_objeto, type(valor_objeto)
                break
        return not condicion    # Condición verifica que sea igual

    def colorear_tabla_empleados(self):
        """
        Prepara y asocia la función para resaltar los empleados
        cuyas horas trabajadas sean inferiores o superiores a
        la duración del parte.
        """
        def cell_func(column, cell, model, itr, numcol):
            idht = model[itr][-1]
            ht = pclases.HorasTrabajadas.get(idht)
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

    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        # Inicialmente no se muestra NADA. Sólo se le deja al
        # usuario la opción de buscar o crear nuevo.
        self.activar_widgets(False)
        self.wids['b_actualizar'].set_sensitive(False)
        self.wids['b_guardar'].set_sensitive(False)
        self.wids['b_nuevo'].set_sensitive(True)
        self.wids['b_buscar'].set_sensitive(True)
        # Inicialización del resto de widgets:
        # (Nombre, tipo, editable, ordenable, buscable, función_actualización)
        cols = (('Nº. de Palet', 'gobject.TYPE_STRING',
                    False, True, True, None),
                ('# cajas/palé', 'gobject.TYPE_STRING',
                    False, True, False, None),
                ('# bolsas/caja', 'gobject.TYPE_STRING',
                    True, True, False, self.cambiar_numbolsas),
                ('Peso neto', 'gobject.TYPE_STRING',
                    False, True, False, None),
                ('B', "gobject.TYPE_BOOLEAN",
                    True, True, False, self.pasar_pale_a_B),
                ('Observaciones', 'gobject.TYPE_STRING',
                    True, False, False, self.cambiar_observaciones),
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None)
               )
        utils.preparar_treeview(self.wids['tv_produccion'], cols)
        self.wids['tv_produccion'].get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        self.wids['tv_produccion'].add_events(gtk.gdk.BUTTON_PRESS_MASK)
        cols = (('Código', 'gobject.TYPE_INT64', False, True, False, None),
                ('Nombre', 'gobject.TYPE_STRING', False, True, False, None),
                ('Apellidos', 'gobject.TYPE_STRING', False, True, True, None),
                ('Horas', 'gobject.TYPE_STRING', True, True, False,
                    self.cambiar_horas_trabajadas),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_empleados'], cols)
        self.colorear_tabla_empleados()
        cols = (('Producto', 'gobject.TYPE_STRING', False, True, True, None),
                ('Cantidad', 'gobject.TYPE_STRING', False, True, False, None),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_consumos'], cols)
        self.wids['tv_consumos'].get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        cols = (("Tipo de incidencia", "gobject.TYPE_STRING",
                    False, True, False, None),
                 ("Hora de inicio", "gobject.TYPE_STRING",
                    False, True, False, None),
                 ("Hora de finalización", "gobject.TYPE_STRING",
                    False, True, False, None),
                 ("Observaciones", "gobject.TYPE_STRING",
                    False, True, True, None),
                 ("ID", "gobject.TYPE_INT64", False, False, False, None))
        utils.preparar_listview(self.wids['tv_incidencias'], cols)
        self.wids['tv_incidencias'].get_selection().set_mode(
            gtk.SELECTION_MULTIPLE)
        self.wids['ventana'].maximize()

    def cambiar_horas_trabajadas(self, cell, path, newtext):
        newtext = newtext.replace(".", ":").replace(",", ":")
        if ":" not in newtext:
            if len(newtext) < 4:
                newtext = ("0" * (4 - len(newtext))) + newtext
            newtext = "%s:%s" % (newtext[:-2], newtext[-2:])
        model = self.wids['tv_empleados'].get_model()
        iid = model[path][-1]
        ht = pclases.HorasTrabajadas.get(iid)
        try:
            try:
                dtdelta = mx.DateTime.DateTimeDelta(0,
                    float(newtext.split(':')[0]), float(newtext.split(':')[1]),
                    0)
            except IndexError:
                dtdelta = mx.DateTime.DateTimeDelta(0, int(newtext), 0)
                newtext = utils.str_hora_corta(dtdelta)
            if dtdelta > self.objeto.get_duracion():
                utils.dialogo_info(titulo = "TIEMPO INCORRECTO", texto = "El tiempo trabajado no puede superar la\nduración del parte de producción.", padre = self.wids['ventana'])
                return
            ht.horas = newtext
            ht.sync(); ht.syncUpdate()
            model[path][3] = ht.horas.strftime('%H:%M')
        except (ValueError, TypeError):
            utils.dialogo_info(titulo = "ERROR",
                texto = 'El texto "%s" no representa el formato horario.' % (
                            newtext),
            padre = self.wids['ventana'])

    def activar_widgets(self, s):
        """
        Activa o desactiva (sensitive=True/False) todos
        los widgets de la ventana que dependan del
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        s = s and ((self.usuario and self.usuario.nivel <= 2)
                   or not self.objeto.bloqueado or not self.usuario)
        if self.objeto:
            s = s or self.objeto.id == self.__lecturaescritura
        ws = ('hbox1', 'hbox2', 'hbox3', 'tv_produccion', 'hbox7',
              'tv_incidencias', 'hbox8', 'tv_consumos', 'hbox9',
              'table1', 'hbox6')
        for w in ws:
            self.wids[w].set_sensitive(s)
        if self.usuario and self.usuario.nivel > 3: # No permito (des)bloquear.
            self.wids['ch_bloqueado'].set_sensitive(False)
        #if self.usuario:
        #    self.wids['b_partida'].set_sensitive(s and self.usuario.nivel < 3)

    def ir_a_primero(self):
        """
        Pregunta si crear un parte nuevo, de forma que al abrir la ventana
        siempre se pueda empezar un parte de rápidamente.
        Si se contesta que no al diálogo, se va al _último_ registro de la tabla.
        """
        nuevo = False
        if nuevo:
            self.crear_nuevo_partedeproduccion(None)
        else:
            partedeproduccion = self.objeto
            try:
                if partedeproduccion != None:
                    partedeproduccion.notificador.desactivar()
                    # Anulo el aviso de actualización del parte que deja de
                    # ser activo.
                partesdeproduccion = pclases.ParteDeProduccion.select(
                    pclases.ParteDeProduccion.q.partidaCemID != None)  # @UndefinedVariable
                partesdeproduccion = partesdeproduccion.orderBy("-id")
                partedeproduccion = partesdeproduccion[0]
                partedeproduccion.notificador.activar(self.aviso_actualizacion)
                    # Activo la notificación
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
                              utils.str_hora_corta(r.horainicio),
                              utils.str_hora_corta(r.horafin),
                              "CLIC PARA VER",
                              r.observaciones))
        idpartedeproduccion = utils.dialogo_resultado(filas_res,
                        titulo = 'Seleccione parte de línea de envasado',
                        cabeceras = ('ID Interno',
                                     'Fecha',
                                     'Hora inicio',
                                     'Hora fin',
                                     'Partida',
                                     'Observaciones'),
                        func_change = self.mostrar_info_parte,
                        padre = self.wids['ventana'])
        if idpartedeproduccion < 0:
            return None
        else:
            return idpartedeproduccion

    def mostrar_info_parte(self, tv):
        model, itr = tv.get_selection().get_selected()
        if itr!=None and model[itr][-2] == "CLIC PARA VER":
            parte = pclases.ParteDeProduccion.get(model[itr][0])   # En los
                # diálogos de resultado el ID va al revés.
            if parte.es_de_bolsas() and parte.articulos:
                #partida = parte.articulos[0].bolsa.caja.pale.partidaCem.codigo
                partida = parte.partidaCem.codigo
            else:
                partida = 'VACIO'
            producto = (parte.articulos != []
                        and parte.articulos[0].productoVenta.nombre or 'VACÍO')
            model[itr][-2] = "%s (%s)" % (partida, producto)

    def rellenar_widgets(self):
        """
        Introduce la información del partedeproduccion actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a
        esta función en ese caso.
        """
        if not self.objeto:
            self.activar_widgets(False)
            return
        partedeproduccion = self.objeto
        self.wids['ch_bloqueado'].set_active(self.objeto.bloqueado)
        # Información global:
        if self.objeto.articulos != []:
            self.producto = self.objeto.articulos[0].productoVenta
            # Y si no hay, sigo usando el de antes.
        self.rellenar_datos_producto(self.producto)
        self.wids['e_fechaini'].set_text(
            utils.str_fecha(partedeproduccion.fechahorainicio))
        self.wids['e_fechafin'].set_text(
            utils.str_fecha(partedeproduccion.fechahorafin))
        self.wids['e_horaini'].set_text(
            partedeproduccion.horainicio.strftime('%H:%M'))
        self.wids['e_horafin'].set_text(
            partedeproduccion.horafin.strftime('%H:%M'))
        self.wids['e_duracion'].set_text(
            partedeproduccion.get_duracion().strftime('%H:%M'))
        self.wids['txt_observaciones'].get_buffer().set_text(
            partedeproduccion.observaciones)
        self.rellenar_estadisticas()
        # Información de detalle:
        try:
            e_partida = self.objeto.partidaCem.codigo
            mostrar_mensaje_correccion_partidaCem = False
        except AttributeError:
            self.objeto._corregir_partidaCem_nula()
            e_partida = self.objeto.partidaCem.codigo
            mostrar_mensaje_correccion_partidaCem = True
        self.wids['e_partida'].set_text(e_partida)
        self.rellenar_tabla_empleados()
        self.rellenar_tabla_bolsas()
        self.rellenar_tabla_incidencias()
        self.rellenar_tabla_consumos()
        self.objeto.make_swap()
        self.check_permisos()
        if mostrar_mensaje_correccion_partidaCem:
            utils.dialogo_info(titulo = "PARTIDA DE CEMENTO CORREGIDA",
                texto = "La partida de cemento del parte actual contenía \n"
                        "un error o era nula.\n"
                        "Se ha corregido automáticamente. Por favor, \n"
                        "verifique que se corresponde con la partida real.",
                padre = self.wids['ventana'])
            self.objeto.observaciones += "\nPartida corregida automáticamente."
        self.wids['b_back'].set_sensitive(self.objeto and self.objeto.anterior() and 1 or 0)
        self.wids['b_next'].set_sensitive(self.objeto and self.objeto.siguiente() and 1 or 0)

    def rellenar_estadisticas(self):
        partedeproduccion = self.objeto
        # Estadísticas:
        #numbolsas = len(self.objeto.articulos)
        #numbolsas = pclases.ParteDeProduccion._queryOne("""
        #    SELECT COUNT(id)
        #    FROM articulo
        #    WHERE articulo.parte_de_produccion_id = %d""" % self.objeto.id)[0]
        numbolsas=sum([a.caja.numbolsas for a in partedeproduccion.articulos])
        self.wids['e_prod_bolsas'].set_text(str(numbolsas))
        #kilos = sum([a.peso for a in self.objeto.articulos])
        # Optimizando, que es gerundio:
        try:
            #kilos = (len(self.objeto.articulos)
            kilos = (numbolsas
                     * self.producto.camposEspecificosBala.gramosBolsa/1000.0)
        except AttributeError:
            kilos = 0.0
        self.wids['e_prod_kg'].set_text(utils.float2str(kilos, autodec = True))
        cajas = set([a.caja for a in self.objeto.articulos]) # Ojo:python > 2.3
        numcajas = len(cajas)
        # Optimización:
        #sqlpales = pclases.Pale.select(pclases.AND(
        #    pclases.Articulo.q.parteDeProduccionID == self.objeto.id,
        #    pclases.Articulo.q.bolsaID == pclases.Bolsa.q.id,
        #    pclases.Bolsa.q.cajaID == pclases.Caja.q.id,
        #    pclases.Caja.q.paleID == pclases.Pale.q.id))
        #pales = set([p for p in sqlpales])  # Ojo: python > 2.3
        #numcajas = sum(p.numcajas for p in pales)
        self.wids['e_prod_cajas'].set_text(str(numcajas))
        try:
            bolsasminuto = str(numbolsas
                                / partedeproduccion.get_duracion().minutes)
        except ZeroDivisionError:
            bolsasminuto = "inf."
        self.wids['e_bolsasminuto'].set_text(bolsasminuto)
        try:
            kgh=utils.float2str(kilos/partedeproduccion.get_duracion().hours,
                                autodec = True)
        except ZeroDivisionError:
            kgh = "inf."
        self.wids['e_kgh'].set_text(kgh)
        pales = set([a.caja.pale
                     for a in self.objeto.articulos]) # Ojo: python > 2.3
        # numpales = len(pales)
        # Optimizando:
        # numpales = sqlpales.count()   # Sin groupBy salen tantas como bolsas
        numpales = len(pales)
        self.wids['e_prodpales'].set_text(str(numpales))
        try:
            activo = partedeproduccion.get_horas_trabajadas()
        except AssertionError:
            partedeproduccion._corregir_duracion_paradas()
            activo = partedeproduccion.get_horas_trabajadas()
        self.wids['e_activo'].set_text(activo.strftime("%H:%M"))
        pasivo = partedeproduccion.get_horas_paradas()
        self.wids['e_pasivo'].set_text(pasivo.strftime("%H:%M"))
        self.wids['e_bbconsumidos'].set_text(
            utils.float2str(len(self.objeto.bigbags), autodec = True))
        self.wids['e_kgconsumidos'].set_text(
            utils.float2str(sum([bb.pesobigbag for bb in self.objeto.bigbags]),
                            autodec = True))
        try:
            palesa = len(self.objeto.partidaCem.get_pales_a())
            palesb = len(self.objeto.partidaCem.get_pales_b())
        except AttributeError:
            palesa = palesb = 0
        self.wids['e_palesa'].set_text(`palesa`)
        self.wids['e_palesb'].set_text(`palesb`)

    def rellenar_tabla_incidencias(self):
        parte = self.objeto
        tv = self.wids['tv_incidencias']
        if parte != None:
            model = tv.get_model()
            tv.set_model(None)
            model.clear()
            incidencias = pclases.Incidencia.select(
                pclases.Incidencia.q.parteDeProduccionID == self.objeto.id,  # @UndefinedVariable
                orderBy = "horainicio")
            for incidencia in incidencias:
                model.append((incidencia.tipoDeIncidencia.descripcion,
                              utils.str_fechahora(incidencia.horainicio),
                              utils.str_fechahora(incidencia.horafin),
                              incidencia.observaciones,
                              incidencia.id))
            tv.set_model(model)

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
                consumos.sort(lambda c1, c2: c1 != None and c2 != None
                                             and int(c1.id - c2.id) or 0)
            except TypeError, msg:
                self.logger.error("partes_de_fabricacion_bolsas.py (rellenar"
                                  "_tabla_consumos): Error ordenando consumo"
                                  "s (%s):\n%s" % (msg, consumos))
            for c in parte.consumos:
                if c.productoCompraID != None:
                    unidad = c.productoCompra.unidad
                    producto = c.productoCompra.descripcion
                else:
                    unidad = ""
                    producto = ""
                model.append((producto,
                              "%s %s" % (utils.float2str(c.cantidad), unidad),
                              c.id))
            for bb in parte.bigbags:    # Consumos de fibra de cemento:
                str_bb = "{} ({}) {}".format(bb.codigo,
                                             bb.articulo.productoVenta.nombre,
                                             bb.api and "✔" or "✘")
                str_bb = geninformes.sanitize_unicode(str_bb)
                model.append((str_bb,
                              utils.float2str(bb.pesobigbag) + " kg",
                              -bb.id))
            self.wids['tv_consumos'].set_model(model)

    def check_permisos(self):
        if self.__permisos.escritura:  # Puede modificar los partes:
            self.activar_widgets(True)
        else:   # Sólo puede modificar el parte que haya creado nuevo (si es
                # que ha creado alguno)
            if self.__lecturaescritura == (self.objeto.id or
                                           not self.objeto.bloqueado):
                self.activar_widgets(True)
            else:
                self.activar_widgets(False)
        # Compruebo primero este porque habilita o deshabilita todos los
        # botones, incluso los que dependen de los otros dos permisos.
        self.wids['b_buscar'].set_sensitive(self.__permisos.lectura)
        self.wids['b_nuevo'].set_sensitive(self.__permisos.nuevo)

    def rellenar_tabla_bolsas(self):
        model = self.wids['tv_produccion'].get_model()
        model.clear()
        #detallesdeproduccion = self.objeto.articulos[:]
        #detallesdeproduccion.sort(lambda x, y:
        #                           utils.orden_por_campo_o_id(x,y,"fechahora"))
        #detallesdeproduccion = self.objeto.articulos
        detallesdeproduccion = pclases.Articulo.select(
            pclases.Articulo.q.parteDeProduccionID == self.objeto.id,  # @UndefinedVariable
            orderBy = "id")
        # Filas del TreeView
        pales = {}  # Diccionarios de nodos padres (cajas) y abuelos (palés).
        cajas = {}
        self.wids['tv_produccion'].freeze_child_notify()
        self.wids['tv_produccion'].set_model(None)
        for articulo in detallesdeproduccion:
            pale = articulo.caja.pale
            if pale not in pales:   # Inserto palé.
                es_clase_b = pale.es_clase_b()
                pale_api = pale.api
                if pale_api is None:
                    volcado = ""
                elif pale_api:
                    volcado = " ✔"
                else:
                    volcado = " ✘"
                volcado = geninformes.sanitize_unicode(volcado)
                peso_neto = sum([c.articulo.peso_neto for c in pale.cajas])
                numcajas = len(pale.cajas)  # = pale.numcajas
                pales[pale] = model.append(None, ("Palé " + pale.codigo + volcado,
                                                  numcajas,
                                                  pale.numbolsas,
                                                  peso_neto,
                                                  es_clase_b,
                                                  pale.observaciones,
                                                  pale.get_puid()))
            if not self.SHOW_PALES_COMPLETOS:
                continue
            caja = articulo.caja
            if caja not in cajas:
                if caja.articulo.api is None:
                    volcado = ""
                elif caja.articulo:
                    volcado = " ✔"
                else:
                    volcado = " ✘"
                volcado = geninformes.sanitize_unicode(volcado)
                cajas[caja] = model.append(pales[pale], ("Caja " + caja.codigo + volcado,
                                                         1,  # 1 caja por caja:)
                                                         caja.numbolsas,
                                                         caja.peso,
                                                         es_clase_b,
                                                         caja.observaciones,
                                                         caja.get_puid()))
            #pesogramos = "%s gr" % utils.float2str(
            #    bolsa.peso * 1000, autodec = True)
            #model.append(cajas[bolsa.caja],
            #                ("Bolsa " + bolsa.codigo,
            #                 pesogramos,
            #                 bolsa.claseb,
            #                 bolsa.observaciones,
            #                 bolsa.get_puid()))
        self.wids['tv_produccion'].set_model(model)
        self.wids['tv_produccion'].thaw_child_notify()

    def seleccionar_producto(self, boton):
        """
        Selecciona el producto del parte actual.
        Si ya tiene producción, cambia el producto de toda la producción
        de la partida completa.
        """
        a_buscar = utils.dialogo_entrada(titulo="BUSCAR PRODUCTO",
                                         texto="Introduzca el texto a buscar:",
                                         padre=self.wids['ventana'])
        if a_buscar is not None:
            pvs = utils.buscar_productos_venta(a_buscar)
            pvs = [p for p in pvs if p.es_bolsa()]
            if len(pvs):
                if len(pvs) == 1:
                    pv = pvs[0]
                elif len(pvs) > 1:
                    idpv = self.refinar_resultados_busqueda_producto(pvs)
                    if idpv:
                        pv = pclases.ProductoVenta.get(idpv)
                    else:
                        pv = None
                if pv:
                    try:
                        pcem = self.objeto.partidaCem
                        producto_anterior = pcem.pales[0].productoVenta
                    except IndexError:
                        producto_anterior = None
                    if producto_anterior == pv:
                        return
                    if not producto_anterior:
                        producto_anterior = pv
                    if (producto_anterior.camposEspecificosBala.bolsasCaja !=
                            pv.camposEspecificosBala.bolsasCaja or
                        producto_anterior.camposEspecificosBala.cajasPale !=
                            pv.camposEspecificosBala.cajasPale):
                        utils.dialogo_info(
                                titulo="PRODUCTO INCOMPATIBLE",
                                texto="Seleccione un producto con el mismo"
                                "número de bolsas por caja\no elimine primero"
                                " la producción actual, cree una nueva "
                                "partida\n y vuelva a crearla con el nuevo "
                                "producto.",
                                padre=self.wids['ventana'])
                        return
                    titulo = "¿CAMBIAR PRODUCTO AL LOTE COMPLETO?"
                    texto = "Va a cambiar la producción del lote completo de"\
                            " %s\na %s. ¿Está seguro?\n\n"\
                            "(Puede durar bastante. "\
                            "No interrumpa el proceso)" % (
                                    producto_anterior
                                    and producto_anterior.descripcion or "",
                                    pv.descripcion)
                    padre = self.wids['ventana']
                    if (not self.objeto.partidaCem.pales
                            or utils.dialogo(texto, titulo, padre)):
                        ceb = pv.camposEspecificosBala
                        for pale in self.objeto.partidaCem.pales:
                            pale.numcajas = ceb.cajasPale
                            pale.numbolsas = ceb.bolsasCaja
                            pale.sync()
                            for caja in pale.cajas:
                                caja.numbolsas = ceb.bolsasCaja
                                caja.peso = (ceb.bolsasCaja
                                             * ceb.gramosBolsa / 1000)
                                a = caja.articulo
                                a.pesoReal = (caja.peso
                                              + pclases.PESO_EMBALAJE_CAJAS)
                                a.productoVenta = pv
                                a.syncUpdate()
                        self.producto = pv
                        self.rellenar_datos_producto(pv)
                        self.actualizar_ventana()

    def rellenar_datos_producto(self, producto):
        """
        A partir del artículo recibido, completa la información
        de la cabecera del formulario (ancho, etc...) en
        función de los datos de la bolsa.
        También verifica si el parte tiene ficha de fabricación. Si no la
        tiene, pone la del producto recibido.
        """
        if producto == None:
            self.wids['e_producto'].set_text('')
        else:
            nomproducto = "%s. Corte: %d mm. %d gr/bolsa" % (
                producto.descripcion,
                producto.camposEspecificosBala.corte,
                producto.camposEspecificosBala.gramosBolsa)
            self.wids['e_producto'].set_text(nomproducto)

    # --------------- Manejadores de eventos ----------------------------
    def add_pale(self, w):
        """
        Crea un nuevo palé con todas las cajas y bolsas que contiene.
        Si es el primer palé del lote pide el número de bolsas que han
        entrado en la primera de las cajas, si no, toma las del primer
        palé de la PARTIDA (aunque debe coincidir con el parte, pero en el
        caso de que no sea así me curo en salud y procuro desde el principio
        que todos los palés de la misma partida sean idénticos).
        Si el número de bolsas es inferior a 40 se va a crear por defecto
        como B.
        """
        if not MURANO:
            utils.dialogo_info(titulo="ERROR DE CONEXIÓN CON MURANO",
                               texto="No puede crear cajas. Solo consultas.",
                               padre=self.wids['ventana'])
            return
        if not self.producto:
            utils.dialogo_info(titulo = "SELECCIONE UN PRODUCTO",
                texto = "Antes debe seleccionar un producto.",
                padre = self.wids['ventana'])
            return
        partidaCem = self.objeto.partidaCem
        try:
            pale = partidaCem.pales[0]
            defecto = pale.numbolsas
        except IndexError:
            defecto = self.producto.camposEspecificosBala.bolsasCaja
            if not defecto:
                defecto = pclases.Pale.NUMBOLSAS
        texto = "Introduzca el número de bolsas de la primera caja:"
        if self.usuario and self.usuario.nivel <= self.NIVEL_POR_LOTES:
            texto += "\n\n<small>Si introduce una serie de números se\n"\
                     "crearán tantos palés como números haya tecleado;\n"\
                     "cada uno de ellos con las bolsas por caja indicadas."\
                     "</small>"
            numbolsas = utils.dialogo_pedir_rango(
                titulo="¿NÚMERO DE BOLSAS?",
                texto=texto,
                padre=self.wids['ventana'],
                valor_por_defecto=defecto,
                permitir_repetidos=True)
        else:
            numbolsas = utils.dialogo_entrada(titulo = "¿NÚMERO DE BOLSAS?",
                    texto = texto,
                    padre = self.wids['ventana'],
                    valor_por_defecto = defecto)
        if not numbolsas:
            return
        if not self.usuario or self.usuario.nivel > self.NIVEL_POR_LOTES:
            try:
                numbolsas = [int(numbolsas)]
            except:
                utils.dialogo_info(titulo = "NÚMERO INCORRECTO",
                                   texto = 'El texto "%s" no es un número.' % (
                                    numbolsas),
                                   padre = self.wids['ventana'])
                return
        listanumbolsas = numbolsas
        if pclases.DEBUG:
            print listanumbolsas
        pales_a_etiquetar = []
        productoVenta = self.producto
        for numbolsas in listanumbolsas:
            vpro = VentanaProgreso(padre=self.wids['ventana'])
            vpro.mostrar()
            icont = 0.0
            # numcajasdefecto = pclases.Pale.NUMCAJAS
            numcajasdefecto = productoVenta.camposEspecificosBala.cajasPale
            # 1.- Creo el palé.
            numpale, codigo = pclases.Pale.get_next_numpale(numbolsas)
            ahora = mx.DateTime.localtime()
            pale = pclases.Pale(partidaCem=partidaCem,
                                numpale=numpale,
                                codigo=codigo,
                                fechahora=None,
                                numbolsas=numbolsas,
                                numcajas=numcajasdefecto)
            try:
                pale.fechahora = ahora
            except:     # noqa
                pale.fechahora = datetime.datetime.now()
            pclases.Auditoria.nuevo(pale, self.usuario, __file__)
            # 2.- Creo las cajas.
            tot = pale.numcajas
            for i in range(pale.numcajas):  # @UnusedVariable
                numcaja, codigo = pclases.Caja.get_next_numcaja()
                vpro.set_valor(icont / tot, "Creando caja %s..." % codigo)
                try:
                    gramos = productoVenta.camposEspecificosBala.gramosBolsa
                except AttributeError:
                    gramos = 0
                peso_neto = (gramos * numbolsas) / 1000.0
                # peso = peso_bruto = peso_neto + 0.150 + 0.100  # Palé+cartón
                caja = pclases.Caja(pale=pale,
                                    numcaja=numcaja,
                                    codigo=codigo,
                                    fechahora=None,
                                    peso=peso_neto,
                                    numbolsas=numbolsas)
                try:
                    caja.fechahora = mx.DateTime.localtime()
                except:     # noqa
                    caja.fechahora = datetime.datetime.now()
                pclases.Auditoria.nuevo(caja, self.usuario, __file__)
                articulo = pclases.Articulo(parteDeProduccion=self.objeto,
                            caja = caja,
                            rolloDefectuoso = None,
                            albaranSalida = None,
                            productoVenta = self.producto,
                            bala = None,
                            rollo = None,
                            bigbag = None,
                            almacen = pclases.Almacen.get_almacen_principal(),
                            rolloC = None,
                            balaCable = None)
                pclases.Auditoria.nuevo(articulo, self.usuario, __file__)
                # DONE: Al final sí que está volcando. Pero va tan sumamente
                # lento caja a caja que parece que se cuelga. Además la salida
                # por consola no está habilitada, con lo que al final el error
                # que da es por algún print de depuración que hay por ahí.
                # try:
                #     murano.ops.create_articulo(articulo)
                # except IOError:
                #     pass    # Alguna movida con la salida por consola de
                #     # depuración y no está disponible.
                icont += 1
            # 3.- Creo el palé en Murano
            vpro.set_valor(icont / tot,
                           "Creando palé {}...".format(pale.codigo))
            # murano.ops.create_pale(pale, observaciones="")
            # OJO: Le paso el último artículo porque la formulación de esta
            # línea será por PALÉS COMPLETOS.
            pales_a_etiquetar.append(pale)
            vpro.ocultar()
            descontar_material_adicional(self, articulo)
            self.objeto.buscar_o_crear_albaran_interno(
                incluir_consumos_auto = True) # Normalmente no, pero
                # aquí sí quiero que aparezcan en el alb. interno.
        imprimir_etiquetas_pales(pales_a_etiquetar, self.wids['ventana'],
                                 mostrar_dialogo = False)
        self.rellenar_tabla_consumos()
        self.rellenar_tabla_bolsas()
        self.rellenar_estadisticas()

    def seleccionar_partida(self, w):
        """
        Wrapper para cambiar_partida.
        """
        self.cambiar_partida(w)

    def _salir(self, w, event = None):
        if (self.__permisos.escritura
            and self.objeto
            and not self.objeto.bloqueado
            and self.objeto.fecha < mx.DateTime.localtime()-mx.DateTime.oneDay
            and (not self.usuario or self.usuario.nivel <= 2)
           ):  # Tiene permiso para bloquear el parte
            res = utils.dialogo(titulo = "DEBE VERIFICAR EL PARTE",
                                texto = "Antes de cerrar el parte debe verifi"
                                        "carlo.\n¿Marcar como verificado?",
                                padre = self.wids['ventana'],
                                bloq_temp = ["Sí"])

            self.objeto.bloqueado = res
            self.wids['ch_bloqueado'].set_active(self.objeto.bloqueado)
            # return True
        if not self.salir(w, mostrar_ventana = event == None):
            # Devuelve True cuando se cancela el cierre de la ventana (por
            # temas de event-chain).
            try:
                padre = self.wids['ventana']
            except KeyError:
                padre = None
            vpro = VentanaActividad(texto="Comprobando disparo de alertas...",
                                    padre = padre)
            vpro.mostrar()
            if not self.linea:
                linea = pclases.LineaDeProduccion.select(
                  pclases.LineaDeProduccion.q.nombre.contains('de embolsado'))  # @UndefinedVariable
                self.linea = linea
            vpro.mover()
            if self.linea == None:
                txt = "WARNING: La línea de embolsado no está correctamente "\
                      "dada de alta."
                print txt
                self.logger.warning(txt)
            else:
                vpro.mover()
                formulacion = self.linea.formulacion
                if not formulacion:
                    # TODO: Dar mensaje de error por logger
                    pass
                else:
                    for ca in [ca_con_p for ca_con_p
                               in formulacion.consumosAdicionales
                               if ca_con_p.productoCompra != None]:
                        vpro.mover()
                        # Verifico que no haya productos bajo mínimos:
                        if ca.productoCompra.existencias < ca.productoCompra.minimo:
                            vpro.mover()
                            try:
                                v = pclases.Ventana.select(pclases.Ventana.q.fichero == "pedidos_de_compra.py")[0]  # @UndefinedVariable
                            except IndexError:
                                txt = "WARNING: ¡La ventana de pedidos de compra "\
                                      "SE HA PERDIDO!"
                                print txt
                                self.logger.warning(txt)
                            mensaje = "El producto %s tiene las existencias bajo "\
                                      "mínimos. Considere hacer un pedido de comp"\
                                      "ra." % ca.productoCompra.descripcion
                            for u in [p.usuario for p in v.permisos if p.nuevo]:
                                vpro.mover()
                                u.enviar_mensaje(mensaje)
                        # Y Verifico que no haya existencias negativas:
                        if ca.productoCompra.existencias < 0:
                            vpro.mover()
                            try:
                                v = pclases.Ventana.select(pclases.Ventana.q.fichero == "pedidos_de_compra.py")[0]  # @UndefinedVariable
                            except IndexError:
                                print "WARNING: ¡La ventana de pedidos de compra SE HA PERDIDO!"
                                self.logger.error("partes_de_fabricacion_rollos: ¡La ventana de pedidos de compra SE HA PERDIDO!")
                            vpro.mover()
                            mensaje = "El producto %s tiene existencias NEGATIVAS. Corrija el error lo antes posible." % ca.productoCompra.descripcion
                            for u in [p.usuario for p in v.permisos if p.nuevo]:
                                vpro.mover()
                                u.enviar_mensaje(mensaje)
            vpro.mover()
            vpro.ocultar()

    def cambiar_observaciones(self, cell, path, newtext):
        """
        Solo cambia las observaciones del objeto. NO PASA A PRODUCTO B.
        """
        model = self.wids['tv_produccion'].get_model()
        puid = model[path][-1]
        clase, aidi = puid.split(":")
        objeto = getattr(pclases, clase).get(int(aidi))
        objeto.observaciones = newtext
        model[path][5] = newtext

    def crear_nuevo_partedeproduccion(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        partedeproduccion = self.objeto
        if not utils.dialogo('Se creará un nuevo parte de producción vacío.',
                             'NUEVO PARTE',
                             padre = self.wids['ventana']):
            return
        if partedeproduccion != None:
            partedeproduccion.notificador.desactivar()
        partedeproduccion = pclases.ParteDeProduccion(fecha = mx.DateTime.localtime(),
            horainicio = time.struct_time(time.localtime()[:4]
                                          + (0,0)
                                          + time.localtime()[6:]),
            horafin = time.struct_time(time.localtime()[:3]
                                       +((time.localtime()[3]+8)%24, 0,0)
                                       +time.localtime()[6:]),
            prodestandar = 0,
            observaciones = '',
            bloqueado = False,
            partidaCem = pclases.PartidaCem.get_nueva_o_ultima_vacia(),
            merma = 0.0)
        pclases.Auditoria.nuevo(partedeproduccion, self.usuario, __file__)
        partedeproduccion._corregir_campos_fechahora()
        self.objeto = partedeproduccion
        self.wids['e_partida'].set_text(self.objeto.partidaCem.codigo)
        self.add_empleados_calendario()
        self.__lecturaescritura = self.objeto.id
        self.actualizar_ventana()
        self.objeto.notificador.activar(self.aviso_actualizacion)
        verificar_solapamiento(partedeproduccion, self.wids['ventana'])

    def refinar_resultados_busqueda_producto(self, resultados):
        """
        Muestra en una ventana de resultados todos los
        registros de "resultados".
        Devuelve el id (primera columna de la ventana
        de resultados) de la fila seleccionada o None
        si se canceló.
        """
        filas_res = []
        for r in resultados:
            filas_res.append((r.id, r.codigo, r.nombre, r.descripcion))
        idproducto = utils.dialogo_resultado(filas_res,
            titulo = 'Seleccione producto',
            cabeceras = ('ID Interno', 'Código','Nombre', 'Descripción'),
            padre = self.wids['ventana'])
        if idproducto < 0:
            return None
        else:
            return idproducto

    def buscar_partedeproduccion(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        PRECONDICION: Los partes de embolsado SIEMPRE deben tener una
        partida de cemento relacionada.
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
                    if len(a_buscar.split('/')[-1]) == 2:
                        fecha = time.strptime(a_buscar, '%d/%m/%y')
                    else:
                        fecha = time.strptime(a_buscar, '%d/%m/%Y')
                    resultados = pclases.ParteDeProduccion.select(
                        pclases.AND(pclases.ParteDeProduccion.q.fecha==fecha,  # @UndefinedVariable
                            pclases.ParteDeProduccion.q.partidaCemID != None))  # @UndefinedVariable
                else:
                    resultados = pclases.ParteDeProduccion.select(
                        pclases.ParteDeProduccion.q.partidaCemID != None)  # @UndefinedVariable
            except:
                producto = pclases.ProductoVenta.select(pclases.AND(
                    pclases.ProductoVenta.q.nombre.contains(a_buscar),  # @UndefinedVariable
                    pclases.ProductoVenta.q.camposEspecificosBalaID != None))  # @UndefinedVariable
                producto = pclases.SQLtuple(
                                [p for p in producto if p.es_bolsa()])
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
                        for p in resultados:
                            if (p.articulos != [] and
                                p.articulos[0].productoVentaID == idproducto):
                                partes.append(p)
                            vpro.set_valor(i/tot, 'Buscando partes')
                            i += 1
                    else:
                        vpro.ocultar()
                        return
                elif producto.count() == 1:
                    for p in resultados:
                        if (p.articulos != [] and
                            p.articulos[0].productoVentaID == producto[0].id):
                            partes.append(p)
                        vpro.set_valor(i/tot, 'Buscando partes')
                        i += 1
                else:
                    for p in resultados:
                        if p.es_de_bolsas():
                            partes.append(p)
                        vpro.set_valor(i/tot, 'Buscando partes')
                        i += 1
                vpro.ocultar()
                resultados = partes
            try:
                len_resultados = len(resultados)
            except:
                len_resultados = resultados.count()
            if len_resultados > 1:
                ## Refinar los resultados
                idpartedeproduccion = self.refinar_resultados_busqueda(
                                        resultados)
                if idpartedeproduccion == None:
                    return
                resultados=[pclases.ParteDeProduccion.get(idpartedeproduccion)]
            elif len_resultados < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info('SIN RESULTADOS',
                    'La búsqueda no produjo resultados.\nPruebe a cambiar el '\
                    'texto buscado o déjelo en blanco para ver una lista comp'\
                    'leta.\n(Atención: Ver la lista completa puede resultar l'\
                    'ento si el número de elementos es muy alto)',
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
                    texto = "Se produjo un error al recuperar la información"\
                            ".\nCierre y vuelva a abrir la aplicación antes "\
                            "de volver a intentarlo.",
                    padre = self.wids['ventana'])
                return
            # Y activo la función de notificación:
            partedeproduccion.notificador.activar(self.aviso_actualizacion)
            self.objeto = partedeproduccion
            # Reinicio preferencias de etiqueta.
            global MEMENTO_MORI
            MEMENTO_MORI = {'que_imprimir': None, 'tipo': None}
            self.actualizar_ventana()

    def guardar(self, widget):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        partedeproduccion = self.objeto
        valores = self.leer_valores_ventana()
        if valores["fechahorainicio"] > valores["fechahorafin"]:
            self.wids['e_fechafin'].set_text(
                self.wids['e_fechaini'].get_text())
            self.wids['e_horafin'].set_text(
                self.wids['e_horaini'].get_text())
            valores = self.leer_valores_ventana()
        ye_olde_fecha = partedeproduccion.fecha
        ye_olde_horainicio = utils.str_hora_corta(partedeproduccion.horainicio)
        ye_olde_horafin = utils.str_hora_corta(partedeproduccion.horafin)
        # Desactivo el notificador momentáneamente
        partedeproduccion.notificador.activar(lambda: None)
        # Actualizo los datos del objeto
        for campo in valores:
            try:
                if (isinstance(valores[campo],
                               type(mx.DateTime.DateTimeDelta(0))) and
                    isinstance(getattr(self.objeto, campo),
                               type(datetime.time()))):
                    # Hay un bug con el mx de Python 2.7 en Windows y tengo
                    # que hacer esta conversión a mano:
                    valores[campo] = datetime.time(valores[campo].hour,
                                                   valores[campo].minute)
                setattr(self.objeto, campo, valores[campo])
            except ValueError:
                if isinstance(valores[campo], mx.DateTime.DateTimeDeltaType):
                    setattr(self.objeto,campo,valores[campo].strftime("%H:%M"))
        # partedeproduccion._corregir_campos_fechahora() <-- Aquí no hace falta
        # Verificación de que no se solapa con otros partes:
        verificar_solapamiento(partedeproduccion,
                               self.wids['ventana'],    # <- Esto es horrible.
                               ye_olde_fecha,
                               ye_olde_horainicio,
                               ye_olde_horafin)
        # Fuerzo la actualización de la BD y no espero a que SQLObject lo haga
        # por mí:
        partedeproduccion.sync()
        # Vuelvo a activar el notificador
        partedeproduccion.notificador.activar(self.aviso_actualizacion)
        self.actualizar_ventana()
        self.wids['b_guardar'].set_sensitive(False)

    def borrar_parte(self, boton):
        if not self.objeto:
            return
        if not utils.dialogo('Se va a intentar eliminar el parte actual.\nSi '\
                             'hay operaciones complejas implicadas se cancela'\
                             'rá el borrado.\nDe cualquier forma, no se acons'\
                             'eja eliminar ningún parte que ya tenga producci'\
                             'ón relacionada.\n¿Está seguro de borrar el part'\
                             'e actual?',
                             'ELIMINAR PARTE',
                             padre = self.wids['ventana']):
            return
        partedeproduccion = self.objeto
        partedeproduccion.notificador.desactivar()
        try:
            partedeproduccion.destroy(ventana = __file__)
        except:
            utils.dialogo_info('PARTE NO BORRADO',
                'El parte no se eliminó.\nSi tiene bolsas o empleados asociad'\
                'os, trate primero de eliminarlos y vuelva a intentarlo.',
                padre = self.wids['ventana'])
            return
        self.ir_a_primero()

    def add_incidencia(self, boton):
        ii = pclases.TipoDeIncidencia.select()
        idincidencia = utils.dialogo_combo('SELECCIONE UN TIPO DE INCIDENCIA',
                'Seleccione un tipo de incidencia del desplegable inferior',
                [(i.id, i.descripcion) for i in ii],
                padre = self.wids['ventana'])
        if idincidencia == None:
            return
        utils.dialogo_info('HORA INICIO',
            'A continuación seleccione la hora de inicio de la incidencia.',
            padre = self.wids['ventana'])
        horaini = utils.mostrar_hora(time.localtime()[3], 0, 0, 'HORA INICIO')
        if not horaini:
            return
        utils.dialogo_info('HORA FIN',
            'A continuación seleccione la hora de finalización de la incide'\
            'ncia.',
            padre = self.wids['ventana'])
        horafin = utils.mostrar_hora(time.localtime()[3], 0, 0, 'HORA FIN')
        if not horafin:
            return
        self.objeto.sync()
        horaini = mx.DateTime.DateTimeFrom(year = self.objeto.fecha.year,
                                           month = self.objeto.fecha.month,
                                           day = self.objeto.fecha.day,
                                           hour = int(horaini.split(":")[0]),
                                           minute = int(horaini.split(":")[1]))
        horafin = mx.DateTime.DateTimeFrom(year = self.objeto.fecha.year,
                                           month = self.objeto.fecha.month,
                                           day = self.objeto.fecha.day,
                                           hour = int(horafin.split(":")[0]),
                                           minute = int(horafin.split(":")[1]))
        if horaini > horafin:
            horafin += mx.DateTime.oneDay
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
            #self.actualizar_ventana()
            self.rellenar_tabla_incidencias()
            self.rellenar_estadisticas()
        else:
            utils.dialogo_info(titulo = 'ERROR HORARIO',
                texto = 'La franja horaria que ha seleccionado no entra en '\
                        'el turno del parte.',
                padre = self.wids['ventana'])

    def drop_pale(self, boton):
        """
        Elimina el palé, sus cajas, bolsas y consumos relacionados.
        """
        if not self.usuario or self.usuario.nivel > 1:
            utils.dialogo_info(titulo="PERMISOS INSUFICIENTES",
                    texto="No puede borrar artículos fabricados.\n\n"
                          "Solicite su eliminación por escrito indicando\n"
                          "claramente los motivos y el código de\n"
                          "trazabilidad del artículo en cuestión.",
                    padre=self.wids['ventana'])
            return
        if not MURANO:
            utils.dialogo_info(titulo="ERROR DE CONEXIÓN CON MURANO",
                               texto="No puede eliminar cajas. Solo consultas.",
                               padre=self.wids['ventana'])
            return
        model, paths = self.wids['tv_produccion'].get_selection().\
                                                            get_selected_rows()
        if (not paths or
            not utils.dialogo(titulo = "¿ESTÁ SEGURO?",
                    texto = "Se van a eliminar %d líneas. ¿Desea continuar?"%(
                        len(paths)),
                    padre = self.wids['ventana'])):
            return
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        icont = 0
        tot = len(paths)
        error = False
        for path in paths:
            puid = model[path][-1]
            vpro.set_valor(icont / tot, "Eliminando %s..." % puid)
            clase, aidi = puid.split(":")
            objeto = getattr(pclases, clase).get(int(aidi))
            if isinstance(objeto, pclases.Pale):
                try:
                    articulo = objeto.cajas[0].articulo
                except IndexError:
                    # Si el palé está vacío, artículo será None
                    articulo = None
            elif isinstance(objeto, pclases.Caja):
                articulo = objeto.articulo
            if articulo:
                # OJO: Le paso el último artículo porque la formulación de
                # esta línea es por PALÉS COMPLETOS.
                descontar_material_adicional(self, articulo, restar = False)
            try:
                # murano.ops.delete_articulo(objeto)
                objeto.destroy_en_cascada(ventana = __file__)
            except IOError:
                pass    # No tenemos consola para sacar los mensajes de debug.
            except Exception, msg:
                vpro.ocultar()
                error = True
                utils.dialogo_info(titulo = "ERROR AL ELIMINAR",
                    texto = "Ocurrió un error al eliminar la producción.\n\n\n"
                            "Información de depuración:\n"
                            "PUID: %s\n"
                            "Mensaje de la excepción:\n%s" % (objeto.get_puid(),
                                                              msg),
                    padre = self.wids['ventana'])
                break   # Paso de seguir con los demás paths (si los hubiera)
            icont += 1
        if not error:
            vpro.ocultar()
        if paths:
            self.rellenar_tabla_consumos()
            self.rellenar_tabla_bolsas()
            self.rellenar_estadisticas()

    def drop_incidencia(self, boton):
        model, paths = self.wids['tv_incidencias'].get_selection().get_selected_rows()
        if paths == None or paths == []:
            utils.dialogo_info('INCIDENCIA NO SELECCIONADA',
                'Debe seleccionar la incidencia que desee eliminar del parte.',
                padre = self.wids['ventana'])
        else:
            if not utils.dialogo('¿Eliminar del parte?',
                                 'BORRAR INCIDENCIAS DE CONTROL DE PRODUCCIÓN',
                                 padre = self.wids['ventana']):
                return
            for path in paths:
                aidi = model[path][-1]
                incidencia = pclases.Incidencia.get(aidi)
                incidencia.parteDeProduccion = None
                try:
                    incidencia.destroy(ventana = __file__)
                except:
                    utils.dialogo_info(titulo = 'INCIDENCIA NO ELIMINADA',
                                       texto = 'Ocurrió un error al intentar '\
                                               'eliminar la incidencia.',
                                       padre = self.wids['ventana'])
            self.actualizar_ventana()

    def add_empleado(self, w):
        empleados = pclases.Empleado.select(pclases.AND(
                pclases.Empleado.q.activo == True,  # @UndefinedVariable
                pclases.Empleado.q.planta == True),  # @UndefinedVariable
            orderBy = 'apellidos')
        empleados = [(e.id, e.nombre, e.apellidos) for e in empleados
                     if e.planta and
                        e.activo and
                        e.categoriaLaboral and
                        e.categoriaLaboral.planta]
                        # e.categoriaLaboral.planta and \
                        # e.categoriaLaboral.lineaDeProduccion == self.linea)]
        ids = utils.dialogo_resultado(filas = empleados,
                                      titulo = 'SELECCIONE EMPLEADOS',
                                      cabeceras = ('ID','Nombre','Apellidos'),
                                      multi = True,
                                      padre = self.wids['ventana'])
        if ids == [-1]:
            return
        for ide in ids:
            try:
                e = pclases.Empleado.get(ide)
                self.objeto.addEmpleado(e)
            except Exception, msg:
                utils.dialogo_info(titulo = 'NÚMERO INCORRECTO',
                        texto = 'El empleado con código identificador %s no '\
                                'existe o no se pudo agregar.\n\n'
                                'Información de depuración:\n'
                                '\t%s' % (ide, msg),
                        padre = self.wids['ventana'])
        self.rellenar_tabla_empleados()

    def drop_empleado(self, w):
        if self.wids['tv_empleados'].get_selection().count_selected_rows()==0:
            return
        model, path = self.wids['tv_empleados'].get_selection().get_selected()
        ide = model[path][0]     # El ide del empleado es la columna 0
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
                          ht.horas.strftime('%H:%M'),
                          ht.id))

    def cambiar_partida(self, w):
        """
        Pide un número de partida por teclado y cambia a él.
        """
        texto = """
        Al cambiar la partida del parte, se cambiará la partida de
        todos los productos relacionados con él, así como el artículo
        al que pertencen los productos.
        Si quiere comenzar la producción de una nueva partida sin afectar
        a los ya existentes, cree un nuevo parte."""
        if (self.objeto.articulos != []
            and not utils.dialogo(titulo = '¿ESTÁ SEGURO?',
                                  texto = texto,
                                  padre = self.wids['ventana'])):
            return
        codigo = utils.dialogo_entrada(titulo = '¿NÚMERO DE PARTIDA?',
                    texto = 'Introduzca el número de partida de embolsado'\
                            ' a producir:',
                    padre = self.wids['ventana'])
        if codigo == None:  # Cancel
            return
        ultima_partida = pclases.PartidaCem.get_nueva_o_ultima_vacia()
        try:
            codigo = utils.parse_numero(codigo.upper().replace(
                pclases.PREFIJO_PARTIDACEM, ""))
            partida = pclases.PartidaCem.select(
                        pclases.PartidaCem.q.numpartida == codigo)[0]  # @UndefinedVariable
            if (self.usuario and self.usuario.nivel > 2
                and partida.numpartida > ultima_partida):
                utils.dialogo_info(titulo = "NÚMERO DE PARTIDA INCORRECTO",
                    texto = "El número de partida %d es superior al de la "
                            "última partida válida para producir: %d\n"
                            "Vuelva a seleccionar partida." % (
                                ultima_partida.numpartida, codigo),
                    padre = self.wids['ventana'])
                return
        except (TypeError, ValueError), msg:
            self.logger.error("partes_de_fabricacion_bolsas::cambiar_partida "\
                              "-> Código partida: %s. Excepción capturada: %s"
                              % (codigo, msg))
            return
        except IndexError:
            if not self.usuario or self.usuario.nivel <= 2:
                partida = pclases.PartidaCem(numpartida = codigo,
                                             codigo = "M-%d" % codigo)
                pclases.Auditoria.nuevo(partida, self.usuario, __file__)
            else:
                danextone = ultima_partida
                if danextone:
                    danextone = danextone.codigo
                else:
                    danextone = "¡no encontrada!"
                if utils.dialogo(titulo = "PARTIDA NO ENCONTRADA",
                    texto = "No se encontró la partida.\n¿Continuar con la"
                            " siguiente partida de embolsado de cemento sin"
                            " \nproducción no asignada a ningún otro parte"
                            " (%s)?" % danextone,
                    padre = self.wids['ventana'],
                    defecto = True,
                    tiempo = 15):
                    partida = ultima_partida
                else:
                    return
        # Pongo la partida como actual.
        self.objeto.partidaCem = partida
        self.wids['e_partida'].set_text(partida.codigo)
        if partida.pales: # Ya tiene algún palé asociado de un parte anterior.
            # Para no mezclar productos, cambio el del parte actual.
            productoVenta = partida.pales[0].cajas[0].articulo.productoVenta
            self.producto = productoVenta
            self.rellenar_datos_producto(self.producto)
        # Y cambio de partida los artículos y de producto de venta.
        pales = []
        for a in self.objeto.articulos:
            a.productoVenta = self.producto
            pale = a.caja.pale
            if pale not in pales:
                pales.append(a.caja.pale)
                pale.partidaCem = partida
        self.actualizar_ventana()

    def get_partida(self):
        """
        Devuelve la partida relacionada con el parte actual.
        Si no hay partida definida devuelve None.
        """
        numpartida = self.wids['e_partida_gtx'].get_text()
        numpartida = numpartida.upper().replace(pclases.PREFIJO_PARTIDACEM, "")
        numpartida = int(numpartida)
        return pclases.PartidaCem.select(
            pclases.PartidaCem.q.numpartida == numpartida)[0]   # @UndefinedVariable
            # Debe existir en la BD por fuerza, "óyenme", por fuerza.

    def _DEPRECATED_bloquear(self, ch, mostrar_alerta = True):
        # Si el parte tiene menos de un día y se encuentra bloqueado, dejo
        # que lo pueda desbloquear cualquiera.
        if (mx.DateTime.localtime() - self.objeto.fecha <= mx.DateTime.oneDay
            and (self.objeto.bloqueado or ch.get_active())):
            self.objeto.bloqueado = False
        elif ch.get_active() != self.objeto.bloqueado:
            # NEW!: Los partes bloqueados solo los pueden desbloquear
            # usuarios con nivel <= 1.
            if self.objeto.bloqueado:
                if self.usuario and self.usuario.nivel <= 2: # and self.objeto.bloqueado and not ch.get_active():
                    self.objeto.bloqueado = False
            else:
                if self.__permisos.escritura:   # Tiene permiso para bloquear
                                                # el parte
                    self.objeto.bloqueado = True
                else:
                    if mostrar_alerta:
                        utils.dialogo_info(titulo = "USUARIO SIN PRIVILEGIOS",
                            texto = "No tiene permisos suficientes para bloq"\
                                    "uear y verificar partes de producción.",
                            padre = self.wids['ventana'])
        self.objeto.sync()
        self.objeto.make_swap()
        ch.set_active(self.objeto.bloqueado)

    def bloquear(self, ch, mostrar_alerta=True):
        """
        - Si el usuario no tiene permisos y mostrar_alerta, avisa de que no
          puede modificar la verificación del parte.
        - Si el usuario tiene permisos,
            - Si el parte está verificado y mostrar_alerta, informa de que no
              se puede desbloquear un parte ya volcado a Murano.
            - Si el parte no está verificado, lo bloquea y vuelca tanto la
              producción como los consumos. Si mostrar_alerta, avisa de que
              es una operación que no se puede deshacer.
        El usuario debe tener nivel 2 o inferior.
        """
        if self.objeto and ch.get_active() != self.objeto.bloqueado:
            # No es la propia ventana la que está marcando la casilla al mostrar
            # un parte bloqueado. El usuario el que ha hecho clic.
            if (self.usuario and self.usuario.nivel <= 3
                    and self.__permisos.escritura):
                if self.objeto.bloqueado:
                    # Ya está bloqueado. **No se puede desbloquear.** Los rollos
                    # puede que incluso ya se hayan vendido en Murano.
                    utils.dialogo_info(titulo="OPERACIÓN NO PERMITIDA",
                            texto="No se pueden desbloquear partes ya volcados "
                                  "a Murano.",
                            padre=self.wids['ventana'])
                else:
                    if mostrar_alerta:
                        seguro = utils.dialogo(titulo="¿VERIFICAR PARTE?",
                                texto="Se verificará el parte y se bloqueará.\n"
                                "Toda la producción y consumos se volcarán a "
                                "Murano.\n\n"
                                "¿Está completamente seguro?\n\n"
                                "(Esta operación no se puede deshacer)",
                                padre = self.wids['ventana'])
                    else:
                        seguro = True
                    if seguro:
                        # Porque Mr. Soy-demasiado-listo-para-esperar me tiene hasta los...
                        finparte = utils.convertir_a_fechahora(
                                self.objeto.fechahorafin)
                        ahora = mx.DateTime.now()
                        parte_terminado = ahora - finparte > 0
                        sensitive = self.wids['ch_bloqueado'].get_sensitive()
                        activo = sensitive and parte_terminado
                        # Impido verificar si el parte está abierto en
                        # producción todavía. Tiene que pasar al menos 1
                        # segundo desde la hora de fin de parte.
                        if not activo:
                            utils.dialogo_info(titulo="HOLA, MARTY",
                                texto="No se puede cerrar un parte que todavía"
                                      " no ha terminado de fabricarse.\n\n\n"
                                      "(Y, por favor, si se te pregunta si "
                                      "estás seguro, mejor que estés seguro "
                                      "de verdad)",
                                padre=self.wids['ventana'])
                        else:
                            res = self.volcar_produccion()
                            if res:
                                self.objeto.bloqueado = True
                                self.objeto.sync()
                                self.objeto.make_swap()
                            else:
                                if mostrar_alerta:
                                    str_error = "No se pudo volcar toda la "\
                                    "producción a Murano.\n\n"\
                                    "Los artículos no volcados se han marcado"\
                                    " con el símbolo «✘».\n"\
                                    "Inténtelo más tarde o contacte con el "\
                                    "administrador.\nEl parte quedará "\
                                    "pendiente de verificar mientras tanto."
                                    utils.dialogo_info(titulo="ERROR VOLCADO",
                                            texto=str_error,
                                            padre=self.wids['ventana'])
                            self.rellenar_widgets()
            else:
                if mostrar_alerta:
                    utils.dialogo_info(titulo = "USUARIO SIN PRIVILEGIOS",
                            texto = "No tiene permisos suficientes para "
                                    "bloquear y verificar partes de "
                                    "producción.\nPruebe a hacerlo desde "
                                    "la ventana de partes pendientes de "
                                    "verificar.",
                            padre = self.wids['ventana'])
            ch.set_active(self.objeto.bloqueado)

    def volcar_produccion(self):
        """
        Vuelca todos los artículos del parte y consumos relacionados a Murano.
        Devuelve True si todo ha ido bien o False si ocurrió algún error.
        Vuelca también los consumos del parte.
        """
        res = True
        if not MURANO:
            utils.dialogo_info(titulo="ERROR CONEXIÓN MURANO",
                    texto="No hay conexión con Murano. Se aborta operación.",
                    padre=self.wids['ventana'])
        else:
            # Producción ===
            vpro = VentanaProgreso(padre=self.wids['ventana'])
            vpro.mostrar()
            i = 0.0
            no_volcados = list(set([a.caja.pale for a in self.objeto.articulos
                                    if not a.api]))
            tot = len(no_volcados)
            for pale in no_volcados:
                i += 1
                vpro.set_valor(i/tot, 'Volcando palé {} ({}/{})'.format(
                    pale.codigo, int(i), tot))
                try:
                    volcado = murano.ops.create_pale(pale, observaciones="")
                    res = res and volcado
                except:
                    res = False
            vpro.ocultar()
            # Consumos ===
            vpro = VentanaProgreso(padre=self.wids['ventana'])
            vpro.mostrar()
            consumos = [c for c in self.objeto.consumos
                        if not c.api and c.actualizado]
            i = 0.0
            tot = len(consumos) + len(self.objeto.bigbags)
            # # consumos materiales
            for consumo in consumos:
                i += 1
                vpro.set_valor(i/tot, 'Consumiendo {} ({}/{})'.format(
                    consumo.productoCompra.descripcion, int(i), tot))
                try:
                    consumido = murano.ops.consumir(consumo.productoCompra,
                                                    consumo.cantidad,
                                                    consumo=consumo)
                    res = res and consumido
                except:
                    res = False
            # # consumos materia prima (bigbags)
            for bigbag in bigbags:
                i += 1
                vpro.set_valor(i/tot, 'Consumiendo materia prima ({})'.format(
                    bigbag.codigo))
                try:
                    consumido = murano.ops.consume_bigbag(bigbag)
                    res = res and consumido
                except:
                    res = False
            vpro.ocultar()
        return res

    def add_empleados_calendario(self):
        """
        Añade los empleados planificados según el calendario laboral
        para la línea de producción.
        1.- Obtener el calendario para self.linea.
        2.- Obtener los laborables del calendario correspondiente a la fecha del objeto.
        3.- Filtrar los laborables en función del turno correspondiente a la hora del objeto.
        4.- Obtener los empleados del laborable resultante.
        5.- Eliminar los empleados actuales. (PREGUNTA ANTES DE HACERLO)
        6.- Insertarlos los nuevos en el parte.
        """
        if self.linea != None:
            idldp = self.linea.id
            CAL = pclases.CalendarioLaboral
            calendarios = CAL.select("""linea_de_produccion_id = %d AND
                                        date_part('month', mes_anno) = %d AND
                                        date_part('year', mes_anno) = %d""" \
                                        % (idldp, self.objeto.fecha.month,
                                           self.objeto.fecha.year))
            if calendarios.count() == 1:
                calendario = calendarios[0]
                empleados = self.get_empleados_de_calendario(calendario)
                # Si hay empleados
                if self.objeto.horasTrabajadas != []:
                    # Si no son los mismos del calendario y los quiere borrar.
                    if ([ht.empleado
                         for ht in self.objeto.horasTrabajadas] != empleados
                       and utils.dialogo(titulo = "¿ELIMINAR OPERARIOS?",
                            texto = "El parte ya tiene empleados relacionado"\
                                    "s.\n¿Desea eliminarlos y asociar los de"\
                                    "finidos en el turno?",
                            padre = self.wids['ventana'])):
                        for ht in self.objeto.horasTrabajadas:
                            self.objeto.removeEmpleado(ht.empleado)
                    else:
                        # Si no los quiere borrar, cancelo todo.
                        return
                # Si no había empleados o no eran los mismos y los ha borrado.
                # Añado empleados de los laborables que cumplan el turno y
                # sean de producción (no-recuperación).
                for empleado in empleados:
                    self.objeto.addEmpleado(empleado)
            elif calendarios.count() > 1:
                self.logger.error("partes_de_fabricacion_bolsas.py -> Existe"
                    " más de un calendario laboral para el mes, año y línea "
                    "de producción: fecha %s - idldp %d - idparte %s." % (
                        self.objeto.fecha, idldp, self.objeto.id))

    def get_empleados_de_calendario(self, calendario):
        res = []
        LAB = pclases.Laborable
        dia_lab_parte = self.objeto.fecha
        seis_am = mx.DateTime.DateTimeDeltaFrom(hours = 6)
        medianoche = mx.DateTime.DateTimeDeltaFrom(hours = 0)
        if self.objeto.horainicio >= medianoche and \
           self.objeto.horainicio <= seis_am and \
           self.objeto.horafin <= seis_am:  # No se mezclan turnos, esta
                                # última comprobación podría no hacer falta.
            dia_lab_parte -= mx.DateTime.oneDay
        laborables = LAB.select("""calendario_laboral_id = %d AND date_part('day', fecha) = %d""" \
                                    % (calendario.id, dia_lab_parte.day))
        for laborable in laborables:
            turno = laborable.turno
            if turno == None:
                mensaje = "partes_de_fabricacion_bolsas.py::get_empleados_de_calendario -> Laborable ID %d no tiene turno relacionado. Intento eliminarlo de la BD." % (laborable.id)
                print "ERROR: %s" % (mensaje)
                self.logger.error(mensaje)
                try:
                    laborable.destroy(ventana = __file__)
                    idlaborable = laborable.id
                    self.logger.warning("partes_de_fabricacion_bolsas.py::get_empleados_de_calendario -> Registro laborable ID %d ELIMINADO SATISFACTORIAMENTE." % (idlaborable))
                except:
                    self.logger.error("partes_de_fabricacion_bolsas.py::get_empleados_de_calendario -> Registro laborable ID %d NO ELIMINADO." % (laborable.id))
                continue
            turnohorainicio = utils.DateTime2DateTimeDelta(turno.horainicio)
            turnohorafin = utils.DateTime2DateTimeDelta(turno.horafin)
            objetohorainicio = utils.DateTime2DateTimeDelta(
                self.objeto.horainicio)
            objetohorafin = utils.DateTime2DateTimeDelta(self.objeto.horafin)
            if not turno.recuperacion:
                ohi = objetohorainicio
                ohf = objetohorafin
                thi = turnohorainicio
                thf = turnohorafin
                if thi > thf: thf += mx.DateTime.oneDay
                if ohi > ohf: ohf += mx.DateTime.oneDay
                if ohi >= medianoche and ohi < seis_am:
                    ohi += mx.DateTime.oneDay
                if ohf >= medianoche and ohf <= seis_am:
                    ohf += mx.DateTime.oneDay
                if thi <= ohi <= thf and thi <= ohf <= thf:
                    for empleado in laborable.empleados:
                        res.append(empleado)
        return res

    def add_consumo(self, boton):
        self.consumir_manual(boton)

    def add_bigbag(self, boton):
        """
        Consume un bigbag buscándolo por su código de trazabilidad.
        """
        codigo = utils.dialogo_entrada(titulo = "BUSCAR BIGBAG",
            texto = "Introduzca el código de trazabilidad del bigbag\n"
                    "de fibra de cemento:",
            padre = self.wids['ventana'])
        if codigo:
            codigo = codigo.replace(" ", "").replace("-", "").upper().strip()
            if not codigo.startswith("C"):
                try:
                    codigo = "C%d" % utils.parse_numero(codigo)
                except TypeError:
                    utils.dialogo_info(titulo="ERROR",
                            texto="El texto introducido «%s» no es un número."
                                % (codigo),
                            padre=self.wids['ventana'])
                    codigo = "erróneo"
            try:
                bb = pclases.Bigbag.selectBy(codigo = codigo)[0]
            except IndexError:
                utils.dialogo_info(titulo = "CÓDIGO NO ENCONTRADO",
                    texto = "El código %s no se encontró." % codigo,
                    padre = self.wids['ventana'])
            else:
                albint = self.objeto.buscar_o_crear_albaran_interno(
                        incluir_consumos_auto = True) # Normalmente no, pero
                        # aquí sí quiero que aparezcan en el alb. interno.
                bb.articulo.sync()
                if bb.articulo.almacen != albint.almacenOrigen:
                    utils.dialogo_info(titulo = "BIGBAG NO ESTÁ EN ALMACÉN",
                        texto="El bigbag %s no se encuentra en el almacén %s"%(
                            codigo, albint.almacenOrigen.nombre),
                        padre = self.wids['ventana'])
                else:
                    # Para consumir lo sacamos del almacén.
                    bb.parteDeProduccion = self.objeto
                    bb.articulo.almacen = None
                    bb.articulo.syncUpdate()
                    # Y lo metemos en el albarán interno.
                    lineas_albaran = {}
                    for ldv in albint.lineasDeVenta:
                        pv = ldv.productoVenta
                        if pv not in lineas_albaran:
                            lineas_albaran[pv] = [ldv]
                        else:
                            lineas_albaran[pv].append(ldv)
                    pv_bb = bb.articulo.productoVenta
                    if pv_bb not in lineas_albaran:
                        linea_albaran = pclases.LineaDeVenta(
                            ticket=None,
                            pedidoVenta=None,
                            facturaVenta=None,
                            productoVenta=pv_bb,
                            albaranSalida=albint,
                            prefactura=None,
                            productoCompra=None,
                            fechahora=mx.DateTime.localtime(),
                            cantidad=0.0,
                            precio=pv_bb.precioDefecto,
                            descuento=0.0,
                            notas="",
                            descripcionComplementaria="Reembolsado")
                        lineas_albaran[pv_bb] = [linea_albaran]
                        pclases.Auditoria.nuevo(linea_albaran,
                                                self.usuario, __file__)
                    bb.articulo.albaranSalida = albint
                    lineas_albaran[pv_bb][-1].cantidad += bb.pesobigbag
                    lineas_albaran[pv_bb][-1].syncUpdate()
                    self.rellenar_tabla_consumos()
                    self.rellenar_estadisticas()

    def drop_consumo(self, boton):
        """
        Elimina los consumos seleccionados.
        """
        model, paths = self.wids['tv_consumos'].get_selection().get_selected_rows()
        if paths == None or paths == []:
            utils.dialogo_info('CONSUMOS NO SELECCIONADOS',
                'Debe seleccionar uno o varios consumos a eliminar del parte.',
                padre=self.wids['ventana'])
        else:
            if not utils.dialogo('¿Eliminar del parte?',
                                 'BORRAR CONSUMOS DEL CONTROL DE ENVASADO',
                                 padre=self.wids['ventana']):
                return
            for path in paths:
                ide = model[path][-1]
                if ide > 0:  # Es consumo
                    consumo = pclases.Consumo.get(ide)
                    consumo.parteDeProduccion = None
                    try:
                        consumo.anular_consumo()
                        #consumo.destroy(ventana = __file__)
                    except:
                        utils.dialogo_info(titulo='INCIDENCIA NO ELIMINADA',
                                    texto='Ocurrió un error al intentar '\
                                          'eliminar la consumo.',
                                    padre=self.wids['ventana'])
                elif ide < 0:    # Es bigbag
                    ide = -ide
                    bb = pclases.Bigbag.get(ide)
                    albint = self.objeto.get_albaran_interno()  # DEBE existir
                    assert albint == bb.articulo.albaranSalida
                    # Devuelvo al almacén
                    bb.parteDeProduccion = None
                    bb.articulo.almacen = albint.almacenOrigen
                    bb.articulo.albaranSalida = None
                    bb.articulo.sync()
                    # Y saco del albarán
                    idldv = albint._buscar_ldv(albint.agrupar_articulos(),
                                             bb.articulo.productoVenta.codigo,
                                             0.0) # La cantidad no me importa.
                    ldv = pclases.LineaDeVenta.get(idldv)
                    ldv.cantidad -= bb.pesobigbag
                    ldv.syncUpdate()
            #self.actualizar_ventana()
            self.objeto.buscar_o_crear_albaran_interno(
            incluir_consumos_auto = True) # Normalmente no, pero
                # aquí sí quiero que aparezcan en el alb. interno.
            self.rellenar_tabla_consumos()

    def cambiar_numbolsas(self, cell, path, newtext):
        """
        Comprueba que se ha escrito un número y ajusta el número de bolsas por
        caja del palé creando o eliminando bolsas de cada caja hasta llegar
        al número tecleado.
        """
        # TODO:
        pass

    def pasar_pale_a_B(self, cell, path):
        """
        Si la fila que ha marcado era B cambia todo el palé a A. Si no, hace
        lo contrario y lo cambia entero a A.
        """
        # TODO: Implica cambiar bolsas por caja y demás. No es solo cambiar un
        # atributo en el objeto.
        pass

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
                texto = "Introduzca la cantidad a consumir de %s%s."
                        "\n<small><i>%s</i></small>" % (
                            descripcion, unidad, producto.observaciones),
                padre = self.wids['ventana'])
            if cantidad != None:
                try:
                    cantidad_a_consumir = utils._float(cantidad)
                except (TypeError, ValueError):
                    utils.dialogo_info(titulo = "ERROR DE FORMATO",
                        texto='El texto introducido "%s" no es un número.' % (
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
                    producto.add_existencias(-cantidad_a_consumir)
                    producto.syncUpdate()
                    self.logger.warning("%sCONSUMO LÍNEA EMBOLSADO -> PARTE %d -> Consumiendo manualmente %f %s de %s (ID %d). Existencias: %f."
                        % (self.usuario and self.usuario.usuario + ": " or "",
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
                        if round(c.cantidad, 3) == 0:
                            # Cosas tan pequeñas como las agujas se descuentan
                            # en cantidades tan pequeñas que tras varias
                            # inserciones y borrados puede quedar el consumo
                            # con cantidad 0.0000...1, que debe ser borrado.
                            try:
                                c.destroy(ventana = __file__)
                            except Exception, msg:
                                self.logger.error("%sConsumo ID %d no se pudo eliminar. Excepción: %s"
                                                  % (self.usuario and self.usuario.usuario + ": " or "",
                                                     c.id,
                                                     msg))
                    self.rellenar_tabla_consumos()
                    # Buscar y crear (si no existe) el albarán interno de
                    # consumos.
                    self.objeto.buscar_o_crear_albaran_interno(
                        incluir_consumos_auto = True) # Normalmente no, pero
                            # aquí sí quiero que aparezcan en el alb. interno.

    def etiquetar(self, boton):
        """
        Genera las etiquetas de los palés seleccionados.
        """
        tv = self.wids['tv_produccion']
        model, paths = tv.get_selection().get_selected_rows()
        if paths == None or paths == []:
            utils.dialogo_info('SELECCIONE PALÉS',
                'Debe seleccionar uno o más palés a etiquetar.',
                padre = self.wids['ventana'])
        else:
            if not utils.dialogo(
                    'A continuación se generarán las etiquetas para '
                    '%d palé%s.\n¿Continuar?' %(
                        len(paths),
                        len(paths) != 1 and "s" or ""),
                    '¿GENERAR ETIQUETAS?',
                    padre = self.wids['ventana']):
                return
            ids = []
            for path in paths:
                puid = model[path][-1]
                clase, ide = puid.split(":")  # @UnusedVariable
                ids.append(ide)
            pales = [pclases.Pale.get(ide) for ide in ids]
            imprimir_etiquetas_pales(pales, self.wids['ventana'])


def imprimir_etiquetas_pales(pales, padre = None, mostrar_dialogo = True):
    """
    Muestra una ventana para seleccionar el tipo de etiquetas a imprimir.
    Por defecto se marca la neutral (tipo = 1).
    Si mostrar_dialogo es False, usa la opción global que haya guardada. Si no
    hay opción globar guardada, se ignora el parámetro y se muestra el
    cuadro de diálogo.
    """
    global MEMENTO_MORI
    # Para la normativa del 1 de julio de 2013 fuerzo a que siempre se
    # saquen ya las etiquetas con el nuevo formato. Pero como puede haber una
    # vuelta atrás, voy a permitir la posibilidad (aunque no en GUI, solo
    # programáticamente) de seguir sacando etiquetas antiguas.
    MEMENTO_MORI['que_imprimir'] = 0 # Ya no se harán etiquetas de caja. Con
                                        # la norma 2013 solo etiquetas de palé.
    if MEMENTO_MORI['que_imprimir'] is None:    # Nunca ha elegido una opción:
        mostrar_dialogo = True
    else:
        que_imprimir = MEMENTO_MORI['que_imprimir']
        mostrar_dialogo = False
    if mostrar_dialogo:
        que_imprimir = utils.dialogo_radio(
            titulo = "SELECCIONAR TIPO IMPRESIÓN",
            texto = "Seleccione qué imprimir:",
            ops = [(0, "Etiqueta de palé"),
                   (1, "Etiquetas de caja"),
                   (2, "Etiquetas de palé y cajas")],
            padre = padre,
            valor_por_defecto = 2)
    if que_imprimir != None:
        MEMENTO_MORI['que_imprimir'] = que_imprimir
        from formularios.reports import mandar_a_imprimir_con_ghostscript
        if que_imprimir == 0 or que_imprimir == 2:
            tipo = 3    # Opción inexistente en el diálogo pero reconocible
                        # por la función que va a generar las etiquetas.

            # BACKTRACKING a etiqueta antigua hasta que arreglemos la etiquetadora de la línea de cemento.
            #tipo = MEMENTO_MORI['tipo'] # <- 18/09/2013: Pasamos a la nueva.
                                         # Ya no permito seleccionar otra.
            if tipo is None:
                tipo = utils.dialogo_radio(titulo = "SELECCIONAR ETIQUETA",
                    texto = "Seleccione el tipo de etiqueta a generar:",
                    ops = [(0, "Mínima (solo código de palé, partida y "
                               "marcado CE)"),
                           (1, "Neutra (incluye datos de producto)"),
                           (2, "Completa (incluye el nombre de la empresa)")],
                    padre = padre,
                    valor_por_defecto = 1)
            if tipo != None:
                MEMENTO_MORI['tipo'] = tipo
            else:
                return
            # EOBACKTRACK: Descomentar el rotate = True cuando volvamos a usar las etiquetas nuevas.
            try:
                func_etiqueta = pales[0].productoVenta.camposEspecificosBala.modeloEtiqueta.get_func()
                filetiqpale = func_etiqueta(pales)
            except (AttributeError, IndexError, ValueError):  # Fallback a etiqueta por defecto.
                filetiqpale = geninformes.generar_etiqueta_pale(pales, tipo)
            for pale in pales:
                pclases.Auditoria.modificado(pale,
                    # self.usuario,
                    None,
                    __file__,
                    "Impresión de etiqueta para palé %s" % (
                    pale.codigo))
            mandar_a_imprimir_con_ghostscript(filetiqpale#)
                                              , rotate = True)
        if que_imprimir == 1 or que_imprimir == 2:
            tipo = MEMENTO_MORI['tipo']
            if tipo is None:
                tipo = utils.dialogo_radio(titulo = "SELECCIONAR ETIQUETA",
                    texto = "Seleccione el tipo de etiqueta a generar:",
                    ops = [(0, "Mínima (solo código de palé, partida y "
                               "marcado CE)"),
                           (1, "Neutra (incluye datos de producto)"),
                           (2, "Completa (incluye el nombre de la empresa)")],
                    padre = padre,
                    valor_por_defecto = 1)
            if tipo != None:
                MEMENTO_MORI['tipo'] = tipo
            cajas = []
            for p in pales:
                cajas += p.cajas[:]
            for caja in cajas:
                pclases.Auditoria.modificado(caja.articulo,
                    self.usuario,
                    __file__,
                    "Impresión de etiqueta para caja %s" % (
                    caja.articulo.get_info()))
            filetiqcaja = geninformes.generar_etiqueta_caja(cajas, tipo)
            mandar_a_imprimir_con_ghostscript(filetiqcaja)


if __name__ == "__main__":
    p = PartesDeFabricacionBolsas()

