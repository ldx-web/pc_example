# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,MapCompose,Join
from w3lib.html import remove_tags
import datetime
from Lagou.settings import SQL_DATETIME_FORMAT,SQL_DATE_FORMAT

# class LagouItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass
def remove_splash(value):
    #去掉城市的斜线
    return value.replace("/","")

def handle_jobaddr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip()!="查看地图"]
    return "".join(addr_list)
def remove_Space(value):
    return value.strip()


class LagouJobItemLoader(ItemLoader):
    default_output_processor = TakeFirst()     #output_processor = TakeFirst()只需要每个字段的一个值，将列表转换为字符串


class LagouJobItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field(
        input_processor=MapCompose(remove_splash)
    )
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_splash)
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(remove_splash)

    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(remove_splash)

    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags,handle_jobaddr),

    )
    company_name = scrapy.Field(
        input_processor=MapCompose(remove_Space)
    )
    company_url = scrapy.Field()
    tags = scrapy.Field(
        input_processor=Join(',')
    )
    crawl_time = scrapy.Field()

