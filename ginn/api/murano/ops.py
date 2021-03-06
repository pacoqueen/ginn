#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Operaciones.

"""

# TODO: No sincroniza el campo que indica que el geotextil es C en los
# productos de venta de tipo Geotextil.

# pylint: disable=too-many-lines, wrong-import-position
# pylint: relative-import

from __future__ import print_function
import os
import sys
import time
import logging
from collections import defaultdict, namedtuple
from tempfile import gettempdir

NOMFLOG = ".".join(os.path.basename(__file__).split(".")[:-1])
try:
    logging.basicConfig(filename="%s.log" % (NOMFLOG),
                        format="%(asctime)s %(levelname)-8s : %(message)s",
                        level=logging.DEBUG)
# pylint:disable=bare-except
except:     # Error de permisos. Fallback a temporal                     # noqa
    NOMFLOG = os.path.join(gettempdir(), "ops.tmp")
    logging.basicConfig(filename="{}{}.log".format(NOMFLOG, time.time()),
                        format="%(asctime)s %(levelname)-8s : %(message)s",
                        level=logging.DEBUG)

import datetime                                                          # noqa
from connection import Connection, DEBUG, VERBOSE, CODEMPRESA, CANALES   # noqa
from connection import FABRICACION, ENTRADA, SALIDA, INVENTARIO, VENTA   # noqa
from export import determinar_familia_murano                             # noqa
from extra import get_peso_bruto, get_peso_neto, get_superficie          # noqa
from extra import AttrDict                                               # noqa

try:
    import win32com.client
except ImportError:
    LCOEM = False
else:
    LCOEM = True

RUTA_GINN = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "ginn"))
sys.path.append(RUTA_GINN)
from framework import pclases   # pylint: disable=import-error          # noqa


# DocumentoUnico a «No» para evitar error con decimales.
SQL_STOCK = """INSERT INTO [%s].[dbo].[TmpIME_MovimientoStock](
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
               UnidadMedida2_,
               FactorConversion_,
               Comentario,
               CodigoCanal,
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
               DocumentoUnico,
               -- FechaRegistro,
               MovPosicion
               )
           VALUES (
               %d,      -- código empresa
               %d,      -- ejercicio
               %d,      -- periodo
               '%s',    -- fecha
               '%s',    -- serie ('FAB'|'API')
               %d,      -- documento
               '%s',    -- codigo_articulo
               '%s',    -- codigo_almacen
               -- '',
               '%s',    -- partida
               -- NULL,
               -- NULL,
               %d,      -- grupo_talla
               '%s',    -- codigo_talla
               %d,      -- tipo_movimiento
               %f,      -- unidades en la unidad de medida específica (m², kg)
               '%s',    -- unidad de medida específica
               %f,      -- precio
               %f,      -- importe
               %f,      -- unidades2 = unidades * factor de conversion | fc!=0
               '%s',    -- UnidadMedida2_ (la básica: ROLLO, BALA...)
               %f,      -- factor de conversión
               '%s',    -- comentario
               '%s',    -- Canal. Antes DIV para evitar un bug de Murano.
               -- NULL,
               -- NULL,
               -- NULL,
               '%s',    -- ubicación
               '%s',    -- origen movimiento
               -- NULL,
               -- NULL,
               -- NULL,
               '%s',    -- NumeroSerieLc
               '%s',    -- IdProcesoIME
               -- NULL,
               0,
               0,
               0,
               -- NULL,
               '%s'     -- GUID MovPosicion
               );"""    # NOQA

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
            VALUES (
                %d,     -- código empresa
                '%s',   -- código artículo
                '%s',   -- número de serie del artículo
                '%s',   -- fecha
                %d,     -- origen documento
                %d,     -- ejercicio
                '%s',   -- serie ('FAB'|'API')
                %d,     -- documento
                '%s',   -- mov. posición origen
                -- NULL,
                '%s',   -- código talla
                '%s',   -- código almacén
                '%s',   -- ubicación
                '%s',   -- partida
                '%s',   -- unidad de medida básica (ROLLO, BALA...)
                        -- NO la específica (kg, m²)
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


def buscar_grupo_talla(producto_venta):
    """
    Devuelve el código de grupo de tallas (calidades) que puede tener el
    producto.
    """
    # Hemos varios grupos de talla: 1 para A, B y C, 2 para A, B (sin C), etc.
    grupo_talla = 0     # Sin grupo de talla
    # res = consultar_producto(nombre = productoVenta.descripcion)
    res = consultar_producto(producto_venta)
    try:
        grupo_talla = res[0]['GrupoTalla_']
    except TypeError as exception:
        strlog = "(EE)[T] %s no se encuentra en Murano." % (
            producto_venta.descripcion)
        print(strlog)
        logging.error(strlog)
        if not DEBUG:
            raise exception
        grupo_talla = 0
    return grupo_talla


# pylint: disable=too-many-branches
def buscar_unidad_medida_basica(producto, articulo=None):
    """
    Devuelve la unidad de medida básica de la ficha de murano para el
    producto indicado. Devuelve "" si el producto no lleva tratamiento de
    serie, porque en ese caso el registro de movimiento de stock solo debe
    llevar una unidad. Y esta función se usa para determinar la segunda.

    ***

    OBSOLETO:
    ---------
    Devuelve la unidad de medida básica según el tipo de producto en ginn.
    Si el producto es un producto de compra o de venta pero sin trazabilidad
    (como ocurre con la granza reciclada, por ejemplo), devuelve la cadena
    vacía como unidad2, ya que en esos movimientos -Sage dixit- el campo
    UnidadMedida2_ debe quedar vacío.
    Si se especifica un artículo, la unidad de éste (BALA, ROLLO, BIGBAG...)
    prevalece sobre la general del producto. Útil para productos que pueden
    empaquetarse tanto en balas como en bigbags.
    """
    # Al principio me dijo Félix que la buscara en Murano, pero no lo hago por
    # dos motivos:
    # 1.- Puede que la unidad básica en mirano sea la BALA pero estemos
    #     mandando un BIGBAG de ese producto.
    # 2.- Por optimización. Cada consulta al MS-SQLServer tarda más que
    #     cualquier operación compleja contra PostgreSQL. Y CONSUME LICENCIA.
    unidad2 = ""
    if articulo:
        if articulo.es_bala():
            unidad2 = "BALA"
        elif articulo.es_bala_cable():
            unidad2 = "BALA"
        elif articulo.es_rollo():
            unidad2 = "ROLLO"
        elif articulo.es_rollo_defectuoso():
            unidad2 = "ROLLO"
        elif articulo.es_rollo_c():
            unidad2 = "ROLLO"
        elif articulo.es_bigbag():
            unidad2 = "BIGBAG"
        elif articulo.es_caja():
            unidad2 = "CAJA"
    if not unidad2:     # Si no artículo o por artículo no se encontró nada.
        if isinstance(producto, pclases.ProductoVenta):
            if producto.es_bala() or producto.es_bala_cable():
                unidad2 = "BALA"
            elif producto.es_rollo() or producto.es_rollo_c():
                unidad2 = "ROLLO"
            elif producto.es_bigbag():
                unidad2 = "BIGBAG"
            elif producto.es_caja() or producto.es_bolsa():
                unidad2 = "CAJA"
            else:
                # es_especial, es_granza o algo así. No lleva unidad2 en Murano
                strlog = "(EE)[U] UnidadMedida2_ para «%s» (%s) indeterminada"\
                         "." % (producto.descripcion, producto.puid)
                logging.error(strlog)
                unidad2 = ""
                # raise ValueError, strlog
        else:   # Es producto de compra. La unidad2 no debe informarse.
            unidad2 = ""
    return unidad2


# pylint: disable=invalid-name
def buscar_unidad_medida_basica_murano(producto):
    """
    Devuelve la unidad de medida básica de la ficha del producto.
    """
    res = consultar_producto(producto)
    try:
        unidad2 = res[0]['UnidadMedida2_']
    except TypeError as exception:
        strlog = "(EE)[U] UnidadMedida2_ para %s no se encuentra en Murano"\
                 "." % (producto.descripcion)
        print(strlog)
        logging.error(strlog)
        if not DEBUG:
            raise exception
        unidad2 = "ROLLO|BALA|BIGBAG|CAJA"
    return unidad2


def buscar_marcado_ce(producto):
    """
    Devuelve los valores de marcado CE para el producto recibido.
    Se devuelve como un diccionario de nombre de campo y valor.
    """
    id_murano = buscar_codigo_producto(producto)
    if not id_murano:
        strerror = "El producto [{}] {} no existe en Murano.".format(
            producto.puid, producto.descripcion)
        logging.error(strerror)
        res = None
    else:
        c = Connection()    # pylint: disable=no-value-for-parameter
        try:
            # pylint: disable=no-member
            sql = "SELECT * FROM %s.dbo.GEO_ArticulosMarcado"\
                  " WHERE " % (c.get_database())
            where = r"CodigoArticulo = '%s';" % (id_murano)
            sql += where
            res = c.run_sql(sql)
            record = res[0]     # NOQA
        except IndexError:
            strerror = "El producto [{}] {} no tiene registro de marcado en "\
                "Murano.".format(producto.puid, producto.descripcion)
            res = None
        else:
            res = desmuranize_valor(record)
    return res


def desmuranize_valor(record):
    """
    Al objeto recibido le convierte los nombres de los atributos al
    equivalente en ginn.
    """
    record_murano = {}
    for clave in record.keys():
        if clave not in ("CodigoEmpresa", "CodigoArticulo"):
            clave_ginn = field_murano2ginn(clave)
            if "." in clave_ginn:  # tabla_realcionada.campo. Me quedo solo
                # con el campo.
                clave_ginn = clave_ginn.split(".")[-1]
            record_murano[clave_ginn] = record[clave]
    RecordMurano = namedtuple('RecordMurano', record_murano.keys())
    res = RecordMurano(**record_murano)
    return res


def field_murano2ginn(campo):
    """
    Devuelve el nombre del campo equivalente en productos de ginn al de Murano
    recibido. Si no tiene equivalencia devuelve None.
    Devuelve el nombre_de_la_tabla.campo. Si el campo en la tabla de Murano se
    puede corresponder con varios de ginn, se devuelve así:
    nombre_tabla1/nombre_tabla2.campo_ginn
    (el campo_ginn se supone que se llama igual en las dos tablas)
    SHOW ME THE CODE!
    """
    # De momento solo lo necesito para los campos de Marcado CE.
    switcher = {
        'GEO_est_por_gramaje': 'camposEspecificosRollo.estandarPruebaGramaje',
        'GEO_est_pr_alar_long':
            'camposEspecificosRollo.estandarPruebaAlargamientoLongitudinal',
        'GEO_est_pr_alar_trans':
            'camposEspecificosRollo.estandarPruebaAlargamientoTransversal',
        'GEO_est_pr_compresion':
            'camposEspecificosRollo.estandarPruebaCompresion',
        'GEO_est_pr_espesor': 'camposEspecificosRollo.estandarPruebaEspesor',
        'GEO_est_pr_long': 'camposEspecificosRollo.estandarPruebaLongitudinal',
        'GEO_est_pr_perforacion':
            'camposEspecificosRollo.estandarPruebaPerforacion',
        'GEO_est_pr_permeabilidad':
            'camposEspecificosRollo.estandarPruebaPermeabilidad',
        'GEO_est_pr_piramidal':
            'camposEspecificosRollo.estandarPruebaPiramidal',
        'GEO_est_pr_poros': 'camposEspecificosRollo.estandarPruebaPoros',
        'GEO_est_pr_trans': 'camposEspecificosRollo.estandarPruebaTransversal',
        'GEO_tol_por_gramaje':
            'camposEspecificosRollo.toleranciaPruebaGramaje',
        'GEO_tol_por_gramaje_sup':
            'camposEspecificosRollo.toleranciaPruebaGramajeSup',
        'GEO_tot_pr_alar_long':
            'camposEspecificosRollo.toleranciaPruebaAlargamientoLongitudinal',
        'GEO_tot_pr_alar_long_sup':
            'toleranciaPruebaAlargamientoLongitudinalSup',
        'GEO_tot_pr_alar_trans':
            'camposEspecificosRollo.toleranciaPruebaAlargamientoTransversal',
        'GEO_tot_pr_alar_trans_sup':
            'toleranciaPruebaAlargamientoTransversalSup',
        'GEO_tot_pr_compresion':
            'camposEspecificosRollo.toleranciaPruebaCompresion',
        'GEO_tot_pr_compresion_sup':
            'camposEspecificosRollo.toleranciaPruebaCompresionSup',
        'GEO_tot_pr_espesor': 'camposEspecificosRollo.toleranciaPruebaEspesor',
        'GEO_tot_pr_espesor_sup':
            'camposEspecificosRollo.toleranciaPruebaEspesorSup',
        'GEO_tot_pr_long':
            'camposEspecificosRollo.toleranciaPruebaLongitudinal',
        'GEO_tot_pr_long_sup':
            'camposEspecificosRollo.toleranciaPruebaLongitudinalSup',
        'GEO_tot_pr_perforacion':
            'camposEspecificosRollo.toleranciaPruebaPerforacion',
        'GEO_tot_pr_perforacion_sup':
            'camposEspecificosRollo.toleranciaPruebaPerforacionSup',
        'GEO_tot_pr_permeabilidad':
            'camposEspecificosRollo.toleranciaPruebaPermeabilidad',
        'GEO_tot_pr_permeabilidad_sup':
            'camposEspecificosRollo.toleranciaPruebaPermeabilidadSup',
        'GEO_tot_pr_piramidal':
            'camposEspecificosRollo.toleranciaPruebaPiramidal',
        'GEO_tot_pr_piramidal_sup':
            'camposEspecificosRollo.toleranciaPruebaPiramidalSup',
        'GEO_tot_pr_poros': 'camposEspecificosRollo.toleranciaPruebaPoros',
        'GEO_tot_pr_poros_sup':
            'camposEspecificosRollo.toleranciaPruebaPorosSup',
        'GEO_tot_pr_trans':
            'camposEspecificosRollo.toleranciaPruebaTransversal',
        'GEO_tot_pr_trans_sup':
            'camposEspecificosRollo.toleranciaPruebaTransversalSup',
        # -- Campos generales en común. Algunos son funciones que reciben el
        #               valor de Murano y devuelvel el correspondiente en ginn
        'DescripcionLinea': _get_linea_produccion_ginn,
        'DescripcionArticulo': 'nombre',
        'Descripcion2Articulo': 'descripcion',
        'CodigoAlternativo': 'codigo',
        'StockMinimo': 'minimo',
        'PrecioVenta': 'preciopordefecto',
        'CodigoArancelario': 'arancel',
        'GEO_ProdEstandar': 'prodestandar',
        'GEO_anno_certificacion': 'annoCertificacion',
        'GEO_Dni': 'dni',
        'GEO_Usi': _get_uso_ginn,
        'ObsoletoLc': 'obsoleto',
        # -- Campos específicos de rollos
        'GEO_gramos': 'camposEspecificosRollo.gramos',
        'GEO_rollos_por_camion': 'camposEspecificosRollo.rollosPorCamion',
        'GEO_Modelo_etiqueta_id': _get_modelo_etiqueta_ginn,
        #     'camposEspecificosRollo.modeloEtiquetaID',
        'GEO_Diametro': 'camposEspecificosRollo.diametro',
        'GEO_Ficha_fabricacion': 'camposEspecificosRollo.fichaFabricacion',
        'MarcaProducto': 'camposEspecificosRollo.codigoComposan',
        'GEO_ancho': 'camposEspecificosRollo.ancho',
        'GEO_metros_lineales': 'camposEspecificosRollo.metrosLineales',
        'GEO_calidad_C': 'camposEspecificosRollo.c',
        'GEO_peso_embalaje': 'camposEspecificosRollo.pesoEmbalaje',
        'GEO_Cliente_id':
            'camposEspecificosRollo/camposEspecificosBala.clienteID',
        # Campos específicos de fibra:
        'GEO_Consumo_granza': 'camposEspecificosBala.consumoGranza',
        'GEO_Tipo_Material_bala_id': _get_tipo_material_bala_ginn,
        'GEO_bolsas_Caja': 'camposEspecificosBala.bolsasCaja',
        'GEO_gramos_bolsa': 'camposEspecificosBala.gramosBolsa',
        'GEO_Reciclada': 'camposEspecificosBala.reciclada',
        'GEO_Color': 'camposEspecificosBala.color',
        'GEO_Cajas_pale': 'camposEspecificosBala.cajasPale',
        # 'GEO_Cliente_id': 'camposEspecificosBala.clienteID', # DUPE
        'GEO_Dtex': 'camposEspecificosBala.dtex',
        'GEO_Corte': 'camposEspecificosBala.corte',
        'GEO_antiuvi': 'camposEspecificosBala.antiuv',
    }
    return switcher.get(campo, None)


def _get_tipo_material_bala_ginn(codigo_murano):
    """
    Devuelve el ID del tipo de material de fibra según el código recibido
    de Murano:
    - '': None
    - 'PR': 1 (Polipropileno)
    - 'LI': 2 (Poliéster)
    """
    # HARCODED
    if codigo_murano == 'PR':
        # Por error en Sage, lo teclearon como Prolipopileno
        res = 1
    elif codigo_murano == 'LI':
        res = 2
    else:
        res = None
    if res:
        res = pclases.TipoMaterialBala.get(res)
    return res


def _get_modelo_etiqueta_ginn(id_etiqueta_murano):
    """
    Devuelve el ID del modelo de la etiqueta en ginn correspondiente al ID
    de Murano para ese mismo modelo recibido.
    Si no lo encuentra o no está establecido en Murano (0), devuelve None.
    """
    # TODO: Debería mirar los campos módulo y función de Murano y dejar todo
    # este lío de mantener las tablas con ID idéntico entre ambos programas.
    # Ya en Murano tienen una tabla con (id, nombre, modelo, función). Esta
    # función debe convertirse en un "sincronizar" las dos tablas o bien
    # sincronizar el registro en cuestión trayéndose modelo y función. Quizás
    # lo primero. Tengo que "echarle una pensada".
    if id_etiqueta_murano == 4:
        # Normativa julio 2013
        res = 4
    elif id_etiqueta_murano in range(1, 99):  # Hasta 99 modelos. Cambiable.
        # Resulta que el ID coincide en ambas bases de datos.
        res = id_etiqueta_murano
    else:   # Incluido el 0, que es el equivalente al None en Murano
        res = None
    if res:
        res = pclases.ModeloEtiqueta.get(res)
    else:
        # Valor por defecto
        res = pclases.ModeloEtiqueta.get_default()
    return res


def _get_uso_ginn(codigo_uso):
    """
    Si recibe, devuelve:
    - DP: Drenaje, filtración, refuerzo, separación, protección
    - DS: Drenaje, filtración, refuerzo, separación
    - FP: Fibra de polipropileno virgen embolsada en papel hidrosoluble para
          su uso como aditivo del hormigón
    - FV: Fibra de polipropileno virgen
    - FS: Filtración, separación
    - FR: Filtración, separación, protección
    - '': ''
    Resto: None
    """
    if codigo_uso == 'DP':
        res = "Drenaje, filtración, refuerzo, separación, protección"
    elif codigo_uso == 'DS':
        res = "Drenaje, filtración, refuerzo, separación"
    elif codigo_uso == 'FP':
        res = "Fibra de polipropileno virgen embolsada en papel hidrosoluble"\
              " para su uso como aditivo del hormigón"
    elif codigo_uso == 'FV':
        res = "Fibra de polipropileno virgen"
    elif codigo_uso == 'FS':
        res = "Filtración, separación"
    elif codigo_uso == 'FR':
        res = "Filtración, separación, protección"
    elif codigo_uso == '':
        res = ""
    else:
        res = None
    return res


def _get_linea_produccion_ginn(descripcion_linea):
    """
    Devuelve el registro de ginn que se corresponde con la descripción de la
    línea de producción de Murano recibida.
    """
    try:
        linea = descripcion_linea.split()[-1]
        if linea.endswith("s"):
            linea = linea[:-1]
        if linea.lower() == "geocem":
            # Problema entre el teclado y la silla. A veces se confunden...
            linea = "embolsado"
    except AttributeError:
        # Es un producto de venta especial. Sin línea de producción.
        linea = None
    try:
        # pylint: disable=no-member
        lineas_ginn = pclases.LineaDeProduccion.select(
            pclases.LineaDeProduccion.q.nombre.contains(linea))
        assert lineas_ginn.count() == 1
        linea_ginn = lineas_ginn[0]
    except IndexError:
        linea_ginn = None
    except AssertionError:
        logging.warning("Encontradas %d posibles líneas de producción para %s",
                        lineas_ginn.count(), descripcion_linea)
        linea_ginn = lineas_ginn[0]
    return linea_ginn


def buscar_codigo_producto(producto_venta):
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
    # res = consultar_producto(nombre = productoVenta.descripcion)
    res = consultar_producto(producto=producto_venta)
    try:
        codarticulo = res[0]['CodigoArticulo']
        desc_ginn = producto_venta.descripcion
        assert (desc_ginn.startswith(res[0]['DescripcionArticulo']) or
                desc_ginn.startswith(res[0]['Descripcion2Articulo']))
    except (IndexError, TypeError) as exception:
        strlog = "(EE)[C] %s no se encuentra en Murano. Excepción: %s" % (
            producto_venta.descripcion, exception)
        print(strlog)
        logging.error(strlog)
        if not DEBUG:
            raise exception
        else:
            codarticulo = ''
    except AssertionError:
        strlog = '(WW)[C] La descripción de "%s" (%s) ha cambiado.'\
                 ' En Murano es: "%s"/"%s"' % (producto_venta.descripcion,
                                               producto_venta.puid,
                                               res[0]['DescripcionArticulo'],
                                               res[0]['Descripcion2Articulo'])
        try:
            print(strlog)
        except IOError:     # pythonw. No estoy conectado a un terminal.
            pass
        logging.warning(strlog)
    return codarticulo


def buscar_precio_coste(producto, ejercicio, codigo_almacen):
    """
    Devuelve el importe en €/kg definido en Murano y después en ginn (si no se
    encuenta) para la familia del producto.
    Si es producto de compra, devuelve el precio de valoracion por unidad de
    producto según la función de valoración definida para él.
    """
    cod_familia = determinar_familia_murano(producto)
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
        raise ValueError("ops:buscar_precio_coste: el producto «%s» recibido"
                         " no es un producto de compra ni de venta."
                         % (producto))
    try:
        precio_coste = float(precio_coste)  # Viene como Decimal
    except TypeError:   # No tiene precio de coste en ningún sitio.
        precio_coste = 0.0
    return precio_coste


def buscar_precio_coste_familia_murano(cod_familia):
    """
    Devuelve el precio de coste de la base de datos de Murano para el código
    de familia recibido.
    Lanza ValueError si el código de familia no se encuentra o no tiene
    precio de coste.
    """
    # pylint: disable=no-value-for-parameter,no-member
    c = Connection()
    # SQL = r"""SELECT TOP 1 PrecioPorUnidadEspecifica
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
    except (TypeError, AttributeError, KeyError):
        # cod_familia es None o no se encontraron registros
        raise ValueError
    except Exception as exception:  # pylint: disable=broad-except
        logging.warning("No se encontró precio en Murano para la familia "
                        "«%s». Además, provocó una excepción %s.",
                        cod_familia, exception)
        precio_coste = None
    return precio_coste


