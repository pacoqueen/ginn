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
## consulta_mensual_nominas.py -- 
###################################################################

from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, time
from framework import pclases
import mx.DateTime
from formularios import ventana_progreso
    
LINEASPRODUCCION = pclases.LineaDeProduccion.select(orderBy = "id")
#RESTOCENTROS = ("Almacén", "Varios")
RESTOCENTROS = pclases.ControlHoras.RESTOCENTROS
RESTOCENTROS_Y_TOTAL = tuple(list(RESTOCENTROS) + ["Total"])

class ConsultaMensualNominas(Ventana):
    def __init__(self, objeto = None, usuario = None):
        self.usuario = usuario
        Ventana.__init__(self, 
                         'consulta_mensual_nominas.glade', 
                         objeto, 
                         usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       "b_exportar/clicked": self.exportar}
        self.add_connections(connections)
        # ListViews de pluses. Sólo empleados de control_horas.
        cols = (('Empleado', 'gobject.TYPE_STRING', False, True, True, None),
                ('Categoría laboral', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Plus jefe de turno', 
                    'gobject.TYPE_STRING', False, True, False, None),
                ('Plus no absentismo', 'gobject.TYPE_STRING', True, True, 
                    False, self.cambiar_absentismo),
                #('Klaatu barada nikto', 'gobject.TYPE_STRING', True, True, 
                ('Concepto libre', 'gobject.TYPE_STRING', True, True, 
                    False, self.cambiar_importe_libre), 
                ('Plus festivos', 
                    'gobject.TYPE_STRING', False, True, False, None),
                ('Plus turnicidad', 
                    'gobject.TYPE_STRING', False, True, False, None),
                ('Plus mantenimiento sábados', 
                    'gobject.TYPE_STRING', False, True, False, None),
                ('Horas extras', 
                    'gobject.TYPE_STRING', False, True, False, None),
                ('Plus nocturnidad', 
                    'gobject.TYPE_STRING', False, True, False, None),
                ('IDEmpleado', 'gobject.TYPE_STRING', False,False,False,None))
        utils.preparar_listview(self.wids['tv_plus'], cols)
        for col in range(2, 10):
            columna = self.wids['tv_plus'].get_column(col)
            for cell in columna.get_cell_renderers():
                cell.set_property("xalign", 1)
        cols = cols[2:]
        utils.preparar_listview(self.wids['tv_totales_plus'], cols)
        for col in range(0, 8):
            columna = self.wids['tv_totales_plus'].get_column(col)
            for cell in columna.get_cell_renderers():
                cell.set_property("xalign", 1)
        col = self.wids['tv_totales_plus'].get_column(2)
        col.connect("clicked", self.cambiar_concepto_libre)
        # ListViews de resúmenes. Todos excepto los de baja en la empresa.
        cols = [('Empleado', 'gobject.TYPE_STRING', False, True, True, None),
                ('Categoría\nlaboral', 'gobject.TYPE_STRING', 
                    False, True, False, None),
                ('Centro de\ntrabajo', 'gobject.TYPE_STRING', # Según cat. lab.
                    False, True, False, None)]
        for linea in LINEASPRODUCCION:
            cols.append(("%s\nHH. labs." % linea.nombre, 
                         'gobject.TYPE_STRING', False, True, False, None))
            cols.append(("%s\nHH. extras" % linea.nombre, 
                         'gobject.TYPE_STRING', False, True, False, None))
            cols.append(("%s\nNoct." % linea.nombre, 
                         'gobject.TYPE_STRING', False, True, False, None))
            cols.append(("%s\nMant. sábado" % linea.nombre, 
                         'gobject.TYPE_STRING', False, True, False, None))
            cols.append(("%s\nMant." % linea.nombre, 
                         'gobject.TYPE_STRING', False, True, False, None))
        for nombre in RESTOCENTROS_Y_TOTAL:
            cols.append(("%s\nHH. labs." % nombre, 
                         'gobject.TYPE_STRING', False, True, False, None))
            cols.append(("%s\nHH. extras" % nombre, 
                         'gobject.TYPE_STRING', False, True, False, None))
            cols.append(("%s\nNoct." % nombre, 
                         'gobject.TYPE_STRING', False, True, False, None))
            cols.append(("%s\nMant." % nombre, 
                         'gobject.TYPE_STRING', False, True, False, None))
        cols.append(('Coste hh. labs.', 
                     'gobject.TYPE_STRING', False, True, False, None))
        cols.append(('Coste hh. extras', 
                     'gobject.TYPE_STRING', False, True, False, None))
        cols.append(('Coste nocturnidad', 
                     'gobject.TYPE_STRING', False, True, False, None))
        cols.append(('Coste trabajador', 
                     'gobject.TYPE_STRING', False, True, False, None))
        cols.append(('IDEmpleado', 
                     'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(self.wids['tv_resumen'], cols)
        for col in range(3, len(cols)-1):
            columna = self.wids['tv_resumen'].get_column(col)
            for cell in columna.get_cell_renderers():
                cell.set_property("xalign", 1)
        cols = cols[3:]
        utils.preparar_listview(self.wids['tv_totales_resumen'], cols)
        for col in range(0, len(cols)-1):
            columna = self.wids['tv_totales_resumen'].get_column(col)
            for cell in columna.get_cell_renderers():
                cell.set_property("xalign", 1)
        # No puedo dejar que reordene columnas o me joderá la exportación a PDF
        #for tv in ("tv_plus", "tv_totales_plus", 
        #           "tv_resumen", "tv_totales_resumen"):
        #    for col in self.wids[tv].get_columns():
        #        col.set_reorderable(False)
        # Fechas iniciales de la ventana:
        temp = time.localtime()  # @UnusedVariable
        self.inicio = mx.DateTime.localtime() - (7*mx.DateTime.oneDay)
        self.fin = mx.DateTime.localtime()
        self.wids['e_fechafin'].set_text(utils.str_fecha(self.fin))
        self.wids['e_fechainicio'].set_text(utils.str_fecha(self.inicio))
        gtk.main()

    def cambiar_concepto_libre(self, col):
        concepto = utils.dialogo_entrada(titulo = "CONCEPTO", 
                    texto = "Introduzca el concepto libre", 
                    valor_por_defecto = col.get_title(), 
                    padre = self.wids['ventana'])
        if concepto != None:
            CH = pclases.ControlHoras
            chs = CH.select(pclases.AND(CH.q.fecha >= self.inicio, 
                                        CH.q.fecha <= self.fin))
            for ch in chs:
                ch.conceptoLibre = concepto
            col.set_title(concepto)
            self.wids['tv_plus'].get_column(4).set_title(concepto)

    def chequear_cambios(self):
        pass

    def cambiar_absentismo(self, cell, path, texto):
        """
        Guarda el plus de no absentismo del empleado en un registro de 
        control de horas dentro del rango de fechas de la consulta.
        La fecha elegida para guardar el plus es la fecha intermedia entre 
        los dos extremos, así aparecerá el plus de no absentismo en el mes 
        que sea aunque las fechas inicial y final varíen ligeramente.
        El truco para no tener que buscar el registro elegido en dos consultas 
        ligeramente distintas y así que al cambiar un 100 por 120 no se 
        convierta mágicamente en 220 (100 en un registro y 120 en otro) es 
        guardar siempre la diferencia entre el texto escrito y el nuevo.
        PLAN: Se podría tratar de usar el campo de nóminas dedicado a este 
        plus, pero se intenta mantener todo lo independiente posible esas 
        tablas, ya que probablemente la ventana de nóminas será DEPRECATED 
        para la siguiente versión. De cualquier forma, siempre se podría 
        tratar de actualizar los valores de la nómina desde esta ventana. 
        También hay que tener en cuenta que las nóminas son para meses 
        completos, mientras que esta consulta está enfocada a granularidad 
        que va desde un solo día a años enteros.
        """
        try:
            pabs = utils._float(texto)
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", 
                texto = "El texto tecleado %s no es un número." % texto, 
                padre = self.wids['ventana'])
            return
        model = self.wids['tv_plus'].get_model()
        ide = model[path][-1]
        if not isinstance(ide, int):
            try:
                ide = int(utils._float(ide))
            except:
                txt = ("Identificador %s no se pudo convertir a entero. An" + 
                       "ulo edición de absentismo" % ide)
                self.logger.error("%consulta_mensual_nominas.py::cambiar_absentismo -> %s" % (self.usuario and self.usuario.usuario + ": " or "", txt))
                return
        empleado = pclases.Empleado.get(ide)
        f1 = self.inicio
        f2 = self.fin
        fecha = mx.DateTime.DateTimeFromTicks((f1.ticks() + f2.ticks()) / 2)
        # Por si acaso, aseguro día, mes y año redondos, sin hora.
        fecha = mx.DateTime.DateTimeFrom(day = fecha.day, 
                                         month = fecha.month, 
                                         year = fecha.year)
        valor_anterior = utils._float(model[path][3])
        a_guardar = pabs - valor_anterior
        try:
            ch = pclases.ControlHoras.select(pclases.AND(
                    pclases.ControlHoras.q.empleadoID == empleado.id, 
                    pclases.ControlHoras.q.fecha == fecha))[0]
        except IndexError:  # Es posible que no haya registro en esa fecha.
            ch = pclases.ControlHoras(fecha = fecha, 
                                      empleado = empleado, 
                                      grupo = None, 
                                      horasRegulares = 0.0, 
                                      nocturnidad = False,
                                      horasExtraDiaProduccion = 0.0, 
                                      horasExtraDiaMantenimiento = 0.0, 
                                      horasExtraDiaAlmacen = 0.0, 
                                      horasExtraDiaVarios = 0.0, 
                                      horasExtraNocheProduccion = 0.0, 
                                      horasExtraNocheMantenimiento = 0.0, 
                                      horasExtraNocheAlmacen = 0.0, 
                                      horasExtraNocheVarios = 0.0, 
                                      horasAlmacen = 0.0, 
                                      horasVarios = 0.0, 
                                      varios = '', 
                                      comentarios = '', 
                                      bajaLaboral = False, 
                                      vacacionesYAsuntosPropios = False, 
                                      festivo = False, 
                                      plusAbsentismo = 0.0)
            pclases.Auditoria.nuevo(ch, self.usuario, __file__)
        ch.plusAbsentismo += a_guardar  # Por si era el mismo, sumo.
        ch.syncUpdate()
        model[path][3] = utils.float2str(
            empleado.calcular_plus_no_absentismo(self.inicio, 
                                                 self.fin))
        total = sum([utils._float(model[p][3]) for p in range(len(model))])
        self.wids['tv_totales_plus'].get_model()[0][1] = utils.float2str(total)

    def cambiar_importe_libre(self, cell, path, texto):
        """
        Guarda el plus de no absentismo del empleado en un registro de 
        control de horas dentro del rango de fechas de la consulta.
        La fecha elegida para guardar el plus es la fecha intermedia entre 
        los dos extremos, así aparecerá el plus de no absentismo en el mes 
        que sea aunque las fechas inicial y final varíen ligeramente.
        El truco para no tener que buscar el registro elegido en dos consultas 
        ligeramente distintas y así que al cambiar un 100 por 120 no se 
        convierta mágicamente en 220 (100 en un registro y 120 en otro) es 
        guardar siempre la diferencia entre el texto escrito y el nuevo.
        PLAN: Se podría tratar de usar el campo de nóminas dedicado a este 
        plus, pero se intenta mantener todo lo independiente posible esas 
        tablas, ya que probablemente la ventana de nóminas será DEPRECATED 
        para la siguiente versión. De cualquier forma, siempre se podría 
        tratar de actualizar los valores de la nómina desde esta ventana. 
        También hay que tener en cuenta que las nóminas son para meses 
        completos, mientras que esta consulta está enfocada a granularidad 
        que va desde un solo día a años enteros.
        """
        try:
            pabs = utils._float(texto)
        except:
            utils.dialogo_info(titulo = "ERROR DE FORMATO", 
                texto = "El texto tecleado %s no es un número." % texto, 
                padre = self.wids['ventana'])
            return
        model = self.wids['tv_plus'].get_model()
        ide = model[path][-1]
        if not isinstance(ide, int):
            try:
                ide = int(utils._float(ide))
            except:
                txt = ("Identificador %s no se pudo convertir a entero. An" + 
                       "ulo edición de importe libre" % ide)
                self.logger.error("%consulta_mensual_nominas.py::cambiar_importe_libre -> %s" % (self.usuario and self.usuario.usuario + ": " or "", txt))
                return
        empleado = pclases.Empleado.get(ide)
        f1 = self.inicio
        f2 = self.fin
        fecha = mx.DateTime.DateTimeFromTicks((f1.ticks() + f2.ticks()) / 2)
        # Por si acaso, aseguro día, mes y año redondos, sin hora.
        fecha = mx.DateTime.DateTimeFrom(day = fecha.day, 
                                         month = fecha.month, 
                                         year = fecha.year)
        valor_anterior = utils._float(model[path][4])
        a_guardar = pabs - valor_anterior
        try:
            ch = pclases.ControlHoras.select(pclases.AND(
                    pclases.ControlHoras.q.empleadoID == empleado.id, 
                    pclases.ControlHoras.q.fecha == fecha))[0]
        except IndexError:  # Es posible que no haya registro en esa fecha.
            ch = pclases.ControlHoras(fecha = fecha, 
                                      empleado = empleado, 
                                      grupo = None, 
                                      horasRegulares = 0.0, 
                                      nocturnidad = False,
                                      horasExtraDiaProduccion = 0.0, 
                                      horasExtraDiaMantenimiento = 0.0, 
                                      horasExtraDiaAlmacen = 0.0, 
                                      horasExtraDiaVarios = 0.0, 
                                      horasExtraNocheProduccion = 0.0, 
                                      horasExtraNocheMantenimiento = 0.0, 
                                      horasExtraNocheAlmacen = 0.0, 
                                      horasExtraNocheVarios = 0.0, 
                                      horasAlmacen = 0.0, 
                                      horasVarios = 0.0, 
                                      varios = '', 
                                      comentarios = '', 
                                      bajaLaboral = False, 
                                      vacacionesYAsuntosPropios = False, 
                                      festivo = False, 
                                      plusAbsentismo = 0.0, 
                                      conceptoLibre = "", 
                                      importeLibre = 0.0)
            pclases.Auditoria.nuevo(ch, self.usuario, __file__)
        ch.importeLibre += a_guardar  # Por si era el mismo, sumo.
        ch.syncUpdate()
        model[path][4] = utils.float2str(
            empleado.calcular_importe_libre(self.inicio, 
                                            self.fin))
        total = sum([utils._float(model[p][4]) for p in range(len(model))])
        self.wids['tv_totales_plus'].get_model()[0][2] = utils.float2str(total)

    def set_inicio(self, boton):
        temp = utils.mostrar_calendario(
            fecha_defecto = utils.parse_fecha(
                self.wids['e_fechainicio'].get_text()), 
            padre = self.wids['ventana'])
        self.inicio = mx.DateTime.DateTimeFrom(*temp[::-1])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(self.inicio))

    def set_fin(self, boton):
        temp = utils.mostrar_calendario(
            fecha_defecto = utils.parse_fecha(
                self.wids["e_fechafin"].get_text()), 
            padre = self.wids['ventana'])
        self.fin = mx.DateTime.DateTimeFrom(*temp[::-1])
        self.wids['e_fechafin'].set_text(utils.str_fecha(self.fin))

    def rellenar_tabla(self, res_plus, res_resumen):
        for res, nombrew, nombrewtot in (
                (res_plus, "tv_plus", "tv_totales_plus"), 
                (res_resumen, "tv_resumen", "tv_totales_resumen")):
            totales = rellenar_subtabla(res, self.wids[nombrew])
            rellenar_subtabla(totales, self.wids[nombrewtot])

    def buscar(self, boton):
        """
        Busca los registros de control de horas entre las fechas del 
        formulario y organiza los resultados de horas, valor monetario, etc. 
        en una lista de listas con los pluses por un lado y el resumen de 
        la nómina por otro.
        """
        CH = pclases.ControlHoras
        chs = CH.select(pclases.AND(CH.q.fecha >= self.inicio, 
                                    CH.q.fecha <= self.fin))
        # OJO: Cálculo de meses aproximado, pero válido para los 
        # casos que manejamos (se necesitaría una consulta de 5 ó 6 años 
        # para un error de 1 mes, más o menos).
        # meses = ((self.fin - self.inicio).day / 30) + 1
        # CWT: Cambio en el cálculo de meses. De 0 a 59 días debe contar como 
        # un solo mes. Las consultas normalmente se harán del veintitantos de 
        # un mes al veintipocos del siguente. No siempre va a transcurrir un 
        # mes de 30 días completo. Por otro lado, a veces entrarán hasta 35 ó 
        # 40 días, y eso también debe contar como un único mes para los pluses 
        # de la nómina. Por tanto:
        meses = self.fin.month - self.inicio.month
        meses += (self.fin.year - self.inicio.year) * 12
        if meses == 0:
            meses = 1
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        tot = chs.count()
        i = 0.0
        vpro.mostrar()
        # OJO: Comienzo sin empleados porque en los registros de control de 
        # personal YA están todos los empleados con alta ese día. Así que 
        # aparecerán aquí aunque no tengan ningún concepto que pagarle, y 
        # no aparecerán aquellos que no trabajaran para la empresa en las 
        # fechas consultadas; que es justamente lo deseable.
        empleados = {}
        for ch in chs:
            vpro.set_valor(i/tot, 'Analizando partes de control...')
            analizar_ch(ch, empleados)
            i += 1
        concepto = CH.get_concepto_libre(self.inicio, self.fin)
        self.wids['tv_plus'].get_column(4).set_title(concepto)
        self.wids['tv_totales_plus'].get_column(2).set_title(concepto)
        for e in empleados:
            empleados[e]["meses"] = meses
        vpro.ocultar()
        res_plus, res_resumen = convertir_a_filas(empleados, 
                                                  padre = self.wids['ventana'])
        # Empleados de oficina para la tabla resumen
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        eoficinas = pclases.Empleado.select(pclases.AND(
            pclases.Empleado.q.planta == False, 
            pclases.Empleado.q.activo == True))
        # TODO: OJO: Si se da de baja un empleado de oficina ya no se podrán 
        # consultar las nóminas antiguas. Esto tengo que apañarlo de alguna 
        # manera, porque no es frecuente, pero se puede dar el caso.
        tot = eoficinas.count()
        i = 0.0
        for e in eoficinas:
            if e.id in [f[-1] for f in res_resumen]:
                # Ya lo he contado porque a pesar de no trabajar en planta, 
                # tiene horas de trabajo asignadas, así que no le vuelvo a 
                # sumar el salario, que es el único concepto que se le paga 
                # al personal indirecto.
                i += 1
                continue
            vpro.set_valor(i/tot, 'Consultando personal indirecto...')
            if e.categoriaLaboral:
                catlab = e.categoriaLaboral.codigo or e.categoriaLaboral.puesto
            else:
                catlab = "N/A"
            fila = [e.apellidos + ", " + e.nombre, 
                    catlab, 
                    e.centroTrabajo and e.centroTrabajo.nombre or "N/A"] 
            for linea in LINEASPRODUCCION:  # @UnusedVariable
                fila += ["", "", "", "", ""]
            for centro in RESTOCENTROS_Y_TOTAL:  # @UnusedVariable
                fila += ["", "", "", ""]
            # Costes:
            # OJO: nomina base de empleado tiene prioridad sobre salarioBase 
            # de su categoría laboral (por si hay alguno con sueldo especial 
            # y tal).
            coste_horas = 0.0
            if e.nomina != 0:
                coste_horas = e.nomina
            elif e.categoriaLaboral:
                coste_horas = e.categoriaLaboral.salarioBase
            coste_horas * meses
            fila += [coste_horas,
                     0.0, 
                     0.0, 
                     coste_horas]   
                # Este último coste_horas es el total de las tres columnas.
            fila.append(e.id)
            res_resumen.append(fila)
            i += 1
        vpro.ocultar()
        self.rellenar_tabla(res_plus, res_resumen)

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        for tvnombre in ("tv_plus", "tv_resumen"):
            tv = self.wids[tvnombre]
            if tvnombre == "tv_resumen":
                filtro_ceros = range(tv.get_model().get_n_columns() - 5)
            else:
                filtro_ceros = range(tv.get_model().get_n_columns())
            abrir_csv(treeview2csv(tv, filtro_ceros = filtro_ceros))

    def imprimir(self, boton):
        from informes.treeview2pdf import treeview2pdf
        from formularios.reports import abrir_pdf
        for tvnombre, titulo, tvresumen, fake_cols in (
                ("tv_plus", "Consulta nóminas: plus salarial", 
                 "tv_totales_plus", 2), 
                ("tv_resumen", "Consulta nóminas: resumen", 
                 "tv_totales_resumen", 3)):
            # A los datos de los totales se le añaden "fake_cols" columnas 
            # de datos vacías para poder añadir una fila más al tv "tvnombre" 
            # antes de generar el PDF. Esa fila se eliminará justo después.
            tv = self.wids[tvnombre]
            if not len(tv.get_model()):
                continue
            # Antes de añadir nada, tengo que evitar que el dato me lo ordene, 
            # porque siempre quiero que el total esté al final.
            bak_order = []
            model = tv.get_model()
            ncol = 0
            for col in tv.get_columns():
                bak_order.append(col.get_sort_column_id())
                col.set_sort_column_id(-1)
                model.set_sort_func(ncol, lambda *args, **kw: 0)
                ncol += 1
            while gtk.events_pending(): gtk.main_iteration(False)
            # EObak_order
            try:
                fila_total = self.wids[tvresumen].get_model()[0]
            except IndexError:
                added = False
            else:
                fila_total = ([""] * (fake_cols-1) + ["TOTAL: "] 
                              + [i for i in fila_total])
                iter_total = tv.get_model().append(fila_total)
                added = True
            tvoriginal = tv
            if tv.get_model().get_n_columns() > 12:
                # Necesito hacer esto para que se redistribuyan los anchos 
                # correctamente:
                #nb = self.wids['notebook1']
                #current = nb.get_current_page()
                #for page in range(nb.get_n_pages()):
                #    nb.set_current_page(page)
                #    while gtk.events_pending(): gtk.main_iteration(False)
                #nb.set_current_page(current)
                tv = crear_fake_listview(tv, filtrar_nulos = True, 
                                             cols_a_ignorar = (1, 2))
                for icol in range(len(tv.get_columns())):
                    col = tv.get_column(icol)
                    tit_columna = col.get_title().strip()
                    if len(tit_columna.split()) > 1:
                        ntit_columna = ".".join(
                            [p[:1].upper() for p in tit_columna.split()[:-1]]
                            + tit_columna.split()[-1:])
                        tit_columna = ntit_columna
                    col.set_title(tit_columna)
            abrir_pdf(treeview2pdf(tv, 
                               titulo = titulo, 
                               fecha = self.wids['e_fechainicio'].get_text() 
                                       + " - " 
                                       + self.wids['e_fechafin'].get_text(), 
                               apaisado = tv.get_model().get_n_columns() > 12, 
                               pijama = True))
            if added:
                tv = tvoriginal
                tv.get_model().remove(iter_total)
            ncol = 0
            for col, order_id in zip(tv.get_columns(), bak_order):
                col.set_sort_column_id(order_id)
                model.set_sort_func(ncol, utils.funcion_orden, ncol)
                ncol += 1

