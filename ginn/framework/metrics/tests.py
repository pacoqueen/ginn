#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_import(self):
        try:
            import core     # noqa
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

    def test_get_existencias_virtuales(self):
        from core import get_existencias_virtuales
        data = get_existencias_virtuales(None)
        # Si se le llama sin productos, debe devolver None o cero.
        # Ya haré otra más "seria" para cunado se invoca de manera normal.
        assert not data

    def test_get_no_volcado(self):
        from core import get_no_volcado
        data = get_no_volcado(None)
        assert data == 0

    def test_importaciones_murano(self):
        from core import importaciones_murano
        data = importaciones_murano()
        assert isinstance(data, dict)


if __name__ == '__main__':
    unittest.main()
