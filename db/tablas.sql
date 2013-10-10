--#############################################################################
-- Copyright (C) 2005-2013 Francisco José Rodríguez Bogado,                   #
--                         Diego Muñoz Escalante.                             #
-- (pacoqueen@users.sourceforge.net, escalant3@users.sourceforge.net)         #
--                                                                            #
-- This file is part of GeotexInn.                                            #
--                                                                            #
-- GeotexInn is free software; you can redistribute it and/or modify          #
-- it under the terms of the GNU General Public License as published by       #
-- the Free Software Foundation; either version 2 of the License, or          #
-- (at your option) any later version.                                        #
--                                                                            #
-- GeotexInn is distributed in the hope that it will be useful,               #
-- but WITHOUT ANY WARRANTY; without even the implied warranty of             #
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
-- GNU General Public License for more details.                               #
--                                                                            #
-- You should have received a copy of the GNU General Public License          #
-- along with GeotexInn; if not, write to the Free Software                   #
-- Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA #
--#############################################################################

-------------------------------------------------------------
-- Script de creación de tablas para la aplicación Geotex-INN
-------------------------------------------------------------
-- Uso:
-- createdb ginn
-- psql -U geotexan -W -h melchor ginn < BD/tablas.sql 2>&1 | grep ERROR
-- Con el usuario geotexan ya creado, por supuesto.
-------------------------------------------------------------------------------
-- 26/02/2007: OJO: Con las nuevas tablas de cuenta origen y cuenta destino
-- añadidas al servidor "en caliente", la restauración de las copias hechas
-- con pg_dump ya no son tan limpias. Hay que cambiar el orden de inserción
-- de registros en dump_datos.sql antes de ejecutar el
-- ./create_and_populate_bd.sh
-------------------------------------------------------------------------------

---- OPERADORES ----

CREATE FUNCTION xor(BOOL, BOOL) RETURNS BOOL AS
    'SELECT ($1 AND NOT $2) OR (NOT $1 AND $2);'
    LANGUAGE 'sql';

-- En realidad creo que <> se comporta igual que XOR. En algunas versiones de
-- PostgreSQL incluso hay un operador != que equivale al XOR lógico también.
-- De cualquier forma, me curo en salud y me construyo el mío propio.
CREATE OPERATOR +^ (PROCEDURE='xor', LEFTARG = BOOL, RIGHTARG = BOOL);



---- TABLAS ------

------------------------------------------------------------------------------
-- Tabla de formas de pago/cobro.                                           --
-- Ya iba siendo hora de unificarlas. De momento se usará en pedidos de     --
-- venta. Después iré cambiando en el resto de tablas.                      --
-- NEW! 13/11/2012                                                          --
-- Formas de pago habituales:                                               --
-- * Contado                                                                --
-- * Transferencia bancaria                                                 --
-- * Pagaré a la orden                                                      --
-- * Pagaré no a la orden                                                   --
-- * Confirming                                                             --
-- * Cheque                                                                 --
-- * Carta de crédito                                                       --
-- Periodos:                                                                --
-- 30, 60, 90, 120, 150, 180, 210, 240                                      --
------------------------------------------------------------------------------
CREATE TABLE documento_de_pago(
    id SERIAL PRIMARY KEY, 
    documento TEXT DEFAULT ''
);

CREATE TABLE forma_de_pago(
    id SERIAL PRIMARY KEY, 
    documento_de_pago_id INT REFERENCES documento_de_pago, 
    plazo INT DEFAULT 120, 
    activa BOOLEAN DEFAULT TRUE -- NEW! 21/11/2012 Para no seguir usando 
                                -- formas de pago obsoletas.
);

-------------
-- Tarifas --
-------------
CREATE TABLE tarifa(
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    observaciones TEXT DEFAULT '',
    periodo_validez_ini DATE DEFAULT NULL,
        -- Fechas de validez de la tarifa. NULL significa que
    periodo_validez_fin DATE DEFAULT NULL       -- no tiene caducidad.
);

--------------------------
-- Tipos de proveedores --
--------------------------
CREATE TABLE tipo_de_proveedor(
    id SERIAL PRIMARY KEY, 
    descripcion TEXT
);

---------------------
-- Tabla proveedor --
---------------------
CREATE TABLE proveedor(
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    cif TEXT DEFAULT '',
    direccion TEXT DEFAULT '',
    pais TEXT DEFAULT '',
    ciudad TEXT DEFAULT '',
    provincia TEXT DEFAULT '',
    cp TEXT DEFAULT '',
    telefono TEXT DEFAULT '',
    fax TEXT DEFAULT '',
    contacto TEXT DEFAULT '',
    observaciones TEXT DEFAULT '',
    -- Segunda dirección
    direccionfacturacion TEXT DEFAULT '',
    paisfacturacion TEXT DEFAULT '',
    ciudadfacturacion TEXT DEFAULT '',
    provinciafacturacion TEXT DEFAULT '',
    cpfacturacion TEXT DEFAULT '',
    email TEXT DEFAULT '',
    formadepago TEXT DEFAULT '',    -- Obsoleto. Se usa el campo "vencimiento".
    documentodepago TEXT DEFAULT '',
    vencimiento TEXT DEFAULT '',    -- En principio va igual que los
                                    -- vencimientos de clientes.
    diadepago TEXT DEFAULT '',  -- El día en que se harán los pagos realmente
                                -- (independientemente de lo que marque
                                -- el vencimiento, el pago se puede hacer días
                                -- antes o días después, en un día del
                                -- mes fijo) P.ej: El vencimiento cumple el 15
                                -- de enero pero siempre se le paga al
                                -- proveedor los días 5 de cada mes.
                                -- De momento es texto (aunque en teoría sería
                                -- un INT) para contemplar la posibilidad
                                -- de meter días concatenados con comas -por
                                -- ejemplo- y así expresar que se le
                                -- pagan -por ejemplo one more time- los días
                                -- 5 y 20 de cada mes.
    correoe TEXT DEFAULT '',    -- NEW! 26/09/2006
    web TEXT DEFAULT '',        -- NEW! 26/09/2006
    banco TEXT DEFAULT '',      -- NEW! 04/12/2006
    swif TEXT DEFAULT '',       -- NEW! 04/12/2006. En realidad es SWIFT, pero
                                -- ya sabes cómo es quien tú sabes en esto de
                                -- inventarse nombres...
    iban TEXT DEFAULT '',       -- NEW! 04/12/2006
    cuenta TEXT DEFAULT '',     -- NEW! 04/12/2006
    inhabilitado BOOLEAN DEFAULT FALSE, -- NEW! 05/12/06
    motivo TEXT DEFAULT '',     -- NEW! 05/12/06. Si está inhabilitado no se
                                -- permitirá hacerle más pedidos de
                                -- compra.(CWT)
    iva FLOAT DEFAULT 0.21,     -- NEW! 30/01/07. Iva por defecto del
                                -- proveedor (21% a no ser que sea extranjero).
    nombre_banco TEXT DEFAULT '',   -- NEW! 07/02/2007. CWT: Nombre del
                                    -- banco. No es lo mismo que "banco"
                                    -- ¿Porcuá? pues no lo sé.
    tipo_de_proveedor_id INT REFERENCES tipo_de_proveedor DEFAULT NULL
);

--------------------
-- Transportistas --
--------------------
CREATE TABLE transportista(
    id SERIAL PRIMARY KEY,
    agencia TEXT DEFAULT '',
    nombre TEXT DEFAULT '',
    DNI TEXT,
    telefono TEXT DEFAULT '',
    matricula TEXT DEFAULT ''
);

--------------
-- Destinos --
-------------------
-- NEW! 23/11/06 --
-------------------
CREATE TABLE destino(
    id SERIAL PRIMARY KEY,
    nombre TEXT DEFAULT '',
    direccion TEXT DEFAULT '',
    cp TEXT DEFAULT '',
    ciudad TEXT DEFAULT '',
    telefono TEXT DEFAULT '',
    pais TEXT DEFAULT ''
--    observaciones TEXT DEFAULT ''
);

-----------------------
-- Pedidos de compra --
-----------------------
CREATE TABLE pedido_compra(
    id SERIAL PRIMARY KEY,
    proveedor_id INT REFERENCES proveedor,   -- Id del proveedor del pedido.
    fecha DATE DEFAULT CURRENT_DATE,
    numpedido TEXT,
    iva FLOAT DEFAULT 0.21,
    descuento FLOAT DEFAULT 0.0, -- Descuento en fracción de 1: 23,44% = 0.2344
    entregas TEXT DEFAULT '',    -- Texto libre para indicar entregas.
    forma_de_pago TEXT DEFAULT '',   -- NEW! 26/09/06
    observaciones TEXT DEFAULT '',   -- NEW! 26/09/06
    bloqueado BOOLEAN DEFAULT FALSE, -- NEW! 08/10/06
    cerrado BOOLEAN DEFAULT FALSE,   -- NEW! 27/11/06. Si el pedido está
                                     -- cerrado no admitirá más albaranes de
                                     -- entrada relacionados ni aparecerá en
                                     -- el listado de pendientes de recibir.
    direccion_entrega0 TEXT DEFAULT '',  -- NEW! 27/02/2009
    direccion_entrega1 TEXT DEFAULT '',  -- NEW! 27/02/2009
    direccion_entrega2 TEXT DEFAULT '',  -- NEW! 27/02/2009
    responsable0 TEXT DEFAULT '',        -- NEW! 27/02/2009
    responsable1 TEXT DEFAULT '',        -- NEW! 27/02/2009
    portes0 TEXT DEFAULT '',             -- NEW! 27/02/2009
    portes1 TEXT DEFAULT '',             -- NEW! 27/02/2009
    observaciones0 TEXT DEFAULT '',     -- NEW! 26/05/2009 3 líneas que van a 
    observaciones1 TEXT DEFAULT '',     -- NEW! 26/05/2009 llevar un texto 
    observaciones2 TEXT DEFAULT ''      -- NEW! 26/05/2009 "casi" fijo. 
);

----------------------
-- Tipo de material --
----------------------
CREATE TABLE tipo_de_material(
    id SERIAL PRIMARY KEY,
    descripcion TEXT
);

-------------------------
-- Productos de compra --
-------------------------
CREATE TABLE producto_compra(
    id SERIAL PRIMARY KEY,
    tipo_de_material_id INT REFERENCES tipo_de_material,
    descripcion TEXT,
    codigo TEXT,
    unidad TEXT DEFAULT 'ud.',
    minimo FLOAT DEFAULT 0.0,
    existencias FLOAT DEFAULT 0.0,
    precio_defecto FLOAT DEFAULT 0.0,
    control_existencias BOOLEAN DEFAULT TRUE,
        -- Si False el programa no controlará las existencias de este producto:
        -- * No mostrará existencias en ventana.
        -- * No mostrará el producto en el listado.
        -- * No permitirá que se añada a la formulación ni se relacione
        --   con consumos.
        -- * No aumentará existencias cuando se le agregue a un albarán de
        --   entrada.
    fvaloracion TEXT DEFAULT '',
        -- Función de evaluación para valorar las existencias en almacén.
        -- Si '' se usa el precio medio (por defecto).
    observaciones TEXT DEFAULT '', 
    obsoleto BOOLEAN DEFAULT FALSE, -- NEW! 13/01/2010. Si True, no se tendrá 
                                    -- en cuenta para listados de existencias 
                                    -- y demás.
    proveedor_id INT REFERENCES proveedor DEFAULT NULL  -- NEW! 6/09/2011. 
                                    -- Proveedor por defecto para cuando 
                                    -- todavía no se haya hecho ningún pedido.
);

---------------------------------------------
-- Formulaciones para descuento automático --
-- de material adicional.                  --
---------------------------------------------
CREATE TABLE formulacion(
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    observaciones TEXT
);

--------------------------
-- Consumos adicionales --
--------------------------
CREATE TABLE consumo_adicional(
    id SERIAL PRIMARY KEY,
    producto_compra_id INT REFERENCES producto_compra,
    formulacion_id INT REFERENCES formulacion,
    nombre TEXT,
    cantidad FLOAT,
    unidad TEXT
);

-------------------------
-- Línea de producción --
-------------------------
CREATE TABLE linea_de_produccion(
    id SERIAL PRIMARY KEY,
    formulacion_id INT REFERENCES formulacion DEFAULT NULL,
    nombre TEXT,
    descripcion TEXT,
    observaciones TEXT DEFAULT '', 
    precio_minimo FLOAT DEFAULT NULL    -- NEW! 10/06/2013 Precio mínimo por 
                                -- kilo al que se pueden vender los productos.
        -- ALTER TABLE linea_de_produccion ADD COLUMN precio_minimo FLOAT DEFAULT NULL; UPDATE linea_de_produccion SET precio_minimo = NULL;
);

----------------------------
-- Tipos de material bala --
----------------------------
CREATE TABLE tipo_material_bala(
    id SERIAL PRIMARY KEY,
    descripcion TEXT,
    codigo TEXT
);

-------------------------------------------------
-- Tabla de cuentas origen para transferencias --
-------------------------------------------------
-- No necesita relacionarse con ningún         --
-- registro como ocurre con las cuentas        --
-- destino porque pertenecen a la propia       --
-- empresa, que siempre es la misma (el primer --
-- -y único- registro de la tabla              --
-- datos_de_la_empresa).                       --
-------------------------------------------------
-- NEW! 21/02/07 --
-------------------
CREATE TABLE cuenta_origen(
    id SERIAL PRIMARY KEY,
    nombre TEXT DEFAULT '',
    banco TEXT DEFAULT '',
    ccc TEXT DEFAULT '',
    observaciones TEXT DEFAULT '',
    contacto TEXT DEFAULT '',     -- NEW! 27/02/2007. Persona de contacto en
                                  -- el banco para los faxes de transferencia.
    fax TEXT DEFAULT '',          -- NEW! 27/02/2007.
    telefono TEXT DEFAULT ''      -- NEW! 27/02/2007.
);

------------------------------------------------
-- Contador de números de factura por cliente --
------------------------------------------------
CREATE TABLE contador(
    id SERIAL PRIMARY KEY,
    prefijo TEXT DEFAULT '',
    sufijo TEXT DEFAULT '',
    contador INT8
);

----------------------
-- Tipos de cliente --
----------------------
CREATE TABLE tipo_de_cliente(
    id SERIAL PRIMARY KEY, 
    descripcion TEXT
);

--------------
-- Clientes --
--------------
CREATE TABLE cliente(
    id SERIAL PRIMARY KEY,
    tarifa_id INT REFERENCES tarifa DEFAULT NULL,
    contador_id INT REFERENCES contador DEFAULT NULL,
    telefono TEXT DEFAULT '',
    nombre TEXT DEFAULT '',
    cif TEXT DEFAULT '',
    direccion TEXT DEFAULT '',
    pais TEXT DEFAULT '',
    ciudad TEXT DEFAULT '',
    provincia TEXT DEFAULT '',
    cp TEXT DEFAULT '',
    iva FLOAT DEFAULT 0.21,
    direccionfacturacion TEXT DEFAULT '',
    paisfacturacion TEXT DEFAULT '',
    ciudadfacturacion TEXT DEFAULT '',
    provinciafacturacion TEXT DEFAULT '',
    cpfacturacion TEXT DEFAULT '',
    nombref TEXT DEFAULT '',        -- Nombre de facturación (por si difiere
                                    -- del del cliente en la factura).
    email TEXT DEFAULT '',          -- Dirección (o direcciones separadas por
                                    -- coma) de correo electrónico.
    contacto TEXT DEFAULT '',
    observaciones TEXT DEFAULT '',
    vencimientos TEXT DEFAULT '',
    formadepago TEXT DEFAULT '',
    documentodepago TEXT DEFAULT '',
    diadepago TEXT DEFAULT '',  -- El día en que se harán los pagos realmente
                                -- (independientemente de lo que marque
                                -- el vencimiento, el pago se puede hacer días
                                -- antes o días después, en un día del
                                -- mes fijo) P.ej: El vencimiento cumple el 15
                                -- de enero pero siempre se le paga al
                                -- proveedor los días 5 de cada mes.
                                -- De momento es texto (aunque en teoría sería
                                -- un INT) para contemplar la posibilidad
                                -- de meter días concatenados con comas -por
                                -- ejemplo- y así expresar que se le
                                -- pagan -por ejemplo one more time- los días
                                -- 5 y 20 de cada mes.
    inhabilitado BOOLEAN DEFAULT FALSE, -- NEW! 08/10/06
    motivo TEXT DEFAULT '',     -- NEW! 08/10/06. Si está inhabilitado no se
        -- permitirá hacerle más pedidos de venta. (CWT)
    cliente_id INT REFERENCES cliente DEFAULT NULL, -- NEW! 25/10/2006.
        -- Comercial que actúa como intermediario con el cliente.
    porcentaje FLOAT DEFAULT 0.0,                   -- NEW! 25/10/2006.
        -- Porcentaje de comisión de la facturación que se lleva.
    enviar_correo_albaran BOOLEAN DEFAULT FALSE,    -- NEW! 25/10/2006. Si
        -- TRUE, se envía por correo-e el PDF del albarán Geotexan.
    enviar_correo_factura BOOLEAN DEFAULT FALSE,    -- NEW! 25/10/2006. Si
        -- TRUE, se envía por correo-e el PDF de la factura.
    enviar_correo_packing BOOLEAN DEFAULT FALSE,    -- NEW! 25/10/2006. Si
        -- TRUE, se envía por correo-e el PDF del packing list.
    fax TEXT DEFAULT '',                            -- NEW! 25/10/2006.
        -- Incomprensiblemente, lleva el fax en la ventana
        -- ¡meses! y todavía no estaba en la tabla.
    proveedor_id INT REFERENCES proveedor DEFAULT NULL, -- Si el cliente es
        -- comercial de otros clientes, debe relacionarse con
        -- un proveedor que actúe como proveedor de servicios para las
        -- facturas de compra de las comisiones a pagar.
    cuenta_origen_id INT REFERENCES cuenta_origen DEFAULT NULL,-- NEW! 26/02/07
        -- Cuenta bancaria _destino_ por defecto para transferencias.
    riesgo_asegurado FLOAT DEFAULT -1.0, -- NEW! 06/11/2008. -1 = Indefinido
    riesgo_concedido FLOAT DEFAULT -1.0, -- NEW! 06/11/2008. -1 = Indefinido
    packing_list_con_codigo BOOLEAN DEFAULT FALSE,  -- NEW! 27/02/2009
    facturar_con_albaran BOOLEAN DEFAULT TRUE,      -- NEW! 02/03/2009
    copias_factura INT DEFAULT 0,   -- Sin incluir la original. NEW! 09/07/2009
    tipo_de_cliente_id INT REFERENCES tipo_de_cliente DEFAULT NULL
);

---------------------------------
-- Campos específicos de balas --
---------------------------------
CREATE TABLE campos_especificos_bala(
    id SERIAL PRIMARY KEY,
    dtex FLOAT DEFAULT 0.0,
    corte INT DEFAULT 0,
    color TEXT DEFAULT '',
    antiuv BOOLEAN DEFAULT False,
    tipo_material_bala_id INT REFERENCES tipo_material_bala,
    consumo_granza FLOAT DEFAULT 0.0,   -- Consumo de granza en kilos por kilo
        --en función, principalmente, de si es NEGRA o NATURAL.
    -- NEW! 20/06/07
    reciclada BOOLEAN DEFAULT False,    -- Si es True, es fibra reciclada. No
        -- consume materia prima, no se relaciona con balas sino con
        -- bala_cable, el corte y título no son significativos, las
        -- etiquetas son diferentes, etc.
    gramos_bolsa INT DEFAULT NULL,    -- Solo aplicable a bolsas de Geocem.
    bolsas_caja INT DEFAULT NULL,     -- Solo aplicable a bolsas de Geocem.
    -- NEW! 20/02/2010
    cajas_pale INT DEFAULT NULL,      -- Solo aplicable a Geocem embolsado.
    cliente_id INT REFERENCES cliente DEFAULT NULL  -- Este producto se 
        -- distribuye a través de un cliente y debe llevar sus datos en 
        -- la etiqueta de las cajas de fibra embolsada. No se suele usar en 
        -- fibra normal.
);

------------------------------------------------
-- Campos específicos de productos especiales --
------------------------------------------------
-- NEW! 23/11/06                              --
------------------------------------------------------------
-- Campos específicos de productos de venta "especiales". --
-- Son productos que no están relacionados con artículos  --
-- de almacén. Por tanto las existencias se guardan como  --
-- campo "absoluto" no calculado.                         --
------------------------------------------------------------
CREATE TABLE campos_especificos_especial(
    id SERIAL PRIMARY KEY,
    stock FLOAT DEFAULT 0.0,    -- Existencias en kg, m, m², ud...
    existencias INT DEFAULT 0,  -- Bultos
    unidad TEXT DEFAULT '',
    observaciones TEXT DEFAULT ''
);

-----------------------------------------------
-- Tabla de funciones para generar etiquetas --
-----------------------------------------------
CREATE TABLE modelo_etiqueta(
    id SERIAL PRIMARY KEY, 
    nombre TEXT,    -- Nombre descriptivo de la etiqueta.
    modulo TEXT,    -- Módulo (fichero python sin extensión) donde reside 
                    -- la función que se invocará para generar la etiqueta.
                    -- El módulo se importará desde el directorio «informes».
    funcion TEXT    -- Nombre de la función que devolverá un PDF con las 
                    -- etiquetas.
);

