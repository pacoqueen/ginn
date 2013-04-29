#!/usr/bin/env python
# -*- coding: utf-8 -*-

#################################################################
# 31 de julio de 2006.
# Script para crear las categorías laborales, centros de trabajo,
# motivos de ausencia, grupos de trabajo y turnos.
# 
#################################################################
import sys, os
from framework import pclases
import mx.DateTime

lineafibra = pclases.LineaDeProduccion.select(pclases.LineaDeProduccion.q.nombre.contains('ibra'))[0]
lineagtx = pclases.LineaDeProduccion.select(pclases.LineaDeProduccion.q.nombre.contains('eotextil'))[0]

pclases.CategoriaLaboral(codigo = 'JLF', puesto = 'Jefe de línea de fibra', lineaDeProduccion = lineafibra, planta = True, precioPlusMantenimientoSabados = 0)
pclases.CategoriaLaboral(codigo = 'OPF', puesto = 'Oficial de producción fibra', lineaDeProduccion = lineafibra, planta = True, precioPlusMantenimientoSabados = 0, precioPlusJefeTurno = 0)
pclases.CategoriaLaboral(codigo = 'JLG', puesto = 'Jefe de línea de geotextiles', lineaDeProduccion = lineafibra, planta = True, precioPlusTurnicidad = 0)
pclases.CategoriaLaboral(codigo = 'OPG', puesto = 'Oficial de producción geotextiles', lineaDeProduccion = lineafibra, planta = True, precioPlusTurnicidad = 0, precioPlusJefeTurno = 0)
pclases.CategoriaLaboral(codigo = 'OPA', puesto = 'Oficial de producción almacén', lineaDeProduccion = None, planta = True, precioPlusTurnicidad = 0, precioPlusJefeTurno = 0, precioPlusMantenimientoSabados = 0)
pclases.CategoriaLaboral(codigo = 'LMP', puesto = 'Limpiadora', lineaDeProduccion = None, planta = True, precioPlusTurnicidad = 0, precioPlusJefeTurno = 0, precioPlusMantenimientoSabados = 0)
pclases.CategoriaLaboral(codigo = 'OAD', puesto = 'Oficial administración', lineaDeProduccion = None, planta = True, precioPlusTurnicidad = 0, precioPlusJefeTurno = 0, precioPlusMantenimientoSabados = 0)
pclases.CategoriaLaboral(codigo = 'LAB', puesto = 'Laboratorio', lineaDeProduccion = None, planta = True, precioPlusTurnicidad = 0, precioPlusJefeTurno = 0, precioPlusMantenimientoSabados = 0)
pclases.CategoriaLaboral(codigo = 'EAL', puesto = 'Encargado almacén', lineaDeProduccion = None, planta = True, precioPlusTurnicidad = 0, precioPlusJefeTurno = 0, precioPlusMantenimientoSabados = 0)
pclases.CategoriaLaboral(codigo = 'DCM', puesto = 'Director comercial', lineaDeProduccion = None, planta = True, precioPlusTurnicidad = 0, precioPlusJefeTurno = 0, precioPlusMantenimientoSabados = 0)
pclases.CategoriaLaboral(codigo = 'DTC', puesto = 'Director técnico', lineaDeProduccion = None, planta = True, precioPlusTurnicidad = 0, precioPlusJefeTurno = 0, precioPlusMantenimientoSabados = 0)
pclases.CategoriaLaboral(codigo = 'DGR', puesto = 'Director gerente', lineaDeProduccion = None, planta = True, precioPlusTurnicidad = 0, precioPlusJefeTurno = 0, precioPlusMantenimientoSabados = 0)

pclases.CentroTrabajo(nombre = "Fibras")
pclases.CentroTrabajo(nombre = "Geotextiles")
#pclases.CentroTrabajo(nombre = "Geocompuestos")
pclases.CentroTrabajo(nombre = "Comercializados") # CWT: Cambiado el 27/09/2010
pclases.CentroTrabajo(nombre = "Almacén")
pclases.CentroTrabajo(nombre = "Laboratorio")
pclases.CentroTrabajo(nombre = "Oficinas")
pclases.CentroTrabajo(nombre = "Varios")

pclases.Grupo(nombre = 'Grupo A', jefeturnoID = None, operario1ID = None, operario2 = None, observaciones = "Línea de fibra.\nIntroducir jefe de turno y operarios.")
pclases.Grupo(nombre = 'Grupo B', jefeturnoID = None, operario1ID = None, operario2 = None, observaciones = "Línea de fibra.\nIntroducir jefe de turno y operarios.")
pclases.Grupo(nombre = 'Grupo C', jefeturnoID = None, operario1ID = None, operario2 = None, observaciones = "Línea de fibra.\nIntroducir jefe de turno y operarios.")
pclases.Grupo(nombre = 'Grupo D', jefeturnoID = None, operario1ID = None, operario2 = None, observaciones = "Línea de fibra.\nIntroducir jefe de turno y operarios.")
pclases.Grupo(nombre = 'Grupo E', jefeturnoID = None, operario1ID = None, operario2 = None, observaciones = "Línea de fibra.\nIntroducir jefe de turno y operarios.")
#pclases.Grupo(nombre = 'Grupo F', jefeturnoID = None, operario1ID = None, operario2 = None, observaciones = "Línea de geocompuestos.\nIntroducir jefe de turno, operarios y crear resto de grupos de la línea.")
pclases.Grupo(nombre = 'Grupo F', jefeturnoID = None, operario1ID = None, operario2 = None, observaciones = "Línea de comercializados.\nIntroducir jefe de turno, operarios y crear resto de grupos de la línea.") # CWT: Cambiado el 27/09/2010

