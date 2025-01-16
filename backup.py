import argparse
import subprocess
import os

def is_machine_reachable(host, timeout=2):
  try:
    # Ping the host
    subprocess.run(
      ["ping", "-c", "1", "-W", str(timeout), host],
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      check=True,
    )
    return True
  except subprocess.CalledProcessError:
    return False
    

parser = argparse.ArgumentParser()
parser.add_argument("container")
parser.add_argument( "-d", "--destination",default="hp2")
args = parser.parse_args()

target = ""
match args.destination:
  case "hp1":
    target = "joe@10.0.0.211"
  case "hp2":
    target = "joe@10.0.0.181"
  case "hp3":
    target = "joe@10.0.0.151"
  case "hp2":
    target = "joe@10.0.0.48"
  case _:
    print(f"Invalid destination: {args.destination}")
    exit()

print(args.container)
print(args.destination)

os.system("ls /home/joe/minecraft")
print(f"~/minecraft/{args.container}")
if not os.path.isdir(f"/home/joe/minecraft/{args.container}"):
  print("No such container present on machine")
  exit()

if not is_machine_reachable(target):
  print(f"Target ({target}) is not reachable.")
  exit()

