import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from urllib import parse
import pymysql
from CSDN.items import CsdnItem


class CsdnSpiderSpider(scrapy.Spider):
    name = 'csdn_spider'
    # allowed_domains = ['www.csdn.net']
    start_urls = ['https://www.csdn.net/nav/python']

    # rules = (Rule(LinkExtractor(allow=r'https://www.csdn.net/nav/.*?'), callback='parse',follow=False),
    #          )

    def parse(self, response):
        urls = response.xpath("//div[@class='title']//a/@href").extract()
        for url in urls:
            print(url)
            yield Request(url=parse.urljoin(response.url,url), callback=self.parse_item)

    def parse_item(self, response):
        item = CsdnItem()
        title = response.xpath("//div[@class='article-title-box']/h1[@class='title-article']/text()").extract_first("")
        print(title)
        Author_name= response.xpath("//div[@class='bar-content']/a[@class='follow-nickName']/text()").extract_first("")
        print(Author_name)
        publish_time = response.xpath("//div[@class='bar-content']//span[@class='time']/text()").extract_first("")
        print(publish_time)
        read_number = response.xpath("//span[@class='read-count']/text()").extract_first("")
        print(read_number)
        Collection = response.xpath("//*[@id='blog_detail_zk_collection']/span[2]/text()").extract_first("")
        Collection = pymysql.escape_string(Collection).strip().replace('\\n',"").lstrip()
        print(Collection)

        Classification = response.xpath("//*[@id='mainBox']/main/div[1]/div/div/div[2]/div[2]/div/a[1]/text()").extract_first("")
        Classification = pymysql.escape_string(Classification).strip().replace('\\n',"").lstrip()
        print(Classification)
        Article_Tags = response.xpath("//*[@id='mainBox']/main/div[1]/div/div/div[2]/div[2]/div/a[2]/text()").extract_first("")
        Article_Tags = pymysql.escape_string(Article_Tags).strip().replace('\\n',"").lstrip()
        print(Article_Tags)


        item['title'] = title
        item['Author_name'] = Author_name
        item['publish_time'] = publish_time
        item['read_number'] = read_number
        item['Collection'] = Collection
        item['Classification'] = Classification
        item['Article_Tags'] = Article_Tags
        item['url'] = response.url
        yield item


