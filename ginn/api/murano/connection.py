#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Funciones relacionadas con la conexión a SQLServer.

Se definen aquí también las constantes CODEMPRESA (empresa destino en Murano),
VERBOSE y DEBUG.
"""

from __future__ import print_function
import os
import logging
logging.basicConfig(
    filename="%s.log" % (".".join(os.path.basename(__file__).split(".")[:-1])),
    format="%(asctime)s %(levelname)-8s : %(message)s",
    level=logging.DEBUG)
import inspect
import pymssql

# DEBUG = True
DEBUG = False
VERBOSE = True
CODEMPRESA = 8000   # Empresa de pruebas. Cambiar por la 10200 en producción.


class Connection(object):
    """
    Clase que encapsula la conexión a SQLServer.
    """
    def __init__(self):
        self.__database = ""    # Inicialización temporal hasta que conecte.
        try:
            self.conn = self.__connect()
        except pymssql.InterfaceError as exception:
            if DEBUG:
                self.conn = None    # No se pudo conectar. Modo "debug".
            else:
                raise exception

    def __del__(self):
        try:
            self.conn.close()
        except AttributeError:
            pass    # No hay conexión que cerrar.

    def __connect(self,
                  server=r"LOGONSERVER\MURANO",
                  user="logic",
                  password=None,
                  database="GEOTEXAN"):
        """
        Inicia la conexión con los parámetros por defecto. Es necesario que
        exista un fichero credentials.txt con la contraseña para acceder al
        servidor MS-SQLServer.
        """
        if VERBOSE and DEBUG:
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
                raise Exception("Cree un fichero credentials.txt en %s "
                                "conteniendo la contraseña para el usuario "
                                "%s." % (directorio, user))
            else:
                password = credentials.readlines()[0].split()[0]
                credentials.close()
        try:
            # pylint: disable=unexpected-keyword-arg
            conn = pymssql.connect(server=server, user=user,
                                   password=password, database=database)
        except TypeError:   # Depende de la versión usa host o server.
            conn = pymssql.connect(host=server, user=user,
                                   password=password, database=database)
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
        if VERBOSE and DEBUG:
            print("Desconectando...")
        # pylint: disable=no-member
        self.conn.disconnect()
        if VERBOSE and DEBUG:
            print("\t\t\t\t[OK]")

    # pylint: disable=too-many-branches
    def run_sql(self, sql):
        """
        Crea un cursor, ejecuta la(s) consulta(s) y cierra el cursor.
        """
        res = None
        if not isinstance(sql, (list, tuple)):
            sql = [sql]
        try:
            conn = self.conn.cursor(as_dict=True)
        except AttributeError as exception:
            if not DEBUG:
                raise exception
        for sentence_sql in sql:
            logging.info("SQL a ejecutar:")
            logging.info(str_clean(sentence_sql))
            if DEBUG:
                strlog = " ==> SQLServer --> %s" % (str_clean(sentence_sql))
                print(strlog)
                logging.debug(strlog)
            if self.conn:   # En modo DEBUG esto es None.
                try:
                    strlog = "Lanzando consulta %s..." % (
                        sentence_sql.split()[0])
                    logging.info(strlog)
                    if VERBOSE and DEBUG:
                        print(strlog)
                    res = conn.execute(sentence_sql)
                    if "SELECT" in sentence_sql:
                        strlog = "    · fetchall..."
                        logging.info(strlog)
                        if VERBOSE and DEBUG:
                            print(strlog)
                        res = conn.fetchall()
                        strlog = "\t\t\t\t[OK]"
                        logging.info(strlog)
                        if VERBOSE and DEBUG:
                            print(strlog)
                    else:
                        strlog = "    · commit..."
                        logging.info(strlog)
                        if VERBOSE and DEBUG:
                            print(strlog)
                        self.conn.commit()
                        strlog = "\t\t\t\t[OK]"
                        logging.info(strlog)
                        if VERBOSE and DEBUG:
                            print(strlog)
                # pylint: disable=broad-except
                except Exception as exception:
                    if not DEBUG:
                        logging.critical(exception)
                        raise exception
                    else:
                        strerror = "\t\t\t -- (!) [Excepción %s]" % exception
                        print(strerror)
                        logging.error(strerror)
        return res


def str_clean(strsql):
    """
    Devuelve la consulta SQL sin comentarios ni retornos de carro.
    """
    import re
    res = re.sub(r"--.*[$|\n]", "", strsql)
    res = res.split()
    res = " ".join([word.strip() for word in res])
    return res
