#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Inspector Clouseau
==================

Now with a GUI!!
"""

DEBUG = True

from gi.repository import Gtk
import os, sys
import tempfile

DIRSCRIPT = os.path.dirname(os.path.abspath(sys.argv[0]))
CLOUSEAU_COMMAND = os.path.join(DIRSCRIPT, "clouseau.py")

class Clouseau(Gtk.Window):
    def __init__(self):
        """
        Constructor de la ventana. La carga de widgets, conexiones y toda 
        esa mierda va aquí.
        """
        self.wids = Gtk.Builder()
        gladefile = os.path.abspath(os.path.join(DIRSCRIPT, "clouseau.glade"))
        self.wids.add_from_file(gladefile)
        self.wids.get_object("b_start").set_sensitive(False)
        self.entries = {}
        handlers = {"b_start/clicked": self.empezar, 
                    "ventana/delete-event": Gtk.main_quit, 
                    "b_select_directorio/clicked": self.auto_buscar_sources}
        for wid_signal in handlers:
            wid, signal = wid_signal.split("/")
            callback = handlers[wid_signal]
            self.wids.get_object(wid).connect(signal, callback)
        for concepto in ("existencias", "prod", "salidas", "consumos"): 
            for periodo in ("ini", "fin", ""):
                for tipo in ("fib", "gtx", "cem"):
                    nombre_boton = "b_%s_%s_%s" % (concepto, periodo, tipo)
                    nombre_boton = nombre_boton.replace("__", "_")
                    boton = self.wids.get_object(nombre_boton)
                    nombre_entry = nombre_boton.replace("b_", "e_")
                    entry = self.wids.get_object(nombre_entry)
                    try:
                        boton.connect("clicked", self.select_source, entry)
                    except AttributeError:
                        pass    # Combinación que no existe como botón.
                    else:
                        # Aprovechando que si encuentra el botón también 
                        # encontrará el entry (se llaman --casi-- igual).
                        self.entries[nombre_entry] = entry
                        entry.connect('changed', self.activar_ejecutar)
        self.wids.get_object("ventana").show_all()


    def activar_ejecutar(self, entry):
        """
        Si todos los entries de ficheros fuente están informados, activa el 
        botón de ejecutar.
        """
        activar = True
        for nom_ent in self.entries:
            nomfichero = self.entries[nom_ent].get_text()
            if not nomfichero:
                activar = False
                break
        self.wids.get_object("b_start").set_sensitive(activar)


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
        # Si hay un fichero seleccionado, lo pongo por defecto en el diálogo.
        dirname = self.wids.get_object("e_directorio").get_text()
        if dirname:
            dialogo_select_csv.set_current_folder(dirname)
        filname = entry.get_text()
        if filname:
            dialogo_select_csv.set_current_name(filname)
        # Ahora toca ejecutar el diálogo de selección de fichero fuente:
        response = dialogo_select_csv.run()
        if response == Gtk.ResponseType.OK:
            csvname = dialogo_select_csv.get_filename()
            if DEBUG:
                print("Fichero seleccionado: ", csvname)
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
    

    def auto_buscar_sources(self, boton):
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
        if os.path.basename(os.path.abspath(os.path.curdir)) == "scripts":
            dialogo_select_dir.set_current_folder(
                    os.path.join("..", "..", "tests"))
        response = dialogo_select_dir.run()
        if response == Gtk.ResponseType.OK:
            dirname = dialogo_select_dir.get_filename()
            if DEBUG:
                print("Directorio seleccionado: ", dirname)
            # Si selecciono el directorio ENTRANDO en él, no lo pilla bien.
            while not os.path.exists(dirname) and dirname:
                dirname = os.path.dirname(dirname)
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
                nom_entry = nom_entry.replace("__", "_")
                fullpath_fichero = os.path.join(dirname, fichero)
                try:
                    self.wids.get_object(nom_entry).set_text(fullpath_fichero)
                except AttributeError:
                    if DEBUG:
                        print("\t\t", nom_entry, "no existe")
                else:
                    self.wids.get_object(nom_entry).set_position(-1)    
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
        tempodiff = tempfile.NamedTemporaryFile(suffix = ".csv", 
                                                delete = False)
        fout = os.path.abspath(tempodiff.name)
        comando = CLOUSEAU_COMMAND + " " + " ".join(
                ['"%s"' % (text) for text in entries_text]
                ) + " > " + fout + " && localc " + fout
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
    elif concepto.isnumeric():
        concepto, periodo = periodo, concepto
    # Periodo, si lo lleva:
    if periodo:
        if "ini" in periodo:
            periodo = "ini"
        elif "fin" in periodo:
            periodo = "fin"
        else:
            periodo = ""    # Debe ser 20140201 o algo asina.
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

