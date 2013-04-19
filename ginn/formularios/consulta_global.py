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
## consulta_global.py - Resumen brutal de producciones y ventas.
###################################################################
## NOTAS:
## Después de varias actualizaciones, el tiempo estimado en 
## realizar todas las consultas ronda los 3'41". 
###################################################################
## Changelog:
## 12 de abril de 2006 -> Inicio
## 
###################################################################
## NOTAS: 
## Hay hasta 3 formas de contar los consumos de fibra. A saber:
##   1.- Con el criterio usado para calcular mermas en línea de 
## geotextiles. Una partida de carga se consume completa o no se 
## consume. La fecha en la que cuenta el consumo es la fecha del 
## último de los partes de producción de todas las partidas que 
## pertenecen a la partida de carga. Una partida de carga sin 
## producción es un descenso en las existencias de la fibra que 
## contiene pero no cuenta como consumo. Las partidas que empiezan
## a consumirse a final de mes no entran como consumo hasta el mes
## siguiente. De igual forma y como consecuencia de la fecha 
## efectiva de consumo, a principio de mes aparecerán partidas de 
## carga cuyo consumo comenzó el mes anterior pero no se 
## contabiliza hasta el actual.
##   2.- Contando directamente las partidas de carga completa 
## según la fecha de cada una. Hay varios métodos en la clase para 
## corregir las fechas en caso de que la partida se haya creado 
## antes de tiempo: igualándola a la fecha del primer parte que la 
## consume, igualándola a la fecha del albarán interno (si lo 
## tiene) o seleccionándola a mano. En cualquier caso, el consumo 
## entre dos fechas se obtiene buscando directamente las partidas 
## cuyas fechas entran en el rango. Independientemente de si se 
## ha consumido o no. Se ajusta mejor al cálculo de existencias 
## pero se aleja del consumo teórico que debería corresponderle a 
## los geotextiles fabricados entre ese rango.
##   3.- Contabilizando la fibra asociada a los albaranes internos 
## entre las fechas. Debería dar un resultado similar al método 
## anterior, pero es posible que existan partidas de carga que no 
## estén completamente relacionadas con albaranes, bien por olvido 
## del usuario o bien porque los albaranes internos de fibra se 
## empezaron a hacer cuando en el sistema ya iban en torno a 1000 
## partidas de carga.
###################################################################
from ventana import Ventana
from formularios import utils
import pygtk
pygtk.require('2.0')
import gtk
from framework import pclases
import mx.DateTime
from ventana_progreso import VentanaProgreso


