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
## consumo_balas_partida.py -- Consumo de fibra por partida.
###################################################################
## NOTAS:
##  
## ----------------------------------------------------------------
##  
###################################################################
## Changelog:
## 19 de septiembre de 2006 -> Inicio.
##
###################################################################
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time
try:
    from framework import pclases
except ImportError:
    import sys
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    from framework import pclases
import mx.DateTime
try:
    import geninformes
except ImportError:
    import sys
    sys.path.append('../informes')
    import geninformes
from ventana_progreso import VentanaProgreso
from ginn.formularios import reports as informes 

class ConsumoBalasPartida(Ventana):
        
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'consumo_balas_partida.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_partida/clicked': self.set_partida,
                       'b_imprimir/clicked': self.imprimir,
                       'b_drop_bala/clicked': self.drop_bala,
                       'b_add_balas/clicked': self.add_balas,
                       'b_add_producto/clicked': self.add_producto, 
                       'b_add_partida_gtx/clicked': self.add_partida_gtx, 
                       'b_drop_partida_gtx/clicked': self.drop_partida_gtx, 
                       'b_albaran/clicked': self.crear_albaran_interno, 
                       'b_phaser/clicked': self.descargar_de_terminal, 
                       'b_fecha/clicked': self.buscar_fecha, 
                       'b_from_pdp/clicked': self.fecha_from_pdp, 
                       'b_from_albaran/clicked': self.fecha_from_albaran
                      }
        self.add_connections(connections)
        cols = (('Nº Bala', 'gobject.TYPE_STRING', False, True, True, None),
                ('Peso', 'gobject.TYPE_FLOAT', True, True, False, self.cambiar_peso_bala),
                ('ID', 'gobject.TYPE_INT64', False, False, False, None))
        utils.preparar_listview(self.wids['tv_balas'], cols)
        # Al loro porque me voy a cargar la mitad de lo que ha hecho el preparar_listview.
        import gobject
        model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_FLOAT, gobject.TYPE_FLOAT, gobject.TYPE_INT64)
        self.wids['tv_balas'].set_model(model)
        self.wids['tv_balas'].get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        cell = gtk.CellRendererProgress()
        column = gtk.TreeViewColumn('Consumido', cell)
        column.add_attribute(cell, 'value', 2)
        column.set_sort_column_id(2)
        self.wids['tv_balas'].insert_column(column, 2) 
        cols = (("#Balas", "gobject.TYPE_INT64", False, True, False, None),
                ('Peso', 'gobject.TYPE_FLOAT', False, True, False, None),
                ("Lote", "gobject.TYPE_STRING", False, True, True, None),
                ("Fibra", "gobject.TYPE_STRING", False, True, False, None),
                ("ID", "gobject.TYPE_INT64", False, False, False, None))
        utils.preparar_listview(self.wids['tv_resumen'], cols)
        cols = (("Nª Partida", "gobject.TYPE_STRING", False, True, True, None), 
                ("Producto", "gobject.TYPE_STRING", False, True, False, None), 
                ("ID", "gobject.TYPE_STRING", False, False, False, None))
        utils.preparar_listview(self.wids['tv_gtx'], cols)
        if self.objeto == None:
            self.ir_a_primero()
        else:
            self.ir_a(objeto)
        gtk.main()

    def add_partida_gtx(self, boton):
        """
        Busca o crea una partida de geotextiles y la asocia con la de carga.
        """
        numpartida = utils.dialogo_entrada(titulo = "NÚMERO DE PARTIDA DE GEOTEXTILES", 
                                           texto = "Introduzca el número de partida de geotextiles", 
                                           padre = self.wids['ventana'])
        if numpartida != None:
            numpartida = numpartida.upper().replace("P-", "")
            partida = pclases.Partida.select(pclases.Partida.q.numpartida == numpartida)
            try:
                encontradas = partida.count()
            except:
                encontradas = 0
            if encontradas == 1:
                partida = partida[0]
                if partida.partidaCargaID != None:
                    if utils.dialogo(titulo = "PARTIDA USADA", 
                                     texto = "La partida de geotextiles %s ya se agregó a la partida de carga %s.\n¿Desea cambiarla a la actual?" % (partida.codigo, partida.partidaCarga.codigo), 
                                     padre = self.wids['ventana']):
                        partida.partidaCarga = self.objeto
                else:
                    partida.partidaCarga = self.objeto
            elif encontradas == 0:
                try:
                    numpartida = int(numpartida)
                except:
                    utils.dialogo_info(titulo = "ERROR NÚMERO DE PARTIDA", 
                                       texto = "El número de partida %s no es correcto." % (numpartida), 
                                       padre = self.wids['ventana'])
                    return
                partida = pclases.Partida(numpartida = numpartida, 
                                          codigo = "P-" + `numpartida`, 
                                          partidaCarga = self.objeto)
                pclases.Auditoria.nuevo(partida, self.usuario, __file__)
            else:
                self.logger.error("consumo_balas_partida.py::add_partida_gtx -> Encontrada más de una partida con el mismo número. NO DEBERÍA OCURRIR.")
        self.actualizar_ventana()

    def drop_partida_gtx(self, boton):
        """
        Elimina la relación de la partida con la partida de carga (pero no
        elimina la partida de la BD).
        """
        model, path = self.wids['tv_gtx'].get_selection().get_selected()
        idpartida = model[path][-1]
        try:
            partida = pclases.Partida.get(idpartida)
        except:
            return
        partida.partidaCarga = None
        self.actualizar_ventana()

    def ir_a_primero(self):
        """
        Hace que el primer registro -si lo hay- de la tabla implicada
        en el objeto del formulario sea el objeto activo.
        """
        try:
            # Anulo el aviso de actualización del envío que deja de ser activo.
            if self.objeto != None: self.objeto.notificador.desactivar()
            self.objeto = pclases.PartidaCarga.select(orderBy = "-numpartida")[0] # Selecciono todos y me quedo con el primero de la lista
            self.objeto.notificador.activar(self.aviso_actualizacion)        # Activo la notificación
        except IndexError:
            self.objeto = None   
        self.actualizar_ventana()

    def chequear_cambios(self):
        pass

    #def actualizar_ventana(self):
    #    self.rellenar_widgets()

    def rellenar_widgets(self):
        partida = self.get_partida()
        if partida != None:
            self.wids['e_partida'].set_text("%d (%s)" % (partida.numpartida, partida.codigo))
            self.wids['e_fecha'].set_text(utils.str_fechahora(partida.fecha))
        else:
            self.wids['e_partida'].set_text("")
            self.wids['e_fecha'].set_text("")
        self.rellenar_balas()
        self.rellenar_partidas_gtx()
        self.comprobar_permisos()

    def comprobar_permisos(self):
        """
        Comprueba si el usuario tiene permiso para escritura o nuevo y 
        deshabilita o habilita los botones según sea el caso.
        """
        # TODO: OJO. No compruebo si self.objeto != None.
        if self.usuario:
            try:
                ventana = pclases.Ventana.select(pclases.Ventana.q.fichero == "consumo_balas_partida.py")[0]     # OJO: HARCODED
            except IndexError:
                txt = "consumo_balas_partida::comprobar_permisos -> Ventana no encontrada en BD."
                self.logger.error(txt)
                print txt
            else:
                permiso = self.usuario.get_permiso(ventana)
                ws = ("b_add_partida_gtx", "b_drop_partida_gtx", "b_add_balas", "b_add_producto", "b_drop_bala", "b_phaser", "b_albaran", 
                      "e_fecha", "b_fecha", "b_from_pdp", "b_from_albaran")
                if not permiso.escritura and self.usuario.nivel > 1:
                    for w in ws:
                        self.wids[w].set_sensitive(False)
                else:
                    for w in ws:
                        self.wids[w].set_sensitive(True)
                self.wids['b_partida'].set_sensitive(
                    not(not permiso.nuevo and not permiso.lectura))
                if self.usuario.nivel > 1 and \
                        permiso.nuevo and \
                        pclases.PartidaCarga.select().count() > 0 and \
                        self.objeto == pclases.PartidaCarga.select(orderBy = "-id")[0]:
                    for w in ws:
                        self.wids[w].set_sensitive(True)
                if self.usuario.nivel <= 1:
                    for w in ws:
                        self.wids[w].set_sensitive(True)
            # print permiso.nuevo, permiso.escritura
            self.wids['b_albaran'].set_sensitive(
                len(self.objeto.get_balas_sin_albaran_interno()) > 0
                and (permiso.nuevo or permiso.escritura))
        else:
            self.wids['b_albaran'].set_sensitive(
                len(self.objeto.get_balas_sin_albaran_interno()) > 0)
 
    def rellenar_partidas_gtx(self):
        """
        Rellena la tabla con las partidas de geotextiles relacionadas con la
        de carga actual.
        """
        model = self.wids['tv_gtx'].get_model()
        model.clear()
        for partida in self.objeto.partidas:
            if partida.rollos != []:
                producto = partida.rollos[0].productoVenta.descripcion
            else:
                producto = "SIN PRODUCCIÓN"
            model.append((partida.codigo, producto, partida.id))

    def cambiar_peso_bala(self, cell, path, newtext):
        try:
            peso = float(newtext)
        except:
            utils.dialogo_info(titulo = 'ERROR DE FORMATO', texto = 'No introdujo un número válido')
            return
        model = self.wids['tv_balas'].get_model()
        idbala = model[path][-1]
        bala = pclases.Bala.get(idbala)
        bala.pesobala = peso
        bala.syncUpdate()
        self.rellenar_balas()

    def get_consumos_estimados(self, partida_carga, vpro):
        """
        Devuelve la suma de los pesos sin embalaje de todos los
        rollos producidos por todos los partes que pertenecen al 
        objeto partida recibido. También devuelve la media de las
        mermas de dichos partes.
        """
        consumos_estimados = 0
        mermas = []
        for partida in partida_carga.partidas:
            rollos = partida.rollos
            rollosd = partida.rollosDefectuosos
            i = 0.0
            tot = len(rollos) + len(rollosd)
            for rollo in rollos:
                vpro.set_valor(i/tot, 'Analizando geotextiles (%s)...' % (rollo.codigo))
                try:
                    # Consumo estimado en base al peso REAL (sin embalaje y en kilos) de los rollos de la partida.
                    peso_rollo = rollo.peso - rollo.articulos[0].productoVenta.camposEspecificosRollo.pesoEmbalaje
                    try:
                        merma = rollo.articulos[0].parteDeProduccion.merma
                    except:
                        merma = 0
                    mermas.append(merma)
                    consumo_rollo = peso_rollo / (1.0 - merma)
                    consumos_estimados += consumo_rollo
                except IndexError:
                    self.logger.error("consumo_balas_partida.py (get_consumos_estimados): ¡No se encontraron artículos en el rollo ID %d!" % (rollo.id))
                i += 1
            for rollo in rollosd:
                vpro.set_valor(i/tot, 'Analizando geotextiles (%s)...' % (rollo.codigo))
                try:
                    # Consumo estimado en base al peso REAL (sin embalaje y en kilos) de los rollos de la partida.
                    peso_rollo = rollo.peso - rollo.articulos[0].productoVenta.camposEspecificosRollo.pesoEmbalaje
                    try:
                        merma = rollo.articulos[0].parteDeProduccion.merma
                    except:
                        merma = 0
                    mermas.append(merma)
                    consumo_rollo = peso_rollo / (1.0 - merma)
                    consumos_estimados += consumo_rollo
                except IndexError:
                    self.logger.error("consumo_balas_partida.py (get_consumos_estimados): ¡No se encontraron artículos en el rollo_defectuoso ID %d!" % (rollo.id))
                i += 1
        try:
            media_mermas = sum(mermas) / len(mermas)
        except ZeroDivisionError:
            media_mermas = 0
        return consumos_estimados, media_mermas

    def func_orden_balas(self, b1, b2):
        if b1.id < b2.id:
            return -1
        if b1.id > b2.id:
            return 1
        return 0

    def rellenar_balas(self):
        model = self.wids['tv_balas'].get_model()
        model.clear()
        cantidad = 0
        partida = self.get_partida()
        lotes = {}
        if partida != None:
            vpro = VentanaProgreso(padre = self.wids['ventana'])
            vpro.mostrar()
            i = 0.0
            vpro.set_valor(i/1.0, 'Cargando datos...')
            while gtk.events_pending(): gtk.main_iteration(False)
            partida.sync()
            tot = len(partida.balas)
            consumos_estimados, merma = self.get_consumos_estimados(partida, vpro)
            self.wids['e_peso_gtx'].set_text("%s kg" % (utils.float2str(consumos_estimados, 2)))
            self.wids['label_gtx'].set_label("""Peso aproximado geotextiles producidos: 
<small><i>Contando merma estimada media del %.2f%%.
Sin embalaje.</i></small>""" % (merma))
            # try:
            #     producto = partida.rollos[0].articulos[0].productoVenta.descripcion
            # except IndexError:
            #     producto = "SIN PRODUCCIÓN"
            # except:
            #     producto = "ERROR"
            # self.wids['e_gtx'].set_text(producto)
            balas = [b for b in partida.balas]
            balas.sort(self.func_orden_balas)

            productos = {}

            for bala in balas:
                vpro.set_valor(i/tot, 'Cargando datos (%d)...' % (bala.numbala))
                
                lote_id = bala.loteID
                if lote_id not in productos:
                    lote = bala.lote
                    try:
                        producto = bala.articulos[0].productoVenta
                    except IndexError:
                        producto = None
                    productos[lote_id] = {'cantidad': 0, 'peso': 0, 'lote': lote, 'producto': producto}
                productos[lote_id]['peso'] += bala.pesobala
                productos[lote_id]['cantidad'] += 1

                if consumos_estimados >= bala.pesobala: # Se ha gastado la bala entera.
                    porcion_consumida = 100
                    consumos_estimados -= bala.pesobala
                else:
                    porcion_consumida = (consumos_estimados /  bala.pesobala) * 100  # % consumido
                    consumos_estimados = 0      # Ya no puedo descontar más o me quedaré por debajo de 0.
                model.append((bala.codigo, bala.pesobala, porcion_consumida, bala.id))
                cantidad += bala.pesobala
                i += 1
                
            model = self.wids['tv_resumen'].get_model()
            model.clear()
            for lote_id in productos:
                try:
                    lote = "%d (%s)" % (productos[lote_id]['lote'].numlote, productos[lote_id]['lote'].codigo)
                except AttributeError:
                    lote = ""
                try:
                    producto = productos[lote_id]['producto'].descripcion
                except AttributeError:
                    producto = ""
                model.append((productos[lote_id]['cantidad'],
                              productos[lote_id]['peso'],
                              lote, 
                              producto,
                              lote_id))
            vpro.ocultar()
        self.wids['e_total'].set_text("%s kg" % (utils.float2str(cantidad, 2)))

    def pedir_rango_balas(self):
        """
        Pide un rango de números de balas.
        Devuelve un generador de números
        de bala que comienza en el primero 
        del rango (o único, si solo se teclea uno)
        y acaba en el último del rango.
        """
        rango = utils.dialogo_entrada(titulo = 'INTRODUZCA RANGO',
                                      texto = 'Rango de números de bala o el código individual.\nEscriba el rango de códigos de la forma "xxxx-yyyy", ambos inclusive.\nO bien una lista de números separada por comas o espacios (xxxx, yyyy zzzz).',
                                      padre = self.wids['ventana'])
        articulos = []
        if rango == '' or rango == None:
            return rango
        try:
            if '-' in rango:
                ini, fin = rango.split('-')
                ini = int(ini)
                fin = int(fin)
                if fin < ini: 
                    ini, fin = fin, ini
            else:
                ini = int(rango)
                fin = ini
        except:
            utils.dialogo_info(titulo = 'CÓDIGO INCORRECTO', 
                               texto = 'Los códigos deben ser numéricos.\n\nVerifique que los ha escrito correctamente y que ha separado el rango con un guión.',
                               padre = self.wids['ventana'])
            return []
        return xrange(ini, fin+1)

    def drop_bala(self, w):
        model, paths=self.wids['tv_balas'].get_selection().get_selected_rows()
        if not paths:
            return
        for path in paths:
            idbala = model[path][-1]
            bala = pclases.Bala.get(idbala)
            # La anulo de la partida
            bala.partida = None
            # La quito del albarán interno si lo tenía
            bala.articulo.albaranSalida = None
            # Y la devuelvo al almacén principal
            bala.articulo.almacen = pclases.Almacen.get_almacen_principal()
            bala.articulo.syncUpdate()
            bala.syncUpdate()
        self.rellenar_balas()

    def add_bala(self, w):
        if self.get_partida() == None:
            utils.dialogo_info(titulo = 'ELIJA PARTIDA', 
                               texto = 'Debe seleccionar antes una partida.', 
                               padre = self.wids['ventana'])
            return
        rango = utils.dialogo_pedir_rango(padre = self.wids['ventana'])
        propia_cliente = pclases.DatosDeLaEmpresa.get_cliente()
        if rango == None:
            return
        elif rango == '':
            balas = pclases.Bala.select(pclases.Bala.q.partidaID == None)
            balas = [(b.id, b.numbala, b.pesobala) 
                     for b in balas 
                     if b.analizada() and 
                         (b.albaranSalida == None 
                          or b.albaranSalida.cliente == propia_cliente)]
            resp = utils.dialogo_resultado(balas, 
                                'SELECCIONE BALAS', 
                                cabeceras = ('ID', 'Número de bala', 'Peso'), 
                                multi = True, 
                                padre = self.wids['ventana'])
            if resp == [-1]:  # Ha cancelado
                return
            partida = self.get_partida()
            for id in resp:
                bala = pclases.Bala.get(id)
                if bala.claseb:
                    if utils.dialogo(titulo = 'BALA MARCADA COMO BAJA CALIDAD',
                                     texto = 'La bala está marcada como clase B. Esto puede provocar\nproblemas en la línea de producción.\n¿Está seguro de querer comsumir la bala de fibra?', 
                                     padre = self.wids['ventana']):
                        bala.partida = partida
                else:
                    bala.partida = partida
        else:
            self.logger.warning("%sconsumo_balas_partida::add_bala -> Añadiendo carga de cuarto manual." % (self.usuario and self.usuario.usuario + ": " or ""))
            for numbala in rango:
                balas = pclases.Bala.select(pclases.AND(
                    pclases.OR(pclases.Bala.q.numbala == numbala, 
                               pclases.Bala.q.numbala == -numbala), 
                    pclases.Bala.q.partidaCargaID == None))
                try:
                    bala = [b for b in balas if b.analizada() and 
                            (b.albaranSalida == None 
                             or b.albaranSalida.cliente == propia_cliente)][0]
                    # Numbala es UNIQUE. Sólo encontrará uno (o ninguno). (En 
                    # todo caso dos: normal y "D", con número igual pero 
                    # negativo) 
                    # Busco sólo entre las balas no usadas con otra partida y 
                    # que si tienen albarán, éste sea de la propia empresa.
                    bala.partida = self.get_partida()
                    # La saco del almacén.
                    bala.articulo.almacen = None
                    bala.articulo.syncUpdate()
                    bala.syncUpdate()
                except IndexError:
                    if balas.count() == 0:
                        utils.dialogo_info(titulo = 'BALA INCORRECTA',
                            texto = "El número de bala %d no se encontró en "\
                                    "el almacén." % numbala, 
                            padre = self.wids['ventana'])
                    else:
                        utils.dialogo_info(titulo = 'BALA NO DISPONIBLE',
                                           texto = """
                        La bala ha salido del almacén en un albarán o bien                                  
                        el lote %s al que pertenece  no ha sido analizado.                                  
                                                                                                            
                        Hasta que no se especifiquen desde laboratorio las                                  
                        características del lote, la bala %d no podrá ser                                   
                        usada en producción.                                                                
                        """ % (balas[0].lote.codigo, balas[0].numbala), 
                                           padre = self.wids['ventana'])
                    return

    def nueva_partida(self, codigo):
        if self.usuario:
            try:
                ventana = pclases.Ventana.select(pclases.Ventana.q.fichero == "consumo_balas_partida.py")[0]     # OJO: HARCODED
            except IndexError:
                txt = "consumo_balas_partida::comprobar_permisos -> Ventana no encontrada en BD."
                self.logger.error(txt)
                print txt
            else:
                permiso = self.usuario.get_permiso(ventana)
                if not permiso.nuevo and self.usuario.nivel > 1:
                    utils.dialogo_info(titulo = "NO TIENE PERMISOS", 
                                       texto = "No tiene permisos suficientes"
                                               " para crear partidas.", 
                                       padre = self.wids['ventana'])
                else:
                    try:
                        numpartida = int(codigo.upper().replace("PC", ""))
                    except ValueError:
                        utils.dialogo_info(titulo = "ERROR NÚMERO PARTIDA", 
                                           texto = "El número de partida debe"
                                                   " ser un entero.", 
                                           padre = self.wids['ventana'])
                        return
                    partida = pclases.PartidaCarga(numpartida = numpartida,
                                                codigo = "PC%d" % (numpartida))
                    pclases.Auditoria.nuevo(partida, self.usuario, __file__)
                    self.objeto = partida
                    self.actualizar_ventana()

    def set_partida(self, boton):
        """
        Hace activa una partida seleccionada para agregarle balas, imprimir su consumo, etc...
        """
        try:
            max_partida = pclases.PartidaCarga._connection.queryOne("SELECT MAX(numpartida) FROM partida_carga")[0]
            max_partida = "%d" % (max_partida + 1)
        except:
            max_partida = ""
        codigo = utils.dialogo_entrada(titulo = '¿NÚMERO DE PARTIDA?', 
                                       texto = 'Introduzca el número de partida de carga:', 
                                       padre = self.wids['ventana'], 
                                       valor_por_defecto = max_partida)
        if codigo == None:
            return 
        try:
            try:
                codigo = int(codigo.upper().replace("PC", ""))
                partida = pclases.PartidaCarga.select(pclases.PartidaCarga.q.numpartida == codigo)[0]
            except ValueError:
                partida = pclases.PartidaCarga.select(pclases.PartidaCarga.q.codigo == codigo)[0]
            self.objeto = partida
            self.actualizar_ventana()
        except TypeError:
            return
        except IndexError:
            codigo = `codigo`       # CHAPU
            if codigo.strip() != "" and utils.dialogo(titulo='¿CREAR PARTIDA?', 
                                                      texto='No se encontró la partida %s.\n¿Desea crear una nueva?' % (codigo), 
                                                      padre = self.wids['ventana']):
                self.nueva_partida(codigo)

    def imprimir(self, boton):
        """
        Imprime un listado del consumo de balas. 
        """
        partida_carga = self.get_partida()
        datos = {'partida': partida_carga}
        datos['partidas_gtx'] = ", ".join([p.codigo for p in partida_carga.partidas]) 
        model = self.wids['tv_balas'].get_model()
        datos['balas'] = []
        for iter in model:
            datos['balas'].append((iter[0], iter[1], ""))
        datos['balas'].append(("-" * 20, "-" * 20, ""))     # El último campo vacío es para que no queden los datos tan separados al imprimir.
        datos['balas'].append(("TOTAL CONSUMO FIBRA", self.wids['e_total'].get_text(), ""))
        datos['balas'].append(("TOTAL GEOTEXTILES PRODUCIDOS", self.wids['e_peso_gtx'].get_text(), ""))
        datos['balas'].append(("(para toda la partida, sin embalaje y con merma)", "", ""))
        model = self.wids['tv_resumen'].get_model()
        datos['balas'].append(("", "", ""))
        datos['balas'].append(("", "", ""))
        datos['balas'].append(("Resumen por lotes:", "", ""))
        for iter in model:
            datos['balas'].append(("%d balas (%s kg)." % (iter[0], utils.float2str(iter[1], 1)), 
                                   "Lote %s." % (iter[2]),
                                   iter[3]))
        informes.abrir_pdf(geninformes.consumo_fibra_partida(datos, utils.str_fecha(mx.DateTime.localtime()), cols_a_derecha=(0, 1, )))
    
    def add_balas(self, boton):
        """
        Añade balas por número o rango de números.
        """
        self.add_bala(boton)
        # self.rellenar_balas()
        self.actualizar_ventana()
    
    def add_producto(self, boton):
        # NO IMPLEMENTADO. Ni creo que llegue a hacer falta. (De momento se queda como oculto en el glade).
        pass 
    
    def get_partida(self):
        """
        Devuelve el objeto partida activo o None si no se encuentra.
        """
        return self.objeto

    def crear_albaran_interno(self, boton = None):
        """
        Crea un albarán interno de la partida actual y 
        lo abre en una nueva ventana.
        """
        albaran = self.objeto.crear_albaran_interno()
        self.wids['b_albaran'].set_sensitive(
            len(self.objeto.get_balas_sin_albaran_interno()) > 0)
            # OJO: Esto puede dar una condición de carrera si el usuario no 
            # tiene permisos y aún no se ha actualizado la ventana.
        import albaranes_de_salida
        ventana = albaranes_de_salida.AlbaranesDeSalida(
                    usuario = self.usuario, objeto = albaran)

    def descargar_de_terminal(self, boton):
        """
        lee los códigos almacenados en el terminal lector de códigos de 
        barras y:
            * si es un diccionario de partidas de carga y números de bala, 
              crea una partida de carga (si no existían) por cada una de 
              las claves del diccionario y relaciona con las mismas las 
              balas de la lista. finalmente, crea un albarán interno con 
              todas esas balas (uno por partida)y abre una ventana de 
              partida de carga (esta) y una de albarán de salida por 
              cada partida de carga y albarán interno procesado con éxito.
            * si es una lista de balas, las agrega a la partida de carga 
              actual y crea el albarán interno.
        """
        self.logger.warning("%sconsumo_balas_partida::descargar_de_terminal -> Iniciando descarga de balas consumidas/a consumir automática." % (self.usuario and self.usuario.usuario + ": " or ""))
        datos = None
        cancelar = False
        while datos == None and not cancelar:
            datos = utils.descargar_phaser(logger = self.logger)
            if datos == None:
                cancelar = not utils.dialogo(titulo = "¿VOLVER A INTENTAR?", 
                                             texto = "Se ha superado el tiempo de espera.\n¿Desea continuar?\n\n(Pulse SÍ para volver a intentar o NO para cancelar la operación.)", 
                                             padre = self.wids['ventana'])
            elif isinstance(datos, (type([]), type(()))):
                self.descargar_y_meter_balas_en_partida_carga_actual(datos)
            elif isinstance(datos, type({})):
                for partida_carga in datos: 
                    if partida_carga == self.objeto:
                        self.descargar_y_meter_balas_en_partida_carga_actual(datos[partida_carga])
                    else:
                        self.descargar_y_meter_balas_en_partida_carga(partida_carga, datos[partida_carga])

    def descargar_y_meter_balas_en_partida_carga_actual(self, lista_balas):
        """
        Mete las balas de la lista de balas en la partida de 
        carga actual en ventana, crea el albarán interno y 
        actualiza la ventana.
        """
        if self.introducir_balas_en_partida(lista_balas, self.objeto):
            self.crear_albaran_interno()
            self.actualizar_ventana()

    def descargar_y_meter_balas_en_partida_carga(self, partida, lista_balas):
        """
        PRECONDICIÓN: La partida debe existir en la BD.
        Mete las balas en la partida recibida, crea el albarán interno 
        correspondiente y abre los dos en sendas ventanas.
        """
        if self.introducir_balas_en_partida(lista_balas, partida):
            albaran = partida.crear_albaran_interno()
            if albaran != None:
                utils.dialogo_info(titulo = "ALBARÁN INTERNO CREADO", 
                                   texto = "Albarán %s creado para la partida %s con %d balas.\n\nPulse «Aceptar» para continuar." % (albaran.numalbaran, partida.codigo, len(albaran.articulos)), 
                                   padre = self.wids['ventana'])
            else:
                self.logger.error("consumo_balas_partida::descargar_y_meter_balas_en_partida_carga: Se han importado balas a la partida ID %d y sin embargo no se ha podido crear el albarán interno." % (partida.id))
                # ventanapartida = ConsumoBalasPartida(usuario = self.usuario, objeto = partida)
                # import albaranes_de_salida
                # ventanaalbaran = albaranes_de_salida.AlbaranesDeSalida(usuario = self.usuario, objeto = albaran)

    def introducir_balas_en_partida(self, lista_balas, partida):
        """
        Relaciona las balas con la partida recibida sii no están ya 
        en un albarán de salida ni en ninguna partida de carga. Si 
        es así, muestra un diálogo de error con un resumen de las 
        balas erróneas.
        Devuelve el número de balas introducidas correctamente.
        """
        malas = []
        buenas = []
        for bala in lista_balas:
            if bala.en_almacen() and bala.analizada():
                bala.partidaCarga = partida
                buenas.append(bala)
            else:
                malas.append(bala)
        if malas != []:
            texto_balas_malas = ""
            for bala_mala in malas:
                if bala_mala.partidaCargaID != None:
                    motivo = "Usada en partida de carga %s." % (bala_mala.partidaCarga.codigo)
                elif not bala.analizada():
                    motivo = "Bala perteneciente al lote no analizado %s." % (bala_mala.lote.codigo)
                elif bala_mala.albaranSalida != None:
                    motivo = "Vendida en albarán %s." % (bala_mala.albaranSalida.numalbaran)
                texto_balas_malas += " - %s: %s\n" % (bala_mala.codigo, motivo)
            utils.dialogo_info(titulo = "BALAS INCORRECTAS", 
                               texto = "Algunos códigos no se pudieron relacionar con la partida %s:\n\n"  % (partida.codigo) + texto_balas_malas + "\n\nPulse «Aceptar» para continuar.", 
                               padre = self.wids['ventana'])
        if buenas != []:
            utils.dialogo_info(titulo = "BALAS CORRECTAS", 
                               texto = "%d balas correctamente importadas a la partida %s.\n\nPulse «Aceptar» para continuar." % (len(buenas), partida.codigo), 
                               padre = self.wids['ventana'])
        return len(buenas)

    def buscar_fecha(self, boton):
        """
        Muestra el diálogo calendario y establece la fecha de la partida.
        """
        partida = self.get_partida()
        if partida != None:
            fecha = utils.mostrar_calendario(fecha_defecto = partida.fecha, padre = self.wids['ventana'])
            fecha = utils.parse_fecha(utils.str_fecha(fecha))
            partida.fecha = mx.DateTime.DateTimeFrom(day = fecha.day, month = fecha.month, year = fecha.year, 
                                                hour = partida.fecha.hour, minute = partida.fecha.minute, second = partida.fecha.second)
            self.wids['e_fecha'].set_text(utils.str_fechahora(partida.fecha))

    def fecha_from_pdp(self, boton):
        """
        Busca la fecha más temprana de producción y se la asigna a la partida 
        de carga.
        Si no hay producción aún, deja la actual.
        """
        partida = self.get_partida()
        if partida != None:
            fecha = partida.get_fecha_inicio()
            if fecha:
                partida.fecha = fecha
                self.wids['e_fecha'].set_text(utils.str_fechahora(partida.fecha))

    def fecha_from_albaran(self, boton):
        """
        Busca la fecha del albarán interno. Si hay más de uno, selecciona el 
        más temprano de ellos.
        Si no hay albarán interno, deja la actual.
        """
        partida = self.get_partida()
        if partida != None:
            fecha = partida.get_fecha_inicio()
            if fecha:
                albaranes_internos = list(partida.get_albaranes_internos())
                if albaranes_internos:
                    albaranes_internos.sort(lambda a1, a2: (a1.fecha < a2.fecha and -1) or (a1.fecha > a2.fecha and 1) or 0)
                    fecha = albaranes_internos[0].fecha
                    partida.fecha = mx.DateTime.DateTimeFrom(day = fecha.day, month = fecha.month, year = fecha.year, 
                                                    hour = partida.fecha.hour, minute = partida.fecha.minute, second = partida.fecha.second)
                    self.wids['e_fecha'].set_text(utils.str_fechahora(partida.fecha))


if __name__ == '__main__':
    t = ConsumoBalasPartida(usuario = pclases.Usuario.get(1))
    #t = ConsumoBalasPartida()
 
