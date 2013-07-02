#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado,                   #
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


###################################################################
## tarifas.py - Define precios de productos para cada tarifa. 
###################################################################
## NOTAS:
## 
###################################################################
## Changelog:
##  6 Julio 2005 -> Inicio
##    (Ver ProjectManager Geotex-Inn para changelog completo)
##  1 Septiembre 2005 -> 100% funcional  
## 29 de enero de 2006 -> Portado a versión 0.2
## 19 de diciembre de 2006 -> Añadido soporte a tarificar productos 
##                            de compra.
###################################################################
## DONE:
##  + Todavía me falta actualizar en caso de cambio "remoto" en la
##    tarifa actual. (Hasta ahora lo hago avisando al usuario).
##    DONE: Y así se va a quedar me parece a mí. Es bastante 
##    usable y no creo que sea mucha molestia para el usuario.
##  + Al crear una nueva tarifa en un puesto remoto... ¿cómo la 
##    hago aparecer en el combo "local"? -> Mediante el Actualizar.
##    DONE pero poco. Vale que mediante el actualizar se haga, pero
##    es que el actualizar no se activa hasta que no cambie la 
##    tarifa mostrada. A ver cómo hago aparecer entonces las nuevas
##    inserciones.
##   PLAN:
##    Podría hacerlo reconsultando los datos del model cada vez que
##    se cambie de tarifa, por ejemplo. O creando nuevas 
##    notificaciones de inserción (también podría aprovechar para
##    crear notificaciones en tarifas_productos y así avisar de 
##    los cambios en los productos de la tarifa), etcétera.
##    Son cambios menores, los dejaré para más adelante.
##  + Sigue pendiente el bug del "select" al salir del programa.
##    DONE también. Era problema de relanzar el hilo cuando el 
##    objeto en realidad ya no estaba en memoria; quedaba como un
##    unbound method de NoneType.select... un follonaco, vamos.
##  + Mejorar usabilidad (por ejemplo, habilitando y deshabilitando
##    los botones guardar y actualizar según sea necesario). DONE.
##  + OJO: ¡NO hay modo de avisar de nuevas inserciones de tarifas!
##  + Antes de fiarte más de gobject, ¿HAY gobject EN WINDOWS? 
##    Mira que son objetos de GNOME directamente... Lo hay, 
##    of course, son parte de la biblioteca GTK.
##  + FLI-PA: Nuevo problema. Se avisa del cambio AUNQUE SEA EN UN
##    OBJETO DISTINTO AL MOSTRADO EN PANTALLA. Estoy a punto de 
##    echarme a llorar.  -> DONE por fin. Ahora asigno la función
##    del notificador y lo anulo (=lambda:None) cada vez que cambio
##    la tarifa mostrada en pantalla.
##  + DONE: Ya casi lo único que falta es hacer un esqueleto con 
##    este formulario para que todos sean prácticamente iguales 
##    (por lo menos en el modo de funcionar).
##  + DONE: ¡ RETABULAR con soft tabs de 4 espacios !
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk, gobject
from framework import pclases
from informes import geninformes
import mx.DateTime

from formularios.pedidos_de_venta import NIVEL_VALIDACION

