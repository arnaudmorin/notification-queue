#!/bin/bash

queue=${1-poezio}
server=${2-https://notifications.arnaudmorin.fr}

while true ; do
    sleep 1
    data=$(curl -X GET -H "Content-Type: application/json" -H "X-Auth-Token: $(cat ~/.p_notif)" ${server}/queues-polling/${queue} 2>/dev/null)
    date=$(date -R)
    if [ "Z$data" != "Z" ]; then
        # If it's a link to open
        if [[ $data =~ ^xdg-open.* ]]; then
            link=$(echo $data | awk '{print $2}')
            echo "$date Link: $link"
            eval "xdg-open '$link'"
        else
            echo "$date Message: $data"
            if [[ $data =~ ^Meeting.* ]]; then
                URGENCY='critical'
            elif [[ $data =~ ^!.* ]]; then
                URGENCY='critical'
                data="${data:1}"
            else
                URGENCY='normal'
            fi
            notify-send -u $URGENCY "$data"
            blink.sh &
            # blink_guirlande.sh &
            #curl -X  POST -d to=33618671034 -d message="$data" -d token="$(cat ~/.p_sms)" http://192.168.100.3:5000/send
        fi
    fi
done
