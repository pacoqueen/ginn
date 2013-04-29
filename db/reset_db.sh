#!/bin/sh

# Reinicia la base de datos creando una copia de seguridad, reordenándola y 
# recreando la BD de nuevo en base a la copia.
# Útil para los cambios en tablas.sql

if [ $# -lt 3 ]; then
    echo "Debe indicar el nombre de la BD a reiniciar, usuario y contraseña."
else
    ./backup_bd.sh $1
    BAK=$(ls *.sql -tr | tail -n 1)
    echo -n "Fichero de copia de seguridad... " 
    echo $BAK
    ./reorder_dump.py tablas.sql  $BAK > reordered_dump_datos.sql
    ./init_db.sh $1 $2 $3 reordered_dump_datos.sql
    if [ $1 == "qinn" ]; then
        cd ../framework
        ./cambiar_conf.sh q
        cd -
    elif [ $1 == "ginn" ]; then
        cd ../framework
        ./cambiar_conf.sh g
        cd -
    elif [ $1 == "crisva" ]; then
        cd ../framework
        ./cambiar_conf.sh c
        cd -
    elif [ $1 == "bpinn" ]; then
        cd ../framework
        ./cambiar_conf.sh b
        cd -
    elif [ $1 == "fbinn" ]; then
        cd ../framework
        ./cambiar_conf.sh f
        cd -
    fi 
fi

