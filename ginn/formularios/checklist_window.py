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
# TODO: En algún lado habrá que volcar la salida de los hilos o algo, ¿no?
#       La barra de progreso no termina de ir fina del todo. Se pone enseguida 
#       en torno al 90%.
# PLAN: Se podría guardar una variable de estado con las tareas completadas 
#       y pendientes para poder cerrar la ventana y seguir por donde se dejó 
#       más adelante. Claro que esto implicaría que de alguna forma habría 
#       que verificar que las tareas completadas siguen siendo válidas y no 
#       ha cambiado ninguna condición, porque en ese caso habría que volver a
#       ejecutarlas.
# TODO: Falta algo que creo que no se comprueba ahora: facturas donde se ha 
#       cobrado de más. Especialmente aquellas en las que se ha cobrado justo
#       el doble o tienen vencimientos a 0; porque son sospechosas de haberse 
#       creado un cobro accidentalmente al agregar la misma factura a varios 
#       pagarés o cosas así cuando originalmente solo tenían un vencimiento.
###############################################################################
# Para volcado de resultados ejecutar con:
# ./checklist_window.py 2>&1 | tee > ../../fixes/salida_check_`date +%Y_%m_%d_%H_%M`.txt
###############################################################################


import pygtk
pygtk.require('2.0')

import sys, os
import time
import gtk, pango

import mx, mx.DateTime

import utils

from threading import Thread, Semaphore

from ventana_progreso import VentanaActividad
vpro = VentanaActividad(texto = "Generando excepciones a ignorar...")
vpro.mostrar()
vpro.mover()
from framework import pclases
vpro.mover()
dde = pclases.DatosDeLaEmpresa.select()[0]
vpro.mover()
if dde.nombre == "Geotexan, S.A.":
    PEDIDOS_ALBARANES_Y_FACTURAS_A_IGNORAR_MISMO_C_O_P = [
        pclases.PedidoVenta.get(376), 
        pclases.PedidoVenta.get(369), 
        pclases.PedidoVenta.get(171), 
        pclases.AlbaranSalida.get(497), 
        pclases.AlbaranSalida.get(494), 
        pclases.AlbaranSalida.get(167), 
        pclases.FacturaVenta.get(279)
        ]
    vpro.mover()
    idspedido = (2, 129, 135, 44, 108, 230, 325, 672) 
    IGNORADOS_SIN_PROVEEDOR_O_CLIENTE = []
    for idpedido in idspedido:
        try:
            IGNORADOS_SIN_PROVEEDOR_O_CLIENTE.append(
                pclases.PedidoVenta.get(idpedido))
        except:
            print >> sys.stderr, "WARNING: Pedido ID %d no encontrado" % (
                idpedido)
    vpro.mover()
    ARTICULOS_A_IGNORAR = tuple(
        pclases.Articulo.select(pclases.Articulo.q.id < 131673))
        # Los artículos fabricados antes del 2008 se ignoran. Son intocables.
    vpro.mover()
    PARTES_A_IGNORAR = tuple(pclases.ParteDeProduccion.select(
        pclases.ParteDeProduccion.q.fecha < mx.DateTime.DateTime(2008, 1, 1)))
        # Los partes anteriores al 2008 tampoco tiene sentido corregirlos ya.
    vpro.mover()
    ALBARANES_A_IGNORAR = tuple(pclases.AlbaranSalida.select(
        pclases.AlbaranSalida.q.fecha < mx.DateTime.DateTime(2008, 1, 1)))
        # Los anteriores a 2008 tampoco se pueden tocar ya a estas alturas.
    vpro.mover()
    TICKETS_A_IGNORAR = []
    vpro.mover()
else:
    vpro.mover()
    PEDIDOS_ALBARANES_Y_FACTURAS_A_IGNORAR_MISMO_C_O_P = []
    IGNORADOS_SIN_PROVEEDOR_O_CLIENTE = []
    ARTICULOS_A_IGNORAR = []
    PARTES_A_IGNORAR = []
    ALBARANES_A_IGNORAR = []
    TICKETS_A_IGNORAR = tuple(pclases.Ticket.select(
        pclases.Ticket.q.fechahora < mx.DateTime.DateTimeFrom(2008, 1, 1)))
    vpro.mover()
