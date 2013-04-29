
class @@Clase@@(SQLObject, PRPCTOO):
    _connection = conn
    _fromDatabase = True
@@Relaciones@@
    def _init(self, *args, **kw):
        starter(self, *args, **kw)
