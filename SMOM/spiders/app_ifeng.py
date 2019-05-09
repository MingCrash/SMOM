# -*- coding: utf-8 -*-
import re
import json
import scrapy
from SMOM import helper
from SMOM.items import SmomItem
from scrapy.http import Request

# 凤凰新闻APP
class AppIfengSpider(scrapy.Spider):
    name = 'app.ifeng'
    entry_point = {
        '汽车': 'https://api.iclient.ifeng.com/ClientNewsRegion?id=QC45,FOCUSQC45,SECNAVQC45&action=down&pullNum=1&choicename=&choicetype=null&gv=6.5.5&av=6.5.5&uid=A000009114F247&deviceid=A000009114F247&proid=ifengnews&os=android_27&df=androidphone&vt=5&screen=720x1356&publishid=6109&nw=wifi&loginid=&st=15571315182743&sn=a7fcf60b2589cafc87f1d232847dfee7'
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip',  # 只要gzip的压缩格式
        'accept-language': 'zh-CN,zh;q=0.9',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
    }

    def start_requests(self):
        for key in self.entry_point.keys():
            yield Request(url=self.entry_point[key], callback=self.parse, headers=self.headers, dont_filter=True)

    def parse(self, response):
        jsonbd = json.loads(response.text)
        if len(jsonbd[0]['item']) == 0: return
        for item in jsonbd[0]['item']:
            type = item['type'] if 'type' in item.keys() else None
            if type == None or type != 'doc': continue
            if 'link' not in item.keys() or len(item['link']['url']) == 0: continue
            url = item['link']['url']
            commentNum = item['commentsall'] if 'commentsall' in item.keys() else None
            yield Request(url=url, callback=self.content_parse, headers=self.headers,meta={'commentNum': commentNum})

    def content_parse(self, response):
        jsonbd = json.loads(response.text)
        if 'body' in jsonbd.keys():
            body = jsonbd['body']
        else:
            return

        pipleitem = SmomItem()

        content = body['text'] if 'text' in body.keys() else None

        pipleitem['S0'] = body['staticId'] if 'staticId' in body.keys() else None
        pipleitem['S1'] = response.url
        pipleitem['S2'] = body['source'] if 'source' in body.keys() else None
        pipleitem['S3a'] = '文章评论类'
        pipleitem['S3d'] = None
        pipleitem['S4'] = body['title'] if 'title' in body.keys() else None
        pipleitem['S5'] = helper.get_localtimestamp()
        pipleitem['S6'] = body['editTime'] if 'editTime' in body.keys() else None
        pipleitem['S7'] = '凤凰新闻APP'
        pipleitem['S9'] = '1'
        pipleitem['S10'] = None
        pipleitem['S11'] = None
        pipleitem['S12'] = response.meta['commentNum']
        pipleitem['S13'] = body['like_num'] if 'like_num' in body.keys() else None
        pipleitem['ID'] = body['staticId'] if 'staticId' in body.keys() else None
        pipleitem['G1'] = body['editorcode'] if 'editorcode' in body.keys() else None
        pipleitem['Q1'] = helper.list2str(re.findall('>(.*?)<', content)) if content != None else None

        return pipleitem

