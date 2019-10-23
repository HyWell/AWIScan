#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: hywell
Email: hywell.28@gmail.com
Blog: iassas.com

date: 2019/10/16 10:18
"""

import os

from lib.controller.engine import run
from lib.core.common import banner, setPaths
from lib.core.data import logger
from lib.core.options import initOptions
from lib.core.setting import CONF
from lib.parse.cmdline import parse_args


def main():
    """"
    Main function of AWIScan when running from command line.
    """

    banner()

    # Set paths of project.
    CONF.ROOT_PATH = os.getcwd()
    setPaths()

    # received command >> parse_args
    base_targets, level = parse_args()
    initOptions(level)

    run(base_targets)
    logger.info("[AWIScan] All target is end")


if __name__ == '__main__':
    main()
