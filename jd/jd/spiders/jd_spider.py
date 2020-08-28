# -*- coding: utf-8 -*-
import scrapy
import json

from jd.items import JdItem

unicornHeader = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'CCC_SE=ADC_b0B7fAqlFxc8HkBLWTVBAxFnfgZW1IG1ppgBbmQWDAFSqaILXHB57i19FwrYGaf2bzVY2ChKdF02%2b9LBKPNl%2f8Pg'
              '%2bfSekgdxwSbm6yImGbBBbh9r2T61NY48ZkSOxR9UnZQ'
              '%2bW479R1QVJb9XfLaQcOdHK3rpk8qxJvps6WmY1AatWG7DLqhOtN7k3zV0M0UV%2fcGMS4L92xBZseUpUb'
              '%2bQgUhNx0BXn6qnkS65uvSjRLXt4wxlCH998kNnOmk2PSgy1mLxv%2fpFQNrTlQ1vG0L9wjbCjw47ce3OSowD'
              '%2bnOBvcO7DjBcg07mQ%2buIgc41w1RfN8z6J7EyuOatr4TcF7ocrUqYYGAn1'
              '%2f98Fj3fcLvBhYuIWqMU4thBazJaS8lazD2ZoCT21CCXQ9FvOl6M%2b2alsDd7590sRkmAmNEzdbmU3kGABdTCuY'
              '%2fd3ttaKuPQ7mpQ; '
              'unpl'
              '=V2_ZzNtbUpRFxx8WEMEfB9cVmILGghKX0oUJghBUSsdWQRjABsJclRCFnQUR1NnGVUUZwIZXkFcRhZFCEdkeR1ZAmYBEV1yZ3MWdThHZH4bXwZgChBecmdEFXw4dh8uRTJDJkEiXUJQRxB3AERdeildNWUCE15GUkUdcgp2HxUYEQBlABFaS1VAJXUJR1V6GVgGZgIiXg%3d%3d; __jdu=43226832; shshshfp=c95227ab79b85de5fdda77a21ebfabaa; shshshfpa=ac0a8630-cddf-1629-4472-6746b99959b6-1592446965; shshshfpb=stI8dI8NVQYB4OCbu2qsNag%3D%3D; 3AB9D23F7A4B3C9B=OBJIAZMUDGZRCVPZHBOTDREWC4D6KUBL26KH5XHLQLW2UA6QDJMQEMLFJVS46LY7T22PJRMF47ZXKFE2BWIGDKIG5M; __jdv=176729966|baidu|-|organic|not set|1594016354519; wlfstk_smdl=opz7qkoy48gcx2t9dgo7qku4tpxypy0e; __jdc=176729966; __jda=176729966.43226832.1587013859.1594705039.1594709449.8; __jdb=176729966.2.43226832|8.1594709449; JSESSIONID=30E7FBBB15D50C7AC344CEBAF3F396FC.s1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/83.0.4103.116 Safari/537.36',
}


class JdSpiderSpider(scrapy.Spider):
    name = 'jd_spider'
    allowed_domains = ['zhaopin.jd.com']

    # start_urls = ['http://zhaopin.jd.com/web/job/job_list']

    def start_requests(self):
        start_urls = 'http://zhaopin.jd.com/web/job/job_list'
        for page in range(1, 4):
            # 因为是post请求，所以必须有data
            myFormData = {'pageIndex': str(page), 'pageSize': '10','workCityJson': '[]','jobTypeJson': '[]','jobSearch':'' }
            print(myFormData)

            yield scrapy.FormRequest(url=start_urls, callback=self.parse, method='POST', headers=unicornHeader, formdata=myFormData, dont_filter=True)


    def parse(self, response):
        all_info = json.loads(response.body)
        # print(all_info)
        # print(len(all_info))
        item = JdItem()
        for info in all_info:

            id = info['id']
            # print(id)
            # 岗位名称
            positionName = info['positionName']

            # print(positionName)
            # 任职要求
            qualification = info['qualification']
            # print(qualification)
            # 岗位职责
            workContent = info['workContent']
            # print(workContent)
            # 工作地点
            workCity = info['workCity']
            # print(workCity)

            item['id'] = id
            item['positionName'] = positionName
            item['qualification'] = qualification
            item['workContent'] = workContent
            item['workCity'] = workCity
            yield item


        pass
