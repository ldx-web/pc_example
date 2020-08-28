# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymysql
from pymysql.cursors import DictCursor
import traceback
#以json进行保存
class TencentPipeline(object):
    def __init__(self):
        self.file = open("tencent_spider.json", 'a', encoding='utf-8')
    def process_item(self,item,spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item
    def spider_closed(self,spider):
        self.file.close()


#以mysql数据库进行保存

class mysqlPipeline(object):
    def process_item(self, item, spider):
        LocationName = item['LocationName']
        Responsibility = item['Responsibility']
        Requirement = item['Requirement']
        PostURL = item['PostURL']
        RecruitPostName = item['RecruitPostName']
        RecruitPostId = item['RecruitPostId']

        article_spider = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='123456',
            db='article_spider',
            charset='utf8mb4',
            cursorclass=DictCursor)

        try:
            cursor = article_spider.cursor()  # 使用cursor()方法获取操作游标

            insert_sql = '''insert into Tencent(LocationName,Responsibility,Requirement,PostURL,RecruitPostName,RecruitPostId) values ('{}','{}','{}','{}','{}',{})'''.format(
                LocationName, Responsibility, Requirement, PostURL,RecruitPostName,RecruitPostId)
            print(insert_sql)
            cursor.execute(insert_sql)  # 执行sql语句
            article_spider.commit()  # 提交修改

        except Exception as e:
            print(traceback.format_exc())  # 若发生异常，抛出异常原因
        finally:
            article_spider.close()  # 关闭连接
        return item
    pass


