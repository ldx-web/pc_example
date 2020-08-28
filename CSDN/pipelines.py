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

#以"json"文档进行保存
# class CsdnPipeline:
#     def __init__(self):
#         self.file = open("csdn2222.json",'w',encoding='utf-8')
#     def process_item(self, item, spider):
#         line = json.dumps(dict(item),ensure_ascii=False) + '\n'
#         self.file.write(line)
#         return item
#     def spider_closed(self,spider):
#         self.file.close()



#以".txt"文档进行保存
class CsdnPipeline(object):
    def process_item(self,item,spider):
        self.file = open("/Users/lidongxue/pcfile/csdn.txt", "a", encoding="utf-8")
        line = json.dumps(dict(item),ensure_ascii=False) + '\n'
        self.file.write(line)
        return item
    def spider_closed(self,spider):
        self.file.close()

#以"mysql"进行保存
class mysqlPipeline(object):
    def process_item(self, item, spider):
        title = item['title']
        url = item['url']
        user_name = item['user_name']
        nickname = item['nickname']
        comments = item['comments']
        ds = item['ds']
        id = item['id']
        tp = item['tp']
        shown_offset = item['shown_offset']

        CSDN = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='123456',
            db='CSDN',
            charset='utf8mb4',
            cursorclass=DictCursor)

        try:
            cursor = CSDN.cursor()  # 使用cursor()方法获取操作游标

            insert_sql = """
            insert into csdn(title,url,user_name,nickname,comments,ds,id,tp,shown_offset) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}')""" .format(title,url,user_name,nickname,comments,ds,id,tp,shown_offset)
            print(insert_sql)
            cursor.execute(insert_sql)  # 执行sql语句
            CSDN.commit()  # 提交修改

        except Exception as e:
            print(traceback.format_exc())  # 若发生异常，抛出异常原因
        finally:
            CSDN.close()  # 关闭连接
        return item

    pass