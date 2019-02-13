'''

EC2 instance HasA kernel.
This class needs to be a composition of base class.
'''

import os
import sys
from syslog import syslog
from ec2sys_autotune.ec2_autotune_utils import read_sysfs_file

# Exception
from ec2sys_autotune.ec2_instance_exception import Ec2AutotuneError


class CfgGenKernelSettings(object):
    '''

    Generate config for kernel settings
    '''
    def __init__(self, set_config, get_instance_data,
                 inst_class, add_secured_config):
        self.set_sysctl_config = set_config["sysctl"]
        self.set_sysfs_config = set_config["sysfs"]
        self.get_instance_data = get_instance_data
        self.add_secured_config = add_secured_config
        return

    def __del__(self):
        self.set_sysctl_config = None
        self.set_sysfs_config = None
        self.get_instance_data = None
        return

    def tune(self):
        '''

        ##### Kernel Settings #####
        '''

        # Controls whether core dumps will append the PID to the core filename.
        self.set_sysctl_config("kernel.core_uses_pid", 1)

        # Controls the default maxmimum size of a mesage queue
        # XXX: Future work, should this be based on memory size?
        self.set_sysctl_config("kernel.msgmnb", 1024 * 64)

        # Controls the maximum size of a message, in bytes
        # XXX: Future work, should this be based on memory size?
        self.set_sysctl_config("kernel.msgmax", 1024 * 64)

        # Controls the maximum shared segment size, in bytes
        # XXX: Future work, should this be based on memory size?
        self.set_sysctl_config("kernel.shmmax", 1024 * 1024 * 1024 * 64)

        # Controls the maximum number of shared memory segments, in pages
        # XXX: Future work, should this be based on memory size?
        self.set_sysctl_config("kernel.shmall", 1024 * 1024 * 1024 * 4)

        '''
        Set TSC as clock source for Xen based instances only except t2.*.
        '''
        try:
            instance_type = self.get_instance_data("Instance Type")
            if (instance_type.find("t2.", 0, 3) == -1):
                if (os.path.isfile("/sys/hypervisor/type") is True):
                    output = read_sysfs_file("/sys/hypervisor/type")
                    if (output == "xen"):
                        self.set_sysfs_config(
                            "/sys/devices/system/clocksource/clocksource0/"
                            "current_clocksource", "tsc")
        except Ec2AutotuneError, e:
            syslog(e.msg)

        if (self.add_secured_config is True):
            # Controls the System Request debugging functionality of the kernel
            self.set_sysctl_config("kernel.sysrq", 0)

            # Restrict access to kernel logs
            self.set_sysctl_config("kernel.dmesg_restrict", 1)

            # Restrict access to kernel pointers in proc filesystem
            self.set_sysctl_config("kernel.kptr_restrict", 1)

        return
