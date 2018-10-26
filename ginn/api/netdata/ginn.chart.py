# -*- coding: utf-8 -*-
# Description: example netdata python.d module
# Author: Put your name here (your github login)
# SPDX-License-Identifier: GPL-3.0-or-later

# from random import SystemRandom

from bases.FrameworkServices.SimpleService import SimpleService

import os
import sys
try:
    from framework import metrics
except ImportError:
    sys.path.append(os.path.join('/', 'home', 'compartido', 'ginn', 'ginn'))
    from framework import metrics


priority = 90000
retries = 60

ORDER = ['almacen', 'produccion', 'articulos', 'producido']
CHARTS = {
    'articulos': {
        'options': [None, 'Articulos fabricados', 'bultos', 'articulos',
                    'produccion', 'area'],
        'lines': [
            ['balas A+B', None, 'absolute'],
            ['balas C', None, 'absolute'],
            ['bigbag', None, 'absolute'],
            ['cajas', None, 'absolute'],
            ['pales', None, 'absolute'],
            ['rollos A', None, 'absolute'],
            ['rollos B', None, 'absolute'],
            ['rollos C', None, 'absolute']
        ]
    },
    'producido': {
        'options': [None, 'kg fabricados', 'kg', 'articulos',
                    'produccion', 'stacked'],
        'lines': [
            ['kg fibra A+B', "fibra A+B", 'absolute'],
            ['kg fibra C', "fibra C", 'absolute'],
            ['kg fibra bigbag', "bigbag", 'absolute'],
            ['kg fibra cemento', "cemento", 'absolute'],
            ['kg geotextiles A', "gtx A", 'absolute'],
            ['kg geotextiles B', "gtx B", 'absolute'],
            ['kg geotextiles C', "gtx C", 'absolute']
        ]
    },
    'produccion': {
        'options': ['productividad', 'Produccion a la hora', 'kg/hora',
                    'produccion', 'produccion', 'line', None, 10],
        'lines': [
            ['kghora fibra A+B', "fibra A+B", 'absolute'],
            ['kghora fibra C', "fibra C", 'absolute'],
            ['kghora fibra bigbag', "bigbag", 'absolute'],
            ['kghora fibra cemento', "cemento", 'absolute'],
            ['kghora geotextiles A', "gtx A", 'absolute'],
            ['kghora geotextiles B', "gtx B", 'absolute'],
            ['kghora geotextiles C', "gtx C", 'absolute']
        ]
    },
    'almacen': {
        'options': ['stock', 'Existencias', 'kg',
                    'articulos', 'produccion', 'stacked', None, 10],
        'lines': [
            ['productoVenta']
        ]
    }
}


class Service(SimpleService):
    def __init__(self, configuration=None, name=None):
        SimpleService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        # self.random = SystemRandom()

    @staticmethod
    def check():
        return True

    def get_data(self):
        return self._get_data()

    def _get_data(self):
        data = dict()
        # Datos para el gráfico de productos terminados (almacén)
        raw = self._get_raw_data()
        data['balas A+B'] = raw[metrics.Bala]['bultos']
        data['balas C'] = raw[metrics.BalaCable]['bultos']
        data['bigbag'] = raw[metrics.Bigbag]['bultos']
        data['cajas'] = raw[metrics.Caja]['bultos']
        data['pales'] = raw[metrics.Pale]['bultos']
        data['rollos A'] = raw[metrics.Rollo]['bultos']
        data['rollos B'] = raw[metrics.RolloDefectuoso]['bultos']
        data['rollos C'] = raw[metrics.RolloC]['bultos']
        # Datos para el gráfico de kg frabricados (almacén)
        data['kg fibra A+B'] = raw[metrics.Bala]['kg']
        data['kg fibra C'] = raw[metrics.BalaCable]['kg']
        data['kg fibra bigbag'] = raw[metrics.Bigbag]['kg']
        data['kg fibra cemento'] = raw[metrics.Caja]['kg']
        data['kg geotextiles A'] = raw[metrics.Rollo]['kg']
        data['kg geotextiles B'] = raw[metrics.RolloDefectuoso]['kg']
        data['kg geotextiles C'] = raw[metrics.RolloC]['kg']
        # Datos para el gráfico de kg frabricados (producción)
        data['kghora fibra A+B'] = raw[metrics.Bala]['kghora']
        data['kghora fibra C'] = raw[metrics.BalaCable]['kghora']
        data['kghora fibra bigbag'] = raw[metrics.Bigbag]['kghora']
        data['kghora fibra cemento'] = raw[metrics.Caja]['kghora']
        data['kghora geotextiles A'] = raw[metrics.Rollo]['kghora']
        data['kghora geotextiles B'] = raw[metrics.RolloDefectuoso]['kghora']
        data['kghora geotextiles C'] = raw[metrics.RolloC]['kghora']
        # Datos de producciones estándar
        for linea in ('fibra', 'geotextiles', 'cemento'):
            if raw[linea]['producto'] is not None:
                leyenda = raw[linea]['producto'].nombre
                prodestandar = raw[linea]['kghora']
                if not prodestandar:
                    prodestandar = -1   # Para **destacar** la fibra a 0 kg/h.
                if leyenda not in self.charts['produccion']:
                    self.charts['produccion'].add_dimension([leyenda])
                data[leyenda] = prodestandar
        # Datos de almacén de productos fabricándose
        for clave in raw.keys():    # Recorro TODOS los datos.
            if isinstance(clave, metrics.ProductoVenta):
                producto = clave
                for calidad in raw[producto].keys():
                    leyenda = "[{}] {}".format(calidad, producto.nombre)
                    existencias = raw[producto][calidad]['KG']
                    if leyenda not in self.charts['almacen']:
                        self.charts['almacen'].add_dimension([leyenda])
                    data[leyenda] = existencias
        return data

    def _get_raw_data(self):
        # Bultos y kg fabricados {clase: {dimensión: valor}, ...}
        data = metrics.bultos_fabricados()
        # Los datos de producción estándar de los partes abiertos
        # {'fibra|geotextiles|cemento': {'producto': productoVenta,
        #                                'kghora': valor}}
        data_referencia = metrics.produccion_estandar()
        productos_fabricandose = []
        for linea in data_referencia:
            data[linea] = data_referencia[linea]
            if data[linea]['producto']:
                productos_fabricandose.append(data[linea]['producto'])
        data_existencias = metrics.get_existencias(productos_fabricandose)
        for clave in data_existencias:
            data[clave] = data_existencias[clave]
        return data
