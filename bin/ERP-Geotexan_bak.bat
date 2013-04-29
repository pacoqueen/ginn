REM @net use l: "\\Ginn\compartido\betav2" /user:nobody
REM @net use l: "\\192.168.1.100\compartido\betav2" /user:nobody

@net use l: "\\192.168.1.100\compartido\ginn"
@L:
@cd formularios
@%SYSTEMDRIVE%\Python27\python.exe menu.py -c ../framework/ginn.conf.dev|| %SYSTEMDRIVE%\Python26\python.exe menu.py -c ../framework/ginn.conf.dev || %SYSTEMDRIVE%\Python26\python.exe menu.py -c ../framework/ginn.conf.dev

echo Abriendo Geotex-INN (edición de ayer)...