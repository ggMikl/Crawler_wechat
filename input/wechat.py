import urllib3
from selenium import webdriver
import time
import json
import requests
import re
import random
import infoProcess.wechat_info as wechat_info

def login(account_name,password):
    # 用webdriver启动谷歌浏览器
    print("启动浏览器，打开微信公众号登录界面")
    #chrome启动器路径
    chrome_driver = r'C:\Users\Administrator\venv\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=chrome_driver)
    driver.get("https://mp.weixin.qq.com/")
    time.sleep(2)
    print("正在输入微信公众号登录账号和密码......")
    # 清空账号框中的内容
    driver.find_element_by_name("account").clear()
    driver.find_element_by_name("account").send_keys(account_name)
    time.sleep(1)
    driver.find_element_by_name("password").clear()
    driver.find_element_by_name("password").send_keys(password)
    time.sleep(1)
    # 在自动输完密码之后需要手动点一下记住我
    print("请在登录界面点击:记住账号")
    driver.find_element_by_class_name("frm_checkbox_label").click()
    time.sleep(5)
    # 自动点击登录按钮进行登录
    driver.find_element_by_class_name("btn_login").click()
    # 拿手机扫二维码！
    print("请拿手机扫码二维码登录公众号")
    time.sleep(20)
    print("登录成功")
    # cookies = driver.get_cookies()
    # 获取cookies
    cookie_items = driver.get_cookies()
    post = {}
    # 获取到的cookies是列表形式，将cookies转成json形式并存入本地名为cookie的文本中
    for cookie_item in cookie_items:
        post[cookie_item['name']] = cookie_item['value']
    cookie_str = json.dumps(post)
    with open('wechat_cookies.txt', 'w+', encoding='utf-8') as f:
        f.write(cookie_str)
    print("微信cookies信息已保存到本地")
    f.close()
    driver.quit()


def get_Content(query,cookies,session):
    # query为要爬取的公众号名称
    # 公众号主页
    url = 'https://mp.weixin.qq.com'
    # 设置headers
    header = {
        "HOST": "mp.weixin.qq.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    urllib3.disable_warnings()
    time.sleep(5)
    # 登录之后的微信公众号首页url变化为：https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=1849751598，从这里获取token信息
    response = session.get(url=url, cookies=cookies, verify=False)
    print('登录成功')
    token = re.findall(r'token=(\d+)', response.url)[0]
    print(token)
    print('获取token')
    time.sleep(2)
    # 搜索微信公众号的接口地址
    search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?'
    # 搜索微信公众号接口需要传入的参数，有三个变量：微信公众号token、随机数random、搜索的微信公众号名字
    query_id = {
        'action': 'search_biz',
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'query': query,
        'begin': '0',
        'count': '5'
    }
    # 打开搜索微信公众号接口地址，需要传入相关参数信息如：cookies、params、headers
    search_response = session.get(
        search_url,
        cookies=cookies,
        headers=header,
        params=query_id)
    # 取搜索结果中的第一个公众号
    lists = search_response.json().get('list')[0]
    # 获取这个公众号的fakeid，后面爬取公众号文章需要此字段
    fakeid = lists.get('fakeid')
    # 微信公众号文章接口地址
    appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
    begin = '0'
    query_id_data = {
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'action': 'list_ex',
        'begin': '{}'.format(begin),
        'count': '5',
        'query': '',
        'fakeid': fakeid,
        'type': '9'
    }
    time.sleep(2)
    query_fakeid_response = requests.get(
        appmsg_url,
        cookies=cookies,
        headers=header,
        params=query_id_data)
    fakeid_list = query_fakeid_response.json().get('app_msg_list')
    link = fakeid_list[0].get('link')
    title = fakeid_list[0].get('title')
    content = wechat_info.html_to_mySoup(session.get(link, cookies=cookies, verify=False).content)
    #获取文章路径
    print('获取文章路径: ' + link)
    #获取文章标题
    print('获取文章标题: ' +title)
    return {
        'title':title,
        'content':content
    }

def dowload_img(content,file,session,cookies):
    img_urls = wechat_info.get_img_urls(content)
    wechat_info.dowload_wechat_img(img_urls,file,session,cookies)
    print('图片下载完成')

def out_file(content,fileName,img_net,query):
    js_content = content['content']
    title = content['title']
    wechat_info.sub_img(js_content)
    wechat_info.recur_contents(js_content)
    list = wechat_info.getOutList()
    wechat_info.out_file(fileName,list,img_net,title,query)
