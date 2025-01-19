import subprocess

def beep(freq=1000, repeat=1, delay=100):
  subprocess.run(["beep", "-f", str(freq), "-r", str(repeat), "-d", str(delay)])
