#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Módulo de intercambio de información con otros ERP.
"""

from setuptools import setup

setup(name="ginn_api",
      version='1.2',
      description="API ginn-Sage Murano / netdata / SAP",
      url="https://github.com/pacoqueen/ginn",
      author="Francisco José Rodríguez Bogado",
      author_email="frbogado@geotexan.com",
      license="GPL3",
      packages=["murano", "netdata", "sap"])
