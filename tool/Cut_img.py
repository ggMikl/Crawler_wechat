import cv2
import os  # 导入模块
import numpy as np
import re
from tool.Crawler_tool import isFile
import shutil

p = re.compile("[^\.]\w*$")
radio = 121 / 75
length = 710

def img_read(img_path):
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    return img

def img_crop(img,radio):#先做自己要的
    img_length = img.shape[1]
    img_width = img.shape[0]
    if img_length > img_width:
        my_length = round(img_width * radio)
        my_width = img_width  # 因为是取最大
        x0 = round((img_length - my_length) / 2)
        if x0 < 0:
            x0 = 0
        x1 = my_length + x0
        if x1 > img_length:
            x1 = img_length
        y0 = 0
        y1 = my_width
        return img[y0:y1, x0:x1]
    else:
        print('宽（高）大于长的没写')
        my_length = round(img_length * radio)
        my_width = round(img_width * radio)
        x0 = 0
        x1 = my_length
        y0 = 0
        y1 = my_width
        return img[y0:y1, x0:x1]

def img_resize(img,length):#先做自己要的
    img_length = img.shape[1]
    img_width = img.shape[0]
    re_length = length
    re_width = round(re_length * img_width / img_length)
    return cv2.resize(img, (re_length, re_width), interpolation=cv2.INTER_CUBIC)

def cut_img(inpath,outpath):
    # path = r''  # 运行程序前，记得修改主文件夹路径！
    isFile(inpath)
    isFile(outpath)
    #检查路径
    img_names = os.listdir(inpath)
    for img_name in img_names:
        type = re.findall(p, img_name)[0]
        img_path = inpath + '\\' + img_name
        new_name = 'cut_' + img_name
        if type != 'txt':
            if type != 'gif':
                img = img_read(img_path)
                cropped = img_crop(img, radio)
                resized = img_resize(cropped, length)
                cv2.imencode('.' + type, resized)[1].tofile(outpath + '\\' + new_name)
            else:
                print('该图为gif,不做修改,复制到新文件夹')
                shutil.copy(os.path.join(inpath, img_name), os.path.join(outpath, new_name))
                # os.rename(os.path.join(inpath, img_name), os.path.join(outpath, new_name))
        else:
            print('这个是txt跳过')
