#!/usr/bin/env bash

VERSION=$(python -V 2>&1 | cut -d\  -f 2) # python 2 prints version to stderr
VERSION=(${VERSION//./ })
if [[ ${VERSION[0]} -lt 3 ]] || [[ ${VERSION[0]} -eq 3 && ${VERSION[1] -lt 7} ]] ; then
    echo "Python 3.7+ needed!"
    return 1
fi

TOKEN="MyToken"
python ./runner.py