----------------------------------
-- Campos específicos de rollos --
----------------------------------
CREATE TABLE campos_especificos_rollo(
    id SERIAL PRIMARY KEY,
    gramos INT DEFAULT 0,
    codigo_composan TEXT DEFAULT '',
    ancho FLOAT DEFAULT 0.0,
    diametro INT DEFAULT 0,
    rollos_por_camion INT DEFAULT 0,
    metros_lineales INT DEFAULT 0,
    peso_embalaje FLOAT DEFAULT 0.0,
    ----- TOLERANCIAS EN PRUEBAS SOBRE GEOTEXTILES sobre estándar -----
    estandar_prueba_gramaje FLOAT DEFAULT 0.0,
    tolerancia_prueba_gramaje FLOAT DEFAULT 0.0,
    estandar_prueba_longitudinal FLOAT DEFAULT 0.0,
        -- Resistencia longitudinal
    tolerancia_prueba_longitudinal FLOAT DEFAULT 0.0,
        -- Resistencia longitudinal
    estandar_prueba_alargamiento_longitudinal FLOAT DEFAULT 0.0,
    tolerancia_prueba_alargamiento_longitudinal FLOAT DEFAULT 0.0,
    estandar_prueba_transversal FLOAT DEFAULT 0.0,
        -- Resistencia transversal
    tolerancia_prueba_transversal FLOAT DEFAULT 0.0,
        -- Resistencia transversal
    estandar_prueba_alargamiento_transversal FLOAT DEFAULT 0.0,
    tolerancia_prueba_alargamiento_transversal FLOAT DEFAULT 0.0,
    estandar_prueba_compresion FLOAT DEFAULT 0.0,           -- CBR
    tolerancia_prueba_compresion FLOAT DEFAULT 0.0,         -- CBR
    estandar_prueba_perforacion FLOAT DEFAULT 0.0,
    tolerancia_prueba_perforacion FLOAT DEFAULT 0.0,
    estandar_prueba_espesor FLOAT DEFAULT 0.0,
    tolerancia_prueba_espesor FLOAT DEFAULT 0.0,
    estandar_prueba_permeabilidad FLOAT DEFAULT 0.0,
    tolerancia_prueba_permeabilidad FLOAT DEFAULT 0.0,
    estandar_prueba_poros FLOAT DEFAULT 0.0,
    tolerancia_prueba_poros FLOAT DEFAULT 0.0,
    -- Tolerancias superiores (las anteries son la tolerancia normal -1 ver la
    -- tolerancia en la hoja de marcado- o la tolerancia inferior -en los
    -- valores que son +/- en el cuadro de marcado-.
    tolerancia_prueba_gramaje_sup FLOAT DEFAULT 0.0,    -- Gramaje
    tolerancia_prueba_longitudinal_sup FLOAT DEFAULT 0.0,
        -- Resistencia longitudinal
    tolerancia_prueba_alargamiento_longitudinal_sup FLOAT DEFAULT 0.0,
        -- Alargamiento longitudinal
    tolerancia_prueba_transversal_sup FLOAT DEFAULT 0.0,
        -- Resistencia transversal
    tolerancia_prueba_alargamiento_transversal_sup FLOAT DEFAULT 0.0,
        -- Alargamiento transversal
    tolerancia_prueba_compresion_sup FLOAT DEFAULT 0.0,     -- CBR
    tolerancia_prueba_perforacion_sup FLOAT DEFAULT 0.0,    -- Cono
    tolerancia_prueba_espesor_sup FLOAT DEFAULT 0.0,        -- Espesor
    tolerancia_prueba_permeabilidad_sup FLOAT DEFAULT 0.0,  -- Permeabilidad
    tolerancia_prueba_poros_sup FLOAT DEFAULT 0.0,          -- Porometría
    ficha_fabricacion TEXT DEFAULT '',      -- NEW! 20/01/08.
    c BOOLEAN DEFAULT FALSE,   -- Si True, es rollo «C» con anchos, largos y
                               -- grosores heterogéneos e ignorables.
    -- NEW! 13/06/2011: Nueva prueba para certificado de calidad ASQUAL
    -- Resistencia al punzonado piramidal (NF G38-019) KN y tolerancia en % 
    -- (aunque guardaré valores absolutos por "tradición").
    -- OJO: Antes de actualizar en clientes, ejecutar esto:
    -- ALTER TABLE campos_especificos_rollo ADD COLUMN estandar_prueba_piramidal FLOAT DEFAULT 0.0; ALTER TABLE campos_especificos_rollo ADD COLUMN tolerancia_prueba_piramidal FLOAT DEFAULT 0.0; ALTER TABLE campos_especificos_rollo ADD COLUMN tolerancia_prueba_piramidal_sup FLOAT DEFAULT 0.0; ALTER TABLE marcado_ce ADD COLUMN estandar_prueba_piramidal FLOAT DEFAULT 0.0; ALTER TABLE marcado_ce ADD COLUMN tolerancia_prueba_piramidal FLOAT DEFAULT 0.0; ALTER TABLE marcado_ce ADD COLUMN tolerancia_prueba_piramidal_sup FLOAT DEFAULT 0.0; ALTER TABLE partida ADD COLUMN piramidal FLOAT DEFAULT 0; CREATE TABLE prueba_piramidal(id SERIAL PRIMARY KEY, partida_id INT REFERENCES partida, fecha DATE DEFAULT CURRENT_DATE, resultado FLOAT DEFAULT 0.0);
    estandar_prueba_piramidal FLOAT DEFAULT 0.0, 
    tolerancia_prueba_piramidal FLOAT DEFAULT 0.0, 
    tolerancia_prueba_piramidal_sup FLOAT DEFAULT 0.0,
    -- NEW! 07/11/2011: Nueva tabla y campo de modelo de etiquetas.
    --                  NULL imprime la etiqueta genérica de geninformes.
    modelo_etiqueta_id INT REFERENCES modelo_etiqueta DEFAULT NULL, 
    cliente_id INT REFERENCES cliente DEFAULT NULL  -- Este producto se 
        -- fabrica específicamente para un cliente y sus etiquetas serán 
        -- la que indique "modelo_etiqueta_id" pero con los datos de 
        -- distribuidor de "cliente_id".
);

CREATE TABLE marcado_ce(
    id SERIAL PRIMARY KEY,
    campos_especificos_rollo_id INT REFERENCES campos_especificos_rollo,
    fecha_inicio DATE DEFAULT CURRENT_DATE, -- Inicio de aplicación.
    fecha_fin DATE DEFAULT CURRENT_DATE,    -- Fin de aplicación de los valores
        -- para comparar con el marcado CE. Cualquier partida fabricada entre
        -- estas dos fechas se compara con estos valores. Las que no, se
        -- comparan con los valores por defecto (los de campos_epecificos...).
    ----- TOLERANCIAS EN PRUEBAS SOBRE GEOTEXTILES sobre estándar -----
    estandar_prueba_gramaje FLOAT DEFAULT 0.0,
    tolerancia_prueba_gramaje FLOAT DEFAULT 0.0,
    estandar_prueba_longitudinal FLOAT DEFAULT 0.0,
        -- Resistencia longitudinal
    tolerancia_prueba_longitudinal FLOAT DEFAULT 0.0,
        -- Resistencia longitudinal
    estandar_prueba_alargamiento_longitudinal FLOAT DEFAULT 0.0,
    tolerancia_prueba_alargamiento_longitudinal FLOAT DEFAULT 0.0,
    estandar_prueba_transversal FLOAT DEFAULT 0.0,
        -- Resistencia transversal
    tolerancia_prueba_transversal FLOAT DEFAULT 0.0,
        -- Resistencia transversal
    estandar_prueba_alargamiento_transversal FLOAT DEFAULT 0.0,
    tolerancia_prueba_alargamiento_transversal FLOAT DEFAULT 0.0,
    estandar_prueba_compresion FLOAT DEFAULT 0.0,           -- CBR
    tolerancia_prueba_compresion FLOAT DEFAULT 0.0,         -- CBR
    estandar_prueba_perforacion FLOAT DEFAULT 0.0,
    tolerancia_prueba_perforacion FLOAT DEFAULT 0.0,
    estandar_prueba_espesor FLOAT DEFAULT 0.0,
    tolerancia_prueba_espesor FLOAT DEFAULT 0.0,
    estandar_prueba_permeabilidad FLOAT DEFAULT 0.0,
    tolerancia_prueba_permeabilidad FLOAT DEFAULT 0.0,
    estandar_prueba_poros FLOAT DEFAULT 0.0,
    tolerancia_prueba_poros FLOAT DEFAULT 0.0,
    -- Tolerancias superiores (las anteries son la tolerancia normal -1 ver la
    -- tolerancia en la hoja de marcado- o la tolerancia inferior -en los
    -- valores que son +/- en el cuadro de marcado-.
    tolerancia_prueba_gramaje_sup FLOAT DEFAULT 0.0,    -- Gramaje
    tolerancia_prueba_longitudinal_sup FLOAT DEFAULT 0.0,
        -- Resistencia longitudinal
    tolerancia_prueba_alargamiento_longitudinal_sup FLOAT DEFAULT 0.0,
        -- Alargamiento longitudinal
    tolerancia_prueba_transversal_sup FLOAT DEFAULT 0.0,
        -- Resistencia transversal
    tolerancia_prueba_alargamiento_transversal_sup FLOAT DEFAULT 0.0,
        -- Alargamiento transversal
    tolerancia_prueba_compresion_sup FLOAT DEFAULT 0.0,     -- CBR
    tolerancia_prueba_perforacion_sup FLOAT DEFAULT 0.0,    -- Cono
    tolerancia_prueba_espesor_sup FLOAT DEFAULT 0.0,        -- Espesor
    tolerancia_prueba_permeabilidad_sup FLOAT DEFAULT 0.0,  -- Permeabilidad
    tolerancia_prueba_poros_sup FLOAT DEFAULT 0.0,          -- Porometría
    -- NEW! 13/06/2011: Nueva prueba para certificado de calidad ASQUAL
    -- Resistencia al punzonado piramidal (NF G38-019) KN y tolerancia en % 
    -- (aunque guardaré valores absolutos por "tradición").
    estandar_prueba_piramidal FLOAT DEFAULT 0.0, 
    tolerancia_prueba_piramidal FLOAT DEFAULT 0.0, 
    tolerancia_prueba_piramidal_sup FLOAT DEFAULT 0.0
);

------------------------
-- Productos de venta --
------------------------
CREATE TABLE producto_venta(
    id SERIAL PRIMARY KEY,
    linea_de_produccion_id INT REFERENCES linea_de_produccion,
    campos_especificos_bala_id INT
        REFERENCES campos_especificos_bala DEFAULT NULL,
    campos_especificos_rollo_id INT
        REFERENCES campos_especificos_rollo DEFAULT NULL,
    nombre TEXT,
    descripcion TEXT,
    codigo TEXT UNIQUE,
    minimo FLOAT DEFAULT 0.0,
    preciopordefecto FLOAT DEFAULT 0.0,
    arancel TEXT DEFAULT '',
    prodestandar FLOAT DEFAULT 0.0,
    -- NEW! 23/11/06
    campos_especificos_especial_id INT
        REFERENCES campos_especificos_especial DEFAULT NULL,
    -- NEW! 9/07/2013
    anno_certificacion INT DEFAULT NULL, 
    dni TEXT DEFAULT '', 
    uso TEXT DEFAULT '', 
    -- ALTER TABLE producto_venta ADD COLUMN anno_certificacion INT DEFAULT NULL; ALTER TABLE producto_venta ADD COLUMN dni TEXT DEFAULT ''; ALTER TABLE producto_venta ADD COLUMN uso TEXT DEFAULT ''; UPDATE producto_venta SET anno_certificacion = NULL; UPDATE producto_venta SET dni = ''; UPDATE producto_venta SET uso = ''; 
    CHECK (NOT(campos_especificos_bala_id <> NULL
                AND campos_especificos_rollo_id <> NULL
                AND campos_especificos_especial_id <> NULL))
);

------------------------------------
-- Relación muchos a muchos entre --
-- producto de venta y consumo    --
-- adicional de formulación.      --
------------------------------------
CREATE TABLE consumo_adicional__producto_venta(
    producto_venta_id INT NOT NULL REFERENCES producto_venta,
    consumo_adicional_id INT NOT NULL REFERENCES consumo_adicional
);

------------------------------
-- Información de los silos --
------------------------------
CREATE TABLE silo(
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    capacidad FLOAT DEFAULT 0.0,
    observaciones TEXT DEFAULT ''
    -- ocupado es campo calculado
);

--------------------------------------------
-- Relación muchos a muchos con atributos --
-- entre productos de compra y silos      --
--------------------------------------------
CREATE TABLE carga_silo(
    id SERIAL PRIMARY KEY,
    producto_compra_id INT REFERENCES producto_compra NOT NULL,
    silo_id INT REFERENCES silo NOT NULL,
    fecha_carga TIMESTAMP DEFAULT LOCALTIMESTAMP(0),
    cantidad FLOAT      -- Cantidad cargada en el silo.
);

----------------------------------------------------------------
-- Precios (relación con atributos entre tarifas y productos) --
----------------------------------------------------------------
CREATE TABLE precio(
    id SERIAL PRIMARY KEY,
--    producto_venta_id INT REFERENCES producto_venta NOT NULL,
    producto_venta_id INT REFERENCES producto_venta DEFAULT NULL,
        -- NEW! 18/12/06: Ahora puede ser NULL porque si no relaciona un
        -- producto_venta...
    tarifa_id INT REFERENCES tarifa NOT NULL,
    precio FLOAT DEFAULT 0,
    producto_compra_id INT REFERENCES producto_compra DEFAULT NULL
        -- NEW! 18/12/06: ... puede relacionar un producto_compra.
);

--------------------------------------------
-- Partidas de fibra de cemento embolsada --
--------------------------------------------
CREATE TABLE partida_cem(
    id SERIAL PRIMARY KEY,
    numpartida INT8 UNIQUE,
    codigo TEXT DEFAULT '',             -- Empezarán por M
    observaciones TEXT DEFAULT ''
    -- TODO: Presumiblemente llevarán algunos valores específicos de su 
    -- marcado CE, pero aún no los sabemos con claridad. Están en ello.
);

--------------------------
-- Partes de producción --
--------------------------
CREATE TABLE parte_de_produccion(
    id SERIAL PRIMARY KEY,
    fecha DATE DEFAULT CURRENT_DATE,
    horainicio TIME DEFAULT LOCALTIME(0),
    horafin TIME DEFAULT LOCALTIME(0),
    prodestandar FLOAT DEFAULT 0,
    merma FLOAT DEFAULT 0.02,    -- Merma calculada por el operario sobre el
                                 -- consumo en relación a la producción.
                                 -- NO SE USA EN PARTES DE BALAS NI DE 
                                 -- EMBOLSADO.
    bloqueado BOOLEAN DEFAULT FALSE,
    observaciones TEXT DEFAULT '',
    fechahorainicio TIMESTAMP DEFAULT LOCALTIMESTAMP(0), -- NEW! 25/10/2006.
        -- Fecha y hora de inicio en el parte. Por defecto deberá ser la
        -- fecha + hora inicial del parte. Cuando esté implantado, se
        -- usará únicamente está. Fecha y horainicio quedan marcadas
        -- como DEPRECATED.
    fechahorafin TIMESTAMP DEFAULT LOCALTIMESTAMP(0), -- NEW! 25/10/2006.Ídem.
    fichaproduccion TEXT DEFAULT '',    -- NEW! 31/07/07 Texto libre con
        -- la versión de la ficha de producción usada en el parte.
    partida_cem_id INT REFERENCES partida_cem DEFAULT NULL  -- NEW! 18/05/2009 
        -- Hasta ahora la partida/lote se obtenía de los artículos, pero en el 
        -- caso de la fibra embolsada es necesario que se obtenga directamente 
        -- del parte. Al menos en etapas tempranas.
);

-----------------------------------------------------------
-- Consumo de materia prima por cada parte de produccion --
-----------------------------------------------------------
CREATE TABLE consumo(
    id SERIAL PRIMARY KEY,
    producto_compra_id INT REFERENCES producto_compra DEFAULT NULL,
    parte_de_produccion_id INT REFERENCES parte_de_produccion DEFAULT NULL,
    actualizado BOOLEAN DEFAULT FALSE, -- Si actualizado, la cantidad ya se ha
                                       -- descontado del producto de compra.
    antes FLOAT DEFAULT 0,      -- Sólo se usa en casos especiales donde es
                                -- necesario anotar la cantidad del producto
    despues FLOAT DEFAULT 0,    -- antes y después del consumo (por ejemplo en
                                -- la granza de los silos en la línea de fibra)
    cantidad FLOAT DEFAULT 0.0,
    silo_id INT REFERENCES silo DEFAULT NULL
);

-----------------------------------------------------------
-- Descuento de materiales (productos de compra) por     --
-- desechos (principalmente).                            --
-----------------------------------------------------------
-- NEW! 14/03/07 --
-------------------
CREATE TABLE descuento_de_material(
    id SERIAL PRIMARY KEY,
    producto_compra_id INT REFERENCES producto_compra DEFAULT NULL,
    parte_de_produccion_id INT REFERENCES parte_de_produccion DEFAULT NULL,
    cantidad FLOAT DEFAULT 0.0,
    fechahora TIMESTAMP DEFAULT LOCALTIMESTAMP(0),
    observaciones TEXT DEFAULT ''       -- Motivo por el cual se ha descontado
                                -- esa cantidad como desperdicio o lo que sea.
);

-----------------------
-- Categoría laboral --
-----------------------
CREATE TABLE categoria_laboral(
    id SERIAL PRIMARY KEY,
    codigo TEXT,    -- Lo usaré para "estandarizar" las búsquedas y tal (para
                    -- evitar casos como Jefe turno != Jefe de turno)...
    puesto TEXT,    -- Jefe de turno, Oficial producción, ...
    linea_de_produccion_id INT REFERENCES linea_de_produccion DEFAULT NULL,
    planta BOOLEAN DEFAULT True,    -- Puede haber auxiliares de planta que no
                                    -- tengan línea de producción fija.
    precio_hora_extra FLOAT DEFAULT 8.26,   -- /hora
    precio_hora_nocturnidad FLOAT DEFAULT 9.58, --/hora extra noche
    precio_plus_nocturnidad FLOAT DEFAULT 10.57,    -- /noche trabajada
    precio_plus_turnicidad FLOAT DEFAULT 100.0,     -- /mes. Sólo Fibra.
    precio_plus_jefe_turno FLOAT DEFAULT 104.0,     -- /mes
    precio_plus_festivo FLOAT DEFAULT 11.0,         -- /hora
    precio_plus_mantenimiento_sabados FLOAT DEFAULT 11.0,   -- /hora. Sólo GTX.
    dias_vacaciones INT DEFAULT 36,  -- Por defecto, 21 en agosto + 15 
                                     -- diciembre/enero, contando sábados y 
                                     -- domingos.
    dias_convenio INT DEFAULT 2,     -- Por defecto y por convenio laboral: 2
    dias_asuntos_propios INT DEFAULT 2, -- Por defecto 2 al año. Remunerados.
    salario_base FLOAT DEFAULT 0.0, 
    precio_hora_regular FLOAT DEFAULT 0.0,-- NEW! 16/09/2008. Necesario para
                                          -- calcular costes de líneas.
    fecha DATE DEFAULT NULL     -- Fecha de entrada en vigor de los precios 
                                -- para esta categoría laboral. Útil a la 
                                -- hora de calcular nóminas según la fecha 
                                -- en que se haga la consulta.
);

---------------
-- Almacenes --
---------------
-- NEW! 11/12/2008
CREATE TABLE almacen(
    id SERIAL PRIMARY KEY, 
    nombre TEXT, 
    observaciones TEXT DEFAULT '', 
    direccion TEXT DEFAULT '', 
    ciudad TEXT DEFAULT '', 
    provincia TEXT DEFAULT '', 
    cp TEXT DEFAULT '', 
    telefono TEXT DEFAULT '', 
    fax TEXT DEFAULT '',
    email TEXT DEFAULT '',
    pais TEXT DEFAULT 'España', 
    principal BOOLEAN DEFAULT TRUE, --OJO: solo se usará el primero de los 
                    -- almacenes principales definidos (en caso de que por 
                    -- error se crearan varios). Si el almacén es principal 
                    -- la producción y los consumos de las líneas se harán 
                    -- directamente en él.
    -- ¿Llegaremos a necesitar datos GIS?
    activo BOOLEAN DEFAULT TRUE
);

--------------------------
-- Albaranes de entrada --
--------------------------
CREATE TABLE albaran_entrada(
    id SERIAL PRIMARY KEY,
    proveedor_id INT REFERENCES proveedor DEFAULT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    numalbaran TEXT,
    bloqueado BOOLEAN DEFAULT FALSE,  -- NEW! 08/10/06
    repuestos BOOLEAN DEFAULT FALSE,    -- NEW! 12/02/08
        -- Si TRUE es un albarán de repuestos, tratamiento un poco especial.
        -- No provienen directamente de pedidos. En ventana permiten crear
        -- artículos.
    almacen_id INT REFERENCES almacen,  -- NEW! 09/01/2009 
    transportista_id INT REFERENCES transportista DEFAULT NULL -- BUGFIX 
                                                               -- 15/01/2009
);

------------------------------
-- Historial de existencias --
------------------------------
-- Una cantidad por fin de mes y producto. Refleja las
-- existencias globales (sin distinguir entre A, B y C) 
-- de ese producto en esa fecha concreta.
CREATE TABLE historial_existencias(
    id SERIAL PRIMARY KEY,
    producto_venta_id INT REFERENCES producto_venta NOT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    cantidad FLOAT DEFAULT 0.0,
    bultos INT DEFAULT 0, 
    almacen_id INT REFERENCES almacen 
);


------------------------------------------------------
-- Historial de existencias de productos de clase A --
------------------------------------------------------
-- NEW! 18/12/2009                                  --
------------------------------------------------------
CREATE TABLE historial_existencias_a(
    id SERIAL PRIMARY KEY,
    producto_venta_id INT REFERENCES producto_venta NOT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    cantidad FLOAT DEFAULT 0.0,
    bultos INT DEFAULT 0, 
    almacen_id INT REFERENCES almacen 
);

------------------------------------------------------
-- Historial de existencias de productos de clase B --
------------------------------------------------------
-- NEW! 18/12/2009                                  --
------------------------------------------------------
CREATE TABLE historial_existencias_b(
    id SERIAL PRIMARY KEY,
    producto_venta_id INT REFERENCES producto_venta NOT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    cantidad FLOAT DEFAULT 0.0,
    bultos INT DEFAULT 0, 
    almacen_id INT REFERENCES almacen 
);

------------------------------------------------------
-- Historial de existencias de productos de clase C --
------------------------------------------------------
-- NEW! 18/12/2009                                  --
------------------------------------------------------
CREATE TABLE historial_existencias_c(
    id SERIAL PRIMARY KEY,
    producto_venta_id INT REFERENCES producto_venta NOT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    cantidad FLOAT DEFAULT 0.0,
    bultos INT DEFAULT 0, 
    almacen_id INT REFERENCES almacen 
);

------------------------------------------------------
-- Historial de existencias de productos de compra. --
------------------------------------------------------
-- NEW! 24/11/06                                    --
----------------------------------------------------------
-- Existencias de los productos de compra en una fecha  --
-- determinada.                                         --
----------------------------------------------------------
CREATE TABLE historial_existencias_compra(
    id SERIAL PRIMARY KEY,
    producto_compra_id INT REFERENCES producto_compra NOT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    cantidad FLOAT DEFAULT 0.0,
    observaciones TEXT DEFAULT '', 
    almacen_id INT REFERENCES almacen 
);

-------------------------------------------------------------------
-- Relación muchos a muchos entre producto de compra y almacenes --
-------------------------------------------------------------------
-- Aquí se guardan las existencias de los productos de compra.
-- La suma de las existencias de todos los almacenes debe coincidir con 
-- el total almacenado en el producto de compra.
CREATE TABLE stock_almacen(
    id SERIAL PRIMARY KEY, 
    almacen_id INT REFERENCES almacen, 
    producto_compra_id INT REFERENCES producto_compra, 
    existencias FLOAT DEFAULT 0.0
);

-----------------------
-- Centro de trabajo --
-----------------------
CREATE TABLE centro_trabajo(
    id SERIAL PRIMARY KEY,
    nombre TEXT, 
    almacen_id INT REFERENCES almacen DEFAULT NULL 
);

-----------------------
-- TABLAS AUXILIARES --
-----------------------
CREATE TABLE usuario(
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(16) UNIQUE NOT NULL CHECK (usuario <> ''), -- Usuario de
                                                               -- la aplicación
    passwd CHAR(32) NOT NULL, -- MD5 de la contraseña
    nombre TEXT DEFAULT '',   -- Nombre completo del usuario
    cuenta TEXT DEFAULT '',   -- Cuenta de correo de soporte
    cpass TEXT DEFAULT '',    -- Contraseña del correo de soporte. TEXTO PLANO.
    nivel INT DEFAULT 5,      -- 0 es el mayor. 5 es el menor.
        -- Además de los permisos sobre ventanas, para un par de casos
        -- especiales se mirará el nivel de privilegios para permitir volver a
        -- desbloquear partes, editar albaranes antiguos y cosas así...
    email TEXT DEFAULT '',          -- NEW! 25/10/2006. Dirección de correo
        -- electrónico del usuario (propia, no soporte).
    smtpserver TEXT DEFAULT '',     -- NEW! 25/10/2006. Servidor SMTP
        -- correspondiente a la dirección anterior por donde
        -- enviar, por ejemplo, albaranes.
    smtpuser TEXT DEFAULT '',       -- NEW! 25/10/2006. Usuario para
        -- autenticación en el servidor SMTP (si fuera necesario)
    smtppassword TEXT DEFAULT '',   -- NEW! 25/10/2006. Contraseña para
        -- autenticación en el servidor SMTP (si fuera necesario).
    firma_total BOOLEAN DEFAULT FALSE,      -- NEW! 26/02/2007. Puede firmar
        -- por cualquiera de los 4 roles en facturas de compra.
    firma_comercial BOOLEAN DEFAULT FALSE,  -- NEW! 26/02/2007. Puede firmar
        -- como director comercial.
    firma_director BOOLEAN DEFAULT FALSE,   -- NEW! 26/02/2007. Puede firmar
        -- como director general.
    firma_tecnico BOOLEAN DEFAULT FALSE,    -- NEW! 26/02/2007. Puede firmar
        -- como director técnico.
    firma_usuario BOOLEAN DEFAULT FALSE,    -- NEW! 26/02/2007. Puede firmar
        -- como usuario (confirmar total de factura).
    observaciones TEXT DEFAULT ''           -- NEW! 26/02/2007. Observaciones.
);

---------------
-- Empleados --
---------------
CREATE TABLE empleado(
    id SERIAL PRIMARY KEY,
    categoria_laboral_id INT REFERENCES categoria_laboral DEFAULT NULL,
    centro_trabajo_id INT REFERENCES centro_trabajo DEFAULT NULL,
    nombre TEXT CHECK (nombre<>''),
    apellidos TEXT,
    dni TEXT,
    planta BOOLEAN DEFAULT True,    -- True si son de planta. False si son de
        -- oficina, etc. OJO: CATEGORÍA LABORAL TIENE PREFERENCIA.
    nomina NUMERIC(9,2) DEFAULT 0.0,       -- BASE nómina mensual.
    preciohora NUMERIC(9,2) DEFAULT 0.0,   -- Precio por hora extra. OJO:
        -- CATEGORÍA LABORAL TIENE PREFERENCIA.
    activo BOOLEAN DEFAULT True,    -- Si False, el empleado está dado de
                                    -- baja pero se conserva en la BD.
    usuario_id INT REFERENCES usuario DEFAULT NULL -- NEW! 30/12/2008
        -- Usuario con el que el empleado hace login. Será util para 
        -- identificar a los comerciales automáticamente.
);

-----------------
-- Comerciales --
-----------------
-- NEW! 30/12/2008 - Tabla de campos específicos para comerciales.
-- Un comercial, un empleado de la BD.
-- Necesitará dar de alta una nueva categoría laboral.
CREATE TABLE comercial(
    id SERIAL PRIMARY KEY, 
    empleado_id INT REFERENCES empleado NOT NULL, 
    comision FLOAT DEFAULT 0.0, -- Porcentaje de comisión por ventas.
    observaciones TEXT DEFAULT '', 
    cargo TEXT DEFAULT '',      -- Para cosas como "Delegado zona norte". Más 
                                -- específico que CategoriaLaboral. 
                                -- NEW! 27/01/2009
    telefono TEXT DEFAULT '',   -- NEW! 27/01/2009
    correoe TEXT DEFAULT ''     -- NEW! 27/01/2009
);

-------------------------------------
-- Nómina mensual de los empleados --
-------------------------------------
CREATE TABLE nomina(
    id SERIAL PRIMARY KEY,
    empleado_id INT REFERENCES empleado NOT NULL,
    fecha DATE,     -- El día se ignorará, pero es más cómodo guardar mes y
                    -- año juntos en el mismo campo.
    cantidad NUMERIC(9,2) DEFAULT 0.0,  -- Total en moneda.
    horas_extra FLOAT DEFAULT 0.0,  -- Número de horas extra que hizo en el
        -- mes de la nómina. Campo calculado, se guarda por eficiencia.
    horas_nocturnidad FLOAT DEFAULT 0.0, -- Número de horas con nocturnidad
        -- (entre las 22:00 y las 6:00). Campo calculado también.
    gratificacion FLOAT DEFAULT 0.0,    -- Manual
    plus_jefe_turno FLOAT DEFAULT 0.0,  -- Cantidad fija o 0 si no lleva. Solo
                                        -- para linea_de_produccion != None
    plus_no_absentismo FLOAT DEFAULT 0.0,   -- Manual. Una vez al año.
    plus_festivo FLOAT DEFAULT 0.0,     -- Cantidad fija * número de festivos.
                                        -- Solo para linea_de_produccion!=None
    plus_turnicidad FLOAT DEFAULT 0.0,  -- Cantidad fija solo para
                                        -- linea_de_produccion == Fibra
    plus_mantenimiento_sabados FLOAT DEFAULT 0.0,   -- Cantidad fija * número
        -- de sábados. Solo si linea_de_produccion != None y != Fibra (GTX).
    total_horas_extra FLOAT DEFAULT 0.0, -- Cantidad en moneda correspondiente
                                         -- a precio_hora_exta * horas_extra
    total_horas_nocturnidad FLOAT DEFAULT 0.0,  -- Cantidad en moneda
        -- correspondiente a precio_hora_nocturnidad * horas_nocturnidad
    base FLOAT DEFAULT 0.0,     -- NEW! 28/03/07 "Sueldo base" del trabajador
                                -- que se sumará a los pluses para obtener el
                                -- total de la nómina.
                                -- Por defecto debería ser igual al campo
                                -- nomina de la tabla empleado. Y a su ver
                                -- debería ser igual a salario_base de su
                                -- categoría laboral.
    otros FLOAT DEFAULT 0.0,    -- NEW! 28/03/07 Otros conceptos a añadir,
        -- como por ejemplo retrasos. Un, dos, tres responda otra vez.
    fechaini DATE DEFAULT CURRENT_DATE,     -- NEW! 27/04/07. Los extras no se
                                            -- calculan a mes natural completo.
    fechafin DATE DEFAULT CURRENT_DATE      -- NEW! 27/04/07. Se suelen
                                            -- calcular desde una semana antes
                                            -- de fin del mes anterior a una
                                            -- semana antes del fin de mes de
                                            -- la nómina.
);

-------------------------
-- Motivos de ausencia --
-------------------------
CREATE TABLE motivo(
    id SERIAL PRIMARY KEY,
    descripcion TEXT,
    descripcion_dias TEXT DEFAULT '',   -- Descripción del tipo "(2 días
                                        -- retribuidos)" o "(Según
                                        -- circunstancia)".
    retribuido INT DEFAULT 0,   -- *Creo* que se refiere a días. En todo caso,
                                -- en la documentación de Geotexan dice que
                                -- son enteros.
    sin_retribuir INT DEFAULT 0,
    excedencia_maxima INT DEFAULT 0,    -- En días también. Si son dos
                                        -- meses: 60 días.
    convenio BOOLEAN DEFAULT True,  -- La ausencia cuenta como días de
                                    -- convenio. Si False, son asuntos propios.
    penaliza BOOLEAN DEFAULT True   -- Si True, penaliza para el plus de no
                                    -- absentismo; aunque de momento es manual.
);

---------------
-- Ausencias --
---------------
CREATE TABLE ausencia(
    id SERIAL PRIMARY KEY,
    empleado_id INT REFERENCES empleado,
    motivo_id INT REFERENCES motivo,
    fecha DATE DEFAULT CURRENT_DATE,
    observaciones TEXT DEFAULT ''
);

--------------------------
-- Bajas por enfermedad --
--------------------------------------------------------------------------
-- Igual que las ausencias pero con fecha de fin que puede ser nula si  --
-- hasta que el trabajado vuelva a darse de alta.                       --
--------------------------------------------------------------------------
-- NEW! 29/07/2008
CREATE TABLE baja(
    id SERIAL PRIMARY KEY,
    empleado_id INT REFERENCES empleado,
    motivo TEXT DEFAULT '',
    fecha_inicio DATE DEFAULT CURRENT_DATE,
    fecha_fin DATE DEFAULT NULL,
    observaciones TEXT DEFAULT ''
);

---------------------------------------------------------------------
-- Relación muchos a muchos entre empleados y partes de producción --
---------------------------------------------------------------------
CREATE TABLE parte_de_produccion_empleado(
    id SERIAL PRIMARY KEY,
    empleadoid INT REFERENCES empleado NOT NULL,
    partedeproduccionid INT REFERENCES parte_de_produccion NOT NULL,
    --    horas FLOAT DEFAULT 0.0  -- Horas trabajadas por el empleado en el
                                   -- parte. Entre 0.0 y 8.0 normalmente.
                                   -- Se correspondería con un
                                   -- mx.DateTimeDelta.hours (aunque éste es
                                   -- un atributo property de solo lectura en
                                   -- el objeto).
    --    horas INTERVAL DEFAULT '0 00:00:00'   -- Esto sería lo correcto,
                                                -- pero SQLObject lo usa como
                                                -- entero en lugar de crear un
                                                -- DateTimeDelta de mx, que
                                                -- sería lo ideal.
    horas TIME DEFAULT '00:00:00'   -- OJO: No permitirá que se trabaje más de
                                    -- 24 horas en un mismo parte...
                                    -- ¿alguien podría trabajar más de 24
                                    -- horas en un mismo parte? ¿En serio?
);

----------------------------------------------------
-- Partes de trabajo independientes de producción --
----------------------------------------------------
CREATE TABLE parte_de_trabajo(
    id SERIAL PRIMARY KEY,
    empleado_id INT REFERENCES empleado NOT NULL,
    trabajo TEXT DEFAULT '',                        -- Trabajo en que empleó
                                                    -- el tiempo.
    horainicio TIMESTAMP DEFAULT LOCALTIMESTAMP(0), -- Una tupla por empleado
                                                    -- con trabajo fuera del
                                                    -- parte.
    horafin TIMESTAMP DEFAULT LOCALTIMESTAMP(0),    -- La fecha va incluida en
                                                    -- las horas de inicio y
                                                    -- fin.
    centro_trabajo_id INT REFERENCES centro_trabajo DEFAULT NULL
);

------------------------
-- Calendario laboral --
----------------------------------------------------
-- Se pueden crear calendarios genéricos, sin LDP --
-- (por ejemplo, para oficinas y administrativos) --
----------------------------------------------------
CREATE TABLE calendario_laboral(
    id SERIAL PRIMARY KEY,
    linea_de_produccion_id INT REFERENCES linea_de_produccion DEFAULT NULL,
    mes_anno DATE DEFAULT CURRENT_DATE, -- Fecha completa, pero ignoraré el
                                        -- día.
    observaciones TEXT DEFAULT ''       -- Que son mucho de pedir campos de
                                        -- texto para anotaciones meses más
                                        -- tarde...
);

--------------
-- Festivos --
----------------------------------------------------------
-- Cada festivo es independiente y pertenece            --
-- a un calendario laboral. Dos festivos (aun siendo    --
-- el mismo día) en dos calendarios laborales           --
-- diferentes, son dos registros de la tabla distintos. --
-- Se pueden crear días festivos sin calendario y       --
-- relacionarlos después en función del mes y año.      --
-- Aunque en ese caso se debe duplicar el registro      --
-- tantas veces como en calendarios laborales encaje.   --
----------------------------------------------------------
CREATE TABLE festivo(
    id SERIAL PRIMARY KEY,
    calendario_laboral_id INT REFERENCES calendario_laboral DEFAULT NULL,
    fecha DATE DEFAULT CURRENT_DATE   -- Día festivo. Año y mes incluidos,
                                      -- aunque se pueden ignorar dado que
                                      -- deben ser iguales a los del
                                      -- calendario.
);

------------------------
-- Festivos genéricos --
-------------------------------------------------------------------------------
-- Provisional. No sé si habrá algún cambio en el futuro con las dos tablas  --
-- de festivos.                                                              --
-- Tabla con los festivos comunes a todos los años. Son los festivos por     --
-- defecto que se crean en cada mes y año particular (calendarios_laborales).--
-------------------------------------------------------------------------------
CREATE TABLE festivo_generico(
    id SERIAL PRIMARY KEY,
    fecha DATE      -- El año puede ser ignorado.
);

----------------
-- Vacaciones --
----------------------------------------------------------
-- Cada dea de vacaiones es independiente y pertenece   --
-- a un calendario laboral. Dos días  (aun siendo       --
-- el mismo día) en dos calendarios laborales           --
-- diferentes, son dos registros de la tabla distintos. --
-- Para un periodo de 21 días de vacaciones, por        --
-- ejemplo, debe haber 21 registros con cada uno de     --
-- esos 21 días. Y 21 registros por cada calendario     --
-- laboral (al menos un calendario por línea de         --
-- producción). Si las vacaciones no coinciden con el   --
-- mes del calendario_laboral, obviamente, no se crean  --
-- asociados a él en esta tabla.                        --
----------------------------------------------------------
CREATE TABLE vacaciones(
    id SERIAL PRIMARY KEY,
    calendario_laboral_id INT REFERENCES calendario_laboral DEFAULT NULL,
    fecha DATE DEFAULT CURRENT_DATE -- Día de vacaciones. Año y mes incluidos,
                                    -- aunque se pueden ignorar dado que
                                    -- deben ser iguales a los del calendario.
);

------------
-- Turnos --
------------
CREATE TABLE turno(
    id SERIAL PRIMARY KEY,
    nombre TEXT,                       -- Mañana, tarde, noche
    horainicio TIMESTAMP DEFAULT NULL, -- 22:00, por ejemplo. None si es un
                                       -- turno de recuperación sin hora fija.
    horafin TIMESTAMP DEFAULT NULL,    -- 6:00, por ejemplo
    noche BOOLEAN DEFAULT False,       -- True si es turno de noche y por
                                       -- tanto llevará plus y cálculos
                                       -- especiales.
    observaciones TEXT DEFAULT '',     -- Por si acaso aparece un CWT.
    recuperacion BOOLEAN DEFAULT False -- Si es True, es un turno de
                                       -- recuperación. No para línea de
                                       -- producción.
);

---------------------------------
-- Grupos de trabajo de planta --
---------------------------------
CREATE TABLE grupo(
    id SERIAL PRIMARY KEY,
    nombre TEXT,        -- 'A', 'B', 'Grupo C'... lo que sea.
    jefeturno_id INT REFERENCES empleado DEFAULT NULL,  -- ¿Tragará bien
        -- SQLObject con esto sin llamarse empleado_id?
    operario1_id INT REFERENCES empleado DEFAULT NULL,
    operario2_id INT REFERENCES empleado DEFAULT NULL,
    observaciones TEXT DEFAULT ''

);

-------------------
-- Día laborable --
--------------------------------------------------
-- Día laborable de un calendario, con el grupo --
-- que trabaja y el turno donde lo hace.        --
--------------------------------------------------
CREATE TABLE laborable(
    id SERIAL PRIMARY KEY,
    fecha DATE DEFAULT CURRENT_DATE,
        -- Mes y año deben coincidir con el del calendario laboral.
    turno_id INT REFERENCES turno,
    calendario_laboral_id INT REFERENCES calendario_laboral,
    grupo_id INT REFERENCES grupo,
    observaciones TEXT DEFAULT ''
);


-------------------------
-- Tipos de incidencia --
-------------------------
CREATE TABLE tipo_de_incidencia(
    id SERIAL PRIMARY KEY,
    descripcion TEXT
);

-----------------
-- Incidencias --
-----------------
CREATE TABLE incidencia(
    id SERIAL PRIMARY KEY,
    tipo_de_incidencia_id INT4 REFERENCES tipo_de_incidencia,
    parte_de_produccion_id INT REFERENCES parte_de_produccion,
    horainicio TIMESTAMP DEFAULT LOCALTIMESTAMP(0),
    horafin TIMESTAMP DEFAULT LOCALTIMESTAMP(0),
    observaciones TEXT DEFAULT ''
);

------------------------------------
-- Cuentas bancarias de clientes. --
------------------------------------
-- NEW! 01/07/07 --
-------------------
CREATE TABLE cuenta_bancaria_cliente(
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES cliente NOT NULL,
    observaciones TEXT DEFAULT '',
    banco TEXT DEFAULT '',
    swif TEXT DEFAULT '',
    iban TEXT DEFAULT '',
    cuenta TEXT DEFAULT ''
);

-------------------------------------------------------------
-- Campos específicos adicionales para productos concretos --
-------------------------------------------------------------
CREATE TABLE campos_especificos(
    id SERIAL PRIMARY KEY,
    producto_venta_id INT REFERENCES producto_venta NOT NULL,
    nombre TEXT,
    valor TEXT DEFAULT ''
);

---------------------
-- Tabla de obras  --
-- NEW! 26/05/2009 --
---------------------
CREATE TABLE obra(
    id SERIAL PRIMARY KEY, 
    nombre TEXT, 
    direccion TEXT DEFAULT '',
    cp TEXT DEFAULT '', 
    ciudad TEXT DEFAULT '', 
    provincia TEXT DEFAULT '', 
    fechainicio DATE DEFAULT CURRENT_DATE, 
    fechafin DATE DEFAULT NULL, 
    observaciones TEXT DEFAULT '', 
    generica BOOLEAN DEFAULT FALSE, -- NEW! 27/07/2009: CWT: Si 
        -- generica = TRUE, es una obra ficticia con los mismos datos del 
        -- cliente, únicamente para cumplir el formato estándar de CRM de 
        -- cliente -> obras y cada cliente al menos una obra.
    pais TEXT DEFAULT ''    -- NEW! 13/07/2010.
);

----------------------
-- Pedidos de venta --
----------------------
CREATE TABLE pedido_venta(
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES cliente,
    tarifa_id INT REFERENCES tarifa DEFAULT NULL,
    transporte_a_cargo BOOLEAN DEFAULT False,   -- CWT one more time. Al
        -- principio bastaba con la tarifa del cliente, ya no.
    fecha DATE DEFAULT CURRENT_DATE,
    numpedido TEXT,
    iva FLOAT DEFAULT 0.21,
    descuento FLOAT DEFAULT 0.0,     -- Descuento como fracción de 1.
                                     -- 1,44% = 0.0144
    bloqueado BOOLEAN DEFAULT FALSE, -- NEW! 08/10/06
    cerrado BOOLEAN DEFAULT FALSE,   -- NEW! 08/10/06. Si el pedido está
                                     -- cerrado no admitirá más albaranes de
                                     -- salida relacionados ni aparecerá en el
                                     -- listado de pendientes de servir.
    envio_direccion TEXT DEFAULT '', -- NEW! 25/10/2006. Dirección de envío
                                     -- heredable por el albarán de salida.
    envio_ciudad TEXT DEFAULT '',    -- NEW! 25/10/2006. Ciudad de envío.
    envio_provincia TEXT DEFAULT '', -- NEW! 25/10/2006. Dirección de envío:
                                     -- provincia.
    envio_cp TEXT DEFAULT '',        -- NEW! 25/10/2006. Dirección de envío:
                                     -- Código postal.
    envio_pais TEXT DEFAULT '',      -- NEW! 25/10/2006. Dirección de envío:
                                     -- país.
    comercial_id INT REFERENCES comercial DEFAULT NULL,-- NEW! 15/01/2009
    nombre_correspondencia TEXT DEFAULT '',     -- NEW! 27/02/2009
    direccion_correspondencia TEXT DEFAULT '',  -- NEW! 27/02/2009
    cp_correspondencia TEXT DEFAULT '',         -- NEW! 27/02/2009
    ciudad_correspondencia TEXT DEFAULT '',     -- NEW! 27/02/2009
    provincia_correspondencia TEXT DEFAULT '',  -- NEW! 27/02/2009
    pais_correspondencia TEXT DEFAULT '',       -- NEW! 27/02/2009
    texto_obra TEXT DEFAULT '',   --- NEW! 27/02/2009 -- Antes se llamaba 
        -- solo "obra", pero como ahora hay un obraID, he tenido que renombrar
        -- el campo.
    obra_id INT REFERENCES obra DEFAULT NULL,   -- NEW! 09/09/2009 Beatles' day
    forma_de_pago_id INT REFERENCES forma_de_pago DEFAULT NULL, 
    validado BOOLEAN DEFAULT TRUE,  -- NEW! 10/06/13. Si cumple requisitos 
                                    -- para poderse servir.
    -- ALTER TABLE pedido_venta ADD COLUMN validado BOOLEAN DEFAULT TRUE; UPDATE pedido_venta SET validado = TRUE; 
    usuario_id INT REFERENCES usuario DEFAULT NULL -- NEW! 11/06/2013. Usuario 
        -- que ha autorizado el pedido.
    -- ALTER TABLE pedido_venta ADD COLUMN usuario_id INT REFERENCES usuario DEFAULT NULL; UPDATE pedido_venta SET usuario_id = NULL;
);

----------------------------
-- Presupuestos (ofertas) --
----------------------------
-- NEW! 15/03/07 --
------------------------------------------------------------------
-- Relación de productos y servicios ofrecidos a un cliente     --
-- concreto y a un precio determinado. Si se aceptan, pasa      --
-- a ser pedido y de ahí en adelantes sigue si cauce natural.   --
------------------------------------------------------------------
CREATE TABLE presupuesto(
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES cliente,
    fecha DATE DEFAULT CURRENT_DATE,
    -- aceptado BOOLEAN DEFAULT FALSE,      -- Es mejor como campo calculado
                                        -- (aceptado, aceptado parcialmente
                                        -- xx% de líneas, no aceptado)
                                        -- etcétera en base a las LDP y
                                        -- servicios que tienen pedidoID!=None.
    persona_contacto TEXT DEFAULT '',   -- Por defecto el del cliente.
    nombrecliente TEXT DEFAULT '',      -- Nombre del cliente. Por defecto el
                                        -- del cliente, pero puede ser otro
                                        -- (una obra/constructora o algo).
    direccion TEXT DEFAULT '',          -- Por defecto la del cliente.
    ciudad TEXT DEFAULT '',             -- Por defecto será la del cliente.
    provincia TEXT DEFAULT '',          -- Por defecto será la del cliente.
    cp TEXT DEFAULT '',                 -- Código postal. Por defecto el del
                                        -- cliente.
    pais TEXT DEFAULT '',               -- Por defecto el del cliente.
    telefono TEXT DEFAULT '',           -- Por defecto el del cliente.
    fax TEXT DEFAULT '',                -- Por defecto el del cliente.
    texto TEXT DEFAULT '',              -- Texto de la carta de oferta. Es un
                                        -- texto libre.
    despedida TEXT DEFAULT '',          -- Texto de despedida de la carta de
                                        -- oferta. Es texto libre también.
    validez INT DEFAULT 6,              -- Validez del presupuesto en meses.
                                        -- Si != 0, se tiene en cuenta.
    numpresupuesto INT DEFAULT NULL,    -- NEW! 31/07/2008
    descuento FLOAT DEFAULT 0.0,        -- NEW! 31/07/2008 Dto. global en %
    comercial_id INT REFERENCES comercial DEFAULT NULL,-- NEW! 30/12/2008
    nombreobra TEXT DEFAULT '',   --- NEW! 27/02/2009 UPDATED 24/08/2013
    -- Campos añadidos para el nuevo módulo de comerciales: NEW! 23/08/2013
    estudio BOOLEAN DEFAULT NULL, 
    adjudicada BOOLEAN DEFAULT FALSE, 
    cif TEXT DEFAULT '', 
    email TEXT DEFAULT '', 
    forma_de_pago_id INT REFERENCES forma_de_pago DEFAULT NULL, 
    observaciones TEXT DEFAULT '', 
    obra_id INT REFERENCES obra DEFAULT NULL, 
    usuario_id INT REFERENCES usuario DEFAULT NULL, -- Usuario que ha validado.
    fecha_validacion TIMESTAMP DEFAULT NULL, 
    -- ALTER TABLE presupuesto ADD COLUMN estudio BOOLEAN DEFAULT NULL; ALTER TABLE presupuesto ADD COLUMN adjudicada BOOLEAN DEFAULT FALSE; ALTER TABLE presupuesto ADD COLUMN cif TEXT DEFAULT ''; ALTER TABLE presupuesto ADD COLUMN email TEXT DEFAULT ''; ALTER TABLE presupuesto ADD COLUMN forma_de_pago_id INT REFERENCES forma_de_pago DEFAULT NULL; ALTER TABLE presupuesto ADD COLUMN observaciones TEXT DEFAULT ''; ALTER TABLE presupuesto ADD COLUMN obra_id INT REFERENCES obra DEFAULT NULL; ALTER TABLE presupuesto RENAME COLUMN obra TO nombreobra; ALTER TABLE presupuesto ADD COLUMN usuario_id INT REFERENCES usuario DEFAULT NULL; ALTER TABLE presupuesto ADD COLUMN fecha_validacion TIMESTAMP DEFAULT NULL;  
    cerrado BOOLEAN DEFAULT FALSE,  -- Para indicar que ya se ha terminado de 
                                    -- introducir información y queda listo 
                                    -- para validar (si fuera necesario).
    -- Algunos contadores que considero interesantes y pueden hacer falta:
    impresiones INT DEFAULT 0,  -- Número de veces que ha generado el PDF
    envios INT DEFAULT 0,       -- Número de veces que ha enviado la oferta.
    version INT DEFAULT 1       -- Veces que ha guardado el presupuesto.
);

----------------------------------
-- Líneas de ofertas a clientes --
----------------------------------
CREATE TABLE linea_de_presupuesto(
    id SERIAL PRIMARY KEY,
    presupuesto_id INT REFERENCES presupuesto,
    producto_venta_id INT REFERENCES producto_venta DEFAULT NULL,
    producto_compra_id INT REFERENCES producto_compra DEFAULT NULL,
    descripcion TEXT DEFAULT '',  -- Texto libre para crear servicios al pasar
    -- a pedido, que puede ser la descripción de un producto también si 
    -- la línea se corresponde con un producto.
    fechahora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cantidad FLOAT,
    precio FLOAT DEFAULT 0.0,
    -- descuento FLOAT DEFAULT 0.0,
    -- fecha_entrega DATE DEFAULT CURRENT_DATE,
    -- texto_entrega TEXT DEFAULT '',
    notas TEXT DEFAULT '' 
);  --    NEW! 24/08/2013
    -- GRANT ALL ON linea_de_presupuesto TO geotexan;
    -- GRANT ALL ON linea_de_presupuesto_id_seq TO geotexan;


--------------------
-- Albarán salida --
--------------------
CREATE TABLE albaran_salida(
    id SERIAL PRIMARY KEY,
    numalbaran TEXT UNIQUE,
    transportista_id INT REFERENCES transportista DEFAULT NULL,
    cliente_id INT REFERENCES cliente DEFAULT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    -- Datos de la dirección de envío:
    nombre TEXT DEFAULT '',
    direccion TEXT DEFAULT '',
    cp TEXT DEFAULT '',
    ciudad TEXT DEFAULT '',
    telefono TEXT DEFAULT '',
    pais TEXT DEFAULT '',
    observaciones TEXT DEFAULT '',
    -- Nuevos campos
    facturable BOOLEAN DEFAULT TRUE,
        -- Si False, el albarán no se puede facturar.
    motivo TEXT DEFAULT '',
        -- Motivo por el que el albarán no puede ser facturado.
    bloqueado BOOLEAN DEFAULT FALSE,
        -- Si True, el albarán solo lo puede modificar un usuario
        -- con nivel de privilegios <= 1.
    destino_id INT REFERENCES destino DEFAULT NULL, 
    almacen_origen_id INT REFERENCES almacen DEFAULT NULL, 
        -- Aunque en realidad por defecto será el almacén principal, pero a la 
        -- hora de crear el registro no se puede definir.
    almacen_destino_id INT REFERENCES almacen DEFAULT NULL
);

-----------
-- Lotes --
-----------
CREATE TABLE lote(
    id SERIAL PRIMARY KEY,
    numlote INT8 UNIQUE,
    codigo TEXT DEFAULT '',
    tenacidad CHAR(1) DEFAULT ' ',
    elongacion CHAR(1) DEFAULT ' ',
    rizo TEXT DEFAULT '',
    encogimiento TEXT DEFAULT '',
    grasa FLOAT DEFAULT 0.0,
    tolerancia FLOAT DEFAULT 0.20,  -- "Delta" o nivel de tolerancia o umbral
        -- entre el título medio obtenido a partir de las pruebas de título y
        -- el DTEX del artículo que se intentó fabricar. En tanto por ciento.
        -- Por defecto, 0.20 (+/- 20% del título del artículo).
    mediatitulo FLOAT DEFAULT 0,
    observaciones TEXT DEFAULT ''   -- NEW! 05/03/07.
);

-- XXX CAMBIO IMPORTANTE (01/11/2006):
-- Antes de restaurar la BD hay que crear en caliente la tabla, duplicar las
-- partidas de geotextiles y modificar las balas para que apunten a
-- partida_cuarto. Después crear copia y restaurar la BD con las tablas nuevas
-- y datos.
-- AL LORO: Hacer primero en una BD de pruebas, porque la mía me la he cargado
-- en el proceso Y DESPUÉS NO SE PUEDE RECUPERAR (a no ser que se tire de un
-- tablas.sql antiguo).

-- CREATE TABLE partida_carga... (copiar de abajo)
-- ginn=# INSERT INTO partida_carga(numpartida, codigo) SELECT
-- partida.numpartida, partida.codigo FROM partida;
-- INSERT 0 582
-- ginn=# ALTER TABLE bala ADD COLUMN partida_carga_id INT REFERENCES
-- partida_carga;
-- ALTER TABLE
-- ginn=# UPDATE bala SET partida_carga_id = (SELECT id FROM partida_carga
-- WHERE partida_carga.numpartida = (SELECT partida.numpartida FROM partida
-- WHERE partida.id = bala.partida_id));
-- UPDATE 17899
-- ginn=# SELECT bala.numbala, partida.numpartida, partida_carga.numpartida
-- FROM bala, partida, partida_carga WHERE bala.partida_id = partida.id AND
-- bala.partida_carga_id = partida_carga.id;
-- ginn=# ALTER TABLE bala DROP COLUMN partida_id;
-- ALTER TABLE
-- ginn=# ALTER TABLE partida ADD COLUMN partida_carga_id INT REFERENCES
-- partida_carga;
-- ALTER TABLE
-- ginn=# UPDATE partida SET partida_carga_id = (SELECT partida_carga.id FROM
-- partida_carga WHERE partida_carga.numpartida = partida.numpartida);
-- UPDATE 582

