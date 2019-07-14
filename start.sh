#!/usr/bin/env bash

VERSION=$(python -V 2>&1 | cut -d\  -f 2 | cut -d. -f 1,2) # python 2 prints version to stderr
if [ $VERSION != '3.7' ] ; then
    echo "Python 3.7+ needed!"
else
    export TOKEN="MyToken"
    python ./runner.py
fi
