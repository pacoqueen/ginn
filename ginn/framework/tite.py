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

## Crea el código de las clases persistentes.
## No soporta relaciones muchos a muchos... de momento.

## Uso: ./tite.py >> pclases.py

def pythonear(p):
    """
    Cambia _x por X. P. ej: linea_de_venta lineaDeVenta.
    """
    while '_' in p:
        i = p.index('_')
        p = p[:i] + p[i+1].upper() + p[i+2:]
    return p    # NO va a haber ningún nombre con _ al final. Así que no va a petar.

def plural(p):
    if '_' in p:
        return plural(p.split('_')[0]) + p[p.index('_'):]
    if p[-1] in "aeiou":
        return p+'s'
    elif p[-1] == 's':
        return p
    else:
        return p+'es'

def pluralpy(p):
    return pythonear(plural(p))

def clasear(t):
    return pythonear(t.capitalize())

skel = open('./skel.py')
tabl = open('../BD/tablas.sql')

relaciones = {}
for l in tabl.readlines():
    #if "CREATE TABLE " in l and not l.startswith('--') and not "_" in l: ## Para evitar las relaciones muchos a muchos, que lo voy a tener que hacer de otra forma
    if "CREATE TABLE " in l and not l.startswith('--'): 
        tabla = ([i for i in l.replace("(", "").replace("\n","").split(" ") if i!='' and i!='CREATE' and i!='TABLE'][0])
        relaciones[tabla] = []
    if "_id" in l and not "CHECK" in l:
        clavajena = l.split()[0]
        try:
            tablajena = clavajena[:clavajena.rindex('_')]
        except ValueError:
            tablajena = clavajena
#        print "Relación con %s a través de %s." % (tablajena, clavajena)
        relaciones[tabla].append(tablajena)  # Siempre se encontrará una tabla antes que una clave ajena.
    # Para mi script sql vale

relaciones_inv = {}
for k in relaciones:
    for v in relaciones[k]:
        if not v in relaciones_inv:
            relaciones_inv[v] = []
        relaciones_inv[v].append(k)

#print relaciones
#print relaciones_inv
        
for tabla in relaciones:
    for l in skel.readlines():
        clase = clasear(tabla)
        l2 = l.replace("@@Clase@@", clase)
        strel = ''
        for tablajena in relaciones[tabla]:
            strel += "    %sID = ForeignKey('%s')\n" % (pythonear(tablajena), clasear(tablajena))
        try:
            for tablajena in relaciones_inv[tabla]:
                strel += "    %s = MultipleJoin('%s')\n" % (pluralpy(tablajena), clasear(tablajena))
        except:
            pass    # No tiene MultipleJoin 
        l2 = l2.replace("@@Relaciones@@", strel)
        print l2,
    skel.seek(0)

skel.close()
tabl.close()
