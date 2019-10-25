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
from lib.core.setting import ASYNC_NUM, CONF, TARGETS, PROCESS_NUM, PROXY, RESULT, STATUS


def TargetRegister(targets):
    target_result = []
    for target in targets:
        parse_targets = parseTarget(target)
        for parse_target in parse_targets:
            ip = parse_target["ip"]
            domain = parse_target["domain"] if parse_target["domain"] else "Domain Null"
            url = parse_target["url"] if parse_target["url"] else "Url Null"
            if ip:
                if ip not in RESULT:
                    RESULT[ip] = {
                        "Status": "",
                        "MAC": "",
                        "HostNames": "",
                        "services": "",
                        domain: {
                            "status": "",
                            "subDomain": []
                        },
                        url: []
                    }
                    TARGETS.IP.append(ip)
                    target_result.append([1, ip, None, None, ip])
                    if domain != "Domain Null":
                        TARGETS.DOMAIN.append(domain)
                        target_result.append([2, ip, domain, None, None])
                        for sub in CONF.dns_sub:
                            TARGETS.subDomain.append("%s.%s" % (sub, domain))
                            target_result.append([2, ip, domain, None, "%s.%s" % (sub, domain)])
                    if url != "Url Null":
                        TARGETS.URL.append(url)
                        target_result.append([3, ip, domain, url, url])
                        for dir in CONF.dir:
                            if "/" in dir:
                                target_result.append([3, ip, domain, url, url + dir])
                                TARGETS.URL.append(url + dir)
                            else:
                                target_result.append([3, ip, domain, url, url + "/" + dir])
                                TARGETS.URL.append(url + "/" + dir)
                else:
                    if domain != "Domain Null" and domain not in RESULT[ip]:
                        RESULT[ip][domain] = {
                            "status": "",
                            "subDomain": []
                        }
                        TARGETS.DOMAIN.append(domain)
                        target_result.append([2, ip, domain, None, None])
                        for sub in CONF.dns_sub:
                            TARGETS.subDomain.append("%s.%s" % (sub, domain))
                            target_result.append([2, ip, domain, None, "%s.%s" % (sub, domain)])
                    if url != "Url Null" and url not in RESULT[ip]:
                        RESULT[ip][url] = []
                        TARGETS.URL.append(url)
                        target_result.append([3, ip, domain, url, url])
                        for dir in CONF.dir:
                            if "/" in dir:
                                target_result.append([3, ip, domain, url, url + dir])
                                TARGETS.URL.append(url + dir)
                            else:
                                target_result.append([3, ip, domain, url, url + "/" + dir])
                                TARGETS.URL.append(url + "/" + dir)
            else:
                logger.warning("[AWIScan] %s is error" % target)
    return target_result


def InitRegister(level):
    CONF.async_num = ASYNC_NUM
    CONF.base_nums = None
    CONF.dir = []
    CONF.dns_servers = []
    CONF.dns_sub = []
    CONF.level = level
    CONF.proxies = []
    CONF.process_num = PROCESS_NUM
    CONF.quiet = False
    CONF.user_agents = []
    CONF.PROXY = True if PROXY else False
    CONF.STATUS = STATUS
    logger.info("[AWIScan] Configuration has been initialized")
    TARGETS.IP = []
    TARGETS.DOMAIN = []
    TARGETS.subDomain = []
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
