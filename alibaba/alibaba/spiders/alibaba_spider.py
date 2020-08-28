# -*- coding: utf-8 -*-
import scrapy
import json

from alibaba.items import AlibabaItem
# from urllib import parse

form_Data = {
    'PageSize': '10',
}


class AlibabaSpiderSpider(scrapy.Spider):
    name = 'alibaba_spider'
    allowed_domains = ['job.alibaba.com']
    start_urls = ['https://job.alibaba.com/zhaopin/socialPositionList/doList.json?pageSize=10&t=0.4758632284490447']

    # def start_requests(self):
    #     url = 'https://job.alibaba.com/zhaopin/socialPositionList/doList.json?'
    #     yield scrapy.Request(url, callback=self.parse)
    #     pass

    def parse(self, response):
        pageIndex = response.meta.get('pageIndex')
        if not pageIndex:
            pageIndex = 2
        # print(response.text)
        all_info = json.loads(response.body)
        # print(all_info)
        returnValue_List = all_info['returnValue']
        datas_List = returnValue_List['datas']

        for datas in datas_List:
            item = AlibabaItem()

            id = datas['id']
            print(id)
            name = datas['name']
            print(name)
            requirement = datas['requirement']
            print(requirement)
            description = datas['description']
            print(description)
            workLocation = datas['workLocation']
            print(workLocation)

            item['id'] = id
            item['name'] = name
            item['requirement'] = requirement
            item['description'] = description
            item['workLocation'] = workLocation
            url = 'https://job.alibaba.com/zhaopin/socialPositionList/doList.json'
            form_Data['pageIndex'] = str(pageIndex)
            if pageIndex < 20:
                yield scrapy.Request(url, callback=self.parse, method='POST', body=json.dumps(form_Data), meta={'pageIndex':pageIndex+1})

            # scrapy.FormRequest
            yield item
            # print(item)
        pass
