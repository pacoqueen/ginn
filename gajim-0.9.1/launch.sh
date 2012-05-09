#!/bin/sh

# XXX Modificador por queen
export LC_MESSAGES=es_ES
# XXX

cd `dirname $0`/src
exec python -OOt gajim.py $@

