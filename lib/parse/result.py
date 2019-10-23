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


def dirParse(base_url, url, result):
    results = []
    status = result[0]
    if base_url:
        RESULT[base_url]["dic"].append([url, status])
    else:
        RESULT[url]["status"] = status
        TARGETS.END.url.append(base_url)
    return results


def subDomainParse(base_domain, domain, result):
    results = []
    status = result[0]
    if status == 1:
        for sub in CONF.dns_sub:
            results.append("%s.%s" % (sub, domain))
    if base_domain:
        RESULT[base_domain]["subDomain"].append(domain)
    else:
        RESULT[domain]["status"] = "open" if base_domain is None else "close"
        TARGETS.END.domain.append(base_domain)
    return results


def portScanParse(ip, results):
    services = {}
    result = results.hosts
    put_targets = []
    if result:
        RESULT[ip]["status"] = "open"
        result = result[0]
        for service in result.services:
            if "http" in service.service or "https" in service.service:
                put_targets.append(str(ip) + ":" + str(service.port))
            services[service.port] = [service.service, service.state]
        HostNames = result.hostnames[0] if result.hostnames else None
        RESULT[ip]["nmap"] = {
            "MAC": result.mac,
            "HostNames": HostNames,
            "services": services
        }
    else:
        RESULT[ip]["status"] = "close"
    TARGETS.END.ip.append(ip)
    return put_targets


def resultParse(task_queue, target, results):
    put_targets = []
    flag = target[0]
    current_target = target[1]
    if flag == 1:
        put_targets = portScanParse(current_target, results)
    elif flag == 2:
        base_domain = target[2]
        put_targets = subDomainParse(base_domain, current_target, results)
    elif flag == 3:
        base_url = target[2]
        put_targets = dirParse(base_url, current_target, results)
    if CONF.level == "not now":
        for put_target in put_targets:
            task_queue.put_nowait(put_target)
