REM ==============
REM = Geotex-INN =
REM ==============
REM 
REM Lanzador DOS para versión contra última copia de seguridad de la base de 
REM datos.
REM 

ECHO OFF
GINNDRIVE=L:
GINNPATH=%GINNDRIVE%\ginn
GINNEXE=%GINNPATH%\main.py
GINNCONF=%GINNPATH%\framework\ginn.conf.dev
GINNHOST=192.168.1.100 	& REM bacall.geotexan.es
GINNSHARE="\\%GINNHOST%\compartido\ginn"
ECHO ON 

@net use %GINNDRIVE% %GINNSHARE%
@%GINNDRIVE%
@cd %GINNPATH%
@export PYTHONPATH=%PYTHONPATH%;%GINNPATH%
@%SYSTEMDRIVE%\Python27\python.exe %GINNEXE% -c %GINNCONF% 
	|| %SYSTEMDRIVE%\Python26\python.exe %GINNEXE% -c %GINNCONF%
	|| %SYSTEMDRIVE%\Python25\python.exe %GINNEXE% -c %GINNCONF%

echo Abriendo Geotex-INN (edición de ayer)...
