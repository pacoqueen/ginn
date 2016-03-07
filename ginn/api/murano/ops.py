#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Operaciones.

"""
from __future__ import print_function
import os
import logging
logging.basicConfig(filename = "%s.log" % (
    ".".join(os.path.basename(__file__).split(".")[:-1])),
    level = logging.DEBUG)
import datetime
from connection import Connection, DEBUG, VERBOSE
from export import determinar_familia_Murano

try:
    import win32com.client
except ImportError:
    LCOEM = False
else:
    LCOEM = True

import sys, os
ruta_ginn = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "ginn"))
sys.path.append(ruta_ginn)
from framework import pclases

CODEMPRESA = 8000   # Empresa de pruebas. Cambiar por la 10200 en producción.

SQL = """INSERT INTO [%s].[dbo].[TmpIME_MovimientoStock](
            CodigoEmpresa,
            Ejercicio,
            Periodo,
            Fecha,
            Serie,
            Documento,
            CodigoArticulo,
            CodigoAlmacen,
            -- AlmacenContrapartida,
            Partida,
            -- Partida2_,
            -- CodigoColor_,
            GrupoTalla_,
            CodigoTalla01_,
            TipoMovimiento,
            Unidades,
            UnidadMedida1_,
            Precio,
            Importe,
            Unidades2_,
            -- UnidadMedida2_,
            FactorConversion_,
            Comentario,
            -- CodigoCanal,
            -- CodigoCliente,
            -- CodigoProveedor,
            -- FechaCaduca,
            Ubicacion,
            OrigenMovimiento,
            -- EmpresaOrigen,
            -- MovOrigen,
            -- EjercicioDocumento,
            NumeroSerieLc,
            IdProcesoIME,
            -- MovIdentificadorIME,
            StatusTraspasadoIME,
            TipoImportacionIME,
            DocumentoUnico --,
            -- FechaRegistro,
            -- MovPosicion
            )
        VALUES (
            %d,         -- código empresa
            %d,         -- ejercicio
            %d,         -- periodo
            '%s',       -- fecha
            'FAB',
            %d,         -- documento
            '%s',       -- codigo_articulo
            '%s',       -- codigo_almacen
            -- '',
            '%s',       -- partida
            -- NULL,
            -- NULL,
            %d,         -- grupo_talla
            '%s',       -- codigo_talla
            %d,         -- tipo_movimiento
            %d,         -- unidades
            '%s',       -- unidad de medida específica
            %f,         -- precio
            %f,         -- importe
            %f,         -- unidades2 = unidades * factor de conversion
            -- NULL,
            %f,         -- factor de conversión
            '%s',       -- comentario
            -- NULL,
            -- NULL,
            -- NULL,
            -- NULL,
            '%s',       -- ubicación
            '%s',       -- origen movimiento
            -- NULL,
            -- NULL,
            -- NULL,
            '%s',       -- NumeroSerieLc
            '%s',       -- IdProcesoIME
            -- NULL,
            0,
            0,
            -1 --,
            -- NULL,
            -- NULL
            );"""

SQL_SERIE = """INSERT INTO [%s].[dbo].[TmpIME_MovimientoSerie](
                CodigoEmpresa,
                CodigoArticulo,
                NumeroSerieLc,
                Fecha, 
                OrigenDocumento,
                EjercicioDocumento,
                SerieDocumento,
                Documento,
                MovPosicionOrigen,
                -- CodigoColor_,
                CodigoTalla01_,
                CodigoAlmacen,
                Ubicacion,
                Partida,
                UnidadMedida1_,
                UnidadesSerie,
                -- NumeroSerieFabricante,
                -- EmpresaOrigen,
                -- CodigoCliente,
                -- CodigoProveedor,
                Comentario,
                IdProcesoIME,
                --MovIdentificadorIME,
                StatusTraspasadoIME,
                TipoImportacionIME,
                PesoBruto_,
                PesoNeto_,
                MetrosCuadrados,
                CodigoPale)
               VALUES(
                %d,     -- código empresa
                '%s',   -- código artículo
                '%s',   -- número de serie del artículo
                '%s',   -- fecha
                %d,     -- origen documento
                %d,     -- ejercicio
                'FAB',
                %d,     -- documento
                '%s',   -- mov. posición origen
                -- NULL,
                '%s',   -- código talla
                '%s',   -- código almacén
                '%s',   -- ubicación
                '%s',   -- partida
                '%s',   -- unidad de medida específica (kg, m²)
                1,
                -- NULL,
                -- NULL,
                -- NULL,
                -- NULL,
                '%s',   -- comentario
                '%s',   -- ID proceso IME
                -- NULL,
                0,
                0,
                %f,     -- peso bruto
                %f,     -- peso neto
                %s,     -- metros cuadrados
                '%s'      -- código de palé
               );"""

def buscar_grupo_talla(productoVenta):
    """
    Devuelve el código de grupo de tallas (calidades) que puede tener el
    producto.
    """
    # Hemos varios grupos de talla: 1 para A, B y C, 2 para A, B (sin C), etc.
    grupo_talla = 0     # Sin grupo de talla
    #res = consultar_producto(nombre = productoVenta.descripcion)
    res = consultar_producto(productoVenta)
    try:
        grupo_talla = res[0]['GrupoTalla_']
    except TypeError, e:
        strlog = "(EE)[T] %s no se encuentra en Murano." % (
                productoVenta.descripcion)
        print(strlog)
        logging.error(strlog)
        if not DEBUG:
            raise e
        else:
            grupo_talla = 0
    return grupo_talla

def buscar_codigo_producto(productoVenta):
    """
    Busca el ID del producto en Murano para la descripción del producto
    recibido.
    """
    # Se puede dar el caso de que el producto exista pero la descripción no
    # coincida completamente porque Murano ha recortado el texto para que
    # quepa en su mierda de campo tipo CHAR[40]. ¿En serio? 2016 bro!
    # Buscamos directamente por el código de murano_exportar: [PC|PV]+ID
    # Podría aquí devolverlo directamente, pero al menos así me aseguro de
    # que existe en Murano.
    #res = consultar_producto(nombre = productoVenta.descripcion)
    res = consultar_producto(producto = productoVenta)
    try:
        codarticulo = res[0]['CodigoArticulo']
        desc_ginn = productoVenta.descripcion
        assert (desc_ginn.startswith(res[0]['DescripcionArticulo']) or
                desc_ginn.startswith(res[0]['Descripcion2Articulo']))
    except (IndexError, TypeError), e:
        strlog = "(EE)[C] %s no se encuentra en Murano. Excepción: %s" % (
                productoVenta.descripcion, e)
        print(strlog)
        logging.error(strlog)
        if not DEBUG:
            raise e
        else:
            codarticulo = ''
    except AssertionError:
        strlog = '(WW)[C] La descripción de "%s" (%s) ha cambiado.'\
                 ' En Murano es: "%s"/"%s"' % (productoVenta.descripcion,
                                               productoVenta.puid,
                                               res[0]['DescripcionArticulo'],
                                               res[0]['Descripcion2Articulo'])
        print(strlog)
        logging.warning(strlog)
    return codarticulo

def buscar_precio_coste(producto, ejercicio, codigo_almacen):
    """
    Devuelve el importe en €/kg definido en Murano y después en ginn (si no se
    encuenta) para la familia del producto.
    Si es producto de compra, devuelve el precio de valoracion por unidad de
    producto según la función de valoración definida para él.
    """
    cod_familia = determinar_familia_Murano(producto)
    if isinstance(producto, pclases.ProductoVenta):
        try:
            precio_coste = buscar_precio_coste_familia_murano(cod_familia)
        except ValueError:
            precio_coste = buscar_precio_coste_familia_ginn(cod_familia)
    elif isinstance(producto, pclases.ProductoCompra):
        try:
            precio_coste = buscar_precio_coste_murano(producto, ejercicio,
                                                      codigo_almacen)
        except ValueError:
            precio_coste = buscar_precio_coste_ginn(producto)
    else:
        # WTF?
        raise ValueError, "ops:buscar_precio_coste: el producto «%s» recibido"\
                          " no es un producto de compra ni de venta." % (
                                  producto)
    return precio_coste

def buscar_precio_coste_familia_murano(cod_familia):
    """
    Devuelve el precio de coste de la base de datos de Murano para el código
    de familia recibido.
    Lanza ValueError si el código de familia no se encuentra o no tiene
    precio de coste.
    """
    c = Connection()
    #SQL = r"""SELECT TOP 1 PrecioPorUnidadEspecifica
    #          FROM [%s].[dbo].[Familias]
    #          WHERE CodigoFamilia = '%s'
    #            AND CodigoSubfamilia = '***********'
    #            AND CodigoEmpresa = '%d';
    #       """ % (c.get_database(),
    #              cod_familia, 
    #              CODEMPRESA)
    SQL = r"""SELECT TOP 1 GEO_CosteUnidadEspecifica
              FROM [%s].[dbo].[Familias]
              WHERE CodigoFamilia = '%s'
                AND CodigoSubfamilia = '**********'
                AND CodigoEmpresa = '%d';
           """ % (c.get_database(),
                  cod_familia, 
                  CODEMPRESA)
    try:
        precio_coste = c.run_sql(SQL)[0]["GEO_CosteUnidadEspecifica"]
        precio_coste = float(precio_coste)  # Viene como Decimal
    except (TypeError, AttributeError, KeyError): 
        # cod_familia es None o no se encontraron registros
        raise ValueError
    except Exception, e:
        logging.warning("No se encontró precio en Murano para la familia "
                        "«%s». Además, provocó una excepción %s." % 
                        (cod_familia, e))
        precio_coste = None
    return precio_coste

