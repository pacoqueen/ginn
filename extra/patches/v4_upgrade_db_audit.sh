databases="dev_ginn ginn" # qinn bpinn crisva fbinn"
for db in $databases; do
    psql $db << EOF
CREATE TABLE auditoria(
    id SERIAL PRIMARY KEY, 
    usuario_id INT REFERENCES usuario,  -- FK al usuario 
    ventana_id INT REFERENCES ventana,  -- FK ventana desde donde se ha hecho.
    dbpuid TEXT,          -- Me lo tiene que dar la capa superior.
    action TEXT,        -- creación, modificación o borrado
    ip TEXT DEFAULT NULL,   -- IP desde la que realizó la acción
    hostname TEXT DEFAULT NULL, -- Si es posible, el nombre de la máquina.
    fechahora TIMESTAMP DEFAULT LOCALTIMESTAMP(0), 
    descripcion TEXT DEFAULT NULL
);
GRANT ALL ON auditoria TO geotexan;
GRANT ALL ON auditoria_id_seq TO geotexan;
EOF
done
echo "Ahora conéctate y comprueba desde pclases que tienes permisos sobre la tabla, sino, toca hacer un GRANT ALL ON auditoria TO quiensea; GRANT ALL on auditoria_id_seq TO quiensea;"