class ConsultaGlobal(Ventana):

    def __init__(self, objeto = None, usuario = None):
        if isinstance(usuario, int):
            usuario = pclases.Usuario.get(usuario)
        self.usuario = usuario
        self.partidas_carga = {}
        Ventana.__init__(self, 'consulta_global.glade', objeto, usuario = usuario)
        connections = {'b_salir/clicked': self.salir,
                       'b_buscar/clicked': self.buscar,
                       'b_imprimir/clicked': self.imprimir,
                       'b_exportar/clicked': self.exportar}
        self.add_connections(connections)
        self.append_meses()
        preparar_tv(self.wids['tv_produccion_gtx'])
        preparar_tv(self.wids['tv_ventas_gtx'])
        preparar_tv(self.wids['tv_consumos_gtx'])
        preparar_tv(self.wids['tv_produccion_fibra'], listview = False)
        preparar_tv(self.wids['tv_ventas_fibra'])
        preparar_tv(self.wids['tv_consumos_fibra'])
        preparar_tv(self.wids['tv_produccion_bolsas'])
        preparar_tv(self.wids['tv_ventas_bolsas'])
        preparar_tv(self.wids['tv_consumos_bolsas'])
        preparar_tv(self.wids['tv_compras_geocompuestos'])
        preparar_tv(self.wids['tv_ventas_geocompuestos'])
        annoactual = mx.DateTime.localtime().year
        self.wids['e_anno'].set_text(str(annoactual))
        self.wids['b_guardar'] = gtk.Button()
        self.wids['b_guardar'].set_property("visible", False)
        self.wids['b_guardar'].set_sensitive(False)
        gtk.main()

    def activar_widgets(self, *args, **kw):
        pass

    def append_meses(self):
        """
        Añade un hbox con los 12 meses del año para poder marcar 
        y desmarcar los meses que se incluirán en la consulta.
        """
        self.wids['hboxmeses'] = gtk.HBox()
        self.wids['vbox3'].add(self.wids['hboxmeses'])
        for n, mes in zip(range(1, 13), ("enero", "febrero", "marzo", 
                                         "abril", "mayo", "junio", 
                                         "julio", "agosto", "septiembre", 
                                         "octubre", "noviembre", "diciembre")):
            self.wids['ch_%d' % n] = gtk.CheckButton(mes)
            self.wids['ch_%d' % n].set_active(True)
            self.wids['hboxmeses'].add(self.wids['ch_%d' % n])
        self.wids['b_todos'] = gtk.Button("Marcar todos los meses")
        self.wids['b_todos'].connect("clicked", self.marcar_todos, True)
        self.wids['b_ninguno'] = gtk.Button("Desmarcar todos los meses")
        self.wids['b_ninguno'].connect("clicked", self.marcar_todos, False)
        self.wids['hbox_b_meses'] = gtk.HBox()
        self.wids['hbox_b_meses'].add(self.wids['b_todos'])
        self.wids['hbox_b_meses'].add(self.wids['b_ninguno'])
        self.wids['vbox3'].add(self.wids['hbox_b_meses'])
        self.wids['vbox3'].add(gtk.HSeparator())
        self.wids['vbox3'].set_spacing(5)
        self.wids['vbox3'].show_all()

    def marcar_todos(self, boton, estado):
        for i in range(1, 13):
            self.wids['ch_%d' % i].set_active(estado)

    def chequear_cambios(self):
        pass

    def get_anno(self):
        """
        Devuelve el año del entry de la ventana.
        Si no es un número, devuelve el año actual y 
        avisa con un mensaje de error.
        """
        anno = self.wids['e_anno'].get_text()
        try:
            anno = int(anno)
        except ValueError:
            year = mx.DateTime.localtime().year
            utils.dialogo_info(titulo = "ERROR FORMATO NUMÉRICO", 
                               texto = "El texto %s no es un año correcto.\n\nSe usará el año de la fecha actual: %d." % (anno, year), 
                               padre = self.wids['ventana'])
            anno = year
        return anno

    def buscar(self, boton):
        """
        Inicia la consulta para el año indicado en el widget y 
        rellena las tablas con la información obtenida.
        """
        anno = self.get_anno()
        vpro = VentanaProgreso(padre = self.wids['ventana'])
        vpro.mostrar()
        meses = []
        for i in range(1, 13):
            if self.wids['ch_%d' % i].get_active():
                meses.append(i)
        meses = tuple(meses)
        # PLAN: cache = preconsultar()
        vpro.set_valor(0.0, "Analizando venta de fibra ignorando tarifas...")
        ventas_fibra_por_color = buscar_ventas_fibra_color(anno, vpro, 0.15, 
                                                           meses)
        vpro.set_valor(0.15, "Analizando producción de geotextiles...")
        produccion_gtx = buscar_produccion_gtx(anno, vpro, 0.15, self.logger, 
                                               meses)  #, cache)
        vpro.set_valor(0.3, "Analizando ventas...")
        (ventas_gtx, 
         ventas_fibra, 
         ventas_bolsas) = buscar_ventas(anno, vpro, 0.15, meses)  #, cache)
        vpro.set_valor(0.45, "Analizando consumos...")
        (consumos_gtx, 
         consumos_fibra, 
         consumos_bolsas) = buscar_consumos(anno, vpro, 0.15, meses) #, cache)
        vpro.set_valor(0.6, "Analizando producción de fibra...")
        produccion_fibra = buscar_produccion_fibra(anno, vpro, 0.1, 
                                                   self.logger, 
                                                   meses)  #, cache)
        vpro.set_valor(0.7, "Analizando producción de fibra de cemento...")
        produccion_bolsas = buscar_produccion_bolsas(anno, vpro, 0.1, 
                                                     self.logger, 
                                                     meses)  #, cache)
        vpro.set_valor(0.8, "Analizando compras de comercializados...")
        compras_geocompuestos = buscar_compras_geocompuestos(anno, vpro, 0.1, 
                                                             self.logger, 
                                                             meses)  #, cache)
        vpro.set_valor(0.9, "Analizando ventas de comercializados...")
        ventas_geocompuestos = buscar_ventas_geocompuestos(anno, vpro, 0.1, 
                                                           self.logger, 
                                                           meses)  #, cache)
        vpro.set_valor(1.0, "Volcando datos a la ventana...")
        self.rellenar_tablas(produccion_gtx, ventas_gtx, consumos_gtx, 
                             produccion_fibra, ventas_fibra, consumos_fibra, 
                             ventas_fibra_por_color, 
                             produccion_bolsas, ventas_bolsas, consumos_bolsas, 
                             compras_geocompuestos, ventas_geocompuestos)
        vpro.ocultar()

    def rellenar_tablas(self, produccion_gtx, ventas_gtx, consumos_gtx, 
                        produccion_fibra, ventas_fibra, consumos_fibra, 
                        ventas_fibra_por_color, 
                        produccion_bolsas, ventas_bolsas, consumos_bolsas, 
                        compras_geocompuestos, ventas_geocompuestos):
        """
        Introduce la información de producciones, ventas y consumos de 
        geotextiles y fibra en los TreeViews correspondientes.
        """
        ## GTX
        self.rellenar_tabla_produccion_gtx(produccion_gtx)
        self.rellenar_tabla_ventas_gtx(ventas_gtx)
        self.rellenar_tabla_consumos(consumos_gtx, 
                                     self.wids['tv_consumos_gtx'])
        ## FIBRA
        self.rellenar_tabla_produccion_fibra(produccion_fibra)
        self.rellenar_tabla_consumos(consumos_fibra, 
                                     self.wids['tv_consumos_fibra'])
        # CWT: CAMBIADA LA FORMA DE AGRUPAR VENTAS FIBRA: 
        #self.rellenar_tabla_ventas_fibra(ventas_fibra)
        self.rellenar_tabla_ventas_fibra_por_color(ventas_fibra_por_color)
        ## BOLSAS
        self.rellenar_tabla_produccion_bolsas(produccion_bolsas)
        self.rellenar_tabla_ventas_bolsas(ventas_bolsas)
        self.rellenar_tabla_consumos(consumos_bolsas, 
                                     self.wids['tv_consumos_bolsas'])
        ## GEOCOMPUESTOS (COMERCIALIZADOS)
        self.rellenar_tabla_compras_geocompuestos(compras_geocompuestos)
        self.rellenar_tabla_ventas_geocompuestos(ventas_geocompuestos)
    
    def rellenar_tabla_produccion_bolsas(self, produccion_bolsas):
        """
        Recibe un diccionario con la producción en A y B de geocem por 
        meses e introduce esa información en el treeview.
        """
        model = self.wids['tv_produccion_bolsas'].get_model()
        model.clear()
        fila_kilos = ["Kilos"]
        fila_bolsas = ["Bolsas"]
        fila_kilos_a = ["Kilos A"]
        fila_bolsas_a = ["Bolsas A"]
        fila_kilos_b = ["Kilos B"]
        fila_bolsas_b = ["Bolsas B"]
        fila_consumo = ["Kg consumidos"]
        fila_kilos_hora = ["Kilos / hora"]
        fila_horas = ["Horas de trabajo"]
        fila_horas_produccion = ["Horas de producción"]
        fila_dias = ["Días de trabajo"]
        fila_turnos = ["Turnos / día"]
        fila_empleados = ["Trabajadores / día"]
        fila_productividad = ["Productividad"]
        bolsas_totales = 0
        kilos_totales = 0.0
        bolsas_a_totales = 0
        kilos_a_totales = 0.0
        bolsas_b_totales = 0
        kilos_b_totales = 0.0
        kilos_consumidos_totales = 0.0
        for mes in xrange(12):
        #for mes in produccion_bolsas:
            bolsas_totales_mes = (produccion_bolsas[mes]['A']['bolsas'] 
                                  + produccion_bolsas[mes]['B']['bolsas'])
            bolsas_totales += bolsas_totales_mes
            fila_bolsas.append(utils.float2str(bolsas_totales_mes, 0))
            
            kilos_totales_mes = (produccion_bolsas[mes]['A']['kilos'] 
                                 + produccion_bolsas[mes]['B']['kilos'])
            kilos_totales += kilos_totales_mes
            fila_kilos.append(utils.float2str(kilos_totales_mes))
            
            bolsas_a_mes = produccion_bolsas[mes]['A']['bolsas']
            fila_bolsas_a.append(utils.float2str(bolsas_a_mes, 0))
            bolsas_a_totales += bolsas_a_mes
            
            kilos_a_mes = produccion_bolsas[mes]['A']['kilos']
            fila_kilos_a.append(utils.float2str(kilos_a_mes))
            kilos_a_totales += kilos_a_mes

            bolsas_b_mes = produccion_bolsas[mes]['B']['bolsas']
            fila_bolsas_b.append(utils.float2str(bolsas_b_mes, 0))
            bolsas_b_totales += bolsas_b_mes
            
            kilos_b_mes = produccion_bolsas[mes]['B']['kilos']
            fila_kilos_b.append(utils.float2str(kilos_b_mes))
            kilos_b_totales += kilos_b_mes

            consumo = produccion_bolsas[mes]['consumo']
            kilos_consumidos_totales += consumo
            fila_consumo.append(utils.float2str(consumo))
            fila_kilos_hora.append(utils.float2str(
                produccion_bolsas[mes]['kilos_hora']))
            fila_horas.append(utils.float2str(
                produccion_bolsas[mes]['horas'], autodec = True))
            fila_horas_produccion.append(utils.float2str(
                produccion_bolsas[mes]['horas_produccion'], autodec = True))
            fila_dias.append("%d" % (produccion_bolsas[mes]['dias']))
            fila_turnos.append(utils.float2str(
                produccion_bolsas[mes]['turnos']))
            fila_empleados.append(utils.float2str(
                produccion_bolsas[mes]['empleados'], autodec = True))
            fila_productividad.append("%s %%" % (utils.float2str(
                produccion_bolsas[mes]['productividad'] * 100.0)))
        # Totales:
        fila_kilos.append(utils.float2str(kilos_totales))
        fila_bolsas.append(utils.float2str(bolsas_totales, 0))
        fila_kilos_a.append(utils.float2str(kilos_a_totales))
        fila_bolsas_a.append(utils.float2str(bolsas_a_totales, 0))
        fila_kilos_b.append(utils.float2str(kilos_b_totales))
        fila_bolsas_b.append(utils.float2str(bolsas_b_totales, 0))
        fila_consumo.append(utils.float2str(kilos_consumidos_totales))
        avg = lambda l: (1.0 * sum(l)) / len(l)
        fila_kilos_hora.append(utils.float2str(avg(
            [produccion_bolsas[mes]['kilos_hora'] 
             for mes in produccion_bolsas])))
        fila_horas.append(utils.float2str(sum(
            [produccion_bolsas[mes]['horas'] for mes in produccion_bolsas])))
        fila_horas_produccion.append(utils.float2str(sum(
            [produccion_bolsas[mes]['horas_produccion'] 
             for mes in produccion_bolsas])))
        fila_dias.append("%d" % (sum(
            [produccion_bolsas[mes]['dias'] for mes in produccion_bolsas])))
        fila_turnos.append("%s" % utils.float2str(avg(
            [produccion_bolsas[mes]['turnos'] for mes in produccion_bolsas])))
        fila_empleados.append("%s" % utils.float2str(avg(
            [produccion_bolsas[mes]['empleados'] 
             for mes in produccion_bolsas])))
        fila_productividad.append("%s %%" % utils.float2str(avg(
            [produccion_bolsas[mes]['productividad'] 
             for mes in produccion_bolsas]) * 100.0))
        # ... al model:
        model.append(fila_kilos + ["Hello."])
        model.append(fila_bolsas + ["Is there anybody in there?"])
        model.append(fila_kilos_a + ["Just nod if you can hear me"])
        model.append(fila_bolsas_a + ["Is there aneyone home?"])
        model.append(fila_kilos_b + ["Come on, now."])
        model.append(fila_bolsas_b + ["I hear you're feeling down"])
        model.append(fila_consumo + ["Well I can ease your pain."])
        model.append(fila_kilos_hora + ["Get you on your feet again."])
        model.append(fila_horas + ["Relax."])
        model.append(fila_horas_produccion + ["I need some information first"])
        model.append(fila_dias + ["Just the basic facts."])
        model.append(fila_turnos + ["Can you show me where it hurts?"])
        model.append(fila_empleados + ["There is no pain, you are receding."])
        model.append(fila_productividad + ["I have become comfortably numb."])

    def rellenar_tabla_ventas_fibra_por_color(self, ventas_fibra_por_color):
        model = self.wids['tv_ventas_fibra'].get_model()
        model.clear()
        for fila in ventas_fibra_por_color:
            model.append(fila)

    def rellenar_tabla_produccion_fibra(self, p):
        model = self.wids['tv_produccion_fibra'].get_model()
        model.clear()
        # "Encabezado"
        fila_total = ["Kg totales"]
        filas_colores = {}
        for i in xrange(12):
            for color in p[i]["colores"]:
                if color not in filas_colores:
                    filas_colores[color] = [color]
        colores_ordenados = filas_colores.keys()
        colores_ordenados.sort()
        fila_cemento = ["Geocem"]
        fila_merma = ["Merma"]
        fila_porc_merma = ["% merma"]
        fila_granza = ["Granza"]
        fila_reciclada = ["Granza reciclada"]
        fila_medio_b = ["Peso medio bala"]
        fila_medio_bb = ["Peso medio bigbag"]
        fila_b = ['Kg "B"']
        fila_kilos_hora = ["Kilos/hora"]
        fila_dias = ["Días de trabajo"]
        fila_horas = ["Horas de trabajo"]
        fila_horas_produccion = ["Horas de producción"]
        fila_turnos = ["Turnos / día"]
        fila_empleados = ["Trabajadores / día"]
        fila_productividad = ["Productividad"]
        fila_cable = ["Fibra C -reciclada- (no computa en el total producido)"]
        filas_c = []
        # Detalle meses
        for i in xrange(12):
            fila_total.append(utils.float2str(p[i]['total']))
            for color in colores_ordenados:
            #for color in filas_colores:
                try:
                    filas_colores[color].append(utils.float2str(p[i]["colores"][color]))
                except KeyError:
                    filas_colores[color].append(utils.float2str(0.0))
            fila_cemento.append(utils.float2str(p[i]["cemento"]))
            fila_merma.append(utils.float2str(p[i]["merma"]))
            fila_porc_merma.append(utils.float2str(p[i]["porc_merma"]))
            fila_granza.append(utils.float2str(p[i]["granza"]))
            fila_reciclada.append(utils.float2str(p[i]["reciclada"]))
            fila_medio_b.append(utils.float2str(p[i]["media_bala"]))
            fila_medio_bb.append(utils.float2str(p[i]["media_bigbag"]))
            fila_b.append(utils.float2str(p[i]["kilos_b"]))
            fila_kilos_hora.append(utils.float2str(p[i]['kilos_hora']))
            fila_horas.append(utils.float2str(p[i]['horas'], autodec = True))
            fila_horas_produccion.append(utils.float2str(p[i]['horas_produccion'], autodec = True))
            fila_dias.append("%d" % (p[i]['dias']))
            fila_turnos.append(utils.float2str(p[i]['turnos']))
            fila_empleados.append(utils.float2str(p[i]['empleados'], autodec = True))
            # Para poder después calcular la media y mostrar el valor sin tener que multiplicar, lo multiplico todo aquí:
            p[i]['productividad'] *= 100.0
            #fila_productividad.append("%s %%" % (utils.float2str(p[i]['productividad'])))  # Con los símbolos de % no puedo después calcular la media "fácil-mente".
            fila_productividad.append("%s" % (utils.float2str(p[i]['productividad'])))
            fila_cable.append("%s" % (utils.float2str(p[i]['balas_cable']['total'])))
            for tipo_cable in p[i]['balas_cable']:
                if tipo_cable != 'total':
                    if tipo_cable not in [f[0] for f in filas_c]:
                        nueva_fila_c = [tipo_cable] + ["0.0"]*i + [utils.float2str(p[i]['balas_cable'][tipo_cable])] + ["0.0"]*(11-i)
                        filas_c.append(nueva_fila_c)
                    else:
                        for fila in filas_c:
                            if fila[0] == tipo_cable:
                                fila[i+1] = utils.float2str(p[i]['balas_cable'][tipo_cable])
        # Columna totales e invisible
        avg = lambda l: (1.0 * sum(l)) / len(l)
        for fila, func in [(fila_total, sum)] + [(filas_colores[c], sum) for c in colores_ordenados] + [(fila_cemento, sum), 
                    (fila_merma, sum), (fila_porc_merma, avg), (fila_granza, sum), (fila_reciclada, sum), 
                    (fila_medio_b, avg), (fila_medio_bb, avg), (fila_b, sum), (fila_kilos_hora, avg), 
                    (fila_productividad, avg), (fila_dias, sum), (fila_horas, sum), (fila_horas_produccion, sum), 
                    (fila_turnos, avg), (fila_empleados, avg), (fila_cable, sum)]:
            fila.append(utils.float2str(func([utils._float(dato) for dato in fila[1:]])))
            fila.append("Can you see the real me?")
            # Este TreeView va con TreeStore en lugar de ListStore, necesita un nodo padre para las filas.
            ultimo_padre = model.append(None, (fila))
            # OJO: El último padre, tal y como se insertan los datos, es el de la fila cable. Si por lo que sea
            # se llegara a cambiar hay que alterar el orden del desglose de la fibra reciclada de cable C que 
            # viene a continuación:
        for fila, func in zip(filas_c, [sum]*len(filas_c)):
            fila.append(utils.float2str(func([utils._float(dato) for dato in fila[1:]])))
            fila.append("Can you see the real me?")
            # Este TreeView va con TreeStore en lugar de ListStore, necesita un nodo padre para las filas.
            model.append(ultimo_padre, (fila))

    def rellenar_tabla_consumos(self, dic, tv):
        model = tv.get_model()
        model.clear()
        for producto in dic:
            total = 0.0
            fila = [producto.descripcion]
            for mes in xrange(12):
                try:
                    cant = dic[producto][mes]
                except KeyError:    # No hay consumos de ese producto para ese mes
                    cant = 0.0
                total += cant
                fila.append(utils.float2str(cant, 4, autodec = True))
            fila.append(utils.float2str(total, 4, autodec = True))
            model.append(fila + ["Sally take my hand"])

    def rellenar_tabla_ventas_fibra(self, ventas_fibra):
        model = self.wids['tv_ventas_fibra'].get_model()
        model.clear()

        fila_total_kg = ["kg"]
        fila_total_e = ["euros"]
        total_kg = 0.0
        total_e = 0.0
        for mes in xrange(12):      # En diccionarios no hay orden. Corremos el riesgo de recorrer los meses erróneamente.
        #for mes in ventas_fibra['total']:  
            total_kg += ventas_fibra['total'][mes]['kilos']
            total_e += ventas_fibra['total'][mes]['euros']
            fila_total_kg.append(utils.float2str(ventas_fibra['total'][mes]['kilos']))
            fila_total_e.append(utils.float2str(ventas_fibra['total'][mes]['euros']))
        fila_total_kg.append(utils.float2str(total_kg))
        fila_total_e.append(utils.float2str(total_e))
        model.append(fila_total_kg + ["I used"])
        model.append(fila_total_e + ["to love"])

        for tarifa in [t for t in ventas_fibra.keys() if t != 'total']:
            fila_kg = ["%s kg" % (tarifa != None and tarifa.nombre or "Otros")]
            fila_e = ["%s euros"% (tarifa != None and tarifa.nombre or "Otros")]
            total_kg = 0.0
            total_e = 0.0
            for mes in xrange(12):
            # for mes in ventas_fibra[tarifa]:
                if mes in ventas_fibra[tarifa]:
                    total_kg += ventas_fibra[tarifa][mes]['kilos']
                    total_e += ventas_fibra[tarifa][mes]['euros']
                    fila_kg.append(utils.float2str(ventas_fibra[tarifa][mes]['kilos']))
                    fila_e.append(utils.float2str(ventas_fibra[tarifa][mes]['euros']))
                else:
                    fila_kg.append(utils.float2str(0.0))
                    fila_e.append(utils.float2str(0.0))
            fila_kg.append(utils.float2str(total_kg))
            fila_e.append(utils.float2str(total_e))
            model.append(fila_kg + ["I used"])
            model.append(fila_e + ["to love"])

    def rellenar_tabla_compras_geocompuestos(self, compras_geocompuestos):
        model = self.wids['tv_compras_geocompuestos'].get_model()
        model.clear()

        fila_total_cantidad = ["cantidad"]
        fila_total_e = ["euros"]
        total_cantidad = 0.0
        total_e = 0.0
        for mes in xrange(12):
            total_cantidad += compras_geocompuestos['total'][mes]['cantidad']
            total_e += compras_geocompuestos['total'][mes]['euros']
            fila_total_cantidad.append(utils.float2str(
                compras_geocompuestos['total'][mes]['cantidad']))
            fila_total_e.append(utils.float2str(
                compras_geocompuestos['total'][mes]['euros']))
        fila_total_cantidad.append(utils.float2str(total_cantidad))
        fila_total_e.append(utils.float2str(total_e))
        model.append(fila_total_cantidad + ["Eternal sunshine of"])
        model.append(fila_total_e + ["the spotless mind."])

        # Los geocompuestos se venden en metros cuadrados...
        # ... a no ser que se indique otra cosa:
        try:
            tdp = pclases.TipoDeMaterial.select(pclases.OR(
              pclases.TipoDeMaterial.q.descripcion.contains("eocompuesto"), 
              pclases.TipoDeMaterial.q.descripcion.contains("omercializado"))
            )[0]
            moda = {}
            for pc in tdp.productosCompra:
                try:
                    moda[pc.unidad] += 1
                except KeyError:
                    moda[pc.unidad] = 1
            try:
                maximo = max([moda[u] for u in moda])
                for u in moda:
                    if moda[u] == maximo:
                        unidad = u
                        break
            except ValueError:
                raise IndexError    # Para que coja unidad por defecto.
        except IndexError:
            unidad = "m²"
        for proveedor in [t for t in compras_geocompuestos.keys() if t != 'total']:
            fila_cantidad = ["%s (%s)" % (
                proveedor != None and proveedor.nombre or "Sin proveedor", 
                unidad)]
            fila_e = ["%s (€)"%(proveedor != None and proveedor.nombre 
                      or "Sin proveedor")]
            total_cantidad = 0.0
            total_e = 0.0
            for mes in xrange(12):
                if mes in compras_geocompuestos[proveedor]:
                    total_cantidad += compras_geocompuestos[proveedor][mes]['cantidad']
                    total_e += compras_geocompuestos[proveedor][mes]['euros']
                    fila_cantidad.append(utils.float2str(
                        compras_geocompuestos[proveedor][mes]['cantidad']))
                    fila_e.append(utils.float2str(
                        compras_geocompuestos[proveedor][mes]['euros']))
                else:
                    fila_cantidad.append(utils.float2str(0.0))
                    fila_e.append(utils.float2str(0.0))
            fila_cantidad.append(utils.float2str(total_cantidad))
            fila_e.append(utils.float2str(total_e))
            model.append(fila_cantidad + 
                ["You can erase someone from your mind."])
            model.append(fila_e + 
                ["Getting them out of your heart is another story."])

    def rellenar_tabla_ventas_geocompuestos(self, ventas_geocompuestos):
        model = self.wids['tv_ventas_geocompuestos'].get_model()
        model.clear()

        fila_total_cantidad = ["cantidad"]
        fila_total_e = ["euros"]
        total_cantidad = 0.0
        total_e = 0.0
        for mes in xrange(12):
            total_cantidad += ventas_geocompuestos['total'][mes]['cantidad']
            total_e += ventas_geocompuestos['total'][mes]['euros']
            fila_total_cantidad.append(utils.float2str(
                ventas_geocompuestos['total'][mes]['cantidad']))
            fila_total_e.append(utils.float2str(
                ventas_geocompuestos['total'][mes]['euros']))
        fila_total_cantidad.append(utils.float2str(total_cantidad))
        fila_total_e.append(utils.float2str(total_e))
        model.append(fila_total_cantidad + ["Eternal sunshine of"])
        model.append(fila_total_e + ["the spotless mind."])

        # Los geocompuestos se venden en metros cuadrados...
        # ... a no ser que se indique otra cosa:
        try:
            tdp = pclases.TipoDeMaterial.select(pclases.OR(
                pclases.TipoDeMaterial.q.descripcion.contains("eocompuesto"), 
                pclases.TipoDeMaterial.q.descripcion.contains("omercializado")
              ))[0]
            moda = {}
            for pc in tdp.productosCompra:
                try:
                    moda[pc.unidad] += 1
                except KeyError:
                    moda[pc.unidad] = 1
            try:
                maximo = max([moda[u] for u in moda])
                for u in moda:
                    if moda[u] == maximo:
                        unidad = u
                        break
            except ValueError:
                raise IndexError    # Para que coja unidad por defecto.
        except IndexError:
            unidad = "m²"
        for tarifa in [t for t in ventas_geocompuestos.keys() if t != 'total']:
            fila_cantidad = ["%s (%s)" % (
                tarifa != None and tarifa.nombre or "Sin tarifa", 
                unidad)]
            fila_e = ["%s (€)"%(tarifa != None and tarifa.nombre 
                      or "Sin tarifa")]
            total_cantidad = 0.0
            total_e = 0.0
            for mes in xrange(12):
                if mes in ventas_geocompuestos[tarifa]:
                    total_cantidad += ventas_geocompuestos[tarifa][mes]['cantidad']
                    total_e += ventas_geocompuestos[tarifa][mes]['euros']
                    fila_cantidad.append(utils.float2str(
                        ventas_geocompuestos[tarifa][mes]['cantidad']))
                    fila_e.append(utils.float2str(
                        ventas_geocompuestos[tarifa][mes]['euros']))
                else:
                    fila_cantidad.append(utils.float2str(0.0))
                    fila_e.append(utils.float2str(0.0))
            fila_cantidad.append(utils.float2str(total_cantidad))
            fila_e.append(utils.float2str(total_e))
            model.append(fila_cantidad + 
                ["You can erase someone from your mind."])
            model.append(fila_e + 
                ["Getting them out of your heart is another story."])

    def rellenar_tabla_ventas_bolsas(self, ventas_bolsas):
        model = self.wids['tv_ventas_bolsas'].get_model()
        model.clear()

        fila_total_bolsas = ["bolsas"]
        fila_total_kg = ["kg"]
        fila_total_e = ["euros"]
        total_bolsas = 0.0
        total_kg = 0.0
        total_e = 0.0
        for mes in xrange(12):
        # for mes in ventas_bolsas['total']:
            total_bolsas += ventas_bolsas['total'][mes]['bolsas']
            total_kg += ventas_bolsas['total'][mes]['kilos']
            total_e += ventas_bolsas['total'][mes]['euros']
            fila_total_bolsas.append(utils.float2str(
                ventas_bolsas['total'][mes]['bolsas']))
            fila_total_kg.append(utils.float2str(
                ventas_bolsas['total'][mes]['kilos']))
            fila_total_e.append(utils.float2str(
                ventas_bolsas['total'][mes]['euros']))
        fila_total_bolsas.append(utils.float2str(total_bolsas, 0))
        fila_total_kg.append(utils.float2str(total_kg))
        fila_total_e.append(utils.float2str(total_e))
        model.append(fila_total_bolsas + ["The girl"])
        model.append(fila_total_kg + ["I used"])
        model.append(fila_total_e + ["to love"])

        for tarifa in [t for t in ventas_bolsas.keys() if t != 'total']:
            fila_bolsas = ["%s bolsas" % (tarifa != None and tarifa.nombre 
                           or "Otros")]
            fila_kg = ["%s kg" % (tarifa != None and tarifa.nombre or "Otros")]
            fila_e = ["%s euros"%(tarifa != None and tarifa.nombre or "Otros")]
            total_bolsas = 0
            total_kg = 0.0
            total_e = 0.0
            for mes in xrange(12):
            # for mes in ventas_bolsas[tarifa]:
                if mes in ventas_bolsas[tarifa]:
                    total_bolsas += ventas_bolsas[tarifa][mes]['bolsas']
                    total_kg += ventas_bolsas[tarifa][mes]['kilos']
                    total_e += ventas_bolsas[tarifa][mes]['euros']
                    fila_bolsas.append(utils.float2str(
                        ventas_bolsas[tarifa][mes]['bolsas']))
                    fila_kg.append(utils.float2str(
                        ventas_bolsas[tarifa][mes]['kilos']))
                    fila_e.append(utils.float2str(
                        ventas_bolsas[tarifa][mes]['euros']))
                else:
                    fila_bolsas.append(utils.float2str(0.0))
                    fila_kg.append(utils.float2str(0.0))
                    fila_e.append(utils.float2str(0.0))
            fila_bolsas.append(utils.float2str(total_bolsas, 0))
            fila_kg.append(utils.float2str(total_kg))
            fila_e.append(utils.float2str(total_e))
            model.append(fila_bolsas + ["The girl"])
            model.append(fila_kg + ["I used"])
            model.append(fila_e + ["to love"])

    def rellenar_tabla_ventas_gtx(self, ventas_gtx):
        model = self.wids['tv_ventas_gtx'].get_model()
        model.clear()

        fila_total_m = ["m²"]
        fila_total_kg = ["kg"]
        fila_total_e = ["euros"]
        total_m = 0.0
        total_kg = 0.0
        total_e = 0.0
        for mes in xrange(12):
        # for mes in ventas_gtx['total']:
            total_m += ventas_gtx['total'][mes]['metros']
            total_kg += ventas_gtx['total'][mes]['kilos']
            total_e += ventas_gtx['total'][mes]['euros']
            fila_total_m.append(utils.float2str(ventas_gtx['total'][mes]['metros']))
            fila_total_kg.append(utils.float2str(ventas_gtx['total'][mes]['kilos']))
            fila_total_e.append(utils.float2str(ventas_gtx['total'][mes]['euros']))
        fila_total_m.append(utils.float2str(total_m))
        fila_total_kg.append(utils.float2str(total_kg))
        fila_total_e.append(utils.float2str(total_e))
        model.append(fila_total_m + ["The girl"])
        model.append(fila_total_kg + ["I used"])
        model.append(fila_total_e + ["to love"])

        for tarifa in [t for t in ventas_gtx.keys() if t != 'total']:
            fila_m = ["%s m²" % (tarifa != None and tarifa.nombre or "Otros")]
            fila_kg = ["%s kg" % (tarifa != None and tarifa.nombre or "Otros")]
            fila_e = ["%s euros"% (tarifa != None and tarifa.nombre or "Otros")]
            total_m = 0.0
            total_kg = 0.0
            total_e = 0.0
            for mes in xrange(12):
            # for mes in ventas_gtx[tarifa]:
                if mes in ventas_gtx[tarifa]:
                    total_m += ventas_gtx[tarifa][mes]['metros']
                    total_kg += ventas_gtx[tarifa][mes]['kilos']
                    total_e += ventas_gtx[tarifa][mes]['euros']
                    fila_m.append(utils.float2str(ventas_gtx[tarifa][mes]['metros']))
                    fila_kg.append(utils.float2str(ventas_gtx[tarifa][mes]['kilos']))
                    fila_e.append(utils.float2str(ventas_gtx[tarifa][mes]['euros']))
                else:
                    fila_m.append(utils.float2str(0.0))
                    fila_kg.append(utils.float2str(0.0))
                    fila_e.append(utils.float2str(0.0))
            fila_m.append(utils.float2str(total_m))
            fila_kg.append(utils.float2str(total_kg))
            fila_e.append(utils.float2str(total_e))
            model.append(fila_m + ["The girl"])
            model.append(fila_kg + ["I used"])
            model.append(fila_e + ["to love"])

    def rellenar_tabla_produccion_gtx(self, produccion_gtx):
        """
        Recibe un diccionario con la producción en A y B de geotextiles por 
        meses e introduce esa información en el treeview.
        """
        model = self.wids['tv_produccion_gtx'].get_model()
        model.clear()
        fila_metros = ["Total m²"]
        fila_kilos = ["Total kg teóricos"]
        fila_kilos_reales = ["Total kg reales sin embalaje"]
        fila_merma = ["Merma", ]
        fila_porciento_merma = ["% merma", ]
        fila_gramaje_medio = ["Gramaje medio"]
        fila_metros_b = ["m² rollos defectuosos"]
        fila_kilos_b = ["kg rollos defectuosos"]
        fila_kilos_hora = ["Kilos (reales s.e.)/hora"]
        fila_horas = ["Horas de trabajo"]
        fila_horas_produccion = ["Horas de producción"]
        fila_dias = ["Días de trabajo"]
        fila_turnos = ["Turnos / día"]
        fila_empleados = ["Trabajadores / día"]
        fila_productividad = ["Productividad"]
        fila_gtxc = ["Kg C (no computa en global)"]
        metros_totales = 0.0
        kilos_totales = 0.0
        metros_b_totales = 0.0
        kilos_b_totales = 0.0
        merma_total = 0.0
        kilos_consumidos_totales = 0.0
        kilos_reales_sin_embalaje_total = 0.0
        kilos_gtxc = 0.0
        for mes in xrange(12):
        #for mes in produccion_gtx:
            metros_totales_mes = produccion_gtx[mes]['A']['metros'] + produccion_gtx[mes]['B']['metros']
            metros_totales += metros_totales_mes
            fila_metros.append(utils.float2str(metros_totales_mes))
            
            kilos_totales_mes = produccion_gtx[mes]['A']['kilos'] + produccion_gtx[mes]['B']['kilos']
            kilos_totales += kilos_totales_mes
            fila_kilos.append(utils.float2str(kilos_totales_mes))
            
            fila_kilos_reales.append(utils.float2str(produccion_gtx[mes]['kilos_a_mas_b_sin_embalaje'])) 
            kilos_reales_sin_embalaje_total += produccion_gtx[mes]['kilos_a_mas_b_sin_embalaje']

            metros_b_mes = produccion_gtx[mes]['B']['metros']
            fila_metros_b.append(utils.float2str(metros_b_mes))
            metros_b_totales += metros_b_mes
            
            kilos_b_mes = produccion_gtx[mes]['B']['kilos']
            fila_kilos_b.append(utils.float2str(kilos_b_mes))
            kilos_b_totales += kilos_b_mes

            try:
                gramaje_medio = (kilos_totales_mes / metros_totales_mes) * 1000
            except ZeroDivisionError:
                gramaje_medio = 0
            fila_gramaje_medio.append(utils.float2str(gramaje_medio, 4, autodec = True))

            kilos_fibra = produccion_gtx[mes]['consumo']
            kilos_consumidos_totales += kilos_fibra
            merma = kilos_fibra - kilos_totales_mes
            merma_total += merma
            fila_merma.append(utils.float2str(merma))
            try:
                porc_merma = (1.0 - (kilos_totales_mes / kilos_fibra)) * 100.0
            except ZeroDivisionError:
                porc_merma = 0.0
            fila_porciento_merma.append("%s %%" % (utils.float2str(porc_merma, 3, autodec = True)))
            fila_kilos_hora.append(utils.float2str(produccion_gtx[mes]['kilos_hora']))
            fila_horas.append(utils.float2str(produccion_gtx[mes]['horas'], autodec = True))
            fila_horas_produccion.append(utils.float2str(produccion_gtx[mes]['horas_produccion'], autodec = True))
            fila_dias.append("%d" % (produccion_gtx[mes]['dias']))
            fila_turnos.append(utils.float2str(produccion_gtx[mes]['turnos']))
            fila_empleados.append(utils.float2str(produccion_gtx[mes]['empleados'], autodec = True))
            fila_productividad.append("%s %%" % (utils.float2str(produccion_gtx[mes]['productividad'] * 100.0)))
            gtxc = produccion_gtx[mes]["gtxc"]
            fila_gtxc.append(utils.float2str(gtxc))
            kilos_gtxc += gtxc
        # Totales:
        fila_metros.append(utils.float2str(metros_totales))
        fila_kilos.append(utils.float2str(kilos_totales))
        fila_kilos_reales.append(utils.float2str(kilos_reales_sin_embalaje_total))
        try:
            fila_gramaje_medio.append(utils.float2str((kilos_totales / metros_totales) * 1000, 4, autodec = True))
        except ZeroDivisionError:
            fila_gramaje_medio.append(utils.float2str(0.0))
        fila_metros_b.append(utils.float2str(metros_b_totales))
        fila_kilos_b.append(utils.float2str(kilos_b_totales))
        fila_merma.append(utils.float2str(merma_total))
        try:
            porc_merma_total = (1.0 - (kilos_totales / kilos_consumidos_totales)) * 100.0
        except ZeroDivisionError:
            porc_merma_total = 0.0
        fila_porciento_merma.append("%s %%" % (utils.float2str(porc_merma_total, 3, autodec = True)))
        avg = lambda l: (1.0 * sum(l)) / len(l)
        fila_kilos_hora.append(utils.float2str(avg([produccion_gtx[mes]['kilos_hora'] for mes in produccion_gtx])))
        fila_horas.append(utils.float2str(sum([produccion_gtx[mes]['horas'] for mes in produccion_gtx])))
        fila_horas_produccion.append(utils.float2str(sum([produccion_gtx[mes]['horas_produccion'] for mes in produccion_gtx])))
        fila_dias.append("%d" % (sum([produccion_gtx[mes]['dias'] for mes in produccion_gtx])))
        fila_turnos.append("%s" % utils.float2str(avg([produccion_gtx[mes]['turnos'] for mes in produccion_gtx])))
        fila_empleados.append("%s" % utils.float2str(avg([produccion_gtx[mes]['empleados'] for mes in produccion_gtx])))
        fila_productividad.append("%s %%" % utils.float2str(avg([produccion_gtx[mes]['productividad'] for mes in produccion_gtx]) * 100.0))
        fila_gtxc.append(utils.float2str(kilos_gtxc))
        # ... al model:
        model.append(fila_metros + ["Love"])
        model.append(fila_kilos + ["reign"])
        model.append(fila_kilos_reales + ["... like a Rolling Stone"])
        model.append(fila_merma + ["o'er"])
        model.append(fila_porciento_merma + ["me"])
        model.append(fila_gramaje_medio + ["reign"])
        model.append(fila_kilos_hora + ["o'er"])
        model.append(fila_metros_b + ["me"])
        model.append(fila_kilos_b + ["... Only love..."])
        model.append(fila_productividad + ["... can make it rain..."])
        model.append(fila_dias + ["... the way the beach..."])
        model.append(fila_horas + ["... is kissed by the sea..."])
        model.append(fila_horas_produccion + ["... ojete moreno..."])
        model.append(fila_turnos + ["... like the sweat of lovers..."])
        model.append(fila_empleados + ["... laying in the fields..."])
        model.append(fila_gtxc + ["Looooooooooooove"])

    def construir_treeview_ficticio(self):
        """
        Construye un TreeView con un ListModel como modelo con 
        las mismas columnas que los TreeViews de la ventana.
        """
        tv = gtk.TreeView()
        tv.set_name("Resumen global")
        cols = (('', 'gobject.TYPE_STRING', False, True, True, None),
                ('Enero', 'gobject.TYPE_STRING', False, False, False, None), 
                ('Febrero', 'gobject.TYPE_STRING', False, False, False, None), 
                ('Marzo', 'gobject.TYPE_STRING', False, False, False, None),
                ('Abril', 'gobject.TYPE_STRING', False, False, False, None),
                ('Mayo', 'gobject.TYPE_STRING', False, False, False, None), 
                ('Junio', 'gobject.TYPE_STRING', False, False, False, None), 
                ('Julio', 'gobject.TYPE_STRING', False, False, False, None), 
                ('Agosto', 'gobject.TYPE_STRING', False, False, False, None), 
                ('Septiembre', 'gobject.TYPE_STRING', False, False, False, None), 
                ('Octubre', 'gobject.TYPE_STRING', False, False, False, None), 
                ('Noviembre', 'gobject.TYPE_STRING', False, False, False, None), 
                ('Diciembre', 'gobject.TYPE_STRING', False, False, False, None), 
                ('Anual', 'gobject.TYPE_STRING', False, False, False, None), 
                ('Rocío', 'gobject.TYPE_STRING', False, False, False, None))
        utils.preparar_listview(tv, cols)
        for col in tv.get_columns()[1:]:
            for cell in col.get_cell_renderers():
                cell.set_property("xalign", 1.0)
            col.set_alignment(0.5)
        return tv

    def unificar_tv(self):
        """
        Construye un único TreeView con la información de los 6 mostrados en 
        pantalla listo para pasarlo a treeview2*.
        """
        tv = self.construir_treeview_ficticio()
        model = tv.get_model()
        for nombretvorig, encabezado in (
                    ("tv_produccion_gtx", "Producción geotextiles"), 
                    ("tv_ventas_gtx", "Ventas geotextiles"), 
                    ("tv_consumos_gtx", "Consumos geotextiles"), 
                    ("tv_produccion_fibra", "Producción fibra"), 
                    ("tv_ventas_fibra", "Ventas fibra"), 
                    ("tv_consumos_fibra", "Consumos fibra"), 
                    ("tv_produccion_bolsas", "Producción fibra embolsada"), 
                    ("tv_ventas_bolsas", "Ventas fibra embolsada"), 
                    ("tv_consumos_bolsas", "Consumos fibra embolsada"), 
                    ("tv_compras_geocompuestos", "Compras comercializados"), 
                    ("tv_ventas_geocompuestos", "Ventas comercializados")):
            tvorig = self.wids[nombretvorig]
            modelorig = tvorig.get_model()
            model.append(["===", encabezado] + ["==="] * 13)
            for filaorig in modelorig:
                fila = []
                for i in xrange(modelorig.get_n_columns()):
                    fila.append(filaorig[i])
                model.append(fila)
                for filahija in filaorig.iterchildren():
                    fila = [" > " + filahija[0]]
                    for i in xrange(1, modelorig.get_n_columns()):
                        fila.append(filahija[i])
                    model.append(fila)
            model.append(["---"] * 15)
        return tv

    def imprimir(self, boton):
        """
        Imprime el contenido de todos los TreeViews en un solo PDF apaisado.
        """
        tv = self.unificar_tv()
        from informes.treeview2pdf import treeview2pdf
        from formularios.reports import abrir_pdf
        strfecha = "%s - %s" % (utils.str_fecha(mx.DateTime.localtime()), 
                                utils.str_hora(mx.DateTime.localtime()))
        abrir_pdf(treeview2pdf(tv, 
            titulo="Resumen global por meses: Producción - Ventas - Consumos",
            fecha = strfecha, 
            apaisado = True))

    def exportar(self, boton):
        """
        Vuelva el contenido de todos los TreeViews en un solo ".csv".
        """
        tv = self.unificar_tv()
        from informes.treeview2csv import treeview2csv
        from formularios.reports import abrir_csv
        nomarchivocsv = treeview2csv(tv)
        abrir_csv(nomarchivocsv)


