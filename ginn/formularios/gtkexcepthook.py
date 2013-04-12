#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: sw=4 ts=4:
#
# (c) 2003 Gustavo J A M Carneiro gjc at inescporto.pt
#     2004-2005 Filip Van Raemdonck
#
# http://www.daa.com.au/pipermail/pygtk/2003-August/005775.html
# Message-ID: <1062087716.1196.5.camel@emperor.homelinux.net>
#     "The license is whatever you want."

# He cambiado algunas cosas. Para respetar el espíritu del autor(es) original, 
# la nueva licencia es la WTFPL (http://sam.zoy.org/wtfpl/)

################################################################################
#             DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                     Version 2, December 2004
# 
#  Copyright (C) 2008 Francisco José Rodríguez Bogado
#                                           
#  Everyone is permitted to copy and distribute verbatim or modified
#  copies of this license document, and changing it is allowed as long
#  as the name is changed.
# 
#             DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#    TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
# 
#   0. You just DO WHAT THE FUCK YOU WANT TO.
################################################################################

# Para ver cómo generar y actualizar 117n l10n: 
#   http://my.opera.com/th3pr0ph3t/blog/localizacion-en-python-usando-gettext
# Usar el script ../l10n/actualizar_traduccion.sh si se cambia o 
# añade alguna cadena. Instala gtranslate si quieres llevar una vida mejor.

import inspect, linecache, pydoc, sys, os# , traceback
from cStringIO import StringIO
from gettext import gettext as _
from smtplib import SMTP, SMTPException

