#!/bin/bash

JOBFILE=""
HOSTIP=""
NUM=1
DATAFILES=""
FLOWBSTER_FEEDER="`dirname $0`/flowbster_feeder.py"

if [[ $# < 1 ]]; then
        echo "Usage: $0 -h [hostip] -i [inputfile] -c [count] -d [inputfile]"
        exit 1
fi

while [[ $# > 0 ]]
do
key="$1"

case $key in
    -c|--count)
    NUM="$2"
    shift # past argument
    ;;
    -h|--hostip)
    HOSTIP="$2"
    shift # past argument
    ;;
    -i|--inputfile)
    JOBFILE="$2"
    shift # past argument
    ;;
    -d|--datafile)
    DATAFILES="$2 $DATAFILES"
    shift # past argument
    ;;
    *)
    ;;
esac
shift # past argument or value
done
echo HOSTIP   : "$HOSTIP"
echo JOBFILE  : "$JOBFILE"
echo DATAFILES: "$DATAFILES"
if [ "$HOSTIP" == "" -o "$JOBFILE" == "" ]; then
    echo "ERROR: At least hostip and inputfile must be defined!"
    echo "Usage: $0 -h [hostip] -i [inputfile] -c [count]"
else
    for a in `seq $NUM`; do
        echo "Instance $a :"
        python $FLOWBSTER_FEEDER $JOBFILE http://$HOSTIP:5000/flowbster $DATAFILES;
    done
fi