########################## P R O D U C C I Ó N   G E O T E X T I L E S ########
def calcular_productividad_conjunta(pdps):
    """
    Devuelve la productividad de una lista de objetos parte.
    Se calcula como:
    sumatorio(tiempos reales trabajados) / sumatorio(duraciones totales)
    donde el tiempo real trabajado de cada parte es la duración del parte 
    menos el sumatorio de las duraciones de las incidencias del mismo.
    """
    durpartes = 0.0
    hts = 0.0
    for pdp in pdps:
        durpartes += pdp.get_duracion()
        try:
            hts += pdp.get_horas_trabajadas()
        except AssertionError, msg:
            txt = "consulta_global::calcular_productividad_conjunta -> "\
                  "El parte ID %d tiene una duración inferior a la suma de "\
                  "sus incidencias. No se tendrán en cuenta las horas "\
                  "trabajadas del mismo. AssertionError: %s" % (pdp.id, msg)
            print txt
    try:
        res = hts / durpartes
    except ZeroDivisionError:
        res = 0.0
    return res

def consultar_metros_y_kilos_gtx(fechaini, fechafin):
    """
    Recibe 2 mx.DateTime con las fechas inicial y final de la 
    consulta de metros y kilos.
    Devuelve los metros de A, kilos de A, metros de B y kilos de B; en este 
    orden.
    Cuenta los productos fabricados en los partes sin tener en cuenta que la 
    partida de carga se haya consumido por completo o no. Puede tener 
    diferencias con la consulta de consumo de fibra por partida de geotextiles,
    que discrimina las partidas según su partida de carga (si la partida de 
    carga no entra en las fechas consultadas, ninguna de sus partidas de 
    geotextiles entrará tampoco).  
    OJO: Ataca directamente a la BD con SQL. No es portable (aunque 
    a estas alturas cualquiera se atreve a cambiar de SGBD).
    (Ver metros_y_kilos_gtx.sql)
    """
    con = pclases.Rollo._connection
    partes_gtx_temp = """SELECT id
                          INTO TEMP partes_gtx_temp
                          FROM parte_de_produccion 
                          WHERE (fecha >= '%s'
                                 AND fecha <= '%s'
                                 AND observaciones NOT LIKE '%%;%%;%%;%%;%%;%%'
                                 AND partida_cem_id IS NULL);
    """ % (fechaini.strftime("%Y-%m-%d"), fechafin.strftime("%Y-%m-%d"))
    producto_venta_con_campos_especificos_temp = """
    SELECT pv.id AS producto_venta_id, 
           peso_embalaje, 
           metros_lineales, 
           ancho, 
           metros_lineales * ancho AS metros_cuadrados, 
           gramos AS gramaje, 
           (metros_lineales * ancho * gramos) / 1000 AS peso_teorico
    INTO TEMP producto_venta_con_campos_especificos_temp
    FROM campos_especificos_rollo cer, producto_venta pv
    WHERE (pv.campos_especificos_rollo_id = cer.id);
    """
    articulos_rollo_fabricados_temp = """
    SELECT id, rollo_id, rollo_defectuoso_id, peso_embalaje, pv.producto_venta_id
     INTO TEMP articulos_rollo_fabricados_temp
     FROM articulo a, producto_venta_con_campos_especificos_temp pv
     WHERE parte_de_produccion_id IN (SELECT id FROM partes_gtx_temp) 
            AND (rollo_id IS NOT NULL
                 OR rollo_defectuoso_id IS NOT NULL)
            AND a.producto_venta_id = pv.producto_venta_id;
    """
    articulos_rollo_b_temp = """
    SELECT id, peso - peso_embalaje AS peso_se, ancho * metros_lineales AS metros_cuadrados
     INTO TEMP articulos_rollo_b_temp
     FROM rollo_defectuoso
     WHERE id IN (SELECT rollo_defectuoso_id 
                   FROM articulo 
                   WHERE parte_de_produccion_id IN (SELECT id FROM partes_gtx_temp)
                         AND rollo_defectuoso_id IS NOT NULL);
    """
    pesos_rollos_temp = """
    SELECT peso AS peso_ce, peso_embalaje AS peso_e, peso - peso_embalaje AS peso_se
     INTO TEMP pesos_rollos_temp
     FROM rollo r, articulos_rollo_fabricados_temp
     WHERE r.id = articulos_rollo_fabricados_temp.rollo_id;
    """
    rollos_a_y_producto_venta_temp = """
    SELECT COUNT(rollo_id) AS rollos_a, producto_venta_id 
     INTO TEMP rollos_a_y_producto_venta_temp
     FROM articulos_rollo_fabricados_temp 
     GROUP BY producto_venta_id;
    """
    con.query(partes_gtx_temp)
    con.query(producto_venta_con_campos_especificos_temp)
    con.query(articulos_rollo_fabricados_temp)
    con.query(articulos_rollo_b_temp)
    con.query(pesos_rollos_temp)
    con.query(rollos_a_y_producto_venta_temp)
    metroskilosa = con.queryAll("""
    SELECT SUM(rollos_a * metros_cuadrados) AS metros_a, 
           SUM(rollos_a * peso_teorico) AS kilos_a 
     FROM rollos_a_y_producto_venta_temp raypvt, 
          producto_venta_con_campos_especificos_temp pvccet 
     WHERE raypvt.producto_venta_id = pvccet.producto_venta_id; 
    """)
    metros_a, kilos_a = metroskilosa[0]
    metroskilosb = con.queryAll("""
    SELECT SUM(metros_cuadrados) AS metros_b, SUM(peso_se) AS kilos_b   --
     FROM articulos_rollo_b_temp;          
    """)
    metros_b, kilos_b = metroskilosb[0]
    caidita_de_roma = """
    DROP TABLE rollos_a_y_producto_venta_temp;
    DROP TABLE pesos_rollos_temp;
    DROP TABLE articulos_rollo_b_temp;
    DROP TABLE articulos_rollo_fabricados_temp;
    DROP TABLE producto_venta_con_campos_especificos_temp;
    DROP TABLE partes_gtx_temp;
    """
    con.query(caidita_de_roma)
    return (metros_a != None and metros_a or 0.0, 
            kilos_a != None and kilos_a or 0.0, 
            metros_b != None and metros_b or 0.0, 
            kilos_b != None and kilos_b or 0.0)

def consultar_bolsas_y_kilos(fechaini, fechafin):
    """
    Recibe 2 mx.DateTime con las fechas inicial y final de la 
    consulta de bolsas y kilos.
    Devuelve los bolsas de A, kilos de A, bolsas de B y kilos de B; en este 
    orden.
    OJO: Ataca directamente a la BD con SQL. No es portable (aunque 
    a estas alturas cualquiera se atreve a cambiar de SGBD).
    """
    con = pclases.Caja._connection
    sqlbase = """
        SELECT SUM(caja.numbolsas), SUM(caja.peso) 
          FROM caja, articulo, parte_de_produccion
         WHERE caja.id = articulo.caja_id 
           AND articulo.parte_de_produccion_id = parte_de_produccion.id 
           AND parte_de_produccion.fecha >= '%s'
           AND parte_de_produccion.fecha <= '%s'
    """ % (fechaini.strftime("%Y-%m-%d"), fechafin.strftime("%Y-%m-%d"))
    if pclases.DEBUG:
        bolsas, kilos = con.queryOne(sqlbase)
    bolsas_a, kilos_a = con.queryOne(sqlbase 
                                    + " AND NOT caja_es_clase_b(caja.id)")
    bolsas_b, kilos_b = con.queryOne(sqlbase + " AND caja_es_clase_b(caja.id)")
    if pclases.DEBUG:
        kilos = kilos != None and kilos or 0.0 
        bolsas = bolsas != None and bolsas or 0
    bolsas_a = bolsas_a != None and bolsas_a or 0
    kilos_a = kilos_a != None and kilos_a or 0.0 
    bolsas_b = bolsas_b != None and bolsas_b or 0
    kilos_b = kilos_b != None and kilos_b or 0.0
    if pclases.DEBUG:
        assert bolsas_a + bolsas_b == bolsas, \
               "consulta_global.py::consultar_bolsas_y_kilos -> "\
               "Suma de bolsas A + B diferente a bolsas totales: %s" % (
                (bolsas_a, bolsas_b, bolsas), )
        assert round(kilos_a + kilos_b, 2) == round(kilos, 2), \
               "consulta_global.py::consultar_bolsas_y_kilos -> "\
               "Suma de kilos A + B diferente a kilos totales: %s" % (
                (kilos_a, kilos_b, kilos), )
    return bolsas_a, kilos_a, bolsas_b, kilos_b

def consultar_kilos_bigbags_consumidos(fechaini, fechafin):
    """
    Devuelve los kilos de fibra consumidos en forma de bigbag por los partes 
    de producción de fibra de cemento.
    OJO: Se considera que un parte de producción consume un bigbag completo 
    aunque realmente no se haya gastado completo y se termine en el parte 
    siguiente.
    """
    con = pclases.ParteDeProduccion._connection
    sql = """
    SELECT SUM(bigbag.pesobigbag)
      FROM bigbag, parte_de_produccion
     WHERE bigbag.parte_de_produccion_id = parte_de_produccion.id 
       AND parte_de_produccion.fecha >= '%s' 
       AND parte_de_produccion.fecha <= '%s'
       AND parte_de_produccion.partida_cem_id IS NOT NULL
    """ % (fechaini.strftime("%Y-%m-%d"), fechafin.strftime("%Y-%m-%d"))
    kilos = con.queryOne(sql)[0]
    kilos = kilos != None and kilos or 0.0
    return kilos

def consultar_kilos_fibra_consumidos(fechaini, fechafin):
    """
    Recibe 2 mx.DateTime con las fechas inicial y final de la 
    consulta de metros y kilos.
    Devuelve los kilos de fibra consumidos según el criterio de 
    que una partida de carga no se considera consumida por completo 
    si todas sus partidas no se han fabricado antes de fechafin.
    OJO: Ataca directamente a la BD con SQL. No es portable (aunque 
    a estas alturas cualquiera se atreve a cambiar de SGBD).
    (Ver metros_y_kilos_gtx.sql)
    """
    con = pclases.Rollo._connection
    # Consultas a pelo
    partes_gtx = """
        SELECT id
         INTO TEMP partes_gtx_temp
         FROM parte_de_produccion 
         WHERE (fecha >= '%s'                     -- Parámetro fecha ini
                AND fecha <= '%s'                 -- Parámetro fecha fin
                AND observaciones NOT LIKE '%%;%%;%%;%%;%%;%%'
                AND partida_cem_id IS NULL); 
    """ % (fechaini.strftime("%Y-%m-%d"), fechafin.strftime("%Y-%m-%d"))
    rollos_fab = """
        SELECT rollo_id, rollo_defectuoso_id
         INTO TEMP articulos_rollo_fabricados_temp
         FROM articulo
         WHERE parte_de_produccion_id IN (SELECT id FROM partes_gtx_temp);
    """
    partidas_rollos_def = """
        SELECT partida_id 
         INTO TEMP partidas_rollos_defectuosos_temp 
         FROM rollo_defectuoso rd
         WHERE rd.id IN (SELECT rollo_defectuoso_id FROM articulos_rollo_fabricados_temp)
         GROUP BY partida_id;
    """
    partidas_rollos = """
        SELECT partida_id 
         INTO TEMP partidas_rollos_temp 
         FROM rollo r
         WHERE r.id IN (SELECT rollo_id FROM articulos_rollo_fabricados_temp)
         GROUP BY partida_id;
    """
    func_partes_de_partida = """
        CREATE OR REPLACE FUNCTION partes_de_partida (INTEGER) RETURNS BIGINT
        AS '
            SELECT COUNT(id)
            FROM parte_de_produccion 
            WHERE id IN (SELECT parte_de_produccion_id
                         FROM articulo 
                         WHERE rollo_id IS NOT NULL AND rollo_id IN (SELECT id 
                                                                     FROM rollo 
                                                                     WHERE partida_id = $1) 
                            OR rollo_defectuoso_id IS NOT NULL AND rollo_defectuoso_id IN (SELECT id 
                                                                                           FROM rollo_defectuoso 
                                                                                           WHERE partida_id = $1) 
                        GROUP BY parte_de_produccion_id)
            ;
        ' LANGUAGE 'sql';
    """
    func_partes_antes_de = """
        CREATE OR REPLACE FUNCTION partes_de_partida_antes_de_fecha (INTEGER, DATE) RETURNS BIGINT
        AS '
            SELECT COUNT(id) 
             FROM parte_de_produccion 
             WHERE fecha <= $2
                AND id IN (SELECT parte_de_produccion_id
                             FROM articulo 
                             WHERE rollo_id IS NOT NULL AND rollo_id IN (SELECT id 
                                                                         FROM rollo 
                                                                         WHERE partida_id = $1) 
                                OR rollo_defectuoso_id IS NOT NULL AND rollo_defectuoso_id IN (SELECT id 
                                                                                               FROM rollo_defectuoso 
                                                                                               WHERE partida_id = $1)
                            GROUP BY parte_de_produccion_id) 
             ;
        ' LANGUAGE 'sql';
    """
    func_partida_entra = """
        CREATE OR REPLACE FUNCTION partida_entra_en_fecha(INTEGER, DATE) RETURNS BOOLEAN 
            -- Recibe un ID de partida de geotextiles y una fecha. Devuelve TRUE si ningún 
            -- parte de producción de la partida tiene fecha posterior a la recibida Y la 
            -- partida existe y tiene producción.
        AS '
            SELECT partes_de_partida($1) > 0 AND partes_de_partida($1) = partes_de_partida_antes_de_fecha($1, $2);
        ' LANGUAGE 'sql';
    """
    func_pc_entra = """ 
        CREATE OR REPLACE FUNCTION partida_carga_entra_en_fecha(INTEGER, DATE) RETURNS BOOLEAN 
            -- Recibe el ID de una partida de carga y devuelve TRUE si todas las partidas 
            -- de geotextiles de la misma pertenecen a partes de producción de fecha anterior 
            -- o igual al segundo parámetro.
        AS' 
            SELECT COUNT(*) > 0 
            FROM partida
            WHERE partida_carga_id = $1 
                  AND partida_entra_en_fecha(partida.id, $2);
        ' LANGUAGE 'sql';
    """
    partidas_carga_id = """        
        SELECT partida_carga_id
         INTO TEMP partidas_carga_id_temp
         FROM partida
         WHERE (id IN (SELECT partida_id FROM partidas_rollos_defectuosos_temp)
                OR id IN (SELECT partida_id FROM partidas_rollos_temp)) 
         GROUP BY partida_carga_id;
    """
    partidas_de_pc_en_fecha = """
        SELECT partida_carga_id 
         INTO TEMP partidas_de_carga_de_partidas_en_fecha_temp
         FROM partidas_carga_id_temp
         WHERE partida_carga_entra_en_fecha(partida_carga_id, '%s');       -- Parámetro fecha fin
    """ % (fechafin.strftime("%Y-%m-%d"))
    balas_y_peso = """
        SELECT id, AVG(pesobala) AS _pesobala    -- Si sale una bala más de una vez, la media dará el mismo peso de la bala en sí.
         INTO TEMP balas_con_peso_de_partida_de_carga 
         FROM bala 
         WHERE partida_carga_id IN (SELECT partida_carga_id 
                                    FROM partidas_de_carga_de_partidas_en_fecha_temp)
         GROUP BY id; 
        -- OJO: Las balas llevan en torno a kilo o kilo y medio de plástico de embalar que se cuenta como fibra consumida.
    """
    total_balas_y_peso = """
        SELECT COUNT(id) AS balas, SUM(_pesobala) AS peso_ce
         FROM balas_con_peso_de_partida_de_carga;
    """
    con.query(partes_gtx) 
    con.query(rollos_fab)
    con.query(partidas_rollos_def)
    con.query(partidas_rollos)
    con.query(func_partes_de_partida)
    con.query(func_partes_antes_de)
    con.query(func_partida_entra)
    con.query(func_pc_entra)
    con.query(partidas_carga_id)
    con.query(partidas_de_pc_en_fecha)
    con.query(balas_y_peso)

    balas_kilos = con.queryAll(total_balas_y_peso)
    caidita_de_roma = """
        DROP FUNCTION partes_de_partida(INTEGER);
        DROP FUNCTION partes_de_partida_antes_de_fecha(INTEGER, DATE);
        DROP FUNCTION partida_entra_en_fecha(INTEGER, DATE);
        DROP FUNCTION partida_carga_entra_en_fecha(INTEGER, DATE);
        DROP TABLE partidas_carga_id_temp;
        DROP TABLE balas_con_peso_de_partida_de_carga;
        DROP TABLE partidas_de_carga_de_partidas_en_fecha_temp;
        DROP TABLE partidas_rollos_defectuosos_temp;
        DROP TABLE partidas_rollos_temp;
        DROP TABLE articulos_rollo_fabricados_temp;
        DROP TABLE partes_gtx_temp;
    """
    con.query(caidita_de_roma)
    balas, kilos = balas_kilos[0]  # @UnusedVariable
    return (kilos and kilos or 0.0)

