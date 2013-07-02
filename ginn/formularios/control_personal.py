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
## control_personal.py - Horas trabajadas al día por empleado.
###################################################################
##  
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk, mx.DateTime
from framework import pclases
from framework.seeker import VentanaGenerica 

XBOTON, YBOTON = 21, 21

FLECHA_ARRIBA = ["9 9 2 1",
"     c None",
".    c #000000",
"         ",
"         ",
"    .    ",
"   ...   ",
"  .....  ",
" ....... ",
".........",
"         ",
"         "]

FLECHA_ABAJO = ["9 9 2 1",
"     c None",
".    c #000000",
"         ",
"         ",
".........",
" ....... ",
"  .....  ",
"   ...   ",
"    .    ",
"         ",
"         "]

def focusin(widget, event, hadj, vadj):
    """
    Porque todo en la vida real ha pasado antes en algún capítulo de Los 
    Simpson. Viva el Focusín (TM).
    """
    parent = widget.get_parent()
    if isinstance(parent, gtk.Alignment):
        parent = parent.get_parent()
    if isinstance(parent, gtk.EventBox):
        widget = parent
    alloc = widget.get_allocation()
    #print event, 
    #print alloc.x, alloc.width, hadj.value, hadj.page_size
    if (alloc.x < hadj.value 
        or alloc.x + alloc.width > hadj.value + hadj.page_size):
        hadj.set_value(min(alloc.x, hadj.upper - hadj.page_size))
    if (alloc.y < vadj.value 
        or alloc.y + alloc.height > vadj.value + vadj.page_size):
        vadj.set_value(min(alloc.y, vadj.upper - vadj.page_size))

def check_horas_regulares(ch, horas_regulares):
    """
    Comprueba que las horas regulares en total del registro «ch» no 
    sea superior a ocho horas.
    Devuelve True si se cumple y False si no.
    """
    return 0 <= horas_regulares <= 8

def check_total_horas(ch):
    """
    Horas regulares + horas extras = horas producción + horas mantenimiento 
        + horas almacén + horas varios
    """
    horas_regulares = ch.horasRegulares
    horas_extras = ch.calcular_total_horas_extras()
    horas_produccion = ch.calcular_total_horas_produccion()
    horas_mantenimiento = ch.calcular_total_horas_mantenimiento()
    horas_almacen = ch.horasAlmacen
    horas_varios = ch.horasVarios
    horas1 = horas_regulares + horas_extras 
    horas2 = (horas_produccion + horas_mantenimiento 
                + horas_almacen + horas_varios)
    return horas1 == horas2

def check_no_ausente_y_horas(ch):
    """
    Devuelve False si el empleado está marcado como ausente y tiene horas 
    asignadas.
    """
    horas_regulares = ch.horasRegulares
    horas_extras = ch.calcular_total_horas_extras()
    horas = horas_regulares + horas_extras
    if horas != 0:
        return not (ch.vacacionesYAsuntosPropios or ch.bajaLaboral)
    else:
        return True

def check_dias_consecutivos(fecha_actual):
    """
    Comprueba que no se intente meter un "parte" sin haber metido los 
    anteriores (aka «debe haber un parte por día obligatorio menos domingo»).
    Devuelve True si el parte anterior no está vacío o es la primera vez 
    que se introduce un parte de horas en la aplicación.
    """
    # Creo que es mejor comprobar que la fecha justo anterior es domingo, 
    # festivo o no está vacía.
    fecha_anterior = fecha_actual - mx.DateTime.oneDay
    if fecha_anterior.day_of_week == 6: # 0 es lunes
        fecha_anterior -= mx.DateTime.oneDay
    chs = pclases.ControlHoras.select(
            pclases.ControlHoras.q.fecha == fecha_anterior)
    # El parte está vacío si no hay registros o éstos no tienen nada.
    regs_no_vacios = [ch for ch in chs if not ch.es_nulo()]
    anterior_vacio = len(regs_no_vacios) == 0
    # Devuelvo que el día anterior no-domingo no sea nulo, lo cual 
    # significa que fecha_actual se puede completar (True).
    # Y si no se ha metido aún ningún día, tengo que dejar que edite.
    res = not anterior_vacio or pclases.ControlHoras.select().count() == 0
    return res

def check_verificados_anteriores(fecha_actual):
    """
    Comprueba que no se verifica un "parte" sin haberse verificado antes el 
    del día anterior (no en fecha, ya que si es lunes el del domingo no se 
    puede verificar porque no existe, así que se entiende que es el del parte 
    inmediatamente anterior, no el de la fecha -1 día).
    Devuelve True si el parte anterior está verificado o es la primera vez 
    que se verifica un parte.
    """
    fecha_anterior = fecha_actual - mx.DateTime.oneDay
    if fecha_anterior.day_of_week == 6: # 0 es lunes
        fecha_anterior -= mx.DateTime.oneDay
    chs = pclases.ControlHoras.select(
            pclases.ControlHoras.q.fecha == fecha_anterior)
    regs_verificados = [ch for ch in chs if ch.bloqueado]
    primera_vez = pclases.ControlHoras.select(
        pclases.ControlHoras.q.bloqueado).count() == 0
    return (len(regs_verificados) > 0) or primera_vez


