# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import traceback
import pymysql
from pymysql.cursors import DictCursor


class JuejinPipeline:
    def __init__(self):
        self.file = open("juejin_spider.json", 'a',encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False) + '\n'
        self.file.write(line)
        return item
    def spider_closed(self,spider):
        self.file.close()


#以mysql数据库进行保存
# class mysqlPipeline(object):
#     def process_item(self, item, spider):
#
#         user_id = item['user_id']
#         title = item['title']
#         mark_content = item['mark_content']
#         user_name = item['user_name']
#         description = item['description']
#         got_view_count = item['got_view_count']
#         category_name = item['category_name']
#         tag_name = item['tag_name']
#         concern_user_count = item['concern_user_count']
#         ctime = item['ctime']
#
#
#         juejin = pymysql.connect(
#             host='127.0.0.1',
#             user='root',
#             passwd='123456',
#             db='juejin',
#             charset='utf8mb4',
#             cursorclass=DictCursor)
#
#         try:
#             cursor = juejin.cursor()  # 使用cursor()方法获取操作游标
#             mark_content = pymysql.escape_string(mark_content).strip().replace('\n','').replace('\t','').replace('\n','').replace('\n','').replace('\n','');
#             print(mark_content)
#
#
#             insert_sql = """insert into juejin(user_id,title,mark_content,user_name,description,got_view_count,category_name,tag_name,concern_user_count,ctime) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(
#                 user_id,title, mark_content,user_name,description,got_view_count,category_name,tag_name,concern_user_count,ctime)
#             print(insert_sql)
#             cursor.execute(insert_sql)  # 执行sql语句
#             juejin.commit()  # 提交修改
#
#         except Exception as e:
#             print(traceback.format_exc())  # 若发生异常，抛出异常原因
#         finally:
#             juejin.close()  # 关闭连接
#         return item
#     pass