class TarifasDePrecios(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'tarifas_de_precios.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_nueva_tarifa/clicked': self.crear_nueva_tarifa,
                       'b_anadir_producto_tarifa/clicked': 
                            self.annadir_producto_a_tarifa,
                       'b_borrar_producto_tarifa/clicked': 
                            self.borrar_producto_de_tarifa,
                       'b_borrar_tarifa/clicked': self.borrar_tarifa_actual,
                       'cb_nombre_tarifa/changed': self.seleccionar_tarifa,
                       'b_cambiar_nombre_tarifa/clicked': 
                            self.cambiar_nombre_tarifa,
                       'b_actualizar/clicked': self.actualizar,
                       'b_guardar/clicked': self.guardar,
                       'b_imprimir/clicked': self.imprimir, 
                       'b_periodo_validez_ini/clicked': self.set_validez, 
                       'b_periodo_validez_fin/clicked': self.set_validez
                      }  
        self.add_connections(connections)
        self.inicializar_ventana()
        gtk.main()

    def set_validez(self, boton):
        """
        Muestra un diálogo de selecciónde fecha y 
        escribe la fecha elegida en el Entry 
        correspondiente.
        """
        entry = boton.name.replace("b", "e")
        fecha = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids[entry].set_text(utils.str_fecha(fecha))

    def imprimir(self, boton):
        """
        Imprime la tarifa en pantalla.
        """
        from formularios import reports
        datos = []
        model = self.wids['tabla_productos'].get_model()
        for itr in model: 
            datos.append((itr[0], 
                          itr[1], 
                          "%s €" % (utils.float2str(itr[2], 3)), 
                          "%s €" % (utils.float2str(itr[3], 3))
                        ))
        def cmp_func(x, y):
            """
            Para ordenar por nombre de producto.
            """
            if x[1] < y[1]:
                return -1
            if x[1] > y[1]:
                return 1
            return 0
        datos.sort(cmp_func)
        if datos != []:
            nombre_tarifa = self.wids['cb_nombre_tarifa'].child.get_text()
            reports.abrir_pdf(geninformes.imprimir_tarifa(datos, nombre_tarifa, utils.str_fecha(mx.DateTime.localtime())))

    def act(self):
