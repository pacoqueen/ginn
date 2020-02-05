#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Funciones relacionadas con la conexión a SQLServer.

Se definen aquí también las constantes CODEMPRESA (empresa destino en Murano),
VERBOSE y DEBUG.
"""

from __future__ import print_function
import os
import inspect
import logging
import pymssql
logging.basicConfig(
    filename="%s.log" % (".".join(os.path.basename(__file__).split(".")[:-1])),
    format="%(asctime)s %(levelname)-8s : %(message)s",
    level=logging.DEBUG)

DEBUG = False
VERBOSE = False
CODEMPRESA = 10200  # Empresa de pruebas: 800. Cambiar a la 10200 en producción
# Canales HARCODED
(FIBRA, RESIDUOS_FIBRA,
 GEOTEXTIL, RESIDUOS_GEOTEXTIL,
 GEOCEM,
 COMERCIALIZADO) = (100, 101, 200, 201, 300, 400)
CANALES = {'100': FIBRA, '101': RESIDUOS_FIBRA,
           '200': GEOTEXTIL, '201': RESIDUOS_GEOTEXTIL,
           '300': GEOCEM, '400': COMERCIALIZADO}
(DANOSA, GEOSYNTHETICS, INTERMAS) = range(1, 4)
PROYECTOS = {'DANOSA': DANOSA,
             'GEOSYN': GEOSYNTHETICS,
             'INTERM': INTERMAS,
             '      ': 0  # Sin informar
             }


class Connection(object):
    """
    Clase que encapsula la conexión a SQLServer.
    """
    def __init__(self):
        self.__database = ""    # Inicialización temporal hasta que conecte.
        try:
            self.conn = self.__connect()
        # pylint: disable=no-member
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
            # pylint: disable=unexpected-keyword-arg, no-member
            conn = pymssql.connect(server=server, user=user,
                                   password=password, database=database)
        except TypeError:   # Depende de la versión usa host o server.
            # pylint: disable=no-member
            conn = pymssql.connect(host=server, user=user,
                                   password=password, database=database)
        return conn

    def get_database(self):
        """
        Devuelve como cadena el nombre de la base de datos a la que
        está conectado.
        """
        return self.__database

    def get_codempresa(self):
        """
        Devuelve el código de empresa sobre el que estamos trabajando en
        Murano.
        """
        return CODEMPRESA

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

    # pylint: disable=too-many-branches, too-many-statements
    def run_sql(self, sql):
        """
        Crea un cursor, ejecuta la(s) consulta(s) y cierra el cursor.
        """
        res = None
        if not isinstance(sql, (list, tuple)):
            sql = [sql]
        try:
            cursor = self.conn.cursor(as_dict=True)
        except TypeError:
            cursor = self.conn.cursor()
        except AttributeError as exception:
            if not DEBUG:
                raise exception
        for sentence_sql in sql:
            # logging.info("SQL a ejecutar:")
            if VERBOSE:
                logging.info(str_clean(sentence_sql))
            if DEBUG:
                strlog = " ==> SQLServer --> %s" % (str_clean(sentence_sql))
                print(strlog)
                logging.debug(strlog)
            if self.conn:   # En modo DEBUG esto es None.
                try:
                    strlog = "Lanzando consulta %s..." % (
                        sentence_sql.split()[0])
                    # logging.info(strlog)
                    if VERBOSE and DEBUG:
                        print(strlog)
                    res = cursor.execute(sentence_sql)
                    if "SELECT" in sentence_sql:
                        strlog = "    · fetchall..."
                        # logging.info(strlog)
                        if VERBOSE and DEBUG:
                            print(strlog)
                        try:
                            res = cursor.fetchall_asdict()
                        except AttributeError:
                            res = cursor.fetchall()
                        strlog = "\t\t\t\t[OK]"
                        if VERBOSE:
                            logging.info(strlog)
                        if VERBOSE and DEBUG:
                            print(strlog)
                    else:
                        strlog = "    · commit..."
                        # logging.info(strlog)
                        if VERBOSE and DEBUG:
                            print(strlog)
                        self.conn.commit()
                        res = True
                        strlog = "\t\t\t\t[OK]"
                        if VERBOSE:
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
