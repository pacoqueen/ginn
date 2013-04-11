#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, mx
try:
    from framework import pclases
except ImportError:
    import sys
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    from framework import pclases
import mx.DateTime

 
def cmpfechahora(detalle1, detalle2):
    if detalle1.fechahora < detalle2.fechahora:
        return -1
    elif detalle1.fechahora > detalle2.fechahora:
        return 1
    else:
        return 0

def horaini(i):
    try:
        return i.horainicio.strftime('%H:%M')
    except:
        return ''

def horafin(i):
    try:
        return i.horafin.strftime('%H:%M')
    except:
        return ''

def duracionhh(i):
    try:
        return (i.horafin - i.horainicio).strftime('%H:%M')
    except:
        return ''
        
def observaciones(d):
    try:
        return d.bala.motivo
    except:     # No es bala. 
        return d.observaciones

def duracion(d):
    return duracionhh(d)

def claseb(d):
    try:
        return d.bala.claseb
    except:
        return False

def calcular_duracion(parte, hfin, hini):
    if isinstance(hfin, mx.DateTime.DateTimeDeltaType):
        hfin = hfin + mx.DateTime.oneDay 
    duracion = hfin - hini
    if duracion.day > 0:
        duracion -= mx.DateTime.oneDay
    if duracion.day > 0:
        print "WARNING: partes_de_fabricacion_balas: calcular_duracion: ID %d: ¿Seguro que dura más de un día completo?", parte.id
    return duracion

def calcular_tiempo_trabajado(parte):
    tiempototal = calcular_duracion(parte.horafin, parte.horainicio)
    paradas = [p for p in parte.incidencias]
    tiempoparadas = 0
    for parada in paradas:
        tiempoparadas += calcular_duracion(parada.horafin, parada.horainicio)
    return tiempototal, tiempototal - tiempoparadas
    
for p in pclases.ParteDeProduccion.select():
    if calcular_duracion(p, p.horainicio, p.horafin) > mx.DateTime.oneDay:
        print "Reparar parte ID %d." % p.id
    else:
        print "Parte ID %d correcto." % p.id
        
        