def crear_fake_listview(tvorig, filtrar_nulos = False, cols_a_ignorar = []):
    """
    Crea un TreeView idéntico al recibido (model clonado, mismas columnas y 
    cabeceras, etc.).
    Si «filtrar_nulos» es True, ignora todas las columnas cuyo valor en todas 
    las filas sea "nulo" (cero, lista vacía, False, "", etc.).
    Las columnas cuyo índice esté en cols_a_ignorar, no se copian.
    """
    tv = gtk.TreeView()
    tv.set_name(tvorig.get_name())
    modelorig = tvorig.get_model()
    cols = []
    origcols = tvorig.get_columns()
    colsnulas = []
    anchos = []
    aligns = []
    for col, i in zip(origcols, range(len(origcols))):
        valores_no_nulos = [fila[i] for fila in modelorig if fila[i] and 
                                        fila[i] not in ("0", "0,0", "0,00")]
        if ((filtrar_nulos and not valores_no_nulos) 
                # Hay que filtrar nulos y no tiene no-nulos. Ingnoro.
            or (i in cols_a_ignorar)):
            colsnulas.append(i)
            continue
        cols.append((col.get_title(), 
                     #modelorig.get_column_type(i), 
                     "gobject.TYPE_STRING",     # Por aquí traga todo.
                     False, 
                     False, 
                     False, 
                     None))
        anchos.append(col.get_width())
        aligns.append(col.get_cell_renderers()[0].get_property("xalign"))
    cols.append(("ID", "gobject.TYPE_STRING", False, False, False, None))
    utils.preparar_listview(tv, cols)
    #for col, ancho in zip(tv.get_columns(), anchos):
    #    col.set_fixed_width(ancho) # Estos anchos son los del tv original. 
                                    # No valen si está filtrado
    for col, align in zip(tv.get_columns(), aligns):
        col.get_cell_renderers()[0].set_property("xalign", align) 
    model = tv.get_model()
    for fila in modelorig:
        if filtrar_nulos:
            _fila = []
            for indice in range(len(fila)):
                if indice not in colsnulas:
                    _fila.append(fila[indice])
            fila = _fila
        model.append(fila)
    return tv

