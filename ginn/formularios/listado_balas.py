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
## listado_balas.py --
###################################################################
## NOTAS:
##
###################################################################
## Changelog:
##
##
###################################################################

import gtk
import time
import datetime
import mx.DateTime
import pygtk
pygtk.require('2.0')
import re
import sys
from formularios.ventana import Ventana
from formularios import utils
from framework import pclases
from informes import geninformes

rexpcajas = re.compile("\([\d]+/[\d]+\)")

class ListadoBalas(Ventana):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        Ventana.__init__(self, 'listado_balas.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin,
                       'b_buscar/clicked': self.buscar_balas, 
                       'b_imprimir/clicked': self.imprimir, 
                       'b_etiquetas/clicked': self.etiquetar, 
                       'b_exportar/clicked': self.exportar}
        self.add_connections(connections)
        cols = (('Código', 'gobject.TYPE_STRING', False, True, False, None), 
                ('Fecha Fab.','gobject.TYPE_STRING',False,True,False,None),
                ('Peso', 'gobject.TYPE_STRING', False, True, False, None),  
                ('Lote','gobject.TYPE_STRING',False,True,False,None),
                ('Albarán','gobject.TYPE_STRING',False,True,False,None),
                ('Partida','gobject.TYPE_STRING',False,True,False,None),
                ('Analizada', 'gobject.TYPE_BOOLEAN',False,True,False,None),
                ('Clase B', 'gobject.TYPE_BOOLEAN', False, True, False, None), 
                ('Almacén', 'gobject.TYPE_STRING', False, True, False, None),
                ('PUID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_balas'], cols)
        self.wids['tv_balas'].get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        self.wids['tv_balas'].connect("row-activated", abrir_trazabilidad, 
                                                       self.usuario)
        temp = time.localtime()
        self.fin = mx.DateTime.localtime()
        self.inicio = None
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        gtk.main()
    
    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        tv = self.wids['tv_balas']
        abrir_csv(treeview2csv(tv))

    def etiquetar(self, boton):
        """
        Genera el PDF de las etiquetas seleccionadas en el TreeView.
        Para poder imprimir es necesario que el usuario tenga el permiso 
        "escritura" sobre la ventana.
        """
        # TODO: Falta adaptar esto a cajas. Para palés ya está. 
        ventana = pclases.Ventana.select(               # OJO: HARCODED
                    pclases.Ventana.q.fichero == "listado_balas.py")[0]
        if (self.usuario == None 
            or self.usuario.get_permiso(ventana).escritura): 
            sel = self.wids['tv_balas'].get_selection()
            model, paths = sel.get_selected_rows()
            balas_defecto = []
            for path in paths: 
                balas_defecto.append(model[path][0])
                balas_defecto.sort()
            balas_defecto = ', '.join(balas_defecto)
            from formularios import reports
            entrada = utils.dialogo_entrada(titulo='ETIQUETAS', 
                        texto="Introduzca los números de bala o bigbags que "
                              "desea etiquetar separados por coma o espacio."
                              "\nUse guiones para especificar rangos.)",
                        valor_por_defecto = balas_defecto,
                        padre = self.wids['ventana'])
            if entrada != None:
                entrada = entrada.replace(",", " ")
                codigos = [c for c in entrada.split() if c.strip() != ""]
                balas, bigbags, balas_cable, pales = separar_balas_y_bigbags_from_codigos(codigos)
                etiqsbalas = preparar_datos_etiquetas_balas(balas)
                etiqsbalascable = preparar_datos_etiquetas_balas_cable(balas_cable)
                if etiqsbalas:
                    etpdf = geninformes.etiquetasBalasEtiquetadora(etiqsbalas)
                    reports.abrir_pdf(etpdf)
                if bigbags:
                    etpdf = geninformes.etiquetasBigbags(bigbags)
                    reports.abrir_pdf(etpdf)
                if balas_cable:
                    etpdf = geninformes.etiquetasBalasCableEtiquetadora(
                                etiqsbalascable)
                    reports.abrir_pdf(etpdf)
                if pales:
                    from partes_de_fabricacion_bolsas import imprimir_etiquetas_pales
                    imprimir_etiquetas_pales(pales, self.wids['ventana'], mostrar_dialogo = True)
        else:
            utils.dialogo_info(titulo = "USUARIO SIN PRIVILEGIOS", 
                texto = "Para poder crear etiquetas de balas existentes es ne"\
                        "cesario\nque tenga permiso de escritura sobre la ven"\
                        "tana actual.", 
                padre = self.wids['ventana'])

    def imprimir(self, boton):
        """
        Crea un PDF con el contenido del TreeView.
        """
        datos = []
        model = self.wids['tv_balas'].get_model()
        for i in model:
            if i[4] == "-":
                if i[5] == "-":
                    #en_almacen = "En almacén"
                    en_almacen = i[8]
                else:
                    en_almacen = "Consumida"
            else:
                en_almacen = "Vendida"
            if (self.wids['ch_filtrar'].get_active() and i[4] == i[5] == "-") or (not self.wids['ch_filtrar'].get_active()):
                texto_baja_calidad = "Baja calidad"
                try:
                    if self.producto.es_bolsa():
                        texto_baja_calidad = "Bolsas insuficientes"
                except (NameError, AttributeError):
                    pass    # Dejo el texto como estaba
                datos.append((i[0], i[1], i[2], i[3], i[4], i[5], en_almacen, 
                              i[6] and "Sí" or "No", 
                              i[7] and texto_baja_calidad or ""))
        datos.append(("---", ) * 9)
        datos.append(("", "Total almacén:", 
                      self.wids['e_total_almacen'].get_text(), 
                      "Total fabricado:", 
                      self.wids['e_total_fabricado'].get_text(), "", "", "", 
                      "")) 
        if not self.inicio:
            fechaInforme = 'Hasta: %s' % (utils.str_fecha(self.fin))
        else:
            fechaInforme = (utils.str_fecha(self.inicio) + ' - ' 
                            + utils.str_fecha(self.fin))
        if datos != []:
            desc_producto = self.wids['e_descripcion'].get_text()
            listado_pdf = geninformes.listado_balas(datos, desc_producto, 
                                                    fechaInforme)
            from formularios import reports
            reports.abrir_pdf(listado_pdf)

    def set_inicio(self,boton):
        try:
            datinw = utils.parse_fecha(self.wids['e_fechainicio'].get_text())
            temp = utils.mostrar_calendario(datinw,
                                            padre = self.wids['ventana'])
        except:
            temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
        self.inicio = mx.DateTime.DateTimeFrom(day = temp[0], 
                                               month = temp[1], 
                                               year = temp[2])

    def get_unambiguous_fecha(self, fecha):
        try:
            res = fecha.strftime('%B %d, %Y')
        except AttributeError:  # Fecha es None
            return ""
        trans = {'January': 'enero',
                 'February': 'febrero',
                 'March': 'marzo',
                 'April': 'abril',
                 'May': 'mayo',
                 'June': 'junio',
                 'July': 'julio',
                 'August': 'agosto',
                 'September': 'septiembre',
                 'October': 'octubre',
                 'November': 'noviembre',
                 'December': 'diciembre'}
        for in_english in trans:
            res = res.replace(trans[in_english], in_english)
        return res

    def set_fin(self,boton):
        try:
            temp = utils.mostrar_calendario(utils.parse_fecha(self.wids['e_fechafin'].get_text()), padre = self.wids['ventana'])
        except:
            temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.fin = mx.DateTime.DateTimeFrom(day = temp[0], month = temp[1], year = temp[2])

    def chequear_cambios(self):
        pass

    def insert_caja(self, model, caja, iterpadre):
        """
        Inserta la caja en el model.
        """
        fechafab = caja.articulo.get_fecha_fabricacion()
        # Lo mismo con el albarán.
        albaran = caja.articulo.albaranSalida
        almacen = caja.articulo.almacen
        nombrealmacen = almacen and almacen.nombre or ""
        # Actualizo almacén del padre.
        if nombrealmacen and nombrealmacen not in model[iterpadre][8]:
            if not model[iterpadre][8]:
                model[iterpadre][8] = nombrealmacen
            else:
                model[iterpadre][8] += ", " + nombrealmacen
        # Actualizo albarán del padre
        numalbaran = albaran and albaran.numalbaran or "-"
        if numalbaran != "-" and numalbaran not in model[iterpadre][4]:
            if model[iterpadre][4] == "-":
                model[iterpadre][4] = numalbaran
            else:
                model[iterpadre][4] += ", " + numalbaran
        fila = (caja.codigo, 
                utils.str_fecha(fechafab), 
                caja.peso, 
                caja.pale.partidaCem.codigo, # Columna "lote", pero es partida.
                numalbaran, 
                "-", # No se consumen en partidas.
                False, 
                caja.claseb, 
                nombrealmacen, 
                caja.puid)
        return model.append(iterpadre, fila)

    def insert_pale(self, model, pale):
        """
        Inserta la información del palé en el model.
        """
        pdp = pale.get_parte_de_produccion()
        try:
            fechafab = pdp.fecha
        except AttributeError:
            self.logger.warning("listado_balas.py::insert_pale -> Palé %d no"
                          " tiene parte de producción relacionado." % pale.id)
            fechafab = pale.fechahora
        claseB = pale.es_clase_b()
        fila = (pale.codigo, 
                utils.str_fecha(fechafab), 
                pale.calcular_peso(), 
                pale.partidaCem.codigo, # Columna "lote", pero es partida.
                "-", # El albarán lo irán actualizando las cajas conforme 
                     # se vayan insertando.
                "-", # No se consumen en partidas.
                False,  # ¿Analizada? Que yo sepa no se analizan los palés. Sí 
                        # la fibra original de los bigbag, pero eso no 
                        # me afecta en absoluto.
                claseB, 
                "", # Lo mismo con el almacén.
                pale.puid)
        return model.append(None, fila)

    def rellenar_pales(self, rs_cajas):
        """
        Rellena el model pero con los palés de los artículos en lugar de 
        con los artículos (bolsas) en sí.
        """
        # Vamos a ir montando un diccionario de iteradores de palés y de ellos 
        # voy a colgar las cajas.
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        model = self.wids['tv_balas'].get_model()
        model.clear()
        kilos_almacen = 0  # @UnusedVariable
        kilos_fabricados = 0
        bultos_almacen = 0
        bultos_fabricados = 0
        i = 0.0
        tot = rs_cajas.count()
        pales = {}
        cajas_tratadas = []
        cajas_por_pale = {}
        self.wids['tv_balas'].freeze_child_notify()
        self.wids['tv_balas'].set_model(None)
        vpro.mostrar()
        for caja in rs_cajas:
            vpro.set_valor(i/tot, 'Añadiendo cajas por palé... (%s)' % 
                                    caja.codigo)
            i += 1
            if pclases.DEBUG:
                print caja.codigo, len(cajas_tratadas)
            if caja in cajas_tratadas:
                if pclases.DEBUG:
                    print "Esta me la salto. Ya está metida de otra bolsa."
                continue
            cajas_tratadas.append(caja)
            paleid = caja.pale.id
            try:
                iterpale = pales[paleid]
            except KeyError:
                pale = pclases.Pale.get(paleid)
                iterpale = self.insert_pale(model, pale)
                pales[paleid] = iterpale
                # Como los totales van por kilos y palés, aprovecho ahora.
                # Lleva el el total de cajas en almacén de ese palé, el número 
                # de cajas en almacén del palé y los kilos de esas cajas.
                cajas_por_pale[paleid] = {'Total cajas': pale.numcajas, 
                                          'Cajas en almacén': 0, 
                                          'Kilos en almacén': 0.0}
                bultos_fabricados += 1 
                kilos_fabricados += pale.calcular_peso()
            kilos_caja = caja.peso
            albaran = caja.albaranSalida
            if not albaran or albaran.fecha > self.fin:    # Cajas en almacén.
                # FILTRO LOS ALBARANES FUERA DEL RANGO SUPERIOR DE FECHAS PARA 
                # QUE APAREZCAN COMO QUE ESTABAN EN ALMACÉN ANTES DE ESE DÍA.
                cajas_por_pale[paleid]['Cajas en almacén'] += 1
                cajas_por_pale[paleid]['Kilos en almacén'] += kilos_caja
            else:   # Ya no está en almacén. Tiene albarán o lo tiene anterior 
                    # a la fecha superior de filtro.
                if pclases.DEBUG:
                    print "Esta caja (%s) no está en almacén." % caja.codigo
            itercaja = self.insert_caja(model, caja, iterpale)  # @UnusedVariable
        # Ahora añado la información de las cajas en almacén de cada palé.
        tot = len(cajas_por_pale)
        i = 0
        for idpale in pales:
            vpro.set_valor(i/tot, 
                           'Analizando palés incompletos... (%d)' % idpale)
            iterpale = pales[idpale]
            total = cajas_por_pale[idpale]['Total cajas']
            en_almacen = cajas_por_pale[idpale]['Cajas en almacén']
            model[iterpale][0] += " (%d/%d)" % (en_almacen, total)
            i += 1
        # Restauro el model y pongo totales.
        self.wids['tv_balas'].set_model(model)
        self.wids['tv_balas'].thaw_child_notify()
        vpro.ocultar()
        kilos_almacen = sum([cajas_por_pale[idpale]['Kilos en almacén'] 
                             for idpale in cajas_por_pale])
        bultos_cajas = sum([cajas_por_pale[idpale]['Cajas en almacén'] 
                            for idpale in cajas_por_pale])
        bultos_cajas_totales = sum([cajas_por_pale[idpale]['Total cajas'] 
                                    for idpale in cajas_por_pale])
        try:
            bultos_almacen = ((bultos_fabricados * bultos_cajas) 
                                / bultos_cajas_totales)
            # bultos_fabricados son los palés en total fabricados.
            # bultos_cajas son los palés que hay en almacén.
            # Y bultos_cajas_totales son las cajas que hay en total en los 
            # palés fabricados. Es una simple regla de tres.
        except ZeroDivisionError:
            bultos_almacen = 0
        self.wids['e_total_almacen'].set_text("%s kg (%s palés)" % (
            utils.float2str(kilos_almacen), 
            utils.float2str(bultos_almacen, autodec = True)))
        self.wids['e_total_fabricado'].set_text("%s kg (%d palés)" % (
            utils.float2str(kilos_fabricados), bultos_fabricados))
        self.colorear(self.wids['tv_balas'])

    def rellenar_tabla(self, lista_balas = None, lista_bigbags = None, 
                       lista_cajas = None):
        """
        Rellena el model con el listado de balas correspondiente
        """
        self.wids['tv_balas'].get_column(5).set_property("visible", 
                                                         lista_cajas == None)
        if lista_cajas != None:   # Delego en otra función
            self.rellenar_pales(lista_cajas)
            return
        from ventana_progreso import VentanaProgreso
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        model = self.wids['tv_balas'].get_model()
        model.clear()
        kilos_almacen = 0
        kilos_fabricados = 0
        bultos_almacen = 0
        bultos_fabricados = 0
        i = 0.0
        if lista_balas != None:
            lista = lista_balas
        elif lista_bigbags != None:
            lista = lista_bigbags
        else:
            return
        tot = lista.count()
        vpro.mostrar()
        # XXX Primer intento de acelerar los treeview
        self.wids['tv_balas'].freeze_child_notify()
        self.wids['tv_balas'].set_model(None)
        # XXX
        for t in lista:
            # kilos = t.bala.pesobala
            kilos = t.peso
            vpro.set_valor(i/tot, 'Añadiendo %s...' % t.codigo_interno)
            if t.albaranSalida != None and t.albaranSalida.fecha <= self.fin:
                # FILTRO LOS ALBARANES FUERA DEL RANGO SUPERIOR DE FECHAS PARA 
                # QUE APAREZCAN COMO QUE ESTABAN EN ALMACÉN ANTES DE ESE DÍA.
                if t.balaID != None:
                    model.append(None, 
                                 (t.bala.codigo,
                                  utils.str_fecha(t.bala.fechahora),
                                  utils.float2str(t.bala.pesobala, 1), 
                                  t.bala.lote.numlote,
                                  "%s (%s)" % (t.albaranSalida.numalbaran,
                                    utils.str_fecha(t.albaranSalida.fecha)), 
                                  t.bala.partidaCarga 
                                    and t.bala.partidaCarga.codigo or "-",
                                  t.bala.analizada(),
                                  t.bala.claseb, 
                                  t.almacen and t.almacen.nombre or "", 
                                  t.puid))
                elif t.bigbagID != None:
                    if t.bigbag.parteDeProduccionID:
                        info_consumo = " (consumido el %s. %s)" % (
                            utils.str_fecha(t.bigbag.parteDeProduccion.fecha), 
                            t.bigbag.parteDeProduccion.partidaCem.codigo)
                    else:
                        info_consumo = ""
                    model.append(None, 
                                 (t.bigbag.codigo,
                                  utils.str_fecha(t.bigbag.fechahora),
                                  utils.float2str(t.bigbag.pesobigbag, 1), 
                                  t.bigbag.loteCem.codigo,
                                  t.albaranSalida.numalbaran + info_consumo,
                                  '-',
                                  False,
                                  t.bigbag.claseb, 
                                  t.almacen and t.almacen.nombre or "", 
                                  t.puid))
                elif t.balaCableID != None:
                    model.append(None, 
                                 (t.balaCable.codigo,
                                  utils.str_fecha(t.balaCable.fechahora),
                                  utils.float2str(t.balaCable.peso, 1), 
                                  "N/A",
                                  t.albaranSalida.numalbaran,
                                  '-',
                                  False,
                                  True, 
                                  t.almacen and t.almacen.nombre or "", 
                                  t.puid))
                kilos_fabricados += kilos
                bultos_fabricados += 1 
            elif (t.bala and t.bala.partidaID != None 
                  and (t.bala.partida.fecha <= self.fin + mx.DateTime.oneDay
                       or t.bala.partida.fecha <= datetime.datetime(
                        *(self.fin + datetime.timedelta(days = 1)).tuple()[:3])
                      )
                 ): 
                    # La fecha de la partida lleva hora, hay que compararla con las 00:00:00 del día siguiente.
                # FILTRO LAS BALAS CONSUMIDAS EN UNA PARTIDA PERO POSTERIORMENTE A LA FECHA DE FIN DE RANGO DE BÚSQUEDA.
                if t.albaranSalida:
                    numalbaran = t.albaranSalida.numalbaran 
                else: # No tiene albarán de consumo, pero SÍ partida de carga.
                    numalbaran = "Consumida en partida carga %d" % (
                        t.bala.partidaCarga.numpartida)
                model.append(None, 
                             (t.bala.codigo,
                              utils.str_fecha(t.bala.fechahora),                        
                              utils.float2str(t.bala.pesobala, 1), 
                              t.bala.lote.numlote,
                              numalbaran,
                              t.bala.partida.codigo,
                              t.bala.analizada(),
                              t.bala.claseb, 
                              t.almacen and t.almacen.nombre or "", 
                              t.puid))
                kilos_fabricados += kilos
                bultos_fabricados += 1
            else:
                kilos_fabricados += kilos
                bultos_fabricados += 1
                kilos_almacen += kilos
                bultos_almacen += 1
                if t.balaID != None:
                    if t.bala.lote != None: 
                        numlote = t.bala.lote.numlote
                    else:
                        numlote = "¡SIN LOTE!"
                    model.append(None, 
                                 (t.bala.codigo,
                                  utils.str_fecha(t.bala.fechahora),
                                  utils.float2str(t.bala.pesobala, 1), 
                                  numlote,
                                  '-',
                                  '-',
                                  t.bala.analizada(),
                                  t.bala.claseb, 
                                  t.almacen and t.almacen.nombre or "", 
                                  t.puid))
                elif t.bigbagID != None:
                    model.append(None, 
                                 (t.bigbag.codigo,
                                  utils.str_fecha(t.bigbag.fechahora),
                                  utils.float2str(t.bigbag.pesobigbag, 1), 
                                  t.bigbag.loteCem.codigo,
                                  '-',
                                  '-',
                                  False,
                                  t.bigbag.claseb, 
                                  t.almacen and t.almacen.nombre or "", 
                                  t.puid))
                elif t.balaCableID != None:
                    numlote = "N/A"
                    model.append(None, 
                                 (t.balaCable.codigo,
                                  utils.str_fecha(t.balaCable.fechahora),
                                  utils.float2str(t.balaCable.peso, 1), 
                                  numlote,
                                  '-',
                                  '-',
                                  False,
                                  True, 
                                  t.almacen and t.almacen.nombre or "", 
                                  t.puid))
            i += 1
        # XXX Primer intento de acelerar los treeview
        self.wids['tv_balas'].set_model(model)
        self.wids['tv_balas'].thaw_child_notify()
        # XXX
        vpro.ocultar()

        self.wids['e_total_almacen'].set_text("%s kg (%d bultos)" % (
            utils.float2str(kilos_almacen), bultos_almacen))
        self.wids['e_total_fabricado'].set_text("%s kg (%d bultos)" % (
            utils.float2str(kilos_fabricados), bultos_fabricados))
        self.colorear(self.wids['tv_balas'])

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
            filas_res.append((r.id, r.codigo, r.nombre, r.descripcion))
        idproducto = utils.dialogo_resultado(filas_res,
                                             titulo = 'Seleccione producto',
                                             cabeceras = ('ID Interno', 
                                                          'Código', 
                                                          'Nombre', 
                                                          'Descripción'), 
                                             padre = self.wids['ventana'])
        if idproducto < 0:
            return None
        else:
            return idproducto

    def buscar_balas(self,wid):
        """
        Pide el código de un producto y busca todos las unidades de ese 
        producto.
        """
        a_buscar = utils.dialogo_entrada(titulo = 'INTRODUZCA DATOS', 
                    texto = 'Introduzca el código, nombre o descripción\n'
                            'del producto que desea listar:', 
                    padre = self.wids['ventana'])
        if a_buscar != None:
            criterio = pclases.OR(
                pclases.ProductoVenta.q.codigo.contains(a_buscar),
                pclases.ProductoVenta.q.nombre.contains(a_buscar),
                pclases.ProductoVenta.q.descripcion.contains(a_buscar))
            criterio = pclases.AND(criterio, 
                pclases.ProductoVenta.q.camposEspecificosBalaID != None)
            resultados = pclases.ProductoVenta.select(criterio)
            if resultados.count() > 1:
                    ## Refinar los resultados
                    idproducto = self.refinar_resultados_busqueda(resultados)
                    if idproducto == None:
                        return
                    resultados = [pclases.ProductoVenta.get(idproducto)]
            elif resultados.count() < 1:
                    ## Sin resultados de búsqueda
                    utils.dialogo_info(titulo = 'ERROR', 
                        texto = 'No hay ningún producto con ese código', 
                        padre = self.wids['ventana'])
                    return
            ## Un único resultado
            # Pongo el objeto como actual
            producto = resultados[0]
            self.producto = producto
            self.wids['e_descripcion'].set_text(producto.descripcion)
            #articulos_bala = [i for i in producto.articulos if i.balaID!=None]
            and_fecha_inicio = "AND fechahora >= '%s'" % (
                self.get_unambiguous_fecha(self.inicio))
            if producto.es_bala():
                articulos_bala = pclases.Articulo.select("""
                    bala_id IS NOT NULL AND producto_venta_id = %d 
                    AND bala_id IN (
                        SELECT id 
                        FROM bala 
                        WHERE fechahora < '%s' %s ) """ 
                    % (producto.id, 
                       self.get_unambiguous_fecha(self.fin+mx.DateTime.oneDay),
                       self.inicio and and_fecha_inicio or ""))
                articulos_bigbag = None
                lista_cajas = None
            elif producto.es_bigbag():
                articulos_bigbag = pclases.Articulo.select("""
                    bigbag_id IS NOT NULL AND producto_venta_id = %d 
                    AND bigbag_id IN (SELECT id 
                                      FROM bigbag 
                                      WHERE fechahora < '%s' %s ) 
                    """ % (producto.id, 
                           self.get_unambiguous_fecha(self.fin 
                                                      + mx.DateTime.oneDay), 
                           self.inicio and and_fecha_inicio or ""))
                articulos_bala = None
                lista_cajas = None
            elif producto.es_bala_cable():
                articulos_bala = pclases.Articulo.select("""
                    bala_cable_id IS NOT NULL AND producto_venta_id = %d 
                    AND bala_cable_id IN (SELECT id 
                                          FROM bala_cable 
                                          WHERE fechahora < '%s' %s ) 
                    """ % (producto.id, 
                           self.get_unambiguous_fecha(
                                self.fin + mx.DateTime.oneDay), 
                           self.inicio and and_fecha_inicio or ""))
                articulos_bigbag = None
                lista_cajas = None
            elif producto.es_bolsa():
                #articulos_bolsas = pclases.Articulo.select("""
                #    bolsa_id IS NOT NULL AND producto_venta_id = %d 
                #    AND bolsa_id IN (
                #        SELECT id 
                #        FROM bolsa 
                #        WHERE fechahora < '%s' %s ) """ 
                #    %(producto.id, 
                #      self.get_unambiguous_fecha(self.fin+mx.DateTime.oneDay),
                #      self.inicio != None and and_fecha_inicio or ""))
                #consulta_cajas = """
                #    id IN (SELECT caja_id 
                #             FROM articulo
                #            WHERE caja_id IS NOT NULL 
                #              AND fechahora < '%s' %s 
                #              AND producto_venta_id = %d 
                #          ) """ % (
                #       self.get_unambiguous_fecha(self.fin+mx.DateTime.oneDay),
                #       self.inicio != None and and_fecha_inicio or "", 
                #       producto.id)
                ## Don't be stupid. OPTIMIZATION!!!
                A = pclases.Articulo
                C = pclases.Caja
                if not self.inicio:
                    consulta_cajas = C.select(pclases.AND(
                        A.q.cajaID == C.q.id, 
                        C.q.fechahora < self.fin + mx.DateTime.oneDay, 
                        A.q.productoVentaID == producto.id))
                else:
                    consulta_cajas = C.select(pclases.AND(
                        A.q.cajaID == C.q.id, 
                        C.q.fechahora < self.fin + mx.DateTime.oneDay, 
                        C.q.fechahora >= self.inicio, 
                        A.q.productoVentaID == producto.id))
                if pclases.DEBUG:
                    print >> sys.stderr, consulta_cajas
                lista_cajas = consulta_cajas
                articulos_bigbag = None
                articulos_bala = None
            self.rellenar_tabla(articulos_bala, articulos_bigbag, 
                                lista_cajas)

    def colorear(self, tv):
        def cell_func(column, cell, model, itr):
            codigo = model[itr][0]
            try:
                cajas_total_and_stock = rexpcajas.findall(codigo)[0][1:-1]
            except IndexError:
                cajas_total = None    # No es palé
                cajas_stock = None
            else:
                cajas_stock,cajas_total = map(int, 
                                              cajas_total_and_stock.split("/"))
            numalbaran = model[itr][4]
            numpartida = model[itr][5]
            claseb = model[itr][7]  # @UnusedVariable
            almacen = model[itr][8]
            if numpartida != '-':
                color = "green"
            elif cajas_stock and cajas_stock < cajas_total:
                color = "orange"
            elif numalbaran != '-' and almacen == "":
                # Los albaranes de transferencia de mercancía no sacan 
                # artículos del almacén, deben aparecer en blanco porque los 
                # productos siguen estando realmente en un almacén, aunque no 
                # sea el principal.
                color = "red"
            elif "Z" in model[itr][0]:
                color = "light blue"
            elif "D" in model[itr][0]:
                color = "LightGray"
            elif model[itr][7]:
                color = "yellow"    # Sólo marca en amarillo las clase B que 
                                    # queden en almacén.
            else:
                color = "white"
            cell.set_property("cell-background", color)

        cols = tv.get_columns()
        for i in range(len(cols)):
            column = cols[i]
            cells = column.get_cell_renderers()
            for cell in cells:
                column.set_cell_data_func(cell,cell_func)

