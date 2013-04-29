#!/bin/sh

TETSUO=chaparobo.no-ip.com

echo "Copiando último backup de base de datos desde tetsuo"
FICHERO=$(ssh blancoperez@$TETSUO "ls *bpinn.tar.bz2 -tr | tail -n 1")
scp blancoperez@$TETSUO:$FICHERO /tmp
echo "Restaurando base de datos en local"
./init_db.py /tmp/$FICHERO ../framework/ginn.conf.blancoperez
echo "Finitto"

