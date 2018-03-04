# vm-boot-order

libvirt has no facility for controlling the order that domains (virtual
machines) boot, nor delays between VMs. This creates thrashing during the
startup of a server with many domains.

This script solves the problem.

## Instructions

1. Ensure that your VMs can shutdown gracefully when the *power-button* is pressed.
2. Place the file `vm-boot-order.py` in `/usr/local/sbin` directory
3. Make it executable: `chmod +x /usr/local/sbin/vm-boot-order.py`
4. Check that the script starts and shuts down your VMs as expected. The script can be executed as follows:

        /usr/local/sbin/vm-boot-order.py start
        /usr/local/sbin/vm-boot-order.py stop
        /usr/local/sbin/vm-boot-order.py status

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

Source: https://gist.github.com/cyberang3l/f4c8b1ab6fc48374fbae9553d89e5eed
