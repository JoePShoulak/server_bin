To add a new service:
1. copy systemd.service.template to `/etc/systemd/system/my_service_name.service`
2. tell systemd to scan for services, `sudo systemctl daemon-reload`
3. let the service run on boot `sudo systemctl enable my_service_name`
4. start the service `sudo systemctl start my_service_name` (or you can reboot if you want)

service template:
[Unit]
Description=Monitors the UPS and managers system power as well as docker containers depending on power state
; After=some_other.service

[Service]
WorkingDirectory=/home/joe/bin
ExecStart=python3 ups_mon.py
Restart=on-failure
User=joe
Group=joe
KillSignal=SIGINT

[Install]
WantedBy=default.target