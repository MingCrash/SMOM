# -*- coding: utf-8 -*-
import re
import json
import scrapy
import requests
from SMOM import helper
from SMOM.items import SmomItem
from scrapy.http import Request
from pyquery import PyQuery as pq

# ZAKER新闻APP
class InewsQqComSpider(scrapy.Spider):
    name = 'myzaker.com'

    # entry_point = {
    #     '汽车': 'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_auto&page=1&channelPosition=12&rtAd=1&devid=1099ffec2ca12181&qimei=1099ffec2ca12181&uid=1099ffec2ca12181&appver=27_android_5.7.90',
    #     # '推荐': 'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_recommend&page=1&channelPosition=2&rtAd=1&devid=1099ffec2ca12181&qimei=1099ffec2ca12181&uid=1099ffec2ca12181&appver=27_android_5.7.90',
    #     # '国际': 'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_world&page=1&channelPosition=9&rtAd=1&devid=1099ffec2ca12181&qimei=1099ffec2ca12181&uid=1099ffec2ca12181&appver=27_android_5.7.90',
    #     # '财经': 'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_finance&page=1&channelPosition=11&rtAd=1&devid=1099ffec2ca12181&qimei=1099ffec2ca12181&uid=1099ffec2ca12181&appver=27_android_5.7.90',
    #     # '新时代': 'https://r.inews.qq.com/getQQNewsUnreadList?chlid=news_news_19&page=1&channelPosition=16&rtAd=1&devid=1099ffec2ca12181&qimei=1099ffec2ca12181&uid=1099ffec2ca12181&appver=27_android_5.7.90',
    # }
    url = 'http://www.myzaker.com/news/next_new.php?f=myzaker_com&url=http%3A%2F%2Fiphone.myzaker.com%2Fzaker%2Fblog2news.php%3Fapp_id%3D7%26since_date%3D1556967501%26nt%3D1%26next_aticle_id%3D5ccf7a357f780bd90f00001c%26_appid%3Diphone%26opage%3D3%26otimestamp%3D173%26from%3D%26top_tab_id%3D12183%26_version%3D6.5&_version=6.5'

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip',  # 只要gzip的压缩格式
        'accept-language': 'zh-CN,zh;q=0.9',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
    }

    def start_requests(self):

        yield Request(url=self.url, callback=self.parse, headers=self.headers, dont_filter=True)

    def parse(self, response):
        jsonbd = json.loads(response.text)
        if len(jsonbd['data']) == 0 : return
        for item in jsonbd['data']['article']:
            if  'href' not in  item.keys() or len(item['href']) == 0:continue

            url = 'http:'+ item['href']
            ID = str(item['href']).replace('//www.myzaker.com/article/','').replace('/','')
            title = item['title'] if 'title' in item.keys() else None

            yield Request(url=url, callback=self.content_parse, headers=self.headers,meta={'title': title,'ID':ID})

    def content_parse(self, response):

        doc = pq(response.text)
        if len(doc) == 0: return

        auther = doc('.auther').text()
        pub_time = doc('.time').text()
        content = doc('#content').text().replace('\n', '')

        pipleitem = SmomItem()

        pipleitem['S0'] =  None
        pipleitem['S1'] = response.url
        pipleitem['S2'] =  None
        pipleitem['S3a'] = '文章评论类'
        pipleitem['S3d'] = None
        pipleitem['S4'] = response.meta['title'] if 'title' in response.meta.keys() else None
        pipleitem['S5'] = helper.get_localtimestamp()
        pipleitem['S6'] = pub_time
        pipleitem['S7'] = 'ZAKER新闻APP'
        pipleitem['S9'] = '1'
        pipleitem['S10'] = None
        pipleitem['S11'] = None
        pipleitem['S12'] =  None
        pipleitem['S13'] = None
        pipleitem['ID'] = response.meta['ID'] if 'ID' in response.meta.keys() else None
        pipleitem['G1'] = content
        pipleitem['Q1'] = auther

        return pipleitem