'''

EC2 instance HasA memory.
This class needs to be a composition of base class.
'''

import os
import sys
from syslog import syslog

# Exception
from ec2sys_autotune.ec2_instance_exception import Ec2AutotuneError

# EC2 instance classes
MEMORY_OPTIMIZED = "memory_optimized"


class CfgGenVirtualMemorySettings(object):
    '''

    Generate config for virtual memory settings
    '''
    def __init__(self, set_config, get_instance_data,
                 inst_class, add_secured_config):
        self.set_sysctl_config = set_config["sysctl"]
        self.get_instance_data = get_instance_data
        self.inst_class = inst_class
        return

    def __del__(self):
        self.set_sysctl_config = None
        self.get_instance_data = None
        self.inst_class = None
        return

    def tune(self):
        '''

        ##### VM Settings #####
        '''

        '''
        vm.swappiness
        This control is used to define how aggressive the kernel will swap
        memory pages. get_scan_count() skips scanning if there are is no
        swap space setup. However we do not want swappiness to interfere
        with hibernation swap space. Most of the databases want to
        manage their own pages and lock them in memory and do not want
        interference from swap management.
        '''
        self.set_sysctl_config("vm.swappiness", 0)

        try:
            if (self.get_instance_data("EBS OPT") == "Yes" and
                    self.get_instance_data("Mem (GiB)") > 28):
                '''
                vm.dirty_expire_centisecs
                Controls time dirty data can be in cache before it needs
                to be written
                '''
                self.set_sysctl_config("vm.dirty_expire_centisecs", 500)

                '''
                vm.dirty_writeback_centisecs
                Controls how often the flusher need to be woken up
                '''
                self.set_sysctl_config("vm.dirty_writeback_centisecs", 100)

                '''
                vm.dirty_background_ratio
                Contains, as a percentage of total available memory that
                contains free pages and reclaimable pages, the number of
                pages at which the background kernel flusher threads will
                start writing out dirty data.
                '''
                self.set_sysctl_config("vm.dirty_background_ratio", 0)
                self.set_sysctl_config("vm.dirty_background_bytes",
                                       1024 * 1024 * 1750 / 2)

                '''
                vm.dirty_ratio
                Contains, as a percentage of total available memory that
                contains free pages and reclaimable pages, the number of
                pages at which a process which is generating disk writes
                will itself start writing out dirty data.
                '''
                self.set_sysctl_config("vm.dirty_ratio", 0)
                self.set_sysctl_config("vm.dirty_bytes",
                                       1024 * 1024 * 1750 * 3)

        except Ec2AutotuneError, e:
            syslog(e.msg)
            syslog("Couldn't configure write back tunables of dirty pages")

        '''
        ##### Transparent Huge Pages (THP) #####
        Performance critical computing applications dealing with large memory
        working sets are already running on top of libhugetlbfs and in turn
        hugetlbfs. Transparent Hugepage Support is an alternative means of
        using huge pages for the backing of virtual memory with huge pages
        that supports the automatic promotion and demotion of page sizes and
        without the shortcomings of hugetlbfs.

        Most of the databases manage their own memory allocation using mmap
        interface. Though huge pages provide the opportunity of fewer TLB
        entries and fewer TLB misses, the case of internal page fragmentation
        and hugepage daemon trying to defragment these pages can result in
        delay of allocation of page. This delay is not acceptable to database
        workload where lot of threads are trying to allocate and free memory.
        '''
        if (self.inst_class == MEMORY_OPTIMIZED):
            self.set_sysfs_config(
                "/sys/kernel/mm/transparent_hugepage/enabled", "never")
            self.set_sysfs_config(
                "/sys/kernel/mm/transparent_hugepage/defrag", "never")
        return
