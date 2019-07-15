#!/usr/bin/env bash

read -r pid < ../.pid
kill -SIGTERM ${pid}
