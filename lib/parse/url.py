#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: hywell
@Email: hywell.28@gmail.com
@Blog: iassas.com
@Date: 2019/10/16 16:31
"""

import re

from lib.core.data import logger
from urllib.parse import urlparse


class URL:

    def __init__(self, schema: bytes, host: bytes, port, path: bytes,
                 query: bytes, fragment: bytes, userinfo: bytes):
        self.schema = schema.decode('utf-8')
        self.host = host.decode('utf-8')
        if port and port != 0:
            self.port = port
        else:
            if schema == b'https':
                self.port = 443
            else:
                self.port = 80
        self.path = path.decode('utf-8') if path else ''
        self.query = query.decode('utf-8') if query else None
        self.fragment = fragment.decode('utf-8') if fragment else None
        self.userinfo = userinfo.decode('utf-8') if userinfo else None
        self.netloc = self.schema + '://' + self.host + ':' + str(self.port)

    @property
    def raw(self):
        return self.netloc + (self.path or '') + (self.query or '') + (self.fragment or '')

    def __repr__(self):
        return ('<URL schema: {!r}, host: {!r}, port: {!r}, path: {!r}, '
                'query: {!r}, fragment: {!r}, userinfo: {!r}>'
                .format(self.schema, self.host, self.port, self.path, self.query, self.fragment, self.userinfo))


def parse_url(url):
    try:
        parsed = urlparse(url)
        userinfo = b'{parsed.username}:{parsed.password}'
        return URL(parsed.scheme, parsed.hostname, parsed.port, parsed.path, parsed.query, parsed.fragment, userinfo)
    except Exception:
        raise ("invalid url {!r}".format(url))


def url_regex(raw):
    """""
    Collect url
    """
    urls = []
    try:
        urls_regex = re.findall(r"((?:https?|ftp|file):\/\/[\-A-Za-z0-9+&@#/%?=~_|!:,.;\*]+[\-A-Za-z0-9+&@#/%=~_|])",
                                str(raw))
        for url in urls_regex:
            url_flag = '<a href="' + url + '" target=_blank />' + url + '</a>'
            urls.append(url_flag)
    except Exception as e:
        logger.error(e)
        pass
    return urls
