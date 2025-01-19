import subprocess
from beep import *
from enum import Enum

LOW_BATTERY_WARNING = """NOTE: The server computer has lost power and is running on battery.
Your game server may shut down within 5 minutes. 
"""

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
    
def warn_minecraft():
    subprocess.run(["sudo", "./rcon_all", f"say ${LOW_BATTERY_WARNING}"])
    
def main():
    state = get_ups_state()
    print(state.name)

    state=State.BATTERY

    match state:
        case State.BATTERY:
            # beep(1000, 5)
            warn_minecraft()
        case State.CRITICAL:
            # beep(2000, 5)
            pass
        case State.ONLINE:
            pass
        case State.UNKNOWN:
            pass
        case _:
            pass

if __name__ == "__main__":
    main()