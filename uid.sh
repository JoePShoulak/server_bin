#!/usr/bin/env bash

LAST=''
while true
do
    read -r _UID </opt/uid/uid
    UID="${_UID^^}"

    if [ "$UID" == IDLE ]
    then
      [ "$LAST" == "$UID" ] && continue
      ilo hp2 UID OFF
    elif [ "$UID" == RUNNING ]
    then
      [ "$LAST" == "$UID" ] && continue
      ilo hp2 UID ON
    elif [ "$UID" == IN_USE ]
    then
      ilo hp2 UID OFF
      sleep 5
      ilo hp2 UID ON
    fi

    LAST="$UID"

    sleep 5
done
