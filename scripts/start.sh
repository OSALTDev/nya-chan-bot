#!/usr/bin/env bash

if [[ -z "$1" ]] ; then
    PYTHON_LAUNCHER=python
else
    PYTHON_LAUNCHER=$1
fi

VERSION=$(${PYTHON_LAUNCHER} -V 2>&1 | cut -d\  -f 2 | cut -d. -f 1,2) # python 2 prints version to stderr
if [[ ${VERSION} != '3.7' ]] ; then
    echo "Python 3.7+ needed!"
else
    C_DIR=`dirname "$(readlink -f $0)"`
    cd ${C_DIR}/..
    source ./.env
    ${PYTHON_LAUNCHER} ./runner.py
fi