def buscar_precio_coste_familia_ginn(cod_familia):
    """
    Devuelve el precio por familia definido en ginn.
    """
    # HARCODED: Esto debeía ir en la tabla de ginn correspondiente
    # y reflejarlo en la ventana que sea (no hay ventana de familias).
    # En teoría no haría falta ya que siempre van a venir de Murano.
    if cod_familia == "GEO":
        precio_coste = 2.210
    elif cod_familia == "FIB" or cod_familia == "FCE":
        precio_coste = 1.545
    elif cod_familia == "FEM":
        precio_coste = 1.884
    else:
        raise ValueError("cod_familia debe ser GEO, FIB, FCE o FEM. Se "
                         "recibió: %s" % (cod_familia))
    return precio_coste


def buscar_precio_coste_murano(producto, ejercicio, codigo_almacen):
    """
    Devuelve el precio de coste de la base de datos de Murano para el producto
    recibido. Según Sage lo aconsejable es enviar el «PrecioMedio» en el
    momento del consumo del producto. Se almacena en el campo «PrecioMedio»
    de la tabla «AcumuladoStock», donde solo hay un registro por producto,
    año y periodo. El periodo 99 siempre guarda el más actualizado.
    """
    # pylint: disable=no-value-for-parameter,no-member
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
                  codigo_almacen,
                  CODEMPRESA)
    try:
        precio_coste = c.run_sql(SQL)[0]["PrecioMedio"]
    except (TypeError, AttributeError, KeyError, IndexError):
        # codalmacen es None o no se encontraron registros
        raise ValueError
    except Exception as exception:  # pylint: disable=broad-except
        logging.warning("No se encontró precio medio en Murano para el "
                        "producto «%s». Además, provocó una excepción %s.",
                        cod_articulo, exception)
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
        cod_familia = determinar_familia_murano(producto)
        precio_coste = buscar_precio_coste_familia_ginn(cod_familia)
    else:
        # WTF?
        raise ValueError("ops:buscar_precio_coste_ginn: el producto «%s» "
                         "recibido no es un producto de compra ni de venta."
                         % (producto))
    return precio_coste


def buscar_codigo_almacen(almacen, articulo=None):
    """
    Devuelve almacén de la empresa configurada cuyo nombre coincida con el del
    almacén de ginn recibido.
    Si el almacén recibido es None, entonces buscará el almacén actual donde
    dice Murano que está el artículo recibido como segundo parámetro.
    """
    # pylint: disable=no-value-for-parameter,no-member
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
        except Exception as exception:  # pylint: disable=broad-except
            strlog = "(EE)[A] Almacén '%s' no se encuentra en Murano." % (
                almacen.nombre)
            print(strlog)
            logging.error(strlog)
            if not DEBUG:
                raise exception
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
                raise ValueError("(EE)[A] Debe especificarse un almacén "
                                 "o un artículo.")
    return codalmacen


def simulate_guid():
    """
    Genera un código aleatorio similar al generado por MSSQLServer.
    """
    if VERBOSE and DEBUG:
        strlog = "Simulando guid..."
        print(strlog)
        logging.info(strlog)
    import random
    grupos = 8, 4, 4, 4, 12
    subgrupos = []
    for g in grupos:
        subgrupo = ""
        for i in range(g):  # pylint: disable=unused-variable
            c = random.choice("01234567890ABCDE")
            subgrupo += c
        subgrupos.append(subgrupo)
    guid = "-".join(subgrupos)
    if VERBOSE and DEBUG:
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


def generar_guid(conexion):
    """
    Devuelve un GUID de SQLServer o simula uno en modo depuración.
    """
    try:
        guid = conexion.run_sql("SELECT NEWID() AS guid;")[0]['guid']
    except Exception as exception:  # pylint: disable=broad-except
        if not DEBUG:
            raise exception
        else:
            guid = simulate_guid()
    return guid


def get_mov_posicion(conexion, codigo_articulo):
    """
    Devuelve el GUID del movimiento de stock asociado al movimiento de número
    de serie. Si el número de serie (el código de artículo) no está en Murano,
    lanza una excepción.
    Si está activado el modo de depuración, devuelve un GUID simulado
    aleatorio.
    """
    try:
        mov_posicion = conexion.run_sql(r"""SELECT TOP 1 MovPosicion
            FROM %s.dbo.TmpIME_MovimientoStock
            WHERE NumeroSerieLc = '%s'
            ORDER BY FechaRegistro DESC;
            """ % (conexion.get_database(), codigo_articulo))[0]['MovPosicion']
    except Exception as exception:  # pylint: disable=broad-except
        if not DEBUG:
            raise exception
        else:
            mov_posicion = simulate_guid()
    return mov_posicion


def get_ultimo_movimiento_articulo_serie(conexion, articulo):
    """
    Devuelve el registro de Murano que contiene la última información del
    código del artículo recibido. Típicamente será un movimiento de entrada de
    fabricación, de salida por albarán o None si no existe el artículo en
    Murano.
    """
    try:
        codigo_articulo = articulo.codigo
    except AttributeError:
        # Por si recibo directamente un código.
        codigo_articulo = articulo
    SQL = r"""SELECT TOP 1 *
              FROM [%s].[dbo].[MovimientoArticuloSerie]
              WHERE NumeroSerieLc = '%s' AND CodigoEmpresa = '%d'
              ORDER BY FechaRegistro DESC;""" % (conexion.get_database(),
                                                 codigo_articulo,
                                                 CODEMPRESA)
    try:
        registro_serie = conexion.run_sql(SQL)[0]
    except (TypeError, AttributeError, KeyError, IndexError):
        # Ese código de artículo (NumeroSerieLc) nunca ha existido en Murano.
        registro_serie = None
    return registro_serie


def get_codalmacen_articulo(conexion, articulo):
    """
    Busca el último movimiento de stock del artículo y devuelve el código
    de almacén si es un movimiento de entrada o la cadena vacía si es de
    salida.
    """
    registro_serie = get_ultimo_movimiento_articulo_serie(conexion, articulo)
    if registro_serie is None:
        # codalmacen es None o no se encontraron registros
        codalmacen = ""
    else:
        codalmacen = registro_serie["CodigoAlmacen"]
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
    guid_proceso = generar_guid(conexion)
    conexion.run_sql(r"""
        INSERT INTO %s.dbo.Iniciador_tmpIME(IdProcesoIME, EstadoIME,
                                            sysUsuario, sysUserName,
                                            Descripcion, TipoImportacion)
        VALUES ('%s', 0, 1, 'administrador', 'Gateway ginn API Murano', 254);
        """ % (conexion.get_database(), guid_proceso))
    return guid_proceso


# pylint: disable=too-many-locals
def prepare_params_movstock(articulo, cantidad=1, producto=None,
                            codigo_almacen=None, calidad=None, fecha=None):
    """
    Prepara los parámetros comunes a todos los artículos con movimiento de
    serie y devuelve la conexión a la base de datos MS-SQLServer.
    Cantidad debe ser 1 para incrementar o -1 para decrementar el almacén.
    """
    assert abs(cantidad) == 1
    # pylint: disable=no-value-for-parameter,no-member
    c = Connection()
    database = c.get_database()
    if fecha is None or not isinstance(fecha, datetime.datetime):
        # TODO: Si la fecha no es correcta, en vez de petar ignoro el
        # error silenciosamente. Danger, danger! High voltage!
        today = datetime.datetime.today()
    else:
        today = fecha
    ejercicio = today.year
    periodo = today.month
    fecha = today.strftime("%Y-%m-%d %H:%M:%S")
    documento = int(today.strftime("%Y%m%d"))
    if not producto:
        producto = articulo.productoVenta
    codigo_articulo = buscar_codigo_producto(producto)
    if calidad is None:
        codigo_talla = articulo.get_str_calidad()
    else:
        codigo_talla = calidad.upper()
    grupo_talla = buscar_grupo_talla(producto)
    if cantidad == 1:
        tipo_movimiento = 1     # 1 = entrada, 2 = salida.
    else:
        tipo_movimiento = 2
    if not codigo_almacen:
        codigo_almacen = buscar_codigo_almacen(articulo.almacen, articulo)
    # OJO: Este caso no se dará cuando pasemos a producción. Todos los bultos a
    # consumir ya estarían en Murano previamente y con un almacén asignado.
    # Para pruebas me aseguro de que se envía un almacén buscando el último
    # donde estuvo el bulto.
    if not codigo_almacen:  # and tipo_movimiento == 2:
        # Es un consumo y en ginn almacen ya es None. En Murano también es
        # None porque puede ser un artículo que nunca había estado antes
        # en Murano. Como por fuerza debe llevar un almacén, buscamos el
        # almacén donde estaba antes de ser consumida la bala o bigbag.
        # Da igual el tipo de movimiento. Aunque sea una entrada, debemos
        # buscar el último almacén **al menos en pruebas**. Se da el caso en
        # que se fabrica un bigbag (por ejemplo) y se vende justo a
        # continuación antes de que dé tiempo a meterlo en Murano. Ya tiene
        # el almacén a None en ginn y ya no lo traga bien Murano.
        codigo_almacen = buscar_ultimo_almacen_conocido_para(articulo)
    # unidades = 1    # En dimensión base: 1 bala, rollo, caja, bigbag...
    # [20160207] Al final no era en dimensión base, sino en la específica.
    unidades = get_cantidad_dimension_especifica(articulo)
    # precio = 0.0
    precio_kg = buscar_precio_coste(producto, ejercicio, codigo_almacen)
    precio = estimar_precio_coste(articulo, precio_kg)
    factor_conversion = buscar_factor_conversion(producto)
    if factor_conversion:
        unidades2 = unidades * factor_conversion
    else:
        unidades2 = 1  # Siempre será uno porque por cada rollo o bala hay
        # solo 1 mov. stock y 1 mov. serie.
    importe = unidades2 * precio
    unidad_medida2 = buscar_unidad_medida_basica(producto, articulo)
    origen_movimiento = "F"  # E = Entrada de Stock (entrada directa),
    # F (fabricación), I (inventario),
    # M (rechazo fabricación), S (Salida stock)
    return (c, database, ejercicio, periodo, fecha, documento, codigo_articulo,
            codigo_almacen, grupo_talla, codigo_talla, tipo_movimiento,
            unidades, precio, importe, unidades2, unidad_medida2,
            factor_conversion, origen_movimiento)


def get_cantidad_dimension_especifica(articulo):
    """
    Devuelve la cantidad a sumar o restar del stock de Murano del artículo
    con código de trazabilidad recibido. Va en undad específica: kg o m².
    """
    if articulo.es_rollo() or articulo.es_rollo_defectuoso():
        # Los rollos C no tienen m² definidos. Se tratan al peso.
        unidades = get_superficie(articulo)  # En dimensión específica: m²
    elif (articulo.es_bala() or articulo.es_bala_cable() or
          articulo.es_rollo_c() or articulo.es_bigbag() or
          articulo.es_caja()):
        # unidades = articulo.get_peso()
        # unidades = get_peso_bruto(articulo)  # En dimensión específica: kg
        unidades = get_peso_neto(articulo)  # En dimensión específica: kg
    return unidades


def buscar_ultimo_almacen_conocido_para(articulo):
    """
    Devuelve el código de almacén de Murano para el último almacén conocido
    en ginn donde estuviera el artículo.
    """
    # Fallback al almacén principal, por si no tuviera ABSOLUTAMENTE ningún
    # movimiento.
    last_almacen = pclases.Almacen.get_almacen_principal()
    for movimiento in articulo.get_historial_trazabilidad()[::-1]:
        # Movimientos van del más antiguo al más nuevo. Empiezo por el final.
        fecha, objeto, almacen = movimiento   # pylint: disable=unused-variable
        if almacen:
            last_almacen = almacen
            break
    res = buscar_codigo_almacen(last_almacen)
    return res


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
    elif articulo.es_rollo_defectuoso():
        peso = articulo.peso
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
        raise ValueError(strerror)
    return peso * precio_kg


