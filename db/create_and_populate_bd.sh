#/bin/sh

# Sólo funciona para Posgtgre y para la base de datos local (por no especificar host en los comandos de postgre; el script python sí se adapta al archivo de configuración). Como siempre... de momento.

# USO: Hacer copia de seguridad sólo de datos (porque la estructura no se puede reconstruir
# después a causa de las funciones PL/SQL).
# Por ejemplo: pg_dump ginn -a -f datos_01_02_06.sql
# Para restaurar la copia (tal como se hace aquí), primero crear las tablas y después
# insertar los datos de la copia de seguridad.
# Por ejemplo: 
# psql ginn < tablas.sql
# psql ginn < datos_01_02_06.sql
# IMPORTANTE: Cuando se metan campos nuevos y tablas nuevas, poner DEFAULTs siempre que
# sea posible para evitar que no se inserten las tuplas de la copia al faltar datos.

dropdb ginn;
#createdb ginn --encoding UNICODE &&
createdb ginn -O geotexan --encoding UNICODE &&
psql -U geotexan ginn < tablas.sql 2>&1 | grep -v NOTICE&&
#echo "SELECT pg_catalog.setval('producto_venta_id_seq', 69, true);" | psql ginn 
#./stock_inicial.py
#psql ginn < ginn.empleados.19_01_06.sql 
#psql ginn < para_instalar_solo_datos.sql
    # Ya tiene clientes, proveedores y pedidos.
#psql ginn < ginn.clientes.19_01_06.sql &&
#psql ginn < ginn.proveedores.19_01_06.sql &&
#psql ginn < dump_datos_01_02_06.sql
psql -U geotexan ginn < dump_datos.sql

