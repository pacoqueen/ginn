#!/bin/bash
# Script para hacer tunel ssh inverso
# Por David Martín :: Suki_ ::
# http://sukiweb.net
# http://sukiweb.net/archivos/2007/01/30/script-para-tunel-ssh-inverso/

USUARIO_TUNEL="remoto"
PUERTO_TUNEL="22222"

SERVIDOR_REMOTO="servidor.remoto.com"
PUERTO_SERVIDOR_REMOTO="22"

TEXTO="echo ' ADMINISTRACIÓN REMOTA';
echo 'Se va a proceder a la conexión remota de este equipo con el servidor:';
echo $SERVIDOR_REMOTO;
echo;
echo 'Mantenga esta ventana abierta mientras desee mantener la conexión.';
echo;
echo 'Teclee a continuación la clave del usuario $USUARIO_TUNEL.';
echo;
echo"

TUNEL="ssh -l $USUARIO_TUNEL -R $PUERTO_TUNEL:localhost:$PUERTO_SERVIDOR_REMOTO -N $SERVIDOR_REMOTO"

# Para que corra en segundo plano:
# TUNEL=”ssh -N -f -R $PUERTO_TUNEL:localhost:$PUERTO_SERVIDOR_REMOTO $USUARIO_TUNEL@$SERVIDOR_REMOTO”

xterm -title "Administración Remota" -e "$TEXTO;$TUNEL"

# En el server:
# ssh -p 22222 usuario_máquina_que_ejecuta_el_scrip@localhost

