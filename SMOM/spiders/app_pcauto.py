# -*- coding: utf-8 -*-
import re
import json
import scrapy
import time
import requests
from SMOM import helper
from SMOM.items import SmomItem
from scrapy.http import Request

# 太平洋汽车APP
class AppPcautoSpider(scrapy.Spider):
    name = 'app.pcauto'
    entry_point = {
        '推荐': 'https://mrobot.pcauto.com.cn/xsp/s/auto/info/nocache/cms/channel1_1.xsp?cityId=1&index=1&pageSize=40&uid=73d11113d01c3f778364b0620cd68ec1&v=5.8.1',
        '最新': 'https://mrobot.pcauto.com.cn/v2/cms/channel1_2?inreview=0&pageNo=1&pageSize=20&v=5.8.1',
        '新车': 'https://mrobot.pcauto.com.cn/v2/cms/channels/2?inreview=0&pageNo=1&pageSize=20&v=5.5.4',
        '评测': 'https://mrobot.pcauto.com.cn/v2/cms/channels/4?inreview=0&pageNo=1&pageSize=20&v=5.5.4',
        '导购': 'https://mrobot.pcauto.com.cn/v2/cms/channels/3?inreview=0&pageNo=1&pageSize=20&v=5.5.4',
        '电动车': 'https://mrobot.pcauto.com.cn/xsp/s/auto/info/cms/newEnergyList.xsp?pageNo=1&pageSize=20',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip',  # 只要gzip的压缩格式
        'accept-language': 'zh-CN,zh;q=0.9',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
    }

    def start_requests(self):
        for key in self.entry_point.keys():
            if key == '推荐':
                yield Request(url=self.entry_point[key], callback=self.recomment_parse, dont_filter=True)
            if key == '最新' or key == '电动车':
                yield Request(url=self.entry_point[key], callback=self.newest_parse, dont_filter=True)
            if key == '新车' or key == '评测' or key == '导购':
                yield Request(url=self.entry_point[key], callback=self.newcar_parse, dont_filter=True)

    def recomment_parse(self, response):
        jsonbd = json.loads(response.text)
        if len(jsonbd['focus']) == 0: return
        for item in jsonbd['focus']:
            if 'url' not in item.keys() or len(item['url']) == 0: continue
            if re.search('www.pcauto.com.cn',item['url']):
                id = item['id'] if 'id' in item.keys() else None
                date = item['pubDate'] if 'pubDate' in item.keys() else None
                yield Request(url=item['url'], callback=self.web_content_parse, headers=self.headers, meta={'date': date,'id': id})

    def newest_parse(self, response):
        jsonbd = json.loads(response.text)
        if len(jsonbd['data']) == 0: return
        for item in jsonbd['data']:
            if 'url' not in item.keys() or len(item['url']) == 0: continue
            if re.search('www.pcauto.com.cn', item['url']):
                id = item['id'] if 'id' in item.keys() else None
                date = item['pubDate'] if 'pubDate' in item.keys() else None
                count = item['count'] if 'count' in item.keys() else None
                yield Request(url=item['url'], callback=self.web_content_parse, headers=self.headers, meta={'date': date,'id': id,'count':count})

    def newcar_parse(self, response):
        jsonbd = json.loads(response.text)
        if len(jsonbd['articleList']) == 0: return
        for item in jsonbd['articleList']:
            if 'url' not in item.keys() or len(item['url']) == 0: continue
            if re.search('www.pcauto.com.cn', item['url']):
                id = item['id'] if 'id' in item.keys() else None
                date = item['pubDate'] if 'pubDate' in item.keys() else None
                count = item['cmtCount'] if 'cmtCount' in item.keys() else None
                yield Request(url=item['url'], callback=self.web_content_parse, headers=self.headers,meta={'date': date, 'id': id, 'count':count})

    def web_content_parse(self, response):
        pipleitem = SmomItem()

        time.sleep(3)
        rs = requests.get(url='https://mrobot.pcauto.com.cn/v3/cmt/get_newest_floor?url={}'.format(response.url))
        commentcount = response.meta['count'] if 'count' in response.meta.keys() else None
        try:
            jsonbd = json.loads(rs.text) if isinstance(rs, requests.Response) and re.search('Page Not Found',rs.text) == None else None
        except:
            jsonbd = None

        pipleitem['S0'] = response.meta['id']
        pipleitem['S1'] = response.url
        pipleitem['S2'] = response.css('#source_baidu::text').extract_first()
        pipleitem['S3a'] = '文章评论类'
        pipleitem['S3d'] = helper.list2str(response.xpath('string(//div[@class="pos-mark"])').extract())
        pipleitem['S4'] = response.css('title::text').extract_first()
        pipleitem['S5'] = helper.get_localtimestamp()
        pipleitem['S6'] = response.meta['date']
        pipleitem['S7'] = '太平洋汽车APP'
        pipleitem['S9'] = '1'
        pipleitem['S10'] = None
        pipleitem['S11'] = None
        pipleitem['S12'] = jsonbd['commentRelNum'] if jsonbd != None and 'commentRelNum' in jsonbd.keys() else commentcount
        pipleitem['S13'] = None
        pipleitem['ID'] = response.meta['id']
        pipleitem['G1'] = response.css('#author_baidu a::text').extract_first()
        pipleitem['Q1'] = helper.list2str(response.xpath('string(//div[@class="artText clearfix"])').extract())

        return pipleitem
