'''

EC2 instance HasA service.
This class needs to be a composition of base class.
'''

import os
import sys
from syslog import syslog


class CfgGenPerfOptimizingServices(object):
    '''

    Generate config for performance optimizing services
    '''
    def __init__(self, set_config, get_instance_data,
                 inst_class, add_secured_config):
        self.set_service_config = set_config["service"]
        return

    def __del__(self):
        self.set_service_config = None
        return

    def tune(self):
        '''
        ##### IRQ Balance #####
        irqbalance is a tool that distributes hardware interrupts across
        processors. Start this service if not already started.
        '''
        self.set_service_config("irqbalance", "start")
        return
