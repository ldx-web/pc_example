# -*- coding: utf-8 -*-
import scrapy
import json
from ximalaya.items import XimalayaItem

class XimalayaSpiderSpider(scrapy.Spider):
    name = 'ximalaya_spider'
    allowed_domains = ['jobs.ximalaya.com']

    def start_requests(self):
        for offset in range(0, 45, 15):
        # offset = 0
        # offset += 15
            start_urls = 'http://jobs.ximalaya.com/api/apply/jobs?limit=15&offset={}&&zhinengId=21943&siteId=7257&orgId=himalaya&site=social&needStat=true'.format(offset)
            yield scrapy.Request(url=start_urls, callback=self.parse ,method='GET')
    def parse(self, response):
        all_info = json.loads(response.body)
        # print(all_info)
        jobs = all_info['jobs']
        # print(jobs)
        for job in jobs:
            id = job['id']
            url = 'http://jobs.ximalaya.com/api/apply/himalaya/job/'+str(id)+'?site=social&orgId=himalaya&siteId=7257'
            # print(url)
            yield scrapy.Request(url,callback=self.parse_detail)

    def parse_detail(self,response):
        get_info = json.loads(response.body)
        # print(get_info)
        title = get_info['title']
        # print(title)
        jobDescription = get_info['jobDescription']
        id = get_info['id']
        locations = get_info['locations']
        # items = []
        for location in locations:

            cityId = location['cityId']
            address = location['address']
            # items.append(cityId)
            # items.append(address)
            item = XimalayaItem()

            item['id'] = id
            item['title'] = title
            item['jobDescription'] = jobDescription
            # item['locations'] = locations
            item['cityId'] = cityId
            item['address'] = address
            yield item
            print(item)



        pass
