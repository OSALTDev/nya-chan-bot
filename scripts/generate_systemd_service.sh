#!/usr/bin/env bash

#!/bin/bash

C_DIR=`dirname "$(readlink -f $0)"`
cat > nyachan.service <<- EOM
        [Unit]
        Description=Nya-Chan Discord bot service

        [Service]
        Type=simple
        ExecStart=/bin/bash ${C_DIR}/start.sh
        ExecStop=/bin/bash ${C_DIR}/stop.sh

        [Install]
        WantedBy=multi-user.target
EOM
