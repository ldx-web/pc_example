# -*- coding: utf-8 -*-

import scrapy
from scrapy.linkextractors import LinkExtractor    #linkextractors非常适合于整站抓取数据
from scrapy.spiders import CrawlSpider, Rule       #CrawlSpider类定义了一些规则（rules）来提供跟进链接（link）的方便机制，从爬取的网页中获取link并继续爬取的工作更适合
from cnjcSpider.items import CnjcspiderItem
from scrapy import Request
from urllib import parse

class cnjcSpider(CrawlSpider):
    name = 'cnjc'
    allowed_domains = ['runoob.com']
    start_urls = [
                  'https://www.runoob.com/python3/python3-tutorial.html',
                  # 'https://www.runoob.com/html/html-tutorial.html',
                  # 'https://www.runoob.com/css/css-tutorial.html',
                  # 'https://www.runoob.com/js/js-tutorial.html',
                  # 'https://www.runoob.com/jquery/jquery-tutorial.html',
                  # 'https://www.runoob.com/bootstrap/bootstrap-tutorial.html',
                  # 'https://www.runoob.com/python/python-tutorial.html',
                  # 'https://www.runoob.com/java/java-tutorial.html',
                  # 'https://www.runoob.com/cprogramming/c-tutorial.html',
                  # 'https://www.runoob.com/cplusplus/cpp-tutorial.html',
                  # 'https://www.runoob.com/csharp/csharp-tutorial.html',
                  # 'https://www.runoob.com/sql/sql-tutorial.html',
                  # 'https://www.runoob.com/mysql/mysql-tutorial.html',
                  # 'https://www.runoob.com/php/php-tutorial.html',
                  ]

    rules = (
        Rule(LinkExtractor(allow=r'https://www.runoob.com/python3/python3-+'), callback='parse_item', follow=False),
        #  Rule(LinkExtractor(allow=r'https://www.runoob.com/html/html-+'), callback='parse_item', follow=False),
        #  Rule(LinkExtractor(allow=r'https://www.runoob.com/css/css-+'), callback='parse_item', follow=False),
        #  Rule(LinkExtractor(allow=r'https://www.runoob.com/js/js-+'), callback='parse_item', follow=False),
        #  Rule(LinkExtractor(allow=r'https://www.runoob.com/jquery/jquery-+'), callback='parse_item', follow=False),
        #  Rule(LinkExtractor(allow=r'https://www.runoob.com/bootstrap/bootstrap-+'), callback='parse_item', follow=False),
        #  Rule(LinkExtractor(allow=r'https://www.runoob.com/python/python-+'), callback='parse_item', follow=False),
        #  Rule(LinkExtractor(allow=r'https://www.runoob.com/java/java-+'), callback='parse_item', follow=False),
        #  Rule(LinkExtractor(allow=r'https://www.runoob.com/cprogramming/c-+'), callback='parse_item', follow=False),
        #  Rule(LinkExtractor(allow=r'https://www.runoob.com/cplusplus/cpp-+'), callback='parse_item', follow=False),
        #  Rule(LinkExtractor(allow=r'https://www.runoob.com/csharp/csharp-+'), callback='parse_item', follow=False),
        #  Rule(LinkExtractor(allow=r'https://www.runoob.com/sql/sql-+'), callback='parse_item', follow=False),
        #  Rule(LinkExtractor(allow=r'https://www.runoob.com/mysql/mysql-+'), callback='parse_item', follow=False),
        #  Rule(LinkExtractor(allow=r'https://www.runoob.com/php/php-+'), callback='parse_item', follow=False),
    )


    # url = "https://www.test.com/page={}"
    # start_urls = []
    # for i in range(1,501):
    #     start_urls.append(url.format(i))

    def parse(self, response):
       urls = response.xpath("//div[@class='design']/a/@href").getall()
       # print(len(urls))
       for url in urls:
           # print(parse.urljoin(response.url, "/python3/python3-{}".format(url)))
           yield Request(url=parse.urljoin(response.url, url), callback=self.parse_item)
          # break


    def parse_item(self, response):

        #url = response.xpath("//div[@class='design']/a/@href").getall()
        name = response.xpath('//div[@class="article-intro"]/h1/text()').get()
        if response.xpath('//div[@class="article-intro"]/h1/span/text()').get():
            name += response.xpath('//div[@class="article-intro"]/h1/span/text()').get()
        contents = response.xpath('//div[@class="article-intro"]//text()').getall()
        title = []
        title.append(name)
        if response.xpath('//div[@class="article-intro"]/h2/text()').get():
            title_2 = response.xpath('//div[@class="article-intro"]/h2/text()').getall()
            title += title_2
        if response.xpath('//div[@class="article-intro"]/h3/text()').get():
            title_3 = response.xpath('//div[@class="article-intro"]/h3/text()').getall()
            title += title_3
        print("===============")
        print(name)
        print(title)
        print(contents)
        content_list = []
        #contents列表
        for i in contents:
            # if content=="\r\n":
            #     continue
            if "\t" in i:
                #包括制表符，剔除这一行
                continue
            if "\n" in i:
                #包括换行，剔除这一行
                continue
            if i in title:
                #标题包括值，添加值并换行
                content_list.append("\n")
            #去除首尾空格和换行符
            content_list.append(i.strip())

            # if i in title:
            #     #标题包括值，添加值并换行
            #     content_list.append("\n")
        content = " ".join(content_list)
        print(content)
        item = CnjcspiderItem(name=name, content=content)
        item["url"] = response.url
        print(item)
        yield item



'''
import scrapy
from scrapy.linkextractors import LinkExtractor    #linkextractors非常适合于整站抓取数据
from scrapy.spiders import CrawlSpider, Rule       #CrawlSpider类定义了一些规则（rules）来提供跟进链接（link）的方便机制，从爬取的网页中获取link并继续爬取的工作更适合
from cnjcSpider.items import CnjcspiderItem


class cnjcSpider(CrawlSpider):
    name = 'cnjc'
    allowed_domains = ['runoob.com']
    start_urls = ['https://www.runoob.com/python3/python3-tutorial.html']

    rules = (
        Rule(LinkExtractor(allow=r'https://www.runoob.com/python3/python3-+'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        name = response.xpath('//div[@class="article-intro"]/h1/text()').get()
        if response.xpath('//div[@class="article-intro"]/h1/span/text()').get():
            name += response.xpath('//div[@class="article-intro"]/h1/span/text()').get()
        contents = response.xpath('//div[@class="article-intro"]//text()').getall()
        title = []
        title.append(name)
        if response.xpath('//div[@class="article-intro"]/h2/text()').get():
            title_2 = response.xpath('//div[@class="article-intro"]/h2/text()').getall()
            title += title_2
        if response.xpath('//div[@class="article-intro"]/h3/text()').get():
            title_3 = response.xpath('//div[@class="article-intro"]/h3/text()').getall()
            title += title_3
        print("===============")
        print(name)
        print(title)
        print(contents)
        content_list = []
        #contents列表
        for i in contents:
            # if content=="\r\n":
            #     continue
            if "\t" in i:
                #包括制表符，剔除这一行
                continue
            if "\n" in i:
                #包括换行，剔除这一行
                continue
            if i in title:
                #标题包括值，添加值并换行
                content_list.append("\n")
            #去除首尾空格和换行符
            content_list.append(i.strip())

            if i in title:
                #标题包括值，添加值并换行
                content_list.append("\n")
        content = " ".join(content_list)
        print(content)
        item = CnjcspiderItem(name=name, content=content)
        print(item)
        yield item
'''
