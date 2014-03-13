#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2014 Francisco José Rodríguez Bogado.                    #
#                         <frbogado@geotexan.com>                             #
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
import mx.DateTime
from framework import pclases
from formularios.reports import abrir_pdf
from tempfile import gettempdir
from gtk import TreeStore

def treeview2pdf(tv, titulo = None, fecha = None, apaisado = None, 
                 pijama = False, graficos = [], numcols_a_totalizar = [], 
                 extra_data = []):
    """
    A partir de un TreeView crea un PDF con su contenido.
    1.- Asigna un nombre de archivo en función del nombre del TreeView.
    2.- Si titulo es None, asigna como título el nombre del TreeView.
    3.- El ancho de los campos será el ancho relativo en porcentaje que ocupa 
        el ancho de la columna (get_width) a la que correspondería. El título 
        del campo será el título (get_title) de la columna.
    4.- Si fecha no es None debe ser una cadena de texto. Si es None, se 
        usará la fecha actual del sistema.
    5.- Si la suma del ancho de las columnas del TreeView es superior a 800 
        píxeles el PDF generado será apaisado, a no ser que se fuerce mediante 
        el parámetro "apaisado" que recibe la función.
    numcols_a_totalizar es una lista de índices (empezando por 0) de las 
    columnas a las que se va a intentar convertir a número y sumar para 
    mostrar una última línea con el texto "TOTAL" o "TOTALES" si hay más de 
    una.
    extra_data son líneas que se añadirán a las que tiene el TreeView 
    *al final* del informe (incluso detrás de los totales, si los hubiera).
    """
    archivo = get_nombre_archivo_from_tv(tv)
    if titulo == None:
        titulo = get_titulo_from_tv(tv)
    campos, pdf_apaisado, cols_a_derecha, cols_centradas=get_campos_from_tv(tv)
    datos = get_datos_from_tv(tv)
    totales = dict(zip(numcols_a_totalizar, len(numcols_a_totalizar) * [0]))
    for fila in datos:  # Si es un TreeView solo sumaré los totales de primer 
                    # nivel. Los hijos se marcan con ">" al inicio del texto.
        try:
            if (fila and 
                    (fila[0].startswith(">") 
                        or ("]" in fila[0] 
                            and fila[0].split("]")[1].startswith(">")))):
                continue
        except (AttributeError, IndexError):
            pass    # Aquí no ha pasado nada. 
        for numcol in totales:
            # Primero hay que limpiar de formato el texto.
            valor_a_parsear = fila[numcol]
            try:
                valor_a_parsear = valor_a_parsear.split("]")[1]
            except IndexError:
                pass
            if valor_a_parsear in ("---", "==="):
                continue
            try:
                valor_a_sumar = utils.parse_float(valor_a_parsear)
            except ValueError:  # ¿No hay dato en esa fila? Entonces cuento 
                                # instancias.
                valor_a_sumar = 1
                #print fila, numcol, fila[numcol]
            if pclases.DEBUG:
                print "+", fila[numcol], "=", valor_a_sumar
            totales[numcol] += valor_a_sumar
    if totales and datos:
        last_i = len(datos) - 1  # Apuntará a la última línea no nula
        while (last_i > 0 
               and reduce(lambda x, y: str(x) + str(y), datos[last_i]) == ""):
            last_i -= 1
        if (datos[last_i] and 
            not reduce(lambda x, y: x == y == "---" and "---", datos[last_i])):
            datos.append(("---", ) * len(campos))
        fila = ["TOTAL"] + [""] * (len(campos) - 1)
        if len(totales) > 1:
            fila[0] = "TOTALES"
        for total in totales:
            fila[total] = utils.float2str(totales[total])
                                            #, precision = 2, autodec = True)
        datos.append(fila)
    if extra_data and not isinstance(extra_data[0], (tuple, list)):
        extra_data = [extra_data]
    for extra in extra_data:
        dif_len = len(campos) - len(extra)
        if dif_len <> 0 and not isinstance(extra, list):
            extra = list(extra)
        if dif_len > 0:
            extra += [""] * dif_len
        elif dif_len < 0:
            extra = extra[:len(campos)]
        datos.append(extra)
    if not fecha:
        fecha = utils.str_fecha(mx.DateTime.localtime())
    if apaisado != None:
        pdf_apaisado = apaisado
    return geninformes.imprimir2(archivo, 
                                 titulo, 
                                 campos, 
                                 datos, 
                                 fecha, 
                                 apaisado = pdf_apaisado, 
                                 cols_a_derecha = cols_a_derecha, 
                                 cols_centradas = cols_centradas, 
                                 pijama = pijama, 
                                 graficos = graficos) 

def get_nombre_archivo_from_tv(tv):
    """
    Devuelve el nombre del archivo que se generará a partir
    del nombre del widget TreeView.
    """
    # Algunos caracteres dan problemas en SO Windows.
    nomtreeview = tv.get_name().replace(" ", "_").replace(":", "_")
    nomarchivo = os.path.join(gettempdir(), "%s_%s.pdf" % (
                    nomtreeview, geninformes.give_me_the_name_baby()))
    return nomarchivo

