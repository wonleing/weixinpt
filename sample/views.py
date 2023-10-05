# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
import xml.etree.ElementTree as ET
from __pname__.models import *
import share, hashlib
TOKEN = "weixinpt"
utitle = {}

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
        return None

def responseMsg(request):
    rawStr = smart_str(request.raw_post_data)
    msg = share.paraseMsgXml(ET.fromstring(rawStr))
    if msg['MsgType'] == 'event':
        if msg['Event'] == 'subscribe':
            return share.getMultiXml(msg, '', __Pname__Main.objects.all().order_by('id'))
        elif msg['Event'] == 'CLICK':
            if msg['EventKey'] == 'menu':
                return share.getMultiXml(msg, '', __Pname__Main.objects.all().order_by('id'))
            if msg['EventKey'] == 'upload':
                return share.getTextXml(msg, u'请在微信中发送"上传：图片标题"，注意冒号为中文全角')
    if msg['MsgType'] == 'text':
        if msg['Content'].isdigit():
            try:
                ret = __Pname__Main.objects.get(id=int(msg['Content']))
            except:
                return share.getMultiXml(msg, '', __Pname__Main.objects.all().order_by('id'))
            if ret.type == 0:
                return share.getTextXml(msg, ret.title+"\n"+ret.description)
            elif ret.type == 1:
                return share.getSingleXml(msg, ret.title, "\x0a".join(ret.description.split(" ")), ret.pic, ret.link)
            elif ret.type == 2:
                title = (ret.title, ret.description, ret.pic, ret.link)
                list = eval("__Pname__%s" %ret.id).objects.all().order_by('id')[:9]
                return share.getMultiXml(msg, title, list)
        elif len(msg['Content'].split("：")) == 2:
            if msg['Content'].split("：")[0] == '上传':
                global utitle
                utitle[msg['FromUserName']] = msg['Content'].split("：")[1]
                return share.getTextXml(msg, u'按输入菜单中的+号，拍照或选中您要上传的照片')
            elif msg['Content'].split("：")[0] == '留言':
                __Pname__Msg(contact=msg['FromUserName'], content=msg['Content'].split("：")[1]).save()
                return share.getTextXml(msg, u"您的留言已经被接受")
            else:
                return share.getTextXml(msg, u'关键词输入错误')
        else:
            return share.getTextXml(msg, share.randomreply(__Pname__Main))
    elif msg['MsgType'] == 'image':
        newid = __Pname__7.objects.count()+1
        global utitle
        if msg['FromUserName'] in utitle.keys():
            newtitle = utitle[msg['FromUserName']]
        else:
            newtitle = "No Title"
        if msg['FromUserName'] == "oKfS1jg6BMWgdJSxEXJVHq4yNqRA":
            uploader = 'Leon'
        else:
            uploader = msg['FromUserName']
        __Pname__7(id=newid,title=newtitle,description=u'上传人：%s\x0a上传时间：%s' %(uploader, msg['CreateTime']), \
        price='',pic=msg['PicUrl'],link=msg['PicUrl']).save()
        return share.getTextXml(msg, u"您上传的图片已经上传成功，发送7可看到您的新图效果")
    else:
        return share.getTextXml(msg, share.randomreply(__Pname__Main))

def subpage(request, pageid):
    ret = share.header("../../static/css/subpage.css")
    root = __Pname__Main.objects.get(id=pageid)
    ret += '    <title>%s</title>\n    <body>\n' % root.title
    ret += share.submenu(__Pname__Main)
    ret += '''        <div class="listData" id="wrapper"><div id="scroller"><ul>\n'''
    if root.type != 2:
        root.title = ""
        ret += share.sublayout(root)
    else:
        list = eval("__Pname__%s" %pageid).objects.all()
        for item in list:
            ret += share.sublayout(item)
    ret += '                </ul></div></div>' + share.footer
    return HttpResponse(ret)
