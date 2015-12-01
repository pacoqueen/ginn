#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from connection import Connection, DEBUG, VERBOSE

try:
    import win32com.client
except ImportError:
    LCOEM = False
else:
    LCOEM = True

CODEMPRESA = 9999   # Empresa de pruebas. Cambiar por la 10200 en producción.

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

def buscar_codigo_producto(productoVenta):
    """
    Busca el ID del producto en Murano para la descripción del producto
    recibido.
    """
    res = consulta_producto(productoVenta.descripcion)
    try:
        codarticulo = res[0]['CodigoArticulo']
    except TypeError, e:
        # TODO: Ver cómo tratar los errores de cuando el producto no existe en Murano. ¿Se puede dar el caso? Todos se darán de alta en Murano y se buscarán ahí cuando se creen los artículos en los partes de producción. Debería exisitir. **Pero se podría dar el caso de que el nombre haya cambiado.**
        print productoVenta.descripcion
        raise e
    return codarticulo

def buscar_codigo_almacen(self):
    """
    Devuelve **el primer** almacén de la empresa configurada.
    """
    c = Connection()
    filas = c.run_sql("""SELECT CodigoAlmacen
        FROM %s.dbo.Almacenes
        WHERE CodigoEmpresa = %d
        ORDER BY CodigoAlmacen;""" % (c.get_database(), CODEMPRESA))
    try:
        codalmacen = filas[0]['CodigoAlmacen']
    except Exception, e:
        if not DEBUG:
            raise e
        else:
            return 'CEN'
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

def buscar_factor_conversion(self):
    # TODO
    return 1

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


def create_bala(bala):
    """
    Crea una bala en las tablas temporales de Murano.
    Recibe un objeto bala de ginn.
    """
    c = Connection()
    database = c.get_database()
    today = datetime.datetime.today()
    ejercicio = today.year
    periodo = today.month
    fecha = today.strftime("%Y-%m-%d %H:%M:%S")
    documento = int(today.strftime("%Y%m%d"))
    articulo = bala.articulo
    codigo_articulo = buscar_codigo_producto(articulo.productoVenta)
    codigo_almacen = buscar_codigo_almacen(articulo.almacen)
    partida = bala.lote.codigo
    grupo_talla = 1    # TODO: ¿Seguro que solo hay un grupo de talla? Creo que hemos creado alguno más. 1 para A, B y C, 2 para A, B (sin C), etc.
    codigo_talla = articulo.get_str_calidad()
    tipo_movimiento = 1     # 1 = entrada, 2 = salida.
    unidades = 1    # En dimensión base: 1 bala.
    unidad_medida = "KG"
    precio = 0.0    # TODO: Hasta que se defina bien el precio coste por familia y cómo actualizarlo mensialmente.
    importe = unidades * precio
    factor_conversion = buscar_factor_conversion(articulo.productoVenta)
    unidades2 = unidades * factor_conversion
    comentario = ("Bala ginn: [%s]" % bala.get_info())[:40]
    ubicacion = "Almac. de fibra."[:15]
    origen_movimiento = "F" # E = Entrada de Stock (entrada directa), 
                            # F (fabricación), I (inventario), 
                            # M (rechazo fabricación), S (Salida stock)
    numero_serie_lc = bala.codigo
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

def create_bigabag(bigbag):
    """
    Crea un bigbag en Murano a partir de la información del bigbag en ginn.
    """
    c = Connection()
    database = c.get_database()
    today = datetime.datetime.today()
    ejercicio = today.year
    periodo = today.month
    fecha = today.strftime("%Y-%m-%d %H:%M:%S")
    documento = int(today.strftime("%Y%m%d"))
    articulo = bigbag.articulo
    codigo_articulo = buscar_codigo_producto(articulo.productoVenta)
    codigo_almacen = buscar_codigo_almacen(articulo.almacen)
    partida = bigbag.loteCem.codigo
    grupo_talla = 1    # TODO: ¿Seguro que solo hay un grupo de talla? Creo que hemos creado alguno más. 1 para A, B y C, 2 para A, B (sin C), etc.
    codigo_talla = articulo.get_str_calidad()
    tipo_movimiento = 1     # 1 = entrada, 2 = salida.
    unidades = 1    # En dimensión base: 1 bigbag.
    unidad_medida = "KG"
    precio = 0.0    # TODO: Hasta que se defina bien el precio coste por familia y cómo actualizarlo mensialmente.
    importe = unidades * precio
    factor_conversion = buscar_factor_conversion(articulo.productoVenta)
    unidades2 = unidades * factor_conversion
    comentario = ("Bigbag ginn: [%s]" % bigbag.get_info())[:40]
    ubicacion = "Almac. de fibra."[:15]
    origen_movimiento = "F" # E = Entrada de Stock (entrada directa), 
                            # F (fabricación), I (inventario), 
                            # M (rechazo fabricación), S (Salida stock)
    numero_serie_lc = bigbag.codigo
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

