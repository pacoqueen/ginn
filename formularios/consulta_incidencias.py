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
## consulta_incidencias.py -- 
###################################################################
## NOTAS:
##  
###################################################################
## Changelog:
## 
###################################################################
###################################################################
from ventana import Ventana
import utils
import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, time
import sys, os
try:
    import pclases
except ImportError:
    from os.path import join as pathjoin; sys.path.append(pathjoin("..", "framework"))
    import pclases
import mx
try:
    import geninformes
except ImportError:
    sys.path.append('../informes')
    import geninformes
import ventana_progreso
sys.path.insert(0, os.path.join("..", "PyChart-1.39"))
from pychart import *   # No me gusta, pero no queda otra
from tempfile import gettempdir

class ConsultaIncidencias(Ventana):
    inicio = None
    fin = None
    resultado = []
        
    def __init__(self, objeto = None, usuario = None):
        """
        Constructor. objeto puede ser un objeto de pclases con el que
        comenzar la ventana (en lugar del primero de la tabla, que es
        el que se muestra por defecto).
        """
        global fin
        Ventana.__init__(self, 'consulta_incidencias.glade', objeto)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_fecha_inicio/clicked': self.set_inicio,
                       'b_fecha_fin/clicked': self.set_fin, 
                       "b_exportar/clicked": self.exportar}
        self.add_connections(connections)
        cols = (('Tipo','gobject.TYPE_STRING',False,True,False,None),
                ('Inicio','gobject.TYPE_STRING',False,True,False,None),
                ('Fin','gobject.TYPE_STRING',False,True,False,None),
                ('Fecha parte','gobject.TYPE_STRING',False,True,False,None),
                ('Turno parte','gobject.TYPE_STRING',False,True,False,None),
                ('Observaciones','gobject.TYPE_STRING',False,True,False,None),
                ('Idincidencia','gobject.TYPE_INT64',False,False,False,None))
        utils.preparar_listview(self.wids['tv_datos'], cols)
        cols = (('Tipo', 'gobject.TYPE_STRING', False, True, True, None),
                ('Tiempo', 'gobject.TYPE_STRING', False, True, False, None),
                ('NADA', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(self.wids['tv_resumen'], cols)
        temp = time.localtime()
        self.fin = str(temp[0])+'/'+str(temp[1])+'/'+str(temp[2])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        import custom_widgets
        self.wids['velocimetro'] = custom_widgets.Velocimetro(0.0, 100.0, 0.0)
        self.wids['hbox8'].pack_end(self.wids['velocimetro'], False, False, 5)
        self.wids['velocimetro'].show_all()
        gtk.main()

    def exportar(self, boton):
        """
        Exporta el contenido del TreeView a un fichero csv.
        """
        import sys, os
        sys.path.append(os.path.join("..", "informes"))
        from treeview2csv import treeview2csv
        from informes import abrir_csv
        tv = self.wids['tv_datos']
        abrir_csv(treeview2csv(tv))

    def chequear_cambios(self):
        pass

    def rellenar_tabla(self, items):
    	"""
        Rellena el model con los items de la consulta
        """        
    	model = self.wids['tv_datos'].get_model()
    	model.clear()
        self.wids['tv_datos'].freeze_child_notify()
        self.wids['tv_datos'].set_model(None)
        total = 0
    	for i in items:            
            total += 1
            model.append((i.tipoDeIncidencia.descripcion,
                          utils.str_hora_corta(i.horainicio),
                          utils.str_hora_corta(i.horafin),
                          utils.str_fecha(i.parteDeProduccion.fecha),
                          utils.str_hora_corta(i.parteDeProduccion.horainicio)+'-'+utils.str_hora_corta(i.parteDeProduccion.horafin),
                          i.observaciones.decode('UTF-8', 'ignore'),
                          i.id))
        # El .decode es para evitar esto:
        #./consulta_incidencias.py:81: PangoWarning: Invalid UTF-8 string passed to pango_layout_set_text()
        self.wids['tv_datos'].set_model(model)
        self.wids['tv_datos'].thaw_child_notify()
        self.wids['e_total'].set_text("%d " % total)
        
    def set_inicio(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechainicio'].set_text(utils.str_fecha(temp))
        self.inicio = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])


    def set_fin(self,boton):
        temp = utils.mostrar_calendario(padre = self.wids['ventana'])
        self.wids['e_fechafin'].set_text(utils.str_fecha(temp))
        self.fin = str(temp[2])+'/'+str(temp[1])+'/'+str(temp[0])


    def por_fecha(self,e1,e2):
        """
        Permite ordenar una lista de albaranes por fecha
        """
        if e1.fecha < e2.fecha:
            return -1
        elif e1.fecha > e2.fecha:
            return 1
        else:
            return 0

        
    def buscar(self, boton):
        """
        Dadas fecha de inicio y de fin, lista todos los albaranes
        pendientes de facturar.
        """
        str2fecha = lambda s: mx.DateTime.DateTimeFrom(day = int(s.split("/")[2]), month = int(s.split("/")[1]), year = int(s.split("/")[0]))
        fechafin = str2fecha(self.fin)
        if self.inicio == None:
            partes = pclases.ParteDeProduccion.select(pclases.ParteDeProduccion.q.fecha <= fechafin, orderBy = 'fecha')
        else:
            fechainicio = str2fecha(self.inicio)
            partes = pclases.ParteDeProduccion.select(pclases.AND(pclases.ParteDeProduccion.q.fecha >= fechainicio,
                                                                  pclases.ParteDeProduccion.q.fecha <= fechafin), 
                                                      orderBy = 'fecha')
        vpro = ventana_progreso.VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        pos = 0.0
        tot = partes.count()
        incidencias = []
        t_paradas = mx.DateTime.DateTimeDelta(0)
        t_partes = mx.DateTime.DateTimeDelta(0)
        t_por_tipo = {}
        for p in partes:
            vpro.set_valor(pos/tot, 'Cargando...')
            if self.entra_en_criterio_seleccion(p):
                for i in p.incidencias:
                    incidencias.append(i)
                    duracion = i.get_duracion()
                    if duracion < 0 or duracion > mx.DateTime.oneDay: 
                        print "ERROR INCIDENCIA ", i
                    t_paradas += i.get_duracion()
                    if i.tipoDeIncidenciaID not in t_por_tipo:
                        t_por_tipo[i.tipoDeIncidenciaID] = mx.DateTime.DateTimeDelta(0) 
                    t_por_tipo[i.tipoDeIncidenciaID] += i.get_duracion()
                t_partes += p.get_duracion()
            pos+=1
        self.resultado = incidencias
        vpro.ocultar()
        self.rellenar_tabla(self.resultado)
        self.rellenar_pie(t_paradas, t_partes)
        self.rellenar_resumen(t_por_tipo)

    def rellenar_resumen(self, t_por_tipo):
        """
        Rellena la tabla resumen con tiempos por tipos de parada.
        """
        model = self.wids['tv_resumen'].get_model()
        model.clear()
        data = []
        for i in t_por_tipo:
            tipo = pclases.TipoDeIncidencia.get(i)
            st_tipo = tipo.descripcion
            tiempo = t_por_tipo[i]
            st_tiempo = "%d:%02d" % (int(tiempo.hours), int(tiempo.minute))
            model.append((st_tipo, st_tiempo, ""))
            # Gráfico usando PyChart:
            data.append((st_tipo, tiempo.hours))
        # Dibujo del gráfico
        if len(data) > 0:
            theme.use_color = True
            theme.reinitialize()
            tempdir = gettempdir()
            formato = "png"   # NECESITA ghostscript
            # formato = "svg"     # Windows no tiene soporte nativo para SVG, por tanto, Gtk en Windows tampoco.
            # formato = "eps"    # gtk.gdk.pixbuf_new_from_file() -lo que usa .set_from_image- no soporta EPS.
            nomarchivo = "%s.%s" % (mx.DateTime.localtime().strftime("gci_%Y_%m_%d_%H_%M_%S"), formato)
            nombregraph = os.path.join(tempdir, "%s") % (nomarchivo)
            can = canvas.init(fname = nombregraph, format=formato)
            ar = area.T(size=(200, 150), legend=legend.T(), x_grid_style = None, y_grid_style = None)
            plot = pie_plot.T(data=data, arc_offsets=[0,10,0,10],
                              shadow = (2, -2, fill_style.gray50),
                              label_offset = 25,
                              arrow_style = arrow.a3)
            ar.add_plot(plot)
            ar.draw(can)
            try:
                can.close()
                self.wids['im_graph'].set_size_request(200, 150)
                self.wids['im_graph'].set_from_file(nombregraph)
            except:
                utils.dialogo_info(titulo = "NECESITA GHOSTSCRIPT",
                                   texto = "Para ver gráficas en pantalla necesita instalar Ghostscript.\nPuede encontrarlo en el servidor de la aplicación o descargarlo de la web (http://www.cs.wisc.edu/~ghost/).",
                                   padre = self.wids['ventana'])
        else:
            self.wids['im_graph'].set_from_file("NOEXISTEPORTANTOVAADIBUJARUNASPA")

    def rellenar_pie(self, t_paradas, t_partes):
        """
        Rellena los datos del pie de la ventana (tiempo paradas, etc.).
        """
        st_paradas = "%d:%02d" % (int(t_paradas.hours), t_paradas.minute)
        t_produccion = t_partes - t_paradas
        st_produccion = "%d:%02d" % (int(t_produccion.hours), t_produccion.minute)
        try:
            rendimiento = 100.0 - ((t_paradas.hours / t_partes.hours) * 100.0)
        except ZeroDivisionError:
            rendimiento = 0.0
        self.wids['velocimetro'].set_value(rendimiento)
        s_rendimiento = "%s %%" % (utils.float2str(rendimiento))
        self.wids['e_total_paradas'].set_text(st_paradas)
        self.wids['e_total_partes'].set_text(st_produccion)
        self.wids['e_rendimiento'].set_text(s_rendimiento)

    def entra_en_criterio_seleccion(self, parte):
        """
        Si el parte es del tipo indicado en los radiobuttons devuelte True.
        NEW 29/01/07! También comprueba que el parte esté verificado.
        """
        res = False
        if self.wids['rb_todas'].get_active():
            res = True
        elif self.wids['rb_fibra'].get_active():
            res = parte.es_de_balas()
        elif self.wids['rb_geotextiles'].get_active():
            res = not parte.es_de_balas()
        elif self.wids['rb_geocompuestos'].get_active():
            res = False    #  Cuando haya partes de geocompuestos (¿los habrá algún día?) esto, evidentemente, habrá que cambiarlo.
        return res and parte.bloqueado

    def imprimir(self,boton):
        """
        Prepara la vista preliminar para la impresión del informe
        """
        import informes
        datos = []
        for i in self.resultado:
#            if len(i.observaciones) > 35:
#                observaciones = i.observaciones[:35]+'...'
#            else:
#                observaciones = i.observaciones        # Ya administra bien el salto de línea. No hace falta cortar.
            observaciones = i.observaciones        # Ya administra bien el salto de línea. No hace falta cortar.
            datos.append((i.tipoDeIncidencia.descripcion,
                          utils.str_hora_corta(i.horainicio),
                          utils.str_hora_corta(i.horafin),
                          utils.str_fecha(i.parteDeProduccion.fecha),
                          utils.str_hora_corta(i.parteDeProduccion.horainicio)+'-'+utils.str_hora_corta(i.parteDeProduccion.horafin),
                          observaciones))

        if (self.inicio) == None:            
            fechaInforme = 'Hasta '+utils.str_fecha(time.strptime(self.fin,"%Y/%m/%d"))
        else:
            fechaInforme = utils.str_fecha(time.strptime(self.inicio,"%Y/%m/%d"))+' - '+utils.str_fecha(time.strptime(self.fin,"%Y/%m/%d"))

        if datos != []:
            informes.abrir_pdf(geninformes.incidencias(datos,fechaInforme))




if __name__ == '__main__':
    t = ConsultaIncidencias()    
