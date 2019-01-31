#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=invalid-name

"""
31/01/2019

Cambio de rollos en existencias de Murano **con fecha de 2018**.


SYNOPSIS

    ./20190131_regularizacion_2018.py [-h,--help] [-v,--verbose] [--version]

VERSION

    $Id$
"""

from __future__ import print_function
import sys
import os
import traceback
import optparse
import time
import datetime
# Determino dónde estoy para importar pclases y utils
DIRACTUAL = os.path.split(os.path.abspath(os.path.curdir))[-1]
if DIRACTUAL != "ginn":
    PATH_TO_F = os.path.join("..", "..", "ginn")
    sys.path.append(PATH_TO_F)
# pylint: disable=wrong-import-position
from framework import pclases   # noqa
from api import murano          # noqa
from lib.tqdm.tqdm import tqdm  # noqa

FECHA = datetime.datetime(2018, 12, 31)  # Fecha base para las operaciones


def main(verbose=False, simulate=False):
    """
    Todo esto en Murano y con fecha de 2018 (¡OJO¡ Periodo cerrado)
    1. Pasa un listado de códigos de rollo deteriorados a Geotextil clase C.
    2. Pasa a calidad B un listado de códigos de bala.
    3. Da de baja un listado de cajas (se consmieron como reembolsado).
    4. Elimina un listado de balas que físicamente no están en almacén.
    5. Elimina todos los rollos B anteriores a 2019 que **no** sean los del
       listado.
    """
    murano.ops.CODEMPRESA = 8000    # XXX
    report = open("20190131_regularizacion_2018.out.md", "w")
    report.write("# Inicio regularización\n")
    report.write("{}\n".format(datetime.datetime.today()))
    if simulate:
        report.write("**SIMULACIÓN**\n")
    convertir_rollos_a_c(verbose, simulate, report)
    convertir_balas_a_b(verbose, simulate, report)
    consumir_cajas(verbose, simulate, report)
    eliminar_balas(verbose, simulate, report)
    eliminar_rollos_b(verbose, simulate, report)
    report.write("Fin regularización\n")
    report.write("{}\n".format(datetime.datetime.today()))
    report.write("\nDr. Cavadas has left the building.\n")
    report.write("\n---\n\n")
    report.close()


def convertir_rollos_a_c(verbose, simulate, report):
    """
    Busca los artículos de la lista (HARCODED) y los convierte de su producto
    original al genérico Geotextil clase C.
    """
    report.write("## Convertir rollos a C\n")
    pvgtxc = pclases.ProductoVenta.get(364)
    codigos = """R465427 R291280 R502330 R454947 R454948 R471728
                 R471729 R471730 R476689 R476690 R476691 R350513
                 R350517 R350519 R350521 R350525 R415850 R415851
                 R415852 R415853 R415854 R415855 R415856 R415857
                 R415865 R415874 R475712 R386629 R386630 R386631
                 R386632 R448219 R312275 R321392 R506862 R396656
                 R396657 R396658 R396659 R396660 R492795 R492796
                 R492797 R455502 R455503 R468144 R468154 R458898
                 R497411 R497438 R497448 R498645 R502388 R502398
                 R516073 R518094 R520145 R471175 R471176 R471177
                 R481921""".split()
    good = 0
    bad = 0
    total = len(codigos)
    for c in tqdm(codigos, desc="Rollos a C"):
        articulo = pclases.Articulo.get_articulo(c)
        if not simulate:
            if murano.ops.CODEMPRESA == 10200:
                nuevo_articulo = pclases.Articulo(
                    rolloC=pclases.RolloC(peso=articulo.peso,
                                          observaciones="Reg. enero 2019 "
                                                        "+nzumer +rparra"),
                    bala=None, bigbag=None, rollo=None, fechahora=FECHA,
                    productoVenta=pvgtxc, parteDeProduccion=None,
                    albaranSalida=None,
                    almacen=pclases.Almacen.get_almacen_principal(),
                    pesoReal=articulo.peso)
            else:
                nuevo_articulo = articulo
            report.write("* Convirtiendo {} ({} [PV{}]) a {} ({} [PV{}]"
                         ") ".format(articulo.codigo,
                                     articulo.productoVenta.descripcion,
                                     articulo.productoVenta.id,
                                     nuevo_articulo.codigo,
                                     nuevo_articulo.productoVenta.descripcion,
                                     nuevo_articulo.productoVenta.id))
            resd = murano.ops.delete_articulo(articulo,
                                              observaciones="Reg. enero 2019 "
                                                            "+nzumer +rparra",
                                              fecha=FECHA)
            report.write(resd and "✔" or "✘")
            report.write("\n")
            if resd:
                resc = murano.ops.create_articulo(nuevo_articulo,
                                                  observaciones="Reg. enero "
                                                                "2019 "
                                                                "+nzumer "
                                                                "+rparra",
                                                  fecha=FECHA)
                report.write(resc and "✔" or "✘")
                report.write("\n")
            res = resd and resc
            if res:
                good += 1
            else:
                bad += 1
            report.write(res and "✔" or "✘")
            report.write("\n")
    report.write("{}/{} rollos convertidos. {} errores.\n".format(
        good, total, bad))
    report.write("Convertir rollos a C: FINALIZADO\n\n")


