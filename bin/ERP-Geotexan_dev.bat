REM @net use l: "\\Ginn\compartido\betav2" /user:nobody
REM @net use l: "\\192.168.1.100\compartido\betav2" /user:nobody

@net use q: "\\192.168.1.102\compartido\ginn"
@Q:
@cd formularios
@%SYSTEMDRIVE%\Python25\python.exe menu.py || %SYSTEMDRIVE%\Python26\python.exe menu.py || %SYSTEMDRIVE%\Python27\python.exe menu.py

echo Abriendo Geotex-INN...
