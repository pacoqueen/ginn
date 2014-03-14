#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2014 Francisco José Rodríguez Bogado,                    #
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

import os
from informes import geninformes
from formularios import utils
from formularios.trazabilidad import Trazabilidad
from framework import pclases
from formularios.reports import abrir_csv
from tempfile import gettempdir
import csv

def to_float(t, sensibilidad = 2):
    """
    Si t es una cadena de texto con el símbolo del euro o de metros cuadrados, 
    convierte todo lo que puede a flotante con técnica "greedy".
    En otro caso lanza una excepción ValueError al igual que hace el _float 
    de utils.
    sensibilidad es un parámetro para evitar falsos positivos. Si en la cadena 
    hay un cierto número de palabras (2 por defecto) entonces no convierte a 
    número flotante.
    """
    if isinstance(t, (int, float)):
        return float(t)
    from string import digits as numeros
    palabras = []
    for p in t.split():
        if p[0] not in numeros:
            palabras.append(p)
            if len(palabras) >= sensibilidad:
                raise ValueError
    simbolos = ("€", "m²", " m", " kg", " k")
    for s in simbolos:
        if s in t:
            res = utils.parse_float(t[:t.index(s)])
            return res
    raise ValueError

def treeview2csv(tv, filtro_ceros = [], desglosar = False, extra_data = []):
    """
    A partir de un TreeView crea un csv con su contenido.
    1.- Asigna un nombre de archivo en función del nombre del TreeView.
    2.- El título del campo será el título (get_title) de la columna.
    Si «filtro_ceros» contiene números de columna, sustituye los valores 
    numéricos "0" y derivados por la cadena vacía en esas columnas del TV.
    Si «desglosar» es True vuelca también los nodos hijos del treeview. No 
    tiene efecto en los listview (porque son "planos"). Si es False, trata 
    los treeview igual que los listview y no manda desgloses al CSV.
    «extra_data» serán filas adicionales que se agregarán al fichero final.
    """
    archivo = get_nombre_archivo_from_tv(tv)
    campos = get_campos_from_tv(tv)
    datos = get_datos_from_tv(tv, filtro_ceros, desglosar)
    ficherocsv = generar_csv(archivo, campos, datos, extra_data)
    return ficherocsv.name  # Por compatibilidad

def generar_csv(nomarchivo, campos, datos, extra_data = []):
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
    #TODO: ¿Qué pasaría si extra_data tiene más columnas que el resto de filas?
    # Pues que en el servidor se cuelga. En mi GNU/Linux no. No sé qué pasará 
    # con un Office normal hasta que no tenga el feedback de nzumer.
    if extra_data and campos:
        extra_data = ajustar_extra_data(extra_data, len(campos))
        escritor.writerows(extra_data)
    archivo.close()
    return archivo

def ajustar_extra_data(d, numcols):
    """
    Si las filas de d son más largas que el número de columnas, las 
    redistribuye para ajustaras.
    Si son más cortas, añade "casillas" en blanco.
    """
    res = []
    while d:
        fila = d.pop(0)
        if not fila or not isinstance(fila, list):
            continue
        if len(fila) > numcols:
            # Lo normal es que vengan valores a pares: label + dato. Corto 
            # de dos en dos para no descuajaringarlo mucho.
            if numcols % 2 != 0 and numcols > 1:
                corte = numcols - 1 
            else:
                corte = numcols
            fila = fila[:corte]
            d.append(fila[corte:])
        while len(fila) < numcols:
            fila.append("")
        if [i for i in fila if i]:  # Si tiene algún valor no nulo (elimino 
            res.append(fila)        # filas en blanco)
    return  res

def get_nombre_archivo_from_tv(tv):
    """
    Devuelve el nombre del archivo que se generará a partir
    del nombre del widget TreeView.
    """
    nomtreeview = tv.get_name().replace(" ", "_")
    nomarchivo = os.path.join(gettempdir(), "%s_%s.csv" % (nomtreeview, geninformes.give_me_the_name_baby()))
    return nomarchivo

def get_datos_from_tv(tv, filtro_ceros, desglosar):
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
                    valor = to_float(valor)
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
        if hasattr(fila, 'iterchildren') and desglosar:
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
                        valor = to_float(valor)
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
    esto_habria_que_annadirlo_al_scrip_inicial = "abrir_csv(treeview2csv(self.wids['tv_datos']))"  # @UnusedVariable
    Trazabilidad(pclases.Rollo.select(orderBy = "-id")[0], locals_adicionales = {'treeview2csv': treeview2csv, 'abrir_csv': abrir_csv})

if __name__ == "__main__":
    probar()