def separar_balas_y_bigbags_from_codigos(codigos):
    """
    Recorre la lista de códigos y busca los objetos Bala [cable] o 
    Bigbag correspondientes, los cuales almacena en dos listas 
    que devuelve.
    Si se encuentra un guión en un código genera un rango de 
    códigos a procesar entre los dos números, ambos incluidos.
    Si un código es incorrecto se ignora.
    Si el código no comienza por ninguna letra, se intentará buscar 
    como bala (anteponiendo una B), y si no se encuentra se buscará 
    como bigbag (anteponiendo una C). Si aún así no se encuentra, se 
    ignora.
    OJO: No se controla que el rango (caso de haberlo) sea demasiado 
    grande. Así que más le vale al usuario no equivocarse tecleando 
    y pasar un rango de 10.000 códigos si no quiere tirarse media vida 
    esperando.
    """
    balas = []
    bigbags = []
    balas_cable = []
    pales = []
    while codigos:
        c = codigos.pop()
        c = c.upper()
        if "-" in c:
            codigo1, codigo2 = c.split("-")
            if codigo1[0].isalpha():
                tipocodigo = codigo1[0]
            elif codigo2[0].isalpha():
                tipocodigo = codigo2[0]
            else:
                tipocodigo = ""
            codigo1 = int("".join([letra 
                                   for letra in codigo1 if letra.isdigit()]))
            codigo2 = int("".join([letra 
                                   for letra in codigo2 if letra.isdigit()]))
            if codigo2 < codigo1:
                codigo1, codigo2 = codigo2, codigo1
            for nuevocodigo in xrange(codigo1, codigo2 + 1):
                codigos.append("%s%03d" % (tipocodigo, nuevocodigo))
        elif c.startswith("B"):
            bala = buscar_bala(c)
            if bala != None:
                balas.append(bala)
        elif c.startswith("C"):
            bigbag = buscar_bigbag(c)
            if bigbag != None:
                bigbags.append(bigbag)
        elif c.startswith("Z"):
            bala_cable = buscar_bala_cable(c)
            if bala_cable != None:
                balas_cable.append(bala_cable)
        elif c.startswith("H"):
            pale = buscar_pale(c)
            if pale != None:
                pales.append(pale)
        else:
            bala = buscar_bala("B%s" % (c)) # Intento buscarlo como bala (es lo más probable).
            if bala != None:
                balas.append(bala)
            else:
                codigos.append("C%s" % (c)) # Lo buscaré en la siguiente iteración como fibra de cemento.
    balas.sort(lambda b1, b2: int(b1.numbala - b2.numbala))
    bigbags.sort(lambda b1, b2: int(b1.numbigbag - b2.numbigbag))
    return balas, bigbags, balas_cable, pales

