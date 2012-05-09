#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Inicializa la base de datos de la copia de seguridad tomando los parámetros 
del archivo de configuración indicado en el segundo parámetro.
"""

import os, sys

def usage():
    print "%s dump_datos.sql[.tar.bz2] ../framework/ginn.conf(.xxxx)" % sys.argv[0]

def descomprimir_si_no_lo_esta(nomfichbak):
    if nomfichbak.endswith(".bz2"):
        params = "mxvjf"
        descomprimir = True 
    elif nomfichbak.endswith(".gz"):
        params = "mxvzf"
        descomprimir = True 
    else:
        nomfichbak = nomfichbak
        descomprimir = False
    if descomprimir:
        os.system("tar %s %s" % (params, nomfichbak))
        os.system("ls *.sql -tr > /tmp/lstr")
        nomfichbak = open("/tmp/lstr").readlines()[-1].replace("\n", "")
    return nomfichbak

def parse_conf(nomfichconf):
    f = open(nomfichconf)
    d = {}
    for l in f.readlines():
        if not l.strip(): continue
        try:
            clave, valor = "_".join(l.split()[:-1]).strip(), l.split()[-1]
        except:
            print l
            raise 
        d[clave] = valor.strip()
    return d['user'], d['pass'], d['dbname']

def main():
    if 2 <= len(sys.argv) <= 3:
        try:
            nomfichbak, nomfichconf = sys.argv[1:]
        except (TypeError, ValueError):
            nomfichbak, nomfichconf = sys.argv[1], "../framework/ginn.conf"
        nomfichbak = descomprimir_si_no_lo_esta(nomfichbak)
        usu, contra, nombd = parse_conf(nomfichconf)
        cmd = "./init_db.sh %(nombre_bd)s %(usuario)s %(contraseña)s %(fichero)s" % {'nombre_bd': nombd, 'usuario': usu, 'contraseña': contra, 'fichero': nomfichbak}
        os.system(cmd)
    else:
        usage()

if __name__ == "__main__":
    main()

