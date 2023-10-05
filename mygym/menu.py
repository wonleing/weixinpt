# -*- coding: utf-8 -*-
import urllib, urllib2, json
APPID = "wx2f643c2234a1e28d"
APPSECRET = "e8f8b24c4eeaa62fd026d12770e3192f"
access_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
menu_url = "https://api.weixin.qq.com/cgi-bin/menu/create?%s"
menus = {
     "button":[
      {
           "name":"美吉姆",
           "sub_button":[
            {
               "type":"view",
               "name":"美吉姆全球",
               "url":"http://mp.weixin.qq.com/s?__biz=MjM5MDIwNjYyMQ==&mid=200054345&idx=1&sn=64cccf137ecb09eda414e37eea26be79#rd"
            },
            {
               "type":"view",
               "name":"美吉姆中国",
               "url":"http://mp.weixin.qq.com/s?__biz=MjM5MDIwNjYyMQ==&mid=200054351&idx=1&sn=e45f84de283389f6751be94bd67ca824#rd"
            },
            {
               "type":"view",
               "name":"美吉姆哲学",
               "url":"http://mp.weixin.qq.com/s?__biz=MjM5MDIwNjYyMQ==&mid=200054358&idx=1&sn=01e053db1c15e93d3ccdf2a1d88a108d#rd"
            },
            {
               "type":"view",
               "name":"国际专家团队",
               "url":"http://mp.weixin.qq.com/s?__biz=MjM5MDIwNjYyMQ==&mid=200054457&idx=1&sn=bd98d0cbacbcef576617c5587d456009#rd"
            },
            {
               "type":"view",
               "name":"国内专家团队",
               "url":"http://mp.weixin.qq.com/s?__biz=MjM5MDIwNjYyMQ==&mid=200054491&idx=1&sn=53731052310a046643d12e4e5fdbdaac#rd"
            }
      ]},
      {
           "name":"三大课程",
           "sub_button":[
            {
               "type":"view",
               "name":"欢动课 My Gym",
               "url":"http://mp.weixin.qq.com/s?__biz=MjM5MDIwNjYyMQ==&mid=200054372&idx=2&sn=81587e85f772d333688fd7b92b4406f3#rd"
            },
            {
               "type":"view",
               "name":"艺术课 My Art",
               "url":"http://mp.weixin.qq.com/s?__biz=MjM5MDIwNjYyMQ==&mid=200054401&idx=2&sn=d4272c413255cf1db44234b270508cdb#rd"
            },
            {
               "type":"view",
               "name":"音乐课 My Music",
               "url":"http://mp.weixin.qq.com/s?__biz=MjM5MDIwNjYyMQ==&mid=200054445&idx=2&sn=09a29348507d689077318144aa160d5b#rd"
            }
      ]},
      {
           "name":"服务中心",
           "sub_button":[
            {
               "type":"view",
               "name":"预约免费试听课",
               "url":"http://m.mygymchina.com.cn/index.php?c=article&a=type&tid=11"
            },
            {
               "type":"view",
               "name":"身边的美吉姆",
               "url":"http://m.mygymchina.com.cn/index.php?c=product&a=type&tid=2"
            },
            {
               "type":"click",
               "name":"我的中心信息",
               "key":"mine"
            },
            {
               "type":"click",
               "name":"小小画展",
               "key":"show"
            }
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
