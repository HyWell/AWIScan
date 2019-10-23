#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: hywell
@Email: hywell.28@gmail.com
@Blog: iassas.com
@Date: 2019/10/22 20:01
"""

import aiohttp


async def dirBrute(current_target):
    async with aiohttp.ClientSession() as session:
        async with session.get(current_target) as response:
            return [response.status, current_target, None]
