#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: hywell
@Email: hywell.28@gmail.com
@Blog: iassas.com
@Date: 2019/10/19 15:58
"""

import aiodns

from lib.core.setting import CONF


async def subDomainBrute(current_target):
    ips = []
    resolver = aiodns.DNSResolver(nameservers=CONF.dns_servers)
    try:
        answers = await resolver.query(current_target, "A")
        for answer in answers:
            address = answer.host
            if address in ['1.1.1.1', '127.0.0.1', '0.0.0.0', '0.0.0.1']:
                return [0, current_target, None]
            else:
                ips.append(address)
        return [1, current_target, ips]
    except aiodns.error.DNSError:
        return [0, current_target, None]
