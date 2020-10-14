import hashlib
import re

def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()      #调用hashlib里的md5()生成一个md5 hash对象
    m.update(url)          #用update方法对url进行md5加密的更新处理


    return m.hexdigest()    #得出加密后的十六进制结果

def extract_num(text):
#从字符串提取数字
    match_re = re.match(".*?(\d+).*")
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
if __name__ =="__main__" :
    print(get_md5("https://www.lagou.com"))