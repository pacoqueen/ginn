databases="dev_ginn ginn"
for db in $databases; do
    psql $db << EOF
CREATE TABLE documento_de_pago(
    id SERIAL PRIMARY KEY, 
    documento TEXT DEFAULT ''
);
CREATE TABLE forma_de_pago(
    id SERIAL PRIMARY KEY, 
    documento_de_pago_id INT REFERENCES documento_de_pago, 
    plazo INT DEFAULT 120, 
    activa BOOLEAN DEFAULT TRUE 
);
ALTER TABLE pedido_venta ADD COLUMN forma_de_pago_id INT REFERENCES forma_de_pago DEFAULT NULL;
ALTER TABLE pagare_cobro ADD COLUMN a_la_orden BOOLEAN DEFAULT TRUE;
UPDATE pagare_cobro SET a_la_orden = TRUE;
CREATE TABLE banco(
    id SERIAL PRIMARY KEY, 
    nombre TEXT, 
    iban TEXT DEFAULT '', 
    direccion TEXT DEFAULT '',  
    ciudad TEXT DEFAULT '', 
    provincia TEXT DEFAULT '', 
    pais TEXT DEFAULT 'España', 
    contacto TEXT DEFAULT '', 
    web TEXT DEFAULT '', 
    telefono TEXT DEFAULT '', 
    fax TEXT DEFAULT '', 
    limite FLOAT DEFAULT NULL, 
    interes FLOAT DEFAULT NULL, 
    comision_estudio FLOAT DEFAULT NULL, 
    concentracion FLOAT DEFAULT NULL, 
    exceso_vencimiento INT DEFAULT NULL
);
ALTER TABLE pagare_cobro ADD COLUMN banco_id INT REFERENCES banco DEFAULT NULL;
UPDATE pagare_cobro SET banco_id = NULL;
CREATE TABLE remesa(
    id SERIAL PRIMARY KEY,
    banco_id INT REFERENCES banco DEFAULT NULL, 
    fecha_prevista DATE DEFAULT NULL, 
    codigo TEXT DEFAULT '', 
    fecha_cobro DATE DEFAULT NULL, 
    aceptada BOOLEAN DEFAULT FALSE
);
ALTER TABLE confirming ADD COLUMN banco_id INT REFERENCES banco DEFAULT NULL;
UPDATE confirming SET banco_id = NULL;
CREATE TABLE concentracion_remesa(
    id SERIAL PRIMARY KEY, 
    banco_id INT NOT NULL REFERENCES banco, 
    cliente_id INT NOT NULL REFERENCES cliente, 
    concentracion FLOAT
);
CREATE TABLE efecto(
    id SERIAL PRIMARY KEY, 
    pagare_cobro_id INT REFERENCES pagare_cobro DEFAULT NULL, 
    confirming_id INT REFERENCES confirming DEFAULT NULL,
    cuenta_bancaria_cliente_id INT REFERENCES cuenta_bancaria_cliente DEFAULT NULL 
    CHECK (pagare_cobro_id IS NULL +^ confirming_id IS NULL)
);

GRANT ALL ON DATABASE ginn TO geotexan;
GRANT ALL ON DATABASE dev_ginn TO geotexan;
GRANT ALL ON remesa TO geotexan;
GRANT ALL ON banco TO geotexan;
GRANT ALL ON concentracion_remesa TO geotexan;
GRANT ALL ON remesa_id_seq TO geotexan;
GRANT ALL ON banco_id_seq TO geotexan;
GRANT ALL ON concentracion_remesa_id_seq TO geotexan;
GRANT ALL ON efecto TO geotexan;
GRANT ALL ON efecto_id_seq TO geotexan;
GRANT ALL ON documento_de_pago TO geotexan;
GRANT ALL ON documento_de_pago_id_seq TO geotexan;
GRANT ALL ON forma_de_pago TO geotexan;
GRANT ALL ON forma_de_pago_id_seq TO geotexan;
CREATE TABLE efecto__remesa(
    efecto_id INT NOT NULL REFERENCES efecto, 
    remesa_id INT NOT NULL REFERENCES remesa
);      -- NEW! 17/01/2013
GRANT ALL ON efecto__remesa TO geotexan;
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
    proveedor_id INT REFERENCES proveedor DEFAULT NULL
);

CREATE TABLE vencimiento_valor_presupuesto_anual(
    id SERIAL PRIMARY KEY,
    valor_presupuesto_anual_id INT REFERENCES valor_presupuesto_anual, 
    fecha DATE NOT NULL
);

CREATE TABLE valor_presupuesto_anual(
    id SERIAL PRIMARY KEY, 
    concepto_presupuesto_anual_id INT REFERENCES concepto_presupuesto_anual NOT NULL, 
    mes DATE NOT NULL, 
    importe FLOAT DEFAULT 0.0, 
    precio FLOAT DEFAULT 1
);

GRANT ALL ON presupuesto_anual TO geotexan;
GRANT ALL ON presupuesto_anual_id_seq TO geotexan;
GRANT ALL ON concepto_presupuesto_anual TO geotexan;
GRANT ALL ON concepto_presupuesto_anual_id_seq TO geotexan;
GRANT ALL ON valor_presupuesto_anual TO geotexan;
GRANT ALL ON valor_presupuesto_anual_id_seq TO geotexan;

CREATE TABLE tipo_de_proveedor(
    id SERIAL PRIMARY KEY, 
    descripcion TEXT
);

ALTER TABLE proveedor ADD COLUMN tipo_de_proveedor_id INT REFERENCES tipo_de_proveedor DEFAULT NULL;
GRANT ALL ON tipo_de_proveedor TO geotexan;
GRANT ALL ON tipo_de_proveedor_id_seq TO geotexan;

CREATE TABLE tipo_de_cliente(
    id SERIAL PRIMARY KEY, 
    descripcion TEXT
);

ALTER TABLE cliente ADD COLUMN tipo_de_cliente_id INT REFERENCES tipo_de_cliente DEFAULT NULL;
GRANT ALL ON tipo_de_cliente TO geotexan;
GRANT ALL ON tipo_de_cliente_id_seq TO geotexan;


EOF
done

