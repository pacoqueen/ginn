#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Acceso a la dll ActiveX lcOEM.dll de Murano para lanzar procesos desde fuera como el de importación
# (Con la versión Win32, no amd64. Al cabo de varios intentos, al final parece que inicializa)

from __future__ import print_function
import win32com.client
murano = win32com.client.Dispatch("LogicControlOEM.OEM_EjecutaOEM")
try:
    murano.InicializaOEM(9999, "OEM", "oem", "", "LOGONSERVER\\MURANO", "GEOTEXAN")
except Exception, e:
    print(e)
murano.InicializaOEM(9999, "OEM", "oem", "", "LOGONSERVER", "GEOTEXAN")
murano.EjecutaOperacion("ENT_LisMunicipios")