# pylint: disable=too-many-arguments
def create_bala(bala, cantidad=1, producto=None, guid_proceso=None,
                simulate=False, procesar=True, codigo_almacen=None,
                calidad=None, comentario=None, serie='API', fecha=None):
    """
    Crea una bala en las tablas temporales de Murano.
    Recibe un objeto bala de ginn.
    Si cantidad es -1 realiza la baja de almacén de la bala.
    Si simulate es True, devuelve las dos consultas SQL generadas. En otro
    caso, el valor de ejecutar el proceso de importación.
    Si procesar es False no lanza el proceso de importación a través de la
    DDL OEM de Murano.
    Si no se especifica comentario (None o ""), se usa uno por defecto.
    """
    articulo = bala.articulo
    if cantidad > 0 and duplica_articulo(articulo):
        logging.warning("La bala %s ya existe en Murano. Se ignora.",
                        bala.codigo)
        res = False
    else:
        try:
            partida = bala.lote.codigo
        except AttributeError:
            partida = ""  # Balas C no tienen lote. No pasa nada. Murano traga.
        unidad_medida = "KG"
        # Si comentario es "", viene de fabricación. Serie FAB.
        if not comentario:
            comentario = "[ginn] {}".format(bala.get_info())
            serie = 'FAB'
        comentario = comentario[:40]    # Por restricciones de Murano.
        ubicacion = "Almac. de fibra."[:15]
        numero_serie_lc = ""
        # Sage me indica que no informe de la serie en el movimiento de stock
        # para solucionar lo del registro duplicado creado por Murano.
        # pylint: disable=bad-continuation
        (c, database, ejercicio, periodo, fecha, documento, codigo_articulo,
         codigo_almacen, grupo_talla, codigo_talla, tipo_movimiento,
         unidades, precio, importe, unidades2, unidad_medida2,
         factor_conversion, origen_movimiento) = prepare_params_movstock(
            articulo, cantidad, producto, codigo_almacen, calidad, fecha=fecha)
        if not guid_proceso:
            id_proceso_IME = crear_proceso_IME(c)
        else:
            id_proceso_IME = guid_proceso
        guid_movposicion = generar_guid(c)
        canal_div = ''
        sql_movstock = SQL_STOCK % (database,
                                    CODEMPRESA, ejercicio, periodo, fecha,
                                    serie,
                                    documento, codigo_articulo, codigo_almacen,
                                    partida, grupo_talla, codigo_talla,
                                    tipo_movimiento, unidades, unidad_medida,
                                    precio, importe, unidades2, unidad_medida2,
                                    factor_conversion, comentario, canal_div,
                                    ubicacion, origen_movimiento,
                                    numero_serie_lc, id_proceso_IME,
                                    guid_movposicion)
        if simulate:
            # pylint: disable=redefined-variable-type
            # Si es una simulación, devuelvo las consultas SQL y no un bool.
            res = [sql_movstock]
        else:
            c.run_sql(sql_movstock)
        if cantidad < 0:
            origen_documento = SALIDA
        else:
            origen_documento = FABRICACION
        # mov_posicion_origen = get_mov_posicion(c, numero_serie_lc)
        mov_posicion_origen = guid_movposicion
        # En el movimiento de serie la UnidadMedida1_ es la básica:ROLLO,BALA..
        unidad_medida1 = buscar_unidad_medida_basica(articulo.productoVenta,
                                                     articulo)
        numero_serie_lc = bala.codigo
        peso_bruto = get_peso_bruto(articulo)
        peso_neto = get_peso_neto(articulo)
        sql_movserie = SQL_SERIE % (database,
                                    CODEMPRESA, codigo_articulo,
                                    numero_serie_lc, fecha, origen_documento,
                                    ejercicio, serie, documento,
                                    mov_posicion_origen, codigo_talla,
                                    codigo_almacen, ubicacion, partida,
                                    unidad_medida1, comentario, id_proceso_IME,
                                    # articulo.peso, articulo.peso_sin,
                                    peso_bruto, peso_neto,
                                    0.0,  # Metros cuadrados. Decimal NOT NULL
                                    ""   # Código palé. Varchar NOT NULL
                                    )  # pylint: disable=bad-continuation
        if simulate:
            res.append(sql_movserie)
        else:
            c.run_sql(sql_movserie)
            # pylint: disable=redefined-variable-type
            if procesar:
                res = fire(id_proceso_IME)
            else:   # No proceso la importación. Todo ha ido bien hasta ahora.
                    # Devuelvo el guid, que me vale como True también.
                res = id_proceso_IME
    return res


def esta_consumido(articulo, parte_de_produccion=None):
    """
    Devuelve la fecha de consumo si el artículo se ha consumido. None en
    otro caso.
    Los valores a mirar si se ha consumido son la serie, origen documento y
    comentario del último registro de MovimientoArticuloSerie y deberían
    ser, si es un consumo: FAB, 11 y "Consumo (bala|bigbag) ginn.*".
    Si `parte_de_produccion` es algo distinto de None, comprueba que se haya
    consumido en ese parte de producción. Se puede saber porque en el
    movimiento de Murano se guarda el ID del parte de producción.
    """
    # pylint: disable=no-value-for-parameter,no-member
    conn = Connection()
    movserie = get_ultimo_movimiento_articulo_serie(conn, articulo)
    # HARDCODED
    if (movserie
            and movserie['SerieDocumento'] == 'FAB'
            and movserie['OrigenDocumento'] == SALIDA
            and movserie['Comentario'].startswith('Consumo')):
        res = movserie['Fecha']
        if parte_de_produccion:
            res = (res and
                   str(parte_de_produccion.id) == str(movserie['Documento']))
    else:
        res = None
    return res


def esta_vendido(articulo):
    """
    Devuelve la fecha de venta si el artículo se ha vendido. None en
    otro caso.
    Los valores a mirar si se ha vendido son la serie, origen documento y
    comentario del último registro de MovimientoArticuloSerie y deberían
    ser, si es un consumo: FAB, 11 y "Consumo (bala|bigbag) ginn.*".
    """
    # pylint: disable=no-value-for-parameter,no-member
    conn = Connection()
    movserie = get_ultimo_movimiento_articulo_serie(conn, articulo)
    # HARDCODED
    if movserie and movserie['OrigenDocumento'] == VENTA:
        res = movserie['Fecha']
    else:
        res = None
    return res


def get_fecha_entrada(articulo, campo="FechaRegistro"):
    """
    Devuelve la fecha en que el artículo se dio de alta en Murano.
    Acepta también un código de artículo directamente en lugar de un artículo
    de ginn.
    Si el artículo no se encuentra, devuelve None.
    Permite obtener la fecha, fecha de registro o serie del alta especificando
    el campo en la llamada a la función. Por defecto devuelve la fecha de
    registro, que no tiene por qué coincidir con la fecha indicada para el
    alta.
    """
    assert campo in ("Fecha", "FechaRegistro", "SerieDocumento"), "Solo se"\
        " admiten Fecha, FechaRegistro o SerieDocumento como campo a "\
        "obtener."
    if isinstance(articulo, pclases.Articulo):
        codigo = articulo.codigo
    else:
        codigo = articulo
    # pylint: disable=no-value-for-parameter,no-member
    conn = Connection()
    sql = """SELECT Fecha, FechaRegistro, SerieDocumento
               FROM {}.dbo.MovimientoArticuloSerie
              WHERE NumeroSerieLc = '{}'
                AND CodigoEmpresa = {}
                AND OrigenDocumento = 2
                AND (SerieDocumento = 'FAB' OR SerieDocumento = 'API')
                AND CodigoAlmacen = 'GTX';""".format(conn.get_database(),
                                                     codigo,
                                                     CODEMPRESA)
    try:
        res = conn.run_sql(sql)[0][campo]
    except IndexError:
        res = None
    return res


# pylint: disable=too-many-arguments,too-many-statements
def consume_bala(bala, cantidad=-1, producto=None, guid_proceso=None,
                 simulate=False, procesar=True, fecha=None):
    """
    Crea un movimiento de salida de una bala en las tablas temporales de
    Murano.
    Recibe un objeto bala de ginn.
    `cantidad` es un parámetro obsoleto que no se usa.
    Si simulate es True, devuelve las dos consultas SQL generadas. En otro
    caso, el valor de ejecutar el proceso de importación.
    Si procesar es False no lanza el proceso de importación a través de la
    DDL OEM de Murano.
    Si la bala ya estaba consumida, no se puede volver a consumir, de modo que
    devuelve False también.
    """
    try:
        articulo = bala.articulo
    except AttributeError:  # Me han pasado directamente un artículo
        articulo = bala
    if not existe_articulo(articulo):
        logging.warning("La bala %s no existe en Murano. Se ignora.",
                        bala.codigo)
        res = False
    elif esta_en_almacen(articulo) is False:
        logging.warning("La bala %s no está en almacén en Murano. Se ignora.",
                        bala.codigo)
        res = False
    else:
        try:
            partida = bala.lote.codigo
        except AttributeError:
            partida = ""  # Balas C no tienen lote. No pasa nada. Murano traga.
        unidad_medida = "KG"
        comentario = "Consumo bala [ginn] {}".format(bala.get_info())[:40]
        serie = 'FAB'
        ubicacion = "Almac. de fibra."[:15]
        numero_serie_lc = ""
        # Sage me indica que no informe de la serie en el movimiento de stock
        # para solucionar lo del registro duplicado creado por Murano.
        (c, database, ejercicio, periodo, fecha, documento, codigo_articulo,
         codigo_almacen, grupo_talla, codigo_talla, tipo_movimiento,
         unidades, precio, importe, unidades2, unidad_medida2,
         factor_conversion, origen_movimiento) = prepare_params_movstock(
            articulo, cantidad, producto,
            fecha=fecha)   # pylint: disable=bad-continuation
        try:
            documento = bala.partidaCarga.numpartida  # No código. Solo números
        except AttributeError:
            pass    # Dejo la fecha, que es valor por defecto que trae.
        if not guid_proceso:
            id_proceso_IME = crear_proceso_IME(c)
        else:
            id_proceso_IME = guid_proceso
        guid_movposicion = generar_guid(c)
        canal_div = "CONSFIB"[:10]
        sql_movstock = SQL_STOCK % (database,
                                    CODEMPRESA, ejercicio, periodo, fecha,
                                    serie,
                                    documento, codigo_articulo, codigo_almacen,
                                    partida, grupo_talla, codigo_talla,
                                    tipo_movimiento, unidades, unidad_medida,
                                    precio, importe, unidades2, unidad_medida2,
                                    factor_conversion, comentario, canal_div,
                                    ubicacion, origen_movimiento,
                                    numero_serie_lc, id_proceso_IME,
                                    guid_movposicion)
        if simulate:
            # pylint: disable=redefined-variable-type
            # Si es una simulación, devuelvo las consultas SQL y no un bool.
            res = [sql_movstock]
        else:
            c.run_sql(sql_movstock)
        if cantidad < 0:
            origen_documento = SALIDA
        else:
            origen_documento = FABRICACION
        # mov_posicion_origen = get_mov_posicion(c, numero_serie_lc)
        mov_posicion_origen = guid_movposicion
        # En el movimiento de serie la UnidadMedida1_ es la básica:ROLLO,BALA..
        unidad_medida1 = buscar_unidad_medida_basica(articulo.productoVenta,
                                                     articulo)
        numero_serie_lc = bala.codigo
        peso_bruto = get_peso_bruto(articulo)
        peso_neto = get_peso_neto(articulo)
        sql_movserie = SQL_SERIE % (database,
                                    CODEMPRESA, codigo_articulo,
                                    numero_serie_lc, fecha, origen_documento,
                                    ejercicio, serie, documento,
                                    mov_posicion_origen, codigo_talla,
                                    codigo_almacen, ubicacion, partida,
                                    unidad_medida1, comentario, id_proceso_IME,
                                    # articulo.peso, articulo.peso_sin,
                                    peso_bruto, peso_neto,
                                    0.0,  # Metros cuadrados. Decimal NOT NULL
                                    ""   # Código palé. Varchar NOT NULL
                                    )  # pylint: disable=bad-continuation
        if simulate:
            res.append(sql_movserie)
        else:
            c.run_sql(sql_movserie)
            # pylint: disable=redefined-variable-type
            if procesar:
                res = fire(id_proceso_IME)
            else:   # No proceso la importación. Todo ha ido bien hasta ahora.
                    # Devuelvo el guid, que me vale como True también.
                res = id_proceso_IME
    return res


def consume_partida_carga(partida_carga):
    """
    Consume la partida de carga completa y actualiza el valor `api`:
    - Si no se ha producido ningún error, lo pone a True.
    - Si se ha producido **algún** error, lo pone a False.
    """
    res = True
    if partida_carga:
        for bala in partida_carga.balas:
            res = ((bool(esta_consumido(bala.articulo)) or consume_bala(bala))
                   and res)
        partida_carga.api = res
        partida_carga.sync()
    return res


# pylint: disable=too-many-arguments,too-many-statements
def consume_bigbag(bigbag, cantidad=-1, producto=None, guid_proceso=None,
                   simulate=False, procesar=True, fecha=None, check_api=True):
    """
    Crea un movimiento de salida de un bigbag en las tablas temporales de
    Murano. Si ya estaba consumido en el mismo parte que se está intentando
    consumir de nuevo, no crea movimientos pero devuelve True para poder
    validar el parte correctamente.
    Recibe un objeto bigbag de ginn.
    `cantidad` es un parámetro obsoleto que no se usa.
    Si simulate es True, devuelve las dos consultas SQL generadas. En otro
    caso, el valor de ejecutar el proceso de importación.
    Si procesar es False no lanza el proceso de importación a través de la
    DDL OEM de Murano.
    """
    try:
        articulo = bigbag.articulo
    except AttributeError:  # Me han pasado directamente un artículo
        articulo = bigbag
    if not existe_articulo(articulo):
        logging.warning("El bigbag %s no existe en Murano. Se ignora.",
                        bigbag.codigo)
        res = False
    elif not esta_en_almacen(articulo):
        logging.warning("El bigbag %s no está en almacén en Murano."
                        " Se ignora.", bigbag.codigo)
        # Será True si estoy intentando consumir otra vez al validar de nuevo
        # un parte que se haya quedado a la mitad por lo que sea. Idempotente.
        res = esta_consumido(bigbag, bigbag.parteDeProduccion)
    else:
        try:
            partida = bigbag.loteCem.codigo
        except AttributeError:
            partida = ""  # Balas C no tienen lote. No pasa nada. Murano traga.
        unidad_medida = "KG"
        comentario = "Consumo bigbag [ginn] {}".format(bigbag.get_info())[:40]
        serie = 'FAB'
        ubicacion = "Almac. de fibra."[:15]
        numero_serie_lc = ""
        # Sage me indica que no informe de la serie en el movimiento de stock
        # para solucionar lo del registro duplicado creado por Murano.
        (c, database, ejercicio, periodo, fecha, documento, codigo_articulo,
         codigo_almacen, grupo_talla, codigo_talla, tipo_movimiento,
         unidades, precio, importe, unidades2, unidad_medida2,
         factor_conversion, origen_movimiento) = prepare_params_movstock(
            articulo, cantidad, producto,
            fecha=fecha)   # pylint: disable=bad-continuation
        try:
            documento = bigbag.parteDeProduccion.id  # Única forma
            # numérica de localizarlo.
        except AttributeError:
            pass    # Dejo la fecha, que es valor por defecto que trae.
        if not guid_proceso:
            id_proceso_IME = crear_proceso_IME(c)
        else:
            id_proceso_IME = guid_proceso
        guid_movposicion = generar_guid(c)
        canal_div = "CONSBB"[:10]
        sql_movstock = SQL_STOCK % (database,
                                    CODEMPRESA, ejercicio, periodo, fecha,
                                    serie,
                                    documento, codigo_articulo, codigo_almacen,
                                    partida, grupo_talla, codigo_talla,
                                    tipo_movimiento, unidades, unidad_medida,
                                    precio, importe, unidades2, unidad_medida2,
                                    factor_conversion, comentario, canal_div,
                                    ubicacion, origen_movimiento,
                                    numero_serie_lc, id_proceso_IME,
                                    guid_movposicion)
        if simulate:
            # pylint: disable=redefined-variable-type
            # Si es una simulación, devuelvo las consultas SQL y no un bool.
            res = [sql_movstock]
        else:
            c.run_sql(sql_movstock)
        if cantidad < 0:
            origen_documento = SALIDA
        else:
            origen_documento = FABRICACION
        # mov_posicion_origen = get_mov_posicion(c, numero_serie_lc)
        mov_posicion_origen = guid_movposicion
        # En el movimiento de serie la UnidadMedida1_ es la básica:ROLLO,BALA..
        unidad_medida1 = buscar_unidad_medida_basica(articulo.productoVenta,
                                                     articulo)
        numero_serie_lc = bigbag.codigo
        peso_bruto = get_peso_bruto(articulo)
        peso_neto = get_peso_neto(articulo)
        sql_movserie = SQL_SERIE % (database,
                                    CODEMPRESA, codigo_articulo,
                                    numero_serie_lc, fecha, origen_documento,
                                    ejercicio, serie, documento,
                                    mov_posicion_origen, codigo_talla,
                                    codigo_almacen, ubicacion, partida,
                                    unidad_medida1, comentario, id_proceso_IME,
                                    # articulo.peso, articulo.peso_sin,
                                    peso_bruto, peso_neto,
                                    0.0,  # Metros cuadrados. Decimal NOT NULL
                                    ""   # Código palé. Varchar NOT NULL
                                    )  # pylint: disable=bad-continuation
        if simulate:
            res.append(sql_movserie)
        else:
            c.run_sql(sql_movserie)
            # pylint: disable=redefined-variable-type
            if procesar:
                res = fire(id_proceso_IME)
                # Solo actualizo el valor del api si no se ha simulado y estoy
                # seguro de que en Murano se ha descontado el bigbag. Prefiero
                # intentar volver a consumir el mismo bigbag que creer que se
                # ha consumido y no volverlo a intentar jamás dejando un
                # descuadre entre ginn y Murano.
                if check_api:
                    # ¿Se ha consumido pero no tiene el valor `api` bien?
                    res = esta_consumido(bigbag.articulo,
                                         bigbag.parteDeProduccion)
                bigbag.api = res
                bigbag.syncUpdate()
                # bigbag.sync()
            else:   # No proceso la importación. Todo ha ido bien hasta ahora.
                # Devuelvo el guid, que me vale como True también.
                res = id_proceso_IME
    return res


