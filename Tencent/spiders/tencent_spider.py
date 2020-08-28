# -*- coding: utf-8 -*-
import scrapy
import json
from Tencent.items import TencentItem
pagenum = 282

class TencentSpiderSpider(scrapy.Spider):
    name = 'tencent_spider'
    allowed_domains = ['careers.tencent.com']
    # start_urls = ['https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1594199570490&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=40001&attrId=&keyword=&pageIndex=1&pageSize=10&language=zh-cn&area=cn']

#获取下一页链接
    def start_requests(self):
        for pageIndex in range(1, pagenum):
            url = 'https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1594205944154&countryId=&cityId=&bgIds=&productId=&categoryId=40001001,40001002,40001003,40001004,40001005,40001006&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh-cn&area=cn'.format(pageIndex)
            yield scrapy.Request(url, callback=self.parse)
#获取详情页链接
    def parse(self,response):
        all_info = json.loads(response.body)
        # print(all_info)
        Data_list = all_info['Data']
        # print(Posts)
        Posts_List = Data_list['Posts']
        # print(Posts_List)
        for Posts in Posts_List:
            PostId = Posts['PostId']
            # print(PostId)
        url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1594202501639&postId={}&language=zh-cn'.format(PostId)
        yield scrapy.Request(url, callback=self.parse_detail)
        pass

    def parse_detail(self,response):
        get_info = json.loads(response.body)
        print(get_info)
        Data = get_info['Data']
        print(Data)

        item = TencentItem()
        #招聘职位ID(在此处是为了当做主键)
        RecruitPostId = Data['RecruitPostId']

        # 定位
        LocationName = Data['LocationName']
        print(LocationName)
        # 岗位职责
        Responsibility = Data['Responsibility']
        print(Responsibility)

        #岗位要求
        Requirement = Data['Requirement']
        print(Requirement)

        #详情页链接
        PostURL = Data['PostURL']
        print(PostURL)

        #职位名称
        RecruitPostName = Data['RecruitPostName']

        item['LocationName'] = LocationName
        item['Responsibility'] = Responsibility
        item['Requirement'] = Requirement
        item['PostURL'] = PostURL
        item['RecruitPostName'] = RecruitPostName
        item['RecruitPostId'] = RecruitPostId
        yield item

        pass