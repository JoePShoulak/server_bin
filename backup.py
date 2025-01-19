import argparse
import subprocess
import os
import shutil
import re
from pathlib import Path

# Determines if the target is reachable
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


# Function to perform the rsync operation
def backup_folder(source_path, target_user, target_ip):
    destination_path = f"{target_user}@{target_ip}:{source_path}"
    rsync_command = [
        "rsync",
        "-av",  # Archive mode, verbose output
        "--delete",  # Delete files on destination not in source
        source_path,
        destination_path,
    ]

    print(f"Backing up the server folder '{source_path}' to {target_user}@{target_ip}...")

    try:
        # Execute the rsync command
        result = subprocess.run(
            rsync_command,
            stderr=subprocess.PIPE,  # Capture error output
            text=True,  # Ensure output is returned as strings
        )

        # Check the return code
        if result.returncode != 0:
            # Handle specific error codes
            if result.returncode == 255:
                print(
                    f"Error: Unable to connect to {target_user}@{target_ip}. Ensure the machine is online and accessible."
                )
            else:
                print(
                    f"Error: Rsync failed with code {result.returncode}. Check /tmp/rsync_error.log for details."
                )
                # Write the error log for debugging
                with open("/tmp/rsync_error.log", "w") as error_log:
                    error_log.write(result.stderr)
            exit(result.returncode)

        print(f"Backup of folder '{source_path}' completed successfully!")

    except Exception as e:
        print(f"Unexpected error during rsync: {e}")
        exit(1)


# Set up the parser
parser = argparse.ArgumentParser()
parser.add_argument("container")
parser.add_argument("-d", "--destination", default="hp2")
args = parser.parse_args()

# Get the target from the hostname
target_user = "joe"
target_ip = ""
match args.destination:
    case "hp1":
        target_ip = "10.0.20.11"
    case "hp2":
        target_ip = "10.0.20.12"
    case "hp3":
        target_ip = "10.0.20.13"
    case "hp4":
        target_ip = "10.0.20.14"
    case _:
        print(f"Invalid destination: {args.destination}")
        exit()

# Check if the directories exist
if not os.path.isdir(f"/home/joe/minecraft/{args.container}") or not os.path.isdir(
    f"/opt/minecraft/{args.container}"
):
    print("No such container present on machine.")
    exit()

# Check if the target machine is reachable
if not is_machine_reachable(target_ip):
    print(f"Target ({target_user}@{target_ip}) is not reachable.")
    exit()

# Perform the backup
backup_folder(f"/opt/minecraft/{args.container}", target_user, target_ip)

compose_file = Path(f"/home/joe/minecraft/{args.container}/compose.yml")
backup_file = compose_file.with_suffix(compose_file.suffix + ".bak")
shutil.copy(compose_file, backup_file)

with compose_file.open("r") as f:
  content = f.read()

  # Replace \d+:25565 with 30001:25565
  updated_content = re.sub(r"\d+:25565", f"3100{args.destination[-1]}:25565", content)

  # Write the updated content back to the original compose_file
  with compose_file.open("w") as f:
    f.write(updated_content)
  print(f"Updated '{compose_file}' with the new port configuration.")

backup_folder(f"/home/joe/minecraft/{args.container}", target_user, target_ip)
