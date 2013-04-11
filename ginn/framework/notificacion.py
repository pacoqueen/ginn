#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


###################################################################
## notificacion.py
##  
##  Notificador de cambios remotos.
###################################################################
## NOTAS:
## 
## ----------------------------------------------------------------
## 
###################################################################
## Changelog:
##  14 de diciembre de 2005 -> Fork del notificador. Lo saco de 
##                             utils.py para hacer una clase 
##                             independiente.
##  3 de enero de 2005 -> Ahora el notificador también se encarga
##                        de controlar el hilo de persistencia del
##                        objeto relacionado.
###################################################################

#-------------------------- CLASE NOTIFICACIÓN ------------------------------
## La idea es:
## Tener una clase notificación, que sea un wrapper para una función de 
## actualización, que será la que se dispare cuando se produzca una 
## notificación en un objeto persistente.
## Mediante set_ y run_, cuando se produzca una notificación en uno de 
## mis objetos de pclases, se ejecutará (run_) la función que desde el 
## formulario (en la inicialización de la ventana) se ha definido (set_).
## DONE: Estaría bien implementar un singleton para asegurarme que sólo hay un
## notificador activo en la interfaz (que se correspondería con el objeto
## mostrado en ese momento). -> No se puede hacer. Hay ventanas multiobjeto 
## que necesitan un notificador por cada objeto en ventana. Ver por ejemplo 
## «productos_especiales.py»

class Notificacion:
  #DONE: No está bonito llamar a las clases con minúsculas. Eso no está bonito.
  def __init__(self, obj):
    """
    obj es el objeto al que se asocia el notificador.
    """
    self.__func = lambda : None
    self.observador = obj

  def set_func(self, f):
    self.__func = f
    ## self.observador.ejecutar_hilo()
  
  def activar(self, f):
    self.set_func(f)
    # print " --- Notificación activada ---"
  
  def desactivar(self):
    ## self.observador.parar_hilo()
    self.__func = lambda : None
    # print " --- Notificación desactivada ---"
    
  def run(self, *args, **kwargs):
    # print "EJECUTO", self.__func
    try:
        self.__func(*args, **kwargs)
    except (AttributeError, KeyError), msg:
        pass    # La ventana se ha cerrado y el objeto sigue en memoria. No 
                # tiene importancia.
        #print "notificacion::run -> Ventana cerrada. Ignorando notificación"
        #      ". Mensaje de la excepción: %s" % (msg)

#---------------------- EOC NOTIFICACIÓN ------------------------------------

