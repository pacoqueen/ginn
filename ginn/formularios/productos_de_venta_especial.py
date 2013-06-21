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
## productos_de_venta_especial.py - Productos de venta "no producción".
###################################################################
## NOTAS:
##  
## ----------------------------------------------------------------
##  
###################################################################
## Changelog:
## 1 de marzo de 2006 -> Inicio 
## 
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
from utils import _float as float
from informes.barcode.EANBarCode import EanBarCode
try:
    from psycopg import ProgrammingError as psycopg_ProgrammingError
except ImportError:
    from psycopg2 import ProgrammingError as psycopg_ProgrammingError


class ProductosDeVentaEspecial(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self._objetoreciencreado = None
        Ventana.__init__(self, 'productos_de_venta_especial.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_anterior/clicked': self.ir_a_anterior,
                       'b_siguiente/clicked': self.ir_a_siguiente,
                       'b_tarifas/clicked': self.ver_tarifas,
                       'b_nuevo/clicked': self.crear_nuevo_producto,
                       'b_borrar/clicked': self.borrar_producto,
                       'b_actualizar/clicked': self.actualizar_ventana,
                       'b_guardar/clicked': self.guardar,
                       'b_add_campoesp/clicked': self.add_campoesp,
                       'b_drop_campoesp/clicked': self.drop_campoesp,
                       'b_change_campoesp/clicked': self.change_campoesp,
                       'b_buscar/clicked': self.buscar_producto}  
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        self.wids['b_contar'].set_property("visible", False)
        gtk.main()

    # --------------- Funciones auxiliares ------------------------------
    def es_diferente(self):
        """
        Devuelve True si la información en pantalla es distinta a la
        del objeto en memoria.
        """
        producto = self.objeto
        if producto == None: return False   # Si no hay producto activo, devuelvo que no hay cambio respecto a la ventana
        condicion = producto.codigo == self.wids['e_codigo'].get_text()
        # print condicion
        if producto.camposEspecificosEspecialID != None:
            producto.camposEspecificosEspecial.sync()
            producto.camposEspecificosEspecial.chequear_cambios()
            condicion = condicion and (utils.float2str(producto.camposEspecificosEspecial.stock) == self.wids['e_stock'].get_text())
            condicion = condicion and (producto.camposEspecificosEspecial.unidad == self.wids['e_unidad'].get_text())
            condicion = condicion and (producto.camposEspecificosEspecial.observaciones == self.wids['e_observaciones'].get_text())
            condicion = condicion and (str(producto.camposEspecificosEspecial.existencias) == self.wids['e_existencias'].get_text())
        condicion = condicion and (producto.descripcion == self.wids['e_descripcion'].get_text())
        condicion = condicion and (producto.nombre == self.wids['e_nombre'].get_text())
        condicion = condicion and (str(producto.preciopordefecto) == self.wids['e_precio'].get_text())
        condicion = condicion and (str(producto.minimo) == self.wids['e_minimo'].get_text())
        condicion = condicion and (str(producto.arancel) == self.wids['e_arancel'].get_text())
        condicion = condicion and (utils.float2str(producto.prodestandar) == self.wids['e_prodestandar'].get_text())
        return not condicion    # Concición verifica que sea igual

    def aviso_actualizacion(self):
        """
        Muestra una ventana modal con el mensaje de objeto 
        actualizado.
        """
        utils.dialogo_info('ACTUALIZAR',
                           'El producto ha sido modificado remotamente.\nDebe actualizar la información mostrada en pantalla.\nPulse el botón «Actualizar»',
                           padre = self.wids['ventana'])
        self.wids['b_actualizar'].set_sensitive(True)

    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        # Inicialmente no se muestra NADA. Sólo se le deja al
        # usuario la opción de buscar o crear nuevo.
        self.activar_widgets(False)
        self.wids['b_actualizar'].set_sensitive(False)
        self.wids['b_guardar'].set_sensitive(False)
        self.wids['b_nuevo'].set_sensitive(True)
        self.wids['b_buscar'].set_sensitive(True)
        # Inicialización del resto de widgets:
        cols = (('Tarifa', 'gobject.TYPE_STRING', False, True, True, None),
                ('Precio', 'gobject.TYPE_FLOAT', False, True, False, None),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_tarifas'], cols)
        cols = (('Almacén', 'gobject.TYPE_STRING', False, True, True, None), 
                ('Existencias', 'gobject.TYPE_STRING',False,True,False,None),
                ('IDAlmacen', 'gobject.TYPE_INT64',False,False,False,None))
        utils.preparar_listview(self.wids['tv_existencias'], cols)

    def rellenar_existencias_almacen(self, producto):
        """
        Rellena las existencias de cada almacén para el producto.
        Relación inyectiva, muestra todos los almacenes y la cantidad para 
        cada uno o "-" si no hay registro.
        """
        model = self.wids['tv_existencias'].get_model()
        self.wids['tv_existencias'].set_model(None)
        model.clear()
        for a in pclases.Almacen.select(pclases.Almacen.q.activo == True, 
                                        orderBy = "id"):
            existencias = a.get_existencias(self.objeto)
            try:
                strexistencias = utils.float2str(existencias)
            except (TypeError, ValueError):
                strexistencias = "-"
            model.append((a.nombre, 
                          strexistencias, 
                          a.id))
        self.wids['tv_existencias'].set_model(model)

    def activar_widgets(self, s, chequear_permisos = True):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        if not self.objeto:
            self.wids['b_anterior'].set_sensitive(False)
            self.wids['b_siguiente'].set_sensitive(False)
            s = False
        else:
            # Se ejecuta DESPUÉS de rellenar_widgets. Así que si allí se han 
            # habilitado/deshabilitado por ser el primero/último; lo dejo 
            # como está.
            pass
            #self.wids['b_anterior'].set_sensitive(True)
            #self.wids['b_siguiente'].set_sensitive(True)
        ws = ('e_idproducto', 'e_codigo', 'e_descripcion', 'frame1', 
              'e_nombre', 'e_precio', 'e_minimo', 'e_stock', 
              'b_contar', 'b_borrar', 'b_tarifas', 'e_arancel', 'frame2') 
        for w in ws:
            self.wids[w].set_sensitive(s)
        if chequear_permisos:
            self.check_permisos(
                nombre_fichero_ventana = "productos_de_venta_especial.py")

    def ir_a_primero(self):
        """
        Hace que el primer registro -si lo hay- de la tabla implicada
        en el objeto del formulario sea el objeto activo.
        """
        producto = self.objeto
        try:
            # Anulo el aviso de actualización del envío que deja de ser activo.
            if producto != None: 
                producto.notificador.desactivar()
                producto.camposEspecificosEspecial.notificador.desactivar()
            producto = pclases.ProductoVenta.select(pclases.ProductoVenta.q.camposEspecificosEspecialID != None, orderBy = "-id")[0]  # Selecciono todos y me quedo con el primero de la lista
            producto.notificador.activar(self.aviso_actualizacion)      # Activo la notificación
            producto.camposEspecificosEspecial.notificador.activar(self.aviso_actualizacion)    
                # Y también la de los campos específicos, que tiene las existencias.
        except:
            producto = None     
        self.objeto = producto
        self.actualizar_ventana()

    def ir_a_anterior(self,widget):
        """
        Hace que el registro anterior (ordenados por ID interno)
        sea el objeto activo
        """
        if self.wids['b_guardar'] != None and self.wids['b_guardar'].get_property('sensitive'):
            # Hay cambios pendientes de guardar.
            if utils.dialogo('Hay cambios pendientes de guardar.\n¿Desea hacerlo ahora?', '¿GUARDAR CAMBIOS?'):
                try:
                    self.guardar(None)
                except:
                    utils.dialogo_info(titulo = 'NO SE PUDO GUARDAR', 
                                       texto = 'Los cambios no se pudieron guardar automáticamente.\nDebe hacerlo de forma manual', 
                                       padre = self.wids['ventana'])
                    return 
        producto = self.objeto
        try:
            anterior = pclases.ProductoVenta.select(pclases.AND(pclases.ProductoVenta.q.camposEspecificosEspecialID != None, pclases.ProductoVenta.q.id < producto.id),orderBy='-id')[0]
        except IndexError:
            utils.dialogo_info(texto = "El elemento seleccionado es el primero registrado en el sistema",
                               titulo="ERROR", 
                               padre = self.wids['ventana'])
            return
        self.objeto = anterior
        self.actualizar_ventana()
        
    def ir_a_siguiente(self,widget):
        """
        Hace que el siguiente registro (ordenados por ID interno)
        sea el objeto activo
        """
        if self.wids['b_guardar'] != None and self.wids['b_guardar'].get_property('sensitive'):
            # Hay cambios pendientes de guardar.
            if utils.dialogo('Hay cambios pendientes de guardar.\n¿Desea hacerlo ahora?', '¿GUARDAR CAMBIOS?'):
                try:
                    self.guardar(None)
                except:
                    utils.dialogo_info(titulo = 'NO SE PUDO GUARDAR', 
                                       texto = 'Los cambios no se pudieron guardar automáticamente.\nDebe hacerlo de forma manual',
                                       padre = self.wids['ventana'])
                    return 
        producto = self.objeto
        try:
            siguiente = pclases.ProductoVenta.select(pclases.AND(pclases.ProductoVenta.q.camposEspecificosEspecialID != None, pclases.ProductoVenta.q.id > producto.id),orderBy='id')[0]
        except IndexError:
            utils.dialogo_info(texto = "El elemento seleccionado es el último registrado en el sistema",
                               titulo="ERROR",
                               padre = self.wids['ventana'])
            return
        self.objeto = siguiente
        self.actualizar_ventana()
   
    def refinar_resultados_busqueda(self, resultados):
        """
        Muestra en una ventana de resultados todos los
        registros de "resultados".
        Devuelve el id (primera columna de la ventana
        de resultados) de la fila seleccionada o None
        si se canceló.
        """
        filas_res = []
        for r in resultados:
            filas_res.append((r.id, r.codigo, r.nombre, r.descripcion, 
                              r.get_stock(), r.get_existencias()))
        idproducto = utils.dialogo_resultado(filas_res,
                        titulo = 'SELECCIONE PRODUCTO',
                        cabeceras = ('ID Interno', 'Código', 'Nombre', 
                                     'Descripción', "Cantidad en almacenes", 
                                     "Bultos"), 
                        padre = self.wids['ventana'])
        if idproducto < 0:
            return None
        else:
            return idproducto

    def rellenar_widgets(self):
        """
        Introduce la información del producto actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        producto = self.objeto
        productos = pclases.ProductoVenta.select(
            pclases.ProductoVenta.q.camposEspecificosEspecialID != None, 
            orderBy='id')
        productos_count = productos.count()
        yo_index = pclases.SQLlist(productos).index(producto) + 1
        self.wids['ventana'].set_title(
            "Productos de venta: ESPECIAL - %s (%d de %d)" % (
                producto.descripcion, 
                yo_index, 
                productos_count))

        self.wids['i_barcode'].set_from_file(EanBarCode().getImage(
            producto.codigo))
        self.wids['e_codigo'].set_text(producto.codigo)
        self.wids['e_descripcion'].set_text(producto.descripcion)
        self.wids['e_nombre'].set_text(producto.nombre)
        self.wids['e_precio'].set_text(str(producto.preciopordefecto))
        self.wids['e_minimo'].set_text(str(producto.minimo))
        self.wids['e_arancel'].set_text(str(producto.arancel))
        self.wids['e_prodestandar'].set_text(utils.float2str(producto.prodestandar))
        campos = producto.camposEspecificosEspecial
        self.wids['e_stock'].set_text(utils.float2str(campos.stock))
        self.wids['e_existencias'].set_text(str(campos.existencias))
        try:
            pesobulto = utils.float2str(producto.calcular_razon_bultos())
        except (ValueError, TypeError):
            pesobulto = "N/A"
        self.wids['e_razon'].set_text(pesobulto)
        self.wids['e_unidad'].set_text(campos.unidad)
        self.wids['e_observaciones'].set_text(campos.observaciones)
        # Datos no modificables:
        self.wids['e_idproducto'].set_text(`producto.id`)
        self.mostrar_especificos()
        self.rellenar_tabla_tarifas()
        self.rellenar_existencias_almacen(producto)
        self.objeto.make_swap()
        self.objeto.camposEspecificosEspecial.make_swap()
        # Sombreado de botones anterior-siguiente
        anteriores = pclases.ProductoVenta.select(pclases.AND(
            pclases.ProductoVenta.q.camposEspecificosEspecialID != None, 
            pclases.ProductoVenta.q.id < producto.id),orderBy='-id').count()
        siguientes = pclases.ProductoVenta.select(pclases.AND(
            pclases.ProductoVenta.q.camposEspecificosEspecialID != None, 
            pclases.ProductoVenta.q.id > producto.id),orderBy='id').count()
        self.wids['b_anterior'].set_sensitive(anteriores)
        self.wids['b_siguiente'].set_sensitive(siguientes)

    def rellenar_tabla_tarifas(self):
        model = self.wids['tv_tarifas'].get_model()
        model.clear()
        for t in pclases.Tarifa.select():
            model.append((t.nombre, t.obtener_precio(self.objeto), t.id))
            
    def mostrar_especificos(self):
        """
        Muestra los datos específicos del producto.
        Elimina los hijos que componen la tabla 
        antes de insertar los nuevos.
        """
        hijos = self.wids['tabla'].get_children()
        for hijo in hijos:
            hijo.destroy()
        producto = self.objeto
        filas = len(producto.camposEspecificos)
        if filas == 0: 
            filas = 1   # Para evitar el "assert". De todas formas aunque sea de 1x2, si no hay datos específicos no se va a mostrar nada.
        self.wids['tabla'].resize(filas, 2)
        y = 0   # Fila donde insertar el campo.
        for campo in producto.camposEspecificos:
            label = gtk.Label("%s: " % campo.nombre)
            entry = gtk.Entry()
            entry.set_text(campo.valor)
            entry.set_has_frame(False)
            entry.set_editable(False)
            self.wids['tabla'].attach(label, 0, 1, y, y+1)
            self.wids['tabla'].attach(entry, 1, 2, y, y+1)
            label.show()
            entry.show()
            y += 1

    def calcular_digitoc(self, cod):
        #def sup(n):
        #    return ((n+9)/10)*10
        #peso = 1
        #suma = 0
        #for d in cod:
        #    suma += int(d) * peso
        #    if peso == 1:
        #        peso = 3
        #    else:
        #        peso = 1
        #return str(sup(suma) - suma)
        pesos = [1, 3]*6
        magic = 10
        suma = 0
        for i in range(12):
            try:
                suma = suma + int(cod[i]) * pesos[i]
            except ValueError:  # Sustituyo caracteres no numéricos
                suma = suma + (ord(cod[i] - ord("0")) % 10) * pesos[i]
        z = (magic - (suma % magic)) % magic
        if z < 0 or z >= magic:
            return None
        return str(z)

    def buscar_cod_libre(self):
        """
        Devuelve un código de tres cifras como 
        cadena que no esté ya en la tabla de 
        productos como producto terminado.
        Siempre devolverá el primer código
        libre más cercano a 000.
        Si no quedan más mostrará un mensaje
        de error por pantalla y devolverá
        999.
        """
        prods = pclases.ProductoVenta.select(pclases.AND(
            pclases.OR(
                pclases.ProductoVenta.q.camposEspecificosBalaID !=None, 
                pclases.ProductoVenta.q.camposEspecificosRolloID !=None, 
                pclases.ProductoVenta.q.camposEspecificosEspecialID !=None), 
            pclases.ProductoVenta.q.codigo.startswith('843603219')))
        codsproducto = [p.codigo[-4:-1] for p in prods]
        codsproducto.sort()
        for i in xrange(1000):  # Si el subcódigo de producto del EAN-13 está 
            # duplicado esto no funcionará. Añadida restricción UNIQUE en la 
            # BD para evitarlo.
            # print i, int(codsproducto[i])
            try:
                if i != int(codsproducto[i]):
                    return "%03d" % i
            except IndexError:  # No hay o me pasé de rango
                return "%03d" % i
        utils.dialogo_info('NO QUEDAN CÓDIGOS DISPONIBLES', 
                           'Todos los códigos EAN13 fueron asignados.',
                           padre = self.wids['ventana'])
        return '999'

    def generar_codigo_ean(self):
        """
        Genera un código EAN-13 completo, dígito control
        incluido, dentro del rango asignado a Geotexan.
        """
        codpais = '84'
        codempresa = '3603219'
        codproducto = self.buscar_cod_libre()
        codtemp = codpais+codempresa+codproducto 
        digitoc = self.calcular_digitoc(codtemp)
        return codtemp + digitoc
        
    def crear_nuevo_producto(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        producto = self.objeto
        if producto != None:
            producto.notificador.desactivar()
            producto.camposEspecificosEspecial.notificador.desactivar()
        campos = pclases.CamposEspecificosEspecial(unidad = '',
                                                   observaciones = '',
                                                   stock = 0.0,
                                                   existencias = 0)
        pclases.Auditoria.nuevo(campos, self.usuario, __file__)
        producto = pclases.ProductoVenta(lineaDeProduccion = None,
                                         camposEspecificosBala = None,
                                         camposEspecificosRollo = None, 
                                         camposEspecificosEspecial = campos,
                                         codigo = self.generar_codigo_ean(), 
                                         nombre = '',
                                         descripcion = '', 
                                         preciopordefecto = 0, 
                                         minimo = 0,
                                         arancel = '')
        pclases.Auditoria.nuevo(producto, self.usuario, __file__)
        self._objetoreciencreado = producto
        utils.dialogo_info('PRODUCTO CREADO', 
                           'Se ha creado un producto nuevo.\n\n\nA continuación complete la información del producto y guarde los cambios.\n', 
                           padre = self.wids['ventana'])
        producto.notificador.activar(self.aviso_actualizacion)
        producto.camposEspecificosEspecial.notificador.activar(self.aviso_actualizacion)
        self.objeto = producto
        self.activar_widgets(True)
        self.actualizar_ventana()

    def buscar_producto(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        producto = self.objeto
        a_buscar = utils.dialogo_entrada(titulo = "BUSCAR PRODUCTO", 
                                         texto = "Introduzca código, nombre o descripción de producto:", 
                                         padre = self.wids['ventana']) 
        if a_buscar != None:
            try:
                ida_buscar = int(a_buscar)
            except ValueError:
                ida_buscar = -1
            criterio = pclases.OR(pclases.ProductoVenta.q.codigo.contains(a_buscar),
                                    pclases.ProductoVenta.q.descripcion.contains(a_buscar),
                                    pclases.ProductoVenta.q.nombre.contains(a_buscar),
                                    pclases.ProductoVenta.q.id == ida_buscar)
            criterio = pclases.AND(criterio, pclases.ProductoVenta.q.camposEspecificosEspecialID != None)
            resultados = pclases.ProductoVenta.select(criterio)
            if resultados.count() > 1:
                    ## Refinar los resultados
                    idproducto = self.refinar_resultados_busqueda(resultados)
                    if idproducto == None:
                        return
                    resultados = [pclases.ProductoVenta.get(idproducto)]
                    # Se supone que la comprensión de listas es más rápida que hacer un nuevo get a SQLObject.
                    # Me quedo con una lista de resultados de un único objeto ocupando la primera posición.
                    # (Más abajo será cuando se cambie realmente el objeto actual por este resultado.)
            elif resultados.count() < 1:
                    ## Sin resultados de búsqueda
                    utils.dialogo_info('SIN RESULTADOS', 'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.\n(Atención: Ver la lista completa puede resultar lento si el número de elementos es muy alto)',
                                       padre = self.wids['ventana'])
                    return
            ## Un único resultado
            # Primero anulo la función de actualización
            if producto != None:
                producto.notificador.desactivar()
                producto.camposEspecificosEspecial.notificador.desactivar()
            # Pongo el objeto como actual
            try:
                producto = resultados[0]
                # Al borrar alguien desde otro ordenador un producto, me ha saltado a mí esta excepción al buscar en mi ventana 
                # otro producto que ni siquiera tenía nada que ver. Creo que es porque la consulta de la búsqueda anterior al 
                # borrado no se refresca al volver a buscar. Sospecho. Si se cierra y vuelve a abrir la ventana, no hay problemas.
                # Traceback (most recent call last):
                #   File "./productos_de_venta_rollos.py", line 473, in buscar_producto
                #     producto = resultados[0]
                # IndexError: list index out of range
            except IndexError:
                utils.dialogo_info(titulo = "ERROR", 
                                   texto = "Se produjo un error al recuperar la información.\nCierre y vuelva a abrir la ventana antes de volver a intentarlo.", 
                                   padre = self.wids['texto'])
                return
            # Y activo la función de notificación:
            producto.notificador.activar(self.aviso_actualizacion)
            producto.camposEspecificosEspecial.notificador.activar(self.aviso_actualizacion)
            self.activar_widgets(True)
        self.objeto = producto
        self.actualizar_ventana()

    def guardar(self, widget):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        producto = self.objeto
        codigo = self.wids['e_codigo'].get_text()
        if len(codigo) < 12:
            utils.dialogo_info(titulo = "CÓDIGO DEMASIADO CORTO", 
                               texto = "El código debe tener 13 dígitos para ajustarse al formato EAN-13.\nSe va a completar con ceros.", 
                               padre = self.wids['ventana'])
            codigo += "0" * (12 - len(codigo))  # Completo hasta 12 para que después se le haga la suma de control.
        if len(codigo) == 12:
            codigo = codigo + self.calcular_digitoc(codigo)
        if len(codigo) > 13:
            utils.dialogo_info(titulo = "CÓDIGO INCORRECTO", 
                               texto = "Código EAN-13 incorrecto. Debe tener exactamente 13 dígitos.\nPuede introducir 12 y dejar que se calcule atomáticamente el dígito de control, si le es más cómodo.\n\nA continuación se va a recortar el código a 13 dígitos y se intentará comprobar la suma de control.", 
                               padre = self.wids['ventana'])
            codigo = codigo[:13]
        if len(codigo) == 13:
            digitocontrol = self.calcular_digitoc(codigo[:12])
            if codigo[12] != digitocontrol:
                utils.dialogo_info(titulo = "FALLÓ SUMA DE COMPROBACIÓN", 
                                   texto = "El dígito de control no es correcto. Se corregirá automáticamente.", 
                                   padre = self.wids['ventana'])
                codigo = codigo[:12] + digitocontrol
        descripcion = self.wids['e_descripcion'].get_text()
        # idlinea Un producto pertenece a una línea, no se puede cambiar
        nombre = self.wids['e_nombre'].get_text()
        arancel = self.wids['e_arancel'].get_text()
        try:
            precio = float(self.wids['e_precio'].get_text())
        except ValueError:
            precio = producto.preciopordefecto
        try:
            minimo = float(self.wids['e_minimo'].get_text())
        except ValueError:
            minimo = producto.minimo
        try:
            stock = utils._float(self.wids['e_stock'].get_text())
        except ValueError:
            stock = producto.camposEspecificosEspecial.stock
        try:
            existencias = int(self.wids['e_existencias'].get_text())
        except:
            existencias = producto.camposEspecificosEspecial.existencias
        # TODO: Falta ajustar los almacenes a la nueva cantidad en existencias.
        unidad = self.wids['e_unidad'].get_text()
        observaciones = self.wids['e_observaciones'].get_text()
 
        # Desactivo el notificador momentáneamente
        producto.notificador.activar(lambda: None)
        producto.camposEspecificosEspecial.notificador.activar(lambda: None)
        # Actualizo los datos del objeto
        try:
            producto.codigo = codigo
        except psycopg_ProgrammingError:
            try:
                producto_asignado = pclases.ProductoVenta.select(pclases.ProductoVenta.q.codigo == codigo)[0]
                producto_asignado = producto_asignado.descripcion
            except IndexError:
                producto_asignado = "?"
            utils.dialogo_info(titulo = "CÓDIGO DUPLICADO", 
                               texto = "El código EAN %s no se encuentra disponible.\nActualmente está asignado a: %s" % (codigo, producto_asignado), 
                               padre = self.wids['ventana'])
        producto.descripcion = descripcion
        producto.nombre = nombre
        producto.preciopordefecto = precio
        producto.minimo = minimo
        producto.arancel = arancel
        producto.camposEspecificosEspecial.stock = stock
        producto.camposEspecificosEspecial.unidad = unidad
        producto.camposEspecificosEspecial.observaciones = observaciones 
        producto.camposEspecificosEspecial.existencias = existencias
        # Fuerzo la actualización de la BD y no espero a que SQLObject lo haga por mí:
        producto.syncUpdate()
        # Vuelvo a activar el notificador
        producto.notificador.activar(self.aviso_actualizacion)
        producto.camposEspecificosEspecial.notificador.activar(self.aviso_actualizacion)
        self.actualizar_ventana()
        self.wids['b_guardar'].set_sensitive(False)

    def borrar_producto(self, widget):
        """
        Elimina el producto de la tabla pero NO
        intenta eliminar ninguna de sus relaciones,
        de forma que si se incumple alguna 
        restricción de la BD, cancelará la eliminación
        y avisará al usuario.
        """
        producto = self.objeto
        if not utils.dialogo('¿Eliminar el producto?', 'BORRAR', padre = self.wids['ventana']):
            return
        if producto.articulos != [] or producto.precios != []:
            utils.dialogo_info('PRODUCTO NO ELIMINADO', 
                               'El producto está implicado en operaciones que impiden su borrado.', 
                               padre = self.wids['ventana'])
        else:
            producto.notificador.desactivar()
            producto.camposEspecificosEspecial.notificador.desactivar()
            cee = producto.camposEspecificosEspecial
            producto.camposEspecificosEspecial = None
            try:
                producto.destroy(ventana = __file__)
            except:
                producto.camposEspecificosEspecial = cee
                utils.dialogo_info(titulo = "PRODUCTO NO BORRADO", 
                                   texto = "El producto no se pudo eliminar",
                                   padre = self.wids['ventana'])
                self.actualizar_ventana()
                return
            cee.destroy(ventana = __file__)
            self.objeto = None
            self.ir_a_primero()

    def ver_tarifas(self, w):
        from formularios import tarifas_de_precios
        v = tarifas_de_precios.TarifasDePrecios()  # @UnusedVariable

    def add_campoesp(self, w):
        campo = utils.dialogo_entrada('Introduzca nombre del campo:', 'NOMBRE', padre = self.wids['ventana'])
        if campo:
            valor = utils.dialogo_entrada('Introduzca valor del campo:', 'VALOR', padre = self.wids['ventana'])
            if valor:
                producto = self.objeto
                ce = pclases.CamposEspecificos(productoVenta = producto,
                                             nombre = campo,
                                             valor = valor)
                pclases.Auditoria.nuevo(ce, self.usuario, __file__)
                self.mostrar_especificos()

    def seleccionar_campoesp(self, campos):
        ops = [(c.id, c.nombre) for c in campos]
        return utils.dialogo_combo('SELECCIONE CAMPO', 
                                   'Seleccione un campo al que camiar el valor o eliminar.\nSi desea cambiar el nombre del campo debe eliminarlo\ny crear uno nuevo con el nuevo nombre.\n',
                                   ops,
                                   padre = self.wids['ventana'])

    def drop_campoesp(self, w):
        producto = self.objeto
        idce = self.seleccionar_campoesp(producto.camposEspecificos)
        if idce == None:
            return
        ce = pclases.CamposEspecificos.get(idce)
        ce.destroy(ventana = __file__)
        self.mostrar_especificos()

    def change_campoesp(self, w):
        producto = self.objeto
        idce = self.seleccionar_campoesp(producto.camposEspecificos)
        if idce == None:
            return
        valor = utils.dialogo_entrada('Introduzca valor del campo:', 'VALOR')
        if valor == None:
            return
        ce = pclases.CamposEspecificos.get(idce)
        ce.valor = valor
        self.mostrar_especificos()

if __name__ == "__main__":
    p = ProductosDeVentaEspecial()
