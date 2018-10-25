# -*- coding: utf-8 -*-
# Description: example netdata python.d module
# Author: Put your name here (your github login)
# SPDX-License-Identifier: GPL-3.0-or-later

from random import SystemRandom

from bases.FrameworkServices.SimpleService import SimpleService

# default module values
# update_every = 4
priority = 90000
retries = 60

ORDER = ['random']
CHART = {
    'random': {
        'options': [None, 'A random number', 'ordinal', 'random', 'random', 'line'],
        'lines': [
            ['random1']
        ]
    }
}


class Service(SimpleService):
    def __init__(self, configuration=None, name=None):
        SimpleService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHART
        self.random = SystemRandom()

    @staticmethod
    def check():
        return True

    def get_data(self):
        data = dict()

        for i in range(1, 4):
            dimension_id = ''.join(['random', str(i)])

            if dimension_id not in self.charts['random']:
                self.charts['random'].add_dimension([dimension_id])

            raw = self._get_raw_data()
            data[dimension_id] = raw

        return data

    def _get_data(self):
        return self.get_data()

    def _get_raw_data(self):
        data = self.random.randint(0, 100)
        return data
