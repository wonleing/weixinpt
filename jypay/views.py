# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
from django.db.models import Q
from django.core import serializers
import xml.etree.ElementTree as ET
from jypay.models import *
import share, hashlib, time, datetime, random, urllib2, json, string, re
from wxpay import build_form, xml_to_dict
import alipay
TOKEN = "weixinpt"
access_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
remind_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s"
oauth_url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&grant_type=authorization_code&code=%s"
userinfo_url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN"
wx_notify_url = "http://weixinpt.sinaapp.com/jypay/payment_notify_wx/"
ali_notify_url = "http://weixinpt.sinaapp.com/jypay/payment_notify_ali/"
ali_return_url = 'http://weixinpt.sinaapp.com/jypay/comment?rawid=ali&memberid=%s'
aligateway = 'https://openapi.alipay.com/gateway.do?'

@csrf_exempt
def handleRequest(request):
    if request.method == 'GET':
        JypayRecord.objects.filter(status=2).delete()
        return HttpResponse("Unpaied record deleted")
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
        return share.getMultiXml(msg, u'欢迎使用捷优支付，具体功能请点击下方菜单，商户功能须先绑定才可使用。更多信息请参见www.jyousoft.com')
    elif msg['MsgType'] == 'text':
        info = msg['Content'].replace(",","，").split("，")
        info2 = msg['Content'].replace("－","-").split("-")
        if len(info) == 2:
            try:
                ret = JypayMember.objects.get(memberid=info[0], password=info[1])
                for old in JypayMember.objects.filter(wxid=msg['FromUserName']):
                    old.wxid = ""
                    old.save()
                ret.wxid = msg['FromUserName']
                ret.save()
                return share.getTextXml(msg, u"收款渠道绑定成功，您可以进入渠道页面编辑信息、查看收款二维码页面了")
            except:
                return share.getTextXml(msg, u"信息输入错误，请确认用户名密码输入正确")
        if len(info2) == 2:
            try:
                ret = JypayCenter.objects.get(centerid=info2[0], password=info2[1])
                for old in JypayCenter.objects.filter(wxid=msg['FromUserName']):
                    old.wxid = ""
                    old.save()
                ret.wxid = msg['FromUserName']
                ret.save()
                return share.getTextXml(msg, u"商户中心绑定成功，您可以进入商户中心及注册收款渠道了")
            except:
                return share.getTextXml(msg, u"信息输入错误，请确认用户名密码输入正确")

def s(ret):
    return serializers.serialize("json", ret)

def index(request, cname):
    t = request.GET.get('type')
    perpage = request.GET.get('perpage')
    pageno = request.GET.get('pageno')
    if not t or t == 'all':
        ret = JypayMember.objects.all()
    else:
        ret = JypayMember.objects.filter(type=int(t))
    ret = ret.filter(fromagent=cname)
    if perpage and pageno:
        ret = ret[int(perpage)*int(pageno)-int(perpage):int(perpage)*int(pageno)]
    center = JypayCenter.objects.get(centerid=cname)
    if center.description[:4] == 'http':
        f_link = center.description
        f_name = center.name
    else:
        f_link = 'http://www.jyousoft.com'
        f_name = u'捷优软件'
    cinfo = (center.type1, center.type2, center.type3, center.type4, center.type5, center.type6, center.man, center.jian)
    baseurl = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid='+center.appid+'&response_type=code&scope=snsapi_base&redirect_uri=http://weixinpt.sinaapp.com/jypay/chargepage/?memberid='
    if request.GET.get('json'):
        context = { 'memberlist':s(ret), 'baseurl':baseurl, 'cinfo':s(cinfo) }
        return HttpResponse(str(context))
    else:
        context = { 'memberlist':ret, 'baseurl':baseurl, 'cinfo':cinfo, 'cssfile':center.cssfile, 'f_link':f_link, 'f_name':f_name }
        return render(request, 'jypay/index.html', context)

