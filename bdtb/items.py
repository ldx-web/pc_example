# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BdtbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user_name = scrapy.Field()
    contents = scrapy.Field()
    time = scrapy.Field()
    tid = scrapy.Field()
    pid = scrapy.Field()


class ReplyBdtbItem(scrapy.Item):
    reply_name = scrapy.Field()
    By_reply_name = scrapy.Field()
    content_replied = scrapy.Field()
    replay_time = scrapy.Field()
