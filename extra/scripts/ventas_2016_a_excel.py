#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Crea un CSV con los totales de las bases imponibles facturadas entre el 1 de
enero de 2016 y el 1 de junio de 2016, agrupadas **por nombre de cliente**.
"""

import csv
import sys
import datetime
try:
    from framework import pclases
except ImportError:
    print "Trata de exportar primero el PYTHONPATH dentro de ginn tal que así:"\
            " cd ...Geotex-INN/ginn; export PYTHONPATH=$PYTHONPATH:."

def buscar_facturas(fini, ffin):
    """
    Busca todas las facturas entre las fechas recibidas. La inicial incluida y
    la final excluida.
    """
    # pylint: disable=no-member
    fras = pclases.FacturaVenta.select(pclases.AND(
        pclases.FacturaVenta.q.fecha >= fini,
        pclases.FacturaVenta.q.fecha < ffin), orderBy="fecha")
    return [fra for fra in fras]

def acumular_facturas(fras):
    """
    Recibe una lista de facturas y devuelve un diccionario de objetos cliente
    con el acumulado de las bases imponibles de las facturas.
    """
    res = {}
    for fra in fras:
        cliente = fra.cliente and fra.cliente.nombre or "¡Sin cliente!"
        base_imponible = fra.calcular_base_imponible()
        try:
            res[cliente] += base_imponible
        except KeyError:
            res[cliente] = base_imponible
    return res

def find_similar(nombre, lista):
    """
    Encuentra el nombre dentro de `lista` más parecido según una aproximación
    un poco burda a la diferencia entre cadenas, pero que no requiere
    bibliotecas de terceros.
    Devuelve el nombre encontrado con la similitud más alta. Idealmente será
    1 si son idénticas.
    """
    import difflib
    similar = None
    maxratio = 0.0
    for canonico in lista:
        ratio = difflib.SequenceMatcher(a=nombre.upper(),
                                        b=canonico.upper()).ratio()
        if ratio > maxratio:
            similar = canonico
            maxratio = ratio
    return similar, maxratio

def main():
    """
    Busca las facturas entre [fecha inicial, fecha final), acumula las bases
    imponibles y las guarda en un diccionario por cliente.
    Después lee los datos de un CSV generado a partir de los datos de Murano.
    Ambos datos (los de ginn y los de Murano) los combina en un diccionario.
    Finalmente volcará una estructura CSV por salida estándar con el nombre del
    cliente y el acumulado de sus bases imponibles.
    """
    # Datos de ginn
    fini = datetime.date(2016, 1, 1)
    ffin = datetime.date(2016, 6, 1)
    fras = buscar_facturas(fini, ffin)
    sys.stderr.write("Encontradas {} facturas. Acumulando...\n".format(len(fras)))
    tot_fras = acumular_facturas(fras)
    # Datos de ginn a un CSV para comprobaciones.
    fout = open("ventas_2016_ginn.csv", "w")
    ginnout = csv.writer(fout)
    nombres = sorted(tot_fras.keys())
    ginnout.writerows(zip(nombres, [tot_fras[c] for c in nombres]))
    fout.close()
    # Datos de Murano
    if len(sys.argv) > 1:
        try:
            fin = open(sys.argv[1], "r")
        except IOError:
            sys.stderr.write("Si especifica un parámetro, debe ser el fichero "
                             "de entrada CSV procedente de Murano.")
            sys.exit(1)
        else:
            muranoin = csv.reader(fin)
            for nombre, total in muranoin:
                total = float(total.replace(".", "").replace(",", "."))
                #sys.stderr.write("{}: {}\n".format(nombre, total))
                try:
                    tot_fras[nombre] += total
                except KeyError:
                    sys.stderr.write("{} no está. ".format(nombre))
                    similar, ratio = find_similar(nombre, nombres)
                    if ratio > 0.9:
                        sys.stderr.write("Pero se parece a {} en un {}.\n".format(
                            similar, ratio))
                        tot_fras[similar] += total
                    else:
                        sys.stderr.write("Y lo agrego porque el más parecido "\
                                         "es {}, con {}.\n".format(similar, ratio))
                        tot_fras[nombre] = total
                        nombres.append(nombre)
            fin.close()
    # Datos combinados
    csvfile = csv.writer(sys.stdout)
    csvfile.writerow(("Cliente",
                      "Base imponible"))
    for nombre in sorted(nombres):
        csvfile.writerow((nombre, tot_fras[nombre]))
    sys.stderr.write("That's all folks!")
    sys.exit(0)

if __name__ == "__main__":
    main()
