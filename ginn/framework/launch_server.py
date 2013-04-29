#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################
# Modificado por Francisco Jos� Rodr�guez Bogado
######################################################
# Código para simular un daemon sacado de:
# http://homepage.hispeed.ch/py430/python/daemon.py
######################################################

import os, sys
#os.chdir("/home/cleo1/compbio/amir/BiRC_New/BiRC")
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

try:
    from framework import parse_mdblogic
except ImportError, msg:
    print 'Error importando "parse_mdblogic": %s' % (msg)
    sys.exit(1)


###########################################################################
# configure these paths:
LOGFILE = '/var/log/parse_mdblogic.log'
PIDFILE = '/var/run/parse_mdblogic.pid'

# and let USERPROG be the main function of your project
#import mymain
#USERPROG = mymain.main
USERPROG = parse_mdblogic.main
###########################################################################

#based on J�rgen Hermanns http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66012

class Log:
    """file like for writes with auto flush after each write
    to ensure that everything is logged, even during an
    unexpected exit."""
    def __init__(self, f):
        self.f = f
    def write(self, s):
        self.f.write(s)
        self.f.flush()

def main():
    #change to data directory if needed
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
    #os.chdir("/root/data")
    #redirect outputs to a logfile
    sys.stdout = sys.stderr = Log(open(LOGFILE, 'a+'))
    #ensure the that the daemon runs a normal user
    os.setegid(0)     #root, si no no puedo pillar el puerto 80
    os.seteuid(0)     #
    #os.setegid(103)     #set group first "pydaemon"
    #os.seteuid(103)     #set user "pydaemon"
    #start the user program here:
    USERPROG(22222)

if __name__ == "__main__":
    # do the UNIX double-fork magic, see Stevens' "Advanced
    # Programming in the UNIX Environment" for details (ISBN 0201563177)
    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    # decouple from parent environment
    os.chdir("/")   #don't prevent unmounting....
    os.setsid()
    os.umask(0)

    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent, print eventual PID before
            #print "Daemon PID %d" % pid
            open(PIDFILE,'w').write("%d"%pid)
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    # start the daemon main loop
    main()

