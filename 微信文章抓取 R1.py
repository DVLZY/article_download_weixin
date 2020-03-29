# pycharm
# python3.8.2
# utf-8
#todo(lin) 使用时间戳清洗数据
import re
import time
from selenium import webdriver

driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\chromedriver.exe")  # 引入chrome驱动
driver.get('https://mp.weixin.qq.com/')  # 打开目标网址

time.sleep(1)
driver.find_element_by_xpath('.//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[1]/div/span/input').clear()
driver.find_element_by_xpath('.//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[1]/div/span/input').send_keys('XXXXX@live.com')  # 输入账号
driver.find_element_by_xpath('.//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[2]/div/span/input').clear()
driver.find_element_by_xpath('.//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[2]/div/span/input').send_keys('XXXXXX')  # 输入密码
driver.find_element_by_xpath('.//*[@id="header"]/div[2]/div/div/div[1]/form/div[4]/a').click()  # 点击登入按钮

time.sleep(8)
driver.find_element_by_xpath('.//*[@id="menuBar"]/li[5]/ul/li[3]/a').click()                #点击 素材管理
driver.find_element_by_xpath('.//*[@id="js_main"]/div[3]/div[1]/div[2]/button').click()     #点击 新建图文
time.sleep(1)
current_windows = driver.window_handles         # 获取当前所有浏览器页面窗口
driver.switch_to.window(current_windows[1])     # 切换到第二个窗口
time.sleep(1)
driver.find_element_by_xpath('.//*[@id="vue_app"]/div[6]/div[1]/div/div[3]/button').click()     #关闭提示框
driver.find_element_by_xpath('.//*[@id="js_editor_insertlink"]').click()                        #点击超链接按钮

def get_artist_list(weixin_name,):
    driver.find_element_by_xpath('.//*[@id="vue_app"]/div[5]/div[1]/div/div[2]/div[2]/form[1]/div[3]/div/div/p/button').click() #选择公众号输入
    driver.find_element_by_xpath('.//*[@id="vue_app"]/div[5]/div[1]/div/div[2]/div[2]/form[1]/div[3]/div/div/div/div/span/input').send_keys(weixin_name)  # 输入要搜索的公众号名称
    driver.find_element_by_xpath('.//*[@id="vue_app"]/div[5]/div[1]/div/div[2]/div[2]/form[1]/div[3]/div/div/div/div/span/span/button[2]/div').click()  # 点击确认搜索
    time.sleep(1)
    driver.find_element_by_xpath('.//*[@id="vue_app"]/div[5]/div[1]/div/div[2]/div[2]/form[1]/div[3]/div/div/div/div[2]/ul/li[1]/div[1]').click()       # 选择第一个公众号
    time.sleep(1)
    weixin_rst = driver.find_element_by_class_name('inner_link_article_list').get_attribute('innerHTML')       # 获取列表的代码
    title = re.compile('"inner_link_article_title">(.*?)</div',re.S).findall(weixin_rst)
    date = re.compile('"inner_link_article_date">(.*?)</div',re.S).findall(weixin_rst)
    link = re.compile('<a href="(.*?)"',re.S).findall(weixin_rst)
    time.sleep(1)
    return title,date,link

weixin_list = ['杨晨大神','aikayangmao','bsbcreditcard','CSDNLIB']

for i in weixin_list:
    wx_title,wx_date,wx_link = get_artist_list(i)
    for j in range(len(wx_link)):
        weixin_rst = wx_date[j]+'\t'+i+'\t'+wx_title[j]+'\t'+wx_link[j]
        print(weixin_rst)
        with open('微信数据' + time.strftime('%Y-%m-%d') + '.txt', 'a+') as f:
            f.write(str(weixin_rst)+'\n')

driver.quit()  # 关闭浏览器