def convertir_balas_a_b(verbose, simulate, report):
    """
    Convierte una lista de balas a calidad B.
    """
    report.write("## Convertir balas a B\n")
    codigos = """B213717 B213736 B214098 B215175 B232104
                 B232105 B232109 B213426 B233328 B233329
                 B233330 B233331 B233332 B233333 B222608
                 B218596 B223859 B233292 B216856 B217200
                 B217497 B229052 B229053 B216262 B229429
                 B229574 B221770 B221771 B221772 B221773
                 B221774 B221775""".split()
    good = 0
    bad = 0
    total = len(codigos)
    for c in tqdm(codigos, desc="Balas a B"):
        articulo = pclases.Articulo.get_articulo(c)
        report.write("* Convirtiendo {} ({} [PV{}]) de {} a B ".format(
            articulo.codigo, articulo.productoVenta.descripcion,
            articulo.productoVenta.id, articulo.get_str_calidad()))
        if not simulate:
            if murano.ops.CODEMPRESA == 10200:
                articulo.bala.claseb = True
                articulo.bala.sync()
            res = murano.ops.update_calidad(articulo, "B",
                                            comentario="Reg. enero 2019 "
                                                       "+nzumer +rparra",
                                            fecha=FECHA)
            if res:
                good += 1
            else:
                bad += 1
            report.write(res and "✔" or "✘")
        report.write("\n")
    report.write("{}/{} balas convertidas. {} errores.\n".format(
        good, total, bad))
    report.write("Convertir balas a B: FINALIZADO\n\n")


