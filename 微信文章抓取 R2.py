# pycharm
# python3.8.2
# utf-8
# todo(lin) 使用时间戳清洗数据，过滤出当天的文章
# todo(lin) 引入读取txt文本的功能，批量访问微信号
# todo(lin) 写入文件小概率报错，抓取文章列表报错
# 账号频繁爬取触发异常，更换账号就行
# todo 添加异常处理

import re
import time
from selenium import webdriver

driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\chromedriver.exe")  # 引入chrome驱动
driver.get('https://mp.weixin.qq.com/')  # 打开目标网址
driver.maximize_window()
time.sleep(1)
driver.find_element_by_xpath('.//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[1]/div/span/input').clear()
driver.find_element_by_xpath('.//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[1]/div/span/input').send_keys('XXXXXX')  # 输入账号
time.sleep(1)
driver.find_element_by_xpath('.//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[2]/div/span/input').clear()
driver.find_element_by_xpath('.//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[2]/div/span/input').send_keys('XXXXXXX')  # 输入密码
time.sleep(1)
driver.find_element_by_xpath('.//*[@id="header"]/div[2]/div/div/div[1]/form/div[4]/a').click()  # 点击登入按钮
time.sleep(8)   # 手机扫码
driver.find_element_by_xpath('.//*[@id="menuBar"]/li[7]/ul/li[3]/a').click()                #点击 素材管理
time.sleep(1)
driver.find_element_by_xpath('.//*[@id="js_main"]/div[3]/div[1]/div[2]/button').click()     #点击 新建图文
time.sleep(1)
current_windows = driver.window_handles         # 获取当前所有浏览器页面窗口
driver.switch_to.window(current_windows[0])     # 切换到第一个窗口
driver.close()
current_windows = driver.window_handles         # 获取当前所有浏览器页面窗口
driver.switch_to.window(current_windows[0])     # 切换到第一个窗口
time.sleep(1)
driver.find_element_by_xpath('.//*[@id="vue_app"]/div[6]/div[1]/div/div[3]/button').click()     #关闭提示框
time.sleep(1)
driver.find_element_by_xpath('.//*[@id="js_editor_insertlink"]').click()                        #点击超链接按钮

def get_artist_list(weixin_name,):
    driver.find_element_by_xpath('.//*[@id="vue_app"]/div[5]/div[1]/div/div[2]/div[2]/form[1]/div[3]/div/div/p/button').click() #选择公众号输入
    driver.find_element_by_xpath('.//*[@id="vue_app"]/div[5]/div[1]/div/div[2]/div[2]/form[1]/div[3]/div/div/div/div/span/input').send_keys(weixin_name)  # 输入要搜索的公众号名称
    driver.find_element_by_xpath('.//*[@id="vue_app"]/div[5]/div[1]/div/div[2]/div[2]/form[1]/div[3]/div/div/div/div/span/span/button[2]/div').click()  # 点击确认搜索
    time.sleep(2)
    driver.find_element_by_xpath('.//*[@id="vue_app"]/div[5]/div[1]/div/div[2]/div[2]/form[1]/div[3]/div/div/div/div[2]/ul/li[1]/div[1]').click()       # 选择第一个公众号
    time.sleep(3)
    weixin_rst = driver.find_element_by_class_name('inner_link_article_list').get_attribute('innerHTML')       # 获取列表的代码
    title = re.compile('"inner_link_article_title">(.*?)</div',re.S).findall(weixin_rst)
    date = re.compile('"inner_link_article_date">(.*?)</div',re.S).findall(weixin_rst)
    link = re.compile('<a href="(.*?)"',re.S).findall(weixin_rst)
    time.sleep(2)
    return title,date,link

weixin_list = [
    "BailuTown",
    "baoshancun1983",
    "成都大熊猫繁育研究基地",
    "gjfybly",
    "gstx2007",
    "floralandchengdu",
    "hysj728",
    "成都海昌极地海洋公园资讯",
    "cdhlg2012",
    "成都七彩海巢欢乐世界",
    "cdsjzgz",
    "成都松鼠部落",
    "cdteddybearmuseum",
    "weiranhuahaid",
    "成都蔚然花海景区官方号",
    "KongLin2013",
    "cdwuhouci",
    "valleyflor",
    "cjchaxiang",
    "CZTYBWG",
    "czsytgz",
    "chuancaibowuguan",
    "EastCD",
    "东来桃源",
    "cxgdjy",
    "hongkoulvyou",
    "dfctbwg",
    "佛山古寺",
    "floraland",
    "Ifloraland",
    "gstxthsj",
    "floraland01",
    "gstx22",
    "CDhnryjnz",
    "heihunongzhuang",
    "虹口花谷",
    "scdjyhongkoupiaoliu",
    "hmtx525499",
    "hwrj-82555666",
    "花舞人间票务",
    "hxgj028",
    "cxzhjq",
    "lszy-gov",
    "大邑新场古镇旅游",
    "schlxgz",
    "黄龙溪欢乐田园",
    "jc-museum",
    "jzqyly",
    "锦门丝绸世界",
    "锦绣安仁花卉公园",
    "kzxzkzxz",
    "luodaigov",
    "manhuazhuangyuan",
    "meiguihuaxigu_520",
    "美丽乡村青杠树",
    "nhdreamland",
    "nhmhd61906688",
    "nkcun123456",
    "cdnongyuan",
    "scpzdjs",
    "CDWLQZGS",
    "PLGZ-TTS",
    "七彩海巢欢乐世界",
    "QCS_DJY",
    "青城山-都江堰景区",
    "青城山都江堰门票管理处",
    "qyglzsy2010",
    "qlzhuxihu",
    "泉映梨花一清流",
    "loveshuixianghuili",
    "SSHXAAAA",
    "神秘园玫瑰花溪谷",
    "selake",
    "shixianghujq",
    "ishuguojuandu",
    "sctfkqy",
    "scwhcly",
    "四川玉皇养生谷景区",
    "tqly_CD",
    "huaxigu",
    "tfnby123",
    "weiranhuahai",
    "wufengxijingqu",
    "ROSEDEMAI2016",
    "西岭雪山景区",
    "xianhuashangu",
    "xinjinlihuaxi",
    "bzljq1",
    "xftylydjcl",
    "罨画池",
    "罨画池文创中心"
]   # 要爬取的公众号列表

for i in weixin_list:
    wx_title,wx_date,wx_link = get_artist_list(i)
    for j in range(len(wx_link)):
        weixin_rst = wx_date[j]+'\t'+i+'\t'+wx_title[j]+'\t'+wx_link[j]
        print(weixin_rst)
        # with open('微信数据' + time.strftime('%Y-%m-%d') + '.txt', 'a+') as f:
        #     f.write(str(weixin_rst)+'\n')

driver.quit()  # 关闭浏览器