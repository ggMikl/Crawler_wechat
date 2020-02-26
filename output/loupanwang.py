from selenium import webdriver
import time
import pickle
import json
import requests

from tool.webTool import session_cookies_Login as Login_sesstion
from tool.fileTool import get_local_cookies as Local_cookies

def login(account_name,password):
    # 用webdriver启动谷歌浏览器
    print("启动浏览器，打开楼盘网后台界面")
    #chrome启动器路径
    chrome_driver = r'C:\Users\Administrator\venv\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get("http://admin.loupan.com/login")
    time.sleep(2)
    print("正在输入楼盘网登录账号和密码......")
    # 清空账号框中的内容
    driver.find_element_by_name("name").clear()
    driver.find_element_by_name("name").send_keys(account_name)
    time.sleep(1)
    driver.find_element_by_name("password").clear()
    driver.find_element_by_name("password").send_keys(password)
    time.sleep(1)
    # 在自动输完密码之后需要手动点一下记住我
    # print("请在登录界面点击:记住账号")
    # driver.find_element_by_class_name("frm_checkbox_label").click()
    # 自动点击登录按钮进行登录
    print("输入验证码")
    time.sleep(10)
    driver.find_element_by_xpath('/html/body/div/form/fieldset/table/tbody/tr[4]/td[2]/button').click()
    print("登录成功")
    cookie_items = driver.get_cookies()
    post = {}
    # 获取到的cookies是列表形式，将cookies转成json形式并存入本地名为cookie的文本中
    cookie_items = driver.get_cookies()
    post = {}
    # 获取到的cookies是列表形式，将cookies转成json形式并存入本地名为cookie的文本中
    for cookie_item in cookie_items:
        post[cookie_item['name']] = cookie_item['value']
    cookie_str = json.dumps(post)
    with open('loupanwang_cookies.txt', 'w+', encoding='utf-8') as f:
        f.write(cookie_str)
    print("楼盘网cookies信息已保存到本地")
    f.close()
    driver.quit()
