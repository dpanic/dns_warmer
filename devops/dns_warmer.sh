#!/bin/bash
SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
echo $SCRIPTPATH
cd $SCRIPTPATH


mkdir $SCRIPTPATH/../logs/
python3 -B ../dns_warmer.py > $SCRIPTPATH/../logs/dns_warmer.log 2>&1
 