-- Después de todo esto, VERIFICAR que partida_carga se crea ANTES que partida
-- en el dump_datos.sql antes de restaurar.



-----------------------------------
-- Partidas de carga de cuartos. --
-----------------------------------
CREATE TABLE partida_carga(
    id SERIAL PRIMARY KEY,
    numpartida INT8 UNIQUE,
    codigo TEXT DEFAULT '',
    fecha TIMESTAMP DEFAULT LOCALTIMESTAMP(0)
);

------------------
-- Rollos malos --
-----------------------------------------
-- No cuentan para el almacén, pero sí --
-- para el cuadrar los consumos.       --
-- Van en tabla aparte porque llevan   --
-- numeración independiente, medidas   --
-- independientes, etc...              --
-----------------------------------------
-- CREATE TABLE rollo_defectuoso(
--    id SERIAL PRIMARY KEY,
--    producto_venta_id INT REFERENCES producto_venta NOT NULL,
-- Producto de venta que se intentó fabricar.
--    parte_de_produccion_id INT REFERENCES parte_de_produccion DEFAULT NULL,
-- Parte de producción donde se fabricó.
--    numrollo INT8 UNIQUE,
--    codigo TEXT DEFAULT '',     -- Será X-numrollo
--    fechahora TIMESTAMP DEFAULT LOCALTIMESTAMP(0),
--    observaciones TEXT DEFAULT '',
--    peso FLOAT DEFAULT 0,       -- Peso del rollo CON EMBALAJE
--    metros_lineales FLOAT DEFAULT 0,    -- Metros lineales del rollo
-- (no coinciden con el del producto, por eso es defectuoso).
--    ancho FLOAT DEFAULT 0
--    albaran_salida_id INT REFERENCES albaran_salida DEFAULT NULL,
-- Algún día puede que se vendan, pero
-- como todavía ni es seguro ni sé cómo hacerlo (¿cómo se vendería, como el
-- producto original, como otro
-- producto especial tipo "restos de geotextiles"? ¿con qué precio? ¿cómo se
-- facturaría?), de momento no creo este campo.
--);    -- Me gusta más el enfoque que le estoy dando ahora (07/03/2007)

