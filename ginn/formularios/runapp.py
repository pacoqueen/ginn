#!/usr/bin/env python
#coding=utf-8

# Créditos: Oswaldo Hernández (oswaldo@soft-com.es)

from formularios import subprocess
import threading
import re

# -- clases auxiliares --
class readpipe(threading.Thread):
    """ Thread para lectura del pipe """
    lck = threading.Lock()

    def __init__(self, pipe, callback=None):
        threading.Thread.__init__(self)
        self.pipe = pipe
        self.callback = callback

    def run(self):
        while 1:
            msg = self.pipe.readline()
            if not msg:
                break

            if self.callback:
                # bloquear, ejecutar funcion y desbloquear
                readpipe.lck.acquire()
                self.callback(msg)
                readpipe.lck.release()


def runapp(app, cbkStdOut = None, cbkStdErr = None, sh=False):
    """
    Ejecuta una aplicacion en segundo plano capturando su salida en tiempo real

    Parametros:
        app = string con la aplicacion y parametros
        cbkStdOut = funcion para captura de salida estandar en tiempo real
        cbkStdErr = funcion para captura de salida error en tiempo real,
                    si no se provee es redirigido a stdout
        sh =    Ejecutar en shell del sistema,
                necesario cuando los parametros de la aplicación incluyen wildcards (*, ?)

    Devuelve el codigo de salida de la aplicación o la excepcion producida si no se puede ejecutar

    Licencia: MIT
    """

    # -- inicio --
    if not cbkStdErr:
        cbkStdErr = cbkStdOut

    if not sh:
        # la ejecucion CON shell precisa que app sea un str con el comando mas todos sus parametros
        # la ejecucion SIN shell precisa que app sea una lista [comando, parametro, parametro, ...]
        app = [p for p in re.split(" |(\".*?\")|(\'.*?\')", app) if p]

    try:
        pr = subprocess.Popen(app,
                              bufsize = 0,
                              stdout = subprocess.PIPE,
                              stderr = subprocess.PIPE,
                              shell = sh)

    except  Exception, e:
        # fallo al ejecutar, comando incorrecto, ....
        raise

    # lanzar treads de captura
    tout = readpipe(pr.stdout, cbkStdOut)
    terr = readpipe(pr.stderr, cbkStdErr)
    tout.start()
    terr.start()

    # esperar que finalice
    pr.wait()

    # esperar que finalizen los threads,
    # en algunos casos se da el proceso por terminado pero todavia no se han cerrado
    # los pipes y quedan datos en los buffers, hay que esperar que los threads
    # terminen de capturar los datos
    while tout.isAlive() or terr.isAlive():
        pass

    # devolver codigo de salida de la aplicacion
    return pr.poll()

##############################
# test, ejemplos
##############################
if __name__ == "__main__":

     import sys

     def printstdout(msg):
         print "Out capturado:%s" % (msg),
         sys.stdout.flush()

     def printstderr(msg):
         print "Err capturado:%s" % (msg),
         sys.stdout.flush()

     def printlista(lista):
         for l in lista:
             print "\t%s" % l,

     # -- capturar resultado en tiempo real --
     cmd = "ping www.google.com"
     ret =  runapp(cmd, printstdout, printstderr)
     if ret == 0:
         print "%s OK " % cmd
     else:
         print "%s Falló con codigo %s" % (cmd, ret)


     # -- ejecutar y guardar el resultado en una lista --
     cmd = "ping www.google.com"
     out = []
     ret =  runapp(cmd, out.append)
     if ret == 0:
         print "%s OK" % cmd
     else:
         print "%s Falló con codigo %s" % (cmd, ret)
     print "Detalles:"
     printlista(out)

     # -- ejecutar en shell --
     out = []
     cmd = "dir *.*"
     ret = runapp(cmd, out.append, sh=True)
     if ret == 0:
         print "%s OK" % cmd
     else:
         print "%s falló con codigo %s" % (cmd, ret)
     printlista(out)

     # -- ejecutar simple, no capturar salida ----
     if runapp("ping dominio.que.no.responde.com") == 0:
         print "OOPS, dominio.que.no.responde.com ¡¡Si responde!!"
     else:
         print "dominio.que.no.responde.com, no responde"
