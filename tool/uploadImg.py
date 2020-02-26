import os
from requests_toolbelt.multipart.encoder import MultipartEncoder
import random
import re
import requests
import json
import time
from tool.webTool import session_cookies_Login as Login_session

p = re.compile(r'(?<=var redis_key = )[\'](.*?)[\']')


#构造mul返回这个与图片对应的dict
def createMultipart(file,img_name,num):
    # file = 'E:/lp_Crawler/weixin/微信图片_20191227090239.jpg'
    multipart_encoder = MultipartEncoder(
        fields={
            'id': 'WU_FILE_' + str(num),
            'upfile': (img_name, open(file + '\\' + img_name, 'rb'), 'image/jpeg')
        },
        boundary='-----------------------------' + str(random.randint(1e28, 1e29 - 1))
    )
    return multipart_encoder

def creatImgDict(img_path):
    # dirs = os.listdir(img_path)
    img_dict = {}
    count = 0
    for file in os.listdir(img_path):
        count = count + 1
        img_dict[re.findall(('([^.]+)'),file)[0]] = createMultipart(img_path, file, count)
    return img_dict



#上传图片
 #返回网络地址

def initParams(redis_key):
    return {
        'dir': 'newsimg/image',
        'redis_key': redis_key,
        'type': '1',
        'action': 'uploadimage',
        'encode': 'utf-8',
        'isWatermark': '0'
    }
def initHeaders():
    return {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control':'no-cache',
    'Connection': 'keep-alive',
    'Host': 'cs.loupan.com',
    'Origin': 'http://admin.loupan.com',
    'Pragma': 'no-cache',
    'Referer': 'http://admin.loupan.com/public/ueditor/dialogs/image/image.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'X_Requested_With': 'XMLHttpRequest'
}

def getImgNet(url,img_dict,redis_key):
    img_net = {}
    headers = initHeaders()
    params = initParams(redis_key)
    for img in img_dict:
        headers['Content-Type'] = img_dict[img].content_type
        img_net[re.findall(('([^.]+)'),img)[0]] = json.loads(requests.post(url, data=img_dict[img], headers=headers, params=params).text)['url'].replace('\\', '')
        print(img + ':上传成功')
        time.sleep(random.randint(1, 2))
    return img_net

def uploadImg(session,cookie,img_path,url):
    redis_key = p.findall(Login_session(session,cookie, 'http://admin.loupan.com/news/add'))[0]
    print(redis_key)
    img_dict = creatImgDict(img_path)
    img_net = getImgNet( url,img_dict, redis_key)
    print(img_net)
    return img_net








