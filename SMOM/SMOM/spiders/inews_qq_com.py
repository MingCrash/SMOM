# -*- coding: utf-8 -*-
import scrapy


class InewsQqComSpider(scrapy.Spider):
    name = 'inews.qq.com'
    allowed_domains = ['inews.qq.com']
    start_urls = ['http://inews.qq.com/']

    def parse(self, response):
        pass
