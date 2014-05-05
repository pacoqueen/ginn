#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Necesitamos algo que facilite la creación de partes de producción cuando se
fabrican rollos de ancho múltiple.
Aquí voy a intentar crear una especie de "monkey-patch" que permita, según
la configuración de producción, crear los partes necesarios para ir después
pesando los rollos según vaya haciendo falta.
Idealmente lleva una lista de productos que se podrán arrastrar a una barra
que represente los 5.5 m que la línea puede hacer. Al arrastrar un producto,
se deshabilitarán para arrastrar los que no sean "compatibles" con él (según
gramaje o porque exceda de longitud). Al final debe quedar una lista de
productos a fabricar (cada uno de medida diferente creará un parte) que
entre todos sumen 5.5 metros de ancho y sean del mismo tipo.
"""

import pygtk
import gtk
from framework import pclases

def main():
    """
    Crea la ventana y lanza Gtk.
    """
    pass

if __name__ == "__main__":
    main()

