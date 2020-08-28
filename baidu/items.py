# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    workContent = scrapy.Field()
    orgName = scrapy.Field()
    serviceCondition = scrapy.Field()
    workPlace = scrapy.Field()
    postId = scrapy.Field()
    pass