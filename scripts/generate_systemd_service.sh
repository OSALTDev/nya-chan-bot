#!/usr/bin/env bash


VERSION=$(python -V 2>&1 | cut -d\  -f 2 | cut -d. -f 1,2) # python 2 prints version to stderr
if [[ ${VERSION} != '3.7' ]] ; then
    echo "Python 3.7+ needed!"
    exit 1
fi

C_DIR=`dirname "$(readlink -f $0)"`/..
PYTHON_EXECUTABLE=`python -c "import sys; print(sys.executable)"`
cat > nyachan.service <<- EOM
[Unit]
Description=Nya-Chan Discord bot service

[Service]
Type=simple
ExecStart=${PYTHON_EXECUTABLE} ${C_DIR}/runner.py
ExecStop=/bin/bash ${C_DIR}/script/stop.sh
User=
Group=

[Install]
WantedBy=multi-user.target
EOM

