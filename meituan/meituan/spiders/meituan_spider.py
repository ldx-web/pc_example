# -*- coding: utf-8 -*-
import scrapy
import json

from meituan.items import MeituanItem
from meituan.pipelines import mysqlPipeline


# data ={'page': {'pageNo':1,'pageSize':20}}

HEADERS = {
    'Content-Type': 'application/json',
}
class MeituanSpiderSpider(scrapy.Spider):
    name = 'meituan_spider'
    allowed_domains = ['zhaopin.meituan.com']
    # start_urls = ['https://zhaopin.meituan.com/api/jobList/getJobList']


    def start_requests(self):
        urls = 'https://zhaopin.meituan.com/api/jobList/getJobList'
        #设置抓取数量
        for pagenum in range(1, 2):
            #因为是post请求，所以必须有data
            data = {'page': {'pageNo': pagenum, 'pageSize': 20}}
            #定义请求方式
            yield scrapy.FormRequest(urls, callback=self.parse, method='POST', headers=HEADERS, body=json.dumps(data))

    def parse(self, response):
        all_info = json.loads(response.body)
        # print(all_info)
        dataList = all_info['data']
        # print(dataList)
        jobList = dataList['jobList']
        # print(jobList)
        for job in jobList:
            jobUnionId = job['jobUnionId']
            url = 'https://zhaopin.meituan.com/api/jobDetail/getJobDetail' + '/' + str(jobUnionId)
            yield scrapy.Request(url, callback=self.parse_detail, method='POST', headers=HEADERS)

    def parse_detail(self, response):
        get_info = json.loads(response.body)
        datas = get_info['data']

        title = datas['name']
        cityList = datas['cityList'][0]
        jobUnionId = datas['jobUnionId']
        desc_info = datas['desc'].replace('\n','')

        item = MeituanItem()
        item['title'] = title
        item['cityList'] = cityList
        item['jobUnionId'] = jobUnionId
        item['desc_info'] = desc_info
        yield item
        # print(len(item['name']))

        pass