import gettext
gettext.textdomain("gtkexcepthook")
gettext.bindtextdomain("gtkexcepthook", 
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mo")))

import pygtk
pygtk.require ('2.0')
import gtk, pango

from formularios.utils import dialogo_entrada as fdialogo
        
#def analyse (exctyp, value, tb):
#    trace = StringIO()
#    traceback.print_exception (exctyp, value, tb, None, trace)
#    return trace

def lookup (name, frame, lcls):
    '''Find the value for a given name in the given frame'''
    if name in lcls:
        return 'local', lcls[name]
    elif name in frame.f_globals:
        return 'global', frame.f_globals[name]
    elif '__builtins__' in frame.f_globals:
        builtins = frame.f_globals['__builtins__']
        if type (builtins) is dict:
            if name in builtins:
                return 'builtin', builtins[name]
        else:
            if hasattr (builtins, name):
                return 'builtin', getattr (builtins, name)
    return None, []

def analyse (exctyp, value, tb):
    import tokenize, keyword

    trace = StringIO()
    nlines = 3
    frecs = inspect.getinnerframes (tb, nlines)
    trace.write ('Traceback (most recent call last):\n')
    for frame, fname, lineno, funcname, context, cindex in frecs: #@UnusedVariable
        trace.write ('  File "%s", line %d, ' % (fname, lineno))
        args, varargs, varkw, lcls = inspect.getargvalues (frame)

        def readline (lno=[lineno], *args):
            if args: print args
            try: return linecache.getline (fname, lno[0])
            finally: lno[0] += 1
        todo, prev, name, scope = {}, None, '', None
        for ttype, tstr, stup, etup, line in tokenize.generate_tokens(readline): #@UnusedVariable
            if ttype == tokenize.NAME and tstr not in keyword.kwlist:
                if name:
                    if name[-1] == '.':
                        try:
                            val = getattr (prev, tstr)
                        except AttributeError:
                            # XXX skip the rest of this identifier only
                            break
                        name += tstr
                else:
                    assert not name and not scope
                    scope, val = lookup (tstr, frame, lcls)
                    name = tstr
                if val:
                    prev = val
                #print '  found', scope, 'name', name, 'val', val, 'in', prev, 'for token', tstr
            elif tstr == '.':
                if prev:
                    name += '.'
            else:
                if name:
                    todo[name] = (scope, prev)
                prev, name, scope = None, '', None
                if ttype == tokenize.NEWLINE:
                    break
        
        args = []   # El "self" dentro de la lista de argumentos da problemas. 
                    # Salta un KeyError. Le paso la lista vacía para evitar 
                    # problemas.
        trace.write (funcname 
                     + inspect.formatargvalues (args, 
                        varargs, 
                        varkw, 
                        lcls, 
                        formatvalue=lambda v: '='+pydoc.text.repr(v))
                     +'\n')
        if context is None:
            context = []
        trace.write (''.join (['    ' + x.replace ('\t', '  ') for x in filter (lambda a: a.strip(), context)]))
        if len (todo):
            trace.write ('  variables: %s\n' % myprettyprint(todo))

    trace.write ('%s: %s' % (exctyp.__name__, value))
    return trace

def myprettyprint(stuff):
    from pprint import pformat
    return pformat(stuff)
    #from myprettyprint import print_dict
    #if isinstance(stuff, dict):
    #    return print_dict(stuff)
    #else:
    #    return pformat(stuff)

def _info (exctyp, value, tb):
    trace = None
    dialog = gtk.MessageDialog (parent=None, flags=0, 
                                type=gtk.MESSAGE_WARNING, 
                                buttons=gtk.BUTTONS_NONE)
    dialog.set_title (_("Bug Detected"))
    if gtk.check_version (2, 4, 0) is not None:
        dialog.set_has_separator (False)

    primary = _("<big><b>A programming error has been detected during the execution of this program.</b></big>")
    secondary = _("It probably isn't fatal, but should be reported to the developers nonetheless.")

    try:
        setsec = dialog.format_secondary_text
    except AttributeError:
        raise
        dialog.vbox.get_children()[0].get_children()[1].set_markup('%s\n\n%s' 
            % (primary, secondary))
        #lbl.set_property ("use-markup", True)
    else:
        del setsec
        dialog.set_markup (primary)
        dialog.format_secondary_text (secondary)

    try:
        email = feedback #@UndefinedVariable
        dialog.add_button (_("Report..."), 3)
    except NameError:
        # could ask for an email address instead...
        pass
    dialog.add_button (_("Details..."), 2)
    dialog.add_button (gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
    dialog.add_button (gtk.STOCK_QUIT, 1)
    dialog.add_button (_("Close all"), 4)

    while True:
        resp = dialog.run()
        if resp == 3:
            if trace == None:
                trace = analyse (exctyp, value, tb)

            # TODO: prettyprint, deal with problems in sending feedback, &tc
            try:
                server = smtphost #@UndefinedVariable
            except NameError:
                server = 'localhost'

            message = 'From: %s"\nTo: %s\nSubject: Exception feedback\n\n%s'%(
                email, "Soporte G-INN", trace.getvalue())

            s = SMTP()
            try:
                s.connect(server, port) #@UndefinedVariable
            except NameError:
                s.connect(server)
            try:
                passoteword = password #@UndefinedVariable
            except NameError:
                pass
            try:
                try:
                    if not passoteword:
                        txt="Introduzca contraseña del servidor de correo %s"%(
                            server)
                        passoteword = fdialogo(titulo = "CONTRASEÑA:", 
                                               texto = txt, 
                                               pwd = True) 
                        if passoteword == None:
                            continue
                except NameError, msg:
                    txt="Introduzca contraseña del servidor de correo %s"%(
                        server)
                    passoteword = fdialogo(titulo = "CONTRASEÑA:", 
                                                        texto = txt, 
                                                        pwd = True) 
                    if passoteword == None:
                        continue
                try:
                    if ssl: #@UndefinedVariable
                        s.ehlo()
                        s.starttls()
                        s.ehlo()
                except NameError, msg:
                    pass    # No hay variable ssl. No cifrado.
                try:
                    s.login(email, passoteword)
                except SMTPException:
                    print msg
                    pass    # Servidor no necesita autenticación.
            except NameError, msg:
                pass    # No se ha especificado contraseña, será que no 
                        # necesita autentificación entonces.
            try:
                s.sendmail (email, (devs_to,), message) #@UndefinedVariable
            except NameError:
                s.sendmail (email, (email,), message)
            s.quit()
            break

        elif resp == 2:
            if trace == None:
                trace = analyse (exctyp, value, tb)

            # Show details...
            details = gtk.Dialog (_("Bug Details"), dialog,
              gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
              (gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE, ))
            details.set_property ("has-separator", False)

            textview = gtk.TextView(); textview.show()
            textview.set_editable (False)
            textview.modify_font (pango.FontDescription ("Monospace"))

            sw = gtk.ScrolledWindow(); sw.show()
            sw.set_policy (gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            sw.add (textview)
            details.vbox.add (sw)
            textbuffer = textview.get_buffer()
            textbuffer.set_text (trace.getvalue())

            monitor = gtk.gdk.screen_get_default ().get_monitor_at_window (dialog.window)
            area = gtk.gdk.screen_get_default ().get_monitor_geometry (monitor)
            try:
                w = area.width // 1.6
                h = area.height // 1.6
            except SyntaxError:
                # python < 2.2
                w = area.width / 1.6
                h = area.height / 1.6
            details.set_default_size (int (w), int (h))

            details.run()
            details.destroy()

        elif resp == 1 and gtk.main_level() > 0:
            gtk.main_quit()
            break
        elif resp == 4:
            sys.exit(1)
        else:
            break

    dialog.destroy()

sys.excepthook = _info

if __name__ == '__main__':
    class X (object):
        pass
    x = X()
    x.y = 'Test'
    x.z = x
    w = ' e'
    # Descomentar para botón enviar por correo:
    #feedback = 'developer@bigcorp.comp'
    #smtphost = 'mx.bigcorp.comp'
    1, x.z.y, f, w #@UndefinedVariable
    raise Exception (x.z.y + w)

