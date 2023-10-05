# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
import xml.etree.ElementTree as ET
from wanda.models import *
import share, hashlib, time, datetime, random, json, urllib, urllib2
TOKEN = "weixinpt"
appid="wxde101a87cf4530ba"
secret="da9ecb9486ae67195dd6386a4defd9df"
baseurl = "http://weixinpt.sinaapp.com/wanda/"
header = '''<head><meta name="viewport" content="width=device-width, minimum-scale=1.0,maximum-scale=1.0,user-scalable=no"></head>'''
menu = u'''答案猜的好像不对哦，试试其它的答案吧！'''

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
            if not WandaMember.objects.filter(wxid=msg['FromUserName']):
                award(msg['FromUserName'], 10)
            return share.getMultiXml(msg, '', WandaMain.objects.filter(id__lt=10).order_by('id'))
        elif msg['Event'] == 'CLICK':
            if msg['EventKey'] == 'menu':
                return share.getMultiXml(msg, '', WandaMain.objects.filter(id__lt=10).order_by('id'))
            elif msg['EventKey'] == 'photo':
                return share.getSingleXml(msg, u"我要投票", u"每人限投一票，请珍惜自己的机会\x0a点击查看全文进行浏览和投票", \
                "http://cqrbepaper.cqnews.net/cqrb/res/1/20100829/71661283024837968.jpg", baseurl+msg['FromUserName']+"/1")
            elif msg['EventKey'] == 'mine':
                ret = WandaMember.objects.get(wxid=msg['FromUserName'])
                return share.getTextXml(msg, u'您当前的积分是：%d' %ret.point)
            elif msg['EventKey'] == 'lucky':
                return share.getTextXml(msg, u'<a href="http://web.jyousoft.com/web/hongbao/piaoyou_share.php">分享得红包，一天一次！</a>')
            else:
                return share.getTextXml(msg, u'该功能尚未设定')
    elif msg['MsgType'] == 'text':
        try:
            match = WandaMain.objects.get(title=msg['Content'])
            if match.type == 3:
                return share.getSingleXml(msg, u'你真是骨灰级影迷，猜中了所有电影', "\x0a".join(match.description.split("^")), match.pic, match.link+msg['FromUserName'])
            else:
                return share.getSingleXml(msg, match.title, "\x0a".join(match.description.split("^")), match.pic, match.link)
        except:
            pass
        if msg['Content'].isdigit():
            try:
                ret = WandaMain.objects.get(id=int(msg['Content']))
            except:
                return share.getMultiXml(msg, '', WandaMain.objects.filter(id__lt=20).order_by('id'))
            if ret.type == 0:
                return share.getTextXml(msg, ret.title+"\n"+ret.description)
            elif ret.type == 1:
                return share.getSingleXml(msg, ret.title, "\x0a".join(ret.description.split("^")), ret.pic, ret.link)
            elif ret.type == 2:
                title = (ret.title, ret.description, ret.pic, ret.link)
                list = eval("Wanda%s" %ret.id).objects.all().order_by('id')[:9]
                return share.getMultiXml(msg, title, list)
        return share.getTextXml(msg, menu)
        #return share.getTextXml(msg, share.randomreply(WandaMain)+menu)

@csrf_exempt
def notify(request):
    #today = datetime.date.today().isoformat()
    if request.method == 'POST':
        wxid = request.POST.get("wxid") or "none"
        shareid = request.POST.get("shareid") or "none"
        detail = request.POST.get("order")
        order = json.loads(detail.replace('\n', ''))
        WandaRecord(wxid=wxid, shareid=shareid, orderid=order['orderId'], type='komovie_buy', date=order['orderTime']).save()
        return HttpResponse('callback sucess')

def subpage(request, pageid):
    try:
        items = eval("Wanda%s" %pageid).objects.all().order_by('id')[:20]
    except:
        return HttpResponse(u'亲，此页不存在哦')
    return HttpResponse(serializers.serialize("json", items))
    #context = {
    #    'items': items,
    #    'pageid': pageid,
    #}
    #return render(request, 'wap/ilovemilk.html', context)

def picturevote(request, userid, pageid):
    pid = int(pageid)
    pages = WandaPhoto.objects.count()/20+1
    ret = share.header("../../../static/css/subpage.css")
    ret += u'    <title>照片上传展示</title>\n    <body>\n'
    ret += '        <div class="category" id="category"><div id="scroller"><ul>\n'
    for s in range(pages):
        ret += u'            <li><a href="../%d">第%d页</a></li>\n' %(s+1, s+1)
    ret += '        </ul></div></div>\n'
    ret += '        <div class="listData" id="wrapper"><div id="scroller"><ul>\n'
    ret += '        <div class="news">\n'
    for item in WandaPhoto.objects.all().order_by('-date')[pid*20-20:pid*20]:
        if item.piclink:
            ret += '        <li><a href="%s"><img src="%s" /></a><br/>\n' %(item.piclink,item.piclink)
            uploader = WandaMember.objects.get(wxid=item.wxid)
            vote = u'''<form action="../../dovote/" method="post"><input type="hidden" name="pid" value="%s" /><input type="hidden" name="uid" 
                   value="%s" /><input type="submit" value="投票" /></form>''' %(item.wxid, userid)
            if not uploader.name:
                uploader.name = u'匿名'
            ret += u'<article><table><tr><td width="120"><b>得票数：<font color="red">%s</font></b></td><td>%s</td></tr></table>上传人：%s，\
            上传时间：%.*s<br/>照片介绍：%s </article></li>\n' %(uploader.point, vote, uploader.name, 10, item.date, uploader.description)
    ret += '''</div></ul></div></div></body><script type="text/javascript" src="../../../static/js/iScroll.js"></script>
    <script type="text/javascript" src="../../../static/js/style.js"></script></html>'''
    return HttpResponse(ret)

