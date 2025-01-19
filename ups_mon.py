from os import system as sys
from time import sleep
import re

# while True:
#     sys("upsc apcups@localhost")
#     sleep(5)


# # Specify the file and the pattern
# file_path = "example.txt"
# pattern = r"hello"

# # Open the file and search for the pattern
# with open(file_path, "r") as file:
#     for line in file:
#         if re.search(pattern, line):
#             print(line.strip())




import subprocess

command = ["upsc", "apcups@localhost"]
pattern = "ups.status"

# Run and filter the output
result = subprocess.run(command, capture_output=True, text=True)
lines = [line for line in result.stdout.splitlines() if pattern in line]

for line in lines:
    print(line)
