import scrapy
import json
from scrapy import Request
from bdtb.items import BdtbItem,ReplyBdtbItem
from urllib import parse
from lxml import etree
import re


HEADERS = {
    'Cookie':'NO_UNAME=1; BIDUPSID=27b0cde9310282ed4b8e34e9c4754db1; PSTM=1594986824; BAIDUID=27b0cde9310282ed4b8e34e9c4754db1:FG=1; TIEBA_USERTYPE=b9c40c8516d0e9b4875429ad; wise_device=0; bdshare_firstime=1595473023425; st_key_id=17; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1596005571,1596005924,1596006330,1596006794; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; delPer=0; PSINO=2; ZD_ENTRY=baidu; TIEBAUID=e7b147868ed76138942e5903; BDUSS=NZRnU1T0IyekRPSndTVWY3TUVaR1lOSmVhN1BEQXRkcDRUd2JiR0ppamVla3RmRVFBQUFBJCQAAAAAAAAAAAEAAAA6HczQzrTAtL~Jxtq809PNt9wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN7tI1~e7SNfY3; BDUSS_BFESS=NZRnU1T0IyekRPSndTVWY3TUVaR1lOSmVhN1BEQXRkcDRUd2JiR0ppamVla3RmRVFBQUFBJCQAAAAAAAAAAAEAAAA6HczQzrTAtL~Jxtq809PNt9wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN7tI1~e7SNfY3; STOKEN=ae6409d8d6e94c41743728910ecff5f30368cb29327f54458d4a86e8dbba3205; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; 3503037754_FRSVideoUploadTip=1; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1596293032; st_data=704076b630fe5e6d800b14ea73fb941ef279ba2200e4e4751289b12d2c6c84763857535320146902dd989b87508a200aa0094af055166aa99c56ea04f69e12816fa80e4d2c40989780ff5b7e6d6115fe57a7ab6d3382ba8da11abba613fa8f1b6aa136b43734f662ce27d72c4fd31d0b984af154470e6c5ced8d9915f29c8df6; st_sign=c8c73be1; H_PS_PSSID=32293_1468_32438_32141_32359_31660_32352_32045_32394_32407_32429_32117_26350_32430',
    'Host':'tieba.baidu.com',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
}
from scrapy.selector import Selector
BASE_URL = "https://tieba.baidu.com"

