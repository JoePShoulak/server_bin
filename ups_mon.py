import subprocess

def query_ups():
    return subprocess.run(["upsc", "apcups@localhost"], capture_output=True, text=True)

def get_ups_state():
    pass

lines = [line for line in query_ups().stdout.splitlines() if "ups.status" in line]

for line in lines:
    print(line)

subprocess.run(["beep", "-f", "1000", "-r", "5", "-d", "100"])
