#!/usr/bin/env bash

# Check if argument is passed, and set PYTHON_LAUNCHER var to the argument passed
# If not passed, just use "python"
if [[ -z "$1" ]] ; then
    PYTHON_LAUNCHER=python
else
    PYTHON_LAUNCHER=$1
fi

# Get python launcher (cut by spaces, get second result, then cut by "b" (beta), and get first result)
VERSION=$(${PYTHON_LAUNCHER} -V 2>&1 | cut -d\  -f 2 | cut -db -f 1) # python 2 prints version to stderr

# Compare version with periods replaced by nothing, to 370 (python 3.7.0 +)
# If lower than, display message for error, and
if [[ "${VERSION//./}" -lt '370' ]] ; then
    echo "Python 3.7+ needed!"
    exit 1
fi

# Change into parent dir of script
C_DIR=`pwd`
cd `dirname "$(readlink -f $0)"`/..

# Cat our script into nyachan.service
cat <<- EOM > ${C_DIR}/nyachan.service
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

