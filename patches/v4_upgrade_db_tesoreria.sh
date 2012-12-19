databases="dev_ginn ginn"
for db in $databases; do
    psql $db << EOF
ALTER TABLE pagare_cobro ADD COLUMN a_la_orden BOOLEAN DEFAULT TRUE;
UPDATE pagare_cobro SET a_la_orden = TRUE;
CREATE TABLE banco(
    id SERIAL PRIMARY KEY, 
    nombre TEXT, 
    iban TEXT DEFAULT '', 
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
ALTER TABLE pagare_cobro ADD COLUMN remesa_id INT REFERENCES remesa DEFAULT NULL;
UPDATE pagare_cobro SET remesa_id = NULL;
ALTER TABLE confirming ADD COLUMN banco_id INT REFERENCES banco DEFAULT NULL;
UPDATE confirming SET banco_id = NULL;
ALTER TABLE confirming ADD COLUMN remesa_id INT REFERENCES remesa DEFAULT NULL;
UPDATE confirming SET remesa_id = NULL;
CREATE TABLE concentracion_remesa(
    id SERIAL PRIMARY KEY, 
    banco_id INT NOT NULL REFERENCES banco, 
    cliente_id INT NOT NULL REFERENCES cliente, 
    concentracion FLOAT
);
GRANT ALL ON DATABASE ginn TO geotexan;
GRANT ALL ON remesa TO geotexan;
GRANT ALL ON banco TO geotexan;
GRANT ALL ON concentracion_remesa TO geotexan;
GRANT ALL ON remesa_id_seq TO geotexan;
GRANT ALL ON banco_id_seq TO geotexan;
GRANT ALL ON concentracion_remesa_id_seq TO geotexan;
EOF
done

