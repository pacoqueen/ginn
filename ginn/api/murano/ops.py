#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Operaciones.

"""
# TODO: Sería interesante guardar un log de todas las consultas lanzadas y el resultado de las mismas para no depender de la salida por consola y el DEBUG.
# TODO: Tengo que hacer un proceso para exportar productos, clientes, proveedores, etc. Porque hacerlo a mano con las guías de exportación mediante hojas de cálculo es un coñazo supino. Y tal vez así podemos poner el código de barras y el ID PK interno mío en algún sitio para después mejorar las búsquedas.

import datetime
from connection import Connection, DEBUG, VERBOSE

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
                %s      -- código de palé
               );"""

def buscar_grupo_talla(productoVenta):
    """
    Devuelve el código de grupo de tallas (calidades) que puede tener el
    producto.
    """
    # Hemos varios grupos de talla: 1 para A, B y C, 2 para A, B (sin C), etc.
    grupo_talla = 0     # Sin grupo de talla
    res = consultar_producto(productoVenta.descripcion)
    try:
        grupo_talla = res[0]['GrupoTalla_']
    except TypeError, e:
        print "(EE)[T]", productoVenta.descripcion, "no se encuentra en Murano."
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
    res = consultar_producto(productoVenta.descripcion)
    try:
        codarticulo = res[0]['CodigoArticulo']
    except TypeError, e:
        # TODO: Ver cómo tratar los errores de cuando el producto no existe en Murano. ¿Se puede dar el caso? Todos se darán de alta en Murano y se buscarán ahí cuando se creen los artículos en los partes de producción. Debería exisitir. **Pero se podría dar el caso de que el nombre haya cambiado.**
        print "(EE)[C]", productoVenta.descripcion, "no se encuentra en Murano."
        if not DEBUG:
            raise e
        else:
            codarticulo = ''
    return codarticulo

def buscar_codigo_almacen(almacen):
    """
    Devuelve almacén de la empresa configurada cuyo nombre coincida con el del
    almacén de ginn recibido.
    """
    # TODO: FIXME: Tenemos un problema. Si por ejemplo recibo una bala consumida, su valor para almacén será None y dará ERROR.
    if almacen:
        c = Connection()
        filas = c.run_sql("""SELECT CodigoAlmacen
            FROM %s.dbo.Almacenes
            WHERE CodigoEmpresa = %d AND Almacen = '%s'
            ORDER BY CodigoAlmacen;""" % (c.get_database(), 
                                          CODEMPRESA,
                                          almacen.nombre))
        try:
            codalmacen = filas[0]['CodigoAlmacen']
        except Exception, e:
            print "(EE)[A]", almacen.nombre, "no se encuentra en Murano."
            if not DEBUG:
                raise e
            else:
                return 'CEN'
    else:
        if DEBUG:
            return 'CEN'
        else:
            raise ValueError, "(EE)[A] Debe especificarse un almacén."
    return codalmacen

def simulate_guid():
    """
    Genera un código aleatorio similar al generado por MSSQLServer.
    """
    if VERBOSE:
        print "Simulando guid...",
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
        print guid
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

def genera_guid():
    """
    Devuelve un GUID de SQLServer o simula uno en modo depuración.
    """
    try:
        guid = c.run_sql("SELECT NEWID() AS guid;")[0]['guid']
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
        mov_posicion = conexion.run_sql(r"""SELECT MovPosicion
            FROM %s.dbo.TmpIME_MovimientoStock
            WHERE NumeroSerieLc = '%s';
            """ % (conexion.get_database(), codigo_articulo))[0]['MovPosicion']
    except Exception, e:
        if not DEBUG:
            raise e
        else:
            mov_posicion = simulate_guid()
    return mov_posicion

def crear_proceso_IME(conexion):
    """
    Crea un proceso de importación con guid único.
    """
    guid_proceso = genera_guid()
    conexion.run_sql(r"""
        INSERT INTO %s.dbo.Iniciador_tmpIME(IdProcesoIME, EstadoIME, sysUsuario,
                                     sysUserName, Descripcion, TipoImportacion)
        VALUES ('%s', 0, 1, 'administrador', 'Importación desde ginn', 254);
        """ % (conexion.get_database(), guid_proceso))
    return guid_proceso

