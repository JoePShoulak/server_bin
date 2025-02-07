import subprocess
from beep import *
from enum import Enum
from time import sleep

LOW_BATTERY_MESSAGE = "The server computer has lost power and is running on battery. Your game server may shut down within 30 seconds."
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

    if "OB" in status: # On Battery
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
            print("All containers stopped successfully.", flush=True)
        else:
            print("No running containers to stop.", flush=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}", flush=True)

def shutdown():
    print('Shutting down in 3 seconds', flush=True)
    sleep(3)
    try:
        subprocess.run(['sudo','shutdown', '-h', 'now'])
    except:
        print("Failed to shutdown. Shit's gonna fail the hard way.", flush=True)

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
        sleep(30)
        state = get_ups_state()

        if state == old_state:
            if state == State.BATTERY:
                # If we've had low battery for 2 iterations, shut down.
                # this way, a single blip doesn't kill everything.
                stop_all_containers()
                shutdown()
            continue

        print(state.name, flush=True)
        match state:
            case State.BATTERY:
                beep(2000, 5)
                announce_minecraft(LOW_BATTERY_MESSAGE, color="red")
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
