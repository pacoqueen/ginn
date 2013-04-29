#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
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

gobject.signal_new("output", ShellCommandJob, \
        gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, \
        [str])


def handle_output(buffer, view, job, line):
    gtk.gdk.threads_enter()
    buffer.insert(buffer.get_end_iter(), line)
    view.scroll_to_iter(buffer.get_end_iter(), 0)
    gtk.gdk.threads_leave()


def execute(command, buffer, view):
    job = ShellCommandJob()
    job.connect("output", lambda job, line:
            handle_output(buffer, view, job, line))
    job.execute(entry.get_text())


if __name__ == "__main__":
    gtk.gdk.threads_init()

    win = gtk.Window()
    win.set_default_size(480, 320)

    vbox = gtk.VBox(False, 6)
    vbox.set_border_width(6)
    win.add(vbox)
    vbox.show()
    
    buffer = gtk.TextBuffer()

    scrollwin = gtk.ScrolledWindow()
    scrollwin.set_shadow_type(gtk.SHADOW_IN)
    scrollwin.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
    vbox.add(scrollwin)
    scrollwin.show()
    
    view = gtk.TextView(buffer)
    scrollwin.add(view)
    view.show()

    hbox = gtk.HBox(False, 12)
    vbox.pack_start(hbox, False, False, 0)
    hbox.show()

    entry = gtk.Entry()
    entry.set_text("ls -tr")
    hbox.add(entry)
    entry.show()

    button = gtk.Button(None, gtk.STOCK_EXECUTE)
    hbox.pack_start(button, False, False, 0)
    button.show()

    button.connect("clicked", lambda *args: execute(entry.get_text(), buffer, view))

    win.connect("destroy", gtk.main_quit)
    win.show()
    
    gtk.main()