class BdtbSpiderSpider(scrapy.Spider):
    name = 'bdtb_spider'
    allowed_domains = ['tieba.baidu.com']


    def start_requests(self):
        for offset in range(0, 50, 50):
            start_urls = 'https://tieba.baidu.com/f?kw=python&ie=utf-8&pn={}'.format(offset)
            print(start_urls)
            yield scrapy.Request(url=start_urls, callback=self.parse)

    # def start_requests(self):
    #     url = 'https://tieba.baidu.com/p/comment?pn=1&tid=6816263340&pid=133434866647&'
    #
    #     yield scrapy.Request(url=url, callback=self.reply_item)


    def parse(self, response):
        b = response.text
        #检查网页源码，发现想要获取的网页源码被注释，以至于提取"详情页的url为空"
        html_new = b.replace(r'<!--','').replace(r'-->','')    #去掉网页源码的注释
        #content = Selector(text=html_new)

        #with open('test.html','w') as f:       # 创建一个"test.html"文件进行，利用谷歌浏览器进行打开，查看是否返回页面信息
        #    f.write(html_new)
        content = etree.HTML(html_new)          ##调用HTML类进行初始化，成功构造XPath解析对象(etree.HTML解析成的是xml)
        print(content)

        urls = content.xpath("//div[contains(@class,'threadlist_title')]//a/@href")     #抓取每一个详情页的url(在xml中定位节点，返回的是一个列表)
        for url in urls:
            url_all = BASE_URL + url
            print(url_all)
            yield Request(url_all, callback=self.parse_item)



    def parse_item(self, response):                #解析详情页中的内容
        text = response.text
        Div_all = response.xpath("//div[contains(@class,'l_post')]")
        for Div in Div_all:
            #创建一个类对象
            item = BdtbItem()

            #1.发贴人姓名
            user_name = Div.xpath(".//ul[@class='p_author']//li[@class='d_name']//a/text()").extract_first("")
            print(user_name)
            #2.发布内容

            contents = Div.xpath(".//div[contains(@class,'j_d_post_content')]/text()").extract()
            contents = [x.strip() for x in contents if x.strip() != '']
            contents =str(contents).replace("[","").replace("]","").replace("'","").replace("'","")
            # print(contents)
            if len(contents) != 0:
                print(contents)
            else:
                print('NULL')
            # for content in contents:       #数据返回的是列表形式，转为字符串
            #     print(content)
            #3.发帖人发布时间
            time_info = Div.xpath(".//@data-field").extract_first("")
            times = json.loads(time_info)
            t_info = times['content']
            time = t_info['date']
            print(time)
            text = response.text
            tid = re.findall('"thread_id":(.*?),', text)[0]  #在json中取"thread_id数据"
            print(tid)
            pid_info = Div.xpath(".//@data-field").extract_first("")
            pid = json.loads(pid_info)
            p_info = pid['content']
            pid = p_info['post_id']
            print(pid)

            item['user_name'] = user_name
            item['contents'] = contents
            item['time'] = time
            item['tid'] = tid
            item['pid'] = pid
            yield item

           #抓取评论页的url网址
            pn = 1
            url = "https://tieba.baidu.com/p/comment?pn={}&tid={}&pid={}&".format(pn, str(tid), str(pid))    #新加&
            yield scrapy.Request(url, callback=self.reply_item)


    #此处是没有设置评论区域的"翻页处理"
    #抓取评论区域的内容，在详情页找到一个评论多的页数，打开审查元素-Network-找到评论区域内容多的，有下一页的部分，进行翻页-进行抓包，找到相对应的api接口链接，如上两行命令
    def reply_item(self, response):
        # print(response.url)
        tid = re.search("tid=(.*?)&",response.url).group(1)       #在评论回复页利用正则表达式，获取相应的值
        # print(tid)
        # print(re.search("pid=(.*?)&", response.url))
        # print(re.search("pid=(.*?)&", response.url).group(0))
        # print(re.search("pid=(.*?)&", response.url))
        # print(re.search("pid=(.*?)&", response.url).group(1))
        pid = re.search("pid=(.*?)&",response.url).group(1)


        pn = int(re.search("pn=(.*?)&",response.url).group(1))



        # tid = response.meta.get("tid", '')
        # pid = response.meta.get("pid", '')
        # pn = response.meta.get('pn','')

        Li_all = response.xpath("//li[contains(@class,'j_lzl_s_p')]")
        if Li_all !=[]:          #只要评论回复页有数据，就进行翻页处理
            pn += 1
            url = "https://tieba.baidu.com/p/comment?pn={}&tid={}&pid={}&".format(pn, str(tid), str(pid))
            yield scrapy.Request(url, callback=self.reply_item)
        for li in Li_all:
            #创建一个item项目
            item = ReplyBdtbItem()
            #回复人
            reply_name = li.xpath(".//a[@class='at j_user_card ']/@username").extract_first("")
            #注：reply_name的取值解析式是在一个标签的内部元素中进行取值，取一个元素的'key'属性对应的值，利用"/@这个键"，如果是取里面的文本，则"/@text()"
            if reply_name ==[]:
                print("reply_name is NULL")
            else:
                print(reply_name)
            #被回复人
            By_reply_name = li.xpath(".//a[@class='at']/text()").extract_first("")
            if By_reply_name ==[]:
                print("reply_name is NULL")
                # return
            else:
                print(By_reply_name)

            #回复内容
            content_replieds = li.xpath(".//span[@class='lzl_content_main']//text()").extract()
            for content_replied in content_replieds:
                content_replied = content_replied.replace(" ",'').replace(":",'')
                print(content_replied)
            # print(content_replied)
            # content_replied = content_replied.replace(" ",'').replace(":",'')
            # # print(content_replied)
            # if len(content_replied) < 1:
            #     return
            # else:
            #     content_replied1 = li.xpath(".//span[@class='lzl_content_main']/a/text()").extract_first("").replace(" ",'').replace(":",'')
            #     content_replied2 = li.xpath(".//span[@class='lzl_content_main']/text()").extract_first("").replace(" ",'').replace(":",'')
            #     content_replied = content_replied1 + content_replied2
            # print(content_replied)


            #回事时间
            replay_time = li.xpath(".//span[@class='lzl_time']/text()").extract_first("")
            if replay_time == []:
                return
            else:
                print(replay_time)
            item = ReplyBdtbItem()
            item['reply_name'] = reply_name
            item['By_reply_name'] = By_reply_name
            item['content_replied'] = content_replied
            item['replay_time'] = replay_time
            yield item







