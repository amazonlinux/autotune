Amazon Linux Kernel Autotuning (Beta):
-------------------------------

License:
--------
The code is released under GNU GENERAL PUBLIC LICENSE 2.0. See LICENSE
for details.

Description:
------------
Amazon Web Services EC2 fleet hosts a wide selection of instance types
optimized to fit different customer use cases. Instance types are carved
out for varying combinations of CPU, Memory, Storage and Networking capacity
to allow customers to pick the correct instance type for their workload.

Amazon Linux Kernel provides a stable, secure and high performance execution
environment for customer applications running on Amazon EC2. Default values
for kernel tunables is not the best and optimized value for all instance
types on EC2. To provide best customer experience for Amazon Linux Kernel
consumers on EC2, this package optimizes kernel tunable for different
instance types.

Architecture:
-------------
Following are main blocks of ec2sys-autotune:

                            -------------
                            | workload  |
                            | specific  |
                            | generator |
                            -------------
                                 ^
                                 | Extends base generator
                                 |
                            -------------      -------------
                            | base      |      | Instance  |
                            | class     | <----| metadata  |
                            | generator |      | properties|
                            -------------      -------------
                                 |
                                 | Auto generated config file
                                 v
                            -------------
                            | Config    |
                            | file      |
                            |           |
                            -------------
                                 |
                                 | Consumed by engine
                                 v
                            -------------      ----------
                            | Config    |      | Saved  |
                            | engine    | <----| system |
                            |           |      | state  |
                            -------------      ----------

ec2sys-autotune is controlled by /bin/autotune CLI.

Base class generator: This block identifies the EC2 instance type that it
is running on and fetches all public properties of this EC2 instance type
from instance metadata file. Based on the public property of EC2 instances
and the instance type it is running on, it generates a config file that is
appropriate for running instance. As of today, this block can generate
config file to control services controlled from systemd, sysctl tunables,
sysfs tunables and CPU settings (C-state and P-state).

Config file: This is an auto generated file from base class generator.
However an end user is free to modify this config file as deemed appropriate
for ec2sys-autotune to apply the changes on the running instance.
These config files reside in /etc/ec2sys-autotune.d directory.

Config engine: This block is transparent to the type of running EC2 instance.
Engine reads the config file and applies all settings onto the running
EC2 instance. It also saves the state of the system. Upon rolling back the
tunables, engine restores the system to default state that was present
prior to tuning the system.

Workload specific generator: Any workload specific tuning need to inherit
from base class generator and generate system tunables. This can also be
used to stack or over ride tunables in base class generator.

Building:
---------
The code can be build using the Makefile script provided in the source.

1) Create a source distribution in gztar format
`make sources`

2) Install everything from build directory
`make install`

3) Create an RPM distribution
`make rpm`

4) Clean up temporary files from 'build' command
`make clean`

Usage:
------
As of this build, there are three profiles packaged:
1) base: This is general tuning of the system and the tunables
       are workload agnostic.
2) udp-server: This profile also demonstrates how the framework
       can be extended to add workload load specific tuning. As of now,
       this profile has few tunables that are required especially in
       docker or containers workload.
3) placement-group: This profile is for instances configured
       with EC2 placement group for low latecy network connectivity.

Display usage of the CLI:
/usr/bin/autotune --help

Set udp-server as profile:
/usr/bin/autotune profile udp-server

Enable the tunables:
/usr/bin/autotune apply

Disable the tunables:
/usr/bin/autotune rollback

Override a tunable in autotune profile:
autotune override sysctl:vm.swappiness:40

Exclude a tunable from autotune profile:
autotune exclude sysctl:vm.swappiness

Delete customized tunable from autotune profile:
autotune delete sysctl:vm.swappiness

Supported Distro's:
-------------------
Amazon Linux Kernel Autotuning is currently supported on Amazon Linux 2.
This package can be ported to Amazon Linux 1 and other distributions
with minimal changes.
