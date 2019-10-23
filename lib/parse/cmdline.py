#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: hywell
@Email: hywell.28@gmail.com
@Blog: iassas.com
@Date: 2019/10/16 16:04
"""

import argparse
import os
import sys

from lib.core.data import logger


def parse_args():
    """"
    This function parses the command line parameters and arguments.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='''
            python AWIScan.py -i 10.10.10.10 -l 1
            python AWIScan.py -f target.com -l 1''', epilog="Believe that with the above description, " +
                                                            "you can start working right away. Wish you success")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-i", "--ip", help="scan a target or network(e.g. target.com ,192.168.1.1[/24], "
                                          "192.168.1.1-192.168.1.100)")
    group.add_argument("-f", "--file", help="load target from targetFile (e.g. target.txt)")
    parser.add_argument("-l", "--level", type=int, choices=[1, 2, 3], default=1,
                        help="This option is used to provide the scan level.")

    args = parser.parse_args()

    if args.ip:
        logger.info("[AWIScan] Load targets from: %s" % args.ip)
        base_targets = [args.ip]

        return base_targets, args.level
    elif args.file:
        if os.path.exists(args.file):
            logger.info("[AWIScan] Load targets from: %s" % args.file)
            base_targets = []
            with open(args.file, 'r', encoding='utf-8') as f:
                tars = f.readlines()
                for target in tars:
                    target = target.strip('\n')
                    base_targets.append(target)
            return base_targets, args.level
        else:
            logger.error("[AWIScan] {} file is not exist.".format(args.file))
            sys.exit(0)
    else:
        parser.print_help()
        sys.exit(0)
