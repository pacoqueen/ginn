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

# Para ver cómo generar y actualizar i18n l10n:
#   http://my.opera.com/th3pr0ph3t/blog/localizacion-en-python-usando-gettext
# Usar el script ../l10n/actualizar_traduccion.sh si se cambia o
# añade alguna cadena. Instala gtranslate si quieres llevar una vida mejor.

import inspect, linecache, pydoc, sys, os# , traceback
from io import StringIO
from smtplib import SMTP, SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime

import locale
if locale.getlocale()[0] is None:
    locale.setlocale(locale.LC_ALL, '')
import gettext
TRANSLATION_DOMAIN = "gtkexcepthook"
LOCALE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "locale"))
language = gettext.translation(TRANSLATION_DOMAIN, LOCALE_DIR, [locale.getdefaultlocale()[0]])
language.install()
_ = language.gettext

import gi
gi.require_version("Gtk", '3.0')
from gi import pygtkcompat

try:
    from gi import pygtkcompat
except importerror:
    pygtkcompat = none
    from gi.repository import Gtk as gtk
    from gi.repository import GObject as gobject

if pygtkcompat is not None:
    pygtkcompat.enable()
    pygtkcompat.enable_gtk(version='3.0')
    import gtk
    import gobject

import pango

from formularios.utils import dialogo_entrada as fdialogo
from formularios.ventana_progreso import VentanaActividad

#def analyse(exctyp, value, tb):
#    trace = StringIO()
#    traceback.print_exception(exctyp, value, tb, None, trace)
#    return trace

def lookup(name, frame, lcls):
    '''Find the value for a given name in the given frame'''
    if name in lcls:
        return 'local', lcls[name]
    elif name in frame.f_globals:
        return 'global', frame.f_globals[name]
    elif '__builtins__' in frame.f_globals:
        builtins = frame.f_globals['__builtins__']
        if type(builtins) is dict:
            if name in builtins:
                return 'builtin', builtins[name]
        else:
            if hasattr(builtins, name):
                return 'builtin', getattr(builtins, name)
    return None, []

def analyse(exctyp, value, tb):
    import tokenize, keyword

    trace = StringIO()
    nlines = 3
    frecs = inspect.getinnerframes(tb, nlines)
    trace.write('Traceback (most recent call last):\n')
    for frame, fname, lineno, funcname, context, cindex in frecs: #@UnusedVariable
        trace.write('  File "%s", line %d, ' % (fname, lineno))
        args, varargs, varkw, lcls = inspect.getargvalues(frame)

        def readline(lno=[lineno], *args):
            if args: print(args)
            try: return linecache.getline(fname, lno[0])
            finally: lno[0] += 1
        todo, prev, name, scope = {}, None, '', None
        for ttype, tstr, stup, etup, line in tokenize.generate_tokens(readline): #@UnusedVariable
            if ttype == tokenize.NAME and tstr not in keyword.kwlist:
                if name:
                    if name[-1] == '.':
                        try:
                            val = getattr(prev, tstr)
                        except AttributeError:
                            # XXX skip the rest of this identifier only
                            break
                        name += tstr
                else:
                    assert not name and not scope
                    scope, val = lookup(tstr, frame, lcls)
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
        trace.write(funcname
                     + inspect.formatargvalues(args,
                        varargs,
                        varkw,
                        lcls,
                        formatvalue=lambda v: '='+pydoc.text.repr(v))
                     +'\n')
        if context is None:
            context = []
        trace.write(''.join(['    ' + x.replace('\t', '  ') for x in [a for a in context if a.strip()]]))
        if len(todo):
            trace.write('  variables: %s\n' % myprettyprint(todo))

    trace.write('%s: %s' % (exctyp.__name__, value))
    return trace

def myprettyprint(stuff):
    # from lib.pprintpp import pformat
    from pprintpp import pformat
    #from pprint import pformat
    return pformat(stuff)
    #from myprettyprint import print_dict
    #if isinstance(stuff, dict):
    #    return print_dict(stuff)
    #else:
    #    return pformat(stuff)

