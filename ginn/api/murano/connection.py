#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pymssql

def connect(server = r"LOGONSERVER\MURANO",
            user = "logic",
            password = None,
            database = "GEOTEXAN"):
    # TODO: PORASQUI
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

