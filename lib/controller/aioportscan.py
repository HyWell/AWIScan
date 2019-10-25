#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: hywell
@Email: hywell.28@gmail.com
@Blog: iassas.com
@Date: 2019/10/17 10:51
"""

from lib.controller.aionmap import *
from lib.core.setting import NMAP_CONF
from lib.core.setting import CONF, SUDO_PASSWORD, TARGETS


async def portScan(current_target):
    scanner = PortScanner()
    try:
        results = await scanner.scan(current_target, arguments=NMAP_CONF[CONF.level][0], sudo=True,
                                     sudo_passwd=SUDO_PASSWORD)
        return results
    except NameError:
        TARGETS.ERROR.ip.append(current_target)
