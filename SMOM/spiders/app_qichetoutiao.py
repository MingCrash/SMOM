# -*- coding: utf-8 -*-
import re
import json
import scrapy
from SMOM import helper
from SMOM.items import SmomItem
from scrapy.http import Request

class AppQichetoutiaoSpider(scrapy.Spider):
    name = 'app.qichetoutiao'
    entry_point = {
        '汽车': 'http://telepathy.kakamobi.com/api/open/v3/article/list.htm?_platform=android&_srv=t&_appName=pingxingzhijia&_product=%E5%B9%B3%E8%A1%8C%E4%B9%8B%E5%AE%B6&_vendor=huawei&_renyuan=YW&_version=3.3.8&_system=HONORDUA-AL00&_manufacturer=HUAWEI&_systemVersion=8.1.0&_device=DUA-AL00&_imei=A000009114F247&_productCategory=pingxingzhijia&_operator=&_androidId=a7caa62cf0f71917&_mac=b8%3A94%3A36%3A14%3Ab3%3A14&_appUser=3c7748a0e720419990030289b215aaae&_pkgName=cn.mucang.android.parallelvehicle&_screenDpi=2.0&_screenWidth=720&_screenHeight=1356&_network=wifi&_launch=1&_firstTime=2019-05-08%2015%3A25%3A50&_apiLevel=27&_userCity=&_p=&_gpsType=gcj&_cityName=%E5%B9%BF%E5%B7%9E%E5%B8%82&_cityCode=440100&_gpsCity=440100&_longitude=113.315359&_latitude=23.132574&_ipCity=440100&_j=1.0&_webviewVersion=4.7&_mcProtocol=4.1&ttVersion=5&_r=434cd2b1b3d94f4e9452b376b0ee3ddb&ttDna=0&channelId=218&page=1&limit=20&sign=b34cd2277db888c76c4e2a40061cb5c401'
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
            yield Request(url=self.entry_point[key], callback=self.parse, dont_filter=True)

    def parse(self, response):
        jsonbd = json.loads(response.text)
        if len(jsonbd['data']['itemList']) == 0: return
        for item in jsonbd['data']['itemList']:
            url = item['content']['shareLink'] if 'shareLink' in item['content'].keys() else None
            id = item['articleId'] if 'articleId' in item.keys() else None
            date = item['content']['publishTime'] if 'publishTime' in item['content'].keys() else None
            commentCount = item['content']['commentCount'] if 'commentCount' in item['content'].keys() else None
            author = item['content']['author'] if 'author' in item['content'].keys() else None
            dislike = item['content']['downCount'] if 'downCount' in item['content'].keys() else None
            like = item['content']['upCount'] if 'upCount' in item['content'].keys() else None
            source = item['content']['source'] if 'source' in item['content'].keys() else None
            yield Request(url=url, callback=self.content_parse,
                          meta={'date': date, 'id': id, 'commentCount': commentCount,
                                'author': author, 'dislike': dislike, 'like': like, 'source': source})

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
        pipleitem['S7'] = '车友头条APP'
        pipleitem['S9'] = '1'
        pipleitem['S10'] = None
        pipleitem['S11'] = None
        pipleitem['S12'] = response.meta['commentCount']
        pipleitem['S13'] = response.meta['like']
        pipleitem['ID'] = response.meta['id']
        pipleitem['G1'] = response.meta['author']
        pipleitem['Q1'] = helper.list2str(response.xpath("string(//div[contains(@class,'article-detail')])").extract())

        return pipleitem
