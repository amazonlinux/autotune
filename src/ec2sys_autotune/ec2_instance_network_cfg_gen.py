'''
EC2 instance HasA network.
This class needs to be a composition of base class.
'''

import os
import sys
from syslog import syslog
from ec2_instance_high_networking_performance import *

# Exceptions
from ec2sys_autotune.ec2_instance_exception import Ec2AutotuneError


class CfgGenNetworkSettings(object):
    '''

    Generate config for network settings
    '''
    def __init__(self, set_config, get_instance_data,
                 inst_class, add_secured_config):
        self.set_sysctl_config = set_config["sysctl"]
        self.get_instance_data = get_instance_data
        self.add_secured_config = add_secured_config
        return

    def __del__(self):
        self.set_sysctl_config = None
        self.get_instance_data = None
        return

    def tune(self):
        '''

        ##### Net Settings #####
        '''

        '''
        net.core.somaxconn
        Increase maximum connections
        '''
        self.set_sysctl_config("net.core.somaxconn", 1024)

        '''
        netdev_max_backlog
        Maximum number  of  packets,  queued  on  the  INPUT  side,
        when the interface receives packets faster than kernel can
        process them.
        '''
        self.set_sysctl_config("net.core.netdev_max_backlog", 1024 * 4)

        try:
            networking_performance = self.get_instance_data(
                                         "Networking Performance")

            if (networking_performance in HIGH_NETWORK_PERFORMANCE):
                '''
                busy_read:
                Low latency busy poll timeout for socket reads.
                busy_poll:
                Low latency busy poll timeout for poll and select.
                '''
                self.set_sysctl_config("net.core.busy_read", 50)
                self.set_sysctl_config("net.core.busy_poll", 50)
            else:
                self.set_sysctl_config("net.core.busy_read", 0)
                self.set_sysctl_config("net.core.busy_poll", 0)

            if (networking_performance in HIGH_NETWORK_PERFORMANCE):
                '''
                Internal tests showed a latency of 100 ms as RTT.
                To avoid bloating buffers in WAN, use only 20% of
                bandwidth delay product.
                Max bandwidth in WAN is limited by slowest link
                in the path.
                '''
                __min = 4
                if (networking_performance == "100 Gigabit"):
                    __def = 30
                    __max = 240
                elif (networking_performance == "50 Gigabit"):
                    __def = 30
                    __max = 120
                elif (networking_performance == "25 Gigabit"):
                    __def = 30
                    __max = 60
                elif (networking_performance == "20 Gigabit"):
                    __def = 12
                    __max = 48
                else:
                    # networking_performance == "10 Gigabit"
                    __def = 12
                    __max = 24

                '''
                rmem_max
                The maximum receive socket buffer size in bytes.
                '''
                self.set_sysctl_config("net.core.rmem_max",
                                       1024 * 1024 * __max)

                '''
                wmem_max
                The maximum send socket buffer size in bytes.
                '''
                self.set_sysctl_config("net.core.wmem_max",
                                       1024 * 1024 * __max)

                '''
                tcp_rmem used by auto tuning
                '''
                self.set_sysctl_config("net.ipv4.tcp_rmem",
                                       [1024 * __min,
                                        1024 * 1024 * __def,
                                        1024 * 1024 * __max])

                '''
                tcp_wmem used by auto tuning
                '''
                self.set_sysctl_config("net.ipv4.tcp_wmem",
                                       [1024 * __min,
                                        1024 * 1024 * __def,
                                        1024 * 1024 * __max])

            if (networking_performance in HIGH_NETWORK_PERFORMANCE):
                # Good for fixed speed network
                self.set_sysctl_config("net.ipv4.tcp_slow_start_after_idle",
                                       0)
                # High speed networks can bloat buffer
                self.set_sysctl_config("net.core.default_qdisc",
                                       "fq_codel")
                # Do not cache ssthresh from previous connection
                self.set_sysctl_config("net.ipv4.tcp_no_metrics_save",
                                       1)

        except Ec2AutotuneError, e:
            syslog(e.msg)
            syslog("Failed to generate configuration specific to "
                   "network performance")

        # MTU discovery
        self.set_sysctl_config("net.ipv4.tcp_mtu_probing", 1)

        # Make sure following defaults are not modified
        self.set_sysctl_config("net.ipv4.tcp_moderate_rcvbuf", 1)
        self.set_sysctl_config("net.ipv4.tcp_timestamps", 1)
        self.set_sysctl_config("net.ipv4.tcp_window_scaling", 1)
        self.set_sysctl_config("net.ipv4.tcp_sack", 1)

        # TCP keepalive parameters
        self.set_sysctl_config("net.ipv4.tcp_keepalive_time", 90)
        self.set_sysctl_config("net.ipv4.tcp_keepalive_intvl", 10)
        self.set_sysctl_config("net.ipv4.tcp_keepalive_probes", 9)

        # Controls IP packet forwarding
        self.set_sysctl_config("net.ipv4.ip_forward", 0)

        # Do not accept source routing
        self.set_sysctl_config("net.ipv4.conf.default.accept_source_route",
                               0)

        # Controls the use of TCP syncookies
        self.set_sysctl_config("net.ipv4.tcp_syncookies", 1)

        # Ignore echo broadcast requests
        self.set_sysctl_config("net.ipv4.icmp_echo_ignore_broadcasts", 1)

        if (self.add_secured_config is True):
            # Enable kernel reverse path filtering to do source validation of
            # the packets received from all the interfaces on the machine
            self.set_sysctl_config("net.ipv4.conf.default.rp_filter", 1)
            self.set_sysctl_config("net.ipv4.conf.all.rp_filter", 1)

            # Log martian packets
            self.set_sysctl_config("net.ipv4.conf.default.log_martians", 1)
            self.set_sysctl_config("net.ipv4.conf.all.log_martians", 1)

        # Ensure network settings if any are used immediately.
        self.set_sysctl_config("net.ipv4.route.flush", 1)
        self.set_sysctl_config("net.ipv6.route.flush", 1)

        return
