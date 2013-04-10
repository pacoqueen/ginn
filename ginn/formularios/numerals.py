#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#   numerals.py
#
#   Copyright (C) 1995 by Chema Cortés
#   Portions of code by Francisco José Rodríguez Bogado.
#
###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado,                   #
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


from utils import _float
from fixedpoint import FixedPoint as ffloat

"""
    Módulos numerals para convertir un número en una cadena literal del número.
    Chema Cortés - Agosto 1995
    Convertido de clipper a python en Septiembre 2001
"""

_n1 = ( "un","dos","tres","cuatro","cinco","seis","siete","ocho",
        "nueve","diez","once","doce","trece","catorce","quince",
        "dieciséis","diecisiete","dieciocho","diecinueve","veinte")

_n11 =( "un","dós","trés","cuatro","cinco","séis","siete","ocho","nueve")

_n2 = ( "dieci","veinti","treinta","cuarenta","cincuenta","sesenta",
        "setenta","ochenta","noventa")

_n3 = ( "ciento","dosc","tresc","cuatroc","quin","seisc",
        "setec","ochoc","novec")

def numerals(nNumero, lFemenino=0, moneda = "", fraccion = "", autoomitir = False):
    """
    numerals(nNumero, lFemenino) --> cLiteral

    Convierte el número a una cadena literal de caracteres
    P.e.:       201     -->   "doscientos uno"
               1111     -->   "mil ciento once"

    <nNumero>       Número a convertir
    <lFemenino>     = 'true' si el Literal es femenino
                    P.e.:   201     -->    "doscientas una"
    Los parámetros "moneda" y "fracción" se usarán tras las
    cantidades enteras y decimales respectivamente. Si por
    ejemplo moneda == "euros" y fraccion == "céntimos", se
    obtendrá algo como:
    dieciséis euros con cincuenta céntimos
    (Legalmente se acepta tanto la preposición "con" como
    la conjunción copulativa "y" para expresión en letra
    de la moneda en España.)
    Si "autoomitir" es True y la parte fraccionaria es 0, 
    no la devuelve.
    """
    # Nos aseguramos del tipo de <nNumero>
    # se podría adaptar para usar otros tipos (pe: float)
    cRes = None
    if isinstance(nNumero, str):
        try:
            nNumero = long(nNumero)
        except ValueError:
            nNumero = _float(nNumero)
    if isinstance(nNumero, int):
        if nNumero<0:       cRes = "menos "+_numerals(-nNumero, lFemenino)
        elif nNumero==0:    cRes = "cero"
        else:               cRes = _numerals(nNumero, lFemenino)
        # Excepciones a considerar
        if not lFemenino and nNumero%10 == 1 and nNumero%100!=11:
            cRes += "o"
    elif isinstance(nNumero, (float, ffloat)):
        if nNumero >= 0:
            parte_entera = numerals(int(nNumero), lFemenino)
            numparte_decimal = int(round((nNumero % 1) * 100))
            if not(numparte_decimal == 0 and autoomitir):
                parte_decimal = numerals(numparte_decimal, lFemenino)
                cRes = "%s %s con %s %s" % (parte_entera, moneda, parte_decimal, fraccion)
            else:
                cRes = "%s %s" % (parte_entera, moneda)
        else:
            nNumero *= -1
            parte_entera = numerals(int(nNumero), lFemenino)
            parte_decimal = numerals(int(round((nNumero % 1) * 100)), lFemenino)
            cRes = "menos %s %s con %s %s" % (parte_entera, moneda, parte_decimal, fraccion)
    try:
        cRes = reduce(lambda x, y: x[-1] == " " and y == " " and x or x+y, cRes)    # Elimino los "dobles espacios".
    except TypeError:
        pass    # cRes es "" (vacío), None (no es iterable) o algo así.
    return cRes
    


# Función auxiliar recursiva
def _numerals(n, lFemenino=0):

    # Localizar los billones    
    prim,resto = divmod(n,10L**12)
    if prim!=0:
        if prim==1:     cRes = "un billón"
        else:           cRes = _numerals(prim,0)+" billones" # Billones es masculino

        if resto!=0:    cRes += " "+_numerals(resto,lFemenino)

    else:
    # Localizar millones
        prim,resto = divmod(n,10**6)
        if prim!=0:
            if prim==1: cRes = "un millón"
            else:       cRes = _numerals(prim,0)+" millones" # Millones es masculino

            if resto!=0: cRes += " " + _numerals(resto,lFemenino)

        else:
    # Localizar los miles
            prim,resto = divmod(n,10**3)
            if prim!=0:
                if prim==1: cRes="mil"
                else:       cRes=_numerals(prim,lFemenino)+" mil"

                if resto!=0: cRes += " " + _numerals(resto,lFemenino)

            else:
    # Localizar los cientos
                prim,resto=divmod(n,100)
                if prim!=0:
                    if prim==1:
                        if resto==0:        cRes="cien"
                        else:               cRes="ciento"
                    else:
                        cRes=_n3[prim-1]
                        if lFemenino:       cRes+="ientas"
                        else:               cRes+="ientos"

                    if resto!=0:  cRes+=" "+_numerals(resto,lFemenino)

                else:
    # Localizar las decenas
                    if lFemenino and n==1:              cRes="una"
                    elif n<=20:                         cRes=_n1[n-1]
                    else:
                        prim,resto=divmod(n,10)
                        cRes=_n2[prim-1]
                        if resto!=0:
                            if prim==2:                 cRes+=_n11[resto-1]
                            else:                       cRes+=" y "+_n1[resto-1]

                            if lFemenino and resto==1:  cRes+="a"
    return cRes

# Crear una demo interactiva
if __name__=="__main__":
    #res = raw_input("¿En masculino o femenino? ([M]/F) ")
    #lFemenino= res != "" and res in "Ff"
    #print lFemenino
    #num=raw_input("Dame un número: ")
    #print numerals(num,lFemenino)
    print numerals(110.00, moneda = "euros", fraccion = "céntimos")
    print numerals(110.00, moneda = "euros", fraccion = "céntimos", autoomitir = False)
    print numerals(110.00, moneda = "euros", fraccion = "céntimos", autoomitir = True)
    print numerals(110.11, moneda = "euros", fraccion = "céntimos")
    print numerals(110.11, moneda = "euros", fraccion = "céntimos", autoomitir = False)
    print numerals(110.11, moneda = "euros", fraccion = "céntimos", autoomitir = True)

