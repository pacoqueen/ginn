REM ==============
REM = Geotex-INN =
REM ==============
REM 
REM Sincronización productos Murano <-> Geotex-INN
REM 

ECHO OFF
set GINNDRIVE=L:
set GINNPATH=%GINNDRIVE%\ginn
set GINNEXE=%GINNPATH%\api\tests\sr_lobo.py
set GINNHOST=192.168.1.100 & REM bacall.geotexan.es
set GINNSHARE="\\%GINNHOST%\compartido\ginn"
ECHO ON 

@net use %GINNDRIVE% %GINNSHARE%
@%GINNDRIVE%
@cd %GINNPATH%
@set PYTHONPATH=%PYTHONPATH%;%GINNPATH%
@echo Sincronizando...
@%SYSTEMDRIVE%\Python27\python.exe %GINNEXE% -p
@%SYSTEMDRIVE%
