#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: hywell
@Email: hywell.28@gmail.com
@Blog: iassas.com
@Date: 2019/10/16 23:38
"""

import asyncio
import aiodns
# import multiprocessing as mp
import traceback
import sys

from lib.controller.aiodirscan import dirBrute
from lib.controller.aioportscan import portScan
from lib.controller.aiosubdomainscan import subDomainBrute
from lib.core.data import logger
from lib.core.options import TargetRegister
from lib.core.setting import CONF, DIR_FILE, DNS_SERVERS, DNS_SUB_FILE, DNS_SUB_FULL_FILE, PROXIES, TARGETS, USER_AGENTS
from lib.parse.result import resultParse, save


async def scan(task_queue):
    while True:
        # e.x [flag, ip, domain, url, current_target]
        target = await task_queue.get()
        flag = target[0]
        current_target = target[4] if target[4] else target[2]
        results = []
        try:
            if flag == 1:
                results = await portScan(current_target)
                TARGETS.END.ip.append(current_target)
            elif flag == 2 and CONF.dns_servers:
                results = await subDomainBrute(current_target)
            elif flag == 3:
                results = await dirBrute(current_target)
        except Exception as e:
            errmsg = traceback.format_exc()
            logger.error("[AWIscan] It's errmsg:%s" % errmsg)
        finally:
            logger.info("[AWIScan] Total ip: %d/%d subDomain: %d/%d url: %d/%d" % (
                len(TARGETS.END.ip), len(TARGETS.IP), len(TARGETS.END.domain) + len(TARGETS.ERROR.domain),
                len(TARGETS.subDomain) + len(TARGETS.DOMAIN), len(TARGETS.END.url) + len(TARGETS.ERROR.url),
                len(TARGETS.URL)))
            if results:
                # Parse the result, put it into the work queue.
                resultParse(task_queue, target, results)
            task_queue.task_done()


async def control(base_targets):
    targets_queue = asyncio.Queue()
    for target in TargetRegister(base_targets):
        targets_queue.put_nowait(target)
    if targets_queue.qsize() == 0:
        logger.warning("[AWIScan] No targets found. Please load targets with [-i|-f] or verify target num")
        sys.exit()
    else:
        logger.info("[AWIScan] Target loading completed. Total %d targets" % (len(TARGETS.IP)))

    logger.info("[AWIScan] Set the tasks of async_nums: %d" % CONF.async_num)
    tasks = []
    for i in range(0, CONF.async_num):
        tasks.append(
            asyncio.create_task(scan(targets_queue))
        )
    await targets_queue.join()
    save()


def webEngine():
    for dir in open(DIR_FILE).readlines():
        dir = dir.strip()
        CONF.dir.append(dir)
    for user_agent in open(USER_AGENTS).readlines():
        user_agent = user_agent.strip()
        CONF.user_agents.append(user_agent)
    if CONF.PROXY:
        for proxy in open(PROXIES).readlines():
            proxy = proxy.strip()
            CONF.proxies.append(proxy)
    logger.info("[AWIScan] Dir data loading completed. Total %d dir" % len(CONF.dir))


async def test_server(server):
    resolver = aiodns.DNSResolver(nameservers=[server])
    try:
        answers = await resolver.query('public-dns-a.baidu.com', "A")
        if answers[0].host != '180.76.76.76':
            raise Exception('[AWIScan] %s return incorrect DNS response' % server)
        else:
            try:
                await resolver.query('test.bad.dns.iassas.com', "A")
                with open('output/AWIScan/bad_dns_servers.txt', 'a+') as f:
                    f.write(server + '\n')
                logger.warning("[AWIScan] Bad DNS Server found %s" % server)
            except aiodns.error.DNSError as e:
                if b"DNS server returned answer with no data" == e.args[1]:
                    CONF.dns_servers.append(server)
                elif b"Timeout while contacting DNS servers" == e.args[1]:
                    logger.warning("[AWIScan] %s DNS Server test error. Please verify." % server)
        logger.info('[AWIScan] DNS Server %s < OK > Found %s' % (server.ljust(16), len(CONF.dns_servers)))
    except Exception as e:
        logger.warning("[AWIScan] DNS Server %s <Fail> Found %s" % (server.ljust(16), len(CONF.dns_servers)))


async def dnsEngine():
    tasks = []
    for server in open(DNS_SERVERS).readlines():
        server = server.strip()
        if server and not server.startswith('#'):
            tasks.append(
                asyncio.create_task(test_server(server))
            )
    await asyncio.gather(*tasks)
    if CONF.dns_servers and (CONF.level == 1 or CONF.level == 2):
        with open(DNS_SUB_FILE) as f:
            for sub in f.readlines():
                CONF.dns_sub.append(sub.strip())
        logger.info(
            "[AWIScan] DNS loading completed. Total %d DNS Server and %d sub" % (len(CONF.dns_servers),
                                                                                 len(CONF.dns_sub)))
    elif CONF.dns_servers and CONF.level == 3:
        with open(DNS_SUB_FULL_FILE) as f:
            for sub in f.readlines():
                CONF.dns_sub.append(sub.strip())
        logger.info(
            "[AWIScan] DNS loading completed. Total %d DNS Server and %d sub" % (len(CONF.dns_servers),
                                                                                 len(CONF.dns_sub)))


def initEngine():
    asyncio.run(dnsEngine())
    webEngine()


def run(base_targets):
    initEngine()

    asyncio.run(control(base_targets))
