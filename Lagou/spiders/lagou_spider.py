#####在登陆的情况下
# #-*- coding: utf-8 -*-
# import scrapy
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
# from selenium import webdriver
# import time
# import os
# # from ..settings import BASE_DIR
# from Lagou.settings import BASE_DIR
# import pickle
# from Lagou.items import LagouJobItemLoader,LagouJobItem
# from Lagou.spiders.utils.common import get_md5
# from datetime import datetime
#
#
# class LagouSpiderSpider(CrawlSpider):
#     name = 'lagou_spider'
#     allowed_domains = ['www.lagou.com']
#     start_urls = ['https://www.lagou.com/']
#
#     rules = (
#         Rule(LinkExtractor(allow=('zhaopin/.*',)),follow=True),
#         Rule(LinkExtractor(allow=('gongsi/j\d+.html',)),follow=True),
#         Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
#
#     )
#
#     def start_requests(self):
#         cookies = []
#         if os.path.exists(BASE_DIR + "/cookies/lagou.cookie"):
#             cookies = pickle.load(open(BASE_DIR + "/cookies/lagou.cookie","rb"))
#         if not cookies:
#             browser = webdriver.Chrome()
#             browser.get("https://passport.lagou.com/login/login.html")
#             # browser.get("https://www.lagou.com/zhaopin/Python/")
#             browser.find_element_by_css_selector("div[data-view='passwordLogin'] input.input_white").send_keys("****")
#             browser.find_element_by_css_selector("div[data-view='passwordLogin'] input[type='password']").send_keys("****")
#             browser.find_element_by_css_selector("div[data-view='passwordLogin'] input[type='submit']").click()
#             time.sleep(10)
#             cookies = browser.get_cookies()
#             #写入cookie到文件
#             pickle.dump(cookies,open(BASE_DIR + "/cookies/lagou.cookie","wb",))
#         cookie_dict = {}
#         for cookie in cookies:
#             cookie_dict[cookie["name"]] = cookie["value"]
#
#         for url in self.start_urls:
#             yield scrapy.Request(url, dont_filter=True,cookies=cookie_dict)
#
#
#     def parse_job(self, response):
#
#         item_loader = LagouJobItemLoader(item=LagouJobItem(),response=response)  #利用item = LagouJobItem()直接进行一个实例化
#
#         item_loader.add_xpath("title","//div[@class='job-name']//h1/text()")
#         item_loader.add_value("url", response.url)
#         item_loader.add_value("url_object_id", get_md5(response.url))
#         item_loader.add_xpath("salary","//dd[@class='job_request']/h3/span[1]/text()")
#         item_loader.add_xpath("job_city","//dd[@class='job_request']/h3/span[2]/text()")
#         item_loader.add_xpath("work_years","//dd[@class='job_request']/h3/span[3]/text()")
#         item_loader.add_xpath("degree_need","//dd[@class='job_request']/h3/span[4]/text()")
#         item_loader.add_xpath("job_type","//dd[@class='job_request']/h3/span[5]/text()")
#         item_loader.add_xpath("publish_time","//p[@class='publish_time']/text()")
#         item_loader.add_xpath("job_advantage","//dd[@class='job-advantage']//p/text()")
#         item_loader.add_xpath("job_desc","//div[@class='job-detail']")
#         item_loader.add_xpath("job_addr","//div[@class='work_addr']")
#         item_loader.add_xpath("company_name","//div[@class='job_company_content']//em[@class='fl-cn']/text()")
#         item_loader.add_xpath("company_url","//ul[@class='c_feature']//a/@href")
#         item_loader.add_xpath("tags","//li[@class='labels']/text()")
#         item_loader.add_value("crawl_time",datetime.now())
#
#         #利用css解析
#         # item_loader.add_css("title", ".job-name::attr(title)")
#         # item_loader.add_value("url", response.url)
#         # item_loader.add_value("url_object_id", get_md5(response.url))
#         # item_loader.add_css("salary", ".job_request .salary::text")
#         # item_loader.add_xpath("job_city", "//*[@class='job_request']/h3/span[2]/text()")
#         # item_loader.add_xpath("work_years", "//*[@class='job_request']/h3/span[3]/text()")
#         # item_loader.add_xpath("degree_need", "//*[@class='job_request']/h3/span[4]/text()")
#         # item_loader.add_xpath("job_type", "//*[@class='job_request']/h3/span[5]/text()")
#         # item_loader.add_css("tags", '.position-label li::text')
#         # item_loader.add_css("publish_time", ".publish_time::text")
#         # item_loader.add_css("job_advantage", ".job-advantage p::text")
#         # item_loader.add_css("job_desc", ".job_bt div")
#         # item_loader.add_css("job_addr", ".work_addr")
#         # item_loader.add_css("company_name", "#job_company dt a img::attr(alt)")
#         # item_loader.add_css("company_url", "#job_company dt a::attr(href)")
#         # item_loader.add_value("crawl_time", datetime.now())
#
#         job_item = item_loader.load_item()    #将item_loader利用load_item方法，在放入item
#         if job_item.get("title"):
#             return job_item
#


