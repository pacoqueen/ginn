@REM ==== Another one pseudoinstaller ====
@REM 01/12/2010
@REM http://unattended.sourceforge.net/installers.php
@REM Echar un vistazo también a: http://www.autoitscript.com/autoit3/index.shtml
"00 gtk2-runtime-2.22.0-2010-10-21-ash.exe" /S /translations=yes /compatdlls=yes
"01 gtk2-themes-2009-09-07-ash.exe" /S
msiexec /qb /i "02 python-2.7.1.msi" 
msiexec /i "03 pygtk-all-in-one-2.24.0.win32-py2.7.msi"
REM "04 pygobject-2.26.0.win32-py2.7.exe"
REM "05 pycairo-1.8.10.win32-py2.7.exe"
"04 reportlab-2.5.win32-py2.7.exe"
"05 setuptools-0.6c11.win32-py2.7.exe"
"06 psycopg2-2.2.2.win32-py2.7-pg9.0.1-release.exe"
REM msiexec /qb /i "09 Slik-Subversion-1.6.13-win32.msi"
msiexec /qb /i "09 egenix-mx-base-3.2.0.win32-py2.7.msi"
"10 PIL-1.1.7.win32-py2.7.exe"
"11 gs905w32.exe"
"08 sqlobject.bat"
"12 pychart.bat"
cd pyserial-2.6
C:\Python27\python.exe setup.py install
