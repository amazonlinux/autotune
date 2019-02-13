'''

There have been many instances of ARP cache table not being able to accommodate
entries which can make the applications fail mysteriously. Most of these issues
have been reported with dockers and containers workload. Following links
discuss this issue extensively:
https://github.com/hashicorp/serf/issues/263
https://github.com/moby/moby/issues/29992
https://github.com/docker/libnetwork/issues/1522
https://github.com/hashicorp/serf/issues/269
This config genertor helps in tuning kernel values to avoid above reported
problems.
'''

import os
import sys
from ec2sys_autotune.ec2_instance_cfg_gen import Ec2InstanceCfgGen


class UdpServerCfgGen(Ec2InstanceCfgGen):
    def tune(self):
        # Call super class as well to inherit base class network settings
        super(UdpServerCfgGen, self).start_cfg_logging()
        super(UdpServerCfgGen, self)._tune()
        self.set_sysctl_config("net.ipv4.neigh.default.gc_thresh1", 30000)
        self.set_sysctl_config("net.ipv4.neigh.default.gc_thresh2", 32000)
        self.set_sysctl_config("net.ipv4.neigh.default.gc_thresh3", 32768)
        self.set_sysctl_config("net.ipv6.neigh.default.gc_thresh1", 30000)
        self.set_sysctl_config("net.ipv6.neigh.default.gc_thresh2", 32000)
        self.set_sysctl_config("net.ipv6.neigh.default.gc_thresh3", 32768)
        super(UdpServerCfgGen, self).stop_cfg_logging()
        return
