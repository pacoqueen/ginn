#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008 Francisco José Rodríguez Bogado.                    #
#                          (pacoqueen@users.sourceforge.net)                  #
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
# DONE: DateTimeCol, DateCol y FloatCol aparecen como SOCol genérico y no 
# encuentro la forma de distinguirlos para afinar bien la búsqueda global.
# Si llego a resolver eso, hacer un constructor genérico de 
# formularios/ventanas para cualquier objeto recibido será coser y cantar:
# * Si es un IntCol, representar en ventana como entry con función de comparación
#   es_diferente get_text = `valor`, guardar objeto.valor = int(get_text) y 
#   mostrar (rellenar_widgets) set_text(`objeto.valor`)
# * Si es un FloatCol, igual pero usando utils.float2str y utils._float.
# * Si es un Bool, usar un gtk.CheckButton.
# * Si es un Date, usar un entry pero con las funciones str_fecha, parse_fecha
#   y adjuntando un botón "buscar fecha" que lance el utils.mostrar_calendario.
# * Si es un ForeignKey, usar un ComboBoxEntry con utils.rellenar... con las
#   tuplas de la tabla referenciada.
# * Si es un String, prácticamente no hay que hacer nada. Un entry y a correr.
# * Como label de todos ellos se puede usar el col.name.
# * Incluso se puede recorrer la lista de registros que referencian al objeto 
#   en cuestión (ver el sqlmeta.joins de pclases.Clase) y mostrarlos todos en 
#   un TreeView/ListView.
###############################################################################


"""
They call me The Seeker 
I've been searching low and high 
I won't get to get what I'm after 
'till the day I die.
"""

import pygtk
pygtk.require('2.0')
import gtk
import sys, os, pclases
from formularios import utils
import mx.DateTime
from formularios.ventana import Ventana

class Resultado:
    """
    Cada uno de los resultados del buscador es un objeto "Resultado" 
    que encapsula un registro de pclases.
    """
    
    def __init__(self, resultado_pclases):
        """
        Recibe un resultado de pclases (un objeto en realidad) y 
        lo encapsula dentro de un atributo propio.
        """
        self.resultado = resultado_pclases
        self.tabla = resultado_pclases.sqlmeta.table
        self.clase = resultado_pclases.__class__.__name__

    def __repr__(self):
        info = self.resultado.get_info()
        if info == "Información no disponible.": 
            info = self.resultado.__repr__()    # OJO: Hasta que todas las clases hayan redefinido el get_info.
        return info

    def get_id(self):
        """
        Devuelve el ID del objeto encapsulado.
        """
        return self.resultado.id

    def get_class(self):
        """
        Devuelve la clase del objeto de pclases encapsulado.
        """
        return type(self.resultado)

    def get_objeto_pclases(self):
        """
        Devuelve el objeto de pclases en sí.
        """
        return self.resultado

    ide = property(get_id)