def prepare_params(articulo, cantidad = 1):
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
    codigo_articulo = buscar_codigo_producto(articulo.productoVenta)
    codigo_almacen = buscar_codigo_almacen(articulo.almacen)
    codigo_talla = articulo.get_str_calidad()
    grupo_talla = buscar_grupo_talla(articulo.productoVenta)
    if cantidad == 1:
        tipo_movimiento = 1     # 1 = entrada, 2 = salida.
    else:
        tipo_movimiento = 2
    unidades = 1    # En dimensión base: 1 bala, rollo, caja, bigbag...
    precio = 0.0    # TODO: Hasta que se defina bien el precio coste por familia y cómo actualizarlo mensialmente.
    importe = unidades * precio
    factor_conversion = buscar_factor_conversion(articulo.productoVenta)
    unidades2 = unidades * factor_conversion
    origen_movimiento = "F" # E = Entrada de Stock (entrada directa), 
                            # F (fabricación), I (inventario), 
                            # M (rechazo fabricación), S (Salida stock)
    return (c, database, ejercicio, periodo, fecha, documento, codigo_articulo,
            codigo_almacen, grupo_talla, codigo_talla, tipo_movimiento,
            unidades, precio, importe, unidades2, factor_conversion,
            origen_movimiento)

def create_bala(bala, cantidad = 1):
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
            origen_movimiento) = prepare_params(articulo, cantidad)
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
                                "''"   # Código palé. Varchar NOT NULL
                               )
    c.run_sql(sql_movserie)
    fire(id_proceso_IME)

def create_bigabag(bigbag, cantodad = 1):
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
            origen_movimiento) = prepare_params(articulo, cantidad)
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
                                "''"   # Código palé. Varchar NOT NULL
                               )
    c.run_sql(sql_movserie)
    fire(id_proceso_IME)

def create_rollo(rollo, cantidad = 1):
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
            origen_movimiento) = prepare_params(articulo, cantidad)
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
                                "''"   # Código palé. Varchar NOT NULL
                               )
    c.run_sql(sql_movserie)
    fire(id_proceso_IME)

def create_caja(caja, cantidad = 1):
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
            origen_movimiento) = prepare_params(articulo, cantidad)
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
                                caja.pale and caja.pale.codigo or "''"
                                       # Código palé. Varchar NOT NULL
                               )
    c.run_sql(sql_movserie)
    fire(id_proceso_IME)

def create_pale(pale, cantidad = 1):
    """
    Crea un palé con todas sus cajas en Murano a partir del palé de ginn.
    Si cantidad es -1 saca el palé del almacén.
    """
    # Los palés se crean automáticamente al crear las cajas con el código de
    # palé informado. No hay que crear movimiento de stock ni de número de
    # serie para eso.
    for caja in pale.cajas:
        # TODO: Check que compruebe si la caja ya existía para no duplicarlas.
        create_caja(caja, cantidad)
    fire(id_proceso_IME)

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

def consultar_producto(nombre = None):
    """
    Busca un producto por nombre.
    Devuelve una lista de productos coincidentes.
    """
    # TODO: Permitir la búsqueda por código EAN.
    c = Connection()
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
    # TODO: Ojo porque si cambio a calidad C probablemente implique un cambio de producto.
    if calidad not in "aAbBcC":
        raise ValueError, "El parámetro calidad debe ser A, B o C."
    # DONE: [Marcos Sage] No modificamos tablas. Hacemos salida del producto A y volvemos a insertarlo como C. En ese caso no importa que se repita el código para el mismo producto porque antes hemos hecho la salida.

def create_articulo(articulo, producto = None):
    """
    Crea un artículo nuevo en Murano con el producto recibido. Si no se
    recibe ninguno, se usa el que tenga asociado en ginn. Si se recibe un
    objeto producto, se ignora el actual del artículo, se reemplaza en ginn
    por el recibido y se da de alta así en Murano.
    """
    if articulo.es_bala():
        create_bala(articulo.bala)
    elif articulo.es_balaCable():
        create_bala(articulo.balaCable)
    elif articulo.es_bigbag():
        create_bigabag(articulo.bigbag)
    elif articulo.es_caja():
        create_caja(articulo.caja)
    elif articulo.es_rollo():
        create_rollo(articulo.rollo)
    elif articulo.es_rolloC():
        create_rollo(articulo.rolloC)
    else:
        raise ValueError, "El artículo %s no es bala, bala de cable, bigbag,"\
                          " caja, rollo ni rollo C." % (articulo.puid)

