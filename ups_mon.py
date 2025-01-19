import subprocess
from beep import *
from enum import Enum
from time import sleep

LOW_BATTERY_WARNING = "The server computer has lost power and is running on battery. Your game server may shut down within 5 minutes."
SHUTDOWN_WARNING = "The server will shut down in 10 seconds."

class State(Enum):
    ONLINE = 2
    BATTERY = 1
    CRITICAL = 0
    UNKNOWN = -1

def query_ups():
    return subprocess.run(["upsc", "apcups@localhost"], capture_output=True, text=True)

def get_ups_state():
    status_line = [line for line in query_ups().stdout.splitlines() if "ups.status" in line][0]
    status = status_line.split(": ")[-1].split(" ")

    if "LB" in status and "OB" in status: # Low Battery and On Battery
        return State.CRITICAL
    elif "OB" in status: # On Battery (but not critical)
        return State.BATTERY
    elif "OL" in status: # OnLine
        return State.ONLINE
    else:
        return State.UNKNOWN
    
def warn_minecraft(message):
    subprocess.run(["sudo", "./rcon_all", f"say §c{message}"])

def stop_all_containers():
    try:
        # Get the list of running container IDs
        container_ids = subprocess.check_output(
            ["sudo", "docker", "ps", "-q"], text=True
        ).strip()

        if container_ids:
            # Stop all running containers
            subprocess.run(["sudo", "docker", "stop"] + container_ids.split(), check=True)
            print("All containers stopped successfully.")
        else:
            print("No running containers to stop.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    
def main():
    old_state = State.UNKNOWN

    while True:
        sleep(1)
        state = get_ups_state()
        state = State.CRITICAL
        print(state.name)

        if state == old_state:
            continue

        match state:
            case State.BATTERY:
                beep(1000, 5)
                warn_minecraft(LOW_BATTERY_WARNING)
            case State.CRITICAL:
                beep(2000, 5)
                warn_minecraft(SHUTDOWN_WARNING)
                sleep(10)
                stop_all_containers()
            case State.ONLINE:
                pass
            case State.UNKNOWN:
                pass
            case _:
                pass

        old_state = state

if __name__ == "__main__":
    main()
