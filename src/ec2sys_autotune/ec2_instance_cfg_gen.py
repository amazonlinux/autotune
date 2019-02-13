'''

EC2 Amazon Linux Kernel Autotuning config generator for base instance role.

Amazon Web Services EC2 fleet hosts a wide selection of instance types
optimized to fit different customer use cases. Instance types are carved
out for varying combinations of CPU, Memory, Storage and Networking capacity
to allow customers to pick the correct instance type for their workload.

Amazon Linux Kernel provides a stable, secure and high performance execution
environment for customer applications running on Amazon EC2. Default values
for kernel tunables is not the best and optimized value for all instance
types on EC2. To provide best customer experience for Amazon Linux Kernel
consumers on EC2, this script generates kernel tunable for different
instance types. This config generator is workload agnostic and the configs
generated are for base instance role.

Workload specific tunable config generator needs to inherit this base
class and then generate tunable configs.
'''

import os
import sys
import stat
import json
import math
import requests
from syslog import syslog
try:
    from configparser import RawConfigParser
except ImportError:
    # Backward compatibility with python versions earlier to 3.0
    from ConfigParser import RawConfigParser
from ec2sys_autotune.ec2_autotune_utils import get_cmd_output
from ec2sys_autotune.ec2_instance_types import general_purpose
from ec2sys_autotune.ec2_instance_types import compute_optimized
from ec2sys_autotune.ec2_instance_types import memory_optimized
from ec2sys_autotune.ec2_instance_types import accelerated_computing
from ec2sys_autotune.ec2_instance_types import storage_optimized
from ec2sys_autotune.ec2_instance_types import ec2_instance_types

# Composition classes
from ec2sys_autotune.ec2_instance_services_cfg_gen \
    import CfgGenPerfOptimizingServices
from ec2sys_autotune.ec2_instance_vm_cfg_gen \
    import CfgGenVirtualMemorySettings
from ec2sys_autotune.ec2_instance_network_cfg_gen \
    import CfgGenNetworkSettings
from ec2sys_autotune.ec2_instance_kernel_cfg_gen import CfgGenKernelSettings
from ec2sys_autotune.ec2_instance_storage_cfg_gen \
    import CfgGenStorageSettings
from ec2sys_autotune.ec2_instance_pm_cfg_gen \
    import CfgGenPowerManagementSettings

# Exceptions
from ec2sys_autotune.ec2_instance_exception import Ec2AutotuneError
from ec2sys_autotune.ec2_instance_exception import Ec2AutotuneEexists


# Config file message intended for end user
COMMENT = "# Do not modify this auto-generated config file,  instead " \
    "customize tuning in user.ini as per your requirements."
PROFILE = "profile"
NAME = "name"
INSTANCE = "instance"
VERSION = "version"
# Bump this number for every new release
RELEASE = "1.0.0"

# Types of tunables being tuned by autotune
SERVICE = "service"
SYSCTL = "sysctl"
SYSFS = "sysfs"
CPU = "cpu"

# EC2 instance classes
GENERAL_PURPOSE = "general_purpose"
COMPUTE_OPTIMIZED = "compute_optimized"
MEMORY_OPTIMIZED = "memory_optimized"
ACCELERATED_COMPUTING = "accelerated_computing"
STORAGE_OPTIMIZED = "storage_optimized"


