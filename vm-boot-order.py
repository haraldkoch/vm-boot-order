#!/usr/bin/env python

from __future__ import print_function
import libvirt
import sys
import time

vm_start_list = ['openmediavault', 'nextcloud'] # The list of VMs to start in the given order
vm_start_waiting_time_list = [90, 0] # A list of waiting times to wait after each VM reaches active
                                     # state, before starting the next VM from the vm_start_list

vm_stop_list = reversed(vm_start_list) # By default, the VMs are stopped in the reverse start order.
                                       # If you want a different order, add the VMs in the vm_stop_list
vm_force_stop_time = 240  # If the the VM shutdown command doesn't work or the VM got stuck,
                          # after 'vm_force_stop_time' seconds the VM will be 'destroyed'.

#----------------------------------------------------------------------
def start_vms(libvirt_conn):
    for i in range(len(vm_start_list)):
        vm_name = vm_start_list[i]
        wait_time = vm_start_waiting_time_list[i]
        try:
            vm = libvirt_conn.lookupByName(vm_name)
        except libvirt.libvirtError:
            # Error code 42 = Domain not found
            if (e.get_error_code() == 42):
                print(e)
                exit(1)
            else:
                raise(e)

        if vm.isActive():
            print("VM '{}' already started".format(vm_name))

        while not vm.isActive():
            print("Starting VM '{}'".format(vm_name))
            vm.create()
            time.sleep(1)
            if vm.isActive():
                try:
                    print("Waiting for {} seconds before trying to start the next VM '{}'".format(wait_time, vm_start_list[i + 1]))
                    time.sleep(wait_time)
                except IndexError:
                    break

    print("All VMs have been started.")


#----------------------------------------------------------------------
def stop_vms(libvirt_conn):
    for vm_name in vm_stop_list:
        try:
            vm = libvirt_conn.lookupByName(vm_name)
        except libvirt.libvirtError as e:
            # Error code 42 = Domain not found
            if (e.get_error_code() == 42):
                print(e)
                exit(1)
            else:
                raise(e)

        if vm.isActive():
            print("Stopping VM '{}'".format(vm_name))
        else:
            print("VM '{}' is already stopped".format(vm_name))

        seconds_waited = 0
        while vm.isActive():
            try:
                vm.shutdown()
                time.sleep(1)
                seconds_waited += 1
                if seconds_waited >= vm_force_stop_time:
                    print("Timeout was reached and VM '{}' hasn't stopped yet. Destroying...".format(vm_name), file = sys.stderr)
                    vm.destroy()
            except libvirt.libvirtError as e:
                # Error code 55 = Not valid operation: domain is not running
                if (e.get_error_code() == 55):
                    pass
                else:
                    raise(e)

    print("All VMs have been stopped.")


#----------------------------------------------------------------------
def vm_status(libvirt_conn):
    domNames = libvirt_conn.listDefinedDomains()

    domIDs = libvirt_conn.listDomainsID()

    if len(domIDs) != 0:
        for domID in domIDs:
            dom = libvirt_conn.lookupByID(domID)
            domNames.append('{} (Running)'.format(dom.name()))

    print("Status for all VMs (active and inactive domain names):")
    print("-----------------------------")
    if len(domNames) == 0:
        print('    None')
    else:
        for domName in domNames:
            print('    {}'.format(domName))
    print("-----------------------------")


if __name__ == '__main__':
    #connect to hypervisor running on localhost
    for c in range(1, 10):
        try:
            conn = libvirt.open('qemu:///system')
        except libvirt.libvirtError:
            time.sleep(2)

    if len(sys.argv) > 1:
        if sys.argv[1] == 'start':
            start_vms(conn)
        elif sys.argv[1] == 'stop':
            stop_vms(conn)
        elif sys.argv[1] == 'restart':
            stop_vms(conn)
            start_vms(conn)
        elif sys.argv[1] == 'status':
            vm_status(conn)
    elif len(sys.argv) == 1:
        start_vms(conn)

    conn.close()

exit(0)