def query(request):
    memberid = request.GET.get('mid')
    stime = request.GET.get('stime')
    etime = request.GET.get('etime')
    if stime and etime and memberid:
        stime = datetime.datetime.strptime(stime, "%Y%m%d")
        etime = datetime.datetime.strptime(etime, "%Y%m%d")
        records = JypayRecord.objects.filter(memberid=memberid, status=1, date__gt=stime, date__lt=etime)
        if len(records) > 0:
            context = { 'records': records }
            return render(request, 'jypay/query.html', context)
        else:
            return HttpResponse('无匹配记录')
    else:
        return HttpResponse('缺少必要参数')

def chargepage(request):
    memberid = request.GET.get('memberid')
    code = request.GET.get('code')
    inputid = request.GET.get('userid')
    password = request.GET.get('password')
    openid = ''
    ret2 = JypayMember.objects.filter(memberid=memberid)
    center = JypayCenter.objects.get(centerid=ret2[0].fromagent)
    if center.description[:4] == 'http':
        f_link = center.description
        f_name = center.name
        f_phone = center.phone
    else:
        f_link = 'http://www.jyousoft.com'
        f_name = u'捷优软件'
        f_phone = '13810776712'
    if len(ret2) != 1:
        return HttpResponse('未找到该服务渠道')
    if inputid:
        ret1 = JypayUser.objects.filter(userid=inputid, password=password)
        if len(ret1) != 1:
            return HttpResponse('用户ID认证失败')
        else:
            rawid = ret1[0].wxid or ret1[0].userid
    elif code:
        tk = json.loads(urllib2.urlopen(oauth_url %(center.appid,center.secret,code)).read())
        if 'openid' in tk:
            request.session['openid'] = tk['openid'] #重新生成成功，写入缓存
        if 'openid' in request.session:
            openid = request.session['openid'] #读取缓存
        else:
            return HttpResponse('openid get failed')
        ret1 = JypayUser.objects.filter(wxid=openid)
        rawid = openid
    else:
        ret1 = False
        rawid = ''
    if ret1:
        balance = ret1[0].balance
    else:
        balance = 0
    comments = []
    cmt = JypayComment.objects.filter(memberid=memberid)
    cm0 = len(cmt.filter(status=0))
    cm1 = len(cmt.filter(status=1))
    cm2 = len(cmt.filter(status=2))
    cm3 = len(cmt.filter(status=3))
    cm4 = len(cmt.filter(status=4))
    cm5 = len(cmt.filter(status=5))
    cnumber = len(cmt)
    if cnumber > 0:
        crate = str((cm1+(cm2*2)+(cm3*3)+(cm4*4)+(cm5*5))/float(cnumber))[:4]
    else:
        crate = 0
    for c in cmt.order_by('-commentid')[:20]:
        user = JypayUser.objects.get(userid=c.userid)
        dname = user.name or user.phone or '匿名'
        image = user.pic if user.pic else "https://up.enterdesk.com/edpic/b3/d6/2e/b3d62ef41f0bb610a69a7d6041e38a71.jpg"
        comments.append({'dname':dname, 'status':c.status, 'tip':c.tip, 'image':image, 'content':c.content, 'date':c.date})
    if request.GET.get('json'):
        context = {'minfo':s(ret2),'openid':rawid,'balance':balance,'comments':s(comments),'cnumber':cnumber,'crate':crate,'logo':center.logo}
        return HttpResponse(str(context))
    else:
        context = { 'minfo':ret2[0],'openid':rawid,'balance':balance,'comments':comments,'cnumber':cnumber,'crate':crate,'logo':center.logo,'cssfile':center.cssfile, 'f_link':f_link, 'f_name':f_name, 'f_phone':f_phone }
        return render(request, 'jypay/chargepage.html', context)

