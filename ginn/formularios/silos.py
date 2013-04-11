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
## silos.py - Control de silos.
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 1 de noviembre de 2006 -> Inicio
## 
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sqlobject
try:
    from framework import pclases
except ImportError:
    import sys
    from os.path import join as pathjoin
    sys.path.append(pathjoin("..", "framework"))
    from framework import pclases
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes
from utils import _float as float
import pango
from ventana_progreso import VentanaActividad, VentanaProgreso


class Silos(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'silos.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_nuevo/clicked': self.nuevo,
                       'b_borrar/clicked': self.borrar,
                       'b_actualizar/clicked': self.rellenar_widgets, 
                      }  
        self.add_connections(connections)
        self.inicializar_ventana()
        self.rellenar_widgets()
        gtk.main()

    # --------------- Funciones auxiliares ------------------------------
    def es_diferente(self):
        """
        Devuelve True si la información en pantalla es distinta a la
        del objeto en memoria.
        """
        return False 

    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        # Inicialmente no se muestra NADA. Sólo se le deja al
        # usuario la opción de buscar o crear nuevo.
        self.activar_widgets(True)

    def activar_widgets(self, s):
        """
        Activa o desactiva (sensitive=True/False) todos 
        los widgets de la ventana que dependan del 
        objeto mostrado.
        Entrada: s debe ser True o False. En todo caso
        se evaluará como boolean.
        """
        ws = ('hbox', 'b_nuevo', 'b_borrar')
        # for w in ws:
        #     self.wids[w].set_sensitive(s)

    def rellenar_widgets(self, boton = None):
        """
        Introduce la información del silo actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        self.wids['ch_debug'].set_property("visible", 
            self.usuario == None or self.usuario.nivel <= 1)
        silos = pclases.Silo.select(orderBy = "nombre")
        box = self.wids['hbox']
        box.set_spacing(15)
        for child in box.get_children():
            child.destroy()
        for silo in silos:
            nombresilo = silo.nombre.replace(" ", "_")
            vbox = gtk.VBox(spacing = 15)
            self.wids['vbox_%s' % (nombresilo)] = vbox
            self.wids['lnombre_%s' % (nombresilo)] = gtk.Label(silo.nombre)
            font_desc = pango.FontDescription("Sans Bold 12")
            self.wids['lnombre_%s' % (nombresilo)].modify_font(font_desc)
            self.wids['lcapacidad_%s' % (nombresilo)] = gtk.Label("Capacidad: %s" % (utils.float2str(silo.capacidad, 1)))
            self.wids['lcarga_%s' % (nombresilo)] = gtk.Label("Carga actual: %s" % (utils.float2str(silo.ocupado, 1)))
            self.wids['b_ajustar_%s' % (nombresilo)] = gtk.Button(label = "Ajustar")
            self.wids['b_ajustar_%s' % (nombresilo)].connect("clicked", self.ajustar_silo, silo)
            self.wids['b_mostrar_%s' % (nombresilo)] = gtk.Button(label = "Ver detalle")
            self.wids['b_mostrar_%s' % (nombresilo)].connect("clicked", self.mostrar_silo, silo)
            contenidobox = gtk.HBox(spacing = 10)
            self.wids['progress_%s' % (nombresilo)] = gtk.ProgressBar()
            try:
                fraccion = max(0.0, min(1.0, silo.ocupado / silo.capacidad))
            except ZeroDivisionError:
                fraccion = 0
            self.wids['progress_%s' % (nombresilo)].set_fraction(fraccion) 
            self.wids['progress_%s' % (nombresilo)].set_orientation(gtk.PROGRESS_BOTTOM_TO_TOP)
            contenidobox.add(self.wids['progress_%s' % (nombresilo)])
            self.wids['vboxcarga_%s' % (nombresilo)] = gtk.VBox()
            contenidobox.add(self.wids['vboxcarga_%s' % (nombresilo)])
            if self.wids['ch_debug'].get_active():
                ocupacion = silo._get_ocupacion()
            else:
                ocupacion = silo.ocupacion
            for producto in ocupacion:
                eventbox = gtk.EventBox()
                label = gtk.Label("%s\n%s" % (
                    producto.descripcion.upper().replace("GRANZA", "").strip(),
                    utils.float2str(ocupacion[producto], 1)))
                fuente = pango.FontDescription("Sans Oblique 8")
                label.modify_font(fuente)
                eventbox.add(label)
                style = eventbox.get_style().copy()
                style.bg[gtk.STATE_NORMAL] = eventbox.get_colormap().alloc_color(get_color_producto(producto.id))
                eventbox.set_style(style)
                self.wids['vboxcarga_%s' % (nombresilo)].add(eventbox)
            vbox.pack_start(self.wids['lnombre_%s' % (nombresilo)], expand = False)
            vbox.pack_start(self.wids['lcapacidad_%s' % (nombresilo)], expand = False)
            vbox.pack_start(self.wids['lcarga_%s' % (nombresilo)], expand = False)
            vbox.pack_start(self.wids['b_ajustar_%s' % (nombresilo)], expand = False)
            vbox.pack_start(self.wids['b_mostrar_%s' % (nombresilo)], expand = False)
            vbox.pack_start(contenidobox, expand = True)
            box.add(vbox)
        box.show_all()

    def leer_datos_cargas_descargas(self, silo):
        """
        Devuelve las cargas y descargas (consumo) del silo 
        agrupadas por fecha en un diccionario de la forma:
        {fecha1: {'cargas': [cargaSilo1, cargaSilo2...], 
                  'descargas': [consumo1, consumo2...]}, 
         fecha2: {'cargas': [], 
                  'descargas': [consumo3, ...]}
        }
        """
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        i = 0.0
        tot = len(silo.cargasSilo) + len(silo.consumos)
        datos = {}
        for carga in silo.cargasSilo:
            vpro.set_valor(i/tot, 'Analizando cargas...')
            i += 1
            if carga.fechaCarga not in datos:
                datos[carga.fechaCarga] = {'cargas': [carga, ], 'descargas': []}
            else:
                datos[carga.fechaCarga]['cargas'].append(carga)
        for descarga in silo.consumos:
            vpro.set_valor(i/tot, 'Analizando consumos...')
            i += 1
            if descarga.parteDeProduccionID != None:
                fecha = descarga.parteDeProduccion.fecha
            else:
                fecha = None
            if fecha not in datos:
                datos[fecha] = {'cargas': [], 'descargas': [descarga, ]}
            else:
                datos[fecha]['descargas'].append(descarga)
        vpro.ocultar()
        return datos


    def mostrar_silo(self, boton, silo):
        """
        Recibe el silo del que hay que mostrar el detalle de 
        cargas y descargas (consumos) y muestra una ventana con las 
        mismas ordenadas por fecha.
        """
        cd_fechas = self.leer_datos_cargas_descargas(silo)
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        i = 0.0
        tot = len(cd_fechas)
        datos = []
        fechas = cd_fechas.keys()
        fechas.sort()
        total_cargado = 0
        total_descargado = 0
        for fecha in fechas:
            vpro.set_valor(i/tot, 'Analizando movimientos...')
            i = i+1
            str_fecha = utils.str_fecha(fecha)
            for carga in cd_fechas[fecha]['cargas']:
                datos.append((str_fecha, carga.productoCompra.descripcion, 
                              utils.float2str(carga.cantidad), "", "", ""))
                total_cargado += carga.cantidad
            for descarga in cd_fechas[fecha]['descargas']: 
                producto_fabricado = "CLIC PARA VER [%d]" % (descarga.id)
                datos.append((str_fecha, "", "", 
                              descarga.productoCompra.descripcion, 
                              utils.float2str(descarga.cantidad), 
                              producto_fabricado))
                total_descargado += descarga.cantidad
        datos.append(("", "TOTAL CARGAS: ", utils.float2str(total_cargado), 
                      "TOTAL CONSUMOS: ", utils.float2str(total_descargado), 
                      ""))
        vpro.ocultar()
        utils.dialogo_resultado(datos, 
            titulo = "DETALLE DE CARGAS Y CONSUMOS DEL SILO", 
            padre = self.wids['ventana'], 
            cabeceras = ("Fecha", "Producto cargado", "Cantidad cargada", 
                         "Producto consumido", "Cantidad consumida", 
                         "Producto fabricado"), 
            func_change = self.mostrar_info_producto_fabricado)

    def mostrar_info_producto_fabricado(self, tv):
        """
        Muestra el producto fabricado en el registro consumo 
        donde se ha hecho clic.
        """
        model, iter = tv.get_selection().get_selected()
        if iter != None and "CLIC PARA VER" in model[iter][-1]:
            s = model[iter][-1]
            idconsumo = s[s.rindex("[")+1: s.rindex("]")]
            descarga = pclases.Consumo.get(int(idconsumo))
            pdp = descarga.parteDeProduccion
            if pdp != None:
                producto_fabricado = pdp.productoVenta
            else:
                producto_fabricado = None
            producto_fabricado = producto_fabricado and producto_fabricado.descripcion or ""
            model[iter][-1] = producto_fabricado
        
    def ajustar_silo(self, boton, silo):
        """
        Recibe el silo que hay que ajustar.
        """
        if self.usuario != None and self.usuario.nivel >= 2:
            utils.dialogo_info(titulo = "USUARIO SIN PRIVILEGIOS", 
                               texto = "No tiene permiso para ajustar los silos.", 
                               padre = self.wids['ventana'])
        else:
            cantidad = utils.dialogo_entrada(titulo = "AJUSTAR SILO", 
                                             texto = "Introduzca la cantidad real que hay en el silo %s." % (silo.nombre), 
                                             padre = self.wids['ventana'])
            if cantidad != None:
                try:
                    cantidad = float(cantidad)
                except:
                    utils.dialogo_info(titulo = "CANTIDAD INCORRECTA", 
                                       texto = "El texto %s no es correcto." % (cantidad), 
                                       padre = self.wids['ventana'])
                else:
                    txt = """
                    Puede corregir la carga del silo sin modificar las existencias                  
                    de los productos que contiene. Esto solo es recomendable                        
                    cuando las existencias son correctas pero hay un desajuste                      
                    únicamente en la medición del silo. Responda «NO» si ese es                     
                    el caso.                                                                        
                                                                                                    
                    ¿Desea modificar las existencias de los productos contenidos                    
                    en el silo? 
                    """
                    modificar_existencias = utils.dialogo(titulo = "¿MODIFICAR EXISTENCIAS?", texto = txt, padre = self.wids['ventana'])
                    en_el_silo = silo.ajustar(cantidad, modificar_existencias)
                    if en_el_silo == -1:
                        utils.dialogo_info(titulo = "SILO NO AJUSTADO", 
                                           texto = "El silo debe haber sido cargado al menos una vez.", 
                                           padre = self.wids['ventana'])
                self.rellenar_widgets()
    
    def nuevo(self, widget):
        """
        Función callback del botón b_nuevo.
        Pide los datos básicos para crear un nuevo objeto.
        Una vez insertado en la BD hay que hacerlo activo
        en la ventana para que puedan ser editados el resto
        de campos que no se hayan pedido aquí.
        """
        silo = self.objeto
        nombre = utils.dialogo_entrada('Introduzca el nombre del silo:', 'NOMBRE', padre = self.wids['ventana'])
        if nombre != None:
            capacidad = utils.dialogo_entrada(titulo = "CAPACIDAD", 
                                              texto = "Introduzca la capacidad del silo:",
                                              padre = self.wids['ventana'])
            try:
                capacidad = float(capacidad)
            except:
                utils.dialogo_info(titulo = "VALOR INCORRECTO",
                                   texto = "El valor %s no es correcto. Inténtelo de nuevo.\nAsegúrese de no introducir unidades.", 
                                   padre = self.wids['ventana'])
                return
            observaciones = utils.dialogo_entrada(titulo = "OBSERVACIONES", 
                                                  texto = "Introduzca observaciones si lo desea:", 
                                                  padre = self.wids['ventana'])
            if observaciones != None:
                silo = pclases.Silo(nombre = nombre,
                                    capacidad = capacidad, 
                                    observaciones = observaciones)
                pclases.Auditoria.nuevo(silo, self.usuario, __file__)
                self.rellenar_widgets()

    def borrar(self, widget):
        """
        Elimina un silo.
        Pregunta con un diálogo combo cuál de ellos borrar.
        """
        opciones = [(s.id, s.nombre) for s in pclases.Silo.select()]
        idsilo = utils.dialogo_combo(titulo = "SELECCIONAR SILO", 
                                     texto = "Seleccione silo a eliminar:", 
                                     ops = opciones, 
                                     padre = self.wids['ventana'])
        if idsilo != None:
            silo = pclases.Silo.get(idsilo)
            try:
                silo.destroy(ventana = __file__)
            except:
                utils.dialogo_info(titulo = "SILO NO BORRADO", 
                                   texto = "El silo no se pudo eliminar.\nProbablemente esté implicado en cargas y consumos.", 
                                   padre = self.wids['ventana'])
                return
            self.rellenar_widgets()
        
def get_color_producto(n):
    colores = ("#AAFFFF", "#FFFFAA", "#AAFFAA", "#AAAAFF", "#FFAAAA", "#FFAAFF", "#FFBBAA", "#BB00FF", "#AA11FF", "#AABBCC", "#FF22EE") 
    if n != None:
        n = n % len(colores)
        return colores[n]
    else:
        return "white"


if __name__ == '__main__':
    v = Silos()

