#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from connection import Connection, DEBUG

try:
    import win32com.client
except ImportError:
    LCOEM = False
else:
    LCOEM = True

CODEMPRESA = 9999   # Empresa de pruebas. Cambiar por la 10200 en producción.

SQL = """INSERT INTO TmpIME_MovimientoStock(
            CodigoEmpresa,
            Ejercicio,
            Periodo,
            Fecha,
            Serie,
            Documento,
            CodigoArticulo,
            CodigoAlmacen,
            AlmacenContrapartida,
            Partida,
            Partida2_,
            CodigoColor_,
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
            CodigoCliente,
            CodigoProveedor,
            FechaCaduca,
            Ubicacion,
            OrigenMovimiento,
            EmpresaOrigen,
            MovOrigen,
            EjercicioDocumento,
            NumeroSerieLc,
            IdProcesoIME,
            MovIdentificadorIME,
            StatusTraspasadoIME,
            TipoImportacionIME,
            DocumentoUnico,
            FechaRegistro,
            MovPosicion)
        VALUES (
            %d,         -- código empresa
            %d,         -- ejercicio
            %d,         -- periodo
            '%s',       -- fecha
            'FAB',
            '%s',       -- documento
            '%s',       -- codigo_articulo
            '%s',       -- codigo_almacen
            NULL,
            '%s',       -- partida
            NULL,
            NULL,
            %d,         -- grupo_talla
            '%s',       -- codigo_talla
            %d,         -- tipo_movimiento
            %d,         -- unidades
            '%s',       -- unidad de medida específica
            %f,         -- precio
            %f,         -- importe
            %f,         -- unidades2 = unidades * factor de conversion
            NULL,
            %f,         -- factor de conversión
            '%s',       -- comentario
            NULL,
            NULL,
            NULL,
            NULL,
            '%s',       -- ubicación
            '%s',       -- origen movimiento
            NULL,
            NULL,
            NULL,
            '%s',       -- NumeroSerieLc
            '%s',       -- IdProcesoIME
            NULL,
            0,
            0,
            -1,
            NULL,
            NULL);"""

SQL_SERIE = """INSERT INTO TmpIME_MovimientoSerie(
                CodigoEmpresa,
                CodigoArticulo,
                NumeroSerieLc,
                Fecha, 
                OrigenDocumento,
                EjercicioDocumento,
                SerieDocumento,
                Documento,
                MovPosicionOrigen,
                CodigoColor_,
                CodigoTalla01_,
                CodigoAlmacen,
                Ubicacion,
                Partida,
                UnidadMedida1_,
                UnidadesSerie,
                NumeroSerieFabricante,
                EmpresaOrigen,
                CodigoCliente,
                CodigoProveedor,
                Comentario,
                IdProcesoIME,
                MovIdentificadorIME,
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
                '%s',   -- documento
                '%s',   -- mov. posición origen
                NULL,
                '%s',   -- código talla
                '%s',   -- código almacén
                '%s',   -- ubicación
                '%s',   -- partida
                '%s',   -- unidad de medida específica (kg, m²)
                1,
                NULL,
                NULL,
                NULL,
                NULL,
                '%s',   -- comentario
                '%s',   -- ID proceso IME
                NULL,
                0,
                0,
                %f,     -- peso bruto
                %f,     -- peso neto
                %s,     -- metros cuadrados
                %s      -- código de palé
               );"""

def buscar_codigo_producto(productoVenta):
    """
    Busca el ID del producto en Murano para la descripción del producto
    recibido.
    """
    c = Connection()
    res = c.run_sql("""SELECT CodigoArticulo
                         FROM Articulos
                        WHERE DescripcionArticulo = '%s';
                    """ % productoVenta.descripcion)
    try:
        codarticulo = res[0][0]
    except TypeError, e:
        if not DEBUG:
            raise e
        else:
            return '00002'  # FIXME: Dato de prueba.
    return codarticulo

def buscar_codigo_almacen(self):
    # TODO
    return 1

def simulate_guid():
    import random
    grupos = 8, 4, 4, 12
    subgrupos = []
    for g in grupos:
        subgrupo = ""
        for i in range(g):
            c = random.choice("01234567890ABCDE")
            subgrupo += c
        subgrupos.append(subgrupo)
    guid = "-".join(subgrupos)
    return guid

def buscar_factor_conversion(self):
    # TODO
    return 1

def genera_guid():
    """
    Devuelve un GUID de SQLServer o simula uno en modo depuración.
    """
    try:
        guid = c.run_sql("SELECT NEWID();")[0][0]
    except Exception, e:
        if not DEBUG:
            raise e
        else:
            guid = simulate_guid()
    return guid

def get_mov_posicion():
    """
    GUID del movimiento de stock asociado al movimiento de número de serie.
    """
    # TODO:
    return simulate_guid()

