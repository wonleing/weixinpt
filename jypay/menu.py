# -*- coding: utf-8 -*-
import urllib, urllib2, json
APPID = "wxd8f34b2d456cc10a"
APPSECRET = "145d67f81174bdac0ef90ef253e261a4"
cname = "yangniuquan"
access_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
menu_url = "https://api.weixin.qq.com/cgi-bin/menu/create?%s"
oauth_url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid="+APPID+"&response_type=code&scope=snsapi_base&redirect_uri=http://weixinpt.sinaapp.com/jypay/"

menus = {
     "button":[
      {
           "name":"买单吧",
           "sub_button":[
            {
               "type":"view",
               "name":"线上商城",
               "url":"http://mp.weixin.qq.com/bizmall/mallshelf?id=&t=mall/list&biz=MzA3NTczNDYwOQ==&shelf_id=2&showwxpaytitle=1#wechat_redirect"
            },
            {
               "type":"view",
               "name":"捷优支付",
               "url":"http://weixinpt.sinaapp.com/jypay/index/"+cname+"/"
            },
      ]},
      {
           "name":"商户功能",
           "sub_button":[
            {
               "type":"view",
               "name":"常见问题",
               "url":"http://www.jyousoft.com/"
            },
            {
               "type":"view",
               "name":"商家绑定",
               "url":oauth_url+"bind/"+cname+"/"
            },
            {
               "type":"view",
               "name":"渠道注册",
               "url":oauth_url+"register/"+cname+"/"
            },
            {
               "type":"view",
               "name":"商户中心",
               "url":oauth_url+"centerdetail/"+cname+"/"
            },
            {
               "type":"view",
               "name":"渠道页面",
               "url":oauth_url+"checkdetail/"+cname+"/"
            }
      ]},
      {
           "name":"我的",
           "sub_button":[
            {
               "type":"view",
               "name":"消费中心",
               "url":oauth_url+"userdetail/"+cname+"/"
            },
            {
                "type":"view",
                "name":"养牛圈",
                "url":"http://buluo.qq.com/mobile/barindex.html?_bid=128&_wv=1027&bid=91395"
            },
      ]}
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
