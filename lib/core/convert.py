#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: hywell
@Email: hywell.28@gmail.com
@Blog: iassas.com
@Date: 2019/10/16 13:57
"""

import sys

from lib.core.setting import IS_WIN
from lib.core.setting import UNICODE_ENCODING


def single_time_warn_message(message):
    """
    Cross-linked function
    """
    sys.stdout.write(message)
    sys.stdout.write("\n")
    sys.stdout.flush()


def stdout_encode(data):
    try:
        data = data or ""

        # Reference: http://bugs.python.org/issue1602
        if IS_WIN:
            output = data.encode(sys.stdout.encoding, "replace")

            if '?' in output and '?' not in data:
                warn_msg = "cannot properly display Unicode characters "
                warn_msg += "inside Windows OS command prompt "
                warn_msg += "(http://bugs.python.org/issue1602). All "
                warn_msg += "unhandled occurances will result in "
                warn_msg += "replacement with '?' character. Please, find "
                warn_msg += "proper character representation inside "
                warn_msg += "corresponding output files. "
                single_time_warn_message(warn_msg)

            ret = output
        else:
            ret = data.encode(sys.stdout.encoding)
    except Exception:
        ret = data.encode(UNICODE_ENCODING) if isinstance(data, str) else data

    return ret