def _str(x):
    if isinstance(x, bool):
        if x:
            return "[x]"
        else:
            return "[ ]"
    return str(x)

def get_datos_from_tv(tv):
    """
    Devuelve una lista de tuplas. Cada tupla contiene los datos de las cells 
    del TreeView para cada fila.
    Si la fila es padre de otra fila, añade debajo de la misma las filas hijas 
    con espacios a su izquierda y un separador horizontal al final.
    """
    datos = []
    model = tv.get_model()
    numcols = len(tv.get_columns())
    for fila in model:
        filadato = []
        for i in xrange(numcols):
            index_columna = tv.get_column(i).get_data("q_ncol")
            if index_columna is None:
                index_columna = i
            filadato.append(_str(fila[index_columna]))
            #filadato.append(fila[i])
        if isinstance(model, TreeStore):
            filadato = ["[fuente=Courier-Bold::6]" + i for i in filadato]
        # Si es un ListStore, que no lleva hijos, dejo la fuente por defecto.
        datos.append(filadato)
        if hasattr(fila, 'iterchildren'):
            filas_hijas = agregar_hijos(fila, numcols, 1, tv)
            if filas_hijas != [] and len(datos) > 1 and datos[-2][0] != "---":
                datos.insert(-1, ("---", ) * numcols)
            for fila_hija in filas_hijas:
                datos.append(fila_hija)
            if filas_hijas != []:
                datos.append(("---", ) * numcols)
    # Elimino líneas duplicadas consecutivas:
    #datosbak = datos[:]
    #datos = []
    #for i in xrange(len(datosbak)-1)
    #    if datos[i] != datos[i+1]:
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
                if index_columna is None: # Por si no viene de utils.preparar_*
                    index_columna = col
                if index_columna == 0:
                    filahijo.append("%s%s" % (
                        "[color=gris]" + "> " * numespacios, 
                        _str(hijo[index_columna])))
                else:
                    filahijo.append("%s" % (_str(hijo[index_columna])))     
                        # Por si acaso trae un entero, un float o algo asina.
            filas += [filahijo] + agregar_hijos(hijo, 
                                                numcols, 
                                                numespacios + 1, 
                                                tv)
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
    Devuelve una tupla de tuplas. Cada tupla "interior" tiene el nombre 
    del campo y el ancho relativo en tanto porciento respecto al total 
    del TreeView.
    Devuelve también un boolean que será True si el ancho total de las 
    columnas supera los 800 píxeles.
    """
    cols = []
    anchotv = 0
    for column in tv.get_columns():
        if not column.get_property("visible"):
            continue 
        anchocol = column.get_width()
        if anchocol == 0:
            anchocol = column.get_fixed_width()
            if anchocol == 0:
                anchocol = 100.0 / len(tv.get_columns())
        anchotv += anchocol
        cell = column.get_cell_renderers()[0]   # Nunca uso más de un cell por 
                                                # columna. La alineación del 
                                                # primero me basta.
        xalign = cell.get_property("xalign")
        if xalign < 0.4:
            alineacion = -1     # Izquierda
        elif 0.4 <= xalign <= 0.6:
            alineacion = 0      # Centro
        else:
            alineacion = 1      # Derecha
        tit_columna = column.get_title()
        cols.append({'título': tit_columna, 
                     'ancho': anchocol, 
                     'alineación': alineacion})
    res = []
    cols_a_derecha = []
    cols_centradas = []
    for col, i in zip(cols, range(len(cols))):
        floanchocol = (col['ancho'] * 100.0) / anchotv
        col['ancho'] = int(round(floanchocol, 0))
            # Trunco para no sobrepasar el 100% en la suma total.
        res.append((col['título'], col['ancho']))
        if col['alineación'] == 1:
            cols_a_derecha.append(i)
        elif col['alineación'] == 0:
            cols_centradas.append(i)
    return res, anchotv >= 800, cols_a_derecha, cols_centradas

def gtktable2list(tabla):
    """
    Devuelve una lista anidada de filas que contienen el texto de los 
    labels y entries de la tabla Gtk.
    """
    cols = tabla.get_property("n-columns")
    fils = tabla.get_property("n-rows")
    res = []
    for f in range(fils):
        fila = []
        for c in range(cols):
            fila.append("")
        res.append(fila)
    for child in tabla.get_children():
        i, d, ar, ab = tabla.child_get(child, "left-attach", "right-attach", 
                                              "top-attach", "bottom-attach")
        try:
            texto = child.get_text()
            try:
                texto = texto.decode("utf8").encode("latin1")
            except: 
                pass
        except AttributeError:
            pass    # El widget no es un entry ni un label
        else:
            res[ar][i] = texto
    return res

def probar():
    """
    Test
    """
    #abrir_pdf(treeview2pdf(tv, titulo, fecha))
    esto_habria_que_annadirlo_al_scrip_inicial = "abrir_pdf(treeview2pdf(self.wids['tv_datos']))"  # @UnusedVariable
    Trazabilidad(pclases.Rollo.select(orderBy = "-id")[0], locals_adicionales = {'treeview2pdf': treeview2pdf, 'abrir_pdf': abrir_pdf})

if __name__ == "__main__":
    probar()