class ControlPersonal(Ventana, VentanaGenerica):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self.clase = pclases.ControlHoras
        self.dic_campos = {}
        Ventana.__init__(self, 'control_personal.glade', objeto, 
                         usuario = usuario)
        # Estos botones no valen más que para "engañar" a la clase padre 
        # al chequear los permisos.
        self.wids['b_nuevo'] = gtk.Button()
        self.wids['b_buscar'] = gtk.Button()
        self.wids['b_guardar'] = gtk.Button()
        connections = {'b_actualizar/clicked': self.actualizar_ventana, 
                       'b_buscarfecha/clicked': self.buscar_fecha, 
                       'ch_bloqueado/clicked': self.bloquear, 
                       'ch_festivo/clicked': self.marcar_festivo, 
                       "b_ultimo_vacio/clicked": self.ir_a_ultimo_vacio, 
                       "b_ultimo_no_bloqueado/clicked": 
                            self.ir_a_ultimo_no_bloqueado, 
                       'b_copiar/clicked': self.copiar_anterior, 
                       }  
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto) 
        gtk.main()

    def ir_a_ultimo_vacio(self, boton):
        """
        Muestra en la ventana el último día vacío encontrado.
        En teoría es últil para no tener que buscar a mano por qué parte 
        te habías quedado en caso de no llevarlos al día.
        Como la aplicación tiene un chequeo para evitar partes vacíos 
        intercalados, el que encuentre será el próximo a completar.
        Ignora, al igual que el chequeo de partes consecutivos, los 
        domingos.
        OJO: La restricción se aplica únicamente a usuarios con nivel > 1.
        PRECONDICIÓN: check_dias_consecutivos debe devolver en algún instante 
        True para evitar un bucle infinito. Así que al menos debe contemplar 
        el caso en que no haya partes y devolver True si se esta metiendo 
        la primera fecha en la aplicación.
        """
        # Aprovechando el código escrito (DRY) esto es equivalente a recorrer 
        # hacia atrás los días, comenzando por la fecha actual, hasta 
        # encontrar una fecha que satisfaga el control de 
        # check_dias_consecutivos 
        fecha = mx.DateTime.localtime()
        while not check_dias_consecutivos(fecha):
            fecha = fecha - mx.DateTime.oneDay
        self.wids['e_fecha'].set_text(utils.str_fecha(fecha))
        self.actualizar_ventana()

    def copiar_anterior(self, boton):
        """
        Copia todos los datos del parte justo anterior al actual en este.
        """
        fecha_ventana = self.wids['e_fecha'].get_text()
        if not utils.dialogo(titulo = "SE CLONARÁ EL PARTE ANTERIOR", 
                texto = "Si introdujo datos en la fecha %s, éstos se "
                        "machacarán.\n¿Desea continuar?" % fecha_ventana, 
                padre = self.wids['ventana']):
            return
        try:
            fecha_parte_en_ventana = utils.parse_fecha(fecha_ventana)
        except (TypeError, ValueError):
            utils.dialogo_info(titulo = "FECHA INCORRECTA", 
                texto = "La fecha %s no es válida." % fecha_ventana, 
                padre = self.wids['ventana'])
        else:
            chs = pclases.ControlHoras.select(
                pclases.ControlHoras.q.fecha < fecha_parte_en_ventana, 
                orderBy = "-fecha")
            fecha_a_copiar = None
            for ch in chs:
                if not ch.es_nulo():    # Busco hacia atrás hasta encontrar un 
                                        # parte no vacío.
                    fecha_a_copiar = ch.fecha
                    break
            if not fecha_a_copiar:
                utils.dialogo_info(titulo = "PARTE NO ENCONTRADO", 
                    texto = "No se encontraron días anteriores que clonar.", 
                    padre = self.wids['ventana'])
            else:
                chs_toclone = pclases.ControlHoras.select(
                    pclases.ControlHoras.q.fecha == fecha_a_copiar)
                chs_toerase = pclases.ControlHoras.select(
                    pclases.ControlHoras.q.fecha == fecha_parte_en_ventana)
                for ch in chs_toerase:
                    ch.destroy_en_cascada(ventana = __file__)
                for ch in chs_toclone:
                    chnuevo = ch.clone(fecha = fecha_parte_en_ventana)
                    for chm in ch.controlesHorasProduccion:
                        chm.clone(controlHoras = chnuevo)
                    for chp in ch.controlesHorasMantenimiento:
                        chp.clone(controlHoras = chnuevo)
                self.actualizar_ventana()

    def ir_a_ultimo_no_bloqueado(self, boton):
        """
        Muestra el último parte sin bloquear. Al igual que el 
        "ir_a_ultimo_vacio", como hay una restricción para impedir bloqueos de 
        días no consecutivos (para ususarios sin privilegios suficientes), 
        debería irse al parte por donde el usuario se quedó verificando. 
        """
        # Me basta con encontrar un controlHoras que cumpla. Se verifican 
        # en bloque por día, así que con encontrar uno habré encontrado todos.
        # De nuevo, aprovecho el check normal que se aplica en estos casos que 
        # ya hace lo que pretendo:
        fecha = mx.DateTime.localtime()
        while not check_verificados_anteriores(fecha):
            fecha = fecha - mx.DateTime.oneDay
        self.wids['e_fecha'].set_text(utils.str_fecha(fecha))
        self.actualizar_ventana()

    def bloquear(self, chbox):
        """
        Bloquea todos los registros de control de horas de la fecha.
        """
        # TODO: Falta control para que usuarios sin permisos no puedan 
        # desbloquear.
        try:
            fecha = utils.parse_fecha(self.wids['e_fecha'].get_text())
        except:
            fecha = utils.parse_fecha(utils.str_fecha(mx.DateTime.localtime()))
        chs = pclases.ControlHoras.select(pclases.ControlHoras.q.fecha==fecha)
        # Compruebo que cuadren las horas antes de bloquear. Es imposible 
        # hacerlo mientras el usuario edita horas, porque no sé cuándo ha 
        # terminado de completar las horas de un currela hasta que no decide 
        # bloquear el día. Mientras introduce horas el descuadre es normal ya 
        # que puede haber metido primero las horas regulares y dejar los 
        # desgloses para el final o viceversa.
        correcto = True
        for ch in chs:
            correcto = correcto and check_total_horas(ch)
            if not correcto and chbox.get_active():
                # Solo muestro diálogo de error si me está intentando bloquear,
                # si me está desbloqueando, me estoy desbloqueando yo mismo 
                # desde este callback o la ventana está cambiando de un día 
                # bloqueado a otro desbloqueado, me/le ahorro la verborrea.
                utils.dialogo_info(titulo = "TOTAL DE HORAS INCORRECTO", 
                            texto = "El total de horas del trabajador %s "\
                                    "no es correcto." % (
                            ch.empleado.apellidos+ ", " + ch.empleado.nombre), 
                                   padre = self.wids['ventana'])
                # USABILIDAD: Si no es correcto, y ya que sé el empleado que 
                # lo impide, lo suyo es llevar al usuario directamente a él.
                # Me vale con pasar el foco al grupo, que es primer widget de 
                # la fila del empleado (así de paso obligo a que se fije, que 
                # últimamente están pasando un poco de poner los grupos bien).
                wabajo = self.wids['abajo_%d' % ch.id]
                wabajo.grab_focus()
                # Ahora muevo el foco al grupo
                wgrupo = self.wids['grupo_%d' % ch.id]
                wgrupo.grab_focus()
                wabajo.get_toplevel().child_focus(gtk.DIR_TAB_FORWARD)
                # Focusin (TM) hará el resto:
                break   # Para no ser cansino si falla más de uno.
            correcto = correcto and check_no_ausente_y_horas(ch)
            if not correcto and chbox.get_active():
                # Solo muestro diálogo de error si me está intentando bloquear,
                # si me está desbloqueando, me estoy desbloqueando yo mismo 
                # desde este callback o la ventana está cambiando de un día 
                # bloqueado a otro desbloqueado, me/le ahorro la verborrea.
                utils.dialogo_info(titulo = "EMPLEADO AUSENTE", 
                            texto = "No puede asignar horas al empleado %s "\
                            "por estar marcado como ausente o de baja." % (
                            ch.empleado.apellidos+ ", " + ch.empleado.nombre), 
                                   padre = self.wids['ventana'])
                # USABILIDAD: Si no es correcto, y ya que sé el empleado que 
                # lo impide, lo suyo es llevar al usuario directamente a él.
                # Me vale con pasar el foco al grupo, que es primer widget de 
                # la fila del empleado (así de paso obligo a que se fije, que 
                # últimamente están pasando un poco de poner los grupos bien).
                wabajo = self.wids['abajo_%d' % ch.id]
                wabajo.grab_focus()
                # Ahora muevo el foco al grupo
                wgrupo = self.wids['grupo_%d' % ch.id]
                wgrupo.grab_focus()
                wabajo.get_toplevel().child_focus(gtk.DIR_TAB_FORWARD)
                # Focusin (TM) hará el resto:
                break   # Para no ser cansino si falla más de uno.
        anterior = check_verificados_anteriores(fecha) 
        # TODO: Si usuario con nivel 0 ó 1, dejar bloquear.
        if not anterior and chbox.get_active():
            utils.dialogo_info(titulo = "NO PUEDE SER VERIFICADO", 
                               texto = "Debe verificar y bloquear el parte "\
                                  "anterior antes de hacerlo con el actual.", 
                               padre = self.wids['ventana'])
        chbox.set_active(chbox.get_active() and correcto and anterior)
        for ch in chs:
            ch.bloqueado = chbox.get_active() and correcto

    def marcar_festivo(self, chbox):
        try:
            fecha = utils.parse_fecha(self.wids['e_fecha'].get_text())
        except:
            fecha = utils.parse_fecha(utils.str_fecha(mx.DateTime.localtime()))
        chs = pclases.ControlHoras.select(pclases.ControlHoras.q.fecha==fecha)
        for ch in chs:
            ch.festivo = chbox.get_active()

    def ir_a_primero(self):
        """
        Va al día actual.
        """
        self.wids['e_fecha'].set_text(utils.str_fecha(mx.DateTime.localtime()))
        self.rellenar_widgets()

    def ir_a(self, objeto):
        """
        Va a la fecha del objeto recibido.
        """
        fecha = objeto.fecha
        self.wids['e_fecha'].set_text(utils.str_fecha(fecha))
        self.rellenar_widgets()

    def actualizar_ventana(self, boton = None):
        cursor_reloj = gtk.gdk.Cursor(gtk.gdk.WATCH)
        self.wids['ventana'].window.set_cursor(cursor_reloj)
        utils.set_unset_urgency_hint(self.wids['ventana'], False)
        while gtk.events_pending(): gtk.main_iteration(False)
        self.rellenar_widgets()
        self.wids['ventana'].window.set_cursor(None)

    def buscar_fecha(self, boton):
        try:
            fecha = utils.parse_fecha(self.wids['e_fecha'].get_text())
        except:
            fecha = mx.DateTime.localtime()
        fecha = utils.str_fecha(utils.mostrar_calendario(
                                                fecha_defecto = fecha, 
                                                padre = self.wids['ventana']))
        self.wids['e_fecha'].set_text(fecha)
        self.actualizar_ventana()

    def es_diferente(self):
        """
        Devuelve True si algún valor en ventana difiere de 
        los del objeto.
        """
        igual = True
        return not igual
    
    def nuevo_attach(self, 
                     child, 
                     left_attach, 
                     right_attach, 
                     top_attach, 
                     bottom_attach, 
                     xoptions=gtk.EXPAND|gtk.FILL, 
                     yoptions=gtk.EXPAND|gtk.FILL, 
                     xpadding=0, 
                     ypadding=0):
        """
        Wrapper del attach de gtk.Table pero guarda la fila de cada 
        widget.
        """
        # Echo de menos los decoradores, pero tengo que ser compatible 
        # hacia atrás.
        dict_widget = {'widget': child, 
                       'left_attach': left_attach, 
                       'right_attach': right_attach, 
                       'top_attach': top_attach, 
                       'bottom_attach': bottom_attach, 
                       'resto_params': [xoptions,yoptions,xpadding,ypadding]
                      }
        if top_attach not in self.hijos_tabla:
            self.hijos_tabla[top_attach] = [dict_widget]
        else:
            self.hijos_tabla[top_attach].append(dict_widget)
        self.wids['tabla']._attach(child, 
                                   left_attach, 
                                   right_attach, 
                                   top_attach, 
                                   bottom_attach, 
                                   xoptions,  
                                   yoptions, 
                                   xpadding, 
                                   ypadding)

    def nuevo_remove(self, widget):
        """
        Wrapper para eliminar un widget de la tabla y del diccionario interno.
        """
        for fila in self.hijos_tabla:
            for dic_w in self.hijos_tabla[fila]:
                if dic_w['widget'] == widget:
                    self.hijos_tabla[fila].remove(dic_w)
        self.wids['tabla']._remove(widget)

    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        #self.activar_widgets(False)
        self.wids['e_fecha'].set_text(utils.str_fecha(mx.DateTime.localtime()))
        self.wids['e_fecha'].connect("activate", 
                        lambda *a, **k: self.wids['b_actualizar'].grab_focus())
        self.wids['ventana'].resize(800, 600)
        self.wids['ventana'].show_all()
        self.hijos_tabla = {}
        self.wids['tabla']._attach = self.wids['tabla'].attach
        self.wids['tabla'].attach \
            = lambda *args, **kw: self.nuevo_attach(*args, **kw)
        self.wids['tabla']._remove = self.wids['tabla'].remove
        self.wids['tabla'].remove \
            = lambda *args, **kw: self.nuevo_remove(*args, **kw)
        self.PIXARRIBA, self.MASKARRIBA = gtk.gdk.pixmap_create_from_xpm_d(
                        self.wids['ventana'].window, 
                        self.wids['ventana'].get_style().bg[gtk.STATE_NORMAL], 
                        FLECHA_ARRIBA)
        self.PIXABAJO, self.MASKABAJO = gtk.gdk.pixmap_create_from_xpm_d(
                        self.wids['ventana'].window, 
                        self.wids['ventana'].get_style().bg[gtk.STATE_NORMAL], 
                        FLECHA_ABAJO)

    def add_empleados_a_tabla(self):
        """
        Añade los empleados y widgets correspondientes a la tabla.
        Si no existen los registros de control de horas, los crea, pues son 
        necesarios para referirse a los nombres de los widgets.
        """
        # DONE: ¿Qué pasa con los emplados que ya no trabajan al consultar 
        #       una fecha donde sí trabajaron? Hay registro pero no se 
        #       muestra. Se soluciona con el nuevo sistema de registros de 
        #       orden de empleados.
        try:
            fecha = utils.parse_fecha(self.wids['e_fecha'].get_text())
        except (mx.DateTime.RangeError, ValueError):
            self.wids['e_fecha'].set_text(
                utils.str_fecha(mx.DateTime.localtime()))
            fecha = utils.parse_fecha(self.wids['e_fecha'].get_text())
        cols = 16
        filas = 1
        # Empiezo la lista con todos los empleados dados de alta.
        empleados = pclases.Empleado.select(pclases.AND(
                            pclases.Empleado.q.planta == True, 
                            pclases.Empleado.q.activo == True),
                        orderBy = "apellidos")
        #orden = [26, 30, 15, 18, 9, 36, 22, 25, 11, 16, 20, 19, 
        #         10, 35, 28, 24, 32, 39, 29, 14, 43, 17, 33, 4]
        # Ahora los organizo según el orden, y los restantes los pongo al 
        # final.
        self.orden = pclases.OrdenEmpleados.buscar_registros(fecha)
        orden = [o.empleadoID for o in self.orden]
        ids = [e.id for e in empleados]
        empleados = []
        while orden:
            ide = orden.pop(0)
            if ide in ids:
                empleados.append(pclases.Empleado.get(ide))
                ids.remove(ide)
        for ide in ids:
            empleados.append(pclases.Empleado.get(ide))
        # Finalmente añado aquellos que en su día estuvieron dados de alta y 
        # ahora no. Por tanto no aparecen en la lista de empleados pero tienen 
        # un registro "controlHoras" que hay que mostrar porque va a entrar en 
        # los controles de verificación y demás. Además interesa consultar 
        # registros pasados de empleados que ya no están.
        chs = pclases.ControlHoras.select(pclases.ControlHoras.q.fecha==fecha)
        for ch in chs:
            if ch.empleado not in empleados:
                empleados.append(ch.empleado)
        # Y ahora sí, redimensiono e inserto los empleados por el orden final 
        # que ha quedado en la lista.
        filas += len(empleados)
        self.wids['tabla'].resize(filas, cols)
        fila = 1
        grupos = pclases.Grupo.select(orderBy = "nombre")
        grupos = [(g.id, g.nombre) for g in grupos]
        for e in empleados:
            asuntos_propios = pclases.Ausencia.select(pclases.AND(
                pclases.Ausencia.q.empleadoID == e.id, 
                pclases.Ausencia.q.fecha == fecha)).count() > 0
            baja = False
            for b in e.bajas:
                if b.esta_vigente(fecha):
                    baja = True
                    break
            try:
                ch = pclases.ControlHoras.select(pclases.AND(
                        pclases.ControlHoras.q.empleadoID == e.id, 
                        pclases.ControlHoras.q.fecha == fecha))[0]
            except IndexError:
                ch = pclases.ControlHoras(grupo = e.grupo, 
                                          empleado = e,
                                          fecha = fecha, 
                                          nocturnidad = False, 
                                          bloqueado = False, 
                                          festivo = False, 
                                          bajaLaboral = baja, 
                                          vacacionesYAsuntosPropios 
                                            = asuntos_propios)
                pclases.Auditoria.nuevo(ch, self.usuario, __file__)
            self.add_grupo(fila, ch, filas, grupos)
            self.add_empleado(fila, ch)
            self.add_horas_regulares(fila, ch)
            self.add_nocturnidad(fila, ch)
            self.add_horas_extras(fila, ch)
            self.add_horas_produccion(fila, ch)
            self.add_horas_mantenimiento(fila, ch)
            self.add_horas_almacen(fila, ch)
            self.add_horas_varios(fila, ch)
            self.add_comentarios(fila, ch)
            self.add_baja_laboral(fila, ch)
            self.add_vacaciones(fila, ch)
            fila += 1
        self.wids['tabla'].show_all()

    def intercambiar_fila(self, tabla, fo, fd):
        """
        Intercambia todos los widgets (apoyándose en el diccionaro de 
        widgets de la tabla self.hijos_tabla) de la fila fo y fd entre sí.
        """
        worigs = self.hijos_tabla[fo]
        wdests = self.hijos_tabla[fd]
        self.hijos_tabla[fo] = []
        self.hijos_tabla[fd] = []
        for wo in worigs:
            tabla.remove(wo['widget'])
            tabla.attach(wo['widget'], 
                         wo['left_attach'], 
                         wo['right_attach'], 
                         fd, 
                         fd + 1, 
                         *wo['resto_params'])
        for wd in wdests:
            tabla.remove(wd['widget'])
            tabla.attach(wd['widget'], 
                         wd['left_attach'], 
                         wd['right_attach'], 
                         fo, 
                         fo + 1, 
                         *wd['resto_params'])

    def mover(self, boton, incremento, filas):
        """
        Intenta mover la fila a la hilera + "incremento" de la tabla. Para 
        averiguar la fila busca en el diccionario interno el top_attach que 
        se usó al meter en la tabla al botón. Como botón no está, sino que 
        está su contenedor más externo hay que buscar dentro de todos los 
        contenedores al botón (buscamos expresamente el botón de 
        mover arriba, así que sabemos que hay 2 niveles de contenedores 
        antes de llegar a él).
        """
        for clavefila in self.hijos_tabla:
            for w in self.hijos_tabla[clavefila]:
                widget = w['widget']
                if isinstance(widget, gtk.Container): 
                        # Es contenedor o alguna de sus clases derivadas.
                    for hbox in widget.get_children():
                        if isinstance(hbox, gtk.Container):
                            for vbox in hbox.get_children():
                                if isinstance(vbox, gtk.Container):
                                    for arriba_o_abajo in vbox.get_children():
                                        if arriba_o_abajo == boton:
                                            fila = w['top_attach']
                                            break
        try:
            filadest = fila + incremento
            if 0 < filadest < filas:
                self.intercambiar_fila(self.wids['tabla'], fila, filadest)
                self.reordenar_registros()
                boton.grab_focus()
        except (NameError, UnboundLocalError):
            pass

    def reordenar_registros(self):
        """
        Reordena los registros de la BD para guardar el orden actual de IDs 
        de empleados.
        Si el registro no coincide con la fecha (se está usando el orden más 
        cercano de hace unos días) crea un conjunto nuevo de registros de 
        orden con el id de los empleados, el orden actual y la fecha.
        """
        joy_division = self.orden
        cardfilas = self.hijos_tabla.keys()
        cardfilas.sort()
        new_order = []
        regs_new_order = []
        for numfila in cardfilas:
            # El id del empleado lo saco del número que se guarda como nombre 
            # en todos los ebox exteriores.
            eid = int(self.hijos_tabla[numfila][0]['widget'].name)
            # PRECONDICIÓN: Al menos hay siempre un ebox en cada fila.
            new_order.append(eid)
        # Nuevo orden de empleados en new_order (¡Temptation! ¡temazo!)
        try:
            fecha = utils.parse_fecha(self.wids['e_fecha'].get_text())
        except:
            fecha = utils.parse_fecha(utils.str_fecha(mx.DateTime.localtime()))
        if joy_division and fecha == joy_division[0].fecha:
            # Modifico los registros existentes
            for i in range(len(new_order)):
                eid = new_order[i]
                try:
                    reg_orden = [o for o in joy_division 
                                 if o.empleadoID == eid][0]
                except IndexError:
                    # Tengo que crearlo, aunque no *debería* ocurrir.
                    reg_orden = pclases.OrdenEmpleados(empleadoID = eid, 
                                                       orden = i, 
                                                       fecha = fecha)
                    pclases.Auditoria.nuevo(reg_orden, self.usuario, __file__)
                else:
                    regs_new_order.append(reg_orden)
                    reg_orden.orden = i
        else:
            # Creo nuevos registros 
            for i in range(len(new_order)):
                eid = new_order[i]
                reg_orden = pclases.OrdenEmpleados(empleadoID = eid, 
                                                   orden = i, 
                                                   fecha = fecha)
                pclases.Auditoria.nuevo(reg_orden, self.usuario, __file__)
                regs_new_order.append(reg_orden)
        self.orden = regs_new_order

    def add_grupo(self, fila, ch, filas, grupos = None):
        """
        Añade el widget de grupo con su valor en la fila y columna de la tabla.
        """
        if grupos == None:
            grupos = pclases.Grupo.select(orderBy = "nombre")
            grupos = [(g.id, g.nombre) for g in grupos]
        tabla = self.wids['tabla']
        grupo = gtk.ComboBox()
        utils.rellenar_lista(grupo, grupos)
        self.wids['grupo_%d' % ch.id] = grupo
        utils.combo_set_from_db(grupo, ch.grupoID)
        ebox = gtk.EventBox()
        ebox.set_property("name", str(ch.empleadoID))
        hbox_en_ebox = gtk.HBox()
        vbox_botones = gtk.VBox()
        imarriba = gtk.Image()
        imarriba.set_from_pixmap(self.PIXARRIBA, self.MASKARRIBA)
        arriba = gtk.Button()
        arriba.add(imarriba)
        arriba.connect("clicked", self.mover, -1, filas)
        arriba.set_size_request(XBOTON, YBOTON)
        imabajo = gtk.Image()
        imabajo.set_from_pixmap(self.PIXABAJO, self.MASKABAJO)
        abajo = gtk.Button()
        abajo.add(imabajo)
        abajo.connect("clicked", self.mover, 1, filas)
        abajo.set_size_request(XBOTON, YBOTON)
        self.wids['arriba_%d' % ch.id] = arriba
        self.wids['abajo_%d' % ch.id] = abajo
        vbox_botones.add(arriba)
        vbox_botones.add(abajo)
        hbox_en_ebox.add(vbox_botones)
        hbox_en_ebox.add(grupo)
        ebox.add(hbox_en_ebox)
        #ebox.add(grupo)
        tips = gtk.Tooltips()
        tips.set_tip(ebox, "%s: Grupo" % 
            (ch.empleado.nombre + " " + ch.empleado.apellidos))
        tips.enable()
        tabla.attach(ebox, 
                     0, 1, 
                     fila, fila+1)
        def guardar_grupo(cb, ide):
            ch = pclases.ControlHoras.get(ide)
            ch.grupo = utils.combo_get_value(cb)
        grupo.connect("changed", guardar_grupo, ch.id)
        #grupo.connect("focus", 
        ebox.connect("focus", 
                      focusin, 
                      self.wids['scrolledwindow1'].get_hadjustment(),
                      self.wids['scrolledwindow1'].get_vadjustment())

    def add_empleado(self, fila, ch):
        """
        Añade el widget de grupo con su valor en la fila y columna de la tabla.
        """
        tabla = self.wids['tabla']
        empleado = gtk.Label(ch.empleado and 
                             ch.empleado.apellidos + ", " + ch.empleado.nombre
                             or "ERROR")
        empleado.set_markup("<small>%s</small>" % empleado.get_text())
        empleado.set_justify(gtk.JUSTIFY_LEFT)
        empleado.set_alignment(0.0, 0.5)
        self.wids['empleado_%d' % ch.id] = empleado
        ebox = gtk.EventBox()
        ebox.set_property("name", str(ch.empleadoID))
        ebox.add(empleado)
        tabla.attach(ebox, 
                     1, 2, 
                     fila, fila+1)
        empleado.connect("focus_in_event", 
                         focusin, 
                         self.wids['scrolledwindow1'].get_hadjustment(),
                         self.wids['scrolledwindow1'].get_vadjustment())

    def add_horas_regulares(self, fila, ch):
        """
        Añade el widget de horas regulares, su valor y la función de 
        autoguardado.
        """
        tabla = self.wids['tabla']
        horas = gtk.Entry()
        horas.set_alignment(0.9)
        horas.set_size_request(50, -1)
        horas.set_text(utils.float2str(ch.horasRegulares, autodec = True))
        self.wids['horas_regulares_%d' % ch.id] = horas
        ebox = gtk.EventBox()
        ebox.set_property("name", str(ch.empleadoID))
        ebox.add(horas)
        tips = gtk.Tooltips()
        tips.set_tip(ebox, "%s: Horas regulares" % 
            (ch.empleado.nombre + " " + ch.empleado.apellidos))
        tips.enable()
        tabla.attach(ebox, 
                     2, 3, 
                     fila, fila+1)
        def guardar(entry, ide):
            txt = entry.get_text()
            if txt:
                ch = pclases.ControlHoras.get(ide)
                try:
                    horas = utils._float(txt)
                    if not check_horas_regulares(ch, horas):
                        utils.dialogo_info(titulo = "ERROR NÚMERO HORAS", 
                                           texto = "Solo se permiten ocho "\
                                     "horas regulares como máximo por día.", 
                                           padre = self.wids['ventana'])
                        raise ValueError, "No se puede trabajar más de"\
                                          " 8 horas regulares por día."
                except:
                    entry.set_text(utils.float2str(ch.horasRegulares, 
                                                   autodec = True))
                else:
                    ch.horasRegulares = horas
        horas.connect("changed", guardar, ch.id)
        horas.connect("focus_in_event", 
                      focusin, 
                      self.wids['scrolledwindow1'].get_hadjustment(),
                      self.wids['scrolledwindow1'].get_vadjustment())

    def add_nocturnidad(self, fila, ch):
        tabla = self.wids['tabla']
        n = gtk.CheckButton()
        n.set_active(ch.nocturnidad)
        self.wids['nocturnidad_%d' % ch.id] = n
        alin = gtk.Alignment(0.5, 0.5)
        alin.add(n)
        ebox = gtk.EventBox()
        ebox.set_property("name", str(ch.empleadoID))
        ebox.add(alin)
        tips = gtk.Tooltips()
        tips.set_tip(ebox, "%s: Nocturnidad" % 
            (ch.empleado.nombre + " " + ch.empleado.apellidos))
        tips.enable()
        tabla.attach(ebox, 
                     3, 4, 
                     fila, fila+1)
        def guardar(chbox, ide):
            ch = pclases.ControlHoras.get(ide)
            ch.nocturnidad = chbox.get_active()
        n.connect("toggled", guardar, ch.id)
        n.connect("focus_in_event", 
                  focusin, 
                  self.wids['scrolledwindow1'].get_hadjustment(),
                  self.wids['scrolledwindow1'].get_vadjustment())

    def add_horas_extras(self, fila, ch):
        tabla = self.wids['tabla']
        he = gtk.Entry()
        he.set_alignment(0.9)
        he.set_has_frame(False)
        he.set_property("editable", False)
        he.set_text(utils.float2str(ch.calcular_total_horas_extras(), 
                                    autodec = True))
        he.set_size_request(50, -1)
        self.wids['horas_extras_%d' % ch.id] = he
        ebox = gtk.EventBox()
        ebox.set_property("name", str(ch.empleadoID))
        ebox.add(he)
        tips = gtk.Tooltips()
        tips.set_tip(ebox, "%s: Horas extras" % 
            (ch.empleado.nombre + " " + ch.empleado.apellidos))
        tips.enable()
        tabla.attach(ebox, 
                     4, 5, 
                     fila, fila+1, 
                     xoptions = gtk.SHRINK)
        he.connect("focus_in_event", 
                   focusin, 
                   self.wids['scrolledwindow1'].get_hadjustment(),
                   self.wids['scrolledwindow1'].get_vadjustment())
        boton_he = gtk.Button(stock = gtk.STOCK_ADD)
        self.wids['boton_horas_extras_%d' % ch.id] = boton_he
        ebox = gtk.EventBox()
        ebox.set_property("name", str(ch.empleadoID))
        ebox.add(boton_he)
        tips = gtk.Tooltips()
        tips.set_tip(ebox, "%s: Desglose de horas extras" % 
            (ch.empleado.nombre + " " + ch.empleado.apellidos))
        tips.enable()
        tabla.attach(ebox, 
                     5, 6, 
                     fila, fila+1)
        def abrir_popup(boton, ide):
            ch = pclases.ControlHoras.get(ide)
            v = gtk.Window()
            v.set_title("Desglose de horas extras")
            v.set_modal(True)
            v.set_transient_for(self.wids['ventana'])
            tabla = gtk.Table()
            tabla.resize(5, 3)
            label = gtk.Label("Producción:")
            tabla.attach(label, 0, 1, 1, 2)
            label = gtk.Label("Mantenimiento:")
            tabla.attach(label, 0, 1, 2, 3)
            label = gtk.Label("Almacén:")
            tabla.attach(label, 0, 1, 3, 4)
            label = gtk.Label("Varios:")
            tabla.attach(label, 0, 1, 4, 5)
            pd = gtk.Entry()
            pd.set_alignment(0.9)
            pd.set_text(utils.float2str(ch.horasExtraDiaProduccion, 
                                        autodec = True))
            pd.connect("activate", lambda *args, **kw: v.destroy())
            md = gtk.Entry()
            md.set_alignment(0.9)
            md.set_text(utils.float2str(ch.horasExtraDiaMantenimiento, 
                                        autodec = True))
            md.connect("activate", lambda *args, **kw: v.destroy())
            ad = gtk.Entry()
            ad.set_alignment(0.9)
            ad.set_text(utils.float2str(ch.horasExtraDiaAlmacen, 
                                        autodec = True))
            ad.connect("activate", lambda *args, **kw: v.destroy())
            vd = gtk.Entry()
            vd.set_alignment(0.9)
            vd.set_text(utils.float2str(ch.horasExtraDiaVarios, 
                                        autodec = True))
            vd.connect("activate", lambda *args, **kw: v.destroy())
            tabla.attach(gtk.Label("Día:"), 1, 2, 0, 1)
            tabla.attach(pd, 1, 2, 1, 2)
            tabla.attach(md, 1, 2, 2, 3)
            tabla.attach(ad, 1, 2, 3, 4)
            tabla.attach(vd, 1, 2, 4, 5)
            pn = gtk.Entry()
            pn.set_alignment(0.9)
            pn.set_text(utils.float2str(ch.horasExtraNocheProduccion, 
                                        autodec = True))
            pn.connect("activate", lambda *args, **kw: v.destroy())
            mn = gtk.Entry()
            mn.set_alignment(0.9)
            mn.set_text(utils.float2str(ch.horasExtraNocheMantenimiento, 
                                        autodec = True))
            mn.connect("activate", lambda *args, **kw: v.destroy())
            an = gtk.Entry()
            an.set_alignment(0.9)
            an.set_text(utils.float2str(ch.horasExtraNocheAlmacen, 
                                        autodec = True))
            an.connect("activate", lambda *args, **kw: v.destroy())
            vn = gtk.Entry()
            vn.set_alignment(0.9)
            vn.set_text(utils.float2str(ch.horasExtraNocheVarios, 
                                        autodec = True))
            vn.connect("activate", lambda *args, **kw: v.destroy())
            tabla.attach(gtk.Label("Noche:"), 2, 3, 0, 1)
            tabla.attach(pn, 2, 3, 1, 2)
            tabla.attach(mn, 2, 3, 2, 3)
            tabla.attach(an, 2, 3, 3, 4)
            tabla.attach(vn, 2, 3, 4, 5)
            v.add(tabla)
            v.show_all()
            era_fullscreen = False
            if self._is_fullscreen:
                self.wids['ventana'].unfullscreen()
                self._is_fullscreen = False
                era_fullscreen = True
            def cerrar_y_actualizar(ventana, ide, 
                                    pd, md, ad, vd, pn, mn, an, vn):
                ch = pclases.ControlHoras.get(ide)
                for campo, entry in (("horasExtraDiaProduccion", pd), 
                                     ("horasExtraDiaMantenimiento", md), 
                                     ("horasExtraDiaAlmacen", ad), 
                                     ("horasExtraDiaVarios", vd), 
                                     ("horasExtraNocheProduccion", pn), 
                                     ("horasExtraNocheMantenimiento", mn), 
                                     ("horasExtraNocheAlmacen", an), 
                                     ("horasExtraNocheVarios", vn)):
                    try:
                        h = utils._float(entry.get_text())
                    except:
                        h = 0
                    setattr(ch, campo, h)
                he = self.wids['horas_extras_%d' % ide]
                he.set_text(utils.float2str(ch.calcular_total_horas_extras(), 
                                            autodec = True))
                if era_fullscreen:
                    self.wids['ventana'].fullscreen()
                    self._is_fullscreen = True
            v.connect("destroy", cerrar_y_actualizar, 
                                 ide, pd, md, ad, vd, pn, mn, an, vn)
        boton_he.connect("clicked", abrir_popup, ch.id)
        boton_he.connect("focus_in_event", 
                         focusin, 
                         self.wids['scrolledwindow1'].get_hadjustment(),
                         self.wids['scrolledwindow1'].get_vadjustment())

    def add_horas_produccion(self, fila, ch):
        tabla = self.wids['tabla']
        hp = gtk.Entry()
        hp.set_alignment(0.9)
        hp.set_size_request(50, -1)
        hp.set_has_frame(False)
        hp.set_property("editable", False)
        hp.set_text(utils.float2str(ch.calcular_total_horas_produccion(), 
                                    autodec = True))
        self.wids['horas_produccion_%d' % ch.id] = hp
        ebox = gtk.EventBox()
        ebox.set_property("name", str(ch.empleadoID))
        ebox.add(hp)
        tips = gtk.Tooltips()
        tips.set_tip(ebox, "%s: Horas de producción" % 
            (ch.empleado.nombre + " " + ch.empleado.apellidos))
        tips.enable()
        tabla.attach(ebox, 
                     6, 7, 
                     fila, fila+1, 
                     xoptions = gtk.SHRINK)
        hp.connect("focus_in_event", 
                   focusin, 
                   self.wids['scrolledwindow1'].get_hadjustment(),
                   self.wids['scrolledwindow1'].get_vadjustment())
        boton = gtk.Button(stock = gtk.STOCK_ADD)
        self.wids['boton_horas_produccion_%d' % ch.id] = boton
        ebox = gtk.EventBox()
        ebox.set_property("name", str(ch.empleadoID))
        ebox.add(boton)
        tips = gtk.Tooltips()
        tips.set_tip(ebox, "%s: Desglose de horas de producción por línea" % 
            (ch.empleado.nombre + " " + ch.empleado.apellidos))
        tips.enable()
        tabla.attach(ebox, 
                     7, 8, 
                     fila, fila+1)
        def abrir_popup(boton, ide):
            ch = pclases.ControlHoras.get(ide)
            v = gtk.Window()
            v.set_title("Desglose de horas de producción")
            v.set_modal(True)
            v.set_transient_for(self.wids['ventana'])
            tabla = gtk.Table()
            lineas = pclases.LineaDeProduccion.select(orderBy = "-id")
            tabla.resize(lineas.count() + 1, 2)
            tabla.attach(gtk.Label("Horas"), 1, 2, 0, 1)
            fila = 1
            entries = {}
            for linea in lineas:
                try:
                    h = pclases.ControlHorasProduccion.select(pclases.AND(
                            pclases.ControlHorasProduccion\
                                .q.lineaDeProduccionID == linea.id, 
                            pclases.ControlHorasProduccion\
                                .q.controlHorasID == ide))[0]
                except IndexError:
                    h = pclases.ControlHorasProduccion(
                            lineaDeProduccion = linea, 
                            controlHorasID = ide)
                    pclases.Auditoria.nuevo(h, self.usuario, __file__)
                entries[h] = gtk.Entry()
                entries[h].set_alignment(0.9)
                tabla.attach(gtk.Label(linea.nombre), 0, 1, fila, fila+1)
                tabla.attach(entries[h], 1, 2, fila, fila+1)
                entries[h].set_text(utils.float2str(h.horasProduccion, 
                                                    autodec = True))
                entries[h].connect("activate", lambda *args, **kw: v.destroy())
                fila += 1
            v.add(tabla)
            v.show_all()
            era_fullscreen = False
            if self._is_fullscreen:
                self.wids['ventana'].unfullscreen()
                self._is_fullscreen = False
                era_fullscreen = True
            def cerrar_y_actualizar(ventana, ide, entries):
                for horaslinea in entries:
                    entry = entries[horaslinea]
                    try:
                        horas = utils._float(entry.get_text())
                    except (TypeError, ValueError):
                        horas = 0
                    horaslinea.horasProduccion = horas
                he = self.wids['horas_produccion_%d' % ide]
                he.set_text(utils.float2str(
                                ch.calcular_total_horas_produccion(), 
                                autodec = True))
                if era_fullscreen:
                    self.wids['ventana'].fullscreen()
                    self._is_fullscreen = True
            v.connect("destroy", cerrar_y_actualizar, ide, entries)
        boton.connect("clicked", abrir_popup, ch.id)
        boton.connect("focus_in_event", 
                      focusin, 
                      self.wids['scrolledwindow1'].get_hadjustment(),
                      self.wids['scrolledwindow1'].get_vadjustment())

    def add_horas_mantenimiento(self, fila, ch):
        tabla = self.wids['tabla']
        hm = gtk.Entry()
        hm.set_alignment(0.9)
        hm.set_size_request(50, -1)
        hm.set_has_frame(False)
        hm.set_property("editable", False)
        hm.set_text(utils.float2str(ch.calcular_total_horas_mantenimiento(), 
                                    autodec = True))
        self.wids['horas_mantenimiento_%d' % ch.id] = hm
        ebox = gtk.EventBox()
        ebox.set_property("name", str(ch.empleadoID))
        ebox.add(hm)
        tips = gtk.Tooltips()
        tips.set_tip(ebox, "%s: Horas de mantenimiento" % 
            (ch.empleado.nombre + " " + ch.empleado.apellidos))
        tips.enable()
        tabla.attach(ebox, 
                     8, 9, 
                     fila, fila+1, 
                     xoptions = gtk.SHRINK)
        hm.connect("focus_in_event", 
                   focusin, 
                   self.wids['scrolledwindow1'].get_hadjustment(),
                   self.wids['scrolledwindow1'].get_vadjustment())
        boton = gtk.Button(stock = gtk.STOCK_ADD)
        self.wids['boton_horas_mantenimiento_%d' % ch.id] = boton
        ebox = gtk.EventBox()
        ebox.set_property("name", str(ch.empleadoID))
        ebox.add(boton)
        tips = gtk.Tooltips()
        tips.set_tip(ebox, "%s: Desglose de horas de mantenimiento" % 
            (ch.empleado.nombre + " " + ch.empleado.apellidos))
        tips.enable()
        tabla.attach(ebox, 
                     9, 10, 
                     fila, fila+1)
        def abrir_popup(boton, ide):
            ch = pclases.ControlHoras.get(ide)
            v = gtk.Window()
            v.set_title("Desglose de horas de mantenimiento")
            v.set_modal(True)
            v.set_transient_for(self.wids['ventana'])
            tabla = gtk.Table()
            lineas = pclases.LineaDeProduccion.select(orderBy = "-id")
            tabla.resize(lineas.count() + 1, 2)
            tabla.attach(gtk.Label("Horas"), 1, 2, 0, 1)
            fila = 1
            entries = {}
            for linea in lineas:
                try:
                    h = pclases.ControlHorasMantenimiento.select(pclases.AND(
                            pclases.ControlHorasMantenimiento\
                                .q.lineaDeProduccionID == linea.id, 
                            pclases.ControlHorasMantenimiento\
                                .q.controlHorasID == ide))[0]
                except IndexError:
                    h = pclases.ControlHorasMantenimiento(
                            lineaDeProduccion = linea, 
                            controlHorasID = ide)
                    pclases.Auditoria.nuevo(h, self.usuario, __file__)
                entries[h] = gtk.Entry()
                entries[h].set_alignment(0.9)
                tabla.attach(gtk.Label(linea.nombre), 0, 1, fila, fila+1)
                tabla.attach(entries[h], 1, 2, fila, fila+1)
                entries[h].set_text(utils.float2str(h.horasMantenimiento, 
                                                    autodec = True))
                entries[h].connect("activate", lambda *args, **kw: v.destroy())
                fila += 1
            v.add(tabla)
            v.show_all()
            era_fullscreen = False
            if self._is_fullscreen:
                self.wids['ventana'].unfullscreen()
                self._is_fullscreen = False
                era_fullscreen = True
            def cerrar_y_actualizar(ventana, ide, entries):
                for horaslinea in entries:
                    entry = entries[horaslinea]
                    try:
                        horas = utils._float(entry.get_text())
                    except (TypeError, ValueError):
                        horas = 0
                    horaslinea.horasMantenimiento = horas
                he = self.wids['horas_mantenimiento_%d' % ide]
                he.set_text(utils.float2str(
                                ch.calcular_total_horas_mantenimiento(), 
                                autodec = True))
                if era_fullscreen:
                    self.wids['ventana'].fullscreen()
                    self._is_fullscreen = True
            v.connect("destroy", cerrar_y_actualizar, ide, entries)
        boton.connect("clicked", abrir_popup, ch.id)
        boton.connect("focus_in_event", 
                      focusin, 
                      self.wids['scrolledwindow1'].get_hadjustment(),
                      self.wids['scrolledwindow1'].get_vadjustment())

    def add_horas_almacen(self, fila, ch):
        tabla = self.wids['tabla']
        ha = gtk.Entry()
        ha.set_alignment(0.9)
        ha.set_size_request(50, -1)
        ha.set_text(utils.float2str(ch.horasAlmacen, autodec = True))
        self.wids['horas_almacen_%d' % ch.id] = ha
        ebox = gtk.EventBox()
        ebox.set_property("name", str(ch.empleadoID))
        ebox.add(ha)
        tips = gtk.Tooltips()
        tips.set_tip(ebox, "%s: Horas de almacén" % 
            (ch.empleado.nombre + " " + ch.empleado.apellidos))
        tips.enable()
        tabla.attach(ebox, 
                     10, 11, 
                     fila, fila+1, 
                     xoptions = gtk.SHRINK)
        def guardar(entry, ide):
            txt = entry.get_text()
            if txt:
                ch = pclases.ControlHoras.get(ide)
                try:
                    ch.horasAlmacen = utils._float(txt)
                except:
                    entry.set_text(utils.float2str(ch.horasAlmacen, 
                                                   autodec = True))
        ha.connect("changed", guardar, ch.id)
        ha.connect("focus_in_event", 
                   focusin, 
                   self.wids['scrolledwindow1'].get_hadjustment(),
                   self.wids['scrolledwindow1'].get_vadjustment())

    def add_horas_varios(self, fila, ch):
        tabla = self.wids['tabla']
        hv = gtk.Entry()
        hv.set_alignment(0.9)
        hv.set_size_request(50, -1)
        hv.set_text(utils.float2str(ch.horasVarios, autodec = True))
        self.wids['horas_varios_%d' % ch.id] = hv
        ebox = gtk.EventBox()
        ebox.set_property("name", str(ch.empleadoID))
        ebox.add(hv)
        tips = gtk.Tooltips()
        tips.set_tip(ebox, "%s: Horas en tareas varias" % 
            (ch.empleado.nombre + " " + ch.empleado.apellidos))
        tips.enable()
        tabla.attach(ebox, 
                     11, 12, 
                     fila, fila+1, 
                     xoptions = gtk.SHRINK)
        hv.connect("focus_in_event", 
                   focusin, 
                   self.wids['scrolledwindow1'].get_hadjustment(),
                   self.wids['scrolledwindow1'].get_vadjustment())
        lista_hv = gtk.ComboBoxEntry()
        textos = [c.varios for c in pclases.ControlHoras.select(
                    pclases.ControlHoras.q.varios != "")]
        textos = utils.unificar_textos(textos)
        textos.sort()
        textos = zip(range(len(textos)), textos)
        utils.rellenar_lista(lista_hv, textos)
        lista_hv.child.set_text(ch.varios)
        self.wids['varios_%d' % ch.id] = lista_hv
        ebox = gtk.EventBox()
        ebox.set_property("name", str(ch.empleadoID))
        ebox.add(lista_hv)
        tips = gtk.Tooltips()
        tips.set_tip(ebox, "%s: Especifique la labor realizada" % 
            (ch.empleado.nombre + " " + ch.empleado.apellidos))
        tips.enable()
        tabla.attach(ebox, 
                     12, 13, 
                     fila, fila+1)
        def guardar(entry, ide):
            txt = entry.get_text()
            if txt:
                ch = pclases.ControlHoras.get(ide)
                try:
                    ch.horasVarios = utils._float(txt)
                except:
                    entry.set_text(utils.float2str(ch.horasVarios, 
                                                   autodec = True))
        hv.connect("changed", guardar, ch.id)
        def guardar_combo(cb, ide):
            ch = pclases.ControlHoras.get(ide)
            ch.varios = cb.child.get_text()
        lista_hv.connect("changed", guardar_combo, ch.id)
        lista_hv.connect("focus_in_event", 
                         focusin, 
                         self.wids['scrolledwindow1'].get_hadjustment(),
                         self.wids['scrolledwindow1'].get_vadjustment())

    def add_comentarios(self, fila, ch):
        tabla = self.wids['tabla']
        comentarios = gtk.Entry()
        comentarios.set_text(ch.comentarios)
        self.wids['comentarios_%d' % ch.id] = comentarios
        ebox = gtk.EventBox()
        ebox.set_property("name", str(ch.empleadoID))
        ebox.add(comentarios)
        tips = gtk.Tooltips()
        tips.set_tip(ebox, "%s: Comentarios y observaciones" % 
            (ch.empleado.nombre + " " + ch.empleado.apellidos))
        tips.enable()
        tabla.attach(ebox, 
                     13, 14, 
                     fila, fila+1)
        def guardar(entry, ide):
            txt = entry.get_text()
            ch = pclases.ControlHoras.get(ide)
            ch.comentarios = txt
        comentarios.connect("changed", guardar, ch.id)
        comentarios.connect("focus_in_event", 
                            focusin, 
                            self.wids['scrolledwindow1'].get_hadjustment(),
                            self.wids['scrolledwindow1'].get_vadjustment())

    def add_baja_laboral(self, fila, ch):
        tabla = self.wids['tabla']
        n = gtk.CheckButton()
        n.set_active(ch.bajaLaboral)
        self.wids['baja_laboral_%d' % ch.id] = n
        alin = gtk.Alignment(0.5, 0.5)
        alin.add(n)
        ebox = gtk.EventBox()
        ebox.set_property("name", str(ch.empleadoID))
        ebox.add(alin)
        tips = gtk.Tooltips()
        tips.set_tip(ebox, "%s: Baja laboral" % 
            (ch.empleado.nombre + " " + ch.empleado.apellidos))
        tips.enable()
        tabla.attach(ebox, 
                     14, 15, 
                     fila, fila+1) 
        def guardar(chbox, ide):
            ch = pclases.ControlHoras.get(ide)
            esta_de_baja = False
            for baja in ch.empleado.bajas:
                if baja.esta_vigente(ch.fecha):
                    esta_de_baja = True
                    break
            if (not chbox.get_active() and  # Está desmarcando 
                esta_de_baja):              # pero está de baja 
                utils.dialogo_info(titulo = "EMPLEADO DE BAJA", 
                                   texto = "Modifique las bajas médicas"\
                        " desde la ventana correspondiente antes de marcar"\
                        " al empleado como disponible.", 
                                   padre = self.wids['ventana'])
            else:
                ch.bajaLaboral = chbox.get_active()
            chbox.set_active(ch.bajaLaboral)
        n.connect("toggled", guardar, ch.id)
        n.connect("focus_in_event", 
                  focusin, 
                  self.wids['scrolledwindow1'].get_hadjustment(),
                  self.wids['scrolledwindow1'].get_vadjustment())

    def add_vacaciones(self, fila, ch):
        tabla = self.wids['tabla']
        n = gtk.CheckButton()
        n.set_active(ch.vacacionesYAsuntosPropios)
        self.wids['vacaciones_%d' % ch.id] = n
        alin = gtk.Alignment(0.5, 0.5)
        alin.add(n)
        ebox = gtk.EventBox()
        ebox.set_property("name", str(ch.empleadoID))
        ebox.add(alin)
        tabla.attach(ebox, 
                     15, 16, 
                     fila, fila+1) 
        tips = gtk.Tooltips()
        tips.set_tip(ebox, "%s: Vacaciones y asuntos propios" % 
            (ch.empleado.nombre + " " + ch.empleado.apellidos))
        tips.enable()
        def guardar(chbox, ide):
            ch = pclases.ControlHoras.get(ide)
            asuntos_propios = pclases.Ausencia.select(pclases.AND(
                pclases.Ausencia.q.empleadoID == ch.empleado.id, 
                pclases.Ausencia.q.fecha == ch.fecha)).count() > 0
            if (not chbox.get_active() and  # Está desmarcando 
                asuntos_propios):           # pero tiene registros de ausencia
                utils.dialogo_info(titulo = "EMPLEADO CON AUSENCIA", 
                                   texto = "Modifique las ausencias y permiso"\
                            "s desde la ventana correspondiente antes de marc"\
                            "ar al empleado como disponible.", 
                                   padre = self.wids['ventana'])
            else:
                ch.vacacionesYAsuntosPropios = chbox.get_active()
            chbox.set_active(ch.vacacionesYAsuntosPropios)
        n.connect("toggled", guardar, ch.id)
        n.connect("focus_in_event", 
                  focusin, 
                  self.wids['scrolledwindow1'].get_hadjustment(),
                  self.wids['scrolledwindow1'].get_vadjustment())

    def activar_widgets(self, s, chequear_permisos = True):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        #if self.objeto == None:
        #    s = False
        ws = tuple(["tabla", "e_fecha", "ch_festivo", "ch_bloqueado"])
        for w in ws:
            try:
                self.wids[w].set_sensitive(s)
            except Exception, msg:
                print "Widget problemático:", w, "Excepción:", msg
                import traceback
                traceback.print_last()
        if chequear_permisos:
            self.check_permisos(nombre_fichero_ventana = "control_personal.py")

    def limpiar_tabla(self):
        """
        Elimina los widgets de la tabla desde la fila 1 al final.
        """
        tabla = self.wids['tabla']
        #self.hijos_tabla = {}
        for hijo in tabla.get_children():
            if not "label" in hijo.get_name():
                tabla.remove(hijo)

    def rellenar_widgets(self):
        """
        Introduce la información del objeto actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        try:
            fecha = utils.parse_fecha(self.wids['e_fecha'].get_text())
        except:
            fecha = utils.parse_fecha(utils.str_fecha(mx.DateTime.localtime()))
        self.limpiar_tabla()
        self.add_empleados_a_tabla()
        chs = pclases.ControlHoras.select(pclases.ControlHoras.q.fecha==fecha)
        self.wids['e_dia_semana'].set_text(fecha.strftime("%A"))
        # Con que haya un festivo o un bloqueado en los registros del día, 
        # basta.
        self.wids['ch_bloqueado'].set_active(
            bool([c for c in chs if c.bloqueado]))
        self.wids['ch_festivo'].set_active(
            bool([c for c in chs if c.festivo]))
        # Para chequear los permisos de la ventana necesito un objeto. Con el 
        # primero de ellos basta para verificar las condiciones de bloqueo:
        try:
            self.objeto = chs[0]
        except IndexError:
            self.objeto = None
        self.wids['tabla'].foreach(conectar_color_foco, 
                                   self.wids['tabla']) 
        for clave in self.wids.keys():
            w = self.wids[clave]
            if isinstance(w, gtk.ComboBoxEntry) and w.child != None:
                w.child.connect("key_press_event",cambiar_cursor_por_tabulador)
            elif isinstance(w, (gtk.Entry, gtk.CheckButton, 
                                gtk.ComboBox, gtk.Button)):
                if w.name != "e_fecha": # Por comodidad para editar la fecha
                    w.connect("key_press_event", cambiar_cursor_por_tabulador)
        # Si usuario tiene nivel 0 ó 1 debería dejarle editar siempre.
        if self.usuario and self.usuario.nivel > 2:
            self.wids['tabla'].set_sensitive(check_dias_consecutivos(fecha))
        else:
            self.wids['tabla'].set_sensitive(True)

def cambiar_cursor_por_tabulador(w, e):
    res = False
    if e.keyval == 65363:   # ->
        w.get_toplevel().child_focus(gtk.DIR_TAB_FORWARD)
        res = True # Así evito que se siga propagando la pulsación del cursor.
    elif e.keyval == 65361: # <-
        w.get_toplevel().child_focus(gtk.DIR_TAB_BACKWARD)
        res = True # y se mueva el foco dos veces seguidas en combos y botones.
    return res  # Mientras que para el resto de teclas (números y tal) se 
                # comporta como debe. Devolviendo siempre True no manda las 
                # pulsaciones y no escribiría en los Entries.

def resaltar_si_foco(w, direccion, tabla):
    alloc = w.get_allocation()
    #print alloc.y
    for hijo in tabla.get_children():
        alloc_hijo = hijo.get_allocation()
        if alloc_hijo.y == alloc.y:
        #if hijo is w:
            color = hijo.get_colormap().alloc_color("yellow")
        else:
            color = None
        hijo.modify_bg(gtk.STATE_NORMAL, color)

def conectar_color_foco(w, tabla):
    try:
        w.connect("set-focus-child", resaltar_si_foco, tabla)
    except TypeError:   # No es un gtk.EventBox
        pass


if __name__ == "__main__":
    p = ControlPersonal()

