# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class question_ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    question_id = scrapy.Field()
    question_name = scrapy.Field()
    q_headline = scrapy.Field()
    title = scrapy.Field()
    q_content = scrapy.Field()
    q_excerpt = scrapy.Field()
    q_excerpt_new = scrapy.Field()
    answer_count = scrapy.Field()
    c_count = scrapy.Field()
    created_time = scrapy.Field()
    updated_time = scrapy.Field()
    visited_count = scrapy.Field()
    answer_id = scrapy.Field()


class answer_ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    Rely_q_title = scrapy.Field()
    author_name = scrapy.Field()
    a_headline = scrapy.Field()
    a_excerpt = scrapy.Field()
    a_content = scrapy.Field()
    created_time = scrapy.Field()
    updated_time = scrapy.Field()
    comment_count = scrapy.Field()
