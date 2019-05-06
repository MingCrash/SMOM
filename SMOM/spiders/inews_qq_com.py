# -*- coding: utf-8 -*-
import re
import json
import scrapy
import requests
from SMOM import helper
from SMOM.items import SmomItem
from scrapy.http import Request

class InewsQqComSpider(scrapy.Spider):
    name = 'inews.qq.com'

    entry_point = {
        '汽车': 'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_auto&page=1&channelPosition=12&rtAd=1&devid=1099ffec2ca12181&qimei=1099ffec2ca12181&uid=1099ffec2ca12181&appver=27_android_5.7.90',
        # '推荐': 'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_recommend&page=1&channelPosition=2&rtAd=1&devid=1099ffec2ca12181&qimei=1099ffec2ca12181&uid=1099ffec2ca12181&appver=27_android_5.7.90',
        # '国际': 'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_world&page=1&channelPosition=9&rtAd=1&devid=1099ffec2ca12181&qimei=1099ffec2ca12181&uid=1099ffec2ca12181&appver=27_android_5.7.90',
        # '财经': 'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_finance&page=1&channelPosition=11&rtAd=1&devid=1099ffec2ca12181&qimei=1099ffec2ca12181&uid=1099ffec2ca12181&appver=27_android_5.7.90',
        # '新时代': 'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_19&page=1&channelPosition=16&rtAd=1&devid=1099ffec2ca12181&qimei=1099ffec2ca12181&uid=1099ffec2ca12181&appver=27_android_5.7.90',
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
        if len(jsonbd['newslist']) == 0: return
        for item in jsonbd['newslist']:
            if 'id' not in item.keys() or len(item['id']) == 0: continue
            url = 'https://r.inews.qq.com/getSimpleNews?id={}&chlid=news_news_top&devid=1099ffec2ca12181&qimei=1099ffec2ca12181&uid=1099ffec2ca12181&appver=27_android_5.7.90'.format(
                item['id'])
            date = item['time'] if 'time' in item.keys() else None
            source = item['source'] if 'source' in item.keys() else None
            title = item['title'] if 'title' in item.keys() else None
            comment_count = item['comments'] if 'comments' in item.keys() else 0
            likes_count = item['likeInfo'] if 'likeInfo' in item.keys() else 0
            read_count = item['readCount'] if 'readCount' in item.keys() else 0

            yield Request(url=url, callback=self.content_parse, headers=self.headers,
                          meta={'id': item['id'], 'comment_count': comment_count,
                                'likes_count': likes_count, 'read_count': read_count, 'title': title, 'date': date,
                                'source': source})

    def content_parse(self, response):
        date = response.meta['date'] if 'date' in response.meta.keys() else None
        # if date == None or len(date) == 0: return
        # try:
        #     if helper.compare_time(date, self.limittime) < 0: return
        # except:
        #     return

        jsonbd = json.loads(response.text)
        if jsonbd == None or len(jsonbd) == 0: return

        pipleitem = SmomItem()

        pipleitem['date'] = date
        pipleitem['id'] = response.meta['id'] if 'id' in response.meta.keys() else None
        pipleitem['url'] = response.url
        pipleitem['title'] = response.meta['title'] if 'title' in response.meta.keys() else None
        pipleitem['source'] = response.meta['source'] if 'source' in response.meta.keys() else None
        pipleitem['editor'] = jsonbd['content']['cms_editor'] if 'cms_editor' in jsonbd['content'].keys() else None
        pipleitem['content'] = helper.list2str(re.findall('>(.*?)<', jsonbd['content']['text'])) if 'text' in jsonbd[
            'content'].keys() else None

        imglist = []
        videolist = []
        if 'attribute' in jsonbd.keys() and len(jsonbd['attribute']) != 0:
            for item in jsonbd['attribute'].keys():
                if re.search('VIDEO', item):
                    videolist.append(jsonbd['attribute'][item]['playurl'])
                if re.search('IMG', item):
                    imglist.append(jsonbd['attribute'][item]['url'])

        pipleitem['image_urls'] = helper.list2str(imglist)
        pipleitem['video_urls'] = helper.list2str(videolist)
        pipleitem['share'] = None
        pipleitem['like'] = response.meta['likes_count'] if 'likes_count' in response.meta.keys() else None
        pipleitem['dislike'] = None
        pipleitem['views'] = response.meta['read_count'] if 'read_count' in response.meta.keys() else None
        pipleitem['comment'] = response.meta['comment_count'] if 'comment_count' in response.meta.keys() else None
        pipleitem['crawl_time'] = helper.get_localtimestamp()

        return pipleitem