def update_producto(articulo, producto):
    """
    Cambia el artículo recibido al producto indicado.
    """
    delete_articulo(articulo)
    create_articulo(articulo, producto)

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
        tipo_movimiento = 2
    unidades = delta    # En dimensión base del producto.
    precio = producto.precioDefecto # TODO: Hasta que se defina bien el precio coste del producto en el momento de ser consumido
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
    create_articulo(articulo, -1)

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
                                guid_proceso, 1, 1, 0)
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

## ====================
## Exportación de datos
## ====================

def exportar_productos():
    """
    Exporta los productos de venta y de compra a una tabla CSV.
    """
    columnas = (
        "id",
        "lineaDeProduccion.nombre",     # Indirecto
        "nombre",
        "descripcion",
        "codigo",
        "minimo",
        "precioPorDefecto/precioDefecto",
                                        # precioDefecto en productos de compra.
        "arancel",
        "prodestandar",
        "annoCertificacion",
        "dni",
        "uso",
        "obsoleto",
        # Específicos de productos de compra:
        "tipoDeMaterial.descripcion", # Indirecto:
                                      # tipoDeMaterianID -> .descripcion
        "unidad",
        "minimo",
        "existencias",
        "controlExistencias",
        "fvaloracion",
        "observaciones",
        "proveedor.nombre", # Indirecto: proveedorID -> proveedor.nombre
        # Campos específicos de rollos y Marcado CE
        "camposEspecificosRollo.gramos",
        "camposEspecificosRollo.codigoComposan",
        "camposEspecificosRollo.ancho",
        "camposEspecificosRollo.diametro",
        "camposEspecificosRollo.rollosPorCamion",
        "camposEspecificosRollo.metrosLineales",
        "camposEspecificosRollo.pesoEmbalaje",
        "camposEspecificosRollo.estandarPruebaGramaje",
        "camposEspecificosRollo.toleranciaPruebaGramaje",
        "camposEspecificosRollo.estandarPruebaLongitudinal",
        "camposEspecificosRollo.toleranciaPruebaLongitudinal",
        "camposEspecificosRollo.estandarPruebaAlargamientoLongitudinal",
        "camposEspecificosRollo.toleranciaPruebaAlargamientoLongitudinal",
        "camposEspecificosRollo.estandarPruebaTransversal",
        "camposEspecificosRollo.toleranciaPruebaTransversal",
        "camposEspecificosRollo.estandarPruebaAlargamientoTransversal",
        "camposEspecificosRollo.toleranciaPruebaAlargamientoTransversal",
        "camposEspecificosRollo.estandarPruebaCompresion",
        "camposEspecificosRollo.toleranciaPruebaCompresion",
        "camposEspecificosRollo.estandarPruebaPerforacion",
        "camposEspecificosRollo.toleranciaPruebaPerforacion",
        "camposEspecificosRollo.estandarPruebaEspesor",
        "camposEspecificosRollo.toleranciaPruebaEspesor",
        "camposEspecificosRollo.estandarPruebaPermeabilidad",
        "camposEspecificosRollo.toleranciaPruebaPermeabilidad",
        "camposEspecificosRollo.estandarPruebaPoros",
        "camposEspecificosRollo.toleranciaPruebaPoros",
        "camposEspecificosRollo.toleranciaPruebaGramajeSup",
        "camposEspecificosRollo.toleranciaPruebaLongitudinalSup",
        "camposEspecificosRollo.toleranciaPruebaAlargamientoLongitudinalSup",
        "camposEspecificosRollo.toleranciaPruebaTransversalSup",
        "camposEspecificosRollo.toleranciaPruebaAlargamientoTransversalSup",
        "camposEspecificosRollo.toleranciaPruebaCompresionSup",
        "camposEspecificosRollo.toleranciaPruebaPerforacionSup",
        "camposEspecificosRollo.toleranciaPruebaEspesorSup",
        "camposEspecificosRollo.toleranciaPruebaPermeabilidadSup",
        "camposEspecificosRollo.toleranciaPruebaPorosSup",
        "camposEspecificosRollo.fichaFabricacion",
        "camposEspecificosRollo.c",
        "camposEspecificosRollo.estandarPruebaPiramidal",
        "camposEspecificosRollo.toleranciaPruebaPiramidal",
        "camposEspecificosRollo.toleranciaPruebaPiramidalSup",
        "camposEspecificosRollo.modeloEtiqueta.modulo",  # Indirecto: .modulo
        "camposEspecificosRollo.modeloEtiqueta.funcion", # Indirecto: .funcion
        "camposEspecificosRollo.cliente.nombre",         # Indirecto: .nombre
        # Campos específicos de fibra
        "camposEspecificosBala.dtex",
        "camposEspecificosBala.corte",
        "camposEspecificosBala.color",
        "camposEspecificosBala.antiuv",
        "camposEspecificosBala.tipoDeMaterialBala.descripcion",   # Indirecto:
                                                                # .descripcion
        "camposEspecificosBala.consumoGranza",
        "camposEspecificosBala.reciclada",
        "camposEspecificosBala.gramosBolsa",
        "camposEspecificosBala.bolsasCaja",
        "camposEspecificosBala.cajasPale",
        # "cliente.nombre", -> Dupe
       )
    filas = []
    for pv in pclases.ProductoVenta.select(orderBy = "descripcion"):
        fila = build_fila(pv, columnas)
        filas.append(fila)
    for pc in pclases.ProductoCompra.select(orderBy = "descripcion"):
        fila = build_fila(pc, columnas)
        filas.append(fila)
    generate_csv(columnas, filas, "productos.csv")
    #generate_sql(columnas, filas, "Articulos")

