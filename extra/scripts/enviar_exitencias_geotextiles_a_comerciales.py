#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2013  Francisco José Rodríguez Bogado,                   #
#                          <pacoqueen@users.sourceforge.net>                  #
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

import os, sys
base_ginn = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', "..", "ginn"))
sys.path.insert(0, base_ginn)
from framework import pclases
from formularios.consulta_existenciasRollos import ConsultaExistenciasRollos
from formularios.utils import enviar_correoe

#pclases.DEBUG = True

def main():
    consulta = ConsultaExistenciasRollos(gui = False)
    adjuntos = consulta.fich_generados
    admin = pclases.Usuario.select(orderBy = "id")[0] 
        # FIXME: Debe ser una cuenta "neutra". Lo más cercano que se me ocurre 
        # es cogerme a mí mismo que soy administrador. Pero obliga a que haya 
        # sido el primer usuario creado en el sistema. O bien coger alguien de 
        # almacén o algo... 
    if pclases.DEBUG:
        # OJO: HARCODED
        dests = ["informatica@geotexan.com"]
    else:
        # OJO: HARCODED. Cuando monte las zonas se podrá hacer mejor.
        dests = [comercial.correoe for comercial in pclases.Comercial.select() 
                 if comercial.correoe 
                    and ("delegado" in comercial.cargo.lower()
                         or "director comercial" in comercial.cargo.lower())]
    servidor = admin.smtpserver
    smtpuser = admin.smtpuser
    smtppass = admin.smtppassword
    rte = admin.email
    texto = "Se le adjuntan las existencias actuales de geotextiles según "\
            "la fecha y hora de generación de este correo."
    ok = enviar_correoe(rte, 
                       dests,
                       "Existencias geotextiles",  
                       texto, 
                       servidor = servidor, 
                       usuario = smtpuser, 
                       password = smtppass, 
                       adjuntos = adjuntos)
    if ok:
        return 0
    else:
        return 1


if __name__ == "__main__":
    main()

