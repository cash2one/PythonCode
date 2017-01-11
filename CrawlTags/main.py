#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'lish'
import urllib2,re


def GenCrawlURL():
    url='http://book.qidian.com/info/3679201'


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}

url='http://book.qidian.com/info/3679201'
req = urllib2.Request(url=url, headers=headers)
resp = urllib2.urlopen(req, timeout=1)
html_details = resp.read()
tags=[]
tags+=re.findall('<a class="tags"[^~]+>(.*?)</a>',html_details)


print tags[0]