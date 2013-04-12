#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
# Copyright (C) 2005-2008  Francisco José Rodríguez Bogado,                   #
#                          (pacoqueen@users.sourceforge.net                   #
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
## certificado_calidad.glade 
###################################################################
##  
###################################################################
## Changelog:
## 1 de octubre de 2009 -> Inicio 
## 
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
from framework.seeker import VentanaGenerica 
from formularios.trazabilidad_articulos import escribir as txt_write, \
                                               borrar_texto as txt_clear

class CertificadoCalidad(Ventana, VentanaGenerica):
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        self.usuario = usuario
        self.objeto = objeto
        Ventana.__init__(self, 'certificado_calidad.glade', self.objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir, 
                       'b_csv/clicked': self.exportar, 
                      }  
        self.add_connections(connections)
        self.inicializar_ventana()
        if self.objeto:
            self.actualizar_ventana()
        gtk.main()

    def actualizar_ventana(self):
        """
        Enmascara el de la clase padre Ventana.
        """
        if self.objeto:
            self.rellenar_widgets()

    def inicializar_ventana(self):
        """
        Inicializa los controles de la ventana, estableciendo sus
        valores por defecto, deshabilitando los innecesarios,
        rellenando los combos, formateando el TreeView -si lo hay-...
        """
        self.wids['b_buscar'].set_sensitive(True)
        cols = (('Característica', 'gobject.TYPE_STRING', 
                    False, True, True, lambda *a, **kw: None),
                ('Valor medio', 'gobject.TYPE_STRING', 
                    False, True, False, lambda *a, **kw: None),
                ('Valor referencia', 'gobject.TYPE_STRING', 
                    False, True, False, lambda *a, **kw: None),
                ('Valor impresión', 'gobject.TYPE_STRING', 
                    False, True, False, lambda *a, **kw: None),
                ('ID', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_treeview(self.wids['tv_datos'], cols)
        tv = self.wids['tv_datos']
        tv.get_column(1).get_cell_renderers()[0].set_property('xalign', 1.0) 
        tv.get_column(2).get_cell_renderers()[0].set_property('xalign', 1.0) 
        tv.get_column(3).get_cell_renderers()[0].set_property('xalign', 1.0) 

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
            if r.almacenDestino:
                destino = r.almacenDestino.nombre
            elif r.destino != None:
                destino = r.destino.get_info()
            elif r.nombre:
                destino = ", ".join((r.nombre, r.direccion, r.cp, r.ciudad, 
                                     r.pais))
            else:
                destino = ""
            filas_res.append((r.id, 
                              r.numalbaran, 
                              r.fecha and r.fecha.strftime('%d/%m/%Y') or '', 
                              r.almacenOrigen.nombre, 
                              r.clienteID and r.cliente.nombre or "", 
                              destino))
        idalbaran = utils.dialogo_resultado(filas_res,
                        titulo = 'Seleccione albarán',
                        cabeceras = ('ID Interno', 
                                     'Número de albarán', 
                                     'Fecha', 
                                     'Origen', 
                                     'Cliente', 
                                     'Destino'), 
                        padre = self.wids['ventana']) 
        if idalbaran < 0:
            return None
        else:
            return idalbaran

    def rellenar_widgets(self):
        """
        Introduce la información del objeto actual
        en los widgets.
        No se chequea que sea != None, así que
        hay que tener cuidado de no llamar a 
        esta función en ese caso.
        """
        if self.objeto:
            self.wids['e_numalbaran'].set_text(self.objeto.numalbaran)
        referencias = {}    # Valores de referencia por producto.
        ## TODO: Refactorizar esto para sacar los cálculos de la capa vista.
        ##       Se debe poder calcular los valores de impresión desde 
        ##       cualquier parte de la aplicación sin tener que abrir esta 
        ##       ventana.
        # Rescato lotes y partidas.
        productos = {}
        for articulo in self.objeto.articulos:
            producto = articulo.productoVenta
            for atributo in ("lote", "loteCem", "partida", "partidaCem"):
                lote_o_partida = getattr(articulo, atributo)
                try:
                    if (lote_o_partida 
                        and lote_o_partida not in productos[producto]):
                        productos[producto].append(lote_o_partida)
                except KeyError:
                    productos[producto] = [lote_o_partida]
            # Valores de referencia.
            if producto.camposEspecificosRolloID:
                try:
                    fpar = articulo.partida.get_fecha_fabricacion()
                    cer = producto.camposEspecificosRollo.buscar_marcado(fpar)
                    if cer == None:
                        raise ValueError
                except (AttributeError, ValueError):
                    cer = producto.camposEspecificosRollo
                referencias[producto] = {
                    "Resistencia longitudinal": 
                        [cer.valorPruebaLongitudinalInf, 
                         cer.estandarPruebaLongitudinal, 
                         cer.valorPruebaLongitudinalSup],
                    "Alargamiento longitudinal": 
                        [cer.valorPruebaAlargamientoLongitudinalInf, 
                         cer.estandarPruebaAlargamientoLongitudinal, 
                         cer.valorPruebaAlargamientoLongitudinalSup], 
                    "Resistencia transversal": 
                        [cer.valorPruebaTransversalInf, 
                         cer.estandarPruebaTransversal, 
                         cer.valorPruebaTransversalSup], 
                    "Alargamiento transversal": 
                        [cer.valorPruebaAlargamientoTransversalInf, 
                         cer.estandarPruebaAlargamientoTransversal, 
                         cer.valorPruebaAlargamientoTransversalSup], 
                    "Resistencia a la compresión": 
                        [cer.valorPruebaCompresionInf, 
                         cer.estandarPruebaCompresion, 
                         cer.valorPruebaCompresionSup], 
                    "Perforación": 
                        [cer.valorPruebaPerforacionInf, 
                         cer.estandarPruebaPerforacion, 
                         cer.valorPruebaPerforacionSup], 
                    "Espesor": 
                        [cer.valorPruebaEspesorInf, 
                         cer.estandarPruebaEspesor,  
                         cer.valorPruebaEspesorSup], 
                    "Permeabilidad": 
                        [cer.valorPruebaPermeabilidadInf, 
                         cer.estandarPruebaPermeabilidad, 
                         cer.valorPruebaPermeabilidadSup], 
                    "Apertura de poros": 
                        [cer.valorPruebaPorosInf, 
                         cer.estandarPruebaPoros, 
                         cer.valorPruebaPorosSup], 
                    "Gramaje": 
                        [cer.valorPruebaGramajeInf, 
                         cer.estandarPruebaGramaje, 
                         cer.valorPruebaGramajeSup], 
                    "Punzonado piramidal": 
                        [cer.valorPruebaPiramidalInf, 
                         cer.estandarPruebaPiramidal, 
                         cer.valorPruebaPiramidalSup]} 
            elif producto.camposEspecificosBalaID:
                ceb = producto.camposEspecificosBala
                referencias[producto] = {
                    "Media título": [ceb.dtex, 
                                     ceb.dtex, 
                                     ceb.dtex]}     # Es el único valor que se 
                                                    # puede comparar.
        # Calculo medias.
        valores = {}
        for p in productos:
            valores[p] = {}
            for lote_o_partida in productos[p]:
                if isinstance(lote_o_partida, pclases.Lote):
                    descripciones_campo = (("Tenacidad", "tenacidad"), 
                                           ("Elongación", "elongacion"), 
                                           ("Encogimiento", "encogimiento"),
                                           ("% Grasa", "grasa"), 
                                           ("Media título", "mediatitulo"))
                elif isinstance(lote_o_partida, pclases.LoteCem):
                    descripciones_campo = (("Tenacidad", "tenacidad"), 
                                           ("Elongación", "elongacion"), 
                                           ("Encogimiento", "encogimiento"),
                                           ("% Grasa", "grasa"), 
                                           ("% Humedad", "humedad"), 
                                           ("Media título", "mediatitulo"))
                elif isinstance(lote_o_partida, pclases.Partida):
                    descripciones_campo = (("Gramaje", "gramaje"), 
                                ("Resistencia longitudinal", "longitudinal"), 
                                ("Alargamiento longitudinal", "alongitudinal"), 
                                ("Resistencia transversal", "transversal"), 
                                ("Alargamiento transversal", "atransversal"), 
                                ("Resistencia a la compresión", "compresion"), 
                                ("Perforación", "perforacion"), 
                                ("Espesor", "espesor"), 
                                ("Permeabilidad", "permeabilidad"), 
                                ("Apertura de poros", "poros"), 
                                ("Punzonado piramidal", "piramidal")) 
                elif isinstance(lote_o_partida, pclases.PartidaCem):
                    descripciones_campo = []
                for descripcion, campo in descripciones_campo:
                    valor = getattr(lote_o_partida, campo)
                    if valor is None or not lote_o_partida.esta_analizada():
                        # DONE: En teoría si no está analizada debería buscar 
                        # la partida anterior o posterior del mismo producto 
                        # que estuviera analizada (jmadrid). 
                        # Al final no. Me ha enviado otro correo con el nuevo 
                        # criterio para la impresión de valores nulos.
                        continue    # Ignoro valores nulos.
                    try:
                        valores[p][descripcion].append(valor)
                    except KeyError:
                        valores[p][descripcion] = [valor]
        # Y ahora sustituyo la lista de valores por su media:
        for p in valores:
            for campo in valores[p]:
                valores[p][campo] = utils.media(valores[p][campo])
        self.rellenar_tabla_datos(valores, referencias)
        self.rellenar_info_albaran(productos)
        self.wids['tv_datos'].expand_all()

    def rellenar_info_albaran(self, lotes_o_partidas):
        """
        Escribe información básica del albarán en el TextView, así cómo el 
        listado de lotes y partidas.
        """
        txt = self.wids['txt_albaran'] 
        txt_clear(txt)
        if self.objeto:
            alb = self.objeto
            txt_write(txt, alb.get_info(), ("negrita", "grande"))
            txt_write(txt, "\nContenido del albarán:\n")
            for ldv in alb.lineasDeVenta:
                strldv = "\t%s %s de %s\n" % (
                            utils.float2str(ldv.cantidad, autodec = True), 
                            ldv.producto.unidad, 
                            ldv.producto.descripcion)
                txt_write(txt, strldv)
                if ldv.producto in lotes_o_partidas:
                    for lote_o_partida in lotes_o_partidas[ldv.producto]:
                        txt_write(txt, "\t\t%s\n" % lote_o_partida.codigo, 
                                  ("cursiva", ))

    def rellenar_tabla_datos(self, productos, referencias):
        """
        Recibe los valores en forma de tupla de tuplas (característica, valor).
        """
        model = self.wids['tv_datos'].get_model()
        model.clear()
        for producto in productos:
            valores = productos[producto]
            padre = model.append(None, 
                                 (producto.descripcion, 
                                  "", 
                                  "", 
                                  "", 
                                  producto.get_puid()))
            for caracteristica in valores:
                try:
                    referencia = referencias[producto][caracteristica][1]
                except KeyError:
                    str_referencia = ""
                else:
                    str_referencia = utils.float2str(referencia, 4)
                valor_impresion = valor_medio = valores[caracteristica]
                # CWT:(jmadrid)Si sale cero, poner el mínimo de estas pruebas:
                if caracteristica == "Permeabilidad":
                    if round(valor_medio, 0) == 0:
                        valor_impresion = \
                            referencias[producto][caracteristica][0]
                elif caracteristica == "Apertura de poros":
                    if round(valor_medio, 0) == 0:
                        valor_impresion = \
                            referencias[producto][caracteristica][0]
                elif caracteristica == "Punzonado piramidal":
                    if round(valor_medio, 0) == 0:
                        valor_impresion = \
                            referencias[producto][caracteristica][0]
                elif caracteristica == "Espesor":
                    if round(valor_medio, 0) == 0:
                        valor_impresion = \
                            referencias[producto][caracteristica][1]
                elif caracteristica == "Perforación":
                    if round(valor_medio, 0) == 0:
                        valor_impresion = \
                            referencias[producto][caracteristica][1]
                else:
                    # CWT: (jmadrid) Si los valores medio están por debajo o 
                    # por encima, que ponga el mínimo o el máximo del marcado 
                    # CE. Esto es un poco engañifa, ¿no?
                    inferior = referencias[producto][caracteristica][0]
                    superior = referencias[producto][caracteristica][2]
                    optimo = referencias[producto][caracteristica][1]
                    if inferior <= optimo <= superior:
                        if valor_impresion > superior:
                            valor_impresion = superior
                        elif valor_impresion < inferior:
                            valor_impresion = inferior
                    elif optimo <= inferior <= superior:
                        if valor_impresion > superior:
                            valor_impresion = superior
                    elif inferior <= superior <= optimo:
                        if valor_impresion < inferior:
                            valor_impresion = inferior
                try:
                    str_impresion = utils.float2str(valor_impresion, 4, 
                                                    autodec = True)
                except (ValueError, TypeError):
                    str_impresion = ""
                model.append(padre, (caracteristica, 
                                     utils.float2str(valor_medio, 4), 
                                     str_referencia, 
                                     str_impresion, 
                                     ""))
    
    def buscar(self, widget):
        """
        Muestra una ventana de búsqueda y a continuación los
        resultados. El objeto seleccionado se hará activo
        en la ventana a no ser que se pulse en Cancelar en
        la ventana de resultados.
        """
        a_buscar = self.wids['e_numalbaran'].get_text()
        if a_buscar != None:
            try:
                ida_buscar = int(a_buscar)
            except ValueError:
                ida_buscar = -1
            criterio = pclases.OR(
                pclases.AlbaranSalida.q.numalbaran.contains(a_buscar),
                pclases.AlbaranSalida.q.id == ida_buscar)
            resultados = pclases.AlbaranSalida.select(criterio)
            if resultados.count() > 1:
                ## Refinar los resultados
                ide = self.refinar_resultados_busqueda(resultados)
                if ide == None:
                    return
                resultados = [pclases.AlbaranSalida.get(ide)]
            elif resultados.count() < 1:
                ## Sin resultados de búsqueda
                utils.dialogo_info('SIN RESULTADOS', 
                    texto = "La búsqueda no produjo resultados.\n"
                            "Pruebe a cambiar el texto buscado o déjelo en "
                            "blanco para ver una lista completa.\n"
                            "(Atención: Ver la lista completa puede resultar"
                            " lento si el número de elementos es muy alto)",
                    padre = self.wids['ventana'])
                return
            ## Un único resultado
            try:
                self.objeto = resultados[0]
            except IndexError:
                utils.dialogo_info(titulo = "ERROR", 
                    texto = "Se produjo un error al recuperar la información"
                            ".\nCierre y vuelva a abrir la ventana antes de "
                            "volver a intentarlo.", 
                    padre = self.wids['texto'])
                return
        self.actualizar_ventana()

    def imprimir(self, boton):
        # OJO: Como no hay catálogo de pruebas en la base de datos, las 
        # unidades, métodos y descripciones de las pruebas sobre geotextiles 
        # están HARCODED aquí.
        # PLAN: Meter todo esto en el tablas.sql, como debe de ser.
        data_prueba = {
            "Resistencia longitudinal": 
                {"descripción": "Resistencia a la tracción DM", 
                 "método": "EN ISO 10319", 
                 "unidad": "kN/m"}, 
            "Resistencia transversal":  
                {"descripción": "Resistencia a la tracción DT", 
                 "método": "EN ISO 10319", 
                 "unidad": "kN/m"}, 
            "Alargamiento longitudinal":  
                {"descripción": "Alargamiento DM", 
                 "método": "EN ISO 10319", 
                 "unidad": "%"}, 
            "Alargamiento transversal":  
                {"descripción": "Alargamiento DT", 
                 "método": "EN ISO 10319", 
                 "unidad": "%"}, 
            "Perforación":  
                {"descripción": 
                    "Resistencia a la perforación dinámica (Caída de cono)", 
                 "método": "EN ISO 13433", 
                 "unidad": "mm"}, 
            "Resistencia a la compresión":  
                {"descripción": 
                    "Resistencia al punzonado estático (CBR a perforación)", 
                 "método": "EN ISO 12236", 
                 "unidad": "kN"}, 
            "Apertura de poros":  
                {"descripción": "Medida de apertura (Porometría 090)", 
                 "método": "EN ISO 12956", 
                 "unidad": "mm"}, 
            "Punzonado piramidal":  
                {"descripción": "Resistencia al punzonado piramidal", 
                 "método": "NF G38-019", 
                 "unidad": "kN"}, 
            "Permeabilidad":  
                {"descripción": "Permeabilidad perpendicular al agua", 
                 "método": "EN ISO 11058", 
                 "unidad": "l/m²/s"}, 
            "Gramaje":  
                {"descripción": "Gramaje", 
                 "método": "EN ISO 9864", 
                 "unidad": "g/m²"}, 
            "Espesor": 
                {"descripción": "Espesor bajo 2 kPa", 
                 "método": "EN ISO 9863-1", 
                 "unidad": "mm"}
            }
        if not self.objeto:
            return
        #tv = self.wids['tv_datos']
        #from informes.treeview2pdf import treeview2pdf
        from formularios.reports import abrir_pdf
        #strfecha = "%s - %s" % (utils.str_fecha(mx.DateTime.localtime()), 
        #                        utils.str_hora(mx.DateTime.localtime()))
        #abrir_pdf(treeview2pdf(tv, 
        #    titulo = "Certificado de calidad de albarán %s" % (
        #        self.objeto.numalbaran),
        #    fecha = strfecha, 
        #    apaisado = False))
        from informes import informe_certificado_calidad
        from informes.geninformes import give_me_the_name_baby
        from time import sleep
        dic_productos = {}
        model = self.wids['tv_datos'].get_model()
        for fila in model:
            producto = pclases.getObjetoPUID(fila[-1])
            dic_productos[producto] = {}
            for hijo in fila.iterchildren():
                caracteristica = hijo[0]
                valor = hijo[-2]
                dic_productos[producto][caracteristica] = {
                    "descripción": data_prueba[caracteristica]["descripción"], 
                    "método": data_prueba[caracteristica]["método"], 
                    "unidad": data_prueba[caracteristica]["unidad"], 
                    "valor": valor}
        for producto in dic_productos:
            dic_valores = dic_productos[producto]
            if producto.es_rollo():
                orden = ("Resistencia longitudinal", 
                         "Resistencia transversal", 
                         "Alargamiento longitudinal", 
                         "Alargamiento transversal", 
                         "Perforación", 
                         "Resistencia a la compresión", 
                         "Apertura de poros", 
                         "Permeabilidad", 
                         "Gramaje", 
                         "Espesor", 
                         "Punzonado piramidal")
            nomfich = informe_certificado_calidad.go(
                "certcalidad_%s.pdf" % give_me_the_name_baby(), 
                producto, 
                dic_valores, 
                pclases.DatosDeLaEmpresa.select()[0], 
                self.objeto, 
                orden = orden)
            sleep(1)
            abrir_pdf(nomfich)

    def exportar(self, boton):
        if not self.objeto:
            return
        tv = self.wids['tv_datos']
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        nomarchivocsv = treeview2csv(tv)
        abrir_csv(nomarchivocsv)


    

if __name__ == "__main__":
    p = CertificadoCalidad()

