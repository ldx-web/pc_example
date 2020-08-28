# -*- coding: utf-8 -*-
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import codecs
import json
import MySQLdb
from twisted.enterprise import adbapi    #使用twisted实现数据库一个异步的功能

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ArticleSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            image_file_path = ""
            for ok, value in results:
                image_file_path = value['path']
            item['front_image_path'] = image_file_path
        return item

#将数据利用json文件的方式保存
class JsonWithEncodingPipeline(object):
    def __init__(self):
        self.file = codecs.open("article.json", 'a', encoding='utf-8')
    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item
    def spider_closed(self):
        self.file.close()

#利用scrapy框架自带的json格式进行保存
class JsonExporterPipeline(object):
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        self.exporter.start_exporting()
    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item
    def spider_closed(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

#利用mysql入库,mysqldb是一个同步库
# class MysqlPipeline(object):
#     # 第1种方法 数据库同步插入数据，在异步框架中容易造成堵塞。
#     def __init__(self):
#         # 连接数据库
#         self.conn = MySQLdb.connect("127.0.0.1", "root", "root", "article_spider", charset='utf8', use_unicode='True')  #建立数据库的连接
#         # 连接游标
#         self.cursor = self.conn.cursor()    #mysqldb中的cursor用于做数据的处理
#
#     def process_item(self, item, spider):   #在其中做一些sql语句的处理
#         insert_sql = """
#         insert into jobbole_article(title, url, url_object_id,front_image_path,front_image_url, praise_nums,comment_nums,fav_nums,tags,create_date,content)
#         values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """#其中insert into是我们首先要找到我们的表jobbole_article
#         # import logging
#         # logging.info(insert_sql)
#         params = list()
#         params.append(item.get("title", ""))
#         params.append(item.get("url", ""))
#         params.append(item.get("url_object_id", ""))
#         params.append(item.get("front_image_path", ""))
#         front_image = ','.join(item.get("front_image_url", []))
#         params.append(front_image)
#         params.append(item.get("praise_nums", "0"))
#         params.append(item.get("comment_nums", "0"))
#         params.append(item.get("fav_nums", "0"))
#         params.append(item.get("tags", ""))
#
#         # params.append(item.get("front_image_url", ""))
#         params.append(item.get("create_date", "1970-07-01"))
#         params.append(item.get("content", ""))
#         # logging.info("p -- {}".format(params))
#
#         self.cursor.execute(insert_sql, tuple(params))  # 执行sql语句
#         # logging.info("p ++ {}".format(params))   #输出sql语句内容
#         self.conn.commit()  # 提交入库
#
#         return item


#因为mysqldb是一个同步库（解析速度大于入库速度，因此数据库的负荷会很大，容易造成阻塞整个爬虫）
#在scrapy中尽量不要写同步库，需要一个异步的入库方法来解决同步的问题

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
                insert into jobbole_article(title, url, url_object_id,front_image_path,front_image_url, praise_nums,comment_nums,fav_nums,tags,create_date,content)
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE url_object_id= VALUES(url_object_id)
                """  # 其中insert into是我们首先要找到我们的表jobbole_article
        # import logging
        # logging.info(insert_sql)
        params = list()
        params.append(item.get("title", ""))
        params.append(item.get("url", ""))
        params.append(item.get("url_object_id", ""))
        params.append(item.get("front_image_path", ""))
        front_image = ','.join(item.get("front_image_url", []))
        params.append(front_image)
        params.append(item.get("praise_nums", "0"))
        params.append(item.get("comment_nums", "0"))
        params.append(item.get("fav_nums", "0"))
        params.append(item.get("tags", ""))

        # params.append(item.get("front_image_url", ""))
        params.append(item.get("create_date", "1970-07-01"))
        params.append(item.get("content", ""))

        cursor.execute(insert_sql, tuple(params))
