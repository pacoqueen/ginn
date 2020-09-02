#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
import gobject
import pango

class BaseBGBox(gtk.HBox):
    __gtype_name__ = 'BaseBGBox'
    
    def __init__(self, palette='BASE'):
        gtk.HBox.__init__(self)
        self.palette = palette
    
    def do_expose_event(self, event):
        allocation = self.get_allocation()
        style = self.get_style()
        state = self.state

        if self.palette == 'BASE':
            gc = style.base_gc[state]
        elif self.palette == 'BG':
            gc = style.bg_gc[state]
        elif self.palette == 'FG':
            gc = style.fg_gc[state]
        else:
            gtk.main_quit()

        self.window.draw_rectangle(gc, True, allocation.x, allocation.y,
                                   allocation.width, allocation.height)
        
        gtk.HBox.do_expose_event(self, event)

class Header(gtk.MenuItem):
    __gtype_name__ = 'Header'

    __gproperties__ = {
        'alignment': (str, None, None, 'LEFT', gobject.PARAM_READWRITE),
        'markup': (str, None, None, '', gobject.PARAM_READWRITE),
        }
    
    def __init__(self, markup, alignment='LEFT'):
        gtk.MenuItem.__init__(self)

        self.label = gtk.Label()

        self.alignment = alignment
        self.markup = markup

        self.set_markup(markup)
        self.set_alignment(alignment)
        
        self.add(self.label)
        
        self.select()
    
    def do_set_property(self, pspec, value):
        if pspec.name == 'markup':
            self.set_markup(value)
        elif pspec.name == 'alignment':
            self.set_alignment(value)
        else:
            raise AttributeError('unknown property %s' % pspec.name)

    def do_get_property(self, pspec):
        if pspec.name == 'markup':
            return self.markup
        elif pspec.name == 'alignment':
            return self.alignment
        else:
            raise AttributeError('unknown property %s' % pspec.name)

    def do_style_set(self, style):
        self.label.set_style(self.get_style())
    
    def set_markup(self, markup):
        self.label.set_markup(markup)
        self.markup = markup
    
    def get_markup(self):
        return self.markup

    def set_alignment(self, alignment):
        self.alignment = alignment
        if alignment == 'LEFT':
            self.label.set_alignment(0, 0.5)
            self.label.set_justify(gtk.JUSTIFY_LEFT)
        if alignment == 'CENTER':
            self.label.set_alignment(0.5, 0.5)
            self.label.set_justify(gtk.JUSTIFY_CENTER)
        if alignment == 'RIGHT':
            self.label.set_alignment(1, 0.5)
            self.label.set_justify(gtk.JUSTIFY_RIGHT)
    
    def get_alignment(self):
        return self.alignment

class WrapLabel(gtk.Label):
    __gtype_name__ = 'WrapLabel'

    def __init__(self, cad=None):
        gtk.Label.__init__(self)
        
        self.__wrap_width = 0
        self.layout = self.get_layout()
        self.layout.set_wrap(pango.WRAP_WORD_CHAR)
        
        if cad != None:
            self.set_text(cad)
        
        self.set_alignment(0.0, 0.0)
    
    def do_size_request(self, requisition):
        layout = self.get_layout()
        width, height = layout.get_pixel_size()  # @UnusedVariable
        requisition.width = 0
        requisition.height = height
    
    def do_size_allocate(self, allocation):
        gtk.Label.do_size_allocate(self, allocation)
        self.__set_wrap_width(allocation.width)
    
    def set_text(self, cad):
        gtk.Label.set_text(self, cad)
        self.__set_wrap_width(self.__wrap_width)
        
    def set_markup(self, cad):
        gtk.Label.set_markup(self, cad)
        self.__set_wrap_width(self.__wrap_width)
    
    def __set_wrap_width(self, width):
        if width == 0:
            return
        layout = self.get_layout()
        layout.set_width(width * pango.SCALE)
        if self.__wrap_width != width:
            self.__wrap_width = width
            self.queue_resize()

def main():
    w = gtk.Window()
    w.connect("destroy", gtk.main_quit)
    w.set_default_size(300, 200)

    bb = BaseBGBox()
    bb.set_border_width(12)

    w.add(bb)

    h = Header("<b>Themed Header Widget</b>")
    h.props.alignment = 'RIGHT'

    vbox = gtk.VBox(False, 6)

    vbox.pack_start(h, False, True, 0)

    l = WrapLabel()
    l.set_markup("This is a very long label that should span many lines. "
                  "It's a good example of what the WrapLabel can do, and "
                  "includes formatting, like <b>bold</b>, <i>italic</i>, "
                  "and <u>underline</u>. The window can be wrapped to any "
                  "width, unlike the standard Gtk::Label, which is set to "
                  "a certain wrap width.")
    print(l.get_text())
    vbox.pack_start(l)

    bb.pack_start(vbox)

    w.show_all()

    gtk.main()


if __name__ == "__main__":
    main()

