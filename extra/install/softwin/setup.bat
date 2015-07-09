@REM ==== Another one pseudoinstaller v2 ====
@REM 9/07/2013

@echo Descomprimiendo Gtk...
@mkdir %SYSTEMDRIVE%\gtk
@FBZip.exe -e -p gtk+-bundle_2.24.10-20120208_win32.zip %SYSTEMDRIVE%\gtk

@echo Estableciendo variables de entorno...
@echo OFF
set KEY_NAME="HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
set VALUE_NAME=Path
FOR /F "usebackq skip=4 tokens=1-3" %%A IN (`REG QUERY %KEY_NAME% /v %VALUE_NAME% 2^>nul`) DO (
  set ValueName=%%A
  set ValueValue=%%C
)
if defined ValueName (
  set newPath=%ValueValue%;%SYSTEMDRIVE%\gtk\bin;%SYSTEMDRIVE%\Python27
  reg.exe ADD "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PathBAK /t REG_EXPAND_SZ /d %ValueValue% /f
  reg.exe ADD "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path /t REG_EXPAND_SZ /d %newPath% /f
  set path=%path%;%SYSTEMDRIVE%\gtk\bin;%SYSTEMDRIVE%\Python27
) else (
    @echo %KEY_NAME%\%VALUE_NAME% not found.
)
@echo ON

@echo Comprobando instalación de Gtk...
pkg-config --cflags gtk+-2.0

@REM Comentar si no se quiere hacer el test de Gtk.
@REM gtk-demo

@echo Instalando Python...
@msiexec /qb /i "python-2.7.10.msi"
@msiexec /i "VCForPython27.msi" ALLUSERS=1
@echo Instalando bibliotecas...
@REM Me aseguro de que pip está en el path, aunque solo sea para la sesión actual.
msiexec /i "pygtk-all-in-one-2.24.2.win32-py2.7.msi"
set PATH=%PATH%;C:\Python27\Scripts
@pip install --upgrade pip
@pip install pycairo
@pip install reportlab
@REM @pip install git+https://github.com/nwcell/psycopg2-windows.git@win32-py27#egg=psycopg2
@psycopg2-2.6.1.win32-py2.7-pg9.4.4-release.exe
@pip install egenix-mx-base
@pip install Pillow
@pip install sqlobject
@pip install pyserial
@pip install pychart

@echo Instalando Ghostscript...
@gs916w32.exe

@echo The end
