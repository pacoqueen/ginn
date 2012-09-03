#!/bin/sh

HOST=alfred

if [ $# -eq 1 ]; then   # TODO: Detectar si es tar.bz2 o el .pgdump
    FPGDUMP=$1
else
    echo "Copiando base de datos"
    ssh geotexan@$HOST "/home/geotexan/geotexinn02/BD/backup_full.sh"
    scp geotexan@$HOST:/tmp/full_ginn.pgdump.tar.bz2 /tmp
    FPGDUMP=/tmp/full_ginn.pgdump
    cd /tmp
    tar xvjf /tmp/full_ginn.pgdump.tar.bz2
    cd -
fi
echo "Restaurando base de datos en local"
#dropdb ginn && createdb ginn -O geotexan --encoding UNICODE | grep -v NOTICE 
pg_restore -c -d ginn $FPGDUMP 
echo "Copiando log"
scp geotexan@$HOST:/home/compartido/betav2/formularios/ginn.log ../formularios