def buscar_precio_coste_familia_ginn(cod_familia):
    """
    Devuelve el precio por familia definido en ginn.
    """
    # TODO: FIXME: HARCODED: Esto debe ir a la tabla de ginn correspondiente y reflejarlo en la ventana que sea.
    if cod_familia == "GEO":
        precio_coste = 2.210
    elif cod_familia == "FIB" or cod_familia == "FCE":
        precio_coste = 1.545
    elif cod_familia == "FEM":
        precio_coste = 1.884
    else:
        raise ValueError, "cod_familia debe ser GEO, FIB, FCE o FEM. Se "\
                          "recibió: %s" % (cod_familia)

def buscar_precio_coste_murano(producto, ejercicio, codigo_almacen):
    """
    Devuelve el precio de coste de la base de datos de Murano para el producto
    recibido. Según Sage lo aconsejable es enviar el «PrecioMedio» en el
    momento del consumo del producto. Se almacena en el campo «PrecioMedio»
    de la tabla «AcumuladoStock», donde solo hay un registro por producto,
    año y periodo. El periodo 99 siempre guarda el más actualizado.
    """
    c = Connection()
    cod_articulo = get_codigo_articulo_murano(producto)
    SQL = r"""SELECT TOP 1 PrecioMedio
              FROM [%s].[dbo].[AcumuladoStock]
              WHERE CodigoArticulo = '%s'
                AND Ejercicio = %d
                AND CodigoAlmacen = '%s'
                AND CodigoEmpresa = '%d'
                AND Periodo = 99;
           """ % (c.get_database(),
                  cod_articulo, 
                  ejercicio,
                  cod_almacen,
                  CODEMPRESA)
    try:
        precio_coste = c.run_sql(SQL)[0]["PrecioMedio"]
    except (TypeError, AttributeError, KeyError): 
        # codalmacen es None o no se encontraron registros
        raise ValueError
    except Exception, e:
        logging.warning("No se encontró precio medio en Murano para el "
                        "producto «%s». Además, provocó una excepción %s." % 
                        (cod_articulo, e))
        precio_coste = None
    return precio_coste