#####在不登陆情况下
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
    'cookie':'user_trace_token=20200814183842-7c6217c3-6616-402e-aea9-803b78afa126; _ga=GA1.2.273708507.1597401523; LGUID=20200814183843-983a11d8-20be-4ce6-afdb-3a2462a8111b; JSESSIONID=ABAAABAABAGABFA6B3AE37F12E88EC5FACB6183498161A6; WEBTJ-ID=20200814183908-173ec8d46e6c36-09592fd4c6226c-31647305-1296000-173ec8d46e78d5; RECOMMEND_TIP=true; _gid=GA1.2.1122499119.1597632964; index_location_city=%E5%8C%97%E4%BA%AC; X_MIDDLE_TOKEN=920d5143e6387eb2b5ac0bbb6bde2bb5; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=784; privacyPolicyPopup=false; LG_HAS_LOGIN=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1597401549,1597632726,1597632743,1597677581; TG-TRACK-CODE=index_bannerad; sensorsdata2015session=%7B%7D; mds_login_authToken="K6mKcQ16hBOgUk/oXAxgswVjDTIcSDwgbkA6l6Z+O2ME3/hrC8Z6Pq7WfE+IxC+JTos3vrOryeNZSPtOsYYNBoQ6cWOh7inAtGRz8cmZuMUqx50rgM+S7EfCpCmhg7dmRSAnTrEt1Y/d6BIniMetv7AUa/RA8WQKzOZD5c7jTvJ4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22173fa58d73edd8-095597c56e7a1e-31667305-1296000-173fa58d73fc8a%22%2C%22%24device_id%22%3A%22173fa58d73edd8-095597c56e7a1e-31667305-1296000-173fa58d73fc8a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22lagou%22%2C%22%24latest_utm_medium%22%3A%22appbanner%22%2C%22%24latest_utm_campaign%22%3A%22%E5%A4%A7%E6%95%B0%E6%8D%AE%E5%BC%80%E5%8F%91%E9%AB%98%E8%96%AA%E8%AE%AD%E7%BB%83%E8%90%A5%22%2C%22%24latest_utm_content%22%3A%22data_enhancement%22%2C%22%24latest_utm_term%22%3A%22data_enhancement%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24os%22%3A%22MacOS%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2284.0.4147.125%22%7D%7D; LGSID=20200819125059-b3776202-cb40-49a8-befa-3016d3543049; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist%5F%25E5%2590%258E%25E7%25AB%25AF%25E5%25BC%2580%25E5%258F%2591%25E5%25B7%25A5%25E7%25A8%258B%25E5%25B8%2588%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; _gat=1; login=false; unick=""; _putrc=""; LG_LOGIN_USER_ID=""; X_HTTP_TOKEN=30760a29107659e108721879514b0d9cf9f795914a; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1597812780; LGRID=20200819125300-6724c57a-9924-40c9-9303-e8791a9df008; SEARCH_ID=7fbb353f850249d9b13e041d3dfd7718',
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