def analizar_ch(ch, empleados):
    """
    En función de los datos del registro de control de horas asigna valores 
    al empleado correspondiente del diccionario.
    """
    empleado = ch.empleado
    if empleado not in empleados:
        empleados[empleado] = {"meses": 0, 
                               "horas festivo": 0.0, 
                               "horas sábado": 0.0, 
                               #"noches": 0, 
                               # CWT: Se paga el plus de nocturnidad por horas 
                               # de noche, no por noches completas. Así que 
                               # ahora se anotan aquí las noches fraccionadas 
                               # según las horas trabajadas (float en 
                               # vez de int).
                               "noches": 0.0, 
                               "horas extras día": 0.0, 
                               "horas extras noche": 0.0, 
                               "no absentismo": 0.0, 
                               "libre": 0.0}
        for linea in LINEASPRODUCCION:
            empleados[empleado][linea] = {"horas laborables": 0.0, 
                                          "horas extras": 0.0, 
                                          "horas noche": 0.0, 
                                          "horas mantenimiento sábado": 0.0, 
                                          "horas mantenimiento": 0.0, 
                                          "no absentismo": 0.0, 
                                          "libre": 0.0}
        for centro in RESTOCENTROS:
            empleados[empleado][centro] = {"horas laborables": 0.0, 
                                           "horas extras": 0.0, 
                                           "horas noche": 0.0, 
                                           "horas mantenimiento": 0.0, 
                                           "no absentismo": 0.0, 
                                           "libre": 0.0}
    # Datos para tabla de pluses
    if ch.festivo:
        empleados[empleado]["horas festivo"] += ch.calcular_total_horas()
    if ch.nocturnidad or ch.calcular_total_horas_extras_noche():
        # empleados[empleado]["noches"] += 1
        # CWT: Hay que contar las noches por fracción. Ya no se paga por noche 
        # completa.
        fraccion_noche = ch.get_por_hora()["noche"] / 8.0
        empleados[empleado]["noches"] += fraccion_noche
    empleados[empleado]["horas extras día"] \
        += ch.calcular_total_horas_extras_dia()
    empleados[empleado]["horas extras noche"] \
        += ch.calcular_total_horas_extras_noche()
    if ch.fecha.day_of_week == 5: 
        #empleados[empleado]["horas sábado"] += ch.calcular_total_horas()
        # CWT: Las horas de sábado para el plus solo son las de mantenimiento.
        hmantsab = ch.calcular_total_horas_mantenimiento()
        empleados[empleado]["horas sábado"] += hmantsab
        # CWT: Las horas extras a pagar el sábado no son acumulables con las 
        # de mantenimiento, por tanto las resto:
        extramantsabdia = ch.horasExtraDiaMantenimiento
        empleados[empleado]["horas extras día"] -= extramantsabdia
        extramantsabnoche = ch.horasExtraNocheMantenimiento
        empleados[empleado]["horas extras noche"] -= extramantsabnoche
    empleados[empleado]["no absentismo"] += ch.plusAbsentismo
    empleados[empleado]["libre"] += ch.importeLibre 
    # Datos para tabla resumen
    horas_por_centro = ch.get_por_centro_de_trabajo_y_tipo()
    for centro in horas_por_centro:
        empleados[empleado][centro]["horas laborables"] += (
            horas_por_centro[centro]["regulares"])
        empleados[empleado][centro]["horas extras"] += (
            horas_por_centro[centro]["extras"])
        empleados[empleado][centro]["horas noche"] += (
            horas_por_centro[centro]["noche"])
        empleados[empleado][centro]["horas mantenimiento"] += (
            horas_por_centro[centro]["mantenimiento"])
        try:
            empleados[empleado][centro]["horas mantenimiento sábado"] += (
                horas_por_centro[centro]["mantenimiento sábado"])
        except KeyError:    # No tiene mantenimiento sábados, no hago nada.
            pass

