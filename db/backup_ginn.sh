#!/bin/bash
FECHA=$(date +"%Y%m%d_%H%M")
FDEST=/home/bogado/backups_sql/$FECHA.ginn.dump
FCHAP=`date +"ginn.%w.dump"`

echo "Creando volcado de la base de datos..."
/usr/bin/pg_dump --host 192.168.1.100 --port 5432 --username "postgres" --role "geotexan" --no-password  --format custom --blobs --encoding UTF8 --verbose ginn > $FDEST 

if [ "$1q" = "cq" ]; then
    echo "Copiando a chaparobo..."
    # Machaco última copia remota del mismo día de la semana para tener 
    # 7 como máximo. No quiero inundar mi servidor.
    scp $FDEST autossh@chaparobo.no-ip.com:$FCHAP
fi

# Aprovecho y hago una copia para pruebas de desarrollo.
echo "Creando réplica dev_ginn en bacall (producción)..."
dropdb dev_ginn
createdb -E UTF8 -O geotexan dev_ginn "Copia de ginn para desarrollo y pruebas" && pg_restore -d dev_ginn $FDEST
echo "Copia completada"

# Y actualizo también la del servidor de pruebas:
echo "Creando réplica dev_ginn en pennyworth (pruebas)..."
dropdb -U geotexan -h pennyworth.geotexan.es dev_ginn
createdb -E UTF8 -O geotexan -U geotexan -h pennyworth.geotexan.es dev_ginn "Copia de ginn para desarrollo y pruebas" && pg_restore -U geotexan -h pennyworth.geotexan.es -d dev_ginn $FDEST
echo "Réplica completada"

