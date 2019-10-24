#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: hywell
@Email: hywell.28@gmail.com
@Blog: iassas.com
@Date: 2019/10/22 20:01
"""

import aiohttp
import random

from lib.core.setting import CONF


async def dirBrute(current_target):
    headers = {
        'User-Agent': CONF.user_agents[random.randint(0, len(CONF.user_agents) - 1)]
    }
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        if CONF.PROXY:
            proxies_num = len(CONF.proxies) - 1 if len(CONF.proxies) > 1 else 0
            proxy = CONF.proxies[random.randint(0, proxies_num)]
            async with session.get(current_target, headers=headers, allow_redirects=False, timeout=10,
                                   proxy=proxy) as response:
                return [response.status, current_target, None]
        else:
            async with session.get(current_target, headers=headers, allow_redirects=False, timeout=10) as response:
                return [response.status, current_target, None]
