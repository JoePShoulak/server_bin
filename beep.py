import subprocess
from time import sleep

def beep(freq=1000, repeat=1, delay=100):
  subprocess.run(["beep", "-f", str(freq), "-r", str(repeat), "-d", str(delay)])

if __name__ == "__main__":
  print("ran")
  beep(1000, 5)
  sleep(1)
  beep(2000, 5)
