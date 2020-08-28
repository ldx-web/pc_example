import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from urllib import parse
import pymysql
import json
import re
from CSDN.items import CsdnItem2


HEADERS = {
    'accept':'application/json, text/javascript, */*; q=0.01',
    'accept-encoding':'gzip, deflate, br',
    'accept-language':'zh-CN,zh;q=0.9',
    'cookie':'uuid_tt_dd=10_18755758740-1595215116491-548857; dc_session_id=10_1595215116491.759427; __gads=ID=7aee151bef6720c0:T=1595215117:S=ALNI_Ma53RYpoBeJ8t-8SkUI304pra4hFg; UN=weixin_49513651; announcement=%257B%2522isLogin%2522%253Atrue%252C%2522announcementUrl%2522%253A%2522https%253A%252F%252Flive.csdn.net%252Froom%252FPayPal_pp%252F59oaV3tv%253Futm_source%253Dan_1594008357%2522%252C%2522announcementCount%2522%253A0%257D; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_18755758740-1595215116491-548857!5744*1*weixin_49513651; Hm_up_62052699443da77047734994abbaed1b=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22weixin_49513651%22%2C%22scope%22%3A1%7D%7D; Hm_ct_62052699443da77047734994abbaed1b=5744*1*weixin_49513651!6525*1*10_18755758740-1595215116491-548857; dc_sid=48a103186a7a52a36b5d563316b32454; TY_SESSION_ID=6d3bad90-e144-4e3f-806f-0344e73583bf; c_first_ref=www.baidu.com; c_segment=9; Hm_lvt_e5ef47b9f471504959267fd614d579cd=1596769179; Hm_lpvt_e5ef47b9f471504959267fd614d579cd=1596769179; Hm_up_e5ef47b9f471504959267fd614d579cd=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22weixin_49513651%22%2C%22scope%22%3A1%7D%7D; Hm_ct_e5ef47b9f471504959267fd614d579cd=5744*1*weixin_49513651!6525*1*10_18755758740-1595215116491-548857; Hm_lvt_8c2775c990735f09b4af48114c7fe3b4=1596984181; Hm_lpvt_8c2775c990735f09b4af48114c7fe3b4=1596984181; Hm_up_8c2775c990735f09b4af48114c7fe3b4=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22weixin_49513651%22%2C%22scope%22%3A1%7D%7D; Hm_ct_8c2775c990735f09b4af48114c7fe3b4=5744*1*weixin_49513651!6525*1*10_18755758740-1595215116491-548857; SESSION=3dfce336-194a-4229-a4c8-17020fe7d8ea; UserName=weixin_49513651; UserInfo=f6d56df5ce6c4dd4bc4a391bd12d7d5b; UserToken=f6d56df5ce6c4dd4bc4a391bd12d7d5b; UserNick=weixin_49513651; AU=729; BT=1597126889188; p_uid=U000000; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22weixin_49513651%22%2C%22scope%22%3A1%7D%7D; Hm_lvt_62052699443da77047734994abbaed1b=1596196717,1597134050; Hm_lpvt_62052699443da77047734994abbaed1b=1597134050; log_Id_click=6; log_Id_pv=24; aliyun_webUmidToken=T2gAmOU1jIxiMAuQGRyEwfL7ft0WZUZ8M2ObHPstfAUz2p2N9H0dRFLORH4zF69p9xDXeJMl8xnR6P3dtfdbZ1mT; log_Id_view=52; c_first_page=https%3A//blog.csdn.net/weixin_44251004/article/details/93516890; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1597140437,1597145478,1597145872,1597145909; c_utm_medium=distribute.pc_feed.none-task-blog-vip_agree_hot-1.nonecase; c_ref=https%3A//blog.csdn.net/; c_page_id=https%3A//blog.csdn.net/nav/java; dc_tos=qexkdm; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1597201258',
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
}
class CsdnSpiderSpider(scrapy.Spider):
    name = 'csdn'
    # allowed_domains = ['www.csdn.net']
    start_urls = ['https://blog.csdn.net/']

#####！！！！！！此处是根据左侧列表的类别抓取！！！！！！
    def parse(self, response):
        url_list = response.xpath('//div[@class="nav_com"]/ul/li[position()>2]/a/@href').extract()
        print(url_list)
        for xurl in url_list:
            # if url.startswith('https'):
            #     pass
            print(xurl)
            word = re.search(r'^/.*?/(.*?)$', xurl)
            if word:
                word = word.group(1)
                print(word)
                show_offset = response.xpath('//ul[@id="feedlist_id"]/@shown-offset').extract_first("")
                base_url = "https://blog.csdn.net/api/articles?type=more&category={}&shown_offset={}".format(word,show_offset)
                # print(base_url)
                for i in range(50):
                    yield Request(url=parse.urljoin(response.url,base_url),callback=self.parse_item,headers=HEADERS,dont_filter=True)



#####！！！！！！！！！此处为写死单抓"python"
    # def parse(self,response):
    #     show_offset = response.xpath('//ul[@id="feedlist_id"]/@shown-offset').extract_first("")
    #     base_url = "https://blog.csdn.net/api/articles?type=more&category=python&shown_offset={}".format(show_offset)
    #     print(base_url)
    #     for i in range(50):
    #         yield Request(url=parse.urljoin(response.url,base_url),callback=self.parse_item,headers=HEADERS,dont_filter=True)
    #
    def parse_item(self,response):
        print(response.url)
        category = re.search("category=(.*?)&",response.url).group(1)
        print(category)


        all_info = json.loads(response.body)
        print(all_info)
        articles = all_info['articles']
        print(articles)
        for article in articles:
            item = CsdnItem2()

            title = article['title']
            print(title)

            url = article['url']
            print(url)

            #用户名
            user_name = article['user_name']
            ''.join(user_name).replace("'","").replace("'","").replace('"','').replace('"','').strip()
            print(user_name)
            #昵称
            nickname = article['nickname']
            # ''.join(nickname).replace("'","").replace("'","").replace('"','').replace('"','').strip()
            print(nickname)
            #评论数
            comments = article['comments']
            print(comments)

            ds = article['desc']
            ds = ds.replace("'",'"')
            print(ds)

            id = article['id']
            print(id)

            tp = article['type']
            print(tp)

            shown_offset = article['shown_offset']
            print(shown_offset)

            item['title'] = title
            item['url'] = url
            item['user_name'] = user_name
            item['nickname'] = nickname
            item['comments'] = comments
            item['ds'] = ds
            item['id'] = id
            item['tp'] = tp
            item['shown_offset'] = shown_offset
            yield item
            url = 'https://blog.csdn.net/api/articles?type=more&category={}&shown_offset={}'.format(category,shown_offset)
            yield Request(url=parse.urljoin(response.url, url), callback=self.parse_item, headers=HEADERS)







