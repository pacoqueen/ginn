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
## resultados_fibra.py - Resultados de pruebas de fibra. 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 18 de mayo de 2006 -> Inicio
## 19 de mayo de 2006 -> Testing
##
###################################################################
## FIXME:
## - Al salir con el evento destroy (bolaspa) pregunta dos veces si 
##   quiere salir y la segunda vez ignora la respuesta.
## 
###################################################################
## NOTAS: Se reusa la misma ventana (glade) de resultados de fibra,
## todo lo relacionado con rizo es humedad en la fibra de cemento.
###################################################################

from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk, time
from framework import pclases
from utils import _float as float
from resultados_fibra import comprobar_y_preguntar_si_guardar
import mx

class ResultadosFibra(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'resultados_fibra.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self._salir,
                       'b_lote/clicked': self.set_loteCem,
                       'b_fecha/clicked': self.fecha,
                       'b_add/clicked': self.add,
                       'b_drop/clicked': self.drop,
                       'sp_tolerancia/value-changed': self.cambiar_tolerancia, 
                       'b_guardar_obs/clicked': self.guardar_obs, 
                       'b_imprimir/clicked': self.imprimir, 
                       'ventana/delete_event': self._salir
                      }
        self.add_connections(connections)
        self.activar_widgets(False)
        self.inicializar_ventana()
        if objeto == None:
            self.loteCem = None
        else:
            self.loteCem = objeto
            self.actualizar_ventana()
        gtk.main()

    def _salir(self, *args, **kw):
        """
        Si hay cambios pendientes en observaciones, pregunta.
        Después llama a la función salir heredada.
        """
        comprobar_y_preguntar_si_guardar(self)
        self.salir(*args, **kw)

    # --------------- Funciones auxiliares ------------------------------
    def activar_widgets(self, valor):
        self.ws = ('e_codigo', 
                   'e_nombre',
                   'e_dtex',
                   'e_corte',
                   'e_color',
                   'e_tenacidad',
                   'e_elongacion',
                   'e_rizo', 
                   'e_grasa', 
                   'e_encogimiento',
                   'tv_pruebas',
                   'b_add',
                   'b_drop',
                   'b_fecha',
                   'e_media',
                   'e_desvtipica',
                   'sp_tolerancia',
                   'txt_observaciones', 
                   'frame4')
        for i in self.ws:
            self.wids[i].set_sensitive(valor)
        if self.usuario:
            try:
                ventana = pclases.Ventana.select(pclases.Ventana.q.fichero == "resultados_cemento.py")[0]     # OJO: HARCODED
            except IndexError:
                txt = "resultados_fibra::activar_widgets -> Ventana no encontrada en BD."
                self.logger.error(txt)
                print txt
            else:
                permiso = self.usuario.get_permiso(ventana)
                if not permiso.escritura and self.usuario.nivel > 2:
                    self.wids['tv_pruebas'].set_sensitive(False)
                    self.wids['txt_observaciones'].set_sensitive(False)
                if not permiso.nuevo and self.usuario.nivel > 2:
                    self.wids['b_add'].set_sensitive(False)
     
    def crear_listview(self, tv):
        cols = (('Fecha', 'gobject.TYPE_STRING', True, True, True, self.cambiar_fecha),
                ('Título (DTEX)', 'gobject.TYPE_STRING', True, True, False, self.cambiar_titulo), 
                ('Alargamiento (%)', 'gobject.TYPE_STRING', True, True, False, self.cambiar_alargamiento), 
                ('Tenacidad (cN/tex)', 'gobject.TYPE_STRING', True, True, False, self.cambiar_tenacidad), 
                ('Grasa (%)', 'gobject.TYPE_STRING', True, True, False, self.cambiar_grasa), 
                ('Encogimiento (%)', 'gobject.TYPE_STRING', True, True, False, self.cambiar_encogimiento), 
                ('Humedad (%)', 'gobject.TYPE_STRING', True, True, False, self.cambiar_humedad), 
                ('ID', 'gobject.TYPE_STRING', False, False, False, None)) # Contiene los ID de los resultados separados por ','
        utils.preparar_listview(tv, cols)
        tv.get_column(1).get_cell_renderers()[0].set_property('xalign', 0.1) 
        tv.get_column(2).get_cell_renderers()[0].set_property('xalign', 0.1) 
        tv.get_column(3).get_cell_renderers()[0].set_property('xalign', 0.1) 
        tv.get_column(4).get_cell_renderers()[0].set_property('xalign', 0.1) 
        tv.get_column(5).get_cell_renderers()[0].set_property('xalign', 0.1) 
        tv.get_column(6).get_cell_renderers()[0].set_property('xalign', 0.1) 

    def inicializar_ventana(self):
        """
        Inicializa los widgets de la ventana.
        """
        self.crear_listview(self.wids['tv_pruebas'])
        self.wids['b_fecha'].set_property("visible", False)
        self.wids['l_rizo'].set_label("Humedad: ")
        self.wids['txt_observaciones'].get_buffer().connect("changed", lambda txtbuffer: self.wids['b_guardar_obs'].set_sensitive(True))

    def func_sort(self, t1, t2):
        if t1[0] < t2[0]:
            return -1
        elif t1[0] > t2[0]:
            return 1
        else:
            return 0

    def preparar_pruebas(self):
        """
        Devuelve una lista de listas que contiene las pruebas ordenadas del 
        loteCem por fecha de la forma: [(fecha, prueba título, ..., "id0,id1,...id5")]
        """
        res = []
        for p in self.loteCem.pruebasTitulo:
            res.append([p.fecha, p.resultado, None, None, None, None, None, [p.id, 0, 0, 0, 0, 0]])
        for p in self.loteCem.pruebasElongacion:
            puesto = False
            for fila in res:
                if p.fecha == fila[0] and fila[2] == None:  # Hay hueco en la fecha
                    fila[2] = p.resultado
                    fila[-1][1] = p.id
                    puesto = True
                    break
            if not puesto:
                res.append([p.fecha, None, p.resultado, None, None, None, None, [0, p.id, 0, 0, 0, 0]])
        for p in self.loteCem.pruebasTenacidad:
            puesto = False
            for fila in res:
                if p.fecha == fila[0] and fila[3] == None:  # Hay hueco en la fecha
                    fila[3] = p.resultado
                    fila[-1][2] = p.id
                    puesto = True
                    break
            if not puesto:
                res.append([p.fecha, None, None, p.resultado, None, None, None, [0, 0, p.id, 0, 0, 0]])
        for p in self.loteCem.pruebasGrasa:
            puesto = False
            for fila in res:
                if p.fecha == fila[0] and fila[4] == None:  # Hay hueco en la fecha
                    fila[4] = p.resultado
                    fila[-1][3] = p.id
                    puesto = True
                    break
            if not puesto:
                res.append([p.fecha, None, None, None, p.resultado, None, None, [0, 0, 0, p.id, 0, 0]])
        for p in self.loteCem.pruebasEncogimiento:
            puesto = False
            for fila in res:
                if p.fecha == fila[0] and fila[5] == None:  # Hay hueco en la fecha
                    fila[5] = p.resultado
                    fila[-1][4] = p.id
                    puesto = True
                    break
            if not puesto:
                res.append([p.fecha, None, None, None, None, p.resultado, None, [0, 0, 0, 0, p.id, 0]])
        for p in self.loteCem.pruebasHumedad:
            puesto = False
            for fila in res:
                if p.fecha == fila[0] and fila[6] == None:  # Hay hueco en la fecha
                    fila[6] = p.resultado
                    fila[-1][5] = p.id
                    puesto = True
                    break
            if not puesto:
                res.append([p.fecha, None, None, None, None, None, p.resultado, [0, 0, 0, 0, 0, p.id]])
        res.sort(self.func_sort)
        res = [(utils.str_fecha(f[0]), \
                f[1] and "%.2f" % f[1] or "", \
                f[2] and "%.2f" % f[2] or "", \
                f[3] and "%.2f" % f[3] or "", \
                f[4] and "%.2f" % f[4] or "", \
                f[5] and "%.2f" % f[5] or "", \
                f[6] and "%.2f" % f[6] or "", \
                ','.join(map(str, f[7]))) for f in res]
        return res

    def rellenar_pruebas(self):
        """
        Introduce en el treeview las pruebas del loteCem seleccionado y 
        recalcula la característica del loteCem.
        """
        model = self.wids['tv_pruebas'].get_model()
        model.clear()
        self.calcular_caracteristicas()
        pruebas = self.preparar_pruebas()
        for prueba in pruebas:
            model.append(prueba)
            
    def calcular_caracteristicas(self):
        """
        Calcula la media, desviación típica y marca los valores según tolerancia. 
        """
        loteCem = self.loteCem
        # La tolerancia depende del tipo de producto:
        try:
            dtex = loteCem.bigbags[0].articulos[0].productoVenta.camposEspecificosBala.dtex
        except:
            utils.dialogo_info(titulo = 'ERROR', 
                               texto = 'Ocurrió un error buscando el tipo de fibra.', 
                               padre = self.wids['ventana'])
            return
        mediatitulo = 0
        sumatorio = 0
        desvtipica = 0
        for p in loteCem.pruebasTitulo:
            mediatitulo += p.resultado
            sumatorio += p.resultado**2.0
        try:
            mediatitulo /= len(loteCem.pruebasTitulo)
            desvtipica = sumatorio / len(loteCem.pruebasTitulo)
            desvtipica -= mediatitulo**2.0
            desvtipica = desvtipica**0.5    # ValueError cuando intente hacer raíz de número negativo. No debería ocurrir.
        except ZeroDivisionError:
            mediatitulo = 0
            desvtipica = 0
        loteCem.mediatitulo = mediatitulo
        self.wids['e_desvtipica'].set_text("%.2f" % desvtipica)
        self.marcar_tolerancia(dtex, mediatitulo, loteCem.tolerancia)
        self.calcular_caracteristicas_propias()
        self.rellenar_info_loteCem()

    def calcular_elongacion(self):
        """
        Calcula la media de los valores de y elongación.
        """
        loteCem = self.loteCem
        loteCem.update_valor("elongacion")

    def calcular_tenacidad(self):
        loteCem = self.loteCem
        loteCem.update_valor("tenacidad")

    def calcular_grasa(self):
        loteCem = self.loteCem
        # La elongación depende del tipo de producto:
        loteCem.update_valor("grasa")
 
    def calcular_encogimiento(self):
        loteCem = self.loteCem
        loteCem.update_valor("encogimiento")
    
    def calcular_humedad(self):
        loteCem = self.loteCem
        loteCem.update_valor("humedad")

    def calcular_caracteristicas_propias(self):
        self.calcular_elongacion()
        self.calcular_tenacidad()
        self.calcular_grasa()
        self.calcular_encogimiento()
        self.calcular_humedad()
        self.rellenar_info_loteCem()

    def marcar_tolerancia(self, dtex, mediatitulo, tolerancia):
        self.wids['ruler'].set_sensitive(False)
        diferencia = abs(mediatitulo - dtex)
        try:
            porcentaje = (diferencia * 100) / dtex   # En formato 0 a 100 porque las posiciones del ruler son de -100 a 100
        except ZeroDivisionError:   # El DTEX del artículo es 0.
            porcentaje = 0.0
        if mediatitulo < dtex:
            porcentaje *= -1
        self.wids['ruler'].set_property('position', porcentaje)
        difmax = dtex * tolerancia
        if round(diferencia,2) > difmax:
            self.wids['e_media'].modify_base(gtk.STATE_NORMAL, self.wids['e_media'].get_colormap().alloc_color("red"))
        else:
            self.wids['e_media'].modify_base(gtk.STATE_NORMAL, self.wids['e_media'].get_colormap().alloc_color("green"))
        self.colorear(self.wids['tv_pruebas'], dtex, difmax)

    def colorear(self, tv, dtex, diferencia):
        """
        diferencia es la diferencia máxima en valor absoluto que debe 
        haber entre el resultado y el título del artículo.
        """
        def cell_func(col, cell, model, itr, (dtex, dif)):
            resultado = model[itr][1].replace(" ", "")
            if resultado != "":
                resultado = float(resultado)
                if round(abs(resultado-dtex),2) > dif:
                    color = "red"
                else:
                    color = "green"
                cell.set_property("text", "%.2f" % resultado)
            else:
                color = "white"
                cell.set_property("text", "")
            cell.set_property("cell-background", color)
        cols = tv.get_columns()
        col = cols[1]
        cells = col.get_cell_renderers()
        for cell in cells:
            col.set_cell_data_func(cell, cell_func, (dtex, diferencia))

    def actualizar_ventana(self):
        """
        Método que sobreescribe el "actualizar_ventana" que hereda de la clase ventana.
        PRECONDICION: self.loteCem no puede ser None
        """
        try:
            self.loteCem.sync()
            self.rellenar_widgets()
        except pclases.SQLObjectNotFound:
                utils.dialogo_info(titulo = 'REGISTRO ELIMINADO', 
                                   texto = 'El registro ha sido borrado desde otro puesto.', 
                                   padre = self.wids['ventana'])
                self.loteCem = None
        self.activar_widgets(self.loteCem!=None)


    # --------------- Manejadores de eventos ----------------------------
    def guardar_obs(self, boton):
        """
        Guarda el contenido del TextView en el atributo observaciones.
        """
        if self.objeto != None:
            buff = self.wids['txt_observaciones'].get_buffer()
            self.objeto.observaciones = buff.get_text(buff.get_start_iter(), buff.get_end_iter())
            self.wids['b_guardar_obs'].set_sensitive(False)

    def add(self, w):
        if self.loteCem != None:
            model = self.wids['tv_pruebas'].get_model()
            model.append((utils.str_fecha(time.localtime()),
                          "", "", "", "", "", "", "0,0,0,0,0,0"))
        else:
            print "WARNING: Se ha intentano añadir una prueba con loteCem = None"
    
    def drop(self, w):
        """
        Borra una línea completa de resultados.
        """
        model, itr = self.wids['tv_pruebas'].get_selection().get_selected()
        if itr != None and utils.dialogo(titulo = 'BORRAR PRUEBA', texto = '¿Está seguro?', padre = self.wids['ventana']):
            ids = map(int, model[itr][-1].split(','))
            for columnaid in range(len(ids)):
                ide = ids[columnaid]
                if ide != 0:
                    clase = self.get_clase(columnaid+1)
                    prueba = clase.get(ide)
                    prueba.destroy(ventana = __file__)
            self.rellenar_pruebas()

    def set_loteCem(self, w):
        comprobar_y_preguntar_si_guardar(self)
        codlote = utils.dialogo_entrada(titulo = 'Nº LOTE', 
                    texto = 'Introduzca número o código de lote de fibra '
                            'de cemento:',
                    padre = self.wids['ventana'])
        if codlote != None:
            numlote = utils.parse_numero(codlote)
            loteCems = pclases.LoteCem.select(pclases.OR(
                pclases.LoteCem.q.numlote == numlote, 
                pclases.LoteCem.q.codigo.contains(codlote)))
            if loteCems.count() == 0:
                utils.dialogo_info(titulo = 'LOTE NO ENCONTRADO', 
                    texto = 'No se encontró ningún lote de fibra de cemento'
                            ' %s.' % (codlote), 
                    padre = self.wids['ventana'])
                return
            elif loteCems.count() > 1:
                filas = [(l.id, l.numlote, l.codigo, l.tenacidad, 
                          l.elongacion, l.humedad, l.encogimiento) 
                         for l in loteCems]
                idloteCem = utils.dialogo_resultado(filas, 
                    titulo = 'SELECCIONE LOTE',
                    cabeceras = ('ID', 'Número', 'Código', 'Tenacidad', 
                                 'Elongación', 'Humedad', 'Encogimiento'), 
                    padre = self.wids['ventana'])
                if idloteCem < 0:
                    return
                loteCem = pclases.LoteCem.get(idloteCem)
            else:
                loteCem = loteCems[0]
            if len(loteCem.bigbags) == 0:
                utils.dialogo_info(titulo = 'LOTE VACÍO', 
                    texto = 'El lote de cemento no contiene bigbags, no '
                            'puede\nrealizar pruebas sobre un lote vacío.', 
                    padre = self.wids['ventana'])
                self.loteCem = None
                return
            self.loteCem = loteCem
            self.actualizar_ventana()
    
    def rellenar_widgets(self):
        self.objeto = self.loteCem
        self.activar_widgets(self.loteCem != None)
        if self.loteCem != None:
            self.rellenar_info_loteCem()
            self.rellenar_pruebas()
            self.rellenar_observaciones()
    
    def rellenar_observaciones(self):
        """
        Introduce las observaciones de la partida en el TextView.
        """
        self.wids['txt_observaciones'].get_buffer().set_text(self.objeto.observaciones)
        self.wids['b_guardar_obs'].set_sensitive(False)

    def rellenar_info_loteCem(self):
        """
        PRECONDICIÓN: self.loteCem != None y len(self.loteCem.bigbags) > 0
        """
        loteCem = self.loteCem
        self.wids['e_codigo'].set_text("%d (%s)" % (loteCem.numlote, loteCem.codigo))
        self.wids['e_nombre'].set_text(loteCem.bigbags[0].articulos[0].productoVenta.nombre)
        self.wids['e_dtex'].set_text("%.1f DTEX" % (loteCem.bigbags[0].articulos[0].productoVenta.camposEspecificosBala.dtex))
        self.wids['e_corte'].set_text(`loteCem.bigbags[0].articulos[0].productoVenta.camposEspecificosBala.corte`)
        self.wids['e_color'].set_text(loteCem.bigbags[0].articulos[0].productoVenta.camposEspecificosBala.color or '')
        self.wids['e_tenacidad'].set_text(loteCem.tenacidad == None and "-" or utils.float2str(loteCem.tenacidad))
        self.wids['e_elongacion'].set_text(loteCem.elongacion == None and "-" or utils.float2str(loteCem.elongacion))
        self.wids['e_rizo'].set_text(loteCem.humedad == None and "-" or utils.float2str(loteCem.humedad))
        self.wids['e_encogimiento'].set_text(loteCem.encogimiento == None and "-" or utils.float2str(loteCem.encogimiento))
        self.wids['e_grasa'].set_text(loteCem.grasa == None and "-" or utils.float2str(loteCem.grasa))
        self.wids['e_media'].set_text(loteCem.mediatitulo == None and "-" or "%.2f DTEX" % (loteCem.mediatitulo))
        try:
            self.wids['sp_tolerancia'].set_value(loteCem.tolerancia*100.0)
        except:
            self.wids['sp_tolerancia'].set_value(20)
            loteCem.tolerancia = 0.2

    def fecha(self, w):
        self.wids['e_fecha'].set_text(utils.str_fecha(utils.mostrar_calendario(fecha_defecto = self.objeto and self.objeto.fecha or None, padre = self.wids['ventana'])))

    def cambiar_fecha(self, cell, path, texto):
        try:
            fecha = time.strptime(texto, '%d/%m/%Y')
            fecha = mx.DateTime.DateFrom(fecha.tm_year, 
                                         fecha.tm_mon, 
                                         fecha.tm_mday)
        except:
            utils.dialogo_info('FECHA INCORRECTA', 
                               'La fecha introducida (%s) no es correcta.' % (texto), 
                               padre = self.wids['ventana'])
            return
        model = self.wids['tv_pruebas'].get_model()
        model[path][0] = utils.str_fecha(fecha)
        ids = map(int, model[path][-1].split(','))
        for col in xrange(6):
            if ids[col] != 0:
                clase = self.get_clase(col+1)
                prueba = clase.get(ids[col])
                prueba.fecha = fecha

    def get_clase(self, columna):
        if columna == 1:
            clase = pclases.PruebaTitulo
        elif columna == 2:
            clase = pclases.PruebaElongacion
        elif columna == 3:
            clase = pclases.PruebaTenacidad
        elif columna == 4:
            clase = pclases.PruebaGrasa
        elif columna == 5:
            clase = pclases.PruebaEncogimiento
        elif columna == 6:
            clase = pclases.PruebaHumedad
        else:
            print "WARNING: resultados_fibra.py: No debería entrar aquí."
            clase = None
        return clase

    def cambiar_resultado(self, tv, path, texto, columna):
        texto = texto.replace(" ", "")
        if texto != "":
            try:
                resultado = utils._float(texto)
            except:
                utils.dialogo_info('RESULTADO INCORRECTO',
                                   'El número tecleado (%s) no es correcto.' % (texto), 
                                   padre = self.wids['ventana'])
                return
        clase = self.get_clase(columna)
        columnaid = columna-1    # Porque en los IDS empieza por 0
        if clase != None:
            model = self.wids['tv_pruebas'].get_model()
            ids = map(int, model[path][-1].split(','))
            ide = ids[columnaid]
            if ide == 0:
                if texto != "":
                    fecha = time.strptime(model[path][0], '%d/%m/%Y')
                    fecha = mx.DateTime.DateFrom(fecha.tm_year, 
                                                 fecha.tm_mon, 
                                                 fecha.tm_mday)
                    try: 
                        prueba = clase(fecha = fecha, 
                                       resultado = resultado,
                                       loteCem = self.loteCem, 
                                       lote = None)
                    except TypeError:   # Es prueba de Humedad, no lleva relación con lote de fibra:
                        prueba = clase(fecha = fecha, 
                                       resultado = resultado,
                                       loteCem = self.loteCem)
                    ids[columnaid] = prueba.id
                    model[path][-1] = ','.join(map(str, ids))
                    model[path][columna] = "%.2f" % resultado
            else:
                prueba = clase.get(int(ide))
                if texto == "": 
                    try:
                        prueba.destroy(ventana = __file__)
                    except:
                        utils.dialogo_info(titulo = "ERROR", 
                                           texto = "El resultado no se pudo eliminar.", 
                                           padre = self.wids['ventana'])
                        return
                    model[path][columna] = ""
                    ids[columnaid] = 0 
                    model[path][-1] = ','.join(map(str, ids))
                    self.rellenar_pruebas() # Prefiero esto a comprobar si la fila se ha quedado vacía, etc...
                else:
                    prueba.resultado = resultado
                    if columna != 6:
                        model[path][columna] = "%.2f" % resultado
                    else:
                        model[path][columna] = "%d" % resultado
            self.calcular_caracteristicas()
            # print model[path][-1]
            # self.rellenar_pruebas()

    def cambiar_titulo(self, tv ,path, texto):
        self.cambiar_resultado(tv, path, texto, 1)
        
    def cambiar_alargamiento(self, tv ,path, texto):
        self.cambiar_resultado(tv, path, texto, 2)
        
    def cambiar_tenacidad(self, tv ,path, texto):
        self.cambiar_resultado(tv, path, texto, 3)
        
    def cambiar_grasa(self, tv ,path, texto):
        self.cambiar_resultado(tv, path, texto, 4)
        
    def cambiar_encogimiento(self, tv ,path, texto):
        self.cambiar_resultado(tv, path, texto, 5)
        
    def cambiar_humedad(self, tv ,path, texto):
        self.cambiar_resultado(tv, path, texto, 6)

    def cambiar_tolerancia(self, sp):
        loteCem = self.loteCem
        try:
            loteCem.tolerancia = float(sp.get_value()) / 100.0
            self.calcular_caracteristicas()
        except ValueError:
            utils.dialogo_info(titulo = 'VALOR INCORRECTO', 
                               texto = 'El valor %s no es correcto.' % (sp.get_value()), 
                               padre = self.wids['ventana'])
    
    def imprimir(self, boton):
        """
        Imprime la información en pantalla.
        """
        from formularios import reports
        from informes import geninformes
        txt = "LOTE: %s\n" % (self.wids['e_codigo'].get_text())
        txt += "PRODUCTO: %s\n\n" % (self.wids['e_nombre'].get_text())
        txt += "\nCaracterísticas del lote:\n"
        txt += "    DTEX: %s\n" % (self.wids['e_dtex'].get_text())
        txt += "    Tenacidad: %s\n" % (self.wids['e_tenacidad'].get_text())
        txt += "    Alargamiento: %s\n" % (self.wids['e_elongacion'].get_text())
        txt += "    Corte: %s\n" % (self.wids['e_corte'].get_text())
        txt += "    Grasa: %s\n" % (self.wids['e_grasa'].get_text())
        txt += "    Encogimiento: %s\n" % (self.wids['e_encogimiento'].get_text())
        txt += "    Color: %s\n" % (self.wids['e_color'].get_text())
        txt += "    Humedad: %s\n" % (self.wids['e_rizo'].get_text())
        loteCem = self.loteCem
        try:
            dtex = loteCem.bigbags[0].articulos[0].productoVenta.camposEspecificosBala.dtex
            tolerancia = loteCem.tolerancia
            mediatitulo = loteCem.mediatitulo
        except:
            utils.dialogo_info(titulo = 'ERROR', 
                               texto = 'Ocurrió un error buscando el tipo de fibra.', 
                               padre = self.wids['ventana'])
            dtex = 0
            tolerancia = 0
            mediatitulo = 0
        difmax = dtex * tolerancia
        diferencia = abs(mediatitulo - dtex)
        if round(diferencia, 2) > difmax:
            ok = False
        else:
            ok = True
        txt += "    Media de título: %s (%s)\n" % (self.wids['e_media'].get_text(), 
                                                   ok and "dentro del %s%% de tolerancia" % utils.float2str(self.wids['sp_tolerancia'].get_value(), 0) 
                                                   or "no cumple el %s%% de tolerancia" % utils.float2str(self.wids['sp_tolerancia'].get_value(), 0)
                                                   )
        txt += "    Desviación típica: %s\n" % (self.wids['e_desvtipica'].get_text())
        txt += "\nResultados de las pruebas:\n"
        model = self.wids['tv_pruebas'].get_model()
        for fila in model:
            txt += "    %s\n" % (fila[0])
            txt += "        Título (dtex): %s\n" % (fila[1])
            txt += "        Alargamiento (%%): %s\n" % (fila[2])
            txt += "        Tenacidad (cN/tex): %s\n" % (fila[3])
            txt += "        Grasa (%%): %s\n" % (fila[4])
            txt += "        Encogimiento (%%): %s\n" % (fila[5])
            txt += "        Humedad (%%): %s\n" % (fila[6])
        buff = self.wids['txt_observaciones'].get_buffer()
        txt += "\nObervaciones: %s\n" % buff.get_text(buff.get_start_iter(), buff.get_end_iter())
        reports.abrir_pdf(geninformes.texto_libre(txt, "Resultados de laboratorio: %s" % (self.objeto and self.objeto.codigo or "")))
        

if __name__=='__main__':
    a = ResultadosFibra()

