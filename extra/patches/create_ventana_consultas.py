#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys                                                                  
base_ginn = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', "..", "ginn"))
sys.path.insert(0, base_ginn)
from framework import pclases

try:
    v = pclases.Ventana.selectBy(fichero = "consulta_ofertas.py")[0]
except IndexError:
    v = pclases.Ventana(
            modulo = pclases.Modulo.selectBy(nombre = "Comercial")[0], 
            descripcion = "Consulta de ofertas de pedido", 
            fichero = "consulta_ofertas.py", 
            clase = "ConsultaOfertas", 
            icono = "informe.png")
usuarios = []
for u in pclases.Usuario.selectBy(nivel = 0):
    usuarios.append(u)
for u in pclases.Usuario.selectBy(nivel = 1):
    usuarios.append(u)
try:
    u = pclases.Usuario.selectBy(usuario = "jaguilar")[0]   # FIXME: HARCODED
    usuarios.append(u)
except IndexError:
    pass
for u in usuarios: 
    pclases.Permiso(usuario = u, ventana = v, permiso = True, lectura = True, 
                    escritura = True, nuevo = True)