def create_bigbag(bigbag, cantidad=1, producto=None, guid_proceso=None,
                  simulate=False, procesar=True, codigo_almacen=None,
                  calidad=None, comentario=None, serie='API', fecha=None):
    """
    Crea un bigbag en Murano a partir de la información del bigbag en ginn.
    Si cantidad = -1 realiza un decremento en el almacén de Murano.
    Si no se especifica comentario, se usa uno por defecto.
    """
    articulo = bigbag.articulo
    if cantidad > 0 and duplica_articulo(articulo):
        logging.warning("El bigbag %s ya existe en Murano. Se ignora.",
                        articulo.codigo)
    else:
        partida = bigbag.loteCem.codigo
        # Si comentario es "", viene de fabricación. Serie FAB.
        if not comentario:
            comentario = "[ginn] {}".format(bigbag.get_info())
            serie = 'FAB'
        comentario = comentario[:40]    # Por restricciones de Murano.
        numero_serie_lc = ""
        # Sage me indica que no informe de la serie en el movimiento de stock
        # para solucionar lo del registro duplicado creado por Murano.
        ubicacion = "Almac. de fibra."[:15]
        unidad_medida = "KG"
        # pylint: disable=bad-continuation
        (c, database, ejercicio, periodo, fecha, documento, codigo_articulo,
         codigo_almacen, grupo_talla, codigo_talla, tipo_movimiento,
         unidades, precio, importe, unidades2, unidad_medida2,
         factor_conversion, origen_movimiento) = prepare_params_movstock(
            articulo, cantidad, producto, codigo_almacen, calidad, fecha=fecha)
        if not guid_proceso:
            id_proceso_IME = crear_proceso_IME(c)
        else:
            id_proceso_IME = guid_proceso
        guid_movposicion = generar_guid(c)
        canal_div = ''
        sql_movstock = SQL_STOCK % (database,
                                    CODEMPRESA, ejercicio, periodo, fecha,
                                    serie,
                                    documento, codigo_articulo, codigo_almacen,
                                    partida, grupo_talla, codigo_talla,
                                    tipo_movimiento, unidades, unidad_medida,
                                    precio, importe, unidades2, unidad_medida2,
                                    factor_conversion, comentario, canal_div,
                                    ubicacion, origen_movimiento,
                                    numero_serie_lc, id_proceso_IME,
                                    guid_movposicion)
        if simulate:
            res = [sql_movstock]
        else:
            c.run_sql(sql_movstock)
        if cantidad < 0:
            origen_documento = SALIDA
        else:
            origen_documento = FABRICACION
        # mov_posicion_origen = get_mov_posicion(c, numero_serie_lc)
        mov_posicion_origen = guid_movposicion
        # En movimiento de serie la UnidadMedida1_ es la básica: ROLLO, BALA...
        unidad_medida1 = buscar_unidad_medida_basica(articulo.productoVenta,
                                                     articulo)
        numero_serie_lc = bigbag.codigo
        peso_bruto = get_peso_bruto(articulo)
        peso_neto = get_peso_neto(articulo)
        sql_movserie = SQL_SERIE % (database,
                                    CODEMPRESA, codigo_articulo,
                                    numero_serie_lc, fecha, origen_documento,
                                    ejercicio, serie, documento,
                                    mov_posicion_origen, codigo_talla,
                                    codigo_almacen, ubicacion, partida,
                                    unidad_medida1, comentario, id_proceso_IME,
                                    # articulo.peso, articulo.peso_sin,
                                    peso_bruto, peso_neto,
                                    0.0,  # Metros cuadrados. Decimal NOT NULL
                                    ""   # Código palé. Varchar NOT NULL
                                    )  # pylint: disable=bad-continuation
        if simulate:
            res.append(sql_movserie)
        else:
            c.run_sql(sql_movserie)
            # pylint: disable=redefined-variable-type
            if procesar:
                res = fire(id_proceso_IME)
            else:   # No proceso la importación. Todo ha ido bien hasta ahora.
                    # Devuelvo el guid, que me vale como True también.
                res = id_proceso_IME
        return res


def create_rollo(rollo, cantidad=1, producto=None, guid_proceso=None,
                 simulate=False, procesar=True, codigo_almacen=None,
                 calidad=None, comentario=None, serie='API', fecha=None):
    """
    Crea un rollo en Murano a partir de la información del rollo en ginn.
    Si cantidad = -1 realiza un decremento en el almacén de Murano.
    Si no se especifica comentario, se usa uno por defecto.
    """
    articulo = rollo.articulo
    if cantidad > 0 and duplica_articulo(articulo):
        logging.warning("El rollo %s ya existe en Murano. Se ignora.",
                        articulo.codigo)
    else:
        try:
            partida = rollo.partida.codigo
        except AttributeError:
            partida = ""   # DONE: Los rollos C no tienen partida. No pasa nada
        # Si comentario es "", viene de fabricación. Serie FAB.
        if not comentario:
            comentario = "[ginn] {}".format(rollo.get_info())
            serie = 'FAB'
        comentario = comentario[:40]    # Por restricciones de Murano.
        numero_serie_lc = ""
        # Sage me indica que no informe de la serie en el movimiento de stock
        # para solucionar lo del registro duplicado creado por Murano.
        ubicacion = "Almac. de geotextiles."[:15]
        if articulo.get_str_calidad() == "C":
            # Los productos C se almacenan y venden en kg. No tienen largo y
            # ancho medible.
            unidad_medida = "KG"
        else:
            unidad_medida = "M2"
        # pylint: disable=bad-continuation
        (c, database, ejercicio, periodo, fecha, documento, codigo_articulo,
         codigo_almacen, grupo_talla, codigo_talla, tipo_movimiento,
         unidades, precio, importe, unidades2, unidad_medida2,
         factor_conversion, origen_movimiento) = prepare_params_movstock(
            articulo, cantidad, producto, codigo_almacen, calidad, fecha=fecha)
        if not guid_proceso:
            id_proceso_IME = crear_proceso_IME(c)
        else:
            id_proceso_IME = guid_proceso
        guid_movposicion = generar_guid(c)
        canal_div = ''
        sql_movstock = SQL_STOCK % (database,
                                    CODEMPRESA, ejercicio, periodo, fecha,
                                    serie,
                                    documento, codigo_articulo, codigo_almacen,
                                    partida, grupo_talla, codigo_talla,
                                    tipo_movimiento, unidades, unidad_medida,
                                    precio, importe, unidades2, unidad_medida2,
                                    factor_conversion, comentario, canal_div,
                                    ubicacion, origen_movimiento,
                                    numero_serie_lc, id_proceso_IME,
                                    guid_movposicion)
        if simulate:
            res = [sql_movstock]
        else:
            c.run_sql(sql_movstock)
        if cantidad < 0:
            origen_documento = SALIDA
        else:
            origen_documento = FABRICACION
        # mov_posicion_origen = get_mov_posicion(c, numero_serie_lc)
        mov_posicion_origen = guid_movposicion
        # En movimiento de serie la UnidadMedida1_ es la básica: ROLLO, BALA...
        unidad_medida1 = buscar_unidad_medida_basica(articulo.productoVenta,
                                                     articulo)
        superficie = get_superficie(articulo) or 0
        numero_serie_lc = rollo.codigo
        peso_bruto = get_peso_bruto(articulo)
        peso_neto = get_peso_neto(articulo)
        sql_movserie = SQL_SERIE % (database,
                                    CODEMPRESA, codigo_articulo,
                                    numero_serie_lc, fecha, origen_documento,
                                    ejercicio, serie, documento,
                                    mov_posicion_origen, codigo_talla,
                                    codigo_almacen, ubicacion, partida,
                                    unidad_medida1, comentario, id_proceso_IME,
                                    # articulo.peso, articulo.peso_sin,
                                    peso_bruto, peso_neto, superficie,
                                    # Metros cuadrados. Decimal NOT NULL
                                    ""   # Código palé. Varchar NOT NULL
                                    )  # pylint: disable=bad-continuation
        if simulate:
            res.append(sql_movserie)
        else:
            c.run_sql(sql_movserie)
            # pylint: disable=redefined-variable-type
            if procesar:
                res = fire(id_proceso_IME)
            else:   # No proceso la importación. Todo ha ido bien hasta ahora.
                    # Devuelvo el guid, que me vale como True también.
                res = id_proceso_IME
        return res


def create_caja(caja, cantidad=1, producto=None, guid_proceso=None,
                simulate=False, procesar=True, codigo_almacen=None,
                calidad=None, comentario=None, serie='API', fecha=None):
    """
    Crea una caja en Murano a partir de la información del objeto caja en ginn.
    Si cantidad es 1, realiza un decremento.
    Si no se especifica comentario, se usa uno por defecto.
    """
    articulo = caja.articulo
    if cantidad > 0 and duplica_articulo(articulo):
        logging.warning("La caja %s ya existe en Murano. Se ignora.",
                        articulo.codigo)
    else:
        partida = caja.partidaCem.codigo
        unidad_medida = "KG"
        # Si comentario es "", viene de fabricación. Serie FAB.
        if not comentario:
            comentario = "[ginn] {}".format(caja.get_info())
            serie = 'FAB'
        comentario = comentario[:40]    # Por restricciones de Murano.
        ubicacion = "Almac. de fibra embolsada."[:15]
        numero_serie_lc = ""
        # Sage me indica que no informe de la serie en el movimiento de stock
        # para solucionar lo del registro duplicado creado por Murano.
        # pylint: disable=bad-continuation
        (c, database, ejercicio, periodo, fecha, documento, codigo_articulo,
         codigo_almacen, grupo_talla, codigo_talla, tipo_movimiento,
         unidades, precio, importe, unidades2, unidad_medida2,
         factor_conversion, origen_movimiento) = prepare_params_movstock(
            articulo, cantidad, producto, codigo_almacen, calidad, fecha=fecha)
        if not guid_proceso:
            id_proceso_IME = crear_proceso_IME(c)
        else:
            id_proceso_IME = guid_proceso
        guid_movposicion = generar_guid(c)
        canal_div = ''
        sql_movstock = SQL_STOCK % (database,
                                    CODEMPRESA, ejercicio, periodo, fecha,
                                    serie,
                                    documento, codigo_articulo, codigo_almacen,
                                    partida, grupo_talla, codigo_talla,
                                    tipo_movimiento, unidades, unidad_medida,
                                    precio, importe, unidades2, unidad_medida2,
                                    factor_conversion, comentario, canal_div,
                                    ubicacion, origen_movimiento,
                                    numero_serie_lc, id_proceso_IME,
                                    guid_movposicion)
        if simulate:
            res = [sql_movstock]
        else:
            c.run_sql(sql_movstock)
        if cantidad < 0:
            origen_documento = SALIDA
        else:
            origen_documento = FABRICACION
        # mov_posicion_origen = get_mov_posicion(c, numero_serie_lc)
        mov_posicion_origen = guid_movposicion
        # En movimiento de serie la UnidadMedida1_ es la básica: ROLLO, BALA...
        unidad_medida1 = buscar_unidad_medida_basica(articulo.productoVenta,
                                                     articulo)
        numero_serie_lc = caja.codigo
        peso_bruto = get_peso_bruto(articulo)
        peso_neto = get_peso_neto(articulo)
        sql_movserie = SQL_SERIE % (database,
                                    CODEMPRESA, codigo_articulo,
                                    numero_serie_lc, fecha, origen_documento,
                                    ejercicio, serie, documento,
                                    mov_posicion_origen, codigo_talla,
                                    codigo_almacen, ubicacion, partida,
                                    unidad_medida1, comentario, id_proceso_IME,
                                    # articulo.peso, articulo.peso_sin,
                                    peso_bruto, peso_neto,
                                    0.0,   # Metros cuadrados. Decimal NOT NULL
                                    caja.pale and caja.pale.codigo or ""
                                    # Código palé. Varchar NOT NULL
                                    )  # pylint: disable=bad-continuation
        if simulate:
            res.append(sql_movserie)
        else:
            c.run_sql(sql_movserie)
            # pylint: disable=redefined-variable-type
            if procesar:
                res = fire(id_proceso_IME)
            else:   # No proceso la importación. Todo ha ido bien hasta ahora.
                    # Devuelvo el guid, que me vale como True también.
                res = id_proceso_IME
        return res


# pylint: disable=too-many-arguments
def create_pale(pale, cantidad=1, producto=None, guid_proceso=None,
                simulate=False, procesar=True, observaciones=None,
                serie="API", check_api=True):
    """
    Crea un palé con todas sus cajas en Murano a partir del palé de ginn.

    Si cantidad es -1 saca el palé del almacén.

    Si `check_api` es True comprueba que el valor del campo api es correcto: si
    las cajas del palé ya existen en Murano con el mismo producto pero el valor
    de api para el artículo es False (por algún fallo anterior, por ejemplo),
    se cambia a True.
    """
    assert observaciones is not None, "murano.ops.create_pale::"\
        "Debe indicar el motivo en el parámetro «observaciones»."
    # Los palés se crean automáticamente al crear las cajas con el código de
    # palé informado. No hay que crear movimiento de stock ni de número de
    # serie para eso.
    # El palé no es más que un campo en las tablas de movimientos de stock, de
    # modo que no es necesario siquiera comprobar si existe. Lo que se
    # comprobarán serán sus cajas una a una para evitar duplicados.
    i = 0
    cajas = pale.cajas
    totcajas = len(cajas)
    if VERBOSE:
        # pylint: disable=import-error
        from lib.tqdm.tqdm import tqdm  # Barra de progreso modo texto.
        cajas = tqdm(cajas, total=totcajas, leave=False)
    for caja in cajas:
        i += 1
        if VERBOSE:
            cajas.set_description("Creando caja %s... (%d/%d)" % (
                caja.codigo, i, totcajas))
        # La primera caja instanaciará el IdProcesoIME y se lo iré pasando
        # a las demás cajas. No lanzo el fire de ninguna de ellas. Lo haré
        # cuando tenga el palé completo.
        guid_proceso = create_caja(caja,
                                   cantidad=cantidad,
                                   producto=producto,
                                   guid_proceso=guid_proceso,
                                   simulate=simulate,
                                   procesar=False,
                                   comentario=observaciones,
                                   serie=serie)
    # No es necesario. Cada caja lanza su proceso y el palé no crea
    # registros en la base de datos. No hay que lanzar ninún proceso adicional.
    if procesar:
        if guid_proceso:  # Si todas las cajas ya existían,guid_proceso es None
            res = fire(guid_proceso)
        else:   # Nada que insertar. Nada insertado. Resultado, False.
            res = False
    else:
        res = guid_proceso
    # if not res:     # No se han insertado todas las cajas del palé.
    if check_api:   # Puede que porque ya existan. Si es así, corrijo `api`
        # Compruebo y actualizo API de todos modos porque por algún motivo
        # que no tengo tiempo ahora de investigar, las cajas no se ponen
        # a True aunque se vuelquen bien a Murano. check_api es True por defec.
        for caja in cajas:
            articulo = caja.articulo
            articulo.api = existe_articulo(articulo)
            articulo.syncUpdate()
        # pale.api es propiedad. Será True si todas sus cajas son api=True.
        res = pale.api
    return res


def consulta_proveedor(nombre=None, cif=None):
    """
    Obtiene los datos de un proveedor buscando por nombre, cif o ambas cosas.
    Devuelve una lista de proveedores coincidentes en forma de diccionarios
    campo:valor para cada registro.
    """
    # pylint: disable=no-value-for-parameter,no-member
    c = Connection()
    sql = "SELECT * FROM %s.dbo.Proveedores WHERE " % (c.get_database())
    where = []
    if nombre:
        where.append("Nombre = '%s'" % nombre)
    if cif:
        where.append("CifDni = '%s'" % cif)
    if nombre and cif:
        where = " AND ".join(where)  # py lint: disable=redefined-variable-type
    else:
        where = where[0]
    where += ";"
    sql += where
    res = c.run_sql(sql)
    return res


def consulta_cliente(nombre=None, cif=None):
    """
    Obtiene los datos de un cliente buscando por nombre, cif o ambas cosas.
    Devuelve una lista de clientes coincidentes.
    """
    # pylint: disable=no-value-for-parameter,no-member
    c = Connection()
    sql = "SELECT * FROM %s.dbo.Clientes WHERE " % (c.get_database())
    where = []
    if nombre:
        where.append("Nombre = '%s'" % nombre)
    if cif:
        where.append("CifDni = '%s'" % cif)
    if nombre and cif:
        where = " AND ".join(where)  # pylint: disable=redefined-variable-type
    else:
        where = where[0]
    where += ";"
    sql += where
    res = c.run_sql(sql)
    return res


def consultar_producto(producto=None, nombre=None, ean=None):
    """
    Busca un producto por nombre, si se especifica el parámetro.
    Si no, y lo que recibe es el código EAN, busca por ese código.
    En otro caso, busca por el código `[PC|PV]id`. Se debe recibir el objeto
    producto de pclases.
    Devuelve una lista de productos coincidentes.
    """
    assert not producto == nombre == ean == None    # NOQA
    # pylint: disable=no-value-for-parameter,no-member
    c = Connection()
    if nombre:
        try:
            sql = "SELECT * FROM {}.dbo.Articulos WHERE ".format(
                c.get_database())
            where = r"DescripcionArticulo = '{}'".format(nombre)
            where += r" AND CodigoEmpresa = '{}';".format(CODEMPRESA)
            sql += where
            res = c.run_sql(sql)
            # Busco por descripción, y si no lo encuentro, busco por la
            # descripción ampliada. Por eso hago esta asignación:
            # pylint: disable=unused-variable
            record = res[0]     # NOQA
        except IndexError:
            sql = "SELECT * FROM %s.dbo.Articulos WHERE ".format(
                c.get_database())
            where = r"Descripcion2Articulo = '{}'".format(nombre)
            where += r" AND CodigoEmpresa = '{}';".format(CODEMPRESA)
            sql += where
            res = c.run_sql(sql)
        except TypeError:   # res es None. Error con la base de datos
            if DEBUG:
                res = []    # pylint: disable=redefined-variable-type
    elif ean:   # Busco por código EAN (CodigoAlternativo)
        sql = "SELECT * FROM %s.dbo.Articulos WHERE " % (c.get_database())
        where = r"CodigoAlternativo = '%s'" % (ean)
        where += r" AND CodigoEmpresa = '{}';".format(CODEMPRESA)
        sql += where
        res = c.run_sql(sql)
    else:   # Busco por el código de Murano: PC|PV + ID
        idmurano = get_codigo_articulo_murano(producto)
        sql = "SELECT * FROM %s.dbo.Articulos WHERE " % (c.get_database())
        where = r"CodigoArticulo = '%s'" % (idmurano)
        where += r" AND CodigoEmpresa = '{}';".format(CODEMPRESA)
        sql += where
        res = c.run_sql(sql)
    if DEBUG:
        try:
            assert len(res) == 1
        except AssertionError:
            if not res or len(res) == 0:
                raise AssertionError("No se encontraron registros.")
            elif len(res) > 1:
                raise AssertionError("Se encontró más de un artículo:\n %s" % (
                    "\n".join([str(i) for i in res])))
    return res