def centerdetail(request, cname):
    inputid = request.GET.get('centerid')
    password = request.GET.get('password')
    code = request.GET.get('code')
    mlist = []
    center = JypayCenter.objects.get(centerid=cname)
    if center.description[:4] == 'http':
        f_link = center.description
        f_name = center.name
    else:
        f_link = 'http://www.jyousoft.com'
        f_name = u'捷优软件'
    if inputid:
        ret1 = JypayCenter.objects.filter(centerid=inputid, password=password)
    else:
        tk = json.loads(urllib2.urlopen(oauth_url %(center.appid,center.secret,code)).read())
        if 'openid' in tk:
            openid = tk['openid'] #重新生成
        elif 'openid' in request.session:
            openid = request.session['openid'] #缓存
        else:
            openid = ''
        ret1 = JypayCenter.objects.filter(wxid=openid)
    if len(ret1) != 1:
        return HttpResponse('<h1>请先进行商户绑定</h1>')
    else:
        centerid = ret1[0].centerid
        request.session['openid'] = ret1[0].wxid
    outlist = JypayMsg.objects.filter(centerid=centerid).order_by("-date")
    for m in JypayMember.objects.filter(fromagent=centerid):
        mb = {}
        mb['memberid'] = m.memberid
        mb['total'] = m.total
        mb['balance'] = m.balance
        mb['yesterday'] = 0
        mb['thismonth'] = 0
        today = datetime.date.today()
        for mrec in JypayRecord.objects.filter(status=1, memberid=m.memberid, date__year=today.year, date__month=today.month):
            mb['thismonth'] += mrec.amount
        y = datetime.date.today() - datetime.timedelta(days=1)
        for drec in JypayRecord.objects.filter(status=1, memberid=m.memberid, date__year=y.year, date__month=y.month, date__day=y.day):
            mb['yesterday'] += drec.amount
        mlist.append(mb)
    if request.GET.get('json'):
        context = { 'cinfo':s(ret1), 'outlist':s(outlist), 'mlist':s(mlist) }
        return HttpResponse(str(context))
    else:
        context = { 'cinfo': ret1[0], 'outlist': outlist, 'mlist':mlist, 'cssfile':center.cssfile, 'f_link':f_link, 'f_name':f_name }
        return render(request, 'jypay/centerdetail.html', context)

def checkdetail(request, cname):
    inputid = request.GET.get('memberid')
    password = request.GET.get('password')
    code = request.GET.get('code')
    center = JypayCenter.objects.get(centerid=cname)
    if center.description[:4] == 'http':
        f_link = center.description
        f_name = center.name
    else:
        f_link = 'http://www.jyousoft.com'
        f_name = u'捷优软件'
    if inputid:
        ret1 = JypayMember.objects.filter(memberid=inputid, password=password)
    else:
        tk = json.loads(urllib2.urlopen(oauth_url %(center.appid,center.secret,code)).read())
        #tk = urllib2.urlopen("http://123.206.26.34/html/getwxid.php?appid=%s&appsecret=%s&code=%s" %(center.appid,center.secret,code)).read()
        if 'openid' in tk:
            openid = tk['openid'] #重新生成
        elif 'openid' in request.session:
            openid = request.session['openid'] #缓存
        else:
            openid = ''
        ret1 = JypayMember.objects.filter(wxid=openid)
    if len(ret1) != 1:
        return HttpResponse('<h1>请先进行收款渠道绑定</h1>')
    else:
        memberid = ret1[0].memberid
        request.session['openid'] = ret1[0].wxid
    cinfo = JypayCenter.objects.filter(centerid=ret1[0].fromagent)
    ret2 = JypayRecord.objects.filter(memberid=memberid, status=1).order_by("-date")[:1000]
    ret3 = JypayMsg.objects.filter(memberid=memberid).order_by("-date")[:30]
    if request.GET.get('json'):
        context = { 'minfo':s(ret1), 'cinfo':s(cinfo), 'inlist':s(ret2), 'outlist':s(ret3) }
        return HttpResponse(str(context))
    else:
        context = { 'minfo': ret1[0], 'cinfo':cinfo[0], 'inlist': ret2, 'outlist': ret3, 'cssfile':center.cssfile, 'f_link':f_link, 'f_name':f_name }
        return render(request, 'jypay/checkdetail.html', context)

