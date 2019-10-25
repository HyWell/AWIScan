#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: hywell
@Email: hywell.28@gmail.com
@Blog: iassas.com
@Date: 2019/10/19 15:58
"""

import aiodns

from lib.core.setting import CONF, TARGETS


async def subDomainBrute(current_target):
    ips = []
    resolver = aiodns.DNSResolver(nameservers=CONF.dns_servers)
    try:
        answers = await resolver.query(current_target, "A")
        TARGETS.END.domain.append(current_target)
        for answer in answers:
            address = answer.host
            if address not in ['1.1.1.1', '127.0.0.1', '0.0.0.0', '0.0.0.1']:
                ips.append(address)
        return [current_target, ips]
    except aiodns.error.DNSError:
        TARGETS.ERROR.domain.append(current_target)
