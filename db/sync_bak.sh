#!/bin/bash
FECHA=$(date +"%Y%m%d_%H%M")
FDEST=/tmp/$FECHA.ginn.dump

echo "Creando volcado de la base de datos..."
/usr/bin/pg_dump --host 192.168.1.100 --port 5432 --username "postgres" --role "geotexan" --no-password  --format custom --blobs --encoding UTF8 --verbose ginn > $FDEST 

# Aprovecho y hago una copia de seguridad ante desastres...
echo "Creando réplica bak_ginn en bacall (producción)..."
dropdb bak_ginn
createdb -E UTF8 -O geotexan bak_ginn "Copia de ginn para desarrollo y pruebas" && pg_restore -d bak_ginn $FDEST
echo "Copia completada"

find /tmp/*.ginn.dump -not -anewer $FDEST -exec rm '{}' \;

