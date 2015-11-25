#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
ruta_ginn = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "ginn"))
sys.path.append(ruta_ginn)
from framework import pclases
from api import murano

b = pclases.Bala.select(orderBy = "-id")[0]
murano.create_bala(b)
