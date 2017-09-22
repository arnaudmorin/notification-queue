#!/bin/bash

while true ; do
	sleep 1
    data=$(curl http://notifications.arnaudmorin.fr:8080/$(cat ~/.p_notif) 2>/dev/null)
	if [ "Z$data" != "Z" ]; then
		notify-send "$data"
		blink.sh &
	fi
done
