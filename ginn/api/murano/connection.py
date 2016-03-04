#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import logging
logging.basicConfig(filename = "%s.log" % (
    ".".join(os.path.basename(__file__).split(".")[:-1])),
    level = logging.DEBUG)
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
            print("Iniciando conexión [%s]" % "; ".join(
                    ["%s = %s" % (i, values[i]) for i in args if i != "self"]))
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
            print("Desconectando...")
        self.conn.disconnect()
        if VERBOSE:
            print("\t\t\t\t[OK]")

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
            logging.debug(sentence_sql)
            if DEBUG:
                strlog = " ==> SQLServer --> %s" % (str_clean(sentence_sql))
                print(strlog)
                logging.info(strlog)
            if self.conn:   # En modo DEBUG esto es None.
                try:
                    if VERBOSE:
                        strlog = "Lanzando consulta %s..." % (
                                sentence_sql.split()[0])
                        print(strlog)
                        logging.info(strlog)
                    res = c.execute(sentence_sql)
                    if "SELECT" in sentence_sql:
                        if VERBOSE:
                            strlog = "    · fetchall..."
                            print(strlog)
                            logging.info(strlog)
                        res = c.fetchall()
                        if VERBOSE:
                            strlog = "\t\t\t\t\t\t\t\t\t[OK]"
                            print(strlog)
                            logging.info(strlog)
                    else:
                        if VERBOSE:
                            strlog = "    · commit..."
                            print(strlog)
                            logging.info(strlog)
                        self.conn.commit()
                        if VERBOSE:
                            strlog = "\t\t\t\t\t\t\t\t\t[OK]"
                            print(strlog)
                            logging.info(strlog)
                except Exception, e:
                    if not DEBUG:
                        logging.critical(e)
                        raise e
                    else:
                        strerror = "\t\t\t\t -- (!) [Excepción %s]" % e
                        print(strerror)
                        logging.error(strerror)
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