def create_rollo(rollo):
    """
    Crea un rollo en Murano a partir de la información del rollo en ginn.
    """
    c = Connection()
    database = c.get_database()
    today = datetime.datetime.today()
    ejercicio = today.year
    periodo = today.month
    fecha = today.strftime("%Y-%m-%d %H:%M:%S")
    documento = int(today.strftime("%Y%m%d"))
    articulo = rollo.articulo
    codigo_articulo = buscar_codigo_producto(articulo.productoVenta)
    codigo_almacen = buscar_codigo_almacen(articulo.almacen)
    partida = rollo.partida.codigo
    grupo_talla = 1    # TODO: ¿Seguro que solo hay un grupo de talla? Creo que hemos creado alguno más. 1 para A, B y C, 2 para A, B (sin C), etc.
    codigo_talla = articulo.get_str_calidad()
    tipo_movimiento = 1     # 1 = entrada, 2 = salida.
    unidades = 1    # En dimensión base: 1 rollo.
    unidad_medida = "M2"
    precio = 0.0    # TODO: Hasta que se defina bien el precio coste por familia y cómo actualizarlo mensialmente.
    importe = unidades * precio
    factor_conversion = buscar_factor_conversion(articulo.productoVenta)
    unidades2 = unidades * factor_conversion
    comentario = ("Rollo ginn: [%s]" % rollo.get_info())[:40]
    ubicacion = "Almac. de geotextiles."[:15]
    origen_movimiento = "F" # E = Entrada de Stock (entrada directa), 
                            # F (fabricación), I (inventario), 
                            # M (rechazo fabricación), S (Salida stock)
    numero_serie_lc = rollo.codigo
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

def create_caja(caja):
    """
    Crea una caja en Murano a partir de la información del objeto caja en ginn.
    """
    c = Connection()
    database = c.get_database()
    today = datetime.datetime.today()
    ejercicio = today.year
    periodo = today.month
    fecha = today.strftime("%Y-%m-%d %H:%M:%S")
    documento = int(today.strftime("%Y%m%d"))
    articulo = caja.articulo
    codigo_articulo = buscar_codigo_producto(articulo.productoVenta)
    codigo_almacen = buscar_codigo_almacen(articulo.almacen)
    partida = caja.partidaCem.codigo
    grupo_talla = 1    # TODO: ¿Seguro que solo hay un grupo de talla? Creo que hemos creado alguno más. 1 para A, B y C, 2 para A, B (sin C), etc.
    codigo_talla = articulo.get_str_calidad()
    tipo_movimiento = 1     # 1 = entrada, 2 = salida.
    unidades = 1    # En dimensión base: 1 caja.
    unidad_medida = "M2"
    precio = 0.0    # TODO: Hasta que se defina bien el precio coste por familia y cómo actualizarlo mensialmente.
    importe = unidades * precio
    factor_conversion = buscar_factor_conversion(articulo.productoVenta)
    unidades2 = unidades * factor_conversion
    comentario = ("Caja ginn: [%s]" % caja.get_info())[:40]
    ubicacion = "Almac. de fibra embolsada."[:15]
    origen_movimiento = "F" # E = Entrada de Stock (entrada directa), 
                            # F (fabricación), I (inventario), 
                            # M (rechazo fabricación), S (Salida stock)
    numero_serie_lc = caja.codigo
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

