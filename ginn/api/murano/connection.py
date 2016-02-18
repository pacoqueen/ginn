#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pymssql
import inspect

DEBUG = True
DEBUG = False
VERBOSE = True

class Connection:
    def __init__(self):
        self.__database = ""    # Inicialización temporal hasta que conecte.
        try:
            self.conn = self.__connect()
        except pymssql.InterfaceError, e:
            if DEBUG:
                self.conn = None    # No se pudo conectar. Modo "debug".
            else:
                raise e

    def __del__(self):
        try:
            self.conn.close()
        except AttributeError:
            pass    # No hay conexión que cerrar. 

    def __connect(self,
                  server = r"LOGONSERVER\MURANO",
                  user = "logic",
                  password = None,
                  database = "GEOTEXAN"):
        """
        Inicia la conexión con los parámetros por defecto. Es necesario que
        exista un fichero credentials.txt con la contraseña para acceder al
        servidor MS-SQLServer.
        """
        if VERBOSE:
            frame = inspect.currentframe()
            args, _, _, values = inspect.getargvalues(frame)
            print "Iniciando conexión [%s]" % "; ".join(
                    ["%s = %s" % (i, values[i]) for i in args if i != "self"])
        self.__database = database
        if password is None:
            try:
                directorio = os.path.abspath(os.path.dirname(__file__))
                credentials = open(os.path.join(directorio, "credentials.txt"))
            except IOError:
                raise Exception, "Cree un fichero credentials.txt en %s "\
                        "conteniendo la contraseña para el usuario %s." %(
                                directorio, user)
            else:
                password = credentials.readlines()[0].split()[0]
                credentials.close()
        try:
            conn = pymssql.connect(server = server, user = user,
                                   password = password, database = database)
        except TypeError:   # Depende de la versión usa host o server.
            conn = pymssql.connect(host = server, user = user,
                                   password = password, database = database)
        return conn

    def get_database(self):
        """
        Devuelve como cadena el nombre de la base de datos a la que
        está conectado.
        """
        return self.__database

    def disconnect(self):
        """
        Desconecta la sesión actual con MS-SQLServer.
        """
        if VERBOSE:
            print "Desconectando...",
        self.conn.disconnect()
        if VERBOSE:
            print "[OK]"

    def run_sql(self, sql):
        """
        Crea un cursor, ejecuta la(s) consulta(s) y cierra el cursor.
        """
        res = None
        if not isinstance(sql, (list, tuple)):
            sql = [sql]
        try:
            c = self.conn.cursor(as_dict = True)
        except AttributeError, e:
            if not DEBUG:
                raise e
        for sentence_sql in sql:
            if DEBUG:
                print " ==> SQLServer -->", str_clean(sentence_sql)
            if self.conn:
                try:
                    if VERBOSE:
                        print "Lanzando consulta %s..." % (
                                sentence_sql.split()[0]),
                    res = c.execute(sentence_sql)
                    if "SELECT" in sentence_sql:
                        if VERBOSE:
                            print "· fetchall...",
                        res = c.fetchall()
                        if VERBOSE:
                            print "[OK]"
                    else:
                        if VERBOSE:
                            print "· commit...",
                        self.conn.commit()
                        if VERBOSE:
                            print "[OK]"
                except Exception, e:
                    if not DEBUG:
                        raise e
                    else:
                        print " -- (!) [Excepción %s]" % e
        return res

def str_clean(s):
    """
    Devuelve la consulta SQL sin comentarios ni retornos de carro.
    """
    import re
    res = re.sub(r"--.*[$|\n]", "", s)
    res = res.split()
    res = " ".join([word.strip() for word in res])
    return res