vpro.ocultar()
del(vpro)

class Test(Thread):
    def __init__ (self, button, count, active_threads):
        Thread.__init__(self)
        self.count = count
        self.button = button
        self.active_threads = active_threads

    def run(self):
        gtk.gdk.threads_enter()
        self.active_threads.append(self)  # La lista de hilos DEL HILO PRINCIPAL del proceso. La bloqueo y desbloqueo cada vez que la toco.
        gtk.gdk.threads_leave()
        for i in range(0, 10):
            time.sleep(1)
            # Acquire and release the lock each time.
            gtk.gdk.threads_enter()
            self.button.set_label("Thread %002d - %d" % (self.count, i))
            gtk.gdk.threads_leave()
        gtk.gdk.threads_enter()
        self.button.set_label("  Start Thread  ")
        self.active_threads.remove(self)
        gtk.gdk.threads_leave()


class ThreadSample:
    """ Simple pyGTK multithreading example"""

    # Adapted from a post by Alif Wahid on the pyGTK mailinglist.
    # Cedric Gustin, August 2003
    def __init__(self):
        self.threadcount = 0
        self.active_threads = []

    def start_new_thread(self, button, data = None):
        self.threadcount += 1
        a = Test(button, self.threadcount, self.active_threads)
        a.start()

    def destroy(self, *args):
        """ Callback function that is activated when the program is destoyed """
        self.window.hide()
        gtk.main_quit()

    def main(self):
        # Initialize threads
        gtk.gdk.threads_init()

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)

        button = gtk.Button("  Start Thread  ")
        button.connect("clicked", self.start_new_thread, button)
        self.window.add(button)
        button.show()

        self.window.show_all()
        gtk.gdk.threads_enter()
        gtk.main()
        print "Finalizando %d hilos pendientes..." % (len(self.active_threads))
        gtk.gdk.threads_leave()

###############################################################################
class TareaSimple(Thread):
    def __init__ (self, 
                  count, 
                  active_threads, 
                  tarea, 
                  ventana_padre, 
                  *args, 
                  **kw):
        """
        count -> Número de procesos creados hasta la llamada a mi constructor. 
                 Se corresponde con el número de esta tarea.
        active_threads -> Lista de objetos tarea en ejecución.
        tarea -> Diccionario con la info de la tarea.
        ventana_padre -> Instancia del objeto ChecklistWindow para poder 
                         acceder a sus widgets.
        *args, **kw -> Lo pasaré tal cual a la función de la tarea.
        """
        Thread.__init__(self)
        self.count = count
        self.active_threads = active_threads
        self.struct_tarea = tarea   # Diccionario de la tarea desde el que 
                # puedo acceder a mis widgets para actualizaros, por ejemplo.
        self.func = tarea['func']   # Lo guardo en otro atributo por comodidad 
                # y legibilidad, más que nada.
        self.res = None             # Resultado de ejecutar la tarea. Lo 
                                    # guardaré por si me lo piden.
        self.ventana_padre = ventana_padre
        self.args = args
        self.kw = kw

    def run(self):
        # MUTEX
        # Cada tarea se encargará de controlarse a sí misma y esperar antes de 
        # hacer su trabajo. Todas competirán entre ellas para continuar 
        # (mediante una espera activa, es lo más sencillo) dejando que el hilo 
        # principal las lance a cascoporro. Para controlar el máximo de tareas 
        # que pueden entrar en la región crítica usaré un semáforo que se 
        # define en la ventana principal.
        # Intento entrar y si no puedo el semáforo me bloquea:
        self.ventana_padre.rc.acquire()
        # EOMUTEX
        
        # INICIALIZACIÓN
        gtk.gdk.threads_enter()
        self.active_threads.append(self.struct_tarea)   
            # Inicialmente eran objetos Tarea, pero será mejor usar los 
            # struct_tarea, que es lo visible desde la hebra principal.
        # print len(self.active_threads)
        gtk.gdk.threads_leave()
        
        # EJECUCIÓN (Podría ir todo en un solo bloque, pero didácticamente 
        # -hacia mí mismo- lo veo más claro así. Además, podría interesarme 
        # hacer bucles adquire-release aquí, por ejemplo.)
        ##gtk.gdk.threads_enter()   # Si no voy a tocar la interfaz, 
            # llamar al threads_enter hace justo lo contrario a lo que 
            # quiero: bloquearla hasta terminar de ejecutar la función.
        # self.res = apply(self.func, self.args, self.kw)   # DEPRECATED
        print "Voy a ejecutar..."
        self.res = self.func(*self.args, **self.kw)
        print "Ejecución finalizada."
        ##gtk.gdk.threads_leave()
        
        # FINALIZACIÓN
        gtk.gdk.threads_enter()
        # Código de finalización
        # print len(self.ventana_padre.get_tareas_completadas()), (1.0 * self.ventana_padre.tareas_totales), fraccion
        # El último que cierre.
        # print len(self.active_threads)
        # Y me salgo de la lista de hilos activos.
        self.active_threads.remove(self.struct_tarea)
        gtk.gdk.threads_leave()

        # Libero la sección crítica:
        self.ventana_padre.rc.release()