def convertir_a_filas(empleados, padre = None):
    """
    Convierte el diccionario de datos extraidos de los registros de control 
    de horas de personal por empleado en las dos listas de resultados de 
    pluses y resumen de la nómina.
    """
    pluses = []
    resumen = []
    es = empleados
    vpro = ventana_progreso.VentanaProgreso(padre = padre)
    i = 0
    tot = len(empleados)
    vpro.mostrar()
    for empleado in empleados:
        vpro.set_valor(i/tot, 'Calculando y convirtiendo datos...')
        i += 1
        # Cálculo de datos
        e = empleado    # Por abreviar
        cat = empleado.categoriaLaboral
        if not cat:
            catlab = "N/A"
            jefeturno = 0.0 
            noabsentismo = 0.0 
            libre = 0.0 
            festivos = 0.0 
            turnicidad = 0.0 
            sabados = 0.0 
            hextras = 0.0
            nocturnidad = 0.0 
        else:
            catlab = cat.codigo
            if not catlab:
                catlab = catlab.puesto
            jefeturno = es[e]["meses"] * cat.precioPlusJefeTurno
            #noabsentismo = 0.0 # DONE: No sé cómo calcularlo.
            noabsentismo = es[e]["no absentismo"] 
            libre = es[e]["libre"] 
            festivos = es[e]["horas festivo"] * cat.precioPlusFestivo
            turnicidad = es[e]["meses"] * cat.precioPlusTurnicidad 
                # OJO: Antes el plus de turnicidad solo era para fibras. Ya no.
            sabados = (es[e]["horas sábado"] 
                        * cat.precioPlusMantenimientoSabados)
            hextras = (es[e]["horas extras día"] * cat.precioHoraExtra + 
                es[e]["horas extras noche"] * cat.precioHoraNocturnidad)
            nocturnidad = es[e]["noches"] * cat.precioPlusNocturnidad
        # Fila pluses
        filaplus = (empleado.apellidos + ", " + empleado.nombre, 
                    catlab, 
                    jefeturno, 
                    noabsentismo, 
                    libre, 
                    festivos, 
                    turnicidad, 
                    sabados, 
                    hextras, 
                    nocturnidad, 
                    empleado.id)
        pluses.append(filaplus)
        # Fila resumen
        filaresumen = [filaplus[0], 
                       filaplus[1], 
                       empleado.centroTrabajo 
                        and empleado.centroTrabajo.nombre or "N/A"]
        horaslaborables = horasextras = nocturnidad = mantenimiento = 0.0
        for linea in LINEASPRODUCCION:
            filaresumen += [es[e][linea]["horas laborables"], 
                            es[e][linea]["horas extras"], 
                            es[e][linea]["horas noche"], 
                            es[e][linea]["horas mantenimiento sábado"], 
                            es[e][linea]["horas mantenimiento"]]
            horaslaborables += es[e][linea]["horas laborables"]
            horasextras += es[e][linea]["horas extras"]
            nocturnidad += es[e][linea]["horas noche"]
            mantenimiento += es[e][linea]["horas mantenimiento"]
        for centro in RESTOCENTROS:
            filaresumen += [es[e][centro]["horas laborables"], 
                            es[e][centro]["horas extras"], 
                            es[e][centro]["horas noche"], 
                            es[e][centro]["horas mantenimiento"]]
            horaslaborables += es[e][centro]["horas laborables"]
            horasextras += es[e][centro]["horas extras"]
            nocturnidad += es[e][centro]["horas noche"]
            mantenimiento += es[e][centro]["horas mantenimiento"]
        filaresumen += [horaslaborables, 
                        horasextras, 
                        nocturnidad, 
                        mantenimiento]
        # OJO: NOTA: Aunque se muestren las horas nocturnas, el precio de 
        # la nocturnidad se calcula por noches completas.
        if cat:
            #preciohora = cat.salarioBase / (8*21)
            preciohora = cat.precioHoraRegular
            precioHoraExtra = cat.precioHoraExtra
            precioPlusNocturnidad = cat.precioPlusNocturnidad
        else:
            preciohora = precioHoraExtra = precioPlusNocturnidad = 0.0
        filaresumen += [(horaslaborables + mantenimiento)* preciohora, 
                        (es[e]["horas extras día"] + 
                         es[e]["horas extras noche"]) * precioHoraExtra, 
                        es[e]["noches"] * precioPlusNocturnidad]
        filaresumen.append(filaresumen[-3] + filaresumen[-2] + filaresumen[-1])
        filaresumen.append(empleado.id)
        resumen.append(tuple(filaresumen))
    vpro.ocultar()
    return pluses, resumen

def rellenar_subtabla(filas, w):
    """
    Introduce las filas en el modelo del widget w y devuelve los totales
    de los campos numéricos en una lista (incluidos los IDs aunque no 
    tenga sentido).
    """
    totales = []
    model = w.get_model()
    model.clear()
    for fila in filas:
        filaformateada = []
        for valor in fila:
            try:
                strv = utils.float2str(valor)
            except:
                strv = valor
            filaformateada.append(strv)
        model.append(filaformateada)
        # Actualizo lista de totales con los valores numéricos únicamente
        offset = 0
        for i in range(len(fila)):
            try:
                valor = utils._float(fila[i])
            except ValueError:
                if fila[i] == "": # Es cadena vacía para el personal indirecto
                    valor = 0
                else:   # Si no, definitivamente es un campo no numérico.
                    offset -= 1 # Para saltar las primeras columnas de texto
            else:
                idest = i + offset
                try:
                    totales[idest] += valor
                except IndexError:
                    while len(totales) < idest:
                        totales.append(0)
                    totales.append(valor)
    return [totales]

 
if __name__ == '__main__':
    t = ConsultaMensualNominas() 

    
