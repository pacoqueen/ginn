#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado,                   #
#                          Diego Muñoz Escalante.                             #
# (pacoqueen@users.sourceforge.net, escalant3@users.sourceforge.net)          #
#                                                                             #
# This file is part of GeotexInn.                                             #
#                                                                             #
# GeotexInn is free software; you can redistribute it and/or modify           #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation; either version 2 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# GeotexInn is distributed in the hope that it will be useful,                #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with GeotexInn; if not, write to the Free Software                    #
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA  #
###############################################################################

###################################################################
## sshsession.py - Clases para sesiones ssh en GNU/Linux y MS-Windows.
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 13 de julio de 2006 -> Inicio
###################################################################
## NOTAS:
## El 90% del código es calcado del de Peter Hansen 
## <peter@engcorp.com> 
## (visto en: http://www.thescripts.com/forum/thread20344.html)
## 
###################################################################


import sys
import os
import time

True, False = 1, 0

class SshException(Exception): 
    pass

class LinuxSshSession:
    # DONE: Tiene un bug. Si no pide contraseña (porque se haya exportado la clave pública) interpreta el 
    # EOF de fin de sesión como error en la autentificación. Aún así, funciona, aunque dispare una 
    # excepción al final. Arreglado con la opción PubkeyAuthentication=no.
    PAT_PASSWORD = '[pP]assword:'

    def __init__(self, host, user, password, timeout=30):
        self.host = host
        self.user = user
        self.password = password
        self.timeout = timeout
        self.verbose = False

    def scp(self, src, dest):
        import pexpect
        user = self.user
        host = self.host

        if self.verbose:
            sys.stdout.write('scp "%(src)s" %(user)s@%(host)s:%(dest)s ...' % locals())
            sys.stdout.flush()
            began = time.time()

        try:
            # use compression (not that that would help with a .tgz file
            # and make sure we don't get messed up by the known_hosts file
            child = pexpect.spawn('scp -C'
            ' -o UserKnownHostsFile=/dev/null'
            ' -o StrictHostKeyChecking=no'
            ' -o PubkeyAuthentication=no'
            ' %(src)s %(user)s@%(host)s:%(dest)s' % locals())
            state = 'authorizing'
            while 1:
                #~ print '%s: %r///%r' % (state, child.before, child.after)
                if state == 'authorizing':
                    match = child.expect([pexpect.EOF, pexpect.TIMEOUT, self.PAT_PASSWORD], timeout=self.timeout)
                    if match == 0:
                        raise SshException('failed to authenticate')
                    elif match == 1:
                        raise SshException('timeout waiting to authenticate')
                    elif match == 2:
                        child.sendline(self.password)
                        state = 'copying'

                elif state == 'copying':
                    match = child.expect([pexpect.EOF, pexpect.TIMEOUT, 'stalled', 'ETA'], timeout=self.timeout)
                    if match == 0:
                        break
                    elif match == 1:
                        raise SshException('timeout waiting for response')
                    elif match == 2:
                        state = 'stalled'

                elif state == 'stalled':
                    match = child.expect([pexpect.EOF, pexpect.TIMEOUT, 'ETA'], timeout=self.timeout)
                    if match == 0:
                        break
                    elif match == 1:
                        #import pdb
                        #pdb.set_trace()
                        raise SshException('stalled for too long, aborted copy')
                    elif match == 2:
                        state = 'copying'

        finally:
            if self.verbose:
                elapsed = time.time() - began
                try:
                    size = os.stat(src)[os.path.stat.ST_SIZE]
                    rate = size / elapsed
                    sys.stdout.write(' %.1fs (%d cps)\n' % (elapsed, rate))
                except:
                    sys.stdout.write(' %.1fs\n' % (elapsed))


    def ssh(self, cmd):
        import pexpect
        user = self.user
        host = self.host

        if self.verbose:
            sys.stdout.write('ssh -l %(user)s %(host)s \"%(cmd)s\"\n' % locals())
            sys.stdout.flush()

        # use compression
        # -o options make sure we don't get messed up by the known_hosts file
        child = pexpect.spawn('ssh -C'
        ' -o UserKnownHostsFile=/dev/null'
        ' -o StrictHostKeyChecking=no'
        ' -l %(user)s %(host)s '
        '\"%(cmd)s\"' % locals())
        state = 'authorizing'
        while 1:
            if state == 'authorizing':
                match = child.expect([pexpect.EOF, pexpect.TIMEOUT, self.PAT_PASSWORD],
                timeout=self.timeout)
            if match == 0:
                raise SshException('failed to authenticate')
            elif match == 1:
                raise SshException('timeout waiting to authenticate')
            elif match == 2:
                child.sendline(self.password)
                state = 'running'

            elif state == 'running':
                match = child.expect([pexpect.EOF, pexpect.TIMEOUT],
                timeout=self.timeout)
                if match == 0:
                    break
                elif match == 1:
                    raise SshException('timeout waiting to finish')

        return child.before


class WindowsSshSession:
    def __init__(self, host, user, password, timeout=30):
        self.host = host
        self.user = user
        self.password = password

    def scp(self, src, dest):
        user = self.user
        host = self.host
        password = self.password
        argumentos = '-pw %(password)s "%(src)s" %(user)s@%(host)s:%(dest)s' % locals()
        ejecutable = os.path.join('..', 'utils', 'pscp.exe')   # Asumo que me encuentro en "formularios"
        comando = '%s %s' % (ejecutable, argumentos)
        return os.system(comando)

    def ssh(self, cmd):
        user = self.user
        host = self.host
        password = self.password
        argumentos = '-pw %(password)s -ssh %(user)s@%(host)s "%(cmd)s"' % locals()
        ejecutable = os.path.join('..', 'utils', 'plink.exe')   # Asumo que me encuentro en "formularios"
        comando = '%s %s' % (ejecutable, argumentos)
        return os.system(comando)


def SshSession(host, user, password, timeout=30):
    if sys.platform == 'win32':
        sessionClass = WindowsSshSession
    else:
        # assume we're on linux if platform is not windows
        sessionClass = LinuxSshSession
    return sessionClass(host, user, password, timeout)


if __name__ == "__main__":
    sesion = SshSession(host = 'tetsuo', user = 'geotexan', password = 'geotexan')
    sesion.scp(src = 'sshsession.py', dest = '/tmp')

