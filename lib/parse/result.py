#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: hywell
@Email: hywell.28@gmail.com
@Blog: iassas.com
@Date: 2019/10/17 22:14
"""

import time

from lib.core.setting import CONF, TARGETS, RESULT


def save():
    with open("output/result/" + str(time.time()) + ".txt", 'w+') as f:
        f.write(str(RESULT))


def dirParse(ip, current_target, base_url, results):
    result = []
    status = results[0]
    RESULT[ip][base_url].append([current_target, status])
    return result


def subDomainParse(ip, current_target, base_domain):
    put_targets = []
    if base_domain:
        RESULT[ip][base_domain]["subDomain"].append(current_target)
        for sub in CONF.dns_sub:
            put_targets.append("%s.%s" % (sub, current_target))
    else:
        RESULT[ip][current_target]["status"] = "open"
    return put_targets


def portScanParse(ip, results):
    services = {}
    result = results.hosts
    put_targets = []
    if result:
        result = result[0]
        for service in result.services:
            if "http" in service.service or "https" in service.service:
                put_targets.append(str(ip) + ":" + str(service.port))
            services[service.port] = [service.service, service.state]
        HostNames = result.hostnames[0] if result.hostnames else None
        RESULT[ip]["Status"] = "open"
        RESULT[ip]["MAC"] = result.mac
        RESULT[ip]["HostNames"] = HostNames
        RESULT[ip]["services"] = services
    else:
        RESULT[ip]["status"] = "close"
    return put_targets


def resultParse(task_queue, target, results):
    put_targets = []
    flag = target[0]
    ip = target[1]
    domain = target[2]
    url = target[3]
    current_target = target[4] if target[4] else target[2]

    if flag == 1:
        put_targets = portScanParse(current_target, results)
    elif flag == 2:
        base_domain = domain if target[4] else None
        current_target = current_target if current_target else domain
        put_targets = subDomainParse(ip, current_target, base_domain)
    elif flag == 3:
        base_url = url if target[4] else None
        current_target = current_target if current_target else url
        put_targets = dirParse(ip, current_target, base_url, results)
    if CONF.level == "not now":
        for put_target in put_targets:
            task_queue.put_nowait(put_target)
