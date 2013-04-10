#!/bin/sh
dropdb -h localhost -WU blancope bpinn
createdb -h localhost -WU blancope bpinn --encoding UNICODE
psql -h localhost -WU blancope bpinn < tablas.sql 2>&1 | grep -v NOTICE 
psql -h localhost -WU blancope bpinn < dump_datos_bpinn.sql 2>&1 | grep -v NOTICE
#createdb -U blancope bpinn
#psql -U blancope bpinn < tablas.sql 2>&1 | grep -v NOTICE 
#psql -U blancope bpinn < dump_datos_bpinn.sql 2>&1 | grep -v NOTICE
 
