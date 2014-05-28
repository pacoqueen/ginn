#!/bin/bash

# HOST=alfred
HOST=bacall
HOST_REMOTO=gtx.duckdns.com
PATH_BAKS=backups_sql/
PATH_LOG=/home/compartido/Geotex-INN/ginn/

function create_fbak(){
	echo "Creando copia de seguridad..."
    ssh bogado@$HOST "/home/compartido/Geotex-INN/db/backup_ginn.sh"
    if [ ! $? -eq 0 ]; then     # Estoy en nostromo
    	echo "    Tunelando para crear copia..."
        ssh bogado@gtx.duckdns.org "ssh bogado@bacall '/home/compartido/Geotex-INN/db/backup_ginn.sh'"
    fi
    echo "    Copia creada."
}

function get_remote_fbak(){
    echo "Copiando fichero de copia de seguridad..."
    # Intento así para ver si estoy en la fábrica:
    DUMP=$(ssh bogado@bacall "ls $PATH_BAKS -tr | tail -n 1")
    scp $HOST:$PATH_BAKS/$DUMP /tmp    
    if [ ! $? -eq 0 ]; then     # Estoy en nostromo
    	DUMP=$(ssh bogado@gtx.duckdns.org "ssh bogado@bacall \"ls $PATH_BAKS -tr | tail -n 1\"")
        echo "    Obteniendo copia a través de Internet..."
        # Primero, la copio a justinho
        ssh bogado@gtx.duckdns.org "scp bogado@bacall:$PATH_BAKS/$DUMP /tmp"
        # Después me la traigo
        scp bogado@gtx.duckdns.org:/tmp/$DUMP /tmp
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
        ssh bogado@gtx.duckdns.org "scp bogado@bacall:$PATH_LOG/ginn.log /tmp"
        # Después me la traigo
        scp bogado@gtx.duckdns.org:/tmp/ginn.log /tmp
        echo "    Copia exitosa por túnel ssh."
    else
        echo "    Copia exitosa por LAN."
    fi
}

function restore_db(){
	if [ -z "$DUMP" ]; then
    	DUMP=$(ssh bogado@gtx.duckdns.org "ssh bogado@bacall \"ls $PATH_BAKS -tr | tail -n 1\"")
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
