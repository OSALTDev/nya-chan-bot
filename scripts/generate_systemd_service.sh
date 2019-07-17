#!/usr/bin/env bash

if [[ -z "$1" ]] ; then
    PYTHON_LAUNCHER=python
else
    PYTHON_LAUNCHER=$1
fi

VERSION=$(${PYTHON_LAUNCHER} -V 2>&1 | cut -d\  -f 2 | cut -d. -f 1,2) # python 2 prints version to stderr

if [[ ${VERSION} != '3.7' ]] ; then
    echo "Python 3.7+ needed!"
    exit 1
fi

C_DIR=`pwd`
cd `dirname "$(readlink -f $0)"`/..
cat > ${C_DIR}/nyachan.service <<- EOM
[Unit]
Description=Nya-Chan Discord bot service

[Service]
Type=simple
ExecStart=/bin/bash `pwd`/scripts/start.sh ${PYTHON_LAUNCHER}
ExecStop=/bin/bash `pwd`/scripts/stop.sh
User=
Group=

[Install]
WantedBy=multi-user.target
EOM

