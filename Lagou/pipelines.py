# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json



# -*- coding: utf-8 -*-
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import codecs
import json
import MySQLdb
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
from Lagou.settings import SQL_DATETIME_FORMAT,SQL_DATE_FORMAT

#以json格式进行保存
# class LagouPipeline(object):
#     def __init__(self):
#         self.file = open("lagou_spider.json", 'a', encoding='utf-8')
#     def process_item(self, job_item, spider):
#         line = json.dumps(dict(job_item), ensure_ascii=False) + '\n'
#         self.file.write(line)
#         return job_item
#     def spider_closed(self, spider):
#         self.file.close()

class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
    @classmethod   #首先承载一个类方法
    def from_settings(cls, settings):
        from MySQLdb.cursors import DictCursor
        dbparms = dict(
            host=settings["MYSQL_HOST"],     #从setting文件中读取相关内容，而不是直接将它写死
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset="utf8mb4",
            cursorclass=DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)   #MySQLdb是固定的，注意大小写；然后将dbparms传进来
        return cls(dbpool)  #此处是一个实例化的方法，将"dbpool"参数传递给def__init__()主配置文件

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self,cursor,item):
        print("----=++++")
        insert_sql = """
                insert into lagou_nodenglu(title,url,url_object_id,salary,job_city,work_years,degree_need,job_type,publish_time,job_advantage,job_desc,job_addr,company_name,company_url,tags,crawl_time)
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE salary=VALUES(salary)
                """  # 其中insert into是我们首先要找到我们的表jobbole_article
        # import logging
        # logging.info(insert_sql)
        params = list()
        params.append(item.get("title", ""))
        params.append(item.get("url", ""))
        params.append(item.get("url_object_id", ""))
        params.append(item.get("salary", ""))
        params.append(item.get("job_city", ""))
        params.append(item.get("work_years", ""))
        params.append(item.get("degree_need", ""))
        params.append(item.get("job_type", ""))
        params.append(item.get("publish_time", "0000-00-00"))
        params.append(item.get("job_advantage", ""))
        params.append(item.get("job_desc", ""))
        params.append(item.get("job_addr", ""))
        params.append(item.get("company_name", ""))
        params.append(item.get("company_url", ""))
        params.append(item.get("tags", ""))
        params.append(item['crawl_time'].strftime(SQL_DATETIME_FORMAT))

        cursor.execute(insert_sql, tuple(params))

# 利用mysql入库,mysqldb是一个同步库
# class MysqlPipeline(object):
#     # 第1种方法 数据库同步插入数据，在异步框架中容易造成堵塞。
#     def __init__(self):
#         # 连接数据库
#         self.conn = MySQLdb.connect("127.0.0.1", "root", "123456", "LG", charset='utf8', use_unicode='True')  #建立数据库的连接
#         # 连接游标
#         self.cursor = self.conn.cursor()    #mysqldb中的cursor用于做数据的处理
#
#     def process_item(self, item, spider):   #在其中做一些sql语句的处理
#         insert_sql = """
#          insert into lagou(title,url,url_object_id,salary,job_city,work_years,degree_need,job_type,publish_time,job_advantage,job_desc,job_addr,company_name,company_url,tags,crawl_time)
#                 values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE salary=VALUES(salary)
#         """#其中insert into是我们首先要找到我们的表jobbole_article
#         # import logging
#         # logging.info(insert_sql)
#         params = list()
#         params.append(item.get("title", ""))
#         params.append(item.get("url", ""))
#         params.append(item.get("url_object_id", ""))
#         params.append(item.get("salary", ""))
#         params.append(item.get("job_city", ""))
#         params.append(item.get("work_years", ""))
#         params.append(item.get("degree_need", ""))
#         params.append(item.get("job_type", ""))
#         params.append(item.get("publish_time", "0000-00-00"))
#         params.append(item.get("job_advantage", ""))
#         params.append(item.get("job_desc", ""))
#         params.append(item.get("job_addr", ""))
#         params.append(item.get("company_name", ""))
#         params.append(item.get("company_url", ""))
#         params.append(item.get("tags", ""))
#         params.append(item['crawl_time'].strftime(SQL_DATETIME_FORMAT))
#
#         # cursor.execute(insert_sql, tuple(params))
#
#         self.cursor.execute(insert_sql, tuple(params))  # 执行sql语句
#         # logging.info("p ++ {}".format(params))   #输出sql语句内容
#         self.conn.commit()  # 提交入库
#
#         return item
