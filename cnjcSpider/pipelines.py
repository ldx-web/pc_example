# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# #方法一：（以txt格式进行保存）
# from scrapy.exporters import JsonLinesItemExporter   #Exporter用于扩展scrapy导出数据的格式
# import json
# class cnjcSpiderPipeline(object):
#     def process_item(self, item, spider):
#         # self.fp = open("cainiao.json", "wb")
#         self.file = open("cainiao.txt", "a", encoding="utf-8")
#         self.file.write(str(item["name"])+'\n')
#         self.file.write(str(item['content'])+'\n\t')
#         #
#         # self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')   #ensure_ascii=False表示想要输出真正的中文
#         # self.exporter.export_item(item)       #处理item
#         return item
#
#     def close_spider(self, spider):
#         # self.fp.close()
#         self.file.close()
#


# #方法二：(以json格式进行保存)
# import json
# import traceback
#
# class JsonPipeline(object):
#     def __init__(self):
#         self.file = open("cainiao.json", "w", encoding="utf-8")
#     def process_item(self, item, spider):
#         line = json.dumps(dict(item), ensure_ascii=False) + '\n'   #json中的dumps和dump是序列化的方法，dumps以字符串str进行保存，json默认是ASCII的形式，并不是以真正的中文进行保存，若想以真正的中文进行保存，需要将ensure_ascii=False
#         self.file.write(line)
#         return item
#     def spider_closed(self,spider):
#         self.file.close()

#
# #方法三：(以mysql入库进行保存)
import pymysql
import traceback
class mysqlPipeline(object):
    def process_item(self, item, spider):
        name = item['name']
        content = item['content']
        url = item['url']
        db = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='123456',
            db='article_spider',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

        try:
            cursor = db.cursor()   #使用cursor()方法获取操作游标
            # insert_sql = """
            #        insert into cnjc_spider(title,content) values (%s, %s)"""  # 其中insert into是我们首先要找到我们的表jobbole_article
            # sql = """INSERT INTO NEWS(title,content) VALUES (%s,%s)""" % (name, content)   #SQL插入语句
            content = content.replace("'", '"')     #因为网站文本处的内容不符合sql语句，可在insert_sql处打断点，将其copy value拷贝到sql数据库中的新建查询进行查看
            content = "'" + content + "'"
            name = name.replace("'", '"')
            name = "'" + name + "'"
            url = url.replace("'", '"')
            url = "'" + url + "'"

            insert_sql = """insert into cnjc(name,content,url) values ({},{},{})""".format(name, content, url)  # 其中insert into是我们首先要找到我们的表jobbole_article

            cursor.execute(insert_sql)       #执行sql语句
            db.commit()                      #提交修改

        except Exception as e:
            print(traceback.format_exc())    #若发生异常，抛出异常原因
        finally:
            db.close()                         #关闭连接
        return item