def buscar_precio_coste_ginn(producto):
    """
    Devuelve el precio de coste en ginn para el producto (debe ser un producto
    de compra) según su función de valoración.
    """
    if isinstance(producto, pclases.ProductoCompra):
        precio_coste = producto.get_precio_valoracion()
    elif isinstance(producto, pclases.ProductoVenta):
        # No debería entrar aquí, pero me estoy adelantando al futuro right now
        cod_familia = determinar_familia_Murano(producto)
        precio_coste = buscar_precio_coste_familia_ginn(cod_familia)
    else:
        # WTF?
        raise ValueError, "ops:buscar_precio_coste_ginn: el producto «%s» "\
                          "recibido no es un producto de compra ni de venta."%(
                                  producto)
    return precio_coste

def buscar_codigo_almacen(almacen, articulo = None):
    """
    Devuelve almacén de la empresa configurada cuyo nombre coincida con el del
    almacén de ginn recibido.
    Si el almacén recibido es None, entonces buscará el almacén actual donde
    dice Murano que está el artículo recibido como segundo parámetro.
    """
    c = Connection()
    if almacen:
        filas = c.run_sql("""SELECT CodigoAlmacen
            FROM %s.dbo.Almacenes
            WHERE CodigoEmpresa = %d AND Almacen = '%s'
            ORDER BY CodigoAlmacen;""" % (c.get_database(), 
                                          CODEMPRESA,
                                          almacen.nombre))
        try:
            codalmacen = filas[0]['CodigoAlmacen']
        except Exception, e:
            strlog = "(EE)[A] Almacén '%s' no se encuentra en Murano." % (
                    almacen.nombre)
            print(strlog)
            logging.error(strlog)
            if not DEBUG:
                raise e
            else:
                return 'CEN'
    else:
        if DEBUG:
            return 'CEN'
        else:
            try:
                assert articulo is not None
                codalmacen = get_codalmacen_articulo(c, articulo)
            except AssertionError:
                raise ValueError, "(EE)[A] Debe especificarse un almacén "\
                                  "o un artículo."
    return codalmacen

def simulate_guid():
    """
    Genera un código aleatorio similar al generado por MSSQLServer.
    """
    if VERBOSE:
        strlog = "Simulando guid..."
        print(strlog)
        logging.info(strlog)
    import random
    grupos = 8, 4, 4, 4, 12
    subgrupos = []
    for g in grupos:
        subgrupo = ""
        for i in range(g):
            c = random.choice("01234567890ABCDE")
            subgrupo += c
        subgrupos.append(subgrupo)
    guid = "-".join(subgrupos)
    if VERBOSE:
        strlog = guid
        print(strlog)
        logging.info(strlog)
    return guid

def buscar_factor_conversion(producto):
    """
    Busca el factor de conversión en la tabla de productos de Murano a partir
    del producto de compra o de venta recibido.
    # Por norma general hay que poner 0 en los productos que tengan factor de
    # conversión (traslación directa entre las unidades básicas --bultos-- y
    # las específicas --KG, M2--) y 1 en los que el peso varíe entre cada
    # artículo del mismo producto.
    """
    # Balas A, B y C: 0
    # Bigbags: 0
    # Rollos A y B: 0 
    # En rollos C: 1
    # En cajas, que todas pesan iguales: 1. Los palés no hay que crearlos, se
    # crean solos al meter las cajas.
    if isinstance(producto, pclases.ProductoVenta):
        if producto.es_clase_c():
            factor_conversion = 1
        else:
            factor_conversion = 0
    else:
        factor_conversion = 1 
    return factor_conversion

