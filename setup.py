#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Geotex-INN',
    'author': 'Francisco José Rodríguez Bogado',
    'url': 'http://sourceforge.net/projects/ginn',
    'download_url': 'https://github.com/pacoqueen/ginn',
    'author_email': 'bogado@qinn.es',
    'version': '5.0.1 (alpha)',
    'install_requires': ['nose', 'sqlobject', 'pygtk >= 2.0', 'reportlab', 'psycopg2'],
    'packages': ['ginn'],
    'scripts': ['bin/ginn.sh'],
    'name': 'ginn'
}

setup(**config)

