databases="ginn qinn bpinn crisva fbinn"
for db in $databases; do
    psql $db << EOF 
-- Crea la tabla de etiquetas con la nueva etiqueta para EkoTex
CREATE TABLE modelo_etiqueta(
    id SERIAL PRIMARY KEY, 
    nombre TEXT,    -- Nombre descriptivo de la etiqueta.
    modulo TEXT,    -- Módulo (fichero python sin extensión) donde reside 
                    -- la función que se invocará para generar la etiqueta.
    funcion TEXT    -- Nombre de la función que devolverá un PDF con las 
                    -- etiquetas.
);
INSERT INTO modelo_etiqueta (nombre, modulo, funcion) VALUES ('EkoTex', 'ekotex', 'etiqueta_rollos_portrait'); 
ALTER TABLE campos_especificos_rollo ADD COLUMN modelo_etiqueta_id INT REFERENCES modelo_etiqueta DEFAULT NULL;
UPDATE campos_especificos_rollo SET modelo_etiqueta_id = NULL;
EOF
done
echo "Ahora conéctate y comprueba desde pclases que tienes permisos sobre la tabla, sino, toca hacer un GRANT ALL ON modelo_etiqueta TO quiensea;"

