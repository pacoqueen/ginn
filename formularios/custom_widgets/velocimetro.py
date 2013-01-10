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
<<<<<<< HEAD
# Reconocimiento del código del widget de escala de estrellas a quien 
=======
# Reconocimiento del código del widget de escala de estrellas a quien
>>>>>>> master
# corresponda (ver docstring de la clase).
###############################################################################

try:
    import gtk
    import gobject
    from gtk import gdk
except:
    raise SystemExit
<<<<<<< HEAD
    
=======

>>>>>>> master

import pygtk
if gtk.pygtk_version < (2, 0):
    print "Se necesita PyGtk 2.0 o posterior."
    raise SystemExit
<<<<<<< HEAD
  
=======

>>>>>>> master
class Velocimetro(gtk.Widget):
    """
    Especie de velocímetro analógico. A ver qué sale.
    """
<<<<<<< HEAD
    
=======

>>>>>>> master
    def __init__(self, minimo = 0.0, maximo = 100.0, posicion = 50.0):
        """
        Inicialización.
        Mínimo es el mínimo de la escala.
        Máximo es el máximo.
<<<<<<< HEAD
        Posición es la posición inicial. 
        Siempre debe cumplirse que mínimo <= posición <= máximo.
        """
        
=======
        Posición es la posición inicial.
        Siempre debe cumplirse que mínimo <= posición <= máximo.
        """

>>>>>>> master
        assert minimo <= posicion <= maximo, "Error. Asegúrese de que mínimo <= posición <= máximo."

        #Inicialización del Widget
        gtk.Widget.__init__(self)
<<<<<<< HEAD
        
        self.minimo = minimo
        self.maximo = maximo
        self.posicion = posicion
        self.radio = 75     # 100 píxeles de radio para empezar está bien. Si se redimensiona, 
=======

        self.minimo = minimo
        self.maximo = maximo
        self.posicion = posicion
        self.radio = 75     # 100 píxeles de radio para empezar está bien. Si se redimensiona,
>>>>>>> master
                            # este radio debe crecer/disminuir acorde con ello.
        self.borde = 5      # Tamaño del borde entre el círculo y el fin del Widget. Ancho total = borde * 2 + radio * 2
        import os
        if "svg" in [i['name'] for i in gtk.gdk.pixbuf_get_formats()]:
            fondo = gtk.gdk.pixbuf_new_from_file(os.path.join(
<<<<<<< HEAD
                os.path.abspath(os.path.dirname(__file__)), 
=======
                os.path.abspath(os.path.dirname(__file__)),
>>>>>>> master
                "..", "..", "imagenes", "velocimetro.svg"))
        else:     # MS-Windows no se lleva bien con un formato tan bonito como SVG. Vaya "usté" a saber por qué capricho del destino.
            fondo = gtk.gdk.pixbuf_new_from_file(os.path.join("..", "imagenes", "velocimetro.png"))
        self.fondo = fondo.scale_simple((self.radio + self.borde) * 2, (self.radio + self.borde) * 2, gtk.gdk.INTERP_BILINEAR)
<<<<<<< HEAD
        
    def do_realize(self):
        """
        Se invoca cada vez que el widget debe crear todos sus 
        recursos de ventana. Crearemos nuestro gtk.gdk.Window 
        y cargaremos la aguja indicadora.
        """
        # Primero establecemos el flag interno indicando que estamos "realized". 
=======

    def do_realize(self):
        """
        Se invoca cada vez que el widget debe crear todos sus
        recursos de ventana. Crearemos nuestro gtk.gdk.Window
        y cargaremos la aguja indicadora.
        """
        # Primero establecemos el flag interno indicando que estamos "realized".
>>>>>>> master
        self.set_flags(self.flags() | gtk.REALIZED)

        # Creamos un nuevo gdk.Window donde poder dibujar.
        # También avisamos de que queremos recibir los eventos "exposure", "click" y "press".
<<<<<<< HEAD
            
=======

>>>>>>> master
        self.window = gtk.gdk.Window(
            parent=self.get_parent_window(),
            width=self.allocation.width,
            height=self.allocation.height,
            window_type=gdk.WINDOW_CHILD,
            wclass=gdk.INPUT_OUTPUT,
            event_mask=self.get_events() | gtk.gdk.EXPOSURE_MASK
                | gtk.gdk.BUTTON1_MOTION_MASK | gtk.gdk.BUTTON_PRESS_MASK
                | gtk.gdk.POINTER_MOTION_MASK
                | gtk.gdk.POINTER_MOTION_HINT_MASK)
<<<<<<< HEAD
                
        # Asociamos el gdk.Window con nostros mismos, GTK+ necesita 
        # una referencia entre el Widget y la ventana gdk.
        self.window.set_user_data(self)
        
        # Conectamos en estilo a la gdk.Window, el estilo contiene los colores y 
        # los "GraphicsContextes" que se usan para dibujar.
        self.style.attach(self.window)
        
        # El color por defecto para el fondo debe ser el que el estilo (tema) 
        # nos indique.
        self.style.set_background(self.window, gtk.STATE_NORMAL)
        self.window.move_resize(*self.allocation)
        
        # self.style es un objeto gtk.Style, self.style.fg_gc es 
=======

        # Asociamos el gdk.Window con nostros mismos, GTK+ necesita
        # una referencia entre el Widget y la ventana gdk.
        self.window.set_user_data(self)

        # Conectamos en estilo a la gdk.Window, el estilo contiene los colores y
        # los "GraphicsContextes" que se usan para dibujar.
        self.style.attach(self.window)

        # El color por defecto para el fondo debe ser el que el estilo (tema)
        # nos indique.
        self.style.set_background(self.window, gtk.STATE_NORMAL)
        self.window.move_resize(*self.allocation)

        # self.style es un objeto gtk.Style, self.style.fg_gc es
>>>>>>> master
        # un array o graphic contexts usados para dibujar los colores del primer plano.
        normal_gc = self.style.fg_gc[gtk.STATE_NORMAL]
        self.gc = gtk.gdk.GC(self.window)
        normal_gc.copy(self.gc)
        self.gc.set_foreground(self.gc.get_colormap().alloc_color("red"))
        self.gc.set_line_attributes(5, gtk.gdk.LINE_SOLID, gtk.gdk.CAP_ROUND, gtk.gdk.JOIN_MITER)
        self.connect("motion_notify_event", self.motion_notify_event)
        import pango
        self.texto = pango.Layout(self.get_pango_context())
        self.texto.set_font_description(pango.FontDescription("Monospace 16"))
        self.texto.set_alignment(pango.ALIGN_CENTER)
<<<<<<< HEAD
        
    def do_unrealize(self):
        # Método responsable de liberar los recursos GDK. Eliminamos la asociación 
        # entre la ventana que hemos creado en do_realize con nosotros mismos.
        self.window.destroy()
        
    def do_size_request(self, requisition):
        """
        De Widget.py: El método do_size_request de GTK+ se invoca 
        en un widget para preguntar al propio widget cómo de grande desea ser.
        No se garantiza que GTK+ realmente nos dé ese tamaño. Así que enviamos 
