#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008 Francisco José Rodríguez Bogado,                   #
#                          Diego Muñoz Escalante.                             #
# (pacoqueen@users.sourceforge.net, escalant3@users.sourceforge.net)          #
#                                                                             #
# This file is part of GeotexInn.                                             #
#                                                                             #
# GeotexInn is free software; you can redistribute it and/or modify           #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation; either version 2 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# GeotexInn is distributed in the hope that it will be useful,                #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with GeotexInn; if not, write to the Free Software                    #
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA  #
###############################################################################

import sys, os
import geninformes
try:
    import utils
    from trazabilidad import Trazabilidad
except ImportError:
    sys.path.append(os.path.join('..', 'formularios'))
    import utils
    from trazabilidad import Trazabilidad
import mx, mx.DateTime
try:
    import pclases
except ImportError:
    sys.path.append(os.path.join('..', 'framework'))
    import pclases
from informes import abrir_csv
from tempfile import gettempdir
import csv

def treeview2csv(tv, filtro_ceros = []):
    """
    A partir de un TreeView crea un csv con su contenido.
    1.- Asigna un nombre de archivo en función del nombre del TreeView.
    2.- El título del campo será el título (get_title) de la columna.
    Si «filtro_ceros» contiene números de columna, sustituye los valores 
    numéricos "0" y derivados por la cadena vacía en esas columnas del TV.
    """
    archivo = get_nombre_archivo_from_tv(tv)
    campos = get_campos_from_tv(tv)
    datos = get_datos_from_tv(tv, filtro_ceros)
    ficherocsv = generar_csv(archivo, campos, datos)
    return ficherocsv.name  # Por compatibilidad

def generar_csv(nomarchivo, campos, datos):
    """
    Genera un fichero de texto plano en formato "comma separated values" con 
    los títulos de los campos en la primera línea y los datos del treeview 
    recibidos a continuación.
    """
    archivo = open(nomarchivo, "w")
    escritor = csv.writer(archivo, delimiter = ";", lineterminator = "\n")  
        # Por defecto formato "excel".
    escritor.writerow(campos)
    escritor.writerows(datos)
    archivo.close()
    return archivo

def get_nombre_archivo_from_tv(tv):
    """
    Devuelve el nombre del archivo que se generará a partir
    del nombre del widget TreeView.
    """
    nomtreeview = tv.get_name().replace(" ", "_")
    nomarchivo = os.path.join(gettempdir(), "%s_%s.csv" % (nomtreeview, geninformes.give_me_the_name_baby()))
    return nomarchivo

def get_datos_from_tv(tv, filtro_ceros):
    """
    Devuelve una lista de tuplas. Cada tupla contiene los datos de las cells 
    del TreeView para cada fila.
    Si la fila es padre de otra fila, añade debajo de la misma las filas hijas 
    con espacios a su izquierda y un separador horizontal al final.
    """
    # PLAN: Se pueden volcar también fórmulas simplemente como texto en el csv.
    # P. ej.: "=A1+B1". El problema es que en los datos extraídos tal cual del 
    # TreeView no sé qué columnas corresponden a sumatorios. Necesitaría un 
    # marcado especial o un cell invisible dentro de la columna o algo así; y 
    # llevar además el control de la columna [A..n] y fila [1..m] para poder 
    # escribir correctamente la expresión.
    datos = []
    model = tv.get_model()
    numcols = len(tv.get_columns())
    for fila in model:
        filadato = []
        for i in xrange(numcols):
            index_columna = tv.get_column(i).get_data("q_ncol")
            if index_columna is None:
                index_columna = i
            valor = fila[index_columna]
            if isinstance(valor, bool):
                dato = valor and u"Sí".encode("iso-8859-15") or "No"
            else:
                try:
                    valor = utils._float(valor)
                    valor = str(valor).replace(".", ",")
                except ValueError:
                    pass    # No es flotante ni se puede convertir a él.
                finally:
                    try:
                        dato = ("%s" % 
                         (valor)).replace(";", ",").encode("iso-8859-15")
                    except UnicodeEncodeError:
                        dato = ("%s" % 
                         (valor)).replace(";", ",").encode("iso-8859-15", 
                                                           "replace")
                if i in filtro_ceros:
                    if dato in ("0", "0,0", "0,00", "0,000", 
                                 0,  "0.0", "0.00", "0.000"):
                        dato = ""   # Más rápido que una regexp.
            filadato.append(dato)
        datos.append(filadato)
        if hasattr(fila, 'iterchildren'):
            filas_hijas = agregar_hijos(fila, numcols, 1, tv)
            #if filas_hijas != [] and len(datos) > 1 and datos[-2][0] != "---":
            #    datos.insert(-1, ("---", ) * numcols)
            for fila_hija in filas_hijas:
                datos.append(fila_hija)
            #if filas_hijas != []:
            #    datos.append(("---", ) * numcols)
    return datos

def agregar_hijos(fila, numcols, numespacios, tv):
    """
    Devuelve una lista con los hijos de "fila", y éstos a 
    su vez con sus hijos, etc... en diferentes niveles.
    numespacios normalmente será el nivel de profundidad de 
    la recursión * 2.
    """
    iterator_hijos = fila.iterchildren()
    if iterator_hijos == None:
        return []
    else:
        filas = []
        for hijo in iterator_hijos:
            filahijo = []
            for col in xrange(numcols):
                index_columna = tv.get_column(col).get_data("q_ncol")
                if index_columna is None:
                    index_columna = col
                valor = hijo[index_columna]
                if isinstance(valor, bool):
                    dato = valor and u"Sí".encode("iso-8859-15") or "No"
                else:
                    try:
                        valor = utils._float(valor)
                        valor = str(valor).replace(".", ",")
                    except ValueError:
                        pass    # No es flotante ni se puede convertir a él.
                    finally:
                        dato = ("%s" % 
                            valor).replace(";", ",").encode("iso-8859-15", 
                                                            "replace")
                        # Por si acaso trae un entero, un float o algo asina.
                if index_columna == 0:
                    filahijo.append("%s%s" % ("> " * numespacios, dato))
                else:
                    filahijo.append(dato)     
            filas += [filahijo] + agregar_hijos(hijo, numcols, numespacios + 1, tv)
        return filas

def get_nombre_archivo_from(tv):
    """
    Devuelve el nombre del widget "tv".
    """
    return tv.get_name()

def get_titulo_from_tv(tv):
    """
    Devuelve el nombre del widget "tv".
    """
    return tv.get_name()

def get_campos_from_tv(tv):
    """
    Devuelve una tupla de nombres de campo.
    """
    cols = []
    for column in tv.get_columns():
        dato = ("%s" % (column.get_title())).replace(";", ",").encode("iso-8859-15")
        cols.append(dato)
    return cols

def probar():
    """
    Test
    """
    esto_habria_que_annadirlo_al_scrip_inicial = "abrir_csv(treeview2csv(self.wids['tv_datos']))"
    Trazabilidad(pclases.Rollo.select(orderBy = "-id")[0], locals_adicionales = {'treeview2csv': treeview2csv, 'abrir_csv': abrir_csv})

if __name__ == "__main__":
    probar()

