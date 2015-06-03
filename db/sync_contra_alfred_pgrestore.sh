#!/bin/bash

# HOST=alfred
HOST=bacall
HOST_REMOTO=gtx.duckdns.org
PATH_BAKS=backups_sql/
PATH_LOG=/home/compartido/Geotex-INN/ginn/
SSH="ssh -oBatchMode=yes "

function create_fbak(){
	echo "Creando copia de seguridad..."
    $SSH bogado@$HOST "/home/compartido/Geotex-INN/db/backup_ginn.sh"
    if [ ! $? -eq 0 ]; then     # Estoy en nostromo
    	echo "    Tunelando para crear copia..."
        $SSH bogado@$HOST_REMOTO "$SSH bogado@bacall.geotexan.es '/home/compartido/Geotex-INN/db/backup_ginn.sh'"
    fi
    echo "    Copia creada."
}

function get_remote_fbak(){
    echo "Copiando fichero de copia de seguridad..."
    # Intento así para ver si estoy en la fábrica:
    DUMP=$($SSH bogado@bacall.geotexan.es "ls $PATH_BAKS -tr | tail -n 1")
    scp $HOST:$PATH_BAKS/$DUMP /tmp    
    if [ ! $? -eq 0 ]; then     # Estoy en nostromo
    	DUMP=$($SSH bogado@$HOST_REMOTO "ssh bogado@bacall.geotexan.es \"ls $PATH_BAKS -tr | tail -n 1\"")
        echo "    Obteniendo copia a través de Internet..."
        # Primero, la copio a justinho
        $SSH bogado@$HOST_REMOTO "scp bogado@bacall.geotexan.es:$PATH_BAKS/$DUMP /tmp"
        # Después me la traigo
        scp bogado@$HOST_REMOTO:/tmp/$DUMP /tmp
        echo "    Copia exitosa por túnel ssh."
    else
        echo "    Copia exitosa por LAN."
    fi
}

function get_remote_log(){
    echo "Copiando fichero de log..."
    # Intento así para ver si estoy en la fábrica:
    scp $HOST:$PATH_LOG/ginn.log /tmp    
    if [ ! $? -eq 0 ]; then     # Estoy en nostromo
        echo "    Obteniendo copia a través de Internet..."
        # Primero, la copio a justinho
        $SSH bogado@$HOST_REMOTO "scp bogado@bacall.geotexan.es:$PATH_LOG/ginn.log /tmp"
        # Después me la traigo
        scp bogado@$HOST_REMOTO:/tmp/ginn.log /tmp
        echo "    Copia exitosa por túnel ssh."
    else
        echo "    Copia exitosa por LAN."
    fi
}

function restore_db(){
	if [ -z "$DUMP" ]; then
    	DUMP=$($SSH bogado@$HOST_REMOTO "ssh bogado@bacall.geotexan.es \"ls $PATH_BAKS -tr | tail -n 1\"")
    	echo "        [DEBUG] DUMP: $DUMP"
    fi 
	echo "Restaurando copia en ginn local..."
	pg_restore -c -d ginn /tmp/$DUMP
	echo "    Restaurando copia en dev_ginn local..."
	pg_restore -c -d dev_ginn /tmp/$DUMP
	echo "    Copia restaurada"
}

function restore_log(){
	echo "Restaurando log..."
	mv -f /tmp/ginn.log ../ginn
	echo "    Copia de log completada."
}

create_fbak
get_remote_fbak
restore_db
get_remote_log
restore_log
