#!/bin/bash

queue=${1:poezio}

while true ; do
    sleep 1
    data=$(curl -X GET -H "Content-Type: application/json" -H "X-Auth-Token: $(cat ~/.p_notif)" https://notifications.arnaudmorin.fr/queues-polling/${queue} 2>/dev/null)
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
