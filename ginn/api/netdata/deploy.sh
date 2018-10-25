#!/bin/bash

# Coloca cada fichero en su sitio. Se ejecuta desde `bacall`.
if [[ $EUID -ne 0 ]]; then
   echo "Este _script_ debe ejecutarse como root: sudo "$0 1>&2
   exit 1
fi

cp -f ginn.chart.py /usr/libexec/netdata/python.d/ginn.chart.py
cp -f ginn.conf /etc/netdata/orig/python.d/ginn.conf
cp -f ginn.local.conf /etc/netdata/python.d/ginn.conf
