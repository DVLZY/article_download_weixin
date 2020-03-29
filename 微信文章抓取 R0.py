# 这个写到一般还没写完
# pycharm
# python3.8.2
# utf-8
#todo(lin) 使用时间戳清洗数据
import requests
import json
import re
import re
import time
import json
import requests
from selenium import webdriver


header = {
    "HOST": "mp.weixin.qq.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
}

driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\chromedriver.exe")  # 引入chrome驱动
driver.get('https://mp.weixin.qq.com/')  # 打开目标网址

time.sleep(1)
driver.find_element_by_xpath('.//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[1]/div/span/input').clear()
driver.find_element_by_xpath('.//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[1]/div/span/input').send_keys(
    'linzeyu@live.com')  # 输入账号
driver.find_element_by_xpath('.//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[2]/div/span/input').clear()
driver.find_element_by_xpath('.//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[2]/div/span/input').send_keys(
    'Lzy&1123')  # 输入密码
driver.find_element_by_xpath('.//*[@id="header"]/div[2]/div/div/div[1]/form/div[4]/a').click()  # 点击登入按钮
time.sleep(10)
driver.find_element_by_xpath('.//*[@id="menuBar"]/li[5]/ul/li[3]/a/span/span').click()  #点击素材管理按钮
driver.find_element_by_xpath('.//*[@id="js_main"]/div[3]/div[1]/div[2]/button').click()  #点击新建图文按钮
time.sleep(5)
cookies = driver.get_cookies()  # 获取cookies（分析cookies的时候主要关注name和value）
post = dict()       # 建立cookies字典
for cookie_item in cookies:
    post[cookie_item.get('name')] = cookie_item.get('value')
cookie_str = json.dumps(post)
cookie_str = json.loads(cookie_str)

rst = requests.get('https://mp.weixin.qq.com/', cookies=cookie_str)
token = re.findall(r'token=(.*)', rst.url)[0]
print(token)

search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz'
search_dict = {
    'action': 'search_biz',
    'begin': '0',  # 起始页
    'count': '5',
    'query': 'aikeai',  # 搜索关键词
    'token': token,
    'lang': 'zh_CN',
    'f': 'json',
    'ajax': '1'
}

header = {
    "Host": "mp.weixin.qq.com",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

search_rst = requests.get(search_url, headers=header,cookies=cookie_str, params=search_dict)
fakeid = search_rst.json().get('list')[0].get('fakeid')
print(fakeid)

driver.close()  # 关闭浏览器