def genera_guid(conexion):
    """
    Devuelve un GUID de SQLServer o simula uno en modo depuración.
    """
    try:
        guid = conexion.run_sql("SELECT NEWID() AS guid;")[0]['guid']
    except Exception, e:
        if not DEBUG:
            raise e
        else:
            guid = simulate_guid()
    return guid

def get_mov_posicion(conexion, codigo_articulo):
    """
    GUID del movimiento de stock asociado al movimiento de número de serie.
    """
    try:
        mov_posicion = conexion.run_sql(r"""SELECT TOP 1 MovPosicion
            FROM %s.dbo.TmpIME_MovimientoStock
            WHERE NumeroSerieLc = '%s'
            ORDER BY FechaRegistro DESC;
            """ % (conexion.get_database(), codigo_articulo))[0]['MovPosicion']
    except Exception, e:
        if not DEBUG:
            raise e
        else:
            mov_posicion = simulate_guid()
    return mov_posicion

def get_codalmacen_articulo(conexion, articulo):
    """
    Busca el último movimiento de stock del artículo y devuelve el código
    de almacén si es un movimiento de entrada o la cadena vacía si es de
    salida.
    """
    codigo_articulo = articulo.codigo
    SQL = r"""SELECT TOP 1 CodigoAlmacen
              FROM [%s].[dbo].[MovimientoArticuloSerie]
              WHERE NumeroSerieLc = '%s' AND CodigoEmpresa = '%d'
              ORDER BY Fecha DESC;""" % (conexion.get_database(),
                                         codigo_articulo, 
                                         CODEMPRESA)
    try:
        codalmacen = conexion.run_sql(SQL)[0]["CodigoAlmacen"]
    except (TypeError, AttributeError, KeyError): 
        # codalmacen es None o no se encontraron registros
        codalmacen = ""
    return codalmacen

def get_codigo_articulo_murano(producto):
    """
    Hemos elegido arbitrariamente (ver export.muranize_valor) que el código
    de artículo en Murano sea [PC|PV]IDginn.
    Calcula el CodigoArticulo del producto recibido según esa expresión y lo
    devuelve.
    """
    if isinstance(producto, pclases.ProductoVenta):
        idmurano = "PV"
    else:
        idmurano = "PC"
    idmurano += str(producto.id)
    return idmurano

def crear_proceso_IME(conexion):
    """
    Crea un proceso de importación con guid único.
    """
    guid_proceso = genera_guid(conexion)
    conexion.run_sql(r"""
        INSERT INTO %s.dbo.Iniciador_tmpIME(IdProcesoIME, EstadoIME, sysUsuario,
                                     sysUserName, Descripcion, TipoImportacion)
        VALUES ('%s', 0, 1, 'administrador', 'Importación desde ginn', 254);
        """ % (conexion.get_database(), guid_proceso))
    return guid_proceso

def prepare_params(articulo, cantidad = 1, producto = None):
    """
    Prepara los parámetros comunes a todos los artículos con movimiento de
    serie y devuelve la conexión a la base de datos MS-SQLServer.
    Cantidad debe ser 1 para incrementar o -1 para decrementar el almacén.
    """
    assert abs(cantidad) == 1
    c = Connection()
    database = c.get_database()
    today = datetime.datetime.today()
    ejercicio = today.year
    periodo = today.month
    fecha = today.strftime("%Y-%m-%d %H:%M:%S")
    documento = int(today.strftime("%Y%m%d"))
    if not producto:
        producto = articulo.productoVenta
    codigo_articulo = buscar_codigo_producto(producto)
    codigo_almacen = buscar_codigo_almacen(articulo.almacen, articulo)
    codigo_talla = articulo.get_str_calidad()
    grupo_talla = buscar_grupo_talla(articulo.productoVenta)
    if cantidad == 1:
        tipo_movimiento = 1     # 1 = entrada, 2 = salida.
    else:
        tipo_movimiento = 2
    unidades = 1    # En dimensión base: 1 bala, rollo, caja, bigbag...
    #precio = 0.0
    precio_kg = buscar_precio_coste(producto, ejercicio, codigo_almacen)
    precio = estimar_precio_coste(articulo, precio_kg)
    importe = unidades * precio
    factor_conversion = buscar_factor_conversion(articulo.productoVenta)
    if factor_conversion:
        unidades2 = unidades * factor_conversion
    else:
        unidades2 = 1 # Siempre será uno porque por cada rollo o bala hay 
                      # solo 1 mov. stock y 1 mov. serie.
    origen_movimiento = "F" # E = Entrada de Stock (entrada directa), 
                            # F (fabricación), I (inventario), 
                            # M (rechazo fabricación), S (Salida stock)
    return (c, database, ejercicio, periodo, fecha, documento, codigo_articulo,
            codigo_almacen, grupo_talla, codigo_talla, tipo_movimiento,
            unidades, precio, importe, unidades2, factor_conversion,
            origen_movimiento)