=======

    def do_unrealize(self):
        # Método responsable de liberar los recursos GDK. Eliminamos la asociación
        # entre la ventana que hemos creado en do_realize con nosotros mismos.
        self.window.destroy()

    def do_size_request(self, requisition):
        """
        De Widget.py: El método do_size_request de GTK+ se invoca
        en un widget para preguntar al propio widget cómo de grande desea ser.
        No se garantiza que GTK+ realmente nos dé ese tamaño. Así que enviamos
>>>>>>> master
        a GTK+ el tamaño máximo que necesitamos para dibujarnos entero.
        """
        # Como nuestro widget es cuadrado, misma altura que ancho
        tamanno = (self.borde + self.radio) * 2
        requisition.height = tamanno
        requisition.width = tamanno
<<<<<<< HEAD
    
    def do_size_allocate(self, allocation):
        """
        A este método se le llama cuando el tamaño real se conoce y al 
        widget se le comunica cuánto espacio puede ocupar. Se guarda el 
        espacio ocupado self.allocation = allocation. El siguiente código 
=======

    def do_size_allocate(self, allocation):
        """
        A este método se le llama cuando el tamaño real se conoce y al
        widget se le comunica cuánto espacio puede ocupar. Se guarda el
        espacio ocupado self.allocation = allocation. El siguiente código
