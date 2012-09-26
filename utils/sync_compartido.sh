#!/bin/sh

if [ $1 == "-h" || $1 == "--help" ]; then
    echo 'Script para sincronizar los ficheros de producción de "compartido" con los del directorio de despliegue.'
    exit
fi
DEST=/home/compartido
if [ -d $DEST ]; then 
    DIRUTILS=`dirname $(readlink -f $0)`
    echo $DIRUTILS
    cd $DIRUTILS 
    cd ../..
    cp -f $DEST/ginn/framework/ginn.conf /tmp
    rsync -av ginn $DEST/ginn
    chown -R nobody:nogroup $DEST/ginn
    cp -f /tmp/ginn.conf $DEST/ginn/framework/
else
    echo "Este script debe ejecutarse en el servidor"
fi