def create_pale(pale):
    """
    Crea un palé con todas sus cajas en Murano a partir del palé de ginn.
    """
    c = Connection()
    database = c.get_database()
    today = datetime.datetime.today()
    ejercicio = today.year
    periodo = today.month
    fecha = today.strftime("%Y-%m-%d %H:%M:%S")
    documento = int(today.strftime("%Y%m%d"))
    articulo = pale.articulo
    codigo_articulo = buscar_codigo_producto(articulo.productoVenta)
    codigo_almacen = buscar_codigo_almacen(articulo.almacen)
    partida = pale.partidaCem.codigo
    grupo_talla = 1    # TODO: ¿Seguro que solo hay un grupo de talla? Creo que hemos creado alguno más. 1 para A, B y C, 2 para A, B (sin C), etc.
    codigo_talla = articulo.get_str_calidad()
    tipo_movimiento = 1     # 1 = entrada, 2 = salida.
    unidades = 1    # En dimensión base: 1 pale.
    unidad_medida = "KG"
    precio = 0.0    # TODO: Hasta que se defina bien el precio coste por familia y cómo actualizarlo mensialmente.
    importe = unidades * precio
    factor_conversion = buscar_factor_conversion(articulo.productoVenta)
    unidades2 = unidades * factor_conversion
    comentario = ("Palé ginn: [%s]" % pale.get_info())[:40]
    ubicacion = "Almac. de fibra."[:15]
    origen_movimiento = "F" # E = Entrada de Stock (entrada directa), 
                            # F (fabricación), I (inventario), 
                            # M (rechazo fabricación), S (Salida stock)
    numero_serie_lc = pale.codigo
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
                                pale.codigo  # Código palé. Varchar NOT NULL
                               )
    c.run_sql(sql_movserie)
    for caja in pale.cajas:
        # TODO: Check que compruebe si la caja ya existía para no duplicarlas.
        create_caja(caja)
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

def consulta_producto(nombre = None):
    """
    Busca un producto por nombre.
    Devuelve una lista de productos coincidentes.
    """
    c = Connection()
    sql = "SELECT * FROM %s.dbo.Articulos WHERE " % (c.get_database())
    where = r"DescripcionArticulo = '%s';" % (nombre)
    sql += where
    res = c.run_sql(sql)
    return res

def update_calidad(articulo, calidad):
    """
    Cambia la calidad del artículo en Murano a la recibida. Debe ser A, B o C.
    """
    # TODO: ¿En qué tabla están exactamente los números de serie para buscar por código de trazabildiad?
    if calidad not in "aAbBcC":
        raise ValueError, "El parámetro calidad debe ser A, B o C."

def create_articulo(articulo, producto = None):
    """
    Crea un artículo nuevo en Murano con el producto recibido. Si no se
    recibe ninguno, se usa el que tenga asociado en ginn. Si se recibe un
    objeto producto, se ignora el actual del artículo, se reemplaza en ginn
    por el recibido y se da de alta así en Murano.
    """
    if articulo.es_bala():
        create_bala(articulo.bala)
    elif articulo.es_bigbag():
        create_bigabag(articulo.bigbag)
    elif articulo.es_caja():
        create_caja(articulo.caja)
    elif articulo.es_rollo():
        create_rollo(articulo.rollo)
    elif articulo.es_rolloC():
        pass # TODO: PORASQUI: Voy a tener que cambiar los create_* para dar soporte a los rollos C, balas C y demás. Y también para aceptar cantidad negativa.
    else:
        raise ValueError, "El artículo %s no es bala, bigbag, caja ni rollo."%(
                articulo.puid)

def update_producto(articulo, producto):
    """
    Cambia el artículo recibido al producto indicado.
    """
    delete_articulo(articulo)
    create_articulo(articulo, producto)

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
    res = burano.EjecutaOEM(operacion, guid_proceso, 0, 1, 0)
    # Después de cada proceso hay que invocar al cálculo que acumula los
    # campos personalizados:
    burano.EjecutaScript("AcumularCamposNuevosSeries",
                         "Label:=Inicio, idProcesoIME:='%s'" % guid_proceso)