class Ec2InstanceCfgGen(object):
    '''

    Common base class config generator for all EC2 instances
    with no role (no workload specific tuning).
    '''

    def __init__(self, config_dir, profile):
        '''

        Need to instantiate by passing in config file and profile name
        '''
        # In-memory config object to generate system settings
        self.cfg_object = None

        self.profile = None
        self.auto_profile = "{0}/{1}.ini".format(config_dir, profile)

        # Query the instance type and instance class
        try:
            self.inst_type = self.get_instance_type()
            self.inst_class = self.get_instance_class()
        except Ec2AutotuneError, e:
            raise e

        # Existing config file is for same profile, skip generation
        if (os.path.isfile(self.auto_profile) is True):
            cfg_file = RawConfigParser(allow_no_value=True)
            cfg_file.read(self.auto_profile)
            if (cfg_file.has_section(PROFILE) and
                    # Check for profile name to match with generated profile
                    cfg_file.has_option(PROFILE, NAME) and
                    cfg_file.get(PROFILE, NAME) == profile and
                    # Check current instance to match with generated profile
                    cfg_file.has_option(PROFILE, INSTANCE) and
                    cfg_file.get(PROFILE, INSTANCE) ==
                    self.get_instance_data("Instance Type") and
                    # Check version to match with generated profiles version
                    cfg_file.has_option(PROFILE, VERSION) and
                    cfg_file.get(PROFILE, VERSION) == RELEASE):
                raise Ec2AutotuneEexists(
                    "Configuration file {0} already "
                    "exists.".format(self.auto_profile))

        self.profile = profile

        return

    def start_cfg_logging(self):
        '''

        Start logging tunables for generating configuration file
        '''
        self.cfg_object = RawConfigParser(allow_no_value=True)

        # Header section
        self.cfg_object.add_section(PROFILE)
        self.cfg_object.set(PROFILE, COMMENT)
        self.cfg_object.set(PROFILE, NAME, self.profile)
        self.cfg_object.set(PROFILE, INSTANCE,
                            self.get_instance_data("Instance Type"))
        self.cfg_object.set(PROFILE, VERSION, RELEASE)

        # List of services
        self.cfg_object.add_section(SERVICE)

        # List of sysctl tunables
        self.cfg_object.add_section(SYSCTL)

        # List of sysfs tunables
        self.cfg_object.add_section(SYSFS)

        # List of CPU tunables
        self.cfg_object.add_section(CPU)
        return

    def stop_cfg_logging(self):
        '''

        Stop and commit all configuration
        '''
        if (self.cfg_object is None):
            return

        cfg_file = open(self.auto_profile, "wb")
        self.cfg_object.write(cfg_file)
        cfg_file.close()
        # Set appropriate permission on config file
        os.chmod(self.auto_profile, 0744)
        self.cfg_object = None
        return

    def get_instance_data(self, name):
        '''

        Return instance data for a particular property
        '''
        try:
            index = self.inst_type[0].index(name)
            return self.inst_type[1][index]
        except ValueError:
            raise Ec2AutotuneError(
                "Error retrieving {0} from local EC2 "
                "instance metadata.".format(name))

    def get_instance_class(self):
        '''

        Return the instance class for which this instance belongs
        '''
        for instance_class in ec2_instance_types:
            if (self.inst_type[1] in instance_class):
                if (instance_class == general_purpose):
                    return GENERAL_PURPOSE
                elif (instance_class == compute_optimized):
                    return COMPUTE_OPTIMIZED
                elif (instance_class == memory_optimized):
                    return MEMORY_OPTIMIZED
                elif (instance_class == accelerated_computing):
                    return ACCELERATED_COMPUTING
                elif (instance_class == storage_optimized):
                    return STORAGE_OPTIMIZED
        raise Ec2AutotuneError("Error identifying instance class.")

    def get_instance_type(self):
        '''

        Query EC2 Metadata server and identify instance type
        '''
        try:
            output = get_cmd_output("/bin/ec2-metadata -t")
            output = output.split(":")[1]
            output = output.strip()
        except Ec2AutotuneError, e:
            raise e

        for instance_class in ec2_instance_types:
            for instance_type in instance_class[1:]:
                if (output == instance_type[0]):
                    return (instance_class[0], instance_type)
        raise Ec2AutotuneError(
            "{0} is not a supported instance type for "
            "autotune.".format(output))

    def write_config_entry(self, section, name, value):
        '''

        Worker function to check for stacking entries & to write
        config in memory
        '''
        assert (self.cfg_object is not None)
        if (section is None or name is None or value is None):
            return

        assert (self.cfg_object.has_section(section))
        if (self.cfg_object.has_option(section, name)):
            syslog("Stacking entry for {0}.".format(name))
            self.cfg_object.remove_option(section, name)
        if (isinstance(value, list) is False):
            value = [value]
        self.cfg_object.set(section, name, value)
        return

    def set_service_config(self, service, state):
        '''

        Set the passed in service state in config
        '''
        return self.write_config_entry(SERVICE, service, state)

    def set_sysctl_config(self, sysctl_setting, value):
        '''

        Set the passed in sysctl kernel value in config
        '''
        return self.write_config_entry(SYSCTL, sysctl_setting, value)

    def set_sysfs_config(self, sysfs_file, value):
        '''

        Set the passed in sysfs value in config
        '''
        return self.write_config_entry(SYSFS, sysfs_file, value)

    def set_cpupower_config(self, state, value):
        '''

        Set the passed in CPU power state's value in config
        '''
        return self.write_config_entry(CPU, state, value)

    def setup_objects_composition(self):
        self.set_config = {"service": self.set_service_config,
                           "sysctl": self.set_sysctl_config,
                           "sysfs": self.set_sysfs_config,
                           "cpu": self.set_cpupower_config}
        self.composition_classes = ["CfgGenPerfOptimizingServices",
                                    "CfgGenVirtualMemorySettings",
                                    "CfgGenNetworkSettings",
                                    "CfgGenKernelSettings",
                                    "CfgGenStorageSettings",
                                    "CfgGenPowerManagementSettings"]
        self.composition_objects = []

        if ("-secured" in self.profile):
            add_secured_config = True
        else:
            add_secured_config = False
        for cl in self.composition_classes:
            ns = globals()[cl]
            self.composition_objects.append(
                ns(self.set_config,
                   self.get_instance_data,
                   self.inst_class,
                   add_secured_config))
        return

    def teardown_objects_composition(self):
        for obj in self.composition_objects:
            del obj
            obj = None
        self.composition_objects = None
        self.composition_classes = None
        self.set_config = None
        return

    def _tune(self):
        self.setup_objects_composition()
        for obj in self.composition_objects:
            obj.tune()
        self.teardown_objects_composition()
        return

    def tune(self):
        self.start_cfg_logging()
        self._tune()
        self.stop_cfg_logging()
        return
