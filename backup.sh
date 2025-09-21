#!/usr/bin/env bash

is_machine_reachable() {
    ping -c 1 -W 2 "$1" &>/dev/null
    return $?
}

backup_folder() {
    rsync -av --delete "$1" "$2@$3:$1" 2>/tmp/rsync_error.log
    local status=$?

    if [ $status -ne 0 ]; then
        echo "Failed to backup $1 to $2@$3:$1"
        if [ $status -eq 255 ]; then
            echo "Failed to connect to $3. Ensure the machine is online and accessible."            
        else
            echo "ERROR: Rsync failed with status $status. Check /tmp/rsync_error.log for details."
        fi
        return $status
    fi

    echo "Successfully backed up $1 to $2@$3:$1"
    return 0
}

# Read arguments
CONTAINER="$1"
DESTINATION="${2:-hp2}"

[ -z "$CONTAINER" ] && echo "Usage: $0 <container> [destination]" && exit 1

TARGET_USER=joe
TARGET_IP=''

# Determine the target IP based on the destination
case "$DESTINATION" in
    hp1) TARGET_IP="10.0.20.11" ;;
    hp2) TARGET_IP="10.0.20.12" ;;
    hp3) TARGET_IP="10.0.20.13" ;;
    hp4) TARGET_IP="10.0.20.14" ;;
    *) echo "Invalid destination '$DESTINATION'. Valid options are hp1, hp2, hp3, hp4."; exit 1 ;;
esac

# Make sure the container exists on the machine
if [ ! -d "/home/joe/minecraft/$CONTAINER" ] || [ ! -d "/opt/minecraft/$CONTAINER" ]; then
    echo "ERROR: No such container present on machine."
    exit 1
fi

# Backup the container first. If this fails, script will exit
backup_folder "/opt/minecraft/$CONTAINER" "$TARGET_USER" "$TARGET_IP" || exit $?

# Backup the compose file, edit it, sync it up and then revert the edit
dir="/home/joe/minecraft/$CONTAINER"
cp "$dir/docker-compose.yml" "/tmp/docker-compose.yml"
sed -iE "s/[0-9]+:25565/3100${DESTINATION: -1}:25565/" "$file" # -i flag is for in-place editing
backup_folder "$dir" "$TARGET_USER" "$TARGET_IP"
local rtnval=$?
mv "/tmp/docker-compose.yml" "$dir/docker-compose.yml"

exit $rtnval