def consumir_cajas(verbose, simulate, report):
    """
    Elimina cajas que han sido consumidas como reembolsado.
    """
    report.write("## Eliminar cajas consumidas\n")
    codigos = """J10286  J10287  J10288  J10289  J10290
                 J10291  J10292  J10293  J10294  J10295
                 J10296  J10297  J10298  J10299  J6972
                 J6977   J6981   J10286  J10287  J10288
                 J10289  J10290  J10291  J10292  J10293
                 J10294  J10295  J10296  J10297  J10298
                 J10299  J6972   J6977   J6981   J10286
                 J10287  J10288  J10289  J10290  J10291
                 J10292  J10293  J10294  J10295  J10296
                 J10297  J10298  J10299  J6972   J6977
                 J6981   J19646  J5834   J5835   J5836
                 J5837   J5838   J5839   J5840   J5841
                 J5842   J5843   J5844   J5845   J5846
                 J5847   J51045  J51046  J51047  J51048
                 J51049  J51050  J51051  J51052  J51053
                 J51054  J51055  J51056  J51057  J51058
                 J18707  J18708  J18709  J18710  J18711
                 J18712  J18713  J18714  J18715  J18716
                 J18717  J18718  J18719  J18720  J18721
                 J59900  J59901  J59902  J59903  J59904
                 J59905  J59906  J59907  J59908  J59909
                 J59910  J59911  J59912  J59913  J59914
                 J59915  J59916  J59917  J59918  J59919
                 J59920  J59921  J59955  J59956  J59957
                 J59958  J59959  J59960  J59961  J59962
                 J59963  J59964  J59965  J59966  J59967
                 J59968  J59969  J59970  J59971  J59972
                 J59973  J59974  J59975  J59976  J59977
                 J59978  J59979  J59980  J59981  J59982
                 J59983  J59984  J59985  J59986  J59987
                 J59988  J59989  J59990  J59991  J59992
                 J59993  J59994  J81259  J81260  J81261
                 J81262  J81263  J81264  J81265  J81266
                 J81267  J81268  J81269  J81270  J81271
                 J81272  J81273  J81274  J81275  J81276
                 J81277  J81278  J81279  J81280  J81281
                 J81282  J81283  J81284  J81285  J81286
                 J81287  J81288  J81289  J81290  J81291
                 J81292  J81293  J81294  J81295  J81296
                 J81297  J81298  J121897 J121898 J121899
                 J121900 J121901 J121902 J121903 J121904
                 J121905 J121906 J121907 J121908 J121909
                 J121910 J121911 J121912 J121913 J121914
                 J121915 J121916 J121917 J121918 J121919
                 J121920 J121921 J121922 J121923 J121924
                 J121925 J121926 J121927 J121928 J91989
                 J91990  J91991  J91992  J91993  J91994
                 J91995  J91996  J91997  J91998  J91999
                 J92000  J92001  J92002  J92003  J92004
                 J92005""".split()
    good = 0
    bad = 0
    total = len(codigos)
    for c in tqdm(codigos, desc="Eliminar cajas consumidas"):
        articulo = pclases.Articulo.get_articulo(c)
        report.write("* Eliminando {} ({} [PV{}]) ".format(
            articulo.codigo, articulo.productoVenta.descripcion,
            articulo.productoVenta.id))
        if not simulate:
            res = murano.ops.delete_articulo(articulo,
                                             comentario="Reg. enero 2019 "
                                                        "+nzumer +rparra",
                                             fecha=FECHA)
            if res:
                good += 1
            else:
                bad += 1
            report.write(res and "✔" or "✘")
        report.write("\n")
    report.write("{}/{} cajas eliminadas. {} errores.\n".format(
        good, total, bad))
    report.write("Eliminar cajas consumidas: FINALIZADO\n\n")


def eliminar_balas(verbose, simulate, report):
    """
    Elimina las balas del listado por no estar físicamente en almacén.
    """
    report.write("## Eliminar balas desaparecidas\n")
    codigos = """B217421 B217897 B217968 B218708 B225395
                 B225449 B227791 B227792 B227793 B227794
                 B227795 B227796 B227797 B228979 B229236
                 B230468 B233837 B235009 B235014 B220279
                 B222400 B222420 B222494 B223423 B224941
                 B225185 B225715 B226503 B229052 B230873
                 B229053 B232406 B232793 B232795 B232816
                 B232827 B233729 B213517 B213532 B213535
                 B213542 B213546 B213552 B213789 B213798
                 B213799 B215487 B215492 B215595 B220780
                 B220839 B228523 B231969 B232616 B220616
                 B222274 B222295 B227892 B227909 B228757
                 B231784 B231788 B231804""".split()
    good = 0
    bad = 0
    total = len(codigos)
    for c in tqdm(codigos, desc="Eliminar balas desaparecidas"):
        articulo = pclases.Articulo.get_articulo(c)
        report.write("* Eliminando {} ({} [PV{}]) ".format(
            articulo.codigo, articulo.productoVenta.descripcion,
            articulo.productoVenta.id))
        if not simulate:
            res = murano.ops.delete_articulo(articulo,
                                             comentario="Reg. enero 2019 "
                                                        "+nzumer +rparra",
                                             fecha=FECHA)
            if res:
                good += 1
            else:
                bad += 1
            report.write(res and "✔" or "✘")
        report.write("\n")
    report.write("{}/{} balas convertidas. {} errores.\n".format(
        good, total, bad))
    report.write("Eliminar cajas consumidas: FINALIZADO\n\n")


