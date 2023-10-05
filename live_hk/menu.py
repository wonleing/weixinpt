# -*- coding: utf-8 -*-
import urllib, urllib2, json
APPID = "wxd8f34b2d456cc10a"
APPSECRET = "145d67f81174bdac0ef90ef253e261a4"
#APPID = "wxde101a87cf4530ba"
#APPSECRET = "da9ecb9486ae67195dd6386a4defd9df"
access_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
menu_url = "https://api.weixin.qq.com/cgi-bin/menu/create?%s"
menus = {
     "button":[
      {
          "type":"view",
          "name":"养牛圈",
          "url":"http://m.wsq.qq.com/262932933"
      },
      {
          "type":"click",
          "name":"新年求签",
          "key":"newyear"
      },
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
