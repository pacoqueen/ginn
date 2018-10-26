#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

try:
    from framework.pclases import Bala, BalaCable, Bigbag, Caja, Pale
    from framework.pclases import Rollo, RolloDefectuoso, RolloC
    from framework.pclases import ParteDeProduccion, ProductoVenta
    from api import murano
except ImportError:
    import os
    import sys
    sys.path.insert(0, os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..')))
    from framework.pclases import Bala, BalaCable, Bigbag, Caja, Pale
    from framework.pclases import Rollo, RolloDefectuoso, RolloC
    from framework.pclases import ParteDeProduccion, ProductoVenta
    from api import murano


def bultos_fabricados(desde=None):
    """Bultos fabricados por clase desde la fecha indicada."""
    data = {}
    clases = (Bala, BalaCable, Bigbag,
              Caja, Pale, Rollo,
              RolloDefectuoso, RolloC)
    for clase in clases:
        data[clase] = dict()
        data[clase]['bultos'] = clase.select().count()
        if 4 <= datetime.datetime.now().month <= 10:
            # UGLY HACK: daylight saving + timezone UTC+1
            antes = datetime.datetime.now()-datetime.timedelta(hours=3)
        else:
            antes = datetime.datetime.now()-datetime.timedelta(hours=2)
        # kg fabricados en la última hora
        select_results = clase.select(clase.q.fechahora >= antes)
        for dim_name in ('pesobala', 'peso', 'pesobigbag'):
            try:
                if select_results.count():
                    mean = select_results.sum(dim_name)
                else:
                    mean = 0
                data[clase]['kghora'] = mean
                data[clase]['kg'] = clase.select().sum(dim_name)
            except Exception:
                data[clase]['kghora'] = 0
                data[clase]['kg'] = 0
                continue
            else:
                break
    return data


def produccion_estandar(fechahora=datetime.datetime.now()):
    # TODO: La parte de buscar por fecha hora no está. Solo busca el **último**
    #  de cada tipo **a partir de fechahora**.
    data = dict()
    initurno = inicio_turno(fechahora)
    pdps = ParteDeProduccion.select(
            ParteDeProduccion.q.fechahorainicio >= initurno,
            orderBy="fechahorainicio")
    fibra = (None, None)
    geotextiles = (None, None)
    cemento = (None, None)
    for pdp in pdps:
        if pdp.es_de_balas():
            fibra = (pdp.productoVenta, pdp.prodestandar)
        elif pdp.es_de_geotextiles():
            geotextiles = (pdp.productoVenta, pdp.prodestandar)
        elif pdp.es_de_bolsas():
            cemento = (pdp.productoVenta, pdp.prodestandar)
    data['fibra'] = {'producto': fibra[0], 'kghora': fibra[1]}
    data['geotextiles'] = {'producto': geotextiles[0],
                           'kghora': geotextiles[1]}
    data['cemento'] = {'producto': cemento[0], 'kghora': cemento[1]}
    # Productos C, que no llevan parte de producción.
    if 4 <= datetime.datetime.now().month <= 10:
        # UGLY HACK: daylight saving + timezone UTC+1
        hace_una_hora = datetime.datetime.now()-datetime.timedelta(hours=3)
    else:
        hace_una_hora = datetime.datetime.now()-datetime.timedelta(hours=2)
    balas_c = BalaCable.select(BalaCable.q.fechahora >= hace_una_hora,
                               orderBy="-fechahora")
    try:
        producto = balas_c[0].productoVenta
        kilos_c = balas_c.sum('peso')
    except IndexError:
        kilos_c = 0
        producto = None
    data['fibra_c'] = {'producto': producto, 'kghora': kilos_c}
    rollos_c = BalaCable.select(BalaCable.q.fechahora >= hace_una_hora,
                                orderBy="-fechahora")
    try:
        producto = rollos_c[0].productoVenta
        kilos_c = rollos_c.sum('peso')
    except IndexError:
        kilos_c = 0
        producto = None
    data['geotextiles_c'] = {'producto': None, 'kghora': 0}
    #  No hay fibra de cemento clase C. Ni siquiera clase B.
    return data


def inicio_turno(hora=datetime.datetime.now()):
    """
    Devuelve la fecha y hora de inicio del turno según la fecha/hora
    recibida.
    """
    if hora.hour >= 22:
        hora_inicio = 22
    elif hora.hour >= 14:
        hora_inicio = 14
    elif hora.hour >= 6:
        hora_inicio = 6
    else:
        hora_inicio = 22
    res = datetime.datetime(year=hora.year,
                            month=hora.month,
                            day=hora.day,
                            hour=hora_inicio,
                            minute=0,
                            second=0)
    if res > hora:  # Corrijo el día si estoy en el turno de madrugada
        res -= datetime.timedelta(days=1)
    return res


def get_existencias(productos=[]):
    """
    Devuelve las existencias por calidad de los productos recibidos en la
    lista en kg o m² y solo para el almacén principal ('GTX').
    """
    res = dict()
    if isinstance(productos, ProductoVenta):
        productos = [productos]
    for producto in productos:
        stocks = murano.ops.get_stock_murano(producto, 'GTX')
        for calidad in stocks:
            for dimension in stocks[calidad].keys():
                if dimension not in ("KG", "M2"):
                    stocks[calidad].pop(dimension)
        res[producto] = stocks
    return res
