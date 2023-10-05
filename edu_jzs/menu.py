# -*- coding: utf-8 -*-
import urllib, urllib2, json
APPID = "wx95d1772f11551586"
APPSECRET = "fb8a3a84cd6fe7a742433ecef2389381"
access_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
menu_url = "https://api.weixin.qq.com/cgi-bin/menu/create?%s"
menus = {
     "button":[
      {
           "name":"开始",
           "sub_button":[
            {
               "type":"click",
               "name":"主菜单",
               "key":"menu"
            },
            {
               "type":"click",
               "name":"使用帮助",
               "key":"help"
            },
            {
               "type":"click",
               "name":"用户注册",
               "key":"register"
            },
            {
               "type":"click",
               "name":"路线导航",
               "key":"navigation"
            },
      ]},
      {
           "name":"互动活动",
           "sub_button":[
            {
               "type":"click",
               "name":"刮刮卡",
               "key":"ggk"
            },
            {
               "type":"click",
               "name":"大转盘",
               "key":"dzp"
            },
            {
               "type":"view",
               "name":"微社区",
               "url":"http://wx.wsq.qq.com/217520131"
            },
            {
               "type":"click",
               "name":"照片上传",
               "key":"upload"
            }
      ]},
      {
           "name":"资源特区",
           "sub_button":[
            {
               "type":"click",
               "name":"VIP资源",
               "key":"vip"
            },
            {
               "type":"view",
               "name":"照片墙",
               "url":"http://weixinpt.sinaapp.com/edu_jzs/photo_1"
            }
      ]},
]}

def get_access_token():
    f = urllib.urlopen(access_url % (APPID, APPSECRET))
    resp = json.loads(f.read())
    return resp['access_token']
 
def generate_menu(token):
    params = {'access_token': urllib.quote(token)}
    url = menu_url % urllib.urlencode(params)
    request = urllib2.Request(url, json.dumps(menus, ensure_ascii=False))
    response = urllib2.urlopen(request)
    print response.read()
 
token = get_access_token()
generate_menu(token)
