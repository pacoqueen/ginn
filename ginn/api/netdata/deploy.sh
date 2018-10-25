#!/bin/sh

# Coloca cada fichero en su sitio. Se ejecuta desde `bacall`.

cp -f ginn.chart.py /usr/libexec/netdata/python.d/ginn.chart.py
cp -f ginn.conf /etc/netdata/orig/python.d/ginn.conf
cp -f ginn.local.conf /etc/netdata/python.d/ginn.conf
