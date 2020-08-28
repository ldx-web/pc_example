# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JuejinItem(scrapy.Item):
    # define the fields for your item here like:
    user_id = scrapy.Field()
    title = scrapy.Field()
    mark_content = scrapy.Field()
    user_name = scrapy.Field()
    description = scrapy.Field()
    got_view_count = scrapy.Field()
    category_name = scrapy.Field()
    tag_name = scrapy.Field()
    concern_user_count = scrapy.Field()
    ctime = scrapy.Field()


    pass