class Tarea(Thread):
    def __init__ (self, count, active_threads, tarea, ventana_padre, *args, **kw):
        """
        count -> Número de procesos creados hasta la llamada a mi constructor. Corresponde con el número de esta tarea.
        active_threads -> Lista de objetos tarea en ejecución.
        tarea -> Diccionario con la info de la tarea.
        ventana_padre -> Instancia del objeto ChecklistWindow para poder acceder a sus widgets.
        *args, **kw -> Lo pasaré tal cual a la función de la tarea.
        """
        Thread.__init__(self)
        self.count = count
        self.active_threads = active_threads
        self.struct_tarea = tarea   # Diccionario de la tarea desde el que puedo acceder a mis widgets para actualizaros, por ejemplo.
        self.func = tarea['func']   # Lo guardo en otro atributo por comodidad y legibilidad, más que nada.
        self.res = None     # Resultado de ejecutar la tarea. Lo guardaré por si me lo piden.
        self.ventana_padre = ventana_padre
        self.args = args
        self.kw = kw

    def run(self):
        # MUTEX
        # Cada tarea se encargará de controlarse a sí misma y esperar antes de hacer su trabajo. Todas competirán 
        # entre ellas para continuar (mediante una espera activa, es lo más sencillo) dejando que el hilo principal 
        # las lance a cascoporro. Para controlar el máximo de tareas que pueden entrar en la región crítica usaré un 
        # semáforo que se define en la ventana principal.
        # Intento entrar y si no puedo el semáforo me bloquea:
        self.ventana_padre.rc.acquire()
        # EOMUTEX
        
        # INICIALIZACIÓN
        gtk.gdk.threads_enter()
        self.ventana_padre.startstop.set_sensitive(False)
        #self.active_threads.append(self)  # La lista de hilos DEL HILO PRINCIPAL del proceso. La bloqueo y desbloqueo cada vez que la toco.
        self.active_threads.append(self.struct_tarea)   # Inicialmente eran objetos Tarea, pero será mejor usar los struct_tarea, que es 
                                                        # lo visible desde la hebra principal.
        # print len(self.active_threads)
        flecha, check, iniciar_si_o_no = self.struct_tarea['widgets']
        iniciar_si_o_no.set_sensitive(False)
        flecha.set_sensitive(True)
        label = check.child
        label.modify_fg(gtk.STATE_NORMAL, label.get_colormap().alloc_color("blue"))
        gtk.gdk.threads_leave()
        
        # EJECUCIÓN (Podría ir todo en un solo bloque, pero didácticamente -hacia mí mismo- lo veo más claro así. Además, 
        #            podría interesarme hacer bucles adquire-release aquí, por ejemplo.)
        ##gtk.gdk.threads_enter()   # Si no voy a tocar la interfaz, llamar al threads_enter hace justo lo contrario a lo que 
                                    # quiero: bloquearla hasta terminar de ejecutar la función.
        # self.res = apply(self.func, self.args, self.kw)   # DEPRECATED
        self.res = self.func(*self.args, **self.kw)
        ##gtk.gdk.threads_leave()
        
        # FINALIZACIÓN
        gtk.gdk.threads_enter()
        # Código de finalización
        check.set_inconsistent(False)
        if self.res == False:
            check.set_active(False)
            label.modify_fg(gtk.STATE_NORMAL, label.get_colormap().alloc_color("red"))
        else:
            check.set_active(True)    # Si no devuelve nada (es decir None) lo tomo como que acabó bien.
            label.modify_fg(gtk.STATE_NORMAL, label.get_colormap().alloc_color("green"))
        flecha.set_sensitive(False)
        check.set_property("can-focus", False)  # ¿Por qué no puedo ponerlo para que no responda al foco y los clics del usuario?
        check.connect("clicked", lambda w: w.set_active(self.res != False))     # HACK: Lo fuerzo a lo que suelta res.
        fraccion = (len(self.ventana_padre.get_tareas_completadas()) + 1) / (1.0 * self.ventana_padre.tareas_totales)
            # Todavía no me cuenta a mí misma como Tarea completada, así que me sumo antes de actualizar la barra de progreso.
        # print len(self.ventana_padre.get_tareas_completadas()), (1.0 * self.ventana_padre.tareas_totales), fraccion
        self.ventana_padre.progreso.set_fraction(fraccion)
        # El último que cierre.
        # print len(self.active_threads)
        # Y me salgo de la lista de procesos activos.
        self.active_threads.remove(self.struct_tarea)
        if len(self.active_threads) == 0: # self.active_threads y ventana_padre.active_threads apuntan a la misma posición de memoria. 
                                          # Puedo usar una u otra variable indistintamente, pero así es más claro. 
            self.ventana_padre.startstop.set_sensitive(True)
            time_elapsed = time.time() - self.ventana_padre.tiempo_inicio
            str_time_elapsed = "%d horas, %d minutos, %d segundos" % (time_elapsed / 60 / 60, (time_elapsed / 60) % 60, time_elapsed % 60)
            self.ventana_padre.progreso.set_text("Tiempo transcurrido: %s" % str_time_elapsed)
        gtk.gdk.threads_leave()

        # Libero la sección crítica:
        self.ventana_padre.rc.release()


