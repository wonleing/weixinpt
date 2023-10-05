# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
import xml.etree.ElementTree as ET
from live_hk.models import *
import share, hashlib, urllib2, json, inspect, random, datetime, string, time
TOKEN = "weixinpt"
appid="wx527ad2d4fd80b7a7" #aimiaoke
secret="819cafe7de43557c1ec08513ee4a87fc"
menu = u'''答案好像不对哦，请再接再厉!'''
#smsdir = { 'accesskey':'1069', 'secretkey':'e724fb459d832d821eabc03c75f561fa15b421a3'}
pwd=inspect.stack()[0][1][:-8]
num1 = 0
num2= 0
pool = open(pwd+"codepool","r").readlines()
pool1 = open(pwd+"codepool1","r").readlines()
pool2 = open(pwd+"codepool2","r").readlines()

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
            ret = LiveHkMain.objects.get(id=1)
            return share.getSingleXml(msg, ret.title, "\x0a".join(ret.description.split("^")), ret.pic, ret.link)
        elif msg['Event'] == 'CLICK':
            if msg['EventKey'] == 'newyear':
                try:
                    rec = LiveHkRecord.objects.get(name=msg['FromUserName'], type='ilovemilk_newyear')
                    ret = LiveHkMain.objects.get(id=rec.phone)
                except:
                    ret = LiveHkMain.objects.get(id=random.randint(21,29))
                    LiveHkRecord(name=msg['FromUserName'], phone=ret.id, type='ilovemilk_newyear').save()
                return share.getSingleXml(msg, ret.title, "\x0a".join(ret.description.split("^")), ret.pic, ret.link)
            else:
                return share.getTextXml(msg, u'该功能尚未设定')
    elif msg['MsgType'] == 'text':
        if msg['Content'] == '话题':
            return share.getTextXml(msg, u'<a href="weixinpt.sinaapp.com/live_hk/polling/%s">热门话题调查</a>' %msg['FromUserName'])
        else:
            info = msg['Content'].replace(",","，").replace(":", "：").split("，")
            if len(info) == 2 and len(info[1]) == 11:
                ret = award(msg['FromUserName'], 0)
                ret.name = info[0]
                ret.phone = info[1]
                ret.save()
                return share.getTextXml(msg, u'签到成功！')
            try:
                match = LiveHkMain.objects.get(title=msg['Content'])
            except:
                return share.getTextXml(msg, menu)
            if match.link == "":
            #当link值为空时，猜牛环节循环
                nextlk = match.pic
            elif match.type == 3:
            #口令环节，注意link不能为空，可任意值
                return share.getTextXml(msg, share.hongbao('ilovemilk', msg['FromUserName']))
            else:
            #猜牛通关后，传入wxid
                nextlk = match.link + msg['FromUserName']
            return share.getSingleXml(msg, match.title, "\x0a".join(match.description.split("^")), match.pic, nextlk)

def subpage(request, pageid):
    ret = share.header("../../static/css/subpage.css")
    ret += u'    <title>话题评选</title>\n    <body background="">\n'
    ret += '<div class="news" style="overflow: hidden; white-space: nowrap;">'
    for p in LiveHkTopic.objects.all().order_by('-score'):
        ret += u'<p><font color="#C00000">%d票</font>&emsp;%s</p>' %(p.score, p.description)
    ret += '</div>'
    ret += share.footer
    return HttpResponse(ret)

def showresult(request, type):
    msg = ""
    for i in LiveHkMember.objects.filter(type=type):
        msg += "<p>" + i.name + ", " + i.phone + ", " + i.company + ", " + i.job + "</p>"
    return HttpResponse(msg)

def sendhb(request):
    bid = request.GET.get("bid")
    code = request.GET.get("code")
    wxid = request.GET.get("wxid")
    if code:
        wxid = getopenid(code)
    elif not wxid:
        return HttpResponse('<html><h1>请不要重复刷新</h1></html>')
    return HttpResponse("<html><h1>"+share.hongbao(bid, wxid)+"</h1></html>")

def award(wxid, point):
    try:
        ret = LiveHkMember.objects.get(wxid=wxid)
    except:
        LiveHkMember(wxid=wxid).save()
        ret = LiveHkMember.objects.get(wxid=wxid)
    ret.point += point
    ret.save()
    return ret

def getopenid(code):
    tk = json.loads(urllib2.urlopen("https://api.weixin.qq.com/sns/oauth2/access_token?appid="+appid+"&secret="+secret+"&code="+code+"&grant_type=authorization_code").read())
    return tk[u'openid']
    #info = json.loads(urllib2.urlopen("https://api.weixin.qq.com/sns/userinfo?access_token="+tk[u'access_token']+"&openid="+tk[u'openid']+"&lang=zh_CN").read())
    #return "<html><img width=240px; src="+info[u'headimgurl']+"><p>"+info[u'nickname']+"</p><p>"+info[u'city']+"</p></html>"

