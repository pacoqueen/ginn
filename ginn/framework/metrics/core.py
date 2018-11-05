#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

try:
    from framework.pclases import Bala, BalaCable, Bigbag, Caja, Pale
    from framework.pclases import Rollo, RolloDefectuoso, RolloC
    from framework.pclases import ParteDeProduccion, ProductoVenta
    from framework.pclases import Articulo
    from framework.pclases import AND
    from api import murano
except ImportError:
    import os
    import sys
    sys.path.insert(0, os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..')))
    from framework.pclases import Bala, BalaCable, Bigbag, Caja, Pale
    from framework.pclases import Rollo, RolloDefectuoso, RolloC
    from framework.pclases import ParteDeProduccion, ProductoVenta
    from framework.pclases import Articulo
    from framework.pclases import AND
    from api import murano


# PORASQUI.
"""
-- Entradas (produccion) --
DECLARE @desde DATE;
SET @desde = DATEADD(HOUR, -1, GETDATE())

SELECT [CodigoArticulo]
      ,COUNT([NumeroSerieLc]) AS bultos
      -- ,[Fecha]
      -- ,[OrigenDocumento]
      -- ,[SerieDocumento]
      ,[CodigoTalla01_] AS calidad
      -- ,[CodigoAlmacen]
      ,[UnidadMedida1_] AS unidad
      -- ,[Comentario]
      -- ,[StatusTraspasadoIME]
      -- ,[TipoImportacionIME]
      ,SUM([PesoBruto_]) AS peso_bruto
      ,SUM([PesoNeto_]) AS peso_neto
      ,SUM([MetrosCuadrados]) AS m2
      -- ,[CodigoPale]
  FROM [GEOTEXAN].[dbo].[TmpIME_MovimientoSerie]
 WHERE CodigoEmpresa = 10200
   AND OrigenDocumento = 2	-- 11 si es salida
   AND SerieDocumento = 'FAB'
   AND CodigoAlmacen = 'GTX'
   AND StatusTraspasadoIME = 1	-- 0 si no ha terminado
   AND Fecha >= @desde
 GROUP BY CodigoArticulo, CodigoTalla01_, UnidadMedida1_, StatusTraspasadoIME, TipoImportacionIME
-- ORDER BY Fecha DESC;

-- Entradas pendientes de volcar:
SELECT [CodigoArticulo]
      ,COUNT([NumeroSerieLc]) AS bultos
      -- ,[Fecha]
      -- ,[OrigenDocumento]
      -- ,[SerieDocumento]
      ,[CodigoTalla01_] AS calidad
      -- ,[CodigoAlmacen]
      ,[UnidadMedida1_] AS unidad
      -- ,[Comentario]
      -- ,[StatusTraspasadoIME]
      -- ,[TipoImportacionIME]
      ,SUM([PesoBruto_]) AS peso_bruto
      ,SUM([PesoNeto_]) AS peso_neto
      ,SUM([MetrosCuadrados]) AS m2
      -- ,[CodigoPale]
  FROM [GEOTEXAN].[dbo].[TmpIME_MovimientoSerie]
 WHERE CodigoEmpresa = 10200
   AND OrigenDocumento = 2	-- 11 si es salida
   AND SerieDocumento = 'FAB'
   AND CodigoAlmacen = 'GTX'
   AND StatusTraspasadoIME = 0	-- 1 si ha terminado
   AND Fecha >= @desde
 GROUP BY CodigoArticulo, CodigoTalla01_, UnidadMedida1_, StatusTraspasadoIME, TipoImportacionIME
-- ORDER BY Fecha DESC;

--
-- Salidas (consumos) --
SELECT [CodigoArticulo]
      ,COUNT([NumeroSerieLc]) AS bultos
      -- ,[Fecha]
      -- ,[OrigenDocumento]
      -- ,[SerieDocumento]
      ,[CodigoTalla01_] AS calidad
      -- ,[CodigoAlmacen]
      ,[UnidadMedida1_] AS unidad
      -- ,[Comentario]
      -- ,[StatusTraspasadoIME]
      -- ,[TipoImportacionIME]
      ,SUM([PesoBruto_]) AS peso_bruto
      ,SUM([PesoNeto_]) AS peso_neto
      ,SUM([MetrosCuadrados]) AS m2
      -- ,[CodigoPale]
  FROM [GEOTEXAN].[dbo].[TmpIME_MovimientoSerie]
 WHERE CodigoEmpresa = 10200
   AND OrigenDocumento = 11		-- 11 si es entrada
   AND SerieDocumento = 'FAB'
   AND CodigoAlmacen = 'GTX'
   AND StatusTraspasadoIME = 1	-- 0 si no ha terminado
   AND Fecha >= @desde
 GROUP BY CodigoArticulo, CodigoTalla01_, UnidadMedida1_, StatusTraspasadoIME, TipoImportacionIME
 -- ORDER BY Fecha DESC;

-- Salidas pendientes de terminar de procesar
SELECT [CodigoArticulo]
      ,COUNT([NumeroSerieLc]) AS bultos
      -- ,[Fecha]
      -- ,[OrigenDocumento]
      -- ,[SerieDocumento]
      ,[CodigoTalla01_] AS calidad
      -- ,[CodigoAlmacen]
      ,[UnidadMedida1_] AS unidad
      -- ,[Comentario]
      -- ,[StatusTraspasadoIME]
      -- ,[TipoImportacionIME]
      ,SUM([PesoBruto_]) AS peso_bruto
      ,SUM([PesoNeto_]) AS peso_neto
      ,SUM([MetrosCuadrados]) AS m2
      -- ,[CodigoPale]
  FROM [GEOTEXAN].[dbo].[TmpIME_MovimientoSerie]
 WHERE CodigoEmpresa = 10200
   AND OrigenDocumento = 11		-- 11 si es entrada
   AND SerieDocumento = 'FAB'
   AND CodigoAlmacen = 'GTX'
   AND StatusTraspasadoIME = 0	-- 1 si ha terminado
   AND Fecha >= @desde
 GROUP BY CodigoArticulo, CodigoTalla01_, UnidadMedida1_, StatusTraspasadoIME, TipoImportacionIME
 -- ORDER BY Fecha DESC;
"""
SQL_IN0 = """
"""
SQL_IN1 = """
"""
SQL_OUT0 = """
"""
SQL_OUT1 = """
"""


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
    fibra = (None, 0)
    geotextiles = (None, 0)
    cemento = (None, 0)
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


def get_existencias_virtuales(productos=[]):
    """
    Devuelve las existencias de Murano de cada producto **más** la producción
    sin volcar a Murano.
    """
    res = get_existencias(productos)
    for producto in productos:
        for dimension in productos[producto]:
            sin_volcar = get_no_volcado(producto, dimension)
            res[producto][dimension] += sin_volcar
    return res


def get_no_volcado(producto, dimension='KG'):
    """
    Devuelve un float que es la suma de los 'KG', 'M2', 'ROLLO', 'BALA'...
    de los artículos del producto pendientes de volcar a Murano (api=False).
    """
    res = 0
    if producto:
        articulos = Articulo.select(
                AND(Articulo.q.productoVentaID == producto.id,
                    Articulo.q.api == False,)   # noqa
                )
        # TODO: ¿Cómo filtro para descartar todos los productos con api False
        # o None anteriores a la implantación de Murano?
        if dimension == 'KG':
            res = [a.peso for a in articulos]
        elif dimension == 'M2':
            res = [a.superficie for a in articulos]
        else:   # 'ROLLO', 'BALA', 'CAJA'... No medimos volumen.
            res = articulos.count()
    return res


def importaciones_murano(horas=1):
    """
    Importaciones completadas y pendientes por producto en Murano en las
    últimas `horas` indicadas. Al proceder de una tabla temporal que se limpia
    periódicamente, no tiene sentido pedir importaciones desde una fecha y hora
    concretas. Es bastante probable que no haya datos para fechas muy antiguas.
    Devuelve un diccionario del tipo:
    {'entradas': {'completadas': [{'CodigoArticulo': '',
                                   'bultos': 0,
                                   'calidad': '',
                                   'm2': 0,
                                   'peso_bruto': 0,
                                   'peso_neto': 0,
                                   'unidad': ''}, {...}, ...],
                  'pendientes': [{}, {}, ...]},
     'salidas': {'completadas': [...], 'pendientes': [...]}
    Las entradas son producciones y las salidas, consumos.
    """
    assert isinstance(horas, int)
    # TODO: Importaciones por segundo o algo así para ver qué productos están
    # entrando en almacén. En forma de (producto, cantidad), por ejemplo.
    res = {'entradas': {'completadas': [],
                        'pendientes':  []},
           'salidas':  {'completadas': [],
                        'pendientes':  []}}
    conn = murano.connection.Connection()
    produccion_confirmada = conn.run_sql(SQL_IN1)
    res['entradas']['completadas'] = produccion_confirmada
    produccion_pendiente = conn.run_sql(SQL_IN0)
    res['entradas']['pendientes'] = produccion_pendiente
    consumos_confirmados = conn.run_sql(SQL_OUT1)
    res['salidas']['completadas'] = consumos_confirmados
    consumos_pendientes = conn.run_sql(SQL_OUT0)
    res['salidas']['pendientes'] = consumos_pendientes
    return res
