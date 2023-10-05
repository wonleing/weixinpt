# -*- coding: utf-8 -*-
import urllib, urllib2, json
APPID = "wx99dc9d6300c74126"
APPSECRET = "bf2613e13e8f4ead30f6e89248e3c769"
access_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
menu_url = "https://api.weixin.qq.com/cgi-bin/menu/create?%s"
menus = {
     "button":[
      {
          "type":"click",
          "name":"加盟商家",
          "key":"shoplist"
      },
      {
           "name":"商家功能",
           "sub_button":[
            {
               "type":"click",
               "name":"功能说明",
               "key":"readme"
            },
            {
               "type":"click",
               "name":"快速查账",
               "key":"qcheck"
            },
            {
               "type":"click",
               "name":"商户中心",
               "key": "scheck"
            }
      ]},
      {
               "type":"click",
               "name":"消费查询",
               "key":"ucheck"
      }
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
