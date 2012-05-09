#!/bin/bash
# Hace una copia de seguridad de la BD, la copia por SSH al servidor remoto o a uno de los dos portátiles de desarrollo 
# y al directorio BD con el nombre por defecto usado por el scrip de restauración.

# TODO: Usar pg_dump con la opción -Fc (permite usar formato personalizado y va comprimido por defecto) y pg_restore 
#       en el init_db.sh en lugar de psql a pelo, que evita errores por tablas mal ordenadas en la copia. Esto funciona 
#       en la máquina de desarrollo:
#       pg_dump -Fc qinn | pg_restore -c -d qinn

function usage {
    echo "Uso: $0 [nombre_base_datos] [c|p|d]"
    exit 1
}

if [ $# -eq 0 ]; then
    NOMBREBD="ginn"
    DEST=""
elif [ $# -eq 1 ]; then
    if [ $1 = "c" ] || [ $1 = "p" ] || [ $1 = "d" ]; then
        NOMBREBD="ginn"
        DEST=$1
    else
        NOMBREBD=$1
        DEST=""
    fi
elif [ $# -eq 2 ]; then
    NOMBREBD=$1
    DEST=$2
else
    usage
fi

PG_DUMP=$(which pg_dump)
FECHA=`date +%Y_%m_%d_%H_%M`
NOMBRE=dump_datos_$NOMBREBD\_$FECHA.sql
NOMBRETAR=$NOMBRE.tar.bz2
DIR=$(basename `pwd`)
if [ $NOMBREBD = "qinn" ]; then
    USUARIO_REMOTO="queen"
elif [ $NOMBREBD = "bpinn" ]; then
    USUARIO_REMOTO="blancoperez"
elif [ $NOMBREBD = "ginn" ]; then
    USUARIO_REMOTO="autossh"
elif [ $NOMBREBD = "crisva" ]; then
    USUARIO_REMOTO="crisva"
elif [ $NOMBREBD = "fbinn" ]; then
    USUARIO_REMOTO="fblanco"
else
    USUARIO_REMOTO="tunelssh"
fi 

function dump {
    # Vuelca el contenido de la BD (primer parámetro) al archivo pasado como segundo parámetro.
    $PG_DUMP $1 -a -f $2
}

function comprime {
    # Comprime el contenido de la copia.
    tar cvjf $NOMBRETAR $1
}

function copiassh {
    # Copia por ssh el archivo recibido como primer parámetro al destino indicado por una letra recibida en el segundo parámetro.
    # Si es destino es el servidor remoto comprime el archivo para aligerar la transferencia por Internet.
    if [ $2 = "c" ]; then
        echo "Comprimiendo $1 a $NOMBRETAR..."
        comprime $1 
        echo "Introduce la contraseña del servidor remoto del túnel ssh:"
        scp -C $NOMBRETAR $USUARIO_REMOTO@chaparobo.no-ip.com:dump_datos.sql.tar.bz2
    elif [ $2 = "p" ]; then
        echo "Introduce la contraseña del usuario geotexan en el portátil .200:"
        # scp $NOMBRE geotexan@192.168.1.200:geotexan/Codificación/BD/dump_datos.sql
        scp -C $1 queen@192.168.1.200:geotexinn02/BD/dump_datos.sql
    elif [ $2 = "d" ]; then
        echo "Introduce la contraseña del usuario geotexan en el portátil .201:"
        scp -C $1 geotexan@192.168.1.201:geotexinn02/BD/dump_datos.sql
    fi
}

function copialocal {
    # Copia el dump al directorio BD local con el nombre reconocido por «./create_and_populate.sh».
    if [ ! $DIR = "BD" ] && [ ! $DIR = "geotexinn02" ]; then
        # Asumo que estoy en el directorio padre (normalmente solo ejecuto el script desde allí).
        echo "Copiando a geotexinn02/BD/dump_datos.sql"
        cp $1 geotexinn02/BD/dump_datos.sql
    elif [ $DIR = "BD" ]; then
        echo "Copiando dentro de BD a dump_datos.sql"
        cp $1 dump_datos.sql
    fi
}


echo "Haciendo backup de la BD sobre $NOMBRE..."
dump $NOMBREBD $NOMBRE

if [ $DEST ]; then
    echo "Copiando por SSH..."
    copiassh $NOMBRE $DEST
fi
copialocal $NOMBRE

