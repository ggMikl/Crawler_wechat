import time

class wechat_entity():
    query = '' #查询公众号
    workPath = '' #爬虫本地文档根目录
    subscriptionPath = '' #新建爬取公众号本地目录
    newsPath = ''  #文章本地路径
    imgPath = '' #图片本地路径
    cutPath = '' #裁剪后图片本地路径

    def __init__(self, query , workPath):
        self.query = query
        self.workPath = workPath
        self.subscriptionPath = self.workPath + '\\' + query
        self.newsPath = self.subscriptionPath + '\\' + query + '_' + str(int(time.time()))
        self.imgPath = self.newsPath + '\\' + 'img'
        self.cutPath = self.newsPath+ '\\' + 'cut_img'

    def get_Query(self):
        return self.query
    def set_Query(self,value):
        self.query = value

    def get_WorkPath(self):
        return self.workPath
    def set_WorkPath(self, value):
        self.workPath = value

    def get_SubscriptionPath(self):
        return self.subscriptionPath
    def set_SubscriptionPath(self, value):
        self.subscriptionPath = value

    def get_NewsPath(self):
        return self.newsPath
    def set_NewsPath(self, value):
        self.newsPath = value

    def get_ImgPath(self):
        return self.imgPath
    def set_ImgPath(self, value):
        self.imgPath = value

    def get_CutPath(self):
        return self.cutPath
    def set_CutPath(self, value):
        self.cutPath = value

    def __str__(self) -> str:
        return 'This Object is some baseInfo when you use the crawler '+ '\n' + \
               'For example,the subscription(wechat)\'s name :' + self.query + '\n' + \
               'It\'s local work path is : ' + self.workPath




