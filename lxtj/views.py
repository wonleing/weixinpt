# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
import xml.etree.ElementTree as ET
from lxtj.models import *
import share, hashlib, random, urllib2, json, re, datetime
from wxpay import build_form, xml_to_dict
TOKEN = "weixinpt"
menu = u'欢迎使用家视天下微信服务。\x0a在微信中输入或语音说出频道名（比如电影），便可查看相应节目单，简单又实用。'
dnsname = "http://weixinpt.sinaapp.com"
serverIP = "http://api.domybox.com"
bluerayIP = "http://blueapi.pthv.gitv.tv/blue-ray"
vnumber = 9
pay_param = {
    'appId': 'wx5527ac2672f6de0f',
    'appSecret': '843509cf762f7b65f7bb9dec2e720913',
    'paySignKey': 'C3RBVo2mcf2daeCjCFSLK5H1QE8pAkZPqGvPhGgaGya4UGEnNz5wb80lGhxpJqpUS26M61oy9cPH529Hd29tTmMlm0NNmwshLM7AYeIeu3MroA63Upp10KMU6elzqLUz',
    'partnerId': '1218950901',
    'partnerKey': '963721c24951cd8531fc152fb7d9e090',
    #'notify_url': 'http://124.207.119.66/wx/phoneNotify.json'
    'notify_url': 'http://125.39.118.37/pay_service/wx/mobileNotify.json'
}

def trim(orig):
    if len(orig) > 10:
        return orig[:9]+"..."
    else:
        return orig

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
    t = request.GET.get("t", None)
    nonce = request.GET.get("nonce", None)
    echoStr = request.GET.get("echostr",None)
    tmpList = [TOKEN,timestamp,nonce]
    tmpList.sort()
    tmpstr = "%s%s%s" % tuple(tmpList)
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return echoStr
    else:
        if t == '10':
            updateChannel()
        elif t == '11':
            updateFree()
        elif t == '20':
            updateCP()
        elif t == '21':
            updateLg()
        return "Channel %s info updated" %t

def responseMsg(request):
    rawStr = smart_str(request.raw_post_data)
    msg = share.paraseMsgXml(ET.fromstring(rawStr))
    if msg['MsgType'] == 'event':
        if msg['Event'] == 'subscribe':
            return share.getTextXml(msg, menu)
        elif msg['Event'] == 'CLICK':
            if msg['EventKey'] == 'free':
                return share.getSingleXml(msg, u'免费影片专区', u'本区内容由爱奇艺提供', 'http://photocdn.sohu.com/20120323/vrsab_hor1010436_pic25.jpg', dnsname+'/lxtj/category/1/?wxid='+msg['FromUserName'])
            elif msg['EventKey'] == 'charge':
                return share.getSingleXml(msg, u'付费影片专区', u'在这里可以使用微信支付购买付费影片，轻松便捷', 'http://photocdn.sohu.com/20120323/vrsab_hor1010436_pic25.jpg', dnsname+'/lxtj/languang/?wxid='+msg['FromUserName'])
            elif msg['EventKey'] == 'bind':
                return share.getTextXml(msg, u'绑定设备后，您可在此与您的大麦盒子进行互动，绑定方法：\x0a1、请确保手机与大麦盒子在同一路由下；\x0a2、在此回复电视上的设备码\x0a设备码位置：盒子>用户中心>设备绑定>微信设备码')
            elif msg['EventKey'] == 'search':
                return share.getTextXml(msg, u'欢迎使用强大无节操的频道搜索功能：\x0a1、文字搜索\x0a回复文字信息比如“电影”\x0a2、语音搜索\x0a回复语音即可得到你想要的频道，比如“电视剧”')
            elif msg['EventKey'] == 'help':
                return share.getSingleXml(msg, u'常见问题解答', u'在这里可以找到常见问题的解答。如果没有合适您的答案，可直接在微信中输入您的问题，我们会尽快解答。', 'https://mmbiz.qlogo.cn/mmbiz/XFTnL1MzGaDe83bOCHoyibv1hxib06kM6lnOtVghoguGbwXhfzsf1WibVlEBpJSzh2PqFDulrTqictlickI7DPUzuBQ/0', 'http://mp.weixin.qq.com/s?__biz=MjM5MTIyOTQxNA==&mid=200546913&idx=1&sn=612872b542ffcdf85c54df248ce6f3fd#rd')
            elif msg['EventKey'] == 'control':
                try:
                    ret = LxtjMember.objects.get(wxid=msg['FromUserName'])
                    return share.getTextXml(msg, '<a href="http://'+ret.ip+u':11111">点击进入摇控器</a>\x0a在这里您可以摇控盒子播放,请确保盒子已在同WIFI网络下开启')
                except:
                    return share.getTextXml(msg, u'请先点击菜单中“设备绑定”，按照提示的步骤绑定设备码')
            else:
                return share.getTextXml(msg, u'该功能尚未设定')
    elif msg['MsgType'] == 'text':
        if re.match("^\w{9}$", msg['Content']):
            try:
                old = LxtjMember.objects.get(wxid=msg['FromUserName'])
                old.wxid = ""
                old.save()
            except:
                pass
            try:
                ret = LxtjMember.objects.get(sn=msg['Content'])
                ret.wxid = msg['FromUserName']
                ret.save() 
                return share.getTextXml(msg, u'盒子绑定成功')
            except:
                return share.getTextXml(msg, u'绑定失败，请确认输入的SN码正确')
        else:
            return search(msg, msg['Content'])
    elif msg['MsgType'] == 'voice':
        return search(msg, msg['Recognition'])
    return share.getTextXml(msg, share.randomreply(LxtjMain)+menu)

