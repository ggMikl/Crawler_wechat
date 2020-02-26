import input.wechat as wechat
import output.loupanwang as lp
from entity.wechat_entity import wechat_entity
import tool.fileTool as file_Tool
import tool.webTool as web
from tool.Cut_img import cut_img
from tool.uploadImg import uploadImg

session = web.get_session(False,511)
upload_url = 'http://cs.loupan.com/new_upload/' + 'ueditor_upload'

wechat_name = ""#输入微信帐号
wechat_pw = ""#输入微信密码
#该微信记得注册一个公众号

lp_nname = ''
lp_pw = ''
#后排帐号密码

query = ''#公众号名
workPath = r''#工作路径



if __name__ == '__main__':
    #检查cookies是否过期
    # 微信登录
    wechat.login(wechat_name,wechat_pw)
    wechat_cookies = file_Tool.get_local_cookies('wechat_cookies.txt')
    # 后台登录
    lp.login(lp_nname,lp_pw)
    lp_cookies = file_Tool.get_local_cookies('loupanwang_cookies.txt')
    # 基础信息构建 爬取公众号 路径 标题
    wechat_base = wechat_entity(query , workPath)
    # 获取内容
    content = wechat.get_Content(query,wechat_cookies,session)
    # 下载图片
    wechat.dowload_img(content['content'],wechat_base.get_ImgPath(),session,wechat_cookies)
    # # 裁剪图片
    cut_img(wechat_base.get_ImgPath(),wechat_base.get_CutPath())
    # 上传图片 # 返回图片字典
    img_net = uploadImg(session,lp_cookies,wechat_base.get_CutPath(),upload_url)
    # 输出文件
    wechat.out_file(content,wechat_base.get_NewsPath(),img_net,query)



