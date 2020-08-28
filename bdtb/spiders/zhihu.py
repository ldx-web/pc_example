# import scrapy
# from selenium import webdriver
# import time
#
#
# class zhihuSpider(scrapy.Spider):
#     name = 'zhihu'
#     allowed_domains = ['www.zhihu.com']
#     # start_urls = ['https://www.zhihu.com/']
#
#     def start_requests(self):
#
#
#         # from selenium.webdriver.chrome.options import Options
#         # chrome_option = Options()
#         # chrome_option.add_argument("--disable-extensions")
#         # chrome_option.add_experimental_option("debuggerAddress","127.0.0.1:9222")
#
#         browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
#         # browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',chrome_options=chrome_option)
#
#         browser.get('https://www.zhihu.com/signin')
#         browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys('15932073062')
#         browser.find_element_by_css_selector(".SignFlow-password input").send_keys('ldx123456')
#         # 点击登陆按钮
#         browser.find_element_by_css_selector(".Button.SignFlow-submitButton.Button--primary.Button--blue").click()
#
#         time.sleep(60)
#


import scrapy
from selenium import webdriver
import time

class zhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']


    def start_requests(self):
        browser = webdriver.Chrome(executable_path='/Users/lidongxue/downloads/chromedriver')
        browser.get('https://www.zhihu.com/signin')

        browser.find_element_by_css_selector("div.SignFlow-accountInput Input-wrapper input").send_keys('15932073062')
        browser.find_element_by_css_selector("SignFlow-passwordInput Input-wrapper input").send_keys('ldx123456')
        #点击登陆按钮
        browser.find_element_by_css_selector("Button SignFlow-submitButton Button--primary Button--blue").click()

        time.sleep(60)

        pass

#登陆不上去，有两种解决办法

#1.下载chrome60 driver2.33版本    路径：https://git.imooc.com/coding-92/coding-92

#2.手动去启动chromedriver 有一些js变量

#（1）启动chrom
"""
#进入chrome的安装目录
#chrome.exe --remote-debugging-port=9222
"""