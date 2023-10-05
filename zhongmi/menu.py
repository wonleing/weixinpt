# -*- coding: utf-8 -*-
import urllib, urllib2, json
APPID = "wxd9e0476a27dd1282"
APPSECRET = "6cc72520a1710b70544b29c8489be237"
cname = "zhongmi"
access_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
menu_url = "https://api.weixin.qq.com/cgi-bin/menu/create?%s"
oauth_url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid="+APPID+"&response_type=code&scope=snsapi_base&redirect_uri=http://weixinpt.sinaapp.com/jypay/"
menus = {
     "button":[
      {
           "type":"view",
           "name":"微网站",
           "url":"http://weixinpt.sinaapp.com/taobao_hxf/subpage/1/"
      },
      {
           "name":"线下支付",
           "sub_button":[
            {
               "type":"view",
               "name":"商户绑定",
               "url":oauth_url+"bind/"+cname+"/"
            },
            {
               "type":"view",
               "name":"渠道注册",
               "url":oauth_url+"register/"+cname+"/"
            },
            {  
               "type":"view",
               "name":"中心页面",
               "url":oauth_url+"centerdetail/"+cname+"/"
            }, 
            {
               "type":"view",
               "name":"渠道页面",
               "url":oauth_url+"checkdetail/"+cname+"/"
            },
            {  
               "type":"view",
               "name":"我的消费",
               "url":oauth_url+"userdetail/"+cname+"/"
            }, 
      ]},
      {
           "name":"在线商城",
           "sub_button":[
            {
               "type":"view",
               "name":"在线商城",
               "url":"https://huaxingbjp.m.tmall"
            },
            {
               "type":"click",
               "name":"使用帮助",
               "key":"howtobind"
            },
            {
               "type":"click",
               "name":"用户信息",
               "key":"userinfo"
            },
            {
               "type":"click",
               "name":"所属门店",
               "key":"userchannel"
            },
            {
               "type":"click",
               "name":"消费记录",
               "key":"salerecord"
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
