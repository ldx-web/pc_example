# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from scrapy import Request

from LCSpider.items import LcspiderItem

class LiangcangSpider(scrapy.Spider):
    name = 'liangcang'
    allowed_domains = ['iliangcang.com']
    # start_urls = ['https://www.iliangcang.com/i/shop/list/?cat_id=00690244&shence=1']
    start_urls = [
        # 'https://www.iliangcang.com/i/shop/list/?cat_id=00690244&shence=1',
        'https://www.iliangcang.com/i/shop/list/?cat_id=00690070&shence=1'
                  ]

    def parse(self, response):
        post_nodes = response.xpath("//div[@id='main']//div[contains(@class,'item')]")
        print(len(post_nodes))
        for post_node in post_nodes:
           image_url = post_node.xpath(".//div[@class='imgCon']//a/@href").extract_first("")
           print(image_url)
           yield Request(url=parse.urljoin(response.url, image_url),callback=self.parse_detail)

        next_url = response.xpath("//input[@type='button'][@class='next']/@onclick").extract_first("")
        # print(next_url)
        yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

 # 详情页面解析
    def parse_detail(self, response):

        brand = response.css(".gdName a::text").extract_first("")
        # print(brand)
        title = response.xpath("//div[@class='gdName']/text()").extract()
        title = ''.join(title).strip()
        # print(title)
        price = response.xpath("//div[@class='infoItem']//span[contains(@id,'goodsPrice')]//text()").extract_first("")
        # print(price)
        item = LcspiderItem()
        item['brand'] = brand
        item['title'] = title
        item['price'] = price
        item['url'] = response.url
        yield item
        pass

