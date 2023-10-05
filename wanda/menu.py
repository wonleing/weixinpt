# -*- coding: utf-8 -*-
import urllib, urllib2, json
#APPID = "wx38333c7676707a92"
#APPSECRET = "7bced59c7434eaaa3812e8f1aec60c9b"
APPID = "wxde101a87cf4530ba"
APPSECRET = "da9ecb9486ae67195dd6386a4defd9df"
access_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
menu_url = "https://api.weixin.qq.com/cgi-bin/menu/create?%s"
menus = {
     "button":[
      {
          "type":"view",
          "name":"选座买票",
          "url":"http://wx.wepiao.com/index.html?channel=mpmovie"
      },
      {
          "type":"view",
          "name":"本周优惠",
          "url":"http://eqxiu.com/s/UJ4PZR"
      },
      {
           "name":"我的票友",
           "sub_button":[
            {
               "type":"view",
               "name":"试试手气",
               "url":"http://b.wepiao.com/hongbao/index.html?pid=%17%0C%B6F7%FF%DE%0E&channelid=3&chid=100"
            },
            {
               "type":"view",
               "name":"票友圈",
               "url":"http://m.wsq.qq.com/263842096"
            }]
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
