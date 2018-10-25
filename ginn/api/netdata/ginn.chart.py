# -*- coding: utf-8 -*-
# Description: example netdata python.d module
# Author: Put your name here (your github login)
# SPDX-License-Identifier: GPL-3.0-or-later

from random import SystemRandom

from bases.FrameworkServices.SimpleService import SimpleService

import os
import sys
import datetime
sys.path.append(os.path.join('/', 'home', 'compartido', 'ginn', 'ginn'))
from framework import pclases

# default module values
# update_every = 4
priority = 90000
retries = 60

ORDER = ['articulos', 'produccion'] # , 'random']
CHARTS = {
#    'random': {
#        'options': [None, 'A random number', 'ordinal', 'random', 'random',
#                    'line'],
#        'lines': [
#            ['random1']
#        ]
#    },
    'articulos': {
        'options': [None, 'Articulos fabricados', 'bultos', 'articulos',
                    'produccion', 'line'],
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
    'produccion': {
        'options': [None, 'Producción a la hora', 'kg/hora', 'articulos',
                    'produccion', 'line'],
        'lines': [
            ['kg fibra A+B', "fibra A+B", 'absolute'],
            ['kg fibra C', "fibra C", 'absolute'],
            ['kg fibra bigbag', "bigbag", 'absolute'],
            ['kg fibra cemento', "cemento", 'absolute'],
            ['kg geotextiles A', "gtx A", 'absolute'],
            ['kg geotextiles B', "gtx B", 'absolute'],
            ['kg geotextiles C', "gtx C", 'absolute']
        ]
    }
}


class Service(SimpleService):
    def __init__(self, configuration=None, name=None):
        SimpleService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        self.random = SystemRandom()

    @staticmethod
    def check():
        return True

    def get_data(self):
        return self._get_data()

    def _get_data(self):
        data = dict()
        # Datos para el gráfico de prueba (números aleatorios)
        # for i in range(1, 4):
        #     dimension_id = ''.join(['random', str(i)])
        #     if dimension_id not in self.charts['random']:
        #         self.charts['random'].add_dimension([dimension_id])
        #     data[dimension_id] = self.random.randint(0, 100)
        # Datos para el gráfico de productos terminados (almacén)
        raw = self._get_raw_data()
        data['balas A+B'] = raw[pclases.Bala]['bultos']
        data['balas C'] = raw[pclases.BalaCable]['bultos']
        data['bigbag'] = raw[pclases.Bigbag]['bultos']
        data['cajas'] = raw[pclases.Caja]['bultos']
        data['pales'] = raw[pclases.Pale]['bultos']
        data['rollos A'] = raw[pclases.Rollo]['bultos']
        data['rollos B'] = raw[pclases.RolloDefectuoso]['bultos']
        data['rollos C'] = raw[pclases.RolloC]['bultos']
        # Datos para el gráfico de kg frabricados (producción)
        data['kg fibra A+B'] = raw[pclases.Bala]['kg']
        data['kg fibra C'] = raw[pclases.BalaCable]['kg']
        data['kg fibra bigbag'] = raw[pclases.Bigbag]['kg']
        data['kg fibra cemento'] = raw[pclases.Caja]['kg']
        data['kg geotextiles A'] = raw[pclases.Rollo]['kg']
        data['kg geotextiles B'] = raw[pclases.RolloDefectuoso]['kg']
        data['kg geotextiles C'] = raw[pclases.RolloC]['kg']
        return data

    def _get_raw_data(self):
        data = {}
        clases = (pclases.Bala, pclases.BalaCable, pclases.Bigbag,
                  pclases.Caja, pclases.Pale, pclases.Rollo,
                  pclases.RolloDefectuoso, pclases.RolloC)
        for clase in clases:
            data[clase] = dict()
            data[clase]['bultos'] = clase.select().count()
            if 4 <= datetime.datetime.now().month <= 10:
                # UGLY HACK: daylight saving + timezone UTC+1
                antes = datetime.datetime.now()-datetime.timedelta(hours=3)
            else:
                antes = datetime.datetime.now()-datetime.timedelta(hours=2)
            # kg fabricados en la última hora
            select_results = clase.select(clase.q.fechahora >= antes)
            for dim_name in ('pesobala', 'peso', 'pesobigbag'):
                try:
                    if select_results.count():
                        mean = select_results.sum(dim_name)
                    else:
                        mean = 0
                    data[clase]['kg'] = mean
                except Exception:
                    data[clase]['kg'] = 0
                    continue
                else:
                    break
        return data
