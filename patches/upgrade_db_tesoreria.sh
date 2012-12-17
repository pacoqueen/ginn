databases="ginn"
for db in $databases; do
    psql $db << EOF
ALTER TABLE pagare_cobro ADD COLUMN a_la_orden BOOLEAN DEFAULT TRUE;
UPDATE pagare_cobro SET a_la_orden = TRUE;
CREATE TABLE banco(
    id SERIAL PRIMARY KEY, 
    nombre TEXT
);
ALTER TABLE pagare_cobro ADD COLUMN banco_id INT REFERENCES banco DEFAULT NULL;
UPDATE pagare_cobro SET banco_id = NULL;
CREATE TABLE remesa(
    id SERIAL PRIMARY KEY,
    banco_id INT REFERENCES banco DEFAULT NULL, 
    fecha_prevista DATE DEFAULT NULL, 
    codigo TEXT DEFAULT '', 
    fecha_cobro DATE DEFAULT NULL
);
ALTER TABLE pagare_cobro ADD COLUMN remesa_id INT REFERENCES remesa DEFAULT NULL;
UPDATE pagare_cobro SET remesa_id = NULL;
ALTER TABLE confirming ADD COLUMN banco_id INT REFERENCES banco DEFAULT NULL;
UPDATE confirming SET banco_id = NULL;
ALTER TABLE confirming ADD COLUMN remesa_id INT REFERENCES remesa DEFAULT NULL;
UPDATE confirming SET remesa_id = NULL;
EOF
done
#echo "Ahora conéctate y comprueba desde pclases que tienes permisos sobre la tabla, sino, toca hacer un GRANT ALL ON auditoria TO quiensea; GRANT ALL on auditoria_id_seq TO quiensea;"