def estimar_precio_coste(articulo, precio_kg):
    """
    Estima el precio de coste del artículo recibido en función de los €/kg
    indicados en el parámetro «precio_kg».
    """
    # Este precio de coste "requete"-estimado es un CWT en toda regla. Ver 
    # correo del 7 de marzo de 2016 - 13:01
    if articulo.es_rollo():
        # Peso teórico ideal, sin embalaje.
        peso = articulo.get_peso_teorico()
    elif articulo.es_rolloC():
        # Peso real dado en báscula, con embalaje y todo.
        peso = articulo.peso
    elif articulo.es_bala():
        # Peso real dado en báscula, con embalaje y todo.
        peso = articulo.peso
    elif articulo.es_bala_cable():
        # Peso real dado en báscula, con embalaje y todo.
        peso = articulo.peso
    elif articulo.es_bigbag():
        # Peso real dado en báscula, con embalaje y todo.
        peso = articulo.peso
    elif articulo.es_caja():
        # Peso nominal de la caja. El teórico. La embaladora no falla y el 
        # cartón es despreciable. Es el peso que se almacena como real para
        # las cajas a la hora de fabricarlas.
        peso = articulo.peso
    else:
        strerror = "ops:estimar_precio_coste:No se pudo estimar para «%s»" % (
                articulo)
        logging.error(strerror)
        raise ValueError, strerror
    return peso * precio_kg

def create_bala(bala, cantidad = 1, producto = None):
    """
    Crea una bala en las tablas temporales de Murano.
    Recibe un objeto bala de ginn.
    Si cantidad es -1 realiza la baja de almacén de la bala.
    """
    articulo = bala.articulo
    try:
        partida = bala.lote.codigo
    except AttributeError:
        partida = "" # DONE: Balas C no tienen lote. No pasa nada. Murano traga.
    unidad_medida = "KG"
    comentario = ("Bala ginn: [%s]" % bala.get_info())[:40]
    ubicacion = "Almac. de fibra."[:15]
    numero_serie_lc = bala.codigo
    (c, database, ejercicio, periodo, fecha, documento, codigo_articulo,
            codigo_almacen, grupo_talla, codigo_talla, tipo_movimiento,
            unidades, precio, importe, unidades2, factor_conversion,
            origen_movimiento) = prepare_params(articulo, cantidad, producto)
    id_proceso_IME = crear_proceso_IME(c)
    sql_movstock = SQL % (database,
                          CODEMPRESA, ejercicio, periodo, fecha, documento,
                          codigo_articulo, codigo_almacen, partida,
                          grupo_talla, codigo_talla, tipo_movimiento, unidades,
                          unidad_medida, precio, importe, unidades2,
                          factor_conversion, comentario, ubicacion,
                          origen_movimiento, numero_serie_lc,
                          id_proceso_IME)
    c.run_sql(sql_movstock)
    origen_documento = 2 # 2 (Fabricación), 10 (entrada de stock), 11 (salida de stock), 12 (inventario)
    mov_posicion_origen = get_mov_posicion(c, numero_serie_lc)
    sql_movserie = SQL_SERIE % (database,
                                CODEMPRESA, codigo_articulo, numero_serie_lc,
                                fecha, origen_documento, ejercicio, documento,
                                mov_posicion_origen, codigo_talla,
                                codigo_almacen, ubicacion, partida,
                                unidad_medida, comentario, id_proceso_IME,
                                articulo.peso, articulo.peso_sin,
                                0.0, # Metros cuadrados. Decimal NOT NULL
                                ""   # Código palé. Varchar NOT NULL
                               )
    c.run_sql(sql_movserie)
    fire(id_proceso_IME)

def create_bigbag(bigbag, cantidad = 1, producto = None):
    """
    Crea un bigbag en Murano a partir de la información del bigbag en ginn.
    Si cantidad = -1 realiza un decremento en el almacén de Murano.
    """
    articulo = bigbag.articulo
    partida = bigbag.loteCem.codigo
    comentario = ("Bigbag ginn: [%s]" % bigbag.get_info())[:40]
    numero_serie_lc = bigbag.codigo
    ubicacion = "Almac. de fibra."[:15]
    unidad_medida = "KG"
    (c, database, ejercicio, periodo, fecha, documento, codigo_articulo,
            codigo_almacen, grupo_talla, codigo_talla, tipo_movimiento,
            unidades, precio, importe, unidades2, factor_conversion,
            origen_movimiento) = prepare_params(articulo, cantidad, producto)
    id_proceso_IME = crear_proceso_IME(c)
    sql_movstock = SQL % (database,
                          CODEMPRESA, ejercicio, periodo, fecha, documento,
                          codigo_articulo, codigo_almacen, partida,
                          grupo_talla, codigo_talla, tipo_movimiento, unidades,
                          unidad_medida, precio, importe, unidades2,
                          factor_conversion, comentario, ubicacion,
                          origen_movimiento, numero_serie_lc,
                          id_proceso_IME)
    c.run_sql(sql_movstock)
    origen_documento = 2 # 2 (Fabricación), 10 (entrada de stock), 11 (salida de stock), 12 (inventario)
    mov_posicion_origen = get_mov_posicion(c, numero_serie_lc)
    sql_movserie = SQL_SERIE % (database,
                                CODEMPRESA, codigo_articulo, numero_serie_lc,
                                fecha, origen_documento, ejercicio, documento,
                                mov_posicion_origen, codigo_talla,
                                codigo_almacen, ubicacion, partida,
                                unidad_medida, comentario, id_proceso_IME,
                                articulo.peso, articulo.peso_sin,
                                0.0, # Metros cuadrados. Decimal NOT NULL
                                ""   # Código palé. Varchar NOT NULL
                               )
    c.run_sql(sql_movserie)
    fire(id_proceso_IME)

