# -*- coding: utf-8 -*-
import urllib, urllib2, json
APPID = "wx68bd26065cdcb5a9"
APPSECRET = "78d0897a77488c49c0dfaa56c7927ee9"
access_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
menu_url = "https://api.weixin.qq.com/cgi-bin/menu/create?%s"
menus = {
     "button":[
      {
          "type":"click",
          "name":"所有频道",
          "key":"allchannel"
      },
      {
          "type":"click",
          "name":"我的订阅",
          "key":"mychannel"
      },
      {
           "name":"APP下载",
           "sub_button":[
            {
               "type":"view",
               "name":"安卓下载",
               "url":"http://fusion.qq.com/cgi-bin/qzapps/unified_jump?appid=10958760&isTimeline=false&actionFlag=0&params=pname%3Dcom.hiveview.phone%26versioncode%3D2%26actionflag%3D0%26channelid%3D&from=singlemessage&isappinstalled=0"
            },
            {
               "type":"view",
               "name":"IOS下载",
               "url":"https://appsto.re/cn/wdfc4.i"
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
