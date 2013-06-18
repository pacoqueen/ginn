REM ==============
REM = Geotex-INN =
REM ==============
REM 
REM Lanzador DOS para versión contra última copia de seguridad de la base de 
REM datos.
REM 

ECHO OFF
set GINNDRIVE=L:
set GINNPATH=%GINNDRIVE%\ginn
set GINNEXE=%GINNPATH%\main.py
set GINNCONF=%GINNPATH%\framework\ginn.conf.dev
set GINNHOST=192.168.1.100 	& REM bacall.geotexan.es
set GINNSHARE="\\%GINNHOST%\compartido\ginn"
ECHO ON 

@net use %GINNDRIVE% %GINNSHARE%
@%GINNDRIVE%
@cd %GINNPATH%
@set PYTHONPATH=%PYTHONPATH%;%GINNPATH%
@echo Abriendo Geotex-INN (edición de ayer)...
@%SYSTEMDRIVE%\Python27\python.exe %GINNEXE% -c %GINNCONF% || %SYSTEMDRIVE%\Python26\python.exe %GINNEXE% -c %GINNCONF%	|| %SYSTEMDRIVE%\Python25\python.exe %GINNEXE% -c %GINNCONF%
@%SYSTEMDRIVE%
