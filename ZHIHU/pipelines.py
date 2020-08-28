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
from ZHIHU.items import question_ZhihuItem,answer_ZhihuItem

#以".txt"文档进行保存
class ZhihuPipeline(object):
    def process_item(self,item,spider):
        self.file = open("/Users/lidongxue/pcfile/zhihu.txt", "a", encoding="utf-8")
        line = json.dumps(dict(item),ensure_ascii=False) + '\n'
        self.file.write(line)
        return item
    def spider_closed(self,spider):
        self.file.close()

#以"mysql"进行保存
class mysqlPipeline(object):
    def process_item(self, item, spider):
        if type(item) == question_ZhihuItem:                  #当有多个item项目需要保存时
            question_id = item['question_id']
            question_name = item['question_name']
            q_headline = item['q_headline']
            title = item['title']
            q_content = item['q_content']
            q_excerpt = item['q_excerpt']
            q_excerpt_new = item['q_excerpt_new']
            answer_count = item['answer_count']
            c_count = item['c_count']
            created_time = item['created_time']
            updated_time = item['updated_time']
            visited_count = item['visited_count']
            answer_id = item['answer_id']

            ZHIHU = pymysql.connect(
                host='127.0.0.1',
                user='root',
                passwd='123456',
                db='ZHIHU',
                charset='utf8mb4',
                cursorclass=DictCursor)

            try:
                cursor = ZHIHU.cursor()  # 使用cursor()方法获取操作游标
                insert_sql = '''insert into question_info(question_id,question_name,q_headline,title,q_content,q_excerpt,q_excerpt_new,answer_count,c_count,created_time,updated_time,visited_count,answer_id) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format(
                    question_id,question_name,q_headline,title,q_content,q_excerpt,q_excerpt_new,answer_count, c_count ,created_time,updated_time,visited_count,answer_id)
                print(insert_sql)
                cursor.execute(insert_sql)  # 执行sql语句
                ZHIHU.commit()  # 提交修改

            except Exception as e:
                print(traceback.format_exc())  # 若发生异常，抛出异常原因
            finally:
                ZHIHU.close()  # 关闭连接
            return item

        else:
            Rely_q_title = item['Rely_q_title']
            author_name = item['author_name']
            a_headline = item['a_headline']
            a_excerpt = item['a_excerpt']
            a_content = item['a_content']
            created_time = item['created_time']
            updated_time = item['updated_time']
            comment_count = item['comment_count']

            ZHIHU = pymysql.connect(
                host='127.0.0.1',
                user='root',
                passwd='123456',
                db='ZHIHU',
                charset='utf8mb4',
                cursorclass=DictCursor)
            try:
                cursor = ZHIHU.cursor()  # 使用cursor()方法获取操作游标

                insert_sql = '''insert into answer_info(Rely_q_title,author_name,a_headline,a_excerpt,a_content,created_time,updated_time,comment_count) values ('{}','{}','{}','{}','{}','{}','{}','{}')'''.format(
                Rely_q_title,author_name,a_headline,a_excerpt,a_content,created_time,updated_time,comment_count)
                print(insert_sql)
                cursor.execute(insert_sql)  # 执行sql语句
                ZHIHU.commit()  # 提交修改

            except Exception as e:
                print(traceback.format_exc())  # 若发生异常，抛出异常原因
            finally:
                ZHIHU.close()  # 关闭连接
            return item