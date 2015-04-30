#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
import gtk

class CellRendererAutoComplete(gtk.CellRendererText):

    """ Text entry cell which accepts a Gtk.EntryCompletion object """

    __gtype_name__ = 'CellRendererAutoComplete'

    def __init__(self, completion, modelcol = 1):
        """
        completion: Objeto autocomletado de Gtk.
        modelcol: Columna en el model del Treeview donde se va a poner el cell.
        """
        self.completion = completion
        self.modelcol = modelcol
        gtk.CellRendererText.__init__(self)
        self.handler_id = None

    def do_start_editing(
               self, event, treeview, path, background_area, cell_area, flags):
        if not self.get_property('editable'):
            return
        self.entry = gtk.Entry()
        descripcion_anterior = treeview.get_model()[path][self.modelcol]
        self.entry.set_text(descripcion_anterior)
        self.entry.set_completion(self.completion)
        self.handler_id = self.entry.connect('editing-done', self.editing_done,
                                        path, descripcion_anterior)
        self.entry.show()
        self.entry.grab_focus()
        return self.entry

    def editing_done(self, entry, path, texto_anterior = ""):
        texto = entry.get_text()
        if not texto:
            texto = texto_anterior
        self.emit('edited', path, texto)

