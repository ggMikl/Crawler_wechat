import requests
from retrying import retry
import json
import pickle
import time
from requests.cookies import RequestsCookieJar

def get_html(url):
    strhtml = requests.get(url)
    return strhtml

def loot_url(url_,num):
    group_url = []
    num = num + 1
    for i in range(1, num):
        url_num = i
        url = url_ + str(url_num)
        group_url.append(url)
    return group_url

@retry(stop_max_attempt_number=5, wait_fixed=1000)
def requests_cookies_Login(cookies , url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Connection': 'keep-alive',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cookie': cookies
    }
    return requests.get(url, headers=header, timeout=1).content.decode()

@retry(stop_max_attempt_number=5, wait_fixed=1000)
def session_cookies_Login(session,cookies , url):
    return session.get(url, cookies=cookies, verify=False).content.decode()

# @retry(stop_max_attempt_number=5, wait_fixed=1000)
def dowload_img(img_url,img_name,flie):
    print('进入dowload')
    print(img_url)
    flie = flie + "\\" + "img_name"
    r = requests.get(img_url,stream=True)
    print(r.status_code)
    # if r.status_code == 302:  # 此时ip被封了，需要代理池poxy
    #     print('此时ip被封了，需要代理池poxy')
    # urllib.request.urlretrieve(img_url,flie.replace('img_name', img_name))
    with open(flie.replace('img_name', img_name), 'wb') as f:
        f.write(r.content)
        print('写入文档')
    f.close()

def get_session(keep_alive,DEFAULT_RETRIES):
    session = requests.Session()
    session.keep_alive = keep_alive
    # 增加重试连接次数
    session.adapters.DEFAULT_RETRIES = DEFAULT_RETRIES
    return session