class Seeker:
    """
    Un buscador que indaga en todas las clases de "pclases".
    """
    def __init__(self, termino_busqueda = None):
        """
        termino_busqueda es el token a buscar. Si no se recibe, debe 
        instanciarse mediante el método buscar o no podrá usarse el 
        objeto buscador.
        Si se recibe, entonces no es necesario llamar a "buscar" para 
        acceder a los resultados.
        """
        self.token = termino_busqueda
        self.resultados = []
        if self.token != None:
            self.buscar()

    def buscar(self, termino_busqueda = None):
        """
        Busca el término de búsqueda "termino_busqueda" y construye la 
        lista de resultados. Si termino_busqueda es None intentará usar 
        el término de búsqueda ya almacenado. Si éste también es None 
        lanza una excepción ValueError.
        """
        if termino_busqueda != None:
            self.token = termino_busqueda
        if self.token == None:
            raise ValueError, "Debe especificar un término a buscar."
        else:
            self._buscar()

    def _buscar(self):
        """
        Método protegido que realiza la búsqueda en sí.
        Primero recorre la lista de clases derivadas de SQLObject y PRPCTOO, que 
        son las que representan a los objetos de la base de datos en el ORM. 
        Después, para cada una de esas clases hace una búsqueda OR pasando el 
        término a buscar en un .contains (i.e. ILIKE '%término%' en mi versión 
        "custom" de SQLObject). Finalmente, reúne todos los results en una única
        lista de resultados.
        """
        clases = self.__buscar_clases()
        for clase in clases:
            consulta = self.__construir_criterio_consulta(clase)
            if consulta != None:
                resultados_select = clase.select(consulta)
                # print " ---> ", resultados_select.count()
                for resultado_select in resultados_select:
                    resultado = Resultado(resultado_select)
                    self.resultados.append(resultado)
            else:
                # print clase, "Sin campos de texto donde buscar."
                pass

    def __construir_criterio_consulta(self, clase):
        """
        Recibe una clase de pclases y devuelve un objeto 
        que se usará para la consulta en sí. Los criterios 
        se encadenarán con OR y cada uno de ellos será una búsqueda 
        del término de búsqueda en un campo de la clase.
        No chequea que el término de búsqueda esté instanciado.
        """
        criterios = []
        for nombre_campo in clase.sqlmeta.columns.keys():
            query_attr = getattr(clase, "q")
            campo_query = getattr(query_attr, nombre_campo)
            if isinstance(clase.sqlmeta.columns[nombre_campo], pclases.SOStringCol):
                criterio = campo_query.contains(self.token)
            elif isinstance(clase.sqlmeta.columns[nombre_campo], pclases.SOBoolCol): 
                if isinstance(self.token, type(True)):
                    criterio = campo_query == self.token
                else:
                    continue
            elif isinstance(clase.sqlmeta.columns[nombre_campo], pclases.SOForeignKey):
                if isinstance(self.token, type(1)):
                    criterio = campo_query == self.token
                else:
                    continue
            elif isinstance(clase.sqlmeta.columns[nombre_campo], pclases.SOIntCol): 
                try:
                    criterio = campo_query == int(self.token)
                except ValueError:
                    continue
            elif isinstance(clase.sqlmeta.columns[nombre_campo], pclases.SOFloatCol): 
                try:
                    criterio = campo_query == float(self.token)
                except ValueError:
                    continue
            elif isinstance(clase.sqlmeta.columns[nombre_campo], pclases.SODateCol): 
                if self.token.count('/') == 2:
                    dia, mes, anno = self.token.split('/')
                else:
                    dia, mes, anno = self.token[:2], self.token[3:5], self.token[6:]
                try:
                    fecha = mx.DateTime.DateTimeFrom(day = dia, month = mes, year = anno)
                except (ValueError, TypeError):
                    continue
                else:
                    criterio = campo_query == fecha 
            elif isinstance(clase.sqlmeta.columns[nombre_campo], pclases.SOCol):    # Aquí estarían los DateTime con hora (timestamp) 
                continue
            else:
                continue
            criterios.append(criterio)
        if len(criterios) >= 2:
            res = pclases.OR(*criterios)
        elif len(criterios) == 1:
            res = criterios[0]
        else:
            res = None
        return res
                
    def __buscar_clases(self):
        """
        Devuelve una lista de clases del Object Relational Mapper que 
        realmente correspondan a una clase válida en la BD. (Esto es, 
        son derivadas de SQLObject y PRPCTOO).
        """
        res = []
        for clase_str in dir(pclases):
            clase = getattr(pclases, clase_str)
            try:
                if issubclass(clase, pclases.SQLObject) and issubclass(clase, pclases.PRPCTOO): 
                    res.append(clase)
            except TypeError:   # No es una clase. Debe ser una función, no la trato.
                pass
        return res