-- XXX ------------------------------------


--------------
-- Partidas --
--------------
CREATE TABLE partida(
    id SERIAL PRIMARY KEY,
    numpartida INT8 UNIQUE,
    codigo TEXT DEFAULT '',
    gramaje FLOAT DEFAULT 0,
    longitudinal FLOAT DEFAULT 0,
    alongitudinal FLOAT DEFAULT 0,
    transversal FLOAT DEFAULT 0,
    atransversal FLOAT DEFAULT 0,
    compresion FLOAT DEFAULT 0,
    perforacion FLOAT DEFAULT 0,
    espesor FLOAT DEFAULT 0,
    permeabilidad FLOAT DEFAULT 0,
    poros FLOAT DEFAULT 0,
    -- XXX CAMBIO IMPORTANTE (01/11/2006):
    partida_carga_id INT REFERENCES partida_carga DEFAULT NULL,
    -- XXX ------------------------------
    observaciones TEXT DEFAULT '',  -- NEW! 05/03/07.
    -- NEW! 13/06/2011: Nueva prueba para certificado de calidad ASQUAL
    piramidal FLOAT DEFAULT 0
);

-----------
-- Balas --
-----------
CREATE TABLE bala(
    id SERIAL PRIMARY KEY,
    lote_id INT REFERENCES lote,
    -- XXX (01/11/2006) Este campo hay que borrarlo antes de hacer la copia de
    -- seguridad:
    --    partida_id INT REFERENCES partida DEFAULT NULL,
    ---------------------------------------------------------------
        -- Si partida != NULL, la bala se ha usado para fabricar una (o parte
        -- de una) partida de rollos. No se enlaza el lote completo con una o
        -- varias partidas porque los operarios introducen códigos de balas al
        -- fabricar una partida de rollos.
    numbala INT8 UNIQUE,
    codigo TEXT DEFAULT '',
    pesobala FLOAT DEFAULT 0.0,
    fechahora TIMESTAMP DEFAULT LOCALTIMESTAMP(0),
    muestra BOOLEAN DEFAULT False,
    -- observaciones TEXT DEFAULT '',    -- Por compatibilidad hacia atrás, el
        -- campo observaciones es equivalente al de motivo.
    claseB BOOLEAN DEFAULT False,   -- Las balas tipo B no son adecuadas para
        -- producir, solo para vender.
    motivo TEXT DEFAULT '',         -- Motivo por el cual la calidad de la
        -- bala es B.
    -- XXX (01/11/2006) Aquí está el campo nuevo que hay que crear:
    partida_carga_id INT REFERENCES partida_carga DEFAULT NULL
    ---------------------------------------------------------------
);

-------------------------------
-- Lotes de fibra de cemento --
-------------------------------------------------------
-- NEW! 12/12/2006: Campos de tenacidad en adelante. --
-------------------------------------------------------
CREATE TABLE lote_cem(
    id SERIAL PRIMARY KEY,
    numlote INT8 UNIQUE,
    codigo TEXT DEFAULT '',
    tenacidad FLOAT DEFAULT NULL,       -- A diferencia de los Lotes de fibra,
                                        -- aquí se almacenan directamente los
    elongacion FLOAT DEFAULT NULL,      -- valores medios de las pruebas.
    encogimiento FLOAT DEFAULT NULL,    -- Un valor nulo indica que no se han
                                        -- realizado pruebas de ese tipo.
    grasa FLOAT DEFAULT NULL,
    tolerancia FLOAT DEFAULT 0.20,  -- "Delta" o nivel de tolerancia o umbral
                                    -- entre el título medio obtenido a partir
                                    -- de las pruebas de título y el DTEX del
                                    -- artículo que se intentó fabricar. En
                                    -- tanto por ciento. Por defecto, 0.20
                                    -- (+/- 20% del título del artículo).
    humedad FLOAT DEFAULT NULL,
    mediatitulo FLOAT DEFAULT 0.0,
    observaciones TEXT DEFAULT ''   -- NEW! 05/03/07.
);

-------------
-- BigBags --
-------------
CREATE TABLE bigbag(
    id SERIAL PRIMARY KEY,
    lote_cem_id INT REFERENCES lote_cem,
    numbigbag INT8 UNIQUE,
    codigo TEXT DEFAULT '',
    pesobigbag FLOAT DEFAULT 0.0,
    fechahora TIMESTAMP DEFAULT LOCALTIMESTAMP(0),
    muestra BOOLEAN DEFAULT FALSE,
    claseB BOOLEAN DEFAULT FALSE,   -- Los bigbag tipo B se pueden vender,
                                    -- pero mejor tenerlos controlados porque
                                    -- pueden contener trozos de cuchillas,
                                    -- llevar fibra mal cortada, etc...
    motivo TEXT DEFAULT '',         -- Motivo por el cual la calidad del
                                    -- bigbag es B.
    parte_de_produccion_id INT REFERENCES parte_de_produccion DEFAULT NULL
        -- Parte de producción en el que se ha consumido el bigbag para 
        -- fabricar bolsas de fibra de cemento.
);

-------------------------------
-- Palés de fibra de cemento --
-------------------------------
CREATE TABLE pale(
    id SERIAL PRIMARY KEY,
    partida_cem_id INT REFERENCES partida_cem,
    numpale INT8 UNIQUE, 
    codigo TEXT,    -- Empezarán por H
    fechahora TIMESTAMP DEFAULT LOCALTIMESTAMP(0),
    numbolsas INT,  -- Bolsas por caja. Es campo calculado, pero por optimizar.
    numcajas INT DEFAULT 14,    -- Se supone que siempre serán 14.
    observaciones TEXT DEFAULT ''
);

-------------------------------
-- Cajas de fibra de cemento --
-------------------------------
CREATE TABLE caja(
    id SERIAL PRIMARY KEY,
    pale_id INT REFERENCES pale, 
    numcaja INT8 UNIQUE, 
    codigo TEXT,    -- Empezarán por J
    fechahora TIMESTAMP DEFAULT LOCALTIMESTAMP(0),
    -- Número de bolsas es campo calculado: ord(enlaces bolsa->caja)
    observaciones TEXT DEFAULT '', 
    numbolsas INT,  -- NEW! 09/09/2009
    peso FLOAT      -- NEW! 11/09/2009  (en kg)
);

------------
-- Rollos --
------------
CREATE TABLE rollo(
    id SERIAL PRIMARY KEY,
    partida_id INT REFERENCES partida,
    numrollo INT8 UNIQUE,
    codigo TEXT DEFAULT '',
    fechahora TIMESTAMP DEFAULT LOCALTIMESTAMP(0),
    observaciones TEXT DEFAULT '',
    muestra BOOLEAN DEFAULT FALSE,
    peso FLOAT DEFAULT 0,       -- Peso del rollo CON EMBALAJE
    densidad FLOAT DEFAULT 0,   -- Densidad en gr/m² del rollo. Puede variar
                                -- respecto a la densidad del producto.
                                -- Es campo calculado. Lo guardo por
                                -- eficiencia. (No estaría mal un trigger.)
    rollob BOOLEAN DEFAULT FALSE   -- NEW! 06/03/2007. True si el rollo es
        -- defectuoso. OJO: No se llama claseB como en bigbags y balas.
);

------------------------
-- Rollos defectuosos --
------------------------------------------------------------------
-- NEW! 07/03/2007                                              --
-- Rollos defectuosos. No comparten numeración con los          --
-- rollos "normales" y son de clase inferior a los              --
-- rollos B (aunque ni siquiera se estén usando actualmente).   --
-- Son rollo que se quedaron cortos de peso, de metros lineales --
-- con ancho isuficiente, etc...                                --
------------------------------------------------------------------
CREATE TABLE rollo_defectuoso(
    id SERIAL PRIMARY KEY,
    partida_id INT REFERENCES partida,  -- Pertenece a la partida del parte en
                                        -- que se fabricó, aunque no comparta
                                        -- características al 100%.
    numrollo INT8 UNIQUE,               -- Número de rollo defectuoso.
    codigo TEXT DEFAULT '',             -- Código del rollo: "X%d" % (numrollo)
    fechahora TIMESTAMP DEFAULT LOCALTIMESTAMP(0),  -- Fechahora de
                                                    -- fabricación.
    observaciones TEXT DEFAULT '',      -- Observaciones: por ejemplo, motivo
                                        -- por el que es un rollo defectuoso.
    peso FLOAT DEFAULT 0.0,             -- Peso del rollo CON EMBALAJE
    densidad FLOAT DEFAULT 0.0,         -- Densidad en gr/m² del rollo. Puede
                                        -- variar respecto a la densidad del
                                        -- producto.
    metros_lineales FLOAT DEFAULT 0.0,  -- Metros lineales del rollo. Se
                                        -- supone que diferente a los del
                                        -- producto, por eso es defectuoso.
    ancho FLOAT DEFAULT 0.0,            -- Ancho del rollo (al no tener
                                        -- producto estrictamente, el ancho
                                        -- del producto original lo guardo
                                        -- aquí).
    peso_embalaje FLOAT DEFAULT 0.0     -- Peso del embalaje que estaba
                                        -- guardado en el producto que se
                                        -- intentó fabricar.
);

--------------------
-- Balas de cable --
------------------------------------------------------------------
-- NEW! 13/06/2007                                              --
-- Balas de cable de fibra para reciblar.                       --
-- No se agrupan en lotes. Llevan numeración independiente.     --
-- Sólo se tiene en cuenta si son de fibra negra/natural y el   --
-- peso de cada bala.                                           --
------------------------------------------------------------------
CREATE TABLE bala_cable(
    id SERIAL PRIMARY KEY,
    numbala INT8 UNIQUE,                -- Número de bala de cable.
    codigo TEXT DEFAULT '',             -- Código de la bala: "Z%d" % (numbala)
    fechahora TIMESTAMP DEFAULT LOCALTIMESTAMP(0),
        -- Fechahora de fabricación.
    observaciones TEXT DEFAULT '',      -- Observaciones.
    peso FLOAT DEFAULT 0.0,             -- Peso CON EMBALAJE
    peso_embalaje FLOAT DEFAULT 0.0,
        -- Peso del embalaje. Sería recomendable estimarlo porque cuando se
        -- recicle es peso que se pierde.
    color TEXT DEFAULT '',
        -- En principio debería ser "Negra/Natural" y copiarse directamente de
        -- la descripción del producto.
    claseB BOOLEAN DEFAULT TRUE 
    --claseB BOOLEAN DEFAULT False
        -- Una bala de cable podría ser de claseB si por ejemplo lleva
        -- residuos o plásticos (criterio aún por decidir y que no sé si
        -- se llegará a usar).
        -- Actualización 14/09/09: Una bala de cable será siempre de clase C. 
        -- Tal vez algún día se distingan balas de cable de clase A y B, pero 
        -- hasta entonces todas son C, al igual que los rollos_c. 
);

----------------
-- Rollos «C» --
----------------------------------------------------------------
-- NEW! 02/06/2008                                            --
-- Rollos de geotextiles de anchos y categorías heterogéneos. --
-- Equivalente a balas de cable "Z" en geotextiles.           --
----------------------------------------------------------------
CREATE TABLE rollo_c(
    id SERIAL PRIMARY KEY,
    numrollo INT8 unique,       -- Número de RolloC.
    codigo TEXT DEFAULT '',     -- Código del rollo: "Y%d" % codigo
    fechahora TIMESTAMP DEFAULT LOCALTIMESTAMP(0),
    observaciones TEXT DEFAULT '',
    peso FLOAT DEFAULT 0.0,     -- Peso CON embalaje.
    peso_embalaje FLOAT DEFAULT 0.0
        -- Peso estimado del embalaje. A priori no se usará, pero puede
        -- ser interesante considerarlo en el futuro.
);

---------------
-- Artículos --
---------------
CREATE TABLE articulo(
    id SERIAL PRIMARY KEY,
    bala_id INT REFERENCES bala DEFAULT NULL,
    rollo_id INT REFERENCES rollo DEFAULT NULL,
    parte_de_produccion_id INT REFERENCES parte_de_produccion DEFAULT NULL,
    producto_venta_id INT REFERENCES producto_venta NOT NULL,
    albaran_salida_id INT REFERENCES albaran_salida DEFAULT NULL,
    bigbag_id INT REFERENCES bigbag DEFAULT NULL,
    rollo_defectuoso_id INT REFERENCES rollo_defectuoso DEFAULT NULL,
        -- NEW! 07/03/2007
    bala_cable_id INT REFERENCES bala_cable DEFAULT NULL,   -- NEW! 13/06/2007
    rollo_c_id INT REFERENCES rollo_c DEFAULT NULL,         -- NEW! 02/06/2008
    almacen_id INT REFERENCES almacen DEFAULT NULL,  
    caja_id INT REFERENCES caja DEFAULT NULL,     -- NEW! 18/05/2009
    CHECK (   (bala_id IS NOT NULL 
               AND rollo_id IS NULL 
               AND bigbag_id IS NULL 
               AND rollo_defectuoso_id IS NULL 
               AND bala_cable_id IS NULL 
               AND rollo_c_id IS NULL 
               AND caja_id IS NULL) 
           OR (bala_id IS NULL 
               AND rollo_id IS NOT NULL 
               AND bigbag_id IS NULL 
               AND rollo_defectuoso_id IS NULL 
               AND bala_cable_id IS NULL 
               AND rollo_c_id IS NULL 
               AND caja_id IS NULL) 
           OR (bala_id IS NULL 
               AND rollo_id IS NULL 
               AND bigbag_id IS NOT NULL 
               AND rollo_defectuoso_id IS NULL 
               AND bala_cable_id IS NULL 
               AND rollo_c_id IS NULL 
               AND caja_id IS NULL) 
           OR (bala_id IS NULL 
               AND rollo_id IS NULL 
               AND bigbag_id IS NULL 
               AND rollo_defectuoso_id IS NOT NULL 
               AND bala_cable_id IS NULL 
               AND rollo_c_id IS NULL 
               AND caja_id IS NULL) 
           OR (bala_id IS NULL 
               AND rollo_id IS NULL 
               AND bigbag_id IS NULL 
               AND rollo_defectuoso_id IS NULL 
               AND bala_cable_id IS NOT NULL 
               AND rollo_c_id IS NULL 
               AND caja_id IS NULL) 
           OR (bala_id IS NULL 
               AND rollo_id IS NULL 
               AND bigbag_id IS NULL 
               AND rollo_defectuoso_id IS NULL 
               AND bala_cable_id IS NULL 
               AND rollo_c_id IS NOT NULL 
               AND caja_id IS NULL) 
           OR (bala_id IS NULL 
               AND rollo_id IS NULL 
               AND bigbag_id IS NULL 
               AND rollo_defectuoso_id IS NULL 
               AND bala_cable_id IS NULL 
               AND rollo_c_id IS NULL 
               AND caja_id IS NOT NULL)) 
);


----------------------------------------------------------
-- Líneas de transferencia de mercancía entre almacenes --
----------------------------------------------------------
-- Aunque el almacén origen y destino pudiera parecer que son 
-- atributos de esta tabla, en realidad son comunes a todas las líneas 
-- del mismo albarán interno de transferencia. Esto debería ser una 
-- tabla generada automáticamente por la relación muchos a muchos entre 
-- el albarán de salida y los artículos, pero no me fío de dejarlo automático.
CREATE TABLE linea_de_movimiento(
    id SERIAL PRIMARY KEY, 
    albaran_salida_id INT REFERENCES albaran_salida, 
    articulo_id INT REFERENCES articulo 
);

--------------------------------
-- Tabla de facturas de venta --
--------------------------------
CREATE TABLE factura_venta(
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES cliente,
    fecha DATE DEFAULT CURRENT_DATE,
    numfactura TEXT,
    descuento FLOAT DEFAULT 0.0,
    cargo NUMERIC(9, 2) DEFAULT 0.0,
    observaciones TEXT DEFAULT '',
    iva FLOAT DEFAULT 0.21,    -- Si el cliente no tiene un IVA válido
                               -- definido, se usará el 21%.
    -- OJO: No se tiene en cuenta Recargo de Equivalencia por petición expresa
    -- en documento de requisitos.
    bloqueada BOOLEAN DEFAULT False,
        -- Campo de factura bloqueada para impedir cambios una vez se imprima
        -- y entregue al cliente.
        -- No estoy seguro de que se llegue a usar, pero por si acaso la
        -- incluyo.
    irpf FLOAT DEFAULT 0.0, -- NEW! 10/04/07. Si en datos_de_la_empresa
                            -- irpf != 0.0, aparecerá en la ventana y se
                            -- aplicará a la B.I.
    obra_id INT REFERENCES obra DEFAULT NULL    -- NEW! 26/05/2009
);

