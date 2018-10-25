# -*- coding: utf-8 -*-
# Description: example netdata python.d module
# Author: Put your name here (your github login)
# SPDX-License-Identifier: GPL-3.0-or-later

from random import SystemRandom

from bases.FrameworkServices.SimpleService import SimpleService

import os, sys
sys.path.append(os.path.join('/', 'home', 'compartido', 'ginn', 'ginn'))
from framework import pclases

# default module values
# update_every = 4
priority = 90000
retries = 60

ORDER = ['articulos', 'random']
CHARTS = {
    'random': {
        'options': [None, 'A random number', 'ordinal', 'random', 'random',
                    'line'],
        'lines': [
            ['random1']
        ]
    },
    'articulos': {
        'options': [None, 'Articulos fabricados', 'bultos', 'articulos',
                    'produccion', 'line'],
        'lines': [
            ['balas A+B', 'balas C', 'bigbag', 'cajas', 'pales', 'rollos A',
                'rollos B', 'rollos C']
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
        for i in range(1, 4):
            dimension_id = ''.join(['random', str(i)])
            if dimension_id not in self.charts['random']:
                self.charts['random'].add_dimension([dimension_id])
            data[dimension_id] = self.random.randint(0, 100)
        # Datos para el gráfico de producción
        raw = self._get_raw_data()
        data['balas A+B'] = raw[pclases.Bala]
        data['balas C'] = raw[pclases.BalaCable]
        data['bigbag'] = raw[pclases.Bigbag]
        data['cajas'] = raw[pclases.Caja]
        data['pales'] = raw[pclases.Pale]
        data['rollos A'] = raw[pclases.Rollo]
        data['rollos B'] = raw[pclases.RolloDefectuoso]
        data['rollos C'] = raw[pclases.RolloC]
        return data

    def _get_raw_data(self):
        data = {}
        for clase in (pclases.Bala, pclases.BalaCable, pclases.Bigbag,
                      pclases.Caja, pclases.Pale, pclases.Rollo,
                      pclases.RolloDefectuoso, pclases.RolloC):
            data[clase] = clase.select().count()
        return data
