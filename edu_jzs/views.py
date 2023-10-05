# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
import xml.etree.ElementTree as ET
from edu_jzs.models import *
import share, hashlib, time, datetime, random
TOKEN = "weixinpt"
menu = u'''发送“姓名，手机号”成为实名绑定会员并显示自己的积分
点击下方 + 号发送图片即可上传到照片墙
发送位置则可获取从当前位置到我们学校的地图导航
每天参加刮刮卡，签到赚积分，赢VIP资格'''

@csrf_exempt
def handleRequest(request):
    if request.method == 'GET':
        return HttpResponse(checkSignature(request),content_type="text/plain")
    elif request.method == 'POST':
        return HttpResponse(responseMsg(request),content_type="application/xml")
    else:
        return None

def checkSignature(request):
    signature = request.GET.get("signature", None)
    timestamp = request.GET.get("timestamp", None)
    nonce = request.GET.get("nonce", None)
    echoStr = request.GET.get("echostr",None)
    tmpList = [TOKEN,timestamp,nonce]
    tmpList.sort()
    tmpstr = "%s%s%s" % tuple(tmpList)
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return echoStr
    else:
        msg={'FromUserName':'123','ToUserName':'445', 'CreateTime':'99999999999999'}
        return None

def responseMsg(request):
    rawStr = smart_str(request.raw_post_data)
    msg = share.paraseMsgXml(ET.fromstring(rawStr))
    if msg['MsgType'] == 'event':
        if msg['Event'] == 'subscribe':
            return share.getMultiXml(msg, '', EduJzsMain.objects.all().order_by('id'))
        elif msg['Event'] == 'CLICK':
            if msg['EventKey'] == 'menu':
                return share.getMultiXml(msg, '', EduJzsMain.objects.all().order_by('id'))
            elif msg['EventKey'] == 'help':
                return share.getTextXml(msg, share.randomreply(EduJzsMain)+menu)
            elif msg['EventKey'] == 'register':
                return share.getTextXml(msg, u'发送“姓名，手机号”即可成为实名注册会员，并显示自己的积分，您也可以再次发送来修改自己的注册姓名和电话。只有注册的会员才能使用互动活动中赢得的积分哦！')
            elif msg['EventKey'] == 'navigation':
                return share.getTextXml(msg, u'不知道我们在哪？点击下方＋号发送位置，即可弹出您当前位置到我们学校的地图导航哦，方便快捷，快来试试吧！')
            elif msg['EventKey'] == 'ggk':
                return lucky(msg, 'ggk')
            elif msg['EventKey'] == 'dzp':
                return lucky(msg, 'dzp')
            elif msg['EventKey'] == 'upload':
                return share.getTextXml(msg, u'点击下方＋号发送图片即可上传到我们的照片墙，和大家一起分享您的喜悦，更有可能获得积分哦！')
            elif msg['EventKey'] == 'vip':
                ret = EduJzsMember.objects.get(wxid=msg['FromUserName'])
                if ret.point < 500:
                    return share.getTextXml(msg, u'VIP资源区访问需要500积分以上，请联系客服充值或坚持每日抽奖增加您的积分')
                else:
                    return pop(msg, 11)
            else:
                return share.getTextXml(msg, u'该功能尚未设定')
    elif msg['MsgType'] == 'text':
        if msg['Content'] == '刮刮卡':
            return lucky(msg, 'ggk')
        elif msg['Content'] == '大转盘':
            return lucky(msg, 'dzp')
        elif msg['Content'].isdigit():
            try:
                ret = EduJzsMain.objects.get(id=int(msg['Content']))
            except:
                return share.getMultiXml(msg, '', EduJzsMain.objects.all().order_by('id'))
            if ret.type == 0:
                return share.getTextXml(msg, u"请点击下方菜单访问该区资源")
            elif ret.type == 1:
                return share.getSingleXml(msg, ret.title, "\x0a".join(ret.description.split("^")), ret.pic, ret.link)
            elif ret.type == 2:
                title = (ret.title, ret.description, ret.pic, ret.link)
                list = eval("EduJzs%s" %ret.id).objects.all().order_by('id')[:9]
                return share.getMultiXml(msg, title, list)
        else:
            info = msg['Content'].replace(",","，").replace(":", "：").split("，")
            if len(info) == 2 and len(info[1]) == 11:
                ret = award(msg['FromUserName'], 0)
                ret.name = info[0]
                ret.phone = info[1]
                ret.save()
                return share.getTextXml(msg, u'会员信息更新成功，目前积分：%s' %ret.point)
            return share.getTextXml(msg, share.randomreply(EduJzsMain)+menu)
    elif msg['MsgType'] == 'image':
        if EduJzsPhoto.objects.filter(wxid=msg['FromUserName']):
            return share.getTextXml(msg, u'你已经上传过照片了，给别人留点机会吧^_^')
        else:
            EduJzsPhoto(wxid=msg['FromUserName'], piclink=msg['PicUrl']).save()
            award(msg['FromUserName'], 0)
            return share.getTextXml(msg, u'您的图片已经上传成功!\x0a<a href="http://weixinpt.sinaapp.com/edu_jzs/photo_1">点击进入照片墙</a>')
    elif msg['MsgType'] == 'location':
        url = u"http://api.map.baidu.com/direction?origin=latlng:%s,%s|name:我的位置&destination=银谷大厦&mode=driving&region=北京&output=html"        %(msg['Location_X'], msg['Location_Y'])
        return share.getTextXml(msg, u'<a href="%s">路线导航</a>' %url)
    else:
        return share.getTextXml(msg, share.randomreply(EduJzsMain)+menu)

