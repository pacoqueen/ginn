#!/bin/bash

# Coloca cada fichero en su sitio. Se ejecuta desde `bacall`.
if [[ $EUID -ne 0 ]]; then
   echo "Este _script_ debe ejecutarse como root: sudo "$0 1>&2
   echo "E incluso..."
   echo "> $ letsgo; cd -; sudo netdata/deploy.sh; sudo service netdata restart; echo -e \"\e[92mDONE\!\""
   exit 1
fi
BASEPATH=$(dirname $(realpath $0))

cp -f $BASEPATH/ginn.chart.py /usr/libexec/netdata/python.d/ginn.chart.py
cp -f $BASEPATH/ginn.conf /etc/netdata/orig/python.d/ginn.conf
cp -f $BASEPATH/ginn.local.conf /etc/netdata/python.d/ginn.conf
chown root:netdata /usr/libexec/netdata/python.d/ginn.chart.py
chown root:netdata /etc/netdata/orig/python.d/ginn.conf
chown root:netdata /etc/netdata/python.d/ginn.conf

echo -e "\e[92mMódulo copiado"