pclases.Motivo(descripcion = "Nacimiento hijo", descripcionDias = "(2 días remunerados)", retribuido = 2, sinRetribuir = 0, excedenciaMaxima = 2, convenio = False)
pclases.Motivo(descripcion = "Nacimiento hijo con desplazamiento", descripcionDias = "(4 días remunerados)", retribuido = 4, sinRetribuir = 0, excedenciaMaxima = 4, convenio = False)
pclases.Motivo(descripcion = "Fallecimiento familiar Clase 1", descripcionDias = "(3 días remunerados)", retribuido = 3, sinRetribuir = 0, excedenciaMaxima = 3, convenio = False)
pclases.Motivo(descripcion = "Fallecimiento familiar Clase 1 con desplazamiento", descripcionDias = "(4 días remunerados + 1 sin remunerar)", retribuido = 4, sinRetribuir = 1, excedenciaMaxima = 5, convenio = False)
pclases.Motivo(descripcion = "Fallecimiento familiar Clase 2", descripcionDias = "(2 días remunerados)", retribuido = 2, sinRetribuir = 0, excedenciaMaxima = 2, convenio = False)
pclases.Motivo(descripcion = "Fallecimiento familiar Clase 2 con desplazamiento", descripcionDias = "(4 días remunerados)", retribuido = 4, sinRetribuir = 0, excedenciaMaxima = 4, convenio = False)
pclases.Motivo(descripcion = "Fallecimiento familiar Clase 3", descripcionDias = "(1 día remunerado)", retribuido = 1, sinRetribuir = 0, excedenciaMaxima = 1, convenio = False)
pclases.Motivo(descripcion = "Fallecimiento familiar Clase 4", descripcionDias = "(1 día remunerado)", retribuido = 1, sinRetribuir = 0, excedenciaMaxima = 1, convenio = False)
pclases.Motivo(descripcion = "Consulta médica", descripcionDias = "(1 día remunerado)", retribuido = 1, sinRetribuir = 0, excedenciaMaxima = 1, convenio = False)
pclases.Motivo(descripcion = "Accidente o enfermedad graves u hospitalización familiares Clases 1 y 2", descripcionDias = "(2 días remunerados)", retribuido = 2, sinRetribuir = 0, excedenciaMaxima = 2, convenio = False)
pclases.Motivo(descripcion = "Accidente o enfermedad graves u hospitalización familiares Clases 1 y 2 con desplazamiento", descripcionDias = "(4 días remunerados)", retribuido = 4, sinRetribuir = 0, excedenciaMaxima = 4, convenio = False)
pclases.Motivo(descripcion = "Intervención quirúrgica o lesión con fractura familiares Clases 1", descripcionDias = "(1 día remunerado)", retribuido = 1, sinRetribuir = 0, excedenciaMaxima = 1, convenio = False)
pclases.Motivo(descripcion = "Matrimonio", descripcionDias = "(15 días remunerados)", retribuido = 15, sinRetribuir = 0, excedenciaMaxima = 15, convenio = False)
pclases.Motivo(descripcion = "Traslado domicilio habitual", descripcionDias = "(1 día remunerado)", retribuido = 1, sinRetribuir = 0, excedenciaMaxima = 1, convenio = False)
pclases.Motivo(descripcion = "Boda de un hijo", descripcionDias = "(1 día remunerado)", retribuido = 1, sinRetribuir = 0, excedenciaMaxima = 1, convenio = False)
pclases.Motivo(descripcion = "Boda de un hermano", descripcionDias = "(1 día sin remunerar)", retribuido = 0, sinRetribuir = 1, excedenciaMaxima = 1, convenio = False)
pclases.Motivo(descripcion = "Cumplimiento de un deber inexcusable de carácter público", descripcionDias = "(Según proceda)", retribuido = 0, sinRetribuir = 0, excedenciaMaxima = 0, convenio = False)
pclases.Motivo(descripcion = "Trámites de adopción o acogimiento", descripcionDias = "(15 días sin remunerar)", retribuido = 0, sinRetribuir = 15, excedenciaMaxima = 15, convenio = False)
pclases.Motivo(descripcion = "Trámites de adopción o acogimiento internacional", descripcionDias = "(Excedencia voluntaria de máx. 2 meses)", retribuido = 0, sinRetribuir = 0, excedenciaMaxima = 30, convenio = False)
pclases.Motivo(descripcion = "Asuntos propios", descripcionDias = "(2 días remunerados al año)", retribuido = 2, sinRetribuir = 0, excedenciaMaxima = 2, convenio = True)

pclases.Turno(nombre = "Mañana", horainicio = mx.DateTime.DateTimeFrom('06:00'), horafin = mx.DateTime.DateTimeFrom('14:00'), noche = False, recuperacion = False)
pclases.Turno(nombre = "Tarde", horainicio = mx.DateTime.DateTimeFrom('14:00'), horafin = mx.DateTime.DateTimeFrom('22:00'), noche = False, recuperacion = False)
pclases.Turno(nombre = "Noche", horainicio = mx.DateTime.DateTimeFrom('22:00'), horafin = mx.DateTime.DateTimeFrom('06:00'), noche = True, recuperacion = False)
pclases.Turno(nombre = "Recuperación", horainicio = mx.DateTime.DateTimeFrom('00:00'), horafin = mx.DateTime.DateTimeFrom('23:59:59.59'), noche = False, recuperacion = True)

