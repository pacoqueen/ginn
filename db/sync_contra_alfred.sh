#!/bin/sh

ALFRED=192.168.1.100

echo "Copiando base de datos"
ssh geotexan@$ALFRED "./backup_bd.sh && cd geotexinn02/BD && tar cvjf /tmp/dd.tar.bz2 dump_datos.sql"
scp geotexan@$ALFRED:/tmp/dd.tar.bz2 /tmp
echo "Descomprimiendo base de datos"
tar xvjf /tmp/dd.tar.bz2 
echo "Restaurando base de datos en local"
./init_db.sh ginn geotexan gy298d.l dump_datos.sql 
echo "Restaurando configuración a local"
cd ../framework
cp -f ginn.conf ginn.conf.bak
cp -f ginn.conf.local ginn.conf
cd -
echo "Copiando log"
scp geotexan@$ALFRED:/home/compartido/betav2/formularios/ginn.log ../formularios

