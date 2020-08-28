# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

##对应"csdn_spider.py"文件的item项
class CsdnItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    Author_name = scrapy.Field()
    publish_time = scrapy.Field()
    read_number = scrapy.Field()
    Collection = scrapy.Field()
    Classification = scrapy.Field()
    Article_Tags = scrapy.Field()
    url = scrapy.Field()

#对应"csdn.py"文件的item项
class CsdnItem2(scrapy.Item):
     # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    user_name = scrapy.Field()
    nickname = scrapy.Field()
    comments = scrapy.Field()
    ds = scrapy.Field()
    # tags = scrapy.Field()
    id = scrapy.Field()
    tp = scrapy.Field()
    shown_offset = scrapy.Field()