class VentanaGenerica(Ventana):
    """
    Ventana genérica que se construye dinámicamente dependiendo del 
    objeto que mostrará.
    """

    def __init__(self, clase, objeto = None, usuario = None): 
        """
        Recibe la clase base para construir la ventana.
        Opcionalmente recibe un objeto para mostrar en la misma y 
        el usuario registrado en el sistema.
        Construye la ventana e inicia el bucle Gtk.
        """
        self.usuario = usuario
        self.clase = clase
        self.objeto = objeto
        ventana_marco = os.path.join('..', 'formularios', 'ventana_generica.glade')
        Ventana.__init__(self, ventana_marco, objeto, usuario)
        # Botones genéricos:
        connections = {'b_salir/clicked': self.salir, 
                       'b_actualizar/clicked': self.actualizar_ventana, 
                       'b_nuevo/clicked': self.nuevo, 
                       'b_borrar/clicked': self.borrar, 
                       'b_buscar/clicked': self.buscar, 
                       'b_guardar/clicked': self.guardar 
                      }
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(self.objeto)
        gtk.main()

    # Funciones estándar "de facto":
    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, construyendo 
        los modelos para los TreeView, etc.
        """
        for colname in self.clase.sqlmeta.columns:
            col = self.clase.sqlmeta.columns[colname]
            contenedor, widget = build_widget(col)
            self.wids[col.name] = widget
            self.wids['vbox'].add(contenedor)
        for col in self.clase.sqlmeta.joins:
            contenedor, widget = build_listview(col)
            self.wids[col.joinMethodName] = widget
            self.wids['vbox_relaciones'].add(contenedor)
        self.wids['vbox'].show_all()
        self.wids['b_actualizar'].set_sensitive(False)
        self.wids['b_guardar'].set_sensitive(False)

    def activar_widgets(self, activo = True):
        """
        Activa o desactiva los widgets de la ventana que 
        dependan del objeto mostrado (generalmente todos 
        excepto el botón de nuevo, salir y buscar).
        """
        if self.usuario and self.usuario.nivel >= 2:
            activo = False
        if self.objeto == None:
            activo = False
        excepciones = ["b_nuevo", "b_salir", "b_buscar"]
        for w in excepciones:
            padre = self.wids[w].parent
            while padre != None:
                excepciones += (padre.name, )
                padre = padre.parent
        for w in self.wids.keys():
            if w != 'b_actualizar' and w != 'b_guardar' and w not in excepciones:
                self.wids[w].set_sensitive(activo)

    def es_diferente(self):
        """
        Devuelve True si algún valor en ventana difiere de 
        los del objeto.
        """
        if self.objeto == None:
            igual = True
        else:
            igual = self.objeto != None
            for colname in self.clase.sqlmeta.columns:
                col = self.clase.sqlmeta.columns[colname]
                valor_ventana = self.leer_valor(col)
                valor_objeto = getattr(self.objeto, col.name)
                if isinstance(col, pclases.SODateCol):
                    valor_objeto = utils.abs_mxfecha(valor_objeto)
                igual = igual and (valor_ventana == valor_objeto)
                if not igual:
                    break
        return not igual

    def leer_valor(self, col, nombre_widget = None):
        """
        Lee el valor de la ventana correspondiente al campo 
        "col" y lo trata convenientemente (p.e. convirtiéndolo 
        a float si el tipo de la columna es SOFloatCol) antes 
        de devolverlo.
        Lanza una excepción si ocurre algún error de conversión.
        """
        if nombre_widget == None:
            nombre_widget = col.name
        widget = self.wids[nombre_widget]
        if isinstance(col, pclases.SOStringCol): 
            try:
                valor = widget.get_text()
            except AttributeError:      # Puede ser un TextView
                buff = widget.get_buffer()
                valor = buff.get_text(buff.get_start_iter(), buff.get_end_iter())
        elif isinstance(col, pclases.SOIntCol):
            if isinstance(widget, gtk.SpinButton):
                valor = widget.get_value()
                valor = int(valor)
            else:
                valor = widget.get_text()
                if valor.strip() == "":
                    valor = None
                else:
                    try:
                        valor = int(valor)
                    except Exception, e:
                        if pclases.DEBUG:
                            print "Excepción %s capturada al convertir %s a entero." % (e, valor)
                        raise e
        elif isinstance(col, pclases.SOFloatCol):
            valor = widget.get_text()
            if valor.strip() == "":
                valor = None
            else:
                try:
                    valor = utils._float(valor)
                except Exception, e:
                    # Intento leerlo como euro
                    try:
                        valor = utils.parse_euro(valor)
                    except Exception, e:
                        # Intento leerlo como porcentaje
                        try:
                            valor = utils.parse_porcentaje(valor)
                        except Exception, e:
                            if pclases.DEBUG:
                                print "Excepción %s capturada al convertir %s a flotante." % (e, valor)
                            raise e
        elif isinstance(col, pclases.SOBoolCol):
            valor = widget.get_active()
        elif isinstance(col, pclases.SODateCol):
            valor = widget.get_text()
            try:
                valor = utils.parse_fecha(valor)
            except Exception, e:
                if pclases.DEBUG:
                    print "Excepción %s capturada al convertir %s a fecha." % (e, valor)
                raise e
        elif isinstance(col, pclases.SOForeignKey):
            valor = utils.combo_get_value(widget)
        else:
            # Lo intento como puedo. A lo mejor faltaría intentarlo también como si fuera un TextView.
            if hasattr(widget, "child"):
                valor = widget.child.get_text()
            else:
                valor = widget.get_text()
        return valor
    
    def rellenar_widgets(self):
        """
        Muestra los valores de cada atributo en el widget
        del campo correspondiente.
        """
        if self.objeto != None:
            for colname in self.clase.sqlmeta.columns:
                col = self.clase.sqlmeta.columns[colname]
                valor_objeto = getattr(self.objeto, col.name)
                self.escribir_valor(col, valor_objeto)
            for col in self.clase.sqlmeta.joins:
                self.rellenar_tabla(col)

    def escribir_valor(self, col, valor, nombre_widget = None, precision = 2):
        """
        Muestra el valor "valor" en el widget correspondiente 
        al campo "col", haciendo las transformaciones necesarias
        dependiendo del tipo de datos.
        """
        if nombre_widget == None:
            nombre_widget = col.name
        widget = self.wids[nombre_widget]
        if isinstance(col, pclases.SOStringCol): 
            try:
                widget.set_text(valor)
            except AttributeError:  # Puede ser un TextView
                widget.get_buffer().set_text(valor)
        elif isinstance(col, pclases.SOIntCol):
            if isinstance(widget, gtk.SpinButton):
                widget.set_value(valor)
            else:
                try:
                    if valor != None:
                        valor = str(valor)
                    else:
                        valor = ""
                except Exception, e:
                    if pclases.DEBUG:
                        print "Excepción %s capturada al convertir %s de entero a cadena." % (e, valor)
                    raise e
                widget.set_text(valor)
        elif isinstance(col, pclases.SOFloatCol):
            if valor is None:
                valor = ""
            else:
                try:
                    valor = utils.float2str(valor, precision = precision)
                except Exception, e:
                    if pclases.DEBUG:
                        print "Excepción %s capturada al convertir %s de flotante a cadena." % (e, valor)
                    raise e
            widget.set_text(valor)
        elif isinstance(col, pclases.SOBoolCol):
            widget.set_active(valor)
        elif isinstance(col, pclases.SODateCol):
            try:
                valor = utils.str_fecha(valor)
            except Exception, e:
                if pclases.DEBUG:
                    print "Excepción %s capturada al convertir %s de fecha a cadena." % (e, valor)
                raise e
            widget.set_text(valor)
        elif isinstance(col, pclases.SOForeignKey):
            utils.combo_set_from_db(widget, valor)
        else:
            # Lo intento como puedo. A lo mejor faltaría intentarlo también como si fuera un TextView.
            if hasattr(widget, "child"):
                widget.child.set_text(`valor`)
            else:
                widget.set_text(`valor`)

    def ir_a_primero(self, invertir = True):
        """
        Hace activo el primer objeto de la clase si "invertir" es False.
        Si es True (valor por defecto), el activo es el último objeto 
        creado en la tabla.
        """
        anterior = self.objeto
        try:
            if invertir:
                objeto = self.clase.select(orderBy = "-id")[0]
            else:
                objeto = self.clase.select(orderBy = "id")[0]
            # Anulo el aviso de actualización del objeto que deja de ser activo.
            if self.objeto != None: self.objeto.notificador.desactivar()
            self.objeto = objeto
            self.objeto.notificador.activar(self.aviso_actualizacion)        # Activo la notificación
        except IndexError:
            self.objeto = None
        self.actualizar_ventana(objeto_anterior = anterior)

    def get_valor_defecto(self, col):
        """
        Devuelve un valor por defecto adecuado al tipo de datos de «col».
        """
        if isinstance(col, pclases.SOStringCol): 
            res = "''"
        elif isinstance(col, pclases.SOIntCol):
            res = "0"
        elif isinstance(col, pclases.SOFloatCol):
            res = "0.0"
        elif isinstance(col, pclases.SOBoolCol):
            res = "False"
        elif isinstance(col, pclases.SODateCol):
            res = "mx.DateTime.localtime()"
        elif isinstance(col, pclases.SOForeignKey):
            res = "None"
        else:
            res = "None"
        return res

    def nuevo(self, boton):
        """
        Crea y muestra un nuevo objeto de la clase.
        """
        params = {}
        for colname in self.clase.sqlmeta.columns:
            col = self.clase.sqlmeta.columns[colname]
            params[colname] = self.get_valor_defecto(col)
        cad_params = ", ".join(["%s = %s" % (param, params[param]) for param in params])
        self.objeto = eval("self.clase(%s)" % (cad_params))
        self.actualizar_ventana()

    def buscar(self, boton):
        """
        Pide un texto a buscar y hace activo el resultado 
        de la búsqueda.
        """
        print "Soy buscar"

    def guardar(self, boton):
        """
        Guarda los valores de la ventana en los atributos del objeto.
        """
        for colname in self.clase.sqlmeta.columns:
            col = self.clase.sqlmeta.columns[colname]
            valor_ventana = self.leer_valor(col)
            setattr(self.objeto, colname, valor_ventana)
        self.objeto.syncUpdate()
        self.objeto.sync()
        self.wids['b_guardar'].set_sensitive(False)

    def borrar(self, boton):
        """
        Elimina el objeto activo en ventana y vuelve al último de la tabla.
        """
        if self.objeto != None:
            try:
                self.objeto.destroy(usuario = self.usuario)
            except:
                utils.dialogo_info(titulo = "NO SE PUEDE ELIMINAR", 
                                   texto = "El objeto está relacionado con otros aún activos.", 
                                   padre = self.wids['ventana'])
            else:
                self.ir_a_primero()

    def rellenar_tabla(self, coljoin):
        """
        Introduce los registro de coljoin relacionados 
        en el modelo del listview construido para él.
        """
        model = self.wids[coljoin.joinMethodName].get_model()
        columnas = getattr(coljoin.otherClass, "sqlmeta.columns").keys()
        columnas.append('id')
        model.clear()
        for registro in getattr(self.objeto, coljoin.joinMethodName):
            fila = []
            for columna in columnas:
                fila.append(getattr(registro, columna))
            model.append((fila))

# Utilidades genéricas de widgets
def build_widget(col, label = None):
    """
    A partir de la columna recibida, construye un hbox con 
    dos widgets más. Un label y el widget que mostrará el 
    valor en sí del campo.
    Si "label" es diferente de None, se usará ese como texto, 
    en otro caso se usará el nombre del campo.
    Devuelve el contenedor hbox y el widget asociado al campo en sí.
    """
    if label == None:
        label = col.name
    hbox = gtk.HBox()
    wlabel = gtk.Label(label)
    hbox.add(wlabel)
    wvalor, contenedor = build_widget_valor(col)
    if contenedor != None:
        hbox.add(contenedor)
    else:
        hbox.add(wvalor)
    hbox.show_all()
    return hbox, wvalor

def build_widget_valor(col):
    """
    Recibe un objeto de la familia SOCol y devuelve el 
    widget adecuado para mostrar su valor.
    Si es un texto, entero o float: entry.
    Si es un boolean: checkbutton.
    Si es una fecha: entry con un botón para mostrar el calendario.
    Si es un ForeignKey, usar un ComboBoxEntry con utils.rellenar... con las
    tuplas de la tabla referenciada.
    """
    box = None  # Posible contenedor externo.
    if isinstance(col, pclases.SOStringCol): 
        w = gtk.Entry()
        w.set_name(col.name)
    elif isinstance(col, pclases.SOIntCol):
        w = gtk.Entry()
        w.set_name(col.name)
    elif isinstance(col, pclases.SOFloatCol):
        w = gtk.Entry()
        w.set_name(col.name)
    elif isinstance(col, pclases.SOBoolCol):
        w = gtk.CheckButton()
        w.set_name(col.name)
    elif isinstance(col, pclases.SODateCol):
        box = gtk.HBox()
        w = gtk.Entry()
        w.set_name(col.name)
        button = gtk.Button(label = "Buscar _fecha")
        button.connect("clicked", lambda boton: w.set_text(utils.str_fecha(utils.mostrar_calendario())))
        button.set_name("b_%s" % (col.name))
        box.add(w)
        box.add(button)
    elif isinstance(col, pclases.SOForeignKey):
        w = gtk.ComboBoxEntry()
        w.set_name(col.name)
        tablajena = col.foreignKey
        clase_tablajena = getattr(pclases, tablajena)
        func_select = getattr(clase_tablajena, "select")
        datos = []
        for reg in func_select():
            campos = []
            for columna in clase_tablajena.sqlmeta.columns:
                valor = getattr(reg, columna)
                campos.append(`valor`)
            info = ", ".join(campos)
            # info = reg.get_info()
            datos.append((reg.id, info))
        utils.rellenar_lista(w, datos)
    else:
        w = gtk.Entry()
        w.set_name(col.name)
    return w, box

def build_listview(coljoin):
    """
    Construye un listview y su modelo para albergar los 
    datos relacionados a través de la columna "uno-a-muchos" «col».
    """
    columnas = getattr(coljoin.otherClass, "sqlmeta.columns").keys()
    cols = []
    for col in columnas:
        nombre = col.title()
        tipo = "gobject.TYPE_STRING"
        cols.append([nombre, tipo, False, True, False, None])
    cols[0][4] = True   # Búsqueda interactiva en la primera columna.
    cols.append(["ID", "gobject.TYPE_INT64", False, False, False, None])
    treeview = gtk.TreeView()
    utils.preparar_listview(treeview, cols)
    despl = gtk.ScrolledWindow()
    despl.add(treeview)
    label = gtk.Label(coljoin.otherClassName)
    contenedor = gtk.HBox()
    contenedor.add(label)
    contenedor.add(despl)
    #contenedor.add(treeview)
    contenedor.show_all()
    return contenedor, treeview
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        buscador = Seeker()
        buscador.buscar(sys.argv[1])
        print len(buscador.resultados), "resultados encontrados. Muestro el primero de todos."
        # for resultado in buscador.resultados: 
        #     print resultado.id
        clase_objeto_resultado = getattr(pclases, buscador.resultados[0].clase)
        objeto_resultado = clase_objeto_resultado.get(buscador.resultados[0].id)
        v = VentanaGenerica(objeto_resultado)
    else:
        v = VentanaGenerica(pclases.DatosDeLaEmpresa)
