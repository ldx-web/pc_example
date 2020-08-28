# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter
import json
import pymysql
from bdtb.items import BdtbItem,ReplyBdtbItem
from pymysql.cursors import DictCursor
import traceback

#以mysql数据库进行保存
class mysqlPipeline(object):
    def process_item(self, item, spider):
        if type(item) == BdtbItem:                  #当有多个item项目需要保存时
            user_name = item['user_name']
            time = item['time']
            contents = item['contents']
            tid = item['tid']
            pid = item['pid']

            BDTB = pymysql.connect(
                host='127.0.0.1',
                user='root',
                passwd='123456',
                db='BDTB',
                charset='utf8mb4',
                cursorclass=DictCursor)

            try:
                cursor = BDTB.cursor()  # 使用cursor()方法获取操作游标

                insert_sql = '''insert into BdtbItem(user_name,time,contents,tid,pid) values ('{}','{}','{}','{}','{}')'''.format(
                    user_name,time, contents,tid,pid)
                print(insert_sql)
                cursor.execute(insert_sql)  # 执行sql语句
                BDTB.commit()  # 提交修改

            except Exception as e:
                print(traceback.format_exc())  # 若发生异常，抛出异常原因
            finally:
                BDTB.close()  # 关闭连接
            return item

        else:
            reply_name = item['reply_name']
            By_reply_name = item['By_reply_name']
            content_replied = item['content_replied']
            replay_time = item['replay_time']
            BDTB = pymysql.connect(
                host='127.0.0.1',
                user='root',
                passwd='123456',
                db='BDTB',
                charset='utf8mb4',
                cursorclass=DictCursor)
            try:
                cursor = BDTB.cursor()  # 使用cursor()方法获取操作游标

                insert_sql = '''insert into ReplyBdtbItem(reply_name,By_reply_name,content_replied,replay_time) values ('{}','{}','{}','{}')'''.format(
                reply_name, By_reply_name, content_replied, replay_time)
                print(insert_sql)
                cursor.execute(insert_sql)  # 执行sql语句
                BDTB.commit()  # 提交修改

            except Exception as e:
                print(traceback.format_exc())  # 若发生异常，抛出异常原因
            finally:
                BDTB.close()  # 关闭连接
            return item


