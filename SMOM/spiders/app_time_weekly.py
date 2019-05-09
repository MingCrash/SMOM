# -*- coding: utf-8 -*-
import re
import json
import scrapy
from SMOM import helper
from SMOM.items import SmomItem
from scrapy.http import Request

# 时代财经APP
class AppTimeWeeklySpider(scrapy.Spider):
    name = 'app.time_weekly'

    entry_point = {
        '汽车': 'http://app.time-weekly.com/wamei/baseController/titan.htm?page=1&pageSize=100&specialId=e548fdc054f188670154f27474eb0037&channelType=0&token=&topicId=2c91219669b928c8016a2c40fd1e5cd1&userImei=A000009114F247&appMetaData=huawei&sessionCache=wfWmXF%2Fjhp%2BovKCYZ6JKZXzxqU%2FXJ%2Fjf'
    }

    headers = {
        'session': 'wfWmXF/jhp+ovKCYZ6JKZRHawHiWKm4ABk6yuoadWH1hjQrQ8wsQnc5CR8YM2f1X',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 8.1.0; DUA-AL00 Build/HONORDUA-AL00)',
        'Host': 'app.time-weekly.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Length': '0'
    }

    def start_requests(self):
        for key in self.entry_point.keys():
            yield Request(url=self.entry_point[key], callback=self.parse, headers=self.headers,dont_filter=True)

    def parse(self, response):
        jsonbd = json.loads(response.text)
        articleList = jsonbd['result']['articleList'] if 'result' in jsonbd.keys() and len(jsonbd['result']['articleList']) != 0 else None
        if articleList == None: return
        for item in articleList:
            if 'linkUrl' not in item.keys(): continue
            commentNum = item['commentCount'] if 'commentCount' in item.keys() else None
            likesCount = item['likesCount'] if 'likesCount' in item.keys() else None
            viewCount = item['viewCount'] if 'viewCount' in item.keys() else None
            editor = item['editor'] if 'editor' in item.keys() else None
            source = item['author'] if 'author' in item.keys() else None
            date = item['factTime'] if 'factTime' in item.keys() else None
            url = item['linkUrl']
            id = item['id'] if 'id' in item.keys() else None

            # print(id,url,date,author,editor,viewCount,likesCount,commentNum)
            yield Request(url=url, callback=self.content_parse, headers=self.headers,meta={'commentNum': commentNum, 'likesCount': likesCount, 'viewCount':viewCount,
                                                                                           'editor':editor, 'source':source, 'date':date, 'id':id})


    def content_parse(self, response):
        pipleitem = SmomItem()

        pipleitem['S0'] = response.meta['id']
        pipleitem['S1'] = response.url
        pipleitem['S2'] = response.meta['source']
        pipleitem['S3a'] = '文章评论类'
        pipleitem['S3d'] = None
        pipleitem['S4'] = response.css('title::text').extract_first()
        pipleitem['S5'] = helper.get_localtimestamp()
        pipleitem['S6'] = response.meta['date']
        pipleitem['S7'] = '时代财经APP'
        pipleitem['S9'] = '1'
        pipleitem['S10'] = None
        pipleitem['S11'] = response.meta['viewCount']
        pipleitem['S12'] = response.meta['commentNum']
        pipleitem['S13'] = response.meta['likesCount']
        pipleitem['ID'] = response.meta['id']
        pipleitem['G1'] = response.meta['editor']
        pipleitem['Q1'] = helper.list2str(response.xpath('string(//div[@id="js_content"])').extract())

        return pipleitem