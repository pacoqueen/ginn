#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008 Francisco José Rodríguez Bogado,                   #
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
## parse_mdblogic.py - Procesa un .MDB de LOGIC CONTROL.
###################################################################
## NOTAS:
## Necesita las "mx extensions" de Egenix (no pertenecen a la 
## biblioteca estándar de Python).
##  
###################################################################
## Changelog:
## 12 de julio de 2005 -> Inicio
## 
## 
###################################################################
## 
###################################################################

##### xmlrpcserver.py #####

#
# XML-RPC SERVER
# $Id: parse_mdblogic.py,v 1.8 2008/01/18 10:19:19 pacoqueen Exp $
#
# a simple XML-RPC server for Python
#
# History:
# 1999-02-01 fl  added to xmlrpclib distribution
#
# written by Fredrik Lundh, January 1999.
#
# Copyright (c) 1999 by Secret Labs AB.
# Copyright (c) 1999 by Fredrik Lundh.
#
# fredrik@pythonware.com
# http://www.pythonware.com
#
# --------------------------------------------------------------------
# Permission to use, copy, modify, and distribute this software and
# its associated documentation for any purpose and without fee is
# hereby granted.  This software is provided as is.
# --------------------------------------------------------------------
#

import SocketServer, BaseHTTPServer
import xmlrpclib, sys, tempfile, os, time, csv, mx
sys.path.append('.')
import pclases

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            # get arguments
            data = self.rfile.read(int(self.headers["content-length"]))
            params, method = xmlrpclib.loads(data)

            # generate response
            try:
                response = self.call(method, params)
                # wrap response in a singleton tuple
                response = (response,)
            except:
                # report exception back to server
                response = xmlrpclib.dumps(
                    xmlrpclib.Fault(1, "%s:%s" % sys.exc_info()[:2])
                    )
            else:
                response = xmlrpclib.dumps(
                    response,
                    methodresponse=1
                    )
        except:
            # internal error, report as HTTP server error
            self.send_response(500)
            self.end_headers()
        else:
            # got a valid XML RPC response
            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.send_header("Content-length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

            # shut down the connection (from Skip Montanaro)
            self.wfile.flush()
            self.connection.shutdown(1)

    def call(self, method, params):
        # override this method to implement RPC methods
        print "CALL", method, params
        return params

#################### 

class MDBParser(RequestHandler):
    def __init__(self, *args, **kws):
        print "Iniciando eXtendedMarkupLanguageRemoteProcedureCall..."
        RequestHandler.__init__(self, *args, **kws)

    def __volcar_mdb(self, nomarchivo, nomarchivo_cuentas):
        try:
            f = open(nomarchivo)
        except:
#            utils.dialogo_info(titulo = "ERROR", texto = "Archivo %s no encontrado." % (nomarchivo))
            return None
        f.close()
        try:
            f = open(nomarchivo_cuentas)
        except:
#            utils.dialogo_info(titulo = "ERROR", texto = "Archivo %s no encontrado." % (nomarchivo_cuentas))
            return None
        f.close()
        # Exportación de movimientos:
        tmpcsv = 'movimientos_%s.csv' % '_'.join(map(str,time.localtime()[:6]))
        tmpcsv = os.path.join(tempfile.gettempdir(), tmpcsv)
        comando = 'mdb-export -H %s Movimientos > %s' % \
            (nomarchivo, tmpcsv)
        print 'Ejecutando %s...\n' % comando
        if os.system(comando):  # salida típica de un comando es 0 para no errores, !=0 para error.
            res = [None, None]
        else:
            res = [tmpcsv, None]
        # Exportación de plan de cuentas:
        tmpcsv = 'plandecuentas_%s.csv' % '_'.join(map(str,time.localtime()[:6]))
        tmpcsv = os.path.join(tempfile.gettempdir(), tmpcsv)
        comando = 'mdb-export -H %s PlanDeCuentas > %s' % \
            (nomarchivo_cuentas, tmpcsv)
        print 'Ejecutando %s...\n' % comando
        if os.system(comando):  # salida típica de un comando es 0 para no errores, !=0 para error.
            res[1] = None
        else:
            res[1] = tmpcsv
        return res

    def __parse_mdb(self, fichero, fichero_cuentas):
        """
        Busca el fichero .MDB en /tmp.
        Si lo encuentra, exporta su contenido a CVS.
        Abre el fichero CVS y por cada registro:
            Comprueba si ya existe en la BD (mediante sqlobject, por lo que no es necesario
            recibir la configuración de tabla, BD y demás) y si no existe lo inserta.
        fichero y fichero_cuentas puede ser el mismo. Del primero extrará la información 
        de los asientos en sí. Del segundo, el titular o nombre de cada códugo de cuenta.
        """
        ruta_a_fichero = os.path.join(tempfile.gettempdir(), fichero)
        ruta_a_fichero_cuentas = os.path.join(tempfile.gettempdir(), fichero_cuentas)
        print "parse_mdb: %s + %s" % (ruta_a_fichero, ruta_a_fichero_cuentas)
        ruta_a_csv_mov, ruta_a_csv_cue = self.__volcar_mdb(ruta_a_fichero, ruta_a_fichero_cuentas)
        if ruta_a_csv_mov != None and ruta_a_csv_cue != None:
            print "MDB volcado a %s + %s." % (ruta_a_csv_mov, ruta_a_csv_cue)
            res = self.__insertar_csv_en_bd(ruta_a_csv_mov, ruta_a_csv_cue)
        else:
            print "CVS DUMP ERROR"
            res = -3
        return res
    
    def __existe_en_bd(self, asiento, orden, codigoCuenta):
        """
        Devuelve True si el registro ya existe en la tabla de Logic.
        Los campos índice (o al menos creo que UNIQUE) en la tabla
        Movimientos de Logic Control.
        """
        consulta = pclases.LogicMovimientos.select(pclases.AND(pclases.LogicMovimientos.q.asiento == asiento,
                                                               pclases.LogicMovimientos.q.orden == orden,
                                                               pclases.LogicMovimientos.q.codigoCuenta == codigoCuenta))
        return consulta.count() > 0
        
    
    def __insertar_csv_en_bd(self, ruta_a_csv_mov, ruta_a_csv_cue):
        # Volcado de plan de cuentas (Nº Cuenta, empresa)
        fcsv = open(ruta_a_csv_cue)
        reader = csv.reader(fcsv)
        cuentas = {}
        while(1):
            try:
                datos = reader.next()
                codigoCuenta = datos[4].strip()
                cuenta = datos[5].strip()
                print codigoCuenta, cuenta
                cuentas[codigoCuenta] = cuenta
            except StopIteration:   # Se terminó
                break
        # Volcado de movimientos.
        fcsv = open(ruta_a_csv_mov)
        reader = csv.reader(fcsv)
        insertados = 0
        errores = 0
        ignorados = 0
        registros = 0
        while(1):
            try:
                datos = reader.next()
                registros += 1
                print "Procesando %s... " % (datos),
                asiento = int(datos[5])
                orden = int(datos[6])
                codigoCuenta = datos[11].strip()
                if codigoCuenta in cuentas:
                    cuenta = cuentas[codigoCuenta]
                else:
                    cuenta = ''
                if not self.__existe_en_bd(asiento, orden, codigoCuenta):
                    try:
                        nuevo_registro = pclases.LogicMovimientos(asiento = asiento, 
                                                                  orden = orden,
                                                                  fecha = mx.DateTime.DateTimeFrom(datos[7]),
                                                                  cargoAbono = datos[10].strip(),
                                                                  codigoCuenta = codigoCuenta,
                                                                  contrapartidaInfo = datos[12].strip(),
                                                                  comentario = datos[15].strip(),
                                                                  importe = float(datos[16]),
                                                                  cuenta = cuenta)
                        print("... %d insertado.\n" % nuevo_registro.id)
                        insertados += 1
                    except:
                        print("ERROR: Registro no insertado\n")
                        errores += 1
                else:
                    print "Registro ya existe. No se importa.\n"
                    ignorados += 1
            except StopIteration:   # Se terminó
                break
        print """
        RESUMEN:
        %d cuentas
        %d registros
        %d insertados
        %d erróneos
        %d ignorados
        """ % (len(cuentas), registros, insertados, errores, ignorados)
        if errores:
            return -4   # Ya habrá tiempo de ser más explícitos.
        else:
            return 0
    
    def call(self, method, params):
        print "Ejecutando %s..." % method
        if method.lower() == "parse":
            if len(params) == 2:
                res = self.__parse_mdb(params[0], params[1])
                if res < 0:
                    print "Hubo errores en la importación."
                else:
                    print "Archivo procesado correctamente."
            else:
                print "Error en los parámetros."
                res = -1
        else:
            print "Método no reconocido."
            res = -2
        return res


def main(puerto):
#    server = SocketServer.TCPServer(('', puerto), RequestHandler)
    server = SocketServer.TCPServer(('', puerto), MDBParser)
    print "Iniciando servidor en TCP(%d)..." % puerto
    server.serve_forever()


if __name__ == "__main__":
    main(22222)