# pylint: disable=unused-argument
def update_calidad(articulo, calidad, comentario=None, serie="API",
                   force=False, fecha=None):
    """
    Cambia la calidad del artículo en Murano a la recibida. Debe ser A, B o C.

    Si el cambio es a calidad C hay casos donde se requiere un cambio de
    producto además de calidad. En ese caso solo se permite si el parámetro
    `force` es True.
    """
    if calidad not in "aAbBcC":
        raise ValueError("El parámetro calidad debe ser A, B o C.")
    # DONE: [Marcos Sage] No modificamos tablas. Hacemos salida del producto A
    # y volvemos a insertarlo como C. En ese caso no importa que se repita el
    # código para el mismo producto porque antes hemos hecho la salida.
    if calidad in "Cc" and not force:
        # TODO: Ojo porque si cambio a calidad C probablemente implique un
        # cambio de producto.
        raise NotImplementedError("Función no disponible por el momento.")
    else:
        if not comentario:
            observaciones_baja = "Baja por cambio a calidad {}".format(calidad)
        else:
            observaciones_baja = comentario
        res = delete_articulo(articulo,
                              observaciones=observaciones_baja,
                              serie=serie, fecha=fecha)
        if res:
            if not comentario:
                observaciones_alta = "Alta por cambio a calidad {}.".format(
                        calidad)
            else:
                observaciones_alta = comentario
            res = create_articulo(articulo, calidad=calidad,
                                  observaciones=observaciones_alta,
                                  serie=serie, fecha=fecha)
    return res


def update_peso(articulo, peso_real):
    """
    Recibe un artículo **ya** volcado a Murano y actualiza el peso en Murano
    y en ginn.
    0. Elimina el artículo de Murano.
    1. Desmarca el artículo como volcado en ginn.
    2. Actualiza el peso bruto, neto y real en ginn teniendo en cuenta peso de
       embalaje y demás.
    3. Vuelca el artículo de nuevo a Murano.
    4. Se comprueba el campo `api` respecto al resultado del volcado.
    """
    serie = 'API'
    peso_anterior = articulo.peso_real
    observaciones = 'Cambio de peso de {} a {}.'.format(peso_anterior,
                                                        peso_real)
    res = delete_articulo(articulo, observaciones=observaciones, serie=serie)
    if res:
        articulo.api = False
        articulo.set_peso_real(peso_real)
        articulo.api = create_articulo(articulo, observaciones=observaciones,
                                       serie=serie)
        articulo.sync()
        res = articulo.api
    return res


def duplica_articulo(articulo, producto=None):
    """
    Devuelve True si al crear el artículo recibido con el producto indicado
    (o el que tenga asignado el artículo, si es None) crearía un duplicado.
    Es decir, si el artículo no existía en Murano (no tiene registro de
    movimiento de serie), devuelve False (no lo duplicaría si lo creara).
    Si el artículo ya existe en Murano pero ha salido en un movimiento de
    borrado desde fabricación --y no por albarán-- entonces tampoco lo
    duplicaría, devuelve False. Si el movimiento es de ajuste manual
    de salida, tampoco lo duplicaría.
    True en el resto de los casos (existe y el último movimiento es de
    albarán o de entrada de fabricación).
    Si tiene un movimiento de entrada de fabricación pero con otro producto,
    **sí** que duplicaría el código (que es lo que comprueba existe_articulo).
    """
    if not isinstance(articulo, pclases.Articulo):
        # Por error o por pruebas he recibido directamente el código del
        # artículo.
        articulo = pclases.Articulo.get_articulo(articulo)
    if not producto:
        producto = articulo.productoVenta
    # pylint: disable=no-value-for-parameter,no-member
    conn = Connection()
    movserie = get_ultimo_movimiento_articulo_serie(conn, articulo)
    if (not movserie or
            es_movimiento_salida_fabricacion(movserie) or
            es_movimiento_ajuste_api(movserie) or
            es_movimiento_salida_manual(movserie)):
        res = False
    else:
        res = True
    return res


def existe_articulo(articulo, productoVenta=None):
    """
    Devuelve True si el artículo ya existe en Murano **Y** es del producto
    recibido. Si ni se recibe producto, se mira si existe con el producto del
    propio artículo según ginn.
    Se permite especificar producto para el caso del cambio de
    producto, donde no me interesa si el artículo existe, sino que si existe
    con el producto de destino para no duplicarlo.
    Se considera que si un artículo ha salido del almacén, sigue existiendo
    en Murano. Esto evita que se dupliquen códigos y se respete la
    trazabilidad.
    Recibe un objeto artículo de ginn.
    """
    if not isinstance(articulo, pclases.Articulo):
        # Por error o por pruebas he recibido directamente el código del
        # artículo.
        articulo = pclases.Articulo.get_articulo(articulo)
    if not productoVenta:
        productoVenta = articulo.productoVenta
    # pylint: disable=no-value-for-parameter,no-member
    c = Connection()
    movserie = get_ultimo_movimiento_articulo_serie(c, articulo)
    if not movserie:
        res = False
    else:
        codigo_producto_venta_actual = movserie['CodigoArticulo']
        codigo_producto_venta_preguntado = get_codigo_articulo_murano(
            productoVenta)
        res = codigo_producto_venta_actual == codigo_producto_venta_preguntado
    return res


def esta_en_almacen(articulo):
    """
    Devuelve el código de almacén si el artículo está en algún almacén de
    Murano. Sea del producto que sea.
    False en caso contrario.
    """
    if not isinstance(articulo, pclases.Articulo):
        # Por error o por pruebas he recibido directamente el código del
        # artículo.
        articulo = pclases.Articulo.get_articulo(articulo)
    # pylint: disable=no-value-for-parameter,no-member
    c = Connection()
    # movserie = get_ultimo_movimiento_articulo_serie(c, articulo)
    # if not movserie:
    #     # Si no ha tenido movimientos de serie, nunca ha existido en Murano.
    #     res = False
    # else:
    #     if es_movimiento_de_salida(movserie):
    #         # Ha tenido movimientos, pero el último ha sido de salida.
    #         res = False
    #     else:
    #         res = True
    sql = """SELECT CodigoAlmacen
               FROM {}.dbo.ArticulosSeries
              WHERE CodigoEmpresa = {}
                AND UnidadesSerie > 0
                AND NumeroSerieLc = '{}'
           ORDER BY FechaInicial;""".format(c.get_database(), CODEMPRESA,
                                            articulo.codigo)
    articulos_serie = c.run_sql(sql)
    try:
        almacen = articulos_serie[-1]['CodigoAlmacen']
    except IndexError:
        almacen = None
    if not almacen:
        res = False
    else:
        res = almacen
    return res


def get_precio_coste(articulo):
    """
    Devuelve el precio de coste por kg según Murano del artículo de ginn
    recibido.
    Se supone que debe coincidir con el que estaba definido para su familia
    en el mes en que se dio de alta.
    Es diferente al buscar_precio_coste para Murano, que devuelve el mismo
    valor pero desde la tabla Familias directamente. Sin tener en cuenta
    la tabla de precios de coste por mes.
    """
    if not isinstance(articulo, pclases.Articulo):
        # Por error o por pruebas he recibido directamente el código del
        # artículo.
        articulo = pclases.Articulo.get_articulo(articulo)
    # pylint: disable=no-value-for-parameter,no-member
    conn = Connection()
    # Esto sería si en Sage lo hubiesen hecho bien. Pero la realidad es otra.
    # sql = """SELECT GEO_CosteUnidadEspecifica
    #            FROM {}.dbo.ArticulosSeries
    #           WHERE CodigoEmpresa = {}
    #             AND UnidadesSerie > 0
    #             AND NumeroSerieLc = '{}'
    #        ORDER BY FechaInicial;""".format(conn.get_database(), CODEMPRESA,
    #                                         articulo.codigo)
    # Solo se han acordado de actualizar los movimientos de stock. Así que
    # tenemos que dar un rodeo para conseguir el valor.
    # OJO: ¿El último es el que tiene el precio bien? ¿Y si es un movimiento
    # de salida de stock y va el precio que le hemos dado al cliente? Bueno,
    # entonces no estará en stock. Aparte, inexplicablemente, el JOIN siempre
    # devuelve un único movimiento FAB. Para la salida de albarán de
    # MovimientoArticuloSerie no hay MovimientoStock. Pero ojo con los borrados
    # y nuevas creaciones. Ahí sí habrá más de un MovimientoStock. **Yo me
    # quedo siempre con el más reciente.**
    sql = """SELECT Precio
               FROM {DB}.dbo.MovimientoArticuloSerie
               JOIN {DB}.dbo.MovimientoStock
                 ON {DB}.dbo.MovimientoArticuloSerie.MovPosicionOrigen
                    = {DB}.dbo.MovimientoStock.MovPosicion
              WHERE {DB}.dbo.MovimientoStock.CodigoEmpresa = {CE}
                AND {DB}.dbo.MovimientoArticuloSerie.NumeroSerieLc = '{cod}'
              ORDER BY {DB}.dbo.MovimientoStock.Fecha DESC;""".format(
                  DB=conn.get_database(),
                  CE=CODEMPRESA,
                  cod=articulo.codigo)
    # DONE: ¿Y los cambios de producto, qué? Bueno, pues lo mismo. El más
    # reciente es el último alta en la base de datos. El producto definitivo.
    articulos_serie = conn.run_sql(sql)
    try:
        precio_coste = articulos_serie[0]['Precio']
    except IndexError:
        precio_coste = None
    if not precio_coste:
        res = 0.0
    else:
        res = precio_coste
    return res

def es_movimiento_de_salida(movserie):
    """
    Recibe un registro MovimientoArticuloSerie de Murano (diccionario) y
    devuelve True si es un movimiento de salida.
    No tiene en cuenta si es un interalmacén (lo tomará como salida también).
    """
    res = (es_movimiento_salida_fabricacion(movserie) or
           es_movimiento_ajuste_api(movserie) or
           es_movimiento_salida_albaran(movserie))
    return res


def get_producto_articulo_murano(articulo):
    """
    Devuelve el pclases.ProductoVenta que tenga asignado el artículo en Murano.
    """
    # pylint: disable=no-value-for-parameter,no-member
    conn = Connection()
    movserie = get_ultimo_movimiento_articulo_serie(conn, articulo)
    if movserie:
        murano_id = movserie['CodigoArticulo']
        pv = get_producto_ginn(murano_id)
    else:   # Nunca ha entrado en Murano.
        pv = None
    return pv


def es_movimiento_salida_fabricacion(movserie):
    """
    True si el registro MovimientoArticuloSerie es de salida de fabricación
    (borrado en partes o consumo).
    OrigenDocumento es 2 para altas y 11 para bajas.
    """
    res = (movserie['OrigenDocumento'] == SALIDA and
           movserie['SerieDocumento'] == 'FAB')
    return res


def es_movimiento_ajuste_api(movserie):
    """
    True si el registro MovimientoArticuloSerie es de salida de fabricación
    (borrado en partes).
    """
    res = (movserie['OrigenDocumento'] == SALIDA and
           movserie['SerieDocumento'] == 'API')
    return res


def es_movimiento_salida_manual(movserie):
    """
    True si el registro MovimientoArticuloSerie es de salida por un ajuste
    manual por entrada/salida de movimientos de Murano.
    OJO: Esos movimientos los debe marcar el usuario como "MAN" en la Serie.
    """
    res = (movserie['OrigenDocumento'] == SALIDA and
           movserie['SerieDocumento'] == 'MAN')
    return res


def es_movimiento_entrada_manual(movserie):
    """
    True si el registro MovimientoArticuloSerie es de entrada por un ajuste
    manual por entrada/salida de movimientos de Murano.
    OJO: Esos movimientos los debe marcar el usuario como "MAN" en la Serie.
    """
    res = (movserie['OrigenDocumento'] == ENTRADA and
           movserie['SerieDocumento'] == 'MAN')
    return res


def es_movimiento_salida_albaran(movserie):
    """
    Devuelve el número de albarán (evaluable como True) por el que ha salido
    el artículo indicado en el registro MovimientoArticuloSerie.
    """
    if movserie['OrigenDocumento'] == VENTA:
        serie = movserie['SerieDocumento']
        documento = movserie['Documento']
        res = serie + str(documento)
    else:
        res = False
    return res


def iter_create_articulos(articulos, simulate=False, serie='API', fecha=None,
                          cantidad=1):
    """
    Crea en Murano **en un solo proceso de importación** los artículos de
    _ginn_ recibidos en una lista.
    Si `simulate` es True, no conecta con Murano. Solo simula la operación con
    éxito.
    Devuelve True si **todos** los artículos se volcaron.
    Funciona **COMO UN GENERADOR** para poder ser usado en parte_produccion_*
    con barras de progreso. Devuelve en cada paso el artículo insertado en la
    tabla temporal listo para procesar. En el último paso devuelve el
    `guid_proceso` o algo interpretable como booleano, que será False si
    *alguno* de los artículos no se pudo importar. El penúltimo es el
    guid_proceso **antes** de ejecutarse el `fire`, para poder notificar al
    usuario.
    """
    i = 0
    # OJO: cantidad=-1 no está probado.
    assert abs(cantidad) == 1, "Cantidad debe ser -1 o 1."
    # Cantidad fija para todos. Esto es solo para dar de alta
    # productos con trazabilidad más rápidamente.
    guid_proceso = None     # El primer GUID es nulo. Hay que crearlo con el
    # primero de los artículos a volcar.
    observaciones = ""  # Para que los comentarios del registro de Murano sean
    # automáticos y se fuerce la serie 'FAB'.
    procesar = True     # Se puede llegar a usar, como con los palés, para
    # encadenar varias importaciones en un mismo proceso de importación. De
    # momento no se permite y se procesa la importación completa.
    totarticulos = len(articulos)
    if VERBOSE:
        # pylint: disable=import-error
        from lib.tqdm.tqdm import tqdm  # Barra de progreso modo texto.
        articulos = tqdm(articulos, total=totarticulos, leave=False)
    for articulo in articulos:
        i += 1
        producto = articulo.productoVenta
        if VERBOSE:
            articulos.set_description("Creando articulo %s... (%d/%d)" % (
                articulo.codigo, i, totarticulos))
        # El primer articulo instanaciará el IdProcesoIME y se lo iré pasando
        # a los demás articulos. No lanzo el fire de ninguna de ellas. Lo haré
        # cuando tenga la estructura completa en la tmpIME montada.
        guid_proceso = create_articulo(articulo,
                                       cantidad=cantidad,
                                       producto=producto,
                                       guid_proceso=guid_proceso,
                                       simulate=simulate,
                                       procesar=False,
                                       codigo_almacen=None,     # Auto
                                       calidad=None,            # Auto
                                       observaciones=observaciones,
                                       serie=serie,
                                       fecha=fecha)
        yield articulo
    yield guid_proceso
    if procesar:
        if guid_proceso:  # Si todos ya existían, guid_proceso es None.
            res = fire(guid_proceso)
        else:   # Nada que insertar. Nada insertado. Resultado, False.
            res = False
    else:
        res = guid_proceso
    # Hasta que no finaliza no puedo comprobar si ha habido errores. Compruebo
    # los que se han volcado, les pongo el campo `.api` a True y devuelvo en
    # consecuencia.
    for articulo in articulos:
        articulo.api = existe_articulo(articulo)
        articulo.syncUpdate()
        # res = reduce(lambda i, l: i and l, articulos)
    todos_volcados = len([i for i in articulos if bool(i)]) == len(articulos)
    res = len(articulos) and todos_volcados and res
    yield res


def create_articulo(articulo, cantidad=1, producto=None, guid_proceso=None,
                    simulate=False, procesar=True, codigo_almacen=None,
                    calidad=None, observaciones=None, serie="API", fecha=None):
    """
    Crea un artículo nuevo en Murano con el producto recibido. Si no se
    recibe ninguno, se usa el que tenga asociado en ginn. Si se recibe un
    objeto producto, se ignora el actual del artículo, se reemplaza en ginn
    por el recibido y se da de alta así en Murano.
    Devuelve False si hubo errores y no se creó o True (o el GUID de proceso)
    en otro caso.
    Las observaciones van como «comentario» en los registros de mov. de Murano.
    Si las observaciones son "", se usa el comentario por defecto del
    create_bala, *_rollo, etc. Pero se fuerza al usuario (más bien al código
    de partes_de_fabricacion_*) a que especifiquen la cadena vacía.
    Si se `observaciones` es "" se usa la serie 'FAB' independientemente de
    lo que se haya indicado en `serie`.
    """
    assert observaciones is not None, "murano.ops.create_articulo::"\
        "Debe indicar el motivo en el parámetro «observaciones»."
    # TODO: ¿Y al descontar existencias? ¿Comprobar también que existan antes?
    # De todos modos el proceso de importación devolverá error si la serie
    # está duplicada.
    if cantidad < 0:
        delta = -1
    else:
        delta = 1
    assert articulo is not None, "Debe especificarse un artículo."
    res = False
    if delta < 0 or not duplica_articulo(articulo, producto):
        for i in range(abs(cantidad)):  # pylint: disable=unused-variable
            if articulo.es_bala():
                res = create_bala(articulo.bala, delta, producto,
                                  guid_proceso=guid_proceso,
                                  simulate=simulate,
                                  procesar=procesar,
                                  codigo_almacen=codigo_almacen,
                                  calidad=calidad,
                                  comentario=observaciones,
                                  serie=serie, fecha=fecha)
            elif articulo.es_balaCable():
                res = create_bala(articulo.balaCable, delta, producto,
                                  guid_proceso=guid_proceso,
                                  simulate=simulate,
                                  procesar=procesar,
                                  codigo_almacen=codigo_almacen,
                                  calidad=calidad,
                                  comentario=observaciones,
                                  serie=serie, fecha=fecha)
            elif articulo.es_bigbag():
                res = create_bigbag(articulo.bigbag, delta, producto,
                                    guid_proceso=guid_proceso,
                                    simulate=simulate,
                                    procesar=procesar,
                                    codigo_almacen=codigo_almacen,
                                    calidad=calidad,
                                    comentario=observaciones,
                                    serie=serie, fecha=fecha)
            elif articulo.es_caja():
                res = create_caja(articulo.caja, delta, producto,
                                  guid_proceso=guid_proceso,
                                  simulate=simulate,
                                  procesar=procesar,
                                  codigo_almacen=codigo_almacen,
                                  calidad=calidad,
                                  comentario=observaciones,
                                  serie=serie, fecha=fecha)
            elif articulo.es_rollo():
                res = create_rollo(articulo.rollo, delta, producto,
                                   guid_proceso=guid_proceso,
                                   simulate=simulate,
                                   procesar=procesar,
                                   codigo_almacen=codigo_almacen,
                                   calidad=calidad,
                                   comentario=observaciones,
                                   serie=serie, fecha=fecha)
            elif articulo.es_rollo_defectuoso():
                res = create_rollo(articulo.rolloDefectuoso, delta, producto,
                                   guid_proceso=guid_proceso,
                                   simulate=simulate,
                                   procesar=procesar,
                                   codigo_almacen=codigo_almacen,
                                   calidad=calidad,
                                   comentario=observaciones,
                                   serie=serie, fecha=fecha)
            elif articulo.es_rolloC():
                res = create_rollo(articulo.rolloC, delta, producto,
                                   guid_proceso=guid_proceso,
                                   simulate=simulate,
                                   procesar=procesar,
                                   codigo_almacen=codigo_almacen,
                                   calidad=calidad,
                                   comentario=observaciones,
                                   serie=serie, fecha=fecha)
            else:
                raise ValueError("El artículo %s no es bala, bala de cable, "
                                 "bigbag, caja, rollo ni rollo C."
                                 % (articulo.puid))
            if VERBOSE:
                print("ops::create_articulo --> {}.res = {} ({})".format(
                    articulo.puid, res, type(res)))
            articulo.api = bool(res)
            articulo.syncUpdate()
    else:
        logging.warning("El código %s ya existe en Murano. Se ignora.",
                        articulo.codigo)
    return res


