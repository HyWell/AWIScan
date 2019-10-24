#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: hywell
@Email: hywell.28@gmail.com
@Blog: iassas.com
@Date: 2019/10/16 22:24
"""

from lib.core.data import logger
from lib.parse.ip import parseTarget
from lib.core.setting import ASYNC_NUM, CONF, TARGETS, PROCESS_NUM, PROXY, RESULT


def TargetRegister(targets):
    target_result = []
    for target in targets:
        parse_targets = parseTarget(target)
        for parse_target in parse_targets:
            ip = parse_target["ip"]
            domain = parse_target["domain"]
            url = parse_target["url"]
            if ip:
                RESULT[ip] = {}
                TARGETS.IP.append(ip)
                target_result.append([1, ip, None])
            elif domain:
                RESULT[domain] = {"subDomain": {"open": [], "close": []}, "status": ""}
                TARGETS.DOMAIN.append(domain)
                target_result.append([2, domain, None])
                for sub in CONF.dns_sub:
                    target_result.append([2, "%s.%s" % (sub, domain), domain])
            elif url:
                RESULT[url] = {"dic": [], "status": ""}
                TARGETS.URL.append(url)
                target_result.append([3, url, None])
                for dir in CONF.dir:
                    if "/" in dir:
                        target_result.append([3, url + dir, url])
                    else:
                        target_result.append([3, url + "/" + dir, url])
            else:
                logger.info("%s is end" % domain if domain else ip)
    return target_result


def InitRegister(level):
    CONF.async_num = ASYNC_NUM
    CONF.base_nums = None
    CONF.dir = []
    CONF.dns_servers = []
    CONF.dns_sub = []
    CONF.level = level
    CONF.levels = {"1": "", "2": "", "3": ""}
    CONF.proxies = []
    CONF.process_num = PROCESS_NUM
    CONF.quiet = False
    CONF.user_agents = []
    CONF.PROXY = True if PROXY else False
    logger.info("[AWIScan] Configuration has been initialized")
    TARGETS.IP = []
    TARGETS.DOMAIN = []
    TARGETS.URL = []
    TARGETS.END.ip = []
    TARGETS.END.domain = []
    TARGETS.END.url = []
    TARGETS.ERROR.ip = []
    TARGETS.ERROR.domain = []
    TARGETS.ERROR.url = []
    logger.info("[AWIScan] Target information has been initialized")


def initOptions(level):
    InitRegister(level)
