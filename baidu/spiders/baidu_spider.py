# -*- coding: utf-8 -*-
import scrapy
import json
from baidu.items import BaiduItem
import re

class BaiduSpiderSpider(scrapy.Spider):
    name = 'baidu_spider'
    allowed_domains = ['talent.baidu.com']
    # start_urls = ['https://talent.baidu.com/baidu/web/httpservice/getPostList?workPlace=0%2F4%2F7%2F9&recruitType=2&pageSize=10&curPage=1&keyWord=&_=1594180148768']
    # Base_url ='https://talent.baidu.com/baidu/web/httpservice/getPostList?workPlace=0%2F4%2F7%2F9&recruitType=2&pageSize=10&keyWord=&_=1594180364837'
    # small_url =
    def start_requests(self):
        for curPage in range(1, 151):
            url = 'https://talent.baidu.com/baidu/web/httpservice/getPostList?workPlace=0%2F4%2F7%2F9&recruitType=2&pageSize=10&keyWord=&_=1594180364837&curPage={}'.format(curPage)
            yield scrapy.Request(url, callback=self.parse)
            # print(url)
    def parse(self, response):
        # print(response.body)
        all_info = json.loads(response.body)
        # print(all_info)
        post_Lists = all_info['postList']
        # print(post_Lists)

        for post_List in post_Lists:
            # print(post_List)
            item = BaiduItem()

            name = post_List['name'].strip()
            print(name)
            workPlace = post_List['workPlace']
            workContent = post_List['workContent'].replace("\r",'')
            workContent = re.sub('<br>', ' ', workContent)
            # print(workContent)
            orgName = post_List['orgName']
            serviceCondition = post_List['serviceCondition']
            postId = post_List['postId']

            item['name'] = name
            print(name)
            item['workPlace'] = workPlace
            print(workPlace)
            item['workContent'] = workContent
            print(workContent)
            item['orgName'] = orgName
            print(orgName)
            item['serviceCondition'] = serviceCondition
            print(serviceCondition)
            item['postId'] = postId
            print(postId)
            yield item
            # print(name)
        pass



