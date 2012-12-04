#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado,                   #
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

###################################################################
## crm_seguimiento_impagos.py - Gestión de facturas impagadas.
###################################################################
## NOTAS:
## 
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade
try:
    import pclases
except ImportError:
    import sys
    from os.path import join as pathjoin
    sys.path.append(pathjoin("..", "framework"))
    import pclases
import mx, mx.DateTime
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes
import pclase2tv

# from crm_detalles_factura import colorear_tv_alarmas # CWT: Solo blanco/rojo
def colorear_tv_alarmas(tv):
    def cell_func(column, cell, model, itr):
        color = None
        id = model[itr][-1]
        try:
            alarma = pclases.Alarma.get(id)
        except pclases.SQLObjectNotFound:
            #model.remove(itr) <- Da muchos problemas. Ya se actualizará 
                            # la ventana después.
            cell.set_property("cell-background", "grey")
            return #La alarma se ha podido anular desde la ventana de detalles.
        ahora = mx.DateTime.localtime()
        if (alarma.fechahoraAlarma <= ahora):
            color = "red"   # En rojo las que han pasado.
        else: 
            color = None    # En "blanco" (color del theme en realidad) resto.
        cell.set_property("cell-background", color)
    cols = tv.get_columns()
    for col in cols:
        for cell in col.get_cell_renderers():
            col.set_cell_data_func(cell, cell_func)


def colorear_tv_facturas(tv):
    """
    Colorea el TreeView de facturas en función de la fecha del último evento.
    """
    def cell_func(column, cell, model, itr):
        color = None
        try:
            abuelo = model[itr].parent.parent
        except AttributeError:
            color = None    # No abuelo, no factura.
        else:
            if not abuelo:
                color = None    # No abuelo, no factura.
                # DONE: ¿Debería colorear los clientes y obras en función de 
                # sus hijos? CWT: No.
            else:
                id = model[itr][-1]
                factura = pclases.FacturaVenta.get(id)
                last_evento = factura.get_last_evento()
                # CWT: Solo dos colores: verde/rojo
                #ayer = mx.DateTime.localtime() - mx.DateTime.oneDay
                if not last_evento:
                    color = "red"
                #elif last_evento.fechahora < ayer:
                #    color = "orange"
                else:
                    color = "green"
        cell.set_property("cell-background", color)
    cols = tv.get_columns()
    for col in cols:
        for cell in col.get_cell_renderers():
            col.set_cell_data_func(cell, cell_func)

def colorear_tv_tareas(tv):
    """
    Colorea el TreeView de facturas en función de la fecha del último evento.
    """
    def cell_func(column, cell, model, itr):
        id = model[itr][-1]
        try:
            tarea = pclases.Tarea.get(id)
        except:
            pass    # Es posible que la tarea se esté eliminando a la vez que 
                    # estoy intentando colorearla.
        else:
            categoria = tarea.categoria
            if not categoria:
                color = None
                cell.set_property("cell-background", color)
            else:
                color = categoria.get_gdk_color_params()
                cell.set_property("cell-background-gdk", gtk.gdk.Color(*color))
    cols = tv.get_columns()
    for col in cols:
        for cell in col.get_cell_renderers():
            col.set_cell_data_func(cell, cell_func)


