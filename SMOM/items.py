# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SmomItem(scrapy.Item):
    # id = scrapy.Field()
    # url = scrapy.Field()
    # title = scrapy.Field()
    # date = scrapy.Field()
    # source = scrapy.Field()
    # editor = scrapy.Field()
    # content = scrapy.Field()
    # views = scrapy.Field()
    # image_urls = scrapy.Field()
    # video_urls = scrapy.Field()
    # share = scrapy.Field()
    # like = scrapy.Field()
    # dislike = scrapy.Field()
    # comment = scrapy.Field()
    # crawl_time = scrapy.Field()
    S0 = scrapy.Field()  # S0 第一层的总ID
    S1 = scrapy.Field()  # S1 url 链接
    S2 = scrapy.Field()  # S2 source 意见的来源
    S3a = scrapy.Field()  # S3a type 文章评论类
    S3d = scrapy.Field()  # S3d natvigate 导航条
    S4 = scrapy.Field()  # S4 title 标题
    S5 = scrapy.Field()  # S5 crawl_time 抓取时间
    S6 = scrapy.Field()  # S6  date  日期
    S7 = scrapy.Field()  # S7 platform 平台 PC&APP
    S9 = scrapy.Field()  # S9 level 层级
    S10 = scrapy.Field()  # S10 replylevel 该意见回复的层数
    S11 = scrapy.Field()  # S11  views 访问量
    S12 = scrapy.Field()  # S12  comments 该意见被回复的数量
    S13 = scrapy.Field()  # S13  like 点赞数
    ID = scrapy.Field()  #
    Q1 = scrapy.Field()  # Q1 content 内容
    G1 = scrapy.Field()  # G1 editor 编辑者
