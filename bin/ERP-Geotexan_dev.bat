REM ==============
REM = Geotex-INN =
REM ==============
REM 
REM Lanzador DOS para versión de desarrollo contra base de datos independiente.
REM 

ECHO OFF
set GINNDRIVE=Q:
set GINNPATH=%GINNDRIVE%\ginn
set GINNEXE=%GINNPATH%\main.py
set GINNCONF=""
set GINNHOST=192.168.1.102 	& REM pennyworth.geotexan.es
set GINNSHARE="\\%GINNHOST%\compartido\ginn"	& REM /user:nobody
ECHO ON 

@net use %GINNDRIVE% %GINNSHARE%
@%GINNDRIVE%
@cd %GINNPATH%
@set PYTHONPATH=%PYTHONPATH%;%GINNPATH%
@%SYSTEMDRIVE%\Python27\python.exe %GINNEXE% -c %GINNCONF% || %SYSTEMDRIVE%\Python26\python.exe %GINNEXE% -c %GINNCONF% || %SYSTEMDRIVE%\Python25\python.exe %GINNEXE% -c %GINNCONF%

echo Abriendo Geotex-INN (version de desarrollo)...