class CRM_SeguimientoImpagos(Ventana):

    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'crm_seguimiento_impagos.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_exportar/clicked': self.exportar, 
                       'b_fechaini/clicked': self.set_fecha_ini, 
                       'b_fechafin/clicked': self.set_fecha_fin, 
                       'tg_filtrar/toggled': self.cambiar_filtro,
                       'tv_datos/cursor-changed': self.cambiar_filtro, 
                       'b_add_todo/clicked': self.add_todo, 
                       'b_drop_todo/clicked': self.drop_todo, 
                       'b_expandir/clicked': self.expandir_facturas, 
                       'b_contraer/clicked': self.contraer_facturas, 
                       'e_fechaini/focus-out-event': show_fecha, 
                       'e_fechafin/focus-out-event': show_fecha, 
                       'b_abrir/clicked': self.abrir_facturas_seleccionadas, 
                       'b_asignar_obra/clicked': self.asignar_obra, 
                       'b_cambiar_cliente/clicked': self.cambiar_cliente
                       }
        self.add_connections(connections)
        cols = [('Cliente', 'gobject.TYPE_STRING', False, True, False, None),
                ('Nº. Factura', 'gobject.TYPE_STRING', 
                    False, True, True, None),
                ('Fecha', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Vencimiento', 'gobject.TYPE_STRING',False,True,False,None), 
                ("Importe pendiente", "gobject.TYPE_STRING", 
                    False, True, False, None), 
                ("Último evento", "gobject.TYPE_STRING", 
                    False, True, False, None), 
                ('id', 'gobject.TYPE_INT64', False, False, False, None)]
        utils.preparar_treeview(self.wids['tv_datos'], cols, multi = True)
        self.wids['tv_datos'].connect("row-activated", self.abrir_factura)
        cell = self.wids['tv_datos'].get_column(4).get_cell_renderers()[0]
        cell.set_property('xalign', 1) 
        cell = self.wids['tv_datos'].get_column(3).get_cell_renderers()[0]
        cell.set_property('xalign', 0.5) 
        colorear_tv_facturas(self.wids['tv_datos'])
        cols = [('Completada', 'gobject.TYPE_BOOLEAN', 
                    True, True, False, self.cambiar_todo_pendiente),
                ('Tarea', 'gobject.TYPE_STRING', 
                    True, True, False, self.cambiar_todo_texto),
                ('Fecha', 'gobject.TYPE_STRING', 
                    True, True, True, self.cambiar_todo_fecha), 
                ('Factura', 'gobject.TYPE_STRING',False,True,False,None), 
                ('Categoría', 'gobject.TYPE_STRING', False, True, False, None),
                ('id', 'gobject.TYPE_INT64', False, False, False, None)]
        utils.preparar_listview(self.wids['tv_todos'], cols, multi = True)
        self.wids['tv_todos'].connect("row-activated", self.ver_factura_en_tv)
        colorear_tv_tareas(self.wids['tv_todos'])
        # Anotaciones y Alertas:
        cols = [('Cliente', 'gobject.TYPE_STRING', False, True, False, None),
                ('Nº. Factura', 'gobject.TYPE_STRING', 
                    False, True, True, None),
                ('Fecha', 'gobject.TYPE_STRING', False, True, False, None), 
                ("Texto", "gobject.TYPE_STRING", False, True, False, None), 
                ("Observaciones","gobject.TYPE_STRING",False,True,False,None), 
                ('id', 'gobject.TYPE_INT64', False, False, False, None)]
        utils.preparar_listview(self.wids['tv_notas'], cols, multi = True)
        self.wids['tv_notas'].connect("row-activated", 
                                        self.abrir_factura_from_alarma)
        cols = [('Cliente', 'gobject.TYPE_STRING', False, True, False, None),
                ('Nº. Factura', 'gobject.TYPE_STRING', 
                    False, True, True, None),
                ('Estado', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Fecha creación','gobject.TYPE_STRING',False,True,False,None),
                ("Texto", "gobject.TYPE_STRING", 
                    True, True, False, self.edit_texto_alarma), 
                ("Fecha alarma","gobject.TYPE_STRING",False,True,False,None), 
                ("Observaciones","gobject.TYPE_STRING",
                    True ,True, False, self.edit_observaciones_alarma), 
                ('id', 'gobject.TYPE_INT64', False, False, False, None)]
        utils.preparar_listview(self.wids['tv_alarmas'], cols, multi = True)
        self.wids['tv_alarmas'].connect("row-activated", 
                                        self.abrir_factura_from_alarma)
        estados = [(e.descripcion, e.get_puid()) for e 
                   in pclases.Estado.select(orderBy = "id")]
        utils.cambiar_por_combo(self.wids['tv_alarmas'], 
                                2, 
                                estados, 
                                pclases.Alarma, 
                                "estado", 
                                self.wids['ventana'])
        #self.tvalertas = pclase2tv.Pclase2tv(pclases.Alarma, 
        #                                self.wids['tv_alarmas'], 
        #                                self.objeto, 
        #                                cols_a_ignorar = [
        #            "facturaVentaID", "objetoRelacionado", "estadoID"], 
        #            nombres_col = ["Fecha y hora", "Texto", 
        #                           "Fecha y hora de alarma", "Observaciones"])
        colorear_tv_alarmas(self.wids['tv_alarmas'])
        #self.wids['ventana'].maximize()
        self.wids['e_fechaini'].set_text("")
        self.wids['e_fechafin'].set_text(
            utils.str_fecha(mx.DateTime.localtime()))
        gtk.main()

    def expandir_facturas(self, boton):
        """
        Expande todas las ramas del TreeView de facturas.
        """
        self.wids['tv_datos'].expand_all()

    def contraer_facturas(self, boton):
        """
        Contrae todas las ramas del TreeView de facturas.
        """
        self.wids['tv_datos'].collapse_all()

    def edit_texto_alarma(self, cell, path, newtext):
        """
        Cambia el texto de la alarma por el texto recibido.
        """
        model = self.wids['tv_alarmas'].get_model()
        id = model[path][-1]
        alarma = pclases.Alarma.get(id)
        alarma.texto = newtext
        alarma.syncUpdate()
        model[path][4] = alarma.texto

    def edit_observaciones_alarma(self, cell, path, newtext):
        """
        Cambia las observaciones de la alarma por el texto recibido.
        """
        model = self.wids['tv_alarmas'].get_model()
        id = model[path][-1]
        alarma = pclases.Alarma.get(id)
        alarma.observaciones = newtext
        alarma.syncUpdate()
        model[path][6] = alarma.observaciones

    def cambiar_todo_pendiente(self, cell, path):
        """
        Cambia la tarea de pendiente a terminada.
        """
        model = self.wids['tv_todos'].get_model()
        id = model[path][-1]
        tarea = pclases.Tarea.get(id)
        tarea.pendiente = model[path][0]
        if tarea.pendiente:
            tarea.fechadone = None
        else:
            tarea.fechadone = mx.DateTime.localtime()
        tarea.sync()
        model[path][0] = not tarea.pendiente
        if not tarea.pendiente:
            nota = pclases.Nota(facturaVenta = tarea.facturaVenta, 
                        fechahora = mx.DateTime.localtime(), 
                        texto = "Se completó la tarea «%s»" % tarea.texto, 
                        observaciones = "Creado automáticamente desde "
                            "crm_seguimiento_impagos al cerrar la tarea %d"%(
                             tarea.id))
        else:
            nota = pclases.Nota(facturaVenta = tarea.facturaVenta, 
                    fechahora = mx.DateTime.localtime(), 
                    texto = "Se anuló el cierre de la tarea «%s»"%tarea.texto, 
                    observaciones = "Creado automáticamente desde "
                    "crm_seguimiento_impagos al abrir la tarea %d"%(
                       tarea.id))
        last_evento = nota
        model = self.wids['tv_datos'].get_model()
        for fila in model:
            #print fila
            for hijo in model[fila.iter].iterchildren(): 
                #print model[hijo.iter[-1]]
                if model[hijo.iter][-1] == tarea.facturaVentaID:
                    last_evento = "[%s] %s" % (
                        utils.str_fechahora(last_evento.fechahora), 
                        last_evento.texto)
                    #print last_evento
                    model[hijo.iter][5] = last_evento 
                    return  # No quiero seguir recorriendo.

    def cambiar_todo_texto(self, cell, path, newtext):
        """
        Cambia el texto de la tarea por el que se ha escrito en ventana.
        """
        model = self.wids['tv_todos'].get_model()
        id = model[path][-1]
        tarea = pclases.Tarea.get(id)
        tarea.texto = newtext
        tarea.syncUpdate()
        model[path][1] = tarea.texto

    def cambiar_todo_fecha(self, cell, path, newtext):
        """
        Si la fecha escrita es válida, cambia la de la tarea por esa.
        """
        try:
            fecha = utils.parse_fecha(newtext)
        except (TypeError, ValueError):
            utils.dialogo_info(titulo = "FECHA NO VÁLIDA", 
                    texto = "El texto «%s» no es una fecha válida." % newtext,
                    padre = self.wids['ventana'])
        else:
            model = self.wids['tv_todos'].get_model()
            id = model[path][-1]
            tarea = pclases.Tarea.get(id)
            tarea.fecha = fecha
            tarea.syncUpdate()
            model[path][2] = utils.str_fecha(tarea.fecha)

    def asignar_obra(self, boton):
        """
        Asigna una obra seleccionada en un desplegable a todas las facturas 
        seleccionadas.
        """
        tv = self.wids['tv_datos']
        model, iters = tv.get_selection().get_selected_rows()
        if not iters:
            utils.dialogo_info(titulo = "SELECCIONE FACTURA", 
                texto = "Debe seleccionar al menos una factura.", 
                padre = self.wids['ventana'])
        else:
            idfras = []
            for iter in iters:
                if not model[iter].parent:          # Es cliente
                    for iterhijo in model[iter].iterchildren():
                        for iternieto in model[iterhijo.iter].iterchildren():
                            id = model[iternieto.iter][-1]
                            idfras.append(id)
                elif not model[iter].parent.parent: # Es obra
                    for iterhijo in model[iter].iterchildren():
                        id = model[iterhijo.iter][-1]
                        idfras.append(id)
                else:                               # Es factura
                    idfras.append(model[iter][-1])
            obra = self.elegir_o_crear_obra()
            if obra:
                for id in idfras:
                    fra = pclases.FacturaVenta.get(id)
                    cliente = fra.cliente
                    if obra not in cliente.obras:
                        cliente.addObra(obra)
                    fra.obra = obra
                self.actualizar_ventana()

    def cambiar_cliente(self, boton):
        """
        Asigna un nuevo cliente seleccionado en un desplegable a todas las 
        facturas seleccionadas.
        """
        tv = self.wids['tv_datos']
        model, iters = tv.get_selection().get_selected_rows()
        if not iters:
            utils.dialogo_info(titulo = "SELECCIONE FACTURA", 
                texto = "Debe seleccionar al menos una factura.", 
                padre = self.wids['ventana'])
        else:
            txt_rollazo = """
            Se va a cambiar el cliente de las facturas seleccionadas.
            Tenga en cuenta que no se modificarán pedidos ni albaranes 
            relacionados.
            ¿Desea continuar?
            """
            if not utils.dialogo(titulo = "¿CONTINUAR?", 
                                 texto = txt_rollazo, 
                                 padre = self.wids['ventana']):
                return 
            idfras = []
            for iter in iters:
                if not model[iter].parent:          # Es cliente
                    for iterhijo in model[iter].iterchildren():
                        for iternieto in model[iterhijo.iter].iterchildren():
                            id = model[iternieto.iter][-1]
                            idfras.append(id)
                elif not model[iter].parent.parent: # Es obra
                    for iterhijo in model[iter].iterchildren():
                        id = model[iterhijo.iter][-1]
                        idfras.append(id)
                else:                               # Es factura
                    idfras.append(model[iter][-1])
            cliente = self.elegir_cliente()
            if cliente:
                for id in idfras:
                    fra = pclases.FacturaVenta.get(id)
                    fra.cliente = cliente
                    obra = self.elegir_o_crear_obra()
                    if obra:
                        if fra.obra not in cliente.obras:
                            cliente.addObra(obra)
                        fra.obra = obra
                        fra.syncUpdate()
                        self.actualizar_ventana()

    def elegir_cliente(self):
        idcliente = utils.dialogo_combo(titulo = "SELECCIONE CLIENTE", 
            texto = "Seleccione un cliente del desplegable inferior:", 
            padre = self.wids['ventana'], 
            ops = [(c.id, c.get_info()) for c in 
                   pclases.Cliente.select(
                    pclases.Cliente.q.inhabilitado == False, 
                    orderBy = "nombre")])
        if idcliente:
            return pclases.Cliente.get(idcliente)
        else:
            return None

    def elegir_o_crear_obra(self):
        """
        Crea una nueva obra relacionada o devuelve una de las existentes. 
        """
        obras = pclases.Obra.select(orderBy = "nombre")
        idobra = utils.dialogo_combo(titulo = "SELECCIONE OBRA", 
            texto = "Seleccione una obra del desplegable inferior o cree una "\
                    "nueva.", 
            padre = self.wids['ventana'], 
            ops = [(0, "Crear una obra nueva")] + [(o.id, o.nombre) 
                                                    for o in obras]) 
        if idobra == 0:
            nombre = utils.dialogo_entrada(titulo = "NOMBRE DE OBRA", 
                texto = "Introduzca el nombre de la obra:", 
                padre = self.wids['ventana'])
            if not nombre:
                return None
            direccion = utils.dialogo_entrada(titulo = "DIRECCIÓN", 
                texto = "Introduzca la dirección de la obra:", 
                padre = self.wids['ventana'])
            if direccion == None:
                return None 
            ciudad = utils.dialogo_entrada(titulo = "CIUDAD", 
                texto = "Introduzca la ciudad:", 
                padre = self.wids['ventana'])
            if ciudad == None:
                return None
            cp = utils.dialogo_entrada(titulo = "CÓDIGO POSTAL", 
                texto = "Introduzca el código postal", 
                padre = self.wids['ventana'])
            if cp == None:
                return None
            provincia = utils.dialogo_entrada(titulo = "PROVINCIA", 
                texto = "Introduzca la provincia:", 
                padre = self.wids['ventana'])
            if provincia == None:
                return None
            # De fecha de inicio, fecha de fin de obra y observacione pasamos 
            # a este nivel. Eso se afina en la ventana de obras.
            obra = pclases.Obra(nombre = nombre, direccion = direccion, 
                    cp = cp, ciudad = ciudad, provincia = provincia, 
                    fechainicio = None, fechafin = None, 
                    observaciones = "Creada desde módulo CRM: detalles de "\
                                    "factura.", 
                    generica = False)
        elif idobra:
            obra = pclases.Obra.get(idobra)
        else:
            obra = None
        return obra

    def actualizar_ventana(self):
        self.buscar(None)

    def add_todo(self, boton):
        """
        Añade una nueva tarea relacionada con la factura seleccionada.
        """
        pagina = self.wids['notebook'].get_current_page()
        if pagina == 0:
            funcion_add = self.nuevo_todo
        elif pagina == 1:
            funcion_add = self.nueva_nota
        elif pagina == 2:
            funcion_add = self.nueva_alarma
        else:
            return
        tv = self.wids['tv_datos']
        model, iters = tv.get_selection().get_selected_rows()
        if not iters:
            utils.dialogo_info(titulo = "SELECCIONE FACTURA", 
                texto = "Debe seleccionar al menos una factura relacionada.", 
                padre = self.wids['ventana'])
        else:
            idfras = []
            for iter in iters:
                if not model[iter].parent:          # Es cliente
                    for iterhijo in model[iter].iterchildren():
                        for iternieto in model[iterhijo.iter].iterchildren():
                            id = model[iternieto.iter][-1]
                            idfras.append(id)
                elif not model[iter].parent.parent: # Es obra
                    for iterhijo in model[iter].iterchildren():
                        id = model[iterhijo.iter][-1]
                        idfras.append(id)
                else:                               # Es factura
                    idfras.append(model[iter][-1])
            funcion_add(idfras)

    def nuevo_todo(self, idfras):
        texto = utils.dialogo_entrada(titulo = "TEXTO TAREA", 
            texto = "Introduzca el texto de la tarea.", 
            padre = self.wids['ventana'])
        if texto:
            idcat = utils.dialogo_entrada_combo(
                        titulo = "SELECCIONE CATEGORÍA", 
                        texto = "Selecciona una categoría del desplegable"\
                                " inferior:", 
                        padre = self.wids['ventana'], 
                        ops = [(c.id, "%s (Pri.: %d)" % (
                                    c.descripcion, c.prioridad))
                                for c in pclases.Categoria.select(
                                    orderBy="prioridad")])
            if idcat and idcat[0] != None:
                for id in idfras:
                    tarea = pclases.Tarea(facturaVentaID = id, 
                                          categoriaID = idcat[0], 
                                          texto = texto, 
                                          pendiente = True, 
                                          fechadone = None, 
                                          fecha = mx.DateTime.localtime()) 
                self.buscar_todos()

    def nueva_nota(self, idfras):
        texto = utils.dialogo_entrada(titulo = "TEXTO NOTA", 
            texto = "Introduzca el texto de la nota:", 
            padre = self.wids['ventana'])
        if texto:
            for id in idfras:
                tarea = pclases.Nota(facturaVentaID = id, 
                                     texto = texto, 
                                     fechahora = mx.DateTime.localtime()) 
            self.buscar_anotaciones()

    def nueva_alarma(self, idfras):
        texto = utils.dialogo_entrada(titulo = "TEXTO ALARMA", 
            texto = "Introduzca el texto de la alarma.", 
            padre = self.wids['ventana'])
        if texto: 
            fechalarma = utils.mostrar_calendario(
                titulo = "FECHA Y HORA", 
                padre = self.wids['ventana'], 
                fecha_defecto = mx.DateTime.localtime() + mx.DateTime.oneDay)
            try:
                dia, mes, anno = fechalarma
                fechalarma = mx.DateTime.DateTimeFrom(day = dia, 
                                                      month = mes, 
                                                      year = anno)
            except (TypeError, ValueError, AttributeError):
                utils.dialogo_info(titulo = "FECHA INCORRECTA", 
                                   texto = "La fecha seleccionada (%s)\n"
                                           "no es correcta." % `fechalarma`, 
                                   padre = self.wids['ventana'])
                fechalarma = None
            if fechalarma:
                hora = utils.mostrar_hora(titulo="SELECCIONE HORA DE ALARMA", 
                        padre = self.wids['ventana'], 
                        horas = mx.DateTime.localtime().hour, 
                        minutos = mx.DateTime.localtime().minute)
                if not hora:
                    return  # Canceló
                try:
                    horas = int(hora.split(":")[0])
                    minutos = int(hora.split(":")[1])
                    fechalarma = mx.DateTime.DateTimeFrom(
                        day = fechalarma.day, 
                        month = fechalarma.month, 
                        year = fechalarma.year, 
                        hour = horas, 
                        minute = minutos)
                except (IndexError, TypeError, ValueError, AttributeError):
                    utils.dialogo_info(titulo = "HORA INCORRECTA", 
                        texto = "La hora %s no es correcta." % (hora), 
                        padre = self.wids['ventana'])
                    fechalarma = None
                if fechalarma:
                    try:
                        estado = pclases.Estado.get(1)  # *Debería* existir.
                    except:
                        estado = None
                    #print idfras
                    for id in idfras:
                        tarea = pclases.Alarma(facturaVentaID = id, 
                                           texto = texto,  
                                           fechahora = mx.DateTime.localtime(),
                                           estado = estado, 
                                           fechahoraAlarma = fechalarma, 
                                           objetoRelacionado = None) 
                    self.buscar_alertas()

    def drop_todo(self, boton):
        """
        Elimina la tarea seleccionada en el TreeView.
        """
        pagina = self.wids['notebook'].get_current_page()
        if pagina == 0:
            tv = self.wids['tv_todos']
            clase = pclases.Tarea
        elif pagina == 1:
            tv = self.wids['tv_notas']
            clase = pclases.Nota
        elif pagina == 2:
            tv = self.wids['tv_alarmas']
            clase = pclases.Alarma
        else:
            return
        model, iters = tv.get_selection().get_selected_rows()
        to_remove = []
        for iter in iters: 
            id = model[iter][-1]
            tarea = clase.get(id)
            tarea.destroySelf()
            to_remove.append(model.get_iter(iter))
        for iter in to_remove:
            model.remove(iter)

    def cambiar_filtro(self, widget, *arg, **kw):
        """
        Cambia el filtro de los todos mostrando todos o solo las facturas 
        de la fila seleccionada (en realidad ese filtro se hace en el método 
        buscar_todos, aquí lo único que se hace es llamarlo).
        """
        self.buscar_todos()
        self.buscar_anotaciones()
        self.buscar_alertas()

    def set_fecha_ini(self, boton):
        utils.set_fecha(self.wids['e_fechaini'])

    def set_fecha_fin(self, boton):
        utils.set_fecha(self.wids['e_fechafin'])

    def ver_factura_en_tv(self, tv, path, view_column):
        """
        Despliega en el TreeView de facturas la factura de la tarea y sitúa 
        el cursor en ella.
        """
        model = tv.get_model()
        id = model[path][-1]
        tarea = pclases.Tarea.get(id)
        model = self.wids['tv_datos'].get_model()
        for fila in model:
            #print fila
            for hijo in model[fila.iter].iterchildren(): 
                #print model[hijo.iter[-1]]
                if model[hijo.iter][-1] == tarea.facturaVentaID:
                    path = model.get_path(hijo.iter)
                    self.wids['tv_datos'].expand_to_path(path) 
                    self.wids['tv_datos'].set_cursor(path) 
    
    def abrir_factura_from_alarma(self, tv, path, view_column):
        """
        Abre la factura a la que pertenece la alarma en la ventana de detalles.
        """
        model = tv.get_model()
        id = model[path][-1]
        try:
            a = pclases.Alarma.get(id)
        except pclases.SQLObjectNotFound:   # Fue eliminado de la BD.
            utils.dialogo_info(titulo = "ALARMA ELIMINADA", 
                texto = "La alarma de %s perteneciente a la factura \n"
                        "%s fue eliminada y ya no es válida." % (
                            model[path][0], model[path][1]), 
                padre = self.wids['ventana'])
        else:
            fra = a.facturaVenta
            import crm_detalles_factura
            v = crm_detalles_factura.CRM_DetallesFactura(fra, 
                                                         usuario = self.usuario)
            # Actualizo último evento porque probablemente lo haya cambiado
            # en la ventana recién abierta. El resto de datos de la 
            # factura debería permanecer tal cual (¿A excepción de los 
            # vencimientos? No creo. No se renegocian... o no debería.).
            model = self.wids['tv_datos'].get_model()
            last_evento = fra.get_last_evento()
            if last_evento:
                last_evento = "[%s] %s" % (
                    utils.str_fechahora(last_evento.fechahora), 
                    last_evento.texto)
            else:
                last_evento = ""
            model[path][5] = last_evento
            self.buscar_todos()
            self.buscar_alertas()
            self.buscar_anotaciones()

    def abrir_facturas_seleccionadas(self, boton):
        sel = self.wids['tv_datos'].get_selection()
        model, paths = sel.get_selected_rows()
        for path in paths:
            self.abrir_factura(self.wids['tv_datos'], path, None)

    def abrir_factura(self, tv, path, view_column):
        """
        Abre la factura a la que pertenece el vencimiento sobre el que se ha 
        hecho doble clic.
        """
        model = tv.get_model()
        id = model[path][-1]
        if model[path].parent:  # Es nodo hijo: abono, factura u obra.
            if model[path].parent.parent: # Es abono o factura
                if id > 0:  # Si es negativo es un ID de cliente. No me interesa.
                    fra = pclases.FacturaVenta.get(id)
                    #import facturas_venta
                    #v = facturas_venta.FacturasVenta(fra, usuario = self.usuario)
                    import crm_detalles_factura
                    v = crm_detalles_factura.CRM_DetallesFactura(fra, 
                                                            usuario = self.usuario)
                    # Actualizo último evento porque probablemente lo haya cambiado
                    # en la ventana recién abierta. El resto de datos de la 
                    # factura debería permanecer tal cual (¿A excepción de los 
                    # vencimientos? No creo. No se renegocian... o no debería.).
                    last_evento = fra.get_last_evento()
                    if last_evento:
                        last_evento = "[%s] %s" % (
                            utils.str_fechahora(last_evento.fechahora), 
                            last_evento.texto)
                    else:
                        last_evento = ""
                    model[path][5] = last_evento
                elif id < 0:   # Ahora los id negativos son de abonos, no clientes.
                    fda = pclases.FacturaDeAbono.get(-id)
                    a = fda.abono
                    import abonos_venta
                    v = abonos_venta.AbonosVenta(a, usuario = self.usuario)
            else:   # Es obra. Abro... ¿cliente?
                idcliente = model[path].parent[-1]
                cliente = pclases.Cliente.get(idcliente)
                import clientes
                v = clientes.Clientes(cliente, usuario = self.usuario)
        else:
            cliente = pclases.Cliente.get(id)
            import clientes
            v = clientes.Clientes(cliente, usuario = self.usuario)

    def chequear_cambios(self):
        pass

    def buscar(self, boton):
        # DONE: Faltan los abonos por descontar.
        fechaini = self.wids['e_fechaini'].get_text().strip()
        if fechaini:
            try:
                fechaini = utils.parse_fecha(fechaini)
            except (ValueError, TypeError):
                utils.dialogo_info(titulo = "ERROR EN FECHA INICIAL", 
                 texto = "El texto «%s» no es una fecha correcta." % fechaini,
                 padre = self.wids['ventana'])
                fechaini = None
        fechafin = self.wids['e_fechafin'].get_text().strip()
        if fechafin:
            try:
                fechafin = utils.parse_fecha(fechafin)
            except (ValueError, TypeError):
                utils.dialogo_info(titulo = "ERROR EN FECHA FINAL", 
                 texto = "El texto «%s» no es una fecha correcta." % fechafin,
                 padre = self.wids['ventana'])
                fechafin = None
        if fechaini and fechafin and fechafin < fechaini:
            fechaini, fechafin = fechafin, fechaini
            self.wids['e_fechaini'].set_text(utils.str_fecha(fechaini))
            self.wids['e_fechafin'].set_text(utils.str_fecha(fechafin))
        if fechafin:
            FV = pclases.FacturaVenta
            VC = pclases.VencimientoCobro   # Para asegurarme de 
                                            # que tiene vencimientos.
            FDA = pclases.FacturaDeAbono
            C = pclases.Cobro
            T = pclases.Tarea
            if fechaini:
                facturas = FV.select(pclases.AND(
                                        FV.q.fecha >= fechaini, 
                                        FV.q.fecha <= fechafin, 
                                        VC.q.facturaVentaID == FV.q.id))
                # Busco los abonos (facturas de abono, en realidad, que no 
                # tienen por qué tener la misma fecha) que no hayan sido 
                # incluidos en facturas (porque si no el importe ya se habría 
                # contado en la factura anterior) ni en pagarés (porque 
                # entonces ya estarían en un documento de pago y por tanto 
                # no deberían aparecer en esta consulta)
                # ... 
                # He decidido que no voy a sacar los abonos. No van a tener 
                # ventana de seguimiento y no se le pueden relacionar tareas.
                # Además, esta ventana era para reclamar pagos, no para pagar.
                #abonos = FDA.select(pclases.AND(
                #    FDA.q.fecha >= fechaini, 
                #    FDA.q.fecha <= fechafin))
                abonos = []
            else:
                facturas = FV.select(pclases.AND(
                                        FV.q.fecha <= fechafin, 
                                        VC.q.facturaVentaID == FV.q.id))
                #abonos = FDA.select(FDA.q.fecha <= fechafin)
                abonos = []
            # No me queda otra que filtrar así aunque sea lento:
            abonos_pendientes = []
            for a in abonos:
                if not a.abono:
                    continue # ¿Error de borrado de un abono? Mmm... mal rollo.
                if a.abono.facturasVenta:
                    continue
                if a.cobros:    # Cada cobro de abono está relacionado 
                                # con un pagaré (o con lo que sea en un 
                                # posible futuro, el caso es que no 
                                # estaría pendiente).
                    continue
                abonos_pendientes.append(a)
            from ventana_progreso import VentanaProgreso
            vpro = VentanaProgreso(padre = self.wids['ventana'])
            vpro.mostrar()
            txtvpro = "Buscando facturas sin documento de pago..."
            nodos_clientes = {}
            total = 0.0
            i = 0.0
            vpro.set_valor(i, txtvpro)
            model = self.wids['tv_datos'].get_model()
            model.clear()
            facturas_added = []
            # Aprovecho para chequear alarmas automáticas.
            pclases.Alarma.crear_alarmas_automaticas(facturas)
            for f in facturas:
                # Aquí voy a hacer un segundo filtro usando la cantidad 
                # pendiente de cobro de cada factura.
                #pendiente = f.calcular_pendiente_cobro()
                pendiente = f.calcular_pendiente_de_documento_de_pago()
                pendiente = round(pendiente, 2)
                if pendiente and f not in facturas_added: 
                    total += pendiente
                    cliente = f.cliente
                    if cliente not in nodos_clientes:
                        tmp_nodo = model.append(None, 
                                                (cliente.nombre, 
                                                 "", "", "", "0", "",  
                                                 cliente.id))
                        nodos_clientes[cliente] = {'nodo_cliente': tmp_nodo}
                    obra = f.obra
                    nodo_cliente_padre=nodos_clientes[cliente]['nodo_cliente']
                    if obra not in nodos_clientes[cliente]:
                        nodos_clientes[cliente][obra] = model.append(
                            nodo_cliente_padre, 
                            (obra and obra.nombre or "Sin obra", 
                             "", "", "", "0", "", 
                             obra and obra.id or 0))
                    fechas_vto = f.vencimientosCobro[:]
                    fechas_vto.sort(lambda v1, v2: (v1.fecha < v2.fecha and -1)
                                                or (v1.fecha > v2.fecha and 1)
                                                or 0)
                    fechas_vto = [utils.str_fecha(v.fecha) 
                                      for v in f.vencimientosCobro]
                    vtos = "; ".join(fechas_vto)
                    nodo_padre = nodos_clientes[cliente][obra]
                    last_evento = f.get_last_evento()
                    if last_evento:
                        last_evento = "[%s] %s" % (
                            utils.str_fechahora(last_evento.fechahora), 
                            last_evento.texto)
                    else:
                        last_evento = ""
                    model.append(nodo_padre, 
                                 ("", 
                                 #(f.cliente.nombre, 
                                  f.numfactura, 
                                  utils.str_fecha(f.fecha), 
                                  vtos, 
                                  utils.float2str(pendiente), 
                                  last_evento, 
                                  f.id))
                    model[nodo_padre][4] = utils.float2str(
                        utils._float(model[nodo_padre][4]) + pendiente)
                    model[nodo_cliente_padre][4] = utils.float2str(
                        utils._float(model[nodo_cliente_padre][4]) + pendiente)
                    facturas_added.append(f)
                i += 1
                vpro.set_valor(i/(facturas.count() + len(abonos_pendientes)), 
                               txtvpro)
            for a in abonos_pendientes:
                pendiente = a.calcular_importe_total()  # O está descontada 
                # entera o no lo está. Con los abonos no hay pagos parciales.
                pendiente = round(pendiente, 2)
                if pendiente: 
                    total += pendiente
                    vtos = utils.str_fecha(a.fecha)  # Tampoco tiene 
                    # vencimientos. La obligación nace desde el mismo día 
                    # en que el abono se convierte en factura de abono.
                    try:
                        cliente = a.cliente
                    except AttributeError:
                        txt = "crm_seguimiento_impagos.py::buscar"\
                            " -> FacturaDeAbono %d sin Abono o Cliente."\
                            " Ignorando. " % a.id
                        self.logger.error(txt)
                        continue
                    if cliente not in nodos_clientes:
                        tmp_nodo = model.append(None, 
                                                (cliente.nombre, 
                                                 "", "", "", "0", "",  
                                                 cliente.id))
                        nodos_clientes[cliente] = {"nodo_cliente": tmp_nodo} 
                    obra = a.obra
                    nodo_cliente_padre=nodos_clientes[cliente]['nodo_cliente']
                    if obra not in nodos_clientes[cliente]:
                        nodos_clientes[cliente][obra] = model.append(
                            nodo_cliente_padre, 
                            (obra and obra.nombre or "Sin obra", 
                             "", "", "", "0", "", 
                             obra and obra.id or 0))
                    nodo_padre = nodos_clientes[cliente][obra]
                    model.append(nodo_padre, 
                                 #(a.cliente.nombre, 
                                 ("", 
                                  a.numfactura, 
                                  utils.str_fecha(a.fecha), 
                                  vtos, 
                                  utils.float2str(pendiente), 
                                  "", #Facturas de abono no tienen anotaciones.
                                  -a.id)) # Para distinguirlo de las facturas. 
                    model[nodo_padre][4] = utils.float2str(
                        utils._float(model[nodo_padre][4]) + pendiente)
                    model[nodo_cliente_padre][4] = utils.float2str(
                        utils._float(model[nodo_cliente_padre][4]) + pendiente)
                i += 1
                vpro.set_valor(i/(facturas.count() + len(abonos_pendientes)), 
                               txtvpro)
            vpro.ocultar()
            self.wids['e_total'].set_text(utils.float2str(total))
            self.buscar_todos()
            self.buscar_anotaciones()
            self.buscar_alertas()

    def buscar_anotaciones(self):
        idfras = []
        if self.wids['tg_filtrar'].get_active():    # Filtrar por seleccionada.
            sel = self.wids['tv_datos'].get_selection()
            model, iters = sel.get_selected_rows()
            for iter in iters:
                id = model[iter][-1]
                if not model[iter].parent:          # Es cliente
                    for iterhijo in model[iter].iterchildren():
                        for iternieto in model[iterhijo.iter].iterchildren():
                            idfras.append(model[iternieto.iter][-1])
                elif not model[iter].parent.parent: # Es obra
                    for iterhijo in model[iter].iterchildren():
                        idfras.append(model[iterhijo.iter][-1])
                else:                               # Es factura
                    idfras.append(id)
        else:
            model = self.wids['tv_datos'].get_model()
            idfras = []
            for fila in model:
                for hijo in model[fila.iter].iterchildren(): 
                    for nieto in model[hijo.iter].iterchildren(): 
                        idfras.append(model[nieto.iter][-1])
        model = self.wids['tv_notas'].get_model()
        model.clear()
        for id in idfras:
            if id > 0:
                fra = pclases.FacturaVenta.get(id)
                for n in fra.notas:
                    try:
                        nombre_cliente = n.facturaVenta.cliente.nombre
                    except AttributeError:
                        nombre_cliente = "¡Sin cliente!"
                    model.append((nombre_cliente, 
                                  n.facturaVenta.numfactura, 
                                  utils.str_fechahora(n.fechahora), 
                                  n.texto, 
                                  n.observaciones, 
                                  n.id))

    def buscar_alertas(self):
        idfras = []
        if self.wids['tg_filtrar'].get_active():    # Filtrar por seleccionada.
            sel = self.wids['tv_datos'].get_selection()
            model, iters = sel.get_selected_rows()
            for iter in iters:
                id = model[iter][-1]
                if not model[iter].parent:          # Es cliente
                    for iterhijo in model[iter].iterchildren():
                        for iternieto in model[iterhijo.iter].iterchildren():
                            idfras.append(model[iternieto.iter][-1])
                elif not model[iter].parent.parent: # Es obra
                    for iterhijo in model[iter].iterchildren():
                        idfras.append(model[iterhijo.iter][-1])
                else:                               # Es factura
                    idfras.append(id)
        else:
            model = self.wids['tv_datos'].get_model()
            idfras = []
            for fila in model:
                for hijo in model[fila.iter].iterchildren(): 
                    for nieto in model[hijo.iter].iterchildren(): 
                        idfras.append(model[nieto.iter][-1])
        model = self.wids['tv_alarmas'].get_model()
        model.clear()
        hoy = mx.DateTime.today()
        for id in idfras:
            if id > 0:
                fra = pclases.FacturaVenta.get(id)
                for a in fra.alarmas:
                    if (a.fechahoraAlarma >= hoy + mx.DateTime.oneDay
                        or not a.estado.pendiente):
                        continue
                    try:
                        nombre_cliente = a.facturaVenta.cliente.nombre
                    except AttributeError:
                        nombre_cliente = "¡Sin cliente!"
                    model.append((nombre_cliente, 
                                  a.facturaVenta.numfactura, 
                                  a.estado.descripcion, 
                                  utils.str_fechahora(a.fechahora), 
                                  a.texto, 
                                  utils.str_fechahora(a.fechahoraAlarma), 
                                  a.observaciones, 
                                  a.id))

    def buscar_todos(self):
        """
        Busca las tareas pendientes relacionadas con la factura seleccionada 
        en el TV o bien de todas si el botón de filtrar está "no presionado".
        """
        idfras = []
        if self.wids['tg_filtrar'].get_active():    # Filtrar por seleccionada.
            sel = self.wids['tv_datos'].get_selection()
            model, iters = sel.get_selected_rows()
            for iter in iters:
                id = model[iter][-1]
                if not model[iter].parent:          # Es cliente
                    for iterhijo in model[iter].iterchildren():
                        for iternieto in model[iterhijo.iter].iterchildren():
                            idfras.append(model[iternieto.iter][-1])
                elif not model[iter].parent.parent: # Es obra
                    for iterhijo in model[iter].iterchildren():
                        idfras.append(model[iterhijo.iter][-1])
                else:                               # Es factura
                    idfras.append(id)
        else:
            model = self.wids['tv_datos'].get_model()
            idfras = []
            for fila in model:
                for hijo in model[fila.iter].iterchildren(): 
                    for nieto in model[hijo.iter].iterchildren(): 
                        idfras.append(model[nieto.iter][-1])
        model = self.wids['tv_todos'].get_model()
        model.clear()
        for id in idfras:
            if id > 0:
                fra = pclases.FacturaVenta.get(id)
                for todo in fra.tareas:
                    if (todo.pendiente or 
                        mx.DateTime.localtime() - todo.fechadone 
                            <= mx.DateTime.oneDay):
                        cat = todo.categoria
                        model.append((not todo.pendiente, 
                                      todo.texto, 
                                      utils.str_fecha(todo.fecha), 
                                      "%s (%s)" % (
                                        todo.facturaVenta.numfactura, 
                                        todo.facturaVenta.cliente and 
                                            todo.facturaVenta.cliente.nombre or
                                            "¡Sin cliente!"), 
                                      cat and cat.descripcion or "", 
                                      todo.id))

    def imprimir(self, boton):
        """
        Prepara la vista preliminar para la impresión del informe.
        """
        tv = self.wids['tv_datos']
        titulo = "Pendientes de cobro"
        from treeview2pdf import treeview2pdf
        from informes import abrir_pdf
        strfecha = "%s - %s" % (
            self.wids['e_fechaini'].get_text(), 
            self.wids['e_fechafin'].get_text())
        nomarchivo = treeview2pdf(tv, 
            titulo = titulo,
            fecha = strfecha, 
            apaisado = False)
        abrir_pdf(nomarchivo)

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        import sys, os
        sys.path.append(os.path.join("..", "informes"))
        from treeview2csv import treeview2csv
        from informes import abrir_csv
        tv = self.wids['tv_datos']
        abrir_csv(treeview2csv(tv))


def show_fecha(entry, event):
    """
    Muestra la fecha en modo texto después de parsearla.
    """
    if entry.get_text():
        try:
            entry.set_text(utils.str_fecha(utils.parse_fecha(
                entry.get_text())))
        except (ValueError, TypeError):
            entry.set_text(utils.str_fecha(mx.DateTime.localtime()))


if __name__ == '__main__':
    t = CRM_SeguimientoImpagos()

