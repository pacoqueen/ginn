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
# Reconocimiento del código del widget de escala de estrellas a quien 
# corresponda (ver docstring de la clase).
###############################################################################

try:
    import gtk
    import gobject
    from gtk import gdk
except:
    raise SystemExit
    

import pygtk
if gtk.pygtk_version < (2, 0):
    print "Se necesita PyGtk 2.0 o posterior."
    raise SystemExit
  
BORDER_WIDTH = 5
PIXMAP_SIZE = 22
STAR_PIXMAP = ["22 22 77 1",
"   c None",
".  c #626260",
"+  c #5E5F5C",
"@  c #636461",
"#  c #949492",
"$  c #62625F",
"%  c #6E6E6B",
"&  c #AEAEAC",
"*  c #757673",
"=  c #61625F",
"-  c #9C9C9B",
";  c #ACACAB",
">  c #9F9F9E",
",  c #61635F",
"'  c #656663",
")  c #A5A5A4",
"!  c #ADADAB",
"~  c #646562",
"{  c #61615F",
"]  c #6C6D6A",
"^  c #797977",
"/  c #868684",
"(  c #A0A19E",
"_  c #AAAAA8",
":  c #A3A3A2",
"<  c #AAAAA7",
"[  c #9F9F9F",
"}  c #888887",
"|  c #7E7E7C",
"1  c #6C6C69",
"2  c #626360",
"3  c #A5A5A3",
"4  c #ABABAA",
"5  c #A9A9A7",
"6  c #A2A2A1",
"7  c #A3A3A1",
"8  c #A7A7A6",
"9  c #A8A8A6",
"0  c #686866",
"a  c #A4A4A2",
"b  c #A4A4A3",
"c  c #A1A19F",
"d  c #9D9D9C",
"e  c #9D9D9B",
"f  c #A7A7A5",
"g  c #666664",
"h  c #A1A1A0",
"i  c #9E9E9D",
"j  c #646461",
"k  c #A6A6A4",
"l  c #A0A09F",
"m  c #9F9F9D",
"n  c #A9A9A8",
"o  c #A0A09E",
"p  c #9B9B9A",
"q  c #ACACAA",
"r  c #60615E",
"s  c #ADADAC",
"t  c #A2A2A0",
"u  c #A8A8A7",
"v  c #6E6F6C",
"w  c #787976",
"x  c #969695",
"y  c #8B8B8A",
"z  c #91918F",
"A  c #71716E",
"B  c #636360",
"C  c #686966",
"D  c #999997",
"E  c #71716F",
"F  c #61615E",
"G  c #6C6C6A",
"H  c #616260",
"I  c #5F605E",
"J  c #5D5E5B",
"K  c #565654",
"L  c #5F5F5D",
"                      ",
"                      ",
"          .           ",
"          +           ",
"         @#$          ",
"         %&*          ",
"        =-;>,         ",
"        ';)!'         ",
"  ~{{]^/(_:<[}|*1@,   ",
"   23&4_5367895&80    ",
"    2a4b:7c>def)g     ",
"     2c4:h>id56j      ",
"      {k8lmeln2       ",
"      j8bmoppqr       ",
"      {stusnd4v       ",
"      ws;x@yq;/       ",
"      zfAB {CmD{      ",
"     rE{     FGH      ",
"     IJ       KL      ",
"                      ",
"                      ",
"                      "]