def userdetail(request, cname):
    inputid = request.GET.get('userid')
    password = request.GET.get('password')
    code = request.GET.get('code')
    center = JypayCenter.objects.get(centerid=cname)
    if center.description[:4] == 'http':
        f_link = center.description
        f_name = center.name
    else:
        f_link = 'http://www.jyousoft.com'
        f_name = u'捷优软件'
    token = json.loads(urllib2.urlopen(access_url%(center.appid,center.secret)).read())['access_token']
    if inputid:
        ret1 = JypayUser.objects.filter(userid=inputid, password=password)
    else:
        tk = json.loads(urllib2.urlopen(oauth_url %(center.appid,center.secret,code)).read())
        if 'openid' in tk:
            openid = tk['openid'] #重新生成
        elif 'openid' in request.session:
            openid = request.session['openid'] #缓存
        else:
            openid = ''
        ret1 = JypayUser.objects.filter(wxid=openid)
    if len(ret1) == 0:
        info = json.loads(urllib2.urlopen(userinfo_url %(token, openid)).read())
        sex = u'，男' if info[u'sex']==1 else u'，女'
        des = info[u'country']+info[u'province']+info[u'city']+sex
        JypayUser(name=info[u'nickname'], wxid=openid, type=0, pic=info[u'headimgurl'], description=des, \
        jointime=str(datetime.date.today())).save()
        ret1 = JypayUser.objects.filter(wxid=openid)
        ret2 = []
    else:
        userid = ret1[0].userid
        request.session['openid'] = ret1[0].wxid
        if not (ret1[0].name or ret1[0].description):
            info = json.loads(urllib2.urlopen(userinfo_url %(token, openid)).read())
            sex = u'，男' if info[u'sex']==1 else u'，女'
            des = info[u'country']+info[u'province']+info[u'city']+sex
            ret1[0].name = info[u'nickname']
            ret1[0].pic = info[u'headimgurl']
            ret1[0].description = des
            ret1[0].save()
        ret2 = JypayRecord.objects.filter(userid=userid).order_by("-date")[:100]
    if request.GET.get('json'):
        context = { 'userinfo':serializers.serialize("json", ret1), 'spendlist':serializers.serialize("json", ret2) }
        return HttpResponse(str(context))
    else:
        context = { 'userinfo': ret1[0], 'spendlist': ret2, 'cssfile':center.cssfile, 'f_link':f_link, 'f_name':f_name }
        return render(request, 'jypay/userdetail.html', context)

def qrcode(request):
    memberid = request.GET.get('memberid')
    center = JypayCenter.objects.get(centerid=JypayMember.objects.get(memberid=memberid).fromagent)
    if center.description[:4] == 'http':
        f_phone = center.phone
        f_name = center.name
    else:
        f_phone = '13810776712'
        f_name = u'捷优软件'
    baseurl = 'https://api.nbhao.org/v1/qrcode/make?text=https://open.weixin.qq.com/connect/oauth2/authorize?appid='+center.appid+'%26response_type=code%26scope=snsapi_base%26redirect_uri=http://weixinpt.sinaapp.com/jypay/chargepage/?memberid='
    try:
        ret = JypayMember.objects.get(memberid=memberid)
    except:
        return HttpResponse('<h1>无此商户</h1>')
    context = { 'baseurl':baseurl, 'minfo':ret, 'cinfo':center, 'cssfile':center.cssfile, 'f_phone':f_phone, 'f_name':f_name }
    return render(request, 'jypay/qrcode.html', context)

@csrf_exempt
def doout(request):
    amount = float(request.POST.get('amount'))
    member = JypayMember.objects.get(memberid=request.POST.get('memberid'))
    center = JypayCenter.objects.get(centerid=request.POST.get('centerid'))
    if amount > 0 and member.balance > 0:
        JypayMsg(centerid=center.centerid, memberid=member.memberid, amount=amount, accountinfo=member.accountinfo).save()
        member.balance -= amount
        center.balance -= amount
        member.save()
        center.save()
        return HttpResponse('余额结算完毕')
    else:
        return HttpResponse('无可结算余额')

def comment(request):
    memberid = request.GET.get('memberid')
    rawid = request.GET.get('rawid')
    center = JypayCenter.objects.get(centerid=JypayMember.objects.get(memberid=memberid).fromagent)
    if center.description[:4] == 'http':
        f_link = center.description
        f_name = center.name
    else:
        f_link = 'http://www.jyousoft.com'
        f_name = u'捷优软件'
    if not rawid.isdigit():
        try:
            rawid = JypayUser.objects.get(wxid=rawid).userid
        except:
            rawid = ''
    try:
        JypayMember.objects.get(memberid=memberid)
    except:
        return HttpResponse('<h1>未找到该渠道</h1>')
    context = { 'memberid': memberid, 'userid': rawid, 'cssfile':center.cssfile, 'f_link':f_link, 'f_name':f_name }
    return render(request, 'jypay/comment.html', context)

