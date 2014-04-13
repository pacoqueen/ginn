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
        self.add_filters(dialogo_select_csv, boton)
        response = dialogo_select_csv.run()
        if response == Gtk.ResponseType.OK:
            csvname = dialogo_select_csv.get_filename()
            if DEBUG:
                print("Directorio seleccionado: ", csvname)
            entry.set_text(csvname)
            entry.set_position(-1)    
        dialogo_select_csv.destroy()


    def add_filters(self, dialogo, boton):
        """
        Filtros para localizar los fuentes adecuadamente según el nombre del 
        botón, que trae el tipo de fichero, periodo, etc.
        """
        nombre_boton = Gtk.Buildable.get_name(boton)
        filter_nombre = Gtk.FileFilter()
        filter_nombre.set_name("Fichero fuente de cierre")
        nombre_fichero = nombre_boton.replace("b_", "") 
        pattern_fichero = "*%s*%s*.csv" % (nombre_fichero.split("_")[0], 
                                           nombre_fichero.split("_")[-1])
        filter_nombre.add_pattern(pattern_fichero)
        dialogo.add_filter(filter_nombre)

        filter_csv = Gtk.FileFilter()
        filter_csv.set_name("Ficheros CSV")
        filter_csv.add_mime_type("text/csv")
        dialogo.add_filter(filter_csv)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Todos")
        filter_any.add_pattern("*")
        dialogo.add_filter(filter_any)
    
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
        dialogo_select_dir.set_current_folder("../../tests")    # TODO: Hacer 
        # que sea "sensitive" al directorio donde se ejecuta. Puede que ya 
        # esté en el directorio "tests"
        response = dialogo_select_dir.run()
        if response == Gtk.ResponseType.OK:
            dirname = dialogo_select_dir.get_filename()
            if DEBUG:
                print("Directorio seleccionado: ", dirname)
            entry_directorio = self.wids.get_object("e_directorio")
            entry_directorio.set_text(dirname)
            entry_directorio.set_position(-1)    
            self.buscar_sources_y_rellenar_entries(dirname)
        dialogo_select_dir.destroy()

    
    def buscar_sources_y_rellenar_entries(self, dirname):
        """
        Recorre el directorio dirname y rellena los entries con los ficheros
        que encuentre y casen con el tipo de fichero fuente buscado.
        """
        for raiz, directorios, ficheros in os.walk(dirname):
            for fichero in ficheros:
                if DEBUG:
                    print("fichero:", fichero)
                concepto, periodo, tipo = analizar(fichero)
                if DEBUG:
                    print("\tconcepto:", concepto, 
                            "; periodo:", periodo, 
                            "; tipo:", tipo)
                if periodo:
                    nom_entry = "e_%s_%s_%s" % (concepto, periodo, tipo)
                elif tipo:
                    nom_entry = "e_%s_%s" % (concepto, tipo)
                else:
                    nom_entry = "e_%s" % (concepto)
                try:
                    self.wids.get_object(nom_entry).set_text(fichero)
                except AttributeError:
                    if DEBUG:
                        print("\t\t", nom_entry, "no existe")
                else:
                    if DEBUG:
                        print("\t\t", nom_entry, "\t[OK]")
    
    
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


def analizar(txt):
    """
    Trata de analizar el texto recibido buscando a qué concepto se refiere, 
    periodo (si lo lleva) y tipo.
    Conceptos: existencias, prod, salidas, consumos.
    Periodo: ini, fin
    Tipo: fib, gtx, cem
    """
    txt = txt.split(".")[0]
    tokens = txt.split("_")
    try:
        concepto, periodo, tipo = tokens
    except ValueError:
        try:
            concepto, tipo = tokens
            periodo = ""
        except ValueError:  # Es "diff.csv" o algo así.
            concepto = tokens[0]
            tipo = periodo = ""
    # Concepto:
    if "exist" in concepto or "stock" in concepto:
        concepto = "existencias"
    elif "prod" in concepto: 
        concepto = "prod"
    elif "sal" in concepto or "vent" in concepto:
        concepto = "salidas"
    elif "cons" in concepto:
        concepto = "consumos"
    # Periodo, si lo lleva:
    if periodo:
        if "ini" in periodo:
            periodo = "ini"
        elif "fin" in periodo:
            periodo = "fin"
    # Y tipo:
    if "fib" in tipo:
        tipo = "fib"
    elif "geotex" in tipo or "gtx" in tipo:
        tipo = "gtx"
    elif "cem" in tipo:
        tipo = "cem"
    return concepto, periodo, tipo


def run(ejecutar = True):
    """
    Crea y abre (si `ejecutar` es `True`) la ventana.
    """
    ventana_clouseau = Clouseau()
    if ejecutar:
        Gtk.main()


if __name__ == '__main__':
    run()