class ChecklistWindow:
    """ 
    Una Checklist Window según las HIG de Gnome: 
    http://developer.gnome.org/projects/gup/hig/2.0/windows-progress.html#progress-window-checklists
    Pero con hilos. Vivo al límite.
    """

    def __init__(self, tareas, titulo = "PROGRESO"):
        """
        tareas es un diccionario que contiene al menos el nombre de la tarea y la función a ejecutar.
        Se ejecutan todas en paralelo en nuevos hilos. No estaría mal una estructura auxiliar que definiera 
        aquéllas que se deben ejecutar secuencialmente entre ellas. Claro que eso implicaría usar una 
        política de planificación, programar un despachador... 
        """
        self.threadcount = 0
        self.active_threads = []
        self.tareas_iniciadas = []
        self.tareas = tareas    # Lista de diccionarios. Cada diccionario tiene el nombre de la tarea, la función a realizar y sus widgets.
        self.titulo = titulo
        self.he_empezado = False
        self.continuar = True   # Si False, no crea más Tareas.
        self.tiempo_inicio = None
        self.tiempo_fin = None
        self.inicializar_ventana()
        self.rc = Semaphore(3)  # Región crítica a la que podrán acceder hasta 3 hilos a la vez.

    def destroy(self, *args):
        tareas_ko = 0
        tareas_ok = 0
        for t in self.tareas:
            wok = t['widgets'][1]
            if not wok.get_inconsistent():
                if wok.get_active():
                    tareas_ok += 1
                else:
                    tareas_ko += 1
        try:
            salud = ((tareas_ok * 1.0) / (tareas_ok + tareas_ko)) * 100
        except ZeroDivisionError:
            salud = 0
        print """
            Pruebas a realizar: %d. 
            Pruebas completadas con éxito: %d. 
            Pruebas fallidas: %d
            Tasa de errores de coherencia de datos: %.1f%%.""" % (
                tareas_ok + tareas_ko, tareas_ok, tareas_ko, 100 - salud)
        self.window.hide()
        gtk.main_quit()

    def inicializar_ventana(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(5)
        self.window.set_title(self.titulo)
        self.add_controls()


    def main(self):
        # Inicialización de hilos.
        gtk.gdk.threads_init()

        # ¿Aquí debería hacer algo?

        gtk.gdk.threads_enter()
        gtk.main()
        print "Finalizando %d hilos pendientes..." % (len(self.active_threads))
        gtk.gdk.threads_leave()

    def add_controls(self):
        """
        Añade los widgets de componen la ventana.
        A saber:
        1 botón de cancelar.
        1 botón de iniciar/cerrar que se pondrá insensitivo una vez se pulse y 
          se activará con el texto "Cerrar" cuando acaben todas las tareas.
        1 barra de progreso global.
        1 VBox que contiene:
            1 HBox por cada tarea que contiene:
                1 Una flecha que se activa cuando la tarea se inicia y se 
                  desactiva después de completarse.
                1 CheckBox que se pone a True cuando la tarea finaliza, a 
                  False si no se completa y en Z si no se ha iniciado aún.
                1 Label con la descripción de la tarea.
        ... y sal al gusto.
        """
        botonera = gtk.HBox(homogeneous = True)
        self.cancel = gtk.Button("Cancelar")
        self.cancel.connect("clicked", self.cancelar)
        botonera.pack_start(self.cancel, False)
        self.startstop = gtk.Button("Iniciar")
        self.startstop.connect("clicked", self.iniciar_o_cerrar)
        botonera.pack_start(self.startstop, False)
        
        self.lista = gtk.VBox()
        self.widgets_tareas = []    # Lista de tuplas con flecha y checkbox.
        for tarea in self.tareas:
            if len(tarea['nombre']) > 140:
                tarea['nombre'] = utils.wrap(tarea['nombre'], 140)
            self.widgets_tareas.append((gtk.Arrow(gtk.ARROW_RIGHT, gtk.SHADOW_NONE), 
                                        gtk.CheckButton(tarea['nombre'], False), 
                                        gtk.CheckButton()))
            tarea['widgets'] = self.widgets_tareas[-1]
            vbox = gtk.HBox()
            vbox.pack_start(tarea['widgets'][0], False)
            vbox.pack_start(tarea['widgets'][1])
            vbox.pack_start(tarea['widgets'][2], False)
            tarea['widgets'][0].set_sensitive(False)
            tarea['widgets'][1].set_inconsistent(True)
            tarea['widgets'][1].set_property("can-focus", False)
            tarea['widgets'][1].connect("clicked", lambda w: w.set_active(w.get_active()))
            tarea['widgets'][2].set_active(True)
            self.lista.pack_start(vbox)

        vbox_out = gtk.VBox()
        vbox_out.pack_start(self.lista, padding = 10)
        self.progreso = gtk.ProgressBar()
        vbox_out.pack_start(self.progreso, False, padding = 10)
        vbox_out.pack_start(botonera, False, padding = 10)
        self.barra_estado = gtk.Statusbar()
        label_statusbar = self.barra_estado.get_children()[0].child
        font = pango.FontDescription("Monospace oblique 7")
        label_statusbar.modify_font(font)
        label_statusbar.modify_fg(gtk.STATE_NORMAL, label_statusbar.get_colormap().alloc_color("darkgray"))
        vbox_out.pack_end(self.barra_estado, False)
        self.window.add(vbox_out)
        self.window.show_all()

    def cancelar(self, boton):
        """
        Cancela los hilos activos y evita iniciar los restantes.
        Una vez se hayan terminado habilita el botón cerrar.
        """
        no_iniciadas = self.get_tareas_no_iniciadas()
        if self.he_empezado and len(no_iniciadas) > 0:
            self.continuar = False
            utils.dialogo_info(titulo = "CANCELANDO TAREAS", 
                               texto = "Las %d tareas restantes no se iniciarán.\nLas %d que han comenzado y aún no han terminado continuarán en segundo plano hasta finalizar.\n\nPulse «Aceptar» para cerrar esta ventana." % (
                                    self.tareas_totales - len(self.tareas_iniciadas), 
                                    self.tareas_totales - len(self.get_tareas_completadas())), 
                               padre = self.window)
        self.destroy()

    def iniciar_o_cerrar(self, boton):
        """
        Si todas las tareas se han completado o cancelado, cierra la ventana.
        Si no, las inicia y cambia el texto del botón por "Cerrar" y lo deshabilita.
        """
        if not self.he_empezado:
            self.iniciar_tareas()
        else:
            self.destroy()

    def get_tareas_completadas(self):
        """
        Devuelve las tareas que están en tareas iniciadas pero no en 
        active_threads. Es decir, las que ya han terminado.
        """
        # XXX ¿Debo bloquear para leer en active_threads?
        completadas = [t for t in self.tareas if t not in self.active_threads and t in self.tareas_iniciadas]
        return completadas

    def get_tareas_no_iniciadas(self):
        """
        Devuelve las tareas de la lista de tareas que no están en la 
        lista de tareas iniciadas. Incluidas las que ni siquiera están 
        marcadas para iniciarse.
        """
        no_iniciadas = [t for t in self.tareas if t not in self.tareas_iniciadas]
        return no_iniciadas

    def iniciar_tareas(self):
        """
        Inicia las tareas de la lista de tareas en un hilo aparte.
        """
        self.startstop.set_label("Cerrar")
        self.he_empezado = True
        self.tiempo_inicio = time.time()
        self.tareas_totales = len([t for t in self.tareas if t['widgets'][2].get_active()])

        count = 0
        for tarea in self.tareas:
            if not self.continuar:
                break
            if tarea['widgets'][2].get_active():
                
                ## print " -> ", len(self.active_threads)
                ## while len(self.active_threads) > 3:     # Como máximo 3 tareas a la vez.
                ##     time.sleep(5)                      # Esto no funca y no sé por qué.
                
                count += 1
                # Debería pasarle a los hilos la barra de progreso y un self.tiempo_estimado para que jueguen con él, 
                # lo actualicen en función de lo que cree que va a tardar cada uno y lo muestre en la barra de progreso. 
                nueva_tarea = Tarea(count, self.active_threads, tarea, self, *tarea['params'])
                nueva_tarea.start()
                self.tareas_iniciadas.append(tarea)

                ## print " -> ", len(self.active_threads)
        
                ## print "Tarea %d lanzada." % (count)
                

    def set_texto_estado(self, texto):
        utils.escribir_barra_estado(self.barra_estado, texto)


###############################################################################

def tarea2():
    print "Lorem ipsum dolor sit amet, consectetur adipisici elit, sed eiusmod tempor incidunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquid ex ea commodi consequat. Quis aute iure reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint obcaecat cupiditat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

def tarea1():
    res = utils.dialogo(titulo = "NO CONOZCO NINGÚN PAÍS LLAMADO QUÉ", 
                        texto = "¿Hablan mi idioma en «qué»?")
    return res

def pruebas_periodicas():
    path_framework = os.path.join("..", "framework")
    if path_framework not in sys.path:
        sys.path.append(path_framework)
    from framework.configuracion import ConfigConexion
    from framework import tests

    tasks = [{"nombre": "Cantidades de caché son correctas.", 
              "func": tests.comprobar_caches, 
              "params": []}, 
             {"nombre": "Fibra consumida antes de fecha de fabricación.", 
              "func": tests.comprobar_fibra_consumida_antes_de_fecha_de_fabricacion, 
              "params": [True, ARTICULOS_A_IGNORAR]}, 
             {"nombre": "Artículos vendidos antes de su fecha de fabricación.", 
              "func": tests.comprobar_articulos_vendidos_antes_de_fecha_de_fabricacion, 
              "params": [True, ARTICULOS_A_IGNORAR]}, 
             {"nombre": "Fibra en partida de carga y albarán de salida a la vez.", 
              "func": tests.comprobar_fibra_en_partida_de_carga_y_albaran_de_salida_a_la_vez, 
              "params": [True, ARTICULOS_A_IGNORAR]}, 
             {"nombre": "Artículos con albarán de salida y en líneas de devolución con albarán de entrada de abono a la vez.", 
              "func": tests.comprobar_articulos_con_albaran_salida_y_albaran_abono, 
              "params": [True, ARTICULOS_A_IGNORAR]}, 
             {"nombre": "Objetos artículo sin bala, rollo, bigbag, balaCable o rolloDefectuoso; con más de uno, o apuntados por más de un registro artículo.", 
              "func": tests.comprobar_articulos_con_enlaces_incorrectos, 
              "params": []}, 
             {"nombre": "Cantidades en líneas de venta coinciden con artículos en albarán.", 
              "func": tests.comprobar_cantidades_albaran, 
              "params": []}, 
             {"nombre": "Partes de producción no solapados.", 
              "func": tests.comprobar_partes_solapados, 
              "params": [True, PARTES_A_IGNORAR]}, 
             {"nombre": "Partes de producción consecutivos sin huecos.", 
              "func": tests.comprobar_huecos_partes, 
              "params": [True, PARTES_A_IGNORAR]}, 
             {"nombre": 'Coherencia entre fecha y horas con "fechahoras" en partes de producción.', 
              "func": tests.comprobar_coherencia_fecha_y_fechahoras_partes, 
              "params": [True]}, 
             {"nombre": "Sumatorio de duración de incidencias no supera duración de su parte de producción.", 
              "func": tests.comprobar_duracion_incidencias, 
              "params": [True]}, 
             {"nombre": "Horas trabajadas de empleados no supera duración de su parte de producción.", 
              "func": tests.comprobar_horas_trabajadas_en_partes, 
              "params": []}, 
             {"nombre": "Empleados en un único parte de producción a la misma hora o bien horas trabajadas menor o igual que duración total de horas no simultáneas.", 
              "func": tests.comprobar_partes_simultaneos_empleados, 
              "params": []}, 
             {"nombre": "Partidas de geotextiles con un único producto fabricado.", 
              "func": tests.comprobar_partidas_con_mas_de_un_producto, 
              "params": []}, 
             {"nombre": "Partidas de carga con producción pero sin fibra relacionada, o con carga pero sin producción, sin estar entre las últimas.", 
              "func": tests.comprobar_partidas_de_carga_sin_fibra_o_sin_produccion, 
              "params": []}, 
             {"nombre": "Suma de consumos de fibra entre fechas coincide con consumos por día entre mismas fechas.", 
              "func": tests.comprobar_consumos_entre_fechas, 
              "params": []}, 
             {"nombre": "Fecha partida carga menor o igual que fecha de inicio de producción y mayor que fecha fabricación de sus balas.", 
              "func": tests.comprobar_fecha_partidas_carga, 
              "params": []}, 
             {"nombre": "Partes de fibra con consumos de granza inferiores a producción.", 
              "func": tests.comprobar_consumos_granza, 
              "params": [True, PARTES_A_IGNORAR]}, 
             {"nombre": 'Artículos con "fechahora" fuera de las "fechahoras" de su parte de producción.', 
              "func": tests.comprobar_fechahora_de_articulos, 
              "params": [True]}, 
             {"nombre": "Balas en albaranes internos sin partida de carga y balas en partidas de carga sin albaranes internos.", 
              "func": tests.comprobar_balas_en_albaranes_internos_sin_partidacarga, 
              "params": [False, mx.DateTime.DateTimeFrom(2007, 1, 1)]}, 
             {"nombre": "Códigos de balas [cable], rollos [defectuoso] y bigbags coinciden con número.", 
              "func": tests.comprobar_codificacion_articulos, 
              "params": [True]}, 
             {"nombre": "Numeración de balas [cable], rollos [defectuosos] y bigbags es consecutiva.", 
              "func": tests.comprobar_numeracion_articulos, 
              "params": [True, ARTICULOS_A_IGNORAR]}, 
             {"nombre": "Albaranes internos de consumo solo contienen balas o productos de compra.", 
              "func": tests.comprobar_albaranes_internos, 
              "params": [True, ALBARANES_A_IGNORAR]}, 
             {"nombre": "Todos los pedidos, albaranes y facturas de compra y venta tienen cliente/proveedor.", 
              "func": tests.comprobar_clientes_proveedores_en_pedidos_albaranes_facturas, 
              "params": [True, 
                         IGNORADOS_SIN_PROVEEDOR_O_CLIENTE]}, 
             {"nombre": "Producción estándar de partes coinciden con producción estándar de productos.", 
              "func": tests.comprobar_producciones_estandar, 
              "params": [True, PARTES_A_IGNORAR]}, 
             {"nombre": "Existencias en silos coincide con existencias de productos.", 
              "func": tests.comprobar_existencias_silos, 
              "params": [True]}, 
             {"nombre": "Códigos de productos de compra únicos.", 
              "func": tests.comprobar_codigos_unicos_en_productos_compra, 
              "params": [True]},
             {"nombre": "Mismo cliente en pedidos, albaranes y facturas relacionadas.", 
              "func": tests.comprobar_mismo_cliente_pedidos_albaranes_facturas, 
              "params": [True, 
                         PEDIDOS_ALBARANES_Y_FACTURAS_A_IGNORAR_MISMO_C_O_P]},
             {"nombre": "Todos los números de tickets, {pedidos, albaranes,} y facturas son consecutivos.", 
              "func": tests.comprobar_saltos_facturas_albaranes_pedidos_y_tickets, 
              "params": [True, True, False, False, True, TICKETS_A_IGNORAR]},  
             {"nombre": "Todos los objetos artículo y sus correspondientes\nrollos, balas, etc. están emparejados", 
              "func": tests.comprobar_pares_articulos, 
              "params": []},  
             {"nombre": "Albaranes de salida y entrada tienen almacén origen y destino respectivamente", 
              "func": tests.comprobar_almacenes_albaranes, 
              "params": []},  
             {"nombre": "Balas en partidas de carga no deben tener almacén asignado", 
              "func": tests.comprobar_almacen_partidas_carga, 
              "params": []} 
            ]
    chkwin = ChecklistWindow(tasks, "PRUEBAS PERIÓDICAS DE COHERENCIA DE DATOS")
    config = ConfigConexion()
    info_conexion = "%s://%s:xxxxxxxx@%s:%s/%s" % (config.get_tipobd(), 
                                                   config.get_user(), 
                                                   config.get_host(), 
                                                   config.get_puerto(), 
                                                   config.get_dbname())
    chkwin.set_texto_estado("Conectado a %s." % (info_conexion))
    chkwin.main()

if __name__ == "__main__":
    # sample = ThreadSample()
    #tasks = [{'nombre': "Tarea 1: Sacar un diálogo modal Sí/No.", 
    #          'func': tarea1}, 
    #         {'nombre': "Tarea 2: Imprimir algo por consola.", 
    #          'func': tarea2}]
    # sample = ChecklistWindow(tasks, "PUEBINES, GUAJE")
    # sample.set_texto_estado("Aquí mostraré los datos de conexión.")
    # sample.main()
    pruebas_periodicas()