--------------------------------
-- Tabla de facturas proforma --
-- o prefacturas.             --
--------------------------------
CREATE TABLE prefactura(
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES cliente,
    fecha DATE DEFAULT CURRENT_DATE,
    numfactura TEXT,
    descuento FLOAT DEFAULT 0.0,
    cargo NUMERIC(9, 2) DEFAULT 0.0,
    observaciones TEXT DEFAULT '',
    iva FLOAT DEFAULT 0.21,     -- Si el cliente no tiene un IVA válido
                                -- definido, se usará el 21%.
    -- OJO: No se tiene en cuenta Recargo de Equivalencia por petición expresa
    -- en documento de requisitos.
    bloqueada BOOLEAN DEFAULT False,
        -- Campo de factura bloqueada para impedir cambios una vez se imprima
        -- y entregue al cliente.
        -- No estoy seguro de que se llegue a usar, pero por si acaso la
        -- incluyo.
    irpf FLOAT DEFAULT 0.0  -- NEW! 10/04/07. Si en datos_de_la_empresa
        -- irpf != 0.0, aparecerá en la ventana y se aplicará a la B.I.
);

------------------------------
-- Tickets de venta por TPV --
------------------------------
-- NEW! 19/04/07            --
------------------------------
CREATE TABLE ticket(
    id SERIAL PRIMARY KEY,
    fechahora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    numticket INT8 -- UNIQUE       -- No es UNIQUE. Cada año se vuelve a 1.
);

---------------------
-- Líneas de venta --
---------------------
-- DONE: Empiezo a echar en falta un campo de observaciones aquí para
-- poder poner anotaciones en las facturas y que se impriman junto a cada
-- concepto.
CREATE TABLE linea_de_venta(
    id SERIAL PRIMARY KEY,
    producto_venta_id INT REFERENCES producto_venta,
    pedido_venta_id INT REFERENCES pedido_venta,
    albaran_salida_id INT REFERENCES albaran_salida DEFAULT NULL,
    factura_venta_id INT REFERENCES factura_venta DEFAULT NULL,
    prefactura_id INT REFERENCES prefactura DEFAULT NULL,
    fechahora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cantidad FLOAT,
    precio FLOAT DEFAULT 0.0,
    descuento FLOAT DEFAULT 0.0,
    --    NEW! 23/22/06
    producto_compra_id INT REFERENCES producto_compra DEFAULT NULL,
    ticket_id INT REFERENCES ticket DEFAULT NULL, -- NEW! 19/04/07
    notas TEXT DEFAULT '',  -- NEW! 28/11/07 Campo para guardar anotaciones
                            -- sobre una LDV.
                            -- No son estrictamente observaciones (que según
                            -- el to-do se imprimirían en la factura). Son
                            -- notas para uso interno del usuario, visibles
                            -- solo en pantalla.
    descripcion_complementaria TEXT DEFAULT '',     -- NEW! 30/11/07
        -- Descripción complementaria. Editable por usuario.
    CHECK (producto_compra_id IS NULL +^ producto_venta_id IS NULL)
);

----------------------
-- Líneas de pedido --
-- NEW! 08/10/06 CWT--
----------------------
CREATE TABLE linea_de_pedido(
    id SERIAL PRIMARY KEY,
    producto_venta_id INT REFERENCES producto_venta,
    pedido_venta_id INT REFERENCES pedido_venta,
    fechahora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cantidad FLOAT,
    precio FLOAT DEFAULT 0.0,
    descuento FLOAT DEFAULT 0.0,
    fecha_entrega DATE DEFAULT CURRENT_DATE,    -- NEW! 08/10/06
    texto_entrega TEXT DEFAULT '',    -- NEW! 08/10/06
    --    NEW! 26/12/06
    producto_compra_id INT REFERENCES producto_compra DEFAULT NULL,
    presupuesto_id INT REFERENCES presupuesto DEFAULT NULL, -- NEW! 15/03/07
    notas TEXT DEFAULT ''       -- NEW! 29/11/07
);

------------------------------------------
-- Tabla de servicios facturables       --
-- (Servicios prestados por la empresa) --
------------------------------------------
CREATE TABLE servicio(
    id SERIAL PRIMARY KEY,
    factura_venta_id INT REFERENCES factura_venta,
    prefactura_id INT REFERENCES prefactura DEFAULT NULL,
    albaran_salida_id INT REFERENCES albaran_salida DEFAULT NULL,
    concepto TEXT,
    cantidad FLOAT DEFAULT 1.0,
    precio FLOAT,
    descuento FLOAT DEFAULT 0.0,
    pedido_venta_id INT REFERENCES pedido_venta DEFAULT NULL,
    presupuesto_id INT REFERENCES presupuesto DEFAULT NULL, -- NEW! 15/03/07
    notas TEXT DEFAULT ''   -- NEW! 28/11/07
);

---------------------------------
-- Tabla de facturas de compra --
---------------------------------
CREATE TABLE factura_compra(
    id SERIAL PRIMARY KEY,
    proveedor_id INT REFERENCES proveedor,
    fecha DATE DEFAULT CURRENT_DATE,
    numfactura TEXT,
    descuento FLOAT DEFAULT 0.0,
    cargo NUMERIC(9,2) DEFAULT 0.0,
    iva FLOAT DEFAULT 0.21,
    bloqueada BOOLEAN DEFAULT FALSE,
        -- Estado se usará a modo de "flag" para indicar si la factura está
        -- marcada como bloqueada (bloqueada = aceptada, recibida y pagada, no
        -- admite cambios por parte del proveedor). Al igual que con las
        -- facturas de venta, aún no se usa este campo.
    visto_bueno_director BOOLEAN DEFAULT FALSE,
        -- NEW! 25/10/2006. Vto. bueno del director general. Si False, no se
        -- aprueba el pago de la factura.
    visto_bueno_comercial BOOLEAN DEFAULT FALSE,
        -- NEW! 25/10/2006. Vto. bueno del director comercial. Si False, no se
        -- aprueba el pago de la factura.
    visto_bueno_tecnico BOOLEAN DEFAULT FALSE,
        -- NEW! 25/10/2006. Vto. bueno del director técnico. Si False, no se
        -- aprueba el pago de la factura.
    fecha_entrada DATE DEFAULT CURRENT_DATE,
        -- NEW! 25/10/2006. Fecha de entrada de la factura (puede diferir de
        -- la fecha de la factura, que suele ser de emisión).
    fecha_visto_bueno_director DATE DEFAULT CURRENT_DATE,   -- Fecha en que se
        -- da el visto bueno.
    fecha_visto_bueno_comercial DATE DEFAULT CURRENT_DATE,  -- Todas estas
        -- columnas de vistos buenos son automáticas si la
    fecha_visto_bueno_tecnico DATE DEFAULT CURRENT_DATE,    -- factura tiene
        -- pedido y albarán y las cantidades y precios no son superiores a
        -- las de éstos.
    visto_bueno_usuario BOOLEAN DEFAULT FALSE,  -- Necesita una comprobación
        -- de totales del usuario para el vº. bueno auto.
    fecha_visto_bueno_usuario DATE DEFAULT NULL,
    observaciones TEXT DEFAULT '',   -- NEW! 15/02/07. Pues eso. Observaciones.
    vencimientos_confirmados BOOLEAN DEFAULT FALSE -- NEW! 29/08/2008. Para
        -- que no pregunte CADA vez si los vencimientos son correctos cuando 
        -- no coincidan con los del proveedor.
);

-------------------------
-- Líneas de de compra --
-------------------------
CREATE TABLE linea_de_compra(
    id SERIAL PRIMARY KEY,
    pedido_compra_id INT REFERENCES pedido_compra DEFAULT NULL,
    albaran_entrada_id INT REFERENCES albaran_entrada DEFAULT NULL,
    factura_compra_id INT REFERENCES factura_compra DEFAULT NULL,
    producto_compra_id INT REFERENCES producto_compra,
    cantidad FLOAT,
    precio FLOAT DEFAULT 0.0,   -- Sin IVA
    descuento FLOAT DEFAULT 0.0,
    --    factura_compra_id INT REFERENCES factura_compra DEFAULT NULL,
    entrega TEXT DEFAULT '',     -- Entrega estimada del contenido de la LDV
        -- (opcional, se escribe en pedidos de compra) NEW! 26/09/2006
    silo_id INT REFERENCES silo DEFAULT NULL,    -- NEW! 08/10/06
    carga_silo_id INT REFERENCES carga_silo DEFAULT NULL,   -- NEW! 01/11/06
        -- (Inhabilita silo_id, pero es tarde para quitarlo sin inutilizar las
        -- copias de seguridad)
    iva FLOAT DEFAULT 0.21      -- NEW! 15/02/07. IVA de la LDC. Por
        -- compatibilidad con los servicios de las facturas de compra con IVA
        -- mixto.
);

--------------------------------
-- Líneas de pedido de compra --
--------------------------------
-- NEW! 23/11/06              --
-----------------------------------------------------------------
-- Líneas de pedidos de compra. Funcionan igual que las líneas --
-- de pedido de pedidos de venta. Son las líneas que contienen --
-- el pedido original y a partir de las cuales se crean las    --
-- líneas de compra albaraneadas y/o facturadas.               --
-----------------------------------------------------------------
CREATE TABLE linea_de_pedido_de_compra(
    id SERIAL PRIMARY KEY,
    producto_compra_id INT REFERENCES producto_compra,
    pedido_compra_id INT REFERENCES pedido_compra,
    fechahora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cantidad FLOAT,
    precio FLOAT DEFAULT 0.0,
    descuento FLOAT DEFAULT 0.0,
    fecha_entrega DATE DEFAULT CURRENT_DATE,
    texto_entrega TEXT DEFAULT '',
    notas TEXT DEFAULT ''   -- NEW! 12/12/07. Meto aquí también la
                            -- columna notas.
);

----------------------------------------------------------------------------
-- Relación múltiple entre líneas de pedido de compra y líneas de compra. --
----------------------------------------------------------------------------
CREATE TABLE linea_de_pedido_de_compra__linea_de_compra(
    linea_de_pedido_de_compra_id INT NOT NULL
        REFERENCES linea_de_pedido_de_compra,
    linea_de_compra_id INT NOT NULL REFERENCES linea_de_compra
);

----------------------------------------
-- Transportes a cuenta de la empresa --
----------------------------------------------
-- NEW! 21/11/2006                          --
----------------------------------------------
-- Transportes pagados por la empresa de    --
-- los que se recibirá factura.             --
----------------------------------------------
CREATE TABLE transporte_a_cuenta(
    id SERIAL PRIMARY KEY,
    concepto TEXT DEFAULT '',
    precio FLOAT DEFAULT 0.0,
    observaciones TEXT DEFAULT '',
    fecha DATE DEFAULT CURRENT_DATE,
    albaran_salida_id INT REFERENCES albaran_salida DEFAULT NULL,
    proveedor_id INT REFERENCES proveedor DEFAULT NULL
);

---------------------------------------------
-- Comisiones de intermediarios soportadas --
----------------------------------------------
-- NEW! 21/11/2006                          --
----------------------------------------------
-- Comisiones que nos facturará un cliente  --
-- que actúa como intermediario en ventas.  --
----------------------------------------------
CREATE TABLE comision(
    id SERIAL PRIMARY KEY,
    concepto TEXT DEFAULT '',
    precio FLOAT DEFAULT 0.0,
    observaciones TEXT DEFAULT '',
    fecha DATE DEFAULT CURRENT_DATE,
    cliente_id INT REFERENCES cliente,  -- Cliente que actúa como intermediario
    factura_venta_id INT REFERENCES factura_venta DEFAULT NULL, -- Factura de
        -- venta sobre la que nos cobra comisión
    prefactura_id INT REFERENCES prefactura DEFAULT NULL, -- Factura de venta 
        -- sobre la que nos cobra comisión
    porcentaje FLOAT DEFAULT 0.0,   -- Porcentaje del importe de la 
                                    -- factura de venta para el intermediario
    albaran_salida_id INT REFERENCES albaran_salida DEFAULT NULL  -- CWT: Las
        -- comisiones que nos cobran se inician en el albarán.
        -- Generalmente 1 albarán - 1 factura de venta, pero es en la
        -- generación del albarán donde deben aparecer ya las comisiones.
        -- Creo que esto deja(rá) obsoleto el campo factura_venta_id.
);

------------------------
-- Servicios tomados. --
----------------------------------------------
-- NEW! 21/11/2006                          --
----------------------------------------------
-- Servicios prestados a la empresa que nos --
-- son facturados. No tienen albarán ni     --
-- pedido de compra.                        --
----------------------------------------------
CREATE TABLE servicio_tomado(
    id SERIAL PRIMARY KEY,
    factura_compra_id INT REFERENCES factura_compra,
    concepto TEXT DEFAULT '',
    cantidad FLOAT DEFAULT 0.0,
    precio FLOAT DEFAULT 0.0,
    descuento FLOAT DEFAULT 0.0,
    comision_id INT REFERENCES comision DEFAULT NULL,
    transporte_a_cuenta_id INT REFERENCES transporte_a_cuenta DEFAULT NULL,
    iva FLOAT DEFAULT 0.21      -- NEW! 15/02/07. IVA del servicio para
        -- facturas de compra "especiales" con IVA mixto. Si una
        -- factura de compra tiene servicios a diferentes IVAs, el IVA de la
        -- factura debe ser 0% e ignorarse.
);

--------------------------
-- Vencimientos de pago --
--------------------------
CREATE TABLE vencimiento_pago(
    id SERIAL PRIMARY KEY,
    factura_compra_id INT REFERENCES factura_compra,
    fecha DATE DEFAULT CURRENT_DATE,
    importe FLOAT DEFAULT 0.0,
    observaciones TEXT DEFAULT '', 
    procesado BOOLEAN DEFAULT FALSE,-- NEW! 06/02/2019 Si True, el programa no 
        -- tratará de crear el registro pago automático al pasar la fecha de 
        -- vencimiento.
    fecha_pagado DATE DEFAULT NULL   -- NEW! 06/02/2019 Fecha en que se 
        -- paga el vencimiento. Se usa para las domiciliaciones automáticas.
    -- ALTER TABLE vencimiento_pago ADD COLUMN procesado BOOLEAN DEFAULT FALSE; UPDATE vencimiento_pago SET procesado = FALSE; ALTER TABLE vencimiento_pago ADD COLUMN fecha_pagado DATE DEFAULT NULL; UPDATE vencimiento_pago SET fecha_pagado = NULL;
    );

----------------------------------------
-- Tabla para importar datos de LOGIC --
----------------------------------------
-- Habrá registros relacionados con los pagos, se tomarán los datos de esta
-- tabla para crear el pago asociado al pagaré, etc. Pero se crea también una
-- relación 1 a 1 para evitar mostrarlo al crear un nuevo pagaré (usabilidad)
-- o borrarlo al reimportar todos los datos de nuevo (también habrá que
-- evitar que se importen registros que ya existen o se han usado en pagos).
CREATE TABLE logic_movimientos(
    id SERIAL PRIMARY KEY,
    asiento INT8 DEFAULT 0,     -- Campos de la tabla Movimientos
    orden INT8 DEFAULT 0,
    fecha DATE DEFAULT NULL,
    cargo_abono CHAR,
    codigo_cuenta TEXT DEFAULT '',
    contrapartida_info TEXT DEFAULT '',
    comentario TEXT,
    importe FLOAT,
    cuenta TEXT DEFAULT ''  -- Nombre de la cuenta, obtenido de PlanDeCuentas.
);

-----------------------------------------------
-- Tabla de pagarés para pagos a proveedores --
-- NEW! 25 de mayo de 2006                   --
-----------------------------------------------
CREATE TABLE pagare_pago(
    id SERIAL PRIMARY KEY,
    codigo TEXT DEFAULT '',                     -- Algún tipo de código
        -- identificativo o algo. No sé si lo llegaré a usar.
    fecha_emision DATE DEFAULT CURRENT_DATE,    -- Fecha en que se emite el
        -- pagaré.
    fecha_pago DATE DEFAULT NULL,  -- Fecha en que el pago del pagaré se
                                   -- realiza al completo.
    cantidad FLOAT,                -- Cantidad que cubre el pagaré.
    pagado FLOAT DEFAULT 0,        -- Pagado del pagaré hasta el momento.
    observaciones TEXT DEFAULT '', 
    procesado BOOLEAN DEFAULT FALSE,-- Si True, el programa no 
        -- cambiará el estado del pagaré de "pendiente" a "pagado" de forma 
        -- automática.
    fecha_cobrado DATE DEFAULT NULL   -- Fecha en que se paga el pagaré     
        -- definitivamente. Tanto por cumplirse el vencimiento como por 
        -- haberse negociado. Si cobrado >= cantidad, este campo guarda la 
        -- fecha en que se ha realizado el cobro y el confirming ha dejado de 
        -- estar pendiente.
);

--------------------------------------------------
-- Tabla de cuentas destino para transferencias --
--------------------------------------------------
-- NEW! 21/02/07 --
-------------------
CREATE TABLE cuenta_destino(
    id SERIAL PRIMARY KEY,
    nombre TEXT DEFAULT '',
    observaciones TEXT DEFAULT '',
    banco TEXT DEFAULT '',     -- Copiado tal cual de la tabla de proveedores.
    swif TEXT DEFAULT '',      -- Copiado tal cual de la tabla de proveedores.
    iban TEXT DEFAULT '',      -- Copiado tal cual de la tabla de proveedores.
    cuenta TEXT DEFAULT '',    -- Copiado tal cual de la tabla de proveedores.
    nombre_banco TEXT DEFAULT '',   -- Copiado tal cual de la tabla de
                                    -- proveedores.
    proveedor_id INT REFERENCES proveedor DEFAULT NULL  -- Proveedor al que
                                                        -- pertenece la cuenta
);

--------------------
-- Tabla de pagos --
--------------------
CREATE TABLE pago(
    id SERIAL PRIMARY KEY,
    factura_compra_id INT REFERENCES factura_compra,
    logic_movimientos_id INT REFERENCES logic_movimientos DEFAULT NULL,
        -- Registro de LOGIC relacionado.
    fecha DATE DEFAULT CURRENT_DATE,
    importe FLOAT DEFAULT 0.0,
    observaciones TEXT DEFAULT '',
    pagare_pago_id INT REFERENCES pagare_pago DEFAULT NULL,
    proveedor_id INT REFERENCES proveedor DEFAULT NULL,
    cuenta_origen_id INT REFERENCES cuenta_origen DEFAULT NULL,
        -- NEW! 21/02/07. Cuenta bancaria origen para las transferencias.
    cuenta_destino_id INT REFERENCES cuenta_destino DEFAULT NULL, 
        -- NEW! 21/02/07. Cuenta bancaria destino para las transferencias.
    concepto_libre TEXT DEFAULT ''    -- Concepto editable para transferencias.
);

-----------------------------------
-- Tabla de estimaciones de pago --
-----------------------------------
CREATE TABLE estimacion_pago(
    id SERIAL PRIMARY KEY,
    factura_compra_id INT REFERENCES factura_compra,
    fecha DATE DEFAULT CURRENT_DATE,
    importe FLOAT DEFAULT 0.0,
    observaciones TEXT DEFAULT ''
);

-----------------------
-- Recibos bancarios --
-----------------------
-- NEW! 22/05/07 --
-------------------
CREATE TABLE recibo(
    id SERIAL PRIMARY KEY,
    numrecibo INT,
    anno INT,   -- Imagino que por defecto será el año de la
                -- fecha_libramiento, pero por si acaso pondré por defecto el
                -- año actual en el "constructor".
    -- numrecibo será "calculado" = numrecibo/anno
    lugar_libramiento TEXT DEFAULT '',
    fecha_libramiento DATE DEFAULT CURRENT_DATE,
    -- importe será un campo calculado con la suma de los vencimientos
    -- relacionados. factura será un texto con los números de factura de cada
    -- vencimiento separados por coma. fecha factura se tratará igual que el
    -- campo factura cliente será el cliente del primero de los vencimientos.
    fecha_vencimiento DATE DEFAULT CURRENT_DATE,    -- Por defecto deberá ser
        -- la fecha del primero de los vencimientos,
        -- pero permito editarla por si hay varios o algo.
    -- vencimiento_cobro_id INT REFERENCES vencimiento_cobro, -- Importe,
        -- factura, fecha factura, cliente y (fecha) vencimiento lo coge del
        -- registro vencimiento relacionado.
    persona_pago TEXT DEFAULT '', -- Supongo que lo sacaré de DDE por defecto.
    domicilio_pago TEXT DEFAULT '', -- Ídem
    cuenta_origen_id INT REFERENCES cuenta_origen DEFAULT NULL,  -- Cuenta
        -- bancaria de la empresa para el cobro. OBSOLETO. UNUSED.
    nombre_librado TEXT DEFAULT '', -- Por defecto lo sacaré del cliente, pero
        -- por si acaso dejo editable como campo.
    direccion_librado TEXT DEFAULT '',  -- Ídem
    observaciones TEXT DEFAULT '',      -- No se usará en un futuro inmediato,
        -- pero nunca se sabe.
    cuenta_bancaria_cliente_id INT
        REFERENCES cuenta_bancaria_cliente DEFAULT NULL  -- Cuenta del cliente
        -- donde cargar el recibo.
);

---------------------------
-- Vencimientos de cobro --
---------------------------
CREATE TABLE vencimiento_cobro(
    id SERIAL PRIMARY KEY,
    factura_venta_id INT REFERENCES factura_venta,
    prefactura_id INT REFERENCES prefactura DEFAULT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    importe FLOAT DEFAULT 0.0,
    observaciones TEXT DEFAULT '',
    cuenta_origen_id INT
        REFERENCES cuenta_origen DEFAULT NULL, -- NEW! 26/02/07. Cuenta
        -- bancaria _destino_ para la transferencia.
        -- Se llama cuenta_origen por motivos de compatibilidad, pero en
        -- realidad es la cuenta de la "propia_empresa" donde el cliente
        -- debe hacer la transferencia.
    recibo_id INT REFERENCES recibo DEFAULT NULL    -- NEW! 22/05/07
);