def buscar_bala(codigo):
    """
    Busca una bala en la BD según el código recibido.
    Devuelve None si no la encuentra.
    Si existiesen varias balas con el mismo código, devuelve 
    la primera de ellas según el orden interno de la BD.
    """
    balas = pclases.Bala.select(pclases.Bala.q.codigo == codigo)
    if balas.count() == 0:
        res = None
    else:
        res = balas[0]
    return res

def buscar_bigbag(codigo):
    """
    Busca una bigbag en la BD según el código recibido.
    Devuelve None si no la encuentra.
    Si existiesen varias bigbags con el mismo código, devuelve 
    la primera de ellas según el orden interno de la BD.
    """
    bigbags = pclases.Bigbag.select(pclases.Bigbag.q.codigo == codigo)
    if bigbags.count() == 0:
        res = None
    else:
        res = bigbags[0]
    return res

def buscar_bala_cable(codigo):
    """
    Busca una bala_cable en la BD según el código recibido.
    Devuelve None si no la encuentra.
    Si existiesen varias bala_cable con el mismo código, devuelve 
    la primera de ellas según el orden interno de la BD.
    """
    balas_cable = pclases.BalaCable.select(pclases.BalaCable.q.codigo == codigo)
    if balas_cable.count() == 0:
        res = None
    else:
        res = balas_cable[0]
    return res