@csrf_exempt
def docomment(request):
    userid = request.POST.get('userid')
    phone = request.POST.get('phone')
    memberid = request.POST.get('memberid')
    content = request.POST.get('content')
    status = request.POST.get('status')
    if not userid and not phone:
        return HttpResponse('<h1>请填写电话</h1>')
    elif phone:
        try:
            user = JypayUser.objects.get(phone=phone)
        except:
            user = JypayUser(type=0, phone=phone, jointime=str(datetime.date.today()))
            user.save()
    else:
        user = JypayUser.objects.get(userid=userid)
    userid = user.userid
    #if not JypayComment.objects.filter(Q(memberid=memberid) | Q(userid=user.userid)) and user.total<10:
    #    user.balance += 1
    #    user.total += 1
    #    user.save()
    if not status:
        status = 5 
    try:
        highpoints = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    content = highpoints.sub(u'\u25FD', content)
    try:
        ret = JypayMember.objects.get(memberid=memberid)
        center = JypayCenter.objects.get(centerid=ret.fromagent)
    except:
        return HttpResponse('未找到该渠道')
    JypayComment(memberid=memberid, userid=int(userid), content=content, status=int(status)).save()
    return HttpResponse('<img src="'+center.pic+'" width="100%"/>')

@csrf_exempt
def dologin(request):
    phone = request.POST.get('phone')
    password = request.POST.get('password')
    memberid = request.POST.get('memberid')
    isb = request.POST.get('isb')
    if isb=='0':
        try:
            ret = JypayUser.objects.get(phone=phone, password=password)
            return HttpResponse(ret.userid)
        except:
            return HttpResponse("登录失败")
    else:
        try:
            ret = JypayMember.objects.get(memberid=memberid, password=password)
            return HttpResponse(ret.memberid)
        except:
            return HttpResponse("登录失败")

def register(request, cname):
    inputid = request.GET.get('centerid')
    password = request.GET.get('password')
    code = request.GET.get('code')
    center = JypayCenter.objects.get(centerid=cname)
    if center.description[:4] == 'http':
        f_link = center.description
        f_name = center.name
    else:
        f_link = 'http://www.jyousoft.com'
        f_name = u'捷优软件'
    if inputid:
        ret1 = JypayCenter.objects.filter(centerid=inputid, password=password)
        openid = ret1[0].wxid
    else:
        tk = json.loads(urllib2.urlopen(oauth_url %(center.appid,center.secret,code)).read())
        if 'openid' in tk:
            openid = tk['openid'] #重新生成
        elif 'openid' in request.session:
            openid = request.session['openid'] #缓存
        else:
            openid = ''
        ret1 = JypayCenter.objects.filter(wxid=openid)
    if len(ret1) != 1:
        return HttpResponse('<h1>只有商户中心才可以注册收款渠道</h1>')
    else:
        request.session['openid'] = openid
        context = { 'center':ret1[0], 'cssfile':center.cssfile, 'f_link':f_link, 'f_name':f_name }
        return render(request, 'jypay/register.html', context)

