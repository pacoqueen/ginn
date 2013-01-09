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
    # Este script está en loquesea/ginn/utils
    DIRUTILS=`dirname $(readlink -f $0)`
    cd $DIRUTILS 
    cd ../..
    echo "Estamos en ",
    echo $(pwd)
    #read -p "ENTER para corregir permisos de grupo..." mierda
    echo "Corrigiendo permisos de grupo..." 
    chmod g+rw -R ginn
    #read -p "Copiando fichero de configuración. Pulsa ENTER para continuar..." mierda
    echo "Coppiando fichero de log y configuración..."
    cp -vf $DEST/ginn/framework/ginn.conf /tmp
    cp -vf $DEST/ginn/formularios/ginn.log /tmp
    #read -p "Copiando ficheros de desarrollo a compartido. Pulsa ENTER para empezar..." mierda
    echo "Copiando ficheros de desarrollo a compartido..."
    sudo rsync -av ginn $DEST
    #read -p "Eliminado .git. Pulsa ENTER para empezar..." merdellOn
    echo "Eliminado .git..."
    find $DEST/ginn -name ".git" -type d -exec rm -rf '{}' \;
    rm $DEST/ginn/.gitignore
    #read -p "Pulsa ENTER para restaurar fichero de configuración..." mierda
    echo "Restaurando fichero de log y configuración..."
    cp -vf /tmp/ginn.conf $DEST/ginn/framework/
    cp -vf /tmp/ginn.log $DEST/ginn/formularios/
    #read -p "Asignando permisos. Pulsa ENTER para seguir..." merde
    echo "Asignando permisos..."
    sudo chown -R nobody:nogroup $DEST/ginn
    echo "Regenerando log..."
    cd ginn
    git log | grep -v "commit " | grep -v "Author:" | egrep -v "$^" | grep -v "Merge: " > $DEST/ginn/ChangeLog.git.txt
else
    echo "Este script debe ejecutarse en el servidor"
fi


