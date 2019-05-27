# -*- coding: utf-8 -*-
import re
import json
import scrapy
from SMOM import helper
from SMOM.items import SmomItem
from scrapy.http import Request

# #要闻
# 'http://c.m.163.com/dlist/article/dynamic?{}'
# par = {
#     'from':'T1467284926140',
#     'offset':'0',
#     'size':'20',
#     'fn':'1',
#     'LastStdTime':'0',
#     'passport':'',
#     'devId':'UtQj6VTqfPTNdHOhqXgx4w%3D%3D',
#     # 'lat':'nEob1URk2zlHby%2FZRQvN9A%3D%3D',
#     # 'lon':'gnbXwKYIXyBHzMQxFSRSxQ%3D%3D',
#     'version':'54.6',
#     'net':'wifi',
#     # 'ts':'1556091859',
#     # 'sign':'uqtTuIyP5oD9HzgvKRKuccyK81gp7LyGqaF2wqK%2F62B48ErR02zJ6%2FKXOnxX046I',
#     'encryption':'1',
#     'canal':'miliao_news',
#     # 'mac':'I0hRorjreoVkNP82fbwMpUn4xdWy8S3keUAmEYPgEfc%3D',
#     # 'open':'',
#     # 'openpath':''
# }
#
# #推荐
# 'http://c.m.163.com/recommend/getSubDocPic?{}'
# par2 = {
#     # 'tid':'T1348647909107',
#     'from':'toutiao',
#     'offset':'0',
#     'size':'10',
#     'fn':'3',
#     'LastStdTime':'0',
#     'spestr':'reader_expert_1',
#     # 'prog':'bjrec_toutiaotoutiao-1100000423-1200000585-1110000662-1111000458-1111000774-1111000698-1111000797-1111000478-1111000673-1200000742-1200000685-1200000604-1111000619-1200000724-1111000438-1111000834-1111000592-1111000394-1111000589-1200000673-1111000545-1200000594-1111000543-1200000710-1200000677-1200000632-1111000289-1111000388-1111000242-1200000576-1200000652-1111000828-1111000729-1200000734-1111000629-1200000678-1111000626-1111000701-1111000548e',
#     'passport':'',
#     'devId':'UtQj6VTqfPTNdHOhqXgx4w%3D%3D',
#     # 'lat':'nEob1URk2zlHby%2FZRQvN9A%3D%3D',
#     # 'lon':'gnbXwKYIXyBHzMQxFSRSxQ%3D%3D',
#     'version':'54.6',
#     'net':'wifi',
#     # 'ts':'1556095657',
#     # 'sign':'QKcKkwKuzkBU7u6u%2B67TXuGGUbk990WpvAlMfaMcqUx48ErR02zJ6%2FKXOnxX046I',
#     'encryption':'1',
#     'canal':'miliao_news',
#     # 'mac':'I0hRorjreoVkNP82fbwMpUn4xdWy8S3keUAmEYPgEfc%3D',
#     # 'open':'',
#     # 'openpath':''
# }
# 不需要headers

# 'http://c.m.163.com/nc/article/list/T1414142214384/{}-20.html'
# 需要headers

# 网易新闻APP
class AppNeteaseSpider(scrapy.Spider):
    name = 'app.netease'
    entry_point = {
        # '要闻': 'http://c.m.163.com/dlist/article/dynamic?from=T1467284926140&offset=0&size=20&fn=1&LastStdTime=0&passport=&devId=UtQj6VTqfPTNdHOhqXgx4w%3D%3D&version=54.6&net=wifi&encryption=1&canal=miliao_news',
        # '头条': 'http://c.m.163.com/recommend/getSubDocPic?from=T1467284926140&offset=0&size=20&fn=1&LastStdTime=0&passport=&devId=UtQj6VTqfPTNdHOhqXgx4w%3D%3D&version=54.6&net=wifi&encryption=1&canal=miliao_news',
        # '财经': 'http://c.m.163.com/dlist/article/dynamic?from=T1348648756099&offset=0&size=10&fn=1&LastStdTime=0&passport=&devId=UtQj6VTqfPTNdHOhqXgx4w%3D%3D&version=55.1&net=wifi&encryption=1&canal=miliao_news&open=&openpath=',
        # '新时代': 'http://c.m.163.com/nc/article/list/T1414142214384/0-20.html'
        '汽车': 'http://c.m.163.com/nc/auto/districtcode/list/440600/{}-20.html'
    }

    headers = {
        'User-Agent': 'NewsApp/54.6 Android/4.4.4 (Xiaomi/MI 3C)'
    }

    def start_requests(self):
        for key in self.entry_point.keys():
            for i in range(16):
                yield Request(url=self.entry_point[key].format(i*20), callback=self.parse, headers=self.headers,dont_filter=True)

    def parse(self, response):
        jsonbd = json.loads(response.text)
        if len(jsonbd['list']) == 0: return
        for item in jsonbd['list']:
            if 'url_3w' not in item.keys() or len(item['url_3w']) == 0: continue
            url = item['url_3w']
            like = item['votecount'] if 'votecount' in item.keys() else None
            id = item['postid'] if 'postid' in item.keys() else None
            date = item['ptime'] if 'ptime' in item.keys() else None
            source = item['source'] if 'source' in item.keys() else None
            replyCount = item['replyCount'] if 'replyCount' in item.keys() else None
            yield Request(url=url, callback=self.content_parse, encoding='utf-8',
                          meta={'like': like, 'id': id, 'date': date, 'replyCount': replyCount, 'source': source})

    def content_parse(self, response):

        pipleitem = SmomItem()

        pipleitem['S0'] = response.meta['id']
        pipleitem['S1'] = response.url
        pipleitem['S2'] = response.meta['source']
        pipleitem['S3a'] = '文章评论类'
        pipleitem['S3d'] = helper.list2str(response.xpath('string(//div[@class="post_crumb"])').extract())
        pipleitem['S4'] = response.css('title::text').extract_first()
        pipleitem['S5'] = helper.get_localtimestamp()
        pipleitem['S6'] = response.meta['date']
        pipleitem['S7'] = '网易新闻APP'
        pipleitem['S9'] = '1'
        pipleitem['S10'] = None
        pipleitem['S11'] = None
        pipleitem['S12'] = response.meta['comment_count'] if 'comment_count' in response.meta.keys() else None
        pipleitem['S13'] = response.meta['replyCount']
        pipleitem['ID'] = response.meta['id']
        pipleitem['G1'] = None
        pipleitem['Q1'] = helper.list2str(response.xpath('string(//div[@id="endText"])').extract()).replace('\t','')

        # pipleitem['image_urls'] = helper.list2str(response.css('#endText img::attr(src)').extract())
        # pipleitem['video_urls'] = helper.list2str(response.css('#endText source::attr(src)').extract())

        return pipleitem
