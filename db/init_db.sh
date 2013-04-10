#!/bin/bash
 
function setup_pgpass {
    if [ -z `ls ~/.pgpass 2>/dev/null` ]; then 
        touch ~/.pgpass
        chmod 600 ~/.pgpass
    fi
    if [ -z "$(grep $1 ~/.pgpass | grep $2 | grep $3)" ]; then
        cat >> ~/.pgpass << EOF
*:*:$1:$2:$3
EOF
    else
        echo -n Usando ... 
        egrep --color "$1.*$2.*$3" ~/.pgpass
    fi
}

if [ $# -gt 2 ]; then
    setup_pgpass $1 $2 $3
    dropdb $1;
    createdb $1 -O $2 --encoding UNICODE &&
    psql -U $2 $1 < tablas.sql 2>&1 | grep -v NOTICE &&
    if [ $# -eq 4 ]; then
        echo "Reordenando datos..."
        ./reorder_dump.py tablas.sql $4 > "$4.reordered"
        echo "Restaurando datos..."
        psql -U $2 $1 < "$4.reordered" | egrep -v "[0-9]+" | egrep -v "([0-9]+ fila)" | grep -v setval | grep -v -- "-\{8\}" | grep '^[^#]' &&
        echo "ANALYZE;" | psql -U $2 $1     # Para mejorar el rendimiento de la BD recién restaurada.
    fi
else
    echo "Debe indicar el nombre de la base de datos, usuario, contraseña y fichero sql de la copia de seguridad (opcional). Por ese orden."
fi

