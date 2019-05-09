# -*- coding: utf-8 -*-
import re
import json
import scrapy
from SMOM import helper
from SMOM.items import SmomItem
from scrapy.http import Request
from pyquery import PyQuery as pq
class InewsQqComSpider(scrapy.Spider):
    name = 'xincheping.com'

    entry_point = [
        'https://m.xincheping.com/pingce//p{p}.do',  #用车
        'https://m.xincheping.com/changce/p{p}.do?longTestId=&arttype=-1', #长测
        'https://m.xincheping.com/views/p{p}.do?page={p}',#观点
        'https://m.xincheping.com/cehua/p{p}.do',  #策划
    ]



    headers = {
        'accept-encoding': 'gzip',  # 只要gzip的压缩格式
        'Accept-Language': "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
        'Accept': "application/json, text/javascript, */*; q=0.01"
    }
    def start_requests(self):
        for entry_point in self.entry_point:
            for i in range(1,16):
                yield Request(url=entry_point.format(p=i), callback=self.parse, headers=self.headers, dont_filter=True)

    def parse(self, response):
        jsonbd = json.loads(response.text)

        if len(jsonbd['msg']) == 0 or '操作成功' not in jsonbd['msg']: return
        for item in jsonbd['result']['list']:
            if 'id' not in item.keys() or len(str(item['id'])) == 0: continue
            url = item['artUrl']

            date = item['time'] if 'time' in item.keys() else None
            source = item['channel'] if 'channel' in item.keys() else None
            title = item['title'] if 'title' in item.keys() else None

            yield Request(url=url, callback=self.content_parse, headers=self.headers,
                          meta={'id': item['id'], 'title': title, 'date': date,'source':source
                        })

    def content_parse(self, response):

        doc = pq(response.text)
        if doc == None or len(doc) == 0: return

        pipleitem = SmomItem()

        pipleitem['S0'] = response.meta['id'] if 'id' in response.meta.keys() else None
        pipleitem['S1'] = response.url
        pipleitem['S2'] = response.meta['source'] if 'source' in response.meta.keys() else None
        pipleitem['S3a'] = '文章评论类'
        pipleitem['S3d'] = None
        pipleitem['S4'] = response.meta['title'] if 'title' in response.meta.keys() else None
        pipleitem['S5'] = helper.get_localtimestamp()
        pipleitem['S6'] = response.meta['date'] if 'date' in response.meta.keys() else None
        pipleitem['S7'] = '新车评'
        pipleitem['S9'] = '1'
        pipleitem['S10'] = None
        pipleitem['S11'] = None
        pipleitem['S12'] = None
        pipleitem['S13'] = None
        pipleitem['ID'] = response.meta['id'] if 'id' in response.meta.keys() else None
        res = re.compile("作者：(.*)")
        pipleitem['G1'] = re.findall(res, doc('.xcp_time ').text())[0]
        pipleitem['Q1'] = doc('.xcp_info').text().replace('\n','')


        return pipleitem