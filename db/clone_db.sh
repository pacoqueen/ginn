#!/bin/bash

if [ $# -eq 0 ]; then
    echo "./clone_db.sh ginn ginn_bak"
else
    echo "CREATE DATABASE $2 WITH TEMPLATE $1 OWNER qinn;" | psql template1 
fi

