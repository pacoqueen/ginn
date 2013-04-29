@REM @net use l: "\\Ginn\compartido\betav2" /user:nobody

@net use l: "\\192.168.1.100\compartido\ginn"
@L:
@cd formularios
@%SYSTEMDRIVE%\Python27\python.exe menu.py || %SYSTEMDRIVE%\Python26\python.exe menu.py || %SYSTEMDRIVE%\Python25\python.exe menu.py

echo Abriendo Geotex-INN...
