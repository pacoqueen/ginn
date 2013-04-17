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
## productos_venta_rollos_geocompuestos.py 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 9 de octubre de 2005 -> Inicio 
## 9 de octubre de 2005 -> 90% funcional (faltan fichas de prod.)
## 9 de enero de 2006 -> Separo productos de venta del resto.
## 23 de enero de 2006 -> Portado a clase.
###################################################################
## TODO:
## - NO ESTÁ PROBADO en absoluto. No usar en producción. Tiene 
##   bastantes bugs (de momento no supone un gran problema, ya que
##   la línea de geocompuestos de la fábrica sigue sin 
##   inaugurarse).
## - Tampoco aparece el campo de producción estándar (nuevo del 25
##   de septiembre de 2006).
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
from utils import _float as float


class ProductosDeVentaRollosGeocompuestos(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self._objetoreciencreado = None
        Ventana.__init__(self, 'productos_de_venta_rollos_geocompuestos.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_anterior/clicked':self.ir_a_anterior,
                       'b_siguiente/clicked':self.ir_a_siguiente,
                       'b_contar/clicked' : self.muestra_stock,
                       'b_fichas/clicked': self.ver_ficha,
                       'b_articulos/clicked': self.ver_articulos,
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
        gtk.main()

    # --------------- Funciones auxiliares ------------------------------
    def es_diferente(self):
        """
        Devuelve True si la información en pantalla es distinta a la
        del objeto en memoria.
        """
        producto = self.objeto
        if producto == None: return False   # Si no hay producto activo, devuelvo que no hay cambio respecto a la ventana
        # Datos a comparar:
        # - código <-> e_codigo
        # - descripción <-> e_descripcion
        # - nombre <-> e_nombre
        # - preciopordefecto <-> e_precio
        # - minimo <-> e_minimo
        condicion = producto.codigo == self.wids['e_codigo'].get_text()
        # print condicion
        condicion = condicion and (producto.descripcion == self.wids['e_descripcion'].get_text())
        condicion = condicion and (producto.nombre == self.wids['e_nombre'].get_text())
        condicion = condicion and (str(producto.preciopordefecto) == self.wids['e_precio'].get_text())
        condicion = condicion and (str(producto.minimo) == self.wids['e_minimo'].get_text())
        condicion = condicion and (str(producto.arancel) == self.wids['e_arancel'].get_text())
        condicion = condicion and (str(producto.camposEspecificosRollo.gramos) == self.wids['e_gramos'].get_text())
        condicion = condicion and (str(producto.camposEspecificosRollo.codigoComposan) == self.wids['e_composan'].get_text())
        condicion = condicion and (str(producto.camposEspecificosRollo.metrosLineales) == self.wids['e_metros_lineales'].get_text())
        condicion = condicion and (str(producto.camposEspecificosRollo.ancho) == self.wids['e_ancho'].get_text())
        condicion = condicion and (str(producto.camposEspecificosRollo.diametro) == self.wids['e_diametro'].get_text())
        condicion = condicion and (str(producto.camposEspecificosRollo.rollosPorCamion) == self.wids['e_rollo_camion'].get_text())
        return not condicion    # Concición verifica que sea igual

    def aviso_actualizacion(self):
        """
        Muestra una ventana modal con el mensaje de objeto 
        actualizado.
        """
        utils.dialogo_info('ACTUALIZAR',
                           'El producto ha sido modificado remotamente.\nDebe actualizar la información mostrada en pantalla.\nPulse el botón «Actualizar»')
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

    def activar_widgets(self, s, chequear_permisos = True):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        ws = ('e_idproducto', 'e_codigo', 'e_descripcion', 'e_nombre', 'e_precio', 'e_minimo', 'e_stock', 'b_contar', 
              'e_gramos' , 'e_composan', 'e_diametro' , 'e_ancho' , 'e_rollo_camion', 'e_metros_lineales', 'b_borrar', 
              'b_fichas', 'b_articulos','b_tarifas','e_arancel', 'b_anterior', 'b_siguiente', 'frame2') 
        for w in ws:
            self.wids[w].set_sensitive(s)
        if chequear_permisos:
            self.check_permisos(nombre_fichero_ventana = "productos_de_venta_rollos_geocompuestos.py")

    def ir_a_primero(self):
        """
        Hace que el primer registro -si lo hay- de la tabla implicada
        en el objeto del formulario sea el objeto activo.
        """
        producto = self.objeto
        try:
            # Anulo el aviso de actualización del envío que deja de ser activo.
            linea = pclases.LineaDeProduccion.select(pclases.OR(
                pclases.LineaDeProduccion.q.nombre.contains('geocompuesto'), 
                pclases.LineaDeProduccion.q.nombre.contains('comercializado'))
            )[0]
            if producto != None: producto.notificador.desactivar()
            producto = pclases.ProductoVenta.select(pclases.AND(pclases.ProductoVenta.q.camposEspecificosRolloID != None,pclases.ProductoVenta.q.lineaDeProduccionID == linea.id))[0]  # Selecciono todos y me quedo con el primero de la lista
            producto.notificador.activar(self.aviso_actualizacion)      # Activo la notificación
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
                                       texto = 'Los cambios no se pudieron guardar automáticamente.\nDebe hacerlo de forma manual')
                    return 
        producto = self.objeto
        linea = pclases.LineaDeProduccion.select(pclases.OR(
            pclases.LineaDeProduccion.q.nombre.contains('geocompuesto'), 
            pclases.LineaDeProduccion.q.nombre.contains('comercializado')))[0]
        try:
            anterior = pclases.ProductoVenta.select(pclases.AND(pclases.ProductoVenta.q.camposEspecificosRolloID != None, pclases.ProductoVenta.q.lineaDeProduccionID == linea.id, pclases.ProductoVenta.q.id < producto.id),orderBy='-id')[0]
        except IndexError:
            utils.dialogo_info(texto = "El elemento seleccionado es el primero registrado en el sistema",titulo="ERROR")
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
                                       texto = 'Los cambios no se pudieron guardar automáticamente.\nDebe hacerlo de forma manual')
                    return 
        producto = self.objeto
        linea = pclases.LineaDeProduccion.select(pclases.OR(
            pclases.LineaDeProduccion.q.nombre.contains('geocompuesto'), 
            pclases.LineaDeProduccion.q.nombre.contains('comercializado')))[0]
        try:
            siguiente = pclases.ProductoVenta.select(pclases.AND(pclases.ProductoVenta.q.camposEspecificosRolloID != None, pclases.ProductoVenta.q.lineaDeProduccionID == linea.id, pclases.ProductoVenta.q.id > producto.id),orderBy='id')[0]
        except IndexError:
            utils.dialogo_info(texto = "El elemento seleccionado es el último"
                                       " registrado en el sistema",
                               titulo = "ERROR", 
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
            filas_res.append((r.id, r.codigo, r.descripcion))
        idproducto = utils.dialogo_resultado(filas_res,
                                             titulo = 'Seleccione producto',
                                             cabeceras = ('ID Interno', 'Código', 'Descripción'))
        if idproducto < 0:
            return None
        else:
            return idproducto

    def rellenar_widgets(self):
        """
        Introduce la información del producto actual
        en los widgets.
        """
        if self.objeto != None:
            self.activar_widgets(True)
            producto = self.objeto
            self.wids['e_codigo'].set_text(producto.codigo)
            self.wids['e_descripcion'].set_text(producto.descripcion)
            self.wids['e_nombre'].set_text(producto.nombre)
            self.wids['e_precio'].set_text(str(producto.preciopordefecto))
            self.wids['e_minimo'].set_text(str(producto.minimo))
            self.wids['e_arancel'].set_text(str(producto.arancel))
            campos = producto.camposEspecificosRollo
            self.wids['e_ancho'].set_text(str(campos.ancho))
            self.wids['e_gramos'].set_text(str(campos.gramos))
            self.wids['e_metros_lineales'].set_text(str(campos.metrosLineales))
            self.wids['e_composan'].set_text(str(campos.codigoComposan))
            self.wids['e_diametro'].set_text(str(campos.diametro))
            self.wids['e_rollo_camion'].set_text(str(campos.rollosPorCamion))
            # Datos no modificables:
            self.wids['e_idproducto'].set_text(`producto.id`)
            self.muestra_stock()
            self.mostrar_especificos()
            self.objeto.make_swap()

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

    # --------------- Manejadores de eventos ----------------------------
    def muestra_stock(self, boton = None):
        """
        Escribe el stock del producto en el widget.
        """
        producto = self.objeto
        self.wids['e_stock'].set_text("%.2f m²" % round(producto.get_stock(),2))

    def calcular_digitoc(self, cod):
        def sup(n):
            return ((n+9)/10)*10
        peso = 1
        suma = 0
        for d in cod:
            suma += int(d) * peso
            if peso == 1:
                peso = 3
            else:
                peso = 1
        return str(sup(suma) - suma)

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
        prods = pclases.ProductoVenta.select(pclases.AND(pclases.ProductoVenta.q.camposEspecificosRolloID !=None, pclases.ProductoVenta.q.codigo.startswith('843603219')))
        codsproducto = [p.codigo[-4:-1] for p in prods]
        codsproducto.sort()
        for i in xrange(1000):
            try:
                if i != int(codsproducto[i]):
                    return "%03d" % i
            except IndexError:  # No hay o me pasé de rango
                return "%03d" % i
        utils.dialogo_info('NO QUEDAN CÓDIGOS DISPONIBLES', 'Todos los códigos EAN13 fueron asignados.')
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
        campos = pclases.CamposEspecificosRollo(gramos = 0,
                                            metrosLineales = 0,
                                            codigoComposan = '',
                                            ancho = 0,
                                            diametro = 0,
                                            rollosPorCamion = 0, 
                                            c = False, 
                                            modeloEtiqueta = None)
        pclases.Auditoria.nuevo(campos, self.usuario, __file__)
        linea = pclases.LineaDeProduccion.select(pclases.OR(
            pclases.LineaDeProduccion.q.nombre.contains('geocompuesto'), 
            pclases.LineaDeProduccion.q.nombre.contains('comercializado')))[0]
        producto = pclases.ProductoVenta(lineaDeProduccion = linea,
                                    camposEspecificosBala = None,
                                    camposEspecificosRollo = campos, 
                                    codigo = self.generar_codigo_ean(), 
                                    nombre = '',
                                    descripcion = '', 
                                    preciopordefecto = 0, 
                                    minimo = 0,
                                    arancel = '')
        pclases.Auditoria.nuevo(producto, self.usuario, __file__)
        self._objetoreciencreado = producto
        utils.dialogo_info('PRODUCTO CREADO', 
                           'Se ha creado un producto nuevo.\nA continuación complete la información del producto y guarde los cambios.', 
                           padre = self.wids['ventana'])
        producto.notificador.activar(self.aviso_actualizacion)
        self.objeto = producto
        self.actualizar_ventana()

    def buscar_producto(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        producto = self.objeto
        a_buscar = utils.dialogo_entrada("Introduzca código o descripción de producto:") 
        if a_buscar != None:
            try:
                ida_buscar = int(a_buscar)
            except ValueError:
                ida_buscar = -1
            criterio = pclases.OR(pclases.ProductoVenta.q.codigo.contains(a_buscar),
                                            pclases.ProductoVenta.q.descripcion.contains(a_buscar),
                                            pclases.ProductoVenta.q.id == ida_buscar)
            linea = pclases.LineaDeProduccion.select(pclases.OR(
             pclases.LineaDeProduccion.q.nombre.contains('geocompuesto'), 
             pclases.LineaDeProduccion.q.nombre.contains('comercializado')))[0]
            criterio = pclases.AND(criterio, 
                pclases.ProductoVenta.q.camposEspecificosRolloID != None, 
                pclases.ProductoVenta.q.lineaDeProduccionID == linea.id)
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
                    utils.dialogo_info('SIN RESULTADOS', 'La búsqueda no produjo resultados.\nPruebe a cambiar el texto buscado o déjelo en blanco para ver una lista completa.\n(Atención: Ver la lista completa puede resultar lento si el número de elementos es muy alto)')
                    return
            # # Un único resultado
            # Primero anulo la función de actualización
            if producto != None:
                producto.notificador.desactivar()
                # Pongo el objeto como actual
                producto = resultados[0]
                # Y activo la función de notificación:
                producto.notificador.activar(self.aviso_actualizacion)
        # self.activar_widgets(True)
        self.objeto = producto
        self.actualizar_ventana()

    def guardar(self, widget):
        """
        Guarda el contenido de los entry y demás widgets de entrada
        de datos en el objeto y lo sincroniza con la BD.
        """
        producto = self.objeto
        codigo = self.wids['e_codigo'].get_text()
        descripcion = self.wids['e_descripcion'].get_text()
        # idlinea Un producto pertenece a una línea, no se puede cambiar
        nombre = self.wids['e_nombre'].get_text()
        arancel = self.wids['e_arancel'].get_text()
        try:
            precio = float(self.wids['e_precio'].get_text().replace(',','.'))
        except ValueError:
            precio = producto.precio
        try:
            minimo = float(self.wids['e_minimo'].get_text())
        except ValueError:
            minimo = producto.minimo
        try:
            gramos = int(self.wids['e_gramos'].get_text())
        except ValueError:
            gramos = producto.camposEspecificosRollo.gramos
        try:
            ancho = float(self.wids['e_ancho'].get_text())
        except ValueError:
            ancho = producto.camposEspecificosRollo.ancho
        try:
            diametro = int(self.wids['e_diametro'].get_text())
        except ValueError:
            diametro = producto.camposEspecificosRollo.diametro
        try:
            metrosLineales = int(self.wids['e_metros_lineales'].get_text())
        except:
            metrosLineales = producto.camposEspecificosRollo.metrosLineales
        try:
            rolloCamion = int(self.wids['e_rollo_camion'].get_text())
        except ValueError:
            rolloCamion = producto.camposEspecificosRollo.rollosPorCamion
        composan = self.wids['e_composan'].get_text()
 
        # Desactivo el notificador momentáneamente
        producto.notificador.activar(lambda: None)
        # Actualizo los datos del objeto
        producto.codigo = codigo
        producto.descripcion = descripcion
        producto.nombre = nombre
        producto.preciopordefecto = precio
        producto.minimo = minimo
        producto.arancel = arancel
        producto.camposEspecificosRollo.gramos = gramos
        producto.camposEspecificosRollo.ancho = ancho
        producto.camposEspecificosRollo.diametro = diametro
        producto.camposEspecificosRollo.codigoComposan = composan
        producto.camposEspecificosRollo.rollosPorCamion = rolloCamion
        producto.camposEspecificosRollo.metrosLineales = metrosLineales
        # Fuerzo la actualización de la BD y no espero a que SQLObject lo haga por mí:
        producto.syncUpdate()
        # Vuelvo a activar el notificador
        producto.notificador.activar(self.aviso_actualizacion)
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
        if not utils.dialogo('¿Eliminar el producto?', 'BORRAR'):
            return
        if producto.articulos != [] or producto.precios != []:
            utils.dialogo_info('PRODUCTO NO ELIMINADO', 'El producto está implicado en operaciones que impiden su borrado.')
        else:
            producto.notificador.desactivar()
            cer = producto.camposEspecificosRollo
            producto.camposEspecificosRollo = None
            cer.destroy(ventana = __file__)
            producto.destroy(ventana = __file__)
            producto = None
            self.ir_a_primero()

    def ver_ficha(self, w):
        utils.dialogo_info(titulo = "NO IMPLEMENTADO", 
                           texto = "Funcionalidad no implementada", 
                           padre = self.wids['ventana'])
        #producto = self.objeto
        #from formularios import formulacion_geotextiles
        #formulacion_geotextiles.FormulacionGeotextiles(producto)

    def ver_articulos(self, w):
        """
        Muestra las existencias del artículo en el almacén
        """
        producto = self.objeto
        elementos = pclases.Articulo.select(pclases.AND(pclases.Articulo.q.albaranSalidaID == None,pclases.Articulo.q.productoVentaID == producto.id))
        utils.dialogo_info(titulo = 'EXISTENCIAS', texto = 'Hay %d unidades de %s en el almacén.\nEl mínimo es %d' % (elementos.count(),producto.descripcion,producto.minimo))
        
    def ver_tarifas(self, w):
        from formularios import tarifas_de_precios
        tarifas_de_precios.TarifasDePrecios()

    def add_campoesp(self, w):
        campo = utils.dialogo_entrada('Introduzca nombre del campo:', 'NOMBRE')
        if not campo:
            return
        valor = utils.dialogo_entrada('Introduzca valor del campo:', 'VALOR')
        if not valor:
            return
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
                                   ops)

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
    p = ProductosDeVentaRollosGeocompuestos()

