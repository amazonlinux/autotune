import os
import sys
import shlex
from subprocess import call
from subprocess import CalledProcessError, check_output
from subprocess import Popen, PIPE

# Exception
from ec2sys_autotune.ec2_instance_exception import Ec2AutotuneError


def exec_cmds(cmds):
    '''

    Execute passed in command
    '''
    devnull = open(os.devnull, 'wb')
    for cmd in cmds:
        try:
            retcode = call(shlex.split(cmd), shell=False,
                           stderr=devnull, stdout=devnull)
            if (retcode != 0):
                raise Ec2AutotuneError("Failed to execute: {0}".format(cmd))
        except OSError, e:
            raise Ec2AutotuneError("Exception encountered while trying to "
                                   "execute: {0} error: {1}".format(cmd, e))
    return


def get_cmd_output(cmd):
    '''

    Execute passed in command and return its output
    '''
    try:
        # Strip trailing newline feed
        output = check_output(shlex.split(cmd), shell=False)[:-1]
        return output
    except CalledProcessError, e:
        raise Ec2AutotuneError("Exception encountered while trying to execute:"
                               " {0} error: {1}".format(cmd, e.output))


def get_piped_cmd_output(cmd1, cmd2):
    try:
        p1 = Popen(shlex.split(cmd1), stdout=PIPE, shell=False)
        p2 = Popen(shlex.split(cmd2), stdin=p1.stdout,
                   stdout=PIPE, shell=False)
        p1.stdout.close()
        # Strip trailing newline feed
        output = (p2.communicate()[0])[:-1]
        return output
    except CalledProcessError, e:
        raise Ec2AutotuneError("Exception encountered while trying to execute:"
                               " {0} | {1}  error: {2}".format(cmd1,
                                                               cmd2,
                                                               e.output))


def read_sysfs_file(sysfs_file):
    try:
        with open(sysfs_file) as fd:
            # Strip trailing newline feed
            output = fd.read()[:-1]
        return output
    except IOError, e:
        raise Ec2AutotuneError(
            "Error while trying to query {0}, error {1}.".format(sysfs_file,
                                                                 e.errno))


def write_sysfs_file(sysfs_file, value):
    try:
        with open(sysfs_file, "wb") as fd:
            fd.write(value)
        return
    except IOError, e:
        raise Ec2AutotuneError(
            "Error while trying to write {0}, error {1}.".format(sysfs_file,
                                                                 e.errno))
