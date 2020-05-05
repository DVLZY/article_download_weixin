# pycharm
# python3.8.2
'''
更新说明：
1、优化了Xpath规则，增大容错率
2、自动根据当前时间创建文件
3、引入读取txt文本的功能，批量访问微信号
 # todo 获取文章列表 优化隐式等待
 # todo 写入文件小概率报错，抓取文章列表报错
 # todo 异常处理（读取不到文件）
 简单说明
1、一共是两个文件，第一个是爬虫程序，另一个是景区公众号列表，这俩要放在一起，景区.txt不能改名
2、首次运行之前要安装chromedriver（安装一次，终身可用），安装方法 https://www.cnblogs.com/lfri/p/10542797.html 简单来说就是下载对应版本的chromedriver然后放到chrome安装目录就行
3、注册几个微信个人订阅号（不用认证），爬虫请求太频繁会被限制，这个时候把景区.txt中账号密码的部分替换一下，然后重新运行就行
4、如果闪退了，可以看看（微信数据.txt）之前爬到哪里了，然后把已经爬过的部分的在 景区.txt中删除（记得备份景区.txt），爬虫就会直接爬取剩余的部分
5、理论上可以多开。假设你要多开5个，那你把景区.txt的账密可以不变（当然账密如果能不同，那更保险）然后景区列表分成5份就行
使用说明
1、运行爬虫后会弹出一个黑框框，然后会自动打开浏览器，这个浏览器不要关闭他，不要保持最大化，（你可以做别的，但是浏览器要保持打开，这个浏览器窗口和你正常的窗口是独立的两个进程）
2、需要在手机上扫码确认登入微信公众号，登入成功之后，回到黑框框输入任意内容，回车，程序就会继续运行。
3、运行过程中，不要 不要 不要 移动，关闭，以及点击这个自动控制的浏览器中任何内容

###如果有问题，记得告诉我错误信息，或者描述错误发生情况。###
'''
# 使用说明
print('''

使用说明:
    1.请将‘景区.txt’和程序放在一起
    2.将公众号的账户和密码分别填入第二行和第三行
    3.请提前准备好手机进行扫码
    4.账号频繁爬取触发异常，更换账号就行
    5.生成的文件，直接复制到Excel按照制表符，分列即可

    正在加载中，请稍后...
''')

import re,sys,io
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys # 键盘按键模拟
from selenium.webdriver.common.action_chains import ActionChains # 鼠标按键模拟
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') # fixed bug UnicodeEncodeError: 'gbk' codec can't encode character '\u200b'

# 获取当前时间
now_time = time.strftime('%Y-%m-%d %H-%M-%S')
now_date = time.strftime('%Y-%m-%d')

# 配置代理
# chromeOptions = webdriver.ChromeOptions()
# chromeOptions.add_argument('--proxy-server=http://120.234.138.99:53779')
# driver = webdriver.Chrome(chrome_options=chromeOptions)

# 读取 景区.txt 文件
with open('景区.txt','r', encoding='utf-8') as f:
    for weixin_list in f:
        weixin_list=f.read().splitlines()

# 登入公众号
driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\chromedriver.exe")  # 引入chrome驱动
driver.get('https://mp.weixin.qq.com/')  # 打开目标网址
driver.maximize_window() # 最大化窗口
time.sleep(1)
driver.find_element_by_xpath('.//input[@name="account"]').clear()
driver.find_element_by_xpath('.//input[@name="account"]').send_keys(weixin_list[0])  # 输入账号
driver.find_element_by_xpath('//input[@name="password"]').clear()
driver.find_element_by_xpath('//input[@name="password"]').send_keys(weixin_list[1])  # 输入密码
time.sleep(1)
driver.find_element_by_xpath('//a[@title="点击登录"]').click()  # 点击登入按钮
input('扫码完成后请点击任意键继续！')

# 进入文章列表页
driver.find_element_by_xpath('.//li[@title="素材管理"]/a').click()                  # 点击 素材管理
time.sleep(1)
driver.find_element_by_xpath("//button[contains(text(),'新建图文消息')]").click()     # 点击 新建图文
time.sleep(1)
current_windows = driver.window_handles         # 获取当前所有浏览器页面窗口
driver.switch_to.window(current_windows[0])     # 切换到第一个窗口
driver.close()
current_windows = driver.window_handles         # 获取当前所有浏览器页面窗口
driver.switch_to.window(current_windows[0])     # 切换到第一个窗口
time.sleep(1)
iknow = driver.find_element_by_xpath('//*[@id="vue_app"]/div[7]/div[1]/div/div[3]/button')  # 关闭提示框
action = ActionChains (driver)
action.move_to_element(iknow).click(iknow).perform() #
time.sleep(1)
driver.find_element_by_xpath('.//*[@id="js_editor_insertlink"]').click()    # 点击超链接按钮

def get_artist_list(weixin_name,):
    '''
    获取列表中所有景区的近期推文
    :param weixin_name: 景区列表
    :return:
    '''
    driver.find_element_by_xpath('//p/button').click() #选择公众号输入
    driver.find_element_by_xpath('//div[@class="inner_link_account_area"]//input').send_keys(weixin_name)  # 输入要搜索的公众号名称
    driver.find_element_by_xpath('//div[@class="inner_link_account_area"]//input').send_keys(Keys.ENTER)  # 点击确认搜索
    time.sleep(2)
    driver.find_element_by_xpath('//ul[@class="inner_link_account_list"]/li[1]').click()       # 选择第一个公众号
    name = driver.find_element_by_xpath('//p[@class="inner_link_account_msg"]').get_attribute('innerText').replace('选择其他公众号','') # 公众号名称
    time.sleep(4)
    weixin_rst = driver.find_element_by_class_name('inner_link_article_list').get_attribute('innerHTML')
    date = re.compile('"inner_link_article_date">(.*?)</div',re.S).findall(weixin_rst) # 公众号 发文日期
    title = re.compile('"inner_link_article_title">(.*?)</div',re.S).findall(weixin_rst) # 公众号 文章标题
    link = re.compile('<a href="(.*?)"',re.S).findall(weixin_rst) # 公众号 文章链接
    return date,title,link,name

# 写入文件
# 写入标题
with open('微信数据 ' + now_time + '.txt', 'a+',encoding='utf-8') as f:
    f.write('公众号名称\t发文日期\t文章标题\t文章链接\n')
# 写入内容
for i in weixin_list[3:]:
    wx_title,wx_date,wx_link,we_name = get_artist_list(i)
    for j in range(len(wx_link)):
        weixin_rst = we_name +'\t'+ wx_date[j]+'\t'+wx_title[j]+'\t'+wx_link[j]
        print(weixin_rst)
        with open('微信数据 ' + now_time + '.txt', 'a+',encoding='utf-8') as f:
            f.write(str(weixin_rst)+'\n')
            f.flush() # 刷新硬盘缓存，及时写入文件

driver.quit()  # 关闭浏览器
input('爬取完成 请按任意键退出')
time.sleep(3)


