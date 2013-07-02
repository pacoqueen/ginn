#!/usr/bin/env python2.3
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado,                         #
#                                  Diego Muñoz Escalante.                                      #
# (pacoqueen@users.sourceforge.net, escalant3@users.sourceforge.net)             #
#                                                                                                      #
# This file is part of GeotexInn.                                                            #
#                                                                                                      #
# GeotexInn is free software; you can redistribute it and/or modify              #
# it under the terms of the GNU General Public License as published by          #
# the Free Software Foundation; either version 2 of the License, or              #
# (at your option) any later version.                                                      #
#                                                                                                      #
# GeotexInn is distributed in the hope that it will be useful,                     #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                  #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                    #
# GNU General Public License for more details.                                          #
#                                                                                                      #
# You should have received a copy of the GNU General Public License              #
# along with GeotexInn; if not, write to the Free Software                          #
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA  #
###############################################################################


"""
nftp.py - A Simple FTP Command Line Utility

Help: ./nftp.py --help
Author: Sean B. Palmer, inamidst.com
License: GNU GPL 2
Date: 2003-11

http://inamidst.com/proj/nftp/

Modificado por Franciso José Rodríguez Bogado para
adaptarlo a Geotex-Inn.
Se usará nftp ginn --get archivo.pyw
Debe existir un archivo ../framework/nftp.conf con 
una entrada para la configuración ginn.
"""

import sys, os, re, ftplib
from optparse import OptionParser

##config = os.path.expanduser('~/.nftprc')
config = ('../framework/nftp.conf')
r_field = re.compile(r'(?s)([^\n:]+): (.*?)(?=\n[^ \t]|\Z)')

def getConfig(name=None): 
    # Find the config file
    home = os.path.expanduser('~/')
    nftp_conf = os.getenv('NFTP_CONF')
    if nftp_conf is not None: 
        s = open(nftp_conf).read()
    elif os.path.exists(config): 
        s = open(config).read()
    elif os.path.exists('.nftprc'): 
        s = open('.nftprc').read()
    elif os.path.exists('nftp.conf'): 
        s = open('nftp.conf').read()
    elif os.path.exists(home + 'nftp.conf'): 
        s = open(home + 'nftp.conf').read()
    elif os.path.exists(os.path.join('..', 'framework', 'nftp.conf')):
        s = open(os.path.join('..', 'framework', 'nftp.conf'))
    else: return {}

    # Parse the config file
    conf = {}
    s = s.replace('\r', '\n')
    for item in s.split('\n'): 
        meta = dict([(j[0].strip(), j[1].strip()) for j in r_field.findall(item)])
        if meta.has_key('name'): 
            fname = meta['name']
            del meta['name']
            conf[fname] = meta
        else: raise 'ConfigError', 'Debe incluir un nombre'

    if name is not None: 
        return conf[name]
    else: 
        return conf['ginn']    #Debe haber al menos una configuración por defecto llamada 'ginn'

def pathSplit(filepath): 
    if filepath.startswith('/'): 
        filepath = filepath[1:]

    if '/' not in filepath: 
        return '', filepath

    parts = filepath.split('/')
    filename = parts.pop()
    return '/'.join(parts), filename    

def getFtp(meta): 
    ftp = ftplib.FTP(meta['host'], meta['username'], meta['password'])
    ftp.cwd(meta['remotedir'])
    return ftp

def chmod(name, filepath, code): 
    meta = getConfig(name)

    ftp = getFtp(meta)
    path, fn = os.path.split(filepath)
    path = path.lstrip('/')
    ftp.cwd(path)

    print >> sys.stderr, 'Haciendo CHMOD -%s en %s...' % (code, fn)
    result = ftp.sendcmd('SITE CHMOD %s %s' % (code, fn))
    print >> sys.stderr, 'Resultado: %s' % result

def upload(name, filepath): 
    meta = getConfig(name)

    ftp = getFtp(meta)
    path, fn = os.path.split(filepath)
    path = path.lstrip('/') or '.'
    try: ftp.cwd(path)
    except ftplib.error_perm, e: 
        print >> sys.stderr, 'Error: "%s"' % e
        if raw_input("Crear directorio /%s? [s/n]: " % path).startswith('s'): 
            for folder in path.split('/'): 
                try: ftp.cwd(folder)
                except: 
                    ftp.mkd(folder)
                    ftp.cwd(folder)
        else: sys.exit(1)

    f = open(os.path.join(meta['localdir'], path+'/'+fn), 'rb')
    print >> sys.stderr, 'Guardando %s...' % filepath
    result = ftp.storbinary('STOR %s' % fn, f)
    print >> sys.stderr, 'Resultado: %s' % result
    f.close()

