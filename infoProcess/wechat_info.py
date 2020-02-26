from tool.fileTool import isFile
import re
import tool.infoTool  as info_T
import time
import random
from bs4 import BeautifulSoup

input_list = []
out_list = []

def getOutList():
    return out_list

#用递归的方法把微信文章里面的内容递归出来
def recur_contents(js_content):
    if js_content:
        for i in js_content:
            if i.string != None:
                input_list.append(info_T.suop_to_string(i.string)) 
            else:
                str = ''.join(input_list)
                if str != '':
                    out_list.append(str)
                input_list.clear()
                recur_contents(i.contents)

#生成本地文件
def out_file(fileName,list,img_net,title,query):
    isFile(fileName)
    fileName = fileName + '\\' + title + '.' + 'txt'
    #清除'\xa0'
    remove_list = info_T.list_remove_n(list,'\xa0')
    fh =  open(fileName, 'a', encoding='utf-8')
    for i in remove_list:
        if re.search('(cut_img)',i):
            for j in re.findall('cut_img\d+',i):
                fh.write('<p style="text-align: center">' + '<img '+ 'src=' + '\"' + img_net[j ] + '\"' +'  title='+ '\"' + query + '\"' + '  alt=' + '\"' + query + '\"' +' />' + '</p>')
        elif i !='':
            fh.write('<p style="text-indent: 2em;">' + i + '</p>' + '\n')
    fh.close()

#标记文章里的图片，用于之后替换
def sub_img(js_content):
    atricle_num = 0
    for i in js_content.find_all('img'):
        atricle_num = atricle_num + 1
        # i.string = '\n' + 'cut_img' + str(atricle_num) +'\n'
        i.string ='cut_img' + str(atricle_num)

#遍历文章图片的url
def get_img_urls(js_content):
    img_urls = []
    for i in js_content.find_all('img'):
        img_urls.append(i['data-src'])
    return img_urls

#下载文章里的图片
def dowload_wechat_img(img_urls,file,session,cookies):
    isFile(file)
    img_path = file + "\\" + "img_name"
    img_num = 0 #计算工具
    p_wechat_img_type = re.compile('mmbiz_[a-zA-z]*') #正则取url中图片的后缀
    for img_url in img_urls:
        img_num = img_num + 1
        pre_type = p_wechat_img_type.findall(img_url)
        if pre_type:
            img_name = 'img' + str(img_num) + '.' + re.sub('mmbiz_', '', pre_type[0])
            print(img_name)
            time.sleep(random.randint(1, 10))
            r = session.get(url=img_url, cookies=cookies, verify=False)
            print(r.status_code)
            with open(img_path.replace('img_name', img_name), 'wb') as f:
                f.write(r.content)
            f.close()
        else:
            print('未知图片类型跳过')

#html转soup，主要用到BeautifulSoup的方法找到数据
def html_to_mySoup(html):
    print('进入get_content')
    soup = BeautifulSoup(html,'lxml')
    print('soup')
    js_content = soup.find(id="js_content")
    print('获取js_content')
    js_content.append(soup.new_tag('patch ', ''))
    print('打补丁')
    return js_content
