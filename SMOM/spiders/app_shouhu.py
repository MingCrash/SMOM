# -*- coding: utf-8 -*-
import re
import json
import scrapy
from SMOM import helper
from SMOM.items import SmomItem
from scrapy.http import Request

# '要闻':'http://v2.sohu.com/integration-api/mix/region/90?secureScore=50&page=1&size=50&mpId=0&adapter=default&channel=8',
# '财经':'http://v2.sohu.com/integration-api/mix/region/94?secureScore=50&page=1&size=50&mpId=0&adapter=default&channel=15',
# '军事':'http://v2.sohu.com/integration-api/mix/region/91?secureScore=50&page=1&size=50&mpId=0&adapter=default&channel=10',
# '科技':'http://v2.sohu.com/integration-api/mix/region/101?secureScore=50&page=1&size=50&mpId=0&adapter=default&channel=30',
# '专题':'http://v2.sohu.com/integration-api/mix/region/4653?size=50',
# comment# 'http://apiv2.sohu.com/api/comment/count?client_id=cyqemw6s1&topic_source_id=309925722|mp_309925722'
# views# 'http://v2.sohu.com/public-api/articles/310314477/pv'

class AppShouhuSpider(scrapy.Spider):
    name = 'app.shouhu'
    entry_point = {
        # '新闻': 'https://api.k.sohu.com/api/channel/v6/news.go?p1=NjUwOTMxNTExMjU1NjczNjUzOA%3D%3D&channelId=960590&num=20&rt=json&net=wifi&from=channel&apiVersion=42&isMixStream=2',
        # '推荐': 'https://api.k.sohu.com/api/channel/v6/news.go?p1=NjUwOTMxNTExMjU1NjczNjUzOA%3D%3D&channelId=13557&num=20&rt=json&net=wifi&from=channel&apiVersion=42&isMixStream=2',
        # '头条': 'https://api.k.sohu.com/api/channel/v6/news.go?p1=NjUwOTMxNTExMjU1NjczNjUzOA%3D%3D&channelId=1&num=20&rt=json&net=wifi&from=channel&apiVersion=42&isMixStream=2'
        '汽车': 'https://api.k.sohu.com/api/channel/v6/news.go?p1=NjUwOTMxNTExMjU1NjczNjUzOA%3D%3D&channelId=11&num=20&rt=json&net=wifi&from=channel&apiVersion=42&isMixStream=2'
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip',  # 只要gzip的压缩格式
        'accept-language': 'zh-CN,zh;q=0.9',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
    }

    def start_requests(self):
        for key in self.entry_point.keys():
            yield Request(url=self.entry_point[key], callback=self.parse, headers=self.headers,dont_filter=True)

    def parse(self, response):
        itemlist = []
        jsonbd = json.loads(response.text)
        if len(jsonbd['recommendArticles']) == 0: return
        for item in jsonbd['recommendArticles']:
            itemlist.append(item)
        for item in jsonbd['topArticles']:
            itemlist.append(item)
        for item in itemlist:
            if 'newsId' not in item.keys(): continue
            commentNum = item['commentNum'] if 'commentNum' in item.keys() else None
            readCount = item['readCount'] if 'readCount' in item.keys() else None
            # mediaName = item['mediaName'] if 'mediaName' in item.keys()  else None
            url = 'https://api.k.sohu.com/api/news/v5/article.go?newsId={}&channelId=1&p1=NjUwOTMxNTExMjU1NjczNjUzOA%3D%3D&rt=json'.format(item['newsId'])
            yield Request(url=url, callback=self.content_parse, headers=self.headers,meta={'commentNum': commentNum, 'readCount': readCount})


    def content_parse(self, response):
        jsonbd = json.loads(response.text)
        pipleitem = SmomItem()

        content = jsonbd['content'] if 'content' in jsonbd.keys() else None

        pipleitem['S0'] = jsonbd['newsId'] if 'newsId' in jsonbd.keys() else None
        pipleitem['S1'] = response.url
        pipleitem['S2'] = jsonbd['media']['mediaName'] if 'media' in jsonbd.keys() else None
        pipleitem['S3a'] = '文章评论类'
        pipleitem['S3d'] = None
        pipleitem['S4'] = jsonbd['title'] if 'title' in jsonbd.keys() else None
        pipleitem['S5'] = helper.get_localtimestamp()
        pipleitem['S6'] = jsonbd['time'] if 'time' in jsonbd.keys() and len(jsonbd['time']) != 0 else None
        pipleitem['S7'] = '搜狐新闻APP'
        pipleitem['S9'] = '1'
        pipleitem['S10'] = None
        pipleitem['S11'] = response.meta['readCount']
        pipleitem['S12'] = response.meta['commentNum']
        pipleitem['S13'] = None
        pipleitem['ID'] = jsonbd['newsId'] if 'newsId' in jsonbd.keys() else None
        pipleitem['G1'] = None
        pipleitem['Q1'] = helper.list2str(re.findall('>(.*?)<', content)) if content != None else None

        # imagelist = []
        # for i in jsonbd['photos']:
        #     if i['pic'] != None and len(i['pic']) != 0:
        #         imagelist.append(i['pic'])
        # pipleitem['image_urls'] = helper.list2str(imagelist)
        # pipleitem['video_urls'] = None

        return pipleitem