def create_bala(bala):
    """
    Crea una bala en las tablas temporales de Murano.
    Recibe un objeto bala de ginn.
    """
    today = datetime.date.today()
    ejercicio = today.year
    periodo = today.month
    fecha = today.strftime("%Y-%m-%d")
    documento = "FAB%s" % today.strftime("%Y%m%d")
    codigo_articulo = buscar_codigo_producto(bala.articulo.productoVenta)
    codigo_almacen = buscar_codigo_almacen(bala.articulo.almacen)
    partida = bala.lote.codigo
    grupo_talla = 1    # TODO: ¿Seguro que solo hay un grupo de talla? Creo que hemos creado alguno más. 1 para A, B y C, 2 para A, B (sin C), etc.
    codigo_talla = bala.articulo.get_str_calidad()
    tipo_movimiento = 1     # 1 = entrada, 2 = salida.
    unidades = 1    # En dimensión base: 1 bala.
    unidad_medida = "KG",
    precio = 0.0    # TODO: Hasta que se defina bien el precio coste por familia y cómo actualizarlo mensialmente.
    importe = unidades * precio
    factor_conversion = buscar_factor_conversion(bala.articulo.productoVenta)
    unidades2 = unidades * factor_conversion
    comentario = "Bala insertada desde ginn. [%s]" % bala.get_info()
    ubicacion = "Almacén de fibra."
    origen_movimiento = "F" # E = Entrada de Stock (entrada directa), F (fabricación), I (inventario), M (rechazo fabricación), S (Salida stock)
    numero_serie_lc = bala.codigo
    id_proceso_IME = genera_guid()
    sql_movstock = SQL % (CODEMPRESA, ejercicio, periodo, fecha, documento,
                          codigo_articulo, codigo_almacen, partida,
                          grupo_talla, codigo_talla, tipo_movimiento, unidades,
                          unidad_medida, precio, importe, unidades2,
                          factor_conversion, comentario, ubicacion,
                          origen_movimiento, numero_serie_lc,
                          id_proceso_IME)
    c = Connection()
    c.run_sql(sql_movstock)
    origen_documento = 2 # 2 (Fabricación), 10 (entrada de stock), 11 (salida de stock), 12 (inventario)
    mov_posicion_origen = get_mov_posicion()
    sql_movserie = SQL_SERIE % (CODEMPRESA, codigo_articulo, numero_serie_lc,
                                fecha, origen_documento, ejercicio, documento,
                                mov_posicion_origen, codigo_talla,
                                codigo_almacen, ubicacion, partida,
                                unidad_medida, comentario, id_proceso_IME,
                                bala.articulo.peso, bala.articulo.peso_sin,
                                "NULL", "NULL")
    c.run_sql(sql_movserie)

def create_bigabag(bigbag):
    """
    Crea un bigbag en Murano a partir de la información del bigbag en ginn.
    """
    pass

def create_rollo(rollo):
    """
    Crea un rollo en Murano a partir de la información del rollo en ginn.
    """
    pass

def create_pale(pale):
    """
    Crea un palé con todas sus cajas en Murano a partir del palé de ginn.
    """
    pass

def consulta_proveedor(nombre = None, cif = None):
    """
    Obtiene los datos de un proveedor buscando por nombre, cif o ambas cosas.
    Devuelve una lista de proveedores coincidentes.
    """

def consulta_cliente(nombre = None, cif = None):
    """
    Obtiene los datos de un cliente buscando por nombre, cif o ambas cosas.
    Devuelve una lista de clientes coincidentes.
    """
    pass

def consulta_producto(nombre = None):
    """
    Busca un producto por nombre.
    Devuelve una lista de productos coincidentes.
    """
    pass

def update_calidad(articulo, calidad):
    """
    Cambia la calidad del artículo en Murano a la recibida. Debe ser A, B o C.
    """
    if calidad not in "aAbBcC":
        raise ValueError, "El parámetro calidad debe ser A, B o C."

def update_producto(articulo, producto):
    """
    Cambia el artículo recibido al producto indicado.
    """
    pass

def update_stock(producto, delta):
    """
    Incrementa o decrementa el stock del producto en la cantidad recibida en
    en el parámetro «delta».
    El producto no debe tener trazabilidad. En otro caso deben usarse las
    funciones "crear_[bala|rollo...]".
    """
    pass

def delete_articulo(articulo):
    """
    Elimina el artículo en Murano mediante la creación de un movimiento de
    stock negativo de ese código de producto.
    """
    pass

def fire():
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
                         "LOGONSERVER\\MURANO",
                         "GEOTEXAN")
    retCode = None
    operacion = "ENT_LisMunicipios" # TODO: Cambiar por la de verdad.
    burano.EjecutaOperacion(operacion, None, retCode)