---------------------
-- Tabla de bancos --
---------------------
CREATE TABLE banco(
    id SERIAL PRIMARY KEY, 
    nombre TEXT, 
    iban TEXT DEFAULT '', -- 34 caracteres [http://es.wikipedia.org/wiki/IBAN]
    direccion TEXT DEFAULT '',  
    ciudad TEXT DEFAULT '', 
    provincia TEXT DEFAULT '', 
    pais TEXT DEFAULT 'España', 
    contacto TEXT DEFAULT '', 
    web TEXT DEFAULT '', 
    telefono TEXT DEFAULT '', 
    fax TEXT DEFAULT '', 
    -- Línea descuento 
    limite FLOAT DEFAULT NULL, 
    interes FLOAT DEFAULT NULL, 
    comision_estudio FLOAT DEFAULT NULL, 
    concentracion FLOAT DEFAULT NULL, 
    exceso_vencimiento INT DEFAULT NULL
);

-------------------------------------------------
-- Concentración clientes en remesas de bancos --
-------------------------------------------------
CREATE TABLE concentracion_remesa(
    id SERIAL PRIMARY KEY, 
    banco_id INT NOT NULL REFERENCES banco, 
    cliente_id INT NOT NULL REFERENCES cliente, 
    concentracion FLOAT
);

------------------------
-- Remesas de pagarés --
------------------------
CREATE TABLE remesa(
    id SERIAL PRIMARY KEY, 
    banco_id INT REFERENCES banco DEFAULT NULL, 
    fecha_prevista DATE DEFAULT NULL, 
    codigo TEXT DEFAULT '', 
    fecha_cobro DATE DEFAULT NULL, 
    aceptada BOOLEAN DEFAULT FALSE
);

-----------------------
-- Tablas de Pagarés --
-- NEW! 25/05/2006   --
-----------------------
CREATE TABLE pagare_cobro(
    id SERIAL PRIMARY KEY,
    codigo TEXT DEFAULT '',                     -- Algún tipo de código
        -- identificativo o algo. No sé si lo llegaré a usar.
    fecha_recepcion DATE DEFAULT CURRENT_DATE,  -- Fecha en que se recibe el
        -- pagaré.
    fecha_cobro DATE DEFAULT NULL,  -- Fecha en que el cobro del
        -- pagaré se realiza al completo. Se usa como vencimiento del pagaré.
    cantidad FLOAT,     -- Cantidad que cubre el pagaré.
    cobrado FLOAT DEFAULT 0,    -- Cobrado del pagaré hasta el momento.
    observaciones TEXT DEFAULT '', 
    fecha_cobrado DATE DEFAULT NULL,   -- Fecha en que se cobra el pagaré 
        -- definitivamente. Tanto por cumplirse el vencimiento como por 
        -- haberse negociado. Si cobrado >= cantidad, este campo guarda la 
        -- fecha en que se ha realizado el cobro y el pagaré ha dejado de 
        -- estar pendiente.
    procesado BOOLEAN DEFAULT FALSE, -- Si True ya se ha procesado 
        -- automáticamente y no hace falta actualizar el estado al cumplir la 
        -- fecha de vencimiento.
    a_la_orden BOOLEAN DEFAULT TRUE, 
    banco_id INT REFERENCES banco DEFAULT NULL
    -- remesa_id INT REFERENCES remesa DEFAULT NULL
);

--------------------------
-- Tabla de confirmings --
----------------------------------------------------------------------
-- Como pagarés pero con los impagos cubiertos por el propio banco. --
-- Solo uso confirmings para cobrar. Ni se paga ni se emiten.       --
----------------------------------------------------------------------
CREATE TABLE confirming(
    id SERIAL PRIMARY KEY, 
    codigo TEXT DEFAULT '',     -- Número -o código- del confirming 
    fecha_recepcion DATE DEFAULT CURRENT_DATE, 
    fecha_cobro DATE DEFAULT NULL,  -- AKA vencimiento
    cantidad FLOAT,                 -- Cantidad cubierta
    cobrado FLOAT DEFAULT 0,        -- Cobrado hasta el momento. Generalmente 
        -- será 0 o la cantidad completa cuando llegue la fecha de vto.
    observaciones TEXT DEFAULT '', 
    fecha_cobrado DATE DEFAULT NULL,   -- Fecha en que se cobra el confirming
        -- definitivamente. Tanto por cumplirse el vencimiento como por 
        -- haberse negociado. Si cobrado >= cantidad, este campo guarda la 
        -- fecha en que se ha realizado el cobro y el confirming ha dejado de 
        -- estar pendiente.
    procesado BOOLEAN DEFAULT FALSE  -- Si True ya se ha procesado 
        -- automáticamente y no hace falta actualizar el estado al cumplir la 
        -- fecha de vencimiento.
    -- remesa_id INT REFERENCES remesa DEFAULT NULL
);      -- NEW! 20/11/2008

----------------------
-- Efectos de cobro --
-----------------------------------------------------
-- Tabla "padre" de pagarés de cobro y confirming. --
-----------------------------------------------------
CREATE TABLE efecto(
    id SERIAL PRIMARY KEY, 
    pagare_cobro_id INT REFERENCES pagare_cobro DEFAULT NULL, 
    confirming_id INT REFERENCES confirming DEFAULT NULL,
    cuenta_bancaria_cliente_id INT REFERENCES cuenta_bancaria_cliente DEFAULT NULL, 
    -- Ya me traeré a esta tabla campos comunes a confirming y pagarés para 
    -- optimizar las búsquedas con criterio más que nada.
    CHECK (pagare_cobro_id IS NULL +^ confirming_id IS NULL)
);      -- NEW! 17/01/2013

------------------------------------------------------------
-- Relación uno a muchos entre efectos de cobro y remesas --
------------------------------------------------------------
CREATE TABLE efecto__remesa(
    efecto_id INT NOT NULL REFERENCES efecto, 
    remesa_id INT NOT NULL REFERENCES remesa
);      -- NEW! 17/01/2013

----------------------------
-- Estimaciones de cobros --
----------------------------
CREATE TABLE estimacion_cobro(
    id SERIAL PRIMARY KEY,
    factura_venta_id INT REFERENCES factura_venta,
    prefactura_id INT REFERENCES prefactura DEFAULT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    importe FLOAT DEFAULT 0.0,
    observaciones TEXT DEFAULT ''
);

------------------------
-- Facturas de abonos --
------------------------
CREATE TABLE factura_de_abono(
    id SERIAL PRIMARY KEY,
    fecha DATE DEFAULT CURRENT_DATE
);

---------------------
-- Tabla de cobros --
---------------------
CREATE TABLE cobro(
    id SERIAL PRIMARY KEY,
    factura_venta_id INT REFERENCES factura_venta,
    prefactura_id INT REFERENCES prefactura DEFAULT NULL,
    fecha DATE DEFAULT CURRENT_DATE,
    importe FLOAT DEFAULT 0.0,
    observaciones TEXT DEFAULT '',
    pagare_cobro_id INT REFERENCES pagare_cobro DEFAULT NULL,
    cliente_id INT REFERENCES cliente DEFAULT NULL,
    factura_de_abono_id INT REFERENCES factura_de_abono DEFAULT NULL, 
    confirming_id INT REFERENCES confirming DEFAULT NULL -- NEW! 20/11/2008
);

------------
-- Abonos --
------------
CREATE TABLE abono(
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES cliente,
    factura_de_abono_id INT REFERENCES factura_de_abono DEFAULT NULL,
    numabono TEXT DEFAULT '',
    fecha DATE DEFAULT CURRENT_DATE,
    observaciones TEXT DEFAULT '',  -- Se mostrará y modificará en una ventana
                                    -- aparte a la hora de imprimir.
    almacen_id INT REFERENCES almacen DEFAULT NULL, -- Almacén destino si es 
                                                    -- un abono de devolución.
    obra_id INT REFERENCES obra
);

---------------------
-- Líneas de abono --
---------------------
CREATE TABLE linea_de_abono(
    id SERIAL PRIMARY KEY,
    linea_de_venta_id INT REFERENCES linea_de_venta,
    abono_id INT REFERENCES abono,
    diferencia FLOAT DEFAULT 0.0,   -- diferencia entre el nuevo precio y el
                                    -- de de la LDV (el precio nuevo no se
                                    -- almacena, es campo calculado)
    cantidad FLOAT DEFAULT 0.0,
    observaciones TEXT DEFAULT '',
    servicio_id INT REFERENCES servicio DEFAULT NULL
);

------------------------------------
-- Albaranes de entrada de abonos --
------------------------------------
CREATE TABLE albaran_de_entrada_de_abono(
    id SERIAL PRIMARY KEY,
    numalbaran TEXT DEFAULT '',
    fecha DATE DEFAULT CURRENT_DATE,
    observaciones TEXT DEFAULT ''
);

----------------------------
-- Líneas de devoluciones --
----------------------------
CREATE TABLE linea_de_devolucion(
    id SERIAL PRIMARY KEY,
    abono_id INT REFERENCES abono,
    articulo_id INT REFERENCES articulo,
    albaran_de_entrada_de_abono_id INT
        REFERENCES albaran_de_entrada_de_abono DEFAULT NULL,
    albaran_salida_id INT REFERENCES albaran_salida,    -- En el artículo se
        -- desvincula para que conste en almacén, pero aquí se guarda el
        -- albarán de salida del que procedía, para consultas posteriores
        -- sobre históricos.
    precio FLOAT DEFAULT 0.0,
    observaciones TEXT DEFAULT ''
);

--------------------
-- Pagos de abono --
--------------------
CREATE TABLE pago_de_abono(
    id SERIAL PRIMARY KEY,
    factura_de_abono_id INT REFERENCES factura_de_abono,
    factura_venta_id INT REFERENCES factura_venta DEFAULT NULL,
    prefactura_id INT REFERENCES prefactura DEFAULT NULL,
    importe FLOAT DEFAULT 0.0,      -- Dado que el contenido del abono no
        -- incluye IVA, este importe tampoco. Se añadirá a la factura_venta
        -- (si se quiere) como un concepto más.
    pendiente BOOLEAN DEFAULT TRUE
);

-----------------
-- LABORATORIO --
-----------------

-- Pruebas sobre lotes de balas de fibra --
CREATE TABLE prueba_tenacidad(
    id SERIAL PRIMARY KEY,
    lote_id INT REFERENCES lote,
    fecha DATE DEFAULT CURRENT_DATE,
    resultado FLOAT DEFAULT 0.0,
    lote_cem_id INT REFERENCES lote_cem DEFAULT NULL    -- NEW! 12/12/2006
);

CREATE TABLE prueba_elongacion(
    id SERIAL PRIMARY KEY,
    lote_id INT REFERENCES lote,
    fecha DATE DEFAULT CURRENT_DATE,
    resultado FLOAT DEFAULT 0.0,
    lote_cem_id INT REFERENCES lote_cem DEFAULT NULL    -- NEW! 12/12/2006
);

CREATE TABLE prueba_rizo(
    id SERIAL PRIMARY KEY,
    lote_id INT REFERENCES lote,
    fecha DATE DEFAULT CURRENT_DATE,
    resultado FLOAT DEFAULT 0.0
);

CREATE TABLE prueba_encogimiento(
    id SERIAL PRIMARY KEY,
    lote_id INT REFERENCES lote,
    fecha DATE DEFAULT CURRENT_DATE,
    resultado FLOAT DEFAULT 0.0,
    lote_cem_id INT REFERENCES lote_cem DEFAULT NULL    -- NEW! 12/12/2006
);

CREATE TABLE prueba_grasa(
    id SERIAL PRIMARY KEY,
    lote_id INT REFERENCES lote,
    fecha DATE DEFAULT CURRENT_DATE,
    resultado FLOAT DEFAULT 0.0,
    lote_cem_id INT REFERENCES lote_cem DEFAULT NULL    -- NEW! 12/12/2006
);

CREATE TABLE prueba_titulo(
    id SERIAL PRIMARY KEY,
    lote_id INT REFERENCES lote,
    fecha DATE DEFAULT CURRENT_DATE,
    resultado FLOAT DEFAULT 0.0,
    lote_cem_id INT REFERENCES lote_cem DEFAULT NULL    -- NEW! 12/12/2006
);

--------------------------------------------------
-- Pruebas de humedad sobre la fibra de cemento --
--------------------------------------------------
-- NEW! 12/12/2006 --
---------------------
CREATE TABLE prueba_humedad(
    id SERIAL PRIMARY KEY,
    lote_cem_id INT REFERENCES lote_cem,
    fecha DATE DEFAULT CURRENT_DATE,
    resultado FLOAT DEFAULT 0.0
);

-- Pruebas sobre partidas de rollos de geotextil --
CREATE TABLE prueba_gramaje(
    id SERIAL PRIMARY KEY,
    partida_id INT REFERENCES partida,
    fecha DATE DEFAULT CURRENT_DATE,
    resultado FLOAT DEFAULT 0.0
);

CREATE TABLE prueba_longitudinal(       -- Resistencia longitudinal
    id SERIAL PRIMARY KEY,
    partida_id INT REFERENCES partida,
    fecha DATE DEFAULT CURRENT_DATE,
    resultado FLOAT DEFAULT 0.0
);

CREATE TABLE prueba_alargamiento_longitudinal(
    id SERIAL PRIMARY KEY,
    partida_id INT REFERENCES partida,
    fecha DATE DEFAULT CURRENT_DATE,
    resultado FLOAT DEFAULT 0.0
);

CREATE TABLE prueba_transversal(    -- Resistencia transversal
    id SERIAL PRIMARY KEY,
    partida_id INT REFERENCES partida,
    fecha DATE DEFAULT CURRENT_DATE,
    resultado FLOAT DEFAULT 0.0
);

CREATE TABLE prueba_alargamiento_transversal(
    id SERIAL PRIMARY KEY,
    partida_id INT REFERENCES partida,
    fecha DATE DEFAULT CURRENT_DATE,
    resultado FLOAT DEFAULT 0.0
);

CREATE TABLE prueba_compresion(        -- CBR
    id SERIAL PRIMARY KEY,
    partida_id INT REFERENCES partida,
    fecha DATE DEFAULT CURRENT_DATE,
    resultado FLOAT DEFAULT 0.0
);

CREATE TABLE prueba_perforacion(
    id SERIAL PRIMARY KEY,
    partida_id INT REFERENCES partida,
    fecha DATE DEFAULT CURRENT_DATE,
    resultado FLOAT DEFAULT 0.0
);

CREATE TABLE prueba_espesor(
    id SERIAL PRIMARY KEY,
    partida_id INT REFERENCES partida,
    fecha DATE DEFAULT CURRENT_DATE,
    resultado FLOAT DEFAULT 0.0
);

CREATE TABLE prueba_permeabilidad(
    id SERIAL PRIMARY KEY,
    partida_id INT REFERENCES partida,
    fecha DATE DEFAULT CURRENT_DATE,
    resultado FLOAT DEFAULT 0.0
);

CREATE TABLE prueba_poros(
    id SERIAL PRIMARY KEY,
    partida_id INT REFERENCES partida,
    fecha DATE DEFAULT CURRENT_DATE,
    resultado FLOAT DEFAULT 0.0
);

-- NEW! 13/06/2011
CREATE TABLE prueba_piramidal(
    id SERIAL PRIMARY KEY, 
    partida_id INT REFERENCES partida, 
    fecha DATE DEFAULT CURRENT_DATE, 
    resultado FLOAT DEFAULT 0.0
);

-- Pruebas sobre materia prima --
CREATE TABLE prueba_granza(
    id SERIAL PRIMARY KEY,
    producto_compra_id INT REFERENCES producto_compra,
    fecha DATE DEFAULT CURRENT_DATE,
    resultado FLOAT DEFAULT 0.0,
    silo TEXT DEFAULT '',
    lote TEXT DEFAULT '',   -- NEW! 08/10/06. Lote del proveedor
    fecha_entrada DATE DEFAULT CURRENT_DATE, -- NEW! 08/10/06.Fecha de entrada.
    mfi FLOAT DEFAULT 0.0   -- NEW! 08/10/06. MFI de referencia que facilita
                            -- el proveedor.
);

--------------
-- Muestras --
--------------
CREATE TABLE muestra(
    id SERIAL PRIMARY KEY,
    lote_id INT REFERENCES lote DEFAULT NULL,
    partida_id INT REFERENCES partida DEFAULT NULL,
        -- No se relaciona directamente con las pruebas. Se relaciona con el
        -- lote/partida del que procede, que a su vez tiene relación con las
        -- pruebas y resultados.
    codigo TEXT DEFAULT '',
    observaciones TEXT DEFAULT '',
    pendiente BOOLEAN DEFAULT True,
    envio TIMESTAMP DEFAULT LOCALTIMESTAMP(0),      -- Fecha y hora en que se
                                                    -- envía la muestra.
    recepcion TIMESTAMP DEFAULT NULL,               -- Fecha y hora en que
                                                    -- deja de estar pendiente.
    lote_cem_id INT REFERENCES lote_cem DEFAULT NULL
);

-------------------------------
-- TABLAS AUXILIARES (cont.) --
-------------------------------
CREATE TABLE modulo(
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    icono TEXT,
    descripcion TEXT
);

CREATE TABLE ventana(
    id SERIAL PRIMARY KEY,
    modulo_id INT REFERENCES modulo,
    descripcion TEXT,
    fichero TEXT,         -- Nombre del fichero .py
    clase TEXT,           -- Nombre de la clase principal de la ventana.
    icono TEXT DEFAULT '' -- Fichero del icono o '' para el icono por defecto
);

CREATE TABLE permiso(
    -- Relación muchos a muchos con atributo entre usuarios y ventanas.
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuario,
    ventana_id INT REFERENCES ventana,
    permiso BOOLEAN DEFAULT False,   -- Indica si tiene permiso o no para
                                     -- abrir la ventana.
    --    PRIMARY KEY(usuario_id, ventana_id)   SQLObject requiere que cada
    -- tabla tenga un único ID.
    lectura BOOLEAN DEFAULT False,
    escritura BOOLEAN DEFAULT False,
    nuevo BOOLEAN DEFAULT False     -- Nuevos permisos. Entrarán en la
                                    -- siguiente versión.
);

CREATE TABLE alerta(
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuario,
    mensaje TEXT DEFAULT '',
    fechahora TIMESTAMP DEFAULT LOCALTIMESTAMP(0),
    entregado BOOLEAN DEFAULT False
);

CREATE TABLE datos_de_la_empresa(
    -- Datos de la empresa. Aparecen en los informes, facturas, albaranes,
    -- etc... Además, también sirven para determinar si un cliente es
    -- extranjero, generar albaranes internos...
    id SERIAL PRIMARY KEY,      -- Lo requiere SQLObject, pero no debería
                                -- haber más de un registro aquí.
    nombre TEXT DEFAULT 'Empresa',
    cif TEXT DEFAULT 'T-00.000.000',
    dirfacturacion TEXT DEFAULT 'C/ Dirección de facturación',
    cpfacturacion TEXT DEFAULT '00000',
    ciudadfacturacion TEXT DEFAULT 'Ciudad',
    provinciafacturacion TEXT DEFAULT 'Provincia',
    direccion TEXT DEFAULT 'C/ Dirección postal',
    cp TEXT DEFAULT '00000',
    ciudad TEXT DEFAULT 'Ciudad',
    provincia TEXT DEFAULT 'Provincia',
    telefono TEXT DEFAULT '034 000 00 00 00',
    fax TEXT DEFAULT '034 000 00 00 00',
    email TEXT DEFAULT 'correo@electronico.com',
    paisfacturacion TEXT DEFAULT 'España',
    pais TEXT DEFAULT 'España',
    telefonofacturacion TEXT DEFAULT '000 000 000 000',
    faxfacturacion TEXT DEFAULT '000 000 000 000',
    nombre_responsable_compras TEXT DEFAULT 'Responsable De Compras',
    telefono_responsable_compras TEXT DEFAULT '000 00 00 00',
    nombre_contacto TEXT DEFAULT 'Nombre Contacto',
    registro_mercantil TEXT DEFAULT 'Inscrita en el Registro Mercantil ...',
    email_responsable_compras TEXT DEFAULT 'resposable@compras.com',
    logo TEXT DEFAULT 'logo-inn.png',  -- Nombre de fichero (solo nombre,
        -- no ruta completa) de la imagen del logo de la empresa.
    logo2 TEXT DEFAULT '',  -- Nombre del logo alternativo
    bvqi BOOLEAN DEFAULT TRUE,          -- True si hay que imprimir el logo
                                        -- de calidad certificada BVQI
    -- Dirección para albaran alternativo (albaran composan)
    nomalbaran2 TEXT DEFAULT 'NOMBRE ALTERNATIVO ALBARÁN',
    diralbaran2 TEXT DEFAULT 'Dirección albarán',
    cpalbaran2 TEXT DEFAULT '00000',
    ciualbaran2 TEXT DEFAULT 'Ciudad',
    proalbaran2 TEXT DEFAULT 'Provincia',
    telalbaran2 TEXT DEFAULT '00 000 00 00',
    faxalbaran2 TEXT DEFAULT '00 000 00 00',
    regalbaran2 TEXT DEFAULT 'CIF T-00000000 Reg.Mec. de ...',
    irpf FLOAT DEFAULT 0.0, -- NEW! 10/04/07. Si -0.15 aparecerá el campo
        -- IRPF en las facturas de venta para descontarse de la base imponible
    es_sociedad BOOLEAN DEFAULT TRUE,   -- NEW! 02/05/07. Si es True la
        -- empresa es una sociedad. Si False, la empresa es
        -- persona física o persona jurídica. En los impresos se usará
        -- "nombre" como nombre comercial y nombre_contacto como nombre
        -- fiscal de facturación.
        -- También servirá para discernir si mostrar servicios y transportes
        -- en albaranes y si valorar o no albaranes en el PDF generado al
        -- imprimir.
        -- OJO: También se usa para escribir "FÁBRICA" o "TIENDA" en los
        -- pedidos de compra, etc.
    logoiso1 TEXT DEFAULT 'bvqi.gif',  -- NEW! 27/06/07. Si bvqi es True en
                                       -- algunos impresos aparecerá este logo.
    logoiso2 TEXT DEFAULT 'bvqi2.png', -- NEW! 27/06/07. Si bvqi es True en
                                       -- algunos impresos aparecerá este logo.
    recargo_equivalencia BOOLEAN DEFAULT FALSE, -- 4% adicional de IVA y eso.
    iva FLOAT DEFAULT 0.21, -- IVA soportado por defecto, sin contar R.E.
    ped_compra_texto_fijo TEXT DEFAULT 'ROGAMOS NOS REMITAN COPIA DE ESTE PEDIDO SELLADO Y FIRMADO POR UDS.',   -- Sólo lo puede editar el usuario de nivel 0 (admin).
    ped_compra_texto_editable TEXT DEFAULT 'ESTA MERCANCIA SE DEBE ENTREGAR CON ALBARAN DE GEOTEXAN S.A. Y ENVIARNOS COPIA DEL MISMO CON LA FIRMA Y SELLO DE RECIBIDO POR EL CLIENTE. ESTO ES CONDICIÓN IMPRESCINDIBLE PARA LA TRAMITACIÓN DE SU FACTURA.', -- Se puede editar por cualquiera con permiso de escritura en pedidos de compra.
    ped_compra_texto_editable_con_nivel1 TEXT DEFAULT 'PAGO A 120 DÍAS F.F. PAGO LOS 25.', -- Solo lo puede editar en perdidos de compra los usuarios con nivel 0 ó 1.
    web TEXT DEFAULT ''
);

----------------------------------------------
-- Observaciones para las nóminas de un mes --
----------------------------------------------
-- NEW! 27/04/07 --
-------------------
CREATE TABLE observaciones_nominas(
    id SERIAL PRIMARY KEY,
    fecha DATE DEFAULT CURRENT_DATE,
    observaciones TEXT DEFAULT ''
);


------------------------------------------------
-- Documentos adjuntos a pedidos, albaranes,  --
-- facturas y pagarés tanto de venta como de  --
-- compra, etc...                             --
------------------------------------------------
-- NEW! 22/10/2007 --
---------------------
CREATE TABLE documento(
    id SERIAL PRIMARY KEY,
    nombre TEXT DEFAULT '', -- Nombre descriptivo
    -- ruta TEXT,   Prefiero que sea calculado uniendo ruta base de documentos
    -- y nombre de fichero.
    nombre_fichero TEXT DEFAULT '', -- Nombre del fichero. SIN RUTAS.
    observaciones TEXT DEFAULT '',
    pedido_venta_id INT REFERENCES pedido_venta DEFAULT NULL,
    albaran_salida_id INT REFERENCES albaran_salida DEFAULT NULL,
    factura_venta_id INT REFERENCES factura_venta DEFAULT NULL,
    prefactura_id INT REFERENCES prefactura DEFAULT NULL,
    pagare_cobro_id INT REFERENCES pagare_cobro DEFAULT NULL,
    pedido_compra_id INT REFERENCES pedido_compra DEFAULT NULL,
    albaran_entrada_id INT REFERENCES albaran_entrada DEFAULT NULL,
    factura_compra_id INT REFERENCES factura_compra DEFAULT NULL,
    pagare_pago_id INT REFERENCES pagare_pago DEFAULT NULL,
    empleado_id INT REFERENCES empleado DEFAULT NULL,
    cliente_id INT REFERENCES cliente DEFAULT NULL,
    proveedor_id INT REFERENCES proveedor DEFAULT NULL, 
    confirming_id INT REFERENCES confirming DEFAULT NULL -- NEW! 20/11/2008
);

----------------------------------------------------
-- Estadísticas de ventanas abiertas por usuario. --
----------------------------------------------------
-- NEW! 16/12/2007 --
---------------------
CREATE TABLE estadistica(
    id SERIAL PRIMARY KEY,
    usuario_id INT REFERENCES usuario,
    ventana_id INT REFERENCES ventana,
    veces INT DEFAULT 0,
    ultima_vez TIMESTAMP DEFAULT LOCALTIMESTAMP(0)
);

-----------------------------------------
-- Control diario de horas de personal --
---------------------------------------------------------
-- NEW! 19/06/2008                                     --
-- Horas diarias trabajadas por el personal de planta. --
---------------------------------------------------------
CREATE TABLE control_horas(
    id SERIAL PRIMARY KEY,
    grupo_id INT REFERENCES grupo,
    empleado_id INT REFERENCES empleado NOT NULL,
    horas_regulares FLOAT DEFAULT 0.0,
    nocturnidad BOOLEAN DEFAULT FALSE,
    horas_extra_dia_produccion FLOAT DEFAULT 0.0,
    horas_extra_dia_mantenimiento FLOAT DEFAULT 0.0,
    horas_extra_dia_almacen FLOAT DEFAULT 0.0,
    horas_extra_dia_varios FLOAT DEFAULT 0.0,
    horas_extra_noche_produccion FLOAT DEFAULT 0.0,
    horas_extra_noche_mantenimiento FLOAT DEFAULT 0.0,
    horas_extra_noche_almacen FLOAT DEFAULT 0.0,
    horas_extra_noche_varios FLOAT DEFAULT 0.0,
    horas_almacen FLOAT DEFAULT 0.0,
    horas_varios FLOAT DEFAULT 0.0,
    varios TEXT DEFAULT '',
    comentarios TEXT DEFAULT '',
    baja_laboral BOOLEAN DEFAULT FALSE,
    vacaciones_y_asuntos_propios BOOLEAN DEFAULT FALSE,
    fecha DATE DEFAULT CURRENT_DATE,
    festivo BOOLEAN DEFAULT FALSE,
    bloqueado BOOLEAN DEFAULT FALSE, 
    plus_absentismo FLOAT DEFAULT 0.0,-- NEW! 24/09/08. Para guardar el plus 
                                      -- manual de no absentismo. 
        -- Para actualizar en clientes:
        -- ALTER TABLE control_horas ADD COLUMN plus_absentismo FLOAT; ALTER TABLE control_horas ALTER COLUMN plus_absentismo SET DEFAULT 0.0; UPDATE control_horas SET plus_absentismo = 0.0; 
    concepto_libre TEXT DEFAULT '', 
    importe_libre FLOAT DEFAULT 0.0 -- NEW! 30/10/2008. Para guardar un 
                                    -- importe a rellenar manualmente.
        -- Para actualizar en clientes:
        -- ALTER TABLE control_horas ADD COLUMN concepto_libre TEXT; ALTER TABLE control_horas ADD COLUMN importe_libre FLOAT; ALTER TABLE control_horas ALTER COLUMN concepto_libre SET DEFAULT ''; ALTER TABLE control_horas ALTER COLUMN importe_libre SET DEFAULT 0.0; UPDATE control_horas SET concepto_libre = ''; UPDATE control_horas SET importe_libre = 0.0; 
);

CREATE TABLE control_horas_produccion(
    id SERIAL PRIMARY KEY,
    horas_produccion FLOAT DEFAULT 0.0,
    linea_de_produccion_id INT REFERENCES linea_de_produccion,
    control_horas_id INT REFERENCES control_horas
);

CREATE TABLE control_horas_mantenimiento(
    id SERIAL PRIMARY KEY,
    horas_mantenimiento FLOAT DEFAULT 0.0,
    linea_de_produccion_id INT REFERENCES linea_de_produccion,
    control_horas_id INT REFERENCES control_horas
);

------------------------------------------------------
-- Tabla auxiliar para el orden de los trabajadores --
------------------------------------------------------
CREATE TABLE orden_empleados(
    id SERIAL PRIMARY KEY,
    orden INT NOT NULL,
    empleado_id INT REFERENCES empleado NOT NULL,
    fecha DATE DEFAULT CURRENT_DATE
);

---------------------------------------------------------------
-- Tabla auxiliar de objetos recientes por usuario y ventana --
---------------------------------------------------------------
-- NEW! 25/08/2008 
CREATE TABLE lista_objetos_recientes(
    id SERIAL PRIMARY KEY, 
    usuario_id INT REFERENCES usuario,
    ventana_id INT REFERENCES ventana
);

----------------------------------------------------
-- IDs de objetos recientes por ventana y usuario --
----------------------------------------------------
-- NEW! 25/08/2008
CREATE TABLE id_reciente(
    id SERIAL PRIMARY KEY, 
    lista_objetos_recientes_id INT REFERENCES lista_objetos_recientes, 
    objeto_id INT NOT NULL
);


----------------------------------------------------
-- Relación muchos a muchos entre productos de    --
-- venta "especiales" y almacenes.                --
----------------------------------------------------
-- NEW! 03/02/2009
CREATE TABLE stock_especial(
    -- Misma función que la tabla stock_almacen
    id SERIAL PRIMARY KEY, 
    almacen_id INT REFERENCES almacen, 
    campos_especificos_especial_id INT REFERENCES campos_especificos_especial,
    existencias FLOAT DEFAULT 0.0
);


--=====--
-- CRM --
--=====--

----------------------------
-- Contactos en las obras --
-- NEW! 26/05/2009        --
----------------------------
CREATE TABLE contacto(
    id SERIAL PRIMARY KEY, 
    nombre TEXT, 
    apellidos TEXT DEFAULT '', 
    cargo TEXT DEFAULT '', 
    telefono TEXT DEFAULT '', 
    fax TEXT DEFAULT '', 
    movil TEXT DEFAULT '', 
    correoe TEXT DEFAULT '', 
    web TEXT DEFAULT '', 
    observaciones TEXT DEFAULT ''
);

------------------------------------------------------
-- Relación muchos a muchos entre obras y clientes. --
-- NEW! 26/05/2009                                  --
------------------------------------------------------
CREATE TABLE obra__cliente(
    obra_id INT NOT NULL REFERENCES obra, 
    cliente_id INT NOT NULL REFERENCES cliente
);

-------------------------------------------------------
-- Relación muchos a muchos entre obras y contactos. --
-- NEW! 26/05/2009                                   --
-------------------------------------------------------
CREATE TABLE obra__contacto(
    obra_id INT NOT NULL REFERENCES obra, 
    contacto_id INT NOT NULL REFERENCES contacto
);

---------------------------------------
-- Anotaciones en facturas de venta. --
-- NEW! 26/05/2009                   --
---------------------------------------
CREATE TABLE nota(
    id SERIAL PRIMARY KEY, 
    factura_venta_id INT REFERENCES factura_venta, 
    fechahora TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    texto TEXT DEFAULT '', 
    observaciones TEXT DEFAULT ''
);

--------------------------------------------------
-- Estados de las alarmas.                      --
-- NEW! 26/05/2009                              --
-- El estado debería cambiar automáticamente    --
-- al menos entre el "no leída" y "en espera".  --
-- El resto de estados podrían estar definidos  --
-- por el usuario y cambiarlos a mano cuando    --
-- quisiera.                                    --
--------------------------------------------------
CREATE TABLE estado(
    id SERIAL PRIMARY KEY, 
    descripcion TEXT, 
    pendiente BOOLEAN,  -- Indica si la alarma está pendiente de activarse 
                        -- aún (TRUE) o si ya "ha sonado" y se ignorará.
    observaciones TEXT DEFAULT ''
);

-- Solo la primera vez:
-- INSERT INTO estado(id, descripcion, pendiente) VALUES (1, 'No leída', TRUE);
-- INSERT INTO estado(id, descripcion, pendiente) VALUES (2, 'En espera', FALSE);
-- INSERT INTO estado(id, descripcion, pendiente) VALUES (3, 'Cerrada', FALSE);

-------------------------------------------
-- Alarmas relacionadas con facturas.    --
-- Deberían alertar al usuario de alguna --
-- forma cuando se cumpla el timestamp   --
-- fechahora_alarma.                     --
-- NEW! 26/05/2009                       --
-------------------------------------------
CREATE TABLE alarma(
    id SERIAL PRIMARY KEY, 
    factura_venta_id INT REFERENCES factura_venta, 
    estado_id INT REFERENCES estado DEFAULT 1, 
    fechahora TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    texto TEXT DEFAULT '', 
    fechahora_alarma TIMESTAMP DEFAULT NULL, 
    objeto_relacionado TEXT DEFAULT NULL,   -- No sé si lo llegaré a usar, 
        -- pero la idea es guardar aquí un puid de pclases y abrirlo desde 
        -- la ventana de CRM con doble clic o mostrar información relevante 
        -- al respecto.
    observaciones TEXT DEFAULT '' 
);

------------------------------
-- Categorías de las tareas --
-- para diferenciarlas por  --
-- colores o algo.          --
-- NEW! 26/05/2009          --
------------------------------
CREATE TABLE categoria(
    id SERIAL PRIMARY KEY, 
    descripcion TEXT, 
    color_r INT,    -- En RGB(256, 256, 256).
    color_g INT, 
    color_b INT, 
    prioridad INT,  -- Prioridad sobre el resto de categorías. Codificada 
                    -- de la misma forma que los ring en los procesadores: 
                    -- 0 = máxima.
    observaciones TEXT DEFAULT ''
);

-- Solo la primera vez
--INSERT INTO categoria (descripcion, color_r, color_g, color_b, prioridad) 
--    VALUES ('Urgente', 255, 65, 0, 0);
--INSERT INTO categoria (descripcion, color_r, color_g, color_b, prioridad) 
--    VALUES ('Llamadas de teléfono', 30, 255, 60, 5);
--INSERT INTO categoria (descripcion, color_r, color_g, color_b, prioridad) 
--    VALUES ('Tareas automáticas', 125, 125, 125, 10);

-------------------------------------------------
-- TO-DOs del usuario respecto a cada factura. --
-- NEW! 26/05/2009                             --
-------------------------------------------------
CREATE TABLE tarea(
    id SERIAL PRIMARY KEY, 
    factura_venta_id INT REFERENCES factura_venta, 
    categoria_id INT REFERENCES categoria DEFAULT NULL, 
    texto TEXT DEFAULT '', 
    pendiente BOOLEAN DEFAULT TRUE, 
    fecha DATE DEFAULT CURRENT_DATE, 
    observaciones TEXT DEFAULT '', 
    fechadone TIMESTAMP DEFAULT NULL
);

-----------------------------------
-- Tablas para presupuesto anual --
-----------------------------------
CREATE TABLE presupuesto_anual(
    -- Conceptos "de primer nivel". En principio no editables por el usuario.
    id SERIAL PRIMARY KEY, 
    descripcion TEXT DEFAULT ''
);

CREATE TABLE concepto_presupuesto_anual(
    -- Conceptos. Primera columna de las flas del presupuesto.
    id SERIAL PRIMARY KEY, 
    presupuesto_anual_id INT REFERENCES presupuesto_anual NOT NULL, 
    descripcion TEXT DEFAULT '', 
    proveedor_id INT REFERENCES proveedor DEFAULT NULL, 
    inmutable BOOLEAN DEFAULT FALSE
);

CREATE TABLE valor_presupuesto_anual(
    id SERIAL PRIMARY KEY, 
    concepto_presupuesto_anual_id INT REFERENCES concepto_presupuesto_anual NOT NULL, 
    mes DATE NOT NULL,  -- Me interesa mes y año nada más.
    importe FLOAT DEFAULT 0.0, 
    precio FLOAT DEFAULT 1      -- Para estimaciones que sean del tipo
                                -- importe=precio*algo (toneladas para los 
                                -- proveedores de granza, por ejemplo).
);

CREATE TABLE vencimiento_valor_presupuesto_anual(
    id SERIAL PRIMARY KEY,
    valor_presupuesto_anual_id INT REFERENCES valor_presupuesto_anual,
    fecha DATE NOT NULL, 
    -- El importe será un campo calculado.
    documento_de_pago_id INT REFERENCES documento_de_pago
);

--------------------------------------------------------------
-- Tabla para guardar usuario, fecha y hora de creación,    --
-- modificación o eliminación de un objeto.                 --
--------------------------------------------------------------
CREATE TABLE auditoria(
    id SERIAL PRIMARY KEY, 
    usuario_id INT REFERENCES usuario,  -- FK al usuario 
    ventana_id INT REFERENCES ventana,  -- FK ventana desde donde se ha hecho.
    dbpuid TEXT,        -- Me lo tiene que dar la capa superior.
    action TEXT,        -- creación, modificación o borrado
    ip TEXT DEFAULT NULL,   -- IP desde la que realizó la acción
    hostname TEXT DEFAULT NULL, -- Si es posible, el nombre de la máquina.
    fechahora TIMESTAMP DEFAULT LOCALTIMESTAMP(0), 
    descripcion TEXT DEFAULT NULL
);

------------------------ FUNCIONES ------------------------
CREATE LANGUAGE plpgsql;

-- Para PostgreSQL 7.4 usar:
-- CREATE FUNCTION plpgsql_call_handler() RETURNS language_handler AS '$libdir/plpgsql' LANGUAGE C;
-- CREATE TRUSTED PROCEDURAL LANGUAGE plpgsql HANDLER plpgsql_call_handler;

CREATE FUNCTION ultimo_lote_mas_uno()
    RETURNS INT8
    LANGUAGE SQL
    AS 'SELECT COALESCE(MAX(numlote),0)+1 FROM lote;';

CREATE FUNCTION ultima_partida_mas_uno()
    RETURNS INT8
    LANGUAGE SQL
    AS 'SELECT COALESCE(MAX(numpartida),0)+1 FROM partida;';

CREATE FUNCTION ultima_bala_mas_uno()
    RETURNS INT8
    LANGUAGE SQL
    AS 'SELECT COALESCE(MAX(numbala), 0)+1 FROM bala;';

CREATE FUNCTION ultimo_rollo_mas_uno()
    RETURNS INT8
    LANGUAGE SQL
    AS 'SELECT COALESCE(MAX(numrollo), 0)+1 FROM rollo;';

CREATE FUNCTION ultimo_rollo_defectuoso_mas_uno()
    RETURNS INT8
    LANGUAGE SQL
    AS 'SELECT COALESCE(MAX(numrollo), 0)+1 FROM rollo_defectuoso;';
        -- NEW! 07/03/2007

CREATE FUNCTION ultimo_codigo_rollo_mas_uno()
    RETURNS TEXT
    LANGUAGE SQL
    AS 'SELECT ''R'' || COALESCE(MAX(numrollo), 0) + 1 FROM rollo;';
        -- NEW! 08/03/2007

CREATE FUNCTION ultimo_codigo_rollo_defectuoso_mas_uno()
    RETURNS TEXT
    LANGUAGE SQL
    AS 'SELECT ''X'' || COALESCE(MAX(numrollo), 0) + 1 FROM rollo_defectuoso;';
        -- NEW! 08/03/2007

CREATE FUNCTION ultima_partida_cem_mas_uno()
    RETURNS INT8
    LANGUAGE SQL
    AS 'SELECT COALESCE(MAX(numpartida),0)+1 FROM partida_cem;';
        -- NEW! 08/03/2007

CREATE FUNCTION ultimo_lote_cem_mas_uno()
    RETURNS INT8
    LANGUAGE SQL
    AS 'SELECT COALESCE(MAX(numlote),0)+1 FROM lote_cem;';
        -- NEW! 08/03/2007

CREATE FUNCTION ultimo_codigo_bala_mas_uno()
    RETURNS TEXT
    LANGUAGE SQL
    AS 'SELECT ''B'' || COALESCE(MAX(numbala), 0) + 1 FROM bala;';
        -- NEW! 08/03/2007

CREATE FUNCTION ultimo_ticket_mas_uno()
    RETURNS INT8
    LANGUAGE SQL
    AS 'SELECT COALESCE(MAX(numticket), 0)+1
        FROM ticket WHERE date_part(''year'', fechahora)
             = date_part(''year'', CURRENT_DATE);';
        -- NEW! 19/04/07

CREATE FUNCTION ultima_bala_cable_mas_uno()
    RETURNS INT8
    LANGUAGE SQL
    AS 'SELECT COALESCE(MAX(numbala), 0)+1 FROM bala_cable;';
        -- NEW! 13/06/2007

CREATE FUNCTION ultimo_codigo_bala_cable_mas_uno()
    RETURNS TEXT
    LANGUAGE SQL
    AS 'SELECT ''Z'' || COALESCE(MAX(numbala), 0) + 1 FROM bala_cable;';
        -- NEW! 13/06/2007

CREATE FUNCTION ultimo_rollo_c_mas_uno()
    RETURNS INT8
    LANGUAGE SQL
    AS 'SELECT COALESCE(MAX(numrollo), 0)+1 FROM rollo_c;';
        -- NEW! 02/06/2008

CREATE FUNCTION ultimo_codigo_rollo_c_mas_uno()
    RETURNS TEXT
    LANGUAGE SQL
    AS 'SELECT ''Y'' || COALESCE(MAX(numrollo), 0) + 1 FROM rollo_c;';
        -- NEW! 02/06/2008


-------------------------------------------------------------------------------
CREATE FUNCTION codigo_albaran_interno_en_observaciones(INT)
    -- Devuelve True si el texo "ALBINTPDPID" típico de los albaranes
    -- internos de consumos aparece en las observaciones.
    RETURNS BOOLEAN
    LANGUAGE SQL STABLE
    AS 'SELECT position(''ALBINTPDPID'' in albaran_salida.observaciones) > 0
               AS res
        FROM albaran_salida, linea_de_venta, producto_compra
        WHERE albaran_salida.id = $1
          AND albaran_salida.id = linea_de_venta.albaran_salida_id
          AND linea_de_venta.producto_compra_id = producto_compra.id;
       ';       -- NEW! 03/07/2007
-- SELECT COALESCE(codigo_albaran_interno_en_observaciones(1658),
--   FALSE); -> False
-- SELECT COALESCE(codigo_albaran_interno_en_observaciones(1651),
--   FALSE); -> True

CREATE FUNCTION es_albaran_interno_de_consumos(INT)
    -- Es albarán interno de consumos si tiene al menos un producto de compra
    -- y el código ALBINT... en las observaciones.
    RETURNS BOOLEAN
    LANGUAGE SQL STABLE
    AS 'SELECT COUNT(*) > 0 AS res
        FROM albaran_salida, linea_de_venta
        WHERE albaran_salida.id = $1
         AND linea_de_venta.albaran_salida_id = albaran_salida.id
         AND linea_de_venta.producto_compra_id IS NOT NULL
         AND COALESCE(codigo_albaran_interno_en_observaciones($1), FALSE)=TRUE
        ;';

-- SELECT es_albaran_interno_de_consumos(1658); -> False
-- SELECT es_albaran_interno_de_consumos(1651); -> True

CREATE FUNCTION cliente_albaran_es_propia_empresa(INT)
    RETURNS BOOLEAN
    LANGUAGE SQL STABLE
    AS 'SELECT COUNT(*) = 1 AS res
        FROM albaran_salida, cliente
        WHERE albaran_salida.id = $1
          AND albaran_salida.cliente_id = cliente.id
          AND cliente.nombre = (SELECT nombre
                                FROM datos_de_la_empresa
                                LIMIT 1)
       ;';      -- NEW! 03/07/2007

-- SELECT cliente_albaran_es_propia_empresa(1656); -> False
-- SELECT cliente_albaran_es_propia_empresa(16560); -> False
-- SELECT cliente_albaran_es_propia_empresa(1658); -> True
-- SELECT cliente_albaran_es_propia_empresa(1651); -> True

CREATE FUNCTION contiene_bala_o_producto_compra(INT)
    RETURNS BOOLEAN
    LANGUAGE SQL STABLE
    AS 'SELECT COUNT(*) > 0 AS res
        FROM albaran_salida, linea_de_venta, articulo
        WHERE albaran_salida.id = $1
          AND linea_de_venta.albaran_salida_id = albaran_salida.id
          AND (articulo.albaran_salida_id = albaran_salida.id
               OR linea_de_venta.producto_compra_id IS NOT NULL)
       ;';      -- NEW! 03/07/2007
-- SELECT contiene_bala_o_producto_compra(1658); -> True
-- SELECT contiene_bala_o_producto_compra(1653); -> False

CREATE FUNCTION es_de_partida_de_carga(INT)
    -- True si el albarán corresponde a una partida de carga. Para ello
    -- _todas_ las balas del albarán deben pertenecer a una partida de carga,
    -- y al menos debe tener una.
    RETURNS BOOLEAN
    LANGUAGE SQL STABLE
    AS 'SELECT COUNT(*) = (SELECT COUNT(*)
                           FROM articulo
                           WHERE articulo.albaran_salida_id = $1
                             AND articulo.bala_id IS NOT NULL)
               AND COUNT(*) >= 1 AS res
        FROM albaran_salida, articulo, bala
        WHERE albaran_salida.id = $1
          AND articulo.albaran_salida_id = $1
          AND articulo.bala_id = bala.id
          AND bala.partida_carga_id IS NOT NULL
       ';      -- NEW! 03/07/2007
