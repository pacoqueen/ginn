#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2014 Francisco José Rodríguez Bogado
# Licencia: http://en.wikipedia.org/wiki/Beerware
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <bogado@qinn.es> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return.
# ----------------------------------------------------------------------------


"""
Wrapper sobre print que no llega a ser un MonkeyPatch por poco.
Lo que intenta es ofrecer una alternativa a print para cuando
las ventanas se ejecutan sin salida estándar para evitar errores
en print, por un lado, y que no se pierda toda esa "valiosa" información
de stdout/stderr, por otro.
"""

import sys
#import os
import tempfile

def myprint(*args, **kw):
    """
    Si hay salida estándar, usa print.
    Si no, al menos no muestra errores.
    """
    cad = " ".join([str(a) for a in args])
    cad += " "
    cad += " ".join([str(k) + "=" + str(kw[k]) for k in kw])
    cad = cad.strip()
    if "pythonw" in sys.executable:
        fout = tempfile.TemporaryFile()
        #sys.stderr = sys.stdout = fout
        try:
            fout.write(cad)
        finally:
            fout.close()
    else:
        print(cad)

def test():
    """
    Prueba. Punto.
    """
    print "Tal y pam", 12*3
    myprint("Tal y pam", 12*3, a = 2)
    myprint()

if __name__ == "__main__":
    test()

