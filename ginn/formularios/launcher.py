#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008 Francisco José Rodríguez Bogado,                    #
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

'''
Created on 22/05/2013

@author: bogado
'''

def run(modulo, clase, usuario):
    """
    Esto va a recibir cuatro parámetros:
    * fichero
    * clase a instanciar
    * usuario
    Con eso iniciará un proceso donde la ventana está instanciada (y por 
    tanto entra en ejecución).
    El parse_params de configuracion.py se encarga de establecer los modos 
    verbose, debug y la configuración de acceso a la BD; y nos devuelve el 
    usuario y contraseña a autenticar (si falta alguno de ellos, se 
    pregunta mediante el autenticacion.py).
    Una vez pasado hecho login, se crea el proceso y se inicia el bucle GTK de 
    la ventana en cuestión.
    """
    exec "import %s" % modulo
    v = eval('%s.%s' % (modulo, clase))
    v(usuario = usuario)
    

def main():
    """
    Trata los argumentos y llama al método run, que es el que realmente 
    hace todo el trabajo.
    """
    import sys
    from framework.configuracion import parse_params
    from formularios.autenticacion import Autenticacion
    usuario, contrasenna, modulo, clase = parse_params()
    login = Autenticacion(usuario, contrasenna)
    if login.loginvalido():
        run(modulo, clase, usuario)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
