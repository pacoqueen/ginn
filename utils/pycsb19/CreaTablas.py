#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite
conn = sqlite.connect(db="./dbCsb19/db", mode=077)
cursor = conn.cursor()

cursor.execute("create table presentadores (nif varchar, sufijo varchar, nombre varchar, banco varchar,oficina varchar)")
conn.commit()

cursor.execute("create table ordenantes (nif varchar, sufijo varchar, nombre varchar, banco varchar,oficina varchar, dc varchar, cuenta varchar)")
conn.commit()

cursor.execute("create table clientes (codigo varchar, nif varchar, nombre varchar, direccion varchar, ciudad varchar, cp varchar, banco varchar, oficina varchar, dc varchar, cuenta varchar)")
conn.commit()

cursor.execute("create table remesas (codigo integer, titulo varchar, importe float, generada varchar, presentador varchar, ordenante varchar, fecha date)")
conn.commit()

cursor.execute("create table det_remesas (codigo integer, indice integer, cliente varchar, importe float, conceptos varchar)")
conn.commit()
#cursor.execute("create index IDX_det_remesas on det_remesas (codigo, indice)")
#cursor.execute("create index IDX_remesas on remesas (codigo)")
#cursor.execute("create index IDX_clientes on clientes (codigo)")

conn.close()