def create_rollo(rollo, cantidad = 1, producto = None):
    """
    Crea un rollo en Murano a partir de la información del rollo en ginn.
    Si cantidad = -1 realiza un decremento en el almacén de Murano.
    """
    articulo = rollo.articulo
    try:
        partida = rollo.partida.codigo
    except AttributeError:
        partida = ""   # DONE: Los rollos C no tienen partida. No pasa nada.
    comentario = ("Rollo ginn: [%s]" % rollo.get_info())[:40]
    numero_serie_lc = rollo.codigo
    ubicacion = "Almac. de geotextiles."[:15]
    unidad_medida = "M2"
    (c, database, ejercicio, periodo, fecha, documento, codigo_articulo,
            codigo_almacen, grupo_talla, codigo_talla, tipo_movimiento,
            unidades, precio, importe, unidades2, factor_conversion,
            origen_movimiento) = prepare_params(articulo, cantidad, producto)
    id_proceso_IME = crear_proceso_IME(c)
    sql_movstock = SQL % (database,
                          CODEMPRESA, ejercicio, periodo, fecha, documento,
                          codigo_articulo, codigo_almacen, partida,
                          grupo_talla, codigo_talla, tipo_movimiento, unidades,
                          unidad_medida, precio, importe, unidades2,
                          factor_conversion, comentario, ubicacion,
                          origen_movimiento, numero_serie_lc,
                          id_proceso_IME)
    c.run_sql(sql_movstock)
    origen_documento = 2 # 2 (Fabricación), 10 (entrada de stock), 11 (salida de stock), 12 (inventario)
    mov_posicion_origen = get_mov_posicion(c, numero_serie_lc)
    sql_movserie = SQL_SERIE % (database,
                                CODEMPRESA, codigo_articulo, numero_serie_lc,
                                fecha, origen_documento, ejercicio, documento,
                                mov_posicion_origen, codigo_talla,
                                codigo_almacen, ubicacion, partida,
                                unidad_medida, comentario, id_proceso_IME,
                                articulo.peso, articulo.peso_sin,
                                articulo.get_superficie(), 
                                       # Metros cuadrados. Decimal NOT NULL
                                ""   # Código palé. Varchar NOT NULL
                               )
    c.run_sql(sql_movserie)
    fire(id_proceso_IME)

def create_caja(caja, cantidad = 1, producto = None):
    """
    Crea una caja en Murano a partir de la información del objeto caja en ginn.
    Si cantidad es 1, realiza un decremento.
    """
    articulo = caja.articulo
    partida = caja.partidaCem.codigo
    unidad_medida = "M2"
    comentario = ("Caja ginn: [%s]" % caja.get_info())[:40]
    ubicacion = "Almac. de fibra embolsada."[:15]
    numero_serie_lc = caja.codigo
    (c, database, ejercicio, periodo, fecha, documento, codigo_articulo,
            codigo_almacen, grupo_talla, codigo_talla, tipo_movimiento,
            unidades, precio, importe, unidades2, factor_conversion,
            origen_movimiento) = prepare_params(articulo, cantidad, producto)
    id_proceso_IME = crear_proceso_IME(c)
    sql_movstock = SQL % (database,
                          CODEMPRESA, ejercicio, periodo, fecha, documento,
                          codigo_articulo, codigo_almacen, partida,
                          grupo_talla, codigo_talla, tipo_movimiento, unidades,
                          unidad_medida, precio, importe, unidades2,
                          factor_conversion, comentario, ubicacion,
                          origen_movimiento, numero_serie_lc,
                          id_proceso_IME)
    c.run_sql(sql_movstock)
    origen_documento = 2 # 2 (Fabricación), 10 (entrada de stock), 11 (salida de stock), 12 (inventario)
    mov_posicion_origen = get_mov_posicion(c, numero_serie_lc)
    sql_movserie = SQL_SERIE % (database,
                                CODEMPRESA, codigo_articulo, numero_serie_lc,
                                fecha, origen_documento, ejercicio, documento,
                                mov_posicion_origen, codigo_talla,
                                codigo_almacen, ubicacion, partida,
                                unidad_medida, comentario, id_proceso_IME,
                                articulo.peso, articulo.peso_sin,
                                0.0,   # Metros cuadrados. Decimal NOT NULL
                                caja.pale and caja.pale.codigo or ""
                                       # Código palé. Varchar NOT NULL
                               )
    c.run_sql(sql_movserie)
    fire(id_proceso_IME)

def create_pale(pale, cantidad = 1, producto = None):
    """
    Crea un palé con todas sus cajas en Murano a partir del palé de ginn.
    Si cantidad es -1 saca el palé del almacén.
    """
    # Los palés se crean automáticamente al crear las cajas con el código de
    # palé informado. No hay que crear movimiento de stock ni de número de
    # serie para eso.
    for caja in pale.cajas:
        # TODO: Check que compruebe si la caja ya existía para no duplicarlas.
        create_caja(caja, cantidad = cantidad, producto = producto)
    # No es necesario. Cada caja lanza su proceso y el palé no crea
    # registros en la base de datos. No hay que lanzar ninún proceso adicional.
    #fire(id_proceso_IME)

