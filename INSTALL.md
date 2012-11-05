Instalación ginn
================

Servidor
--------

### Prerrequisitos ###

* Descargar [código fuente](https://github.com/pacoqueen/ginn "GitHub").
> No hay archivo empaquetado. Usar _git_ para clonar la rama `master`.

* Instalar *PostgreSQL* y *Samba*.

### Base de datos ###

0. Preparar conexión en pg_hba de PostgreSQL:
	
		host    ginn             uginn            0.0.0.0 0.0.0.0         md5

1. Crear usuario (`uginn`) y asignar contraseña (`pwginn`):

		createuser -d -R -S -P uginn

2. Crear base de datos y estructura de tablas:

		createdb -E UTF8 -O uginn -h localhost -U uginn -W ginn
		psql -U uginn -W -h localhost ginn < tablas.sql

3. Restaurar datos de ejemplo:

		pg_restore -c -d ginn populate.sql

> El usuario de la aplicación que viene en el [conjunto de datos de ejemplo][1] es `admin` con contraseña `admin`.

### Compartido SAMBA ###

0. Preparar fichero de configuración `ginn.conf`:

		tipobd  postgres                                                                
		user    uginn
		pass    pwginn
		dbname  ginn
		host    localhost
		modelo_presupuesto presupuesto2
		ventanas_sobre fc
		logo    logo_nuevo.png
		precision 2

1. Copiar código y compartir directorio padre en `/etc/samba/smb.conf` como `compartido`. Comprobar con `testparm`.



Clientes
--------

### Microsoft Windows ###

0. Instalar bibliotecas (últimas versiones testeadas):
> 00. `gtk2-runtime-2.22.0-2010-10-21-ash.exe` (**GTK+ 2**)
> 01. `gtk2-themes-2009-09-07-ash.exe` (**Temas GTK**. Opcional)
> 02. `python-2.7.1.msi` (**Python 2.7**)
> 03. `pygtk-all-in-one-2.24.0.win32-py2.7.msi` (**PyGTK**)
> 04. `reportlab-2.5.win32-py2.7.exe` (**ReportLab**)
> 05. `setuptools-0.6c11.win32-py2.7.exe` (**Setup Tools** de Python)
> 06. `psycopg2-2.2.2.win32-py2.7-pg9.0.1-release.exe` (**Psycopg**)
> 07. `Slik-Subversion-1.6.13-win32.msi` (**Subversion** para MS-Windows)
> 09. `egenix-mx-base-3.2.0.win32-py2.7.msi` (**mxDateTime**)
> 10. `PIL-1.1.7.win32-py2.7.exe` (**Python Imaging Library**)
> 11. `gs905w32.exe` (**GhostScript**)
> 08. __SQLObject__:  

				md "%APPDATA%\Subversion"
				REM --------8<-----------
				REM >>> Solo si proxy <<<
				REM echo [global] > "%APPDATA%\Subversion\servers"
				REM echo http-proxy-host=192.168.0.239 >> "%APPDATA%\Subversion\servers"
				REM echo http-proxy-port=8080 >> "%APPDATA%\Subversion\servers"
				REM -------->8-----------
				SET Path="%ProgramFiles%\SlikSvn\bin\";%Path%
				%SYSTEMDRIVE%\Python27\Scripts\easy_install.exe -U SQLObject

1. Copiar `utils/ERP-Geotexan.bat` y establecer icono `utils/logo.ico` al acceso directo. Recomendada opción _«Ejecutar: Minimizada»_ en _Propiedades_.

### GNU/Linux ###

0. Instalar bibliotecas.

1. Montar directorio compartido o, desde el propio servidor, entrar en `ginn/formularios`.

2. Ejecutar `menu.py`

---

[1]: https://github.com/pacoqueen/ginn/blob/master/BD/populate.sql