def consultar_horas_reales_gtx(fechaini, fechafin):
    """
    Devuelve la suma de las duraciones de los partes entre las dos 
    fechas recibidas.
    """
    sql = """
        SELECT SUM(fechahorafin - fechahorainicio)
         FROM parte_de_produccion 
         WHERE (fecha >= '%s'                     -- Parámetro fecha ini
                AND fecha <= '%s'                 -- Parámetro fecha fin
                AND observaciones NOT LIKE '%%;%%;%%;%%;%%;%%'
                AND partida_cem_id IS NULL); 
    """ % (fechaini.strftime("%Y-%m-%d"), fechafin.strftime("%Y-%m-%d"))
    try:
        horas_sql = pclases.ParteDeProduccion._queryAll(sql)[0][0]  # @UndefinedVariable
        try:
            horas = horas_sql.hours
        except AttributeError:  # Es un datetime.timedelta
            horas = (horas_sql.days * 24.0) + (horas_sql.seconds / 3600.0)
    except (IndexError, AttributeError):
        horas = 0.0
    return horas

def consultar_horas_reales_bolsas(fechaini, fechafin):
    """
    Devuelve la suma de las duraciones de los partes entre las dos 
    fechas recibidas.
    """
    sql = """
        SELECT SUM(fechahorafin - fechahorainicio)
         FROM parte_de_produccion 
         WHERE (fecha >= '%s'                     -- Parámetro fecha ini
                AND fecha <= '%s'                 -- Parámetro fecha fin
                AND partida_cem_id IS NOT NULL); 
    """ % (fechaini.strftime("%Y-%m-%d"), fechafin.strftime("%Y-%m-%d"))
    try:
        horas_sql = pclases.ParteDeProduccion._queryAll(sql)[0][0]  # @UndefinedVariable
        try:
            horas = horas_sql.hours
        except AttributeError:  # Es un datetime.timedelta
            horas = (horas_sql.days * 24.0) + (horas_sql.seconds / 3600.0)
    except (IndexError, AttributeError):
        horas = 0.0
    return horas

def consultar_horas_trabajo_bolsas(fechaini, fechafin, logger = None):
    """
    Devuelve la suma de las duraciones de los partes entre las dos 
    fechas recibidas menos las horas de parada.
    """
    partes = pclases.ParteDeProduccion.select(""" 
        fecha >= '%s' 
        AND fecha <= '%s' 
        AND partida_cem_id IS NOT NULL
        """ % (fechaini.strftime("%Y-%m-%d"), fechafin.strftime("%Y-%m-%d")))
    try:
        horas_trabajadas = sum([pdp.get_horas_trabajadas() for pdp in partes])
    except AssertionError, msg:
        txt = "consulta_global::consultar_horas_trabajo_bolsas -> "\
              "Error calculando horas de trabajo de línea de geotextiles: %s."\
              " Ignoro todos los partes implicados en el mismo rango de "\
              "fechas del que provoca el error." % (msg)
        print txt
        if logger != None:
            logger.error(txt)
        horas_trabajadas = mx.DateTime.DateTimeDelta(0)
    try:
        horas_trabajadas = horas_trabajadas.hours
    except AttributeError:
        try:    # Es un datetime.timedelta
            horas_trabajadas = ((horas_trabajadas.days * 24.0) 
                                + (horas_trabajadas.seconds / 3600.0))
        except AttributeError:
            horas_trabajadas = 0.0
    return horas_trabajadas

def consultar_horas_trabajo_gtx(fechaini, fechafin, logger = None):
    """
    Devuelve la suma de las duraciones de los partes entre las dos 
    fechas recibidas menos las horas de parada.
    """
    partes = pclases.ParteDeProduccion.select(""" 
                fecha >= '%s' 
                AND fecha <= '%s' 
                AND observaciones NOT LIKE '%%;%%;%%;%%;%%;%%'
                AND partida_cem_id IS NULL
                """ % (fechaini.strftime("%Y-%m-%d"), 
                       fechafin.strftime("%Y-%m-%d")))
    try:
        horas_trabajadas = sum([pdp.get_horas_trabajadas() for pdp in partes])
    except AssertionError, msg:
        txt = "consulta_global::consultar_horas_trabajo_gtx -> Error calculando horas de trabajo de línea de geotextiles: %s. Ignoro todos los partes implicados en el mismo rango de fechas del que provoca el error." % (msg)
        print txt
        if logger != None:
            logger.error(txt)
        horas_trabajadas = mx.DateTime.DateTimeDelta(0)
    try:
        horas_trabajadas = horas_trabajadas.hours
    except AttributeError:
        try:    # Es un datetime.timedelta
            horas_trabajadas = ((horas_trabajadas.days * 24.0) 
                                + (horas_trabajadas.seconds / 3600.0))
        except AttributeError:
            horas_trabajadas = 0.0
    return horas_trabajadas

def consultar_dias_gtx(fechaini, fechafin):
    """
    Devuelve el número de días (fechas distintas) en los que hay 
    al menos un parte de producción de geotextiles entre las fechas 
    recibidas.
    """ 
    sql = """ 
        SELECT COUNT(DISTINCT fecha) 
         FROM parte_de_produccion
         WHERE (fecha >= '%s'                     -- Parámetro fecha ini
                AND fecha <= '%s'                 -- Parámetro fecha fin
                AND observaciones NOT LIKE '%%;%%;%%;%%;%%;%%'
                AND partida_cem_id IS NULL); 
    """ % (fechaini.strftime("%Y-%m-%d"), fechafin.strftime("%Y-%m-%d"))
    try:
        dias = pclases.ParteDeProduccion._queryAll(sql)[0][0]  # @UndefinedVariable
    except IndexError:
        dias = 0
    return dias

def consultar_productividad_gtx(fechaini, fechafin):
    """
    Devuelve la productividad de los partes de producción de 
    geotextiles entre las fechas recibidas.
    """ 
    sql_where = """ fecha >= '%s' AND fecha <= '%s' AND observaciones NOT LIKE '%%;%%;%%;%%;%%;%%' AND partida_cem_id IS NULL """ % (
        fechaini.strftime("%Y-%m-%d"), fechafin.strftime("%Y-%m-%d"))
    pdps = pclases.ParteDeProduccion.select(sql_where)
    return calcular_productividad_conjunta(pdps)

def consultar_productividad_bolsas(fechaini, fechafin):
    """
    Devuelve la productividad de los partes de producción de 
    embolsado entre las fechas recibidas.
    """ 
    sql_where=" fecha >= '%s' AND fecha <= '%s' AND partida_cem_id IS NULL "%(
        fechaini.strftime("%Y-%m-%d"), fechafin.strftime("%Y-%m-%d"))
    pdps = pclases.ParteDeProduccion.select(sql_where)
    return calcular_productividad_conjunta(pdps)

def consultar_empleados_por_dia_bolsas(fechaini, fechafin):
    """
    Devuelve el número de empleados por día a través de una tocho-consulta(TM) 
    a la base de datos.
    """
    sql = """
    SELECT fecha, empleadoid 
    FROM parte_de_produccion_empleado, 
        (SELECT id, fecha 
           FROM parte_de_produccion 
          WHERE fecha >= '%s' 
            AND fecha <= '%s' 
            AND partida_cem_id IS NOT NULL) AS partes 
    WHERE partes.id = parte_de_produccion_empleado.partedeproduccionid 
    GROUP BY fecha, empleadoid ORDER BY fecha; """ % (
        fechaini.strftime("%Y-%m-%d"), fechafin.strftime("%Y-%m-%d"))
    filas_fecha_idempleado=pclases.ParteDeProduccion._queryAll(sql)  # @UndefinedVariable
    # Y ahora sumo (lo sé, se podría hacer directamente en la consulta, pero 
    # prefiero dejarla así porque creo que me hará falta en un futuro tenerlo 
    # desglosado).
    fechas = []
    empleados = 0.0
    for fecha, idempleado in filas_fecha_idempleado:  # @UnusedVariable
        if fecha not in fechas:
            fechas.append(fecha)
        empleados += 1
    try:
        res = empleados / len(fechas)
    except ZeroDivisionError:
        res = 0.0
    return res

def consultar_empleados_por_dia_gtx(fechaini, fechafin):
    """
    Devuelve el número de empleados por día a través de una tocho-consulta(TM) 
    a la base de datos.
    """
    sql = """
    SELECT fecha, empleadoid 
    FROM parte_de_produccion_empleado, (SELECT id, fecha 
                                        FROM parte_de_produccion 
                                        WHERE fecha >= '%s' 
                                          AND fecha <= '%s' 
                                          AND observaciones NOT LIKE '%%;%%;%%;%%;%%;%%' AND partida_cem_id IS NULL) AS partes 
    WHERE partes.id = parte_de_produccion_empleado.partedeproduccionid GROUP BY fecha, empleadoid ORDER BY fecha; """ % (
        fechaini.strftime("%Y-%m-%d"), fechafin.strftime("%Y-%m-%d"))
    filas_fecha_idempleado = pclases.ParteDeProduccion._queryAll(sql)  # @UndefinedVariable
    # Y ahora sumo (lo sé, se podría hacer directamente en la consulta, pero 
    # prefiero dejarla así porque creo que me hará falta en un futuro tenerlo desglosado).
    fechas = []
    empleados = 0.0
    for fecha, idempleado in filas_fecha_idempleado:  # @UnusedVariable
        if fecha not in fechas:
            fechas.append(fecha)
        empleados += 1
    try:
        res = empleados / len(fechas)
    except ZeroDivisionError:
        res = 0.0
    return res

def buscar_kilos_reales_gtx_producidos_sin_embalaje(fechaini, fechafin):
    """
    Devuelve los kilos reales con embalaje fabricados en los partes de 
    geotextiles entre las dos fechas recibidas.
    Incluye rollos y rollos defectuosos.
    """
    res = 0.0
    sqlfechaini = fechaini.strftime("%Y-%m-%d")
    sqlfechafin = fechafin.strftime("%Y-%m-%d")
    PDP = pclases.ParteDeProduccion
    peso_sin_rollos = PDP._queryOne("""SELECT SUM(rollo.peso - campos_especificos_rollo.peso_embalaje) 
                                                  FROM rollo, articulo, producto_venta, campos_especificos_rollo, parte_de_produccion 
                                                  WHERE articulo.producto_venta_id = producto_venta.id
                                                    AND producto_venta.campos_especificos_rollo_id = campos_especificos_rollo.id 
                                                    AND articulo.rollo_id = rollo.id 
                                                    AND articulo.parte_de_produccion_id = parte_de_produccion.id 
                                                    AND parte_de_produccion.fecha >= '%s' 
                                                    AND parte_de_produccion.fecha <= '%s' ;
                                                """ % (sqlfechaini, sqlfechafin))
    total_peso_sin_rollos = peso_sin_rollos[0]
    if total_peso_sin_rollos != None:
        res += total_peso_sin_rollos
    peso_sin_rollos_d = PDP._queryOne("""
        SELECT SUM(rollo_defectuoso.peso - rollo_defectuoso.peso_embalaje) 
          FROM rollo_defectuoso, articulo, parte_de_produccion 
         WHERE articulo.rollo_defectuoso_id = rollo_defectuoso.id 
           AND articulo.parte_de_produccion_id = parte_de_produccion.id 
           AND parte_de_produccion.fecha >= '%s' 
           AND parte_de_produccion.fecha <= '%s' ;
    """ % (sqlfechaini, sqlfechafin))
    total_peso_sin_rollos_d = peso_sin_rollos_d[0]
    if total_peso_sin_rollos_d != None:
        res += total_peso_sin_rollos_d
    # Ahora los que no tienen parte de producción (a partir del 2007 -aprox.- no debería haber ninguno):
    peso_sin_rollos = PDP._queryOne("""
        SELECT SUM(rollo.peso - campos_especificos_rollo.peso_embalaje) 
          FROM rollo, articulo, producto_venta, campos_especificos_rollo 
         WHERE articulo.producto_venta_id = producto_venta.id
           AND producto_venta.campos_especificos_rollo_id = campos_especificos_rollo.id 
           AND articulo.rollo_id = rollo.id 
           AND articulo.parte_de_produccion_id IS NULL 
           AND rollo.fechahora >= '%s' 
           AND rollo.fechahora <= '%s' ;
    """ % (sqlfechaini, (fechafin + mx.DateTime.oneDay).strftime("%Y-%m-%d")))
    total_peso_sin_rollos = peso_sin_rollos[0]
    if total_peso_sin_rollos != None:
        res += total_peso_sin_rollos
    peso_sin_rollos_d = PDP._queryOne("""
        SELECT SUM(rollo_defectuoso.peso - rollo_defectuoso.peso_embalaje) 
          FROM rollo_defectuoso, articulo 
         WHERE articulo.rollo_defectuoso_id = rollo_defectuoso.id 
           AND articulo.parte_de_produccion_id IS NULL 
           AND rollo_defectuoso.fechahora >= '%s' 
           AND rollo_defectuoso.fechahora <= '%s' ;
    """ % (sqlfechaini, (fechafin + mx.DateTime.oneDay).strftime("%Y-%m-%d")))
    total_peso_sin_rollos_d = peso_sin_rollos_d[0]
    if total_peso_sin_rollos_d != None:
        res += total_peso_sin_rollos_d
    return res

def buscar_produccion_gtx(anno, vpro = None, rango = None, logger = None, 
                          meses = []):
    """
    "anno" es el año del que buscará las producciones.
    "vpro" es la ventana de progreso de la ventana principal.
    "rango" es un flotante que indica el porcentaje máximo a 
            recorrer por la ventana de progreso durante esta función.
    Devuelve la producción en kg y m² de A y B en un diccionario 
    cuyas claves son números enteros del 0 al 11 que se corresponden 
    con los meses. Dentro de cada clave hay otro diccionario con 
    claves 'A' y 'B', y como valores otro diccionario 
    con claves 'metros' y 'kilos'.
    """
    res = dict([(i, 0) for i in xrange(12)])
    if vpro != None:
        incr_progreso = rango / 12.0
    for i in xrange(12):
        if i+1 not in meses:
            res[i] = {'A' : {'metros': 0, 'kilos': 0}, 
                      'B' : {'metros': 0, 'kilos': 0}, 
                      'kilos_a_mas_b_sin_embalaje': 0,  
                      'consumo': 0, 'kilos_hora': 0, 
                      'horas': 0, 'horas_produccion': 0, 
                      'dias': 0, 'turnos': 0,
                      'empleados': 0, 'productividad': 0, 
                      'gtxc': 0}
        else:
            fechaini = mx.DateTime.DateTimeFrom(day=1, month=i+1, year=anno)
            fechafin = mx.DateTime.DateTimeFrom(day=-1, month=i+1, year=anno)
            
            # XXX: No estoy seguro de por qué, pero de repente la versión de 
            #      mx de Sid amd64 ha empezado a devolver -1 como día 
            #      al operar con la fecha, en lugar de convertir los valores 
            #      negativos en días desde el final de mes, como siempre.
            fechafin = utils.asegurar_fecha_positiva(fechafin)
            # XXX

            (metros_a, 
             kilos_a, 
             metros_b, 
             kilos_b) = consultar_metros_y_kilos_gtx(fechaini, fechafin)
            kilos_consumidos = consultar_kilos_fibra_consumidos(fechaini, 
                                                                fechafin)
            horas = consultar_horas_reales_gtx(fechaini, fechafin)
            horas_trabajo = consultar_horas_trabajo_gtx(fechaini, 
                                                        fechafin, 
                                                        logger)

            # XXX fix_kilos_hora 05/07/2007
            kilos_reales_producidos_sin_embalaje = buscar_kilos_reales_gtx_producidos_sin_embalaje(fechaini, fechafin)
            # print kilos_reales_producidos_sin_embalaje
            try:
                # kilos_hora = (kilos_a + kilos_b) / horas_trabajo
                kilos_hora=kilos_reales_producidos_sin_embalaje/horas_trabajo
            # XXX EOfix_kilos_hora 05/07/2007
            
            except ZeroDivisionError:
                kilos_hora = 0.0
            dias = consultar_dias_gtx(fechaini, fechafin)
            # print kilos_a, kilos_b, horas, horas_trabajo. # OJO: Kg/hora se 
            # calcula con las horas en las que la máquina funciona, sin contar 
            # paradas. En la ventana se muestran las horas totales de los 
            # partes de la línea.
            try:
                turnos = (horas / 8.0) / dias   
                # (Horas / 8 horas por turno) / días para obtener 
                # los turnos por día. 
            except ZeroDivisionError:
                turnos = 0.0
            # OJO: Como los Geotextiles C no tienen ancho ni largo, no los 
            #      meto en la producción global para no falsear los 
            #      resultados.
            gtxc = consultar_gtxc(fechaini, fechafin)
            res[i] = {'A' : {'metros': metros_a, 'kilos': kilos_a}, 
                      'B' : {'metros': metros_b, 'kilos': kilos_b}, 
                      'kilos_a_mas_b_sin_embalaje': 
                        kilos_reales_producidos_sin_embalaje,  
                      'consumo': kilos_consumidos, 
                      'kilos_hora': kilos_hora, 
                      'horas': horas, 
                      'horas_produccion': horas_trabajo, 
                      'dias': dias,  
                      'turnos': turnos,
                      'empleados': consultar_empleados_por_dia_gtx(fechaini, 
                                                                   fechafin), 
                      'productividad': consultar_productividad_gtx(fechaini, 
                                                                   fechafin), 
                      'gtxc': gtxc
                     }
        if vpro != None: vpro.set_valor(vpro.get_valor() + incr_progreso, 
                                        vpro.get_texto())
    return res

def buscar_produccion_bolsas(anno, vpro = None, rango = None, logger = None, 
                             meses = []):
    """
    "anno" es el año del que buscará las producciones.
    "vpro" es la ventana de progreso de la ventana principal.
    "rango" es un flotante que indica el porcentaje máximo a 
            recorrer por la ventana de progreso durante esta función.
    Devuelve la producción en kg y m² de A y B en un diccionario 
    cuyas claves son números enteros del 0 al 11 que se corresponden 
    con los meses. Dentro de cada clave hay otro diccionario con 
    claves 'A' y 'B', y como valores otro diccionario 
    con claves 'bolsas' y 'kilos'.
    """
    res = dict([(i, 0) for i in xrange(12)])
    if vpro != None:
        incr_progreso = rango / 12.0
    for i in xrange(12):
        if i+1 not in meses:
            res[i] = {'A' : {'bolsas': 0, 'kilos': 0}, 
                      'B' : {'bolsas': 0, 'kilos': 0}, 
                      'consumo': 0, 'kilos_hora': 0, 
                      'horas': 0, 'horas_produccion': 0, 
                      'dias': 0, 'turnos': 0,
                      'empleados': 0, 'productividad': 0}
        else:
            fechaini = mx.DateTime.DateTimeFrom(day=1, month=i+1, year=anno)
            fechafin = mx.DateTime.DateTimeFrom(day=-1, month=i+1, year=anno)
            
            # XXX: No estoy seguro de por qué, pero de repente la versión de 
            #      mx de Sid amd64 ha empezado a devolver -1 como día 
            #      al operar con la fecha, en lugar de convertir los valores 
            #      negativos en días desde el final de mes, como siempre.
            fechafin = utils.asegurar_fecha_positiva(fechafin)
            # XXX

            (bolsas_a, 
             kilos_a, 
             bolsas_b, 
             kilos_b) = consultar_bolsas_y_kilos(fechaini, fechafin)
            kilos_consumidos = consultar_kilos_bigbags_consumidos(fechaini, 
                                                                  fechafin)
            horas = consultar_horas_reales_bolsas(fechaini, fechafin)
            horas_trabajo = consultar_horas_trabajo_bolsas(fechaini, 
                                                           fechafin, 
                                                           logger)

            try:
                kilos_hora = (kilos_a + kilos_b) / horas_trabajo
            except ZeroDivisionError:
                kilos_hora = 0.0
            dias = consultar_dias_bolsas(fechaini, fechafin)
            # print kilos_a, kilos_b, horas, horas_trabajo. # OJO: Kg/hora se 
            # calcula con las horas en las que la máquina funciona, sin contar 
            # paradas. En la ventana se muestran las horas totales de los 
            # partes de la línea.
            try:
                turnos = (horas / 8.0) / dias   
                # (Horas / 8 horas por turno) / días para obtener 
                # los turnos por día. 
            except ZeroDivisionError:
                turnos = 0.0
            res[i] = {'A' : {'bolsas': bolsas_a, 'kilos': kilos_a}, 
                      'B' : {'bolsas': bolsas_b, 'kilos': kilos_b}, 
                      'consumo': kilos_consumidos, 
                      'kilos_hora': kilos_hora, 
                      'horas': horas, 
                      'horas_produccion': horas_trabajo, 
                      'dias': dias,  
                      'turnos': turnos,
                      'empleados':consultar_empleados_por_dia_bolsas(fechaini,
                                                                   fechafin), 
                      'productividad':consultar_productividad_bolsas(fechaini,
                                                                   fechafin), 
                     }
        if vpro != None: vpro.set_valor(vpro.get_valor() + incr_progreso, 
                                        vpro.get_texto())
    return res


