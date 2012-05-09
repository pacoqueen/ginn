#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"Parsea" (pero que muy entre comillas) el archivo dump indicado y la 
estructura de tablas.sql para construir en memoria una lista con el orden 
en que se deben restaurar los datos de las tablas y los datos en sí. Vuelca 
el resultado en salida estándar de forma que sea totalmente compatible e 
idéntica (en cuanto a contenido) al dump en texto plano del que parte.
"""

import sys, re

def usage():
    sys.stderr.write("Uso: %s tablas.sql dump_datos.sql\n" % sys.argv[0])
    sys.exit(1)

def parse_datos(fd):
    """
    Devuelve una tupla con tres elementos:
    cabecera (todas las líenas del fichero antes de empezar los datos: 
              secuencias, permiso, usuario, etc.).
    datos (un diccionario con el nombre de las tablas como clave y las líneas 
           de inserción de datos -COPY- como valores).
    pie (resto de líneas una vez acaban las líneas de datos).
    """
    cabecera = ""
    datos = {}
    pie = ""
    #print "Grñai mama"
    while 1:
        marca = fd.tell()
        l = fd.readline()
        #print l; sys.stdout.flush()
        if "-- Data " not in l:
            cabecera += l
        else:
            fd.seek(marca)
            break
    # raw_input("Keith Richards ¡que se te va la olla a Camboya!")
    #print "Grñai que te cojo"
    seguir = True
    while seguir:
        datatemp = l
        nombretabla = None
        l = fd.readline()
        # print l; sys.stdout.flush()
        while not l.startswith("\."):
            datatemp += l
            if "Name:" in l:
                palabras = l.split()
                # print palabras
                nombretabla = palabras[palabras.index("Name:")+1].replace(";", "")
            l = fd.readline()
            # print " ->", l; sys.stdout.flush()
        # raw_input("¡Keith Richards no seas loco!")
        while not l.startswith("--"):   
            # El resto de líneas y saltos de línea hasta el siguiente token.
            datatemp += l
            l = fd.readline()
            #print l; sys.stdout.flush()
        datos[nombretabla] = datatemp
        # Aquí necesito un pequeño "lookahead" (si me viera la TurboTere 
        # maltratar así su asignatura de compiladores). Miro un par de 
        # líneas -6 en realidad- buscando un "COPY". Si no lo encuentro, 
        # no quedan más tablas y lo demás puede ir a la sección "pie".
        # Primero marco la posición por donde voy:
        marca = fd.tell()
        # Busco
        seguir = False
        for i in range(6):
            seguir = seguir or fd.readline().strip().startswith("COPY")
        # Vuelvo a la posición de la marca
        fd.seek(marca)
        # Y determino si seguir con mi bucle de tablas o no.
    #raw_input("Keith Richards ¡di STOP!")
    while 1:
        l = fd.readline()
        #print l; sys.stdout.flush()
        if l == "":
            break
        pie += l
    return (cabecera, datos, pie) 

def vuerca_vuerca(c, t, d, p):
    """
    Escribe en salida estándar el fichero de volcado recompuesto.
    """
    print c
    for nombretabla in t:
        try:
            print d[nombretabla]
        except KeyError:
            print " -- Tabla nueva %s ignorada." % nombretabla
    print p

def parse_tablas(ft):
    """
    Lee el fichero de tablas y devuelve una lista con el nombre 
    de las tablas en el mismo orden en el que están en el fichero.
    """
    tablas = []
    rex = re.compile("CREATE TABLE [\w]+[^ \(\.]")
    for l in ft.readlines():
        if not l.strip().startswith("--"):
            resparse = rex.findall(l)
            if resparse != []:
                tablas.append(resparse[0].split()[-1])
    return tablas

def main():
    if len(sys.argv) != 3:
        usage()
    else:
        try:
            ftablas = open(sys.argv[1])
        except IOError:
            usage()
        try:
            fdatos = open(sys.argv[2])
        except IOError:
            usage()
        tablas = parse_tablas(ftablas)
        ftablas.close()
        cabecera, datos, pie = parse_datos(fdatos)
        fdatos.close()
        vuerca_vuerca(cabecera, tablas, datos, pie)

if __name__ == "__main__":
    main()