def update_producto(articulo, producto, observaciones=None, serie="API",
                    fecha=None):
    """
    Cambia el artículo recibido al producto indicado.
    """
    res = delete_articulo(articulo, observaciones=observaciones, serie=serie)
    if res:
        res = create_articulo(articulo, producto=producto,
                              observaciones=observaciones,
                              serie=serie, fecha=fecha)
    return res


def update_stock(producto, delta, almacen, guid_proceso=None,
                 simulate=False, procesar=True):
    """
    Incrementa o decrementa el stock del producto en la cantidad recibida en
    en el parámetro «delta».
    El producto **no** debe tener trazabilidad. En otro caso deben usarse las
    funciones "crear_[bala|rollo...]".
    """
    assert isinstance(producto, pclases.ProductoCompra)
    partida = ""
    unidad_medida = ""  # producto.unidad
    comentario = ("Stock [ginn] %f (%s)" % (delta, producto.get_info()))[:40]
    serie = 'FAB'
    ubicacion = "Almacén general"[:15]
    numero_serie_lc = ""
    # pylint: disable=no-value-for-parameter,no-member
    c = Connection()
    database = c.get_database()
    today = datetime.datetime.today()
    ejercicio = today.year
    periodo = today.month
    fecha = today.strftime("%Y-%m-%d %H:%M:%S")
    documento = int(today.strftime("%Y%m%d"))
    codigo_articulo = buscar_codigo_producto(producto)
    if isinstance(almacen, pclases.Almacen):
        codigo_almacen = buscar_codigo_almacen(almacen)
    else:
        codigo_almacen = almacen    # He recibido un código directamente.
    codigo_talla = ""   # No hay calidades en los productos de compra.
    grupo_talla = 0  # No tratamiento de calidad en productos sin trazabilidad.
    if delta >= 0:
        tipo_movimiento = 1     # 1 = entrada, 2 = salida.
    else:
        delta = abs(delta)
        tipo_movimiento = 2
    unidades = delta    # En dimensión base del producto.
    # precio = producto.precioDefecto
    precio = buscar_precio_coste(producto, ejercicio, codigo_almacen)
    importe = unidades * precio
    factor_conversion = buscar_factor_conversion(producto)
    unidades2 = unidades * factor_conversion
    origen_movimiento = "F"  # E = Entrada de Stock (entrada directa),
    # F (fabricación), I (inventario),
    # M (rechazo fabricación), S (Salida stock)
    # P (apertura), B(albarán de compra), A(albarán de venta)
    if not guid_proceso:
        id_proceso_IME = crear_proceso_IME(c)
    else:
        id_proceso_IME = guid_proceso
    # En el movimiento de stock la unidad principal (unidad_medida) es la que
    # sea. En la segunda unidad (unidad_mediad2) mandamos "", que es lo que
    # me devolverá buscar_unidad_medida_basica para todo lo que no sea un
    # producto con código de trazabilidad.
    unidad_medida2 = buscar_unidad_medida_basica(producto)
    guid_movposicion = generar_guid(c)
    canal_div = ''
    sql_movstock = SQL_STOCK % (database,
                                CODEMPRESA, ejercicio, periodo, fecha,
                                serie,
                                documento, codigo_articulo, codigo_almacen,
                                partida, grupo_talla, codigo_talla,
                                tipo_movimiento, unidades, unidad_medida,
                                precio, importe, unidades2, unidad_medida2,
                                factor_conversion, comentario, canal_div,
                                ubicacion, origen_movimiento, numero_serie_lc,
                                id_proceso_IME, guid_movposicion)
    if simulate:
        res = [sql_movstock]
    else:
        c.run_sql(sql_movstock)
        # pylint: disable=redefined-variable-type
        if procesar:
            res = fire(id_proceso_IME, acumular_campos_personalizados=False)
        else:   # No proceso la importación. Todo ha ido bien hasta ahora.
                # Devuelvo el guid, que me vale como True también.
            res = id_proceso_IME
    return res


def delete_articulo(articulo, codigo_almacen=None, observaciones=None,
                    serie='API', fecha=None, guid_proceso=None,
                    simulate=False, procesar=True):
    """
    Elimina el artículo en Murano mediante la creación de un movimiento de
    stock negativo de ese código de producto.
    """
    # Buscamos el producto que tiene asignado ahora en Murano para darlo de
    # baja de ESE producto en concreto. Seguramente no sea el que tiene
    # asignado en ginn y fallará si intentamos crear el movimiento negativo
    # contra él.
    res = False
    # pylint: disable=no-value-for-parameter,no-member
    conn = Connection()
    movserie = get_ultimo_movimiento_articulo_serie(conn, articulo)
    if movserie:
        id_producto_anterior = movserie["CodigoArticulo"]
        producto_anterior = get_producto_ginn(id_producto_anterior)
        res = create_articulo(articulo, cantidad=-1,
                              producto=producto_anterior,
                              codigo_almacen=codigo_almacen,
                              observaciones=observaciones,
                              serie=serie, fecha=fecha,
                              guid_proceso=guid_proceso,
                              procesar=procesar,
                              simulate=simulate)
    else:
        logging.warning("El artículo %s no existe en Murano.", articulo.codigo)
    return res


def consumir(productoCompra, cantidad, almacen=None, consumo=None):
    """
    Decrementa las existencias del producto recibido en la cantidad indicada
    mediante registros de movimientos de stock en Murano en el almacén
    principal si no se indica otro como tercer parámetro; o en el almacén del
    silo correspondiente si almacen es None, el producto de compra es de
    granza y se especifica un consumo.
    """
    if not almacen:
        if not productoCompra.es_granza():
            almacen = pclases.Almacen.get_almacen_principal()
            # Los consumos de materia prima siempre se hacen desde el almacén
            # principal. EXCEPTO los de granza, que se hacen desde un silo que
            # se trata como almacén en Murano.
        else:
            try:
                almacen = consumo.silo
            except AttributeError:
                raise ValueError("Si no especifica un almacén debe indicar "
                                 "el consumo origen de ginn como referencia.")
    res = update_stock(productoCompra, -cantidad, almacen)
    if consumo:     # Si he recibido el consumo, actualizo el valor `api`.
        consumo.api = res
        consumo.sync()
    return res


def get_existencias_silo(silo):
    """
    Recibe un silo de ginn y devuelve un diccionario con los productos y sus
    existencias en el almacén correspondiente de Murano.
    Cada silo tiene un almacén en Murano.
    0. Se determina el almacén correspondiente en Murano al silo recibido.
    1. Se buscan los productos que hay en ese almacén y sus existencias.
    2. Se monta un diccionario con los productos de ginn correspondientes a
        los productos de Murano de ese almacén.
    3. Se almacena en el diccionario, para cada producto de ginn, las
        existencias consultadas anteriormente.
    4. Se devuelve ese diccionario.
    """
    res = {}
    # pylint: disable=no-value-for-parameter,no-member
    conn = Connection()
    rs_ejercicio = conn.run_sql("""SELECT MAX(Ejercicio) AS ejercicio
                                   FROM {}.dbo.AcumuladoStock
                                   WHERE CodigoEmpresa = {};
                                """.format(conn.get_database(),
                                           CODEMPRESA))
    try:
        ejercicio = rs_ejercicio[0]['ejercicio']
    except (IndexError, KeyError):
        ejercicio = datetime.date.today().year
    almacen = buscar_almacen_silo(silo)
    sql_silos = """SELECT AcumuladoStock.Ejercicio,
                          AcumuladoStock.CodigoEmpresa,
                          AcumuladoStock.CodigoAlmacen,
                          Articulos.CodigoFamilia,
                          Articulos.CodigoSubfamilia,
                          Familias.Descripcion,
                          Subfamilias.Descripcion AS Descripcion2,
                          AcumuladoStock.CodigoArticulo,
                          Articulos.DescripcionArticulo,
                          AcumuladoStock.CodigoTalla01_,
                          AcumuladoStock.Partida,
                          ArticulosSeries.NumeroSerieLc,
                          Articulos.UnidadMedida2_,
                          Articulos.UnidadMedidaAlternativa_,
                          AcumuladoStock.UnidadSaldo,
                          AcumuladoStock.UnidadSaldoTipo_,
                          Articulos.TipoEnvase_,
                          Articulos.PrecioCompra,
                          ArticulosSeries.GEO_CosteUnidadEspecifica,
                          ArticulosSeries.UnidadesSerie,
                          ArticulosSeries.PesoBruto_,
                          ArticulosSeries.PesoNeto_,
                          ArticulosSeries.MetrosCuadrados
        FROM AcumuladoStock
             INNER JOIN Articulos ON AcumuladoStock.CodigoEmpresa =
                Articulos.CodigoEmpresa
             AND AcumuladoStock.CodigoArticulo = Articulos.CodigoArticulo
             LEFT OUTER JOIN ArticulosSeries ON
                AcumuladoStock.Partida = ArticulosSeries.Partida AND
                AcumuladoStock.CodigoAlmacen = ArticulosSeries.CodigoAlmacen
                    AND
                AcumuladoStock.CodigoTalla01_ = ArticulosSeries.CodigoTalla01_
                    AND Articulos.CodigoEmpresa =
                        ArticulosSeries.CodigoEmpresa AND
                Articulos.CodigoArticulo = ArticulosSeries.CodigoArticulo
            LEFT OUTER JOIN Familias AS Subfamilias ON
                Articulos.CodigoFamilia = Subfamilias.CodigoFamilia AND
                Articulos.CodigoSubfamilia = Subfamilias.CodigoSubfamilia AND
                Articulos.CodigoEmpresa = Subfamilias.CodigoEmpresa
            LEFT OUTER JOIN Familias ON
                Articulos.CodigoFamilia = Familias.CodigoFamilia AND
                Articulos.CodigoEmpresa = Familias.CodigoEmpresa AND
                Familias.CodigoSubfamilia = '**********'
        WHERE AcumuladoStock.Periodo = 99
          AND AcumuladoStock.Ejercicio = %d
          AND AcumuladoStock.CodigoAlmacen = '%s'
          AND AcumuladoStock.CodigoEmpresa = '%s'
          AND AcumuladoStock.UnidadSaldo <> 0
        ORDER BY FechaUltimaEntrada DESC;""" % (
                  ejercicio, almacen, CODEMPRESA)
    res_murano = conn.run_sql(sql_silos)
    for registro in res_murano:
        codigo_producto = registro['CodigoArticulo']
        existencias = registro['UnidadSaldo']
        producto = get_producto_ginn(codigo_producto)
        res[producto] = float(existencias)
    return res


def get_ocupado_silo(silo):
    """
    Devuelve la cantidad total de existencias que hay en un silo, sea del
    producto que sea.
    """
    stock_murano = get_existencias_silo(silo)
    ocupado = sum([stock_murano[producto] for producto in stock_murano])
    return ocupado


def get_carga_mas_antigua_silo(silo):
    """
    Devuelve una estructura similar a las cargas de ginn pero con los datos
    de Murano. Ver pclases.Silo.get_carga_mas_antigua
    """
    CargaSilo = namedtuple('CargaSilo',
                           ['productoCompra', 'siloID', 'cantidad'])
    productos_cargados = get_existencias_silo(silo)
    cs = None
    for pc in productos_cargados:
        # Solo devolverá uno: el último. Las cargas están ordenadas por fecha
        # de carga de la más nueva a la más antigua.
        cs = CargaSilo(pc, silo.id, productos_cargados[pc])
    return cs


def get_producto_ginn(codigo_murano):
    """
    Devuelve el objeto producto de ginn (de compra o de venta) según el código
    recibido de Murano.
    """
    # FIXME: Implementar otra forma de que la relación sea biyectiva.
    # OJO: HARCODED. Si se crean nuevos productos, hay que tener cuidado de que
    # se respete esta codificación.
    if codigo_murano.startswith("PC"):
        clase = pclases.ProductoCompra
    elif codigo_murano.startswith("PV"):
        clase = pclases.ProductoVenta
    else:
        raise NotImplementedError("Solo se permite buscar por código PV|PC")
    idginn = int(codigo_murano.replace("PC", "").replace("PV", ""))
    res = clase.get(idginn)
    return res


def buscar_almacen_silo(silo):
    """
    Devuelve el código de almacén de Murano del silo recibido.
    """
    # OJO: HARCODED
    # Podría tirar de la tabla almacenes y buscar por nombre, pero prefiero
    # ahorrar llamadas al SQLServer.
    almacenes = {"Silo 1": "SIL1",
                 "Silo 2": "SIL2",
                 "Silo 3": "SIL3",
                 "Silo 4": "SIL4",
                 "Silo 5": "SIL5",
                 "Silo 6": "SIL6",
                 "Silo 7": "SIL7",
                 "Silo 8": "SIL8"}
    try:
        almacen = almacenes[silo.nombre]
    except KeyError:
        almacen = None
    return almacen


