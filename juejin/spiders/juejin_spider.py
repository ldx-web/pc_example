import scrapy
import json
import time
from juejin.items import JuejinItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

HEADERS={
    'accept':'*/*',
    'accept-language':'zh-CN,zh;q=0.9',
    'content-type':'application/json',
    'cookie':'SLARDAR_WEB_ID=65eb9317-851e-4d22-87e1-8ae064a0f5a8; _ga=GA1.2.2018111071.1597041363; _gid=GA1.2.1965987533.1597041363',
    'referer':'https://juejin.im/',
    'user-agent:':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
}
form_Data = {
    'client_type': 2608,
    'cursor': '0',
    'id_type': 2,
    'limit': 100,
    'sort_type': 200,
}

class JuejinSpiderSpider(scrapy.Spider):
    name = 'juejin_spider'
    allowed_domains = ['apinew.juejin.im']

    def start_requests(self):
        start_urls = 'https://apinew.juejin.im/recommend_api/v1/article/recommend_all_feed'
        yield scrapy.Request(url=start_urls, callback=self.parse, method='POST', headers=HEADERS, encoding='utf-8',body=json.dumps(form_Data))

    # def start_requests(self):
    #     start_urls = ['https://apinew.juejin.im/recommend_api/v1/article/recommend_all_feed',
    #                   ]
    #     rules = (Rule(LinkExtractor(allow=r'https://apinew.juejin.im/recommend_api/v1/article/recommend_all_feed'),callback='parse',follow=False),
    #     )

    def parse(self, response):
         all_info = json.loads(response.body)
         # print((all_info))
         data_list = all_info['data']
         # print(data_list)

         for data in data_list:
            item_info = data['item_info']
            try:
                article_id = item_info['article_id']
                print(article_id)
                # print(len(article_id))
                form_Data2 = {
                    'article_id': article_id
                }
                print(form_Data2)
                url = 'https://apinew.juejin.im/content_api/v1/article/detail'

                yield scrapy.Request(url=url, callback=self.abc, method='POST', headers=HEADERS, encoding='utf-8',
                                body=json.dumps(form_Data2))
            except:
                pass

    def abc(self,response):

        all_content = json.loads(response.body)
        data_all = all_content['data']
        # print(data_all)
        article_info = data_all['article_info']
        print(article_info)

        item = JuejinItem()
        #用户id
        user_id = article_info['user_id']
        #标题
        title = article_info['title']
        print(title)
        #简要内容
        # brief_content = article_info['brief_content']
        # print(brief_content)
        #相关内容
        mark_content = article_info['mark_content']
        # print(mark_content)
        # mark_content = " ".join(mark_content).strip().replace("`","").replace("`","")
        print(mark_content)
        #作者姓名
        author_user_info = data_all['author_user_info']
        print(author_user_info)
        user_name = author_user_info['user_name']
        print(user_name)
        #座右铭
        description= author_user_info['description']
        print(description)

        #阅读数
        got_view_count = author_user_info['got_view_count']
        print(got_view_count)

        #类别名称
        category = data_all['category']
        print(category)
        category_name = category['category_name']
        print(category_name)
        # 时间戳
        ctime = category['ctime']
        print(ctime)
        # dt = time.strftime("%Y-%m-%d %H:%M:%S",ctime) #转为特定格式时间
        # print(dt)

        tags = data_all['tags']
        for tag in tags:
            # 标签名
            tag_name = tag['tag_name']
            print(tag_name)
            item['tag_name'] = tag_name
            #关注用户数
            concern_user_count = tag['concern_user_count']
            print(concern_user_count)
            item['concern_user_count'] = concern_user_count



        item['user_id'] = user_id
        item['title'] = title
        item['mark_content'] = mark_content
        item['user_name'] = user_name
        item['description'] = description
        item['got_view_count'] = got_view_count
        item['category_name'] = category_name
        # item['tag_name'] = tag_name
        # item['concern_user_count'] = concern_user_count
        item['ctime'] = ctime
        yield item



