#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_import(self):
        try:
            from core import *                                      # noqa
            assert True
        except ImportError:
            assert False

    def test_bultos_fabricados(self):
        from core import bultos_fabricados
        bultos = bultos_fabricados()
        assert isinstance(bultos, dict)

    def test_produccion_estandar(self):
        from core import produccion_estandar
        data = produccion_estandar()
        assert isinstance(data, dict)

    def test_get_existencias(self):
        from core import get_existencias
        data = get_existencias()
        assert isinstance(data, dict)

if __name__ == '__main__':
    unittest.main()
