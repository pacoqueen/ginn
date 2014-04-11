#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Inspector Clouseau
==================

Now with a GUI!!
"""

DEBUG = True

from gi.repository import Gtk
import os

class Clouseau(Gtk.Window):
    def __init__(self):
        """
        Constructor de la ventana. La carga de widgets, conexiones y toda 
        esa mierda va aquí.
        """
        self.wids = Gtk.Builder()
        self.wids.add_from_file("clouseau.glade")
        handlers = {"b_start/clicked": self.empezar, 
                    "ventana/delete-event": Gtk.main_quit, 
                    "b_select_directorio/clicked": self.buscar_sources}
        for wid_signal in handlers:
            wid, signal = wid_signal.split("/")
            callback = handlers[wid_signal]
            self.wids.get_object(wid).connect(signal, callback)
        for concepto in ("existencias", "prod", "salidas", "consumos"): 
            for periodo in ("ini", "fin", ""):
                for tipo in ("fib", "gtx", "cem"):
                    nombre_boton = "b_%s_%s_%s" % (concepto, periodo, tipo)
                    boton = self.wids.get_object(nombre_boton)
                    nombre_entry = nombre_boton.replace("b_", "e_")
                    entry = self.wids.get_object(nombre_entry)
                    try:
                        boton.connect("clicked", self.select_source, entry)
                    except AttributeError:
                        pass    # Combinación que no existe como botón.
        self.wids.get_object("ventana").show_all()


    def select_source(self, boton, entry):
        """
        Coloca en el entry recibido el fichero seleccionado al abrir el 
        diálogo con el botón que ha lanzado el evento "clicked".
        """
        dialogo_select_csv = Gtk.FileChooserDialog(
            "SELECCIONE FICHERO ORIGEN", 
            self.wids.get_object("ventana"), 
            Gtk.FileChooserAction.OPEN, 
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, 
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
            # TODO: Añadir filtro para seleccionar el CSV correcto y además 
            # que *gtx*.csv o *fib*.csv o incluso existencias* consum* o lo 
            # que sea en función del nombre del botón o del entry (si es que 
            # se puede sacar por get_name; si no, recibirlo como parámetro).
        response = dialogo_select_csv.run()
        if response == Gtk.ResponseType.OK:
            csvname = dialogo_select_csv.get_filename()
            if DEBUG:
                print("Directorio seleccionado: ", csvname)
        dialogo_select_csv.destroy()
        entry.set_text(csvname)
        entry.set_position(-1)    

    
    def buscar_sources(self, boton):
        """
        Muestra un diálogo para seleccionar un directorio.
        Si pulsa aceptar, recorre el contenido del directorio buscando 
        ficheros que cumplan un determinado formato e introduce sus 
        nombres en los entries inferiores de la ventana.
        """
        dialogo_select_dir = Gtk.FileChooserDialog(
            "SELECCIONE DIRECTORIO ORIGEN", 
            self.wids.get_object("ventana"), 
            Gtk.FileChooserAction.SELECT_FOLDER, 
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, 
             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        response = dialogo_select_dir.run()
        if response == Gtk.ResponseType.OK:
            dirname = dialogo_select_dir.get_filename()
            if DEBUG:
                print("Directorio seleccionado: ", dirname)
        dialogo_select_dir.destroy()
        entry_directorio = self.wids.get_object("e_directorio")
        entry_directorio.set_text(dirname)
        entry_directorio.set_position(-1)    
    
    
    def empezar(self, boton):
        """
        Callback del botón empezar. Recibe el propio botón en `boton`.
        """
        wids_list = ['e_existencias_ini_fib', 'e_existencias_ini_gtx', 
                     'e_existencias_ini_cem', 'e_prod_fib', 'e_prod_gtx',
                     'e_prod_cem', 'e_salidas_fib', 'e_salidas_gtx', 
                     'e_salidas_cem', 'e_consumos', 'e_existencias_fin_fib',
                     'e_existencias_fin_gtx', 'e_existencias_fin_cem'
                    ]
        entries_text = []
        for widget in wids_list:
            entry_text = self.wids.get_object(widget)
            simple_text = entry_text.get_text()
            entries_text.append(simple_text)
        comando = "dir " + " ".join(entries_text)
        if (DEBUG):
            print(comando)
        os.system(comando)


def run(ejecutar = True):
    """
    Crea y abre (si `ejecutar` es `True`) la ventana.
    """
    ventana_clouseau = Clouseau()
    if ejecutar:
        Gtk.main()


if __name__ == '__main__':
    run()

