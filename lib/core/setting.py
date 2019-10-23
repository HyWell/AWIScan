# coding=utf-8

"""
@Author: hywell
@Email: hywell.28@gmail.com
@Blog: iassas.com
@Date: 2019/10/16 13:19
"""

import os
import random
import re
import sys

from lib.core.datatype import AttribDict

VERSION = "0.0.0.1"
SITE = "https://iassas.com"
TYPE = "dev" if VERSION.count('.') > 2 and VERSION.split('.')[-1] != '0' else "stable"
TYPE_COLORS = {"dev": 33, "stable": 90}
IS_WIN = True if (sys.platform in ["win32", "cygwin"] or os.name == "nt") else False
UNICODE_ENCODING = "utf-8"

BANNER = """\033[01;33m
      __          _______  _____                 
     /\ \        / /_   _|/ ____|                  \033[01;37m{\033[01;%dm%s\033[01;37m#%s}\033[01;33m
    /  \ \  /\  / /  | | | (___   ___ __ _ _ __  
   / /\ \ \/  \/ /   | |  \___ \ / __/ _` | '_ \ 
  / ____ \  /\  /   _| |_ ____) | (_| (_| | | | |
 /_/    \_\/  \/   |_____|_____/ \___\__,_|_| |_|  \033[0m\033[4;37m%s\033[0m\n
""" % (TYPE_COLORS.get(TYPE, 31), VERSION.split('/')[-1], TYPE, SITE)
HEURISTIC_CHECK_ALPHABET = ('"', '\'', ')', '(', ',', '.')
BANNER = re.sub(r"\[.\]", lambda _: "[\033[01;41m%s\033[01;49m]" % random.sample(HEURISTIC_CHECK_ALPHABET, 1)[0],
                BANNER)

NMAP_CONF = {1: ["-T4 -F "],
             2: ["-T4 -A -v -Pn"],
             3: ["-p 1-65535 -T4 -A -v -sS -Pn"]}
SUDO_PASSWORD = "082888"

ASYNC_NUM = 100
PROCESS_NUM = 10

CONF = AttribDict()
CONF.ROOT_PATH = ""

TARGETS = AttribDict()
TARGETS.END = AttribDict()
TARGETS.ERROR = AttribDict()

RESULT = AttribDict()

target_end = AttribDict()

DNS_SERVERS = "data/subDomain/dns_server.txt"
DNS_SUB_FILE = "data/subDomain/next_sub_full.txt"
DNS_SUB_FULL_FILE = "data/subDomain/subnames_full.txt"

DIR_FILE = "data/webScan/dict.txt"
USER_AGENTS = "data/webScan/user-agents.txt"
