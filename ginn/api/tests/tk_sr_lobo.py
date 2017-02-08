#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Simple wrapper around sr_lobo.py to see output in graphic mode.
"""

import os
from Tkinter import Tk, BOTH, RIGHT, LEFT, RAISED, PhotoImage
from ttk import Frame, Button, Style


# pylint: disable=too-many-ancestors
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

    def init_ui(self):
        """ Crea la ventana. """
        self.parent.title("Sr. Lobo - Soluciono problemas")
        dirname = os.path.abspath(os.path.dirname(__file__))
        iconpath = os.path.join(dirname, "mr_wolf.png")
        # self.parent.iconbitmap(iconpath)
        icon = PhotoImage(file=iconpath)
        # pylint: disable=protected-access
        self.parent.tk.call("wm", "iconphoto", self.parent._w, icon)
        self.style = Style()
        self.style.theme_use("default")
        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)
        self.pack(fill=BOTH, expand=True)
        save_button = Button(self, text="Guardar", command=self.saveas)
        save_button.pack(side=LEFT, padx=5, pady=5)
        reload_button = Button(self, text="Recargar", command=self.reload)
        reload_button.pack(side=LEFT, padx=5, pady=5, expand=True)
        quit_button = Button(self, text="Salir", command=self.quit)
        quit_button.pack(side=RIGHT, padx=5, pady=5)

    def center_window(self):
        """ Centra la ventana en la pantalla. """
        width = 640
        height = 480
        screenw = self.parent.winfo_screenwidth()
        screenh = self.parent.winfo_screenheight()
        xpos = (screenw - width)/2
        ypos = (screenh - height)/2
        self.parent.geometry('%dx%d+%d+%d' % (width, height, xpos, ypos))

    def saveas(self):
        """ Guarda el contenido del widget de texto en un nuevo fichero. """
        # TODO
        pass

    def run_sr_lobo(self, path_report=None):
        """
        Ejecuta el verdadero script y carga en el widget el contenido del
        fichero de salida. El fichero de salida se creará en la ruta
        recibida «path_report», que será con lo que se invoque sr_lobo. Si no
        se recibe nada, usa el que genere sr_lobo.py por defecto.
        """
        if path_report:
            self.textfile = path_report
        # TODO: importar sr_lobo y pasar el fichero como opción.

    def reload(self):
        """ Recarga el contenido del fichero en el widget. """
        # TODO: Todavía no tengo los widgets de texto.
        pass


def main():
    """ Main function. """
    root = Tk()
    app = SrLoboViewer(root)
    # FIXME: Solo para pruebas:
    fp_report = "tk_sr_lobo.py"
    app.run_sr_lobo(fp_report)
    root.mainloop()

if __name__ == "__main__":
    main()
