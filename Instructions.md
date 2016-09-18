1. Ensure that your VMs can shutdown gracefully when the *power-button* is pressed.
2. Place the file `vm-boot-order.py` in `/opt` directory
3. Make it executable: `chmod +x /opt/vm-boot-order.py`
4. Check that the script starts and shuts down your VMs as expected. The script can be executed as follows:

        /opt/vm-boot-order.py start
        /opt/vm-boot-order.py stop
        /opt/vm-boot-order.py status

4. Make a systemd service to execute the script when booting or shutting down the hypervisor:

  For RHEL/CentOS:
  * Place the file `vm-boot-order.service` in `/etc/systemd/system/`
  * Apply the correct permissions `chmod 644 /etc/systemd/system/vm-boot-order.service`
  * Reload systemd services and enable the newly added service:

            systemctl daemon-reload
            systemctl enable vm-boot-order.service

  * Start/Restart the service

            systemctl start vm-boot-order.service
            systemctl status vm-boot-order.service
            systemctl stop vm-boot-order.service
            systemctl status vm-boot-order.service