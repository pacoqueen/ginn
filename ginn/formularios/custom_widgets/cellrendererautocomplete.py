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
        entry.set_completion(self.completion)
        entry.connect('editing-done', self.editing_done, path)
        entry.show()
        entry.grab_focus()
        return entry

    def editing_done(self, entry, path):
        self.emit('edited', path, entry.get_text())


