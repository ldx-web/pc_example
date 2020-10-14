# Scrapy settings for Lagou project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Lagou'

SPIDER_MODULES = ['Lagou.spiders']
NEWSPIDER_MODULE = 'Lagou.spiders'

# SPIDER_MODULES = ['Lagou.select']
# NEWSPIDER_MODULE = 'Lagou.select'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False                #不遵守robots协议

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
RANDOMIZE_DOWNLOAD_DELAY = True         #如果启用，scrapy将随机等待一段时间（0.5-1.5）
DOWNLOAD_DELAY = 10                     #隔10s发送一个请求
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False
COOKIES_ENABLED = False
COOKIES_DEBUG = True


# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': '*/*',
#   'Accept-Language': 'zh-CN,zh;q=0.9',
#   'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
#   'cookie':'user_trace_token=20200814183842-7c6217c3-6616-402e-aea9-803b78afa126; _ga=GA1.2.273708507.1597401523; LGUID=20200814183843-983a11d8-20be-4ce6-afdb-3a2462a8111b; JSESSIONID=ABAAABAABAGABFA6B3AE37F12E88EC5FACB6183498161A6; WEBTJ-ID=20200814183908-173ec8d46e6c36-09592fd4c6226c-31647305-1296000-173ec8d46e78d5; RECOMMEND_TIP=true; _gid=GA1.2.1122499119.1597632964; index_location_city=%E5%8C%97%E4%BA%AC; X_MIDDLE_TOKEN=920d5143e6387eb2b5ac0bbb6bde2bb5; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22173fa58d73edd8-095597c56e7a1e-31667305-1296000-173fa58d73fc8a%22%2C%22%24device_id%22%3A%22173fa58d73edd8-095597c56e7a1e-31667305-1296000-173fa58d73fc8a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=784; privacyPolicyPopup=false; LG_HAS_LOGIN=1; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1597401549,1597632726,1597632743,1597677581; login=false; unick=""; _putrc=""; LG_LOGIN_USER_ID=""; LGSID=20200818152856-a1d3a12b-6bbe-45f0-babf-9aa2bb55c819; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist%5Fpython%2Fp-city%5F2%3F%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; _gat=1; TG-TRACK-CODE=jobs_similar; X_HTTP_TOKEN=30760a29107659e154063779514b0d9cf9f795914a; LGRID=20200818153405-795077b7-be57-4f12-9fce-ee935b313d82; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1597736045; SEARCH_ID=36cc36654ee5471fa327c526f77b4045',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#     'Lagou.middlewares.LagouSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'Lagou.middlewares.LagouDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,

}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # 'Lagou.pipelines.LagouPipeline': 300,
    'Lagou.pipelines.MysqlTwistedPipeline': 200,

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0,os.path.join(BASE_DIR,'Lagou'))
# print(BASE_DIR)



MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'LG'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'


SQL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
SQL_DATE_FORMAT = "%Y-%m-%d"