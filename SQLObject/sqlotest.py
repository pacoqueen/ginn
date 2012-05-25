# OJO: Son pruebas. No creo que ni funcione actualmente.

from sqlobject import *

import threading, select, psycopg

conn = 'postgres://queen@localhost/ginn-prueba'

#class Persona(SQLObject):
#  _connection = conn
#  _cacheValue = False

#  nombre = StringCol()
#  apellidos = StringCol()

#  def notifyNombreChange(self, valor):
#    print "Atenchione: El nombre ha cambiado, ahora vale %s" % valor

#  def _set_nombre(self, valor):
#    self.notifyNombreChange(valor)
#    self._SO_set_nombre(valor)
    
    # Si tengo el _cacheValue = False, cada vez que se acceda a un valor se
    # vuelve consultar la base de datos. Pero para esto hay que usar transacciones
    # cada vez que se cambie un atributo de la clase:
    # Esto no tira: trans = self._connection.transaction()
    ## DAQUIPABAJO es mierda to:
#    trans = DBConnection.PostgresConnection(conn)
#    self._SO_set_nombre(valor)
#    trans.commit()


#class Clientes(SQLObject):
class Facturas(SQLObject):
  _connection = conn
  _fromDatabase = True
#  _idName = 'idcliente'
  _idName = 'idfactura'
  def _init(self, *args, **kw):
    ## ---- Código para los hilos:
    self.__th_espera = threading.Thread(target=self.esperarNotificacion)
    self.__th_espera.setDaemon(1)
    self.__th_espera.start()
    try:
      self.__conn = psycopg.connect("dbname=%s user=%s password=%s" %('ginn-prueba','queen','******'))
    except:
      print "ERROR estableciendo conexión secundaria para IPC."
    ## ---------------------------
    # Llamada al constructor de la clase padre:
    SQLObject._init(self, *args, **kw) 

  ## Código del hilo:
  def esperarNotificacion(self, func=None):
    c = self.__conn.cursor()
    c.execute("LISTEN IPC_facturas;")
    self.__conn.commit()
    if select.select([c],[],[])!=([],[],[]):
      print "Notificación recibida"
      try:
        self.sync()
      except SQLObjectNotFound:
        print "Registro borrado"	## Algo debería hacer para eliminar este objeto de memoria o algo.
    self.__th_espera.run()	## Vuelvo a ejecutar el hilo, aunque si el registro está borrado no sé para qué.

if __name__=="__main__":
#  p = Persona.get(1)
#  p.set(nombre="Steven", apellidos="Falken")
  f=Facturas.get(1)