##################### V E N T A S ##############################################
       
def _buscar_compras_geocompuestos(fecha_ini, fecha_fin):
    """
    Dadas fecha de inicio y de fin, busca todas las compras
    (LDVs, LDAs y LDDs) facturadas entre esas dos fechas.
    """
    compras_geocmp = {}
    if 'total' not in compras_geocmp:
        compras_geocmp['total'] = {'cantidad': 0.0, 'euros': 0.0}
    idcliente = None  # @UnusedVariable
    resultado = []  # @UnusedVariable
    facturas = pclases.FacturaCompra.select(pclases.AND(
                                pclases.FacturaCompra.q.fecha >= fecha_ini,
                                pclases.FacturaCompra.q.fecha <= fecha_fin),
                            orderBy='fecha')
    facturas = list(facturas)
    for f in facturas:
        for linea in f.lineasDeCompra:
            p = linea.productoCompra
            if p != None and (p.es_geocompuesto()):
                proveedor = linea.proveedor
                euros = linea.get_subtotal()
                cantidad = linea.cantidad
                if proveedor not in compras_geocmp:
                    compras_geocmp[proveedor] = {'cantidad':cantidad,
                                                 'euros':euros} 
                else:
                    compras_geocmp[proveedor]['cantidad'] += cantidad
                    compras_geocmp[proveedor]['euros'] += euros
                compras_geocmp['total']['cantidad'] += cantidad
                compras_geocmp['total']['euros'] += euros
    # No hay abonos de productos de compra. Se usan facturas con cantidad < 0
    return compras_geocmp

def _buscar_ventas_geocompuestos(fecha_ini, fecha_fin):
    """
    Dadas fecha de inicio y de fin, busca todas las ventas 
    (LDVs, LDAs y LDDs) facturadas entre esas dos fechas.
    """
    ventas_geocmp = {}
    if 'total' not in ventas_geocmp:
        ventas_geocmp['total'] = {'cantidad': 0.0, 'euros': 0.0}
    idcliente = None  # @UnusedVariable
    resultado = []  # @UnusedVariable
    facturas = pclases.FacturaVenta.select(pclases.AND(
                                    pclases.FacturaVenta.q.fecha >= fecha_ini,
                                    pclases.FacturaVenta.q.fecha <= fecha_fin),
                                orderBy='fecha')
    facturas = list(facturas)
    for f in facturas:
        for linea in f.lineasDeVenta:
            p = linea.productoCompra
            if p != None and (p.es_geocompuesto()):
                tarifa = linea.get_tarifa()
                euros = linea.get_subtotal()
                cantidad = linea.cantidad
                if tarifa not in ventas_geocmp:
                    ventas_geocmp[tarifa]={'cantidad':cantidad,'euros':euros} 
                else:
                    ventas_geocmp[tarifa]['cantidad'] += cantidad
                    ventas_geocmp[tarifa]['euros'] += euros
                ventas_geocmp['total']['cantidad'] += cantidad
                ventas_geocmp['total']['euros'] += euros
    # No hay abonos de productos de compra. Se usan facturas con cantidad < 0
    return ventas_geocmp

def _buscar_ventas(fecha_ini, fecha_fin):
    """
    Dadas fecha de inicio y de fin, busca todas las ventas 
    (LDVs) facturadas entre esas dos fechas.
    """
    ventas_gtx = {}
    ventas_fibra = {}
    ventas_bolsas = {}
    if 'total' not in ventas_gtx:
        ventas_gtx['total'] = {'metros': 0.0, 'kilos': 0.0, 'euros': 0.0}
    if 'total' not in ventas_fibra:
        ventas_fibra['total'] = {'kilos': 0.0, 'euros': 0.0}
    if 'total' not in ventas_bolsas:
        ventas_bolsas['total'] = {'bolsas': 0, 'kilos': 0.0, 'euros': 0.0}
    idcliente = None  # @UnusedVariable
    resultado = []  # @UnusedVariable
    resultado_abonos = {'lineasDeAbono': [], 'lineasDeDevolucion': []}  # @UnusedVariable
    facturas = pclases.FacturaVenta.select(pclases.AND(
                                    pclases.FacturaVenta.q.fecha >= fecha_ini,
                                    pclases.FacturaVenta.q.fecha <= fecha_fin),
                                orderBy='fecha')
    facturasDeAbono = pclases.FacturaDeAbono.select(pclases.AND(
                            pclases.FacturaDeAbono.q.fecha <= fecha_fin, 
                            pclases.FacturaDeAbono.q.fecha >= fecha_ini), 
                        orderBy = 'fecha')
    facturasDeAbono = [f for f in facturasDeAbono if f.abono]
    facturas = list(facturas)
    for f in facturas:
        for linea in f.lineasDeVenta:
            procesar_ldv(linea, ventas_gtx, ventas_fibra, ventas_bolsas)
    for f in facturasDeAbono:
        abono = f.abono
        for lda in abono.lineasDeAbono:
            # Filtro las que son ajuste de precio de servicios.
            if lda.lineaDeVenta != None: 
                procesar_lda(lda, ventas_gtx, ventas_fibra, ventas_bolsas)
        for ldd in abono.lineasDeDevolucion:
            procesar_ldd(ldd, ventas_gtx, ventas_fibra, ventas_bolsas)
    return ventas_gtx, ventas_fibra, ventas_bolsas

def procesar_lda(linea, ventas_gtx, ventas_fibra, ventas_bolsas):
    p = linea.productoVenta
    if p != None:
        tarifa = linea.get_tarifa()
        euros = linea.diferencia * linea.cantidad
        if p.es_rollo():
            # metros = -linea.cantidad
            metros = 0  # OJO: Es un ajuste de precio, no se ha devuelto 
                        # material.
            # kilos = -linea.cantidad*p.camposEspecificosRollo.gramos/1000.0
            kilos = 0 # OJO: Es un ajuste de precio, no se ha devuelto material.
            if tarifa not in ventas_gtx:
                ventas_gtx[tarifa] = {'metros': metros, 
                                      'kilos': kilos, 
                                      'euros': euros}
            else:
                ventas_gtx[tarifa]['metros'] += metros
                ventas_gtx[tarifa]['kilos'] += kilos
                ventas_gtx[tarifa]['euros'] += euros
            ventas_gtx['total']['metros'] += metros
            ventas_gtx['total']['kilos'] += kilos
            ventas_gtx['total']['euros'] += euros
        elif p.es_bigbag() or p.es_bala():
            # kilos = -linea.cantidad
            kilos = 0 # OJO: Es un ajuste de precio, no se ha devuelto material.
            if tarifa not in ventas_fibra:
                ventas_fibra[tarifa] = {'kilos': kilos, 'euros': euros}
            else:
                ventas_fibra[tarifa]['kilos'] += kilos
                ventas_fibra[tarifa]['euros'] += euros
            ventas_fibra['total']['kilos'] += kilos
            ventas_fibra['total']['euros'] += euros
        elif p.es_bolsa():
            kilos = 0 #OJO: Es un ajuste de precio, no se ha devuelto material.
            bolsas = kilos / (p.camposEspecificosBala.gramosBolsa / 1000.0)
            if tarifa not in ventas_bolsas:
                ventas_bolsas[tarifa] = {'kilos': kilos, 'euros': euros, 
                                        'bolsas': bolsas}
            else:
                ventas_bolsas[tarifa]['kilos'] += kilos
                ventas_bolsas[tarifa]['euros'] += euros
                ventas_bolsas[tarifa]['bolsas'] += bolsas
            ventas_bolsas['total']['kilos'] += kilos
            ventas_bolsas['total']['euros'] += euros
            ventas_bolsas['total']['bolsas'] += bolsas
        elif p.es_especial():   # No sé qué hacer con los productos especiales, 
                                # así que los ignoro.
            print "OJO: Ignorando venta de línea LDA ID %d por no ser fibra"\
                  " ni geotextil (es producto especial)." % (linea.id)
        elif p.es_bala_cable(): # Tampoco sé muy bien cómo habría que tratar 
                                # una devolución de bala de cable enviada 
                                # para reciclar.
            print "OJO: Ignorando venta de línea LDA ID %d por no ser fibra"\
                  " ni geotextil (es bala_cable)." % (linea.id)
    else:   # No sé qué hacer con las ventas de productos de compra o 
            # servicios, así que las ignoro.
        print "OJO: Ignorando venta de línea LDA ID %d por no ser fibra ni geotextil (es producto de compra o servicio)." % (linea.id)

def procesar_ldd(linea, ventas_gtx, ventas_fibra, ventas_bolsas):
    p = linea.productoVenta
    if p != None:
        tarifa = linea.get_tarifa()
        # euros = linea.cantidad * linea.precio 
        # FIXED: LineaDeDevolucion.precio es el importe total de la 
        #        línea. Cantidad es un property que mira la cantidad exacta 
        #        en m² o kg del bulto relacionado 
        #        (1 LDD = 1 bulto = 1 pclases.Articulo).
        euros = -1 * linea.precio
        if p.es_rollo():
            metros = linea.cantidad
            kilos = linea.cantidad * p.camposEspecificosRollo.gramos / 1000.0
            if tarifa not in ventas_gtx:
                ventas_gtx[tarifa] = {'metros': metros, 'kilos': kilos, 'euros': euros}
            else:
                ventas_gtx[tarifa]['metros'] += metros
                ventas_gtx[tarifa]['kilos'] += kilos
                ventas_gtx[tarifa]['euros'] += euros
            ventas_gtx['total']['metros'] += metros
            ventas_gtx['total']['kilos'] += kilos
            ventas_gtx['total']['euros'] += euros
        elif p.es_bigbag() or p.es_bala():
            kilos = linea.cantidad
            if tarifa not in ventas_fibra:
                ventas_fibra[tarifa] = {'kilos': kilos, 'euros': euros}
            else:
                ventas_fibra[tarifa]['kilos'] += kilos
                ventas_fibra[tarifa]['euros'] += euros
            ventas_fibra['total']['kilos'] += kilos
            ventas_fibra['total']['euros'] += euros
        elif p.es_bolsa():
            kilos = linea.cantidad
            bolsas = kilos / (p.camposEspecificosBala.gramosBolsa / 1000.0)
            if tarifa not in ventas_bolsas:
                ventas_bolsas[tarifa] = {'kilos': kilos, 'euros': euros, 
                                        'bolsas': bolsas}
            else:
                ventas_bolsas[tarifa]['kilos'] += kilos
                ventas_bolsas[tarifa]['euros'] += euros
                ventas_bolsas[tarifa]['bolsas'] += bolsas
            ventas_bolsas['total']['kilos'] += kilos
            ventas_bolsas['total']['euros'] += euros
            ventas_bolsas['total']['bolsas'] += bolsas
        elif p.es_especial():   
            # No sé qué hacer con los productos especiales, así que los ignoro.
            print "OJO: Ignorando venta de línea LDD ID %d por no ser fibra"\
                  " ni geotextil (es producto especial)." % (linea.id)
    else:   # No sé qué hacer con las ventas de productos de compra o 
            # servicios, así que las ignoro.
        print "OJO: Ignorando venta de línea LDD ID %d por no ser fibra ni "\
              "geotextil (es producto de compra o servicio)." % (linea.id)

def procesar_ldv(linea, ventas_gtx, ventas_fibra, ventas_bolsas):
    p = linea.productoVenta
    # XXX: if p != None:     OJO: Ahora la fibra se organiza de otra forma. 
    # Me salto las ventas de fibra aquí. Sólo proceso las de geotextiles.
    if p != None and (p.es_rollo() or p.es_bolsa()):
        tarifa = linea.get_tarifa()
        euros = linea.get_subtotal()
        if p.es_rollo():
            metros = linea.cantidad
            kilos = linea.cantidad * p.camposEspecificosRollo.gramos / 1000.0
            if tarifa not in ventas_gtx:
                ventas_gtx[tarifa] = {'metros': metros, 'kilos': kilos, 
                                      'euros': euros}
            else:
                ventas_gtx[tarifa]['metros'] += metros
                ventas_gtx[tarifa]['kilos'] += kilos
                ventas_gtx[tarifa]['euros'] += euros
            ventas_gtx['total']['metros'] += metros
            ventas_gtx['total']['kilos'] += kilos
            ventas_gtx['total']['euros'] += euros
        elif p.es_bigbag() or p.es_bala():
            kilos = linea.cantidad
            if tarifa not in ventas_fibra:
                ventas_fibra[tarifa] = {'kilos': kilos, 'euros': euros}
            else:
                ventas_fibra[tarifa]['kilos'] += kilos
                ventas_fibra[tarifa]['euros'] += euros
            ventas_fibra['total']['kilos'] += kilos
            ventas_fibra['total']['euros'] += euros
        elif p.es_bolsa():
            kilos = linea.cantidad
            bolsas = kilos / (p.camposEspecificosBala.gramosBolsa / 1000.0)
            if tarifa not in ventas_bolsas:
                ventas_bolsas[tarifa] = {'kilos': kilos, 'euros': euros, 
                                        'bolsas': bolsas}
            else:
                ventas_bolsas[tarifa]['kilos'] += kilos
                ventas_bolsas[tarifa]['euros'] += euros
                ventas_bolsas[tarifa]['bolsas'] += bolsas
            ventas_bolsas['total']['kilos'] += kilos
            ventas_bolsas['total']['euros'] += euros
            ventas_bolsas['total']['bolsas'] += bolsas
        elif p.es_especial():   # No sé qué hacer con los productos 
                                # especiales, así que los ignoro.
            print "OJO: Ignorando venta de línea LDV ID %d por no ser "\
                  "fibra ni geotextil (es producto especial)." % (linea.id)
        elif p.es_bala_cable(): # No sé cómo tratar las ventas de fibra para 
                                # reciclar. Se supone que no se factura. Sólo 
                                # salen en albarán.
            print "OJO: Ignorando venta de línea LDV ID %d por no ser "\
                  "fibra ni geotextil (es bala_cable)." % (linea.id)
    else:   # No sé qué hacer con las ventas de productos de compra o 
            # servicios, así que las ignoro.
        # print "OJO: Ignorando venta de línea LDV ID %d por no ser fibra ni geotextil (es producto de compra o servicio)." % (linea.id)
        pass    # En esta función ya solo se cuentan geotextiles. No tiene 
                # sentido sacar el mensaje. Se ha cambiado la condición 
                # y entra en la rama else tanto si es producto de compra o 
                # servicio como si es fibra normal.

def ejecutar_consultas_ventas_fibra_por_color(fechaini, fechafin):
    """
    Ejecuta las consultas de venta de fibra (balas) por color 
    entre las fechas fechaini y fechafin y devuelve los kilos y 
    euros de facturas y albaranes en un diccionario de colores 
    y "internacional" o "nacional".
    Incluye fibra B (marcada como B en el parte de producción) pero 
    no la C (balas de cable -balaCable- que tiene True en el campo 
    reciclada del camposEspecificosBala del producto de venta).
    """
    #prods = """
    #    SELECT pv.id AS producto_venta_id, color 
    #     INTO TEMP fibra_balas_con_campos_especificos_temp
    #     FROM campos_especificos_bala ceb, producto_venta pv
    #     WHERE pv.campos_especificos_bala_id = ceb.id
    #           AND pv.descripcion NOT ILIKE '%GEOCEM%';
    #"""
    prods = """
        SELECT pv.id AS producto_venta_id, color 
         INTO TEMP fibra_balas_con_campos_especificos_temp
         FROM campos_especificos_bala ceb, producto_venta pv
         WHERE pv.campos_especificos_bala_id = ceb.id
               AND pv.descripcion NOT ILIKE %s 
               AND ceb.reciclada = FALSE;
    """ % pclases.ProductoVenta.sqlrepr("%GEOCEM%")
    sql_fechaini = fechaini.strftime("%Y-%m-%d")
    sql_fechafin = fechafin.strftime("%Y-%m-%d")
    kilos_euros_ldv = """
        SELECT SUM(linea_de_venta.cantidad) AS kilos,
               SUM(linea_de_venta.cantidad 
                    * linea_de_venta.precio 
                    * (1-linea_de_venta.descuento)) AS euros, 
               fibra_balas_con_campos_especificos_temp.color, 
               cliente.pais 
         FROM linea_de_venta, 
              factura_venta, 
              cliente, 
              fibra_balas_con_campos_especificos_temp
         WHERE linea_de_venta.factura_venta_id = factura_venta.id
               AND factura_venta.fecha >= '%s'
               AND factura_venta.fecha <= '%s'
               AND cliente.id = factura_venta.cliente_id
               AND linea_de_venta.producto_venta_id = fibra_balas_con_campos_especificos_temp.producto_venta_id
         GROUP BY cliente.pais, fibra_balas_con_campos_especificos_temp.color; 
    """ % (sql_fechaini, sql_fechafin)
    kilos_euros_lda = """
        SELECT 0.0 AS kilos, 
               SUM(linea_de_abono.cantidad*linea_de_abono.diferencia) AS euros, 
               fibra_balas_con_campos_especificos_temp.color, 
               cliente.pais
         FROM linea_de_abono, 
              factura_de_abono, 
              cliente, 
              abono, 
              linea_de_venta, 
              fibra_balas_con_campos_especificos_temp
         WHERE linea_de_abono.abono_id = abono.id
               AND linea_de_abono.linea_de_venta_id = linea_de_venta.id
               AND linea_de_venta.producto_venta_id = fibra_balas_con_campos_especificos_temp.producto_venta_id
               AND factura_de_abono.fecha >= '%s'
               AND factura_de_abono.fecha <= '%s'
               AND cliente.id = abono.cliente_id
               AND factura_de_abono.id = abono.factura_de_abono_id
        GROUP BY cliente.pais, fibra_balas_con_campos_especificos_temp.color; 
    """ % (sql_fechaini, sql_fechafin)
    frabonos = """
        SELECT linea_de_devolucion.id, 
               linea_de_devolucion.articulo_id, 
               cliente.pais, 
               linea_de_devolucion.precio, 
               fibra_balas_con_campos_especificos_temp.color
         INTO TEMP facturas_de_abono_temp 
         FROM linea_de_devolucion, 
              factura_de_abono, 
              cliente, 
              abono, 
              articulo, 
              fibra_balas_con_campos_especificos_temp
         WHERE linea_de_devolucion.abono_id = abono.id
           AND factura_de_abono.id = abono.factura_de_abono_id
           AND factura_de_abono.fecha >= '%s'
           AND factura_de_abono.fecha <= '%s'
           AND cliente.id = abono.cliente_id
           AND linea_de_devolucion.albaran_de_entrada_de_abono_id IS NOT NULL
           AND articulo.id = linea_de_devolucion.articulo_id
           AND articulo.producto_venta_id = fibra_balas_con_campos_especificos_temp.producto_venta_id; 
    """ % (sql_fechaini, sql_fechafin)
    kilos_euros_ldd = """
        SELECT -1 * SUM(bala.pesobala) AS kilos, 
               -1 * SUM(precio) AS euros, 
               color, 
               pais
         FROM bala, facturas_de_abono_temp, articulo
         WHERE bala.id = articulo.bala_id 
               AND facturas_de_abono_temp.articulo_id = articulo.id
         GROUP BY pais, color;
    """
    caidita_de_roma = """
        DROP TABLE fibra_balas_con_campos_especificos_temp;
        DROP TABLE facturas_de_abono_temp;
    """
    con = pclases.Bala._connection  # En realidad la clase da igual.
    con.query(prods)
    con.query(frabonos)
    ke_ldv = con.queryAll(kilos_euros_ldv)
    ke_lda = con.queryAll(kilos_euros_lda)
    ke_ldd = con.queryAll(kilos_euros_ldd)
    try:
        dde = pclases.DatosDeLaEmpresa.select()[0]
    except IndexError:
        print "No existen datos en la tabla datos_de_la_empresa. Usando 'ESPAÑA' como país predeterminado."
        pais_empresa = unicode("españa")
    else:
        pais_empresa = unicode(dde.paisfacturacion.strip()).lower()
    res = {}
    for fila in ke_ldv + ke_lda + ke_ldd:
        kilos, euros, color, pais = fila
        if color not in res:
            res[color] = {}
        pais = unicode(pais.strip())
        if pais != "" and pais.lower() != pais_empresa:
            clavepais = "internacional"
        else:   # Si no lleva país, lo considero nacional (es normal 
                # dejarlo en blanco si el país es España).
            clavepais = "nacional"
        if clavepais not in res[color]:
            res[color][clavepais] = {'kilos': 0.0, 'euros': 0.0}
        res[color][clavepais]['kilos'] += kilos
        res[color][clavepais]['euros'] += euros
    con.query(caidita_de_roma)
    return res

