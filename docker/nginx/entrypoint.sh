#!/bin/bash

set -ex

if [ $# -eq 0 ]
then
    echo "Staring nginx"
    exec /usr/sbin/nginx -g "daemon off;"
else
    exec $@
fi
