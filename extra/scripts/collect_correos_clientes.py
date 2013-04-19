#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Crea un CSV con las direcciones de correo de clientes y contactos y otro de proveedores.
"""

import re
import csv
from framework import pclases

regexp = re.compile(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}', re.IGNORECASE)


csv_clientes = csv.writer(open("clientes_gtx.csv", "wb"), delimiter = ";")
csv_proveedores = csv.writer(open("proveedores_gtx.csv", "wb"), delimiter = ";")

clientes = []
for c in pclases.Cliente.select():
    nombre = c.nombre
    apellidos = ""
    for email in regexp.findall(c.email):
        cliente = [email.lower(), nombre, apellidos]
        if cliente not in clientes:
            clientes.append(cliente)
    for email in regexp.findall(c.contacto):
        cliente = [email.lower(), c.contacto.replace(email.lower(), ""), ""]
        if cliente not in clientes:
            clientes.append(cliente)
    for obra in c.obras:
        for contacto in obra.contactos:
            for email in regexp.findall(contacto.correoe):
                cliente = [email.lower(), contacto.nombre, contacto.apellidos]
                if cliente not in clientes:
                    clientes.append(cliente)
for c in clientes:
    csv_clientes.writerow(c)

proveedores = []
for p in pclases.Cliente.select():
    nombre = p.nombre
    apellidos = ""
    for email in regexp.findall(p.email):
        proveedor = [email.lower(), nombre, apellidos]
        if proveedor not in proveedores:
            proveedores.append(proveedor)
    for email in regexp.findall(p.contacto):
        proveedor = [email.lower(), p.contacto.replace(email.lower(), ""), ""]
        if proveedor not in proveedores:
            proveedores.append(proveedor)
for p in proveedores:
    csv_proveedores.writerow(p)

