To add a new service:
1. copy systemd.service.template to `/etc/systemd/system/my_service_name.service`
2. tell systemd to scan for services, `sudo systemctl daemon-reload`
3. let the service run on boot `sudo systemctl enable my_service_name`
4. start the service `sudo systemctl start my_service_name` (or you can reboot if you want)