>>>>>>> master
        es idéntoco al del ejemplo de widget.py.
        """
        if self.flags() & gtk.REALIZED:
            self.window.move_resize(*allocation)
<<<<<<< HEAD
    
    def __calcular_posicion_aguja(self):
        """
        Devuelve la posición X e Y del extremo de la aguja en el perímetro 
        de la circunferencia según el máximo, mínimo y posición; teniendo en 
        cuenta que el mínimo se corresponde con un ángulo de 45 grados y 
=======

    def __calcular_posicion_aguja(self):
        """
        Devuelve la posición X e Y del extremo de la aguja en el perímetro
        de la circunferencia según el máximo, mínimo y posición; teniendo en
        cuenta que el mínimo se corresponde con un ángulo de 45 grados y
>>>>>>> master
        el máximo con uno de 315.
        """
        self.posicion = min(self.maximo, max(self.posicion, self.minimo))
        # Ángulo proporcional a la posición entre máximo y mínimo trasladado a la escala [45..270]
        offset = self.minimo - 0.0
        minimo = 0.0
        maximo = self.maximo - offset
        posicion = self.posicion - offset
        try:
            prop = posicion / (maximo - minimo)
        except ZeroDivisionError:
            prop = 0.0
        angulo = 45.0 + (270.0 * prop)
            # FIXME: Dejo para después el rotar la circunferencia. 0/360 apunta a la derecha y alfa crece hacia "arriba".
        # Intersección entre la línea en ese ángulo y la circunferencia:
        from math import sin, cos, radians
        x = cos(radians(angulo))
        y = sin(radians(angulo))
        x *= (self.radio * 0.85)    # Escalamos
        y *= (self.radio * 0.85)
        x += self.radio     # Y trasladamos
        y += self.radio
        x = int(round(x))
        y = int(round(y))
<<<<<<< HEAD
        return x, y 
=======
        return x, y
>>>>>>> master

    def do_expose_event(self, event):
        """
        Aquí es cuando el widget se debe dibujar a sí mismo.
        """
<<<<<<< HEAD
        # Dibujamos una línea entre el centro del widget y la posición del perímetro 
=======
        # Dibujamos una línea entre el centro del widget y la posición del perímetro
>>>>>>> master
        # de la circunferencia correspondiente proporcionalmente a self.posicion.
        # El ángulo de 45º correspondería al mínimo y 360º - 45º al máximo.
        xcentro = self.radio + self.borde
        ycentro = self.radio + self.borde
        xaguja, yaguja = self.__calcular_posicion_aguja()
        self.window.draw_pixbuf(self.gc, self.fondo, 0, 0, 0, 0, -1, -1)
        self.window.draw_line(self.gc, xcentro, ycentro, xaguja, yaguja)
        txtpos = str(round(self.posicion, 1))
        self.texto.set_text(txtpos)
        if self.posicion <= 33.3:
            color = gtk.gdk.Color(32767, 0, 0)
        elif self.posicion <= 66.6:
            color = gtk.gdk.Color(32767, 32767, 0)
        else:
            color = gtk.gdk.Color(0, 32767, 0)
        self.window.draw_layout(self.gc, self.radio - len(txtpos) * 5, int(self.radio + (25.0/100) * self.radio), self.texto, color)
<<<<<<< HEAD
            
    def motion_notify_event(self, widget, event):
        # Si es un "hint", entonces cojamos toda la información necesaria. 