def descargar_archivo(archivo, md5 = False):
    """
    Recibe un archivo concreto que debe ser descargado
    al directorio de trabajo.
    Por defecto descarga el archivo del directorio de 
    formularios (enlazado a través de "ginn"). Si 
    md5 es True descarga el archivo desde el directorio
    ginn/md5. NO AÑADE LA EXTENSIÓN .md5, el nombre del 
    archivo debe ser correcto.
    """
    # OJO: Todo esto está HARCODED. Hay que hacer un archivo de configuración de donde coger los datos y tal.
#    meta = {'host':'192.168.1.33', 'username':'geotexan', 'password':'', 'localdir':'.', 'remotedir':'ginn'}
#    meta = {'host' : '192.168.1.100', 'username':'geotexan', 'password':'', 'localdir':'.', 'remotedir':'ginn'}
    meta = getConfig() 

    ftp = getFtp(meta)
    path, fn = os.path.split(archivo)
    path = path.lstrip('/')
    if md5:
        ftp.cwd('md5')

    if not md5:
        filename = os.path.join(meta['localdir'], fn)
    else:
        filename = os.path.join(meta['localdir'], 'md5', fn)
    if not os.path.exists(os.path.join(meta['localdir'], 'md5')):
        os.mkdir(os.path.join(meta['localdir'], 'md5'))
    f = open(filename, 'wb')
    print >> sys.stderr, 'Obteniendo %s...' % archivo 
    ftp.retrbinary("RETR %s" % fn, f.write)
    print >> sys.stderr, 'Descarga correcta'
    f.close()

def get(name, filepath): 
    meta = getConfig(name)

    ftp = getFtp(meta)
    path, fn = os.path.split(filepath)
    path = path.lstrip('/')
    ftp.cwd(path)

    retrieve = False
#    filename = os.path.join(meta['localdir'], path + '/' + fn)
    filename = os.path.join(meta['localdir'], fn)
    if os.path.exists(filename): 
        retrieve = raw_input('Sobreescribir %s? [s/n]: ' % fn).startswith('s')
    else: retrieve = True

    if retrieve: 
        f = open(filename, 'wb')
        print >> sys.stderr, 'Obteniendo %s...' % filepath
        ftp.retrbinary("RETR %s" % fn, f.write)
        print >> sys.stderr, 'Descarga correcta'
        f.close()
    else: print >> sys.stderr, "No se puede descargar %s" % fn

def delete(name, filepath): 
    meta = getConfig(name)

    ftp = getFtp(meta)
    path, fn = os.path.split(filepath)
    path = path.lstrip('/')
    ftp.cwd(path)

    if raw_input('¿Borrar %s? [s/n]: ' % fn).startswith('s'): 
        print >> sys.stderr, 'Borrando %s...' % fn
        try: result = ftp.delete(fn)
        except ftplib.error_perm, e: 
            msg = 'Se tiene "%s", ¿intentar borrar como directorio? [s/n]: ' % e
            if raw_input(msg).startswith('s'): 
                try: result = ftp.rmd(fn)
                except ftplib.error_perm, e: 
                    print >> sys.stderr, 'Error:', e
                    sys.exit(1)
        print >> sys.stderr, 'Resultado: %s' % result
    else: print >> sys.stderr, "No se eliminó %s" % fn

# upload, -c chmod, -d delete, -u update, -g get

def main(argv=None): 
    ##parser = OptionParser(usage='%prog [options] <name> <path>')
    parser = OptionParser(usage='%prog <name> [options]')
    parser.add_option("-c", "--chmod", dest="chmod", default=False, 
                            help="chmod a file on the server")
    parser.add_option("-u", "--update", dest="update", 
                            action="store_true", default=False, 
                            help="update a file, on the server or locally")
    parser.add_option("-g", "--get", dest="get", 
                            action="store_true", default=False, 
                            help="download a file from the server")
    parser.add_option("-d", "--delete", dest="delete", 
                            action="store_true", default=False, 
                            help="delete a file from the server")

    options, args = parser.parse_args(argv)

    if (len(args) < 1) or (len(args) > 2): 
        parser.error("Número incorrecto de argumentos")
    elif len(args) == 1: 
        print >> sys.stderr, 'Intentando (Guessing) cuenta y ruta...'
        found, cwd, fn = False, os.getcwd(), args[0]
        for (account, info) in getConfig().items(): 
            if cwd.startswith(info['localdir']): 
                path = cwd[len(info['localdir']):]
                filepath = path + '/' + fn
                print >> sys.stderr, 'Encontrado "%s %s"' % (account, filepath)
                name, found = account, True
        if not found: 
            print >> sys.stderr, "¡No se pudo encontrar la cuenta!"
            sys.exit(1)
    else: name, filepath = args

    if options.update: 
        raise "NotImplemented", "¡Implementar @@!"
    elif options.chmod: 
        chmod(name, filepath, options.chmod)
    elif options.get: 
        get(name, filepath)
    elif options.delete: 
        delete(name, filepath)
    else: upload(name, filepath)

if __name__=="__main__": 
    main()

