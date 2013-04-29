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
## consulta_productividad.py - Consultas de productividad de partes
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 16 de marzo de 2006 -> Inicio
###################################################################
## TODO: Es bastante lento. Optimizar las consultas.
##       Además, no sólo hay que mirar la fecha del parte. La hora
##       también influye para determinar a qué día laborable 
##       pertenece (y eso aquí no se tiene en cuenta).
###################################################################

from formularios.utils import _float as float
from framework import pclases
from ventana import Ventana
import gtk
import time
import mx.DateTime
import pygtk
from formularios import utils
pygtk.require('2.0')


class ConsultaProductividad(Ventana):
    inicio = None
    fin = None
    
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        global fin
        Ventana.__init__(self, 'consulta_productividad.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       'b_imprimir/clicked': self.imprimir, 
                       'b_exportar/clicked': self.exportar}
        self.add_connections(connections)
        cols = (('Fecha', 'gobject.TYPE_STRING', False, True, False, None),
                ('Inicio del turno', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Fin del turno', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Producción', 'gobject.TYPE_STRING', False, True, False, None),
                ('Productividad', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Idparte', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        self.wids['tv_datos'].connect("row-activated", self.abrir_parte)
        # XXX
        import gobject
        model = gtk.TreeStore(gobject.TYPE_STRING, 
                              gobject.TYPE_STRING, 
                              gobject.TYPE_STRING, 
                              gobject.TYPE_STRING,
                              gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT,
                              gobject.TYPE_INT64)
        self.wids['tv_datos'].set_model(model)
        model.set_sort_func(0, utils.funcion_orden, 0)
        cell = gtk.CellRendererProgress()
        column = gtk.TreeViewColumn('', cell)
        column.add_attribute(cell, 'value', 5)
        column.set_sort_column_id(5)
        self.wids['tv_datos'].insert_column(column, 5)
        # XXX
        self.wids['tv_datos'].add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.wids['tv_datos'].connect('button_press_event', 
                                      self.button_clicked) 
        # XXX
        self.colorear(self.wids['tv_datos'])
        temp = time.localtime()
        self.fin = str(temp[0])+'/'+str(temp[1])+'/'+str(temp[2])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.wids['e_fechainicio'].set_text(utils.str_fecha(
            mx.DateTime.localtime() - (7 * mx.DateTime.oneDay)))
        self.inicio = self.wids['e_fechainicio'].get_text().split('/')
        self.inicio.reverse()
        self.inicio = '/'.join(self.inicio)
        gtk.main()
    
    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        tv = self.wids['tv_datos']
        abrir_csv(treeview2csv(tv))

    def colorear(self, tv):
        """
        Asocia una función al treeview para resaltar los partes pendientes 
        de verificar.
        """
        def cell_func(column, cell, model, itr, numcol):
            """
            Si la fila corresponde a un parte de producción no verificado, 
            lo colorea en rojo oscuro, si no, lo hace en verde oscuro.
            """
            color = "black"
            idparte = model[itr][-1]
            if idparte > 0:
                parte = pclases.ParteDeProduccion.get(idparte)
                if parte.bloqueado:
                    color = "dark green"
                else:
                    color = "dark red"
            cell.set_property("foreground", color)

        cols = tv.get_columns()
        for i in xrange(len(cols) - 1): # Todas las columas menos la 
                                        # del porcentaje en barra.
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell, cell_func, i)

    def imprimir(self, boton):
        """
        Prepara los datos para enviar a geninformes.
        """
        from formularios import reports
        from informes import geninformes
        if self.wids['r_rollos'].get_active():
            linea = "de línea de geotextiles."
        elif self.wids['r_balas'].get_active():
            linea = "de línea de fibra."
        else:
            linea = "global."
        titulo = "Productividad %s" % (linea)
        if not self.inicio:
            str_fecha = "Hasta %s" % ('/'.join(self.fin.split('/')[::-1]))
        else:
            str_fecha = "Del %s al %s" % ('/'.join(self.inicio.split('/')[::-1]), '/'.join(self.fin.split('/')[::-1]))
        datos = []
        model = self.wids['tv_datos'].get_model()
        for row in model:
            datos.append((row[0], "", "", ""))
            for hijo in row.iterchildren():
                datos.append(("", "%s-%s" % (hijo[1], hijo[2]), hijo[3], hijo[4]))
            datos.append(("", "", "---", "---"))
            datos.append(("", "", row[3], row[4]))
            datos.append(("===", "===", "===", "==="))
        datos.append(("", )*4)
        datos.append(("TOTALES:", "", "", ""))
        datos.append(("", "Producido:", 
                      self.wids['e_kilosproducidos'].get_text(), ""))
        datos.append(("", "Consumido:", 
                      self.wids['e_kilosgranza'].get_text(), ""))
        datos.append(("", "Producción a la hora:", 
                      self.wids['e_kiloshora'].get_text(), ""))
        datos.append(("", "Productividad total:", 
                      self.wids['e_total'].get_text(), ""))
        datos.append(("", "Personas/turno:", 
                      self.wids['e_personasturno'].get_text(), ""))
        reports.abrir_pdf(
            geninformes.consulta_productividad(titulo, str_fecha, datos))

    def abrir_parte(self, treeview, path, view_column):
        # print "My name is Ivor. I'm an engine driver"
        idparte = treeview.get_model()[path][-1]
        if idparte > 0: # Podría usar también el chequeo de que padre != None.
            parte = pclases.ParteDeProduccion.get(idparte)
            if parte.es_de_balas():
                from formularios import partes_de_fabricacion_balas
                ventana_parteb = partes_de_fabricacion_balas.PartesDeFabricacionBalas(parte)  # @UnusedVariable
            elif parte.es_de_geotextiles():
                from formularios import partes_de_fabricacion_rollos
                ventana_parteb = partes_de_fabricacion_rollos.PartesDeFabricacionRollos(parte)  # @UnusedVariable
            elif parte.es_de_bolsas():
                from formularios import partes_de_fabricacion_bolsas
                ventana_parteb = partes_de_fabricacion_bolsas.PartesDeFabricacionBolsas(parte)  # @UnusedVariable

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, partes, solobalas):
        """
        Rellena el model con los tipos de material existentes
        """        
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        model = self.wids['tv_datos'].get_model()
        model.clear()
        total = 0
        kilosproducidos = 0
        kilosgranza = 0
        vector = []
        tot = len(partes)
        i = 0.0
        vpro.mostrar()
        e_personasturno = 0
        tiempototal = 0
        tiemporeal = 0      # Por si inicia una consulta sin resultados.
        metrosproducidos = 0
        kilosconsumidos = kilosconsumidos_partidas_completas = 0
        tiempototaltotal = mx.DateTime.DateTimeDelta(0)
        selffin = utils.parse_fecha('/'.join(self.fin.split('/')[::-1]))
        # ... WTF? Esto está hecho como el culo. ¡REFACTORIZAR!
        # XXX Primer intento de acelerar los treeview
        self.wids['tv_datos'].freeze_child_notify()
        self.wids['tv_datos'].set_model(None)
        # XXX 
        personashora = []
        dia_actual = ""     # Estos tres parámetros son para medir la 
                            # producción y productividad por día.
        produccion_actual = 0.0
        productividad_actual = 0.0
        nodos_hijos_por_dia = 0
        balas_consumidas = []       # Lista con las balas consumidas por 
            # todos los partes, así evito contar la misma dos veces si en dos 
            # partes se ha usado la misma partida o dos partidas de la misma 
            # partida de carga.
        padre = None # En una de las iteraciones se espera que padre se haya 
            # instanciado en el final de la anterior. Inicializo para evitar 
            # errores y errores en análisis sintáctico de algunos IDE en la 
            # línea 342.
        for p in partes:
            if p.se_solapa():
                self.logger.warning("%sconsulta_productividad::rellenar_tabla"
                    " -> El parte ID %d se solapa con otros de la misma línea"
                    ". Si estaba verificado, lo desbloqueo para que se vuelva"
                    " a revisar y lo ignoro para el cálculo actual." % (
                     self.usuario and self.usuario.usuario + ": " or "", p.id))
                p.bloqueado = False
                continue
            vpro.set_valor(i/tot, 'Añadiendo parte %s...' % (
                                    utils.str_fecha(p.fecha)))
            kilosgranza_del_parte = 0.0
            tiempototal, tiemporeal = self.calcular_tiempo_trabajado(p)
            tiempototaltotal += tiempototal
            try:
                # print tiemporeal, tiempototal
                productividad = (tiemporeal.seconds / tiempototal.seconds)*100
            except ZeroDivisionError:
                productividad = 100     # Bueno, el máximo es 1 (100%). Es lo 
                                    # más parecido a infinito positivo, ¿no?
            if productividad < 0:
                productividad = 0
                self.logger.warning("consulta_productividad::rellenar_tabla "
                    "-> Parte con productividad NEGATIVA: %s" % p)
            # Tratamiento especial para partes de balas
            if (self.wids['r_balas'].get_active() 
                or self.wids['r_ambos'].get_active()):   # Sólo balas o todos. 
                if p.es_de_fibra(): 
                    balas = [a.bala for a in p.articulos if a.balaID != None]
                    bigbags = [a.bigbag for a in p.articulos if a.bigbagID != None]
                    for b in balas:
                        kilosproducidos += b.pesobala
                    for b in bigbags:
                        kilosproducidos += b.pesobigbag
                    kilosgranza_del_parte = p.get_granza_consumida()
                    kilosgranza += kilosgranza_del_parte
                    if p.get_produccion()[0] - kilosgranza_del_parte > 1000: 
                                                                    # XXX DEBUG
                        self.logger.warning("El parte ID %d (%s) ha consumido (%s) mucha menos granza que fibra ha producido (%s) !!!" % (p.id, utils.str_fecha(p.fecha), utils.float2str(kilosgranza_del_parte), utils.float2str(p.get_produccion()[0])))     
                                                                    # XXX DEBUG
            if (self.wids['r_cemento'].get_active() 
                or self.wids['r_ambos'].get_active()):
                kilosproducidos += p.get_produccion()[0]
                kilosconsumidos += sum([bb.pesobigbag for bb in p.bigbags])
            if (self.wids['r_rollos'].get_active()
                or self.wids['r_ambos'].get_active()):  # Sólo rollos o todos.
                if p.es_de_geotextiles():
                    superficies_defectuosos = [a.superficie 
                        for a in p.articulos if a.es_rollo_defectuoso()]
                    metrosproducidos += sum(superficies_defectuosos)
                    rollos = [a.rollo for a in p.articulos if a.rollo != None]
                    if len(rollos) > 0:     # Para que no intente hacer el 
                        # cálculo con partes que tengan balas y/o no rollos.
                        metrosproducidos += len(rollos) * p.articulos[0].productoVenta.camposEspecificosRollo.ancho * p.articulos[0].productoVenta.camposEspecificosRollo.metrosLineales
                        if p.articulos[0].es_rollo():
                            partida = p.articulos[0].rollo.partida
                        elif p.articulos[0].es_rollo_defectuoso():
                            partida = p.articulos[0].rolloDefectuoso.partida
                        else:
                            partida = None
                        if partida != None:
                            contar_kilosconsumidos_partidas_completas = partida.entra_en_cota_superior(selffin)
                            for b in partida.balas:
                                if b not in balas_consumidas:   # Evito contar la misma bala dos veces.
                                    bpesobala = b.pesobala
                                    kilosconsumidos += bpesobala
                                    if contar_kilosconsumidos_partidas_completas:
                                        kilosconsumidos_partidas_completas += bpesobala
                                    balas_consumidas.append(b)
            
            empleados = len(p.horasTrabajadas)
            e_personasturno += empleados
            tiempoparte = p.get_duracion().hours
            if tiempoparte > 0:
                personashora.append(empleados/tiempoparte)
            else:
                personashora.append(0.0)
            
            vector.append(productividad)
            produccion = p.get_produccion()

            # Resúmenes por día como nodos padre del TreeView.
            if dia_actual != utils.str_fecha(p.fecha):
                if dia_actual != "":  # Actualizo el padre
                    if not self.wids['r_ambos'].get_active():
                        model[padre][3] = "%s %s" % (utils.float2str(produccion_actual), produccion[1])
                    else:   # Evito mezclar kilos con metros
                        model[padre][3] = "-"
                    try:
                        productividad_actual /= nodos_hijos_por_dia
                    except ZeroDivisionError:
                        productividad_actual = 100.0    # A falta de infinito.
                    model[padre][4] = "%s %%" % (utils.float2str(productividad_actual))
                    model[padre][5] = productividad_actual
                dia_actual = utils.str_fecha(p.fecha)
                produccion_actual = 0.0
                productividad_actual = 0.0
                nodos_hijos_por_dia = 0
                padre = model.append(None, 
                            (utils.str_fecha(p.fecha), 
                             "", 
                             "", 
                             "", 
                             "%s %%" % (utils.float2str(productividad_actual)), 
                             productividad_actual,
                             0))
            model.append(padre, 
                (utils.str_fecha(p.fecha),
                 str(p.horainicio)[:5],
                 str(p.horafin)[:5],
                 "%s %s" % (utils.float2str(produccion[0]), produccion[1]),
                 "%s %%" % (utils.float2str(productividad)),
                 productividad,
                 p.id))
            produccion_actual += produccion[0]
            # BUG: Es media ponderada, no media aritmética:            productividad_actual += productividad
            # BUG: Es media ponderada, no media aritmética:            nodos_hijos_por_dia += 1
            productividad_actual += productividad * p.get_duracion().hours
            nodos_hijos_por_dia += p.get_duracion().hours
            i+=1
        # Actualizo el padre de los últimos nodos:
        if dia_actual != "":  # Actualizo el padre
            if not self.wids['r_ambos'].get_active():
                model[padre][3] = "%s %s" % (utils.float2str(produccion_actual), produccion[1])
            else:   # Evito mezclar kilos con metros
                model[padre][3] = "-"
            try:
                productividad_actual /= nodos_hijos_por_dia
            except ZeroDivisionError:
                productividad_actual = 100.0    # A falta de infinito...
            model[padre][4] = "%s %%" % (utils.float2str(productividad_actual))
            model[padre][5] = productividad_actual

        vpro.ocultar()
        # XXX Primer intento de acelerar los treeview
        self.wids['tv_datos'].set_model(model)
        self.wids['tv_datos'].thaw_child_notify()
        # XXX
        if partes != []:
            # total = total / len(partes)    
            total = sum([r[-2] for r in self.wids['tv_datos'].get_model() if r.parent == None]) / len([r for r in self.wids['tv_datos'].get_model() if r.parent == None])
            # Campos especiales de "Sólo balas"
            if self.wids['r_balas'].get_active():
                self.wids['label7'].set_text('Kilos producidos:')
                self.wids['label8'].set_text('Kilos granza consumidos:')
                self.wids['label9'].set_text('Kilos / Hora producción:')
                self.wids['e_kilosproducidos'].set_text(
                    "%s kg" % (utils.float2str(kilosproducidos)))
                self.wids['e_kilosgranza'].set_text(
                    "%s kg" % (utils.float2str(kilosgranza)))
                try:
                    e_kiloshora = (kilosproducidos/float(tiempototaltotal.hours))
                except ZeroDivisionError:
                    self.logger.warning("consulta_productividad.py::rellenar_tabla -> tiempototaltotal = 0")
                    e_kiloshora = 0   # Cero por poner algo. Porque un parte de tiempo transcurrido=0... se las trae.
                self.wids['e_kiloshora'].set_text("%s kg/h" % (utils.float2str(e_kiloshora)))
            elif self.wids['r_rollos'].get_active():
                tips = gtk.Tooltips()
                tips.set_tip(self.wids['e_kilosgranza'], """Kilogramos consumidos contando partidas completas por defecto y por exceso. 
(En un caso se cuentan solo partidas de carga cuyas partidas de geotextiles se hayan completado estrictamente antes o en la cota superior. 
En el otro, por exceso, se contabilizan partidas completas aunque parte de su producción se salga del rango de fechas.
En ambos casos el límite inferior es flexible -por compensación-.)""")
                tips.enable()
                self.wids['label7'].set_text('m² producidos:')
                self.wids['label8'].set_text('Kg fibra consumidos:') 
                self.wids['label9'].set_text('m²/h producción:')
                try:
                    e_kiloshora = (metrosproducidos/float(tiempototaltotal.hours))
                except ZeroDivisionError:
                    self.logger.warning("consulta_productividad.py::rellenar_tabla -> tiempototaltotal = 0")
                    e_kiloshora = 0
                self.wids['e_kilosproducidos'].set_text("%s m²" % (utils.float2str(metrosproducidos)))
                self.wids['e_kilosgranza'].set_text("%s kg ~ %s kg" % (utils.float2str(kilosconsumidos_partidas_completas), utils.float2str(kilosconsumidos)))
                self.wids['e_kiloshora'].set_text("%s m²/h" % (utils.float2str(e_kiloshora)))
            else:
                self.wids['label7'].set_text('Producido:')
                self.wids['label8'].set_text('Consumido:')
                self.wids['label9'].set_text('Producción combinada a la hora:')
                try:
                    e_kiloshora = (kilosproducidos/float(tiempototaltotal.hours))
                    metros_hora = (metrosproducidos/float(tiempototaltotal.hours))
                except ZeroDivisionError:
                    self.logger.warning("consulta_productividad.py::rellenar_tabla -> tiempototaltotal = 0")
                    e_kiloshora = 0 
                    metros_hora = 0
                self.wids['e_kilosproducidos'].set_text("%s m²; %s kg" % (utils.float2str(metrosproducidos), utils.float2str(kilosproducidos)))
                self.wids['e_kilosgranza'].set_text("%s kg fibra; %s kg granza" % (utils.float2str(kilosconsumidos), utils.float2str(kilosgranza)))
                self.wids['e_kiloshora'].set_text("%s m²/h; %s kg/h" % (utils.float2str(metros_hora), utils.float2str(e_kiloshora)))
            # Fin campos especiales de "Sólo balas"
            self.wids['curva'].set_range(0, len(vector), 0, 100)
            self.wids['curva'].set_vector(vector)
            self.wids['curva'].set_curve_type(gtk.CURVE_TYPE_SPLINE)
            # self.wids['curva'].set_curve_type(gtk.CURVE_TYPE_LINEAR)
            self.wids['pb'].set_fraction(total / 100.0)
        else:
            self.wids['curva'].set_range(0, 2, 0, 100)
            self.wids['curva'].set_vector((0, 0))
            self.wids['pb'].set_fraction(1 / 100.0)
            self.wids['e_kilosproducidos'].set_text('')
            self.wids['e_kilosgranza'].set_text('')
            self.wids['e_kiloshora'].set_text('')
        self.wids['e_total'].set_text("%s %%" % (utils.float2str(total)))
        try:
            personashora = sum(personashora)/len(personashora)
        except ZeroDivisionError:
            personashora = 0
        try:
            e_personasturno = float(e_personasturno) / len(partes)
        except ZeroDivisionError:
            e_personasturno = 0
        self.wids['e_personasturno'].set_text("%s (%s personas/h)" % (utils.float2str(e_personasturno), utils.float2str(personashora)))
        
    def set_inicio(self, boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
        self.inicio = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])


    def set_fin(self, boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.fin = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])


    def calcular_duracion(self, hfin, hini, parte = None):
        if isinstance(hfin, mx.DateTime.DateTimeDeltaType):
            hfin = hfin + mx.DateTime.oneDay 
        duracion = hfin - hini
        if duracion.day > 0:
            duracion -= mx.DateTime.oneDay
        if duracion.day > 0:
            self.logger.warning("WARNING: consulta_productividad: calcular_duracion: ID %d: ¿Seguro que dura más de un día completo?" % (parte and parte.id or 0))
        return duracion
 
    def calcular_tiempo_trabajado(self, parte):
        tiempototal = parte.get_duracion()
        try:
            tiemporeal = parte.get_horas_trabajadas()
        except AssertionError, msg:
            txt = "consulta_productividad.py::calcular_tiempo_trabajado -> Parte ID %d tiene más horas de parada que lo que dura el parte total. (%s)" % (parte.id, msg)
            self.logger.error(txt)
            print txt
            tiemporeal = mx.DateTime.DateTimeDelta(0)
        return tiempototal, tiemporeal

        
    def buscar(self, boton):
        """
        Dadas fecha de inicio y de fin, y un tipo de parte, lista
        todos los partes de dicho periodo indicando la productividad
        de dicho parte
        """
        solobalas = False
        if not self.inicio:
            partes = pclases.ParteDeProduccion.select(
                        orderBy = ('fecha', 'horainicio'))
        else:
            partes = pclases.ParteDeProduccion.select(pclases.AND(
                    pclases.ParteDeProduccion.q.fecha >= self.inicio,
                    pclases.ParteDeProduccion.q.fecha <= self.fin), 
                orderBy = ('fecha', 'horainicio'))
        if self.wids['r_balas'].get_active():
            partes = [p for p in partes if p.es_de_balas()]
            solobalas = True
        elif self.wids['r_rollos'].get_active():
            #partes = [p for p in partes if not p.es_de_balas()]
            partes = [p for p in partes if p.es_de_geotextiles()]
        elif self.wids['r_cemento'].get_active():
            partes = [p for p in partes if p.es_de_bolsas()]
        else:
            partes = list(partes)
        self.rellenar_tabla(partes, solobalas)

    def button_clicked(self, lista, event):
        if event.button == 3:
            # menu = gtk.Menu()
            ui_string = """<ui>
                            <popup name='Popup'>
                                <menuitem action='Enviar muestra'/>
                            </popup>
                           </ui>"""
            ag = gtk.ActionGroup('WindowActions')
            actions = [('Enviar muestra', gtk.STOCK_COLOR_PICKER, '_Enviar muestra', '<control>E',
                        'Envia una muestra del lote o partida correspondiente al parte a laboratorio', 
                        self.enviar_a_laboratorio), ]
            ag.add_actions(actions)
            ui = gtk.UIManager()    #gtk.UI_MANAGER_POPUP
            ui.insert_action_group(ag, 0)
            ui.add_ui_from_string(ui_string)
            widget = ui.get_widget("/Popup")
            widget.popup(None, None, None, event.button, event.time)
    
    def enviar_a_laboratorio(self, parametro):
        # NOTA: Ni idea de qué es lo que traerá el parámetro, sólo me interesa
        # el parte que está seleccionado en el treeview.
        model, itr = self.wids['tv_datos'].get_selection().get_selected()
        if itr == None:
            utils.dialogo_info(titulo = "PARTE NO SELECCIONADO", 
                               texto = "Seleccione un parte para enviar una muestra de su\nlote o partida al laboratorio.", 
                               padre = self.wids['ventana'])
        else:
            idparte = model[itr][-1]
            if idparte > 0:
                parte = pclases.ParteDeProduccion.get(idparte)
                if not parte.articulos:
                    utils.dialogo_info(titulo = "PARTE VACÍO", texto = "En el parte seleccionado no hubo producción.", padre = self.wids['ventana'])
                else:
                    a = parte.articulos[0]  # Al menos tiene 1 artículo. Con el primero me vale.
                    if parte.es_de_balas():
                        try:
                            lote = a.bala.lote
                            loteCem = None
                        except AttributeError:
                            lote = None
                            loteCem = a.bigbag.loteCem
                        partida = None
                    else:
                        lote = None
                        partida = a.rollo.partida
                    self.crear_muestra(lote, partida, loteCem)
      
    def crear_muestra(self, lote, partida, loteCem):
        dialogo = gtk.Dialog("DATOS DE LA MUESTRA",
                             self.wids['ventana'],
                             gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                             (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT,
                              gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
        dialogo.connect("response", self.crear_muestra_ok_cancel, lote, partida, loteCem)
        texto = """
        Introduzca, si lo desea, los datos para la muestra          
        de%s número %d.
        """ % (partida and " la partida" or "l lote", 
               partida and partida.numpartida or lote.numlote)
        txt = gtk.Label(texto)
        dialogo.vbox.pack_start(txt)
        dialogo.vbox.pack_start(gtk.Label("\nCódigo de muestra:"))
        codigo = gtk.Entry()
        dialogo.vbox.pack_start(codigo)
        dialogo.vbox.pack_start(gtk.Label("\nObservaciones:"))
        observaciones = gtk.Entry()
        dialogo.vbox.pack_start(observaciones)
        dialogo.vbox.show_all()
        dialogo.run()
        dialogo.destroy()
    
    def crear_muestra_ok_cancel(self, dialogo, respuesta, lote, partida, loteCem):
        if respuesta == gtk.RESPONSE_ACCEPT:
            codigo = dialogo.vbox.get_children()[2].get_text()
            observaciones = dialogo.vbox.get_children()[4].get_text()
            m = pclases.Muestra(lote = lote,
                                loteCem = loteCem, 
                                partida = partida,
                                codigo = codigo,
                                observaciones = observaciones,
                                pendiente = True,
                                envio = mx.DateTime.localtime(),
                                recepcion = None)
            pclases.Auditoria.nuevo(m, self.usuario, __file__)
            if utils.dialogo(titulo = "MUESTRA ENVIADA",
                             texto = "Muestra creada, enviada y pendiente para su análisis en laboratorio.\n¿Desea enviar una alerta?", 
                             padre = self.wids['ventana']):
                usuarios = [(u.id, u.usuario) for u in pclases.Usuario.select(orderBy = 'usuario')]
                usuario = utils.dialogo_combo(titulo = "SELECCIONE USUARIO",
                                              texto = "Seleccione del desplegable inferior al usuario que quiere alertar acerda de la muestra.",
                                              ops = usuarios,
                                              padre = self.wids['ventana'])
                if usuario != None:
                    user = pclases.Usuario.get(usuario)
                    if m.codigo:
                        msj = "La muestra %s está " % m.codigo
                    else:
                        msj = "Tiene una muestra "
                    msj += "pendiente de analizar." 
                    user.enviar_mensaje(msj)

if __name__ == '__main__':
    t = ConsultaProductividad()
 
