#!/bin/sh

if [ $# -eq 1 ]; then 
  if [ "$1" = "-h" ]; then
    echo 'Script para sincronizar los ficheros de producción de "compartido" con los del directorio de despliegue.'
  else
    echo "¿Qué quieres hacer? Las opciones son:"
    echo "-h   Ayuda"
  fi
  exit
fi

DEST=/home/compartido
if [ -d $DEST ]; then 
    # Este script está en loquesea/Geotex-INN/ginn/lib
    DIRUTILS=`dirname $(readlink -f $0)`
    cd $DIRUTILS 
    cd ../../..
    echo "Estamos en ",
    echo $(pwd)
    #read -p "ENTER para corregir permisos de grupo..." mierda
    echo "Corrigiendo permisos de grupo..." 
    chmod g+rw -R Geotex-INN
    #read -p "Copiando fichero de configuración. Pulsa ENTER para continuar..." mierda
    echo "Coppiando fichero de log y configuración..."
    cp -vf $DEST/Geotex-INN/ginn/framework/ginn.conf /tmp
    cp -vf $DEST/Geotex-INN/ginn/ginn.log /tmp
    #read -p "Copiando ficheros de desarrollo a compartido. Pulsa ENTER para empezar..." mierda
    echo "Copiando ficheros de desarrollo a compartido..."
    sudo rsync -av Geotex-INN $DEST
    #read -p "Eliminado .git. Pulsa ENTER para empezar..." merdellOn
    echo "Eliminado .git..."
    find $DEST/Geotex-INN -name ".git" -type d -exec rm -rf '{}' \;
    rm $DEST/Geotex-INN/.gitignore
    #read -p "Pulsa ENTER para restaurar fichero de configuración..." mierda
    echo "Restaurando fichero de log y configuración..."
    cp -vf /tmp/ginn.conf $DEST/Geotex-INN/ginn/framework/
    cp -vf /tmp/ginn.log $DEST/Geotex-INN/ginn/
    #read -p "Asignando permisos. Pulsa ENTER para seguir..." merde
    echo "Regenerando log..."
    cd Geotex-INN
    sudo chown $(whoami) $DEST/Geotex-INN/doc/ChangeLog.git.txt
    chmod +w $DEST/Geotex-INN/ginn/doc/ChangeLog.git.txt
    git log | grep -v "commit " | grep -v "Author:" | egrep -v "$^" | grep -v "Merge: " > $DEST/Geotex-INN/doc/ChangeLog.git.txt
    echo "Asignando permisos..."
    sudo chown -R nobody:nogroup $DEST/Geotex-INN
else
    echo "Este script debe ejecutarse en el servidor"
fi


