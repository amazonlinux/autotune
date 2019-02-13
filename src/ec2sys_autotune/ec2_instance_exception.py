import os
import sys


class Ec2AutotuneError(Exception):
    '''

    Exception class to indicate fatal configuration
    errors in autotune. This class can be extended
    to include more debugging information.
    '''
    def __init__(self, msg):
        self.msg = msg


class Ec2AutotuneEexists(Exception):
    '''

    Exception class to indicate EEXISTS error
    in autotune. This class can be extended
    to include more debugging information.
    '''

    def __init__(self, msg):
        self.msg = msg
