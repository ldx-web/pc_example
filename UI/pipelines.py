# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import pymysql
from pymysql.cursors import DictCursor
import traceback

class UiPipeline(object):
    def __init__(self):
        self.file = open("ui_spider.json",'a',encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False) + '\n'
        self.file.write(line)
        return item

    def spider_closed(self,spider):
        self.file.close()


#以"mysql"进行保存
class mysqlPipeline(object):
    def process_item(self, item, spider):
        big_title = item['big_title']
        url = item['url']
        image_url = item['image_url']
        small_title = item['small_title']
        ds = item['ds']

        UI = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='123456',
            db='UI',
            charset='utf8mb4',
            cursorclass=DictCursor)

        try:
            cursor = UI.cursor()  # 使用cursor()方法获取操作游标

            insert_sql = """
            insert into ui(big_title,url,image_url,small_title,ds) values ('{}','{}','{}','{}','{}')""" .format(big_title,url,image_url,small_title,ds)
            print(insert_sql)
            cursor.execute(insert_sql)  # 执行sql语句
            UI.commit()  # 提交修改
        except Exception as e:
            print(traceback.format_exc())  # 若发生异常，抛出异常原因
        finally:
            UI.close()  # 关闭连接
        return item

    pass