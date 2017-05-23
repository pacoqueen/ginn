#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2017 Francisco José Rodríguez Bogado,                    #
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

###############################################################################
# BUG localizado: El gc no puede eliminar objetos de memoria (o al menos sus
#                 hilos) por estar las hebras pendientes del "signal" aunque el
#                 objeto persistente ya no se use más en adelante.
#                 Ver weakref y en especial este código:
#                 http://osdir.com/ml/python.general.castellano/2004-03
#                   /msg00116.html
###############################################################################

# DONE: Aún colea de vez en cuando el error en los hilos al salir del
# intérprete de python a pesar de que ya he solucionado otros muy parecidos
# que salían también.

# DONE: URGENTE: Con el mismo objeto en dos ventanas funciona bien. Cuando hay
# tres (o más, supongo) empieza a fallar a veces y se queda bloqueada la
# ventana de "Actualizar".
# Esto de arriba ocurre con las señales. Tal y como se hace ahora (ver NOTAS)
# no hay problema.

# PLAN: El _init se podría haber heredado. GAÑANAZO.

# NOTAS:
#  Ahora mismo todo esto es un batiburrillo. Las notificaciones de cambios
# remotos, el IPC, la persistencia y todo eso de momento queda en el aire. Lo
# voy a hacer a la forma "tradicional".
#  El ye olde check: Cada cierto tiempo comprobar si hay cambios entre los
# atributos del objeto y los de la caché local (que aquí se llama swap por
# motivos que no vienen a cuento), y si los hay lanzo la función definida en
# el notificador y puto pelota.
#  ¿Qué es lo que hay que hacer entonces en cada ventana? Pues cada vez que se
# muestren datos en pantalla se llama al make_swap y con un timeout_add que
# chequean los cambios de vez en cuando con .chequear_cambios(). Fácil, ¿no?
# PUES NO ME GUSTA. Prefería las notificaciones y las señales de la BD, su
# hilo con su conexión IPC, etc...

"""
    Catálogo de clases persistentes.
"""


DEBUG = False
# DEBUG = True  # Se puede activar desde ipython después de importar con
                # pclases.DEBUG = True
VERBOSE = True  # Activar para mostrar por pantalla progreso al cargar clases.
VERBOSE = False

import sys
import os
if sys.executable.endswith("pythonw.exe"):
    # Porque entonces no hay stdout y salta excepción IOError 9
    # Más info: http://bugs.python.org/issue706263
    DEBUG = VERBOSE = False

from lib.myprint import myprint

if DEBUG or VERBOSE:
    myprint("IMPORTANDO PCLASES")

logged_user = None

from framework.configuracion import ConfigConexion, parse_params
from math import ceil
from select import select
from sqlobject.col import SOForeignKey, SODateCol, SODateTimeCol, \
                          SOUnicodeCol, SODecimalCol, SOMediumIntCol, \
                          SOSmallIntCol, SOTinyIntCol
from sqlobject.col import ForeignKey, SOBoolCol, SOCol  # @UnusedImport
from sqlobject.col import SOFloatCol, SOIntCol, SOStringCol   # @UnusedImport
from sqlobject.joins import MultipleJoin, RelatedJoin
from sqlobject.main import SQLObjectNotFound, SQLObject
from sqlobject.sqlbuilder import AND, OR, NOT  # @UnusedImport
from sqlobject import connectionForURI, sqlhub
import pprint
import re
import threading #, psycopg
import time
from formularios import utils
from framework import notificacion
import datetime
import mx.DateTime  # WARNING: Será marcado como DEPRECATED pronto.
try:
    from collections import OrderedDict
except ImportError:
    from lib.ordereddict import OrderedDict
from collections import defaultdict

# GET FUN !

usu, contra, modul, clas, confi, verb, debu, obj_puid = parse_params()
# Comprueba que no se haya especificado una conf. alternativa y establezco
# parametrización en función de lo especificado en CLI. La configuración
# alternativa se cambia en el propio parse_params.
# El usuario lo establezco después, una vez declarada la clase.
if debu:
    DEBUG = debu
if verb:
    VERBOSE = verb
config = ConfigConexion()

#conn = '%s://%s:%s@%s/%s' % (config.get_tipobd(),
conn = '%s://%s:%s@%s/%s?autoCommit=False' % (config.get_tipobd(),
                                              config.get_user(),
                                              config.get_pass(),
                                              config.get_host(),
                                              config.get_dbname())

# HACK: No reconoce el puerto en el URI y lo toma como parte del host. Lo
# añado detrás y colará en el dsn cuando lo parsee.
#conn = '%s://%s:%s@%s/%s port=%s' % (config.get_tipobd(),
#                                     config.get_user(),
#                                     config.get_pass(),
#                                     config.get_host(),
#                                     config.get_dbname(),
#                                     config.get_puerto())
sqlhub.processConnection = connectionForURI(conn)

if DEBUG and VERBOSE:
    conndebug = connectionForURI(conn)
    #conndebug.autoCommit = False
    conndebug.debug = True

###############################################################################
## TODO: PORASQUI: Ya sé cómo conectar a dos BD a la vez y cruzar los datos
## de los cierres mensuales para detectar los códigos de rollos divergentes:
# https://www.mail-archive.com/sqlobject-discuss@lists.sourceforge.net/msg04028.html
#Just open connections:
#
#connection1 = connectionForURI('postgres://host:port/db')
#connection2 = connectionForURI('sqlite:///path/to/db')
#
#   and use them:
#
#class MyTable(SQLObject):
#   name = StringCol()
#
#   Get a row from the first DB:
#
#row1 = MyTable.get(id, connection=connection1)
#
#   and insert the data into the second:
#
#row2 = MyTable(**row.asDict(), connection=connection2)
#
#   Most methods in SQLObject accept connection parameter.
#
###############################################################################

# HACK:
# autocommit en algunas versiones es un boolean y sqlobject intenta
# activarlo como si fuera una función. Aquí hago el cambiazo:
#conhack = sqlhub.getConnection().getConnection()
#conhack = sqlhub.processConnection.getConnection()
conhack = connectionForURI(conn)
#conhack._autocommit = conhack.autocommit
#def _setAutoCommit(conn, auto):
#    conn.autocommit = auto
#conhack.autocommit = _setAutoCommit
#conhack.autocommit(1)
# Esto no funciona. Me pone el autocommit en otra conexión. Lo activo al final
# del fichero. Ver HACK antes del "__main__".
## if hasattr(conhack, "autocommit"):
##    if callable(conhack.autocommit):
##        conhack.autocommit(1)
##    else:
##        conhack.autocommit = 1
# HACK:
# Hago todas las consultas case-insensitive machacando la función de
# sqlbuilder y de paso hago un workaround del bug del doble caracter
# de ESCAPE con postgresql en la versión empaquetada con Ubuntu precise.
# TODO: Temporal hasta que la versión upstream 1.2 entre en el repositorio.
from sqlobject import sqlbuilder, LIKE, styles
_CONTAINSSTRING = sqlbuilder.CONTAINSSTRING
def CONTAINSSTRING_failsafe(expr, pattern):
    # return LIKE(expr, '%' + _LikeQuoted(pattern) + '%', escape='\\')
    # Esto de arriba DUPLICA el carácter \ y da error al ejecutar la consulta.
    return LIKE(expr, '%' + sqlbuilder._LikeQuoted(pattern) + '%')

def CONTAINSSTRING(expr, pattern):
    try:
        #nombre_clase = SQLObject.sqlmeta.style.dbTableToPythonClass(
        #                expr.tableName)
        nombre_clase = styles.defaultStyle.dbTableToPythonClass(
                        expr.tableName)
        clase = globals()[nombre_clase]
        columna = clase.sqlmeta.columns[expr.fieldName]
    except (AttributeError, KeyError):
        return _CONTAINSSTRING(expr, pattern)
    if isinstance(columna, (SOStringCol, SOUnicodeCol)):
        # Algunos backends no tienen ILIKE. En ese caso debería usar la
        # versión "a prueba de fallos" declarada arriba.
        op = sqlbuilder.SQLOp("ILIKE", expr,
                                '%' + sqlbuilder._LikeQuoted(pattern) + '%')
    elif isinstance(columna, (SOFloatCol, SOIntCol, SODecimalCol,
                              SOMediumIntCol, SOSmallIntCol, SOTinyIntCol)):
        try:
            pattern = str(float(pattern))
        except ValueError:
            pattern = None
        if not pattern:
            op = sqlbuilder.SQLOp("IS NOT", expr, None)
        else:
            op = sqlbuilder.SQLOp("=", expr,
                                    sqlbuilder._LikeQuoted(pattern))
    else:
        op = sqlbuilder.SQLOp("LIKE", expr,
                                '%' + sqlbuilder._LikeQuoted(pattern) + '%')
    return op

sqlbuilder.CONTAINSSTRING = CONTAINSSTRING


class SQLObjectChanged(Exception):
    """ User-defined exception para ampliar la funcionalidad
    de SQLObject y que soporte objetos persistentes."""
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return repr(self.value)
class SQLtuple(tuple):
    """
    Básicamemte una tupla, pero con la función .count() para hacerla
    "compatible" con los SelectResults de SQLObject.
    """
    def __init__(self, *args, **kw):
        if len(args) + len(kw) == 0:
            self.elbicho = tuple()
            tuple.__init__(self.elbicho)
        else:
            self.elbicho = tuple(*args, **kw)
            tuple.__init__(*args, **kw)
    #def __new__(self, *args, **kw):
    #    self.elbicho = tuple(*args, **kw)
    #    tuple.__new__(*args, **kw)
    def count(self):
        return len(self)
    def sum(self, campo):
        res = 0.0
        for item in self.elbicho:
            res += getattr(item, campo)
        return res

class SQLlist(list):
    """
    Básicamemte una lista, pero con la función .count() para hacerla
    "compatible" con los SelectResults de SQLObject.
    """
    def __init__(self, *args, **kw):
        if len(args) + len(kw) == 0:
            self.rocio = list()
            list.__init__(self.rocio)
        else:
            self.rocio = list(*args, **kw)
            list.__init__(self, *args, **kw)
    def count(self):
        return len(self.rocio)
    # DISCLAIMER: Paso de otra clase base para solo 2 funciones que se repiten.
    def sum(self, campo):
        res = 0.0
        for item in self.rocio:
            res += getattr(item, campo)
        return res
    def append(self, *args, **kw):
        raise TypeError, "No se pueden añadir elementos a un SelectResults"
    def extend(self, *args, **kw):
        raise TypeError, "No se puede extender un SelectResults."
    def insert(self, *args, **kw):
        raise TypeError, "No se pueden insertar elementos en un SelectResults."
    def pop(self, *args, **kw):
        raise TypeError, "No se pueden eliminar elementos de un SelectResults."
    def remove(self, *args, **kw):
        raise TypeError, "No se pueden eliminar elementos de un SelectResults."


class PRPCTOO:
    """
    Clase base para heredar y no repetir código.
    Únicamente implementa los métodos para iniciar un hilo de
    sincronización y para detenerlo cuando ya no sea necesario.
    Ningún objeto de esta clase tiene utilidad "per se".
    """
    # El nombre viene de todo lo que NO hace pero para lo que es útil:
    # PersistentRemoteProcessComunicatorThreadingObservadorObservado. TOOOOOMA.
    def __init__(self, nombre_clase_derivada = ''):
        """
        El nombre de la clase derivada pasado al
        constructor es para la metainformación
        del hilo.
        """
        self.__oderivado = nombre_clase_derivada
        self.swap = {}

    def abrir_conexion(self):
        """
        Abre una conexión con la BD y la asigna al
        atributo conexión de la clase.
        No sale del método hasta que consigue la
        conexión.
        """
        while 1:
            try:
                self.conexion = self._connection.getConnection()
                if DEBUG:
                    myprint(" --> Conexión abierta.")
                return
            except:
                myprint("ERROR estableciendo conexión secundaria para IPC."
                        " Vuelvo a intentar")

    def abrir_cursor(self):
        self.cursor = self.conexion.cursor()
        if DEBUG: myprint([self.cursor!=None and self.cursor or "El cursor devuelto es None."][0], self.conexion, len(self.conexion.cursors))

    def make_swap(self, campo = None):
        # Antes del sync voy a copiar los datos a un swap temporal, para
        # poder comparar:
        if not campo:
            for campo in self.sqlmeta.columns:
                self.swap[campo] = getattr(self, campo)
        else:
            self.swap[campo] = getattr(self, campo)

    def diff(self):
        """
        Devuelve un diccionario de nombres de campos y valores que han
        cambiado respecto al "swap" (valores en memoria a la hora de
        presentar la ventana).
        """
        res = {}
        self.sync()
        for campo in self.sqlmeta.columns:
            old = self.swap[campo]
            new = getattr(self, campo)
            if old != new:
                res[campo] = (old, new)
        return res

    def comparar_swap(self):
        """
        Lanza una excepción propia para indicar que algún valor ha cambiado
        remotamente en el objeto, comparando la caché en memoria local con
        los valores de la BD. Como mensaje de la excepción devuelve el nombre
        del campo que ha cambiado.
        Si han cambiado varios, saltará con el primero de ellos.
        """
        # Y ahora sincronizo:
        self.sync()
        # y comparo:
        for campo in self.sqlmeta.columns:
            if self.swap[campo] != getattr(self, campo):
                if DEBUG and VERBOSE:
                    myprint("comparar_swap\n\tCampo: %s. Valor swap: %s. "\
                          "Valor registro: %s" % (
                            campo, self.swap[campo], getattr(self, campo)))
                raise SQLObjectChanged(self)

    def cerrar_cursor(self):
        self.cursor.close()

    def cerrar_conexion(self):
        self.conexion.close()
        if DEBUG: myprint(" <-- Conexión cerrada.")

    ## Código del hilo:
    def esperarNotificacion(self, nomnot, funcion=lambda: None):
        """
        Código del hilo que vigila la notificación.
        self -> Objeto al que pertenece el hilo.
        nomnot es el nombre de la notificación a esperar.
        funcion es una función opcional que será llamada cuando se
        produzca la notificación.
        """
        if DEBUG: myprint("Inicia ejecución hilo")
        while self != None and self.continuar_hilo:   # XXX
            if DEBUG: myprint("Entra en la espera bloqueante: %s" % nomnot)
            self.abrir_cursor()
            self.cursor.execute("LISTEN %s;" % nomnot)
            self.conexion.commit()
            if select([self.cursor], [], [])!=([], [], []):
                if DEBUG: myprint("Notificación recibida")
                try:
                    self.comparar_swap()
                except SQLObjectChanged:
                    if DEBUG: myprint("esperarNotificacion: Objeto cambiado")
                    funcion()
                except SQLObjectNotFound:
                    if DEBUG: myprint("Registro borrado")
                    funcion()
                # self.cerrar_cursor()
        else:
            if DEBUG: myprint("Hilo no se ejecuta")
        if DEBUG: myprint("Termina ejecución hilo")

    def chequear_cambios(self):
        try:
            self.comparar_swap()
            # myprint("NO CAMBIA")
        except SQLObjectChanged:
            # myprint("CAMBIA")
            if DEBUG: myprint("chequear_cambios: Objeto cambiado")
            # myprint(self.notificador)
            self.notificador.run()
        except SQLObjectNotFound:
            if DEBUG: myprint("Registro borrado")
            self.notificador.run()

    def ejecutar_hilo(self):
        ## ---- Código para los hilos:
        self.abrir_conexion()
        self.continuar_hilo = True
        nombre_clase = self.__oderivado
        self.th_espera = threading.Thread(target = self.esperarNotificacion,
                    args = ("IPC_%s" % nombre_clase, self.notificador.run),
                    name="Hilo-%s" % nombre_clase)
        self.th_espera.setDaemon(1)
        self.th_espera.start()

    def parar_hilo(self):
        self.continuar_hilo = False
        if DEBUG: myprint("Parando hilo...")
        self.cerrar_conexion()

    def destroy_en_cascada(self, usuario = None, ventana = None):
        """
        Destruye recursivamente los objetos que dependientes y
        finalmente al objeto en sí.
        OJO: Es potencialmente peligroso y no ha sido probado a fondo.
             Puede llegar a provocar un RuntimeError por alcanzar la
             profundidad máxima de recursividad intentando eliminarse en
             cascada a sí mismo por haber ciclos en la BD.
        """
        for join in self.sqlmeta.joins:
            lista = join.joinMethodName
            for dependiente in getattr(self, lista):
            # for dependiente in eval("self.%s" % (lista)):
                if DEBUG:
                    myprint("Eliminando %s..." % dependiente)
                dependiente.destroy_en_cascada(ventana = ventana)
        self.destroy(usuario = usuario, ventana = ventana)

    def destroy(self, usuario = None, ventana = None):
        # Si no se especifica usuario se determinará a través de logged_user,
        # que se instancia al crear cada ventana.
        res = True
        try:
            descripcion = self.get_info()
        except Exception, msg:  # Seguro que vengo de destroy_en_cascada
            if DEBUG:
                myprint("pclases::destroy: Excepción ignorada:\n\t%s" % msg)
            descripcion = `self`.replace("'", '"')
        puid = self.get_puid()
        try:
            self.destroySelf()
        except Exception, msg: # IntegrityError:
            res = False     # «a lo» rollback
            if DEBUG:
                myprint("pclases:destroy: Objeto no borrado\n\t%s"
                        "\n\tExcepción: %s" % (descripcion, msg))
        else:
            Auditoria.borrado(puid, usuario, ventana, descripcion)
            del self
        return res

    def copyto(self, obj, eliminar = False):
        """
        Copia en obj los datos del objeto actual que en obj sean
        nulos.
        Enlaza también las relaciones uno a muchos para evitar
        violaciones de claves ajenas, ya que antes de terminar,
        si "eliminar" es True se borra el registro de la BD.
        PRECONDICIÓN: "obj" debe ser del mismo tipo que "self".
        POSTCONDICIÓN: si "eliminar", self debe quedar eliminado.
        """
        assert type(obj) == type(self) and obj != None, \
                "Los objetos deben pertenecer a la misma clase y no ser nulos."
        for nombre_col in self.sqlmeta.columns:
            valor = getattr(obj, nombre_col)
            if valor == None or (isinstance(valor, str) and valor.strip() == ""):
                if DEBUG and VERBOSE:
                    myprint("Cambiando valor de columna %s en objeto destino."%(
                            nombre_col))
                setattr(obj, nombre_col, getattr(self, nombre_col))
        for col in self.sqlmeta.joins:
            atributo_lista = col.joinMethodName
            lista_muchos = getattr(self, atributo_lista)
            nombre_clave_ajena = repr(self.__class__).replace("'", ".").split(".")[-2] + "ID" # HACK (y de los feos)
            nombre_clave_ajena = nombre_clave_ajena[0].lower() + nombre_clave_ajena[1:]       # HACK (y de los feos)
            for propagado in lista_muchos:
                if DEBUG and VERBOSE:
                    myprint("Cambiando valor de columna %s en objeto destino." % (nombre_clave_ajena))
                    myprint("   >>> Antes: ", getattr(propagado, nombre_clave_ajena))
                setattr(propagado, nombre_clave_ajena, obj.id)
                if DEBUG and VERBOSE:
                    myprint("   >>> Después: ", getattr(propagado, nombre_clave_ajena))
        if eliminar:
            try:
                self.destroy()
            except:     # No debería. Pero aún así, me aseguro de que quede
                        # eliminado (POSTCONDICIÓN).
                self.destroy_en_cascada()

    def clone(self, *args, **kw):
        """
        Crea y devuelve un objeto idéntico al actual.
        Si se pasa algún parámetro adicional se intentará enviar
        tal cual al constructor de la clase ignorando los
        valores del objeto actual para esos parámetros.
        """
        parametros = {}
        for campo in self.sqlmeta.columns:
            valor = getattr(self, campo)
            parametros[campo] = valor
        for campo in kw:
            valor = kw[campo]
            parametros[campo] = valor
        nuevo = self.__class__(**parametros)
        return nuevo

    # PLAN: Hacer un full_clone() que además de los atributos, clone también
    # los registros relacionados.

    def get_info(self):
        """
        Devuelve información básica (str) acerca del objeto. Por ejemplo,
        si es un pedido de venta, devolverá el número de pedido, fecha y
        cliente.
        Este método se hereda por todas las clases y debería ser redefinido.
        """
        try:
            return "%s ID %d (PUID %s)"%(self.sqlmeta.table, self.id, self.get_puid())
        except AttributeError:
            try:
                return "%s ID %d (PUID %s)" % (self.sqlmeta.table, self.id,
                                               self.get_puid())
            except:
                pass
        return "Información no disponible."

    def get_puid(self):
        """
        Devuelve un identificador único (¿único? I don't think so) para toda
        la base de datos.
        Las clases pueden redefinir este método. Y de hecho deberían de, acorde
        a la lógica de negocio.
        """
        #pre = "".join([l for l in self.__class__.__name__ if l.isupper()])
        # Muncho mejore asina:
        pre = self.__class__.__name__
        ide = self.id
        puid = "%s:%d" % (pre, ide)
        return puid

    puid = property(get_puid)

    @classmethod
    def selectLike(clase, campo, expresion):
        """
        Ejecuta un .select sobre la clase buscando en el campo especificado
        la expresión recibida.
        """
        # TODO: Recibir más parámetros opcionales y combinarlos con AND en
        # el select.
        if isinstance(campo, str):
            # campoqry = getattr(clase, "q").getattr(campo)
            # HACK
            campoqry = eval(clase.__name__ + ".q." + campo)
        else:
            campoqry = campo
        res = clase.select(campoqry.contains(expresion))
        return res

    @classmethod
    def _queryAll(clase, *args, **kw):
        return clase._connection.queryAll(*args, **kw)

    @classmethod
    def _queryOne(clase, *args, **kw):
        return clase._connection.queryOne(*args, **kw)


def starter(objeto, *args, **kw):
    """
    Método que se ejecutará en el constructor de todas las
    clases persistentes.
    Inicializa el hilo y la conexión secundaria para IPC,
    así como llama al constructor de la clase padre SQLObject.
    """
    objeto.continuar_hilo = False
    objeto.notificador = notificacion.Notificacion(objeto)
    SQLObject._init(objeto, *args, **kw)
    PRPCTOO.__init__(objeto, objeto.sqlmeta.table)
    # XXX: Compatibilidad hacia atrás con SQLObject 0.6.1
    #if not hasattr(objeto, "_table"):
    #    objeto._table = objeto.sqlmeta.table
    #if not hasattr(objeto, "_SO_columnDict"):
    #    objeto._SO_columnDict = objeto.sqlmeta.columns
    #if not hasattr(objeto, "_connection"):
    #    objeto._connection = sqlhub.getConnection()
    # XXX
    objeto.make_swap()  # Al crear el objeto hago la primera caché de datos,
                        # por si acaso la ventana se demora mucho e intenta
                        # compararla antes de crearla.

    #objeto._cacheValues = False    # FIXME: Sospecho que tarde o temprano
        # tendré que desactivar las cachés locales de SQLObject.
        # Tengo que probarlo antes de poner en producción porque no sé si va
        # a resultar peor el remedio (por ineficiente) que la enfermedad
        # (que solo da problemas de vez en cuando y se resuelven con un
        # Shift+F5).
        # Mala idea. ¡Si desactivo el caché de SQLObject tengo que hacer
        # sync() después de cada operación!

def actualizar_estado_cobro_de(clase):
    """
    Actualiza el estado de confirming o pagarés dependiendo de la fecha de
    vencimiento y la del sistema. Por defecto marcará todo lo vencido como
    cobrado.
    """
    for p in clase.select(clase.q.procesado == False):
        if mx.DateTime.today() >= p.fechaVencimiento:
            if DEBUG:
                myprint("Actualizando el estado de %s..." % p.get_puid())
                try:
                    sys.stdout.flush()
                except AttributeError:
                    pass    # Consola de depuración o algo. No tiene flush.
            p.fechaCobrado = p.fechaVencimiento
            p.cobrado = p.cantidad
            p.procesado = True
            Auditoria.modificado(p, None, None,
                    "%s marcado como procesado al actualizar automáticamente"
                    " su estado de cobro." % clase.__name__)
            p.syncUpdate()
            try:
                cobros = p.cobros
            except AttributeError:
                cobros = p.pagos
            for c in cobros:
                c.fecha = p.fechaCobrado
                c.syncUpdate()
            if DEBUG:
                myprint("DONE.")
                assert not p.pendiente

## XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX

# Prefijos de códigos de artículo, partidas y demás:
PREFIJO_PARTIDACEM = "M-"
PREFIJO_ROLLO = "R"
PREFIJO_LOTECEM = "C-"
PREFIJO_BALA = "B"
PREFIJO_LOTE = "L-"
PREFIJO_PARTIDA = "P-"
PREFIJO_PARTIDACARGA = "PC"
PREFIJO_BIGBAG = "C"
PREFIJO_ROLLODEFECTUOSO = "X"
PREFIJO_BALACABLE = "Z"
PREFIJO_ROLLOC = "Y"
PREFIJO_PALE = "H"
PREFIJO_CAJA = "J"
PREFIJO_BOLSA = "K"

# Estados de pagarés/confirming
GESTION, CARTERA, DESCONTADO, IMPAGADO, COBRADO = range(5)

# Estados de validación de pedidos y ofertas
NO_VALIDABLE, VALIDABLE, PLAZO_EXCESIVO, SIN_FORMA_DE_PAGO, \
        PRECIO_INSUFICIENTE, CLIENTE_DEUDOR, SIN_CIF, SIN_CLIENTE, \
        COND_PARTICULARES, COMERCIALIZADO, BLOQUEO_FORZADO, \
        BLOQUEO_CLIENTE, SERVICIO = range(13)

# Algunos pesos HARCODED:
PESO_EMBALAJE_BALAS = 0.86
PESO_EMBALAJE_CAJAS = 0.25
PESO_EMBALAJE_BALAS_C = 0.0
PESO_EMBALAJE_BIGBAGS = 0.0
PESO_EMBALAJE_ROLLOS = None        # Según producto
PESO_EMBALAJE_ROLLOS_DEFECTUOSOS = None
PESO_EMBALAJE_ROLLOS_C = None

# VERBOSE MODE
total = 161 # egrep "^class" pclases.py | grep "(SQLObject, PRPCTOO)" | wc -l
            # Más bien grep " = print_verbose(" pclases.py | grep -v \# | wc -l
cont = 0
tiempo = time.time()

def print_verbose(cont, total, antes):
    if VERBOSE:
        cont += 1
        quedan = total - cont
        tiempo = time.time() - antes
        estimado = int(quedan * tiempo) + 1
        myprint("Cargando... (%d/%d) Tiempo restante estimado: %d seg" % (
            cont, total, estimado))
    return cont, time.time()

cont, tiempo = print_verbose(cont, total, tiempo)
##############

class Area(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

class Zona(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    areas = MultipleJoin("Area")
    comerciales = MultipleJoin("Comercial")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

class DocumentoDePago(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    formasDePago = MultipleJoin("FormaDePago")
    vencimientosValorPresupuestoAnual = MultipleJoin(
            "VencimientoValorPresupuestoAnual")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    CONTADO = "Contado"
    TRANSFERENCIA = "Transferencia bancaria"
    PAGARE = "Pagaré a la orden"
    PAGARE_NO_A_LA_ORDEN = "Pagaré no a la orden"
    CONFIRMING = "Confirming"
    CHEQUE = "Cheque"
    CARTA = "Carta de crédito"
    CARTA_VISTA = "Carta de crédito a la vista"
    DOMICILIACION = "Domiciliación bancaria"
    LUNES = "Pagaré a la orden a primer lunes del mes siguiente"

    @classmethod
    def Contado(clase):
        return clase._oblomov(clase.CONTADO)

    @classmethod
    def Transferencia(clase):
        return clase._oblomov(clase.TRANSFERENCIA)

    @classmethod
    def Pagare(clase):
        return clase._oblomov(clase.PAGARE)

    @classmethod
    def NoALaOrden(clase):
        return clase._oblomov(clase.PAGARE_NO_A_LA_ORDEN)

    @classmethod
    def Confirming(clase):
        return clase._oblomov(clase.CONFIRMING)

    @classmethod
    def Cheque(clase):
        return clase._oblomov(clase.CHEQUE)

    @classmethod
    def Carta(clase):
        return clase._oblomov(clase.CARTA)

    @classmethod
    def CartaVista(clase):
        return clase._oblomov(clase.CARTA_VISTA)

    @classmethod
    def Domiciliacion(clase):
        return clase._oblomov(clase.DOMICILIACION)

    @classmethod
    def Lunes(clase):
        return clase._oblomov(clase.LUNES)

    @classmethod
    def _oblomov(clase, strtipo):
        try:
            return clase.selectBy(documento = strtipo)[0]
        except IndexError:
            return clase(documento = strtipo)


class FormaDePago(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #------------------------- documentoDePagoID = ForeignKey('DocumentoDePago')
    pedidosVenta = MultipleJoin('PedidoVenta')
    presupuestos = MultipleJoin('Presupuesto')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def toString(self, cliente = None):
        """
        Si se especifica un cliente, usa el texto complementario de la
        forma de pago que se le pusiera en la ficha.
        """
        texto_dias = "D. F. F."
        if cliente and cliente.textoComplementarioFormaDePago:
            texto_dias = ""
        res = "%s, %d %s" % (self.documentoDePago.documento, self.plazo,
                             texto_dias)
        try:
            if cliente and cliente.textoComplementarioFormaDePago:
                res += " " + cliente.textoComplementarioFormaDePago
        except (TypeError, AttributeError):
            pass
        res = utils.eliminar_dobles_espacios(res)
        return res

    def porDefecto(cls):
        """
        Devuelve la forma de cobro por defecto.
        """
        try:
            docdefecto = DocumentoDePago.select(
                    DocumentoDePago.q.documento == "Pagaré a la orden")[0]
        except IndexError:
            docdefecto = DocumentoDePago("Pagaré a la orden")
        try:
            fdp = cls.select(AND(cls.q.plazo == 120,
                                   cls.q.documentoDePagoID == docdefecto.id
                                  ))[0]
        except IndexError:
            fdp = cls(plazo = 120, documentoDePago = docdefecto)
        return fdp

    porDefecto = classmethod(porDefecto)


class Almacen(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    albaranesSalidaServidos = MultipleJoin('AlbaranSalida',
                                   joinColumn = "almacen_origen_id")
    albaranesSalidaRecibidos = MultipleJoin('AlbaranSalida',
                                   joinColumn = "almacen_destino_id")
    articulos = MultipleJoin("Articulo")
    abonos = MultipleJoin("Abono")
    stocksAlmacen = MultipleJoin("StockAlmacen")
    centrosTrabajo = MultipleJoin("CentroTrabajo")
    stocksEspecial = MultipleJoin("StockEspecial")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    @staticmethod
    def get_almacen_principal():
        ppal = Almacen.selectBy(principal = True)
        assert ppal.count() == 1
        ppal = ppal[0]
        return ppal

    @staticmethod
    def get_almacen_principal_or_none():
        """
        Para casos muy concretos en los que no puedo permitir que una
        excepción no tratada cuelgue la aplicación (por ejemplo, con el
        default de AlbaranSalida. Si no hay almacén principal, no podría ni
        llegar a cargar pclases para crearlo).
        """
        try:
            return Almacen.get_almacen_principal()
        except:
            return None

    @staticmethod
    def get_almacen_principal_id_or_none():
        """
        Para casos muy concretos en los que no puedo permitir que una
        excepción no tratada cuelgue la aplicación (por ejemplo, con el
        default de AlbaranSalida. Si no hay almacén principal, no podría ni
        llegar a cargar pclases para crearlo).
        """
        try:
            return Almacen.get_almacen_principal().id
        except:
            return None

    def get_existencias(self, producto):
        """
        Devuelve las existencias actuales del producto en el almacén o
        None si no hay registro que los relacione.
        """
        if isinstance(producto, ProductoCompra):
            try:
                sa = StockAlmacen.select(AND(
                        StockAlmacen.q.almacenID == self.id,
                        StockAlmacen.q.productoCompraID == producto.id))[0]
            except IndexError:
                res = None
            else:
                sa.sync()
                res = sa.existencias
        elif isinstance(producto, ProductoVenta) and producto.es_especial():
            try:
                se = StockEspecial.select(AND(
                        StockEspecial.q.almacenID == self.id,
                        StockEspecial.q.camposEspecificosEspecialID
                            == producto.camposEspecificosEspecialID))[0]
            except IndexError:
                res = None
            else:
                se.sync()
                res = se.existencias
        else:
            #raise TypeException, "El parámetro debe ser un ProductoCompra."
            # Versión lenta. «premature optimization is the root of all evil»
            cantidades_en_almacen = [a.get_cantidad() for a in self.articulos
                                    if a.productoVenta == producto]
            res = sum(cantidades_en_almacen)
        return res

    def set_existencias(self, producto, existencias):
        """
        Establece las existencias actuales del producto en el almacén.
        Crea un registro si fuera necesario.
        """
        if isinstance(producto, ProductoCompra):
            try:
                sa = StockAlmacen.select(AND(
                        StockAlmacen.q.almacenID == self.id,
                        StockAlmacen.q.productoCompraID == producto.id))[0]
            except IndexError:
                sa = StockAlmacen(almacenID = self.id,
                                  productoCompra = producto,
                                  existencias = existencias)
            sa.existencias = existencias
        else:
            raise TypeError, "El parámetro debe ser un ProductoCompra."

    def crear_almacen_principal():
        """
        Crea el almacén principal en la aplicación. Primero chequea que no
        exista ya. Devuelve el almacén o None si no se pudo crear.
        """
        ppal = Almacen.get_almacen_principal_or_none()
        if not ppal:
            ppal = Almacen(nombre = "Almacén principal",
                           observaciones = "Creado automáticamente.",
                           direccion = "",
                           ciudad = "",
                           provincia = "",
                           cp = "",
                           telefono = "",
                           fax = "",
                           email = "",
                           pais = "",
                           principal = True)
        return ppal

    crear_almacen_principal = staticmethod(crear_almacen_principal)

cont, tiempo = print_verbose(cont, total, tiempo)

class PruebaTenacidad(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------------- loteID = ForeignKey('Lote')
    #---------------------------- loteCemID = ForeignKey('Lote', default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        """
        Devuelve el resultado de la prueba y la fecha.
        """
        return "Prueba de tenacidad: %.2f. Fecha %s" % (self.resultado, utils.str_fecha(self.fecha))

cont, tiempo = print_verbose(cont, total, tiempo)

class PruebaElongacion(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------------- loteID = ForeignKey('Lote')
    #---------------------------- loteCemID = ForeignKey('Lote', default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        """
        Devuelve que es una prueba de elongación, el resultado y el
        código de lote sobre el que se hizo.
        """
        return "Prueba de elongación.\n\tFecha: %s\n\tResultado: %s\n\tLote: %s" % (utils.str_fecha(self.fecha),
                                                                              utils.float2str(self.resultado),
                                                                              self.lote and self.lote.codigo or "")

cont, tiempo = print_verbose(cont, total, tiempo)

class PruebaRizo(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------------- loteID = ForeignKey('Lote')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class PruebaEncogimiento(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------------- loteID = ForeignKey('Lote')
    #---------------------------- loteCemID = ForeignKey('Lote', default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class PruebaGrasa(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------------- loteID = ForeignKey('Lote')
    #---------------------------- loteCemID = ForeignKey('Lote', default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class PruebaTitulo(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------------- loteID = ForeignKey('Lote')
    #---------------------------- loteCemID = ForeignKey('Lote', default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class PruebaHumedad(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #-------------------------------------------- loteCemID = ForeignKey('Lote')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class PruebaGramaje(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- partidaID = ForeignKey('Partida')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class PruebaLongitudinal(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- partidaID = ForeignKey('Partida')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class PruebaAlargamientoLongitudinal(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- partidaID = ForeignKey('Partida')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class PruebaTransversal(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- partidaID = ForeignKey('Partida')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class PruebaAlargamientoTransversal(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- partidaID = ForeignKey('Partida')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class PruebaCompresion(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- partidaID = ForeignKey('Partida')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class PruebaPerforacion(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- partidaID = ForeignKey('Partida')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class PruebaEspesor(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- partidaID = ForeignKey('Partida')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class PruebaPermeabilidad(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- partidaID = ForeignKey('Partida')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class PruebaPoros(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- partidaID = ForeignKey('Partida')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class PruebaPiramidal(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- partidaID = ForeignKey('Partida')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class CacheExistencias:
    def get_existencias(cls, producto, fecha, almacen):
        """
        Devuelve las existencias en bultos en la fecha dada y el almacén
        especificado.
        Si no existe devuelve None.
        """
        rec = cls.get_registro(producto, fecha, almacen)
        if rec:
            return rec.bultos
        return None

    def get_stock(cls, producto, fecha, almacen):
        """
        Devuelve las existencias en las unidades del producto en la fecha dada
        y el almacén especificado.
        Si no existe devuelve None.
        """
        rec = cls.get_registro(producto, fecha, almacen)
        if rec:
            return rec.cantidad
        return None

    def get_registro(cls, producto, fecha, almacen):
        """
        Devuelve el registro de caché relacionado con el producto en la fecha
        dada y el almacén especificado.
        Si no existe devuelve None.
        """
        recs = cls.select(AND(cls.q.productoVentaID == producto.id,
                                cls.q.fecha == fecha,
                                cls.q.almacenID == almacen.id))
        if recs.count() == 1:
            return recs[0]
        elif recs.count > 1:
            # Error de coherencia. Más de un reg. de caché. Borro todos.
            for r in recs:
                r.destroySelf() #¿Para qué auditarlo? Uso el destroy de sqlobj.
            return None
        else:   # recs.count() == 0
            return None

    def actualizar(cls, producto, bultos, cantidad, fecha, almacen):
        """
        Actualizar el registro de caché para el producto, fecha y almacén.
        Si existen varios elimina los que sobren. Si no existe lo crea. Y si
        solo existe uno, lo actualiza y sincroniza.
        """
        cache = cls.select(AND(cls.q.productoVentaID == producto.id,
                                 cls.q.fecha == fecha,
                                 cls.q.almacenID == almacen.id))
        if cache.count() == 1:
            cache = cache[0]
        else:   # cache.count() > 1 or cache.count() == 0:
            for c in cache:
                c.destroySelf()
            cache = cls(productoVenta = producto,
                          fecha = fecha,
                          almacen = almacen,
                          cantidad = 0,
                          bultos = 0)
        cache.cantidad = cantidad
        cache.bultos = bultos
        cache.syncUpdate()

    def get_fechas_cacheadas(cls, producto = None):
        """
        Devuelve una lista de fechas que ya han sido cacheadas. Si se
        especifica producto, devuelve las fechas cacheadas solo para ese
        producto.
        OJO: Solo va a mirar en los cachés del tipo de existencias por las
        que se pregunta dependiendo de la cls invocadora: totales, A, B o C.
        """
        fechas = []
        if producto:
            rs = cls.select(cls.q.productoVentaID == producto.id)
        else:
            rs = cls.select()
        for r in rs:
            fecha = r.fecha
            if fecha not in fechas:
                fechas.append(fecha)
        fechas.sort()
        return fechas

    get_existencias = classmethod(get_existencias)
    get_stock = classmethod(get_stock)
    get_registro = classmethod(get_registro)
    actualizar = classmethod(actualizar)
    get_fechas_cacheadas = classmethod(get_fechas_cacheadas)


class HistorialExistencias(SQLObject, PRPCTOO, CacheExistencias):
    class sqlmeta:
        fromDatabase = True
    #----------------------------- productoVentaID = ForeignKey('ProductoVenta')
    #----------------------------------------- almacenID = ForeignKey("Almacen")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def test(self, almacen = None):
        """
        Comprueba que la cantidad del registro es correcta.
        Para hacerlo busca las existencias del producto relacionado en la
        fecha actual, resta la producción entre esa fecha y la del registro,
        suma las ventas (y consumos, si es fibra) del mismo periodo y
        compara la cantidad resultante con la almacenada.
        (Es decir, vuelve atrás en el tiempo partiendo de las existencias
        actuales, que se supone que son correctas -o al menos más fiables
        que las cacheadas, que pueden partir de otras existencias cacheadas
        igual de erróneas-).
        Devuelve True/False y las cantidades halladas, en bultos primero y en
        cantidad del SI a continuación.
        ACTUALIZACIÓN: La caché cuenta existencias HASTA la fecha que guarda,
        incluida esta última. Para contar hacia atrás, ese día completo hay
        que excluirlo, ya que las cantidades deben coincidir exactamente a
        las 23:59:59 del día "self.fecha" y 00:00:00 del día
        "self.fecha + mx.DateTime.oneDay", por tanto el test debe sumar desde
        el self.fecha más un día (es decir, desde las 00:00) hasta la fecha
        actual; de otro modo las ventas, producciones y demás del día en
        cuestión (self.fecha) se estarían contando de más.
        #### Versión con ampliación almacenes:
        Si almacen != None comprueba las existencias solo para ese almacén.
        En otro caso lo hace para el total de todos los almacenes.
        """
        hoy = mx.DateTime.localtime()
        fecha = self.fecha + mx.DateTime.oneDay
        ##### BULTOS #####
        existencias_base = self.productoVenta.get_existencias(
            contar_defectuosos = True,
            almacen = almacen) # Cantidad en bultos
        if not almacen or almacen.principal:
            # TODO: ¿Qué pasaría al cambiar de almacén principal?
            produccion_bultos = self.productoVenta.buscar_produccion_bultos(
                fecha,
                hoy) # Producción entre fecha base y fecha del registro
        else:
            produccion_bultos = 0
        ventas_bultos = self.productoVenta.buscar_ventas_bultos(
            fecha,
            hoy,
            almacen = almacen) # Ventas en bultos entre fechas
        if not almacen or almacen.principal:
            consumos_bultos = self.productoVenta.buscar_consumos_bultos(
                fecha,
                hoy) # Consumos en bultos entre fechas
        else:
            consumos_bultos = 0
        total_bultos = (   existencias_base
                        - produccion_bultos
                        +     ventas_bultos
                        +   consumos_bultos)
        if DEBUG:
            myprint("[", self.productoVenta.id, "]", self.productoVenta.descripcion)
            myprint("\tBULTOS:", utils.str_fecha(hoy), existencias_base)
            myprint("\tPRODUCCIÓN:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "-", produccion_bultos)
            myprint("\tCONSUMOS:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "+", consumos_bultos)
            myprint("\tVENTAS:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "+", ventas_bultos)
            myprint("\t\t\t", "=", total_bultos)
            myprint("\tCACHEADO", utils.str_fecha(self.fecha), ":", self.bultos, " - ", self.bultos == total_bultos and "OK" or "KO")
        ##### CANTIDAD #####
        stock_base = self.productoVenta.get_stock(
            contar_defectuosos = True,
            almacen = almacen)    # Cantidad en m²/kg
        if not almacen or almacen.principal:
            produccion_cantidad=self.productoVenta.buscar_produccion_cantidad(
                fecha,
                hoy)    # Producción entre fecha base y
                        # fecha del registro en m²/kg
        else:
            produccion_cantidad = 0
        ventas_cantidad = self.productoVenta.buscar_ventas_cantidad(
            fecha,
            hoy,
            almacen = almacen) # Ventas en cantidad entre fechas
        if not almacen or almacen.principal:
            consumos_cantidad = self.productoVenta.buscar_consumos_cantidad(
                fecha,
                hoy)  # Consumos en cantidad entre fechas
        else:
            consumos_cantidad = 0
        total_cantidad = (           stock_base
                          - produccion_cantidad
                          +     ventas_cantidad
                          +   consumos_cantidad)
        if DEBUG:
            myprint("[", self.productoVenta.id, "]", self.productoVenta.descripcion)
            myprint("\tCANTIDAD:", utils.str_fecha(hoy), stock_base)
            myprint("\tPRODUCCIÓN:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "-", produccion_cantidad)
            myprint("\tCONSUMOS:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "+", consumos_cantidad)
            myprint("\tVENTAS:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "+", ventas_cantidad)
            myprint("\t\t\t", "=", total_cantidad)
            myprint("\tCACHEADO", utils.str_fecha(self.fecha), ":", self.cantidad, " - ", self.cantidad == total_cantidad and "OK" or "KO")
        return (total_bultos == self.bultos
                and round(total_cantidad, 2) == round(self.cantidad, 2),
                total_bultos,
                total_cantidad)

cont, tiempo = print_verbose(cont, total, tiempo)

class HistorialExistenciasA(SQLObject, PRPCTOO, CacheExistencias):
    class sqlmeta:
        fromDatabase = True
    #----------------------------- productoVentaID = ForeignKey('ProductoVenta')
    #----------------------------------------- almacenID = ForeignKey("Almacen")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def test(self, almacen = None):
        """
        Comprueba que la cantidad del registro es correcta.
        Para hacerlo busca las existencias del producto relacionado en la
        fecha actual, resta la producción entre esa fecha y la del registro,
        suma las ventas (y consumos, si es fibra) del mismo periodo y
        compara la cantidad resultante con la almacenada.
        (Es decir, vuelve atrás en el tiempo partiendo de las existencias
        actuales, que se supone que son correctas -o al menos más fiables
        que las cacheadas, que pueden partir de otras existencias cacheadas
        igual de erróneas-).
        Devuelve True/False y las cantidades halladas, en bultos primero y en
        cantidad del SI a continuación.
        ACTUALIZACIÓN: La caché cuenta existencias HASTA la fecha que guarda,
        incluida esta última. Para contar hacia atrás, ese día completo hay
        que excluirlo, ya que las cantidades deben coincidir exactamente a
        las 23:59:59 del día "self.fecha" y 00:00:00 del día
        "self.fecha + mx.DateTime.oneDay", por tanto el test debe sumar desde
        el self.fecha más un día (es decir, desde las 00:00) hasta la fecha
        actual; de otro modo las ventas, producciones y demás del día en
        cuestión (self.fecha) se estarían contando de más.
        #### Versión con ampliación almacenes:
        Si almacen != None comprueba las existencias solo para ese almacén.
        En otro caso lo hace para el total de todos los almacenes.
        """
        hoy = mx.DateTime.localtime()
        fecha = self.fecha + mx.DateTime.oneDay
        ##### BULTOS #####
        existencias_base = self.productoVenta.get_existencias_A(
            contar_defectuosos = True,
            almacen = almacen) # Cantidad en bultos
        if not almacen or almacen.principal:
            # TODO: ¿Qué pasaría al cambiar de almacén principal?
            produccion_bultos = self.productoVenta.buscar_produccion_bultos(
                fecha,
                hoy) # Producción entre fecha base y fecha del registro
        else:
            produccion_bultos = 0
        ventas_bultos = self.productoVenta.buscar_ventas_bultos(
            fecha,
            hoy,
            almacen = almacen) # Ventas en bultos entre fechas
        if not almacen or almacen.principal:
            consumos_bultos = self.productoVenta.buscar_consumos_bultos(
                fecha,
                hoy) # Consumos en bultos entre fechas
        else:
            consumos_bultos = 0
        total_bultos = (   existencias_base
                        - produccion_bultos
                        +     ventas_bultos
                        +   consumos_bultos)
        if DEBUG:
            myprint("[", self.productoVenta.id, "]", self.productoVenta.descripcion )
            myprint("\tBULTOS:", utils.str_fecha(hoy), existencias_base)
            myprint("\tPRODUCCIÓN:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "-", produccion_bultos)
            myprint("\tCONSUMOS:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "+", consumos_bultos)
            myprint("\tVENTAS:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "+", ventas_bultos)
            myprint("\t\t\t", "=", total_bultos)
            myprint("\tCACHEADO", utils.str_fecha(self.fecha), ":", self.bultos, " - ", self.bultos == total_bultos and "OK" or "KO")
        ##### CANTIDAD #####
        stock_base = self.productoVenta.get_stock_A(
            contar_defectuosos = True,
            almacen = almacen)    # Cantidad en m²/kg
        if not almacen or almacen.principal:
            produccion_cantidad=self.productoVenta.buscar_produccion_cantidad(
                fecha,
                hoy)    # Producción entre fecha base y
                        # fecha del registro en m²/kg
        else:
            produccion_cantidad = 0
        ventas_cantidad = self.productoVenta.buscar_ventas_cantidad(
            fecha,
            hoy,
            almacen = almacen) # Ventas en cantidad entre fechas
        if not almacen or almacen.principal:
            consumos_cantidad = self.productoVenta.buscar_consumos_cantidad(
                fecha,
                hoy)  # Consumos en cantidad entre fechas
        else:
            consumos_cantidad = 0
        total_cantidad = (           stock_base
                          - produccion_cantidad
                          +     ventas_cantidad
                          +   consumos_cantidad)
        if DEBUG:
            myprint("[", self.productoVenta.id, "]", self.productoVenta.descripcion)
            myprint("\tCANTIDAD:", utils.str_fecha(hoy), stock_base)
            myprint("\tPRODUCCIÓN:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "-", produccion_cantidad)
            myprint("\tCONSUMOS:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "+", consumos_cantidad)
            myprint("\tVENTAS:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "+", ventas_cantidad)
            myprint("\t\t\t", "=", total_cantidad)
            myprint("\tCACHEADO", utils.str_fecha(self.fecha), ":", self.cantidad, " - ", self.cantidad == total_cantidad and "OK" or "KO")
        return (total_bultos == self.bultos
                and round(total_cantidad, 2) == round(self.cantidad, 2),
                total_bultos,
                total_cantidad)

cont, tiempo = print_verbose(cont, total, tiempo)

class HistorialExistenciasB(SQLObject, PRPCTOO, CacheExistencias):
    class sqlmeta:
        fromDatabase = True
    #----------------------------- productoVentaID = ForeignKey('ProductoVenta')
    #----------------------------------------- almacenID = ForeignKey("Almacen")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def test(self, almacen = None):
        """
        Comprueba que la cantidad del registro es correcta.
        Para hacerlo busca las existencias del producto relacionado en la
        fecha actual, resta la producción entre esa fecha y la del registro,
        suma las ventas (y consumos, si es fibra) del mismo periodo y
        compara la cantidad resultante con la almacenada.
        (Es decir, vuelve atrás en el tiempo partiendo de las existencias
        actuales, que se supone que son correctas -o al menos más fiables
        que las cacheadas, que pueden partir de otras existencias cacheadas
        igual de erróneas-).
        Devuelve True/False y las cantidades halladas, en bultos primero y en
        cantidad del SI a continuación.
        ACTUALIZACIÓN: La caché cuenta existencias HASTA la fecha que guarda,
        incluida esta última. Para contar hacia atrás, ese día completo hay
        que excluirlo, ya que las cantidades deben coincidir exactamente a
        las 23:59:59 del día "self.fecha" y 00:00:00 del día
        "self.fecha + mx.DateTime.oneDay", por tanto el test debe sumar desde
        el self.fecha más un día (es decir, desde las 00:00) hasta la fecha
        actual; de otro modo las ventas, producciones y demás del día en
        cuestión (self.fecha) se estarían contando de más.
        #### Versión con ampliación almacenes:
        Si almacen != None comprueba las existencias solo para ese almacén.
        En otro caso lo hace para el total de todos los almacenes.
        """
        hoy = mx.DateTime.localtime()
        fecha = self.fecha + mx.DateTime.oneDay
        ##### BULTOS #####
        existencias_base = self.productoVenta.get_existencias_B(
            contar_defectuosos = True,
            almacen = almacen) # Cantidad en bultos
        if not almacen or almacen.principal:
            # TODO: ¿Qué pasaría al cambiar de almacén principal?
            produccion_bultos = self.productoVenta.buscar_produccion_bultos(
                fecha,
                hoy) # Producción entre fecha base y fecha del registro
        else:
            produccion_bultos = 0
        ventas_bultos = self.productoVenta.buscar_ventas_bultos(
            fecha,
            hoy,
            almacen = almacen) # Ventas en bultos entre fechas
        if not almacen or almacen.principal:
            consumos_bultos = self.productoVenta.buscar_consumos_bultos(
                fecha,
                hoy) # Consumos en bultos entre fechas
        else:
            consumos_bultos = 0
        total_bultos = (   existencias_base
                        - produccion_bultos
                        +     ventas_bultos
                        +   consumos_bultos)
        if DEBUG:
            myprint("[", self.productoVenta.id, "]", self.productoVenta.descripcion )
            myprint("\tBULTOS:", utils.str_fecha(hoy), existencias_base)
            myprint("\tPRODUCCIÓN:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "-", produccion_bultos)
            myprint("\tCONSUMOS:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "+", consumos_bultos)
            myprint("\tVENTAS:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "+", ventas_bultos)
            myprint("\t\t\t", "=", total_bultos)
            myprint("\tCACHEADO", utils.str_fecha(self.fecha), ":", self.bultos, " - ", self.bultos == total_bultos and "OK" or "KO")
        ##### CANTIDAD #####
        stock_base = self.productoVenta.get_stock_B(
            contar_defectuosos = True,
            almacen = almacen)    # Cantidad en m²/kg
        if not almacen or almacen.principal:
            produccion_cantidad=self.productoVenta.buscar_produccion_cantidad(
                fecha,
                hoy)    # Producción entre fecha base y
                        # fecha del registro en m²/kg
        else:
            produccion_cantidad = 0
        ventas_cantidad = self.productoVenta.buscar_ventas_cantidad(
            fecha,
            hoy,
            almacen = almacen) # Ventas en cantidad entre fechas
        if not almacen or almacen.principal:
            consumos_cantidad = self.productoVenta.buscar_consumos_cantidad(
                fecha,
                hoy)  # Consumos en cantidad entre fechas
        else:
            consumos_cantidad = 0
        total_cantidad = (           stock_base
                          - produccion_cantidad
                          +     ventas_cantidad
                          +   consumos_cantidad)
        if DEBUG:
            myprint("[", self.productoVenta.id, "]", self.productoVenta.descripcion)
            myprint("\tCANTIDAD:", utils.str_fecha(hoy), stock_base)
            myprint("\tPRODUCCIÓN:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "-", produccion_cantidad)
            myprint("\tCONSUMOS:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "+", consumos_cantidad)
            myprint("\tVENTAS:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "+", ventas_cantidad)
            myprint("\t\t\t", "=", total_cantidad)
            myprint("\tCACHEADO", utils.str_fecha(self.fecha), ":", self.cantidad, " - ", self.cantidad == total_cantidad and "OK" or "KO")
        return (total_bultos == self.bultos
                and round(total_cantidad, 2) == round(self.cantidad, 2),
                total_bultos,
                total_cantidad)

cont, tiempo = print_verbose(cont, total, tiempo)

class HistorialExistenciasC(SQLObject, PRPCTOO, CacheExistencias):
    class sqlmeta:
        fromDatabase = True
    #----------------------------- productoVentaID = ForeignKey('ProductoVenta')
    #----------------------------------------- almacenID = ForeignKey("Almacen")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def test(self, almacen = None):
        """
        Comprueba que la cantidad del registro es correcta.
        Para hacerlo busca las existencias del producto relacionado en la
        fecha actual, resta la producción entre esa fecha y la del registro,
        suma las ventas (y consumos, si es fibra) del mismo periodo y
        compara la cantidad resultante con la almacenada.
        (Es decir, vuelve atrás en el tiempo partiendo de las existencias
        actuales, que se supone que son correctas -o al menos más fiables
        que las cacheadas, que pueden partir de otras existencias cacheadas
        igual de erróneas-).
        Devuelve True/False y las cantidades halladas, en bultos primero y en
        cantidad del SI a continuación.
        ACTUALIZACIÓN: La caché cuenta existencias HASTA la fecha que guarda,
        incluida esta última. Para contar hacia atrás, ese día completo hay
        que excluirlo, ya que las cantidades deben coincidir exactamente a
        las 23:59:59 del día "self.fecha" y 00:00:00 del día
        "self.fecha + mx.DateTime.oneDay", por tanto el test debe sumar desde
        el self.fecha más un día (es decir, desde las 00:00) hasta la fecha
        actual; de otro modo las ventas, producciones y demás del día en
        cuestión (self.fecha) se estarían contando de más.
        #### Versión con ampliación almacenes:
        Si almacen != None comprueba las existencias solo para ese almacén.
        En otro caso lo hace para el total de todos los almacenes.
        """
        hoy = mx.DateTime.localtime()
        fecha = self.fecha + mx.DateTime.oneDay
        ##### BULTOS #####
        existencias_base = self.productoVenta.get_existencias_C(
            contar_defectuosos = True,
            almacen = almacen) # Cantidad en bultos
        if not almacen or almacen.principal:
            # TODO: ¿Qué pasaría al cambiar de almacén principal?
            produccion_bultos = self.productoVenta.buscar_produccion_bultos(
                fecha,
                hoy) # Producción entre fecha base y fecha del registro
        else:
            produccion_bultos = 0
        ventas_bultos = self.productoVenta.buscar_ventas_bultos(
            fecha,
            hoy,
            almacen = almacen) # Ventas en bultos entre fechas
        if not almacen or almacen.principal:
            consumos_bultos = self.productoVenta.buscar_consumos_bultos(
                fecha,
                hoy) # Consumos en bultos entre fechas
        else:
            consumos_bultos = 0
        total_bultos = (   existencias_base
                        - produccion_bultos
                        +     ventas_bultos
                        +   consumos_bultos)
        if DEBUG:
            myprint("[", self.productoVenta.id, "]", self.productoVenta.descripcion )
            myprint("\tBULTOS:", utils.str_fecha(hoy), existencias_base)
            myprint("\tPRODUCCIÓN:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "-", produccion_bultos)
            myprint("\tCONSUMOS:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "+", consumos_bultos)
            myprint("\tVENTAS:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "+", ventas_bultos)
            myprint("\t\t\t", "=", total_bultos)
            myprint("\tCACHEADO", utils.str_fecha(self.fecha), ":", self.bultos, " - ", self.bultos == total_bultos and "OK" or "KO")
        ##### CANTIDAD #####
        stock_base = self.productoVenta.get_stock_C(
            contar_defectuosos = True,
            almacen = almacen)    # Cantidad en m²/kg
        if not almacen or almacen.principal:
            produccion_cantidad=self.productoVenta.buscar_produccion_cantidad(
                fecha,
                hoy)    # Producción entre fecha base y
                        # fecha del registro en m²/kg
        else:
            produccion_cantidad = 0
        ventas_cantidad = self.productoVenta.buscar_ventas_cantidad(
            fecha,
            hoy,
            almacen = almacen) # Ventas en cantidad entre fechas
        if not almacen or almacen.principal:
            consumos_cantidad = self.productoVenta.buscar_consumos_cantidad(
                fecha,
                hoy)  # Consumos en cantidad entre fechas
        else:
            consumos_cantidad = 0
        total_cantidad = (           stock_base
                          - produccion_cantidad
                          +     ventas_cantidad
                          +   consumos_cantidad)
        if DEBUG:
            myprint("[", self.productoVenta.id, "]", self.productoVenta.descripcion)
            myprint("\tCANTIDAD:", utils.str_fecha(hoy), stock_base)
            myprint("\tPRODUCCIÓN:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "-", produccion_cantidad)
            myprint("\tCONSUMOS:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "+", consumos_cantidad)
            myprint("\tVENTAS:", utils.str_fecha(fecha), "->", utils.str_fecha(hoy), "+", ventas_cantidad)
            myprint("\t\t\t", "=", total_cantidad)
            myprint("\tCACHEADO", utils.str_fecha(self.fecha), ":", self.cantidad, " - ", self.cantidad == total_cantidad and "OK" or "KO")
        return (total_bultos == self.bultos
                and round(total_cantidad, 2) == round(self.cantidad, 2),
                total_bultos,
                total_cantidad)

cont, tiempo = print_verbose(cont, total, tiempo)

class Silo(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    cargasSilo = MultipleJoin('CargaSilo')
    lineasDeCompra = MultipleJoin('LineaDeCompra')
    consumos = MultipleJoin('Consumo')
    PDPConfSilos = MultipleJoin("PDPConfSilo")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        """
        Devuelve número de silo, carga y capacidad.
        """
        string = "Silo ID %d. Nombre: %s. Capacidad: %s. Carga actual: %s" % (self.id,
                                                                              self.nombre,
                                                                              utils.float2str(self.capacidad, 1),
                                                                              utils.float2str(self.ocupado, 1))
        return string

    def get_ocupado(self):
        """
        Devuelve la carga actual del silo a partir de
        las cargas no consumidas del mismo.
        No distingue entre los productos. Devuelve
        siempre un float con el total absoluto.
        NO COMPRUEBA QUE SE HAYA SUPERADO LA CAPACIDAD DEL SILO.
        """
        # Para calcular las cargas consumidas hay que:
        # 1.- Sumar las cantidades de las cargas del silo.
        # 2.- Sumar las cantidades de los consumos del silo.
        # 3.- Devolver la diferencia.
        cargas = CargaSilo.select(CargaSilo.q.siloID == self.id)
        if cargas.count():
            cantidad_cargada = cargas.sum("cantidad")
        else:
            cantidad_cargada = 0
        consumos = Consumo.select(Consumo.q.siloID == self.id)
        if consumos.count():
            cantidad_consumida = consumos.sum("cantidad")
        else:
            cantidad_consumida = 0
        # assert cantidad_cargada - cantidad_consumida <= self.capacidad
        return cantidad_cargada - cantidad_consumida

    def get_ocupacion(self):
        """
        Ligeramente distinto al método get_ocupado.
        Este devuelve un diccionario de productos y
        cantidad restante en el silo del mismo. La
        suma de los valores del diccionario debería
        ser igual a lo devuelto por get_ocupacion.
        OJO: Orden muy alto (como mínimo, O(2*n)
        más el orden de la consulta en el motor de la BD).
        """
        # 1.- Obtiene por orden de fecha todas las cargas del silo, separadas
        #     por producto.
        # 2.- Obtiene todos los consumos del silo, también separados por
        #     producto.
        # 3.- Devuelve el diccionario con el sumatorio de cargas - sumatorio
        #     de consumos pero filtrando aquellos productos que tengan
        #     cantidad real en el silo (es decir, cantidad > 0).
        cargas = CargaSilo._connection.queryAll("""
            SELECT carga_silo.producto_compra_id, SUM(carga_silo.cantidad)
              FROM carga_silo
             WHERE carga_silo.silo_id = %d
             GROUP BY carga_silo.producto_compra_id """ % (self.id))
        consumos = Consumo._connection.queryAll("""
            SELECT consumo.producto_compra_id, SUM(consumo.cantidad)
              FROM consumo
             WHERE consumo.silo_id = %d
             GROUP BY consumo.producto_compra_id """ % (self.id))
        dic_productos = {}
        for idproducto, carga in cargas:
            producto = ProductoCompra.get(idproducto)
            dic_productos[producto] = carga
        for idproducto, consumo in consumos:
            producto = ProductoCompra.get(idproducto)
            if producto not in dic_productos:
                dic_productos[producto] = -consumo
            else:
                dic_productos[producto] -= consumo
        for producto in dic_productos.keys():
            if dic_productos[producto] <= 0:
                dic_productos.pop(producto)
        return dic_productos

    def _get_ocupacion(self):
        """
        Igual que get_ocupacion pero devuelve todos los productos que
        se hayan cargado o consumido alguna vez. Útil únicamente para
        depuración.
        """
        # 1.- Obtiene por orden de fecha todas las cargas del silo, separadas
        #     por producto.
        # 2.- Obtiene todos los consumos del silo, también separados por
        #     producto.
        # 3.- Devuelve el diccionario con el sumatorio de cargas - sumatorio
        #     de consumos.
        cargas = CargaSilo._connection.queryAll("""
            SELECT carga_silo.producto_compra_id, SUM(carga_silo.cantidad)
              FROM carga_silo
             WHERE carga_silo.silo_id = %d
             GROUP BY carga_silo.producto_compra_id """ % (self.id))
        consumos = Consumo._connection.queryAll("""
            SELECT consumo.producto_compra_id, SUM(consumo.cantidad)
              FROM consumo
             WHERE consumo.silo_id = %d
             GROUP BY consumo.producto_compra_id """ % (self.id))
        dic_productos = {}
        for idproducto, carga in cargas:
            producto = ProductoCompra.get(idproducto)
            dic_productos[producto] = carga
        for idproducto, consumo in consumos:
            producto = ProductoCompra.get(idproducto)
            if producto not in dic_productos:
                dic_productos[producto] = -consumo
            else:
                dic_productos[producto] -= consumo
        return dic_productos

    def consumir(self, cantidad, parte_de_produccion = None):
        """
        Consume (descarga) la cantidad recibida por
        parámetro del silo.
        El producto elegido para ello irá en función
        de las cargas del mismo.
        Devuelve un diccionario de productos y cantidad consumida de los mismos.
        Por tanto, crea tantos consumos de cada producto
        del silo (comenzando por los más antiguos, los que
        están en el fondo, por gravedad) como necesite hasta
        consumir lo requerido o dejar el silo vacío.
        ¡OJO! Actualiza las cantidades de los productos de compra.
        """
        # Para consumir del silo:
        # Mientras no esté vacío o cantidad > 0:
        # 1.- Se determina el producto más antiguo del silo.
        # 2.- Se crea un registro consumo entre el producto de compra y parte
        #     de produccion con cantidad = min(cantidad, cantidad_de_producto)
        # 3.- Se actualiza cantidad a cantidad - consumo.cantidad.
        # 4.- Se devuelve la suma de las cantidades de los consumos creados.
        #######################################################################
        # He descubierto un par de fallos por temas de paralelismo y
        # concurrencia.
        # Por ejemplo. Al producir se leen las existencias de la granza,
        # pongamos x.
        # Al mismo tiempo que el parte de producción está abierto, se abre un
        # albarán de entrada y se recibe una cantidad y del mismo producto.
        # Justo en ese instante el producto tiene como existencias x+y.
        # Se fabrica una bala que consume una cantidad z del mismo producto.
        # Las existencias deberían pasar a ser x+y-z, sin embargo el parte de
        # producción guarda como existencias en caché x, así que actualiza la
        # cantidad a x-z. Como los partes de producción *siempre* están
        # abiertos todo ha resultado en que prácticamente no se ha
        # contabilizado ninguna entrada de granza desde que se pusieron en
        # marcha los consumos automáticos de materia prima.
        # SOLUCIÓN: Sincronizar el producto (y el silo en sí, ya que estamos)
        # antes de cada consumo.
        #######################################################################
        self.sync()
        res = {}
        cantidad_consumida_total = 0
        cantidad_ocupada = self.get_ocupado()
        while int(cantidad_ocupada) > 0 and int(cantidad) > 0:
            carga_antigua = self.get_carga_mas_antigua()
            # myprint("All I want", carga_antigua)
            producto_compra = carga_antigua.productoCompra
            producto_compra.sync()
            try:
                cantidad_de_producto = carga_antigua.cantidad - carga_antigua.consumido
            except AssertionError:  # Por haber un consumo con más cosumido
                                    # que cargado. Quitar cuando arregle el
                                    # FIXME que viene a continuación.
                cantidad_de_producto = 0.0
            # Hay un desfase entre las cantidades cargadas por consumo y las
            # consumidas. En get_carga_mas_antigua devuelve una carga con un
            # resto por consumir, pero la ver la parte consumida desde el
            # objeto carga, devuelve que esa carga está completamente
            # consumida.
            # FIXME: Para solucionarlo, si cantidad_de_producto (que es lo que
            # vamos a consumir del silo) es 0.0, a la carga antigua le pongo
            # que se ha consumido por completo y vuelvo a iterar (la carga
            # mas antigua entonces será otra).
            # Para que esa carga aparezca como consumida por completo lo que
            # voy a hacer es decrementar la cantidad  cargada (no hay riesgo
            # de que se modifique el albarán) en 10 kilos hasta que se igualen
            # ambas cantidades. El cambio es meramente de cara a las
            # consultas. Internamente no había mucha incoherencia.
            # Sin embargo no es lo correcto y al mirar las cargas desde la
            # ventana de silos aparecerían cantidades erróneas. Por poco,
            # pero erróneas (difieren de la de los albaranes de la carga).
            # Por eso, ARRÉGLAME CUANTO ANTES. (Es urgente, por eso lo del
            # chapú.)
            if int(cantidad_de_producto) == 0:
                carga_antigua.cantidad -= 10.0
                carga_antigua.syncUpdate()
                continue
            if DEBUG:
                try:
                    myprint(" --->", carga_antigua.cantidad, carga_antigua.consumido, cantidad_de_producto)
                except AssertionError, msg:
                    myprint(" ---> AssertionError", msg)
            cantidad_consumida = min(cantidad_de_producto, cantidad)
            #myprint("¡Hola hombre cangrejo!", cantidad_consumida,
            #        cantidad_de_producto, cantidad)
            consumo = Consumo(parteDeProduccion = parte_de_produccion,
                              productoCompra = producto_compra,
                              actualizado = True,
                              antes = cantidad_ocupada,
                              despues = cantidad_ocupada - cantidad_consumida,
                              cantidad = cantidad_consumida,
                              siloID = self.id)
            consumo.productoCompra.existencias -= consumo.cantidad
            consumo.productoCompra.add_existencias(-consumo.cantidad)
            if consumo.productoCompra not in res:
                res[consumo.productoCompra] = consumo.cantidad
            else:
                res[consumo.productoCompra] += consumo.cantidad
            consumo.productoCompra.syncUpdate()
            cantidad_ocupada -= cantidad_consumida  # Para optimizar, evito hacer más llamadas a get_ocupado()
            cantidad -= cantidad_consumida
            cantidad_consumida_total += cantidad_consumida
        return res

    def get_carga_mas_antigua(self):
        """
        Devuelve el registro cargaSilo efectivo (con algún
        resto o cantidad > 0 en el silo) más antiguo.
        Si no se encuentra (presumiblemente porque el silo
        esté vacío), devuelve None.
        """
        # cargas = self.cargasSilo[:]
        # cargas.sort(func_orden_cargas_fecha)
        # cargas.reverse()
        cargas = CargaSilo.select(CargaSilo.q.siloID == self.id,
                                  orderBy = "-fechaCarga")
        consumos = Consumo.select(Consumo.q.siloID == self.id)
        if cargas.count() > 0:
            cantidad_cargada = cargas.sum("cantidad")
        else:
            cantidad_cargada = 0
        if consumos.count() > 0:
            cantidad_consumida = consumos.sum("cantidad")
        else:
            cantidad_consumida = 0
        cargado = cantidad_cargada - cantidad_consumida
        carga_mas_antigua = None
        if DEBUG: myprint(cargado)
        if int(cargado) > 0:
            for carga_mas_antigua in cargas:
                cargado -= carga_mas_antigua.cantidad
                if DEBUG: myprint(" -> ", cargado)
                if  int(cargado) <= 0:
                    break
        if DEBUG: myprint(" --> ", carga_mas_antigua and carga_mas_antigua.cantidad or " None")
        return carga_mas_antigua

    def cargar(self, producto, cantidad, fecha = None, ldc = None):
        """
        Realiza una carga del producto en el silo. La
        cantidad debe ser en kilos. Si no se pasa una fecha,
        se usa la actual del sistema.
        NO COMPRUEBA QUE NO SE SOBREPASE LA CAPACIDAD DEL SILO.
        ¡OJO! ACTUALIZA LA CANTIDAD DEL PRODUCTO DE COMPRA.
        pychecker dice: ldc no se usa. Y es verdad. ¿Qué hace ahí?
        """
        if not fecha:
            fecha = mx.DateTime.localtime()
        carga_silo = CargaSilo(silo = self,  # @UnusedVariable
                               productoCompra = producto,
                               fechaCarga = fecha,
                               cantidad = cantidad)
        producto.existencias += cantidad
        return cantidad

    def ajustar(self, cantidad, ajustar_producto_compra = True):
        """
        Ajusta la carga del silo a la cantidad recibida.
        Para ello, de la capacidad ocupada por cada producto,
        añade o resta una parte proporcional hasta quedar
        la cantidad indicada.
        Devuelve la carga final del silo ó -1 si no se pudo ajustar.
        POSTCONDICIÓN: La carga final siempre será x | 0<=x<=capacidad.
        ¡OJO! ACTUALIZA LAS EXISTENCIAS DEL PRODUCTO COMPRA a no ser
        que se indique lo contrario.
        """
        # 1.- Obtener las últimas cargas con cantidad efectiva en el silo > 0.
        # 2.- Restar a la cantidad recibida la cantidad actual del silo.
        # 3.- Dividir la cantidad resultante entre el número de cargas efectivas del silo.
        # 4.- Ajustar las cargas sumando la cantidad resultante dividida (que podría ser negativa si se reduce la carga).
        cantidad = cantidad * 1.0       # Para asegurarme que estoy trabajando con floats
        if cantidad > self.capacidad:
            cantidad = self.capacidad
        cantidad = max(0, cantidad)
        cargas = CargaSilo.select(""" silo_id = %d ORDER BY fecha_carga DESC, id DESC """ % (self.id))
        cantidad_cargada = CargaSilo.select(CargaSilo.q.siloID == self.id)
        if cantidad_cargada.count() > 0:
            cantidad_cargada = cantidad_cargada.sum("cantidad")
        else:
            cantidad_cargada = 0
        consumos = Consumo.select(Consumo.q.siloID == self.id)
        if consumos.count() > 0:
            cantidad_consumida = consumos.sum("cantidad")
        else:
            cantidad_consumida = 0
        cantidad_restante = cantidad_cargada - cantidad_consumida
        # myprint("cantidad_restante", cantidad_restante)
        cargas_efectivas = []
        for carga in cargas:
            if cantidad_restante <= 0:
                break
            cargas_efectivas.append(carga)
            cantidad_restante -= carga.cantidad
            # myprint("cantidad_restante:", cantidad_restante,
            #         "carga.cantidad:", carga.cantidad)
        if len(cargas_efectivas) == 0:  # El silo está vacío (o lo que es peor:
                                        # EN NEGATIVO)
            if cantidad_cargada - cantidad_consumida <= 0:
                # Ajusto la última carga:
                try:
                    carga = cargas[0]
                except IndexError:
                    myprint("El silo no se ha cargado nunca. No se puede ajustar")
                    return -1
                delta_existencias = (abs(cantidad_cargada - cantidad_consumida)
                                     + cantidad)
                carga.cantidad += delta_existencias
                if ajustar_producto_compra:
                    carga.productoCompra.existencias += delta_existencias
                    try:
                        stock_almacen_ppal = [s for s
                                        in carga.productoCompra.stocksAlmacen
                                        if s.almacen.principal][0]
                    except IndexError:
                        stock_almacen_ppal = StockAlmacen(
                                almacen = Almacen.get_almacen_principal(),
                                productoCompra = carga.productoCompra,
                                existencias = 0)
                    stock_almacen_ppal.existencias += delta_existencias
                en_el_silo = cantidad
            else:
                myprint("ERROR pclases.py (Silo.ajustar)-> No hay cargas efectivas pero la cantidad en el silo es mayor que 0.")
                return cantidad_cargada - cantidad_consumida    # Para darse este caso debería haber al menos una carga efectiva
        else:
            # parte_proporcional = (cantidad - (cantidad_cargada - cantidad_consumida))/ len(cargas_efectivas)
            # parte_proporcional = cantidad / len(cargas_efectivas)
            parte_proporcional = (cantidad - cantidad_restante) / len(cargas_efectivas)
                    # [1] La "última" de las cargas efectivas no tiene por qué ser exacta, puede tener parte
                    # en el silo y parte consumida. Ese resto (negativo) se resta (suma) a la cantidad
                    # proporcional a añadir a cada carga.
            #myprint("parte_proporcional:", parte_proporcional)
            for carga in cargas_efectivas:
                if ajustar_producto_compra:
                    carga.productoCompra.existencias += parte_proporcional - carga.cantidad
                carga.cantidad = parte_proporcional
                #myprint("carga.cantidad", carga.cantidad)
            en_el_silo = (parte_proporcional * len(cargas_efectivas)
                          + cantidad_restante) # Por lo mismo que antes. [1]
            # myprint("en_el_silo:", en_el_silo,
            #         "parte_proporcional:", parte_proporcional,
            #         "len(cargas_efectivas):", len(cargas_efectivas))
            # assert en_el_silo == cantidad
        return en_el_silo

    ocupado = property(get_ocupado)
    ocupacion = property(get_ocupacion)

cont, tiempo = print_verbose(cont, total, tiempo)

class CargaSilo(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------------- productoCompraID = ForeignKey('ProductoCompra')
    #----------------------------------------------- siloID = ForeignKey('Silo')
    lineasDeCompra = MultipleJoin('LineaDeCompra')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_consumido(self):
        """
        Devuelve la cantidad consumida correspondiente a esta carga.
        Algoritmo con orden O(log(n)) ~ O(n) en el peor caso -alto
        en comparación con O(1), que es lo que sería de esperar si
        no fuera un campo calculado-. No abusar.
        """
        # 1.- Busco todos los consumos de este producto y de este silo.
        # 2.- Sumo sus cantidades.
        # 3.- Busco todas las cargas en este silo de este producto y los ordeno por fecha.
        # 4.- Sumo sus cantidades.
        # 5.- La cantidad de las cargas debería ser superior a la de los consumos. restante = sum_cargas - sum_consumos.
        # 6.- Comenzando por la última carga:
        #   6.1.- Si carga.cantidad <= restante. De esa carga no se ha tocado nada todavía. restante = restante - carga.cantidad
        #   6.2.- Si carga.cantidad > restante. Esa carga está consumida parcialmente. restante_carga = carga.cantidad - restante;restante = 0
        #   6.3.- Si self == carga, devolver restante_carga.
        #   6.4.- Si restante == 0. Devolver carga.cantidad (se ha consumido por completo).
        consumos = Consumo.select(AND(Consumo.q.siloID == self.siloID,
                                      Consumo.q.productoCompraID == self.productoCompraID))
        if consumos.count() > 0:
            cantidad_consumida = consumos.sum("cantidad")
        else:
            cantidad_consumida = 0
        cantidad_cargada = CargaSilo.select(AND(CargaSilo.q.siloID == self.siloID,
                                                CargaSilo.q.productoCompraID == self.productoCompraID))
        if cantidad_cargada.count() > 0:
            cantidad_cargada = cantidad_cargada.sum("cantidad")
        else:
            cantidad_cargada = 0
        assert cantidad_cargada >= cantidad_consumida, "La cantidad cargada en el silo debe ser mayor o igual que la consumida del mismo."
            # Si no lo es, saltará un AssertionError que debe tratar la función que me invoque.
        cargas = CargaSilo.select(AND(CargaSilo.q.siloID == self.siloID,
                                      CargaSilo.q.productoCompraID == self.productoCompraID),
                                  orderBy = "-fecha_carga")
        cantidad_restante = cantidad_cargada - cantidad_consumida
        for carga in cargas:
            if carga.cantidad <= cantidad_restante:
                cantidad_restante -= carga.cantidad
                consumido_de_la_carga = 0
            else:
                consumido_de_la_carga = carga.cantidad - cantidad_restante
                cantidad_restante = 0
            if carga == self:
                res = consumido_de_la_carga
                break
            if cantidad_restante == 0:      # Por optimizar y que no haga el for hasta el final si ya sabemos seguro que se ha consumido.
                res = carga.cantidad
                break
        return res                          # Uno de los dos breaks se debe cumplir. En otro caso la he cagado con el algoritmo
                                            # y prefiero ver una excepción y arreglarlo lo antes posible.

    def get_restante(self):
        """
        Devuelve la cantidad restante en el silo correspondiente a esta carga.
        """
        return self.cantidad - self.get_consumido()

    consumido = property(get_consumido)
    restante = property(get_restante)

cont, tiempo = print_verbose(cont, total, tiempo)

class PruebaGranza(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------------- productoCompraID = ForeignKey('ProductoCompra')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class FacturaCompra(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #------------------------------------- proveedorID = ForeignKey('Proveedor')
    lineasDeCompra = MultipleJoin('LineaDeCompra')
    vencimientosPago = MultipleJoin('VencimientoPago')
    pagos = MultipleJoin('Pago')
    estimacionesPago = MultipleJoin('EstimacionPago')
    serviciosTomados = MultipleJoin('ServicioTomado')
    documentos = MultipleJoin('Documento')

    codigos_no_validacion = {0: "Visto bueno automático correcto.",
                             1: "Existen líneas sin pedido.",
                             2: "Existen líneas sin albarán.",
                             3: "Los precios no coinciden.",
                             4: "La cantidad servida es superior a la "
                                "solicitada.",
                             5: "Factura mixta de servicios y mercancía.",
                             6: "Servicios no se corresponden con transporte "
                                "ni comisión.",
                             -1: "N/D",
                             7: "Cantidad tecleada por usuario no coincide con"
                                " total de factura.",
                             8: "Más de un proveedor en albaranes y pedidos.",
                             9: "Proveedor de albaranes no coincide con el de"
                                " pedidos.",
                             10: "Factura vacía."}

    codigos_no_validacion = staticmethod(codigos_no_validacion)

    def get_info(self):
        if self.proveedor:
            proveedor = self.proveedor.nombre
        else:
            proveedor = "sin proveedor"
        if self.bloqueado:
            bloqueado = "bloqueada"
        else:
            bloqueado = "no bloqueada"
        return "Factura %s (%s) de %s. %s." % (self.numfactura,
                                                   utils.str_fecha(self.fecha),
                                                   proveedor,
                                                   bloqueado.title())

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    bloqueado = property(lambda self: self.bloqueada,
                         lambda self, valor: setattr(self, "bloqueada", valor))

    def calcular_importe_total(self, iva = True):
        """
        Calcula y devuelve el importe total, incluyendo IVA (por defecto),
        de la factura.
        """
        total = 0
        for ldc in self.lineasDeCompra:
            total += ldc.get_subtotal(iva = False)
        for s in self.serviciosTomados:
            total += s.get_subtotal(iva = False)
        total *= (1 - self.descuento)
        total += utils._float(self.cargo)
        #total = round(total, 2)         # Por ley la base imponible debe
                                # llevar 2 decimales y el IVA es el x% de la
                                # B.I., también con 2 decimales.
        # La ley dirá lo que quiera, pero menudos dolores de cabeza me está dando.
        #myprint("Con redondeo: %s. Sin redondeo: %s" % (
        #           utils.float2str(total + self.importeIva, 2),
        #           utils.float2str(round(total, 2) + self.importeIva)))
        if iva:
            total += self.importeIva        # Este método ya tiene en cuenta
                                # los distintos tipos de IVA, por línea, etc.
        return total

    def calcular_importe_iva(self):
        """
        Calcula el importe del IVA de la factura a partir de
        las LDC y servicios de la misma.
        Antes de devolverlo comprueba si todas las LDC y
        servicios tienen el mismo IVA y coinciden con el
        de la factura. En ese caso lanza una excepción si
        el importe calculado a partir de las LDC y servicios
        no es igual al subtotal de la factura por su propio IVA.
        Si el IVA de la factura tampoco coincide con el de las
        líneas de compra, se añade al IVA total (para el caso,
        por ejemplo, de las facturas con 18 + 4% por régimen de
        equivalencia).
        """
        totiva = 0.0
        #subtotal = self.cargo  # El cargo no entra en el IVA
        subtotal = 0.0
        ivas = []
        for ldc in self.lineasDeCompra + self.serviciosTomados:
            subtotalldc = ldc.get_subtotal(iva = False)
            totiva += subtotalldc * ldc.iva
            subtotal += subtotalldc
            if ldc.iva not in ivas:
                ivas.append(ldc.iva)
        #subtotal = round(subtotal, 2)   # Por ley la B.I. debe llevar 2 decimales y el IVA se calcula en base a ello.
        if len(ivas) == 1:
            if self.iva == ivas[0]:
                try:
                    msg = "El IVA total de la factura de compra %d no coincide con el IVA de sus líneas de venta USANDO ÚNICAMENTE 2 DÍGITOS DE PRECISIÓN: %s != %s." % (self.id, subtotal * self.iva, totiva)
                    assert round(subtotal * self.iva, 2) == round(totiva, 2), msg ## Este es el assert que usaba hasta ahora, pero da más problemas que soluciones el propagarlo y capturarlo fuera.
                except AssertionError, msg:
                    myprint(msg)
                # assert subtotal * self.iva == totiva, "El IVA total de la factura de compra %d no coincide con el IVA de sus líneas de venta: %s != %s." % (self.id, subtotal * self.iva, totiva)
            else:
                totiva += subtotal * self.iva
        #totiva = round(totiva, 2)       # Al igual que la base imponible, el total de IVA se redondea a 2 decimales.
        totiva = utils.myround(totiva) # Lo cambio por mi propia versión
            # correcta de redondear a 2 decimales. Caso fra. FV4/0003558
            # de 24/12/2014 (mrodriguez)
        return totiva

    importeIva = property(calcular_importe_iva,
                          doc = calcular_importe_iva.__doc__)
    importeTotal = property(calcular_importe_total,
                            doc = calcular_importe_total.__doc__)

    def iva_es_correcto(self):
        """
        Devuelve True sii el IVA de la factura y el IVA de las
        LDCs y servicios es el mismo.
        Si el IVA de todas las líneas es el mismo pero difiere del
        de la factura, cambia este último por el iva de las LDC.
        """
        ivas = []
        res = True
        for linea in self.lineasDeCompra + self.serviciosTomados:
            linea_iva = linea.iva
            if linea_iva not in ivas:
                ivas.append(linea_iva)
            if self.iva != linea_iva:
                res = False
        if len(ivas) == 1:
            self.iva = ivas[0]
            self.syncUpdate()
            res = True
        return res

    def iva_homogeneo(self):
        """
        Devuelve True sii el IVA de todas las LDC y servicios
        de la factura es el mismo (o no tiene).
        """
        ivas = []
        for linea in self.lineasDeCompra + self.serviciosTomados:
            linea_iva = linea.iva
            if linea_iva not in ivas:
                ivas.append(linea_iva)
        return len(ivas) <= 1

    def generar_numero_control(self):
        """
        Devuelve una cadena con un número de control de 6
        cifras relacionado unívocamente con la factura.
        """
        res = None
        if (self.proveedorID and self.vistoBuenoComercial
            and self.vistoBuenoTecnico and self.vistoBuenoDirector):
            base = self.numfactura + self.proveedor.nombre  # OJO: NUNCA
            # NUNCA NUNCA se debe cambiar el nombre del proveedor una
            # vez tenga algo facturado y con visto bueno.
            try:
                from hashlib import md5
                m = md5(base)
            except ImportError:
                import md5
                m = md5.md5(base)
            digest = m.hexdigest()
            res = digest[::6].upper() # Vale. No parece muy buena. Pero de una
            # muestra aleatoria de 1 millón de cadenas, tan solo se han
            # producido un 0.0038990426457789383 % de colisiones. No puedo
            # hacer más si uno de los requisitos del cliente es que tenga
            # exactamente 6 dígitos.
        return res

    numeroControl = property(generar_numero_control,
                             doc = "Número de control unívoco para la factura"
                                   ". Vale None si la factura de compra no es"
                                   " válida.")

    def get_codigo_validacion_visto_bueno(self):
        """
        Devuelve el código de validación del visto bueno
        en lugar de solamente True o False.
        Para obtener el visto bueno debe cumplir que:
        1.- Todas las líneas que contiene pertenecen a un pedido.
        2.- Todas esas mismas líneas pertenecen también a un albarán.
        3.- Los precios de las líneas de compra son iguales a los de las líneas de pedido. Si hay
            varios, la cantidad servida a cada precio debe ser inferior o igual a la cantidad
            pedida del mismo producto a cada precio.
        4.- La cantidad recibida en los albaranes es igual o inferior a la cantidad solicitada
            en el pedido.
        O BIEN (NEW! 24/01/07):
        1.- Solo contiene líneas de servicio.
        2.- Las líneas de servicio tienen un transporte o una comisión.
        """
        code = None
        if self.serviciosTomados and not self.lineasDeCompra:
            vto = len(self.serviciosTomados) == len([s for s in self.serviciosTomados if s.comision or s.transporteACuenta])
            if not vto:
                code = 6
        else:
            vto = len(self.lineasDeCompra) > 0
            if not vto:
                code = 10
            else:
                vto = vto and self.vistoBuenoUsuario    # Comenzamos con el chequeo del visto bueno del total del usuario.
                if not vto:
                    code = 7
            productos = {}
            pedidos = []
            proveedores_de_pedidos = []
            proveedores_de_albaranes = []
            if self.serviciosTomados:
                vto = False     # TODO: Si los servicios -mezclados con compras en esta factura- provienen de una factura de venta por
                                # ser comisión... ¿habría que chequearlo también?.
                code = 5
            for ldc in self.lineasDeCompra:
                vto = vto \
                and ldc.pedidoCompraID != None \
                and ldc.albaranEntradaID != None #\
                # and ldc.pedidoCompra.get_menor_precio(ldc.productoCompra) == ldc.precio
                if not vto:
                    if ldc.pedidoCompraID == None:
                        code = 1
                    elif ldc.albaranEntradaID == None:
                        code = 2
                    break
                if ldc.productoCompra not in productos:
                    productos[ldc.productoCompra] = {'pedida': 0,
                                                     'servida': ldc.cantidad,
                                                     'precios_servido': {ldc.precioConDescuento: ldc.cantidad},  # Precios a los que fueron
                                             # servidos los productos y cantidad servida total de cada uno de esos precios para ese producto.
                                                     'precios_pedido': {ldc.precioConDescuento: 0}
                                                    }
                else:
                    productos[ldc.productoCompra]['servida'] += ldc.cantidad
                    if ldc.precioConDescuento not in productos[ldc.productoCompra]['precios_servido']:
                        productos[ldc.productoCompra]['precios_servido'][ldc.precioConDescuento] = ldc.cantidad
                    else:
                        productos[ldc.productoCompra]['precios_servido'][ldc.precioConDescuento] += ldc.cantidad
                if ldc.pedidoCompra not in pedidos:
                    pedidos.append(ldc.pedidoCompra)
            if vto:
                for pedido in pedidos:
                    # Se ignora si el pedido está cerrado o no porque la diferencia entre un pedido
                    # no cerrado y uno cerrado es que la cantidad pedida sería mayor, lo cual no
                    # afecta al criterio de visto bueno.
                    if pedido.proveedor not in proveedores_de_pedidos:
                        proveedores_de_pedidos.append(pedido.proveedor)
                    for ldpc in pedido.lineasDePedidoDeCompra:
                        if ldpc.productoCompra not in productos:
                            productos[ldpc.productoCompra] = {'pedida': ldpc.cantidad,
                                                              'servida': 0,
                                                              'precios_pedido': {ldpc.precioConDescuento: ldpc.cantidad},
                                                              'precios_servido': {ldpc.precioConDescuento: 0}}
                        else:
                            productos[ldpc.productoCompra]['pedida'] += ldpc.cantidad
                            if ldpc.precioConDescuento not in productos[ldpc.productoCompra]['precios_pedido']:
                                productos[ldpc.productoCompra]['precios_pedido'][ldpc.precioConDescuento] = ldpc.cantidad
                            else:
                                productos[ldpc.productoCompra]['precios_pedido'][ldpc.precioConDescuento] += ldpc.cantidad
                for producto in productos:
                    vto = vto and productos[producto]['servida'] <= productos[producto]['pedida']
                    if not vto:
                        code = 4
                        break
                    for precio in productos[producto]['precios_servido']:
                        try:
                            vto = vto and productos[producto]['precios_servido'][precio] <= productos[producto]['precios_pedido'][precio]
                            if not vto:
                                code = 3
                        except KeyError:    # Si no está el precio que sea en el diccionario, directamente no doy visto bueno.
                            vto = False
                            code = 3
            # DONE: Quedaría una comprobación adicional: El proveedor del albarán debe ser el mismo que el del pedido.
            if vto:
                for ldc in self.lineasDeCompra:
                    if ldc.albaranEntrada.proveedor not in proveedores_de_albaranes:
                        proveedores_de_albaranes.append(ldc.albaranEntrada.proveedor)
                vto = vto and (len(proveedores_de_albaranes) == len(proveedores_de_pedidos) == 1)
                if not vto:
                    code = 8
                vto = vto and (self.proveedor == proveedores_de_pedidos[0] == proveedores_de_albaranes[0])
                if not vto:
                    code = 9
        if not vto:
            if not code:
                code = -1
        else:
            code = 0
        return code

    def get_visto_bueno_automatico(self):
        """
        Devuelve True si la factura obtiene el visto bueno
        automático.
        (Ver documentación de get_codigo_validacion_visto_bueno
        para las condiciones de visto bueno automático.)
        """
        return self.get_codigo_validacion_visto_bueno() == 0

    def get_visto_bueno_pago(self):
        """
        Devuelve True si la factura tiene el visto bueno para
        el pago. Se consigue si:
        Tiene el visto bueno automático (incluye la confirmación del total por el usuario).
        O bien si tiene el visto bueno del director comercial, técnico y gerente.
        """
        return (self.vistoBuenoComercial and self.vistoBuenoTecnico and self.vistoBuenoDirector) or (self.vistoBuenoAutomatico)

    vistoBuenoAutomatico = property(get_visto_bueno_automatico, doc = get_visto_bueno_automatico.__doc__)
    vistoBuenoPago = property(get_visto_bueno_pago, doc = get_visto_bueno_pago.__doc__)

    def emparejar_vencimientos(self):
        """
        Devuelve un diccionario con los vencimientos y cobros de la factura
        emparejados.
        El diccionario es de la forma:
        {vencimiento1: [cobro1],
         vencimiento2: [cobro2],
         vencimiento3: [],
         'vtos': [vencimiento1, vencimiento2, vencimiento3...],
         'cbrs': [cobro1, cobro2]}
        Si tuviese más cobros que vencimientos, entonces se devolvería un diccionario tal que:
        {vencimiento1: [cobro1],
         vencimiento2: [cobro2],
         None: [cobro3, cobro4...],
         'vtos': [vencimiento1, vencimiento2],
         'cbrs': [cobro1, cobro2, cobro3, cobro4...]}
        'vtos' y 'cbrs' son copias ordenadas de las listas de vencimientos y cobros.
        El algoritmo para hacerlo es:
        1.- Construyo el diccionario con todos los vencimientos.
        2.- Construyo una lista auxiliar con los cobros ordenados por fecha.
        3.- Recorro el diccionario de vencimientos por orden de fecha.
            3.1.- Saco y asigno el primer cobro de la lista al vencimiento tratado en la iteración.
            3.2.- Si no quedan vencimientos por asignar, creo una clave None y agrego los cobros restantes.
        """
        res = {}
        cbrs = self.pagos[:]
        cbrs.sort(utils.cmp_fecha_id)
        vtos = self.vencimientosPago[:]
        vtos.sort(utils.cmp_fecha_id)
        res['vtos'] = vtos[:]
        res['cbrs'] = cbrs[:]
        for vto in vtos:
            try:
                cbr = cbrs.pop()
            except IndexError:
                res[vto] = []
            else:
                res[vto] = [cbr]
        if cbrs != []:
            res[None] = cbrs
        return res

    def get_importe_primer_vencimiento_pendiente(self):
        """
        Devuelve el importe del primer vencimiento pendiente de pagar
        de la factura o 0 si no quedan.
        """
        res = 0.0
        pares = self.emparejar_vencimientos()
        for vto in pares['vtos']:       # pares['vtos'] está ordenado por fecha
            if pares[vto] == []:
                res = vto.importe
                break
        return res

    def anular_vistos_buenos(self):
        """
        Anula los vistos buenos de la factura.
        (Útil por ejemplo para cuando se modifica el
        contenido de una factura después de haber
        obtenido el visto bueno).
        """
        self.vistoBuenoComercial = self.vistoBuenoTecnico = self.vistoBuenoDirector = self.vistoBuenoUsuario = False
        self.fechaVistoBuenoUsuario = self.fechaVistoBuenoDirector = self.fechaVistoBuenoTecnico = self.fechaVistoBuenoComercial = None
        self.syncUpdate()

cont, tiempo = print_verbose(cont, total, tiempo)

class LineaDeCompra(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #------------------------------- pedidoCompraID = ForeignKey('PedidoCompra')
    #--------------------------- albaranEntradaID = ForeignKey('AlbaranEntrada')
    #--------------------------- productoCompraID = ForeignKey('ProductoCompra')
    #----------------------------- facturaCompraID = ForeignKey('FacturaCompra')
    #---- siloID = ForeignKey("Silo", default = None)     # Redundante, pero por
                                                    # compatibilidad.
    #--------------------- cargaSiloID = ForeignKey('CargaSilo', default = None)
    lineasDePedidoDeCompra = RelatedJoin('LineaDePedidoDeCompra',
                joinColumn='linea_de_compra_id',
                otherColumn='linea_de_pedido_de_compra_id',
                intermediateTable='linea_de_pedido_de_compra__linea_de_compra')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        info_alb_fra = ""
        if self.albaranEntrada or self.facturaCompra:
            info_alb_fra = []
            if self.albaranEntrada:
                info_alb_fra.append("alb. %s" % self.albaranEntrada.numalbaran)
            if self.facturaCompra:
                info_alb_fra.append("fra. %s" % self.facturaCompra.numfactura)
            info_alb_fra = "; ".join(info_alb_fra)
            info_alb_fra = "(%s)" % info_alb_fra
        return "%s; %s * %s = %s%s" % (self.productoCompra.descripcion,
            utils.float2str(self.cantidad),
            utils.float2str(self.precio * (1 - self.descuento)),
            utils.float2str(self.get_subtotal(iva = True, prorrateado = True)),
            info_alb_fra)

    def get_fecha_albaran(self):
        """
        Devuelve la fecha del albarán al que pertenece la línea de compra
        o None si no tiene.
        """
        if self.albaranEntradaID != None:
            fecha = self.albaranEntrada.fecha
        else:
            fecha = None
        return fecha

    def get_precio_con_descuento(self):
        """
        Precio total de la línea incluyendo descuento, pero sin incluir el IVA.
        """
        return self.precio * (1 - self.descuento)

    precioConDescuento = property(get_precio_con_descuento,
                                  doc = get_precio_con_descuento.__doc__)

    def get_proveedor(self):
        return ((self.albaranEntrada and self.albaranEntrada.proveedor)
                or (self.facturaCompra and self.facturaCompra.proveedor)
                or None)

    def get_nombre_proveedor(self):
        proveedor = self.get_proveedor()
        return proveedor and proveedor.nombre or ""

    def get_descripcion_productoCompra(self):
        return self.productoCompra and self.productoCompra.descripcion or ""

    proveedor = property(get_proveedor, doc = "Objeto proveedor del albarán de la línea de compra o None si no tiene.")
    nombre_proveedor = property(get_nombre_proveedor,
                                doc = 'Nombre del proveedor de la línea de compra del albarán o "" si no tiene.')
    descripcion_productoCompra = property(get_descripcion_productoCompra,
                                          doc = 'Descripción del producto de compra de la LDC o "" si no tiene.')

    def es_igual_salvo_cantidad(self, ldp):
        """
        Compara la LDP con otra recibida. Devuelve True si los valores
        son iguales para los campos:
          - pedidoCompraID
          - albaranEntradaID
          - facturaCompraID
          - productoCompraID
          - precio
          - descuento
          - entrega
          - siloID
          - cargaSiloID
        """
        campos = ("pedidoCompraID",
                  "albaranEntradaID",
                  "facturaCompraID",
                  "productoCompraID",
                  "precio",
                  "descuento",
                  "entrega",
                  "siloID",
                  "cargaSiloID")
        for campo in campos:
            if getattr(self, campo) != getattr(ldp, campo):
                return False
        return True

    def get_subtotal(self, iva = False, descuento = True, prorrateado = False):
        """
        Devuelve el subtotal con o sin IVA (según se indique) de
        la línea de compra: precio * cantidad - descuento.
        NOTA: No se aplica redondeo en el subtotal antes de aplicar el
        IVA. Me permito trabajar con varios decimales en el contenido
        de la factura, pero a partir del subtotal neto de la factura
        completa solo se permite trabajar con céntimos de euro como
        fracción máxima (ver aeat.es).
        Si «prorrateado» devuelve el importe dividido entre el número de
        vencimientos de la factura. Si no tiene vtos. todavía, lo hace según
        la forma de pago por defecto del proveedor.
        """
        res = self.cantidad * self.precio
        if descuento:
            res *= (1 - self.descuento)
        if iva:
            res *= 1 + self.iva
        # Las líneas ya tienen IVA propio, no se usa más el IVA del pedido.
        # if iva and self.pedidoCompraID:
        #    res *= (1 + self.pedidoCompra.iva)
        if prorrateado:
            try:
                numvtos = max(1, len(self.proveedor.get_vencimientos()))
            except (AttributeError, TypeError, ValueError):
                numvtos = 1
            res /= numvtos
        return res

cont, tiempo = print_verbose(cont, total, tiempo)

class VencimientoPago(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------- facturaCompraID = ForeignKey('FacturaCompra')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def calcular_importe_pdte(self):
        """
        Devuelve el importe total o parcial del vencimiento que está
        pendiente de pago.
        El algoritmo que usa es:
            1.- Ordena los vtos. por fecha de manera que si queda algo
                pendiente siempre sea en los últimos vencimientos.
            2.- Suma el importe total pagado de la factura.
            3.- Anula los vencimientos por orden de fecha con los pagos
                realizados hasta completar todos o agotar la cantidad pagada.
        OJO: O(n) en el peor caso.
        """
        fra = self.facturaCompra
        cant_pagada = abs(sum([p.importe for p in fra.pagos]))
        vencimientos_pendientes = fra.vencimientosPago[:]
        vencimientos_pendientes.sort(utils.cmp_fecha_id)
        while cant_pagada > 0 and vencimientos_pendientes:
            v = vencimientos_pendientes.pop(0)
            if cant_pagada < abs(v.importe):
                # Si no cubre al vencimiento lo devuelvo a la lista de pdtes.
                vencimientos_pendientes.insert(0, v)
            cant_pagada -= v.importe
        if self in vencimientos_pendientes:
            if self == vencimientos_pendientes[0] and cant_pagada < 0:
                res = -cant_pagada
            else:   # No es el primer vencimiento (único sospechoso de estar
                    # pagado parcialmente sólo) o los pagos y vencimientos han
                    # cuadrado hasta donde han llegado (cant_pagada == 0).
                res = self.importe
        else:
            res = 0.0
        return res

    def actualizar_estado_pago_domiciliaciones():
        """
        Pone como pagadas las domiciliaciones bancarias automáticamente
        al llegar al vencimiento.
        """
        for v in VencimientoPago.select(AND(
                VencimientoPago.q.procesado == False,
                NOT(VencimientoPago.q.observaciones.contains("TRANSF")),
                OR(VencimientoPago.q.observaciones.contains("DOMICILIA"),
                   VencimientoPago.q.observaciones.contains("RECIBO"),
                   VencimientoPago.q.observaciones.contains("BANC")))):
            # Si ya está pagado, paso
            if DEBUG:
                myprint("Procesando", v.get_puid())
            if v.facturaCompra:
                vtos_pagos = v.facturaCompra.emparejar_vencimientos()
                try:
                    pagos = vtos_pagos[v]
                except KeyError:
                    pass
                else:
                    importe_cobrado = sum([p.importe for p in pagos])
                    if importe_cobrado >= v.importe:
                        v.procesado = True    # Marco para no volver a tratar.
                        Auditoria.modificado(v, None, None,
                            "Vencimiento de pago marcado como procesado al "
                            "comprobar automáticamente su importe pagado.")
                        continue    # Ya está pagado aunque no haya sido
                                    # procesado automáticamente.
            if mx.DateTime.today() >= v.fecha:
                if DEBUG:
                    myprint("Actualizando el estado de %s..." % v.get_puid())
                    try:
                        sys.stdout.flush()
                    except AttributeError:
                        pass    # Consola de depuración o algo. No tiene flush.
                v.fechaCobrado = v.fecha
                v.procesado = True
                Auditoria.modificado(v, None, None,
                    "Vencimiento de pago domiciliado marcado como procesado y"
                    " pagado al comprobar automáticamente su fecha de "
                    "vencimiento.")
                v.syncUpdate()
                # Creo el pago:
                try:
                    cuenta_defecto = CuentaOrigen.select(
                        orderBy = "-id")[0]
                except IndexError:
                    cuenta_defecto = None
                try:
                    proveedor = v.facturaCompra.proveedor
                except AttributeError:
                    proveedor = None
                try:
                    cuenta_destino = proveedor.cuentasDestino[-1]
                except (IndexError, AttributeError):
                    cuenta_destino = None
                Pago(proveedor = proveedor,
                     cuentaOrigen = cuenta_defecto,
                     cuentaDestino = cuenta_destino,
                     logicMovimientos = None,
                     pagarePago = None,
                     facturaCompra = v.facturaCompra,
                     fecha = v.fecha,
                     importe = v.importe - importe_cobrado,
                     observaciones = "Pago creado automáticamente al vencer "
                                     "la domiciliación bancaria.",
                     conceptoLibre = "")
                if DEBUG:
                    myprint("DONE.")

    actualizar_estado_pago_domiciliaciones = staticmethod(
        actualizar_estado_pago_domiciliaciones)

cont, tiempo = print_verbose(cont, total, tiempo)

class Pago(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------- facturaCompraID = ForeignKey('FacturaCompra')
    #------------------- pagarePagoID = ForeignKey('PagarePago', default = None)
    #------- logicMovimientosID = ForeignKey('LogicMovimientos', default = None)
    #--------------------- proveedorID = ForeignKey('Proveedor', default = None)
    #--------------- cuentaOrigenID = ForeignKey('CuentaOrigen', default = None)
    #------------- cuentaDestinoID = ForeignKey('CuentaDestino', default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_concepto(self):
        """
        Devuelve el número de factura o el nombre de la cuenta
        LOGIC, dependiendo de a qué esté asociado el pago.
        """
        concepto = "-"
        if self.facturaCompra != None:
            concepto = "Factura %s" % (self.facturaCompra.numfactura)
        elif self.logicMovimientos != None:
            concepto  = "Cuenta LOGIC %s: %s" % (self.logicMovimientos.cuenta, self.logicMovimientos.comentario)
        return concepto

    concepto = property(get_concepto, doc = "Factura o cuenta LOGIC relacionada con el pago.")

    def es_transferencia(self):
        """
        Devuelve True si el pago se puede considerar una transferencia.
        Se considera una transferencia si cuentaOrigen o cuentaDestino
        no son None. Al menos una de las dos debe estar instanciada.
        """
        return self.cuentaOrigen != None or self.cuentaDestino != None

    def get_fecha_emision(self):
        """
        Devuelve la fecha de emisión del pago.
        Si el pago es un pagaré o confirming, es la fecha de emisión del
        pagaré o confirming.
        Si el pago es una transferencia, es la fecha del pago.
        Si es un movimiento contable, también es la fecha del pago.
        Si es cualquier otro tipo de forma de pago (contado, etc.) pues
        también coincide con la fecha del pago.
        """
        if self.pagarePago:
            return self.pagarePago.fechaEmision
        else:
            return self.fecha

cont, tiempo = print_verbose(cont, total, tiempo)

class EstimacionPago(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------- facturaCompraID = ForeignKey('FacturaCompra')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class VencimientoCobro(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #------------------------------- facturaVentaID = ForeignKey('FacturaVenta')
    #------------------- prefacturaID = ForeignKey('Prefactura', default = None)
    #--------------- cuentaOrigenID = ForeignKey('CuentaOrigen', default = None)
    #--------------------------- reciboID = ForeignKey('Recibo', default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_factura_o_prefactura(self):
        """
        Devuelve la factura relacionada, tanto si es facturaVenta
        como prefactura, o None si no tiene ninguna de ellas.
        Como no debería tener ambos valores distintos de nulo a
        la vez, tiene preferencia facturaVenta sobre prefactura.
        """
        return self.facturaVenta or self.prefactura

    @property
    def factura(self):
        return self.get_factura_o_prefactura()

    def get_documentoDePago(self):
        """
        Devuelve el documento de pago normalizado (el de la base de datos, no
        el texto libre del vencimiento) según el campo observaciones del
        vencimiento. Si no se puede determinar, busca en el pedido de donde
        viene la factura y posteriormente en el cliente.
        Finalmente devuelve un objeto DocumentoDePago de pclases o None.
        """
        res = None
        try:
            res = Cobro._parse_docpago(self.observaciones)
        except AttributeError:
            res = None
        if not res:
            res = self.facturaVenta.cliente.get_documentoDePago()
        return res


cont, tiempo = print_verbose(cont, total, tiempo)

class PagarePago(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    pagos = MultipleJoin('Pago')
    # fechaCobro = ... default=None.     NOTA: No lo pilla por defecto de la
    #   BD. En la creación de objetos en las ventanas habrá que decirle
    # explícitamente que será None.
    documentos = MultipleJoin('Documento')

    # Por compatibilidad con Pagarés de cobro y confirmings. (Por menos que
    # esto he hecho superclases. Esta vez tengo prisa. Pero que sepas que
    # deberías tener un class DocumentoDePago del que heredar).
    def set_fechaPago(self, fecha):
        self.fechaPago = fecha
    fechaVencimiento = property(lambda self: self.fechaPago, set_fechaPago)
    def set_fechaCobrado(self, fecha):
        self.fechaCobrado = fecha
    fechaPagado = property(lambda self: self.fechaCobrado, set_fechaCobrado)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def esta_pendiente(self):
        return self.cantidad > self.pagado

    def get_cantidad_pendiente(self):
        return self.cantidad - self.pagado

    def set_cantidad_pendiente(self, pendiente):
        """
        Modifica la cantidad cobrada para que quede como pendiente
        la cantidad recibida.
        """
        self.pagado = self.cantidad - pendiente

    pendiente = property(esta_pendiente, doc = "Valor booleano que devuelve si el pagaré está completamente pagado (False) o no -tiene algo o todo pendiente de pagar (True)-.")
    cantidad_pendiente = property(get_cantidad_pendiente, set_cantidad_pendiente, doc = "Cantidad pendiente de pagar del total del pagaré")

    def actualizar_estado_cobro(cls):
        """
        Marca por defecto como cobrados todos los pagarés vencidos, pero
        respetando aquellos que ya se marcaron manualmente como pendientes.
        """
        actualizar_estado_cobro_de(cls)

    actualizar_estado_cobro = classmethod(actualizar_estado_cobro)


cont, tiempo = print_verbose(cont, total, tiempo)

class Cobro(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #------------------------------- facturaVentaID = ForeignKey('FacturaVenta')
    #------------------- prefacturaID = ForeignKey('Prefactura', default = None)
    #--------------------------- facturaDeAbonoID = ForeignKey('FacturaDeAbono')
    #----------------- pagareCobroID = ForeignKey('PagareCobro', default = None)
    #------------------- confirmingID = ForeignKey('Confirming', default = None)
    #------------------------- clienteID = ForeignKey('Cliente', default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_factura_o_prefactura(self):
        """
        Devuelve la factura relacionada, tanto si es facturaVenta
        como prefactura, o None si no tiene ninguna de ellas.
        Como no debería tener ambos valores distintos de nulo a
        la vez, tiene preferencia facturaVenta sobre prefactura.
        """
        return self.facturaVenta or self.prefactura

    def get_numfactura(self):
        """
        Devuelve el número de la factura de venta o de la
        factura de abono relacionada con el cobro actual.
        Devuelve la cadena vacía si no tiene relación con
        ninguna de las dos cosas.
        """
        if self.facturaVentaID != None:
            return self.facturaVenta.numfactura
        if self.facturaDeAbonoID != None:
            return self.facturaDeAbono.numfactura
        return ""

    def get_cliente(self):
        """
        Devuelve el objeto cliente relacionado con el cobro
        o None si no se encontró.
        """
        cliente = None
        if self.facturaVentaID != None:
            cliente = self.facturaVenta.cliente
        if self.prefacturaID != None:
            cliente = self.prefactura.cliente
        if (self.facturaDeAbonoID != None
                and self.facturaDeAbono.abonoID != None):
            cliente = self.facturaDeAbono.abono.cliente
        if self.clienteID != cliente:
            try:
                self.clienteID = cliente.id
            except AttributeError:  # No hay cliente
                self.clienteID = None
        return cliente

    def set_cliente(self, cliente):
        """
        Hace que el cliente de la factura de venta o
        de abono relacionada(s) con el cobro tengan como
        cliente el objeto cliente recibido.
        """
        if self.facturaVentaID != None:
            self.facturaVenta.cliente = cliente
        if self.prefacturaID != None:
            self.prefactura.cliente = cliente
        if (self.facturaDeAbonoID != None
                and self.facturaDeAbono.abonoID != None):
            self.facturaDeAbono.abono.cliente = cliente
        self.clienteID = cliente.id

    # DONE: La tabla ya tiene un cliente_id. ¿Por qué esta property?
    #       Probablemente sea una modificación posterior. Me aseguro en el
    #       getter y en el setter que se mantiene la coherencia entre la
    #       propiedad calculada (cliente) y el atributo de la tabla
    #       (clienteID).
    cliente = property(get_cliente, set_cliente,
                       doc = "Cliente relacionado con el cobro.")
    numfactura = property(get_numfactura, doc = get_numfactura.__doc__)

    def esta_cobrado(self, fecha_base = None):
        # EXPERIMENTAL
        if fecha_base:
            strfecha = fecha_base.strftime("%Y-%m-%d")
            sql = "SELECT cobro_esta_cobrado(%d, '%s');" % (self.id, strfecha)
        else:
            sql = "SELECT cobro_esta_cobrado(%d);" % self.id
        try:
            cobrado = self._connection.queryOne(sql)[0]
        except IndexError:
            cobrado = 0.0 # Ola ke ase ¿cobro no existe o ke ase?
        return cobrado  # 0.0 es False

    def DEPRECATED_esta_cobrado(self, fecha_base = None, gato_en_talega = False):
        """
        Devuelve True si el cobro está realmente pagado en la fecha indicada
        (o en cualquier fecha, si no se especifica), esto es:
            - Si es una transferencia.
            - Si es en efectivo.
            - Si es un cheque.
            - Si es un confirming.
            - Si es un pagaré no vencido.
            - Si es un pagaré no pendiente.
        Pero si gato_en_talega es True solo cuento que un cobro está cobrado
        cuando el gato está en la talega. Gatus in talegui. Esto es, cuando
        el ninerito lo tengo yo ya, aunque sea un confirming del mismísimo
        Emilio Botín, o está confirmado por el usuario que ya no está
        pendiente o no lo cuento como cobro.
        """
        cobrado = 0.0
        if not self.confirmingID and not self.pagareCobroID:
            # Cualquier otro cobro que no implique futuribles, está cobrado
            # desde el momento en que se introduce en el sistema.
            if not fecha_base or fecha_base >= self.fecha:
                cobrado += self.importe
        elif self.pagareCobro:
            compromiso_cobro = self.pagareCobro
            compromiso_cobro.sync()
            if not fecha_base:
                if not compromiso_cobro.pendiente:
                    cobrado += compromiso_cobro.cantidad
                else:
                    if not gato_en_talega:
                        # Además de no estar pendiente(arriba), lo considero
                        # cobrado si no ha vencido aún aunque esté pendiente.
                        if (compromiso_cobro.fechaVencimiento
                            > mx.DateTime.localtime()):
                            cobrado += compromiso_cobro.cantidad
            else:
                if (compromiso_cobro.fechaCobrado
                    and fecha_base >= compromiso_cobro.fechaCobrado
                    and compromiso_cobro.cobrado >= compromiso_cobro.cantidad):
                    cobrado += compromiso_cobro.cantidad
                else:
                    if not gato_en_talega:
                        # Cobrado si no ha vencido en fecha base y ya existía.
                        if (compromiso_cobro.fechaVencimiento > fecha_base and
                            compromiso_cobro.fechaRecepcion <= fecha_base):
                            cobrado += compromiso_cobro.cantidad
        elif self.confirming:
            compromiso_cobro = self.confirming
            compromiso_cobro.sync()
            if not fecha_base:
                if not compromiso_cobro.pendiente:
                    cobrado += compromiso_cobro.cantidad
                else:
                    if not gato_en_talega:
                        # Además de no estar pendiente(arriba), lo considero
                        # cobrado siempre porque si no responde el cliente,
                        # responde el banco, por lo que el cobro lo tengo
                        # asegurado como proveedor.
                        cobrado += compromiso_cobro.cantidad
            else:
                if (compromiso_cobro.fechaCobrado
                    and fecha_base >= compromiso_cobro.fechaCobrado
                    and compromiso_cobro.cobrado >= compromiso_cobro.cantidad):
                    cobrado += compromiso_cobro.cantidad
                else:
                    if not gato_en_talega:
                        # Cobrado si ya existía.
                        if compromiso_cobro.fechaRecepcion <= fecha_base:
                            cobrado += compromiso_cobro.cantidad
        return cobrado  # 0.0 es False.

    def get_fechaVencimiento(self):
        """
        Devuelve la fecha de vencimiento del documento de pago asociado
        al cobro. Si la forma de pago no lleva vencimiento devolverá la
        fecha en que se hace real en que se hace el cobro.
        """
        if self.confirming:
            res = self.confirming.fechaVencimiento
        elif self.pagareCobro:
            res = self.pagareCobro.fechaVencimiento
        else:
            res = self.fecha
        return res

    @staticmethod
    def _parse_fdp(txt, force_create = False, strict_mode = True):
        rex = re.compile("\d+")
        try:
            plazo = int(rex.findall(txt)[0])
        except (IndexError, TypeError, ValueError):
            if "CONTADO" in txt:
                plazo = 0
            else:
                return None
        if not ((plazo % 15) == 0 and (0 <= plazo <= 365)):
            return None
        documento = txt.split(",")[0]
        documento_de_pago = Cobro._parse_docpago(documento, strict_mode)
        if not documento_de_pago:
            return None
        try:
            fdp = FormaDePago.select(AND(
                    FormaDePago.q.plazo == plazo,
                    FormaDePago.q.documentoDePagoID == documento_de_pago.id
                ))[0]
        except IndexError:
            # Aquí me aseguro, ya que el documento de pago es válido, de
            # crear la forma de pago correcta si así se me ha indicado.
            if force_create:
                fdp = FormaDePago(plazo = plazo,
                                  documentoDePago = documento_de_pago)
            else:
                fdp = None
        return fdp

    @staticmethod
    def _parse_docpago(txt, strict_mode = True):
        """
        "Parsea" una forma de pago y devuelve el registro estandarizado que
        le corresponde. Si strict_mode es True, el texto recibido debe
        ajustarse fielmente al objeto del documento de pago que devolverá.
        Por ejemplo, solo devolverá "Pagaré a la orden" si el texto es
        "pagaré a la orden" o muy parecido. Pero con "pagaré" a secas, sin
        especificar el tipo, devolverá None.
        Si es False habrá más posibilidades de que devuelva alguna forma de
        pago válida aunque el texto recibido sea algo impreciso.
        """
        txt = txt.upper()
        if "LUNES" in txt:
            doc = DocumentoDePago.Lunes()
        elif ("PAGAR" in txt or "PGR" in txt):
            if strict_mode:
                if "ORD" in txt:
                    # CWT: Si no se especifica si es a la orden o no a la
                    # orden entonces tengo que respetar lo que decía el
                    # vencimiento textualmente.
                    if " NO " in txt:
                        doc = DocumentoDePago.NoALaOrden()
                    else:
                        doc = DocumentoDePago.Pagare()
                else:
                    doc = None
            else:
                if " NO " in txt and "ORD" in txt:
                    doc = DocumentoDePago.NoALaOrden()
                else:
                    doc = DocumentoDePago.Pagare()
        elif "CONFIRMING" in txt:
            doc = DocumentoDePago.Confirming()
        elif "CONTADO" in txt or "EFECTIVO" in txt:
            doc = DocumentoDePago.Contado()
        elif "TRANSF" in txt:
            doc = DocumentoDePago.Transferencia()
        elif "NO A LA ORDEN" in txt:
            doc = DocumentoDePago.NoALaOrden()
        elif "CHEQUE" in txt:
            doc = DocumentoDePago.Cheque()
        elif "CARTA" in txt and "VISTA" in txt:
            doc = DocumentoDePago.CartaVista()
        elif "CARTA" in txt:
            doc = DocumentoDePago.Carta()
        elif "DOMICILIA" in txt or "RECIBO" in txt or "BANC" in txt:
            doc = DocumentoDePago.Domiciliacion()
        # DONE: Falta recibo. Pero no me han dicho nada. Tampoco si cuando dice
        #       "PAGARÉ" es a la orden o no a la orden. [update] Si no se
        #       especifica, es a la orden. Del recibo, de momento, nada.
        #       [update 20/03/2013] Ya me piden dar de alta la domiciliación.
        else:
            doc = None
        return doc

    def get_documentoDePago(self):
        """
        :returns: Un objeto DocumentoDePago concordante con el
                  usado en el cobro. Si no se puede determinar devuelve
                  lo que ponga literalmente en la cadena de texto almacenada
                  en los vencimientos. Y si la factura no tiene vencimientos,
                  entonces devuelve None (caso altamente improbable).
        """
        vencimiento = None
        try:
            vtoscobros = self.get_factura_o_prefactura().emparejar_vencimientos()
        except AttributeError:
            # Es una factura de abono
            vtoscobros = self.facturaDeAbono.emparejar_vencimientos()
        doc = Cobro._parse_docpago(self.observaciones)
        if not doc:
            for vto in vtoscobros['vtos']:
                if self in vtoscobros[vto]:
                    vencimiento = vto
            if vencimiento:
                doc = Cobro._parse_docpago(vencimiento.observaciones)
            if not doc:
                if self.confirming:
                    try:
                        doc = DocumentoDePago.selectBy(
                                documento = "Confirming")[0]
                    except IndexError:
                        doc = None
            if not doc: # No puedo tirar del vencimiento que corresponde al cobro.
                        # Tiro del primero de ellos, que es el caso más común.
                try:
                    try:
                        vto = self.facturaVenta.vencimientosCobro[0]
                    except AttributeError:  # No es fra. venta.
                        try:
                            vto = self.facturaDeAbono.vencimientosCobro[0]
                        except AttributeError:  # Tampoco es abono.
                            vto = self.prefactura.vencimientosCobro[0]
                    try:
                        doc = vto.observaciones.split(",")[0]
                    except IndexError:
                        doc = vto.observaciones
                except IndexError:
                    # Ni siquiera tiene vencimientos, tendré que devolver
                    # None ¿Qué hago si no?
                    doc = None
        return doc

    fechaVencimiento = property(get_fechaVencimiento)
    documentoDePago = property(get_documentoDePago)

    def calc_plazo_pago_real(self):
        """
        :returns: Devuelve un número entero con los días que han transcurrido
                  desde la fecha de la factura hasta la del cobro real o el
                  vencimiento del documento del cobro. Si ocurre algún
                  error, devuelve None.
        """
        try:
            fechafra = self.facturaVenta.fecha
        except AttributeError:   # Es una factura proforma o de abono.
            try:
                fechafra = self.facturaDeAbono.fecha
            except AttributeError:
                fechafra = self.prefactura.fecha
        fechavto = self.fechaVencimiento
        res = int(ceil((fechavto - fechafra).days))
        return res

    def calc_diferencia_plazo_pago(self):
        """
        :returns: Número entero con la diferencia en días entre el plazo
                  de pago que tenía el vencimiento y el plazo de pago real
                  que ha acabado teniendo el documento de cobro.
                  Se calcula restando a la fecha de vencimiento del cobro
                  la fecha de vencimiento original.
                  Si el cobro no tiene factura o la factura no tiene
                  vencimientos, etc. Devuelve None.
        """
        retraso = None
        try:
            vtoscobros = self.facturaVenta.emparejar_vencimientos()
        except AttributeError:
            retraso = None  # No tiene factura el cobro. WTF?
        else:
            fechavto = None
            for vto in vtoscobros["vtos"]:
                if self in vtoscobros[vto]:
                    fechavto = vto.fecha
                    break
            if fechavto is None:
                try:        # Pruebo con el último vencimiento.
                    fechavto = vto.fecha
                except (AttributeError, NameError):
                    retraso = None # No tiene vencimientos la fra.
            try:
                retraso = int(ceil((self.fechaVencimiento - fechavto).days))
            except (AttributeError, TypeError, ValueError):
                retraso = None
        return retraso

cont, tiempo = print_verbose(cont, total, tiempo)

class PagareCobro(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    cobros = MultipleJoin('Cobro')
    # fechaCobro = ... default=None.     NOTA: No lo pilla por defecto de la BD. En la creación de objetos en las
    #                                    ventanas habrá que decirle explícitamente que será None.
    documentos = MultipleJoin('Documento')
    #--------------------------------------------- bancoID = ForeignKey('Banco')
    #----------------------------------------- # remesaID = ForeignKey('Remesa')
    efectos = MultipleJoin("Efecto")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_puid(self):
        """
        Devuelve un identificador único, etcétera, etcétera
        """
        return "%s:%d" % ("PAGC", self.id)

    @property
    def remesado(self):
        """
        True si está en una remesa confirmada. Condiciones para ello:
        * Que estén tengan un efecto relacionado.
        * Que el efecto esté en una remesa.
        * Que la remesa esté confirmada (aceptada = True).
        """
        try:
            return reduce(lambda x, y: x and y,
                          [r.aceptada for r in self.efecto.remesas])
        except (AttributeError, TypeError): # No efecto o efecto pero no remesa.
            return False

    def get_efecto(self):
        try:
            return self.efectos[0]
        except IndexError:
            efecto = Efecto(pagareCobro = self,
                            confirming = None,
                            cuentaBancariaCliente = None)
            return efecto

    def set_efecto(self, value_efecto):
        value_efecto.pagareCobro = self
        value_efecto.confirming = None

    efecto = property(get_efecto, set_efecto)

    def esta_pendiente(self):
        return self.cantidad > self.cobrado

    def get_cantidad_pendiente(self):
        return self.cantidad - self.cobrado

    def set_cantidad_pendiente(self, pendiente):
        """
        Modifica la cantidad cobrada para que quede como pendiente
        la cantidad recibida.
        """
        self.cobrado = self.cantidad - pendiente

    def get_cliente(self):
        """
        Devuelve el objeto cliente relacionado con el pagaré a través de
        "cobros". Si no tiene, devuelve None.
        """
        res = None
        if len(self.cobros) > 0:
            res = self.cobros[0].cliente
        return res

    def get_fechaCobro(self):
        return self.fechaCobro

    def set_fechaCobro(self, fecha):
        self.fechaCobro = fecha
        self.syncUpdate()

    pendiente = property(esta_pendiente, doc = "Valor booleano que devuelve si el pagaré está completamente pagado (False) o no -tiene algo o todo pendiente de cobrar (True)-.")
    cantidad_pendiente = property(get_cantidad_pendiente, set_cantidad_pendiente, doc = "Cantidad pendiente de cobrar del total del pagaré")
    cliente = property(get_cliente, doc = "Devuelve el objeto Cliente relacionado con el pagaré.")
    fechaVencimiento = property(get_fechaCobro, set_fechaCobro) # Por si
    # alguien se lía con el nombre, que no queda muy claro a qué se refiere.

    def actualizar_estado_cobro(cls):
        """
        Marca por defecto como cobrados todos los pagarés vencidos, pero
        respetando aquellos que ya se marcaron manualmente como pendientes.
        """
        actualizar_estado_cobro_de(cls)

    actualizar_estado_cobro = classmethod(actualizar_estado_cobro)

    @property
    def remesa(self):
        """
        Devuelve la remesa confirmada a la que pertenece el pagaré. Si está en
        varias remesas no confirmadas o en ninguna, devuelve None.
        """
        try:
            return [r for r in self.efecto.remesas if r.aceptada][0]
        except (AttributeError, IndexError):
            return None

    def get_estado(self, fecha = mx.DateTime.today()):
        """
        Devuelve el estado del pagaré:
        0: Gestión de cobro: Entregado al banco al vencimiento y esperando a
                             que nos hagan efectivo el importe.
        1: En cartera: Disponible para negociar o en remesa no enviada al banco.
        2: Descontado: En remesa.
        3: Impagado: Pasó la fecha de vto. y no se ha cobrado.
        4: Cobrado: Cobrado al vencimiento o en la remesa.
        """
        if self.remesa:
            if self.remesa.fechaCobro and self.remesa.fechaCobro <= fecha:
                return COBRADO
            elif self.remesa and not self.remesa.fechaPrevista:
                return CARTERA
            else:
                return DESCONTADO
        elif self.esta_pendiente() and self.fechaCobro < fecha:
            return IMPAGADO
        elif not self.esta_pendiente() and self.fechaCobrado <= fecha:
            return COBRADO
        else:
            return CARTERA
        # TODO: Falta el estado GESTION

    def get_str_estado(self):
        """
        Estados:
            Gestión de cobro -> Se lleva al banco para cobrar al vencimiento.
            En cartera -> Pagaré disponible para negociar en remesa.
            Descontado -> Pagaré en remesa.
            Impagado -> Pasa la fecha de vencimiento y no se ha cobrado.
            Cobrado -> Pasa la fecha de vencimiento y se ha cobrado o la
                       remesa se ha aceptado.
        """
        ESTADOS = ("Gestión de cobro",
                   "En cartera",
                   "Descontado",
                   "Impagado",
                   "Cobrado")
        estado = self.get_estado()
        str_estado = ESTADOS[estado]
        return str_estado

cont, tiempo = print_verbose(cont, total, tiempo)

class Confirming(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    cobros = MultipleJoin('Cobro')
    documentos = MultipleJoin('Documento')
    #--------------------------------------------- bancoID = ForeignKey('Banco')
    #------------------------------------------ #remesaID = ForeignKey('Remesa')
    efectos = MultipleJoin("Efecto")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    @property
    def remesado(self):
        """
        True si está en una remesa confirmada. Condiciones para ello:
        * Que estén tengan un efecto relacionado.
        * Que el efecto esté en una remesa.
        * Que la remesa esté confirmada (aceptada = True).
        """
        try:
            return reduce(lambda x, y: x and y,
                          [r.aceptada for r in self.efecto.remesas])
        except (AttributeError, TypeError): # No efecto o efecto pero no remesa.
            return False

    def get_efecto(self):
        try:
            return self.efectos[0]
        except IndexError:
            efecto = Efecto(pagareCobro = None,
                            confirming = self,
                            cuentaBancariaCliente = None)
            return efecto

    def set_efecto(self, value_efecto):
        value_efecto.pagareCobro = None
        value_efecto.confirming = self

    efecto = property(get_efecto, set_efecto)

    def esta_pendiente(self, fecha_base = mx.DateTime.today()):
        """
        Devuelve True si el confirming ya se ha cobrado completamente.
        OJO: Un confirming está cobrado si la cantidad de cobro no es menor
        al importe o si la fecha «fecha_base» (generalmente la actual del
        sistema) es superior a la fecha de vencimiento.
        OJO: Si la fecha de comprobación «fecha_base» es la del sistema,
        actualizará la cantidad cobrada para ajustarla al importe si además
        es superior a la de vencimiento (fecha_cobro).
        """
        if fecha_base == mx.DateTime.today() and fecha_base >= self.fechaCobro:
            self.cobrado = self.cantidad
            # Si se ha cobrado pero no tengo fecha de cobro, esto es un sindiós
            if not self.fechaCobrado:
                self.fechaCobrado = fecha_base
            self.syncUpdate()
        res = self.cobrado < self.cantidad #or fecha_base < self.fechaCobro
            # Si se adelanta el confirming, ya no está pendiente.
        return res

    def get_cantidad_pendiente(self):
        return self.cantidad - self.cobrado

    def set_cantidad_pendiente(self, pendiente):
        """
        Modifica la cantidad cobrada para que quede como pendiente
        la cantidad recibida.
        """
        self.cobrado = self.cantidad - pendiente

    def get_cliente(self):
        """
        Devuelve el objeto cliente relacionado con el pagaré a través de
        "cobros". Si no tiene, devuelve None.
        """
        res = None
        if len(self.cobros) > 0:
            res = self.cobros[0].cliente
        return res

    def get_fechaCobro(self):
        return self.fechaCobro

    def set_fechaCobro(self, fecha):
        self.fechaCobro = fecha
        self.syncUpdate()

    pendiente = property(esta_pendiente, doc = "Valor booleano que devuelve si el pagaré está completamente pagado (False) o no -tiene algo o todo pendiente de cobrar (True)-.")
    cantidad_pendiente = property(get_cantidad_pendiente, set_cantidad_pendiente, doc = "Cantidad pendiente de cobrar del total del pagaré")
    cliente = property(get_cliente, doc = "Devuelve el objeto Cliente relacionado con el pagaré.")
    fechaVencimiento = property(get_fechaCobro, set_fechaCobro) # Por si
    # alguien se lía con el nombre, que no queda muy claro a qué se refiere.

    def actualizar_estado_cobro(cls):
        """
        Marca por defecto como cobrados todos los pagarés vencidos, pero
        respetando aquellos que ya se marcaron manualmente como pendientes.
        """
        actualizar_estado_cobro_de(cls)

    actualizar_estado_cobro = classmethod(actualizar_estado_cobro)

    @property
    def remesa(self):
        try:
            return [r for r in self.efecto.remesas if r.aceptada][0]
        except (AttributeError, IndexError):
            return None
    #    try:
    #        return self.efecto.remesa
    #    except AttributeError:
    #        Efecto(pagareCobro = None,
    #               confirming = self,
    #               cuentaBancariaCliente = None)

    def get_estado(self, fecha = mx.DateTime.today()):
        """
        Devuelve el estado del confirming:
        0: Gestión de cobro: En el banco esperando al vencimiento.
        1: En cartera: Disponible para negociar.
        2: Descontado: En remesa.
        3: Impagado: Pasó la fecha de vto. y no se ha cobrado.
        4: Cobrado: Cobrado al vencimiento o en la remesa.
        """
        if self.remesa:
            if self.remesa.fechaCobro and self.remesa.fechaCobro <= fecha:
                return COBRADO
            else:
                return DESCONTADO
        elif self.esta_pendiente() and self.fechaCobro < fecha:
            return IMPAGADO
        elif not self.esta_pendiente() and (self.fechaCobrado
                                            and self.fechaCobrado <= fecha):
            return COBRADO
        else:
            return CARTERA
        # TODO: Falta el estado GESTION

    def get_str_estado(self):
        """
        Estados:
            Gestión de cobro -> Se lleva al banco para cobrar al vencimiento.
            En cartera -> Pagaré disponible para negociar en remesa.
            Descontado -> Pagaré en remesa.
            Impagado -> Pasa la fecha de vencimiento y no se ha cobrado.
            Cobrado -> Pasa la fecha de vencimiento y se ha cobrado o la
                       remesa se ha aceptado.
        """
        ESTADOS = ("Gestión de cobro",
                   "En cartera",
                   "Descontado",
                   "Impagado",
                   "Cobrado")
        estado = self.get_estado()
        str_estado = ESTADOS[estado]
        return str_estado

cont, tiempo = print_verbose(cont, total, tiempo)

class EstimacionCobro(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #------------------------------- facturaVentaID = ForeignKey('FacturaVenta')
    #------------------- prefacturaID = ForeignKey('Prefactura', default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_factura_o_prefactura(self):
        """
        Devuelve la factura relacionada, tanto si es facturaVenta
        como prefactura, o None si no tiene ninguna de ellas.
        Como no debería tener ambos valores distintos de nulo a
        la vez, tiene preferencia facturaVenta sobre prefactura.
        """
        return self.facturaVenta or self.prefactura

cont, tiempo = print_verbose(cont, total, tiempo)

class TipoMaterialBala(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class Bigbag(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- loteCemID = ForeignKey('LoteCem')
    articulos = MultipleJoin('Articulo')
    #----- parteDeProduccionID = ForeignKey("ParteDeProduccion", default = None)
        # Parte donde se consume para embolsar.

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_analizado(self):
        """
        Devuelve True si el  lote de cemento al que pertence
        el bigbag ya ha sido analizado.
        Se considera analizado si al menos se le han hecho las dos
        pruebas de elongación y tenacidad.
        """
        res = False
        c = self.loteCem
        if c != None:
            res = c.tenacidad != None and c.elongacion != None
        return res

    def get_articulo(self):
        """
        Devuelve el artículo asociado al bigbag.
        """
        return self.articulos[0]

    def get_articuloID(self):
        """
        Devuelve el identificador del artículo asociado al bigbag o None.
        """
        return self.articulos and self.articulos[0].id or None

    articulo = property(get_articulo)
    articuloID = property(get_articuloID)

    def set_productoVenta(self, producto):
        """
        Instancia el producto del artículo relacionado con el rollo.
        """
        if not isinstance(producto, ProductoVenta):
            raise ValueError
        self.articulos[0].productoVenta = producto

    def get_productoVenta(self):
        """
        Devuelve el producto relacionado con el rollo a través del artículo.
        """
        try:
            return self.articulos[0].productoVenta
        except IndexError:
            return None

    productoVenta = property(get_productoVenta, set_productoVenta)

    def get_albaranSalida(self):
        """
        Devuelve el albarán de salida del artículo relacionado con el bigbag.
        """
        return self.articulos[0].albaranSalida

    def set_albaranSalida(self, albaranSalida):
        """
        Establece el albarán de salida del artículo relacionado con el bigbag.
        """
        self.articulos[0].albaranSalida = albaranSalida

    def get_albaranSalidaID(self):
        """
        Devuelve el ID albarán de salida del artículo relacionado con el bigbag o None.
        """
        return self.articulos[0].albaranSalidaID

    def set_albaranSalidaID(self, albaranSalidaID):
        """
        Establece el id de albarán de salida del artículo relacionado con el bigbag.
        """
        self.articulos[0].albaranSalidaID = albaranSalidaID

    albaranSalida = property(get_albaranSalida, set_albaranSalida)
    albaranSalidaID = property(get_albaranSalidaID, set_albaranSalidaID)

    def set_peso(self, p):
        self.pesobigbag = p

    peso = property(lambda self: self.pesobigbag, set_peso)

cont, tiempo = print_verbose(cont, total, tiempo)

#class Bolsa(SQLObject, PRPCTOO):
#    _connection = conn
#    _fromDatabase = True
#    cajaID = ForeignKey('Caja')
#    articulos = MultipleJoin('Articulo')
#
#    def _init(self, *args, **kw):
#        starter(self, *args, **kw)
#
#    def get_puid(self):
#        """
#        Identificador único en la BD para cada objeto de esta clase.
#        OJO: No lleva el mismo formato que los usados hasta ahora, aunque sí
#        asegura que sigue siendo único.
#        """
#        # Voy a hacer unas pruebas con esta versión alfa de puid. Llevará
#        # nombre de la clase, dos puntos, y el identificador. Así a partir de
#        # un puid puedo cargar el objeto sin tener conocimiento a priori de
#        # qué es. Las 4 clases nuevas de líneas de embolsado van a funcionar
#        # así. Si funciona bien, migraré todas las clases.
#        return "Bolsa:%d" % self.id
#
#    def get_next_numbolsa(clase):
#        """
#        Devuelve el entero correspondiente al siguiente número de bolsa y
#        su código de trazabilidad.
#        """
#        maxi = clase._connection.queryOne("SELECT MAX(numbolsa) FROM bolsa;")[0]
#        try:
#            res = maxi + 1
#        except TypeError:   # No hay bolsas creadas:
#            res = 1
#        return res, "K%d" % res
#
#    get_next_numbolsa = classmethod(get_next_numbolsa)
#
#    def get_bigbag_origen(self):
#        """
#        Devuelve el bigbag que contenía la fibra que contiene esta bolsa.
#        """
#        # Necesitamos el parte de producción, y de ahí sacar el consumo de
#        # bigbags. El bigbag origen será el que, ordenando por ID tanto
#        # bolsas fabricadas como bigbags, coincida con el peso de las bolsas
#        # fabricadas menos los bigbags consumidos. Es más fácil verlo en
#        # código que explicarlo.
#        # OJO: Ordeno por ID para que sea determinista, pero en realidad sería
#        # más correcto ordenar por fecha y hora *de consumo*. Pero como ese
#        # dato no se guarda y en teoría los bigbags que se carguen son todos
#        # iguales, y además se consideran analizados todos los bigbags del
#        # mismo lote; siempre y cuando no necesitemos tanta granuralidad,
#        # esta forma de relacionar bolsas y bigbags es perfectamente válida.
#        if DEBUG:
#            myprint("CARIIIÑO, YA ESTOY EN CASA.")
#        pdp = self.articulos[0].parteDeProduccion
#        bbs = pdp.bigbags[:]
#        res = None
#        if len(bbs):    # No debería ocurrir, pero por si acaso. Cada parte
#                        # al menos habrá empezado un bigbag.
#            bolsas = [a.bolsa for a in pdp.articulos] #Al menos voy a estar yo.
#            bbs.sort(lambda b1, b2: int(b1.id - b2.id))
#            bolsas.sort(lambda b1, b2: int(b1.id - b2.id))
#            # OJO: Peso de las bolsas en y BBs en kg.
#            tmp_peso_bb_actual = bbs[0].pesobigbag
#            res = bbs.pop(0)
#            pos_bolsa_actual = bolsas.index(self)
#            pos = 0
#            while pos < pos_bolsa_actual:
#                tmp_peso_bb_actual -= bolsas[pos].peso #/1000.0  # En kg, no gr
#                pos += 1
#                if tmp_peso_bb_actual <= 0.0:
#                    try:
#                        res = bbs.pop(0)
#                    except IndexError:
#                        break   # No quedan Bigbags, asumo el último.
#                    tmp_peso_bb_actual = res.peso + abs(tmp_peso_bb_actual)
#        return res
#
#    def get_analizada(self):
#        """
#        Devuelve True si la fibra del bigbag origen que ha sido
#        embolsada aquí ha sido analizada.
#        OJO: TODO: De momento vamos a ignorar las pruebas anuales.
#        OJO: TODO 2: Siempre va a devolver que está analizada, hasta que se
#        decida lo contrario, por motivos de eficiencia.
#        """
#        # XXX
#        res = True
#        # XXX
#        # Vamos a considerar una bolsa como analizada cuando lo esté la
#        # fibra que contiene, es decir, el bigbag de procedencia.
#        #bb = self.get_bigbag_origen()
#        #res = bb.get_analizado()
#        return res
#
#    def get_articulo(self):
#        """
#        Devuelve el artículo asociado a la bolsa.
#        """
#        return self.articulos[0]
#
#    def get_articuloID(self):
#        """
#        Devuelve el identificador del artículo asociado a la bolsa o None.
#        """
#        return self.articulos and self.articulos[0].id or None
#
#    articulo = property(get_articulo)
#    articuloID = property(get_articuloID)
#
#    def get_albaranSalida(self):
#        """
#        Devuelve el albarán de salida del artículo relacionado con la bolsa.
#        """
#        return self.articulos[0].albaranSalida
#
#    def set_albaranSalida(self, albaranSalida):
#        """
#        Establece el albarán de salida del artículo relacionado con la bolsa.
#        """
#        self.articulos[0].albaranSalida = albaranSalida
#
#    def get_albaranSalidaID(self):
#        """
#        Devuelve el ID albarán de salida del artículo relacionado con la bolsa
#        o None.
#        """
#        return self.articulos[0].albaranSalidaID
#
#    def set_albaranSalidaID(self, albaranSalidaID):
#        """
#        Establece el id de albarán de salida del artículo relacionado con la
#        bolsa.
#        """
#        self.articulos[0].albaranSalidaID = albaranSalidaID
#
#    albaranSalida = property(get_albaranSalida, set_albaranSalida)
#    albaranSalidaID = property(get_albaranSalidaID, set_albaranSalidaID)
#
#    def en_almacen(self, fecha = None, almacen = None):
#        return self.articulo.en_almacen(fecha, almacen)
#
#    def get_partidaCem(self):
#        return self.articulo.partidaCem
#
#    partidaCem = property(get_partidaCem)
#    partidaCemID = property(lambda self: self.articulo.partidaCemID)
#
#cont, tiempo = print_verbose(cont, total, tiempo)

class LoteCem(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    bigbags = MultipleJoin('Bigbag')
    muestras = MultipleJoin('Muestra')
    pruebasTenacidad = MultipleJoin('PruebaTenacidad')
    pruebasElongacion = MultipleJoin('PruebaElongacion')
    pruebasHumedad = MultipleJoin('PruebaHumedad')
    pruebasEncogimiento = MultipleJoin('PruebaEncogimiento')
    pruebasGrasa = MultipleJoin('PruebaGrasa')
    pruebasTitulo = MultipleJoin('PruebaTitulo')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    @property
    def productoVenta(self):
        return self.get_productoVenta()

    def calcular_media_pruebas(self, pruebas):
        """
        Devuelve la media del campo resultados de
        la lista de pruebas recibidas.
        """
        denominador = len(pruebas)
        numerador = sum([prueba.resultado for prueba in pruebas])
        try:
            return numerador / denominador
        except ZeroDivisionError:
            return 0

    calcular_tenacidad_media = lambda self: self.calcular_media_pruebas(
                                                    self.pruebasTenacidad)
    calcular_elongacion_media = lambda self: self.calcular_media_pruebas(
                                                    self.pruebasElongacion)
    calcular_humedad_media = lambda self: self.calcular_media_pruebas(
                                                    self.pruebasHumedad)
    calcular_encogimiento_medio = lambda self: self.calcular_media_pruebas(
                                                    self.pruebasEncogimiento)
    calcular_grasa_media = lambda self: self.calcular_media_pruebas(
                                                    self.pruebasGrasa)
    calcular_titulo_medio = lambda self: self.calcular_media_pruebas(
                                                    self.pruebasTitulo)

    def update_valor(self, caracteristica):
        """
        Actualiza el valor de la característica "característica"
        sumando de nuevo todos los resultados de las pruebas y
        dividiéndolo entre el total de pruebas de ese tipo (media
        aritmética).
        """
        try:
            lista_pruebas = getattr(self, "pruebas%s" % (
                                    caracteristica.title()))
            try:
                media = ((sum([p.resultado for p in lista_pruebas]) * 1.0)
                         / len(lista_pruebas))
            except ZeroDivisionError:   # No hay pruebas de esa característica.
                media = None
            setattr(self, caracteristica, media)
        except AttributeError:
            myprint("pclases::class LoteCem::update_valor-> El atributo %s no"
                    " es correcto." % (caracteristica))

    def get_productoVenta(self):
        """
        Devuelve el producto de venta al que pertenece
        el lote o None si no tiene producción.
        """
        if self.bigbags:
            producto = self.bigbags[0].articulo.productoVenta
        else:
            producto = None
        return producto

    def set_productoVenta(self, productoVenta):
        """
        Hace que el producto de venta de todas las bigbags
        del lote sea el recibido.
        """
        if not isinstance(productoVenta, ProductoVenta):
            raise TypeError, "El producto debe ser un objeto de la clase "\
                             "ProductoVenta."
        for b in self.bigbags:
            b.articulo.productoVenta = productoVenta

    productoVenta = property(get_productoVenta, set_productoVenta,
                    "Producto de venta relacionado con el lote de cemento.")

    def esta_analizada(self):
        """
        Devuelve True si el lote está analizado (tiene al menos un valor en
        los resultados de las pruebas).
        """
        valores_nulos = (' ', '', None)
        return ((self.tenacidad not in valores_nulos)
                or (self.elongacion not in valores_nulos)
                or (self.encogimiento not in valores_nulos))

cont, tiempo = print_verbose(cont, total, tiempo)

class Pale(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------- partidaCemID = ForeignKey('PartidaCem')
    cajas = MultipleJoin('Caja')

    # Un par de constantes para valores por defecto:
    NUMCAJAS = 14  # Valor por defecto también en la BD. No va a
                                # cambiar (o eso dicen).
    NUMBOLSAS = 40  # Es el ideal que deberían entrar a no ser que el
                    # producto indique lo contrario.

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_puid(self):
        """
        Identificador único en la BD para cada objeto de esta clase.
        OJO: No lleva el mismo formato que los usados hasta ahora, aunque sí
        asegura que sigue siendo único.
        """
        # Voy a hacer unas pruebas con esta versión alfa de puid. Llevará
        # nombre de la clase, dos puntos, y el identificador. Así a partir de
        # un puid puedo cargar el objeto sin tener conocimiento a priori de
        # qué es. Las 4 clases nuevas de líneas de embolsado van a funcionar
        # así. Si funciona bien, migraré todas las clases.
        return "Pale:%d" % self.id

    def completo_en_almacen(self, almacen = None):
        """
        Devuelve True si el palé está por completo en el almacén.
        """
        return len(self.cajas) == self.cajas_en_almacen(almacen = almacen)

    def cajas_en_almacen(self, almacen = None):
        res = []
        for c in self.cajas:
            if almacen and c.en_almacen(almacen = almacen):
                res.append(c)
            elif not almacen and c.en_almacen():
                res.append(c)
        return res

    def en_almacen(self, almacen = None):
        """
        Devuelve la proporción de cajas del palé que siguen en almacén.
        """
        return (len(self.cajas_en_almacen(almacen)) * 1.0) / len(self.cajas)

    def es_clase_b(self, force_no_cache = False):
        """
        Devuelve True si el palé contiene fibra B. Basta con que se marque
        una bolsa de alguna caja del palé como B para todo el palé se
        convierta en clase B.
        Aquí no se modifican las bolsas. Aunque se considere todo el palé como
        clase B puede que contenga bolsas que no tienen claseb a True.
        parámetro «force_no_cache» DEPRECATED.
        """
        # XXX: Este es el criterio que se definió para hacer las bolsas de un
        # palé como clase B. ¿Por qué no usarlo ahora para determinar si un
        # palé completo es B en lugar de andar con algortimos de O(n²)?
        pv = self.productoVenta
        if not pv:
            claseb = self.numbolsas < Pale.NUMBOLSAS
        else:
            try:
                claseb = self.numbolsas < pv.camposEspecificosBala.bolsasCaja
            except AttributeError:
                claseb = self.numbolsas < Pale.NUMBOLSAS
        return claseb
        #return self.numbolsas != Pale.NUMBOLSAS
        # Todo esto de aquí abajo ya no haría falta, pero lo dejo por si
        # las moscas, que nunca se sabe cuándo cambiará el criterio de
        # clase B.
        # Que un palé sea clase B no es variable desde el momento que se
        # fabrica la primera caja, así que lo guardaré en un caché.
        #try:
        #    if force_no_cache:
        #        raise NameError # Por poner alguna.
        #    return self.__cache_claseb
        #except (NameError, AttributeError):
        #    bolsasb = []
        #    for caja in self.cajas:
        #        for bolsa in caja.bolsas:
        #            if bolsa.claseb:
        #                self.__cache_claseb = True
        #                return True
        #self.__cache_claseb = False
        #return False

    claseb = property(es_clase_b)

    def get_next_numpale(cls, numbolsas = None, numpale = None):
        """
        Devuelve el entero correspondiente al siguiente número de palé y
        su código de trazabilidad en función del número de bolsas.
        """
        if numbolsas is None:   # Debe ser None. Aceptaría cero.
            numbolsas = cls.NUMBOLSAS
        if numpale is None:
            maxi = cls._connection.queryOne(
                                        "SELECT MAX(numpale) FROM pale;")[0]
            try:
                res = maxi + 1
            except TypeError:   # No hay palés creados:
                res = 1
        else:
            res = numpale
        return res, "H%d/%d" % (res, numbolsas)

    get_next_numpale = classmethod(get_next_numpale)

    def get_productoVenta(self):
        """
        Devuelve el producto de venta relacionado con el palé a través de la
        caja, bolsa y artículo.
        """
        # Y si salta alguna excepción por faltar alguna relación, prefiero
        # comérmela y que casque el programa para coscarme, porque no debería
        # ocurrir.
        return self.cajas[0].articulo.productoVenta

    productoVenta = property(get_productoVenta)

    def calcular_peso(self):
        """
        Fácil, el peso por bolsa por el número de bolsas por caja por el
        número de cajas. OJO: Da igual que falten bolsas, que alguna tenga
        otro peso o lo que sea. Siempre va a devolver el peso teórico del
        palé completo.
        Devuelve el peso en kilogramos.
        """
        if (self.observaciones
            or self.es_clase_b()):
            # Por si acaso tiene alguna caja con menos bolsas o algo.
            res = sum([c.numbolsas for c in self.cajas])
        else:
            res = self.numbolsas * self.numcajas
        try:
            res *= self.__cache_gramos_bolsa
        except (NameError, AttributeError):
            pv = self.productoVenta
            self.__cache_gramos_bolsa = pv.camposEspecificosBala.gramosBolsa
            res *= self.__cache_gramos_bolsa
        return res / 1000.0

    def get_cajas_en_almacen(self, almacen = None):
        """
        Devuelve los registros correspondientes a las cajas que
        estén en el almacén recibido (o en cualquiera de ellos si es None)
        relacionadas con las cajas del palé.
        """
        if almacen:
            query = " almacen_id = %d " % almacen.id
        else:
            query = " almacen_id IS NOT NULL "
        query += """
        AND caja_id IS NOT NULL AND caja_id IN
            (SELECT id FROM caja WHERE pale_id = %d)
        """ % self.id
        articulos = Articulo.select(query)
        cajas = [a.caja for a in articulos]
        return cajas

    def get_parte_de_produccion(self):
        """
        Devuelve el parte de producción al que pertenece el palé.
        """
        # Usaré el parte de una de las cajas. Aunque
        # se puedan vender por separado, se fabrican juntas y por palés
        # completos que no se dividirán entre dos turnos aunque físicamente
        # se pueda dar el caso.
        return self.cajas[0].articulo.parteDeProduccion

    def set_parte_de_produccion(self, pdp):
        articulos = Articulo.select(AND(Articulo.q.cajaID == Caja.q.id,
                                        Caja.q.paleID == self.id))
        for a in articulos:
            if isinstance(pdp, int):
                a.parteDeProduccionID = pdp
            elif isinstance(pdp, ParteDeProduccion):
                a.parteDeProduccionID = pdp.id
            else:
                raise TypeError, "pclases.py::Pale::set_parte_de_produccion: "\
                                 "El parámetro debe ser un entero o un "\
                                 "objeto ParteDeProduccion"

    parteDeProduccion = property(get_parte_de_produccion,
                                 set_parte_de_produccion)

    def crear_pale(parteDeProduccion, numpale = None, partidaCem = None,
                   productoVenta = None, numbolsas = None, numcajas = None):
        """
        Crea un palé con todas las cajas y bolsas que contiene.
        """
        from formularios import partes_de_fabricacion_rollos
        if not partidaCem:
            partidaCem = parteDeProduccion.partidaCem
            if not partidaCem:
                raise ValueError, "pclases.py::crear_pale -> No se pudo "\
                    "determinar partida de cemento. Especifique una."
        if productoVenta == None:
            productoVenta = parteDeProduccion.productoVenta
        if not productoVenta:
            raise ValueError, "pclases.py::crear_pale -> No se pudo "\
                "determinar producto de venta. Especifique uno."
        if numbolsas is None:
            numbolsas = productoVenta.camposEspecificosBala.bolsasCaja
            if not numbolsas:
                raise ValueError, "pclases.py::crear_pale -> No se pudo "\
                    "determinar el número de bolsas por caja. Especifique "\
                    "una cantidad."
        listanumbolsas = [numbolsas]
        for numbolsas in listanumbolsas:
            if not numcajas:
                try:
                    ceb = productoVenta.camposEspecificosBala
                    numcajasdefecto = ceb.cajasPale
                except AttributeError:
                    numcajasdefecto = Pale.NUMCAJAS
            else:
                numcajasdefecto = numcajas
            # 1.- Creo el palé.
            numpale, codigo = Pale.get_next_numpale(numbolsas, numpale)
            pale = Pale(partidaCem = partidaCem,
                    numpale = numpale,
                    codigo = codigo,
                    fechahora = mx.DateTime.localtime(),
                    numbolsas = numbolsas,
                    numcajas = numcajasdefecto
                    )
            # 2.- Creo las cajas.
            for i in range(pale.numcajas):  # @UnusedVariable
                caja = Caja.crear_caja(parteDeProduccion, pale,
                                       numbolsas)
            # OJO: Le paso el último artículo porque la formulación de esta
            # línea será por PALÉS COMPLETOS.
            class FakeVentanaPartes:
                def __init__(self, objeto):
                    self.objeto = objeto
            try:
                partes_de_fabricacion_rollos.descontar_material_adicional(
                                        FakeVentanaPartes(parteDeProduccion),
                                        caja.articulo)
                parteDeProduccion.buscar_o_crear_albaran_interno(
                    incluir_consumos_auto = True) # Normalmente no, pero
                    # aquí sí quiero que aparezcan en el alb. interno.
            except (UnboundLocalError, NameError):
                pass # No se ha creado ninguna caja.
        return pale
    crear_pale = staticmethod(crear_pale)


cont, tiempo = print_verbose(cont, total, tiempo)

class Caja(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------------- paleID = ForeignKey('Pale')
    #bolsas = MultipleJoin('Bolsa')
    articulos = MultipleJoin("Articulo")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def OLD_get_peso(self):
        """
        DEPRECATED
        """
        pv = self.articulos[0].productoVenta
        pesobolsa = pv.camposEspecificosBala.gramosBolsa
        res = self.numbolsas * pesobolsa    # OJO:Desprecio el peso del cartón.
        res /= 1000.0    # En kg, please.
        return res

    def get_articulo(self):
        return self.articulos[0]

    def set_articulo(self, articulo, syncUpdate = False, sync = False):
        articulo.caja = self
        if syncUpdate and articulo:
            articulo.syncUpdate()
        if sync and articulo:
            articulo.sync()

    def es_clase_b(self):
        """
        Caja es clase B si el palé al que pertenece lo es.
        ACTUALIZACIÓN: Caja es clase B si tiene menos bolsas de las que
        indica su producto como estándar.
        """
        #return self.pale.es_clase_b()
        sql = "SELECT caja_es_clase_b(%d);" % self.id
        res = self._connection.queryOne(sql)
        res = bool(res[0])
        return res

    #peso = property(get_peso)
    articulo = property(get_articulo, set_articulo)
    claseb = property(es_clase_b)

    def get_analizada(self):
        # TODO: De momento siempre va a devolver que sí por motivos de
        # eficiencia*. Ver el código de get_analizada() comentado en las
        # -extintas- bolsas.
        # * E incompletitud, porque ahora todos los métodos de las bolsas
        # habrá que traerlos aquí.
        return True

    def get_puid(self):
        """
        Identificador único en la BD para cada objeto de esta clase.
        OJO: No lleva el mismo formato que los usados hasta ahora, aunque sí
        asegura que sigue siendo único.
        """
        # Voy a hacer unas pruebas con esta versión alfa de puid. Llevará
        # nombre de la clase, dos puntos, y el identificador. Así a partir de
        # un puid puedo cargar el objeto sin tener conocimiento a priori de
        # qué es. Las 4 clases nuevas de líneas de embolsado van a funcionar
        # así. Si funciona bien, migraré todas las clases.
        return "Caja:%d" % self.id

    def get_next_numcaja(cls):
        """
        Devuelve el entero correspondiente al siguiente número de caja y
        su código de trazabilidad.
        """
        maxi = cls._connection.queryOne("SELECT MAX(numcaja) FROM caja;")[0]
        try:
            res = maxi + 1
        except TypeError:   # No hay cajas creadas:
            res = 1
        return res, "J%d" % res

    get_next_numcaja = classmethod(get_next_numcaja)

    def calcular_peso(self):
        """
        Devuelve el peso teórico de la caja.
        """
        try:
            numbolsas = self.pale.numbolsas
        except AttributeError:  # Solo por si acaso
            numbolsas = self.productoVenta.camposEspecificosBala.bolsasCaja
        pesobolsa = self.productoVenta.camposEspecificosBala.gramosBolsa
        res = numbolsas * pesobolsa / 1000.0    # En kg, please.
        return res

    get_peso_teorico = calcular_peso
    peso_teorico = property(get_peso_teorico)

    def en_almacen(self, fecha = None, almacen = None):
        """
        Una caja está entera en almacén o no lo está
        """
        return self.articulo.en_almacen(fecha, almacen)

    def get_albaranSalida(self, use_cache = False):
        """
        Devuelve el albarán de salida relacionado con la caja a través de una
        (arbitrariamente) de sus bolsas. En teoría una caja no es fraccionable.
        ACTUALIZACIÓN: Y desde septiembre de 2009, en la práctica tampoco.
        """
        #if not use_cache:
        #    a = self.bolsas[0].articulo
        #    a.sync()
        #    self.__cache_albaranSalida = a.albaranSalida
        #try:
        #    res = self.__cache_albaranSalida
        #except (NameError, AttributeError):
        #    self.__cache_albaranSalida=self.bolsas[0].articulo.albaranSalida
        #    res = self.__cache_albaranSalida
        #return res
        return self.articulo.albaranSalida

    def get_albaranSalidaID(self, use_cache = True):
        """
        Devuelve el ID del albarán relacionado con la caja a través de una
        (arbitrariamente) de sus bolsas. En teoría una caja no es fraccionable.
        """
        #if not use_cache:
        #    a = self.bolsas[0].articulo
        #    a.sync()
        #    self.__cache_albaranSalida = a.albaranSalidaID
        #try:
        #    res = self.__cache_albaranSalida
        #except (NameError, AttributeError):
        #    self.__cache_albaranSalida=self.bolsas[0].articulo.albaranSalidaID
        #    res = self.__cache_albaranSalida
        #return res
        alb = self.get_albaranSalida()
        if alb:
            return alb.id
        else:
            return None

    def set_albaranSalida(self, alb):
        """
        Almacena el albarán de salida relacionado con la caja a través de
        sus bolsas. En teoría una caja no es fraccionable.
        """
        #for bolsa in self.bolsas:
        #    bolsa.articulo.albaranSalida = alb
        self.articulo.albaranSalida = alb

    def set_albaranSalidaID(self, albid):
        """
        Almacena el identificador del albarán relacionado con la caja a través
        de sus bolsas. En teoría una caja no es fraccionable.
        """
        #for bolsa in self.bolsas:
        #    bolsa.articulo.albaranSalidaID = albid
        if isinstance(albid, AlbaranSalida):
            albid = albid.id
        self.articulo.albaranSalidaID = albid

    albaranSalida = property(get_albaranSalida, set_albaranSalida)
    albaranSalidaID = property(get_albaranSalidaID, set_albaranSalidaID)

    def get_productoVentaID(self):
        """
        Devuelve el ID del producto de venta relacionado con la caja a través
        del artículo. En teoría todas las bolsas deben ser del
        mismo producto de venta.
        Si la caja está vacía devuelve None.
        """
        try:
            return self.articulos[0].productoVentaID
        except IndexError:
            return None

    def get_productoVenta(self):
        try:
            return self.articulos[0].productoVenta
        except:
            return None

    productoVenta = property(get_productoVenta)
    productoVentaID = property(get_productoVentaID)

    def get_partidaCemID(self):
        """
        Devuelve la partida relacionada con la caja a través de la primera
        de sus bolsas. None si está vacía.
        """
        try:
            return self.articulos[0].partidaCemID
        except IndexError:
            return None

    def get_partidaCem(self):
        try:
            return self.articulos[0].partidaCem
        except:
            return None

    partidaCem = property(get_partidaCem)
    partidaCemID = property(get_partidaCemID)

    def get_bounds_numbolsa(self):
        """
        Devuelve el primer y último número de bolsa que se incluyen en la caja.
        """
        # ¿A partir de qué número de bolsa va en esta caja?
        cajas_anteriores = Caja.select(Caja.q.numcaja < self.numcaja)
        # ¿Y hasta dónde llega?
        cajas_conmigo = Caja.select(Caja.q.numcaja <= self.numcaja)
        try:
            bolsas_anteriores = cajas_anteriores.sum("numbolsas")
        except TypeError: # Número de caja no válido. No se pudo hacer el sum.
            bolsas_anteriores = 0
        if bolsas_anteriores is None:
            bolsas_anteriores = 0
        primera = bolsas_anteriores + 1
        ultima = cajas_conmigo.sum("numbolsas")
        if ultima is None:
            ultima = 0
        return primera, ultima  # Ambas incluidas.

    def _get_bounds_numbolsa_range(self):
        """
        Devuelve el primer número de bolsa de esta caja y el primero de la
        siguiente.
        Es como el get_bounds_numbolsa pero adaptado al [x]range de python
        para usar como función auxiliar en otros algoritmos.
        """
        p, u = self.get_bounds_numbolsa()
        return p, u+1

    def get_bolsas(self):
        """
        Devuelve un diccionario con los números de bolsas que se supone
        van en la caja, así como sus códigos de trazabilidad y peso.
        """
        primera, ultima = self.get_bounds_numbolsa()
        numsbolsas = range(primera, ultima + 1)
        databolsas = []
        try:
            ceb = self.productoVenta.camposEspecificosBala
            peso_bolsa_en_kg = ceb.gramosBolsa
        except AttributeError, msg:
            # O no es un producto de fibra de cemento o está mal dado de alta.
            myprint("El palé %s tiene un producto de venta relacionado "\
                  "inválido. Excepción AttributeError: %s" % (self.get_puid(),
                                                              msg))
            peso_bolsa_en_kg = 0
        peso_bolsa_en_kg /= 1000.0   # En kg
        for numbolsa in numsbolsas:
            databolsas.append({"código": "K%d" % numbolsa,
                               "peso": peso_bolsa_en_kg})
        res = dict(zip(numsbolsas, databolsas))
        return res

    def get_caja_from_bolsa(numbolsa):
        """
        Devuelve el objeto caja relacionado con un número o un código de bolsa.


        >>> from framework import pclases
        >>> i = 1
        >>> i in pclases.Caja.get_caja_from_bolsa(i).get_bolsas()
        True
        >>> i = 125
        >>> i in pclases.Caja.get_caja_from_bolsa(i).get_bolsas()
        True
        >>> i = 12345
        >>> i in pclases.Caja.get_caja_from_bolsa(i).get_bolsas()
        True
        >>> i = 12345678
        >>> i in pclases.Caja.get_caja_from_bolsa(i).get_bolsas()
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        AttributeError: 'NoneType' object has no attribute 'get_bolsas'

        """
        if not isinstance(numbolsa, int):
            numbolsa = utils.parse_numero(numbolsa)
            if not numbolsa:
                raise TypeError, "pclases.py::Caja::get_caja_from_bolsa -> "\
                                 "El parámetro numbolsa debe ser un entero."
        ## Algoritmo base: búsqueda secuencial. O(n)
        #for caja in Caja.select(orderBy = "numcaja"):
        #    if numbolsa in xrange(*caja._get_bounds_numbolsa_range()):
        #        break
        #if numbolsa not in xrange(*caja._get_bounds_numbolsa_range()):
        #    caja = None
        ## Algoritmo optimizado: Búsqueda binaria. O(log(n))
        izq = 0
        der = Caja.select().count()
        centro = (izq + der) / 2
        #################################################################
        def data_from(i):
            """
            Devuelve la lista de números de bolsa que hay en la caja i.
            """
            try:
                caja = Caja.selectBy(numcaja = i)[0]
                return xrange(*caja._get_bounds_numbolsa_range())
            except IndexError:
                return []
        #################################################################
        numsbolsas = data_from(centro)
        while ((izq <= der) and (numbolsa not in numsbolsas)):
            if numbolsa < numsbolsas[0]:
                der = centro - 1
            else:
                izq = centro + 1
            centro = (izq + der) / 2
            numsbolsas = data_from(centro)  # Va a hacer una comparación de
                                    # más en la última iteración, pero
                                    # O(n+1) ~= O(n), así que me da igual.
        if izq > der:
            caja = None
        else:
            caja = Caja.selectBy(numcaja = centro)[0]
        return caja

    get_caja_from_bolsa = staticmethod(get_caja_from_bolsa)

    def crear_caja(parteDeProduccion, pale, numbolsas = None):
        productoVenta = parteDeProduccion.productoVenta
        if not productoVenta:
            raise ValueError, "pclases.py::crear_caja -> No se pudo "\
                "determinar producto de venta. Especifique uno."
        if numbolsas is None:
            numbolsas = pale.numbolsas
            if not numbolsas:
                raise ValueError, "pclases.py::crear_caja -> No se pudo "\
                    "determinar el número de bolsas por caja. Especifique "\
                    "una cantidad."
        numcaja, codigo = Caja.get_next_numcaja()
        try:
            gramos = productoVenta.camposEspecificosBala.gramosBolsa
        except AttributeError:
            gramos = 0
        peso = (gramos * numbolsas) / 1000.0
        caja = Caja(pale = pale,
                    numcaja = numcaja,
                    codigo = codigo,
                    fechahora = mx.DateTime.localtime(),
                    peso = peso,
                    numbolsas = numbolsas)
        ## 3.- Creo los artículos.
        #for j in range(pale.numbolsas):
        #    numbolsa, codigo = Bolsa.get_next_numbolsa()
        #    ceb = productoVenta.camposEspecificosBala
        #    peso = (ceb.gramosBolsa / 1000.0)
        #    #claseb = Pale.NUMBOLSAS != pale.numbolsas
        #    bolsas_estandar = ceb.bolsasCaja
        #    if not bolsas_estandar:
        #        bolsas_estandar = Pale.NUMBOLSAS
        #    claseb = pale.numbolsas < bolsas_estandar
        #    bolsa = Bolsa(caja = caja,
        #                          numbolsa = numbolsa,
        #                          codigo = codigo,
        #                          fechahora = mx.DateTime.localtime(),
        #                          peso = peso,
        #                          claseb = claseb)
        articulo = Articulo(parteDeProduccion = parteDeProduccion,  # @UnusedVariable
                            caja = caja,
                            rolloDefectuoso = None,
                            albaranSalida = None,
                            productoVenta = productoVenta,
                            bala = None,
                            rollo = None,
                            bigbag = None,
                            almacen = Almacen.get_almacen_principal(),
                            rolloC = None,
                            balaCable = None)
        return caja
    crear_caja = staticmethod(crear_caja)

cont, tiempo = print_verbose(cont, total, tiempo)

class PartidaCem(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    partesDeProduccion = MultipleJoin('ParteDeProduccion')
    pales = MultipleJoin('Pale')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    @property
    def productoVenta(self):
        return self.get_productoVenta()

    def get_puid(self):
        """
        Identificador único en la BD para cada objeto de esta clase.
        OJO: No lleva el mismo formato que los usados hasta ahora, aunque sí
        asegura que sigue siendo único.
        """
        # Voy a hacer unas pruebas con esta versión alfa de puid. Llevará
        # nombre de la clase, dos puntos, y el identificador. Así a partir de
        # un puid puedo cargar el objeto sin tener conocimiento a priori de
        # qué es. Las 4 clases nuevas de líneas de embolsado van a funcionar
        # así. Si funciona bien, migraré todas las clases.
        return "PartidaCem:%d" % self.id

    def get_productoVenta(self):
        """
        Devuelve el producto de venta al que pertenece
        la partida o None si no tiene producción.
        """
        try:
            producto = self.pales[0].cajas[0].articulo.productoVenta
        except IndexError:  # No tiene producción todavía.
            producto = None
        return producto

    def set_productoVenta(self, productoVenta):
        """
        Hace que el producto de venta de todas las bigbags
        la partida sea el recibido.
        """
        if not isinstance(productoVenta, ProductoVenta):
            raise TypeError, "El producto debe ser un objeto de la clase Pro"\
                             "ductoVenta."
        for p in self.pales:
            for c in p.cajas:
                c.articulo.productoVenta = productoVenta
                c.articulo.sync()
                c.sync()

    productoVenta = property(get_productoVenta, set_productoVenta,
                    "Producto de venta relacionado con la partida de cemento.")

    def get_nueva_o_ultima_vacia():
        """
        Devuelve una partida de cemento nueva con el número de partida
        secuencial correcto o la última partida de cemento existente
        vacía y sin partes relacionados (por si se creó por error para que
        no siga aumentando el número de partida por delante del real).
        """
        try:
            ultima = PartidaCem.select(orderBy = "-numpartida")[0]
        except:
            res = PartidaCem()
        else:
            if not ultima.partesDeProduccion and not ultima.pales:
                res = ultima
            else:
                res = PartidaCem()
        # Y antes de devolver, asigno el código de trazabilidad.
        res.codigo = "%s%d" % (PREFIJO_PARTIDACEM, res.numpartida)
        return res

    get_nueva_o_ultima_vacia = staticmethod(get_nueva_o_ultima_vacia)

    def esta_analizada(self):
        """
        True si la partida de cemento está analizada.
        """
        # OJO: De momento, y hasta que decidan qué van a hacer con los
        # los análisis de fibra de cemento, devolveré siempre True (al igual
        # que se hace con los objetos Caja).
        return True

    def get_pales_a(self):
        """
        Devuelve los objetos palé de la partida de tipo A.
        """
        return [p for p in self.pales if not p.claseb]

    def get_pales_b(self):
        """
        Devuelve los objetos palé de la partida de tipo B.
        """
        return [p for p in self.pales if p.claseb]

cont, tiempo = print_verbose(cont, total, tiempo)

class Bala(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------------- loteID = ForeignKey('Lote')
    #--------------------------------------- # partidaID = ForeignKey('Partida')
    articulos = MultipleJoin('Articulo')
    #------------------------------- partidaCargaID = ForeignKey('PartidaCarga')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def _buscar_en_almacen_actualmente(productoVenta = None, almacen = None):
        """
        Devuelve una tupla de objetos bala en almacén (cualquiera) y en la
        fecha actual. Si productoVenta no es None, devuelve las balas
        únicamente de ese producto.
        """
        # Con los almacenes ya no hace falta andar mirando si tiene albarán
        # de salida o si se ha consumido en una partida de carga. Basta con
        # chequear la relación "almacenada".
        clauses =  [(Articulo.q.balaID != None)]
        if productoVenta:
            clauses.append(Articulo.q.productoVentaID == productoVenta.id)
        if almacen:
            clauses.append(Articulo.q.almacenID == almacen.id)
        else:
            clauses.append(Articulo.q.almacenID != None)
        articulos = Articulo.select(AND(*clauses))
        balas = [a.bala for a in articulos]
        balas = SQLtuple(balas)
        return balas

    _buscar_en_almacen_actualmente = staticmethod(_buscar_en_almacen_actualmente)

    def set_productoVenta(self, producto):
        """
        Instancia el producto del artículo relacionado con el rollo.
        """
        if not isinstance(producto, ProductoVenta):
            raise ValueError
        self.articulos[0].productoVenta = producto

    def get_productoVenta(self):
        """
        Devuelve el producto relacionado con el rollo a través del artículo.
        """
        try:
            return self.articulos[0].productoVenta
        except IndexError:
            return None

    productoVenta = property(get_productoVenta, set_productoVenta)

    def get_articulo(self):
        """
        Devuelve el artículo asociado al bala.
        """
        return self.articulos[0]

    def get_articuloID(self):
        """
        Devuelve el identificador del artículo asociado al bala o None.
        """
        return self.articulos and self.articulos[0].id or None

    articulo = property(get_articulo)
    articuloID = property(get_articuloID)

    def get_fake_partidaID(self):
        """
        Devuelve la partida de carga en el cuarto en el que
        se ha usado la bala.
        """
        # Espero conservar la compatibilidad haciendo un property con esto.
        return self.partidaCargaID

    def set_fake_partidaID(self, partidaID):
        """
        Establece la partida de carga en el cuarto en el que
        se ha usado la bala.
        """
        # Espero conservar la compatibilidad haciendo un property con esto.
        self.partidaCargaID = partidaID

    def get_fake_partida(self):
        """
        Devuelve la partida de carga en el cuaro en el que
        se ha usado la bala.
        """
        return self.partidaCarga

    def set_fake_partida(self, partida):
        """
        Establece la partida de carga en el cuarto en el que
        se ha usado la bala.
        """
        # Espero conservar la compatibilidad haciendo un property con esto.
        self.partidaCarga = partida

    partidaID = property(get_fake_partidaID, set_fake_partidaID)
    partida = property(get_fake_partida, set_fake_partida)

    def analizada(self):
        """
        Devuelve True si la bala ya ha sido analizada
        y catalogada por el laboratorio. Esto es, pertenece
        a un lote con tenacidad, elongación y rizo con
        un valor diferente de NULL, '' y ' '.
        """
        lote = self.lote
        if lote == None:
            return False
        valores_nulos = (' ', '', None)
        return (lote.tenacidad not in valores_nulos) and \
               (lote.elongacion not in valores_nulos) and \
               (lote.rizo not in valores_nulos) and \
               (lote.encogimiento not in valores_nulos)

    def en_almacen(self, almacen = None):
        """
        Si almacen es None, devuelve True si la bala está en algún almacén.
        Si no es None, devuelve True si está en el almacén indicado.
        False si se ha vendido o se ha consumido.
        """
        self.sync()
        articulo = self.articulos[0]
        articulo.sync()
        if almacen:
            res = articulo == almacen
        else:
            res = articulo.almacen != None
        #return (self.partidaCargaID == None
        #        and self.articulos[0].albaranSalidaID == None)
        return res

    def get_albaranSalida(self):
        """
        Devuelve el albarán de salida del artículo relacionado con la bala.
        """
        return self.articulos[0].albaranSalida

    def set_albaranSalida(self, albaranSalida):
        """
        Establece el albarán de salida del artículo relacionado con la bala.
        """
        self.articulos[0].albaranSalida = albaranSalida

    def get_albaranSalidaID(self):
        """
        Devuelve el ID albarán de salida del artículo relacionado con la bala o None.
        """
        return self.articulos[0].albaranSalidaID

    def set_albaranSalidaID(self, albaranSalidaID):
        """
        Establece el id de albarán de salida del artículo relacionado con la bala.
        """
        self.articulos[0].albaranSalidaID = albaranSalidaID

    albaranSalida = property(get_albaranSalida, set_albaranSalida)
    albaranSalidaID = property(get_albaranSalidaID, set_albaranSalidaID)

cont, tiempo = print_verbose(cont, total, tiempo)

class TipoDeMaterial(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    productosCompra = MultipleJoin('ProductoCompra')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class CuentaDestino(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------- proveedorID = ForeignKey('Proveedor', default = None)
    pagos = MultipleJoin('Pago')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        return ", ".join((self.nombre, self.banco, self.swif, self.iban, self.cuenta, self.nombreBanco, self.proveedor and self.proveedor.nombre or ""))

cont, tiempo = print_verbose(cont, total, tiempo)

class CuentaOrigen(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    pagos = MultipleJoin('Pago')
    vencimientosCobro = MultipleJoin('VencimientoCobro')
    clientes = MultipleJoin('Cliente')
    recibos = MultipleJoin('Recibo')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        return ", ".join((self.nombre, self.banco, self.ccc, self.observaciones))

cont, tiempo = print_verbose(cont, total, tiempo)

class TipoDeProveedor(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    proveedores = MultipleJoin("Proveedor")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        return "%s: %d proveedores en esta categoría." % (
                self.descripcion, len(self.proveedores))

    @staticmethod
    def check_defaults():
        """
        Comprueba que existen --y si no, los crea-- los tipos por defecto.
        """
        # FIXME: La creación dentro del AssertionError no funciona. Al hacerlo
        # con una base de datos limpia, peta. Dice que el ID del objeto
        # recién insertado no existe. Supongo que es en la línea de Auditoria.
        # Tal vez necesite un commit explícito antes o algo.
        # insert into tipo_de_proveedor("descripcion") values('Granza'); insert into tipo_de_proveedor("descripcion") values('Comercializados'); insert into tipo_de_proveedor("descripcion") values('Transporte'); insert into tipo_de_proveedor("descripcion") values('Repuestos'); insert into tipo_de_proveedor("descripcion") values('Suministros');  insert into tipo_de_proveedor("descripcion") values('Materiales'); insert into tipo_de_proveedor("descripcion") values('Resto');
        tipos = ("Granza", "Comercializados", "Transporte", "Repuestos",
                 "Suministros", "Materiales", "Resto")
        for t in tipos:
            try:
                assert TipoDeProveedor.selectBy(descripcion = t).count() > 0
            except AssertionError:
                tipo = TipoDeProveedor(descripcion = t)
                Auditoria.nuevo(tipo, None, __file__)

    @classmethod
    def get_por_defecto(claseproveedor):
        """
        Devuelve el tipo de cliente por defecto a usar.
        """
        try:
            tdp = claseproveedor.selectBy(descripcion = "Repuestos")[0]
        except IndexError:
            tdp = claseproveedor(descripcion = "Repuestos")
            Auditoria.nuevo(tdp, None, __file__)
        return tdp

cont, tiempo = print_verbose(cont, total, tiempo)

class Proveedor(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    pedidosCompra = MultipleJoin('PedidoCompra')
    albaranesEntrada = MultipleJoin('AlbaranEntrada')
    facturasCompra = MultipleJoin('FacturaCompra')
    pagos = MultipleJoin('Pago')
    transportesACuenta = MultipleJoin('TransporteACuenta')
    clientes = MultipleJoin('Cliente')
    cuentasDestino = MultipleJoin('CuentaDestino')
    documentos = MultipleJoin('Documento')
    productosCompra = MultipleJoin("ProductoCompra")    # Productos que tiene
                                    # asignados como proveedor por defecto.
    conceptosPresupuestoAnual = MultipleJoin("ConceptoPresupuestoAnual")
    #--------- tipoDeProveedorID = ForeignKey("TipoDeProveedor", default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_dias_de_pago(self):
        """
        Devuelve UNA TUPLA con los días de pago del cliente (vacía si no tiene).
        """
        res = []
        if self.diadepago != None:
            regexpr = re.compile("\d*")
            lista_dias = regexpr.findall(self.diadepago)
            try:
                res = tuple([int(i) for i in lista_dias if i != ''])
            except TypeError, msg:
                print "ERROR: pclases: cliente.get_dias_de_pago(): %s" % (msg)
        return res

    def get_documentoDePago(self, strict_mode = False):
        """
        Devuelve un objeto DocumentoDePago que se relaciona unívocamente con
        el texto que tiene el cliente en el documento de pago.
        None si no lo puede determinar.
        """
        return Cobro._parse_docpago(self.documentodepago, strict_mode)

    def get_tipos_de_proveedor_secundarios(self):
        """
        En función de los pedidos hechos al proveedor devuelve todos los
        tipos de material que nos ha servido.
        """
        tipos_material = []
        for p in self.get_productos():
            t = p.tipoDeMaterial
            if t not in tipos_material:
                tipos_material.append(t)
        return tipos_material

    def es_extranjero(self):
        """
        Devuelve True si el proveedor es extranjero.
        Para ello mira si el país del proveedor es diferente al
        de la empresa. Si no se encuentran datos de la empresa
        devuelve True si el país no es España.
        """
        cpf = unicode(self.paisfacturacion.strip())
        try:
            de = DatosDeLaEmpresa.select()[0]
            depf = unicode(de.paisfacturacion.strip())
            res = cpf != "" and depf.lower() != cpf.lower()
        except IndexError:
            res = (cpf != "" and cpf.lower() != unicode("españa")
                             and cpf.lower() != unicode("spain"))
        return res

    extranjero = property(es_extranjero)

    def get_texto_forma_pago(self):
        """
        Devuelve un texto que representa la forma de pago del proveedor.
        Por ejemplo:  efectivo, pagaré 90 D.F.F., transferencia banco 1423-...
        """
        formapago = ""
        if self.documentodepago != None and self.documentodepago.strip() != "" and self.documentodepago.strip() != "0":
            formapago = "%s, " % (self.documentodepago)
        if self.cuenta != None and self.cuenta.strip() != "" and "ferenc" in self.documentodepago.lower():
            formapago += "(%s) " % (self.cuenta)
        if self.vencimiento != None and self.vencimiento.strip() != "" and self.vencimiento.strip() != "0":
            formapago += "%s " % (self.vencimiento)
        if self.diadepago != None and self.diadepago.strip() != "" and self.diadepago.strip() != "-":
            formapago += "los días %s" % (self.diadepago)
        if len(formapago) > 0:
            formapago += ". "
        return formapago

    textoformapago = property(get_texto_forma_pago)

    def get_albaranes_pendientes_de_facturar(self):
        """
        Devuelve un diccionario de LDCs pendientes de facturar
        cuyas claves son sus albaranes.
        """
        res = {}
        for albaran in self.albaranesEntrada:
            for ldc in albaran.lineasDeCompra:
                if ldc.facturaCompra == None:
                    if albaran not in res:
                        res[albaran] = [ldc]
                    else:
                        res[albaran].append(ldc)
        return res

    def get_comisiones_pendientes_de_facturar(self):
        """
        Devuelve las comisiones pendientes de facturar del proveedor.
        La estructura en la BD es que un proveedor puede tener uno o
        varios clientes sobre los que actúa como "representante" en
        las facturas de compra. Cada uno de esos clientes (por lo general
        será uno y casi idéntico al registro cliente, solo que en la
        tabla de proveedores) puede tener una o varias comisiones
        generadas en albaranes de salida.
        Estas comisiones estarán facturadas sii tienen un registro
        "servicioTomado" relacionado y éste está a su vez relacionado
        con una "facturaCompra". No deberían existir registros
        "servicioTomado" relacionados con una comisión y sin facturas
        de compra. De ser así, en este método se eliminarán al detectarlos.
        """
        comisiones = []
        for cliente in self.clientes:
            for comision in cliente.comisiones:
                # Chequeo coherencia:
                for servicio in comision.serviciosTomados:
                    if servicio.facturaCompraID == None:
                        servicio.destroy()
                # Ahora miro si de verdad está facturado o no.
                if comision.serviciosTomados == []:
                    comisiones.append(comision)
        return comisiones

    def get_transportes_pendientes_de_facturar(self):
        """
        Devuelve las transportes pendientes de facturar del proveedor.
        La estructura en la BD es que un proveedor puede tener uno o
        varios clientes sobre los que actúa como "representante" en
        las facturas de compra. Cada uno de esos clientes (por lo general
        será uno y casi idéntico al registro cliente, solo que en la
        tabla de proveedores) puede tener una o varias transportes
        generadas en albaranes de salida.
        Estas transportes estarán facturadas sii tienen un registro
        "servicioTomado" relacionado y éste está a su vez relacionado
        con una "facturaCompra". No deberían existir registros
        "servicioTomado" relacionados con una comisión y sin facturas
        de compra. De ser así, en este método se eliminarán al detectarlos.
        """
        transportes = []
        for transporte in self.transportesACuenta:
            # Chequeo coherencia:
            for servicio in transporte.serviciosTomados:
                if servicio.facturaCompraID == None:
                    servicio.destroy()
            # Ahora miro si de verdad está facturado o no.
            if transporte.serviciosTomados == []:
                transportes.append(transporte)
        return transportes

    def get_productos(self):
        """
        Devuelve una lista de objetos producto compra que
        hayan sido comprados a este proveedor mediante
        pedidos, albaranes o facturas.
        Como el resultado se convierte a tupla antes de
        devolverse, este método puede llegar a resultar lento.
        USAR CON CUIDADO.
        """
        productos = ProductoCompra.select(""" id IN (
            SELECT producto_compra_id
            FROM linea_de_compra
            WHERE pedido_compra_id IN (
                    SELECT id
                    FROM pedido_compra
                    WHERE proveedor_id = %d)
               OR albaran_entrada_id IN (
                    SELECT id
                    FROM albaran_entrada
                    WHERE proveedor_id = %d)
               OR factura_compra_id IN (
                    SELECT id
                    FROM factura_compra
                    WHERE proveedor_id = %d))
               OR id IN (SELECT producto_compra_id
                    FROM linea_de_pedido_de_compra
                    WHERE pedido_compra_id IN (SELECT id
                    FROM pedido_compra
                    WHERE proveedor_id = %d))
            """ % (self.id, self.id, self.id, self.id))
        return tuple(productos)

    def get_fechas_vtos_por_defecto(self, fecha):
        """
        Devuelve una lista ordenada de fechas de vencimientos a
        partir de los vencimientos, día de pago y tomando la
        fecha recibida como base.
        En caso de que el proveedor no tenga la información necesaria
        devuelve una lista vacía.
        """
        res = []
        vtos = self.get_vencimientos()
        try:
            diacobro = int(self.diadepago)
        except (TypeError, ValueError):
            diacobro = None
        for incr in vtos:
            try:
                nfecha = fecha + incr
            except TypeError: # No se pueden sumar fechas datetime con enteros.
                nfecha = fecha + datetime.timedelta(incr)
            res.append(nfecha)
            if diacobro != None:
                while True:
                    try:
                        res[-1] = mx.DateTime.DateTimeFrom(
                                    day = diacobro,
                                    month = res[-1].month,
                                    year = res[-1].year)
                        break
                    except:
                        diacobro -= 1
                        if diacobro <= 0:
                            diacobro = 31
                try:
                    nfecha = fecha + incr
                except TypeError:
                    nfecha = fecha + datetime.timedelta(incr)
                if res[-1] < nfecha:
                    mes = res[-1].month + 1; anno = res[-1].year
                    if mes > 12:
                        mes = 1; anno += 1
                    res[-1] = mx.DateTime.DateTimeFrom(day = diacobro,
                                                       month = mes,
                                                       year = anno)
                try:
                    diasemana = res[-1].day_of_week
                except AttributeError:
                    diasemana = res[-1].weekday()
                while diasemana >= 5:
                    res[-1] += mx.DateTime.oneDay
                    try:
                        diasemana = res[-1].day_of_week
                    except AttributeError:
                        diasemana = res[-1].weekday()
        res.sort()
        return res

    def get_vencimientos(self):
        """
        Devuelve una lista con los días naturales de los vencimientos
        del cliente. P. ej.:
        - Si el cliente tiene "30", devuelve [30].
        - Si no tiene, devuelve [].
        - Si tiene "30-60", devuelve [30, 60].
        - Si tiene "90 D.F.F." (90 días a partir de fecha factura),
          devuelve [90].
        - Si tiene "30-120 D.R.F." (30 y 120 días a partir de fecha de
          recepción de factura) devuelve [30, 120].
        etc.
        En definitiva, filtra todo el texto y devuelve los números que
        encuentre en cliente.vencimientos.
        """
        res = []
        # Antes había dos campos para "lo mismo", compruebo que no haya
        # todavía proveedores con algo en "formadepago" y "vencimientos" aún
        # vacío.
        if ((self.vencimiento == None or self.vencimiento.strip() == '')
            and (self.formadepago != None and self.formadepago.strip() != '')):
            self.vencimiento = self.formadepago
        if self.vencimiento != None:
            if "contado" in self.vencimiento.lower():
                res = [0]
            else:
                regexpr = re.compile("\d*")
                lista_vtos = regexpr.findall(self.vencimiento)
                try:
                    res = [int(i) for i in lista_vtos if i != '']
                except TypeError, msg:
                    myprint("ERROR: pclases::proveedor.get_vencimientos()-> %s"%(
                        msg))
        return res

    def get_facturas(self, fechaini = None, fechafin = None):
        """
        Devuelve las facturas del proveedor entre las dos
        fechas recibidas (incluidas). Si ambas son None no
        aplicará rango de fecha en la búsqueda.
        """
        criterio = (FacturaCompra.q.proveedorID == self.id)
        if fechaini:
            criterio = AND(criterio, FacturaCompra.q.fecha >= fechaini)
        if fechafin:
            criterio = AND(criterio, FacturaCompra.q.fecha <= fechafin)
        return FacturaCompra.select(criterio)

    def calcular_comprado(self, fechaini = None, fechafin = None):
        """
        Devuelve el importe total de compras al proveedor
        entre las fechas indicadas. Si las fechas son None no
        impondrá rangos en la búsqueda. No se consideran
        pedidos ni albaranes, solo compras ya facturadas.
        """
        total = 0
        facturas = self.get_facturas(fechaini, fechafin)
        for f in facturas:
            total += f.calcular_importe_total()
        return total

    def calcular_pagado(self, fechaini = None, fechafin = None):
        """
        Devuelve el importe total de compras pagadas al proveedor
        entre las fechas indicadas. Si las fechas son None no
        impondrá rangos en la búsqueda. No se consideran
        pedidos ni albaranes, solo compras ya facturadas.
        De todas esas facturas, suma el importe de los pagos
        relacionadas con las mismas. _No tiene en cuenta_ las
        fechas de los pagos, solo las fechas de las facturas
        a las que corresponden esos pagos (ya que la consulta
        base es de facturas, lo lógico es saber cuánto de esas
        facturas está pagado, sea en las fechas que sea).
        """
        total = 0
        facturas = self.get_facturas(fechaini, fechafin)
        for f in facturas:
            for pago in f.pagos:
                total += pago.importe
        return total

    def calcular_pendiente_pago(self, fechaini = None, fechafin = None):
        """
        Devuelve el importe total pendiente de pago. Para ello
        _ignora los vencimientos_ y simplemente devuelve la diferencia
        entre el importe total facturado y el importe total de los
        cobros relacionados con esas facturas.
        """
        total = self.calcular_comprado(fechaini, fechafin)
        pagado = self.calcular_pagado(fechaini, fechafin)
        pendiente = total - pagado
        return pendiente

cont, tiempo = print_verbose(cont, total, tiempo)

class PartidaCarga(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    balas = MultipleJoin('Bala')
    partidas = MultipleJoin('Partida')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def _get_partes_partidas(self):
        """
        Devuelve una lista de partes de
        produccion relacionados con las partidas
        de la partida de carga.
        """
        pdps = []
        for p in self.partidas:
            #for r in p.rollos:
            #    pdp = r.articulo.parteDeProduccion
            #    if pdp != None and pdp not in pdps:
            #        pdps.append(pdp)
            pdps += p.get_partes_de_produccion()
        return pdps

    def get_fecha_inicio(self):
        """
        Devuelve la fecha de inicio del consumo de la partida
        de carga, que es la fecha de parte de producción más
        temprana de todas las partidas relacionadas o None
        si no las tiene.
        OJO: Este método usa fechahorainicio, que es un atributo que se
        introdujo A POSTERIORI y la fecha absoluta debería coincidir con
        parteDeProduccion.fecha.
        """
        partes = self._get_partes_partidas()
        partes.sort(lambda pdp1, pdp2:
                        (pdp1.fechahorainicio < pdp2.fechahorainicio and -1)
                        or (pdp1.fechahorainicio > pdp2.fechahorainicio and 1)
                        or 0)
        try:
            return partes[0].fechahorainicio
        except IndexError:
            return None

    def get_fecha_fin(self):
        """
        Devuelve la fecha de inicio del consumo de la partida
        de carga, que es la fecha de parte de producción más
        temprana de todas las partidas relacionadas o None
        si no las tiene.
        OJO: Este método usa fechahorafin, que es un atributo que se introdujo A POSTERIORI y la fecha absoluta debería
             coincidir con parteDeProduccion.fecha si la hora es posterior a parteDeProduccion.horainicio; e igual a
             parteDeProduccion.fecha + mx.DateTime.oneDay en caso contrario.
        """
        partes = self._get_partes_partidas()
        partes.sort(lambda pdp1, pdp2:
                            (pdp1.fechahorafin < pdp2.fechahorafin and -1)
                            or (pdp1.fechahorafin > pdp2.fechahorafin and 1)
                            or 0)
        try:
            return partes[-1].fechahorafin
        except IndexError:
            return None

    def test(self):
        """
        Comprueba que get_fecha_inicio y get_fecha_fin son coherentes.
        Devuelve True si lo son. Lanza un AssertionError si no.
        """
        fi = self.get_fecha_inicio()
        ff = self.get_fecha_fin()
        assert (fi == None and ff == None) or (fi <= ff), \
                "Fechas de inicio (%s) y fin (%s) incorrectas para la partida de carga ID %d" % (fi, ff, self.id)
        if ff != None:
            for p in self.partidas:
                if len(p.rollos) + len(p.rollosDefectuosos) > 0:
                    assert p.entra_en_cota_superior(ff, contar_partida_carga_completa = False), "Algoritmo falló. Por definición todas las partidas con al menos un rollo producido deberían entrar en el rango de fechas de su partida de carga. Partida ID %d. PartidaCarga ID %d." % (p.id, self.id)
        return True

    def get_lotes(self):
        """
        Devuelve una lista de lotes relacionados con la partida
        de carga a través de sus balas de fibra.
        """
        lotes = Lote.select(""" lote.id IN (SELECT bala.lote_id FROM bala WHERE bala.partida_carga_id = %d) """ % (self.id))
        return [l for l in lotes]

    def __crear_albaran(self, cliente):
        """
        Crea un nuevo albarán de salida "interno".
        Debe recibir el cliente "propia-empresa".
        """
        numalbaran = AlbaranSalida.get_ultimo_numero_numalbaran() + 1
        observaciones = "Albarán interno correspondiente a %d balas de "\
                        "la partida de carga %s." % (
                            len(self.balas),
                            self.codigo)
        almacen_ppal = Almacen.get_almacen_principal()
        # Cogeré la fecha de la primera partida de producción, que es lo
        # lógico, ya que lo que se va a reflejar en el albarán interno es el
        # consumo de balas en el cuarto. Si por lo que sea se intenta crear
        # el albarán interno antes de terminar de cargar las balas y sin
        # partes de producción relacionados, uso la de la partida de carga,
        # mejor que la actual.
        fecha_albaran_interno = self.get_fecha_inicio()
        if not fecha_albaran_interno:
            fecha_albaran_interno = self.fecha
        if not isinstance(numalbaran, str):
            numalbaran = str(numalbaran)
        albaran = AlbaranSalida(numalbaran = numalbaran,
                                transportista = None,
                                cliente = cliente,
                                facturable = True,  # ¡¿Por qué se crean los
                                    # albaranes internos como facturables?!
                                destino = None,
                                #fecha = self.fecha,
                                fecha = fecha_albaran_interno,
                                bloqueado = True,
                                observaciones = observaciones,
                                almacenOrigen = almacen_ppal,
                                almacenDestino = None)
        return albaran

    def __buscar_pedido_linea(self, cliente):
        """
        Devuelve el último pedido de venta "interno" a la
        línea de producción.
        Debe recibir el cliente "propia-empresa".
        Si no quedan pedidos abiertos, devuelve None.
        """
        # De entre todos los pedidos de la "propia-empresa" me quedo con el
        # último que no esté cerrado (si es que tiene).
        pedidos = [p for p in cliente.pedidosVenta if not p.cerrado
                   and p.es_de_fibra()]
        pedidos.sort(lambda p1, p2: int(p1.id - p2.id))
        if pedidos == []:
            pedido = None
        else:
            pedido = pedidos[-1]
        return pedido

    def __buscar_precio_producto_venta(self, productoVenta, pedido = None):
        """
        Devuelve el precio al que se debe valorar el albarán "interno"
        para un producto dado. Recibe también el pedido de venta para
        buscar el precio al que se valoró en el pedido. Si éste es
        None, devuelve el precio por defecto del producto.
        """
        if pedido == None:
            precio = productoVenta.precioDefecto
        else:
            try:
                precio = [ldp.precio for ldp in pedido.lineasDePedido if ldp.productoVenta == productoVenta][0]
            except IndexError:
                precio = productoVenta.precioDefecto
        return precio

    def __crear_linea_de_venta(self, pedido, productoVenta, albaran, precio):
        """
        Crea una LDV en el albarán "interno" con los datos recibidos.
        """
        ahora = mx.DateTime.localtime()
        try:
            ldv = LineaDeVenta(productoCompra = None,
                               pedidoVenta = pedido,
                               facturaVenta = None,
                               productoVenta = productoVenta,
                               albaranSalida = albaran,
                               fechahora = ahora,
                               cantidad = 0.0,
                               precio = precio,
                               descuento = 0.0)
        except Exception as e:  # Invalid
            ahora = datetime.datetime(*ahora.timetuple()[:7])
            ldv = LineaDeVenta(productoCompra = None,
                               pedidoVenta = pedido,
                               facturaVenta = None,
                               productoVenta = productoVenta,
                               albaranSalida = albaran,
                               fechahora = ahora,
                               cantidad = 0.0,
                               precio = precio,
                               descuento = 0.0)
        return ldv

    def crear_albaran_interno(self):
        """
        Crea un albarán "interno" de salida (interno = cliente es la propia
        empresa) con las balas de la partida de carga que no estén ya
        relacionadas con otro albarán.
        Devuelve el albarán creado o None si no se pudo crear.
        """
        cliente = DatosDeLaEmpresa.get_cliente()
        if cliente == None:
            myprint("pclases.py::class PartidaCarga::crear_albaran_interno ->"
                    " No se pudo encontrar propia empresa como cliente.")
            albaran = None
        else:
            balas = self.get_balas_sin_albaran_interno()
            if len(balas) > 0:
                albaran = self.__crear_albaran(cliente)
                pedido = self.__buscar_pedido_linea(cliente)
                for bala in balas:
                    productoVenta = bala.articulo.productoVenta
                    try:
                        ldv = [ldv
                               for ldv in albaran.lineasDeVenta
                               if ldv.productoVenta == productoVenta][0]
                    except IndexError:
                        precio = self.__buscar_precio_producto_venta(
                                    productoVenta, pedido)
                        ldv = self.__crear_linea_de_venta(
                                pedido,
                                productoVenta, albaran, precio)
                    ldv.cantidad += bala.pesobala
                    bala.articulo.albaranSalida = albaran
            else:
                albaran = None
        return albaran

    def get_albaranes_internos(self):
        """
        Devuelve una tupla con los albaranes internos relacionados con la
        partida de carga.
        """
        albs = []
        for b in self.balas:
            alb = b.albaranSalida
            if alb != None and alb not in albs and alb.es_interno():
                albs.append(alb)
        return tuple(albs)

    def get_balas_sin_albaran_interno(self):
        """
        Devuelve una lista de objetos bala pertenecientes a
        la partida de carga actual que no pertenezcan ya a
        un albarán interno (que no pertenezcan a un albarán
        de salida, en general; no se comprueba que el albarán
        al que pertenezcan sea interno o no, pero se supone
        precondición que si una bala de la partida de carga
        pertenece a un albarán, éste debe ser interno).
        """
        balas = []
        for bala in self.balas:
            if bala.albaranSalida == None:
                balas.append(bala)
        return balas

cont, tiempo = print_verbose(cont, total, tiempo)

class Partida(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    # balas = MultipleJoin('Bala')
    #------------------------------- partidaCargaID = ForeignKey('PartidaCarga')
    rollos = MultipleJoin('Rollo')
    pruebasGramaje = MultipleJoin('PruebaGramaje')
    pruebasResistenciaLongitudinal = MultipleJoin('PruebaLongitudinal')
    pruebasAlargamientoLongitudinal = MultipleJoin('PruebaAlargamientoLongitudinal')
    pruebasResistenciaTransversal = MultipleJoin('PruebaTransversal')
    pruebasAlargamientoTransversal = MultipleJoin('PruebaAlargamientoTransversal')
    pruebasCompresion = MultipleJoin('PruebaCompresion')
    pruebasPerforacion = MultipleJoin('PruebaPerforacion')
    pruebasEspesor = MultipleJoin('PruebaEspesor')
    pruebasPermeabilidad = MultipleJoin('PruebaPermeabilidad')
    pruebasPoros = MultipleJoin('PruebaPoros')
    pruebasPiramidal = MultipleJoin('PruebaPiramidal')
    muestras = MultipleJoin('Muestra')
    rollosDefectuosos = MultipleJoin('RolloDefectuoso')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    @property
    def productoVenta(self):
        return self.get_producto()

    def calcular_media_pruebas(self, pruebas):
        """
        Devuelve la media del campo resultados de
        la lista de pruebas recibidas.
        """
        denominador = len(pruebas)
        numerador = sum([prueba.resultado for prueba in pruebas])
        try:
            return numerador / denominador
        except ZeroDivisionError:
            return 0

    calcular_gramaje_medio = lambda self: self.calcular_media_pruebas(self.pruebasGramaje)
    calcular_resistencia_longitudinal_media = lambda self: self.calcular_media_pruebas(self.pruebasResistenciaLongitudinal)
    calcular_alargamiento_longitudinal_medio = lambda self: self.calcular_media_pruebas(self.pruebasAlargamientoLongitudinal)
    calcular_resistencia_transversal_media = lambda self: self.calcular_media_pruebas(self.pruebasResistenciaTransversal)
    calcular_alargamiento_transversal_medio = lambda self: self.calcular_media_pruebas(self.pruebasAlargamientoTransversal)
    calcular_compresion_media = lambda self: self.calcular_media_pruebas(self.pruebasCompresion)
    calcular_perforacion_media = lambda self: self.calcular_media_pruebas(self.pruebasPerforacion)
    calcular_espesor_medio = lambda self: self.calcular_media_pruebas(self.pruebasEspesor)
    calcular_permeabilidad_media = lambda self: self.calcular_media_pruebas(self.pruebasPermeabilidad)
    calcular_poros_medio = lambda self: self.calcular_media_pruebas(self.pruebasPoros)
    calcular_piramidal_media = lambda self: self.calcular_media_pruebas(self.pruebasPiramidal)

    def get_balas(self):
        """
        Devuelve las balas de la partida de carga relacionada.
        """
        return self.partidaCarga and self.partidaCarga.balas or []

    balas = property(get_balas)

    def enAlmacen(self, almacen = None):
        """
        Devuelve cierto si queda algún rollo de esa partida
        en almacen.
        NOTA: No se contabilizan los rollos defectuosos.
        Si «almacen» != None busca solo las que se encuentren en ese almacén.
        """
        #rollos_en_almacen = Articulo.select("""
        #    articulo.rollo_id IN (SELECT rollo.id
        #                          FROM rollo
        #                          WHERE rollo.partida_id = %d)
        #                          AND articulo.albaran_salida_id IS NULL """
        #    % (self.id))
        clauses = [Articulo.q.rolloID == Rollo.q.id,
                   Rollo.q.partidaID == self.id]
        if almacen:
            clauses.append(Articulo.q.almacenID == almacen.id)
        else:
            clauses.append(Articulo.q.almacenID != None)
        rollos_en_almacen = Articulo.select(AND(*clauses))
        return rollos_en_almacen.count() # > 0

    def get_kilos_totales(self):
        """
        Devuelve los kilos de geotextiles producidos en la partida,
        incluyendo el peso del núcleo y del embalaje.
        OJO: Incluye también los rollos defectuosos.
        """
        return sum([rollo.peso for rollo in self.rollos]) + sum([rollod.peso for rollod in self.rollosDefectuosos])

    def get_kilos_teorico(self, contar_defectuosos = True):
        """
        Devuelve los kilos de geotextiles producidos en la partida,
        solo incluye el geotextil en sí (sin embalaje) y en peso teórico.
        OJO: Incluye también por defecto los rollos defectuosos.
        """
        # return sum([rollo.peso_teorico for rollo in self.rollos])
        # Optimización:
        numrollos = len(self.rollos)
        if contar_defectuosos:
            numrollos += len(self.rollosDefectuosos)
        if numrollos > 0:
            try:
                return self.rollos[0].peso_teorico * numrollos
            except IndexError:  # Se cuentan los defectuosos y no hay rollos
                                # normales de donde sacar el peso teórico.
                return self.rollosDefectuosos[0].productoVenta.camposEspecificosRollo.peso_teorico
        else:
            return 0.0

    def get_kilos(self):
        """
        Devuelve los kilos de geotextiles producidos en la partida.
        No incluye el peso del embalaje, casquillo y núcleo.
        OJO: Cuenta también los rollos defectuosos.
        """
        return sum([rollo.peso_sin for rollo in self.rollos]) + sum([rollod.peso_sin for rollod in self.rollosDefectuosos])

    def get_producto(self):
        """
        Devuelve el producto producido en la partida.
        """
        #if self.rollos:
        #    return self.rollos[0].articulo.productoVenta  # todos los artículos de la partida DEBEN compartir producto de venta.
        #elif self.rollosDefectuosos:    # Devuelvo el producto del primer rollo defectuoso. A lo mejor no todos son del mismo,
        #                                # pero lo más probable es que sí...
        #    return self.rollosDefectuosos[0].articulo.productoVenta
        #else:
        #    return None
        ## A ver si podemos acelerar esto un poco.
        producto = ProductoVenta.select("""
            id IN (SELECT producto_venta_id FROM articulo
                   WHERE rollo_id IN (SELECT id FROM rollo
                                      WHERE partida_id = %d)
                    OR rollo_defectuoso_id IN (SELECT id FROM rollo_defectuoso
                                               WHERE partida_id = %d))""" % (self.id, self.id))
        productocount = producto.count()
        if productocount == 0:
            return None
        elif productocount > 1:
            myprint("pclases::Partida::get_producto -> %d productos encontrados para la partida ID %d. Devuelvo el primero de ellos." % (productocount, self.id))
            return producto[0]
        else:
            return producto[0]

    def set_producto(self, producto):
        """
        Establece el producto de todos los rollos de la
        partida al recibido.
        """
        if not isinstance(producto, ProductoVenta):
            raise TypeError, "Operación no permitida. El parámetro debe ser un ProductoVenta."
        for rollo in self.rollos:
            rollo.articulo.productoVenta = producto
        for rollod in self.rollosDefectuosos:
            rollod.articulo.productoVenta = producto

    def get_metros(self, contar_defectuosos = True):
        """
        Devuelve los metros cuadrados producidos en la partida.
        OJO: Por defecto incluye los rollos defectuosos.
        """
        producto = self.get_producto()
        if producto == None:
            return 0.0
        else:
            buenos = len(self.rollos) * producto.camposEspecificosRollo.metros_cuadrados
            malos = sum([rollod.metrosLineales * rollod.ancho for rollod in self.rollosDefectuosos])
            return buenos + malos

    def get_productos(self):
        """
        Devuelve una lista de productos (únicos) fabricados
        en la partida. Si la partida es "defectuosa" (anterior
        a la división de partidas de carga y eso) devolverá una
        lista de tamaño > 1.
        NO USAR con partidas "correctas", ya que es más lento
        que el método get_producto.
        NOTA: No tiene en cuenta los rollos defectuosos, ya que un rollo defectuoso ni siquiera se
              puede considerar como un producto estándar en sí (probablemente ni tiene el mismo
              gramaje, ni el peso ni los metros lineales del producto de la partida).
        """
        productos = ProductoVenta.select("""  producto_venta.id IN (SELECT producto_venta_id FROM articulo WHERE rollo_id IN (SELECT rollo.id FROM rollo WHERE rollo.partida_id = %d )) """ % (self.id))
        return list(productos)

    def entra_en_cota_superior(self, fecha,
                               contar_partida_carga_completa = True):
        """
        Devuelve True si todos los partes de producción relacionados con
        la partida son de fecha menor o igual a la recibida Y (si contar_...
        es True) todas las demás partidas de la partida de carga también
        entran en esa cota -útil para discernir a qué mes pertenece un consumo
        de fibra.
        Pertenecerá al mes en el que se haya terminado de consumir la carga de
        cuarto por completo-. Si una partida de la partida de carga está vacía
        (sin producción) se considera que la partida de carga no entra en la
        fecha porque no se ha fabricado nada en esa partida de geotextiles. La
        diferencia es que si la partida tuviera producción, la partida de
        carga aparecería en la fecha de esa partida de geotextiles. Si no
        tiene producción, simplemente no entra en ningún rango de fechas hasta
        que se fabrique algo o se anule.
        """
        #res = True
        #partes = []
        #for r in self.rollos + self.rollosDefectuosos:
        #    parte = r.articulo.parteDeProduccion
        #    if parte != None and r.articulo.parteDeProduccion not in partes:
        #        if parte.fecha > fecha:
        #            res = False
        #            break
        #        partes.append(parte)
        #return res
        ## Optimizando, que es gerundio:
        consulta_entran = self._connection.queryAll("""
            SELECT fecha <= '%s' AS "menor_o_igual"
            FROM parte_de_produccion
            WHERE id IN (
                SELECT parte_de_produccion_id
                FROM articulo
                WHERE rollo_id IS NOT NULL AND rollo_id IN (
                    SELECT id
                    FROM rollo
                    WHERE partida_id = %d)
                  OR rollo_defectuoso_id IS NOT NULL
                  AND rollo_defectuoso_id IN (
                    SELECT id
                    FROM rollo_defectuoso
                    WHERE partida_id = %d)
                ); """ % (fecha.strftime("%Y-%m-%d"), self.id, self.id))
        try:
            res = reduce(lambda x, y: [x[0] and y[0]], consulta_entran)
            res = res[0] == 1
        except (TypeError, IndexError):   # TypeError: reduce() of empty sequence with no initial value. IndexError no debería darse.
            res = False     # No debería producirse a no ser que la partida sólo contenga
                            # rollos (probablemente duplicados) que no tienen parte.
        if contar_partida_carga_completa:
            if self.partidaCarga != None:
                for partida in self.partidaCarga.partidas:
                    if partida != self:
                        res = res and partida.entra_en_cota_superior(fecha, contar_partida_carga_completa = False)
                            # Si no False entrará en bucle infinito.
                    if not res:
                        break
            else:
                myprint("pclases::Partida::entra_en_cota_superior -> La partida ID %d no tiene partida de carga. Ignoro parámetro 'contar_partida_carga_completa." % (self.id))
        return res

    def entra_en_cota_inferior(self, fecha, contar_partida_carga_completa = True):
        """
        Devuelve True si se considera que la partida entra en la cota
        inferior "fecha".
        Si contar_...es True lo hará también con todas las demás partidas de
        la partida de carga a la que pertenezca.
        Al consultar el consumo de una partida entre dos fechas se corre el
        riesgo de que una misma partida entre en todas las fechas de sus
        partes de producción.
        Así, si se consulta el consumo entre el día 1/1 y el 3/1 dará, por
        ejemplo 1000 kg.
        Pero al consultar por separado los consumos del 1/1 al 2/1 y del 2/1
        al 3/1 volverá a dar 1000 kg y 1000kg en cada uno de los días. Esto no
        cumpliría que la suma de los consumos entre los días
        1/1 -> 2/1 + 2/1 -> 3/1 = 1/1 -> 3/1. Así que es necesario este método
        para que haya una proyección inyectiva entre días y consumos.
        Según esta función, la partida pertenecerá como consumo al día al que
        pertenezca el último de los partes de producción de la partida (aunque
        realmente las balas sigan en el cuarto de carga y ya no están en el
        almacén -conceptualmente sería correcto considerarlo así- tengo que
        seguir el criterio de entra_en_cota_superior y por fuerza debo usar el
        último de los partes). Por otro lado, como se pueden asignar balas a
        partidas aún sin producción, visto de otra forma tampoco sería
        incorrecto considerar que las balas no salen del almacén hasta que
        consumo la última de ellas en el último de los partes de la partida.
        """
        consulta_entran = self._connection.queryAll("""
            SELECT fecha > '%s' AS "mayor"
            FROM parte_de_produccion
            WHERE id IN (
                SELECT parte_de_produccion_id
                FROM articulo
                WHERE rollo_id IS NOT NULL AND rollo_id IN (
                        SELECT id
                        FROM rollo
                        WHERE partida_id = %d)
                   OR rollo_defectuoso_id IS NOT NULL
                  AND rollo_defectuoso_id IN (
                        SELECT id
                        FROM rollo_defectuoso
                        WHERE partida_id = %d)
            ); """ % (fecha.strftime("%Y-%m-%d"), self.id, self.id))
        try:
            res = reduce(lambda x, y: [x[0] or y[0]], consulta_entran)
                # Combino con OR todos los partes de la partida para ver
                # si al menos uno de ellos (el último) está por encima de
                # la fecha base.
            res = res[0] == 1
        except (TypeError, IndexError):   # TypeError: reduce() of empty sequence with no initial value. IndexError no debería darse.
            res = False     # No debería producirse a no ser que la partida
                            # sólo contenga rollos (probablemente duplicados)
                            # que no tienen parte.
        if contar_partida_carga_completa:
            if self.partidaCarga != None:
                for partida in self.partidaCarga.partidas:
                    if partida != self:
                        res = res and partida.entra_en_cota_inferior(fecha,
                                        contar_partida_carga_completa = False)
                            # Si no False entrará en bucle infinito.
                    if not res:
                        break
            else:
                myprint("pclases::Partida::entra_en_cota_inferior -> "\
                      "La partida ID %d no tiene partida de carga. "\
                      "Ignoro parámetro 'contar_partida_carga_completa." % (
                        self.id))
        return res

    def comparar_con_marcado(self, prueba, fecha = None):
        """
        Compara el valor de la partida con el del marcado CE
        del producto para la prueba indicada.
        Devuelve None si la partida está vacía.
        En otro caso devuelve dos valores, la diferencia
        respecto al estándar y una evaluación del valor de 0 a 3
        donde 0 es el óptimo y 3 el peor valor.
        En caso de que para la prueba seleccionada no se hayan realizado
        análisis, devuelve -1 para la evaluación y la diferencia respecto
        a 0. (para un valor nulo en pruebas usa el valor numérico 0 para
        calcular la diferencia respecto al óptimo, pero no se puede tomar
        como evaluación esa diferencia, ya que en realidad no tiene pruebas;
        no es que hayan dado 0, es que aún no se han realizado o ni siquiera
        se van a hacer -como por ejemplo, porometría, que se hace 1 cada
        6 meses-).
        """
        trans = {'Gramaje': 'gramaje',
                 'Longitudinal': 'longitudinal',
                 'Transversal': 'transversal',
                 'AlargamientoLongitudinal': 'alongitudinal',
                 'AlargamientoTransversal': 'atransversal',
                 'Compresion': 'compresion',
                 'Perforacion': 'perforacion',
                 'Espesor': 'espesor',
                 'Permeabilidad': 'permeabilidad',
                 'Poros': 'poros',
                 'Piramidal': 'piramidal'
                } #"Traducción" de la prueba al nombre del campo en la partida.
        dic_pruebas = {'Gramaje': 'pruebasGramaje',
                       'Longitudinal': 'pruebasResistenciaLongitudinal',
                       'Transversal': 'pruebasResistenciaTransversal',
                       'AlargamientoLongitudinal': 'pruebasAlargamientoLongitudinal',
                       'AlargamientoTransversal': 'pruebasAlargamientoTransversal',
                       'Compresion': 'pruebasCompresion',
                       'Perforacion': 'pruebasPerforacion',
                       'Espesor': 'pruebasEspesor',
                       'Permeabilidad': 'pruebasPermeabilidad',
                       'Poros': 'pruebasPoros',
                       'Piramidal': 'pruebasPiramidal'
                      }  # "Traducción" de la prueba al nombre del campo de la lista de pruebas.
        if prueba not in trans:
            raise ValueError, '"prueba" debe tener uno de los siguientes valores: %s' % (", ".join([p for p in trans.keys()]))
        producto = self.get_producto()
        if producto != None:
            valor = getattr(self, trans[prueba])
            res = producto.camposEspecificosRollo.comparar_con_marcado(
                valor, prueba, fecha)
            if len(getattr(self, dic_pruebas[prueba])) == 0:
                res = (res[0], -1)
        else:
            res = None
        return res

    def get_fecha_fabricacion(self):
        """
        Devuelve la fecha del primer parte donde se comenzó a
        fabricar la partida. Si la partida aún no se ha fabricado
        devuelve None.
        """
        fecha = self._connection.queryOne("""
            SELECT fecha
            FROM parte_de_produccion
            WHERE id IN (SELECT parte_de_produccion_id
                         FROM articulo
                         WHERE rollo_id IN (SELECT id
                                            FROM rollo
                                            WHERE partida_id = %d)
                            OR rollo_defectuoso_id IN (SELECT id
                                                       FROM rollo_defectuoso
                                                       WHERE partida_id = %d)
                        )
            ORDER BY fecha;""" % (self.id, self.id))
        if not fecha:
            res = None
        else:
            if (not isinstance(fecha[0], type(mx.DateTime.today()))
                and hasattr(fecha[0], "strftime")):
                # Devuelvo un mx, que es lo que espera el resto del programa.
                res = mx.DateTime.DateFrom(fecha[0].strftime("%Y-%m-%d"))
            else:
                res = fecha[0]
        return res

    def get_partes_de_produccion(self):
        """
        Devuelve los partes de producción relacionados con la partida de geotextiles.
        Si hay algún rollo sin parte, lo ignora.
        """
        PDP = ParteDeProduccion
        pdpsr = PDP.select(AND(Articulo.q.parteDeProduccionID == PDP.q.id,
                              Articulo.q.rolloID == Rollo.q.id,
                              Rollo.q.partidaID == self.id), distinct = True)
        pdpsrd = PDP.select(AND(Articulo.q.parteDeProduccionID == PDP.q.id,
                                Articulo.q.rolloDefectuosoID == RolloDefectuoso.q.id,
                                RolloDefectuoso.q.partidaID == self.id), distinct = True)
        return list(pdpsr) + [pdp for pdp in pdpsrd if pdp not in pdpsr]

    def esta_vacia(self):
        """
        Devuelve True si la partida no tiene rollos ni rollos defectuosos.
        """
        rollostotales = len(self.rollos) + len(self.rollosDefectuosos)
        return rollostotales == 0

    def esta_analizada(self):
        """
        Devuelve True si se le ha hecho al menos una prueba de laboratorio a
        la partida.
        """
        valores_nulos = (None, "", " ")
        res = (self.gramaje not in valores_nulos or
               self.longitudinal not in valores_nulos or
               self.alongitudinal not in valores_nulos or
               self.transversal not in valores_nulos or
               self.atransversal not in valores_nulos or
               self.compresion not in valores_nulos or
               self.perforacion not in valores_nulos or
               self.espesor not in valores_nulos or
               self.permeabilidad not in valores_nulos or
               self.poros not in valores_nulos or
               self.piramidal not in valores_nulos)
        return res

    def esta_pendiente(self):
        """
        Devuelve True si la partida está pendiente de analizar en laboratorio.
        OJO: esta_pendiente y esta_analizada son conjuntos DISJUNTOS pero
        NO COMPLEMENTARIOS.
        Se tienen en cuenta las pruebas fundamentales que han de hacerse a la
        partida completa en función del producto. A saber:
            - NT 155, NT 235 y NT 305: Punzonado piramidal.
            - Resto: Compresión (CBR), Res. long., Res. trans., Perforación y
                     Permeabilidad.
        """
        if not self.esta_vacia():
            producto = self.get_producto()
            if not producto:    # Si no producto, no puede tener muestras y
                res = False     # no se puede analizar, no puede estar pdte.
            else:
                # Lo mínimo que deben tener analizado son las pruebas:
                completamente_analizada = (self.pruebasCompresion
                               and self.pruebasResistenciaLongitudinal
                               and self.pruebasPerforacion
                               and self.pruebasPermeabilidad
                               and self.pruebasResistenciaTransversal)
                if ("NT" in producto.descripcion
                    and ("155" in producto.descripcion
                         or "235" in producto.descripcion
                         or "305" in producto.descripcion)
                   ):   # Aparte, para estos 3 que llevan certificación ASQUAL
                    completamente_analizada = (completamente_analizada
                                               and self.pruebasPiramidal)
                res = not completamente_analizada
        else:
            res = False
        return res

cont, tiempo = print_verbose(cont, total, tiempo)

class Muestra(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------------- loteID = ForeignKey('Lote')
    #----------------------------------------- partidaID = ForeignKey('Partida')
    #------------------------- loteCemID = ForeignKey('LoteCem', default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class Rollo(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- partidaID = ForeignKey('Partida')
    articulos = MultipleJoin('Articulo')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_claseB(self):
        """
        Devuelve si el rollo es de clase B.
        """
        return self.rollob

    def set_claseB(self, valor):
        """
        Pone el campo rollob a True o False.
        """
        self.rollob = valor

    claseB = property(get_claseB, set_claseB, 'Campo equivalente a los "claseB" de balas y bigbags.')

    def get_analizado(self):
        """
        CWT: Devuelve True siempre, ya que en el almacén
        hay rollos que no se han analizado ni se analizarán nunca.
        """
        return True
        #"""
        #Devuelve True si la partida a la que pertenece
        #el rollo ya ha sido analizado.
        #Se considera analizado si se le han hecho las
        #pruebas de gramaje, las dos de longitudinal,
        #las dos de transversal, la de compresión, perforación
        #y espesor.
        #"""
        #res = False
        #p = self.partida
        #if p != None:
        #    res = p.gramaje != 0.0 and \
        #          p.longitudinal != 0.0 and \
        #          p.alongitudinal != 0.0 and \
        #          p.transversal != 0.0 and \
        #          p.atransversal != 0.0 and \
        #          p.compresion != 0.0 and \
        #          p.perforacion != 0.0 and \
        #          p.espesor != 0.0
        #return res

    def get_articulo(self):
        """
        Devuelve el artículo asociado al rollo.
        """
        return self.articulos[0]

    def get_articuloID(self):
        """
        Devuelve el identificador del artículo asociado al rollo o None.
        """
        return self.articulos and self.articulos[0].id or None

    articulo = property(get_articulo)
    articuloID = property(get_articuloID)

    def set_parteDeProduccion(self, pdp):
        if isinstance(pdp, int):
            self.articulo.parteDeProduccionID = pdp
        elif isinstance(pdp, ParteDeProduccion):
            self.articulo.parteDeProduccion = pdp
        else:
            raise TypeError
        self.articulo.syncUpdate()

    parteDeProduccion = property(lambda self: self.articulo.parteDeProduccion,
                                 set_parteDeProduccion)
    parteDeProduccionID = property(
            lambda self: self.articulo.parteDeProduccionID,
            set_parteDeProduccion)

    def cambiar_numrollo(self, numrollo):
        """
        Cambia el número de rollo y el código de acuerdo al nuevo
        número de rollo recibido.
        numrollo debe ser un entero.
        Devuelve el número de rollo que tenga finalmente. Si no es
        el mismo que recibió, significará que no ha podido cambiarlo,
        probablemente porque ya exista otro rollo con ese número.
        """
        try:
            self.numrollo = numrollo
            self.codigo = "%s%d" % (PREFIJO_ROLLO, numrollo)
        # except psycopg.ProgrammingError:    # Es la excepción que se corresponde con ERROR:  llave
                                            # duplicada viola restricción unique "tal"
        finally:
            return self.numrollo

    def get_albaranSalida(self):
        """
        Devuelve el albarán de salida del artículo relacionado con el rollo.
        """
        return self.articulos[0].albaranSalida

    def set_albaranSalida(self, albaranSalida):
        """
        Establece el albarán de salida del artículo relacionado con el rollo.
        """
        self.articulos[0].albaranSalida = albaranSalida

    def get_albaranSalidaID(self):
        """
        Devuelve el ID albarán de salida del artículo relacionado con el rollo o None.
        """
        return self.articulos[0].albaranSalidaID

    def set_albaranSalidaID(self, albaranSalidaID):
        """
        Establece el id de albarán de salida del artículo relacionado con el rollo.
        """
        self.articulos[0].albaranSalidaID = albaranSalidaID

    albaranSalida = property(get_albaranSalida, set_albaranSalida)
    albaranSalidaID = property(get_albaranSalidaID, set_albaranSalidaID)

    def set_productoVenta(self, producto):
        """
        Instancia el producto del artículo relacionado con el rollo.
        """
        if not isinstance(producto, ProductoVenta):
            raise ValueError
        self.articulos[0].productoVenta = producto

    def get_productoVenta(self):
        """
        Devuelve el producto relacionado con el rollo a través del artículo.
        """
        try:
            return self.articulos[0].productoVenta
        except IndexError:
            return None

    productoVenta = property(get_productoVenta, set_productoVenta)

    def get_peso_teorico(self):
        """
        Devuelve el peso teórico del rollo (ancho * largo * densidad) en
        kilogramos.
        """
        return self.articulo.productoVenta.camposEspecificosRollo.peso_teorico

    def get_peso_sin(self):
        """
        Devuelve el peso *real* del rollo en kg, pero descontando el embalaje.
        """
        return (self.peso
            - self.articulo.productoVenta.camposEspecificosRollo.pesoEmbalaje)

    peso_teorico = property(get_peso_teorico)
    peso_sin = property(get_peso_sin)

    def get_fecha_fabricacion(self):
        """
        Devuelve la fecha de fabricación del rollo, que será:
        Si tiene parte de producción, la del parte de producción.
        Si no tiene, la del rollo en sí (fecha de alta en el sistema).
        NOTA: Devuelve una fecha _absoluta_, sin hora.
        """
        if self.articulo and self.articulo.parteDeProduccionID:
            fecha = self.articulo.parteDeProduccion.fecha
        else:
            fecha = utils.abs_mxfecha(self.fechahora)
        return fecha

    def get_info(self):
        """
        Devuelve código de rollo y descripción del producto.
        """
        cad = "Rollo %s (%s)" % (self.codigo,
                self.productoVenta and self.productoVenta.descripcion or "")
        return cad

    def calcular_densidad(self):
        """
        Devuelve la densidad del rollo en gramos por metro cuadrado en
        función del producto al que pertence.
        NO modifica la densidad actual del rollo guardada en el atributo
        «densidad» y que se calculó a la hora de darlo de alta en planta.
        """
        A = self.articulo.productoVenta.camposEspecificosRollo.metros_cuadrados
        pesosin = self.peso_sin * 1000  # Viene en kilos
        try:
            densidad = pesosin / A
        except ZeroDivisionError:
            densidad = 0
        return densidad

cont, tiempo = print_verbose(cont, total, tiempo)

class RolloDefectuoso(SQLObject, PRPCTOO):
    """
    Rollo con algún defecto que hace que no se pueda contabilizar
    como existencias del supuesto producto que se intentó fabricar
    (menos metros lineales, peso insuficiente, etc...).
    Sólo cuenta a efectos de producción (descuento de materiales,
    kilos fabricados en un parte...) pero no se tienen en cuenta
    en el almacén, por lo que no influye en el cálculo de existencias
    histórico y demás.
    Supuestamente tampoco se pueden vender, aunque como tienen un
    objeto Articulo relacionado, en un futuro se podría hacer.
    """
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- partidaID = ForeignKey('Partida')
    articulos = MultipleJoin('Articulo')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_articulo(self):
        """
        Devuelve el artículo asociado al rollo.
        """
        return self.articulos[0]

    def get_articuloID(self):
        """
        Devuelve el identificador del artículo asociado al rollo o None.
        """
        return self.articulos and self.articulos[0].id or None

    articulo = property(get_articulo)
    articuloID = property(get_articuloID)

    def cambiar_numrollo(self, numrollo):
        """
        Cambia el número de rollo y el código de acuerdo al nuevo
        número de rollo recibido.
        numrollo debe ser un entero.
        Devuelve el número de rollo que tenga finalmente. Si no es
        el mismo que recibió, significará que no ha podido cambiarlo,
        probablemente porque ya exista otro rollo con ese número.
        """
        try:
            self.numrollo = numrollo
            self.codigo = "X%d" % (numrollo)
        # except psycopg.ProgrammingError:
            # Es la excepción que se corresponde con ERROR:  llave
            # duplicada viola restricción unique "tal"
        finally:
            return self.numrollo

    def get_albaranSalida(self):
        """
        Devuelve el albarán de salida del artículo relacionado con el rollo.
        """
        return self.articulos[0].albaranSalida

    def set_albaranSalida(self, albaranSalida):
        """
        Establece el albarán de salida del artículo relacionado con el rollo.
        """
        self.articulos[0].albaranSalida = albaranSalida

    def get_albaranSalidaID(self):
        """
        Devuelve el ID albarán de salida del artículo relacionado con el rollo
        o None.
        """
        return self.articulos[0].albaranSalidaID

    def set_albaranSalidaID(self, albaranSalidaID):
        """
        Establece el id de albarán de salida del artículo relacionado con el
        rollo defectuoso.
        """
        self.articulos[0].albaranSalidaID = albaranSalidaID

    albaranSalida = property(get_albaranSalida, set_albaranSalida)
    albaranSalidaID = property(get_albaranSalidaID, set_albaranSalidaID)

    def set_productoVenta(self, producto):
        """
        Instancia el producto del artículo relacionado con el rollo.
        """
        if not isinstance(producto, ProductoVenta):
            raise ValueError
        self.articulos[0].productoVenta = producto

    def get_productoVenta(self):
        """
        Devuelve el producto relacionado con el rollo a través del artículo.
        """
        return self.articulos[0].productoVenta

    productoVenta = property(get_productoVenta, set_productoVenta)

    def get_peso_teorico(self):
        """
        Devuelve el peso teórico del rollo (ancho * largo * densidad)
        en kilogramos.
        Lo más probable es que NO coincida con el del producto que se supone
        que sería.
        """
        return (self.densidad * self.ancho * self.metrosLineales) / 1000.0

    def get_peso_sin(self):
        """
        Devuelve el peso *real* del rollo en kg, pero descontando el embalaje.
        """
        return self.peso - self.pesoEmbalaje

    peso_teorico = property(get_peso_teorico)
    peso_sin = property(get_peso_sin)

    def get_fecha_fabricacion(self):
        """
        Devuelve la fecha de fabricación del rollo, que será:
        Si tiene parte de producción, la del parte de producción.
        Si no tiene, la del rollo en sí (fecha de alta en el sistema).
        NOTA: Devuelve una fecha _absoluta_, sin hora.
        """
        if self.articulo and self.articulo.parteDeProduccionID:
            fecha = self.articulo.parteDeProduccion.fecha
        else:
            fecha = utils.abs_mxfecha(self.fechahora)
        return fecha

    def get_info(self):
        """
        Devuelve código de rollo y descripción del producto.
        """
        cad = "Rollo defectuoso %s (%s)" % (self.codigo,
                self.productoVenta and self.productoVenta.descripcion or "")
        return cad

cont, tiempo = print_verbose(cont, total, tiempo)

class BalaCable(SQLObject, PRPCTOO):
    """
    Balas de cable de fibra o fibra para reciblar.
    No cuentan como existencias de ninguna fibra. En todo caso
    contarán como existencias de un hipotético producto "Cable
    de fibra natural" (o negra o lo que sea). Llevan numeración
    diferente respecto a las balas normales, comenzando su código
    por "Z". Llevan mezcla de distintos cortes y títulos. Se
    embalan y tratan como artículos independientes porque cada
    bala tiene un peso que hay que controlar, además de ser
    de color o natural. Esas balas se envían en albaranes de
    salida a un proveedor y se reciben de nuevo como granza
    reciclada. El peso de los embalajes y una pequeña merma
    se perderá en el proceso de reciclado.
    Estas balas no consumen materia prima. Se crean a partir
    de las mermas y pérdidas de fibra en una prensa. Tampoco
    es necesario agruparlas por lote.
    """
    class sqlmeta:
        fromDatabase = True
    articulos = MultipleJoin('Articulo')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_articulo(self):
        """
        Devuelve el artículo asociado al rollo.
        """
        return self.articulos[0]

    def get_articuloID(self):
        """
        Devuelve el identificador del artículo asociado al rollo o None.
        """
        return self.articulos and self.articulos[0].id or None

    articulo = property(get_articulo)
    articuloID = property(get_articuloID)

    def cambiar_numbala(self, numbala):
        """
        Cambia el número de bala y el código de acuerdo al nuevo
        número de bala recibido.
        numbala debe ser un entero.
        Devuelve el número de bala que tenga finalmente. Si no es
        el mismo que recibió, significará que no ha podido cambiarlo,
        probablemente porque ya exista otra bala de cable con ese número.
        """
        try:
            self.numbala = numbala
            self.codigo = "Z%d" % (self.numbala)
        finally:
            return self.numbala

    def get_albaranSalida(self):
        """
        Devuelve el albarán de salida del artículo relacionado con la bala.
        """
        return self.articulos[0].albaranSalida

    def set_albaranSalida(self, albaranSalida):
        """
        Establece el albarán de salida del artículo relacionado con la bala.
        """
        self.articulos[0].albaranSalida = albaranSalida

    def get_albaranSalidaID(self):
        """
        Devuelve el ID albarán de salida del artículo relacionado con la bala o None.
        """
        return self.articulos[0].albaranSalidaID

    def set_albaranSalidaID(self, albaranSalidaID):
        """
        Establece el id de albarán de salida del artículo relacionado con la bala.
        """
        self.articulos[0].albaranSalidaID = albaranSalidaID

    albaranSalida = property(get_albaranSalida, set_albaranSalida)
    albaranSalidaID = property(get_albaranSalidaID, set_albaranSalidaID)

    def set_productoVenta(self, producto):
        """
        Instancia el producto del artículo relacionado con la bala.
        """
        if not isinstance(producto, ProductoVenta):
            raise ValueError
        self.articulos[0].productoVenta = producto

    def get_productoVenta(self):
        """
        Devuelve el producto relacionado con la bala a través del artículo.
        """
        return self.articulos[0].productoVenta

    productoVenta = property(get_productoVenta, set_productoVenta)

    def get_peso_sin(self):
        """
        Devuelve el peso *real* de la bala de cable en kg, pero descontando
        el embalaje. El peso guardado en pclases.BalaCable es el bruto de
        báscula, el real.
        """
        return self.peso - self.pesoEmbalaje

    peso_sin = property(get_peso_sin)

    def get_fecha_fabricacion(self):
        """
        Devuelve la fecha de fabricación de la bala, que será:
        Si tiene parte de producción, la del parte de producción.
        Si no tiene, la del rollo en sí (fecha de alta en el sistema).
        NOTA: Devuelve una fecha _absoluta_, sin hora.
        """
        if self.articulo and self.articulo.parteDeProduccionID:
            fecha = self.articulo.parteDeProduccion.fecha
        else:
            fecha = utils.abs_mxfecha(self.fechahora)
        return fecha

    def get_info(self):
        """
        Devuelve código de bala de cable y descripción del producto.
        """
        cad = "Bala de cable para reciclar %s (%s)" % (self.codigo, self.productoVenta and self.productoVenta.descripcion or "")
        return cad

    def calcular_acumulado_peso_sin():
        """
        Devuelve el total del peso de todas las balas de cable menos
        el embalaje.
        """
        peso = BalaCable.select().sum("peso")
        if peso is None:
            peso = 0.0
        emba = BalaCable.select().sum("peso_embalaje")
        if emba is None:
            emba = 0.0
        res = peso - emba
        return res
    calcular_acumulado_peso_sin = staticmethod(calcular_acumulado_peso_sin)

    def calcular_acumulado_mes_peso_sin(mes, anno):
        """
        «mes» es un entero que corresponde al mes natural [1..12] del
        año «anno».
        Devuelve el peso de todas las balas recicladas ese mes sin el
        embalaje.
        """
        primero_mes = mx.DateTime.DateTimeFrom(day = 1,
                                               month = mes,
                                               year = anno)
        primero_mes_sig = mx.DateTime.DateTimeFrom(day = -1,
                                                   month = mes,
                                                   year = anno)
        primero_mes_sig += mx.DateTime.oneDay
        balas = BalaCable.select(AND(BalaCable.q.fechahora >= primero_mes,
                                     BalaCable.q.fechahora < primero_mes_sig))
        peso = balas.sum("peso")
        if peso is None:
            peso = 0
        emba = balas.sum("peso_embalaje")
        if emba is None:
            emba = 0
        res = peso - emba
        return res

    calcular_acumulado_mes_peso_sin = \
        staticmethod(calcular_acumulado_mes_peso_sin)

cont, tiempo = print_verbose(cont, total, tiempo)

class RolloC(SQLObject, PRPCTOO):
    """
    Rollos de geotextiles "sin orden ni concierto".
    No cuentan como existencias de ningún producto concreto. Son rollos de
    anchos, metros lineales y grosores diversos. Sólo se tiene en cuenta el
    peso. Únicamente cuentan como exitencias de un producto llamado
    "Geotextiles C" o algo parecido que tenga True en el campo «c» de
    su camposEspecificosRollo.
    Llevan numeración diferente y su código comienza por «Y».
    No se agrupan por lote, pero al darlos de alta sí que consumen, al menos,
    un núcleo de cartón. Los consumos son configurables como si de cualquier
    otro geotextil se tratara.
    """
    class sqlmeta:
        fromDatabase = True
    articulos = MultipleJoin('Articulo')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_articulo(self):
        """
        Devuelve el artículo asociado al rollo.
        """
        return self.articulos[0]

    def get_articuloID(self):
        """
        Devuelve el identificador del artículo asociado al rollo o None.
        """
        return self.articulos and self.articulos[0].id or None

    articulo = property(get_articulo)
    articuloID = property(get_articuloID)

    def cambiar_numrollo(self, numrollo):
        """
        Cambia el número de rollo y el código de acuerdo al nuevo
        número de rollo recibido.
        numrollo debe ser un entero.
        Devuelve el número de rollo que tenga finalmente. Si no es
        el mismo que recibió, significará que no ha podido cambiarlo,
        probablemente porque ya exista otro rollo C con ese número.
        """
        try:
            self.numrollo = numrollo
            self.codigo = "Y%d" % (self.numrollo)
        finally:
            return self.numrollo

    def get_albaranSalida(self):
        """
        Devuelve el albarán de salida del artículo relacionado con el rollo.
        """
        return self.articulos[0].albaranSalida

    def set_albaranSalida(self, albaranSalida):
        """
        Establece el albarán de salida del artículo relacionado con el rollo.
        """
        self.articulos[0].albaranSalida = albaranSalida

    def get_albaranSalidaID(self):
        """
        Devuelve el ID albarán de salida del artículo relacionado con el
        rollo o None.
        """
        return self.articulos[0].albaranSalidaID

    def set_albaranSalidaID(self, albaranSalidaID):
        """
        Establece el id de albarán de salida del artículo relacionado con
        el rollo.
        """
        self.articulos[0].albaranSalidaID = albaranSalidaID

    albaranSalida = property(get_albaranSalida, set_albaranSalida)
    albaranSalidaID = property(get_albaranSalidaID, set_albaranSalidaID)

    def set_productoVenta(self, producto):
        """
        Instancia el producto del artículo relacionado con el rollo.
        """
        if not isinstance(producto, ProductoVenta):
            raise ValueError
        self.articulos[0].productoVenta = producto

    def get_productoVenta(self):
        """
        Devuelve el producto relacionado con el rollo a través del artículo.
        """
        return self.articulos[0].productoVenta

    productoVenta = property(get_productoVenta, set_productoVenta)

    def get_peso_sin(self):
        """
        Devuelve el peso *real* del rollo en kg, pero descontando el embalaje.
        """
        return self.peso - self.pesoEmbalaje

    peso_sin = property(get_peso_sin)

    def get_fecha_fabricacion(self):
        """
        Devuelve la fecha de fabricación de la bala de cable que será:
        Si tiene parte de producción, la del parte de producción.
        Si no tiene, la del rollo en sí (fecha de alta en el sistema).
        NOTA: Devuelve una fecha _absoluta_, sin hora.
        """
        if self.articulo and self.articulo.parteDeProduccionID:
            fecha = self.articulo.parteDeProduccion.fecha
        else:
            fecha = utils.abs_mxfecha(self.fechahora)
        return fecha

    def get_info(self):
        """
        Devuelve código del rollo C y descripción del producto.
        """
        cad = "Rollo C %s (%s)" % (self.codigo,
                self.productoVenta and self.productoVenta.descripcion or "")
        return cad

    def calcular_acumulado_peso_sin():
        """
        Devuelve el total del peso de todas las balas de cable menos
        el embalaje.
        """
        peso = RolloC.select().sum("peso")
        emba = RolloC.select().sum("peso_embalaje")
        if peso is None:
            peso = 0.0
        if emba is None:
            emba = 0.0
        res = peso - emba
        return res

    calcular_acumulado_peso_sin = staticmethod(calcular_acumulado_peso_sin)

    def calcular_acumulado_mes_peso_sin(mes, anno):
        """
        «mes» es un entero que corresponde al mes natural [1..12] del
        año «anno».
        Devuelve el peso de todas las balas recicladas ese mes sin el
        embalaje.
        """
        primero_mes = mx.DateTime.DateTimeFrom(day = 1,
                                               month = mes,
                                               year = anno)
        primero_mes_sig = mx.DateTime.DateTimeFrom(day = -1,
                                                   month = mes,
                                                   year = anno)
        primero_mes_sig += mx.DateTime.oneDay
        rollosc = RolloC.select(AND(RolloC.q.fechahora >= primero_mes,
                                    RolloC.q.fechahora < primero_mes_sig))
        peso = rollosc.sum("peso")
        if peso is None:
            peso = 0.0
        emba = rollosc.sum("peso_embalaje")
        if emba is None:
            emba = 0.0
        res = peso - emba
        return res

    calcular_acumulado_mes_peso_sin = \
        staticmethod(calcular_acumulado_mes_peso_sin)


cont, tiempo = print_verbose(cont, total, tiempo)

class LineaDePedido(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------- productoVentaID = ForeignKey('ProductoVenta')
    #--------------------------------- pedidoVentaID = ForeignKey('PedidoVenta')
    #----------- productoCompraID = ForeignKey('ProductoCompra', default = None)
    #----------------- presupuestoID = ForeignKey('Presupuesto', default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def calcular_precio_unitario_coherente(self, precision = 3):
        """
        Devuelve un precio unitario como cadena con los decimales suficientes
        (hasta un máximo de 5 y comenzando por «precision») para que al
        multiplicarlo por la cantidad dé el subtotal con la precisión recibida
        (por defecto, 3 -por compatibilidad hacia atrás-).
        """
        totlinea = self.get_subtotal()
        cantidad = self.cantidad
        precio = utils.float2str_autoprecision(self.precio, totlinea, cantidad, precision)
        return precio

    def get_subtotal(self, iva = False, descuento = True):
        """
        Devuelve el subtotal de esta línea de pedido.
        """
        subtotal = self.cantidad * self.precio
        if descuento:
            subtotal *= (1.0 - self.descuento)
        if iva:
            if self.pedidoVenta:
                subtotal *= (1 + self.pedidoVenta.iva)
            else:
                raise ValueError, "pclases::LineaDePedido::calcular_subtotal -> La LDP ID %s no tiene pedido del que obtener el IVA."
        return subtotal

    calcular_subtotal = get_subtotal # Por compatibilidad con LineaDeVenta.

    def get_albaraneada(self):
        """
        Devuelve True si la cantidad de la LDP se ha
        servido por completo en LDVs del pedido con
        albaranes de salida. Si se ha servido más de
        lo pedido, también devuelve True.
        """
        servida = self.get_cantidad_servida()
        pedida = self.get_cantidad_pedida()
        return servida >= pedida

    def get_cantidad_pedida(self):
        """
        Devuelve la cantidad pedida _del producto_ de la
        LDP en el pedido. OJO: Y al mismo precio -y descuento-. Dos productos
        pedidos a precios distintos, son dos líneas independientes.
        """
        pedida = 0
        for ldp in self.pedidoVenta.lineasDePedido:
            if (ldp.productoVentaID == self.productoVentaID
                and ldp.productoCompraID == self.productoCompraID
                and ldp.precio == self.precio
                and ldp.descuento == self.descuento):
                pedida += ldp.cantidad
        return pedida

    def get_cantidad_servida(self):
        """
        Devuelve la cantidad servida en LDVs del producto
        de la LDP.
        Postcondición: las LDVs están relacionadas con el
        pedido y tienen albarán de salida.OJO: Y al mismo precio -y
        descuento-.
        Dos productos pedidos a precios distintos, son dos líneas
        independientes.
        """
        ldvs = self.get_lineas_de_venta(
            productoVentaID = self.productoVentaID,
            productoCompraID = self.productoCompraID,
            precio = self.precio,
            descuento = self.descuento,
            como_lista = False)
        #servida = 0
        #for ldv in ldvs:
            #if (ldv.productoVentaID == self.productoVentaID
            #    and ldv.productoCompraID == self.productoCompraID
            #    and ldv.precio == self.precio
            #    and ldv.descuento == self.descuento):
            #    servida += ldv.cantidad
        #    servida += ldv.cantidad
        servida = sum([ldv.cantidad for ldv in ldvs])
        return servida

    def get_cantidad_pendiente(self):
        """
        Devuelve la cantidad pendiente de servir contando todos los posibles
        albaranes del pedido.
        """
        pedida = self.get_cantidad_pedida()
        servida = self.get_cantidad_servida()
        return pedida - servida

    def get_lineas_de_venta(self,
                            productoVentaID = -1,
                            productoCompraID = -1,
                            precio = None,
                            descuento = None,
                            como_lista = True):
        """
        Devuelve las líneas de venta que comparten productoVenta
        con el objeto línea de pedido.
        """
        # return [ldv for ldv in self.pedidoVenta.lineasDeVenta if
        #         ldv.productoVentaID == self.productoVentaID]
        res = []
        if DEBUG:
            res2 = []
        if self.pedidoVentaID != None:
            #res2 = [ldv for ldv in self.pedidoVenta.lineasDeVenta
            #       if ldv.productoVentaID == self.productoVentaID
            #            and ldv.productoCompraID == self.productoCompraID]
            if productoVentaID == -1:
                productoVentaID = self.productoVentaID
            if productoCompraID == -1:
                productoCompraID = self.productoCompraID
            LDV = LineaDeVenta
            criterio = [LDV.q.pedidoVentaID == self.pedidoVentaID,
                        LDV.q.productoVentaID == productoVentaID,
                        LDV.q.productoCompraID == productoCompraID]
            if precio != None:
                criterio.append(LDV.q.precio == precio)
            if descuento != None:
                criterio.append(LDV.q.descuento == descuento)
            ldvs = LDV.select(AND(*criterio))
            if como_lista:
                res = [ldv for ldv in ldvs]
            else:
                res = ldvs
        if DEBUG:
            _res = [i for i in res]
            _res.sort()
            res2.sort()
            myprint(res2 == _res)
        return res

    def get_albaranes_salida(self):
        """
        Devuelve los albaranes de salida relacionados con la línea
        de pedido atendiendo al producto de venta.
        OJO: Si hay varias LDP del mismo producto, NO DISTINGUE qué
        LDVs exactamente se corresponde con cada una de ellas.
        """
        # return [ldv.albaranSalida for ldv in self.pedidoVenta.lineasDeVenta if ldv.productoVentaID == self.productoVentaID]
        return [ldv.albaranSalida for ldv in self.pedidoVenta.lineasDeVenta
                if ldv.productoVentaID == self.productoVentaID
                    and ldv.productoCompraID == self.productoCompraID]

    def get_cantidad_servida_en_esta_LDP(self):
        """
        Devuelve la cantidad servida en la LDP.
        ASSERT: Nunca será superior a la cantidad solicitada en la LDP.
        ASSERT: La suma de get_cantidad_servida_en_esta_LDP para todas las
                LDP del pedido será igual a la suma de todas las
                LDV.cantidad = LDP.get_cantidad_servida.
        Hace una estimación para calcular la cantidad servida de la LDP
        en el caso en que haya varias LDP del mismo producto y varias
        LDV del mismo producto. Para ello:
          * Si tienen fecha de entrega, las LDP con fecha de entrega menores
            se supone que han sido las primeras en ser servidas. Lo que exceda
            será lo pendiente de servir.
          * Si no tienen fecha de entrega, se ordenan por ID y se comienza a
            repartir la cantidad servida por orden de ID entre las LDP. Lo que
            exceda debe coincidir con lo pendiente de servir.
        """
        cantidad_a_repartir = self.get_cantidad_servida()
        if cantidad_a_repartir == 0:
            res = 0
        else:
            # ldps = [ldp for ldp in self.pedidoVenta.lineasDePedido if ldp.productoVentaID == self.productoVentaID and ldp.precio == self.precio]
            ldps = [ldp for ldp in self.pedidoVenta.lineasDePedido
                    if ldp.productoVentaID == self.productoVentaID
                        and ldp.precio == self.precio
                        and ldp.descuento == self.descuento
                        and ldp.productoCompraID == self.productoCompraID]
            ldps.sort(utils.orden_por_fecha_entrega_o_id)
            for ldp in ldps:
                if cantidad_a_repartir <= 0:
                    res = 0       # Si no queda nada que repartir, la LDP se
                    # va a quedar a 0, sea esta o alguna de las siguientes.
                    break
                if ldp == self:    # Soy yo. Me toca.
                    if ldp.cantidad > cantidad_a_repartir:
                        res = cantidad_a_repartir  # Queda menos por repartir
                        # que lo que se pidió en "mí". Devuelvo lo que queda.
                        break
                    else:
                        res = ldp.cantidad  # De "lo mío" se ha repartido todo.
                        # (Lo que sobre me da igual, no voy a terminar el
                        # bucle. Estrategia "cada perrito que se lama su
                        # pijito", que se llama.)
                        break
                else:
                    cantidad_a_repartir -= ldp.cantidad
        return res

    albaranesSalida = property(get_albaranes_salida)
    albaraneada = property(get_albaraneada)
    cantidadServida = property(get_cantidad_servida)
    cantidadPedida = property(get_cantidad_pedida)
    cantidadServidaPropia = property(get_cantidad_servida_en_esta_LDP)

    def get_producto(self):
        """
        Devuelve el objeto producto relacionado con la línea de venta, sea
        del tipo que sea (productoVenta o productoCompra). None si no hay
        ningún producto relacionado.
        """
        res = None
        if self.productoVenta != None:
            res = self.productoVenta
        elif self.productoCompra != None:
            res = self.productoCompra
        return res

    def set_producto(self, producto):
        """
        Comprueba qué tipo de producto es el del parámetro "producto"
        recibido e instancia el atributo adecuado poniendo a
        None el del tipo de producto que no corresponda.
        Si la clase del objeto no es ninguna de las soportadas por
        la línea de venta, lanzará una excepción TypeError.
        """
        if isinstance(producto, ProductoVenta):
            self.productoVenta = producto
            self.productoCompra = None
        elif isinstance(producto, ProductoCompra):
            self.productoVenta = None
            self.productoCompra = producto
        else:
            raise TypeError

    producto = property(get_producto, set_producto, "Objeto producto de venta o de compra relacionado con la línea de compra.")

    def get_info(self):
        """
        Devuelve una cadena con la cantidad, producto, precio, descuento y
        subtotal de la línea (s/IVA).
        """
        precio_con_descuento = self.calcular_precio_unitario_coherente()
        if self.descuento:
            precio_con_descuento += " (%s%% dto. incl.)" % (
                utils.float2str(self.descuento * 100))
        info_entrega = ""
        if self.fechaEntrega and self.textoEntrega:
            info_entrega = " [Entrega: %s; %s]" % (
                utils.str_fecha(self.fechaEntrega),
                self.textoEntrega)
        elif self.fechaEntrega:
            info_entrega = " [Entrega: %s]" % (
                utils.str_fecha(self.fechaEntrega))
        elif self.textoEntrega:
            info_entrega = " [Entrega: %s]" % (self.textoEntrega)
        total_ldp = self.get_subtotal()
        res = "%s %s * %s = %s%s" % (
            utils.float2str(self.cantidad),
            self.producto.descripcion,
            precio_con_descuento,
            utils.float2str(total_ldp),
            info_entrega)
        return res

    @property
    def precioKilo(self):
        """
        Devuelve el precio por kilo de la línea de pedido siempre que sea
        posible. None si no lo puede calcular.
        """
        res = None
        # TODO: De momento solo para geotextiles.
        if hasattr(self.producto, "es_rollo") and self.producto.es_rollo():
            # El precio es por metro cuadrado. Tengo que hacer la conversión:
            gramos_m2 = self.producto.camposEspecificosRollo.gramos
            m2 = self.producto.camposEspecificosRollo.metrosCuadrados
            kilos = gramos_m2 / 1000.0 * m2
            try:
                res = self.precio * m2 / kilos
            except ZeroDivisionError:
                res = None
        return res

cont, tiempo = print_verbose(cont, total, tiempo)

class Ticket(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    lineasDeVenta = MultipleJoin('LineaDeVenta')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_iva(self):
        """
        Devuelve el IVA aplicable al ticket en función de su fecha: antes
        del 1 de julio de 2010, 16%; después y hasta el 1 de septiembre de
        2012, el 18%. A partir de entonces, el 21%
        """
        fechahora = mx.DateTime.DateFrom(self.fechahora.year,
                                         self.fechahora.month,
                                         self.fechahora.day)
        if fechahora >= mx.DateTime.DateFrom(2012, 9, 1):
            iva = 0.21
        elif (fechahora >= mx.DateTime.DateFrom(2010, 7, 1) and
            fechahora < mx.DateTime.DateFrom(2012, 9, 1)):
            iva = 0.18
        else:
            iva = 0.16
        return iva

    def calcular_total(self, iva_incluido = True):
        """
        Devuelve el total del ticket basándose en la cantidad y
        precios de la LDV.
        El total incluye IVA por defecto.
        """
        try:
            subtotal = self._connection.queryOne("""
                SELECT SUM(precio * cantidad * (1 - descuento))
                FROM linea_de_venta
                WHERE ticket_id = %d;""" % self.id)[0]
            #print "  --> He usado consulta."
            if subtotal is None:
                raise TypeError
        except (IndexError, TypeError):
            subtotal = 0
            for ldv in self.lineasDeVenta:
                subtotal += ldv.precio * ldv.cantidad * (1 - ldv.descuento)
            #print "  --> No he usado consulta."
        if iva_incluido:
            iva = self.get_iva()
            # Las ventas de ticket llevan impepinablemente el 21% de IVA.
        else:
            iva = 0
        total = subtotal * (1 + iva)
        return total

    def get_facturas(self):
        """
        Devuelve las facturas relacionadas con el ticket
        a través de sus líneas de venta.
        """
        fras = []
        for ldv in self.lineasDeVenta:
            fra = ldv.facturaVenta or ldv.prefactura
            if fra != None and fra not in fras:
                fras.append(fra)
        return fras

cont, tiempo = print_verbose(cont, total, tiempo)

class Venta:
    """
    Superclase de líneas de venta y servicios. Define interfaz e implementa
    métodos comunes.
    """
    def get_comercial(self):
        """
        Devuelve el comercial relacionado con la LDV a través del pedido de
        venta.
        Devuelve None si el pedido no tiene pedido o comercial relacionado.
        """
        try:
            return self.pedidoVenta.comercial
        except AttributeError:
            return None

    comercial = property(get_comercial)

    def get_proveedor(self):
        """
        Devuelve el proveedor relacionado con la LDV a través del producto.
        """
        try:
            return self.producto.proveedor
        except AttributeError:
            return None

    proveedor = property(get_proveedor)

cont, tiempo = print_verbose(cont, total, tiempo)

class LineaDeVenta(SQLObject, PRPCTOO, Venta):
    class sqlmeta:
        fromDatabase = True
    #----------------------------- productoVentaID = ForeignKey('ProductoVenta')
    #----------- productoCompraID = ForeignKey('ProductoCompra', default = None)
    #--------------------------------- pedidoVentaID = ForeignKey('PedidoVenta')
    #----------------------------- albaranSalidaID = ForeignKey('AlbaranSalida')
    #------------------------------- facturaVentaID = ForeignKey('FacturaVenta')
    #------------------- prefacturaID = ForeignKey('Prefactura', default = None)
    lineasDeAbono = MultipleJoin('LineaDeAbono')
    #--------------------------- ticketID = ForeignKey('Ticket', default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        res = "%s %s de %s a %s = %s" % (utils.float2str(self.cantidad),
            self.producto.unidad, self.producto.descripcion,
            utils.float2str(self.precio), utils.float2str(self.get_subtotal()))
        if self.factura:
            res += " (factura %s)" % self.factura.get_info()
        elif self.albaranSalida:
            res += " (albarán %s)" % self.albaranSalida.get_info()
        return res

    def get_almacen(self):
        """
        Devuelve el almacén relacionado con la línea de devolución, que será
        aquel al que se haya devuelto la mercancía.
        """
        return self.albaranSalida and self.albaranSalida.almacenOrigen or None

    def get_cliente(self):
        """
        Devuelve el objeto cliente de la LDV según su pedido, albarán o
        factura. Por ese orden.
        """
        try:
            return self.pedidoVenta.cliente
        except AttributeError:
            try:
                return self.albaranSalida.cliente
            except AttributeError:
                try:
                    return self.facturaVenta.cliente
                except AttributeError:
                    try:
                        return self.prefactura.cliente
                    except AttributeError:
                        return None

    def calcular_precio_unitario_coherente(self, precision = 3):
        """
        Devuelve un precio unitario como cadena con los decimales suficientes
        (hasta un máximo de 5 y comenzando por «precision») para que al
        multiplicarlo por la cantidad dé el subtotal con la precisión recibida
        (por defecto, 3 -por compatibilidad hacia atrás-).
        """
        totlinea = self.get_subtotal()
        cantidad = self.cantidad
        precio = utils.float2str_autoprecision(self.precio,
                                               totlinea,
                                               cantidad,
                                               precision)
        return precio

    def get_factura_o_prefactura(self):
        """
        Devuelve la factura relacionada, tanto si es facturaVenta
        como prefactura, o None si no tiene ninguna de ellas.
        Como no debería tener ambos valores distintos de nulo a
        la vez, tiene preferencia facturaVenta sobre prefactura.
        """
        return self.facturaVenta or self.prefactura

    @property
    def factura(self):
        return self.get_factura_o_prefactura()

    def get_producto(self):
        """
        Devuelve el objeto producto relacionado con la línea de venta, sea
        del tipo que sea (productoVenta o productoCompra). None si no hay
        ningún producto relacionado.
        """
        res = None
        if self.productoVenta != None:
            res = self.productoVenta
        elif self.productoCompra != None:
            res = self.productoCompra
        return res

    def set_producto(self, producto):
        """
        Comprueba qué tipo de producto es el del parámetro "producto"
        recibido e instancia el atributo adecuado poniendo a
        None el del tipo de producto que no corresponda.
        Si la clase del objeto no es ninguna de las soportadas por
        la línea de venta, lanzará una excepción TypeError.
        """
        if isinstance(producto, ProductoVenta):
            self.productoVenta = producto
            self.productoCompra = None
        elif isinstance(producto, ProductoCompra):
            self.productoVenta = None
            self.productoCompra = producto
        else:
            raise TypeError

    producto = property(get_producto, set_producto,
                        "Objeto producto de venta o de compra relacionado con"
                        " la línea de venta.")

    def get_tarifa(self):
        """
        Devuelve la tarifa relacionada con la línea de venta.
        La forma de determinarla es:
        1.- Si pertenece a un pedido y tiene tarifa, comprueba que el precio
            de la LDV sea el de la tarifa del pedido.
        2.- Si el pedido no tiene tarifa o no coincide con el precio de la LDV
            para el producto, busca entre todas las tarifas del sistema aquella
            que tenga el mismo precio para el mismo producto y los periodos de
            validez a None o dentro de la fecha del pedido o de la fechahora de
            la LDV, por este orden.
        3.- Si no coincide ninguna o el precio es 0, devuelve None.
        4.- ...
        5.- Profit!
        """
        tarifa = None
        if (self.pedidoVenta and
            self.pedidoVenta.tarifaID != None and
            abs(self.pedidoVenta.tarifa.obtener_precio(self.producto)
                - self.precio) < 0.001):
                # NOTA: Manejamos siempre 3 decimales como mucho en precios.
                #       No hay que ser más papistas que el papa.
            tarifa = self.pedidoVenta.tarifa
        elif self.precio == 0.0:
            tarifa = None
        else:
            primera = None
            for t in Tarifa.select(orderBy = "-id"):
                # Empiezo a recorrer partiendo de la última tarifa, ya que
                # probablemente sea la que esté vigente y seguramente sea la
                # que interesa obtener en caso de que el pedido no tuviera
                # tarifa.
                if abs(t.obtener_precio(self.producto) - self.precio) < 0.001:
                    fechaldv = (self.pedidoVenta
                                and self.pedidoVenta.fecha
                                or self.fechahora)
                    if ((not t.periodoValidezIni
                         or t.periodoValidezIni <= fechaldv)
                        and
                        (not t.periodoValidezFin
                         or t.periodoValidezFin >= fechaldv)
                       ):
                        tarifa = t
                        if not primera:
                            primera = tarifa
                        if t.esta_en_tarifa(self.producto):
                            primera = t
                            break
                        # Si no está en la tarifa, aunque coincida el precio,
                        # sigo buscando. Si al final no estaba en ninguna
                        # tarifa devolverá la primera con la que coincidió o
                        # la última de todas.
            if primera:
                tarifa = primera
        return tarifa

    def get_str_bultos(self):
        """
        Devuelve los bultos de la línea de venta como
        cadena de texto con las unidades del producto.
        Si el producto son balas o bigbags, no se puede
        saber a priori cuántos bultos pertenecen a
        la línea de venta.
        Si la línea de venta no es de un producto de
        venta devuelve "?"
        """
        res = "?"
        if self.productoVentaID != None:
            if self.productoVenta.es_rollo():
                try:
                    cantidad = utils.float2str(self.cantidad /
                    self.productoVenta.camposEspecificosRollo.metros_cuadrados,
                    0)
                except ZeroDivisionError:
                    cantidad = "0"
                unidad = "rollos"
            elif self.productoVenta.es_bala():
                # TODO: Habrá que hacer un método copiado de la forma de
                # repartir balas entre LDVs de albaranes de salida.
                cantidad = "?"
                unidad = "balas"
            elif self.productoVenta.es_bigbag():
                # TODO: Habrá que hacer un método copiado de la forma de
                # repartir bigbags entre LDVs de albaranes de salida.
                cantidad = "?"
                unidad = "bigbags"
            elif self.productoVenta.es_caja():
                try:
                    cantidad = utils.float2str(self.cantidad /
                       self.productoVenta.camposEspecificosBala.gramosBolsa, 0)
                except ZeroDivisionError:
                    cantidad = "0"
                unidad = "bolsa"
            else:
                cantidad = ""
                unidad = ""
            res = "%s %s" % (cantidad, unidad)
        elif self.productoCompraID != None:
            # res = "%s %s" % (self.cantidad, self.productoCompra.unidad)
            res = "-"
        return res

    def get_str_cantidad(self):
        """
        Devuelve la cantidad de la línea de venta como
        cadena de texto con las unidades del producto.
        Si el producto no es un productoVenta devuelve "?".
        """
        res = "?"
        if self.productoVentaID != None:
            if self.productoVenta.es_rollo():
                unidad = "m²"
            elif (self.productoVenta.es_bala()
                  or self.productoVenta.es_bigbag()
                  or self.productoVenta.es_caja()):
                unidad = "kg"
            else:
                unidad = ""
            res = "%s %s" % (utils.float2str(self.cantidad), unidad)
        elif self.productoCompraID != None:
            unidad = self.productoCompra.unidad
            res = "%s %s" % (utils.float2str(self.cantidad), unidad)
        return res

    def get_cantidad_total_solicitada_del_producto(self):
        """
        Devuelve la cantidad total del producto de
        esta línea de venta solicitada en el pedido completo,
        SIN TENER EN CUENTA PRECIOS.
        """
        res = 0
        if self.pedidoVentaID != None:
            for ldv in self.pedidoVenta.lineasDeVenta:
                if ldv.producto == self.producto:
                    res += ldv.cantidad
        return res

    def get_cantidad_albaraneada(self):
        """
        Si la LDV pertenece a un albarán, devuelve la
        cantidad albaraneada de su producto en ese
        albarán. Si no, devuelve 0.
        """
        res = 0
        if self.albaranSalidaID != None:
            producto = self.producto
            if isinstance(producto, ProductoVenta):     # Si es un producto de
                    # venta, contamos las cantidades de sus bultos (artículos).
                # PLAN: Optimizar. El agrupar_articulos es bastante lento.
                articulos_clasificados = self.albaranSalida.agrupar_articulos()
                res = articulos_clasificados[self.id]['cantidad']
                # XXX: Ojito porque si es producto C, la cantidad del LDV (que
                # es la que se factura) puede diferir de la suma de sus
                # artículos (que es la que se descuenta de existencias). Esto
                # es así por diseño (CWT) y poder vender al peso incluyendo
                # plásticos, agua, residuos, etc.
            elif isinstance(producto, ProductoCompra):  # Si es un producto de
                # compra, la cantidad albaraneada es la de la propia LDV,
                res = self.cantidad                     # ya que no tiene
                # bultos ni nada que se pueda contar aparte de eso.
        return res

    def get_cantidad_albaraneada_por_calidad(self):
        """
        Si la LDV pertenece a un albarán, devuelve la
        cantidad albaraneada de su producto en ese
        albarán divididas por clase: A, B y C; y por unidades:
        bultos, kilos y m² (si procede).
        Si no, lanza una excepción: TypeError para cuando se trata una
        línea de venta con producto de compra y ValueError si un artículo
        no es A, B ni C (No debería pasar a no ser que se haya quedado un
        artículo a medio crear o a medio borrar. Y creo que ni eso)
        """
        res = {'a':     {'m²': 0.0,
                         'kg': 0.0,
                         '#' : 0},
               'b':     {'m²': 0.0,
                         'kg': 0.0,
                         '#' : 0},
               'c':     {'m²': 0.0,
                         'kg': 0.0,
                         '#' : 0},
               'total': {'m²': 0.0,
                         'kg': 0.0,
                         '#' : 0}
              }
        if self.albaranSalidaID != None:
            producto = self.producto
            if isinstance(producto, ProductoVenta):     # Si es un producto de
                    # venta, contamos las cantidades de sus bultos (artículos).
                # PLAN: Optimizar. El agrupar_articulos es bastante lento.
                articulos_clasificados = self.albaranSalida.agrupar_articulos()
                articulos = articulos_clasificados[self.id]['articulos']
                # XXX: Ojito porque si es producto C, la cantidad del LDV (que
                # es la que se factura) puede diferir de la suma de sus
                # artículos (que es la que se descuenta de existencias). Esto
                # es así por diseño (CWT) y poder vender al peso incluyendo
                # plásticos, agua, residuos, etc.
                for a in articulos:     # Momento de clasificar
                    superficie = a.superficie
                    if superficie == None:
                        superficie = 0.0    # Para no joder el acumulado.
                    peso = a.peso   # Con embalaje, que es como se vende.
                    bultos = 1 # Un artículo, un bulto. Al menos eso está claro
                    if a.es_clase_a():
                        res['a']['m²'] += superficie
                        res['a']['kg'] += peso
                        res['a']['#'] += 1
                    elif a.es_clase_b():
                        res['b']['m²'] += superficie
                        res['b']['kg'] += peso
                        res['b']['#'] += 1
                    elif a.es_clase_c():
                        # Los productos C no tienen m².
                        res['c']['kg'] += peso
                        res['c']['#'] += 1
                    else:
                        txtexcepcion = "pclases::__init__ -> Artículo %s "\
                                "no es A, B ni C." % a.puid
                        raise ValueError, txtexcepcion
                    res['total']['m²'] += superficie
                    res['total']['kg'] += peso
                    res['total']['#'] += 1
            elif isinstance(producto, ProductoCompra):  # Si es un producto de
                # compra, no se puede dividir en A, B y C por artículo.
                res = None
        if res == None:
            txtexception = "pclases::__init__ -> Solo los productos de venta "\
                    "pueden clasificarse por calidad (A, B y C)."
            raise TypeError, txtexception
        return res

    def eliminar(self):
        """
        Intenta eliminar la línea de venta.
        Si tiene relaciones activas con
        albaranes, pedidos o facturas no la
        eliminará.
        Devuelve 0 si se elimina de la BD y
        el número de relaciones en otro caso.
        """
        rels = 0
        if self.pedidoVenta != None:
            rels += 1
        if self.albaranSalida != None:
            rels += 1
        if self.facturaVenta != None:
            rels += 1
        if self.prefactura != None:
            rels += 1
        if rels == 0:
            try:
                self.destroy()
            except Exception, msg:
                # No es buena práctica capturar _cualquier_ excepción
                # genérica. Esto es eventual para temas de depuración.
                myprint("ERROR: pclases::LineaDeVenta:eliminar-> No se pudo eliminar la LDV. Excepción disparada: %s" % (msg))
        return rels

    cantidad_albaraneada = property(get_cantidad_albaraneada)
    cantidad_total_solicitada_del_producto = property(get_cantidad_total_solicitada_del_producto)

    def get_subtotal(self, iva = False, descuento = True, precision = None,
                     prorrateado = False):
        """
        Devuelve el subtotal con o sin IVA (según se indique) de
        la línea de compra: precio * cantidad - descuento.
        Si prorrateado es True devuelve el importe correspondiente
        proporcional a un vencimiento de la factura o del proveedor si
        corresponde a un albarán no facturado.
        """
        asserterror = "Precision debe ser None o un número entero postivo."
        assert precision == None or (isinstance(precision, int)
                                     and precision >= 0), asserterror
        res = self.cantidad * self.precio
        if descuento:
            res *= (1 - self.descuento)
        if iva:
            if self.facturaVentaID != None:
                res *= 1 + self.facturaVenta.iva
            elif self.prefacturaID != None:
                res *= 1 + self.prefactura.iva
            elif self.pedidoVentaID != None:
                res *= 1 + self.pedidoVenta.iva
            elif (self.albaranSalidaID != None
                  and self.albaranSalida.clienteID != None):
                res *= 1 + self.albaranSalida.cliente.iva
            elif self.ticketID != None:
                res *= 1.21     # PVP siempre 21% de IVA.
        if prorrateado:
            try:
                numvtos = len(self.facturaVenta.vencimientosCobro)
            except AttributeError:
                try:
                    cliente = (self.pedidoVenta and self.pedidoVenta.cliente
                                or self.albaranSalida.cliente)
                    numvtos = max(1, len(cliente.get_vencimientos()))
                except AttributeError:
                    numvtos = 1
            res /= numvtos
        if precision != None:
            res = round(res, precision)
        return res

    calcular_subtotal = get_subtotal

    def calcular_beneficio(self):
        """
        Devuelve el precio de venta sin IVA por el porcentaje de la tarifa
        aplicada a la línea de venta y por la cantidad.
        Si la tarifa de la LDV no se pudo determinar, el porcentaje
        corresponde a la diferencia entre el precio por defecto y el precio de
        venta.
        """
        precio = self.precio
        cantidad = self.cantidad
        producto = self.producto
        tarifa = self.get_tarifa()
        if tarifa != None:
            porcentaje = tarifa.get_porcentaje(producto, fraccion = True)
        else:
            try:
                porcentaje = (precio / producto.precioDefecto) - 1.0
            except ZeroDivisionError:
                porcentaje = 1.0
        return producto.precioDefecto * porcentaje * cantidad

    def calcular_precio_costo(self):
        """
        Devuelve el precio de costo del producto de la LDV *en el momento
        actual* del cálculo.
        Es imposible, con el modelo de datos actual (29/04/2008) saber a
        qué precio de costo valorar el producto de compra. Se usa
        precioDefecto. Se podría usar la función de valoración, pero en ese
        caso se falsearía el método para calcular el beneficio.
        Por tanto, cambiar el precioDefecto (= precio de costo a todos los
        efectos) cambia la estimación del beneficio y este cálculo del precio
        de costo en ventas antiguas -esto es, anteriores al cambio-.
        Hago un método en vez de consultar directamente al producto por si
        en el futuro necesito cambiarlo, usar esta función desde el
        calcular_beneficio y demás; y así tener centralizado el asunto.
        """
        return self.producto.precioDefecto

cont, tiempo = print_verbose(cont, total, tiempo)

class LineaDePedidoDeCompra(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------------- productoCompraID = ForeignKey('ProductoCompra')
    #------------------------------- pedidoCompraID = ForeignKey('PedidoCompra')
    lineasDeCompra = RelatedJoin('LineaDeCompra',
                joinColumn='linea_de_pedido_de_compra_id',
                otherColumn='linea_de_compra_id',
                intermediateTable='linea_de_pedido_de_compra__linea_de_compra')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_precio_con_descuento(self):
        """
        Precio total de la línea incluyendo descuento, pero sin incluir el IVA.
        """
        return self.precio * (1 - self.descuento)

    precioConDescuento = property(get_precio_con_descuento,
                                  doc = get_precio_con_descuento.__doc__)

    def get_cantidad_servida(self):
        """
        Devuelve la cantidad servida del producto solicitado en la línea de
        pedido de compra. Si el producto se ha pedido en más de una LDPC
        se estima qué parte de la LDC se ha servido en cada una de ellas
        para avergiuar la cantidad restante de la LDPC actual.
        """
        producto = self.productoCompra
        pedida = self.cantidad
        servida = 0
        ldpcs = [self]
        ldcs = []
        if self.pedidoCompra == None:
            myprint("pclases.py::get_cantidad_servida -> ERROR: La línea de pedido de compra ID %d no tiene pedido." % (self.id))
            return 0
        for ldpc in self.pedidoCompra.lineasDePedidoDeCompra:
                # Hay una relación muchos a muchos entre LDC y LDPC que podría evitarme tirar del pedido de compra, construir
                # las dos listas, compararlas...
            if ldpc.productoCompraID == producto.id and ldpc != self:   # "Yo" ya estoy.
                pedida += ldpc.cantidad
                ldpcs.append(ldpc)
        for ldc in self.pedidoCompra.lineasDeCompra:
            if ldc.productoCompraID == producto.id:
                servida += ldc.cantidad
                ldcs.append(ldc)
        if servida >= pedida:
            # Si se ha servido todo, es un derroche de recursos ponerme a buscar nada. De esta LDPC se ha servido toda su cantidad.
            res = self.cantidad
        else:
            try:
                ldpcs.sort(utils.cmp_fecha_id)
            except TypeError, msg:
                myprint("pclases.py (get_cantidad_servida): Excepción al ordenar líneas de pedido de compra: %s" % (msg))
                myprint(ldpcs)
            try:
                ldcs.sort(utils.cmp_fecha_id)
            except TypeError, msg:
                myprint("pclases.py (get_cantidad_servida): Excepción al ordenar líneas de compra: %s" % (msg))
                myprint(ldcs)
            ildpc = 0
            while ildpc < len(ldpcs):
                ldpc = ldpcs[ildpc]
                servida -= ldpc.cantidad
                if ldpc == self:
                    if servida >= 0:
                        res = self.cantidad
                    else:
                        res = self.cantidad + servida
                    break
                ildpc += 1
        return res

    cantidadServida = property(get_cantidad_servida,
        doc="Cantidad servida correspondiente a la línea de pedido de compra.")

    def get_cantidad_pendiente(self):
        """
        Devuelve la cantidad pendiente de servir de la línea de pedido de compra actual.
        """
        return self.cantidad - self.cantidadServida

    cantidadPendiente = property(get_cantidad_pendiente,
        doc = "Cantidad pendiente de servir correspondiente a la línea de "
              "pedido de compra.")

    def get_subtotal(self, iva = False, descuento = True, prorrateado = False):
        """
        Devuelve el subtotal con o sin IVA (según se indique) de
        la línea de compra: precio * cantidad - descuento.
        Si «prorrateado» es True, devuelve el importe dividido entre el número
        de vencimientos.
        """
        res = self.cantidad * self.precio
        if descuento:
            res *= (1 - self.descuento)
        if iva and self.pedidoCompraID:
            res *= (1 + self.pedidoCompra.iva)
        if prorrateado:
            try:
                numvtos = max(1, len(self.proveedor.get_vencimientos()))
            except (AttributeError, TypeError, ValueError):
                numvtos = 1
            res /= numvtos
        return res

    def es_igual_salvo_cantidad(self, ldpc):
        """
        Compara la LDPC con otra recibida. Devuelve True si los valores
        son iguales para los campos:
          - pedidoCompraID
          - albaranEntradaID
          - facturaCompraID
          - productoCompraID
          - precio
          - descuento
          - fecha de entrega
          - texto de entrega
        """
        campos = ("pedidoCompraID",
                  "productoCompraID",
                  "precio",
                  "descuento",
                  "textoEntrega",
                  "fechaEntrega"
                 )
        for campo in campos:
            if getattr(self, campo) != getattr(ldpc, campo):
                return False
        return True

cont, tiempo = print_verbose(cont, total, tiempo)

class PedidoCompra(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #------------------------------------- proveedorID = ForeignKey('Proveedor')
    lineasDeCompra = MultipleJoin('LineaDeCompra')
    lineasDePedidoDeCompra = MultipleJoin('LineaDePedidoDeCompra')
    documentos = MultipleJoin('Documento')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def unificar_ldcs(self):
        """
        Combina las líneas de compra del pedido que sólo
        difieran en la cantidad, en una sola.
        """
        a_borrar = []
        copia_ldcs = self.lineasDeCompra[:]     # Para evitar que se cambien de orden al actualizar cantidades.
        for i in xrange(len(copia_ldcs)):
            ldc1 = copia_ldcs[i]
            for j in xrange(i+1, len(copia_ldcs)):
                ldc2 = copia_ldcs[j]
                if ldc1 not in a_borrar and ldc2 not in a_borrar and ldc1.es_igual_salvo_cantidad(ldc2):
                    ldc1.cantidad += ldc2.cantidad
                    a_borrar.append(ldc2)
        for ldc in a_borrar:
            try:
                ldc.destroy()
            except:
                myprint("pclases.py::unificar_ldcs-> No se pudo eliminar la LDP ID %d. Se asigna 0 a cantidad para evitar descuadres." % (ldc.id))
                ldc.cantidad = 0

    def unificar_ldpcs(self):
        """
        Combina las líneas de compra del pedido que sólo
        difieran en la cantidad, en una sola.
        """
        a_borrar = []
        copia_ldpcs = self.lineasDePedidoDeCompra[:]     # Para evitar que se cambien de orden al actualizar cantidades.
        for i in xrange(len(copia_ldpcs)):
            ldpc1 = copia_ldpcs[i]
            for j in xrange(i+1, len(copia_ldpcs)):
                ldpc2 = copia_ldpcs[j]
                if ldpc1 not in a_borrar and ldpc2 not in a_borrar and ldpc1.es_igual_salvo_cantidad(ldpc2):
                    ldpc1.cantidad += ldpc2.cantidad
                    a_borrar.append(ldpc2)
        for ldpc in a_borrar:
            try:
                ldpc.destroy()
            except:
                myprint("pclases.py::unificar_ldpcs-> No se pudo eliminar la LDP ID %d. Se asigna 0 a cantidad para evitar descuadres." % (ldpc.id))
                ldpc.cantidad = 0

    def get_productos_pendientes_servir(self):
        """
        Devuelve una tupla de tuplas de objetos producto y la cantidad
        total pendiente de servir del mismo. No se tiene en cuenta si
        el pedido está o no cerrado y se considera que un resto negativo
        también es "pendiente". Es decir, sólo filtra y no devuelve
        aquellos productos cuya cantidad solicitada y cantidad servida
        coinciden por completo.
        """
        res = []
        productos = {}
        for ldpc in self.lineasDePedidoDeCompra:
            producto = ldpc.productoCompra
            if producto not in productos:
                productos[producto] = {'pedida': ldpc.cantidad, 'servida': 0}
            else:
                productos[producto]['pedida'] += ldpc.cantidad
        for ldc in self.lineasDeCompra:
            producto = ldc.productoCompra
            if producto not in productos:
                productos[producto] = {'pedida': 0, 'servida': ldc.cantidad}
            else:
                productos[producto]['servida'] += ldc.cantidad
        for producto in productos:
            diferencia = productos[producto]['pedida'] - productos[producto]['servida']
            if diferencia != 0:
                res.append((producto, diferencia))
        return tuple(res)

    def get_lineas_sin_albaranear(self):
        """
        Devuelve las LDPC del pedido que no están albaraneadas por completo.
        """
        res = []
        # DONE: Esta función está a punto de quedar obsoleta con la implementación de las nuevas líneas de pedido de compra.
        # return [ldc for ldc in self.lineasDeCompra if ldc.albaranEntradaID == None]
        for ldpc in self.lineasDePedidoDeCompra:
            if ldpc.cantidad > ldpc.cantidadServida:
                res.append(ldpc)
        return res

    def get_pendiente(self, producto):
        """
        Devuelve la cantidad pendiente de recibir del
        producto según el pedido actual y su valoración
        en precio.
        """
        cantidad, valor = 0, 0
        lineas_pendientes = [l for l in self.get_lineas_sin_albaranear() if l.productoCompra == producto]
        for linea in lineas_pendientes:
            cantidad += linea.cantidadPendiente
            valor += cantidad * linea.precio
        return cantidad, valor

    def get_menor_precio(self, productoCompra):
        """
        Devuelve el menor precio del pedido para el producto
        de compra recibido.
        Devuelve None si el producto no se solicitó en el pedido.
        """
        menor = None
        for ldpc in self.lineasDePedidoDeCompra:
            if ldpc.productoCompraID == productoCompra.id:
                precio = ldpc.precio * (1 - ldpc.descuento)
                if menor == None or precio < menor:
                    menor = precio
        return menor

    def get_cantidad_pedida(self, productoCompra):
        """
        Devuelve la cantidad pedida en total del producto de
        compra en este pedido.
        """
        cantidad = 0
        for ldpc in self.lineasDePedidoDeCompra:
            if ldpc.productoCompraID == productoCompra.id:
                cantidad += ldpc.cantidad
        return cantidad

cont, tiempo = print_verbose(cont, total, tiempo)

class Producto:
    """
    Superclase para productos de compra y de venta.
    ... que ya iba siendo hora.
    """
    @property
    def precioMinimo(self):
        """
        Devuelve el precio mínimo establecido para el tipo de producto. None
        si no se ha especificado.
        """
        try:
            linea = self.lineaDeProduccion
            res = linea.precioMinimo
        except AttributeError:
            res = None
        return res

    def es_granza(self):
        """
        Devuelve True si el producto es un producto de compra, es materia
        prima y lleva la palabra "GRANZA" en la descripción.
        """
        materiaprima = TipoDeMaterial.select(
                TipoDeMaterial.q.descripcion.contains('materia prima'))[0]
        try:
            res = (self.tipoDeMaterialID == materiaprima.id
                    and "granza" in self.descripcion.lower())
        except AttributeError:
            res = False     # Es un producto de compra.
        return res

    def es_fibra(self):
        """
        Devuelve True si el producto es un producto de venta y además
        es fibra (bala, balas de cable o bigbags de fibra de cemento)
        """
        try:
            return (self.es_bala() or self.es_bala_cable() or self.es_bigbag()
                    or self.es_caja())
        except AttributeError:
            return False

    def ajustar_a_fecha_pasada(self, fecha, cantidad = None, bultos = None,
                               almacen = None):
        """
        Método "virtual" que debe ser implementado por las clases hijas.
        Ajusta las existencias actuales en base a las que se le indiquen en
        la fecha «fecha».
        Esto se hace sumando y restando producciones, ventas, etc. hasta
        llegar al día actual.
        «cantidad» es el stock en las unidades del producto (metros, kilos...)
        «bultos» son las existencias en bultos completos (número de artículos
        si es un producto de venta o la cantidad que sea según la razón
        bultos/cantidad del producto de compra).
        Los dos parámetros no pueden ser None a la vez. Si alguno de los dos
        falta, intenta calcular el otro. Si no se puede calcular lanzará una
        excepción.
        Si no se especifica almacén ajustará las cantidades globales en
        función del origen/destino de la mercancía en cada albarán tratado.
        Si se especifica un almacén solo se tendrán en cuenta los movimientos
        de ese almacén y ajustará el global en consecuencia, pero no se
        hará nada en el resto de almacenes.
        """
        raise NotImplementedError


class ProductoCompra(SQLObject, PRPCTOO, Producto):
    class sqlmeta:
        fromDatabase = True
    #--------------------------- tipoDeMaterialID = ForeignKey('TipoDeMaterial')
    lineasDeCompra = MultipleJoin('LineaDeCompra')
    lineasDeVenta = MultipleJoin('LineaDeVenta')
    consumos = MultipleJoin('Consumo')
    consumosAdicionales = MultipleJoin('ConsumoAdicional')
    pruebasGranza = MultipleJoin('PruebaGranza')
    cargasSilo = MultipleJoin('CargaSilo')
    lineasDePedidoDeCompra = MultipleJoin('LineaDePedidoDeCompra')
    historialesExistenciasCompra = MultipleJoin('HistorialExistenciasCompra')
    precios = MultipleJoin('Precio')
    lineasDePedido = MultipleJoin('LineaDePedido')
    descuentosDeMaterial = MultipleJoin('DescuentoDeMaterial')
    stocksAlmacen = MultipleJoin("StockAlmacen")
    #----------- proveedorID = ForeignKey("Proveedor")   # Proveedor por defecto

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    preciopordefecto = property(lambda o: o.precioDefecto)

    def get_proveedor(self):
        """
        Devuelve el proveedor habitual (o por defecto) del producto.
        """
        try:
            res = self.get_proveedores()[0]
        except (AttributeError, IndexError):
            # Nunca se ha comprado el producto. Devuelvo el proveedor por
            # defecto.
            res = self.proveedor
        return res

    def es_nucleo_carton(self):
        """
        Devuelve TRUE si se puede considerar al producto como núcleo de
        cartón, o tubo. Es necesario porque ya van tres o cuatro sitios
        donde a este tipo de productos se le da un trato especial (sobre
        todo respecto a consumos) y crear un tipo de material sería aún
        más trabajoso -por uno de los clientes, más que nada-.
        Con un método especial, al menos el criterio estará unificado si
        algún día se (vuelve) a cambiar.
        """
        return (("cleo" in self.descripcion.lower()
                 and "cart" in self.descripcion.lower())
                or "tubo" in self.descripcion.lower())

    def es_geocompuesto(self):
        """
        Devuelve True si el producto es un geocompuesto (comercializado).
        Consideraremos que un producto de compra es geocompuesto si pertenece
        a un tipo de producto que contenga la cadena "eocompuesto" o
        "omercializado" en su descripción.
        """
        return (self.tipoDeMaterialID and
                ("eocompuesto" in self.tipoDeMaterial.descripcion.lower()
                 or "omercializado" in self.tipoDeMaterial.descripcion.lower())
               )

    def get_puid(self):
        """
        Devuelve una *cadena* con PV: y el ID del producto.
        puid viene a ser como ProductoUnicoID (un ID único para cada producto
        cuyo tipo de objeto se diferencia por la cadena que antecede a los :).
        """
        return "PC:%d" % self.id

    def corregir_almacenes(self):
        """
        Comprueba y corrige los almacenes para que la suma total sea
        igual a las existencias del producto.
        Siempre corrige del almacén principal en caso de desajustes y elimina
        las existencias negativas.
        """
        self.sync() # Me aseguro de que las existencias son las actuales
        print self.existencias
        for sa in self.stocksAlmacen:
            sa.sync()
            if sa.existencias < 0:
                sa.existencias = 0
            sa.syncUpdate()
        ppal = Almacen.get_almacen_principal()
        sappal = None
        resto = 0.0
        for sa in self.stocksAlmacen:
            if sa.almacen == ppal:
                sappal = sa
            else:
                resto += sa.existencias
        try:
            sappal.existencias = self.existencias - resto
        except AttributeError:  # No hay registro de almacén ppal. con stock.
            sappal = StockAlmacen(almacen = ppal,
                                  productoCompra = self,
                                  existencias = self.existencias - resto)
        sappal.sync()
        if sappal.existencias < 0:
            sappal.existencias = 0
            self.existencias = resto
            self.sync()
            sappal.sync()


    def set_existencias(self, cantidad, almacen = None):
        """
        Ajusta las existencias *actuales* del producto a la cantidad recibida.
        Si no se especifica almacén, se ajustará en base al almacén principal
        (según el contrato de add_existencias).
        Anotará en las observaciones del caché de existencias que se ha
        ajustado programáticamente.
        """
        #self.ajustar_a_fecha_pasada(fecha = mx.DateTime.today(),
        #                            cantidad = cantidad, almacen = almacen,
        #    observaciones_historico = "Cacheado por ajuste de existencias",
        #    check_assert = False)   # No tiene sentido comprobar nada porque
        #                            # estamos forzando las de HOY sin base
        #                            # ninguna de entradas y salidas.
        ## Pasando de tirar de un algoritmo que se pensó justamente para
        ## el caso contrario.
        self.sync()
        if not almacen:
            almacen = Almacen.get_almacen_principal()
        elif isinstance(almacen, int):
            try:
                almacen = Almacen.get(almacen)
            except:
                raise ValueError, "Si almacen es un número, debe coincidir"\
                                  " con un ID de la base de datos."
        # actual = self.existencias
        actual = self.get_existencias(almacen)
        delta = cantidad - actual
        self.add_existencias(delta, almacen, actualizar_global = True)
        # Me aseguro de que las existencias finales coinciden con el
        # el sumatorio de los almacenes, porque actualizar_global de
        # add_existencias trabaja con deltas. Si hay un error de coherencia
        # entre los stocksAlmacen y las existencias, se conservará después del
        # add_existencias.
        self.existencias = sum([sa.existencias for sa in self.stocksAlmacen])
        # Cacheo para que quede constancia de que es un ajuste manual:
        for a in Almacen.select():
            try:
                HistorialExistenciasCompra(productoCompra = self,
                        cantidad = a.get_existencias(self),
                        observaciones = "Cacheado por ajuste de existencias",
                        fecha = mx.DateTime.today(),
                        almacen = a)
            except:     # Integrity error. Ya existía para esa fecha.
                for hec in HistorialExistenciasCompra.select(AND(
                   HistorialExistenciasCompra.q.productoCompraID == self.id,
                   HistorialExistenciasCompra.q.almacenID == a.id,
                   HistorialExistenciasCompra.q.fecha == mx.DateTime.today())):
                    hec.destroySelf()
                HistorialExistenciasCompra(productoCompra = self,
                        cantidad = a.get_existencias(self),
                        observaciones = "Cacheado por ajuste de existencias",
                        fecha = mx.DateTime.today(),
                        almacen = a)

    def ajustar_a_fecha_pasada(self, fecha, cantidad = None, bultos = None,
                               almacen = None,
                               observaciones_historico
                                    = "Cacheado por ajuste de existencias "
                                      "a fecha pasada",
                               check_assert = True):
        """
        Ajusta las existencias actuales en base a las que se le indiquen en
        la fecha «fecha».
        Esto se hace sumando y restando producciones, ventas, etc. hasta
        llegar al día actual.
        «cantidad» es el stock en las unidades del producto (metros, kilos...)
        «bultos» son las existencias en bultos completos según la razón
        bultos/cantidad del producto de compra.
        Los dos parámetros no pueden ser None a la vez. Si alguno de los dos
        falta, intenta calcular el otro. Si no se puede calcular lanzará una
        excepción.
        Si no se especifica almacén ajustarán las cantidades globales tocando
        solo el almacén principal (no hay otra forma de hacerlo, ya que si
        las cantidades de los almacenes están mal, lo que tenemos es un
        sistema de n+1 ecuaciones con n incógnicas donde n = #almacenes).
        Si se especifica un almacén solo se tendrán en cuenta los movimientos
        de ese almacén y ajustará el global en consecuencia, pero no se
        hará nada en el resto de almacenes.
        Si check_assert es True comprobará después de ajustar que las
        existencias siguen siendo coherentes con los históricos, entradas y
        salidas (a False es útil para llamadas recursivas).
        """
        if cantidad == None:
            raise ValueError, "En productos de compra se debe especificar "\
                              "una cantidad. No es posible la estimación a "\
                              "partir de bultos."
        # 1.- Calcular entradas y salidas
        delta = {}
        if not almacen:
            for a in Almacen.select():
                delta[a] = self.get_entradas_y_salidas_entre(fecha,
                                                             almacen = a)
        else:
            delta[almacen] = self.get_entradas_y_salidas_entre(fecha,
                                                            almacen = almacen)
        if DEBUG:
            myprint("pclases::ajustar_a_fecha_pasada -> delta:")
            for alm in delta:
                myprint("\t%s: %s" % (alm.nombre, delta[alm]))
        # 2.- Eliminar cachés falsear consultas de históricos.
        i = 0
        if not almacen:
            for hec in self.historialesExistenciasCompra:
                hec.destroySelf()
                i += 1
        else:
            for hec in self.historialesExistenciasCompra:
                if hec.almacen == almacen:
                    hec.destroySelf()
                    i += 1
        if DEBUG:
            myprint("pclases::ajustar_a_fecha_pasada -> "\
                  "%d historiales eliminados." % i)
        # 3.- Actualizar existencias del almacén (si es caso) y globales.
        if DEBUG:
            myprint("pclases::ajustar_a_fecha_pasada -> "\
                  "Existencias actuales antes de tocar: %s" % (
                    utils.float2str(self.existencias)))
            for stock_alm in self.stocksAlmacen:
                myprint("\tAlmacén %s: %s" % (
                    stock_alm.almacen.nombre,
                    utils.float2str(stock_alm.existencias)))
        ppal = Almacen.get_almacen_principal()
        for alm_stock in self.stocksAlmacen:
            if almacen:
                if alm_stock.almacen == almacen:
                    alm_stock.existencias = (cantidad
                                                + delta[alm_stock.almacen])
                else:
                    pass    # No los toco
            else:   # No se especifica almacén. Ajusto el principal.
                if alm_stock.almacen == ppal:
                    # A la cantidad que debía haber en la fecha indicada, le
                    # sumo entradas y salidas totales para que me dé la
                    # cantidad actual. Después, como los demás almacenes no
                    # los voy a tocar, la diferencia de ambos totales es lo
                    # que meto en el principal a día de hoy.
                    total = cantidad + sum([delta[sa] for sa in delta])
                    #print total
                    total_menos_ppal = sum([sa.existencias
                                            for sa in self.stocksAlmacen
                                            if sa.almacen != ppal])
                    #print total_menos_ppal
                    alm_stock.existencias = total - total_menos_ppal
            alm_stock.sync()
        self.existencias = sum([sa.existencias for sa in self.stocksAlmacen])
        self.sync()

        if check_assert:
            if not almacen:
                try:
                    ehist = self.get_existencias_historico(fecha = fecha,
                            observaciones_historico = observaciones_historico)
                    assert ehist == cantidad, "get_existencias_historico: %f;"\
                                              " cantidad: %f" % (ehist,
                                                                 cantidad)
                except AssertionError:
                    # Estará tirando de históricos anteriores erróneos.
                    # Borro todo.
                    if DEBUG:
                        selfdesc = self.descripcion
                        myprint("\t... Borrando históricos de %s" % (selfdesc))
                    for hec in self.historialesExistenciasCompra:
                        hec.destroySelf()
                    # Y vuelvo a intentarlo.
                    self.ajustar_a_fecha_pasada(fecha, cantidad, bultos,
                                                almacen, check_assert = False)
                    ehist = self.get_existencias_historico(fecha = fecha,
                                                observaciones_historico
                                                    = observaciones_historico)
                    assert ehist == cantidad, "get_existencias_historico: %f;"\
                                              " cantidad: %f" % (ehist,
                                                                 cantidad)
            else:
                try:
                    ehist = self.get_existencias_historico(fecha = fecha,
                            almacen = almacen,
                            observaciones_historico = observaciones_historico)
                    assert ehist == cantidad, "get_existencias_historico: %f;"\
                                              " cantidad: %f" % (ehist,
                                                                 cantidad)
                except:
                    # Estará tirando de históricos anteriores erróneos.
                    # Borro todo.
                    if DEBUG:
                        selfdesc = self.descripcion
                        myprint("\t... Borrando históricos de %s" % selfdesc)
                    for hec in self.historialesExistenciasCompra:
                        hec.destroySelf()
                    # Y vuelvo a intentarlo.
                    self.ajustar_a_fecha_pasada(fecha, cantidad, bultos,
                                                almacen, check_assert = False)
                    ehist = self.get_existencias_historico(fecha = fecha,
                            almacen = almacen,
                            observaciones_historico = observaciones_historico)
                    assert ehist == cantidad, "get_existencias_historico: %f;"\
                                              " cantidad: %f" % (ehist,
                                                                 cantidad)
        if DEBUG:
            myprint("pclases::ajustar_a_fecha_pasada -> "\
                  "Existencias actualizadas a %s:"  % (
                    utils.float2str(self.existencias)))
            for stock_alm in self.stocksAlmacen:
                myprint("\tAlmacén %s: %s" % (
                    stock_alm.almacen.nombre,
                    utils.float2str(stock_alm.existencias)))

    def get_existencias_historico(self,
                                  fecha = mx.DateTime.localtime(),
                                  forzar = False,
                                  almacen = None,
                                  observaciones_historico
                                    = "Cacheado automáticamente"):
        """
        Devuelve las existencias del producto de compra en
        la fecha proporcionada. Si no se le pasa ninguna
        devuelve las existencias -que en teoría- deberían ser
        las actuales (salvo pequeña desviación de fechas en
        albaranes, consumos o por CORRECCIONES MANUALES).
        0.- Si fecha es la fecha actual devuelve las existencias en tabla.
        PROTOCOLO DE CACHÉ:
            1.- Buscar la fecha recibida en la tabla HistorialExistenciasCompra
            2.- Si se encuentra:
                2.1.- Si forzar = False:
                    2.1.1.- Devuelve la cantidad de la tabla.
                    2.1.2.- EOA.
                2.2.- Si forzar = True:
                    2.2.1.- Elimina el registro de la caché.
                    2.2.1.- Pasa al paso 3.
            3.- Busca en la tabla historialExistenciasCompra la fecha
                anterior más cercana a la recibida.
            4.- Si encuentra una fecha:
                4.1.- A la cantidad en esa fecha resta los consumos y salidas
                      del producto entre las fechas del histórico y la
                      recibida.
                4.2.- A la cantidad resultante suma las entradas entre la
                      fecha del histórico y la fecha recibida.
            (4 1/2.- Aquí cabría la posibilidad de poder hacer la operación
                     inversa: partir de un registro de caché superior a la
                     fecha recibida y restar entradas y sumar consumos y
                     salidas en lugar de hacerlo al contrario como en el
                     paso 4.)
            5.- Si no encuentra una fecha anterior:
                4.1.- Del total actual de existencias suma los consumos y
                      salidas del producto DESDE la fecha recibida.
                4.2.- A la cantidad resultante resta las entradas de los
                      albaranes DESDE la fecha recibida.
            6.- Crea un registro en la tabla histórico con la fecha y
                cantidad resultante.
        ### ACTUALIZACIÓN ALMACENES
        Si almacen == None, se devuelve el histórico de la suma de todas las
        almacenes. Si es != None, devuelve el histórico para ese almacén en
        concreto.
        """
        res = None
        if fecha == mx.DateTime.localtime():
            if not almacen:
                res = self.existencias
            else:
                res = self.get_existencias(almacen)
        else:
            HEC = HistorialExistenciasCompra
            if almacen:
                regs_cache = HEC.select(AND(HEC.q.productoCompraID == self.id,
                                            HEC.q.fecha == fecha,
                                            HEC.q.almacenID == almacen.id))
                if regs_cache.count() > 1:
                    myprint("WARNING: pclases.py (get_existencias_historico) "\
                          "-> Más de un registro en caché o forzado por "\
                          "parámetro. Los elimino todos y recuento.")
                    for reg in regs_cache:
                        reg.destroySelf()
                    res = self.get_existencias_historico(fecha,
                            almacen = almacen,
                            observaciones_historico = observaciones_historico)
                elif regs_cache.count() == 1:
                    if not forzar:
                        res = regs_cache[0].cantidad
                    else:
                        regs_cache[0].destroySelf()
                        res = None
            else:       # not almacen
                # Para todos los almacenes necesito sumatorio, pero no a partir
                # de registros directos de la BD porque puede que un almacén no
                # esté cacheado en esa fecha y haga falta interpolación.
                caches_almacenes = []
                for a in Almacen.select():
                    cache = self.get_existencias_historico(fecha, almacen = a,
                            forzar = forzar,
                            observaciones_historico = observaciones_historico)
                    caches_almacenes.append(cache)
                res = sum(caches_almacenes)
        # ---
        if res == None: # Aún no he encontrado las existencias, bien por
                        # no caché o bien porque hay que forzar.
            if almacen:
                cache_mas_cercano = HEC.select(
                    AND(HEC.q.fecha < fecha,
                        HEC.q.productoCompraID == self.id,
                        HEC.q.almacenID == almacen.id),
                    orderBy = "-fecha")
                if cache_mas_cercano.count() >= 1:
                    cache_mas_cercano = cache_mas_cercano[0]
                    # En un caso raro, podría ser None. Aseguro un número:
                    existencias_anteriores = cache_mas_cercano.cantidad or 0
                    entradas_y_salidas = self.get_entradas_y_salidas_entre(
                        mx.DateTime.DateFrom(cache_mas_cercano.fecha)
                            + mx.DateTime.oneDay, fecha,
                        almacen = almacen)
                        # Le sumo un día porque en el caché ya están incluídas
                        # las existencias justo hasta las 23:59:59 de ese mismo
                        # día.
                    res = existencias_anteriores + entradas_y_salidas
                    if DEBUG:
                        myprint("pclases::ProductoCompra."\
                              "get_existencias_historico -> %s | %s | Caché "\
                              "más cercano:" % (fecha.strftime("%Y-%m-%d"),
                                        almacen and almacen.nombre or "-"), \
                              cache_mas_cercano.fecha.strftime("%Y-%m-%d"),\
                              "; existencias_anteriores:", \
                              existencias_anteriores, \
                              "; entradas_y_salidas:", entradas_y_salidas, \
                              "; res:", res)
                else:
                    res=(self.get_existencias(almacen)
                         - self.get_entradas_y_salidas_entre(fecha,
                                                             fechafin = None,
                                                             almacen=almacen))
                nuevo_cache = HEC(productoCompraID = self.id,  # @UnusedVariable
                                  fecha = fecha,
                                  cantidad = res,
                                  observaciones = observaciones_historico,
                                  almacen = almacen)
            else:   # not almacen. Misma movida pero uno por uno. No debería
                    # entrar aquí porque es un caso que debería cubrir la rama
                    # else del if anterior... ¿salvo que haya que forzar?
                caches_almacenes = []
                for a in Almacen.select():
                    cache = self.get_existencias_historico(fecha, forzar, a,
                        observaciones_historico = observaciones_historico)
                    caches_almacenes.append(cache)
                res = sum([caches_almacenes])
        if DEBUG:
            myprint("pclases::get_existencias_historico -> self:",
                    self.descripcion, "[", self.get_puid(), "]",
                    "| res:", res, "| fecha:", fecha, "| forzar:", forzar,
                    "| almacen:", almacen and almacen.nombre or "-")
        return res

    def __get_consultas_entradas_y_salidas_desde(self, sqlfechaini,
                                                 almacen = None):
        """
        Devuelve tres ResultSelect de entradas, consumos y salidas del
        producto de compra desde la fecha indicada en formato SQL (%Y-%m-%d).
        Si almacen != None, devuelve lo anterior pero solo para ese almacén.
        Dado que la mayoría de consumos también se contabilizan en un albarán
        interno de consumo, no se devolverán los consumos que pertenezcan a un
        parte que tenga albarán interno y éste una línea de venta con el
        mismo producto y cantidad que el consumo.
        """
        # XXX
        """
        #unittest:
        from framework import pclases
        import mx.DateTime
        pclases.DEBUG = True
        pc = pclases.ProductoCompra.select(
            pclases.ProductoCompra.q.descripcion.contains("PLAST"),
            orderBy = "id")[0]
        fechaini = mx.DateTime.DateTimeFrom(2009,1,1)
        pc.get_entradas_y_salidas_entre(fechaini)
        pc.get_entradas_y_salidas_entre(fechaini,
            almacen = pclases.Almacen.get_almacen_principal())
        pc.get_entradas_y_salidas_entre(fechaini,
            almacen = pclases.Almacen.select(orderBy = "-id")[0])
        """

        if not almacen:
            entradas = LineaDeCompra.select("""
                producto_compra_id = %d AND
                albaran_entrada_id IN (SELECT albaran_entrada.id
                                         FROM albaran_entrada
                                        WHERE albaran_entrada.fecha >= '%s')
                """ % (self.id, sqlfechaini))
            # Ahora también pueden entrar productos en albaranes de salida
            # procedentes de otro almacén.
            entradas2 = LineaDeVenta.select("""
                producto_compra_id = %d AND
                albaran_salida_id IN (SELECT albaran_salida.id
                                        FROM albaran_salida
                                       WHERE albaran_salida.fecha >= '%s'
                                         AND almacen_destino_id IS NOT NULL)
                """ % (self.id, sqlfechaini))
            if DEBUG:
                myprint(" --> entradas:",entradas.count()," +",entradas2.count())
            entradas = SQLlist(SQLlist(entradas) + SQLlist(entradas2))
        else:
            entradas = LineaDeCompra.select("""
                producto_compra_id = %d AND
                albaran_entrada_id IN (SELECT albaran_entrada.id
                                         FROM albaran_entrada
                                        WHERE albaran_entrada.fecha >= '%s'
                                          AND almacen_id = %d)
                """ % (self.id, sqlfechaini, almacen.id))
            # Ahora también pueden entrar productos en albaranes de salida
            # procedentes de otro almacén.
            entradas2 = LineaDeVenta.select("""
                producto_compra_id = %d AND
                albaran_salida_id IN (SELECT albaran_salida.id
                                        FROM albaran_salida
                                       WHERE albaran_salida.fecha >= '%s'
                                         AND almacen_destino_id = %d)
                """ % (self.id, sqlfechaini, almacen.id))
            entradas = SQLlist(SQLlist(entradas) + SQLlist(entradas2))
            if DEBUG:
                myprint(" --> entradas:",entradas.count(), "+", entradas2.count())
        if not almacen:
            salidas_consumos = Consumo.select("""
                producto_compra_id = %d AND
                parte_de_produccion_id IN (
                    SELECT parte_de_produccion.id
                      FROM parte_de_produccion
                     WHERE parte_de_produccion.fecha >= '%s')
                """ % (self.id, sqlfechaini))
        else:
            if almacen is Almacen.get_almacen_principal_or_none():
                # Solo se puede consumir del almacén principal.
                salidas_consumos = Consumo.select("""
                    producto_compra_id = %d AND
                    parte_de_produccion_id IN (
                        SELECT parte_de_produccion.id
                          FROM parte_de_produccion
                         WHERE parte_de_produccion.fecha >= '%s')
                    """ % (self.id, sqlfechaini))
            else:
                salidas_consumos = SQLtuple([])
        if DEBUG:
            myprint(" <-* consumos(prefilter):", salidas_consumos.count())
        # Ahora filtro para quitar los consumos que se han contado en
        # albaranes internos. Esto va a ser lento y doloroso, peque...
        _salidas_consumos, salidas_consumos = salidas_consumos[:], []
        for c in _salidas_consumos:
            ldv = c.get_linea_de_venta_albaran_interno()
            if not ldv:
                salidas_consumos.append(c)
        salidas_consumos = SQLtuple(salidas_consumos)
        if DEBUG:
            myprint(" <-- consumos:", salidas_consumos.count())
        if not almacen:
            salidas_albaranes = LineaDeVenta.select("""
                producto_compra_id = %d AND
                albaran_salida_id IN (SELECT albaran_salida.id
                                      FROM albaran_salida
                                      WHERE albaran_salida.fecha >= '%s')
                """ % (self.id, sqlfechaini))
        else:
            salidas_albaranes = LineaDeVenta.select("""
                producto_compra_id = %d AND
                albaran_salida_id IN (SELECT albaran_salida.id
                                      FROM albaran_salida
                                      WHERE albaran_salida.fecha >= '%s'
                                        AND almacen_origen_id = %d)
                """ % (self.id, sqlfechaini, almacen.id))
        if DEBUG:
            myprint(" <-- salidas:", salidas_albaranes.count())
        return entradas, salidas_consumos, salidas_albaranes

    def __get_consultas_entradas_y_salidas_entre(self,
                                                 sqlfechaini,
                                                 sqlfechafin,
                                                 almacen = None):
        """
        Devuelve tres ResultSelect de entradas, consumos y salidas del
        producto de compra desde y hasta las fecha indicadas en formato
        SQL (%Y-%m-%d).
        Si almacen != None, devuelve lo anterior pero solo para ese almacén.
        Dado que la mayoría de consumos también se contabilizan en un albarán
        interno de consumo, no se devolverán los consumos que pertenezcan a un
        parte que tenga albarán interno y éste una línea de venta con el
        mismo producto y cantidad que el consumo.
        """
        if not almacen:
            entradas = LineaDeCompra.select("""
                producto_compra_id = %d AND
                albaran_entrada_id IN (SELECT albaran_entrada.id
                                       FROM albaran_entrada
                                       WHERE albaran_entrada.fecha <= '%s'
                                       AND albaran_entrada.fecha >= '%s')
                """ % (self.id, sqlfechafin, sqlfechaini))
            # Ahora también pueden entrar productos en albaranes de salida
            # procedentes de otro almacén.
            entradas2 = LineaDeVenta.select("""
                producto_compra_id = %d AND
                albaran_salida_id IN (SELECT albaran_salida.id
                                        FROM albaran_salida
                                       WHERE albaran_salida.fecha >= '%s'
                                         AND albaran_salida.fecha <= '%s'
                                         AND almacen_destino_id IS NOT NULL)
                """ % (self.id, sqlfechafin, sqlfechaini))
            entradas = SQLlist(SQLlist(entradas) + SQLlist(entradas2))
        else:
            entradas = LineaDeCompra.select("""
                producto_compra_id = %d AND
                albaran_entrada_id IN (SELECT albaran_entrada.id
                                       FROM albaran_entrada
                                       WHERE albaran_entrada.fecha <= '%s'
                                       AND albaran_entrada.fecha >= '%s'
                                       AND almacen_id = %d)
                """ % (self.id, sqlfechafin, sqlfechaini, almacen.id))
            # Ahora también pueden entrar productos en albaranes de salida
            # procedentes de otro almacén.
            entradas2 = LineaDeVenta.select("""
                producto_compra_id = %d AND
                albaran_salida_id IN (SELECT albaran_salida.id
                                        FROM albaran_salida
                                       WHERE albaran_salida.fecha >= '%s'
                                         AND albaran_salida.fecha <= '%s'
                                         AND almacen_destino_id = %d)
                """ % (self.id, sqlfechaini, sqlfechafin, almacen.id))
            entradas = SQLlist(SQLlist(entradas) + SQLlist(entradas2))
        if not almacen:
            salidas_consumos = Consumo.select("""
                producto_compra_id = %d AND
                parte_de_produccion_id IN (
                    SELECT parte_de_produccion.id
                      FROM parte_de_produccion
                     WHERE parte_de_produccion.fecha <= '%s'
                       AND parte_de_produccion.fecha >= '%s')
                """ % (self.id, sqlfechafin, sqlfechaini))
        else:
            if almacen is Almacen.get_almacen_principal_or_none():
                # Solo se puede consumir del almacén principal.
                salidas_consumos = Consumo.select("""
                    producto_compra_id = %d AND
                    parte_de_produccion_id IN (
                        SELECT parte_de_produccion.id
                          FROM parte_de_produccion
                         WHERE parte_de_produccion.fecha <= '%s'
                           AND parte_de_produccion.fecha >= '%s')
                    """ % (self.id, sqlfechafin, sqlfechaini))
            else:
                salidas_consumos = SQLtuple([])
        # Ahora filtro para quitar los consumos que se han contado en
        # albaranes internos. Esto va a ser lento y doloroso, peque...
        _salidas_consumos, salidas_consumos = salidas_consumos[:], []
        for c in _salidas_consumos:
            ldv = c.get_linea_de_venta_albaran_interno()
            if not ldv:
                salidas_consumos.append(c)
        salidas_consumos = SQLtuple(salidas_consumos)
        if not almacen:
            salidas_albaranes = LineaDeVenta.select("""
                producto_compra_id = %d AND
                albaran_salida_id IN (SELECT albaran_salida.id
                                      FROM albaran_salida
                                      WHERE albaran_salida.fecha <= '%s'
                                      AND albaran_salida.fecha >= '%s')
                """ % (self.id, sqlfechafin, sqlfechaini))
        else:
            salidas_albaranes = LineaDeVenta.select("""
                producto_compra_id = %d AND
                albaran_salida_id IN (SELECT albaran_salida.id
                                      FROM albaran_salida
                                      WHERE albaran_salida.fecha <= '%s'
                                      AND albaran_salida.fecha >= '%s'
                                      AND almacen_origen_id = %d)
                """ % (self.id, sqlfechafin, sqlfechaini, almacen.id))
        return entradas, salidas_consumos, salidas_albaranes

    def get_entradas_y_salidas_entre(self, fechaini, fechafin = None,
                                     almacen = None):
        """
        Devuelve la cantidad total (entradas - salidas) de entradas y salidas
        del producto entre las fechas indicadas, AMBAS INCLUIDAS.
        Si la fecha final es None, no establece límite superior en la consulta.
        """
        # DONE: OJO: No sé si al final se llegó a algo respecto a los
        #            abonos de proveedores.
        #            Tengo que mirarlo. Si fue así, AQUÍ NO SE TIENE EN CUENTA.
        #       Los abonos de proveedores finalmente se meten como facturas
        #       en negativo.
        qin = 0.0     # Quantity in
        qout = 0.0    # Quantity out
        # NOTA: No tiene en cuenta los partes por turno, solo por fecha
        # "absoluta" (o días naturales, si después de 12 de la noche, es del
        # día siguiente).
        sqlfechaini = fechaini.strftime("%Y-%m-%d")
        if fechafin:
            sqlfechafin = fechafin.strftime("%Y-%m-%d")
            entradas, salidas_consumos, salidas_albaranes \
                = self.__get_consultas_entradas_y_salidas_entre(sqlfechaini,
                                                                sqlfechafin,
                                                                almacen)
        else:
            entradas, salidas_consumos, salidas_albaranes \
                = self.__get_consultas_entradas_y_salidas_desde(sqlfechaini,
                                                                almacen)
        if entradas.count() > 0:
            esum = entradas.sum("cantidad")
            if esum is None:
                esum = 0.0
            qin += esum
            if DEBUG:
                myprint("get_entradas_y_salidas_desde; qin:", qin)
        if salidas_consumos.count() > 0:
            esum = salidas_consumos.sum("cantidad")
            if esum is None:
                esum = 0.0
            qout += esum
            if DEBUG:
                myprint("get_entradas_y_salidas_desde; qout:", qout)
        if salidas_albaranes.count() > 0:
            esum = salidas_albaranes.sum("cantidad")
            if esum is None:
                esum = 0.0
            qout += esum
            if DEBUG:
                myprint("get_entradas_y_salidas_desde; qout:", qout)
        return qin - qout

    def _muestrear_historicos(self):
        """
        Devuelve un diccionario de existencias del producto en los días 1 y 15
        de los últimos 12 meses y las existencias actuales.
        """
        hoy = mx.DateTime.localtime()   # Hoy... que no es hoy. Dará las
                    # existencias a las 00:00 de hoy, no en tiempo real.
        if hoy.day > 15:
            ultima = mx.DateTime.DateTimeFrom(day = 15,
                                              month = hoy.month,
                                              year = hoy.year)
        else:
            ultima = mx.DateTime.DateTimeFrom(day = 1,
                                              month = hoy.month,
                                              year = hoy.year)
        primera = mx.DateTime.DateTimeFrom(day = ultima.day,
                                           month = ultima.month,
                                           year = ultima.year - 1)
        fechas = [primera, ]
        while fechas[-1] != ultima:
            if fechas[-1].month < 12:
                anno = fechas[-1].year
                mes = fechas[-1].month + 1
            else:
                anno = fechas[-1].year + 1
                mes = 1
            fechas.append(mx.DateTime.DateTimeFrom(day = 1,
                                                   month = mes,
                                                   year = anno))
            fechas.append(mx.DateTime.DateTimeFrom(day = 15,
                                                   month = mes,
                                                   year = anno))
        fechas.append(hoy)
        res = {}
        for fecha in fechas:
            res[fecha] = self.get_existencias_historico(fecha)
#            print "%s -> %s: %s" % (self.descripcion, fecha.strftime("%d/%m/%Y"), utils.float2str(res[fecha]))
#        print "          AHORA, EN TIEMPO REAL: %s" % (utils.float2str(self.existencias))
        return res

    def get_entradas(self, fechaini = None, fechafin = None):
        """
        Devuelve las entradas del producto, agrupadas por fecha y tal.
        El resultado es un diccionario tal que:
            {fecha: {'albaranes': {albaranEntrada: cantidad,... }, 'cantidad': 0}, ...}
        fechaini y fechafin, de recibirse, _deben ser_ fechas mx.DateTime.
        """
        res = {}
        if not fechaini and not fechafin:
            entradas = LineaDeCompra.select(""" producto_compra_id = %d AND
                                                albaran_entrada_id IN (SELECT albaran_entrada.id
                                                                       FROM albaran_entrada)""" % (self.id))
        elif not fechaini and fechafin:
            sqlfechafin = fechafin.strftime("%Y-%m-%d")
            entradas = LineaDeCompra.select(""" producto_compra_id = %d AND
                                                albaran_entrada_id IN (SELECT albaran_entrada.id
                                                                       FROM albaran_entrada
                                                                       WHERE albaran_entrada.fecha <= '%s') """ % (self.id, sqlfechafin))
        elif fechaini and not fechafin:
            sqlfechaini = fechaini.strftime("%Y-%m-%d")
            entradas = LineaDeCompra.select(""" producto_compra_id = %d AND
                                                albaran_entrada_id IN (SELECT albaran_entrada.id
                                                                       FROM albaran_entrada
                                                                       WHERE albaran_entrada.fecha >= '%s') """ % (self.id, sqlfechaini))
        else:
            sqlfechaini = fechaini.strftime("%Y-%m-%d")
            sqlfechafin = fechafin.strftime("%Y-%m-%d")
            entradas = LineaDeCompra.select(""" producto_compra_id = %d AND
                                                albaran_entrada_id IN (SELECT albaran_entrada.id
                                                                       FROM albaran_entrada
                                                                       WHERE albaran_entrada.fecha >= '%s'
                                                                        AND albaran_entrada.fecha <= '%s') """ % (self.id,
                                                                                                                  sqlfechaini,
                                                                                                                  sqlfechafin))
        for ldc in entradas:
            if ldc.albaranEntrada.fecha not in res:
                res[ldc.albaranEntrada.fecha] = {'albaranes': {ldc.albaranEntrada: ldc.cantidad},
                                  'cantidad': ldc.cantidad}
            else:
                if ldc.albaranEntrada not in res[ldc.albaranEntrada.fecha]['albaranes']:
                    res[ldc.albaranEntrada.fecha]['albaranes'][ldc.albaranEntrada] = ldc.cantidad
                else:
                    res[ldc.albaranEntrada.fecha]['albaranes'][ldc.albaranEntrada] += ldc.cantidad
                res[ldc.albaranEntrada.fecha]['cantidad'] += ldc.cantidad
        return res

    def get_salidas(self, fechaini = None, fechafin = None):
        """
        Devuelve las salidas del producto, agrupadas por fecha y tal.
        El resultado es un diccionario tal que:
            {fecha: {'partes': {ParteDeProduccion: cantidad, ... },
                     'albaranes': {AlbaranSalida: cantidad, ...},
                     'cantidad': 0}, ...}
        fechaini y fechafin, de recibirse, _deben ser_ fechas mx.DateTime.
        """
        res = {}
        if not fechaini and not fechafin:
            consumos = Consumo.select("""
                producto_compra_id = %d AND parte_de_produccion_id IS NOT NULL
                """ % (self.id))
            salidas = LineaDeVenta.select("""
                producto_compra_id = %d AND albaran_salida_id IS NOT NULL
                """ % (self.id))
        elif not fechaini and fechafin:
            sqlfechafin = fechafin.strftime("%Y-%m-%d")
            consumos = Consumo.select("""
                producto_compra_id = %d AND
                parte_de_produccion_id IN (
                    SELECT parte_de_produccion.id
                    FROM parte_de_produccion
                    WHERE parte_de_produccion.fecha <= '%s')
                """ % (self.id, sqlfechafin))
            salidas = LineaDeVenta.select("""
                producto_compra_id = %d AND
                albaran_salida_id IN (
                    SELECT albaran_salida.id
                    FROM albaran_salida
                    WHERE albaran_salida.fecha <= '%s')
                """ % (self.id, sqlfechafin))
        elif fechaini and not fechafin:
            sqlfechaini = fechaini.strftime("%Y-%m-%d")
            consumos = Consumo.select("""
                producto_compra_id = %d AND
                parte_de_produccion_id IN (
                    SELECT parte_de_produccion.id
                    FROM parte_de_produccion
                    WHERE parte_de_produccion.fecha >= '%s')
                """ % (self.id, sqlfechaini))
            salidas = LineaDeVenta.select("""
                producto_compra_id = %d AND
                albaran_salida_id IN (
                    SELECT albaran_salida.id
                    FROM albaran_salida
                    WHERE albaran_salida.fecha >= '%s')
                """ % (self.id, sqlfechaini))
        else:
            sqlfechaini = fechaini.strftime("%Y-%m-%d")
            sqlfechafin = fechafin.strftime("%Y-%m-%d")
            consumos = Consumo.select("""
                producto_compra_id = %d AND
                parte_de_produccion_id IN (
                    SELECT parte_de_produccion.id
                    FROM parte_de_produccion
                    WHERE parte_de_produccion.fecha >= '%s'
                      AND parte_de_produccion.fecha <= '%s')
                """ % (self.id, sqlfechaini, sqlfechafin))
            salidas = LineaDeVenta.select("""
                producto_compra_id = %d AND
                albaran_salida_id IN (SELECT albaran_salida.id
                                      FROM albaran_salida
                                      WHERE albaran_salida.fecha >= '%s'
                                      AND albaran_salida.fecha <= '%s')
                """ % (self.id, sqlfechaini, sqlfechafin))
        for consumo in consumos:
            fecha = consumo.parteDeProduccion.fecha
            parte = consumo.parteDeProduccion
            cantidad = consumo.cantidad
            if fecha not in res:
                res[fecha] = {'partes': {parte: cantidad},
                              'albaranes': {},
                              'cantidad': cantidad}
            else:
                if parte not in res[fecha]['partes']:
                    res[fecha]['partes'][parte] = cantidad
                else:
                    res[fecha]['partes'][parte] += cantidad
                res[fecha]['cantidad'] += cantidad
        for salida in salidas:
            fecha = salida.albaranSalida.fecha
            albaran = salida.albaranSalida
            cantidad = salida.cantidad
            if fecha not in res:
                res[fecha] = {'albaranes': {albaran: cantidad},
                              'partes': {},
                              'cantidad': cantidad}
            else:
                if albaran not in res[fecha]['albaranes']:
                    res[fecha]['albaranes'][albaran] = cantidad
                else:
                    res[fecha]['albaranes'][albaran] += cantidad
                res[fecha]['cantidad'] += cantidad
        return res

    def get_pendientes(self, fechainicio = None, fechafin = None):
        """
        Devuelve un diccionario de pedidos de compra y cantidad
        pendiente de recibir del producto entre las fechas indicadas.
        {pedidoCompra: {'cantidad': cantidad_pendiente,
                        'valor': cantidad_pendiente_valorada_en_euros}, ...}
        """
        if not fechainicio and not fechafin:
            pedidos = PedidoCompra.select(PedidoCompra.q.cerrado == False,
                    orderBy = sqlbuilder.func.lower(PedidoCompra.q.numpedido))
        elif fechainicio and not fechafin:
            pedidos = PedidoCompra.select(
                        AND(PedidoCompra.q.fecha >= fechainicio,
                            PedidoCompra.q.cerrado == False),
                        orderBy = "numpedido")
        elif not fechainicio and fechafin:
            pedidos = PedidoCompra.select(AND(PedidoCompra.q.fecha <= fechafin,
                                              PedidoCompra.q.cerrado == False),
                                          orderBy = "numpedido")
        else:
            pedidos=PedidoCompra.select(AND(PedidoCompra.q.fecha>=fechainicio,
                                            PedidoCompra.q.fecha <= fechafin,
                                            PedidoCompra.q.cerrado == False),
                                          orderBy = "numpedido")
        pendiente = {}
        for pedido in pedidos:
            cantidad_pendiente, valor = pedido.get_pendiente(self)
            if cantidad_pendiente > 0:
                if pedido not in pendiente:
                    pendiente[pedido] = {'cantidad': cantidad_pendiente,
                                         'valor': valor}
                else:
                    pendiente[pedido]['cantidad'] += cantidad_pendiente
                    pendiente[pedido]['valor'] += valor
        return pendiente

    def get_ultimo_precio(self):
        """
        Devuelve el precio al que se compró el producto
        en el último pedido. Si el producto no tiene
        pedidos, devuelve None.
        El precio que se tiene en cuenta es el de la línea
        de compra en sí, no el de la línea de pedido; ya que
        un producto se puede pedir a un precio y recibir
        finalmente a otro. Este último precio es el precio
        real al que se ha comprado y es el que se usará para
        valorar las existencias.
        """
        ultimo_precio = None
        consulta_ultimo_pedido = PedidoCompra.select("""
            id IN (SELECT pedido_compra_id
                   FROM linea_de_compra
                   WHERE linea_de_compra.producto_compra_id = %d)
                   ORDER BY fecha DESC """ % (self.id))
        try:
            ultimo_pedido = consulta_ultimo_pedido[0]
        except IndexError:
            ultimo_precio = None
        else:
            ultima_ldc = LineaDeCompra.select(AND(
                          LineaDeCompra.q.pedidoCompraID == ultimo_pedido.id,
                          LineaDeCompra.q.productoCompraID == self.id))[0]
            ultimo_precio = ultima_ldc.precio
        return ultimo_precio

    def get_ultimo_precio_albaran(self):
        """
        Devuelve el precio al que se compró el producto
        en el último ALBARÁN. Si el producto no tiene
        pedidos, devuelve None.
        El precio que se tiene en cuenta es el de la línea
        de compra en sí, no el de la línea de pedido; ya que
        un producto se puede pedir a un precio y recibir
        finalmente a otro. Este último precio es el precio
        real al que se ha comprado y es el que se usará para
        valorar las existencias.
        """
        ultimo_precio = None
        consulta_ultimo_albaran = AlbaranEntrada.select("""
            id IN (SELECT albaran_entrada_id
                   FROM linea_de_compra
                   WHERE linea_de_compra.producto_compra_id = %d)
            ORDER BY fecha DESC """ % (self.id))
        try:
            ultimo_albaran = consulta_ultimo_albaran[0]
        except IndexError:
            ultimo_precio = None
        else:
            ultima_ldc = LineaDeCompra.select(AND(
                LineaDeCompra.q.albaranEntradaID == ultimo_albaran.id,
                LineaDeCompra.q.productoCompraID == self.id))[0]
            ultimo_precio = ultima_ldc.precio
        return ultimo_precio

    def get_precio_medio(self, fechaini = None, fechafin = None):
        """
        Devuelve el precio medio del producto de compra
        en función de las entradas del mismo
        mediante albaranes. Devuelve None si
        no ha habido entradas.
        Si fechainicio y fechafin son None, devuelve el
        precio medio de todas las entradas. En otro caso
        usa las entradas comprendidas entre ambas fechas.
        """
        entradas = self.get_entradas(fechaini, fechafin)
        stock_entradas = 0
        valoracion_entradas = 0
        for fecha in entradas:
            for albaran in entradas[fecha]['albaranes']:
                for ldc in albaran.lineasDeCompra:
                    if ldc.productoCompra == self:
                        stock_entradas += ldc.cantidad
                        valoracion_entradas += ldc.get_subtotal()
        try:
            precio_medio = valoracion_entradas / stock_entradas
        except ZeroDivisionError:
            precio_medio = None
        return precio_medio

    def __get_ldcs_entre(self, fechaini, fechafin):
        """
        Devuelve las LDCs entre las fechas indicadas.
        """
        ldcs = []
        for ldc in self.lineasDeCompra:
            if not fechafin and not fechaini:   # Todas las LDCS.
                ldcs.append(ldc)
            else:
                fechaldc = ldc.get_fecha_albaran()
                if not fechafin and fechaini:
                    # Posteriores a fechaini
                    if fechaini <= fechaldc:
                        ldcs.append(ldc)
                elif fechafin and not fechaini:
                    # Anteriores a fechafin
                    if fechafin >= fechaldc:
                        ldcs.append(ldc)
                elif fechafin and fechaini:
                    # Entre fechaini y fechafin
                    if fechaini <= fechaldc <= fechafin:
                        ldcs.append(ldc)
        return ldcs

    def get_precio_valoracion(self, fechaini = None, fechafin = None):
        """
        Devuelve el precio con el que se valoran las
        existencias del producto de compra.
        Wrapper al método que realmente lo calcula.
        NOTA: Actualmente se usa el precio medio de las entradas
        entre dos fechas.
        """
        precio = self.precioDefecto
        if (self.fvaloracion == "Función por defecto"
            or self.fvaloracion == "Precio medio"):
            ldcs = self.__get_ldcs_entre(fechaini, fechafin)
            if ldcs != []:  # Si tiene entradas que evaluar:
                precio = self.get_precio_medio(fechaini, fechafin)
        elif self.fvaloracion == "Precio último pedido":
            precio = self.get_ultimo_precio()
        elif self.fvaloracion == "Precio última entrada en almacén":
            precio = self.get_ultimo_precio_albaran()
        elif self.fvaloracion == "Usar precio por defecto especificado":
            precio = self.precioDefecto
        else:
            precio = None
                # precio = None cuando no hay función de valoración
                # especificada o cuando la misma no ha podido devolver un
                # precio válido.
                # Acabará tomando un par de líneas más abajo el precio por
                # defecto.
        if precio == None:
            precio = self.precioDefecto
        return precio

    def get_pedidos(self, proveedor = None):
        """
        Devuelve una tupla de objetos pedido donde se haya
        pedido el producto del objeto.
        Si proveedor != None filtra la lista para devolver
        solo aquellos pedidos que se correspondan con el
        proveedor recibido.
        NOTA: Tiene en cuenta tanto las LDC (líneas ya albaraneadas
        o facturadas) como las LDPC (líneas de pedido de compra en sí).
        OJO: Ya que convierte un SelectResult a tupla antes de devolver,
        puede resultar algo lento si la lista de pedidos es grande.
        """
        consulta_sql = """ (id IN (SELECT pedido_compra_id
                                   FROM linea_de_compra
                                   WHERE producto_compra_id = %d)
                            OR id IN (SELECT pedido_compra_id
                                      FROM linea_de_pedido_de_compra
                                      WHERE producto_compra_id = %d))
                       """ % (self.id, self.id)
        if proveedor != None:
            consulta_sql += " AND proveedor_id = %d " % (proveedor.id)
        pedidos = PedidoCompra.select(consulta_sql)
        return tuple(pedidos)

    def get_albaranes(self, proveedor = None):
        """
        Devuelve los albaranes relacionados con el producto de compra.
        Si proveedor no es None los filtra para devolver solo los de
        ese proveedor.
        """
        consulta_sql=""" (id IN (SELECT albaran_entrada_id
                                 FROM linea_de_compra
                                 WHERE producto_compra_id = %d)) """%(self.id)
        if proveedor != None:
            consulta_sql += " AND proveedor_id = %d " % (proveedor.id)
        albaranes = AlbaranEntrada.select(consulta_sql)
        return tuple(albaranes)

    def get_facturas(self, proveedor = None):
        """
        Devuelve las facturas relacionadas con el producto de compra.
        Si el proveedor no es None, los filtra para devolver solo los
        ese proveedor.
        """
        consulta_sql=""" (id IN (SELECT factura_compra_id
                                 FROM linea_de_compra
                                 WHERE producto_compra_id = %d)) """%(self.id)
        if proveedor != None:
            consulta_sql += " AND proveedor_id = %d " % (proveedor.id)
        facturas = FacturaCompra.select(consulta_sql)
        return tuple(facturas)

    def get_proveedores(self):
        """
        Devuelve una lista de proveedores que sirven el
        producto actual a partir de facturas, albaranes y
        pedidos sin orden concreto. No incluye específicamente al proveedor
        por defecto (a no ser que se le haya hecho algún pedido o algo, claro).
        OJO: Puede llegar a resultar MUY lento.
        """
        proveedores = []
        for pedido in self.get_pedidos():
            try:
                pedido_tiene_proveedor = pedido.proveedor != None
            except SQLObjectNotFound:
                pedido_tiene_proveedor = False
                pedido.proveedor = None
                pedido.syncUpdate()
            if (pedido_tiene_proveedor
                and pedido.proveedor not in proveedores):
                proveedores.append(pedido.proveedor)
        for albaran in self.get_albaranes():
            try:
                albaran_tiene_proveedor = albaran.proveedor != None
            except SQLObjectNotFound:
                albaran_tiene_proveedor = False
                albaran.proveedor = None
                albaran.syncUpdate()
            if (albaran_tiene_proveedor
                and albaran.proveedor not in proveedores):
                proveedores.append(albaran.proveedor)
        for factura in self.get_facturas():
            try:
                factura_tiene_proveedor = factura.proveedor != None
            except SQLObjectNotFound:
                factura_tiene_proveedor = False
                factura.proveedor = None
                factura.syncUpdate()
            if (factura_tiene_proveedor
                and factura.proveedor not in proveedores):
                proveedores.append(factura.proveedor)
        return proveedores

    proveedores = property(get_proveedores, doc = "Proveedores relacionados "\
          "con el producto de compra mediante pedidos, albaranes o facturas.")

    def get_stock(self, almacen = None):
        """
        Devuelve las existencias.
        Por compatibilidad con ProductoVenta.
        """
        #return self.existencias
        return self.get_existencias(almacen)

    def get_str_unidad_de_venta(self):
        return self.unidad

    def get_str_stock(self):
        """
        Devuelve las existencias como cadena con su unidad.
        """
        return (utils.float2str(self.get_stock(), autodec = True)
                + " " + self.get_str_unidad_de_venta())

    def get_existencias(self, almacen = None):
        """
        Devuelve las existencias.
        Por compatibilidad con ProductoVenta.
        Si almacen es None, devuelve el total.
        Si no, devuelve las existencias del almacén en concreto.
        OJO: No se asegura aquí que las existencias totales coincidan con
        la suma de los almacenes.
        """
        # TODO: Para hacerlo compatible con los productos de venta, dejar
        # que reciba una fecha y llamar a get_existencias_historico.
        if not almacen:
            res = self.existencias
        else:
            try:
                res = [sa.existencias
                       for sa in self.stocksAlmacen
                       if sa.almacen == almacen][0]
            except IndexError:
                res = 0
        return res

    def get_str_existencias(self):
        """
        Devuelve las existencias como cadena con su unidad.
        """
        return utils.float2str(self.get_existencias(), autodec = True) + " " + self.unidad

    def calcular_kilos(self):
        """
        Intenta determinar el peso en kg del producto buscando la palabra
        "kilo", "litro" o "l." "l\0" y devolviendo el número justo a su
        izquierda.
        Si no se puede determinar, devuelve None.
        OJO: Esta función puede quedar en desuso o ser sustituida por una
        equivalente con el peso real. Por el momento el peso puede no ser
        preciso (no hay propiedad en los objetos producto de compra que
        indique el peso real y además se asume que la densidad de todos los
        productos es la del agua 1 kg/l).
        """
        s = self.descripcion
        s = s.upper()
        divisor = 1.0
        if "K." in s:
            pos = s.rindex("K.")
        elif "KILO" in s:
            pos = s.rindex("KILO")
        elif "ML." in s:
            pos = s.rindex("ML.")
            divisor = 1000.0
        elif "ML," in s:
            pos = s.rindex("ML,")
            divisor = 1000.0
        elif s.strip().endswith("ML"):
            pos = s.rindex("ML")
            divisor = 1000.0
        elif "ML " in s:
            pos = s.rindex("ML ")
            divisor = 1000.0
        elif "L." in s:
            pos = s.rindex("L.")
        elif "L," in s:
            pos = s.rindex("L,")
        elif s.strip().endswith("L"):
            pos = s.rindex("L")
        elif "GR " in s:
            pos = s.rindex("GR ")
            divisor = 1000.0
        elif s.strip().endswith("GR"):
            pos = s.rindex("GR")
            divisor = 1000.0
        elif "GR." in s:
            pos = s.rindex("GR.")
            divisor = 1000.0
        else:
            pos = None
        res = None
        if pos:
            s = s[pos-1::-1]
            try:
                s = s.split()[0]
            except IndexError:
                pass
            nums = ""
            for l in s:
                if l in ("0123456789.,"):
                    nums += l
            try:
                res = utils._float(nums[::-1])
            except (ValueError, TypeError):
                res = None
            else:
                res /= divisor
        return res

    def add_existencias(self,
                        cantidad,
                        almacen = None,
                        actualizar_global = False):
        """
        Incrementa las existencias del producto en el almacén «almacén» en la
        cantidad recibida.
        Si no se recibe almacén se usa el almacén principal por defecto.
        Si actualizar_global es True cambia también las existencias totales
        del producto.
        """
        if isinstance(almacen, int):
            try:
                almacen = Almacen.get(almacen)
            except:
                raise ValueError, "Si almacen es un número, debe coincidir"\
                                  " con un ID de la base de datos."
        if almacen == None:
            almacen = Almacen.get_almacen_principal()
        try:
            rstock = StockAlmacen.select(AND(
                StockAlmacen.q.productoCompraID == self.id,
                StockAlmacen.q.almacenID == almacen.id))[0]
        except IndexError:
            rstock = StockAlmacen(productoCompra = self,
                                  almacen = almacen,
                                  existencias = 0)
        rstock.sync()
        rstock.existencias += cantidad
        rstock.syncUpdate()
        if actualizar_global:
            self.sync()
            self.existencias += cantidad
            self.syncUpdate()

    def _unificar_historiales(self, d):
        """
        Une los históricos del objeto y d de forma coherente.
        1.- Crear una lista ordenada de fechas de ambos historiales.
        2.- Anotar existencias diferenciales de ambos.
        3.- Sumar las listas en el registro «o»
        4.- Eliminar los historialExistencias de «d».
        """
        fechas = []
        fechas1 = {}
        fechas2 = {}
        for h1 in self.historialesExistenciasCompra:
            fecha = h1.fecha
            if fecha not in fechas:
                fechas.append(fecha)
            try:
                fechas1[fecha][0] += h1.cantidad
                fechas1[fecha][1] += h1.observaciones
            except (KeyError, IndexError):
                fechas1[fecha] = [h1.cantidad, h1.observaciones]
        for h2 in d.historialesExistenciasCompra:
            fecha = h2.fecha
            if fecha not in fechas:
                fechas.append(fecha)
            try:
                fechas2[fecha][0] += h2.cantidad
                fechas2[fecha][1] += h2.observaciones
            except (KeyError, IndexError):
                fechas2[fecha] = [h2.cantidad, h2.observaciones]
        # Guardo las diferencias en lugar de cantidades absolutas.
        for f in (fechas1, fechas2):
            fechasdic = f.keys()
            fechasdic.sort()
            for i in range(1, len(fechasdic)):
                fecha = fechasdic[i]
                base = fechasdic[i-1]
                f[fecha][0] = f[fecha][0] - f[base][0]
        # Unifico en un nuevo diccionario:
        final = {}
        fechas.sort()
        for fecha in fechas:
            try:
                c1, o1 = fechas1[fecha]
            except (KeyError, IndexError):
                c1 = 0
                o1 = ""
            try:
                c2, o2 = fechas2[fecha]
            except (KeyError, IndexError):
                c2 = 0
                o2 = ""
            try:
                fecha_base = fechas[fechas.index(fecha)-1]
                base = final[fecha_base][0]
            except (KeyError, IndexError):
                base = 0
            final[fecha] = [base + c1 + c2,
                            o1 + " " + o2 +
                            " Registro unificado por duplicidad de producto."]
        # Elimino los registros existentes y creo los nuevos:
        for h in self.historialesExistenciasCompra + d.historialesExistenciasCompra:
            h.destroySelf()
        for fecha in final:
            h = HistorialExistenciasCompra(productoCompra = self,
                                           cantidad = final[fecha][0],
                                           observaciones = final[fecha][1],
                                           fecha = fecha)

    def unificar_productos_compra(bueno, malos):
        """
        Unifica dos o más productos de compra. Pasa las existencias totales y
        por almacén al producto "bueno" sumando las existencias de éste y de
        todos los de la lista "malos". También combina los históricos de
        existencias sumándolos.
        Acaba eliminando todos los productos de la lista "malos".
        """
        # Recuento existencias
        existencias = {}
        for a in Almacen.select():
            existencias[a] = 0.0
        for sa in bueno.stocksAlmacen:
            existencias[a] += sa.existencias
            sa.destroy()
        for malo in malos:
            for sa in malo.stocksAlmacen:
                if malo.controlExistencias:
                    existencias[a] += sa.existencias
                sa.destroy()
        if DEBUG:
            myprint("DEBUG: pclases.ProductoCompra.unificar_productos_compra ->"\
                  " Existencias:", existencias)
        # Unifico historiales y aprovecho para eliminar tarifas de malos. No
        # quiero que se dupliquen precios en «bueno».
        for malo in malos:
            if DEBUG:
                myprint("DEBUG: pclases.ProductoCompra.unificar_productos_"\
                      "compra -> Unificando historiales...")
            bueno._unificar_historiales(malo)
            for precio in malo.precios:     # Respeto la tarifa del bueno.
                precio.destroy()
        # Unifico resto de registros dependientes (pedidos, etc.)
        unificar(bueno, malos, borrar_despues = True)
        # Actualizo existencias.
        for a in existencias:
            if DEBUG:
                myprint("DEBUG: pclases.ProductoCompra.unificar_productos_"\
                      "compra ->"\
                      "\n  %d registros stockAlmacen."\
                      "\n  Creando nuevo registro de %s para %s..." % (
                        len(bueno.stocksAlmacen), existencias[a], a.nombre))
            StockAlmacen(productoCompra = bueno,
                         almacen = a,
                         existencias = existencias [a])
            if DEBUG:
                myprint("\n  %d registros stockAlmacen"%len(bueno.stocksAlmacen))
        bueno.existencias = sum([sa.existencias for sa in bueno.stocksAlmacen])
        bueno.syncUpdate()

    unificar_productos_compra = staticmethod(unificar_productos_compra)

cont, tiempo = print_verbose(cont, total, tiempo)

class CamposEspecificosBala(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    productosVenta = MultipleJoin('ProductoVenta')
    #----------------------- tipoMaterialBalaID = ForeignKey('TipoMaterialBala')
    #--------------------------- modeloEtiquetaID = ForeignKey("ModeloEtiqueta")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class AlbaranEntrada(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #------------------------------------- proveedorID = ForeignKey('Proveedor')
    lineasDeCompra = MultipleJoin('LineaDeCompra')
    documentos = MultipleJoin('Documento')
    #----------------------------------------- almacenID = ForeignKey("Almacen",
    #----------------------- default=Almacen.get_almacen_principal_id_or_none())
    #------------- transportistaID = ForeignKey('Transportista', default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        return "Albarán %s (%s) del proveedor %s." % (self.numalbaran,
                utils.str_fecha(self.fecha),
                self.proveedor and self.proveedor.nombre or "")

    def contar_lineas_facturadas(self):
        """
        Devuelve el número de líneas de venta del albarán
        que ya han sido facturadas.
        """
        lineas_facturadas = [ldc for ldc in self.lineasDeCompra
                             if ldc.facturaCompraID]
            # Acceder a ...ID es más rápido que acceder al objeto en sí,
            # aunque sea solo para comparar si no es None.
        return len(lineas_facturadas)

    def contar_lineas_no_facturadas(self):
        """
        Devuelve el número de líneas de venta del albarán
        que todavía han sido facturadas.
        """
        lineas_no_facturadas = [ldc for ldc in self.lineasDeCompra
                                if not ldc.facturaCompraID]
            # Acceder a ...ID es más rápido que acceder al objeto en sí,
            # aunque sea solo para comparar si no es None.
        return len(lineas_no_facturadas)

    def get_facturas(self):
        """
        Devuelve una lista de objetos factura relacionados con el albarán.
        """
        facturas = []
        for ldc in self.lineasDeCompra:
            if (ldc.facturaCompraID != None
                    and ldc.facturaCompra not in facturas):
                facturas.append(ldc.facturaCompra)
        return facturas

    def get_pedidos(self):
        """
        Devuelve una lista de pedidos de compra relacionados con el albarán.
        """
        pedidos = []
        for ldc in self.lineasDeCompra:
            if ldc.pedidoCompraID != None and ldc.pedidoCompra not in pedidos:
                pedidos.append(ldc.pedidoCompra)
        return pedidos

    facturasCompra = property(get_facturas,
        doc = "Facturas relacionadas con el albarán de entrda.")
    pedidosCompra = property(get_pedidos,
        doc = 'Lista de objetos "pedido de compra" servidos en este albarán')


cont, tiempo = print_verbose(cont, total, tiempo)

class Articulo(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------------- balaID = ForeignKey('Bala')
    #--------------------------------------------- rolloID = ForeignKey('Rollo')
    #----------------------------- productoVentaID = ForeignKey('ProductoVenta')
    #----------------------------- albaranSalidaID = ForeignKey('AlbaranSalida')
    #--------------------- parteDeProduccionID = ForeignKey('ParteDeProduccion')
    lineasDeDevolucion = MultipleJoin('LineaDeDevolucion')
    #--------------------------- bigbagID = ForeignKey('Bigbag', default = None)
    #--------- rolloDefectuosoID = ForeignKey('RolloDefectuoso', default = None)
    #--------------------- balaCableID = ForeignKey("BalaCable", default = None)
    #--------------------------- rolloCID = ForeignKey("RolloC", default = None)
    #------------ almacenID = ForeignKey("Almacen")   # NO default = None porque
        # precísamente cuando se crea (fabrica) es cuando por cojones debe
        # estar en un almacén. Si después se vende, entonces sí será None.
    lineasDeMovimiento = MultipleJoin("LineaDeMovimiento")
    #---------------------------- #bolsaID = ForeignKey('Bolsa', default = None)
    #------------------------------- cajaID = ForeignKey('Caja', default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        """
        Devuelve una cadena con el PUID del artículo, el código de
        trazabilidad, el producto, dimensiones y el historial.
        """
        cad = self.get_puid()
        cad += " - %s (%s): %s %s\n" % (self.get_codigo_interno(),
            self.productoVenta.nombre,
            utils.float2str(self.get_cantidad(), autodec = True),
            self.productoVenta.get_str_unidad_de_venta())
        cad += "Peso: %s kg\n" % (utils.float2str(self.get_peso()))
        cad += "Peso sin embalaje: %s kg\n" % (
            utils.float2str(self.get_peso_sin()))
        try:
            largo = utils.float2str(self.get_largo(), autodec = True)
        except (ValueError, TypeError):  # Objeto no tiene largo.
            largo = "N/A"   # No aplicable.
        cad += "Largo: %s m\n" % largo
        try:
            ancho = utils.float2str(self.get_ancho(), autodec = True)
        except (ValueError, TypeError): # Objeto no tiene ancho.
            ancho = "N/A"
        cad += "Ancho: %s m\n" % ancho
        try:
            superficie = utils.float2str(self.get_superficie(),
                                         autodec = True)
        except (ValueError, TypeError):
            superficie = "N/A"
        cad += "Área: %s m²\n" % (superficie)
        cad += "Analizado: %s\n" % (self.get_analizado() and "Sí" or "No")
        cad += "Fecha y hora de alta: %s\n" % (
            utils.str_fechahora(self.fechahora))
        cad += "Fecha de fabricación: %s\n" % (
            utils.str_fecha(self.get_fecha_fabricacion()))
        cad += "Historial de trazabilidad:\n"
        for fecha, objeto, almacen in self.get_historial_trazabilidad():
            cad += "  * %s: %s. %s\n" % (
                utils.str_fecha(fecha),
                objeto and objeto.get_info() or "",
                almacen and "Almacén destino: %s" % almacen.nombre or "")

        return cad


    @staticmethod
    def get_articulo(codigo):
        """
        Devuelve el objeto artículo correspondiente al código recibido o
        None si no se encuentra.
        """
        mapping = {PREFIJO_ROLLO: Rollo,
                   PREFIJO_BALA: Bala,
                   PREFIJO_BIGBAG: Bigbag,
                   PREFIJO_PALE: Pale,
                   PREFIJO_CAJA: Caja,
                   PREFIJO_BALACABLE: BalaCable,
                   PREFIJO_ROLLOC: RolloC,
                   PREFIJO_ROLLODEFECTUOSO: RolloDefectuoso}
        objeto = None
        for prefijo in mapping:
            if codigo.startswith(prefijo):
                clase_pclases = mapping[prefijo]
                try:
                    objeto = clase_pclases.selectBy(codigo=codigo)[0]
                except IndexError:
                    objeto = None
                else:
                    objeto = objeto.articulo
                    break
        return objeto

    def es_clase_a(self):
        """
        Devuelve True si el artículo es de clase A.
        Un artículo es de clase A cuando no es de clase B ni C. Así de simple.
        """
        return not self.es_clase_b() and not self.es_clase_c()

    def es_clase_b(self):
        """
        Devuelve True si el artículo es de clase B. Si es de clase A devuelve
        False. Si es de clase "C" (rollos C) o no tienen clase por no ser
        ni siquiera un producto concreto -esto es matizable, pero para
        entendernos- como las balas de cable. Devuelve None.
        El valor por defecto para tipos de artículo no contemplado es False.
        """
        b = False
        if self.rolloID:
            b = self.rollo.claseB
        elif self.balaID:
            b = self.bala.claseb
        elif self.bigbagID:
            b = self.bigbag.claseb
        elif self.rolloDefectuosoID:
            b = True    # Los rollos defectuosos siempre son B.
        elif self.balaCableID:
            b = None    # Las balas de cable y los rollos C no son ni A ni B,
                        # son simplemente desechos que hay que embalarlos de
                        # alguna manera. Pero no son productos B siquiera.
        elif self.rolloCID:
            b = None
        elif self.cajaID:
            b = self.caja.claseb
        return b

    def es_clase_c(self):
        """
        Devuelve True si el artículo es de clase C.
        Un artículo es de clase C si pertenece a un producto de clase C:
        rollos_C y balas de cable.
        """
        return self.rolloCID or self.balaCableID

    def get_str_calidad(self):
        """
        Devuelve la calidad del artículo como un carácter: A, B o C.
        """
        if self.es_clase_a():
            return "A"
        elif self.es_clase_b():
            return "B"
        elif self.es_clase_c():
            return "C"
        else:
            raise ValueError, "El artículo %d no es clase A, B ni C." % self.id

    def get_ldv(self, albaran):
        """
        Devuelve la LDV que corresponde al artículo y al
        albarán recibido.
        Para que el algoritmo sea determinista, ordena todos
        los artículos y las LDVs del mismo producto (el producto
        del artículo, también) de venta por ID. Después
        distribuye los artículos en las LDV hasta completar
        la cantidad de cada una de ellas. La única LDV que
        puede quedar con más cantidad asignada -mayor estricto-
        en artículos que la cantidad de la propia LDV será
        la última.
        Finalmente devuelve la LDV a la que ha quedado asignado
        el artículo actual.
        Devuelve None si no se encontró LDV en el albarán para
        el artículo -algo que NO debería ocurrir, por otra parte-.
        NOTA: Usa el método "agrupar_articulos" de la clase
        AlbaranSalida. Si no se quiere expresamente encontrar
        la LDV de este único artículo, es preferible llamar
        al método del albarán para reducir coste computacional.
        """
        res = None
        dic_articulos = albaran.agrupar_articulos()
        for idldv in dic_articulos:
            if self in dic_articulos[idldv]['articulos']:
                res = LineaDeVenta.get(idldv)
                break
        return res

    def get_partida(self):
        """
        Devuelve la partida a la que pertenece el artículo o None
        si no es un producto agrupable en partidas.
        """
        res = None
        if self.rolloID != None:
            res = self.rollo.partida
        elif self.rolloDefectuosoID != None:
            res = self.rolloDefectuoso.partida
        return res

    def set_partida(self, partida):
        """
        Instancia la partida a la que pertenece el artículo
        a la recibida si el artículo es un rollo o un rollo
        defectuoso. Si es bala o bigbag, no hace nada.
        Si "partida" no es una Partida, lanza un TypeError.
        """
        if not isinstance(partida, Partida):
            raise TypeError, "pclases::Articulo::set_partida -> La partida debe ser un objeto Partida de pclases."
        if self.rolloID != None:
            self.rollo.partida = partida
        elif self.rolloDefectuosoID != None:
            self.rolloDefectuoso.partida = partida

    def get_lote(self):
        """
        Devuelve la lote a la que pertenece el artículo o None
        si no es un producto agrupable en lotes.
        """
        if self.balaID != None:
            return self.bala.lote
        return None

    def get_loteCem(self):
        """
        Devuelve la lote de fibra de cemento a la que pertenece el artículo o None
        si no es un producto agrupable en lotes de fibra de cemento.
        """
        if self.bigbagID != None:
            return self.bigbag.loteCem
        return None

    def get_partidaCem(self):
        """
        Devuelve la partida de cemento relacionada con el artículo en caso de
        que éste sea una caja de bolsas de cemento.
        """
        try:
            return self.caja.pale.partidaCem
        except AttributeError:
            return None

    partida = property(get_partida, set_partida, doc = get_partida.__doc__)
    lote = property(get_lote, doc = get_lote.__doc__)
    loteCem = property(get_loteCem, doc = get_loteCem.__doc__)
    partidaCem = property(get_partidaCem, doc = get_partidaCem.__doc__)

    def en_almacen(self, fecha = None, almacen = None):
        """
        Devuelve True si el artículo está en el almacén.
        False en caso contrario.
        Si es rollo o bigbag, está en almacén sii albaranSalida == None.
        Si es bala, está en almacén
        sii albaranSalida == None ^ partidaCarga == None.
        Si fecha != None, devuelve si estaba en almacén en esa fecha.
        Imaginemos una bala fabricada el día 1/1/2007 a las 23:00 y vendida
        el día 1/1/2007 a las 23:01 minutos. ¿Estaba el día 1 en el almacén?
        SÍ. Hasta el día 2/1/2007 no aparecerá como que salió del almaceń. En
        caso contrario, si tomáramos como "fechahora" del albarán el
        1/1/2007 00:00, la bala se habría vendido y habría salido del
        almacén _antes_ de haberse fabricado.
        OJO: ATCHUNG y tal: Siendo estrictos, una bala no está en almacén si
        está en una partida de carga, aunque aún no se haya consumido. Sin
        embargo, para calcular el histórico (y testearlos) se buscan los
        partes de producción y a partir de ahí las partidas y partidas de
        carga. Por tanto una partida de carga sin producción implica que sus
        balas están en almacén. Pero a si esas mismas balas le haces
        un .en_almacen() te dirá que sí.
        Si la fecha de fabricación del producto es posterior a la fecha
        consultada, devuelve False, ya que no puede estar en almacén si aún
        no ha sido fabricado.
        Si almacen != None comprueba si está (o estaba en la fecha recibida)
        en ese almacén únicamente, aunque siguiendo todos los criterios
        explicados anteriormente.
        """
        # XXX: La diferencia entre activar el sync o no es un segundo por cada
        #      1.000 artículos.
        #self.sync()
        if not fecha:   # No pregunta por ninguna fecha en concreto. Chequeo
                        # por la actual.
            if almacen:
                res = self.almacen == almacen
            else:
                res = self.almacen != None
        else:   # Remember, preguntamos por una fecha concreta.
            # Sea cual sea el almacén, no estará en ninguno si se pregunta por
            # una fecha anterior a la de fabricación.
            if fecha < self.fecha_fabricacion:
                res = False
            elif fecha >= mx.DateTime.today():
                # Si pregunto por hoy, solo tengo que mirar si está en almacén
                if almacen:
                    res = self.almacen == almacen
                else:
                    res = self.almacen != None
            else:
                hist = self.get_historial_trazabilidad()
                pos = len(hist) - 1
                while pos > 0 and fecha < hist[pos][0]:
                    pos -= 1
                if fecha < hist[pos][0]:    # Aún no había "nacido".
                    almacen_en_esa_fecha = None
                else:
                    almacen_en_esa_fecha = hist[pos][2]
                if almacen:
                    res = almacen_en_esa_fecha == almacen
                else:
                    res = almacen_en_esa_fecha != None
        return res

    def get_historial_trazabilidad(self):
        """
        Devuelve una lista de tuplas (fecha, objeto, almacén).
        Cada fecha indica un movimiento del artículo en almacén. Junto a cada
        fecha está el objeto implicado en el movimiento y el almacén donde
        se encontraba en esa fecha o None si no estaba en almacén.
        """
        # La posición 0 del array siempre será la fecha de fabricación y un
        # enlace al parte de producción -si lo tuviera, que debería, pero
        # hay algunos casos en que no-.
        fechafab = self.get_fecha_fabricacion()
        res = [(fechafab,
                self.parteDeProduccion,
                Almacen.get_almacen_principal())]
        # Albaranes de salida:
        if self.albaranSalida and self.albaranSalida.almacenDestino == None:
                # Si el almacén destino es != None, es un albarán de
                # transferencia, entra en el siguiente for.
            alb = self.albaranSalida
            res.append((alb.fecha,
                        alb,
                        None))  # Sale destino al cliente. No está en ningún
                                # almacén.
        # Líneas de movimiento entre almacenes:
        for ldm in self.lineasDeMovimiento:
            fecha = ldm.albaranSalida.fecha
            alb = ldm.albaranSalida
            res.append((alb.fecha,
                        alb,
                        alb.almacenDestino))
        # Abonos:
        for ldd in self.lineasDeDevolucion:
            abono = ldd.abono
            fecha = abono.fecha
            # Primero los albaranes originales en los que estaba.
            try:
                fechalbaran = ldd.albaranSalida.fecha
            except AttributeError:
                fechalbaran = None
            res.append((fechalbaran,
                        ldd.albaranSalida,
                        None))
            # Y finalmente el abono, para que conste.
            res.append((abono.fecha,
                        abono,
                        abono.almacen))
        # Consumos de fibra
        if self.bala and self.bala.partidaCarga:
            # Se consumió en una partida de carga
            pc = self.bala.partidaCarga
            fecha = pc.fecha
            res.append((fecha,
                        pc,
                        None))
        # ... y ordenar por fecha.
        res.sort(utils.comparar_como_fechahora)
        #res.sort(lambda t1, t2: (t1[0] < t2[0] and -1)
        #                        or (t1[0] > t2[0] and 1)
        #                        or 0)
        return res

    def es_rollo(self):
        return self.rolloID != None

    def es_rollo_defectuoso(self):
        return self.rolloDefectuosoID != None

    def es_bala(self):
        return self.balaID != None

    def es_bigbag(self):
        return self.bigbagID != None

    def es_bala_cable(self):
        return self.balaCableID != None

    def es_rollo_c(self):
        return self.rolloCID != None

    def es_caja(self):
        """
        Devuelve True si es una caja de bolsas de fibra de cemento. False en
        caso contrario.
        """
        return self.cajaID != None

    es_balaCable = es_bala_cable
    es_rolloC = es_rollo_c

    def get_peso(self):
        """
        Devuelve el peso bruto (con embalaje y todo, lo que marcó en báscula)
        del artículo en función de si es rollo, bala o bigbag.
        """
        if self.es_rollo():
            #return self.rollo.peso  # <-- Peso real. No el nuevo "bruto".
            # CWT: [23/06/2016] Es lo que se va a mandar a Murano. Un paso
            # bruto ideal, que no es real de báscula.
            return self.peso_teorico + self.peso_embalaje
        if self.es_bala():
            # En el caso de las balas, el objeto bala guarda el peso
            # real menos el embalaje estimado.
            if not self.peso_real:
                return self.bala.pesobala + self.peso_embalaje
            else:
                return self.peso_real
        if self.es_bigbag():
            if not self.peso_real:
                return self.bigbag.pesobigbag  + PESO_EMBALAJE_BIGBAGS
            else:
                return self.peso_real
        if self.es_rollo_defectuoso():
            return self.rolloDefectuoso.peso # <-- Peso real. No el nuevo "bruto".
            # CWT: [23/06/2016] Es lo que se va a mandar a Murano. Un paso
            # bruto ideal, que no es real de báscula.
            return self.peso_teorico + self.peso_embalaje
        if self.es_bala_cable():
            if not self.peso_real:
                return self.balaCable.peso
            else:
                return self.peso_real
        if self.es_rollo_c():
            return self.rolloC.peso
        if self.es_caja():
            # En las cajas también se guarda el peso teórico. No hay
            # báscula ni peso real.
            return self.caja.peso + self.peso_embalaje # Campo calculado.
        return None

    def get_peso_sin(self):
        """
        Devuelve el peso neto (sin embalaje)
        del artículo en función de si es rollo,
        rollo defectuoso, bala, bala de cable o bigbag.
        """
        return self.peso_bruto - self.peso_embalaje

    def get_peso_embalaje(self):
        """
        Devuelve el peso estimado del embalaje en cada caso.
        """
        if self.es_bala():
            res = PESO_EMBALAJE_BALAS  # ~~200 gramos. Ver Zim del 14/10/2015~~
            # 865 gr. Pesado en fábrica. Redondeamos a 0.86 porque solo
            # podemos trabajar con 2 decimales contra Murano.
        elif self.es_bala_cable():
            res = self.balaCable.pesoEmbalaje
            # Tienen su propio campo en la BD, aunque no se usa. Ceropordefecto
        elif self.es_bigbag():
            res = PESO_EMBALAJE_BIGBAGS
            #res = 0.0       # Despreciable
        elif self.es_caja():
            res = PESO_EMBALAJE_CAJAS
            #res = 0.1 + 0.15   # CWT: 100 gr de bolsa y cartón. 150 gr
            # proporcionales del palé. Entre todas las cajas se supone que
            # suman el palé completo. Aunque varíe el número de cajas.
        elif self.es_rollo():
            res = self.productoVenta.camposEspecificosRollo.pesoEmbalaje
        elif self.es_rollo_c():
            res = self.rolloC.pesoEmbalaje
        elif self.es_rollo_defectuoso():
            res = self.rolloDefectuoso.pesoEmbalaje
        else:
            res = None
        return res

    def get_superficie(self):
        """
        Devuelve la superficie en metros cuadrados del
        artículo.
        Si es una bala o un bigbag, devuelve None (no
        tienen superficie definida).
        Si es un rollo C también devuelve None (se supone que tiene
        superficie pero no se tiene en cuenta).
        """
        if (self.es_bala() or self.es_bigbag() or self.es_bala_cable() or
            self.es_caja()):
            return None
        if self.es_rollo():
            return self.productoVenta.camposEspecificosRollo.metros_cuadrados
        if self.es_rollo_defectuoso():
            return self.rolloDefectuoso.ancho * self.rolloDefectuoso.metrosLineales
        return None

    def get_ancho(self):
        """
        Devuelve el ancho en metros del
        artículo.
        Si es una bala o un bigbag, devuelve None (no
        tienen superficie definida).
        Si es un rollo C también devuelve None (se supone que tiene
        ancho pero no se tiene en cuenta o varía a lo largo del rollo).
        """
        if (self.es_bala() or self.es_bigbag() or self.es_bala_cable()
            or self.es_caja()):
            return None
        if self.es_rollo():
            return self.productoVenta.camposEspecificosRollo.ancho
        if self.es_rollo_defectuoso():
            return self.rolloDefectuoso.ancho
        return None

    def get_largo(self):
        """
        Devuelve el largo en metros del
        artículo.
        Si es una bala o un bigbag, devuelve None (no
        tienen superficie definida).
        Si es un rollo C también devuelve None (se supone que tiene
        largo pero no se tiene en cuenta).
        """
        if (self.es_bala() or self.es_bigbag() or self.es_bala_cable() or
                self.es_caja()):
            return None
        if self.es_rollo():
            return self.productoVenta.camposEspecificosRollo.metrosLineales
        if self.es_rollo_defectuoso():
            return self.rolloDefectuoso.metrosLineales
        return None

    def get_cantidad(self):
        """
        Devuelve la cantidad en kilos o m2 del artículo,
        dependiendo de si es un producto vendible en kg
        (fibra) o en m² (geotextiles).
        Si es rolloC, a pesar de ser geotextil, la cantidad se
        mide en kg.
        Si es cemento embolsado se mide en gramos.
        """
        if self.es_rollo():
            cantidad = self.superficie
        elif (self.es_bala() or self.es_bigbag() or self.es_bala_cable() or
              self.es_caja()):
            cantidad = self.peso
        elif self.es_rollo_defectuoso():
            cantidad = self.superficie
        elif self.es_rolloC():
            cantidad = self.peso
        else:
            cantidad = 0
        return cantidad

    get_stock = get_cantidad    # Por compatibilidad de nomenclatura.

    def get_analizado(self):
        """
        Devuelve True si el lote o partida al que pertenece
        el artículo ha sido analizado.
        """
        if self.es_bala():
            res = self.bala.analizada()
        elif self.es_bigbag():
            res = self.bigbag.get_analizado()
        elif self.es_rollo():
            res = self.rollo.get_analizado()
        elif (self.es_rollo_defectuoso()
              or self.es_bala_cable()
              or self.es_rolloC()):
            res = False
            # Aunque pertenezca a una partida, no comparte sus características
            # al completo, así que por defecto no estará nunca "analizado".
            # Si es una bala de cable fibra para reciclar, ni se analizan ni
            # llevan lote (al menos de momento).
        elif self.es_caja():
            res = self.caja.get_analizada()
        else:
            myprint("Artículo ID %d no es bala [de cable], rollo [{defectuoso,"\
                  "C}], bigbag ni caja." % (self.id))
            res = False
        return res

    def get_peso_teorico(self):
        """
        Devuelve el peso teórico o ideal del artículo según su producto.
        """
        if self.es_bala() or self.es_bala_cable() or self.es_bigbag():
            res = None
        elif self.es_caja():
            res = self.caja.peso_teorico
        elif self.es_rollo():
            res = self.rollo.peso_teorico
        elif self.es_rollo_defectuoso():
            res = self.rolloDefectuoso.peso_teorico
        elif self.es_rollo_c():
            res = None
        else:
            res = None
        return res

    def get_peso_real(self):
        """
        El peso real del artículo, el dado por báscula siempre que sea
        aplicable.
        """
        if not self.pesoReal:  # Para los artículos creados antes del 23/06/16
            if self.es_rollo():
                res = self.rollo.peso
            elif self.es_rollo_defectuoso():
                res = self.rolloDefectuoso.peso
            elif self.es_rollo_c():
                res = self.rolloC.peso
            elif self.es_bala():
                # OJO: Caso especial.
                # El peso guardado en pclases.Bala no es el de báscula. Es el
                # de báscula **menos** el embalaje estimado, que a lo largo del
                # tiempo ha pasado de 1/1.5 kg a 200 gr y finalmente a 860 gr
                res = self.bala.pesobala + self.peso_embalaje
            elif self.es_bala_cable():
                res = self.balaCable.peso
            elif self.es_bigbag():
                res = self.bigbag.peso
            elif self.es_caja():
                # res = None   # No tienen peso real de báscula.
                # Tomamos como peso real el peso teórico de las bolsas más
                # el estimado de embalaje de la caja completa.
                res = self.caja.peso + self.peso_embalaje
            else:
                res = None
        else:  # Para los artículos posteriores, el valor de la base de datos.
            res = self.pesoReal
        return res

    superficie = property(get_superficie)
    peso_real = property(get_peso_real)
    peso = property(get_peso)
    peso_bruto = peso
    peso_sin = property(get_peso_sin, doc = get_peso_sin.__doc__)
    peso_neto = peso_sin
    peso_teorico = property(get_peso_teorico)
    peso_embalaje = property(get_peso_embalaje)
    ancho = property(get_ancho)
    largo = property(get_largo)
    cantidad = property(get_cantidad)
    analizado = property(get_analizado, doc = get_analizado.__doc__)

    def get_codigo_interno(self):
        """
        Devuelve el código interno de la bala o
        el rollo asociado al artículo.
        Un artículo nunca debe tener asociado a
        la vez un rollo y una bala, pero si esto
        ocurriera devuelve el código del rollo.
        Si el artículo no tiene bala ni rollo
        asociado devuelve None (aunque tampoco
        debería ocurrir).
        """
        if self.rollo != None:
            return self.rollo.codigo
        if self.bala != None:
            return self.bala.codigo
        if self.bigbag != None:
            return self.bigbag.codigo
        if self.rolloDefectuosoID != None:
            return self.rolloDefectuoso.codigo
        if self.balaCableID != None:
            return self.balaCable.codigo
        if self.es_rolloC():
            return self.rolloC.codigo
        if self.cajaID != None:
            return self.caja.codigo
        myprint("ERROR: pclases.py: get_codigo_interno: El artículo no tiene bala [cable], rollo [{defectuoso, C}] ni bigbag relacionado.")
        return None

    def get_fechahora(self):
        """
        Devuelve la fecha de fabricación (alta en la BD/creación del objeto)
        del rollo o de la bala.
        """
        if self.es_rollo():
            return self.rollo.fechahora
        elif self.es_bala():
            return self.bala.fechahora
        elif self.es_bigbag():
            return self.bigbag.fechahora
        elif self.es_rollo_defectuoso():
            return self.rolloDefectuoso.fechahora
        elif self.es_bala_cable():
            return self.balaCable.fechahora
        elif self.es_rollo_c():
            return self.rolloC.fechahora
        elif self.es_caja():
            return self.caja.fechahora
        else:
            # ¿Artículo que no es ni bala, ni bigbag ni rollo? Devuelvo None. NO DEBERÍA PASAR.
            myprint("ERROR: pclases.py: get_fechahora: ¡Artículo no es ni bala "\
                  "[cable], ni bigbag ni rollo [{defectuoso, C}] ni caja de "\
                  "bolsas de fibra de cemento!")
            return None

    def set_fechahora(self, fechahora):
        """
        Devuelve la fecha de fabricación del rollo o de la bala.
        """
        if self.es_rollo():
            self.rollo.fechahora = fechahora
        elif self.es_bala():
            self.bala.fechahora = fechahora
        elif self.es_bigbag():
            self.bigbag.fechahora = fechahora
        elif self.es_rollo_defectuoso():
            self.rolloDefectuoso.fechahora = fechahora
        elif self.es_bala_cable():
            self.balaCable.fechahora = fechahora
        elif self.es_rolloC():
            self.rolloC.fechahora = fechahora
        elif self.es_caja():
            self.bolsa.fechahora = fechahora
        else:
            # ¿Artículo que no es ni bala, ni bigbag ni rollo? Devuelvo None. NO DEBERÍA PASAR.
            myprint("ERROR: pclases.py: get_fechahora: ¡Artículo no es ni bala "\
                  "[cable], ni bigbag ni rollo [{defectuoso,C}] ni caja de "\
                  "bolsas de fibra de cemento!")

    def get_fecha_fabricacion(self):
        """
        Devuelve la fecha absoluta (sin horas) de fabricación del artículo.
        Será la del parte de producción, si lo tiene, o la de la
        bala/rollo/bigbag si no.
        """
        if self.parteDeProduccionID:
            return self.parteDeProduccion.fecha
        return utils.abs_mxfecha(self.fechahora)

    codigo_interno = property(get_codigo_interno)
    codigo = codigo_interno
    fechahora = property(get_fechahora, set_fechahora)
    fecha_fabricacion = property(get_fecha_fabricacion)

    def es_de_baja_calidad(self):
        """
        Devuelve True si es un rollo defectuoso, un rollo marcado como
        rollob (en la práctica en desuso), una bala o una bala de cable
        marcada como B (si lleva plástico el cable de fibra, por ejemplo),
        un bigbag de fibra de cemento marcado como claseb o un rollo «C»,
        que no son aptos para consumo por llevar largos, anchos y grosores
        heterogéneos.
        Devuelve None si ocurrió un error.
        """
        if self.es_rollo():
            return self.rollo.rollob
        elif self.es_bala():
            return self.bala.claseb
        elif self.es_bala_cable():
            return self.balaCable.claseb
        elif self.es_bigbag():
            return self.bigbag.claseb
        elif self.es_rollo_defectuoso() or self.es_rolloC():
            return True
        elif self.es_caja():
            return self.caja.claseb
                # Si la BD dice que no es clase B, no lo será aunque no
                # haya suficientes bolsas por caja.
        else:
            # ¿Artículo que no es ni bala, ni bigbag ni rollo? Devuelvo None.
            # NO DEBERÍA PASAR.
            myprint("ERROR: pclases.py: es_de_baja_calidad: ¡Artículo no es ni "\
                  "bala [cable], ni bigbag ni rollo [{defectuoso,C}] ni caja!")
            return None

    def check_abono(self):
        """
        Devuelve True si el artículo está correctamente abonado, o no abonado.
        Devuelve False si incumple esa condición estando a la vez en un
        albarán de entrada de abono y en el mismo albarán de salida devuelto.
        """
        albaranes_salida_devueltos = []
        for ldd in self.lineasDeDevolucion:
            if ldd.albaranSalida != None and ldd.albaranDeEntradaDeAbono != None and ldd.albaranSalida not in albaranes_salida_devueltos:
                albaranes_salida_devueltos.append(ldd.albaranSalida)
        # En la lista no entra None, así que si albaranSalida es None devuelve True; y si no lo es, devuelve True si no está en la lista.
        return self.albaranSalida not in albaranes_salida_devueltos

    def mover_entre_almacenes(self, origen, destino, albaran):
        """
        Mueve un artículo entre dos almacenes, de «origen» a «destino»,
        creando la línea de movimiento correspondiente y chequeando que
        esté en el almacén origen antes de llevarlo al destino.
        Es necesario recibir el albarán donde se va a producir el movimiento.
        Devuelve la línea de movimiento o None si no se pudo transferir.
        """
        # PLAN: A ver. Aquí la transferencia es instantánea, pero en
        # "el mundo real" (TM) la mercancía estará durante un tiempo en
        # el camión, tiempo en el que no son existencias ni de uno ni de
        # otro almacén.
        if self.almacen != origen:
            linea_de_movimiento = None
        else:
            linea_de_movimiento = LineaDeMovimiento(albaranSalida = albaran,
                                                    articulo = self)
            self.almacen = destino
            self.syncUpdate()
        return linea_de_movimiento

    def anular_movimiento(self, origen, destino, albaran):
        """
        Anula la línea de movimiento y devuelve el artículo al almacén
        origen.
        Devuelve 0 si se hizo con éxito la operación. 1 si el objeto ya no
        estaba en el almacén del que se intenta extraer y 2 si nunca ha
        existido el traslado de mercancía entre los dos almacenes
        recibidos y el albarán especificado.
        """
        if self.almacen != destino:
            res = 1
        else:
            try:
                linea_de_movimiento = LineaDeMovimiento.select(AND(
                    LineaDeMovimiento.q.albaranSalidaID == albaran.id,
                    LineaDeMovimiento.q.articuloID == self.id))[0]
            except IndexError:
                res = 2
            else:
                linea_de_movimiento.destroy()
                self.almacen = origen
                self.syncUpdate()
                res = 0
        return res

    def calcular_tiempo_teorico(self, solo_clase_a = True):
        """
        Devuelve el tiempo en horas en que se debería haber producido el
        artículo según la producción estándar de la ficha del producto que sea
        y el peso teórico que debería haber tenido, NO EL REAL QUE HA DADO.
        En el caso de la fibra, que no tiene peso teórico, se usa el peso
        que haya dado sin embalaje entre la producción estándar de la ficha,
        dando el tiempo teórico que se debería haber tardado.
        Si solo_clase_a es True, el tiempo teórico solo se calculará si
        el artículo es de clase A. En otro caso calculará el tiempo teórico
        aunque sea clase B (que debería ser igual pero en las consultas
        --CWT-- no debe tenerse en cuenta) o C (que de momento no tienen
        tiempo teórico porque no tienen un ancho y gramaje constantes o
        son de tan baja calidad que no debe tenerse en cuenta bajo ningún
        concepto).
        """
        if self.es_clase_a() or not solo_clase_a:
            vel = self.productoVenta.prodestandar
            try:
                # XXX: CWT
                peso = peso_teorico = self.productoVenta.get_peso_teorico()
            except ValueError:  # No tiene peso teórico. Es bala o algo.
                peso = peso_sin = self.peso_sin
            try:
                tiempo = peso / vel
            except ZeroDivisionError:
                tiempo = 0.0
        else:   # CWT: Si es B o C, el tiempo teórico es 0 porque no debe
                # contar para las consultas de productividad.
            tiempo = 0.0
        return tiempo

    #def get_peso_teorico(self):
    #    """
    #    Devuelve el peso teórico del artículo según la ficha del producto.
    #    """
    #    res = None
    #    for link in ("bala", "balaCable", "rollo", "rolloDefectuoso", "rolloC",
    #                 "bigbag", "caja"):
    #        try:
    #            linked = getattr(self, link)
    #            if linked == None:
    #                raise AttributeError
    #        except AttributeError:
    #            continue
    #        else:
    #            try:
    #                res = linked.get_peso_teorico()
    #            except AttributeError:
    #                res = None # Este tipo de producto no lo tiene definido.
    #            break
    #    return res

    def calcular_tiempo_fabricacion(self):
        """
        Calcula el tiempo transcurrido entre el artículo y el siguiente de
        la misma serie. Si todavía no se ha fabricado el siguiente devuelve
        None.
        """
        # FIXME: Para las cajas hay que afinar más y buscar el tiempo entre
        # palé y palé, ya que todas las cajas de un mismo palé se hacen con
        # la misma fecha y hora.
        for tipo, atributo in (("bala",      "numbala"),
                               ("balaCable", "numbala"),
                               ("rollo",     "numrollo"),
                               ("rolloC",    "numrollo"),
                               ("caja",      "numcaja"),
                               ("bigbag",    "numbigbag")):
            try:
                mi_codigo = getattr(getattr(self, tipo), atributo)
            except AttributeError:
                mi_codigo = None
            else:
                break
        if mi_codigo:
            try:
                sig = eval(tipo.capitalize()).select(
                    getattr(getattr(eval(tipo.capitalize()), "q"), atributo)
                        > mi_codigo,
                    orderBy = atributo,
                    limit = 1
                    )[0]
            except IndexError:
                res = None
            else:
                res = sig.fechahora - self.fechahora
                # TODO: De alguna forma habrá que controlar que el siguiente
                # rollo o lo que sea se fabricó justo después, porque si no:
                # 1.- Si lo siguiente es una incidencia, el tiempo sería hasta
                #     la siguiente incidencia.
                # 2.- Si hay una parada de fin de semana o algo, no debería
                #     devolver que se ha tardado dos días en hacer el rollo.
                #     ¿Debería fijarme en el tiempo de fin del parte?
        else:
            res = None
        return res

cont, tiempo = print_verbose(cont, total, tiempo)

class PedidoVenta(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- clienteID = ForeignKey('Cliente')
    lineasDeVenta = MultipleJoin('LineaDeVenta')
    lineasDePedido = MultipleJoin('LineaDePedido')
    #--------------------------- tarifaID = ForeignKey('Tarifa', default = None)
    servicios = MultipleJoin('Servicio')
    documentos = MultipleJoin('Documento')
    #--------------------- comercialID = ForeignKey("Comercial", default = None)
    #------------------------------- obraID = ForeignKey('Obra', default = None)
    #----------------- formaDePagoID = ForeignKey("FormaDePago", default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        if self.cliente:
            cliente = self.cliente.nombre
        else:
            cliente = "sin cliente"
        if self.cerrado:
            abierto = "Cerrado"
        else:
            abierto = "Abierto"
        if self.bloqueado:
            bloqueado = "bloqueado"
        else:
            bloqueado = "no bloqueado"
        if self.validado:
            validado = "validado"
        else:
            validado = "no validado"
        return "Pedido %s (%s) de %s. %s, %s y %s." % (self.numpedido,
                                                utils.str_fecha(self.fecha),
                                                cliente,
                                                abierto,
                                                bloqueado,
                                                validado)

    def get_str_estado(self):
        """
        Devuelve una cadena de texto con el estado del pedido y el motivo,
        en su caso, de la no validación automática.
        """
        txtestado = None
        estado_validacion = self.get_estado_validacion()
        if estado_validacion == VALIDABLE:
            txtestado = "Validado"
            if self.usuario:
                txtestado += " (%s)" % self.usuario.usuario
        elif estado_validacion == NO_VALIDABLE:
            txtestado = "Necesita validación manual: "\
                        "Validación cancelada por el usuario."
        elif estado_validacion == PLAZO_EXCESIVO:
            txtestado = "Necesita validación manual: "\
                        "El plazo de la forma de pago es excesivo."
        elif estado_validacion == SIN_FORMA_DE_PAGO:
            txtestado = "Necesita validación manual: "\
                        "No se ha seleccionado forma de pago para el pedido."
        elif estado_validacion == CLIENTE_DEUDOR:
            txtestado = "Necesita validación manual: "\
                        "Cliente con crédito insuficiente."
        elif estado_validacion == PRECIO_INSUFICIENTE:
            txtestado = "Necesita validación manual: "\
                        "Ventas por debajo de precio mínimo definido."
            for ldp in self.lineasDePedido:
                precioMinimo = ldp.producto.precioMinimo
                precioKilo = ldp.precioKilo
                if (precioMinimo != None and precioKilo != None
                        and precioKilo < precioMinimo):
                    txtestado = "Necesita validación manual: "\
                                "ventas por debajo de precio\n"\
                                "(%s < %s)." % (
                                    utils.float2str(precioKilo),
                                    utils.float2str(precioMinimo))
                    break
        return txtestado

    @property
    def validable(self):
        """
        Devuelve True si el pedido es validable:
            * Ningún precio está por debajo del mínimo.
            * El cliente no está en riesgo (crédito insuficiente).
            * La forma de pago es inferior o igual a 120 días.
        """
        estado_validacion = self.get_estado_validacion()
        if estado_validacion == VALIDABLE:
            return True
        else:
            return False

    def get_estado_validacion(self):
        """
        Devuelve el estado de la validación del pedido en el momento de
        llamar a la función. Puede ser:
            NO_VALIDABLE: Por algún motivo indeterminado o invalidación
                          manual del usuario.
            VALIDABLE: Cumple todos los requisitos de validación automática.
            PLAZO_EXCESIVO: La forma de pago seleccionada en el pedido supera
                            los 120 días. [02/12/2013] Se cambia a 60.
            SIN_FORMA_DE_PAGO: El pedido no tiene forma de pago definida.
            PRECIO_INSUFICIENTE: Algún precio por kilo en las líneas del
                                 pedido está por encima del mínimo configurado
                                 por familia de productos.
            CLIENTE_DEUDOR: El cliente no tiene crédito suficiente.
        """
        validable = VALIDABLE
        for ldp in self.lineasDePedido:
            precioMinimo = ldp.producto.precioMinimo
            precioKilo = ldp.precioKilo
            if (precioMinimo != None and precioKilo != None
                    and precioKilo < precioMinimo):
                validable = PRECIO_INSUFICIENTE
                break
        if validable:
            fdp = self.formaDePago
            if not fdp:
                validable = SIN_FORMA_DE_PAGO
            # elif fdp.plazo > 120:
            elif fdp.plazo > 60:
                validable = PLAZO_EXCESIVO
        if validable:
            importe_pedido = self.calcular_importe_total(iva = True)
            if self.cliente and self.cliente.calcular_credito_disponible(
                    base = importe_pedido) <= 0:
                validable = CLIENTE_DEUDOR
        return validable

    def adivinar_obra(self):
        """
        Devuelve un registro obra o None. El registro obra lo buscará en
        función del texto que tenga guardado el pedido. Si no se encuentra
        ninguno similar, devuelve None.
        Si hubiera varios devuelve el más antiguo de todos para asegurar
        el determinismo.
        """
        txtobra = self.textoObra.strip().upper()
        txtobra = utils.eliminar_dobles_espacios(txtobra)
        obras = Obra.select(Obra.q.nombre == txtobra, orderBy = "id")
        try:
            res = obras[0]
        except IndexError:
            res = None
        return res

    def get_nombre_cliente(self):
        """
        Devuelve el nombre del cliente
        o '' si no tiene cliente asociado.
        """
        if self.cliente == None:
            return ''
        else:
            return self.cliente.nombre

    def calcular_importe_total(self, iva = True):
        """
        Devuelve el importe total del pedido (incluyendo IVA y demás).
        """
        total = 0.0
        for ldp in self.lineasDePedido:
            total += ldp.precio * (1 - ldp.descuento) * ldp.cantidad
        for srv in self.servicios:
            total += srv.get_subtotal()
        total -= total * self.descuento
        if iva:
            total *= (1 + self.iva)
        return total

    @classmethod
    def ultimo_numpedido(cls):
        """
        Devuelve un ENTERO con el último número de albarán sin letras o 0 si
        no hay ninguno o los que hay tienen caracteres alfanuméricos y no se
        pueden pasar a entero.
        Para determinar el último número de albarán no se recorre toda la
        tabla de pedidos intentando convertir a entero. Lo que se hace es
        ordenar a la inversa por ID y comenzar a buscar el primer número de
        pedido convertible a entero.
        """
        # DONE: Además, esto debería ser un método de cls.
        regexp = re.compile("[0-9]*")
        ultimo = 0
        peds = cls.select(orderBy = '-id')
        for p in peds:
            try:
                numpedido = p.numpedido
                ultimo = [int(item) for item in regexp.findall(numpedido)
                          if item != ''][0]
                break
            except (IndexError, ValueError), msg:
                myprint("pclases.py (ultimo_numpedido): Número de último pedido no se pudo determinar: %s" % (msg))
                # No se encontaron números en la cadena de numalbaran o ¿se
                # encontró un número pero no se pudo parsear (!)?
                ultimo = 0
        return ultimo

    @classmethod
    def siguiente_numpedido(cls):
        """
        Devuelve el siguiente número de pedido libre partiendo del último encontrado como entero.
        """
        ultimo = PedidoVenta.get_ultimo_numero_numpedido()
        while PedidoVenta.select(PedidoVenta.q.numpedido == str(ultimo + 1)).count() != 0:
            ultimo += 1
        return ultimo + 1

    get_ultimo_numero_numpedido = ultimo_numpedido
    get_siguiente_numero_numpedido = siguiente_numpedido

    def es_de_fibra(self):
        """
        Devuelve True si es un pedido únicamente de fibra.
        Recalco: u-ni-ca-men-te.
        ¿No ha quedado claro?
        One more time: Debe tener al menos una LDP, y todas las que haya deben
        tener relacionadas un pedido de venta que cumpla que
        producto.es_fibra().
        """
        ldps = [ldp for ldp in self.lineasDePedido if ldp.producto.es_fibra()]
        return len(ldps) == len(self.lineasDePedido) >= 1

    def get_pendiente_servir(self):
        """
        Devuelve un diccionario de productos del pedido con la cantidad
        servida y pedida, una lista de productos pendientes de servir y
        una lista de servicios pendientes de servir.
        """
        productos = {}
        for ldp in self.lineasDePedido:
            producto = ldp.producto
            if producto not in productos:
                productos[producto] = {'servido': 0, 'pedido': 0}
            productos[producto]['pedido'] += ldp.cantidad
        for ldv in self.lineasDeVenta:
            if ldv.albaranSalida:
                producto = ldv.producto
                if producto not in productos:
                    productos[producto] = {'servido': 0, 'pedido': 0}
                productos[producto]['servido'] += ldv.cantidad
        servicios_pendientes = [s for s in self.servicios
                                if s.albaranSalida == None]
        productos_pendientes = [p for p in productos
                        if productos[p]['pedido'] != productos[p]['servido']]
        return productos, productos_pendientes, servicios_pendientes

    def calcular_importe_servido(self, iva = False):
        """
        Devuelve el importe servido de este pedido a los precios que hayan
        especificado en la línea de venta.
        """
        res = 0.0
        for ldv in self.lineasDeVenta:
            res += ldv.calcular_subtotal(iva = True)
        return res

    def calcular_importe_pendiente_de_servir(self, iva = False):
        """
        Devuelve el importe total de productos y servicios pendientes de
        servir del pedido actual según los precios de las líneas de pedido
        pero valorando las salidas al precio de factura (o albarán).
        Incluye el IVA por defecto.
        """
        total = self.calcular_importe_total(iva = iva)
        servido = self.calcular_importe_servido(iva = iva)
        res = total - servido
        return res

    def get_pendiente_facturar(self):
        """
        Devuelve una lista de diccionarios de productos y otra de servicios
        con lo pendiente de facturar del pedido actual, al precio de las
        líneas de pedido y servicios, pero solo con la cantidad pendiente de
        facturar.
        """
        # Primero los servicios, que es lo fácil.
        srvs = []
        for srv in self.servicios:
            if not srv.facturaVenta:
                srvs.append(srv)
        # Ahora los productos.
        productos = {}
        for ldp in self.lineasDePedido:
            producto = ldp.producto
            try:
                productos[producto]['pedido'] += ldp.cantidad
                precio_anterior = productos[producto]['precio']
                if precio_anterior != ldp.precio:
                    # FIXME: Creo que este algoritmo de cálculo de precio
                    # medio no acaba de estar bien.
                    precio_medio = ((ldp.precio * ldp.cantidad) +
                        (precio_anterior * productos[producto]['pedido'])
                        / (productos[producto]['pedido'] + ldp.cantidad))
                    productos[producto]['precio'] = precio_medio
                descuento_anterior = productos[producto]['descuento']
                if descuento_anterior != ldp.descuento:
                    descuento_medio = ((ldp.descuento * ldp.cantidad) +
                        (descuento_anterior * productos[producto]['pedido'])
                        / (productos[producto]['pedido'] + ldp.cantidad))
                    productos[producto]['descuento'] = descuento_medio
                productos[producto]['notas'].append(ldp.notas)
                productos[producto]['textoEntrega'].append(ldp.textoEntrega)
                productos[producto]['fechaEntrega'].append(ldp.fechaEntrega)
            except KeyError:
                productos[producto] = {'pedido': ldp.cantidad,
                                       'facturado': 0.0,
                                       'precio': ldp.precio,
                                       'descuento': ldp.descuento,
                                       'notas': [ldp.notas],
                                       'textoEntrega': [ldp.textoEntrega],
                                       'fechaEntrega': [ldp.fechaEntrega]}
        # Ahora actualizo las cantidades facturadas de los productos
        # recorriendo las facturas del pedido de venta:
        # FIXME: Si se sirve el mismo producto desde dos pedidos diferentes,
        # como para ver lo pendiente de facturar solo se tiene en cuenta
        # este pedido, puede aparecer que se ha facturado de más dando una
        # cantidad negativa en lo pdte. de facturar. Cuando en realidad en
        # ambos pedidos está todo servido y facturado.
        for f in self.get_facturas():
            for ldv in f.lineasDeVenta:
                p = ldv.producto
                if p in productos:
                    productos[p]['facturado'] += ldv.cantidad
        # Aprovecho para limpiar los textos y fechas nulas.
        for p in productos:
            productos[p]['textoEntrega'] = [
                t for t in productos[p]['textoEntrega'] if t]
            productos[p]['fechaEntrega'] = [
                t for t in productos[p]['fechaEntrega'] if t]
        return productos, srvs

    def get_albaranes(self):
        """
        Devuelve los albaranes de salida relacionados con el pedido.
        """
        albaranes = []
        for ldv in self.lineasDeVenta:
            a = ldv.albaranSalida
            if a not in albaranes:
                albaranes.append(a)
        for srv in self.servicios:
            a = srv.albaranSalida
            if a not in albaranes:
                albaranes.append(a)
        return tuple(albaranes)

    def get_facturas(self):
        """
        Devuelve las facturas relacionadas con el pedido actual a través de
        las líneas de venta.
        """
        facturas = []
        for ldv in self.lineasDeVenta:
            fra = ldv.facturaVenta
            if fra != None and fra not in facturas:
                facturas.append(fra)
        return facturas

    def _DEPRECATED_get_facturas(self):
        """
        Devuelve las facturas relacionadas con el pedido actual a través de
        sus albaranes de salida.
        """
        # DEPRECATED
        facturas = []
        for a in self.get_albaranes():
            if not a:
                continue
            for f in a.get_facturas():
                if f not in facturas:
                    facturas.append(f)
        return facturas

    def get_presupuestos(self):
        """
        Devuelve los presupuestos relacionados con el pedido actual.
        """
        presupuestos = []
        for ldp in self.lineasDePedido:
            presupuesto = ldp.presupuesto
            if presupuesto and ldp.presupuesto not in presupuestos:
                presupuestos.append(presupuesto)
        return presupuestos

cont, tiempo = print_verbose(cont, total, tiempo)

class LineaDePresupuesto(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_descripcion_producto(self):
        if self.productoVenta:
            desc = self.productoVenta.descripcion
        elif self.productoCompra:
            desc = self.productoCompra.descripcion
        else:
            desc = self.descripcion
        return desc

    def get_subtotal(self, iva = False):
        """
        Devuelve el subtotal de esta línea de presupuesto.
        """
        subtotal = self.cantidad * self.precio
        if iva:
            try:
                subtotal *= (1 + self.presupuesto.cliente.iva)
            except AttributeError:
                raise ValueError, "pclases::LineaDePresupuesto::calcular_subtotal -> La LDP ID %s no tiene cliente del que obtener el IVA."
        return subtotal

    @property
    def precioKilo(self):
        """
        Devuelve el precio por kilo de la línea de pedido siempre que sea
        posible. None si no lo puede calcular.
        """
        res = None
        # TODO: De momento solo para geotextiles.
        if hasattr(self.producto, "es_rollo") and self.producto.es_rollo():
            # El precio es por metro cuadrado. Tengo que hacer la conversión:
            gramos_m2 = self.producto.camposEspecificosRollo.gramos
            m2 = self.producto.camposEspecificosRollo.metrosCuadrados
            kilos = gramos_m2 / 1000.0 * m2
            try:
                res = self.precio * m2 / kilos
            except ZeroDivisionError:
                res = None
        return res

    @property
    def producto(self):
        """
        Devuelve el objeto producto relacionado con la línea de venta, sea
        del tipo que sea (productoVenta o productoCompra). None si no hay
        ningún producto relacionado.
        """
        res = None
        if self.productoVenta != None:
            res = self.productoVenta
        elif self.productoCompra != None:
            res = self.productoCompra
        return res

    @producto.setter
    def producto(self, producto):
        """
        Comprueba qué tipo de producto es el del parámetro "producto"
        recibido e instancia el atributo adecuado poniendo a
        None el del tipo de producto que no corresponda.
        Si la clase del objeto no es ninguna de las soportadas por
        la línea de venta, lanzará una excepción TypeError.
        """
        if isinstance(producto, ProductoVenta):
            self.productoVenta = producto
            self.productoCompra = None
        elif isinstance(producto, ProductoCompra):
            self.productoVenta = None
            self.productoCompra = producto
        else:
            raise TypeError

    def _link_producto(self):
        """
        Localiza un producto de venta o de compra cuya descripción sea
        igual a la guardada y crea el enlace correspondiente entre registros.
        Devuelve True si hace algún cambio en el registro.
        """
        res = False
        self.sync()
        if not self.productoCompra and not self.productoVenta:
            try:
                self.producto = ProductoVenta.selectBy(
                        descripcion = self.descripcion)[0]
                res = True
            except IndexError:
                try:
                    self.producto = ProductoCompra.selectBy(
                            descripcion = self.descripcion)[0]
                    res = True
                except IndexError:
                    pass
        if res:
            self.syncUpdate()
        return res

cont, tiempo = print_verbose(cont, total, tiempo)

class Presupuesto(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- clienteID = ForeignKey('Cliente')
    lineasDePedido = MultipleJoin('LineaDePedido')
    servicios = MultipleJoin('Servicio')
    lineasDePresupuesto = MultipleJoin('LineaDePresupuesto')
    #------------------------------------- comercialID = ForeignKey("Comercial")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_ofertado_por_producto(self):
        """
        Devuelve un diccionario de productos y cantidad solicitada total.
        """
        res = {}
        for ldp in self.lineasDePresupuesto:
            producto = ldp.producto
            if not producto:
                producto = ldp.descripcion
            try:
                res[producto] += ldp.cantidad
            except KeyError:
                res[producto] = ldp.cantidad
        return res

    def get_pedido_por_producto(self):
        """
        Devuelve un diccionario de productos y cantidad total pasada a pedido.
        """
        res = {}
        for ldp in self.lineasDePedido:
            producto = ldp.producto
            try:
                res[producto] += ldp.cantidad
            except KeyError:
                res[producto] = ldp.cantidad
        for srv in self.servicios:
            concepto = srv.concepto
            try:
                res[concepto] += srv.cantidad
            except KeyError:
                res[concepto] = srv.cantidad
        return res

    def get_servido_por_producto(self):
        """
        Devuelve un diccionario de productos y cantidad total servida en
        albaranes a través de pedido.
        """
        res = {}
        for ldp in self.lineasDePedido:
            producto = ldp.producto
            try:
                res[producto] += ldp.get_cantidad_servida()
            except KeyError:
                res[producto] = ldp.get_cantidad_servida()
        for srv in self.servicios:
            if not srv.albaranSalida:   # No se ha servido
                continue
            concepto = srv.concepto
            try:
                res[concepto] += srv.cantidad
            except KeyError:
                res[concepto] = srv.cantidad
        return res

    def get_facturado_por_producto(self):
        """
        Devuelve un diccionario de productos y cantidad total facturada en
        facturas a través de albaranes y pedidos.
        """
        res = {}
        for ldp in self.lineasDePedido:
            for ldv in ldp.get_lineas_de_venta():
                producto = ldp.producto
                try:
                    res[producto] += ldv.cantidad
                except KeyError:
                    res[producto] = ldv.cantidad
        for srv in self.servicios:
            if not srv.facturaVenta:   # No se ha facturado
                continue
            concepto = srv.concepto
            try:
                res[concepto] += srv.cantidad
            except KeyError:
                res[concepto] = srv.cantidad
        return res

    def get_pendiente_pasar_a_pedido(self):
        """
        Devuelve un diccionario de productos (o descripciones de productos)
        con las cantidades pendientes de pasar a pedido. Si un producto ya
        se ha pasado por completo según las cantidades de las líneas de
        presupuesto, no lo añade al diccionario.
        """
        res = self.get_ofertado_por_producto()
        dic_pedido = self.get_pedido_por_producto()
        for p in dic_pedido:
            if p in res:    # Y si no se ha presupuestado, viene de otro lado
                            # o se ha creado a mano. Lo ignoro.
                res[p] -= dic_pedido[p]
                if res[p] <= 0:     # Lo retiro del resultado por contrato.
                    res.pop(p)
        return res

    def get_pedidos(self):
        """
        Devuelve los pedidos relacionados con el presupuesto
        a través de sus líneas de pedido y servicios.
        """
        pedidos = []
        for ldp in self.lineasDePedido:
            ldppedidoVenta = ldp.pedidoVenta
            if ldppedidoVenta != None and ldppedidoVenta not in pedidos:
                pedidos.append(ldppedidoVenta)
        for srv in self.servicios:
            srvpedidoVenta = srv.pedidoVenta
            if srvpedidoVenta != None and srvpedidoVenta not in pedidos:
                pedidos.append(srvpedidoVenta)
        return pedidos

    def get_albaranes(self):
        """
        Devuelve los albaranes relacionados con los pedidos relacionados con
        la oferta.
        No siempre, pero por lo general la correspondencia es 1:1:1
        """
        albaranes = []
        for p in self.get_pedidos():
            for a in p.get_albaranes():
                if a not in albaranes:
                    albaranes.append(a)
        return albaranes

    def get_facturas(self):
        """
        Devuelve las facturas relacionadas con los albaranes relacionados
        con los pedidos relacionados con la oferta actual.
        No siempre, pero por lo general la correspondencia es 1:1:1:1
        """
        facturas = []
        for p in self.get_pedidos():
            for f in p.get_facturas():
                if f not in facturas:
                    facturas.append(f)
        return facturas

    def esta_servido(self):
        """
        Devuelve True con que tan solo se haya servido una parte del pedido.
        En realidad lo único que hace es ver si tiene líneas de pedido o
        servicios asociados a la oferta.
        """
        return self.lineasDePedido or self.servicios

    def calcular_total(self, iva = True):
        """
        Calcula el total del presupuesto, con IVA y demás incluido.
        Devuelve un FixedPoint (a casi todos los efectos, se comporta como
        un FLOAT.
        De todas formas, pasa bien por el utils.float2str).
        """
        subtotal = self.calcular_subtotal()
        if iva:
            tot_iva = self.calcular_total_iva(subtotal)
        else:
            tot_iva = 0.0
        irpf = self.calcular_total_irpf(subtotal)
        total = subtotal + tot_iva + irpf
        return total

    def calcular_importe_total(self, iva = True):
        """
        Calcula y devuelve el importe total, incluyendo IVA, de la factura.
        """
        return self.calcular_total(iva)

    importeTotal = property(calcular_importe_total,
                            doc = calcular_importe_total.__doc__)

    def calcular_total_iva(self, subtotal = None):
        """
        Calcula el importe total de IVA del presupuesto.
        """
        if subtotal == None:
            subtotal = self.calcular_subtotal()
        try:
            iva = self.cliente.get_iva_norm()
        except AttributeError:
            espanna = ("ESPAÑA", "ESPAñA", "SPAIN", "ESPANA", "ESP", "ES",
                       "ESPANNA")
            if (self.pais and self.pais.upper() not in espanna):
                iva = 0
            else:
                iva = 0.21
        total_iva = utils.ffloat(subtotal) * iva
        return total_iva

    def calcular_total_irpf(self, subtotal = None):
        """
        Calcula el importe total de retención de IRPF (se resta al total)
        del presupuesto.
        """
        if subtotal == None:
            subtotal = self.calcular_subtotal()
        try:
            dde = DatosDeLaEmpresa.select()[0]
            irpf = dde.irpf
        except IndexError:
            irpf = 0.0
        total_irpf = utils.ffloat(subtotal) * irpf
        return total_irpf

    def calcular_subtotal(self, incluir_descuento = True):
        """
        Devuelve el subtotal del presupuesto: líneas
        de pedido + servicios - descuento.
        No cuenta IVA.
        """
        #total_ldvs = sum([utils.ffloat((l.cantidad * l.precio) * (1 - l.descuento)) for l in self.lineasDePedido])
        #total_srvs = sum([utils.ffloat((s.precio * s.cantidad) * (1 - s.descuento)) for s in self.servicios])
        #subtotal = total_ldvs + total_srvs
        subtotal = sum([utils.ffloat(s.precio * s.cantidad)
                        for s in self.lineasDePresupuesto])
        #if incluir_descuento:
        #    subtotal *= 1 - self.descuento
        return subtotal

    def calcular_base_imponible(self):
        """
        Devuelve la suma de conceptos con el descuento global por defecto.
        """
        return self.calcular_subtotal(incluir_descuento = True)

    def calcular_fecha_limite(self):
        """
        Calcula y deuelve la fecha límite de validez del presupuesto.
        El periodo de validez es en meses, de modo que no soy estricto con los
        días; y si cae en final de mes, por ejemplo, y el mes siguiente no
        tiene los mismos días, bajo hasta el último día del mes, no lo paso
        al 1 del siguiente para respetar el "sentido" de la validez en meses.
        """
        fecha_limite = fecha = self.fecha
        mes_fecha = fecha.month
        anno_fecha = fecha.year
        mes_limite = mes_fecha + self.validez
        anno_limite = anno_fecha + ((mes_limite) / 13)
        if mes_limite > 12:
            mes_limite %= 12
        dia = fecha.day
        while dia > 0:
            # Usando «dia» como variable de control evito por un lado el
            # bucle infinito y por otro que se intente crear fechas con
            # días negativos (que según qué versión de MX es posible, pero
            # no me es útil en este caso).
            try:
                fecha_limite = mx.DateTime.DateTimeFrom(day = dia,
                                                        month = mes_limite,
                                                        year = anno_limite)
                break
            except mx.DateTime.RangeError:  # Día fuera de rango
                dia -= 1
        return fecha_limite

    def esta_vigente(self):
        """
        Devuelve True si la validez del presupuesto es 0 o la fecha actual
        es inferior o igual a la fecha del presupuesto + «validez» meses.
        """
        hoy = mx.DateTime.localtime()
        fecha_limite = self.calcular_fecha_limite()
        return (not self.validez) or hoy <= fecha_limite

    def check_validacion_precios(self):
        """
        Comprueba la restricción del precio mínimo. Si se incumple devuelve
        False. Si la supera, True.
        """
        res = True
        for ldp in self.lineasDePresupuesto:
            try:
                precioMinimo = round(ldp.producto.precioMinimo, 3)
            except (AttributeError, TypeError): # Es un producto que no existe,
                    # no tiene precio mínimo su familia o un es un servicio.
                precioMinimo = None
            try:
                precioKilo = round(ldp.precioKilo, 3)
            except TypeError:   # Es None
                precioKilo = None
            if (precioMinimo != None and precioKilo != None
                    and precioKilo < precioMinimo):
                res = False
                break
        return res

    @property
    def condicionesParticulares(self):
        return self.texto

    @condicionesParticulares.setter
    def condicionesParticulares(self, txt):
        self.texto = txt
        self.syncUpdate()

    def __lleva_servicio(self):
        """
        Devuelve True si hay al menos una línea del presupuesto que es de
        servicios.
        """
        res = False
        for ldp in self.lineasDePresupuesto:
            if (not ldp.productoVenta and not ldp.productoCompra and
                not "TRANSPORTE " in ldp.descripcion.upper() and
                not "TRANSPORT " in ldp.descripcion.upper() and
                ldp.descripcion.upper().strip() != "TRANSPORTE" and
                ldp.descripcion.upper().strip() != "TRANSPORT"):
                res = True
                break   # Para optimizar
        return res

    def get_estado_validacion(self):
        """
        Devuelve el estado de la validación del presupuesto en el momento de
        llamar a la función. Puede ser:
            VALIDABLE: Cumple todos los requisitos de validación automática.
            NO_VALIDABLE: El cliente todavía no tiene ficha.
            PLAZO_EXCESIVO: La forma de pago seleccionada en el pedido supera
                            los 120 días. [02/12/2013] Se cambia a 60.
            SIN_FORMA_DE_PAGO: El pedido no tiene forma de pago definida.
            PRECIO_INSUFICIENTE: Algún precio por kilo en las líneas del
                                 pedido está por encima del mínimo configurado
                                 por familia de productos.
            CLIENTE_DEUDOR: El cliente no tiene crédito suficiente.
            SIN_CIF: No se ha informado del CIF del cliente.
            COND_PARTICULARES: Lleva condiciones particulares y requiere
                               por CWT que se valide manualmente.
            COMERCIALIZADO: Lleva comercializados (ProductoCompra).
            BLOQUEO_FORZADO: El usuario al que pertenece el presupuesto tiene
                             el campo "validacion_manual" a True, que fuerza
                             a que todos sus presupuestos deban ser validados
                             manualmente a pesar de que cumpla el resto de
                             requisitos. (CWT)
            BLOQUEO_CLIENTE: El cliente de la oferta tiene el campo
                             "validacion_manual" a True, que fuerza a que
                             todos sus presupuestos deban ser validados
                             manualmente aunque cumpla el resto de requisitos.
                             (CWT)
            SERVICIO: La oferta lleva algún de servicio. Necesita
                      validación manual para evitar los casos en que se
                      mete un producto como servicio, se valida y a posteriori
                      se crea el comercializado exactamente con la misma
                      descripción (conservando validación y convirtiendo la
                      línea en una venta de comercializados sin pasar por
                      la validación COMERCIALIZADO).
        """
        # Debería tener las condiciones en un solo sitio. Los pedidos y
        # presupuestos siguen el mismo criterio, pero están especificados por
        # duplicado en una función en cada clase.
        # Para el caso del bloqueo forzado, ver correo de nzumer del 16/10/2014
        validable = VALIDABLE
        if (validable == VALIDABLE
                and self.comercial and self.comercial.validacionManual):
            validable = BLOQUEO_FORZADO
        if (validable == VALIDABLE
                and self.cliente and self.cliente.validacionManual):
            validable = BLOQUEO_CLIENTE
        if (validable == VALIDABLE
                and self.__lleva_servicio()):
            validable = SERVICIO
        if validable == VALIDABLE:
            if self._lleva_comercializado():
                validable = COMERCIALIZADO
        if self.condicionesParticulares:
            validable = COND_PARTICULARES
        if validable == VALIDABLE and not self.check_validacion_precios():
            validable = PRECIO_INSUFICIENTE
        if validable == VALIDABLE:
            fdp = self.formaDePago
            if not fdp:
                validable = SIN_FORMA_DE_PAGO
            # elif fdp.plazo > 120:
            elif fdp.plazo > 60:
                validable = PLAZO_EXCESIVO
        if validable == VALIDABLE:
            if not self.cif.strip():
                validable = SIN_CIF
        if validable == VALIDABLE:
            importe_presupuesto = self.calcular_importe_total(iva = True)
            if self.cliente and self.cliente.calcular_credito_disponible(
                    base = importe_presupuesto) <= 0:
                validable = CLIENTE_DEUDOR
        if validable == VALIDABLE:
            if not self.cliente and not self.nombrecliente:
                validable = SIN_CLIENTE
        if validable == VALIDABLE:
            if not self.cliente:
                validable = NO_VALIDABLE
        return validable

    def _lleva_comercializado(self):
        """
        True si alguna línea de presupuesto lleva comercializados.
        """
        res = False
        for ldp in self.lineasDePresupuesto:
            if isinstance(ldp.producto, ProductoCompra):
                res = True
                break
        return res

    def get_str_estado(self):
        """
        Devuelve una cadena de texto con el estado de la oferta y el motivo,
        en su caso, del impedimento de pasarlo a pedido.
        """
        txtestado = None
        estado_validacion = self.get_estado_validacion()
        if estado_validacion == VALIDABLE:
            txtestado = "Presupuesto válido"
            if self.usuario:
                txtestado += " (%s)" % self.usuario.usuario
        elif estado_validacion == NO_VALIDABLE:
            txtestado = "Necesita validación manual: "\
                        "Cliente sin alta en la aplicación."
        elif estado_validacion == PLAZO_EXCESIVO:
            txtestado = "Necesita validación manual: "\
                        "El plazo de la forma de pago es excesivo."
        elif estado_validacion == SIN_FORMA_DE_PAGO:
            txtestado = "Necesita validación manual: "\
                        "No se ha seleccionado forma de pago para la oferta."
        elif estado_validacion == CLIENTE_DEUDOR:
            txtestado = "Necesita validación manual: "\
                        "Cliente con crédito insuficiente."
        elif estado_validacion == SIN_CIF:
            txtestado = "Necesita validación manual: "\
                        "CIF no presente."
        elif estado_validacion == SIN_CLIENTE:
            txtestado = "Necesita validación manual: "\
                        "Presupuesto sin cliente."
        elif estado_validacion == PRECIO_INSUFICIENTE:
            txtestado = "Necesita validación manual: "\
                        "Productos por debajo de precio mínimo definido."
            for ldp in self.lineasDePedido:
                precioMinimo = ldp.producto.precioMinimo
                precioKilo = ldp.precioKilo
                if (precioMinimo != None and precioKilo != None
                        and precioKilo < precioMinimo):
                    txtestado = "Necesita validación manual: "\
                                "ventas por debajo de precio\n"\
                                "(%s < %s)." % (
                                    utils.float2str(precioKilo),
                                    utils.float2str(precioMinimo))
                    break
        elif estado_validacion == COND_PARTICULARES:
            txtestado = "Necesita validación manual: "\
                        "La oferta presenta condiciones particulares."
        elif estado_validacion == COMERCIALIZADO:
            txtestado = "Necesita validación manual: "\
                        "La oferta contiene comercializados."
        elif estado_validacion == BLOQUEO_FORZADO:
            txtestado = "Necesita validación manual: "\
                        "Restricción forzada en la configuración del usuario."
        elif estado_validacion == BLOQUEO_CLIENTE:
            txtestado = "Necesita validacion manual: "\
                        "Restricción forzada en la configuración del cliente."
        elif estado_validacion == SERVICIO:
            txtestado = "Necesita validación manual: "\
                        "La oferta incluye alguna línea de prestación de "\
                        "servicios." # o transporte."
        return txtestado

    def get_str_validacion(self):
        """
        Devuelve, si está validado, una cadena con la persona y fecha en que
        validó.
        """
        res = ""
        if self.validado:
            res = "Validado por %s el %s." % (self.usuario.nombre,
                        utils.str_fechahora(self.fechaValidacion))
        return res

    @property
    def validable(self):
        return self.get_estado_validacion() == VALIDABLE

    @property
    def validado(self):
        return self.usuario and True or False

    @validado.setter
    def validado(self, usuario):
        if not usuario:
            self.usuario = None
            self.fechaValidacion = None
        elif isinstance(usuario, Usuario):
            self.usuario = usuario
            fv = datetime.datetime.now()
            if fv:
                fv_aprox = datetime.datetime(fv.year, fv.month, fv.day,
                                             fv.hour, fv.minute, fv.second)
            else:
                fv_aprox = None
            self.fechaValidacion = fv
        else:
            raise ValueError, "El parámetro de validación de presupuesto "\
                              "debe ser un usuario de pclases o False."

    def get_str_tipo(self):
        if self.estudio is None:
            return "Indeterminado"
        if self.estudio:
            return "Estudio"
        return "Pedido"

cont, tiempo = print_verbose(cont, total, tiempo)

class Comercial(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------------------------- empleadoID = ForeignKey("Empleado")
    presupuestos = MultipleJoin("Presupuesto")
    pedidosVenta = MultipleJoin('PedidoVenta')
    visitas = MultipleJoin("Visita")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_nombre_completo(self):
        try:
            return self.empleado.get_nombre_completo()
        except AttributeError:
            return ""

    def get_usuario(self):
        """
        Devuelve el usuario asociado a este comercial.
        """
        try:
            return self.empleado.usuario
        except AttributeError:
            return None

    def get_firma_html(self):
        try:
            firma_comercial = '<b>%s %s</b><br><i>%s</i><br>'\
                              '%s<br>'\
                              '<u><a href="mailto:%s">%s</a></u>'\
                              '<b> </b>' % (
                self.empleado.nombre and self.empleado.nombre or "",
                self.empleado.apellidos and self.empleado.apellidos or "",
                self.cargo and self.cargo or "",
                self.telefono and self.telefono or "",
                self.correoe and self.correoe or "",
                self.correoe and self.correoe or "")
        except AttributeError:
            firma_comercial = ""
        return firma_comercial

    def get_firma(self):
        try:
            firma_comercial = '%s %s\n%s\n'\
                              '%s\n'\
                              '%s' % (
                self.empleado.nombre and self.empleado.nombre or "",
                self.empleado.apellidos and self.empleado.apellidos or "",
                self.cargo and self.cargo or "",
                self.telefono and self.telefono or "",
                self.correoe and self.correoe or "")
        except AttributeError:
            firma_comercial = ""
        return firma_comercial

cont, tiempo = print_verbose(cont, total, tiempo)

class MotivoVisita(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True

    visitas = MultipleJoin("Visita")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    @staticmethod
    def search(text):
        """
        Busca y devuelve el motivo de visita correspondiente al texto.
        Si no encuentra nada o no existen, devuelve None.
        """
        # PLAN: Podría hacer una búsqueda difusa o algo, pero como el texto
        # siempre va a existir en la BD porque viene de un
        # autocompletado/combo, ni me molesto.
        try:
            res = MotivoVisita.selectBy(motivo = text)[0]
        except IndexError:
            res = None
        return res

cont, tiempo = print_verbose(cont, total, tiempo)

class Visita(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class CamposEspecificos(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------- productoVentaID = ForeignKey('ProductoVenta')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class ModeloEtiqueta(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    camposEspecificosRollo = MultipleJoin("CamposEspecificosRollo")
    camposEspecificosBala = MultipleJoin("CamposEspecificosBala")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_func(self):
        """
        Devuelve un objeto función (ya instanciado y listo para llamar) que
        generará el PDF de las etiquetas. Este método se encarga de importar
        el módulo y todo lo necesario para devolver el "puntero a función".
        Si no se encuentra la función configurada, lanza una ValueError.
        """
        if self.modulo:
            modulo = self.modulo
        else:   # Si no hay módulo, se busca en geninformes.
            modulo = "geninformes"
        try:
            modulobj = __import__("informes." + modulo)
        except ImportError, e:
            raise ValueError, "pclases::ModeloEtiqueta.get_func -> "\
                "El módulo %s no se encontró en la ruta estándar "\
                "de informes. Información de la excepción original: %s" % (
                modulo, e)
        try:
            fwrap = getattr(getattr(modulobj, modulo), self.funcion)
        except NameError:
            raise ValueError, "pclases::ModeloEtiqueta.get_func -> " \
                "El módulo %s no contiene ninguna función %s." % (
                    modulo, self.funcion)
        return fwrap

    @staticmethod
    def get_default():
        """
        Devuelve el modelo de etiqueta a usar por defecto.
        """
        try:
            res = ModeloEtiqueta.selectBy(nombre="Normativa julio 2013")[0]
        except IndexError:
            res = None
        return res


cont, tiempo = print_verbose(cont, total, tiempo)

class CamposEspecificosRollo(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    productosVenta = MultipleJoin('ProductoVenta')
    marcadosCe = MultipleJoin("MarcadoCe")
    #--------------------------- modeloEtiquetaID = ForeignKey("ModeloEtiqueta")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_metros_cuadrados(self):
        """
        Devuelve los metros cuadrados del producto.
        """
        return self.ancho * self.metrosLineales

    def get_peso_teorico(self):
        """
        Devuelve el peso teórico del producto en kilogramos.
        """
        return (self.metros_cuadrados * self.gramos) / 1000.0

    metros_cuadrados = metrosCuadrados = property(get_metros_cuadrados)
    peso_teorico = pesoTeorico = property(get_peso_teorico)

    valorPruebaGramajeSup = property(lambda self:
        self.estandarPruebaGramaje + self.toleranciaPruebaGramajeSup)
    valorPruebaGramajeInf = property(lambda self:
        self.estandarPruebaGramaje + self.toleranciaPruebaGramaje)
    valorPruebaLongitudinalSup = property(lambda self:
        self.estandarPruebaLongitudinal + self.toleranciaPruebaLongitudinalSup)
    valorPruebaLongitudinalInf = property(lambda self:
        self.estandarPruebaLongitudinal + self.toleranciaPruebaLongitudinal)
    valorPruebaAlargamientoLongitudinalSup = property(lambda self:
        self.estandarPruebaAlargamientoLongitudinal
        + self.toleranciaPruebaAlargamientoLongitudinalSup)
    valorPruebaAlargamientoLongitudinalInf = property(lambda self:
        self.estandarPruebaAlargamientoLongitudinal
        + self.toleranciaPruebaAlargamientoLongitudinal)
    valorPruebaTransversalSup = property(lambda self:
        self.estandarPruebaTransversal + self.toleranciaPruebaTransversalSup)
    valorPruebaTransversalInf = property(lambda self:
        self.estandarPruebaTransversal + self.toleranciaPruebaTransversal)
    valorPruebaAlargamientoTransversalSup = property(lambda self:
        self.estandarPruebaAlargamientoTransversal
        + self.toleranciaPruebaAlargamientoTransversalSup)
    valorPruebaAlargamientoTransversalInf = property(lambda self:
        self.estandarPruebaAlargamientoTransversal
        + self.toleranciaPruebaAlargamientoTransversal)
    valorPruebaCompresionSup = property(lambda self:
        self.estandarPruebaCompresion + self.toleranciaPruebaCompresionSup)
    valorPruebaCompresionInf = property(lambda self:
        self.estandarPruebaCompresion + self.toleranciaPruebaCompresion)
    valorPruebaPerforacionSup = property(lambda self:
        self.estandarPruebaPerforacion + self.toleranciaPruebaPerforacionSup)
    valorPruebaPerforacionInf = property(lambda self:
        self.estandarPruebaPerforacion + self.toleranciaPruebaPerforacion)
    valorPruebaEspesorSup = property(lambda self:
        self.estandarPruebaEspesor + self.toleranciaPruebaEspesorSup)
    valorPruebaEspesorInf = property(lambda self:
        self.estandarPruebaEspesor + self.toleranciaPruebaEspesor)
    valorPruebaPermeabilidadSup = property(lambda self:
        self.estandarPruebaPermeabilidad+self.toleranciaPruebaPermeabilidadSup)
    valorPruebaPermeabilidadInf = property(lambda self:
        self.estandarPruebaPermeabilidad + self.toleranciaPruebaPermeabilidad)
    valorPruebaPorosSup = property(lambda self:
        self.estandarPruebaPoros + self.toleranciaPruebaPorosSup)
    valorPruebaPorosInf = property(lambda self:
        self.estandarPruebaPoros + self.toleranciaPruebaPoros)
    valorPruebaPiramidalSup = property(lambda self:
        self.estandarPruebaPiramidal + self.toleranciaPruebaPiramidalSup)
    valorPruebaPiramidalInf = property(lambda self:
        self.estandarPruebaPiramidal + self.toleranciaPruebaPiramidal)
    # NOTA: estandarPrueba siempre es el óptimo y puede ocurrir que no se
    # encuentre en medio de las dos tolerancias aplicadas sobre el mismo.

    def comparar_con_marcado(self, valor, prueba, fecha=None):
        """
        "valor" es un float que se comparará con el marcado.
        "prueba" es el nombre del campo de la prueba («Gramaje», por ejemplo) y
        debe respetar el formato 'de facto' de los nombres de los atributos.
        Devuelve dos valores: la diferencia respecto al óptimo de la prueba y
        un entero en una escala de 0 a 3 donde 0 es el valor óptimo y 3 es el
        peor resultado.
        Ese valor se determina según el tipo de prueba:
            - Si es una prueba donde el óptimo se encuentra en el centro de un
              rango:
              <-----3----)[-----1----)[0](----1-----](----3----->  (2: UNUSED)
             min      tol. inf.      óptimo      tol. sup.     max
            - Si es una prueba donde el óptimo es a la vez un extremo del rango:
              <-----3----)[-----2----)[-----1----)[0----->
             min      tol. inf.    tol. sup.    óptimo  max
                                             (Óptimo = valor estándar o mejor)
        Devuelve -1 cuando no se puede evaluar la prueba, bien por valor nulo
        en pruebas (valor = None) o bien porque no se pudo determinar el rango
        de evaluación.
        Si fecha es None o no hay marcados que comprendan la fecha, se compara
        con los valores de referencia que se guardan aquí. En otro caso, los
        valores se toman de la ficha de marcado CE cuyo rango de fechas
        comprenda a la fecha recibida. Si hay más de uno, usa el último
        introducido en el sistema.
        """
        pruebas = ("AlargamientoLongitudinal", "AlargamientoTransversal",
                   "Longitudinal", "Transversal", "Poros", "Gramaje",
                   "Espesor", "Compresion", "Perforacion", "Permeabilidad",
                   "Piramidal")
        if prueba not in pruebas:
            raise ValueError, '"prueba" debe tener alguno de estos valores'\
                              ': %s' % (", ".join([p for p in pruebas]))

        # Determino el valor de referencia en función de la fecha recibida.
        marcado = self.buscar_marcado(fecha)
        if not fecha or not marcado:
            marcado = self
        inf = getattr(marcado, "valorPrueba%sInf" % (prueba))
        sup = getattr(marcado, "valorPrueba%sSup" % (prueba))
        optimo = getattr(marcado, "estandarPrueba%s" % (prueba))
        if valor != None:
            dif = valor - optimo
            if inf <= optimo <= sup:    # Inf SIEMPRE SIEMPRE es menor que
                                        # Sup esté donde esté el estándar.
                if valor == optimo:
                    evaluacion = 0
                elif (inf <= valor < optimo) or (optimo < valor <= sup):
                    evaluacion = 1
                else:
                    evaluacion = 3
            elif inf <= sup <= optimo:      # Más, mejor.
                if valor >= optimo:
                    evaluacion = 0
                elif sup <= valor < optimo:
                    evaluacion = 1
                elif inf <= valor < sup:
                    evaluacion = 2
                else:
                    evaluacion = 3
            elif optimo <= inf <= sup:      # Menos, mejor.
                if valor <= optimo:
                    evaluacion = 0
                elif optimo < valor <= inf:
                    evaluacion = 1
                elif inf < valor <= sup:
                    evaluacion = 2
                else:
                    evaluacion = 3
            else:
                myprint("pclases::CamposEspecificosRollo::comparar_con_marcado"\
                      " -> No se pudo determinar el tipo de rango de la "\
                      "prueba de marcado CE. ID %d.", self.id)
                evaluacion = -1
        else:
            dif = optimo
            evaluacion = -1
        return dif, evaluacion

    def buscar_marcado(self, fecha):
        """
        Devuelve un registro MarcadoCe que corresponda con la fecha recibida.
        Si no se encuentra, devuelve None.
        Si hay varios, devuelve el último introducido en el sistema (por orden
        de clave primaria).
        """
        marcados = MarcadoCe.select(AND(
                        OR(MarcadoCe.q.fechaInicio <= fecha,
                           MarcadoCe.q.fechaInicio == None),
                        OR(MarcadoCe.q.fechaFin >= fecha,
                           MarcadoCe.q.fechaFin == None),
                        MarcadoCe.q.camposEspecificosRolloID == self.id),
                    orderBy = "-id")
        try:
            res = marcados[0]
        except IndexError:
            res = None
        return res

    def _copyMarcadoTo(self, cer):
        """
        Copia los valores del marcado CE del rollo al objeto
        CamposEspecificosRollo recibido.
        """
        if not isinstance(cer, (CamposEspecificosRollo, MarcadoCe)):
            raise TypeError
        pruebas = ("AlargamientoLongitudinal", "AlargamientoTransversal",
                   "Longitudinal", "Transversal", "Poros", "Gramaje",
                   "Espesor", "Compresion", "Perforacion", "Permeabilidad",
                   "Piramidal")
        campos = ("toleranciaPrueba%s",
                  "toleranciaPrueba%sSup",
                  "estandarPrueba%s")
        for prueba in pruebas:
            for campo in campos:
                nombre_campo = campo % prueba
                valor = getattr(self, nombre_campo)
                setattr(cer, nombre_campo, valor)


cont, tiempo = print_verbose(cont, total, tiempo)

class MarcadoCe(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------- camposEspecificosRolloID = ForeignKey('CamposEspecificosRollo')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    valorPruebaGramajeSup = property(lambda self: self.estandarPruebaGramaje + self.toleranciaPruebaGramajeSup)
    valorPruebaGramajeInf = property(lambda self: self.estandarPruebaGramaje + self.toleranciaPruebaGramaje)
    valorPruebaLongitudinalSup = property(lambda self: self.estandarPruebaLongitudinal + self.toleranciaPruebaLongitudinalSup)
    valorPruebaLongitudinalInf = property(lambda self: self.estandarPruebaLongitudinal + self.toleranciaPruebaLongitudinal)
    valorPruebaAlargamientoLongitudinalSup = property(lambda self: self.estandarPruebaAlargamientoLongitudinal + self.toleranciaPruebaAlargamientoLongitudinalSup)
    valorPruebaAlargamientoLongitudinalInf = property(lambda self: self.estandarPruebaAlargamientoLongitudinal + self.toleranciaPruebaAlargamientoLongitudinal)
    valorPruebaTransversalSup = property(lambda self: self.estandarPruebaTransversal + self.toleranciaPruebaTransversalSup)
    valorPruebaTransversalInf = property(lambda self: self.estandarPruebaTransversal + self.toleranciaPruebaTransversal)
    valorPruebaAlargamientoTransversalSup = property(lambda self: self.estandarPruebaAlargamientoTransversal + self.toleranciaPruebaAlargamientoTransversalSup)
    valorPruebaAlargamientoTransversalInf = property(lambda self: self.estandarPruebaAlargamientoTransversal + self.toleranciaPruebaAlargamientoTransversal)
    valorPruebaCompresionSup = property(lambda self: self.estandarPruebaCompresion + self.toleranciaPruebaCompresionSup)
    valorPruebaCompresionInf = property(lambda self: self.estandarPruebaCompresion + self.toleranciaPruebaCompresion)
    valorPruebaPerforacionSup = property(lambda self: self.estandarPruebaPerforacion + self.toleranciaPruebaPerforacionSup)
    valorPruebaPerforacionInf = property(lambda self: self.estandarPruebaPerforacion + self.toleranciaPruebaPerforacion)
    valorPruebaEspesorSup = property(lambda self: self.estandarPruebaEspesor + self.toleranciaPruebaEspesorSup)
    valorPruebaEspesorInf = property(lambda self: self.estandarPruebaEspesor + self.toleranciaPruebaEspesor)
    valorPruebaPermeabilidadSup = property(lambda self: self.estandarPruebaPermeabilidad + self.toleranciaPruebaPermeabilidadSup)
    valorPruebaPermeabilidadInf = property(lambda self: self.estandarPruebaPermeabilidad + self.toleranciaPruebaPermeabilidad)
    valorPruebaPorosSup = property(lambda self: self.estandarPruebaPoros + self.toleranciaPruebaPorosSup)
    valorPruebaPorosInf = property(lambda self: self.estandarPruebaPoros + self.toleranciaPruebaPoros)
    valorPruebaPiramidalSup = property(lambda self: self.estandarPruebaPiramidal + self.toleranciaPruebaPiramidalSup)
    valorPruebaPiramidalInf = property(lambda self: self.estandarPruebaPiramidal + self.toleranciaPruebaPiramidal)
    # NOTA: estandarPrueba siempre es el óptimo y puede ocurrir que no se
    # encuentre en medio de las dos tolerancias aplicadas sobre el mismo.

    def _copyMarcadoTo(self, cer):
        """
        Copia los valores del marcado CE del rollo al objeto
        CamposEspecificosRollo recibido.
        """
        if not isinstance(cer, (CamposEspecificosRollo, MarcadoCe)):
            raise TypeError
        pruebas = ("AlargamientoLongitudinal", "AlargamientoTransversal",
                   "Longitudinal", "Transversal", "Poros", "Gramaje",
                   "Espesor", "Compresion", "Perforacion", "Permeabilidad",
                   "Piramidal")
        campos = ("toleranciaPrueba%s",
                  "toleranciaPrueba%sSup",
                  "estandarPrueba%s")
        for prueba in pruebas:
            for campo in campos:
                nombre_campo = campo % prueba
                valor = getattr(self, nombre_campo)
                setattr(cer, nombre_campo, valor)

cont, tiempo = print_verbose(cont, total, tiempo)

class ProductoVenta(SQLObject, PRPCTOO, Producto):
    # DONE: Hacer que se cachee en la tabla de históricos el stock histórico
    #       consultado y buscar ahí primero para no recalcular.
    class sqlmeta:
        fromDatabase = True
    #--------------------- lineaDeProduccionID = ForeignKey('LineaDeProduccion')
    #------------- camposEspecificosBalaID = ForeignKey('CamposEspecificosBala')
    #----------- camposEspecificosRolloID = ForeignKey('CamposEspecificosRollo')
    #----- camposEspecificosEspecialID = ForeignKey('CamposEspecificosEspecial',
    #----------------------------------------------------------- default = None)
    lineasDeVenta = MultipleJoin('LineaDeVenta')
    lineasDePedido = MultipleJoin('LineaDePedido')
    articulos = MultipleJoin('Articulo')
    camposEspecificos = MultipleJoin('CamposEspecificos')
    precios = MultipleJoin('Precio')
    historialesExistencias = MultipleJoin('HistorialExistencias')
    consumosAdicionales = RelatedJoin('ConsumoAdicional',
                        joinColumn='producto_venta_id',
                        otherColumn='consumo_adicional_id',
                        intermediateTable='consumo_adicional__producto_venta')
    historialesExistenciasA = MultipleJoin('HistorialExistenciasA')
    historialesExistenciasB = MultipleJoin('HistorialExistenciasB')
    historialesExistenciasC = MultipleJoin('HistorialExistenciasC')
    lineasDePresupuesto = MultipleJoin("LineaDePresupuesto")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        """
        Devuelve una cadena con el total de existencias, el total en A, B y
        C y el total por almacén; así como el PUID, código, nombre y
        descripción.
        """
        cad = self.get_puid()
        cad += " - %s (%s)\n" % (self.nombre, self.descripcion)
        cad += "  Existencias: %d bultos, A: %d; B: %d; C: %d.\n" % (
            self.get_existencias(contar_defectuosos = True),
            self.get_existencias_A(),
            self.get_existencias_B(),
            self.get_existencias_C())
        for a in Almacen.select(orderBy = "id"):
            cad += "    -> Almacén %s: %d bultos. A: %d; B: %d; C: %d\n" % (
                a.nombre,
                self.get_existencias(contar_defectuosos = True, almacen = a),
                self.get_existencias_A(almacen = a),
                self.get_existencias_B(almacen = a),
                self.get_existencias_C(almacen = a))
        cad += "  Stock: %s %s, A: %s; B: %s; C: %s.\n" % (
            utils.float2str(self.get_stock(contar_defectuosos = True)),
            self.get_str_unidad_de_venta(),
            utils.float2str(self.get_stock_A()),
            utils.float2str(self.get_stock_B()),
            utils.float2str(self.get_stock_C()))
        for a in Almacen.select(orderBy = "id"):
            stock_A = self.get_stock_A(almacen = a)
            if stock_A is None: stock_A = 0.0
            stock_B = self.get_stock_B(almacen = a)
            if stock_B is None: stock_B = 0.0
            stock_C = self.get_stock_C(almacen = a)
            if stock_C is None: stock_C = 0.0
            cad += "    -> Almacén %s: %s %s. A: %s; B: %s; C: %s\n" % (
                a.nombre,
                utils.float2str(self.get_stock(contar_defectuosos = True,
                                               almacen = a)),
                self.get_str_unidad_de_venta(),
                utils.float2str(stock_A),
                utils.float2str(stock_B),
                utils.float2str(stock_C))
        return cad

    def get_puid(self):
        """
        Devuelve una *cadena* con PV: y el ID del producto.
        puid viene a ser como ProductoUnicoID (un ID único para cada producto
        cuyo tipo de objeto se diferencia por la cadena que antecede a los :).
        """
        return "PV:%d" % self.id

    def get_proveedor(self):
        # No es producto de compra. Devuelvo None.
        res = None  # PLAN: Tal vez sería interesante devolver el
                    # proveedor de la materia prima de la que sale
                    # el producto.
        return res

    proveedor = property(get_proveedor)

    def calcular_razon_bultos(self):
        """
        Devuelve la cantidad de producto que contiene un bulto en las unidades
        del producto.
        Devuelve None si no se puede determinar. Lanza una excepción si el
        tipo de producto no está soportado.
        """
        if self.es_bala():
            res = None  # Peso de una bala es variable.
        elif self.es_bala_cable():
            res = None  # El peso también es variable.
        elif self.es_bigbag():
            res = None  # Peso variable.
        elif self.es_bolsa() or self.es_caja(): # Por compatibilidad, cada
            # vez que preguntemos si un producto "es" bolsa nos estamos
            # refiriendo en realidad a si el producto es fibra de cemento
            # embolsada. Por eso no devuelvo el peso de *una* bolsa, sino el
            # peso de un bulto del producto, es decir, una caja.
            ceb = self.camposEspecificosBala
            pesobolsa = ceb.gramosBolsa / 1000.0  # @UnusedVariable
            pesocaja = ceb.pesobolsa * ceb.bolsasCaja
            res = pesocaja  # El bulto es la caja.
        elif self.es_especial():    # El número que devolverá puede variar
            # con el tiempo, porque depende exclusivamente de la información
            # que dé el usuario sobre cuántos bultos y cantidad de producto
            # hay. Lo único que se asegura es que el sistema no cambiará esta
            # cifra con la variación de existencias a no ser que sea el
            # usuario el que específicamente varíe alguna de las dos
            # cantidades en la ventana de productos especiales.
            cee = self.camposEspecificosEspecial
            try:
                res = cee.stock / cee.existencias
            except ZeroDivisionError:
                res = None  # No se puede determinar si tiene 0 bultos.
        elif self.es_fibra():
            res = None  # El peso de la fibra es variable en cada bulto.
        elif self.es_rollo():
            res = None  # El peso de los rollos es variable en cada bulto.
        elif self.es_rollo_c():
            res = None  # El peso es variable en cada bulto.
        else:
            raise ValueError, "pclases::calcular_razon_bultos -> Tipo de "\
                              "producto no soportado. PUID: %s" % (
                                self.get_puid())
        return res

    def buscar_produccion_bultos(self, fecha0, fecha1):
        """
        Busca la producción del producto del producto entre las fechas
        recibidas.
        AMBAS INCLUIDAS.
        """
        pv = self
        res = 0
        if (pv.es_rollo() or pv.es_bala() or pv.es_bigbag() or pv.es_caja()):
            PDP = ParteDeProduccion
            articulos = Articulo.select(AND(PDP.q.fecha >= fecha0,
                                PDP.q.fecha <= fecha1,
                                Articulo.q.productoVentaID == self.id,
                                Articulo.q.parteDeProduccionID == PDP.q.id))
            res += articulos.count()
            # Y ahora los "magic_bultos" (TM), que son los artículos sin parte
            # de producción que se han creado en el sistema por arte de
            # biribirloque y vete tú a saber por qué.
            magic_articulos = Articulo.select(AND(
                                    Articulo.q.productoVentaID == self.id,
                                    Articulo.q.parteDeProduccionID == None))
            res += len([a for a in magic_articulos
                        if a.fecha_fabricacion >= fecha0
                        and a.fecha_fabricacion <= fecha1+mx.DateTime.oneDay])
        elif pv.es_bala_cable():
            BC = BalaCable
            balas_cable = BC.select(AND(BC.q.fechahora >= fecha0,
                                BC.q.fechahora <= fecha1 + mx.DateTime.oneDay,
                                BC.q.id == Articulo.q.balaCableID,
                                Articulo.q.productoVentaID == self.id))
                # Le sumo un día porque una bala de cable del día 1/1/07 23:59
                # debe entrar en el día 1/1/07 (00:00), y como
                # 1/1/07 23:59 > 1/1/07 00:00 debo comparar con la fecha
                # 2/2/07 00:00
            res = balas_cable.count()
        elif pv.es_rolloC():
            RC = RolloC
            rollos_c = RC.select(AND(RC.q.fechahora >= fecha0,
                                     RC.q.fechahora <= fecha1
                                        + mx.DateTime.oneDay,
                                     RC.q.id == Articulo.q.balaCableID,
                                     Articulo.q.productoVentaID == self.id))
                # Le sumo un día porque una rollo C del día 1/1/07 23:59 debe
                # entrar en el día 1/1/07 (00:00), y como
                # 1/1/07 23:59 > 1/1/07 00:00 debo comparar con la fecha
                # 2/2/07 00:00
            res = rollos_c.count()
        else:
            myprint("pclases::ProductoVenta: ProductoVenta ID %d no es bala [cable], rollo [C] ni bigbag." % (pv.id))
        return res

    def buscar_produccion_cantidad(self, fecha0, fecha1):
        """
        Busca la producción del producto del producto entre las fechas
        recibidas.
        AMBAS INCLUIDAS.
        """
        pv = self
        res = 0.0
        PDP = ParteDeProduccion
        if pv.es_bala():
            balas = Bala.select(AND(Bala.q.id == Articulo.q.balaID,
                                    Articulo.q.productoVentaID == self.id,
                                    Articulo.q.parteDeProduccionID == PDP.q.id,
                                    PDP.q.fecha >= fecha0,
                                    PDP.q.fecha <= fecha1))
            if balas.count() > 0:
                res = balas.sum("pesobala")
            else:
                res = 0.0
            # Y ahora los "magic_bultos" (TM), que son los artículos sin
            # parte de producción que se han creado en el sistema por arte de
            # biribirloque y vete tú a saber por qué.
            magic_articulos = Articulo.select(AND(
                Articulo.q.productoVentaID == self.id,
                Articulo.q.parteDeProduccionID == None))
            res += sum([a.peso for a in magic_articulos
                        if a.fecha_fabricacion >= fecha0
                        and a.fecha_fabricacion <= fecha1 + mx.DateTime.oneDay])
        elif pv.es_bigbag():
            bigbags = Bigbag.select(AND(
                            Bigbag.q.id == Articulo.q.bigbagID,
                            Articulo.q.productoVentaID == self.id,
                            Articulo.q.parteDeProduccionID == PDP.q.id,
                            PDP.q.fecha >= fecha0,
                            PDP.q.fecha <= fecha1))
            if bigbags.count() > 0:
                res = bigbags.sum("pesobigbag")
            else:
                res = 0.0
            # Y ahora los "magic_bultos" (TM), que son los artículos sin parte
            # de producción que se han creado en el sistema por arte de
            # biribirloque y vete tú a saber por qué.
            magic_articulos = Articulo.select(AND(
                                Articulo.q.productoVentaID == self.id,
                                Articulo.q.parteDeProduccionID == None))
            res += sum([a.peso for a in magic_articulos
                        if a.fecha_fabricacion >= fecha0
                        and a.fecha_fabricacion <= fecha1 + mx.DateTime.oneDay])
        elif pv.es_caja():
            cajas = Caja.select(AND(
                            Caja.q.id == Articulo.q.cajaID,
                            Articulo.q.productoVentaID == self.id,
                            Articulo.q.parteDeProduccionID == PDP.q.id,
                            PDP.q.fecha >= fecha0,
                            PDP.q.fecha <= fecha1))
            res = sum([c.peso for c in cajas])
            # Y ahora los "magic_bultos" (TM), que son los artículos sin parte
            # de producción que se han creado en el sistema por arte de
            # biribirloque y vete tú a saber por qué.
            magic_articulos = Articulo.select(AND(
                                Articulo.q.productoVentaID == self.id,
                                Articulo.q.parteDeProduccionID == None))
            res += sum([a.peso for a in magic_articulos
                        if a.fecha_fabricacion >= fecha0
                        and a.fecha_fabricacion <= fecha1 + mx.DateTime.oneDay])
        elif pv.es_rollo():
            PDP = ParteDeProduccion
            pdps = PDP.select(AND(PDP.q.fecha >= fecha0, PDP.q.fecha <= fecha1))
            for pdp in pdps:
                articulos_de_producto_en_pdp = [a for a in pdp.articulos
                                                if a.productoVenta == pv]
                res += sum([a.superficie for a in articulos_de_producto_en_pdp])
            # Y ahora los "magic_bultos" (TM), que son los artículos sin parte
            # de producción que se han creado en el sistema por arte de
            # biribirloque y vete tú a saber por qué.
            magic_articulos = Articulo.select(AND(
                                Articulo.q.productoVentaID == self.id,
                                Articulo.q.parteDeProduccionID == None))
            res += sum([a.superficie for a in magic_articulos
                        if a.fecha_fabricacion >= fecha0
                        and a.fecha_fabricacion <= fecha1 + mx.DateTime.oneDay])
        elif pv.es_bala_cable():
            BC = BalaCable
            balas_cable = BC.select(AND(
                            BC.q.fechahora >= fecha0,
                            BC.q.fechahora <= fecha1 + mx.DateTime.oneDay,
                            BC.q.id == Articulo.q.balaCableID,
                            Articulo.q.productoVentaID == self.id))
                # Le sumo un día porque una bala de cable del día 1/1/07
                # 23:59 debe entrar en el día 1/1/07 (00:00), y como
                # 1/1/07 23:59 > 1/1/07 00:00 debo comparar con la
                # fecha 2/2/07 00:00
            if balas_cable.count():
                res = balas_cable.sum("peso")
            else:
                res = 0.0
        elif pv.es_rollo_c():
            RC = RolloC
            balas_cable = RC.select(AND(
                            RC.q.fechahora >= fecha0,
                            RC.q.fechahora <= fecha1 + mx.DateTime.oneDay,
                            RC.q.id == Articulo.q.balaCableID,
                            Articulo.q.productoVentaID == self.id))
                # Le sumo un día porque una bala de cable del día 1/1/07
                # 23:59 debe entrar en el día 1/1/07 (00:00), y como
                # 1/1/07 23:59 > 1/1/07 00:00 debo comparar con la
                # fecha 2/2/07 00:00
            if balas_cable.count():
                res = balas_cable.sum("peso")
            else:
                res = 0.0
        else:
            myprint("pclases::ProductoVenta: ProductoVenta ID %d no es bala [cable], rollo [C] ni bigbag ni caja de fibra de cemento." % (pv.id))
        return res

    def buscar_consumos_balas(self, fecha0, fecha1):
        """
        Devuelve una lista de balas del producto consumidas entre las fechas a
        partir de las fechas de las partidas de carga.
        """
        ## XXX: Muchísimo más rápido si lo hacemos a "medio nivel". Ni SQL a
        ## pelo (rapidísimo) ni el alto nivel de SQLObject recorriendo
        ## objetos uno a uno. Mucho mejor con la consulta en SQLBuilder:
        res = Bala.select(AND(Bala.q.id == Articulo.q.balaID,
                              Bala.q.partidaCargaID == PartidaCarga.q.id,
                              Articulo.q.productoVentaID == self.id,
                              PartidaCarga.q.fecha > fecha0,
                              PartidaCarga.q.fecha < fecha1 + mx.DateTime.oneDay))
        return res
        # return list(res)

    def buscar_consumos_bultos(self, fecha0, fecha1):
        """
        Devuelve los consumos del producto entre las fechas proporcionadas.
        """
        return self.buscar_consumos_balas(fecha0, fecha1).count()

    def buscar_consumos_cantidad(self, fecha0, fecha1):
        """
        devuelve los consumos del producto entre las fechas proporcionadas.
        ambas incluidas.
        """
        consumos = self.buscar_consumos_balas(fecha0, fecha1)
        if consumos.count() > 0:
            return consumos.sum('pesobala')
        else:
            return 0.0

    def _buscar_albaranes_entre_fechas(self, fecha0, fecha1, almacen = None,
            contar_transferencias_entre_almacenes_como_salidas = False):
        """
        Busca albaranes entre dos fechas. AMBAS INCLUIDAS.
        Devuelve un SelectResults.
        Si almacen es distinto de None solo devuelve los albaranes de la
        mercancía que salió de ese almacén («almacenOrigen» es «almacen»)
        *pero no fueron a otro* («almacenDestino» debe ser None). ¿"Porcuá"?
        Porque queremos salidas _efectivas_ de almacén[1]. De cualquier modo
        se puede cambiar el comportamiento con el parámetro
        «contar_transferencias_entre_almacenes_como_salidas».

        [1] Ojo. Nos interesa en el caso particular en que se invoca esta
            rutina (HistorialExistencias.test). En condiciones normales, una
            salida de un almacén concreto debería ser también una
            transferencia entre almacenes.
        """
        clauses = AND(AlbaranSalida.q.fecha >= fecha0,
                      AlbaranSalida.q.fecha <= fecha1,
                      Articulo.q.albaranSalidaID == AlbaranSalida.q.id,
                      Articulo.q.productoVentaID == self.id)
        if almacen:
            try:
                almacen_id = almacen.id
            except:
                almacen_id = almacen
            clauses = AND(clauses,
                          AlbaranSalida.q.almacenOrigen == almacen_id)
            if not contar_transferencias_entre_almacenes_como_salidas:
                clauses = AND(clauses,
                              AlbaranSalida.q.almacenDestino == None)
        albs = AlbaranSalida.select(clauses, distinct = True)
        return albs

    def buscar_ventas_bultos(self, fecha0, fecha1, incluir_internos = False,
                             almacen = None):
        """
        Ventas (salidas de almacén) en bultos entre fechas. AMBAS INCLUIDAS.
        Las ventas se determinan partiendo de albaranes de salida. Por
        tanto se consideran ventas todas las salidas de almacén, sean
        de albaranes internos o no, facturados y no facturados.
        La fecha de cada salida será la del albarán al que corresponda,
        independientemente de la fecha de la factura -si la tiene- o del
        pedido.
        """
        bultos = 0
        albs = self._buscar_albaranes_entre_fechas(fecha0, fecha1, almacen)
        for alb in albs:
            if not incluir_internos and alb.es_interno():
                continue
            articulos_del_pv = Articulo.select(AND(
                                Articulo.q.productoVentaID == self.id,
                                Articulo.q.albaranSalidaID == alb.id))
            bultos += articulos_del_pv.count()
        return bultos

    def buscar_ventas_cantidad(self, fecha0, fecha1, incluir_internos = False,
                               almacen = None):
        """
        Ventas (salidas de almacén) en cantidad en unidades del producto
        entre fechas. AMBAS INCLUIDAS.
        Las ventas se determinan partiendo de albaranes de salida. Por
        tanto se consideran ventas todas las salidas de almacén, sean
        de albaranes internos o no, facturados y no facturados.
        La fecha de cada salida será la del albarán al que corresponda,
        independientemente de la fecha de la factura -si la tiene- o del
        pedido.
        OJO: Cuento las existencias que realmente salieron en albarán, no
        las reflejadas (y facturadas) en las LDV.
        ACTUALIZACIÓN: incluir_internos es False por defecto para no
        contar los albaranes de partidas de carga que no entran en las
        fechas. El cálculo se debe hacer entonces en dos llamadas para
        conocer exactamente las existencias de un producto en una fecha
        determinada. La primera a las ventas y la segunda a los consumos.
        Así, las existencias en fecha1 - producción entre fecha0 y fecha1
        + ventas entre fecha0 y fecha1 (este método) + consumos entre fecha0
        y fecha1 deben cuadrar _exactamente_ con las existencias en fecha0.
        """
        # PLAN: optimizar
        # TODO: Tengo que pensarlo un poco... ¿sería necesario tratar los
        # productos especiales? ¿Y los que tienen el control por software a
        # False?
        cantidad = 0.0
        albs = self._buscar_albaranes_entre_fechas(fecha0, fecha1, almacen)
        for alb in albs:
            if incluir_internos or not alb.es_interno():
                for a in alb.articulos:
                    if a.productoVenta == self:
                        if (a.es_bala() or a.es_bala_cable()
                            or a.es_bigbag() or a.es_rolloC() or a.es_caja()):
                            cantidad += a.peso
                        elif a.es_rollo() or a.es_rollo_defectuoso():
                            cantidad += a.superficie
                        else:
                            myprint("pclases::ProductoVenta::buscar_ventas_cant"\
                                  "idad -> Articulo ID %d de albarán ID %d no"\
                                  " es bala [cable], bigbag, caja ni rollo ["\
                                  "{defectuoso,C}]." % (a.id, alb.id))
        # Y ahora los abonos:
        ## ACTUALIZACIÓN: Los abonos no se cuentan. Si un producto está abonado, tiene el albaranSalida a None. Aunque se
        ## haya abonado y vendido varias veces. Si tiene el albaranSalida != None es que no está en almacén, independientemente
        ## de si ha sido abonado anteriormente o no.
        #for albaran_abono in AlbaranDeEntradaDeAbono.select(AND(AlbaranDeEntradaDeAbono.q.fecha >= fecha0,
        #                                                        AlbaranDeEntradaDeAbono.q.fecha <= fecha1)):
        #    for ldd in albaran_abono.lineasDeDevolucion:
        #        a = ldd.articulo
        #        if a.productoVenta == self:
        #            if a.es_rollo() or a.es_rollo_defectuoso():
        #                cantidad -= a.superficie
        #            elif a.es_bala() or a.es_bigbag() or a.es_bala_cable():
        #                cantidad -= a.peso
        #            else:
        #                print "pclases::ProductoVenta::buscar_ventas_cantidad -> Articulo ID %d de LineaDeDevolucion ID %d no es bala [cable], bigbag ni rollo [defectuoso]." % (a.id, ldd.id)
        return cantidad

    def set_precioDefecto(self, v):
        self.preciopordefecto = v

    # Para compatibilizar todo lo posible los campos de productos(Venta|Compra)
    precioDefecto = property(lambda o: o.preciopordefecto,
                             set_precioDefecto)

    def es_rollo(self):
        """
        Devuelve True si el producto se empaqueta
        como rollos PERO no es de categoría «C».
        """
        return self.camposEspecificosRollo != None and not self.es_rollo_c()

    def es_bigbag(self):
        """
        Devuelve si el producto se empaqueta como BigBag.
        """
        # NOTA: Desgraciadamente, por el momento sólo es posible discernir el
        # tipo de producto "fibra de cemento" si la descripción contiene GEOCEM.
        # TODO: Esto no es así. La fibra embolsada también contiene "GEOCEM".
        # Hay que buscar una forma mejor de determinarlo. Esto es una chapuza.
        res = "GEOCEM" in self.descripcion and not self.es_caja()
        # HARCODED: Casos especiales (SIKACIM)
        if not res:
            res = "SIKACIM" in self.descripcion
        return res

    def es_bala_cable(self):
        """
        Devuelve True si es fibra de cable.
        Se distingue mirando el campo "reciclada".
        """
        return bool(self.camposEspecificosBala
                    and self.camposEspecificosBala.reciclada)

    def es_rollo_c(self):
        """
        Devuelve True si el producto es de Geotextiles «C».
        """
        return self.camposEspecificosRollo and self.camposEspecificosRollo.c

    es_rolloC = es_rollo_c

    def es_clase_c(self):
        return self.es_bala_cable() or self.es_rollo_c()

    def es_bala(self):
        return (self.camposEspecificosBala != None and not self.es_bigbag()
                and not self.es_bala_cable() and not self.es_caja())

    def es_especial(self):
        """
        Devuelve True si el producto es un artículo especial (sin balas ni
        rollos asociados).
        """
        return self.camposEspecificosEspecialID != None

    def es_caja(self):
        """
        Devuelve True si el producto es de la línea de embolsado de fibra de
        cemento.
        """
        # TODO: De momento lo vamos a hacer así, con el campo de gramos por
        # bolsa. Pero en realidad debería mirar la relación con la línea de
        # producción. Lo que pasa es que hasta el momento se está usando
        # la ventana de fibra y los productos de embolsado están relacionados
        # con la línea de fibra en vez de con la suya.
        try:
            res = self.camposEspecificosBala.gramosBolsa # (!= None ^ != 0)
        except AttributeError:  # Ni siquiera tiene camposEspecíficos de fibra
            res = False
        return res

    es_bolsa = es_caja  # Por compatibilidad con versión 2.9.96

    def __get_articulos_no_bala_en_almacen_hasta(self,
                                                 hasta,
                                                 contar_defectuosos = False):
        """
        Devuelve los artículos en almacén hasta (incluida)
        la fecha dada. No sirve para balas porque no tiene
        en cuenta las partidas de carga.
        """
        # DONE: contar_defectuosos no se usa todavía porque realmente no se
        #       cuentan. Para contarlos habría que incluir una subconsulta que
        #       usara la tabla rollo_defectuoso. De todas formas lo cuento
        #       aparte, ya que no los puedo multiplicar por los metros
        #       cuadrados del producto.
        #       Lo segundo es cierto: no puede multiplicarse por lo m², pero
        #       lo primero era una cochina mentira. Entraban en el primer
        #       operando del OR:
        #           tenían parte de producción IN partes_antes_de_fecha.
        #       Lo mismo es aplicable a los nuevos rollos C. No son
        #       multiplicables por la superficie del artículo, y además
        #       no prodecen de partes de producción, así que se ignoran aquí.
        fecha = hasta.strftime('%Y-%m-%d')
        fecha_limite_para_comparaciones_con_fechahoras = (hasta
                                    + mx.DateTime.oneDay).strftime('%Y-%m-%d')
        albaranes_antes_de_fecha = """
            SELECT albaran_salida.id
            FROM albaran_salida
            WHERE albaran_salida.fecha <= '%s'
        """ % (fecha)
        partes_antes_de_fecha = """
            SELECT parte_de_produccion.id
            FROM parte_de_produccion
            WHERE parte_de_produccion.fecha <= '%s'
        """ % (fecha)
        articulos_de_rollos_anteriores_a_fecha = """
            SELECT rollo.id
            FROM rollo
            WHERE rollo.fechahora < '%s'
        """ % (fecha_limite_para_comparaciones_con_fechahoras)
        articulos_de_balas_anteriores_a_fecha = """
            SELECT bala.id
            FROM bala
            WHERE bala.fechahora < '%s'
        """ % (fecha_limite_para_comparaciones_con_fechahoras)
            # Porque fechahora contiene fecha y hora, y p.ej.:
            # 1/1/2006 10:23 no es <= 1/1/2006 0:00 (que sería la
            # fecha recibida).
        articulos_de_bigbags_anteriores_a_fecha = """
            SELECT bigbag.id
            FROM bigbag
            WHERE bigbag.fechahora < '%s'
        """ % (fecha_limite_para_comparaciones_con_fechahoras)
        articulos_de_cajas_anteriores_a_fecha = """
            SELECT caja.id
            FROM caja
            WHERE caja.fechahora < '%s'
        """ % (fecha_limite_para_comparaciones_con_fechahoras)
        if contar_defectuosos:
            clausula_defectuosos = ""
        else:
            clausula_defectuosos = "AND rollo_defectuoso_id IS NULL"
        parte_where = """
        articulo.producto_venta_id = %d
        AND (articulo.parte_de_produccion_id IN (%s)
             OR (articulo.parte_de_produccion_id IS NULL
                 AND (articulo.rollo_id IN (%s AND articulo.rollo_id = rollo.id)
                      OR articulo.bala_id IN (%s AND articulo.bala_id = bala.id)
                      OR articulo.bigbag_id IN (%s AND articulo.bigbag_id = bigbag.id)
                      OR articulo.caja_id IN (%s AND articulo.caja_id = caja.id)
                     )
                )
            )
        AND (articulo.albaran_salida_id IS NULL
             OR articulo.albaran_salida_id NOT IN (%s))
        %s
        """ % (self.id,
               partes_antes_de_fecha,
               articulos_de_rollos_anteriores_a_fecha,
               articulos_de_balas_anteriores_a_fecha,
               articulos_de_bigbags_anteriores_a_fecha,
               articulos_de_cajas_anteriores_a_fecha,
               albaranes_antes_de_fecha,
               clausula_defectuosos)
        articulos_en_almacen = Articulo.select(parte_where)
        return articulos_en_almacen

    def __OLD_get_balas_hasta(self, hasta):
        """
        Devuelve una consulta de balas en almacén
        hasta (incluida) la fecha proporcionada.
        """
        fecha = hasta.strftime('%Y-%m-%d')
        fecha_limite_para_comparaciones_con_fechahoras = (hasta
                                    + mx.DateTime.oneDay).strftime('%Y-%m-%d')
        albaranes_de_salida_antes_de_fecha = """
            SELECT albaran_salida.id
            FROM albaran_salida
            WHERE albaran_salida.fecha <= '%s'
        """ % (fecha)
        balas_vendidas_antes_de_fecha = """
            SELECT bala_id
            FROM articulo
            WHERE articulo.bala_id IS NOT NULL
                AND articulo.albaran_salida_id IN (%s)
        """ % (albaranes_de_salida_antes_de_fecha)
        partes_de_balas_antes_de_fecha = """
            SELECT id
            FROM parte_de_produccion
            WHERE parte_de_produccion.observaciones LIKE '%%;%%;%%;%%;%%;%%'
                  AND fecha <= '%s'
        """ % (fecha)
        balas_de_partes_de_balas_antes_de_fecha = """
            SELECT bala_id
              FROM articulo
             WHERE articulo.bala_id IS NOT NULL
               AND (articulo.parte_de_produccion_id IN (%s)
                    OR (articulo.parte_de_produccion_id IS NULL
                        AND (articulo.bala_id IN
                                (SELECT bala.id
                                   FROM bala
                                  WHERE bala.fechahora < '%s'
                                    AND articulo.bala_id = bala.id
                                )
                            )
                       )
                   )
        """ % (partes_de_balas_antes_de_fecha,
               fecha_limite_para_comparaciones_con_fechahoras)
        partes_de_rollos_antes_de_fecha = """
          SELECT parte_de_produccion.id
            FROM parte_de_produccion
           WHERE parte_de_produccion.fecha <= '%s'
             AND parte_de_produccion.observaciones NOT LIKE '%%;%%;%%;%%;%%;%%'
        """ % (fecha)
        rollos_de_articulos_antes_de_fecha = """
            SELECT articulo.rollo_id
            FROM articulo
            WHERE articulo.parte_de_produccion_id IN (%s)
        """ % (partes_de_rollos_antes_de_fecha)
        partidas_de_rollos_antes_de_fecha = """
            SELECT rollo.partida_id
            FROM rollo
            WHERE rollo.id IN (%s)
            GROUP BY rollo.partida_id
        """ % (rollos_de_articulos_antes_de_fecha)
        partidas_de_carga_en_partidas_antes_de_fecha = """
            SELECT partida.partida_carga_id
            FROM partida
            WHERE partida.id IN (%s)
        """ % (partidas_de_rollos_antes_de_fecha)
        partidas_de_carga_usadas_antes_de_fecha = """
            SELECT partida_carga.id
            FROM partida_carga
            WHERE partida_carga.id IN (%s)
        """ % (partidas_de_carga_en_partidas_antes_de_fecha)
        balas_usadas_antes_de_fecha = """
            SELECT bala.id
            FROM bala
            WHERE bala.partida_carga_id IN (%s)
        """ % (partidas_de_carga_usadas_antes_de_fecha)
        balas_del_producto = """
            SELECT articulo.bala_id
            FROM articulo
            WHERE articulo.producto_venta_id = %d
                AND articulo.bala_id IS NOT NULL
        """ % (self.id)
        query = """
            bala.id IN (%s)
            AND bala.id IN (%s)
            AND bala.id NOT IN (%s)
            AND bala.id NOT IN (%s)
        """ % (balas_de_partes_de_balas_antes_de_fecha,
               balas_del_producto,
               balas_vendidas_antes_de_fecha,
               balas_usadas_antes_de_fecha)
        balas = Bala.select(query)
        #ids1 = [b.id for b in balas]
        #ids2 = [a.bala.id for a in Articulo.select(""" articulo.bala_id IN (SELECT bala.id
        #                                                                        FROM bala
        #                                                                        WHERE bala.partida_carga_id IS NULL)
        #                                                   AND articulo.albaran_salida_id IS NULL
        #                                                   AND articulo.producto_venta_id = %d""" % self.id)]
        #for id in ids1:
        #    if id not in ids2:
        #        print id,
        #print
        #for id in ids2:
        #    if id not in ids1:
        #        print id,
        #print
        # NOTA: Las balas que no coinciden entre ambas consultas se deben a balas que han entrado en los
        # cuartos pero no se han llegado a consumir porque las partidas donde se gastan tienen fecha
        # superior al tope. Esto es así porque partidaCarga.fechahora NO ES FIABLE (antes de noviembre, todas
        # tienen la misma fecha de carga por haberse metido esta tabla con posterioridad al diseño de la BD).
        return balas

    def __get_balas_hasta(self, hasta, almacen = None):
        """
        Devuelve una consulta de balas en almacén
        hasta (incluida) la fecha proporcionada.
        """
        if almacen != None:
            return self.__get_balas_hasta_por_almacen(hasta, almacen = almacen)
        fecha = hasta.strftime('%Y-%m-%d')
        fecha_limite_para_comparaciones_con_fechahoras = (hasta
                                    + mx.DateTime.oneDay).strftime('%Y-%m-%d')
        ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
        try:
            Bala._connection.query("""
                DROP TABLE tmp_balas_vendidas_despues_de_fecha_o_no_vendidas,
                           tmp_balas_de_partes_de_balas_antes_de_fecha,
                           tmp_balas_usadas_despues_de_fecha_o_no_usadas,
                           tmp_balas_del_producto;""")
        except:
            pass    # Si existen en mi sesión las borro. Y si no, no pasa nada.
        ## ## ## PRODUCCIÓN  ## ## ## ## ## ## ## ## ## ##
        partes_de_balas_antes_de_fecha = """
            SELECT id
            FROM parte_de_produccion
            WHERE parte_de_produccion.observaciones LIKE '%%;%%;%%;%%;%%;%%'
                  AND fecha <= '%s'
        """ % (fecha)
        balas_de_partes_de_balas_antes_de_fecha = """
            SELECT bala_id
            INTO TEMP tmp_balas_de_partes_de_balas_antes_de_fecha
            FROM articulo
            WHERE articulo.bala_id IS NOT NULL
                  AND (articulo.parte_de_produccion_id IN (%s)
                       OR (articulo.parte_de_produccion_id IS NULL
                           AND (articulo.bala_id IN (
                                    SELECT bala.id
                                    FROM bala
                                    WHERE bala.fechahora < '%s'
                                      AND articulo.bala_id = bala.id
                                                    )
                               )
                          )
                      );
        """ % (partes_de_balas_antes_de_fecha,
               fecha_limite_para_comparaciones_con_fechahoras)
        ## ## ## VENTAS # ## ## ## ## ## ## ## ## ## ## ##
        albaranes_de_salida_despues_de_fecha = """
            SELECT albaran_salida.id
            FROM albaran_salida
            WHERE albaran_salida.fecha > '%s'
--              AND es_interno(albaran_salida.id) = FALSE
        """ % (fecha)
        balas_vendidas_despues_de_fecha_o_no_vendidas = """
            SELECT bala_id
            INTO TEMP tmp_balas_vendidas_despues_de_fecha_o_no_vendidas
            FROM articulo
            WHERE articulo.bala_id IS NOT NULL
                  AND articulo.producto_venta_id = %d
                  AND (articulo.albaran_salida_id IN (%s)
                       OR articulo.albaran_salida_id IS NULL);
        """ % (self.id, albaranes_de_salida_despues_de_fecha)
        ## ## ## CONSUMOS ## ## ## ## ## ## ## ## ## ## ##
        partes_de_rollos_despues_de_fecha = """
            SELECT parte_de_produccion.id
            FROM parte_de_produccion
            WHERE parte_de_produccion.fecha > '%s'
                AND parte_de_produccion.observaciones NOT LIKE '%%;%%;%%;%%;%%;%%'
        """ % (fecha)
        rollos_de_articulos_despues_de_fecha = """
            SELECT articulo.rollo_id
            FROM articulo
            WHERE articulo.parte_de_produccion_id IN (%s)
        """ % (partes_de_rollos_despues_de_fecha)
        partidas_de_rollos_despues_de_fecha = """
            SELECT rollo.partida_id
            FROM rollo
            WHERE rollo.id IN (%s)
            GROUP BY rollo.partida_id
        """ % (rollos_de_articulos_despues_de_fecha)
        partidas_de_carga_en_partidas_despues_de_fecha = """
            SELECT partida.partida_carga_id
            FROM partida
            WHERE partida.id IN (%s)
        """ % (partidas_de_rollos_despues_de_fecha)
        partidas_de_carga_usadas_despues_de_fecha = """
            SELECT partida_carga.id
            FROM partida_carga
            WHERE partida_carga.id IN (%s)
        """ % (partidas_de_carga_en_partidas_despues_de_fecha)
        # PLAN: Tal vez esta subconsulta chorretosa que mezca SQL y
        #       SQLObject se pueda optimizar:
        ids_pcs_sin_prod = [pc.id for pc
                            in PartidaCarga.select(
                                PartidaCarga.q.fecha > hasta)
                            if len(pc._get_partes_partidas()) == 0]
        if len(ids_pcs_sin_prod) > 0:
            partidas_de_carga_sin_produccion = ", ".join(
                                        map(str, map(int, ids_pcs_sin_prod)))
        else:
            partidas_de_carga_sin_produccion = "-1" # No hay IDs -1, así que
            # es como si no estuviera la rama OR (pero algo hay que poner).
        # print partidas_de_carga_sin_produccion
        balas_usadas_despues_de_fecha_o_no_usadas = """
            SELECT bala.id AS bala_id
            INTO TEMP tmp_balas_usadas_despues_de_fecha_o_no_usadas
            FROM bala, articulo
            WHERE bala.id = articulo.bala_id
              AND articulo.bala_id IS NOT NULL
              AND articulo.producto_venta_id = %d
              AND (bala.partida_carga_id IN (%s)
                   OR bala.partida_carga_id IN (%s)
                   OR bala.partida_carga_id IS NULL);
        """ % (self.id, partidas_de_carga_usadas_despues_de_fecha,
               partidas_de_carga_sin_produccion)
        ## ## ## BALAS DEL PRODUCTO # ## ## ## ## ## ## ##
        balas_del_producto = """
            SELECT articulo.bala_id
            INTO TEMP tmp_balas_del_producto
            FROM articulo
            WHERE articulo.producto_venta_id = %d
                AND articulo.bala_id IS NOT NULL ;
        """ % (self.id)
        ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
        # print 1
        Bala._connection.query(balas_vendidas_despues_de_fecha_o_no_vendidas)
        # print 2
        Bala._connection.query(balas_de_partes_de_balas_antes_de_fecha)
        # print 3
        Bala._connection.query(balas_usadas_despues_de_fecha_o_no_usadas)
        # print 4
        Bala._connection.query(balas_del_producto)
        # print 5
        ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
        query = """ id IN
            (SELECT bala.id
               FROM bala,
                    tmp_balas_del_producto p,
                    tmp_balas_de_partes_de_balas_antes_de_fecha produccion,
                    tmp_balas_vendidas_despues_de_fecha_o_no_vendidas,
                    tmp_balas_usadas_despues_de_fecha_o_no_usadas
              WHERE bala.id = p.bala_id
                AND bala.id = produccion.bala_id
                AND bala.id
                    = tmp_balas_vendidas_despues_de_fecha_o_no_vendidas.bala_id
                AND bala.id
                    = tmp_balas_usadas_despues_de_fecha_o_no_usadas.bala_id
               GROUP BY bala.id
            ) """
        balas = Bala.select(query)
        ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
        # TODO: ¿Faltan los abonos? Pues claro que faltan los abonos.
        return balas

    def __get_balas_hasta_por_almacen(self, hasta, almacen = None):
        """
        Devuelve una consulta de balas en almacén
        hasta (incluida) la fecha proporcionada para el almacén recibido.
        """
        if almacen == None:
            raise ValueError, "pclases.py::__get_balas_hasta_por_almacen:Deb"\
                              "e especificarse un almacén."
        fecha = hasta.strftime('%Y-%m-%d')
        fecha_limite_para_comparaciones_con_fechahoras = (hasta
            + mx.DateTime.oneDay).strftime('%Y-%m-%d')
        ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
        try:
            Bala._connection.query("""
                DROP TABLE tmp_balas_vendidas_despues_de_fecha_o_no_vendidas,
                           tmp_balas_de_partes_de_balas_antes_de_fecha,
                           tmp_balas_usadas_despues_de_fecha_o_no_usadas,
                           tmp_balas_del_producto;""")
        except:
            pass    # Si existen en mi sesión las borro. Y si no, no pasa nada.
        ## ## ## PRODUCCIÓN  ## ## ## ## ## ## ## ## ## ##
        if almacen == Almacen.get_almacen_principal():
            partes_de_balas_antes_de_fecha = """
            SELECT id
            FROM parte_de_produccion
            WHERE parte_de_produccion.observaciones LIKE '%%;%%;%%;%%;%%;%%'
              AND fecha <= '%s'
            """ % (fecha)
            balas_de_partes_de_balas_antes_de_fecha = """
            SELECT bala_id
            INTO TEMP tmp_balas_de_partes_de_balas_antes_de_fecha
            FROM articulo
            WHERE articulo.bala_id IS NOT NULL
              AND (articulo.parte_de_produccion_id IN (%s)
                   OR (articulo.parte_de_produccion_id IS NULL
                       AND (articulo.bala_id IN (SELECT bala.id
                                                 FROM bala
                                                 WHERE bala.fechahora < '%s'
                                                   AND articulo.bala_id = bala.id
                                                )
                           )
                      )
                  );
        """ % (partes_de_balas_antes_de_fecha,
               fecha_limite_para_comparaciones_con_fechahoras)
        else:
            balas_de_partes_de_balas_antes_de_fecha = """
                SELECT bala_id FROM articulo WHERE id < 0;
            """ # Es decir, ninguna. Solo se fabrica para el almacén ppal.
        ## ## ## VENTAS # ## ## ## ## ## ## ## ## ## ## ##
        albaranes_de_salida_despues_de_fecha = """
            SELECT albaran_salida.id
            FROM albaran_salida
            WHERE albaran_salida.fecha > '%s'
--              AND es_interno(albaran_salida.id) = FALSE
                AND albaran_salida.almacen_origen_id = %d
        """ % (fecha, almacen.id)
        balas_vendidas_despues_de_fecha_o_no_vendidas = """
            SELECT bala_id
            INTO TEMP tmp_balas_vendidas_despues_de_fecha_o_no_vendidas
            FROM articulo
            WHERE articulo.bala_id IS NOT NULL
                  AND articulo.producto_venta_id = %d
                  AND (articulo.albaran_salida_id IN (%s)
                       OR articulo.albaran_salida_id IS NULL);
        """ % (self.id, albaranes_de_salida_despues_de_fecha)
        ## ## ## CONSUMOS ## ## ## ## ## ## ## ## ## ## ##
        # Solo se consume desde el almacén ppal.
        if almacen == Almacen.get_almacen_principal():
            partes_de_rollos_despues_de_fecha = """
                SELECT parte_de_produccion.id
                FROM parte_de_produccion
                WHERE parte_de_produccion.fecha > '%s'
                  AND parte_de_produccion.observaciones NOT LIKE '%%;%%;%%;%%;%%;%%'
            """ % (fecha)
            rollos_de_articulos_despues_de_fecha = """
                SELECT articulo.rollo_id
                FROM articulo
                WHERE articulo.parte_de_produccion_id IN (%s)
            """ % (partes_de_rollos_despues_de_fecha)
            partidas_de_rollos_despues_de_fecha = """
                SELECT rollo.partida_id
                FROM rollo
                WHERE rollo.id IN (%s)
                GROUP BY rollo.partida_id
            """ % (rollos_de_articulos_despues_de_fecha)
            partidas_de_carga_en_partidas_despues_de_fecha = """
                SELECT partida.partida_carga_id
                FROM partida
                WHERE partida.id IN (%s)
            """ % (partidas_de_rollos_despues_de_fecha)
            partidas_de_carga_usadas_despues_de_fecha = """
                SELECT partida_carga.id
                FROM partida_carga
                WHERE partida_carga.id IN (%s)
            """ % (partidas_de_carga_en_partidas_despues_de_fecha)
            # PLAN: Tal vez esta subconsulta chorretosa que mezca SQL y
            #       SQLObject se pueda optimizar:
            ids_pcs_sin_prod = [pc.id for pc in PartidaCarga.select(PartidaCarga.q.fecha > hasta) if len(pc._get_partes_partidas()) == 0]
            if len(ids_pcs_sin_prod) > 0:
                partidas_de_carga_sin_produccion = ", ".join(map(str, map(int, ids_pcs_sin_prod)))
            else:
                partidas_de_carga_sin_produccion = "-1" # No hay IDs -1, así que
                # es como si no estuviera la rama OR (pero algo hay que poner).
            # print partidas_de_carga_sin_produccion
            balas_usadas_despues_de_fecha_o_no_usadas = """
                SELECT bala.id AS bala_id
                INTO TEMP tmp_balas_usadas_despues_de_fecha_o_no_usadas
                FROM bala, articulo
                WHERE bala.id = articulo.bala_id
                  AND articulo.bala_id IS NOT NULL
                  AND articulo.producto_venta_id = %d
                  AND (bala.partida_carga_id IN (%s)
                       OR bala.partida_carga_id IN (%s)
                       OR bala.partida_carga_id IS NULL);
            """ % (self.id, partidas_de_carga_usadas_despues_de_fecha, partidas_de_carga_sin_produccion)
        else:   # No es el almacén ppal. No se ha podido consumir desde ahí.
            balas_usadas_despues_de_fecha_o_no_usadas = """
                SELECT bala.id AS bala_id FROM bala WHERE id < 0;
                """
        ## ## ## BALAS DEL PRODUCTO # ## ## ## ## ## ## ##
        balas_del_producto = """
            SELECT articulo.bala_id
            INTO TEMP tmp_balas_del_producto
            FROM articulo
            WHERE articulo.producto_venta_id = %d
                AND articulo.bala_id IS NOT NULL ;
        """ % (self.id)
        ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
        # print 1
        Bala._connection.query(balas_vendidas_despues_de_fecha_o_no_vendidas)
        # print 2
        Bala._connection.query(balas_de_partes_de_balas_antes_de_fecha)
        # print 3
        Bala._connection.query(balas_usadas_despues_de_fecha_o_no_usadas)
        # print 4
        Bala._connection.query(balas_del_producto)
        # print 5
        ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
        query = """ id IN (SELECT bala.id
                           FROM bala,
                                tmp_balas_del_producto p,
                                tmp_balas_de_partes_de_balas_antes_de_fecha produccion,
                                tmp_balas_vendidas_despues_de_fecha_o_no_vendidas,
                                tmp_balas_usadas_despues_de_fecha_o_no_usadas
                           WHERE bala.id = p.bala_id
                                 AND bala.id = produccion.bala_id
                                 AND bala.id = tmp_balas_vendidas_despues_de_fecha_o_no_vendidas.bala_id
                                 AND bala.id = tmp_balas_usadas_despues_de_fecha_o_no_usadas.bala_id
                           GROUP BY bala.id
                           ) """
        balas = SQLlist(Bala.select(query))
        ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
        ## ## ## BALAS DEVUELTAS    # ## ## ## ## ## ## ##
        # Busco los abonos anteriores a esa fecha. Las balas de esos abonos
        # estaban en el almacén ya en la fecha «hasta» si el almacén de
        # destino del abono es el indicado.
        A = Articulo
        B = Bala
        AB = Abono
        LDD = LineaDeDevolucion
        balas_devueltas = B.select(AND(  # @UnusedVariable
                            A.q.balaID == B.q.id,
                            LDD.q.articuloID == A.q.id,
                            LDD.q.abonoID == AB.q.id,
                            AB.q.fecha <= hasta,
                            A.q.productoVentaID == self.id,
                            AB.q.almacenID == almacen.id))
        return balas

    def _agregar_a_historico(self, fecha, cantidad = None, bultos = None,
                             almacen = None):
        """
        Añade a la tabla de históricos la cantidad y bultos recibidas
        en la fecha dada para el producto correspondiente al objeto.
        Si cantidad o bultos es None, hace el recuento antes de
        agregar el registro.
        Si almacen es None se asume que es un histórico global *Y NO SE
        AÑADE NADA, PORQUE ES REQUISITO INDISPENSABLE QUE CADA REGISTRO
        VAYA CON UN ALMACÉN*, y como repartir por igual entre todos los
        almacenes no es realista, prefiero no agregar nada.
        En otro caso (esto es, se recibe un almacén) es el histórico para
        el almacén recibido.
        Devuelve el registro histórico (tanto recién creado como si ya
        existía y no hizo falta crearlo) o None si no hay (porque haya que
        crearlo y no se haya recibido almacén, etc.).
        """
        #print "cantidad", cantidad
        #print "bultos", bultos
        #print "almacen", almacen
        #raw_input()
        if cantidad == None:
            cantidad = self.get_stock(fecha, forzar = True,
                                      actualizar = False)
        if bultos == None:
            bultos = self.get_existencias(fecha, forzar = True,
                                          actualizar = False)
        try:
            historico_actual = self._buscar_en_historico(fecha, almacen)[0]
        except IndexError:
            historico_actual = None
        res = None
        if not historico_actual:
            if fecha and almacen:   # Evito crear registros
                # inútiles con fecha a None. Tampoco los quiero sin almacén.
                historico = HistorialExistencias(productoVenta = self,
                                                 cantidad = cantidad,
                                                 bultos = bultos,
                                                 fecha = fecha,
                                                 almacen = almacen)
                res = historico
        else:
            historico_actual.cantidad = cantidad
            historico_actual.bultos = bultos
            historico_actual.syncUpdate()
            res = historico_actual
        return res

    def _buscar_en_historico(self, fecha, almacen = None):
        """
        Busca en la tabla de historiales de existencia un registro
        para el producto del objeto y la fecha recibida.
        Si lo encuentra, lo devuelve dentro de una tupla. Si no, devuelve una
        tupla vacía.
        Si almacen:
            - es None: Devuelve una tupla de registros historial de
                       existencias para los almacenes.
            - no es None: Devuelve para el almacén recibido, pero siempre
                          en forma de tupla.

        IN:  fecha (mx.DateTime)
             almacen (pclases.Almacen | int) [None]
        OUT: tupla{pclases.HistorialExistencias}
        """
        reg = ()
        try:
            almacen_id = almacen.id
        except AttributeError:
            almacen_id = almacen
        if fecha:
            if almacen != None:
                historial = HistorialExistencias.select(AND(
                            HistorialExistencias.q.fecha == fecha,
                            HistorialExistencias.q.productoVentaID == self.id,
                            HistorialExistencias.q.almacenID == almacen_id))
                if historial.count() > 1:
                    myprint("pclases.py: _buscar_en_historico: Caché corrupta"\
                          ". Dos registros con misma fecha, almacén y produ"\
                          "ctoVenta.")
                if historial.count() >= 1:
                    reg = (historial[0], )
            else:   # almacen == None
                historiales = HistorialExistencias.select(AND(
                            HistorialExistencias.q.fecha == fecha,
                            HistorialExistencias.q.productoVentaID == self.id))
                if historiales:
                    reg = tuple([h for h in historiales])
        return reg

    def get_existencias(self, hasta = None, forzar = False, actualizar = True,
                        contar_defectuosos = False, almacen = None):
        """
        Devuelve las existencias en almacén del producto.
        Las existencias en almacén es el número de
        artículos del producto que no tengan albarán
        relacionado (ni partida de carga si es fibra).
        OJO: Devuelve el número de unidades, no los
        kilos ni m2.
        Si "hasta" != None devuelve las existencias hasta esa fecha.
        Si "forzar" es True, obliga al recuento y no busca en caché.
        Si "actualizar" es True, actualiza la caché (creando un registro en
        HistorialExistencias si fuera necesario).
        """
        #return self._DEPRECATED_get_existencias(hasta, forzar, actualizar,
        #                             contar_defectuosos, almacen)
        # 0.- Preparo estrucutras de datos.
        historicos = {}
        for a in Almacen.select():
            historicos[a] = (None, 0)
        if hasta and hasta >= mx.DateTime.localtime():
            # No permito búsquedas ni caché en HistorialExistencias de fechas
            # posteriores al día de hoy.
            hasta = None
        # 1.- Buscar en caché
        registros_historicos = self._buscar_en_historico(hasta, almacen)
        for r in registros_historicos:
            historicos[r.almacen] = (r, r.bultos)
        # 3/2.- Si se pregunta por todos los almacenes me aseguro de que
        # existe un histórico por almacén. En caso contrario fuerzo y
        # recuento todos.
        if not almacen:
            try:
                assert Almacen.select().count() == len(registros_historicos)
            except AssertionError:
                if DEBUG:
                    myprint("pclases.py::ProductoVenta.get_existencias: No hay "\
                          "registros HistorialExistencias para todos los alma"\
                          "cenes.")
                # ¿Porcuá actualizar si no me lo piden expresamente
                # por cabecera?
                #actualizar = True
                registros_historicos = None
        else:
            try:
                assert (len(registros_historicos) == 1
                        and (registros_historicos[0].almacen == almacen))
            except AssertionError:
                if DEBUG:
                    myprint("pclases.py::ProductoVenta.get_existencias: No hay "\
                          "registros HistorialExistencias para todos los alma"\
                          "cenes.")
                # Si hay más de uno, los borro todos.
                if len(registros_historicos) > 1:
                    for r in registros_historicos:
                        r.destroySelf()
                # ¿Y por qué querría yo actualizar a coj*nes? Si me está
                # preguntando la función de crear históricos, provocaré
                # recursividad infinita.
                #actualizar = True
                registros_historicos = None
        # 2.- Si no existe(n) registros o hay que forzar, recuento existencias:
        if not registros_historicos or (registros_historicos and forzar):
            almacenes_registros_bultos = self._recontar_existencias(hasta,
                                                        contar_defectuosos,
                                                        almacen)
                # Devuelve un "tipo de datos" compatible con «historicos».
            for a in almacenes_registros_bultos:
                registro, bultos = almacenes_registros_bultos[a]
                historicos[a] = (registro, bultos)
            # 2.1.- Si debo actualizar, lo hago.
            if actualizar:
                self.__machacar_o_crear_registros(historicos, hasta)
        # 3.- Devuelvo los bultos totales del almacén o los almacenes si se
        #     ha pedido para todos.
        res_bultos = sum([historicos[a][1] for a in historicos])
        return res_bultos

    def _recontar_existencias(self, hasta, contar_defectuosos, almacen = None):
        """
        Cuenta las existencias del producto que había en la fecha «hasta» y
        en el almacén «almacen» o en todos si es None.
        OUT: un diccionario cuyas claves son registros Almacen y los valores
             son listas con (registro HistorialExistencias|None, bultos).
        """
        if almacen:
            assert isinstance(almacen, Almacen)
            actuales = self.get_bultos_actuales(contar_defectuosos, almacen)
            entradas = self.get_entradas(hasta, contar_defectuosos, almacen)
            salidas = self.get_salidas(hasta, contar_defectuosos, almacen)
            existencias = actuales - len(entradas) + len(salidas)
            res = {almacen: [None, existencias]}
        else:
            res = {}
            for a in Almacen.select():
                actuales = self.get_bultos_actuales(contar_defectuosos, a)
                entradas = self.get_entradas(hasta, contar_defectuosos, a)
                salidas = self.get_salidas(hasta, contar_defectuosos, a)
                existencias = actuales - len(entradas) + len(salidas)
                res[a] = [None, existencias]
        return res

    def get_salidas(self, desde, contar_defectuosos = False, almacen = None,
                    hasta = mx.DateTime.localtime()):
        """
        Listado de artículos que salieron de un almacén en concreto o de
        cualquier almacén (ojo, un artículo puede estar en stock en un
        almacén y aparecer en este listado por haber abandonado el principal,
        por ejemplo) entre las fechas indicadas.
        """
        # Todo lo que sale, sale por albarán, so...
        AS = AlbaranSalida
        A = Articulo
        clauses = []
        clauses.append(AS.q.fecha >= desde)
        clauses.append(AS.q.fecha <= hasta)
        clauses.append(A.q.albaranSalidaID == AS.q.id)
        clauses.append(A.q.productoVentaID == self.id)
        if not contar_defectuosos:
            clauses.append(A.q.rolloDefectuosoID == None)
        if almacen:
            clauses.append(AS.q.almacenOrigenID == almacen.id)
        articulos_as = A.select(AND(*clauses))
        if DEBUG:
            myprint("# artículos en albaranes de salida:", articulos_as.count())
        return list(articulos_as)

    def get_entradas(self, desde, contar_defectuosos = False, almacen = None,
                     hasta = mx.DateTime.localtime()):
        """
        Listado de artículos que entraron en el almacén desde la fecha
        «desde» hasta la actualidad por defecto, ambas incluidas.
        Las entradas se componen de los artículos fabricados en los partes
        de producción, los devueltos en abonos y los albaranes de
        transferencia (que en realidad son una entrada y una salida a la
        vez, pero se contará una, otra o las dos en función de si se
        solicita un almacén o la cifra global).
        «contar_defectuosos» solo tiene efecto para los geotextiles.
        """
        # 1.- Albaranes de transferencia actuando como entrada en almacén.
        AS = AlbaranSalida
        A = Articulo
        clauses = []
        clauses.append(AS.q.fecha >= desde)
        clauses.append(AS.q.fecha <= hasta)
        clauses.append(A.q.albaranSalidaID == AS.q.id)
        clauses.append(A.q.productoVentaID == self.id)
        if not contar_defectuosos:
            clauses.append(A.q.rolloDefectuosoID == None)
        if almacen:
            clauses.append(AS.q.almacenDestinoID == almacen.id)
        else:
            clauses.append(AS.q.almacenDestinoID != None)
        articulos_as = A.select(AND(*clauses))
        if DEBUG:
            myprint("# artículos en albaranes de salida:", articulos_as.count())
        # 2.- Partes de producción
        PDP = ParteDeProduccion
        clauses = []
        almacen_ppal = Almacen.get_almacen_principal_or_none()
        # Si quiere un almacén en concreto y no es el principal, no hay
        # artículos procedentes de los PDP. Si no hay definido un almacén
        # principal, almacen_ppal es None, pero como «almacen» no lo será,
        # entrará por la rama else.
        if not contar_defectuosos:
            clauses.append(A.q.rolloDefectuosoID == None)
        if (almacen and almacen != almacen_ppal):
            articulos_pdp = A.select(AND(A.q.id==-1, *clauses))
                # Siempre va a dar un SelectResult vacío porque no hay ID <= 0,
                # que es justamente lo que queremos.
        else:
            clauses.append(PDP.q.fechahorainicio >= desde)
            clauses.append(PDP.q.fechahorafin <= hasta)
            clauses.append(A.q.parteDeProduccionID == PDP.q.id)
            clauses.append(A.q.productoVentaID == self.id)
            articulos_pdp = A.select(AND(*clauses))
        if DEBUG:
            myprint("# artículos en partes de producción:", articulos_pdp.count())
        # 3.- Abonos
        AB = Abono
        LDD = LineaDeDevolucion
        clauses = []
        clauses.append(AB.q.fecha >= desde)
        clauses.append(AB.q.fecha <= hasta)
        clauses.append(LDD.q.abonoID == AB.q.id)
        clauses.append(LDD.q.articuloID == A.q.id)
        clauses.append(A.q.productoVentaID == self.id)
        if not contar_defectuosos:
            clauses.append(A.q.rolloDefectuosoID == None)
        if almacen:
            clauses.append(AB.q.almacenID == almacen.id)
        articulos_abonados = A.select(AND(*clauses))
        if DEBUG:
            myprint("# artículos abonados:", articulos_abonados.count())
        # Aquí viene la matraca. Si pudiera sumar SelectResults rápidamente...
        articulos = []
        for lista in articulos_as, articulos_pdp, articulos_abonados:
            for a in lista:
                if a not in articulos:
                    articulos.append(a)
        return articulos

    def get_diferencia_entradas_salidas(self, desde,
                                        contar_defectuosos = False,
                                        almacen = None,
                                        hasta = mx.DateTime.localtime()):
        """
        Devuelve los objetos artículos de difernecia entre las entradas y
        las salidas entre dos fechas dadas.
        El resultado lo devuelve como un diccionario con dos claves: entradas
        y salidas. Los valores serán conjuntos.
        """
        entradas = self.get_entradas(desde, contar_defectuosos, almacen, hasta)
        salidas = self.get_salidas(desde, contar_defectuosos, almacen, hasta)
        res = {'entradas': set(entradas) - set(salidas),
               'salidas': set(salidas) - set(entradas)}
        return res

    def get_bultos_actuales(self, contar_defectuosos = False, almacen = None):
        """
        Cuenta los objetos artículo relacionados con el producto actual y que
        se encuentran en almacén en general si «almacen» es None, o en el
        almacén «almacen».
        contar_defectuosos solo tiene efecto si el producto es de geotextiles.
        """
        # En la nueva versión, todo artículo está en almacén si tiene un
        # registro almacén relacionado directamente.
        clause_producto = Articulo.q.productoVentaID == self.id
        if almacen:
            clause_almacen = Articulo.q.almacenID == almacen.id
        else:
            clause_almacen = Articulo.q.almacenID != None
        if not contar_defectuosos:
            articulos = Articulo.select(AND(clause_producto, clause_almacen,
                                        Articulo.q.rolloDefectuosoID == None))
        else:
            articulos = Articulo.select(AND(clause_producto, clause_almacen))
        bultos = articulos.count()
        return bultos

    def __machacar_o_crear_registros(self, historicos, fecha):
        """
        Recibe un diccionario de almacenes con su registro
        HistorialExistencias|None y bultos que debería tener.
        Por cada almacén, si el registro es None, lo crea. Si no, lo actualiza
        con la cantidad correspondiente.
        """
        for almacen in historicos:
            registro, bultos = historicos[almacen]
            if not registro:    # Hay que crearlo nuevo.
                registro = self._agregar_a_historico(fecha,
                                                     bultos = bultos,
                                                     almacen = almacen)
            else:               # Existe y hay que actualizarlo.
                registro.bultos = bultos
                cantidad = self.get_stock(fecha, forzar = True,
                                          actualizar = False,
                                          almacen = almacen)
                registro.cantidad = cantidad
                registro.syncUpdate()

    def _DEPRECATED_get_existencias(self, hasta = None, forzar = False,
                                    actualizar = True,
                                    contar_defectuosos = False,
                                    almacen = None):
        """
        ==============
        = DEPRECATED =
        ==============

        Devuelve las existencias en almacén del producto.
        Las existencias en almacén es el número de
        artículos del producto que no tengan albarán
        relacionado (ni partida de carga si es fibra).
        OJO: Devuelve el número de unidades, no los
        kilos ni m2.
        Si "hasta" != None devuelve las existencias hasta esa fecha.
        Si "forzar" es True, obliga al recuento y no busca en caché.
        Si "actualizar" es True, actualiza la caché (creando un registro en
        HistorialExistencias si fuera necesario).
        """
        # TMP: De momento se ignora el almacén. Es únicamente para evitar
        #      errores en invocación.
        if hasta and hasta >= mx.DateTime.localtime():
            # No permito búsquedas ni caché en HistorialExistencias de fechas
            # posteriores al día de hoy.
            hasta = None
        bultos = 0
        if forzar:
            historicos = None
        else:
            historicos = self._buscar_en_historico(hasta)
        if historicos:
            bultos = sum([h.bultos for h in historicos])
        else:
            if not self.es_bala():
                if self.es_especial():
                    return self.camposEspecificosEspecial.existencias
                else:
                    if not hasta:
                        if contar_defectuosos:
                            articulos_en_almacen = Articulo.select(
                                AND(Articulo.q.albaranSalidaID == None,
                                    Articulo.q.productoVentaID == self.id))
                        else:
                            articulos_en_almacen = Articulo.select(
                                AND(Articulo.q.albaranSalidaID == None,
                                    Articulo.q.productoVentaID == self.id,
                                    Articulo.q.rolloDefectuosoID == None))
                        # Para los rollosC "contrar_defectuosos" no tiene
                        # relevancia.
                        bultos = articulos_en_almacen.count()
                    else:
                        if self.es_bala_cable():
                            fecha = hasta.strftime('%Y-%m-%d')
                            albaranes_de_salida_despues_de_fecha = """
                            SELECT albaran_salida.id
                            FROM albaran_salida
                            WHERE albaran_salida.fecha > '%s'
                            """ % (fecha)
                            fecha_limite_para_comparaciones_con_fechahoras = (
                                hasta+mx.DateTime.oneDay).strftime('%Y-%m-%d')
                            articulos_en_almacen = BalaCable.select("""
                                bala_cable.id IN (SELECT articulo.bala_cable_id
                                                 FROM articulo
                                                 WHERE articulo.producto_venta_id = %d
                                                    AND articulo.bala_cable_id IS NOT NULL
                                                    AND (articulo.albaran_salida_id IS NULL OR articulo.albaran_salida_id IN (%s)))
                                AND bala_cable.fechahora < '%s'
                                                     """ % (self.id,
                                                            albaranes_de_salida_despues_de_fecha,
                                                            fecha_limite_para_comparaciones_con_fechahoras))
                        elif self.es_rolloC():
                            fecha = hasta.strftime('%Y-%m-%d')
                            albaranes_de_salida_despues_de_fecha = """
                            SELECT albaran_salida.id
                            FROM albaran_salida
                            WHERE albaran_salida.fecha > '%s'
                            """ % (fecha)
                            fecha_limite_para_comparaciones_con_fechahoras = (
                                hasta+mx.DateTime.oneDay).strftime('%Y-%m-%d')
                            articulos_en_almacen = RolloC.select("""
                                rollo_c.id IN (
                                    SELECT articulo.rollo_c_id
                                    FROM articulo
                                    WHERE articulo.producto_venta_id = %d
                                    AND articulo.rollo_c_id IS NOT NULL
                                    AND (articulo.albaran_salida_id IS NULL
                                         OR articulo.albaran_salida_id IN (%s)
                                        ))
                                AND rollo_c.fechahora < '%s'
                                """ % (
                              self.id,
                              albaranes_de_salida_despues_de_fecha,
                              fecha_limite_para_comparaciones_con_fechahoras))
                        else:
                            articulos_en_almacen = (
                                self.__get_articulos_no_bala_en_almacen_hasta(
                                    hasta, contar_defectuosos))
                            #DEBUG: for a in articulos_en_almacen:
                            #DEBUG:     print a.codigo
                        bultos = articulos_en_almacen.count()
            else:   # Las balas se pueden vender Y TAMBIÉN CONSUMIR:
                if not hasta:
                    articulos_en_almacen = Articulo.select("""
                        articulo.bala_id IN (SELECT bala.id
                        FROM bala
                        WHERE bala.partida_carga_id IS NULL)
                        AND articulo.albaran_salida_id IS NULL
                        AND articulo.bala_id IS NOT NULL
                        AND articulo.producto_venta_id = %d""" % (self.id))
                    bultos = articulos_en_almacen.count()
                else:
                    balas = self.__get_balas_hasta(hasta)
                    bultos = balas.count()
            if actualizar:
                self._agregar_a_historico(hasta, bultos = bultos)
        return bultos

    get_bultos = get_existencias

    def _OBSOLETE_get_stock(self, hasta = None, forzar = False,
                            actualizar = True, contar_defectuosos = False,
                            almacen = None):
        """
        Devuelve las existencias pero en las unidades
        del producto: metros si es rollo o kilos si es
        bala.
        Los kilos de las balas se obtienen sumando el
        peso de todas las balas en almacén.
        Los metros cuadrados de los rollos se obtienen
        multiplicando el número de rollos en almacén por
        el ancho y metros lineales del producto.
        Si "hasta" es distinto de None, debe ser una fecha; y
        calculará las existencias hasta esa fecha.
        Si "forzar" es True, obliga al recuento y no busca en caché.
        Si "actualizar" es True, actualiza la caché (creando un registro en
        HistorialExistencias si fuera necesario).
        ---
        OBSOLETO. Ya no se usa. No tiene en cuenta almacenes y provoca
        recursión infinita con determinada combinación de parámetros.
        """
        # TMP: De momento se ignora el almacén. Es únicamente para evitar
        # errores en invocación.
        if hasta >= mx.DateTime.localtime():
            # No permito búsquedas ni caché en HistorialExistencias de fechas
            # posteriores al día de hoy.
            hasta = None
        cantidad = 0.0
        if not hasta:
            actualizar = False
        if forzar:
            historicos = None
        else:
            historicos = self._buscar_en_historico(hasta)
        if historicos:
            cantidad = sum([h.cantidad for h in historicos])
        else:
            if self.es_bala():
                try:
                    if not hasta:
                        balas = Bala.select("""
                        bala.id IN (SELECT articulo.bala_id
                                    FROM articulo
                                    WHERE articulo.albaran_salida_id IS NULL
                                    AND articulo.producto_venta_id = %d
                                    AND NOT articulo.bala_id IS NULL)
                                    AND bala.partida_carga_id IS NULL """ % (
                            self.id))
                    else:
                        balas = self.__get_balas_hasta(hasta)
                    if balas.count() > 0:
                        cantidad = balas.sum('pesobala')
                    else:
                        cantidad = 0.0
                except Exception, msg:      # Lo que sea. Error psycopg,
                                            # interno de sqlobjet, lo que sea.
                    myprint("pclases.py: get_stock: Error contando existencias en balas de productoVentaID %d: %s" % (self.id, msg))
                    cantidad = 0.0
            elif self.es_rollo():
                cantidad = self.get_existencias(hasta, forzar = forzar,
                                                actualizar = actualizar,
                                                contar_defectuosos = False) \
                           * self.camposEspecificosRollo.ancho \
                           * self.camposEspecificosRollo.metrosLineales
                if contar_defectuosos:
                    if hasta:
                        rollos_defectuosos_almacen = RolloDefectuoso.select(
                            AND(RolloDefectuoso.q.id
                                    == Articulo.q.rolloDefectuosoID,
                                Articulo.q.productoVentaID == self.id,
                                Articulo.q.parteDeProduccionID
                                    == ParteDeProduccion.q.id,
                                ParteDeProduccion.q.fecha
                                    < hasta + mx.DateTime.oneDay,
                                Articulo.q.albaranSalidaID == None))
                    else:
                        rollos_defectuosos_almacen = RolloDefectuoso.select(
                            AND(RolloDefectuoso.q.id
                                    == Articulo.q.rolloDefectuosoID,
                                Articulo.q.productoVentaID == self.id,
                                Articulo.q.albaranSalidaID == None))
                    if DEBUG: myprint("Antes de defectuosos:", cantidad)
                    cantidad += sum([rd.ancho * rd.metrosLineales for rd in rollos_defectuosos_almacen])
                    if DEBUG: myprint("Después de defectuosos:", cantidad)
            elif self.es_bigbag():
                try:
                    if not hasta:
                        bigbags = Bigbag.select("""
                         bigbag.id IN (SELECT articulo.bigbag_id
                                       FROM articulo
                                       WHERE articulo.albaran_salida_id IS NULL
                                       AND articulo.producto_venta_id = %d
                                       AND NOT articulo.bigbag_id IS NULL)
                         """ % (self.id))
                    else:
                        fecha = hasta.strftime('%Y-%m-%d')
                        fecha_limite_para_comparaciones_con_fechahoras = (
                                hasta+mx.DateTime.oneDay).strftime('%Y-%m-%d')
                        partes_de_produccion_antes_de_fecha = """
                        SELECT id
                        FROM parte_de_produccion
                        WHERE parte_de_produccion.fecha <= '%s'
                        """ % (fecha)
                        condicion_no_parte_y_fecha_fab_antes_de_fecha = """
                        articulo.parte_de_produccion_id IS NULL
                        AND articulo.bigbag_id IN (SELECT bigbag.id
                                                   FROM bigbag
                                                   WHERE bigbag.id = articulo.bigbag_id AND bigbag.fechahora < '%s')
                        """ % (fecha_limite_para_comparaciones_con_fechahoras)
                        albaranes_de_salida_despues_de_fecha = """
                        SELECT albaran_salida.id
                        FROM albaran_salida
                        WHERE albaran_salida.fecha > '%s'
                        """ % (fecha)
                        bigbags = Bigbag.select("""
                          bigbag.id IN (SELECT articulo.bigbag_id
                                        FROM articulo
                                        WHERE articulo.producto_venta_id = %d
                                        AND articulo.bigbag_id IS NOT NULL
                                        AND (articulo.parte_de_produccion_id IN (%s) OR (%s))
                                        AND (articulo.albaran_salida_id IS NULL OR articulo.albaran_salida_id IN (%s)))
                          """ % (self.id,
                                 partes_de_produccion_antes_de_fecha,
                                 condicion_no_parte_y_fecha_fab_antes_de_fecha,
                                 albaranes_de_salida_despues_de_fecha))
                    if bigbags.count() > 0:
                        cantidad = bigbags.sum('pesobigbag')
                    else:
                        cantidad = 0.0
                except:     # Lo que sea. Error psycopg, interno de
                            # sqlobjet, lo que sea.
                    myprint("pclases.py: get_stock: Error contando existencias en bigbags de productoVentaID %d." % (self.id))
                    cantidad = 0.0
            elif self.es_caja():
                try:
                    if not hasta:
                        cajas = Caja.select("""
                         caja.id IN (SELECT articulo.caja_id
                                       FROM articulo
                                       WHERE articulo.albaran_salida_id IS NULL
                                       AND articulo.producto_venta_id = %d
                                       AND NOT articulo.caja_id IS NULL)
                         """ % (self.id))
                    else:
                        fecha = hasta.strftime('%Y-%m-%d')
                        fecha_limite_para_comparaciones_con_fechahoras = (
                                hasta+mx.DateTime.oneDay).strftime('%Y-%m-%d')
                        partes_de_produccion_antes_de_fecha = """
                        SELECT id
                        FROM parte_de_produccion
                        WHERE parte_de_produccion.fecha <= '%s'
                        """ % (fecha)
                        condicion_no_parte_y_fecha_fab_antes_de_fecha = """
                        articulo.parte_de_produccion_id IS NULL
                        AND articulo.caja_id IN (SELECT caja.id
                                                   FROM caja
                                                   WHERE caja.id = articulo.caja_id AND caja.fechahora < '%s')
                        """ % (fecha_limite_para_comparaciones_con_fechahoras)
                        albaranes_de_salida_despues_de_fecha = """
                        SELECT albaran_salida.id
                        FROM albaran_salida
                        WHERE albaran_salida.fecha > '%s'
                        """ % (fecha)
                        cajas = Caja.select("""
                          caja.id IN (SELECT articulo.caja_id
                                        FROM articulo
                                        WHERE articulo.producto_venta_id = %d
                                        AND articulo.caja_id IS NOT NULL
                                        AND (articulo.parte_de_produccion_id IN (%s) OR (%s))
                                        AND (articulo.albaran_salida_id IS NULL OR articulo.albaran_salida_id IN (%s)))
                          """ % (self.id,
                                 partes_de_produccion_antes_de_fecha,
                                 condicion_no_parte_y_fecha_fab_antes_de_fecha,
                                 albaranes_de_salida_despues_de_fecha))
                    cantidad = sum([c.peso for c in cajas])
                except:     # Lo que sea. Error psycopg, interno de
                            # sqlobjet, lo que sea.
                    myprint("pclases.py: get_stock: Error contando existencias en bolsas de productoVentaID %d." % (self.id))
                    cantidad = 0.0
            elif self.es_bala_cable():
                try:
                    if not hasta:
                        bala_cables = BalaCable.select("""
                            bala_cable.id IN (
                                SELECT articulo.bala_cable_id
                                FROM articulo
                                WHERE articulo.albaran_salida_id IS NULL
                                AND articulo.producto_venta_id = %d
                                AND NOT articulo.bala_cable_id IS NULL)
                        """ % (self.id))
                    else:
                        fecha = hasta.strftime('%Y-%m-%d')
                        albaranes_de_salida_despues_de_fecha = """
                        SELECT albaran_salida.id
                        FROM albaran_salida
                        WHERE albaran_salida.fecha > '%s'
                        """ % (fecha)
                        fecha_limite_para_comparaciones_con_fechahoras = (
                                hasta+mx.DateTime.oneDay).strftime('%Y-%m-%d')
                        bala_cables = BalaCable.select("""
                            bala_cable.id IN (
                                SELECT articulo.bala_cable_id
                                FROM articulo
                                WHERE articulo.producto_venta_id = %d
                                AND articulo.bala_cable_id IS NOT NULL
                                AND (articulo.albaran_salida_id IS NULL
                                     OR articulo.albaran_salida_id IN (%s)))
                            AND bala_cable.fechahora < '%s'
                        """ % (self.id,
                               albaranes_de_salida_despues_de_fecha,
                               fecha_limite_para_comparaciones_con_fechahoras))
                    if bala_cables.count() > 0:
                        cantidad = bala_cables.sum('peso')
                    else:
                        cantidad = 0.0
                except Exception, msg:      # Lo que sea. Error psycopg,
                                            # interno de sqlobjet, lo que sea.
                    myprint("pclases.py: get_stock: Error contando existencias en balas de cable de productoVentaID %d. Excepción: %s" % (self.id, msg))
                    cantidad = 0.0
            elif self.es_rollo_c():
                try:
                    if not hasta:
                        rollos_c = RolloC.select("""
                            rollo_c.id IN (
                                SELECT articulo.rollo_c_id
                                FROM articulo
                                WHERE articulo.albaran_salida_id IS NULL
                                AND articulo.producto_venta_id = %d
                                AND NOT articulo.rollo_c_id IS NULL)
                        """ % (self.id))
                    else:
                        fecha = hasta.strftime('%Y-%m-%d')
                        albaranes_de_salida_despues_de_fecha = """
                        SELECT albaran_salida.id
                        FROM albaran_salida
                        WHERE albaran_salida.fecha > '%s'
                        """ % (fecha)
                        fecha_limite_para_comparaciones_con_fechahoras = (
                                hasta+mx.DateTime.oneDay).strftime('%Y-%m-%d')
                        rollos_c = RolloC.select("""
                            rollo_c.id IN (
                                SELECT articulo.rollo_c_id
                                FROM articulo
                                WHERE articulo.producto_venta_id = %d
                                AND articulo.rollo_c_id IS NOT NULL
                                AND (articulo.albaran_salida_id IS NULL
                                     OR articulo.albaran_salida_id IN (%s)))
                            AND rollo_c.fechahora < '%s'
                        """ % (self.id,
                               albaranes_de_salida_despues_de_fecha,
                               fecha_limite_para_comparaciones_con_fechahoras))
                    if rollos_c.count() > 0:
                        cantidad = rollos_c.sum('peso')
                    else:
                        cantidad = 0.0
                except Exception, msg:      # Lo que sea. Error psycopg,
                                            # interno de sqlobjet, lo que sea.
                    myprint("pclases.py: get_stock: Error contando existencias en balas de cable de productoVentaID %d. Excepción: %s" % (self.id, msg))
                    cantidad = 0.0
            elif self.es_especial():
                cantidad = self.camposEspecificosEspecial.stock
            else:
                myprint("pclases::ProductoVenta::get_stock: ERROR: El producto de venta %s no es ni rollo ni bigbag ni caja ni bala de cable. Verificar." % (self.id))
                cantidad = 0.0
            if actualizar:
                self._agregar_a_historico(hasta, cantidad = cantidad)
        return cantidad

    def _get_rollos_defectuososos_en_fecha_almacen(self, hasta, almacen = None):
        """
        Devuelve un listado de objetos rolloDefectuoso que estaban en el
        almacén «almacen» en la fecha «hasta». Si «almacen» es None devuelve
        todos los rollos defectuosos que estaban almacenados en esa fecha.
        """
        # Un rollo defectuoso estaba en el almacén en una fecha dada si:
        # 1.- Se fabricó en la fecha «hasta» o en una anterior.
        # 2.- No está en ningún albarán de salida cuyo almacén de origen
        #     sea el almacén en cuestión.
        # 3.- Está en algún abono con destino «almacén» con fecha posterior
        #     a «hasta».
        # 4.- Está en un albarán de transferencia con almacén de destino
        #     «almacen» en fecha posterior a «hasta».
        RD = RolloDefectuoso
        A = Articulo
        PDP = ParteDeProduccion
        rds = RD.select(AND(A.q.rolloDefectuosoID == RD.q.id,
                            A.q.parteDeProduccionID == PDP.q.id,
                            PDP.q.fecha < hasta + mx.DateTime.oneDay))
        # Premature optimization is the root of all evil.
        # De entre todos los rollos fabricados antes de la fecha, voy a ver
        # los que estaban en el almacén. Puede ser lento, sí, pero es lo que
        # hay. Lee el aforismo de antes, anda.
        en_almacen = []
        for rd in rds:
            if rd.articulo.en_almacen(hasta, almacen):
                en_almacen.append(rd)
        return SQLlist(en_almacen)

    def _get_articulos_en_fecha_en_almacen(self, fecha = mx.DateTime.today(),
                                           almacen = None,
                                           tipo = None):
        """
        Devuelve una lista de artículos que se encontraban en un almacén
        concreto en la fecha «fecha» o en cualquier almacén si «almacen» es
        None para el producto en cuestión.
        OJO: Solo vale para artículos FABRICABLES. O sea, no vale para
        balas de cable, por ejemplo, porque no proceden de un parte de
        producción.
        """
        A = Articulo
        PDP = ParteDeProduccion
        if not fecha:
            fecha = mx.DateTime.today()
        clauses = [A.q.parteDeProduccionID == PDP.q.id,
                   PDP.q.fecha < fecha + mx.DateTime.oneDay,
                   A.q.productoVentaID == self.id]
        if tipo is Rollo:
            clauses.append(A.q.rolloID != None)
        elif tipo is Bala:
            clauses.append(A.q.balaID != None)
        elif tipo is Bigbag:
            clauses.append(A.q.bigbagID != None)
        elif tipo is Caja:
            clauses.append(A.q.cajaID != None)
        elif tipo is RolloDefectuoso:
            clauses.append(A.q.rolloDefectuosoID != None)
        elif (tipo is BalaCable or tipo is RolloC):
            #raise ValueError, "Solo productos fabricables en partes de prod"\
            #                  "ucción."
            clauses = [A.q.productoVentaID == self.id]
            if tipo is BalaCable:
                clauses.append(
                    BalaCable.q.fechahora < fecha + mx.DateTime.oneDay)
                clauses.append(A.q.balaCableID == BalaCable.q.id)
                #clauses.append(A.q.balaCableID != None)
            elif tipo is RolloC:
                clauses.append(
                    RolloC.q.fechahora < fecha + mx.DateTime.oneDay)
                clauses.append(A.q.rolloCID == RolloC.q.id)
                #clauses.append(A.q.rolloCID != None)
            else:
                raise ValueError, "pclases.py::ProductoVenta: tipo debe ser "\
                                  "Rollo, Bala, Bigbag, Caja, "\
                                  " RolloDefecutoso, BalaCable o RolloC"
        else:
            pass    # Cualquier tipo de artículo. No cláusulas adicionales.
        articulos = A.select(AND(*clauses))
        en_almacen = []
        # PLAN: Optimizar
        if DEBUG and VERBOSE:
            contador = 0
            total = articulos.count()
        for a in articulos:
            if a.en_almacen(fecha, almacen):
                en_almacen.append(a)
            if DEBUG and VERBOSE:
                contador += 1
                myprint("%d de %d" % (contador, total))
        return SQLtuple(en_almacen)

    def _get_rollos_defectuososos_actuales_almacen(self, almacen = None):
        """
        Devuelve una lista de objetos rolloDefectuoso que están en algún
        almacén o en un almacén concreto (si «almacen» no es None) actualmente.
        """
        A = Articulo
        RD = RolloDefectuoso
        clauses = [A.q.rolloDefectuosoID == RD.q.id,
                   A.q.productoVentaID == self.id]
        if almacen:
            clauses.append(A.q.almacenID == almacen.id)
        else:
            clauses.append(A.q.almacenID != None)
        rds = RD.select(AND(*clauses))
        return SQLlist(rds)

    def get_stock(self, hasta = None, forzar = False, actualizar = True,
                  contar_defectuosos = False, almacen = None):
        """
        Devuelve las existencias pero en las unidades
        del producto: metros si es rollo o kilos si es
        bala.
        Los kilos de las balas se obtienen sumando el
        peso de todas las balas en almacén.
        Los metros cuadrados de los rollos se obtienen
        multiplicando el número de rollos en almacén por
        el ancho y metros lineales del producto.
        IN:
            hasta -> None: Existencias a fecha actual.
                  -> fecha: Existencias a esa fecha.
            forzar -> True. No consulta históricos.
                   -> False. Tira de caché de históricos.
            actualizar -> True. Machaca o crea los registros históricos.
                          False. No hace nada.
            contar_defectuosos -> True. Incluye los rolloDefectuoso en las
                                        existencias.
                                  False. Excluye los artículos con
                                         rolloDefectuoso de las existencias.
            almacen -> None. Devuelve el total para todos los almacenes.
                       != None. Devuelve el stock en unidades del SI para el
                                almacén recibido.
        """
        if hasta and hasta >= mx.DateTime.localtime():
            # No permito búsquedas ni caché en HistorialExistencias de fechas
            # posteriores al día de hoy.
            hasta = None
        if not hasta:
            actualizar = False
        if forzar:
            historicos = None
        else:
            historicos = self._buscar_en_historico(hasta)
        cantidad = 0.0
        if historicos:
            cantidad = sum([h.cantidad for h in historicos])
        else:
            if self.es_bala():
                try:
                    if not hasta:
                        # Listado de objetos Bala en almacén ACTUALMENTE.
                        balas = Bala._buscar_en_almacen_actualmente(
                                      productoVenta = self, almacen = almacen)
                    else:
                        balas=self.__get_balas_hasta(hasta, almacen = almacen)
                    if balas.count() > 0:
                        cantidad = balas.sum('pesobala')
                    else:
                        cantidad = 0.0
                except Exception, msg:      # Lo que sea. Error psycopg,
                                            # interno de sqlobjet, lo que sea.
                    myprint("pclases.py: get_stock: Error contando existencias "\
                          "en balas de productoVentaID %d: %s" % (self.id, msg))
                    cantidad = 0.0
            elif self.es_rollo():
                cantidad = self.get_existencias(hasta, forzar = True,
                                    actualizar = False,
                                    contar_defectuosos = False,
                                    almacen = almacen) \
                           * self.camposEspecificosRollo.ancho \
                           * self.camposEspecificosRollo.metrosLineales
                if contar_defectuosos:
                    if hasta:
                        rollos_defectuosos_almacen = self._get_rollos_defectuososos_en_fecha_almacen(hasta, almacen)
                        #if almacen:
                        #    rollos_defectuosos_almacen=RolloDefectuoso.select(
                        #        AND(RolloDefectuoso.q.id
                        #                == Articulo.q.rolloDefectuosoID,
                        #            Articulo.q.productoVentaID == self.id,
                        #            Articulo.q.parteDeProduccionID
                        #                == ParteDeProduccion.q.id,
                        #            ParteDeProduccion.q.fecha
                        #                < hasta + mx.DateTime.oneDay,
                        #            Articulo.q.almacen == almacen))
                        #            #Articulo.q.albaranSalidaID == None))
                        #else:
                        #    rollos_defectuosos_almacen=RolloDefectuoso.select(
                        #        AND(RolloDefectuoso.q.id
                        #                == Articulo.q.rolloDefectuosoID,
                        #            Articulo.q.productoVentaID == self.id,
                        #            Articulo.q.parteDeProduccionID
                        #                == ParteDeProduccion.q.id,
                        #            ParteDeProduccion.q.fecha
                        #                < hasta + mx.DateTime.oneDay,
                        #            Articulo.q.almacen != None))
                        #            #Articulo.q.albaranSalidaID == None))
                    else:
                        # Rollos defectuosos en algún almacen o en uno
                        # concreto pero actualmente.
                        rollos_defectuosos_almacen = self._get_rollos_defectuososos_actuales_almacen(almacen)
                        #rollos_defectuosos_almacen = RolloDefectuoso.select(
                        #    AND(RolloDefectuoso.q.id
                        #            == Articulo.q.rolloDefectuosoID,
                        #        Articulo.q.productoVentaID == self.id,
                        #        Articulo.q.albaranSalidaID == None))
                    if DEBUG: myprint("Antes de defectuosos:", cantidad)
                    cantidad += sum([rd.ancho * rd.metrosLineales for rd in rollos_defectuosos_almacen])
                    if DEBUG: myprint("Después de defectuosos:", cantidad)
            elif self.es_bigbag():
                try:
                    if not hasta:
                        if not almacen:
                            bigbags = Bigbag.select("""
                             bigbag.id IN (SELECT articulo.bigbag_id
                                         FROM articulo
                                         WHERE articulo.almacen_id IS NOT NULL
                                           AND articulo.producto_venta_id = %d
                                           AND NOT articulo.bigbag_id IS NULL)
                             """ % (self.id))
                        else:
                            bigbags = Bigbag.select("""
                             bigbag.id IN (SELECT articulo.bigbag_id
                                         FROM articulo
                                         WHERE articulo.almacen_id = %d
                                           AND articulo.producto_venta_id = %d
                                           AND NOT articulo.bigbag_id IS NULL)
                             """ % (almacen.id, self.id))
                    else:
                        articulos = self._get_articulos_en_fecha_en_almacen(
                                    hasta, almacen, tipo = Bigbag)
                        bigbags = SQLtuple([a.bigbag for a in articulos
                                            if a.bigbagID != None])
                        #fecha = hasta.strftime('%Y-%m-%d')
                        #fecha_limite_para_comparaciones_con_fechahoras = (hasta + mx.DateTime.oneDay).strftime('%Y-%m-%d')
                        #partes_de_produccion_antes_de_fecha = """
                        #SELECT id
                        #FROM parte_de_produccion
                        #WHERE parte_de_produccion.fecha <= '%s'
                        #""" % (fecha)
                        #condicion_no_parte_y_fecha_fab_antes_de_fecha = """
                        #articulo.parte_de_produccion_id IS NULL
                        #AND articulo.bigbag_id IN (SELECT bigbag.id
                        #                           FROM bigbag
                        #                           WHERE bigbag.id = articulo.bigbag_id AND bigbag.fechahora < '%s')
                        #""" % (fecha_limite_para_comparaciones_con_fechahoras)
                        #albaranes_de_salida_despues_de_fecha = """
                        #SELECT albaran_salida.id
                        #FROM albaran_salida
                        #WHERE albaran_salida.fecha > '%s'
                        #""" % (fecha)
                        #bigbags = Bigbag.select("""
                        #  bigbag.id IN (SELECT articulo.bigbag_id
                        #                FROM articulo
                        #                WHERE articulo.producto_venta_id = %d
                        #                AND articulo.bigbag_id IS NOT NULL
                        #                AND (articulo.parte_de_produccion_id IN (%s) OR (%s))
                        #                AND (articulo.albaran_salida_id IS NULL OR articulo.albaran_salida_id IN (%s)))
                        #  """ % (self.id,
                        #         partes_de_produccion_antes_de_fecha,
                        #         condicion_no_parte_y_fecha_fab_antes_de_fecha,
                        #         albaranes_de_salida_despues_de_fecha))
                    if bigbags.count() > 0:
                        cantidad = bigbags.sum('pesobigbag')
                    else:
                        cantidad = 0.0
                except Exception, msg:  # Lo que sea. Error psycopg, interno
                                        # de sqlobjet, lo que sea.
                    myprint("pclases.py: get_stock: Error contando existencias en bigbags de productoVentaID %d: %s" % (self.id, msg))
                    cantidad = 0.0
            elif self.es_bala_cable():
                try:
                    if not hasta:
                        #bala_cables = BalaCable.select("""
                        #    bala_cable.id IN (
                        #        SELECT articulo.bala_cable_id
                        #        FROM articulo
                        #        WHERE articulo.albaran_salida_id IS NULL
                        #        AND articulo.producto_venta_id = %d
                        #        AND NOT articulo.bala_cable_id IS NULL)
                        #""" % (self.id))
                        if not almacen:
                            bala_cables = BalaCable.select("""
                                bala_cable.id IN (
                                    SELECT articulo.bala_cable_id
                                    FROM articulo
                                    WHERE NOT articulo.almacen_id IS NULL
                                      AND articulo.producto_venta_id = %d
                                      AND NOT articulo.bala_cable_id IS NULL)
                            """ % (self.id))
                        else:
                            bala_cables = BalaCable.select("""
                                bala_cable.id IN (
                                    SELECT articulo.bala_cable_id
                                    FROM articulo
                                    WHERE articulo.almacen_id  = %d
                                      AND articulo.producto_venta_id = %d
                                      AND NOT articulo.bala_cable_id IS NULL)
                            """ % (almacen.id, self.id))
                    else:
                        articulos = self._get_articulos_en_fecha_en_almacen(
                                    hasta, almacen, tipo = BalaCable)
                        bala_cables = SQLtuple([a.balaCable for a in articulos
                                                if a.balaCableID != None])
                        #fecha = hasta.strftime('%Y-%m-%d')
                        #albaranes_de_salida_despues_de_fecha = """
                        #SELECT albaran_salida.id
                        #FROM albaran_salida
                        #WHERE albaran_salida.fecha > '%s'
                        #""" % (fecha)
                        #fecha_limite_para_comparaciones_con_fechahoras = (hasta + mx.DateTime.oneDay).strftime('%Y-%m-%d')
                        #bala_cables = BalaCable.select("""
                        #    bala_cable.id IN (
                        #        SELECT articulo.bala_cable_id
                        #        FROM articulo
                        #        WHERE articulo.producto_venta_id = %d
                        #        AND articulo.bala_cable_id IS NOT NULL
                        #        AND (articulo.albaran_salida_id IS NULL
                        #             OR articulo.albaran_salida_id IN (%s)))
                        #    AND bala_cable.fechahora < '%s'
                        #""" % (self.id,
                        #       albaranes_de_salida_despues_de_fecha,
                        #       fecha_limite_para_comparaciones_con_fechahoras))
                    if bala_cables.count() > 0:
                        cantidad = bala_cables.sum('peso')
                    else:
                        cantidad = 0.0
                except Exception, msg:      # Lo que sea. Error psycopg,
                                            # interno de sqlobjet, lo que sea.
                    myprint("pclases.py: get_stock: Error contando existencias en balas de cable de productoVentaID %d. Excepción: %s" % (self.id, msg))
                    cantidad = 0.0
            elif self.es_rollo_c():
                try:
                    if not hasta:
                        #rollos_c = RolloC.select("""
                        #    rollo_c.id IN (
                        #        SELECT articulo.rollo_c_id
                        #        FROM articulo
                        #        WHERE articulo.albaran_salida_id IS NULL
                        #        AND articulo.producto_venta_id = %d
                        #        AND NOT articulo.rollo_c_id IS NULL)
                        #""" % (self.id))
                        if not almacen:
                            rollos_c = RolloC.select("""
                                rollo_c.id IN (
                                    SELECT articulo.rollo_c_id
                                    FROM articulo
                                    WHERE NOT articulo.almacen_id IS NULL
                                      AND articulo.producto_venta_id = %d
                                      AND NOT articulo.rollo_c_id IS NULL)
                            """ % (self.id))
                        else:
                            rollos_c = RolloC.select("""
                                rollo_c.id IN (
                                    SELECT articulo.rollo_c_id
                                    FROM articulo
                                    WHERE articulo.almacen_id  = %d
                                      AND articulo.producto_venta_id = %d
                                      AND NOT articulo.rollo_c_id IS NULL)
                            """ % (almacen.id, self.id))
                    else:
                        articulos = self._get_articulos_en_fecha_en_almacen(
                                    hasta, almacen, tipo = RolloC)
                        rollos_c = SQLtuple([a.rolloC for a in articulos
                                                if a.rolloCID != None])
                        #fecha = hasta.strftime('%Y-%m-%d')
                        #albaranes_de_salida_despues_de_fecha = """
                        #SELECT albaran_salida.id
                        #FROM albaran_salida
                        #WHERE albaran_salida.fecha > '%s'
                        #""" % (fecha)
                        #fecha_limite_para_comparaciones_con_fechahoras = (hasta + mx.DateTime.oneDay).strftime('%Y-%m-%d')
                        #rollos_c = RolloC.select("""
                        #    rollo_c.id IN (
                        #        SELECT articulo.rollo_c_id
                        #        FROM articulo
                        #        WHERE articulo.producto_venta_id = %d
                        #        AND articulo.rollo_c_id IS NOT NULL
                        #        AND (articulo.albaran_salida_id IS NULL
                        #             OR articulo.albaran_salida_id IN (%s)))
                        #    AND rollo_c.fechahora < '%s'
                        #""" % (self.id,
                        #       albaranes_de_salida_despues_de_fecha,
                        #       fecha_limite_para_comparaciones_con_fechahoras))
                    if rollos_c.count() > 0:
                        cantidad = rollos_c.sum('peso')
                    else:
                        cantidad = 0.0
                except Exception, msg:      # Lo que sea. Error psycopg,
                                            # interno de sqlobjet, lo que sea.
                    myprint("pclases.py: get_stock: Error contando existencias "\
                          "en rollos_c de productoVentaID %d. Excepción: "\
                          "%s" % (self.id, msg))
                    cantidad = 0.0
            elif self.es_especial():
                cantidad = self.camposEspecificosEspecial.stock
            elif self.es_caja():
                try:
                    if not hasta:
                        if not almacen:
                            cajas = Caja.select("""
                             caja.id IN (SELECT articulo.caja_id
                                         FROM articulo
                                         WHERE articulo.almacen_id IS NOT NULL
                                           AND articulo.producto_venta_id = %d
                                           AND NOT articulo.caja_id IS NULL)
                             """ % (self.id))
                        else:
                            cajas = Caja.select("""
                             caja.id IN (SELECT articulo.caja_id
                                         FROM articulo
                                         WHERE articulo.almacen_id = %d
                                           AND articulo.producto_venta_id = %d
                                           AND NOT articulo.caja_id IS NULL)
                             """ % (almacen.id, self.id))
                    else:
                        articulos = self._get_articulos_en_fecha_en_almacen(
                                    hasta, almacen, tipo = Caja)
                        cajas = SQLtuple([a.caja for a in articulos
                                            if a.cajaID != None])
                    if cajas.count() > 0:
                        cantidad = sum([c.peso for c in cajas])
                    else:
                        cantidad = 0.0
                except Exception, msg:  # Lo que sea. Error psycopg, interno
                                        # de sqlobjet, lo que sea.
                    myprint("pclases.py: get_stock: Error contando existencias en cajas de productoVentaID %d: %s" % (self.id, msg))
                    cantidad = 0.0
            else:
                myprint("pclases::ProductoVenta::get_stock: ERROR: El producto "\
                      "de venta %s no es ni rollo ni bigbag ni caja ni bala "\
                      "de cable. Verificar." % (self.id))
                cantidad = 0.0
            if actualizar:
                self._agregar_a_historico(hasta, cantidad = cantidad)
        return cantidad

    get_cantidad = get_stock

    existencias = property(get_existencias)
    stock = property(get_stock)

    def get_str_stock(self, precision = 1):
        """
        Devuelve las existencias (stock) en unidades (kilos o metros) como
        cadena.
        """
        # TODO: ¿Y por almacén?
        stock = self.stock
        unidad = self.get_str_unidad_de_venta()
        return "%s %s" % (utils.float2str(stock, precision), unidad)

    def get_str_existencias(self):
        """
        Devuelve las existencias (bultos) como cadena.
        """
        # TODO: ¿Y por almacén?
        existencias = self.existencias
        if self.es_rollo() or self.es_rollo_c():
            unidad = "rollos"
        elif self.es_bala():
            unidad = "balas"
        elif self.es_bigbag():
            unidad = "bigbags"
        elif self.es_caja():
            unidad = "bolsa"
        elif self.es_especial():
            unidad = self.camposEspecificosEspecial.unidad
        else:
            unidad = ""
        return "%d %s" % (existencias, unidad)

    def get_cantidad_A_actuales_todos_almacenes(self):
        if self.es_bala():
            try:
                res = Bala.select("""
                        id IN (SELECT bala_id
                               FROM articulo
                               WHERE producto_venta_id = %d
                                AND almacen_id IS NOT NULL)
                            AND claseb = FALSE
                        """ % (self.id)).sum("pesobala")
            except TypeError:   # No pudo hacer el sum porque no
                                # había registros.
                res = 0.0
            if res is None:
                res = 0.0
        elif self.es_rollo():
            rollos = Rollo.select("""
                        id IN (SELECT rollo_id
                               FROM articulo
                               WHERE producto_venta_id = %d
                                AND almacen_id IS NOT NULL)
                            AND rollob = FALSE """ % (self.id)).count()
            res = rollos * self.camposEspecificosRollo.metros_cuadrados
        elif self.es_bigbag():
            try:
                res = Bigbag.select("""
                        id IN (SELECT bigbag_id
                               FROM articulo
                               WHERE producto_venta_id = %d
                                AND almacen_id IS NOT NULL)
                            AND claseb = FALSE
                        """ % (self.id)).sum("pesobigbag")
            except TypeError:       # No pudo hacer el sum porque
                                    # no había registros.
                res = 0.0
            if res is None:
                res = 0.0
        elif self.es_caja():
            try:
                res = Caja.select("""
                        id IN (SELECT caja_id
                               FROM articulo
                               WHERE producto_venta_id = %d
                                AND almacen_id IS NOT NULL)
                            AND NOT caja_es_clase_b(id)
                        """ % (self.id)).sum("peso")
                #res = sum([c.peso for c in res if not c.claseb])
            except TypeError:       # No pudo hacer el sum porque no
                                    # había registros.
                res = 0.0
            if res is None:
                res = 0.0
        else:
            res = 0.0
        return res

    def get_cantidad_A_actuales_de_almacen(self, almacen):
        if self.es_bala():
            try:
                res = Bala.select("""
                        id IN (SELECT bala_id
                               FROM articulo
                               WHERE producto_venta_id = %d
                                AND almacen_id = %d)
                            AND claseb = FALSE
                        """%(self.id, almacen.id)).sum("pesobala")
            except TypeError:   # No pudo hacer el sum porque no
                                # había registros.
                res = 0.0
            if res is None:
                res = 0.0
        elif self.es_rollo():
            rollos = Rollo.select("""
                        id IN (SELECT rollo_id
                               FROM articulo
                               WHERE producto_venta_id = %d
                                AND almacen_id = %d)
                            AND rollob = FALSE """ % (
                        self.id, almacen.id)).count()
            res = rollos * self.camposEspecificosRollo.metros_cuadrados
        elif self.es_bigbag():
            try:
                res = Bigbag.select("""
                        id IN (SELECT bigbag_id
                               FROM articulo
                               WHERE producto_venta_id = %d
                                AND almacen_id  = %d)
                            AND claseb = FALSE
                        """%(self.id,almacen.id)).sum("pesobigbag")
            except TypeError:       # No pudo hacer el sum porque no
                                    # había registros.
                res = 0.0
            if res is None:
                res = 0.0
        elif self.es_caja():
            try:
                res = Caja.select("""
                        id IN (SELECT caja_id
                               FROM articulo
                               WHERE producto_venta_id = %d
                                AND almacen_id  = %d)
                            AND NOT caja_es_clase_b(id)
                        """ % (self.id, almacen.id)).sum("peso")
                #res = sum([c.peso for c in res if not c.claseb])
                        #""" % (self.id, almacen.id)).sum("peso")
            except TypeError:       # No pudo hacer el sum porque no
                                    # había registros.
                res = 0.0
            if res is None:
                res = 0.0
        else:
            res = 0.0
        return res

    def get_stock_A(self, hasta = None, forzar = False, actualizar = True,
                    contar_defectuosos = False, almacen = None):
        """
        Devuelve el stock (existencias en kg o m²) de clase A del producto
        de venta.
        NOTA: Las balas de cable y los geotextiles «C» no se consideran ni
              A ni B. Son simplemente otro tipo de producto. Desechos.
              Los rolloDefectuoso (rollos X) se consideran B por tener un
              largo inferior al estándar.
        """
        if not hasta or hasta >= mx.DateTime.localtime():
            if not almacen:     # Todos los almacenes
                res = self.get_cantidad_A_actuales_todos_almacenes()
            else:   # Pregunta por un almacén concreto.
                res = self.get_cantidad_A_actuales_de_almacen(almacen)
        else:   # Hasta != None. Quiero una fecha concreta
            if not almacen:
                res = self.__sum_llamada_recursiva_por_almacen_stock(
                                                            hasta, forzar,
                                                            actualizar,
                                                            contar_defectuosos,
                                                            almacen,
                                                            "A")
            else:   # Almacén está instanciado a != None
                if forzar:
                    res = self.get_cantidad_A_en_fecha(fecha = hasta,
                                                       almacen = almacen)
                    bultos = self.get_bultos_A_en_fecha(fecha = hasta,
                                                        almacen = almacen)
                else:   # Not forzar. Buscar en caché.
                    reg = HistorialExistenciasA.get_registro(self,
                                                             hasta,
                                                             almacen)
                    if not reg:
                        actualizar = True
                        res = self.get_stock_A(hasta = hasta,
                                    forzar = True,
                                    actualizar = False,
                                    contar_defectuosos = contar_defectuosos,
                                    almacen = almacen)
                        bultos = self.get_existencias_A(hasta = hasta,
                                    forzar = True,
                                    actualizar = False,
                                    contar_defectuosos = contar_defectuosos,
                                    almacen = almacen)
                    else:   # Sí existe caché.
                        res = reg.cantidad
                        bultos = reg.bultos
                        actualizar = False  # No tiene sentido. Son los mismos
                                            # datos que ya hay en la caché.
                if actualizar:
                    HistorialExistenciasA.actualizar(self,
                                                bultos = bultos,
                                                cantidad = res,
                                                fecha = hasta,
                                                almacen = almacen)
        return res

    def get_stock_kg_A(self, hasta = None, forzar = False, actualizar = True,
                       contar_defectuosos = False, almacen = None):
        """
        Devuelve el stock en kg de clase A del producto de venta.
        """
        if self.es_rollo():
            # No cuento rollos defecuosos, que por definición son B.
            articulos = self._get_articulos_en_fecha_en_almacen(
                    hasta, almacen, tipo = Rollo)
            # XXX: No cuento peso_sin (que cuadraría con la producción) porque
            # a la hora de vender y pesar la mercancía, se hace con embalaje.
            res = sum([a.peso for a in articulos if a.es_clase_a()])
            # Pero de todas maneras filtro aquí por si se ha colado un B como
            # rollo normal (no RolloDefectuoso)
        else:
            # Los rollos A y B son los únicos que se cuentan en m². Lo demás
            # en Kg. Así que paso la llamada a la original.
            res = self.get_stock_A(hasta, forzar, actualizar,
                                   contar_defectuosos, almacen)
        return res

    def get_stock_kg_B(self, hasta = None, forzar = False, actualizar = True,
                       contar_defectuosos = False, almacen = None):
        """
        Devuelve el stock en kg de clase B del producto de venta.
        """
        # TODO: Esto va a tardar...
        if self.es_rollo():
            # Aunque en teoría todo lo B está en RolloDefectuoso, ya nos vamos
            # conociendo...
            articulos1 = self._get_articulos_en_fecha_en_almacen(
                    hasta, almacen, tipo = Rollo)
            articulos2 = self._get_articulos_en_fecha_en_almacen(
                    hasta, almacen, tipo = RolloDefectuoso)
            # XXX: No cuento peso_sin (que cuadraría con la producción) porque
            # a la hora de vender y pesar la mercancía, se hace con embalaje.
            res = sum([a.peso for a in articulos1 if a.es_clase_b()])
            res += sum([a.peso for a in articulos2 if a.es_clase_b()])
        else:
            # Los rollos A y B son los únicos que se cuentan en m². Lo demás
            # en Kg. Así que paso la llamada a la original.
            res = self.get_stock_B(hasta, forzar, actualizar,
                                   contar_defectuosos, almacen)
        return res

    def get_stock_kg_C(self, hasta = None, forzar = False, actualizar = True,
                       contar_defectuosos = False, almacen = None):
        """
        La clase C siempre se cuenta en Kg. En todo. Hasta en geotextiles;
        porque no se puede precisar los m² al ser de ancho variable, restos,
        etc.
        """
        return self.get_stock_C(hasta, forzar, actualizar,
                                contar_defectuosos, almacen)

    def get_cantidad_B_actuales_todos_almacenes(self):
        if self.es_bala():
            try:
                res = Bala.select("""
                        id IN (SELECT bala_id
                               FROM articulo
                               WHERE producto_venta_id = %d
                                AND almacen_id IS NOT NULL)
                            AND partida_carga_id IS NULL
                            AND claseb = TRUE
                        """ % (self.id)).sum("pesobala")
            except TypeError:   # No pudo hacer el sum porque no
                                # había registros.
                res = 0.0
            if res is None:
                res = 0.0
        elif self.es_rollo():
            rollos = RolloDefectuoso.select("""
                        id IN (SELECT rollo_defectuoso_id
                               FROM articulo
                               WHERE producto_venta_id = %d
                               AND almacen_id IS NOT NULL)
                        """ % (self.id))
            res = sum([r.ancho * r.metrosLineales for r in rollos])
        elif self.es_bigbag():
            try:
                res = Bigbag.select("""
                        id IN (SELECT bigbag_id
                               FROM articulo
                               WHERE producto_venta_id = %d
                                AND almacen_id IS NOT NULL)
                            AND claseb = TRUE
                        """ % (self.id)).sum("pesobigbag")
            except TypeError:       # No pudo hacer el sum porque no
                                    # había registros.
                res = 0.0
            if res is None:
                res = 0.0
        elif self.es_caja():
            try:
                res = Caja.select("""
                        id IN (SELECT caja_id
                               FROM articulo
                               WHERE producto_venta_id = %d
                                AND almacen_id IS NOT NULL)
                            AND caja_es_clase_b(id)
                        """ % (self.id)).sum("peso")
            except TypeError:       # No pudo hacer el sum porque no
                                    # había registros.
                res = 0.0
            if res is None:
                res = 0.0
        else:
            res = 0.0
        return res

    def get_cantidad_B_actuales_de_almacen(self, almacen):
        if self.es_bala():
            try:
                res = Bala.select("""
                        id IN (SELECT bala_id
                               FROM articulo
                               WHERE producto_venta_id = %d
                                AND almacen_id = %d)
                            AND partida_carga_id IS NULL
                            AND claseb = TRUE
                        """ % (self.id, almacen.id)).sum("pesobala")
            except TypeError:       # No pudo hacer el sum porque no
                                    # había registros.
                res = 0.0
            if res is None:
                res = 0.0
        elif self.es_rollo():
            rollos = RolloDefectuoso.select("""
                        id IN (SELECT rollo_defectuoso_id
                               FROM articulo
                               WHERE producto_venta_id = %d
                                 AND almacen_id = %d)
                        """ % (self.id, almacen.id))
            res = sum([r.ancho * r.metrosLineales for r in rollos])
        elif self.es_bigbag():
            try:
                res = Bigbag.select("""
                        id IN (SELECT bigbag_id
                               FROM articulo
                               WHERE producto_venta_id = %d
                                 AND almacen_id = %d)
                            AND claseb = TRUE
                        """ % (self.id, almacen.id)).sum("pesobigbag")
            except TypeError:       # No pudo hacer el sum porque no
                                    # había registros.
                res = 0.0
            if res is None:
                res = 0.0
        elif self.es_caja():
            try:
                res = Caja.select("""
                        id IN (SELECT caja_id
                               FROM articulo
                               WHERE producto_venta_id = %d
                                 AND almacen_id = %d)
                            AND caja_es_clase_b(id)
                        """ % (self.id, almacen.id)).sum("peso")
            except TypeError:       # No pudo hacer el sum porque no
                                    # había registros.
                res = 0.0
            if res is None:
                res = 0.0
        else:
            res = 0.0
        return res

    def get_stock_B(self, hasta = None, forzar = False, actualizar = True,
                    contar_defectuosos = False, almacen = None):
        """
        Devuelve el stock (existencias en kg o m²) de clase B del producto de
        venta.
        OJO: En el caso de los rollos devuelve los rollos defectuosos. En el
        diseño de la BD (no tanto a nivel conceptual) los rollos B no son
        lo mismo que los rollos defectuosos. No debería darse el caso -ya que
        no existe posibilidad en la interfaz de crear rollos B- de que
        rollos_A (R) + rollos_B (X) + rollos_defectuosos (Y)
        != rollos_A + rollos_defectuosos != rollos totales (existencias del
        producto).
        [... meses más tarde ...] WTF? ¿Qué he querido decir con esa
        triple desigualdad? ¡Claro que se pueden crear rollos X desde los
        partes de producción! [... End Of Meses más tarde ...]
        NOTA: Las balas de cable y los geotextiles «C» no se consideran ni
              A ni B. Son simplemente otro tipo de producto. Desechos.
        [... más meses más tarde ...] Pues no. Rollos X sí se pueden crear,
        pero no objetos pclases.Rollo con claseb = True. A eso me refería.
        [... end of más meses más tarde ...]
        """
        if not hasta or hasta >= mx.DateTime.localtime():
            if not almacen:     # Todos los almacenes
                res = self.get_cantidad_B_actuales_todos_almacenes()
            else:   # Pregunta por un almacén concreto.
                res = self.get_cantidad_B_actuales_de_almacen(almacen)
        else:   # Quiero una fecha concreta.
            if not almacen:
                res = self.__sum_llamada_recursiva_por_almacen_stock(
                                                            hasta, forzar,
                                                            actualizar,
                                                            contar_defectuosos,
                                                            almacen,
                                                            "B")
            else:   # Almacen está instanciado a != None.
                if forzar:
                    res = self.get_cantidad_B_en_fecha(fecha = hasta,
                                                       almacen = almacen)
                    bultos = self.get_bultos_B_en_fecha(fecha = hasta,
                                                        almacen = almacen)
                else:   # No forzar. Buscar en caché.
                    reg = HistorialExistenciasB.get_registro(self,
                                                             hasta,
                                                             almacen)
                    if not reg: # No existe caché.
                        actualizar = True
                        res = self.get_stock_B(hasta = hasta,
                                forzar = True,
                                actualizar = False,
                                contar_defectuosos = contar_defectuosos,
                                almacen = almacen)
                        bultos = self.get_existencias_B(hasta = hasta,
                                forzar = True,
                                actualizar = False,
                                contar_defectuosos = contar_defectuosos,
                                almacen = almacen)
                    else:
                        res = reg.cantidad
                        bultos = reg.bultos
                        actualizar = False
                if actualizar:
                    HistorialExistenciasB.actualizar(self,
                                                     bultos = bultos,
                                                     cantidad = res,
                                                     fecha = hasta,
                                                     almacen = almacen)
        return res

    def get_cantidad_C_actuales_todos_almacenes(self):
        if self.es_bala_cable():
            # NOTA: Se ignora el campo claseb de las balas de cable.
            try:
                res = BalaCable.select("""
                        id IN (SELECT bala_cable_id
                               FROM articulo
                               WHERE producto_venta_id = %d
                                AND almacen_id IS NOT NULL)
                        """ % (self.id)).sum("peso")
            except TypeError:   # No pudo hacer el sum porque no
                                # había registros.
                res = 0.0
            if res is None:
                res = 0.0
        elif self.es_rollo_c():
            try:
                res = RolloC.select("""
                        id IN (SELECT rollo_c_id
                               FROM articulo
                               WHERE producto_venta_id = %d
                                AND almacen_id IS NOT NULL)
                        """ % (self.id)).sum("peso")
            except TypeError:       # No pudo hacer el sum porque
                                    # no había registros.
                res = 0.0
            if res is None:
                res = 0.0
        else:
            res = 0.0
        return res

    def get_cantidad_C_actuales_de_almacen(self, almacen):
        if self.es_bala_cable():
            try:
                res = BalaCable.select("""
                        id IN (SELECT bala_cable_id
                               FROM articulo
                               WHERE producto_venta_id = %d
                                AND almacen_id = %d)
                    """ % (self.id, almacen.id)).sum("peso")
            except TypeError:   # No pudo hacer el sum porque no
                                # había registros.
                res = 0.0
            if res is None:
                res = 0.0
        elif self.es_rollo_c():
            try:
                res = RolloC.select("""
                        id IN (SELECT rollo_c_id
                               FROM articulo
                               WHERE producto_venta_id = %d
                                AND almacen_id = %d)
                        """ % (self.id, almacen.id)).sum("peso")
            except TypeError:       # No pudo hacer el sum porque
                                    # no había registros.
                res = 0.0
            if res is None:
                res = 0.0
        else:
            res = 0.0
        return res

    def get_stock_C(self, hasta = None, forzar = False, actualizar = True,
                    contar_defectuosos = False, almacen = None):
        """
        PLAN: Habrá un get_*_C para aquellos productos cuyas existencias no
        pueden ser consideradas A (primera calidad) ni B (baja calidad pero
        vendible en determinadas circunstancias). Estos productos son los
        rollos C (mezcla de geotextiles almacenados en forma de rollo) y las
        balas de cable (restos de fibra que se embalan para reciclar o
        almacenar temporalmente).
        Hasta entonces se contarán como clase B.
        """
        if not hasta or hasta >= mx.DateTime.localtime():
            if not almacen:     # Todos los almacenes
                res = self.get_cantidad_C_actuales_todos_almacenes()
            else:   # Pregunta por un almacén concreto.
                res = self.get_cantidad_C_actuales_de_almacen(almacen)
        else:   # Hasta != None. Quiero una fecha concreta
            if not almacen:
                res = self.__sum_llamada_recursiva_por_almacen_stock(
                                                            hasta, forzar,
                                                            actualizar,
                                                            contar_defectuosos,
                                                            almacen,
                                                            "C")
            else:   # Almacen está instanciado a != None.
                if forzar:
                    res = self.get_cantidad_C_en_fecha(fecha = hasta,
                                                       almacen = almacen)
                    bultos = self.get_bultos_C_en_fecha(fecha = hasta,
                                                        almacen = almacen)
                else:   # No forzar. Buscar en caché.
                    reg = HistorialExistenciasC.get_registro(self,
                                                             hasta,
                                                             almacen)
                    if not reg: # No existe caché.
                        actualizar = True
                        res = self.get_stock_C(hasta = hasta,
                                forzar = True,
                                actualizar = False,
                                contar_defectuosos = contar_defectuosos,
                                almacen = almacen)
                        bultos = self.get_existencias_C(hasta = hasta,
                                forzar = True,
                                actualizar = False,
                                contar_defectuosos = contar_defectuosos,
                                almacen = almacen)
                    else:
                        res = reg.cantidad
                        bultos = reg.bultos
                        actualizar = False
                if actualizar:
                    HistorialExistenciasC.actualizar(self,
                                                     bultos = bultos,
                                                     cantidad = res,
                                                     fecha = hasta,
                                                     almacen = almacen)
        return res

    def get_bultos_A_actuales_todos_almacenes(self):
        """
        Devuelve el número de bultos que hay actualmente en todos los
        almacenes.
        """
        if self.es_bala():
            res = Bala.select("""
                id IN (SELECT bala_id
                         FROM articulo
                        WHERE producto_venta_id = %d
                          -- AND albaran_salida_id IS NULL
                          AND almacen_id IS NOT NULL)
                AND partida_carga_id IS NULL
                AND claseb = FALSE """ % (self.id)).count()
        elif self.es_rollo():
            rollos = Rollo.select("""
                id IN (SELECT rollo_id
                         FROM articulo
                        WHERE producto_venta_id = %d
                          AND almacen_id IS NOT NULL)
                          AND rollob = FALSE """ % (self.id)).count()
            res = rollos
        elif self.es_bigbag():
            res = Bigbag.select("""
                id IN (SELECT bigbag_id
                         FROM articulo
                        WHERE producto_venta_id = %d
                          AND almacen_id IS NOT NULL)
                          AND claseb = FALSE """ % (self.id)).count()
        elif self.es_caja():
            res = Caja.select("""
                id IN (SELECT caja_id
                         FROM articulo
                        WHERE producto_venta_id = %d
                          AND almacen_id IS NOT NULL)
                          AND NOT caja_es_clase_b(id)
                              """ % (self.id)).count()
        else:
            res = 0
        return res

    def get_bultos_A_actuales_de_almacen(self, almacen):
        if self.es_bala():
            res = Bala.select(""" id IN (SELECT bala_id
                                         FROM articulo
                                         WHERE producto_venta_id = %d
                                           AND almacen_id = %d)
                                 AND partida_carga_id IS NULL
                                 AND claseb = FALSE """ % (
                              self.id, almacen.id)).count()
        elif self.es_rollo():
            rollos = Rollo.select(""" id IN (SELECT rollo_id
                                             FROM articulo
                                             WHERE producto_venta_id = %d
                                              AND almacen_id = %d)
                                      AND rollob = FALSE """ % (
                                  self.id, almacen.id)).count()
            res = rollos
        elif self.es_bigbag():
            res = Bigbag.select(""" id IN (SELECT bigbag_id
                                           FROM articulo
                                           WHERE producto_venta_id = %d
                                             AND almacen_id = %d)
                                    AND claseb = FALSE """ % (
                                self.id, almacen.id)).count()
        elif self.es_caja():
            res = Caja.select(""" id IN (SELECT caja_id
                                           FROM articulo
                                           WHERE producto_venta_id = %d
                                             AND almacen_id = %d)
                                    AND NOT caja_es_clase_b(id) """ % (
                                self.id, almacen.id)).count()
        else:
            res = 0
        return res

    def get_bultos_A_en_fecha(self, fecha, almacen = None):
        """
        Devuelve el número de bultos de clase A que había en una fecha
        determinada en un almacén en concreto o en almacén en general,
        dependiendo de si almacen es None o no.
        """
        articulos = [a for a in self.articulos if
                     a.es_clase_a() and a.en_almacen(fecha, almacen)]
        res = len(articulos)
        del articulos
        return res

    def get_cantidad_A_en_fecha(self, fecha, almacen = None):
        """
        Devuelve la cantidad en unidades del producto que había en una fecha
        determinada en un almacén en concreto o en el almacén en general,
        dependiendo de si «almacen» es None o no.
        """
        stocks = [a.get_stock() for a in self.articulos if
                  a.es_clase_a() and a.en_almacen(fecha, almacen)]
        res = sum(stocks)
        del stocks
        return res

    def __sum_llamada_recursiva_por_almacen_existencias(self,
                                            hasta, forzar, actualizar,
                                            contar_defectuosos, almacen,
                                            tipo):
        """
        Devuelve la suma de existencias (bultos) del tipo especificado en
        "tipo" para la fecha indicada y en todos los almacenes.
        """
        assert isinstance(tipo, str) and tipo.upper() in ("A", "B", "C")
        res = 0
        func_get_existencias = getattr(self,
                                       "get_existencias_%s" % tipo.upper())
        for a in Almacen.select():
            res += func_get_existencias(hasta = hasta, forzar = forzar,
                            actualizar = actualizar,
                            contar_defectuosos = contar_defectuosos,
                            almacen = a)
        return res

    def __sum_llamada_recursiva_por_almacen_stock(self,
                                            hasta, forzar, actualizar,
                                            contar_defectuosos, almacen,
                                            tipo):
        """
        Devuelve la suma de stock (cantidad en unidades del producto) del
        tipo especificado en "tipo" para la fecha indicada y en todos los
        almacenes.
        """
        assert isinstance(tipo, str) and tipo.upper() in ("A", "B", "C")
        res = 0
        func_get_stock = getattr(self,
                                       "get_stock_%s" % tipo.upper())
        for a in Almacen.select():
            res += func_get_stock(hasta = hasta, forzar = forzar,
                            actualizar = actualizar,
                            contar_defectuosos = contar_defectuosos,
                            almacen = a)
        return res

    def get_existencias_A(self, hasta = None, forzar = False,
                          actualizar = True, contar_defectuosos = False,
                          almacen = None):
        """
        Devuelve las existencias (número de bultos) de clase A del producto de
        venta.
        NOTA: Las balas de cable y los geotextiles «C» no se consideran ni
              A ni B. Son simplemente otro tipo de producto. Desechos.
        Parámetros:
            hasta -> Fecha en la que contará las existencias.
            forzar -> Ignora el caché.
            actualizar -> Calcula y actualiza el caché.
            contar_defectuosos -> Por compatibilidad. Se ignora.
            almacén -> Almacén sobre el que cuenta las existencias. Si None,
                       devuelve la cantidad total entre todos los almacenes.
        """
        if not hasta or hasta >= mx.DateTime.localtime():
            if not almacen:
                res = self.get_bultos_A_actuales_todos_almacenes()
            else:
                res = self.get_bultos_A_actuales_de_almacen(almacen)
        else:   # Quiero una fecha concreta.
            if not almacen:
                res = self.__sum_llamada_recursiva_por_almacen_existencias(
                                                            hasta, forzar,
                                                            actualizar,
                                                            contar_defectuosos,
                                                            almacen,
                                                            "A")
            else:   # Almacén está instanciado a != None
                if DEBUG:
                    myprint("pclases::ProductoVenta:get_existencias_A "\
                          "-> almacen != None.")
                if forzar:
                    res = self.get_bultos_A_en_fecha(fecha = hasta,
                                                     almacen = almacen)
                    cantidad = self.get_cantidad_A_en_fecha(fecha = hasta,
                                                            almacen = almacen)
                else:   # Not forzar. Buscar en caché.
                    if DEBUG:
                        myprint("pclases::ProductoVenta:get_existencias_A "\
                              "-> Buscando en caché...")
                    reg = HistorialExistenciasA.get_registro(self,
                                                             hasta,
                                                             almacen)
                    if not reg: # No existe caché
                        if DEBUG:
                            myprint("pclases::ProductoVenta:get_existencias_A "\
                                  "-> Fallo de caché.")
                        actualizar = True
                        res = self.get_existencias_A(hasta = hasta,
                                    forzar = True,
                                    actualizar = False,
                                    contar_defectuosos = contar_defectuosos,
                                    almacen = almacen)
                        cantidad = self.get_stock_A(hasta = hasta,
                                    forzar = True,
                                    actualizar = False,
                                    contar_defectuosos = contar_defectuosos,
                                    almacen = almacen)
                    else:       # Sí existe caché
                        if DEBUG:
                            myprint("pclases::ProductoVenta:get_existencias_A "\
                                  "-> Registro de caché encontrado.")
                        res = reg.bultos
                        cantidad = reg.cantidad
                        actualizar = False  # No tiene sentido. Son los mismos
                                            # datos que ya hay en caché.
                if actualizar:
                    if DEBUG:
                        myprint("pclases::ProductoVenta:get_existencias_A "\
                              "-> Actualizando caché.")
                    HistorialExistenciasA.actualizar(self,
                                                bultos = res,
                                                cantidad = cantidad,
                                                fecha = hasta,
                                                almacen = almacen)
        return res

    def get_bultos_B_actuales_todos_almacenes(self):
        if self.es_bala():
            res = Bala.select("""
                id IN (SELECT bala_id
                         FROM articulo
                        WHERE producto_venta_id = %d
                          AND almacen_id IS NOT NULL)
                          AND partida_carga_id IS NULL
                          AND claseb = TRUE """ % (self.id)).count()
        elif self.es_rollo():
            rollos = RolloDefectuoso.select("""
                id IN (SELECT rollo_defectuoso_id
                       FROM articulo
                       WHERE producto_venta_id = %d
                         AND almacen_id IS NOT NULL)
                """ % (self.id)).count()
            res = rollos
        elif self.es_bigbag():
            res = Bigbag.select("""
                    id IN (SELECT bigbag_id
                             FROM articulo
                            WHERE producto_venta_id = %d
                              AND almacen_id IS NOT NULL)
                    AND claseb = TRUE """ % (self.id)).count()
        elif self.es_caja():
            res = Caja.select("""
                    id IN (SELECT caja_id
                            FROM articulo
                           WHERE producto_venta_id = %d
                             AND almacen_id IS NOT NULL)
                    AND caja_es_clase_b(id) """ % (self.id)).count()
        else:
            res = 0
        return res

    def get_bultos_B_actuales_de_almacen(self, almacen):
        if self.es_bala():
            res = Bala.select(""" id IN (SELECT bala_id
                                         FROM articulo
                                         WHERE producto_venta_id = %d
                                           AND almacen_id = %d)
                                 AND partida_carga_id IS NULL
                                 AND claseb = TRUE """ % (
                              self.id, almacen.id)).count()
        elif self.es_rollo():
            rollos = RolloDefectuoso.select("""
                id IN (SELECT rollo_defectuoso_id
                       FROM articulo
                       WHERE producto_venta_id = %d
                         AND almacen_id = %d)
                """ % (self.id, almacen.id)).count()
            res = rollos
        elif self.es_bigbag():
            res = Bigbag.select(""" id IN (SELECT bigbag_id
                                           FROM articulo
                                           WHERE producto_venta_id = %d
                                             AND almacen_id = %d)
                                    AND claseb = TRUE """ % (
                                self.id, almacen.id)).count()
        elif self.es_caja():
            res = Caja.select(""" id IN (SELECT caja_id
                                           FROM articulo
                                           WHERE producto_venta_id = %d
                                             AND almacen_id = %d)
                                    AND caja_es_clase_b(id)
                              """ % (
                                self.id, almacen.id)).count()
        else:
            res = 0
        return res

    def get_bultos_B_en_fecha(self, fecha, almacen = None):
        articulos = [1 for a in self.articulos if
                     a.es_clase_b() and a.en_almacen(fecha, almacen)]
        res = len(articulos)
        del articulos
        return res

    def get_cantidad_B_en_fecha(self, fecha, almacen = None):
        """
        Devuelve la cantidad en unidades del producto que había en una fecha
        determinada en un almacén en concreto o en el almacén en general,
        dependiendo de si «almacen» es None o no.
        """
        articulos = [a for a in self.articulos if
                     a.es_clase_b() and a.en_almacen(fecha, almacen)]
        res = sum([a.cantidad for a in articulos])
        del articulos
        return res

    def get_existencias_B(self, hasta = None, forzar = False,
                          actualizar = True, contar_defectuosos = False,
                          almacen = None):
        """
        Devuelve las existencias (número de bultos) de clase B del producto de
        venta.
        OJO: En el caso de los rollos devuelve los rollos defectuosos. En el
        diseño de la BD (no tanto a nivel conceptual) los rollos B no son lo
        mismo que los rollos defectuosos. No debería darse el caso -ya que no
        existe posibilidad en la interfaz de crear rollos B- de que
        rollos_A + rollos_B + rollos_defectuosos
        != rollos_A + rollos_defectuosos != rollos totales
        (existencias del producto).
        NOTA: Las balas de cable y los geotextiles «C» no se consideran ni
              A ni B. Son simplemente otro tipo de producto. Desechos.
        """
        if not hasta or hasta >= mx.DateTime.localtime():
            if not almacen:
                res = self.get_bultos_B_actuales_todos_almacenes()
            else:
                res = self.get_bultos_B_actuales_de_almacen(almacen)
        else:   # Quiero una fecha concreta.
            if not almacen:
                res = self.__sum_llamada_recursiva_por_almacen_existencias(
                                                            hasta, forzar,
                                                            actualizar,
                                                            contar_defectuosos,
                                                            almacen,
                                                            "B")
            else:   # Almacén está instanciado a != None
                if forzar:
                    res = self.get_bultos_B_en_fecha(fecha = hasta,
                                                     almacen = almacen)
                    cantidad = self.get_cantidad_B_en_fecha(fecha = hasta,
                                                            almacen = almacen)
                else:   # Not forzar. Buscar en caché.
                    reg = HistorialExistenciasB.get_registro(self,
                                                             hasta,
                                                             almacen)
                    if not reg: # No existe caché
                        actualizar = True
                        res = self.get_existencias_B(hasta = hasta,
                                    forzar = True,
                                    actualizar = False,
                                    contar_defectuosos = contar_defectuosos,
                                    almacen = almacen)
                        cantidad = self.get_stock_B(hasta = hasta,
                                    forzar = True,
                                    actualizar = False,
                                    contar_defectuosos = contar_defectuosos,
                                    almacen = almacen)
                    else:       # Sí existe caché
                        res = reg.bultos
                        cantidad = reg.cantidad
                        actualizar = False  # No tiene sentido. Son los mismos
                                            # datos que ya hay en caché.
                if actualizar:
                    HistorialExistenciasB.actualizar(self,
                                                bultos = res,
                                                cantidad = cantidad,
                                                fecha = hasta,
                                                almacen = almacen)
        return res

    def get_bultos_C_actuales_todos_almacenes(self):
        if self.es_bala_cable():
            res = BalaCable.select("""
                id IN (SELECT bala_cable_id
                         FROM articulo
                        WHERE producto_venta_id = %d
                          AND almacen_id IS NOT NULL)
                """ % self.id).count()
        elif self.es_rollo_c():
            rollos = RolloC.select("""
                id IN (SELECT rollo_c_id
                         FROM articulo
                        WHERE producto_venta_id = %d
                          AND almacen_id IS NOT NULL)
                """ % (self.id)).count()
            res = rollos
        else:
            res = 0
        return res

    def get_bultos_C_actuales_de_almacen(self, almacen):
        if self.es_bala_cable():
            res = BalaCable.select(""" id IN (SELECT bala_cable_id
                                         FROM articulo
                                         WHERE producto_venta_id = %d
                                           AND almacen_id = %d) """ % (
                                    self.id, almacen.id)).count()
        elif self.es_rollo_c():
            rollos = Rollo.select("""
                        id IN (SELECT rollo_c_id
                                 FROM articulo
                                WHERE producto_venta_id = %d
                                  AND almacen_id = %d)
                        """ % (self.id, almacen.id)).count()
            res = rollos
        else:
            res = 0
        return res

    def get_bultos_C_en_fecha(self, fecha, almacen = None):
        articulos = [1 for a in self.articulos if
                     a.es_clase_c() and a.en_almacen(fecha, almacen)]
        res = len(articulos)
        del articulos
        return res

    def get_cantidad_C_en_fecha(self, fecha, almacen = None):
        articulos = [a for a in self.articulos if
                     a.es_clase_c() and a.en_almacen(fecha, almacen)]
        res = sum([a.cantidad for a in articulos])
        del articulos
        return res

    def get_existencias_C(self, hasta = None, forzar = False,
                          actualizar = True, contar_defectuosos = False,
                          almacen = None):
        """
        PLAN: Habrá un get_*_C para aquellos productos cuyas existencias no
        pueden ser consideradas A (primera calidad) ni B (baja calidad pero
        vendible en determinadas circunstancias). Estos productos son los
        rollos C (mezcla de geotextiles almacenados en forma de rollo) y las
        balas de cable (restos de fibra que se embalan para reciclar o
        almacenar temporalmente).
        Hasta entonces se contarán como clase B.
        """
        if not hasta or hasta >= mx.DateTime.localtime():
            if not almacen:
                res = self.get_bultos_C_actuales_todos_almacenes()
            else:
                res = self.get_bultos_C_actuales_de_almacen(almacen)
        else:   # Quiero una fecha concreta.
            if not almacen:
                res = self.__sum_llamada_recursiva_por_almacen_existencias(
                                                            hasta, forzar,
                                                            actualizar,
                                                            contar_defectuosos,
                                                            almacen,
                                                            "C")
            else:   # Almacén está instanciado a != None
                if forzar:
                    res = self.get_bultos_C_en_fecha(fecha = hasta,
                                                     almacen = almacen)
                    cantidad = self.get_cantidad_C_en_fecha(fecha = hasta,
                                                            almacen = almacen)
                else:   # Not forzar. Buscar en caché.
                    reg = HistorialExistenciasC.get_registro(self,
                                                             hasta,
                                                             almacen)
                    if not reg: # No existe caché
                        actualizar = True
                        res = self.get_existencias_C(hasta = hasta,
                                    forzar = True,
                                    actualizar = False,
                                    contar_defectuosos = contar_defectuosos,
                                    almacen = almacen)
                        cantidad = self.get_stock_C(hasta = hasta,
                                    forzar = True,
                                    actualizar = False,
                                    contar_defectuosos = contar_defectuosos,
                                    almacen = almacen)
                    else:       # Sí existe caché
                        res = reg.bultos
                        cantidad = reg.cantidad
                        actualizar = False  # No tiene sentido. Son los mismos
                                            # datos que ya hay en caché.
                if actualizar:
                    HistorialExistenciasC.actualizar(self,
                                                bultos = res,
                                                cantidad = cantidad,
                                                fecha = hasta,
                                                almacen = almacen)
        return res

    def get_partidas(self, fechaini = None, fechafin = None):
        """
        Devuelve las partidas relacionadas con el producto actual (si es
        que hay alguna y el producto es un geotextil).
        Si fechaini o fechafin son distintas de None, filtra las partidas
        por su fecha de fabricación.
        """
        partidas = Partida.select("""
            id IN (SELECT partida_id
                   FROM rollo
                   WHERE id IN (SELECT rollo_id
                                FROM articulo
                                WHERE producto_venta_id = %d))
            """ % (self.id))
        res = [p for p in partidas]     # Aquí está toda la manteca (lento
            # como él solo, pero no queda otra. Hay que traerlas de la BD).
        if fechaini:
            tmp = []
            for p in res:
                ffab = p.get_fecha_fabricacion()
                if DEBUG:
                    myprint("pclases::ProductoVenta.get_partidas", \
                          ffab, fechaini, ffab >= fechaini)
                if ffab != None and ffab >= fechaini:
                    tmp.append(p)
            res = tmp
        if fechafin:
            tmp = []
            for p in res:
                ffab = p.get_fecha_fabricacion()
                if DEBUG:
                    myprint("pclases::ProductoVenta.get_partidas", \
                          ffab, fechaini, ffab >= fechaini)
                if ffab != None and ffab <= fechafin:
                    tmp.append(p)
            res = tmp
        res = list(res)   # Para que tenga "len" y demás.
        if DEBUG:
            myprint("pclases::ProductoVenta.get_partidas", len(res))
        return res

    def get_unidad(self):
        """
        Devuelve la unidad de medida del producto.
        """
        if self.es_rollo():
            unidad = "m²"
        elif (self.es_bala() or self.es_bigbag() or self.es_caja()
            or self.es_rollo_c() or self.es_bala_cable()):
            unidad = "kg"
        elif self.es_especial():
            unidad = self.camposEspecificosEspecial.unidad
        else:
            unidad = ""
        return unidad

    def get_str_unidad_de_venta(self):
        return self.get_unidad()

    unidad = property(get_unidad)

    def get_peso_teorico(self):
        """
        Devuelve el peso teórico del rollo (ancho * largo * densidad) en
        kilogramos.
        Si es caja, devuelve el peso teórico de la misma (sus artículos no
        tienen peso "real" porque no se pesan en la línea). Ojo: no del palé
        completo. Solo de una caja.
        Si es fibra, lanza excepción porque no hay definido un peso teórico
        estándar para esos productos.
        """
        try:
            return self.camposEspecificosRollo.peso_teorico
        except AttributeError:
            if self.es_caja():
                return (self.camposEspecificosBala.gramosBolsa
                        * self.camposEspecificosBala.bolsasCaja)
            else:
                if self.es_especial():
                    raise ValueError, "Los productos especiales no tienen"\
                                      " peso teórico."
                elif self.es_fibra():
                    raise ValueError, "Las balas de fibra no tienen peso "\
                                      "teórico."

cont, tiempo = print_verbose(cont, total, tiempo)

class StockAlmacen(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- almacenID = ForeignKey("Almacen")
    #--------------------------- productoCompraID = ForeignKey("ProductoCompra")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class StockEspecial(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- almacenID = ForeignKey("Almacen")
    #----- camposEspecificosEspecialID = ForeignKey("CamposEspecificosEspecial")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class LineaDeMovimiento(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------- albaranSalidaID = ForeignKey("AlbaranSalida")
    #--------------------------------------- articuloID = ForeignKey("Articulo")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_producto_venta(self):
        try:
            return self.articulo.productoVenta
        except AttributeError:
            return None

    productoVenta = property(get_producto_venta)

cont, tiempo = print_verbose(cont, total, tiempo)

class AlbaranSalida(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------- transportistaID = ForeignKey('Transportista')
    lineasDeVenta = MultipleJoin('LineaDeVenta')
    articulos = MultipleJoin('Articulo')
    #----------------------------------------- clienteID = ForeignKey('Cliente')
    lineasDeDevolucion = MultipleJoin('LineaDeDevolucion')
    servicios = MultipleJoin('Servicio')
    #----------------------------------------- destinoID = ForeignKey('Destino')
    transportesACuenta = MultipleJoin('TransporteACuenta')
    comisiones = MultipleJoin('Comision')
    documentos = MultipleJoin('Documento')
    #----------------------------------- almacenOrigenID = ForeignKey('Almacen',
    #--------------------- default = Almacen.get_almacen_principal_or_none() and
    #----------------------------- Almacen.get_almacen_principal_or_none().id or
    #--------------------------------------------------------------------- None)
    #------------------ almacenDestinoID = ForeignKey('Almacen', default = None)
    lineasDeMovimiento = MultipleJoin("LineaDeMovimiento")

    str_tipos = ("Movimiento", "Interno", "Normal", "Repuestos", "Vacío")
    MOVIMIENTO, INTERNO, NORMAL, REPUESTOS, VACIO = range(len(str_tipos))

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    @property
    def comercial(self):
        """
        Devuelve EL comercial relacionado con el pedido del que procede el
        albarán de salida.
        """
        for p in self.get_pedidos():
            if p.comercial:
                return p.comercial
        return None

    @property
    def provincia(self):
        """
        Devuelve la provincia de la dirección de envío del albarán. Por
        motivos históricos se guarda en el mismo campo que el código postal.
        """
        try:
            return " ".join(self.cp.split()[1:])
        except AttributeError:
            return ""

    @property
    def codigo_postal(self):
        """
        Devuelve únicamente el código postal de la dirección de envío del
        albarán. Por motivos históricos se guarda en el mismo campo junto con
        la provincia.
        """
        rexp_cp = re.compile("[\d]+")
        try:
            cp = rexp_cp.findall(self.cp)[0]
        except (IndexError, AttributeError):
            cp = ""
        return cp

    def cambiar_destino(self, almacen_destino = None):
        """Cambia el destino de un albarán. Si ya tenía cantidades asignadas,
        altera también sus existencias en cada almacén para ajustarlo a la
        realidad.
        Usar con precaución. Cambiar el destino de un albarán antiguo que
        tenga, por ejemplo, artículos trazables que se hayan movido a otro
        almacén para servirlos desde allí provocará una ruptura en la
        trazabilidad.

        Si el nuevo almacén es None, puede ser porque se cambia el tipo de
        albarán a uno normal con destino a un cliente. En ese caso simplemente
        corrige las existencias del almacén actual pero no aumenta en ningún
        otro.

        :almacen_destino: objeto Almacén o None.
        """
        # Para cada línea del albarán:
        #   - Si es producto de compra, aumenta las existencias en el nuevo
        #   almacén en la cantidad indicada por la línea de venta.
        #   - Si es producto de venta comprueba que esté en el almacén que
        #   tenía asignado el albarán antes del cambio. Si es así, entonces
        #   saca el artículo de allí y lo mete en el almacén recibido.
        # Y finalmente, si todo ha ido bien, cambia el propio almacén de
        # destino del albarán.
        for ldv in self.lineasDeVenta:
            producto = ldv.producto
            if isinstance(ldv.producto, ProductoCompra):
                cantidad = ldv.cantidad
                # Saco del que estaba:
                producto.add_existencias(cantidad, self.almacenDestino,
                        actualizar_global = True)
                # Aumento en el nuevo:
                if almacen_destino != None:
                    producto.add_existencias(cantidad, almacen_destino,
                            actualizar_global = True)
            elif isinstance(producto, ProductoVenta):
                pass    # Los recorremos después artículo por artículo.
        for a in self.articulos:
            if a.almacen:
                if a.almacen == self.almacen:
                    # Corrijo línea de movimiento y artículo
                    a.lineaDeMovimiento.almacen = almacen_destino
                    a.almacen = almacen_destino
                else:
                    # Ya no está en el almacén en el que estaba.
                    pass    # No sé si dar error o qué... Rompería la
                        # trazabilidad, pero abortar aquí el proceso
                        # sería peor. FIXME: Hacer un "rollback" o algo.
            else:   # Se vendió a un cliente.
                a.almacen = almacen_destino
        self.almacenDestino = almacen_destino

    def determinar_obra(self, ventana_padre = None, preguntar_usuario = False,
                        dejar_crear_nueva = False):
        """
        Devuelve la obra relacionada (o None) con el albarán a partir de
        los textos de obras que hay en los pedidos relacionados.
        En caso de duda pregunta al usuario mediante un cuadro de diálogo
        usando la ventana padre.
        Si ya tiene facturas devolverá la obra de sus facturas si es la
        misma. En otro caso preguntará al usuario.
        La opción de preguntar al usuario se puede omitir mediante el
        parámetro preguntar_usuario = False. En ese caso siempre devolverá
        None cuando no se pueda relacionar unívocamente una obra con el
        albarán.
        «dejar_crear_nueva» no tendrá efecto si «preguntar_usuario» es False.
        En otro caso el usuario podrá crear una nueva obra a través de
        ventanas de diálogo.
        """
        # NOTA: No me gusta mezclar así las capas y dejar que desde aquí se
        # interactúe con el GUI. Pero en este caso creo que está justificado.
        obras = self.determinar_obras()
        if len(obras) == 1:     # Solo una obra. No hay duda.
            res = obras[0]
        elif len(obras) > 1:    # Más de una.
            if preguntar_usuario: # Si hay que preguntarle al usuario...
                opciones = [(o.id, "%s (%s; %s - %s, %s)" % (o.nombre,
                                                             o.direccion,
                                                             o.cp,
                                                             o.ciudad,
                                                             o.provincia))
                            for o in obras]
                opciones.append((0, "Sin obra relacionada"))
                if dejar_crear_nueva:
                    opciones.append((-1, "Crear nueva obra"))
                respuesta = utils.dialogo_combo(titulo = "DETERMINAR OBRA",
                    texto = "Seleccione la obra que se corresponde con "
                            "el albarán %s:" % self.numalbaran,
                    padre = ventana_padre,
                    ops = opciones)
                if respuesta == 0:
                    res = None
                elif respuesta == -1:
                    nombre = utils.dialogo_entrada(titulo = "NUEVA OBRA",
                        texto = "Introduzca el nombre de la nueva obra:",
                        padre = ventana_padre)
                    if nombre:
                        res = Obra(nombre = nombre,
                                   generica = False) # Resto de valores, que
                            # se metan donde corresponda. Demasiado es esto ya.
                    else:
                        res = None
                else:
                    res = Obra.get(respuesta)
            else:   # Si no, devuelvo None.
                res = None
        else:   # No hay obras relacionadas.
            if preguntar_usuario:   # Si hay que preguntar...
                if dejar_crear_nueva:
                    opciones = [(0, "Sin obra relacionada")]
                    opciones.append((-1, "Crear nueva obra"))
                else:   # Si hay que preguntar pero no dejo crear y no hay
                        # opciones entre las que elegir, devuelvo None. No me
                        # me queda otra.
                    res = None
                respuesta = utils.dialogo_combo(titulo = "DETERMINAR OBRA",
                    texto = "Seleccione la obra que se corresponde con "
                            "el albarán %s:" % self.numalbaran,
                    padre = ventana_padre,
                    ops = opciones)
                if respuesta == 0:
                    res = None
                elif respuesta == -1:
                    nombre = utils.dialogo_entrada(titulo = "NUEVA OBRA",
                        texto = "Introduzca el nombre de la nueva obra:",
                        padre = ventana_padre)
                    if nombre:
                        res = Obra(nombre = nombre) # Resto de valores, que se
                            # metan donde corresponda. Demasiado es esto ya.
                    else:
                        res = None
                else:
                    res = Obra.get(respuesta)
            else:   # Si no, devuelvo None.
                res = None
        return res

    def determinar_obras(self, incluir_nones = False):
        """
        Devuelve una lista de objetos obra relacionados con el albarán
        actual mediante sus pedidos (guiándose por el texto del atributo
        «obra») y facturas.
        """
        res = []
        # Obras de pedidos:
        for p in self.get_pedidos():
            obra = p.obra
            if not obra:    # Si no tiene obra relacionada, intento adivinarla.
                obra = p.adivinar_obra()
            if ((incluir_nones and not obra) or obra) and obra not in res:
                res.append(obra)
        for f in self.get_facturas():
            obra = f.obra
            if ((incluir_nones and not obra) or obra) and obra not in res:
                res.append(obra)
        return res

    def get_pedidos(self):
        """
        Devuelve una lista de pedidos relacionados con el albarán actual.
        """
        res = []
        for ldv in self.lineasDeVenta:
            pedido = ldv.pedidoVenta
            if pedido and pedido not in res:
                res.append(pedido)
        for srv in self.servicios:
            pedido = srv.pedidoVenta
            if pedido and pedido not in res:
                res.append(pedido)
        return res

    def get_presupuestos(self):
        """
        Devuelve los presupuestos relacionados con el albarán actual.
        """
        presupuestos = []
        for pedido in self.get_pedidos():
            for presupuesto in pedido.get_presupuestos():
                if presupuesto not in presupuestos:
                    presupuestos.append(presupuesto)
        return presupuestos

    def es_de_repuestos(self):
        """
        Devuelve True si es un albarán de repuestos.
        Para ello debe cumplir que:
        1.- El cliente sea la propia empresa.
        2.- Contiene en las observaciones el texto "repuestos".
        """
        # TODO: Esto se convertirá en un boolean en la tabla cuando
        #       se pruebe a fondo.
        res = False
        idPropiaEmpresa = Cliente.id_propia_empresa_cliente()
        if idPropiaEmpresa != 0:
            res = self.clienteID == idPropiaEmpresa
            if res:
                res = "repuestos" in self.observaciones.lower()
        return res

    def es_de_movimiento(self):
        """
        Devuelve True si es un albarán de movimiento de mercancías entre
        almacenes.
        Para ello debe cumplir que:
        1.- Tenga almacén origen instanciado (por defecto, siempre lo estará).
        2.- Tenga almacén destino instanciado.
        NOTA: Un albarán puede ser interno y de movimiento a la vez. De hecho
        será lo normal, aunque se verifique las condiciones independientemente.
        """
        return bool(self.almacenOrigen and self.almacenDestino)

    def es_interno(self):
        """
        Devuelve si es un albarán interno de consumo de materiales o de fibra.
        No devuelve True si es un albarán de ajuste aunque el cliente sea la
        propia empresa.
        Es fundamental que no esté vacío para poder determinar si es interno.
        """
        # Condición para considerar un albarán como interno (hasta solucionar
        # el To-Do):
        #  1.- Que el cliente sea la propia empresa.
        #  2.- Si contiene artículos bala, que éstos (¡Todos!) pertenezcan a
        #      una partida de carga.
        #  3.- Si contiene productosCompra, que tenga el código "ALBINTPDPID"
        #      en las observaciones.
        #  4.- Que contenga al menos una bala, un bigbag o un producto de
        #      compra.
        #res = False
        #idPropiaEmpresa = id_propia_empresa_cliente()
        #if idPropiaEmpresa != 0:
        #    res = self.clienteID == idPropiaEmpresa
        #    tiene_balas = False
        #    tiene_productos_compra = False
        #    if res:
        #        for a in self.articulos:
        #            if a.es_bala():
        #                tiene_balas = True
        #                if a.bala.partidaCarga == None:
        #                    res = False
        #                    break
        #        if res:
        #            for ldv in self.lineasDeVenta:
        #                pc = ldv.productoCompra
        #                if pc != None:
        #                    tiene_productos_compra = True
        #                    res = "ALBINTPDPID" in self.observaciones
        #                    if not res:
        #                        break
        #    res = res and (tiene_balas or tiene_productos_compra)
        ## Toda esta lógica de negocio (¿quién coño puso de moda esa expresión tan pedante -y probablemente
        ## mal traducida del francés-?) ha pasado a la capa inferior: Ahora es un procedimiento almacenado
        ## en la BD. Aunque no compilado, es STABLE, por lo que sí está optimizado y vuela; sobre todo en
        ## comparación con el código de arriba.
        res = self._connection.queryOne(
                "SELECT es_interno(%d);" % self.id)[0] == 1
        ## ... Aunque en determinadas ocasiones, recorriendo una lista de 1560 albaranes, la consulta me
        ## ha llegado a dar un par de segundos por arriba. De todas formas la necesitaba como funcion SQL para
        ## la consulta de HistorialExistencias.
        # Para no cambiar la función de la BD, compruebo aquí:
        if not res:
            hay_un_bigbag_relacionado_con_un_parte = False
            hay_una_bala_reenvasada = False
            # XXX: Voy a tener que recorrer la lista de artículos. A tomar
            # por saco la optimización:
            # TODO: Optimizar y pasarlo a función de la BD, por los clavos de
            #       cristo.
            for a in self.articulos:
                # OJO: No vale con que tenga un bigbag, tiene que tener un
                # bigbag conectado con un parte donde se ha consumido. Pero no
                # conectado mediante el artículo (que todos los productos con
                # trazabilidad lo tienen), sino directamente entre BB y parte.
                if a.bigbagID and a.bigbag.parteDeProduccion:
                    hay_un_bigbag_relacionado_con_un_parte = True
                    break
                # O bien tiene al menos una bala que se ha consumido en
                # reenvasarla para sacar nueva(s) bala(s).
                elif a.bala and "ALBINTPDP" in self.observaciones:
                    hay_una_bala_reenvasada = True
                    break
            res = (hay_un_bigbag_relacionado_con_un_parte
                    or hay_una_bala_reenvasada)
        return res

    def comprobar_cantidades(self):
        """
        Devuelve True si las cantidades de las líneas de venta coinciden
        con las de los artículos del albarán para todos los productos
        del albarán agrupables en objetos Articulo.
        """
        prods_ldvs = {}
        prods_arts = {}
        # Suma de cantidades de LDVs.
        for ldv in self.lineasDeVenta:
            pv = ldv.productoVenta
            if pv != None and (pv.es_bala() or pv.es_bala_cable()
                or pv.es_bigbag() or pv.es_rollo() or pv.es_caja()):
                if pv not in prods_ldvs:
                    prods_ldvs[pv] = ldv.cantidad
                else:
                    prods_ldvs[pv] += ldv.cantidad
        # Suma de cantidades de artículos.
        for a in self.articulos + [ldd.articulo for ldd
                                    in self.lineasDeDevolucion]:
            pv = a.productoVenta
            if a.es_rollo() or a.es_rollo_defectuoso():
                cantidad = a.superficie
            elif (a.es_bala() or a.es_bala_cable() or a.es_bigbag()
                  or a.es_caja()):
                cantidad = a.peso
            else:
                myprint("pclases::AlbaranSalida::comprobar_cantidades -> El artículo ID %d no es bala [cable], ni bigbag ni caja ni rollo [defectuoso]." % (a.id))
                cantidad = 0
            if pv not in prods_arts:
                prods_arts[pv] = cantidad
            else:
                prods_arts[pv] += cantidad
        # Comprobación
        res = len(prods_arts) == len(prods_ldvs)
        for pv in prods_ldvs:
            if not res:
                break   # Ahorro iteraciones
            if pv not in prods_arts:
                res = False
            else:
                res = round(prods_arts[pv], 2) == round(prods_ldvs[pv], 2)
        if DEBUG and not res:
            myprint("prods_arts", prods_arts)
            myprint("prods_ldvs", prods_ldvs)
        return res

    def get_precio_pedido_con_descuento_para(self, articulo):
        """
        Devuelve el precio del pedido, incluyendo descuento, de la
        línea de pedido de venta correspondiente al artículo recibido.
        Lanza excepción ValueError si en el pedido no se solicitó el
        producto.
        """
        pv = articulo.productoVenta
        pedidos = self.get_pedidos()
        total_cantidad = 0
        total_importe = 0.0
        for p in pedidos:
            for ldp in p.lineasDePedido:
                if ldp.productoVenta == pv:
                    precio = ldp.precio * (1 - ldp.descuento)
                    cantidad = ldp.cantidad
                    total_importe += cantidad * precio
                    total_cantidad += cantidad
        # Si tiene varios precios, devuelvo la media de todos; puesto que
        # a priori es difícil determinar a qué LDV va a ir el artículo cuando
        # facture; y como lo normal es facturarlo todo, el total finalmente
        # coincidirá.
        try:
            precio_final = total_importe / total_cantidad
        except ZeroDivisionError:
            precio_final = pv.precioDefecto
        return precio_final

    def calcular_total(self, iva_incluido = False, segun_factura = True):
        """
        Devuelve el total del albarán basándose en la cantidad y
        precios de la LDV.
        El total no incluye IVA a no ser que se indique lo contrario.
        Si segun_factura es False, devuelve el total según el pedido (precios
        de allí, contando artículos individuales en vez de líneas de venta,
        etc,).
        Si es True (más rápido) se basa en las líneas de venta que compondrán
        la factura, es decir, que es solo válido para los cálculos justo ANTES
        de imprimir y cerrar el albarán, porque es cuando se ajustará al
        importe total real.
        """
        subtotal = 0.0
        # BUGFIX: ¡Así lo que hace es calcular el total DEL PEDIDO, vuvuzelo!
        #for ldv in self.lineasDeVenta:
        #    subtotal += ldv.precio * ldv.cantidad * (1 - ldv.descuento)
        for ldv in self.lineasDeVenta:
            if ldv.productoCompraID != None:    # No trazable. Cuento línea
                                                # del pedido.
                subtotal += ldv.precio * ldv.cantidad * (1 - ldv.descuento)
        if not segun_factura:
            for a in self.articulos:
                subtotal += (self.get_precio_pedido_con_descuento_para(a)
                             * a.cantidad)
        else:
            for ldv in self.lineasDeVenta:  # Cuento las líneas de venta que
                                            # se facturarán. No artículos
                                            # individuales.
                if ldv.productoVentaID: # Las de los productos de compra ya
                                        # lo he calculado antes.
                    subtotal += ldv.precio * ldv.cantidad * (1 - ldv.descuento)
        for srv in self.servicios:
            subtotal += srv.precio * srv.cantidad * (1 - srv.descuento)
        if iva_incluido:
            iva = self.cliente and self.cliente.get_iva_norm() or 0
        else:
            iva = 0
        total = subtotal * (1 + iva)
        return total

    def calcular_comisiones(self):
        """
        Calcula las comisiones del albarán solo si el mismo no está bloqueado.
        Primero mira si existe la comisión legítima correspondiente al
        comercial del cliente del albarán. Si no existe, la crea. Si existe,
        ajusta la cantidad al porcentaje de la valoración actual del albarán.
        Después, si existen más comisiones, recalcula también el precio de las
        mismas en base al porcentaje que tengan.
        """
        self.sync()
        if not self.bloqueado:
            valor_albaran = self.calcular_total()
            if self.cliente and self.cliente.cliente:
                comercial = self.cliente.cliente
                comision_comercial = [c for c in self.comisiones if c.cliente == comercial and comercial != None]
                if comision_comercial == []:
                    # Si no existe ninguna comisión con el comercial, la creo:
                    comision_comercial = Comision(cliente = comercial,
                                                  porcentaje = self.cliente.porcentaje,
                                                  precio = valor_albaran * self.cliente.porcentaje,
                                                  concepto = "Comisión por ventas. Albarán %s." % (self.numalbaran),
                                                  observaciones = "",
                                                  albaranSalida = self,
                                                  fecha = self.fecha)
            # Ahora recalculo todas las comisiones, incluida la del comercial e incluso si la acabo de crear (tardo menos
            # en actualizarla que en filtrarlas). Así, si no la acabo de crear y el usuario ha modificado el porcentaje,
            # respeto el que haya puesto:
            for comision in self.comisiones:
                comision.precio = comision.porcentaje * valor_albaran

    def _buscar_ldv(self, d, codigo, cantidad):
        """
        Busca en el diccionario d, la clave cuyo valor (que es otro
        diccionario) contiene el código c en el campo 'codigo' Y la
        cantidad de la LDV sea superior a la cantidad ya añadida (es
        otro campo del diccionario que hace de valor del primer
        diccionario) más la que se quiere añadir -cant-.
        Si no se encuentra una LDV donde la cantidad sea superior o
        igual, devolverá cualquiera de las LDV donde coincida el
        código, aunque después al añadir se sobrepase la cantidad.
        Suena lioso... pero no lo es... ¿o sí? Que va, viendo el
        código se ve muy claro.
        Devuelve la clave o None si no se encontró.
        """
        # print d
        # print codigo
        # print cantidad
        res = None
        for idldv in d:
            # XXX
            # if idldv == 0: return None
            # XXX
            if d[idldv]['codigo'] == codigo:
                res = idldv
                if d[idldv]['cantidad'] + cantidad <= d[idldv]['ldv'].cantidad:
                    res = idldv
                    break
        return res

    def agrupar_articulos(self):
        """
        Devuelve un diccionario cuyas claves son un ID de línea de venta
        los valores son listas de articulos del producto de la LDV.
        No se permite que un mismo artículo se relacione con dos LDVs
        distintas.
        Si la cantidad de los artículos (en m2, kilos, etc...) supera
        de la LDV donde se quiere añadir, se intentará añadir a otra
        LDV del mismo producto. Si no hay más LDV, se añadirá a la
        LDV que haya.
        NOTA: Este método es casi calcado al de la ventana de albaranes
        de salida. El único motivo por el cual se mantienen los dos es
        porque allí se muestra una ventana de mensaje de error en
        un caso concreto, que obligatoriamente necesita que la ventana
        padre esté cargada. En un futuro se modificará para usar
        únicamente este método y devolver un código de error para
        poder mostrar el diálogo correspondiente en lugar de hacerlo
        desde el propio procedimiento.
        NOTA 2: Modificado para que sea determinista (un mismo artículo
        siempre debe pertenecer a una misma LDV a no ser que cambien
        las condiciones iniciales). Se ha hecho simplemente ordenando
        por ID (de otro modo, modificar un simple descuento en una LDV
        podía moverla al final de la lista y devolver otros artículos
        en la llamada anterior y posterior a la modificación.
        """
        if DEBUG:
            antes = time.time()
            myprint("Soy agrupar artículos. T0 =", antes )
        # Creo un diccionario con todas las LDVs. Dentro del diccionario irá
        # un campo 'codigo' con el código del producto de la LDV, un 'articulos'
        # con una lista de artículos relacionados a la LDV, un 'cantidad' con
        # la cantidad añadida y un 'ldv' con el objeto LDV.
        d = {}
        for ldv in self.lineasDeVenta:
            d[ldv.id] = {'codigo': ldv.producto.codigo, 'articulos': [],
                         'cantidad' : 0.0, 'ldv': ldv, 'idsarticulos': []}
        # for a in self.articulos:
        # CWT: Hay que contar también con las devoluciones como parte del
        # albarán. Aunque se hayan devuelto. No importa. Al imprimir el
        # albarán DEBEN VOLVER A APARECER AHí. Porque sí, porque... porque
        # sí, y... ¡se sienten coño!
        # NOTA: OJO: CUIDADÍN: Si no se usa con cuidado es posible que surjan
        # descuadres si se considera que todos los artículos devueltos en el
        # diccionario no están en el almacén.
        articulos = self.articulos[:]
        devoluciones = [ldd.articulo for ldd in self.lineasDeDevolucion][:]
        transferencias = [ldm.articulo for ldm in self.lineasDeMovimiento][:]
        articulos.sort(lambda x, y: int(x.id - y.id))
        devoluciones.sort(lambda x, y: int(x.id - y.id))
        transferencias.sort(lambda x, y: int(x.id - y.id))
        for a in utils.unificar(articulos + devoluciones + transferencias):
            codigo = a.productoVenta.codigo
            # OJO: NO deberían haber artículos de productos que no se han
            # pedido. O al menos no deberían haber artículos sin LDV (aunque
            # la LDV no tenga pedido asignado).
            idldv = self._buscar_ldv(d, codigo, a.get_cantidad())
            if idldv == None:
                myprint(#>> sys.stderr,
                        "WARNING(1)::pclases.py::AlbaranSalida: No hay línea de venta para el artículo con id %d." % (a.id))
                myprint(#>> sys.stderr,
                        "WARNING(2)::pclases.py::AlbaranSalida: Creando línea de venta sin pedido.")
                ldv = LineaDeVenta(pedidoVenta = None,
                                   facturaVenta = None,
                                   productoVenta = a.productoVenta,
                                   albaranSalida = self,
                                   cantidad = 0)
                idldv = ldv.id
                d[idldv] = {'codigo': ldv.producto.codigo, 'articulos': [],
                            'cantidad' : 0.0, 'ldv': ldv, 'idsarticulos': []}
                myprint(#>> sys.stderr,
                        "WARNING(3)::pclases.py::AlbaranSalida: Línea de venta con id %d creada." % (idldv))
            # idldv NO debería ser None. Si lo es, algo grave pasa; prefiero que salte la excepción.
            d[idldv]['articulos'].append(a)
            d[idldv]['idsarticulos'].append(a.id)
            d[idldv]['cantidad'] += a.get_cantidad()
        if DEBUG:
            myprint("Soy agrupar artículos. T1 - T0=", time.time() - antes )
        return d

    def contar_lineas_facturadas(self):
        """
        Devuelve el número de líneas de venta del albarán
        que ya han sido facturadas.
        """
        lineas_facturadas = [ldv for ldv in self.lineasDeVenta if ldv.facturaVentaID != None or ldv.prefacturaID != None]
            # Acceder a ...ID es más rápido que acceder al objeto en sí, aunque sea solo para comparar si no es None.
        return len(lineas_facturadas)

    def get_facturas(self):
        """
        Devuelve una lista de objetos factura relacionados con el albarán.
        """
        facturas = []
        for ldv in self.lineasDeVenta:
            if ldv.facturaVentaID != None and ldv.facturaVenta not in facturas:
                facturas.append(ldv.facturaVenta)
            elif ldv.prefacturaID != None and ldv.prefactura not in facturas:
                facturas.append(ldv.prefactura)
        for srv in self.servicios:
            if srv.facturaVentaID != None and srv.facturaVenta not in facturas:
                facturas.append(srv.facturaVenta)
            elif srv.prefacturaID != None and srv.prefactura not in facturas:
                facturas.append(srv.prefactura)
        return facturas

    @classmethod
    def ultimo_numalbaran(cls):
        """
        Devuelve un ENTERO con el último número de albarán sin letras o 0 si
        no hay ninguno o los que hay tienen caracteres alfanuméricos y no se
        pueden pasar a entero.
        Para determinar el último número de albarán no se recorre toda la
        tabla de albaranes intentando convertir a entero. Lo que se hace es
        ordenar a la inversa por ID y comenzar a buscar el primer número de
        albarán convertible a entero. Como hay una restricción para crear
        albaranes, es de suponer que siempre se va a encontrar el número más
        alto al principio de la lista orderBy="-id".
        OJO: Aquí los números son secuenciales y no se reinicia en cada año
        (que es como se está haciendo ahora en facturas).
        """
        # DONE: Además, esto debería ser un método de cls.
        regexp = re.compile("[0-9]*")
        ultimo = 0
        # albs = AlbaranSalida.select(orderBy = '-numalbaran')       # No, porque A_AJUSTE se colocaría el primero a tratar.
        albs = cls.select(orderBy = '-id')
        for a in albs:
            try:
                numalbaran = a.numalbaran
                ultimo = [int(item) for item in regexp.findall(numalbaran) if item != ''][0]
                # ultimo = int(numalbaran)
                break
            except (IndexError, ValueError), msg:
                myprint("pclases.py (ultimo_numalbaran): Número de último albarán no se pudo determinar: %s" % (msg))
                # No se encontaron números en la cadena de numalbaran o ¿se encontró un número pero no se pudo parsear (!)?
                ultimo = 0
        return ultimo

    @classmethod
    def siguiente_numalbaran(cls):
        """
        Devuelve un ENTERO con el siguiente número de albarán sin letras o 0
        si no hay ninguno o los que hay tienen caracteres alfanuméricos y no
        se pueden pasar a entero.
        OJO: Aquí los números son secuenciales y no se reinicia en cada año
        (que es como se está haciendo ahora en facturas).
        """
        return AlbaranSalida.get_ultimo_numero_numalbaran() + 1

    def get_num_numalbaran(self):
        """
        Devuelve el número de albarán como entero.
        Hasta ahora se han usado números solo o año y número, por lo que
        el número en sí será el último entero encontrado.
        """
        rexp = re.compile("\d+")
        nums = rexp.findall(self.numalbaran)
        return int(nums[-1])

    @classmethod
    def siguiente_numalbaran_str(cls):
        """
        Devuelve el siguiente número de albarán libre como cadena intentando
        respetar el formato del último numalbaran.
        """
        regexp = re.compile("[0-9]*")
        ultimo = None
        albs = cls.select(orderBy = '-id')
        for a in albs:
            try:
                numalbaran = a.numalbaran
                ultimo = [int(item) for item in regexp.findall(numalbaran) if item != ''][-1]
                break
            except (IndexError, ValueError), msg:
                myprint("pclases.py (siguiente_numalbaran_str): Número de último albarán no se pudo determinar: %s" % (msg))
                # No se encontaron números en la cadena de numalbaran o ¿se encontró un número pero no se pudo parsear (!)?
                ultimo = ""
        if ultimo != "" and ultimo != None:
            head = numalbaran[:numalbaran.rindex(str(ultimo))]
            tail = numalbaran[numalbaran.rindex(str(ultimo)) + len(str(ultimo)):]
            str_ultimo = str(ultimo + 1)
            res = head + str_ultimo + tail
            while AlbaranSalida.select(AlbaranSalida.q.numalbaran == res).count() != 0:
                ultimo += 1
                str_ultimo = str(ultimo + 1)
                res = head + str_ultimo + tail
        else:
            res = 0
        if not isinstance(res, str):
            res = str(res)
        return res

    get_ultimo_numero_numalbaran = ultimo_numalbaran
    get_siguiente_numero_numalbaran = siguiente_numalbaran
    get_siguiente_numero_numalbaran_str = siguiente_numalbaran_str

    def get_str_tipo(self):
        """
        Devuelve una cadena en castellano con el tipo de albarán de salida:
            - Movimiento (si es de movimiento de mercancía entre almacenes).
            - Repuestos (si es albarán de repuestos).
            - Interno (si cliente es propia empresa).
            [- Ajuste (PLAN: No sé si incluir los albaranes de ajuste como un
                       tipo de albarán por derecho propio).]
            - Salida (normal, no movimiento ni interno).
            - Vacío (si no tiene ninguna línea de venta ni nada asociado).
        Las condiciones se chequean en este orden. Esto es importante porque
        un albarán de movimiento generalmente también será interno.
        """
        if self.esta_vacio():
            return AlbaranSalida.str_tipos[AlbaranSalida.VACIO]
        if self.es_interno():
            return AlbaranSalida.str_tipos[AlbaranSalida.INTERNO]
        if self.es_de_repuestos():
            return AlbaranSalida.str_tipos[AlbaranSalida.REPUESTOS]
        if self.es_de_movimiento():
            return AlbaranSalida.str_tipos[AlbaranSalida.MOVIMIENTO]
        return AlbaranSalida.str_tipos[AlbaranSalida.NORMAL]

    def esta_vacio(self):
        """
        Devuelve True si el albarán no tiene registrado nada. Ni líneas de
        venta, ni artículos ni servicios. No miro las devoluciones. De todas
        formas, si tiene devoluciones también tiene LDVs, que sí que se mira.
        """
        return (not self.lineasDeVenta
                and not self.articulos
                and not self.servicios)

    def get_info(self):
        """
        Muestra número de albarán, fecha, cliente y tipo: interno,
        movimiento o salida.
        """
        return "Albarán %s. Fecha: %s. Cliente: %s. Tipo: %s" % (
            self.numalbaran,
            utils.str_fecha(self.fecha),
            self.clienteID and self.cliente.nombre or "",
            self.get_str_tipo())

cont, tiempo = print_verbose(cont, total, tiempo)

class LineaDeProduccion(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    productosVenta = MultipleJoin('ProductoVenta')
    #--------------------------------- formulacionID = ForeignKey('Formulacion')
    calendariosLaborales = MultipleJoin('CalendarioLaboral')
    categoriasLaborales = MultipleJoin('CategoriaLaboral')
    controlesHorasProduccion = MultipleJoin('ControlHorasProduccion')
    controlesHorasMantenimiento = MultipleJoin('ControlHorasMantenimiento')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class Formulacion(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    lineasDeProduccion = MultipleJoin('LineaDeProduccion')
    consumosAdicionales = MultipleJoin('ConsumoAdicional')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class ConsumoAdicional(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------------------- formulacionID = ForeignKey('Formulacion')
    #--------------------------- productoCompraID = ForeignKey('ProductoCompra')
    productosVenta = RelatedJoin('ProductoVenta',
                        joinColumn='consumo_adicional_id',
                        otherColumn='producto_venta_id',
                        intermediateTable='consumo_adicional__producto_venta')

    PORCENTAJE = 1
    FRACCION = 2

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def __parsear_porcentaje(self):
        """
        Devuelve la cantidad del porcentaje como fracción de 1.
        """
        txt = "%s %s" % (self.cantidad, self.unidad)
        regexp_float = re.compile("^-?\d+[\.,]?\d*")
        num = regexp_float.findall(txt)[0]
        num = utils._float(num) / 100
        return num

    def __parsear_fraccion(self):
        """
        Devuelve la cantidad de producto compra y unidad que hay que descontar
        por cada cantidad de producto venta y unidad (que también se devuelven).
        Es necesario que venga la cantidadpc aunque en el registro, en el campo
        "unidad" no aparece.
        """
        txt = "%s %s" % (self.cantidad, self.unidad)
        regexp_float = re.compile("-?\d+[\.,]?\d*")
        regexp_unidad = re.compile("\w+")
        cantidades = regexp_float.findall(txt)
        if len(cantidades) == 1:
            cantidadpc = cantidades[0]
            cantidadpv = '1'
            txt = txt.replace(cantidadpc, "")
        elif len(cantidades) == 2:
            cantidadpc, cantidadpv = cantidades[0:2]
            txt = txt.replace(cantidadpc, "")
            txt = txt.replace(cantidadpv, "")
        else:
            cantidadpc = '1'
            cantidadpv = '1'
        txt = txt.replace("/", "")
        unidadpc, unidadpv = regexp_unidad.findall(txt)[0:2]
        cantidadpc = utils._float(cantidadpc)
        cantidadpv = utils._float(cantidadpv)
        return cantidadpc, unidadpc, cantidadpv, unidadpv

    def _comprobar_unidad(self, cantidadpc = 1.0):
        """
        Comprueba si la unidad de descuento "txt" cumple con
        alguna de las unidades interpretables por el programa.
        cantidadpc se usa para agregarlo a la parte "unidad" y
        chequear todo el conjunto en el proceso.
        Devuelve False si la unidad es incorrecta,
        ConsumoAdicional.PORCENTAJE si es un
        porcentaje y ConsumoAdicional.FRACCION si es una fracción.
        """
        res = False
        txt = "%s %s" % (utils.float2str(cantidadpc, 5), self.unidad)
        txt = txt.strip()
        # TODO: De momento lo hago así porque no sé de qué modo
        #       ni dónde guardarlo:
        regexp_porcentaje = re.compile("^-?\d+[\.,]?\d*\s*%$")
        regexp_fraccion = re.compile("-?\d+[\.,]?\d*\s*\w*\s*/\s*-?\d*[\.,]?\d*\s*\w+")
        if regexp_porcentaje.findall(txt) != []:
            cantidad = self.__parsear_porcentaje()  # @UnusedVariable
            res = ConsumoAdicional.PORCENTAJE
        elif regexp_fraccion.findall(txt) != []:
            cantidad, unidad, cantidad_pv, unidad_pv = self.__parsear_fraccion()  # @UnusedVariable
            res = ConsumoAdicional.FRACCION
        return res

    def _calcular_metros_forzados(self, ancho, ancho_max):
        """
        Calcula el ancho inmediatamente superior a «ancho» y que sea
        divisor "exacto"[1] de «ancho_max». Todas las cantidades son metros
        en float.
        Devuelve también un float en metros.
        Los cálculos internos se hacen en centímetros para facilitar
        el trabajo, en enteros.
        ----
        [1] No es exacto del todo. El ancho 1.83 no es un tercio exacto de
        5.50 m.
        """
        ancho_max *= 100
        ancho_max = int(ancho_max)
        ancho *= 100
        ancho = int(ancho)
        num_piezas = ancho_max / ancho  # Máximo número de piezas de
                            # ancho "ancho" que entran en "ancho_max"
        ancho_f = ancho_max / num_piezas    # El truncamiento de enteros hace
                        # todo el trabajo sucio. Devuelvo el ancho justo de
                        # una pieza tal que ese ancho por el número de piezas
                        # dan el ancho máximo "casi" exacto.
        ancho_f /= 100.0
        return ancho_f

    def consumir(self,
                 articulo,
                 cancelar = False,
                 silo = None,
                 productoCompra = None):
        """
        Crea un registro consumo en el cual consta la cantidad de
        productoCompra correspondiente, el parte de producción del
        artículo que hace el consumo y la cantidad que indique el
        objeto de consumo adicional (self).
        La cantidad se determina en función de las unidades indicadas
        y si el artículo es bala (se usará pesobala o ud) o rollo
        (se puede usar peso del rollo, densidad * ancho * metros lineales,
        ancho * metros lineales o unidad).
        Si cancelar = True, la cantidad irá en negativo para cancelar
        un consumo igual anterior.
        Si silo != None, se asigna el consumo al silo correspondiente,
        PERO NO SE REALIZA EL CONSUMO DEL SILO NI SE ACTUALIZAN LAS
        EXISTENCIAS DEL PRODUCTO DE COMPRA, ya que el método consumir del
        objeto silo se encarga de descontar el material del almacén.
        Si silo == None, entonces sí se actualiza el producto de compra.
        Si productoCompra != None, se usa ese producto en lugar del
        predeterminado en el registro.
        TODO: (Habrá un unificar consumos para
        que no haya exceso de registros consumo anulándose entre sí o
        que se puedan sumar si son del mismo parte y productoCompra).
        TODO: El consumo de granza se considera un consumo normal, es
        en el parte de producción donde hay que llamar a esta función
        con los distintos porcentajes de la cantidad para cada silo, y
        descargar el silo desde esa ventana (no se hace aquí).
        OJO: La cantidad a consumir se cuenta en base al peso total, lo cual
        es correcto, porque del peso de un rollo -por ejemplo- de 100 kg, 5
        serán de embalaje -según la ficha del producto- y los descontará aquí
        según la fórmula (que debe expresar que el 5% del peso es de
        embalaje), etc...
        NOTA: Siempre, siempre, siempre, se consume del almacén principal.
        """
        if productoCompra != None:
            producto_a_consumir = productoCompra
        else:
            producto_a_consumir = self.productoCompra
        if producto_a_consumir == None:
            myprint("pclases.py: class ConsumoAdicional::consumir(): ¡El producto a consumir es None! Ignoro consumo y devuelvo 0 como cantidad consumida.")
            return 0
        producto_a_consumir.sync()
        if (producto_a_consumir.es_nucleo_carton()
            or "cleo" in self.nombre.lower() or "tubo" in self.nombre.lower()):
            # Se van a consumir núcleos de cartón, por lo que se han de
            # descontar 1.83, 2.75 o 5.5 m. Los "restos" directamente
            # se desechan y no deben permanecer en existencias. Fuerzo
            # el ancho del artículo a una medida divisora de 5.50
            # inmediatamente superior al ancho real.
            # OJO: En el consumo debe aparecer la palabra "*cleo" o "*cleo*
            # *cart*" en la descripción del producto (pocas cosas
            # hay aparte de núcleos de cartón deberían cumplir este requisito).
            try:
                ancho_tubos, unidad = self.__parsear_fraccion()[-2:]
                if "m" not in unidad.lower():
                    raise ValueError
            except:
                ancho_tubos = 5.5
            if articulo.es_rolloC():
                # No tienen ancho "per se". Generalizo a 5.5
                metros_forzados = self._calcular_metros_forzados(5.5,
                                        ancho_tubos)
            else:
                metros_forzados = self._calcular_metros_forzados(
                                        articulo.ancho,
                                        ancho_tubos)
            cantidad_a_consumir = self._calcular_cantidad_a_consumir(
                                        articulo,
                                        metros_articulo = metros_forzados)
        else:
            cantidad_a_consumir = self._calcular_cantidad_a_consumir(articulo)
        if cancelar:
            cantidad_a_consumir *= -1
        consumo = Consumo(silo = silo,  # @UnusedVariable
                          parteDeProduccion = articulo.parteDeProduccion,
                          productoCompra = producto_a_consumir,
                          actualizado = True,
                          antes = self.productoCompra.existencias,
                          despues = self.productoCompra.existencias - cantidad_a_consumir,
                          cantidad = cantidad_a_consumir)
        if silo == None:
            self.productoCompra.sync()
            self.productoCompra.existencias -= cantidad_a_consumir
            self.productoCompra.add_existencias(-cantidad_a_consumir)
        producto_a_consumir.syncUpdate()
        producto_a_consumir.sync()
        return cantidad_a_consumir

    def _calcular_cantidad_a_consumir(self,
                                      articulo,
                                      kilos_articulo = None,
                                      metros2_articulo = None,
                                      metros_articulo = None):
        """
        Calcula la cantidad de producto compra a consumir
        para un bulto del artículo recibido.
        Hace las conversiones necesarias para transformar la
        unidad del consumo en la unidad de producto compra por
        bulto del producto venta (artículo).
        Si no se puede calcular, devuelve None.
        En otro caso, devuelve un Float en las unidades del
        producto de compra.
        Las dimensiones (kilos, metros y metros cuadrados) del
        artículo se pueden forzar pasándolas en la llamada.
        """
        cantidad = 0
        if kilos_articulo == None:
            kilos_articulo = articulo.peso
        if metros2_articulo == None:
            metros2_articulo = articulo.superficie
        if metros_articulo == None:
            metros_articulo = articulo.ancho
        unidad = self._comprobar_unidad(self.cantidad)
        if unidad == ConsumoAdicional.PORCENTAJE:
            # La cantidad es un porcentaje del peso del producto de venta.
            # Las unidades del producto de compra *se supone* que son kg.
            if self.productoCompra.unidad.strip().lower().replace(".", "") != "kg":
                myprint('WARNING pclases.py (_calcular_cantidad_a_consumir): La unidad del producto de compra %s [%d] (%s) no coincide con "kg", que es la unidad de consumo en la formulación.' % (self.productoCompra.descripcion, self.productoCompra.id, self.productoCompra.unidad))
            porcentaje = self.__parsear_porcentaje()
            cantidad = porcentaje * kilos_articulo
        elif unidad == ConsumoAdicional.FRACCION:
            # La cantidad es una fracción de la unidad de producto venta
            # indicada, en las unidades del producto de compra; que debería
            # coincidir con la unidad expresada delante de "/".
            cantidad_pc, unidad_pc, cantidad_pv, unidad_pv = self.__parsear_fraccion()
            if self.productoCompra.unidad.strip().lower().replace(".", "") != unidad_pc.strip().lower().replace(".", ""):
                myprint('WARNING pclases.py (_calcular_cantidad_a_consumir): La unidad del producto de compra %s [%d] (%s) no coincide con "%s", que es la unidad de consumo en la formulación.' % (self.productoCompra.descripcion, self.productoCompra.id, self.productoCompra.unidad, unidad_pc))
            if unidad_pv.strip().lower() == "ud":
                cantidad = cantidad_pc
            elif unidad_pv.strip().lower() == "m":
                cantidad = (metros_articulo * cantidad_pc) / cantidad_pv
            elif unidad_pv.replace(" ", "").lower() == "m2" or unidad_pv.replace(" ", "").lower() == "m²":
                cantidad = (metros2_articulo * cantidad_pc) / cantidad_pv
            elif unidad_pv.strip().lower() == "kg":
                cantidad = (kilos_articulo * cantidad_pc) / cantidad_pv
            else:
                myprint("ERROR pclases.py (_calcular_cantidad_a_consumir): No se pudo interpretar la unidad de consumo de la formulación. ConsumoAdicional.id = %d" % (self.id))
                cantidad = 0
        return cantidad

cont, tiempo = print_verbose(cont, total, tiempo)

class TipoDeCliente(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    clientes = MultipleJoin("Cliente")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        return "%s: %d clientes en esta categoría." % (
                self.descripcion, len(self.clientes))

    @staticmethod
    def check_defaults():
        """
        Comprueba que existen --y si no, los crea-- los tipos por defecto.
        """
        # FIXME: La creación dentro del AssertionError no funciona. Al hacerlo
        # con una base de datos limpia, peta. Dice que el ID del objeto
        # recién insertado no existe. Supongo que es en la línea de Auditoria.
        # Tal vez necesite un commit explícito antes o algo.
        # INSERT INTO tipo_de_cliente("descripcion") VALUES ('Industrial'), ('General'), ('Fibra'), ('Geocem'), ('Comercializado');
        tipos = ("Industrial", "General", "Fibra", "Geocem", "Comercializado")
        for t in tipos:
            try:
                assert TipoDeCliente.selectBy(descripcion = t).count() > 0
            except AssertionError:
                tipo = TipoDeCliente(descripcion = t)
                Auditoria.nuevo(tipo, None, __file__)

    @classmethod
    def get_por_defecto(clasecliente):
        """
        Devuelve el tipo de cliente por defecto a usar.
        """
        try:
            tdc = clasecliente.selectBy(descripcion = "General")[0]
        except IndexError:
            tdc = clasecliente(descripcion = "General")
            Auditoria.nuevo(tdc, None, __file__)
        return tdc

cont, tiempo = print_verbose(cont, total, tiempo)

class Contador(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    clientes = MultipleJoin('Cliente')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_last_factura_creada(self):
        """
        Devuelve la última factura creada según el orden del campo numfactura.
        None si no hay facturas de la serie (ninguna factura coincide en
        prefijo ni sufijo).
        """
        self.sync()
        fras = self.__get_facturas()
        if fras.count() > 0:
            return fras[0]
        return None

    def get_last_numfactura_creada(self):
        """
        Devuelve la última factura creada de la serie según el orden del
        campo numfactura, no el de ID ni el de la tabla de la BD.
        Si no hay facturas en la serie, devuelve la cadena vacía.
        """
        ultima_fra = self.get_last_factura_creada()
        if ultima_fra:
            return ultima_fra.numfactura
        return ""

    def __get_facturas(self):
        self.sync()
        fras = FacturaVenta.select(AND(
            FacturaVenta.q.numfactura.startswith(self.prefijo),
            FacturaVenta.q.numfactura.endswith(self.sufijo)),
            orderBy = "-numfactura")
        return fras

    def get_facturas(self):
        """
        Devuelve las facturas de la serie, ordenadas por numfactura.
        """
        fras = [f for f in self.__get_facturas()]
        fras.reverse()
        return fras

    def get_and_commit_numfactura(self):
        """
        Devuelve y hace efectivo (esto es, aumenta el contador)
        el siguiente número de factura de la serie facturable
        del contador.
        """
        return self.get_next_numfactura(commit = True)

    def get_next_numfactura(self, commit = False, inc = 1):
        """
        Por defecto devuelve el que sería el siguiente número
        de factura. Si commit = True entonces sí lo hace
        efectivo y corre el contador de la serie.
        "inc" es el número en que avanza el contador. Por defecto 1
        """
        self.sync()
        # CWT: El número entre prefijo y sufijo pasa a tener 4 dígitos como
        # mínimo
        numfactura = "%s%04d%s" % (self.prefijo,
                                   self.contador - 1 + inc,
                                   self.sufijo)
        if commit:
            self.contador += inc
            self.syncUpdate()
        return numfactura

    def get_info(self):
        """
        Devuelve el prefijo, número actual y sufijo del contador.
        """
        # return "%s%d%s" % (self.prefijo, self.contador, self.sufijo)
        return self.get_next_numfactura(commit = False)

cont, tiempo = print_verbose(cont, total, tiempo)

class Obra(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    facturasVenta = MultipleJoin('FacturaVenta')
    contactos = RelatedJoin("Contacto",
                            joinColumn = "obra_id",
                            otherColumn = "contacto_id",
                            intermediateTable = "obra__contacto")
    clientes = RelatedJoin('Cliente',
                           joinColumn = 'obra_id',
                           otherColumn = 'cliente_id',
                           intermediateTable = 'obra__cliente')
    abonos = MultipleJoin('Abono')
    pedidosVenta = MultipleJoin('PedidoVenta')
    presupuestos = MultipleJoin('Presupuesto')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_str_direccion(self):
        """
        Devuelve una cadena con la dirección completa.
        """
        res = ""
        if self.direccion:
            res += " %s" % self.direccion
        if self.cp:
            res += "; %s" % self.cp
        if self.ciudad and self.provincia:
            res += " - %s (%s)" % (self.ciudad, self.provincia)
        elif self.ciudad:
            res += " - %s" % self.ciudad
        elif self.provincia:
            res += " - %s" % self.provincia
        elif self.pais:
            res += ". %s" % self.pais
        return res

    def get_str_obra(self):
        """
        Devuelve una cadena con el nombre de la obra y la dirección completa.
        """
        res = "%s." % self.nombre
        str_direccion = self.get_str_direccion()
        if str_direccion:
            res += " " + str_direccion
        return res

    @property
    def finalizada(self):
        """
        Devuelve True si la obra tiene fecha de finalización y ya se ha
        alcanzado.
        """
        ended = False
        if self.fechafin:
            try:
                if mx.DateTime.today() > self.fechafin:
                    ended = True
            except TypeError:
                if datetime.date.today() > self.fechafin:
                    ended = True
        return ended

cont, tiempo = print_verbose(cont, total, tiempo)

class Contacto(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    obras = RelatedJoin("Obra",
                        joinColumn = "contacto_id",
                        otherColumn = "obra_id",
                        intermediateTable = "obra__contacto")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_str_contacto(self):
        """
        Devuelve la información del contacto como texto.
        """
        res = "%s, %s" % (self.apellidos, self.nombre)
        if self.cargo:
            res += " (%s)" % self.cargo
        if self.telefono:
            res += ". Tlf.: %s" % self.telefono
        if self.fax:
            res += ". Fax: %s" % self.fax
        if self.movil:
            res += ". Móvil: %s" % self.movil
        if self.correoe:
            res += ". Correo-e: %s" % self.correoe
        if self.web:
            res += ". Web: %s" % self.web
        if self.observaciones:
            res += ". Obs.: %s" % self.observaciones
        res += "."
        return res

    def existe_en(self, obra):
        """
        Devuelve True si el contacto (self) existe en la obra recibida. Se
        compara la representación como cadena de los contactos para abarcar
        el mayor número de campos posible. No se comparan los contactos en sí
        porque pueden ser el mismo y tener ID diferentes en la BD.
        """
        yo = self.get_str_contacto()
        for c in obra.contactos:
            if c.get_str_contacto() == yo:
                return True
        return False

cont, tiempo = print_verbose(cont, total, tiempo)

class Nota(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #------------------------------- facturaVentaID = ForeignKey('FacturaVenta')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_str_nota(self):
        txtnota = utils.str_fechahora(self.fechahora) + ": "
        if self.texto and self.observaciones:
            if self.texto.strip().endswith("."):
                txtnota += "%s %s" % (self.texto, self.observaciones)
            else:
                txtnota += "%s. %s" % (self.texto, self.observaciones)
        elif self.texto:
            txtnota += self.texto
        else:
            txtnota += self.observaciones
        return txtnota

cont, tiempo = print_verbose(cont, total, tiempo)

class Alarma(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #------------------------------- facturaVentaID = ForeignKey('FacturaVenta')
    #------------------------------------------- estadoID = ForeignKey("Estado")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def crear_alarmas_automaticas(fras_de_venta):
        """
        Recorre la lista de facturas recibidas y crea las alarmas automáticas
        correspondientes, si no estaban creadas ya.
        """
        try:
            estado = Estado.get(1)  # *Debería* existir.
        except:
            estado = Estado(id = 1, descripcion = "No leída", pendiente = True)
        for fra in fras_de_venta:
            # Primera de las alarmas automáticas: Crear una alarma para las
            # facturas vencidas sin documento de pago.
            if (fra.calcular_pendiente_de_documento_de_pago()
                and not fra.alarmas
                and fra.esta_vencida()):
                # Si tiene importes pendientes de cubrir por un documento de
                # pago, no tiene ya alarmas relacionadas y tiene algún
                # vencimiento vencido, creo una alarma:
                if DEBUG:
                    myprint("Creando alarma automática...")
                fechahora_last_vencimiento = fra.vencimientosCobro[-1].fecha
                nueva_alarma = Alarma(facturaVenta = fra,
                            estado = estado,
                            fechahora = mx.DateTime.localtime(),
                            texto = "Factura vencida sin documento de pago.",
                            fechahoraAlarma = fechahora_last_vencimiento,
                            objetoRelacionado = None,
                            observaciones = "Alarma creada automáticamente.")
                if DEBUG:
                    myprint('Alarma "%s" con fecha de alarma %s creada.' % (
                        nueva_alarma.get_info(),
                        utils.str_fechahora(nueva_alarma.fechahoraAlarma)))
            # Segunda de las alarmas automáticas: Enviar un correo electrónico
            # al comercial relacionado si la factura se emitió hace más de 45
            # días y aún no se ha recibido un documento de pago. En el correo
            # se debe adjuntar el PDF del historial de la factura y un PDF de
            # la copia de la factura -la que lleva marca de agua-.
            if (mx.DateTime.DateFrom(fra.fecha) + (mx.DateTime.oneDay * 45)
                    <= mx.DateTime.localtime()
                and not fra.cobros):
                # Verifico que no se haya enviado ya el correo electrónico.
                for t in fra.tareas:
                    if (t.es_automatica()
                        and "Enviar correo a comercial" in t.texto
                        and t.pendiente == False):
                        fra.enviar_por_correoe_a_comercial_relacionado(
                            asunto = "Reclamación factura %s" % fra.numfactura)
            # TODO: Quedan más alarmas automáticas por crear, pero esta de
            #       arriba era la más urgente. Ya meteré las demás más tarde.

    crear_alarmas_automaticas = staticmethod(crear_alarmas_automaticas)

cont, tiempo = print_verbose(cont, total, tiempo)

class Tarea(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #------------------------------- facturaVentaID = ForeignKey('FacturaVenta')
    #------------------------------------- categoriaID = ForeignKey("Categoria")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def es_automatica(self):
        """
        Devuelve True si la tarea es una tarea de categoría automática.
        Si la categoría de tareas automáticas no existe, la crea.
        """
        auto = Categoria.get_categoria_tareas_automaticas()
        return self.categoriaID == auto.id

cont, tiempo = print_verbose(cont, total, tiempo)

class Categoria(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    tareas = MultipleJoin('Tarea')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_gdk_color_params(self):
        """
        Devuelve los parámetros de un gtk.gdk.Color correspondiente al color
        RGB de la categoría.
        Las componentes RGB de la categoria van de 0 a 255. Se escalarán al
        rango del gdk.Color que llega hasta 65535.
        """
        factor_escala = 65535.0 / 255
        r = int(self.colorR * factor_escala)
        g = int(self.colorG * factor_escala)
        b = int(self.colorB * factor_escala)
        pixel = 0   # No sé para qué usa gtk este valor.
        return (r, g, b, pixel)

    def get_categoria_tareas_automaticas():
        """
        Devuelve la categoría de tareas automáticas o la crea si
        no existe.
        """
        try:
            auto = Categoria.select(
                        Categoria.q.descripcion == "Tareas automáticas",
                        orderBy = "id")[0]
        except IndexError:
            auto = Categoria(descripcion = "Tareas automáticas",
                         colorR = 125, colorG = 125, colorB = 125,
                         prioridad = 10,
                         observaciones = "Creado automáticamente. Reservado "\
                                         "para tareas de alarmas automáticas.")
        return auto

    get_categoria_tareas_automaticas = staticmethod(
                                            get_categoria_tareas_automaticas)

cont, tiempo = print_verbose(cont, total, tiempo)

class Estado(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    alarmas = MultipleJoin('Estado')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class Servicio(SQLObject, PRPCTOO, Venta):
    class sqlmeta:
        fromDatabase = True
    #------------------------------- facturaVentaID = ForeignKey('FacturaVenta')
    #------------------- prefacturaID = ForeignKey('Prefactura', default = None)
    #------------- albaranSalidaID = ForeignKey('AlbaranSalida', default = None)
    lineasDeAbono = MultipleJoin('LineaDeAbono')
    #----------------- pedidoVentaID = ForeignKey('PedidoVenta', default = None)
    #----------------- presupuestoID = ForeignKey('Presupuesto', default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_almacen(self):
        """
        Devuelve el almacén relacionado con la línea de devolución, que será
        aquel al que se haya devuelto la mercancía.
        """
        return self.albaranSalida and self.albaranSalida.almacenOrigen or None

    def get_cliente(self):
        """
        Devuelve el objeto cliente de la LDV según su pedido, albarán o
        factura. Por ese orden.
        """
        try:
            return self.pedidoVenta.cliente
        except AttributeError:
            try:
                return self.albaranSalida.cliente
            except AttributeError:
                try:
                    return self.facturaVenta.cliente
                except AttributeError:
                    try:
                        return self.prefactura.cliente
                    except AttributeError:
                        return None

    def get_factura_o_prefactura(self):
        """
        Devuelve la factura relacionada, tanto si es facturaVenta
        como prefactura, o None si no tiene ninguna de ellas.
        Como no debería tener ambos valores distintos de nulo a
        la vez, tiene preferencia facturaVenta sobre prefactura.
        """
        return self.facturaVenta or self.prefactura

    @property
    def factura(self):
        return self.get_factura_o_prefactura()

    def get_subtotal(self, iva = False, descuento = True, prorrateado = False):
        """
        Devuelve el subtotal del servicio. Con IVA (el IVA de la factura) si
        se le indica.
        """
        # PLAN: Con un buen diagrama de clases podría haber tenido una clase
        #       padre común para servicios, líneas de venta y demás con sus
        #       métodos abstractos get_subtotal y demás. Claro que sin un
        #       documento de requisitos en condiciones es imposible tener unos
        #       casos de uso en condiciones para poder hacer un diagrama de
        #       clases en condiciones. A dios pongo por testigo de que jamás
        #       volveré a confiar en un cliente que diga "yo creo que ya no
        #       necesitamos más reuniones de validación de requisitos.
        #       Eso es todo lo que queremos".
        res = self.cantidad * self.precio
        if descuento:
            res *= (1 - self.descuento)
        if iva and self.facturaVentaID:
            res *= (1 + self.facturaVenta.iva)
        elif iva and self.prefacturaID:
            res *= (1 + self.prefactura.iva)
        if prorrateado:
            try:
                numvtos = len(self.factura.cliente.get_vencimientos())
            except AttributeError:
                numvtos = len(self.albaranSalida.cliente.get_vencimientos())
            if not numvtos:
                numvtos = 1
            res /= numvtos
        return res

    calcular_subtotal = get_subtotal

    def calcular_beneficio(self):
        """
        Devuelve como beneficio el importe total del servicio.
        """
        return self.get_subtotal(iva = False)

    def get_info(self):
        """
        Devuelve cadena con cantidad, descripción y subtotal del servicio (IVA
        no incluido).
        """
        precio_con_descuento = utils.float2str(
            self.precio * (1.0 - self.descuento))
        if self.descuento:
            precio_con_descuento += " (%s%% dto. incl.)" % (
                utils.float2str(self.descuento * 100))
        total_srv = self.get_subtotal()
        res = "%s %s * %s = %s" % (
            utils.float2str(self.cantidad),
            self.concepto,
            precio_con_descuento,
            utils.float2str(total_srv))
        return res


cont, tiempo = print_verbose(cont, total, tiempo)

class Lote(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    balas = MultipleJoin('Bala')
    pruebasTenacidad = MultipleJoin('PruebaTenacidad')
    pruebasElongacion = MultipleJoin('PruebaElongacion')
    pruebasRizo = MultipleJoin('PruebaRizo')
    pruebasEncogimiento = MultipleJoin('PruebaEncogimiento')
    pruebasGrasa = MultipleJoin('PruebaGrasa')
    pruebasTitulo = MultipleJoin('PruebaTitulo')
    muestras = MultipleJoin('Muestra')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    @property
    def productoVenta(self):
        return self.get_productoVenta()

    def calcular_media_pruebas(self, pruebas):
        """
        Devuelve la media del campo resultados de
        la lista de pruebas recibidas.
        """
        denominador = len(pruebas)
        numerador = sum([prueba.resultado for prueba in pruebas])
        try:
            return numerador / denominador
        except ZeroDivisionError:
            return 0

    calcular_tenacidad_media = lambda self: self.calcular_media_pruebas(self.pruebasTenacidad)
    calcular_elongacion_media = lambda self: self.calcular_media_pruebas(self.pruebasElongacion)
    calcular_rizo_medio = lambda self: self.calcular_media_pruebas(self.pruebasRizo)
    calcular_encogimiento_medio = lambda self: self.calcular_media_pruebas(self.pruebasEncogimiento)
    calcular_grasa_media = lambda self: self.calcular_media_pruebas(self.pruebasGrasa)
    calcular_titulo_medio = lambda self: self.calcular_media_pruebas(self.pruebasTitulo)

    def get_productoVenta(self):
        """
        Devuelve el producto de venta al que pertenece
        el lote o None si no tiene producción.
        """
        if self.balas:
            producto = self.balas[0].articulo.productoVenta
        else:
            producto = None
        return producto

    def set_productoVenta(self, productoVenta):
        """
        Hace que el producto de venta de todas las balas
        del lote sea el recibido.
        """
        if not isinstance(productoVenta, ProductoVenta):
            raise TypeError, "El producto debe ser un objeto de la clase ProductoVenta."
        for b in self.balas:
            b.articulo.productoVenta = productoVenta

    productoVenta = property(get_productoVenta, set_productoVenta, "Producto de venta relacionado con el lote.")

    def enAlmacen(self, almacen = None):
        """
        Devuelve cierto si queda alguna bala de ese lote
        en almacen.
        Si «almacen» != None busca solo las que se encuentren en ese almacén.
        """
        #        for bala in self.balas:
        #            if bala.partidaID == None or bala.articulos[0].albaranSalidaID == None:
        #                return True
        #        return False
        # Primero extrae las balas no consumidas para fabricar y después filtra las que se han vendido en albarán.
        #balas_en_almacen = Articulo.select("""
        #    articulo.bala_id IN (SELECT bala.id
        #                         FROM bala
        #                         WHERE bala.lote_id = %d
        #                           AND bala.partida_carga_id IS NULL)
        #                     AND articulo.albaran_salida_id IS NULL
        #    """ % (self.id))
        clauses = [Articulo.q.balaID == Bala.q.id,
                   Bala.q.loteID == self.id]
        if almacen:
            clauses.append(Articulo.q.almacenID == almacen.id)
        else:
            clauses.append(Articulo.q.almacenID != None)
        balas_en_almacen = Articulo.select(AND(*clauses))
        return balas_en_almacen.count()# > 0    Así además puedo aprovechar
                        # para ver las que quedan. Total, un 0 ya es False.

    def get_consumos(self):
        """
        Devuelve una lista de consumos relacionados con el lote completo
        para saber la materia prima empleada en cada caso.
        """
        partes = ParteDeProduccion.select(""" id IN (SELECT parte_de_produccion_id
                                                     FROM articulo
                                                     WHERE bala_id IN (SELECT id
                                                                       FROM bala
                                                                       WHERE lote_id = %d)) """ % (self.id))
        consumos = {}
        for parte in partes:
            for consumo in parte.consumos:
                producto = consumo.productoCompra
                if producto not in consumos:
                    consumos[producto] = consumo.cantidad
                else:
                    consumos[producto] += consumo.cantidad
        return consumos

    def esta_analizada(self):
        """
        Devuelve True si el lote está analizado (tiene al menos un valor en
        los resultados de las pruebas).
        """
        valores_nulos = (' ', '', None)
        return (self.tenacidad not in valores_nulos) or \
               (self.elongacion not in valores_nulos) or \
               (self.rizo not in valores_nulos) or \
               (self.encogimiento not in valores_nulos)


cont, tiempo = print_verbose(cont, total, tiempo)

class Destino(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    albaranesSalida = MultipleJoin('AlbaranSalida')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        """
        Devuelve información básica acerca del destino.
        """
        return ", ".join((self.nombre, self.direccion, self.cp, self.ciudad, self.pais))

cont, tiempo = print_verbose(cont, total, tiempo)

class Transportista(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    albaranesEntrada = MultipleJoin('AlbaranEntrada')
    albaranesSalida = MultipleJoin('AlbaranSalida')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def parse_matricula(self):
        """
        Devuelve una tupla de dos elementos con la matrícula del
        vehículo tractor en primer lugar y la del semirremolque en segundo.
        Si no se puede parsear o determinar alguna de las dos, devuelve
        la segunda posición con la cadena vacía.
        """
        # TODO: Con expresiones regulares esto iría mejor.
        if "  " in self.matricula:
            try:
                t, s = [i.strip() for i in self.matricula.split("  ")
                        if i.strip() != ""]
            except Exception, msg:
                if DEBUG:
                    myprint("pclases::transportista::parse_matricula -> %s" % msg)
                t = self.matricula.split("  ")[0].strip()
                s = "".join(self.matricula.split("  ")[1:]).strip()
        elif " " in self.matricula:
            t = self.matricula.split(" ")[0].strip()
            s = "".join(self.matricula.split(" ")[1:]).strip()
            if len(t) <= 3 or len(s) <= 3:
                t += " "
                t += s
                s = ""
        else:
            t = self.matricula.strip()
            s = ""
        return (t, s)

cont, tiempo = print_verbose(cont, total, tiempo)

class Tarifa(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    precios = MultipleJoin('Precio')
    clientes = MultipleJoin('Cliente')
    pedidosVenta = MultipleJoin('PedidoVenta')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        """
        Devuelve una cadena con información básica de la tarifa.
        """
        if self.esta_vigente:
            vigencia = "vigente"
            if self.periodoValidezIni:
                vigencia += " desde el %s" % (
                utils.str_fecha(self.periodoValidezIni))
        else:
            vigencia = "obsoleta desde el %s" % (
                utils.str_fecha(self.periodoValidezFin))
        res = "%s (%s)" % (self.nombre, vigencia)
        return res

    def esta_vigente(self, fecha = mx.DateTime.localtime()):
        """
        Devuelve True si la tarifa está vigente en la
        fecha recibida.
        """
        res = True
        res = res and (not self.periodoValidezIni
                        or fecha >= self.periodoValidezIni)
        res = res and (not self.periodoValidezFin
                        or fecha <= self.periodoValidezFin)
        return res

    vigente = property(esta_vigente, doc = esta_vigente.__doc__)

    def esta_en_tarifa(self, producto):
        """
        Devuelve True si el producto está explícitamente en la tarifa.
        """
        if isinstance(producto, ProductoVenta):
            precios = Precio.select(AND(Precio.q.productoVentaID == producto.id,
                                        Precio.q.tarifaID == self.id))
            if precios.count() == 1:
                return True
            elif precios.count() > 1:
                myprint("WARNING: pclases.py: obtener_precio: Más de un precio para una misma tarifa y producto de venta.")
                return True
        elif isinstance(producto, ProductoCompra):
            precios = Precio.select(AND(
                        Precio.q.productoCompraID == producto.id,
                        Precio.q.tarifaID == self.id))
            if precios.count() == 1:
                return True
            elif precios.count() > 1:
                myprint("WARNING: pclases.py: obtener_precio: Más de un precio para una misma tarifa y producto de compra.")
                return True
        else:
            raise TypeError, "producto debe ser un ProductoCompra o un ProductoVenta."
        return False

    def obtener_precio(self,
                       producto,
                       precio_defecto = None,
                       tarifa_defecto = None,
                       sincronizar = True):
        """
        Dado un producto devuelve el precio que tiene en la
        tarifa. Si el producto no está incluido en la tarifa
        devuelve el precio por defecto de dicho producto.
        Si defecto != None, devuelve el precio por defecto recibido
        en lugar del precio por defecto.
        Si tarifa_defecto != None y precio == None, entonces devuelve
        el precio para la tarifa_defecto.
        Si sincronizar es False omite el sync antes de consultar el precio,
        lo cual puede significar que el precio devuelto no sea correcto si
        ha habido actualizaciones recientes desde otro puesto de trabajo. Se
        deja la opción de desactivar el sync para consultas masivas de
        precios al listar tarifas, ya que las tarifas no sueles modificarse
        tan frecuentemente como para sincronizar en esos casos puntuales
        (como por ejemplo, en la consulta valor_almacen.py, donde ahorra
        mucho tiempo -dependiendo, sobre todo, de la red- en la consulta
        y el riesgo de obtener un valor total erróneo para las valoraciones
        es mínimo).
        """
        # PLAN: Faltaría un método o algo para saber si el producto
        # finalmente estaba o no en la tarifa.
        # for p in self.precios:
        #     if p.productoVenta == producto:
        #         print "Precio tarifa", p.precio
        # print "Precio defecto", producto.preciopordefecto
        if isinstance(producto, ProductoVenta):
            precios = Precio.select(AND(Precio.q.productoVentaID == producto.id,
                                        Precio.q.tarifaID == self.id))
            if precios.count() == 1:
                precio = precios[0]
                if sincronizar:
                    precio.sync()
                precio = precio.precio
            elif precios.count() > 1:
                myprint("WARNING: pclases.py: obtener_precio: Más de un precio para una misma tarifa y producto de venta.")
                precio = precios[0]
                if sincronizar:
                    precio.sync()
                precio = precio.precio
            else:
                if precio_defecto != None:
                    precio = precio_defecto
                elif tarifa_defecto != None:
                    precio = tarifa_defecto.obtener_precio(producto)
                else:
                    precio = producto.preciopordefecto
        elif isinstance(producto, ProductoCompra):
            precios = Precio.select(AND(
                        Precio.q.productoCompraID == producto.id,
                        Precio.q.tarifaID == self.id))
            if precios.count() == 1:
                precio = precios[0]
                if sincronizar:
                    precio.sync()
                precio = precio.precio
            elif precios.count() > 1:
                myprint("WARNING: pclases.py: obtener_precio: Más de un precio para una misma tarifa y producto de compra.")
                precio = precios[0]
                if sincronizar:
                    precio.sync()
                precio = precio.precio
            else:
                if precio_defecto != None:
                    precio = precio_defecto
                elif tarifa_defecto != None:
                    precio = tarifa_defecto.obtener_precio(producto)
                else:
                    precio = producto.precioDefecto
        else:
            raise TypeError, "producto debe ser un ProductoCompra o un ProductoVenta."
        return precio

    def get_porcentaje(self, producto, fraccion = False, precio_cache = None):
        """
        Devuelve el porcentaje de la tarifa sobre el precio por defecto del
        producto.
        """
        if precio_cache == None:
            preciotarifa = self.obtener_precio(producto)
        else:
            preciotarifa = precio_cache
        try:
            porcentaje = 100.0 * ((preciotarifa / producto.precioDefecto) - 1)
        except ZeroDivisionError:
            porcentaje = 0.0
        if fraccion:
            porcentaje /= 100.0
        return porcentaje

    def asignarTarifa(self, producto, precio):
        """
        Si el producto ya tiene un precio asignado a la tarifa
        lo cambia por el precio recibido.
        Si no, crea un registro intermedio y relaciona el
        producto con la tarifa.
        Devuelve el precio del producto para la tarifa asignado
        finalmente o un código de error que es:
            -1 si no tenía precio y no se pudo crear.
            -2 si tenía precio pero no se pudo actualizar.
        """
        if isinstance(producto, ProductoVenta):
            criterio = AND(Precio.q.productoVentaID == producto.id,
                           Precio.q.tarifaID == self.id)
        elif isinstance(producto, ProductoCompra):
            criterio = AND(Precio.q.productoCompraID == producto.id,
                           Precio.q.tarifaID == self.id)
        else:
            raise TypeError, "El producto debe ser un objeto de ProductoVenta o ProductoCompra."
        precios = Precio.select(criterio)
        if precios.count() == 0:
            # Crear registro
            if isinstance(producto, ProductoVenta):
                try:
                    reg_precio = Precio(productoVenta = producto,
                                        productoCompra = None,
                                        tarifa = self,
                                        precio = precio)
                except: # Supongo que por no estar el precio en flotante.
                    return -1
            elif isinstance(producto, ProductoCompra):
                try:
                    reg_precio = Precio(productoVenta = None,
                                        productoCompra = producto,
                                        tarifa = self,
                                        precio = precio)
                except: # Supongo que por no estar el precio en flotante.
                    return -1
        else:
            # Actualizarlo
            reg_precio = precios[0]
            # No debería haber más de uno. Si lo hay, me quedo con el primero.
            try:
                reg_precio.precio = precio
            except:
                # ERROR: El precio no se puede convertir a flotante.
                return -2
        reg_precio.syncUpdate()
        return reg_precio.precio

    def get_tarifa_defecto():
        """
        Devuelve la tarifa por defecto (venta público o tarifa1).
        None si no hay tarifa por defecto para PVP.
        """
        try:
            tarifa = Tarifa.select(Tarifa.q.nombre.contains("enta p"))[0]
        except IndexError:
            try:
                tarifa = Tarifa.select(Tarifa.q.nombre.contains("arifa 1"))[0]
            except IndexError:
                tarifa = None
        return tarifa

    get_tarifa_defecto = staticmethod(get_tarifa_defecto)

cont, tiempo = print_verbose(cont, total, tiempo)

class Precio(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #------------- productoVentaID = ForeignKey('ProductoVenta', default = None)
    #------------------------------------------- tarifaID = ForeignKey('Tarifa')
    #----------- productoCompraID = ForeignKey('ProductoCompra', default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_producto(self):
        """
        Devuelve el producto (de compra o de venta) relacionado
        con el precio de tarifa actual.
        """
        if self.productoVentaID != None:
            return self.productoVenta
        elif self.productoCompraID != None:
            return self.productoCompra
        else:
            return None

    def set_producto(self, producto):
        if isinstance(producto, ProductoVenta):
            self.productoVenta = producto
            self.productoCompra = None
        elif isinstance(producto, ProductoCompra):
            self.productoVenta = None
            self.productoCompra = producto
        else:
            raise TypeError, 'El parámetro "producto" debe ser del tipo ProductoCompra o ProductoVenta.'

    producto = property(get_producto, set_producto, "Producto relacionado con el precio de tarifa.")

cont, tiempo = print_verbose(cont, total, tiempo)

class ParteDeProduccion(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    articulos = MultipleJoin('Articulo')
    # empleados = RelatedJoin('Empleado', joinColumn = 'parteDeProduccionID', otherColumn = 'empleadoID', intermediateTable = 'parte_de_produccion_empleado')
    horasTrabajadas = MultipleJoin('HorasTrabajadas', joinColumn = 'partedeproduccionid') # Ver BUG de la clase HorasTrabajadas
    incidencias = MultipleJoin('Incidencia')
    consumos = MultipleJoin('Consumo')
    descuentosDeMaterial = MultipleJoin('DescuentoDeMaterial')
    #------------------- partidaCemID = ForeignKey('PartidaCem', default = None)
    bigbags = MultipleJoin("Bigbag")
    PDPConfSilos = MultipleJoin("PDPConfSilo")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        producto = self.get_producto_fabricado()
        if not producto:
            producto = "Vacío"
        else:
            producto = producto.descripcion
        return "%s (%s --> %s): %s" % (self.puid, self.fechahorainicio,
                self.fechahorafin, producto)

    def save_conf_silos(self, silos = {}, fechahora = mx.DateTime.localtime()):
        """
        Guarda la configuración de los silos reales y de granza reciclada
        recibidos. El diccionario debe contener objetos silos (o enteros
        de silo "ficticio" de reciclada), producto consumiéndose y porcentaje
        marcado en un diccionario con el silo o el entero como clave.
        P.ej.:
        silos = {Silo_1: {'productoCompra': ProductoCompra_1,
                          'porcentaje': 0.5},
                 1: {'productoCompra': ProductoCompra_2,
                     'porcentaje': 0.5}
                }
        OJO: No se comprueba que la suma de porcentajes sea 1.0 (100%).
        Compara cada registro con el último del parte y solo guarda objetos
        de configuración de silos si han cambiado en producto o porcentaje.
        """
        prev_conf = self.get_conf_silos(fechahora)
        if not PDPConfSilo.cmp_conf_silos(silos, prev_conf):
            for key_silo in silos.keys():
                if isinstance(key_silo, Silo):
                    silo = key_silo
                    reciclada = None
                else:
                    silo = None
                    reciclada = key_silo
                PDPConfSilo(silo = silo,
                            reciclada = reciclada,
                            productoCompra = silos[key_silo]['productoCompra'],
                            fechahora = fechahora,
                            porcentaje = silos[key_silo]['porcentaje'],
                            parteDeProduccion = self)

    def get_conf_silos(self, fechahora = mx.DateTime.localtime()):
        """
        Devuelve un diccionario de silos con el porcentaje marcado en cada
        uno de ellos y el producto de compra seleccionado en ese momento como
        materia prima a través del registro PDPConfSilo que lleva como valor
        de la clave Silo. La clave puede ser un objeto silo o un entero
        representando el silo "ficticio" de granza reciclada.
        Si un silo no estaba marcado, lo devuelve con None.
        """
        # Partiendo de la fechahora de inicio del parte, voy recorriendo la
        # configuración por si a lo largo del parte se ha modificado la
        # configuración del silo.
        res = defaultdict(lambda: None)
        css = self.PDPConfSilos[:]
        css.sort(key = lambda cs: cs.fechahora)
        for cs in css:
            # Sanity check:
            if not (cs.parteDeProduccion.fechahorainicio
                    <= cs.fechahora <= cs.parteDeProduccion.fechahorafin):
                raise AssertionError, "pclases::ParteDeProduccion."\
                        "get_conf_silos -> [%s] Configuración inválida "\
                        "para %s. Hora incorrecta: %s (%s)" % (
                                self.puid,
                                self.get_info(),
                                utils.str_fechahora(cs.fechahora),
                                cs.get_info())
            if cs.fechahora > fechahora:
                break
            # Se trata de agrupar por misma fechahora (segundos incluidos). Si
            # el registro que voy a tratar ahora no tiene la misma fechahora
            # que los de antes (con comprobar uno, me vale), vacío el dict.
            if res and res[res.keys()[0]].fechahora != cs.fechahora:
                res = defaultdict(lambda: None)
            if cs.silo:
                res[cs.silo] = cs
            else:
                res[cs.reciclada] = cs
        # Check de que lleva todos los silos y que entre ellos sumaban el 100%
        sum_silos = sum([res[silo].porcentaje for silo in res if res[silo]])
        assert (sum_silos == 1.0 or sum_silos == 0.0),\
                    "[%s] Configuración de silos inválida para %s." % (
                            self.puid,
                            utils.str_fechahora(fechahora))
        return res

    def get_historial_conf_silos(self):
        """
        Devuelve un diccionario de horas con todas las configuraciones
        tomadas por el parte en cuanto a consumo de porcentajes de silos.
        En cada clave hay un diccionario completo con la configuración en
        ese momento. Las claves del diccionario "interno" son los silos
        a los que corresponde la configuración o bien un número entero que
        representa el silo ficticio de donde consumió granza reciclada
        (empezando por 0). Las claves de "primer nivel" del diccionario
        devuelto son "fechahoras".
        Al menos devolverá dos "fechahora": la de inicio y finalización del
        parte.
        """
        res = OrderedDict()
        res[self.fechahorainicio] = self.get_conf_silos(self.fechahorainicio)
        res[self.fechahorafin] = self.get_conf_silos(self.fechahorafin)
        css = self.PDPConfSilos[:]
        css.sort(key = lambda cs: cs.fechahora)
        for cs in css:
            res[cs.fechahora] = self.get_conf_silos(cs.fechahora)
        return res

    def _es_del_mismo_tipo(self, pdp):
        """
        Devuelve True si el tipo del parte y el del parte recibido es el
        mismo.
        """
        assert (type(self) == type(pdp))
        funcs_tipo = [f for f in dir(self) if f.startswith("es_de_")]
        iguales = True
        for f in funcs_tipo:
            iguales = iguales and (bool(getattr(self, f)())
                                    == bool(getattr(pdp, f)()))
        return iguales

    def siguiente(self):
        """
        Devuelve el siguiente parte (cronológicamente) del mismo tipo que el
        actual o None si no hay más.
        """
        # Se tiene que cumplir que:
        # pdp.anterior().siguiente() == pdp == pdp.siguiente().anterior()
        res = None
        pdps = ParteDeProduccion.select(
                ParteDeProduccion.q.fechahorainicio > self.fechahorainicio,
                orderBy = "fechahorainicio")
        for pdp in pdps:
            if self._es_del_mismo_tipo(pdp):
                res = pdp
                break
        return res

    def anterior(self):
        """
        Devuelve el anterior parte (cronológicamente) del mismo tipo que el
        actual o None si es el primero.
        """
        res = None
        pdps = ParteDeProduccion.select(
                ParteDeProduccion.q.fechahorainicio < self.fechahorainicio,
                orderBy = "-fechahorainicio")
        for pdp in pdps:
            if self._es_del_mismo_tipo(pdp):
                res = pdp
                break
        return res

    def buscar_o_crear_albaran_interno(self, incluir_consumos_auto = False):
        """
        Busca un albarán interno con los consumos del parte de producción
        PDP. Si no existe lo crea.
        Se asegura de que los consumos del parte queden reflejados en el
        albarán interno, aunque quede vacío porque se hayan eliminado los
        consumos del parte. No se elimina un albarán interno vacío para
        evitar huecos en la numeración al eliminarse después de haberse
        creado otro con posterioridad.
        """
        albint = self.albaranInterno
        if albint == None:
            albint = self.crear_albaran_interno()
        if albint != None:
            # 1.- Elimino las LDVs del albarán para volcarlas de nuevo
            for ldv in albint.lineasDeVenta:
                ldv.destroy(ventana = __file__)
            # 2.- Agrego los consumos QUE NO SEAN AUTOMÁTICOS NI DE GRANZA como
            # nuevas LDVs del albarán interno, a no ser que se indique lo
            # contrario por parámetro.
            for c in self.consumos:
                es_de_granza = c.silo != None
                es_automatico = len(c.productoCompra.consumosAdicionales) != 0
                if DEBUG:
                    myprint("es_de_granza", es_de_granza,
                            "es_automatico", es_automatico)
                if not es_de_granza:
                    if not incluir_consumos_auto and es_automatico:
                        continue
                    ldv = LineaDeVenta(productoCompra = c.productoCompra,
                                       cantidad = c.cantidad,
                                       precio = c.productoCompra.precioDefecto,
                                       albaranSalida = albint,
                                       pedidoVenta = None,
                                       facturaVenta = None,
                                       productoVenta = None)
                    Auditoria.nuevo(ldv, None, __file__)
        return albint

    def crear_albaran_interno(self):
        """
        Crea un albarán "interno" de salida (interno = cliente es la propia
        empresa).
        Devuelve el albarán creado o None si no se pudo crear.
        """
        cliente = DatosDeLaEmpresa.get_cliente()
        if cliente == None:
            myprint("pclases.py::class ParteDeProduccion::"
                    "crear_albaran_interno -> No se pudo encontrar propia "
                    "empresa como cliente.")
            albaran = None
        else:
            #numalbaran = AlbaranSalida.get_ultimo_numero_numalbaran() + 1
            # Sanity check. Se ha dado un caso de condición de carrera y
            # mientras detecto el origen, tengo que asegurar que el albarán
            # se crea. Es una postcondición del contrato: si hay cliente, el
            # albarán debe crearse y devolverse.
            numalbaran = AlbaranSalida.get_siguiente_numero_numalbaran_str()
            i = 0
            while AlbaranSalida.selectBy(numalbaran = numalbaran).count() > 0:
                # No corro riesgo de bucle infinito porque tarde o temprano
                # encontrará un número entero válido o saltará una excepción
                # al salirse de rango.
                numalbaran = AlbaranSalida.get_ultimo_numero_numalbaran() + i
                i += 1
            if not isinstance(numalbaran, str):
                numalbaran = str(numalbaran)
            albaran = AlbaranSalida(numalbaran = numalbaran,
                        transportista = None,
                        cliente = cliente,
                        facturable = True,
                        destino = None,
                        fecha = self.fecha,
                        bloqueado = True,
                        observaciones = "Albarán interno de consumos de línea"
                                        ".\nCódigo ALBINTPDPID%d\n(¡No editar"
                                        " este campo!)." % (self.id),
                        almacenOrigen = Almacen.get_almacen_principal_or_none())
        return albaran

    def get_albaran_interno(self):
        """
        Devuelve el albarán interno relacionado con el parte de
        producción o None si no se encuentra.
        OJO: La forma de localizar un albarán interno de consumos
        es por el campo observaciones. Lo siento, no queda otra y
        de momento se hará así hasta nueva orden.
        """
        albs = AlbaranSalida.select(AlbaranSalida.q.observaciones.contains("ALBINTPDPID%d" % self.id))
        if albs.count() == 0:
            return None
        return albs[0]      # No debería tampoco haber más de 1.

    albaranInterno = property(get_albaran_interno)

    def get_grupos(self):
        """
        Devuelve un diccionario de grupos que trabajaron en el parte.
        Si algún trabajador no pertenece a un grupo, se asigna un
        grupo None para él.
        Los valores del diccionario son el número de horas totales que
        invirtió el grupo en el parte (suma de horas de cada uno de
        los empleados del grupo).
        """
        res = {}
        for ht in self.horasTrabajadas:
            grupo = ht.empleado.grupo
            ht_horas = ht.horas
            if not hasattr(ht_horas, "hours"):
                ht_horas=mx.DateTime.TimeDeltaFrom(ht_horas.strftime("%H:%M"))
            if grupo not in res:
                res[grupo] = ht_horas
            else:
                res[grupo] += ht_horas
        return res

    def calcular_tiempo_real(self):
        """
        Simplemente devuelve la duración en horas (flotante) del parte.
        """
        return self.get_duracion().hours

    def calcular_tiempo_teorico(self):
        """
        Devuelve el tiempo teórico en horas que debería haber tardado el parte
        para fabricar los kilogramos teóricos de A correspondientes a los
        bultos de A que se han fabricado. Ojo: no con los kilos reales de A
        fabricados, sino con los teóricos del producto.
        """
        res = 0.0
        for a in self.articulos:
            if a.es_clase_a():
                res += a.calcular_tiempo_teorico()
        return res

    def calcular_kilos_teoricos(self):
        """
        Devuelve los kilos teóricos que deberían haberse fabricado en el
        parte según la producción estándar almacenada, que viene de la
        producción estándar de la ficha del producto al crear el parte.
        """
        horas = self.get_duracion().hours
        if self.prodestandar:
            kilos = horas * self.prodestandar
        else:   # Cojo la del producto si el parte la tiene a 0
            try:
                kilos = horas * self.productoVenta.prodestandar
            except AttributeError:  # ¿No tiene producto el parte? ?¿Vacío?
                kilos = 0.0
        return kilos

    def calcular_kilos_producidos(self, A = True, B = False, C = False):
        """
        Devuelve la producción **en kilos** del parte. Incluye los productos
        A, B y C si así se especifica en los parámetros de la función.
        """
        res = 0.0
        if A:
            res += self.calcular_kilos_producidos_A()
        if B:
            res += self.calcular_kilos_producidos_B()
        if C:
            res += self.calcular_kilos_producidos_C()
        return res

    def calcular_kilos_producidos_A(self):
        """
        Devuelve los kilos producidos **netos** reales --sin embalaje-- de
        producto A.
        """
        articulos_A = [a for a in self.articulos if a.es_clase_a()]
        kg_producidos = sum([a.peso_real - a.peso_embalaje
                             for a in articulos_A])
        return kg_producidos

    def calcular_kilos_producidos_B(self):
        """
        Devuelve los kilos producidos **netos** --sin embalaje-- de producto B.
        """
        articulos_B = [a for a in self.articulos if a.es_clase_b()]
        kg_producidos = sum([a.peso_sin for a in articulos_B])
        return kg_producidos

    def calcular_kilos_producidos_C(self):
        """
        Devuelve los kilos producidos **netos** --sin embalaje-- de producto C.
        """
        articulos_C = [a for a in self.articulos if a.es_clase_c()]
        kg_producidos = sum([a.peso_sin for a in articulos_C])
        return kg_producidos

    def calcular_rendimiento(self):
        """
        Calcula el rendimiento de la línea si el
        parte es de rollos.
        El cálculo se realiza según la fórmula:
        % rendimiento = (kg producidos A[1] * 100)
                        / (horas del parte * kg producción estándar/hora)
        los kg no cuentan el peso del embalaje __y solo son de producto A__.
        ---
        [1] En el caso de los rollos, los kg producidos de A según peso
            estándar del producto, **NO LOS REALES**. En los demás casos
            son los kilos fabricados de A sin embalaje.
        """
        # CWT: Se cuenta todo el parte completo. Incluyendo paradas.
        #try:
        #    horas_trabajadas = self.get_horas_trabajadas()
        #except AssertionError:
        #    horas_trabajadas = mx.DateTime.DateTimeDelta(0)
        #denominador = horas_trabajadas.hours * self.prodestandar
        # CWT: No se incluye producto B en el cálculo de la nueva productividad
        #kg_producidos += sum([a.rolloDefectuoso.peso_sin for a in self.articulos if a.es_rollo_defectuoso()])
        # CWT: Hay que volverlo a cambiar por kilos teóricos, no por los
        # producidos reales. Aquí «teóricos» = kilos según peso estándar del
        # producto, no kilos según velocidad de la línea.
        denominador = self.calcular_kilos_teoricos()
        try:
            kg_peso_estandar_A = self.calcular_kilos_peso_estandar_A()
            numerador = 100.0 * kg_peso_estandar_A
        except ValueError: # No soy de geotextiles. Uso peso real
            kg_producidos_A = self.calcular_kilos_producidos(A = True,
                                                             B = False,
                                                             C = False)
            numerador = kg_producidos_A * 100.0
        try:
            rendimiento = numerador / denominador
        except ZeroDivisionError:
            rendimiento = 0.0   # Aunque esto se daría si producción estándar es 0,
                                # pero así por lo menos se dan cuenta de que hay que poner algo.
                                # (Si vieran 100% -lo más parecido a infinito positivo- no les dolería "al bolsillo".)
        return rendimiento

    def calcular_kilos_peso_estandar_A(self):
        """
        Devuelve los kilos que se deberían haber fabricado si cada rollo
        llevara el peso estándar (o teórico) que debería. Solo cuenta
        producción A.
        Si el parte es de fibra lanza una excepción ValueError.
        """
        res = 0.0
        for a in self.articulos:
            if a.es_clase_a():
                try:
                    res += a.productoVenta.camposEspecificosRollo.peso_teorico
                except AttributeError:  # No es rollo.
                    txterror = "pclases::__init__ -> "\
                            "calcular_kilos_peso_estandar_A -> "\
                            "La fibra no tiene peso teórico estándar definido."
                    raise ValueError, txterror
        return res

    def calcular_productividad(self):
        """
        Calcula la productividad del parte. La productividad se define como
        horas trabajadas / duración del parte. Siendo «horas trabajadas» =
        duración del parte - sumatorio(duración incidencias).
        El resultado se devuelve en tanto por ciento (no como fracción de 1,
        sino como float en el rango 0..100, por motivos de coherencia con el
        cálculo de rendimiento).
        """
        durparte = self.get_duracion()
        try:
            ht = self.get_horas_trabajadas()
        except AssertionError, msg:
            myprint("pclases::ParteDeProduccion::calcular_productividad -> Parte ID %d con más tiempo de paradas que duración. AssertionError: %s" % (self.id, msg))
            ht = 0.0
        try:
            res = ht / durparte     # Está sobrecarcado el operador, no hace falta convertir antes a float, minutos ni nada.
        except ZeroDivisionError:
            res = 0.0
        return res * 100.0

    def get_horas_paradas(self):
        """
        Devuelve la suma de las horas de incidencias en las que la línea
        ha estado parada como un DateTimeDelta.
        """
        horas_paradas = sum([i.get_duracion() for i in self.incidencias])
        if isinstance(horas_paradas, (int, float)):
            horas_paradas = mx.DateTime.DateTimeDeltaFrom(horas_paradas)
        return horas_paradas

    def get_horas_trabajadas(self):
        """
        Devuelve las horas trabajadas (horas del parte - horas de incidencias).
        """
        horas_totales = self.get_duracion()
        horas_paradas = self.get_horas_paradas()
        assert horas_totales >= horas_paradas, "pclases.py::get_horas_trabajadas-> horas_totales < horas_paradas en parte ID %d" % (self.id)
        return horas_totales - horas_paradas

    def _corregir_duracion_paradas(self):
        """
        Si la duración total de las paradas es mayor que la duración total del
        parte, acorta las paradas hasta hacerlas coincidir.
        Si las horas de inicio y fin de las paradas se salen de las de inicio
        y fin del parte de producción, las corrige también.
        """
        sinco_minutosh = mx.DateTime.DateTimeDeltaFrom(minutes = 5)
        while self.get_horas_paradas() > self.get_duracion():
            for parada in self.incidencias:
                if (not (self.fechahorainicio
                         <= parada.horainicio
                         <= self.fechahorafin)):
                    parada.horainicio = self.fechahorainicio
                if (not (self.fechahorainicio
                         <= parada.horafin
                         <= self.fechahorafin)):
                    parada.horafin = self.fechahorafin
                if parada.horafin > parada.horainicio:
                    try:
                        parada.horafin -= sinco_minutosh
                    except TypeError:   # Algo es un datetime.datetime
                        sinco_minutosh = datetime.timedelta(minutes = 5)
                        parada.horafin -= sinco_minutosh

    def _corregir_partidaCem_nula(self):
        """
        Coloca como partida de cemento de fibra embolsada del parte de
        producción actual la última creada en el sistema.
        """
        partidaCem = PartidaCem.get_nueva_o_ultima_vacia()
        self.partidaCem = partidaCem
        self.syncUpdate()

    def se_solapa(self, desbloquear_si_mal = False):
        """
        Devuelve True si el parte se solapa con algún otro parte
        de entre todos los partes de su misma línea.
        Antes de salir se asegura que no quede como verificado un
        parte que se solape con otros si el parámetro desbloquear_si_mal
        es True (por defecto no lo es).
        NOTA: Para distinguir los partes se emplea ye-olde-method de
        contar el número de ";" que tiene en el campo observaciones.
        """
        criterio_balas = " (parte_de_produccion.observaciones "\
                "LIKE '%%;%%;%%;%%;%%;%%') "\
                "AND parte_de_produccion.partida_cem_id IS NULL"
        criterio_rollos = " (parte_de_produccion.observaciones "\
                "NOT LIKE '%%;%%;%%;%%;%%;%%') "\
                "AND parte_de_produccion.partida_cem_id IS NULL"
        criterio_cajas = "NOT parte_de_produccion.partida_cem_id IS NULL"
        mi_sqlhini = self.fechahorainicio.strftime("%Y-%m-%d %H:%M:%S")
        mi_sqlhfin = self.fechahorafin.strftime("%Y-%m-%d %H:%M:%S")
        pisan_por_abajo = """
            (parte_de_produccion.fechahorainicio < '%s'
             AND parte_de_produccion.fechahorafin <= '%s'
             AND parte_de_produccion.fechahorafin > '%s') """ % (
                mi_sqlhini, mi_sqlhfin, mi_sqlhini)
        pisan_por_arriba = """
            (parte_de_produccion.fechahorainicio >= '%s'
             AND parte_de_produccion.fechahorainicio < '%s'
             AND parte_de_produccion.fechahorafin > '%s') """ % (
                mi_sqlhini, mi_sqlhfin, mi_sqlhfin)
        pisan_por_completo = """
            (parte_de_produccion.fechahorainicio >= '%s'
             AND parte_de_produccion.fechahorafin <= '%s') """ % (
                mi_sqlhini, mi_sqlhfin)
        if self.es_de_bolsas():
            criterio_br = criterio_cajas
        elif self.es_de_fibra(): # Porque los de fibra engloban los de bolsas.
            criterio_br = criterio_balas
        elif self.es_de_geotextiles():
            criterio_br = criterio_rollos
        else:
            raise ValueError, "El parte ID %s no es ni de fibra, geotextiles"\
                              " ni embolsado."
        criterio = """ %s AND (%s OR %s OR %s) """ % (criterio_br,
                                                      pisan_por_arriba,
                                                      pisan_por_abajo,
                                                      pisan_por_completo)
        partes = ParteDeProduccion.select(criterio)
        if DEBUG:
            for p in partes:
                myprint(p.id, p.fecha, p.horainicio, p.horafin, \
                      p.fechahorainicio, p.fechahorafin)
            myprint("------------------------------")
        res = partes.count() > 1    # Sólo debo aparecer yo (self) en el
                                    # resultado de la consulta.
        if DEBUG and res:
            myprint([(pdp.id, pdp.fechahorainicio, pdp.fechahorafin)
                    for pdp in partes if pdp != self])
        if desbloquear_si_mal and res:
            self.bloqueado = False
            self.sync()
        return res

    def es_de_balas(self):
        """
        Devuelve True si es un parte de producción de balas (o bigbags) de
        fibra.
        El criterio que distingue uno y otro tipo puede cambiar. La
        función siempre devolverá el resultado correcto aunque esto
        cambie, por tanto SIEMPRE usar esto:
        if not parte.es_de_balas()... -por ejemplo-
        (Este método debería llamarse "es_de_fibra". Comento.)
        ([Meses más tarde...] Bueno, ya no. Vuelvo a comentar.)
        """
        return self.observaciones.count(';') >= 5 and not self.es_de_bolsas()

    def es_de_bolsas(self):
        """
        Devuelve True si es un parte de embolsado de fibra de cemento.
        Se usa primero el producto relacionado con el parte. Si todavía no
        tiene producción, entonces se fija en el campo correspondiente a la
        partida de cemento (ojo, no confundir con Lote de cemento, que son
        bigbags).
        """
        try:
            res = self.productoVenta.es_bolsa()
        except (IndexError, AttributeError):
            res = self.partidaCemID != None
        return res

    def es_de_cajas(self):
        return self.es_de_bolsas()  # Por si acaso.

    def es_de_bigbags(self):
        """
        Devuelve True si es un parte de fibra de cemento.
        """
        # Los partes de fibra de cemento y los de balas son idénticos a
        # efectos prácticos.
        return self.es_de_balas()

    def es_de_fibra(self):
        """
        Devuelve si el parte es de fibra (sean balas, bigbags o bolsas).
        """
        return (self.es_de_balas() or self.es_de_bigbags()
                or self.es_de_bolsas())

    def es_de_rollos(self):
        """
        Devuelve si el parte es de rollos de geotextiles.
        En realidad asume que es de geotextiles si no es de balas.
        """
        #return not self.es_de_balas()
        return not self.es_de_balas() and not self.es_de_bolsas()

    def es_de_geotextiles(self):
        """
        Devuelve si el parte es de geotextiles.
        """
        return self.es_de_rollos()

    def addEmpleado(self, empleado, horas = None):
        """
        Añade un empleado al parte de producción creando el registro que
        sirve de "puente" para la relación con atributos.
        Por defecto, si horas = None, le asigna el total de horas del
        parte de producción. Si horas != None pero no es de un tipo
        compatible con una representación de cadena de DateTimeDelta
        saltará una excepción de sqlobject.
        Si el empleado ya estaba en el parte no se hace nada.
        """
        HT = HorasTrabajadas
        qry = HT.select(AND(HT.q.empleadoid == empleado,
                            HT.q.partedeproduccionid == self))
        if qry.count() == 0:
            if horas == None:
                try:
                    if self.horafin < self.horainicio:
                        horas = (self.horafin + mx.DateTime.oneDay
                                 - self.horainicio)
                    else:
                        horas = self.horafin - self.horainicio
                except Exception, msg:
                    try:
                        horas = utils.restar_datetime_time(self.horafin,
                                                           self.horainicio)
                    except Exception, msg:
                        horas = mx.DateTime.DateTimeDelta(0)
                        if DEBUG:
                            myprint("pclases::ParteDeProduccion.addEmpleado "\
                                  "Excepción al calcular la duración del "\
                                  "parte:", msg)
                horas = horas.strftime('%H:%M')
            horas_trabajadas = HT(empleadoidID = empleado.id,
                                  partedeproduccionidID = self.id,
                                  horas = horas)    # ¿Porcuá? No lo sé.
                                                    # Debería seguir el
                                                    # formato CamelCase pero
                                                    # no lo hace.
            if DEBUG:
                myprint("pclases::ParteDeProduccion.addEmpleado "\
                      "-> Horas trabajadas:", horas_trabajadas)

    def removeEmpleado(self, empleado):
        """
        Elimina al empleado del parte, eliminando también el registro
        relacionado entre ambos.
        Si el emeplado no estaba en el parte no se hace nada. Ni siquiera se
        lanza una excepción.
        """
        HT = HorasTrabajadas
        qry = HT.select(AND(HT.q.empleadoid == empleado,
                            HT.q.partedeproduccionid == self))
        # No debería haber más de un registro con el mismo par de IDs. El método de creación lo asegura.
        if qry.count() != 0:
            # qry[0].empleado = None
            # qry[0].parteDeProduccion = None
            qry[0].destroy()

    def rolloEnParte(self, numrollo):
        """
        Dado un número de rollo devuelve cierto si el rollo se
        encuentra en el parte y falso en caso contrario.
        "numrollo" puede ser un número o un código de rollo o rollo_defectuoso.
        """
        if self.articulos == [] or self.articulos[0].balaID != None:
            return False
        for a in self.articulos:
            if a.es_rollo():
                if (a.rollo.numrollo == numrollo) or (isinstance(numrollo, str) and "R" in numrollo.upper() and numrollo.upper() == a.codigo_interno.upper()):
                    return True
            elif a.es_rollo_defectuoso():
                if (a.rolloDefectuoso.numrollo == numrollo) or (isinstance(numrollo, str) and "X" in numrollo.upper() and numrollo.upper() == a.codigo_interno.upper()):
                    return True
        return False

    def balaEnParte(self, bala):
        """
        Dado un número de bala devuelve cierto si la bala se
        encuentra en el parte y falso en caso contrario
        """
        #if self.articulos == [] or self.articulos[0].rolloID != None:
        if self.articulos == [] or not self.es_de_balas():
            return False
        for a in self.articulos:
            if a.bala.numbala == bala or a.codigo_interno == bala:
                return True
        return False

    def bigbagEnParte(self, bigbag):
        """
        Dado un número o código de bigbag devuelve cierto si el bigbag se
        encuentra en el parte y falso en caso contrario.
        """
        #if self.articulos == [] or self.articulos[0].rolloID != None:
        if self.articulos == [] or not self.es_de_bigbags():
            return False
        for a in self.articulos:
            if a.bigbag.numbigbag == bigbag or a.codigo_interno == bigbag:
                return True
        return False

    def get_duracion(self):
        """
        No se fija en los campos fechahorainicio y fechahorafin, por tanto,
        aunque se intente forzar un parte a más de un día, esta función
        NUNCA devolverá más de 23 horas, 59 minutos.
        """
        self.sync()
        try:
            duracion = self.horafin - self.horainicio
        except TypeError:   # Vienen como datetime.date y no soportan la resta.
            duracion = (utils.DateTime2DateTimeDelta(self.horafin)
                        - utils.DateTime2DateTimeDelta(self.horainicio))
        if duracion < 0:
            duracion += mx.DateTime.oneDay
        while duracion > mx.DateTime.oneDay:
            duracion -= mx.DateTime.oneDay
            # Ningún parte dura más de un turno, me aseguro que sea así
            # aunque las horas de inicio y fin estén mal.
        return duracion

    def get_produccion(self, clase_A = True, clase_B = False, clase_C = False):
        """
        Devuelve la producción del parte en kilos si es de
        balas o en metros si es de rollos de la forma:
        (cantidad_producida, unidad).
        Cuenta como producción, por defecto, solo clase A. Para incluir lo
        demás hay que activar los "flags" clase_B y clase_C.
        """
        producido = 0
        unidad = ""
        if self.es_de_fibra():
            unidad = "kg"
        elif self.es_de_geotextiles():
            unidad = "m²"
        soy_parte_de_cemento = self.es_de_bolsas()
        for a in self.articulos:
            if ((clase_A and a.es_clase_a())
                    or (clase_B and a.es_clase_b())
                    or (clase_C and a.es_clase_c())):
                cantidad_normalizada = a.cantidad   # En balas se guarda
                    # siempre el peso neto. kg de fibra pura. Sin embalaje.
                    # En rollos los m² no se afectan por el embalaje.
                    # En bigbags no se especifica peso de embalaje y en cajas
                    # es despreciable.
                if a.es_rolloC():
                    unidad = "kg"
                    cantidad_normalizada = a.peso_sin
                if soy_parte_de_cemento:     # Cantidad viene en gramos
                    # Ya no viene en gramos. Todo en kilos. Pero hay que
                    # restarle el embalaje.
                    cantidad_normalizada -= a.peso_embalaje
                producido += cantidad_normalizada
        return producido, unidad

    def calcular_consumo_mp(self):
        """
        - Si es un parte de rollos devuelve el consumo de fibra según la carga
        de cuartos de la partida completa **entre** los m² fabricados por
        todos los partes de la partida y por el número de m² fabricados
        en este parte.
        - Si es un parte de fibra devuelve el consumo de granza hecho en el
        parte.
        - Si es un parte de cemento devuelve el consumo de fibra de cemento
        en bigbags del parte.

        Los partes de producto C no son partes de producción. Son listados
        infinitos de alta de artículos sin ParteDeProduccion asociado.
        """
        if self.es_de_rollos():
            return self._get_consumo_fibra()
        elif self.es_de_balas() or self.es_de_bigbags():
            return self._get_consumo_granza()
        elif self.es_de_bolsas():
            return self._get_consumo_bigbags()
        else:
            raise NotImplementedError, "Tipo de parte no contemplado en el "\
                                       "consumo de materia prima."

    def _get_consumo_granza(self):
        return self.get_granza_consumida()

    def _get_consumo_bigbags(self):
        """
        Devuelve la suma de los pesos de los bigbags cargados en el parte
        de fibra de cemento.
        """
        res = 0.0
        for bb in self.bigbags:
            res += bb.articulo.peso_sin
        return res

    def _get_consumo_fibra(self):
        """
        Devuelve los kilos de fibra cargada en la partida del parte entre los
        m² de la partida completa y por los m² reales fabricados en el parte.
        Es la aproximación más precisa que he encontrado para hacer la
        estimación del consumo POR PARTE DE PRODUCCIÓN (ya que hasta ahora
        solo se había contemplado por partida de geotextiles completa).
        """
        pc = self._get_partidaCarga()
        try:
            kgs = sum([b.articulo.peso_sin for b in pc.balas])
        except AttributeError:  # pc es None. ¡Parte sin carga!
            res = 0.0
        else:
            # Metros totales:
            total_m2 = 0.0
            for partida in pc.partidas:
                #if partida == self.partida:
                if True:    # Si cuento los kilos de TODA la partida de carga,
                            # por fuerza he de contar los m² de TODA la
                            # producción asociada. Sea solo mi partida o sean
                            # varias partidas; que es lo normal.
                    for pdp in partida.get_partes_de_produccion():
                        m2 = pdp.get_produccion(clase_A = True,
                                                clase_B = True,
                                                clase_C = True)[0]
                        # Devuelve m² y unidad. Me quedo solo con la cantidad
                        if pdp is self:
                            mis_m2 = m2
                            #print "mis_m2", mis_m2
                        total_m2 += m2
            # Kg de fibra por metro:
            try:
                densidad_media = kgs / total_m2
            except ZeroDivisionError:
                densidad_media = 0.0
            # Kilos que se supone que YO he consumido
            res = mis_m2 * densidad_media
            #print "total_m2", total_m2, "kgs", kgs, "densidad_media", densidad_media
        return res

    def _get_partida(self):
        """
        Devuelve la partida de geotextiles relacionada con el parte a través
        de uno de sus artículos.
        Si el parte no es de geotextiles lanza una excepción.
        Si el parte está vacío devuelve None.
        """
        if not self.es_de_geotextiles():
            raise ValueError, "Solo los partes de geotextiles tienen "\
                    "asociados una partida de geotextiles."
        try:
            return self.articulos[0].partida
        except IndexError:  # Vacío
            return None

    def _get_partidaCarga(self):
        """
        Devuelve la partida de carga relacionada con el parte si es de
        geotextiles. Si es de otro tipo lanza un ValueError.
        """
        try:
            return self._get_partida().partidaCarga
        except AttributeError:
            if not self.es_de_geotextiles():
                raise ValueError, "Solo los partes de geotextiles tienen "\
                        "asociados una partida de carga de fibra en cuartos."
            else:
                return None     # Parte vacío.

    def es_nocturno(self):
        """
        Devuelve True si el parte pertenece al turno de noche.
        """
        turnosnoche = Turno.select(Turno.q.noche == True)
        res = False
        for turno in turnosnoche:
            # Con que el parte empiece en algún turno de noche (suponiendo que haya varios), ya se considera nocturno.
            if turno.horainicio > turno.horafin:
                #esta_en_turno = self.horainicio >= utils.DateTime2DateTimeDelta(turno.horainicio) and \
                #                self.horainicio <= (utils.DateTime2DateTimeDelta(turno.horafin) + mx.DateTime.oneDay)
                # Time for algebra!
                # Traslado el eje para facilitar los calculotes:
                dif = mx.DateTime.oneDay - utils.DateTime2DateTimeDelta(turno.horainicio)
                hf = utils.DateTime2DateTimeDelta(turno.horafin) + dif
                hi = mx.DateTime.DateTimeDelta(0)   # Equivalente a hi + dif módulo oneDay
                try:
                    hp = self.horainicio + dif
                        # % mx.DateTime.oneDay  -> Operation not implemented
                except TypeError:
                    hp = utils.DateTime2DateTimeDelta(self.horainicio) + dif
                while hp >= mx.DateTime.oneDay:
                    hp -= mx.DateTime.oneDay
                # Y ahora a comparar:
                esta_en_turno = hp >= hi and hp < hf
            else:
                esta_en_turno = self.horainicio >= utils.DateTime2DateTimeDelta(turno.horainicio) and \
                                self.horainicio < utils.DateTime2DateTimeDelta(turno.horafin)
            res = res or esta_en_turno
        return res

    def es_parte_de_reenvasado(self):
        """
        Un parte de reenvasado es un parte de producción que "consume" balas
        y produce nuevas balas a partir de éstas con embalaje nuevo y
        probablemente nueva calidad al solucionar mezclas de colores
        en las balas originales, etc.
        """
        return "reenvas" in self.observaciones.lower()

    def unificar_consumos(self):
        """
        Une todos los consumos del parte en uno solo por
        cada producto de compra y silo, con la cantidad sumada.
        Borra los registros que sobran, de modo que se
        queda un solo registro por consumo de producto de
        compra y parte de producción (se evitan así muchos
        problemas por registros innecesarios).
        NOTA: Los campos "antes" y "despues" no se tocan,
        ya que no se usan salvo para discriminar el tipo de
        consumo en determinados productos.
        """
        dcons = {}  # Diccionario de consumos por producto.
        for c in self.consumos:
            key = (c.productoCompraID, c.siloID)
            if key not in dcons:
                dcons[key] = []
            dcons[key].append(c)
        # Una vez los consumos están agrupados por producto, se unifica en
        # el primero de ellos las cantidades del resto (que se eliminan).
        for key in dcons:
            if len(dcons[key]) > 1:
                for consumo in dcons[key][1:]:
                    dcons[key][0].cantidad += consumo.cantidad
                    consumo.destroy()
            # OJO: HACK: CHAPUZA: HARCODED: etc... Caso especial de los tubos
            # de cartón. Se deben consumir en cantidades enteras, así que
            # compruebo si es un consumo de ese tipo, y en ese caso redondeo
            # tanto el consumo como las existencias del producto. Para
            # redondear debe estar una décima por encima o por debajo del
            # número entero; así sólo redondeamos cada 3 rollos de 1.83, 2 de
            # 2.75 (aunque en ese caso no sería necesario), etc. La
            # descripción del producto de compra debe contener las palabras
            # "*cleo*" y "*cart*" o "*tubo*".
            consumo = dcons[key][0]
            producto = consumo.productoCompra
            if producto.es_nucleo_carton():
                if abs(consumo.cantidad - round(consumo.cantidad, 0)) <= 0.1:
                    consumo.cantidad = round(consumo.cantidad, 0)
                    consumo.sync()
                    consumo.productoCompra.existencias = round(consumo.productoCompra.existencias, 0)
                    consumo.productoCompra.sync()

    def unificar_desechos(self):
        """
        Une todos los desechos del parte en uno solo por
        cada producto de compra y observaciones (motivo por
        el que se ha considerado defectuoso ese materuial),
        con la cantidad sumada.
        Borra los registros que sobran, de modo que se
        queda un solo registro por desecho de producto de
        compra y parte de producción (se evitan así muchos
        problemas por registros innecesarios).
        Los desechos (DescuentoDeMaterial) que quedan con
        cantidad cero no se eliminan.
        """
        dcons = {}  # Diccionario de desechos por producto.
        for c in self.descuentosDeMaterial:
            key = (c.productoCompraID, c.observaciones)
            if key not in dcons:
                dcons[key] = []
            dcons[key].append(c)
        # Ua vez los desechos están agrupados por producto, se unifica en
        # el primero de ellos las cantidades del resto (que se eliminan).
        for key in dcons:
            if len(dcons[key]) > 1:
                for desecho in dcons[key][1:]:
                    dcons[key][0].cantidad += desecho.cantidad
                    desecho.destroy()

    def get_granza_consumida(self):
        """
        Si el parte es de fibra (normal o de cemento) devuelve
        la granza consumida. Si es de rollos lanza una excepción ValueError.
        """
        if self.es_de_rollos():
            raise ValueError, "El parte ID %d no es de fibra. No consume granza como materia prima." % (self.id)
        return sum([c.cantidad for c in self.consumos if c.es_de_granza()])

    def get_producto_fabricado(self):
        """
        Devuelve el producto de venta fabricado en el parte
        de producción o None si no se produjo nada.
        """
        #if len(self.articulos) > 0:
            #return self.articulos[0].productoVenta
        try:
            a = Articulo.selectBy(parteDeProduccionID = self.id)[0]
        except IndexError:
            return None
        return a.productoVenta
        #return None

    def set_producto_fabricado(self, producto):
        """
        Hace que el producto fabricado del parte sea el recibido
        poniendo el mismo como productoVenta de los artículo del parte.
        """
        if not isinstance(producto, ProductoVenta):
            raise TypeError, "El parámetro debe ser un objeto de la clase ProductoVenta."
        for a in self.articulos:
            a.productoVenta = producto

    productoVenta = property(get_producto_fabricado, set_producto_fabricado, doc = "Producto de venta fabricado en el parte.")

    def _corregir_campos_fechahora(self):
        """
        Corrige el valor de fechahorainicio y fechahorafin del parte actual
        para que coincidan con los campos fecha, horainicio y horafin.
        """
        fechahorainicio, fechahorafin = self.__calcular_campos_fechahora()
        try:
            self.fechahorainicio = fechahorainicio
            self.fechahorafin = fechahorafin
        except Exception, e:
            # Jaleo de versiones entre SQLObject, mx y datetime
            self.fechahorainicio = datetime.datetime(*fechahorainicio.timetuple()[:7])
            self.fechahorafin = datetime.datetime(*fechahorafin.timetuple()[:7])
        self.syncUpdate()

    def __calcular_campos_fechahora(self):
        """
        Devuelve una tupla con los campos fechahorainicio y fechahorafin
        calculados en base a fecha, fechahora y fechafin.
        """
        self.sync()    # Necesario para asegurar un mx en el atributo.
        fechahorainicio = utils.unir_fecha_y_hora(self.fecha, self.horainicio)
        fechahorafin = utils.unir_fecha_y_hora(self.fecha, self.horafin)
        if fechahorafin < fechahorainicio:
            fechahorafin += mx.DateTime.oneDay
        return (fechahorainicio, fechahorafin)

    def _comprobar_coherencia_campos_fechahora(self):
        """
        Devuelve True si si los campos fechahora son coherentes. Esto
        es, si la fechahorainicio y fechahorafin coinciden con fecha,
        horainicio y horafin.
        """
        fechahorainicio, fechahorafin = self.__calcular_campos_fechahora()
        return fechahorainicio == self.fechahorainicio and fechahorafin == self.fechahorafin

    def get_fechalaboral(self):
        """
        Devuelve la fecha del parte que corresponde al día "laboral" del mismo.
        Los días naturales van de 00:00:00 a 23:59:59, los días "laborales"
        van desde las 6:00:00 a las 5:59:59 del día "natural" siguiente.
        Si la fecha de inicio del parte es antes de las 6 de la mañana pero
        después de las 12, pertenece al día anterior al que indica el campo
        fechahorainicio (que marca siempre el día natural).
        En otro caso, corresponden ambas.
        Si el parte ocupa dos días laborables (p. ej. empieza a las 5:00 y
        acaba a las 13:00) se asiganará al día laborable que empieza a las 6:00
        del día natural anterior.
        """
        dia = mx.DateTime.DateTimeFrom(day = self.fechahorainicio.day,
                                       month = self.fechahorainicio.month,
                                       year = self.fechahorainicio.year)
        if (self.fechahorainicio.hour >= 0
           and self.fechahorainicio.hour < 6):
            dia -= mx.DateTime.oneDay
        return dia

cont, tiempo = print_verbose(cont, total, tiempo)

class PDPConfSilo(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------------- siloID = ForeignKey('Silo')
    #--------------------- parteDeProduccionID = ForeignKey('ParteDeProduccion')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        res = "PDPConfSilo: [%s] %s estaba consumiendo %s de %s al %s%%" % (
                    utils.str_fechahora(self.fechahora),
                    self.parteDeProduccion.puid,
                    self.productoCompra.descripcion,
                    self.silo.puid,
                    utils.float2str(self.porcentaje * 100, autodec = True)
                    )
        return res
    @staticmethod
    def cmp_conf_silos(silos, conf_silos):
        """
        Recibe un diccionario con objetos silo o enteros representando los
        silos ficticios de granza reciclada. Los valores son otro diccionario
        con producto de compra y porcentaje.
        Recibe también otro diccionario de configuraciones de silo.
        Compara los valores y devuelve True si coinciden silos (o enteros),
        porcentajes y productos.
        """
        # TODO: PORASQUI: Si se crean dos balas a la misma hora pero con
        # porcentajes diferentes en, por ejemplo, dos silos marcados. Se
        # machaca la configuración en vez de crear una nueva.
        res = len(silos) == len(conf_silos)
        if res:
            for silo_key in silos:
                cs_dict = silos[silo_key]
                try:
                    cs_db = conf_silos[silo_key]
                    if (cs_dict['porcentaje'] != cs_db.porcentaje
                         or cs_dict['productoCompra'] != cs_db.productoCompra):
                        res = False
                        break
                except (KeyError,        # El silo no está presente en la conf.
                        AttributeError): # No hay configuración para ese silo.
                                         # ¿Hora incorrecta?
                    res = False
                    break
        return res

cont, tiempo = print_verbose(cont, total, tiempo)

class CentroTrabajo(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    empleados = MultipleJoin('Empleado')
    partesDeTrabajo = MultipleJoin('ParteDeTrabajo')
    #------------------------- almacenID = ForeignKey("Almacen", default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)


cont, tiempo = print_verbose(cont, total, tiempo)

class Empleado(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    # partesDeProduccion = RelatedJoin('ParteDeProduccion', joinColumn = 'empleadoID', otherColumn = 'parteDeProduccionID', intermediateTable = 'parte_de_produccion_empleado')
    horasTrabajadas = MultipleJoin('HorasTrabajadas', joinColumn = 'empleadoid')    # Ver BUG en la clase HorasTrabajadas.
    #----------------------------- centroTrabajoID = ForeignKey('CentroTrabajo')
    nominas = MultipleJoin('Nomina')
    partesDeTrabajo = MultipleJoin('ParteDeTrabajo')
    #----------------------- categoriaLaboralID = ForeignKey('CategoriaLaboral')
    ausencias = MultipleJoin('Ausencia')
    # grupos = MultipleJoin('Grupo')      # Es relación 1 a 1 en realidad.
    grupos_jt = MultipleJoin('Grupo', joinColumn = 'jefeturno_id')
    grupos_o1 = MultipleJoin('Grupo', joinColumn = 'operario1_id')
    grupos_o2 = MultipleJoin('Grupo', joinColumn = 'operario2_id')
    documentos = MultipleJoin('Documento')
    controlesHoras = MultipleJoin('ControlHoras')
    bajas = MultipleJoin("Baja")
    ordenesEmpleados = MultipleJoin("OrdenEmpleados")
    comerciales = MultipleJoin("Comercial") # En realidad es relación 1 a 1.
    #------------------------- usuarioID = ForeignKey("Usuario", default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_categoriaLaboral_vigente(self, fecha = mx.DateTime.today()):
        """
        Devuelve la categoría laboral vigente según fecha o None.
        """
        res = None
        if self.categoriaLaboral:
            codigo = self.categoriaLaboral.codigo
            cats = [c for c in CategoriaLaboral.selectBy(codigo = codigo)
                    if c.fecha]
            cats.sort(key = lambda c: c.fecha)
            try:
                res = CategoriaLaboral.select(AND(
                    CategoriaLaboral.q.codigo == codigo,
                    CategoriaLaboral.q.fecha == None))[0] # Por defecto
            except IndexError:
                res = self.categoriaLaboral     # Uso la que tenga el empleado
                                        # como categoría laboral por defecto.
            for c in cats:
                if c.fecha and c.fecha > fecha:
                    break
                res = c
        return res

    def get_nombre_completo(self):
        """
        Devuelve el nombre del empleado en la forma 'apellidos, nombre'
        """
        return "%s, %s" % (self.apellidos, self.nombre)

    def calcular_plus_no_absentismo(self, f1, f2):
        """
        Calcula el importe total del plus de no absentismo del empleado
        sumando el concepto plusAbsentismo de sus controles de horas entre
        las fechas recibidas, ambas incluidas por si son la misma.
        """
        if f1 > f2:
            f1, f2 = f2, f1
        # Mucho más rápido que recorrer la lista de objetos relacionados,
        # que el motor de la BD cargue con las operaciones de fecha:
        chs = ControlHoras.select(AND(ControlHoras.q.fecha >= f1,
                                      ControlHoras.q.fecha <= f2,
                                      ControlHoras.q.empleadoID == self.id))
        res = 0.0
        for ch in chs:
            res += ch.plusAbsentismo
        return res

    def calcular_importe_libre(self, f1, f2):
        """
        Calcula el importe total del plus de no absentismo del empleado
        sumando el concepto plusAbsentismo de sus controles de horas entre
        las fechas recibidas, ambas incluidas por si son la misma.
        """
        if f1 > f2:
            f1, f2 = f2, f1
        # Mucho más rápido que recorrer la lista de objetos relacionados,
        # que el motor de la BD cargue con las operaciones de fecha:
        chs = ControlHoras.select(AND(ControlHoras.q.fecha >= f1,
                                      ControlHoras.q.fecha <= f2,
                                      ControlHoras.q.empleadoID == self.id))
        res = 0.0
        for ch in chs:
            res += ch.importeLibre
        return res

    def get_grupo(self):
        try:
            if self.grupos_jt != []:
                return self.grupos_jt[0]
            if self.grupos_o1 != []:
                return self.grupos_o1[0]
            return self.grupos_o2[0]
        except IndexError:
            return None

    grupo = property(get_grupo, doc = "Grupo al que pertenece como jefe de turno, operario 1 u operario 2.")

    def get_grupo_and_rol(self):
        """
        Devuelve el nombre del grupo y el rol que tiene en él como
        cadena de texto: "Jefe de turno", "Operario 1" u "Operario 2".
        """
        try:
            if self.grupos_jt != []:
                return self.grupos_jt[0].nombre, "Jefe de turno"
            if self.grupos_o1 != []:
                return self.grupos_o1[0].nombre, "Operario 1"
            return self.grupos_o2[0].nombre, "Operario 2"
        except IndexError:
            return "", ""
        except AttributeError:
            return "", ""

    def get_diasConvenioRestantes(self, anno = mx.DateTime.localtime().year):
        dc_cogidos = len([a for a in self.ausencias if a.motivo and a.motivo.convenio and a.fecha.year == anno])
        try:
            dc_restantes = self.categoriaLaboral.diasConvenio - dc_cogidos
        except AttributeError:
            dc_restantes = 0
        return dc_restantes

    def get_diasAsuntosPropiosRestantes(self, anno = mx.DateTime.localtime().year):
        dap_cogidos = len([a for a in self.ausencias if a.motivo and not a.motivo.convenio and a.fecha.year == anno])
        try:
            dap_restantes = self.categoriaLaboral.diasAsuntosPropios - dap_cogidos
        except AttributeError:
            dap_restantes = 0
        return dap_restantes

    diasConvenioRestantes = property(get_diasConvenioRestantes, doc = "Días de ausencia de convenio restantes para el año en curso.")

    diasAsuntosPropiosRestantes = property(get_diasAsuntosPropiosRestantes, doc = "Días de ausencia por asuntos propios restantes para el año en curso.")

    def calcular_horas_produccion(self, fechaini, fechafin):
        # UNUSED, NOT TESTED
        """
        Devuelve el tiempo trabajado en partes de producción en horas en forma
        de diccionario de fibras, geotextiles y geocompuestos:
        res = {'fibra': {dia1: {'día': mx.DateTime.DateTimeDelta,
                                'noche': mx.DateTime.DateTimeDelta},
                         dia2: {'día': mx.DateTime.DateTimeDelta,
                                'noche': mx.DateTime.DateTimeDelta},
                         ...
                        }
               'geotextiles': {},
               'geocompuestos': {}
              }
        dia(n) -> Día laboral (empieza a las 6:00).
         'día'   -> Horas del día dia(n) que trabajó entre las 6:00 y las 22:00.
         'noche' -> Horas del día dia(n) que trabajó entre las 22:00 y las 6:00.
        """
        PDP = ParteDeProduccion
        inicio = mx.DateTime.DateTimeFrom(day = fechaini.day,
                                          month = fechaini.month,
                                          year = fechaini.year,
                                          hour = 6)
        fin = mx.DateTime.DateTimeFrom(day = fechafin.day,
                                       month = fechafin.month,
                                       year = fechafin.year,
                                       hour = 6)
        fin += mx.DateTime.oneDay   # hasta 6:00 AM del día siguiente entra
                                    # en el día laboral.
        partes = PDP.select(PDP.q.fechahorainicio >= inicio,
                            PDP.q.fechahorainicio <= fin)
        dias = {"fibra": {}, "geotextiles": {}}
        for parte in partes:
            for ht in parte.horasTrabajadas:
                if ht.empleado == self:
                    fecha = parte.get_fechalaboral()
                    if parte.es_de_fibra():
                        tipo = "fibra"
                    elif parte.es_de_geotextiles():
                        tipo = "geotextiles"
                    else:
                        raise ValueError, "pclases.py::Empleado::calcular_ho"\
                                          "ras_produccion -> El parte no es "\
                                          "de fibra ni de geotextiles. ¿Ya s"\
                                          "e ha abierto la línea de geocompu"\
                                          "estos y yo con estos pelos?"
                    try:
                        dias[tipo][fecha]["día"] += ht.horas_dia
                    except KeyError:
                        dias[tipo][fecha]["día"] = ht.horas_dia
                    try:
                        dias[tipo][fecha]["noche"] += ht.horas_noche
                    except KeyError:
                        dias[tipo][fecha]["noche"] = ht.horas_noche
        return dias

cont, tiempo = print_verbose(cont, total, tiempo)

class HorasTrabajadas(SQLObject, PRPCTOO):
    # BUG: Debido a que he tenido que asegurar la compatibilidad hacia
    # atrás, me he saltado el "convention style" de SQLObject en las
    # tablas (../BD/tablas.sql) y en esta clase se me duplican las columnas
    # empleadoid y partedeproduccionid si no las declaro tal y como en las
    # tablas.
    class sqlmeta:
        table = "parte_de_produccion_empleado"
        fromDatabase = True
    #empleado = ForeignKey('Empleado', dbName = 'empleadoid')
    #parteDeProduccion = ForeignKey('ParteDeProduccion',
    #                                 dbName = 'partedeproduccionid')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_parteDeProduccion(self):
        return self.partedeproduccionid

    def set_parteDeProduccion(self, valor):
        self.partedeproduccionid = valor

    def get_parteDeProduccionID(self):
        return self.partedeproduccionidID

    def set_parteDeProduccionID(self, valor):
        self.partedeproduccionidID = valor

    parteDeProduccionID = property(get_parteDeProduccionID,
                                   set_parteDeProduccionID)
    # Por coherencia con el resto de clases
    parteDeProduccion = property(get_parteDeProduccion, set_parteDeProduccion)
    # Por coherencia con el resto de clases

    @property
    def empleado(self):
        return self.empleadoid

    @empleado.setter
    def empleado(self, e):
        self.empleadoid = e

    @empleado.deleter
    def empleado(self):
        del self.empleadoid

    def get_horas_dia(self):
        """
        :returns: DateTimeDelta con el número de horas trabajadas entre
                  las 6:00 y las 22:00.
        """
        horainicio = mx.DateTime.TimeFrom(self.parteDeProduccion.horainicio)
        horafin = horainicio + self.horas
        NOCHE = mx.DateTime.DateTimeDeltaFrom(22*60*60)
        DIA = mx.DateTime.DateTimeDeltaFrom(6*60*60)
        if horainicio >= DIA:
            horasdia = mx.DateTime.DateTimeDeltaFrom(self.horas)
            if horafin > NOCHE:
                horasdia -= (horafin - NOCHE)
        else:
            horasdia = horafin - DIA
        return horasdia

    def get_horas_noche(self):
        """
        :returns: DateTimeDelta con el número de horas transcurridas entre
                  22:00 y las 6:00.
        """
        return mx.DateTime.DateTimeDeltaFrom(self.horas) - self.get_horas_dia()

    horas_dia = property(get_horas_dia)
    horas_noche = property(get_horas_noche)

cont, tiempo = print_verbose(cont, total, tiempo)

class Nomina(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------------------------- empleadoID = ForeignKey('Empleado')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def calcular_total(self, actualizar = True):
        """
        Devuelve el total de la nómina.
        Se calcula sumando los campos gratificacion + plusJefeTurno +
        plusNoAbsentismo + plusFestivo + plusTurnicidad +
        plusMantenimientoSabados + totalHorasExtra + totalHorasNocturnidad +
        base + otros
        Si actualizar es False no guarda el valor en el campo "calculado"
        cantidad.
        """
        total = (self.gratificacion + self.plusJefeTurno +
                 self.plusNoAbsentismo + self.plusFestivo +
                 self.plusTurnicidad + self.plusMantenimientoSabados +
                 self.totalHorasExtra + self.totalHorasNocturnidad +
                 self.base + self.otros)
        if actualizar:
            self.cantidad = total
            self.syncUpdate()
        return total

cont, tiempo = print_verbose(cont, total, tiempo)

class DescuentoDeMaterial(SQLObject, PRPCTOO):
    """
    Descuento de producto de compra no relacionado directamente con
    producción.
    Se usará principalmente para dar de alta los desechos que se tiran
    (núcleos mojados, plásticos rotos, etc.) y se hará desde los partes
    de producción. En principio podría usarse para cualquier variación
    de existencias. La cantidad será en positivo para restar existencias
    y en negativo para sumar (en caso de cancelar un descuento de
    material o algo).
    Hay que tener cuidado y sincronizar el objeto producto de compra
    después de crear o actualizar cada consumo, para que siempre esté
    en la BD con la cantidad correcta y evitar efectos secundarios
    relacionados con la concurrencia y la caché de objetos.
    """
    class sqlmeta:
        fromDatabase = True
    #--------------------------- productoCompraID = ForeignKey('ProductoCompra')
    #--------------------- parteDeProduccionID = ForeignKey('ParteDeProduccion')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def desechar(cls, producto, cantidad, pdp = None, observaciones = ''):
        """
        Crea un registro de descuento de material con la cantidad
        recibida y se asegura de que el producto de venta quede
        con sus existencias disminuidas en esa cantidad (se recibe
        en positivo y se resta. Si la cantidad es negativa,
        menos-por-menos-más y se sumará).
        Las existencias finales del producto no pueden quedar en
        negativo. Devuelve el registro creado si no ocurre ningún
        error. En otro caso lanzará un error de aserción.
        """
        if not isinstance(producto, ProductoCompra):
            raise TypeError, 'pclases::desechar -> "producto" debe ser un ProductoCompra.'
        producto.sync()         # Me aseguro de que tabajo con la cantidad correcta en existencias.
        existencias_antes = producto.existencias
        if existencias_antes < cantidad:
            cantidad = producto.existencias
            producto.existencias = 0
        else:
            producto.existencias -= cantidad
        producto.syncUpdate()   # Aseguro que mis cambios pasen a la BD para evitar efectos colaterales.
        producto.sync()         # Y compruebo que no ha habido problemas de concurrencia.
        descuentoDeMaterial = cls(productoCompra = producto,
                                    parteDeProduccion = pdp,
                                    cantidad = cantidad,
                                    fechahora = mx.DateTime.localtime(),
                                    observaciones = observaciones)
        assert abs(producto.existencias - (existencias_antes - cantidad)) < 0.001, "pclases::desechar -> Error de concurrencia. Existencias antes: %f. Existencias después: %f. Cantidad desechada: %f." % (existencias_antes, producto.existencias, cantidad)
        return descuentoDeMaterial

    desechar = classmethod(desechar)

    def cambiar_cantidad(self, cantidad, fechahora = mx.DateTime.localtime()):
        """
        Cambia la cantidad consumida/desechada, actualiza
        las existencias del producto implicado y cambia la
        fechahora a la fecha y hora actual si no se indica
        lo contrario.
        No permite que el producto quede con existencias
        negativas. Devuelve la cantidad final del consumo.
        """
        productoCompra = self.productoCompra
        productoCompra.sync()
        antes = productoCompra.existencias  # @UnusedVariable
        cantidad_original = productoCompra.existencias + self.cantidad
        productoCompra.existencias = cantidad_original
        if cantidad > productoCompra.existencias:
            cantidad = productoCompra.existencias
        productoCompra.existencias -= cantidad
        productoCompra.sync()
        self.cantidad = cantidad
        self.fechahora = fechahora
        return self.cantidad

    def anular(self):
        """
        Anula el consumo de material actual.
        """
        cantidad_final = self.cambiar_cantidad(0)
        assert cantidad_final == 0, "El descuento de material ID %d (desecho) no se pudo anular por descuadre de cantidad. Cantidad sobrante = %f" % (self.id, cantidad_final)
        self.destroy()


cont, tiempo = print_verbose(cont, total, tiempo)

class Consumo(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------------- productoCompraID = ForeignKey('ProductoCompra')
    #--------------------- parteDeProduccionID = ForeignKey('ParteDeProduccion')
    #----------------------------------------------- siloID = ForeignKey('Silo')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def anular_consumo_silo(self, a_silo = None):
        """
        Anula el consumo del silo incrementando las unidades
        del producto de compra.
        Si se recibe el parámetro "a_silo" se cambia el consumo
        al silo indicado, descontando la cantidad de material del
        nuevo silo.
        Al finalizar unifica los consumos del parte por si se
        cambia a un silo que ya se había consumido en él.
        """
        assert self.silo != None, "El consumo debe ser un consumo de silo."
        assert self.parteDeProduccion != None, "El consumo debe estar relacionado con un parte de producción."
        if a_silo != None:
            assert isinstance(a_silo, Silo), "El parámetro a_silo debe ser un objeto Silo de pclases."
        producto = self.productoCompra
        producto.sync()
        producto.existencias += self.cantidad
        producto.sync()
        if a_silo == None:
            self.destroy()
        else:
            carga = a_silo.get_carga_mas_antigua()
            if carga != None:
                producto = carga.productoCompra
                producto.sync()
                producto.existencias -= self.cantidad
                producto.sync()
                self.productoCompra = producto
                self.silo = a_silo
                self.syncUpdate()
                self.parteDeProduccion.unificar_consumos()
            else:
                self.destroy()
                raise ValueError, "pclases.py::anular_consumo_silo -> No se pudo trasladar el consumo al silo %s por no haber existencias en él. El consumo se eliminó. Cree un nuevo consumo después de asegurarse que el silo %s tiene carga suficiente." % (a_silo.nombre, a_silo.nombre)

    def anular_consumo(self):
        """
        Anula un consumo eliminando el registro y aumentando
        las existencias del producto de compra en la cantidad
        consumida.
        """
        producto = self.productoCompra
        producto.sync()
        producto.existencias += self.cantidad
        producto.sync()
        self.destroy()

    def es_de_granza(self):
        """
        Devuelve True si el consumo es de granza.
        Para que un consumo sea considerado de granza se tiene que
        cumplir que:
            1.- SiloID sea <> None.
            o bien
            2.- Que el productoCompra contenga la palabra "granza" y que sea del tipo "materia prima".
        """
        if self.siloID != None:
            return True     # Está feo, pero es por optimizar.
        return self.productoCompra.es_granza()

    def get_linea_de_venta_albaran_interno(self):
        """
        Devuelve, si la tiene, la línea de venta relacionada con el consumo
        del albarán interno de consumos del parte de producción.
        """
        pdp = self.parteDeProduccion
        alb = pdp.get_albaran_interno()
        if alb:
            for ldv in alb.lineasDeVenta:
                if (ldv.producto == self.productoCompra
                    and ldv.cantidad == self.cantidad):
                    return ldv
        return None

    def get_fecha(self):
        """
        Devuelve la fecha del parte en que se hizo el consumo.
        """
        return self.parteDeProduccion and self.parteDeProduccion.fecha

    fecha = property(get_fecha, doc = get_fecha.__doc__)

cont, tiempo = print_verbose(cont, total, tiempo)

class TipoDeIncidencia(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    incidencias = MultipleJoin('Incidencia')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class Incidencia(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------- parteDeProduccionID = ForeignKey('ParteDeProduccion')
    #----------------------- tipoDeIncidenciaID = ForeignKey('TipoDeIncidencia')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_horainicio(self):
        return self.horainicio

    def get_duracion(self):
        # FIXED: BUG en cáclulo duración parada si día de horafin no coincide
        # con día de horainicio.
        try:
            duracion = self.horafin - self.horainicio
        except TypeError:   # Vienen como datetime.date y no soportan la resta.
            duracion = (utils.DateTime2DateTimeDelta(self.horafin)
                        - utils.DateTime2DateTimeDelta(self.horainicio))
        try:
            tiene_duracion_negativa = duracion < 0
        except TypeError:
            duracion = utils.DateTime2DateTimeDelta(duracion)
        finally:
            tiene_duracion_negativa = duracion < 0
        if tiene_duracion_negativa:
            duracion += mx.DateTime.oneDay
        while duracion > mx.DateTime.oneDay:
            duracion -= mx.DateTime.oneDay      # FIXME: Esto es para devolver
                # una duración correcta, pero aún quedaría arreglar la fecha
                # para que se coincidiera con la de su parte
                # (self.parteDeProduccion); ya que si ha dado más de un día es
                # porque horafin y horainicio son de fechas (días) distintos.
        return duracion

    fechahora = property(get_horainicio)

cont, tiempo = print_verbose(cont, total, tiempo)

class Abono(SQLObject, PRPCTOO):
    """
    Abonos de devolución de clientes.
    NOTA: Los números de abono _siempre_ deben cumplir el formato "Ayxxxx",
    donde "y" es un solo dígito correspondiente al último número del año y
    "xxxx" es un número entero secuencial. No deberíamos tener problemas
    hasta el año 2016, lo cual tampoco me consuela demasiado, la verdad.
    """
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- clienteID = ForeignKey('Cliente')
    #--------------------------- facturaDeAbonoID = ForeignKey('FacturaDeAbono')
    lineasDeDevolucion = MultipleJoin('LineaDeDevolucion')
    lineasDeAbono = MultipleJoin('LineaDeAbono')
    #----------------------------------------- almacenID = ForeignKey("Almacen")
    #------------------------------- obraID = ForeignKey("Obra", default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def calcular_importe_sin_iva(self):
        """
        Devuelve el importe total sin IVA del abono.
        """
        total = 0
        for ldd in self.lineasDeDevolucion:
            total -= ldd.precio     # OJO: NOTA: El precio va en positivo en
                        # el registro, pero al ser un abono, hay que restarlo.
        for lda in self.lineasDeAbono:
            total += lda.diferencia * lda.cantidad
        return total

    importeSinIva = property(calcular_importe_sin_iva,
                             doc = calcular_importe_sin_iva.__doc__)

    def calcular_total_iva(self):
        """
        Calcula el importe total de IVA con dos decimales basándose en la
        factura de abono. Si no hay, lanzará una excepción.
        """
        try:
            return self.facturaDeAbono.calcular_total_iva()
        except AttributeError:
            raise NotImplementedError, "pclases::Abono -> No puede calcularse"\
                    " el importe de IVA sin generar previamente la factura "\
                    "de abono."

    def get_albaranes(self):
        """
        Devuelve una lista de albaranes de salida relacionados
        con el abono a través de sus líneas de devolución y de
        abono.
        """
        albs = []
        for ldd in self.lineasDeDevolucion:
            if ldd.albaranSalidaID != None and ldd.albaranSalida not in albs:
                albs.append(ldd.albaranSalida)
        for lda in self.lineasDeAbono:
            if (lda.lineaDeVentaID != None
                and lda.lineaDeVenta.albaranSalidaID != None
                and lda.lineaDeVenta.albaranSalida not in albs):
                albs.append(lda.lineaDeVenta.albaranSalida)
            if (lda.servicioID != None
                and lda.servicio.albaranSalidaID != None
                and lda.servicio.albaranSalida not in albs):
                albs.append(lda.servicio.albaranSalida)
        return albs

    def get_albaranes_de_entrada_de_abono(self):
        """
        Devuelve los albaranes de entrada de abono generados a
        partir del abono.
        """
        albs = []
        for ldd in self.lineasDeDevolucion:
            if ldd.albaranDeEntradaDeAbono != None and ldd.albaranDeEntradaDeAbono not in albs:
                albs.append(ldd.albaranDeEntradaDeAbono)
        return albs

    def get_facturas(self):
        """
        Devuelve una lista de objetos FacturaVenta relacionados
        con el abono mediante sus líneas de ajuste y líneas de devolución.
        """
        fras = []
        for ldd in self.lineasDeDevolucion:
            if ldd.albaranSalidaID != None:
                for fra in ldd.albaranSalida.get_facturas():
                    if fra not in fras:
                        fras.append(fra)
        for lda in self.lineasDeAbono:
            if (lda.lineaDeVentaID != None
                and lda.lineaDeVenta.facturaVentaID != None
                and lda.lineaDeVenta.facturaVenta not in fras):
                fras.append(lda.lineaDeVenta.facturaVenta)
            elif (lda.lineaDeVentaID != None
                  and lda.lineaDeVenta.prefacturaID != None
                  and lda.lineaDeVenta.prefactura not in fras):
                fras.append(lda.lineaDeVenta.prefactura)
            if (lda.servicioID != None
                and lda.servicio.facturaVentaID != None
                and lda.servicio.facturaVenta not in fras):
                fras.append(lda.servicio.facturaVenta)
            elif (lda.servicioID != None
                  and lda.servicio.prefacturaID != None
                  and lda.servicio.prefactura not in fras):
                fras.append(lda.servicio.prefactura)
        return fras

    def get_nuevo_numabono():
        """
        Devuelve el siguiente número de abono libre.
        Siempre será el mayor número de abono más uno,
        independientemente del orden en que éstos se
        hayan introducido en la base de datos.
        El valor devuelto será un string Ayxxxx donde
        "xxxx" es el número hallado e "y" es el último
        dígito del año corriente.
        Los números no se repetirán e irán correlativos
        _dentro_ de la serie del año (dígito "y").
        """
        anno = mx.DateTime.localtime().year
        abonos_de_mi_serie, prefijo = Abono._buscar_abonos_de_la_serie(anno)
        numsabono = []
        for abono in abonos_de_mi_serie:
            numabono = abono.numabono.replace(prefijo, "")
            try:
                numabono = int(numabono)
            except ValueError:
                myprint("pclases.py: get_nuevo_numabono: Ignoro número de abono %s (ID %d) por no cumplir el formato correcto." % (numabono, abono.id))
            else:
                numsabono.append(numabono)
        numsabono.sort()
        if numsabono == []:
            sig_num = 1
        else:
            sig_num = numsabono[-1] + 1
        res = "%s%03d" % (prefijo, sig_num)
        return res

    get_nuevo_numabono = staticmethod(get_nuevo_numabono)
    albaranesSalida = property(get_albaranes, doc = get_albaranes.__doc__)
    facturasVenta = property(get_facturas, doc = get_facturas.__doc__)

    def get_numero_numabono(self):
        """
        Devuelve el número del abono como entero,
        sin el prefijo «Ay» (donde "y" es el dígito
        correspondiente al año del abono).
        """
        # VERY UGLY DIRTY HACK: El segundo dígito nunca se va a usar porque
        # presumiblemente no se harán más de 999 abonos al año. El cliente
        # lo ha confirmado y lo quiere asi. Y en los abonos donde sí se podría
        # haber usado porque no pertenecía al año (los abonos anteriores a
        # 2016) no se ha llegado a más de 60 abonos el año que más.
        return int(self.numabono[3:])

    def set_numero_numabono(self, numero):
        """
        Cambia el número del abono respetando el prefijo «Ay[y]» donde "y" es
        el último o dos últimos dígitos del año del abono.
        Si el abono no tiene fecha le pone la actual.
        Si el número no satisface la restricción de
        secuencialidad lanza una excepción (la fecha
        se modificará en cualquier caso si estaba a
        None) y vuelve a dejar el número de abono
        anterior.
        """
        if not isinstance(numero, int):
            raise TypeError, "El parámetro debe ser un número entero."
        numabono_anterior = self.numabono
        if not self.fecha:
            self.fecha = mx.DateTime.localtime()
        if self.fecha.year <= 2015:
            digito_anno = `self.fecha.year`[-1] + "0"
        else:
            digito_anno = `self.fecha.year`[-2:]
        self.numabono = "A%s%03d" % (digito_anno, numero)
        if not self.numabono_correcto():
            self.numabono = numabono_anterior
            raise ValueError, "El número %d no satisface restricción de secuencialidad para el abono ID %d" % (numero, self.id)

    numero_numabono = property(get_numero_numabono, set_numero_numabono)

    @classmethod
    def _buscar_abonos_de_la_serie(cls, anno):
        # DIRTY HACK para que reconozca A60000 y A16000 como en años
        # diferentes: 2006 y 2016. Habrá conflicto de nuevo en 2020. Se ha
        # usado ya A20001 para el año 2012.
        if anno <= 2015:
            digito_anno = str(anno)[-1] + '0'
        else:
            digito_anno = str(anno)[-2:]
        prefijo = "A" + digito_anno
        # Esto puede ser un poco lento:
        qryabonos = Abono.select(Abono.q.numabono.startswith(prefijo),
                                 orderBy = "fecha,numabono")
        abonos_de_mi_serie = [a for a in qryabonos]
        # Ordeno la lista por número de abono (esto puede ser un poco lento
        # también):
        abonos_de_mi_serie.sort(lambda a1, a2: a1.numero_numabono
                                - a2.numero_numabono)
        return abonos_de_mi_serie, prefijo

    def _buscar_abonos_de_mi_serie(self):
        """
        Devuelve una lista ordenada de los abonos correspondientes a la
        misma serie Y año del actual (self).
        """
        anno = self.fecha.year
        abonos_de_mi_serie, prefijo = Abono._buscar_abonos_de_la_serie(anno)
        assert self.numabono.startswith(
                prefijo), "Formato número abono debe ser: Ayynnn o Aynnnn"
        return abonos_de_mi_serie

    def get_abono_anterior(self):
        """
        Devuelve el abono anterior al actual según
        orden de fecha y numérico o None si es el
        primero de su año.
        Si la fecha no coincide con el dígito del año
        del número del abono saltará un "assertion error".
        """
        abonos_de_mi_serie = self._buscar_abonos_de_mi_serie()
        # Localizo mi número en la lista de números de mi año:
        i_yo = abonos_de_mi_serie.index(self)
        if i_yo == 0:
            return None
        else:
            return abonos_de_mi_serie[i_yo - 1]

    def get_abono_posterior(self):
        """
        Devuelve el abono posterior al actual según
        orden de fecha y numérico o None si es el
        primero de su año.
        Si la fecha no coincide con el dígito del año
        del número del abono saltará un "assertion error".
        """
        abonos_de_mi_serie = self._buscar_abonos_de_mi_serie()
        # Localizo mi número en la lista de números de mi año:
        i_yo = abonos_de_mi_serie.index(self)
        if i_yo == len(abonos_de_mi_serie)-1:
            return None
        else:
            return abonos_de_mi_serie[i_yo + 1]

    def numabono_correcto(self):
        """
        Devuelve True si el número del abono actual es
        correcto. Para ello comprueba que el abono con
        número anterior tenga también una fecha anterior
        (o no exista) y que el número posterior tenga
        una fecha posterior (o no exista).
        """
        anterior = self.get_abono_anterior()
        posterior = self.get_abono_posterior()
        condicion_anterior = anterior == None or (
                #anterior.numero_numabono < self.numero_numabono
                anterior.numero_numabono + 1 == self.numero_numabono
                and anterior.fecha <= self.fecha)
        condicion_posterior = posterior == None or (
                #posterior.numero_numabono > self.numero_numabono
                posterior.numero_numabono - 1 == self.numero_numabono
                and posterior.fecha >= self.fecha)
        return condicion_anterior and condicion_posterior

    def get_str_cobro(self):
        """
        Devuelve una cadena con el texto de la manera en que se ha pagado
        el abono al cliente.
        Para ello mira la factura de abono y la forma de pago de ésta:
        descontado de otra factura, o descontado en un pagaré.
        """
        fra = self.facturaDeAbono
        pagos = []
        if fra:
            for c in fra.cobros:
                if c.confirmingID:
                    p = c.confirming
                    pagos.append("Confirming %s (%s) [%s]" % (p.codigo,
                                    p.pendiente and "pendiente" or "cobrado",
                                    utils.str_fecha(p.fechaRecepcion)))
                elif c.pagareCobroID:
                    p = c.pagareCobro
                    pagos.append("Pagaré %s (%s) [%s]" % (p.codigo,
                                    p.pendiente and "pendiente" or "cobrado",
                                    utils.str_fecha(p.fechaRecepcion)))
                else:
                    pagos.append("%s [%s]" % (c.observaciones,
                                              utils.str_fecha(c.fecha)))
            for p in fra.pagosDeAbono:  # Compensada con una fra. de venta.
                pagos.append("Compensada con %s" % p.facturaVenta.numfactura)
        res = ", ".join(pagos)
        return res

cont, tiempo = print_verbose(cont, total, tiempo)

class LineaDeAbono(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #------------------------------- lineaDeVentaID = ForeignKey('LineaDeVenta')
    #--------------------------------------------- abonoID = ForeignKey('Abono')
    #----------------------- servicioID = ForeignKey('Servicio', default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    get_tarifa = lambda self: self.lineaDeVentaID and self.lineaDeVenta.get_tarifa() or None

    def get_almacen(self):
        """
        Devuelve el almacén relacionado con la línea de devolución, que será
        aquel al que se haya devuelto la mercancía.
        """
        return self.abono and self.abono.almacen or None

    # Algunas "properties" para hacerlas coherentes con las líneas de venta:
    albaranSalida = property(lambda self: self.lineaDeVentaID and self.lineaDeVenta.albaranSalida or None, doc = "Albarán de salida relacionado con la línea de ajuste a través de la línea de venta intermedia.")
    albaranSalidaID = property(lambda self: self.lineaDeVentaID and self.lineaDeVenta.albaranSalidaID or None, doc = "ID del albarán de salida relacionado con la línea de ajuste a través de la línea de venta intermedia.")
    precio = property(lambda self: self.diferencia, doc = "Diferencia y precio son lo mismo en las líneas de ajuste.")
    descuento = property(lambda self: 0.0, doc = "Las líneas de devolución no tienen descuento.")
    tarifa = property(get_tarifa, doc = "Tarifa de la línea de venta relacionada con la línea de ajuste.")
    productoVenta = property(lambda self: self.lineaDeVentaID and self.lineaDeVenta.productoVenta or None, doc = "Objeto producto de venta relacionado.")
    productoVentaID = property(lambda self: self.lineaDeVentaID and self.lineaDeVenta.productoVentaID or None, doc = "ID del producto de venta relacionado.")
    producto = productoVenta
    pedidoVenta = property(lambda self: self.lineaDeVentaID and self.lineaDeVenta.pedidoVenta or None, doc = "Objeto pedido de venta relacionado con la línea de devolución.")
    pedidoVentaID = property(lambda self: self.lineaDeVentaID and self.lineaDeVenta.pedidoVentaID or None, doc = "ID del pedido de venta relacionado con la línea de devolución.")
    facturaVenta = property(lambda self: self.abonoID and self.abono.facturaDeAbono or None, doc = "Factura DE ABONO relacionada con la línea de devolución. Para obtener las facturas de venta en sí, usar la relación LineaDeAbono-LineaDeVenta-FacturaVenta. El nombre viene por compatibilidad con las LDV.")
    facturaVentaID = property(lambda self: self.abonoID and self.abono.facturaDeAbonoID or None, doc = "Factura DE ABONO relacionada con la línea de devolución. Para obtener las facturas de venta en sí, usar la relación LineaDeAbono-LineaDeVenta-FacturaVenta. El nombre viene por compatibilidad con las LDV.")

    def calcular_subtotal(self, iva = False):
        res = self.cantidad * self.precio
        if iva:
            try:
                res *= (1 + self.abono.facturaDeAbono.iva)
            except AttributeError:  # ¿Sin factura?
                res *= (1 + self.abono.cliente.iva)
        return res

    def calcular_beneficio(self):
        """
        Devuelve el "beneficio" negativo originado por la devolución de la
        mercancía.
        """
        # Este sí que habría que reimplementarlo se heredase o no de una
        # clase padre común para LDD, LDV, LDA y demás fauna.
        return self.diferencia * self.cantidad

    def get_comercial(self):
        """
        Devuelve el comercial relacionado con la línea de abono tirando de la
        línea de venta o del servicio, y None si no lo tiene.
        """
        if self.servicio:
            return self.servicio.get_comercial()
        else:
            return self.lineaDeVenta.get_comercial()

    comercial = property(get_comercial)

    def get_proveedor(self):
        """
        Devuelve el proveedor relacionado con la LDD. Al proveedor se llega
        a través del producto devuelto.
        """
        proveedor = self.producto and self.producto.proveedor or None
        return proveedor

    proveedor = property(get_proveedor)


cont, tiempo = print_verbose(cont, total, tiempo)

class LineaDeDevolucion(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------------------------------- abonoID = ForeignKey('Abono')
    #--------------------------------------- articuloID = ForeignKey('Articulo')
    #--------- albaranDeEntradaDeAbonoID = ForeignKey('AlbaranDeEntradaDeAbono')
    #----------------------------- albaranSalidaID = ForeignKey('AlbaranSalida')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    # Algunas "properties" para hacerlas coherentes con las líneas de venta:
    def calcular_subtotal(self, iva = False):
        res = self.cantidad * self.precio
        if iva:
            try:
                res *= (1 + self.abono.facturaDeAbono.iva)
            except AttributeError:  # ¿Sin factura?
                res *= (1 + self.abono.cliente.iva)
        return res

    def get_cantidad(self):
        """
        Devuelve la cantidad en m² si es una línea de devolución de geotextiles
        o en kg si es de fibra.
        """
        res = 0
        a = self.articulo
        if a != None:
            if a.es_rollo() or a.es_rollo_defectuoso():
                res = a.superficie
            elif (a.es_bala() or a.es_bigbag() or a.es_rolloC()
                  or a.es_balaCable() or a.es_caja()):
                res = a.peso
            else:
                res = 0
                myprint("Artículo ID %d no es bala [cable], cemento, rollo, rolloC o rollo_defectuoso." % (a.id))
        return -res     # Devuelvo en negativo porque a todos los efectos
                        # una cantidad que no sale del almacén, sino
                        # que entra, se considera negativa para facilitar
                        # los cálculos de subtotales y demás.

    def get_preciounitario(self):
        """
        Devuelve el precio unitario del producto en la línea de devolución.
        Como el precio en sí es para el bulto completo, el precio por unidad
        es la división de éste entre la cantidad.
        Se devuelve en positivo siempre y cuando la cantidad o el precio sea
        una cantidad negativa, algo que está asegurado ya que el precio total
        siempre es en negativo al tratarse de una devolución de dinero de
        cara a la aplicación.
        """
        try:
            return -self.precio / self.cantidad
        except ZeroDivisionError:
            return 0.0

    def get_tarifa(self):
        """
        Devuelve la tarifa de la LDV relacionada con la LDD a través del abono.
        Para ello determina el producto de venta y precio que tienen en común.
        Devuelve None si ninguna LDV coincide.
        """
        res = None
        if self.albaranSalida:
            ldvs = [ldv for ldv in self.albaranSalida.lineasDeVenta \
                    if ldv.productoVenta == self.articulo.productoVenta and
                        abs(ldv.precio - self.get_preciounitario()) < 0.001]
                            # Me conformo con que el precio sea *casi* el mismo. Una fracción de céntimo es aceptable
                            # teniendo en cuenta los errores de redondeo en flotantes "i-e-cubo" después de tantas operaciones.
            if ldvs != []:
                res = ldvs[0].get_tarifa()  # Si hay más de una, todas tienen el mismo precio y por tanto misma tarifa.
        return res

    def get_pedido_venta(self):
        """
        Devuelve el pedido de venta relacionado con la LDD o None si no
        se pudo determinar.
        Para considerar que un pedido está relacionado con la LDD se buscan
        en el albarán al que corresponda las LDV con mismo producto *y precio*.
        Si se encuentran varias, devuelve la primera que tenga un pedido de
        venta relacionado.
        """
        res = None
        if self.albaranSalida:
            ldvs = [ldv for ldv in self.albaranSalida.lineasDeVenta \
                    if ldv.productoVenta == self.articulo.productoVenta and ldv.precio == self.precio]
            for ldv in ldvs:
                if ldv.pedidoVenta != None:
                    res = ldv.pedidoVenta
                    break
        return res

    cantidad = property(get_cantidad, doc = get_cantidad.__doc__)
    descuento = property(lambda self: 0.0, doc = "Las líneas de devolución no tienen descuento.")
    tarifa = property(get_tarifa, doc = get_tarifa.__doc__)
    productoVenta = property(lambda self: self.articuloID and self.articulo.productoVenta or None, doc = "Objeto producto de venta relacionado.")
    productoVentaID = property(lambda self: self.articuloID and self.articulo.productoVentaID or None, doc = "ID del producto de venta relacionado.")
    producto = productoVenta
    pedidoVenta = property(get_pedido_venta, doc = get_pedido_venta.__doc__)
    pedidoVentaID = property(lambda self: self.get_pedido_venta() and self.get_pedido_venta().id or None, doc = "ID del pedido de venta relacionado con la línea de devolución.")
    facturaVenta = property(lambda self: self.abonoID and self.abono.facturaDeAbono or None, doc = "Factura DE ABONO relacionada con la línea de devolución. Para obtener las facturas de venta en sí, usar el atributo facturasVenta. El nombre viene por compatibilidad con las LDV.")
    facturaVentaID = property(lambda self: self.abonoID and self.abono.facturaDeAbonoID or None, doc = "Factura DE ABONO relacionada con la línea de devolución. Para obtener las facturas de venta en sí, usar el atributo facturasVenta. El nombre viene por compatibilidad con las LDV.")

    def calcular_beneficio(self):
        """
        Devuelve el "beneficio" negativo originado por la devolución de la
        mercancía.
        """
        # De momento es igualico igualico que el difunto de su agüelico.
        # Vamos, que está pidiendo una superclase Línea para LDD, LDV, LDA y
        # demás fauna.
        precio = self.precio
        cantidad = self.cantidad
        producto = self.producto
        tarifa = self.get_tarifa()
        if tarifa != None:
            porcentaje = tarifa.get_porcentaje(producto, fraccion = True)
        else:
            try:
                porcentaje = (precio / producto.precioDefecto) - 1.0
            except ZeroDivisionError:
                porcentaje = 1.0
        return producto.precioDefecto * porcentaje * cantidad

    def get_comercial(self):
        """
        Devuelve el comercial relacionado con la LDD. Al comercial se llega
        a través del pedido de venta que está relacionado con las LDVs del
        albarán de salida del que procede el artículo devuelto aquí.
        El problema es que se pierde "granularidad" en la relación muchos a
        muchos entre albaranes de salida y pedidos a través de las LDV. Si
        hubiera varios pedidos relacionados con el mismo albarán (cosa muy
        improbable, pero posible), aquí se devolvería de forma determinista el
        primero de ellos, sin ningún criterio en especial más que el orden
        inverso de IDs de las LDVs.
        """
        a = self.albaranSalida
        if a:
            ldvs = [ldv for ldv in a.lineasDeVenta]
            ldvs.sort(lambda l1, l2: int(l2.id) - int(l1.id))
            # No hay muchas, pero alguna LDV sin pedido sí que hay.
            # OJO: Que aunque haya otras LDVs con pedido y comercial en el
            # mismo albarán, como no sea la última añadida, paso y devuelvo
            # que no tiene comercial (None).
            comercial = ldvs[0].comercial
        else:   # No albarán. No comercial.
            comercial = None
        return comercial

    comercial = property(get_comercial)

    def get_proveedor(self):
        """
        Devuelve el proveedor relacionado con la LDD. Al proveedor se llega
        a través del producto devuelto.
        """
        proveedor = self.producto.proveedor
        return proveedor

    proveedor = property(get_proveedor)


    def get_almacen(self):
        """
        Devuelve el almacén relacionado con la línea de devolución, que será
        aquel al que se haya devuelto la mercancía.
        """
        return self.abono and self.abono.almacen or None

cont, tiempo = print_verbose(cont, total, tiempo)

class AlbaranDeEntradaDeAbono(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True

    lineasDeDevolucion = MultipleJoin('LineaDeDevolucion')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class PagoDeAbono(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------------- facturaDeAbonoID = ForeignKey('FacturaDeAbono')
    #------------------------------- facturaVentaID = ForeignKey('FacturaVenta')
    #------------------- prefacturaID = ForeignKey('Prefactura', default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_factura_o_prefactura(self):
        """
        Devuelve la factura relacionada, tanto si es facturaVenta
        como prefactura, o None si no tiene ninguna de ellas.
        Como no debería tener ambos valores distintos de nulo a
        la vez, tiene preferencia facturaVenta sobre prefactura.
        """
        return self.facturaVenta or self.prefactura

cont, tiempo = print_verbose(cont, total, tiempo)

class Usuario(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    permisos = MultipleJoin('Permiso')
    alertas = MultipleJoin('Alerta')
    estadisticas = MultipleJoin('Estadistica')
    listasObjetosRecientes = MultipleJoin("ListaObjetosRecientes")
    empleados = MultipleJoin("Empleado")
    auditorias = MultipleJoin("Auditoria")
    pedidosVenta = MultipleJoin("PedidoVenta")
    presupuestos = MultipleJoin("Presupuesto",
            joinColumn = "usuario_id")
    #credPresupuestos = MultipleJoin("Presupuestos",
    #        joinColumn = "cred_usuario_id")
    # TODO: XXX: FIXME: It does not work. And I don't know why.

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    @property
    def comerciales(self):
        """
        Devuelve lista de comerciales con los que opera el usuario.
        """
        res = []
        for e in self.empleados:
            res += e.comerciales
        return res

    def get_permiso(self, ventana):
        """
        Devuelve el registro permiso del usuario sobre
        la ventana "ventana" o None si no se encuentra.
        """
        if isinstance(ventana, str):
            try:
                ventana = Ventana.selectBy(fichero = ventana)[0]
            except IndexError:
                ventana = os.path.basename(ventana)
                if ventana.endswith(".pyc"):
                    ventana = ventana[:-1]
                try:
                    ventana = Ventana.selectBy(fichero = ventana)[0]
                except IndexError:
                    pass    # No existe o me han mandado otra cosa en el
                            # parámetro. Intento seguir...
        elif isinstance(ventana, int):
            ventana = Ventana.get(ventana)
        try:
            # return [p for p in self.permisos if p.ventana == ventana][0]
            query = """
                    SELECT id FROM permiso
                    WHERE ventana_id = %d AND usuario_id = %d;
                    """ % (ventana.id, self.id)
            ide = self.__class__._connection.queryOne(query)[0]
            permiso = Permiso.get(ide)
            return permiso
        except (IndexError, TypeError):
            return None

    def enviar_mensaje(self, texto, permitir_duplicado = False):
        """
        Envía un nuevo mensaje al usuario creando una
        alerta pendiente para el mismo.
        Si permitir_duplicado es False, se buscan los mensajes
        con el mismo texto que se intenta enviar. En caso de
        que exista, solo se actualizará la hora de la alerta
        y se pondrá el campo "entregado" a False.
        Si es True, se envía el nuevo mensaje aunque pudiera
        estar duplicado.
        """
        mensajes = Alerta.select(AND(Alerta.q.mensaje == texto,
                                     Alerta.q.usuarioID == self.id))
        if not permitir_duplicado:
            for m in mensajes:
                #m.destroy()
                m.destroySelf()     # No quiero guardar traza de esto. Son
                        # demasiados registros que voy a acabar ignorando.
        a = Alerta(usuario = self, mensaje = texto, entregado = False)  # @UnusedVariable

    def cambiar_password(self, nueva):
        """
        Cambia la contraseña por la nueva recibida.
        """
        import md5
        self.passwd = md5.new(nueva).hexdigest()
        self.syncUpdate()

    def get_comerciales(self):
        """
        Devuelve una lista de objetos comerciales relacionados con el
        usuario a través del registro empleados.
        """
        res = []
        for e in self.empleados:
            for c in e.comerciales:
                if c not in res:
                    res.append(c)
        return res

# Instanciación diferida de usuario según parámetros
if usu:
    try:
        logged_user = Usuario.selectBy(usuario = usu)[0]
    except IndexError:
        pass

cont, tiempo = print_verbose(cont, total, tiempo)

class Modulo(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    ventanas = MultipleJoin('Ventana')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class Ventana(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #------------------------------------------- moduloID = ForeignKey('Modulo')
    permisos = MultipleJoin('Permiso')
    estadisticas = MultipleJoin('Estadistica')
    listasObjetosRecientes = MultipleJoin("ListaObjetosRecientes")
    auditorias = MultipleJoin("Auditoria")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class Permiso(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- usuarioID = ForeignKey('Usuario')
    #----------------------------------------- ventanaID = ForeignKey('Ventana')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class Alerta(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- usuarioID = ForeignKey('Usuario')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class DatosDeLaEmpresa(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_ruta_completa_logo(self, logo = None):
        """
        Devuelve la ruta completa al logotipo de datos de la empresa.
        Si no tiene logo, devuelve None.
        Si logo es distinto a None (un nombre de fichero), devuelve la ruta
        para ese logo según la estructura de directorios de la aplicación.
        """
        if not logo:
            im = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                              "..", "..", "imagenes", self.logo)
        else:
            im = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                              "..", "..", "imagenes", logo)
        return os.path.abspath(im)

    @classmethod
    def get_propia_empresa_como_cliente(cls):
        """
        Devuelve el registro cliente de la BD que se corresponde
        con la empresa atendiendo a los datos del registro DatosDeLaEmpresa
        o None si no se encuentra.
        """
        nombre_propia_empresa = cls.select()[0].nombre
        clientes = Cliente.select(Cliente.q.nombre == nombre_propia_empresa)
        if clientes.count() == 0:
            cliente = None
        elif clientes.count() == 1:
            cliente = clientes[0]
        else:   # >= 2
            myprint("pclases.py: DatosDeLaEmpresa::get_propia_empresa_como_cliente: Más de un posible cliente encontrado. Selecciono el primero.")
            cliente = clientes[0]
        return cliente

    @classmethod
    def get_propia_empresa_como_proveedor(cls):
        """
        Devuelve el registro proveedor que se corresponde con la
        empresa atendiendo a los datos del registro DatosDeLaEmpresa
        o None si no se encuentra.
        """
        nombre_propia_empresa = cls.select()[0].nombre
        proveedores = Proveedor.select(Proveedor.q.nombre == nombre_propia_empresa)
        if proveedores.count() == 0:
            proveedor = None
        elif proveedores.count() == 1:
            proveedor = proveedores[0]
        else:   # >= 2
            myprint("pclases.py: DatosDeLaEmpresa::get_propia_empresa_como_proveedor: Más de un posible proveedor encontrado. Selecciono el primero.")
            proveedor = proveedores[0]
        return proveedor

    get_cliente = get_propia_empresa_como_cliente
    get_proveedor = get_propia_empresa_como_proveedor

    def str_cif_o_nif(self):
        """
        Devuelve la cadena "N.I.F." o "C.I.F." dependiendo de si el atributo
        «cif» de la empresa es un N.I.F. (aplicable a personas) o C.I.F.
        (aplicable a empresas).
        """
        try:
            return self.cif[0].isalpha() and "C.I.F." or "N.I.F."
        except IndexError:
            return ""

    def get_dir_facturacion_completa(self):
        res = ""
        if self.dirfacturacion:
            res = self.dirfacturacion
        if self.cpfacturacion:
            res += "; %s" % self.cpfacturacion
        if self.ciudadfacturacion and self.provinciafacturacion:
            if self.ciudadfacturacion == self.provinciafacturacion:
                res += " - %s" % self.provinciafacturacion
            else:
                res += " - %s (%s)" % (self.ciudadfacturacion,
                                       self.provinciafacturacion)
        elif self.ciudadfacturacion:
            res += " - %s" % self.ciudadfacturacion
        elif self.provinciafacturacion:
            res += " - %s" % self.provinciafacturacion
        elif self.paisfacturacion:
            res += ". %s" % self.paisfacturacion
        return res

    def get_dir_correspondencia_completa(self):
        res = ""
        if self.direccion:
            res = self.direccion
        if self.cp:
            res += "; %s" % self.cp
        if self.ciudad and self.provincia:
            if self.ciudad == self.provincia:
                res += " - %s" % self.provincia
            else:
                res += " - %s (%s)" % (self.ciudad,
                                       self.provincia)
        elif self.ciudad:
            res += " - %s" % self.ciudad
        elif self.provincia:
            res += " - %s" % self.provincia
        elif self.pais:
            res += ". %s" % self.pais
        return res

    def get_dia_de_pago(self):
        """
        Devuelve el día que deben llevar los pagos por defecto (pagarés, etc.)
        """
        # OJO: HARDCODED hasta que encuentre dónde meterlo para que sea
        # configurable. Como no se ha cambiado en 10 años, lo que se dice
        # prisa, no hay.
        dia_de_pago = 25    # FIXME
        return dia_de_pago

    @staticmethod
    def calcular_dia_de_pago(fecha_base = None):
        """
        Devuelve una fecha del tipo datetime con el día exacto en que se debe
        hacer un pago basándose en la fecha base especificada o en el día de
        hoy si no se instancia el parámetro.
        NOTAS: Si la fecha_base es un mx, devolverá un mx.DateTime
        """
        # CWT: Fecha por defecto los 25 si no es domingo.
        if not fecha_base:
            fecha_defecto = mx.DateTime.localtime()
        else:
            fecha_defecto = fecha_base
        while fecha_defecto.day != 25:
            # fecha_defecto += mx.DateTime.oneDay
            fecha_defecto += datetime.timedelta(1)
        try:
            diasemana = fecha_defecto.day_of_week
        except AttributeError:  # No es un mx. Es un datetime.
            diasemana = fecha_defecto.weekday()
        if diasemana == 6:
            #fecha_defecto += mx.DateTime.oneDay
            fecha_defecto += datetime.timedelta(1)
        return fecha_defecto

cont, tiempo = print_verbose(cont, total, tiempo)

class LogicMovimientos(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    pagos = MultipleJoin('Pago')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_codigo(self):
        """
        Devuelve un código único formado a partir del número de cuenta,
        asiento y orden.
        """
        return "%s-%s-%s" % (self.codigoCuenta.strip(), self.asiento, self.orden)

cont, tiempo = print_verbose(cont, total, tiempo)

class ParteDeTrabajo(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True

    #--------------------------------------- empleadoID = ForeignKey('Empleado')
    #----------------------------- centroTrabajoID = ForeignKey('CentroTrabajo')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_duracion(self):
        try:
            duracion = self.horafin - self.horainicio
        except TypeError:   # Vienen como datetime.date y no soportan la resta.
            duracion = (utils.DateTime2DateTimeDelta(self.horafin)
                        - utils.DateTime2DateTimeDelta(self.horainicio))
        return duracion

    horas = property(get_duracion)

    def es_nocturno(self):
        """
        Devuelve True si el parte pertenece al turno de noche.
        """
        turnosnoche = Turno.select(Turno.q.noche == True)
        res = False
        for turno in turnosnoche:
            # Con que el parte empiece en algún turno de noche (suponiendo que haya varios), ya se considera nocturno.
            if turno.horainicio > turno.horafin:
                esta_en_turno = utils.DateTime2DateTimeDelta(self.horainicio) >= \
                                    utils.DateTime2DateTimeDelta(turno.horainicio) and \
                                utils.DateTime2DateTimeDelta(self.horainicio) <= \
                                    (utils.DateTime2DateTimeDelta(turno.horafin) + mx.DateTime.oneDay)
            else:
                esta_en_turno = utils.DateTime2DateTimeDelta(self.horainicio) >= \
                                    utils.DateTime2DateTimeDelta(turno.horainicio) and \
                                utils.DateTime2DateTimeDelta(self.horainicio) <= \
                                    utils.DateTime2DateTimeDelta(turno.horafin)
            res = res or esta_en_turno
        return res

    def get_fecha(self):
        """
        Devuelve la fecha del parte de trabajo (horainicio en realidad).
        """
        return self.horainicio
    fecha = property(get_fecha)

cont, tiempo = print_verbose(cont, total, tiempo)

class CategoriaLaboral(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------- lineaDeProduccionID = ForeignKey('LineaDeProduccion')
    empleados = MultipleJoin('Empleado')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self, *args, **kw):
        return "%s (%s)" % (self.puesto, self.codigo)

cont, tiempo = print_verbose(cont, total, tiempo)

class Motivo(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    ausencias = MultipleJoin('Ausencia')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class ObservacionesNominas(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class Ausencia(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #------------------------------------------- motivoID = ForeignKey('Motivo')
    #--------------------------------------- empleadoID = ForeignKey('Empleado')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class Baja(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------------------------- empleadoID = ForeignKey('Empleado')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def esta_vigente(self, fecha = mx.DateTime.localtime()):
        """
        Devuelve True si la baja era efectiva en la fecha recibida.
        """
        if self.fechaFin:
            res = self.fechaInicio <= fecha < self.fechaFin
        else:
            res = self.fechaInicio <= fecha
        return res

cont, tiempo = print_verbose(cont, total, tiempo)

class CalendarioLaboral(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------- lineaDeProduccionID = ForeignKey('LineaDeProduccion')
    laborables = MultipleJoin('Laborable')
    vacaciones = MultipleJoin('Vacaciones')
    festivos = MultipleJoin('Festivo')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_mes(self):
        return self.mesAnno.month

    def get_anno(self):
        return self.mesAnno.year

    def set_mes(self, mes):
        self.mesAnno = mx.DateTime.DateTimeFrom(day = self.mesAnno.day, month = mes, year = self.mesAnno.year)

    def set_anno(self, anno):
        self.mesAnno = mx.DateTime.DateTimeFrom(day = self.mesAnno.day, month = self.mesAnno.month, year = anno)

    mes = property(get_mes, set_mes, doc = "Mes")
    anno = property(get_anno, set_anno, doc = "Año")

cont, tiempo = print_verbose(cont, total, tiempo)

class Festivo(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------- calendarioLaboralID = ForeignKey('CalendarioLaboral')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class FestivoGenerico(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class Vacaciones(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------- calendarioLaboralID = ForeignKey('CalendarioLaboral')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class Turno(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    laborables = MultipleJoin('Laborable')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class Grupo(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #-------------------------------------- jefeturnoID = ForeignKey('Empleado')
    #-------------------------------------- operario1ID = ForeignKey('Empleado')
    # operario2ID = ForeignKey('Empleado')    # Máximo 3 por grupo. Restricción de requisitos del cliente.
    laborables = MultipleJoin('Laborable')
    controlesHoras = MultipleJoin('ControlHoras')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class Laborable(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------------------------------- turnoID = ForeignKey('Turno')
    #--------------------------------------------- grupoID = ForeignKey('Grupo')
    #--------------------- calendarioLaboralID = ForeignKey('CalendarioLaboral')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_empleados(self):
        """
        Devuelve los empleados del grupo para el día laborable
        como lista de objetos "empleado".
        Filtra previamente para ignorar aquellos que tengan una
        baja en el día de la fecha del laborable.
        Para obtener el rol de cada uno, usar el método
        get_grupo_and_rol del empleado.
        Si se obtienen los empleados directamente del grupo,
        las ausencias se ignoran, HAY QUE CHEQUEARLAS APARTE.
        """
        empleados = []
        if self.fecha not in [a.fecha for a in self.grupo.jefeturno.ausencias]:
            empleados.append(self.grupo.jefeturno)
        if self.fecha not in [a.fecha for a in self.grupo.operario1.ausencias]:
            empleados.append(self.grupo.operario1)
        if self.fecha not in [a.fecha for a in self.grupo.operario2.ausencias]:
            empleados.append(self.grupo.operario2)
        return tuple(empleados)

    empleados = property(get_empleados, doc = "Devuelve los empleados del grupo disponibles (es decir, sin ausencia programada) para el día y turno del laborable en cuestión (self).")

cont, tiempo = print_verbose(cont, total, tiempo)

class TransporteACuenta(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    serviciosTomados = MultipleJoin('ServicioTomado')
    #------------- albaranSalidaID = ForeignKey('AlbaranSalida', default = None)
    #--------------------- proveedorID = ForeignKey('Proveedor', default = None)

    def _init(self, *args, **kw):
        """
        Además de constructor, comprueba la consistencia con
        las facturas de compra. Si existe un registro (o varios)
        de servicioTomado relacionado con el transporte, éste
        debe tener facturaCompra != None; en otro caso, se elimina.
        """
        starter(self, *args, **kw)
        self.__comprobar_si_facturado()

    def __comprobar_si_facturado(self):
        """
        Comprueba que si el transporte no está facturado, no tenga
        registros "serviciosTomados". En caso de que los tenga sin
        factura, los elimina.
        """
        for servicio in self.serviciosTomados:
            if servicio.facturaCompraID == None:
                servicio.destroy()

    def facturar(self, facturaCompra):
        """
        Factura la transporte en la factura de compra recibida, creando
        el registro intermedio servicioTomado.
        Si "facturaCompra" es None, elimina la relación entre la factura
        y la transporte.
        Devuelve el servicio recién creado o None si se eliminó.
        PRECONDICIÓN: "facturaCompra" debe ser un objeto de la clase
                      FacturaCompra válido o None.
        """
        if facturaCompra != None:
            servicio = ServicioTomado(comision = None,
                                      transporteACuenta = self,
                                      facturaCompra = facturaCompra,
                                      concepto = self.concepto,
                                      precio = self.precio,
                                      cantidad = 1,
                                      descuento = 0,
                                      fechahoraFacturado =
                                        datetime.datetime.today())
        else:
            for servicio in self.serviciosTomados:
                servicio.destroy()
            servicio = None
        return servicio

cont, tiempo = print_verbose(cont, total, tiempo)

class Comision(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- clienteID = ForeignKey('Cliente')
    #--------------- facturaVentaID = ForeignKey('FacturaVenta', default = None)
    #------------------- prefacturaID = ForeignKey('Prefactura', default = None)
    serviciosTomados = MultipleJoin('ServicioTomado')
    #------------- albaranSalidaID = ForeignKey('AlbaranSalida', default = None)

    def _init(self, *args, **kw):
        """
        Pseudo-constructor. Se llama únicamente al crear el objeto en
        memoria. No vuelve a ejecutarse al recuperar un registro de
        caché, por ejemplo.
        De los comentarios de SQLObject (main.py):
            # This function gets called only when the object is
            # created, unlike __init__ which would be called
            # anytime the object was returned from cache.
        Para el caso concreto de las comisiones, además de
        las tareas rutinarias del constructor, comprueba la
        coherencia comisión-serviciosTomados-facturaCompra, donde
        serviciosTomados != [] sii para cada uno de ellos
        facturaCompra != None.
        """
        starter(self, *args, **kw)
        self.__comprobar_si_facturado()

    def get_factura_o_prefactura(self):
        """
        Devuelve la factura relacionada, tanto si es facturaVenta
        como prefactura, o None si no tiene ninguna de ellas.
        Como no debería tener ambos valores distintos de nulo a
        la vez, tiene preferencia facturaVenta sobre prefactura.
        """
        return self.facturaVenta or self.prefactura

    def __comprobar_si_facturado(self):
        """
        Comprueba que si la comisión no está facturada, no tenga
        registros "serviciosTomados". En caso de que los tenga sin
        factura, los elimina.
        """
        for servicio in self.serviciosTomados:
            if servicio.facturaCompraID == None:
                servicio.destroy()

    def facturar(self, facturaCompra):
        """
        Factura la comisión en la factura de compra recibida, creando
        el registro intermedio servicioTomado.
        Si "facturaCompra" es None, elimina la relación entre la factura
        y la comisión.
        Devuelve el servicio recién creado o None si se eliminó.
        PRECONDICIÓN: "facturaCompra" debe ser un objeto de la clase
                      FacturaCompra válido o None.
        """
        if facturaCompra != None:
            servicio = ServicioTomado(comision = self,
                                      transporteACuenta = None,
                                      facturaCompra = facturaCompra,
                                      concepto = self.concepto,
                                      precio = self.precio,
                                      cantidad = 1,
                                      descuento = 0,
                                      fechahoraFacturado =
                                        datetime.datetime.today())
        else:
            for servicio in self.serviciosTomados:
                servicio.destroy()
            servicio = None
        return servicio

cont, tiempo = print_verbose(cont, total, tiempo)

class ServicioTomado(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------- facturaCompraID = ForeignKey('FacturaCompra')
    #----------------------- comisionID = ForeignKey('Comision', default = None)
    #----- transporteACuentaID = ForeignKey('TransporteACuenta', default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        """
        Devuelve cadena con cantidad, descripción y subtotal del servicio (IVA
        no incluido).
        """
        precio_con_descuento = utils.float2str(
            self.precio * (1.0 - self.descuento))
        if self.descuento:
            precio_con_descuento += " (%s%% dto. incl.)" % (
                utils.float2str(self.descuento * 100))
        total_srv = self.get_subtotal(iva = True, prorrateado = True)
        res = "%s %s * %s = %s" % (
            utils.float2str(self.cantidad),
            self.concepto,
            precio_con_descuento,
            utils.float2str(total_srv))
        return res

    def get_subtotal(self, iva = False, descuento = True, prorrateado = False):
        """
        Devuelve el subtotal con o sin IVA (según se indique) de
        la línea de compra: precio * cantidad - descuento.
        Si «prorrateado» es True, devuelve el importe entre el número de
        vencimientos.
        """
        res = self.cantidad * self.precio
        if descuento:
            res *= (1 - self.descuento)
        if iva:
            res *= 1 + self.iva
        # Ahora el servicio tiene su propio IVA.
        #if iva and self.facturaCompraID:
        #    res *= (1 + self.facturaCompra.iva)
        if prorrateado:
            try:
                numvtos = max(1, len(self.proveedor.get_vencimientos()))
            except (AttributeError, TypeError, ValueError):
                numvtos = 1
            res /= numvtos
        return res

    def _get_qconcepto(self):
        """
        Si el registro tiene una comisión relacionada, devuelve el
        concepto de la comisión.
        Si tiene un transporte a cuenta, devuelve el del transporte
        a cuenta.
        En otro caso, devuelve el concepto del registro.
        """
        if self.comision != None:
            return self.comision.concepto
        if self.transporteACuenta != None:
            return self.transporteACuenta.concepto
        return self.concepto

    def _set_qconcepto(self, txt):
        """
        Si el registro tiene una comisión relacionada, guarda en su
        concepto y en del mismo registro el texto recibido.
        Lo mismo con el transporte a cuenta.
        """
        self.concepto = txt
        if self.comision != None:
            self.comision.concepto = self.concepto
        if self.transporteACuenta != None:
            self.transporteACuenta.concepto = self.concepto

    def _get_qcantidad(self):
        """
        Si el registro tiene una comisión relacionada, devuelve el
        cantidad de la comisión.
        Si tiene un transporte a cuenta, devuelve el del transporte
        a cuenta.
        En otro caso, devuelve el cantidad del registro.
        """
        if self.comision != None or self.transporteACuenta != None:
            return 1    # Los transportes a cuenta y comisiones no tienen cantidad.
        return self.cantidad

    def _set_qcantidad(self, txt):
        """
        Como transportes y comisiones no tienen cantidades, este método
        simplemente ignora la cantidad recibida si existe alguna
        de estas dos relaciones.
        """
        if not self.transporteACuenta and not self.comisionID:
            self.cantidad = txt     # Y si no es un valor válido, que SQLObject
                                    # se encargue de lanzar la excepción.

    def _get_qprecio(self):
        """
        Si el registro tiene una comisión relacionada, devuelve el
        precio de la comisión.
        Si tiene un transporte a cuenta, devuelve el del transporte
        a cuenta.
        En otro caso, devuelve el precio del registro.
        """
        self.sync()
        if self.comision != None:
            self.comision.sync()
            return self.comision.precio
        if self.transporteACuenta != None:
            self.transporteACuenta.sync()
            return self.transporteACuenta.precio
        return self.precio

    def _set_qprecio(self, txt):
        """
        Si el registro tiene una comisión relacionada, guarda en su
        precio y en del mismo registro el texto recibido.
        Lo mismo con el transporte a cuenta.
        """
        # Si el precio recibido en txt no es correcto, ya se encargará
        # SQLObject de disparar la excepción correspondiente.
        self.precio = txt
        self.syncUpdate()
        if self.comision != None:
            self.comision.precio = self.precio
            self.comision.syncUpdate()
        if self.transporteACuenta != None:
            self.transporteACuenta.precio = self.precio
            self.transporteACuenta.syncUpdate()

    def _get_qdescuento(self):
        """
        Si el registro tiene una comisión relacionada, devuelve el
        descuento de la comisión.
        Si tiene un transporte a cuenta, devuelve el del transporte
        a cuenta.
        En otro caso, devuelve el descuento del registro.
        """
        if self.comision != None or self.transporteACuenta != None:
            return 0 # Los transportes a cuenta y comisiones no tienen dto.
        return self.descuento

    def _set_qdescuento(self, txt):
        """
        Como transportes y comisiones no tienen descuentos, este método
        simplemente ignora la cantidad recibida si existe alguna
        de estas dos relaciones.
        """
        if not self.transporteACuenta and not self.comisionID:
            self.descuento = txt    # Y si no es un valor válido, que
                        # SQLObject se encargue de lanzar la excepción.

    qconcepto = property(_get_qconcepto, _set_qconcepto,
            doc = "Concepto del servicio, o del transporte o comisión "
                  "relacionada si lo tuviera.")
    qcantidad = property(_get_qcantidad, _set_qcantidad,
            doc = "Cantidad del servicio, o del transporte o comisión "
                  "relacionada si lo tuviera.")
    qprecio = property(_get_qprecio, _set_qprecio,
            doc = "Precio del servicio, o del transporte o comisión "
                  "relacionada si lo tuviera.")
    qdescuento = property(_get_qdescuento, _set_qdescuento,
            doc = "Descuento del servicio, o del transporte o comisión "
                  "relacionada si lo tuviera.")

cont, tiempo = print_verbose(cont, total, tiempo)

class CamposEspecificosEspecial(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    productosVenta = MultipleJoin('ProductoVenta')
    stocksEspecial = MultipleJoin("StockEspecial")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class HistorialExistenciasCompra(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------------- productoCompraID = ForeignKey('ProductoCompra')
    #----------------------------------------- almacenID = ForeignKey("Almacen")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class Recibo(SQLObject, PRPCTOO):
    """
    Recibos bancarios para cobros a clientes.
    Incluye un vencimiento que en observaciones (lo que se muestra como
    "forma de pago" en las facturas) llevará "Recibo bancario nº %d" % (self.numrecibo).
    """
    class sqlmeta:
        fromDatabase = True

    #--------------- cuentaOrigenID = ForeignKey('CuentaOrigen', default = None)
    vencimientosCobro = MultipleJoin('VencimientoCobro')
    # cuentaBancariaClienteID = ForeignKey('CuentaBancariaCliente', default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_next_numrecibo(cls, anno):
        """
        Devuelve el siguiente número de recibo disponible para
        el ano «anno».
        """
        try:
            ultimo_recibo = cls.select(cls.q.anno == anno, orderBy = "-numrecibo")[0]
        except IndexError:
            return 1
        else:
            return ultimo_recibo.numrecibo + 1

    get_next_numrecibo = classmethod(get_next_numrecibo)

    def calcular_importe(self):
        """
        Devuelve un float con la suma de los vencimientos relacionados.
        """
        return sum([v.importe for v in self.vencimientosCobro])

    importe = property(calcular_importe, doc = calcular_importe.__doc__)

    def get_cliente(self):
        """
        Devuelve el cliente del recibo (cliente del primer
        vencimiento relacionado. Todos deberían permanecer
        al mismo).
        """
        cliente = None
        if self.vencimientosCobro:
            fra = self.vencimientosCobro[0].facturaVenta or self.vencimientosCobro[0].prefactura
            cliente = fra.cliente
        return cliente

    def get_facturas(self):
        """
        Devuelve una lista de facturas relacionadas con el
        recibo a través de los vencimientos de cobro.
        """
        return [v.facturaVenta or v.prefactura for v in self.vencimientosCobro]

cont, tiempo = print_verbose(cont, total, tiempo)

class CuentaBancariaCliente(SQLObject, PRPCTOO):
    """
    Cuenta Bancaria de un cliente.
    """
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- clienteID = ForeignKey('Cliente')
    recibos = MultipleJoin("Recibo")
    efectos = MultipleJoin("Efecto")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class Documento(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------- pedidoVentaID = ForeignKey('PedidoVenta', default = None)
    #------------- albaranSalidaID = ForeignKey('AlbaranSalida', default = None)
    #--------------- facturaVentaID = ForeignKey('FacturaVenta', default = None)
    #------------------- prefacturaID = ForeignKey('Prefactura', default = None)
    #----------------- pagareCobroID = ForeignKey('PagareCobro', default = None)
    #--------------- pedidoCompraID = ForeignKey('PedidoCompra', default = None)
    #----------- albaranEntradaID = ForeignKey('AlbaranEntrada', default = None)
    #------------- facturaCompraID = ForeignKey('FacturaCompra', default = None)
    #------------------- pagarePagoID = ForeignKey('PagarePago', default = None)
    #----------------------- empleadoID = ForeignKey('Empleado', default = None)
    #------------------------- clienteID = ForeignKey('Cliente', default = None)
    #--------------------- proveedorID = ForeignKey('Proveedor', default = None)
    #------------------- confirmingID = ForeignKey('Confirming', default = None)

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    @staticmethod
    def get_ruta_base():
        """
        Devuelve la ruta del directorio que contiene los documentos adjuntos.
        Se asegura cada vez que es consultada que el directorio existe.
        """
        # Siempre se trabaja en un subdirectorio del raíz del programa.
        # Normalmente formularios o framework.
        # Por tanto lo primero que hago es salir del subdirectorio para buscar
        # el de documentos adjuntos.
        RUTA_BASE = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                          "..", "..", config.get_dir_adjuntos())
        try:
            assert os.path.exists(RUTA_BASE)
        except AssertionError:
            os.mkdir(RUTA_BASE)
        return RUTA_BASE

    ruta_base = get_ruta_base

    def get_ruta_completa(self):
        """
        Devuelve la ruta completa al fichero: directorio base + nombre del fichero.
        """
        return os.path.join(Documento.get_ruta_base(), self.nombreFichero)

    def copiar_a(self, ruta):
        """
        Copia el fichero del objeto a la ruta seleccionada.
        """
        import shutil
        try:
            shutil.copy(self.get_ruta_completa(), ruta)
            res = True
        except Exception, msg:
            myprint("pclases::Documento::copiar_a -> Excepción %s" % msg)
            res = False
        return res

    def copiar_a_diradjuntos(ruta):
        """
        Copia el fichero de la ruta al directorio de adjuntos.
        """
        import shutil
        try:
            shutil.copy(ruta, Documento.get_ruta_base())
            res = True
        except Exception, msg:
            myprint("pclases::Documento::copiar_a_diradjuntos -> Excepción %s" % msg)
            res = False
        return res

    copiar_a_diradjuntos = staticmethod(copiar_a_diradjuntos)

    def adjuntar(ruta, objeto, nombre = ""):
        """
        Adjunta el fichero del que recibe la ruta con el objeto
        del segundo parámetro.
        Si no puede determinar la clase del objeto o no está
        soportado en la relación, no crea el registro documento
        y devuelve None.
        En otro caso devuelve el objeto Documento recién creado.
        """
        res = None
        if objeto != None and os.path.exists(ruta):
            pedidoVenta = albaranSalida = facturaVenta = prefactura = \
            pedidoCompra = albaranEntrada = facturaCompra = \
            cliente = proveedor = empleado = \
            pagarePago = pagareCobro = None
            if isinstance(objeto, PedidoVenta):
                pedidoVenta = objeto
            elif isinstance(objeto, AlbaranSalida):
                albaranSalida = objeto
            elif isinstance(objeto, FacturaVenta):
                facturaVenta = objeto
            elif isinstance(objeto, Prefactura):
                prefactura = objeto
            elif isinstance(objeto, PedidoCompra):
                pedidoCompra = objeto
            elif isinstance(objeto, AlbaranEntrada):
                albaranEntrada = objeto
            elif isinstance(objeto, FacturaCompra):
                facturaCompra = objeto
            elif isinstance(objeto, Empleado):
                empleado = objeto
            elif isinstance(objeto, Cliente):
                cliente = objeto
            elif isinstance(objeto, Proveedor):
                proveedor = objeto
            elif isinstance(objeto, PagareCobro):
                pagareCobro = objeto
            elif isinstance(objeto, PagarePago):
                pagarePago = objeto
            else:
                raise TypeError, "pclases::Documento::adjuntar -> %s no es un tipo válido." % type(objeto)
            nombreFichero = os.path.split(ruta)[-1]
            if Documento.copiar_a_diradjuntos(ruta):
                nuevoDoc = Documento(nombre = nombre,
                                     nombreFichero = nombreFichero,
                                     pedidoVenta = pedidoVenta,
                                     albaranSalida = albaranSalida,
                                     facturaVenta = facturaVenta,
                                     prefactura = prefactura,
                                     pedidoCompra = pedidoCompra,
                                     albaranEntrada = albaranEntrada,
                                     facturaCompra = facturaCompra,
                                     cliente = cliente,
                                     proveedor = proveedor,
                                     empleado = empleado,
                                     pagareCobro = pagareCobro,
                                     pagarePago = pagarePago)
                res = nuevoDoc
        return res

    adjuntar = staticmethod(adjuntar)

cont, tiempo = print_verbose(cont, total, tiempo)

class Estadistica(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- usuarioID = ForeignKey('Usuario')
    #----------------------------------------- ventanaID = ForeignKey('Ventana')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def incrementar(usuario, ventana):
        if isinstance(usuario, int):
            usuario_id = usuario
        else:
            usuario_id = usuario.id
        if isinstance(ventana, int):
            ventana_id = ventana
        elif isinstance(ventana, str):
            try:
                ventana = Ventana.selectBy(fichero = ventana)[0]
                ventana_id = ventana.id
            except Exception, msg:
                myprint("pclases::Estadistica::incrementar -> Ventana '%s' no encontrada. Excepción: %s" % (ventana, msg))
                return
        else:
            ventana_id = ventana.id
        st = Estadistica.select(AND(Estadistica.q.usuarioID == usuario_id, Estadistica.q.ventanaID == ventana_id))
        if not st.count():
            st = Estadistica(usuarioID = usuario_id,
                             ventanaID = ventana_id)
        else:
            if st.count() > 1:
                sts = list(st)
                st = sts[0]
                for s in sts[1:]:
                    st.veces += s.veces
                    s.destroySelf()
            st = st[0]
        # Esto peta con algunas versiones de SQLObject y MX en WinXP
        #st.ultimaVez = mx.DateTime.localtime()
        st.ultimaVez = datetime.date.today()
        st.veces += 1
        st.sync()

    incrementar = staticmethod(incrementar)

cont, tiempo = print_verbose(cont, total, tiempo)

class ControlHoras(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------------------------------- grupoID = ForeignKey('Grupo')
    #--------------------------------------- empleadoID = ForeignKey('Empleado')
    controlesHorasProduccion = MultipleJoin('ControlHorasProduccion')
    controlesHorasMantenimiento = MultipleJoin('ControlHorasMantenimiento')

    RESTOCENTROS = ("Almacén", "Varios")    # HARCODED
    # Se les puede cambiar el nombre, pero el orden siempre debe ser el
    # centro de trabajo correspondiente a la actividad «almacén» y el de la
    # actividad «varios».

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def calcular_total_horas_extras_dia(self):
        return (self.horasExtraDiaProduccion +
                self.horasExtraDiaMantenimiento +
                self.horasExtraDiaAlmacen +
                self.horasExtraDiaVarios)

    def calcular_total_horas_extras_noche(self):
        return (self.horasExtraNocheProduccion +
                self.horasExtraNocheMantenimiento +
                self.horasExtraNocheAlmacen +
                self.horasExtraNocheVarios)

    def calcular_total_horas_extras(self):
        """
        Devuelve un flotante con la suma de todos los tipos de horas extras.
        """
        res = (self.calcular_total_horas_extras_dia() +
               self.calcular_total_horas_extras_noche())
        return res

    def calcular_total_horas_produccion(self):
        """
        Total de horas de producción en todas las líneas.
        """
        return sum([hp.horasProduccion
                    for hp in self.controlesHorasProduccion])

    def calcular_total_horas_mantenimiento(self):
        """
        Total de horas de mantenimiento en todas las líneas.
        """
        return sum([hp.horasMantenimiento
                    for hp in self.controlesHorasMantenimiento])

    def calcular_total_horas(self):
        """
        Devuelve el total de horas del registro, es decir, horas regulares
        más horas extras. De lo que sean cada una, da igual. Simplemente el
        total de horas.
        """
        return self.horasRegulares + self.calcular_total_horas_extras()

    def es_nulo(self):
        """
        Devuelve True si el registro está "vacío": no tiene horas anotadas
        de ningún tipo, no es festivo, no está bloqueado, no tiene baja a True
        y los comentarios y varios están al valor por defecto ''.
        """
        horas = (self.calcular_total_horas_extras() +
                 self.calcular_total_horas_produccion() +
                 self.calcular_total_horas_mantenimiento() +
                 self.horasRegulares + self.horasVarios + self.horasAlmacen)
        res = (horas == 0 and not self.festivo and not self.bajaLaboral
               and not self.vacacionesYAsuntosPropios and not self.bloqueado
               and not self.comentarios and not self.varios)
        return res

    def get_por_tipo(self):
        """
        Devuelve un diccionario con las horas por tipo (regulares o extras).
        """
        res = {"regulares": self.horasRegulares,
               "extras": self.calcular_total_horas_extras()
               }
        return res

    def get_por_hora(self):
        """
        Devuelve un diccionario con las horas según la hora del día (día o
        noche).
        """
        dia = noche = 0
        if self.nocturnidad:
            noche += self.horasRegulares
        else:
            dia += self.horasRegulares
        noche += self.calcular_total_horas_extras_noche()
        dia += self.calcular_total_horas_extras_dia()
        res = {"día": dia,
               "noche": noche}
        return res

    def get_por_actividad(self):
        """
        Devuelve un diccionario con las horas separas por actividad:
        "producción", "mantenimiento", "almacén" y "varios".
        """
        res = {"producción": self.calcular_total_horas_produccion(),
               "mantenimiento": self.calcular_total_horas_mantenimiento(),
               "almacén": self.horasAlmacen,
               "varios": self.horasVarios}
        return res

    def get_por_centro_de_trabajo(self, linea_as_str = True):
        """
        Devuelve un diccionario con las horas clasificadas según el centro
        de trabajo:
        lineaDeProduccion.nombre, "Almacén", self.varios si
        self.horasVarios > 0.
        FIXME: OJO: Con el paso de los cambios constantes de requisitos,
        organización de la producción y demás, se han acabado creando dos
        entidades independientes pero muy relacionadas y prácticamente
        equivalentes: centro de trabajo y lineaDeProducción.
        En teoría aquí debería usarse el CentroTrabajo, pero desgraciadamente
        esa clase casi ha quedado obsoleta sin apenas haberse utilizado. Así
        que hasta que se pueda solucionar, siempre que sea posible, todos los
        cálculos de horas por lugar donde se ha trabajado se centrarán en
        las líneas de producción y los conceptos HARCODED "Almacén" y
        "Varios" + concepto introducido por el usuario.
        Si linea_as_str es True devuelve los nombres de las líneas de
        producción. Si es False devuelve los objetos lineaDeProduccion como
        claves del diccionario en lugar de la cadena de texto.
        """
        res = {}
        for hm in self.controlesHorasMantenimiento:
            if hm.horasMantenimiento > 0:
                if linea_as_str:
                    linea = hm.lineaDeProduccion.nombre
                else:
                    linea = hm.lineaDeProduccion
                try:
                    res[linea] += hm.horasMantenimiento
                except KeyError:
                    res[linea] = hm.horasMantenimiento
        for hp in self.controlesHorasProduccion:
            if hp.horasProduccion > 0:
                if linea_as_str:
                    linea = hp.lineaDeProduccion.nombre
                else:
                    linea = hp.lineaDeProduccion
                try:
                    res[linea] += hp.horasProduccion
                except KeyError:
                    res[linea] = hp.horasProduccion
        if self.horasAlmacen > 0:
            res[self.RESTOCENTROS[0]] = self.horasAlmacen
        if self.horasVarios > 0:
            concepto_varios = (self.RESTOCENTROS[1] + ": "
                               + self.varios.strip().title())
            res[concepto_varios] = self.horasVarios
        return res

    def get_por_centro_de_trabajo_y_tipo(self):
        """
        Devuelve las horas divididas por centro de trabajo y dentro de
        cada uno por:
        - horas regulares de producción (no extras y no mantenimiento, incluye
          día y noche; incluye las de almacén si el centro de trabajo es
          almacén; ídem con las de varios).
        - horas extras (día o noche y de lo que sean).
        - horas noche (normales + extras).
        - horas mantenimiento sábado (solo mantenimiento y día == 5).
        - horas mantenimiento (sólo mantenimiento, incluye las de sábado).

        Tal y como el cliente planteó las horas en la reunión (procedente de
        una hoja de cálculo "legacy") es imposible determinar con exactitud
        si las horas de producción de una línea son regulares o extra en caso
        de que hubiera de las dos en el mismo registro.
        Para discernirlas hay que idear un algoritmo determinista que asegure
        la diferenciación de horas por línea y tipo coherentemente.
        1.- Determinar las horas de producción por línea.
        2.- Ir restando por orden de ID de línea las horas extras de
            producción hasta agotarlas.
        3.- Las horas restantes de las líneas que sigan >= 0 serán horas
            regulares.
        Misma operación con resto de horas (almacén, mantenimiento y varios).
        """
        res = {}
        for linea in LineaDeProduccion.select():
            res[linea] = {"regulares": 0.0,
                          "extras": 0.0,
                          "noche": 0.0,
                          "mantenimiento sábado": 0.0,
                          "mantenimiento": 0.0}
        for centro in self.RESTOCENTROS:
            res[centro] = {"regulares": 0.0,
                           "extras": 0.0,
                           "noche": 0.0,
                           "mantenimiento": 0.0}
        horas_regulares_por_centro, horas_extras_por_centro = (
            self._dividir_horas_por_centro())
        # Actualizo diccionarios de líneas:
        hrpc = horas_regulares_por_centro
        hepc = horas_extras_por_centro
        noche_por_centro = self._calcular_totales_noche_por_centro()
        for linea in LineaDeProduccion.select():
            res[linea]["regulares"] += hrpc["producción"][linea]
            # No hay horas de almacén ni varios en las líneas, y como
            # aquí no entran las de mantenimiento, solo meto las de prod.
            res[linea]["extras"] += (hepc["producción"][linea]
                                     + hepc["mantenimiento"][linea])
            res[linea]["noche"] = noche_por_centro[linea]
            mantsab = sum([cm.horasMantenimiento for cm
                           in self.controlesHorasMantenimiento
                           if cm.lineaDeProduccion == linea])
            try:
                diasemana = self.fecha.day_of_week
            except AttributeError:
                diasemana = self.fecha.weekday()
            if diasemana == 5:
                res[linea]["mantenimiento sábado"] = mantsab
            res[linea]["mantenimiento"] = mantsab
        res[self.RESTOCENTROS[0]]["regulares"] += hrpc["almacén"]
        res[self.RESTOCENTROS[1]]["regulares"] += hrpc["varios"]
        res[self.RESTOCENTROS[0]]["extras"] += hepc["almacén"]
        res[self.RESTOCENTROS[1]]["extras"] += hepc["varios"]
        res[self.RESTOCENTROS[0]]["noche"] \
            += noche_por_centro[self.RESTOCENTROS[0]]
        res[self.RESTOCENTROS[1]]["noche"] \
            += noche_por_centro[self.RESTOCENTROS[1]]
        # OJO: ¿Horas de mantenimiento en almacén y varios? I like turtles.
        res[self.RESTOCENTROS[0]]["mantenimiento"] = 0.0
        res[self.RESTOCENTROS[1]]["mantenimiento"] = 0.0
        return res

    def _calcular_totales_noche_por_centro(self):
        """
        Devuelve las horas totales de noche regulares por línea, además
        de las de los centros de mantenimiento y almacén.
        Si el parte no tiene marcado nocturnidad, devuelve 0. Si la tiene,
        devuelve las horas de producción por línea.
        """
        lineas = LineaDeProduccion.select()
        lineas = [l for l in lineas]
        res = dict(zip(lineas + list(self.RESTOCENTROS),
                       (0, )*(len(lineas) + len(self.RESTOCENTROS))))
        # Empiezo con diccionario con todas las líneas a 0.
        if self.get_por_hora()["noche"]:
            # Primero lo fácil, horas de almacén y de varios.
            res[self.RESTOCENTROS[0]] = self.horasAlmacen
            res[self.RESTOCENTROS[1]] = self.horasVarios
            # Ahora las de producción y mantenimiento
            for hp in self.controlesHorasProduccion:
                res[hp.lineaDeProduccion] += hp.horasProduccion
            for hm in self.controlesHorasMantenimiento:
                res[hm.lineaDeProduccion] += hm.horasMantenimiento
        return res

    def _dividir_horas_por_centro(self):
        """
        Devuelve dos diccionarios. El primero con las horas regulares y
        el segundo con las horas extra.
        Ambos tienen similar estructura: las claves son "producción",
        "mantenimiento", "almacén" y "varios". Las dos primeras claves son
        a su vez diccionarios cuyas claves son las líneas de producción
        (objetos LineaDeProduccion) y finalmente los valores son flotantes
        con las horas empleadas.
        Los centros de trabajo de varios y almacén no son líneas de producción,
        son siempre "Almacén" y "Varios" (RESTOCENTROS[0] y [1]).
        """
        lineas = LineaDeProduccion.select()
        claves = zip(lineas, (0, )*lineas.count())
        r = {"producción": dict(claves),
             "mantenimiento": dict(claves),
             "almacén": 0.0,
             "varios": 0.0}
        e = {"producción": dict(claves),
             "mantenimiento": dict(claves),
             "almacén": 0.0,
             "varios": 0.0}
        por_tipo_y_linea = self._dividir_por_tipo_y_linea("producción")
        for linea in por_tipo_y_linea:
            e["producción"][linea] += por_tipo_y_linea[linea]["extras"]
        for linea in por_tipo_y_linea:
            r["producción"][linea] += por_tipo_y_linea[linea]["regulares"]
        por_tipo_y_linea = self._dividir_por_tipo_y_linea("mantenimiento")
        for linea in por_tipo_y_linea:
            e["mantenimiento"][linea] += por_tipo_y_linea[linea]["extras"]
        for linea in por_tipo_y_linea:
            r["mantenimiento"][linea] += por_tipo_y_linea[linea]["regulares"]
        e["almacén"] = self.horasExtraDiaAlmacen + self.horasExtraNocheAlmacen
        r["almacén"] = self.horasAlmacen - e["almacén"]
        e["varios"] = self.horasExtraDiaVarios + self.horasExtraNocheVarios
        r["varios"] = self.horasVarios - e["varios"]
        return r, e

    def _dividir_por_tipo_y_linea(self, actividad):
        """
        «actividad» debe ser "producción" o "mantenimiento". Devuelve un
        diccionario con las horas indicadas divididas por línea y tipo (extra
        o regulares).
        Aquí es donde realmente se implementa el algoritmo indicado en
        get_por_centro_de_trabajo_y_tipo.
        """
        res = {}
        if actividad == "producción":
            por_linea = self._dividir_horas_produccion_por_linea()
            rp, ep = self._dividir_horas_produccion_por_tipo()  # @UnusedVariable
        elif actividad == "mantenimiento":
            por_linea = self._dividir_horas_mantenimiento_por_linea()
            rp, ep = self._dividir_horas_mantenimiento_por_tipo()  # @UnusedVariable
        else:
            raise ValueError, "actividad debe ser producción o mantenimiento."
        for linea in por_linea:
            # Inicialmente asigno todas las horas como regulares (optimizo
            # para caso más común):
            res[linea] = {"regulares": por_linea[linea],
                          "extras": 0.0}
        # Y ahora paso paso horas a extras hasta cumplir los cálculos
        # totales de extras y regulares.
        lineas = por_linea.keys()
        lineas.sort(lambda l1, l2: int(l1.id - l2.id))
        # Siempre mismo orden para asegurar determinismo.
        i = 0
        while (rp > 0 and i < len(lineas)):
            rp -= res[lineas[i]]["regulares"]
            if rp < 0:# He agotado las horas regulares, el resto son extra
                res[lineas[i]]["regulares"] += rp
                    # Devuelvo las regulares que he contado de más (rp ha
                    # quedado con un número negativo -si cero no entra aquí-).
                res[lineas[i]]["extras"] = abs(rp) # Comienzo a pasar
                    # horas a extras empezando por el resto regulares -si
                    # lo hubiera- del reparto.
            i += 1  # Y paso a la siguiente línea
        while i < len(lineas):  # Con las demás:
            res[lineas[i]]["extras"] = res[lineas[i]]["regulares"]
            res[lineas[i]]["regulares"] = 0.0
            i += 1
        return res

    def _dividir_horas_produccion_por_linea(self):
        """
        Divide las horas exclusivamente de producción por línea.
        """
        lineas = LineaDeProduccion.select()
        res = dict(zip(lineas, (0, )*lineas.count()))
        for hp in self.controlesHorasProduccion:
            # Los registros ControlHorasProduccion incluyen horas extras.
            res[hp.lineaDeProduccion] += hp.horasProduccion
        return res

    def _dividir_horas_mantenimiento_por_linea(self):
        """
        Divide las horas exclusivamente de mantenimiento por línea.
        """
        lineas = LineaDeProduccion.select()
        res = dict(zip(lineas, (0, )*lineas.count()))
        for hp in self.controlesHorasMantenimiento:
            # Los registros ControlHorasMantenimiento incluyen horas extras.
            res[hp.lineaDeProduccion] += hp.horasMantenimiento
        return res

    def _dividir_horas_produccion_por_tipo(self):
        """
        Divide las horas de producción entre extras y regulares.
        Las regulares son las horas totales de producción menos las horas
        extra de producción de día y de noche.
        """
        extras = self.horasExtraDiaProduccion + self.horasExtraNocheProduccion
        produccion_totales = self.calcular_total_horas_produccion()
        regulares_produccion = produccion_totales - extras
        return regulares_produccion, extras

    def _dividir_horas_mantenimiento_por_tipo(self):
        """
        Divide las horas de mantenimiento entre extras y regulares.
        Las regulares son las horas totales de mantenimiento menos las horas
        extra de mantenimiento de día y de noche.
        """
        extras = (self.horasExtraDiaMantenimiento
                  + self.horasExtraNocheMantenimiento)
        mantenimiento_totales = self.calcular_total_horas_mantenimiento()
        regulares_mantenimiento = mantenimiento_totales - extras
        return regulares_mantenimiento, extras

    def get_concepto_libre(f1, f2):
        """
        Devuelve el concepto libre más común entre las dos fechas.
        Si no hay registros en ese intervalo, devuelve la cadena vacía.
        """
        chs = ControlHoras.select(AND(ControlHoras.q.fecha >= f1,
                                      ControlHoras.q.fecha <= f2))
        conceptos = {}
        for ch in chs:
            if ch.conceptoLibre not in conceptos:
                conceptos[ch.conceptoLibre] = 1
            else:
                conceptos[ch.conceptoLibre] += 1
        maxim, concepto = 0, ""
        for c in conceptos:
            if conceptos[c] > maxim:
                concepto = c
        return concepto

    get_concepto_libre = staticmethod(get_concepto_libre)


cont, tiempo = print_verbose(cont, total, tiempo)

class ControlHorasProduccion(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #------------------------------- controlHorasID = ForeignKey('ControlHoras')
    #--------------------- lineaDeProduccionID = ForeignKey('LineaDeProduccion')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class ControlHorasMantenimiento(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #------------------------------- controlHorasID = ForeignKey('ControlHoras')
    #--------------------- lineaDeProduccionID = ForeignKey('LineaDeProduccion')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class OrdenEmpleados(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------------------------- empleadoID = ForeignKey('Empleado')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def buscar_registros(cls, fecha):
        """
        Devuelve un registro por cada empleado, todos con la misma fecha
        y siendo la más cercana a «fecha» y mayor que ésta.
        """
        try:
            fecha_base = cls._connection.queryOne("""
                            SELECT fecha FROM orden_empleados
                             WHERE fecha <= '%s' ORDER BY fecha DESC
                            """ % fecha.strftime("%Y-%m-%d"))[0]
        except (TypeError, IndexError):
            res = []
        else:
            rs = cls.select(cls.q.fecha == fecha_base,
                              orderBy = "orden")
            pos_tratadas = []
            ids_tratados = []
            res = []
            for r in rs:
                if (r.orden not in pos_tratadas
                    and r.empleadoID not in ids_tratados):
                    res.append(r)
        return res

    buscar_registros = classmethod(buscar_registros)

    def buscar(cls, fecha):
        regs = cls.buscar_registros(fecha)
        return [r.empleadoID for r in regs]

    buscar = classmethod(buscar)

cont, tiempo = print_verbose(cont, total, tiempo)

class ListaObjetosRecientes(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- usuarioID = ForeignKey('Usuario')
    #----------------------------------------- ventanaID = ForeignKey('Ventana')
    idsRecientes = MultipleJoin("IdReciente")

    MAX_RECIENTES = 5

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def push(self, ide):
        """
        Añade un objeto reciente a la lista de IDs si no estaba ya.
        Mantiene siempre la lista con un máximo de MAX_RECIENTES elementos.
        """
        if ide not in [i.objetoID for i in self.idsRecientes]:
            if len(self.idsRecientes) >= self.MAX_RECIENTES:
                self.pop()
        else:
            self.pop(ide)
        idr = IdReciente(listaObjetosRecientes = self, objetoID = ide)  # @UnusedVariable

    def pop(self, ide = None):
        """
        Si se recibe un ID y éste está en la lista, lo saca y lo devuelve.
        En otro caso saca de la pila el que tenga ID más bajo (es decir, el
        más antiguo).
        """
        if ide != None:
            if ide not in [r.objetoID for r in self.idsRecientes]:
                raise ValueError, "ID %d no está en la lista de ids recientes."
            idr = [r for r in self.idsRecientes if r.objetoID == ide][0]
            idr.destroySelf()
            res_id = ide
        else:
            if len(self.idsRecientes) == 0:
                raise ValueError, "Lista de ids recientes vacía."
            idrs = [r for r in self.idsRecientes]
            idrs.sort(lambda r1, r2: int(r1.id - r2.id))
            idr = idrs[0]
            res_id = idr.objetoID
            idr.destroySelf()
        return res_id

    def get_lista(self):
        """
        Devuelve una lista de IDs ordenada por id del registro.
        """
        idrs = [r for r in self.idsRecientes]
        idrs.sort(lambda r1, r2: int(r1.id - r2.id))
        return [r.objetoID for r in idrs]

    def buscar(cls, ventana, usuario = None, crear = False):
        """
        Devuelve el registro que coincide con el usuario y ventana recibidos.
        None si no se encontró ninguno.
        El primero de todos si se encontraron varios.
        Si «usuario» es None, se aplica en la búsqueda como None. «ventana» no
        puede ser None. Sí puede ser una cadena, en cuyo caso se buscará
        primero si la ventana existe en la BD como registro.
        Si «crear» es True, en lugar de devolver None crea un registro nuevo.
        """
        if isinstance(ventana, str):
            try:
                ventana = Ventana.select(Ventana.q.fichero == ventana)[0]
            except IndexError:
                raise ValueError, "%s no es una ventana válida en la BD" % (
                    ventana)
        if usuario != None:
            uid = usuario.id
        else:
            uid = None
        rs = cls.select(AND(cls.q.usuarioID == uid,
                              cls.q.ventanaID == ventana.id),
                          orderBy = "id")
        try:
            return rs[0]
        except:
            if not crear:
                res = None
            else:
                nuevo = cls(ventana = ventana, usuario = usuario)
                res = nuevo
        return res

    buscar = classmethod(buscar)

cont, tiempo = print_verbose(cont, total, tiempo)

class IdReciente(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #------------- listaObjetosRecientesID = ForeignKey('ListaObjetosRecientes')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class Auditoria(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------------------------- usuarioID = ForeignKey('Usuario')
    #----------------------------------------- ventanaID = ForeignKey("Ventana")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        res = "[%s] %s en %s (desde %s <%s>); %s en %s: %s" % (
                utils.str_fechahoralarga(self.fechahora),
                self.usuario and self.usuario.usuario or "Desconocido",
                self.ventana and self.ventana.fichero or "Ventana desconocida",
                self.hostname and self.hostname or "host desconocido",
                self.ip and self.ip or "IP desconocida",
                self.action,
                self.puid,
                self.descripcion)
        return res

    @staticmethod
    def trace(objeto, printout = True):
        """
        Muestra por pantalla la traza en audotoría del objeto de pclases
        recibido si printout es True. También puede ser una lista de
        objetos.
        En otro caso devuelve los textos en una lista.
        """
        res = []
        if isinstance(objeto, (list, tuple)):
            lista_objetos = objeto
            for objeto in lista_objetos:
                res += Auditoria.trace(objeto, printout = False)
        else:
            try:
                dbpuid = objeto.puid
            except AttributeError:  # Es None o algo
                pass
            else:
                audis = Auditoria.select(Auditoria.q.dbpuid == dbpuid,
                                         orderBy = "fechahora")
                for a in audis:
                    res.append(a)
        if printout:
            res.sort(key = lambda a: a.fechahora)
            for a in res:
                myprint(a.get_info())
        else:
            return res

    @staticmethod
    def nuevo(objeto, usuario, ventana, descripcion = None):
        """
        Nuevo registro en la base de datos. Creo un objeto auditoría
        con el usuario recibido y determino IP y nombre de la máquina.
        """
        from formularios import autenticacion
        from socket import gethostname
        ip = autenticacion.get_IPLocal()
        host = gethostname()
        if isinstance(ventana, str):
            if ventana.endswith(".pyc"):
                ventana = ventana[:-1]
            ventana = os.path.basename(ventana)
            try:
                ventana = Ventana.select(Ventana.q.fichero == ventana)[0]
            except IndexError:
                ventana = None
        if not descripcion:
            try:
                descripcion = objeto.get_info().replace("'", "`")
            except Exception, msg:
                descripcion = "pclases::Auditoria.nuevo -> "\
                              "Error al obtener información del objeto. "\
                              "Excepción capturada: %s " % msg
        if not usuario:
            usuario = logged_user
        Auditoria(usuario = usuario,
                  ventana = ventana,
                  dbpuid = objeto.puid,
                  action = "create",
                  ip = ip,
                  hostname = host,
                  descripcion = descripcion)

    @staticmethod
    def borrado(puid, usuario, ventana, descripcion = None):
        """
        Registro borrado en la base de datos. Creo un objeto auditoría con
        una breve descripción del registro eliminado, usuario y ventana desde
        la que se ha hecho. Determino IP y nombre de la máquina aquí.
        """
        from formularios import autenticacion
        from socket import gethostname
        ip = autenticacion.get_IPLocal()
        host = gethostname()
        if isinstance(ventana, str):
            if ventana.endswith(".pyc"):
                ventana = ventana[:-1]
            ventana = os.path.basename(ventana)
            try:
                ventana = Ventana.select(Ventana.q.fichero == ventana)[0]
            except IndexError:
                ventana = None
        if not usuario:
            usuario = logged_user
        if not descripcion:
            # No es muy útil la información por defecto. Pero menos es nada.
            descripcion = "Objeto con PUID %s eliminado." % puid
        Auditoria(usuario = usuario,
                  ventana = ventana,
                  dbpuid = puid,
                  action = "drop",
                  ip = ip,
                  hostname = host,
                  descripcion = descripcion.replace("'", '"'))

    @staticmethod
    def modificado(objeto, usuario, ventana, descripcion = None):
        """
        Registro modificado en la base de datos. Creo un objeto auditoría con
        una breve descripción del registro cambiado, usuario y ventana desde
        la que se ha hecho. Determino IP y nombre de la máquina aquí.
        """
        from formularios import autenticacion
        from socket import gethostname
        ip = autenticacion.get_IPLocal()
        host = gethostname()
        if isinstance(ventana, str):
            if ventana.endswith(".pyc"):
                ventana = ventana[:-1]
            ventana = os.path.basename(ventana)
            try:
                ventana = Ventana.select(Ventana.q.fichero == ventana)[0]
            except IndexError:
                ventana = None
        if not descripcion:
            try:
                difobjeto = objeto.diff()
                #descripcion = objeto.get_info() #Nuevos valores. Mejor que nada
                descripcion = pprint.pformat(difobjeto)
                descripcion = descripcion.decode("utf8", "ignore")
                descripcion = descripcion.replace("'", '"')
                descripcion = descripcion.encode("ascii", "ignore")
            except Exception, msg:
                descripcion = "pclases::Auditoria.modificado -> "\
                              "Error al obtener información del objeto. "\
                              "Excepción capturada: %s " % msg
        else:
            descripcion = descripcion.decode("utf8", "ignore").encode("ascii", "ignore")
        if not usuario:
            usuario = logged_user
        Auditoria(usuario = usuario,
                  ventana = ventana,
                  dbpuid = objeto.puid,
                  action = "update",
                  ip = ip,
                  hostname = host,
                  descripcion = descripcion)

cont, tiempo = print_verbose(cont, total, tiempo)

class ConcentracionRemesa(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------------------------------- bancoID = ForeignKey("Banco")
    #----------------------------------------- clienteID = ForeignKey("Cliente")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

cont, tiempo = print_verbose(cont, total, tiempo)

class Banco(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    pagaresCobro = MultipleJoin('PagareCobro')
    confirmings = MultipleJoin("Confirming")
    remesas = MultipleJoin("Remesa")
    concentracionesRemesa = MultipleJoin("ConcentracionRemesa")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_disponible(self):
        """
        Disponible en la línea de crédito: límite - remesas aceptadas no
        vencidas.
        """
        res = self.limite
        if res != None:
            for r in self.remesas:
                if r.aceptada and not r.esta_vencida():
                    res -= r.importe
        return res

    def get_concentracion_actual(self):
        """
        Devuelve el porcentaje máximo de concentración de un cliente en
        las remesas aceptadas y no vencidas del banco.
        """
        concentraciones = [r.concentracion for r in self.remesas
                            if r.concentracion]
        try:
            concentracion = max(concentraciones, key = lambda c: c[0])
        except (ValueError, TypeError):
            concentracion = None
        return concentracion

    concentracion_actual = property(get_concentracion_actual)

    def comprobar_concentracion_clientes(self, efectos):
        """
        Devuelve una lista de clientes que superan la concentración permitida
        en este banco con la concentración permitida y la concentración en
        el conjunto de efectos recibida.
        """
        concentraciones = {}
        importe_total = 0.0
        res = []
        for efecto in efectos:
            cliente = efecto.cliente
            try:
                concentraciones[cliente] += efecto.cantidad
            except KeyError:
                concentraciones[cliente] = efecto.cantidad
            importe_total += efecto.cantidad
        for cliente in concentraciones:
            concentraciones[cliente] = concentraciones[cliente] / importe_total
            try:
                concentracion_remesa = ConcentracionRemesa.select(AND(
                    ConcentracionRemesa.q.clienteID ==
                                            (cliente and cliente.id or None),
                    ConcentracionRemesa.q.bancoID == self.id))[0]
                concentracion_maxima_cliente=concentracion_remesa.concentracion
            except IndexError:
                concentracion_maxima_cliente = None
            if (concentracion_maxima_cliente != None
                and concentraciones[cliente] > concentracion_maxima_cliente):
                res.append((cliente, concentracion_maxima_cliente,
                            concentraciones[cliente]))
        return res

    @staticmethod
    def digitos_control(entidad, oficina, cuenta):
        def proc(digitos):
            if not digitos.isdigit() or len(digitos) != 10:
                raise ValueError('Debe ser numero de 10 digitos: %s' % digitos)
            factores = [1, 2, 4, 8, 5, 10, 9, 7, 3, 6]
            resultado = 11-sum(int(d)*f for d,f in zip(digitos, factores)) % 11
            if resultado == 10:  return 1
            if resultado == 11:  return 0
            return resultado
        return '%d%d' % (proc('00'+entidad+oficina), proc(cuenta))

cont, tiempo = print_verbose(cont, total, tiempo)

class Efecto(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------------------- pagareCobroID = ForeignKey("PagareCobro")
    #----------------------------------- confirmingID = ForeignKey("Confirming")
    #------------- cuentaBancariaClienteID = ForeignKey("CuentaBancariaCliente")
    remesas = RelatedJoin('Remesa',
                joinColumn = 'efecto_id',
                otherColumn = 'remesa_id',
                intermediateTable = 'efecto__remesa')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    @property
    def observaciones(self):
        try:
            return self.confirming.observaciones
        except AttributeError:
            return self.pagareCobro.observaciones

    @property
    def importe(self):
        try:
            return self.confirming.cantidad
        except AttributeError:
            return self.pagareCobro.cantidad

    @property
    def codigo(self):
        try:
            return self.confirming.codigo
        except AttributeError:
            return self.pagareCobro.codigo

    @property
    def cliente(self):
        try:
            return self.confirming.cliente
        except AttributeError:
            return self.pagareCobro.cliente

    @property
    def cantidad(self):
        try:
            return self.confirming.cantidad
        except AttributeError:
            return self.pagareCobro.cantidad

    @property
    def fechaRecepcion(self):
        try:
            return self.confirming.fechaRecepcion
        except AttributeError:
            return self.pagareCobro.fechaRecepcion

    @property
    def fechaVencimiento(self):
        try:
            return self.confirming.fechaVencimiento
        except AttributeError:
            return self.pagareCobro.fechaVencimiento

    def get_str_tipo(self):
        if self.pagareCobro:
            if self.pagareCobro.aLaOrden:
                str_a_la_orden = "Pagaré a la orden"
            else:
                str_a_la_orden = "Pagaré no a la orden"
        else:
            str_a_la_orden = "Confirming"
        return str_a_la_orden

    def get_estado(self, fecha = mx.DateTime.today()):
        """
        Devuelve el estado del efecto de cobro. Ya sea confirming o pagaré.
        """
        try:
            return self.pagareCobro.get_estado(fecha)
        except AttributeError:
            return self.confirming.get_estado(fecha)

    def get_str_estado(self):
        try:
            return self.pagareCobro.get_str_estado()
        except AttributeError:
            return self.confirming.get_str_estado()


class Remesa(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #--------------------------------------------- bancoID = ForeignKey("Banco")
    efectos = RelatedJoin('Efecto',
                joinColumn = 'remesa_id',
                otherColumn = 'efecto_id',
                intermediateTable = 'efecto__remesa')
    #pagaresCobro = MultipleJoin('PagareCobro')
    #confirmings = MultipleJoin("Confirming")
    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def esta_vencida(self, fecha_base = mx.DateTime.today()):
        """
        True si la primera fecha de vencimiento está cumplida.
        """
        fecha_vto = min([c.fechaVencimiento for c in self.efectos])
        return fecha_vto > fecha_base
    @property
    def tipo(self):
        """
        Remesa a la orden o no a la orden en función del tipo de los
        efectos que incluye.
        """
        # Todos los efectos deben ser del mismo tipo, así que me basta con
        # ver el primero
        try:
            e = self.efectos[0]
        except IndexError:
            return "Vacía"
        else:
            if e.confirming:
                return "Confirming"
            else:
                if e.pagareCobro.aLaOrden:
                    return "A la orden"
                else:
                    return "No a la orden"

    @property
    def importe(self):
        return sum([p.cantidad for p in self.efectos])

    @property
    def concentracion(self):
        """
        Devuelve el porcentaje de concentración máximo, el importe total y el
        objeto cliente al que pertenece esa concentración en la remesa actual.
        """
        # La concentración se calcula por el importe sobre el total.
        total = self.importe
        concentraciones = self.calcular_concentraciones()
        if concentraciones:
            cliente_maximo = max(concentraciones,
                         key = lambda cliente: concentraciones[cliente][0])
            res = (concentraciones[cliente_maximo][0],
                   concentraciones[cliente_maximo][1],
                   cliente_maximo)
        else:
            res = None
        return res

    def calcular_concentraciones(self):
        concentraciones = {}
        for p in self.efectos:
            try:
                concentraciones[p.cliente][1] += p.cantidad
            except KeyError:
                concentraciones[p.cliente] = [None, p.cantidad]
        for cliente in concentraciones:
            concentraciones[cliente][0] = \
                    concentraciones[cliente][1] / self.importe
        return concentraciones

    def get_str_estado(self):
        # DONE: Los estados van:
        #           En preparación -> En estudio -> Confirmada / Rechazada.
        if self.aceptada:
            return "Confirmada"    # El banco la ha aceptado y me da las pelas.
        elif not self.fechaPrevista:
            return "En preparación" # Se está montando la remesa. Todavía no
                                    # se ha enviado al banco.
        #elif self.fechaPrevista and not self.aceptada:
        #    return "Rechazada"  # No se ha aceptado después de haberse enviado.
        # Las rechazadas se borran directamente. No se guardan y por tanto no
        # hay estado para ellas.
        else:
            return "En estudio"     # El banco me la está mirando y puede que
                                    # me confirme un efecto, todos o ninguno.

cont, tiempo = print_verbose(cont, total, tiempo)

class PresupuestoAnual(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    conceptosPresupuestoAnual = MultipleJoin("ConceptoPresupuestoAnual")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def es_gasto(self):
        """
        True si no es un concepto de ingresos (ventas a clientes únicamente).
        """
        # OJO: HARCODED.
        # PLAN: Tal vez hubiera sido mejor un atributo "gasto = bool"
        # en la tabla.
        return self.descripcion != "Clientes"

    @staticmethod
    def check_defaults():
        """
        Comprueba que existen --y si no, los crea-- los conceptos por defecto
        para el presupuesto anual.
        """
        conceptos = {"Gastos personal":
                        ("Nómina mes", "Paga extra", "Hoja de gastos",
                         "Seguros sociales"),
                     "Impuestos": [],
                     "Gastos financieros": ("Estructurales", "Corrientes"),
                     "Proveedores granza": [],
                    # Coincide con los tipos por defecto de clientes y
                    # proveedores (ver su check_defaults)
                     "Resto proveedores":
                        ("Comercializados", "Transporte", "Repuestos",
                         "Suministros", "Materiales", "Resto"),
                     "Clientes":
                        ("Nacionales - Industrial",
                            "Nacionales - General",
                            "Nacionales - Fibra",
                            "Nacionales - Geocem",
                            "Nacionales - Comercializado",
                         "Internacionales - Industrial",
                            "Internacionales - General",
                            "Internacionales - Fibra",
                            "Internacionales - Geocem",
                            "Internacionales - Comercializado"
                        )
                    }
        for c in conceptos:
            try:
                pa = PresupuestoAnual.select(
                        PresupuestoAnual.q.descripcion == c)[0]
            except IndexError:
                pa = PresupuestoAnual(descripcion = c)
            for subc in conceptos[c]:
                if not ConceptoPresupuestoAnual.select(AND(
                        ConceptoPresupuestoAnual.q.descripcion == subc,
                        ConceptoPresupuestoAnual.q.presupuestoAnualID == pa.id)
                       ).count():
                    ConceptoPresupuestoAnual(presupuestoAnual = pa,
                                             descripcion = subc)

cont, tiempo = print_verbose(cont, total, tiempo)

class ConceptoPresupuestoAnual(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #----------------------- presupuestoAnualID = ForeignKey("PresupuestoAnual")
    #--------------------- proveedorID = ForeignKey("Proveedor", default = None)
    valoresPresupuestoAnual = MultipleJoin("ValorPresupuestoAnual")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def calcular_vencimientos(self, fecha = mx.DateTime.today()):
        """
        En función del tipo de concepto devuelve la fecha de vencimiento
        para el importe presupuestado.
        """
        # OJO: Todo HARCODED.
        if self.descripcion == "IVA":
            # Vence el 20 del mes siguiente a no ser que:
            # - Sea diciembre, que entonces se tiene hasta el 30 de enero en
            #   lugar del 20.
            # - Si es julio, en lugar de vencer el 20 de agosto lo hace el 20
            #   de septiembre.
            if fecha.month == 12:
                vto = [mx.DateTime.DateFrom(fecha.year + 1, 1, 30)]
            elif fecha.month == 7:
                vto = [mx.DateTime.DateFrom(fecha.year, 9, 20)]
            else:
                vto = [mx.DateTime.DateFrom(fecha.year, fecha.month + 1, 20)]
        elif self.proveedor:
            # Cada proveedor vence en la fecha que diga su forma de pago.
            self.proveedor.sync()
            vto = self.proveedor.get_fechas_vtos_por_defecto(fecha)
        elif self.presupuestoAnual.descripcion == "Clientes":
            plazos_media_forma_pago = self.calcular_vencimiento_medio_clientes(
                    *self.descripcion.split(" - "))
            vto = []
            for plazo in plazos_media_forma_pago:
                vto.append(fecha + (mx.DateTime.oneDay * plazo))
        elif self.presupuestoAnual.descripcion == "Resto proveedores":
            plazos_media_forma_pago \
                    = self.calcular_vencimiento_medio_proveedores(
                        self.descripcion)
            vto = []
            for plazo in plazos_media_forma_pago:
                vto.append(fecha + (mx.DateTime.oneDay * plazo))
        else:
            vto = [fecha]
        return vto

    def calcular_vencimiento_medio_clientes(self, nacionalidad_as_str,
                                            tipo_as_str):
        """
        Devuelve una lista de días de media de vencimiento de los clientes
        nacionales o extranjeros y del tipo especificado.
        """
        tipo = TipoDeCliente.selectBy(descripcion = tipo_as_str)[0]
        clientes = Cliente.select(AND(
            Cliente.q.tipoDeClienteID == tipo.id,
            Cliente.q.inhabilitado == False))
        vtos = []
        for c in clientes:
            if ((nacionalidad_as_str == "Internacionales"
                    and c.es_extranjero())
                or (nacionalidad_as_str == "Nacionales"
                    and not c.es_extranjero())):
                vtos.append(c.get_vencimientos())
        vtos_medio = self._calcular_media(vtos)
        return vtos_medio

    def calcular_documento_moda_clientes(self, nacionalidad_as_str,
                                         tipo_as_str):
        """
        De todos los documentos de pago de los clientes devuelve el más
        repetido (lo que es la moda de una variable discreta, vaya).
        """
        tipo = TipoDeCliente.selectBy(descripcion = tipo_as_str)[0]
        clientes = Cliente.select(AND(
            Cliente.q.tipoDeClienteID == tipo.id,
            Cliente.q.inhabilitado == False))
        ddps = []
        for c in clientes:
            if ((nacionalidad_as_str == "Internacionales"
                    and c.es_extranjero())
                or (nacionalidad_as_str == "Nacionales"
                    and not c.es_extranjero())):
                ddps.append(c.get_documentoDePago(strict_mode = False))
        vtos_moda = utils.moda(ddps)
        return vtos_moda

    def calcular_vencimiento_medio_proveedores(self, tipo_as_str):
        """
        Devuelve una lista de días de media de vencimiento de los proveedores
        del tipo especificado.
        """
        tipo = TipoDeProveedor.selectBy(descripcion = tipo_as_str)[0]
        proveedores = Proveedor.select(AND(
            Proveedor.q.tipoDeProveedorID == tipo.id,
            Proveedor.q.inhabilitado == False))
        vtos = []
        for c in proveedores:
            vtos.append(c.get_vencimientos())
        vtos_medio = self._calcular_media(vtos)
        return vtos_medio

    def calcular_documento_moda_proveedores(self, tipo_as_str):
        """
        Devuelve una lista de días de media de vencimiento de los proveedores
        del tipo especificado.
        """
        tipo = TipoDeProveedor.selectBy(descripcion = tipo_as_str)[0]
        proveedores = Proveedor.select(AND(
            Proveedor.q.tipoDeProveedorID == tipo.id,
            Proveedor.q.inhabilitado == False))
        ddps = []
        for p in proveedores:
            ddps.append(p.get_documentoDePago(strict_mode = False))
        ddps_moda = utils.moda(ddps)
        return ddps_moda

    def _calcular_media(self, vtos):
        """
        Recibe una lista de listas de enteros. Devuelve una lista de un
        entero media de todos los demás.
        """
        # FIXME: Aquí no se tienen en cuenta varios vencimientos. Se unifica
        # en uno solo. Por ejemplo, nunca devolvería [30, 60, 90].
        nums = utils.aplanar(vtos)
        res = utils.media(nums)
        return [res]

    def es_gasto(self):
        """
        Si mi "padre" es gasto, entonces yo también.
        """
        return self.presupuestoAnual.es_gasto()

    @property
    def documentoDePago(self):
        """
        Devuelve el documento de pago con el que se realizará el pago/cobro
        que representa este concepto en el presupuesto del módulo de tesorería.
        """
        # OJO: HARCODED
        if self.descripcion == "IVA":
            doc = DocumentoDePago.Transferencia()
        elif self.proveedor:
            # Cada proveedor vence en el documento que diga su forma de pago.
            self.proveedor.sync()
            doc = self.proveedor.get_documentoDePago(strict_mode = False)
        elif self.presupuestoAnual.descripcion == "Clientes":
            doc = self.calcular_documento_moda_clientes(
                    *self.descripcion.split(" - "))
        elif self.presupuestoAnual.descripcion == "Resto proveedores":
            doc = self.calcular_documento_moda_proveedores(self.descripcion)
        else:
            doc = None
        return doc

    def calcular_total(self, fini = mx.DateTime.today(), ffin = None):
        """
        Devuelve el total de los importes de los valores presupuestados
        bajo este concepto entre las fechas indicadas. Ambas incluidas.
        """
        criterios = [
                ValorPresupuestoAnual.q.conceptoPresupuestoAnualID == self.id]
        if fini:
            criterios.append(ValorPresupuestoAnual.q.mes >= fini)
        if ffin:
            criterios.append(ValorPresupuestoAnual.q.mes <= ffin)
        valores = ValorPresupuestoAnual.select(AND(*criterios))
        res = valores.sum("importe")
        if res is None:
            res = 0.0
        return res

    def calcular_total_vencimientos(self, fini = mx.DateTime.today(),
                                    ffin = None):
        """
        Devuelve el total de los importes de los valores presupuestados
        bajo este concepto cuyos vencimientos caigan entre las fechas
        indicadas. Ambas incluidas.
        Más lento que el «calcular_total».
        """
        criterios = []
        if fini:
            criterios.append(VencimientoValorPresupuestoAnual.q.fecha >= fini)
        if ffin:
            criterios.append(VencimientoValorPresupuestoAnual.q.fecha <= ffin)
        if criterios:
            vtos = ValorPresupuestoAnual.select(AND(*criterios))
        else:
            vtos = ValorPresupuestoAnual.select()
        res = 0.0
        for v in vtos:
            if v.conceptoPresupuestoAnual == self:
                res += v.importe
        return res

cont, tiempo = print_verbose(cont, total, tiempo)

class VencimientoValorPresupuestoAnual(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #------------- valorPresupuestoAnualID = ForeignKey("ValorPresupuestoAnual")
    #------------------------- documentoDePagoID = ForeignKey('DocumentoDePago')

    def _init(self, *args, **kw):
        starter(self, *args, **kw)

    def get_info(self):
        return "(%s) Vto.: %s. Importe: %s" % (
                self.valorPresupuestoAnual.get_info(),
                utils.str_fecha(self.fecha),
                utils.float2str(self.importe))

    @property
    def importe(self):
        self.valorPresupuestoAnual.sync()
        valor = self.valorPresupuestoAnual.importe
        importe = valor / len(
                self.valorPresupuestoAnual.vencimientosValorPresupuestoAnual)
        return importe

    @property
    def toneladas(self):
        """
        Si el valor es de un proveedor de granza, devuelve las toneladas
        calculadas como importe / precio por tonelada. Si no, lanza una
        excepción ValueError.
        """
        if self.valorPresupuestoAnual.es_de_granza():
            return self.importe / self.precio
        else:
            raise ValueError

    @property
    def precio(self):
        self.valorPresupuestoAnual.sync()
        return self.valorPresupuestoAnual.precio

    @property
    def conceptoPresupuestoAnual(self):
        return self.valorPresupuestoAnual.conceptoPresupuestoAnual

    def get_mes(self):
        return self.fecha

    def set_mes(self, value):
        self.fecha = value

    mes = property(get_mes, set_mes)

    def es_de_granza(self):
        return self.valorPresupuestoAnual.es_de_granza()

    def es_de_iva(self):
        return self.valorPresupuestoAnual.es_de_iva()

    def es_de_compras(self):
        return self.valorPresupuestoAnual.es_de_compras()

    def es_de_compras_comercializados(self):
        return self.valorPresupuestoAnual.es_de_compras_comercializados()

    def es_de_compras_transporte(self):
        return self.valorPresupuestoAnual.es_de_compras_transporte()

    def es_de_compras_resto(self):
        return self.valorPresupuestoAnual.es_de_compras_resto()

    def es_de_compras_repuestos(self):
        return self.valorPresupuestoAnual.es_de_compras_repuestos()

    def es_de_compras_suministros(self):
        return self.valorPresupuestoAnual.es_de_compras_suministros()

    def es_de_compras_materiales(self):
        return self.valorPresupuestoAnual.es_de_compras_materiales()

    def es_de_ventas(self):
        return self.valorPresupuestoAnual.es_de_ventas()

    def es_de_ventas_nacionales(self):
        return self.valorPresupuestoAnual.es_de_ventas_nacional()

    def es_de_ventas_internacionales(self):
        return self.valorPresupuestoAnual.es_de_ventas_internacional()

    def es_de_ventas_comercializado(self):
        return self.valorPresupuestoAnual.es_de_ventas_comercializado()

    def es_de_ventas_fibra(self):
        return self.valorPresupuestoAnual.es_de_ventas_fibra()

    def es_de_ventas_general(self):
        return self.valorPresupuestoAnual.es_de_ventas_general()

    def es_de_ventas_geocem(self):
        return self.valorPresupuestoAnual.es_de_ventas_geocem()

    def es_de_ventas_industrial(self):
        return self.valorPresupuestoAnual.es_de_ventas_industrial()

    @classmethod
    def _remove_dupes(classVVPA):
        """
        Comprueba y elimina cualquier vencimiento duplicado para el mismo
        concepto y fecha.
        """
        dupes = []
        for vto in classVVPA.select():
            if vto not in dupes:
                for vto_dup in classVVPA.select(AND(classVVPA.q.id != vto.id,
                                        classVVPA.q.fecha == vto.fecha,
                                        classVVPA.q.valorPresupuestoAnualID
                                            == vto.valorPresupuestoAnual.id)):
                    dupes.append(vto_dup)
        to_drop = len(dupes)
        for vto in dupes:
            vto.destroy()
        return to_drop

class ValorPresupuestoAnual(SQLObject, PRPCTOO):
    class sqlmeta:
        fromDatabase = True
    #------- conceptoPresupuestoAnualID = ForeignKey("ConceptoPresupuestoAnual")
    vencimientosValorPresupuestoAnual = MultipleJoin(
            "VencimientoValorPresupuestoAnual")

    def _init(self, *args, **kw):
        starter(self, *args, **kw)
        if not self.vencimientosValorPresupuestoAnual:
            concepto = self.conceptoPresupuestoAnual
            vencimientos = concepto.calcular_vencimientos(self.mes)
            doc_pago = concepto.documentoDePago
            for v in vencimientos:
                vto = VencimientoValorPresupuestoAnual(
                        valorPresupuestoAnual = self,
                        fecha = v,
                        documentoDePago = doc_pago)
                Auditoria.nuevo(vto, None, __file__)
                if DEBUG:
                    myprint("ValorPresupuestoAnual::_init -> (%s) "\
                            "Vto. %s creado." % (self.puid, vto.get_info()))

    def get_info(self):
        try:
            toneladas = ", %s tm" % utils.float2str(self.toneladas)
        except ValueError:
            toneladas = ""
        return "(%d) %s: %s%s. Mes presupuesto: %s. Fecha vencimiento: %s." % (
                self.id, self.concepto, utils.float2str(self.importe),
                toneladas,
                self.mes.strftime("%B '%y"),
                ", ".join(["%s (%s)" % (utils.str_fecha(v.fecha),
                                        utils.float2str(v.importe))
                           for v in self.vencimientosValorPresupuestoAnual]))

    @property
    def concepto(self):
        try:
            return self.conceptoPresupuestoAnual.descripcion
        except AttributeError:
            return ""

    def get_fecha(self):
        return self.mes

    def set_fecha(self, value):
        self.mes = value

    fecha = property(get_fecha, set_fecha)

    def es_de_granza(self):
        """
        Devuelve True si es un valor de presupuesto de un concepto
        correspondiente a compras a proveedores de materia prima (granza).
        """
        # OJO: HARCODED
        c = self.conceptoPresupuestoAnual
        return c.presupuestoAnual.descripcion == "Proveedores granza"

    def es_de_iva(self):
        """
        Devuelve True si es un valor de presupuesto de un concepto
        correspondiente al IVA mensual.
        """
        # OJO: HARCODED
        c = self.conceptoPresupuestoAnual
        assert (c.descripcion != "IVA" or
                (c.descripcion == "IVA"
                    and c.presupuestoAnual.descripcion == "Impuestos"))
        return c.descripcion == "IVA"

    def es_de_compras(self):
        """
        True si es un valor presupuestado de compras que no sean materia prima
        (granza específicamente).
        """
        # OJO: HARCODED
        c = self.conceptoPresupuestoAnual
        return c.presupuestoAnual.descripcion == "Resto proveedores"

    def es_de_compras_comercializados(self):
        # OJO: HARCODED
        return self.es_de_compras() and self.descripcion == "Comercializados"

    def es_de_compras_transporte(self):
        # OJO: HARCODED
        return self.es_de_compras() and self.descripcion == "Transporte"

    def es_de_compras_resto(self):
        # OJO: HARCODED
        return self.es_de_compras() and self.descripcion == "Resto"

    def es_de_compras_repuestos(self):
        # OJO: HARCODED
        return self.es_de_compras() and self.descripcion == "Repuestos"

    def es_de_compras_suministros(self):
        # OJO: HARCODED
        return self.es_de_compras() and self.descripcion == "Suministros"

    def es_de_compras_materiales(self):
        # OJO: HARCODED
        return self.es_de_compras() and self.descripcion == "Materiales"

    def es_de_ventas(self):
        """
        True si es un valor de presupuesto correspondiente a ventas.
        """
        # OJO: HARCODED
        c = self.conceptoPresupuestoAnual
        return c.presupuestoAnual.descripcion == "Clientes"

    def es_de_ventas_nacionales(self):
        # OJO: HARCODED
        return self.es_de_ventas() and not self.es_de_ventas_nacionales()

    def es_de_ventas_internacionales(self):
        # OJO: HARCODED
        return (self.es_de_ventas()
                and self.descripcion.startswith("Internacionales"))

    def es_de_ventas_comercializado(self):
        # OJO: HARCODED
        return (self.es_de_ventas()
                and self.descripcion.endswith("Comercializado"))

    def es_de_ventas_fibra(self):
        # OJO: HARCODED
        return (self.es_de_ventas()
                and self.descripcion.endswith("Fibra"))

    def es_de_ventas_general(self):
        # OJO: HARCODED
        return (self.es_de_ventas()
                and self.descripcion.endswith("General"))

    def es_de_ventas_geocem(self):
        # OJO: HARCODED
        return (self.es_de_ventas()
                and self.descripcion.endswith("Geocem"))

    def es_de_ventas_industrial(self):
        # OJO: HARCODED
        return (self.es_de_ventas()
                and self.descripcion.endswith("Industrial"))

    @property
    def toneladas(self):
        """
        Si el valor es de un proveedor de granza, devuelve las toneladas
        calculadas como importe / precio por tonelada. Si no, lanza una
        excepción ValueError.
        """
        if self.es_de_granza():
            return self.importe / self.precio
        else:
            raise ValueError

cont, tiempo = print_verbose(cont, total, tiempo)


# TODO: Esto tengo que diferirlo porque durante la carga de pclases no puedo
#       crear objetos. Da error. Sobre todo si la carga es indirecta desde
#       el menú y tras una primera ejecución del programa con la BD limpia.
# Con esto me aseguro de que existen los tipos de proveedor mínimos necesarios.
TipoDeProveedor.check_defaults()
TipoDeCliente.check_defaults()

## XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX XXX

def getObjetoPUID(puid):
    """
    Intenta determinar la clase del objeto a partir de la primera parte del
    PUID y devuelve el objeto en sí o lanzará una excepción.
    """
    dict_clases = {"PC": ProductoCompra,
                   "PV": ProductoVenta,
                   "PAGC": PagareCobro,
                   "PAGP": PagarePago,
                   "CONF": Confirming,
                   "COB": Cobro,
                   "PAG": Pago,
                   #"Bolsa": Bolsa,
                   "Caja": Caja,
                   "Pale": Pale,
                   "PartidaCem": PartidaCem,
                  }
    tipo, ide = puid.split(":")  # @UnusedVariable
    if tipo not in dict_clases:
        try:
            clase = eval(tipo)
        except:
            raise ValueError, "La primera parte del PUID debe ser: %s" % (
                ", ".join(dict_clases.keys()))
    else:
        clase = dict_clases[tipo]
    ide = int(ide)
    objeto = clase.get(ide)
    return objeto

def func_orden_cargas_fecha(c1, c2):
    """
    Compara dos fechas entre dos cargas de silo.
    """
    if c1.fechaCarga < c2.fechaCarga:
        return -1
    if c1.fechaCarga > c2.fechaCarga:
        return 1
    return 0

def unificar(bueno, malos, borrar_despues = True):
    """
    Pasa todos los registros dependientes de cada objeto de «malos» a «bueno».
    Si borrar_despues es Verdadero, elimina los malos después de haber
    unificado.
    Se comprueba que todos los objetos sean de la misma clase de pclases.
    OJO: No funciona para objetos con relaciones muchos a muchos.
    """
    if not isinstance(malos, (list, tuple)):
        malos = [malos]
    for malo in malos:
        assert malo.__class__ == bueno.__class__
    assert bueno not in malos
    nombreclase=str(bueno.__class__).split(".")[-1].split()[0]
    from string import letters
    nombreclase = [l for l in nombreclase
                   if l in letters or l in "12344567890" or l in "_"]
    nombreclase = "".join(nombreclase)
    for malo in malos:
        for join in malo.sqlmeta.joins:
            lista = join.joinMethodName
            for dependiente in getattr(malo, lista):
                for col in dependiente.sqlmeta.columnList:
                    if (isinstance(col, SOForeignKey)
                        and col.foreignKey == nombreclase):
                        clave_ajena = col.name
                try:
                    setattr(dependiente, clave_ajena, bueno.id)
                except UnboundLocalError, e:
                    myprint("pclases.py::unificar -> UnboundLocalError %s:"\
                          "\ndependiente: %s\ncol: %s" % (
                            e, dependiente, col))
                dependiente.syncUpdate()
    if borrar_despues:
        for malo in malos:
            malo.destroy()

def el_anecdoton(fecha):
    """
    Devuelve una lista de puids de objetos cuya fecha coincida con la
    recibida.
    """
    res = []
    this_mod = __import__(__name__)
    clases_y_mas = [val.replace(__name__ + ".", "") for val in dir(this_mod)]
    for nombreitem in clases_y_mas:
        # FIXME: Esto ya no vale con la nueva estructura de paquete. Da un
        #        NameError: name '__all__' is not defined
        clase = eval(nombreitem)
        if DEBUG:
            myprint("clase", clase)
        try:
            padres = clase.__bases__
            if DEBUG:
                myprint("padres", padres)
        except AttributeError:
            padres = []
        if SQLObject in padres:
            dict_cols = clase.sqlmeta.columns
            for namecol in dict_cols:
                col = dict_cols[namecol]
                if isinstance(col, SODateCol):
                    res += buscar_puids_en_fecha(fecha, nombreitem, namecol)
                elif isinstance(col, SODateTimeCol):
                    res += buscar_puids_sobre_fecha(fecha, nombreitem, namecol)
    return res

def buscar_puids_en_fecha(fecha, nameclase, namecol):
    """
    Recibe una clase y un nombre de columna por el que buscar la fecha "fecha".
    Devuelve una lista de PUIDs coincidentes.
    """
    colbusqueda = nameclase + ".q." + namecol
    consulta = nameclase + ".select(%s == fecha)" % colbusqueda
    if DEBUG:
        myprint("consulta (buscar_puids_sobre_fecha)", consulta)
    consulta = eval(consulta)
    puids = [o.get_puid() for o in consulta]
    return puids

def buscar_puids_sobre_fecha(fecha, nameclase, namecol):
    """
    Recibe una clase y un nombre de columna por el que buscar la fecha "fecha".
    Devuelve una lista de PUIDs coincidentes.
    """
    colbusqueda = nameclase + ".q." + namecol
    diasiguiente = fecha + mx.DateTime.oneDay  # @UnusedVariable
    consulta = nameclase + ".select(AND(%s >= fecha, %s < diasiguiente))" % (
        colbusqueda)
    if DEBUG:
        myprint("consulta (buscar_puids_sobre_fecha)", consulta)
    consulta = eval(consulta)
    puids = [o.get_puid() for o in consulta]
    return puids

def do_unittests():
    # Pruebas unitarias
    cmd_grep = r"egrep ^class %s | grep PRPCTOO | grep ')' | cut -d ' ' -f 2 "\
                "| cut -d '(' -f 1" % __file__
    clases_persistentes = [s.replace("\n", "") for s in os.popen(cmd_grep)]
    conhack.autoCommit = False  # HACK del autocommit en SQLObject Ubuntu 12.04
    for clase in clases_persistentes:
        try:
            c = eval(clase)
            myprint("Buscando primer registro de %s... " % (clase))
            reg = c.select(orderBy="id")[0]  # @UnusedVariable
            myprint("[OK]")
        except IndexError:
            myprint("[KO] - La clase %s no tiene registros" % (clase))
    conhack.autoCommit = True   # HACK del autocommit en SQLObject Ubuntu 12.04


######################## Clases refactorizadas ###############################

cont, tiempo = print_verbose(cont, total, tiempo)

#from superfacturaventa import *

cont, tiempo = print_verbose(cont, total, tiempo)

from facturaventa import *

cont, tiempo = print_verbose(cont, total, tiempo)

from facturadeabono import *

cont, tiempo = print_verbose(cont, total, tiempo)

from prefactura import *

cont, tiempo = print_verbose(cont, total, tiempo)

from cliente import *

##############################################################################

# Si no existen el par de estados que deberían existir, los creo sobre la
# marcha:
try:
    Estado.get(1)
except SQLObjectNotFound:
    myprint("Creando estado de alarmas 1...")
    Estado(id=1, descripcion="No leída", pendiente=True)
try:
    Estado.get(2)
except SQLObjectNotFound:
    myprint("Creando estado de alarmas 2...")
    Estado(id=2, descripcion="En espera", pendiente=True)
try:
    Estado.get(3)
except SQLObjectNotFound:
    myprint("Creando estado de alarmas 3...")
    Estado(id=3, descripcion="Cerrada", pendiente=False)



# HACK:
# autocommit en algunas versiones es un boolean y sqlobject intenta
# activarlo como si fuera una función. Aquí pasa algo parecido a la
# magia. Porque si lo activo manualmente ahora, no protesta y
# funciona el autocommit.
conhack.autoCommit = True

def do_performance_test():
    import time
    #for pv in ProductoVenta.select():
    for pv in [ProductoVenta.get(102)]:
        antes = time.time()
        myprint(pv.puid, pv.descripcion, pv.get_stock_kg_A())
        myprint(">>>", round(time.time() - antes, 2), "s")


if __name__ == '__main__':
    DEBUG = True
    do_unittests()
    #do_performance_test()
    #r = Rollo.select()[0]
    #r.destroy_en_cascada()
