#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A ver cómo sale el invento.

Esto es un módulo que a partir de una clase de pclases construye el TreeModel 
correspondiente con sus funciones para editar los valores de acuerdo al tipo 
de datos de la columna y todo, todo, todo.
"""

from framework import pclases
import utils

def edit_text(cell, path, newtext, tv, numcol, clase, atributo):
    """
    Cambia el texto del model[path][numcol] y del objeto relacionado que 
    saca a partir del ID de la última columna del model.
    """
    model = tv.get_model()
    ide = model[path][-1]
    objeto = clase.get(ide)
    setattr(objeto, atributo, newtext)  # Sin validación. Texto acepta todo.
    objeto.syncUpdate()
    model[path][numcol] = getattr(objeto, atributo)

def edit_fecha(cell, path, newtext, tv, numcol, clase, atributo):
    """
    Cambia el texto del model[path][numcol] y del objeto relacionado que 
    saca a partir del ID de la última columna del model.
    """
    model = tv.get_model()
    ide = model[path][-1]
    objeto = clase.get(ide)
    try:
        fecha = utils.parse_fecha(newtext)
    except (ValueError, TypeError):
        parent = tv.parent
        while parent != None:
            parent = parent.parent
        utils.dialogo_info(titulo = "ERROR EN FECHA", 
            texto = "El texto «%s» no es una fecha válida." % (newtext), 
            padre = parent)
    else:
        setattr(objeto, atributo, fecha)  
        objeto.syncUpdate()
    model[path][numcol] = utils.str_fecha(getattr(objeto, atributo))

def edit_fechahora(cell, path, newtext, tv, numcol, clase, atributo):
    """
    Cambia el texto del model[path][numcol] y del objeto relacionado que 
    saca a partir del ID de la última columna del model.
    """
    model = tv.get_model()
    ide = model[path][-1]
    objeto = clase.get(ide)
    try:
        fecha = utils.parse_fechahora(newtext)
    except (ValueError, TypeError):
        parent = tv.parent
        while parent != None:
            parent = parent.parent
        utils.dialogo_info(titulo = "ERROR EN FECHA Y HORA", 
            texto = "El texto «%s» no es una fecha y hora válida." % (newtext), 
            padre = parent)
    else:
        setattr(objeto, atributo, fecha)  
        objeto.syncUpdate()
    model[path][numcol] = utils.str_fechahora(getattr(objeto, atributo))

def edit_hora(cell, path, newtext, tv, numcol, clase, atributo):
    """
    Cambia el texto del model[path][numcol] y del objeto relacionado que 
    saca a partir del ID de la última columna del model.
    """
    model = tv.get_model()
    ide = model[path][-1]
    objeto = clase.get(ide)
    try:
        hora = utils.parse_hora(newtext)
    except (ValueError, TypeError):
        parent = tv.parent
        while parent != None:
            parent = parent.parent
        utils.dialogo_info(titulo = "ERROR EN HORA", 
            texto = "El texto «%s» no es una hora válida." % (newtext), 
            padre = parent)
    else:
        setattr(objeto, atributo, hora)  
        objeto.syncUpdate()
    model[path][numcol] = utils.str_hora(getattr(objeto, atributo))

def edit_float(cell, path, newtext, tv, numcol, clase, atributo):
    """
    Cambia el texto del model[path][numcol] y del objeto relacionado que 
    saca a partir del ID de la última columna del model.
    """
    try:
        numero = utils.parse_float(newtext)
    except (ValueError, TypeError):
        parent = tv.parent
        while parent != None:
            parent = parent.parent
        utils.dialogo_info(titulo = "ERROR EN NÚMERO", 
            texto = "El texto «%s» no es un número válido." % (newtext), 
            padre = parent)
    else:
        model = tv.get_model()
        ide = model[path][-1]
        objeto = clase.get(ide)
        setattr(objeto, atributo, numero) 
        objeto.syncUpdate()
    model[path][numcol] = utils.float2str(getattr(objeto, atributo), 
                                          autodec = True)

def edit_int(cell, path, newtext, tv, numcol, clase, atributo):
    """
    Cambia el texto del model[path][numcol] y del objeto relacionado que 
    saca a partir del ID de la última columna del model.
    """
    try:
        numero = utils.parse_numero(newtext)
    except (ValueError, TypeError):
        parent = tv.parent
        while parent != None:
            parent = parent.parent
        utils.dialogo_info(titulo = "ERROR EN NÚMERO", 
            texto = "El texto «%s» no es un número entero válido." % (newtext), 
            padre = parent)
    else:
        model = tv.get_model()
        ide = model[path][-1]
        objeto = clase.get(ide)
        setattr(objeto, atributo, numero) 
        objeto.syncUpdate()
    model[path][numcol] = getattr(objeto, atributo)

def edit_boolean(cell, path, tv, numcol, clase, atributo):
    """
    Cambia el valor booleano del model[path][numcol] y del objeto relacionado 
    que saca a partir del ID de la última columna del model.
    """
    model = tv.get_model()
    ide = model[path][-1]
    objeto = clase.get(ide)
    valor = not model[path][numcol]
    setattr(objeto, atributo, valor) 
    objeto.syncUpdate()
    model[path][numcol] = getattr(objeto, atributo)

def col2value(objeto, col):
    """
    Convierte el valor del objeto a un formato legible en función de su 
    tipo de datos.
    """
    valor = getattr(objeto, col.name)
    if isinstance(col, pclases.SODateCol):    # Es DATE.
        return utils.str_fecha(valor)
    elif isinstance(col, pclases.SOStringCol):  # TEXT
        return valor 
    elif isinstance(col, pclases.SOFloatCol):   # FLOAT
        return utils.float2str(valor, autodec = True)
    elif isinstance(col, pclases.SOIntCol):     # INT
        return valor 
    elif isinstance(col, pclases.SOBoolCol):    # BOOLEAN
        return valor 
    elif isinstance(col, pclases.SOForeignKey): # Clave ajena. 
        return valor # and valor.id or ""
    elif isinstance(col, pclases.SOCol):          # Es TIMESTAMP o TIME
        if "timestamp" in str(col) or ("fecha" in col.name 
                                       and "hora" in col.name):
            return utils.str_fechahora(valor)
        else:
            return utils.str_hora(valor) 


class Pclase2tv:
    """
    El objetivo es, por cada atributo de pclase, crear la tupla que se le 
    va a pasar al utils inlcuyendo una función anónima que gestionará los 
    cambios en el modelo.
    """

    def __init__(self, pclase, tv, objeto_clave_ajena = None, 
                 cols_a_ignorar = [], nombres_col = [], 
                 seleccion_multiple = False, 
                 orden = None):
        """
        Si se recibe un "objeto_clave_ajena" filtrará los datos mostrados en 
        el treeview a los relacionados con él. Sin embargo si se recibiera 
        un filtro en rellenar_tabla, éste prevalecerá sobre el del constructor.
        Las columnas cuyos nombres estén en cols_a_ignorar no se mostrarán.
        Si se recibe algo en «orden», las columnas se montarán en ese orden.
        Debe ser una lista o una tupla de los nombres de las columnas en 
        estilo CamelCase. Si alguna está en la lista de ignorar, se ingorará 
        aunque esté incluida en el orden. Si alguna columna 
        no está en la lista de orden, se añadirá al final.
        """
        self.clase = pclase
        self.tv = tv
        self.funciones = {}
        self.cols_a_ignorar = cols_a_ignorar
        self.__columnas = self.clase._SO_columns
        cols = self.crear_cols(nombres_col, orden)
        utils.preparar_listview(self.tv, cols, multi = seleccion_multiple)
        if objeto_clave_ajena:
            nombrefk = (objeto_clave_ajena.__class__.__name__[0].lower() + 
                        objeto_clave_ajena.__class__.__name__[1:] + "ID")
            ajeno_id = objeto_clave_ajena.id
            self.filtro = lambda o: getattr(o, nombrefk) == ajeno_id
        else:
            self.filtro = lambda o: True

    def build_funcedit(self, col, numcol):
        """
        Devuelve una función de edición que será el callback que se 
        pasará al TreeView para enlazar con la señal del cell.
        """
        if isinstance(col, pclases.SODateCol):    # Es DATE.
            return edit_fecha, self.tv, numcol, self.clase, col.name
        elif isinstance(col, pclases.SOStringCol):  # TEXT
            return edit_text, self.tv, numcol, self.clase, col.name
        elif isinstance(col, pclases.SOFloatCol):   # FLOAT
            return edit_float, self.tv, numcol, self.clase, col.name
        elif isinstance(col, pclases.SOIntCol):     # INT
            return edit_int, self.tv, numcol, self.clase, col.name
        elif isinstance(col, pclases.SOBoolCol):    # BOOLEAN
            return edit_boolean, self.tv, numcol, self.clase, col.name
        elif isinstance(col, pclases.SOForeignKey): # Clave ajena. La ignoro.
            return None, []
        elif isinstance(col, pclases.SOCol):          # Es TIMESTAMP o TIME
            if "timestamp" in str(col) or ("fecha" in col.name 
                                           and "hora" in col.name):
                return edit_fechahora, self.tv, numcol, self.clase, col.name
            else:
                return edit_hora, self.tv, numcol, self.clase, col.name

    def crear_cols(self, nombres_col = [], orden = None):
        """
        Crea las tuplas que se pasarán al preparar_listview a partir de los 
        atributos de pclases y las funciones a ejecutar cuando se modifican 
        las celdas.
        """
        cols = []
        numcol = 0
        if orden:
            _columnas = []
            for nombrecol in orden:
                for col in self.__columnas:
                    if col.name == nombrecol:
                        _columnas.append(col)
            for col in self.__columnas:
                if col not in _columnas:
                    _columnas.append(col)
            self.__columnas = _columnas
        for col in self.__columnas:
            if col.name in self.cols_a_ignorar:
                continue
            a_conectar = self.build_funcedit(col, numcol)
            funcion_edicion, parametros = a_conectar[0], a_conectar[1:]
            if isinstance(col, pclases.SOBoolCol):
                tipo = "gobject.TYPE_BOOLEAN"
            else:
                tipo = "gobject.TYPE_STRING"
            try:
                nombre_col = nombres_col.pop(0)
            except IndexError:
                nombre_col = col.name.title()
            tvcol = [nombre_col, 
                     tipo,  
                     True, 
                     True, 
                     False, 
                     funcion_edicion, 
                     parametros]
            if not funcion_edicion:
                tvcol[2] = False
            else:
                self.funciones[col.name] = funcion_edicion
            cols.append(tvcol)
            numcol += 1
        cols.append(["ID", "gobject.TYPE_INT64", False, False, False, None])
        cols[0][4] = True   # Búsqueda interactiva en la primera columna.
        return cols

    def rellenar_tabla(self, filtro = None, campo_orden = "id", padre = None,
                       sumatorios = [], limpiar_model = True, *args, **kw):
        """
        A partir de todos los objetos de la clase rellena la tabla, mostrando 
        una ventana de progreso durante el proceso. Si filtro != None, debe 
        ser una función que sirva para DESCARTAR los objetos que no se 
        mostrarán. La función debe evaluarse a True con el objeto que se esté 
        tratando para que se añada al model ListView del TreeView.
        «padre» es la ventana padre para la de progreso.
        Las columnas (sus nombres en realidad) que vengan en «sumatorios» se 
        sumarán y se devolverán en el mismo orden.
        *args y **kw son parámetros adicionales que se pasarán al filtro.
        """
        res = []
        for colsum in sumatorios:  # @UnusedVariable
            res.append(0.0)
        objetos = self.clase.select(orderBy = campo_orden)
        model = self.tv.get_model()
        self.tv.freeze_child_notify()
        self.tv.set_model(None)
        if not filtro:
            filtro = self.filtro 
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = padre)
        txtpro = "Mostrando %s (%%d/%%d)..." % self.clase.__name__
        vpro.mostrar()
        if limpiar_model:
            model.clear()
        total = objetos.count()
        if not total:
            total = 1.0
        i = 0.0
        vpro.set_valor(i / total, txtpro % (i, total)) 
        for objeto in objetos:
            i += 1
            if filtro(objeto, *args, **kw):
                fila = []
                for col in self.__columnas:
                    if col.name in self.cols_a_ignorar:
                        continue
                    if col.name in sumatorios:
                        res[sumatorios.index(col.name)] += getattr(objeto, 
                                                                   col.name)
                    valor = col2value(objeto, col)
                    fila.append(valor)
                fila.append(objeto.id)
                model.append(fila)
            vpro.set_valor(i / total, txtpro % (i, total)) 
        self.tv.set_model(model)
        self.tv.thaw_child_notify()
        vpro.ocultar()
        return res

def test(pclase):
    """
    Recibe una pclase y monta una ventana con un TreeView para el modelo 
    generado.
    """
    import gtk
    ventana = gtk.Window()
    ventana.set_title("table2tv")
    ventana.resize(800, 600)
    container = gtk.ScrolledWindow()
    ventana.add(container)
    tv = gtk.TreeView()
    container.add(tv)
    rocio = Pclase2tv(pclase, tv)
    ventana.show_all()
    rocio.rellenar_tabla()
    gtk.main()


if __name__ == "__main__":
    test(pclases.Usuario)
    #test(pclases.Nota)

