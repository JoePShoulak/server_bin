import subprocess
from beep import *
from enum import Enum
from time import sleep

LOW_BATTERY_MESSAGE = "The server computer has lost power and is running on battery. Your game server may shut down within 5 minutes."
SHUTDOWN_MESSAGE = "The server will shut down in 10 seconds."
ONLINE_MESSAGE = "Power has been restored to the server. Crisis averted! :)"

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
    
def announce_minecraft(message, color="red"):
    colors = {
        'black': '§0',
        'darkblue': '§1',
        'green': '§2',
        'teal': '§3',
        'darkred': '§4',
        'purple': '§5',
        'gold': '§6',
        'silver': '§7',
        'gray': '§8',
        'blue': '§9',
        'lime': '§a',
        'aqua': '§b',
        'red': '§c',
        'violet': '§d',
        'yellow': '§e',
    }

    if colors.get(color):
        message = colors.get(color) + message

    subprocess.run(["sudo", "./rcon_all", f"say {message}"])

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

def happy_beep():
    beep()
    sleep(0.1)
    beep(2000)
    sleep(0.1)
    beep()
    sleep(0.1)
    beep(2000)
    sleep(0.1)

def main():
    old_state = State.UNKNOWN

    while True:
        sleep(1)
        state = get_ups_state()
        print(state.name)

        if state == old_state:
            continue

        match state:
            case State.BATTERY:
                beep(1000, 5)
                announce_minecraft(LOW_BATTERY_MESSAGE, color="red")
            case State.CRITICAL:
                beep(2000, 5)
                announce_minecraft(SHUTDOWN_MESSAGE, color="red")
                sleep(10)
                stop_all_containers()
            case State.ONLINE:
                if old_state == State.UNKNOWN: continue
                
                happy_beep()
                announce_minecraft(ONLINE_MESSAGE, color="green")
            case State.UNKNOWN:
                pass
            case _:
                pass

        old_state = state

if __name__ == "__main__":
    main()
