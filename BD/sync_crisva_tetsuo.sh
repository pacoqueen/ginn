#!/bin/sh

TETSUO=chaparobo.no-ip.com

echo "Copiando último backup de base de datos desde tetsuo"
FICHERO=$(ssh crisva@$TETSUO "ls dump_datos* -tr | tail -n 1")
scp crisva@$TETSUO:$FICHERO /tmp
echo "Restaurando base de datos en local"
./init_db.py /tmp/$FICHERO ../framework/ginn.conf.crisva
echo "Finitto"

