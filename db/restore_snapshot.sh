#!/bin/bash

# Crea una base de datos de nombre igual al del archivo de backup y 
# restaura su contenido.

if [ $# -eq 1 ]; then
    DUMP=$1
    HOST=pennyworth
    HOST_BAKS=bacall
    #PATH_BAKS="/home/bogado/backups_sql"
    PATH_BAKS="backups_sql"
    FECHA=$(echo $DUMP | cut -d '.' -f 1)
    PARTENOMBRE=$(echo $DUMP | cut -d '.' -f 2)
    NOMBD="$PARTENOMBRE"_"$FECHA"
    if [ ! -f /tmp/$DUMP ]; then
        echo "Copiando fichero de copia de seguridad..."
        scp $HOST_BAKS:$PATH_BAKS/$DUMP /tmp
    fi
    echo "Creando base de datos $NOMBD en $HOST..."
    createdb -h $HOST -O geotexan -E 'UTF-8' $NOMBD
    echo "Restaurando $DUMP en $NOMBD en $HOST..."
    pg_restore -h $HOST -c -d $NOMBD /tmp/$DUMP
    echo "Creando fichero de configuración..."
    cp ../ginn/framework/ginn.conf ../ginn/framework/ginn.conf.$FECHA
    echo "dbname  $NOMBD" >> ../ginn/framework/ginn.conf.$FECHA
    echo "host    $HOST" >> ../ginn/framework/ginn.conf.$FECHA 
else
    echo "Debe especificar el nombre del archivo de copia de seguridad."
    echo "Por ejemplo:"
    echo "$0 20131231_1400.ginn.dump"
fi