def ejecutar_consultas_ventas_bigbags(fechaini, fechafin):
    """
    Ejecuta consultas SQL directamente contra la BD para 
    obtener las ventas de bigbags entre las fechas indicadas.
    """
    sql_fechaini = fechaini.strftime("%Y-%m-%d")
    sql_fechafin = fechafin.strftime("%Y-%m-%d")
    prods = """
        SELECT pv.id AS producto_venta_id
         INTO TEMP fibra_bigbags
         FROM producto_venta pv
         WHERE pv.descripcion ILIKE '%GEOCEM%';
    """
    kilos_euros_ldv = """
        SELECT COALESCE(SUM(linea_de_venta.cantidad), 0.0) AS kilos,
               COALESCE(SUM(linea_de_venta.cantidad * linea_de_venta.precio * (1-linea_de_venta.descuento)), 0.0) AS euros 
         FROM linea_de_venta, factura_venta, fibra_bigbags
         WHERE linea_de_venta.factura_venta_id = factura_venta.id
               AND factura_venta.fecha >= '%s'
               AND factura_venta.fecha <= '%s'
               AND linea_de_venta.producto_venta_id = fibra_bigbags.producto_venta_id
         ;
    """ % (sql_fechaini, sql_fechafin)
    kilos_euros_lda = """
        SELECT 0.0 AS kilos, 
               COALESCE(SUM(linea_de_abono.cantidad * linea_de_abono.diferencia), 0.0) AS euros 
         FROM linea_de_abono, factura_de_abono, abono, linea_de_venta, fibra_bigbags
         WHERE linea_de_abono.abono_id = abono.id
               AND linea_de_abono.linea_de_venta_id = linea_de_venta.id
               AND linea_de_venta.producto_venta_id = fibra_bigbags.producto_venta_id
               AND factura_de_abono.fecha >= '%s'
               AND factura_de_abono.fecha <= '%s'
               AND factura_de_abono.id = abono.factura_de_abono_id
         ;
    """ % (sql_fechaini, sql_fechafin)
    frabonos = """
        SELECT linea_de_devolucion.id, linea_de_devolucion.articulo_id, linea_de_devolucion.precio
         INTO TEMP facturas_de_abono_temp
         FROM linea_de_devolucion, factura_de_abono, abono, articulo, fibra_bigbags
         WHERE linea_de_devolucion.abono_id = abono.id
           AND factura_de_abono.id = abono.factura_de_abono_id
           AND factura_de_abono.fecha >= '%s'
           AND factura_de_abono.fecha <= '%s'
           AND linea_de_devolucion.albaran_de_entrada_de_abono_id IS NOT NULL
           AND articulo.id = linea_de_devolucion.articulo_id
           AND articulo.producto_venta_id = fibra_bigbags.producto_venta_id; 
    """ % (sql_fechaini, sql_fechafin)
    kilos_euros_ldd = """  
        SELECT COALESCE(-1 * SUM(bigbag.pesobigbag), 0.0) AS kilos, 
               COALESCE(-1 * SUM(precio), 0.0) AS euros 
         FROM bigbag, facturas_de_abono_temp, articulo
         WHERE bigbag.id = articulo.bigbag_id 
               AND facturas_de_abono_temp.articulo_id = articulo.id
         ;
    """
    caidita_de_roma = """
        DROP TABLE fibra_bigbags;
        DROP TABLE facturas_de_abono_temp;
    """
    con = pclases.Bala._connection  # En realidad la clase da igual.
    con.query(prods)
    con.query(frabonos)
    ke_ldv = con.queryAll(kilos_euros_ldv)
    ke_lda = con.queryAll(kilos_euros_lda)
    ke_ldd = con.queryAll(kilos_euros_ldd)
    res = {'kilos': 0.0, 'euros': 0.0}
    for fila in ke_ldv + ke_lda + ke_ldd:
        kilos, euros = fila
        try:
            res['kilos'] += kilos
        except TypeError:   # kilos viene como un Decimal. Paso a float.
            res['kilos'] += float(kilos)
        try:
            res['euros'] += euros
        except TypeError:   # Viene como un Decimal. Paso a float.
            res['euros'] += float(euros)
    con.query(caidita_de_roma)
    return res

def buscar_ventas_por_color(anno, vpro = None, rango = None, meses = []):
    """
    Busca las ventas de fibra por color y país del cliente en 
    lugar de por tarifa.
    Devuelve un diccionario de colores donde cada valor es 
    otro diccionario de meses con las claves "nacional" y "internacional" 
    y como valores otro diccionario con "euros" y "kilos" (incluye 
    fibra B y excluye bigbags).
    """
    fibra = {}
    for i in xrange(12):
        if i+1 not in meses:
            kilos_euros_balas_mes = {}
        else:
            fechaini = mx.DateTime.DateTimeFrom(day = 1, 
                                                month = i + 1, 
                                                year = anno)
            fechafin = mx.DateTime.DateTimeFrom(day = -1, 
                                                month = i+1, 
                                                year = anno)
            # XXX: No estoy seguro de por qué, pero de repente la versión de 
            #      mx de Sid amd64 ha empezado a devolver -1 como día 
            #      al operar con la fecha, en lugar de convertir los valores 
            #      negativos en días desde el final de mes, como siempre.
            fechafin = utils.asegurar_fecha_positiva(fechafin)
            # XXX
            kilos_euros_balas_mes = ejecutar_consultas_ventas_fibra_por_color(
                fechaini, fechafin)
        fibra[i] = kilos_euros_balas_mes
    meses = range(12)
    colores = []
    tarifas = []
    for mes in fibra:
        for color in fibra[mes]:
            if color not in colores:
                colores.append(color)
            for tarifa in fibra[mes][color]:
                if tarifa not in tarifas:
                    tarifas.append(tarifa)
    _fibra = {}
    for color in colores:
        if color not in _fibra:
            _fibra[color] = {}
        for tarifa in tarifas:
            if tarifa not in _fibra[color]:
                _fibra[color][tarifa] = {}
            for mes in meses:
                if mes not in _fibra[color][tarifa]:
                    _fibra[color][tarifa][mes] = {}
                try:
                    _fibra[color][tarifa][mes] = fibra[mes][color][tarifa]
                except KeyError:
                    _fibra[color][tarifa][mes] = {'kilos': 0.0, 'euros': 0.0}
    return _fibra

def buscar_ventas_bigbags(anno, vpro = None, rango = None, meses = []):
    """
    Devuelve un diccionario de meses cuyos valores son otro 
    diccionario con los euros y los kilos de bigbags vendidos 
    en el año recibido.
    """
    fibra = {}
    for i in xrange(12):
        if i+1 not in meses:
            kilos_euros_bigbags_mes = {'kilos': 0, 'euros': 0}
        else:
            fechaini = mx.DateTime.DateTimeFrom(day=1, month=i + 1, year=anno)
            fechafin = mx.DateTime.DateTimeFrom(day=-1, month=i + 1, year=anno)
            
            # XXX: No estoy seguro de por qué, pero de repente la versión de 
            #      mx de Sid amd64 ha empezado a devolver -1 como día 
            #      al operar con la fecha, en lugar de convertir los valores 
            #      negativos en días desde el final de mes, como siempre.
            fechafin = utils.asegurar_fecha_positiva(fechafin)
            # XXX
            kilos_euros_bigbags_mes=ejecutar_consultas_ventas_bigbags(fechaini, 
                                                                      fechafin)
        fibra[i] = kilos_euros_bigbags_mes
    return fibra

def buscar_ventas_fibra_b(anno, vpro = None, rango = None, meses = []):
    """
    Devuelve las ventas (en euros y kilos) de la fibra marcada 
    como baja calidad.
    """
    ventasb = {}
    for i in xrange(12):
        if i+1 not in meses:
            kilos = euros = 0
        else:
            fechaini = mx.DateTime.DateTimeFrom(day=1, month=i+1, year=anno)
            fechafin = mx.DateTime.DateTimeFrom(day=-1, month=i+1, year=anno)
            
            # XXX: No estoy seguro de por qué, pero de repente la versión 
            #      de mx de Sid amd64 ha empezado a devolver -1 como día 
            #      al operar con la fecha, en lugar de convertir los valores 
            #      negativos en días desde el final de mes, como siempre.
            fechafin = utils.asegurar_fecha_positiva(fechafin)
            # XXX
    
            kilos, euros = ejecutar_consultas_fibra_b_por_fechas(fechaini, 
                                                                 fechafin)
        ventasb[i] = {'kilos': kilos, 'euros': euros}
    return ventasb

def buscar_ventas_cable(anno, vpro = None, rango = None):
    """
    Devuelve las salidas de albarán en kilos de la fibra reciclada.
    """
    cable = {}
    for i in range(12):
        fechaini = mx.DateTime.DateTimeFrom(day=1, month=i+1, year=anno)
        fechafin = mx.DateTime.DateTimeFrom(day=-1, month=i+1, year=anno)
        
        # XXX: No estoy seguro de por qué, pero de repente la versión de mx 
        #      de Sid amd64 ha empezado a devolver -1 como día 
        #      al operar con la fecha, en lugar de convertir los valores 
        #      negativos en días desde el final de mes, como siempre.
        fechafin = utils.asegurar_fecha_positiva(fechafin)
        # XXX
        BC = pclases.BalaCable
        A = pclases.Articulo
        AS = pclases.AlbaranSalida
        balasc = BC.select(pclases.AND(A.q.balaCableID == BC.q.id, 
                                       A.q.albaranSalidaID == AS.q.id, 
                                       AS.q.fecha >= fechaini, 
                                       AS.q.fecha <= fechafin))
        if balasc.count() > 0:
            kilos = balasc.sum("peso")
        else:
            kilos = 0.0

        cable[i] = {'kilos': kilos} # No devuelvo euros como con el resto de 
                                    # la fibra porque salen a precio 0. 
                                    # Nos cobran por reciclarla. Se paga en 
                                    # albaranes entrada y facturas compra.
    return cable

def buscar_ventas_internas_fibra(anno, vpro = None, rango = None, meses = []):
    """
    Devuelve en kilos y euros la fibra consumida en la línea 
    de producción de geotextiles.
    Se usa el precio por defecto para valorar los kilos.
    """
    consumo_fibra = {}
    for i in xrange(12):
        if i+1 not in meses:
            kilos_consumidos = euros_consumidos = 0
        else:
            fechaini = mx.DateTime.DateTimeFrom(day = 1, month = i + 1, year = anno)
            fechafin = mx.DateTime.DateTimeFrom(day = -1, month = i+1, year = anno)
            
            # XXX: No estoy seguro de por qué, pero de repente la versión de 
            #      mx de Sid amd64 ha empezado a devolver -1 como día 
            #      al operar con la fecha, en lugar de convertir los valores 
            #      negativos en días desde el final de mes, como siempre.
            fechafin = utils.asegurar_fecha_positiva(fechafin)
            # XXX
    
            #kilos_consumidos, euros_consumidos = consultar_kilos_y_euros_fibra_consumidos(fechaini, fechafin)
            kilos_consumidos, euros_consumidos = consultar_kilos_y_euros_fibra_consumidos_segun_pcs(fechaini, fechafin)
        consumo_fibra[i] = {'kilos': kilos_consumidos, 
                            'euros': euros_consumidos}
    return consumo_fibra

def consultar_kilos_y_euros_fibra_consumidos_segun_pcs(fechaini, fechafin):
    """
    Devuelve las "ventas" internas (consumo de fibra en línea de geotextiles) 
    según las fechas de las partidas de carga. Es decir, es más fiel a las 
    existencias, pero cuenta partidas que no han producido geotextiles o que 
    ha servido para fabricar geotextiles fuera del rango de fechas. También 
    hay que confiar en que las fechas de las partidas de carga son correctas. 
    En cualquier caso es coherente (sean o no sean precisas las fechas de las 
    partidas de carga) con las existencias en listado_balas, caché, etc.
    OJO: La valoración en euros es estimativa y, aunque determinista, varía 
    con el tiempo en función del precioDefecto que tenga cada producto en el 
    momento en que se ejecuta la consulta. Mucho ojito con eso.
    """
    pvfs = [pv for pv in pclases.ProductoVenta.select() if pv.es_bala()]
    kilos = 0.0
    euros = 0.0
    for pv in pvfs:
        kilos_pv = pv.buscar_consumos_cantidad(fechaini, fechafin)  
            # Es la misma función que se usa en HistoralExistencias.test(), 
            # así que debe cuadar existencias fechainicio - 1 día + ventas 
            # + consumos - produccion == existencias fechafin. 
            # Por definición, vaya.
        euros += kilos_pv * pv.precioDefecto
        kilos += kilos_pv
    return kilos, euros

def consultar_kilos_y_euros_fibra_consumidos(fechaini, fechafin):
    """
    Recibe 2 mx.DateTime con las fechas inicial y final de la 
    consulta de metros y kilos.
    Devuelve los kilos y euros a precio defecto de fibra consumidos 
    según el criterio de que una partida de carga no se considera 
    consumida por completo si todas sus partidas no se han fabricado 
    antes de fechafin.
    OJO: Ataca directamente a la BD con SQL. No es portable (aunque 
    a estas alturas cualquiera se atreve a cambiar de SGBD).
    (Ver metros_y_kilos_gtx.sql)
    """
    con = pclases.Rollo._connection
    # Consultas a pelo
    partes_gtx = """
        SELECT id
         INTO TEMP partes_gtx_temp
         FROM parte_de_produccion 
         WHERE (fecha >= '%s'                     -- Parámetro fecha ini
                AND fecha <= '%s'                 -- Parámetro fecha fin
                AND observaciones NOT LIKE '%%;%%;%%;%%;%%;%%'
                AND partida_cem_id IS NULL); 
    """ % (fechaini.strftime("%Y-%m-%d"), fechafin.strftime("%Y-%m-%d"))
    rollos_fab = """
        SELECT rollo_id, rollo_defectuoso_id
         INTO TEMP articulos_rollo_fabricados_temp
         FROM articulo
         WHERE parte_de_produccion_id IN (SELECT id FROM partes_gtx_temp);
    """
    partidas_rollos_def = """
        SELECT partida_id 
         INTO TEMP partidas_rollos_defectuosos_temp 
         FROM rollo_defectuoso rd
         WHERE rd.id IN (SELECT rollo_defectuoso_id FROM articulos_rollo_fabricados_temp)
         GROUP BY partida_id;
    """
    partidas_rollos = """
        SELECT partida_id 
         INTO TEMP partidas_rollos_temp 
         FROM rollo r
         WHERE r.id IN (SELECT rollo_id FROM articulos_rollo_fabricados_temp)
         GROUP BY partida_id;
    """
    func_partes_de_partida = """
        CREATE OR REPLACE FUNCTION partes_de_partida (INTEGER) RETURNS BIGINT
        AS '
            SELECT COUNT(id)
            FROM parte_de_produccion 
            WHERE id IN (SELECT parte_de_produccion_id
                         FROM articulo 
                         WHERE rollo_id IS NOT NULL 
                           AND rollo_id IN (SELECT id 
                                            FROM rollo 
                                            WHERE partida_id = $1) 
                           OR rollo_defectuoso_id IS NOT NULL 
                           AND rollo_defectuoso_id IN (SELECT id 
                                                       FROM rollo_defectuoso 
                                                       WHERE partida_id = $1) 
                         GROUP BY parte_de_produccion_id)
            ;
        ' LANGUAGE 'sql';
    """
    func_partes_antes_de = """
        CREATE OR REPLACE FUNCTION partes_de_partida_antes_de_fecha (INTEGER, DATE) RETURNS BIGINT
        AS '
            SELECT COUNT(id) 
             FROM parte_de_produccion 
             WHERE fecha <= $2
               AND id IN (SELECT parte_de_produccion_id
                          FROM articulo 
                          WHERE rollo_id IS NOT NULL 
                            AND rollo_id IN (SELECT id 
                                             FROM rollo 
                                             WHERE partida_id = $1) 
                            OR rollo_defectuoso_id IS NOT NULL 
                            AND rollo_defectuoso_id IN (SELECT id 
                                                        FROM rollo_defectuoso 
                                                        WHERE partida_id = $1)
                            GROUP BY parte_de_produccion_id) 
             ;
        ' LANGUAGE 'sql';
    """
    func_partida_entra = """
        CREATE OR REPLACE FUNCTION partida_entra_en_fecha(INTEGER, DATE) RETURNS BOOLEAN 
            -- Recibe un ID de partida de geotextiles y una fecha. 
            -- Devuelve TRUE si ningún parte de producción de la partida 
            -- tiene fecha posterior a la recibida Y la partida existe y 
            -- tiene producción.
        AS '
            SELECT partes_de_partida($1) > 0 AND partes_de_partida($1) = partes_de_partida_antes_de_fecha($1, $2);
        ' LANGUAGE 'sql';
    """
    func_pc_entra = """ 
        CREATE OR REPLACE FUNCTION partida_carga_entra_en_fecha(INTEGER, DATE) RETURNS BOOLEAN 
            -- Recibe el ID de una partida de carga y devuelve TRUE si todas las partidas 
            -- de geotextiles de la misma pertenecen a partes de producción de fecha anterior 
            -- o igual al segundo parámetro.
        AS' 
            SELECT COUNT(*) > 0 
            FROM partida
            WHERE partida_carga_id = $1 
              AND partida_entra_en_fecha(partida.id, $2);
        ' LANGUAGE 'sql';
    """
    partidas_carga_id = """        
        SELECT partida_carga_id
         INTO TEMP partidas_carga_id_temp
         FROM partida
         WHERE (id IN (SELECT partida_id FROM partidas_rollos_defectuosos_temp)
                OR id IN (SELECT partida_id FROM partidas_rollos_temp)) 
         GROUP BY partida_carga_id;
    """
    partidas_de_pc_en_fecha = """
        SELECT partida_carga_id 
         INTO TEMP partidas_de_carga_de_partidas_en_fecha_temp
         FROM partidas_carga_id_temp
         WHERE partida_carga_entra_en_fecha(partida_carga_id, '%s');       -- Parámetro fecha fin
    """ % (fechafin.strftime("%Y-%m-%d"))
    balas_y_peso = """
        SELECT bala.id AS id_bala_id, 
               AVG(pesobala) AS _pesobala, 
               articulo.producto_venta_id, 
               AVG(producto_venta.preciopordefecto) AS precio 
         INTO TEMP balas_con_peso_de_partida_de_carga 
         FROM bala, articulo, producto_venta 
         WHERE partida_carga_id IN (SELECT partida_carga_id 
                                    FROM partidas_de_carga_de_partidas_en_fecha_temp)
           AND bala.id = articulo.bala_id
           AND articulo.producto_venta_id = producto_venta.id
         GROUP BY bala.id, producto_venta_id; 
        -- OJO: Las balas llevan en torno a kilo o kilo y medio de plástico de embalar que se cuenta como fibra consumida.
    """
    total_balas_y_peso = """
        SELECT COUNT(id_bala_id) AS balas, SUM(_pesobala) AS peso_ce, SUM(_pesobala * precio) AS euros
         FROM balas_con_peso_de_partida_de_carga;
    """
    con.query(partes_gtx) 
    con.query(rollos_fab)
    con.query(partidas_rollos_def)
    con.query(partidas_rollos)
    con.query(func_partes_de_partida)
    con.query(func_partes_antes_de)
    con.query(func_partida_entra)
    con.query(func_pc_entra)
    con.query(partidas_carga_id)
    con.query(partidas_de_pc_en_fecha)
    con.query(balas_y_peso)

    balas_kilos = con.queryAll(total_balas_y_peso)
    caidita_de_roma = """
        DROP FUNCTION partes_de_partida(INTEGER);
        DROP FUNCTION partes_de_partida_antes_de_fecha(INTEGER, DATE);
        DROP FUNCTION partida_entra_en_fecha(INTEGER, DATE);
        DROP FUNCTION partida_carga_entra_en_fecha(INTEGER, DATE);
        DROP TABLE partidas_carga_id_temp;
        DROP TABLE balas_con_peso_de_partida_de_carga;
        DROP TABLE partidas_de_carga_de_partidas_en_fecha_temp;
        DROP TABLE partidas_rollos_defectuosos_temp;
        DROP TABLE partidas_rollos_temp;
        DROP TABLE articulos_rollo_fabricados_temp;
        DROP TABLE partes_gtx_temp;
    """
    con.query(caidita_de_roma)
    balas, kilos, euros = balas_kilos[0]  # @UnusedVariable
    return kilos and kilos or 0.0, euros and euros or 0.0

