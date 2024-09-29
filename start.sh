#!/bin/bash

cd "$(dirname "$0")"

export NOTIFICATION_HOST=${NOTIFICATION_HOST-0.0.0.0}
export NOTIFICATION_PORT=${NOTIFICATION_PORT-8082}
export NOTIFICATION_PASSWORD=${NOTIFICATION_PASSWORD-changeme}

poetry run notification-queue
