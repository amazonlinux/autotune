#!/usr/bin/python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

ec2sys_autotune_classifiers = [
    "Development Status :: Preview",
    "Environment :: Amazon Linux 2",
    "Intended Audience :: AWS EC2 AL2 consumers",
    "Operating System :: Amazon Linux 2",
    "Programming Language :: Python",
    "License :: GNU GENERAL PUBLIC LICENSE 2.0",
    "Topic :: Utilities",
]

with open("README.md", "r") as fp:
    ec2sys_autotune_long_description = fp.read()

setup(name="ec2sys-autotune",
      version='1.0.5',
      author="Vallish Vaidyeshwara",
      author_email="vallish@amazon.com",
      url="https://github.com/awslabs/ec2sys-autotune",
      scripts=["scripts/ec2sys_autotune_start",
               "scripts/ec2sys_autotune_stop",
               "scripts/autotune"],
      data_files=[("/usr/lib/systemd/system", ["unit/autotune.service"]),
                  ("/etc", ["config/ec2sys-autotune.cfg"]),
                  ("/etc/ec2sys-autotune.d", ["config/user.ini"]),
                  ("/var/lib/ec2sys-autotune", [])],
      packages=["ec2sys_autotune"],
      package_dir={"ec2sys_autotune": "src/ec2sys_autotune"},
      description="Amazon Linux Kernel Autotuning",
      long_description=ec2sys_autotune_long_description,
      license="GNU GENERAL PUBLIC LICENSE 2.0",
      classifiers=ec2sys_autotune_classifiers)
