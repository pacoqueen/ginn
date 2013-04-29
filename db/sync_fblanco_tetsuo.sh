#!/bin/sh

TETSUO=chaparobo.no-ip.com
USER=fblanco

echo "Copiando último backup de base de datos desde tetsuo"
FICHERO=$(ssh $USER@$TETSUO "ls dump_datos* -tr | tail -n 1")
scp $USER@$TETSUO:$FICHERO /tmp
echo "Restaurando base de datos en local"
./init_db.py /tmp/$FICHERO ../framework/ginn.conf.fblanco
echo "Finitto"