@csrf_exempt
def dovote(request):
    pid = request.POST.get("pid")
    uid = request.POST.get("uid")
    if WandaRecord.objects.filter(wxid=uid):
        return HttpResponse(header + u'您已经投过票了，谢谢参与')
    else:
        ret = WandaMember.objects.get(wxid=pid)
        ret.point += 1
        ret.save()
        WandaRecord(wxid=uid,type='vote').save()
        return HttpResponse(header + u'感谢您投下此珍贵的一票')
    
def sendhb(request):
    code = request.GET.get("code")
    wxid = request.GET.get("wxid")
    failimg = request.GET.get("failimg")
    if code:
        wxid = getopenid(code)
    if not code and not wxid:
        return HttpResponse('<html><h1>请不要重复刷新</h1></html>')
    elif code:
        wxid = getopenid(code)
    rcode = share.hongbao('piaoyou', wxid)
    if rcode == u'手气差了点' and failimg:
        return HttpResponse("<html><head><style>body{background-image:url('%s');background-repeat:no-repeat;background-size:cover;background-position:center;}</style></head></html>" %failimg)
    else:
        return HttpResponse("<html><h1>"+rcode+"</h1></html>")

def user(request, userid):
    form_str = u'''<form action="../../douser/" method="post">
    <input type="hidden" name="wxid" value="%s" />
    <label>姓名：</label>&emsp;<input type="text" name="name" size=24 /></br>
    <label>电话：</label>&emsp;<input type="text" name="phone" size=24 /></br>
    <label>地址：</label>&emsp;<input type="text" name="address" size=24 /></br>
    <textarea rows="4" cols="30" name="description" onclick="value='';focus()" >照片描述...</textarea></br>
    <input type="submit" value="提交" /></form></html>''' %userid
    return HttpResponse(share.header("../../../static/css/single.css") + form_str)

@csrf_exempt
def douser(request):
    wxid = request.POST.get("wxid")
    name = request.POST.get("name")
    phone = request.POST.get("phone")
    address = request.POST.get("address")
    description = request.POST.get("description")
    try:
        ret = WandaMember.objects.get(wxid=wxid)
        ret.name = name
        ret.phone = phone
        ret.address = address
        ret.description = description
        ret.save()
        return HttpResponse(header + "信息更新成功")
    except:
        WandaMember(wxid=wxid, name=name, phone=phone, address=address, description=description).save()
        return HttpResponse(header + "信息保存成功")

def buyticket(request):
    code = request.GET.get('code')
    openid = getopenid(code)
    ret = WandaMain.objects.get(id=11)
    return redirect(ret.link+openid)

def shareticket(request):
    code = request.GET.get('code')
    shareurl = request.GET.get('state')
    openid = getopenid(code)
    if shareurl:
        return redirect(shareurl+"&shareid="+openid)
    else:
        ret = WandaMain.objects.get(id=10)
        return redirect(ret.link+openid)

def getopenid(code):
    tk = json.loads(urllib2.urlopen("https://api.weixin.qq.com/sns/oauth2/access_token?appid="+appid+"&secret="+secret+"&code="+code+"&grant_type=authorization_code").read())
    return tk[u'openid']

def award(wxid, point):
    try:
        ret = WandaMember.objects.get(wxid=wxid)
    except:
        WandaMember(wxid=wxid).save()
        ret = WandaMember.objects.get(wxid=wxid)
    ret.point += point
    ret.save()
    return ret

def lucky(msg):
    today = datetime.date.today().isoformat()
    try:
        WandaRecord.objects.get(wxid=msg['FromUserName'],type='piaoyou_share',date=today)
        return share.getTextXml(msg, u'您今天已经参加过抽奖，请明天再试')
    except:
        WandaRecord(wxid=msg['FromUserName'],type='piaoyou_share',date=today).save()
        for aw in WandaAward.objects.all():
            if aw.rate != 0 and aw.amount > 0 and random.random()*aw.rate < 1:
                award(msg['FromUserName'], aw.point)
                aw.amount -= 1
                aw.save()
                return share.getSingleXml(msg, aw.title, aw.description, aw.pic, aw.link)