def consulta_proveedor(nombre = None, cif = None):
    """
    Obtiene los datos de un proveedor buscando por nombre, cif o ambas cosas.
    Devuelve una lista de proveedores coincidentes en forma de diccionarios
    campo:valor para cada registro.
    """
    c = Connection()
    sql = "SELECT * FROM %s.dbo.Proveedores WHERE " % (c.get_database())
    where = []
    if nombre:
        where.append("Nombre = '%s'" % nombre)
    if cif:
        where.append("CifDni = '%s'" % cif)
    if nombre and cif:
        where = " AND ".join(where)
    else:
        where = where[0]
    where += ";"
    sql += where
    res = c.run_sql(sql)
    return res

def consulta_cliente(nombre = None, cif = None):
    """
    Obtiene los datos de un cliente buscando por nombre, cif o ambas cosas.
    Devuelve una lista de clientes coincidentes.
    """
    c = Connection()
    sql = "SELECT * FROM %s.dbo.Clientes WHERE " % (c.get_database())
    where = []
    if nombre:
        where.append("Nombre = '%s'" % nombre)
    if cif:
        where.append("CifDni = '%s'" % cif)
    if nombre and cif:
        where = " AND ".join(where)
    else:
        where = where[0]
    where += ";"
    sql += where
    res = c.run_sql(sql)
    return res

def consultar_producto(producto = None, nombre = None):
    """
    Busca un producto por nombre, si se especifica el parámetro.
    En otro caso, busca por el código `[PC|PV]id`. Se debe recibir el objeto
    producto de pclases.
    Devuelve una lista de productos coincidentes.
    """
    assert(not (producto == nombre == None))
    # TODO: Permitir la búsqueda por código EAN.
    c = Connection()
    if nombre:
        try:
            sql = "SELECT * FROM %s.dbo.Articulos WHERE " % (c.get_database())
            where = r"DescripcionArticulo = '%s';" % (nombre)
            sql += where
            res = c.run_sql(sql)
            # Busco por descripción, y si no lo encuentro, busco por la
            # descripción ampliada. Por eso hago esta asignación:
            record = res[0]
        except IndexError:
            sql = "SELECT * FROM %s.dbo.Articulos WHERE " % (c.get_database())
            where = r"Descripcion2Articulo = '%s';" % (nombre)
            sql += where
            res = c.run_sql(sql)
        except TypeError:   # res es None. Error con la base de datos
            if DEBUG:
                res = []
    else:   # Busco por el código de Murano: PC|PV + ID
        idmurano = get_codigo_articulo_murano(producto)
        sql = "SELECT * FROM %s.dbo.Articulos WHERE " % (c.get_database())
        where = r"CodigoArticulo = '%s';" % (idmurano)
        sql += where
        res = c.run_sql(sql)
    if DEBUG:
        try:
            assert len(res) == 1
        except AssertionError:
            if not res or len(res) == 0:
                raise AssertionError, "No se encontraron registros."
            elif len(res) > 1:
                raise AssertionError, "Se encontró más de un artículo:\n %s"%(
                        "\n".join([str(i) for i in res]))
    return res

def update_calidad(articulo, calidad):
    """
    Cambia la calidad del artículo en Murano a la recibida. Debe ser A, B o C.
    """
    if calidad not in "aAbBcC":
        raise ValueError, "El parámetro calidad debe ser A, B o C."
    # DONE: [Marcos Sage] No modificamos tablas. Hacemos salida del producto A
    # y volvemos a insertarlo como C. En ese caso no importa que se repita el 
    # código para el mismo producto porque antes hemos hecho la salida.
    # TODO: Ojo porque si cambio a calidad C probablemente implique un cambio de producto.
    raise NotImplementedError, "Función no disponible por el momento."

def create_articulo(articulo, cantidad = 1, producto = None):
    """
    Crea un artículo nuevo en Murano con el producto recibido. Si no se
    recibe ninguno, se usa el que tenga asociado en ginn. Si se recibe un
    objeto producto, se ignora el actual del artículo, se reemplaza en ginn
    por el recibido y se da de alta así en Murano.
    """
    if cantidad < 0:
        delta = 1
    else:
        delta = -1
    for i in range(abs(cantidad)):
        if articulo.es_bala():
            create_bala(articulo.bala, delta, producto)
        elif articulo.es_balaCable():
            create_bala(articulo.balaCable, delta, producto)
        elif articulo.es_bigbag():
            create_bigbag(articulo.bigbag, delta, producto)
        elif articulo.es_caja():
            create_caja(articulo.caja, delta, producto)
        elif articulo.es_rollo():
            create_rollo(articulo.rollo, delta, producto)
        elif articulo.es_rolloC():
            create_rollo(articulo.rolloC, delta, producto)
        else:
            raise ValueError, "El artículo %s no es bala, bala de cable, "\
                              "bigbag, caja, rollo ni rollo C." % (
                                      articulo.puid)

