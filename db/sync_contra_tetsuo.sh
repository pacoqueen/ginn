#!/bin/sh

#scp autossh@tetsuo:dump_datos.sql.tar.bz2 .
scp autossh@chaparobo.no-ip.com:dump_datos.sql.tar.bz2 . || scp autossh@tetsuo:dump_datos.sql.tar.bz2 .
./init_db.py dump_datos.sql.tar.bz2 ../framework/ginn.conf

