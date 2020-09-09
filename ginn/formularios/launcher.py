#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2020 Francisco José Rodríguez Bogado                     #
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

'''
Created on 22/05/2013

@author: bogado
'''

import os
import sys


def guess_interprete():
    """
    Devuelve el intérprete python encontrado en el sistema.
    None si no se pudo determinar.
    Solo útil para SO Windows.
    """
    sysdrive = os.getenv("SYSTEMDRIVE")
    if not sysdrive:
        sysdrive = "C:"
    res = None
    for pyver in ("27", "26", "25"):
        # PLAN: ¿Se podría meter aquí la optimización -OO al intérprete?
        # ¿Serviría de algo o el cuello de botella seguiría siendo el ORM?
        # ¿Y si con eso me cargo la introspección del GtkExceptionHook y me
        # empiezan a llegar bug reports con las líneas y el código equivocado?
        interprete = os.path.join(sysdrive, os.path.sep, "Python" + pyver,
                                  "pythonw.exe")
        if os.path.exists(interprete):
            res = interprete
            break
    return res


def run(modulo, clase, usuario, fconfig, obj_puid=None,
        debug=False, verbose=False):
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
    try:
        # assert sys.platform != "linux2"     # DONE: ¿Por qué ahora no me
        # funca el popen en linux?
        import subprocess
        ruta = os.path.realpath(os.path.join(os.path.dirname(
            os.path.realpath(__file__)), '..'))
        if sys.platform[:3] == "win":
            comando = "set PYTHONPATH=%PYTHONPATH%;" + ruta + " & "
            interprete = guess_interprete()
            if not interprete:
                interprete = ""
        else:
            comando = "export PYTHONPATH=$PYTHONPATH:" + ruta + "; "
            interprete = ""
        comando += interprete
        args = [os.path.join(ruta, "formularios", modulo + ".py")]
        if not isinstance(usuario, str):
            usuario = usuario.usuario   # Debe de ser instancia de pclases
        args += ["-u %s" % usuario, "-c %s" % fconfig]
        if obj_puid:
            args.append(" -o %s" % obj_puid)
        if debug:
            args.append(" -d")
        if verbose:
            args.append(" -v")
        # print(comando, args)
        prcomando = " ".join([comando] + args)
        # print(prcomando)
        subprocess.Popen(prcomando, shell=True)
        # OJO: Si no funciona y Windows dice que
        # "La ruta de acceso no es válida", comprueba antes que nada que el
        # fichero de log de formularios existe y es accesible para escritura
        # para todos los usuarios. Para depurar, lo mejor es que
        # ejecutes el launcher directamente. Sin menú. Tal que así:
        # Q:\ginn\formularios>C:\Python27\python.exe launcher.py -u admin
        # -p ******* -w bancos.py
    except Exception as msg:     # fallback @UnusedVariable
        # TODO: Esto debería ir al logger o algo:
        # print "launcher.py:", msg
        exec("import {}".format(modulo))
        v = eval('{}.{}'.format(modulo, clase))
        if obj_puid:
            if isinstance(obj_puid, str):
                from framework import pclases
                objeto = pclases.getObjetoPUID(obj_puid)
            else:
                objeto = obj_puid
            v(usuario=usuario, objeto=objeto)
        else:
            v(usuario=usuario)


def main():
    """
    Trata los argumentos y llama al método run, que es el que realmente
    hace todo el trabajo.
    """
    import sys
    from framework.configuracion import parse_params
    from formularios.autenticacion import Autenticacion
    # @UnusedVariable
    (usuario, contrasenna, modulo, clase,
     fconfig, verbose, debug, obj_puid) = parse_params()
    login = Autenticacion(usuario, contrasenna)
    if login.loginvalido():
        run(modulo, clase, usuario, fconfig, obj_puid, debug, verbose)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