def extract_valor_indirecto(producto, columna):
    if columna.count(".") == 1:
        tabla_intermedia, campo = columna.split(".")
        try:
            registro_intermedio = getattr(producto, tabla_intermedia)
        except AttributeError:
            valor = ''
        else:
            try:
                valor = getattr(registro_intermedio, campo)
            except AttributeError:
                assert registro_intermedio is None
                valor = ''  # registro_intermedio es None
    elif columna.count(".") > 1:
        tabla_intermedia = columna.split(".")[0]
        resto_campo = columna[columna.index(".")+1:]
        try:
            registro_intermedio = getattr(producto, tabla_intermedia)
        except AttributeError:  # Este tipo de registro no tiene esa relación
            registro_intermedio = None
        if registro_intermedio:
            valor = extract_valor_indirecto(registro_intermedio, resto_campo)
        else:
            valor = ''
    else:
        raise ValueError, "El campo «%s» no es indirecto." % campo
    return valor

def build_fila(producto, columnas):
    """
    Genera una lista con los datos del producto en el orden de las columnas
    recibidas.
    """
    res = []
    for columna in columnas:
        if "." in columna:      # Indirecto
            valor = extract_valor_indirecto(producto, columna)
        elif "/" in columna:    # Alternativo
            campo, campo_alternativo = columna.split("/")
            try:
                valor = getattr(producto, campo)
            except AttributeError:
                valor = getattr(producto, campo_alternativo)
        else:
            campo = columna
            try:
                valor = getattr(producto, campo)
            except AttributeError:
                valor = ''
        valor = clean_valor(valor)
        res.append(valor)
    return res

def clean_valor(valor):
    """
    Cambia los valores problemáticos para la guía de importación de Murano.
    Por ejemplo, cambia m² por M2.
    """
    try:
        valor = valor.strip()
    except AttributeError:  # Es un entero o un float.
        res = valor
    else:
        if valor.lower() in ("m²", "m2", "m2."):
            res = "M2"
        elif valor.lower() in ("kg", "kg."):
            res = "KG"
        elif valor.lower() in ("ud", "ud."):
            res = "UD"
        elif valor.lower() in ("m", "m.", "ml", "ml."):
            res = "M"
        elif valor.lower() == "caja":
            res = "CAJA"
        elif valor.lower() == "bobina":
            res = "BOBINA"
        else:
            res = valor
    return res

def clean_cabecera(columnas):
    """
    Elimina los puntos de los nombres de los campos para evitar problemas
    en la guía de importación de Murano.
    """
    res = []
    for c in columnas:
        cabecera = c.split(".")[-1]
        cabecera = cabecera.split("/")[0]
        res.append(cabecera)
    return res

def generate_csv(columnas, filas, nombre_fichero):
    """
    Crea un fichero CSV con las filas recibidas. La primera estará compuesta
    por los nombres de los campos (columnas).
    """
    import csv
    fout = file(nombre_fichero, "w")
    fcsv = csv.writer(fout)
    cabecera = clean_cabecera(columnas)
    fcsv.writerow(cabecera)
    fcsv.writerows(filas)
    fout.close()
