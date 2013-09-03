#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
import gtk

class CellRendererAutoComplete(gtk.CellRendererText):

    """ Text entry cell which accepts a Gtk.EntryCompletion object """

    __gtype_name__ = 'CellRendererAutoComplete'

    def __init__(self, completion):
        self.completion = completion
        gtk.CellRendererText.__init__(self)

    def do_start_editing(
               self, event, treeview, path, background_area, cell_area, flags):
        if not self.get_property('editable'):
            return
        entry = gtk.Entry()
        descripcion_anterior = treeview.get_model()[path][1]
        entry.set_text(descripcion_anterior)
        entry.set_completion(self.completion)
        entry.connect('editing-done', self.editing_done, path, 
                                                         descripcion_anterior)
        entry.show()
        entry.grab_focus()
        return entry

    def editing_done(self, entry, path, texto_anterior = ""):
        texto = entry.get_text()
        if not texto:
            texto = texto_anterior
        self.emit('edited', path, texto)


