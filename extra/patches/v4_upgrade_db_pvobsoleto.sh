databases="dev_ginn ginn" # qinn bpinn crisva fbinn"
for db in $databases; do
    psql $db << EOF
ALTER TABLE producto_venta ADD COLUMN obsoleto BOOLEAN DEFAULT FALSE; 
CREATE INDEX pvobsoleto ON producto_venta (obsoleto);
UPDATE producto_venta SET obsoleto=FALSE;
GRANT ALL ON producto_venta TO geotexan;
EOF
done
echo "Ahora conéctate y comprueba desde pclases que tienes permisos sobre el campo, sino, toca hacer un GRANT en psql."

