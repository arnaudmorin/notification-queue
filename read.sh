#!/bin/bash

while true ; do
    sleep 1
    data=$(curl http://notifications.arnaudmorin.fr:8080/$(cat ~/.p_notif) 2>/dev/null)
    if [ "Z$data" != "Z" ]; then
        notify-send "$data"
        blink.sh &
        curl -X  POST -d to=33618671034 -d message="salut" -d token="$(cat ~/.p_sms)" http://192.168.100.3:5000/send
    fi
done
