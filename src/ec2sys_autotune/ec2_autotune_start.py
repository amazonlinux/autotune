import os
import sys
import fcntl
from syslog import syslog
from ec2sys_autotune.ec2_instance_cfg_gen import Ec2InstanceCfgGen
from ec2sys_autotune.udp_server_cfg_gen import UdpServerCfgGen
from ec2sys_autotune.placement_group_cfg_gen import PlacementGroupCfgGen
from ec2sys_autotune.ec2_instance_cfg_engine import Ec2InstanceCfgEngine
try:
    from configparser import RawConfigParser
except ImportError:
    # Backward compatibility with python versions earlier to 3.0
    from ConfigParser import RawConfigParser
from ec2sys_autotune.ec2_autotune_lock import Lock

# Exceptions
from ec2sys_autotune.ec2_instance_exception import Ec2AutotuneError
from ec2sys_autotune.ec2_instance_exception import Ec2AutotuneEexists


class Ec2AutotuneStart(object):
    '''

    Generate config file for a particular profile
    '''

    def __init__(self, config="/etc/ec2sys-autotune.cfg",
                 genconfigonly=False):
        self.config = config
        self.genconfigonly = genconfigonly
        self.cfg_file = RawConfigParser(allow_no_value=True)
        self.cfg_file.read(self.config)

        # Read in the config directory location
        if (self.cfg_file.has_option("DEFAULT", "CONFIG_DIR") is False):
            raise Ec2AutotuneError("Missing CONFIG_DIR in config file.")
        self.config_dir = self.cfg_file.get("DEFAULT", "CONFIG_DIR")

        # Read in the user config file
        if (self.cfg_file.has_option("DEFAULT", "USER_CONFIG") is False):
            raise Ec2AutotuneError("Missing USER_CONFIG in config file.")
        self.user_config = self.cfg_file.get("DEFAULT", "USER_CONFIG")
        self.usercfg_log = RawConfigParser(allow_no_value=True)
        self.usercfg_log.read("{0}/{1}".format(self.config_dir,
                                               self.user_config))

        return

    def start(self):
        '''

        Start Autotune service
        '''
        # Disallow multiple instances of the same service
        try:
            lock_obj = Lock(self.config)
        except Ec2AutotuneError, e:
            raise (e)

        # Profile to tune the system with
        if (self.usercfg_log.has_option("profile", "PROFILE") is False):
            raise Ec2AutotuneError("Missing PROFILE in user config file.")
        PROFILE = self.usercfg_log.get("profile", "PROFILE")

        # State dir
        if (self.cfg_file.has_option("DEFAULT", "STATE_DIR") is False):
            raise Ec2AutotuneError("Missing STATE_DIR in config file.")
        STATE_DIR = self.cfg_file.get("DEFAULT", "STATE_DIR")

        # Log file
        if (self.cfg_file.has_option("DEFAULT", "LOG_FILE") is False):
            raise Ec2AutotuneError("Missing LOG_FILE in config file.")
        LOG_FILE = self.cfg_file.get("DEFAULT", "LOG_FILE")

        # Status file
        if (self.cfg_file.has_option("DEFAULT", "STATUS") is False):
            raise Ec2AutotuneError("Missing STATUS in config file.")
        STATUS = self.cfg_file.get("DEFAULT", "STATUS")
        if (os.path.isfile(STATUS) is True and self.genconfigonly is False):
            raise Ec2AutotuneError("Autotune profile {0} is already active"
                                   .format(PROFILE))

        try:
            instance = None
            # Instantiate appropriate object for the profile
            if ("base" in PROFILE):
                instance = Ec2InstanceCfgGen(self.config_dir, PROFILE)
            elif ("udp-server" in PROFILE):
                instance = UdpServerCfgGen(self.config_dir, PROFILE)
            elif ("placement-group" in PROFILE):
                instance = PlacementGroupCfgGen(self.config_dir, PROFILE)
            else:
                raise Ec2AutotuneError("Invalid role {0} specified."
                                       .format(PROFILE))

            # Generate config tunables for sub systems
            instance.tune()

            syslog("Configuration {0} role has been generated."
                   .format(PROFILE))
        except Ec2AutotuneEexists, e:
            # Config file exists from previous instance, reuse the same
            syslog(e.msg)
        except Ec2AutotuneError, e:
            # Fatal error, config file could not be generated
            raise (e)

        # If the request was to generate config only, return now
        if (self.genconfigonly is True):
            return

        # Configure system with generated config file
        try:
            instance = None
            instance = Ec2InstanceCfgEngine("{0}/{1}".format(STATE_DIR,
                                                             LOG_FILE),
                                            self.config_dir,
                                            PROFILE,
                                            "{0}/{1}".format(self.config_dir,
                                                             self.user_config))
            # Core function of configuration engine
            instance.configure_system_settings()

            # Mark the service as started
            with open(STATUS, "w") as status_file:
                pass

            syslog("System has now been configured with EC2 "
                   "AWS Autotune {0} profile.".format(PROFILE))
        except Ec2AutotuneError, e:
            raise (e)

        return
