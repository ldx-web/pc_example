# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import traceback

#方法一：以json格式进行保存
class LcspiderPipeline:
    def __init__(self):
         self.file = open("liangcang.json", "a", encoding="utf-8")

    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False) + '\n'  # json中的dumps和dump是序列化的方法，dumps以字符串str进行保存，json默认是ASCII的形式，并不是以真正的中文进行保存，若想以真正的中文进行保存，需要将ensure_ascii=False
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()

#方法二：以数据库形式进行保存
import pymysql
# import traceback
class mysqlPipeline(object):
    def process_item(self, item, spider):
        brand = item['brand']
        title = item['title']
        price = item['price']
        url = item['url']
        article_spider = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='123456',
            db='article_spider',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

        try:
            cursor = article_spider.cursor()   #使用cursor()方法获取操作游标
            #
            # content = content.replace("'", '"')     #因为网站文本处的内容不符合sql语句，可在insert_sql处打断点，将其copy value拷贝到sql数据库中的新建查询进行查看
            # content = "'" + content + "'"
            # name = name.replace("'", '"')
            # name = "'" + name + "'"
            # url = url.replace("'", '"')
            # url = "'" + url + "'"

            insert_sql = '''insert into LC(brand,title,price,url) values ('{}','{}','{}','{}')ON DUPLICATE KEY UPDATE url=VALUES(url)'''.format(brand, title, price, url)
            print(insert_sql)
            cursor.execute(insert_sql)       #执行sql语句
            article_spider.commit()                      #提交修改

        except Exception as e:
            print(traceback.format_exc())    #若发生异常，抛出异常原因
        finally:
            article_spider.close()                         #关闭连接
        return item