@csrf_exempt
def doregister(request):
    isb = request.POST.get('isb')
    phone = request.POST.get('phone')
    password = request.POST.get('password')
    type = request.POST.get('type')
    name = request.POST.get('name')
    pic = request.POST.get('pic')
    description = request.POST.get('description')
    centerid = request.POST.get('centerid')
    memberid = request.POST.get('memberid')
    accountinfo = request.POST.get('accountinfo')
    if isb=='0':
        if not (phone and password and type):
            return HttpResponse('电话、密码不能为空')
        try:
            ret = JypayMember.objects.get(phone=phone)
            ret.password = password
            ret.name = name
            ret.type = type
            ret.pic = pic
            ret.description = description
        except:
            ret = JypayUser(phone=phone, password=password, name=name, type=type, pic=pic, description=description, \
            jointime=str(datetime.date.today()))
        ret.save()
        return HttpResponse(ret.userid)
    else:
        if not (memberid and password and centerid and accountinfo and type):
            return HttpResponse('所有项目均须填写')
        newid = centerid + "_" + memberid
        if JypayMember.objects.filter(memberid=newid):
            return HttpResponse('此商户ID已注册过')
        center = JypayCenter.objects.get(centerid=centerid)
        if len(JypayMember.objects.filter(fromagent=centerid)) >= center.limit:
            return HttpResponse('已达到渠道数上限，请联系代理商提升您的商户等级')
        nm = JypayMember(memberid=newid, password=password, accountinfo=accountinfo, fromagent=centerid, type=type, \
        jointime=str(datetime.date.today()))
        nm.save()
        return HttpResponse(nm.memberid + u'注册成功')

@csrf_exempt
def updateuser(request):
    userid = request.POST.get('userid')
    memberid = request.POST.get('memberid')
    centerid = request.POST.get('centerid')
    phone = request.POST.get('phone')
    password = request.POST.get('password')
    name = request.POST.get('name')
    pic = request.POST.get('pic')
    logo = request.POST.get('logo')
    description = request.POST.get('description')
    address = request.POST.get('address')
    type1 = request.POST.get('type1')
    type2 = request.POST.get('type2')
    type3 = request.POST.get('type3')
    type4 = request.POST.get('type4')
    type5 = request.POST.get('type5')
    type6 = request.POST.get('type6')
    man = request.POST.get('man')
    jian = request.POST.get('jian')
    if userid:
        ret = JypayUser.objects.filter(userid=userid)[0]
        ret.logo = logo
    elif memberid:
        ret = JypayMember.objects.filter(memberid=memberid)[0]
    elif centerid:
        ret = JypayCenter.objects.filter(centerid=centerid)[0]
        ret.logo = logo
        ret.type1 = type1
        ret.type2 = type2
        ret.type3 = type3
        ret.type4 = type4
        ret.type5 = type5
        ret.type6 = type6
        ret.man = man
        ret.jian = jian
    else:
        return HttpResponse('无法找到修改对象')
    try:
        ret.password = password
        ret.name = name
        ret.pic = pic
        ret.description = description
        ret.address =  address
        ret.phone = phone
        ret.save()
        return HttpResponse('信息更新成功')
    except:
        return HttpResponse('更新失败，请重新再试')

@csrf_exempt
def uploadimg(request):
    type = request.GET.get('type')
    ext = request.GET.get('ext')
    url = 'http://123.206.26.34/html/upload/upload.php?type='+type+'&ext='+ext
    request = urllib2.Request(url, request.body)
    response = urllib2.urlopen(request)
    return HttpResponse(response.read())

def tip(request):
    inputid = request.GET.get('memberid')
    password = request.GET.get('password')
    if inputid and password:
        ret1 = JypayMember.objects.filter(memberid=inputid, password=password)
    elif 'openid' not in request.session:
        return HttpResponse('<h1>请重新登录渠道页面</h1>')
    else:
        ret1 = JypayMember.objects.filter(wxid=request.session['openid'])
    if len(ret1) != 1:
        return HttpResponse('<h1>商户认证失败</h1>')
    else:
        center = JypayCenter.objects.get(centerid=ret1[0].fromagent)
        if center.description[:4] == 'http':
            f_link = center.description
            f_name = center.name
        else:
            f_link = 'http://www.jyousoft.com'
            f_name = u'捷优软件'
        comments = []
        for c in JypayComment.objects.filter(memberid=ret1[0].memberid, tip=0).order_by('-commentid'):
            u = JypayUser.objects.get(userid=c.userid)
            comments.append({'pic':u.pic, 'name':u.name or u.phone or u'匿名', 'commentid':c.commentid, 'status':c.status,
            'content':c.content, 'date':c.date})
        context = { 'comments':comments, 'cssfile':center.cssfile, 'f_link':f_link, 'f_name':f_name }
        return render(request, 'jypay/tip.html', context)

