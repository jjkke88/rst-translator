#coding=utf-8
import os
import re
import requests
import time
import random
import json
from hashlib import md5
from bs4 import BeautifulSoup 
import unicodedata  

# Set your own appid/appkey.
appid = '20230925001829396'
appkey = 'be6TrvYdQT7qefbhaKwu'

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path
query = 'Hello World! This is 1st paragraph.This is 2nd paragraph.'


def contains_chinese(s):  
    chinese_texts = re.findall(u'[\u4e00-\u9fa5]+', s)  
    if len(chinese_texts) != 0:
        return True
    return False

# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

def baidu_api(query,from_lang,to_lang):
    time.sleep(0.2)
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    print(str(r))
    result = r.json()
    if result.get("trans_result"):
        return result["trans_result"][0]["dst"]
    else:
        print("翻译API请求失败")
        return query
  
def translate_chinese_to_english(text):  
    chinese_texts = re.findall(u'[\u4e00-\u9fa5]+', text)  
    if len(chinese_texts) != 0: 
        # 繁体：cht 简体 zh 英文 en
        trans_text = baidu_api(text, from_lang, to_lang)
        print(text, " ====> ", trans_text)
        return trans_text
    else:
        return text
  
def replace_chinese_with_english(text):  
    # # 使用正则表达式找到所有中文字符  
    # chinese_texts = re.findall(u'[\u4e00-\u9fa5]+', text)  
    # 按行拆分文本  
    lines = text.split("\n")  
    
    # 去除每行前后的空格和换行符  
    stripped_lines = [line.strip() for line in lines] 
    for line in stripped_lines:
        if to_lang == "cht":
            chinese_texts = re.findall(u'[\u4e00-\u9fa5]+', line)  
            for cht_text in chinese_texts:
                english_text = translate_chinese_to_english(cht_text)  
                text = text.replace(cht_text, english_text)  
        else:
            lst_tets = line.split(' ')
            for lst_tet in lst_tets:
                if contains_chinese(lst_tet):
                    english_text = translate_chinese_to_english(lst_tet) 
                    matches = re.findall(r'\`(.*?)\`', english_text)  
                    # 在匹配到的内容前后插入空格
                    for match in matches:  
                        english_text = english_text.replace('`' + match + '`', '`' + match + '` ')
                    text = text.replace(lst_tet, english_text)

    return text

if __name__ == "__main__":
    path = "C:/Users/yupei.wu/Downloads/documents/docs-others"
    # # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
    from_lang = 'zh'
    to_lang =  'en'
    def find_rst_files(directory):  
        rst_files = []  
        for root, dirs, files in os.walk(directory):  
            for file in files:  
                if file.endswith('.rst') or file.endswith('.cpp') or file.endswith(".cs") or file.endswith(".hpp"):  
                    rst_files.append(os.path.join(root, file))  
        return rst_files
    
    all_rst_files = find_rst_files(path)

    for rst_file in all_rst_files:
        print("正在处理：", rst_file)
        print("===========================")
        # 打开文件
        file = open(rst_file, encoding="utf-8")
        trans_text = file.read()
        file.close()
        # 翻译
        trans_content = replace_chinese_with_english(trans_text)
        print(trans_content)
        # 存储
        base_name = os.path.basename(rst_file)
        target_file_path = rst_file.replace("documents/docs-others", "documents/docs-others-trans")
        with open(target_file_path, 'w', encoding="utf-8") as f2:
            f2.write(trans_content)