def subpage(request, pageid):
    ret = share.header("../../static/css/subpage.css")
    root = EduJzsMain.objects.get(id=pageid)
    ret += '    <title>%s</title>\n    <body>\n' % root.title
    ret += share.submenu(EduJzsMain)
    ret += '''        <div class="listData" id="wrapper"><div id="scroller"><ul>\n'''
    if root.type == 0:
        return HttpResponse(u'此页面须从微信菜单中点击访问')
    elif root.type == 1:
        root.title = ""
        ret += share.sublayout(root)
    else:
        try:
            list = eval("EduJzs%s" %pageid).objects.all()
        except:
            return HttpResponse(u'亲，此页不存在哦')
        for item in list:
            ret += share.sublayout(item)
    ret += '                </ul></div></div>' + share.footer
    return HttpResponse(ret)

def photo(request, pageid):
    pid = int(pageid)
    pages = EduJzsPhoto.objects.count()/20+1
    ret = share.header("../../static/css/subpage.css")
    ret += u'    <title>照片上传展示</title>\n    <body>\n'
    ret += '        <div class="category" id="category"><div id="scroller"><ul>\n'
    for s in range(pages):
        ret += u'            <li><a href="../photo_%d">第%d页</a></li>\n' %(s+1, s+1)
    ret += '        </ul></div></div>\n'
    ret += '        <div class="listData" id="wrapper"><div id="scroller"><ul>\n'
    ret += '        <div class="news">\n'
    for item in EduJzsPhoto.objects.all().order_by('-date')[pid*20-20:pid*20]:
        if item.piclink:
            ret += '        <li><a href="%s"><img src="%s" /></a><br/>\n' %(item.piclink,item.piclink)
            uploader = EduJzsMember.objects.get(wxid=item.wxid).name
            if not uploader:
                uploader = u'匿名'
            ret += u'        <article>上传人：%s，上传时间：%.*s</article></li>\n' %(uploader, 10, item.date)
    ret += '</div>' + share.footer
    return HttpResponse(ret)

def award(wxid, point):
    try:
        ret = EduJzsMember.objects.get(wxid=wxid)
    except:
        EduJzsMember(wxid=wxid).save()
        ret = EduJzsMember.objects.get(wxid=wxid)
    ret.point += point
    ret.save()
    return ret

def lucky(msg, type):
    today = datetime.date.today().isoformat()
    try:
        EduJzsRecord.objects.get(wxid=msg['FromUserName'],type=type,date=today)
        return share.getTextXml(msg, u'您今天已经参加过抽奖，请明天再试')
    except:
        EduJzsRecord(wxid=msg['FromUserName'],type=type,date=today).save()
        for aw in EduJzsAward.objects.filter(type=type):
            if aw.rate != 0 and aw.amount > 0 and random.random()*aw.rate < 1:
                award(msg['FromUserName'], aw.point)
                aw.amount -= 1
                aw.save()
                return share.getSingleXml(msg, aw.title, aw.description, aw.pic, aw.link)

def pop(msg, number):
    try:
        ret = EduJzsMain.objects.get(id=number)
    except:
        return share.getMultiXml(msg, '', EduJzsMain.objects.all().order_by('id'))
    if ret.type == 2:
        title = (ret.title, ret.description, ret.pic, ret.link)
        list = eval("EduJzs%s" %ret.id).objects.all().order_by('id')[:9]
        return share.getMultiXml(msg, title, list)
    else:
        return share.getSingleXml(msg, ret.title, "\x0a".join(ret.description.split(" ")), ret.pic, ret.link)
