'''

EC2 instance HasA storage.
This class needs to be a composition of base class.
'''
import os
import sys
from syslog import syslog
from ec2sys_autotune.ec2_autotune_utils import exec_cmds
from ec2sys_autotune.ec2_autotune_utils import get_cmd_output
from ec2sys_autotune.ec2_autotune_utils import get_piped_cmd_output

# Exception
from ec2sys_autotune.ec2_instance_exception import Ec2AutotuneError


class CfgGenStorageSettings(object):
    '''
    Generate config for storage settings
    '''
    def __init__(self, set_config, get_instance_data,
                 inst_class, add_secured_config):
        self.set_sysfs_config = set_config["sysfs"]
        return

    def __del__(self):
        self.set_sysfs_config = None
        return

    def tune(self):
        '''
        ##### I/O scheduler #####
        Set I/O scheduler on following criteria:
        Ephermeral store HDD - deadline
        Instance store NVME - kyber
        Default is noop for EBS backed HDD and none for EBS backed NVME.

        Also set max_retries for NVME devices to 10 (default is 5)
        '''
        try:
            output = get_piped_cmd_output("/bin/ec2-metadata -b",
                                          "/bin/grep ephemeral")
            for hdd_link in output.split():
                if ("ephemeral" in hdd_link):
                    continue
                hdd_device = get_cmd_output("/bin/readlink /dev/{0}"
                                            .format(hdd_link))
                self.set_sysfs_config(
                    "/sys/block/{0}/queue/scheduler".format(hdd_device),
                    "deadline")
        except Ec2AutotuneError, e:
            syslog(e.msg)

        try:
            nvme_present = False
            output = get_piped_cmd_output(
                         "/bin/lsblk -l -d --output NAME,TRAN",
                         "/bin/grep -e nvme")
            for nvme_device in output.split():
                if ("nvme" == nvme_device):
                    continue
                nvme_present = True
                try:
                    exec_cmds(["/sbin/ebsnvme-id /dev/{0}"
                               .format(nvme_device)])
                except Ec2AutotuneError, e:
                    # Instance store NVME
                    self.set_sysfs_config(
                        "/sys/block/{0}/queue/scheduler".format(nvme_device),
                        "kyber")
            if (nvme_present):
                    self.set_sysfs_config(
                         "/sys/module/nvme_core/parameters/max_retries",
                         10)
        except Ec2AutotuneError, e:
            syslog(e.msg)

        return
