#!/bin/bash

GATHER_BIN="`dirname $0`/flowbster_gather.py"
PIDFILE="flowbster-gather.pid"
LOGFILE="flowbster-gather.log"

if [[ $# < 1 ]]; then
		echo "Usage: $0 [-s|--start] [-d|--destroy]"
        exit 1
fi

while [[ $# > 0 ]]
do 
key="$1"

case $key in
    -d|--destroy)
    shift
    if [ -e $PIDFILE ]; then
        pid=`cat $PIDFILE`
        if [ -e /proc/$pid -a /proc/$pid/exe ]; then
            kill $pid
            sleep 1
            rm -f $PIDFILE
        fi
    fi
    ;;
    -s|--start)
    shift
    if [ -e $PIDFILE ]; then
        pid=`cat $PIDFILE`
        if [ -e /proc/$pid -a /proc/$pid/exe ]; then
            kill $pid
            sleep 1
            rm -f $PIDFILE
        fi
    fi
    python $GATHER_BIN &
    echo $! > $PIDFILE
    touch $LOGFILE
    tail -f $LOGFILE
    ;;
    *)
    echo "WARNING: unknown argument: $key"
    shift
    ;;
esac
done

exit 0
 
