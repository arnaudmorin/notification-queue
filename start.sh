#!/bin/bash

export NOTIFICATION_HOST=${1-127.0.0.1}
export NOTIFICATION_PORT=${2-8082}

if [ "$3" = "source" ] ; then
    source /opt/notification-queue/venv/bin/activate
fi

./run.py