@csrf_exempt
def dotip(request):
    commentid = request.POST.get('commentid')
    tipamount = 1
    ret = JypayComment.objects.get(commentid=int(commentid))
    if ret.tip > 0:
        return HttpResponse('该评论已打赏过')
    else:
        ret1 = JypayMember.objects.get(memberid=ret.memberid)
        if ret1.balance < tipamount:
            return HttpResponse('商户余额需大于%d元' %tipamount)
        else:
            ret.tip += tipamount
            ret.save()
            ret1.balance -= tipamount
            ret1.save()
            ret2 = JypayUser.objects.get(userid=ret.userid)
            ret2.balance += tipamount
            ret2.save()
            return HttpResponse('成功打赏%d元' %tipamount)

def bind(request, cname):
    code = request.GET.get('code')
    center = JypayCenter.objects.get(centerid=cname)
    if center.description[:4] == 'http':
        f_link = center.description
        f_name = center.name
    else:
        f_link = 'http://www.jyousoft.com'
        f_name = u'捷优软件'
    tk = json.loads(urllib2.urlopen(oauth_url %(center.appid,center.secret,code)).read())
    if 'openid' in tk:
        openid = tk['openid'] #重新生成
    elif 'openid' in request.session:
        openid = request.session['openid'] #缓存
    else:
        openid = ''
    context = { 'centerid':center.centerid, 'openid':openid, 'cssfile':center.cssfile, 'f_link':f_link, 'f_name':f_name }
    return render(request, 'jypay/bind.html', context)

@csrf_exempt
def dobind(request):
    centerid = request.POST.get('centerid')
    openid = request.POST.get('openid')
    memberid = request.POST.get('memberid')
    password = request.POST.get('password')
    type = request.POST.get('type')
    if not centerid or not openid:
        return HttpResponse('商户号或微信ID获取失败')
    if type=='1':
        try:
            ret = JypayCenter.objects.get(centerid=centerid, password=password)
            for old in JypayCenter.objects.filter(wxid=openid):
                old.wxid = ""
                old.save()
            ret.wxid = openid
            ret.save()
            return HttpResponse('商户中心绑定成功，您可以进入商户中心及注册收款渠道了')
        except:
            return HttpResponse('信息输入错误，请确认用户名密码输入正确')
    elif type=='0':
        mid = centerid + "_" + memberid
        try:
            ret = JypayMember.objects.get(memberid=mid, password=password)
            for old in JypayMember.objects.filter(wxid=openid):
                old.wxid = ""
                old.save()
            ret.wxid = openid
            ret.save()
            return HttpResponse("收款渠道绑定成功，您可以进入渠道页面编辑信息、查看收款二维码页面了")
        except:
            return HttpResponse("信息输入错误，请确认用户名密码输入正确")

@csrf_exempt
def payable(request):
    pr = request.POST.get('pay_real')
    pb = request.POST.get('pay_balance')
    oid = request.POST.get('openid')
    mid = request.POST.get('memberid')
    otid = mid+'-'+str(int(time.time())) #不能含有.
    try:
        ret = JypayMember.objects.get(memberid=mid)
        center = JypayCenter.objects.get(centerid=ret.fromagent)
    except:
        return HttpResponse('未找到该渠道')
    if oid: #wxpy
        parameter = {
        'appId': center.appid,
        'appSecret': center.secret,
        'mch_id': center.mch_id,
        'partnerKey': center.partnerkey,
        'notify_url': wx_notify_url,
        'body': 'Jyousoft wxpay',
        'openid': oid,
        'out_trade_no': otid,
        'spbill_create_ip': request.META.get('REMOTE_ADDR', ''),
        'total_fee': str(int(float(pr)*100)),
        }
        JypayRecord(orderid=otid, memberid=mid, userid=0, type='wx', detail=pr+'-'+pb, amount=0, status=2).save()
        #JypayRecord(orderid=otid, memberid=mid, userid=0, type='wx', detail=str(build_form(parameter)).replace(" u'", "'"), amount=0, status=2).save() #This is for debuging
        return HttpResponse(str(build_form(parameter)).replace(" u'", "'"))
    else: #alipay
        aliprivate ='-----BEGIN RSA PRIVATE KEY-----\n'+center.aliprivate+'\n-----END RSA PRIVATE KEY-----'
        alipublic = '-----BEGIN PUBLIC KEY-----\n'+center.alipublic+'\n-----END PUBLIC KEY-----'
        paybar = alipay.AliPay(appid=center.aliappid, app_notify_url=ali_notify_url, app_private_key_string=aliprivate, alipay_public_key_string=alipublic, sign_type="RSA", debug=True)
        order_string = paybar.api_alipay_trade_wap_pay(
            out_trade_no=otid,
            total_amount=float(pr),
            subject='支付宝消费',
            return_url=ali_return_url % mid)
        JypayRecord(orderid=otid, memberid=mid, userid=0, type='alipay', detail=pr+'-'+pb, amount=0, status=2).save()
        return HttpResponse(aligateway+order_string)

