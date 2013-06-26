#!/usr/bin/env python
# -*- coding: utf-8 -*-

PYCALLGRAPH = False

import sys, os
ruta_ginn = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "ginn"))
sys.path.append(ruta_ginn)
from framework import pclases

if PYCALLGRAPH:
    ruta_pycallgraph = os.path.abspath(os.path.join(os.environ["HOME"], "bin", "pycallgraph"))
    sys.path.append(ruta_pycallgraph)
    import pycallgraph
else:
    import cProfile, pstats, time

def test_cetco():
    clientes = pclases.Cliente.select(pclases.Cliente.q.nombre.contains("CETCO"))
    for c in clientes:
        print "Cliente:", c.nombre, "- Crédito:", c.calcular_credito_disponible()

def main():
    if PYCALLGRAPH:
        pycallgraph.start_trace()
        test_cetco()
        pycallgaph.make_dot_graph(os.path.join(os.path.dirname(__file__), 
            "..", "doc", "calcular_credito_disponible.png"))
    else:
        fechahora = time.localtime()
        fechahora = "%d%02d%02d%02d%02d%02d" % (fechahora.tm_year, 
                                                fechahora.tm_mon, 
                                                fechahora.tm_mday, 
                                                fechahora.tm_hour, 
                                                fechahora.tm_min, 
                                                fechahora.tm_sec)
        filestats = os.path.abspath(os.path.join(os.path.dirname(__file__), 
            "..", "doc", "credito_perf_%s.stats" % fechahora))
        #cProfile.run("test_cetco()", sort = 'cumulative')
        cProfile.run("test_cetco()", filestats, sort = 'cumulative')
        p = pstats.Stats(filestats)
        p.strip_dirs().sort_stats("time").print_stats(10)
        p.strip_dirs().sort_stats("cumulative").print_stats(10)

if __name__ == "__main__":
    main()