def update_producto(articulo, producto):
    """
    Cambia el artículo recibido al producto indicado.
    """
    delete_articulo(articulo)
    create_articulo(articulo, producto = producto)

def update_stock(producto, delta, almacen):
    """
    Incrementa o decrementa el stock del producto en la cantidad recibida en
    en el parámetro «delta».
    El producto no debe tener trazabilidad. En otro caso deben usarse las
    funciones "crear_[bala|rollo...]".
    """
    assert(isinstance(producto, pclases.ProductoCompra))
    partida = ""
    unidad_medida = "" # producto.unidad
    comentario = ("Stock ginn: %f [%s]" % (delta, producto.get_info()))[:40]
    ubicacion = "Almacén general"[:15]
    numero_serie_lc = ""
    c = Connection()
    database = c.get_database()
    today = datetime.datetime.today()
    ejercicio = today.year
    periodo = today.month
    fecha = today.strftime("%Y-%m-%d %H:%M:%S")
    documento = int(today.strftime("%Y%m%d"))
    codigo_articulo = buscar_codigo_producto(producto)
    codigo_almacen = buscar_codigo_almacen(almacen)
    codigo_talla = ""   # No hay calidades en los productos de compra.
    grupo_talla = 0 # No tratamiento de calidades en productos sin trazabilidad.
    if delta >= 0:
        tipo_movimiento = 1     # 1 = entrada, 2 = salida.
    else:
        delta = abs(delta)
        tipo_movimiento = 2
    unidades = delta    # En dimensión base del producto.
    #precio = producto.precioDefecto
    precio = buscar_precio_coste(producto, ejercicio, codigo_almacen)
    importe = unidades * precio
    factor_conversion = buscar_factor_conversion(producto)
    unidades2 = unidades * factor_conversion
    origen_movimiento = "F" # E = Entrada de Stock (entrada directa), 
                            # F (fabricación), I (inventario), 
                            # M (rechazo fabricación), S (Salida stock)
    id_proceso_IME = crear_proceso_IME(c)
    sql_movstock = SQL % (database,
                          CODEMPRESA, ejercicio, periodo, fecha, documento,
                          codigo_articulo, codigo_almacen, partida,
                          grupo_talla, codigo_talla, tipo_movimiento, unidades,
                          unidad_medida, precio, importe, unidades2,
                          factor_conversion, comentario, ubicacion,
                          origen_movimiento, numero_serie_lc,
                          id_proceso_IME)
    c.run_sql(sql_movstock)
    fire(id_proceso_IME)

def delete_articulo(articulo):
    """
    Elimina el artículo en Murano mediante la creación de un movimiento de
    stock negativo de ese código de producto.
    """
    create_articulo(articulo, cantidad = -1)

def consumir(productoCompra, cantidad, almacen = None, consumo = None):
    """
    Decrementa las existencias del producto recibido en la cantidad indicada
    mediante registros de movimientos de stock en Murano en el almacén
    principal si no se indica otro como tercer parámetro o en el almacén del
    silo correspondiente si almacen es None, el producto de compra no es de
    granza y se especifica un consumo.
    """
    if not almacen:
        if not productoCompra.es_granza():
            almacen = pclases.Almacen.get_almacen_principal() # Los consumos de 
                    # materia prima siempre se hacen desde el almacén principal.
                    # EXCEPTO los de granza, que se hacen desde un silo que se
                    # trata como almacén en Murano.
        else:
            try:
                almacen = consumo.silo
            except AttributeError:
                raise ValueError, "Si no especifica un almacén debe indicar "\
                                  "el consumo origen de ginn como referencia."
    update_stock(productoCompra, -cantidad, almacen)

def fire(guid_proceso):
    """
    Lanza el proceso de importación de Murano de todos los movimientos de
    stock de la tabla temporal.
    """
    strerror = "No puede ejecutar código nativo de Murano. Necesita instalar"\
               " la biblioteca win32com y lanzar esta función desde una "\
               "plataforma donde se encuentre instalado Sage Murano."
    if not LCOEM:
        raise NotImplementedError, strerror
    burano = win32com.client.Dispatch("LogicControlOEM.OEM_EjecutaOEM")
    burano.InicializaOEM(CODEMPRESA,
                         "OEM",
                         "oem",
                         "",
                         r"LOGONSERVER\MURANO",
                         "GEOTEXAN")
    retCode = None
    operacion = "ImportaIME"
    retCode = burano.EjecutaOEM("LCCImExP.LcImExProceso", operacion,
                                str(guid_proceso), 1, 1, 0)
    # 1 = No borrar registros IME al finalizar.
    # 1 = No borrar registros con errores ni siquiera cuando el primer 
    # parámetro esté a 0.
    # 0 = Ejecutar en todos los módulos.
    # Después de cada proceso hay que invocar al cálculo que acumula los
    # campos personalizados:
    # FIXED: No ejecuta el cálculo. Era por las '' alrededor del guid. Según el
    # .chm de ayuda los parámetros van sin encerrar en nada aunque sean cadena.
    retCode = burano.EjecutaScript("AcumularCamposNuevosSeries",
                         "Label:=Inicio, idProcesoIME:=%s" % guid_proceso)
