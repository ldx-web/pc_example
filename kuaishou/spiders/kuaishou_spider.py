# -*- coding: utf-8 -*-
import scrapy
import json

from kuaishou.items import KuaishouItem

HEADERS={
    'Cookie':'__secdyid=bc4323a00bfd1805e62e13ebeb35ff036fcb0442e57c5ef9021594618243; accessproxy_session=948703c7-a740-400e-86b9-f4cb75b330f8; _did=web_2917694672DEE2D3',
    'Host':'zhaopin.kuaishou.cn',
    'Referer':'https://zhaopin.kuaishou.cn/recruit/e/',
}

class KuaishouSpiderSpider(scrapy.Spider):
    name = 'kuaishou_spider'
    allowed_domains = ['zhaopin.kuaishou.cn']
    start_urls = ['https://zhaopin.kuaishou.cn/recruit/e/#/official/social/?pageNum=1']

    def start_requests(self):
        for i in range(1, 5):
            start_urls = 'https://zhaopin.kuaishou.cn/recruit/e/api/v1/open/positions/simple?pageNum={}&pageSize=10&recruitProject=socialr'.format(i)
            yield scrapy.Request(url=start_urls,callback=self.parse,method='GET',headers=HEADERS,encoding='utf-8')

    def parse(self, response):
        all_info = json.loads(response.body)
        # print(all_info)
        result = all_info['result']
        # print(result)
        list = result['list']
        # print(list)
        item = KuaishouItem()
        for info in list:
            id = info['id']
            # print(id)
            name = info['name']
            # print(name)
            description = info['description']
            # print(description)
            positionDemand = info['positionDemand']
            # print(positionDemand)
            workLocationCode = info['workLocationCode']
            # print(workLocationCode)

            item['id'] = id
            item['name'] = name
            item['description'] = description
            item['positionDemand'] = positionDemand
            item['workLocationCode'] = workLocationCode

            yield item


        pass