@csrf_exempt
def payment_notify_ali(request):
    otid = request.POST.get('out_trade_no')
    transaction_id = request.POST.get('trade_no')
    userid = request.POST.get('buyer_id')
    bank_type = 'alipay'
    if (request.POST.get('notify_type') == 'trade_status_sync' and request.POST.get('trade_status') == 'TRADE_SUCCESS'): #Alipay
        if checkin(transaction_id, userid, bank_type, otid) == 'success':
            return HttpResponse('Success')
    return HttpResponse('Ali Notify not recognized!')

@csrf_exempt
def payment_notify_wx(request):
    params = xml_to_dict(request.body)
    otid = params['out_trade_no']
    transaction_id = params['transaction_id']
    openid = params['openid']
    bank_type = params['bank_type']
    if params['return_code'] == 'SUCCESS': #Wxpay
        if checkin(transaction_id, openid, bank_type, otid) == 'success':
            return HttpResponse('<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>')
    return HttpResponse('WX Notify not recognized!')

def checkin(transaction_id, openid, bank_type, otid):
    try:
        rc = JypayRecord.objects.get(orderid=otid)
    except:
        return 'Record not found'
    pr,pb = rc.detail.split("-")
    mid = rc.memberid
    pr = float(pr)
    pb = float(pb)
    income = pr + pb
    try:#商户入帐
        ret = JypayMember.objects.get(memberid=mid)
    except:
        return 'Member not found'
    center = JypayCenter.objects.get(centerid=ret.fromagent)
    if center.man == 0:
        m_return = 0
    else:
        m_return = int(income/center.man)*center.jian
    m_realin = income-m_return
    ret.balance += m_realin
    center.balance += pr
    ret.total += m_realin
    center.total += pr
    ret.save()
    center.save()
    #商户提醒
    body={"touser":ret.wxid,
          "template_id":center.wxtemplate,
          "url":"",
          "topcolor":"#173177",
          "data":{
              "keyword1":{"value":str(datetime.datetime.now())[:-7],"color":"#173177"},
              "keyword2":{"value":bank_type,"color":"#173177"},
              "keyword3":{"value":str(m_realin),"color":"#173177"},
              "keyword4":{"value":mid,"color":"#173177"},
              "keyword5":{"value":transaction_id,"color":"#173177"}}}
    token = json.loads(urllib2.urlopen(access_url%(center.appid,center.secret)).read())['access_token']
    urllib2.urlopen(urllib2.Request(remind_url%token, json.dumps(body, ensure_ascii=False)))
    try:#消费者入帐
        ret1 = JypayUser.objects.get(wxid=openid)
        ret1.total += pr
        ret1.balance += m_return - pb
        ret1.save()
    except:
        ret1 = JypayUser(wxid=openid, type=1, jointime=str(datetime.date.today())) #新建支付宝用户
        ret1.total += pr
        ret1.balance += m_return - pb
        ret1.save()
    detail_str = u"商家实收"+str(m_realin)+u"返现"+str(m_return)+u"（"+str(pb)+u"来自余额）, 订单编号："+transaction_id
    rc.userid = ret1.userid
    rc.type = bank_type
    rc.detail = detail_str
    rc.amount = m_realin
    rc.status = 1
    rc.save()
    return 'success'