def search(msg, name):
    try:
        ret = LxtjMain.objects.get(title=name)
        return share.getSingleXml(msg, ret.title, "\x0a".join(ret.description.split(" ")), ret.pic, ret.link)
    except:
        return share.getTextXml(msg, u'没有找到相应的频道')

#def pop(msg, number):
#    try:
#        ret = LxtjMain.objects.get(id=number)
#    except:
#        return share.getMultiXml(msg, '', LxtjMain.objects.all().order_by('id'))
#    return share.getSingleXml(msg, ret.title, "\x0a".join(ret.description.split(" ")), ret.pic, ret.link)

def subpage(request, pageid):
    ret = share.header("../../static/css/subpage.css")
    root = LxtjMain.objects.get(id=pageid)
    ret += '    <title>%s</title>\n    <body>\n' % root.title
    ret += share.submenu(LxtjMain)
    ret += '''        <div class="listData" id="wrapper"><div id="scroller"><ul>\n'''
    try:
        list = eval("Lxtj%s" %pageid).objects.all().order_by('id')
    except:
        return HttpResponse(u'亲，此页不存在哦')
    for item in list:
        ret += share.sublayout(item)
    ret += share.footer
    return HttpResponse(ret)

def detail(request, cid, vid):
    wxid = request.GET.get("wxid")
    try:
        #ret = LxtjFree.objects.get(id=vid)
        #change to use API instead of cache
        ret = json.loads(urllib2.urlopen(serverIP+"/api/open/video/mobile/VideoSetDetail/"+vid+"/1.json").read())['result']
    except:
        return HttpResponse(u'该视频没有找到')
    content = {}
    number = 0
    try:
        user = LxtjMember.objects.get(wxid=wxid)
        boxip = user.ip
    except:
        return HttpResponse(u'请先在微信中绑定设备码，具体流程可参考菜单中的帮助')
    if cid == '2' or cid == '4':
        type = 3
        number = ret['videoset_update']
    elif cid == '6':
        type = 2
        vlist = json.loads(urllib2.urlopen(serverIP+"/api/open/video/mobile/VideoList/"+vid+"/6/1/100/1.json", timeout=1).read())['result']
        number = len(vlist)
        for r in vlist:
            content[r['phase']]=r['video_name']
    else:
        type = 1
    playurl = "http://"+boxip+":11111/startPlayer?cpId="+cid+"&albumId="+vid+"&isFree=true&tvId="
    ret['title'] = ret['videoset_name']
    ret['pic'] = ret['videoset_img']
    ret['suetime'] = ret['is_suetime']
    ret['description'] = ret['videoset_brief']
    ret['director'] = trim(ret['director'])
    ret['actors'] = trim(ret['actors'])
    context = {
        'ret': ret,
        'number': 'x'*number,
        'content': content,
        'type': type,
        'playurl': playurl,
    }
    return render(request, 'jiashitianxia/detail.html', context)

