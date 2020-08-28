# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MeituanItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    cityList = scrapy.Field()
    jobUnionId = scrapy.Field()
    desc_info = scrapy.Field()
    pass
