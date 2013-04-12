@echo 
@echo The Subversion client can go through a proxy, if you configure it to do so. First, edit your "servers" configuration file to indicate which proxy to use. The files location depends on your operating system. On Linux or Unix it is located in the directory "~/.subversion". On Windows it is in "\%APPDATA\%\Subversion". (Try "echo %APPDATA%", note this is a hidden directory.)
@echo There are comments in the file explaining what to do. If you don't have that file, get the latest Subversion client and run any command; this will cause the configuration directory and template files to be created.
@echo Example : Edit the 'servers' file and add something like :
@echo [global]
@echo http-proxy-host = your.proxy.name
@echo http-proxy-port = 3128
md "%APPDATA%\Subversion"
echo [global] > "%APPDATA%\Subversion\servers"
echo http-proxy-host=192.168.0.239 >> "%APPDATA%\Subversion\servers"
echo http-proxy-port=8080 >> "%APPDATA%\Subversion\servers"
SET Path="%ProgramFiles%\SlikSvn\bin\";%Path%
%SYSTEMDRIVE%\Python27\Scripts\easy_install.exe -U SQLObject
REM pause