def payarea(request):
    if request.GET.get("notpay"):
        return HttpResponse(u'请购买后再播放')
    wxid = request.GET.get("wxid")
    vid = request.GET.get("vid")
    opid = request.GET.get("opid")
    op = LxtjCharge.objects.get(operationid=opid)
    try:
        box = LxtjMember.objects.get(wxid=wxid)
    except:
        return HttpResponse(u'付费播放必须先绑定设备码')
    type = 3 # take it as TV series
    if LxtjPayment.objects.filter(sn=box.sn, cpid=op.cpid):
        ispaied = 1
        playurl = "http://"+box.ip+":11111/startPlayer?&cpId="+op.cpid+"&albumId="+vid+"&isFree=false&tvId="
    else:
        ispaied = None
        playurl = "?notpay="
    try:
        #ret = LxtjLg.objects.get(id=int(vid))
        #change to use API instead of cache
        ret = json.loads(urllib2.urlopen(bluerayIP+"/api/v/album/"+vid+"-.json").read())['data']['result']
    except:
        return HttpResponse(u'该视频没有找到'+vid)
    if wxid:
        payform = payable(box.sn, op.cpid, op.price, request.META.get('REMOTE_ADDR', ''))
    else:
        payform = ""
    recommend = json.loads(urllib2.urlopen(bluerayIP+"/api/r/Recommend/1-5-"+op.cpid+"-"+vid+".json").read())['data']['result']['pageContent']
    ret['title'] = ret['albumName']
    ret['director'] = trim(ret['directors'])
    ret['tag'] = ret['labels']
    ret['actors'] = trim(ret['mainActors'])
    ret['pic'] = ret['picUrl']
    ret['description'] = ret['albumDesc']
    ret['price'] = op.price
    ret['origprice'] = op.origprice
    context = {
        'ret': ret,
        'type': type,
        'number': 'x'*len(ret['videoList']),
        'ispaied': ispaied,
        'payform': payform,
        'playurl': playurl,
        'recommend': recommend,
        'wxid': wxid,
        'opid': opid,
    }
    return render(request, 'jiashitianxia/detail.html', context)

def languang(request):
    category = LxtjCharge.objects.filter(active=1).order_by('operationid')
    wxid = request.GET.get("wxid")
    list = {}
    for c in category:
        content = LxtjLg.objects.filter(cateid=c.operationid)
        list[c.operationid] = content
    context = {
        'category': category,
        'keys': sorted(list),
        'list': list,
        'cid': 1,
        'wxid': wxid,
        'charge':1
    }
    return render(request, 'jiashitianxia/category.html', context)

def category(request, cid):
    category = LxtjMain.objects.all().order_by('id')
    wxid = request.GET.get("wxid")
    list = {}
    for c in category:
        content = LxtjFree.objects.filter(cateid=c.id)
        list[c.id] = content
    context = {
        'category': category,
        'keys': sorted(list),
        'list': list,
        'cid': cid,
        'wxid': wxid
    }
    return render(request, 'jiashitianxia/category.html', context)

def getmore(request, type, cid, number):
    if type == 'free':
        raw = urllib2.urlopen(serverIP+"/api/open/video/mobile/VideoSetList/"+cid+"/"+str(vnumber)+"/"+number+"/1.json", timeout=5).read()
        if cid=='1' or cid=='2' or cid=='4' or cid=='6':
            return HttpResponse(raw.replace(".jpg","_260_360.jpg"))
        else:
            return HttpResponse(raw.replace(".jpg","_320_180.jpg"))
    elif type == 'charge':
        return HttpResponse(urllib2.urlopen(bluerayIP+"/api/r/operation/"+number+"-"+str(vnumber)+"--"+cid+"-.json", timeout=5).read())

def iprefresh(request):
    ip = str(request.GET.get('ip'))
    sn = str(request.GET.get('sn'))
    if len(ip.split("."))==4 and len(sn)==9:
        ret = LxtjMember.objects.filter(sn=sn)
        if ret:
            ret[0].ip = ip
            ret[0].save()
            return HttpResponse("IP refreshed")
        else:
            LxtjMember(sn=sn, ip=ip).save()
            return HttpResponse("New SN and IP added")
    else:
        return HttpResponse("IP or SN format error, please check their lenth")