-- SELECT es_de_partida_de_carga(1253); -> True
-- SELECT es_de_partida_de_carga(1651); -> False
-- SELECT es_de_partida_de_carga(4618); -> False
-- SELECT es_de_partida_de_carga(1649); -> True

CREATE FUNCTION es_interno(INT)
    -- Devuelve TRUE si el albarán es un albarán interno de consumo de
    -- materiales o de fibra.
    RETURNS BOOLEAN
    LANGUAGE SQL STABLE
    AS 'SELECT cliente_albaran_es_propia_empresa($1)
           AND contiene_bala_o_producto_compra($1)
           AND (es_de_partida_de_carga($1)
            OR es_albaran_interno_de_consumos($1))
    ;'; -- NEW 03/07/2007

CREATE FUNCTION caja_es_clase_b(INT)
    -- Devuelve TRUE si la caja es de clase B. El criterio para definir si 
    -- una caja es B es mirar el número de bolsas por caja que lleva. Si es 
    -- menor al número de bolsas estándar del producto, es B.
    RETURNS BOOLEAN
    LANGUAGE SQL STABLE
    AS '
        SELECT caja.numbolsas < ceb.bolsas_caja 
          FROM caja, articulo, producto_venta, campos_especificos_bala as ceb
         WHERE caja.id = $1
           AND caja.id = articulo.caja_id
           AND articulo.producto_venta_id = producto_venta.id
           AND producto_venta.campos_especificos_bala_id = ceb.id 
    ;'; -- NEW 11/09/2009

CREATE OR REPLACE FUNCTION cobro_esta_cobrado(idcobro INTEGER, 
                                   fecha DATE DEFAULT CURRENT_DATE)
    -- Recibe un ID de cobro y una fecha.
    -- Devuelve el importe cobrado en esa fecha, que depende de:
    --  * Si es una transferencia, efectivo, cheque o cualquier otra cosa 
    --    que no sea un confirming o un pagaré; se cuenta como cobrado en 
    --    cuanto se alcanza la fecha de cobro.
    --  * Si es un confirming, cuenta como cobrado siempre que tenga el 
    --    campo pendiente == FALSE. Ya que si no responde el cliente, 
    --    responde el banco por él.
    --  * Si es un pagaré, cuenta como cobrado si no está pendiente o no 
    --    está vencido todavía (fecha_cobro <= DATE recibido).
    RETURNS FLOAT
    AS $$
        DECLARE
            registro_cobro cobro%ROWTYPE;
            registro_pagare_cobro pagare_cobro%ROWTYPE;
            registro_confirming confirming%ROWTYPE;
            cobrado FLOAT;
        BEGIN
            -- Selecciono el cobro en cuestión:
            SELECT * INTO registro_cobro FROM cobro WHERE id = idcobro;
            -- Buscar si es pagaré, confirming u otra cosa. Aquí ya 
            -- me aseguro de que esté recibido mirando la fecha.
            IF NOT (registro_cobro.pagare_cobro_id IS NULL) THEN
                SELECT * INTO registro_pagare_cobro 
                  FROM pagare_cobro 
                 WHERE pagare_cobro.id = registro_cobro.pagare_cobro_id 
                   AND pagare_cobro.fecha_recepcion <= fecha;
                -- Si tiene fecha de cobro y ya ha pasado, he cobrado lo 
                -- que indique el pagaré (que puede ser 0 si está pendiente,  
                -- solo una parte del pagaré por error de alguien o lo que 
                -- sea, o completo --cuando se pone el pendiente=FALSE, el 
                -- cobrado se iguala al importe total del pagaré--).
                IF (NOT (registro_pagare_cobro.fecha_cobrado IS NULL))
                    AND fecha >= registro_pagare_cobro.fecha_cobrado THEN
                    cobrado := registro_pagare_cobro.cobrado;
                -- Si no tiene fecha de cobrado o ésta todavía no ha llegado 
                -- según la recibida, está documentado, pero no cobrado.
                -- O si no tiene fecha de cobrado en abosulto. Que estaría 
                -- no documentado.
                ELSE
                    cobrado := 0.0;
                END IF;
            ELSIF NOT (registro_cobro.confirming_id IS NULL) THEN
                -- Si es un confirming, lo cuento como cobrado si no está 
                -- pendiente o si ya lo he recibido, ya que si no responde 
                -- el cliente, responderá el banco. Pero lo cuento como 
                -- cobrado solo si se ha indicado una fecha de cobro. Ya que 
                -- si se negocia o se cobra, este campo estará informado.
                -- Y si no está informado, es que es un importe documentado 
                -- (si no no existiría el registro) pero no cobrado ni 
                -- negociado. Estaría impagado/vencido.
                SELECT * INTO registro_confirming
                  FROM confirming 
                 WHERE confirming.id = registro_cobro.confirming_id 
                   AND confirming.fecha_recepcion <= fecha;
                IF (NOT (registro_confirming.fecha_cobrado IS NULL))
                    AND fecha >= registro_confirming.fecha_cobrado THEN
                    cobrado := registro_confirming.cobrado;
                -- Si no tiene fecha de cobrado o ésta todavía no ha llegado 
                -- según la recibida, está documentado, pero no cobrado.
                -- O si no tiene fecha de cobrado en abosulto. Que estaría 
                -- no documentado.
                ELSE
                    cobrado := 0.0;
                END IF;
            ELSE
                -- Es un cobro que no implica efectos futuribles 
                -- (transferencia, contado, etc.). Cuenta como cobrado desde 
                -- el momento en que se recibe.
                IF registro_cobro.fecha <= fecha THEN
                    cobrado := registro_cobro.importe;
                ELSE
                    cobrado := 0.0;
                END IF;
            END IF;
            RETURN cobrado;
        END;
    $$ LANGUAGE plpgsql; -- NEW 26/06/2013 MODIFICADO 0/08/2013

