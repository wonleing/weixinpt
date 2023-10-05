# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.utils.encoding import smart_str
from django.contrib import auth
import xml.etree.ElementTree as ET
from mygym.models import *
import share, hashlib, random, time
TOKEN = "weixinpt"

@csrf_exempt
def handleRequest(request):
    if request.method == 'GET':
        return HttpResponse('')
        #return HttpResponse(checkSignature(request),content_type="text/plain")
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
        return None

def responseMsg(request):
    rawStr = smart_str(request.raw_post_data)
    msg = share.paraseMsgXml(ET.fromstring(rawStr))
    if msg['MsgType'] == 'event':
        if msg['Event'] == 'subscribe':
            return share.getTextXml(msg, u'欢迎您访问美吉姆中国微信公众号。详细功能请参见菜单')
        elif msg['Event'] == 'CLICK':
            if msg['EventKey'] == 'menu':
                return share.getMultiXml(msg, '', MygymMain.objects.all().order_by('id'))
            elif msg['EventKey'] == 'show':
                return show(msg)
            elif msg['EventKey'] == 'mine':
                return mine(msg)
            elif msg['EventKey'] == 'pop1':
                return pop(msg, 1)
            elif msg['EventKey'] == 'pop2':
                return pop(msg, 2)
            elif msg['EventKey'] == 'pop3':
                return pop(msg, 3)
            return share.getTextXml(msg, u'该功能尚未设定')
    elif msg['MsgType'] == 'text':
        info = msg['Content'].replace(",","，").split("，")
        if len(info) == 2 and len(info[1]) == 11:
            try:
                old = MygymCustomer.objects.get(wxid=msg['FromUserName'])
                old.wxid = ""
                old.save()
            except:
                pass
            try:
                ret = MygymCustomer.objects.get(name=info[0], phone=info[1])
                ret.wxid = msg['FromUserName']
                ret.save()
                return share.getTextXml(msg, u"家长信息绑定成功，请点击菜单栏中的小小画展查看照片")
            except:
                return share.getTextXml(msg, u"家长信息未找到，请联系中心确认您的信息已正确录入")
        elif msg['Content'].isdigit():
            return pop(msg, int(msg['Content']))
        elif '画' in msg['Content']:
            return show(msg)
        elif '我' in msg['Content']:
            return mine(msg)
    return share.getTextXml(msg, u'详细功能请参见下方自定义菜单')

def pop(msg, number):
    try:
        ret = MygymMain.objects.get(id=number)
    except:
        return share.getMultiXml(msg, '', MygymMain.objects.all().order_by('id'))
    if ret.type == 0:
        return share.getTextXml(msg, ret.title+"\x0a"+"\x0a".join(ret.description.split("^")))
    elif ret.type == 1:
        return share.getSingleXml(msg, ret.title, "\x0a".join(ret.description.split("^")), ret.pic, ret.link)
    elif ret.type == 2:
        title = (ret.title, ret.description, ret.pic, ret.link)
        list = eval("Mygym%s" %ret.id).objects.all().order_by('id')[:9]
        return share.getMultiXml(msg, title, list)

def show(msg):
    try:
        r1 = MygymCustomer.objects.get(wxid=msg['FromUserName'])
        r2 = MygymSite.objects.get(sid=r1.sid)
        return share.getTextXml(msg, u'<a href="%s">小小画展</a>\x0a密码：%s' %(r2.link, r2.password))
    except:
        return share.getTextXml(msg, u'需要先验证家长信息，请按格式输入“姓名，手机号”进行验证，注意中间用逗号隔开')

def mine(msg):
    try:
        r1 = MygymCustomer.objects.get(wxid=msg['FromUserName'])
        r2 = MygymSite.objects.get(sid=r1.sid)
        return share.getTextXml(msg, u'姓名：%s\x0a手机号：%s\x0a中心编号：%s\x0a中心名称：%s\x0a中心地址：%s\x0a电话：%s' \
        %(r1.name, r1.phone, r1.sid, r2.name, r2.location, r2.phone))
    except:
        return share.getTextXml(msg, u'需要先验证家长信息，请按格式输入“姓名，手机号”进行验证，注意中间用逗号隔开')

def subpage(request, pageid):
    ret = share.header("../../static/css/subpage.css")
    root = MygymMain.objects.get(id=pageid)
    ret += '    <title>%s</title>\n    <body>\n' % root.title
    ret += share.submenu(MygymMain)
    ret += '''        <div class="listData" id="wrapper"><div id="scroller"><ul>\n'''
    if root.type != 2:
        root.title = ""
        ret += share.sublayout(root)
    else:
        try:
            list = eval("Mygym%s" %pageid).objects.all()
        except:
            return HttpResponse(u'亲，此页不存在哦')
        for item in list:
            ret += share.sublayout(item)
    ret += '                </ul></div></div>' + share.footer
    return HttpResponse(ret)

def memberinput(request):
    if 'login_user' not in request.session:
        request.session['login_user'] = ""
    context = { 'title': '美吉姆会员录入系统',
                'login_user': request.session['login_user'] }
    return render(request, 'memberinput.html', context)

def dologin(request):
    ac = request.POST.get('account')
    pw = request.POST.get('password')
    user = auth.authenticate(username=ac, password=pw)
    if user:
        request.session['login_user'] = user.get_username()
        return HttpResponse('''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../memberinput/"></head>登录成功</html>''')
    else:
        return HttpResponse('''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../memberinput/"></head>用户名密码错误</html>''')

def doinput(request):
    cid = request.POST.get('cid').replace(" ", "")
    name = request.POST.get('name').replace(" ", "")
    phone = request.POST.get('phone').replace(" ", "").replace(".", "")
    sid = request.POST.get('sid').replace(" ", "")
    if cid == "":
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../memberinput"></head>学号不能为空</html>')
    elif "(" in name or u"（" in name or "/" in name or u"／" in name:
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../memberinput"></head>姓名格式有误，请去掉姓名中括号里或/后的昵称</html>')
    elif "/" in phone or u"／" in phone:
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../memberinput"></head>电话格式有误，请只保留一个电话，去掉/后的电话号码</html>')
    try:
        ret = MygymCustomer.objects.get(phone=phone,name=name)
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../memberinput"></head>该会员信息已经存在</html>')
    except:
        pass
    try:
        ret = MygymCustomer.objects.get(cid=cid,name=name)
        ret.phone = phone
        ret.sid = sid
        ret.save()
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="1;URL=../memberinput"></head>会员信息更新成功</html>')
    except:
        MygymCustomer(cid=cid, name=name, phone=phone, sid=sid).save()
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="1;URL=../memberinput"></head>会员信息添加成功</html>')

def logout(request):
    request.session['login_user'] = ""
    return HttpResponse('''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../memberinput/"></head>登出成功!</html>''')