#        utils.dialogo_info('ACTUALIZAR', 'El objeto ha sido modificado remotamente.\nDebe actualizar la información mostrada en pantalla. Pulse el botón «Actualizar».', padre = self.wids['ventana'])
        # Habilito el botón actualizar para que pueda pulsarlo:
        self.wids['b_actualizar'].set_sensitive(True)

    ## ---------------- Funciones auxiliares ---------------------------------
    def activar_widgets(self, s):
        """ Activa o desactiva (sensitive=True/False) todos
        los widgets de la ventana.
        Entrada: s debe ser True o False. En todo caso se 
        evaluará como boolean."""
        ws = ('tv_descripcion_tarifa', 'b_cambiar_nombre_tarifa',
              'tabla_productos', 'b_anadir_producto_tarifa',
              'b_borrar_producto_tarifa', 'b_borrar_tarifa', 
              "b_periodo_validez_ini", "b_periodo_validez_fin", 
              "e_periodo_validez_ini", "e_periodo_validez_fin")
        for w in ws:
            self.wids[w].set_sensitive(s)
        if self.usuario and self.usuario.nivel >= 2:
            self.wids['b_nueva_tarifa'].set_sensitive(False)
            self.wids['b_anadir_producto_tarifa'].set_sensitive(False)
            self.wids['b_borrar_producto_tarifa'].set_sensitive(False)
            self.wids['b_borrar_tarifa'].set_sensitive(False)
            self.wids['b_cambiar_nombre_tarifa'].set_sensitive(False)
            self.wids['b_guardar'].set_sensitive(False)
            col = self.wids['tabla_productos'].get_column(3)
            for cell in col.get_cell_renderers():
                cell.set_property("editable", False)
                # cell.connect("edited", lambda c, p, n: None)

    def rellenar_lista(self, wid, textos):
        """ Crea, rellena y asocia al model de un combobox
        el ListStore que se creará a partir de una lista o
        tupla de (enteros,cadenas)."""
        model = gtk.ListStore(int, str)
        for t in textos:
            model.append(t)
        cb = wid
        cb.set_model(model)
        
        if type(cb) == gtk.ComboBoxEntry:
            if cb.get_text_column()==-1:    # MORON HACK: Para evitar un 
                cb.set_text_column(1)       # "assert - GtkWarning"
            completion = gtk.EntryCompletion()
            completion.set_model(model)
            wid.child.set_completion(completion)
            completion.set_text_column(1)
            #completion.set_minimum_key_length(2)
        elif type(cb) == gtk.ComboBox:
            cell = gtk.CellRendererText()
            cb.pack_start(cell, True)
            cb.add_attribute(cell, 'text',1)

    def rellenar_tarifas(self, wid, ir_a_primera=True):
        """ Inserta las tarifas de la BD en el widget pasado.
        wid debe ser un combo o un widget con ListStore.
        Devuelve la primera tarifa o None si no hay ninguna.
        Si "ir_a_primera" es True, se mueve a la primera 
        tarifa de todas, en caso contrario devuelve None y
        deja el ítem activo tal como estaba antes de la llamada.
        """
        # Primero obtengo los nombres e id de todas las tarifas
        ts = pclases.Tarifa.select(orderBy = 'nombre')
        if ts.count() == 0:
            self.activar_widgets(False)
            return None
        self.activar_widgets(True)
        self.rellenar_lista(wid, [(t.id, t.nombre) for t in ts])
        if ir_a_primera:
            wid.set_active(0)
            temp = ts[0]
        else:
            temp = None
        del ts
        return temp

    def insertar_tarifa_en_lista(self, tarifa):
        m =  self.wids['cb_nombre_tarifa'].get_model()
        if m == None:
            self.rellenar_lista(self.wids['cb_nombre_tarifa'], [[tarifa.id, tarifa.nombre]])
            # rellenar_lista crea el model y añade los items de la lista pasada.
        else:
            # Si el model ya existe (no es None) añado la tarifa creada:
            m.append([tarifa.id, tarifa.nombre])
     
    def borrar_tarifa_de_lista(self, tarifa):
        m = self.wids['cb_nombre_tarifa'].get_model()
        itr = m.get_iter_first()
        while itr != None:
            if m.get(itr, 0)[0] == tarifa.id:
                # model.get devuelve una tupla de valores de columnas.
                m.remove(itr)
                break     # No sigo recorriendo. Sólo elimino el primero y 
                        # me ahorro el resto del recorrido.
            itr = m.iter_next(itr)

    def buscar_indice_texto(self, combo, texto):
        """ No tengo mucho tiempo que perder. Hasta que encuentre
        el método que haga esto (¿por qué son tan retorcidos los
        diseñadores de GTK?) moveré el índice del combobox hasta
        encontrar el texto pasado.
        Devuelve el índice del texto dentro del ListStore del combo.
        Si el texto no se encuentra, devuelve -1.
        Si hay dos textos idénticos, devuelve el índice del primero
        de ellos.
        OJO: Esto PUEDE pasar. El UNIQUE es el id. Como al luser se
        le ocurra poner el mismo nombre a dos tarifas se caga la perra.
        """
        m = combo.get_model()
        itr = m.get_iter_first()
        i=0
        while itr!=None and m[i][1]!=texto:
            i+=1
            itr = m.iter_next(itr)
        if itr==None: return -1
        else: return i

    def actualizar_ventana(self):
        """
        Actualiza los widgets de la ventana en función a la tarifa 
        actual SIN recurrir directamente al objeto Tarifa. En su 
        lugar, mueve el índice del combo; con lo cual relee la 
        tarifa de la BD. Es por tanto imprescindible que todos los
        cambios que se hagan a los datos queden guardados antes de
        actualizar la ventana.
        """
        index = self.wids['cb_nombre_tarifa'].get_active()
        self.wids['cb_nombre_tarifa'].set_active(-1)
        self.wids['cb_nombre_tarifa'].set_active(index)

    def rellenar_widgets(self):
        """
        Muestra los datos de la tarifa en los widgets del
        formulario.
        """
        tarifa = self.objeto
        self.activar_widgets(tarifa!=None)
        if tarifa!=None:
            # Primero borro los datos que hubiera:
            self.limpiar_ventana()
            # Y ahora meto los que corresponden:
            try:
                self.wids['tv_descripcion_tarifa'].get_buffer().set_text(
                    tarifa.observaciones)
            except TypeError:
                self.wids['tv_descripcion_tarifa'].get_buffer().set_text('')
            m = self.wids['tabla_productos'].get_model()
            self.wids['tabla_productos'].freeze_child_notify()
            self.wids['tabla_productos'].set_model(None)
            precios = [p for p in tarifa.precios]
            precios.sort()
            for p in precios:
                producto = p.producto
                if hasattr(producto, "obsoleto") and producto.obsoleto:
                    continue
                try:
                    porcentaje = 100*((p.precio/producto.preciopordefecto)-1)
                except ZeroDivisionError:
                    porcentaje = 0
                m.append([producto.codigo, 
                          producto.descripcion, 
                          producto.preciopordefecto, 
                          p.precio, 
                          "%s %%" % (utils.float2str(porcentaje, 1)), 
                          p.id])
            self.wids['tabla_productos'].set_model(m)
            self.wids['tabla_productos'].thaw_child_notify()
            self.wids['e_periodo_validez_ini'].set_text(
                utils.str_fecha(tarifa.periodoValidezIni))
            self.wids['e_periodo_validez_fin'].set_text(
                utils.str_fecha(tarifa.periodoValidezFin))
            self.objeto.make_swap()
            self.rellenar_precio_minimo()

    def rellenar_precio_minimo(self):
        # Precios mínimos
        model = self.wids['tv_precio_minimo'].get_model()
        try:
            model.clear()
            for l in pclases.LineaDeProduccion.select(orderBy = "id"):
                strfamilia = l.nombre
                if l.nombre.startswith("Línea de"):
                    strfamilia = strfamilia.replace("Línea de", "")
                if l.precioMinimo != None:
                    strprecioMinimo = utils.float2str(l.precioMinimo)
                else:
                    strprecioMinimo = ""
                model.append((strfamilia, strprecioMinimo, l.puid))
        except AttributeError:
            return  # Todavía no se ha creado el TV.
        self.wids['tv_precio_minimo'].set_sensitive(
                self.usuario and self.usuario.nivel <= NIVEL_VALIDACION 
                or False)
  
    def inicializar_ventana(self):
        """ Prepara los widgets del formulario. Esto sólo debe 
        hacerse una vez, al crear la ventana."""
        # Por defecto, tanto los botones Actualizar como Guardar están 
        # deshabilitados. Ya se habilitarán cuando necesite el usuario:
        self.wids['b_actualizar'].set_sensitive(False)
        self.wids['b_guardar'].set_sensitive(False)
        ## ------------------------ TABLA -------------------------------------
        # Preparo el ListStore de la tabla:
        treest = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING, 
                               gobject.TYPE_FLOAT, gobject.TYPE_FLOAT, 
                               gobject.TYPE_STRING, gobject.TYPE_INT)
            # Los campos serán: código, descripción, precio por defecto y precio para la tarifa)
        self.wids['tabla_productos'].set_model(treest)
        # Creo tantas columnas como campos se van a mostrar:
        columns = []
        columns.append(gtk.TreeViewColumn('Código'))
        columns.append(gtk.TreeViewColumn('Descripción'))
        columns.append(gtk.TreeViewColumn('Precio costo por defecto'))
        columns.append(gtk.TreeViewColumn('Precio tarifa'))
        columns.append(gtk.TreeViewColumn('Porcentaje'))
        # Añado las columnas a la tabla:
        for c in columns:
            self.wids['tabla_productos'].append_column(c)
        columns.append(gtk.TreeViewColumn('precioID'))
        # Creo los "renders" para las celdas, los añado a las columnas y los asocio:
        cells = []
        for i in xrange(len(columns) - 1):
            cells.append(gtk.CellRendererText())
            columns[i].pack_start(cells[i], True)
            columns[i].add_attribute(cells[i], 'text', i)
        # La última columna (precio para la tarifa) debe ser editable:
        cells[-1].set_property("editable", True)
        cells[-2].set_property("editable", True)
        # Y conectar la edición con un manejador:
        cells[-1].connect("edited", self.actualizar_porcentaje_tarifa)
        cells[-2].connect("edited", self.actualizar_precio_tarifa)
        # Defino la columna de búsqueda:
        self.wids['tabla_productos'].set_search_column(1)
        # Y hago que se pueda ordenar por código, nombre o precio por defecto:
        columns[0].set_sort_column_id(0)
        columns[1].set_sort_column_id(1)
        columns[2].set_sort_column_id(2)
        columns[3].set_sort_column_id(3)
        columns[4].set_sort_column_id(4)
        self.wids['tabla_productos'].get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        # WTF? Vaya chorizo de función.
        cols = self.wids['tabla_productos'].get_columns()
        for i in (2, 3):
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell,
                    utils.redondear_flotante_en_cell_cuando_sea_posible, 
                    (i, 3))
  
        ## ----------------------- COMBO BOX ---------------------------------
        tarifa = self.rellenar_tarifas(self.wids['cb_nombre_tarifa'])
        # Al rellenar las tarifas del combo ya se selecciona la primera
        # automáticamente, así que aprovecho para asignarla.
        # Y desactivo los widgets si no hay ninguna:
        self.activar_widgets(tarifa != None)
        ## Precio mínimo por "familia"
        cols = (("Familia", "gobject.TYPE_STRING", False, True, True, None), 
                ("Precio mínimo por kg", "gobject.TYPE_STRING", 
                    True, True, False, self.cambiar_precio_minimo), 
                ("puid", "gobject.TYPE_STRING", False, False, False, None))
        utils.preparar_listview(self.wids['tv_precio_minimo'], cols)
        cell = self.wids['tv_precio_minimo'].get_column(1).get_cell_renderers()[0]
        cell.set_property("xalign", 1.0)
        self.wids['notebook1'].set_current_page(1)
        self.rellenar_widgets()

    def cambiar_precio_minimo(self, cell, path, texto):
        if texto.strip() == "":
            precio = None
        else:
            try:
                precio = utils._float(texto)
            except:
                return
        model = self.wids['tv_precio_minimo'].get_model()
        ldp = pclases.getObjetoPUID(model[path][-1])
        antes = ldp.precioMinimo
        ldp.precioMinimo = precio
        pclases.Auditoria.modificado(ldp, self.usuario, __file__, 
            "Precio mínimo de %s cambiado de %s a %s" % (
                ldp.nombre, antes, ldp.precioMinimo))
        self.rellenar_precio_minimo()
  
    def limpiar_ventana(self):
        """ 
        Limpa todos los widgets de la ventana, EXCEPTO 
        el del nombre de la tarifa, ya que al cambiar éste
        cambia el contenido del formulario y la selección 
        de la propia tarifa actual, metiéndose esto en un
        bucle infinito de limpiar-rellenar-limpiar-... que
        podría acabar EN UNA PARADOJA TEMPORAL. 
        
        O algo peor.
        
        Que sí, que lo he visto en futurama y puede pasar.
        """
        self.wids['tv_descripcion_tarifa'].get_buffer().set_text('')
        self.wids['tabla_productos'].get_model().clear()

    ## ---------------- Manejadores de eventos -------------------------------
    def guardar(self, button):
        """
        Actualiza la información del objeto respecto a la 
        mostrada en pantalla. Guarda todos los datos de
        la ventana en el objeto persistente (y por tanto
        en la base de datos).
        """
        ## NOTAS: A ver, vamos por orden. Campos que tiene una tarifa:
        ## - Nombre -> Se guarda automáticamente con el botón "Cambiar nombre"
        ## - Descripción -> Hay que guardarlo en esta función.
        ## - Identificador -> Es automático y ni lo muestro. No se puede 
        ##                    cambiar.
        ## - Productos asociados -> Se añaden y eliminan con sus botones correspondientes.
        tarifa = self.objeto
  
        # Desactivo notificador:
        tarifa.notificador.set_func(lambda : None)
        
        # Guardo cambios:
        ## Por tanto, sólo hay que guardar los cambios en la descripción:
        buff = self.wids['tv_descripcion_tarifa'].get_buffer()
        texto=buff.get_text(buff.get_bounds()[0], buff.get_bounds()[1])
        tarifa.observaciones=texto
        try:
            periodoValidezIni = utils.parse_fecha(self.wids['e_periodo_validez_ini'].get_text())
        except:
            periodoValidezIni = None
        tarifa.periodoValidezIni = periodoValidezIni
        try:
            periodoValidezFin = utils.parse_fecha(self.wids['e_periodo_validez_fin'].get_text())
        except:
            periodoValidezFin = None
        tarifa.periodoValidezFin = periodoValidezFin
        if tarifa.periodoValidezIni != None and tarifa.periodoValidezFin != None and tarifa.periodoValidezIni > tarifa.periodoValidezFin:
            tarifa.periodoValidezIni, tarifa.periodoValidezFin = tarifa.periodoValidezFin, tarifa.periodoValidezIni
        tarifa.syncUpdate()  # Por probare.
  
        self.actualizar(None)
        # Y vuelvo a activar el notificador:
        tarifa.notificador.set_func(self.act)
        # Y por último deshabilito el botón hasta que el usuario lo vuelva a necesitar
        self.wids['b_guardar'].set_sensitive(False)

    def actualizar(self, button):
        """ 
        Actualiza la información mostrada en pantalla a partir
        de la guardada en el objeto. Machaca los datos que 
        no estén guardados o difieran entre la ventana y el 
        objeto. Si el registro ha sido borrado se deshabilitan
        los controles de información para que el usuario se
        mueva a otra tarifa.
        """
        tarifa = self.objeto
        try:
            tarifa.sync()
            # Por si se ha creado alguna nueva, actualizo la lista de tarifas
            # pero no asigno la que devuelve, para no machacar la actual:
            self.rellenar_tarifas(self.wids['cb_nombre_tarifa'], False)
            index = self.buscar_indice_texto(self.wids['cb_nombre_tarifa'], tarifa.nombre) 
            self.wids['cb_nombre_tarifa'].child.set_text('')
            self.wids['cb_nombre_tarifa'].set_active(-1)
            self.wids['cb_nombre_tarifa'].set_active(index)
        except pclases.SQLObjectNotFound:
            utils.dialogo_info('Tarifa borrada.', 'La tarifa no existe o ha sido eliminada.')
            tarifa = self.rellenar_tarifas(self.wids['cb_nombre_tarifa'])
        # Y finalmente, deshabilito el botón (puesto que presumiblemente no deberá usarlo
        # a no ser que remotamente se modifique el objeto, en cuyo caso ya se lo habilitaré
        # yo al usuario)
        self.wids['b_actualizar'].set_sensitive(False)

    def actualizar_porcentaje_tarifa(self, celleditable, path, nuevotexto):
        """
        Se recibe la celda que ha cambiado.
        El contenido se toma como nuevo precio para la tarifa
        actual y el producto de la fila a la que pertenezca
        la fila.
        """
        idprecio = self.wids['tabla_productos'].get_model()[path][-1]
        precio = pclases.Precio.get(idprecio)
        producto = precio.producto
        tarifa = self.objeto
            # OJO: No se debería devolver ni más ni menos de un producto.
        try:
            porcentaje = utils.parse_porcentaje(nuevotexto, True)
        except ValueError:
            utils.dialogo_info(titulo = 'VALOR INCORRECTO', 
                               texto = 'El texto tecleado (%s) no es un porcentaje correcto' % (nuevotexto), 
                               padre = self.wids['ventana'])
        else:
            nuevoprecio = producto.preciopordefecto * (1 + porcentaje)
            tarifa.asignarTarifa(producto, float(nuevoprecio))
            #self.actualizar_ventana()
            model = self.wids['tabla_productos'].get_model()
            model[path][-3] = precio.precio
            model[path][-2] = "%s %%" % (porcentaje * 100)

    def actualizar_precio_tarifa(self, celleditable, path, nuevotexto):
        """
        Se recibe la celda que ha cambiado.
        El contenido se toma como nuevo precio para la tarifa
        actual y el producto de la fila a la que pertenezca
        la fila.
        """
