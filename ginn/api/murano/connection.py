#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pymssql

DEBUG = True

class Connection:
    def __init__(self):
        self.DEBUG = DEBUG
        try:
            self.conn = self.__connect()
        except pymssql.InterfaceError, e:
            if self.DEBUG:
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
        if password is None:
            try:
                directorio = os.path.abspath(os.path.dirname(__file__))
                credentials = open(os.path.join(directorio, "credentials.txt"))
            except IOError:
                raise Exception, "Cree un fichero credentials.txt en %s "\
                        "conteniendo la contraseña para el usuario %s." %(
                                directorio, user)
            else:
                password = credentials.readlines()[0]
                credentials.close()
        try:
            conn = pymssql.connect(server = server, user = user,
                                   password = password, database = database)
        except TypeError:
            conn = pymssql.connect(host = server, user = user,
                                   password = password, database = database)
        return conn

    def disconnect(self):
        """
        Desconecta la sesión actual con MS-SQLServer.
        """
        self.conn.disconnect()

    def run_sql(self, sql):
        """
        Crea un cursor, ejecuta la(s) consulta(s) y cierra el cursor.
        """
        if not isinstance(sql, (list, tuple)):
            sql = [sql]
        try:
            c = self.conn.cursor()
        except AttributeError, e:
            if not self.DEBUG:
                raise e
        for sentence_sql in sql:
            if self.DEBUG:
                print " ==> SQLServer -->", sql
            if self.conn:
                try:
                    c.execute(sql)
                    c.fetchall()
                except Exception, e:
                    if not self.DEBUG:
                        raise e

