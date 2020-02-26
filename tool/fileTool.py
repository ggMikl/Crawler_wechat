import os
import sys
import json

def isFile(fileName):
    if os.path.exists(fileName):
        print('该文件夹存在,直接返回文件夹路径' + fileName)
        # 该路径存在返回这个路径
        return fileName
    else:
        print('该文件夹不存在,创建')
        os.makedirs(fileName)
        # 返回这个路径
        print('返回这个路径文件夹路径' + fileName)
        return fileName

def add_prefix_subfolders(path,type):        #定义函数名称
    old_names = os.listdir( path )  #取路径下的文件名，生成列表
    for old_name in old_names:      #遍历列表下的文件名
        if old_name!= sys.argv[0]:     #代码本身文件路径，防止脚本文件放在path路径下时，被一起重命名
            new_name = old_name.split('.') [0] + '.' + type
            if old_name!= new_name:
                os.rename(os.path.join(path,old_name),os.path.join(path,new_name))  #子文件夹重命名
            else:
                print('这个重名的文件是:'+new_name)

def get_local_cookies(path):
    print("读取cookies")
    with open(path, 'r', encoding='utf-8') as f:
        cookie = f.read()
    print("读取cookies成功")
    return json.loads(cookie)
