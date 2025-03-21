#!/bin/bash
NAME=reversessh
DESC="reversessh to server"
case "$1" in
  start)
    echo -n "Starting $DESC: "
    echo "$NAME."
    if [ ! -e /tmp/reverse_ssh.pid ]; then   # Check if the file already exists
        #ssh -f -N -T -R40000:localhost:22 root@125.209.200.159 -p 2222&
        ssh -N o2obox-ssh&
        echo $! > /tmp/reverse_ssh.pid
    else
        echo -n "ERROR: The process is already running with pid "
        cat /tmp/reverse_ssh.pid
    fi

    ;;
  stop)
    echo -n "Stopping $DESC: "
    if [ -f /tmp/reverse_ssh.pid ]; then   # If the file do not exists, then the
        kill `cat /tmp/reverse_ssh.pid`      #+the process is not running. Useless
        rm /tmp/reverse_ssh.pid              #+trying to kill it.
    else
        echo "reverse ssh is not running"
    fi
    ;;
  restart)
    $0 stop
    sleep 1
    $0 start
    ;;
  *)
    echo "Usage: $0 {start|stop|restart}" >&2
    exit 1
    ;;

esac

exit 0
