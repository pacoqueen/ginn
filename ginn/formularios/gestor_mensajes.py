#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2020  Francisco José Rodríguez Bogado,                   #
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
# gestor_mensajes.py -- Gestor de mensajes y alertas de usuarios.
###################################################################
# NOTAS:
##
# ----------------------------------------------------------------
##
###################################################################
# Changelog:
# 27 de abril de 2006 -> Inicio
##
##
###################################################################
# FIXME:
# OJO: Hay un BUG en SQLObject 0.6.1 que ignora los DEFAULTs en
# los campos BOOLEAN de la base de datos y usa siempre True como
# valor por defecto aunque en la tabla se haya especificado
# BOOLEAN DEFAULT False.
# La clase Widget también debería hacer saltar una excepción
# cuando se accede a un widget que no existe, en lugar de devolver
# None. Opino. <-- Esto ya está hecho.
###################################################################
from formularios.widgets import Widgets
from framework import pclases
import os
from gi import pygtkcompat
import gi
gi.require_version("Gtk", '3.0')

try:
    from gi import pygtkcompat
except importerror:
    pygtkcompat = none
    from gi.repository import Gtk as gtk
    from gi.repository import GObject as gobject

if pygtkcompat is not None:
    pygtkcompat.enable()
    pygtkcompat.enable_gtk(version='3.0')
    import gtk
    import gobject


def eliminar_temporales():
    """
    Trata de eliminar todos los archivos temporales del usuario para evitar
    que al generar una etiqueta, código de barras, etc. se quede pillado
    el programa y pete.
    """
    from tempfile import gettempdir
    for root, dirs, files in os.walk(gettempdir()):  # @UnusedVariable
        for fich in files:
            try:
                # print os.path.join(root, fich)
                os.unlink(os.path.join(root, fich))
                # ¿Realmente necesito borrar solo los de ayer y anteriores?
                # Se acaba de abrir el menú principal. No puede haber
                # etiquetas recién creadas y no impresas. Y si las hay,
                # el visor de PDF ya las tiene en memoria y no pasa nada por
                # borrar el archivo... a no ser que esté en Winmerde y no
                # me deje. Exception powah!
            except (OSError, IOError):
                pass    # Protegido, bloqueado... da igual. Sigo borrando.


class GestorMensajes:
    def __init__(self, usuario):
        """
        Constructor.
        Recibe un objeto usuario.
        """
        # XXX: Procesos automáticos:
        pclases.Confirming.actualizar_estado_cobro()
        pclases.PagareCobro.actualizar_estado_cobro()
        pclases.PagarePago.actualizar_estado_cobro()
        pclases.VencimientoPago.actualizar_estado_pago_domiciliaciones()
        eliminar_temporales()
        # XXX: EOPA

        self.__usuario = usuario
        if self.__usuario == None:
            print(__file__, "ERROR: Intentando iniciar gestor de mensajes "
                  "con usuario inválido.")
        else:
            self.__pendientes = self.comprobar_pendientes()
            if self.__pendientes:
                self.run()

    def comprobar_pendientes(self):
        no_entregados = pclases.Alerta.select(
            """ usuario_id = %d AND entregado = FALSE """ % (
                self.__usuario.id))
        return [a for a in no_entregados if "bajo mínimos" not in a.mensaje]

    def mostrar_alerta(self, a):
        """
        a es un objeto Alerta.
        Muestra una ventana con el mensaje de la alerta y
        modifica la recepción si se marca la casilla
        correspondiente.
        Devuelve la longitud de alertas pendientes que quedan
        por mostrar.
        """
        mensaje = a.mensaje
        fecha = a.fechahora.strftime("%d/%m/%Y a las %H:%M")
        ventana = self.construir_ventana(
            fecha, mensaje, len(self.__pendientes))
        a.entregado = self.mostrar_ventana(ventana, a)
        if a.entregado:
            try:
                self.__pendientes.remove(a)
            except ValueError:
                pass    # el mensaje «a» ya fue eliminado de pendientes.
        return len(self.__pendientes)

    def construir_ventana(self, f, m, p):
        """
        f -> Fecha y hora en forma de cadena
        m -> Mensaje.
        p -> Número de alertas pendientes del usuario
        Construye y devuelve un Widgets con la información
        de la alerta y una casilla para confirmar la lectura.
        """
        ventana = Widgets('alerta.glade')
        ventana['fecha'].set_text('<b>%s</b>' % f)
        ventana['fecha'].set_use_markup(True)
        ventana['mensaje'].get_buffer().set_text(m)
        ventana['no_leidos'].set_text('<i>%d alertas pendientes.</i>' % p)
        ventana['no_leidos'].set_use_markup(True)
        ventana['confirmado'].set_active(True)
        ventana['ch_todos'].set_active(False)
        return ventana

    def cambiar_contador_pendientes(self, togglebutton, label_pendientes, res):
        if togglebutton.get_active():
            p = len(self.__pendientes) - 1
            # La alerta actual está pendiente hasta que cierre la ventana.
            # Así que resto uno al total de pendientes para que se muestre
            # en el resto de pendientes el mensaje actual como leído (aunque
            # realmente no quede leído hasta que cierre).
            res[0] = True
        else:
            p = len(self.__pendientes)
            res[0] = False
        label_pendientes.set_text('<i>%d alertas pendientes.</i>' % p)
        label_pendientes.set_use_markup(True)

    def aceptar(self, boton, ventana, alerta):
        if ventana['ch_todos'].get_active():
            for a in [a for a in self.__pendientes if a != alerta]:
                # La alerta original se eliminará después, por eso la respeto
                # en este for.
                a.entregado = True
                self.__pendientes.remove(a)
        ventana['ventana'].destroy()

    def mostrar_ventana(self, ventana, alerta):
        """
        Recibe un objeto Window de GTK. Lo muestra y devuelve
        si se marcó o no la casilla "Confirmar lectura".
        """
        res = [True]
        ventana['b_aceptar'].connect("clicked", self.aceptar, ventana, alerta)
        ventana['confirmado'].connect("toggled",
                                      self.cambiar_contador_pendientes, ventana['no_leidos'], res)
        ventana['ventana'].connect("destroy", gtk.main_quit)
        gtk.main()  # Saldrá de aquí con el main_quit
        return res[0]

    def nueva_alerta(self, texto):
        self.__usuario.enviar_mensaje(texto)

    def run(self):
        """
        Realiza una nueva "pasada" del gestor de mensajes en
        busca de mensajes sin confirmar. Si hay, inicia la
        rutina gráfica de Gtk y los muestra.
        """
        self.__pendientes = self.comprobar_pendientes()
        for a in self.__pendientes[:]:
            # Hago una copia de la lista de pendientes porque
            # probablemente se modificará durante el recorrido.
            if self.mostrar_alerta(a) == 0:
                break


if __name__ == '__main__':
    gm = GestorMensajes()
    # pclases.Usuario.select(pclases.Usuario.q.usuario=='admin')[0])
#    gm.nueva_alerta('Esto es una alerta de prueba')
#    gm.nueva_alerta('Esto es otra alerta')
#    gm.nueva_alerta("""Oh! Otra alerta más. Y esta a demás tiene un montón de texto. Pero no un montón de eso que dices "bueno, es un montoncito", no. Esto es un montón pero un montón de verdad. Meet the new boss... same as the old boss. My name is Ivor, I'm an engine driver.
#    I'm taking a ride with my best friend.
#    Never let me down... again""")
#    gm.run()
