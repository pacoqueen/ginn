#!/bin/sh

pg_dump -Fc -f /tmp/full_ginn.pgdump ginn
cd /tmp 
tar cvjf /tmp/full_ginn.pgdump.tar.bz2 full_ginn.pgdump

