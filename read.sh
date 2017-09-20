#!/bin/bash

while true ; do
	sleep 1
	data=$(curl http://145.239.194.85:8080 2>/dev/null)
	if [ "Z$data" != "Z" ]; then
		notify-send "$data"
		blink.sh &
	fi
done
