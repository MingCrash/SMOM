# -*- coding: utf-8 -*-
import re
import json
import scrapy
from SMOM import helper
from SMOM.items import SmomItem
from scrapy.http import Request,FormRequest

# 天天快报
class AppCnewsQqSpider(scrapy.Spider):
    name = 'app.cnews.qq'

    entry_point = {
        '汽车': 'http://r.cnews.qq.com/getSubNewsChlidInterest?devid=A000009114F247',
    }

    headers = {
        'Host: r.cnews.qq.com',
        'Accept-Encoding: gzip,deflate',
        'Referer: http://cnews.qq.com/cnews/android/',
        'User-Agent: %E5%A4%A9%E5%A4%A9%E5%BF%AB%E6%8A%A55050(android)',
        'Cookie: lskey=; luin=; skey=; uin=; logintype=0;',
        'qn-sig: b9be61684b5066b8c0da561ba4e58f1d',
        'svqn: 1_4',
        'qn-rid: 11324bfc-340d-49e0-aafa-43911fe607c3',
        'snqn: YMyuXspv1oaObsq1xVgJjBk/bRxcNkH+NhHB5zb+kYB7MWt9jXPyIRsNgxHlvFyM41VPg7QAG8QeEeqc8/TLJHUYr3Jp0H/2J/UC2NM6VwxHcQTy9UwQOX447r76y7y46mUk7giTgj7By41B/u30Ew==',
        'Content-Type: application/x-www-form-urlencoded',
        'Connection: Keep-Alive',
        'Content-Length: 1997'
        # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 'accept-encoding': 'gzip',  # 只要gzip的压缩格式
        # 'accept-language': 'zh-CN,zh;q=0.9',
        # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
    }

    data = {

    }

    def start_requests(self):
        for key in self.entry_point.keys():
            yield FormRequest(url=self.entry_point[key], callback=self.parse, headers=self.headers,dont_filter=True)

    def parse(self, response):
        print(len(response.text))
        print(response.text)