def ejecutar_consultas_fibra_b_por_fechas(fechaini, fechafin):
    albaranes_facturados = """
        SELECT albaran_salida.id AS albaran_salida_id, 
               linea_de_venta.precio*(1-linea_de_venta.descuento) AS precio, 
               linea_de_venta.producto_venta_id, 
               linea_de_venta.id AS linea_de_venta_id
         INTO albaranes_facturados_en_fecha_temp 
         FROM albaran_salida, linea_de_venta
         WHERE albaran_salida.id = linea_de_venta.albaran_salida_id 
           AND linea_de_venta.producto_venta_id IS NOT NULL
           AND linea_de_venta.factura_venta_id 
               IN (SELECT factura_venta.id
                    FROM factura_venta
                    WHERE factura_venta.fecha >= '%s'
                      AND factura_venta.fecha <= '%s')
         ;
    """ % (fechaini.strftime("%Y-%m-%d"), fechafin.strftime("%Y-%m-%d"))
    con = pclases.Bala._connection  # En realidad la clase da igual.
    con.query(albaranes_facturados)
    balas_facturadas_y_producto = """
        SELECT bala.pesobala, 
               articulo.producto_venta_id, 
               articulo.albaran_salida_id
         FROM bala, articulo
         WHERE bala.claseb = TRUE
           AND articulo.bala_id = bala.id
           AND articulo.albaran_salida_id IN (SELECT albaran_salida_id 
                                               FROM albaranes_facturados_en_fecha_temp)
         ;
    """
    filas_balas_facturadas_y_producto=con.queryAll(balas_facturadas_y_producto)
    bigbags_facturados_y_producto = """
        SELECT bigbag.pesobigbag, 
               articulo.producto_venta_id, 
               articulo.albaran_salida_id
         FROM bigbag, articulo
         WHERE bigbag.claseb = TRUE
           AND articulo.bigbag_id = bigbag.id
           AND articulo.albaran_salida_id IN (SELECT albaran_salida_id 
                                               FROM albaranes_facturados_en_fecha_temp)
         ;
    """
    filas_bigbags_facturados_y_producto = con.queryAll(bigbags_facturados_y_producto)
    filas_precios_facturados_por_producto_y_albaran = con.queryAll(""" SELECT * FROM albaranes_facturados_en_fecha_temp; """)
    #  Organizo los precios por albarán y producto:
    albaranes = {}
    for fila in filas_precios_facturados_por_producto_y_albaran:
        albaran_salida_id, precio, producto_venta_id, linea_de_venta_id = fila
        if albaran_salida_id not in albaranes:
            albaranes[albaran_salida_id] = {}
        if producto_venta_id not in albaranes[albaran_salida_id]:
            albaranes[albaran_salida_id][producto_venta_id] = {}
        if linea_de_venta_id not in albaranes[albaran_salida_id][producto_venta_id]:
            albaranes[albaran_salida_id][producto_venta_id][linea_de_venta_id] = precio
        else:
            print "consulta_global::ejecutar_consultas_fibra_b_por_fechas -> ¡ERROR! línea de venta (%d) duplicada en mismo albarán salida y producto de venta." % (linea_de_venta_id)
    euros = 0.0
    for fila in filas_balas_facturadas_y_producto + filas_bigbags_facturados_y_producto:
        peso, producto_venta_id, albaran_salida_id = fila
        # Si en el albarán y producto solo hay una LDV, el precio no tiene confusión:
        if len(albaranes[albaran_salida_id][producto_venta_id]) == 1:
            idldv = albaranes[albaran_salida_id][producto_venta_id].keys()[0]
            precio = albaranes[albaran_salida_id][producto_venta_id][idldv]
        else:
        # El precio es media ponderada:
            ldvs = albaranes[albaran_salida_id][producto_venta_id]
            cantidad_total = 0.0
            precio_total = 0.0
            for idldv in ldvs:
                ldv = pclases.LineaDeVenta.get(idldv)
                cantidad = ldv.cantidad  # @UnusedVariable
                cantidad_total += ldv.cantidad
                precio_total += ldv.precio
            precio = precio_total / cantidad_total
        euros += peso * precio

    ### vvv Kilos vvv ### ^^^ euros ^^^ ###

    kilos_balas_b_facturados = """
        SELECT COALESCE(SUM(bala.pesobala), 0) AS kilos_b_b
         FROM articulo, bala
         WHERE articulo.albaran_salida_id IN (SELECT albaran_salida_id 
                                               FROM albaranes_facturados_en_fecha_temp)
           AND articulo.bala_id = bala.id
           AND bala.claseb = TRUE;
    """
    kilos = con.queryAll(kilos_balas_b_facturados)[0][0]
    kilos_bigbags_b_facturados = """
        SELECT COALESCE(SUM(bigbag.pesobigbag), 0) AS kilos_bb_b
         FROM articulo, bigbag
         WHERE articulo.albaran_salida_id IN (SELECT albaran_salida_id 
                                               FROM albaranes_facturados_en_fecha_temp)
           AND articulo.bigbag_id = bigbag.id
           AND bigbag.claseb = TRUE;
    """
    kilos += con.queryAll(kilos_bigbags_b_facturados)[0][0]
    caidita_de_roma = """
        DROP TABLE albaranes_facturados_en_fecha_temp;
    """
    con.query(caidita_de_roma)

    # DONE: ¡¡¡Aún faltaría descontar los abonos!!!
    #       No hay abonos en consumos internos, ceporro.

    return kilos, euros

def buscar_ventas_fibra_color(anno, vpro = None, rango = None, meses = []):
    """
    Busca las ventas de fibra por color, consumidas por la línea, 
    fibra B y bigbags. Devuelve una lista de listas. Cada lista 
    tiene en la primera posición un texto descriptivo, las siguientes
    posiciones corresponden a las ventas en kilos o euros (dependiendo
    del texto que la encabece) por cada mes y en orden. La última 
    posición se deja vacía ya que no se mostrará en el TreeView.
    «meses» es una lista o una tupla con los meses del año sobre los 
    que consultar datos (comenzando en 1).
    """
    # Ejecuto consulta:
    if vpro != None:
        incr_progreso = rango / 5.0
    vi = buscar_ventas_internas_fibra(anno, vpro, rango, meses)
    if vpro != None:
        vpro.set_valor(vpro.get_valor() + incr_progreso, vpro.get_texto())
    vbb = buscar_ventas_bigbags(anno, vpro, rango, meses)
    if vpro != None:
        vpro.set_valor(vpro.get_valor() + incr_progreso, vpro.get_texto())
    vpc = buscar_ventas_por_color(anno, vpro, rango, meses)
    if vpro != None:
        vpro.set_valor(vpro.get_valor() + incr_progreso, vpro.get_texto())
    fb = buscar_ventas_fibra_b(anno, vpro, rango, meses)
    if vpro != None:
        vpro.set_valor(vpro.get_valor() + incr_progreso, vpro.get_texto())
    # Organizo datos:
    filas = []
    ## Total
    filas.append(["Total kilos"] + [0.0] * 12)
    filas.append(["Total euros"] + [0.0] * 12)
    ## Geotexan
    filas.append(["Kilos Geotexan"])
    filas.append(["Euros Geotexan"])
    for mes in vi:
        filas[-2].append(vi[mes]['kilos'])
        filas[-1].append(vi[mes]['euros'])
        filas[0][mes+1] += vi[mes]['kilos']
        filas[1][mes+1] += vi[mes]['euros']
    ## Geocem
    filas.append(["Kilos Geocem"])
    filas.append(["Euros Geocem"])
    for mes in vbb:
        filas[-2].append(vbb[mes]['kilos'])
        filas[-1].append(vbb[mes]['euros'])
        filas[0][mes+1] += vbb[mes]['kilos']
        filas[1][mes+1] += vbb[mes]['euros']
    ## Colores
    for color in vpc:
        for extnac in vpc[color]:
            filas.append(["Kilos %s %s (A+B)" % (color, extnac)])
            filas.append(["Euros %s %s (A+B)" % (color, extnac)])
            for mes in vpc[color][extnac]:
                filas[-2].append(vpc[color][extnac][mes]['kilos'])
                filas[-1].append(vpc[color][extnac][mes]['euros'])
                filas[0][mes+1] += vpc[color][extnac][mes]['kilos']
                filas[1][mes+1] += vpc[color][extnac][mes]['euros']
    ## B
    filas.append(["Desglose: kilos fibra B"])
    filas.append(["Desglose: euros fibra B"])
    for mes in fb:
        filas[-2].append(fb[mes]['kilos'])
        filas[-1].append(fb[mes]['euros'])
        # filas[0][mes+1] += fb[mes]['kilos']   # La fibra B no hay que sumarla otra vez. En el desglose por colores ya 
        # filas[1][mes+1] += fb[mes]['euros']   # se incluye fibra B.
    ## CABLE DE FIBRA 
    filas.append(["Fibra reciclada (no computa en el total de ventas)"])
    cable = buscar_ventas_cable(anno, vpro, rango)
    if vpro != None:
        vpro.set_valor(vpro.get_valor() + incr_progreso, vpro.get_texto())
    for mes in cable:
        filas[-1].append(cable[mes]['kilos'])
        # Salen a siempre a 0 € porque son para reciclar y las pagamos al recibirlas de nuevo como granza.
    ## TOTALES 
    for fila in filas:
        total_fila = sum(fila[1:])
        fila += [total_fila, "Me estoy quedando sin fuerzas, solo espero ya la muerte. Me fanta sangre en las venas. Mi corazón se retuerce."]
        for i in xrange(1, len(fila) - 1):
            fila[i] = utils.float2str(fila[i])
    return filas

def buscar_ventas(anno, vpro = None, rango = None, meses = []):
    """
    "anno" es el año del que buscará las ventas.
    """
    gtx = dict([(i, 0) for i in xrange(12)])
    fibra = dict([(i, 0) for i in xrange(12)])
    bolsas = dict([(i, 0) for i in xrange(12)])
    if vpro != None:
        incr_progreso = rango / 12.0
    for i in xrange(12):
        if i+1 not in meses:
            ventas_gtx = {'total': {'metros': 0.0, 'kilos': 0.0, 'euros': 0.0}}
            ventas_fibra = {'total': {'kilos': 0.0, 'euros': 0.0}}
            ventas_bolsas={'total': {'kilos': 0.0, 'bolsas': 0, 'euros': 0.0}}
        else:
            fechaini = mx.DateTime.DateTimeFrom(day=1, month=i+1, year=anno)
            fechafin = mx.DateTime.DateTimeFrom(day=-1, month=i+1, year=anno)
            
            # XXX: No estoy seguro de por qué, pero de repente la versión de 
            #      mx de Sid amd64 ha empezado a devolver -1 como día 
            #      al operar con la fecha, en lugar de convertir los valores 
            #      negativos en días desde el final de mes, como siempre.
            fechafin = utils.asegurar_fecha_positiva(fechafin)
            # XXX

            (ventas_gtx, 
             ventas_fibra, 
             ventas_bolsas) = _buscar_ventas(fechaini, fechafin)
        gtx[i] = ventas_gtx 
        fibra[i] = ventas_fibra
        bolsas[i] = ventas_bolsas
        if vpro != None: 
            vpro.set_valor(vpro.get_valor() + incr_progreso, vpro.get_texto())
    _gtx = {}   # En lugar de [mes][tarifa] voy a hacer un diccionario 
                # [tarifa][mes]

    primeroanno = mx.DateTime.DateTimeFrom(day = 1, month = 1, 
                                           year = mx.DateTime.localtime().year)
    #########################################
    class FakeTarifa:                       #
        def __init__(self, nombre):         #
            self.nombre = nombre            #
    #########################################
    fake_tarifa = FakeTarifa("Tarifas anteriores a %s" % (
                             utils.str_fecha(primeroanno)))
    for mes in gtx:
        for tarifa in gtx[mes]:
            # Filtro por fechaValidezFin de tarifas y agrupar todas las 
            # "caducadas" a principios de año en una sola línea.
            if (tarifa != None and tarifa != "total" 
                and tarifa.periodoValidezFin != None 
                and tarifa.periodoValidezFin < primeroanno):
                _tarifa = fake_tarifa
            else:
                _tarifa = tarifa
            if _tarifa not in _gtx:
                _gtx[_tarifa] = {mes: gtx[mes][tarifa]}
            else:
                if mes not in _gtx[_tarifa]:
                    _gtx[_tarifa][mes] = {}
                for metros_kilos_euros in gtx[mes][tarifa]:
                    algo = gtx[mes][tarifa][metros_kilos_euros]
                    try:
                        _gtx[_tarifa][mes][metros_kilos_euros] += algo
                    except KeyError:
                        _gtx[_tarifa][mes][metros_kilos_euros] = algo
    _fibra = {}
    for mes in fibra:
        for tarifa in fibra[mes]:
            if tarifa not in _fibra:
                _fibra[tarifa] = {mes: fibra[mes][tarifa]}
            else:
                _fibra[tarifa][mes] = fibra[mes][tarifa]
    _bolsas = {}
    for mes in bolsas:
        for tarifa in bolsas[mes]:
            if tarifa not in _bolsas:
                _bolsas[tarifa] = {mes: bolsas[mes][tarifa]}
            else:
                _bolsas[tarifa][mes] = bolsas[mes][tarifa]
    return _gtx, _fibra, _bolsas

def buscar_compras_geocompuestos(anno, vpro = None, rango = None, 
                                 logger = None, meses = []):
    """
    Devuelve un diccionario por proveedor y mes de las compras de producto de 
    tipo geocompuestos, en euros y en metros cuadrados (o la unidad que tenga 
    la mayoría de productos de tipo geocompuesto).
    """
    gcomp = dict([(i, 0) for i in xrange(12)])
    if vpro != None:
        incr_progreso = rango / 12.0
    for i in xrange(12):
        if i+1 not in meses:
            gcompmes = {'total': {'cantidad': 0.0, 'euros': 0.0}}
        else:
            fechaini = mx.DateTime.DateTimeFrom(day=1, month=i+1, year=anno)
            fechafin = mx.DateTime.DateTimeFrom(day=-1, month=i+1, year=anno)
            
            # XXX: No estoy seguro de por qué, pero de repente la versión de 
            #      mx de Sid amd64 ha empezado a devolver -1 como día 
            #      al operar con la fecha, en lugar de convertir los valores 
            #      negativos en días desde el final de mes, como siempre.
            fechafin = utils.asegurar_fecha_positiva(fechafin)
            # XXX

            gcompmes = _buscar_compras_geocompuestos(fechaini, fechafin)
        gcomp[i] = gcompmes
        if vpro != None: 
            vpro.set_valor(vpro.get_valor() + incr_progreso, vpro.get_texto())
    _gcomp = {}     # En lugar de [mes][proveedor] voy a hacer un diccionario 
                    # [proveedor][mes]
    for mes in gcomp:
        for proveedor in gcomp[mes]:
            if proveedor not in _gcomp:
                _gcomp[proveedor] = {mes: gcomp[mes][proveedor]}
            else:
                _gcomp[proveedor][mes] = gcomp[mes][proveedor]
    return _gcomp

def buscar_ventas_geocompuestos(anno, vpro = None, rango = None, 
                                 logger = None, meses = []):
    """
    Devuelve un diccionario por tarifa y mes de las ventas de producto de 
    tipo geocompuestos, en euros y en metros cuadrados.
    """
    gcomp = dict([(i, 0) for i in xrange(12)])
    if vpro != None:
        incr_progreso = rango / 12.0
    for i in xrange(12):
        if i+1 not in meses:
            gcompmes = {'total': {'cantidad': 0.0, 'euros': 0.0}}
        else:
            fechaini = mx.DateTime.DateTimeFrom(day=1, month=i+1, year=anno)
            fechafin = mx.DateTime.DateTimeFrom(day=-1, month=i+1, year=anno)
            
            # XXX: No estoy seguro de por qué, pero de repente la versión de 
            #      mx de Sid amd64 ha empezado a devolver -1 como día 
            #      al operar con la fecha, en lugar de convertir los valores 
            #      negativos en días desde el final de mes, como siempre.
            fechafin = utils.asegurar_fecha_positiva(fechafin)
            # XXX

            gcompmes = _buscar_ventas_geocompuestos(fechaini, fechafin)
        gcomp[i] = gcompmes
        if vpro != None: 
            vpro.set_valor(vpro.get_valor() + incr_progreso, vpro.get_texto())
    _gcomp = {}     # En lugar de [mes][tarifa] voy a hacer un diccionario 
                    # [tarifa][mes]
    for mes in gcomp:
        for tarifa in gcomp[mes]:
            if tarifa not in _gcomp:
                _gcomp[tarifa] = {mes: gcomp[mes][tarifa]}
            else:
                _gcomp[tarifa][mes] = gcomp[mes][tarifa]
    return _gcomp

################## C O N S U M O S #############################################

def consultar_consumos(mes, anno, consumos_gtx, consumos_fibra, 
                       consumos_bolsas):
    ini = mx.DateTime.DateTimeFrom(day = 1, month = mes + 1, year = anno)
    fin = mx.DateTime.DateTimeFrom(day = -1, month = mes + 1, year = anno)
        
    # XXX: No estoy seguro de por qué, pero de repente la versión de mx de 
    #      Sid amd64 ha empezado a devolver -1 como día al operar con la 
    #      fecha, en lugar de convertir los valores negativos en días desde 
    #      el final de mes, como siempre.
    fin = utils.asegurar_fecha_positiva(fin)
    # XXX

    gtx = {}  # @UnusedVariable
    fibra = {}  # @UnusedVariable
    bolsas = {}  # @UnusedVariable
    pdps = pclases.ParteDeProduccion.select(pclases.AND(
            pclases.ParteDeProduccion.q.fecha >= ini, 
            pclases.ParteDeProduccion.q.fecha <= fin))
    for pdp in pdps:
        if pdp.es_de_balas():
            consumos = consumos_fibra
        elif pdp.es_de_geotextiles():
            consumos = consumos_gtx
        elif pdp.es_de_bolsas():
            consumos = consumos_bolsas
        else:
            pass    # Es un parte vacío
        for consumo in pdp.consumos:
            p = consumo.productoCompra
            if p not in consumos:
                consumos[p] = {}
            if mes not in consumos[p]:
                consumos[p][mes] = 0.0
            consumos[p][mes] += consumo.cantidad

def buscar_consumos(anno, vpro = None, rango = None, meses = []):
    """
    "anno" es el año del que buscará los consumos.
    """
    if vpro != None:
        incr_progreso = rango / 12.0
    consumos_gtx = {}
    consumos_fibra = {}
    consumos_bolsas = {}
    for i in xrange(12):
        if i+1 in meses:
            consultar_consumos(i, anno, consumos_gtx, consumos_fibra, 
                               consumos_bolsas)
        if vpro != None: 
            vpro.set_valor(vpro.get_valor() + incr_progreso, vpro.get_texto())
    return consumos_gtx, consumos_fibra, consumos_bolsas

################### P R O D U C C I Ó N   F I B R A ############################
def consultar_horas_reales_fibra(fechaini, fechafin):
    """
    Devuelve la suma de las duraciones de los partes entre las dos 
    fechas recibidas.
    """
    sql = """
        SELECT SUM(fechahorafin - fechahorainicio)
         FROM parte_de_produccion 
         WHERE (fecha >= '%s'                     -- Parámetro fecha ini
                AND fecha <= '%s'                 -- Parámetro fecha fin
                AND observaciones LIKE '%%;%%;%%;%%;%%;%%'
                AND partida_cem_id IS NULL); 
    """ % (fechaini.strftime("%Y-%m-%d"), fechafin.strftime("%Y-%m-%d"))
    try:
        horas_sql = pclases.ParteDeProduccion._queryAll(sql)[0][0]  # @UndefinedVariable
        try:
            horas = horas_sql.hours
        except AttributeError:  # Es un datetime.timedelta
            horas = (horas_sql.days * 24.0) + (horas_sql.seconds / 3600.0)
    except (IndexError, AttributeError):
        horas = 0.0
    return horas

def consultar_horas_trabajo_fibra(fechaini, fechafin, logger):
    """
    Devuelve la suma de las duraciones de los partes entre las dos 
    fechas recibidas menos las horas de parada.
    """
    partes = pclases.ParteDeProduccion.select(""" 
        fecha >= '%s' 
        AND fecha <= '%s' 
        AND observaciones LIKE '%%;%%;%%;%%;%%;%%'
        AND partida_cem_id IS NULL 
        AND observaciones NOT ILIKE '%%reenvas%%'
        """ % (fechaini.strftime("%Y-%m-%d"), fechafin.strftime("%Y-%m-%d")))
    # Ignoro los partes de reenvasado puesto que la máquina no ha estado 
    # produciendo ese tiempo.
    try:
        horas_trabajadas = sum([pdp.get_horas_trabajadas() for pdp in partes])
    except AssertionError, msg:
        txt = "consulta_global::consultar_horas_trabajo_fibra -> Error calculando horas de trabajo de línea de fibra: %s. Ignoro todos los partes implicados en el mismo rango de fechas del que provoca el error." % (msg)
        print txt
        if logger != None:
            logger.error(txt)
        horas_trabajadas = mx.DateTime.DateTimeDelta(0)
    try:
        horas_trabajadas = horas_trabajadas.hours
    except AttributeError:
        try:    # Es un datetime.timedelta
            horas_trabajadas = ((horas_trabajadas.days * 24.0) 
                                + (horas_trabajadas.seconds / 3600.0))
        except AttributeError:
            horas_trabajadas = 0.0
    return horas_trabajadas