def buscar_pale(codigo):
    """
    Busca una palé en la BD según el código recibido.
    Devuelve None si no la encuentra.
    Si existiesen varias palés con el mismo código, devuelve 
    el primero de ellos según el orden interno de la BD.
    """
    pales = pclases.Pale.select(pclases.Pale.q.codigo == codigo)
    try:
        res = pales[0]
    except IndexError:
        res = None
    return res

def preparar_datos_etiquetas_balas(balas):
    """
    Recibe una lista de objetos bala y devuelve una lista de 
    diccionarios con los datos que lleva una etiqueta de balas.
    """
    etiqs = []
    for bala in balas:
        producto = bala.articulo.productoVenta
        campos = producto.camposEspecificosBala
        datsetiq = {'descripcion': producto.descripcion,
                    'codigo': bala.codigo,
                    'color': str(campos.color),
                    'peso': utils.float2str(bala.pesobala),
                    'lote': bala.lote.codigo,
                    'tipo': campos.tipoMaterialBala and str(campos.tipoMaterialBala.descripcion) or "",
                    'longitud': str(campos.corte),
                    'nbala': str(bala.numbala),
                    'dtex': str(campos.dtex),
                    'dia': utils.str_fecha(bala.fechahora),
                    'acabado': campos.antiuv and "1" or "0",
                    'codigoBarra': producto.codigo}
        etiqs.append(datsetiq)
    return etiqs

def preparar_datos_etiquetas_balas_cable(balas):
    """
    Recibe una lista de objetos bala y devuelve una lista de 
    diccionarios con los datos que lleva una etiqueta de balas.
    """
    data = []
    for bala in balas:
        pv = bala.productoVenta
        ceb = pv.camposEspecificosBala
        quitar_vocales = lambda txt: "".join([c for c in txt if c.upper() not in "AEIOU"])
        if quitar_vocales(ceb.color) not in quitar_vocales(pv.descripcion.upper()) and ceb.color.strip() != "":
            color = pv.descripcion + "; color: " + ceb.color + "."
        else:
            color = pv.descripcion
        b = {'codigoBarra': pv.codigo, 
             'codigo': bala.codigo, 
             'color': color, 
             'peso': utils.float2str(bala.peso, 1)
            }
        data.append(b)
    return data

def abrir_trazabilidad(tv, path, view_col, usuario):
    puid = tv.get_model()[path][-1]
    objeto = pclases.getObjetoPUID(puid)
    from formularios import trazabilidad_articulos
    v = trazabilidad_articulos.TrazabilidadArticulos(usuario = usuario,  # @UnusedVariable
                                                     objeto = objeto)

if __name__ == '__main__':
    t = ListadoBalas()