def updateChannel():
    LxtjMain.objects.all().delete()
    raw = json.loads(urllib2.urlopen(serverIP+"/api/open/video/mobile/FirstClassList/1/1.json").read())
    ret = sorted(raw['result'], key=lambda k: k['firstclass_id'])
    LxtjMain.objects.all().delete()
    count=1
    for r in ret:
        LxtjMain(id=r['firstclass_id'],title=r['firstclass_name'],pic=r['icon'],link=dnsname+"/lxtj/category/"+str(count)).save()
        count += 1

def updateCP():
    LxtjCharge.objects.all().delete()
    for i in ["1","4","7","9"]:
        cp = json.loads(urllib2.urlopen(bluerayIP+"/api/p/getPrice/"+i+"-2001.json").read())['data']['result'][0]
        raw = json.loads(urllib2.urlopen(bluerayIP+"/api/r/operation_tag/"+i+".json").read())
        for j in sorted(raw['data']['result'], key=lambda k: k['operationTagId']):
            LxtjCharge(operationid=j["operationTagId"], cpid=j["cpId"], title=j["operationTagName"], origprice=int(cp['price']), \
            price=int(cp['vipPrice']), active=0).save()

def updateFree():
    LxtjFree.objects.all().delete()
    for i in LxtjMain.objects.all():
        raw = json.loads(urllib2.urlopen(serverIP+"/api/open/video/mobile/VideoSetList/"+str(i.id)+"/"+str(vnumber)+"/1/1.json").read())
        for r in raw['result']['pageContent']:
            if i.id==1 or i.id==2 or i.id==4 or i.id==6:
                r['videoset_img'] = r['videoset_tv_img'].replace(".jpg","_260_360.jpg")
            else:
                r['videoset_img'] = r['videoset_img'].replace(".jpg","_320_180.jpg")
            if not r['is_suetime']:
                r['is_suetime'] = ""
                r['score'] = ""
                r['isSeries'] = 0
                r['videoset_update'] = 0
            LxtjFree(id=r['videoset_id'],cateid=i.id,title=r['videoset_name'],description=r['videoset_brief'],pic=r['videoset_img'],tag=r['tag'],suetime=r['is_suetime'],director=r['director'],actors=r['actors'],focus=r['videoset_focus'],score=r['score'],series=r['isSeries'],update=r['videoset_update'],link="/lxtj/detail/"+str(r['videoset_type'])+"/"+str(r['videoset_id'])).save()

def updateLg():
    LxtjLg.objects.all().delete()
    for i in LxtjCharge.objects.filter(active=1):
        raw = json.loads(urllib2.urlopen(bluerayIP+"/api/r/operation/1-9--"+i.operationid+"-.json").read())
        for video in raw['data']['result']['pageContent']:
            r = json.loads(urllib2.urlopen(bluerayIP+"/api/v/album/"+str(video['contentId'])+"-.json").read())['data']['result']
            LxtjLg(id=r['albumId'],cateid=int(i.operationid),title=r['albumName'],description=r['albumDesc'],pic=r['picUrl'],tag=r['labels'],suetime=r['year'],director=r['directors'],actors=r['mainActors'],focus=r['focus'],score=r['score'],link="/lxtj/payarea/?vid="+str(r['albumId'])).save()

def payment_notify(request):
    params = request.GET.get('out_trade_no').split("-")
    total_fee = int(request.GET.get('total_fee'))/100
    if not LxtjPayment.objects.filter(sn=params[0], cpid=params[1]):
        LxtjPayment(sn=params[0], cpid=params[1], fee=total_fee).save()
    return HttpResponse('success')

def payable(sn, cpid, price, remote_ip):
    parameter = {
        'body': u'本影厅包年价格为：'+str(price)+' RMB.',
        'out_trade_no': sn+"-"+str(cpid)+"-"+datetime.date.today().strftime('%Y%m%d'),
        'spbill_create_ip': remote_ip,
        'total_fee': str(price*100),
    }
    parameter.update(pay_param)
    return build_form(parameter)