#        codigo = self.wids['tabla_productos'].get_model()[path][0]
#        producto = pclases.ProductoVenta.selectBy(codigo=codigo)[0]
        idprecio = self.wids['tabla_productos'].get_model()[path][-1]
        precio = pclases.Precio.get(idprecio)
        producto = precio.producto
        tarifa = self.objeto
            # OJO: No se debería devolver ni más ni menos de un producto.
        try:
            tarifa.asignarTarifa(producto, float(nuevotexto))
        except ValueError:
            utils.dialogo_info(titulo = 'VALOR INCORRECTO', 
                               texto = 'Debe introducir un número usando el punto (.) como separador decimal.', 
                               padre = self.wids['ventana'])
        self.actualizar_ventana()

    def borrar_producto_de_tarifa(self, event):
        model = self.wids['tabla_productos'].get_model()
        for path in self.wids['tabla_productos'].get_selection().get_selected_rows()[1]:
        # get_selected_rows devuelve una lista con el TreeView como primer elemento y los paths de las filas seleccionadas en otra lista como segundo (posición 1) elemento.
            idprecio = model[path][-1]
            precio = pclases.Precio.get(idprecio)
            precio.destroy(ventana = __file__)
        self.actualizar_ventana()

    def seleccionar_tarifa(self, combo):
        if combo.get_active()==-1:
            pos=self.buscar_indice_texto(combo, combo.get_active_text())
        else:
            pos=combo.get_active()
        if pos>=0:    # Tenemos una tarifa válida en el combo:
            # Obtengo el identificador a partir del model
            ide = combo.get_model()[pos][0]    # La columna 0 es el ide.
            # Y finalmente la tarifa actual:
            tarifa = self.objeto
            try:
                if tarifa != None:
                    tarifa.notificador.set_func(lambda : None)
                tarifa=pclases.Tarifa.get(ide)
                # Por si acaso ya estaba en memoria (devuelve entonces el mismo
                # objeto sin volver a pedir datos a la BD), sincronizo y me 
                # aseguro que trae información actualizada:
                tarifa.sync()
                # Y activo la función de notificación:
                tarifa.notificador.set_func(self.act)
            except:
                print "ERROR: Ocurrió un error al cargar la tarifa. ¿Existe el ide %d?" %ide
            self.objeto = tarifa
            self.rellenar_widgets()

    def cambiar_nombre_tarifa(self, event):
        nombre = utils.dialogo_entrada('Introduzca el nuevo nombre para la tarifa:')
        if nombre != None:
            tarifa = self.objeto
            try:
                tarifa.nombre = nombre
            finally:
                index = self.wids['cb_nombre_tarifa'].get_active()
                model = self.wids['cb_nombre_tarifa'].get_model()
                model[index] = [tarifa.id, tarifa.nombre]
                self.wids['cb_nombre_tarifa'].set_active(-1)
                self.wids['cb_nombre_tarifa'].set_active(index)

    def crear_nueva_tarifa(self, event):
        nombre = utils.dialogo_entrada("Nombre de la nueva tarifa:")
        if nombre != None:
            tarifa = self.objeto
            tarifa = pclases.Tarifa(nombre=nombre, observaciones='', periodoValidezIni = None, periodoValidezFin = None)
            pclases.Auditoria.nuevo(tarifa, self.usuario, __file__)
            self.insertar_tarifa_en_lista(tarifa)
            self.wids['cb_nombre_tarifa'].set_active(self.buscar_indice_texto(self.wids['cb_nombre_tarifa'], tarifa.nombre))
            self.seleccionar_tarifa(self.wids['cb_nombre_tarifa'])
            self.objeto = tarifa

    def borrar_tarifa_actual(self, event):
        """ Debe -si el usuario lo confirma- borrar 
        la tarifa actual y sus relaciones con los 
        productos."""
        if utils.dialogo('¿Eliminar tarifa?'):
            tarifa = self.objeto
            for p in tarifa.precios:
                p.destroy(ventana = __file__)
            self.borrar_tarifa_de_lista(tarifa)
            tarifa.notificador.set_func(lambda : None)
            tarifa.destroy(ventana = __file__)
            # Ahora me muevo a la primera de las tarifas o a None si no hay:
            m = self.wids['cb_nombre_tarifa'].get_model() 
            if len(m)==0:
                self.limpiar_ventana()
                self.wids['cb_nombre_tarifa'].child.set_text('')
                self.wids['cb_nombre_tarifa'].set_active(-1)
                tarifa = None
            else:
                tarifa = pclases.Tarifa.get(m[0][0]) # m[0][0] -> id de la primera fila
                self.wids['cb_nombre_tarifa'].set_active(0)
            self.objeto = tarifa
            self.activar_widgets(tarifa != None)

    def annadir_producto_a_tarifa(self, event):
        """ 
        Solicita un producto mediante su código, ide o descripción.
        Una vez seleccionado el producto, se asocia el objeto que
        lo representa con la tarifa actual mostrada en pantalla y 
        se actualiza la información de la ventana.
        NOTA: Si el producto ya está en la tarifa, se actualiza 
        con el precio por defecto del producto.
        """
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR PRODUCTO", 
                                         texto = "Introduzca texto a buscar: ", 
                                         padre = self.wids['ventana'])
        if a_buscar != None:
            criterio = pclases.OR(
                pclases.ProductoVenta.q.codigo.contains(a_buscar),
                pclases.ProductoVenta.q.descripcion.contains(a_buscar))
            resultados_pv = pclases.ProductoVenta.select(criterio)
            criterio = pclases.OR(
                pclases.ProductoCompra.q.codigo.contains(a_buscar),
                pclases.ProductoCompra.q.descripcion.contains(a_buscar))
            resultados_pc = pclases.ProductoCompra.select(pclases.AND(
                pclases.ProductoCompra.q.obsoleto == False, 
                criterio))
            numresultados = resultados_pv.count() + resultados_pc.count()
            if numresultados > 1:
                ## Refinar los resultados:
                filas_res = []
                for r in resultados_pv:
                    filas_res.append(("PV:%d" % r.id, r.codigo, r.descripcion))
                for r in resultados_pc:
                    filas_res.append(("PC:%d" % r.id, r.codigo, r.descripcion))
                idsproducto = utils.dialogo_resultado(filas_res, 
                                                      'Seleccione producto', 
                                                      multi = True, 
                                                      padre = self.wids['ventana'])
                if idsproducto != [-1]:
                    # No ha cancelado.
                    productos = []
                    for tipo_id in idsproducto:
                        tipo, ide = tipo_id.split(":")
                        ide = int(ide)
                        if tipo == "PC":
                            productos.append(pclases.ProductoCompra.get(ide))
                        elif tipo == "PV": 
                            productos.append(pclases.ProductoVenta.get(ide))
                else:
                    productos = []
            elif numresultados == 1:
                if resultados_pc.count() == 1:
                    productos = resultados_pc
                elif resultados_pv.count() == 1:
                    productos = resultados_pv
                else:
                    productos = []
            else:
                ## La búsqueda no produjo resultados.
                utils.dialogo_info('SIN RESULTADOS', 'La búsqueda no produjo ningún resultado.\nIntente una búsqueda menos restrictiva usando un texto más corto.', padre = self.wids['ventana'])
                return
            tarifa = self.objeto
            for producto in productos:
                try:
                    defecto = producto.preciopordefecto
                except AttributeError:
                    defecto = producto.precioDefecto
                tarifa.asignarTarifa(producto, defecto)
            self.actualizar_ventana()

    def es_diferente(self):
        """ Comprueba si los datos en pantalla y los del objeto
        son diferentes. En ese caso activará el botón de guardar.
        Esta función está pensada para ser usada con el 
        gobject.timeout de forma que se compruebe aproximadamente
        cada segundo si hay cambios. La opción de guardarlos queda
        a elección del usuario."""
        ## Datos a comprobar: Únicamente los que no se guardan directamente.
        ## En el caso de las tarifas es sólo la descripción.
        tarifa = self.objeto
        if tarifa == None: return False
        buff = self.wids['tv_descripcion_tarifa'].get_buffer()
        texto=buff.get_text(buff.get_bounds()[0], buff.get_bounds()[1])
        condicion = tarifa.observaciones == texto
        condicion = condicion and utils.str_fecha(tarifa.periodoValidezIni) == self.wids['e_periodo_validez_ini'].get_text()
        condicion = condicion and utils.str_fecha(tarifa.periodoValidezFin) == self.wids['e_periodo_validez_fin'].get_text()
        return not condicion


if __name__ == '__main__':
    v = TarifasDePrecios()