class StarHScale(gtk.Widget):
    """A horizontal Scale Widget that attempts to mimic the star
    rating scheme used in iTunes.
    
    -----------------------------------------------------------------------------------    
    
    StarHScale a Horizontal slider that uses stars
    Copyright (C) 2006 Mark Mruss <selsine@gmail.com>
    
    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.
    
    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.
    
    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
    
    If you find any bugs or have any suggestions email: selsine@gmail.coim
    
    http://www.learningpython.com/2006/07/25/writing-a-custom-widget-using-pygtk/
    
    """
    
    def __init__(self, max_stars=5, stars=0):
        """Initialization, max_stars is the total number
        of stars that may be visible, and stars is the current
        number of stars to draw"""
        
        #Initialize the Widget
        gtk.Widget.__init__(self)
        
        self.max_stars = max_stars
        self.stars = stars
        
        # Init the list to blank
        self.sizes = []     
        for count in range(0,self.max_stars):
            self.sizes.append((count * PIXMAP_SIZE) + BORDER_WIDTH)
        
    def do_realize(self):
        """Called when the widget should create all of its 
        windowing resources.  We will create our gtk.gdk.Window
        and load our star pixmap."""
        
        # First set an internal flag showing that we're realized
        self.set_flags(self.flags() | gtk.REALIZED)
        
        # Create a new gdk.Window which we can draw on.
        # Also say that we want to receive exposure events 
        # and button click and button press events
            
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
                
        # Associate the gdk.Window with ourselves, Gtk+ needs a reference
        # between the widget and the gdk window
        self.window.set_user_data(self)
        
        # Attach the style to the gdk.Window, a style contains colors and
        # GC contextes used for drawing
        self.style.attach(self.window)
        
        # The default color of the background should be what
        # the style (theme engine) tells us.
        self.style.set_background(self.window, gtk.STATE_NORMAL)
        self.window.move_resize(*self.allocation)
        
        # load the star xpm
        self.pixmap, mask = gtk.gdk.pixmap_create_from_xpm_d(
            self.window
            , self.style.bg[gtk.STATE_NORMAL]
            , STAR_PIXMAP)
            
        # self.style is a gtk.Style object, self.style.fg_gc is
        # an array or graphic contexts used for drawing the forground
        # colours   
        self.gc = self.style.fg_gc[gtk.STATE_NORMAL]
        
        self.connect("motion_notify_event", self.motion_notify_event)
        
    def do_unrealize(self):
        # The do_unrealized method is responsible for freeing the GDK resources
        # De-associate the window we created in do_realize with ourselves
        self.window.destroy()
        
    def do_size_request(self, requisition):
        """From Widget.py: The do_size_request method Gtk+ is calling
         on a widget to ask it the widget how large it wishes to be. 
         It's not guaranteed that gtk+ will actually give this size 
         to the widget.  So we will send gtk+ the size needed for
         the maximum amount of stars"""
        
        requisition.height = PIXMAP_SIZE
        requisition.width = (PIXMAP_SIZE * self.max_stars) + (BORDER_WIDTH * 2)
    
    
    def do_size_allocate(self, allocation):
        """The do_size_allocate is called by when the actual 
        size is known and the widget is told how much space 
        could actually be allocated Save the allocated space
        self.allocation = allocation. The following code is
        identical to the widget.py example"""
    
        if self.flags() & gtk.REALIZED:
            self.window.move_resize(*allocation)
        
    def do_expose_event(self, event):
        """This is where the widget must draw itself."""
        
        #Draw the correct number of stars.  Each time you draw another star
        #move over by 22 pixels. which is the size of the star.
        for count in range(0,self.stars):
            self.window.draw_drawable(self.gc, self.pixmap, 0, 0
                                                , self.sizes[count] 
                                                , 0,-1, -1) 
            
    def motion_notify_event(self, widget, event):
        # if this is a hint, then let's get all the necessary 
        # information, if not it's all we need.
        if event.is_hint:
            x, y, state = event.window.get_pointer()
        else:
            x = event.x
            y = event.y
            state = event.state
        
        if (state & gtk.gdk.BUTTON1_MASK):
            # loop through the sizes and see if the
            # number of stars should change
            self.check_for_new_stars(event.x)   
            
    def do_button_press_event(self, event):
        """The button press event virtual method"""
        
        # make sure it was the first button
        if event.button == 1:
            #check for new stars
            self.check_for_new_stars(event.x)           
        return True
        
    def check_for_new_stars(self, xPos):
        """This function will determine how many stars
        will be show based on an x coordinate. If the
        number of stars changes the widget will be invalidated
        and the new number drawn"""
        
        # loop through the sizes and see if the
        # number of stars should change
        new_stars = 0
        for size in self.sizes:
            if (xPos < size):
                # we've reached the star number
                break
            new_stars = new_stars + 1
            
        # set the new value
        self.set_value(new_stars)
            
    def set_value(self, value):
        """Sets the current number of stars that will be 
        drawn.  If the number is different then the current
        number the widget will be redrawn"""
        
        if (value >= 0):
            if (self.stars != value):
                self.stars = value
                #check for the maximum
                if (self.stars > self.max_stars):
                    self.stars = self.max_stars
                
                # redraw the widget
                self.queue_resize()
                self.window.move_resize(*self.allocation)
            
    def get_value(self):
        """Get the current number of stars displayed"""
        
        return self.stars
        
    def set_max_value(self, max_value):
        """set the maximum number of stars"""
        
        if (self.max_stars != max_value):
            """Save the old max incase it is less than the
            current number of stars, in which case we will
            have to redraw"""
            
            if (max_value > 0):
                self.max_stars = max_value
                #reinit the sizes list (should really be a separate function)
                self.sizes = []     
                for count in range(0,self.max_stars):
                    self.sizes.append((count * PIXMAP_SIZE) + BORDER_WIDTH)
                """do we have to change the current number of
                stars?"""           
                if (self.stars > self.max_stars):
                    self.set_value(self.max_stars)
    
    def get_max_value(self):
        """Get the maximum number of stars that can be shown"""
        
        return self.max_stars