def consultar_dias_fibra(fechaini, fechafin):
    """
    Devuelve el número de días (fechas distintas) en los que hay 
    al menos un parte de producción de geotextiles entre las fechas 
    recibidas.
    """ 
    sql = """ 
        SELECT COUNT(DISTINCT fecha) 
         FROM parte_de_produccion
         WHERE (fecha >= '%s'                     -- Parámetro fecha ini
                AND fecha <= '%s'                 -- Parámetro fecha fin
                AND observaciones LIKE '%%;%%;%%;%%;%%;%%'
                AND partida_cem_id IS NULL); 
    """ % (fechaini.strftime("%Y-%m-%d"), fechafin.strftime("%Y-%m-%d"))
    try:
        dias = pclases.ParteDeProduccion._queryAll(sql)[0][0]  # @UndefinedVariable
    except IndexError:
        dias = 0
    return dias

def consultar_dias_bolsas(fechaini, fechafin):
    """
    Devuelve el número de días (fechas distintas) en los que hay 
    al menos un parte de producción de geotextiles entre las fechas 
    recibidas.
    """ 
    sql = """ 
        SELECT COUNT(DISTINCT fecha) 
         FROM parte_de_produccion
         WHERE (fecha >= '%s'                     -- Parámetro fecha ini
                AND fecha <= '%s'                 -- Parámetro fecha fin
                AND partida_cem_id IS NOT NULL); 
    """ % (fechaini.strftime("%Y-%m-%d"), fechafin.strftime("%Y-%m-%d"))
    try:
        dias = pclases.ParteDeProduccion._queryAll(sql)[0][0]  # @UndefinedVariable
    except IndexError:
        dias = 0
    return dias

def consultar_fibra_producida(fechaini, fechafin):
    """
    Ataca a la BD mediante consultas SQL y devuelve los kilos y 
    bultos de fibra fabricados, separados entre bigbags (fibra cemento) 
    y balas; y dentro de éstas, por color.
    """
    partes = """
        SELECT id
         INTO TEMP partes_fib_temp
         FROM parte_de_produccion 
         WHERE (fecha >= '%s'                     -- Parámetro fecha ini
                AND fecha <= '%s'                 -- Parámetro fecha fin
                AND observaciones LIKE '%%;%%;%%;%%;%%;%%'
                AND partida_cem_id IS NULL
                AND observaciones NOT ILIKE '%%reenvas%%');    -- GTX. Hay que escapar los porcientos
    """ % (fechaini.strftime("%Y-%m-%d"), fechafin.strftime("%Y-%m-%d"))
    pvs = """
        SELECT pv.id AS producto_venta_id, color 
         INTO TEMP producto_venta_con_campos_especificos_temp
         FROM campos_especificos_bala ceb, producto_venta pv
         WHERE (pv.campos_especificos_bala_id = ceb.id);
    """
    ids_balas = """
        SELECT bala_id AS id, color
         INTO TEMP ids_balas_fabricadas_temp
         FROM articulo, producto_venta_con_campos_especificos_temp AS pv
         WHERE parte_de_produccion_id IN (SELECT id FROM partes_fib_temp)
           AND articulo.producto_venta_id = pv.producto_venta_id;
    """
    ids_bigbags = """
        SELECT bigbag_id AS id
         INTO TEMP ids_bigbags_fabricados_temp
         FROM articulo 
         WHERE parte_de_produccion_id IN (SELECT id FROM partes_fib_temp);
    """
    balas = """
        SELECT bala.id, pesobala AS peso_ce, color
         INTO TEMP balas_fabricadas_temp
         FROM bala, ids_balas_fabricadas_temp
         WHERE bala.id IN (SELECT id FROM ids_balas_fabricadas_temp)
           AND bala.id = ids_balas_fabricadas_temp.id;
    """
    bigbags = """
        SELECT id, pesobigbag AS peso_ce
         INTO TEMP bigbags_fabricados_temp
         FROM bigbag
         WHERE id IN (SELECT id FROM ids_bigbags_fabricados_temp);
    """
    bultos_kilos_bbs = """
        SELECT COUNT(id), SUM(peso_ce) AS kilos_bb
         FROM bigbags_fabricados_temp;
    """
    bultos_kilos_color_bs = """
        SELECT COUNT(id), SUM(peso_ce) AS kilos_b, color
         FROM balas_fabricadas_temp
         GROUP BY color;
    """
    caidita_de_roma = """
        DROP TABLE balas_fabricadas_temp;
        DROP TABLE bigbags_fabricados_temp;
        DROP TABLE ids_balas_fabricadas_temp;
        DROP TABLE ids_bigbags_fabricados_temp;
        DROP TABLE producto_venta_con_campos_especificos_temp;
        DROP TABLE partes_fib_temp;
    """
    con = pclases.Bala._connection  # En realidad la clase da igual.
    for consulta in (partes, pvs, ids_balas, ids_bigbags, balas, bigbags):
        con.query(consulta)
    balas_kilos_color = con.queryAll(bultos_kilos_color_bs)
    bigbags_kilos = con.queryAll(bultos_kilos_bbs)
    con.query(caidita_de_roma)
    
    balas = {}
    for fila in balas_kilos_color:
        bultos_balas, kilos_ce, color = fila
        balas[color] = {'bultos': bultos_balas and bultos_balas or 0.0, 
                        'kilos': kilos_ce and kilos_ce or 0.0} 
    bultos_bigbags, kilos_ce = bigbags_kilos[0]
    bigbags = {'bultos': bultos_bigbags and bultos_bigbags or 0.0, 
               'kilos': kilos_ce and kilos_ce or 0.0}
    
    # Clase B
    bultos_bs_b, kilos_bs_b, bultos_bbs_b, kilos_bbs_b = consultar_fibra_b(fechaini, fechafin)
    balas['_FIBRACLASE_B_'] = {'bultos': bultos_bs_b and bultos_bs_b or 0.0, 
                               'kilos': kilos_bs_b and kilos_bs_b or 0.0}
    bigbags['_FIBRACLASE_B_'] = {'bultos': bultos_bbs_b and bultos_bbs_b or 0.0,
                                 'kilos': kilos_bbs_b and kilos_bbs_b or 0.0}
    return balas, bigbags

def consultar_fibra_b(fechaini, fechafin):
    """
    Devuelve la fibra de clase B separada en balas y bigbags, 
    kilos y bultos.
    """
    partes = """
        SELECT id
         INTO TEMP partes_fib_temp
         FROM parte_de_produccion 
         WHERE (fecha >= '%s'                     -- Parámetro fecha ini
                AND fecha <= '%s'                 -- Parámetro fecha fin
                AND observaciones LIKE '%%;%%;%%;%%;%%;%%'
                AND partida_cem_id IS NULL 
                AND observaciones NOT ILIKE '%%reenvas%%');    -- GTX. Hay que escapar los porcientos
    """ % (fechaini.strftime("%Y-%m-%d"), fechafin.strftime("%Y-%m-%d"))
    ids_balas = """
        SELECT bala_id AS id
         INTO TEMP ids_balas_fabricadas_temp
         FROM articulo
         WHERE parte_de_produccion_id IN (SELECT id FROM partes_fib_temp);
    """
    ids_bigbags = """
        SELECT bigbag_id AS id
         INTO TEMP ids_bigbags_fabricados_temp
         FROM articulo 
         WHERE parte_de_produccion_id IN (SELECT id FROM partes_fib_temp);
    """
    balas = """
        SELECT bala.id, pesobala AS peso_ce
         INTO TEMP balas_fabricadas_temp
         FROM bala
         WHERE id IN (SELECT id FROM ids_balas_fabricadas_temp)
            AND bala.claseb;
    """
    bigbags = """
        SELECT id, pesobigbag AS peso_ce
         INTO TEMP bigbags_fabricados_temp
         FROM bigbag
         WHERE id IN (SELECT id FROM ids_bigbags_fabricados_temp)
            AND bigbag.claseb;
    """
    bultos_kilos_bbs = """
        SELECT COUNT(id), SUM(peso_ce) AS kilos_bb
         FROM bigbags_fabricados_temp;
    """
    bultos_kilos_color_bs = """
        SELECT COUNT(id), SUM(peso_ce) AS kilos_b
         FROM balas_fabricadas_temp
    """
    caidita_de_roma = """
        DROP TABLE balas_fabricadas_temp;
        DROP TABLE bigbags_fabricados_temp;
        DROP TABLE ids_balas_fabricadas_temp;
        DROP TABLE ids_bigbags_fabricados_temp;
        DROP TABLE partes_fib_temp;
    """
    con = pclases.Bala._connection  # En realidad la clase da igual.
    for consulta in (partes, ids_balas, ids_bigbags, balas, bigbags):
        con.query(consulta)
    balas_kilos = con.queryAll(bultos_kilos_color_bs)
    bigbags_kilos = con.queryAll(bultos_kilos_bbs)
    con.query(caidita_de_roma)
    bultos_bs_b, kilos_bs_b = balas_kilos[0]
    bultos_bbs_b, kilos_bbs_b = bigbags_kilos[0]
    return bultos_bs_b, kilos_bs_b, bultos_bbs_b, kilos_bbs_b

def consultar_granza_consumida(fechaini, fechafin):
    """
    Devuelve la granza consumida por los partes de producción de fibra 
    entre las fechas fechaini y fechafin en forma de diccionario 
    cuyas claves son el tipo de granza.
    """
    PDP = pclases.ParteDeProduccion
    parte_where = (""" fecha >= '%s' 
                       AND fecha <= '%s' 
                       AND observaciones LIKE '%%;%%;%%;%%;%%;%%' 
                       AND partida_cem_id IS NULL 
                    """ % (fechaini.strftime("%Y-%m-%d"), 
                           fechafin.strftime("%Y-%m-%d")))
    pdps = PDP.select(parte_where)
    granza = 0.0
    granza_reciclada = 0.0
    # OJO: NOTA: WARNING: ATCHUNG: HARCODED: Etcétera, etcétera. La separación 
    #                                        de la granza del resto de materia 
    #                                        prima y a su vez la separación 
    #                                        entre granza {reciclada|recuperada}
    #                                        de las demás es totalmente 
    #                                        arbitraria, a ojo y harcoded. Lo 
    #                                        ideal es que tuvieran un campo en 
    #                                        ProductoCompra o que hubiera un 
    #                                        TipoDeMaterial que las 
    #                                        distinguiese, pero -como siempre- 
    #                                        ni era un requisito ni hay tiempo 
    #                                        ahora de verificar que el cambio 
    #                                        no afecta a todo el código que 
    #                                        tira de TipoDeMaterial en el resto 
    #                                        de ventanas.
    for pdp in pdps:
        for c in pdp.consumos:
            desc = c.productoCompra.descripcion.upper()
            if "GRANZA" in desc:
                if "RECICLADA" in desc or "RECUPERADA" in desc:
                    granza_reciclada += c.cantidad
                else:
                    granza += c.cantidad
    return {'total': granza + granza_reciclada, 
            'granza': granza, 
            'reciclada': granza_reciclada}

def consultar_empleados_por_dia_fibra(fechaini, fechafin):
    """
    Devuelve el número de empleados por día a través de una tocho-consulta(TM) 
    a la base de datos.
    """
    sql = """
    SELECT fecha, empleadoid 
    FROM parte_de_produccion_empleado, 
         (SELECT id,fecha 
          FROM parte_de_produccion 
          WHERE fecha >= '%s' 
            AND fecha <= '%s' 
            AND observaciones LIKE '%%;%%;%%;%%;%%;%%'
            AND partida_cem_id IS NULL) AS partes 
    WHERE partes.id = parte_de_produccion_empleado.partedeproduccionid 
    GROUP BY fecha, empleadoid ORDER BY fecha; """ % (
        fechaini.strftime("%Y-%m-%d"), fechafin.strftime("%Y-%m-%d"))
    filas_fecha_idempleado = pclases.ParteDeProduccion._queryAll(sql)  # @UndefinedVariable
    # Y ahora sumo (lo sé, se podría hacer directamente en la consulta, pero 
    # prefiero dejarla así porque creo que me hará falta en un futuro tenerlo 
    # desglosado).
    fechas = []
    empleados = 0.0
    for fecha, idempleado in filas_fecha_idempleado:  # @UnusedVariable
        if fecha not in fechas:
            fechas.append(fecha)
        empleados += 1
    try:
        res = empleados / len(fechas)
    except ZeroDivisionError:
        res = 0.0
    return res

def consultar_productividad_fibra(fechaini, fechafin):
    """
    Devuelve la productividad de los partes de producción de 
    geotextiles entre las fechas recibidas.
    """ 
    sql_where = """ fecha >= '%s' 
                    AND fecha <= '%s' 
                    AND observaciones LIKE '%%;%%;%%;%%;%%;%%' 
                    AND partida_cem_id IS NULL 
                """ % (fechaini.strftime("%Y-%m-%d"), 
                       fechafin.strftime("%Y-%m-%d"))
    pdps = pclases.ParteDeProduccion.select(sql_where)
    return calcular_productividad_conjunta(pdps)

def buscar_produccion_fibra(anno, 
                            vpro = None, 
                            rango = None, 
                            logger = None, 
                            meses = []):
    """
    "anno" es el año del que buscará las producciones.
    Devuelve un diccionario _por meses_ con los kilos fabricados y 
    granza consumida.
    """
    if vpro != None:
        incr_progreso = rango / 12.0
    res = dict([(i, 0) for i in xrange(12)])
    for i in xrange(12):
        if i+1 not in meses:
            res[i] = {'total': 0,  
                      'consumo_total': 0}
            res[i]["colores"] = {}
            res[i]['cemento'] = 0
            res[i]['merma'] = 0
            res[i]['porc_merma'] = 0
            res[i]['granza'] = 0
            res[i]['reciclada'] = 0
            res[i]['media_bala'] = 0
            res[i]['media_bigbag'] = 0
            res[i]['kilos_b'] = 0
            res[i]['kilos_hora'] = 0
            res[i]['horas'] = 0
            res[i]['horas_produccion'] = 0
            res[i]['dias'] = 0
            res[i]['turnos'] = 0
            res[i]['empleados'] = 0
            res[i]['productividad'] = 0
            res[i]['balas_cable'] = {'total': 0}
        else:
            fechaini = mx.DateTime.DateTimeFrom(day=1, month=i+1, year=anno)
            fechafin = mx.DateTime.DateTimeFrom(day=-1, month=i+1, year=anno)
            # XXX: No estoy seguro de por qué, pero de repente la versión de 
            #      mx de Sid amd64 ha empezado a devolver -1 como día al 
            #      operar con la fecha, en lugar de convertir los valores 
            #      negativos en días desde el final de mes, como siempre.
            fechafin = utils.asegurar_fecha_positiva(fechafin)
            # XXX
            bs, bbs = consultar_fibra_producida(fechaini, fechafin)
            consumos_materia_prima_del_mes = consultar_granza_consumida(fechaini, fechafin)
            res[i] = {'total': bbs['kilos'] + sum([bs[color]['kilos'] for color in bs if color != "_FIBRACLASE_B_"]), 
                        # _FIBRACLASE_B_ es un desglose de la fibra B. 
                        # Va también incluida en los colores, así que no hay 
                        # que sumarla dos veces al total.
                      'consumo_total': consumos_materia_prima_del_mes['total']}
            res[i]["colores"] = {}
            for color in bs:
                if color != "_FIBRACLASE_B_":   
                                # La clave "_FIBRACLASE_B_" se reserva para la 
                                # fibra "claseb" (espero que a nadie se le 
                                # ocurra dar de alta el color "_FIBRACLASE_B_"
                    res[i]["colores"][color] = bs[color]['kilos']
            res[i]['cemento'] = bbs['kilos']
            res[i]['merma'] = res[i]['consumo_total'] - res[i]['total']
            try:
                res[i]['porc_merma'] = (1.0 - (res[i]['total'] / res[i]['consumo_total'])) * 100.0
            except ZeroDivisionError:
                res[i]['porc_merma'] = 0.0
            res[i]['granza'] = consumos_materia_prima_del_mes['granza']
            res[i]['reciclada'] = consumos_materia_prima_del_mes['reciclada']
            try:
                res[i]['media_bala'] = sum([bs[color]['kilos'] for color in bs]) / sum([bs[color]['bultos'] for color in bs])
            except ZeroDivisionError:
                res[i]['media_bala'] = 0.0
            try:
                res[i]['media_bigbag'] = bbs['kilos'] / bbs['bultos']
            except ZeroDivisionError: 
                res[i]['media_bigbag'] = 0.0
            res[i]['kilos_b'] = bs['_FIBRACLASE_B_']['kilos'] + bbs['_FIBRACLASE_B_']['kilos']
            horas = consultar_horas_reales_fibra(fechaini, fechafin)
            horas_trabajo = consultar_horas_trabajo_fibra(fechaini, fechafin, logger)
            try:
                kilos_hora = (res[i]['total']) / horas_trabajo
            except ZeroDivisionError:
                kilos_hora = 0.0
            res[i]['kilos_hora'] = kilos_hora
            res[i]['horas'] = horas
            res[i]['horas_produccion'] = horas_trabajo
            dias = consultar_dias_fibra(fechaini, fechafin)
            res[i]['dias'] = dias
            try:
                turnos = (horas / 8.0) / dias
            except ZeroDivisionError:
                turnos = 0.0
            res[i]['turnos'] = turnos
            empleados_dia = consultar_empleados_por_dia_fibra(fechaini, fechafin)
            res[i]['empleados'] = empleados_dia
            res[i]['productividad'] = consultar_productividad_fibra(fechaini, fechafin)
            # Actualización 04/07/2007: Una línea más para la fibra reciclada. 
            # Agrupo toda en una sola línea y no la cuento para 
            # totales de fibra producida. A fin de cuentas, no es realmente 
            # fibra. Son residuos que se embalan para reciclar y no 
            # consumen *estrictamente* granza. (Está claro que sí consumen, 
            # de algún lado debe salir, pero es imposible determinar 
            # de qué materia prima viene cada. Son restos que se van 
            # acumulando a lo largo de los turnos).
            res[i]['balas_cable'] = {'total': sum([bc.peso for bc in pclases.BalaCable.select(pclases.AND(
                                                        pclases.BalaCable.q.fechahora >= fechaini, 
                                                        pclases.BalaCable.q.fechahora < fechafin + mx.DateTime.oneDay))])}
            for ceb_reciclada in pclases.CamposEspecificosBala.select(pclases.CamposEspecificosBala.q.reciclada == True):
                descripcion = ceb_reciclada.productosVenta[0].descripcion
                pesos = [bc.peso 
                         for bc in pclases.BalaCable.select(pclases.AND(
                             pclases.BalaCable.q.fechahora >= fechaini, 
                             pclases.BalaCable.q.fechahora < 
                                fechafin + mx.DateTime.oneDay, 
                             pclases.BalaCable.q.id == 
                                pclases.Articulo.q.balaCableID, 
                             pclases.Articulo.q.productoVentaID == 
                                ceb_reciclada.productosVenta[0].id))]
                res[i]['balas_cable'][descripcion] = sum(pesos)
        if vpro != None: vpro.set_valor(vpro.get_valor() + incr_progreso, vpro.get_texto())
    return res

################################################################################

def preparar_tv(tv, listview = True):
    """
    Prepara las columnas del TreeView.
    Si listview es True usa un ListStore como modelo de datos. En 
    otro caso usa un TreeStore.
    """
    cols = (('', 'gobject.TYPE_STRING', False, True, True, None),
            ('Enero', 'gobject.TYPE_STRING', False, False, False, None), 
            ('Febrero', 'gobject.TYPE_STRING', False, False, False, None), 
            ('Marzo', 'gobject.TYPE_STRING', False, False, False, None),
            ('Abril', 'gobject.TYPE_STRING', False, False, False, None),
            ('Mayo', 'gobject.TYPE_STRING', False, False, False, None), 
            ('Junio', 'gobject.TYPE_STRING', False, False, False, None), 
            ('Julio', 'gobject.TYPE_STRING', False, False, False, None), 
            ('Agosto', 'gobject.TYPE_STRING', False, False, False, None), 
            ('Septiembre', 'gobject.TYPE_STRING', False, False, False, None), 
            ('Octubre', 'gobject.TYPE_STRING', False, False, False, None), 
            ('Noviembre', 'gobject.TYPE_STRING', False, False, False, None), 
            ('Diciembre', 'gobject.TYPE_STRING', False, False, False, None), 
            ('Anual', 'gobject.TYPE_STRING', False, False, False, None), 
            ('Rocío', 'gobject.TYPE_STRING', False, False, False, None))
    if listview:
        utils.preparar_listview(tv, cols)
    else:
        utils.preparar_treeview(tv, cols)
    for col in tv.get_columns()[1:]:
        for cell in col.get_cell_renderers():
            cell.set_property("xalign", 1.0)
        col.set_alignment(0.5)

def consultar_gtxc(fechaini, fechafin):
    """
    Devuelve los kg de geotextiles C producidos entre fechaini y 
    fechafin.
    No devuelve m² porque de los geotextiles C solo se guarda el peso.
    """
    fini = fechaini
    ffin = fechafin + mx.DateTime.oneDay
    rollosc = pclases.RolloC.select(pclases.AND(
                pclases.RolloC.q.fechahora >= fini, 
                pclases.RolloC.q.fechahora < ffin))
    return rollosc.sum("peso")

if __name__ == '__main__':
    import sys
    try:
        t = ConsultaGlobal(
            usuario = pclases.Usuario.get(int(sys.argv[1])))
    except:
        t = ConsultaGlobal(
            usuario = pclases.Usuario.selectBy(usuario = "nicolas")[0])

