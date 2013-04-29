#!/bin/sh

if [ $1 = "p" ]; then
	cp -f ginn.conf.portatil ginn.conf
	#cp -f nftp.conf.portatil nftp.conf
elif [ $1 = "g" ]; then
	cp -f ginn.conf.geotexan ginn.conf
	#cp -f nftp.conf.geotexan nftp.conf
elif [ $1 = "q" ]; then
    cp -f ginn.conf.qinnova ginn.conf
elif [ $1 = "d" ]; then
    cp -f ginn.conf.diego ginn.conf
elif [ $1 = "t" ]; then
    cp -f ginn.conf.tetsuo ginn.conf
elif [ $1 = "b" ]; then
    cp -f ginn.conf.blancoperez ginn.conf
elif [ $1 = "c" ]; then
    cp -f ginn.conf.crisva ginn.conf
elif [ $1 = "f" ]; then
    cp -f ginn.conf.fblanco ginn.conf
fi	
