#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: hywell
@Email: hywell.28@gmail.com
@Blog: iassas.com
@Date: 2019/10/16 16:32
"""

import re
import socket
import ipaddress

from lib.core.data import logger
from urllib.parse import urlparse


def url2ip(url):
    ip = ''
    try:
        handel_url = urlparse(url).hostname
        ip = socket.gethostbyname(handel_url)
    except Exception as e:
        logger.warning('[AWIScan] %s can not get ip! Please verify', url)
    return ip

# def c_ip(ip):
#     ip_list = []
#     ip_split = ip.split('.')
#     for c in range(1, 255):
#         ip = "%s.%s.%s.%d" % (ip_split[0], ip_split[1], ip_split[2], c)
#         ip_list.append(ip)
#     return ip_list


def genIP(ip_range):
    """
    print (genIP('192.18.1.1-192.168.1.3'))
    ['192.168.1.1', '192.168.1.2', '192.168.1.3']
    """

    # from https://segmentfault.com/a/1190000010324211
    def num2ip(num):
        return '%s.%s.%s.%s' % ((num >> 24) & 0xff, (num >> 16) & 0xff, (num >> 8) & 0xff, (num & 0xff))

    def ip2num(ip):
        ips = [int(x) for x in ip.split('.')]
        return ips[0] << 24 | ips[1] << 16 | ips[2] << 8 | ips[3]

    start, end = [ip2num(x) for x in ip_range.split('-')]
    return [num2ip(num) for num in range(start, end + 1) if num & 0xff]


def parseTarget(target):
    lists = []
    ipv4_re = re.compile(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
    ipv4withmask_re = re.compile("^(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|["
                                 "1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1["
                                 "0-9][0-9]|[1-9]?[0-9])/(3[0-2]|[1-2]?[0-9])$")
    ipv4range_re = re.compile("^(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|["
                              "1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1["
                              "0-9][0-9]|[1-9]?[0-9])-(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4]["
                              "0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25["
                              "0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$")
    try:
        parsed_url = urlparse(target)
        if parsed_url.scheme == "http" or parsed_url.scheme == "https":
            # e.x http://10.1.1.1 https://10.1.1.1
            url2ip(target)
            target = {"ip": None, "domain": None, "url": "%s://%s" % (parsed_url.scheme, parsed_url.netloc)}
            lists.append(target)
        else:
            if ipv4withmask_re.search(parsed_url.path):
                # e.x 10.1.1.1/24
                network = list(ipaddress.ip_interface(target).network)
                for ip in network:
                    target = {"ip": str(ip), "domain": None, "url": None}
                    lists.append(target)
            elif ipv4range_re.search(target):
                # e.x 10.1.1.1-10.1.1.10
                ips = genIP(target)
                for ip in ips:
                    target = {"ip": ip, "domain": None, "url": None}
                    lists.append(target)
            else:
                if ipv4_re.search(target):
                    # e.x 10.1.1.1
                    target = {"ip": target, "domain": None, "url": None}
                    lists.append(target)
                else:
                    target = {"ip": None, "domain": target, "url": None}
                    lists.append(target)
    except Exception as e:
        logger.error(e)
    return lists