=======

    def motion_notify_event(self, widget, event):
        # Si es un "hint", entonces cojamos toda la información necesaria.
>>>>>>> master
        # Si no, es todo lo que necesitamos.
        if event.is_hint:
            x, y, state = event.window.get_pointer()
        else:
            x = event.x
            y = event.y
            state = event.state
<<<<<<< HEAD
        
        if (state & gtk.gdk.BUTTON1_MASK):
            # Comprobamos que el clic está dentro de la aguja y si ésta debe cambiar de posición.
            self.check_for_new_posicion(event.x, event.y)
            
=======

        if (state & gtk.gdk.BUTTON1_MASK):
            # Comprobamos que el clic está dentro de la aguja y si ésta debe cambiar de posición.
            self.check_for_new_posicion(event.x, event.y)

>>>>>>> master
    def do_button_press_event(self, event):
        """
        El método virtual del evento "press".
        """
        # Me aseguro de que ha sido el botón principal (izquierdo, generalmente).
        if event.button == 1:
            # Chequeamos la posicón.
            self.check_for_new_posicion(event.x, event.y)
        return True
<<<<<<< HEAD
        
    def check_for_new_posicion(self, xPos, yPos):
        """
        Esta función debería determinar si xPos e yPos están en la línea 
        trazada por la aguja. De no ser así, la posición de la misma 
        debe cambiar a la descrita por la intersección entre xPos, yPos y 
        el centro de la circunferencia.
        """
        # Aquí deberían ir un montón de calculotes para averiguar si una 
        # línea pasa por dos puntos, pero tengo el álgebra oxidada y no 
        # voy a usar el widget como entrada para el usuario. Así que 
        # ignoro el clic y cambio la posición a la misma que tenía ya.
        nueva_posicion = self.posicion  # Debería ser la posición proporcional correspondiente al ángulo que forma el clic con el centro.
        self.set_value(nueva_posicion)
            
=======

    def check_for_new_posicion(self, xPos, yPos):
        """
        Esta función debería determinar si xPos e yPos están en la línea
        trazada por la aguja. De no ser así, la posición de la misma
        debe cambiar a la descrita por la intersección entre xPos, yPos y
        el centro de la circunferencia.
        """
        # Aquí deberían ir un montón de calculotes para averiguar si una
        # línea pasa por dos puntos, pero tengo el álgebra oxidada y no
        # voy a usar el widget como entrada para el usuario. Así que
        # ignoro el clic y cambio la posición a la misma que tenía ya.
        nueva_posicion = self.posicion  # Debería ser la posición proporcional correspondiente al ángulo que forma el clic con el centro.
        self.set_value(nueva_posicion)

>>>>>>> master
    def set_value(self, valor):
        """
        Cambia la posición de la aguja al valor entre minimo y maximo recibido.
        """
        if (self.minimo <= valor <= self.maximo):
            if valor != self.posicion:
                self.posicion = valor
                # Redibujo el widget
                self.queue_resize()
                self.window.move_resize(*self.allocation)
<<<<<<< HEAD
            
=======

>>>>>>> master
    def get_value(self):
        """
        Devuelve el valor actual mostrado.
        """
        return self.posicion
<<<<<<< HEAD
        
=======

>>>>>>> master
    # Paso de los métodos de get y set de máximo y mínimo. Son los que se inicializaron y punto pelota.

###############################################################################

def main():
    # Registro la clase como un widget Gtk
    gobject.type_register(Velocimetro)
<<<<<<< HEAD
    
    win = gtk.Window()
    win.resize(210, 210)
    win.connect('delete-event', gtk.main_quit)
    
=======

    win = gtk.Window()
    win.resize(210, 210)
    win.connect('delete-event', gtk.main_quit)

>>>>>>> master
    velocimetro = Velocimetro(0, 100, 50.0)
    win.add(velocimetro)
    win.show()
    win.show_all()
    gtk.main()

if __name__ == "__main__":
    main()
<<<<<<< HEAD

=======
>>>>>>> master
