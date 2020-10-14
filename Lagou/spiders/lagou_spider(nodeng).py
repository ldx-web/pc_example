# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
import time
import os
# from ..settings import BASE_DIR
from Lagou.settings import BASE_DIR
import pickle
from Lagou.items import LagouJobItemLoader,LagouJobItem
from Lagou.spiders.utils.common import get_md5
from datetime import datetime


HEADERS={
    'cookie':'',
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
}

class LagouSpiderSpider(CrawlSpider):
    name = 'lagou_spider'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    rules = (
        Rule(LinkExtractor(allow=('zhaopin/.*',)),follow=True),
        Rule(LinkExtractor(allow=('gongsi/j\d+.html',)),follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),

    )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True,headers=HEADERS)


    def parse_job(self, response):

        item_loader = LagouJobItemLoader(item=LagouJobItem(),response=response)

        item_loader.add_xpath("title","//div[@class='job-name']//h1/text()")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_xpath("salary","//dd[@class='job_request']/h3/span[1]/text()")
        item_loader.add_xpath("job_city","//dd[@class='job_request']/h3/span[2]/text()")
        item_loader.add_xpath("work_years","//dd[@class='job_request']/h3/span[3]/text()")
        item_loader.add_xpath("degree_need","//dd[@class='job_request']/h3/span[4]/text()")
        item_loader.add_xpath("job_type","//dd[@class='job_request']/h3/span[5]/text()")
        item_loader.add_xpath("publish_time","//p[@class='publish_time']/text()")
        item_loader.add_xpath("job_advantage","//dd[@class='job-advantage']//p/text()")
        item_loader.add_xpath("job_desc","//div[@class='job-detail']")
        item_loader.add_xpath("job_addr","//div[@class='work_addr']")
        item_loader.add_xpath("company_name","//div[@class='job_company_content']//em[@class='fl-cn']/text()")
        item_loader.add_xpath("company_url","//ul[@class='c_feature']//a/@href")
        item_loader.add_xpath("tags","//li[@class='labels']/text()")
        item_loader.add_value("crawl_time",datetime.now())


        job_item = item_loader.load_item()
        if job_item.get("title"):
            return job_item




