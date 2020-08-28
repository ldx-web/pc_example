# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UiItem(scrapy.Item):
    # define the fields for your item here like:
    big_title = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()
    small_title = scrapy.Field()
    ds = scrapy.Field()

    pass