def getuserinfo(request):
    #Visit this URL with Wechat, only get openid with snsapi_base, get img and name with snsapi_userinfo
    #https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxd8f34b2d456cc10a&redirect_uri=http://weixinpt.sinaapp.com/live_hk/getuserinfo/&response_type=code&scope=snsapi_base
    code = request.GET.get("code")
    return HttpResponse(getopenid(code))

def getcode(request):
    code1 = "没有中..."
    code2 = "没有中..."
    ip = request.GET.get('ip')
    t = request.GET.get('type')
    a = request.GET.get('a')
    b = request.GET.get('b')
    ret = LiveHkRecord.objects.filter(name=ip, type='code')
    ret1 = LiveHkRecord.objects.filter(name=ip, type='code1')
    ret2 = LiveHkRecord.objects.filter(name=ip, type='code2')
    if ret:
        code = ret[0].phone
    else:
        flag = LiveHkRecord.objects.filter(type='code').count()
        code = pool[flag][:-1]
        LiveHkRecord(name=ip, phone=code,type='code').save()
    if ret1:
        code1 = ret1[0].phone
    elif random.random()*2 < 1:
        flag1 = LiveHkRecord.objects.filter(type='code1').count()
        code1 = pool1[flag1][:-1]
        LiveHkRecord(name=ip, phone=code1,type='code1').save()
    if ret2:
        code2 = ret2[0].phone
    elif random.random()*5 < 0:
        flag2 = LiveHkRecord.objects.filter(type='code2').count()
        code2 = pool2[flag2][:-1]
        LiveHkRecord(name=ip, phone=code2,type='code2').save()
    if t == 'game':
        context = { 'a':a, 'b':b, 'code':code, 'code1':code1, 'code2':code2 }
        return render(request, 'code1.html', context)
    else:
        context = { 'code':code, 'code1':code1, 'code2':code2 }
        return render(request, 'code.html', context)

def sharewx(request):
    bid = request.GET.get('bid')
    ret = LiveHkAward.objects.get(bid=bid)
    sign = Sign("http://weixinpt.sinaapp.com"+request.get_full_path())
    jsparams = sign.sign()
    if ret.rate != 0 and ret.amount > 0 and random.random()*ret.rate < 1: 
        link = ret.link
        ret.amount -= 1
        ret.save()    
    else:
        link="http://ww3.sinaimg.cn/mw690/558fe6e3gw1ejdfrww623j206o06oq34.jpg"
    context = { 'event':ret.type, 'picture':ret.pic, 'link':link, 'jsp':jsparams, 'appid':appid}
    return render(request, 'sharewx.html', context)

def baoming(request):
    tp = request.GET.get('type')
    wecha_id = request.GET.get('wecha_id')
    name = request.GET.get('name')
    phone = request.GET.get('phone')
    company = request.GET.get('company')
    job = request.GET.get('job')
    if LiveHkMember.objects.filter(name=name, phone=phone):
        return HttpResponse("你已经填写过了")
    if tp=='beiqi':
        LiveHkMember(name=name, phone=phone, type=tp).save()
        return redirect('http://jyousoft.com/index.php?g=Wap&m=Lottery&a=index&token=fmomcc1407945037&type=1&id=140&wecha_id=' + wecha_id)
    elif tp=='haier':
        LiveHkMember(name=name, phone=phone, company=company, job=job, type=tp).save()
        return redirect('http://jyousoft.com/web/haier')
    else:
        LiveHkMember(name=name, phone=phone, company=company, job=job, type=tp).save()
        return HttpResponse("信息提交成功")

def polling(request):
    return render(request, 'poll.html', context)

def dopoll(request):
    choices = request.POST.getlist('choices')
    uid = request.POST.get('uid')
    if LiveHkRecord.objects.filter(name=uid):
        return HttpResponse("<h1>您已经参加过调查，感谢您的参与！<br/><a href='../1/'>点击查看调查统计</a></h1>")
    else:
        for c in choices:
            ret = LiveHkTopic.objects.get(id=int(c))
            ret.score += 1
            ret.save()
        LiveHkRecord(name=uid, phone='', type='poll').save()
        return HttpResponse("<h1>提交完成，感谢您的参与！<br/><a href='../1/'>点击查看调查统计</a></h1>")

def lucky(request, round):
    phones = [13810776712,13120437317]
    if round == '1':
       num = 10
       des = '爱牛奶T恤（Ilovemilk T-shirt)  %d件' %num
    elif round == '2':
       num = 3
       des = '金郁金香（Golden Tulip）  %d个' %num
    dig = []
    for i in range(num):
        dig.append(i+1)
    #ret = LiveHkMember.objects.filter(point=type).exclude(phone="")
    #for r in ret:
    #    phones.append(int(r.phone))
    context = {
        'phones': phones,
        'num': dig,
        'des': des,
    }
    return render(request, 'lucky.html', context)

class Sign:
    def __init__(self, url):
        t = urllib2.urlopen("http://123.206.26.34/html/piaoyou_jsapiticket.json").read()
        jsapi_ticket = json.loads(t)['jsapi_ticket']
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        #return string
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        return self.ret
