# -*- coding: utf-8 -*-
import re
import json
import scrapy
from SMOM import helper
from SMOM.items import SmomItem
from scrapy.http import Request
from pyquery import PyQuery as pq

# 汽车头条APP
class InewsQqComSpider(scrapy.Spider):
    name = 'm.qctt.cn'

    # entry_point = {
    #         "新车"  : "id=1&page={}",
    #         "行业"  : "id=2&page={}",
    #         "导购"  : "id=3&page={}",
    #         "原创"  : "id=10002&page={}",
    #         "来电"  : "id=39&page={}",
    #         "用车"  : "id=30&page={}"
    #      }

    id_num = [ "1","2","3","10002","39","30"]
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip',  # 只要gzip的压缩格式
        'accept-language': 'zh-CN,zh;q=0.9',
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
    }

    def start_requests(self):
        for id in self.id_num:
            for i in range(1,20):
                url = 'https://m.qctt.cn/channel_more'
                yield scrapy.FormRequest(url=url,formdata = {'id': id ,'page': str(i)},
                                         callback=self.parse, headers=self.headers,
                                         dont_filter=True)
    #
    def parse(self, response):
        jsonbd = json.loads(response.text)

        if len(jsonbd['data']) == 0: return
        for item in jsonbd['data']:
            if 'id' not in item.keys() or len(str(item['id'])) == 0: continue
            url = 'https://m.qctt.cn/news/{}'.format(
                item['id'])
            date = item['publish_time'] if 'publish_time' in item.keys() else None
            source = item['source'] if 'source' in item.keys() else None
            title = item['title'] if 'title' in item.keys() else None
            read_num = item['read_num'] if 'read_num' in item.keys() else 0
            author_name = item['author_name'] if 'author_name' in item.keys() else 0

            yield Request(url=url, callback=self.content_parse, headers=self.headers,
                          meta={'id': item['id'], 'read_num': read_num, 'title': title,
                                'date': date,'source': source,'author_name':author_name})
    #
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
        pipleitem['S7'] = '汽车头条APP'
        pipleitem['S9'] = '1'
        pipleitem['S10'] = None
        pipleitem['S11'] = response.meta['read_num'] if 'read_num' in response.meta.keys() else None
        pipleitem['S12'] = None
        pipleitem['S13'] = None
        pipleitem['ID'] = response.meta['id'] if 'id' in response.meta.keys() else None
        pipleitem['G1'] = response.meta['author_name'] if 'author_name' in response.meta.keys() else None
        pipleitem['Q1'] = doc('.cont_wrap').text().replace('\n','')


        return pipleitem