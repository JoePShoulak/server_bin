import subprocess

def query_ups():
    return subprocess.run(["upsc", "apcups@localhost"], capture_output=True, text=True)

def get_ups_state():
    status_line = [line for line in query_ups().stdout.splitlines() if "ups.status" in line][0]
    print(status_line)


# subprocess.run(["beep", "-f", "1000", "-r", "5", "-d", "100"])
get_ups_state()
