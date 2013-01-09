#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk, pygtk, gobject

class MarqueeLabel(gtk.Label):
    """
    Label con el texto desplazándose "cutremente" de derecha a izquierda.
    """
    # TODO: Permitir que use markups el texto.
    # TODO: Permitir que el texto mostrado sea mayor o menor en función del 
    #       tamaño del padre.

    def __init__(self, texto = "", init_long = 30, speed = 10):
        """
        init_long es la longitud EN CARACTERES de la parte del texto mostrado.
        Idealmente debería verse la parte que quepa en función del tamaño del 
        padre del widget. Se deja para futuras versiones.
        speed es el número de caracteres por segundo que se desplazan.
        """
        self.texto_original = self.texto = texto
        self._long = init_long
        self.parte_visible = texto[:self._long]
        FRAME_DELAY = int(round(1000.0 / speed))
        self.__timeout_id = gobject.timeout_add(FRAME_DELAY, self.timeout)
        gtk.Label.__init__(self, self.parte_visible)
        #self.set_use_markup(True)

    def timeout(self):
        """
        Manejador para regenerar el contenido del label.
        """
        l, self.texto = self.texto[0], self.texto[1:]
        self.texto += l
        self.parte_visible = self.texto[:self._long]
        self.set_text(self.parte_visible)
        #self.set_use_markup(True)
        return True
    
    def rewind(self, speed = None):
        """
        Rebobina el texto el número de caracteres indicado en "speed". Si es 
        None, vuelve al principio.
        """
        if speed is None: # reset!
            self.texto = self.texto_original
        else:
            raise NotImplementedError, "Not implemented yed."


def test():
    w = gtk.Window()
    longtext = " ".join(["Texto muy largo %d." % j 
                         for j in range(25)])
    marquee = MarqueeLabel(longtext)
    w.add(marquee)
    w.show_all()
    w.connect("destroy", gtk.main_quit)
    gtk.main()

if __name__ == "__main__":
    test()

