#!/bin/bash

# Empiezo. Variables y fecha y hora en que empieza el jaleo:
ORIGEN=192.168.1.100
BACALL=192.168.1.26
date 

# Pasos:
# 1.- rsync de compartido
ssh root@$ORIGEN rsync -av /home/compartido root@$BACALL:/home/

# 2.- copia y restauración de la BD
# Backup de la base de datos. No quiero ver nada.
echo "Copiando datos de alfred..."
time /usr/bin/pg_dump --host $ORIGEN --port 5432 --username "postgres" --role "geotexan" --no-password  --format custom --blobs --encoding UTF8 --verbose --file "/home/bogado/Geotexan/backups_sql/20120628_ginn.backup" "ginn" 2>&1>/dev/null

# Creo triggers a mano (pg_* no los maneja bien) metiendo toda la estructura.
echo "Creando estructura en bacall..."
psql --host $BACALL -U geotexan ginn < tablas.sql 2>&1 | grep -v NOTICE

# Restauro resto de datos
echo "Restaurando datos en bacall..."
time /usr/bin/pg_restore --host $BACALL --port 5432 --username "postgres" --dbname "ginn" --role "geotexan" --no-password  --disable-triggers --clean --verbose "/home/bogado/Geotexan/backups_sql/20120628_ginn.backup" 2>&1 | grep ERROR

# 3.- cambio de IP por DHCP
ssh root@$ORIGEN dhclient -r -v && dhclient -v eth0
ssh root@$BACALL dhclient -v eth0

# 4.- Tiro base de datos en ORIGEN para evitar que se conecte alguien por error.
ssh root@$ORIGEN /etc/init.d/postgresql stop

# S'acabó 
date
echo "Finitto"

