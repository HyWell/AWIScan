#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: hywell
@Email: hywell.28@gmail.com
@Blog: iassas.com
@Date: 2019/10/16 13:18
"""

import os
import re
import sys

from lib.core.convert import stdout_encode
from lib.core.log import LOGGER_HANDLER
from lib.core.setting import BANNER, CONF, IS_WIN, UNICODE_ENCODING
from lib.thirdparty.colorama.initialise import init as coloramainit
from lib.thirdparty.termcolor.termcolor import colored


def set_color(message, bold=False):
    if isinstance(message, bytes):
        message = message.decode(UNICODE_ENCODING)
    ret = message

    if message and getattr(LOGGER_HANDLER, "is_tty", False):  # colorizing handler
        if bold:
            ret = colored(message, color=None, on_color=None, attrs=("bold",))

    return ret


def data_to_stdout(data, bold=False):
    """
    Writes text to the stdout (console) stream
    """
    if 'quiet' not in CONF or not CONF.quiet:
        message = ""

        if isinstance(data, str):
            message = stdout_encode(data)
        else:
            message = data

        sys.stdout.write(set_color(message, bold))

        try:
            sys.stdout.flush()
        except IOError:
            pass
    return


def clear_colors(message):
    ret = message
    if message:
        ret = re.sub(r"\x1b\[[\d;]+m", "", message)
    return ret


def banner():
    _ = BANNER
    if not getattr(LOGGER_HANDLER, "is_tty", False):
        _ = clear_colors(_)
    elif IS_WIN:
        coloramainit()

    data_to_stdout(_)


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
