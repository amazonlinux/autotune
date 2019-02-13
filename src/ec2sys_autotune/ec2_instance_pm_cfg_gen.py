'''

EC2 instance HasA CPU.
This class needs to be a composition of base class.
'''
import os
import sys
from syslog import syslog
from ec2sys_autotune.ec2_autotune_utils import get_piped_cmd_output

# Exception
from ec2sys_autotune.ec2_instance_exception import Ec2AutotuneError


class CfgGenPowerManagementSettings(object):
    '''

    Generate config for power management settings
    '''
    def __init__(self, set_config, get_instance_data,
                 inst_class, add_secured_config):
        self.set_sysfs_config = set_config["sysfs"]
        self.set_cpupower_config = set_config["cpu"]
        self.get_instance_data = get_instance_data
        return

    def __del__(self):
        self.set_sysfs_config = None
        self.set_cpupower_config = None
        self.get_instance_data = None
        return

    def tune(self):
        '''
        ##### Power Management #####
        CPU Power (P-state)
        '''
        try:
            # Set if only intel_pstate driver
            driver = get_piped_cmd_output(
                         "/bin/cpupower frequency-info --driver",
                         "/bin/grep \"driver: intel_pstate\"")
            if(len(driver) > 0):
                self.set_cpupower_config("p-state", "performance")
                # Intel Turbo Boost
                if (self.get_instance_data("Intel Turbo") == "True"):
                    self.set_sysfs_config(
                           "/sys/devices/system/cpu/intel_pstate/no_turbo",
                           0)
        except Ec2AutotuneError, e:
            syslog(e.msg)

        # CPU Sleep (C-state)
        try:
            # Set if only intel_idle driver
            driver = get_piped_cmd_output(
                         "/bin/cpupower idle-info --silent",
                         "/bin/grep \"driver: intel_idle\"")
            if(len(driver) > 0):
                self.set_cpupower_config("c-state", "C1E")
        except Ec2AutotuneError, e:
            syslog(e.msg)

        return