CREATE OR REPLACE FUNCTION cobro_esta_documentado(idcobro INTEGER, 
                                   fecha DATE DEFAULT CURRENT_DATE)
    -- Recibe un ID de cobro y una fecha.
    -- Devuelve el importe documentado PERO NO COBRADO/VENCIDO en esa fecha, 
    -- que depende de:
    --  * Si es una transferencia, efectivo, cheque o cualquier otra cosa 
    --    que no sea un confirming o un pagaré; se cuenta como cobrado en 
    --    cuanto se alcanza la fecha de cobro. Nunca está documentado.
    --  * Si es un confirming o un pagaré cuentan como documentados si 
    --    no tienen informado el campo fecha_cobrado.
    RETURNS FLOAT
    AS $$
        DECLARE
            registro_cobro cobro%ROWTYPE;
            registro_pagare_cobro pagare_cobro%ROWTYPE;
            registro_confirming confirming%ROWTYPE;
            documentado FLOAT;
        BEGIN
            -- Selecciono el cobro en cuestión:
            SELECT * INTO registro_cobro FROM cobro WHERE id = idcobro;
            -- Buscar si es pagaré, confirming u otra cosa:
            IF NOT (registro_cobro.pagare_cobro_id IS NULL) THEN
                SELECT * INTO registro_pagare_cobro 
                  FROM pagare_cobro 
                 WHERE pagare_cobro.id = registro_cobro.pagare_cobro_id;
                -- Si no tiene fecha de cobro o tiene pero es posterior 
                -- a la fecha consultada, está documentado. Si es posterior 
                -- estaría cobrado y si no tiene y dependiendo de la 
                -- fecha del vencimiento, impagado. Contando siempre con que 
                -- se haya recibido en la fecha indicada.
                IF (registro_pagare_cobro.fecha_cobrado IS NULL OR 
                    registro_pagare_cobro.fecha_cobrado > fecha)
                   AND registro_pagare_cobro.fecha_recepcion <= fecha THEN
                    documentado := registro_pagare_cobro.cantidad;
                ELSE
                    documentado := 0.0;
                END IF;
            ELSIF NOT (registro_cobro.confirming_id IS NULL) THEN
                SELECT * INTO registro_confirming 
                  FROM confirming
                 WHERE confirming.id = registro_cobro.confirming_id;
                -- Si no tiene fecha de cobro o tiene pero es posterior 
                -- a la fecha consultada, está documentado. Si es posterior 
                -- estaría cobrado y si no tiene y dependiendo de la 
                -- fecha del vencimiento, impagado.
                IF (registro_confirming.fecha_cobrado IS NULL OR 
                    registro_confirming.fecha_cobrado > fecha) 
                   AND registro_confirming.fecha_recepcion <= fecha THEN
                    documentado := registro_confirming.cantidad;
                ELSE
                    documentado := 0.0;
                END IF;
            ELSE
                -- Es un cobro que no implica efectos futuribles 
                -- (transferencia, contado, etc.). No llega a tener nunca 
                -- un documento de cobro.
                documentado := 0.0;
            END IF;
            RETURN documentado;
        END;
    $$ LANGUAGE plpgsql; -- NEW 7/08/2013

CREATE OR REPLACE FUNCTION calcular_importe_cobrado_factura_venta(idfra INTEGER, 
								  fecha DATE DEFAULT CURRENT_DATE)
    -- Devuelve el importe cobrado en fecha para la factura cuyo id se recibe.
    RETURNS FLOAT
    AS $$
        SELECT COALESCE(SUM(importe), 0) FROM cobro WHERE cobro.factura_venta_id = $1 AND cobro_esta_cobrado(cobro.id, $2) <> 0;
    $$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION calcular_importe_documentado_factura_venta(
                                idfra INTEGER, 
                                fecha DATE DEFAULT CURRENT_DATE)
    -- Indica el importe documentado y no vencido ni cobrado de la factura.
    RETURNS FLOAT
    AS $$
        SELECT COALESCE(SUM(importe), 0) 
          FROM cobro 
         WHERE cobro.factura_venta_id = $1 
           AND cobro_esta_documentado(cobro.id, $2) <> 0;
    $$ LANGUAGE SQL;    -- NEW! 7/08/2013

CREATE OR REPLACE FUNCTION calcular_importe_vencido_factura_venta(
                                idfra INTEGER, 
                                fecha DATE DEFAULT CURRENT_DATE)
    RETURNS FLOAT
    AS $$
        SELECT COALESCE(SUM(importe), 0) 
          FROM vencimiento_cobro 
         WHERE vencimiento_cobro.factura_venta_id = $1 
           AND vencimiento_cobro.fecha < $2;
    $$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION calcular_importe_no_vencido_factura_venta(
                                idfra INTEGER, 
                                fecha DATE DEFAULT CURRENT_DATE)
    RETURNS FLOAT
    AS $$
        SELECT COALESCE(SUM(importe), 0) 
          FROM vencimiento_cobro 
         WHERE vencimiento_cobro.factura_venta_id = $1 
           AND vencimiento_cobro.fecha >= $2;
    $$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION fra_cobrada(idfra INTEGER, 
                                       fecha DATE DEFAULT CURRENT_DATE)
    -- Devuelve TRUE si el importe de los vencimientos es igual al importe 
    -- de los cobros en la fecha recibida.
    RETURNS BOOLEAN
    AS $BODY$
    DECLARE
        cobrado FLOAT;
        vencido FLOAT;
        no_vencido FLOAT;
    BEGIN
        SELECT calcular_importe_cobrado_factura_venta($1, $2) INTO cobrado;
        SELECT calcular_importe_vencido_factura_venta($1, $2) INTO vencido;
        SELECT calcular_importe_no_vencido_factura_venta($1, $2) INTO no_vencido;
        RETURN cobrado != 0 AND ABS(cobrado) >= ABS(vencido + no_vencido);
    END;
    $BODY$ LANGUAGE plpgsql;    -- NEW! 1/08/2013

CREATE OR REPLACE FUNCTION fra_no_documentada(idfra INTEGER, 
                                              fecha DATE DEFAULT CURRENT_DATE)
    -- Fra. no documentada es la que no ha vencido ni tiene cobros porque 
    -- todavía no ha llegado ni un triste pagaré. O si ha llegado, no cubre 
    -- el total de la factura.
    RETURNS BOOLEAN
    AS $$
    DECLARE
        cobrado FLOAT;
        vencido FLOAT;
        no_vencido FLOAT;
        documentado FLOAT;
    BEGIN
        SELECT calcular_importe_documentado_factura_venta($1, $2) INTO documentado;
        SELECT calcular_importe_cobrado_factura_venta($1, $2) INTO cobrado;
        SELECT calcular_importe_vencido_factura_venta($1, $2) INTO vencido;
        SELECT calcular_importe_no_vencido_factura_venta($1, $2) INTO no_vencido;
        RETURN (cobrado = 0 AND vencido = 0 AND documentado = 0) 
            -- OJO: Si tiene cobros o está vencida pero la factura tiene 
            -- importe CERO, entonces va a clasificarse como NO DOCUMENTADA.
            OR (cobrado + documentado < vencido + no_vencido); 
            -- Vencido + No vencido = TOTAL factura. Si se ha documentado 
            -- menos que el total de la factura, es que tiene parte pendiente 
            -- de documentar. Así que la factura está no documentada, supongo, 
            -- aunque solo sea parcialmente.
    END;
    $$ LANGUAGE plpgsql; -- NEW! 2/08/2013 MODIFIED 7/08/2013 UPDATED 17/09/2013

CREATE OR REPLACE FUNCTION fra_no_vencida(idfra INTEGER, 
                                          fecha DATE DEFAULT CURRENT_DATE)
    RETURNS BOOLEAN
    -- Devuelve TRUE (no vencida o documentada no vencida) si:
    --   * no ha vencido nada de la factura.
    --   * lo que ha vencido está documentado y los vencimientos de 
    --     los documentos no han vencido.
    --   * La factura no está cobrada por adelanto del pago aunque formalmente 
    --     sí que esté no vencida.
    AS $$
    DECLARE
        cobrado FLOAT;
        vencido FLOAT;
        no_vencido FLOAT;
        documentado FLOAT;
    BEGIN
        SELECT calcular_importe_cobrado_factura_venta($1, $2) INTO cobrado;
        SELECT calcular_importe_vencido_factura_venta($1, $2) INTO vencido;
        SELECT calcular_importe_no_vencido_factura_venta($1, $2) INTO no_vencido;
        SELECT calcular_importe_documentado_factura_venta($1, $2) INTO documentado;
        RETURN cobrado = 0
               --AND NOT fra_no_documentada($1, $2)   -- Está documentada, pero
               AND ((vencido = 0 -- no ha vencido. Porque si ha vencido algo
                                -- entonces la factura está cobrada o impagada.
                     --AND cobrado = 0 -- A no ser que se haya adelantado 
                                      -- el cobro.
                    ) OR vencido = documentado)
               AND NOT fra_no_documentada($1, $2); -- Como es cortocircuitado,
                                                    -- así optimizo.
    END;
    $$ LANGUAGE plpgsql;        -- NEW! 2/08/2013

CREATE OR REPLACE FUNCTION fra_impagada(idfra INTEGER, 
                                        fecha DATE DEFAULT CURRENT_DATE)
    -- Factura impagada es la que ha vencido y ese importe (o parte) vencido 
    -- supera el documentado más el cobrado.
    RETURNS BOOLEAN
    AS $$
    DECLARE
        cobrado FLOAT;
        vencido FLOAT;
        documentado FLOAT;
    BEGIN
        SELECT calcular_importe_cobrado_factura_venta($1, $2) INTO cobrado;
        SELECT calcular_importe_vencido_factura_venta($1, $2) INTO vencido;
        SELECT calcular_importe_documentado_factura_venta($1, $2) INTO documentado;
        RETURN cobrado + documentado >= 0 and cobrado + documentado < vencido;
    END;
    $$ LANGUAGE plpgsql;        -- NEW! 2/08/2013

CREATE OR REPLACE FUNCTION fra_abono(idfra INTEGER, 
                                     fecha DATE DEFAULT CURRENT_DATE)
    -- Por compatibilidad con pclases. Pero en realidad ninguna factura de venta 
    -- es de abono. Las de abono van en otra tabla.
    RETURNS BOOLEAN
    AS $$
    BEGIN
        RETURN FALSE;
    END;
    $$ LANGUAGE plpgsql;        -- NEW! 2/08/2013

CREATE OR REPLACE FUNCTION calcular_importe_factura_venta(idfra INTEGER)
    -- Devuelve el importe total de la factura A PARTIR DE LOS VENCIMIENTOS. Si no tiene 
    -- vencimientos asumo que la factura está incompleta, algún usuario está trabajando 
    -- en ella o lo que sea y no la tengo en cuenta para nada.
    RETURNS FLOAT
    AS $$
        SELECT COALESCE(SUM(importe), 0) FROM vencimiento_cobro WHERE vencimiento_cobro.factura_venta_id = $1;
    $$ LANGUAGE SQL;    -- NEW! 5/08/2013

CREATE OR REPLACE FUNCTION calcular_credito_disponible(idcliente INTEGER, 
                                                       fecha DATE DEFAULT CURRENT_DATE, 
                                                       base FLOAT DEFAULT 0.0, 
                                                       devil BOOLEAN DEFAULT TRUE)
     -- Devuelve el crédito del cliente cuyo id se recibe. La cantidad "base" se resta 
     -- al crédito para el cálculo de crédito en el momento de formalizar un pedido. La 
     -- "base" debería ser el importe del pedido en ese momento y de ese modo saber si 
     -- el pedido se podría servir con el crédito actual. Por ejemplo: un pedido de 1.5k €
     -- (base) no podrá servirse si el crédito es de 1K.
     -- devil (because premature optimization is the root of all evil): Si TRUE usa las optimizaciones de crédito. Si FALSE las ignora; y así puedo comparar si el resultado es el mismo en los dos casos.
     RETURNS FLOAT
     AS $$
     DECLARE
        sin_documentar FLOAT;
        sin_vencer FLOAT;
        riesgo_concedido FLOAT;
        fraventa RECORD;
        credito FLOAT;
     BEGIN
        SELECT cliente.riesgo_concedido FROM cliente WHERE cliente.id = $1 INTO riesgo_concedido;
        IF riesgo_concedido = -1 THEN
            credito := 'Infinity'; 
        ELSIF devil = TRUE AND riesgo_concedido = 0 THEN   -- CWT: 10/10/2013 OPTIMIZACIÓN. 
                -- Si el crédito es cero, y como no cuento los abonos, ni me 
                -- molesto en calcular nada. Disponible: cero.
            credito := 0; 
        ELSE
            sin_documentar := 0;
            sin_vencer := 0;
            -- Inicialización del crédito. Por si no entra en el bucle.
            credito := riesgo_concedido - (sin_documentar + sin_vencer) - base;
            FOR fraventa IN SELECT * FROM factura_venta WHERE factura_venta.cliente_id = $1 LOOP
                IF fra_impagada(fraventa.id, $2) THEN
                    -- PSEUDOOPTIMIZACIÓN. Si alguna factura está impagada, crédito 0. No sigo.
                    RETURN 0;
                ELSIF fra_no_documentada(fraventa.id, $2) THEN
                    sin_documentar := sin_documentar + calcular_importe_factura_venta(fraventa.id); -- Esto no es exactamente así. Puede estar parcialmente 
                    -- documentada; pero me agarro al caso general en aras 
                    -- de la velocidad computacional.
                ELSIF fra_no_vencida(fraventa.id, $2) THEN
                    sin_vencer := sin_vencer + calcular_importe_factura_venta(fraventa.id);
                END IF;
                IF devil = TRUE THEN
                    -- OPTIMIZACIÓN: 10/10/2013. CWT: Si durante el cálculo llego 
                    -- a cero, paro. Dejo de seguir calculando. Lo mismo da que 
                    -- tenga cero como que tenga menos quince mil. No se le va a 
                    -- servir nada.
                    credito := riesgo_concedido - (sin_documentar + sin_vencer) - base;
                    IF credito < 0 THEN
                        RETURN 0;
                    END IF;
                END IF; 
            END LOOP;
            IF NOT devil THEN
                credito := riesgo_concedido - (sin_documentar + sin_vencer) - base;
            END IF; 
        END IF;
        RETURN credito;
     END;
     $$ LANGUAGE plpgsql;    -- NEW! 5/08/2013

-------------------------------------------------------------------------------

---- ALTERS TABLESss ---- s ----
ALTER TABLE lote ALTER COLUMN numlote SET DEFAULT ultimo_lote_mas_uno();
ALTER TABLE lote_cem ALTER COLUMN numlote
    SET DEFAULT ultimo_lote_cem_mas_uno(); -- NEW! 08/03/2007
ALTER TABLE partida_cem ALTER COLUMN numpartida
    SET DEFAULT ultima_partida_cem_mas_uno(); -- NEW! 08/03/2007
ALTER TABLE partida ALTER COLUMN numpartida
    SET DEFAULT ultima_partida_mas_uno();

ALTER TABLE bala ALTER COLUMN numbala SET DEFAULT ultima_bala_mas_uno();
ALTER TABLE bala ALTER COLUMN codigo SET DEFAULT ultimo_codigo_bala_mas_uno();
    -- NEW! 08/03/2007

ALTER TABLE rollo ALTER COLUMN numrollo SET DEFAULT ultimo_rollo_mas_uno();
ALTER TABLE rollo ALTER COLUMN codigo
    SET DEFAULT ultimo_codigo_rollo_mas_uno(); -- NEW! 08/03/2007

ALTER TABLE rollo_defectuoso ALTER COLUMN numrollo
    SET DEFAULT ultimo_rollo_defectuoso_mas_uno();       -- NEW! 07/03/2007
ALTER TABLE rollo_defectuoso ALTER COLUMN codigo
    SET DEFAULT ultimo_codigo_rollo_defectuoso_mas_uno();  -- NEW! 08/03/2007

ALTER TABLE ticket ALTER COLUMN numticket SET DEFAULT ultimo_ticket_mas_uno();
    -- NEW! 19/04/07

ALTER TABLE bala_cable ALTER COLUMN numbala
    SET DEFAULT ultima_bala_cable_mas_uno();       -- NEW! 13/06/2007
ALTER TABLE bala_cable ALTER COLUMN codigo
    SET DEFAULT ultimo_codigo_bala_cable_mas_uno();  -- NEW! 13/06/2007

ALTER TABLE rollo_c ALTER COLUMN numrollo SET DEFAULT ultimo_rollo_c_mas_uno();
    -- NEW! 02/06/2008
ALTER TABLE rollo_c ALTER COLUMN codigo
    SET DEFAULT ultimo_codigo_rollo_c_mas_uno();    -- NEW! 02/06/2008

---- REGLAS -----

---- ÍNDICES ----
CREATE INDEX cerid ON producto_venta (campos_especificos_rollo_id);
CREATE UNIQUE INDEX idarticulo ON articulo (id);    -- NEW! 20/07/2009
CREATE INDEX rid ON articulo (rollo_id);
CREATE INDEX bid ON articulo (bala_id);
CREATE INDEX bbid ON articulo (bigbag_id);
CREATE INDEX cjid ON articulo (caja_id);
CREATE INDEX pdpid ON articulo (parte_de_produccion_id);
CREATE INDEX pvid ON articulo (producto_venta_id);
CREATE INDEX asid ON articulo (albaran_salida_id);
CREATE INDEX rdid ON articulo (rollo_defectuoso_id);
CREATE INDEX bcid ON articulo (bala_cable_id);
CREATE INDEX rcid ON articulo (rollo_c_id);
CREATE INDEX articuloid ON articulo (id);
CREATE INDEX cajaid ON articulo (caja_id);    -- NEW! 20/07/2009
CREATE UNIQUE INDEX idcaja ON caja (id);        -- NEW! 20/07/2009
CREATE UNIQUE INDEX idpale ON pale (id);        -- NEW! 20/07/2009
CREATE INDEX paleid ON caja (pale_id);          -- NEW! 20/07/2009
CREATE INDEX pid ON rollo (partida_id);
CREATE INDEX lid ON bala (lote_id);
CREATE INDEX pcid ON partida (partida_carga_id);
CREATE INDEX cliid ON albaran_salida (cliente_id);
CREATE INDEX prcid ON stock_almacen (producto_compra_id);
CREATE INDEX aid ON stock_almacen (almacen_id);
CREATE UNIQUE INDEX prcid_aid ON stock_almacen (producto_compra_id, almacen_id);
CREATE UNIQUE INDEX he ON historial_existencias (producto_venta_id, almacen_id, fecha);
CREATE UNIQUE INDEX hec ON historial_existencias_compra (producto_compra_id, almacen_id, fecha);
CREATE INDEX pcobsoleto ON producto_compra (obsoleto);

---- TRIGGERS ----
CREATE FUNCTION un_solo_almacen_ppal() RETURNS TRIGGER AS '
    BEGIN
--        -- Casos a cubrir:
--        IF OLD IS NULL THEN
--            IF (SELECT COUNT(id) FROM almacen WHERE principal = TRUE) = 0 THEN
--                -- 1.- Que sea el primer almacén que se crea. Debe ser 
--                --     el principal.
--                NEW.principal = TRUE;
--            ELSE
--                -- 2.- Que sea cualquier otro. principal = FALSE.
--                NEW.principal = FALSE;
--            END IF;
--        ELSE    -- OLD IS NOT NULL, está en UPDATE.
--            -- 3.- Que esté actualizando un almacén. 
--            -- IF OLD.principal = TRUE
--                -- Si es el principal, se deja como estaba. 
--                -- NEW.principal = TRUE
--            -- ELSE
--                -- Si no lo es, se pone principal al FALSE.
--                -- NEW.principal = FALSE
--            -- END IF;
--            NEW.principal = OLD.principal;
--        END IF;
        -- Mucho más fácil. Si ya hay un almacén principal el nuevo registro 
        -- debe estar a FALSE en el campo principal. Si no hay ninguno, tanto 
        -- si estoy creando como actualizando registros, devuelvo TRUE y será 
        -- el primero. Las siguientes veces ya siempre devolverá FALSE en ese 
        -- campo.
        IF (SELECT COUNT(id) FROM almacen WHERE principal = TRUE) = 0 THEN
            NEW.principal = TRUE; 
        ELSE
            NEW.principal = FALSE;
        END IF;
        RETURN NEW;
        -- OJO: Si se hace un UPDATE con varios registros, el primero de 
        -- ellos se quedará con el principal a TRUE dependiendo de cómo 
        -- se lo monte el planificador de consultas. De todos modos no me 
        -- preocupa porque el ORM siempre ataca los registros individualmente.
        -- El único problema latente es que hasta que se haga el sync() o 
        -- syncUpdate() el objeto tendrá ese atributo a True.
    END;
' LANGUAGE plpgsql;

CREATE FUNCTION un_solo_almacen_ppal_pero_el_ultimo() RETURNS TRIGGER AS '
    BEGIN
        -- Vale. La idea es justo la contraria que en el caso anterior. Ahora 
        -- voy a intentar respetar el valor del registro nuevo. Si no hay 
        -- definido almacén principal, el nuevo es el principal. Si ya lo 
        -- había y el nuevo quiere serlo, le dejo.
        IF NEW.principal = TRUE THEN
            UPDATE almacen SET principal = FALSE;
        ELSE
            IF (SELECT COUNT(id) FROM almacen WHERE principal = TRUE) = 0 THEN
                NEW.principal = TRUE; 
            END IF;
        END IF;
        RETURN NEW;
    END;
' LANGUAGE plpgsql;

CREATE TRIGGER tr_un_solo_almacen_ppal_pero_el_ultimo 
--CREATE TRIGGER tr_un_solo_almacen_ppal 
    BEFORE INSERT OR UPDATE ON almacen 
    --FOR EACH ROW EXECUTE PROCEDURE un_solo_almacen_ppal();
    FOR EACH ROW EXECUTE PROCEDURE un_solo_almacen_ppal_pero_el_ultimo();

