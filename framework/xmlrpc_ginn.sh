#! /bin/sh
#
# parse_mdblogic initscript
#
# Author:	Francisco José Rodríguez Bogado <rodriguez.bogado@gmail.com>
#
#

set -e

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DESC="servidor XML-RPC ginn..."
NAME=parse_mdblogic
DAEMON="/home/compartido/betav2/framework/launch_server.py"
#DAEMON="/home/geotexan/launch_server.py"
PIDFILE=/var/run/$NAME.pid
SCRIPTNAME=/etc/init.d/$NAME

# Gracefully exit if the package has been removed.
test -x $DAEMON || exit 0

# Read config file if it is present.
#if [ -r /etc/default/$NAME ]
#then
#	. /etc/default/$NAME
#fi

#
#	Function that starts the daemon/service.
#
d_start() {
	start-stop-daemon --start --quiet --pidfile $PIDFILE \
		--exec $DAEMON
}

#
#	Function that stops the daemon/service.
#
d_stop() {
#	start-stop-daemon --stop --quiet --signal 9 --pidfile $PIDFILE \
#		--name $NAME
#	start-stop-daemon --stop --signal 9 -p /var/run/skeletonz.pid 
	start-stop-daemon --stop --signal 9 -p $PIDFILE 
}

#
#	Function that sends a SIGHUP to the daemon/service.
#
d_reload() {
	start-stop-daemon --stop --quiet --pidfile $PIDFILE \
		--name $NAME --signal 1
}

case "$1" in
  start)
	echo -n "Starting $DESC: $NAME"
	d_start
	echo "."
	;;
  stop)
	echo -n "Stopping $DESC: $NAME"
	d_stop
	echo "."
	;;
  #reload)
	#
	#	If the daemon can reload its configuration without
	#	restarting (for example, when it is sent a SIGHUP),
	#	then implement that here.
	#
	#	If the daemon responds to changes in its config file
	#	directly anyway, make this an "exit 0".
	#
	# echo -n "Reloading $DESC configuration..."
	# d_reload
	# echo "done."
  #;;
  restart|force-reload)
	#
	#	If the "reload" option is implemented, move the "force-reload"
	#	option to the "reload" entry above. If not, "force-reload" is
	#	just the same as "restart".
	#
	echo -n "Restarting $DESC: $NAME"
	d_stop
	sleep 1
	d_start
	echo "."
	;;
  *)
	# echo "Usage: $SCRIPTNAME {start|stop|restart|reload|force-reload}" >&2
	echo "Usage: $SCRIPTNAME {start|stop|restart|force-reload}" >&2
	exit 1
	;;
esac

exit 0
