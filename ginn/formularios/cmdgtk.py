#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from threading import Thread

import pygtk
pygtk.require("2.0")
import gtk
import gobject

class ShellCommandJob(gobject.GObject):

    def execute(self, command):
        self.command = command
        Thread(target = self._process).start()
    
    def _process(self):
        handle = os.popen(self.command)
        line = handle.readline()
        while line:
            self.emit("output", line)
            line = handle.readline()
        handle.close()


class CmdGTK:
    def __init__(self):
        if not gobject.signal_lookup("output", ShellCommandJob):
            gobject.signal_new("output", ShellCommandJob, \
                    gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, \
                    [str])
        if not gtk.main_level():
            gtk.gdk.threads_init()  # _DEBE_ llamarse _ANTES_ del gtk.main por temas del GIL.
                                    # (http://www.pygtk.org/docs/pygtk/gdk-functions.html#function-gdk--threads-init).

    def handle_output(self, buff, view, job, line):
        gtk.gdk.threads_enter()
        buff.insert(buff.get_end_iter(), line)
        view.scroll_to_iter(buff.get_end_iter(), 0)
        gtk.gdk.threads_leave()


    def execute(self, command, buff, view):
        job = ShellCommandJob()
        job.connect("output", lambda job, line:
                self.handle_output(buff, view, job, line))
        job.execute(command)

    def attach_to(self, contenedor):
        """
        Agrega el emuldor de terminal al contenedor recibido.
        """
        buff = gtk.TextBuffer()

        scrollwin = gtk.ScrolledWindow()
        scrollwin.set_shadow_type(gtk.SHADOW_IN)
        scrollwin.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        contenedor.add(scrollwin)
        scrollwin.show()
        
        view = gtk.TextView(buff)
        scrollwin.add(view)
        view.show()

        hbox = gtk.HBox(False, 12)
        contenedor.pack_start(hbox, False, False, 0)
        hbox.show()

        entry = gtk.Entry()
        entry.set_text("ls -tr")
        hbox.add(entry)
        entry.show()

        button = gtk.Button(None, gtk.STOCK_EXECUTE)
        hbox.pack_start(button, False, False, 0)
        button.show()

        ejecutar = lambda boton, entry, buff, view: self.execute(entry.get_text(), buff, view)

        button.connect("clicked", ejecutar, entry, buff, view)
        #-----------------------------------------------------------#
        def pasar_foco(widget, event, button):                      #
            if event.keyval == 65293 or event.keyval == 65421:      #
                button.grab_focus()                                 #
        #-----------------------------------------------------------#
        entry.connect("key_press_event", pasar_foco, button)

if __name__ == "__main__":
    
    gtk.gdk.threads_init()

    win = gtk.Window()
    win.set_default_size(480, 320)

    vbox = gtk.VBox(False, 6)
    vbox.set_border_width(6)
    win.add(vbox)
    vbox.show()
    
    cmdgtk = CmdGTK()
    cmdgtk.attach_to(vbox)

    win.connect("destroy", gtk.main_quit)
    win.show()
    
    gtk.main()

