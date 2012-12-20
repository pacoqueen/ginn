#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
sys.path.insert(0, (os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                    "..", "framework")))

import pclases

fventanas = (("consulta_cartera.py", 
                "Consultar efectos en cartera", 
                "ConsultaCartera", 
                "informes.png"), 
             ("bancos.py", 
                 "Fichas de banco", 
                 "Bancos", 
                 "money.png"), 
             ("remesas.py", 
                 "Remesas de efectos de cobro", 
                 "Remesas", 
                 "isoldi.png"), 
            )

try:
    tesoreria = pclases.Modulo.selectBy(nombre = "Tesorería")[0]
except IndexError:
    tesoreria = pclases.Modulo(nombre = "Tesorería", icono = "tesoreria.png", 
            descripcion = "Módulo de tesorería y análisis financiero")
ventanas = []
for fventana, descripcion, clase, icono in fventanas:
    try:
        ventanas.append(pclases.Ventana.selectBy(fichero = nomventana)[0])
    except IndexError:
        ventanas.append(pclases.Ventana(modulo = tesoreria, 
                                        descripcion = descripcion, 
                                        fichero = fventana, 
                                        clase = clase, 
                                        icono = icono))

for nomuser in ("administrador", "javier", "kiko", "nicolas"):
    u = pclases.Usuario.selectBy(usuario = nomuser)
    for v in ventanas:
        permiso = u.get_permiso(v)
        try:
            permiso.permiso = permiso.lectura = permiso.escritura \
                    = permiso.nuevo = True
        except AttributeError:
            pclases.Permiso(ventana = v, 
                            usuario = u, 
                            permiso = True, 
                            lectura = True, 
                            escritura = True, 
                            nuevo = True)