def _str_time(t):
    """
    Devuelve una cadena con los segundos recibidos en formato minutos:segundos
    """
    minutos = int(t // 60)
    segundos = t % 60
    if minutos:
        res = "{:d}:{:0>5.2f} m".format(minutos, segundos)
    else:
        res = "{:.2f} s".format(segundos)
    return res


def _get_fin_proceso_importacion_retcode(guid):
    """
    Busca un registro concreto en la tabla de Murano encargada de procesar
    las importaciones. Si ese registro existe, la importación ha finalizado.
    Si en ese registro el valor del campo sysStatus es 0, el proceso ha
    terminado bien. Si es 2 (u otro valor, en general) ha habido algún error.
    """
    # pylint: disable=no-value-for-parameter,no-member
    conn = Connection()
    sql = """SELECT sysStatus
     FROM {}.dbo.lsysTraceIME
    WHERE IdProcesoIME=CONVERT(uniqueidentifier, '{}')
      AND sysTraceDescription LIKE 'Fin proceso de importaci%n';""".format(
          conn.get_database(), guid)
    try:
        # FIXME: Ojo porque puede crear 2 registros con el mismo texto y guid.
        # ¿Mismo sysStatus también? Espero que sí... Preguntar a Sage.
        res = conn.run_sql(sql)[0]['sysStatus']
    except IndexError:
        res = None
    return res


def _get_fin_proceso_acumulacion_retcode(guid):
    """
    Busca un registro concreto en la tabla de Murano encargado de acumular los
    campos personalizados en las importaciones.
    Si ese registro existe, la importación ha finalizado.
    Si en ese registro el valor del campo sysStatus es 0, el proceso ha
    acumulado bien. Si es 2 (u otro valor, en general) ha habido algún error.
    """
    # pylint: disable=no-value-for-parameter,no-member
    conn = Connection()
    sql = """SELECT sysStatus
     FROM {}.dbo.LsysTraceIME
    WHERE IdProcesoIME=CONVERT(uniqueidentifier, '{}')
      AND sysTraceDescription LIKE 'Fin proceso de acumulaci%n';""".format(
          conn.get_database(), guid)
    try:
        res = conn.run_sql(sql)[0]['sysStatus']
    except IndexError:
        res = None
    return res


def espera_activa(funcion, parametros, res=None, timeout=30, tick=5):
    """
    Ejecuta la función recibida aplicando la **lista** de parámetros en
    intervalos de `tick`segundos hasta llegar al tiempo indicado en `timeout`
    o hasta que el valor devuelto por la función sea diferente al recibido
    en `res`.
    Devuelve lo que devuelva la función `funcion`.
    """
    antes = time.time()
    if VERBOSE:
        logging.warning("Iniciando espera activa...")
    tries = 0
    max_tries = timeout/tick
    while timeout > 0:
        retCode = funcion(*parametros)
        tries += 1
        if retCode != res:
            success = True
            res = retCode
            timeout = 0
        else:
            success = False
            time.sleep(tick)
            timeout -= tick
    tiempo = time.time() - antes
    strlog = "[{}] Espera activa finalizada en {}/{} intentos ({:.2f} s)"\
             ".".format(success and '✔' or '✘', tries, max_tries, tiempo)
    if VERBOSE:
        logging.warning(strlog)
    return res


# pylint: disable=too-many-statements
def fire(guid_proceso, ignore_errors=False,
         acumular_campos_personalizados=True):
    """
    Lanza el proceso de importación de Murano de todos los movimientos de
    stock de la tabla temporal.

    ~~Devuelve 0 si el proceso se completó con éxito o 1 en caso contrario.~~

    Devuelve True si se completó con éxito o False en caso contrario.
    Ya no devuelve None si Murano lanzó asíncronamente los procesos de
    importación y acumulación. Ahora se hace espera activa hasta que acabe
    el proceso o el tiempo máximo de espera (único caso en que devolvería
    None).
    """
    antes = time.time()
    strerror = "No puede ejecutar código nativo de Murano. Necesita instalar"\
               " la biblioteca win32com y lanzar esta función desde una "\
               "plataforma donde se encuentre instalado Sage Murano."
    if not LCOEM:
        raise NotImplementedError(strerror)
    if VERBOSE:
        logging.info("Inicializando OEM...")
    burano = win32com.client.Dispatch("LogicControlOEM.OEM_EjecutaOEM")
    burano.InicializaOEM(CODEMPRESA,
                         "OEM",
                         "oem",
                         "",
                         r"LOGONSERVER\MURANO",
                         "GEOTEXAN")
    ahora = time.time()
    tiempo_inicializacion = ahora - antes
    str_tiempo_inicializacion = _str_time(tiempo_inicializacion)
    if VERBOSE:
        logging.info("OEM inicializada en %s", str_tiempo_inicializacion)
    retCode = None
    operacion = "ImportaIME"
    strverbose = "Lanzando proceso de importación `%s` con GUID `%s`..." % (
        operacion, guid_proceso)
    if VERBOSE:
        logging.info(strverbose)
    if VERBOSE and DEBUG:
        print(strverbose)
    retCode = burano.EjecutaOEM("LCCImExP.LcImExProceso", operacion,
                                str(guid_proceso), 1, 1, 4)
    # 1 = No borrar registros IME al finalizar.
    # 1 = No borrar registros con errores ni siquiera cuando el primer
    # parámetro esté a 0.
    # 0 = Ejecutar en todos los módulos.
    # 4 = Procesar solo para el módulo de gestión. [20160704] Cambiamos 0 por 4
    # ### [20170601] Espera activa.
    # DONE: En lugar de usar el código de retorno, como resulta que al final
    # las llamadas a la dll son asíncronas, haremos un SELECT contra
    # LsysTraceIME buscando el GUID en cuestión y en sysTraceDescription el
    # texto 'Fin proceso de importación".
    # Si sysStatus es 0, ha acabado bien. Si es 2 (u otro valor), ha habido
    # fallos.
    # **Si el registro no existe, es que no ha terminado todavía.** Hacer
    # espera activa hasta que aparezca el registro.
    retCode = None  # XXX: [20170601] Por algún motivo que ni Félix ni yo
    # adivinamos, la lcOEM ha empezado a devolver 1 aunque importe
    # correctamente los registros. Por tanto, el valor de retorno ya no es
    # útil para detectar nada. Usaremos ya siempre la espera activa, que es lo
    # único fiable.
    if retCode is None:
        retCode = espera_activa(_get_fin_proceso_importacion_retcode,
                                [guid_proceso], retCode, timeout=40, tick=5)
    # ### EOEspera_activa
    strverbose = "Importación `%s` concluida con código de retorno: %s" % (
        guid_proceso, retCode)
    if VERBOSE:
        logging.info(strverbose)
    if VERBOSE and DEBUG:
        print(strverbose)
    # Si retcode es 1: cagada. Si es 0: éxito
    # ¿Y si es None? Lo he visto en procesos con errores.
    #  Mucho me temo que si es None, no lo ha procesado. Y no se procesan más
    # adelante. Se quedan pendiente para siempre.
    # **A no ser que se procese a mano desde Murano**. Entonces se desbloquean
    # todos los pendientes y deja entrar más.
    # **Pero si se hace a mano no se ejecutan el AcumularCamposSeries y el
    # GEO_DIV que divide entre 100.**
    # El GEO_DIV se ejecutará en la siguiente importación, porque se hace
    # para todos los pendientes. Pero el otro necesita un GUID de proceso
    # y habría que editarlo y ejecutarlo a mano uno por uno de los pendientes.
    # O bien tirar del Sr. Lobo y que haga el fire de todos los pendientes.
    # [2016/08/30] UPDATE: En la versión 2016.70.000 se corrige el bug de
    # Murano. Ya no es necesario usar el canal DIV.
    if retCode is None:    # Solo ocurre si se alcanza timeout en espera_activa
        if VERBOSE:
            logging.warning("Se cambia el valor None por 1 (FAIL).")
        retCode = 1
    if retCode and not ignore_errors:
        strerr = "¡PROCESO DE IMPORTACIÓN %s CON ERRORES!"\
                 " No se lanza el script de acumulación de stock." % (
                     guid_proceso)
        logging.error(strerr)
    else:
        if retCode:
            strerr = "¡PROCESO DE IMPORTACIÓN %s CON ERRORES!" % (guid_proceso)
            logging.error(strerr)
        # Después de cada proceso hay que invocar al cálculo que acumula los
        # campos personalizados:
        # FIXED: No ejecuta el cálculo. Era por las '' alrededor del guid.
        # Según el .chm de ayuda los parámetros van sin encerrar en nada
        # aunque sean cadena.
        nombrescript = "AcumularCamposNuevosSeries"
        paramsscript = "Label:=Inicio, idProcesoIME:=%s" % guid_proceso
        if not acumular_campos_personalizados:
            # Si la importación es de movimiento de productos sin campos
            # personalizados, no tiene sentido perder 30 segundos en intentar
            # acumular nada.
            strverbose = "Se ignora script `%s` con GUID `%s`..." % (
                nombrescript, guid_proceso)
            if VERBOSE:
                logging.info(strverbose)
            if VERBOSE and DEBUG:
                print(strverbose)
        else:
            strverbose = "Lanzando script `%s` con GUID `%s`..." % (
                nombrescript, guid_proceso)
            if VERBOSE:
                logging.info(strverbose)
            if VERBOSE and DEBUG:
                print(strverbose)
            retCode = burano.EjecutaScript(nombrescript, paramsscript)
            # retCode devuelve (True, ...) si se hace con éxito. El problema es
            # que no sé si retCode[0] será False cuando falla.
            # ### Fuerzo espera activa para obtener el resultado **real**
            #   (la llamada dentro de la dll parece ser asíncrona y el valor de
            #   retorno, si lo hay, no es de fiar. Puede que siempre sea True
            #   pase lo que pase por dentro de Murano)
            retCode = None
            if retCode is None:
                retCode = espera_activa(_get_fin_proceso_acumulacion_retcode,
                                        [guid_proceso], retCode, timeout=20,
                                        tick=5)
            strverbose = "Ejecución `%s` (GUID `%s`) "\
                         "concluida con código de retorno: %s" % (
                             nombrescript, guid_proceso, retCode)
            if VERBOSE:
                logging.info(strverbose)
            if VERBOSE and DEBUG:
                print(strverbose)
        # ## Ya no es necesario el script del canal DIV. Sage solucionó el bug.
        # nombrescript = "GEO_DividirStock"
        # paramsscript = "Label:=Inicio"
        # strverbose = "Lanzando script `%s`..." % (
        #     nombrescript)
        # logging.info(strverbose)
        # if VERBOSE and DEBUG:
        #     print(strverbose)
        # retCode = burano.EjecutaScript(nombrescript, paramsscript)
        # strverbose = "Ejecución `%s` concluida con código de retorno: %s" % (
        #     nombrescript, retCode)
        # logging.info(strverbose)
        # if VERBOSE and DEBUG:
        #     print(strverbose)
    # El código de retorno es 1 ó 2 para error y 0 para éxito o bien una tupla
    # con True/False en la primera posición. Cambio a boolean.
    if VERBOSE:
        strres = "murano:ops:fire -> Código de retorno: {} ({})".format(
            retCode, type(retCode))
        print(strres)
        logging.info(strres)
    if isinstance(retCode, int):
        res = not bool(retCode)
    else:
        try:
            res = retCode[0]
        except IndexError:  # ¿Qué demonios es?
            res = bool(retCode)
        except TypeError:   # Es None. Lo interpretará como False la invocadora
            res = None
    if VERBOSE:
        strres = "murano:ops:fire -> Valor devuelto: {} ({})".format(
            res, type(res))
        try:
            print(strres)
            logging.info(strres)
        except IOError:
            # Por un error extraño en el ordenador de cemento, que lanza
            # un IOError Errno 9 Bad file descriptor. Probablemente por no
            # tener salida estándar (se abre sin ventana de "terminal").
            pass
    ahora = time.time()
    tiempo_fire = ahora - antes
    str_tiempo_fire = _str_time(tiempo_fire)
    if VERBOSE:
        logging.info("Proceso de importación `%s` finalizado en %s",
                     guid_proceso, str_tiempo_fire)
    return res


def corregir_dimensiones_articulo(articulo, peso_bruto=None, peso_neto=None,
                                  metros_cuadrados=None):
    """
    Corrige el peso bruto, neto y metros cuadrados del artículo recibido
    para poner en Murano los indicados por parámetro o los de los valores
    en ginn para el artículo si son None.
    """
    if peso_bruto is None:
        peso_bruto = articulo.peso_bruto
    if peso_neto is None:
        peso_neto = articulo.peso_neto
    if metros_cuadrados is None:
        metros_cuadrados = articulo.superficie
        if metros_cuadrados is None:
            metros_cuadrados = 0
    codigo = articulo.codigo
    # pylint: disable=no-value-for-parameter,no-member
    conn = Connection()
    tablas = ['ArticulosSeries', 'MovimientoArticuloSerie',
              'GEO_LineasSeriesCargadas', 'GEO_Pales']
    res = True
    for tabla in tablas:
        SQL = r"""UPDATE %s.dbo.%s
                  SET PesoBruto_ = %f,
                      PesoNeto_ = %f,
                      MetrosCuadrados = %f
                  WHERE NumeroSerieLc = '%s'
                    AND CodigoEmpresa = '%s';
               """ % (conn.get_database(), tabla, peso_bruto, peso_neto,
                      metros_cuadrados, codigo, CODEMPRESA)
        res = conn.run_sql(SQL) and res
    return res


def _get_peso_bruto_murano(articulo):
    """
    Devuelve el peso bruto que guarda Murano para el artículo de ginn recibido.
    """
    # pylint: disable=no-value-for-parameter,no-member
    conn = Connection()
    SQL = r"""SELECT PesoBruto_ FROM %s.dbo.ArticulosSeries
               WHERE NumeroSerieLc = '%s'
                 AND CodigoEmpresa = %d;""" % (conn.get_database(),
                                               articulo.codigo,
                                               CODEMPRESA)
    try:
        res = conn.run_sql(SQL)[0]['PesoBruto_']
    except IndexError:
        res = None
    else:
        res = float(res)    # Viene como Decimal()
    return res


def _get_peso_neto_murano(articulo):
    """
    Devuelve el peso bruto que guarda Murano para el artículo de ginn recibido.
    """
    # pylint: disable=no-value-for-parameter,no-member
    conn = Connection()
    SQL = r"""SELECT PesoNeto_ FROM %s.dbo.ArticulosSeries
               WHERE NumeroSerieLc = '%s'
                 AND CodigoEmpresa = %d;""" % (conn.get_database(),
                                               articulo.codigo,
                                               CODEMPRESA)
    try:
        res = conn.run_sql(SQL)[0]['PesoNeto_']
    except IndexError:
        res = None
    else:
        res = float(res)
    return res


def _get_superficie_murano(articulo):
    """
    Devuelve el peso bruto que guarda Murano para el artículo de ginn recibido.
    """
    # pylint: disable=no-value-for-parameter,no-member
    conn = Connection()
    SQL = r"""SELECT MetrosCuadrados FROM %s.dbo.ArticulosSeries
               WHERE NumeroSerieLc = '%s'
                 AND CodigoEmpresa = %d;""" % (conn.get_database(),
                                               articulo.codigo,
                                               CODEMPRESA)
    try:
        res = conn.run_sql(SQL)[0]['MetrosCuadrados']
    except IndexError:
        res = None
    else:
        res = float(res)
    return res


def _get_dimensiones_murano(articulo):
    """
    Devuelve el peso bruto, neto y metros cuadrados que guarda Murano para el
    artículo de ginn recibido.
    """
    # pylint: disable=no-value-for-parameter,no-member
    conn = Connection()
    SQL = r"""SELECT PesoBruto_, PesoNeto_, MetrosCuadrados
              FROM %s.dbo.ArticulosSeries
              WHERE NumeroSerieLc = '%s'
                AND CodigoEmpresa = '%s';""" % (conn.get_database(),
                                                articulo.codigo,
                                                CODEMPRESA)
    try:
        result = conn.run_sql(SQL)[0]
    except IndexError:
        peso_bruto, peso_neto, superficie = None, None, None
    else:
        peso_bruto = result['PesoBruto_']
        peso_neto = result['PesoNeto_']
        superficie = result['MetrosCuadrados']
        peso_bruto = float(peso_bruto)
        peso_neto = float(peso_neto)
        superficie = float(superficie)
    return peso_bruto, peso_neto, superficie


def _get_calidad_murano(articulo):
    """
    Devuelve un caracter con la calidad del artículo (A, B ó C) en Murano para
    el artículo de ginn recibido.
    Devuelve None si el artículo no existe, cadena vacía si no tiene calidad y
    la letra que tenga en Murano si la tiene.
    """
    # pylint: disable=no-value-for-parameter,no-member
    conn = Connection()
    SQL = r"""SELECT CodigoTalla01_
              FROM %s.dbo.ArticulosSeries
              WHERE NumeroSerieLc = '%s'
                AND CodigoEmpresa = '%s';""" % (conn.get_database(),
                                                articulo.codigo,
                                                CODEMPRESA)
    try:
        result = conn.run_sql(SQL)[0]
    except IndexError:
        calidad = None
    else:
        calidad = result['CodigoTalla01_']
    return calidad


def _get_codigo_pale(articulo):
    """
    Devuelve el código de palé que tiene el artículo de ginn en Murano.
    """
    # pylint: disable=no-value-for-parameter,no-member
    conn = Connection()
    SQL = r"""SELECT CodigoPale FROM %s.dbo.ArticulosSeries
              WHERE NumeroSerieLc = '%s'
                AND CodigoEmpresa = '%s';""" % (conn.get_database(),
                                                articulo.codigo, CODEMPRESA)
    try:
        codigo_pale = conn.run_sql(SQL)[0]['CodigoPale']
    except IndexError:
        codigo_pale = None
    return codigo_pale


def corregir_pale(articulo, pale=None):
    """
    Corrige el valor del campo CodigoPale en Murano para el artículo de acuerdo
    al palé o al código de palé recibido.
    """
    if not pale:
        pale = articulo.caja.pale
    try:
        codigo_pale = pale.codigo
    except AttributeError:
        codigo_pale = pale
    # pylint: disable=no-value-for-parameter,no-member
    conn = Connection()
    SQL = r"""UPDATE %s.dbo.ArticulosSeries
                 SET CodigoPale = '%s'
               WHERE CodigoEmpresa = '%s'
                 AND NumeroSerieLc = '%s';""" % (conn.get_database(),
                                                 codigo_pale,
                                                 CODEMPRESA,
                                                 articulo.codigo)
    res = conn.run_sql(SQL)
    return res


def get_producto_murano(codigo):
    """
    Devuelve el registro `Articulos` de Murano que coincide con el código
    (de Murano) recibido. El valor devuelto es un diccionario cuyas claves
    son los nombres de los campos o None si no lo encuentra.
    """
    if isinstance(codigo, pclases.ProductoVenta):
        codigo = "PV{}".format(codigo.id)
    elif isinstance(codigo, pclases.ProductoCompra):
        codigo = "PC{}".format(codigo.id)
    # pylint: disable=no-value-for-parameter,no-member
    conn = Connection()
    SQL = r"""SELECT * FROM %s.dbo.Articulos
              WHERE CodigoEmpresa = '%s'
                AND CodigoArticulo = '%s';""" % (conn.get_database(),
                                                 CODEMPRESA, codigo)
    try:
        prod_murano = conn.run_sql(SQL)[0]
        prod_murano = AttrDict(prod_murano)
    except IndexError:
        strerr = "El código %s no existe en Murano." % (codigo)
        logging.error(strerr)
        prod_murano = None
    return prod_murano


def producto_murano2ginn(codigo, sync=False):
    """
    Vuelca el produco de Murano del código recibido en ginn.
    Respeta el ID de Murano en ginn.
    Si el ID ya existe, machaca la información de ginn con la de Murano si
    el flag «sync» está activo. En otro caso, lanza una excepción.
    """
    # p y l i n t: disable=redefined-variable-type
    prod_murano = get_producto_murano(codigo)
    if not prod_murano:
        strerr = "El código %s no existe en Murano." % (codigo)
        raise ValueError(strerr)
    try:
        prod_ginn = get_producto_ginn(codigo)
    except pclases.SQLObjectNotFound:
        res = _create_producto_ginn(prod_murano)
    else:
        if sync:
            res = _update_producto_ginn(prod_ginn, prod_murano)
        else:
            res = None
    return res


def _create_producto_ginn(prod_murano):
    """
    Recibe un producto de Murano en forma de diccionario cuyas claves son los
    nombres de los campos y los valores, sus valores.
    Crea un producto en ginn con el ID de Murano y devuelve el objeto
    recién creado.
    """
    # p y l i n t: disable=redefined-variable-type
    id_murano = prod_murano['CodigoArticulo']
    if "PV" in id_murano:
        res = _create_producto_venta_ginn(prod_murano)
    elif "PC" in id_murano:
        res = _create_producto_compra_ginn(prod_murano)
    else:
        raise ValueError("Producto {} no soportado.".format(id_murano))
    return res


def _create_producto_compra_ginn(prod_murano):
    """
    Crea un producto de compra en ginn con los datos de prod_murano.
    """
    id_murano = prod_murano['CodigoArticulo']
    ide = int(id_murano.replace("PC", ""))
    # pylint: disable=unexpected-keyword-arg, no-value-for-parameter
    pc = pclases.ProductoCompra(id=ide)
    _update_producto_ginn(pc, prod_murano)
    return pc


def _create_producto_venta_ginn(prod_murano):
    """
    Crea un producto de venta en ginn con los atributos de prod_murano.
    """
    id_murano = prod_murano['CodigoArticulo']
    ide = int(id_murano.replace("PV", ""))
    try:
        # pylint: disable=unexpected-keyword-arg, no-value-for-parameter
        pv = pclases.ProductoVenta(id=ide)
        if prod_murano['CodigoAreaCompetenciaLc'] == "ROLLO":
            pv.camposEspecificosRollo = pclases.CamposEspecificosRollo()
        elif prod_murano['CodigoAreaCompetenciaLc'] == "BALA":
            pv.camposEspecificosBala = pclases.CamposEspecificosBala()
        elif prod_murano['CodigoAreaCompetenciaLc'] == "CAJA":
            pv.camposEspecificosBala = pclases.CamposEspecificosBala()
        elif prod_murano['CodigoAreaCompetenciaLc'] == "BIGBAG":
            pv.camposEspecificosBala = pclases.CamposEspecificosBala()
        else:
            strerror = "El producto {} no tiene indicado si es rollo, bala, "\
                       "caja o bigbag en Murano (campo «Área "\
                       "competencia»).".format(prod_murano['CodigoArticulo'])
            print(strerror)
            logging.error(strerror)
            pv.destroySelf()
            pv = None
    # pylint: disable=broad-except
    except Exception as excepcion:
        # TODO: Hasta que lea directamente el producto de Murano
        # desde el parte y laboratorio, sincronizar manualmente con estas
        # funciones.
        strerror = "El producto {} no se pudo crear en ginn."\
                   " Expceción: {}".format(prod_murano['CodigoArticulo'],
                                           excepcion)
        print(strerror)
        logging.error(strerror)
        pv = None
    else:
        if pv:
            _update_producto_ginn(pv, prod_murano)
    return pv


def _update_producto_ginn(prod_ginn, prod_murano):
    """
    Recibe un producto de ginn y otro de Murano en forma de diccionario.
    Actualiza los campos de ginn según los valores del de Murano.
    Devuelve None si no se pudo actualizar, y el producto de ginn sí se pudo.
    """
    res = None
    if isinstance(prod_ginn, pclases.ProductoCompra):
        res = _update_producto_compra_ginn(prod_ginn, prod_murano)
    elif isinstance(prod_ginn, pclases.ProductoVenta):
        res = _update_producto_venta_ginn(prod_ginn, prod_murano)
    return res


def _get_tipo_de_material(codigo):
    """
    Devuelve el registro tipo de material de ginn correspondiente al código
    recibido de Murano.
    """
    # pylint: disable=bad-continuation
    switcher = {'OIL': pclases.TipoDeMaterial.selectBy(
                descripcion='Aceites y lubricantes')[0],
                'COM': pclases.TipoDeMaterial.selectBy(
                descripcion='Comercializados')[0],
                'MAN': pclases.TipoDeMaterial.selectBy(
                descripcion='Mantenimiento')[0],
                'MAP': pclases.TipoDeMaterial.selectBy(
                descripcion='Materia Prima')[0],
                'GRANZA': pclases.TipoDeMaterial.selectBy(
                descripcion='Materia Prima')[0],
                'MAT': pclases.TipoDeMaterial.selectBy(
                descripcion='Material adicional')[0],
                'MIV': pclases.TipoDeMaterial.selectBy(
                descripcion='Mercancía inicial Valdemoro')[0],
                'PCOM': pclases.TipoDeMaterial.selectBy(
                descripcion='Productos comercializados')[0],
                'REF': pclases.TipoDeMaterial.selectBy(
                descripcion='Repuestos fibra')[0],
                'REG': pclases.TipoDeMaterial.selectBy(
                descripcion='Repuestos geotextiles')[0]}
    return switcher.get(codigo, None)


def _update_producto_compra_ginn(prod_ginn, prod_murano):
    """
    Actualiza los valores del producto de compra con los del producto en
    Murano.
    """
    res = prod_ginn
    try:
        prod_ginn.descripcion = prod_murano['DescripcionArticulo']
    except UnicodeEncodeError:
        prod_ginn.descripcion = prod_murano['DescripcionArticulo'].encode(
            "utf8")
    prod_ginn.tipoDeMaterial = _get_tipo_de_material(
        prod_murano['CodigoFamilia'])
    prod_ginn.codigo = prod_murano['CodigoAlternativo']
    prod_ginn.unidad = prod_murano['UnidadMedida2_']
    prod_ginn.precioDefecto = prod_murano['PrecioVenta']
    # Si es Material (M) sí lo lleva. Si es Inmaterial o Comentario, no.
    prod_ginn.controlExistencias = prod_murano['TipoArticulo'] == "M"
    try:
        prod_ginn.observaciones = prod_murano['ComentarioArticulo']
    except UnicodeEncodeError:
        prod_ginn.observaciones = prod_murano.ComentarioArticulo.encode("utf8")
    # Si está obsoleto para Murano, -1. Si no, 0
    prod_ginn.obsoleto = prod_murano['ObsoletoLc'] == -1
    try:
        proveedor = pclases.Proveedor.get(prod_murano['CodigoProveedor'])
    except (ValueError, pclases.SQLObjectNotFound):
        # Es un ID de un proveedor que no existe en ginn o está mal informado
        # en Murano y en lugar de un número es una cadena de texto.
        proveedor = None
    prod_ginn.proveedor = proveedor
    prod_ginn.minimo = prod_murano['StockMinimo']
    # Función de valoración y existencias ya no me interesan ni para sync.
    # prod_ginn.fvaloracion =
    # prod_ginn.existencias =
    return res


def _update_producto_venta_ginn(prod_ginn, prod_murano):
    """
    Actualiza el registro de ginn conforme a los datos del registro de Murano.
    Tiene en cuenta el tipo de producto para actualizar también los valores
    de los registros relacionados camposEspecificos*.
    Se procura no machacar la descripción del producto en ginn. Admite más
    caracteres que en Murano y se usa para imprimir las etiquetas. Preferimos
    usar la descripción de ginn, que no está cortada para productos largos.
    """
    res = _sync_campos_comunes_pv(prod_ginn, prod_murano)
    res = _sync_campos_especificos(prod_ginn, prod_murano)
    return res


def _sync_campos_comunes_pv(prod_ginn, prod_murano):
    """
    Copia en el registro prod_ginn los valores de prod_murano comunes a todos
    los productos de venta.
    """
    res = prod_ginn
    prod_ginn.lineaDeProduccion = _get_linea_produccion_ginn(
        prod_murano.DescripcionLinea)
    try:
        prod_ginn.nombre = prod_murano.Descripcion2Articulo
    except UnicodeEncodeError:
        # Por un error de sqlobject, no parece estar reconociendo bien el
        # encoding. Lo fuerzo para los casos del PV581 en polaco, por ejemplo.
        connection = pclases.sqlhub.getConnection()
        connection.dbEncoding = "utf-8"
        prod_ginn.nombre = prod_murano.Descripcion2Articulo
    if prod_murano.DescripcionArticulo:
        try:
            prod_ginn.descripcion = prod_murano.DescripcionArticulo
        except UnicodeEncodeError:
            connection = pclases.sqlhub.getConnection()
            connection.dbEncoding = "utf-8"
            prod_ginn.descripcion = prod_murano.DescripcionArticulo
    prod_ginn.codigo = prod_murano.CodigoAlternativo
    prod_ginn.arancel = prod_murano.CodigoArancelario
    prod_ginn.prodestandar = prod_murano.GEO_ProdEstandar
    prod_ginn.annoCertificacion = prod_murano.GEO_anno_certificacion
    prod_ginn.dni = prod_murano.GEO_Dni
    prod_ginn.uso = _get_uso_ginn(prod_murano.GEO_Uso)
    prod_ginn.obsoleto = prod_murano.ObsoletoLc == -1
    return res


def _sync_campos_especificos(prod_ginn, prod_murano):
    """
    Sincroniza los campos específicos del producto de ginn con los de Murano.
    """
    if prod_ginn.camposEspecificosRollo:
        res = _sync_campos_especificos_rollo(prod_ginn, prod_murano)
    elif prod_ginn.camposEspecificosBala:
        res = _sync_campos_especificos_bala(prod_ginn, prod_murano)
    else:
        res = _sync_campos_especificos_especial(prod_ginn, prod_murano)
    return res


def _sync_campos_especificos_rollo(prod_ginn, prod_murano):
    """
    Sincroniza los campos relacionados con los geotextiles.
    """
    res = prod_ginn
    cer = prod_ginn.camposEspecificosRollo
    if prod_murano.GEO_Cliente_id:
        if prod_murano.GEO_Cliente_id.startswith("C"):
            # Como no admitimos id alfanuméricos y es poco probable que
            # lleguemos a un millón de clientes, uso los nuevos clientes
            # Cnnnnnn de Murano como 1nnnnnn en ginn.
            cliente_id = prod_murano.GEO_Cliente_id.replace("C", "1")
        else:
            try:
                cliente_id = int(prod_murano.GEO_Cliente_id)
            except ValueError:
                cliente_id = prod_murano.GEO_Cliente_id
        try:
            cer.clienteID = cliente_id
        except TypeError:
            cer.clienteID = None
            res = False
    else:
        cer.clienteID = None
    if res:
        cer.gramos = prod_murano.GEO_gramos
        cer.codigoComposan = prod_murano.MarcaProducto
        cer.ancho = prod_murano.GEO_ancho
        cer.diametro = prod_murano.GEO_Diametro
        cer.rollosPorCamion = prod_murano.GEO_rollos_por_camion
        cer.metrosLineales = prod_murano.GEO_metros_lineales
        cer.pesoEmbalaje = prod_murano.GEO_peso_embalaje
        cer.modeloEtiqueta = _get_modelo_etiqueta_ginn(
            prod_murano.GEO_Modelo_etiqueta_id)
        cer.fichaFabricacion = prod_murano.GEO_Ficha_fabricacion
        res = _sync_marcado_ce(prod_ginn, prod_murano)
    return res


def _sync_marcado_ce(prod_ginn, prod_murano):
    """
    Sincroniza los valores del marcado CE. Si han cambiado, se crea un
    registro histórico del marcado actual en ginn.
    """
    res = prod_ginn
    # TODO: PORASQUI
    return res


def _sync_campos_especificos_bala(prod_ginn, prod_murano):
    """
    Sincroniza los campos relacionados con la fibra.
    """
    res = prod_ginn
    ceb = prod_ginn.camposEspecificosBala
    ceb.dtex = prod_murano.GEO_Dtex
    ceb.corte = prod_murano.GEO_Corte
    ceb.color = prod_murano.GEO_Color
    ceb.antiuv = prod_murano.GEO_antiuv == -1
    ceb.tipoMaterialBalaID = _get_tipo_material_bala_ginn(
        prod_murano.GEO_Tipo_Material_bala_id)
    ceb.consumoGranza = prod_murano.GEO_Consumo_granza
    ceb.reciclada = prod_murano.GEO_Reciclada == -1
    ceb.gramosBolsa = prod_murano.GEO_gramos_bolsa
    ceb.bolsasCaja = prod_murano.GEO_bolsas_Caja
    ceb.cajasPale = prod_murano.GEO_Cajas_pale
    ceb.modeloEtiqueta = _get_modelo_etiqueta_ginn(
            prod_murano.GEO_Modelo_etiqueta_id)
    if prod_murano.GEO_Cliente_id:
        if prod_murano.GEO_Cliente_id.startswith("C"):
            # Como no admitimos id alfanuméricos y es poco probable que
            # lleguemos a un millón de clientes, uso los nuevos clientes
            # Cnnnnnn de Murano como 1nnnnnn en ginn.
            cliente_id = prod_murano.GEO_Cliente_id.replace("C", "1")
        else:
            try:
                cliente_id = int(prod_murano.GEO_Cliente_id)
            except ValueError:
                cliente_id = prod_murano.GEO_Cliente_id
        try:
            ceb.clienteID = cliente_id
        except TypeError:
            ceb.clienteID = None
            res = False
    else:
        ceb.clienteID = None
    return res


def _sync_campos_especificos_especial(prod_ginn, prod_murano):
    """
    No sincroniza nada porque los productos con CamposEspecificosEspedoal
    son pocos y los campos, obsoletos.
    """
    res = prod_ginn
    return res


def get_canal(producto):
    """
    Busca el canal del producto en Murano y devuelve el código de canal
    (HARCODED en `connection`) correspondiente. None si en Murano no tiene
    canal informado.
    Acepta objeto de pclases o código (como cadena) directamente.
    Si el producto no existe, lanza una excepción.
    """
    if isinstance(producto, pclases.ProductoCompra):
        codigo = "PC" + str(producto.id)
    elif isinstance(producto, pclases.ProductoVenta):
        codigo = "PV" + str(producto.id)
    elif isinstance(producto, str):
        codigo = producto
    else:
        raise TypeError("ops::get_canal -> producto debe ser un "
                        "pclases.ProductoCompra o pclases.ProductoVenta")
    pmurano = get_producto_murano(codigo)
    canal = pmurano.CodigoCanal     # pylint: disable=no-member
    try:
        cod_canal = CANALES[canal]
    except KeyError:
        cod_canal = None
    return cod_canal


def get_proyecto(producto):
    """
    Busca el proyecto del producto en Murano y devuelve el código de proyecto
    (HARCODED en `connection`) correspondiente. Cero si en Murano no tiene
    proyecto informado («Sin informar»).
    Acepta objeto de pclases o código (como cadena) directamente.
    Si el producto no existe, lanza una excepción.
    """
    if isinstance(producto, pclases.ProductoCompra):
        codigo = "PC" + str(producto.id)
    elif isinstance(producto, pclases.ProductoVenta):
        codigo = "PV" + str(producto.id)
    elif isinstance(producto, str):
        codigo = producto
    else:
        raise TypeError("ops::get_proyecto -> producto debe ser un "
                        "pclases.ProductoCompra o pclases.ProductoVenta")
    pmurano = get_producto_murano(codigo)
    cod_proyecto = pmurano.CodigoProyecto     # pylint: disable=no-member
    return cod_proyecto


def get_stock_murano(producto, _almacen=None, _calidad=None, _unidad=None):
    """
    Devuelve un diccionario por almacén con el stock del producto recibido
    tanto en unidades base como específica y calidad (si se aplican).
    Si se especifica código de almacén o unidad, solo devuelve las existencias
    para ese almacén y unidad.
    Ejemplos:
    {'GTX': {'A': {'KG': 100, 'ROLLO': 2},
             'B': {'KG': 500, 'ROLLO': 10}},
     'SUS': {'A': {'KG': 500, 'ROLLO': 10}}}
    {'GTX': {'UD': 13},
     'RES': {'UD': 0}}
    """
    if isinstance(producto, pclases.ProductoCompra):
        codigo = "PC" + str(producto.id)
    elif isinstance(producto, pclases.ProductoVenta):
        codigo = "PV" + str(producto.id)
    elif isinstance(producto, str):
        codigo = producto
    else:
        raise TypeError("ops::get_stock_murano -> producto debe ser un "
                        "pclases.ProductoCompra o pclases.ProductoVenta")
    pmurano = get_producto_murano(codigo)
    res = {}
    # pylint: disable=no-value-for-parameter,no-member
    conn = Connection()
    rs_ejercicio = conn.run_sql("""SELECT MAX(Ejercicio) AS ejercicio
                                   FROM {}.dbo.AcumuladoStock
                                   WHERE CodigoEmpresa = {};
                                """.format(conn.get_database(),
                                           CODEMPRESA))
    ejercicio = rs_ejercicio[0]['ejercicio']
    codempresa = CODEMPRESA
    database = conn.get_database()
    periodo = 99
    sql = """SELECT CodigoAlmacen, CodigoTalla01_, TipoUnidadMedida_,
                    UnidadSaldo, UnidadSaldoTipo_
               FROM {}.dbo.AcumuladoStock
              WHERE CodigoEmpresa = {}
                AND Ejercicio = {}
                AND CodigoArticulo = '{}'
                AND Periodo = {};
            """.format(database,
                       codempresa,
                       ejercicio,
                       pmurano['CodigoArticulo'],
                       periodo)
    rs = conn.run_sql(sql)
    # Tratamiento de datos: los meto en un diccionario bien estructurado.
    for registro in rs:     # Cada registro, el acumulado de una partida
        almacen = registro['CodigoAlmacen']
        calidad = registro['CodigoTalla01_']
        if almacen not in res:
            res[almacen] = {}
        if calidad not in res[almacen]:
            res[almacen][calidad] = defaultdict(lambda: 0.0)
        stock_basica = registro['UnidadSaldo']
        stock_especifica = registro['UnidadSaldoTipo_']
        unidad_especifica = registro['TipoUnidadMedida_']
        unidad_basica = pmurano['UnidadMedida2_']
        if _unidad:
            if _unidad == unidad_especifica:
                res[almacen][calidad][unidad_especifica] += float(
                        stock_especifica)
            elif _unidad == unidad_basica:
                res[almacen][calidad][unidad_basica] += float(stock_basica)
        else:
            res[almacen][calidad][unidad_basica] += float(stock_basica)
            res[almacen][calidad][unidad_especifica] += float(stock_especifica)
    # Ahora filtro por los valores recibidos:
    # La unidad se filtra arriba directamente. La unidad (KG, BALA...) siempre
    # se devuelve para saber en qué está el valor. A no ser que (y por
    # simplificar) si me piden un almacén concreto, calidad y una dimensión
    # concreta, solo tendré un valor en el diccionario. Lo devuelvo
    # directamente.
    if _almacen is not None and _calidad is not None and _unidad is not None:
        try:
            res = res[_almacen][_calidad][_unidad]
        except KeyError:
            # O no hay stock para ese almacén, o en esa calidad o la unidad
            # es errónea.
            # Por simplificar, si pide una cantidad en concreto devuelvo float.
            res = 0.0   # pylint: disable=redefined-variable-type
    else:
        if _calidad:
            _res = {}
            for almacen in res:
                try:
                    _res[almacen] = res[almacen][_calidad]
                except KeyError:
                    # Esa calidad no está presente en el almacén
                    _res[almacen] = {}
            res = _res
        if _almacen:
            res = res[_almacen]
    return res
