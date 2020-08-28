# -*- coding: utf-8 -*-

# import sys
# import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import scrapy
from scrapy import selector
from scrapy import Request
import requests
import re
import json
from urllib import parse
# from PycharmProjects.ArticleSpider.ArticleSpider.items import ArticlespiderItem
from .. items import ArticlespiderItem
from .. spiders.utils import common
from .. pipelines import ArticleSpiderPipeline

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['https://news.cnblogs.com/']

    def parse(self, response):
        # urls = response.xpath("//div[@class='content']/h2[@class='news_entry']/a/@href").extract_first("")
        post_nodes = response.css("#news_list .news_block")[1:31]
        for post_node in post_nodes:
            image_url = 'https:' + post_node.css(".entry_summary a img::attr(src)").extract_first("")
            post_url = post_node.css("h2.news_entry a::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url":image_url},callback=self.parse_detail)

        #提取下一页并交给scrapy进行下载
        #法一css选择器
        #
        next_url = response.css("div.pager a:last-child::text").extract_first("")
        if next_url == "Next >":
            next_url = response.css("div.pager a:last-child::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

        # #法二：xpath
        # next_url = response.xpath("//a[contains(text(),'Next >')]/@href").extract_first("")
        #yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

#详情页面解析
    def parse_detail(self, response):
        match_re = re.match(".*?(\d+)" , response.url)
        if match_re:
            post_id = match_re.group(1)
            #先定义一个item,然后进行赋值，见此函数最后
            article_item = ArticlespiderItem()
            title = response.css("#news_title a::text").extract_first("")
            create_date = response.css("#news_info span.time::text").extract_first("")
            match_re = re.match(".*?(\d+.*)",create_date)
            if match_re:
                create_date = match_re.group(1)
            # content = None
            # tags = None
            try:
               # content = response.xpath("//div[@id='news_content']").extract()[0]
               contents = response.xpath("//div[@id='news_content']//text()").extract()
               content = ','.join(contents).replace(',', '').replace('"', '').strip()
               # print(content)
               tag_list = response.css(".news_tags a::text").extract()
               tags = ','.join(tag_list)
            except Exception as e:
                content = ''         #当content、tags值为空时,返回一个错误提醒
                tags = ''
                import logging
                logging.error("error :{}".format(e))



            # post_id =match_re.group(1)
            # html = requests.get(parse.urljoin(response.url,"/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)))

           #一定要确保此时key中的值在items.py中
            article_item['title'] = title
            article_item['create_date'] = create_date
            article_item['content'] = content
            article_item['tags'] = tags
            article_item['url'] = response.url

            if response.meta.get("front_image_url", ""):
                 article_item['front_image_url'] = [response.meta.get("front_image_url", "")]
            else:
                article_item['front_image_url'] = []

            yield Request(url=parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)),
                          meta={"article_item": article_item}, callback=self.parse_nums)

    def parse_nums(self, response):
        j_data = json.loads(response.text)
        article_item = response.meta.get("article_item", "")

        praise_nums = j_data["DiggCount"]
        fav_nums = j_data["TotalView"]
        comment_nums = j_data["CommentCount"]


        article_item["praise_nums"] = praise_nums
        article_item["fav_nums"] = fav_nums
        article_item["comment_nums"] = comment_nums
        article_item["url_object_id"] = common.get_md5(article_item['url'])
        yield article_item
        pass