def eliminar_rollos_b(verbose, simulate, report):
    """
    Elimina todos los rollos B antermidas como reembolsado.
    """
    report.write("## Eliminar rollos B anteriores a 2019\n")
    codigos = """X1987 X2049 X2058 X2067 X2126
                 X2142 X2022 X2116 X2139 X2150
                 X2151 X2173 X2027 X2065 X2074
                 X2140 X2021 X2028 X2047 X2048
                 X2069 X2125 X2170 X2129 X2138
                 X2118 X2064 X2059 X2109 X2110
                 X2111 X2112 X2113 X2114 X2159
                 X2160 X2180 X2181 X2068 X2104
                 X2182 X2044 X2134 X2017 X2018
                 X2078 X2079 X2117 X2096 X2097
                 X2066 X2077 X2141 X2175 X2081
                 X2169 X2168 X2172 X2174 X2176
                 X2177 X2178 X2179""".split()
    good = 0
    bad = 0
    articulos = []
    dosmildiecinueve = datetime.datetime(2019, 1, 1)
    rollosd = pclases.RolloDefectuoso.select(
            pclases.RolloDefectuoso.q.fechahora < dosmildiecinueve,
            orderBy="-id")
    for rd in tqdm(rollosd, desc="Buscar rollos B", total=rollosd.count()):
        a = rd.articulo
        if murano.ops.esta_en_almacen(a):
            articulos.append(a)
    total = len(articulos)
    report.write("{} rollos B anteriores a 2019 encontrados en almacén "
                 "de Murano.\n".format(total))
    for articulo in tqdm(articulos, desc="Eliminar rollos B"):
        if articulo.codigo not in codigos:
            report.write("* Eliminando {} ({} [PV{}]), calidad {} ".format(
                articulo.codigo, articulo.productoVenta.descripcion,
                articulo.productoVenta.id, articulo.get_str_calidad()))
            if not simulate:
                res = murano.ops.delete_articulo(articulo,
                                                 comentario="Reg. enero 2019 "
                                                            "+nzumer +rparra",
                                                 fecha=FECHA)
                if res:
                    good += 1
                else:
                    bad += 1
                report.write(res and "✔" or "✘")
            report.write("\n")
        else:
            report.write("* {} no se elimina. [PV{}], calidad {}\n".format(
                    articulo.codigo, articulo.productoVenta.descripcion,
                    articulo.productoVenta.id, articulo.get_str_calidad()))
    report.write("{}/{} rollos eliminados. {} errores.\n".format(
        good, total, bad))
    report.write("{} rollos encontrados en listado. No eliminados.\n".format(
        total - (good + bad)))
    report.write("Eliminar rollos B sobrantes: FINALIZADO\n\n")


if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = optparse.OptionParser(
                formatter=optparse.TitledHelpFormatter(),
                usage=globals()['__doc__'],
                version='$Id$')
        parser.add_option('-v',
                          '--verbose',
                          action='store_true',
                          default=False,
                          help='información por pantalla')
        parser.add_option('-d',
                          '--dryrun',
                          action='store_true',
                          default=False,
                          help='no realiza cambios')
        (options, args) = parser.parse_args()
        # if len(args) < 1:
        #     parser.error ('missing argument')
        if options.verbose:
            print(time.asctime())
        main(options.verbose, options.dryrun)
        if options.verbose:
            print(time.asctime())
        if options.verbose:
            print('Tiempo total en minutos: ', (time.time() - start_time)/60.0)
        sys.exit(0)
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
    except SystemExit as e:         # sys.exit()
        raise e
    except Exception as e:          # pylint: disable=broad-except
        print('Error, excepción inesperada.')
        print(str(e))
        traceback.print_exc()
        sys.exit(1)
