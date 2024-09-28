#!/bin/bash

cd "$(dirname "$0")"

export NOTIFICATION_HOST=${1-0.0.0.0}
export NOTIFICATION_PORT=${2-8082}
export NOTIFICATION_PASSWORD=${3-changeme}

poetry run notification-queue
