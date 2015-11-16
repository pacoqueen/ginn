#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pymssql

class Connection:
    def __init__():
        self.conn = self.__connect()

    def __connect(server = r"LOGONSERVER\MURANO",
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
        conn = pymssql.connect(server = server, user = user, password = password,
                               database = database)
        return conn

    def disconnect():
        """
        Desconecta la sesión actual con MS-SQLServer.
        """
        self.conn.disconnect()



