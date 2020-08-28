import scrapy
import pymysql
from UI.items import UiItem



class UiSpiderPySpider(scrapy.Spider):
    name = 'ui_spider'
    allowed_domains = ['so.uigreat.com']
    start_urls = ['http://so.uigreat.com/']

    def parse(self, response):
        Div = response.xpath("//div[@class='panel']")
        for div in Div:
            item = UiItem()
            big_title = div.xpath(".//span[@class='web-title']//text()").extract_first("")
            print(big_title)
            such_ass = div.xpath(".//div[@class='col-sm-6 col-md-4 col-lg-3']")
            for such_as in such_ass:
                url = such_as.xpath("./a/@href").extract_first("")
                print(url)
                if such_as.xpath(".//img[@class='img-responsive']/@src").extract_first(""):
                    image_url = such_as.xpath(".//img[@class='img-responsive']/@src").extract_first("")
                else:
                    image_url = such_as.xpath(".//div[@class='web-cover']/img/@src").extract_first("")

                print(image_url)

                small_title = such_as.xpath(".//span[@class='web-name']/text()").extract_first("")
                print(small_title)
                ds = such_as.xpath(".//div[@class='dot web-content-bottom-content']/text()").extract_first("")
                print(ds)
                ds = pymysql.escape_string(ds).replace('\\n',"").rstrip().lstrip().replace(" ","").replace("\\r","")
                print(ds)

                item['big_title'] = big_title
                item['url'] = url
                item['image_url'] = image_url
                item['small_title'] = small_title
                item['ds'] = ds
                yield item





