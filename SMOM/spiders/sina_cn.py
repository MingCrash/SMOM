# -*- coding: utf-8 -*-
import re
import json
import scrapy
from SMOM import helper
from SMOM.items import SmomItem
from scrapy.http import Request
from pyquery import PyQuery as pq
class InewsQqComSpider(scrapy.Spider):
    name = 'sina.cn'

    entry_point = 'http://interface.sina.cn/auto/inner/getWapNewsByColumnID.d.json?tagnews=no&cid=78606&label=null&limit=20&page={}&tuji=yes&weight=50'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip',  # 只要gzip的压缩格式
        'accept-language': 'zh-CN,zh;q=0.9',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
    }

    def start_requests(self):

        for i in range(1,10):
            yield Request(url=self.entry_point.format(i), callback=self.parse, headers=self.headers, dont_filter=True)

    def parse(self, response):
        jsonbd = json.loads(response.text)

        if len(jsonbd['data']) == 0: return
        for item in jsonbd['data']['data']:
            if 'id' not in item.keys() or len(item['id']) == 0: continue
            url = item['wap_url'] if 'wap_url' in item.keys() else None
            source = item['source'] if 'source' in item.keys() else None
            title = item['title'] if 'title' in item.keys() else None
            date = item['cTime'] if 'cTime' in item.keys() else None
            auther = item['writer'] if 'writer' in item.keys() else None

            yield Request(url=url, callback=self.content_parse, headers=self.headers,
                          meta={'id': item['id'],'title': title, 'date': date,
                                'source': source,'auther': auther})

    def content_parse(self, response):

        doc = pq(response.text)
        if doc == None or len(doc) == 0: return

        pipleitem = SmomItem()

        pipleitem['S0'] = response.meta['id'] if 'id' in response.meta.keys() else None
        pipleitem['S1'] = response.url
        pipleitem['S2'] =  None
        pipleitem['S3a'] = '文章评论类'
        pipleitem['S3d'] = None
        pipleitem['S4'] = response.meta['title'] if 'title' in response.meta.keys() else None
        pipleitem['S5'] = helper.get_localtimestamp()
        pipleitem['S6'] = response.meta['date'] if 'date' in response.meta.keys() else None
        pipleitem['S7'] = '新浪新闻'
        pipleitem['S9'] = '1'
        pipleitem['S10'] = None
        pipleitem['S11'] = None
        pipleitem['S12'] =  None
        pipleitem['S13'] =  None
        pipleitem['ID'] = response.meta['id'] if 'id' in response.meta.keys() else None
        pipleitem['G1'] = response.meta['auther'] if 'auther' in response.meta.keys() else None
        pipleitem['Q1'] = doc('#artCont').text().replace('\n','')

        return pipleitem