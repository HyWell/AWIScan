#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: hywell
@Email: hywell.28@gmail.com
@Blog: iassas.com
@Date: 2019/10/16 13:18
"""

import os

from lib.core.setting import BANNER, CONF


def banner():
    _ = BANNER
    print(_)


def setPaths():
    """
    Set absolute absolute path
    """

    root_path = CONF.ROOT_PATH

    CONF.DATA_PATH = os.path.join(root_path, "data")
    CONF.OUTPUT_PATH = os.path.join(root_path, "output")
    if not os.path.exists(CONF.OUTPUT_PATH):
        os.mkdir(CONF.OUTPUT_PATH)
    if not os.path.exists(CONF.DATA_PATH):
        os.mkdir(CONF.DATA_PATH)
