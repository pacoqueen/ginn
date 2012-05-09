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
## Al salir con el evento destroy (bolaspa) pregunta dos veces si 
## quiere salir y la segunda vez ignora la respuesta.
##
###################################################################
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time, sqlobject
try:
    import pclases
except ImportError:
    import sys
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    import pclases
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes
from utils import _float as float


class ResultadosFibra(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'resultados_fibra.glade', objeto)
        connections = {'b_salir/clicked': self._salir,
                       'b_lote/clicked': self.set_lote,
                       'b_fecha/clicked': self.fecha,
                       'b_add/clicked': self.add,
                       'b_drop/clicked': self.drop,
                       'sp_tolerancia/value-changed': self.cambiar_tolerancia, 
                       'b_guardar_obs/clicked': self.guardar_obs, 
                       'b_consumos/clicked': self.ver_consumos, 
                       'b_imprimir/clicked': self.imprimir, 
                       'ventana/delete_event': self._salir
                      }
        self.add_connections(connections)
        self.activar_widgets(False)
        self.inicializar_ventana()
        if objeto == None:
            self.lote = None
        else:
            self.lote = objeto
            self.actualizar_ventana()
        gtk.main()

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
                   'frame4', 
                   'txt_observaciones', 
                   'b_consumos')
        for i in self.ws:
            self.wids[i].set_sensitive(valor)
        if self.usuario:
            try:
                ventana = pclases.Ventana.select(pclases.Ventana.q.fichero == "resultados_fibra.py")[0]     # OJO: HARCODED
            except IndexError:
                txt = "resultados_fibra::activar_widgets -> Ventana no encontrada en BD."
                self.logger.error(txt)
                print txt
            else:
                permiso = self.usuario.get_permiso(ventana)
                if not permiso.escritura and self.usuario.nivel > 1:
                    self.wids['tv_pruebas'].set_sensitive(False)
                    self.wids['txt_observaciones'].set_sensitive(False)
                if not permiso.nuevo and self.usuario.nivel > 1:
                    self.wids['b_add'].set_sensitive(False)
    
    def crear_listview(self, tv):
        cols = (('Fecha', 'gobject.TYPE_STRING', True, True, True, self.cambiar_fecha),
                ('Título (DTEX)', 'gobject.TYPE_STRING', True, True, False, self.cambiar_titulo), 
                ('Alargamiento (%)', 'gobject.TYPE_STRING', True, True, False, self.cambiar_alargamiento), 
                ('Tenacidad (cN/tex)', 'gobject.TYPE_STRING', True, True, False, self.cambiar_tenacidad), 
                ('Grasa (%)', 'gobject.TYPE_STRING', True, True, False, self.cambiar_grasa), 
                ('Encogimiento (%)', 'gobject.TYPE_STRING', True, True, False, self.cambiar_encogimiento), 
                ('Rizo', 'gobject.TYPE_STRING', True, True, False, self.cambiar_rizo), 
                ('ID', 'gobject.TYPE_STRING', False, False, False, None)) # Contiene los ID de los resultados separados por ','
        utils.preparar_listview(tv, cols)
        tv.get_column(1).get_cell_renderers()[0].set_property('xalign', 0.1) 
        tv.get_column(2).get_cell_renderers()[0].set_property('xalign', 0.1) 
        tv.get_column(3).get_cell_renderers()[0].set_property('xalign', 0.1) 
        tv.get_column(4).get_cell_renderers()[0].set_property('xalign', 0.1) 
        tv.get_column(5).get_cell_renderers()[0].set_property('xalign', 0.1) 
        tv.get_column(6).get_cell_renderers()[0].set_property('xalign', 0.1) 

    def ver_consumos(self, boton):
        """
        Muestra un diálogo de resultados con los consumos del 
        lote completo mostrado en pantalla.
        """
        if self.lote != None:
            consumos = self.lote.get_consumos()
            if consumos == {}:
                utils.dialogo_info(titulo = "SIN CONSUMO", 
                                   texto = "¡El lote %s no ha consumido productos en su fabricación!\n\nCompruebe que no esté vacío." % self.lote.codigo, 
                                   padre = self.wids['ventana'])
            else:
                filas = [("", p.descripcion, "%s %s" % (utils.float2str(consumos[p], 3, autodec = True), p.unidad)) for p in consumos]
                nada = utils.dialogo_resultado(filas, 
                                               titulo = 'CONSUMOS DEL LOTE %s EN PARTES DE PRODUCCIÓN' % (self.lote.codigo),
                                               cabeceras = ('', 'Producto', 'Cantidad consumida'), 
                                               padre = self.wids['ventana'])

    def inicializar_ventana(self):
        """
        Inicializa los widgets de la ventana.
        """
        self.crear_listview(self.wids['tv_pruebas'])
        self.wids['b_fecha'].set_property("visible", False)
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
        lote por fecha de la forma: [(fecha, prueba título, ..., "id0,id1,...id5")]
        """
        res = []
        for p in self.lote.pruebasTitulo:
            res.append([p.fecha, p.resultado, None, None, None, None, None, [p.id, 0, 0, 0, 0, 0]])
        for p in self.lote.pruebasElongacion:
            puesto = False
            for fila in res:
                if p.fecha == fila[0] and fila[2] == None:  # Hay hueco en la fecha
                    fila[2] = p.resultado
                    fila[-1][1] = p.id
                    puesto = True
                    break
            if not puesto:
                res.append([p.fecha, None, p.resultado, None, None, None, None, [0, p.id, 0, 0, 0, 0]])
        for p in self.lote.pruebasTenacidad:
            puesto = False
            for fila in res:
                if p.fecha == fila[0] and fila[3] == None:  # Hay hueco en la fecha
                    fila[3] = p.resultado
                    fila[-1][2] = p.id
                    puesto = True
                    break
            if not puesto:
                res.append([p.fecha, None, None, p.resultado, None, None, None, [0, 0, p.id, 0, 0, 0]])
        for p in self.lote.pruebasGrasa:
            puesto = False
            for fila in res:
                if p.fecha == fila[0] and fila[4] == None:  # Hay hueco en la fecha
                    fila[4] = p.resultado
                    fila[-1][3] = p.id
                    puesto = True
                    break
            if not puesto:
                res.append([p.fecha, None, None, None, p.resultado, None, None, [0, 0, 0, p.id, 0, 0]])
        for p in self.lote.pruebasEncogimiento:
            puesto = False
            for fila in res:
                if p.fecha == fila[0] and fila[5] == None:  # Hay hueco en la fecha
                    fila[5] = p.resultado
                    fila[-1][4] = p.id
                    puesto = True
                    break
            if not puesto:
                res.append([p.fecha, None, None, None, None, p.resultado, None, [0, 0, 0, 0, p.id, 0]])
        for p in self.lote.pruebasRizo:
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
                f[6] and "%d" % f[6] or "", \
                ','.join(map(str, f[7]))) for f in res]
        return res

    def rellenar_pruebas(self):
        """
        Introduce en el treeview las pruebas del lote seleccionado y 
        recalcula la característica del lote.
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
        lote = self.lote
        # La tolerancia depende del tipo de producto:
        try:
            dtex = lote.balas[0].articulos[0].productoVenta.camposEspecificosBala.dtex
        except:
            utils.dialogo_info(titulo = 'ERROR', 
                               texto = 'Ocurrió un error buscando el tipo de fibra.', 
                               padre = self.wids['ventana'])
            return       
        mediatitulo = 0
        sumatorio = 0
        desvtipica = 0
        for p in lote.pruebasTitulo:
            mediatitulo += p.resultado
            sumatorio += p.resultado**2.0
        try:
            mediatitulo /= len(lote.pruebasTitulo)
            desvtipica = sumatorio / len(lote.pruebasTitulo)
            desvtipica -= mediatitulo**2.0
            desvtipica = desvtipica**0.5    # ValueError cuando intente hacer raíz de número negativo. No debería ocurrir.
        except ZeroDivisionError:
            mediatitulo = 0
            desvtipica = 0
        lote.mediatitulo = mediatitulo
        self.wids['e_desvtipica'].set_text("%.2f" % desvtipica)
        self.marcar_tolerancia(dtex, mediatitulo, lote.tolerancia)
        self.calcular_caracteristicas_propias()
        self.rellenar_info_lote()

    def calcular_elongacion(self):
        """
        Calcula la media de los valores de y elongación.
        """
        lote = self.lote
        # La elongación depende del tipo de producto:
        try:
            dtex = lote.balas[0].articulos[0].productoVenta.camposEspecificosBala.dtex
        except:
            utils.dialogo_info(titulo = 'ERROR', 
                               texto = 'Ocurrió un error buscando el tipo de fibra', 
                               padre = self.wids['ventana'])
            return       
        mediaElongacion = 0
        for p in lote.pruebasElongacion:
            mediaElongacion += p.resultado
        try:
            mediaElongacion /= len(lote.pruebasElongacion)
        except ZeroDivisionError:
            mediaElongacion = 0
        # Elongación A(>90), B(70-90), C(<70)
        if dtex == 3.3: 
            if (mediaElongacion >= 40 and mediaElongacion <= 70):
                lote.elongacion = 'A'
            else:
                lote.elongacion = 'N'
        elif dtex == 4.4: 
            if (mediaElongacion >= 50 and mediaElongacion <= 80):
                lote.elongacion = 'A'
            else:
                lote.elongacion = 'N'
        elif dtex == 6.7: 
            if (mediaElongacion >=60 and mediaElongacion <= 90):
                lote.elongacion = 'A'
            else:
                lote.elongacion = 'N'
        elif dtex == 8.9: 
            if (mediaElongacion >=70 and mediaElongacion <= 100):
                lote.elongacion = 'A'
            else:
                lote.elongacion = 'N'   
        else:
            lote.elongacion = '?'

    def calcular_tenacidad(self):
        lote = self.lote
         # La elongación depende del tipo de producto:
        try:
            dtex = lote.balas[0].articulos[0].productoVenta.camposEspecificosBala.dtex
        except:
            utils.dialogo_info(titulo = 'ERROR', 
                               texto = 'Ocurrió un error buscando el tipo de fibra', 
                               padre = self.wids['ventana'])
            return       
        mediaTenacidad = 0
        for p in lote.pruebasTenacidad:
            mediaTenacidad += p.resultado
        try:
            mediaTenacidad /= len(lote.pruebasTenacidad)
        except ZeroDivisionError:
            mediaTenacidad = 0
        # Tenacidad: Alta(>=50), otra normal
        if mediaTenacidad >= 50:
            lote.tenacidad = 'A'
        else:
            lote.tenacidad = 'N'

    def calcular_grasa(self):
        lote = self.lote
         # La elongación depende del tipo de producto:
        try:
            dtex = lote.balas[0].articulos[0].productoVenta.camposEspecificosBala.dtex
        except:
            utils.dialogo_info(titulo = 'ERROR', 
                               texto = 'Ocurrió un error buscando el tipo de fibra', 
                               padre = self.wids['ventana'])
            return       
        ## Grasa
        mediaGrasa = 0
        for p in lote.pruebasGrasa:
            mediaGrasa += p.resultado
        try:
            mediaGrasa /= len(lote.pruebasGrasa)
        except ZeroDivisionError:
            mediaGrasa = 0
        lote.grasa = mediaGrasa
 
    def calcular_encogimiento(self):
        lote = self.lote
         # La elongación depende del tipo de producto:
        try:
            dtex = lote.balas[0].articulos[0].productoVenta.camposEspecificosBala.dtex
        except:
            utils.dialogo_info(titulo = 'ERROR', 
                               texto = 'Ocurrió un error buscando el tipo de fibra', 
                               padre = self.wids['ventana'])
            return       
        ## Encogimiento
        mediaEncogimiento = 0
        for p in lote.pruebasEncogimiento:
            mediaEncogimiento += p.resultado
        try:
            mediaEncogimiento /= len(lote.pruebasEncogimiento)
        except ZeroDivisionError:
            mediaEncogimiento = 0
        if mediaEncogimiento <= 10:
            lote.encogimiento = 'B'
        elif (mediaEncogimiento >10 and mediaEncogimiento<=15):
            lote.encogimiento = 'N'
        elif mediaEncogimiento > 15:
            lote.encogimiento = 'A'
        else:
            lote.encogimiento = '?'
    
    def calcular_rizo(self):
        lote = self.lote
         # La elongación depende del tipo de producto:
        try:
            dtex = lote.balas[0].articulos[0].productoVenta.camposEspecificosBala.dtex
        except:
            utils.dialogo_info(titulo = 'ERROR', 
                               texto = 'Ocurrió un error buscando el tipo de fibra', 
                               padre = self.wids['ventana'])
            return       
        mediaRizo = 0
        for p in lote.pruebasRizo:
            mediaRizo += p.resultado
        try:
            mediaRizo /= len(lote.pruebasRizo)
        except ZeroDivisionError:
            mediaRizo = 0
        ## Rizo
        lote.rizo = str(int(round(mediaRizo)))

    def calcular_caracteristicas_propias(self):
        self.calcular_elongacion()
        self.calcular_tenacidad()
        self.calcular_grasa()
        self.calcular_encogimiento()
        self.calcular_rizo()
        self.rellenar_info_lote()

    def marcar_tolerancia(self, dtex, mediatitulo, tolerancia):
        self.wids['ruler'].set_sensitive(False)
        diferencia = abs(mediatitulo-dtex)
        try:
            porcentaje = (diferencia*100)/dtex   # En formato 0 a 100 porque las posiciones del ruler son de -100 a 100
        except ZeroDivisionError:
            porcentaje = 0.0
        if mediatitulo < dtex:
            porcentaje *= -1
        self.wids['ruler'].set_property('position', porcentaje)
        difmax = dtex*tolerancia
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
        PRECONDICION: self.lote no puede ser None
        """
        try:
            self.lote.sync()
            self.rellenar_widgets()
        except sqlobject.SQLObjectNotFound:
                utils.dialogo_info(titulo = 'REGISTRO ELIMINADO', 
                                   texto = 'El registro ha sido borrado desde otro puesto.', 
                                   padre = self.wids['ventana'])
                self.lote = None
        self.activar_widgets(self.lote!=None)


    # --------------- Manejadores de eventos ----------------------------
    def guardar_obs(self, boton):
        """
        Guarda el contenido del TextView en el atributo observaciones.
        """
        if self.objeto != None:
            buffer = self.wids['txt_observaciones'].get_buffer()
            self.objeto.observaciones = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter())
            self.wids['b_guardar_obs'].set_sensitive(False)

    def add(self, w):
        if self.lote != None:
            model = self.wids['tv_pruebas'].get_model()
            model.append((utils.str_fecha(time.localtime()),
                          "", "", "", "", "", "", "0,0,0,0,0,0"))
        else:
            print "WARNING: Se ha intentano añadir una prueba con lote = None"
    
    def drop(self, w):
        """
        Borra una línea completa de resultados.
        """
        model, iter = self.wids['tv_pruebas'].get_selection().get_selected()
        if iter != None and utils.dialogo(titulo = 'BORRAR PRUEBA', texto = '¿Está seguro?', padre = self.wids['ventana']):
            ids = map(int, model[iter][-1].split(','))
            for columnaid in range(len(ids)):
                id = ids[columnaid]
                if id != 0:
                    clase = self.get_clase(columnaid+1)
                    prueba = clase.get(id)
                    prueba.destroySelf()
            self.rellenar_pruebas()

    def set_lote(self, w):
        comprobar_y_preguntar_si_guardar(self)
        numlote = utils.dialogo_entrada(titulo = 'Nº LOTE', 
                                        texto = 'Introduzca número de lote:',
                                        padre = self.wids['ventana'])
        if numlote != None:
            numlote = numlote.upper().replace("L-", "")
            lotes = pclases.Lote.select(pclases.Lote.q.codigo.contains(numlote))
            if lotes.count() == 0:
                utils.dialogo_info(titulo = 'LOTE NO ENCONTRADO', 
                                   texto = 'No se encontró ningún lote %s.' % (numlote), 
                                   padre = self.wids['ventana'])
                return
            elif lotes.count() > 1:
                filas = [(l.id, l.numlote, l.codigo, l.tenacidad, l.elongacion, l.rizo, l.encogimiento) for l in lotes]
                idlote = utils.dialogo_resultado(filas, 
                                                 titulo = 'SELECCIONE LOTE',
                                                 cabeceras = ('ID', 'Número', 'Código', 'Tenacidad', 'Elongación', 'Rizo', 'Encogimiento'), 
                                                 padre = self.wids['ventana'])
                if idlote < 0:
                    return
                lote = pclases.Lote.get(idlote)
            else:
                lote = lotes[0]
            if len(lote.balas) == 0:
                utils.dialogo_info(titulo = 'LOTE VACÍO', 
                                   texto = 'El lote no contiene balas, no puede\nrealizar pruebas sobre un lote vacío.', 
                                   padre = self.wids['ventana'])
                self.lote = None
                return
            self.lote = lote
            self.actualizar_ventana()
    
    def rellenar_widgets(self):
        self.objeto = self.lote
        self.activar_widgets(self.lote != None)
        if self.lote != None:
            self.rellenar_info_lote()
            self.rellenar_pruebas()
            self.rellenar_observaciones()
    
    def rellenar_observaciones(self):
        """
        Introduce las observaciones de la partida en el TextView.
        """
        self.wids['txt_observaciones'].get_buffer().set_text(self.objeto.observaciones)
        self.wids['b_guardar_obs'].set_sensitive(False)

    def rellenar_info_lote(self):
        """
        PRECONDICIÓN: self.lote != None y len(self.lote.balas) > 0
        """
        lote = self.lote
        self.wids['e_codigo'].set_text("%d (%s)" % (lote.numlote, lote.codigo))
        self.wids['e_nombre'].set_text(lote.balas[0].articulos[0].productoVenta.nombre)
        self.wids['e_dtex'].set_text("%.1f DTEX" % lote.balas[0].articulos[0].productoVenta.camposEspecificosBala.dtex)
        self.wids['e_corte'].set_text(`lote.balas[0].articulos[0].productoVenta.camposEspecificosBala.corte`)
        self.wids['e_color'].set_text(lote.balas[0].articulos[0].productoVenta.camposEspecificosBala.color or '')
        self.wids['e_tenacidad'].set_text(lote.tenacidad or '')
        self.wids['e_elongacion'].set_text(lote.elongacion or '')
        self.wids['e_rizo'].set_text(lote.rizo or '')
        self.wids['e_encogimiento'].set_text(lote.encogimiento or '')
        self.wids['e_grasa'].set_text(lote.grasa and ("%.2f %%" % lote.grasa) or '')
        self.wids['e_media'].set_text("%.2f DTEX" % lote.mediatitulo or 0)
        try:
            self.wids['sp_tolerancia'].set_value(lote.tolerancia*100.0)
        except:
            self.wids['sp_tolerancia'].set_value(20)
            lote.tolerancia = 0.2

    def fecha(self, w):
        self.wids['e_fecha'].set_text(utils.str_fecha(utils.mostrar_calendario(fecha_defecto = self.objeto and self.objeto.fecha or None, padre = self.wids['ventana'])))

    def cambiar_fecha(self, cell, path, texto):
        try:
            fecha = time.strptime(texto, '%d/%m/%Y')
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
            clase = pclases.PruebaRizo
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
            id = ids[columnaid]
            if id == 0:
                if texto != "":
                    fecha = time.strptime(model[path][0], '%d/%m/%Y') 
                    prueba = clase(fecha = fecha, 
                                   resultado = resultado,
                                   lote = self.lote)
                    ids[columnaid] = prueba.id
                    model[path][-1] = ','.join(map(str, ids))
                    if columna != 6:
                        model[path][columna] = "%.2f" % resultado
                    else:
                        model[path][columna] = "%d" % resultado
            else:
                prueba = clase.get(int(id))
                if texto == "": 
                    try:
                        prueba.destroySelf()
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
#            print model[path][-1]
#            self.rellenar_pruebas()

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
        
    def cambiar_rizo(self, tv ,path, texto):
        self.cambiar_resultado(tv, path, texto, 6)

    def _salir(self, *args, **kw):
        """
        Si hay cambios pendientes en observaciones, pregunta.
        Después llama a la función salir heredada.
        """
        comprobar_y_preguntar_si_guardar(self)
        self.salir(*args, **kw)

    def cambiar_tolerancia(self, sp):
        lote = self.lote
        try:
            lote.tolerancia = float(sp.get_value()) / 100.0
            self.calcular_caracteristicas()
        except ValueError:
            utils.dialogo_info(titulo = 'VALOR INCORRECTO', 
                               texto = 'El valor %s no es correcto.' % (sp.get_value()), 
                               padre = self.wids['ventana'])
    def imprimir(self, boton):
        """
        Imprime la información en pantalla.
        """
        import informes, geninformes
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
        txt += "    Rizo: %s\n" % (self.wids['e_rizo'].get_text())
        lote = self.lote
        try:
            dtex = lote.balas[0].articulos[0].productoVenta.camposEspecificosBala.dtex
            tolerancia = lote.tolerancia
            mediatitulo = lote.mediatitulo
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
        buffer = self.wids['txt_observaciones'].get_buffer()
        txt += "\nObervaciones: %s\n" % buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter())
        informes.abrir_pdf(geninformes.texto_libre(txt, "Resultados de laboratorio: %s" % (self.objeto and self.objeto.codigo or "")))
        
def comprobar_y_preguntar_si_guardar(ventana_padre):
    """
    Comprueba si hay cambios pendientes de guardar y guarda 
    si se responde que sí.
    """
    if (ventana_padre.wids['b_guardar_obs'].get_property("sensitive") and 
        ventana_padre.wids['txt_observaciones'].get_property("sensitive") and 
        utils.dialogo(titulo = "¿GUARDAR?", 
                      texto = "Hay cambios pendientes de guardar.\n¿Desea hacerlo ahora?", 
                      padre = ventana_padre.wids['ventana'])):
        ventana_padre.guardar_obs(None)


if __name__=='__main__':
    a = ResultadosFibra()

