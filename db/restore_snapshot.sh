#!/bin/bash

# Crea una base de datos de nombre igual al del archivo de backup y 
# restaura su contenido.

function check_nombre_fbak(){
    if [ ! "$(echo $1 | grep '.ginn.dump')" ]; then 
        DUMP=$1.ginn.dump
    else 
        DUMP=$1
    fi
}

function get_remote_fbak(){
    echo "Copiando fichero de copia de seguridad..."
    HOST_BAKS=bacall
    #PATH_BAKS="/home/bogado/backups_sql"
    PATH_BAKS="backups_sql"
    # Intento así para ver si estoy en la fábrica:
    scp $HOST_BAKS:$PATH_BAKS/$DUMP /tmp
    if [ ! $? -eq 0 ]; then     # Estoy en nostromo
        echo "Obteniendo copia a través de Internet..."
        # Primero, la copio a justinho
        ssh bogado@gtx.dyndns-server.com "scp bogado@bacall:backups_sql/$1 /tmp"
        # Después me la traigo
        scp bogado@gtx.dyndns-server.com:/tmp/$1 /tmp
    else
        echo "Copia exitosa por LAN."
    fi
}

function crear_bd(){
    HOST=pennyworth
    FECHA=$(echo $DUMP | cut -d '.' -f 1)
    PARTENOMBRE=$(echo $DUMP | cut -d '.' -f 2)
    NOMBD="$PARTENOMBRE"_"$FECHA" 
    WHORU=$(ssh bogado@pennyworth hostname)
    if [ ! "$WHORU" = "$HOST" ]; then
        HOST=localhost     # Estoy en nostromo
        OPTS=""
    else
        OPTS="-h $HOST "
    fi
    echo "Creando base de datos $NOMBD en $HOST..."
    createdb $OPTS -O geotexan -E 'UTF-8' $NOMBD
}

function restaurar_bd(){
    echo "Restaurando $DUMP en $NOMBD en $HOST..."
    pg_restore $OPTS -c -d $NOMBD /tmp/$DUMP
}

function crear_fconf(){
    echo "Creando fichero de configuración..."
    cp ../ginn/framework/ginn.conf ../ginn/framework/ginn.conf.$FECHA
    echo "dbname  $NOMBD" >> ../ginn/framework/ginn.conf.$FECHA
    echo "host    $HOST" >> ../ginn/framework/ginn.conf.$FECHA 
}

if [ $# -eq 1 ]; then
    check_nombre_fbak $1
    if [ ! -f /tmp/$DUMP ]; then
          get_remote_fbak $DUMP
    fi
    crear_bd
    restaurar_bd
    crear_fconf
else
    echo "Debe especificar el nombre del archivo de copia de seguridad."
    echo "Por ejemplo:"
    echo "$0 20131231_1400.ginn.dump"
fi