def prettyprint_html(m):
    """
    Envuelvo el cuerpo del correo en HTML usando
    http://code.google.com/p/google-code-prettify/
    """
    TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   "..", "informes"))
    tmpl = open(os.path.join(TEMPLATE_DIR, "traceback_template.html"))
    s = "".join(tmpl.readlines())
    tmpl.close()
    #cabecera, traza = m.split("Excepción capturada.\n\n")
    #cabecera += "Excepción capturada.\n\n"
    traza = m
    mark = "<!-- TRACEBACK_HERE -->"
    s = s.replace(mark, mark + "\n\n" + traza)
    #mensaje_html = cabecera + s
    mensaje_html = s
    return mensaje_html

def _info(exctyp, value, tb):
    # DONE: Si se puede enviar por correo, enviar por correo y no abrir
    # siquiera la ventana. O guardar a log o algo así si no se puede. Lo de
    # preguntar al usuario se tiene que quedar como última opción, porque
    # siempre pasan del tema. Solo mostrar una ventana si no se puede continuar
    # la ejecución del programa de ninguna de las maneras.
    trace = None
    dialog = gtk.MessageDialog(parent=None, flags=0,
                                type=gtk.MESSAGE_WARNING,
                                buttons=gtk.BUTTONS_NONE)
    dialog.set_title(_("Bug Detected"))
    # if gtk.check_version(2, 4, 0) is not None:
    #     dialog.set_has_separator(False)

    primary = _("<big><b>A programming error has been detected during the execution of this program.</b></big>")
    secondary = _("It probably isn't fatal, but should be reported to the developers nonetheless.")

    try:
        setsec = dialog.format_secondary_text
    except AttributeError:
        raise
        dialog.vbox.get_children()[0].get_children()[1].set_markup('%s\n\n%s'
            % (primary, secondary))
        #lbl.set_property("use-markup", True)
    else:
        del setsec
        dialog.set_markup(primary)
        dialog.format_secondary_text(secondary)

    try:
        email = feedback #@UndefinedVariable
        dialog.add_button(_("Report..."), 3)
        autosend = True
    except NameError:
        # could ask for an email address instead...
        autosend = False
    dialog.add_button(_("Details..."), 2)
    dialog.add_button(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE)
    dialog.add_button(gtk.STOCK_QUIT, 1)
    dialog.add_button(_("Close all"), 4)

    while True:
        if not autosend:
            resp = dialog.run()
        else:
            resp = 3    # Emulo que se ha pulsado el botón.
        if resp == 3:
            vpro = VentanaActividad(
                texto = "Enviando informe de error. Por favor, espere...\n"
                        "(Si esta ventana persiste, reinicie la aplicación)")
            # TODO: PLAN: Si la ventana lleva más de un minuto sin enviar el
            # correo, ya no lo hará casi seguro. Cerrarla programáticamente.
            vpro.mostrar()
            vpro.mover()
            if trace == None:
                trace = analyse(exctyp, value, tb)
            vpro.mover()
            # TODO: prettyprint, deal with problems in sending feedback, &tc
            try:
                server = smtphost #@UndefinedVariable
            except NameError:
                server = 'localhost'
            vpro.mover()
            msgmail = MIMEMultipart("alternative")
            msgmail["Subject"] = "Geotex-INN -- Excepción capturada"
            msgmail["From"] = email
            msgmail["To"] = "Soporte G-INN"
            traza = trace.getvalue()
            message = 'From: %s"\nTo: %s\nSubject: Geotex-INN'\
                      ' -- Excepción capturada.\n\n%s'%(msgmail["From"],
                                                        msgmail["To"],
                                                        traza)
            text_version = message
            html_version = prettyprint_html(traza)
            ferrname = traza.split("\n")[-1].split(":")[0]
            if not ferrname:
                ferrname = "error_ginn"
            #import re
            #regexpline = re.compile("line [0-9]+")
            #try:
            #    linea = regexplline.findall(traza)[-1]
            #except IndexError:
            #    pass
            #else:
            #    ferrname += "_" + linea.replace(" ", "_")
            # XXX: Test del HTML. En el navegador se ve fetén, pero en el
            #      thunderbird no carga el prettyPrint()
            #      Tristeza infinita.
            if False:
                tempfile = open("/tmp/%s.html" % ferrname, "w")
                tempfile.write(html_version)
                tempfile.close()
                os.system("xdg-open /tmp/%s.html" % ferrname)
            # XXX
            part1 = MIMEText(text_version, "plain")
            part2 = MIMEText(html_version, "html")
            msgmail.attach(part1)
            msgmail.attach(part2)
            adjunto = MIMEBase("text", "html")
            adjunto.set_payload(html_version)
            encoders.encode_base64(adjunto)
            adjunto.add_header("Content-Disposition",
                               "attachment;filename=%s.html" % (ferrname))
            msgmail.attach(adjunto)
            vpro.mover()
            # Aparte de enviarlo por correo, si tengo consola, vuelco.
            try:
                sys.stderr.write("\n")
                sys.stderr.write("="*79)
                sys.stderr.write(datetime.datetime.now().strftime(
                    "%Y%m%d %H:%M:%S").center(80))
                sys.stderr.write("="*79)
                sys.stderr.write("\n")
                sys.stderr.write(message)
                sys.stderr.write("\n")
            except:
                pass
            s = SMTP()
            vpro.mover()
            try:
                s.connect(server, port) #@UndefinedVariable
            except NameError:
                s.connect(server)
            vpro.mover()
            try:
                passoteword = password #@UndefinedVariable
            except NameError:
                pass
            vpro.ocultar()
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
                except NameError as msg:
                    txt="Introduzca contraseña del servidor de correo %s"%(
                        server)
                    passoteword = fdialogo(titulo = "CONTRASEÑA:",
                                                        texto = txt,
                                                        pwd = True)
                    if passoteword == None:
                        continue
                vpro.mostrar()
                vpro.mover()
                try:
                    if ssl: #@UndefinedVariable
                        s.ehlo()
                        s.starttls()
                        s.ehlo()
                except (ValueError, NameError) as msg:
                    pass    # No hay variable ssl. No cifrado.
                vpro.mover()
                try:
                    s.login(email, passoteword)
                except SMTPException:
                    print(msg)
                    pass    # Servidor no necesita autenticación.
                vpro.mover()
            except NameError as msg:
                pass    # No se ha especificado contraseña, será que no
                        # necesita autentificación entonces.
            vpro.mover()
            try:
                try:
                    s.sendmail(email, (devs_to,), msgmail.as_string()) #@UndefinedVariable
                except NameError:
                    s.sendmail(email, (email,), msgmail.as_string())
            except:
                vpro.ocultar()
                autosend = False # ¿No Inet? Volver a bucle mostrando ventana.
                                    # TODO: Y además volcar a log o algo, ¿no?
                continue
            else:
                vpro.ocultar()
                s.quit()
                break

        elif resp == 2:
            if trace == None:
                trace = analyse(exctyp, value, tb)

            # Show details...
            details = gtk.Dialog(_("Bug Details"), dialog,
              gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
              (gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE, ))
            # details.set_property("has-separator", False)

            textview = gtk.TextView(); textview.show()
            textview.set_editable(False)
            textview.modify_font(pango.FontDescription("Monospace"))

            sw = gtk.ScrolledWindow(); sw.show()
            sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            sw.add(textview)
            details.vbox.add(sw)
            textbuffer = textview.get_buffer()
            textbuffer.set_text(trace.getvalue())

            monitor = gtk.gdk.screen_get_default().get_monitor_at_window(dialog.window)
            area = gtk.gdk.screen_get_default().get_monitor_geometry(monitor)
            try:
                w = area.width // 1.6
                h = area.height // 1.6
            except SyntaxError:
                # python < 2.2
                w = area.width / 1.6
                h = area.height / 1.6
            details.set_default_size(int(w), int(h))

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
    class X(object):
        pass
    x = X()
    x.y = 'Test'
    x.z = x
    w = ' e'
    # Descomentar para botón enviar por correo:
    feedback = 'informatica@geotexan.com'
    smtphost = 'smtp.googlemail.com'
    devs_to = "frbogado@geotexan.com"
    port = 465
    port = 587
    ssl = True
    1, x.z.y, f, w #@UndefinedVariable
    raise Exception(x.z.y + w)