###############################################################################
class Velocimetro(gtk.Widget):
    """
    Especie de velocímetro analógico. A ver qué sale.
    """
    
    def __init__(self, minimo = 0.0, maximo = 100.0, posicion = 50.0):
        """
        Inicialización.
        Mínimo es el mínimo de la escala.
        Máximo es el máximo.
        Posición es la posición inicial. 
        Siempre debe cumplirse que mínimo <= posición <= máximo.
        """
        
        assert minimo <= posicion <= maximo, "Error. Asegúrese de que mínimo <= posición <= máximo."

        #Inicialización del Widget
        gtk.Widget.__init__(self)
        
        self.minimo = minimo
        self.maximo = maximo
        self.posicion = posicion
        self.radio = 75     # 100 píxeles de radio para empezar está bien. Si se redimensiona, 
                            # este radio debe crecer/disminuir acorde con ello.
        self.borde = 5      # Tamaño del borde entre el círculo y el fin del Widget. Ancho total = borde * 2 + radio * 2
        import os
        if "svg" in [i['name'] for i in gtk.gdk.pixbuf_get_formats()]:
            fondo = gtk.gdk.pixbuf_new_from_file(os.path.join("..", "imagenes", "velocimetro.svg"))
        else:     # MS-Windows no se lleva bien con un formato tan bonito como SVG. Vaya "usté" a saber por qué capricho del destino.
            fondo = gtk.gdk.pixbuf_new_from_file(os.path.join("..", "imagenes", "velocimetro.png"))
        self.fondo = fondo.scale_simple((self.radio + self.borde) * 2, (self.radio + self.borde) * 2, gtk.gdk.INTERP_BILINEAR)
        
    def do_realize(self):
        """
        Se invoca cada vez que el widget debe crear todos sus 
        recursos de ventana. Crearemos nuestro gtk.gdk.Window 
        y cargaremos la aguja indicadora.
        """
        # Primero establecemos el flag interno indicando que estamos "realized". 
        self.set_flags(self.flags() | gtk.REALIZED)

        # Creamos un nuevo gdk.Window donde poder dibujar.
        # También avisamos de que queremos recibir los eventos "exposure", "click" y "press".
            
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
        
    def do_unrealize(self):
        # Método responsable de liberar los recursos GDK. Eliminamos la asociación 
        # entre la ventana que hemos creado en do_realize con nosotros mismos.
        self.window.destroy()
        
    def do_size_request(self, requisition):
        """
        De Widget.py: El método do_size_request de GTK+ se invoca 
        en un widget para preguntar al propio widget cómo de grande desea ser.
        No se garantiza que GTK+ realmente nos dé ese tamaño. Así que enviamos 
        a GTK+ el tamaño máximo que necesitamos para dibujarnos entero.
        """
        # Como nuestro widget es cuadrado, misma altura que ancho
        tamanno = (self.borde + self.radio) * 2
        requisition.height = tamanno
        requisition.width = tamanno
    
    def do_size_allocate(self, allocation):
        """
        A este método se le llama cuando el tamaño real se conoce y al 
        widget se le comunica cuánto espacio puede ocupar. Se guarda el 
        espacio ocupado self.allocation = allocation. El siguiente código 
        es idéntoco al del ejemplo de widget.py.
        """
        if self.flags() & gtk.REALIZED:
            self.window.move_resize(*allocation)
    
    def __calcular_posicion_aguja(self):
        """
        Devuelve la posición X e Y del extremo de la aguja en el perímetro 
        de la circunferencia según el máximo, mínimo y posición; teniendo en 
        cuenta que el mínimo se corresponde con un ángulo de 45 grados y 
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
        x = int(x)
        y = int(y)
        return x, y 

    def do_expose_event(self, event):
        """
        Aquí es cuando el widget se debe dibujar a sí mismo.
        """
        # Dibujamos una línea entre el centro del widget y la posición del perímetro 
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
            
    def motion_notify_event(self, widget, event):
        # Si es un "hint", entonces cojamos toda la información necesaria. 
        # Si no, es todo lo que necesitamos.
        if event.is_hint:
            x, y, state = event.window.get_pointer()
        else:
            x = event.x
            y = event.y
            state = event.state
        
        if (state & gtk.gdk.BUTTON1_MASK):
            # Comprobamos que el clic está dentro de la aguja y si ésta debe cambiar de posición.
            self.check_for_new_posicion(event.x, event.y)
            
    def do_button_press_event(self, event):
        """
        El método virtual del evento "press".
        """
        # Me aseguro de que ha sido el botón principal (izquierdo, generalmente).
        if event.button == 1:
            # Chequeamos la posicón.
            self.check_for_new_posicion(event.x, event.y)
        return True
        
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
            
    def get_value(self):
        """
        Devuelve el valor actual mostrado.
        """
        return self.posicion
        
    # Paso de los métodos de get y set de máximo y mínimo. Son los que se inicializaron y punto pelota.

###############################################################################

gobject.type_register(StarHScale)
gobject.type_register(Velocimetro)

def main():
    # Registro la clase como un widget Gtk
    gobject.type_register(Velocimetro)
    #gobject.type_register(StarHScale)
    
    win = gtk.Window()
    # win.resize(200,50)
    win.resize(210, 210)
    win.connect('delete-event', gtk.main_quit)
    
    #starScale = StarHScale(10,5)
    velocimetro = Velocimetro(0, 100, 50.0)
    # win.add(starScale)
    win.add(velocimetro)
    win.show()
    win.show_all()
    gtk.main()

if __name__ == "__main__":
    main()

