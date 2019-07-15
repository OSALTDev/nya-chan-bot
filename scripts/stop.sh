#!/usr/bin/env bash

C_DIR=`dirname "$(readlink -f $0)"`

read -r pid < ${C_DIR}/../.pid
kill -TERM ${pid}
