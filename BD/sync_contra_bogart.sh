#!/bin/sh

HOST=chaparobo.no-ip.com
USER=autossh

echo -n "Buscando última copia de seguridad... "
ORIG=`ssh autossh@chaparobo.no-ip.com "ls *.dump -tr | tail -n 1"`
echo $ORIG

echo "Copiando base de datos..."
scp $USER@$HOST:$ORIG /tmp

echo "Restaurando base de datos en local..."
pg_restore -c -d ginn -U geotexan -h localhost /tmp/$ORIG

