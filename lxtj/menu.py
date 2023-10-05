# -*- coding: utf-8 -*-
import urllib, urllib2, json
APPID = "wx5527ac2672f6de0f"
APPSECRET = "843509cf762f7b65f7bb9dec2e720913"
access_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
menu_url = "https://api.weixin.qq.com/cgi-bin/menu/create?%s"
menus = {
     "button":[
      {
           "name":"精彩视频",
           "sub_button":[
            {
               "type":"click",
               "name":"免费专区",
               "key":"free"
            },
            {
               "type":"click",
               "name":"付费专区",
               "key":"charge"
            }
      ]},
      {
          "type":"click",
          "name":"设备绑定",
          "key":"bind"
      },
      {
           "name":"用户中心",
           "sub_button":[
            {
               "type":"click",
               "name":"搜索",
               "key":"search"
            },
            {
               "type":"click",
               "name":"帮助反馈",
               "key":"help"
            },
            {
               "type":"click",
               "name":"摇控器",
               "key":"control"
            }
      ]},
      ]
}
 
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
