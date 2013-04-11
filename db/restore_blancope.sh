#!/bin/sh

scp blancoperez@chaparobo.no-ip.com:dump_datos_bpinn.sql .
./init_db.py dump_datos_bpinn.sql ../framework/ginn.conf.bp

