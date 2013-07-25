REM ==============
REM = Geotex-INN =
REM ==============
REM 
REM Lanzador DOS para versión estable contra base de datos en producción.
REM 

ECHO OFF
set GINNDRIVE=L:
set GINNPATH=%GINNDRIVE%\ginn
set GINNEXE=%GINNPATH%\main.py
set GINNCONF=%GINNPATH%\framework\ginn.conf
set GINNHOST=192.168.1.100& REM bacall.geotexan.es
set GINNSHARE="\\%GINNHOST%\compartido\ginn"
ECHO ON 

@net use %GINNDRIVE% %GINNSHARE%
@%GINNDRIVE%
@cd %GINNPATH%
@set PYTHONPATH=%PYTHONPATH%;%GINNPATH%
@echo Abriendo Geotex-INN...
@%SYSTEMDRIVE%\Python27\python.exe %GINNEXE% -c %GINNCONF% || %SYSTEMDRIVE%\Python26\python.exe %GINNEXE% -c %GINNCONF%	|| %SYSTEMDRIVE%\Python25\python.exe %GINNEXE% -c %GINNCONF%
@%SYSTEMDRIVE%
