#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Procedimientos para exportar productos, clientes y proveedores a Murano.
Generan ficheros CSV, no importan nada directamente a Murano. Esos ficheros
CSV sirven como fuente para las guías de importación diseñadas por Sage.
"""

import sys
import os
import datetime
import csv
from collections import OrderedDict
RUTA_GINN = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "ginn"))
sys.path.append(RUTA_GINN)
# pylint: disable=wrong-import-position, import-error,too-many-branches
from framework import pclases
from formularios.utils import eliminar_dobles_espacios

# # ====================
# # Exportación de datos
# # ====================

# # Productos #################################################################


def exportar_productos(fdestproductos='productos.csv'):
    """
    Exporta los productos de venta y de compra a una tabla CSV.
    """
    columnas = [
        "id",                                                           # 0
        "lineaDeProduccion.nombre",     # Indirecto
        # Nos interesa intercambiar la descripcion (larga) por el nombre
        # (corto) porque Murano buscará antes por descripción que por
        # descripcion2, así que en descripcion2 meteremos el nombre (corto).
        "descripcion",                                                  # 2
        "descripcion2/nombre",                                          # 3
        "codigo",
        "minimo",                                                       # 5
        "precioPorDefecto/precioDefecto",
        # precioDefecto en productos de compra.
        "arancel",
        "prodestandar",
        "annoCertificacion",
        "dni",                                                          # 10
        "uso",
        "obsoleto",
        # Específicos de productos de compra:
        "tipoDeMaterial.descripcion",  # Indirecto:
                                       # tipoDeMaterianID -> .descripcion
        "unidad",
        "minimo",
        "existencias",
        "controlExistencias",
        "fvaloracion",
        "observaciones",
        "proveedor.nombre",  # Indirecto: proveedorID -> proveedor.nombre
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
        "camposEspecificosRollo.modeloEtiqueta.modulo",   # Indirecto: .modulo
        "camposEspecificosRollo.modeloEtiqueta.funcion",  # Indirecto: .funcion
        "camposEspecificosRollo.cliente.nombre",          # Indirecto: .nombre
        # Campos específicos de fibra
        "camposEspecificosBala.dtex",
        "camposEspecificosBala.corte",
        "camposEspecificosBala.color",
        "camposEspecificosBala.antiuv",
        "camposEspecificosBala.tipoMaterialBala.descripcion",   # Indirecto:
                                                                # .descripcion
        "camposEspecificosBala.consumoGranza",
        "camposEspecificosBala.reciclada",
        "camposEspecificosBala.gramosBolsa",
        "camposEspecificosBala.bolsasCaja",
        "camposEspecificosBala.cajasPale",
        # "cliente.nombre", -> Dupe
        # Campos artificiales. Solo existe en Murano y hay que informarlos.
        "unidadDeMedidaBasica",     # ROLLO, BALA, etc.
        "tratamientoSeries",  # Sí/No(-1,0) para indicar si llevan trazabilidad
        "grupoTallas",          # "ABC", "AB" o "".
        "tratamientoPartidas",  # Sí/No. Sí para los de trazabilidad.
        "factorConversion",     # 0 si no es fijo o la cantidad correspondiente
        # por ejemplo, cuántas cajas entran en un Kg. Solo lo usaremos en cajas
        "unidadMedidaVentas",  # Unidad en que se venderá el artículo (M2,KG..)
        "unidadMedidaPrecio",  # Indica en qué se expresa el precio: unidad
        # "Específica" para rollos, balas, cajas y BB (mandar una "E") o
        # básica para el resto (mandar una "B")
        "familia"]  # Familia a la que pertenece. Es donde se especifica el
    # precio mínimo, por tanto el producto debe pertenecer a
    # una familia al importarlo.
    filas = []
    for prodventa in pclases.ProductoVenta.select(orderBy="descripcion"):
        fila = build_fila(prodventa, columnas)
        filas.append(fila)
    for prodcompra in pclases.ProductoCompra.select(orderBy="descripcion"):
        fila = build_fila(prodcompra, columnas)
        filas.append(fila)
    columnas, filas = post_process(columnas, filas)
    generate_csv(columnas, filas, fdestproductos)


def extract_valor_indirecto(producto, columna):
    """
    Devuelve el valor de un campo "indirecto" del producto.
    Divide por el "." para saber cuál es el objeto intermedio y el campo final
    del que extraer el valor.
    """
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
        resto_campo = columna[columna.index(".") + 1:]
        try:
            registro_intermedio = getattr(producto, tabla_intermedia)
        except AttributeError:  # Este tipo de registro no tiene esa relación
            registro_intermedio = None
        if registro_intermedio:
            valor = extract_valor_indirecto(registro_intermedio, resto_campo)
        else:
            valor = ''
    else:
        raise ValueError("El campo «%s» no es indirecto." % campo)
    return valor


# pylint: disable=redefined-variable-type
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
                try:
                    valor = getattr(producto, campo_alternativo)
                except AttributeError as excepcion:
                    # DIRTY HACK: Hemos invertido los campos nombre y desc.
                    if campo_alternativo == "nombre":
                        valor = ""
                    else:
                        raise excepcion
        # Campos que no existen en ginn pero necesita Murano:
        elif columna == "unidadDeMedidaBasica":
            valor = determinar_unidad_medida_basica(producto)
        elif columna == "tratamientoSeries":
            # Sí/No(-1, 0) para indicar si llevan trazabilidad
            valor = determinar_tratamiento_series(producto)
        elif columna == "grupoTallas":
            # "ABC", "AB" o "".
            valor = determinar_grupo_tallas(producto)
        elif columna == "tratamientoPartidas":
            # Sí/No. Sí para los de trazabilidad.
            valor = determinar_tratamiento_partidas(producto)
        elif columna == "factorConversion":
            # 0 si no es fijo o la cantidad correspondiente
            # por ejemplo, cuántas cajas entran en un Kg. Solo lo
            # usaremos en cajas.
            valor = determinar_factor_conversion(producto)
        elif columna == "unidadMedidaVentas":
            # Unidad en que se venderá el artículo (M2, KG...)
            valor = determinar_unidad_medida_ventas(producto)
        elif columna == "unidadMedidaPrecio":
            # Indica en qué se expresa el precio: unidad
            # "Específica" para rollos, balas, cajas y BB (mandar una "E") o
            # básica para el resto (mandar una "B")
            valor = determinar_unidad_medida_precio(producto)
        elif columna == "familia":
            # Familia a la que pertenece. Es donde se especifica el
            # precio mínimo, por tanto el producto debe pertenecer a
            # una familia al importarlo.
            valor = determinar_familia_murano(producto)
        else:
            campo = columna
            try:
                valor = getattr(producto, campo)
            except AttributeError:
                valor = ''
        valor = muranize_valor(valor, columna, producto)
        valor = clean_valor(valor)
        res.append(valor)
    return res


def determinar_unidad_medida_basica(producto):
    """
    Devuelve ROLLO, BALA, CAJA o la unidad de medida principal del producto
    con trazabilidad, o la unidad del producto en otro caso.
    """
    if isinstance(producto, pclases.ProductoCompra):
        res = producto.unidad
    elif isinstance(producto, pclases.ProductoVenta):
        if producto.es_rollo() or producto.es_rolloC():
            res = "ROLLO"   # Geotextil
        elif producto.es_bala() or producto.es_bala_cable():
            res = "BALA"    # Fibra
        elif producto.es_bigbag():
            res = "BIGBAG"  # Fibra cemento
        elif producto.es_bolsa() or producto.es_caja():
            res = "CAJA"    # Fibra embolsada
        elif producto.es_especial():
            res = producto.unidad  # Comercializados
        elif producto.es_granza():
            res = producto.unidad  # Granza
        else:
            res = ""
    else:
        res = ""
    return res


def determinar_tratamiento_series(producto):
    """
    -1 si lleva código de trazabilidad. 0 en otro caso.
    """
    if isinstance(producto, pclases.ProductoVenta):
        res = -1
    else:
        res = 0
    return res


def determinar_grupo_tallas(producto):
    """
    "ABC" si el producto admite las 3 calidades, "AB" si solo 2 o "".
    """
    res = ""
    if isinstance(producto, pclases.ProductoVenta):
        if producto.es_rollo() or producto.es_rolloC():
            res = "ABC"
        elif producto.es_bala() or producto.es_bala_cable():
            res = "ABC"
        elif producto.es_bigbag():
            res = "AB"
        elif producto.es_bolsa() or producto.es_caja():
            res = "AB"
    return res


def determinar_tratamiento_partidas(producto):
    """
    -1 si lleva trazabilidad. 0 en otro caso.
    """
    if isinstance(producto, pclases.ProductoVenta):
        res = -1
    else:
        res = 0
    return res


def determinar_factor_conversion(producto):
    """
    Si el peso es variable por cada artículo del producto, 0. En otro caso
    el número de unidades específicas que caben en una básica. Por ejemplo,
    cuántas cajas entran en un kilogramo de fibra embolsada del producto
    concreto.
    """
    res = 0
    if isinstance(producto, pclases.ProductoVenta) and producto.es_caja():
        kilos_caja = producto.camposEspecificosBala.gramosBolsa / 1000.0
        res = 1.0 / kilos_caja
    return res


def determinar_unidad_medida_ventas(producto):
    """
    Devuelve la unidad en que se vende el artículo (Kg, m²...).
    """
    if isinstance(producto, pclases.ProductoCompra):
        res = producto.unidad
    elif isinstance(producto, pclases.ProductoVenta):
        if producto.es_rollo():
            res = "M2"  # Geotextil
        if producto.es_rolloC():
            res = "KG"   # Geotextil clase C
        elif producto.es_bala() or producto.es_bala_cable():
            res = "KG"    # Fibra
        elif producto.es_bigbag():
            res = "KG"  # Fibra cemento
        elif producto.es_bolsa() or producto.es_caja():
            res = "KG"  # Fibra embolsada
        elif producto.es_especial():
            res = producto.unidad  # Comercializados
        elif producto.es_granza():
            res = "KG"  # Granza
        else:
            res = ""
    else:
        res = ""
    return res


def determinar_unidad_medida_precio(producto):
    """
    Devuelve si el precio se expresa en la unidad de medida básica ("B") o
    específica ("E"). Será específica si el producto lleva trazabilidad,
    donde la unidad específica es Kg o m² y la básica es el rollo, caja, etc.
    pero el precio siempre va según la específica.
    """
    res = "B"
    if isinstance(producto, pclases.ProductoVenta):
        res = "E"
    return res


def determinar_familia_murano(producto):
    """
    Devuelve el código de familia del producto. En el código de familia se
    especifica el precio mínimo, por tanto es importante y relevante solo
    para productos con trazabilidad.
    """
    res = ""
    # Devuelve el mismo tipo de producto que se usa en muranize_valor para
    # el tipo de material en caso de productos de venta.
    if isinstance(producto, pclases.ProductoVenta):
        # DONE: ¿No habría que sacarlo de alguna manera de Murano? O, al
        # menos, tenerlos creados o incluso crearlos desde aquí mediante SQL.
        # No problem. Se pueden exportar los códigos de familia y crearlos
        # más tarde. No fallará al importar (Sage)
        if producto.es_rollo() or producto.es_rolloC():
            res = "GEO"     # Geotextil
        elif producto.es_bala() or producto.es_bala_cable():
            res = "FIB"     # Fibra
        elif producto.es_bigbag():
            res = "FCE"     # Fibra cemento
        elif producto.es_bolsa() or producto.es_caja():
            res = "FEM"     # Fibra embolsada
    elif isinstance(producto, pclases.ProductoCompra):
        valor = producto.tipoDeMaterial.descripcion
        if valor:
            if valor == "Aceites y lubricantes":
                res = "OIL"
            elif valor == "Comercializados":
                res = "COM"
            elif valor == "Mantenimiento":
                res = "MAN"
            elif valor == "Materia Prima":
                res = "MAP"
            elif valor == "Material adicional":
                res = "MAT"
            elif valor == "Mercancía inicial Valdemoro":
                res = "MIV"
            elif valor == "Productos comercializados":
                res = "COM"
            elif valor == "Repuestos fibra":
                res = "REF"
            elif valor == "Repuestos geotextiles":
                res = "REG"
            else:
                res = valor
    return res


# pylint: disable=redefined-variable-type, too-many-statements
def muranize_valor(valor, columna, producto):
    """
    Devuelve el valor conforme a los tipos de Murano. Se confirma el tipo de
    destino según el nombre del campo (parámetro «columna»).
    """
    # Para Murano: True -1, False 0
    if isinstance(valor, type(True)):
        if valor:
            res = -1
        else:
            res = 0
    elif columna == "id":
        # Va a ir al código de artículo de Murano. No permite duplicados, pero
        # sí letras y números.
        if isinstance(producto, pclases.ProductoVenta):
            res = "PV%d" % valor
        elif isinstance(producto, pclases.ProductoCompra):
            res = "PC%d" % valor
        else:
            res = valor
    elif columna == "controlExistencias":
        if valor:
            res = 0
        else:
            res = -1
    elif columna == "camposEspecificosBala.color":
        res = valor.upper()
    elif columna == "tipoDeMaterial.descripcion":
        # [20160207] Una vez modificado el determinar_familia_murano ya no
        # haría falta. Lo dejo para no romper la compatibilidad hacia atrás
        if valor:
            if valor == "Aceites y lubricantes":
                res = "OIL"
            elif valor == "Comercializados":
                res = "COM"
            elif valor == "Mantenimiento":
                res = "MAN"
            elif valor == "Materia Prima":
                res = "MAP"
            elif valor == "Material adicional":
                res = "MAT"
            elif valor == "Mercancía inicial Valdemoro":
                res = "MIV"
            elif valor == "Productos comercializados":
                res = "COM"
            elif valor == "Repuestos fibra":
                res = "REF"
            elif valor == "Repuestos geotextiles":
                res = "REG"
            else:
                res = valor
        else:
            if isinstance(producto, pclases.ProductoVenta):
                if producto.es_rollo() or producto.es_rolloC():
                    res = "GEO"     # Geotextil
                elif producto.es_bala() or producto.es_bala_cable():
                    res = "FIB"     # Fibra
                elif producto.es_bigbag():
                    res = "FCE"     # Fibra cemento
                elif producto.es_bolsa() or producto.es_caja():
                    res = "FEM"     # Fibra embolsada
                elif producto.es_especial():
                    res = "COM"     # Comercializados
                elif producto.es_granza():
                    res = "GRA"     # Granza
                else:
                    res = ""
    else:
        res = valor
    return res


def clean_valor(valor):
    """
    Cambia los valores problemáticos para la guía de importación de Murano.
    Por ejemplo, cambia m² por M2.
    """
    try:
        valor = eliminar_dobles_espacios(valor.strip())
    except AttributeError:  # Es un entero o un float.
        res = valor
    else:
        if valor.lower() in ("m²", "m2", "m2."):
            res = "M2"
        elif valor.lower() in ("kg", "kg.", "kg.."):
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
    index = 0
    for cabecera in columnas:
        if cabecera in ("lineaDeProduccion.nombre",
                        "tipoDeMaterial.descripcion"):
            cabecera = cabecera.replace(".", "")
        elif cabecera.startswith("camposEspecificosRollo"):
            cabecera = cabecera.replace("camposEspecificosRollo", "CER")
            cabecera = cabecera.replace(".", "")
        elif cabecera.startswith("camposEspecificosBala"):
            cabecera = cabecera.replace("camposEspecificosBala", "CEB")
            cabecera = cabecera.replace(".", "")
        elif cabecera == "nombre" and index <= 5:
            # De momento lo hago así de cutremente. El caso es cambiar
            # el nombre del producto por nombreArticulo para que no se
            # confunda con el proveedor.nombre (que se recorta también a
            # «nombre» solo). Como el nombre del artículo viene antes y seguro
            # que está en la columna 2 ó 3...
            cabecera = "nombreArticulo"
        else:
            cabecera = cabecera.split(".")[-1]
            cabecera = cabecera.split("/")[0]
        res.append(cabecera)
        index += 1
    return res


def generate_csv(columnas, filas, nombre_fichero, limpiar_cabecera=True):
    """
    Crea un fichero CSV con las filas recibidas. La primera estará compuesta
    por los nombres de los campos (columnas).
    """
    if limpiar_cabecera:
        cabecera = clean_cabecera(columnas)
    else:
        cabecera = columnas
    # Si no existe, agrega la cabecera. Si ya existía, solo agrega los datos.
    escribir_cabecera = not os.path.exists(nombre_fichero)
    fout = open(nombre_fichero, "a")
    fcsv = csv.writer(fout)
    if escribir_cabecera:
        fcsv.writerow(cabecera)
    fcsv.writerows(filas)
    fout.close()


def filtro_comercializados(descripcion):
    """
    Devuelve True si es alguno de los productos que estaban en la familia
    de Mercancía Inicial de Valdemoro (deprecated) y corresponden en realidad a
    comercializados.
    """
    res = descripcion in ("COMPO-PET-120 (100X2,20) (CT)",
                          "COMPO-PET-300 (100X2,20) (CT)"
                          "COMPOFOL / GUTTA P8 NEGRO (30X2) M2.",
                          "COMPOFOL PAC 4,3X200",
                          "COMPO-PET-200 (140X2,20) (CT)",
                          "COMPOGRID 200/40 (4,4x 100) m2",
                          "COMPOGRID 200/40 (4,4x 100) m2",
                          "COMPOCORE 8 MM (1,05 X20) M2",
                          "COMPOFOL / GUTTA P8 NEGRO (30X2) M2.",
                          "COMPOFOL PAC 2,2X32 (M2) (CT)",
                          "COMPOGRID 110/30 (3,90X100) M2",
                          "ROADRAIN 800/160 R (48ML) ML")
    return res


def post_process(columnas, _filas):
    """
    Recorre toda la tabla y la limpia de valores que no interesa volcar.
    Devuelve las mismas columnas y las filas correspondientes.
    """
    filas = []
    for fila in _filas:
        dict_fila = dict(zip(columnas, fila))
        if dict_fila['tipoDeMaterial.descripcion'] == "MIV":
            if filtro_comercializados(dict_fila["descripcion"]):
                # Los paso a la familia que realmente le corresponde.
                dict_fila['tipoDeMaterial.descripcion'] = "COM"
                fila[columnas.index("tipoDeMaterial.descripcion")] = "COM"
            else:
                continue    # Ignoro familia Mercancía Inicial de Valdemoro
        filas.append(fila)
    return columnas, filas


# # Clientes ##################################################################
def exportar_clientes():
    """
    Exporta los clientes con actividad en los últimos 2 años a una tabla CSV.
    La tabla la construye según la lista de campos del fichero que espera
    la guía de importación y toma como fuente:
    * Base de datos de ginn.
    * Fichero CSV (originalmente es un Excel) con el resto de datos.
    """
    fdestclientes = "clientesproveedores.csv"
    fdestdomicilios = "domicilios.csv"
    fdestcontactos = "contactos.csv"
    hoy = datetime.date.today()
    two_years_ago = datetime.date(day=hoy.day, month=hoy.month,
                                  year=hoy.year - 2)
    listado = create_dic_clientes(two_years_ago)
    dump(listado, fdestclientes, fdestdomicilios, fdestcontactos)


def create_dic_clientes(fecha_ultima_actividad=None):
    """
    Devuelve un diccionario cuyas claves son los ID de cliente y los valores
    son diccionarios con los campos y valores para cada cliente.
    Cada diccionario de cliente (el valor de la clave de su ID en el
    diccionario principal) lleva también una clave 'OBRAS' y otra
    'CONTACTOS' con una colección de diccionarios de sus obras y contactos
    ya tratados también con las claves que espera la guía de importación y
    los valores correspondientes.
    Si se especifica una fecha de última actividad se filtran los clientes
    e ignoran aquellos que no hayan realizado un pedido u oferta después
    de esa fecha.
    """
    fcuentas = "20160216_clientes_fjflopez.csv"
    cuentas_clientes = build_dic_cuentas(fcuentas)
    lista_campos = load_lista_campos_cliente()
    clientes = set()
    if not fecha_ultima_actividad:
        for cliente in pclases.Cliente.select():
            clientes.add(cliente.id)
    else:
        for cliente in buscar_clientes_con_actividad(pclases.Presupuesto,
                                                     fecha_ultima_actividad):
            clientes.add(cliente.id)
        for cliente in buscar_clientes_con_actividad(pclases.PedidoVenta,
                                                     fecha_ultima_actividad):
            clientes.add(cliente.id)
    res = {}
    for cid in clientes:
        cliente = pclases.Cliente.get(cid)
        res[cid] = build_dic_cliente(cliente, cuentas_clientes, lista_campos)
        res[cid]['OBRAS'] = {}
        res[cid]['CONTACTOS'] = {}
        for obra in cliente.obras:
            res[id]['OBRAS'][obra.id] = build_dic_obra(obra)
            for contacto in obra.contactos:
                res[id]['CONTACTOS'][contacto.id] = build_dic_contacto(contacto)
                # OJO: Es posible que duplique contactos si varios clientes lo
                # comparten. El ID será el mismo. Ya veremos qué hace Murano
                # en ese caso.
    return res


def load_lista_campos_cliente():
    """
    Devuelve la lista de campos en el orden específico que espera la guía
    de importación de Murano. La lista de campos es según la nomenclatura
    de Murano. La correspondencia con los campos de ginn la da el propio
    diccionario ordenado. Si un mismo campo se corresponde con 2 ó 3 de los
    de Murano es porque hay que separar el valor entre esos campos de Murano
    de ser necesario.
    """
    res = OrderedDict()
    res['CodigoEmpresa'] = None      # Sin correspondencia en ginn.
    res['ClienteOProveedor'] = None  # Se determina después.
    res['CodigoClienteProveedor'] = 'id'
    res['TarifaPrecio'] = 'tarifaID'
    res['Telefono'] = 'telefono'
    res['Nombre'] = 'nombre'
    res['CIFDNI'] = 'cif'
    res['Domicilio'] = 'direccion'
    res['Nacion'] = 'pais'
    res['Municipio'] = 'ciudad'
    res['Provincia'] = 'provincia'
    res['CodigoPostal'] = 'cp'
    res['CodigoIva'] = 'iva'
    res['RazonSocial'] = 'nombref'
    res['email1'] = 'email'
    res['email2'] = 'email'
    res['nombre1'] = 'contacto'
    res['nombre2'] = 'contacto'
    res['Comentarios'] = 'observaciones'
    res['CodigoCondiciones'] = 'vencimientos'
    res['CodigoTipoEfecto'] = 'documentodepago'
    res['DiasFijos1'] = 'diadepago'
    res['DiasFijos2'] = 'diadepago'
    res['DiasFijos3'] = 'diadepago'
    res['BloqueoAlbaran'] = 'inhabilitado'
    res['GEO_EnviaCorreoAlbaran'] = 'enviarCorreoAlbaran'
    res['GEO_EnviaCorreoFactura'] = 'enviarCorreoFactura'
    res['GEO_EnviaCorreoPacking'] = 'enviarCorreoPacking'
    res['Fax'] = 'fax'
    res['RemesaHabitual'] = 'cuentaOrigenID'
    res['GEO_RiesgoAseguradora'] = 'riesgoAsegurado'
    res['RiesgoMaximo'] = 'riesgoConcedido'
    res['CopiasFactura'] = 'copiasFactura'
    res['CodigoTipoClienteLC'] = 'tipoDeClienteID'
    res['GEO_RequiereValidacion'] = 'validacionManual'
    res['CodigoCuenta'] = None
    res['CodigoSeccion'] = None
    return res


def load_lista_campos_domicilios():
    """
    Devuelve un diccionario ordenado con la lista de campos que espera
    recibir Murano en la guía de importación de domicilios (obras).
    """
    res = OrderedDict()
    res['CP'] = None
    res['CodigoEmpresa'] = None
    res['TipoDomicilio'] = None
    res['CodigoCliente'] = 'clientes'  # FIXME: Ya veré cómo discernimos cuál
    res['NumeroDomicilio'] = None
    # TODO: PORASQUI
    res['Nombre'] = ''
    res[''] = ''
    res[''] = ''
    res[''] = ''
    res[''] = ''
    res[''] = ''
    res[''] = ''
    return res


def load_lista_campos_contactos():
    """
    Devuelve un diccionario ordenado con la lista de campos que espera
    recibir Murano en la guía de importación de contactos.
    """
    res = OrderedDict()
    return res

def build_cabecera(listado, orden_campos=()):
    """
    Devuelve una lista de campos del listado.
    """
    campos_tratados = []
    # Si el listado está vacío, petará.
    campos = listado[listado.keys()[0]].keys()
    res = []
    for campo in orden_campos:
        if campo not in campos:
            raise ValueError("El campo %s no existe en el diccionario de "
                             "clientes." % campo)
            # ¿TYPO en el nombre del campo?
        res.append(campo)
        campos_tratados.append(campo)
    # El resto de campos del diccionario que no se especificaron en el orden.
    for campo in campos:
        if campo in campos_tratados:
            continue
        res.append(campo)
    return res


def build_fila_cliente(dic_cliente, campos):
    """
    Devuelve una lista de valores según el orden de campos especificado.
    """
    res = []
    for campo in campos:
        res.append(dic_cliente[campo])
    return res


def dump(listado, fdest):
    """
    Convierte el diccionaro «listado» en filas para alimentar un nuevo CSV
    que incluye los nombres de los campos como cabecera de columnas.
    """
    cabecera = build_cabecera(listado, orden_campos)
    filas = []
    for cid in listado:
        fila = build_fila_cliente(listado[cid], cabecera)
        filas.append(fila)
    generate_csv(cabecera, filas, fdest, limpiar_cabecera=False)


def parse(fdest):
    """
    Abre el fichero CSV y devuelve un diccionario de clientes con el ID como
    clave y un diccionario de campos como valores.
    """
    res = {}
    fin = open(fdest, "r")
    reader = csv.reader(fin)
    cabecera = None
    for fila in reader:
        if not cabecera:
            cabecera = fila     # Solo la primera vez.
        else:
            dic_cliente = dict(zip(cabecera, fila))
            res[dic_cliente["id"]] = dic_cliente
    fin.close()
    return res


def update_listado(listado, pclase=pclases.Cliente):
    """
    En el propio diccionario de clientes recibido actualiza los valores
    según los actuales de los clientes de la base de datos. Si algún
    cliente no está presente en el diccionario, pero se ha creado con
    posterioridad, lo incluye **aunque no haya tenido actividad según el
    criterio con que se construye la lista inicial**.
    Estos nuevos clientes puede que sean tan nuevos que ni siquiera ha
    dado tiempo a que hagan un pedido, por eso se incluyen.
    Para ver si un cliente es nuevo, se mira su ID. Debe ser posterior al
    mayor del diccionario.
    """
    if listado:     # Si no hay listado previo...
        ultimo_id_csv = max([int(cid) for cid in listado.keys()])
        nuevos = pclase.select(pclase.q.id > ultimo_id_csv)
        # Respeto los campos del CSV actual, que ya están en uno (cualquiera)
        # de los objetos (clientes/proveedores) del diccionario.
        campos = listado[listado.keys()[0]].keys()
        # Repaso los existentes
        for cid in listado:
            objeto = pclase.get(cid)
            for campo in campos:
                valor_db = getattr(objeto, campo, None)
                valor_csv = listado[cid][campo]
                # Sobreescribo el valor del Excel de contabilidad solo si el
                # valor de la base de datos no es nulo. Asumo que la BD siempre
                # está más actualizada excepto en los campos nuevos adicionales
                # de cuenta contable y demás. (CWT)
                if valor_db != valor_csv and valor_db:
                    listado[cid][campo] = valor_db
        # Y agrego los nuevos
        for nuevo in nuevos:
            listado[nuevo.id] = {}
            for campo in campos:
                listado[nuevo.id][campo] = getattr(objeto, campo, None)


def buscar_clientes_con_actividad(pclase, fecha):
    """
    Devuelve una lista de ID de clientes con algún objeto en la tabla
    representada por pclase posterior a la fecha indicada.
    """
    for objeto in pclase.select():
        if objeto.fecha >= fecha:
            if objeto.cliente:
                yield objeto.cliente


def build_dic_cliente(cliente):
    """
    Devuelve un diccionario que representa a un cliente con los nombres de
    campo como clave y los datos del cliente como valores.
    """
    return cliente.sqlmeta.asDict()


# # Proveedores ###############################################################
def exportar_proveedores():
    """
    Exporta los clientes con actividad en los últimos 2 años a una tabla CSV.
    Esta tabla posteriormente se procesa para completar información.
    Al realizar cada importación primero se trata de leer el fichero CSV,
    se construye un nuevo volcado combinando los datos de la base de datos
    y el CSV y se vuelve a volcar el fichero CSV.
    """
    fdest = "proveedores.csv"
    # Me aseguro que el orden es siempre el mismo porque Murano es muy
    # quisuilloso al respecto.
    proveedor = pclases.Proveedor.select()[0]
    cols_extra = ["cuenta contable", "sección", "departamento"]
    orden_campos = ["id"] + [f.name for f in proveedor.sqlmeta.columnList]
    orden_campos += cols_extra
    if os.path.exists(fdest):
        listado = parse(fdest)
        update_listado(listado)
    else:
        hoy = datetime.date.today()
        two_years_ago = datetime.date(day=hoy.day, month=hoy.month,
                                      year=hoy.year - 2)
        listado = create_dic_inicial_proveedores(cols_extra, two_years_ago)
    dump(listado, fdest, orden_campos)


def create_dic_inicial_proveedores(cols_extra,
                                   fecha_ultima_actividad=None):
    """
    Devuelve un diccionario cuyas claves son los ID de proveedor y los valores
    son diccionarios con los campos y valores para cada proveedor.
    Agrega campos adicionales que deben ir al CSV y no están presentes en
    la base de datos.
    Si se especifica una fecha de última actividad se filtran los proveedores
    e ignoran aquellos que no hayan realizado un pedido u oferta después
    de esa fecha.
    """
    proveedores = set()
    if not fecha_ultima_actividad:
        for proveedor in pclases.Proveedor.select():
            proveedores.add(proveedor.id)
    else:
        for proveedor in buscar_proveedores_activos(pclases.PedidoCompra,
                                                    fecha_ultima_actividad):
            proveedores.add(proveedor.id)
        for proveedor in buscar_proveedores_activos(pclases.FacturaCompra,
                                                    fecha_ultima_actividad):
            proveedores.add(proveedor.id)
    res = {}
    for cid in proveedores:
        proveedor = pclases.Proveedor.get(cid)
        # Me vale la función de clientes para el diccionario del proveedor.
        res[cid] = build_dic_cliente(proveedor)
        for col in cols_extra:
            res[cid][col] = None
    return res


def buscar_proveedores_activos(pclase, fecha):
    """
    Devuelve una lista de ID de clientes con algún objeto en la tabla
    representada por pclase posterior a la fecha indicada.
    """
    for objeto in pclase.select():
        # Sorprendentemente hay pedidos o facturas sin fecha.
        if objeto.fecha and objeto.fecha >= fecha:
            if objeto.proveedor:
                yield objeto.proveedor
