#!/usr/bin/env bash

LAST=''
while true
do
    read -r STATE </opt/uid/uid
    STATE="${STATE^^}"

    if [ "$STATE" == IDLE ]
    then
      [ "$LAST" == "$STATE" ] && continue
      ilo hp2 UID OFF
    elif [ "$STATE" == RUNNING ]
    then
      [ "$LAST" == "$STATE" ] && continue
      ilo hp2 UID ON
    elif [ "$STATE" == IN_USE ]
    then
      ilo hp2 UID OFF
      sleep 5
      ilo hp2 UID ON
    fi

    LAST="$STATE"

    sleep 5
done
