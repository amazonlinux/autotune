import os
import sys
from syslog import syslog
from ec2sys_autotune.ec2_instance_cfg_engine import Ec2InstanceCfgEngine
try:
    from configparser import RawConfigParser
except ImportError:
    # Backward compatibility with python versions earlier to 3.0
    from ConfigParser import RawConfigParser
from ec2sys_autotune.ec2_autotune_lock import Lock

# Exception
from ec2sys_autotune.ec2_instance_exception import Ec2AutotuneError


class Ec2AutotuneStop(object):
    '''

    Restore system to earlier default state
    '''

    def __init__(self, config="/etc/ec2sys-autotune.cfg"):
        self.config = config
        self.cfg_file = RawConfigParser(allow_no_value=True)
        self.cfg_file.read(self.config)
        return

    def stop(self):
        # Disallow multiple instances of the same service
        try:
            lock_obj = Lock(self.config)
        except Ec2AutotuneError, e:
            raise (e)

        # State directory - mandatory option in config file to stop service
        if (self.cfg_file.has_option("DEFAULT", "STATE_DIR") is False):
            raise Ec2AutotuneError("Missing STATE_DIR in config file.")
        STATE_DIR = self.cfg_file.get("DEFAULT", "STATE_DIR")

        # Log file - mandatory option in config file to stop service
        if (self.cfg_file.has_option("DEFAULT", "LOG_FILE") is False):
            raise Ec2AutotuneError("Missing LOG_FILE in config file.")
        LOG_FILE = self.cfg_file.get("DEFAULT", "LOG_FILE")

        # Status file - mandatory option in config file to stop service
        if (self.cfg_file.has_option("DEFAULT", "STATUS") is False):
            raise Ec2AutotuneError("Missing STATUS in config file.")
        STATUS = self.cfg_file.get("DEFAULT", "STATUS")
        if (os.path.isfile(STATUS) is False):
            raise Ec2AutotuneError("Autotune is not active")

        try:
            instance = None
            # Restore the system settings to earlier state
            instance = Ec2InstanceCfgEngine("{0}/{1}".format(STATE_DIR,
                                                             LOG_FILE))
            instance.restore_system_settings()

            # Clear the service status
            os.remove(STATUS)

            syslog("EC2 AWS Autotune has restored original system settings "
                   "after clean up.")
        except Ec2AutotuneError, e:
            raise (e)

        return
