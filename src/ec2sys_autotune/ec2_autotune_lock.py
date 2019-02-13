import os
import sys
import fcntl
import time
from syslog import syslog
from ec2sys_autotune.ec2_instance_exception \
    import Ec2AutotuneError


class Lock(object):
    '''

    This is a blocking lock implementation. However this will block
    and retry only MAX_TRIES for every SLEEP_TIME seconds before failing.
    '''
    def __init__(self, lock):
        SLEEP_TIME = 3
        MAX_TRIES = 10
        for count in range(0, MAX_TRIES):
            try:
                self.lock = open(lock, "r+")
                fcntl.lockf(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                syslog("Acquired lock")
                return
            except IOError, e:
                syslog("Retrying lock on error {0}".format(e.errno))
                self.lock.close()
                time.sleep(SLEEP_TIME)
                continue
        raise Ec2AutotuneError(
            "Couldn't acquire the lock during service startup.")

    def __del__(self):
        fcntl.lockf(self.lock, fcntl.LOCK_UN)
        self.lock.close()
        syslog("Released lock")
