#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Simple wrapper around sr_lobo.py to see output in graphic mode.
"""

import os
import sys
import subprocess
from threading import Thread
from Queue import Queue, Empty
from collections import deque
from itertools import islice
from Tkinter import Tk, BOTH, RIGHT, LEFT, X, END, NORMAL, DISABLED
from ttk import Frame, Button, Style, Label
import ScrolledText
import tkFileDialog


# TODO: Ya, si aprendes a empaquetar bien los widgets para aprovechar mejor
# el espacio de la ventana, haces un bind de "/" y "n" para buscar y eso,
# consigues arreglar el desaguisado de las barras de progreso, que vaya la
# interfaz más fluida y arreglar el bug que carga el report que no es...
# lo bordas.

# Funciones para hilos
def iter_except(function, exception):
    """Works like builtin 2-argument `iter()`, but stops on `exception`."""
    try:
        while True:
            yield function()
    except exception:
        return


# Funciones auxiliares
def search_reportfile(ruta="."):
    """
    Busca el último log creado por sr_lobo usando el nombre por defecto y
    devuelve su ruta.
    """
    try:
        res = max([os.path.join(ruta, f) for f in os.listdir(ruta)
                   if f.endswith('sr_lobo.txt')], key=os.path.getctime)
    except ValueError:
        print "Fichero *sr_lobo.txt no encontrado en `{}`.".format(ruta)
        sys.exit(1)
    return res



# pylint: disable=too-few-public-methods
class RedirectText(object):
    """
    Redirige la salida de sys.stdout para usar el texto en el scrolledtext.
    """
    def __init__(self, text_ctrl):
        """ Constructor. """
        self.output = text_ctrl

    def write(self, cadena):
        """
        Aquí es donde realmente se escribe el texto recibido en el
        control usado en el constructor como salida de datos.
        """
        self.output.config(state=NORMAL)
        self.output.insert(END, cadena)
        self.output.see(END)
        self.output.config(state=DISABLED)
        self.output.update_idletasks()

    # pylint: disable=no-self-use
    def fileno(self):
        """ Descriptor de fichero. Haré como que soy la salida estándar. """
        return sys.stdout.fileno()


# pylint: disable=too-many-ancestors,too-many-instance-attributes
class SrLoboViewer(Frame):
    """
    Class around all GUI stuff.
    """
    def __init__(self, parent, txtfile=None):
        """ Constructor. """
        self.textfile = txtfile
        Frame.__init__(self, parent) #, background="white")
        self.parent = parent
        self.init_ui()
        self.center_window()
        self._process = None
        self._cached_stamp = 0

    def init_ui(self):
        """ Crea la ventana. """
        self.parent.title("Sr. Lobo - Soluciono problemas")
        dirname = os.path.abspath(os.path.dirname(__file__))
        iconpath = os.path.join(dirname, "mr_wolf.ico")
        self.parent.iconbitmap(iconpath)
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=True)
        # ## Frame de la salida estándar (consola)
        frameconsole = Frame(self)
        frameconsole.pack(fill=X)
        labelstdout = Label(frameconsole, text="Salida estándar:", width=15)
        labelstdout.pack(side=LEFT, padx=5, pady=5)
        self.consolepad = ScrolledText.ScrolledText(frameconsole,
                                                    background="black",
                                                    foreground="orange",
                                                    font="monospace",
                                                    height=5) # líneas
        self.consolepad.pack(fill=X)
        # ## Frame de la salida del informe (report)
        framereport = Frame(self)
        framereport.pack(fill=X)
        labelreport = Label(framereport, text="Informe:", width=15)
        labelreport.pack(side=LEFT, padx=5, pady=5)
        self.reportpad = ScrolledText.ScrolledText(framereport)
        self.reportpad.pack(fill=X)
        # ## Botones de guardar, recargar y salir.
        save_button = Button(self, text="Guardar", command=self.saveas)
        save_button.pack(side=LEFT, padx=5, pady=5)
        reload_button = Button(self, text="Recargar", command=self.reload)
        reload_button.pack(side=LEFT, padx=5, pady=5, expand=True)
        quit_button = Button(self, text="Salir", command=self.quit)
        quit_button.pack(side=RIGHT, padx=5, pady=5)
        self.update_idletasks()
        self.redir = RedirectText(self.consolepad)

    def quit(self, *args, **kw):
        """ Mata los hilos pendientes y cierra la ventana. """
        if self._process:
            subprocess.Popen.kill(self._process)
        return Frame.quit(self, *args, **kw)

    def center_window(self):
        """ Centra la ventana en la pantalla. """
        width = 800
        height = 600
        screenw = self.parent.winfo_screenwidth()
        screenh = self.parent.winfo_screenheight()
        xpos = (screenw - width)/2
        ypos = (screenh - height)/2
        self.parent.geometry('%dx%d+%d+%d' % (width, height, xpos, ypos))

    def saveas(self):
        """ Guarda el contenido del widget de texto en un nuevo fichero. """
        filename = tkFileDialog.asksaveasfile(mode='w')
        if filename:
            # slice off the last character from get, as an extra return is added
            data = self.reportpad.get('1.0', END+'-1c')
            data = data.encode("utf-8")
            filename.write(data)
            filename.close()

    def run_sr_lobo(self, path_report=None):
        """
        Ejecuta el verdadero script y carga en el widget el contenido del
        fichero de salida. El fichero de salida se creará en la ruta
        recibida «path_report», que será con lo que se invoque sr_lobo. Si no
        se recibe nada, usa el que genere sr_lobo.py por defecto.
        """
        comando = ["python", "-u", "sr_lobo.py"]
        if path_report:
            self.textfile = path_report
            comando.append(path_report)
        else:
            self.textfile = None
        # ##
        self._process = subprocess.Popen(comando,
                                         shell=False,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT,
                                         bufsize=0)
        queue = Queue()
        thread = Thread(target=self.reader_thread, args=[queue])
        thread.start()
        self.update_queue(queue)
        # Busco el fichero que ha debido generar el Sr. Lobo
        if not self.textfile:
            self.textfile = search_reportfile()
        # Cada vez que se actualice el fichero...
        th_output = Thread(target=self.reload, args=[False])
        th_output.start()

    def update_queue(self, queue):
        """Update GUI with items from the queue."""
        # read no more than 10000 lines, use deque to discard lines except the last one,
        for line in deque(islice(iter_except(queue.get_nowait, Empty), 10000), maxlen=1):
            if line is None:
                return # stop updating
            else:
                self.redir.write(line) # update GUI
        self.parent.after(40, self.update_queue, queue) # schedule next update

    def reader_thread(self, queue):
        """Read subprocess output and put it into the queue."""
        sys.stdout.flush()
        for line in iter(self._process.stdout.readline, b''):
            sys.stdout.flush()
            queue.put(line)

    def reload(self, force_reload=True):
        """
        Recarga el contenido del fichero en el widget si ha cambiado o si
        se ha pulsado el botón.
        """
        if not self.textfile and force_reload:
            self.textfile = search_reportfile()
        if self.textfile:
            stamp = os.stat(self.textfile)
            if force_reload or stamp != self._cached_stamp:
                filein = open(self.textfile, "r")
                content = filein.read()
                filein.close()
                self.reportpad.config(state=NORMAL)
                self.reportpad.delete('1.0', END)
                self.reportpad.insert("1.0", content)
                self.reportpad.see(END)
                self.reportpad.config(state=DISABLED)
                self._cached_stamp = stamp


def main():
    """ Main function. """
    root = Tk()
    app = SrLoboViewer(root)
    app.run_sr_lobo()
    root.mainloop()

if __name__ == "__main__":
    main()
